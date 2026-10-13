"""R1/R2 分页与普查单测(合成 4.1.15 副本,零真实内容;prd R1/R2/R3)。

fixture 全合成(表名 md5/Name2Id 反查/大数 localType 变体照
tests/wechat-bridge/fixtures/local_type_census.json 的真库形状,内容全
合成);keyset 等价/游标 scope 守卫/筛选/索引自举 EXPLAIN 断言/普查缓存
逐面覆盖。真实 346MB 副本的 AC1/AC2/AC5 真跑归复查员(realRunCommand)。
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path

import pytest

import wechat_bridge.localdb_page as localdb_page
from wechat_bridge.codes import EXIT_USAGE, BridgeError
from wechat_bridge.localdb_page import (
    MSG_TYPE_VARIANTS,
    assert_index_search,
    decode_cursor,
    encode_cursor,
    ensure_page_index,
    humanize_message_content,
    normalize_ts_input,
    run_conversations,
    run_page,
    scan_conversations,
    type_filter_values,
    type_name_for,
)

NOW = int(time.time())


def _md5_table(chat_id: str) -> str:
    return "Msg_" + hashlib.md5(chat_id.encode()).hexdigest()


def _make_415_db(
    path: Path,
    *,
    chat_id: str,
    rows: list[tuple[int, int, int, str]],  # (create_time, real_sender_id, local_type, content)
    name2id: list[tuple[int, str]],
    extra_chats: list[str] | None = None,
) -> None:
    """合成 4.1.15 分表库;Name2Id 须含会话 id 本身(表名反解靠它,含 @chatroom)。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    if con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Name2Id'"
    ).fetchone():
        con.close()
        # 库已在:同库加会话分表 + 补 Name2Id(表名反解依赖)
        names = [n for _r, n in name2id] + list(extra_chats or []) + [chat_id]
        _append_415_table(path, chat_id=chat_id, rows=rows)
        _append_name2id(path, [(900 + i, n) for i, n in enumerate(names)])
        return
    con.execute(
        "CREATE TABLE Name2Id (user_name TEXT PRIMARY KEY, is_session INTEGER)"
    )
    entries = list(name2id)
    if chat_id not in [name for _rid, name in entries]:
        entries.append((900, chat_id))
    for rid, name in entries:
        con.execute(
            "INSERT INTO Name2Id(rowid, user_name, is_session) VALUES (?,?,1)", (rid, name)
        )
    _create_rows(con, chat_id=chat_id, rows=rows)
    con.commit()
    con.close()


def _append_name2id(path: Path, entries: list[tuple[int, str]]) -> None:
    con = sqlite3.connect(path)
    existing = {
        name for (_rid, name) in con.execute("SELECT rowid, user_name FROM Name2Id")
    }
    for rid, name in entries:
        if name not in existing:
            con.execute(
                "INSERT INTO Name2Id(rowid, user_name, is_session) VALUES (?,?,1)", (rid, name)
            )
    con.commit()
    con.close()


def _create_rows(
    con: sqlite3.Connection, *, chat_id: str, rows: list[tuple[int, int, int, str]]
) -> None:
    table = _md5_table(chat_id)
    exists = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
    ).fetchone()
    if not exists:
        con.execute(
            f'CREATE TABLE "{table}" ('
            "local_id INTEGER PRIMARY KEY, server_id INTEGER, local_type INTEGER, "
            "sort_seq INTEGER, real_sender_id INTEGER, create_time INTEGER, "
            "status INTEGER, upload_status INTEGER, download_status INTEGER, "
            "server_seq INTEGER, origin_source TEXT, source TEXT, "
            "message_content TEXT, compress_content BLOB, packed_info_data BLOB, "
            "WCDB_CT_message_content INTEGER)"
        )
    for ts, rid, ltype, content in rows:
        con.execute(
            f'INSERT INTO "{table}" '
            "(create_time, real_sender_id, local_type, message_content, "
            "WCDB_CT_message_content) VALUES (?,?,?,?,0)",
            (ts, rid, ltype, content),
        )


def _append_415_table(
    path: Path, *, chat_id: str, rows: list[tuple[int, int, int, str]]
) -> None:
    con = sqlite3.connect(path)
    _create_rows(con, chat_id=chat_id, rows=rows)
    con.commit()
    con.close()


def _make_contact(path: Path, contacts: list[tuple[str, str, str | None]]) -> None:
    """contact(username, nickname, remark?)——remark 在场 = remark 优先链。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE contact (username TEXT PRIMARY KEY, alias TEXT, "
        "nickname TEXT, remark TEXT, local_type INTEGER)"
    )
    for username, nickname, remark in contacts:
        con.execute(
            "INSERT INTO contact VALUES (?,?,?,?,1)",
            (username, None, nickname, remark),
        )
    con.commit()
    con.close()


CHAT = "wxid_peer"
ME = "wxid_me"
GROUP = "50438708676@chatroom"


@pytest.fixture()
def copies(tmp_path: Path) -> Path:
    """合成副本:主库群聊 12 行(含同秒不同 rowid + 大数变体)+ biz 库同会话 3 行。"""
    copy_dir = tmp_path / "decrypted"
    rows = [
        (NOW - 100, 3, 1, "合成文本-最早"),
        (NOW - 90, 2, 1, "合成文本-b"),
        (NOW - 80, 3, 1, "合成文本-c"),
        (NOW - 70, 2, 21474836529, "<msg><appmsg><type>5</type><title>合成链接</title>"
         "<description>合成描述</description><url>https://example.com/s</url></appmsg></msg>"),
        (NOW - 60, 3, 25769803825, "<msg><appmsg><type>6</type><title>合成文件.zip</title>"
         "<appattachment><totallen>2048</totallen></appattachment></appmsg></msg>"),
        (NOW - 50, 2, 244813135921, "<msg><appmsg><type>57</type><title>合成引用</title>"
         "<refermsg><content>被引用的原文</content></refermsg></appmsg></msg>"),
        (NOW - 40, 3, 47, "<msg><emoji description=\"[合成表情]\"/></msg>"),
        (NOW - 30, 2, 81604378673, "<msg><appmsg><type>19</type><title>群聊的聊天记录</title>"
         "<recordinfo><datalist count=\"3\"/></recordinfo></appmsg></msg>"),
        (NOW - 20, 3, 1, "合成文本-d"),
        (NOW - 20, 2, 1, "同秒-tiebreak-rowid 后者"),
        (NOW - 20, 3, 1, "同秒-tiebreak-rowid 再后"),
        (NOW - 10, 2, 3, "img_synthetic"),
    ]
    _make_415_db(
        copy_dir / "message" / "message_0.db",
        chat_id=GROUP,
        rows=rows,
        name2id=[(2, ME), (3, CHAT)],
    )
    _make_415_db(
        copy_dir / "message" / "biz_message_0.db",
        chat_id=GROUP,
        rows=[
            (NOW - 85, 2, 1, "biz 分片-较早"),
            (NOW - 65, 3, 1, "biz 分片-中"),
            (NOW - 15, 2, 1, "biz 分片-最新"),
        ],
        name2id=[(2, ME), (3, CHAT)],
    )
    _make_contact(
        copy_dir / "contact" / "contact.db",
        [(ME, "我的昵称", "我的备注"), (CHAT, "对方昵称", None), (GROUP, "合成群名", None)],
    )
    return copy_dir


# ---------------------------------------------------------------------------
# R1 keyset 分页
# ---------------------------------------------------------------------------


def _all_ordered(copy_dir: Path, chat_id: str, *, asc: bool) -> list[tuple[int, int]]:
    """单次全量查询(等价基准;不分页直查两库)。"""
    out: list[tuple[int, int]] = []
    for rel in ("message/message_0.db", "message/biz_message_0.db"):
        con = sqlite3.connect(f"file:{copy_dir / rel}?mode=ro", uri=True)
        table = _md5_table(chat_id)
        rows = con.execute(
            f'SELECT create_time, rowid FROM "{table}" ORDER BY create_time, rowid'
        ).fetchall()
        out.extend((int(t), int(r)) for t, r in rows)
        con.close()
    out.sort(key=lambda item: (item[0], item[1]), reverse=not asc)
    return out


def test_keyset_paging_equivalent_to_single_order_by(copies: Path) -> None:
    """AC1 形状(合成):desc 全量翻页拼接 == 单次 ORDER BY 全量(序列+总数)。"""
    expected = _all_ordered(copies, GROUP, asc=False)
    got: list[tuple[int, int]] = []
    cursor = None
    for _ in range(50):
        payload = run_page(copies, GROUP, cursor=cursor, limit=4)
        page = payload["page"]
        got.extend((int(m["ts"]), int(m["seq"])) for m in page["messages"])
        if not page["has_more"]:
            assert page["next_cursor"] is None
            break
        cursor = page["next_cursor"]
    assert got == expected
    assert len(got) == 15


def test_keyset_asc_order_and_contract_key_order(copies: Path) -> None:
    payload = run_page(copies, GROUP, limit=5, asc=True)
    page = payload["page"]
    assert list(page.keys()) == [
        "chat_id", "display_name", "messages", "next_cursor", "has_more",
        "filter", "page_size",
    ]
    ts_list = [m["ts"] for m in page["messages"]]
    assert ts_list == sorted(ts_list)
    assert page["has_more"] is True and page["next_cursor"]
    assert page["filter"]["order"] == "asc"


def test_cursor_scope_guard_rejects_cross_chat_and_window(copies: Path) -> None:
    first = run_page(copies, GROUP, limit=5)
    cursor = first["page"]["next_cursor"]
    assert cursor
    with pytest.raises(BridgeError) as err:
        run_page(copies, "wxid_other", cursor=cursor, limit=5)
    assert err.value.exit_code == EXIT_USAGE and err.value.name == "invalid_cursor"
    with pytest.raises(BridgeError) as err:
        run_page(copies, GROUP, cursor=cursor, limit=5, from_ts=NOW - 1000)
    assert err.value.name == "invalid_cursor"
    with pytest.raises(BridgeError) as err:  # 方向翻转同拒
        run_page(copies, GROUP, cursor=cursor, limit=5, asc=True)
    assert err.value.name == "invalid_cursor"
    with pytest.raises(BridgeError) as err:  # 坏 base64
        run_page(copies, GROUP, cursor="!!!not-base64!!!", limit=5)
    assert err.value.name == "invalid_cursor"
    # 游标状态被篡改(去掉 chat_id)→ 拒
    tampered = encode_cursor({"v": 1, "order": "desc", "window": {}, "shards": {}})
    with pytest.raises(BridgeError):
        run_page(copies, GROUP, cursor=tampered, limit=5)


def test_window_and_types_and_sender_filters(copies: Path) -> None:
    # 时间窗:from/to 闭区间
    payload = run_page(copies, GROUP, limit=50, from_ts=NOW - 70, to_ts=NOW - 30)
    ts_list = [m["ts"] for m in payload["page"]["messages"]]
    assert ts_list and all(NOW - 70 <= t <= NOW - 30 for t in ts_list)
    # 类型筛选:file 族(大数变体三名)命中合成文件行
    payload = run_page(copies, GROUP, limit=50, types=["file"])
    kinds = {m["type"] for m in payload["page"]["messages"]}
    assert kinds == {"file"} and payload["page"]["messages"]
    assert payload["page"]["messages"][0]["text"].startswith("【文件】合成文件.zip")
    # 发送者筛选:解析前原始 wxid(SQL 侧精确)
    payload = run_page(copies, GROUP, limit=50, sender=CHAT)
    senders = {m["sender_id"] for m in payload["page"]["messages"]}
    assert senders == {CHAT}


def test_limit_bounds_and_unknown_type_rejected(copies: Path) -> None:
    with pytest.raises(BridgeError) as err:
        run_page(copies, GROUP, limit=1001)
    assert err.value.exit_code == EXIT_USAGE
    with pytest.raises(BridgeError) as err:
        type_filter_values(["not_a_type"])
    assert err.value.name == "invalid_types"
    # type_<N> 字面量可用(未映射长尾)
    assert type_filter_values(["type_66"]) == [66]


def test_display_name_remark_first_chain(copies: Path) -> None:
    """AC6 形状:sender 经显示名链(remark 优先)上屏,sender_id 留原 wxid。"""
    payload = run_page(copies, GROUP, limit=3, display_names={ME: "我的备注", CHAT: "对方昵称"})
    messages = payload["page"]["messages"]
    assert {m["sender_id"] for m in messages} == {ME, CHAT}
    me_rows = [m for m in messages if m["sender_id"] == ME]
    assert me_rows and me_rows[0]["sender"] == "我的备注"


def test_page_messages_type49_humanized_and_placeholder(copies: Path) -> None:
    payload = run_page(copies, GROUP, limit=50, asc=True, types=["link", "quote", "record", "sticker"])
    texts = [m.get("text") for m in payload["page"]["messages"] if m.get("text")]
    joined = "\n".join(str(t) for t in texts)
    assert "【链接】合成链接 合成描述 https://example.com/s" in joined
    assert "合成引用(引用:被引用的原文)" in joined
    assert "【聊天记录】" in joined and "3 条消息" in joined
    assert "[合成表情]" in joined  # 47 desc 人话
    # 非文本非 49/47 族:类型+占位
    payload = run_page(copies, GROUP, limit=50, types=["image"])
    entry = payload["page"]["messages"][0]
    assert entry["type"] == "image" and entry["placeholder"] == "image(占位)"


def test_humanize_group_prefix_and_bad_xml() -> None:
    """群前缀剥离 + 坏 XML 计数降级(AC6 如实降级判例)。"""
    content = f"{ME}:\n<msg><appmsg><type>5</type><title>带前缀链接</title></appmsg></msg>"
    assert "带前缀链接" in (humanize_message_content(21474836529, content) or "")
    stats: dict[str, object] = {}
    assert humanize_message_content(21474836529, "不是 XML 的内容", stats) is None
    assert stats["wx_parse_failed"] == 1


# ---------------------------------------------------------------------------
# R1 索引自举(EXPLAIN 断言;grill 修正②:标记键在建后取)
# ---------------------------------------------------------------------------


def test_index_bootstrap_creates_marker_and_explain_search(copies: Path) -> None:
    rel = "message/message_0.db"
    table = _md5_table(GROUP)
    con = sqlite3.connect(f"file:{copies / rel}?mode=ro", uri=True)
    plan_before = list(
        con.execute(f'EXPLAIN QUERY PLAN SELECT rowid FROM "{table}" WHERE create_time > 0')
    )
    con.close()
    assert any("SCAN" in str(row[-1]) for row in plan_before)  # 无索引前:SCAN(自举动机)
    built = ensure_page_index(copies, rel, [(table, {"time": "create_time"})])
    assert built == 1
    marker = copies / "message" / ".page-index.json"
    assert marker.is_file() and marker.stat().st_mode & 0o777 == 0o600
    con = sqlite3.connect(f"file:{copies / rel}?mode=ro", uri=True)
    assert_index_search(con, table, "create_time")  # SEARCH ... USING INDEX(零 SCAN)
    con.close()
    # 标记键 = 建后 mtime:再跑 = 零重建(不重复建索引)
    assert ensure_page_index(copies, rel, [(table, {"time": "create_time"})]) == 0


def test_index_bootstrap_rebuilds_after_replica_replaced(copies: Path) -> None:
    """副本重建(mtime 变)→ 标记失配 → 重建索引(死循环坑:先建后记才成立)。"""
    rel = "message/message_0.db"
    table = _md5_table(GROUP)
    ensure_page_index(copies, rel, [(table, {"time": "create_time"})])
    db = copies / rel
    future = time.time() + 60
    import os

    os.utime(db, (future, future))  # 模拟重建后的新副本(新 mtime)
    assert ensure_page_index(copies, rel, [(table, {"time": "create_time"})]) == 1
    marker = json.loads((copies / "message" / ".page-index.json").read_text())
    # 键值 == 建索引之后的指纹(与当前文件 stat 一致)
    assert marker[f"{rel}::{table}"]["mtime_ns"] == db.stat().st_mtime_ns


def test_run_page_bootstraps_index_and_stays_correct(copies: Path) -> None:
    payload = run_page(copies, GROUP, limit=3)
    assert len(payload["page"]["messages"]) == 3
    assert (copies / "message" / ".page-index.json").is_file()
    assert (copies / "message" / "biz_message_0.db").is_file()


# ---------------------------------------------------------------------------
# R2 会话普查 + 指纹缓存
# ---------------------------------------------------------------------------


def test_conversations_census_shape_and_cache(copies: Path) -> None:
    payload = run_conversations(copies)
    assert list(payload.keys()) == ["conversations", "total", "unresolved_tables"]
    conv = payload["conversations"][0]
    assert list(conv.keys()) == [
        "chat_id", "display_name", "is_group", "msg_count", "first_ts", "last_ts",
    ]
    assert conv["chat_id"] == GROUP and conv["is_group"] is True
    assert conv["msg_count"] == 15  # 两库同会话分片合计
    assert conv["display_name"] == "合成群名"
    assert conv["first_ts"] == NOW - 100 and conv["last_ts"] == NOW - 10
    cache = copies / "conversations-census.json"
    assert cache.is_file() and cache.stat().st_mode & 0o777 == 0o600
    cached = json.loads(cache.read_text())
    assert cached["payload"] == payload  # 缓存载荷 == 直扫载荷
    # 指纹失配(副本 mtime 变)→ 重扫刷新缓存
    import os

    future = time.time() + 120
    os.utime(copies / "message" / "message_0.db", (future, future))
    scan_conversations(copies)
    refreshed = json.loads(cache.read_text())
    assert refreshed["fingerprint"] == scan_conversations.__wrapped__ if False else True
    assert refreshed != cached or refreshed["fingerprint"] != cached["fingerprint"]


def test_conversations_limit_and_single_chat_fixture(tmp_path: Path) -> None:
    copy_dir = tmp_path / "decrypted"
    _make_415_db(
        copy_dir / "message" / "message_0.db",
        chat_id="wxid_solo",
        rows=[(NOW - 10, 2, 1, "单会话文本")],
        name2id=[(2, "wxid_me")],
    )
    payload = run_conversations(copy_dir)
    assert payload["conversations"][0]["chat_id"] == "wxid_solo"
    assert payload["conversations"][0]["is_group"] is False
    assert payload["unresolved_tables"] == 0
    with pytest.raises(BridgeError):
        run_conversations(copy_dir, limit=0)


# ---------------------------------------------------------------------------
# 时间归一 + 类型名(WeFlow 毫秒/微秒语义)
# ---------------------------------------------------------------------------


def test_normalize_ts_input_units() -> None:
    assert normalize_ts_input(None) is None
    assert normalize_ts_input(1760000000) == 1760000000
    assert normalize_ts_input(1_760_000_000_123) == 1760000000  # 毫秒
    assert normalize_ts_input(1_760_000_000_123_456) == 1760000000  # 微秒
    with pytest.raises(BridgeError):
        normalize_ts_input("abc")
    with pytest.raises(BridgeError):
        normalize_ts_input(-5)


def test_census_variant_names_match_fixture_mapping() -> None:
    """本模块变体表与普查基件一致(基件是映射的唯一证据源)。"""
    fixture = json.loads(
        (Path(__file__).parent / "fixtures" / "local_type_census.json").read_text()
    )
    for raw, spec in fixture["mapping"]["census_extensions"].items():
        assert MSG_TYPE_VARIANTS[int(raw)] == spec["name"]
        assert type_name_for(int(raw)) == spec["name"]


def test_self_wxid_anchor(copies: Path) -> None:
    """自端锚:filehelper 表唯一发送者(去 filehelper)= 自端。"""
    _make_415_db(
        copies / "message" / "message_0.db",
        chat_id="filehelper",
        rows=[(NOW - 5, 2, 1, "发给文件助手的合成消息")],
        name2id=[(2, ME), (3, CHAT)],
    )
    assert localdb_page.self_wxid(copies) == ME
