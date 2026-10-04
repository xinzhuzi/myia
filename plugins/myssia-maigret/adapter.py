"""myssia-maigret 适配器:子进程调用上游 maigret(MIT)——MYIA 侧代码.

本文件由 MYIA 仓库创作与维护,**不是**上游代码;上游 maigret(MIT,
soxoj/maigret)不 vendor、不复制,以 ``uv run --no-project --with maigret``
的 pip 依赖形态隔离调用,依赖只进 uv 缓存的临时环境,绝不进根依赖。
版本不钉(裁定 R-1):站点库随上游自更新;测试全 mock 子进程,零网络。

适配器职责:对一个用户名跑一次跨站侦察(``-J simple`` JSON 报告),解析
报告装配结构化命中清单。报告契约(2026-10-05 对 maigret v0.6.6 实测):

- 报告文件落 ``--folderoutput`` 目录,名如 ``report_<username>_simple.json``
  (适配器按 ``*.json`` glob 兜底,取 mtime 最新,免钉文件名);
- 顶层 = {站点键: 条目};条目的**命中对象**在 ``entry["status"]`` 键下
  (未命中为 None),内层字段 ``site_name``/``url``/``status``("Claimed" 等)/
  ``ids``/``tags``——上游把完整结果叫 status,是它的命名,如实适配。

错误契约(spec python/error-handling):所有失败抛 :class:`MaigretAdapterError`
(code + message + 结构化 details)。code 词表:

- ``username_invalid``  用户名非法(防 argv 注入:首字符禁 ``-``)
- ``uv_missing``        宿主无 uv(隔离运行时不可用)
- ``maigret_failed``    maigret 子进程非零退出(采集失败)
- ``maigret_timeout``   子进程超过 wall-clock 预算(采集失败)
- ``maigret_report_missing`` / ``maigret_report_invalid``
                       退出 0 但报告缺失/不可解析(采集失败)

零命中 = 合法空态(status success,hit_count 0),不是错误。
失败码 → CLI 退出码的映射归 CLI 所有(:data:`myssia.cli.MAIGRET_FETCH_FAILURE_CODES`);
适配器只负责如实上报 code。铁律:任何失败只影响 ``myssia maigret`` 自身,
核心品类流水线照常跑通(测试钉在 tests/plugins/test_maigret_plugin.py)。

采集边界:逐站点直连查询由使用者自负其责(授权侦察目标);本件零凭据
注入,零第三方聚合服务器(不经过任何厂商 SaaS,P0 本地执行硬规则)。
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

__all__ = [
    "DEFAULT_SITE_TIMEOUT_SECONDS",
    "DEFAULT_TIMEOUT_SECONDS",
    "DEFAULT_TOP_SITES",
    "MAIGRET_DEPENDENCIES",
    "MaigretAdapterError",
    "build_command",
    "is_available",
    "normalize_username",
    "parse_report",
    "plugin_dir",
    "run",
]

#: 适配器所在插件目录(本文件按样板布局固定在 plugins/myssia-maigret/ 下)。
PLUGIN_DIR = Path(__file__).resolve().parent

#: 隔离子进程注入的上游依赖(MIT;不钉版,见模块 docstring 裁定 R-1)。
MAIGRET_DEPENDENCIES = ("maigret",)

#: 缺省扫描范围:站点库 rank 前 N 站(全库数千站要数小时,桌面缺省必须有界)。
DEFAULT_TOP_SITES = 100

#: 子进程 wall-clock 预算缺省值(整个侦察过程;top-100 站量级实测分钟级)。
DEFAULT_TIMEOUT_SECONDS = 600.0

#: 单站点超时缺省秒数(上游 ``--timeout``,逐站请求超时)。
DEFAULT_SITE_TIMEOUT_SECONDS = 15.0

#: 用户名合法性(maigret 站点模板的公共子集;首字符禁 ``-`` = argv 注入面)。
_USERNAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")

#: 结构化错误里 stderr/stdout 摘录的上限(保持 JSON 输出有界)。
_PROCESS_TAIL_CHARS = 2000


class MaigretAdapterError(Exception):
    """结构化适配器错误:code + message + details,``to_dict()`` 进 JSON 输出."""

    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        """结构化形态:{"code", "message", **details}(供 CLI --json 与 agent 自修)."""
        return {"code": self.code, "message": self.message, **self.details}


def plugin_dir() -> Path:
    """本插件目录(适配器所在处)."""
    return PLUGIN_DIR


def is_available() -> bool:
    """运行前提是否就位:宿主有 uv(上游依赖经 uv 临时环境注入)."""
    return shutil.which("uv") is not None


def normalize_username(username: str) -> str:
    """校验用户名:公共字符集子集 + 首字符禁 ``-``(防 argv 注入)."""
    value = (username or "").strip()
    if not _USERNAME_RE.fullmatch(value):
        raise MaigretAdapterError(
            "username_invalid",
            f"用户名非法:{value!r}(须字母数字开头,仅字母/数字/./_/-,≤64 字符)",
            username=value,
        )
    return value


def build_command(
    username: str,
    output_dir: str | Path,
    *,
    top_sites: int | None = DEFAULT_TOP_SITES,
    site_timeout: float = DEFAULT_SITE_TIMEOUT_SECONDS,
    extra_args: tuple[str, ...] | list[str] = (),
) -> list[str]:
    """装配隔离子进程命令:uv 临时环境按需装 maigret,再跑其 CLI.

    ``-J simple`` JSON 报告落 ``--folderoutput``;``--no-color
    --no-progressbar`` 保输出干净;``--top-sites`` 按站点 rank 前置预算
    (桌面缺省必须有界);``--timeout`` 是上游的**逐站**请求超时。
    """
    command = ["uv", "run", "--no-project"]
    for dependency in MAIGRET_DEPENDENCIES:
        command += ["--with", dependency]
    command += [
        "maigret",
        username,
        "-J",
        "simple",
        "--folderoutput",
        str(output_dir),
        "--no-color",
        "--no-progressbar",
        "--timeout",
        str(site_timeout),
    ]
    if top_sites is not None and top_sites > 0:
        command += ["--top-sites", str(top_sites)]
    command += [*extra_args]
    return command


def _tail(text: str | None) -> str:
    """进程输出摘录(尾部),保持结构化错误有界."""
    value = (text or "").strip()
    return value[-_PROCESS_TAIL_CHARS:]


def parse_report(report: dict[str, Any]) -> list[dict[str, Any]]:
    """解析 maigret simple 报告:命中对象在条目 ``status`` 键下(实测契约).

    每个命中进 ``hits``:site/url/status(内层,恒 Claimed 族)/rank/
    is_similar/tags/ids(仅保留标量值,富 id 如粉丝数可很大但键少,有界)。
    """
    hits: list[dict[str, Any]] = []
    for entry in report.values():
        if not isinstance(entry, dict):
            continue
        found = entry.get("status")
        if not isinstance(found, dict):
            continue  # 未命中(None)或异常形态:跳过,不算失败
        site_meta = entry.get("site") if isinstance(entry.get("site"), dict) else {}
        ids = {
            key: value
            for key, value in (found.get("ids") or {}).items()
            if isinstance(value, (str, int, float, bool))
        }
        hits.append(
            {
                "site": found.get("site_name") or site_meta.get("name"),
                "url": found.get("url"),
                "status": found.get("status"),
                "rank": entry.get("rank"),
                "is_similar": entry.get("is_similar"),
                "tags": found.get("tags") or [],
                "ids": ids,
            }
        )
    return hits


def _read_report(output_dir: Path) -> dict[str, Any]:
    """读回报告文件:glob ``*.json`` 取 mtime 最新(上游文件名含用户名+类型,
    钉死文件名反而脆)。零文件=missing;不可解析=invalid。"""
    candidates = sorted(
        output_dir.glob("*.json"), key=lambda path: path.stat().st_mtime, reverse=True
    )
    if not candidates:
        raise MaigretAdapterError(
            "maigret_report_missing",
            f"maigret 退出 0 但 {output_dir} 下没有任何 JSON 报告",
        )
    try:
        report = json.loads(candidates[0].read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        raise MaigretAdapterError(
            "maigret_report_invalid",
            f"maigret 报告 {candidates[0].name} 不可解析:{exc}",
        ) from exc
    if not isinstance(report, dict):
        raise MaigretAdapterError(
            "maigret_report_invalid",
            f"maigret 报告不是对象:{type(report).__name__}",
        )
    return report


def run(
    username: str,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    top_sites: int | None = DEFAULT_TOP_SITES,
    site_timeout: float = DEFAULT_SITE_TIMEOUT_SECONDS,
    extra_args: tuple[str, ...] | list[str] = (),
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """对 ``username`` 跑一次上游 maigret 跨站侦察.

    Args:
        username: 待查用户名(授权侦察目标,由使用者自负边界)。
        timeout: 子进程 wall-clock 预算秒数,超时抛 ``maigret_timeout``。
        top_sites: 站点 rank 前 N 预算(None=全库,慎用,可达数小时)。
        site_timeout: 逐站请求超时秒数(上游 ``--timeout``)。
        extra_args: 透传给上游 CLI 的附加参数。
        runner: subprocess.run 注入口(测试 mock 用)。
        clock: 单调时钟注入口(测试 mock 用)。

    Returns:
        结构化结果 dict:plugin/target/status/command/exit_code/
        duration_seconds/top_sites/site_timeout/hit_count/hits。

    Raises:
        MaigretAdapterError: 全部失败形态都是结构化错误(见模块 docstring 词表)。
        零命中不是错误:status=success 且 hit_count=0(合法空态)。
    """
    do_run = runner if runner is not None else subprocess.run
    clean_username = normalize_username(username)
    if shutil.which("uv") is None:
        raise MaigretAdapterError(
            "uv_missing",
            "隔离运行时不可用: PATH 上找不到 uv(https://docs.astral.sh/uv/)。"
            "适配器以 uv 临时环境运行上游 CLI,依赖不进根依赖。",
            username=clean_username,
        )
    started = clock()
    with tempfile.TemporaryDirectory(prefix="myssia-maigret-") as scratch:
        output_dir = Path(scratch) / "reports"
        command = build_command(
            clean_username,
            output_dir,
            top_sites=top_sites,
            site_timeout=site_timeout,
            extra_args=extra_args,
        )
        try:
            completed = do_run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise MaigretAdapterError(
                "maigret_timeout",
                f"maigret 子进程超过 {timeout:g}s 预算被终止(目标 {clean_username})",
                username=clean_username,
                timeout_seconds=timeout,
                stderr_tail=_tail(exc.stderr if isinstance(exc.stderr, str) else None),
            ) from exc
        duration = round(clock() - started, 3)
        if completed.returncode != 0:
            raise MaigretAdapterError(
                "maigret_failed",
                (
                    f"maigret 子进程非零退出(code={completed.returncode};"
                    f"目标 {clean_username})"
                ),
                username=clean_username,
                exit_code=completed.returncode,
                stderr_tail=_tail(completed.stderr),
                stdout_tail=_tail(completed.stdout),
            )
        report = _read_report(output_dir)
        hits = parse_report(report)
    return {
        "plugin": "myssia-maigret",
        "target": clean_username,
        "status": "success",
        "command": command,
        "exit_code": completed.returncode,
        "duration_seconds": duration,
        "top_sites": top_sites,
        "site_timeout": site_timeout,
        "hit_count": len(hits),
        "hits": hits,
    }
