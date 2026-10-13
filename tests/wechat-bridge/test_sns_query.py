"""E3 朋友圈域查询单测(task 10-13-wechat-sns-feed;合成明文副本,零真实内容)。

夹具形状照 2026-10-13 直查本机解密副本实测 DDL(``SnsTimeLine`` 四列 +
content XML;``SnsMessage_tmp3`` 通知宽表,feed_id INTEGER 雪花 id);内容
全合成。CLI 面照 ``test_bridge_cli.py`` 的 ⑤ 形态(密钥缺位 → exit 21)。

golden 基件只加一锚(CLI 缺钥错误形态):feed/notices 的错误载荷同形
(不含 argv),双锚零增量信息;成功载荷的形状对账由本文件合成副本用例
承担(比 golden 更细,design §4「+2 锚」的 grill 裁量修正,见
implement.md 勾档注记)。
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path

import pytest

from bridge_testkit import run_cli
from wechat_bridge.codes import DB_NOT_FOUND, DECRYPT_FAILED, BridgeError
from wechat_bridge.sns_query import (
    FEED_TABLE,
    NOTICES_TABLE,
    parse_feed_row,
    run_sns_query,
)

NOW = int(time.time())

#: 合成 XML 模板(真形状:SnsDataItem/TimelineObject + ContentObject/
#: mediaList + 转发源;字段序照实测)。
_XML = (
    "<SnsDataItem><TimelineObject>"
    "<id>{entry_id}</id><username>{user}</username>"
    "<createTime>{ts}</createTime><contentDesc>{text}</contentDesc>"
    "<ContentObject><mediaList>{media}</mediaList></ContentObject>"
    "<sourceUserName>{ref_user}</sourceUserName>"
    "<sourceNickName>{ref_nick}</sourceNickName>"
    "</TimelineObject></SnsDataItem>"
)
_MEDIA = "<media><type>{t}</type></media>"


def _feed_xml(
    entry_id: str,
    user: str,
    ts: int,
    text: str,
    media_types: list[str] | None = None,
    ref_user: str = "",
    ref_nick: str = "",
) -> str:
    media = "".join(_MEDIA.format(t=t) for t in (media_types or []))
    return _XML.format(
        entry_id=entry_id, user=user, ts=ts, text=text, media=media,
        ref_user=ref_user, ref_nick=ref_nick,
    )


@pytest.fixture()
def sns_copies(tmp_path: Path) -> Path:
    """合成解密副本(sns+contact 双域,全合成内容,零真实语料)。"""
    copy_root = tmp_path / "decrypted"
    sns = copy_root / "sns" / "sns.db"
    sns.parent.mkdir(parents=True)
    con = sqlite3.connect(sns)
    con.execute(
        f'CREATE TABLE "{FEED_TABLE}" (tid INTEGER, user_name TEXT, '
        "content TEXT, pack_info_buf TEXT)"
    )
    rows = [
        # 窗口内:正文+双图,contact 域有 remark → nickname 回填
        (1, "wxid_a", _feed_xml("9001", "wxid_a", NOW - 600, "合成正文-一", ["2", "2"])),
        # 窗口内:纯图(正文空)→ text=None,media_count 透传
        (2, "wxid_b", _feed_xml("9002", "wxid_b", NOW - 1200, "", ["2"])),
        # 窗口内:转发形态(ref 双字段)
        (3, "wxid_c", _feed_xml(
            "9003", "wxid_c", NOW - 1800, "合成转发", [], "wxid_src", "被转发的原作者",
        )),
        # 窗口外(40 天前):滤掉,计 out_of_window
        (4, "wxid_a", _feed_xml("9004", "wxid_a", NOW - 40 * 86400, "旧动态", [])),
        # 坏 XML:弃行计 parse_errors,不炸整轮
        (5, "wxid_d", "<SnsDataItem><TimelineObject>未闭合"),
        # 窗口内但缺 id 字段:必要字段缺失 → 弃行计 parse_errors
        (6, "wxid_e", _feed_xml("", "wxid_e", NOW - 60, "无 id")),
    ]
    con.executemany(
        f'INSERT INTO "{FEED_TABLE}" VALUES (?,?,?,?)',
        [(t, u, c, "") for t, u, c in rows],
    )
    con.execute(
        f'CREATE TABLE "{NOTICES_TABLE}" (local_id INTEGER PRIMARY KEY, '
        "create_time INTEGER, type INTEGER, feed_id INTEGER, is_unread INTEGER, "
        "from_username TEXT, from_nickname TEXT, to_username TEXT, "
        "to_nickname TEXT, content TEXT, serialized_comment_buf BLOB, "
        "comment_id INTEGER, client_id TEXT, comment64_id INTEGER, "
        "comment_flag INTEGER, del_status INTEGER, is_relative_me INTEGER)"
    )
    notices = [
        # like:content 空,feed_id 雪花 id(INTEGER)
        (247, NOW - 86400, 1, -3417398247010987346, "wxid_f", "合成赞者", None, 0),
        # comment:content = 评论文本
        (248, NOW - 7200, 2, -3417446710553996519, "wxid_g", "合成评论者", "合成评论文本", 1),
        # 未知 type:原样数字字符串
        (249, NOW - 3600, 99, None, "wxid_h", "未知型", None, 0),
        # 窗口外:SQL 滤掉
        (250, NOW - 30 * 86400, 1, None, "wxid_f", "旧赞", None, 0),
    ]
    con.executemany(
        f'INSERT INTO "{NOTICES_TABLE}" (local_id, create_time, type, feed_id, '
        "from_username, from_nickname, content, is_relative_me) "
        "VALUES (?,?,?,?,?,?,?,?)",
        notices,
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
    con.executemany(
        "INSERT INTO contact VALUES (?,?,?,?,1)",
        [
            ("wxid_a", "", "昵称A", "备注A",),
            ("wxid_b", "", "昵称B", "",),
            # wxid_c 无 contact 行:nickname=None 如实回落 username
        ],
    )
    con.commit()
    con.close()
    return copy_root


def _run(copy_dir: Path, mode: str, days: int = 3) -> dict:
    return run_sns_query(
        copy_dir=copy_dir, mode=mode, since_days=days,
        copy_info={"dir": str(copy_dir), "built": [], "kept": []},
    )["sns"]


class TestParseFeedRow:
    def test_full_shape(self) -> None:
        entry = parse_feed_row(_feed_xml(
            "123", "wxid_x", 1791891649, "正文", ["2", "4"], "wxid_r", "转发源",
        ))
        assert entry == {
            "id": "123",
            "username": "wxid_x",
            "nickname": None,
            "create_time": 1791891649,
            "text": "正文",
            "media_count": 2,
            "media_types": ["2", "4"],
            "ref_username": "wxid_r",
            "ref_nickname": "转发源",
        }

    def test_bad_xml_and_missing_required(self) -> None:
        assert parse_feed_row("不是 XML") is None
        assert parse_feed_row(None) is None
        assert parse_feed_row(_feed_xml("1", "u", 1, "t").replace(
            "<createTime>1</createTime>", "<createTime>x</createTime>"
        )) is None  # createTime 非数字 → 弃


class TestFeed:
    def test_window_fields_nickname_ref(self, sns_copies: Path) -> None:
        payload = _run(sns_copies, "feed")
        feed = payload["feed"]
        assert len(feed) == 3  # 6 行 - 1 窗口外 - 2 坏行
        assert payload["rows_total"] == 6
        assert payload["rows_out_of_window"] == 1
        assert payload["parse_errors"] == 2
        by_id = {item["id"]: item for item in feed}
        assert by_id["9001"]["nickname"] == "备注A"  # remark 优先
        assert by_id["9001"]["text"] == "合成正文-一"
        assert by_id["9001"]["media_types"] == ["2", "2"]
        assert by_id["9002"]["text"] is None and by_id["9002"]["media_count"] == 1
        assert by_id["9003"]["ref_nickname"] == "被转发的原作者"
        assert "9004" not in by_id  # 窗口外
        assert by_id["9001"]["nickname"] and by_id["9002"]["nickname"] == "昵称B"
        # contact 域未解出的(wxid_c)= None 如实
        assert by_id["9003"]["nickname"] is None
        # 升序(create_time)
        times = [item["create_time"] for item in feed]
        assert times == sorted(times)

    def test_contact_domain_missing_nickname_none(self, sns_copies: Path) -> None:
        (sns_copies / "contact" / "contact.db").unlink()
        payload = _run(sns_copies, "feed")
        assert all(item["nickname"] is None for item in payload["feed"])
        assert payload["domains"]["contact"] == "copy_missing"

    def test_copy_missing_raises_decrypt_failed(self, tmp_path: Path) -> None:
        with pytest.raises(BridgeError) as excinfo:
            _run(tmp_path, "feed")
        assert excinfo.value.exit_code == DECRYPT_FAILED

    def test_table_missing_raises_db_not_found(self, sns_copies: Path) -> None:
        con = sqlite3.connect(sns_copies / "sns" / "sns.db")
        con.execute(f'DROP TABLE "{FEED_TABLE}"')
        con.commit()
        con.close()
        with pytest.raises(BridgeError) as excinfo:
            _run(sns_copies, "feed")
        assert excinfo.value.exit_code == DB_NOT_FOUND


class TestNotices:
    def test_type_map_window_feed_id_str(self, sns_copies: Path) -> None:
        payload = _run(sns_copies, "notices")
        notices = payload["notices"]
        assert len(notices) == 3  # 4 行 - 1 窗口外(SQL 层滤)
        # rows_total 语义不对称是设计使然:feed 窗口过滤在 Python(rows_total
        # = 全表行数,out_of_window 另计);notices 在 SQL(rows_total = 窗口
        # 内行数)。各自如实,消费方按 mode 解释。
        assert payload["rows_total"] == 3
        assert [n["type"] for n in notices] == ["like", "comment", "99"]
        assert [n["local_id"] for n in notices] == [247, 248, 249]
        # feed_id INTEGER → str;None 原样
        assert notices[0]["feed_id"] == "-3417398247010987346"
        assert notices[2]["feed_id"] is None
        # like content 恒空 → None;comment 带文本
        assert notices[0]["content"] is None
        assert notices[1]["content"] == "合成评论文本"
        assert notices[1]["is_relative_me"] == 1
        assert notices[0]["from_nickname"] == "合成赞者"

    def test_table_missing_raises_db_not_found(self, sns_copies: Path) -> None:
        con = sqlite3.connect(sns_copies / "sns" / "sns.db")
        con.execute(f'DROP TABLE "{NOTICES_TABLE}"')
        con.commit()
        con.close()
        with pytest.raises(BridgeError) as excinfo:
            _run(sns_copies, "notices")
        assert excinfo.value.exit_code == DB_NOT_FOUND


class TestCli:
    """CLI 面:密钥缺位(⑤ 形态同款)+ usage 拒;成功链由真跑/引擎测试覆盖。"""

    def _fake_root(self, monkeypatch, tmp_path: Path) -> Path:
        fake_root = tmp_path / "xwechat_files"
        account = fake_root / "wxid_demo_8253"
        (account / "db_storage" / "sns").mkdir(parents=True)
        monkeypatch.setattr("wechat_bridge.localdb.WECHAT_FILES_ROOT", fake_root)
        return fake_root

    @pytest.mark.parametrize("mode", ["feed", "notices"])
    def test_key_unavailable(self, monkeypatch, tmp_path: Path, mode: str) -> None:
        self._fake_root(monkeypatch, tmp_path)
        exit_code, payload = run_cli(
            ["localdb", "sns", mode, "--since", "3d", "--json"],
            monkeypatch, tmp_path,
        )
        assert exit_code == 21
        assert payload["error"]["code"] == "key_unavailable"

    def test_usage_rejections(self, monkeypatch, tmp_path: Path) -> None:
        self._fake_root(monkeypatch, tmp_path)
        # 0d 非法:走 _parse_since_days 的 BridgeError(exit 2 正常返回)
        exit_code, payload = run_cli(
            ["localdb", "sns", "feed", "--since", "0d", "--json"],
            monkeypatch, tmp_path,
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"
        # 缺 --since / 未知子命令:argparse 用法错走 SystemExit(2)(既有
        # TestUsageErrors 同款断言形态)
        for argv in (["localdb", "sns", "feed"], ["localdb", "sns", "bogus"]):
            with pytest.raises(SystemExit) as excinfo:
                run_cli(argv + ["--json"], monkeypatch, tmp_path)
            assert excinfo.value.code == 2
