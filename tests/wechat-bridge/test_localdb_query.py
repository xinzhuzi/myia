"""E3 三域只读查询单测(合成明文副本,4.x 形状 schema;零真实内容)。

fixture schema 按公开参考(微信 4.x:``Msg_<hash>`` 宽表 + ``contact`` 表,
luvrell/wechat-msg-extract scripts/test_exporter.py:16-24)全合成——
查询层与真实解密副本的对账归 D4 闭合后(当前 E1 实测密钥不可得)。
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

import pytest

from wechat_bridge.codes import BridgeError
from wechat_bridge.localdb_query import (
    find_message_tables,
    list_sessions,
    lookup_contact,
    query_messages,
    run_query,
)

NOW = int(time.time())  # 以真实时钟为锚,_since 窗口语义才可判(40 天前行必滤)


@pytest.fixture()
def copies(tmp_path: Path) -> Path:
    """合成解密副本(message/contact/session 三域,全合成内容)。"""
    copy_root = tmp_path / "home" / "wechat-localdb" / "decrypted"
    msg = copy_root / "message" / "message_0.db"
    msg.parent.mkdir(parents=True)
    con = sqlite3.connect(msg)
    con.execute(
        'CREATE TABLE "Msg_ab12cd34" (localId INTEGER PRIMARY KEY, serverId INTEGER, '
        "localType INTEGER, createTime INTEGER, sortSeq INTEGER, isSender INTEGER, "
        "strTalker TEXT, content TEXT)"
    )
    rows = [
        (1, 101, 1, NOW - 60, 1, 1, "filehelper", "合成文本-我发"),
        (2, 102, 1, NOW - 120, 2, 0, "filehelper", "合成文本-对方发"),
        (3, 103, 3, NOW - 180, 3, 0, "filehelper", "img_合成立名"),
        (4, 104, 1, NOW - 40 * 86400, 4, 0, "filehelper", "合成文本-40天前应被窗口滤掉"),
        (5, 105, 1, NOW - 30, 5, 0, "other_chat", "合成文本-别的会话"),
    ]
    con.executemany(
        'INSERT INTO "Msg_ab12cd34" VALUES (?,?,?,?,?,?,?,?)', rows
    )
    con.commit()
    con.close()

    contact = copy_root / "contact" / "contact.db"
    contact.parent.mkdir(parents=True)
    con = sqlite3.connect(contact)
    con.execute(
        "CREATE TABLE contact (username TEXT PRIMARY KEY, alias TEXT, "
        "nickname TEXT, remark TEXT, localType INTEGER)"
    )
    con.execute(
        "INSERT INTO contact VALUES ('filehelper','fh','文件传输助手','文件传输助手',1)"
    )
    con.commit()
    con.close()

    session = copy_root / "session" / "session.db"
    session.parent.mkdir(parents=True)
    con = sqlite3.connect(session)
    con.execute(
        "CREATE TABLE SessionTable (strTalker TEXT PRIMARY KEY, nickName TEXT, "
        "unreadCount INTEGER)"
    )
    con.execute("INSERT INTO SessionTable VALUES ('filehelper','文件传输助手',2)")
    con.commit()
    con.close()
    return copy_root


class TestFindMessageTables:
    def test_detects_msg_table_by_signature(self, copies: Path) -> None:
        con = sqlite3.connect(f"file:{copies / 'message' / 'message_0.db'}?mode=ro", uri=True)
        try:
            tables = find_message_tables(con)
            assert [t for t, _ in tables] == ["Msg_ab12cd34"]
            colmap = tables[0][1]
            assert colmap["talker"] == "strTalker"
            assert colmap["time"] == "createTime"
            assert colmap["content"] == "content"
            assert colmap["sender"] == "isSender"
        finally:
            con.close()


class TestQueryMessages:
    def test_window_type_and_sender(self, copies: Path) -> None:
        con = sqlite3.connect(f"file:{copies / 'message' / 'message_0.db'}?mode=ro", uri=True)
        try:
            messages = query_messages(con, "filehelper", NOW - 7 * 86400, 50)
        finally:
            con.close()
        # 40 天前的被 since 窗口滤掉;别的会话被 talker 过滤。
        assert len(messages) == 3
        assert [m["text"] for m in messages if m["type"] == "text"] == [
            "合成文本-我发",
            "合成文本-对方发",
        ]
        image = next(m for m in messages if m["type"] == "image")
        assert "text" not in image and image["media_placeholder"]
        assert messages[0]["sender"] == "me"  # 最新一条 isSender=1
        assert messages[1]["sender"] == "filehelper"

    def test_limit_truncates(self, copies: Path) -> None:
        con = sqlite3.connect(f"file:{copies / 'message' / 'message_0.db'}?mode=ro", uri=True)
        try:
            messages = query_messages(con, "filehelper", 0, 2)
        finally:
            con.close()
        assert len(messages) == 2


class TestContactAndSession:
    def test_lookup_prefers_remark(self, copies: Path) -> None:
        con = sqlite3.connect(f"file:{copies / 'contact' / 'contact.db'}?mode=ro", uri=True)
        try:
            assert lookup_contact(con, "filehelper") == "文件传输助手"
            assert lookup_contact(con, "absent") is None
        finally:
            con.close()

    def test_sessions_listing(self, copies: Path) -> None:
        con = sqlite3.connect(f"file:{copies / 'session' / 'session.db'}?mode=ro", uri=True)
        try:
            sessions = list_sessions(con, 20)
        finally:
            con.close()
        assert sessions == [{"id": "filehelper", "name": "文件传输助手", "unread": 2}]


class TestRunQuery:
    def test_three_domain_payload(self, copies: Path) -> None:
        payload = run_query(
            copy_dir=copies,
            domains=["message", "session", "contact"],
            chat_id="filehelper",
            since_days=7,
            limit=50,
            copy_info={"dir": str(copies), "built": [], "kept": [], "skipped": [], "total_bytes": 0},
        )
        assert payload["chat_id"] == "filehelper"
        assert len(payload["messages"]) == 3
        assert payload["display_name"] == "文件传输助手"
        assert payload["sessions"] and payload["domains"] == {
            "message": "ok",
            "session": "ok",
            "contact": "ok",
        }

    def test_missing_copy_domains_degrade_but_message_rules(
        self, copies: Path
    ) -> None:
        """contact/session 副本缺 → 域如实降级;message 缺 → 结构化 22。"""
        payload = run_query(
            copy_dir=copies,
            domains=["message"],
            chat_id="filehelper",
            since_days=7,
            limit=50,
            copy_info={"dir": str(copies), "built": [], "kept": [], "skipped": [], "total_bytes": 0},
        )
        assert payload["display_name"] is None and payload["sessions"] == []
        (copies / "message" / "message_0.db").unlink()
        with pytest.raises(BridgeError) as excinfo:
            run_query(
                copy_dir=copies,
                domains=["message"],
                chat_id="filehelper",
                since_days=7,
                limit=50,
                copy_info={"dir": str(copies), "built": [], "kept": [], "skipped": [], "total_bytes": 0},
            )
        assert excinfo.value.exit_code == 22
