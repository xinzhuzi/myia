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

**4.1.15 分表形态**(0.4.2 B0,2026-10-13 直查解密副本实测):消息库按
会话分表,表名 = ``Msg_`` + md5(username) 十六进制,**无会话列**;列族 =
local_id/server_id/local_type/sort_seq/real_sender_id/create_time(秒)/
status/upload_status/download_status/server_seq/origin_source/source/
message_content/compress_content/packed_info_data/WCDB_CT_message_content/
WCDB_CT_source。适配:①内容列候选补 ``message_content``;②无会话列的
``Msg_`` 前缀表按表名 md5 反解会话(message 库 ``Name2Id`` 表
``(user_name TEXT PRIMARY KEY, is_session INTEGER)`` 全表逐行算 md5 对
表名后缀,不单认查询参数本身的 md5);③发送者列 ``real_sender_id`` 经
Name2Id 的 rowid→user_name 反查(实测 246/246 Msg_ 表全覆盖、sender id
全在 rowid 集内);④``WCDB_CT_message_content`` 非 0 非空 = 该行内容
zstd 压缩(实测 CT=4 → message_content 为 BLOB、字节以魔数 x28 xb5 x2f
xfd 开头;CT=0/NULL = 未压 TEXT)——优先真解码(两级 import 链:
stdlib ``compression.zstd``(PEP 784/Python 3.14+)→ pip ``zstandard``
(自管 3.12 主路,pyproject 主依赖)),两级缺位或解压失败才落
媒体占位并计数,乱码绝不冒充内容。
"""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import Any

from .codes import DECRYPT_FAILED, BridgeError

try:  # stdlib zstd(PEP 784,Python 3.14+);缺位回落 pip zstandard(自管 3.12 主路)
    from compression import zstd as _zstd
except ImportError:  # pragma: no cover - 取决于解释器版本与装态
    try:
        import zstandard as _zstd  # type: ignore[no-redef]
    except ImportError:  # pragma: no cover - 两级都缺=占位+计数,不误吐乱码
        _zstd = None

__all__ = [
    "run_query",
    "find_message_tables",
    "name2id_maps",
    "query_messages",
    "lookup_contact",
]

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
_CONTENT_COLS = ("content", "Content", "strContent", "message", "message_content")
_SENDER_COLS = ("isSender", "is_sender", "IsSender")
#: 4.1.15 分表发送者列(整数 id,经 Name2Id rowid 反查;0.4.2 B0)。
_SENDER_ID_COLS = ("real_sender_id",)
#: 4.1.15 压缩标记列(WCDB zstd 影子列;非 0 非空 = 该行内容已压缩)。
_CT_CONTENT_COLS = ("WCDB_CT_message_content",)
_UNREAD_COLS = ("unreadCount", "unread_count", "UnReadCount", "unread")

#: 4.1.15 会话分表前缀(表名 = 前缀 + md5(username) 十六进制)。
_MD5_TABLE_PREFIX = "Msg_"

#: zstd 帧魔数(28 b5 2f fd;压缩内容字节以此开头,2026-10-13 实测)。
_ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"

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


def name2id_maps(con: sqlite3.Connection) -> tuple[dict[int, str], dict[str, str]]:
    """4.1.15 message 库 ``Name2Id`` 反查表(只读;表缺/列漂移 → 空映射)。

    Returns:
        ``(rowid → user_name, md5(user_name) hex → user_name)``——前者供
        ``real_sender_id`` 反查发送者,后者供 ``Msg_<md5>`` 表名反解会话
        (全表逐行算 md5,不单认查询参数;2026-10-13 实测 246/246 表全覆盖)。
    """
    id_to_name: dict[int, str] = {}
    md5_to_name: dict[str, str] = {}
    cols = _columns(con, "Name2Id")
    if not cols or _pick(cols, ("user_name",)) is None:
        return id_to_name, md5_to_name
    try:
        rows = con.execute('SELECT rowid, "user_name" FROM "Name2Id"').fetchall()
    except sqlite3.Error:
        return id_to_name, md5_to_name
    for rowid, user_name in rows:
        if isinstance(user_name, str) and user_name:
            id_to_name[int(rowid)] = user_name
            digest = hashlib.md5(user_name.encode("utf-8")).hexdigest()
            md5_to_name[digest] = user_name
    return id_to_name, md5_to_name


def find_message_tables(con: sqlite3.Connection) -> list[tuple[str, dict[str, str | None]]]:
    """自适应识别消息表(两种列签名,旧形态优先兼容)。

    ① 宽表形态:会话列+时间列+内容列齐备(4.x 早形 ``Msg_<hash>`` 宽表
    及其余同名族;既有识别逻辑,不变);② 4.1.15 分表形态:``Msg_`` 前缀
    +时间列+内容列、**无会话列**(会话编码在表名 md5 里,经 ``Name2Id``
    反解挂到 ``colmap["chat"]``;反解不出的表如实挂 ``None``)。返回
    ``(表名, 列映射)`` 列表。
    """
    try:
        tables = [
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    except sqlite3.Error:
        return []
    found: list[tuple[str, dict[str, str | None]]] = []
    md5_to_name: dict[str, str] | None = None  # 懒加载:仅在遇到无会话列分表时读
    ordered = sorted(tables, key=lambda t: (not t.startswith("Msg_"), t))
    for table in ordered:
        columns = _columns(con, table)
        colmap: dict[str, str | None] = {
            "talker": _pick(columns, _TALKER_COLS),
            "time": _pick(columns, _TIME_COLS),
            "type": _pick(columns, _TYPE_COLS),
            "content": _pick(columns, _CONTENT_COLS),
            "sender": _pick(columns, _SENDER_COLS),
            "sender_id": _pick(columns, _SENDER_ID_COLS),
            "ct_content": _pick(columns, _CT_CONTENT_COLS),
        }
        if colmap["talker"] and colmap["time"] and colmap["content"]:
            found.append((table, colmap))
            continue
        if (
            table.startswith(_MD5_TABLE_PREFIX)
            and colmap["time"]
            and colmap["content"]
        ):
            if md5_to_name is None:
                _ids, md5_to_name = name2id_maps(con)
            colmap["chat"] = md5_to_name.get(table[len(_MD5_TABLE_PREFIX) :].lower())
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


def _bump(stats: dict[str, object] | None, key: str) -> None:
    if stats is not None:
        stats[key] = int(stats.get(key, 0)) + 1


def _is_compressed(content: Any, ct_marker: Any) -> bool:
    """压缩判定:WCDB_CT 标记非 0 非空,或内容字节自带 zstd 魔数。

    实测(2026-10-13,TMS 群表 CT 分布):CT=4 → BLOB 且魔数开头;
    CT=0/NULL → 未压 TEXT。两个信号取或,单一信号缺失不误判。
    """
    if ct_marker is not None:
        try:
            if int(ct_marker) != 0:
                return True
        except (TypeError, ValueError):
            return True  # 标记列形状异常:按压缩走,解不开自会占位
    return isinstance(content, (bytes, bytearray, memoryview)) and bytes(
        content[:4]
    ) == _ZSTD_MAGIC


def _decode_text_content(
    content: Any, ct_marker: Any, stats: dict[str, object] | None
) -> tuple[str | None, str | None]:
    """文本内容解码 → ``(text, placeholder)`` 二元组(恰一非 None)。

    4.1.15 压缩行优先真解码(stdlib ``compression.zstd``,3.14+);模块
    缺位/解压失败/UTF-8 解不开 → 媒体占位并计数(``zstd_module_missing``/
    ``zstd_decode_failed``/``text_decode_failed``;成功解码计
    ``zstd_decoded``)。乱码绝不冒充内容(prd 红线 6 同源纪律)。
    """
    if _is_compressed(content, ct_marker):
        if _zstd is None:
            _bump(stats, "zstd_module_missing")
            return None, _MEDIA_PLACEHOLDER
        if not isinstance(content, (bytes, bytearray, memoryview)):
            _bump(stats, "zstd_decode_failed")
            return None, _MEDIA_PLACEHOLDER
        try:
            text = bytes(_zstd.decompress(bytes(content))).decode("utf-8")
        except Exception:  # noqa: BLE001 - 解码边界:坏帧/坏UTF-8 一律占位
            # (compression.zstd.ZstdError 等异常类型随解释器版本在场性不定,
            # 此处只认「解不出就占位」的语义,不认具体异常族)
            _bump(stats, "zstd_decode_failed")
            return None, _MEDIA_PLACEHOLDER
        _bump(stats, "zstd_decoded")
        return text, None
    if isinstance(content, str):
        return content, None
    if isinstance(content, (bytes, bytearray, memoryview)):
        try:  # 未压 BLOB:严格 UTF-8 能解才是真文本,解不开如实占位
            return bytes(content).decode("utf-8"), None
        except UnicodeDecodeError:
            _bump(stats, "text_decode_failed")
            return None, _MEDIA_PLACEHOLDER
    return None, _MEDIA_PLACEHOLDER


def _sender_name(
    raw_id: Any, id_to_name: dict[int, str], chat_id: str
) -> str:
    """4.1.15 发送者:real_sender_id(Name2Id rowid)反查 user_name。

    反查失败(行不在 Name2Id/形状异常)回落会话 id——与无发送者列的
    旧形态同一「无从归因即归会话」惯例,不臆造。
    """
    try:
        rid = int(raw_id)
    except (TypeError, ValueError):
        return chat_id
    return id_to_name.get(rid) or chat_id


def query_messages(
    con: sqlite3.Connection,
    chat_id: str,
    since_ts: int,
    limit: int,
    *,
    stats: dict[str, object] | None = None,
) -> list[dict[str, object]]:
    """查指定会话最近消息(全识别表并集;时间倒序;limit 截断)。

    每条 = {"ts","sender","type","text"?,"media_placeholder"?};文本消息才
    携带 text,媒体类落类型占位(prd R1a 语义)。4.1.15 分表(0.4.2 B0):
    无会话列表按 ``colmap["chat"]``(表名 md5 反解)选表,发送者经
    ``real_sender_id`` → Name2Id rowid 反查,压缩行解码/占位计数进
    ``stats``(缺省 None = 不收集)。
    """
    tables = find_message_tables(con)
    id_to_name: dict[int, str] = {}
    if any(colmap.get("sender_id") for _table, colmap in tables):
        id_to_name = name2id_maps(con)[0]
    messages: list[dict[str, object]] = []
    for table, colmap in tables:
        cols = [colmap["time"], colmap["content"]]
        idx = {"time": 0, "content": 1}
        for key in ("type", "sender", "sender_id", "ct_content"):
            if colmap.get(key):
                idx[key] = len(cols)
                cols.append(colmap[key])
        quoted = ", ".join(chr(34) + c + chr(34) for c in cols)
        if colmap["talker"]:
            sql = (
                f"SELECT {quoted} FROM \"{table}\" "
                f'WHERE "{colmap["talker"]}" = ? AND "{colmap["time"]}" >= ? '
                f'ORDER BY "{colmap["time"]}" DESC LIMIT ?'
            )
            params: tuple[object, ...] = (chat_id, since_ts, limit)
        elif colmap.get("chat") == chat_id:
            sql = (
                f'SELECT {quoted} FROM "{table}" '
                f'WHERE "{colmap["time"]}" >= ? '
                f'ORDER BY "{colmap["time"]}" DESC LIMIT ?'
            )
            params = (since_ts, limit)
        else:
            continue  # 会话归属不明的分表:无法按 chat 过滤,如实跳过
        try:
            rows = con.execute(sql, params).fetchall()
        except sqlite3.Error:
            continue  # 单表漂移不拖垮整个查询(红线 7:如实降级)
        for row in rows:
            ts = _normalize_ts(row[idx["time"]])
            content = row[idx["content"]]
            msg_type = 1
            if "type" in idx:
                try:
                    msg_type = int(row[idx["type"]] or 0)
                except (TypeError, ValueError):
                    msg_type = 0
            if "sender" in idx:  # 旧形态 isSender(0/1)
                sender = "me" if row[idx["sender"]] == 1 else chat_id
            elif "sender_id" in idx:  # 4.1.15 real_sender_id → Name2Id 反查
                sender = _sender_name(row[idx["sender_id"]], id_to_name, chat_id)
            else:
                sender = chat_id
            entry: dict[str, object] = {
                "ts": ts,
                "sender": sender,
                "type": MSG_TYPE_NAMES.get(msg_type, f"type_{msg_type}"),
            }
            if msg_type == 1:
                text, placeholder = _decode_text_content(
                    content,
                    row[idx["ct_content"]] if "ct_content" in idx else None,
                    stats,
                )
                if text is not None:
                    entry["text"] = text
                else:
                    entry["media_placeholder"] = placeholder
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
    decode_stats: dict[str, object] = {"zstd_available": _zstd is not None}
    try:
        messages = query_messages(con, chat_id, since_ts, limit, stats=decode_stats)
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
        "content_decode": decode_stats,
        "display_name": display_name,
        "sessions": sessions,
        "domains": domain_status,
        "copy": copy_info,
    }
