"""E3 三域只读查询(task 10-11-wechat-ui-bridge;G4:message/session/contact)。

对**解密副本**(数据根私有区,``localdb.ensure_decrypted_copies`` 产物)
做纯只读 SQL:指定会话最近 N 天文本消息 + 联系人名解析 + 会话列表
(best-effort)。零出网、零微信进程接触;查询结果 = CLI stdout 契约载荷,
不入日志、不入 git(prd 红线 6)。

**表结构自适应**(prd 红线 7 版本脆弱性):微信 4.x 的 message 库是
``Msg_<hash>`` 宽表(公开参考:luvrell/wechat-msg-extract
``scripts/test_exporter.py:16-24``——localId/serverId/localType/createTime/
isSender/strTalker/content;contact 库 ``contact`` 表),但列名/表名随版本
可能漂移——本层不写死单一表名,按「列签名」自适应识别(时间列+会话列+
内容列齐备才算消息表);识别失败 = 结构化报错/空结果如实上报,不猜。
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from .codes import DECRYPT_FAILED, BridgeError

__all__ = ["run_query", "find_message_tables", "query_messages", "lookup_contact"]

#: 微信消息 localType → 类型名(公开常量表;未知类型回落 type_<N>)。
MSG_TYPE_NAMES: dict[int, str] = {
    1: "text",
    3: "image",
    34: "voice",
    43: "video",
    47: "sticker",
    48: "location",
    49: "file_or_link",
    10000: "system",
    10002: "revoke",
}

# 列名候选族(自适应识别;命中顺序即优先序)。
_TALKER_COLS = ("strTalker", "str_talker", "talker", "ChatName", "chat_name")
_TIME_COLS = ("createTime", "create_time", "CreateTime", "timestamp", "msgCreateTime")
_TYPE_COLS = ("localType", "local_type", "Type", "type", "msgType")
_CONTENT_COLS = ("content", "Content", "strContent", "message")
_SENDER_COLS = ("isSender", "is_sender", "IsSender")
_UNREAD_COLS = ("unreadCount", "unread_count", "UnReadCount", "unread")

#: 媒体占位语义(prd:图片/文件类先落「类型+占位描述」,不做内容识别)。
_MEDIA_PLACEHOLDER = "非文本消息,内容未导出(占位)"


def _open_copy(copy_dir: Path, rel: str) -> sqlite3.Connection | None:
    """只读打开副本库(缺失/损坏 → None 如实;URI mode=ro 零写入)。"""
    path = copy_dir / rel
    if not path.is_file():
        return None
    try:
        return sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    except sqlite3.Error:
        return None


def _columns(con: sqlite3.Connection, table: str) -> list[str]:
    try:
        return [row[1] for row in con.execute(f'PRAGMA table_info("{table}")')]
    except sqlite3.Error:
        return []


def _pick(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    lowered = {c.lower(): c for c in columns}
    for cand in candidates:
        actual = lowered.get(cand.lower())
        if actual is not None:
            return actual
    return None


def find_message_tables(con: sqlite3.Connection) -> list[tuple[str, dict[str, str]]]:
    """自适应识别消息表(列签名:会话列+时间列+内容列齐备)。

    优先 ``Msg_`` 前缀表(4.x 分片内每会话一表的公开形态),其余表按同
    签名兜底;返回 ``(表名, 列映射)`` 列表。
    """
    try:
        tables = [
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    except sqlite3.Error:
        return []
    found: list[tuple[str, dict[str, str]]] = []
    ordered = sorted(tables, key=lambda t: (not t.startswith("Msg_"), t))
    for table in ordered:
        columns = _columns(con, table)
        colmap = {
            "talker": _pick(columns, _TALKER_COLS),
            "time": _pick(columns, _TIME_COLS),
            "type": _pick(columns, _TYPE_COLS),
            "content": _pick(columns, _CONTENT_COLS),
            "sender": _pick(columns, _SENDER_COLS),
        }
        if colmap["talker"] and colmap["time"] and colmap["content"]:
            found.append((table, colmap))
    return found


def _normalize_ts(value: Any) -> int:
    """时间归一(秒;毫秒值启发式回落)。"""
    try:
        ts = int(value)
    except (TypeError, ValueError):
        return 0
    if ts > 10**12:  # 毫秒 → 秒
        ts //= 1000
    return ts


def query_messages(
    con: sqlite3.Connection, chat_id: str, since_ts: int, limit: int
) -> list[dict[str, object]]:
    """查指定会话最近消息(全识别表并集;时间倒序;limit 截断)。

    每条 = {"ts","sender","type","text"?,"media_placeholder"?};文本消息才
    携带 text,媒体类落类型占位(prd R1a 语义)。
    """
    messages: list[dict[str, object]] = []
    for table, colmap in find_message_tables(con):
        cols = [colmap["time"], colmap["content"]]
        if colmap["type"]:
            cols.append(colmap["type"])
        if colmap["sender"]:
            cols.append(colmap["sender"])
        sql = (
            f'SELECT {", ".join(chr(34) + c + chr(34) for c in cols)} '
            f'FROM "{table}" WHERE "{colmap["talker"]}" = ? '
            f'AND "{colmap["time"]}" >= ? ORDER BY "{colmap["time"]}" DESC LIMIT ?'
        )
        try:
            rows = con.execute(sql, (chat_id, since_ts, limit)).fetchall()
        except sqlite3.Error:
            continue  # 单表漂移不拖垮整个查询(红线 7:如实降级)
        for row in rows:
            ts = _normalize_ts(row[0])
            content = row[1]
            type_col_idx = 2
            msg_type = 1
            if colmap["type"]:
                try:
                    msg_type = int(row[type_col_idx] or 0)
                except (TypeError, ValueError):
                    msg_type = 0
            entry: dict[str, object] = {
                "ts": ts,
                "sender": "me" if (colmap["sender"] and row[len(cols) - 1] == 1) else chat_id,
                "type": MSG_TYPE_NAMES.get(msg_type, f"type_{msg_type}"),
            }
            if msg_type == 1 and isinstance(content, str):
                entry["text"] = content
            else:
                entry["media_placeholder"] = _MEDIA_PLACEHOLDER
            messages.append(entry)
    messages.sort(key=lambda item: int(item["ts"]), reverse=True)
    return messages[:limit]


def lookup_contact(con: sqlite3.Connection, chat_id: str) -> str | None:
    """contact 域:会话 id → 展示名(remark > nickname > alias;best-effort)。"""
    name_cols = ("remark", "Remark", "conRemark", "nickname", "nickName", "NickName", "alias")
    id_cols = ("username", "userName", "UserName", "user_name")
    try:
        tables = [
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    except sqlite3.Error:
        return None
    for table in tables:
        if "contact" not in table.lower():
            continue
        columns = _columns(con, table)
        id_col = _pick(columns, id_cols)
        if id_col is None:
            continue
        for name_col in name_cols:
            actual = next((c for c in columns if c.lower() == name_col.lower()), None)
            if actual is None:
                continue
            try:
                row = con.execute(
                    f'SELECT "{actual}" FROM "{table}" WHERE "{id_col}" = ?',
                    (chat_id,),
                ).fetchone()
            except sqlite3.Error:
                continue
            if row and isinstance(row[0], str) and row[0].strip():
                return row[0]
    return None


def list_sessions(con: sqlite3.Connection, limit: int) -> list[dict[str, object]]:
    """session 域:会话列表 best-effort(id + 展示名 + 未读数(缺列则 null))。"""
    try:
        tables = [
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    except sqlite3.Error:
        return []
    for table in sorted(tables, key=lambda t: ("session" not in t.lower(), t)):
        if "session" not in table.lower():
            continue
        columns = _columns(con, table)
        talker = _pick(columns, _TALKER_COLS) or _pick(columns, id_cols_tuple())
        if talker is None:
            continue
        unread = _pick(columns, _UNREAD_COLS)
        name_col = _pick(columns, ("nickName", "nickname", "NickName", "remark", "displayName"))
        select = [talker]
        if name_col:
            select.append(name_col)
        if unread:
            select.append(unread)
        try:
            rows = con.execute(
                f'SELECT {", ".join(chr(34) + c + chr(34) for c in select)} '
                f'FROM "{table}" LIMIT ?',
                (limit,),
            ).fetchall()
        except sqlite3.Error:
            continue
        sessions: list[dict[str, object]] = []
        for row in rows:
            # 列序固定:[talker, name?, unread?]——name/unread 按在场拼装,
            # 缺列如实 null(不臆造 0)。
            item: dict[str, object] = {"id": row[0]}
            idx = 1
            item["name"] = row[idx] if name_col else row[0]
            if name_col:
                idx += 1
            item["unread"] = row[idx] if unread else None
            sessions.append(item)
        return sessions
    return []


def id_cols_tuple() -> tuple[str, ...]:
    """会话 id 列候选(session 表可能直接用 contact 的 id 列名)。"""
    return ("username", "userName", "UserName", "user_name", "strTalker")


def run_query(
    *,
    copy_dir: Path,
    domains: list[str],
    chat_id: str,
    since_days: int,
    limit: int,
    copy_info: dict[str, object],
) -> dict[str, object]:
    """E3 三域查询编排(G4:域清单来自配置;缺域如实降级不装死)。"""
    import time

    domain_status: dict[str, str] = {}
    for domain in domains:
        rel_map = {
            "message": "message/message_0.db",
            "contact": "contact/contact.db",
            "session": "session/session.db",
        }
        rel = rel_map.get(domain)
        if rel is None:
            domain_status[domain] = "unknown_domain"
            continue
        path = copy_dir / rel
        domain_status[domain] = "ok" if path.is_file() else "copy_missing"

    message_rels = ("message/message_0.db", "message/biz_message_0.db")
    con = None
    for rel in message_rels:
        con = _open_copy(copy_dir, rel)
        if con is not None:
            break
    if con is None:
        raise BridgeError(
            DECRYPT_FAILED,
            "message 域解密副本不可用(副本缺失或损坏;G5 重建流程未产出可用库)",
            fix_hint="重跑 localdb query 触发副本重建;持续失败先核密钥与 sqlcipher(design §5.1)",
        )

    since_ts = int(time.time()) - since_days * 86400
    try:
        messages = query_messages(con, chat_id, since_ts, limit)
    finally:
        con.close()

    display_name: str | None = None
    sessions: list[dict[str, object]] = []
    contact_con = _open_copy(copy_dir, "contact/contact.db") if "contact" in domains else None
    if contact_con is not None:
        try:
            display_name = lookup_contact(contact_con, chat_id)
        finally:
            contact_con.close()
    session_con = _open_copy(copy_dir, "session/session.db") if "session" in domains else None
    if session_con is not None:
        try:
            sessions = list_sessions(session_con, 20)
        finally:
            session_con.close()

    return {
        "chat_id": chat_id,
        "since_days": since_days,
        "messages": messages,
        "display_name": display_name,
        "sessions": sessions,
        "domains": domain_status,
        "copy": copy_info,
    }
