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
import time
import xml.etree.ElementTree as ET
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
    "query_messages_range",
    "lookup_contact",
    "group_info",
    "humanize_content",
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
    # —— R3 类型映射扩展(task 10-14-wechat-chat-export;真库普查实证,
    #    证据逐条在 census 基件 tests/wechat-bridge/fixtures/
    #    local_type_census.json mapping 节;大数 = (appmsg子型<<32)|49)——
    42: "card",             # 名片(WeFlow 42;真库抽样 root=msg 空子节点)
    50: "call",             # 音视频通话(真库抽样 root=voipmsg)
    21474836529: "link",    # 链接卡(5<<32|49;appmsg<type>=5 + url)
    25769803825: "file",    # 文件(6<<32|49;WeFlow file 变体)
    34359738417: "file",    # 文件(8<<32|49;WeFlow file 变体)
    103079215153: "file",   # 文件(24<<32|49;WeFlow file 变体)
    81604378673: "record",  # 合并转发(19<<32|49;title=群聊的聊天记录)
    244813135921: "quote",  # 引用(57<<32|49;refermsg 在场)
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

# —— R3 人话化(task 10-14-wechat-chat-export;prd R3 定稿落位本模块,
#    localdb_page 的模块级 try-import 自动接管共享版,消费方零改)——
#: type-49 族编码底数(hi32<<32|49;census _meta 注记)。
_APPMSG_SHIFT = 32
#: 群消息 type-49/47 XML 的 ``wxid:\n`` 前缀上限(4.1.15 真库实测)。
_GROUP_XML_PREFIX_MAX = 128


def _is_appmsg_local_type(local_type: int) -> bool:
    """type-49 族判定(含大数变体;非 49 编码的大数不成族)。"""
    if local_type == 49:
        return True
    if local_type < 1 << 62 and local_type > 1 << _APPMSG_SHIFT:
        return (local_type - 49) % (1 << _APPMSG_SHIFT) == 0
    return False


def _appmsg_subtype(local_type: int) -> int | None:
    """type-49 族的 appmsg 语义位(hi32;与 ``<appmsg><type>`` 子节点同值)。"""
    if local_type == 49:
        return None  # 纯 49 无语义位,以 XML 内 <type> 为准
    if not _is_appmsg_local_type(local_type):
        return None
    return (local_type - 49) >> _APPMSG_SHIFT


def _humanize_size(num_bytes: Any) -> str:
    """字节数 → 人话(B/KB/MB/GB;坏值原样字符串,不臆造)。"""
    try:
        size = int(num_bytes)
    except (TypeError, ValueError):
        return str(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size}{unit}" if unit == "B" else f"{size:.1f}{unit}"
        size = round(size / 1024, 1)
    return f"{size}TB"  # pragma: no cover - 循环末态兜底


def _strip_group_prefix(text: str) -> str:
    """剥离群消息 XML 的 ``wxid:\n`` 前缀(仅当后跟 '<' 才剥,正文不误伤)。"""
    head, sep, rest = text.partition(":\n")
    if sep and len(head) <= _GROUP_XML_PREFIX_MAX and rest.lstrip().startswith("<"):
        return rest.lstrip()
    return text


def _parse_xml_content(content: str) -> ET.Element | None:
    """内容 → XML 根节点(两段:直解 → 剥群前缀再解;坏 XML = None)。"""
    cleaned = content.strip().strip("\x00").strip()
    try:
        return ET.fromstring(cleaned)
    except ET.ParseError:
        pass
    try:
        return ET.fromstring(_strip_group_prefix(cleaned))
    except ET.ParseError:
        return None


def _humanize_appmsg(local_type: int, appmsg: ET.Element) -> str | None:
    """``<appmsg>`` 节点 → 人话(链接/引用/合并转发/文件四形,prd R3 文案)。

    语义位取 ``<appmsg><type>`` 子节点(真库实测在场),缺位回落 local_type
    的 hi32(同一语义,census _meta 注记)。缺节点/空文案 = None(调用方落
    占位 + 计数,如实降级)。
    """
    try:
        subtype = int((appmsg.findtext("type") or "").strip())
    except ValueError:
        subtype = _appmsg_subtype(local_type)
        subtype = -1 if subtype is None else subtype
    title = (appmsg.findtext("title") or "").strip()
    if subtype == 5:  # 链接卡
        description = (appmsg.findtext("description") or "").strip()
        url = (appmsg.findtext("url") or "").strip()
        parts = [p for p in (title, description, url) if p]
        return f"【链接】{' '.join(parts)}" if parts else None
    if subtype == 57:  # 引用
        refer = appmsg.find(".//refermsg")
        summary = ((refer.findtext("content") if refer is not None else "") or "")
        summary = summary.strip().replace("\n", " ")[:50]
        if title and summary:
            return f"{title}(引用:{summary})"
        return title or None
    if subtype == 19:  # 合并转发(4.1.15 真库抽样无 recordinfo,如实降级)
        datalist = appmsg.find(".//datalist")
        count = (datalist.get("count") if datalist is not None else "") or ""
        display = (appmsg.findtext(".//displayname") or "").strip() or title
        if display and count.isdigit():
            return f"【聊天记录】{display} 的 {int(count)} 条消息"
        return f"【聊天记录】{display}" if display else None
    if subtype == 6:  # 文件
        if not title:
            return None
        raw_size = appmsg.findtext(".//totallen")
        size_text = _humanize_size(raw_size) if raw_size not in (None, "") else ""
        return f"【文件】{title}({size_text})" if size_text else f"【文件】{title}"
    return None  # 其余 appmsg 子型(转账/红包/拍一拍…)不臆造文案


def humanize_content(
    local_type: int, content: Any, stats: dict[str, object] | None = None
) -> str | None:
    """type-49 族 / 47 XML → 人话(str;None = 解不出,调用方落占位+计数)。

    prd R3 定稿的共享实现(参考实现 = localdb_page._humanize_impl,契约同一;
    stdlib xml.etree 解析):type-49 XML 四形【链接】/引用/【聊天记录】/
    【文件】+ 47 emoji description;群消息 ``wxid:\\n`` 前缀剥离;坏 XML =
    None + ``wx_parse_failed`` 计数(stats 透传应答附加键)。
    """
    if not isinstance(content, str) or not content.strip():
        return None
    root = _parse_xml_content(content)
    if root is None:
        if stats is not None:
            stats["wx_parse_failed"] = int(stats.get("wx_parse_failed", 0)) + 1
        return None
    if local_type == 47:  # 表情:emoji XML 的 description 属性
        emoji = root if root.tag == "emoji" else root.find(".//emoji")
        desc = (emoji.get("description") if emoji is not None else "") or ""
        return desc.strip() or None
    if _is_appmsg_local_type(local_type):
        appmsg = root.find(".//appmsg")
        if appmsg is not None:
            text = _humanize_appmsg(local_type, appmsg)
            if text is not None:
                return text
    if stats is not None:
        stats["wx_parse_failed"] = int(stats.get("wx_parse_failed", 0)) + 1
    return None


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


def query_messages_range(
    con: Any,
    chat_id: str,
    since_ts: int,
    end_ts: int | None = None,
    *,
    limit: int = 500,
    offset: int = 0,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """水位增量查询(R5 ChatLab Pull;task 10-14-wechat-http-api PRD 终位
    = 本模块纯加法平移;httpapi 与 watermark 消费同一函数,不得另写一份)。

    - 选表按 :func:`find_message_tables` 同一自适应机制(宽表 talker 过滤
      /分表 Name2Id md5 反解);``create_time > since``(且 ``<= end`` 若给)
      **升序** + ``LIMIT limit OFFSET offset``;
    - ``watermark`` = 该会话表当前 ``max(create_time)``(单会话表内聚合,
      代价=单会话规模,不扫全库);
    - sync 块:取满 ``limit`` → ``hasMore=true, nextOffset=offset+limit,
      nextSince=since``(翻页期 since 不动);未取满 → ``hasMore=false,
      nextOffset=0, nextSince=max(watermark, since)``(拉毕跳水位;max 防御
      表 max 早于 since 时的游标回退)。多表命中时页语义按表独立后归并
      截断(现实=单会话单表;宽表形态的边缘并流如实注记)。

    既有 :func:`query_messages` 零改动(纯加法)。行形状与其同源:
    ``{"ts","sender","type","text"?,"media_placeholder"?}``。
    """
    tables = find_message_tables(con)
    id_to_name: dict[int, str] = {}
    if any(colmap.get("sender_id") for _table, colmap in tables):
        id_to_name = name2id_maps(con)[0]
    messages: list[dict[str, Any]] = []
    watermark_value = int(since_ts)
    for table, colmap in tables:
        if colmap.get("talker"):
            chat_condition = (f'"{colmap["talker"]}" = ?', [chat_id])
        elif colmap.get("chat") == chat_id:
            chat_condition = None
        else:
            continue
        cols: list[str] = []
        idx: dict[str, int] = {}
        for key, col in (
            ("time", colmap.get("time")),
            ("content", colmap.get("content")),
            ("type", colmap.get("type")),
            ("sender", colmap.get("sender")),
            ("sender_id", colmap.get("sender_id")),
            ("ct_content", colmap.get("ct_content")),
        ):
            if col:
                idx[key] = len(cols)
                cols.append(col)
        quoted = ", ".join(chr(34) + c + chr(34) for c in cols)
        conditions: list[str] = []
        params: list[Any] = []
        if chat_condition is not None:
            conditions.append(chat_condition[0])
            params.extend(chat_condition[1])
        conditions.append(f'"{colmap["time"]}" > ?')
        params.append(int(since_ts))
        if end_ts is not None:
            conditions.append(f'"{colmap["time"]}" <= ?')
            params.append(int(end_ts))
        sql = (
            f'SELECT {quoted} FROM "{table}" WHERE {" AND ".join(conditions)} '
            f'ORDER BY "{colmap["time"]}" ASC LIMIT ? OFFSET ?'
        )
        params.extend([int(limit), int(offset)])
        max_sql = f'SELECT MAX("{colmap["time"]}") FROM "{table}"'
        max_params: list[Any] = []
        if chat_condition is not None:
            max_sql += f" WHERE {chat_condition[0]}"
            max_params.extend(chat_condition[1])
        try:
            rows = con.execute(sql, params).fetchall()
            row_max = con.execute(max_sql, max_params).fetchone()
        except Exception:  # noqa: BLE001 - 单表漂移不拖垮整查询(红线 7)
            continue
        if row_max and row_max[0] is not None:
            watermark_value = max(watermark_value, _normalize_ts(row_max[0]))
        for row in rows:
            ts = _normalize_ts(row[idx["time"]])
            content = row[idx["content"]] if "content" in idx else None
            msg_type = 1
            if "type" in idx:
                try:
                    msg_type = int(row[idx["type"]] or 0)
                except (TypeError, ValueError):
                    msg_type = 0
            if "sender" in idx:
                sender = "me" if row[idx["sender"]] == 1 else chat_id
            elif "sender_id" in idx:
                sender = _sender_name(row[idx["sender_id"]], id_to_name, chat_id)
            else:
                sender = chat_id
            entry: dict[str, Any] = {
                "ts": ts,
                "sender": sender,
                "type": MSG_TYPE_NAMES.get(msg_type, f"type_{msg_type}"),
            }
            if msg_type == 1:
                text, placeholder = _decode_text_content(
                    content,
                    row[idx["ct_content"]] if "ct_content" in idx else None,
                    None,
                )
                if text is not None:
                    entry["text"] = text
                else:
                    entry["media_placeholder"] = placeholder
            else:
                entry["media_placeholder"] = "非文本消息,内容未导出(占位)"
            messages.append(entry)
    messages.sort(key=lambda item: int(item["ts"]))
    messages = messages[: int(limit)]
    has_more = len(messages) >= int(limit)
    sync = {
        "hasMore": has_more,
        "nextSince": int(since_ts) if has_more else watermark_value,
        "nextOffset": int(offset) + int(limit) if has_more else 0,
        "watermark": watermark_value,
    }
    return messages, sync


def lookup_contact(con: sqlite3.Connection, chat_id: str) -> str | None:
    """contact 域:会话 id → 展示名(remark > nickname > alias;best-effort)。"""
    return _contact_pick_names(con, [chat_id]).get(chat_id)


def _contact_pick_names(
    con: sqlite3.Connection, user_names: list[str]
) -> dict[str, str]:
    """contact 域批量:username → 展示名(remark > nickname > alias;0.5.1)。

    群消息发送者上屏要名字不要裸 wxid(主人令 2026-10-13「要展示名字」):
    逐批 IN 查询同表发现逻辑与 :func:`lookup_contact` 同族;查不到的
    username 不入映射(调用方回落原样,陌生群成员如实保留 wxid)。
    """
    wanted = [u for u in dict.fromkeys(user_names) if isinstance(u, str) and u]
    if not wanted:
        return {}
    name_cols = ("remark", "Remark", "conRemark", "nick_name", "nickname", "nickName", "NickName", "alias")
    id_cols = ("username", "userName", "UserName", "user_name")
    try:
        tables = [
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    except sqlite3.Error:
        return {}
    result: dict[str, str] = {}
    for table in tables:
        if "contact" not in table.lower():
            continue
        columns = _columns(con, table)
        id_col = _pick(columns, id_cols)
        if id_col is None:
            continue
        name_actual = [
            next((c for c in columns if c.lower() == nc.lower()), None)
            for nc in name_cols
        ]
        selectable = [a for a in name_actual if a is not None]
        if not selectable:
            continue
        quoted_id = chr(34) + id_col + chr(34)
        quoted_names = ", ".join(chr(34) + a + chr(34) for a in selectable)
        marks = ", ".join("?" for _ in wanted)
        try:
            rows = con.execute(
                f"SELECT {quoted_id}, {quoted_names} FROM \"{table}\" "
                f"WHERE {quoted_id} IN ({marks})",
                wanted,
            ).fetchall()
        except sqlite3.Error:
            continue
        for row in rows:
            username = row[0]
            if not isinstance(username, str):
                continue
            display = next(
                (v for v in row[1:] if isinstance(v, str) and v.strip()), None
            )
            if display:
                result[username] = display
        if result:
            break
    return result


def _contact_pick_remarks(
    con: sqlite3.Connection, user_names: list[str]
) -> dict[str, str]:
    """contact 域批量:username → 备注原样(remark;无备注不入映射;0.6.0)。

    群信息面板「备注」列的直源:显示名经 :func:`_contact_pick_names` 的
    remark>nickname>alias 优先序已含备注优先,但契约 v1 要求显示名与备注
    两列分立——备注缺席(昵称上屏)= None 如实,不拿显示名冒充备注。
    表发现逻辑与 :func:`_contact_pick_names` 同族(首个有命中的 contact 系
    表胜)。
    """
    wanted = [u for u in dict.fromkeys(user_names) if isinstance(u, str) and u]
    if not wanted:
        return {}
    remark_cols = ("remark", "Remark", "conRemark")
    id_cols = ("username", "userName", "UserName", "user_name")
    try:
        tables = [
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        ]
    except sqlite3.Error:
        return {}
    result: dict[str, str] = {}
    for table in tables:
        if "contact" not in table.lower():
            continue
        columns = _columns(con, table)
        id_col = _pick(columns, id_cols)
        if id_col is None:
            continue
        remark_actual = [
            next((c for c in columns if c.lower() == rc.lower()), None)
            for rc in remark_cols
        ]
        selectable = [a for a in remark_actual if a is not None]
        if not selectable:
            continue
        quoted_id = chr(34) + id_col + chr(34)
        quoted_remarks = ", ".join(chr(34) + a + chr(34) for a in selectable)
        marks = ", ".join("?" for _ in wanted)
        try:
            rows = con.execute(
                f"SELECT {quoted_id}, {quoted_remarks} FROM \"{table}\" "
                f"WHERE {quoted_id} IN ({marks})",
                wanted,
            ).fetchall()
        except sqlite3.Error:
            continue
        for row in rows:
            username = row[0]
            if not isinstance(username, str):
                continue
            remark = next(
                (v for v in row[1:] if isinstance(v, str) and v.strip()), None
            )
            if remark:
                result[username] = remark
        if result:
            break
    return result


def _apply_sender_display(
    messages: list[dict[str, object]], display_map: dict[str, str]
) -> None:
    """发送者上屏名替换(0.5.1,原地):sender→展示名+sender_id 留原 id+
    群消息文本前缀 ``<wxid>:\\n`` 同步换名(引擎标题/预览取首行,首行带名
    则 feed 行自然读作「名字: 内容」)。"""
    for entry in messages:
        sender = entry.get("sender")
        if not isinstance(sender, str) or sender not in display_map:
            continue
        display = display_map[sender]
        text = entry.get("text")
        prefix = sender + ":"
        if isinstance(text, str) and text.startswith(prefix):
            entry["text"] = display + ":" + text[len(prefix):]
        entry["sender"] = display
        entry["sender_id"] = sender


# =====================================================================
# E3 群信息只读查询(task 10-13-wechat-groupinfo;应答契约 v1 逐字段)
# =====================================================================

#: 群信息表名(2026-10-13 contact.db 实锚直查;缺表 = 对应键 null/空表如实
#: 降级,不搞发现式查询——判例同 sns_query 的直查纪律)。
_CHAT_ROOM_TABLE = "chat_room"
_CHAT_ROOM_INFO_TABLE = "chat_room_info_detail"
_CHATROOM_MEMBER_TABLE = "chatroom_member"


def _format_wall_ts(value: Any) -> str | None:
    """秒级时间戳 → 人话上屏形态(本地时 ``YYYY-MM-DD HH:MM:SS``)。

    0/负/形状异常 = None(「未发布」不是 1970;如实缺省,不臆造);
    毫秒值经 :func:`_normalize_ts` 启发式归一(与消息时间列同一纪律)。
    """
    ts = _normalize_ts(value)
    if ts <= 0:
        return None
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def _json_safe_status(status: Any) -> Any:
    """群状态串化守卫(v1 原样透传不臆造语义,但 stdout 是 JSON)。

    列值若为 BLOB(bytes/json.dump 无 default 会 TypeError 崩出非契约
    退出码),转 hex 串保真进出(零失真、可逆);其余标量(int/str/None)
    原样。"""
    if isinstance(status, (bytes, bytearray, memoryview)):
        return bytes(status).hex()
    return status


def _chat_room_row(
    con: sqlite3.Connection, chat_id: str
) -> tuple[Any, Any] | None:
    """contact 库 ``chat_room(username, owner)`` → ``(id, owner)``。

    群主 wxid 直源;``id`` 供 ``chatroom_member.room_id`` 关联。缺表/缺列/
    缺行 = None 如实(降级,不判错)。
    """
    columns = _columns(con, _CHAT_ROOM_TABLE)
    if not (_pick(columns, ("id",)) and _pick(columns, ("username",)) and _pick(columns, ("owner",))):
        return None
    try:
        row = con.execute(
            f'SELECT id, owner FROM "{_CHAT_ROOM_TABLE}" WHERE username = ?',
            (chat_id,),
        ).fetchone()
    except sqlite3.Error:
        return None
    return (row[0], row[1]) if row is not None else None


def _chatroom_member_ids(con: sqlite3.Connection, room_id: Any) -> list[int]:
    """contact 库 ``chatroom_member(room_id, member_id)`` → 成员 id 清单。

    **member_id = contact 表 rowid**(2026-10-13 实测对拍裁决,见
    :func:`_contact_rowid_usernames` 注);形状异常的行跳过(宁缺毋假)。
    缺表/缺列 = 空清单如实。
    """
    columns = _columns(con, _CHATROOM_MEMBER_TABLE)
    if not (_pick(columns, ("room_id",)) and _pick(columns, ("member_id",))):
        return []
    try:
        rows = con.execute(
            f'SELECT member_id FROM "{_CHATROOM_MEMBER_TABLE}" WHERE room_id = ?',
            (room_id,),
        ).fetchall()
    except sqlite3.Error:
        return []
    ids: list[int] = []
    for (member_id,) in rows:
        try:
            ids.append(int(member_id))
        except (TypeError, ValueError):
            continue
    return ids


def _contact_rowid_usernames(
    con: sqlite3.Connection, rowids: list[int]
) -> dict[int, str]:
    """contact 库 rowid → username 批量反查(``chatroom_member.member_id``
    的真源映射,0.6.0)。

    **裁决注记(2026-10-13,500 人群实拍)**:member_id 曾被预设为 message
    库 Name2Id rowid(real_sender_id 同款语义),真数据证伪——TMS 群
    (50438708676@chatroom,500 成员)按 contact.rowid 解释 500/500 可解且
    500/500 命中 ``chat_room.ext_buffer`` 可读名单锚、群主 wxid 的 contact
    rowid 恰在成员表;按 Name2Id 解释仅 16/500 命中(行号空间重叠的巧合
    错配,会张冠李戴真群成员)。故成员反查走 contact.rowid 直查,不碰
    Name2Id。缺行(退群成员残留/联系人被删)= 不入映射,调用方弃行如实。
    """
    wanted = list(dict.fromkeys(rowids))
    if not wanted:
        return {}
    marks = ", ".join("?" for _ in wanted)
    try:
        rows = con.execute(
            f'SELECT rowid, username FROM "contact" WHERE rowid IN ({marks})',
            wanted,
        ).fetchall()
    except sqlite3.Error:
        return {}
    return {
        int(rowid): username
        for rowid, username in rows
        if isinstance(username, str) and username
    }


def _chat_room_settings(
    con: sqlite3.Connection,
    chat_id: str,
    display_map: dict[str, str],
) -> tuple[dict[str, object] | None, object]:
    """contact 库 ``chat_room_info_detail`` → (公告节, 群状态原样)。

    公告节 = ``{"text","editor_display","published_at"}``:文本空串 = None;
    编辑人 wxid 经 display_map 反解(查不到回落原样,0.5.1 同款);发布
    时间 0 = 未发布 = None。**chat_room_status_ 原样透传不臆造语义**
    (实测域含 0 与 524288 等,词面归 UI 线;BLOB 列值经
    :func:`_json_safe_status` hex 串化保 JSON 契约);缺表/缺列/缺行 =
    (None, None)。
    """
    needed = (
        "username_",
        "announcement_",
        "announcement_editor_",
        "announcement_publish_time_",
        "chat_room_status_",
    )
    columns = _columns(con, _CHAT_ROOM_INFO_TABLE)
    if not all(_pick(columns, (c,)) for c in needed):
        return None, None
    try:
        row = con.execute(
            f'SELECT announcement_, announcement_editor_, '
            f'announcement_publish_time_, chat_room_status_ '
            f'FROM "{_CHAT_ROOM_INFO_TABLE}" WHERE username_ = ?',
            (chat_id,),
        ).fetchone()
    except sqlite3.Error:
        return None, None
    if row is None:
        return None, None
    announcement_raw, editor_raw, published_raw, status_raw = row
    text = (
        announcement_raw
        if isinstance(announcement_raw, str) and announcement_raw.strip()
        else None
    )
    editor_display: str | None = None
    if isinstance(editor_raw, str) and editor_raw:
        editor_display = display_map.get(editor_raw, editor_raw)
    announcement: dict[str, object] = {
        "text": text,
        "editor_display": editor_display,
        "published_at": _format_wall_ts(published_raw),
    }
    return announcement, status_raw


def group_info(copy_dir: Path, chat_id: str) -> dict[str, object]:
    """E3 群信息只读查询(task 10-13-wechat-groupinfo;应答契约 v1 逐字段)。

    数据源(2026-10-13 解密副本实锚,**单 contact 域自足**,全部复用既有件):
    群显示名 = :func:`lookup_contact`;群主 = ``chat_room(username, owner)``;
    公告/编辑人/发布时间/状态 = ``chat_room_info_detail(username_, …)``;
    成员 = ``chatroom_member(room_id, member_id)`` 经 ``chat_room.id`` 关联,
    member_id = contact 表 rowid(实拍裁决见
    :func:`_contact_rowid_usernames`,不碰 Name2Id);显示名批量解析
    :func:`_contact_pick_names`、备注 :func:`_contact_pick_remarks`。

    **缺库/缺表/缺行 = 对应键 null 或空表,恒不判错**(判例同 key-status:
    状态查询不判错);contact 域整库缺失 = 全空结构。``is_owner`` 按
    ``chat_room.owner`` 标记,恰一真或零真。返回 ``{"group_info": …}``
    契约载荷(键序 = 契约 v1 原文序)。
    """
    info: dict[str, object] = {
        "chat_id": chat_id,
        "display_name": None,
        "member_count": 0,
        "owner": None,
        "announcement": None,
        "status": None,
        "members": [],
    }
    contact_con = _open_copy(copy_dir, "contact/contact.db")
    if contact_con is None:  # contact 域缺位:空结构如实降级,不判错
        return {"group_info": info}
    try:
        info["display_name"] = lookup_contact(contact_con, chat_id)
        room = _chat_room_row(contact_con, chat_id)
        if room is None:  # 非群 id / 群行缺:设置域全空如实
            return {"group_info": info}
        room_id, owner_wxid = room
        owner = (
            owner_wxid
            if isinstance(owner_wxid, str) and owner_wxid
            else None
        )
        member_ids = _chatroom_member_ids(contact_con, room_id)
        info["member_count"] = len(member_ids)
        rowid_map = _contact_rowid_usernames(contact_con, member_ids)
        usernames = [
            rowid_map[mid] for mid in member_ids if mid in rowid_map
        ]  # 反查不出的 member_id 弃(退群残留/联系人已删;宁缺毋假,
        # member_count 仍记真值)
        display_map = _contact_pick_names(
            contact_con,
            usernames + ([owner] if owner else []),
        )
        remark_map = _contact_pick_remarks(contact_con, usernames)
        announcement, status = _chat_room_settings(
            contact_con, chat_id, display_map
        )
        info["owner"] = (
            {
                "username": owner,
                "display": display_map.get(owner, owner),
            }
            if owner
            else None
        )
        info["announcement"] = announcement
        info["status"] = _json_safe_status(status)
        info["members"] = [
            {
                "username": username,
                "display": display_map.get(username, username),
                "remark": remark_map.get(username),
                "is_owner": username == owner,
            }
            for username in sorted(usernames)
        ]
    finally:
        contact_con.close()
    return {"group_info": info}


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
            # 0.5.1 发送者上屏名(主人令「要展示名字」):批量解析消息发送者
            # wxid→展示名并原地替换(文本前缀同步换名,sender_id 留原 id);
            # contact 域缺位时跳过,sender 维持 wxid 原样(如实,不臆造)。
            senders = [
                m.get("sender")
                for m in messages
                if isinstance(m.get("sender"), str)
            ]
            _apply_sender_display(messages, _contact_pick_names(contact_con, senders))
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
