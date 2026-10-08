"""Tests for SQLiteStore.count_items(F2 计数口径根治,10-09-tg-category-entry).

store 层验收(协议面 with_total 三态归 test_desktop_sidecar_protocol.py):

- 同 WHERE:count_items 与 list_items 经同一 _items_filter_sql 构造,过滤
  参数(category/source/source_kind/since/游标/query)逐键同口径 ——
  count == len(list_items(同参, 无 limit)) 是本批的不变式;
- 不分页:limit 不在 count_items 参数面,total 恒为全量行数;
- 校验同门:category/source 空串、source_kind 词表外、before_id 单传,
  ValueError 与 list_items 同文。

全部 I/O 走 tmp_path 存储,零真实网络/时钟依赖。
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from myssia.store import ItemRecord, SQLiteStore


@pytest.fixture()
def store(tmp_path):
    """A throwaway SQLiteStore per test (zero shared state between tests)."""
    db = SQLiteStore(tmp_path / "count-items.db")
    yield db
    db.close()


def _seed(store: SQLiteStore) -> None:
    """7 条夹具:3 条 telegram-demo(im)/ 3 条 rss-news(web)/ 1 条无源;
    first_seen 逐条错开 1 小时(query/LIKE 用例可辨)。"""
    base = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)
    for index in range(7):
        store.save_item(
            ItemRecord(
                url=f"https://example.com/{index}",
                dedup_key=f"k{index}",
                title=f"条目{index} 版本 1.0.{index}",
                source="telegram-demo" if index < 3 else ("rss-news" if index < 6 else None),
                category="proto-demo" if index % 2 == 0 else "other",
                first_seen=base + timedelta(hours=index),
            )
        )


def test_count_items_matches_list_items_without_limit(store):
    """同 WHERE 不变式:全量/各过滤组合下 count == len(list_items(无 limit))。"""
    _seed(store)
    combos: list[dict] = [
        {},
        {"category": "proto-demo"},
        {"source": "telegram-demo"},
        {"source_kind": "im"},
        {"source_kind": "web"},
        {"query": "版本"},
        {"since": datetime(2026, 10, 1, 15, tzinfo=timezone.utc)},
    ]
    for kwargs in combos:
        assert store.count_items(**kwargs) == len(store.list_items(limit=None, **kwargs)), kwargs


def test_count_items_ignores_nothing_has_no_limit(store):
    """不分页:limit 不在参数面;7 条夹具全量 = 7。"""
    _seed(store)
    assert store.count_items() == 7
    assert store.count_items(source_kind="im") == 3


def test_count_items_cursor_semantics_subset(store):
    """游标键原样接受:带复合游标 = 「该页之后的余量」口径(过滤条件的一部分)。"""
    _seed(store)
    items = store.list_items(limit=3)  # 新→旧前 3 条
    oldest = items[-1]
    remaining_list = store.list_items(before=oldest.first_seen, before_id=oldest.id)
    assert store.count_items(before=oldest.first_seen, before_id=oldest.id) == len(remaining_list) == 4


def test_count_items_validation_same_gate_as_list_items(store):
    """校验同门:空 category/source、词表外 source_kind、before_id 单传 ——
    ValueError 与 list_items 同规矩(空库语义不猜)。"""
    _seed(store)
    with pytest.raises(ValueError):
        store.count_items(category="")
    with pytest.raises(ValueError):
        store.count_items(source="")
    with pytest.raises(ValueError):
        store.count_items(source_kind="sms")
    with pytest.raises(ValueError):
        store.count_items(before_id=5)
    with pytest.raises(ValueError):
        store.count_items(query=None, before_id=5, before=None)


def test_count_items_empty_store_zero(store):
    """空库 = 0(零行不炸,协议面 total: 0 合法应答)。"""
    assert store.count_items() == 0
