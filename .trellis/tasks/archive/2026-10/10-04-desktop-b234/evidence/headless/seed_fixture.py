"""B234 无头冒烟夹具种子(真 SQLiteStore 写入,镜像 tests/test_desktop_sidecar_protocol.py
:2016 runs.trend / :3219 _seed_feedback_db / :3304 store.trend 的种子法)。

夹具 home = /tmp/myia-b234-e2e/home(MYIA_HOME 隔离;plugins/ai-news.yaml 已拷入):
  - myia.db(serve 上下文缺省 db = <home>/myia.db)
  - items:10 天前 7 条 + 3 天前 3 条 + 今天 5 条(其中 dedup_key=b234-smoke-key-1
    为 B2 反馈目标)→ B4 采集量趋势 14 天窗 = [0,0,0,7,0,0,0,0,0,0,3,0,0,5](峰值 7 共 15)
  - runs(category=ai-news):今天 success3+failed1+running1;昨天 success1+running1;
    3 天前 failed2;40 天前 partial1(14 天窗外、90 天窗内)
    → G6 成功率序列 = [d-3: 0/2=0, d-1: 1/1=1, d0: 3/4=0.75](零完结日不入线)
    → 累计 4/7≈57%;「近期 run 成功率」卡(runs.list 内存合并口径)= 4/10=40%
  - feedback:既有 CLI 行 good×1(14 天窗内)→ B2 标记后 stats good=2
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, "/Users/zhengbingjin/Project/Github/MYIA/src")

from myia.store.models import FEEDBACK_CHANNEL_CLI, FeedbackRecord, ItemRecord  # noqa: E402
from myia.store.sqlite import SQLiteStore  # noqa: E402

HOME = Path("/tmp/myia-b234-e2e/home")
DB = HOME / "myia.db"
CATEGORY = "ai-news"
now = datetime.now(timezone.utc)

store = SQLiteStore(str(DB))


def item(n: int, seen: datetime, key: str | None = None) -> ItemRecord:
    return ItemRecord(
        url=f"https://example.com/b234/{seen.date().isoformat()}/{n}",
        dedup_key=key or f"b234-key-{seen.date().isoformat()}-{n}",
        title=f"B234 冒烟条目 {seen.date().isoformat()} #{n}",
        source="b234-smoke",
        category=CATEGORY,
        first_seen=seen,
    )


def backdate(run_id: int, started: datetime, finished: datetime | None = None) -> None:
    if finished is not None:
        store.conn.execute(
            "UPDATE runs SET started_at = ?, finished_at = ? WHERE id = ?",
            (started.isoformat(), finished.isoformat(), run_id),
        )
    else:
        store.conn.execute(
            "UPDATE runs SET started_at = ? WHERE id = ?", (started.isoformat(), run_id)
        )
    store.conn.commit()


def run_day(day_offset: int, status: str, count: int) -> None:
    for n in range(count):
        started = now - timedelta(days=day_offset, minutes=n)
        rid = store.start_run(CATEGORY)
        if status == "running":
            backdate(rid, started)  # 只 start 不 finish = running 行
        else:
            store.finish_run(rid, status=status)
            backdate(rid, started, started + timedelta(seconds=30))


# items:10 天前 7 + 3 天前 3 + 今天 5(目标条目最后存,id 最大排最前)
for n in range(7):
    store.save_item(item(n, now - timedelta(days=10)))
for n in range(3):
    store.save_item(item(n, now - timedelta(days=3)))
for n in range(4):
    store.save_item(item(n, now))
store.save_item(ItemRecord(
    url="https://example.com/b234/target", dedup_key="b234-smoke-key-1",
    title="B234 冒烟反馈条目", source="b234-smoke", category=CATEGORY, first_seen=now,
))

# runs:今天 3s+1f+1r / 昨天 1s+1r / 3 天前 2f / 40 天前 1p(窗外)
run_day(0, "success", 3)
run_day(0, "failed", 1)
run_day(0, "running", 1)
run_day(1, "success", 1)
run_day(1, "running", 1)
run_day(3, "failed", 2)
run_day(40, "partial", 1)

# 既有 CLI 反馈行(14 天窗内,good)—— B2 标记后的对照面
store.save_feedback(FeedbackRecord(
    dedup_key="b234-cli-old", verdict="good", channel=FEEDBACK_CHANNEL_CLI,
    item_id=None, title="旧 CLI 条", category=None, created_at=now - timedelta(days=2),
))

summary = {
    "db": str(DB),
    "now_utc": now.isoformat(),
    "today": now.date().isoformat(),
    "yesterday": (now - timedelta(days=1)).date().isoformat(),
    "d3": (now - timedelta(days=3)).date().isoformat(),
    "d10": (now - timedelta(days=10)).date().isoformat(),
    "d40": (now - timedelta(days=40)).date().isoformat(),
    "items": {"d10": 7, "d3": 3, "today": 5, "target_dedup_key": "b234-smoke-key-1"},
    "runs": {
        "today": {"success": 3, "failed": 1, "running": 1},
        "yesterday": {"success": 1, "running": 1},
        "d3": {"failed": 2},
        "d40": {"partial": 1},
    },
    "feedback_cli_rows": 1,
    # 期望值(驱动侧对算用):
    "expected": {
        "trend_counts_14d": [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 3, 0, 0, 5],
        "trend_total_text_14d": "近 14 天共 15 条 · 峰值 7 条/日",
        "trend_counts_7d": [0, 0, 0, 3, 0, 0, 5],
        "trend_total_text_7d": "近 7 天共 8 条 · 峰值 5 条/日",
        "rate_points_14d": [0.0, 1.0, 0.75],
        "rate_summary_14d": "近 14 天累计成功率 57%(4/7 次成功)",
        "rate_summary_7d": "近 7 天累计成功率 57%(4/7 次成功)",
        "run_success_rate_card": "40%",
    },
}
store.close()
print(json.dumps(summary, ensure_ascii=False, indent=2))
