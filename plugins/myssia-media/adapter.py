"""myssia-media 适配器:子进程调用上游 yt-dlp(公域,Unlicense)——MYIA 侧代码.

本文件由 MYIA 仓库创作与维护,**不是**上游代码;上游 yt-dlp(Unlicense)
不 vendor、不复制,以 ``uv run --no-project --with yt-dlp`` 的 pip 依赖形态
隔离调用,依赖只进 uv 缓存的临时环境,绝不进根依赖。版本不钉(裁定 R-1):
yt-dlp 抽取器时效即生命,每次取 uv 缓存最新版;测试全 mock 子进程,零网络。

适配器职责:对单个视频/频道/播放列表 URL 跑一次「扁平快扫」
(``--dump-single-json --flat-playlist``,不逐条解析媒体流),把上游 JSON
装配成结构化结果(items 有界、字段白名单)供 ``myssia media --json`` 与
agent 消费。

错误契约(spec python/error-handling):所有失败抛 :class:`MediaAdapterError`
(code + message + 结构化 details,``to_dict()`` 直接进 CLI 的 JSON 输出)。
code 词表:

- ``url_invalid``        目标不是 http(s) URL(用法/配置错误)
- ``uv_missing``         宿主无 uv(隔离运行时不可用)
- ``media_failed``       yt-dlp 子进程非零退出(采集失败;站点不支持/反爬/
                         地区限制等上游语义都在 stderr 摘录里)
- ``media_timeout``      子进程超过 wall-clock 预算(采集失败)
- ``media_output_invalid`` 退出 0 但 stdout JSON 缺失/不可解析(采集失败)

失败码 → CLI 退出码的映射归 CLI 所有(:data:`myssia.cli.MEDIA_FETCH_FAILURE_CODES`);
适配器只负责如实上报 code。铁律(security-baseline):任何失败只影响
``myssia media`` 自身,核心品类流水线照常跑通(测试钉在
tests/plugins/test_media_plugin.py)。

采集边界:目标由使用者指定,须遵守目标站点服务条款与当地法律;本适配器
不做任何凭据注入,仅公开可访问内容。
"""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

__all__ = [
    "DEFAULT_MAX_ITEMS",
    "DEFAULT_TIMEOUT_SECONDS",
    "ENTRY_FIELDS",
    "MediaAdapterError",
    "build_command",
    "is_available",
    "normalize_target",
    "plugin_dir",
    "run",
]

#: 适配器所在插件目录(本文件按样板布局固定在 plugins/myssia-media/ 下)。
PLUGIN_DIR = Path(__file__).resolve().parent

#: 隔离子进程注入的上游依赖(公域;不钉版,见模块 docstring 裁定 R-1)。
MEDIA_DEPENDENCIES = ("yt-dlp",)

#: 扁平快扫缺省返回条目上限(频道可达数千条,payload 必须有界)。
DEFAULT_MAX_ITEMS = 50

#: 单条条目进 payload 的字段白名单(其余上游字段一律丢弃,保持输出有界)。
ENTRY_FIELDS = (
    "id",
    "url",
    "title",
    "uploader",
    "channel",
    "duration",
    "view_count",
    "upload_date",
)

#: 子进程 wall-clock 预算缺省值(整个快扫过程,非单请求超时)。
DEFAULT_TIMEOUT_SECONDS = 180.0

#: 结构化错误里 stderr/stdout 摘录的上限(保持 JSON 输出有界)。
_PROCESS_TAIL_CHARS = 2000


class MediaAdapterError(Exception):
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


def normalize_target(target: str) -> str:
    """校验并规整采集目标:必须是 http(s) URL(防误用与 argv 注入面)."""
    value = (target or "").strip()
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise MediaAdapterError(
            "url_invalid",
            f"采集目标必须是 http(s) URL,当前为 {value!r}"
            "(示例:https://www.youtube.com/watch?v=… 或频道/播放列表页)",
            target=target,
        )
    return value


def build_command(
    target: str,
    *,
    max_items: int | None = None,
    extra_args: tuple[str, ...] | list[str] = (),
) -> list[str]:
    """装配隔离子进程命令:uv 临时环境按需装 yt-dlp,再跑其 CLI.

    ``--dump-single-json`` 单 JSON 输出到 stdout;``--flat-playlist`` 扁平快扫
    (频道/列表不逐条解析媒体流);``--no-warnings`` 保 stdout 纯 JSON;
    ``max_items`` 经上游 ``--playlist-end`` 预算前置(不在解析后再截)。
    """
    command = ["uv", "run", "--no-project"]
    for dependency in MEDIA_DEPENDENCIES:
        command += ["--with", dependency]
    command += [
        "yt-dlp",
        "--dump-single-json",
        "--flat-playlist",
        "--no-warnings",
    ]
    if max_items is not None and max_items > 0:
        command += ["--playlist-end", str(max_items)]
    command += [*extra_args, target]
    return command


def _tail(text: str | None) -> str:
    """进程输出摘录(尾部),保持结构化错误有界."""
    value = (text or "").strip()
    return value[-_PROCESS_TAIL_CHARS:]


def _entry(raw: dict[str, Any]) -> dict[str, Any]:
    """条目字段白名单装配:已知字段 + None 剔除(上游扁平条目字段稀疏)."""
    return {key: raw[key] for key in ENTRY_FIELDS if raw.get(key) is not None}


def run(
    target: str,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    max_items: int | None = DEFAULT_MAX_ITEMS,
    extra_args: tuple[str, ...] | list[str] = (),
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """对 ``target``(视频/频道/播放列表 URL)跑一次上游 yt-dlp 扁平快扫.

    Args:
        target: http(s) 目标 URL(由使用者指定并自负授权边界)。
        timeout: 子进程 wall-clock 预算秒数,超时抛 ``media_timeout``。
        max_items: 返回条目上限(缺省 50;经 ``--playlist-end`` 前置预算,
            ``None`` 表示不设限,慎用于大频道)。
        extra_args: 透传给上游 CLI 的附加参数(如 ``("--proxy", "…")``)。
        runner: subprocess.run 注入口(测试 mock 用)。
        clock: 单调时钟注入口(测试 mock 用)。

    Returns:
        结构化结果 dict:plugin/target/status/command/exit_code/
        duration_seconds/entry_count(截断后条数)/entry_total(上游总条数)/
        entries(白名单字段条目)/meta(单视频或频道头部信息:title/channel/
        uploader/item_count)。

    Raises:
        MediaAdapterError: 全部失败形态都是结构化错误(见模块 docstring 词表)。
    """
    do_run = runner if runner is not None else subprocess.run
    clean_target = normalize_target(target)
    if shutil.which("uv") is None:
        raise MediaAdapterError(
            "uv_missing",
            "隔离运行时不可用: PATH 上找不到 uv(https://docs.astral.sh/uv/)。"
            "适配器以 uv 临时环境运行上游 CLI,依赖不进根依赖。",
            target=clean_target,
        )
    started = clock()
    command = build_command(clean_target, max_items=max_items, extra_args=extra_args)
    try:
        completed = do_run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise MediaAdapterError(
            "media_timeout",
            f"yt-dlp 子进程超过 {timeout:g}s 预算被终止(目标 {clean_target})",
            target=clean_target,
            timeout_seconds=timeout,
            stderr_tail=_tail(exc.stderr if isinstance(exc.stderr, str) else None),
        ) from exc
    duration = round(clock() - started, 3)
    if completed.returncode != 0:
        raise MediaAdapterError(
            "media_failed",
            f"yt-dlp 子进程非零退出(code={completed.returncode};目标 {clean_target})",
            target=clean_target,
            exit_code=completed.returncode,
            stderr_tail=_tail(completed.stderr),
            stdout_tail=_tail(completed.stdout),
        )
    try:
        payload = json.loads(completed.stdout or "")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise MediaAdapterError(
            "media_output_invalid",
            f"yt-dlp 退出 0 但 stdout JSON 不可解析:{exc}",
            target=clean_target,
            stdout_tail=_tail(completed.stdout),
        ) from exc
    if not isinstance(payload, dict):
        raise MediaAdapterError(
            "media_output_invalid",
            f"yt-dlp 输出不是 JSON 对象:{type(payload).__name__}",
            target=clean_target,
        )
    raw_entries = payload.get("entries")
    if raw_entries is None:
        raw_entries = [payload]  # 单视频:对象自身即唯一条目
    if not isinstance(raw_entries, list) or not all(
        isinstance(item, dict) for item in raw_entries
    ):
        raise MediaAdapterError(
            "media_output_invalid",
            "yt-dlp 输出的 entries 不是对象数组(扁平快扫契约被上游打破)",
            target=clean_target,
        )
    entry_total = len(raw_entries)
    entries = [_entry(item) for item in raw_entries[: (max_items or entry_total)]]
    meta = {
        key: payload[key]
        for key in ("title", "channel", "uploader", "item_count", "upload_date")
        if payload.get(key) is not None
    }
    return {
        "plugin": "myssia-media",
        "target": clean_target,
        "status": "success",
        "command": command,
        "exit_code": completed.returncode,
        "duration_seconds": duration,
        "entry_count": len(entries),
        "entry_total": entry_total,
        "entries": entries,
        "meta": meta,
    }
