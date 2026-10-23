"""新消息通知扫描 + 撤回检测/恢复(task 10-14-wechat-notify-revoke C5,R1)。

对**解密副本**(数据根私有区,``localdb.ensure_decrypted_copies`` 产物)做
纯只读两层扫描,零微信进程接触、零微信侧写入(``mode=ro`` 查询纪律同
:mod:`wechat_bridge.localdb_query`):

- **R1.1 会话基线层(便宜先筛)**:单查 ``SessionTable``(表名/列名按
  ``_pick`` 列签名自适应,直查纪律同 group_info);仅对**白名单内**会话比
  对基线 ``{ts, unread}``——候选 = ``last_timestamp`` 前进 OR ``unread``
  变化 OR ``last_msg_type == 10002`` OR 无基线;非白名单会话**零二次查询**
  (白名单外 = 不通知,不声明即屏蔽)。2026-10-14 真库实测:表名
  ``SessionTable``、454 行、``username/unread_count/last_timestamp/
  last_msg_type/summary/last_sender_display_name`` 列全在场。
- **R1.2 定点增量层(仅候选会话)**:对候选会话的 ``Msg_<md5(username)>``
  分表(经 ``name2id_maps`` md5 映射选表)查 ``create_time >= 水位-90s
  ORDER BY create_time DESC LIMIT 20``(server_id/local_id/sort_seq/
  local_type/real_sender_id/message_content/compress_content/WCDB_CT 全列);
  自消息过滤(``real_sender_id`` → Name2Id → username == 账号 wxid,
  ``all_users/login/<wxid>/`` 目录名)默认不出事件;预览 80 字。首轮无
  基线 = 当前时刻,**只建基线零事件**(防装机首弹轰炸;lookback 90s 兜住
  首轮进行中到达的消息)。性能铁律:严禁全库扫——SessionTable 全表 1 次 +
  候选分表定点。
- **R1.3 撤回检测与恢复阶梯** + **R1.5 revoke-list**(同一函数族两壳):
  谓词 ``local_type == 10002`` OR(``10000`` AND 内容标记);恢复阶梯
  server_id 直查 → 时间近邻启发式 → replacemsg 文本兜底 → none,
  ``recovery`` 字段如实标注;自撤回不出事件;同撤回双到达抑制。

**来源纪律(拷问修正①,写死)**:hicccc77/WeFlow(CC BY-NC-SA 4.0)与
imldy/chatlog fork(Apache-2.0)均**只做语义参照,不逐行对写、零代码
借入**——本文件水位/谓词/恢复阶梯全部按语义重写;若未来需要逐段参考
chatlog 代码,须先补 Apache-2.0 归属协议(保留 LICENSE/NOTICE/变更声明)
再动手,此处不预支。

**只读红线**:全程解密副本;禁任何微信侧写入与拦截件安装(WeFlow 向
微信消息表写 SQLite trigger 的「防撤回」层显式剥离,不做不模仿不进货
——AC7 守卫词面另行核验,此处只述语义)。

**性能/并发(拷问修正②③)**:

- 副本侧 create_time 索引 = **统一副本写政策的单点件**
  :func:`ensure_ct_indexes`(命名 ``idx_<表>_ct``,与 C1 聊天导出批的
  索引方案同名同规;只在 ensure 之后、只对副本、幂等 ``IF NOT EXISTS``,
  懒建 = 仅本轮真正要点查的表)。不在查询热路径另起索引,不碰源库。
- sqlite busy(``database is locked``——*/1 cron 与 C1 建索引/C2 长查询
  同库并发时的常态)**降级语义 = 本轮跳过不判死**:该查询面放弃、
  ``stats.db_busy = true``、事件少出但 exit 0;候选会话水位不推进(下轮
  重开,lookback+主机侧锚去重消化重叠;``ensure_decrypted_copies`` 的
  副本单飞锁管重建串行,读侧竞争只有短窗)。非 busy 的 sqlite 异常按
  副本损坏如实 ``decrypt_failed``(sns_query 判例)。

私有数据红线:查询结果 = CLI stdout 契约载荷,不入日志、不入 git;错误
消息只承载形状计数。
"""

from __future__ import annotations

import json
import re
import sqlite3
import time
from pathlib import Path
from typing import Any

from .codes import DECRYPT_FAILED, EXIT_USAGE, BridgeError
from .localdb_query import (
    MSG_TYPE_NAMES,
    _columns,
    _contact_pick_names,
    _decode_text_content,
    _normalize_ts,
    _open_copy,
    _pick,
    _sender_name,
    find_message_tables,
    name2id_maps,
)

__all__ = [
    "LOOKBACK_SECONDS",
    "PREVIEW_CHARS",
    "REVOKE_MARKERS",
    "ROW_LIMIT",
    "SESSION_TABLE",
    "ensure_ct_indexes",
    "extract_revoke_server_ids",
    "extract_replacemsg_text",
    "is_revoke_row",
    "login_wxid",
    "notify_scan",
    "read_scan_payload",
    "revoke_list",
    "run_notify_scan",
    "run_revoke_list",
]

#: 会话基线表(2026-10-14 直查解密副本实测;缺表 = 零事件如实降级)。
SESSION_TABLE = "SessionTable"

#: R1.2 lookback 常量(秒):轮询周期 60s + 副本刷新滞后裕量(WeFlow 的
#: 2s 是 350ms 实时态专用,不适用);重读重叠由主机侧锚去重沉默消化。
LOOKBACK_SECONDS = 90

#: 通知预览截断(R1.2;约束节「通知预览 80 字帽」)。
PREVIEW_CHARS = 80

#: 单会话单轮行上限(R1.2 SQL LIMIT)。
ROW_LIMIT = 20

#: 系统行/撤回行 local_type(localdb_query.MSG_TYPE_NAMES 同源值)。
_SYSTEM_TYPE = 10000
_REVOKE_TYPE = 10002

#: R1.3 撤回谓词内容标记(10000 行须含其一才算撤回;WeFlow 语义参照)。
REVOKE_MARKERS: tuple[str, ...] = (
    "revokemsg",
    "<replacemsg",
    "撤回了一条消息",
    "尝试撤回此消息",
)

#: 自撤回内容标记(你撤回 = 账号本人撤回,不出事件)。
_SELF_REVOKE_MARKER = "你撤回"

#: R1.3 撤回行内容里的原消息 server_id 键(正则同时匹配 XML 属性
#: ``newmsgid="123"`` 与元素文本 ``<newmsgid>123</newmsgid>`` 两种形态;
#: 命中序即恢复阶梯的尝试序)。
_SERVER_ID_KEYS: tuple[str, ...] = ("newmsgid", "sessionmsgid", "svrid", "oldmsgid")  # noqa: RUF012 - 文档锚
_SERVER_ID_RE = re.compile(
    r"(newmsgid|sessionmsgid|svrid|oldmsgid)(?:\s*=\s*\"|>)(\d+)",
    re.IGNORECASE,
)

#: XML ``<replacemsg>`` 文本(CDATA 与裸文本两形;replacemsg 兜底数据源)。
_REPLACEMSG_RE = re.compile(
    r"<replacemsg>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</replacemsg>", re.DOTALL
)

# 列名候选族(_pick 自适应;2026-10-14 实测列名为首位候选)。
_SESSION_ID_COLS = ("username", "userName", "UserName", "user_name", "strTalker")
_SESSION_UNREAD_COLS = ("unread_count", "unreadCount", "UnReadCount", "unread")
_SESSION_TS_COLS = ("last_timestamp", "lastTimestamp", "LastTimestamp")
_SESSION_TYPE_COLS = ("last_msg_type", "lastMsgType", "LastMsgType")

_LOCAL_ID_COLS = ("local_id", "localId")
_SERVER_ID_COLS = ("server_id", "serverId")
_SORT_SEQ_COLS = ("sort_seq", "sortSeq")
_TYPE_COLS = ("local_type", "localType")
_SENDER_ID_COLS = ("real_sender_id",)
_CONTENT_COLS = ("message_content", "content", "Content", "strContent")
_COMPRESS_COLS = ("compress_content",)
_CT_CONTENT_COLS = ("WCDB_CT_message_content",)

#: 消息域副本清单(message_0 主库 + biz_message_0;两库都开,谁的
#: ``Msg_<md5>`` 表归属该会话就查谁——run_query 只开首个在场库是单会话
#: 历史查询的取舍,notify 的分表定点天然两库各查各的)。
_MESSAGE_DB_RELS: tuple[str, ...] = (
    "message/message_0.db",
    "message/biz_message_0.db",
)

#: 副本侧 create_time 索引后缀(统一索引方案:``idx_<表>_ct``,与 C1
#: 聊天导出批同名同规;归属 ensure 后单点,见模块 docstring)。
_CT_INDEX_SUFFIX = "_ct"

#: 建索引的 busy 等待窗(秒):并发读者在场时放弃本轮索引(查询走扫,
#: 性能面不判死——拷问修正③的同一降级语义)。
_INDEX_BUSY_TIMEOUT_SECONDS = 2.0

#: 行键序(R1.2 全列契约的载荷侧名字)。
_ROW_KEYS = (
    "local_id", "server_id", "sort_seq", "time", "type",
    "sender_id", "content", "compress", "ct_content",
)


def _is_busy_error(exc: sqlite3.Error) -> bool:
    """sqlite busy/locked 族判定(锁竞争 = 本轮跳过不判死)。"""
    text = str(exc).lower()
    return "locked" in text or "busy" in text


def _to_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _duration_ms(started: float) -> int:
    return int((time.monotonic() - started) * 1000)


def _copy_query_error(label: str, exc: sqlite3.Error) -> BridgeError:
    """非 busy 的 sqlite 异常 → 副本损坏形状(解密失败族,sns_query 判例)。"""
    return BridgeError(
        DECRYPT_FAILED,
        f"notify 副本查询失败({label}:{type(exc).__name__});疑似副本损坏",
        fix_hint="删除数据根 wechat-localdb/decrypted/ 对应域触发下轮重建(纯派生缓存,安全)",
    )


# =====================================================================
# 账号 wxid(自消息/自撤回判定数据源)
# =====================================================================


def login_wxid(db_storage: Path) -> str | None:
    """当前账号 wxid(``<数据根>/all_users/login/<wxid>/key_info.db`` 目录名)。

    复用 :func:`wechat_bridge.localdb.locate_key_info_db` 的多候选择一逻辑
    (账号目录前缀优先,其余 mtime 最新);定位失败 = None 如实(自消息
    过滤退化为不过滤,不臆造)。best-effort,永不判错。
    """
    from . import localdb

    try:
        return localdb.locate_key_info_db(db_storage).parent.name
    except BridgeError:
        return None


# =====================================================================
# 副本侧 create_time 索引(统一副本写政策单点;拷问修正②)
# =====================================================================


def ensure_ct_indexes(copy_dir: Path, tables: list[tuple[str, str]]) -> list[str]:
    """副本侧懒建 ``idx_<表>_ct(create_time)`` 索引(幂等;仅副本)。

    - **只在 ensure 之后**的解密副本上执行(源库永不触碰——只读红线);
    - 命名与 C1 聊天导出批统一(``idx_<表>_ct``),不另起第二套索引;
    - 懒建:只对本轮真正要点查的表(候选会话分表/revoke-list 目标表),
      不预铺全库 400+ 表;
    - busy(并发读/重建短窗)→ 放弃本轮该索引,查询走全表扫(性能面
      降级不判死);表不在该库 → 跳过(两库各自建各自的)。

    Returns:
        实际创建的索引名清单(已存在的幂等跳过不计)。
    """
    created: list[str] = []
    for rel in _MESSAGE_DB_RELS:
        path = copy_dir / rel
        if not path.is_file():
            continue
        try:
            con = sqlite3.connect(path, timeout=_INDEX_BUSY_TIMEOUT_SECONDS)
        except sqlite3.Error:
            continue
        try:
            existing = {
                row[0]
                for row in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='index'"
                )
            }
            for table, time_col in tables:
                if not table or not time_col:
                    continue
                index_name = f"idx_{table}{_CT_INDEX_SUFFIX}"
                if index_name in existing:
                    continue  # 幂等:已在场零动作(不占写锁)
                try:
                    con.execute(
                        f'CREATE INDEX IF NOT EXISTS "{index_name}" '
                        f'ON "{table}" ("{time_col}")'
                    )
                except sqlite3.OperationalError:
                    continue  # busy/缺表:本轮放弃,查询走扫
                con.commit()
                created.append(index_name)
        finally:
            con.close()
    return created


# =====================================================================
# 撤回谓词与恢复阶梯(R1.3;notify-scan 与 revoke-list 共用同一函数族)
# =====================================================================


def _decoded_text(row: dict[str, Any]) -> str:
    """行内容解码(zstd/UTF-8/占位;message_content 优先,空则试
    compress_content 列——R1.2 全列契约里 compress_content 的消费位)。"""
    content = row.get("content")
    ct_marker = row.get("ct_content")
    text, placeholder = _decode_text_content(content, ct_marker, None)
    if text is None and row.get("compress") is not None:
        text, _fallback = _decode_text_content(row.get("compress"), ct_marker, None)
    if text is None:
        text = placeholder or ""
    return text


def _preview(text: str, limit: int = PREVIEW_CHARS) -> str:
    """预览:压空白(群消息 ``wxid:\\n`` 前缀拍平)后截断。"""
    flat = " ".join(text.split())
    if len(flat) <= limit:
        return flat
    return flat[:limit] + "…"


def _type_preview(local_type: int, text: str) -> str:
    """事件预览:文本行用真文本;非文本行落类型词面(``[图片]`` 族)。"""
    if local_type == 1 and text.strip():
        return _preview(text)
    name = MSG_TYPE_NAMES.get(local_type, f"type_{local_type}")
    return f"[{name}]"


def is_revoke_row(local_type: int, content_text: str) -> bool:
    """R1.3 撤回谓词:``10002`` OR(``10000`` AND 内容标记)。"""
    if local_type == _REVOKE_TYPE:
        return True
    if local_type == _SYSTEM_TYPE:
        return any(marker in content_text for marker in REVOKE_MARKERS)
    return False


def extract_revoke_server_ids(content_text: str) -> list[int]:
    """撤回行内容 → 候选原消息 server_id 清单(键优先序 = 阶梯尝试序,去重)。"""
    priority = {key: index for index, key in enumerate(_SERVER_ID_KEYS)}
    matches = [
        (priority.get(key.lower(), len(priority)), int(value))
        for key, value in _SERVER_ID_RE.findall(content_text or "")
    ]
    ids: list[int] = []
    seen: set[int] = set()
    for _rank, parsed in sorted(matches):
        if parsed > 0 and parsed not in seen:
            seen.add(parsed)
            ids.append(parsed)
    return ids


def extract_replacemsg_text(content_text: str) -> str | None:
    """``<replacemsg>`` 文本兜底(如「"张三"撤回了一条消息」)。"""
    match = _REPLACEMSG_RE.search(content_text or "")
    if match is None:
        return None
    text = " ".join(match.group(1).split())
    return text or None


def _build_row_select(
    con: sqlite3.Connection, table: str
) -> tuple[str, list[str]] | None:
    """构造全列 SELECT 的 (SQL 前缀, 列名序);time/content 缺 = None。"""
    columns = _columns(con, table)
    picks = {
        "local_id": _pick(columns, _LOCAL_ID_COLS),
        "server_id": _pick(columns, _SERVER_ID_COLS),
        "sort_seq": _pick(columns, _SORT_SEQ_COLS),
        "time": _pick(columns, ("create_time", "createTime")),
        "type": _pick(columns, _TYPE_COLS),
        "sender_id": _pick(columns, _SENDER_ID_COLS),
        "content": _pick(columns, _CONTENT_COLS),
        "compress": _pick(columns, _COMPRESS_COLS),
        "ct_content": _pick(columns, _CT_CONTENT_COLS),
    }
    if not picks["time"] or not picks["content"]:
        return None
    names = [picks[key] or "" for key in _ROW_KEYS]
    quoted = ", ".join(f'"{name}"' for name in names if name)
    return f'SELECT {quoted} FROM "{table}" ', names


def _row_to_dict(row: tuple, names: list[str]) -> dict[str, Any]:
    """行元组 → 键控 dict(缺失列不进 dict;列序 = _ROW_KEYS 序)。"""
    result: dict[str, Any] = {}
    index = 0
    for key, name in zip(_ROW_KEYS, names):
        if name:
            result[key] = row[index]
            index += 1
    return result


def _chat_message_table(
    con: sqlite3.Connection, chat_id: str
) -> tuple[str, dict[str, Any]] | None:
    """该会话在该库的消息表:①4.1.15 分表按 ``colmap['chat']`` 精确归属;
    ②旧形态宽表(有会话列)兜底(SQL 按 talker 过滤,挂 ``_chat_id``)。"""
    tables = find_message_tables(con)
    for table, colmap in tables:
        if colmap.get("chat") == chat_id:
            return table, dict(colmap)
    for table, colmap in tables:
        if colmap.get("talker"):
            wide = dict(colmap)
            wide["_chat_id"] = chat_id
            return table, wide
    return None


def _fetch_recent_rows(
    con: sqlite3.Connection,
    table: str,
    since_ts: int,
    limit: int,
    *,
    talker: str | None = None,
    chat_id: str | None = None,
) -> list[dict[str, Any]] | None:
    """R1.2 定点增量查询(``create_time >= since DESC LIMIT``)。

    busy → None(调用方跳过该会话,水位不推进);其余 sqlite 异常上抛由
    调用方归 decrypt_failed。``talker``+``chat_id`` 在场 = 旧形态宽表按
    会话列过滤(colmap["_chat_id"] 挂的声明会话)。
    """
    built = _build_row_select(con, table)
    if built is None:
        return []
    prefix, names = built
    keys = dict(zip(_ROW_KEYS, names))
    time_col = keys["time"]
    if talker and chat_id:
        sql = (
            f"{prefix}WHERE \"{time_col}\" >= ? AND \"{talker}\" = ? "
            f'ORDER BY "{time_col}" DESC LIMIT ?'
        )
        params: tuple[Any, ...] = (since_ts, chat_id, limit)
    else:
        sql = f'{prefix}WHERE "{time_col}" >= ? ORDER BY "{time_col}" DESC LIMIT ?'
        params = (since_ts, limit)
    try:
        rows = con.execute(sql, params).fetchall()
    except sqlite3.OperationalError as exc:
        if _is_busy_error(exc):
            return None
        raise
    return [_row_to_dict(row, names) for row in rows]


def _recover_original(
    con: sqlite3.Connection,
    table: str,
    revoke_row: dict[str, Any],
    revoke_text: str,
    self_name: str | None,
    id_to_name: dict[int, str],
) -> tuple[dict[str, Any] | None, str, str | None]:
    """R1.3 恢复阶梯 → ``(original_row, recovery, replacemsg_text)``。

    1. ``server_id``:撤回行内容提取 ``newmsgid/sessionmsgid/svrid/
       oldmsgid`` → 同表 ``server_id`` 精查(``local_type NOT IN (10000,
       10002)``);
    2. ``heuristic``:撤回点前(``create_time <= 撤回行``)最近一条非本人、
       非系统行(``create_time DESC, sort_seq DESC, local_id DESC`` 三级序);
    3. ``replacemsg``:``<replacemsg>`` 文本兜底(original=None);
    4. ``none``:全空。

    busy → 该级如实按未命中回落;original 是**行 dict**(载荷化归调用方,
    含 recovery 字段),不在此处臆造。
    """
    built = _build_row_select(con, table)
    if built is not None:
        prefix, names = built
        keys = dict(zip(_ROW_KEYS, names))
        # —— 阶梯 1:server_id 直查 ——
        if keys.get("server_id") and keys.get("type"):
            for svrid in extract_revoke_server_ids(revoke_text):
                sql = (
                    f"{prefix}WHERE \"{keys['server_id']}\" = ? "
                    f"AND \"{keys['type']}\" NOT IN (?, ?) LIMIT 1"
                )
                try:
                    row = con.execute(sql, (svrid, _SYSTEM_TYPE, _REVOKE_TYPE)).fetchone()
                except sqlite3.OperationalError as exc:
                    if _is_busy_error(exc):
                        row = None
                    else:
                        raise
                if row is not None:
                    return _row_to_dict(row, names), "server_id", None
        # —— 阶梯 2:时间近邻启发式(撤回点前最近非本人非系统行)——
        if keys.get("time") and keys.get("type"):
            revoke_ts = _normalize_ts(revoke_row.get("time"))
            order_parts = [f"\"{keys['time']}\" DESC"]
            if keys.get("sort_seq"):
                order_parts.append(f"\"{keys['sort_seq']}\" DESC")
            if keys.get("local_id"):
                order_parts.append(f"\"{keys['local_id']}\" DESC")
            exclusions = ""
            params: list[Any] = [revoke_ts, _SYSTEM_TYPE, _REVOKE_TYPE]
            if self_name and keys.get("sender_id"):
                self_rowids = [
                    rid for rid, name in id_to_name.items() if name == self_name
                ]
                if self_rowids:
                    marks = ", ".join("?" for _ in self_rowids)
                    exclusions = f" AND \"{keys['sender_id']}\" NOT IN ({marks})"
                    params.extend(self_rowids)
            sql = (
                f"{prefix}WHERE \"{keys['time']}\" <= ? "
                f"AND \"{keys['type']}\" NOT IN (?, ?){exclusions} "
                f"ORDER BY {', '.join(order_parts)} LIMIT 1"
            )
            try:
                row = con.execute(sql, params).fetchone()
            except sqlite3.OperationalError as exc:
                if _is_busy_error(exc):
                    row = None
                else:
                    raise
            if row is not None:
                return _row_to_dict(row, names), "heuristic", None
    # —— 阶梯 3:replacemsg 文本兜底 ——
    replacemsg_text = extract_replacemsg_text(revoke_text)
    if replacemsg_text is not None:
        return None, "replacemsg", replacemsg_text
    # —— 阶梯 4:none ——
    return None, "none", None


# =====================================================================
# 会话基线层(R1.1)
# =====================================================================


def _read_session_rows(con: sqlite3.Connection) -> dict[str, dict[str, int]] | None:
    """SessionTable 单查 → ``{chat_id: {ts, unread, type?}}``。

    缺表/缺列 = 空表如实({});busy = None(调用方降级本轮跳过)。
    """
    columns = _columns(con, SESSION_TABLE)
    id_col = _pick(columns, _SESSION_ID_COLS)
    unread_col = _pick(columns, _SESSION_UNREAD_COLS)
    ts_col = _pick(columns, _SESSION_TS_COLS)
    type_col = _pick(columns, _SESSION_TYPE_COLS)
    if not (id_col and unread_col and ts_col):
        return {}
    select = [id_col, ts_col, unread_col]
    if type_col:
        select.append(type_col)
    quoted = ", ".join(f'"{c}"' for c in select)
    try:
        rows = con.execute(f'SELECT {quoted} FROM "{SESSION_TABLE}"').fetchall()
    except sqlite3.OperationalError as exc:
        if _is_busy_error(exc):
            return None
        raise _copy_query_error(SESSION_TABLE, exc)
    sessions: dict[str, dict[str, int]] = {}
    for row in rows:
        chat_id = row[0]
        if not isinstance(chat_id, str) or not chat_id.strip():
            continue
        entry = {"ts": _normalize_ts(row[1]), "unread": _to_int(row[2])}
        if type_col:
            entry["type"] = _to_int(row[3])
        sessions[chat_id.strip()] = entry
    return sessions


def _open_message_copies(copy_dir: Path) -> list[sqlite3.Connection]:
    """打开在场的消息域副本(≥1;全缺 = decrypt_failed,run_query 判例)。"""
    connections: list[sqlite3.Connection] = []
    for rel in _MESSAGE_DB_RELS:
        con = _open_copy(copy_dir, rel)
        if con is not None:
            connections.append(con)
    if not connections:
        raise BridgeError(
            DECRYPT_FAILED,
            "message 域解密副本不可用(副本缺失或损坏;G5 重建流程未产出可用库)",
            fix_hint="重跑 localdb notify-scan 触发副本重建;持续失败先核密钥与 sqlcipher",
        )
    return connections


def _display_map(copy_dir: Path, usernames: list[str]) -> dict[str, str]:
    """contact 域批量显示名(缺副本/查不出 = 空映射,回落原 id 不臆造)。"""
    con = _open_copy(copy_dir, "contact/contact.db")
    if con is None:
        return {}
    try:
        return _contact_pick_names(con, usernames)
    finally:
        con.close()


def _original_payload(
    original: dict[str, Any],
    recovery: str,
    id_to_name: dict[int, str],
    chat_id: str,
) -> dict[str, object]:
    """恢复行 → 载荷 ``original`` 节(sender_display 此处留 wxid,编排层
    统一回填显示名)。"""
    return {
        "server_id": _to_int(original.get("server_id")),
        "ts": _normalize_ts(original.get("time")),
        "sender_display": _sender_name(
            original.get("sender_id"), id_to_name, chat_id
        ),
        "content_preview": _type_preview(
            _to_int(original.get("type")), _decoded_text(original)
        ),
        "recovery": recovery,
    }


# =====================================================================
# R1.4 notify-scan 查询本体(纯函数:stdin 基线 → stdout 事件+新基线)
# =====================================================================


def run_notify_scan(
    *,
    copy_dir: Path,
    whitelist: list[str],
    baseline: dict[str, Any] | None,
    self_name: str | None = None,
    notify_self: bool = False,
    now: float | None = None,
    index_tables: bool = True,
) -> dict[str, object]:
    """两层扫描本体 → ``{"notify_scan": {events, baseline, stats}}``。

    桥零持久化(纯函数):基线推进只回传不落盘,持久化归主机;首轮
    (baseline 缺席/该会话无条目)= 只建基线零事件(初值 now)。busy =
    本轮跳过不判死(``stats.db_busy = true``,该会话基线原样回传不推进)。
    """
    started = time.monotonic()
    now_ts = int(time.time() if now is None else now)
    cleaned_whitelist = [
        item.strip() for item in whitelist
        if isinstance(item, str) and item.strip()
    ]
    old_baseline: dict[str, dict[str, int]] = {}
    for chat_id, entry in (baseline or {}).items():
        if not isinstance(chat_id, str) or not isinstance(entry, dict):
            continue
        old_baseline[chat_id] = {
            "ts": _to_int(entry.get("ts")),
            "unread": _to_int(entry.get("unread")),
        }

    stats: dict[str, object] = {
        "sessions_scanned": 0,
        "whitelist_sessions": len(cleaned_whitelist),
        "candidates": 0,
        "msg_rows_read": 0,
        "self_filtered": 0,
        "revoke_events": 0,
        "db_busy": False,
    }
    events: list[dict[str, object]] = []
    new_baseline: dict[str, dict[str, int]] = {}

    # —— R1.1 会话基线层:SessionTable 单查(便宜先筛)——
    session_con = _open_copy(copy_dir, "session/session.db")
    session_rows: dict[str, dict[str, int]] = {}
    if session_con is not None:
        try:
            try:
                read = _read_session_rows(session_con)
            except sqlite3.OperationalError as exc:  # 表发现/PRAGMA 面
                if not _is_busy_error(exc):
                    raise _copy_query_error(SESSION_TABLE, exc) from exc
                read = None
            if read is None:
                stats["db_busy"] = True
            else:
                session_rows = read
        finally:
            session_con.close()
    stats["sessions_scanned"] = len(session_rows)

    # 候选判定 + 推进后基线(白名单内每会话)。
    candidates: list[str] = []
    for chat_id in cleaned_whitelist:
        row = session_rows.get(chat_id)
        old = old_baseline.get(chat_id)
        if row is None:
            if old is not None:
                new_baseline[chat_id] = dict(old)  # 会话行缺:保旧值,零信号
            continue
        if old is None:
            # 首轮:初值 now(chatlog「初值 now」语义——若取 last_timestamp,
            # 下轮 lookback 会吞下装机前的整段历史,首弹轰炸)。
            new_baseline[chat_id] = {"ts": now_ts, "unread": row["unread"]}
            candidates.append(chat_id)
            continue
        new_baseline[chat_id] = {
            "ts": max(old["ts"], row["ts"]),
            "unread": row["unread"],
        }
        if (
            row["ts"] > old["ts"]
            or row["unread"] != old["unread"]
            or row.get("type") == _REVOKE_TYPE
        ):
            candidates.append(chat_id)
    stats["candidates"] = len(candidates)

    # 首轮候选只建基线(连 Msg_ 查询都不发);有基线候选才进定点层。
    scan_candidates = [chat for chat in candidates if chat in old_baseline]
    if scan_candidates:
        # —— R1.2 定点增量层(仅候选;非白名单零二次查询)——
        message_cons = _open_message_copies(copy_dir)
        sender_maps: dict[int, dict[int, str]] = {}  # id(con) → Name2Id 映射
        chat_tables: dict[str, tuple[sqlite3.Connection, str, dict[str, Any]]] = {}
        index_targets: list[tuple[str, str]] = []
        try:
            for chat_id in scan_candidates:
                for con in message_cons:
                    found = _chat_message_table(con, chat_id)
                    if found is None:
                        continue
                    table, colmap = found
                    chat_tables[chat_id] = (con, table, colmap)
                    time_col = colmap.get("time")
                    if isinstance(time_col, str):
                        index_targets.append((table, time_col))
                    break
            # 懒建索引(统一副本写政策单点;busy 放弃 = 走扫,拷问修正②)
            if index_tables and index_targets:
                ensure_ct_indexes(copy_dir, index_targets)
            for chat_id, (con, table, colmap) in chat_tables.items():
                if colmap.get("sender_id") and id(con) not in sender_maps:
                    sender_maps[id(con)] = name2id_maps(con)[0]
                rows = _fetch_recent_rows(
                    con,
                    table,
                    old_baseline[chat_id]["ts"] - LOOKBACK_SECONDS,
                    ROW_LIMIT,
                    talker=colmap.get("talker") if isinstance(colmap.get("talker"), str) else None,
                    chat_id=colmap.get("_chat_id") if isinstance(colmap.get("_chat_id"), str) else None,
                )
                if rows is None:
                    stats["db_busy"] = True
                    continue  # busy:本轮跳过该会话,水位不推进
                stats["msg_rows_read"] = int(stats["msg_rows_read"]) + len(rows)
                try:
                    _events_for_rows(
                        events, stats, chat_id, rows, con, table,
                        self_name, notify_self,
                        sender_maps.get(id(con), {}),
                    )
                except sqlite3.OperationalError as exc:
                    if _is_busy_error(exc):
                        stats["db_busy"] = True
                        continue
                    raise _copy_query_error(table, exc)
        finally:
            for con in message_cons:
                con.close()

        if stats["db_busy"]:
            # busy 轮:该会话基线回退旧值(下轮重开,lookback+锚去重消化重叠)。
            for chat_id in scan_candidates:
                new_baseline[chat_id] = dict(old_baseline[chat_id])

    # 显示名解析(编排层统一回填;解析不出回落原 id,不臆造)。
    displays = _display_map(
        copy_dir,
        cleaned_whitelist
        + [str(event.get("sender_display")) for event in events
           if isinstance(event.get("sender_display"), str)]
        + [str(event.get("revoker_display")) for event in events
           if isinstance(event.get("revoker_display"), str)],
    )
    for event in events:
        session_display = displays.get(str(event.get("session_id")))
        event["session_display"] = session_display or str(event.get("session_id"))
        for key in ("sender_display", "revoker_display"):
            value = event.get(key)
            if isinstance(value, str):
                event[key] = displays.get(value, value)
        original = event.get("original")
        if isinstance(original, dict):
            sender = original.get("sender_display")
            if isinstance(sender, str):
                original["sender_display"] = displays.get(sender, sender)

    stats["duration_ms"] = _duration_ms(started)
    return {"notify_scan": {
        "events": events, "baseline": new_baseline, "stats": stats,
    }}


def _events_for_rows(
    events: list[dict[str, object]],
    stats: dict[str, object],
    chat_id: str,
    rows: list[dict[str, Any]],
    con: sqlite3.Connection,
    table: str,
    self_name: str | None,
    notify_self: bool,
    id_to_name: dict[int, str],
) -> None:
    """候选会话的增量行 → 事件(时间 ASC 输出;撤回恢复+自过滤+双到达抑制)。

    抛 busy 的 OperationalError 归调用方降级(该会话本轮弃,不判死)。
    """
    pending_new: list[dict[str, object]] = []
    recovered_server_ids: set[int] = set()
    for row in reversed(rows):  # SQL DESC → 输出 ASC(时间正序)
        local_type = _to_int(row.get("type"))
        text = _decoded_text(row)
        sender = _sender_name(row.get("sender_id"), id_to_name, chat_id)
        ts = _normalize_ts(row.get("time"))
        server_id = _to_int(row.get("server_id"))
        if is_revoke_row(local_type, text):
            if (
                _SELF_REVOKE_MARKER in text
                or (self_name is not None and sender == self_name)
            ):
                stats["self_filtered"] = int(stats["self_filtered"]) + 1
                continue
            original, recovery, replacemsg_text = _recover_original(
                con, table, row, text, self_name, id_to_name
            )
            original_payload: dict[str, object] | None = None
            if original is not None:
                original_payload = _original_payload(
                    original, recovery, id_to_name, chat_id
                )
                recovered_sid = int(original_payload["server_id"])
                if recovered_sid:
                    recovered_server_ids.add(recovered_sid)
            events.append({
                "event": "message.revoke",
                "session_id": chat_id,
                "session_display": chat_id,  # 显示名在编排层统一回填
                "revoker_display": sender,
                "is_self_revoke": False,
                "ts": ts,
                "server_id": server_id,
                "local_type": local_type,
                "original": original_payload,
                "replacemsg_text": replacemsg_text,
            })
            stats["revoke_events"] = int(stats["revoke_events"]) + 1
            continue
        if local_type == _SYSTEM_TYPE:
            continue  # 系统行非撤回:不通知不计错(红包/拍一拍等)
        is_self = self_name is not None and sender == self_name
        if is_self and not notify_self:
            stats["self_filtered"] = int(stats["self_filtered"]) + 1
            continue
        pending_new.append({
            "event": "message.new",
            "session_id": chat_id,
            "session_display": chat_id,
            "sender_display": sender,
            "is_self": is_self,
            "content_preview": _type_preview(local_type, text),
            "ts": ts,
            "server_id": server_id,
            "local_type": local_type,
        })
    # 同撤回双到达抑制:同轮恢复出的原消息不再另发新消息事件。
    for entry in pending_new:
        if int(entry.get("server_id") or 0) in recovered_server_ids:
            continue
        events.append(entry)


# =====================================================================
# R1.5 revoke-list 查询本体(同一阶梯,历史窗全量)
# =====================================================================


def run_revoke_list(
    *,
    copy_dir: Path,
    chat_id: str,
    since_days: int,
    self_name: str | None = None,
    now: float | None = None,
    index_tables: bool = True,
) -> dict[str, object]:
    """撤回历史查询 → ``{"revoke_list": [...], "stats": {...}}``。

    对该会话全部 Msg_ 表(两库)扫撤回谓词行(SQL 层窗口+标记过滤)+
    R1.3 同一恢复阶梯;自撤回跳过并计数;busy = 该库跳过不判死。
    """
    started = time.monotonic()
    now_ts = int(time.time() if now is None else now)
    since_ts = now_ts - since_days * 86400
    stats: dict[str, object] = {
        "chat_id": chat_id,
        "since_days": since_days,
        "tables_scanned": 0,
        "revoke_rows": 0,
        "self_revoked": 0,
        "recovery": {"server_id": 0, "heuristic": 0, "replacemsg": 0, "none": 0},
        "db_busy": False,
        "duration_ms": 0,
    }
    revoke_list: list[dict[str, object]] = []
    message_cons = _open_message_copies(copy_dir)
    index_targets: list[tuple[str, str]] = []
    chat_tables: list[tuple[sqlite3.Connection, str]] = []
    try:
        for con in message_cons:
            found = _chat_message_table(con, chat_id)
            if found is None:
                continue
            table, colmap = found
            time_col = colmap.get("time")
            if isinstance(time_col, str):
                index_targets.append((table, time_col))
            chat_tables.append((con, table))
        if index_tables and index_targets:
            ensure_ct_indexes(copy_dir, index_targets)
        for con, table in chat_tables:
            sender_names: dict[int, str] = name2id_maps(con)[0]
            built = _build_row_select(con, table)
            if built is None:
                continue
            prefix, names = built
            keys = dict(zip(_ROW_KEYS, names))
            stats["tables_scanned"] = int(stats["tables_scanned"]) + 1
            conditions = [f"\"{keys['time']}\" >= ?"]
            params: list[Any] = [since_ts]
            if keys.get("type") and keys.get("content"):
                like = " OR ".join(
                    f"CAST(\"{keys['content']}\" AS TEXT) LIKE ?"
                    for _ in REVOKE_MARKERS
                )
                conditions.append(
                    f"(\"{keys['type']}\" = ? OR "
                    f"(\"{keys['type']}\" = ? AND ({like})))"
                )
                params.extend(
                    [_REVOKE_TYPE, _SYSTEM_TYPE, *(f"%{m}%" for m in REVOKE_MARKERS)]
                )
            sql = (
                f"{prefix}WHERE {' AND '.join(conditions)} "
                f"ORDER BY \"{keys['time']}\" ASC"
            )
            try:
                rows = con.execute(sql, params).fetchall()
            except sqlite3.OperationalError as exc:
                if _is_busy_error(exc):
                    stats["db_busy"] = True
                    continue
                raise _copy_query_error(table, exc)
            for row in rows:
                item = _row_to_dict(row, names)
                text = _decoded_text(item)
                sender = _sender_name(item.get("sender_id"), sender_names, chat_id)
                stats["revoke_rows"] = int(stats["revoke_rows"]) + 1
                if (
                    _SELF_REVOKE_MARKER in text
                    or (self_name is not None and sender == self_name)
                ):
                    stats["self_revoked"] = int(stats["self_revoked"]) + 1
                    continue
                original, recovery, replacemsg_text = _recover_original(
                    con, table, item, text, self_name, sender_names
                )
                original_payload = None
                if original is not None:
                    original_payload = _original_payload(
                        original, recovery, sender_names, chat_id
                    )
                recovery_counts = stats["recovery"]
                recovery_counts[recovery] = int(recovery_counts[recovery]) + 1  # type: ignore[index]
                revoke_list.append({
                    "event": "message.revoke",
                    "session_id": chat_id,
                    "session_display": chat_id,
                    "revoker_display": sender,
                    "is_self_revoke": False,
                    "ts": _normalize_ts(item.get("time")),
                    "server_id": _to_int(item.get("server_id")),
                    "local_type": _to_int(item.get("type")),
                    "original": original_payload,
                    "replacemsg_text": replacemsg_text,
                })
    finally:
        for con in message_cons:
            con.close()

    displays = _display_map(
        copy_dir,
        [chat_id]
        + [str(entry.get("revoker_display")) for entry in revoke_list
           if isinstance(entry.get("revoker_display"), str)],
    )
    chat_display = displays.get(chat_id) or chat_id
    for entry in revoke_list:
        entry["session_display"] = chat_display
        revoker = entry.get("revoker_display")
        if isinstance(revoker, str):
            entry["revoker_display"] = displays.get(revoker, revoker)
        original = entry.get("original")
        if isinstance(original, dict):
            sender = original.get("sender_display")
            if isinstance(sender, str):
                original["sender_display"] = displays.get(sender, sender)

    stats["duration_ms"] = _duration_ms(started)
    return {"revoke_list": revoke_list, "stats": stats}


# =====================================================================
# stdin 载荷契约(R1.4:argv 零内容,私有数据走 stdin)
# =====================================================================


def read_scan_payload(text: str) -> dict[str, Any]:
    """stdin JSON → ``{"whitelist", "baseline", "notify_self"}``。

    形状纪律(usage 拒,fail-fast):空 stdin / 非 JSON / 非 dict /
    ``whitelist`` 缺席或非非空字符串清单 / ``baseline`` 非 dict/null /
    ``notify_self`` 非布尔。基线条目形状宽松(脏条目由扫描层弃置——
    主机侧回写的值是本桥上轮产物,不设双重严卡)。
    """
    if not text.strip():
        raise BridgeError(
            EXIT_USAGE,
            "notify-scan stdin 无内容(载荷经 --file - 传入,argv 零内容)",
            code="usage",
            fix_hint='stdin 传 JSON 载荷:{"whitelist": [会话 id], "baseline": {...} 或 null}',
        )
    try:
        payload = json.loads(text)
    except ValueError as exc:
        raise BridgeError(
            EXIT_USAGE,
            f"notify-scan stdin 载荷不是合法 JSON:{type(exc).__name__}",
            code="usage",
            fix_hint='载荷形状:{"whitelist": [会话 id], "baseline": {...} 或 null, "notify_self": false}',
        ) from exc
    if not isinstance(payload, dict):
        raise BridgeError(
            EXIT_USAGE,
            f"notify-scan stdin 载荷须为 JSON 对象,当前为 {type(payload).__name__}",
            code="usage",
        )
    whitelist = payload.get("whitelist")
    if (
        not isinstance(whitelist, list)
        or not whitelist
        or any(
            isinstance(item, bool) or not isinstance(item, str) or not item.strip()
            for item in whitelist
        )
    ):
        raise BridgeError(
            EXIT_USAGE,
            "notify-scan 载荷 whitelist 须为非空字符串清单(会话 id;空清单 = 功能空转,"
            "主机侧引擎在构造期即拒)",
            code="usage",
        )
    baseline = payload.get("baseline")
    if baseline is not None and not isinstance(baseline, dict):
        raise BridgeError(
            EXIT_USAGE,
            f"notify-scan 载荷 baseline 须为对象或 null,当前为 {type(baseline).__name__}",
            code="usage",
        )
    notify_self = payload.get("notify_self", False)
    if not isinstance(notify_self, bool):
        raise BridgeError(
            EXIT_USAGE,
            "notify-scan 载荷 notify_self 须为布尔(缺省 false:自己发的消息不通知),"
            f"当前为 {notify_self!r}",
            code="usage",
        )
    return {
        "whitelist": [item.strip() for item in whitelist],
        "baseline": baseline if isinstance(baseline, dict) else {},
        "notify_self": notify_self,
    }


# =====================================================================
# 编排(R2:照 query_history 模式;resolve/ensure 归 CLI 分支前置)
# =====================================================================


def _ensure_and_heal(
    config, db_storage: Path, keys: dict[str, str], domains: list[str],
    *, data_root: Path | None, now: float | None,
) -> dict[str, object]:
    """E2 副本 + 解密失败自愈钩子(query_history 同款逻辑,独立副本零
    共享文件改动)。"""
    from . import localdb, memsearch

    def _ensure(keys_mapping: dict[str, str]) -> dict[str, object]:
        return localdb.ensure_decrypted_copies(
            db_storage,
            keys_mapping,
            domains=domains,
            ttl_hours=config.copy_ttl_hours,
            capacity_mb=config.copy_capacity_mb,
            data_root=data_root,
            now=now,
        )

    try:
        return _ensure(keys)
    except BridgeError as exc:
        if exc.exit_code != DECRYPT_FAILED:
            raise
        if not memsearch.self_heal_armed(config=config, data_root=data_root):
            raise
        healed = memsearch.try_self_heal(db_storage, config=config, data_root=data_root)
        if healed is None:
            raise
        return _ensure(healed)


def notify_scan(
    config,  # BridgeConfig(鸭子类型;避免循环导入)
    db_storage: Path,
    keys: dict[str, str],
    payload: dict[str, Any],
    *,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """``localdb notify-scan`` 全链编排:ensure(message/session/contact)
    → 副本侧懒建索引 → R1.1/R1.2/R1.3 扫描本体。

    密钥链(resolve_keys)归 CLI 分支前置(与 query 同一全链;
    key_unavailable 照旧 exit 21,主机侧结构化 skip)。
    """
    copy_info = _ensure_and_heal(
        config, db_storage, keys, ["message", "session", "contact"],
        data_root=data_root, now=now,
    )
    return run_notify_scan(
        copy_dir=Path(str(copy_info["dir"])),
        whitelist=payload["whitelist"],
        baseline=payload.get("baseline"),
        self_name=login_wxid(db_storage),
        notify_self=bool(payload.get("notify_self", False)),
        now=now,
    )


def revoke_list(
    config,
    db_storage: Path,
    keys: dict[str, str],
    chat_id: str,
    days: int,
    *,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """``localdb revoke-list`` 全链编排:ensure(message/contact)→ R1.5
    撤回谓词全窗扫描(与 notify-scan 两壳共享 R1.3 同一阶梯实现)。"""
    copy_info = _ensure_and_heal(
        config, db_storage, keys, ["message", "contact"],
        data_root=data_root, now=now,
    )
    return run_revoke_list(
        copy_dir=Path(str(copy_info["dir"])),
        chat_id=chat_id,
        since_days=days,
        self_name=login_wxid(db_storage),
        now=now,
    )
