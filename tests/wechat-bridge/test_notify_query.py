"""notify_query 单测(10-14-wechat-notify-revoke R7;AC1/AC2 覆盖)。

合成库(sqlite 造 SessionTable + ``Msg_<md5>`` 分表 + Name2Id + contact,
DDL 照 2026-10-13/14 直查解密副本实测形状;内容全合成,零真实语料——
私有数据红线)。覆盖:

- 基线差分四候选分支(last_timestamp 前发/unread 变化/last_msg_type=10002/
  无基线)/非白名单零 Msg_ 查询(SQL trace 断言)/自消息过滤/首建基线
  零事件/LIMIT 上限/水位推进取 max;
- 撤回谓词四标记/恢复阶梯四级(server_id·heuristic·replacemsg·none;
  夹具驱动 = fixtures/revoke_samples.json)/自撤回不出/双到达抑制;
- 载荷 golden 形状(events/baseline/stats 键序逐键);
- busy 降级(monkeypatch 触发 locked → db_busy=true 零事件不判死)、
  副本侧索引懒建(idx_<表>_ct 命名/幂等)。
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any

import pytest

from wechat_bridge.codes import BridgeError
from wechat_bridge.notify_query import (
    LOOKBACK_SECONDS,
    ROW_LIMIT,
    ensure_ct_indexes,
    read_scan_payload,
    run_notify_scan,
    run_revoke_list,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures"
NOW = int(time.time())
CHAT = "50438708676@chatroom"  # 形状照真实 chatroom 形态;非任何真实会话内容
OTHER_CHAT = "wxid_other_party"
SELF_WXID = "wxid_self"

_DDL_415 = (
    "(local_id INTEGER PRIMARY KEY AUTOINCREMENT, server_id INTEGER, "
    "local_type INTEGER, sort_seq INTEGER, real_sender_id INTEGER, "
    "create_time INTEGER, status INTEGER, upload_status INTEGER, "
    "download_status INTEGER, server_seq INTEGER, origin_source INTEGER, "
    "source TEXT, message_content TEXT, compress_content TEXT, "
    "packed_info_data BLOB, WCDB_CT_message_content INTEGER DEFAULT NULL, "
    "WCDB_CT_source INTEGER DEFAULT NULL)"
)

_SESSION_DDL = (
    "(username TEXT PRIMARY KEY, unread_count INTEGER, last_timestamp INTEGER, "
    "last_msg_type INTEGER, summary TEXT, last_sender_display_name TEXT)"
)


def _md5hex(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()


def _msg_row(
    local_id: int, server_id: int, local_type: int, create_time: int,
    sender_id: int, content: str, sort_seq: int | None = None,
) -> tuple:
    return (
        local_id, server_id, local_type, sort_seq or local_id, sender_id,
        create_time, 1, 0, 0, 0, 0, "", content, None, None, None, None,
    )


def _insert(con: sqlite3.Connection, table: str, rows: list[tuple]) -> None:
    con.executemany(
        f'INSERT INTO "{table}" VALUES ({",".join("?" * 17)})', rows
    )


def build_copies(
    root: Path,
    *,
    session_rows: list[tuple],
    chat_rows: dict[str, list[tuple]] | None = None,
    with_contact: bool = True,
) -> Path:
    """合成解密副本(session + message 分表 + Name2Id + contact)。"""
    copy_dir = root / "decrypted"
    session_db = copy_dir / "session" / "session.db"
    session_db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(session_db)
    con.execute(f'CREATE TABLE "SessionTable" {_SESSION_DDL}')
    con.executemany(
        'INSERT INTO "SessionTable" (username, unread_count, last_timestamp,'
        " last_msg_type, summary, last_sender_display_name)"
        " VALUES (?,?,?,?,?,?)",
        [(r[0], r[1], r[2], r[3], r[4] if len(r) > 4 else "", r[5] if len(r) > 5 else None)
         for r in session_rows],
    )
    con.commit()
    con.close()

    msg_db = copy_dir / "message" / "message_0.db"
    msg_db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(msg_db)
    con.execute(
        "CREATE TABLE Name2Id(user_name TEXT PRIMARY KEY, is_session INTEGER)"
    )
    for rid, name, sess in (
        (10, SELF_WXID, 0),
        (20, "wxid_alice", 0),
        (30, CHAT, 1),
        (40, OTHER_CHAT, 1),
    ):
        con.execute(
            "INSERT INTO Name2Id(rowid, user_name, is_session) VALUES (?,?,?)",
            (rid, name, sess),
        )
    for chat, rows in (chat_rows or {}).items():
        table = "Msg_" + _md5hex(chat)
        con.execute(f'CREATE TABLE "{table}"{_DDL_415}')
        _insert(con, table, rows)
    con.commit()
    con.close()

    if with_contact:
        contact_db = copy_dir / "contact" / "contact.db"
        contact_db.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(contact_db)
        con.execute(
            "CREATE TABLE contact (username TEXT PRIMARY KEY, alias TEXT,"
            " nickname TEXT, remark TEXT, localType INTEGER)"
        )
        con.execute(
            "INSERT INTO contact VALUES (?,?,?,?,1)",
            (CHAT, None, "合成群聊名", "合成群备注"),
        )
        con.execute(
            "INSERT INTO contact VALUES (?,?,?,?,1)",
            ("wxid_alice", None, "合成爱丽丝", None),
        )
        con.commit()
        con.close()
    return copy_dir


# ---------------------------------------------------------------------------
# R1.1 基线差分:四候选分支 + 非白名单零二次查询 + 水位取 max
# ---------------------------------------------------------------------------


class TestBaselineDiff:
    def _copies(self, tmp_path: Path) -> Path:
        return build_copies(
            tmp_path,
            session_rows=[
                (CHAT, 3, NOW - 30, 1, "", None),          # ts 前进候选
                (OTHER_CHAT, 0, NOW - 30, 1, "", None),    # 白名单外(同变化)
            ],
            chat_rows={
                CHAT: [
                    _msg_row(1, 101, 1, NOW - 60, 20, "合成-候选会话新消息"),
                    _msg_row(2, 102, 1, NOW - 600, 20, "合成-十分钟前旧消息"),
                ],
                OTHER_CHAT: [
                    _msg_row(1, 201, 1, NOW - 60, 10, "合成-白名单外不该出现"),
                ],
            },
        )

    def test_ts_advance_is_candidate_and_events(self, tmp_path: Path) -> None:
        copies = self._copies(tmp_path)
        payload = run_notify_scan(
            copy_dir=copies,
            whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        assert [e["event"] for e in node["events"]] == ["message.new"]
        event = node["events"][0]
        assert event["session_id"] == CHAT
        assert event["session_display"] == "合成群备注"  # contact remark > nickname 优先
        assert event["sender_display"] == "合成爱丽丝"
        assert event["is_self"] is False
        assert event["content_preview"] == "合成-候选会话新消息"
        assert event["server_id"] == 101
        # 水位推进取 max(旧 300s 前 < SessionTable last_timestamp)
        assert node["baseline"][CHAT] == {"ts": NOW - 30, "unread": 3}
        assert node["stats"]["candidates"] == 1
        assert node["stats"]["sessions_scanned"] == 2
        assert node["stats"]["whitelist_sessions"] == 1

    def test_unread_change_is_candidate_even_without_ts_move(self, tmp_path: Path) -> None:
        copies = self._copies(tmp_path)
        payload = run_notify_scan(
            copy_dir=copies,
            whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 30, "unread": 0}},  # unread 3 != 0
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        # 窗口 = ts-90s:一条新消息在窗内(60s 前)
        assert [e["content_preview"] for e in node["events"]] == ["合成-候选会话新消息"]
        assert node["stats"]["candidates"] == 1

    def test_revoke_last_msg_type_is_candidate_without_row_diff(self, tmp_path: Path) -> None:
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 300, 10002, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 320, 20, "合成-撤回窗内原文")]},
        )
        payload = run_notify_scan(
            copy_dir=copies,
            whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},  # ts/unread 全同
            self_name=SELF_WXID,
        )
        assert payload["notify_scan"]["stats"]["candidates"] == 1

    def test_no_change_no_candidate_zero_msg_query(self, tmp_path: Path) -> None:
        copies = self._copies(tmp_path)
        payload = run_notify_scan(
            copy_dir=copies,
            whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 30, "unread": 3}},
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        assert node["events"] == []
        assert node["stats"]["candidates"] == 0
        assert node["stats"]["msg_rows_read"] == 0

    def test_non_whitelist_zero_msg_query_sql_trace(self, tmp_path: Path, monkeypatch) -> None:
        """非白名单零二次查询:SQL trace 断言白名单外分表零触碰(AC1)。"""
        import wechat_bridge.notify_query as nq

        copies = self._copies(tmp_path)
        statements: list[str] = []
        real_open = nq._open_copy

        def traced_open(copy_dir: Path, rel: str):
            con = real_open(copy_dir, rel)
            if con is not None and "message" in rel:
                con.set_trace_callback(lambda statement: statements.append(statement))
            return con

        monkeypatch.setattr(nq, "_open_copy", traced_open)
        run_notify_scan(
            copy_dir=copies,
            whitelist=[CHAT],  # OTHER_CHAT 同样 ts 前进,但白名单外
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID,
        )
        other_table = "Msg_" + _md5hex(OTHER_CHAT)
        chat_table = "Msg_" + _md5hex(CHAT)
        # 表发现(PRAGMA table_info/sqlite_master)允许提及;**数据面 SELECT**
        # 只许白名单内分表——白名单外零二次查询(R1.1)。
        selects = [s for s in statements if s.lstrip().upper().startswith("SELECT")]
        assert any(f'FROM "{chat_table}"' in s for s in selects)  # 白名单内被点查
        assert not any(
            other_table in s for s in selects
        ), "白名单外分表被数据查询触碰(违反 R1.1 零二次查询)"

    def test_missing_baseline_row_kept_for_absent_session(self, tmp_path: Path) -> None:
        """白名单会话从 SessionTable 消失:保旧基线零信号(不臆造 0)。"""
        copies = self._copies(tmp_path)
        payload = run_notify_scan(
            copy_dir=copies,
            whitelist=["wxid_ghost"],
            baseline={"wxid_ghost": {"ts": NOW - 50, "unread": 2}},
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        assert node["events"] == []
        assert node["baseline"] == {"wxid_ghost": {"ts": NOW - 50, "unread": 2}}

    def test_watermark_takes_max_when_session_row_older(self, tmp_path: Path) -> None:
        """水位取 max:SessionTable.last_timestamp 比旧基线旧 → 保旧值。"""
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 1, NOW - 3600, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 7200, 20, "合成-旧消息")]},
        )
        payload = run_notify_scan(
            copy_dir=copies,
            whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 60, "unread": 1}},
            self_name=SELF_WXID,
        )
        assert payload["notify_scan"]["baseline"][CHAT]["ts"] == NOW - 60


class TestFirstRoundAndLimit:
    def test_first_round_builds_baseline_zero_events(self, tmp_path: Path) -> None:
        """首建基线零事件 + 初值 now(不看 last_timestamp,防首弹轰炸)。"""
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成-首轮不该弹")]},
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT], baseline=None,
            self_name=SELF_WXID, now=NOW,
        )
        node = payload["notify_scan"]
        assert node["events"] == []
        assert node["baseline"][CHAT] == {"ts": NOW, "unread": 3}
        assert node["stats"]["msg_rows_read"] == 0  # 连 Msg_ 查询都不发
        assert node["stats"]["candidates"] == 1

    def test_first_round_lookback_catches_inflight_messages(self, tmp_path: Path) -> None:
        """首轮进行中到达的消息:次轮 lookback 90s 兜住(初值 now 语义)。"""
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW + 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW + 10, 20, "合成-首轮进行中到达")]},
        )
        first = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT], baseline=None,
            self_name=SELF_WXID, now=NOW,
        )
        assert first["notify_scan"]["events"] == []
        baseline = first["notify_scan"]["baseline"]
        second = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT], baseline=baseline,
            self_name=SELF_WXID, now=NOW + 60,
        )
        assert [
            e["content_preview"] for e in second["notify_scan"]["events"]
        ] == ["合成-首轮进行中到达"]

    def test_row_limit_truncates(self, tmp_path: Path) -> None:
        rows = [
            _msg_row(i, 500 + i, 1, NOW - i, 20, f"合成-第{i}条")
            for i in range(1, ROW_LIMIT + 5)
        ]
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 1, 1, "", None)],
            chat_rows={CHAT: rows},
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 400, "unread": 3}},
            self_name=SELF_WXID, index_tables=False,
        )
        node = payload["notify_scan"]
        assert node["stats"]["msg_rows_read"] == ROW_LIMIT
        assert len(node["events"]) == ROW_LIMIT
        # ASC 输出:最新一条(第 1 条,NOW-1)在末尾
        assert node["events"][-1]["content_preview"] == "合成-第1条"


class TestSelfFilter:
    def test_self_messages_filtered_and_counted(self, tmp_path: Path) -> None:
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 10, 1, "", None)],
            chat_rows={
                CHAT: [
                    _msg_row(1, 101, 1, NOW - 60, 20, "合成-对方消息"),
                    _msg_row(2, 102, 1, NOW - 50, 10, "wxid_self:\n合成-我的消息"),
                ]
            },
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        assert [e["content_preview"] for e in node["events"]] == ["合成-对方消息"]
        assert node["stats"]["self_filtered"] == 1

    def test_notify_self_passes_self_messages(self, tmp_path: Path) -> None:
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 10, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 102, 1, NOW - 50, 10, "合成-我的消息")]},
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID, notify_self=True,
        )
        node = payload["notify_scan"]
        assert [e["content_preview"] for e in node["events"]] == ["合成-我的消息"]
        assert node["events"][0]["is_self"] is True

    def test_no_self_wxid_degrades_to_unfiltered(self, tmp_path: Path) -> None:
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 10, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 102, 1, NOW - 50, 10, "合成-无从判自")]},
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=None,
        )
        assert len(payload["notify_scan"]["events"]) == 1


# ---------------------------------------------------------------------------
# R1.3 撤回:谓词四标记 + 恢复阶梯(夹具驱动)+ 自撤回 + 双到达抑制
# ---------------------------------------------------------------------------


class TestRevokePredicate:
    @pytest.mark.parametrize(
        "marker",
        ["revokemsg", "<replacemsg", "撤回了一条消息", "尝试撤回此消息"],
    )
    def test_system_row_with_marker_is_revoke(self, marker: str) -> None:
        from wechat_bridge.notify_query import is_revoke_row

        assert is_revoke_row(10000, f"前缀 {marker} 后缀")

    def test_system_row_without_marker_is_not_revoke(self) -> None:
        from wechat_bridge.notify_query import is_revoke_row

        assert not is_revoke_row(10000, "某某某 邀请你加入群聊")
        assert not is_revoke_row(1, "revokemsg 出现在普通文本也不算")


class TestRecoveryLadder:
    """fixtures/revoke_samples.json 驱动:四级恢复 + 自撤回(AC2 主诉)。"""

    @pytest.fixture()
    def samples(self) -> dict[str, Any]:
        return json.loads(
            (FIXTURES / "revoke_samples.json").read_text(encoding="utf-8")
        )

    def _build_case(self, tmp_path: Path, case: dict[str, Any], base_ts: int) -> Path:
        revoke_ts = base_ts - 10
        rows: list[tuple] = []
        local_id = 1
        for fixture_row in case["fixture_rows"]:
            rows.append(
                _msg_row(
                    local_id,
                    fixture_row["server_id"],
                    1,
                    revoke_ts + fixture_row["create_time_offset"],
                    fixture_row["real_sender_id"],
                    fixture_row["message_content"],
                )
            )
            local_id += 1
        rows.append(
            _msg_row(
                local_id,
                9000000000 + local_id,
                case["revoke_row"]["local_type"],
                revoke_ts,
                case["revoke_row"].get("real_sender_id", 20),
                case["revoke_row"]["message_content"],
            )
        )
        return build_copies(
            tmp_path,
            session_rows=[(CHAT, 0, revoke_ts, case["revoke_row"]["local_type"], "", None)],
            chat_rows={CHAT: rows},
        )

    @pytest.mark.parametrize("case_index", range(6))
    def test_case(self, tmp_path: Path, samples: dict[str, Any], case_index: int) -> None:
        case = samples["cases"][case_index]
        base_ts = NOW  # 平移到当前时刻(revoke-list since 窗口语义才可判)
        copies = self._build_case(tmp_path, case, base_ts)
        payload = run_revoke_list(
            copy_dir=copies, chat_id=CHAT, since_days=1,
            self_name=SELF_WXID, now=base_ts,
        )
        expect = case["expect"]
        node = payload["revoke_list"]
        if expect.get("suppressed"):
            assert node == []
            assert payload["stats"]["self_revoked"] == 1
            return
        assert len(node) == 1, case["name"]
        entry = node[0]
        assert entry["event"] == "message.revoke"
        assert entry["session_display"] == "合成群备注"
        assert entry["is_self_revoke"] is False
        original = entry["original"]
        if expect["recovery"] in ("server_id", "heuristic"):
            assert original is not None, case["name"]
            assert original["recovery"] == expect["recovery"]
            assert original["server_id"] == expect["original_server_id"]
            assert expect["original_preview_contains"] in original["content_preview"]
        else:
            assert original is None, case["name"]
            assert entry["replacemsg_text"] == expect.get("replacemsg_text")
            recovery_counts = payload["stats"]["recovery"]
            assert recovery_counts[expect["recovery"]] == 1

    def test_double_arrival_suppression(self, tmp_path: Path) -> None:
        """同撤回双到达抑制:恢复出的原消息不再另发新消息事件(R1.3 附)。"""
        revoke_ts = NOW - 10
        rows = [
            _msg_row(1, 700123, 1, NOW - 60, 20, "合成-将被撤回的原文"),
            _msg_row(
                2, 900001, 10002, revoke_ts, 20,
                '<sysmsg type="revokemsg"><revokemsg><newmsgid>700123</newmsgid>'
                "</revokemsg></sysmsg>",
            ),
        ]
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 0, revoke_ts, 10002, "", None)],
            chat_rows={CHAT: rows},
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 0}},
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        assert [e["event"] for e in node["events"]] == ["message.revoke"]
        assert node["stats"]["revoke_events"] == 1
        assert node["events"][0]["original"]["server_id"] == 700123
        # 双到达抑制:new 事件不重复出现(server_id 700123 已被恢复消费)

    def test_revoke_list_self_revoke_marker_suppresses(self, tmp_path: Path) -> None:
        """内容含「你撤回」= 自撤回不出事件(他人手机上撤回自己消息形态)。"""
        rows = [
            _msg_row(
                1, 900002, 10002, NOW - 10, 20,
                "<sysmsg><revokemsg><newmsgid>1</newmsgid>你撤回了一条消息"
                "</revokemsg></sysmsg>",
            ),
        ]
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 0, NOW - 10, 10002, "", None)],
            chat_rows={CHAT: rows},
        )
        payload = run_revoke_list(
            copy_dir=copies, chat_id=CHAT, since_days=1,
            self_name=SELF_WXID, now=NOW,
        )
        assert payload["revoke_list"] == []
        assert payload["stats"]["self_revoked"] == 1


# ---------------------------------------------------------------------------
# 载荷 golden 形状 + busy 降级 + 索引懒建
# ---------------------------------------------------------------------------


class TestPayloadShape:
    def test_notify_scan_golden_shape(self, tmp_path: Path) -> None:
        """载荷 golden 形状:events/baseline/stats 三节 + 事件键序逐键(AC1)。"""
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成-形状消息")]},
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID, now=NOW, index_tables=False,
        )
        assert list(payload.keys()) == ["notify_scan"]
        node = payload["notify_scan"]
        assert list(node.keys()) == ["events", "baseline", "stats"]
        event = node["events"][0]
        assert list(event.keys()) == [
            "event", "session_id", "session_display", "sender_display",
            "is_self", "content_preview", "ts", "server_id", "local_type",
        ]
        assert list(node["stats"].keys()) == [
            "sessions_scanned", "whitelist_sessions", "candidates",
            "msg_rows_read", "self_filtered", "revoke_events", "db_busy",
            "duration_ms",
        ]
        assert isinstance(node["stats"]["duration_ms"], int)

    def test_revoke_event_shape(self, tmp_path: Path) -> None:
        revoke_ts = NOW - 10
        rows = [
            _msg_row(1, 700777, 1, NOW - 60, 20, "合成-撤回原文"),
            _msg_row(2, 900003, 10002, revoke_ts, 20,
                     '<sysmsg><revokemsg><newmsgid>700777</newmsgid></revokemsg></sysmsg>'),
        ]
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 0, revoke_ts, 10002, "", None)],
            chat_rows={CHAT: rows},
        )
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 0}},
            self_name=SELF_WXID,
        )
        event = payload["notify_scan"]["events"][0]
        assert list(event.keys()) == [
            "event", "session_id", "session_display", "revoker_display",
            "is_self_revoke", "ts", "server_id", "local_type",
            "original", "replacemsg_text",
        ]
        assert list(event["original"].keys()) == [
            "server_id", "ts", "sender_display", "content_preview", "recovery",
        ]


class TestBusyDegrade:
    def test_busy_session_read_degrades_to_zero_events(self, tmp_path: Path, monkeypatch) -> None:
        """sqlite busy → 本轮跳过不判死(db_busy=true;基线原样回传)。"""
        import wechat_bridge.notify_query as nq

        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成-busy 轮消息")]},
        )

        def busy_read(con):
            raise sqlite3.OperationalError("database is locked")

        monkeypatch.setattr(nq, "_read_session_rows", busy_read)
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        assert node["events"] == []
        assert node["stats"]["db_busy"] is True
        assert node["baseline"] == {CHAT: {"ts": NOW - 300, "unread": 3}}  # 不推进

    def test_busy_msg_query_keeps_old_baseline(self, tmp_path: Path, monkeypatch) -> None:
        import wechat_bridge.notify_query as nq

        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成-busy 轮消息")]},
        )

        def busy_fetch(*args, **kwargs):
            return None

        monkeypatch.setattr(nq, "_fetch_recent_rows", busy_fetch)
        payload = run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID,
        )
        node = payload["notify_scan"]
        assert node["events"] == []
        assert node["stats"]["db_busy"] is True
        assert node["baseline"][CHAT] == {"ts": NOW - 300, "unread": 3}

    def test_non_busy_sqlite_error_is_decrypt_failed(self, tmp_path: Path, monkeypatch) -> None:
        import wechat_bridge.notify_query as nq

        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成")]},
        )

        def corrupt(con):
            raise sqlite3.OperationalError("no such column: bogus")

        monkeypatch.setattr(nq, "_read_session_rows", corrupt)
        with pytest.raises(BridgeError) as excinfo:
            run_notify_scan(
                copy_dir=copies, whitelist=[CHAT],
                baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
                self_name=SELF_WXID,
            )
        assert excinfo.value.exit_code == 22

    def test_missing_message_copy_is_decrypt_failed(self, tmp_path: Path) -> None:
        copies = build_copies(
            tmp_path, session_rows=[(CHAT, 3, NOW - 30, 1, "", None)], chat_rows={},
        )
        (copies / "message" / "message_0.db").unlink()
        with pytest.raises(BridgeError) as excinfo:
            run_notify_scan(
                copy_dir=copies, whitelist=[CHAT],
                baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
                self_name=SELF_WXID,
            )
        assert excinfo.value.exit_code == 22


class TestCopyIndexes:
    def test_lazy_index_naming_and_idempotency(self, tmp_path: Path) -> None:
        """idx_<表>_ct 命名(C1 统一索引方案同规)+ 幂等二次零新建。"""
        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成")]},
        )
        table = "Msg_" + _md5hex(CHAT)
        created = ensure_ct_indexes(copies, [(table, "create_time")])
        assert created == [f"idx_{table}_ct"]
        again = ensure_ct_indexes(copies, [(table, "create_time")])
        assert again == []  # 幂等:已存在不再计新建
        con = sqlite3.connect(f"file:{copies / 'message' / 'message_0.db'}?mode=ro", uri=True)
        try:
            names = [
                row[0]
                for row in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='index'"
                )
            ]
        finally:
            con.close()
        assert f"idx_{table}_ct" in names

    def test_scan_builds_index_only_for_candidates(self, tmp_path: Path) -> None:
        copies = build_copies(
            tmp_path,
            session_rows=[
                (CHAT, 3, NOW - 30, 1, "", None),
                (OTHER_CHAT, 3, NOW - 30, 1, "", None),
            ],
            chat_rows={
                CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成-候选")],
                OTHER_CHAT: [_msg_row(1, 201, 1, NOW - 60, 10, "合成-白名单外")],
            },
        )
        run_notify_scan(
            copy_dir=copies, whitelist=[CHAT],
            baseline={CHAT: {"ts": NOW - 300, "unread": 3}},
            self_name=SELF_WXID,
        )
        con = sqlite3.connect(f"file:{copies / 'message' / 'message_0.db'}?mode=ro", uri=True)
        try:
            names = [
                row[0]
                for row in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='index'"
                )
            ]
        finally:
            con.close()
        assert f"idx_Msg_{_md5hex(CHAT)}_ct" in names
        assert f"idx_Msg_{_md5hex(OTHER_CHAT)}_ct" not in names  # 懒建:仅候选


# ---------------------------------------------------------------------------
# stdin 载荷契约(R1.4)
# ---------------------------------------------------------------------------


class TestReadScanPayload:
    def test_minimal_and_full_shapes(self) -> None:
        assert read_scan_payload('{"whitelist": ["a@chatroom"]}') == {
            "whitelist": ["a@chatroom"], "baseline": {}, "notify_self": False,
        }
        assert read_scan_payload(
            '{"whitelist": [" a@chatroom "], "baseline": null, "notify_self": true}'
        ) == {
            "whitelist": ["a@chatroom"], "baseline": {}, "notify_self": True,
        }
        assert read_scan_payload(
            '{"whitelist": ["a"], "baseline": {"a": {"ts": 1, "unread": 2}}}'
        )["baseline"] == {"a": {"ts": 1, "unread": 2}}

    @pytest.mark.parametrize(
        "text",
        [
            "",
            "   ",
            "not-json",
            "[1, 2]",
            '{"baseline": {}}',                       # whitelist 缺席
            '{"whitelist": []}',                       # 空清单
            '{"whitelist": ["a", 3]}',                 # 非字符串成员
            '{"whitelist": ["a"], "baseline": [1]}',   # baseline 非对象
            '{"whitelist": ["a"], "notify_self": "yes"}',
        ],
    )
    def test_bad_shapes_are_usage(self, text: str) -> None:
        with pytest.raises(BridgeError) as excinfo:
            read_scan_payload(text)
        assert excinfo.value.exit_code == 2
        assert excinfo.value.name == "usage"


# ---------------------------------------------------------------------------
# 编排(monkeypatch 隔离;真数据干跑归复查员 realRunCommand)
# ---------------------------------------------------------------------------


class TestOrchestration:
    def _fake_config(self):
        from wechat_bridge.config import BridgeConfig

        return BridgeConfig()

    def test_notify_scan_orchestration_wires_copy_dir(self, tmp_path: Path, monkeypatch) -> None:
        import wechat_bridge.notify_query as nq

        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 3, NOW - 30, 1, "", None)],
            chat_rows={CHAT: [_msg_row(1, 101, 1, NOW - 60, 20, "合成-编排消息")]},
        )
        seen: dict[str, Any] = {}

        def fake_ensure(config, db_storage, keys, domains, *, data_root, now):
            seen["domains"] = list(domains)
            return {"dir": str(copies), "built": [], "kept": [], "skipped": [], "total_bytes": 0}

        monkeypatch.setattr(nq, "_ensure_and_heal", fake_ensure)
        monkeypatch.setattr(nq, "login_wxid", lambda db_storage: SELF_WXID)
        payload = nq.notify_scan(
            self._fake_config(), tmp_path, {"k": "v"},
            {"whitelist": [CHAT], "baseline": {CHAT: {"ts": NOW - 300, "unread": 3}}},
            now=NOW,
        )
        assert seen["domains"] == ["message", "session", "contact"]
        assert [e["content_preview"] for e in payload["notify_scan"]["events"]] == [
            "合成-编排消息"
        ]

    def test_revoke_list_orchestration_domains(self, tmp_path: Path, monkeypatch) -> None:
        import wechat_bridge.notify_query as nq

        copies = build_copies(
            tmp_path,
            session_rows=[(CHAT, 0, NOW - 10, 10002, "", None)],
            chat_rows={CHAT: [
                _msg_row(1, 7001, 1, NOW - 60, 20, "合成-原文"),
                _msg_row(2, 9004, 10002, NOW - 10, 20,
                         '<sysmsg><revokemsg><newmsgid>7001</newmsgid></revokemsg></sysmsg>'),
            ]},
        )
        seen: dict[str, Any] = {}

        def fake_ensure(config, db_storage, keys, domains, *, data_root, now):
            seen["domains"] = list(domains)
            return {"dir": str(copies), "built": [], "kept": [], "skipped": [], "total_bytes": 0}

        monkeypatch.setattr(nq, "_ensure_and_heal", fake_ensure)
        monkeypatch.setattr(nq, "login_wxid", lambda db_storage: None)
        payload = nq.revoke_list(self._fake_config(), tmp_path, {"k": "v"}, CHAT, 1, now=NOW)
        assert seen["domains"] == ["message", "contact"]
        assert payload["stats"]["recovery"]["server_id"] == 1
