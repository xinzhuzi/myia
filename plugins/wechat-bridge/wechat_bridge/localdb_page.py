"""R1/R2 查询增强:按会话 keyset 分页 + 会话清单普查(task 10-14-wechat-chat-export)。

对解密副本(``localdb.ensure_decrypted_copies`` 产物)的**只读查询增强**,
与 :mod:`wechat_bridge.localdb_query` 同族零微信进程接触:

- **R1 keyset 分页**(:func:`run_page`):每 Msg_ 分表谓词
  ``(create_time > ? OR (create_time = ? AND rowid > ?)) ORDER BY create_time, rowid``,
  翻页成本 O(页),严禁 OFFSET;游标 = base64(JSON) 不透明串,携带
  v/chat_id/order/window/shards **scope 守卫**(请求参数与游标不一致 →
  exit 2 ``invalid_cursor``,防串会话/串窗口复用;chatlog-keeper 版本号+
  scope 校验语义,自写实现)。首帧(无游标)= 从时间窗端点起取。
- **索引自举**(:func:`ensure_page_index`):解密副本是桥私有产物,允许建
  ``create_time`` 索引(SQLite 索引隐式追加 rowid 尾列,ORDER BY create_time,
  rowid 可整体命中)。标记文件键 = **建索引之后**取的副本 mtime(先记后建 =
  自举死循环——建索引会改 DB mtime;grill 修正②);建索引写动作与 E2 重建
  同走 ``.rebuild.lock`` 排他锁(localdb.py:1438 同一锁文件,零进程间穿插);
  每次建后 ``EXPLAIN QUERY PLAN`` 断言 ``SEARCH ... USING INDEX``(出现
  ``SCAN`` 即结构化报错,测试同名断言)。已知副作用(如实注记,grill 修正②):
  建索引刷新副本 mtime,会使按 mtime+size 指纹缓存的邻居件(C2 stats)指纹
  失效一次——属一次性成本,不触发副本重建(copy 比 source 新 = 新鲜)。
- **R2 会话普查**(:func:`run_conversations` / :func:`scan_conversations`):
  全部 Msg_ 分表逐表 ``COUNT(*)/MIN/MAX`` 一次性普查;**按副本指纹缓存**
  (mtime_ns+size;grill 修正①——441 表×346MB 的 COUNT(*) 不吃 create_time
  索引,每次 sidecar 调用重扫直接违反父档「严禁每次全库扫」;缓存与 C2 stats
  chats 共用 :func:`scan_conversations` 同一普查原语,指纹机制同 C2 R3)。

类型映射与 type-49 人话化(R3)证据 = ``tests/wechat-bridge/fixtures/
local_type_census.json``(真库只读普查,零内容);本模块的
:data:`MSG_TYPE_VARIANTS` 只收录普查在场的变体(WeFlow 变体表对拍 + 逐变体
抽样 XML 语义验证),不在场的不臆造,未知仍回落 ``type_<N>``。
"""

from __future__ import annotations

import base64
import fcntl
import hashlib
import json
import os
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from . import localdb_query
from .codes import EXIT_USAGE, BridgeError
from .localdb_query import (
    MSG_TYPE_NAMES,
    _decode_text_content,
    _normalize_ts,
    _open_copy,
    _sender_name,
    find_message_tables,
    name2id_maps,
)

__all__ = [
    "MSG_TYPE_VARIANTS",
    "CURSOR_VERSION",
    "PAGE_DEFAULT_LIMIT",
    "PAGE_LIMIT_CAP",
    "EXPORT_PAGE_BATCH",
    "normalize_ts_input",
    "humanize_message_content",
    "type_name_for",
    "type_filter_values",
    "encode_cursor",
    "decode_cursor",
    "ensure_page_index",
    "assert_index_search",
    "run_page",
    "run_conversations",
    "scan_conversations",
    "self_wxid",
]

#: 游标契约版本(scope 守卫第一道;升版 = 旧游标全量拒收)。
CURSOR_VERSION = 1

#: 分页缺省页大小与 CLI 帽(prd R1:--limit 缺省 200,帽 1000)。
PAGE_DEFAULT_LIMIT = 200
PAGE_LIMIT_CAP = 1000

#: 导出复用分页通道的批大小(prd R4:同游标逐批,批 500)。
EXPORT_PAGE_BATCH = 500

#: 副本内两库的消息分片(与 localdb_query.run_query 的 message_rels 同源)。
MESSAGE_DB_RELS = ("message/message_0.db", "message/biz_message_0.db")

#: R3 类型映射扩展(真库普查实证;证据逐条在 census 基件 ``mapping`` 节)。
#: 集成侧把本表并进 localdb_query.MSG_TYPE_NAMES 后,此处覆写变冗余无害
#: (同值;消费方零感)。
MSG_TYPE_VARIANTS: dict[int, str] = {
    42: "card",            # 名片(WeFlow 42;真库抽样 root=msg 空子节点)
    50: "call",            # 音视频通话(真库抽样 root=voipmsg)
    21474836529: "link",   # 链接卡(5<<32|49;appmsg<type>=5 + url)
    25769803825: "file",   # 文件(6<<32|49;WeFlow file 变体)
    34359738417: "file",   # 文件(8<<32|49;WeFlow file 变体)
    103079215153: "file",  # 文件(24<<32|49;WeFlow file 变体)
    81604378673: "record",  # 合并转发(19<<32|49;title=群聊的聊天记录)
    244813135921: "quote",  # 引用(57<<32|49;refermsg 在场)
}

#: type-49 族编码底数(hi32<<32|49;普查件 _meta 注记)。
_APPMSG_SHIFT = 32

#: 群消息 type-49/47 XML 的 ``wxid:\\n`` 前缀上限(4.1.15 真库实测)。
_GROUP_XML_PREFIX_MAX = 128

#: keyset 无穷端哨兵(SQL 参数安全量级)。
_BOUND_INF = 1 << 62


def _is_appmsg_local_type(local_type: int) -> bool:
    """type-49 族判定(含大数变体;非 49 编码的大数不成族)。"""
    if local_type == 49:
        return True
    if local_type < _BOUND_INF and local_type > 1 << _APPMSG_SHIFT:
        return (local_type - 49) % (1 << _APPMSG_SHIFT) == 0
    return False


def appmsg_subtype(local_type: int) -> int | None:
    """type-49 族的 appmsg 语义位(hi32;与 ``<appmsg><type>`` 子节点同值)。"""
    if local_type == 49:
        return None  # 纯 49 无语义位,以 XML 内 <type> 为准
    if not _is_appmsg_local_type(local_type):
        return None
    return (local_type - 49) >> _APPMSG_SHIFT


def type_name_for(local_type: int) -> str:
    """local_type → 类型名(census 覆写 → MSG_TYPE_NAMES → type_<N>)。"""
    name = MSG_TYPE_VARIANTS.get(local_type) or MSG_TYPE_NAMES.get(local_type)
    return name if name is not None else f"type_{local_type}"


def type_filter_values(types: list[str]) -> list[int]:
    """类型名(或 type_<N> 字面量)→ local_type 值集(SQL IN 谓词用)。

    一个名字可映射多个 local_type(file 族);字面量 ``type_<N>`` 允许筛
    普查在场的未映射长尾;未知名字 = exit 2 用法错(拼错早炸,不静默空结果)。
    """
    wanted = [t.strip() for t in types if t.strip()]
    if not wanted:
        return []
    by_name: dict[str, list[int]] = {}
    for value in (*MSG_TYPE_VARIANTS.keys(), *MSG_TYPE_NAMES.keys()):
        by_name.setdefault(type_name_for(value), []).append(value)
    values: list[int] = []
    for name in wanted:
        if name in by_name:
            values.extend(v for v in by_name[name] if v not in values)
            continue
        if name.startswith("type_") and name[5:].lstrip("-").isdigit():
            values.append(int(name[5:]))
            continue
        raise BridgeError(
            EXIT_USAGE,
            f"未知消息类型 {name!r}(合法名:{sorted(by_name)} 或 type_<N> 字面量)",
            code="invalid_types",
            fix_hint="类型名见 tests/wechat-bridge/fixtures/local_type_census.json 映射表;"
            "常用:text/image/voice/video/sticker/location/file/link/quote/record/card/call",
        )
    return values


# ---------------------------------------------------------------------------
# R3 人话化(type-49 XML / 47 表情;prd R3 产出行文案)
# ---------------------------------------------------------------------------

# 集成侧把 humanize_content 落位 localdb_query.py(prd R3 定稿)后,共享实现
# 优先;本文件参考实现保底(同契约,先落谁都不破消费方)。
try:
    from .localdb_query import humanize_content as _shared_humanize
except ImportError:  # pragma: no cover - 集成落位前缺符号是合法态
    _shared_humanize = None


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
    """剥离群消息 XML 的 ``wxid:\\n`` 前缀(仅当后跟 '<' 才剥,正文不误伤)。"""
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
        subtype = appmsg_subtype(local_type)
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


def _humanize_impl(
    local_type: int, content: Any, stats: dict[str, object] | None
) -> str | None:
    """humanize 参考实现(str 人话;None = 解不出,调用方落占位+计数)。"""
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


def humanize_message_content(
    local_type: int, content: Any, stats: dict[str, object] | None = None
) -> str | None:
    """type-49 族 / 47 → 人话(prd R3 定稿落 localdb_query.humanize_content;
    集成前由本模块参考实现兜底——同一契约,消费方零感)。"""
    if _shared_humanize is not None:
        return _shared_humanize(local_type, content, stats)
    return _humanize_impl(local_type, content, stats)


# ---------------------------------------------------------------------------
# 时间归一(prd R1:秒;>1e12 毫秒 /1000,>1e15 微秒 /1e6;WeFlow 语义)
# ---------------------------------------------------------------------------


def normalize_ts_input(raw: Any, *, flag: str = "ts") -> int | None:
    """CLI/协议时间输入归一到 unix 秒(None 透传;坏形状 = exit 2)。"""
    if raw is None:
        return None
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        raise BridgeError(
            EXIT_USAGE, f"--{flag} 须为整数时间戳,当前为 {raw!r}", code="usage"
        ) from None
    if value > 10**15:  # 微秒 → 秒
        value //= 10**6
    elif value > 10**12:  # 毫秒 → 秒
        value //= 1000
    if value < 0:
        raise BridgeError(
            EXIT_USAGE, f"--{flag} 不接受负时间戳: {raw!r}", code="usage"
        )
    return value


# ---------------------------------------------------------------------------
# 游标(base64 JSON;scope 守卫)
# ---------------------------------------------------------------------------


def encode_cursor(state: dict[str, Any]) -> str:
    """游标状态 → 不透明串(标准 base64;utf-8 JSON)。"""
    return base64.b64encode(
        json.dumps(state, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).decode("ascii")


def decode_cursor(
    raw: str | None,
    *,
    chat_id: str,
    order: str,
    from_ts: int | None,
    to_ts: int | None,
) -> dict[str, Any] | None:
    """不透明串 → 游标状态;**scope 守卫**:v/chat_id/order/window 与请求
    不一致 → exit 2 ``invalid_cursor``(防串会话/串窗口复用)。坏 base64/
    坏 JSON/坏形状同码(不透明串对调用方就是黑盒,损坏即拒)。None = 首帧。"""
    if raw is None or not raw.strip():
        return None
    try:
        state = json.loads(base64.b64decode(raw.strip(), validate=True))
    except ValueError:  # binascii.Error/JSONDecodeError 均其子类
        raise BridgeError(
            EXIT_USAGE, "游标不可解码(损坏或非本命令产物)", code="invalid_cursor"
        ) from None
    if (
        not isinstance(state, dict)
        or state.get("v") != CURSOR_VERSION
        or state.get("chat_id") != chat_id
        or state.get("order") != order
        or state.get("window") != {"from_ts": from_ts, "to_ts": to_ts}
        or not isinstance(state.get("shards"), dict)
        or not all(
            isinstance(shard, dict)
            and isinstance(shard.get("ts"), int)
            and isinstance(shard.get("rowid"), int)
            for shard in state["shards"].values()
        )
    ):
        raise BridgeError(
            EXIT_USAGE,
            "游标与请求参数不匹配(chat_id/顺序/时间窗须与首发一致)",
            code="invalid_cursor",
            fix_hint="游标只能续拉同一会话同一筛选形状的下一页;换筛选条件请不带游标重新首发",
        )
    return state


# ---------------------------------------------------------------------------
# 索引自举(副本私有区唯一写动作之一;prd R1 / grill 修正②)
# ---------------------------------------------------------------------------

#: 副本各库目录旁的索引标记文件名(键 = 建索引**之后**取的 mtime_ns+size)。
_INDEX_MARKER_NAME = ".page-index.json"


def index_marker_path(copy_dir: Path, rel: str) -> Path:
    return copy_dir / Path(rel).parent / _INDEX_MARKER_NAME


class _RebuildLock:
    """E2 重建同款排他锁(localdb.ensure_decrypted_copies 同一锁文件;
    索引写动作进锁 = 与副本重建零穿插,grill 修正②锁竞争注记在此闭合)。

    刻意不用 @contextmanager:其退出路径对异常做 Python 级
    ``exc.__traceback__ = …`` 赋值,frozen dataclass 的 BridgeError 会炸
    FrozenInstanceError(2026-10-14 实测);类式上下文管理器零此坑。
    """

    def __init__(self, copy_dir: Path) -> None:
        self._copy_dir = copy_dir
        self._fh: Any = None

    def __enter__(self) -> "_RebuildLock":
        lock_path = self._copy_dir / ".rebuild.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(lock_path, "a")
        fcntl.flock(self._fh, fcntl.LOCK_EX)
        return self

    def __exit__(self, *_exc: object) -> None:
        if self._fh is not None:
            self._fh.close()
            self._fh = None


def _load_marker(path: Path) -> dict[str, dict[str, int]]:
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return {}


def _fingerprint(path: Path) -> dict[str, int]:
    stat = path.stat()
    return {"mtime_ns": stat.st_mtime_ns, "size": stat.st_size}


def assert_index_search(con: sqlite3.Connection, table: str, time_col: str) -> None:
    """EXPLAIN 断言:分页查询计划须索引命中(``SEARCH … USING [COVERING]
    INDEX`` 均合法——SQLite 对该查询形状常报 COVERING 形态;出现 ``SCAN``
    即报错,prd R1 断言语义)。"""
    plan = list(
        con.execute(
            f'EXPLAIN QUERY PLAN SELECT rowid FROM "{table}" '
            f'WHERE "{time_col}" > ? ORDER BY "{time_col}", rowid LIMIT 1',
            (0,),
        )
    )
    details = " | ".join(str(row[-1]) for row in plan)
    if "SCAN" in details or "USING" not in details or "INDEX" not in details:
        raise BridgeError(
            1,
            f"分页索引未按预期命中(计划含 SCAN 或无索引): {details}",
            code="index_plan_scan",
            fix_hint="副本索引自举异常;删除副本目录旁 .page-index.json 后重试触发重建",
        )


def ensure_page_index(
    copy_dir: Path, rel: str, tables: list[tuple[str, dict[str, Any]]]
) -> int:
    """对涉及 Msg_ 表自举 create_time 索引;返回本次新建索引计数。

    标记文件键 = **CREATE INDEX 之后**取的 mtime_ns+size(先记后建 = 自举
    死循环:建索引改 mtime → 标记永不匹配 → 每次重建;grill 修正②)。副本
    重建(新文件 mtime)→ 标记失配 → 下次自举重建索引。写动作与 E2 重建
    同走 ``.rebuild.lock``。
    """
    db_path = copy_dir / rel
    marker_path = index_marker_path(copy_dir, rel)
    time_cols = {
        table: colmap.get("time") for table, colmap in tables if colmap.get("time")
    }
    if not time_cols:
        return 0
    built = 0
    with _RebuildLock(copy_dir):
        markers = _load_marker(marker_path)
        stale = [
            table
            for table, time_col in time_cols.items()
            if markers.get(f"{rel}::{table}") != _fingerprint(db_path)
        ]
        if not stale:
            return 0
        con = sqlite3.connect(db_path)  # rw:建索引是副本私有区合法写
        try:
            for table in stale:
                con.execute(
                    f'CREATE INDEX IF NOT EXISTS "idx_{table}_ct" '
                    f'ON "{table}" ("{time_cols[table]}")'
                )
                assert_index_search(con, table, time_cols[table])
                built += 1
            con.commit()
        finally:
            con.close()
        # 键值取值时点 = 建索引落盘**之后**(grill 修正②的死循环坑位)
        fresh_fp = _fingerprint(db_path)
        for table in stale:
            markers[f"{rel}::{table}"] = fresh_fp
        marker_path.write_text(json.dumps(markers, ensure_ascii=False, indent=1))
        os.chmod(marker_path, 0o600)
    return built


# ---------------------------------------------------------------------------
# 分片与 keyset 行拉取
# ---------------------------------------------------------------------------


class _Shard:
    """一个 Msg_ 分表的查询形状(库相对路径/表名/列映射)。"""

    __slots__ = ("rel", "table", "colmap")

    def __init__(self, rel: str, table: str, colmap: dict[str, Any]) -> None:
        self.rel = rel
        self.table = table
        self.colmap = colmap

    @property
    def key(self) -> str:
        return f"{self.rel}::{self.table}"


def iter_message_shards(
    copy_dir: Path, chat_id: str
) -> tuple[dict[str, tuple[sqlite3.Connection, _Shard]], dict[str, dict[int, str]]]:
    """开全部分片连接:两库 ×(旧形态 talker 命中 / 4.1.15 表名 md5 反解)。

    Returns:
        ``(shards, name_maps)``——shards 键 = ``<rel>::<table>``;name_maps
        为每库 Name2Id rowid→wxid(发送者反查;调用方负责关连接)。
    """
    shards: dict[str, tuple[sqlite3.Connection, _Shard]] = {}
    name_maps: dict[str, dict[int, str]] = {}
    for rel in MESSAGE_DB_RELS:
        con = _open_copy(copy_dir, rel)
        if con is None:
            continue
        try:
            tables = find_message_tables(con)
        except sqlite3.Error:
            con.close()
            continue
        selected = [
            (table, colmap)
            for table, colmap in tables
            if colmap.get("talker") or colmap.get("chat") == chat_id
        ]
        if not selected:
            con.close()
            continue
        name_maps[rel] = name2id_maps(con)[0]
        for table, colmap in selected:
            shard = _Shard(rel, table, colmap)
            shards[shard.key] = (con, shard)
    return shards, name_maps


#: 发送者过滤形状:None = 不过滤;("rowids", …) = 4.1.15 real_sender_id IN 集
#: (空集 = 无可命中);("issender", 0|1) = 旧形态 isSender 精确等值。
_SenderFilter = tuple[str, Any] | None


def _sender_filter(
    shard: _Shard, name_map: dict[int, str], chat_id: str, sender: str
) -> _SenderFilter:
    """--sender wxid → SQL 侧精确谓词形状(按解析前原始 id 匹配)。"""
    if shard.colmap.get("sender_id"):
        rowids = [rid for rid, name in name_map.items() if name == sender]
        return ("rowids", rowids)  # 空集如实:该库无此 wxid = 零命中
    if shard.colmap.get("sender"):  # 旧形态原名只有 me/chat_id 两名可匹配
        if sender == "me":
            return ("issender", 1)
        if sender == chat_id:
            return ("issender", 0)
        return ("issender", -1)  # 无从匹配:恒假谓词
    return ("none", None)


def _build_shard_sql(
    shard: _Shard,
    *,
    bound_ts: int,
    bound_rowid: int,
    ascending: bool,
    from_ts: int | None,
    to_ts: int | None,
    type_values: list[int],
    sender_filter: _SenderFilter,
    chat_id: str,
    limit: int,
) -> tuple[str, list[object], dict[str, int]]:
    """构造单分片 keyset SQL(严格参数化;返回 (sql, params, 列序索引))。"""
    colmap = shard.colmap
    time_col = colmap["time"]
    op = ">" if ascending else "<"
    clauses = [f'("{time_col}" {op} ? OR ("{time_col}" = ? AND rowid {op} ?))']
    params: list[object] = [bound_ts, bound_ts, bound_rowid]
    if colmap.get("talker"):
        clauses.append(f'"{colmap["talker"]}" = ?')
        params.append(chat_id)
    if from_ts is not None:
        clauses.append(f'"{time_col}" >= ?')
        params.append(from_ts)
    if to_ts is not None:
        clauses.append(f'"{time_col}" <= ?')
        params.append(to_ts)
    if type_values:
        if colmap.get("type"):
            marks = ",".join("?" for _ in type_values)
            clauses.append(f'"{colmap["type"]}" IN ({marks})')
            params.extend(type_values)
        else:
            clauses.append("1 = 0")
    if sender_filter is not None and sender_filter[0] == "rowids":
        rowids = sender_filter[1]
        if colmap.get("sender_id") and rowids:
            marks = ",".join("?" for _ in rowids)
            clauses.append(f'"{colmap["sender_id"]}" IN ({marks})')
            params.extend(rowids)
        else:
            clauses.append("1 = 0")  # 空集/无列:如实零命中
    elif sender_filter is not None and sender_filter[0] == "issender":
        value = sender_filter[1]
        if colmap.get("sender") and value in (0, 1):
            clauses.append(f'"{colmap["sender"]}" = ?')
            params.append(value)
        else:
            clauses.append("1 = 0")
    cols = ['rowid', f'"{time_col}"', f'"{colmap["content"]}"']
    idx = {"rowid": 0, "time": 1, "content": 2}
    for key in ("type", "sender_id", "sender", "ct_content"):
        if colmap.get(key):
            idx[key] = len(cols)
            cols.append(f'"{colmap[key]}"')
    direction = "ASC" if ascending else "DESC"
    sql = (
        f"SELECT {', '.join(cols)} FROM \"{shard.table}\" "
        f"WHERE {' AND '.join(clauses)} "
        f'ORDER BY "{time_col}" {direction}, rowid {direction} LIMIT ?'
    )
    params.append(limit)
    return sql, params, idx


def page_rows(
    con: sqlite3.Connection,
    shard: _Shard,
    name_map: dict[int, str],
    chat_id: str,
    *,
    bound_ts: int,
    bound_rowid: int,
    ascending: bool,
    from_ts: int | None = None,
    to_ts: int | None = None,
    type_values: list[int] | None = None,
    sender: str | None = None,
    limit: int = PAGE_DEFAULT_LIMIT,
    stats: dict[str, object] | None = None,
) -> list[dict[str, object]]:
    """单分片 keyset 行拉取 → R1 消息条目(条目语义同 query_messages 族:
    sender 经显示名解析前的 wxid,sender_id 留原 wxid,非文本占位不臆造,
    type-49 族/47 经人话化出文案)。"""
    sender_filter = _sender_filter(shard, name_map, chat_id, sender) if sender else None
    sql, params, idx = _build_shard_sql(
        shard,
        bound_ts=bound_ts,
        bound_rowid=bound_rowid,
        ascending=ascending,
        from_ts=from_ts,
        to_ts=to_ts,
        type_values=type_values or [],
        sender_filter=sender_filter,
        chat_id=chat_id,
        limit=limit,
    )
    try:
        rows = con.execute(sql, params).fetchall()
    except sqlite3.Error:
        return []  # 单表漂移不拖垮整页(红线 7 同款降级)
    entries: list[dict[str, object]] = []
    for row in rows:
        content = row[idx["content"]]
        local_type = 1
        if "type" in idx:
            try:
                local_type = int(row[idx["type"]] or 0)
            except (TypeError, ValueError):
                local_type = 0
        ct_marker = row[idx["ct_content"]] if "ct_content" in idx else None
        if "sender_id" in idx:  # 4.1.15 real_sender_id → Name2Id rowid 反查
            sender_wxid = _sender_name(row[idx["sender_id"]], name_map, chat_id)
        elif "sender" in idx:  # 旧形态 isSender(0/1)
            sender_wxid = "me" if row[idx["sender"]] == 1 else chat_id
        else:
            sender_wxid = chat_id
        entry: dict[str, object] = {
            "seq": int(row[idx["rowid"]]),
            "ts": _normalize_ts(row[idx["time"]]),
            "sender": sender_wxid,
            "sender_id": sender_wxid,
            "type": type_name_for(local_type),
            "local_type": local_type,
        }
        text: str | None = None
        placeholder: str | None = None
        if local_type == 1:
            text, placeholder = _decode_text_content(content, ct_marker, stats)
        elif _is_appmsg_local_type(local_type) or local_type == 47:
            decoded, decode_ph = _decode_text_content(content, ct_marker, stats)
            if decoded is not None:
                human = humanize_message_content(local_type, decoded, stats)
                if human is not None:
                    text = human
                else:
                    placeholder = entry["type"] + "(内容未识别)"
            else:
                placeholder = decode_ph
        else:
            placeholder = entry["type"] + "(占位)"
        if text is not None:
            entry["text"] = text
        else:
            entry["placeholder"] = placeholder or "内容未导出(占位)"
        entries.append(entry)
    return entries


# ---------------------------------------------------------------------------
# R1 run_page(编排入口;CLI/编排层直调)
# ---------------------------------------------------------------------------


def run_page(
    copy_dir: Path,
    chat_id: str,
    *,
    cursor: str | None = None,
    limit: int | None = None,
    asc: bool | None = None,
    from_ts: int | None = None,
    to_ts: int | None = None,
    types: list[str] | None = None,
    sender: str | None = None,
    display_names: dict[str, str] | None = None,
    stats: dict[str, object] | None = None,
) -> dict[str, object]:
    """R1 分页查询主体(应答 = ``{"page": …}`` 契约载荷,键序 = prd 原文序)。

    Args:
        copy_dir: 解密副本根(E2 产物路径)。
        chat_id: 目标会话 id(wxid 或 @chatroom)。
        cursor: 首发传 None;续拉传上页 next_cursor(scope 守卫在此)。
        limit: 页大小(缺省 200,帽 1000;帽外 = exit 2)。
        asc: None = desc(最新在前,prd 缺省);True/False 显式定序。
        from_ts/to_ts: 时间窗(unix 秒;编排层已归一)。
        types: 类型名清单(text/file/…或 type_<N> 字面量;SQL 侧 IN)。
        sender: 按解析前原始 wxid 精确匹配(SQL 侧谓词)。
        display_names: 编排层(contact 域在场)批量解析的 wxid→显示名
            (remark>nickname>alias);缺省/未命中 = sender 维持 wxid(如实)。
        stats: 解码/解析降级计数(调用方透传应答附加键;None = 不收集)。
    """
    page_size = PAGE_DEFAULT_LIMIT if limit is None else limit
    if not 1 <= page_size <= PAGE_LIMIT_CAP:
        raise BridgeError(
            EXIT_USAGE,
            f"--limit 须为 1..{PAGE_LIMIT_CAP} 的整数,当前为 {limit}",
            code="usage",
        )
    order = "asc" if (asc if asc is not None else False) else "desc"
    ascending = order == "asc"
    type_values = type_filter_values(types or [])
    state = decode_cursor(
        cursor, chat_id=chat_id, order=order, from_ts=from_ts, to_ts=to_ts
    )
    shards, name_maps = iter_message_shards(copy_dir, chat_id)
    try:
        for rel in MESSAGE_DB_RELS:
            ensure_page_index(
                copy_dir,
                rel,
                [(s.table, s.colmap) for (_c, s) in shards.values() if s.rel == rel],
            )
        fetch_n = page_size + 1  # 多拉一条探 has_more(两分片时合并后再裁)
        candidates: list[tuple[int, int, str, dict[str, object]]] = []
        has_more = False
        next_shards: dict[str, dict[str, int]] = {}
        for key, (con, shard) in shards.items():
            if state is not None and key in state["shards"]:
                bound = state["shards"][key]
                bound_ts, bound_rowid = int(bound["ts"]), int(bound["rowid"])
                next_shards[key] = dict(bound)  # 未消耗分片游标原地
            else:
                # 首帧从时间窗端点起取:asc = from 端;desc = to 端/上界
                bound_ts = (
                    from_ts if from_ts is not None else 0
                ) if ascending else (to_ts if to_ts is not None else _BOUND_INF)
                bound_rowid = 0 if ascending else _BOUND_INF
            rows = page_rows(
                con,
                shard,
                name_maps.get(shard.rel, {}),
                chat_id,
                bound_ts=bound_ts,
                bound_rowid=bound_rowid,
                ascending=ascending,
                from_ts=from_ts,
                to_ts=to_ts,
                type_values=type_values,
                sender=sender,
                limit=fetch_n,
                stats=stats,
            )
            if len(rows) > page_size:
                has_more = True  # 该分片窗内必有更多(limit+1 已到手)
            for row in rows[:page_size]:
                candidates.append((int(row["ts"]), int(row["seq"]), key, row))
        if len(candidates) > page_size:
            has_more = True  # 多分片合流超页宽(即使单分片未触 limit+1)
        candidates.sort(key=lambda item: (item[0], item[1], item[2]), reverse=not ascending)
        window = candidates[:page_size]
        messages = [item[3] for item in window]
        # 游标推进 = 各分片在本页窗口内**实际消费**到的最后一行;被合并裁剪
        # 掉的行不推进(留在原窗,下页续取)——先排序后裁剪保证每分片子序列
        # 在窗口内连续,推进到最后消费行即正确。
        for ts, seq, key, _row in window:
            next_shards[key] = {"ts": ts, "rowid": seq}
        if display_names:
            for message in messages:
                wxid = message.get("sender_id")
                if isinstance(wxid, str) and wxid in display_names:
                    message["sender"] = display_names[wxid]
        next_cursor = None
        if has_more and next_shards:
            next_cursor = encode_cursor(
                {
                    "v": CURSOR_VERSION,
                    "chat_id": chat_id,
                    "order": order,
                    "window": {"from_ts": from_ts, "to_ts": to_ts},
                    "shards": next_shards,
                }
            )
        return {
            "page": {
                "chat_id": chat_id,
                "display_name": (display_names or {}).get(chat_id),
                "messages": messages,
                "next_cursor": next_cursor,
                "has_more": has_more,
                "filter": {
                    "from_ts": from_ts,
                    "to_ts": to_ts,
                    "types": [t.strip() for t in types if t.strip()] if types else [],
                    "sender": sender,
                    "order": order,
                },
                "page_size": page_size,
            }
        }
    finally:
        for con, _shard in shards.values():
            con.close()


# ---------------------------------------------------------------------------
# R2 会话普查(conversations;指纹缓存 = grill 修正①)
# ---------------------------------------------------------------------------

#: 普查缓存文件(副本根下;键 = 两库 mtime_ns+size 指纹)。
_CENSUS_CACHE_NAME = "conversations-census.json"

#: 会话清单缺省条数与上界(prd R2:--limit 缺省 500)。
CONVERSATIONS_DEFAULT_LIMIT = 500
CONVERSATIONS_LIMIT_MAX = 5000


def _census_fingerprint(copy_dir: Path) -> dict[str, list[int]]:
    fp: dict[str, list[int]] = {}
    for rel in MESSAGE_DB_RELS:
        path = copy_dir / rel
        if path.is_file():
            stat = path.stat()
            fp[rel] = [stat.st_mtime_ns, stat.st_size]
    return fp


def _census_cache_path(copy_dir: Path) -> Path:
    return copy_dir / _CENSUS_CACHE_NAME


def scan_conversations(copy_dir: Path) -> dict[str, object]:
    """R2 普查原语(一次性逐表 COUNT/MIN/MAX;C2 stats chats 复用同一原语,
    grill 修正①「两档在做同一件事」的合流点)。

    缓存按副本指纹(两库 mtime_ns+size)落副本根 0600;指纹失配(副本重建/
    索引自举改 mtime)→ 重扫一次并刷新缓存。返回:
    ``{"conversations": […按 last_ts 降序…], "total": N, "unresolved_tables": M}``
    (total 含反解不出的表;不入清单,不猜归属)。
    """
    cache_path = _census_cache_path(copy_dir)
    fingerprint = _census_fingerprint(copy_dir)
    try:
        cached = json.loads(cache_path.read_text())
        if (
            isinstance(cached, dict)
            and cached.get("fingerprint") == fingerprint
            and isinstance(cached.get("payload"), dict)
        ):
            return cached["payload"]
    except (OSError, ValueError):
        pass
    per_chat: dict[str, dict[str, int]] = {}
    unresolved = 0
    for rel in MESSAGE_DB_RELS:
        con = _open_copy(copy_dir, rel)
        if con is None:
            continue
        try:
            for table, colmap in find_message_tables(con):
                time_col = colmap.get("time")
                if not time_col:
                    continue
                chat = None if colmap.get("talker") else colmap.get("chat")
                try:
                    row = con.execute(
                        f'SELECT COUNT(*), MIN("{time_col}"), MAX("{time_col}") '
                        f'FROM "{table}"'
                    ).fetchone()
                except sqlite3.Error:
                    continue
                if chat is None:
                    unresolved += 1  # 会话编码在行内(旧形态)/反解不出:不猜归属
                    continue
                count, first_ts, last_ts = int(row[0] or 0), row[1], row[2]
                agg = per_chat.setdefault(
                    chat, {"msg_count": 0, "first_ts": 1 << 62, "last_ts": 0}
                )
                agg["msg_count"] += count
                if first_ts is not None:
                    agg["first_ts"] = min(agg["first_ts"], _normalize_ts(first_ts))
                if last_ts is not None:
                    agg["last_ts"] = max(agg["last_ts"], _normalize_ts(last_ts))
        except sqlite3.Error:
            pass  # 库级漂移:已扫表保留,普查是尽力面
        finally:
            con.close()
    names: dict[str, str] = {}
    contact_con = _open_copy(copy_dir, "contact/contact.db")
    try:
        if contact_con is not None and per_chat:
            names = localdb_query._contact_pick_names(contact_con, list(per_chat))
    finally:
        if contact_con is not None:
            contact_con.close()
    conversations = [
        {
            "chat_id": chat,
            "display_name": names.get(chat),
            "is_group": chat.endswith("@chatroom"),
            "msg_count": agg["msg_count"],
            "first_ts": agg["first_ts"] if agg["first_ts"] < (1 << 62) else None,
            "last_ts": agg["last_ts"] or None,
        }
        for chat, agg in per_chat.items()
        if agg["msg_count"] > 0
    ]
    conversations.sort(key=lambda item: item["last_ts"] or 0, reverse=True)
    payload: dict[str, object] = {
        "conversations": conversations,
        "total": len(conversations) + unresolved,
        "unresolved_tables": unresolved,
    }
    try:
        cache_path.write_text(
            json.dumps(
                {"fingerprint": fingerprint, "payload": payload},
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )
        os.chmod(cache_path, 0o600)
    except OSError:
        pass  # 缓存写失败不拦普查(只读面恒可用)
    return payload


def run_conversations(copy_dir: Path, *, limit: int | None = None) -> dict[str, object]:
    """R2 会话清单(应答键序 = prd 原文;普查原语 + limit 截断)。"""
    page_size = CONVERSATIONS_DEFAULT_LIMIT if limit is None else limit
    if not 1 <= page_size <= CONVERSATIONS_LIMIT_MAX:
        raise BridgeError(
            EXIT_USAGE,
            f"--limit 须为 1..{CONVERSATIONS_LIMIT_MAX} 的整数,当前为 {limit}",
            code="usage",
        )
    payload = scan_conversations(copy_dir)
    return {
        "conversations": payload["conversations"][:page_size],
        "total": payload["total"],
        "unresolved_tables": payload["unresolved_tables"],
    }


# ---------------------------------------------------------------------------
# 自端锚定(HTML 气泡左右侧语义;filehelper 表 = 只含自发/文件助手两源)
# ---------------------------------------------------------------------------


def self_wxid(copy_dir: Path) -> str | None:
    """自端 wxid 推断:``Msg_md5("filehelper")`` 表的发送者并集去掉
    ``filehelper`` 本身 = 自端(文件传输助手会话只含自端发送;4.1.15 真库
    实测该表唯一发送者即自端 wxid)。锚表缺席/歧义 = None 如实(HTML 全部
    单侧渲染,不臆造)。"""
    digest = hashlib.md5(b"filehelper").hexdigest()
    for rel in MESSAGE_DB_RELS:
        con = _open_copy(copy_dir, rel)
        if con is None:
            continue
        try:
            tables = [
                row[0]
                for row in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
                if isinstance(row[0], str) and row[0].lower().endswith(digest)
            ]
            if not tables:
                continue
            matches = {
                table: colmap
                for table, colmap in find_message_tables(con)
                if table == tables[0]
            }
            sender_col = matches[tables[0]].get("sender_id")
            if not sender_col:
                return None
            name_map = name2id_maps(con)[0]
            senders = set()
            for (rid,) in con.execute(
                f'SELECT DISTINCT "{sender_col}" FROM "{tables[0]}"'
            ):
                try:
                    name = name_map.get(int(rid))
                except (TypeError, ValueError):
                    continue
                if name:
                    senders.add(name)
            senders.discard("filehelper")
            return next(iter(senders)) if len(senders) == 1 else None
        except (sqlite3.Error, StopIteration, KeyError):
            return None
        finally:
            con.close()
    return None
