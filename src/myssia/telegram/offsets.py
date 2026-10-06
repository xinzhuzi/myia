"""Telegram serve 档的 offset 持久化(10-06-telegram-telethon B3).

getUpdates 的 ``offset`` 是全 bot 确认游标:传 ``<max_update_id>+1`` 即确认
(服务器丢弃)之前的全部更新。serve 档每轮处理后把新游标原子落盘 ——
重启从断点续拉,不重放已处理窗口(批量档无此面:窗口帽 + 锚点去重兜底)。

形态:``{"offset": <int>}`` 单键 JSON,临时文件 + ``os.replace`` 原子写
(半写的 JSON 永远不会出现在正式路径);读失败/缺文件 = 0(从头拉一次
未确认窗口,锚点去重兜底 —— 文件损坏最坏重放一轮,不丢消息)。
**单写者前提**:offsets 属 serve 宿主私有,批量引擎不碰(与 serve 同跑会
409 互斥,设计上就不同时存在)。

**按 bot 指纹分键**(深审 F8):update_id 是 per-bot 独立序列 —— 多 bot
双宿主(桌面 + CLI / 两品类各一宿主)共享同一数据根时,共享单键
``offsets.json`` 会交叉污染:A bot 写下的游标对 B bot 是**越前游标**
(跳过 B 未处理更新 = 静默丢单),且无任何报错面。构造时传
``bot_token`` 即按指纹分文件:``offsets-<sha8(token)>.json`` 兄弟文件,
各 bot 各游标互不可见。旧单键文件迁移:指纹文件缺席而旧文件在场 →
采纳其值一次(单 bot 升级不断点),写成功后**删除旧文件** —— 双宿主下
第二个 bot 不会再误采他人游标,从 0 续拉由锚点去重兜底(**重放安全,
越前不安全**,方向钉死)。token 只进 sha256 指纹不落盘不落日志。
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

__all__ = ["OffsetStore", "bot_fingerprint"]


def bot_fingerprint(bot_token: str) -> str:
    """bot token 指纹(sha256 前 8 hex;文件名维度用,非凭据可反推面)."""
    return hashlib.sha256(bot_token.encode("utf-8")).hexdigest()[:8]


class OffsetStore:
    """getUpdates 确认游标的持久化(可选按 bot 指纹分键;深审 F8).

    Args:
        path: 游标文件路径。``bot_token`` 缺省 = 该路径原样读写(单键旧形态,
            既有调用方零感知);传 ``bot_token`` = 实际落盘
            ``<stem>-<sha8(token)><suffix>`` 兄弟文件,并把旧单键文件按
            「采纳一次即删」迁移(见模块文档)。
    """

    def __init__(self, path: str | Path, *, bot_token: str | None = None) -> None:
        self._legacy_path = Path(path)
        if bot_token is None:
            self._path = self._legacy_path
        else:
            self._path = self._legacy_path.parent / (
                f"{self._legacy_path.stem}-{bot_fingerprint(bot_token)}"
                f"{self._legacy_path.suffix}"
            )

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> int:
        """当前游标(缺文件/损坏/形状坏 = 0 + warning;绝不抛).

        指纹分键形态下指纹文件缺席 → 先试旧单键迁移(采纳一次即删).
        """
        try:
            raw = self._path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return self._migrate_from_legacy()
        except OSError as exc:
            logger.warning("telegram offset 文件读取失败,按 0 续拉: %s", exc)
            return 0
        return self._parse_offset(raw)

    def _migrate_from_legacy(self) -> int:
        """旧单键文件 → 指纹文件的一次性迁移(仅指纹分键形态才走)."""
        if self._path == self._legacy_path:
            return 0
        try:
            raw = self._legacy_path.read_text(encoding="utf-8")
        except OSError:
            return 0  # 旧文件不在:新 bot 从 0 续拉(重放安全)
        value = self._parse_offset(raw)
        logger.info(
            "telegram offset 旧单键文件迁移(采纳一次即删,此后各 bot 各键)"
            " legacy=%s → %s offset=%s",
            self._legacy_path,
            self._path,
            value,
        )
        self.save(value)
        try:
            self._legacy_path.unlink()
        except OSError as exc:
            logger.warning(
                "telegram offset 旧单键文件删除失败(留盘无害,不再读它): %s", exc
            )
        return value

    def _parse_offset(self, raw: str) -> int:
        """单键 JSON 文本 → 游标值(坏形态 = 0 + warning)."""
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
