"""Tests for G9 server-side read state (PRD 10-04-read-state-server, engine 件).

store 层验收(design.md §1-§3 对应面;协议/迁移 handler 面归
test_desktop_sidecar_protocol.py):

- 表结构:items.read/starred/later 三列(NOT NULL DEFAULT 0)+ 
  idx_items_dedup_key(非 UNIQUE);fresh 库直建 v8 与 v7 旧库迁移两路径同形;
- 语义红线:save_item 列清单不含三列——采集管线永不携带读态,新入库行
  恒为未读;置位只走本批三方法;
- set_item_states:按 dedup_key 置位,同键多行(dated-key 旋转)同置,
  rowcount 口径 = 匹配行数;
- set_all_item_states:全库单 UPDATE,category 精确等值过滤,无 query 面;
- import_item_states:key 三分(dedup_key 直配 / id:<n> 映射 / id:<url> 与
  无法解析跳过),整键覆盖,缺省标记继承现有列值,{} 值条目跳写。

全部 I/O 走 tmp_path 存储,零真实网络/时钟依赖。
"""

from __future__ import annotations

import sqlite3

import pytest

from myssia.store import SCHEMA_VERSION, ItemRecord, SQLiteStore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture()
def store(tmp_path):
    """A throwaway SQLiteStore per test (zero shared state between tests)."""
    db = SQLiteStore(tmp_path / "read-state.db")
    yield db
    db.close()


def add_item(
    store: SQLiteStore,
    *,
    url: str,
    dedup_key: str | None = None,
    category: str | None = "羊毛",
    title: str = "条目",
) -> ItemRecord:
    """Seed one item and return the stored row (with its id)."""
    store.save_item(
        ItemRecord(url=url, dedup_key=dedup_key or url, title=title, category=category)
    )
    item = store.get_item_by_dedup_key(dedup_key or url)
    assert item is not None
    return item


def item_columns(store: SQLiteStore) -> set[str]:
    return {
        str(row[1])
        for row in store.conn.execute("PRAGMA table_info(items)").fetchall()
    }


def index_names(store: SQLiteStore) -> set[str]:
    return {
        str(row[0])
        for row in store.conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'index'"
        ).fetchall()
    }


# ---------------------------------------------------------------------------
# 表结构:fresh v8 直建 + save_item 缺省语义
# ---------------------------------------------------------------------------


class TestFreshSchemaV8:
    def test_schema_version_is_8(self, store):
        assert SCHEMA_VERSION >= 9  # v10 = runs.log_run_id(10-07-logs-restart-visibility)
        assert int(store.get_meta("schema_version")) == SCHEMA_VERSION

    def test_items_table_has_three_state_columns_with_defaults(self, store):
        columns = {
            str(row[1]): row for row in store.conn.execute("PRAGMA table_info(items)")
        }
        for name in ("read", "starred", "later"):
            assert name in columns
            # notnull=1 且 dflt_value='0':新条目 = 未读/无星/无稍后读(语义即缺省)。
            assert columns[name][3] == 1, f"{name} 必须 NOT NULL"
            assert columns[name][4] == "0", f"{name} 缺省必须为 0"

    def test_dedup_key_index_present_and_not_unique(self, store):
        assert "idx_items_dedup_key" in index_names(store)
        # 非 UNIQUE:dated-key 旋转下同键多行合法(同键多行同置的存储前提)。
        sql = store.conn.execute(
            "SELECT sql FROM sqlite_master WHERE name = 'idx_items_dedup_key'"
        ).fetchone()[0]
        assert "UNIQUE" not in str(sql).upper()

    def test_new_item_defaults_all_false(self, store):
        item = add_item(store, url="https://a/1")
        assert (item.read, item.starred, item.later) == (False, False, False)

    def test_save_item_never_persists_state_even_if_record_carries_it(self, store):
        """采集管线永不携带读态(design §1.4):INSERT 列清单不含三列。"""
        store.save_item(
            ItemRecord(
                url="https://a/2", dedup_key="https://a/2", title="带态入库", read=True, starred=True
            )
        )
        item = store.get_item_by_dedup_key("https://a/2")
        assert item is not None
        assert (item.read, item.starred, item.later) == (False, False, False)


# ---------------------------------------------------------------------------
# 迁移:v7 旧库 → v8(两路径同形,行保留,迁移不猜测读态)
# ---------------------------------------------------------------------------

#: v7 期 items 表形状(无 read/starred/later 三列;直造旧表而非从 v8 降级
#: ——SQLite DROP COLUMN 会因建表 DDL 中的行注释重建出非法语句,而真实
#: 旧库本就是这种带列旧形状,直造更忠实)。
_V7_ITEMS_DDL = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    dedup_key TEXT NOT NULL,
    source TEXT,
    title TEXT NOT NULL,
    content TEXT,
    content_hash TEXT,
    tags TEXT,
    category TEXT,
    scores TEXT,
    pushed_at TEXT,
    push_slot TEXT,
    first_seen TEXT NOT NULL,
    raw TEXT
);
"""


def make_v7_database(path, rows: list[tuple[str, str, str]]) -> None:
    """手造 v7 库:旧形状 items 表 + 版本戳 7(模拟升级前的库文件)。

    其余表(dedup_registry/runs/store_meta 之外)由 init_schema 的
    ``CREATE TABLE IF NOT EXISTS`` 在重开时补建,迁移只关心 items 列形状。
    """
    raw = sqlite3.connect(path)
    raw.executescript(
        _V7_ITEMS_DDL
        + "CREATE TABLE IF NOT EXISTS store_meta"
        + " (key TEXT PRIMARY KEY, value TEXT NOT NULL);"
    )
    raw.execute("INSERT INTO store_meta (key, value) VALUES ('schema_version', '7')")
    raw.executemany(
        "INSERT INTO items (url, dedup_key, title, first_seen) VALUES (?, ?, ?, '2026-10-01T00:00:00+00:00')",
        rows,
    )
    raw.commit()
    raw.close()


class TestMigrationV7ToV8:
    def test_v7_database_migrates_to_v8_preserving_rows(self, tmp_path):
        """v7 库(无三列)打开即补齐,既有数据零丢失且读态不猜测。"""
        path = tmp_path / "legacy-v7.db"
        make_v7_database(
            path,
            [
                ("https://old/1", "https://old/1", "旧条目一"),
                ("https://old/2", "https://old/2", "旧条目二"),
            ],
        )

        migrated = SQLiteStore(path)
        try:
            assert int(migrated.get_meta("schema_version")) == SCHEMA_VERSION
            assert {"read", "starred", "later"} <= item_columns(migrated)
            assert "idx_items_dedup_key" in index_names(migrated)
            titles = [item.title for item in migrated.list_items()]
            assert sorted(titles) == ["旧条目一", "旧条目二"]
            # 迁移不猜测读态:存量行三态全 0(未读),首切由 import 搬运。
            for item in migrated.list_items():
                assert (item.read, item.starred, item.later) == (False, False, False)
            # 迁移后的列立即可写(同 v3→v4 先例:补表/补列后马上真用)。
            assert migrated.set_item_states(["https://old/1"], "read", True) == 1
            assert migrated.get_item_by_dedup_key("https://old/1").read is True
        finally:
            migrated.close()

    def test_migration_idempotent_on_reopen(self, tmp_path):
        """重开即续:已到 v8 的库再开一次,不重放 ALTER、行与状态原样。"""
        path = tmp_path / "reopen.db"
        first = SQLiteStore(path)
        add_item(first, url="https://r/1")
        assert first.set_item_states(["https://r/1"], "read", True) == 1
        first.close()

        again = SQLiteStore(path)
        try:
            assert int(again.get_meta("schema_version")) == SCHEMA_VERSION
            assert again.get_item_by_dedup_key("https://r/1").read is True
        finally:
            again.close()

    def test_partially_migrated_database_resumes(self, tmp_path):
        """三列 ALTER 中断后重开可续(逐列独立幂等 if,不要求原子批)。

        「迁移做到一半崩了」的形状:read 列已 ALTER 出(且可能已被置位),
        starred/later 仍缺,版本戳还在 7 —— 重开补齐剩余列且不动已有列值。
        """
        path = tmp_path / "half.db"
        make_v7_database(path, [("https://h/1", "https://h/1", "半迁移条目")])
        raw = sqlite3.connect(path)
        raw.execute("ALTER TABLE items ADD COLUMN read INTEGER NOT NULL DEFAULT 0")
        raw.execute("UPDATE items SET read = 1 WHERE dedup_key = 'https://h/1'")
        raw.commit()
        raw.close()

        resumed = SQLiteStore(path)
        try:
            assert int(resumed.get_meta("schema_version")) == SCHEMA_VERSION
            assert {"read", "starred", "later"} <= item_columns(resumed)
            assert "idx_items_dedup_key" in index_names(resumed)
            # 中断前已置位的列值原样保留(幂等 if 只补缺列,不重置已有)。
            item = resumed.get_item_by_dedup_key("https://h/1")
            assert item.read is True
            assert (item.starred, item.later) == (False, False)
        finally:
            resumed.close()


# ---------------------------------------------------------------------------
# set_item_states:按 dedup_key 置位(同键多行同置红线)
# ---------------------------------------------------------------------------


class TestSetItemStates:
    def test_marks_single_key_and_returns_matched_rows(self, store):
        add_item(store, url="https://s/1")
        add_item(store, url="https://s/2")

        assert store.set_item_states(["https://s/1"], "read", True) == 1
        one = store.get_item_by_dedup_key("https://s/1")
        two = store.get_item_by_dedup_key("https://s/2")
        assert one.read is True
        assert two.read is False  # 未列出的键不动。

    def test_marks_three_markers_independently(self, store):
        add_item(store, url="https://m/1")
        keys = ["https://m/1"]
        assert store.set_item_states(keys, "starred", True) == 1
        assert store.set_item_states(keys, "later", True) == 1
        item = store.get_item_by_dedup_key("https://m/1")
        assert (item.read, item.starred, item.later) == (False, True, True)

    def test_stores_zero_one_integers_not_booleans(self, store):
        add_item(store, url="https://i/1")
        store.set_item_states(["https://i/1"], "read", True)
        row = store.conn.execute(
            "SELECT read FROM items WHERE dedup_key = 'https://i/1'"
        ).fetchone()
        assert row[0] == 1  # 库列 0/1,与协议层 bool 互转(design §1.1)。

    def test_rowcount_counts_matched_rows_including_same_value(self, store):
        """rowcount 口径:匹配行数——显式置同值也计入,如实回传不二次核算。"""
        add_item(store, url="https://c/1")
        assert store.set_item_states(["https://c/1"], "read", True) == 1
        assert store.set_item_states(["https://c/1"], "read", True) == 1  # 幂等重放同计数。
        assert store.set_item_states(["https://c/1"], "read", False) == 1  # 回置未读。

    def test_unknown_keys_report_zero_matched(self, store):
        add_item(store, url="https://u/1")
        assert store.set_item_states(["https://gone/1"], "read", True) == 0

    def test_same_dedup_key_multi_row_all_marked(self, store):
        """AC2 红线:dated-key 旋转下同键多行同置(与 localStorage itemKey 语义一致)。"""
        add_item(store, url="https://d/old", dedup_key="dated:2026-10-01", title="旧轮")
        add_item(store, url="https://d/new", dedup_key="dated:2026-10-01", title="新轮")

        assert store.set_item_states(["dated:2026-10-01"], "read", True) == 2
        rows = store.list_items()
        assert len(rows) == 2
        assert all(item.read for item in rows)

    def test_invalid_inputs_raise_value_error(self, store):
        add_item(store, url="https://v/1")
        with pytest.raises(ValueError, match="marker"):
            store.set_item_states(["https://v/1"], "deleted", True)  # 白名单外 marker
        with pytest.raises(ValueError, match="dedup_keys"):
            store.set_item_states([], "read", True)  # 空列表
        with pytest.raises(ValueError, match="dedup_keys"):
            store.set_item_states(["ok", ""], "read", True)  # 含空串
        with pytest.raises(ValueError, match="dedup_keys"):
            store.set_item_states(["ok", 5], "read", True)  # 含非字符串


# ---------------------------------------------------------------------------
# set_all_item_states:全库单 UPDATE(「全部标已读」的全库语义底座)
# ---------------------------------------------------------------------------


class TestSetAllItemStates:
    def test_marks_whole_library(self, store):
        add_item(store, url="https://all/1")
        add_item(store, url="https://all/2")
        add_item(store, url="https://all/3", category="情报")

        assert store.set_all_item_states("read", True) == 3
        assert all(item.read for item in store.list_items())

        assert store.set_all_item_states("read", False) == 3  # 全库回置未读。
        assert not any(item.read for item in store.list_items())

    def test_category_filter_is_exact_equality(self, store):
        """category 词义与 list_items 同参:精确等值,非 LIKE。"""
        add_item(store, url="https://cat/1", category="羊毛")
        add_item(store, url="https://cat/2", category="羊毛")
        add_item(store, url="https://cat/3", category="情报")

        assert store.set_all_item_states("starred", True, category="羊毛") == 2
        by_key = {item.dedup_key: item for item in store.list_items()}
        assert by_key["https://cat/1"].starred is True
        assert by_key["https://cat/2"].starred is True
        assert by_key["https://cat/3"].starred is False

    def test_invalid_inputs_raise_value_error(self, store):
        with pytest.raises(ValueError, match="marker"):
            store.set_all_item_states("hidden", True)
        with pytest.raises(ValueError, match="category"):
            store.set_all_item_states("read", True, category="")  # 空串 ≠ 全库

    def test_source_kind_filter_is_prefix_gate(self, store):
        """source_kind 作用域(10-08-tg-channel-card v2,卡片墙第二层批量):
        im = telegram/tg 前缀源,web = 其余含无源;非法值 ValueError。"""
        store.save_item(
            ItemRecord(url="https://im/1", dedup_key="im1", title="条目", source="telegram-durov")
        )
        store.save_item(
            ItemRecord(url="https://im/2", dedup_key="im2", title="条目", source="tg-openai_news")
        )
        store.save_item(
            ItemRecord(url="https://web/1", dedup_key="web1", title="条目", source="openai-news")
        )
        store.save_item(ItemRecord(url="https://web/2", dedup_key="web2", title="条目", source=None))

        assert store.set_all_item_states("read", True, source_kind="im") == 2
        by_key = {item.dedup_key: item for item in store.list_items()}
        assert by_key["im1"].read is True
        assert by_key["im2"].read is True
        assert by_key["web1"].read is False
        assert by_key["web2"].read is False

        assert store.set_all_item_states("read", True, source_kind="web") == 2
        assert all(item.read for item in store.list_items())

        with pytest.raises(ValueError, match="source_kind"):
            store.set_all_item_states("read", True, source_kind="bogus")


# ---------------------------------------------------------------------------
# import_item_states:localStorage 快照一次性搬迁(key 三分 + 整键覆盖)
# ---------------------------------------------------------------------------


class TestImportItemStates:
    def test_direct_dedup_key_applies_full_snapshot(self, store):
        add_item(store, url="https://imp/1")
        imported, skipped = store.import_item_states(
            {"https://imp/1": {"read": True, "starred": True, "later": False}}
        )
        assert (imported, skipped) == (1, 0)
        item = store.get_item_by_dedup_key("https://imp/1")
        assert (item.read, item.starred, item.later) == (True, True, False)

    def test_id_numeric_reference_maps_to_dedup_key(self, store):
        """id:<n> 形态:先按行 id 取 dedup_key 再置位(itemKey 的 id 兜底来源)。"""
        item = add_item(store, url="https://imp/id", dedup_key="opaque-key")
        imported, skipped = store.import_item_states({f"id:{item.id}": {"read": True}})
        assert (imported, skipped) == (1, 0)
        assert store.get_item_by_dedup_key("opaque-key").read is True

    def test_id_url_form_and_unknown_keys_count_skipped(self, store):
        """id:<url> 形态与无匹配键如实计 skipped,不复活已剪枝条目(AC4)。"""
        add_item(store, url="https://imp/2")
        imported, skipped = store.import_item_states(
            {
                "id:https://imp/never-had-id": {"read": True},  # id:<url>:无从解析
                "https://pruned/long-gone": {"read": True},  # 已剪枝:自然落空
                "id:999999": {"read": True},  # id 合法但行不存在
            }
        )
        assert (imported, skipped) == (0, 3)

    def test_partial_snapshot_inherits_unmentioned_markers(self, store):
        """缺省态继承现有列值——只覆盖快照中出现的键(design §3.3)。"""
        add_item(store, url="https://part/1")
        store.set_item_states(["https://part/1"], "starred", True)
        store.set_item_states(["https://part/1"], "later", True)

        imported, _ = store.import_item_states({"https://part/1": {"read": True}})
        assert imported == 1
        item = store.get_item_by_dedup_key("https://part/1")
        assert (item.read, item.starred, item.later) == (True, True, True)

    def test_empty_snapshot_entry_is_skip_written(self, store):
        """三键全缺省({} 值)条目跳写:不触库,计入 skipped。"""
        add_item(store, url="https://empty/1")
        imported, skipped = store.import_item_states({"https://empty/1": {}})
        assert (imported, skipped) == (0, 1)
        assert store.get_item_by_dedup_key("https://empty/1").read is False

    def test_same_dedup_key_multi_row_import_marks_all(self, store):
        add_item(store, url="https://mi/a", dedup_key="shared", title="甲")
        add_item(store, url="https://mi/b", dedup_key="shared", title="乙")

        imported, skipped = store.import_item_states({"shared": {"read": True}})
        assert (imported, skipped) == (1, 0)
        assert all(item.read for item in store.list_items())

    def test_replay_overwrites_without_flag_guards(self, store):
        """store 方法本身可重复调用(重放 = 再覆盖)——幂等必须由 handler 侧旗标保证。"""
        add_item(store, url="https://rep/1")
        store.import_item_states({"https://rep/1": {"read": True}})
        imported, _ = store.import_item_states({"https://rep/1": {"read": False}})
        assert imported == 1
        assert store.get_item_by_dedup_key("https://rep/1").read is False

    def test_import_flag_roundtrip_via_store_meta(self, store):
        """搬迁幂等旗标走既有 store_meta 设施(design §3.4,零新增代码)。"""
        assert store.get_meta("feed_state_imported_at") is None
        store.set_meta("feed_state_imported_at", "2026-10-04T12:00:00+00:00")
        assert store.get_meta("feed_state_imported_at") == "2026-10-04T12:00:00+00:00"
