"""Cron job 存储(tests 冻结命名,10-04-hermes-cron implement A2)。

一个文件收拢 jobs.json 注册表的测试面:

- 定位与目录:``for_db`` 数据根推导(A6)、首跑自建、缺文件空态;
- 损坏 JSON 自修复:控制字符 strict 重试、id 键映射拍平、裸列表包 dict、
  jobs 字段烂形状重置、非对象条目丢弃、repeat.completed 规整、不可修复
  RuntimeError;
- 崩溃残留合并:磁盘意外多出的 job 记录合并不覆盖、有意删除(removed_ids)
  不被合并回;
- 并发写:8 线程 × 5 job 持锁 load-modify-save 全量保真;跨进程 flock 超时
  降级为进程内锁(子进程持锁,写不卡死、大声记日志、数据仍落盘);
- 原子写:落盘不留 ``.jobs_*`` 临时残骸;锁可重入(jobs.py A4 的用法形状);
- 记录规整:name 回退链取 category 文件名截 50、schedule_display 回退链、
  effective_job_state/is_job_runnable/is_terminal_job/is_recoverable_error_job;
- 输出目录:id 路径成分校验拒逃逸。

上游对照:`~/.hermes/hermes-agent/cron/jobs.py` 存储段(模块 docstring 行号)。
"""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

import pytest

from myia.cron import store as cron_store
from myia.cron.store import CronJobStore


def make_job(job_id: str, **overrides: Any) -> dict[str, Any]:
    """最小合法 job 记录(design §2.1 字段面的常用子集)。"""
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


@pytest.fixture()
def store(tmp_path: Path) -> CronJobStore:
    return CronJobStore.for_db(tmp_path / "myia.db")


# --- 定位与目录 ---------------------------------------------------------------


def test_for_db_derives_data_root_and_dirs(tmp_path: Path) -> None:
    db = tmp_path / "myia.db"
    s = CronJobStore.for_db(db)
    assert s.data_root == tmp_path
    assert s.cron_dir == tmp_path / "cron"
    assert s.jobs_file == tmp_path / "cron" / "jobs.json"
    assert s.output_dir == tmp_path / "cron" / "output"
    assert s.jobs_lock_file == tmp_path / "cron" / ".jobs.lock"
    assert not s.cron_dir.exists()
    s.ensure_dirs()
    assert s.cron_dir.is_dir() and s.output_dir.is_dir()


def test_load_missing_file_returns_empty_and_creates_dirs(store: CronJobStore) -> None:
    assert store.load_jobs() == []
    assert store.cron_dir.is_dir()  # 读取方也确保目录在(上游 load_jobs 同款)


def test_save_load_roundtrip(store: CronJobStore) -> None:
    jobs = [make_job("a1"), make_job("b2")]
    store.save_jobs(jobs)
    assert store.load_jobs() == jobs
    raw = json.loads(store.jobs_file.read_text(encoding="utf-8"))
    assert raw["jobs"] == jobs
    assert isinstance(raw["updated_at"], str) and raw["updated_at"]


# --- 损坏 JSON 自修复 ---------------------------------------------------------


def write_raw(store: CronJobStore, payload: Any) -> None:
    store.cron_dir.mkdir(parents=True, exist_ok=True)
    text = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
    store.jobs_file.write_text(text, encoding="utf-8")


def test_control_characters_repaired_via_strict_retry(
    store: CronJobStore, caplog: pytest.LogCaptureFixture,
) -> None:
    # 字符串里的裸控制字符:json 严格模式拒绝,strict=False 容忍 → 修复后重写。
    store.cron_dir.mkdir(parents=True, exist_ok=True)
    store.jobs_file.write_text(
        '{"jobs": [{"id": "a' + chr(1) + 'b", "name": "x"}]}', encoding="utf-8")
    with caplog.at_level("WARNING", logger="myia.cron.store"):
        jobs = store.load_jobs()
    assert [j["id"] for j in jobs] == ["a\x01b"]
    # 落盘后的文件用严格模式即可解析(修复持久化)。
    data = json.loads(store.jobs_file.read_text(encoding="utf-8"))
    assert data["jobs"][0]["id"] == "a\x01b"
    assert any("control characters" in r.message for r in caplog.records)


def test_id_keyed_map_flattened_to_list(
    store: CronJobStore, caplog: pytest.LogCaptureFixture,
) -> None:
    write_raw(store, {"jobs": {
        "abc": {"name": "A"},            # 无内联 id → 取键
        "def": {"id": "xyz", "name": "D"},  # 内联 id 优先
        "junk": 3,                        # 非对象 → 跳过并告警
    }})
    with caplog.at_level("WARNING", logger="myia.cron.store"):
        jobs = store.load_jobs()
    assert sorted(j["id"] for j in jobs) == ["abc", "xyz"]
    assert jobs[[j["id"] for j in jobs].index("xyz")]["name"] == "D"
    assert any("id-keyed" in r.message for r in caplog.records)
    assert any("junk" in r.message for r in caplog.records)
    # 磁盘形状已被 replace 重写为可合并的规范列表。
    assert isinstance(json.loads(store.jobs_file.read_text(encoding="utf-8"))["jobs"], list)


def test_bare_list_wrapped_as_dict(store: CronJobStore) -> None:
    write_raw(store, [make_job("only")])
    assert store.load_jobs() == [make_job("only")]
    raw = json.loads(store.jobs_file.read_text(encoding="utf-8"))
    assert isinstance(raw, dict) and raw["jobs"] == [make_job("only")]


def test_invalid_jobs_field_replaced(store: CronJobStore) -> None:
    write_raw(store, {"jobs": "not-a-list", "updated_at": "x"})
    assert store.load_jobs() == []
    assert json.loads(store.jobs_file.read_text(encoding="utf-8"))["jobs"] == []


def test_non_object_entries_dropped(
    store: CronJobStore, caplog: pytest.LogCaptureFixture,
) -> None:
    write_raw(store, [make_job("keep"), "junk", 3, None])
    with caplog.at_level("WARNING", logger="myia.cron.store"):
        jobs = store.load_jobs()
    assert jobs == [make_job("keep")]
    assert any("non-object" in r.message for r in caplog.records)


def test_repeat_completed_normalized(store: CronJobStore) -> None:
    write_raw(store, [
        {"id": "s", "repeat": {"times": 2, "completed": "3"}},   # 字符串数字 → 3
        {"id": "n", "repeat": {"times": 2, "completed": None}},  # null → 0
        {"id": "neg", "repeat": {"times": 2, "completed": -5}},  # 负数 → 0
        {"id": "flt", "repeat": {"times": 2, "completed": 1.0}},  # float → int 1
        {"id": "ok", "repeat": {"times": 2, "completed": 4}},    # 已合法 → 原样
    ])
    jobs = {j["id"]: j for j in store.load_jobs()}
    assert jobs["s"]["repeat"]["completed"] == 3
    assert jobs["n"]["repeat"]["completed"] == 0
    assert jobs["neg"]["repeat"]["completed"] == 0
    assert jobs["flt"]["repeat"]["completed"] == 1
    assert type(jobs["flt"]["repeat"]["completed"]) is int
    assert jobs["ok"]["repeat"]["completed"] == 4


def test_unrepairable_corruption_raises(store: CronJobStore) -> None:
    write_raw(store, "{not json at all")
    with pytest.raises(RuntimeError, match="corrupted and unrepairable"):
        store.load_jobs()


def test_unexpected_top_level_shape_raises(store: CronJobStore) -> None:
    write_raw(store, "42")
    with pytest.raises(RuntimeError, match="Cron database corrupted: expected"):
        store.load_jobs()


# --- 崩溃残留合并 -------------------------------------------------------------


def test_merge_preserves_unexpected_disk_jobs(store: CronJobStore) -> None:
    store.save_jobs([make_job("j1")])
    # 另一进程(或降级锁写者)直接在磁盘上追加了 j2——绕过本进程 save。
    disk = json.loads(store.jobs_file.read_text(encoding="utf-8"))
    disk["jobs"].append(make_job("j2"))
    store.jobs_file.write_text(json.dumps(disk, ensure_ascii=False), encoding="utf-8")
    # 本进程的陈旧载荷只有改过名的 j1:保存不许把 j2 碾掉。
    store.save_jobs([make_job("j1", name="changed")])
    merged = {j["id"]: j for j in store.load_jobs()}
    assert set(merged) == {"j1", "j2"}
    assert merged["j1"]["name"] == "changed"


def test_removed_ids_are_intentional_not_merged_back(store: CronJobStore) -> None:
    store.save_jobs([make_job("j1"), make_job("j2")])
    store.save_jobs([], removed_ids=["j1"])  # 只有意删 j1
    assert [j["id"] for j in store.load_jobs()] == ["j2"]
    store.save_jobs([], removed_ids=["j2"])
    assert store.load_jobs() == []


# --- 并发写 -------------------------------------------------------------------


def test_concurrent_threaded_writes_lose_nothing(store: CronJobStore) -> None:
    errors: list[Exception] = []

    def worker(index: int) -> None:
        try:
            for k in range(5):
                with store.jobs_lock():
                    jobs = store.load_jobs()
                    jobs.append(make_job(f"t{index}-{k}"))
                    store.save_jobs(jobs)
        except Exception as exc:  # pragma: no cover - 失败也要让断言看到
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert errors == []
    assert len(store.load_jobs()) == 40


def test_cross_process_flock_timeout_degrades(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    store = CronJobStore.for_db(tmp_path / "myia.db")
    monkeypatch.setattr(cron_store, "JOBS_LOCK_TIMEOUT_SECONDS", 0.5)
    store.ensure_dirs()
    holder = subprocess.Popen(
        [sys.executable, "-c",
         "import fcntl, time\n"
         f"fd = open({str(store.jobs_lock_file)!r}, 'a+')\n"
         "fcntl.flock(fd, fcntl.LOCK_EX)\n"
         "print('held', flush=True)\n"
         "time.sleep(10)\n"],
        stdout=subprocess.PIPE, text=True,
    )
    try:
        assert holder.stdout is not None
        assert holder.stdout.readline().strip() == "held"
        with caplog.at_level("ERROR", logger="myia.cron.store"):
            started = time.monotonic()
            store.save_jobs([make_job("degraded")])
            elapsed = time.monotonic() - started
        # 等满超时窗后降级直写:既不是 30s 死等,也不是永阻塞。
        assert 0.3 <= elapsed <= 8.0
        assert any("Timed out" in r.message for r in caplog.records)
        assert [j["id"] for j in store.load_jobs()] == ["degraded"]
    finally:
        holder.kill()
        holder.wait()


def test_lock_reentrant_nested_save(store: CronJobStore) -> None:
    # jobs.py(A4)的用法形状:外层持锁读改,内层 save 重入同一把锁。
    with store.jobs_lock():
        jobs = store.load_jobs()
        jobs.append(make_job("nested"))
        store.save_jobs(jobs)
    assert [j["id"] for j in store.load_jobs()] == ["nested"]


def test_atomic_write_leaves_no_tmp_litter(store: CronJobStore) -> None:
    for i in range(5):
        store.save_jobs([make_job(f"j{i}")])
    assert list(store.cron_dir.glob(".jobs_*")) == []


# --- 记录规整 -----------------------------------------------------------------


def test_normalize_job_record_name_fallback_and_display() -> None:
    job = cron_store.normalize_job_record({
        "id": "x1",
        "category": "plugins/news.yaml",
        "schedule": {"kind": "cron", "expr": "0 9 * * *"},
        "enabled": True,
    })
    assert job["name"] == "news.yaml"          # 缺省名取 category 文件名
    assert job["schedule_display"] == "0 9 * * *"  # schedule_display 回退到 expr
    assert job["state"] == "scheduled"
    # 显式字段保留。
    assert cron_store.normalize_job_record(
        {"id": "x2", "name": "自定义", "category": "a.yaml",
         "schedule_display": "every 30m"})["name"] == "自定义"
    # 长文件名截 50。
    long = cron_store.normalize_job_record(
        {"id": "z", "category": "dir/" + "n" * 80 + ".yaml"})
    assert len(long["name"]) == 50
    # id/全缺:兜底 unknown / "?";name 回退链经 job_id(上游同款:id 先被
    # coerce 成 "unknown",name 随之取 "unknown" 而非死代码 "cron job")。
    assert cron_store.normalize_job_record({"category": "a.yaml"})["id"] == "unknown"
    assert cron_store.normalize_job_record({"id": "q"})["schedule_display"] == "?"
    assert cron_store.normalize_job_record({})["name"] == "unknown"


def test_effective_job_state_derivation() -> None:
    # enabled 权威:半暂停(enabled+paused_at)不许显示 paused 还继续发。
    assert cron_store.effective_job_state({"enabled": True, "state": "paused"}) == "scheduled"
    assert cron_store.effective_job_state(
        {"enabled": True, "paused_at": "2026-10-04T00:00:00+08:00"}) == "scheduled"
    assert cron_store.effective_job_state(
        {"enabled": False, "state": "paused"}) == "paused"
    assert cron_store.effective_job_state({"enabled": False}) == "paused"
    # 终态无条件保留。
    assert cron_store.effective_job_state({"enabled": False, "state": "completed"}) == "completed"
    assert cron_store.effective_job_state({"enabled": True, "state": "error"}) == "error"
    assert cron_store.effective_job_state({}) == "scheduled"


def test_runnable_and_terminal_helpers() -> None:
    assert cron_store.is_job_runnable({"enabled": True}) is True
    assert cron_store.is_job_runnable({"enabled": True, "state": "paused"}) is False
    assert cron_store.is_job_runnable({"enabled": True, "paused_at": "x"}) is False
    assert cron_store.is_job_runnable({"enabled": False}) is False
    assert cron_store.is_terminal_job({"state": "completed"}) is True
    assert cron_store.is_terminal_job({"state": "error"}) is True
    assert cron_store.is_terminal_job({"state": "scheduled"}) is False
    # error 态 recurring 可恢复(上游 #16265);once completed 是真终态。
    assert cron_store.is_recoverable_error_job(
        {"state": "error", "schedule": {"kind": "cron"}}) is True
    assert cron_store.is_recoverable_error_job(
        {"state": "error", "schedule": {"kind": "interval"}}) is True
    assert cron_store.is_recoverable_error_job(
        {"state": "error", "schedule": {"kind": "once"}}) is False
    assert cron_store.is_recoverable_error_job(
        {"state": "completed", "schedule": {"kind": "cron"}}) is False


# --- 输出目录 -----------------------------------------------------------------


def test_job_output_dir_rejects_path_escape(store: CronJobStore) -> None:
    store.ensure_dirs()
    assert store.job_output_dir("abc123") == store.output_dir / "abc123"
    for bad in ["", " ", ".", "..", "a/b", "/abs", "a\\b", "a b/.."]:
        with pytest.raises(ValueError):
            store.job_output_dir(bad)
