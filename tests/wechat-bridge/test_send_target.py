"""sendtarget 单测(design §B-1/§G;sqlite 用 tmp_path 建假 contact 库,
localdb 链整体 monkeypatch 注入——零真实微信数据)。

三形态解析、三路命中集唯一性判据(绝不静默取首行)、storage/keys 注入
路径、四档搜索词、指纹稳定性是受测面。
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))

import wechat_bridge.localdb as localdb  # noqa: E402
import wechat_bridge.sendtarget as st  # noqa: E402
from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError  # noqa: E402
from wechat_bridge.config import BridgeConfig  # noqa: E402

#: 靶场两白名单目标的假 contact 行(username/alias/remark/nick)。
ROWS = [
    ("filehelper", "filehelper", "文件传输助手", "文件传输助手"),
    ("wxid_m90epbt5ojml22", "jiangliushi666", None, "🐳"),
    ("wxid_other_111", "other_alias", "同事小张", "张三"),
]


@pytest.fixture()
def contact_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """假 E2 副本目录:contact/contact.db(列名对齐 4.1.15 形态)。"""
    copy_dir = tmp_path / "copies" / "decrypted"
    (copy_dir / "contact").mkdir(parents=True)
    con = sqlite3.connect(copy_dir / "contact" / "contact.db")
    con.execute(
        'CREATE TABLE contact (username TEXT, alias TEXT, remark TEXT, '
        "nick_name TEXT)"
    )
    con.executemany("INSERT INTO contact VALUES (?,?,?,?)", ROWS)
    con.commit()
    con.close()
    # localdb 链整体 mock:locate/resolve/ensure → 假副本目录。
    monkeypatch.setattr(localdb, "locate_db_storage", lambda: tmp_path / "db_storage")
    monkeypatch.setattr(
        localdb, "resolve_keys", lambda storage, *, config=None: {"k": "v"}
    )
    monkeypatch.setattr(
        localdb,
        "ensure_decrypted_copies",
        lambda db_storage, keys, *, domains, ttl_hours, capacity_mb, data_root=None, now=None, runner=None: {
            "dir": str(copy_dir)
        },
    )
    return copy_dir


class TestResolveThreeForms:
    def test_username_direct_lookup(self, contact_db: Path) -> None:
        target = st.resolve_target(BridgeConfig(), "filehelper")
        assert target is not None
        assert target.username == "filehelper"
        assert target.display_name == "文件传输助手"

    def test_alias_reverse_lookup(self, contact_db: Path) -> None:
        target = st.resolve_target(BridgeConfig(), "jiangliushi666")
        assert target is not None
        assert target.username == "wxid_m90epbt5ojml22"
        assert target.display_name == "🐳"
        assert target.search_term == "jiangliushi666"  # alias 纯 ASCII ≥3

    def test_display_name_full_scan_python_compare(self, contact_db: Path) -> None:
        """展示名反查:SQL 全量拉取 + Python compact 比对(sessions list
        的 id 本就是展示名,pixel.py SessionRow 契约)。"""
        target = st.resolve_target(BridgeConfig(), "文件传输助手")
        assert target is not None
        assert target.username == "filehelper"

    def test_display_name_emoji(self, contact_db: Path) -> None:
        target = st.resolve_target(BridgeConfig(), "🐳")
        assert target is not None
        assert target.username == "wxid_m90epbt5ojml22"

    def test_display_name_casefolds_ascii(self, contact_db: Path) -> None:
        """大小写折叠用例:ASCII 名 sqlite BINARY collation 不折叠,
        Python 侧 casefold 命中(design §J-21)。"""
        target = st.resolve_target(BridgeConfig(), "张 三")  # 空白不敏感
        assert target is not None
        assert target.username == "wxid_other_111"

    def test_remark_wins_over_nick_and_alias(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """display_name 取 remark > nick_name > alias(优先序)。"""
        copy_dir = tmp_path / "copies2" / "decrypted"
        (copy_dir / "contact").mkdir(parents=True)
        con = sqlite3.connect(copy_dir / "contact" / "contact.db")
        con.execute("CREATE TABLE contact (username, alias, remark, nick_name)")
        con.execute(
            "INSERT INTO contact VALUES ('u1','a1','备注名','昵称名')"
        )
        con.commit()
        con.close()
        monkeypatch.setattr(localdb, "locate_db_storage", lambda: tmp_path)
        monkeypatch.setattr(
            localdb, "resolve_keys", lambda storage, *, config=None: {}
        )
        monkeypatch.setattr(
            localdb,
            "ensure_decrypted_copies",
            lambda *a, **k: {"dir": str(copy_dir)},
        )
        target = st.resolve_target(BridgeConfig(), "备注名")
        assert target is not None and target.display_name == "备注名"

    def test_no_hit_returns_none(self, contact_db: Path) -> None:
        assert st.resolve_target(BridgeConfig(), "no_such_zzz123") is None


class TestAmbiguity:
    def test_alias_multiple_hits_is_ambiguous(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """alias 反查多行 → send_target_ambiguous(绝不静默取首行,
        design §J-21)。"""
        copy_dir = tmp_path / "copies3" / "decrypted"
        (copy_dir / "contact").mkdir(parents=True)
        con = sqlite3.connect(copy_dir / "contact" / "contact.db")
        con.execute("CREATE TABLE contact (username, alias, remark, nick_name)")
        con.executemany(
            "INSERT INTO contact VALUES (?,?,?,?)",
            [("u1", "same_alias", "甲", "甲"), ("u2", "same_alias", "乙", "乙")],
        )
        con.commit()
        con.close()
        monkeypatch.setattr(localdb, "locate_db_storage", lambda: tmp_path)
        monkeypatch.setattr(
            localdb, "resolve_keys", lambda storage, *, config=None: {}
        )
        monkeypatch.setattr(
            localdb,
            "ensure_decrypted_copies",
            lambda *a, **k: {"dir": str(copy_dir)},
        )
        with pytest.raises(BridgeError) as excinfo:
            st.resolve_target(BridgeConfig(), "same_alias")
        assert excinfo.value.exit_code == 1
        assert excinfo.value.name == "send_target_ambiguous"
        assert "消歧" in (excinfo.value.fix_hint or "")

    def test_display_name_and_username_cross_paths_merge_to_ambiguous(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """三路命中合集 >1(展示名撞另一个 username)→ 同样 ambiguous。"""
        copy_dir = tmp_path / "copies4" / "decrypted"
        (copy_dir / "contact").mkdir(parents=True)
        con = sqlite3.connect(copy_dir / "contact" / "contact.db")
        con.execute("CREATE TABLE contact (username, alias, remark, nick_name)")
        con.executemany(
            "INSERT INTO contact VALUES (?,?,?,?)",
            [("wxid_a", None, None, "小美"), ("小美", None, None, "别的人")],
        )
        con.commit()
        con.close()
        monkeypatch.setattr(localdb, "locate_db_storage", lambda: tmp_path)
        monkeypatch.setattr(
            localdb, "resolve_keys", lambda storage, *, config=None: {}
        )
        monkeypatch.setattr(
            localdb,
            "ensure_decrypted_copies",
            lambda *a, **k: {"dir": str(copy_dir)},
        )
        with pytest.raises(BridgeError) as excinfo:
            st.resolve_target(BridgeConfig(), "小美")
        assert excinfo.value.name == "send_target_ambiguous"


class TestChainInjection:
    def test_storage_keys_injection_skips_self_resolution(
        self, contact_db: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """注入 storage/keys 时不再自解析(单次解析纪律,§J-19)。"""
        calls = {"resolve": 0, "locate": 0}

        def fail_resolve(storage, *, config=None):
            calls["resolve"] += 1
            return {}

        def fail_locate():
            calls["locate"] += 1
            return tmp_path

        monkeypatch.setattr(localdb, "resolve_keys", fail_resolve)
        monkeypatch.setattr(localdb, "locate_db_storage", fail_locate)
        target = st.resolve_target(
            BridgeConfig(), "filehelper", storage=Path("/injected"), keys={"k": "v"}
        )
        assert target is not None and target.username == "filehelper"
        assert calls == {"resolve": 0, "locate": 0}

    def test_chain_bridge_error_passthrough_with_stage_note(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """localdb 链 20/21/22 族原样透传,消息注记「发送前目标解析」。"""

        def fail(storage, *, config=None):
            raise BridgeError(KEY_UNAVAILABLE, "本地库密钥不可得", fix_hint="D4")

        monkeypatch.setattr(localdb, "locate_db_storage", lambda: tmp_path)
        monkeypatch.setattr(localdb, "resolve_keys", fail)
        with pytest.raises(BridgeError) as excinfo:
            st.resolve_target(BridgeConfig(), "filehelper")
        assert excinfo.value.exit_code == 21
        assert excinfo.value.message.startswith("发送前目标解析:")
        assert "key-acquire" in (excinfo.value.fix_hint or "")


class TestSearchTermAndFingerprint:
    def test_pick_search_term_four_tiers(self) -> None:
        # 档1:alias 纯 ASCII ≥3
        assert st.pick_search_term("wxid_m90epbt5ojml22", "jiangliushi666", "🐳") == "jiangliushi666"
        # 档1 不取短 alias / 非 ASCII alias
        assert st.pick_search_term("wxid_x", "ab", "名") == "wxid_x"  # <3 落档3
        # 档2:非 wxid_ 纯 ASCII username(filehelper / gh_ 公众号)
        assert st.pick_search_term("filehelper", None, "文件传输助手") == "filehelper"
        assert st.pick_search_term("gh_abc123", None, "公众号名") == "gh_abc123"
        # 档3:wxid_ username
        assert st.pick_search_term("wxid_m90epbt5ojml22", None, "🐳") == "wxid_m90epbt5ojml22"
        # 档4:全非 ASCII(username 中文 + 无可用 alias)
        assert st.pick_search_term("中文名", None, "中文名") == "中文名"

    def test_row_match_terms_dedup_keeps_priority(self, contact_db: Path) -> None:
        target = st.resolve_target(BridgeConfig(), "jiangliushi666")
        assert target is not None
        terms = st.row_match_terms(target)
        assert terms[0] == "🐳"  # display_name 在首(结果行显示的是它)
        assert "jiangliushi666" in terms
        assert "wxid_m90epbt5ojml22" in terms
        assert len(terms) == len(set(terms))

    def test_fingerprint_stable_across_three_forms(self, contact_db: Path) -> None:
        """三形态入参解析到同一目标 → 同指纹(防重闭合,design §1-5)。"""
        by_username = st.resolve_target(BridgeConfig(), "wxid_m90epbt5ojml22")
        by_alias = st.resolve_target(BridgeConfig(), "jiangliushi666")
        by_display = st.resolve_target(BridgeConfig(), "🐳")
        assert by_username and by_alias and by_display
        body = "嘻嘻"
        keys = {
            st.fingerprint(t, body) for t in (by_username, by_alias, by_display)
        }
        assert len(keys) == 1
        # 同目标异正文 → 异指纹
        assert st.fingerprint(by_username, body) != st.fingerprint(by_username, "嘻嘻2")

    def test_fingerprint_shape_is_sha256_hex(self, contact_db: Path) -> None:
        import hashlib

        target = st.resolve_target(BridgeConfig(), "filehelper")
        assert target is not None
        want = hashlib.sha256("filehelper\0嘻嘻".encode("utf-8")).hexdigest()
        assert st.fingerprint(target, "嘻嘻") == want
