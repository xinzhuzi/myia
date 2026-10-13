"""E3 联系人工作台只读查询单测(task 10-14-wechat-contacts R6;合成明文副本,零真实内容)。

夹具形状照 2026-10-14 直查本机解密副本实测 DDL(contact 全列含
local_type/quan_pin/flag/description;stranger 同列集;Name2Id(user_name);
contact_label(label_id_/label_name_);room_verify_application 八列)。内容全
合成。

覆盖面(prd AC1/AC2/AC3 的合成夹具形态):
- 判定闭包:六桶加和 == COUNT(*),每桶逐行对拍手写 SQL;
- 游标零重漏:keyset 翻页拼接无重复无遗漏,行数 == 桶 count;
- keyword 五列 LIKE 对拍手写 SQL(含通配符字面量化);
- Tier 对拍:Tier A == former 候选 ∩ Name2Id.user_name(独立集算);
- limit 三态:0 = 全量(防「limit 0=空」bug,设计拷问修正①)、帽 1000、
  负值 usage 拒;
- 缺表/缺列降级空结构恒不判错(判例 group-info);
- invalid_cursor 族:串筛选/坏 base64/坏形状;
- CLI 接线(集成批落位后自激活:localdb.contacts_inventory 在场才跑,
  判例 key_unavailable exit 21 + usage 拒)。

golden 基件零新增锚(缺钥错误形态与 query/sns/group-info 全族同形,判例
同 test_sns_query);契约全字段形状对账由本文件合成副本用例承担(逐键
封闭断言,零自造键)。
"""

from __future__ import annotations

import base64
import json
import sqlite3
from pathlib import Path

import pytest

from bridge_testkit import run_cli
from wechat_bridge.contacts_query import (
    LIMIT_DEFAULT,
    SYSTEM_USERNAMES,
    TYPE_FILTERS,
    contacts_page,
    decode_cursor,
    encode_cursor,
    normalize_cli_limit,
)
from wechat_bridge.codes import BridgeError

GROUP_A = "91000000001@chatroom"
GROUP_B = "91000000002@chatroom"


def _build_contact_db(path: Path, *, room_verify_rows: int = 0) -> None:
    """合成 contact 库(全合成内容;列集照真库 DDL 的判定相关子集)。

    六桶布点:system 2 / group 2 / official 3(lt1+lt0+lt3 全占——gh_ 桶
    不叠 lt 条件的分歧判例)/ former 4(2 个带身份字段)/ friend 3 /
    other 3(lt0 裸行 + lt3 无昵称 + lt5)。
    """
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE contact (id INTEGER PRIMARY KEY, username TEXT, "
        "local_type INTEGER, alias TEXT, encrypt_username TEXT, flag INTEGER, "
        "delete_flag INTEGER, verify_flag INTEGER, remark TEXT, "
        "remark_quan_pin TEXT, nick_name TEXT, pin_yin_initial TEXT, "
        "quan_pin TEXT, description TEXT, extra_buffer BLOB)"
    )
    rows: list[tuple[str, int, str, str, str, str, str, int]] = [
        # username, local_type, alias, remark, nick_name, quan_pin, description, flag
        ("weixin", 1, "", "", "微信团队", "", "", 0),          # system(①)
        ("fmessage", 1, "", "", "朋友圈消息", "", "", 0),      # system(①)
        (GROUP_A, 2, "", "", "合成群A", "", "", 0),            # group(②)
        (GROUP_B, 2, "", "", "合成群B", "", "群说明", 0),      # group(②)
        ("gh_abc123", 1, "", "", "公众号甲", "", "", 0),       # official(③)
        ("gh_def456", 0, "", "", "公众号乙", "gzh", "", 0),    # official(③,lt0 也在 gh_)
        ("gh_ghi789", 3, "", "", "公众号丙", "", "", 0),       # official(③,lt3 也在 gh_)
        ("wxid_former_a", 3, "", "", "旧友A", "", "", 0),      # former(④)
        ("wxid_former_b", 3, "alias_b", "", "旧友B", "", "曾备注", 0),  # former+identity
        ("wxid_former_c", 3, "", "remark_c", "旧友C", "quan_c", "", 0),  # former+identity
        ("wxid_former_d", 3, "", "", "旧友D", "", "", 4),      # former(flag=4)
        ("wxid_friend_a", 1, "", "", "好友A", "", "", 0),      # friend(⑤)
        ("wxid_friend_b", 1, "alias_fb", "备注FB", "好友B", "", "", 0),  # friend
        ("wxid_friend_c", 1, "", "", "好友C", "", "好友描述", 0),  # friend
        ("wxid_other_lt0", 0, "", "", "", "", "", 0),          # other(lt0 裸行)
        ("wxid_other_lt3nonick", 3, "", "", "", "", "", 0),    # other(lt3 无昵称)
        ("wxid_other_lt5", 5, "", "", "openim账号", "", "", 0),  # other(lt5)
    ]
    con.executemany(
        "INSERT INTO contact (username, local_type, alias, remark, nick_name, "
        "quan_pin, description, flag) VALUES (?,?,?,?,?,?,?,?)",
        rows,
    )
    con.execute(
        "CREATE TABLE chat_room (id INTEGER PRIMARY KEY, username TEXT, "
        "owner TEXT, ext_buffer BLOB)"
    )
    con.execute(
        "CREATE TABLE chatroom_member (room_id INTEGER, member_id INTEGER)"
    )
    con.execute("INSERT INTO chat_room VALUES (101, ?, 'wxid_friend_a', x'')", (GROUP_A,))
    con.execute("INSERT INTO chat_room VALUES (102, ?, NULL, x'')", (GROUP_B,))
    con.executemany(
        "INSERT INTO chatroom_member VALUES (?,?)",
        [(101, 1), (101, 2), (101, 3), (102, 4)],  # 群A 3 成员;群B 1 成员
    )
    con.execute(
        "CREATE TABLE stranger (id INTEGER PRIMARY KEY, username TEXT, "
        "local_type INTEGER, alias TEXT, nick_name TEXT, remark TEXT, "
        "quan_pin TEXT, description TEXT)"
    )
    con.executemany(
        "INSERT INTO stranger (username, local_type, alias, nick_name, remark) "
        "VALUES (?,?,?,?,?)",
        [
            ("v3_stranger_1@stranger", 4, "", "陌生人甲", ""),
            ("v3_stranger_2@stranger", 4, "alias_s2", "陌生人乙", ""),
            ("v3_stranger_3@stranger", 4, "", "陌生人丙", "备注丙"),
        ],
    )
    con.execute(
        "CREATE TABLE contact_label (label_id_ INTEGER PRIMARY KEY, "
        "label_name_ TEXT, sort_order_ INTEGER)"
    )
    con.executemany(
        "INSERT INTO contact_label VALUES (?,?,?)",
        [(4, "同事", 0), (5, "家人", 1)],
    )
    con.execute(
        "CREATE TABLE room_verify_application (msg_server_id INTEGER, "
        "chatroom_name TEXT, hash_key TEXT, inviter_username TEXT, state INTEGER, "
        "read_status INTEGER, data_json TEXT, update_time INTEGER)"
    )
    for i in range(room_verify_rows):
        con.execute(
            "INSERT INTO room_verify_application VALUES (?,?,?,?,?,?,?,?)",
            (1000 + i, GROUP_A, f"hash_{i}", "wxid_inviter", 0, 0,
             '{"opaque": true}', 1780000000 + i),
        )
    con.commit()
    con.close()


def _build_message_db(path: Path) -> None:
    """合成 message 库(只建 Name2Id;Msg_ 表已删即真库形态)。

    残留集布点:former_a/former_b/former_d 在 Name2Id(Tier A);former_c
    不在(Tier B);好友与非联系人各占位防误沾。
    """
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE Name2Id (user_name TEXT PRIMARY KEY, is_session INTEGER)")
    con.executemany(
        "INSERT INTO Name2Id VALUES (?,?)",
        [
            ("wxid_former_a", 0),
            ("wxid_former_b", 0),
            ("wxid_former_d", 1),
            ("wxid_friend_a", 1),
            ("wxid_not_in_contact", 0),
            (GROUP_A, 1),
        ],
    )
    con.commit()
    con.close()


@pytest.fixture()
def copies(tmp_path: Path) -> Path:
    copy_root = tmp_path / "decrypted"
    (copy_root / "contact").mkdir(parents=True)
    (copy_root / "message").mkdir(parents=True)
    _build_contact_db(copy_root / "contact" / "contact.db")
    _build_message_db(copy_root / "message" / "message_0.db")
    return copy_root


@pytest.fixture()
def contact_only(tmp_path: Path) -> Path:
    """单 contact 域副本(无 message 目录——域收缩纪律的查询面)。"""
    copy_root = tmp_path / "decrypted"
    (copy_root / "contact").mkdir(parents=True)
    _build_contact_db(copy_root / "contact" / "contact.db")
    return copy_root


def _run(copy_dir: Path, **kwargs) -> dict:
    return contacts_page(copy_dir, **kwargs)["contacts"]


# ---------------------------------------------------------------------------
# 契约形状 + 判定闭包(AC1 合成形态)
# ---------------------------------------------------------------------------


class TestContractAndBuckets:
    def test_contract_keys_closed(self, copies: Path) -> None:
        payload = _run(copies)
        assert list(payload) == [
            "counts",
            "former_tiers",
            "residue_checked",
            "strict_residual_count",
            "labels",
            "stranger",
            "room_verify",
            "rows",
            "next_cursor",
            "has_more",
            "filter",
            "page_size",
            "degraded",
        ]
        assert list(payload["counts"]) == [
            "friend", "group", "official", "former", "other", "system",
        ]

    def test_bucket_closure_matches_count(self, copies: Path) -> None:
        payload = _run(copies)
        assert sum(payload["counts"].values()) == 17  # == COUNT(*)
        assert payload["counts"] == {
            "friend": 3,
            "group": 2,
            "official": 3,
            "former": 4,
            "other": 3,
            "system": 2,
        }

    def test_bucket_order_gh_beats_local_type(self, copies: Path) -> None:
        """判定序:gh_ 前缀先于 lt 条件(③在④⑤前)——lt0/lt3 的 gh_ 行
        全归 official(与 WeFlow gh_+lt1 组合有意分歧,分歧原因=真库实测)。"""
        rows = _run(copies, type_filter="official")["rows"]
        assert {row["username"] for row in rows} == {
            "gh_abc123", "gh_def456", "gh_ghi789",
        }
        assert all(row["type"] == "official" for row in rows)

    def test_system_never_in_rows_but_counted(self, copies: Path) -> None:
        payload = _run(copies)
        assert payload["counts"]["system"] == 2
        assert all(row["type"] != "system" for row in payload["rows"])
        usernames = {row["username"] for row in payload["rows"]}
        assert "weixin" not in usernames and "fmessage" not in usernames

    def test_row_shape_and_display_chain(self, copies: Path) -> None:
        rows = {row["username"]: row for row in _run(copies, limit=0)["rows"]}
        assert list(rows["wxid_friend_b"].keys()) == [
            "username", "display_name", "remark", "nickname", "alias",
            "type", "local_type", "evidence", "description",
        ]
        assert rows["wxid_friend_b"]["display_name"] == "备注FB"  # remark 优先
        assert rows["wxid_friend_b"]["remark"] == "备注FB"
        assert rows["wxid_friend_b"]["alias"] == "alias_fb"
        assert rows["wxid_friend_b"]["local_type"] == 1
        assert rows["wxid_friend_c"]["display_name"] == "好友C"  # 无备注→nickname
        assert rows["wxid_other_lt0"]["display_name"] == "wxid_other_lt0"  # 裸行回落 username
        assert rows["wxid_friend_c"]["description"] == "好友描述"
        assert rows["wxid_other_lt0"]["description"] is None

    def test_group_rows_carry_member_count(self, copies: Path) -> None:
        rows = {row["username"]: row for row in _run(copies, type_filter="group")["rows"]}
        assert rows[GROUP_A]["member_count"] == 3
        assert rows[GROUP_B]["member_count"] == 1
        friend_rows = _run(copies, type_filter="friend")["rows"]
        assert all("member_count" not in row for row in friend_rows)


# ---------------------------------------------------------------------------
# 分页与过滤(AC2 合成形态)
# ---------------------------------------------------------------------------


class TestPagingAndFilter:
    def test_cursor_paging_zero_dup_zero_miss(self, copies: Path) -> None:
        """全库 keyset 翻页(页大小 2):拼接 rowid/username 集无重复无遗漏,
        行数 == 可见五桶加和(system 不出行)。"""
        seen: list[str] = []
        cursor: str | None = None
        pages = 0
        while True:
            payload = _run(copies, limit=2, cursor=cursor)
            seen.extend(row["username"] for row in payload["rows"])
            pages += 1
            assert payload["page_size"] == 2
            if not payload["has_more"]:
                assert payload["next_cursor"] is None
                break
            assert payload["next_cursor"]
            cursor = payload["next_cursor"]
            assert pages < 50, "翻页不终止"
        assert len(seen) == len(set(seen)) == 15  # 17 - system 2
        visible = sum(_run(copies)["counts"][b] for b in TYPE_FILTERS)
        assert len(seen) == visible

    def test_bucket_paging_matches_count(self, copies: Path) -> None:
        for bucket in TYPE_FILTERS:
            seen: list[str] = []
            cursor: str | None = None
            while True:
                payload = _run(copies, type_filter=bucket, limit=1, cursor=cursor)
                seen.extend(row["username"] for row in payload["rows"])
                assert all(row["type"] == bucket for row in payload["rows"])
                cursor = payload["next_cursor"]
                if not payload["has_more"]:
                    break
            assert len(seen) == _run(copies)["counts"][bucket], bucket

    def test_limit_zero_is_full_not_empty(self, copies: Path) -> None:
        """设计拷问修正①:limit 0 = 全量导出态(帽豁免),不是空页。"""
        payload = _run(copies, limit=0)
        assert len(payload["rows"]) == 15
        assert payload["has_more"] is False
        assert payload["next_cursor"] is None
        assert payload["page_size"] == 0

    def test_normalize_cli_limit_three_states(self) -> None:
        assert normalize_cli_limit(None) == LIMIT_DEFAULT == 100
        assert normalize_cli_limit(0) == 0  # 全量导出态
        assert normalize_cli_limit(1000) == 1000
        assert normalize_cli_limit(99999) == 1000  # 帽
        with pytest.raises(BridgeError) as excinfo:
            normalize_cli_limit(-1)
        assert excinfo.value.exit_code == 2

    def test_keyword_matches_handwritten_sql(self, copies: Path) -> None:
        """keyword 五列 LIKE 对拍手写 SQL(含通配符字面量化:% 不当通配符)。"""
        con = sqlite3.connect(f"file:{copies}/contact/contact.db?mode=ro", uri=True)
        expected = {
            row[0]
            for row in con.execute(
                "SELECT username FROM contact WHERE remark LIKE ? OR nick_name LIKE ? "
                "OR alias LIKE ? OR username LIKE ? OR quan_pin LIKE ? ESCAPE '\\'",
                ["%友%"] * 5,
            )
        }
        con.close()
        expected -= set(SYSTEM_USERNAMES)  # system 恒不出行(①只进 counts)
        rows = _run(copies, keyword="友", limit=0)["rows"]
        assert {row["username"] for row in rows} == expected

    def test_keyword_wildcard_literalized(self, copies: Path) -> None:
        """搜「%」不命中全表(通配符字面量化;合成库无字面 % 行 → 零命中)。"""
        payload = _run(copies, keyword="%")
        assert payload["rows"] == []

    def test_invalid_type_is_usage(self, copies: Path) -> None:
        with pytest.raises(BridgeError) as excinfo:
            contacts_page(copies, type_filter="bogus")
        assert excinfo.value.exit_code == 2
        assert excinfo.value.code == "usage"

    def test_invalid_cursor_family(self, copies: Path) -> None:
        # 坏 base64
        with pytest.raises(BridgeError) as excinfo:
            contacts_page(copies, cursor="!!!not-base64!!!")
        assert excinfo.value.code == "invalid_cursor"
        assert excinfo.value.exit_code == 2
        # 坏 JSON(base64 合法)
        garbage = base64.b64encode(b"not json").decode("ascii")
        with pytest.raises(BridgeError) as excinfo:
            contacts_page(copies, cursor=garbage)
        assert excinfo.value.code == "invalid_cursor"
        # 形状漂移(缺 filter)
        malformed = base64.b64encode(
            json.dumps({"v": 1, "rowid": 3}).encode()
        ).decode("ascii")
        with pytest.raises(BridgeError) as excinfo:
            contacts_page(copies, cursor=malformed)
        assert excinfo.value.code == "invalid_cursor"
        # 版本不识
        bad_version = base64.b64encode(
            json.dumps({"v": 99, "rowid": 3, "filter": {"type": None, "keyword": None}}).encode()
        ).decode("ascii")
        with pytest.raises(BridgeError) as excinfo:
            contacts_page(copies, cursor=bad_version)
        assert excinfo.value.code == "invalid_cursor"

    def test_cursor_scope_guard_rejects_filter_mismatch(self, copies: Path) -> None:
        """scope 守卫:游标内 filter 与请求不一致 → invalid_cursor(串
        筛选/串 keyword 复用旧游标都拒)。"""
        # 无过滤首页拿游标
        first = _run(copies, limit=2)
        assert first["next_cursor"]
        with pytest.raises(BridgeError) as excinfo:
            _run(copies, type_filter="friend", cursor=first["next_cursor"])
        assert excinfo.value.code == "invalid_cursor"
        with pytest.raises(BridgeError):
            _run(copies, keyword="友", cursor=first["next_cursor"])
        # 同 filter 续拉合法
        friend_first = _run(copies, type_filter="friend", limit=2)
        second = _run(copies, type_filter="friend", limit=2, cursor=friend_first["next_cursor"])
        assert second["rows"]
        assert {r["username"] for r in friend_first["rows"]}.isdisjoint(
            {r["username"] for r in second["rows"]}
        )

    def test_cursor_roundtrip_shape(self) -> None:
        cursor = encode_cursor(42, "former", "张")
        assert decode_cursor(cursor, "former", "张") == 42
        # keyword 归一(空白 = None)两侧一致
        cursor = encode_cursor(7, None, "  ")
        assert decode_cursor(cursor, None, "") == 7


# ---------------------------------------------------------------------------
# 考古分层(AC3 合成形态)
# ---------------------------------------------------------------------------


class TestResidue:
    def test_no_residue_contact_domain_only(self, contact_only: Path) -> None:
        """无 --with-residue:former_tiers null / residue_checked False;
        identity_fields 仍出(contact 域本地事实,与 message 域无关)。"""
        assert not (contact_only / "message").exists()
        payload = _run(contact_only, type_filter="former", limit=0)
        assert payload["former_tiers"] is None
        assert payload["residue_checked"] is False
        by_name = {row["username"]: row for row in payload["rows"]}
        assert by_name["wxid_former_b"]["evidence"] == ["identity_fields"]
        assert by_name["wxid_former_c"]["evidence"] == ["identity_fields"]
        assert by_name["wxid_former_a"]["evidence"] == []

    def test_with_residue_tiers_and_evidence(self, copies: Path) -> None:
        """Tier 对拍:Tier A == former 候选 ∩ Name2Id.user_name(独立集算);
        逐行 evidence:msg_residue 在前、identity_fields 在后。"""
        payload = _run(copies, with_residue=True, type_filter="former", limit=0)
        assert payload["residue_checked"] is True
        con = sqlite3.connect(f"file:{copies}/message/message_0.db?mode=ro", uri=True)
        name2id = {row[0] for row in con.execute("SELECT user_name FROM Name2Id")}
        con.close()
        expected_a = len(name2id & {"wxid_former_a", "wxid_former_b", "wxid_former_c", "wxid_former_d"})
        assert payload["former_tiers"] == {
            "msg_residue": expected_a,       # former_a/b/d
            "table_only": 4 - expected_a,    # former_c
        }
        assert expected_a == 3
        by_name = {row["username"]: row for row in payload["rows"]}
        assert by_name["wxid_former_a"]["evidence"] == ["msg_residue"]
        assert by_name["wxid_former_b"]["evidence"] == ["msg_residue", "identity_fields"]
        assert by_name["wxid_former_c"]["evidence"] == ["identity_fields"]  # Tier B + 身份字段
        assert by_name["wxid_former_d"]["evidence"] == ["msg_residue"]

    def test_with_residue_message_missing_degrades(self, contact_only: Path) -> None:
        """--with-residue 但 message 副本缺:residue_checked False、tiers
        null、degraded 标注,恒不判错。"""
        payload = _run(contact_only, with_residue=True)
        assert payload["residue_checked"] is False
        assert payload["former_tiers"] is None
        assert "missing_copy:message" in payload["degraded"]

    def test_stranger_shape_and_not_in_former_counts(self, copies: Path) -> None:
        payload = _run(copies)
        assert len(payload["stranger"]) == 3
        first = payload["stranger"][0]
        assert set(first) == {"username", "display_name", "local_type", "remark"}
        assert first["username"] == "v3_stranger_1@stranger"
        assert first["local_type"] == 4
        # stranger 不混入 former 计数(独立子卡语义)
        assert payload["counts"]["former"] == 4

    def test_include_stranger_off(self, copies: Path) -> None:
        assert _run(copies, include_stranger=False)["stranger"] == []

    def test_room_verify_empty_and_present(self, tmp_path: Path) -> None:
        copy_root = tmp_path / "decrypted2"
        (copy_root / "contact").mkdir(parents=True)
        _build_contact_db(copy_root / "contact" / "contact.db", room_verify_rows=2)
        payload = _run(copy_root)
        assert payload["room_verify"] == {
            "present": True,
            "rows": 2,
            "sample": [
                {
                    "chatroom_name": GROUP_A,
                    "inviter_username": "wxid_inviter",
                    "state": 0,
                    "update_time": 1780000000,
                },
                {
                    "chatroom_name": GROUP_A,
                    "inviter_username": "wxid_inviter",
                    "state": 0,
                    "update_time": 1780000001,
                },
            ],
        }

    def test_strict_residual_count_handwritten(self, copies: Path) -> None:
        """严判据对照:人集作用域(lt0+quan_pin 的 gh_def456 被排除);
        lt3+flag≠4+身份 → former_b/c(flag=0)命中,former_d flag=4 被排除。"""
        payload = _run(copies)
        # 合成库手算:lt0 臂(gh_def456 有 quan_pin 但 gh_ 排除)= 0;
        # lt3 臂 = former_b(alias+remark)+ former_c(remark+quan_pin) = 2
        assert payload["strict_residual_count"] == 2

    def test_labels_listed_without_contact_join(self, copies: Path) -> None:
        assert _run(copies)["labels"] == [
            {"id": 4, "name": "同事"},
            {"id": 5, "name": "家人"},
        ]


# ---------------------------------------------------------------------------
# 降级(AC3 尾款:缺表/缺列降级空结构恒 exit 0 形态)
# ---------------------------------------------------------------------------


class TestDegrade:
    def test_contact_copy_missing_all_empty(self, tmp_path: Path) -> None:
        payload = _run(tmp_path / "no_such_copy")
        assert payload["counts"] == {
            "friend": 0, "group": 0, "official": 0, "former": 0, "other": 0, "system": 0,
        }
        assert payload["rows"] == []
        assert payload["former_tiers"] is None
        assert payload["residue_checked"] is False
        assert payload["labels"] == []
        assert payload["stranger"] == []
        assert payload["room_verify"] == {"present": False, "rows": 0}
        assert payload["has_more"] is False

    def test_local_type_column_missing_buckets_null(self, copies: Path) -> None:
        """local_type 列缺:④⑤臂不可判 → 未落入 ①②③ 的行不入桶不进
        counts(不倒进 other 冒充);①②③ 照常;degraded 标注。"""
        con = sqlite3.connect(copies / "contact" / "contact.db")
        con.execute("CREATE TABLE contact_2 AS SELECT * FROM contact")
        con.execute("DROP TABLE contact")
        con.execute("ALTER TABLE contact_2 RENAME TO contact")
        con.commit()
        con.close()
        # 重建缺列形态:直接建新表搬列(去掉 local_type)
        con = sqlite3.connect(copies / "contact" / "contact.db")
        rows = con.execute(
            "SELECT id, username, alias, remark, nick_name, quan_pin, description, flag "
            "FROM contact"
        ).fetchall()
        con.execute("DROP TABLE contact")
        con.execute(
            "CREATE TABLE contact (id INTEGER PRIMARY KEY, username TEXT, alias TEXT, "
            "remark TEXT, nick_name TEXT, quan_pin TEXT, description TEXT, flag INTEGER)"
        )
        con.executemany("INSERT INTO contact VALUES (?,?,?,?,?,?,?,?)", rows)
        con.commit()
        con.close()
        payload = _run(copies)
        assert payload["counts"]["group"] == 2  # ②不依赖 local_type
        assert payload["counts"]["official"] == 3  # ③同
        assert payload["counts"]["system"] == 2  # ①同
        assert payload["counts"]["former"] == 0
        assert payload["counts"]["friend"] == 0
        assert payload["counts"]["other"] == 0
        assert any("local_type" in note for note in payload["degraded"])
        rows = {row["username"] for row in payload["rows"]}
        assert "wxid_friend_a" not in rows  # 不可判行不出行
        assert GROUP_A in rows  # ②照常出行

    def test_side_tables_missing_degrade_with_notes(self, copies: Path) -> None:
        con = sqlite3.connect(copies / "contact" / "contact.db")
        for table in ("stranger", "room_verify_application", "contact_label",
                      "chat_room", "chatroom_member"):
            con.execute(f"DROP TABLE {table}")
        con.commit()
        con.close()
        payload = _run(copies)
        assert payload["stranger"] == []
        assert payload["room_verify"] == {"present": False, "rows": 0}
        assert payload["labels"] == []
        assert any("stranger" in note for note in payload["degraded"])
        assert any("room_verify_application" in note for note in payload["degraded"])
        assert any("contact_label" in note for note in payload["degraded"])
        # 群行 member_count 缺表降级 0
        group_rows = [r for r in payload["rows"] if r["type"] == "group"]
        assert all(r["member_count"] == 0 for r in group_rows)

    def test_quan_pin_missing_keyword_drops_column(self, copies: Path) -> None:
        con = sqlite3.connect(copies / "contact" / "contact.db")
        con.execute(
            "CREATE TABLE contact_nq AS SELECT id, username, local_type, alias, "
            "flag, remark, nick_name, description FROM contact"
        )
        con.execute("DROP TABLE contact")
        con.execute("ALTER TABLE contact_nq RENAME TO contact")
        con.commit()
        con.close()
        payload = _run(copies, keyword="quan_c")
        assert payload["rows"] == []  # quan_pin 列缺 → 该列不参与 LIKE
        assert "missing_column:quan_pin" in payload["degraded"]
        # 其余四列照常命中
        assert _run(copies, keyword="好友A")["rows"]


# ---------------------------------------------------------------------------
# CLI 接线(集成批落位后自激活)
# ---------------------------------------------------------------------------


def _cli_wired() -> bool:
    """cli.py ``localdb contacts`` 分支 + localdb.contacts_inventory 是否已
    落位(集成批;判据 = 编排函数在场——integrationSpec 把两者钉在同一批)。"""
    from wechat_bridge import localdb

    return hasattr(localdb, "contacts_inventory")


class TestCli:
    """CLI 面(判例 test_group_info.TestCli:⑤ 形态密钥缺位 → exit 21 +
    usage 拒;成功链与 invalid_cursor 由查询层用例覆盖)。"""

    def _fake_root(self, monkeypatch, tmp_path: Path) -> Path:
        fake_root = tmp_path / "xwechat_files"
        account = fake_root / "wxid_demo_8253"
        (account / "db_storage" / "contact").mkdir(parents=True)
        monkeypatch.setattr("wechat_bridge.localdb.WECHAT_FILES_ROOT", fake_root)
        return fake_root

    def test_key_unavailable(self, monkeypatch, tmp_path: Path) -> None:
        if not _cli_wired():
            pytest.skip("cli.py localdb contacts 未接线(集成批落位后自激活)")
        self._fake_root(monkeypatch, tmp_path)
        exit_code, payload = run_cli(
            ["localdb", "contacts", "--json"], monkeypatch, tmp_path
        )
        assert exit_code == 21
        assert payload["error"]["code"] == "key_unavailable"

    def test_bad_type_is_usage(self, monkeypatch, tmp_path: Path) -> None:
        if not _cli_wired():
            pytest.skip("cli.py localdb contacts 未接线(集成批落位后自激活)")
        self._fake_root(monkeypatch, tmp_path)
        exit_code, payload = run_cli(
            ["localdb", "contacts", "--type", "bogus", "--json"],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"

    def test_negative_limit_is_usage_with_full_export_hint(
        self, monkeypatch, tmp_path: Path
    ) -> None:
        """设计拷问修正①:0=全量的特例语义在 usage 文案里钉死(负值拒,
        错误消息携带「0 = 全量导出态」防误用)。"""
        if not _cli_wired():
            pytest.skip("cli.py localdb contacts 未接线(集成批落位后自激活)")
        self._fake_root(monkeypatch, tmp_path)
        exit_code, payload = run_cli(
            ["localdb", "contacts", "--limit", "-1", "--json"],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"
        assert "全量" in payload["error"]["message"]
