"""send_text 的 DB 侧目标解析 + 搜索词选择(task 10-14-wechat-send-text
design §B-1;红线 2 的「发送前 DB 侧验证」落点)。

职责:把 ``send_text <id>`` 的 id 三形态(username 真源 / alias / 展示名
或备注名)统一解析到 :class:`SendTarget`(username 真源 + 展示名 + 搜索
词 + 指纹件),并派生导航与防重所需的全部词表——**查无/多义都在任何
UI 扰动之前拒发**(exit 1 具名 code,零激活零点击)。

输入面声明(既有输入零破坏):sessions list 契约的 id 本就是展示名
(pixel.py SessionRow.to_payload ``"id": self.name``),「文件传输助手」
「🐳」直接可用;alias(wxid 之外的微信号)与 username(wxid_…/
filehelper/gh_…/@chatroom)同受。

三路命中集统一唯一性判据(design §J-21:任何一路多行命中都送
ambiguous,绝不静默取首行=潜在错发):

- 路① username 正查(SQL 精确等值;username 本就是唯一键,多行视同库
  异常 → ambiguous 如实);
- 路② alias 反查(SQL 等值拉**全部**命中行;不取首行);
- 路③ 展示名反查——**SQL 只做全量拉取、Python 侧比对**(compact() 是
  Python 函数进不了 sqlite WHERE;ASCII 名 sqlite 默认 BINARY collation
  不折叠大小写,伪 SQL 不可执行,design §J-21):
  ``SELECT <id>,<alias>,<remark>,<nick_name> FROM contact`` 全量(千行级)
  → Python 侧 ``compact(remark)==compact(chat_id) or
  compact(nick_name)==compact(chat_id)``(去空白 + casefold)。

display_name 取 remark > nick_name > alias(localdb_query.
_contact_pick_names 同序)。**不查 stranger 表**:靶场实证两白名单目标
均无 stranger 行,contact 表是白名单目标的真源(如实边界)。

storage/keys 注入(design §J-19):CLI 在 send 分支单次解析
``locate_db_storage`` + ``resolve_keys`` 后注入本模块与回执闭包——取钥
器交互/自愈链全程至多一次;缺省自解析仅供单测/复用。

依赖方向(design §A):sendtarget → localdb/localdb_query。
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .codes import EXIT_GENERIC_FAILURE, BridgeError
from .navfilter import compact as _compact

__all__ = [
    "CONTACT_REL",
    "SendTarget",
    "fingerprint",
    "pick_search_term",
    "resolve_target",
    "row_match_terms",
]

#: contact 域副本相对路径(localdb_query.run_query 的 rel_map 同款)。
CONTACT_REL = "contact/contact.db"

_WXID_PREFIX = "wxid_"


@dataclass(frozen=True)
class SendTarget:
    """解析后的发送目标(username 真源 + 展示名 + 搜索词;design §B-1)。"""

    username: str
    alias: str | None
    display_name: str
    search_term: str


def _is_ascii(text: str) -> bool:
    return all(ord(ch) < 128 for ch in text)


def _is_pure_emoji(text: str) -> bool:
    """名字是否纯 emoji/符号(无字母数字,CJK 计字母)——🐳 类。"""
    return not any(ch.isalnum() for ch in text)


def pick_search_term(username: str, alias: str | None, display_name: str) -> str:
    """搜索词选择(确定性四档;2026-10-14 主人判例:**中文优先**——
    搜索框里敲给人看的中文名,filehelper/jiangliushi666 等机器名不再上屏)。

    1. display_name 非空且非纯 emoji → display_name(主人令:搜索用中文);
    2. elif alias 非空、纯 ASCII、长度 ≥3 → alias(纯 emoji 名走此路,
       行匹配仍以 display_name 为主——design §D-3 不变);
    3. elif username 纯 ASCII 且不以 ``wxid_`` 开头(filehelper/gh_ 公众号)
       → username;
    4. else → username。
    """
    if display_name and not _is_pure_emoji(display_name):
        return display_name
    if alias and _is_ascii(alias) and len(alias) >= 3:
        return alias
    if _is_ascii(username) and not username.startswith(_WXID_PREFIX):
        return username
    return username


def row_match_terms(target: SendTarget) -> list[str]:
    """OCR/AX 行匹配词表(去空去重,顺序即优先级;design §B-1)。

    搜索结果行显示的是 display_name 不显示搜索词,故 display_name 在首;
    alias 兜「微信号:alias」副文本;username 兜 wxid 直显形态。
    """
    terms: list[str] = []
    for candidate in (target.display_name, target.search_term, target.alias or "", target.username):
        compacted = (candidate or "").strip()
        if compacted and compacted not in terms:
            terms.append(compacted)
    return terms


def fingerprint(target: SendTarget, body: str) -> str:
    """防重指纹:sha256(username + "\\0" + body) hex(WZ:138-141 同构)。

    键用解析后 username——同一人 alias/wxid/展示名三种叫法指纹相同,
    防重闭合(design §1-5)。
    """
    digest = hashlib.sha256(
        (target.username + "\0" + body).encode("utf-8")
    )
    return digest.hexdigest()


def _resolve_chain(
    config: Any,
    storage: Path | None,
    keys: dict[str, str] | None,
    data_root: Path | None,
) -> Path:
    """localdb 链:E2 contact 副本目录(注入则零重复解析;design §J-19)。

    缺省自跑 locate → resolve → ensure(与 ``localdb query`` 同链);链上
   任何 BridgeError(20/21/22 族)原样透传、码不变,消息注记阶段=「发送前
    目标解析」——链失败 = 拒发(红线 2:DB 侧验证是发送前置)。
    """
    from . import localdb, localdb_query  # noqa: F401 - _open_copy 惯例同源

    try:
        db_storage = storage if storage is not None else localdb.locate_db_storage()
        mapping = keys if keys is not None else localdb.resolve_keys(
            db_storage, config=config
        )
        copy_info = localdb.ensure_decrypted_copies(
            db_storage,
            mapping,
            domains=["contact"],
            ttl_hours=config.copy_ttl_hours,
            capacity_mb=config.copy_capacity_mb,
            data_root=data_root,
        )
    except BridgeError as exc:
        raise BridgeError(
            exc.exit_code,
            f"发送前目标解析:{exc.message}",
            code=exc.code,
            fix_hint=(exc.fix_hint or "") + ";密钥侧可先跑 wechat-bridge localdb key-acquire",
            retry_after_seconds=exc.retry_after_seconds,
        ) from exc
    return Path(str(copy_info["dir"]))


def _contact_tables(con: sqlite3.Connection) -> list[tuple[str, dict[str, str]]]:
    """contact 表发现 + 列名自适应(localdb_query._columns/_pick 惯例)。"""
    from .localdb_query import _columns, _pick

    tables: list[tuple[str, dict[str, str]]] = []
    try:
        names = [
            row[0]
            for row in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        ]
    except sqlite3.Error:
        return tables
    for table in names:
        if "contact" not in table.lower():
            continue
        columns = _columns(con, table)
        id_col = _pick(columns, ("username", "userName", "UserName", "user_name"))
        if id_col is None:
            continue
        colmap = {"id": id_col}
        for key, candidates in (
            ("alias", ("alias", "Alias")),
            ("remark", ("remark", "Remark", "conRemark")),
            ("nick", ("nick_name", "nickname", "nickName", "NickName")),
        ):
            colmap[key] = _pick(columns, candidates) or ""
        tables.append((table, colmap))
    return tables


def _quote(name: str) -> str:
    return '"' + name + '"'


def _fetch_rows(
    con: sqlite3.Connection,
    table: str,
    colmap: dict[str, str],
    where: str | None = None,
    param: str | None = None,
) -> list[tuple[str, str | None, str | None, str | None]]:
    """拉 (username, alias, remark, nick) 行;SQL 错误 → 空(如实降级)。"""
    cols = ", ".join(
        _quote(colmap[key]) if colmap[key] else "NULL"
        for key in ("id", "alias", "remark", "nick")
    )
    sql = f"SELECT {cols} FROM {_quote(table)}"
    if where is not None:
        sql += f" WHERE {where}"
    try:
        rows = con.execute(sql, (param,) if param is not None else ()).fetchall()
    except sqlite3.Error:
        return []
    result: list[tuple[str, str | None, str | None, str | None]] = []
    for row in rows:
        username = row[0]
        if not isinstance(username, str) or not username.strip():
            continue

        def _text(value: Any) -> str | None:
            return value.strip() if isinstance(value, str) and value.strip() else None

        result.append((_text(username), _text(row[1]), _text(row[2]), _text(row[3])))
    return result


def _display_of(row: tuple[str, str | None, str | None, str | None]) -> str:
    """display_name 取 remark > nick_name > alias(_contact_pick_names 同序)。"""
    alias, remark, nick = row[1], row[2], row[3]
    return remark or nick or alias or row[0]


def resolve_target(
    config: Any,
    chat_id: str,
    *,
    storage: Path | None = None,
    keys: dict[str, str] | None = None,
    data_root: Path | None = None,
) -> SendTarget | None:
    """三形态 id → :class:`SendTarget`(design §B-1)。

    Args:
        config: BridgeConfig(链参数;鸭子类型避免循环导入)。
        chat_id: 原样入参(username / alias / 展示名或备注名)。
        storage: CLI 单次解析注入的 db_storage(注入则不自解析)。
        keys: CLI 单次解析注入的密钥映射(同上)。
        data_root: 数据根覆写(单测隔离)。

    Returns:
        恰 1 命中 → SendTarget;0 命中 → None(调用方 exit 1
        ``send_target_not_found``)。

    Raises:
        BridgeError: exit 1 ``send_target_ambiguous``(三路命中合集 >1,
        绝不静默取首行)/ localdb 链 20/21/22 族透传(消息注记阶段)。
    """
    from .localdb_query import _open_copy

    copy_dir = _resolve_chain(config, storage, keys, data_root)
    con = _open_copy(copy_dir, CONTACT_REL)
    if con is None:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "发送前目标解析:contact 域解密副本不可用(副本缺失或损坏)",
            code="send_target_not_found",
            fix_hint="重跑一次触发副本重建;持续失败核密钥(localdb key-acquire)",
        )
    try:
        wanted = chat_id.strip()
        hits: dict[str, tuple[str, str | None, str | None, str | None]] = {}
        for table, colmap in _contact_tables(con):
            # 路① username 正查(唯一键;多行 = 库异常 → 计入命中集送判据)
            if colmap["id"]:
                for row in _fetch_rows(con, table, colmap, f"{_quote(colmap['id'])} = ?", wanted):
                    hits.setdefault(row[0], row)
            # 路② alias 反查(SQL 等值拉全部命中行,不取首行)
            if colmap["alias"]:
                for row in _fetch_rows(con, table, colmap, f"{_quote(colmap['alias'])} = ?", wanted):
                    hits.setdefault(row[0], row)
            # 路③ 展示名反查:SQL 全量拉取 + Python compact 比对
            for row in _fetch_rows(con, table, colmap):
                _alias, remark, nick = row[1], row[2], row[3]
                if (remark is not None and _compact(remark) == _compact(wanted)) or (
                    nick is not None and _compact(nick) == _compact(wanted)
                ):
                    hits.setdefault(row[0], row)
    finally:
        con.close()

    if not hits:
        return None
    if len(hits) > 1:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"命中多个联系人(chat_id={chat_id},共 {len(hits)} 个)",
            code="send_target_ambiguous",
            fix_hint="改用 alias 或 username(wxid)消歧;localdb query 可先验目标",
        )
    row = next(iter(hits.values()))
    username, alias = row[0], row[1]
    display_name = _display_of(row)
    return SendTarget(
        username=username,
        alias=alias,
        display_name=display_name,
        search_term=pick_search_term(username, alias, display_name),
    )
