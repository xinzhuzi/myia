"""Cron job 生命周期:CRUD、暂停/恢复/手动触发、运行记账、到期扫描、心跳标记。

MYIA 移植重写自 Hermes ``cron/jobs.py`` 的生命周期段(NousResearch/
Hermes-Agent,MIT;上游路径 ``~/.hermes/hermes-agent/cron/jobs.py``)。
上游行号对照(``H:`` 前缀):心跳标记族 H:1239-1351 / 记录助手(_with_job、
_complete/_activate_job_record)H:1626-1647 / create_job H:1812 / get_job
H:1943 / resolve_job_ref H:1961 / list_jobs H:1979 / update_job+_
apply_schedule_update H:2077-2147 / pause H:2150 / resume H:2163 / trigger
H:2203 / _claim_is_live H:2245 / rearm_oneshot H:2264 / remove_job H:2299 /
mark_job_run+_record_run_outcome+_advance_after_run H:2376-2518 /
claim_dispatch H:2586 / 心跳认领 H:2641-2682 / advance_next_runs H:2685 /
_machine_id+claim_job_for_fire+heartbeat_fire_claim H:2720-2812 /
COMPLETED_ONESHOT_RETENTION_DAYS+留存清扫 H:2815-2870 / get_due_jobs 全族
H:2875-3340 / 一次性诊断 H:2521-2584。estop 语义照抄上游
``agent/estop.py``(marker 文件、损坏仍算踩下、stat 失败 fail-safe)。

MYIA 适配(任务 10-04-hermes-cron design §2.1/§6/§8,非照抄处仅此):

- **实例化**:Hermes 用 profile 全局 ``_current_cron_store()``;MYIA 用显式
  :class:`CronJobs(data_root)` 持 :class:`~myssia.cron.store.CronJobStore` +
  :class:`~myssia.cron.executions.ExecutionLedger`(与 store/executions 两底座
  同款取舍)。``now`` 可注入(``now_fn``,测试控时范式 B16:显式 aware
  datetime,无 freezegun)。
- **载荷 = category**(D2):prompt/skills/model/provider/toolsets/monitor 族
  不搬;create 时 category 解析为**绝对路径**存储(grill Q5);Q6 的
  ``load_category_file`` 早失败校验属 create 调用方(CLI/sidecar,B2/B3),
  底座层不耦合 pipeline——本模块与 schedule/store/executions 一样零
  ``myssia.*``(cron 外)依赖。
- **四态 last_status**(design §2.1):``ok|failed|delivery_failed|
  skipped_busy``——上游失败态字面量 ``"error"`` 相应改为 ``"failed"``
  (stale-error 重挂守卫同步改判 ``"failed"``);``skipped_busy`` 由
  派发方(tick/runner)经 ``mark_job_run(status=...)`` 显式覆写记入。
- **终态留存**(§8.1):repeat 到限/one-shot 完成 → ``state="completed"``
  记录**留存** 7 天(:data:`COMPLETED_ONESHOT_RETENTION_DAYS`,构造参数
  ``completed_retention_days`` 可覆写,非正数禁用清扫)后由到期扫描清扫;
  recurring 算不出 next → ``state="error"`` 绝不静默停摆(H #16265 守卫)。
- **无 fire fence 文件锁**(上游 ``_under_fire_fence``/scheduler_
  ownership.py):MYIA 的 claim/mark/sweep 各自是 jobs_lock 原子临界区,
  ``expected_fire_owner`` 令牌校验已覆盖过期回据丢弃;跨分钟持有型 fence
  是上游 delivery-queue 形态的诉求(D5 不搬)。
- **无配置面**:上游 ``cron.catch_up_missed``(坍缩后跳过)/``cron.
  completed_retention_days`` 读 hermes config——MYIA 无配置系统:坍缩后
  **无条件补发一发**(F1.4 固定语义),留存天数走构造参数;
  ``record_cron_missed``(监控族,D8)随之不搬。
- **认领 TTL 派生**(D12):one-shot run_claim TTL = ``max(run_timeout ×
  CLAIM_TTL_INACTIVITY_HEADROOM, 1800)`` 按 job 的 ``run_timeout``(缺省
  3600s)派生,替代上游 HERMES_CRON_TIMEOUT 环境旋钮。
- **remove 保留 output 目录**(design §4.1 CLI 表:删记录、output 保留;
  上游 rmtree)。
- **estop marker** = ``<cron_dir>/paused.marker``(design §3.1 步骤 2;
  上游为 ``$HERMES_HOME/ESTOP``,grill Q4 保留语义)。
- **在途运行集**(上游居 scheduler.py 的 ``try_register_running_job`` 族)
  落本模块:due 扫描与 occurrences 都要问「本进程还在跑它吗」,放 runner
  会造成循环 import;runner(B1)派发前 register、finally release。
"""

from __future__ import annotations

import contextlib
import copy
import json
import logging
import os
import re
import socket
import tempfile
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Collection, Optional, Union
from zoneinfo import ZoneInfo

from apscheduler.triggers.cron import CronTrigger

from myssia.cron.constants import (
    CLAIM_TTL_INACTIVITY_HEADROOM,
    FIRE_CLAIM_SKEW_SECONDS,
    FIRE_CLAIM_TTL_SECONDS,
)
from myssia.cron.executions import ExecutionLedger, pid_exists
from myssia.cron.schedule import (
    ONESHOT_GRACE_SECONDS,
    _classify_dispatch_lateness,
    _compute_grace_seconds,
    _elapsed_seconds,
    _ensure_aware,
    _instant_after,
    _instant_at_or_before,
    _normalize_cron_expr,
    _parse_aware,
    _recoverable_oneshot_run_at,
    _stored_wall_clock_is_future,
    _timezone_offset_mismatch,
    compute_next_run,
    normalize_repeat_value,
    parse_schedule,
    resolve_zone,
)
from myssia.cron.store import (
    CronJobStore,
    _has_pause_marker,
    is_job_runnable,
    is_recoverable_error_job,
    is_terminal_job,
    normalize_job_record,
)

logger = logging.getLogger(__name__)

__all__ = [
    "COMPLETED_ONESHOT_RETENTION_DAYS",
    "DEFAULT_RUN_TIMEOUT_SECONDS",
    "ONESHOT_RUN_CLAIM_TTL_SECONDS",
    "AmbiguousJobReference",
    "CronJobs",
    "claim_is_live",
    "job_running_in_this_process",
    "machine_id",
    "release_running_job",
    "resolve_failure_deliver",
    "try_register_running_job",
]


# 完成的 one-shot 留存天数(§8.1;到期扫描清扫,构造参数可覆写)。
COMPLETED_ONESHOT_RETENTION_DAYS = 7

# job 缺省墙钟超时秒数(design §2.1 ``run_timeout`` 缺省 3600;D12)。
DEFAULT_RUN_TIMEOUT_SECONDS = 3600.0

# one-shot run_claim TTL 的下限秒数(上游 H:201 同值):一个真跑着的一次性
# job 不该被 TTL 误杀;TTL 只回收「认领后进程死了」的 claim。
ONESHOT_RUN_CLAIM_TTL_SECONDS = 1800.0

# 全局急停 marker 文件名(design §3.1 步骤 2;`cron pause --all` 写,Q4)。
ESTOP_MARKER_NAME = "paused.marker"

# fire 认领心跳的刷新阈值(缺陷 3 写节流):认领戳年轻于此值时心跳只验
# 属主、不重写 jobs.json。取 TTL/2(150s)——60s 心跳节奏下观测年龄上限
# ≈ 210s < 300s TTL,保活不受影响;测试可 monkeypatch 本值压到 0 复现
# 「每跳必写」的旧语义(test_cron_tick 真实时钟用例)。
CLAIM_REFRESH_MIN_AGE_SECONDS = FIRE_CLAIM_TTL_SECONDS / 2

# create/update 共用的空载荷报错文案(D2:载荷 = category)。
EMPTY_CATEGORY_ERROR = (
    "Cron job requires a category (pipeline YAML path) — the job payload is "
    "the category it runs."
)

_IMMUTABLE_JOB_FIELDS = frozenset({"id"})

_REARM_RECURRING_ERROR = "Cannot re-arm recurring jobs: re-arm is one-shot-only; use plain resume or cron run."

# mark_job_run 里区分「job 不在库」与「写入被拒」的哨兵(上游 _MISSING 同款)。
_MISSING = object()


# ---------------------------------------------------------------------------
# 认领属主与在途运行集(上游 _machine_id/_claim_is_live/scheduler 运行集)
# ---------------------------------------------------------------------------


def machine_id() -> str:
    """认领署名(非正确性来源——正确性来自 jobs 文件锁与令牌校验):
    ``hostname:pid``(上游 ``_machine_id`` H:2720,去 HERMES_MACHINE_ID 覆写)。"""
    try:
        host = socket.gethostname()
    except Exception:
        host = "unknown"
    return f"{host}:{os.getpid()}"


def _claim_owner_is_dead(claim: dict[str, Any]) -> bool:
    """claim 的 ``by`` 是否指认一个**本机可证已死**的进程。异机署名、署名残缺、
    探测失败一律 False(fail-safe:只有确凿死讯才缩短 TTL;上游 H:2228)。"""
    parts = str(claim.get("by") or "").split(":")
    if len(parts) < 2 or not parts[1].isdigit():
        return False
    try:
        if parts[0] != socket.gethostname():
            return False
        return not pid_exists(int(parts[1]))
    except Exception:
        return False


def claim_is_live(claim: Any, now: datetime, ttl_seconds: float) -> bool:
    """well-formed 且年龄落在 ``[-FIRE_CLAIM_TTL_SECONDS, ttl)``、属主未证死的
    认领算活。残缺 claim 与远未来时刻(超容差的时钟/时区偏斜)都算 stale
    ——永远不许楔死一个 job;同机属主进程已退出的认领立即失效,而非等满
    TTL(上游 H:2245)。

    负时长容忍(10-06-hermes-monitor-audit 缺陷 2):时钟回拨/NTP 步进会让
    「刚刚写的认领」读出负年龄;负窗内的认领按活处理——否则回拨瞬间活
    ``fire_claim`` 被 stale 清扫放掉,他宿主重新认领形成双跑窗口(owner-fence
    只能弃回据,停不了已在跑的进程)。容差 = 一个 fire 认领 TTL:回拨超它
    的认领仍判 stale,「永不楔死」红线不变;属主可证死时仍立即失效
    (回拨救不了真死的属主)。"""
    if not isinstance(claim, dict) or not claim.get("at"):
        return False
    claimed_at = _parse_aware(claim["at"], resolve_zone())
    if claimed_at is None or not (
        -FIRE_CLAIM_TTL_SECONDS
        <= _elapsed_seconds(now, claimed_at)
        < ttl_seconds
    ):
        return False
    return not _claim_owner_is_dead(claim)


# --- 在途运行集(上游 scheduler.py try_register/release/is_job_running)-------

# 本进程在途 job id 集(ticker + 手动 run 的单一去重口径:fire claim 的 300s
# TTL 会被真跑长于它的 job 活过——那时手动 run 会二次认领并发跑同一个 job)。
# 键为裸 job id:MYIA 的部署形态是每进程一个数据根(serve 单 --db / sidecar
# 单 home),上游的 per-profile 分键场景不存在(上游 H:222 注释论证照搬)。
_running_lock = threading.Lock()
_running_job_ids: set[str] = set()


def try_register_running_job(job_id: str) -> bool:
    """原子地把 *job_id* 记入在途集;已在途 → False(调用方必须跳过)。成功后
    调用方**必须**在 ``finally`` 里配对 :func:`release_running_job`
    (runner/tick 派发前 register,上游同款契约)。"""
    with _running_lock:
        if job_id in _running_job_ids:
            return False
        _running_job_ids.add(job_id)
        return True


def release_running_job(job_id: str) -> None:
    """把 *job_id* 移出在途集(与 register 配对;幂等)。"""
    with _running_lock:
        _running_job_ids.discard(job_id)


def job_running_in_this_process(job_id: str) -> bool:
    """本进程是否仍有 *job_id* 的在途 run(run_claim TTL 区分不了「认领方死了」
    与「活着但慢」——在途集直接回答;上游 H:222 惰性 import 版的对应物)。"""
    with _running_lock:
        return job_id in _running_job_ids


def resolve_failure_deliver(job: dict[str, Any]) -> Optional[str]:
    """failure_deliver 的有效投递目标(§8.1 事实裁决):

    - 显式 ``"none"`` → ``None``(关闭失败告警);
    - 显式目标 → 原样;
    - 缺省(键缺席/空)→ **回落 deliver**(上游 create_job 同款语义)。

    ``"local"`` 回落值原样返回:本地落盘本身就是有效的失败摘要去向。
    """
    explicit = job.get("failure_deliver")
    if explicit is None:
        explicit_value = None
    elif isinstance(explicit, str):
        explicit_value = explicit.strip() or None
    else:
        explicit_value = str(explicit)
    if explicit_value is None:
        deliver = job.get("deliver")
        return str(deliver) if deliver else None
    if explicit_value.lower() == "none":
        return None
    return explicit_value


# ---------------------------------------------------------------------------
# 心跳标记族(上游 H:1239-1351 照抄;路径挂 store.cron_dir)
# ---------------------------------------------------------------------------


def _atomic_write_marker(path: Path, text: str, tmp_prefix: str) -> None:
    """原子(永不撕裂)的尽力 marker 写:mkstemp 同目录 + fsync + rename +
    收权 0600。失败上抛由调用方吞(上游 atomic_write_text 语义等价重写)。"""
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=tmp_prefix)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        with contextlib.suppress(OSError):
            os.unlink(tmp_name)
        raise
    if os.name != "nt":
        with contextlib.suppress(OSError):
            path.chmod(0o600)


@dataclass
class _MarkerFile:
    """一个 marker 文件名(类型安全的轻量常量;避免裸字符串散布)。"""

    name: str


TICKER_HEARTBEAT = _MarkerFile("ticker_heartbeat")
TICKER_LAST_SUCCESS = _MarkerFile("ticker_last_success")
TICKER_LAST_ERROR = _MarkerFile("ticker_last_error")
CATCH_UP_OCCURRENCES = _MarkerFile("catch_up_occurrences")

# per-writer 心跳戳目录与陈旧写者清扫线(10-06-hermes-monitor-audit 缺陷 1):
# 单 ``ticker_heartbeat`` marker 是 last-writer-wins——双 serve 并存时后写者
# 先停,``cron status`` 只核最后写者 pid,留下最长 3×interval+20s 的 ticker
# 假阴性窗(另一实例明明在跑却被判死)。per-writer 戳集让活性判读覆盖全部
# 写者;沉默超期的写者不是活 ticker,顺手清掉防目录无限累积。
TICKER_WRITERS_DIRNAME = "ticker_writers"
TICKER_WRITER_STALE_SECONDS = 86400.0

# 心跳扫描专用错误 marker(缺陷 9):cron_stale 评估侧持续失败的 Operator
# 可见痕迹——与 ``ticker_last_error``(ticker 自身死活面)分立,互不误染。
HEARTBEAT_SCAN_LAST_ERROR = _MarkerFile("heartbeat_scan_last_error")


# ---------------------------------------------------------------------------
# 到期扫描的共享状态(上游 _DueScan/_DueJob H:2889/2984 照抄)
# ---------------------------------------------------------------------------


@dataclass
class _DueScan:
    """一次到期扫描穿起的可变状态:存储原始记录 + 待持久化信号。"""

    raw_jobs: list[dict[str, Any]]
    now: datetime
    needs_save: bool = False
    removed: set[str] = field(default_factory=set)

    def find(self, job_id: Any) -> Optional[dict[str, Any]]:
        return next((rj for rj in self.raw_jobs if rj["id"] == job_id), None)

    def persist(self, job_id: Any, **fields_: Any) -> None:
        """把 *fields_* 写到 *job_id* 的原始记录并标记需保存(缺失时 no-op)。"""
        rj = self.find(job_id)
        if rj is not None:
            rj.update(fields_)
            self.needs_save = True

    def retire(self, job_id: Any) -> None:
        """把 *job_id* 的原始记录作为有意删除丢弃。"""
        rj = self.find(job_id)
        if rj is not None:
            self.raw_jobs.remove(rj)
            self.removed.add(str(job_id))
            self.needs_save = True


@dataclass
class _DueJob:
    """评估中的一个候选:其记录、schedule、存储的 next_run(原文/aware 形态)。"""

    job: dict[str, Any]
    scan: _DueScan
    next_run: str  # 存储 ISO 串,与 manual_run_at 做字符串精确比对
    raw_next_run_dt: datetime  # 按存储原文(可能带迁移前偏移)
    next_run_dt: datetime  # 规整到配置时区
    zone: ZoneInfo  # job 时区(§2.1 解析链的 job 档)

    @property
    def schedule(self) -> dict[str, Any]:
        return self.job.get("schedule", {})

    @property
    def kind(self) -> Optional[str]:
        return self.schedule.get("kind")

    @property
    def label(self) -> Any:
        return self.job.get("name", self.job.get("id", "?"))

    def recompute_next(self) -> Optional[str]:
        return compute_next_run(
            self.schedule, self.scan.now.isoformat(), tz=self.zone, now=self.scan.now
        )


# ---------------------------------------------------------------------------
# 生命周期门面
# ---------------------------------------------------------------------------


class AmbiguousJobReference(LookupError):
    """job 名匹配到多条记录时抛出(上游 H:1949)。"""

    def __init__(self, ref: str, matches: list[dict[str, Any]]) -> None:
        self.ref = ref
        self.matches = matches
        ids = ", ".join(m["id"] for m in matches)
        super().__init__(
            f"Job name '{ref}' is ambiguous — matches {len(matches)} jobs: {ids}. "
            f"Use the job ID instead."
        )


class CronJobs:
    """一个数据根的 cron job 生命周期门面(存储 + 账本同根)。

    Args:
        data_root: 数据根目录(db 路径的父目录,A6)。
        now_fn: 可注入时钟(返回 aware datetime);缺省本地真实时钟。测试控时
            走这里(B16:显式 aware datetime,无 freezegun)。
        completed_retention_days: 完成终态记录的留存天数(§8.1;缺省
            :data:`COMPLETED_ONESHOT_RETENTION_DAYS`,非正数禁用清扫)。

    契约冻结(10-04-hermes-cron implement A4):tick(A6)/runner(B1)/CLI(B2)/
    sidecar(B3)经本类生命周期 API 读写 job,接口形状不得擅改。
    """

    def __init__(
        self,
        data_root: Union[str, Path],
        *,
        now_fn: Optional[Callable[[], datetime]] = None,
        completed_retention_days: Optional[float] = None,
    ) -> None:
        self.store = CronJobStore(data_root)
        self.ledger = ExecutionLedger(data_root)
        self._now_fn = now_fn
        self._retention_days = (
            float(COMPLETED_ONESHOT_RETENTION_DAYS)
            if completed_retention_days is None
            else float(completed_retention_days)
        )

    @classmethod
    def for_db(cls, db_path: Union[str, Path], **kwargs: Any) -> "CronJobs":
        """从 myssia.db 路径定位(CLI ``--db`` 一传即得;A6)。"""
        return cls(Path(db_path).parent, **kwargs)

    # --- 内部助手 ------------------------------------------------------------

    def _now(self) -> datetime:
        """调度时钟(aware 本地;上游 ``_hermes_now`` 对应物)。"""
        if self._now_fn is not None:
            return self._now_fn()
        return datetime.now().astimezone()

    def _with_job(
        self,
        job_id: Any,
        fn: Callable[[list[dict[str, Any]], int, dict[str, Any]], Any],
        missing: Any = None,
    ) -> Any:
        """在 jobs_lock 内对首个 id 匹配跑 ``fn(jobs, i, job)``;``fn`` 自行保存。
        无匹配返回 *missing*(上游 H:1626)。"""
        with self.store.jobs_lock():
            jobs = self.store.load_jobs()
            for i, job in enumerate(jobs):
                if job.get("id") == job_id:
                    return fn(jobs, i, job)
        return missing

    def _job_zone(self, job: dict[str, Any]) -> ZoneInfo:
        """job 时区(§2.1 解析链的 job 档;``None`` → 本地)。无效 IANA 名
        (手编 jobs.json)告警后按本地处理——绝不因脏数据崩掉 mark/扫描。"""
        tz = job.get("timezone") if isinstance(job, dict) else None
        if not tz:
            return resolve_zone()
        try:
            return resolve_zone(str(tz))
        except ValueError:
            logger.warning(
                "Job %r carries invalid timezone %r; falling back to local time",
                job.get("id"),
                tz,
            )
            return resolve_zone()

    def _oneshot_run_claim_ttl(self, job: dict[str, Any]) -> float:
        """one-shot run_claim TTL(§模块 docstring D12 派生式)。"""
        try:
            timeout = float(job.get("run_timeout") or DEFAULT_RUN_TIMEOUT_SECONDS)
        except (TypeError, ValueError):
            timeout = DEFAULT_RUN_TIMEOUT_SECONDS
        if timeout <= 0:
            return ONESHOT_RUN_CLAIM_TTL_SECONDS
        return max(
            timeout * CLAIM_TTL_INACTIVITY_HEADROOM, ONESHOT_RUN_CLAIM_TTL_SECONDS
        )

    def _next_run_or_reject_past_oneshot(
        self,
        parsed_schedule: dict[str, Any],
        label: str,
        fallback_run_at: Any,
        what: str,
        zone: Optional[ZoneInfo] = None,
    ) -> Optional[str]:
        """compute_next_run 的一次性超窗拒收包装:grace 窗外的 once 不许入库
        (幽灵 job ``next_run_at=None`` 永不落地;上游 H:1797)。"""
        next_run_at = compute_next_run(parsed_schedule, tz=zone, now=self._now())
        if parsed_schedule.get("kind") == "once" and next_run_at is None:
            run_at = parsed_schedule.get("run_at") or fallback_run_at
            logger.warning(
                "Rejecting one-shot cron job %s'%s': run_at %s is outside the %ss grace window",
                what,
                label,
                run_at,
                ONESHOT_GRACE_SECONDS,
            )
            raise ValueError(
                f"Requested one-shot time {run_at} is more than "
                f"{ONESHOT_GRACE_SECONDS}s in the past and cannot be scheduled."
            )
        return next_run_at

    # --- estop(全局急停;grill Q4,上游 agent/estop.py 语义照抄)------------

    @property
    def estop_marker(self) -> Path:
        """全局急停 marker 路径(``<cron_dir>/paused.marker``)。"""
        return self.store.cron_dir / ESTOP_MARKER_NAME

    def engage_estop(self, reason: Optional[str] = None) -> Path:
        """踩下全局急停(``cron pause --all``):存在期间 tick 跳过派发,绝不动
        在途 run。幂等;body 为可选 JSON ``{"reason","engaged_at"}``,损坏/空
        文件同样算踩下(fail-safe,``touch`` 即停)。"""
        path = self.estop_marker
        payload = {"engaged_at": self._now().isoformat(), "reason": reason or None}
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        except OSError:
            with contextlib.suppress(OSError):
                path.touch(exist_ok=True)
        return path

    def disengage_estop(self) -> bool:
        """解除全局急停(``cron resume --all``);返回是否有 marker 被移除。"""
        with contextlib.suppress(OSError):
            self.estop_marker.unlink()
            return True
        return False

    def is_estopped(self) -> bool:
        """急停是否踩下;stat 失败 fail-safe 按**踩下**处理(上游 is_engaged)。"""
        try:
            return self.estop_marker.exists()
        except OSError:
            return True

    # --- 心跳标记族(上游 H:1239-1351)---------------------------------------

    def _write_marker(self, marker: _MarkerFile, text: str, tmp_prefix: str) -> None:
        """原子尽力 marker 写;失败吞掉——marker 永远不许弄崩 tick。"""
        try:
            self.store.ensure_dirs()
            _atomic_write_marker(self.store.cron_dir / marker.name, text, tmp_prefix)
        except Exception:
            pass

    def _read_marker_fields(self, marker: _MarkerFile) -> list[str]:
        try:
            return (
                (self.store.cron_dir / marker.name)
                .read_text(encoding="utf-8-sig")
                .split()
            )
        except Exception:
            return []

    def _epoch_file_age(self, marker: _MarkerFile) -> Optional[float]:
        """距 marker 里 epoch 戳的秒数;缺失/不可读 → None(「不能判定」而非
        「已死」)。"""
        try:
            return max(0.0, time.time() - float(self._read_marker_fields(marker)[0]))
        except Exception:
            return None

    def record_ticker_heartbeat(self, success: bool = False) -> None:
        """记录 ticker 活性(``success=True`` 时另戳「上次成功 tick」),让
        ``cron status`` 分得清「活着但在失败」与「真在发」——每 tick 恰一次。
        内容 ``<epoch> <pid>``:被杀 ticker 的最后戳还能新鲜约几分钟,无其他
        凭据的读者要能核实写入进程仍活着(上游 #32612/#32895)。

        另落 per-writer 戳(缺陷 1):单 marker 是 last-writer-wins,双 serve
        并存时活性判读必须覆盖全部写者——每实例 ``ticker_writers/<host>-<pid>``
        一份,读者取全集仲裁,写者顺手清死同胞。"""
        self._write_marker(TICKER_HEARTBEAT, f"{time.time()} {os.getpid()}", ".hb_")
        if success:
            self._write_marker(TICKER_LAST_SUCCESS, str(time.time()), ".hb_")
        self._refresh_ticker_writer_stamp()

    @staticmethod
    def _sanitize_host(host: str) -> str:
        """host 名压进 marker 文件名的安全形(非 ``[A-Za-z0-9_.-]`` → ``_``)。"""
        return re.sub(r"[^A-Za-z0-9_.-]", "_", host)

    @staticmethod
    def _local_hostname() -> str:
        try:
            return socket.gethostname()
        except Exception:
            return "unknown"

    def _ticker_writers_dir(self) -> Path:
        """per-writer 心跳戳目录(缺陷 1)。"""
        return self.store.cron_dir / TICKER_WRITERS_DIRNAME

    def _refresh_ticker_writer_stamp(self) -> None:
        """刷新自己的 per-writer 戳并顺手清死写者;全部尽力——marker 族
        永不许弄崩 tick。"""
        try:
            writers_dir = self._ticker_writers_dir()
            writers_dir.mkdir(parents=True, exist_ok=True)
            pid = os.getpid()
            name = f"{self._sanitize_host(self._local_hostname())}-{pid}"
            _atomic_write_marker(
                writers_dir / name, f"{time.time()} {pid}\n", ".hbw_"
            )
            self._prune_ticker_writers(writers_dir, own_pid=pid)
        except Exception:
            pass

    def _prune_ticker_writers(self, writers_dir: Path, *, own_pid: int) -> None:
        """清同机可证已死的写者戳与沉默超期的陈旧戳(OSError 尽力吞)。"""
        now = time.time()
        local = self._sanitize_host(self._local_hostname())
        try:
            paths = list(writers_dir.iterdir())
        except OSError:
            return
        for path in paths:
            host, _, pid_text = path.name.rpartition("-")
            epoch: Optional[float] = None
            try:
                fields = path.read_text(encoding="utf-8-sig").split()
                epoch = float(fields[0])
            except (OSError, ValueError, IndexError):
                pass
            if (
                host == local
                and pid_text.isdigit()
                and int(pid_text) != own_pid
                and not pid_exists(int(pid_text))
            ):
                with contextlib.suppress(OSError):
                    path.unlink()  # 同机死写者:进程已退,戳不再算数
                continue
            if epoch is not None and now - epoch > TICKER_WRITER_STALE_SECONDS:
                with contextlib.suppress(OSError):
                    path.unlink()  # 沉默超期的写者不是活 ticker

    def _ticker_writer_stamps(self) -> list[tuple[Optional[float], Optional[int], str]]:
        """全部 per-writer 戳的 ``(戳龄, pid, host)``;读不了的项跳过。"""
        stamps: list[tuple[Optional[float], Optional[int], str]] = []
        try:
            paths = list(self._ticker_writers_dir().iterdir())
        except OSError:
            return stamps
        for path in paths:
            try:
                fields = path.read_text(encoding="utf-8-sig").split()
                age = max(0.0, time.time() - float(fields[0]))
                pid = int(fields[1])
            except (OSError, ValueError, IndexError):
                continue
            host, _, _pid = path.name.rpartition("-")
            stamps.append((age, pid, host))
        return stamps

    def ticker_heartbeat_writer_alive(self) -> bool:
        """是否有**任一**心跳写者进程仍在运行。单 marker 只见最后写者
        (缺陷 1 的假阴性窗),per-writer 集覆盖全部写者——任一同机写者
        pid 活着即活;无 per-writer 集的遗留形态回落旧式单 marker(旧式
        裸 epoch 戳没有署名,单凭它不算活调度器的证明)。异机署名证不了
        活,跳过(fail-safe 同 ``_claim_owner_is_dead`` 取向)。"""
        local = self._sanitize_host(self._local_hostname())
        for _age, pid, host in self._ticker_writer_stamps():
            if host == local and pid is not None and pid_exists(pid):
                return True
        fields_ = self._read_marker_fields(TICKER_HEARTBEAT)
        try:
            return len(fields_) >= 2 and pid_exists(int(fields_[1]))
        except Exception:
            return False

    def get_ticker_heartbeat_age(self) -> Optional[float]:
        """距 ticker 上次循环迭代的秒数(全写者取**最新鲜**的一份;含旧式
        单 marker);None = 缺失/不可读。"""
        ages = [age for age, _pid, _host in self._ticker_writer_stamps()]
        legacy = self._epoch_file_age(TICKER_HEARTBEAT)
        if legacy is not None:
            ages.append(legacy)
        return min(ages) if ages else None

    def get_ticker_success_age(self) -> Optional[float]:
        """距 ticker 上次**无异常完成**一次 tick 的秒数,或 None。"""
        return self._epoch_file_age(TICKER_LAST_SUCCESS)

    def _read_dated_error(self, marker: _MarkerFile) -> Optional[str]:
        """``<epoch>\n<消息…>`` 形 marker 的消息段;缺失/不可读 → None。"""
        try:
            raw = (self.store.cron_dir / marker.name).read_text(encoding="utf-8-sig")
        except Exception:
            return None
        lines = raw.splitlines()
        if len(lines) < 2:
            return None
        return "\n".join(lines[1:]).strip() or None

    def record_ticker_error(self, message: str) -> None:
        """持久化最近一次 tick 失败,让另一进程的 ``cron status`` 能给出原因
        而非只有新鲜度。"""
        self._write_marker(
            TICKER_LAST_ERROR, f"{time.time()}\n{message.strip()}\n", ".terr_"
        )

    def clear_ticker_error(self) -> None:
        """成功 tick 后移除上次错误 marker(尽力)。"""
        with contextlib.suppress(OSError):
            (self.store.cron_dir / TICKER_LAST_ERROR.name).unlink()

    def get_ticker_last_error(self) -> Optional[str]:
        """最近记录的 tick 错误消息,或 None。"""
        return self._read_dated_error(TICKER_LAST_ERROR)

    # --- 心跳扫描错误 marker(缺陷 9:ticker 直挂 cron_stale 扫描的失败面)---

    def record_heartbeat_scan_error(self, message: str) -> None:
        """持久化最近一次心跳告警扫描失败:持续失败此前只留 ERROR 日志,
        ``cron status`` 无从可见(缺陷 9)。与 ticker 自身错误面分立——
        写 ``ticker_last_error`` 会把「ticker 活着但评估在失败」误染成
        「ticker 在失败」。"""
        self._write_marker(
            HEARTBEAT_SCAN_LAST_ERROR, f"{time.time()}\n{message.strip()}\n", ".hserr_"
        )

    def clear_heartbeat_scan_error(self) -> None:
        """成功一扫后移除扫描错误 marker(尽力)。"""
        with contextlib.suppress(OSError):
            (self.store.cron_dir / HEARTBEAT_SCAN_LAST_ERROR.name).unlink()

    def get_heartbeat_scan_last_error(self) -> Optional[str]:
        """最近记录的心跳扫描错误消息,或 None。"""
        return self._read_dated_error(HEARTBEAT_SCAN_LAST_ERROR)

    def get_catch_up_occurrence_count(self) -> int:
        """积压补发(catch-up)计数(本数据根)。"""
        try:
            return max(
                0,
                int(
                    (self.store.cron_dir / CATCH_UP_OCCURRENCES.name)
                    .read_text(encoding="utf-8-sig")
                    .strip()
                ),
            )
        except (OSError, ValueError):
            return 0

    def record_catch_up_occurrence(self) -> None:
        """积压补发计数 +1(尽力)。"""
        self._write_marker(
            CATCH_UP_OCCURRENCES,
            str(self.get_catch_up_occurrence_count() + 1),
            ".count_",
        )

    # --- 一次性 job 诊断(上游 H:2521-2584,措辞 MYIA 化)-------------------

    def _write_oneshot_diagnostic(
        self, job: dict[str, Any], text: str, what: str
    ) -> bool:
        """job 输出目录里的尽力操作者可见痕迹;永不弄崩调用方。"""
        try:
            output_dir = self.store.job_output_dir(str(job.get("id", "")))
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{self._now().strftime('%Y-%m-%d_%H-%M-%S')}.md"
            _atomic_write_marker(output_file, text, f".{what}_")
            return True
        except Exception as exc:
            logger.debug(
                "Failed to write %s diagnostic for job %r: %s", what, job.get("id"), exc
            )
            return False

    def _write_wedged_oneshot_diagnostic(self, job: dict[str, Any]) -> None:
        """楔死 one-shot 移除前的痕迹:派发已认领(completed>=times)但
        mark_job_run 没跑成(``last_run_at`` 未写)——调度器重启/被杀/非
        Exception 逃逸。静默移除会让用户无输出、无错误、无记录(上游 #73973)。"""
        if job.get("last_run_at") is not None:
            return  # 有过完成 run——正常完成竞态,不是楔死
        repeat = job.get("repeat") or {}
        claim = job.get("run_claim") or {}
        written = self._write_oneshot_diagnostic(
            job,
            "# Cron job removed without producing output\n\n"
            f"- job id: {job.get('id')}\n"
            f"- name: {job.get('name')}\n"
            f"- dispatch claimed: {repeat.get('completed', '?')}/{repeat.get('times', '?')}\n"
            f"- run claimed at: {claim.get('at', 'unknown')} by {claim.get('by', 'unknown')}\n"
            f"- removed at: {self._now().isoformat()}\n\n"
            "This one-shot job's dispatch was claimed, but the run never "
            "completed (`last_run_at` was never written) — the scheduler "
            "process was most likely killed or restarted mid-execution. The "
            "job has been removed to stop it re-firing; recreate it to run "
            "again.\n",
            "wedged-oneshot",
        )
        if written:
            logger.warning(
                "Job '%s': removed without a completed run — diagnostic written to "
                "its output directory",
                job.get("name", job.get("id", "?")),
            )

    def _write_missed_oneshot_diagnostic(
        self, job: dict[str, Any], next_run: str
    ) -> None:
        """grace 窗外退役的从未跑过 one-shot 的痕迹(否则它会无声消失)。"""
        self._write_oneshot_diagnostic(
            job,
            "# Cron job removed before firing (run time outside grace window)\n\n"
            f"- job id: {job.get('id')}\n"
            f"- name: {job.get('name')}\n"
            f"- scheduled run time: {next_run}\n"
            f"- grace window: {ONESHOT_GRACE_SECONDS}s\n"
            f"- removed at: {self._now().isoformat()}\n\n"
            "This one-shot's run time is more than the grace window in the "
            "past (scheduler down past the window, host asleep, or jobs.json "
            "edited), which is outside the 'will never fire' contract "
            "enforced at create/update/resume time. The job was removed "
            "without running; recreate it (or use cron run) to schedule it "
            "again.\n",
            "missed-oneshot",
        )

    # --- CRUD(上游 H:1812-1992,D2/D4 载荷改造)----------------------------

    def create_job(
        self,
        category: str,
        schedule: str,
        *,
        name: Optional[str] = None,
        repeat: Optional[Union[int, str]] = None,
        deliver: Optional[str] = None,
        failure_deliver: Optional[str] = None,
        origin: Optional[dict[str, Any]] = None,
        timezone: Optional[str] = None,
        db_path: Optional[Union[str, Path]] = None,
        config_path: Optional[Union[str, Path]] = None,
        run_timeout: Optional[float] = None,
        dry_run: Optional[bool] = None,
        paused: bool = False,
        paused_reason: Optional[str] = None,
    ) -> dict[str, Any]:
        """创建 cron job 并返回存储记录。

        - ``category``:品类 YAML 路径(载荷,D2);**解析为绝对路径存储**
          (grill Q5)。``load_category_file`` 早失败校验属调用方(B2/B3,Q6)。
        - ``schedule``:五形态 schedule 串(:func:`parse_schedule`)。
        - ``repeat``:``None`` = forever(once 自动 ``times=1``);0/负数按
          forever,字符串 ``'forever'``/``'once'``/数字串规整(共享 chokepoint)。
        - ``deliver`` 缺省 ``"local"``(D4);``failure_deliver`` 仅显式设置才
          持久化——缺省回落 deliver、显式 ``"none"`` 关闭(§8.1)。
        - ``paused``/``paused_reason``:生而暂停(待操作者放行)。
        - 可选键(``dry_run``/``db_path``/``config_path``/``run_timeout``/
          ``failure_deliver``/``origin``/``timezone``)仅显式设置才持久化
          (Hermes 可选键风格,遗留记录字节不变)。

        Raises:
            ValueError: category 空、schedule 无法解析(五形态清单文案)、
                one-shot 时间在 grace 窗外、repeat 不可规整、paused 参数
                自相矛盾、timezone 非 IANA、run_timeout 非正数。
        """
        if not isinstance(paused, bool):
            raise ValueError("paused must be a boolean.")
        if paused_reason is not None and not isinstance(paused_reason, str):
            raise ValueError("paused_reason must be a string.")
        if paused_reason is not None and not paused:
            raise ValueError("paused_reason requires paused=True.")
        if run_timeout is not None and float(run_timeout) <= 0:
            raise ValueError(f"run_timeout must be positive (got {run_timeout!r}).")
        if timezone is not None:
            resolve_zone(str(timezone))  # 早失败:非 IANA 名在此抛
        zone = resolve_zone(str(timezone) if timezone else None)
        category_text = str(category or "").strip()
        if not category_text:
            raise ValueError(EMPTY_CATEGORY_ERROR)
        # grill Q5:解析为绝对路径存储(~ 展开;不校验存在——存在性校验属 Q6
        # 的 load_category_file,归调用方)。
        category_abs = str(Path(category_text).expanduser().resolve())

        parsed_schedule = parse_schedule(schedule, tz=zone, now=self._now())
        repeat_value = normalize_repeat_value(repeat)
        if parsed_schedule["kind"] == "once" and repeat_value is None:
            repeat_value = 1
        if deliver is None:
            deliver = "local"
        job_id = uuid.uuid4().hex[:12]
        now = self._now().isoformat()

        label_source = Path(category_abs).name or "cron job"
        name = name or label_source[:50].strip() or "cron job"
        next_run_at = self._next_run_or_reject_past_oneshot(
            parsed_schedule, name, schedule, "", zone
        )

        job: dict[str, Any] = {
            "id": job_id,
            "name": name,
            "category": category_abs,
            "schedule": parsed_schedule,
            "schedule_display": parsed_schedule.get("display", schedule),
            "repeat": {"times": repeat_value, "completed": 0},  # times None = forever
            "enabled": not paused,
            "state": "paused" if paused else "scheduled",
            "paused_at": now if paused else None,
            "paused_reason": (
                (paused_reason or "").strip()
                or "Created paused; awaiting operator approval."
            )
            if paused
            else None,
            "manual_run_at": None,  # trigger 的单发手动标记(§8.1;mark 后清)
            "created_at": now,
            "next_run_at": None if paused else next_run_at,
            "last_run_at": None,
            "last_status": None,
            "last_error": None,
            "last_delivery_error": None,
            "failure_streak": 0,
            "deliver": deliver,
            "origin": origin,  # 创建来源记录(cli|desktop);不参与投递(D4)
            "timezone": None,
        }
        for key, value in (
            ("failure_deliver", failure_deliver),
            ("db_path", str(db_path) if db_path is not None else None),
            ("config_path", str(config_path) if config_path is not None else None),
            ("run_timeout", float(run_timeout) if run_timeout is not None else None),
            ("dry_run", dry_run),
            ("timezone", str(timezone) if timezone else None),
        ):
            if value is not None:
                job[key] = value

        with self.store.jobs_lock():
            self.store.save_jobs(self.store.load_jobs() + [job])
        return job

    def get_job(self, job_id: str) -> Optional[dict[str, Any]]:
        """按 id 取 job(规整后)。"""
        job = next((j for j in self.store.load_jobs() if j.get("id") == job_id), None)
        return normalize_job_record(job) if job is not None else None

    def resolve_job_ref(self, ref: str) -> Optional[dict[str, Any]]:
        """id 或名字解析到 job:精确 id 优先,其次大小写不敏感名字;重名抛
        :class:`AmbiguousJobReference` 而非静默挑一个(上游 H:1961)。"""
        if not ref:
            return None
        jobs = self.store.load_jobs()
        by_id = next((j for j in jobs if j.get("id") == ref), None)
        if by_id is not None:
            return normalize_job_record(by_id)
        ref_lower = ref.lower()
        name_matches = [j for j in jobs if (j.get("name") or "").lower() == ref_lower]
        if not name_matches:
            return None
        if len(name_matches) > 1:
            raise AmbiguousJobReference(
                ref, [normalize_job_record(j) for j in name_matches]
            )
        return normalize_job_record(name_matches[0])

    def list_jobs(self, include_disabled: bool = False) -> list[dict[str, Any]]:
        """全部 job(可选含 disabled);附 ``latest_execution``(账本富化,
        账本不可用时静默空)。"""
        jobs = [normalize_job_record(j) for j in self.store.load_jobs()]
        if not include_disabled:
            jobs = [j for j in jobs if j.get("enabled", True)]
        try:
            latest = self.ledger.latest_executions(
                [str(job.get("id") or "") for job in jobs]
            )
        except Exception:
            latest = {}
        for job in jobs:
            job["latest_execution"] = latest.get(job.get("id", ""))
        return jobs

    # --- update 族(上游 H:1995-2147,D2 裁字段)----------------------------

    def _reject_terminal_activation(
        self,
        job: dict[str, Any],
        updated: dict[str, Any],
        job_id: str,
    ) -> None:
        """真终态 job 不许经 update_job 复活(走 resume --at / run;上游 H:1995)。"""
        if (
            is_terminal_job(job)
            and not is_recoverable_error_job(job)
            and (
                updated.get("state") not in {"completed", "error"}
                or updated.get("enabled") is True
                or updated.get("next_run_at") is not None
            )
        ):
            raise ValueError(
                f"Cannot activate terminal cron job '{job.get('name', job_id)}' "
                "through update_job; use cron resume --at <ISO-8601> "
                "(or cron run for an immediate fire)."
            )

    def _normalize_job_updates(
        self, job: dict[str, Any], updates: dict[str, Any]
    ) -> None:
        """create 同款的规整,无效值在合并**前**抛;``repeat`` 收存储 dict 或
        裸值(规整,completed 计数保留;上游 H:2027)。"""
        if "category" in updates:
            category_text = str(updates["category"] or "").strip()
            if not category_text:
                raise ValueError(EMPTY_CATEGORY_ERROR)
            updates["category"] = str(Path(category_text).expanduser().resolve())
        if "timezone" in updates and updates["timezone"] is not None:
            resolve_zone(str(updates["timezone"]))  # 早失败
            updates["timezone"] = str(updates["timezone"])
        if "run_timeout" in updates and updates["run_timeout"] is not None:
            if float(updates["run_timeout"]) <= 0:
                raise ValueError(
                    f"run_timeout must be positive (got {updates['run_timeout']!r})."
                )
            updates["run_timeout"] = float(updates["run_timeout"])
        for key in ("db_path", "config_path"):
            if key in updates and updates[key] is not None:
                updates[key] = str(updates[key])
        if "dry_run" in updates and updates["dry_run"] is not None:
            updates["dry_run"] = bool(updates["dry_run"])
        if "repeat" in updates:
            rp = updates["repeat"]
            completed = (job.get("repeat") or {}).get("completed", 0)
            if isinstance(rp, dict):
                rp = dict(rp)
                rp["times"] = normalize_repeat_value(rp.get("times"))
                rp.setdefault("completed", completed)
                updates["repeat"] = rp
            else:
                updates["repeat"] = {
                    "times": normalize_repeat_value(rp),
                    "completed": completed,
                }

    def _rederive_repeat_for_schedule_change(
        self,
        job: dict[str, Any],
        updates: dict[str, Any],
    ) -> None:
        """schedule 更新翻转 kind 时重推导 repeat 缺省:once→times=1、
        recurring→times=None(否则 once 转 recurring 带 times=1 预算一发退役、
        recurring 转 once 永不完成)。同 update 显式 repeat 优先;同 kind 不动
        (上游 H:2045)。"""
        if "schedule" not in updates or "repeat" in updates:
            return
        new_schedule = updates["schedule"]
        if isinstance(new_schedule, str):
            new_schedule = parse_schedule(
                new_schedule, tz=self._job_zone(job), now=self._now()
            )
            updates["schedule"] = new_schedule
        old_kind = (job.get("schedule") or {}).get("kind")
        new_kind = new_schedule.get("kind")
        if old_kind == new_kind:
            return
        repeat = dict(job.get("repeat") or {})
        times = repeat.get("times")
        if new_kind == "once" and times is None:
            repeat["times"] = 1
        elif new_kind != "once" and old_kind == "once" and times == 1:
            repeat["times"] = None
        else:
            return
        repeat.setdefault("completed", 0)
        updates["repeat"] = repeat

    def _apply_schedule_update(
        self,
        updated: dict[str, Any],
        updates: dict[str, Any],
        job_id: str,
    ) -> None:
        """解析字符串 schedule、刷新 ``schedule_display`` 与(未暂停时的)
        ``next_run_at``(上游 H:2077)。"""
        updated_schedule = updated["schedule"]
        if isinstance(updated_schedule, str):
            updated_schedule = parse_schedule(
                updated_schedule, tz=self._job_zone(updated), now=self._now()
            )
            updated["schedule"] = updated_schedule
        updated["schedule_display"] = updates.get(
            "schedule_display",
            updated_schedule.get("display", updated.get("schedule_display")),
        )
        if updated.get("state") != "paused":
            updated["next_run_at"] = self._next_run_or_reject_past_oneshot(
                updated_schedule,
                updated.get("name", job_id),
                updated_schedule,
                "update ",
                self._job_zone(updated),
            )

    def _fill_missing_next_run(self, updated: dict[str, Any]) -> None:
        """enabled 且未暂停的记录绝不许无 ``next_run_at`` 持久化(否则永不发;
        上游 H:2090)。"""
        if (
            not updated.get("enabled", True)
            or updated.get("state") == "paused"
            or updated.get("next_run_at")
        ):
            return
        next_run = compute_next_run(
            updated["schedule"], tz=self._job_zone(updated), now=self._now()
        )
        if next_run is None and updated["schedule"].get("kind") == "once":
            run_at = updated["schedule"].get("run_at", "unknown")
            raise ValueError(
                f"Requested one-shot time {run_at} is in the past "
                f"(grace window: {ONESHOT_GRACE_SECONDS}s) and cannot be scheduled."
            )
        updated["next_run_at"] = next_run

    def update_job(
        self, job_id: str, updates: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """按 id 更新 job,schedule 相关派生字段按需刷新。

        ``id`` 不可更新(输出目录路径成分,更新可泄 ``../escape``)。schedule
        变更时:解析 → 重推导 repeat 缺省 → 重算 ``next_run_at``(未暂停)。
        显式 schedule/生命周期改写会丢弃派发器未认领的 occurrence
        (``pending_slot``)——pause/resume/edit 不得复活编辑前的 slot。
        """
        bad_fields = _IMMUTABLE_JOB_FIELDS.intersection(updates or {})
        if bad_fields:
            raise ValueError(
                f"Cron job field(s) cannot be updated: {', '.join(sorted(bad_fields))}"
            )

        def apply(
            jobs: list[dict[str, Any]], i: int, job: dict[str, Any]
        ) -> dict[str, Any]:
            self._rederive_repeat_for_schedule_change(job, updates)
            self._normalize_job_updates(job, updates)
            updated = {**job, **updates}
            self._reject_terminal_activation(job, updated, job_id)
            if "schedule" in updates:
                self._apply_schedule_update(updated, updates, job_id)
            if {"schedule", "next_run_at", "enabled", "state"}.intersection(updates):
                # 显式 schedule/生命周期改写取代派发器留下的任何未认领 occurrence。
                updated.pop("pending_slot", None)
            self._fill_missing_next_run(updated)
            self._reject_terminal_activation(job, updated, job_id)
            jobs[i] = updated
            self.store.save_jobs(jobs)
            return normalize_job_record(updated)

        return self._with_job(job_id, apply)

    def pause_job(
        self, job_id: str, reason: Optional[str] = None
    ) -> Optional[dict[str, Any]]:
        """暂停(不删)。收 id 或名字(上游 H:2150)。"""
        job = self.resolve_job_ref(job_id)
        if not job:
            return None
        return self.update_job(
            job["id"],
            {
                "enabled": False,
                "state": "paused",
                "paused_at": self._now().isoformat(),
                "paused_reason": reason,
            },
        )

    def resume_job(self, job_id: str) -> Optional[dict[str, Any]]:
        """恢复暂停的 job(收 id 或名字)。

        recurring job 暂停跨过自己的射点时,存储的(已过期的)
        ``next_run_at`` 作为 due 时刻原样过闸——迟发/补发/坍缩策略交给到期
        扫描,绝不静默重锚越过它(#113603);one-shot 与未来时刻照旧从 now
        重算(上游 H:2163)。
        """
        job = self.resolve_job_ref(job_id)
        if not job:
            return None
        stored_next = job.get("next_run_at")
        zone = self._job_zone(job)
        stored_dt = _parse_aware(stored_next, zone) if stored_next else None
        if (
            (job.get("schedule") or {}).get("kind") in {"cron", "interval"}
            and stored_dt is not None
            and _instant_at_or_before(stored_dt, self._now())
        ):
            next_run_at = stored_next
            logger.info(
                "Job '%s' resumed with occurrence %s that elapsed while paused kept due; "
                "the next tick fires it (late/catch-up) or logs the skip.",
                job.get("name", job["id"]),
                stored_next,
            )
        else:
            next_run_at = compute_next_run(job["schedule"], tz=zone, now=self._now())
        if next_run_at is None and (job.get("schedule") or {}).get("kind") == "once":
            run_at = (job.get("schedule") or {}).get("run_at", "unknown")
            raise ValueError(
                f"Cannot resume: one-shot time {run_at} is in the past "
                f"(grace window: {ONESHOT_GRACE_SECONDS}s) and will never fire."
            )
        return self.update_job(
            job["id"],
            {
                "enabled": True,
                "state": "scheduled",
                "paused_at": None,
                "paused_reason": None,
                "next_run_at": next_run_at,
            },
        )

    def trigger_job(self, job_id: str) -> Optional[dict[str, Any]]:
        """安排 job 下个 tick 立即跑(收 id 或名字)。

        §8.1 事实裁决:**复活 paused**(enabled=True + state=scheduled、清暂停
        标记)且**计入 repeat.completed**(真跑一次,由 mark_job_run 计数);
        ``manual_run_at`` 标记(与 ``next_run_at`` 同串)防 TZ 修复守卫把手动
        跑误判为陈旧状态,mark 后清除(上游 H:2203,manual_run_prompt 属 D2
        不搬)。终态 job 拒绝。
        """
        job = self.resolve_job_ref(job_id)
        if not job:
            return None
        if is_terminal_job(job):
            name = job.get("name", job_id)
            raise ValueError(
                f"Cannot run: job '{name}' is {job.get('state')} (terminal). "
                f"Create a new occurrence with 'cron resume {name} --at <ISO-8601>'."
            )
        manual_run_at = self._now().isoformat()
        return self.update_job(
            job["id"],
            {
                "enabled": True,
                "state": "scheduled",
                "paused_at": None,
                "paused_reason": None,
                "next_run_at": manual_run_at,
                "manual_run_at": manual_run_at,
            },
        )

    def rearm_oneshot(self, job_id: str, run_at: Any) -> Optional[dict[str, Any]]:
        """把完成的 one-shot 重挂为显式新 occurrence(上游 H:2264)。

        recurring 拒绝(re-arm 仅一次性);时间经 :func:`parse_schedule` 必须
        解析为 once;grace 窗外拒收;活 run/fire 认领在握时拒收。
        """
        job_ref = self.resolve_job_ref(job_id)
        if not job_ref:
            return None
        if isinstance(run_at, datetime):
            run_at = run_at.isoformat()
        parsed_schedule = parse_schedule(
            str(run_at), tz=self._job_zone(job_ref), now=self._now()
        )
        if parsed_schedule.get("kind") != "once":
            raise ValueError(_REARM_RECURRING_ERROR)
        next_run_at = compute_next_run(
            parsed_schedule, tz=self._job_zone(job_ref), now=self._now()
        )
        if next_run_at is None:
            raise ValueError(
                f"Requested one-shot time {parsed_schedule.get('run_at') or run_at} is more "
                f"than {ONESHOT_GRACE_SECONDS}s in the past and cannot be scheduled."
            )

        def apply(
            jobs: list[dict[str, Any]], _i: int, job: dict[str, Any]
        ) -> dict[str, Any]:
            now = self._now()
            if claim_is_live(
                job.get("run_claim"), now, self._oneshot_run_claim_ttl(job)
            ):
                raise ValueError("Cannot re-arm one-shot over a live run claim.")
            if claim_is_live(job.get("fire_claim"), now, FIRE_CLAIM_TTL_SECONDS):
                raise ValueError("Cannot re-arm one-shot over a live fire claim.")
            if (job.get("schedule") or {}).get("kind") != "once":
                raise ValueError(_REARM_RECURRING_ERROR)
            repeat = job.get("repeat") or {}
            repeat["completed"] = 0
            job.update(
                schedule=parsed_schedule,
                schedule_display=parsed_schedule.get("display", str(run_at)),
                repeat=repeat,
                run_claim=None,
                fire_claim=None,
            )
            self._activate_job_record(job)
            job["next_run_at"] = next_run_at
            self.store.save_jobs(jobs)
            return normalize_job_record(job)

        return self._with_job(job_ref["id"], apply)

    def remove_job(self, job_id: str) -> bool:
        """删除 job(收 id 或名字)。**output 目录保留**(design §4.1:账本与
        输出是运行证据;上游 rmtree 不搬),runs 账本行同样保留。"""
        job = self.resolve_job_ref(job_id)
        if not job:
            return False
        canonical_id = job["id"]
        with self.store.jobs_lock():
            jobs = self.store.load_jobs()
            original_len = len(jobs)
            jobs = [j for j in jobs if j.get("id") != canonical_id]
            if len(jobs) == original_len:
                return False
            self.store.save_jobs(jobs, removed_ids={canonical_id})
            return True

    # --- 运行记账(上游 H:2376-2518;quota/unreachable 钩子 D7 不搬)--------

    def _record_run_outcome(
        self,
        job: dict[str, Any],
        success: bool,
        error: Optional[str],
        delivery_error: Optional[str],
        status: Optional[str],
        now: str,
    ) -> None:
        """把一次完成的 run 戳到 *job*:状态字段、失败连击、告警标记、认领。"""
        job["last_run_at"] = now
        # 手动跑上下文是单发的:刚完成的 run 消费掉了它(§8.1 manual_run_at)。
        job.pop("manual_run_at", None)
        delivery_failed = isinstance(delivery_error, str) and bool(
            delivery_error.strip()
        )
        # 四态(§2.1):显式 status(如 skipped_busy)覆写推导值;MYIA 失败态
        # 字面量 "failed"(上游 "error")。
        job["last_status"] = status or (
            "failed"
            if not success
            else ("delivery_failed" if delivery_failed else "ok")
        )
        job["last_error"] = None if success else error
        if success:
            job["failure_streak"] = 0
        else:
            # 连续**运行**失败连击;投递失败不计(F1.7:success=True 路径)。
            job["failure_streak"] = int(job.get("failure_streak") or 0) + 1
        job["last_delivery_error"] = delivery_error
        # run 结束,job 重新可认领。
        job["fire_claim"] = None
        job.pop("pending_slot", None)
        if job.get("run_claim") is not None:  # 保持遗留记录的键缺席形态
            job["run_claim"] = None

    def _advance_after_run(self, job: dict[str, Any], now: str) -> None:
        """bump ``repeat.completed`` 并重算 ``next_run_at``;到限或 one-shot 无
        下次 run 时退役为终态完成(**记录留存**,§8.1)。

        **锚 run 完成时刻**(§8.1 事实裁决):``compute_next_run(schedule,
        now)`` 的 now = mark 时刻——interval 5m 跑 8m → 下次 = 完成后 +5m,
        不立即补发。recurring 算不出 next → ``state="error"`` 绝不静默停摆
        (H #16265:把缺依赖/坏 expr 变成「job 完成」= 用户的排程无声消失)。
        """
        kind = (job.get("schedule") or {}).get("kind")
        repeat = job.get("repeat")
        if repeat:
            times = repeat.get("times")
            finite = times is not None and times > 0
            completed = repeat.get("completed", 0)
            # 有限 one-shot 的派发已被 claim_dispatch 预认领(completed 已 +1)
            # ——不双计;recurring 与直接调用方照常计数(§8.1:手动 trigger 同样
            # 计入)。上游 #38758 守卫。
            if not (kind == "once" and finite and completed > 0):
                completed += 1
                repeat["completed"] = completed
            if finite and completed >= times:
                # 到限:保留终态记录供 inspect(状态刚写入的 last_status 可查),
                # 留存清扫稍后修剪(§8.1)。
                self._complete_job_record(job)
                return

        job["next_run_at"] = compute_next_run(
            job["schedule"], now, tz=self._job_zone(job), now=self._now()
        )
        if job["next_run_at"] is not None:
            if job.get("state") != "paused":
                job["state"] = "scheduled"
        elif kind in {"cron", "interval"}:
            # recurring:瞬态故障(坏 expr/缺 interval 分钟数)——disable 它会把
            # 故障变成「job 完成」,静默丢掉排程。
            job["state"] = "error"
            if not job.get("last_error"):
                job["last_error"] = (
                    "Failed to compute next run for recurring schedule (malformed "
                    "cron expression or interval); leaving enabled and marking "
                    "state=error so the job is not silently disabled."
                )
            logger.error(
                "Job '%s' (%s) could not compute next_run_at; "
                "leaving enabled and marking state=error so the job is not silently disabled.",
                job.get("name", job.get("id", "?")),
                kind,
            )
        else:
            self._complete_job_record(job)  # one-shot:终态完成

    def mark_job_run(
        self,
        job_id: str,
        success: bool,
        error: Optional[str] = None,
        delivery_error: Optional[str] = None,
        status: Optional[str] = None,
        *,
        expected_fire_owner: Optional[str] = None,
    ) -> bool:
        """记一次 run:last_run_at/last_status、completed 计数、重算
        next_run_at、到限退役终态。

        ``delivery_error`` 与运行错误分立:运行成功但投递失败记
        ``last_status="delivery_failed"``(绝不是 "ok")且 ``failure_streak``
        不动(F1.7)。显式 ``status``(如 ``"skipped_busy"``,Q2)覆写推导值。
        ``expected_fire_owner``:fire 认领属主已换人时丢弃过期完成回据
        (返回 False)。job 不在库 → False(告警)。
        """

        def apply(jobs: list[dict[str, Any]], _i: int, job: dict[str, Any]) -> bool:
            if expected_fire_owner is not None:
                claim = job.get("fire_claim")
                if (
                    not isinstance(claim, dict)
                    or claim.get("by") != expected_fire_owner
                ):
                    logger.warning(
                        "mark_job_run: job_id %s fire claim owner changed; discarding stale completion",
                        job_id,
                    )
                    return False
            now = self._now().isoformat()
            self._record_run_outcome(job, success, error, delivery_error, status, now)
            self._advance_after_run(job, now)
            self.store.save_jobs(jobs)
            return True

        found = self._with_job(job_id, apply, missing=_MISSING)
        if found is _MISSING:
            logger.warning("mark_job_run: job_id %s not found, skipping save", job_id)
            return False
        return bool(found)

    # --- 一次性派发预认领(上游 H:2586 照抄)--------------------------------

    def claim_dispatch(self, job_id: str) -> bool:
        """执行**前**原子预认领有限 one-shot 派发:jobs 锁内 bump 并落盘
        ``repeat.completed``,tick 中途死掉也不丢派发(*at-most-times* 取代
        *at-least-once*;#38758)。True = 调用方可跑;False = 已到限。
        仅 ``kind=="once"`` 且 ``times>0`` 走认领。"""

        def apply(jobs: list[dict[str, Any]], i: int, job: dict[str, Any]) -> bool:
            repeat = job.get("repeat") or {}
            times = repeat.get("times")
            # recurring 用 advance_next_run;无/无限 repeat 上限总是派发。
            if (
                (job.get("schedule") or {}).get("kind") != "once"
                or times is None
                or times <= 0
            ):
                return True
            completed = repeat.get("completed", 0)
            label = job.get("name", job.get("id", "?"))
            if completed >= times:
                if job.get("last_run_at") is not None:
                    # 先前 run 正常完成(mark_job_run 与本 tick 竞态):保留终态
                    # 记录,如 mark_job_run 的到限分支。
                    self._complete_job_record(job)
                    self.store.save_jobs(jobs)
                    logger.info(
                        "Job '%s': dispatch limit reached (%d/%d) — marking completed",
                        label,
                        completed,
                        times,
                    )
                    return False
                # 先前 tick 认领了派发后死掉——真楔死。移除使其不再 due,留
                # 操作者可见诊断(#73973)。
                jobs.pop(i)
                self.store.save_jobs(jobs, removed_ids={job_id})
                self._write_wedged_oneshot_diagnostic(job)
                logger.info(
                    "Job '%s': dispatch limit reached (%d/%d) — removing",
                    label,
                    completed,
                    times,
                )
                return False
            # 副作用跑起来之前认领本次派发。
            repeat["completed"] = completed + 1
            self.store.save_jobs(jobs)
            logger.debug(
                "Job '%s': claimed dispatch %d/%d", label, repeat["completed"], times
            )
            return True

        claimed = self._with_job(job_id, apply, missing=_MISSING)
        if claimed is _MISSING:
            logger.debug(
                "claim_dispatch: job_id %s not in store — proceeding without claim "
                "(nothing to persist a claim against)",
                job_id,
            )
            return True
        return bool(claimed)

    # --- 认领心跳(上游 H:2641-2682 + H:2803)-------------------------------

    def _refresh_claim(
        self,
        jobs: list[dict[str, Any]],
        claim: Any,
        expected_owner: str,
        *,
        min_refresh_age_seconds: float,
    ) -> bool:
        """compare-and-refresh 认领的 ``at`` 戳;*expected_owner* 不再持有 → False。

        写节流(10-06-hermes-monitor-audit 缺陷 3):认领戳仍年轻于
        *min_refresh_age_seconds* 时只验属主、跳过 jobs.json 全量重写——保活
        只需戳年龄远离 TTL(观测年龄上限 = 阈值 + 一跳心跳间隔,取 ``TTL/2``
        即留半窗余量),不必每跳落盘。降级锁下每次全量重写都在放大与并发
        CLI 写互踩的窗口;节流后 fire 认领在 300s TTL/60s 心跳节奏下约
        2-3 跳才写一次。"""
        if not isinstance(claim, dict) or claim.get("by") != expected_owner:
            return False
        now = self._now()
        claimed_at = _parse_aware(claim.get("at"), resolve_zone())
        if (
            claimed_at is not None
            and 0 <= _elapsed_seconds(now, claimed_at) < min_refresh_age_seconds
        ):
            return True  # 属主已验、戳仍新鲜:免一次全量重写
        claim["at"] = now.isoformat()
        self.store.save_jobs(jobs)
        return True

    def heartbeat_run_claim(self, job_id: str, *, expected_owner: str) -> bool:
        """one-shot 的 ``run_claim`` 在 run 存活期间保活:过期 claim 就真意味着
        认领进程死了。compare-and-refresh 阻止陈旧 runner 延长别人接管的认领
        (#62002)。刷新阈值 = 该 job 认领 TTL 的一半(写节流,缺陷 3)。"""

        def apply(jobs: list[dict[str, Any]], _i: int, job: dict[str, Any]) -> bool:
            if (job.get("schedule") or {}).get("kind") != "once":
                return False
            return self._refresh_claim(
                jobs,
                job.get("run_claim"),
                expected_owner,
                min_refresh_age_seconds=self._oneshot_run_claim_ttl(job) / 2,
            )

        return bool(self._with_job(job_id, apply, False))

    def clear_run_claim(self, job_id: str) -> bool:
        """派发本身失败时清 one-shot 的 ``run_claim``:这类 job 到不了
        mark_job_run,陈旧认领会堵住重派发直到 TTL 过期。每个早退路径都调它,
        恢复「job 保持 due、下个健康 tick 会发」的不变量(#86522)。"""

        def apply(jobs: list[dict[str, Any]], _i: int, job: dict[str, Any]) -> bool:
            if (job.get("schedule") or {}).get("kind") != "once" or job.get(
                "run_claim"
            ) is None:
                return False  # recurring,或已清
            job["run_claim"] = None
            self.store.save_jobs(jobs)
            return True

        return bool(self._with_job(job_id, apply, False))

    def heartbeat_fire_claim(self, job_id: str, *, expected_owner: str) -> bool:
        """活 ``fire_claim`` 保活(执行可活过 TTL;属主校验阻止陈旧 runner
        刷新被恢复的认领;上游 H:2803)。刷新阈值 =
        :data:`CLAIM_REFRESH_MIN_AGE_SECONDS`(写节流,缺陷 3:60s 心跳节奏
        下约 2-3 跳落一次盘)。"""

        def apply(jobs: list[dict[str, Any]], _i: int, job: dict[str, Any]) -> bool:
            return self._refresh_claim(
                jobs,
                job.get("fire_claim"),
                expected_owner,
                min_refresh_age_seconds=CLAIM_REFRESH_MIN_AGE_SECONDS,
            )

        return bool(self._with_job(job_id, apply, False))

    # --- 推进(上游 H:2685-2717 照抄)---------------------------------------

    def advance_next_runs(self, job_ids: Collection[str]) -> int:
        """批量推进 recurring ``next_run_at``:整个 due 集一次 load + 至多一次
        save;one-shot/未知 id 跳过;返回推进数。末尾一次持久化——批中途崩溃
        会让重启后重发整个集合而非前缀(亚 10ms 窗口;上游 H:2685)。"""
        ids = set(job_ids)
        if not ids:
            return 0
        with self.store.jobs_lock():
            jobs = self.store.load_jobs()
            now = self._now().isoformat()
            advanced = 0
            for job in jobs:
                if (
                    job.get("id") not in ids
                    or (is_terminal_job(job) and not is_recoverable_error_job(job))
                    or (job.get("schedule") or {}).get("kind")
                    not in {"cron", "interval"}
                ):
                    continue
                new_next = compute_next_run(
                    job["schedule"], now, tz=self._job_zone(job), now=self._now()
                )
                if new_next and new_next != job.get("next_run_at"):
                    job["next_run_at"] = new_next
                    advanced += 1
            if advanced:
                self.store.save_jobs(jobs)
            return advanced

    def advance_next_run(self, job_id: str) -> bool:
        """run_job **前**推进单个 recurring job 的 next_run_at:run 中途崩溃
        不会在重启后重发(at-most-once;一发错过胜过崩溃循环连发)。one-shot
        不动以便重试(上游 H:2712)。"""
        # >= 1(而非 == 1):损坏文件里的重复 id 全部推进;仍如实报推进。
        return self.advance_next_runs([job_id]) >= 1

    # --- fire 认领(上游 H:2734-2800)---------------------------------------

    def claim_job_for_fire(
        self,
        job_id: str,
        *,
        force: bool = False,
        manual: bool = False,
        return_job: bool = False,
    ) -> Union[bool, dict[str, Any]]:
        """为一个外部 fire 原子认领 job(多进程 at-most-once):恰一个 N 之
        一的竞争者赢。jobs 锁内:拒绝缺失/终态/暂停 job,除非 ``force``
        (显式手动 fire,顺带原子复活 job;外部回调必须留 false,陈旧回调不
        得复活暂停 job)。``manual`` = 无射点身份的 off-tick 立即跑(存储的
        ``next_run_at`` 是**下一**个 occurrence,戳它会吞掉那个槽)。输给
        TTL 内更年轻的认领(TTL 让崩溃后的另一 fire 可回收;mark_job_run 清
        认领)。认领成功则戳 ``fire_claim`` 并(recurring)推进
        ``next_run_at``,陈旧重投递无法重发。
        """

        def apply(
            jobs: list[dict[str, Any]], _i: int, job: dict[str, Any]
        ) -> Union[bool, dict[str, Any]]:
            if is_terminal_job(job) and not is_recoverable_error_job(job):
                return False
            # enabled 与暂停标记双闸——半暂停的自相矛盾记录不许认领。``force``
            # (对暂停 job 的 Trigger-now)绕闸并在下面原子复活。
            if not force and not is_job_runnable(job):
                return False
            now = self._now()
            zone = self._job_zone(job)
            if claim_is_live(job.get("fire_claim"), now, FIRE_CLAIM_TTL_SECONDS):
                return False  # 有人持新鲜认领
            from myssia.cron import occurrences

            # ``manual``(off-tick 立即跑)不得戳 occurrence 身份:tick 之外
            # ``next_run_at`` 是下一 occurrence 而非正在跑的这个,戳它会让
            # completed_occurrence() 在那个槽到达时跳过它。
            manual_fire = (
                force or manual or job.get("manual_run_at") == job.get("next_run_at")
            )
            instant = (
                None
                if manual_fire
                else occurrences.scheduled_instant(job.get("next_run_at"))
            )
            # 调度 tick 只在 now >= next_run_at 时发(_evaluate_due_job 对未来
            # 存储射点返回 False),所以**早于**存储下一射点到达的认领不可能是
            # 拥有它的 tick——那是手动/面板 fire,必须不带 occurrence 身份。
            # 绑上它会让 run 把那个**未来**射点在账本里记成 completed:之后的
            # 手动 fire 被拒、调度 tick 的真投递被去重跳过。FIRE_CLAIM_SKEW_
            # SECONDS 窗内的认领就是那个槽的 fire(提供方时钟偏斜);丢它的
            # 身份会让槽无记录、mark_job_run 重算同一 cron 槽、误发保底跑两遍。
            if instant is not None and datetime.fromisoformat(
                instant
            ) - now >= timedelta(seconds=FIRE_CLAIM_SKEW_SECONDS):
                instant = None
            if instant and occurrences.completed_occurrence(
                job, instant, ledger=self.ledger
            ):
                if (job.get("schedule") or {}).get("kind") in {"cron", "interval"}:
                    nxt = compute_next_run(
                        job["schedule"], now.isoformat(), tz=zone, now=now
                    )
                    if nxt:
                        job["next_run_at"] = nxt
                        self.store.save_jobs(jobs)
                return False
            if force:
                self._activate_job_record(job)
            # 每次获取新令牌:进程合法回收自己的陈旧租约,前任 runner 不得仅凭
            # hostname+PID 相同就给新认领续命。
            job["fire_claim"] = {
                "at": now.isoformat(),
                "by": f"{machine_id()}:{uuid.uuid4().hex}",
            }
            # 已认领:occurrence 现归一个 run 所有(其账本行 + fire 认领承载)。
            job.pop("pending_slot", None)
            if (job.get("schedule") or {}).get("kind") in {"cron", "interval"}:
                nxt = compute_next_run(
                    job["schedule"], now.isoformat(), tz=zone, now=now
                )
                if nxt:
                    job["next_run_at"] = nxt
            self.store.save_jobs(jobs)
            return (
                dict(copy.deepcopy(job), _scheduled_instant=instant)
                if return_job
                else True
            )

        # return_job=True 时 apply 返回 dict(快照 + _scheduled_instant),不得
        # 经 bool() 压扁——runner(B1)靠它拿派发时点身份。
        return self._with_job(job_id, apply, False)

    # --- 终态记录与留存清扫(上游 H:1639/2815-2870)--------------------------

    @staticmethod
    def _complete_job_record(job: dict[str, Any]) -> None:
        """就地退役 *job* 为终态完成(记录留存供列表inspect;上游 H:1639)。"""
        job.update(enabled=False, state="completed", next_run_at=None)

    @staticmethod
    def _activate_job_record(job: dict[str, Any]) -> None:
        """就地清暂停标记,*job* 重新可跑(上游 H:1644)。"""
        job.update(enabled=True, state="scheduled", paused_at=None, paused_reason=None)

    def _sweep_completed_oneshots(
        self,
        raw_jobs: list[dict[str, Any]],
        now: datetime,
        *,
        removed_ids: Optional[set[str]] = None,
    ) -> bool:
        """修剪超过留存期的完成 one-shot 记录(就地;有移除返回 True)。
        移除 id 进 *removed_ids* 让 save_jobs 的 shrink-merge 守卫放行删除。
        年龄按 ``last_run_at`` 计;无可解析值的记录保留(绝不猜着删;上游
        H:2836)。"""
        retention_days = self._retention_days
        if retention_days <= 0:
            return False
        cutoff = now - timedelta(days=retention_days)
        removed = False
        for rj in list(raw_jobs):
            try:
                if rj.get("state") != "completed":
                    continue
                schedule = rj.get("schedule")
                if (
                    schedule.get("kind") if isinstance(schedule, dict) else None
                ) != "once":
                    continue
                last_run = rj.get("last_run_at")
                last_run_dt = (
                    _parse_aware(last_run, resolve_zone())
                    if isinstance(last_run, str)
                    else None
                )
                if last_run_dt is None or last_run_dt >= cutoff:
                    continue
                raw_jobs.remove(rj)
                removed = True
                rid = rj.get("id")
                if removed_ids is not None and rid:
                    removed_ids.add(str(rid))
                logger.info(
                    "Job '%s': pruning completed one-shot record (finished %s, retention %.1f days)",
                    rj.get("name", rj.get("id", "?")),
                    last_run,
                    retention_days,
                )
            except Exception:
                logger.debug(
                    "Retention sweep skipped malformed job record %r",
                    rj.get("id", "?"),
                    exc_info=True,
                )
        return removed

    # --- 到期扫描(上游 H:2875-3340;D1/D7/无配置面适配)----------------------

    def get_due_jobs(self) -> list[dict[str, Any]]:
        """返回现在到期的全部 job。

        recurring job 落后超过一个周期(宿主宕机、或 run 超过 interval)时
        积压**坍缩**——``next_run_at`` fast-forward,不连发——但仍**立即补发
        一发**(经 mark_job_run 消耗一次 ``repeat.times``),避免 run 长于
        interval + grace 的 job 被永续推迟(#33315)。坍缩后一律补发(MYIA 无
        ``catch_up_missed`` 配置面,F1.4 固定语义;监控族 record_cron_missed
        D8 不搬)。
        """
        with self.store.jobs_lock():
            return self._get_due_jobs_locked()

    def _get_due_jobs_locked(self) -> list[dict[str, Any]]:
        """get_due_jobs 内层;必须已持 jobs_lock(上游 H:3304)。"""
        raw_jobs = self.store.load_jobs()
        scan = _DueScan(raw_jobs, self._now())
        scan.needs_save = self._normalize_due_scan_records(raw_jobs)
        # 返回的是深拷贝快照:调用方(runner)的内存改动不得别名存储记录。
        jobs = copy.deepcopy(raw_jobs)

        # 留存清扫:完成的 one-shot 供 inspect 保留,但不许无限累积(§8.1)。
        if self._sweep_completed_oneshots(raw_jobs, scan.now, removed_ids=scan.removed):
            scan.needs_save = True
            jobs = [j for j in jobs if scan.find(j.get("id")) is not None]

        due: list[dict[str, Any]] = []
        for job in jobs:
            # 逐 job 隔离:一条残缺记录绝不许中止整个扫描——上面的规整修复已知
            # 形状,这里兜住**未来**变体,健康的兄弟照常 run/持久化。
            try:
                if is_terminal_job(job) and not is_recoverable_error_job(job):
                    continue
                if not job.get("enabled", True):
                    continue
                if _has_pause_marker(job):
                    self._self_disable_half_paused(job, scan)
                    continue
                if self._evaluate_due_job(job, scan):
                    due.append(job)
            except Exception:
                logger.exception(
                    "Skipping malformed cron job %r during due scan",
                    job.get("name") or job.get("id") or "?",
                )

        if scan.needs_save:
            self.store.save_jobs(raw_jobs, removed_ids=scan.removed or None)
        return due

    def _normalize_due_scan_records(self, raw_jobs: list[dict[str, Any]]) -> bool:
        """due 扫描按键前的就地修复:缺失 ``id``(旧写者用 ``job_id``)、非
        dict ``schedule``、非 ISO 时间戳——这些曾让整个扫描在 save_jobs 前
        中止,把调度器冻在 fast-forward 循环里(上游 H:2916)。"""
        changed = False
        zone = resolve_zone()  # 仅做可解析性判定,时区选择无关
        for rj in raw_jobs:
            if not rj.get("id"):
                rj["id"] = rj.pop("job_id", None) or uuid.uuid4().hex[:12]
                changed = True
            if not isinstance(rj.get("schedule"), dict):
                rj["schedule"] = {}
                changed = True
            for key in ("next_run_at", "last_run_at"):
                value = rj.get(key)
                if value is not None and _parse_aware(value, zone) is None:
                    rj.pop(key, None)  # 走「无 next_run_at」路径重算
                    changed = True
        return changed

    def _self_disable_half_paused(self, job: dict[str, Any], scan: _DueScan) -> None:
        """自愈 enabled=true 却带暂停标记:操作者以为冻结而调度器还会发。强制
        enabled=false 让列表诚实;大声记日志(pause_job 原子设两字段,这里
        本应罕见;上游 H:2936)。"""
        jid = job.get("id")
        logger.error(
            "Job '%s' (%s) has pause markers while enabled=true; "
            "self-disabling so it cannot fire (pause must be authoritative).",
            job.get("name", jid),
            jid,
        )
        rj = scan.find(jid)
        if rj is None:
            return
        rj.update(enabled=False, state="paused")
        if not rj.get("paused_at"):
            rj["paused_at"] = scan.now.isoformat()
        if not rj.get("paused_reason"):
            rj["paused_reason"] = "auto-disabled: enabled+paused contradiction"
        scan.needs_save = True

    def _recover_missing_next_run(
        self,
        job: dict[str, Any],
        scan: _DueScan,
    ) -> Optional[str]:
        """重算并持久化缺失的 ``next_run_at``;不可恢复返回 None。one-shot 用
        grace 窗;recurring 走到这里是 jobs.json 被直接编辑绕过了 create,或
        瞬态 compute 失败留在 ``state='error'``(#127182)——重挂成功的回到
        ``'scheduled'``,否则会被永远静默跳过(上游 H:2956)。"""
        schedule = job.get("schedule", {})
        kind = schedule.get("kind")
        zone = self._job_zone(job)
        recovered_next = _recoverable_oneshot_run_at(
            schedule, scan.now, last_run_at=job.get("last_run_at"), zone=zone
        )
        recovery_kind = "one-shot" if recovered_next else None
        if not recovered_next and kind in {"cron", "interval"}:
            recovered_next = compute_next_run(
                schedule, scan.now.isoformat(), tz=zone, now=scan.now
            )
            if recovered_next:
                recovery_kind = str(kind)
        if not recovered_next:
            return None
        logger.info(
            "Job '%s' had no next_run_at; recovering %s run at %s",
            job.get("name", job.get("id", "?")),
            recovery_kind,
            recovered_next,
        )
        fields_: dict[str, Any] = {"next_run_at": recovered_next}
        if is_recoverable_error_job(job):
            fields_["state"] = "scheduled"
        job.update(fields_)
        scan.persist(job["id"], **fields_)
        return recovered_next

    def _repair_timezone_shifted_cron(self, d: _DueJob) -> bool:
        """修复存储偏移不再匹配 now 的 cron job(TZ 迁移)。

        next_run_at 是绝对时刻而 expr 表达本地墙钟,TZ 变更会让它提前数小时
        看似到期。存储墙钟还在未来则重算,在对的本地时刻发。True = 已重锚
        (调用方跳过本 tick)。取舍:DST 偏移变更遇同条件会**跳过**待发
        occurrence;接受为罕见(上游 H:3010)。"""
        now = d.scan.now
        if not (
            _instant_at_or_before(d.next_run_dt, now)
            and _timezone_offset_mismatch(d.raw_next_run_dt, now)
            and _stored_wall_clock_is_future(d.raw_next_run_dt, now)
        ):
            return False
        new_next = d.recompute_next()
        if not new_next:
            return False
        logger.info(
            "Job '%s' next_run_at offset changed (%s -> %s). "
            "Recomputing cron run to preserve local wall-clock intent: %s",
            d.label,
            d.raw_next_run_dt.utcoffset(),
            now.utcoffset(),
            new_next,
        )
        d.scan.persist(d.job["id"], next_run_at=new_next)
        return True

    def _job_is_stale_error_recurring(
        self,
        job: dict[str, Any],
        schedule: dict[str, Any],
        now: datetime,
    ) -> bool:
        """recurring job 是否楔在陈旧的持久失败态(调用方已保证 recurring):
        ``last_status == "failed"``(MYIA 四态字面量;上游 "error")、本进程
        未在跑(绝不在活 run 底下重挂)、且 ``last_run_at`` 老于
        ``cadence + grace``——按排程错误重试的 job 保持新鲜,不算楔(上游
        H:971;quota hold D7 不搬,fire 认领活=他进程在跑,不重挂)。"""
        if job.get("last_status") != "failed":
            return False
        if job_running_in_this_process(str(job.get("id") or "")):
            return False
        if claim_is_live(job.get("fire_claim"), now, FIRE_CLAIM_TTL_SECONDS):
            return False
        last_run = job.get("last_run_at")
        zone = self._job_zone(job)
        last_run_dt = _parse_aware(last_run, zone) if last_run else None
        if last_run_dt is None:
            return False
        age_seconds = _elapsed_seconds(now, last_run_dt)
        if age_seconds < 0:
            return False
        grace = _compute_grace_seconds(schedule)
        cadence_seconds = _schedule_cadence_with_zone(schedule, zone)
        if cadence_seconds is None:
            # 未知 cadence:回落 grace 窗,绝不重挂比它年轻的。
            cadence_seconds = float(grace)
        return age_seconds > (cadence_seconds + grace)

    def _rearm_stale_error_recurring(self, d: _DueJob) -> datetime:
        """重挂楔在持久 last_status=failed 的 recurring job;返回生效的
        next_run_dt。

        这类 job 失败后 mark_job_run 把 next_run_at 停在未来,却没有任何东西
        重派发它。interval 重挂到 now(总是合法射点);cron 重挂到下一**合法**
        射点(重挂到 now 会在 expr 排除的时刻发)。正确的停泊值不动(上游
        H:3035)。"""
        now = d.scan.now
        if not (
            d.kind in ("cron", "interval")
            and _instant_after(d.next_run_dt, now)
            and self._job_is_stale_error_recurring(d.job, d.schedule, now)
        ):
            return d.next_run_dt
        if d.kind == "interval":
            recovered_next: Optional[str] = now.isoformat()
            recovered_next_dt: Optional[datetime] = now
        else:
            recovered_next = d.recompute_next()
            recovered_next_dt = (
                _parse_aware(recovered_next, d.zone) if recovered_next else None
            )
        if not (
            recovered_next
            and recovered_next_dt is not None
            and _instant_after(d.next_run_dt, recovered_next_dt)
        ):
            return d.next_run_dt
        jid = d.job.get("id")
        logger.warning(
            "cron.persisted_error.recovered job='%s' id=%s — recurring "
            "job wedged in stale last_status=failed without re-firing for "
            "a full cadence; re-arming next_run_at to %s so it re-dispatches without force-run/resume",
            d.job.get("name", jid),
            jid,
            recovered_next,
        )
        d.job["next_run_at"] = recovered_next
        d.scan.persist(jid, next_run_at=recovered_next)
        return recovered_next_dt

    def _reanchor_stale_cron(self, d: _DueJob) -> bool:
        """到期 cron 射点的陈旧排程守卫;True = 已重锚未发。

        直接编辑 schedule.expr 会把 next_run_at 留在旧栅格上,先重锚(按当前
        expr,故收敛)。有些射点**有意**离栅:偏移表示迁移(否则吞掉从未发的
        occurrence)——那类落到**发一发**(at-most-once 仍成立:完成覆写射点;
        上游 H:3074;quota/unreachable 停泊射点 D7 不搬,离栅授权发分支随裁)。"""
        stale_class = _classify_stale_cron_next_run(
            d.schedule, d.raw_next_run_dt, d.next_run_dt
        )
        if stale_class == "expr_edit":
            new_next = d.recompute_next()
            logger.info(
                "Job '%s' next_run_at %s does not match its current "
                "cron expression %r (direct jobs.json edit?); re-anchoring to %s without firing.",
                d.label,
                d.next_run,
                d.schedule.get("expr"),
                new_next,
            )
            if new_next:
                d.scan.persist(d.job["id"], next_run_at=new_next)
            return True
        if stale_class == "timezone_migration":
            logger.warning(
                "cron.timezone_migration.catch_up job='%s' id=%s expr=%r "
                "stored=%s normalized=%s — stored next_run_at carries a "
                "pre-migration UTC offset (%s, now %s) and is a legal "
                "occurrence at its own wall clock; firing the due run instead of re-anchoring past it.",
                d.label,
                d.job.get("id"),
                d.schedule.get("expr"),
                d.next_run,
                d.next_run_dt.isoformat(),
                d.raw_next_run_dt.utcoffset(),
                d.scan.now.utcoffset(),
            )
        return False

    def _fast_forward_missed_recurring(self, d: _DueJob, grace: int) -> bool:
        """重锚累计错过;本函数 MYIA 形态恒返回 False(坍缩后一律补发一发,
        F1.4;上游的 catch_up_missed=false 跳过分支随配置面裁)。

        fast-forward 立即持久化——与 advance_next_run/mark_job_run **不**
        冗余:它保护 mark_job_run 之前的崩溃窗口。mark_job_run 完成时重锚,
        所以这个值是临时的(上游 H:3112)。"""
        if _elapsed_seconds(d.scan.now, d.next_run_dt) <= grace:
            return False
        new_next = d.recompute_next()
        if not new_next:
            return False
        d.scan.persist(d.job["id"], next_run_at=new_next)
        logger.info(
            "Job '%s' missed its scheduled time (%s, grace=%ds). "
            "Running now; next run provisionally set to: %s (re-anchored on completion)",
            d.label,
            d.next_run,
            grace,
            new_next,
        )
        self.record_catch_up_occurrence()
        return False

    def _retire_expired_oneshot(self, d: _DueJob) -> bool:
        """one-shot grace 闸;True = 本 tick 不许发。

        grace 窗外的 one-shot 绝不发(create/update/resume 拒收这类 schedule,
        恢复窗也从不复活;只有 due 扫描曾在数小时后派发它们)。无认领在戳则
        退役 + 诊断(绝不静默删)。有认领 = run 可能仍在别处跑——跳过但保留
        记录,让它的 mark_job_run 能落地(上游 H:3142)。"""
        if _elapsed_seconds(d.scan.now, d.next_run_dt) <= ONESHOT_GRACE_SECONDS:
            return False
        if not (d.job.get("run_claim") or d.job.get("fire_claim")):
            self._write_missed_oneshot_diagnostic(d.job, d.next_run)
            d.scan.retire(d.job["id"])
        return True

    def _oneshot_dispatch_limit_reached(
        self, job: dict[str, Any], scan: _DueScan
    ) -> bool:
        """一次性派发到限守卫;True = 本 tick 不许发。

        claim_dispatch 预认领过、tick 却在 mark_job_run 前死掉的有限 one-shot
        会 completed>=times 而仍看似 due。移除而非重发——除非**本进程**还在跑
        它(活 run 之下绝不删 job 记录:活过 run_claim TTL 的 run 是慢,不是
        陈旧;mark_job_run 还需要记录落地 last_run_at 等;上游 #62002)。"""
        repeat = job.get("repeat") or {}
        times = repeat.get("times")
        completed = repeat.get("completed", 0)
        if times is None or times <= 0 or completed < times:
            return False
        name = job.get("name", job.get("id", "?"))
        if job_running_in_this_process(str(job.get("id", ""))):
            logger.info(
                "Job '%s': dispatch limit reached (%d/%d) but its run is still in flight in this "
                "process — keeping entry",
                name,
                completed,
                times,
            )
            return True
        if job.get("last_run_at") is not None:
            # 有 last_run_at 的记录完成过真 run、重挂时没重置预算(旧版或手编)
            # ——不是死 tick 场景;告警让移除留痕。
            logger.warning(
                "Job '%s': one-shot dispatch limit reached (%d/%d) on a record that already completed "
                "a run (last_run_at=%s) — removing it WITHOUT firing. This record was re-armed "
                "without a budget reset (hand edit); re-run it with 'cron run'.",
                name,
                completed,
                times,
                job.get("last_run_at"),
            )
        else:
            logger.info(
                "Job '%s': one-shot dispatch limit reached (%d/%d) — removing stale due entry",
                name,
                completed,
                times,
            )
        scan.retire(job["id"])
        # 认领的 run 按定义没在本进程完成——留操作者可见诊断。
        self._write_wedged_oneshot_diagnostic(job)
        return True

    def _restore_unclaimed_slot(
        self, job: dict[str, Any], scan: _DueScan
    ) -> Optional[str]:
        """把派发器推进过却从未认领的 occurrence 放回排程(#107485);返回
        恢复的 ``next_run_at`` 或 None。**恰恢复一次**:此戳在这里被丢弃,
        槽随后按普通迟到/fast-forward 策略流动——绝不重放每个错过的槽(上游
        H:3200;属主死/租约过才恢复,见 occurrences.unclaimed_pending_slot)。"""
        from myssia.cron import occurrences

        slot = occurrences.unclaimed_pending_slot(job, scan.now)
        if slot is None:
            return None
        logger.warning(
            "Job '%s' (%s): occurrence %s was taken off the schedule but never claimed "
            "(scheduler stopped before dispatch); restoring it as the due instant (was %s).",
            job.get("name", job.get("id")),
            job.get("id"),
            slot,
            job.get("next_run_at"),
        )
        job["next_run_at"] = slot
        job.pop("pending_slot", None)
        rj = scan.find(job["id"])
        if rj is not None:
            rj.pop("pending_slot", None)
        scan.persist(job["id"], next_run_at=slot)
        return slot

    def _evaluate_due_job(self, job: dict[str, Any], scan: _DueScan) -> bool:
        """判定一个 enabled、非终态 job 本 tick 是否发,持久化一切修复。

        顺序要紧:恢复缺失 next_run_at → 修复时区漂移 → 重挂陈旧失败 recurring;
        到期后:重锚陈旧 cron 射点、fast-forward 错过的 recurring、退役/守卫
        one-shot、最后戳 run 认领/派发记录(上游 H:3223)。"""
        now = scan.now
        zone = self._job_zone(job)
        # 跨进程守卫:他进程活着的 one-shot run_claim(年轻于 TTL)——不重派。
        # 残缺/远未来戳(超容差的时钟/TZ 偏斜)算 stale,永不永久新鲜;负窗
        # 内的偏斜按活处理(缺陷 2,见 claim_is_live)。
        if (job.get("schedule") or {}).get("kind") == "once" and claim_is_live(
            job.get("run_claim"), now, self._oneshot_run_claim_ttl(job)
        ):
            return False

        next_run = (
            self._restore_unclaimed_slot(job, scan)
            or job.get("next_run_at")
            or self._recover_missing_next_run(job, scan)
        )
        if not next_run:
            return False
        raw_next_run_dt = datetime.fromisoformat(next_run)
        d = _DueJob(
            job,
            scan,
            next_run,
            raw_next_run_dt,
            _ensure_aware(raw_next_run_dt, zone),
            zone,
        )
        kind = d.kind
        recurring = kind in {"cron", "interval"}
        # 有意对存储原值做字符串精确比对:trigger_job 把同一 isoformat 串戳进
        # 两个字段,next_run_at 的任何改写(edit、重锚、fire-claim 推进)都必须
        # 使标记失效。别用 _ensure_aware 规整来「修」它。
        manual_run = job.get("manual_run_at") == next_run
        from myssia.cron import occurrences

        if not manual_run and occurrences.completed_occurrence(
            job, next_run, ledger=self.ledger
        ):
            new_next = d.recompute_next() if recurring else None
            if new_next:
                scan.persist(job["id"], next_run_at=new_next)
            return False
        if kind == "cron" and not manual_run and self._repair_timezone_shifted_cron(d):
            return False
        d.next_run_dt = self._rearm_stale_error_recurring(d)
        if _instant_after(d.next_run_dt, now):
            return False

        # 只有派发快照携带此字段;绝不从之后的戳推断。
        job["_scheduled_instant"] = (
            None
            if manual_run
            else occurrences.scheduled_instant(job.get("next_run_at"))
        )

        if not manual_run and kind == "cron" and self._reanchor_stale_cron(d):
            return False
        grace = _compute_grace_seconds(d.schedule)
        if (
            not manual_run
            and recurring
            and self._fast_forward_missed_recurring(d, grace)
        ):
            return False
        if kind == "once":
            if self._retire_expired_oneshot(d) or self._oneshot_dispatch_limit_reached(
                job, scan
            ):
                return False
            # 为 run 的**全程**持久认领 one-shot:同一存储上的第二个调度进程不得
            # 在途重派,固定窗口推进 next_run_at 对活过 tick 的 run 不够。他进程
            # 见新鲜认领即跳;mark_job_run 清除。TTL 只覆盖死掉的 tick。
            claim = {"at": now.isoformat(), "by": machine_id()}
            job["run_claim"] = claim
            scan.persist(job["id"], run_claim=claim)

        # 错过可见性:持久化计划 vs 实际派发时序,让独立 CLI 进程能展示迟到
        # 补发。仅 recurring——过期 one-shot 上面已退役;手动触发不迟到。
        if not manual_run and recurring:
            lateness = max(0.0, _elapsed_seconds(now, d.next_run_dt))
            # See #99879(上游引):忙碌分钟级 ticker 滑几分是正常节律。
            dispatch_stamp = {
                "scheduled_at": next_run,
                "dispatched_at": now.isoformat(),
                "lateness_seconds": round(lateness, 1),
                "kind": _classify_dispatch_lateness(lateness, grace),
            }
            job["last_dispatch"] = dispatch_stamp
            # tick 在任何 fire 认领存在**之前**就把 next_run_at 推过该
            # occurrence;戳在进程死于该窗口时存活,槽被恢复而非丢失。
            scan.persist(
                job["id"],
                last_dispatch=dispatch_stamp,
                pending_slot=occurrences.pending_slot_stamp(next_run, now),
            )
        return True


# ---------------------------------------------------------------------------
# cron 栅格判定(D1:CronTrigger 版的上游 croniter get_prev 等价物)
# ---------------------------------------------------------------------------


def _cron_next_run_matches_expr(schedule: dict[str, Any], dt: datetime) -> bool:
    """*dt* 是否落在 schedule 当前 cron expr 的栅格上(秒级容差)。

    上游用 croniter(expr, dt+1s).get_prev == dt(H:1100);croniter 以起始
    时刻**自身的 UTC 偏移**为工作偏移(H:1192 注释)。CronTrigger 的等价
    形态:以 *dt* 的偏移构造 fixed-offset 时区的 trigger,再取
    ``get_next_fire_time(None, dt-1s)``——严格后继射点恰为 *dt* 本身 ⟺ dt
    在栅格上。expr 缺失/无法构造一律 True(fail-open:算不出的 expr 绝不当
    离栅处理,免得把射点吞掉)。"""
    if schedule.get("kind") != "cron":
        return True
    expr = schedule.get("expr")
    if not expr:
        return True
    try:
        trigger = CronTrigger.from_crontab(
            _normalize_cron_expr(str(expr)), timezone=dt.tzinfo or timezone.utc
        )
    except (TypeError, ValueError):
        return True
    previous = trigger.get_next_fire_time(None, dt - timedelta(seconds=1))
    return previous is not None and abs((previous - dt).total_seconds()) < 1.0


def _classify_stale_cron_next_run(
    schedule: dict[str, Any],
    raw_next_run_dt: datetime,
    next_run_dt: datetime,
) -> str:
    """解释存储的 ``next_run_at`` 为何错过当前 cron 栅格;两种成因要相反
    处置(上游 H:1118)。

    - ``"expr_edit"``:直接改 jobs.json 换了 expr 而 next_run_at 还是旧栅格
      (#93049)——重锚**不发**;
    - ``"timezone_migration"``:仅偏移表示变了(遗留 UTC 行规整进配置时区)
      ——当编辑处理会吞掉从未发的到期 occurrence,判迁移则**发**。

    判别式:规整移动了墙钟 **且** 存储射点自己的墙钟是合法射点(偏移一致时
    真编辑永远读不成迁移)。
    """
    if _cron_next_run_matches_expr(schedule, next_run_dt):
        return "match"
    wall_clock_shifted = raw_next_run_dt.replace(tzinfo=None) != next_run_dt.replace(
        tzinfo=None
    )
    if wall_clock_shifted and _cron_next_run_matches_expr(schedule, raw_next_run_dt):
        return "timezone_migration"
    return "expr_edit"


def _schedule_cadence_with_zone(
    schedule: dict[str, Any],
    zone: ZoneInfo,
) -> Optional[float]:
    """``_schedule_cadence_seconds`` 的带时区直通(job 时区版;上游经全局
    配置时区,cron 差值随基准时刻浮动可接受)。"""
    from myssia.cron import schedule as cron_schedule

    return cron_schedule._schedule_cadence_seconds(schedule, tz=zone)  # noqa: SLF001 同包私有
