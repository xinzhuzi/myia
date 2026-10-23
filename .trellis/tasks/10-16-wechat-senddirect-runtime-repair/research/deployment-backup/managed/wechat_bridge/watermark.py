"""SSE 水位扫描与事件数据面(task 10-14-wechat-http-api R6/R8)。

**这是 ``localdb serve`` 常驻进程内的独立模块**(PRD R6「serve 进程内,
独立模块」),三块职责:

- **水位持久化**:<数据根>/wechat-localdb/http-watermark.json(600,目录
  700),内容仅 ``{"watermark": <epoch 秒>, "updated_at": …}``——零聊天
  内容、零密钥材料(红线 6)。冷启动(无文件/坏文件)→ watermark=now
  **不倒灌历史**(历史走 Pull 端点);有文件 → 断档间隙首轮扫描如实补发。
- **单轮扫描**:session 表前 50 会话(库内自然序,复用
  :func:`wechat_bridge.localdb_query.list_sessions`)逐会话 since 水位增量
  查询。**免全库扫机制(design 裁决落此)**:会话表按 rowid **尾部窗口**
  定点读(``ORDER BY rowid DESC LIMIT K``——走 rowid B 树逆序,取满即停,
  零排序零全表扫;消息行按到达序追加,rowid≈时间序),窗口整段落在增量内
  才按级数扩窗(×4,封顶 :data:`TAIL_WINDOW_MAX_ROWS`);超顶=如实截断,
  消费端经 Pull 端点补齐。**不另建索引/台账**(约束:PRD Notes「别在
  design 期再发明第三套索引方案」;若 C1 R1 副本索引自举落地,本机制
  可平移到索引前缀查询,接口不变)。索引/台账只落解密副本或数据根私有
  区的红线在本模块同样成立——本机制干脆不落任何新件。
- **事件枢纽(EventHub)+ SSE 帧生成**:重放环形缓冲 ≤1000 事件 / TTL
  10min / Last-Event-ID 续传;25s 心跳注释帧 ``: ping``(常量注入点,单测
  不真等)。事件延迟=扫描间隔量级(**分钟级**,60s 一轮;文案禁「实时」
  ——WeFlow 靠 FFI 表变更通知做到秒级,MYIA 只读链无此件,不虚标)。

R8 撤回解析件(:func:`parse_revoke_events`)在本模块(PRD R8 归属:C6
先落则归 C6;若集成员钉 C5 notify_query 产权,平移该函数并让本模块消费,
**两头不得各写一份**)。识别 ``local_type=10002`` revoke 记录:优先
``<newmsgid>`` 与增量行 ``server_id`` 精确配对残留原消息(不臆造);配
不上回落 ``<replacemsg>`` 文案;原消息缺失=仅撤回事实。``orig_preview``
≤30 字(PRD R6)。

消费端契约(PRD R6 原文):按 ``(chat_id, ts, sender, sha1(text)[:16])``
内容锚去重——扫描边界秒(ts==watermark)的行会每轮重发(同秒迟到行不
丢的代价),at-least-once 交付 + 消费端去重是既定契约;重连过晚(重放
缓冲已淘汰)= 从头经 Pull 端点补。
"""

from __future__ import annotations

import hashlib
import json
import os
import queue
import re
import sqlite3
import sys
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterator

from . import localdb
from .codes import DECRYPT_FAILED, BridgeError
from .config import myssia_home
from .localdb import LOCALDB_PRIVATE_DIR
from .localdb_query import (
    MSG_TYPE_NAMES,
    _decode_text_content,
    _normalize_ts,
    _pick,
    _columns,
    _sender_name,
    find_message_tables,
    list_sessions,
    name2id_maps,
)

__all__ = [
    "HEARTBEAT_SECONDS",
    "ORIG_PREVIEW_MAX_CHARS",
    "REPLAY_MAX_EVENTS",
    "REPLAY_TTL_SECONDS",
    "REVOKE_LOCAL_TYPE",
    "SCAN_INTERVAL_SECONDS",
    "SCAN_SESSIONS_LIMIT",
    "TAIL_WINDOW_ESCALATION",
    "TAIL_WINDOW_MAX_ROWS",
    "TAIL_WINDOW_ROWS",
    "WATERMARK_REL_PATH",
    "EventHub",
    "WatermarkScanner",
    "parse_revoke_events",
    "read_watermark",
    "scan_round",
    "sse_stream",
    "watermark_path",
    "write_watermark",
]

# —— 模块常量(单测注入点;PRD R6 钉死的工程参数,WeFlow 语义自写实现)——
#: 扫描间隔(秒;事件延迟=本量级=分钟级,文案禁「实时」)。
SCAN_INTERVAL_SECONDS = 60
#: SSE 心跳间隔(秒;注释帧 ``: ping``)。
HEARTBEAT_SECONDS = 25
#: 重放环形缓冲上限(事件数)。
REPLAY_MAX_EVENTS = 1000
#: 重放缓冲 TTL(秒)。
REPLAY_TTL_SECONDS = 600
#: 单轮扫描会话上限(session 表前 N,库内自然序;PRD R6)。
SCAN_SESSIONS_LIMIT = 50
#: 尾部窗口基数(行;rowid 逆序定点读)。
TAIL_WINDOW_ROWS = 200
#: 窗口扩级(窗口整段落在增量内才扩;×4)。
TAIL_WINDOW_ESCALATION = 4
#: 窗口封顶(行;超顶=如实截断,消费端经 Pull 端点补)。
TAIL_WINDOW_MAX_ROWS = 51200
#: 撤回系统消息 local_type(公开常量表;localdb_query.MSG_TYPE_NAMES 同源)。
REVOKE_LOCAL_TYPE = 10002
#: revoke 事件原文预览上限(字;PRD R6)。
ORIG_PREVIEW_MAX_CHARS = 30
#: 水位文件相对数据根路径(PRD R6:<数据根>/wechat-localdb/http-watermark.json)。
WATERMARK_REL_PATH = f"{LOCALDB_PRIVATE_DIR}/http-watermark.json"

_SERVER_ID_COLS = ("server_id", "serverId", "server_id_", "ServerId")

# revoke 系统消息 content 形状(4.x 实测族;解析不干净=仅撤回事实,不臆造)
_REVOKE_NEWMSGID_RE = re.compile(r"<newmsgid>\s*(\d+)\s*</newmsgid>")
_REVOKE_REPLACEMSG_RE = re.compile(
    r"<replacemsg>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</replacemsg>", re.S
)
_REVOKE_QUOTED_NAME_RE = re.compile(r'["“「]([^"”」]{1,40}?)["”」]')


# =====================================================================
# 水位持久化(数据根私有区 600;零内容零密钥)
# =====================================================================


def watermark_path(data_root: Path | None = None) -> Path:
    """水位文件路径(数据根私有区 wechat-localdb/http-watermark.json)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / Path(WATERMARK_REL_PATH)


def read_watermark(data_root: Path | None = None) -> float | None:
    """读水位(epoch 秒);缺文件/坏 JSON/形状漂移 → None(=冷启动,不倒灌)。"""
    path = watermark_path(data_root)
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        value = raw.get("watermark") if isinstance(raw, dict) else None
        ts = float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None
    except (OSError, ValueError):
        return None
    return ts if ts is not None and ts > 0 else None


def write_watermark(
    data_root: Path | None, watermark: float, *, now: float | None = None
) -> Path:
    """写水位(600,原子落盘 tmp+rename;内容仅 watermark/updated_at 两键)。"""
    path = watermark_path(data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    stamp = time.time() if now is None else now
    body = {
        "watermark": int(watermark),
        "updated_at": datetime.fromtimestamp(stamp).isoformat(timespec="seconds"),
    }
    tmp = path.with_name(f"{path.name}.tmp-{os.getpid()}")
    try:
        tmp.write_text(json.dumps(body, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()
    return path


# =====================================================================
# R8 撤回事件解析件(C6 落地版;C5 消费同一函数,不得另写一份)
# =====================================================================


def parse_revoke_events(
    rows: list[dict[str, Any]], chat_id: str
) -> list[dict[str, Any]]:
    """从会话增量行识别撤回事件(``local_type=10002``;R8)。

    输入行形状(:func:`scan_round` 产出):``{"rowid","ts","sender",
    "local_type","text"(解码后正文/None),"server_id"(int|None)}``。
    配对策略(宁缺毋假,不臆造内容):

    ① revoke 行 content 含 ``<newmsgid>`` → 在**同批增量行**内找
       ``server_id == newmsgid`` 的残留原消息,其 text/占位截 30 字为
       ``orig_preview``;② 配不上 → 试 ``<replacemsg>`` 文案里被引号
       括起的撤回原文(部分撤回形态把预览嵌在文案里);③ 都没有 →
       仅撤回事实(不携 ``orig_preview`` 键)。操作人 = replacemsg 引号名
       (常见形态 ``"名字" 撤回了一条消息``),缺回落行 sender。

    Returns:
        事件载荷列表(键序稳定):``{"type":"message.revoke","chat_id",
        "ts","sender","orig_preview"?}``。
    """
    by_server_id = {
        int(row["server_id"]): row
        for row in rows
        if row.get("server_id") is not None
    }
    events: list[dict[str, Any]] = []
    for row in rows:
        if row.get("local_type") != REVOKE_LOCAL_TYPE:
            continue
        content = row.get("text")
        if not isinstance(content, str) or not content.strip():
            continue  # 形状异常:仅按类型不可信,弃(宁缺毋假)
        newmsgid_match = _REVOKE_NEWMSGID_RE.search(content)
        replace_match = _REVOKE_REPLACEMSG_RE.search(content)
        replacemsg = (replace_match.group(1).strip() if replace_match else "") or ""
        # 操作人:replacemsg 引号名 → 行 sender 兜底(无从归因即不编造)。
        operator = row.get("sender")
        if replacemsg:
            quoted = _REVOKE_QUOTED_NAME_RE.search(replacemsg)
            if quoted:
                operator = quoted.group(1) or operator
        event: dict[str, Any] = {
            "type": "message.revoke",
            "chat_id": chat_id,
            "ts": row.get("ts") or 0,
            "sender": operator,
        }
        # ① newmsgid ↔ server_id 精确配对残留原消息。
        orig_preview: str | None = None
        if newmsgid_match:
            original = by_server_id.get(int(newmsgid_match.group(1)))
            if original is not None:
                source_text = original.get("text") or original.get(
                    "media_placeholder"
                )
                if isinstance(source_text, str) and source_text:
                    orig_preview = source_text[:ORIG_PREVIEW_MAX_CHARS]
        # ② replacemsg 嵌入的撤回原文(第二段被引号括起且非「撤回了一条消息」操作人段)。
        if orig_preview is None and replacemsg:
            quoted_all = _REVOKE_QUOTED_NAME_RE.findall(replacemsg)
            for candidate in quoted_all[1:]:
                if "撤回" not in candidate:
                    orig_preview = candidate[:ORIG_PREVIEW_MAX_CHARS]
                    break
        if orig_preview is not None:
            event["orig_preview"] = orig_preview
        events.append(event)
    return events


# =====================================================================
# 单轮扫描(session 前 50 会话 × 尾部窗口增量;零全库扫)
# =====================================================================


def _server_id_column(con: sqlite3.Connection, table: str) -> str | None:
    """会话表的 server id 列(revoke newmsgid 配对用;列漂移 = None 如实)。"""
    return _pick(_columns(con, table), _SERVER_ID_COLS)


def scan_session_increment(
    con: sqlite3.Connection,
    table: str,
    colmap: dict[str, str | None],
    chat_id: str,
    since_ts: int,
    *,
    id_to_name: dict[int, str] | None = None,
    stats: dict[str, Any] | None = None,
    tail_rows: int = TAIL_WINDOW_ROWS,
    tail_max: int = TAIL_WINDOW_MAX_ROWS,
    tail_step: int = TAIL_WINDOW_ESCALATION,
) -> tuple[list[dict[str, Any]], int]:
    """单会话尾部窗口增量扫描 → ``(事件载荷列表, 本会话 max(create_time))``。

    查询形状:``SELECT … FROM <表> [WHERE talker=?] ORDER BY rowid DESC
    LIMIT <窗口>``——rowid B 树逆序定点读,取满即停(免全库扫机制,见
    模块 docstring);窗口整段落在增量内(取满且最旧行 ts 仍 ≥ since)才
    扩窗 ×4,封顶 ``tail_max``。行过滤在 Python 层:``ts >= since``(**含
    等号**——同秒迟到行不丢;边界秒重发由消费端内容锚去重消化,契约见
    模块 docstring)。产出消息行/撤回行混排事件(ts 升序)。
    """
    names = id_to_name or {}
    cols: list[str] = []  # 列序 = 行元组 idx
    idx: dict[str, int] = {}
    wanted = [
        ("time", colmap.get("time")),
        ("type", colmap.get("type")),
        ("content", colmap.get("content")),
        ("sender", colmap.get("sender")),
        ("sender_id", colmap.get("sender_id")),
        ("ct_content", colmap.get("ct_content")),
        ("server_id", _server_id_column(con, table)),
    ]
    for key, col in wanted:
        if col:
            idx[key] = len(cols)
            cols.append(col)
    quoted = ", ".join(chr(34) + c + chr(34) for c in cols)
    rowid_term = "rowid"
    talker = colmap.get("talker")
    where = f'WHERE "{talker}" = ?' if talker else ""

    window = max(1, int(tail_rows))
    fetched: list[tuple] = []
    while True:
        sql = (
            f'SELECT {quoted}, {rowid_term} FROM "{table}" {where} '
            f"ORDER BY {rowid_term} DESC LIMIT ?"
        )
        params: tuple[Any, ...] = (chat_id, window) if talker else (window,)
        try:
            rows_desc = con.execute(sql, params).fetchall()
        except sqlite3.Error:
            return [], since_ts  # 单表漂移不拖垮整轮(红线 7:如实降级)
        fetched = list(reversed(rows_desc))  # rowid 升序(≈时间序)
        window_full = len(fetched) == window
        oldest_ts = min(
            (_normalize_ts(row[idx["time"]]) for row in fetched), default=since_ts
        )
        if window_full and oldest_ts >= since_ts and window < tail_max:
            window = min(window * max(2, tail_step), tail_max)
            if stats is not None:
                stats["tail_escalations"] = int(stats.get("tail_escalations", 0)) + 1
            continue
        break
    if window_full and oldest_ts >= since_ts and window >= tail_max and stats is not None:
        stats["tail_capped"] = int(stats.get("tail_capped", 0)) + 1

    events: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []
    chat_max = since_ts
    for row in fetched:
        ts = _normalize_ts(row[idx["time"]])
        chat_max = max(chat_max, ts)
        if ts < since_ts:
            continue
        content = row[idx["content"]] if "content" in idx else None
        msg_type = 1
        if "type" in idx:
            try:
                msg_type = int(row[idx["type"]] or 0)
            except (TypeError, ValueError):
                msg_type = 0
        if "sender" in idx:  # 旧形态 isSender
            sender = "me" if row[idx["sender"]] == 1 else chat_id
        elif "sender_id" in idx:
            sender = _sender_name(row[idx["sender_id"]], names, chat_id)
        else:
            sender = chat_id
        text, placeholder = _decode_text_content(
            content, row[idx["ct_content"]] if "ct_content" in idx else None, None
        )
        raw_rows.append(
            {
                "rowid": row[-1],
                "ts": ts,
                "sender": sender,
                "local_type": msg_type,
                "text": text,
                "media_placeholder": placeholder,
                "server_id": (
                    int(row[idx["server_id"]]) if "server_id" in idx else None
                ),
            }
        )
    # 撤回行 → 独立 message.revoke 事件(R8 解析件);其余行 → message.new。
    events.extend(parse_revoke_events(raw_rows, chat_id))
    for row in raw_rows:
        if row["local_type"] == REVOKE_LOCAL_TYPE:
            continue
        event: dict[str, Any] = {
            "type": "message.new",
            "chat_id": chat_id,
            "ts": row["ts"],
            "sender": row["sender"],
            "msg_type": MSG_TYPE_NAMES.get(
                row["local_type"], f"type_{row['local_type']}"
            ),
        }
        if row["local_type"] == 1 and row["text"] is not None:
            event["text"] = row["text"]
        else:
            event["media_placeholder"] = (
                row["media_placeholder"] or "非文本消息,内容未导出(占位)"
            )
        events.append(event)
    events.sort(key=lambda item: (int(item["ts"]), str(item.get("chat_id", ""))))
    return events, chat_max


def scan_round(
    session_con: sqlite3.Connection,
    message_con: sqlite3.Connection,
    since_ts: int,
    *,
    session_limit: int = SCAN_SESSIONS_LIMIT,
    stats: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], int]:
    """一轮扫描:session 表前 ``session_limit`` 会话逐会话增量(R6)。

    会话清单复用 :func:`list_sessions`(库内自然序);每会话表按
    :func:`find_message_tables` 同一自适应机制定位(分表经 Name2Id md5
    反解;宽表按 talker 过滤)。覆盖面如实:近活跃会话(前 50),全量
    历史=Pull 端点(PRD R6 原文)。返回 ``(事件列表(ts 升序),
    新水位=max(各会话 max(create_time)))``。
    """
    sessions = list_sessions(session_con, session_limit)
    chat_ids = [
        item["id"] for item in sessions if isinstance(item.get("id"), str) and item["id"]
    ]
    tables = find_message_tables(message_con)
    id_to_name: dict[int, str] = {}
    if any(colmap.get("sender_id") for _table, colmap in tables):
        id_to_name = name2id_maps(message_con)[0]
    wide_tables = [(t, cm) for t, cm in tables if cm.get("talker")]
    split_map = {
        cm["chat"]: (t, cm) for t, cm in tables if not cm.get("talker") and cm.get("chat")
    }
    events: list[dict[str, Any]] = []
    new_watermark = since_ts
    for chat_id in chat_ids:
        located = split_map.get(chat_id) or (wide_tables[0] if wide_tables else None)
        if located is None:
            if stats is not None:
                stats["sessions_without_table"] = int(
                    stats.get("sessions_without_table", 0)
                ) + 1
            continue  # 会话无对应消息表(如 biz 会话):如实跳过
        table, colmap = located
        chat_events, chat_max = scan_session_increment(
            message_con,
            table,
            colmap,
            chat_id,
            since_ts,
            id_to_name=id_to_name,
            stats=stats,
        )
        events.extend(chat_events)
        new_watermark = max(new_watermark, chat_max)
        if stats is not None:
            stats["sessions_scanned"] = int(stats.get("sessions_scanned", 0)) + 1
    events.sort(key=lambda item: (int(item["ts"]), str(item.get("chat_id", ""))))
    return events, new_watermark


# =====================================================================
# 事件枢纽(重放环形缓冲 + 订阅风扇)
# =====================================================================


class EventHub:
    """SSE 事件枢纽:单调 id、环形重放缓冲(≤max_events / TTL)、订阅队列。

    - :meth:`publish`:分配单调递增整数 id(SSE ``id:`` 帧),入缓冲并按
      TTL/容量淘汰(超量/超期如实淘汰——重连过晚的消费端经 Pull 端点补,
      PRD R6),向全部订阅队列非阻塞投递(队列满=该订阅者掉队,丢弃不阻塞
      发布方;掉队者靠 Last-Event-ID 重连或 Pull 补)。
    - :meth:`events_after`:重放 ``id > last_id`` 且仍在缓冲内的事件(已被
      淘汰的 id 不复活,如实缺席)。
    """

    def __init__(
        self,
        *,
        max_events: int = REPLAY_MAX_EVENTS,
        ttl_seconds: int = REPLAY_TTL_SECONDS,
        now_fn: Callable[[], float] = time.time,
        queue_max: int = REPLAY_MAX_EVENTS,
    ) -> None:
        self._events: deque[tuple[int, float, dict[str, Any]]] = deque()
        self._next_id = 0
        self._lock = threading.Lock()
        self._subscribers: set[queue.Queue] = set()
        self.max_events = max_events
        self.ttl_seconds = ttl_seconds
        self.now_fn = now_fn
        self.queue_max = queue_max

    def _prune_locked(self, now: float) -> None:
        """容量/TTL 双淘汰(调用方持锁;超量/超期如实淘汰,不复活)。"""
        while len(self._events) > self.max_events:
            self._events.popleft()
        cutoff = now - self.ttl_seconds
        while self._events and self._events[0][1] < cutoff:
            self._events.popleft()

    def publish(self, payload: dict[str, Any]) -> int:
        """发布单事件 → 事件 id(单调递增,进程内从 1 起)。"""
        with self._lock:
            self._next_id += 1
            event_id = self._next_id
            now = self.now_fn()
            self._events.append((event_id, now, dict(payload)))
            self._prune_locked(now)
            subscribers = list(self._subscribers)
        for subscriber in subscribers:
            try:
                subscriber.put_nowait((event_id, payload))
            except queue.Full:  # 掉队订阅者:丢弃,不阻塞发布方
                continue
        return event_id

    def publish_all(self, payloads: list[dict[str, Any]]) -> int:
        """按序发布一批事件 → 末事件 id(空批 = 当前末 id,无事件时 0)。"""
        last = 0
        for payload in payloads:
            last = self.publish(payload)
        return last

    def events_after(self, last_id: int) -> list[tuple[int, dict[str, Any]]]:
        """重放缓冲内 ``id > last_id`` 的事件(升序;(id, payload) 二元组)。

        读取时按 TTL 再淘汰一轮(长时间无发布时超期事件同样过期,不赖账)。
        """
        with self._lock:
            self._prune_locked(self.now_fn())
            return [
                (event_id, dict(payload))
                for event_id, _ts, payload in self._events
                if event_id > last_id
            ]

    def subscribe(self) -> queue.Queue:
        """订阅后续事件(与 :meth:`events_after` 配合:先订阅后重放,
        重叠 id 由消费方跳过——见 :func:`sse_stream`)。"""
        subscriber: queue.Queue = queue.Queue(maxsize=self.queue_max)
        with self._lock:
            self._subscribers.add(subscriber)
        return subscriber

    def unsubscribe(self, subscriber: queue.Queue) -> None:
        with self._lock:
            self._subscribers.discard(subscriber)

    def latest_id(self) -> int:
        with self._lock:
            return self._next_id


# =====================================================================
# SSE 帧生成(transport 无关;socket 泵在 httpapi 适配层)
# =====================================================================


def _sse_frame(event_id: int, payload: dict[str, Any]) -> str:
    data = json.dumps(payload, ensure_ascii=False)
    return f"id: {event_id}\nevent: message\ndata: {data}\n\n"


def sse_stream(
    hub: EventHub,
    last_event_id: int | None = None,
    *,
    heartbeat_seconds: float = HEARTBEAT_SECONDS,
    poll_timeout: float | None = None,
    stop_event: threading.Event | None = None,
    max_frames: int | None = None,
) -> Iterator[str]:
    """SSE 帧生成器:先重放(Last-Event-ID 之后仍在缓冲内者),再活流+心跳。

    帧形态:事件帧 ``id: N\\nevent: message\\ndata: {json}\\n\\n``;心跳注释帧
    ``: ping\\n\\n``(每 ``heartbeat_seconds`` 无事件时一发;常量注入点,
    单测以 ``poll_timeout``/``max_frames`` 免真等)。订阅与重放之间无缺环:
    先订阅后重放,队列里与重放重叠的 id 被跳过(> last 已发 id)。
    """
    subscriber = hub.subscribe()
    last = int(last_event_id) if last_event_id is not None else 0
    frames_left = max_frames
    timeout = heartbeat_seconds if poll_timeout is None else poll_timeout
    try:
        for event_id, payload in hub.events_after(last):
            yield _sse_frame(event_id, payload)
            last = event_id
            if frames_left is not None:
                frames_left -= 1
                if frames_left <= 0:
                    return
        while stop_event is None or not stop_event.is_set():
            try:
                event_id, payload = subscriber.get(timeout=max(timeout, 0.01))
            except queue.Empty:
                yield ": ping\n\n"
                if frames_left is not None:
                    frames_left -= 1
                    if frames_left <= 0:
                        return
                continue
            if event_id <= last:
                continue  # 重放重叠帧:跳过(不丢不重)
            yield _sse_frame(event_id, payload)
            last = event_id
            if frames_left is not None:
                frames_left -= 1
                if frames_left <= 0:
                    return
    finally:
        hub.unsubscribe(subscriber)


# =====================================================================
# 扫描线程(serve 进程内;定位/取钥/副本链全复用桥既有编排)
# =====================================================================


class WatermarkScanner:
    """60s 一轮的水位扫描线程(R6;常驻服务进程内,daemon)。

    每轮:读水位(缺=now 冷启动不倒灌)→ :func:`localdb.locate_db_storage`
    → :func:`localdb.resolve_keys` → :func:`localdb.ensure_decrypted_copies`
    (域固定 ``["session","message"]``;「源新即重建」让新消息在分钟级
    扫描间隔内可见)→ :func:`scan_round` → 事件入 :class:`EventHub` →
    推进并落盘水位。**密钥/库不可得(BridgeError)不推进水位**(下轮
    成功时断档间隙如实补发),stderr 只记形状。``locate``/``resolve``/
    ``ensure`` 均可注入(单测免真链)。
    """

    def __init__(
        self,
        *,
        hub: EventHub,
        config: Any = None,
        data_root: Path | None = None,
        files_root: Path | None = None,
        interval_seconds: float = SCAN_INTERVAL_SECONDS,
        now_fn: Callable[[], float] = time.time,
        locate: Callable[[], Path] | None = None,
        resolve: Callable[[Path], dict[str, str]] | None = None,
        ensure: Callable[[Path, dict[str, str]], dict[str, Any]] | None = None,
        session_limit: int = SCAN_SESSIONS_LIMIT,
    ) -> None:
        self.hub = hub
        self.config = config
        self.data_root = data_root
        self.files_root = files_root
        self.interval_seconds = interval_seconds
        self.now_fn = now_fn
        self.session_limit = session_limit
        self._locate = locate or self._default_locate
        self._resolve = resolve or self._default_resolve
        self._ensure = ensure or self._default_ensure
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.last_stats: dict[str, Any] | None = None
        self.last_watermark: float | None = None

    # —— 缺省链(与 localdb 命令族同一编排;测试注入替换)——
    def _default_locate(self) -> Path:
        return localdb.locate_db_storage(files_root=self.files_root)

    def _default_resolve(self, storage: Path) -> dict[str, str]:
        return localdb.resolve_keys(storage, config=self.config, data_root=self.data_root)

    def _default_ensure(self, storage: Path, keys: dict[str, str]) -> dict[str, Any]:
        from . import memsearch

        def _ensure(keys_mapping: dict[str, str]) -> dict[str, Any]:
            assert self.config is not None
            return localdb.ensure_decrypted_copies(
                storage,
                keys_mapping,
                domains=["session", "message"],
                ttl_hours=self.config.copy_ttl_hours,
                capacity_mb=self.config.copy_capacity_mb,
                data_root=self.data_root,
            )

        try:
            return _ensure(keys)
        except BridgeError as exc:  # 自愈钩子(与 query_history 同构)
            if exc.exit_code != DECRYPT_FAILED:
                raise
            if not memsearch.self_heal_armed(config=self.config, data_root=self.data_root):
                raise
            healed = memsearch.try_self_heal(
                storage, config=self.config, data_root=self.data_root
            )
            if healed is None:
                raise
            return _ensure(healed)

    def _open_copy(self, copy_dir: Path, rel: str) -> sqlite3.Connection:
        path = copy_dir / rel
        if not path.is_file():
            raise BridgeError(
                DECRYPT_FAILED,
                f"扫描所需解密副本不可用: {rel}(G5 重建流程未产出可用库)",
                fix_hint="重跑 localdb query 触发副本重建;持续失败先核密钥与 sqlcipher",
            )
        return sqlite3.connect(f"file:{path}?mode=ro", uri=True)

    def scan_once(self) -> float:
        """跑一轮(同步;常驻线程与门控测试共用)→ 本轮水位(epoch 秒)。"""
        since = read_watermark(self.data_root)
        if since is None:
            since = self.now_fn()  # 冷启动:不倒灌(历史走 Pull 端点)
        storage = self._locate()
        keys = self._resolve(storage)
        copy_info = self._ensure(storage, keys)
        copy_dir = Path(str(copy_info["dir"]))
        session_con = self._open_copy(copy_dir, "session/session.db")
        try:
            message_con = self._open_copy(copy_dir, "message/message_0.db")
        except BridgeError:
            session_con.close()
            raise
        stats: dict[str, Any] = {}
        try:
            events, new_watermark = scan_round(
                session_con,
                message_con,
                int(since),
                session_limit=self.session_limit,
                stats=stats,
            )
        finally:
            message_con.close()
            session_con.close()
        self.hub.publish_all(events)
        watermark = max(float(since), float(new_watermark))
        if new_watermark > since:
            write_watermark(self.data_root, new_watermark, now=self.now_fn())
        self.last_stats = stats
        self.last_watermark = watermark
        return watermark

    def start(self) -> None:
        if self._thread is not None:
            return
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._run, name="wechat-httpapi-watermark", daemon=True
        )
        self._thread.start()

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                self.scan_once()
            except BridgeError as exc:
                self._diag(f"watermark: 扫描未成({exc.name}),水位不推进")
            except Exception as exc:  # noqa: BLE001 - 常驻线程兜底:不炸进程
                self._diag(f"watermark: 扫描异常({type(exc).__name__}),水位不推进")
            self._stop.wait(self.interval_seconds)

    def stop(self, timeout: float | None = 2.0) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None

    @staticmethod
    def _diag(message: str) -> None:
        """stderr 摘要行(形状级;零聊天内容零密钥,红线 6)。"""
        try:
            sys.stderr.write(message + "\n")
        except OSError:  # pragma: no cover - stderr 关闭的极端形态
            pass


#: 内容锚(消费端去重契约的桥侧对照实现;PRD R6 形态,与
#: engines/wechat_local.py 锚同族——消费端自实现,桥侧仅供文档/测试对拍)。
def content_anchor(chat_id: str, ts: int, sender: str, text: str) -> str:
    """``sha1(chat|ts|sender|text)[:16]``(消费端去重锚;R6 契约字段)。"""
    digest = hashlib.sha1(
        f"{chat_id}|{ts}|{sender}|{text}".encode("utf-8")
    ).hexdigest()
    return digest[:16]
