"""E3 联系人工作台只读查询(task 10-14-wechat-contacts;R1 分类计数分页 + R2 考古分层)。

对**解密副本**(数据根私有区,``localdb.ensure_decrypted_copies`` 产物)做
纯只读 SQL。编排壳(localdb.py ``contacts_inventory``,集成批落位)负责
E2 副本域选择与自愈钩子——缺省/无 residue = 单 ``contact`` 域(group-info
域收缩纪律);``--with-residue`` = ``["contact","message"]``(Tier A 需要
message_0.db Name2Id)。本层吃 ``copy_dir`` 直查。

**六桶判定序(钉死,每行恰归一桶;2026-10-14 真库实测自考,唯一权威源)**:

①username ∈ 系统号排除集 → ``system``(不出行,只进 counts 诊断);
②``username LIKE '%@chatroom'`` → ``group``;③``username LIKE 'gh\\_%'``
(ESCAPE)→ ``official``(不叠 lt1 条件——本机 gh_ 三种 local_type 都在,
全量归公众号桶,与 WeFlow 的 gh_+lt1 组合**有意分歧**,分歧原因=真库
实测);④``local_type=3 AND nick_name<>''`` → ``former``;⑤``local_type=1``
→ ``friend``;⑥其余 → ``other``。实测闭包:六桶加和 == COUNT(*)。

**WeFlow 严判据对照(诊断字段 strict_residual_count)**:原式词面 =
「lt0+quan_pin 或 lt3+flag≠4+身份字段」,作用域是**人集**(排除系统号/
chatroom/gh_——2026-10-14 本机实测:lt0+quan_pin 命中 8 行**全是 gh_**,
排除后 lt0 臂零命中、lt3 臂恰 1 行,全式命中 1 与真库锚一致)。许可红线:
WeFlow 是 CC BY-NC-SA,此处是判定式的数据事实转写,零码零文案照搬。

**诚实契约**:缺表/缺列 → 对应桶/字段空 + ``degraded`` 诊断标注,恒
exit 0(判例 group-info);extra_buffer/data_json 等 blob 列 opaque 原样
不解析(greenbubbles 判例);找回=考古呈现非保证,零重加操作(prd 红线)。

私有数据红线(prd 红线 6 同款):查询结果 = CLI stdout 契约载荷,不入
日志、不入 git;错误消息只承载形状与计数。
"""

from __future__ import annotations

import base64
import binascii
import json
import sqlite3
from pathlib import Path
from typing import Any

from .codes import EXIT_USAGE, BridgeError
from .localdb_query import _columns, _open_copy, _pick, name2id_maps

__all__ = [
    "contacts_page",
    "normalize_cli_limit",
    "encode_cursor",
    "decode_cursor",
    "SYSTEM_USERNAMES",
    "TYPE_FILTERS",
    "LIMIT_DEFAULT",
    "LIMIT_MAX",
]

#: 系统号排除集(R1 ①;2026-10-14 真库在场 4 个,集为判定式钉死全量)。
SYSTEM_USERNAMES: tuple[str, ...] = (
    "medianote",
    "floatbottle",
    "qmessage",
    "qqmail",
    "fmessage",
    "weixin",
    "weixinigram",
    "weixin_team",
)

#: 可见五桶(出行的桶;system 只进 counts 诊断不出行)。
TYPE_FILTERS: tuple[str, ...] = ("friend", "group", "official", "former", "other")

#: counts 六键(契约键序;system 是诊断桶)。
_COUNT_KEYS: tuple[str, ...] = ("friend", "group", "official", "former", "other", "system")

#: 列名候选族(PRAGMA 自适应,判例 localdb_query._pick;命中顺序即优先序)。
_USERNAME_COLS = ("username", "userName", "UserName", "user_name")
_NICKNAME_COLS = ("nick_name", "nickname", "nickName", "NickName")
_REMARK_COLS = ("remark", "Remark", "conRemark")
_ALIAS_COLS = ("alias", "Alias")
_LOCALTYPE_COLS = ("local_type", "localType")
_QUANPIN_COLS = ("quan_pin", "quanPin")
_DESCRIPTION_COLS = ("description", "desc")
_FLAG_COLS = ("flag",)

#: keyword 检索列(R1:五列 LIKE %K%)。
_KEYWORD_COLS = ("remark", "nick_name", "alias", "username", "quan_pin")

#: ``--limit`` 三态(prd.md:75 + 设计拷问修正①:0 与缺省 100/帽 1000 三态,
#: 防误写成「limit 0=空」——0 = 全量导出态,帽豁免)。
LIMIT_DEFAULT = 100
LIMIT_MAX = 1000

#: 游标形状版本(不透明串内 JSON 的 v 字段;形状变体递增防串用)。
_CURSOR_VERSION = 1


def normalize_cli_limit(raw: int | None) -> int:
    """CLI ``--limit`` 三态归一:缺省 100 / 0 = 全量(帽豁免)/ N 帽 1000。

    负值 = usage 拒(0 是合法的「全量导出态」特例,不是页大小;cli 注册
    的 help 措辞与本函数共同防误用——见 integrationSpec)。
    """
    if raw is None:
        return LIMIT_DEFAULT
    if raw < 0:
        raise BridgeError(
            EXIT_USAGE,
            f"--limit 须为非负整数(0 = 全量导出态,缺省 {LIMIT_DEFAULT},"
            f"上帽 {LIMIT_MAX}),当前为 {raw}",
            code="usage",
            fix_hint="分页浏览给 1..1000;全量导出走 --limit 0(桥内帽豁免)",
        )
    if raw == 0:
        return 0
    return min(raw, LIMIT_MAX)


def _esc(text: str) -> str:
    """LIKE 模式字面量化(%/_/\\ 前置反斜杠;配 ``ESCAPE '\\'`` 子句)。"""
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _norm_filter(type_filter: str | None, keyword: str | None) -> dict[str, Any]:
    """请求过滤归一:type ∈ 五桶或 None;keyword 去首尾空白、空 → None。"""
    normalized_type: str | None = None
    if type_filter is not None:
        normalized_type = str(type_filter).strip() or None
    if normalized_type is not None and normalized_type not in TYPE_FILTERS:
        raise BridgeError(
            EXIT_USAGE,
            f"--type 须为 {'|'.join(TYPE_FILTERS)} 之一,当前为 {type_filter!r}",
            code="usage",
        )
    normalized_keyword: str | None = None
    if keyword is not None:
        normalized_keyword = str(keyword).strip() or None
    return {"type": normalized_type, "keyword": normalized_keyword}


def encode_cursor(rowid: int, type_filter: str | None, keyword: str | None) -> str:
    """keyset 游标 = base64(JSON ``{"v":1,"rowid":N,"filter":{"type","keyword"}}``)。

    续拉页 ``WHERE rowid > N`` 升序;filter 进游标供 scope 守卫对拍
    (C1 page 同族:防串筛选复用旧游标)。
    """
    payload = {
        "v": _CURSOR_VERSION,
        "rowid": int(rowid),
        "filter": _norm_filter(type_filter, keyword),
    }
    return base64.b64encode(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).decode("ascii")


def decode_cursor(cursor: str, type_filter: str | None, keyword: str | None) -> int:
    """游标解包 + scope 守卫:请求 filter 与游标内不一致 → exit 2 ``invalid_cursor``。

    返回续拉起点 rowid。坏 base64/坏 JSON/形状漂移/版本不识同码拒
    (游标是不透明串,任何不自洽都当串用拒,不猜)。
    """
    try:
        payload = json.loads(base64.b64decode(cursor.encode("ascii"), validate=True))
    except (binascii.Error, ValueError, UnicodeEncodeError):
        raise BridgeError(
            EXIT_USAGE,
            f"游标不可解码(坏 base64/JSON): {cursor[:32]!r}…",
            code="invalid_cursor",
            fix_hint="游标取上一页应答的 next_cursor 原值,不自造",
        ) from None
    if (
        not isinstance(payload, dict)
        or payload.get("v") != _CURSOR_VERSION
        or not isinstance(payload.get("rowid"), int)
        or not isinstance(payload.get("filter"), dict)
    ):
        raise BridgeError(
            EXIT_USAGE,
            "游标形状不识(v/rowid/filter 缺失或类型漂移)",
            code="invalid_cursor",
            fix_hint="游标取上一页应答的 next_cursor 原值,不自造",
        )
    if payload["filter"] != _norm_filter(type_filter, keyword):
        raise BridgeError(
            EXIT_USAGE,
            "游标与当前筛选不一致(串筛选复用旧游标)",
            code="invalid_cursor",
            fix_hint="换筛选时从首页拉起(不带 --cursor),不沿用旧游标",
        )
    return int(payload["rowid"])


def _display_name(row: dict[str, Any]) -> str:
    """显示名链(remark > nick_name > alias > username;空白串跳过)。

    与 ``localdb_query._contact_pick_names`` 同序(strip 判空);真库空值
    以 '' 而非 NULL 在场,裸 COALESCE 会命中空串,故 Python 侧判空实现
    prd R1「COALESCE(remark,nick_name,alias,username) 同序」的语义。
    """
    for key in ("remark", "nick_name", "alias", "username"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return str(row.get("username") or "")


def _table_exists(con: sqlite3.Connection, table: str) -> bool:
    try:
        row = con.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name = ?", (table,)
        ).fetchone()
    except sqlite3.Error:
        return False
    return row is not None


def _bucket_expr(cols: dict[str, str | None]) -> str | None:
    """六桶判定 CASE(实际列名代入;username 缺 = 整库不可判 → None)。

    local_type/nick_name 列缺 → ④⑤臂不可判:未落入 ①②③ 的行判 NULL
    (不入任何桶、不出行不进 counts,``degraded`` 标注——不把 20k 行倒进
    other 冒充分类)。
    """
    username = cols.get("username")
    if username is None:
        return None
    quoted = chr(34) + username + chr(34)
    # 系统号集内联字面量(固定 ASCII 集无引号;CASE 要嵌进子查询/SELECT
    # 多处,占位符形态会漏绑参数,字面量形态单一出处零绑定面)。
    system_literals = ", ".join(f"'{name}'" for name in SYSTEM_USERNAMES)
    arms = [
        f"WHEN {quoted} IN ({system_literals}) THEN 'system'",
        f"WHEN {quoted} LIKE '%@chatroom' THEN 'group'",
        f"WHEN {quoted} LIKE 'gh\\_%' ESCAPE '\\' THEN 'official'",
    ]
    local_type = cols.get("local_type")
    nick = cols.get("nick_name")
    if local_type is not None and nick is not None:
        arms.append(
            f'WHEN "{local_type}" = 3 AND COALESCE("{nick}", \'\') <> \'\' '
            "THEN 'former'"
        )
        arms.append(f'WHEN "{local_type}" = 1 THEN \'friend\'')
        return "CASE " + " ".join(arms) + " ELSE 'other' END"
    # ④⑤臂不可判:未落入 ①②③ 的行判 NULL(不入桶不出行不进 counts,
    # degraded 已由调用方标注——不倒进 other 冒充分类)。
    return "CASE " + " ".join(arms) + " ELSE NULL END"


def _contact_columns(con: sqlite3.Connection) -> dict[str, str | None]:
    """contact 表逻辑列 → 实际列名(PRAGMA 自适应;表缺 = 全 None)。"""
    columns = _columns(con, "contact")
    return {
        "username": _pick(columns, _USERNAME_COLS),
        "nick_name": _pick(columns, _NICKNAME_COLS),
        "remark": _pick(columns, _REMARK_COLS),
        "alias": _pick(columns, _ALIAS_COLS),
        "local_type": _pick(columns, _LOCALTYPE_COLS),
        "quan_pin": _pick(columns, _QUANPIN_COLS),
        "description": _pick(columns, _DESCRIPTION_COLS),
        "flag": _pick(columns, _FLAG_COLS),
    }


def _keyword_clause(
    cols: dict[str, str | None], keyword: str, degraded: list[str]
) -> tuple[str | None, list[str]]:
    """五列 LIKE %K% 子句(纯 SQL;缺列剔除 + degraded 标注)。

    返回 (SQL 片段或 None, 绑定参数表);keyword 通配符字面量化(%/_
    /\\ 转义,配 ESCAPE)防「搜索 % 命中全表」。
    """
    pattern = f"%{_esc(keyword)}%"
    usable: list[str] = []
    for logical in _KEYWORD_COLS:
        actual = cols.get(logical)
        if actual is None:
            degraded.append(f"missing_column:{logical}")
            continue
        usable.append(f'"{actual}" LIKE ? ESCAPE \'\\\'')
    if not usable:
        return None, []
    return "(" + " OR ".join(usable) + ")", [pattern] * len(usable)


def _counts(
    con: sqlite3.Connection, bucket_expr: str, degraded: list[str]
) -> dict[str, int]:
    """六桶全量计数(cheap GROUP BY;counts 恒全量,与 filter 无关)。"""
    counts = {key: 0 for key in _COUNT_KEYS}
    try:
        rows = con.execute(
            f"SELECT bucket, COUNT(*) FROM (SELECT {bucket_expr} AS bucket "
            f'FROM "contact") WHERE bucket IS NOT NULL GROUP BY bucket'
        ).fetchall()
    except sqlite3.Error:
        degraded.append("counts:unreadable")
        return counts
    for bucket, total in rows:
        if isinstance(bucket, str) and bucket in counts:
            counts[bucket] = int(total)
    return counts


def _strict_residual_count(
    con: sqlite3.Connection, cols: dict[str, str | None], degraded: list[str]
) -> int:
    """WeFlow 原式对照诊断(词面转写;人集作用域,见模块 docstring 实测注)。

    ``lt0+quan_pin 或 lt3+flag≠4+(quan_pin/alias/remark)``;缺列 → 可算臂
    照算 + degraded 标注(诊断字段不做静默零)。local_type 缺 = 全式不可
    算,0 + 标注。
    """
    username = cols.get("username")
    local_type = cols.get("local_type")
    if username is None or local_type is None:
        degraded.append("strict_residual_count:missing_column:local_type")
        return 0
    quoted = chr(34) + username + chr(34)
    system_literals = ", ".join(f"'{name}'" for name in SYSTEM_USERNAMES)
    person_scope = (
        f"({quoted} NOT IN ({system_literals}) "
        f"AND {quoted} NOT LIKE '%@chatroom' "
        f"AND {quoted} NOT LIKE 'gh\\_%' ESCAPE '\\')"
    )
    lt0_arm = "0 = 1"
    if cols.get("quan_pin") is not None:
        lt0_arm = (
            f'"{local_type}" = 0 AND COALESCE("{cols["quan_pin"]}", \'\') <> \'\''
        )
    else:
        degraded.append("strict_residual_count:missing_column:quan_pin")
    identity: list[str] = []
    for logical in ("quan_pin", "alias", "remark"):
        actual = cols.get(logical)
        if actual is None:
            degraded.append(f"strict_residual_count:missing_column:{logical}")
            continue
        identity.append(f"COALESCE(\"{actual}\", '') <> ''")
    lt3_identity = "(" + " OR ".join(identity) + ")" if identity else "0 = 1"
    if cols.get("flag") is not None:
        lt3_arm = (
            f'"{local_type}" = 3 AND COALESCE("{cols["flag"]}", 0) <> 4 '
            f"AND {lt3_identity}"
        )
    else:
        degraded.append("strict_residual_count:missing_column:flag")
        lt3_arm = f'"{local_type}" = 3 AND {lt3_identity}'
    try:
        (total,) = con.execute(
            f"SELECT COUNT(*) FROM \"contact\" WHERE {person_scope} "
            f"AND (({lt0_arm}) OR ({lt3_arm}))"
        ).fetchone()
        return int(total)
    except sqlite3.Error:
        degraded.append("strict_residual_count:unreadable")
        return 0


def _labels(con: sqlite3.Connection, degraded: list[str]) -> list[dict[str, object]]:
    """contact_label → ``[{"id","name"}]``(标签只呈清单不做逐人关联——归属在
    extra_buffer(opaque)内,实测无关联列,诚实不臆造)。"""
    if not _table_exists(con, "contact_label"):
        degraded.append("missing_table:contact_label")
        return []
    columns = _columns(con, "contact_label")
    id_col = _pick(columns, ("label_id_", "label_id", "id"))
    name_col = _pick(columns, ("label_name_", "label_name", "name"))
    if id_col is None or name_col is None:
        degraded.append("missing_column:contact_label")
        return []
    try:
        rows = con.execute(
            f'SELECT "{id_col}", "{name_col}" FROM "contact_label" ORDER BY "{id_col}"'
        ).fetchall()
    except sqlite3.Error:
        degraded.append("labels:unreadable")
        return []
    return [
        {"id": int(row[0]), "name": row[1] if isinstance(row[1], str) else ""}
        for row in rows
    ]


def _stranger_rows(
    con: sqlite3.Connection, degraded: list[str]
) -> list[dict[str, object]]:
    """stranger 表原样小数组(与 contact 同列集,实测 3 行;独立子卡语义
    「非好友联系人缓存」,**不混入 former 计数**)。"""
    if not _table_exists(con, "stranger"):
        degraded.append("missing_table:stranger")
        return []
    stranger_columns = _columns(con, "stranger")
    cols = {"username": _pick(stranger_columns, _USERNAME_COLS)}
    for logical, candidates in (
        ("nick_name", _NICKNAME_COLS),
        ("remark", _REMARK_COLS),
        ("alias", _ALIAS_COLS),
        ("local_type", _LOCALTYPE_COLS),
    ):
        cols[logical] = _pick(stranger_columns, candidates)
    if cols["username"] is None:
        degraded.append("missing_column:stranger.username")
        return []
    selects = [f'"{cols["username"]}"']
    for logical in ("remark", "nick_name", "alias", "local_type"):
        selects.append(f'"{cols[logical]}"' if cols[logical] else "NULL")
    try:
        rows = con.execute(f'SELECT {", ".join(selects)} FROM "stranger"').fetchall()
    except sqlite3.Error:
        degraded.append("stranger:unreadable")
        return []
    out: list[dict[str, object]] = []
    for username, remark, nick, alias, local_type in rows:
        if not isinstance(username, str) or not username:
            continue
        out.append(
            {
                "username": username,
                "display_name": _display_name(
                    {
                        "remark": remark,
                        "nick_name": nick,
                        "alias": alias,
                        "username": username,
                    }
                ),
                "local_type": int(local_type) if isinstance(local_type, int) else None,
                "remark": remark if isinstance(remark, str) else "",
            }
        )
    return out


def _room_verify(con: sqlite3.Connection, degraded: list[str]) -> dict[str, object]:
    """room_verify_application:存在性 + 行数;行数>0 附前 100 行四列直读。

    语义标「推断:群验证/入群申请」(greenbubbles 无释义);``data_json``
    blob 原样字符串不解析(诚实契约)。本机实测 0 行 → present=true rows=0。
    """
    info: dict[str, object] = {"present": False, "rows": 0}
    if not _table_exists(con, "room_verify_application"):
        degraded.append("missing_table:room_verify_application")
        return info
    info["present"] = True
    columns = _columns(con, "room_verify_application")
    needed = {
        key: _pick(columns, (key,))
        for key in ("chatroom_name", "inviter_username", "state", "update_time")
    }
    if any(actual is None for actual in needed.values()):
        degraded.append("missing_column:room_verify_application")
        return info
    try:
        (total,) = con.execute(
            'SELECT COUNT(*) FROM "room_verify_application"'
        ).fetchone()
        info["rows"] = int(total)
        if total > 0:
            quoted = ", ".join(f'"{col}"' for col in needed.values())
            sample = con.execute(
                f'SELECT {quoted} FROM "room_verify_application" ORDER BY rowid LIMIT 100'
            ).fetchall()
            info["sample"] = [
                {
                    "chatroom_name": row[0] if isinstance(row[0], str) else None,
                    "inviter_username": row[1] if isinstance(row[1], str) else None,
                    "state": row[2],
                    "update_time": row[3],
                }
                for row in sample
            ]
    except sqlite3.Error:
        degraded.append("room_verify:unreadable")
    return info


def _group_member_counts(
    con: sqlite3.Connection, usernames: list[str]
) -> dict[str, int]:
    """群聊行 member_count(chat_room.username → id → chatroom_member 计数;
    判例 ``_chatroom_member_ids`` 同表关联;缺表/缺列 = 0 如实)。"""
    if not usernames:
        return {}
    if not (_table_exists(con, "chat_room") and _table_exists(con, "chatroom_member")):
        return {}
    room_columns = _columns(con, "chat_room")
    id_col = _pick(room_columns, ("id",))
    username_col = _pick(room_columns, _USERNAME_COLS)
    member_columns = _columns(con, "chatroom_member")
    room_id_col = _pick(member_columns, ("room_id",))
    if not (id_col and username_col and room_id_col):
        return {}
    marks = ", ".join("?" for _ in usernames)
    try:
        rooms = con.execute(
            f'SELECT "{username_col}", "{id_col}" FROM "chat_room" '
            f"WHERE \"{username_col}\" IN ({marks})",
            usernames,
        ).fetchall()
        if not rooms:
            return {}
        room_ids = [room_id for _username, room_id in rooms]
        id_marks = ", ".join("?" for _ in room_ids)
        counts = con.execute(
            f'SELECT "{room_id_col}", COUNT(*) FROM "chatroom_member" '
            f"WHERE \"{room_id_col}\" IN ({id_marks}) GROUP BY \"{room_id_col}\"",
            room_ids,
        ).fetchall()
    except sqlite3.Error:
        return {}
    by_room = {room_id: int(total) for room_id, total in counts}
    return {username: by_room.get(room_id, 0) for username, room_id in rooms}


def _residue_usernames(copy_dir: Path) -> set[str] | None:
    """Tier A 依据:message_0.db ``Name2Id.user_name`` 集合(行读取复用
    :func:`localdb_query.name2id_maps`;不扫 Msg_ 表——表已删,映射残留
    即证据)。副本缺/表缺 = None(残留检查未发生,如实)。"""
    con = _open_copy(copy_dir, "message/message_0.db")
    if con is None:
        return None
    try:
        id_to_name, _md5_to_name = name2id_maps(con)
    finally:
        con.close()
    if not id_to_name:
        return None
    return set(id_to_name.values())


def _former_candidates(
    con: sqlite3.Connection, bucket_expr: str
) -> set[str]:
    """former 候选全集(username 集;Tier 计数与逐行 evidence 共用)。"""
    try:
        rows = con.execute(
            f"SELECT \"username\" FROM \"contact\" WHERE {bucket_expr} = 'former'"
        ).fetchall()
    except sqlite3.Error:
        return set()
    return {row[0] for row in rows if isinstance(row[0], str) and row[0]}


def contacts_page(
    copy_dir: Path,
    *,
    type_filter: str | None = None,
    keyword: str | None = None,
    limit: int | None = LIMIT_DEFAULT,
    cursor: str | None = None,
    with_residue: bool = False,
    include_stranger: bool = True,
) -> dict[str, object]:
    """``localdb contacts`` 查询本体 → ``{"contacts": {…}}`` 契约载荷。

    键序 = prd R1 应答契约原文序(counts → former_tiers → residue_checked
    → strict_residual_count → labels → stranger → room_verify → rows →
    next_cursor → has_more → filter → page_size),尾部附加 ``degraded``
    诊断标注(缺表/缺列清单;恒在场,健康时空数组——R1「诊断字段标注」
    的承载位)。行序 = 库序(rowid 升序,v1 不承诺时间序,prd 边界注记)。

    分页:keyset 游标(base64 JSON ``{"v":1,"rowid",filter}``),scope 守卫
    不一致 → exit 2 ``invalid_cursor``(BridgeError);``limit=0`` = 全量
    导出态(帽豁免,has_more 恒 false、next_cursor 恒 null)。counts 恒
    全量六桶(与 filter 无关);行内 ``type`` 直取 SQL 判定列(判定序单一
    出处,不做 Python 侧二次推导)。
    """
    normalized = _norm_filter(type_filter, keyword)
    effective_type = normalized["type"]
    effective_keyword = normalized["keyword"]
    degraded: list[str] = []

    start_rowid = 0
    if cursor is not None:
        start_rowid = decode_cursor(cursor, effective_type, effective_keyword)

    page_size = LIMIT_DEFAULT if limit is None else int(limit)
    if page_size < 0:
        raise BridgeError(
            EXIT_USAGE,
            f"limit 须为非负整数(0 = 全量导出态),当前为 {page_size}",
            code="usage",
        )

    contact_con = _open_copy(copy_dir, "contact/contact.db")
    counts = {key: 0 for key in _COUNT_KEYS}
    rows_out: list[dict[str, object]] = []
    former_tiers: dict[str, int] | None = None
    residue_checked = False
    strict_residual_count = 0
    labels: list[dict[str, object]] = []
    stranger: list[dict[str, object]] = []
    room_verify: dict[str, object] = {"present": False, "rows": 0}
    next_cursor: str | None = None
    has_more = False

    if contact_con is not None:
        try:
            cols = _contact_columns(contact_con)
            bucket_expr = _bucket_expr(cols)
            if bucket_expr is None:
                degraded.append("missing_column:username")
                if "local_type" in cols and cols.get("local_type") is None:
                    degraded.append("missing_column:local_type")
            else:
                if cols.get("local_type") is None or cols.get("nick_name") is None:
                    degraded.append("missing_column:local_type")
                counts = _counts(contact_con, bucket_expr, degraded)
                strict_residual_count = _strict_residual_count(
                    contact_con, cols, degraded
                )
                rows_out, next_cursor, has_more = _rows_page(
                    contact_con,
                    cols,
                    bucket_expr,
                    effective_type,
                    effective_keyword,
                    start_rowid,
                    page_size,
                    with_residue,
                    degraded,
                )
                # —— R2 考古分层(Tier A 需 message 域;--with-residue 才触发)——
                residue_names: set[str] | None = None
                if with_residue:
                    residue_names = _residue_usernames(copy_dir)
                    if residue_names is None:
                        degraded.append("missing_copy:message")
                    else:
                        candidates = _former_candidates(contact_con, bucket_expr)
                        tier_a = candidates & residue_names
                        former_tiers = {
                            "msg_residue": len(tier_a),
                            "table_only": len(candidates) - len(tier_a),
                        }
                        _stamp_row_evidence(
                            rows_out, residue_names, candidates
                        )
                residue_checked = residue_names is not None
            labels = _labels(contact_con, degraded)
            if include_stranger:
                stranger = _stranger_rows(contact_con, degraded)
            room_verify = _room_verify(contact_con, degraded)
        finally:
            contact_con.close()

    return {
        "contacts": {
            "counts": counts,
            "former_tiers": former_tiers,
            "residue_checked": residue_checked,
            "strict_residual_count": strict_residual_count,
            "labels": labels,
            "stranger": stranger,
            "room_verify": room_verify,
            "rows": rows_out,
            "next_cursor": next_cursor,
            "has_more": has_more,
            "filter": {
                "type": effective_type,
                "keyword": effective_keyword,
                "with_residue": bool(with_residue),
                "include_stranger": bool(include_stranger),
            },
            "page_size": page_size,
            "degraded": degraded,
        }
    }


def _rows_page(
    con: sqlite3.Connection,
    cols: dict[str, str | None],
    bucket_expr: str,
    effective_type: str | None,
    effective_keyword: str | None,
    start_rowid: int,
    page_size: int,
    with_residue: bool,
    degraded: list[str],
) -> tuple[list[dict[str, object]], str | None, bool]:
    """行页拉取 + 行组装(keyset rowid 升序;system 恒不出行)。

    ``with_residue`` 只用来**预取** evidence 所需列的语义提示(列集恒含
    quan_pin——identity_fields 是 contact 域本地事实,无 residue 也照算);
    msg_residue 位由调用方在拿到 Name2Id 集后经 :func:`_stamp_row_evidence`
    盖章。返回 (rows, next_cursor, has_more)。
    """
    del with_residue  # evidence 列集恒定,不随 residue 扩列(见 docstring)
    selects = ["rowid AS \"_rowid\"", f"{bucket_expr} AS \"_bucket\""]
    for logical in (
        "username",
        "remark",
        "nick_name",
        "alias",
        "local_type",
        "description",
        "quan_pin",
    ):
        actual = cols.get(logical)
        selects.append(f'"{actual}"' if actual else "NULL")
    if effective_type is not None:
        bucket_condition = f"{bucket_expr} = '{effective_type}'"
    else:
        bucket_in = ", ".join(f"'{bucket}'" for bucket in TYPE_FILTERS)
        bucket_condition = f"{bucket_expr} IN ({bucket_in})"
    conditions = [bucket_condition]
    params: list[Any] = []
    if effective_keyword is not None:
        clause, like_params = _keyword_clause(cols, effective_keyword, degraded)
        if clause is not None:
            conditions.append(clause)
            params.extend(like_params)
    conditions.append("rowid > ?")
    params.append(start_rowid)
    sql = (
        f'SELECT {", ".join(selects)} FROM "contact" '
        f"WHERE {' AND '.join(conditions)} ORDER BY rowid ASC"
    )
    if page_size > 0:
        sql += f" LIMIT {page_size + 1}"
    try:
        fetched = con.execute(sql, params).fetchall()
    except sqlite3.Error:
        degraded.append("rows:unreadable")
        fetched = []
    has_more = page_size > 0 and len(fetched) > page_size
    if has_more:
        fetched = fetched[:page_size]

    raw_rows = [
        {
            "_rowid": row[0],
            "bucket": row[1],
            "username": row[2],
            "remark": row[3],
            "nick_name": row[4],
            "alias": row[5],
            "local_type": row[6],
            "description": row[7],
            "quan_pin": row[8],
        }
        for row in fetched
    ]

    group_usernames = [
        row["username"]
        for row in raw_rows
        if row["bucket"] == "group" and isinstance(row["username"], str)
    ]
    member_counts = _group_member_counts(con, group_usernames)

    rows_out: list[dict[str, object]] = []
    for raw in raw_rows:
        username = raw["username"]
        safe_username = username if isinstance(username, str) else ""
        bucket = raw["bucket"] if isinstance(raw["bucket"], str) else "other"
        # identity_fields:former 候选行 quan_pin/alias/remark 任一非空
        # (contact 域本地事实,无 --with-residue 也照算;WeFlow 式附加证据位)
        evidence: list[str] = []
        if bucket == "former" and any(
            isinstance(raw[key], str) and raw[key] != ""
            for key in ("quan_pin", "alias", "remark")
        ):
            evidence.append("identity_fields")
        entry: dict[str, object] = {
            "username": safe_username,
            "display_name": _display_name(raw),
            "remark": raw["remark"] if isinstance(raw["remark"], str) else "",
            "nickname": raw["nick_name"] if isinstance(raw["nick_name"], str) else "",
            "alias": raw["alias"] if isinstance(raw["alias"], str) else "",
            "type": bucket,
            "local_type": raw["local_type"]
            if isinstance(raw["local_type"], int)
            else None,
            "evidence": evidence,
            "description": raw["description"]
            if isinstance(raw["description"], str) and raw["description"].strip()
            else None,
        }
        if bucket == "group":
            entry["member_count"] = member_counts.get(safe_username, 0)
        rows_out.append(entry)

    next_cursor: str | None = None
    if has_more and raw_rows:
        next_cursor = encode_cursor(
            int(raw_rows[-1]["_rowid"]), effective_type, effective_keyword
        )
    return rows_out, next_cursor, has_more


def _stamp_row_evidence(
    rows: list[dict[str, object]],
    residue_names: set[str],
    candidates: set[str],
) -> None:
    """Tier A 盖章(原地):former 行 username ∈ Name2Id 集合 → evidence
    头部插 ``msg_residue``(顺序:msg_residue 在前、identity_fields 在后;
    仅 former 候选盖章,非候选行不沾)。"""
    for entry in rows:
        if entry.get("type") != "former":
            continue
        username = entry.get("username")
        if not isinstance(username, str) or username not in candidates:
            continue
        evidence = entry.get("evidence")
        evidence_list = list(evidence) if isinstance(evidence, list) else []
        if username in residue_names and "msg_residue" not in evidence_list:
            evidence_list.insert(0, "msg_residue")
        entry["evidence"] = evidence_list
