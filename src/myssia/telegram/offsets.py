"""Telegram serve 档的 offset 持久化(10-06-telegram-telethon B3).

getUpdates 的 ``offset`` 是全 bot 确认游标:传 ``<max_update_id>+1`` 即确认
(服务器丢弃)之前的全部更新。serve 档每轮处理后把新游标原子落盘 ——
重启从断点续拉,不重放已处理窗口(批量档无此面:窗口帽 + 锚点去重兜底)。

形态:数据根 ``telegram/offsets.json`` 单键 JSON(``{"offset": <int>}``),
临时文件 + ``os.replace`` 原子写(半写的 JSON 永远不会出现在正式路径);
读失败/缺文件 = 0(从头拉一次未确认窗口,锚点去重兜底 —— 文件损坏最坏
重放一轮,不丢消息)。**单写者前提**:offsets 属 serve 宿主私有,批量引擎
不碰(与 serve 同跑会 409 互斥,设计上就不同时存在)。
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

__all__ = ["OffsetStore"]


class OffsetStore:
    """getUpdates 确认游标的持久化(数据根 ``telegram/offsets.json``)."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> int:
        """当前游标(缺文件/损坏/形状坏 = 0 + warning;绝不抛)."""
        try:
            raw = self._path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return 0
        except OSError as exc:
            logger.warning("telegram offset 文件读取失败,按 0 续拉: %s", exc)
            return 0
        try:
            payload = json.loads(raw)
        except ValueError as exc:
            logger.warning(
                "telegram offset 文件不是有效 JSON,按 0 续拉(重放一轮,"
                "锚点去重兜底) path=%s: %s",
                self._path,
                exc,
            )
            return 0
        value = payload.get("offset") if isinstance(payload, dict) else None
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            logger.warning(
                "telegram offset 形状坏(应为非负整数),按 0 续拉: %r", payload
            )
            return 0
        return value

    def save(self, offset: int) -> None:
        """游标原子落盘(临时文件 + replace;失败 WARNING,不中断循环)."""
        if isinstance(offset, bool) or not isinstance(offset, int) or offset < 0:
            logger.warning("telegram offset 拒写非法值: %r", offset)
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".json.tmp")
        try:
            tmp.write_text(
                json.dumps({"offset": offset}), encoding="utf-8"
            )
            os.replace(tmp, self._path)
        except OSError as exc:
            logger.warning(
                "telegram offset 落盘失败(下轮从旧游标续拉,可能重放,"
                "锚点去重兜底) path=%s: %s",
                self._path,
                exc,
            )
