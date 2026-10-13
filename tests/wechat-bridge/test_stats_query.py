"""统计查询层单测(task 10-14-wechat-stats-reports AC1/AC4/AC5)。

夹具形态 = 4.1.15 分表(``Msg_<md5(username)>`` 无会话列 + ``Name2Id``
反查 + ``WCDB_CT`` 压缩列)混居旧形态宽表(isSender),内容全合成(红线
6:零真实语料入库)。**SQL 聚合 vs Python 全量游标累加双算互证**:测试内
持一份纯 Python 参考实现(与 stats_query 的 SQL 路径零共享代码),两树
逐字段相等(AC1)。

时区钉 UTC(``TZ`` env + ``tzset``):strftime ``'localtime'`` 与
``time.localtime`` 同源,桶值可逐位断言。缓存用例钉:命中/未命中/副本
指纹失效/``--refresh`` 旁路/同键重算逐字节一致(AC4/AC5)。
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
import statistics
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pytest

from bridge_testkit import COMPONENT_SRC

if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))

from wechat_bridge import stats_query  # noqa: E402
from wechat_bridge.stats_query import TYPE_COUNT_KEYS  # noqa: E402

# 时区钉 UTC:strftime('localtime') 与 time.localtime 同源(同 libc,
# macOS 实测 SQLite 亦随 TZ env + tzset 走);夹具时间戳按 UTC 设计桶值。
# 本模块按字典序在 test_sns_query 之后导入,桥测试族内无后继文件受
# TZ 全局态影响。
os.environ["TZ"] = "UTC"
time.tzset()

#: 夹具基准时刻(2023-11-14 02:30:00 UTC,周二;深夜 0-5:59 桶内)。
BASE = int(datetime(2023, 11, 14, 2, 30, 0, tzinfo=timezone.utc).timestamp())
NOW = BASE + 30 * 86400  # 窗口右界(注入 now,不取墙钟)

SELF = "wxid_me"
FRIEND = "wxid_friend"
GROUP = "12345678@chatroom"
OFFICIAL = "gh_official"
HELPER = "filehelper"
ALIAS_FRIEND = "wxid_alias"
UNATTRIBUTED_TABLE = "Msg_" + "0" * 32  # Name2Id 反解不出 → unattributed

_DDL = (
    "(local_id INTEGER PRIMARY KEY AUTOINCREMENT, server_id INTEGER, "
    "local_type INTEGER, sort_seq INTEGER, real_sender_id INTEGER, "
    "create_time INTEGER, status INTEGER, upload_status INTEGER, "
    "download_status INTEGER, server_seq INTEGER, origin_source INTEGER, "
    "source TEXT, message_content TEXT, compress_content TEXT, "
    "packed_info_data BLOB, WCDB_CT_message_content INTEGER DEFAULT NULL, "
    "WCDB_CT_source INTEGER DEFAULT NULL)"
)

_NAME2ID_ROWS = [
    (1, SELF, 0),
    (2, FRIEND, 0),
    (3, GROUP, 1),
    (4, OFFICIAL, 1),
    (5, HELPER, 1),
    (6, ALIAS_FRIEND, 0),
    (7, "", 0),  # 空串 user_name(真库实证存在;反查回落会话,不投票)
    (8, "wxid_member_a", 0),
]


def _md5hex(name: str) -> str:
    return hashlib.md5(name.encode("utf-8")).hexdigest()


def _uid(name: str) -> int:
    return next(rid for rid, n, _s in _NAME2ID_ROWS if n == name)


#: 合成行:(chat, local_type, sender_name, create_time, content)。
CHAT_ROWS: list[tuple[str, int, str, int, str]] = [
    # —— 群(GROUP):多发送者 + 各类型 + 会话/响应形态 ——
    (GROUP, 1, FRIEND, BASE, "早上好"),                       # 03:00 周二
    (GROUP, 1, SELF, BASE + 60, "早上好"),                    # 异向 60s → 响应对
    (GROUP, 1, "wxid_member_a", BASE + 3600, "大家好大家好"),  # 同向不采样
    (GROUP, 3, FRIEND, BASE + 7200, "img"),                   # image
    (GROUP, 34, SELF, BASE + 7300, "v"),                      # voice
    (GROUP, 43, FRIEND, BASE + 7400, "v"),                    # video
    (GROUP, 47, SELF, BASE + 7500, "s"),                      # sticker
    (GROUP, 48, FRIEND, BASE + 7600, "loc"),                  # location
    (GROUP, 49, SELF, BASE + 7700, "f"),                      # file_or_link
    (GROUP, 99999, FRIEND, BASE + 7800, "x"),                 # other 桶
    (GROUP, 10000, FRIEND, BASE + 7900, "<sysmsg>"),          # system(不计人指标)
    (GROUP, 10002, SELF, BASE + 7950, "rev"),                 # revoke
    # 距上条 >30 分钟(3600s)→ 新会话,首条方向 me
    (GROUP, 1, SELF, BASE + 7200 + 3600, "第二会话我开的"),
    # 距上条 >24h 的异向对 → 不进响应采样
    (GROUP, 1, FRIEND, BASE + 86400 * 2, "很久之后"),
    # —— 私聊(FRIEND):短语 + streak + 窗口外行 ——
    (FRIEND, 1, FRIEND, BASE, "机器学习真有趣"),
    (FRIEND, 1, SELF, BASE + 10, "机器学习是吧"),
    (FRIEND, 1, FRIEND, BASE + 20, "对的 Machine Learning rocks"),
    (FRIEND, 1, SELF, BASE + 30, "okok okok okok"),           # ok×6 ≥3
    (FRIEND, 1, FRIEND, BASE + 86400, "第二天继续 Machine machine machine"),
    (FRIEND, 1, SELF, BASE + 86400 + 30, "嗯嗯"),
    (FRIEND, 1, FRIEND, BASE + 86400 * 3, "隔一天再来"),       # streak 断
    (FRIEND, 1, FRIEND, BASE + 86400 * 3 + 60, "机器学习"),    # 连续同日
    (FRIEND, 3, SELF, BASE + 86400 * 3 + 120, "img"),
    (FRIEND, 1, FRIEND, BASE - 40 * 86400, "窗口外应被滤掉"),  # --all 之外无:恒入
    # —— 官号/系统账号(annual 私谈集排除面)——
    (OFFICIAL, 1, OFFICIAL, BASE + 100, "官号推文"),
    (HELPER, 1, HELPER, BASE + 200, "文件传输助手消息"),
    # —— 另一私聊(friend_contrast / top_chats 第二名)——
    (ALIAS_FRIEND, 1, ALIAS_FRIEND, BASE + 5, "hello hello hello"),
    (ALIAS_FRIEND, 1, SELF, BASE + 15, "world world world"),
]


def _build_copies(root: Path) -> Path:
    """合成 4.1.15 副本:message 库(分表+宽表混居+归属不明表)+ contact 库。"""
    msg_dir = root / "message"
    msg_dir.mkdir(parents=True)
    con = sqlite3.connect(msg_dir / "message_0.db")
    con.execute("CREATE TABLE Name2Id(user_name TEXT PRIMARY KEY, is_session INTEGER)")
    con.executemany(
        "INSERT INTO Name2Id(rowid, user_name, is_session) VALUES (?,?,?)",
        _NAME2ID_ROWS,
    )
    by_chat: dict[str, list[tuple[str, int, str, int, str]]] = {}
    for row in CHAT_ROWS:
        by_chat.setdefault(row[0], []).append(row)
    for chat, rows in by_chat.items():
        table = "Msg_" + _md5hex(chat)
        con.execute(f'CREATE TABLE "{table}"{_DDL}')
        for i, (_c, lt, sender, ts, content) in enumerate(rows, start=1):
            con.execute(
                f'INSERT INTO "{table}" (local_id, server_id, local_type, sort_seq, '
                "real_sender_id, create_time, status, upload_status, download_status, "
                "server_seq, origin_source, source, message_content, compress_content, "
                "packed_info_data, WCDB_CT_message_content, WCDB_CT_source) "
                "VALUES (?,?,?,?,?,?,1,0,0,0,0,'',?,NULL,NULL,NULL,NULL)",
                (i, 100 + i, lt, i, _uid(sender), ts, content),
            )
    # 归属不明分表(md5 后缀在 Name2Id 无命中)
    con.execute(f'CREATE TABLE "{UNATTRIBUTED_TABLE}"{_DDL}')
    con.execute(
        f'INSERT INTO "{UNATTRIBUTED_TABLE}" (local_id, server_id, local_type, sort_seq, '
        "real_sender_id, create_time, status, upload_status, download_status, "
        "server_seq, origin_source, source, message_content, compress_content, "
        "packed_info_data, WCDB_CT_message_content, WCDB_CT_source) "
        "VALUES (1, 1, 1, 1, 2, ?, 1, 0, 0, 0, 0, '', '孤儿表行', NULL, NULL, NULL, NULL)",
        (BASE,),
    )
    # 旧形态宽表(isSender)同库混居:回归守卫(方向走 isSender 语义)
    con.execute(
        "CREATE TABLE Msg_legacy_wide (localId INTEGER PRIMARY KEY, serverId INTEGER, "
        "localType INTEGER, createTime INTEGER, sortSeq INTEGER, isSender INTEGER, "
        "strTalker TEXT, content TEXT)"
    )
    con.execute(
        "INSERT INTO Msg_legacy_wide VALUES (1, 301, 1, ?, 1, 0, ?, '旧宽表行')",
        (BASE + 120, GROUP),
    )
    con.commit()
    con.close()
    contact_dir = root / "contact"
    contact_dir.mkdir(parents=True)
    ccon = sqlite3.connect(contact_dir / "contact.db")
    ccon.execute(
        "CREATE TABLE contact (username TEXT PRIMARY KEY, alias TEXT, "
        "nickname TEXT, remark TEXT)"
    )
    for username, remark, nickname in (
        (FRIEND, "好友备注", "好友昵称"),
        (GROUP, None, "合成群名"),
        (ALIAS_FRIEND, None, "别名好友"),
    ):
        ccon.execute(
            "INSERT INTO contact VALUES (?,?,?,?)", (username, None, nickname, remark)
        )
    ccon.commit()
    ccon.close()
    return root


@pytest.fixture(scope="module")
def copies() -> Path:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        yield _build_copies(Path(tmp) / "decrypted")


def _run(copy_dir: Path, mode: str, **kwargs) -> dict:
    return stats_query.run_stats_query(
        copy_dir=copy_dir, mode=mode, now=NOW, **kwargs
    )


# =====================================================================
# Python 全量游标参考实现(与 SQL 路径零共享代码;AC1 互证基准)
# =====================================================================


def _py_reference_rows(copy_dir: Path, chat_id: str | None = None) -> list[dict]:
    """纯 Python 全量游标:直连副本读全行(SQLite 仅当行存储,零聚合)。"""
    con = sqlite3.connect(
        f"file:{copy_dir / 'message' / 'message_0.db'}?mode=ro", uri=True
    )
    id_to_name = {
        int(rid): name
        for rid, name in con.execute('SELECT rowid, "user_name" FROM "Name2Id"')
    }
    md5_to_name = {
        hashlib.md5(name.encode("utf-8")).hexdigest(): name
        for name in id_to_name.values()
    }
    rows: list[dict] = []
    for (table,) in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Msg_%'"
    ):
        if table == "Msg_legacy_wide":
            for lid, sid, lt, ts, seq, is_sender, talker, content in con.execute(
                "SELECT * FROM Msg_legacy_wide"
            ):
                if chat_id and talker != chat_id:
                    continue
                rows.append(
                    {
                        "chat": talker,
                        "ts": int(ts),
                        "local_type": int(lt),
                        "sender": None,
                        "is_me": is_sender == 1,
                        "content": content,
                    }
                )
            continue
        chat = md5_to_name.get(table[4:].lower())
        if chat_id and chat != chat_id:
            continue
        for lt, rid, ts, content in con.execute(
            f'SELECT "local_type", "real_sender_id", "create_time", "message_content" '
            f'FROM "{table}"'
        ):
            sender = id_to_name.get(int(rid or 0)) or chat
            rows.append(
                {
                    "chat": chat,
                    "ts": int(ts),
                    "local_type": int(lt),
                    "sender": sender,
                    "is_me": bool(chat and sender and sender != chat and sender == SELF),
                    "content": content,
                }
            )
    con.close()
    return rows


def _py_buckets(rows: list[dict]) -> dict:
    hourly = [0] * 24
    weekday = [0] * 7
    monthly = [0] * 12
    daily: Counter = Counter()
    for row in rows:
        dt = datetime.fromtimestamp(row["ts"], tz=timezone.utc)
        hourly[dt.hour] += 1
        weekday[dt.weekday()] += 1  # 0=周一
        monthly[dt.month - 1] += 1
        daily[dt.strftime("%Y-%m-%d")] += 1
    return {"hourly": hourly, "weekday": weekday, "monthly": monthly, "daily": daily}


def _py_type_counts(rows: list[dict]) -> dict:
    names = {
        1: "text",
        3: "image",
        34: "voice",
        43: "video",
        47: "sticker",
        48: "location",
        49: "file_or_link",
        10000: "system",
        10002: "revoke",
    }
    counts = Counter()
    for row in rows:
        counts[names.get(row["local_type"], "other")] += 1
    return {key: counts.get(key, 0) for key in TYPE_COUNT_KEYS}


def _py_phrases(rows: list[dict]) -> list[dict]:
    import re

    stop = set("的了是我你吗呢吧哈")
    noise = re.compile(r"wxid_[0-9A-Za-z_-]+|[0-9]+@chatroom|gh_[0-9A-Za-z_-]+|https?://\S+")
    cjk = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]+")
    latin = re.compile(r"[0-9A-Za-z]+")
    counter: Counter = Counter()
    for row in rows:
        if row["local_type"] != 1 or not isinstance(row["content"], str):
            continue
        text = noise.sub(" ", row["content"])
        for run in cjk.findall(text):
            for i in range(len(run) - 1):
                bg = run[i : i + 2]
                if bg[0] in stop and bg[1] in stop:
                    continue
                counter[bg] += 1
        for word in latin.findall(text):
            if len(word) >= 2:
                counter[word.lower()] += 1
    ranked = sorted(
        ((p, c) for p, c in counter.items() if c >= 3), key=lambda kv: (-kv[1], kv[0])
    )[:20]
    return [{"phrase": p, "count": c} for p, c in ranked]


def _py_sessions_response(rows: list[dict]):
    human = [r for r in rows if r["local_type"] not in (10000, 10002)]
    human.sort(key=lambda r: r["ts"])
    total = me_init = other_init = 0
    samples: list[tuple[int, bool]] = []  # (dt, responder_is_me)
    last_ts = last_me = None
    for row in human:
        ts, is_me = row["ts"], row["is_me"]
        if last_ts is None or ts - last_ts > 30 * 60:
            total += 1
            if is_me:
                me_init += 1
            else:
                other_init += 1
        if last_ts is not None and is_me != last_me and 0 <= ts - last_ts <= 24 * 3600:
            samples.append((ts - last_ts, is_me))
        last_ts, last_me = ts, is_me
    return {
        "sessions": {
            "threshold_minutes": 30,
            "total": total,
            "me_initiated": me_init,
            "other_initiated": other_init,
        },
        "samples": samples,
    }


# =====================================================================
# chats / chat
# =====================================================================


class TestChats:
    def test_enumeration_kinds_and_counts(self, copies: Path) -> None:
        payload = _run(copies, "chats")["stats_chats"]
        by_id = {c["chat_id"]: c for c in payload["chats"]}
        assert set(by_id) == {GROUP, FRIEND, OFFICIAL, HELPER, ALIAS_FRIEND}
        assert by_id[GROUP]["kind"] == "group"
        assert by_id[OFFICIAL]["kind"] == "official"
        assert by_id[HELPER]["kind"] == "system"
        assert by_id[FRIEND]["kind"] == "private"
        group_rows = [r for r in CHAT_ROWS if r[0] == GROUP]
        # 群计数 = 分表行 + 旧宽表行(isSender 形态同库并集)
        assert by_id[GROUP]["message_count"] == len(group_rows) + 1
        assert by_id[GROUP]["display_name"] == "合成群名"
        assert by_id[FRIEND]["display_name"] == "好友备注"  # remark > nickname
        assert by_id[GROUP]["first_ts"] == BASE
        assert by_id[GROUP]["last_ts"] == BASE + 86400 * 2
        assert payload["unattributed_tables"] == 1

    def test_ordering_deterministic(self, copies: Path) -> None:
        chats = _run(copies, "chats")["stats_chats"]["chats"]
        keys = [(-c["message_count"], c["chat_id"]) for c in chats]
        assert keys == sorted(keys)


class TestChatMode:
    """AC1 双算互证:SQL 树 vs Python 参考树逐字段相等(群聊)。"""

    def test_group_tree_matches_python_reference(self, copies: Path) -> None:
        sc = _run(copies, "chat", chat_id=GROUP, all_time=True)["stats_chat"]
        rows = _py_reference_rows(copies, GROUP)
        ref_buckets = _py_buckets(rows)
        assert sc["total"] == len(rows)
        assert sc["type_counts"] == _py_type_counts(rows)
        assert sc["hourly"] == ref_buckets["hourly"]
        assert sc["weekday"] == ref_buckets["weekday"]
        assert sc["monthly"] == ref_buckets["monthly"]
        assert sc["daily"] == [
            {"date": d, "count": c} for d, c in sorted(ref_buckets["daily"].items())
        ]
        assert sc["active_days"] == len(ref_buckets["daily"])
        assert sc["human_total"] == len(rows) - 2  # system+revoke 各一
        assert sc["top_phrases"] == _py_phrases(rows)
        sess = _py_sessions_response(rows)
        assert sc["sessions"] == sess["sessions"]
        dts = [dt for dt, _r in sess["samples"]]
        assert sc["response"]["pairs"] == len(dts)
        assert sc["response"]["avg_seconds"] == round(statistics.mean(dts))
        assert sc["response"]["median_seconds"] == round(statistics.median(dts))
        assert sc["response"]["fastest_seconds"] == min(dts)
        # self_id:群聊目标 → 私谈集全局推导
        assert sc["self_id"] == SELF
        assert sc["kind"] == "group"
        assert sc["window"] == {"mode": "all", "from_ts": 0, "to_ts": NOW}

    def test_private_direction_and_streak(self, copies: Path) -> None:
        sc = _run(copies, "chat", chat_id=FRIEND, all_time=True)["stats_chat"]
        rows = _py_reference_rows(copies, FRIEND)
        assert sc["self_id"] == SELF
        me = sum(1 for r in rows if r["is_me"] and r["local_type"] not in (10000, 10002))
        assert sc["sent"] == me
        assert sc["received"] == sc["human_total"] - me
        # streak:d0(11-14)、d1(11-15)、d3(11-17)+ d3 当日续 → 最长 2 天
        assert sc["longest_streak"]["days"] == 2
        assert sc["longest_streak"]["from"] == "2023-11-14"
        # 发言排行:私聊双方;display 用 contact 显示名
        senders = {s["sender_id"]: s for s in sc["senders"]}
        assert senders[SELF]["display"] == SELF  # 无 contact 行回落原样
        assert senders[FRIEND]["display"] == "好友备注"

    def test_window_since_filters_rows(self, copies: Path) -> None:
        # 近 28 天窗 = [BASE+2d, NOW):BASE/BASE+1d 行被滤,BASE+3d 行保留
        sc = _run(copies, "chat", chat_id=FRIEND, since_days=28)["stats_chat"]
        rows = [
            r
            for r in _py_reference_rows(copies, FRIEND)
            if NOW - 28 * 86400 <= r["ts"] < NOW
        ]
        assert sc["window"]["mode"] == "since"
        assert sc["window"]["from_ts"] == NOW - 28 * 86400
        assert sc["total"] == len(rows) == 3
        assert sc["first_ts"] == BASE + 86400 * 3

    def test_window_since_recent_empty(self, copies: Path) -> None:
        """近 10 天窗(夹具最晚行 BASE+3d 仍在窗外)= 空树如实。"""
        sc = _run(copies, "chat", chat_id=FRIEND, since_days=10)["stats_chat"]
        assert sc["total"] == 0
        assert sc["first_ts"] is None
        assert sc["type_counts"]["text"] == 0

    def test_missing_chat_degrades_to_empty_tree(self, copies: Path) -> None:
        sc = _run(copies, "chat", chat_id="wxid_nobody", since_days=7)["stats_chat"]
        assert sc["chat_id"] == "wxid_nobody"
        assert sc["total"] == 0
        assert sc["top_phrases"] == []
        assert sc["response"]["pairs"] == 0

    def test_legacy_wide_table_sender_semantics(self, copies: Path) -> None:
        """旧形态宽表 isSender=0 → other;计数并入群树(并集)。"""
        sc = _run(copies, "chat", chat_id=GROUP, all_time=True)["stats_chat"]
        # 旧宽表行 isSender=0 → received 侧 +1
        rows = _py_reference_rows(copies, GROUP)
        assert sc["received"] == sum(
            1 for r in rows if not r["is_me"] and r["local_type"] not in (10000, 10002)
        )


# =====================================================================
# annual
# =====================================================================


class TestAnnual:
    def test_private_only_and_aggregates(self, copies: Path) -> None:
        sa = _run(copies, "annual", year=2023)["stats_annual"]
        rows = [
            r
            for r in _py_reference_rows(copies, None)
            if r["chat"] in {FRIEND, ALIAS_FRIEND}  # 私谈集:群/官号/系统排除
        ]
        assert sa["year"] == 2023
        assert sa["total"] == len(rows)
        assert sa["type_counts"] == _py_type_counts(rows)
        assert sa["chats_count"] == 2
        assert sa["sent"] + sa["received"] == sa["human_total"]
        top = sa["top_chats"][0]
        assert top["chat_id"] == FRIEND  # 9 行 > ALIAS 2 行
        assert top["display_name"] == "好友备注"
        # years_available:全部归属表 MIN/MAX(含群/官号)
        assert sa["years_available"] == [2023]

    def test_midnight_and_friend_contrast(self, copies: Path) -> None:
        sa = _run(copies, "annual", year=2023)["stats_annual"]
        # BASE=03:00 UTC → 0-5:59 桶;FRIEND 首行 03:00 / ALIAS 05:00+ 均
        # 属深夜;friend_contrast 边界 = 2023-07-01(夹具全在 H2 → late)
        assert sa["midnight"]["count"] > 0
        for row in sa["friend_contrast"]:
            assert row["early_count"] == 0
            assert row["late_count"] > 0

    def test_all_time_mode(self, copies: Path) -> None:
        sa = _run(copies, "annual", all_time=True)["stats_annual"]
        assert sa["year"] == "all"
        rows = [
            r for r in _py_reference_rows(copies, None) if r["chat"] in {FRIEND, ALIAS_FRIEND}
        ]
        assert sa["total"] == len(rows)

    def test_excludes_system_accounts(self, copies: Path) -> None:
        sa = _run(copies, "annual", all_time=True)["stats_annual"]
        ids = {row["chat_id"] for row in sa["friend_contrast"]}
        assert OFFICIAL not in ids and HELPER not in ids and GROUP not in ids


# =====================================================================
# dual
# =====================================================================


class TestDual:
    def test_dual_tree(self, copies: Path) -> None:
        sd = _run(copies, "dual", chat_id=FRIEND, all_time=True)["stats_dual"]
        rows = [
            r
            for r in _py_reference_rows(copies, FRIEND)
            if r["local_type"] not in (10000, 10002)
        ]
        assert sd["me"]["count"] == sum(1 for r in rows if r["is_me"])
        assert sd["other"]["count"] == sum(1 for r in rows if not r["is_me"])
        # 首条 = BASE-40d 的「窗口外应被滤掉」(--all 含全历史;该行仅
        # 对 since 窗才是窗外)
        assert sd["first_chat"]["ts"] == BASE - 40 * 86400
        assert sd["first_chat"]["sender"] == "other"
        assert sd["first_chat"]["text"] == "窗口外应被滤掉"
        # 热度格总和 = 人消息数;7 行 24 列
        assert len(sd["heatmap"]) == 7 and all(len(r) == 24 for r in sd["heatmap"])
        assert sum(sum(r) for r in sd["heatmap"]) == len(rows)
        assert sd["active_days"] == len(
            {datetime.fromtimestamp(r["ts"], tz=timezone.utc).strftime("%Y-%m-%d") for r in rows}
        )
        # 响应:me 侧(我回对方)与 other 侧平均
        sess = _py_sessions_response(
            [r for r in _py_reference_rows(copies, FRIEND)]
        )
        me_resp = [dt for dt, is_me in sess["samples"] if is_me]
        other_resp = [dt for dt, is_me in sess["samples"] if not is_me]
        assert sd["me"]["avg_response_seconds"] == round(statistics.mean(me_resp))
        assert sd["other"]["avg_response_seconds"] == round(statistics.mean(other_resp))
        assert sd["me"]["initiated"] == sess["sessions"]["me_initiated"]
        assert sd["other"]["initiated"] == sess["sessions"]["other_initiated"]

    def test_dual_phrase_columns(self, copies: Path) -> None:
        sd = _run(copies, "dual", chat_id=FRIEND, all_time=True)["stats_dual"]
        mine = {p["phrase"] for p in sd["me"]["top_phrases"]}
        theirs = {p["phrase"] for p in sd["other"]["top_phrases"]}
        assert "okok" in mine and "okok" not in theirs  # 我方独有短语 ≥3 次
        assert "machine" in theirs and "machine" not in mine

    def test_first_chat_non_text_falls_to_type_name(self, tmp_path: Path) -> None:
        """首条消息非文本 → text = 类型名(不臆造内容)。迷你夹具:私聊
        首行 local_type=3(image)。"""
        root = tmp_path / "dec"
        msg = root / "message"
        msg.mkdir(parents=True)
        con = sqlite3.connect(msg / "message_0.db")
        con.execute("CREATE TABLE Name2Id(user_name TEXT PRIMARY KEY, is_session INTEGER)")
        con.executemany(
            "INSERT INTO Name2Id(rowid, user_name, is_session) VALUES (?,?,?)",
            [(1, SELF, 0), (2, "wxid_peer", 0)],
        )
        table = "Msg_" + _md5hex("wxid_peer")
        con.execute(f'CREATE TABLE "{table}"{_DDL}')
        con.execute(
            f'INSERT INTO "{table}" (local_id, server_id, local_type, sort_seq, '
            "real_sender_id, create_time, status, upload_status, download_status, "
            "server_seq, origin_source, source, message_content, compress_content, "
            "packed_info_data, WCDB_CT_message_content, WCDB_CT_source) "
            "VALUES (1,1,3,1,2,?,1,0,0,0,0,'','img-bytes',NULL,NULL,NULL,NULL)",
            (BASE,),
        )
        con.commit()
        con.close()
        sd = _run(root, "dual", chat_id="wxid_peer", all_time=True)["stats_dual"]
        assert sd["first_chat"]["sender"] == "other"
        assert sd["first_chat"]["text"] == "image"  # 非文本 = 类型名

    def test_first_chat_text_truncated_to_120(self, tmp_path: Path) -> None:
        """首条文本超 120 字 → 截断(长文不整段进契约载荷)。"""
        root = tmp_path / "dec"
        msg = root / "message"
        msg.mkdir(parents=True)
        con = sqlite3.connect(msg / "message_0.db")
        con.execute("CREATE TABLE Name2Id(user_name TEXT PRIMARY KEY, is_session INTEGER)")
        con.executemany(
            "INSERT INTO Name2Id(rowid, user_name, is_session) VALUES (?,?,?)",
            [(1, SELF, 0), (2, "wxid_peer2", 0)],
        )
        table = "Msg_" + _md5hex("wxid_peer2")
        con.execute(f'CREATE TABLE "{table}"{_DDL}')
        long_text = "长" * 200
        con.execute(
            f'INSERT INTO "{table}" (local_id, server_id, local_type, sort_seq, '
            "real_sender_id, create_time, status, upload_status, download_status, "
            "server_seq, origin_source, source, message_content, compress_content, "
            "packed_info_data, WCDB_CT_message_content, WCDB_CT_source) "
            "VALUES (1,1,1,1,2,?,1,0,0,0,0,'',?,NULL,NULL,NULL,NULL)",
            (BASE, long_text),
        )
        con.commit()
        con.close()
        sd = _run(root, "dual", chat_id="wxid_peer2", all_time=True)["stats_dual"]
        assert sd["first_chat"]["text"] == "长" * 120


# =====================================================================
# 短语分词单元
# =====================================================================


class TestPhraseTokenize:
    def test_cjk_bigram_and_stopwords(self) -> None:
        counter: Counter = Counter()
        stats_query._count_phrases("我我我", None, counter)  # 单字运行 → 无二元组
        assert not counter
        stats_query._count_phrases("的了的了", None, counter)  # 全停用 → 弃
        assert not counter
        counter2: Counter = Counter()
        stats_query._count_phrases("机器学习", None, counter2)
        assert counter2 == {"机器": 1, "器学": 1, "学习": 1}

    def test_latin_words_and_structural_noise(self) -> None:
        counter: Counter = Counter()
        stats_query._count_phrases(
            "看 https://example.com/a 和 @wxid_abc123 提及", None, counter
        )
        assert "https" not in counter and "wxid" not in counter
        assert "abc123" not in counter
        counter2: Counter = Counter()
        stats_query._count_phrases("GPT gpt Gpt", None, counter2)
        assert counter2 == {"gpt": 3}

    def test_row_cap_hard_limit(self, copies: Path) -> None:
        budget = stats_query._PhraseBudget(cap=3)
        counter: Counter = Counter()
        with stats_query._Plan(copies) as plan:
            for idx, table, colmap in plan.target_entries(FRIEND):
                stats_query._stream_phrases(
                    plan.cons[idx], table, colmap, 0, NOW, counter, budget
                )
        assert budget.capped is True  # FRIEND 表 9 行文本 > 帽 3


# =====================================================================
# self_id 双路互证
# =====================================================================


class TestSelfId:
    def test_mode_derivation(self, copies: Path) -> None:
        with stats_query._Plan(copies) as plan:
            assert (
                stats_query._derive_self_id_from_private_tables(plan) == SELF
            )

    def test_verify_self_id_agreement(self, copies: Path) -> None:
        report = stats_query.verify_self_id(copies)
        assert report["self_id"] == SELF
        assert report["agreement"] is True
        assert report["private_tables_checked"] >= 2
        # 每私聊表:me 行全部归 SELF,other 行 = 收件,空名行如实分立
        friend = next(
            r for r in report["per_chat_shape"] if r["chat_id"] == FRIEND
        )
        assert friend["other_rows"] > 0 and friend["me_rows"] > 0

    def test_tie_yields_none(self, copies: Path) -> None:
        with stats_query._Plan(copies) as plan:
            votes: Counter = Counter()
            votes["a"] = votes["b"] = 5
            assert stats_query._mode_winner(votes) is None


# =====================================================================
# 缓存(AC4/AC5)
# =====================================================================


class TestCache:
    def test_miss_then_hit_and_refresh(self, copies: Path, tmp_path: Path) -> None:
        cache_dir = tmp_path / "stats-cache"
        first = _run(copies, "chat", chat_id=GROUP, all_time=True, cache_dir=cache_dir)
        assert first["stats_chat"]["cache"]["hit"] is False
        files = list(cache_dir.glob("chat-*.json"))
        assert len(files) == 1
        second = _run(copies, "chat", chat_id=GROUP, all_time=True, cache_dir=cache_dir)
        assert second["stats_chat"]["cache"]["hit"] is True
        assert second["stats_chat"]["total"] == first["stats_chat"]["total"]
        refreshed = _run(
            copies, "chat", chat_id=GROUP, all_time=True, cache_dir=cache_dir, refresh=True
        )
        assert refreshed["stats_chat"]["cache"]["hit"] is False

    def test_same_key_recompute_byte_identical(self, copies: Path, tmp_path: Path) -> None:
        cache_dir = tmp_path / "stats-cache"
        _run(copies, "annual", year=2023, cache_dir=cache_dir, refresh=True)
        first = next(cache_dir.glob("annual-*.json")).read_bytes()
        _run(copies, "annual", year=2023, cache_dir=cache_dir, refresh=True)
        second = next(cache_dir.glob("annual-*.json")).read_bytes()
        assert first == second  # AC4:同键重算逐字节一致

    def test_fingerprint_change_invalidates(self, copies: Path, tmp_path: Path) -> None:
        import shutil

        work = tmp_path / "copies"
        shutil.copytree(copies, work)
        db = work / "message" / "message_0.db"
        cache_dir = tmp_path / "stats-cache"
        first = _run(work, "chat", chat_id=GROUP, all_time=True, cache_dir=cache_dir)
        assert first["stats_chat"]["cache"]["hit"] is False
        # 模拟副本重建:mtime 变(内容不动)→ 键变 → 重算
        os.utime(db, (db.stat().st_mtime + 10, db.stat().st_mtime + 10))
        again = _run(work, "chat", chat_id=GROUP, all_time=True, cache_dir=cache_dir)
        assert again["stats_chat"]["cache"]["hit"] is False
        assert len(list(cache_dir.glob("chat-*.json"))) == 2

    def test_cache_key_includes_contract_revision(self, copies: Path) -> None:
        key1 = stats_query._cache_key(
            "chat", {"chat_id": "x"}, "1:2"
        )
        key2 = stats_query._cache_key(
            "chat", {"chat_id": "x", "extra": 1}, "1:2"
        )
        assert key1 != key2  # 参数不同键不同

    def test_corrupt_cache_falls_back_to_recompute(
        self, copies: Path, tmp_path: Path
    ) -> None:
        cache_dir = tmp_path / "stats-cache"
        cache_dir.mkdir()
        key = stats_query._cache_key(
            "chat", {"chat_id": GROUP, "since_days": None, "year": None, "all_time": True},
            stats_query._copy_fingerprint(copies),
        )
        (cache_dir / f"{key}.json").write_text("{bad json", encoding="utf-8")
        result = _run(copies, "chat", chat_id=GROUP, all_time=True, cache_dir=cache_dir)
        assert result["stats_chat"]["cache"]["hit"] is False
        assert result["stats_chat"]["total"] > 0


# =====================================================================
# 红线(AC7)
# =====================================================================


class TestRedlines:
    def test_no_network_imports(self) -> None:
        source = Path(stats_query.__file__).read_text(encoding="utf-8")
        for banned in ("httpx", "requests", "urllib.request", "socket", "subprocess"):
            assert banned not in source, f"stats_query 禁 {banned}"

    def test_connections_are_readonly(self, copies: Path) -> None:
        with stats_query._Plan(copies) as plan:
            assert plan.cons
            for con in plan.cons:
                # mode=ro URI 连接:任何写语句必败(真验,非形状推断)
                with pytest.raises(sqlite3.OperationalError):
                    con.execute("CREATE TABLE _probe(x)")

    def test_empty_copy_dir_degrades(self, tmp_path: Path) -> None:
        empty = tmp_path / "empty"
        empty.mkdir()
        payload = _run(empty, "chats")
        assert payload["stats_chats"]["chats"] == []
        assert payload["stats_chats"]["unattributed_tables"] == 0
