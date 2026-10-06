"""myssia-urlwatch 适配器:子进程调用上游 urlwatch(BSD-3-Clause)——MYIA 侧代码.

本文件由 MYIA 仓库创作与维护,**不是**上游代码;上游 urlwatch
(BSD-3-Clause,thp/urlwatch)不 vendor、不复制,以 ``uv run --no-project
--with urlwatch`` 的 pip 依赖形态隔离调用,依赖只进 uv 缓存的临时环境,
绝不进根依赖。版本不钉(裁定 R-1 同款);测试全 mock 子进程,零网络。

适配器职责:对一组 URL 跑一次快照对比监控,产出结构化事件清单。上游
契约(2026-10-05 对 urlwatch 2.29 装包源码亲核):

- 上游 CLI **无 JSON reporter**(reporter 词表全是人读型:text/markdown/
  html/stdout/…),故子进程内跑 :data:`SHIM_SOURCE`(MYIA 自写薄 shim,
  非上游代码)借其 Python API 结构化取事件;
- shim 复用上游 ``worker.run_jobs`` 主循环(抓取/过滤/对比/重试语义原样),
  只把 ``report`` 换成 JSON collector(``new``/``changed``/``unchanged``/
  ``error`` 事件;上游 Report 是鸭子类型,collector 同形);
- jobs 文件是上游 ``UrlsYaml`` 多文档 YAML(每 doc 一个 ``{name, url}``
  映射,JSON 即合法 YAML 流映射);快照缓存走 ``CacheMiniDBStorage``
  (minidb 文件,跨 run 持久——**首次跑全部 new**,之后才有 changed 判定);
- URL 去重语义在上游是硬错(重复 guid 抛 ValueError),适配器侧预去重
  (保序,首个胜出)避免整跑报废。

错误契约(spec python/error-handling):所有失败抛 :class:`UrlwatchAdapterError`
(code + message + 结构化 details)。code 词表:

- ``url_invalid``          输入 URL 非法(非 http/https、空、超上限)
- ``uv_missing``           宿主无 uv(隔离运行时不可用=上游依赖缺失的结构化形态)
- ``urlwatch_failed``      子进程非零退出(采集失败)
- ``urlwatch_timeout``     子进程超过 wall-clock 预算(采集失败)
- ``urlwatch_output_invalid``  退出 0 但 stdout 不是可解析的事件 JSON

零变更 = 合法空态(status success,counts.changed 0),不是错误;``deferred``
是上游 max_tries 重试未到报错阈值、本轮不判定的 job 数(checked - 事件数)。
铁律:任何失败只影响本次调用,核心品类流水线照常跑通(测试钉在
tests/plugins/test_urlwatch_plugin.py)。

采集边界:逐 URL 直连抓取由使用者自负其责(授权监控目标);本件零凭据
注入,零第三方聚合服务器(不经过任何厂商 SaaS,P0 本地执行硬规则)。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

__all__ = [
    "DEFAULT_CACHE_FILE",
    "DEFAULT_TIMEOUT_SECONDS",
    "MAX_URLS_PER_RUN",
    "URLWATCH_DEPENDENCIES",
    "UrlwatchAdapterError",
    "build_command",
    "is_available",
    "normalize_urls",
    "plugin_dir",
    "run",
    "write_jobs_yaml",
]

#: 适配器所在插件目录(本文件按样板布局固定在 plugins/myssia-urlwatch/ 下)。
PLUGIN_DIR = Path(__file__).resolve().parent

#: 隔离子进程注入的上游依赖(BSD-3-Clause;不钉版,见模块 docstring)。
URLWATCH_DEPENDENCIES = ("urlwatch", "cssselect")

#: 快照缓存缺省落位(MYIA_HOME 桌面数据路径约定;minidb 文件,跨 run 持久)。
DEFAULT_CACHE_FILE = Path.home() / ".myia" / "urlwatch" / "cache.db"

#: 子进程 wall-clock 预算缺省值(≤64 URL × 上游单 job 60s 请求超时的有界预算)。
DEFAULT_TIMEOUT_SECONDS = 300.0

#: 单次 run 的 URL 上限(桌面缺省必须有界;更多目标分批跑)。
MAX_URLS_PER_RUN = 64

#: 结构化事件里 diff 的截断上限(保持 JSON 输出有界)。
_DIFF_TAIL_CHARS = 4000

#: 结构化错误/trace 的截断上限。
_TEXT_TAIL_CHARS = 2000

#: URL 合法性:仅 http/https(上游 UrlJob 另支持 file:// 等,本件刻意收窄
#: ——网络监控语义);禁空白/控制字符(argv 不经过 URL,但 jobs 文件经
#: YAML 装载,提前拒脏输入)。
_ALLOWED_SCHEMES = ("http", "https")
_MAX_URL_LENGTH = 2048


class UrlwatchAdapterError(Exception):
    """结构化适配器错误:code + message + details,``to_dict()`` 进 JSON 输出."""

    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        """结构化形态:{"code", "message", **details}(供 --json 输出与 agent 自修)."""
        return {"code": self.code, "message": self.message, **self.details}


def plugin_dir() -> Path:
    """本插件目录(适配器所在处)."""
    return PLUGIN_DIR


#: GUI 态 PATH 常缺的 uv 已知落位(桌面壳 spawn sidecar 只注入 PYTHONPATH
#: 不补 PATH;Finder/Dock 启动的 app PATH 无 /opt/homebrew/bin 等——which
#: 未命中时按序探测这些绝对路径兜底,本机实测两处双在位)。Windows 官方
#: 安装器落 %USERPROFILE%\.local\bin\uv.exe(winget/scoop 另有 PATH 注入,
#: GUI 态兜底仍取官方位)。
_KNOWN_UV_PATHS: tuple[Path, ...] = (
    Path.home() / ".local" / "bin" / ("uv.exe" if sys.platform == "win32" else "uv"),
    Path("/opt/homebrew/bin/uv")
    if sys.platform == "darwin"
    else Path("/nonexistent/uv"),
    Path("/usr/local/bin/uv"),
)


def uv_executable() -> str | None:
    """解析 uv 可执行路径:PATH(which)优先,GUI 态 PATH 缺失走已知落位."""
    found = shutil.which("uv")
    if found:
        return found
    for candidate in _KNOWN_UV_PATHS:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def is_available() -> bool:
    """运行前提是否就位:宿主有 uv(上游依赖经 uv 临时环境注入)."""
    return uv_executable() is not None


def _default_name(url: str) -> str:
    """从 URL 派生可读名:host + path(去尾斜杠),退化即 URL 本身."""
    parts = urlparse(url)
    name = (parts.netloc or url) + (parts.path or "").rstrip("/")
    return name or url


def normalize_urls(urls: Any) -> list[dict[str, str]]:
    """校验并规整输入 URL 清单:统一为 ``[{name, url}]`` job 描述.

    接受:单个 URL 字符串,或其序列;元素为字符串或 ``{"name":…, "url":…}``
    映射(name 可省,缺省从 URL 派生)。校验:仅 http/https、无空白/控制
    字符、长度 ≤2048、总数 ≤:data:`MAX_URLS_PER_RUN`(空清单拒绝——监控
    什么都不监控没有意义)。重复 URL 去重保序(上游对重复 guid 是硬错,
    这里预去重避免整跑报废)。

    Raises:
        UrlwatchAdapterError: ``url_invalid``(任一校验不过)。
    """
    if isinstance(urls, str):
        items: list[Any] = [urls]
    elif isinstance(urls, (list, tuple)):
        items = list(urls)
    else:
        raise UrlwatchAdapterError(
            "url_invalid",
            f"urls 应为 URL 字符串或其列表,当前为 {type(urls).__name__}",
        )
    if not items:
        raise UrlwatchAdapterError("url_invalid", "urls 为空(至少给一个要监控的 URL)")
    if len(items) > MAX_URLS_PER_RUN:
        raise UrlwatchAdapterError(
            "url_invalid",
            f"单次 run 最多 {MAX_URLS_PER_RUN} 个 URL(当前 {len(items)}),更多目标请分批",
        )
    jobs: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        url = (
            item
            if isinstance(item, str)
            else (item.get("url") if isinstance(item, dict) else None)
        )
        if not isinstance(url, str) or not url.strip():
            raise UrlwatchAdapterError(
                "url_invalid",
                f"URL 项非法:{item!r}(须为字符串或含 url 键的映射)",
            )
        url = url.strip()
        if len(url) > _MAX_URL_LENGTH or any(
            ch.isspace() or ord(ch) < 32 for ch in url
        ):
            raise UrlwatchAdapterError(
                "url_invalid",
                f"URL 非法(含空白/控制字符或超 {_MAX_URL_LENGTH} 字符):{url[:80]!r}",
            )
        if urlparse(url).scheme not in _ALLOWED_SCHEMES:
            raise UrlwatchAdapterError(
                "url_invalid",
                f"URL 仅支持 http/https:{url[:80]!r}",
            )
        if url in seen:
            continue  # 重复 URL 去重保序(上游重复 guid 是硬错)
        seen.add(url)
        name = None
        job_filter = None
        if isinstance(item, dict):
            name = item.get("name")
            job_filter = item.get("filter")
        if not isinstance(name, str) or not name.strip():
            name = _default_name(url)
        job: dict[str, Any] = {"name": name.strip(), "url": url}
        # 可选内容过滤(10-06-ai-news-sources:官网页 watch 的框架噪声根治)
        # ——上游 UrlsYaml 原生 filter 链,如
        #   filter: [{"css": {"selector": "main", "format": "text"}}]
        # css 过滤器需 cssselect(URLWATCH_DEPENDENCIES 随带);形状校验只做
        # 浅层(非空列表/子键映射),具体过滤器参数由上游装载期校验。
        if job_filter is not None:
            if (
                not isinstance(job_filter, list)
                or not job_filter
                or not all(isinstance(sub, dict) and sub for sub in job_filter)
            ):
                raise UrlwatchAdapterError(
                    "url_invalid",
                    f"job 的 filter 应为非空子过滤器映射列表(上游 UrlsYaml 形态),"
                    f"当前为 {job_filter!r}",
                )
            job["filter"] = job_filter
        jobs.append(job)
    return jobs


def write_jobs_yaml(jobs: list[dict[str, str]], path: str | Path) -> None:
    """把 job 描述写成上游 UrlsYaml 多文档 YAML(JSON 即合法 YAML 流映射)."""
    docs = "\n---\n".join(json.dumps(job, ensure_ascii=False) for job in jobs)
    Path(path).write_text(f"{docs}\n", encoding="utf-8")


#: 隔离环境内跑的 MYIA 薄 shim(**非上游代码**):复用上游 ``worker.run_jobs``
#: 主循环(抓取/过滤/对比/max_tries 重试语义原样),只把 report 换成 JSON
#: collector——上游 Report 是鸭子类型(new/changed/unchanged/error 同形)。
#: stdout 只打印这一个 JSON 对象(上游 logging 走 stderr,不污染)。
SHIM_SOURCE = '''\
"""MYIA shim: run urlwatch jobs, emit JSON events (runs inside uv temp env)."""
import argparse
import json
from types import SimpleNamespace

import urlwatch
from urlwatch.storage import CacheMiniDBStorage, UrlsYaml
from urlwatch.worker import run_jobs


class Collector:
    def __init__(self):
        self.events = []

    def _record(self, verb, job_state):
        job = job_state.job
        event = {
            "event": verb,
            "name": job.pretty_name(),
            "location": job.get_location(),
            "timestamp": job_state.timestamp,
        }
        if verb == "changed":
            try:
                event["diff"] = job_state.get_diff()
            except Exception as exc:  # noqa: BLE001 - diff 工具失败不让事件丢失
                event["diff"] = ""
                event["diff_error"] = str(exc)
        if verb == "error":
            event["error"] = str(job_state.exception)
            event["traceback_tail"] = (job_state.traceback or "")[-2000:]
        self.events.append(event)

    def new(self, job_state):
        self._record("new", job_state)

    def changed(self, job_state):
        self._record("changed", job_state)

    def unchanged(self, job_state):
        self._record("unchanged", job_state)

    def error(self, job_state):
        self._record("error", job_state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", required=True)
    parser.add_argument("--cache", required=True)
    args = parser.parse_args()

    jobs = UrlsYaml(args.jobs).load()
    cache = CacheMiniDBStorage(args.cache)
    collector = Collector()
    urlwatcher = SimpleNamespace(
        urlwatch_config=SimpleNamespace(tags=None, idx_set=set(), joblist=[]),
        jobs=jobs,
        cache_storage=cache,
        config_storage=SimpleNamespace(config={"job_defaults": {}, "display": {}}),
        report=collector,
        should_run=lambda idx, job: True,
    )
    try:
        run_jobs(urlwatcher)
    finally:
        cache.close()
    payload = {
        "urlwatch_version": getattr(urlwatch, "__version__", None),
        "checked": len(jobs),
        "events": collector.events,
    }
    print(json.dumps(payload, ensure_ascii=False))


if __name__ == "__main__":
    main()
'''


def build_command(
    shim_path: str | Path,
    jobs_path: str | Path,
    cache_path: str | Path,
    uv: str = "uv",
) -> list[str]:
    """装配隔离子进程命令:uv 临时环境跑 MYIA shim(借上游 Python API).

    ``uv`` 可注入绝对路径(GUI 态 which 未命中、经 :func:`uv_executable`
    已知落位解析出的形态);缺省字面 ``uv`` 走子进程 PATH 解析不变。
    """
    command = [uv, "run", "--no-project"]
    for dependency in URLWATCH_DEPENDENCIES:
        command += ["--with", dependency]
    command += [
        "python",
        str(shim_path),
        "--jobs",
        str(jobs_path),
        "--cache",
        str(cache_path),
    ]
    return command


def _tail(text: str | None, limit: int = _TEXT_TAIL_CHARS) -> str:
    """文本摘录(尾部),保持结构化结果有界."""
    return (text or "").strip()[-limit:]


def parse_payload(raw: str) -> dict[str, Any]:
    """解析 shim stdout:须是含 ``events`` 列表与 ``checked`` 计数的 JSON 对象.

    Raises:
        UrlwatchAdapterError: ``urlwatch_output_invalid``(不可解析/形状不对)。
    """
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError) as exc:
        raise UrlwatchAdapterError(
            "urlwatch_output_invalid",
            f"shim stdout 不是可解析 JSON:{exc}",
        ) from exc
    if (
        not isinstance(payload, dict)
        or not isinstance(payload.get("events"), list)
        or not isinstance(payload.get("checked"), int)
    ):
        raise UrlwatchAdapterError(
            "urlwatch_output_invalid",
            f"shim 输出形状不对(缺 events 列表/checked 计数):{str(raw)[:120]!r}",
        )
    return payload


def _normalize_events(events: list[Any]) -> list[dict[str, Any]]:
    """shim 事件 → 有界结构化事件(diff/error 截尾,只留标量字段)."""
    normalized: list[dict[str, Any]] = []
    for event in events:
        if not isinstance(event, dict):
            continue
        item: dict[str, Any] = {
            "event": event.get("event"),
            "name": event.get("name"),
            "location": event.get("location"),
        }
        if isinstance(event.get("timestamp"), (int, float)):
            item["timestamp"] = event["timestamp"]
        if event.get("event") == "changed":
            item["diff"] = _tail(event.get("diff"), _DIFF_TAIL_CHARS)
            if event.get("diff_error"):
                item["diff_error"] = _tail(event.get("diff_error"))
        if event.get("event") == "error":
            item["error"] = _tail(event.get("error"))
        normalized.append(item)
    return normalized


def run(
    urls: Any,
    *,
    cache_file: str | Path | None = None,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """对 ``urls`` 跑一次快照对比监控(new/changed/unchanged/error 事件).

    Args:
        urls: URL 字符串或其列表(元素可为 ``{"name":…, "url":…}``;校验见
            :func:`normalize_urls`;授权监控目标,边界由使用者自负)。
        cache_file: 快照缓存落位(缺省 ``~/.myia/urlwatch/cache.db``;**跨 run
            持久**——首次跑全部 new,换路径即换基线)。
        timeout: 子进程 wall-clock 预算秒数,超时抛 ``urlwatch_timeout``。
        runner: subprocess.run 注入口(测试 mock 用)。
        clock: 单调时钟注入口(测试 mock 用)。

    Returns:
        结构化结果 dict:plugin/status/checked/counts{new,changed,
        unchanged,error,deferred}/events/cache_file/command/exit_code/
        duration_seconds/urlwatch_version。

    Raises:
        UrlwatchAdapterError: 全部失败形态都是结构化错误(见模块 docstring 词表)。
        零变更不是错误:status=success 且 counts.changed=0(合法空态)。
    """
    do_run = runner if runner is not None else subprocess.run
    jobs = normalize_urls(urls)
    uv = uv_executable()
    if uv is None:
        raise UrlwatchAdapterError(
            "uv_missing",
            "隔离运行时不可用: PATH 上找不到 uv,已知落位"
            f"({', '.join(str(p) for p in _KNOWN_UV_PATHS)})也不存在"
            "(https://docs.astral.sh/uv/)。适配器以 uv 临时环境运行上游"
            " urlwatch,依赖不进根依赖。",
            checked=len(jobs),
        )
    cache_path = (
        Path(cache_file).expanduser() if cache_file is not None else DEFAULT_CACHE_FILE
    )
    started = clock()
    with tempfile.TemporaryDirectory(prefix="myssia-urlwatch-") as scratch:
        scratch_dir = Path(scratch)
        shim_path = scratch_dir / "shim.py"
        jobs_path = scratch_dir / "urls.yaml"
        shim_path.write_text(SHIM_SOURCE, encoding="utf-8")
        write_jobs_yaml(jobs, jobs_path)
        command = build_command(shim_path, jobs_path, cache_path, uv=uv)
        try:
            completed = do_run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise UrlwatchAdapterError(
                "urlwatch_timeout",
                f"urlwatch 子进程超过 {timeout:g}s 预算被终止({len(jobs)} 个 URL)",
                timeout_seconds=timeout,
                url_count=len(jobs),
                stderr_tail=_tail(exc.stderr if isinstance(exc.stderr, str) else None),
            ) from exc
        duration = round(clock() - started, 3)
        if completed.returncode != 0:
            raise UrlwatchAdapterError(
                "urlwatch_failed",
                f"urlwatch 子进程非零退出(code={completed.returncode};{len(jobs)} 个 URL)",
                exit_code=completed.returncode,
                stderr_tail=_tail(completed.stderr),
                stdout_tail=_tail(completed.stdout),
            )
        payload = parse_payload(completed.stdout)
    events = _normalize_events(payload["events"])
    counts = {verb: 0 for verb in ("new", "changed", "unchanged", "error")}
    for event in events:
        if event.get("event") in counts:
            counts[event["event"]] += 1
    checked = int(payload["checked"])
    counts["deferred"] = max(0, checked - len(events))
    return {
        "plugin": "myssia-urlwatch",
        "status": "success",
        "checked": checked,
        "counts": counts,
        "events": events,
        "cache_file": str(cache_path),
        "command": command,
        "exit_code": completed.returncode,
        "duration_seconds": duration,
        "urlwatch_version": payload.get("urlwatch_version"),
    }
