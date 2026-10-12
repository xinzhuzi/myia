"""推送槽位防重按渠道分键(10-12-push-slot-per-channel)。

主人报障实证:news.yaml 双通道(feishu_card + telegram)下,#88 轮日志
20 条「摘要同槽位拦截 channel=telegram」——旧键=条目级不含渠道,先发通道
把后发通道全拦,双通道配置实际只出第一通道摘要。本文件钉死新语义:
(channel, key) 二元组键,同条目 A 通道发过不拦 B 通道;同通道同槽仍拦、
跨槽放行语义不变。(独立文件:test_store_dedup.py 属并行在途面,不碰。)
"""

from __future__ import annotations

from datetime import datetime

from myssia.dedup import DedupRegistry
from myssia.store import SQLiteStore


def test_slot_suppression_is_per_channel(tmp_path):
    store = SQLiteStore(tmp_path / "d.db")
    registry = DedupRegistry(store)
    now = datetime(2026, 10, 12, 15, 0)

    registry.record_push("https://example.com/a", now=now, channel="feishu_card")
    assert registry.should_send("https://example.com/a", now=now, channel="feishu_card") is False
    assert registry.should_send("https://example.com/a", now=now, channel="telegram") is True
    registry.record_push("https://example.com/a", now=now, channel="telegram")
    assert registry.should_send("https://example.com/a", now=now, channel="telegram") is False
    # 跨槽(次日 AM)放行
    assert (
        registry.should_send(
            "https://example.com/a", now=datetime(2026, 10, 13, 9, 0), channel="feishu_card"
        )
        is True
    )
    # 裸键空间不受渠道键影响(doctor/debug 内仍旧语义)
    assert registry.should_send("https://example.com/a", now=now) is True
    store.close()
