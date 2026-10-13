#!/usr/bin/env python3
"""AC1/AC2 真库只读复查脚本(task 10-14-wechat-chat-export;复查员直跑)。

**严格只读**:mode=ro 连接;不建索引(ensure_page_index 不调)、不落普查
缓存(scan_conversations 不调)——索引自举与缓存的真跑归 CLI 集成后验收。

跑法(仓库根):

    .venv/bin/python .trellis/tasks/10-14-wechat-chat-export/research/real_check.py

覆盖:
- AC1 形状:keyset 逐页拼接(desc,批 500)vs 单次 ORDER BY 全量 —— 序列与
  总条数一致;EXPLAIN 查询计划(未建索引时 = SCAN + TEMP B-TREE,即索引自
  举的动机;建索引后应为 SEARCH ... USING [COVERING] INDEX,见单测断言)。
- AC2:census 基件 fixtures/local_type_census.json 与映射表一致性。
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]  # research/ → 本档 → tasks → .trellis → 仓库根
sys.path.insert(0, str(REPO / "plugins" / "wechat-bridge"))

from wechat_bridge.localdb_page import MSG_TYPE_VARIANTS, iter_message_shards, page_rows  # noqa: E402

COPY = Path.home() / "Library/Application Support/MYIA/wechat-localdb/decrypted"
CHAT = "50438708676@chatroom"  # TMS 群真锚(prd「来源与依赖」)


def main() -> int:
    shards, name_maps = iter_message_shards(COPY, CHAT)
    if not shards:
        print("FAIL: 未找到 TMS 群分表(副本缺位?)")
        return 1
    key, (con, shard) = next(iter(shards.items()))
    t0 = time.monotonic()
    got: list[tuple[int, int]] = []
    bound_ts, bound_rowid = 1 << 62, 1 << 62
    pages = 0
    while True:
        rows = page_rows(
            con, shard, name_maps.get(shard.rel, {}), CHAT,
            bound_ts=bound_ts, bound_rowid=bound_rowid,
            ascending=False, limit=500,
        )
        if not rows:
            break
        pages += 1
        got.extend((int(r["ts"]), int(r["seq"])) for r in rows)
        bound_ts, bound_rowid = int(rows[-1]["ts"]), int(rows[-1]["seq"])
    elapsed_ms = (time.monotonic() - t0) * 1000
    for open_con, _ in shards.values():
        open_con.close()

    check = sqlite3.connect(f"file:{COPY/'message/message_0.db'}?mode=ro", uri=True)
    expected = sorted(
        (
            (int(t), int(r))
            for t, r in check.execute(
                f'SELECT create_time, rowid FROM "{shard.table}" '
                f"ORDER BY create_time, rowid"
            )
        ),
        key=lambda x: (x[0], x[1]),
        reverse=True,
    )
    plan = " | ".join(
        str(row[-1])
        for row in check.execute(
            f'EXPLAIN QUERY PLAN SELECT rowid FROM "{shard.table}" '
            f'WHERE create_time > 0 ORDER BY create_time, rowid LIMIT 1'
        )
    )
    check.close()

    print(f"shard={key} rows={len(got)} pages={pages} elapsed={elapsed_ms:.0f}ms")
    print(f"keyset_sequence_equal={got == expected}")
    print(f"explain_plan(no index yet)={plan}")
    ok = got == expected

    fixture = json.loads(
        (REPO / "tests/wechat-bridge/fixtures/local_type_census.json").read_text()
    )
    mismatches = [
        raw for raw, spec in fixture["mapping"]["census_extensions"].items()
        if MSG_TYPE_VARIANTS.get(int(raw)) != spec["name"]
    ]
    print(f"census_mapping_consistent={not mismatches} (mismatches={mismatches})")
    ok = ok and not mismatches
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
