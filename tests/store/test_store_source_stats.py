"""Tests for SQLiteStore.source_stats(v8 三级界面 1 级类型卡统计底座,
10-09-tg-category-entry)。

store 层验收(协议面 store.source_stats 三态归 test_desktop_sidecar_protocol.py):

- 分组聚合:每源一行 {total, today, unread, latest_first_seen, latest_title};
- today 窗锚:since = 当日窗锚(03:00)语义,窗内计数;since 缺省 = today
  恒 0(「无窗无今日」如实,不猜自然日边界);
- unread = 未标已读(COALESCE(read,0)=0);标读后计数降;
- NULL source 行照出(source: null),归并口径在 UI,store 层不裁剪;
- latest_title = 每源最新一条 title(同刻多行取 id 最大);
- 空库 = 空表(合法应答)。

全部 I/O 走 tmp_path 存储,零真实网络/时钟依赖。
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from myssia.store import ItemRecord, SQLiteStore


@pytest.fixture()
def store(tmp_path):
    """A throwaway SQLiteStore per test (zero shared state between tests)."""
    db = SQLiteStore(tmp_path / "source-stats.db")
    yield db
    db.close()


def _seed(store: SQLiteStore) -> None:
    """7 条夹具:3 条 telegram-demo / 3 条 rss-news / 1 条无源;
    2 条在窗内(since 之后)、5 条在窗外;rss-news 有一条标已读。"""
    window_start = datetime(2026, 10, 10, 3, 0, tzinfo=timezone.utc)
    base = datetime(2026, 10, 9, 0, 0, tzinfo=timezone.utc)
    for index in range(7):
        item = ItemRecord(
            url=f"https://example.com/{index}",
            dedup_key=f"k{index}",
            title=f"条目{index} 最新版",
            source="telegram-demo" if index < 3 else ("rss-news" if index < 6 else None),
            category="proto-demo",
            first_seen=window_start + timedelta(hours=index) if index < 2 else base + timedelta(hours=index),
        )
        store.save_item(item)
    # rss-news 第 4 条(index=3)标已读:unread = 2/3
    store.set_item_states(["k3"], "read", True)


def test_source_stats_groups_by_source(store):
    """分组聚合:三行(TG/网站/NULL source),total 分源正确,行形状六键全在。"""
    _seed(store)
    rows = {row["source"]: row for row in store.source_stats()}
    assert set(rows) == {"telegram-demo", "rss-news", None}
    assert rows["telegram-demo"]["total"] == 3
    assert rows["rss-news"]["total"] == 3
    assert rows[None]["total"] == 1
    for row in rows.values():
        assert set(row) == {
            "source", "total", "today", "unread", "latest_first_seen", "latest_title",
        }


def test_source_stats_today_follows_since_anchor(store):
    """today 窗锚:since = 当日窗锚,只计窗内条目;since 缺省 = today 恒 0。"""
    _seed(store)
    window_start = datetime(2026, 10, 10, 3, 0, tzinfo=timezone.utc)
    rows = {row["source"]: row for row in store.source_stats(since=window_start)}
    # 夹具 index 0/1 在窗内且都归 telegram-demo(index<3)
    assert rows["telegram-demo"]["today"] == 2
    assert rows["rss-news"]["today"] == 0
    assert rows[None]["today"] == 0
    # 省略 since:today 全 0(无窗无今日,不猜自然日)
    for row in store.source_stats():
        assert row["today"] == 0


def test_source_stats_unread_counts_unmarked(store):
    """unread = 未标已读:k3 标读后 rss-news 未读 = 2(总 3);today 与读态无关。"""
    _seed(store)
    rows = {row["source"]: row for row in store.source_stats()}
    assert rows["rss-news"]["unread"] == 2
    assert rows["telegram-demo"]["unread"] == 3
    assert rows[None]["unread"] == 1


def test_source_stats_latest_title_is_newest_per_source(store):
    """latest_title = 每源最新一条 title(同刻多行取 id 最大,ORDER BY id DESC);
    latest_first_seen = MAX(first_seen);行序按最新入库源在前。"""
    window_start = datetime(2026, 10, 10, 3, 0, tzinfo=timezone.utc)
    store.save_item(ItemRecord(
        url="https://a.example/old", dedup_key="a-old", title="A 旧",
        source="src-a", first_seen=window_start - timedelta(hours=5),
    ))
    store.save_item(ItemRecord(
        url="https://a.example/new", dedup_key="a-new", title="A 新",
        source="src-a", first_seen=window_start,
    ))
    store.save_item(ItemRecord(
        url="https://b.example/x", dedup_key="b-x", title="B 唯一",
        source="src-b", first_seen=window_start - timedelta(hours=1),
    ))
    rows = store.source_stats()
    assert [row["source"] for row in rows] == ["src-a", "src-b"]  # 最新在前
    by_source = {row["source"]: row for row in rows}
    assert by_source["src-a"]["latest_title"] == "A 新"
    assert by_source["src-a"]["latest_first_seen"] is not None
    assert by_source["src-b"]["latest_title"] == "B 唯一"
    # 同刻两条:取 id 最大(后入库)
    same = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
    store.save_item(ItemRecord(
        url="https://c.example/1", dedup_key="c-1", title="C 先",
        source="src-c", first_seen=same,
    ))
    store.save_item(ItemRecord(
        url="https://c.example/2", dedup_key="c-2", title="C 后",
        source="src-c", first_seen=same,
    ))
    rows = {row["source"]: row for row in store.source_stats()}
    assert rows["src-c"]["latest_title"] == "C 后"


def test_source_stats_empty_store_zero_rows(store):
    """空库 = 空表(零行不炸,协议面 rows: [] 合法应答)。"""
    assert store.source_stats() == []
