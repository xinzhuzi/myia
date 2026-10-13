"""E3 朋友圈域只读查询(task 10-13-wechat-sns-feed;design §2.3/§2.4)。

对**解密副本**(数据根私有区,``localdb.ensure_decrypted_copies`` 产物,
domains=["sns","contact"])做纯只读查询,两模式:

- **feed**(`SnsTimeLine`):content 列是一段微信自家序列化 XML
  (``SnsDataItem/TimelineObject``;2026-10-13 实探 4408 行形状)。全表
  拉取后逐行 ``xml.etree.ElementTree`` 解析(stdlib;估算亚秒级,实现时
  实测——超 2s 再上 createTime 正则前置过滤,见 design §2.3)。**解析
  失败不炸整轮**:坏行/必要字段缺失 → 弃行 + ``parse_errors`` 计数
  (宁缺毋假)。**media type 数字语义不臆造**(2=图/4=视频未实证):
  ``media_types`` 原样透传,标题回退不依赖它(design grill 决议)。
- **notices**(`SnsMessage_tmp3`):互动通知,窗口过滤在 SQL 层
  (``create_time`` 是真列)。type 映射 ``1→like``/``2→comment``/其余
  原样数字字符串;``is_relative_me`` 原样透传(**通知不全是「对我的
  动态」**——含好友间互动,消费方词面不假设归属)。

表名漂移(prd 红线 7 同源):v1 直查两张表名,缺表 = 结构化
``db_not_found`` 如实报(微信版本形状变化不猜,发现式查询是过度设计,
design §5)。

私有数据红线(prd 红线 6 同款):查询结果 = CLI stdout 契约载荷,不入
日志、不入 git;错误消息只承载形状计数。
"""

from __future__ import annotations

import sqlite3
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from .codes import DB_NOT_FOUND, DECRYPT_FAILED, BridgeError
from .localdb_query import _contact_pick_names, _open_copy

__all__ = ["run_sns_query", "parse_feed_row", "NOTICE_TYPE_NAMES"]

#: 动态表(2026-10-13 实探:tid/user_name/content/pack_info_buf 四列,
#: content = XML;SQL 层无时间列,窗口过滤在解析后)。
FEED_TABLE = "SnsTimeLine"
#: 互动通知表(tmp3 后缀疑似版本产物;缺表如实报,见模块 docstring)。
NOTICES_TABLE = "SnsMessage_tmp3"

#: 通知 type → 词面(实探:1=赞 182 条 content 恒空;2=评论 67 条
#: content=评论文本;未知类型原样数字字符串,不臆造)。
NOTICE_TYPE_NAMES: dict[int, str] = {1: "like", 2: "comment"}

#: is_relative_me 语义注记:真跑 3 条赞全 0(语义未实证——可能不是
#: 「与我相关」的简单布尔),**原样透传不解释**;消费方词面中性不依赖它。


def _text_of(element: ET.Element | None) -> str | None:
    """元素文本(去首尾空白;缺失/空 = None;不臆造)。"""
    if element is None or element.text is None:
        return None
    stripped = element.text.strip()
    return stripped or None


def parse_feed_row(content: object) -> dict[str, object] | None:
    """一行 SnsTimeLine.content(XML)→ 载荷行;解析不干净 = None(弃行计错).

    契约字段(design §2.3 表):id/username/create_time 必备(缺失即弃),
    text/media/ref_username/ref_nickname 可选。media = ContentObject/
    mediaList/media 列表,每条取 type 文本(media type 数字语义不臆造,
    原样透传)。
    """
    if not isinstance(content, str) or not content.strip():
        return None
    try:
        root = ET.fromstring(content)
    except ET.ParseError:
        return None
    timeline = root.find("TimelineObject")
    if timeline is None:
        return None
    entry_id = _text_of(timeline.find("id"))
    username = _text_of(timeline.find("username"))
    create_time_raw = _text_of(timeline.find("createTime"))
    if not entry_id or not username or create_time_raw is None:
        return None
    try:
        create_time = int(create_time_raw)
    except ValueError:
        return None
    media_types: list[str] = []
    media_list = timeline.find("ContentObject/mediaList")
    if media_list is not None:
        for media in media_list.findall("media"):
            media_type = _text_of(media.find("type"))
            if media_type is not None:
                media_types.append(media_type)
    return {
        "id": entry_id,
        "username": username,
        "nickname": None,  # 编排层 contact 反查回填
        "create_time": create_time,
        "text": _text_of(timeline.find("contentDesc")),
        "media_count": len(media_types),
        "media_types": media_types,
        "ref_username": _text_of(timeline.find("sourceUserName")),
        "ref_nickname": _text_of(timeline.find("sourceNickName")),
    }


def _sns_copy_error(rel: str) -> BridgeError:
    """sns 域副本不可用的结构化错误(message 域同款语义;design §2.4)."""
    return BridgeError(
        DECRYPT_FAILED,
        f"sns 域解密副本不可用(副本缺失或损坏;G5 重建流程未产出可用库): {rel}",
        fix_hint="重跑 localdb sns 命令触发副本重建;持续失败先核密钥与 sqlcipher",
    )


def _table_exists(con: sqlite3.Connection, table: str) -> bool:
    try:
        row = con.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone()
    except sqlite3.Error:
        return False
    return row is not None


def run_sns_query(
    *,
    copy_dir: Path,
    mode: str,
    since_days: int,
    copy_info: dict[str, object],
) -> dict[str, object]:
    """sns 查询编排(feed|notices;design §2.4 载荷契约,键序稳定).

    feed:SnsTimeLine 全表 → 逐行 XML 解析 → createTime 窗口过滤(Python
    层,SQL 无时间列)→ contact 域批量反查 nickname(缺域/未解出 = None
    如实,消费方回落 username)。notices:SnsMessage_tmp3 SQL 直查(窗口
    在 WHERE)。两模式共用 domains 状态节与 copy 原样节。
    """
    domain_status = {
        "sns": "ok" if (copy_dir / "sns" / "sns.db").is_file() else "copy_missing",
        "contact": "ok"
        if (copy_dir / "contact" / "contact.db").is_file()
        else "copy_missing",
    }
    con = _open_copy(copy_dir, "sns/sns.db")
    if con is None:
        raise _sns_copy_error("sns/sns.db")
    since_ts = int(time.time()) - since_days * 86400
    try:
        if mode == "feed":
            payload = _query_feed(con, since_ts, since_days, copy_dir)
        else:
            payload = _query_notices(con, since_ts, since_days)
    finally:
        con.close()
    payload["domains"] = domain_status
    payload["copy"] = copy_info
    return {"sns": payload}


def _query_feed(
    con: sqlite3.Connection, since_ts: int, since_days: int, copy_dir: Path
) -> dict[str, object]:
    """feed 模式:全表拉取 → XML 解析 → 窗口过滤 → 升序返回(§2.3).

    nickname 回填:contact 域批量反查(remark > nickname > alias,
    ``_contact_pick_names`` 复用);contact 域缺位/未解出 = None 如实,
    消费方回落 username。
    """
    if not _table_exists(con, FEED_TABLE):
        raise BridgeError(
            DB_NOT_FOUND,
            f"sns 副本缺 {FEED_TABLE} 表(微信版本形状漂移;2026-10-13 实探形状失配)",
            fix_hint="微信升级可能改表名;重登/升级后重试,持续缺失报 issue 附版本号",
        )
    rows = con.execute(
        f'SELECT user_name, content FROM "{FEED_TABLE}"'
    ).fetchall()
    feed: list[dict[str, object]] = []
    parse_errors = 0
    out_of_window = 0
    for _user_name, content in rows:
        entry = parse_feed_row(content)
        if entry is None:
            parse_errors += 1
            continue
        if int(entry["create_time"]) < since_ts:
            out_of_window += 1
            continue
        feed.append(entry)
    feed.sort(key=lambda item: int(item["create_time"]))
    contact_con = _open_copy(copy_dir, "contact/contact.db")
    if contact_con is not None:
        try:
            names = _contact_pick_names(
                contact_con,
                [str(item["username"]) for item in feed],
            )
            for item in feed:
                nickname = names.get(str(item["username"]))
                if nickname:
                    item["nickname"] = nickname
        finally:
            contact_con.close()
    return {
        "mode": "feed",
        "since_days": since_days,
        "feed": feed,
        "rows_total": len(rows),
        "rows_out_of_window": out_of_window,
        "parse_errors": parse_errors,
    }


def _query_notices(
    con: sqlite3.Connection, since_ts: int, since_days: int
) -> dict[str, object]:
    """notices 模式:SQL 直查(窗口在 WHERE;type 映射+is_relative_me 透传)."""
    if not _table_exists(con, NOTICES_TABLE):
        raise BridgeError(
            DB_NOT_FOUND,
            f"sns 副本缺 {NOTICES_TABLE} 表(微信版本形状漂移;tmp3 后缀疑似版本产物)",
            fix_hint="微信升级可能改表名;重登/升级后重试,持续缺失报 issue 附版本号",
        )
    rows = con.execute(
        f'SELECT local_id, create_time, type, from_username, from_nickname, '
        f'feed_id, content, is_relative_me FROM "{NOTICES_TABLE}" '
        f"WHERE create_time >= ? ORDER BY create_time ASC",
        (since_ts,),
    ).fetchall()
    notices: list[dict[str, object]] = []
    for local_id, create_time, notice_type, from_user, from_nick, feed_id, content, relative in rows:
        try:
            type_name = NOTICE_TYPE_NAMES.get(int(notice_type), str(notice_type))
        except (TypeError, ValueError):
            type_name = str(notice_type)
        notices.append(
            {
                "local_id": local_id,
                "create_time": int(create_time or 0),
                "type": type_name,
                "from_username": from_user if isinstance(from_user, str) else None,
                "from_nickname": from_nick if isinstance(from_nick, str) else None,
                # feed_id 列是 INTEGER(雪花 id;实测非字符串)——统一转 str
                # 入载荷(消费方零类型分叉),None 原样。
                "feed_id": str(feed_id) if feed_id is not None else None,
                "content": content if isinstance(content, str) and content.strip() else None,
                "is_relative_me": relative,
            }
        )
    return {
        "mode": "notices",
        "since_days": since_days,
        "notices": notices,
        "rows_total": len(rows),
        "parse_errors": 0,
    }
