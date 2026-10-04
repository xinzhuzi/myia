"""Cron job 生命周期(tests 冻结命名,10-04-hermes-cron implement A4)。

一个文件收拢 :class:`myia.cron.jobs.CronJobs` 的测试面:

- CRUD:create 全字段面(design §2.1;category 绝对路径 Q5、once→repeat 1、
  paused reason、可选键仅显式持久化)、get/resolve(id/名/重名)、list
  (include_disabled + latest_execution 富化)、update(不可变 id、schedule
  变更重算 + repeat 重推导、终态复活拒绝、pending_slot 丢弃);
- 生命周期:pause/resume(跨槽保留 due、过期 once 拒收)/trigger(复活
  paused + manual_run_at 字符串精确标记 + 计入 repeat,§8.1)/rearm_oneshot
  /remove(output 目录保留,design §4.1);
- 运行记账:mark_job_run 四态(ok/failed/delivery_failed/显式覆写
  skipped_busy)、failure_streak 语义、expected_fire_owner 过期回据丢弃、
  repeat 到限退役为**留存**终态、recurring 算不出 next→state=error 不静默
  停摆(#16265)、_advance_after_run 锚 run 完成时刻(§8.1);
- 终态留存清扫:7 天后由到期扫描修剪、可覆写/禁用、无可解析 last_run_at
  的记录保留;
- claim_dispatch(有限 one-shot 预认领、楔死移除+诊断)/ claim_job_for_fire
  (令牌、TTL 内互斥、force 复活、occurrence 去重、manual 无射点身份)+
  心跳认领族;
- advance_next_runs 批量推进;
- 心跳标记族(ticker_heartbeat/last_success/last_error/catch_up 计数、
  writer 存活)与 estop marker(paused.marker,grill Q4);
- 到期扫描:积压坍缩只补一发(#33315)、半暂停自愈、缺失 next_run_at 恢复、
  completed occurrence 去重、过期 one-shot 退役+诊断、run_claim 跨进程守卫、
  manual 标记绕守卫、pending_slot 恢复恰一次(#107485)、expr 改写重锚、
  时区迁移 catch-up、逐 job 隔离;
- 在途运行集 register/release;failure_deliver 缺省回落 deliver、显式
  "none" 关闭(§8.1)。

上游对照:`~/.hermes/hermes-agent/cron/jobs.py` 生命周期段(模块 docstring
行号)。控时纪律(ground-truth B16):无 freezegun,一律注入 ``now_fn``
显式 aware datetime;时区显式 ZoneInfo,不依赖机器本地时区。
"""

from __future__ import annotations

import json
import os
import re
import socket
import subprocess
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional
from zoneinfo import ZoneInfo

import pytest

from myia.cron.executions import ExecutionLedger
from myia.cron.jobs import (
    COMPLETED_ONESHOT_RETENTION_DAYS,
    AmbiguousJobReference,
    CronJobs,
    job_running_in_this_process,
    machine_id,
    release_running_job,
    resolve_failure_deliver,
    try_register_running_job,
)

TZ = ZoneInfo("Asia/Shanghai")
BASE = datetime(2026, 10, 4, 9, 0, tzinfo=TZ)  # 周日 09:00,固定控时基准


class Clock:
    """可拨动的注入时钟(now_fn 形态)。"""

    def __init__(self, at: datetime) -> None:
        self.now = at

    def __call__(self) -> datetime:
        return self.now

    def tick(self, **delta: float) -> None:
        self.now = self.now + timedelta(**delta)


@pytest.fixture()
def clock() -> Clock:
    return Clock(BASE)


@pytest.fixture()
def jobs(tmp_path: Path, clock: Clock) -> CronJobs:
    return CronJobs(tmp_path, now_fn=clock)


def make_job(job_id: str, **overrides: Any) -> dict[str, Any]:
    """最小合法 job 记录(design §2.1 字段面的常用子集;直落库用)。"""
    base: dict[str, Any] = {
        "id": job_id,
        "name": f"job {job_id}",
        "category": "plugins/news.yaml",
        "schedule": {"kind": "interval", "minutes": 30, "display": "every 30m"},
        "schedule_display": "every 30m",
        "repeat": {"times": None, "completed": 0},
        "enabled": True,
        "state": "scheduled",
        "paused_at": None,
        "paused_reason": None,
        "next_run_at": None,
        "last_run_at": None,
        "last_status": None,
        "deliver": "local",
        "failure_deliver": None,
    }
    base.update(overrides)
    return base


def seed(jobs_api: CronJobs, *records: dict[str, Any]) -> None:
    """绕过生命周期 API 直落库(模拟手编/遗留 jobs.json)。"""
    with jobs_api.store.jobs_lock():
        jobs_api.store.save_jobs(list(records), replace=True)


def raw_records(jobs_api: CronJobs) -> list[dict[str, Any]]:
    return jobs_api.store.load_jobs()


def raw_of(jobs_api: CronJobs, job_id: str) -> dict[str, Any]:
    return next(j for j in raw_records(jobs_api) if j.get("id") == job_id)


def past_clock(hours: float = 3.0) -> Clock:
    """账本互操作测试用:基准取真实时钟的过去时刻——completed_occurrence 的
    毒行判定比较账本 finished_at(真实时钟)与到期身份(注入时钟),注入时钟
    不许跑到真实时钟之前(Skew)去,否则完成证明会被误判毒行。"""
    return Clock(datetime.now().astimezone() - timedelta(hours=hours))


@pytest.fixture()
def dead_pid() -> int:
    """确定已死且已收尸的 pid(claim 属主死亡判定用)。"""
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    child.kill()
    child.wait()
    return child.pid


# --- create -------------------------------------------------------------------


def test_create_defaults(jobs: CronJobs, tmp_path: Path) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    assert re.fullmatch(r"[0-9a-f]{12}", job["id"])
    # Q5:解析为绝对路径存储。
    assert job["category"] == str(
        (tmp_path.parent / "plugins" / "news.yaml").resolve()
    ) or (Path(job["category"]).is_absolute() and job["category"].endswith("news.yaml"))
    assert job["name"] == "news.yaml"  # 缺省名 = category 文件名
    assert job["schedule"] == {"kind": "interval", "minutes": 5, "display": "every 5m"}
    assert job["schedule_display"] == "every 5m"
    assert job["repeat"] == {"times": None, "completed": 0}
    assert job["enabled"] is True and job["state"] == "scheduled"
    assert job["paused_at"] is None and job["paused_reason"] is None
    assert job["manual_run_at"] is None
    assert job["deliver"] == "local"
    assert job["origin"] is None and job["timezone"] is None
    assert job["next_run_at"] == (BASE + timedelta(minutes=5)).isoformat()
    assert job["last_status"] is None and job["failure_streak"] == 0
    # 可选键仅显式设置才持久化(Hermes 可选键风格)。
    for absent in (
        "failure_deliver",
        "db_path",
        "config_path",
        "run_timeout",
        "dry_run",
    ):
        assert absent not in job


def test_create_once_implies_repeat_one(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 30m")
    assert job["repeat"] == {"times": 1, "completed": 0}
    assert job["schedule"]["kind"] == "once"
    assert job["next_run_at"] == (BASE + timedelta(minutes=30)).isoformat()


def test_create_paused_with_reason(jobs: CronJobs) -> None:
    job = jobs.create_job(
        "plugins/news.yaml", "every 5m", paused=True, paused_reason="待审核"
    )
    assert job["enabled"] is False and job["state"] == "paused"
    assert job["paused_at"] == BASE.isoformat()
    assert job["paused_reason"] == "待审核"
    assert job["next_run_at"] is None  # 暂停 job 不预排


def test_create_paused_default_reason(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", paused=True)
    assert job["paused_reason"] == "Created paused; awaiting operator approval."


@pytest.mark.parametrize(
    "kwargs",
    [
        {"paused": "yes"},
        {"paused": True, "paused_reason": 5},
        {"paused": False, "paused_reason": "x"},
        {"run_timeout": 0},
        {"run_timeout": -5},
        {"timezone": "Mars/Olympus"},
        {"category": "  "},
    ],
)
def test_create_invalid_inputs_raise(jobs: CronJobs, kwargs: dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        jobs.create_job(
            kwargs.pop("category", "plugins/news.yaml"), "every 5m", **kwargs
        )


def test_create_past_oneshot_rejected(jobs: CronJobs) -> None:
    with pytest.raises(ValueError, match="more than 120s in the past"):
        jobs.create_job("plugins/news.yaml", "2020-01-01T00:00:00")


def test_create_invalid_schedule_lists_five_forms(jobs: CronJobs) -> None:
    with pytest.raises(ValueError) as excinfo:
        jobs.create_job("plugins/news.yaml", "banana")
    text = str(excinfo.value)
    for form in ("'30m'", "'in 30m'", "'every monday 9am'", "'0 9 * * *'", "Timestamp"):
        assert form in text


@pytest.mark.parametrize(
    "repeat,expected",
    [
        (None, None),
        ("forever", None),
        ("once", 1),
        ("3", 3),
        (2, 2),
        (0, None),
        (-1, None),
    ],
)
def test_create_repeat_string_forms(
    jobs: CronJobs, repeat: Any, expected: Optional[int]
) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", repeat=repeat)
    assert job["repeat"]["times"] == expected


def test_create_name_explicit_kept_and_default_truncated(jobs: CronJobs) -> None:
    # 显式名原样保留;截断只作用于缺省推导链(§2.1「缺省取文件名截 50」)。
    assert (
        jobs.create_job("plugins/news.yaml", "every 5m", name="早晚情报流")["name"]
        == "早晚情报流"
    )
    assert (
        jobs.create_job("plugins/news.yaml", "every 5m", name="x" * 80)["name"]
        == "x" * 80
    )
    assert (
        jobs.create_job("plugins/" + "y" * 80 + ".yaml", "every 5m")["name"]
        == "y" * 50 + ".yaml"[:50][-50:]
        or len(jobs.create_job("plugins/" + "y" * 80 + ".yaml", "every 5m")["name"])
        == 50
    )


def test_create_optional_keys_persisted_when_set(jobs: CronJobs) -> None:
    job = jobs.create_job(
        "plugins/news.yaml",
        "every 5m",
        failure_deliver="feishu:ops",
        db_path="/data/x/myia.db",
        config_path="/data/pools.yaml",
        run_timeout=120,
        dry_run=True,
        origin={"source": "cli"},
        timezone="UTC",
    )
    assert job["failure_deliver"] == "feishu:ops"
    assert job["db_path"] == "/data/x/myia.db"
    assert job["config_path"] == "/data/pools.yaml"
    assert job["run_timeout"] == 120.0
    assert job["dry_run"] is True
    assert job["origin"] == {"source": "cli"}
    assert job["timezone"] == "UTC"
    # timezone 生效:cron next 按该时区墙钟(09:00 UTC = 17:00 上海)。
    daily = jobs.create_job("plugins/news.yaml", "0 9 * * *", timezone="UTC")
    # BASE 09:00+08 = 01:00 UTC → 当日 09:00 UTC 射点(严格后继)。
    assert daily["next_run_at"] == "2026-10-04T09:00:00+00:00"


# --- get / resolve / list ------------------------------------------------------


def test_get_job_missing_returns_none(jobs: CronJobs) -> None:
    assert jobs.get_job("nope") is None


def test_resolve_by_name_case_insensitive(jobs: CronJobs) -> None:
    created = jobs.create_job("plugins/news.yaml", "every 5m", name="Daily Brief")
    assert jobs.resolve_job_ref("daily brief")["id"] == created["id"]
    assert jobs.resolve_job_ref(created["id"])["id"] == created["id"]
    assert jobs.resolve_job_ref("其他") is None


def test_resolve_ambiguous_name_raises(jobs: CronJobs) -> None:
    jobs.create_job("plugins/news.yaml", "every 5m", name="twin")
    jobs.create_job("plugins/tech.yaml", "every 6m", name="twin")
    with pytest.raises(AmbiguousJobReference, match="ambiguous"):
        jobs.resolve_job_ref("twin")


def test_list_jobs_filter_and_latest_execution(tmp_path: Path, clock: Clock) -> None:
    api = CronJobs(tmp_path, now_fn=clock)
    a = api.create_job("plugins/news.yaml", "every 5m", name="a")
    b = api.create_job("plugins/news.yaml", "every 5m", name="b", paused=True)
    visible = api.list_jobs()
    assert [j["name"] for j in visible] == ["a"]
    assert all(j["latest_execution"] is None for j in visible)
    assert [j["name"] for j in api.list_jobs(include_disabled=True)] == ["a", "b"]
    # 账本富化:一行 completed 执行挂到 latest_execution。
    row = api.ledger.create_execution(a["id"], source="tick")
    api.ledger.mark_execution_running(row["id"])
    api.ledger.finish_execution(row["id"], success=True)
    assert api.list_jobs()[0]["latest_execution"]["id"] == row["id"]


# --- update --------------------------------------------------------------------


def test_update_immutable_id_rejected(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    with pytest.raises(ValueError, match="cannot be updated"):
        jobs.update_job(job["id"], {"id": "evil/../escape"})


def test_update_schedule_recomputes_next_run(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    updated = jobs.update_job(job["id"], {"schedule": "every monday 9am"})
    assert updated["schedule"]["kind"] == "cron"
    assert (
        updated["next_run_at"] == "2026-10-05T09:00:00+08:00"
    )  # 周日 09:00 建 → 下个周一
    assert updated["schedule_display"] == "every monday 9am"
    clock.tick(minutes=90)
    assert jobs.get_due_jobs() == []  # 新排程在周一,当前不 due


def test_update_schedule_kind_flip_rederives_repeat(jobs: CronJobs) -> None:
    once = jobs.create_job("plugins/news.yaml", "in 10m")
    assert once["repeat"]["times"] == 1
    updated = jobs.update_job(once["id"], {"schedule": "every 5m"})
    assert updated["repeat"] == {"times": None, "completed": 0}
    # 反向:recurring → once 得回 times=1。
    back = jobs.update_job(once["id"], {"schedule": "in 30m"})
    assert back["repeat"] == {"times": 1, "completed": 0}


def test_update_schedule_on_paused_job_keeps_next_run_none(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", paused=True)
    updated = jobs.update_job(job["id"], {"schedule": "every 10m"})
    assert updated["state"] == "paused"
    assert updated["next_run_at"] is None


def test_update_pending_slot_dropped_on_schedule_change(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    raw = raw_of(jobs, job["id"])
    raw["pending_slot"] = {
        "scheduled_at": "x",
        "at": BASE.isoformat(),
        "by": machine_id(),
    }
    seed(jobs, raw)
    kept = jobs.update_job(job["id"], {"name": "renamed"})
    assert kept.get("pending_slot") is not None  # 普通字段编辑不丢槽
    dropped = jobs.update_job(job["id"], {"schedule": "every 9m"})
    assert "pending_slot" not in dropped
    assert "pending_slot" not in raw_of(jobs, job["id"])


def test_update_terminal_activation_rejected(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 10m")
    jobs.mark_job_run(job["id"], success=True)  # one-shot 完成 → 终态
    assert raw_of(jobs, job["id"])["state"] == "completed"
    assert (
        jobs.update_job(job["id"], {"name": "still editable"})["name"]
        == "still editable"
    )
    with pytest.raises(ValueError, match="terminal"):
        jobs.update_job(job["id"], {"enabled": True})


def test_update_category_absolute_and_validated(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    updated = jobs.update_job(job["id"], {"category": "plugins/tech.yaml"})
    assert Path(updated["category"]).is_absolute()
    with pytest.raises(ValueError, match="category"):
        jobs.update_job(job["id"], {"category": ""})


def test_update_repeat_preserves_completed(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", repeat=5)
    jobs.mark_job_run(job["id"], success=True)
    updated = jobs.update_job(job["id"], {"repeat": 3})
    assert updated["repeat"] == {"times": 3, "completed": 1}
    assert (
        jobs.update_job(job["id"], {"repeat": {"times": "once"}})["repeat"]["times"]
        == 1
    )


def test_update_run_timeout_and_timezone_validated(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    assert jobs.update_job(job["id"], {"run_timeout": 60})["run_timeout"] == 60.0
    with pytest.raises(ValueError, match="run_timeout"):
        jobs.update_job(job["id"], {"run_timeout": -1})
    with pytest.raises(ValueError, match="IANA"):
        jobs.update_job(job["id"], {"timezone": "Nowhere/Land"})


# --- pause / resume / trigger / rearm / remove ---------------------------------


def test_pause_persists_reason(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    paused = jobs.pause_job(job["id"], reason="维护窗口")
    assert paused["enabled"] is False and paused["state"] == "paused"
    assert paused["paused_reason"] == "维护窗口"
    assert paused["paused_at"] == BASE.isoformat()
    assert jobs.pause_job("missing") is None


def test_resume_future_recomputes_on_lattice(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 30m")
    jobs.pause_job(job["id"])
    resumed = jobs.resume_job(job["id"])
    assert resumed["enabled"] is True and resumed["state"] == "scheduled"
    assert resumed["paused_at"] is None and resumed["paused_reason"] is None
    # 未跨槽:next_run_at 保持原排程(09:30)。
    assert resumed["next_run_at"] == (BASE + timedelta(minutes=30)).isoformat()


def test_resume_elapsed_recurring_keeps_due(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 30m")
    clock.tick(hours=2)  # 跨过射点后暂停→恢复
    jobs.pause_job(job["id"])
    resumed = jobs.resume_job(job["id"])
    # 暂停期间流过的 occurrence 保留为 due(#113603):恢复不静默重锚越过它。
    assert resumed["next_run_at"] == (BASE + timedelta(minutes=30)).isoformat()
    assert [j["id"] for j in jobs.get_due_jobs()] == [job["id"]]


def test_resume_past_oneshot_raises(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 10m")
    clock.tick(hours=1)
    jobs.pause_job(job["id"])
    with pytest.raises(ValueError, match="will never fire"):
        jobs.resume_job(job["id"])


def test_trigger_revives_paused_and_marks_manual(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", paused=True)
    clock.tick(minutes=1)
    triggered = jobs.trigger_job(job["id"])
    assert triggered["enabled"] is True and triggered["state"] == "scheduled"
    assert triggered["paused_at"] is None and triggered["paused_reason"] is None
    # 字符串精确同戳:manual 标记防 TZ 修复守卫误判(§8.1)。
    assert (
        triggered["manual_run_at"]
        == triggered["next_run_at"]
        == (BASE + timedelta(minutes=1)).isoformat()
    )
    due = jobs.get_due_jobs()
    assert [j["id"] for j in due] == [job["id"]]
    assert due[0].get("_scheduled_instant") is None  # 手动跑不带射点身份
    # manual 标记单发:mark 后清除。
    jobs.mark_job_run(job["id"], success=True)
    assert "manual_run_at" not in raw_of(jobs, job["id"])


def test_trigger_terminal_rejected(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    jobs.mark_job_run(job["id"], success=True)
    with pytest.raises(ValueError, match="terminal"):
        jobs.trigger_job(job["id"])


def test_trigger_run_counts_toward_repeat(jobs: CronJobs, clock: Clock) -> None:
    # §8.1:手动 trigger 的 run 计入 repeat.completed。
    job = jobs.create_job("plugins/news.yaml", "every 5m", repeat=2)
    for _ in range(2):
        jobs.trigger_job(job["id"])
        jobs.get_due_jobs()
        assert jobs.mark_job_run(job["id"], success=True) is True
    raw = raw_of(jobs, job["id"])
    assert raw["repeat"] == {"times": 2, "completed": 2}
    assert raw["state"] == "completed" and raw["enabled"] is False


def test_rearm_oneshot_reactivates(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    jobs.mark_job_run(job["id"], success=True)
    clock.tick(minutes=10)
    rearmed = jobs.rearm_oneshot(
        job["id"], (clock.now + timedelta(minutes=20)).isoformat()
    )
    assert rearmed["state"] == "scheduled" and rearmed["enabled"] is True
    assert rearmed["repeat"]["completed"] == 0
    assert rearmed["next_run_at"] == (clock.now + timedelta(minutes=20)).isoformat()


@pytest.mark.parametrize(
    "schedule,match", [("every 5m", "one-shot-only"), ("2020-01-01T00:00:00", "past")]
)
def test_rearm_rejects_recurring_and_past(
    jobs: CronJobs, schedule: str, match: str
) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m" if match == "past" else schedule)
    jobs.mark_job_run(job["id"], success=True) if match == "past" else None
    with pytest.raises(ValueError, match=match):
        jobs.rearm_oneshot(job["id"], schedule)


def test_rearm_over_live_fire_claim_rejected(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    raw["fire_claim"] = {"at": BASE.isoformat(), "by": machine_id()}
    seed(jobs, raw)
    with pytest.raises(ValueError, match="live fire claim"):
        jobs.rearm_oneshot(job["id"], "2030-01-01T00:00:00")


def test_remove_keeps_output_dir(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    out = jobs.store.job_output_dir(job["id"])
    out.mkdir(parents=True, exist_ok=True)
    (out / "run.md").write_text("evidence", encoding="utf-8")
    assert jobs.remove_job(job["name"]) is True  # 名字也行
    assert raw_records(jobs) == []
    assert (out / "run.md").read_text(
        encoding="utf-8"
    ) == "evidence"  # design §4.1:保留
    assert jobs.remove_job(job["id"]) is False


# --- mark_job_run / _advance_after_run ------------------------------------------


def test_mark_job_run_four_states(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    assert raw["last_status"] == "ok" and raw["last_error"] is None
    assert raw["failure_streak"] == 0 and raw["last_run_at"] == clock.now.isoformat()
    jobs.mark_job_run(job["id"], success=False, error="boom")
    raw = raw_of(jobs, job["id"])
    assert raw["last_status"] == "failed" and raw["last_error"] == "boom"
    assert raw["failure_streak"] == 1
    jobs.mark_job_run(job["id"], success=True, delivery_error="feishu 429")
    raw = raw_of(jobs, job["id"])
    # 运行成功投递失败:delivery_failed;delivery 失败不计入连击——该 run 本身
    # 成功,照上游 success 分支清零 streak(H _record_run_outcome 代码为准)。
    assert raw["last_status"] == "delivery_failed"
    assert raw["last_delivery_error"] == "feishu 429"
    assert raw["failure_streak"] == 0
    jobs.mark_job_run(job["id"], success=True, status="skipped_busy")
    assert raw_of(jobs, job["id"])["last_status"] == "skipped_busy"  # 显式覆写(Q2)
    assert jobs.mark_job_run("ghost", success=True) is False


def test_mark_failure_streak_resets_on_success(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    for _ in range(3):
        jobs.mark_job_run(job["id"], success=False, error="x")
    assert raw_of(jobs, job["id"])["failure_streak"] == 3
    jobs.mark_job_run(job["id"], success=True)
    assert raw_of(jobs, job["id"])["failure_streak"] == 0


def test_mark_expected_fire_owner_discards_stale_receipt(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    claimed = jobs.claim_job_for_fire(job["id"])
    assert claimed is True
    owner = raw_of(jobs, job["id"])["fire_claim"]["by"]
    assert (
        jobs.mark_job_run(job["id"], success=True, expected_fire_owner="someone-else")
        is False
    )
    assert raw_of(jobs, job["id"])["last_run_at"] is None  # 回据被丢
    assert jobs.mark_job_run(job["id"], success=True, expected_fire_owner=owner) is True
    assert raw_of(jobs, job["id"])["fire_claim"] is None  # run 结束清认领


def test_repeat_limit_retires_retained_record(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", repeat=2)
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    assert raw["repeat"] == {"times": 2, "completed": 1}
    assert raw["state"] == "scheduled"  # 未到限继续
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    # 到限:终态**留存**(可 inspect),不弹出入库(§8.1)。
    assert raw["state"] == "completed" and raw["enabled"] is False
    assert raw["next_run_at"] is None
    assert raw["last_status"] == "ok"
    assert len(raw_records(jobs)) == 1


def test_mark_clears_claims_and_slot(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    raw = raw_of(jobs, job["id"])
    raw.update(
        fire_claim={"at": BASE.isoformat(), "by": machine_id()},
        pending_slot={"scheduled_at": "x", "at": BASE.isoformat(), "by": machine_id()},
        run_claim={"at": BASE.isoformat(), "by": machine_id()},
    )
    seed(jobs, raw)
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    assert raw["fire_claim"] is None and raw["run_claim"] is None
    assert "pending_slot" not in raw


def test_advance_after_run_anchors_completion_moment(
    jobs: CronJobs, clock: Clock
) -> None:
    # §8.1 事实裁决:interval 5m 跑 8m → 下次 = 完成时刻 +5m,不立即补发。
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    clock.tick(minutes=5)
    jobs.get_due_jobs()
    clock.tick(minutes=8)  # run 耗时 8 分钟
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    assert raw["last_run_at"] == clock.now.isoformat()
    assert datetime.fromisoformat(raw["next_run_at"]) == clock.now + timedelta(
        minutes=5
    )
    assert jobs.get_due_jobs() == []  # 完成后 5 分钟内不补发


@pytest.mark.parametrize(
    "schedule", [{"kind": "interval"}, {"kind": "cron", "expr": "bad expr !!"}]
)
def test_recurring_compute_failure_marks_error_not_disabled(
    jobs: CronJobs,
    schedule: dict[str, Any],
) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    raw = raw_of(jobs, job["id"])
    raw["schedule"] = schedule  # 手编坏排程
    seed(jobs, raw)
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    # #16265 守卫:绝不静默停摆——state=error 且保持 enabled。
    assert raw["state"] == "error" and raw["enabled"] is True
    assert raw["next_run_at"] is None
    assert raw["last_error"] and "recurring" in raw["last_error"]


def test_oneshot_without_next_run_completes(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    assert raw["state"] == "completed" and raw["repeat"]["completed"] == 1


# --- 终态留存清扫 ---------------------------------------------------------------


def completed_once(jobs_api: CronJobs, *, days: float, clock_now: datetime) -> str:
    """造一条 days 天前完成的 once 终态记录,返回 id。"""
    job = jobs_api.create_job("plugins/news.yaml", "in 5m")
    jobs_api.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs_api, job["id"])
    raw["last_run_at"] = (clock_now - timedelta(days=days)).isoformat()
    seed(
        jobs_api,
        *[r if r.get("id") != job["id"] else raw for r in raw_records(jobs_api)],
    )
    return job["id"]


def test_retention_sweeps_after_seven_days(jobs: CronJobs, clock: Clock) -> None:
    old = completed_once(jobs, days=8.0, clock_now=clock.now)
    fresh = completed_once(jobs, days=2.0, clock_now=clock.now)
    assert [j["id"] for j in raw_records(jobs)] == [old, fresh]
    jobs.get_due_jobs()  # 清扫挂在到期扫描里(上游同款入口)
    assert [j["id"] for j in raw_records(jobs)] == [fresh]
    # 移除的 id 不被 shrink-merge 复活:同 id 重建落得住。
    jobs.store.save_jobs(raw_records(jobs) + [make_job(old)])
    assert old in {j["id"] for j in raw_records(jobs)}


def test_retention_respects_overridden_window(tmp_path: Path, clock: Clock) -> None:
    api = CronJobs(tmp_path, now_fn=clock, completed_retention_days=1)
    old = completed_once(api, days=2.0, clock_now=clock.now)
    api.get_due_jobs()
    assert [j["id"] for j in raw_records(api)] == [] or old not in {
        j["id"] for j in raw_records(api)
    }


def test_retention_zero_disables_sweep(tmp_path: Path, clock: Clock) -> None:
    api = CronJobs(tmp_path, now_fn=clock, completed_retention_days=0)
    old = completed_once(api, days=90.0, clock_now=clock.now)
    api.get_due_jobs()
    assert old in {j["id"] for j in raw_records(api)}


def test_retention_only_touches_completed_oneshots(
    jobs: CronJobs, clock: Clock
) -> None:
    # recurring 到限退役的终态记录不在清扫面(上游仅扫 state=completed + once)。
    job = jobs.create_job("plugins/news.yaml", "every 5m", repeat=1)
    jobs.mark_job_run(job["id"], success=True)
    raw = raw_of(jobs, job["id"])
    raw["last_run_at"] = (clock.now - timedelta(days=30)).isoformat()
    seed(jobs, raw)
    jobs.get_due_jobs()
    assert job["id"] in {j["id"] for j in raw_records(jobs)}
    # 无可解析 last_run_at 的完成记录保留(绝不猜着删)。
    vague = completed_once(jobs, days=99.0, clock_now=clock.now)
    raw = raw_of(jobs, vague)
    raw["last_run_at"] = "not-a-date"
    seed(jobs, *[r if r.get("id") != vague else raw for r in raw_records(jobs)])
    jobs.get_due_jobs()
    assert vague in {j["id"] for j in raw_records(jobs)}


# --- claim_dispatch(有限 one-shot 预认领)---------------------------------------


def test_claim_dispatch_increments_and_allows(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m", repeat=2)
    assert jobs.claim_dispatch(job["id"]) is True
    assert raw_of(jobs, job["id"])["repeat"]["completed"] == 1
    # 预认领后的 mark 不双计(#38758)。
    jobs.mark_job_run(job["id"], success=True)
    assert raw_of(jobs, job["id"])["repeat"]["completed"] == 1


def test_claim_dispatch_limit_with_prior_run_marks_completed(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m", repeat=1)
    raw = raw_of(jobs, job["id"])
    raw["repeat"]["completed"] = 1  # 模拟已发满
    seed(jobs, raw)
    jobs.mark_job_run(job["id"], success=True)  # 有过真 run(last_run_at 在)
    assert jobs.claim_dispatch(job["id"]) is False
    assert raw_of(jobs, job["id"])["state"] == "completed"
    assert job["id"] in {j["id"] for j in raw_records(jobs)}


def test_claim_dispatch_wedged_removes_with_diagnostic(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m", repeat=1)
    raw = raw_of(jobs, job["id"])
    raw["repeat"]["completed"] = 1  # 派发已认领,mark 没跑成 → 楔死
    seed(jobs, raw)
    assert jobs.claim_dispatch(job["id"]) is False
    assert job["id"] not in {j["id"] for j in raw_records(jobs)}
    outputs = list(jobs.store.job_output_dir(job["id"]).glob("*.md"))
    assert len(outputs) == 1 and "removed without producing output" in outputs[
        0
    ].read_text(encoding="utf-8")


def test_claim_dispatch_recurring_always_true(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", repeat=3)
    assert jobs.claim_dispatch(job["id"]) is True
    assert raw_of(jobs, job["id"])["repeat"]["completed"] == 0  # recurring 不预认领


# --- claim_job_for_fire + 心跳认领 ----------------------------------------------


def test_fire_claim_stamps_token_and_advances_recurring(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    assert jobs.claim_job_for_fire(job["id"]) is True
    raw = raw_of(jobs, job["id"])
    claim = raw["fire_claim"]
    assert (
        claim["by"].startswith(machine_id() + ":") and len(claim["by"].split(":")) == 3
    )
    assert claim["at"] == BASE.isoformat()
    # 认领即推进 recurring:陈旧重投递无法重发。
    assert datetime.fromisoformat(raw["next_run_at"]) == BASE + timedelta(minutes=5)
    assert jobs.claim_job_for_fire(job["id"]) is False  # TTL 内第二认领输


def test_fire_claim_force_resumes_paused(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m", paused=True)
    assert jobs.claim_job_for_fire(job["id"]) is False  # 暂停不让认
    assert jobs.claim_job_for_fire(job["id"], force=True) is True  # force 原子复活
    raw = raw_of(jobs, job["id"])
    assert raw["enabled"] is True and raw["state"] == "scheduled"
    assert raw["paused_at"] is None and raw["paused_reason"] is None


def test_fire_claim_manual_carries_no_instant(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    claimed = jobs.claim_job_for_fire(job["id"], manual=True, return_job=True)
    assert isinstance(claimed, dict)
    assert claimed["_scheduled_instant"] is None  # off-tick 手动不绑未来射点
    assert "fire_claim" in claimed


def test_fire_claim_terminal_loses(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    jobs.mark_job_run(job["id"], success=True)
    assert jobs.claim_job_for_fire(job["id"], force=True) is False


def test_fire_claim_dead_owner_releases_immediately(
    jobs: CronJobs, dead_pid: int
) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    raw = raw_of(jobs, job["id"])
    raw["fire_claim"] = {
        "at": BASE.isoformat(),
        "by": f"{socket.gethostname()}:{dead_pid}",
    }  # 属主已死
    seed(jobs, raw)
    assert jobs.claim_job_for_fire(job["id"]) is True  # 不等满 TTL


def test_fire_claim_foreign_host_claim_stays_live(jobs: CronJobs) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    raw = raw_of(jobs, job["id"])
    raw["fire_claim"] = {"at": BASE.isoformat(), "by": "other-host:123:abc"}
    seed(jobs, raw)
    assert jobs.claim_job_for_fire(job["id"]) is False  # 异机署名证不了死 → 尊重


def test_heartbeat_fire_claim_owner_scoped(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    jobs.claim_job_for_fire(job["id"])
    owner = raw_of(jobs, job["id"])["fire_claim"]["by"]
    assert jobs.heartbeat_fire_claim(job["id"], expected_owner="not-me") is False
    clock.tick(minutes=2)
    assert jobs.heartbeat_fire_claim(job["id"], expected_owner=owner) is True
    assert raw_of(jobs, job["id"])["fire_claim"]["at"] == clock.now.isoformat()


def test_run_claim_heartbeat_and_clear(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    clock.tick(minutes=6)
    jobs.get_due_jobs()  # due 扫描戳 run_claim
    owner = raw_of(jobs, job["id"])["run_claim"]["by"]
    clock.tick(minutes=2)
    assert jobs.heartbeat_run_claim(job["id"], expected_owner=owner) is True
    assert jobs.heartbeat_run_claim(job["id"], expected_owner="other") is False
    assert jobs.clear_run_claim(job["id"]) is True
    assert raw_of(jobs, job["id"])["run_claim"] is None
    assert jobs.clear_run_claim(job["id"]) is False  # 已清


# --- advance_next_runs -----------------------------------------------------------


def test_advance_next_runs_batch(jobs: CronJobs, clock: Clock) -> None:
    a = jobs.create_job("plugins/news.yaml", "every 5m")
    b = jobs.create_job("plugins/tech.yaml", "every 10m")
    once = jobs.create_job("plugins/life.yaml", "in 30m")
    clock.tick(minutes=6)  # a/b 的射点已过:推进=重锚到 now+周期
    assert jobs.advance_next_runs([a["id"], b["id"], once["id"], "ghost"]) == 2
    assert datetime.fromisoformat(
        raw_of(jobs, a["id"])["next_run_at"]
    ) == clock.now + timedelta(minutes=5)
    assert datetime.fromisoformat(
        raw_of(jobs, b["id"])["next_run_at"]
    ) == clock.now + timedelta(minutes=10)
    assert (
        raw_of(jobs, once["id"])["next_run_at"]
        == (BASE + timedelta(minutes=30)).isoformat()
    )  # once 不动
    assert jobs.advance_next_run(a["id"]) is False  # 幂等:再推进无位移
    assert jobs.advance_next_run("ghost") is False


# --- 心跳标记族 + estop -----------------------------------------------------------


def test_heartbeat_markers_roundtrip(jobs: CronJobs) -> None:
    assert jobs.get_ticker_heartbeat_age() is None  # 缺失 = 不能判定
    assert jobs.get_ticker_success_age() is None
    assert jobs.ticker_heartbeat_writer_alive() is False
    jobs.record_ticker_heartbeat(success=True)
    assert (
        jobs.get_ticker_heartbeat_age() is not None
        and jobs.get_ticker_heartbeat_age() < 5
    )
    assert jobs.get_ticker_success_age() is not None
    assert jobs.ticker_heartbeat_writer_alive() is True  # 本进程写的
    # 内容形态:<epoch> <pid>(cron status 消费)。
    fields = (
        (jobs.store.cron_dir / "ticker_heartbeat").read_text(encoding="utf-8").split()
    )
    assert len(fields) == 2 and int(fields[1]) == os.getpid()


def test_heartbeat_writer_dead_pid_not_alive(jobs: CronJobs, dead_pid: int) -> None:
    jobs.store.ensure_dirs()
    (jobs.store.cron_dir / "ticker_heartbeat").write_text(
        f"1700000000 {dead_pid}", encoding="utf-8"
    )
    assert jobs.ticker_heartbeat_writer_alive() is False


def test_ticker_error_marker_lifecycle(jobs: CronJobs) -> None:
    assert jobs.get_ticker_last_error() is None
    jobs.record_ticker_error("tick blew up\n细节")
    assert "tick blew up" in (jobs.get_ticker_last_error() or "")
    jobs.clear_ticker_error()
    assert jobs.get_ticker_last_error() is None


def test_catch_up_counter(jobs: CronJobs) -> None:
    assert jobs.get_catch_up_occurrence_count() == 0
    jobs.record_catch_up_occurrence()
    jobs.record_catch_up_occurrence()
    assert jobs.get_catch_up_occurrence_count() == 2


def test_estop_marker_lifecycle(jobs: CronJobs) -> None:
    assert jobs.is_estopped() is False
    jobs.engage_estop("升级维护")
    assert jobs.is_estopped() is True
    payload = json.loads(jobs.estop_marker.read_text(encoding="utf-8"))
    assert payload["reason"] == "升级维护" and payload["engaged_at"]
    assert jobs.disengage_estop() is True
    assert jobs.is_estopped() is False and not jobs.estop_marker.exists()


def test_estop_corrupt_marker_still_engaged_and_stat_fails_safe(
    jobs: CronJobs, monkeypatch: Any
) -> None:
    jobs.store.cron_dir.mkdir(parents=True, exist_ok=True)
    jobs.estop_marker.write_text("", encoding="utf-8")  # 空文件 = 踩下(fail-safe)
    assert jobs.is_estopped() is True

    def boom(self: Path) -> bool:
        raise OSError("stat failed")

    monkeypatch.setattr(Path, "exists", boom)
    assert jobs.is_estopped() is True  # stat 失败同样 fail-safe 按踩下


# --- 在途运行集 ------------------------------------------------------------------


def test_running_set_register_release_dedupe() -> None:
    jid = f"job-{uuid.uuid4().hex[:6]}"
    assert try_register_running_job(jid) is True
    assert try_register_running_job(jid) is False  # 在途去重
    assert job_running_in_this_process(jid) is True
    release_running_job(jid)
    assert job_running_in_this_process(jid) is False
    release_running_job(jid)  # 幂等
    assert try_register_running_job(jid) is True
    release_running_job(jid)


# --- failure_deliver 回落(§8.1)---------------------------------------------------


def test_resolve_failure_deliver_fallback_and_none() -> None:
    # 缺省(键缺席)→ 回落 deliver。
    assert resolve_failure_deliver({"deliver": "feishu:ops"}) == "feishu:ops"
    # 显式 "none" → 关闭。
    assert (
        resolve_failure_deliver({"deliver": "feishu:ops", "failure_deliver": "none"})
        is None
    )
    # 显式目标 → 原样;deliver=local 时回落即 local(本地落盘是有效去向)。
    assert (
        resolve_failure_deliver({"deliver": "local", "failure_deliver": "telegram:1"})
        == "telegram:1"
    )
    assert resolve_failure_deliver({"deliver": "local"}) == "local"


# --- 到期扫描 ---------------------------------------------------------------------


def test_due_scan_future_not_due(jobs: CronJobs, clock: Clock) -> None:
    jobs.create_job("plugins/news.yaml", "every 5m")
    clock.tick(minutes=4)
    assert jobs.get_due_jobs() == []
    clock.tick(minutes=2)
    assert len(jobs.get_due_jobs()) == 1


def test_due_scan_backlog_collapses_and_fires_once(
    jobs: CronJobs, clock: Clock
) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    clock.tick(hours=3)  # 积压 36 个周期
    due = jobs.get_due_jobs()
    assert [j["id"] for j in due] == [job["id"]]  # 坍缩只补一发(#33315)
    raw = raw_of(jobs, job["id"])
    assert (
        datetime.fromisoformat(raw["next_run_at"]) > clock.now
    )  # fast-forward 已持久化
    assert raw["last_dispatch"]["kind"] == "catch_up"
    assert jobs.get_catch_up_occurrence_count() == 1
    # pending_slot 戳带上被消费的精确射点(恢复窗口凭证,#107485)。
    assert (
        raw["pending_slot"]["scheduled_at"] == (BASE + timedelta(minutes=5)).isoformat()
    )
    assert raw["pending_slot"]["by"] == machine_id()
    # 快照携带 UTC 规范化的射点身份(runner 消费)。
    assert due[0]["_scheduled_instant"] == "2026-10-04T01:05:00+00:00"


def test_due_scan_skips_disabled_paused_terminal(jobs: CronJobs) -> None:
    disabled = make_job("d1", enabled=False)
    paused = make_job("p1", enabled=True, state="paused", paused_at=BASE.isoformat())
    terminal = make_job("t1", enabled=False, state="completed", next_run_at=None)
    recoverable = make_job(
        "r1",
        state="error",
        enabled=True,
        schedule={"kind": "interval", "minutes": 5},
        next_run_at=(BASE - timedelta(minutes=1)).isoformat(),
    )
    seed(jobs, disabled, paused, terminal, recoverable)
    due = jobs.get_due_jobs()
    assert [j["id"] for j in due] == ["r1"]  # 可恢复 error job 照常参与
    # 射点在场时不走恢复路径,state=error 保持到下一次 mark(run 成功才回 scheduled)。
    assert raw_of(jobs, "r1")["state"] == "error"
    jobs.mark_job_run("r1", success=True)
    assert raw_of(jobs, "r1")["state"] == "scheduled"


def test_due_scan_half_paused_self_disables(jobs: CronJobs, caplog: Any) -> None:
    job = make_job(
        "hp1", enabled=True, paused_at=BASE.isoformat(), next_run_at=BASE.isoformat()
    )
    seed(jobs, job)
    with caplog.at_level("ERROR", logger="myia.cron.jobs"):
        assert jobs.get_due_jobs() == []
    raw = raw_of(jobs, "hp1")
    assert raw["enabled"] is False and raw["state"] == "paused"
    assert "auto-disabled" in raw["paused_reason"]
    assert any("pause markers while enabled" in r.message for r in caplog.records)


def test_due_scan_recovers_missing_next_run(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    raw = raw_of(jobs, job["id"])
    raw.pop("next_run_at")
    seed(jobs, raw)
    clock.tick(minutes=10)
    # 恢复=重挂未来射点(interval 锚 now → now+5m),不是立即补发(上游同款)。
    assert jobs.get_due_jobs() == []
    assert datetime.fromisoformat(
        raw_of(jobs, job["id"])["next_run_at"]
    ) == clock.now + timedelta(minutes=5)
    clock.tick(minutes=6)
    assert [j["id"] for j in jobs.get_due_jobs()] == [job["id"]]
    jobs.mark_job_run(job["id"], success=True)  # 消费掉该 fire 的 pending_slot
    # 非法 ISO 的 next_run_at 被规整弹掉后同样走恢复路径。
    raw = raw_of(jobs, job["id"])
    raw["next_run_at"] = "garbage"
    seed(jobs, raw)
    clock.tick(minutes=12)
    assert jobs.get_due_jobs() == []
    clock.tick(minutes=5)
    assert [j["id"] for j in jobs.get_due_jobs()] == [job["id"]]


def test_due_scan_completed_occurrence_dedup(tmp_path: Path) -> None:
    # 账本互操作:注入时钟取真实过去,防毒行误判(见 past_clock 注释)。
    clock = past_clock()
    api = CronJobs(tmp_path, now_fn=clock)
    job = api.create_job("plugins/news.yaml", "every 5m")
    instant = job["next_run_at"]
    row = api.ledger.create_execution(
        job["id"], source="tick", scheduled_instant=instant
    )
    api.ledger.finish_execution(row["id"], success=True)
    clock.tick(minutes=6)
    assert api.get_due_jobs() == []  # 该 occurrence 已有完成执行 → 跳过
    # recurring 已被推进到新射点。
    assert datetime.fromisoformat(raw_of(api, job["id"])["next_run_at"]) > clock.now


def test_due_scan_retires_expired_oneshot_with_diagnostic(
    jobs: CronJobs, clock: Clock
) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    clock.tick(hours=1)  # grace(120s)之外
    assert jobs.get_due_jobs() == []
    assert job["id"] not in {j["id"] for j in raw_records(jobs)}  # 退役移除
    outputs = list(jobs.store.job_output_dir(job["id"]).glob("*.md"))
    assert len(outputs) == 1 and "outside grace window" in outputs[0].read_text(
        encoding="utf-8"
    )


def test_due_scan_oneshot_with_live_claim_skips_but_keeps(
    jobs: CronJobs, clock: Clock
) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m")
    clock.tick(hours=1)
    raw = raw_of(jobs, job["id"])
    raw["run_claim"] = {
        "at": clock.now.isoformat(),
        "by": machine_id(),
    }  # run 可能仍在跑
    seed(jobs, raw)
    assert jobs.get_due_jobs() == []
    assert job["id"] in {j["id"] for j in raw_records(jobs)}  # 记录保留等 mark 落地


def test_due_scan_oneshot_dispatch_limit_removes(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "in 5m", repeat=1)
    clock.tick(minutes=6)
    jobs.get_due_jobs()  # 戳 run_claim + 派发窗口
    # 模拟:claim_dispatch 已预认领(completed=1)、tick 死了、mark 没跑成。
    assert raw_of(jobs, job["id"])["repeat"]["completed"] == 0  # due 扫描本身不预认领
    raw = raw_of(jobs, job["id"])
    raw["repeat"]["completed"] = 1
    raw.pop("run_claim", None)
    seed(jobs, raw)
    clock.tick(minutes=1)
    assert jobs.get_due_jobs() == []
    assert job["id"] not in {j["id"] for j in raw_records(jobs)}


def test_due_scan_pending_slot_restored_once(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    slot = (BASE + timedelta(minutes=5)).isoformat()
    clock.tick(minutes=6)
    jobs.get_due_jobs()  # 正常发掉这个槽
    jobs.mark_job_run(job["id"], success=True)
    # 造一个「推进已做、认领未取」的崩溃凭证:属主=本机、job 不在本进程跑。
    raw = raw_of(jobs, job["id"])
    stale_slot = (clock.now + timedelta(minutes=5)).isoformat()
    raw["next_run_at"] = (clock.now + timedelta(hours=1)).isoformat()  # 已被推进到远处
    raw["pending_slot"] = {
        "scheduled_at": stale_slot,
        "at": clock.now.isoformat(),
        "by": machine_id(),
    }
    seed(jobs, raw)
    clock.tick(minutes=30)  # 槽已过期,推进到的远处还没到
    due = jobs.get_due_jobs()
    assert [j["id"] for j in due] == [job["id"]]  # 恰恢复一次(旧戳被消费)
    raw = raw_of(jobs, job["id"])
    # 恢复即清旧戳;本次 fire 照常盖**新** pending_slot(其 scheduled_at=刚恢复的槽)。
    assert raw["pending_slot"]["scheduled_at"] == stale_slot


def test_due_scan_expr_edit_reanchors_without_firing(
    jobs: CronJobs, clock: Clock
) -> None:
    job = jobs.create_job("plugins/news.yaml", "0 9 * * *")  # 每天 09:00
    clock.tick(hours=10)  # 19:00
    jobs.mark_job_run(job["id"], success=True)  # 下射点=明 09:00(在旧栅格)
    # 手编 expr → 10:00;存储 next_run_at 改成已到期但离新栅格的 10:30。
    raw = raw_of(jobs, job["id"])
    raw["schedule"] = {"kind": "cron", "expr": "0 10 * * *", "display": "0 10 * * *"}
    raw["next_run_at"] = "2026-10-04T10:30:00+08:00"
    seed(jobs, raw)
    assert jobs.get_due_jobs() == []  # 离栅 → 重锚不发(#93049)
    raw = raw_of(jobs, job["id"])
    assert datetime.fromisoformat(raw["next_run_at"]).strftime("%H:%M") == "10:00"
    assert datetime.fromisoformat(raw["next_run_at"]).date().isoformat() == "2026-10-05"


def test_due_scan_timezone_migration_fires(
    jobs: CronJobs, clock: Clock, caplog: Any
) -> None:
    # 存储射点带迁移前偏移(UTC),其自身墙钟(09:00)在 expr 栅格上;规整到
    # 上海(+08)后是 17:00,离栅——判 timezone_migration 而非 expr_edit,发。
    raw = make_job(
        "m1",
        schedule={"kind": "cron", "expr": "0 9 * * *", "display": "0 9 * * *"},
        next_run_at="2026-10-04T09:00:00+00:00",
    )
    seed(jobs, raw)
    clock.now = datetime(2026, 10, 4, 18, 0, tzinfo=TZ)  # 17:00+08 已过 → due
    with caplog.at_level("WARNING", logger="myia.cron.jobs"):
        due = jobs.get_due_jobs()
    assert [j["id"] for j in due] == ["m1"]
    assert any("timezone_migration" in r.message for r in caplog.records)


def test_due_scan_repairs_future_timezone_shift(jobs: CronJobs, clock: Clock) -> None:
    # 存储射点带大偏移:绝对时刻已到(10:30+08 ≤ now 12:00)但自身墙钟(13:30)
    # 还在未来 → 时区漂移守卫重锚到本地意图(下一 09:00)、本 tick 不发。
    clock.now = datetime(2026, 10, 4, 12, 0, tzinfo=TZ)
    raw = make_job(
        "tz1",
        schedule={"kind": "cron", "expr": "0 9 * * *", "display": "0 9 * * *"},
        next_run_at="2026-10-04T13:30:00+13:00",
    )
    seed(jobs, raw)
    assert jobs.get_due_jobs() == []
    assert raw_of(jobs, "tz1")["next_run_at"] == "2026-10-05T09:00:00+08:00"


def test_due_scan_stale_failed_recurring_rearms(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    clock.tick(minutes=5)
    jobs.get_due_jobs()
    jobs.mark_job_run(job["id"], success=False, error="x")  # failed,被停到下周期
    # 楔住:next_run_at 在未来、last_status=failed 挂满一个 cadence+grace。
    clock.tick(minutes=30)
    due = jobs.get_due_jobs()
    assert [j["id"] for j in due] == [job["id"]]  # 重挂回 now 附近而非干等


def test_due_scan_isolates_malformed_job(jobs: CronJobs, monkeypatch: Any) -> None:
    healthy = jobs.create_job("plugins/news.yaml", "every 5m")
    poison = make_job("poison")
    seed(jobs, *raw_records(jobs), poison)
    clock_now = BASE + timedelta(minutes=6)

    original = CronJobs._evaluate_due_job

    def raising(self: CronJobs, job: dict[str, Any], scan: Any) -> bool:
        if job.get("id") == "poison":
            raise RuntimeError("future malformed variant")
        return original(self, job, scan)

    monkeypatch.setattr(CronJobs, "_evaluate_due_job", raising)
    jobs._now_fn = lambda: clock_now  # type: ignore[assignment]
    due = jobs.get_due_jobs()
    assert [j["id"] for j in due] == [healthy["id"]]  # 姐妹照常跑
    jobs._now_fn = None


def test_due_scan_triggers_manual_immediately(jobs: CronJobs, clock: Clock) -> None:
    job = jobs.create_job("plugins/news.yaml", "0 9 * * 1")  # 每周一(远未来)
    assert jobs.get_due_jobs() == []
    jobs.trigger_job(job["id"])
    assert [j["id"] for j in jobs.get_due_jobs()] == [job["id"]]  # manual 绕过未来判定


# --- 内部:mark 与扫描的组合(语义冒烟已由上覆,此处补 advance 前置)----------------


def test_advance_before_dispatch_prevents_refire(jobs: CronJobs, clock: Clock) -> None:
    # F1.4 时序:先推进再派发——推进+fire 认领后,派发窗口内再扫不重发。
    job = jobs.create_job("plugins/news.yaml", "every 5m")
    clock.tick(minutes=6)
    due = jobs.get_due_jobs()
    assert len(due) == 1
    assert jobs.advance_next_runs([job["id"]]) == 1  # 先推进(at-most-once)
    assert jobs.claim_job_for_fire(job["id"]) is True  # 派发认领(清 pending_slot)
    clock.tick(seconds=30)
    assert jobs.get_due_jobs() == []  # 已推进+认领,不重发
