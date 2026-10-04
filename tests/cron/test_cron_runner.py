"""cron 执行体与运行摘要(tests 冻结命名,10-04-hermes-cron implement B1)。

覆盖面(ask B1 四组 + 邻接):

- **spawn/JSON 解析**:真子进程 stdout JSON 泵 + stderr 分流(``--json``
  契约:stdout 恰一份 JSON)、替身 payload 直携、契约破裂(垃圾 stdout)→
  failed 结构化错误;
- **退出码映射**:0=ok / 3=ok+partial 附注 / 2、1=failed / 超时=failed /
  spawn 失败=failed;
- **超时 killpg**:SIGTERM 即死路径 + 忽略 SIGTERM 的宽限 SIGKILL 路径
  (真子进程、自成进程组,start_new_session 形态与生产一致);
- **deliver**:local(零通道触碰)+ 平台 spec(RecordingChannel 范式,
  test_push.py:74 同款;kind="cron_summary"、透传模板、伪条目 markdown)、
  failure_deliver 回落/显式/none、投递失败 → ``(True, None, err)`` 三态
  (delivery_failed 语义的 runner 侧证据);
- **D14 孤儿回收**:死属主 killpg+unknown+清登记、活属主不越权、已终态
  行仍杀孤、PID 复用指纹不符绝不误杀;在途登记随 spawn 起落;
- 邻接:输出文档落盘/裁剪、D10 run_summary 入账本、self_command dev/冻结
  形态、JobRunner 协议形状(与 tick 端到端)、SendContext 受控扩值 +
  feishu card_title 摘要支(grill Q3)。

控时纪律(ground-truth B16):无 freezegun,注入 ``now_fn`` 显式 aware
datetime;子进程一律 ``sys.executable -c`` 内联脚本,零网络零管线依赖。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Optional
from zoneinfo import ZoneInfo

import pytest

import myssia.push as myssia_push
from myssia.cron.executions import pid_exists
from myssia.cron.jobs import CronJobs
from myssia.cron.runner import (
    CronRunner,
    InflightContext,
    SubprocessResult,
    _parse_run_payload,
    _prune_job_outputs,
    _write_inflight_marker,
    job_command,
    job_db_path,
    reap_orphaned_subprocesses,
    run_subprocess,
    self_command,
)
from myssia.cron.summary import (
    CRON_SUMMARY_TEMPLATE,
    FAILURE_ERROR_CLIP_CHARS,
    SUMMARY_FAILURE_LINE_CLIP,
    SUMMARY_FAILURE_LINE_LIMIT,
    deliver_run_summary,
    render_failure_markdown,
    render_summary_markdown,
    summarize_run,
)
from myssia.cron.tick import tick
from myssia.push.base import PushSendError, SendContext, item_view
from myssia.push.targets import ChannelTarget

TZ = ZoneInfo("Asia/Shanghai")
BASE = datetime(2026, 10, 4, 9, 5, tzinfo=TZ)  # 周日 09:05 → slot=am


class Clock:
    """可拨动的注入时钟(test_cron_tick 同款)。"""

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
def cron(tmp_path: Path, clock: Clock) -> CronJobs:
    return CronJobs(tmp_path, now_fn=clock)


def make_job(**overrides: Any) -> dict[str, Any]:
    """最小合法 job 记录(design §2.1 字段面常用子集;直落库用)。"""
    base: dict[str, Any] = {
        "id": "j1",
        "name": "早晚情报流",
        "category": "/abs/plugins/news.yaml",
        "db_path": None,
        "config_path": None,
        "run_timeout": None,
        "dry_run": False,
        "schedule": {"kind": "interval", "minutes": 30, "display": "every 30m"},
        "schedule_display": "every 30m",
        "repeat": {"times": None, "completed": 0},
        "enabled": True,
        "state": "scheduled",
        "paused_at": None,
        "paused_reason": None,
        "manual_run_at": None,
        "created_at": (BASE - timedelta(days=1)).isoformat(),
        "next_run_at": (BASE - timedelta(minutes=1)).isoformat(),
        "last_run_at": None,
        "last_status": None,
        "last_error": None,
        "last_delivery_error": None,
        "failure_streak": 0,
        "deliver": "local",
        "failure_deliver": None,
        "origin": {"source": "cli"},
        "timezone": None,
    }
    base.update(overrides)
    return base


def make_payload(
    *,
    status: str = "success",
    failed_source: bool = False,
    failures: int = 0,
) -> dict[str, Any]:
    """RunResult.to_dict() 的最小同形片段(A1 契约字段)。"""
    sources = [
        {
            "source": "hnrss",
            "engine": "direct_api",
            "url": "https://hnrss",
            "item_count": 100,
            "attempts": 1,
            "duration_seconds": 1.0,
            "skipped": False,
            "skip_reason": None,
            "failures": [],
            "error": None,
            "failed": False,
        },
        {
            "source": "bad-src",
            "engine": "static_html",
            "url": "https://bad",
            "item_count": 0,
            "attempts": 3,
            "duration_seconds": 2.0,
            "skipped": False,
            "skip_reason": None,
            "failures": [{"error_type": "http_error", "message": "boom"}],
            "error": {"code": "http_error", "message": "boom"}
            if failed_source
            else None,
            "failed": failed_source,
        },
    ]
    return {
        "category": "news",
        "category_name": "情报",
        "run_id": 7,
        "status": status,
        "dry_run": False,
        "resumed_from_run_id": None,
        "started_at": "2026-10-04T01:00:00+00:00",
        "finished_at": "2026-10-04T01:00:42+00:00",
        "duration_seconds": 42.0,
        "stages": [],
        "sources": sources,
        "items": [{"url": f"https://item/{n}", "title": f"t{n}"} for n in range(3)],
        "push": [
            {
                "channel": "feishu_card",
                "ok": True,
                "immediate": 3,
                "digest": 12,
                "archive": 8,
            }
        ],
        "failures": [
            {
                "source": "bad-src",
                "url": "https://item/0",
                "title": "t0",
                "error_type": "http_error",
                "message": "boom " * 60,
            }
        ]
        * failures,
        "maintenance": None,
        "feedback_tuning": None,
    }


def fake_spawn(
    result: SubprocessResult,
) -> Callable[..., SubprocessResult]:
    """CronRunner spawn 替身:记录调用、恒返回 *result*。"""
    calls: list[dict[str, Any]] = []

    def _spawn(
        cmd: list[str],
        env: dict[str, str],
        *,
        timeout: float,
        inflight: Optional[InflightContext] = None,
    ) -> SubprocessResult:
        calls.append({"cmd": cmd, "env": env, "timeout": timeout, "inflight": inflight})
        return result

    _spawn.calls = calls  # type: ignore[attr-defined]
    return _spawn


class RecordingChannel:
    """定向摘要投递的测试替身(test_push.py:74 RecordingChannel 范式):
    类级 ``created`` 登记实例(deliver_run_summary 在函数内直构,测试从
    这里取回);``fail=True`` 时发送抛结构化错误。"""

    name = "recording"
    supports_targeting = True
    created: list["RecordingChannel"] = []
    fail: bool = False

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.calls: list[dict[str, Any]] = []
        type(self).created.append(self)

    @staticmethod
    def parse_direct_ref(ref: str) -> ChannelTarget:
        return ChannelTarget(platform="recording", chat_id=ref)

    async def send(self, items: Any, context: SendContext) -> None:
        if type(self).fail:
            raise PushSendError("http_error", "模拟通道故障")
        self.calls.append(
            {"items": [item_view(item) for item in items], "context": context}
        )


@pytest.fixture()
def recording(monkeypatch: pytest.MonkeyPatch) -> type[RecordingChannel]:
    RecordingChannel.created = []
    RecordingChannel.fail = False
    monkeypatch.setitem(myssia_push.PLATFORMS, "recording", RecordingChannel)
    return RecordingChannel


def seed(cron: CronJobs, *records: dict[str, Any]) -> None:
    with cron.store.jobs_lock():
        cron.store.save_jobs(list(records), replace=True)


def raw_of(cron: CronJobs, job_id: str) -> dict[str, Any]:
    return next(j for j in cron.store.load_jobs() if j.get("id") == job_id)


def wait_until(predicate: Callable[[], bool], timeout: float = 10.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return True
        time.sleep(0.05)
    return False


# ---------------------------------------------------------------------------
# self_command / job_command(D11 命令组装)
# ---------------------------------------------------------------------------


def test_self_command_dev_form() -> None:
    """dev 形态:``python -m myssia.cli`` + PYTHONPATH 前插 <repo>/src。"""
    cmd, env = self_command(["run", "x.yaml", "--json"])
    assert cmd[:4] == [sys.executable, "-m", "myssia.cli", "run"]
    src_root = str(Path(__file__).resolve().parents[2] / "src")
    assert env["PYTHONPATH"].startswith(src_root + os.pathsep)


def test_self_command_frozen_form(monkeypatch: pytest.MonkeyPatch) -> None:
    """冻结包形态:直通(bootloader 自带模块,entry.py 同款)。"""
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    cmd, _env = self_command(["run", "x.yaml"])
    assert cmd == [sys.executable, "run", "x.yaml"]


def test_job_command_assembles_argv(cron: CronJobs, tmp_path: Path) -> None:
    """必选段 + 可选段组装:category/--db/--json/--dry-run/--config/db 覆写。"""
    job = make_job(
        dry_run=True,
        config_path="/etc/pools.yaml",
        db_path=str(tmp_path / "alt.db"),
    )
    cmd, env = job_command(cron, job)
    tail = cmd[cmd.index("run") :]
    assert tail[:3] == ["run", "/abs/plugins/news.yaml", "--db"]
    assert tail[3] == str(tmp_path / "alt.db")
    assert "--json" in tail and "--dry-run" in tail
    assert tail[tail.index("--config") + 1] == "/etc/pools.yaml"
    assert env  # 环境透传存在


def test_job_db_path_default_and_override(cron: CronJobs, tmp_path: Path) -> None:
    """db 缺省 = 数据根 myssia.db;覆写 ~ 展开绝对化(tick 分组同口径)。"""
    assert job_db_path(cron, make_job()) == cron.store.data_root / "myssia.db"
    assert (
        job_db_path(cron, make_job(db_path=str(tmp_path / "x.db"))) == tmp_path / "x.db"
    )


# ---------------------------------------------------------------------------
# 子进程层:spawn / JSON 解析 / 超时 killpg
# ---------------------------------------------------------------------------


def test_run_subprocess_pumps_streams_and_parses_payload() -> None:
    """真 spawn:stdout 恰一份 JSON、stderr 分流(--json 契约),解析出 payload。"""
    script = (
        "import sys, json; print('log to stderr', file=sys.stderr); "
        "print(json.dumps({'status': 'success', 'sources': [], 'run_id': 1}))"
    )
    result = run_subprocess(
        [sys.executable, "-c", script], os.environ.copy(), timeout=30
    )
    assert result.exit_code == 0
    assert not result.timed_out
    assert result.spawn_error is None
    assert "log to stderr" in result.stderr_text
    payload = _parse_run_payload(result)
    assert payload is not None and payload["status"] == "success"


def test_run_subprocess_spawn_failure_is_structured() -> None:
    """mock 子进程失败:无法 spawn → [spawn_failed] 结构化错误(不上抛)。"""
    result = run_subprocess(["/nonexistent/binary/xyz"], os.environ.copy(), timeout=5)
    assert result.exit_code is None
    assert result.spawn_error is not None and result.spawn_error.startswith(
        "[spawn_failed]"
    )


def test_run_subprocess_timeout_sigterm_fast_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """墙钟超时:普通子进程 SIGTERM 即死(宽限内收尸)。"""
    result = run_subprocess(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        os.environ.copy(),
        timeout=0.5,
    )
    assert result.timed_out
    assert result.pid is not None
    assert wait_until(lambda: not pid_exists(result.pid or 0), timeout=5)


def test_run_subprocess_timeout_sigkill_after_grace(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """忽略 SIGTERM 的子进程:宽限后 SIGKILL 兜底(killpg 进程组杀)。"""
    monkeypatch.setattr("myssia.cron.runner.TERMINATE_GRACE_SECONDS", 0.5)
    script = (
        "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); "
        "time.sleep(60)"
    )
    started = time.monotonic()
    result = run_subprocess(
        [sys.executable, "-c", script], os.environ.copy(), timeout=0.5
    )
    elapsed = time.monotonic() - started
    assert result.timed_out
    assert result.pid is not None
    # SIGKILL 收尸 + 进程组死透(等待窗口给收尸留余量)。
    assert wait_until(lambda: not pid_exists(result.pid or 0), timeout=10)
    assert elapsed < 30  # 宽限 0.5s + 收尸,秒级完成(不挂满 60s 即证明被杀)


def test_parse_run_payload_rejects_contract_break() -> None:
    """退出码 0 但 stdout 垃圾:payload=None(契约破裂交给执行体判 failed)。"""
    result = SubprocessResult(exit_code=0, stdout_text="not json at all")
    assert _parse_run_payload(result) is None
    # 退出码 1 的 config-error JSON 也不是 RunResult(形状守卫挡下)。
    result = SubprocessResult(exit_code=1, stdout_text='{"error": {"code": "x"}}')
    assert _parse_run_payload(result) is None
    # 空壳 dict 缺 status/sources 同样拒收。
    result = SubprocessResult(exit_code=0, stdout_text='{"foo": 1}')
    assert _parse_run_payload(result) is None


# ---------------------------------------------------------------------------
# 执行体:退出码映射 / 三态 / 落盘 / 账本(D10)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("result", "success", "status", "error_frag"),
    [
        # 0 = ok
        (
            SubprocessResult(exit_code=0, payload=make_payload()),
            True,
            "ok",
            None,
        ),
        # 3 = ok + partial 附注(附注在 summary.status,不进 last_error)
        (
            SubprocessResult(
                exit_code=3, payload=make_payload(status="partial", failed_source=True)
            ),
            True,
            "partial",
            None,
        ),
        # 2 = failed(全源失败)
        (
            SubprocessResult(
                exit_code=2, payload=make_payload(status="failed", failed_source=True)
            ),
            False,
            "failed",
            "Pipeline failed",
        ),
        # 1 = config error(stdout 是错误 JSON,非 RunResult)
        (
            SubprocessResult(
                exit_code=1,
                stdout_text='{"error": {"code": "config"}}',
                stderr_text="boom",
            ),
            False,
            "failed",
            "boom",
        ),
        # 超时 = failed(结构化错误)
        (SubprocessResult(exit_code=-15, timed_out=True), False, "failed", "timed out"),
        # 无法解析 = failed(--json 契约破裂)
        (
            SubprocessResult(exit_code=0, stdout_text="garbage"),
            False,
            "failed",
            "run_json_invalid",
        ),
        # spawn 失败 = failed
        (
            SubprocessResult(
                exit_code=None, spawn_error="[spawn_failed] OSError: nope"
            ),
            False,
            "failed",
            "spawn_failed",
        ),
    ],
)
def test_execute_exit_code_mapping(
    cron: CronJobs,
    result: SubprocessResult,
    success: bool,
    status: str,
    error_frag: Optional[str],
) -> None:
    """退出码映射:0=ok / 3=partial 附注 / 2、1、超时、契约破裂、spawn 失败
    = failed(design §3.2 步骤 4)。"""
    runner = CronRunner(cron, spawn=fake_spawn(result))
    got_success, error, delivery_error = runner.execute(make_job())
    assert got_success is success
    assert delivery_error is None  # deliver=local:零投递
    if success:
        assert error is None
    else:
        assert error is not None and error_frag in error


def test_execute_writes_run_documents_and_records_summary(cron: CronJobs) -> None:
    """输出文档落 output/<job_id>/(:md 带 markdown+摘要 JSON、.log 收 stderr)
    + D10 摘要入账本(终态行带 run_summary_json)。"""
    payload = make_payload(failed_source=True, failures=2)
    result = SubprocessResult(
        exit_code=0, payload=payload, stderr_text="line1\nline2\n"
    )
    execution = cron.ledger.create_execution("j1", source="tick")
    cron.ledger.mark_execution_running(execution["id"])
    runner = CronRunner(cron, spawn=fake_spawn(result))
    job = make_job(execution_id=execution["id"])
    success, error, delivery_error = runner.execute(job)
    assert (success, error, delivery_error) == (True, None, None)

    out_dir = cron.store.job_output_dir("j1")
    docs = sorted(out_dir.glob("*.md"))
    logs = sorted(out_dir.glob("*.log"))
    assert len(docs) == 1 and len(logs) == 1
    doc_text = docs[0].read_text(encoding="utf-8")
    assert "定时运行摘要" in doc_text
    assert "早晚情报流" in doc_text
    assert "条目留存:3" in doc_text
    assert "immediate 3 / digest 12 / archive 8" in doc_text
    assert "失败摘要(共 2 条" in doc_text
    assert "```json" in doc_text  # 摘要 JSON 附录
    assert logs[0].read_text(encoding="utf-8").strip() == "line1\nline2"

    row = cron.ledger.get_execution(execution["id"])
    assert row is not None and row["status"] == "completed"
    summary = json.loads(row["run_summary_json"])
    assert summary["run"]["status"] == "ok"
    assert summary["sources"] == {"total": 2, "ok": 1, "failed": 1, "items": 100}
    assert summary["items_retained"] == 3
    assert len(summary["failures"]) == 2


def test_execute_failure_records_failed_row(cron: CronJobs) -> None:
    """失败路径:账本行 failed + error 文本入账。"""
    execution = cron.ledger.create_execution("j1", source="tick")
    result = SubprocessResult(
        exit_code=2, payload=make_payload(status="failed", failed_source=True)
    )
    runner = CronRunner(cron, spawn=fake_spawn(result))
    job = make_job(execution_id=execution["id"])
    success, error, _ = runner.execute(job)
    assert success is False and error is not None
    row = cron.ledger.get_execution(execution["id"])
    assert row is not None and row["status"] == "failed"
    assert row["error"] == error


def test_prune_job_outputs_keeps_newest() -> None:
    """输出裁剪:时间戳文件名倒序留新(上游 _prune_job_output 语义)。"""
    with tempfile.TemporaryDirectory() as tmp:
        job_dir = Path(tmp)
        for index in range(4):
            (job_dir / f"2026-10-04_09-00-0{index}_000000.md").write_text("x")
            (job_dir / f"2026-10-04_09-00-0{index}_000000.log").write_text("x")
        deleted = _prune_job_outputs(job_dir, 2)
        assert deleted == 4  # 每后缀各删 2
        remaining = sorted(p.name for p in job_dir.iterdir())
        assert remaining == [
            "2026-10-04_09-00-02_000000.log",
            "2026-10-04_09-00-02_000000.md",
            "2026-10-04_09-00-03_000000.log",
            "2026-10-04_09-00-03_000000.md",
        ]


# ---------------------------------------------------------------------------
# deliver:local / 平台 spec / failure_deliver / 三态
# ---------------------------------------------------------------------------


def test_deliver_local_touches_no_channel(cron: CronJobs, recording: type) -> None:
    """deliver=local:投递层吸收(本地落盘即输出文档,D4),零通道触碰。"""
    runner = CronRunner(
        cron, spawn=fake_spawn(SubprocessResult(exit_code=0, payload=make_payload()))
    )
    job = make_job(deliver="local")
    success, _error, delivery_error = runner.execute(job)
    assert (success, delivery_error) == (True, None)
    assert recording.created == []


def test_deliver_platform_spec_sends_cron_summary(
    cron: CronJobs, recording: type
) -> None:
    """平台 spec:通道直构(透传模板)+ kind="cron_summary" + 伪条目 markdown。"""
    result = SubprocessResult(exit_code=0, payload=make_payload())
    runner = CronRunner(cron, spawn=fake_spawn(result))
    job = make_job(deliver="recording:ops")
    success, _error, delivery_error = runner.execute(job)
    assert (success, delivery_error) == (True, None)
    assert len(recording.created) == 1
    channel = recording.created[0]
    assert channel.kwargs.get("template") == CRON_SUMMARY_TEMPLATE
    assert len(channel.calls) == 1
    call = channel.calls[0]
    # SendContext(grill Q3):kind 受控扩值;slot/date 按 fire 完成本地。
    context = call["context"]
    assert isinstance(context, SendContext)
    assert context.kind == "cron_summary"
    assert context.slot == "am"
    assert context.date == "2026-10-04"
    assert context.target is not None and context.target.chat_id == "ops"
    # 伪条目携带摘要 markdown(透传模板取回的就是它)。
    assert "定时运行摘要" in call["items"][0]["markdown"]
    assert "早晚情报流" in call["items"][0]["markdown"]


def test_failure_deliver_falls_back_to_deliver(cron: CronJobs, recording: type) -> None:
    """§8.1 裁决:failure_deliver 缺省回落 deliver —— 失败告警投同一 spec。"""
    result = SubprocessResult(
        exit_code=2, payload=make_payload(status="failed", failed_source=True)
    )
    runner = CronRunner(cron, spawn=fake_spawn(result))
    job = make_job(deliver="recording:ops", failure_deliver=None)
    success, _error, delivery_error = runner.execute(job)
    assert success is False and delivery_error is None
    assert len(recording.created) == 1
    markdown = recording.created[0].calls[0]["items"][0]["markdown"]
    assert "定时运行失败" in markdown
    assert "Pipeline failed" in markdown


def test_failure_deliver_explicit_spec_and_none(
    cron: CronJobs, recording: type
) -> None:
    """显式 failure_deliver 走自己的 spec;``"none"`` 关闭失败告警。"""
    result = SubprocessResult(
        exit_code=2, payload=make_payload(status="failed", failed_source=True)
    )
    runner = CronRunner(cron, spawn=fake_spawn(result))
    success, _e, _d = runner.execute(
        make_job(deliver="recording:ops", failure_deliver="recording:alerts")
    )
    assert success is False
    assert recording.created[0].calls[0]["context"].target.chat_id == "alerts"

    recording.created.clear()
    success, _e, delivery_error = runner.execute(
        make_job(deliver="local", failure_deliver="none")
    )
    assert success is False and delivery_error is None
    assert recording.created == []


def test_delivery_failed_three_state(cron: CronJobs, recording: type) -> None:
    """三态(F1.7):运行成功但投递失败 → ``(True, None, delivery_error)``
    —— success 不翻转,streak 语义交由 tick 的 mark_job_run(邻接测试钉过)。"""
    recording.fail = True
    result = SubprocessResult(exit_code=0, payload=make_payload())
    runner = CronRunner(cron, spawn=fake_spawn(result))
    success, error, delivery_error = runner.execute(make_job(deliver="recording:ops"))
    assert success is True
    assert error is None
    assert delivery_error is not None and "http_error" in delivery_error


def test_deliver_run_summary_error_shapes(tmp_path: Path) -> None:
    """投递层边界:local→None、坏 spec、未知平台 —— 全部返回结构化文本不抛。"""
    job = make_job()
    now = BASE
    assert (
        deliver_run_summary("local", "md", job=job, data_root=tmp_path, now=now) is None
    )
    assert deliver_run_summary("", "md", job=job, data_root=tmp_path, now=now) is None
    bad = deliver_run_summary(
        "no-colon-spec", "md", job=job, data_root=tmp_path, now=now
    )
    assert bad is not None and bad.startswith("[bad_deliver_spec]")
    unknown = deliver_run_summary(
        "nosuch:platform", "md", job=job, data_root=tmp_path, now=now
    )
    assert unknown is not None and unknown.startswith("[unknown_platform]")


def test_deliver_run_summary_stdout_spec_buffered_and_echoed(
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """§8.1 末条:stdout 系 deliver spec 可用(AC6 ``--deliver <stdout/…>``)。

    stdout 永不支持寻址(不入 PLATFORMS)——不走 [unknown_platform];卡片行
    入内存缓冲后经 logger 回显,**绝不写 sys.stdout**(serve 模式协议流零
    污染,push.test 先例同款);JSON 行携带透传模板渲染的 markdown 与
    kind="cron_summary"(grill Q3)。
    """
    import io
    import logging

    stdout_capture = io.StringIO()
    monkeypatch.setattr(sys, "stdout", stdout_capture)
    job = make_job(deliver="stdout:debug")
    markdown = "**早晚情报流** · 定时运行摘要"
    with caplog.at_level(logging.INFO, logger="myssia.cron.summary"):
        result = deliver_run_summary(
            "stdout:debug", markdown, job=job, data_root=tmp_path, now=BASE
        )
    assert result is None
    assert stdout_capture.getvalue() == ""  # 协议流零污染:一行都不直写
    echoed = "\n".join(r.getMessage() for r in caplog.records)
    assert "stdout 通道回显" in echoed
    echo_record = next(
        r for r in caplog.records if "stdout 通道回显" in r.getMessage()
    )
    line = "{" + echo_record.getMessage().partition("{")[2]
    payload = json.loads(line)
    assert payload["channel"] == "stdout"
    assert payload["kind"] == "cron_summary"
    assert payload["text"] == markdown  # 透传模板把伪条目 markdown 渲染进 text


# ---------------------------------------------------------------------------
# JobRunner 协议形状 + tick 端到端(派发回调注入)
# ---------------------------------------------------------------------------


def test_runner_satisfies_tick_protocol_end_to_end(cron: CronJobs) -> None:
    """tick 派发回调注入:execute 即 JobRunner 协议;at-most-once 时序不变
    (先推进后派发、槽消耗后二次 tick 不重发)。"""
    seed(cron, make_job())
    result = SubprocessResult(exit_code=0, payload=make_payload())
    runner = CronRunner(cron, spawn=fake_spawn(result))
    assert tick(cron, execute_job=runner.execute) == 1
    job = raw_of(cron, "j1")
    assert job["last_status"] == "ok"
    assert job["last_error"] is None
    assert (
        job["next_run_at"] == (BASE + timedelta(minutes=30)).isoformat()
    )  # 先推进重锚
    assert tick(cron, execute_job=runner.execute) == 0  # 槽已消耗:不重发


def test_tick_records_delivery_failed_via_real_runner(
    cron: CronJobs, recording: type
) -> None:
    """tick × 真执行体:成功运行 + 投递失败 → last_status="delivery_failed"、
    streak 不动(F1.7 全链)。"""
    recording.fail = True
    seed(cron, make_job(deliver="recording:ops"))
    result = SubprocessResult(exit_code=0, payload=make_payload())
    runner = CronRunner(cron, spawn=fake_spawn(result))
    assert tick(cron, execute_job=runner.execute) == 1
    job = raw_of(cron, "j1")
    assert job["last_status"] == "delivery_failed"
    assert job["failure_streak"] == 0
    assert job["last_delivery_error"] is not None


# ---------------------------------------------------------------------------
# D14:在途登记 + 孤儿回收
# ---------------------------------------------------------------------------


def _spawn_sleep_child() -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,  # 生产形态:自成进程组(killpg 一锅端)
    )


def _dead_pid() -> int:
    child = subprocess.Popen([sys.executable, "-c", "pass"])
    child.wait()
    return child.pid


def _insert_execution_with_owner(
    cron: CronJobs, job_id: str, pid: int, *, status: str = "running"
) -> str:
    """直插一行指定属主 pid 的账本行(模拟他进程认领;公开 transaction)。"""
    from myssia.cron.executions import process_start_time as pst

    execution_id = f"exec-{pid}-{status}"
    with cron.ledger.transaction() as conn:
        conn.execute(
            """INSERT INTO executions
               (id, job_id, source, status, scheduled_instant, pid,
                process_start_time, claimed_at, started_at)
               VALUES (?, ?, 'tick', ?, NULL, ?, ?, ?, ?)""",
            (
                execution_id,
                job_id,
                status,
                pid,
                pst(pid),
                BASE.isoformat(),
                BASE.isoformat(),
            ),
        )
    return execution_id


def test_inflight_marker_written_during_flight_and_dropped() -> None:
    """在途登记随 spawn 起落:飞行中在盘、收尾即删(线程观测飞行窗口)。"""
    with tempfile.TemporaryDirectory() as tmp:
        cron = CronJobs(tmp, now_fn=lambda: BASE)
        cron.store.ensure_dirs()
        inflight = InflightContext(cron.store, "j1", "exec-live")
        done = threading.Event()
        holder: dict[str, Any] = {}

        def _run() -> None:
            holder["result"] = run_subprocess(
                [sys.executable, "-c", "import time; time.sleep(30)"],
                os.environ.copy(),
                timeout=1.0,
                inflight=inflight,
            )
            done.set()

        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
        marker = cron.store.job_output_dir("j1") / ".inflight" / "exec-live.json"
        try:
            assert wait_until(lambda: marker.exists(), timeout=5), (
                "marker never written"
            )
            record = json.loads(marker.read_text(encoding="utf-8"))
            assert record["execution_id"] == "exec-live"
            assert isinstance(record["pid"], int)
            assert isinstance(record["process_start_time"], float)
        finally:
            assert done.wait(timeout=15)
            thread.join(timeout=5)
        assert not marker.exists()  # 收尾即删
        assert holder["result"].timed_out  # 30s 子进程被 1s 墙钟杀掉


def test_reap_kills_orphan_and_marks_unknown(cron: CronJobs) -> None:
    """D14 主路径:死属主孤儿 → killpg + 行终态化 unknown + 清登记。"""
    cron.store.ensure_dirs()
    orphan = _spawn_sleep_child()
    dead = _dead_pid()
    execution_id = _insert_execution_with_owner(cron, "j1", dead)
    _write_inflight_marker(cron.store, "j1", execution_id, orphan)

    assert reap_orphaned_subprocesses(cron) == 1
    orphan.wait(timeout=10)
    assert orphan.returncode is not None and orphan.returncode != 0  # 被杀,非自然退出
    row = cron.ledger.get_execution(execution_id)
    assert row is not None and row["status"] == "unknown"
    marker = cron.store.job_output_dir("j1") / ".inflight" / f"{execution_id}.json"
    assert not marker.exists()


def test_reap_skips_live_owner(cron: CronJobs) -> None:
    """活属主在途:不越权(不杀、不清登记——它的 runner 自己收)。"""
    cron.store.ensure_dirs()
    child = _spawn_sleep_child()
    execution_id = _insert_execution_with_owner(
        cron, "j1", os.getpid()
    )  # 本进程 = 活属主
    _write_inflight_marker(cron.store, "j1", execution_id, child)
    try:
        assert reap_orphaned_subprocesses(cron) == 0
        assert child.poll() is None  # 没被杀
        marker = cron.store.job_output_dir("j1") / ".inflight" / f"{execution_id}.json"
        assert marker.exists()  # 登记未动
    finally:
        child.terminate()
        child.wait(timeout=10)


def test_reap_terminal_row_still_kills_orphan(cron: CronJobs) -> None:
    """行已终态(启动恢复先行标过 unknown)→ 孤儿照样杀、只清登记(D14 的
    杀孤独立于记账:防与新 fire 并发写同 db)。"""
    cron.store.ensure_dirs()
    orphan = _spawn_sleep_child()
    dead = _dead_pid()
    execution_id = _insert_execution_with_owner(cron, "j1", dead, status="unknown")
    _write_inflight_marker(cron.store, "j1", execution_id, orphan)

    assert reap_orphaned_subprocesses(cron) == 1
    orphan.wait(timeout=10)
    assert orphan.returncode is not None and orphan.returncode != 0
    row = cron.ledger.get_execution(execution_id)
    assert row is not None and row["status"] == "unknown"  # 终态不可变:未被二次改写


def test_reap_fingerprint_mismatch_never_kills(cron: CronJobs) -> None:
    """PID 复用防御:登记指纹与当前进程不符 → 只清登记,绝不误杀活进程。"""
    cron.store.ensure_dirs()
    child = _spawn_sleep_child()
    dead = _dead_pid()
    execution_id = _insert_execution_with_owner(cron, "j1", dead)
    marker = _write_inflight_marker(cron.store, "j1", execution_id, child)
    # 篡改登记指纹:与 child 的真实起始时间差出一个世纪。
    record = json.loads(marker.read_text(encoding="utf-8"))
    record["process_start_time"] = 1.0
    marker.write_text(json.dumps(record), encoding="utf-8")
    try:
        assert reap_orphaned_subprocesses(cron) == 1
        assert child.poll() is None  # 指纹不符:没杀
    finally:
        child.terminate()
        child.wait(timeout=10)


def test_tick_reap_step_invokes_orphan_recovery(cron: CronJobs) -> None:
    """tick 集成:reap 步骤(tick.py D14 一行挂点)驱动孤儿回收。"""
    cron.store.ensure_dirs()
    orphan = _spawn_sleep_child()
    dead = _dead_pid()
    execution_id = _insert_execution_with_owner(cron, "j1", dead)
    _write_inflight_marker(cron.store, "j1", execution_id, orphan)
    try:
        from myssia.cron import tick as tick_module

        tick_module._last_dead_owner_reap_at.clear()
        assert tick(cron, execute_job=lambda job: (True, None, None)) == 0
        orphan.wait(timeout=10)
        row = cron.ledger.get_execution(execution_id)
        assert row is not None and row["status"] == "unknown"
    finally:
        if orphan.poll() is None:  # pragma: no cover - 防御收尾
            orphan.terminate()
            orphan.wait(timeout=10)


# ---------------------------------------------------------------------------
# summary.py 单元:归约 / markdown / 截断(Q3 卡面)
# ---------------------------------------------------------------------------


def test_summarize_run_reduction_shape() -> None:
    """零新统计:摘要 dict 只是 RunResult.to_dict 的归约(计数/截断)。"""
    job = make_job()
    payload = make_payload(failed_source=True, failures=7)
    summary = summarize_run(job, payload=payload, exit_code=3)
    assert summary["run"]["status"] == "partial"  # 3 = ok+partial 附注
    assert summary["sources"] == {"total": 2, "ok": 1, "failed": 1, "items": 100}
    assert summary["items_retained"] == 3
    assert summary["push"][0]["archive"] == 8
    assert summary["failure_count"] == 7
    assert len(summary["failures"]) == SUMMARY_FAILURE_LINE_LIMIT  # 行截断
    assert all(len(line) <= SUMMARY_FAILURE_LINE_CLIP for line in summary["failures"])
    # 无 payload(超时):零源面、错误直透。
    empty = summarize_run(
        job, payload=None, exit_code=None, timed_out=True, error="boom"
    )
    assert empty["run"]["status"] == "failed" and empty["run"]["timed_out"] is True
    assert empty["sources"] == {"total": 0, "ok": 0, "failed": 0, "items": 0}


def test_render_markdown_fields() -> None:
    """markdown 版式(design §5 八字段):状态/时长/源/留存/push 桶/失败行。"""
    summary = summarize_run(
        make_job(), payload=make_payload(failed_source=True, failures=1), exit_code=0
    )
    text = render_summary_markdown(summary)
    assert "定时运行摘要" in text
    assert "✅ ok · 退出码 0" in text
    assert "时长:42.0s" in text
    assert "源:2 个,正常 1 / 失败 1,采集条目 100" in text
    assert "条目留存:3" in text
    assert "推送:feishu_card(immediate 3 / digest 12 / archive 8)" in text
    assert "- 失败摘要(共 1 条" in text
    # 超时附注。
    timed = summarize_run(
        make_job(), payload=None, exit_code=-15, timed_out=True, error="x"
    )
    assert "墙钟超时" in render_failure_markdown(timed)


def test_render_failure_markdown_bounded() -> None:
    """失败告警有界:错误截断、stderr 尾行、详情指路(上游一行式纪律)。"""
    summary = summarize_run(
        make_job(),
        payload=None,
        exit_code=2,
        error="E" * 500,
    )
    text = render_failure_markdown(
        summary,
        stderr_tail=["a" * 300, "tail-line"],
        output_path=Path("/tmp/some-output.md"),
    )
    assert "定时运行失败" in text
    # clip_text 计入省略号:上限 180 → 最长 179 个 E + "…"。
    assert "E" * (FAILURE_ERROR_CLIP_CHARS - 1) in text
    assert "E" * FAILURE_ERROR_CLIP_CHARS not in text
    assert "tail-line" in text
    assert "/tmp/some-output.md" in text
    assert len(text.splitlines()[3]) <= 200  # 错误行含前缀在内有界


# ---------------------------------------------------------------------------
# grill Q3:SendContext 受控扩值 + feishu card_title 摘要支
# ---------------------------------------------------------------------------


def test_send_context_accepts_cron_summary_kind() -> None:
    """SendContext.kind="cron_summary" 合法;非法值仍 fail-fast。"""
    ctx = SendContext(slot="am", date="2026-10-04", kind="cron_summary")
    assert ctx.kind == "cron_summary"
    with pytest.raises(ValueError, match="cron_summary"):
        SendContext(slot="am", date="2026-10-04", kind="bogus")


def test_feishu_card_title_cron_summary_branch() -> None:
    """feishu card_title 的 cron_summary 支(既有两支不变)。"""
    from myssia.push.feishu_card import card_title

    ctx = SendContext(
        slot="pm", date="2026-10-04", category="news", kind="cron_summary"
    )
    assert card_title(ctx) == "⏱ news定时摘要 10-04"
    assert card_title(
        SendContext(slot="pm", date="2026-10-04", category="news", kind="immediate")
    ) == ("🔔 news · 10-04")
    assert card_title(
        SendContext(slot="pm", date="2026-10-04", category="news", kind="digest")
    ) == ("📡 news日报 10-04 · 下午摘要")


def test_cron_summary_template_passes_markdown_through() -> None:
    """透传模板:items[0]['markdown'] 原样取回(TemplateRenderer 渲染)。"""
    from myssia.push.templates import TemplateRenderer

    rendered = TemplateRenderer().render(
        CRON_SUMMARY_TEMPLATE,
        [{"markdown": "**hello** 摘要"}],
        SendContext(slot="am", date="2026-10-04", kind="cron_summary"),
    )
    assert rendered == "**hello** 摘要"
