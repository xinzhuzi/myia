"""Telegram serve 档的事件账本(10-06-telegram-telethon B3).

设计 D1:「账本复用 executions 形态新表 telegram_events」—— cron 执行账本
(``myssia.cron.executions``)的观测纪律照搬:常驻宿主干了什么,事后要能
从库里答(不翻日志)。每条**消息级事件**一行:update_id(全 bot 单调,
天然主键)/chat_id/message_id(锚区间)/outcome(去向)/score(精筛分)/
时间戳。写失败只 WARNING,绝不带着 serve 循环走(cron ``_guarded_store_write``
同惯例)。

outcome 词表(封闭,doctor/统计消费):

- ``stored``   粗筛+精筛后普通出仓,已入库(进合并日报「Telegram 群」分区);
- ``pushed``   高价值合并单条已即时推(**轮内首个高分消息**记 pushed,
               同轮并入合并的其余消息记 stored —— 一轮一推,账本不虚增);
- ``dropped_coarse``  粗筛未命中(零痕迹跳过,只有账本知道来过);
- ``dropped_chat``    消息属于未配置的 chat(serve 只服务配置内群);
- ``dropped_textless`` 无文本无 caption(贴纸/纯图,零可筛面);
- ``dropped_other``   非消息类更新(callback_query 等);
- ``error``           处理面炸了(入库/推送失败;循环不死,下轮续)。
"""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

#: 合法 outcome 词表(封闭;写侧钳制,读侧可信)。
OUTCOMES = (
    "stored",
    "pushed",
    "dropped_coarse",
    "dropped_chat",
    "dropped_textless",
    "dropped_other",
    "error",
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS telegram_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    update_id INTEGER NOT NULL,
    chat_id TEXT,
    message_id INTEGER,
    outcome TEXT NOT NULL,
    score INTEGER,
    detail TEXT,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_telegram_events_update
    ON telegram_events (update_id);
CREATE INDEX IF NOT EXISTS idx_telegram_events_outcome
    ON telegram_events (outcome);
"""

__all__ = ["OUTCOMES", "TelegramEventLedger"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class TelegramEventLedger:
    """serve 档消息级事件账本(独立 sqlite 文件,executions 形态)."""

    def __init__(self, db_path: str | Path) -> None:
        self._path = Path(db_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        with self._conn:
            self._conn.executescript(_SCHEMA)

    # ------------------------------------------------------------------ write

    def record(
        self,
        *,
        update_id: int,
        chat_id: str | None = None,
        message_id: int | None = None,
        outcome: str,
        score: int | None = None,
        detail: str | None = None,
    ) -> bool:
        """记一行(写失败 WARNING 返 False,绝不抛;词表外 outcome 拒写)."""
        if outcome not in OUTCOMES:
            logger.warning("telegram 事件账本拒写未知 outcome: %r", outcome)
            return False
        try:
            with self._conn:
                self._conn.execute(
                    "INSERT INTO telegram_events"
                    " (update_id, chat_id, message_id, outcome, score, detail, created_at)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        int(update_id),
                        chat_id,
                        message_id,
                        outcome,
                        score,
                        detail[:500] if isinstance(detail, str) else None,
                        _now_iso(),
                    ),
                )
            return True
        except sqlite3.Error as exc:
            logger.warning("telegram 事件账本写入失败(忽略): %s", exc)
            return False

    # ------------------------------------------------------------------- read

    def tail(self, limit: int = 20) -> list[dict[str, Any]]:
        """最近事件(新 → 旧;doctor/排障消费)."""
        rows = self._conn.execute(
            "SELECT * FROM telegram_events ORDER BY id DESC LIMIT ?",
            (max(1, min(int(limit), 500)),),
        ).fetchall()
        return [dict(row) for row in rows]

    def counts(self) -> dict[str, int]:
        """各 outcome 累计(状态面板/健康检查消费)."""
        rows = self._conn.execute(
            "SELECT outcome, COUNT(*) AS n FROM telegram_events GROUP BY outcome"
        ).fetchall()
        return {row["outcome"]: row["n"] for row in rows}

    def close(self) -> None:
        self._conn.close()
