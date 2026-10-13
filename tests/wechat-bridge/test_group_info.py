"""E3 群信息只读查询单测(task 10-13-wechat-groupinfo;合成明文副本,零真实内容)。

夹具形状照 2026-10-13 直查本机解密副本实测 DDL(``chat_room(id,username,
owner,ext_buffer)`` / ``chat_room_info_detail(room_id_,username_,
announcement_,announcement_editor_,announcement_publish_time_,
chat_room_status_,…)`` / ``chatroom_member(room_id,member_id)``)。内容全
合成。CLI 面照 ``test_bridge_cli.py`` 的 ⑤ 形态(密钥缺位 → exit 21)。

**member_id = contact 表 rowid**(2026-10-13 实拍裁决:500 人群按
contact.rowid 解释 500/500 可解且全部命中 ext_buffer 名单锚、按 Name2Id
解释仅 16/500 命中=巧合错配;裁决注记见
``localdb_query._contact_rowid_usernames``)——夹具成员用显式 rowid 的
contact 行,查询**单 contact 域自足**(零 message 域)。

golden 基件零新增锚(缺钥错误形态与 sns/query 全族同形,加锚零增量信息,
判例同 test_sns_query);契约 v1 全字段的形状对账由本文件合成副本用例
承担(逐键封闭断言,零自造键)。
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

from bridge_testkit import run_cli
from wechat_bridge.localdb_query import group_info

GROUP_A = "90000000001@chatroom"
GROUP_B = "90000000002@chatroom"
PUB_TS = 1785581178  # 秒级(2026-08 实锚量级)


@pytest.fixture()
def group_copies(tmp_path: Path) -> Path:
    """合成解密副本(**仅 contact 域**;全合成内容,零真实语料)。

    群 A:群主 wxid_owner + 3 个可反查成员 + 1 个 contact 缺行成员
    (member_id=555,弃行但 member_count 记真值 4)+ 有公告(编辑人=群主)。
    群 B:chat_room 行在(owner NULL)+ 无 info_detail 行 + 无成员。
    成员经 contact.rowid 显式钉死(7/8/9)。
    """
    copy_root = tmp_path / "decrypted"
    contact = copy_root / "contact" / "contact.db"
    contact.parent.mkdir(parents=True)
    con = sqlite3.connect(contact)
    con.execute(
        "CREATE TABLE contact (username TEXT PRIMARY KEY, alias TEXT, "
        "nickname TEXT, remark TEXT, localType INTEGER)"
    )
    con.executemany(
        "INSERT INTO contact (rowid, username, alias, nickname, remark, "
        "localType) VALUES (?,?,?,?,?,1)",
        [
            (7, "wxid_a", "", "昵称A", "备注A"),
            (8, "wxid_b", "", "昵称B", ""),
            (9, "wxid_owner", "", "群主昵称", "群主备注"),
            # wxid_c 无 contact 行:display 回落 wxid 原样,remark None
            (None, GROUP_A, "", "合成群A", ""),
        ],
    )
    con.execute(
        "CREATE TABLE chat_room (id INTEGER PRIMARY KEY, username TEXT, "
        "owner TEXT, ext_buffer BLOB)"
    )
    con.executemany(
        "INSERT INTO chat_room VALUES (?,?,?,?)",
        [(101, GROUP_A, "wxid_owner", b""), (102, GROUP_B, None, b"")],
    )
    con.execute(
        "CREATE TABLE chat_room_info_detail (room_id_ INTEGER, username_ TEXT, "
        "announcement_ TEXT, announcement_editor_ TEXT, "
        "announcement_publish_time_ INTEGER, chat_room_status_ INTEGER, "
        "xml_announcement_ TEXT, ext_buffer_ BLOB)"
    )
    con.execute(
        "INSERT INTO chat_room_info_detail VALUES (?,?,?,?,?,?,?,?)",
        (101, GROUP_A, "请勿发广告", "wxid_owner", PUB_TS, 524288, "", b""),
    )
    con.execute(
        "CREATE TABLE chatroom_member (room_id INTEGER, member_id INTEGER)"
    )
    con.executemany(
        "INSERT INTO chatroom_member VALUES (?,?)",
        [(101, 9), (101, 7), (101, 8), (101, 555)],
    )
    con.commit()
    con.close()
    return copy_root


def _run(copy_dir: Path, chat_id: str = GROUP_A) -> dict:
    return group_info(copy_dir=copy_dir, chat_id=chat_id)["group_info"]


class TestContractShape:
    def test_all_fields_full_group(self, group_copies: Path) -> None:
        payload = _run(group_copies)
        # 契约 v1 逐键封闭:零自造键、零缺键(钉死漂移)。
        assert set(payload) == {
            "chat_id",
            "display_name",
            "member_count",
            "owner",
            "announcement",
            "status",
            "members",
        }
        assert payload["chat_id"] == GROUP_A
        assert payload["display_name"] == "合成群A"
        assert payload["member_count"] == 4  # 真行数(含 contact 缺行的 1)
        assert payload["status"] == 524288  # 原样透传,不臆造语义
        assert payload["owner"] == {
            "username": "wxid_owner",
            "display": "群主备注",  # remark > nickname
        }
        assert payload["announcement"] == {
            "text": "请勿发广告",
            "editor_display": "群主备注",
            "published_at": datetime.fromtimestamp(PUB_TS).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

    def test_member_entries_rowid_and_remark(self, group_copies: Path) -> None:
        members = _run(group_copies)["members"]
        for entry in members:
            assert set(entry) == {"username", "display", "remark", "is_owner"}
        # contact 缺行的 member_id=555 弃行(宁缺毋假),不冒充成员
        assert [m["username"] for m in members] == [
            "wxid_a",
            "wxid_b",
            "wxid_owner",
        ]
        by_name = {m["username"]: m for m in members}
        assert by_name["wxid_a"] == {
            "username": "wxid_a",
            "display": "备注A",  # remark 优先
            "remark": "备注A",
            "is_owner": False,
        }
        assert by_name["wxid_b"] == {
            "username": "wxid_b",
            "display": "昵称B",  # 无备注 → nickname 上屏,remark None 如实
            "remark": None,
            "is_owner": False,
        }
        assert by_name["wxid_owner"]["is_owner"] is True

    def test_is_owner_exactly_one(self, group_copies: Path) -> None:
        members = _run(group_copies)["members"]
        assert sum(1 for m in members if m["is_owner"]) == 1
        assert next(m for m in members if m["is_owner"])["username"] == "wxid_owner"

    def test_unknown_chat_all_empty(self, group_copies: Path) -> None:
        payload = _run(group_copies, "1@chatroom")
        assert payload == {
            "chat_id": "1@chatroom",
            "display_name": None,
            "member_count": 0,
            "owner": None,
            "announcement": None,
            "status": None,
            "members": [],
        }

    def test_group_without_settings_and_owner(self, group_copies: Path) -> None:
        """群 B:owner NULL + 无 info_detail 行 + 无成员 → 各键 null/空表。"""
        payload = _run(group_copies, GROUP_B)
        assert payload["owner"] is None
        assert payload["announcement"] is None
        assert payload["status"] is None
        assert payload["members"] == []
        assert payload["member_count"] == 0


class TestDegrade:
    def test_contact_copy_missing_empty_structure(self, group_copies: Path) -> None:
        (group_copies / "contact" / "contact.db").unlink()
        payload = _run(group_copies)
        assert payload == {
            "chat_id": GROUP_A,
            "display_name": None,
            "member_count": 0,
            "owner": None,
            "announcement": None,
            "status": None,
            "members": [],
        }

    def test_contact_domain_only_is_self_sufficient(
        self, group_copies: Path
    ) -> None:
        """单 contact 域自足:无 message/session 目录照样全字段出齐
        (member_id 即 contact rowid,零消息域依赖——2026-10-13 裁决)。"""
        assert not (group_copies / "message").exists()
        payload = _run(group_copies)
        assert payload["member_count"] == 4
        assert payload["owner"]["display"] == "群主备注"
        assert len(payload["members"]) == 3
        assert payload["announcement"]["text"] == "请勿发广告"

    def test_info_detail_table_missing_announcement_status_null(
        self, group_copies: Path
    ) -> None:
        con = sqlite3.connect(group_copies / "contact" / "contact.db")
        con.execute("DROP TABLE chat_room_info_detail")
        con.commit()
        con.close()
        payload = _run(group_copies)
        assert payload["announcement"] is None
        assert payload["status"] is None
        assert payload["owner"]["username"] == "wxid_owner"  # 其余域照常
        assert payload["member_count"] == 4

    def test_chatroom_member_table_missing_count_zero(
        self, group_copies: Path
    ) -> None:
        con = sqlite3.connect(group_copies / "contact" / "contact.db")
        con.execute("DROP TABLE chatroom_member")
        con.commit()
        con.close()
        payload = _run(group_copies)
        assert payload["member_count"] == 0
        assert payload["members"] == []
        assert payload["owner"]["username"] == "wxid_owner"  # 设置域照常

    def test_publish_time_zero_means_unpublished(self, group_copies: Path) -> None:
        con = sqlite3.connect(group_copies / "contact" / "contact.db")
        con.execute(
            "UPDATE chat_room_info_detail SET announcement_publish_time_ = 0"
        )
        con.commit()
        con.close()
        announcement = _run(group_copies)["announcement"]
        assert announcement["published_at"] is None  # 0 = 未发布,不是 1970

    def test_status_blob_is_hex_serialized_not_crash(
        self, group_copies: Path
    ) -> None:
        """status 列值 BLOB:stdout 是 JSON,json.dump 无 default —— bytes
        原样会 TypeError 崩出非契约退出码;守卫转 hex 串保真(可逆零失真),
        整链 exit 0 照常。"""
        con = sqlite3.connect(group_copies / "contact" / "contact.db")
        con.execute(
            "UPDATE chat_room_info_detail SET chat_room_status_ = X'00FF10'"
        )
        con.commit()
        con.close()
        payload = _run(group_copies)
        assert payload["status"] == "00ff10"  # bytes(b"\x00\xff\x10").hex()


class TestCli:
    """CLI 面:密钥缺位(⑤ 形态同款)+ usage 拒;成功链由真跑/引擎测试覆盖。"""

    def _fake_root(self, monkeypatch, tmp_path: Path) -> Path:
        fake_root = tmp_path / "xwechat_files"
        account = fake_root / "wxid_demo_8253"
        (account / "db_storage" / "contact").mkdir(parents=True)
        monkeypatch.setattr("wechat_bridge.localdb.WECHAT_FILES_ROOT", fake_root)
        return fake_root

    def test_key_unavailable(self, monkeypatch, tmp_path: Path) -> None:
        self._fake_root(monkeypatch, tmp_path)
        exit_code, payload = run_cli(
            ["localdb", "group-info", GROUP_A, "--json"],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 21
        assert payload["error"]["code"] == "key_unavailable"

    def test_missing_chat_is_argparse_usage(self, monkeypatch, tmp_path: Path) -> None:
        """缺位置参数 = argparse 级用法错(parse_args 内抛 SystemExit;
        判例同 test_bridge_cli.TestUsageErrors.test_no_command_is_usage)。"""
        self._fake_root(monkeypatch, tmp_path)
        with pytest.raises(SystemExit) as excinfo:
            run_cli(["localdb", "group-info", "--json"], monkeypatch, tmp_path)
        assert excinfo.value.code == 2

    def test_blank_chat_is_usage(self, monkeypatch, tmp_path: Path) -> None:
        """空白群 id = usage 拒(main 内 _require_chat_id,JSON 契约形态)。"""
        self._fake_root(monkeypatch, tmp_path)
        exit_code, payload = run_cli(
            ["localdb", "group-info", "   ", "--json"], monkeypatch, tmp_path
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"
