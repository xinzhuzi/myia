"""水位扫描/SSE 数据面单测(task 10-14-wechat-http-api R6/R8;CI 全合成)。

夹具 = 4.1.15 分表形状合成库(与 test_httpapi.FakeEnv 同族,内容全合成);
覆盖:水位持久化(600/仅时间戳)、冷启动=now 不倒灌、断档间隙如实补发、
50 会话扫描上限、尾部窗口扩级、撤回解析(newmsgid↔server_id 配对 /
原消息缺失=仅撤回事实)、EventHub 重放淘汰(容量/TTL)、Last-Event-ID 续传。
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import time
from pathlib import Path

import pytest

import wechat_bridge.watermark as watermark
from wechat_bridge.watermark import (
    EventHub,
    WatermarkScanner,
    parse_revoke_events,
    read_watermark,
    scan_round,
    sse_stream,
    write_watermark,
    watermark_path,
)

NOW = int(time.time())
CHAT_A = "chat_a"
CHAT_B = "chat_b"
GROUP = "123456@chatroom"
REVOKE_NEWMSGID = 77001


def _table(chat: str) -> str:
    return "Msg_" + hashlib.md5(chat.encode()).hexdigest()


def _msg_columns() -> str:
    return (
        "local_id INTEGER PRIMARY KEY, server_id INTEGER, local_type INTEGER, "
        "sort_seq INTEGER, real_sender_id INTEGER, create_time INTEGER, "
        "status INTEGER, upload_status INTEGER, download_status INTEGER, "
        "server_seq INTEGER, origin_source TEXT, source TEXT, "
        "message_content TEXT, compress_content BLOB, packed_info_data BLOB, "
        "WCDB_CT_message_content INTEGER, WCDB_CT_source INTEGER"
    )


def build_env(root: Path, *, sessions: int = 3, rows_per_chat: int = 4) -> dict:
    """合成 message+session 库(连接直接返回,复制到 tmp 后只读打开)。"""
    message_db = root / "decrypted" / "message" / "message_0.db"
    message_db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(message_db)
    con.execute("CREATE TABLE Name2Id (user_name TEXT PRIMARY KEY, is_session INTEGER)")
    rowids: dict[str, int] = {}
    for index in range(sessions):
        username = CHAT_A if index == 0 else (CHAT_B if index == 1 else f"wxid_{index}")
        cur = con.execute(
            "INSERT INTO Name2Id (user_name, is_session) VALUES (?, 1)", (username,)
        )
        rowids[username] = int(cur.lastrowid)
    chat_names = [CHAT_A, CHAT_B] + [f"wxid_{i}" for i in range(2, sessions)]
    for chat in chat_names:
        con.execute(f'CREATE TABLE "{_table(chat)}" ({_msg_columns()})')
    # CHAT_A:窗口内 4 行 + 撤回对(原消息 server_id=REVOKE_NEWMSGID + 10002 行)。
    base = NOW - 300
    sender = rowids[CHAT_A]
    rows = [
        (1, 20001, 1, base + 10, "文本一"),
        (2, 20002, 3, base + 20, "图片占位内容"),
        (3, REVOKE_NEWMSGID, 1, base + 30, "被撤回的原始消息内容超长也要截断到三十字以内检查"),
        (4, 20004, 10002, base + 40, (
            f'<sysmsg type="revokemsg"><revokemsg><session>{CHAT_A}</session>'
            f"<msgid>9</msgid><newmsgid>{REVOKE_NEWMSGID}</newmsgid>"
            '<replacemsg><![CDATA["某人" 撤回了一条消息]]></replacemsg>'
            "</revokemsg></sysmsg>"
        )),
    ]
    for local_id, server_id, local_type, ts, content in rows:
        con.execute(
            f'INSERT INTO "{_table(CHAT_A)}" (local_id, server_id, local_type, '
            "sort_seq, real_sender_id, create_time, message_content) "
            "VALUES (?,?,?,?,?,?,?)",
            (local_id, server_id, local_type, local_id, sender, ts, content),
        )
    # 其余会话:各 rows_per_chat 行窗口内文本。
    for chat in chat_names[1:]:
        for i in range(rows_per_chat):
            con.execute(
                f'INSERT INTO "{_table(chat)}" (local_id, server_id, local_type, '
                "sort_seq, real_sender_id, create_time, message_content) "
                "VALUES (?,?,?,?,?,?,?)",
                (i + 1, 30000 + i, 1, i + 1, rowids[chat], base + i, f"{chat}-文本{i}"),
            )
    con.commit()
    con.close()
    session_db = root / "decrypted" / "session" / "session.db"
    session_db.parent.mkdir(parents=True, exist_ok=True)
    scon = sqlite3.connect(session_db)
    scon.execute(
        "CREATE TABLE SessionTable (strTalker TEXT PRIMARY KEY, nickName TEXT, unreadCount INTEGER)"
    )
    for index, chat in enumerate(chat_names):
        scon.execute("INSERT INTO SessionTable VALUES (?,?,?)", (chat, f"会话{index}", 0))
    scon.commit()
    scon.close()
    return {"message": message_db, "session": session_db, "chats": chat_names}


def _open(path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


@pytest.fixture()
def env(tmp_path: Path) -> dict:
    return build_env(tmp_path)


# =====================================================================
# 水位持久化
# =====================================================================


class TestWatermarkPersistence:
    def test_write_then_read_roundtrip(self, tmp_path: Path) -> None:
        path = write_watermark(tmp_path, 1_700_000_123, now=1_700_000_200.0)
        assert path == watermark_path(tmp_path)
        assert path.is_file()
        assert (path.stat().st_mode & 0o777) == 0o600
        assert (path.parent.stat().st_mode & 0o777) == 0o700
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert set(raw) == {"watermark", "updated_at"}  # 仅时间戳,零内容零密钥
        assert raw["watermark"] == 1_700_000_123
        assert read_watermark(tmp_path) == 1_700_000_123

    def test_missing_file_is_none_cold_start(self, tmp_path: Path) -> None:
        assert read_watermark(tmp_path) is None

    @pytest.mark.parametrize("body", ["", "{broken", '["not", "dict"]', '{"watermark": "x"}'])
    def test_corrupt_shapes_fall_back_to_cold_start(self, tmp_path: Path, body: str) -> None:
        path = watermark_path(tmp_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        assert read_watermark(tmp_path) is None  # 坏水位不倒灌:回冷启动语义


# =====================================================================
# 单轮扫描
# =====================================================================


class TestScanRound:
    def test_gap_round_republishes_increments(self, env: dict) -> None:
        """断档间隙:旧水位 → 首轮如实补发窗口内全部行(PRD R6)。"""
        message_con = _open(env["message"])
        session_con = _open(env["session"])
        try:
            events, new_watermark = scan_round(session_con, message_con, NOW - 400)
        finally:
            message_con.close()
            session_con.close()
        chat_a_events = [e for e in events if e["chat_id"] == CHAT_A]
        assert len(chat_a_events) == 4  # 3 message.new + 1 message.revoke
        assert new_watermark == NOW - 300 + 40
        revoke = next(e for e in events if e["type"] == "message.revoke")
        # newmsgid ↔ server_id 配对到残留原消息:orig_preview ≤30 字(此处 24 字不截断)。
        assert revoke["orig_preview"] == "被撤回的原始消息内容超长也要截断到三十字以内检查"
        assert len(revoke["orig_preview"]) <= 30

    def test_cold_start_watermark_now_publishes_nothing(self, env: dict) -> None:
        """冷启动 watermark=now → 不倒灌历史(零事件,水位推进)。"""
        message_con = _open(env["message"])
        session_con = _open(env["session"])
        try:
            events, new_watermark = scan_round(session_con, message_con, NOW)
        finally:
            message_con.close()
            session_con.close()
        assert events == []
        assert new_watermark >= NOW  # 水位仍推进到表 max(供下轮起跳)

    def test_session_limit_is_50(self, tmp_path: Path) -> None:
        """60 会话在场只扫前 50(session 表自然序;扫描上限,PRD R6)。"""
        big = build_env(tmp_path, sessions=60, rows_per_chat=1)
        message_con = _open(big["message"])
        session_con = _open(big["session"])
        stats: dict = {}
        try:
            events, _wm = scan_round(session_con, message_con, NOW - 400, stats=stats)
        finally:
            message_con.close()
            session_con.close()
        assert stats["sessions_scanned"] == 50
        scanned_chats = {event["chat_id"] for event in events}
        assert len(scanned_chats) == 50
        assert big["chats"][59] not in {c for c in scanned_chats}

    def test_tail_window_escalates_when_increment_exceeds_window(
        self, tmp_path: Path
    ) -> None:
        """增量行数 > 尾窗基数 → 级数扩窗直到覆盖(免全库扫机制的完备面)。"""
        root = tmp_path
        db = root / "decrypted" / "message" / "message_0.db"
        db.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(db)
        con.execute("CREATE TABLE Name2Id (user_name TEXT PRIMARY KEY, is_session INTEGER)")
        cur = con.execute("INSERT INTO Name2Id VALUES (?, 1)", (CHAT_A,))
        sender = int(cur.lastrowid)
        con.execute(f'CREATE TABLE "{_table(CHAT_A)}" ({_msg_columns()})')
        for i in range(500):  # 500 行窗口内(> 默认尾窗 200 → 必扩窗)
            con.execute(
                f'INSERT INTO "{_table(CHAT_A)}" (local_id, server_id, local_type, '
                "sort_seq, real_sender_id, create_time, message_content) "
                "VALUES (?,?,?,?,?,?,?)",
                (i + 1, 40000 + i, 1, i + 1, sender, NOW - 500 + i, f"行{i}"),
            )
        con.commit()
        con.close()
        message_con = _open(db)
        try:
            colmap = {
                "talker": None,
                "time": "create_time",
                "type": "local_type",
                "content": "message_content",
                "sender": None,
                "sender_id": "real_sender_id",
                "ct_content": "WCDB_CT_message_content",
                "chat": CHAT_A,
            }
            stats: dict = {}
            events, chat_max = watermark.scan_session_increment(
                message_con,
                _table(CHAT_A),
                colmap,
                CHAT_A,
                NOW - 500,
                stats=stats,
            )
        finally:
            message_con.close()
        assert stats["tail_escalations"] >= 1
        assert len(events) == 500  # 扩窗后不丢行
        assert chat_max == NOW - 500 + 499

    def test_tail_window_cap_is_honest(self, tmp_path: Path) -> None:
        """增量 > 封顶 → 如实截断(不静默装全;消费端经 Pull 端点补)。"""
        root = tmp_path
        db = root / "decrypted" / "message" / "message_0.db"
        db.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(db)
        con.execute("CREATE TABLE Name2Id (user_name TEXT PRIMARY KEY, is_session INTEGER)")
        cur = con.execute("INSERT INTO Name2Id VALUES (?, 1)", (CHAT_A,))
        sender = int(cur.lastrowid)
        con.execute(f'CREATE TABLE "{_table(CHAT_A)}" ({_msg_columns()})')
        for i in range(300):
            con.execute(
                f'INSERT INTO "{_table(CHAT_A)}" (local_id, server_id, local_type, '
                "sort_seq, real_sender_id, create_time, message_content) "
                "VALUES (?,?,?,?,?,?,?)",
                (i + 1, 50000 + i, 1, i + 1, sender, NOW - 400 + i, f"行{i}"),
            )
        con.commit()
        con.close()
        message_con = _open(db)
        try:
            colmap = {
                "talker": None,
                "time": "create_time",
                "type": "local_type",
                "content": "message_content",
                "sender": None,
                "sender_id": "real_sender_id",
                "ct_content": "WCDB_CT_message_content",
                "chat": CHAT_A,
            }
            stats: dict = {}
            events, _chat_max = watermark.scan_session_increment(
                message_con,
                _table(CHAT_A),
                colmap,
                CHAT_A,
                NOW - 400,
                stats=stats,
                tail_max=256,
            )
        finally:
            message_con.close()
        assert stats["tail_capped"] == 1
        assert len(events) == 256  # 封顶如实截断


# =====================================================================
# R8 撤回解析
# =====================================================================


class TestRevokeParsing:
    def _row(self, **overrides) -> dict:
        row = {
            "rowid": 1,
            "ts": 100,
            "sender": "op",
            "local_type": 1,
            "text": "文本",
            "media_placeholder": None,
            "server_id": None,
        }
        row.update(overrides)
        return row

    def test_newmsgid_pairs_with_server_id(self) -> None:
        rows = [
            self._row(server_id=111, text="原文内容一二三四五六七八九十"),
            self._row(
                local_type=10002,
                ts=101,
                text=(
                    "<revokemsg><newmsgid>111</newmsgid>"
                    '<replacemsg><![CDATA["操作人" 撤回了一条消息]]></replacemsg></revokemsg>'
                ),
            ),
        ]
        events = parse_revoke_events(rows, "chat")
        assert len(events) == 1
        event = events[0]
        assert event["type"] == "message.revoke"
        assert event["sender"] == "操作人"  # replacemsg 引号名优先
        assert event["orig_preview"] == "原文内容一二三四五六七八九十"

    def test_missing_original_is_fact_only(self) -> None:
        """原消息缺失 = 仅撤回事实,不臆造内容(PRD R8)。"""
        rows = [
            self._row(
                local_type=10002,
                text="<revokemsg><newmsgid>999</newmsgid>"
                '<replacemsg><![CDATA["张三" 撤回了一条消息]]></replacemsg></revokemsg>',
            )
        ]
        events = parse_revoke_events(rows, "chat")
        assert events == [
            {"type": "message.revoke", "chat_id": "chat", "ts": 100, "sender": "张三"}
        ]  # 无 orig_preview 键:不臆造

    def test_operator_falls_back_to_row_sender(self) -> None:
        rows = [
            self._row(
                local_type=10002,
                sender="raw-wxid",
                text="<revokemsg><newmsgid>1</newmsgid></revokemsg>",
            )
        ]
        events = parse_revoke_events(rows, "chat")
        assert events[0]["sender"] == "raw-wxid"

    def test_non_revoke_and_shapeless_rows_ignored(self) -> None:
        assert parse_revoke_events([self._row()], "chat") == []
        assert parse_revoke_events([self._row(local_type=10002, text=None)], "chat") == []
        assert parse_revoke_events([self._row(local_type=10002, text="")], "chat") == []

    def test_preview_truncated_to_30(self) -> None:
        rows = [
            self._row(server_id=1, text="长" * 80),
            self._row(local_type=10002, text="<newmsgid>1</newmsgid>"),
        ]
        events = parse_revoke_events(rows, "chat")
        assert len(events[0]["orig_preview"]) == 30


# =====================================================================
# EventHub + SSE 续传
# =====================================================================


class TestEventHub:
    def test_publish_assigns_monotonic_ids_and_fanout(self) -> None:
        hub = EventHub(now_fn=lambda: 1.0)
        subscriber = hub.subscribe()
        first = hub.publish({"n": 1})
        second = hub.publish({"n": 2})
        assert (first, second) == (1, 2)
        assert subscriber.get(timeout=0.1) == (1, {"n": 1})
        assert subscriber.get(timeout=0.1) == (2, {"n": 2})
        hub.unsubscribe(subscriber)
        hub.publish({"n": 3})
        assert subscriber.empty()

    def test_resume_after_last_event_id(self) -> None:
        hub = EventHub(now_fn=lambda: 1.0)
        hub.publish_all([{"n": i} for i in range(10)])
        replay = hub.events_after(7)
        assert [eid for eid, _ in replay] == [8, 9, 10]

    def test_stale_subscriber_does_not_block_publisher(self) -> None:
        hub = EventHub(now_fn=lambda: 1.0, queue_max=1)
        subscriber = hub.subscribe()
        hub.publish({"n": 1})
        hub.publish({"n": 2})  # 队列满:丢弃该订阅者,不阻塞
        hub.publish({"n": 3})
        assert hub.latest_id() == 3


class TestScannerThread:
    def test_scan_once_full_round_with_injections(self, env: dict, tmp_path: Path) -> None:
        """注入链一轮:水位文件驱动(断档补发)→ 事件入 hub → 水位推进落盘。"""
        data_root = tmp_path / "home"
        write_watermark(data_root, NOW - 400)  # 断档水位:窗口内行全部补发
        message_con = _open(env["message"])
        session_con = _open(env["session"])

        # 注入 ensure:返回假副本目录(连接即开在真合成库上)。
        copy_info = {"dir": str(env["message"].parents[1])}
        hub = EventHub(now_fn=lambda: 1.0)
        scanner = WatermarkScanner(
            hub=hub,
            data_root=data_root,
            locate=lambda: Path("/fake/storage"),
            resolve=lambda storage: {"k": "v"},
            ensure=lambda storage, keys: copy_info,
            now_fn=lambda: float(NOW),
        )
        # _open_copy 走 copy_dir/rel:session 库与 message 库同根(decrypted/)。
        watermark_value = scanner.scan_once()
        message_con.close()
        session_con.close()
        assert watermark_value == NOW - 300 + 40  # 表 max 推进
        assert read_watermark(data_root) == NOW - 300 + 40
        events = [payload for _eid, payload in hub.events_after(0)]
        assert any(e["type"] == "message.revoke" for e in events)
        assert len(events) >= 8  # chat_a 4 + chat_b/wxid 各 ≥1

    def test_scan_failure_keeps_watermark(self, env: dict, tmp_path: Path) -> None:
        """密钥不可得(BridgeError):水位不推进(下轮补发间隙)。"""
        from wechat_bridge.codes import BridgeError

        data_root = tmp_path / "home"
        write_watermark(data_root, NOW - 1000)
        hub = EventHub(now_fn=lambda: 1.0)

        def broken_resolve(storage):
            raise BridgeError(21, "密钥缺位(合成)")

        scanner = WatermarkScanner(
            hub=hub,
            data_root=data_root,
            locate=lambda: Path("/fake/storage"),
            resolve=broken_resolve,
            ensure=lambda storage, keys: {},
        )
        with pytest.raises(BridgeError):
            scanner.scan_once()
        assert read_watermark(data_root) == NOW - 1000  # 未推进

    def test_cold_start_uses_now_no_backfill(self, env: dict, tmp_path: Path) -> None:
        data_root = tmp_path / "home"  # 无水位文件
        hub = EventHub(now_fn=lambda: 1.0)
        scanner = WatermarkScanner(
            hub=hub,
            data_root=data_root,
            locate=lambda: Path("/fake/storage"),
            resolve=lambda storage: {"k": "v"},
            ensure=lambda storage, keys: {"dir": str(env["message"].parents[1])},
            now_fn=lambda: float(NOW),
        )
        watermark_value = scanner.scan_once()
        assert hub.events_after(0) == []  # 冷启动不倒灌:零事件
        assert watermark_value >= NOW

    def test_thread_run_and_stop(self, env: dict, tmp_path: Path) -> None:
        hub = EventHub(now_fn=lambda: 1.0)
        scanner = WatermarkScanner(
            hub=hub,
            data_root=tmp_path / "home",
            locate=lambda: Path("/fake/storage"),
            resolve=lambda storage: {"k": "v"},
            ensure=lambda storage, keys: {"dir": str(env["message"].parents[1])},
            interval_seconds=0.05,
            now_fn=lambda: float(NOW),
        )
        scanner.start()
        deadline = time.time() + 3
        while time.time() < deadline and not hub.events_after(0) and scanner.last_watermark is None:
            time.sleep(0.02)
        scanner.stop()
        assert scanner.last_watermark is not None  # 至少一轮完成

    def test_sse_resume_via_last_event_id(self) -> None:
        hub = EventHub(now_fn=lambda: 1.0)
        hub.publish_all([{"n": 1}, {"n": 2}, {"n": 3}])
        frames = list(sse_stream(hub, 1, poll_timeout=0.01, max_frames=2))
        assert frames[0].startswith("id: 2\n")
        assert frames[1].startswith("id: 3\n")
