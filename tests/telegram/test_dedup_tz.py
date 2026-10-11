"""DedupRegistry 时区收编回归(2026-10-11 web 线首条真消息踩响).

背景:telegram serve 两装配面(CLI ``_cmd_telegram_serve`` 与桌面
``_assemble_telegram_host``)都把品类 YAML 的 ``timezone`` **字符串**
直传 ``DedupRegistry(store, tz=...)`` —— 构造不炸,``is_seen`` 首次
取 now(tz=串) 才炸(``tzinfo argument must be … not type 'str'``),
web 线消息入库全灭。本件钉死:str 串收编 ZoneInfo、坏串回落本地、
tzinfo 对象原样透传三面。
"""

from __future__ import annotations

from datetime import timezone as dt_timezone
from zoneinfo import ZoneInfo

from myssia.dedup import DedupRegistry
from myssia.store import SQLiteStore


def _registry(tz: object) -> tuple[DedupRegistry, SQLiteStore]:
    import tempfile
    from pathlib import Path

    store = SQLiteStore(
        Path(tempfile.mkdtemp(prefix="myssia-dedup-tz-")) / "items.db"
    )
    return DedupRegistry(store, tz=tz), store  # type: ignore[arg-type]


def test_str_timezone_coerced_to_zoneinfo() -> None:
    """品类 YAML 的 str 时区(serve 两装配面的实传形态)收编后 is_seen 可用。"""
    registry, store = _registry("Asia/Shanghai")
    assert registry._tz == ZoneInfo("Asia/Shanghai")
    assert registry.is_seen("https://web.telegram.org#tg--1-1") is False
    registry.mark_seen("https://web.telegram.org#tg--1-1")
    assert registry.is_seen("https://web.telegram.org#tg--1-1") is True
    store.close()


def test_bad_timezone_string_falls_back_to_local() -> None:
    """坏串防御回落本地时区(不炸不吞消息)。"""
    registry, store = _registry("Not/AZone")
    assert registry._tz is not None  # 本地时区兜底
    assert registry.is_seen("k") is False
    store.close()


def test_tzinfo_object_passthrough() -> None:
    """既有 tzinfo 调用面(管线 ``_category_tz``)零行为差。"""
    registry, store = _registry(dt_timezone.utc)
    assert registry._tz is dt_timezone.utc
    store.close()
