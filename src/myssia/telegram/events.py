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
- ``no_channel``      品类未配 push 通道:高价值合并条目已入库、未推
               (深审 F14 虚账修正 —— 未配通道不再记 pushed,counts/stats
               不虚增;条目在库,日报兜底可见);
- ``dropped_coarse``  粗筛未命中(零痕迹跳过,只有账本知道来过);
- ``dropped_chat``    消息属于未配置的 chat(serve 只服务配置内群);
- ``dropped_textless`` 无文本无 caption(贴纸/纯图,零可筛面);
- ``dropped_other``   非消息类更新(callback_query 等);
- ``error``           处理面炸了(入库/推送失败;循环不死,下轮续)。

**按 bot 指纹分库**(深审 F8,offsets 同判例):多 bot 双宿主共享数据根
时各 bot 各账本文件(``events-<sha8(token)>.db``),counts 不再跨 bot 混
计;``bot_token`` 缺省 = 传入路径原样(旧形态,兼容既有调用方)。

**保留策略**(深审 F11):每写一行后按 id 新→旧裁到
:data:`MAX_EVENTS`(1000 行帽,cron executions 终态裁剪同判例 —— 排序面
被帽钉死,每写一裁亚毫秒,不引入「帽短暂超限」节流不变量)。观测面
(doctor/counts)只需要近期尾部,全量历史不属本账本职责。
"""

from __future__ import annotations

import logging
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from myssia.telegram.offsets import bot_fingerprint

logger = logging.getLogger(__name__)

#: 合法 outcome 词表(封闭;写侧钳制,读侧可信)。
OUTCOMES = (
    "stored",
    "pushed",
    "no_channel",
    "dropped_coarse",
    "dropped_chat",
    "dropped_textless",
    "dropped_other",
    "error",
)

#: 保留帽(行数;executions 终态 1000 行帽判例,深审 F11)。
MAX_EVENTS = 1000

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

__all__ = ["MAX_EVENTS", "OUTCOMES", "TelegramEventLedger"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _prune_events(conn: sqlite3.Connection) -> sqlite3.Cursor | None:
    """最新 :data:`MAX_EVENTS` 行外裁掉(id 自增即新→旧序;深审 F11).

    executions 终态裁剪(``_prune_unlocked``)同判例:每写一裁全表删旧,
    排序面被 1000 行帽钉死亚毫秒;不引入「帽短暂超限」节流不变量。
    """
    try:
        return conn.execute(
            "DELETE FROM telegram_events WHERE id IN ("
            " SELECT id FROM telegram_events ORDER BY id DESC LIMIT -1 OFFSET ?"
            ")",
            (max(0, int(MAX_EVENTS)),),
        )
    except sqlite3.Error as exc:  # pragma: no cover - 裁剪是卫生动作,失败不带走写
        logger.warning("telegram 事件账本裁剪失败(忽略): %s", exc)
        return None


class TelegramEventLedger:
    """serve 档消息级事件账本(独立 sqlite 文件,executions 形态).

    Args:
        db_path: 账本文件路径。``bot_token`` 缺省 = 该路径原样(旧形态);
            传 ``bot_token`` = 落盘 ``<stem>-<sha8(token)><suffix>`` 兄弟文件
            (深审 F8:多 bot 双宿主各账本,counts 不跨 bot 混计;观测账本
            无迁移面 —— 新文件从零累计,旧文件留盘不读)。
    """

    def __init__(self, db_path: str | Path, *, bot_token: str | None = None) -> None:
        path = Path(db_path)
        if bot_token is not None:
            path = path.parent / (
                f"{path.stem}-{bot_fingerprint(bot_token)}{path.suffix}"
            )
        self._path = path
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # check_same_thread=False(store/sqlite.py 同款):桌面 sidecar 在装配
        # 线建账本、serve 线写行(2026-10-08 装机实跑暴露);CLI serve 单线
        # 程不受影响。写面单一(serve 事件循环),无并发写者。
        self._conn = sqlite3.connect(self._path, check_same_thread=False)
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
        """记一行(写失败 WARNING 返 False,绝不抛;词表外 outcome 拒写).

        每写一行即裁剪到 :data:`MAX_EVENTS` 帽(深审 F11;同事务).
        """
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
                _prune_events(self._conn)
            return True
        except sqlite3.Error as exc:
            logger.warning("telegram 事件账本写入失败(忽略): %s", exc)
            return False

    def prune(self) -> int:
        """显式裁剪到 :data:`MAX_EVENTS` 帽;返回删掉的行数(0 = 已在帽内)."""
        try:
            with self._conn:
                cursor = _prune_events(self._conn)
            return max(0, cursor.rowcount) if cursor is not None else 0
        except sqlite3.Error as exc:
            logger.warning("telegram 事件账本裁剪失败(忽略): %s", exc)
            return 0

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
