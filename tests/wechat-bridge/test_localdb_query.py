"""E3 三域只读查询单测(合成明文副本,4.x 形状 schema;零真实内容)。

fixture schema 按公开参考(微信 4.x:``Msg_<hash>`` 宽表 + ``contact`` 表,
luvrell/wechat-msg-extract scripts/test_exporter.py:16-24)全合成——
查询层与真实解密副本的对账归 D4 闭合后(当前 E1 实测密钥不可得)。

0.4.2 B0 增:4.1.15 分表形态夹具(``Msg_<md5(username)>`` 无会话列 +
``Name2Id`` 反查 + ``WCDB_CT_message_content`` zstd 压缩行),形状照
2026-10-13 直查本机解密副本实测 DDL;内容全合成,零真实语料。

压缩行走**真 zstd 实解**:夹具用 pip ``zstandard``(根 pyproject dev 组,
与插件 pyproject 主依赖同版本窗)产真 zstd 帧,桥侧两级 import 链
(stdlib ``compression.zstd`` → ``zstandard``)真解回明文——与生产链
同构,不做变换替身;仅「模块缺位」负例保留 monkeypatch。

zstandard 缺位(未装 dev 组)时:本文件照常收集,4.1.15 压缩相关用例
经 ``copies_415`` 夹具统一 skip,旧形态用例照常跑——收集期不再整文件炸。
"""

from __future__ import annotations

import hashlib
import sqlite3
import time
from pathlib import Path

import pytest

try:  # dev 组可选件:缺位时本文件仍可收集,压缩用例运行期统一 skip
    import zstandard
except ImportError:
    zstandard = None

import wechat_bridge.localdb_query as localdb_query
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


# =====================================================================
# 4.1.15 分表形态(0.4.2 B0):Msg_<md5(username)> 无会话列 + Name2Id
# 反查 + WCDB_CT_message_content zstd 压缩行。DDL 照 2026-10-13 直查本机
# 解密副本实测;内容全合成(红线 6:零真实语料入库)。
# =====================================================================

CHAT_415 = "50438708676@chatroom"  # 表名 md5 反解锚(形状照真实库)
SECRET_TEXT = "合成压缩行-解出的真文本"  # 压缩行解出的目标明文
ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"
def _secret_zstd_frame() -> bytes:
    """真 zstd 帧惰性生成(帧头自带魔数,与 4.1.15 实测库字节形状一致)。

    惰性化保收集期安全:zstandard 缺位时模块可收集,运行期由
    copies_415 夹具统一 skip。
    """
    if zstandard is None:
        pytest.skip("pip zstandard 未装(根 pyproject dev 组;uv sync --all-extras 后可跑)")
    frame = zstandard.compress(SECRET_TEXT.encode("utf-8"))
    assert frame[:4] == ZSTD_MAGIC  # 夹具自检:确系真 zstd 帧
    return frame


def _md5hex(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()


_DDL_415 = (
    "(local_id INTEGER PRIMARY KEY AUTOINCREMENT, server_id INTEGER, "
    "local_type INTEGER, sort_seq INTEGER, real_sender_id INTEGER, "
    "create_time INTEGER, status INTEGER, upload_status INTEGER, "
    "download_status INTEGER, server_seq INTEGER, origin_source INTEGER, "
    "source TEXT, message_content TEXT, compress_content TEXT, "
    "packed_info_data BLOB, WCDB_CT_message_content INTEGER DEFAULT NULL, "
    "WCDB_CT_source INTEGER DEFAULT NULL)"
)


def _build_415_db(path: Path, *, with_name2id: bool = True) -> None:
    """合成 4.1.15 message 库:目标群分表 + 旁会话分表 + 旧形态宽表混居。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    if with_name2id:
        con.execute(
            "CREATE TABLE Name2Id(user_name TEXT PRIMARY KEY, is_session INTEGER)"
        )
        # rowid 显式钉住(= real_sender_id 的整数 id;实测同构)
        for rid, name, sess in (
            (10, "wxid_me", 0),
            (20, "wxid_alice", 0),
            (30, CHAT_415, 1),
            (40, "wxid_bob", 0),
        ):
            con.execute(
                "INSERT INTO Name2Id(rowid, user_name, is_session) VALUES (?,?,?)",
                (rid, name, sess),
            )
    target = "Msg_" + _md5hex(CHAT_415)
    other = "Msg_" + _md5hex("wxid_alice")
    con.execute(f'CREATE TABLE "{target}"{_DDL_415}')
    con.execute(f'CREATE TABLE "{other}"{_DDL_415}')
    rows = [
        # (local_id,server_id,local_type,sort_seq,real_sender_id,create_time,
        #  status,upload,download,server_seq,origin_source,source,
        #  message_content,compress,NULL,WCDB_CT_message_content,NULL)
        (1, 101, 1, 1, 20, NOW - 60, 1, 0, 0, 0, 0, "", "合成明文-对方发", None, None, None, None),
        (2, 102, 1, 2, 10, NOW - 120, 1, 0, 0, 0, 0, "", "合成明文-我发", None, None, 0, None),
        (3, 103, 1, 3, 20, NOW - 180, 1, 0, 0, 0, 0, "", _secret_zstd_frame(), None, None, 4, None),
        (4, 104, 3, 4, 20, NOW - 240, 1, 0, 0, 0, 0, "", "img_合成立名", None, None, None, None),
        (5, 105, 1, 5, 20, NOW - 40 * 86400, 1, 0, 0, 0, 0, "", "合成-40天前应被窗口滤掉", None, None, None, None),
        (6, 106, 1, 6, 99, NOW - 30, 1, 0, 0, 0, 0, "", "合成-未知sender回落会话", None, None, None, None),
        # CT=4 但字节无魔数:真模块/替身都解不开 → 占位 + zstd_decode_failed
        (7, 107, 1, 7, 20, NOW - 10, 1, 0, 0, 0, 0, "", b"corrupt-no-magic", None, None, 4, None),
        # 未压 BLOB 且非 UTF-8:严格解码失败 → 占位 + text_decode_failed
        (8, 108, 1, 8, 20, NOW - 150, 1, 0, 0, 0, 0, "", b"\xff\xfe\x00\xba", None, None, None, None),
    ]
    con.executemany(f'INSERT INTO "{target}" VALUES ({",".join("?" * 17)})', rows)
    con.execute(
        f'INSERT INTO "{other}" VALUES (1,201,1,1,10,{NOW - 50},1,0,0,0,0,"",'
        '"合成-旁会话不该出现",NULL,NULL,NULL,NULL)'
    )
    # 旧形态宽表混居(回归守卫:两形态并存、并集输出、互不回退)
    con.execute(
        'CREATE TABLE "Msg_legacy_wide" (localId INTEGER PRIMARY KEY, serverId INTEGER, '
        "localType INTEGER, createTime INTEGER, sortSeq INTEGER, isSender INTEGER, "
        "strTalker TEXT, content TEXT)"
    )
    con.execute(
        "INSERT INTO Msg_legacy_wide VALUES (1,301,1,?,1,0,?,?)",
        (NOW - 45, CHAT_415, "合成-旧形态宽表行"),
    )
    con.commit()
    con.close()


@pytest.fixture()
def copies_415(tmp_path: Path) -> Path:
    if zstandard is None:
        pytest.skip("pip zstandard 未装(根 pyproject dev 组;uv sync --all-extras 后可跑)")
    copy_root = tmp_path / "home415" / "decrypted"
    _build_415_db(copy_root / "message" / "message_0.db")
    return copy_root


def _open_415(copies: Path) -> sqlite3.Connection:
    return sqlite3.connect(
        f"file:{copies / 'message' / 'message_0.db'}?mode=ro", uri=True
    )


class TestFindMessageTables415:
    def test_md5_table_resolves_chat_via_name2id(self, copies_415: Path) -> None:
        """表名反解:遍历 Name2Id 全表 md5 匹配表名后缀(非仅查询参数)。"""
        con = _open_415(copies_415)
        try:
            tables = dict(find_message_tables(con))
        finally:
            con.close()
        target = "Msg_" + _md5hex(CHAT_415)
        other = "Msg_" + _md5hex("wxid_alice")
        assert target in tables and other in tables and "Msg_legacy_wide" in tables
        colmap = tables[target]
        assert colmap["talker"] is None  # 4.1.15 分表无会话列
        assert colmap["chat"] == CHAT_415  # 表名 md5 反解
        assert tables[other]["chat"] == "wxid_alice"  # 旁表也反解(全表遍历)

    def test_column_mapping_415(self, copies_415: Path) -> None:
        """列映射:time=create_time / content=message_content / type=local_type
        / sender_id=real_sender_id / ct_content=WCDB_CT_message_content。"""
        con = _open_415(copies_415)
        try:
            colmap = dict(find_message_tables(con))["Msg_" + _md5hex(CHAT_415)]
        finally:
            con.close()
        assert colmap["time"] == "create_time"
        assert colmap["content"] == "message_content"
        assert colmap["type"] == "local_type"
        assert colmap["sender_id"] == "real_sender_id"
        assert colmap["ct_content"] == "WCDB_CT_message_content"

    def test_legacy_wide_shape_unchanged(self, copies_415: Path) -> None:
        """旧形态签名不回退:宽表仍按会话列识别,colmap 不挂 chat 反解。"""
        con = _open_415(copies_415)
        try:
            colmap = dict(find_message_tables(con))["Msg_legacy_wide"]
        finally:
            con.close()
        assert colmap["talker"] == "strTalker"
        assert colmap["content"] == "content"
        assert colmap["sender"] == "isSender"
        assert colmap.get("chat") is None


class TestQueryMessages415:
    def test_decode_sender_and_window(self, copies_415: Path) -> None:
        """压缩行真 zstd 实解 + sender 经 Name2Id 反查 + 窗口/旁会话过滤。

        无 monkeypatch:走生产两级 import 链(venv 3.12 → pip zstandard),
        真帧真解——与装机态同构。"""
        con = _open_415(copies_415)
        try:
            stats: dict[str, object] = {}
            messages = query_messages(
                con, CHAT_415, NOW - 7 * 86400, 50, stats=stats
            )
        finally:
            con.close()
        assert [m["text"] for m in messages if "text" in m] == [
            "合成-未知sender回落会话",  # ts=-30
            "合成-旧形态宽表行",  # ts=-45(旧形态并集)
            "合成明文-对方发",  # ts=-60
            "合成明文-我发",  # ts=-120
            SECRET_TEXT,  # ts=-180(压缩行解出)
        ]
        by_text = {m.get("text"): m for m in messages}
        assert by_text["合成明文-我发"]["sender"] == "wxid_me"  # rowid 10 反查
        assert by_text["合成明文-对方发"]["sender"] == "wxid_alice"  # rowid 20
        assert by_text["合成-未知sender回落会话"]["sender"] == CHAT_415  # 未知 id 回落
        assert by_text[SECRET_TEXT]["sender"] == "wxid_alice"
        assert by_text["合成-旧形态宽表行"]["sender"] == CHAT_415  # 旧形态并集
        # 压缩坏帧(CT=4 无魔数)/图片/非 UTF-8 BLOB → 占位,不吐乱码
        placeholders = [m for m in messages if "media_placeholder" in m]
        assert len(placeholders) == 3
        assert all(m["media_placeholder"] == "非文本消息,内容未导出(占位)" for m in placeholders)
        # 40 天前被窗口滤、旁会话分表不串台
        assert all("40天前" not in str(m.get("text", "")) for m in messages)
        assert all(m.get("text") != "合成-旁会话不该出现" for m in messages)
        assert stats["zstd_decoded"] == 1
        assert stats["zstd_decode_failed"] == 1
        assert stats["text_decode_failed"] == 1

    def test_compressed_row_placeholder_without_zstd_module(
        self, copies_415: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """zstd 模块缺位:压缩行落占位 + 计数,明文行不受影响(能解的仍出)。"""
        monkeypatch.setattr(localdb_query, "_zstd", None)
        con = _open_415(copies_415)
        try:
            stats: dict[str, object] = {}
            messages = query_messages(con, CHAT_415, NOW - 7 * 86400, 50, stats=stats)
        finally:
            con.close()
        assert [m["text"] for m in messages if "text" in m] == [
            "合成-未知sender回落会话",
            "合成-旧形态宽表行",
            "合成明文-对方发",
            "合成明文-我发",
        ]
        assert stats["zstd_module_missing"] == 2  # 好压缩行 + 坏帧行都缺模块
        assert "zstd_decoded" not in stats

    def test_name2id_absent_degrades_to_legacy_only(
        self, tmp_path: Path
    ) -> None:
        """Name2Id 缺失:md5 分表会话归属不明 → 如实跳过,旧形态照常出。"""
        copy_root = tmp_path / "noname2id"
        _build_415_db(copy_root / "message" / "message_0.db", with_name2id=False)
        con = sqlite3.connect(
            f"file:{copy_root / 'message' / 'message_0.db'}?mode=ro", uri=True
        )
        try:
            colmap = dict(find_message_tables(con))["Msg_" + _md5hex(CHAT_415)]
            assert colmap.get("chat") is None  # 反解不出:如实 None
            messages = query_messages(con, CHAT_415, NOW - 7 * 86400, 50)
        finally:
            con.close()
        assert [m.get("text") for m in messages] == ["合成-旧形态宽表行"]

    def test_run_query_reports_decode_stats(self, copies_415: Path) -> None:
        """run_query 载荷带 content_decode 统计(zstd 可用性与计数;真解)。"""
        payload = run_query(
            copy_dir=copies_415,
            domains=["message"],
            chat_id=CHAT_415,
            since_days=7,
            limit=50,
            copy_info={"dir": str(copies_415), "built": [], "kept": [], "skipped": [], "total_bytes": 0},
        )
        assert payload["messages"], "4.1.15 分表查询必须出消息(B0 主诉)"
        assert any(m.get("text") == SECRET_TEXT for m in payload["messages"])
        decode = payload["content_decode"]
        assert isinstance(decode["zstd_available"], bool)
        assert decode["zstd_decoded"] == 1
