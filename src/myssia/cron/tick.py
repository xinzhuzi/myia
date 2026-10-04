"""tick 入场与派发:文件锁单飞、先推进后派发(at-most-once)、按 db 分组派发。

MYIA 移植重写自 Hermes(NousResearch/Hermes-Agent,MIT;上游路径
``~/.hermes/hermes-agent/cron/``):

- ``cron/scheduler_tick.py``(121 行全文,2026-10-04 HEAD)——本模块 ``tick``
  的全时序蓝本:tick 锁 → estop → reap 死属主 → due 扫描 → sweep → 空转心跳
  → **先 advance_next_runs 再派发** → 释放锁;
- ``cron/scheduler.py`` 的 tick 支撑段——``_acquire_tick_lock`` H:4100 /
  ``_release_tick_lock`` H:4136(真 OSError 绝不放行成「锁被占」,#87644)、
  ``_maybe_reap_dead_owners`` H:4146(300s 节流)、
  ``_sweep_stale_inflight_for_tick`` H:4178(见下方步骤 5 的 MYIA 形态)、
  ``_process_due_job`` H:4224(派发单 job 主干)、``_submit_with_guard``
  H:4239(在途去重 + 账本行 + 派发失败清理)、
  ``_run_with_fire_claim_heartbeat`` H:2706(fire 认领心跳保活);
- ``cron/scheduler_provider.py`` 的 ``InProcessCronScheduler.start`` 循环段
  H:438-532——是 :mod:`myia.cron.ticker` 的 ``run_ticker_loop`` 蓝本,非本模块。

MYIA 适配(任务 10-04-hermes-cron design §3.1/§3.3/§6,非照抄处仅此):

- **实例化**:上游 tick 经 profile 全局解析存储;MYIA 显式传
  :class:`~myia.cron.jobs.CronJobs` 门面(存储 + 账本 + 可注入时钟同根)。
- **D13 派发分组**:上游无界并行池逐一派发;MYIA **同 db 的 job 串行、
  不同 db 并行**——按 ``db_path`` 覆写(缺省回落数据根)分组,组内顺序
  执行,组间 ``ThreadPoolExecutor(max_workers=min(4, cpu))``。理由:管线
  并发写同 db 未验证(ground-truth W7)。
- **执行体注入**:上游在派发内联 agent 运行时;MYIA 的执行体是注入的
  ``execute_job`` 钩子(Stage A 为 no-op 测试桩,B1 的
  :mod:`myia.cron.runner` 子进程模型替换),返回
  ``(success, error, delivery_error)`` 三元组供 :meth:`mark_job_run` 记账。
- **宿主互斥钩子**(grill Q2):``dispatch_gate`` 在 fire claim **之前**逐
  job 检查;False = 宿主忙(桌面 ``run_busy`` 单飞锁被用户手点占用)——
  跳过本 fire(advance 已消耗槽,不排队不回滚,与 at-most-once 一致),
  ``last_status="skipped_busy"``。``cron.skipped`` 事件由宿主(B3)发,
  本层不耦合 sidecar。
- **步骤 5 sweep 的 MYIA 形态**:design §3.1「清理超龄 fire_claim」——把
  due job 名下已证不活的 ``fire_claim`` 从 jobs.json 清掉。上游对等的
  in-flight 集强制回收(``_running_since``/``_running_futures`` 机器)未随
  A4 移植(MYIA 在途集是进程内裸集、worker ``finally`` 必释、随进程消亡),
  故不搬。
- **不搬**(design §6):stale-code yield(D8)、worktree 维护(D8)、
  bot_chat_delivery drain(D5)、MCP 孤儿清扫(D8)、detached worker(D3)、
  上游异步派发(``sync=False`` 非阻塞提交)——MYIA tick 同步等派发收尾,
  serve/sidecar 的专用循环天然容纳;解释器关断守卫随异步派发裁。
- **空转心跳**(design §3.1 步骤 6):上游 tick() 本身不写 marker(循环层
  写);MYIA 的空转 tick 落一次 ``ticker_heartbeat(success=True)``,让
  ``cron status`` 在仅有手动 tick 的机器上也有新鲜凭证。
"""

from __future__ import annotations

import concurrent.futures
import contextlib
import errno
import logging
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import IO, Any, Callable, Collection, Optional, Text, Tuple

from myia.cron.constants import FIRE_CLAIM_TTL_SECONDS
from myia.cron.jobs import (
    CronJobs,
    claim_is_live,
    job_running_in_this_process,
    release_running_job,
    try_register_running_job,
)

try:  # 跨平台文件锁:Unix fcntl / Windows msvcrt(上游同款守卫导入)
    import fcntl  # noqa: F401  (可能缺,保名字存在)
except ImportError:  # pragma: no cover - Windows
    fcntl = None  # type: ignore[assignment]
try:
    import msvcrt  # type: ignore[import-not-found]  # noqa: F401
except ImportError:  # pragma: no cover - POSIX
    msvcrt = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

__all__ = [
    "DEAD_OWNER_REAP_INTERVAL_SECONDS",
    "DEFAULT_DB_NAME",
    "DispatchGate",
    "FIRE_CLAIM_HEARTBEAT_GRACE_SECONDS",
    "FIRE_CLAIM_HEARTBEAT_SECONDS",
    "FIRE_CLAIM_MISS_CONFIRM_SECONDS",
    "JobRunner",
    "MAX_PARALLEL_DB_GROUPS",
    "TICK_LOCK_NAME",
    "tick",
]

#: tick 文件锁名(design §3.1 步骤 1:``<cron_dir>/tick.lock``;上游为
#: ``.tick.lock``,命名从 design)。多宿主(serve + sidecar + 手动 tick)
#: 全进程单飞:抢不到的静默让路。
TICK_LOCK_NAME = "tick.lock"

#: 数据根缺省 db 名(``--db`` 缺省 ``myia.db``;db_path 无覆写的 job 归
#: 默认组,ground-truth B9)。
DEFAULT_DB_NAME = "myia.db"

#: 死属主回收节流(上游 H:4027 同值):recover 要开账本,空闲 60s tick
#: 不必每轮付一次连接;测试可清 ``_last_dead_owner_reap_at`` 强制下一轮回收。
DEAD_OWNER_REAP_INTERVAL_SECONDS = 300.0
_last_dead_owner_reap_at: dict[str, float] = {}

#: D13 并行池上限:不同 db 组间并行,帽 = min(4, cpu)。
MAX_PARALLEL_DB_GROUPS = 4

#: fire 认领心跳节奏与宽限(上游 H:1436-1438 同值;TTL 300s 内保活长执行)。
FIRE_CLAIM_HEARTBEAT_SECONDS = 60.0
FIRE_CLAIM_HEARTBEAT_GRACE_SECONDS = FIRE_CLAIM_HEARTBEAT_SECONDS * 3
#: 心跳失联的二次采样确认间隔(一次 miss 是采样不是判决,上游 #113357)。
FIRE_CLAIM_MISS_CONFIRM_SECONDS = 1.0

#: 执行体契约(B1 runner 替换;A6 缺省 no-op 桩):
#: 入参 = 派发快照(含 ``execution_id``/``_scheduled_instant``),
#: 返回 ``(success, error, delivery_error)``——delivery_error 分立才有
#: ``last_status="delivery_failed"`` 三态(F1.7)。
JobRunner = Callable[[dict[str, Any]], Tuple[bool, Optional[str], Optional[str]]]

#: 宿主互斥钩子(Q2 注入点):入参 = 派发快照;False = 宿主忙,跳过本 fire。
DispatchGate = Callable[[dict[str, Any]], bool]


# ---------------------------------------------------------------------------
# tick 文件锁(上游 _acquire_tick_lock/_release_tick_lock H:4100-4144 照抄)
# ---------------------------------------------------------------------------


def _is_lock_contention_errno(err: OSError) -> bool:
    """*err* 是否意味着「另一 ticker 持锁」而非真故障(POSIX flock:
    EWOULDBLOCK/EAGAIN、个别 NFS 的 EACCES;msvcrt: EACCES/EDEADLK)。
    其余——尤其 fd 耗尽的 EMFILE/ENFILE——必须上抛,绝不当锁竞争吞掉
    (否则调度器看着健康、job 永远不再跑,#87644)。"""
    if err.errno is None:
        return False
    if fcntl is not None:
        return err.errno in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EACCES)
    if msvcrt is not None:  # pragma: no cover - Windows
        return err.errno in (errno.EACCES, errno.EDEADLK)
    return False


def _acquire_tick_lock(lock_file: Path) -> Optional[IO[Text]]:
    """开 + 非阻塞锁 tick 文件;真锁竞争返回 None,真 OSError 上抛(让
    ticker 循环记一次失败 tick 而非静默装健康)。"""
    lock_fd: Optional[IO[Text]] = None
    try:
        lock_fd = open(lock_file, "w", encoding="utf-8")
        if fcntl is not None:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        elif msvcrt is not None:  # pragma: no cover - Windows
            msvcrt.locking(lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
        return lock_fd
    except OSError as exc:
        if lock_fd is not None:
            with contextlib.suppress(OSError):
                lock_fd.close()
            if _is_lock_contention_errno(exc):
                logger.debug("Tick skipped — another instance holds the lock")
                return None
        logger.error("Cron tick could not acquire tick lock: %s", exc)
        raise


def _release_tick_lock(lock_fd: IO[Text]) -> None:
    if fcntl is not None:
        with contextlib.suppress((OSError, IOError)):
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
    elif msvcrt is not None:  # pragma: no cover - Windows
        with contextlib.suppress((OSError, IOError)):
            msvcrt.locking(lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
    lock_fd.close()


# ---------------------------------------------------------------------------
# 死属主回收与超龄 fire_claim 清扫(design §3.1 步骤 3/5)
# ---------------------------------------------------------------------------


def _maybe_reap_dead_owners(cron: CronJobs) -> None:
    """把属主可证已死、却停在 claimed/running 的账本行终态化 unknown(#86721:
    回收只在调度器启动时跑过,会让崩溃过的行永远堵住该 job)。开账本有成本,
    按 cron 目录节流。"""
    key = str(cron.store.cron_dir)
    reap_now = time.monotonic()
    last = _last_dead_owner_reap_at.get(key)
    if last is not None and reap_now - last < DEAD_OWNER_REAP_INTERVAL_SECONDS:
        return
    _last_dead_owner_reap_at[key] = reap_now
    try:
        # D14(B1):先杀宿主崩溃遗留的孤儿子进程再通用恢复——孤儿杀除独立于
        # 记账(行可能已被启动恢复先行标 unknown,进程组仍要杀)。
        from myia.cron.runner import (
            reap_orphaned_subprocesses,
        )  # deferred: 避免 tick → runner 顶层环

        reap_orphaned_subprocesses(cron)
        reclaimed = cron.ledger.recover_interrupted_executions()
        if reclaimed:
            logger.warning(
                "Reclaimed %d cron execution(s) whose owner process died "
                "before reaching a terminal state (marked unknown)",
                reclaimed,
            )
    except Exception as reap_exc:
        logger.debug("Dead-owner execution reclaim failed: %s", reap_exc)


def _sweep_stale_fire_claims(
    cron: CronJobs, due_jobs: Collection[dict[str, Any]]
) -> int:
    """派发前清掉 due job 名下**已证不活**的 ``fire_claim``(design §3.1
    步骤 5):崩溃 tick 留下的超龄认领会先于去重闸被强制放掉,而不是吃到
    下一次重启。活认领(TTL 内且属主未证死)与本进程在途 job 的认领不动。
    正确性上与 ``claim_job_for_fire`` 的锁内覆写冗余——此处让 jobs.json
    早点诚实。尽力而为:失败只告警,绝不弄崩 tick。"""
    ids = {
        str(job.get("id"))
        for job in due_jobs
        if isinstance(job, dict) and job.get("id")
    }
    if not ids:
        return 0
    now = cron._now()  # noqa: SLF001 同包私有(注入时钟口径,jobs.py 先例)
    cleared = 0
    try:
        with cron.store.jobs_lock():
            jobs = cron.store.load_jobs()
            for job in jobs:
                jid = str(job.get("id") or "")
                if jid not in ids or not job.get("fire_claim"):
                    continue
                if job_running_in_this_process(jid):
                    continue  # 本进程在途:worker 自己保活,不越权清
                if not claim_is_live(
                    job.get("fire_claim"), now, FIRE_CLAIM_TTL_SECONDS
                ):
                    job["fire_claim"] = None
                    cleared += 1
            if cleared:
                cron.store.save_jobs(jobs)
    except Exception as exc:
        logger.warning("Stale fire-claim sweep failed: %s", exc)
        return 0
    if cleared:
        logger.info(
            "Cleared %d stale fire claim(s) from jobs.json before dispatch", cleared
        )
    return cleared


# ---------------------------------------------------------------------------
# tick 主体(design §3.1;上游 scheduler_tick.py 全时序)
# ---------------------------------------------------------------------------


def _default_execute_job(
    job: dict[str, Any],
) -> Tuple[bool, Optional[str], Optional[str]]:
    """Stage A 占位执行体:不做任何事、记成功。真执行体是 B1 的
    :mod:`myia.cron.runner`(spawn ``myia run --json`` 子进程,D11);生产
    宿主(serve/sidecar)必须注入——WARNING 让误用可见。"""
    logger.warning(
        "Job '%s': cron runner not injected (Stage A no-op stub) — recording "
        "no-op success; the real runner lands with myia.cron.runner (B1).",
        job.get("name") or job.get("id"),
    )
    return True, None, None


def tick(
    cron: CronJobs,
    *,
    verbose: bool = True,
    execute_job: Optional[JobRunner] = None,
    dispatch_gate: Optional[DispatchGate] = None,
    max_workers: Optional[int] = None,
) -> int:
    """检查并跑全部到期 job;返回处理的 job 数(0 = 空转或锁被他人持有)。

    文件锁全进程单飞:serve ticker、sidecar ticker、手动 ``cron tick``
    同一时刻恰一个在跑;抢不到锁**静默返回 0**(手动 tick 与 daemon 并存
    安全)。时序(design §3.1):

    1. tick 文件锁(抢不到 → return 0);
    2. estop(``paused.marker`` 全局急停):跳过派发,绝不动在途 run;
    3. reap 死属主(300s 节流);
    4. ``get_due_jobs()``(含积压坍缩只补一发);
    5. sweep 超龄 fire_claim;
    6. 空转:更新心跳标记,return 0;
    7. **先** ``advance_next_runs``(at-most-once:run 中途崩溃不在重启时
       重发;recurring 盖 pending_slot 戳在 get_due_jobs 内已落);
    8. 派发:同 db 串行、不同 db 并行(D13);逐 job = 宿主互斥钩子 →
       fire claim → executions claimed → 执行体 → mark_job_run;
    9. 释放锁。

    ``execute_job``/``dispatch_gate`` 语义见模块 docstring;``max_workers``
    供测试覆写并行池上限(缺省 ``min(4, cpu)``)。
    """
    runner: JobRunner = execute_job if execute_job is not None else _default_execute_job
    cron.store.ensure_dirs()
    lock_fd = _acquire_tick_lock(cron.store.cron_dir / TICK_LOCK_NAME)
    if lock_fd is None:
        return 0
    try:
        # `cron pause --all` ESTOP:跳过派发,绝不动在途 run(Q4)。
        if cron.is_estopped():
            (logger.info if verbose else logger.debug)(
                "%s - Cron estopped (paused.marker); skipping dispatch",
                datetime.now().strftime("%H:%M:%S"),
            )
            return 0

        _maybe_reap_dead_owners(cron)
        due_jobs = cron.get_due_jobs()
        _sweep_stale_fire_claims(cron, due_jobs)

        if not due_jobs:
            # 空转也更新心跳(design §3.1 步骤 6;上游只有循环层写 marker):
            # 无 due 的干净 tick 就是成功 tick。
            if verbose:
                logger.info("%s - No jobs due", datetime.now().strftime("%H:%M:%S"))
            cron.record_ticker_heartbeat(success=True)
            return 0
        if verbose:
            logger.info(
                "%s - %d job(s) due",
                datetime.now().strftime("%H:%M:%S"),
                len(due_jobs),
            )

        # ★ 先推进 next_run_at(at-most-once)再派发:锁内、任何执行开始前
        # (上游 scheduler_tick.py:80-83 同款注释)。running job 的再推进
        # 维持 grace 窗口;mark_job_run 完成时覆写;与 claim_job_for_fire
        # 的认领时推进复合。one-shot 不动(run_claim 已在 get_due_jobs 戳)。
        cron.advance_next_runs([job["id"] for job in due_jobs])

        return _dispatch_due_jobs(
            cron,
            due_jobs,
            execute_job=runner,
            dispatch_gate=dispatch_gate,
            max_workers=max_workers,
            verbose=verbose,
        )
    finally:
        _release_tick_lock(lock_fd)


# ---------------------------------------------------------------------------
# 派发(D13 分组;上游 _process_due_job H:4224 + _submit_with_guard H:4239)
# ---------------------------------------------------------------------------


def _job_db_key(cron: CronJobs, job: dict[str, Any]) -> str:
    """job 的 db 归组键:``db_path`` 覆写(缺省 = 数据根 ``myia.db``),
    绝对化后比较(W7:同 db 派发必须互斥,相对路径按 cwd 归一)。"""
    override = job.get("db_path")
    if isinstance(override, str) and override.strip():
        return os.path.abspath(os.path.expanduser(override.strip()))
    return os.path.abspath(str(cron.store.data_root / DEFAULT_DB_NAME))


def _dispatch_due_jobs(
    cron: CronJobs,
    due_jobs: list[dict[str, Any]],
    *,
    execute_job: JobRunner,
    dispatch_gate: Optional[DispatchGate],
    max_workers: Optional[int],
    verbose: bool,
) -> int:
    """D13 派发:按 db 分组——组内(同 db)顺序执行,组间(不同 db)
    ``ThreadPoolExecutor(max_workers=min(4, cpu))`` 并行;单组免池内联。
    返回处理成功的 job 数(上游 sum(bool) 同口径:处理了但失败的算 0,
    在途去重跳过的不计)。"""
    groups: dict[str, list[dict[str, Any]]] = {}
    for job in due_jobs:  # dict 保序:组内顺序 = due 顺序
        groups.setdefault(_job_db_key(cron, job), []).append(job)

    if max_workers is None:
        cap = min(MAX_PARALLEL_DB_GROUPS, os.cpu_count() or 1)
    else:
        cap = max(1, int(max_workers))
    if verbose:
        logger.info(
            "Running %d job(s) across %d db group(s) (max_workers=%d)",
            len(due_jobs),
            len(groups),
            min(len(groups), cap),
        )

    if len(groups) == 1:
        # 单组:串行是组内语义本身,免一次线程跳板。
        return _dispatch_group(
            cron,
            next(iter(groups.values())),
            execute_job=execute_job,
            dispatch_gate=dispatch_gate,
        )

    processed = 0
    pool = concurrent.futures.ThreadPoolExecutor(
        max_workers=min(len(groups), cap), thread_name_prefix="cron-dispatch"
    )
    try:
        futures = [
            pool.submit(
                _dispatch_group,
                cron,
                group_jobs,
                execute_job=execute_job,
                dispatch_gate=dispatch_gate,
            )
            for group_jobs in groups.values()
        ]
        for future in concurrent.futures.as_completed(futures):
            try:
                processed += future.result()
            except Exception as exc:  # 一组崩了绝不拖垮其余组(单组内部已逐 job 隔离)
                logger.error("Cron dispatch group failed: %s", exc, exc_info=exc)
    finally:
        pool.shutdown(wait=True)
    return processed


def _dispatch_group(
    cron: CronJobs,
    group_jobs: list[dict[str, Any]],
    *,
    execute_job: JobRunner,
    dispatch_gate: Optional[DispatchGate],
) -> int:
    """同 db 组内**串行**逐 job 派发(D13);单 job 崩溃只计失败,不拖垮
    同组兄弟与整个 tick。"""
    processed = 0
    for job in group_jobs:
        try:
            outcome = _guarded_dispatch(
                cron, job, execute_job=execute_job, dispatch_gate=dispatch_gate
            )
        except Exception:
            logger.exception(
                "Cron dispatch crashed for job %r", job.get("name") or job.get("id")
            )
            continue
        if outcome:
            processed += 1
    return processed


def _clear_run_claim_best_effort(cron: CronJobs, job: dict[str, Any]) -> None:
    """派发失败路径的尽力 ``run_claim`` 清理(上游 #86522):one-shot 的
    run_claim 到不了 mark_job_run 就会堵住重派发到 TTL 过期;降级路径
    (关断、fd 耗尽)上清理本身可能抛——TTL 过期胜过崩 tick,只告警。"""
    schedule = job.get("schedule")
    if not (isinstance(schedule, dict) and schedule.get("kind") == "once"):
        return
    try:
        cron.clear_run_claim(str(job.get("id") or ""))
    except Exception as claim_err:
        logger.warning(
            "Could not clear run_claim for job '%s' after dispatch failure: %s "
            "(claim will expire at TTL)",
            job.get("name") or job.get("id"),
            claim_err,
        )


def _guarded_dispatch(
    cron: CronJobs,
    job: dict[str, Any],
    *,
    execute_job: JobRunner,
    dispatch_gate: Optional[DispatchGate],
) -> Optional[bool]:
    """在途去重守卫 + 账本行创建(上游 ``_submit_with_guard`` 的 D13 形态:
    无池队列,组内即席执行)。已在途 → None(跳过,不计处理数);执行行
    创建失败 → 释放守卫 + 清 run_claim + None。worker ``finally`` 释守卫。"""
    job_id = str(job.get("id") or "")
    label = job.get("name") or job_id
    if not job_id:
        return None
    if not try_register_running_job(job_id):
        logger.info("Job '%s' already running — skipping", label)
        return None
    try:
        # 派发前先落一行 claimed(审计在先;source='tick',design §2.3)。
        execution = cron.ledger.create_execution(
            job_id, source="tick", scheduled_instant=job.get("_scheduled_instant")
        )
    except Exception as execution_err:
        release_running_job(job_id)
        _clear_run_claim_best_effort(cron, job)
        logger.exception(
            "Job '%s' not dispatched: execution creation failed: %s",
            label,
            execution_err,
        )
        return None
    dispatched = dict(job, execution_id=execution["id"])
    try:
        return _process_due_job(
            cron, dispatched, execute_job=execute_job, dispatch_gate=dispatch_gate
        )
    finally:
        release_running_job(job_id)


def _finish_execution_best_effort(
    cron: CronJobs, execution_id: str, *, success: bool, error: Optional[str]
) -> None:
    """账本终态尽力写;失败只告警(账本行过期会被死属主回收兜底)。"""
    try:
        cron.ledger.finish_execution(execution_id, success=success, error=error)
    except Exception:
        logger.warning(
            "Failed to finish execution record %s", execution_id, exc_info=True
        )


def _mark_job_run_owner_fenced(
    cron: CronJobs,
    job_id: str,
    success: bool,
    error: Optional[str],
    delivery_error: Optional[str],
    fire_owner: str,
    *,
    status: Optional[str] = None,
) -> bool:
    """:meth:`CronJobs.mark_job_run` 的 owner-fence 形态:fire 认领属主已
    换人时丢弃过期完成回据(返回 False)。``status`` 透传显式覆写
    (如 ``"skipped_busy"``,Q2)。"""
    kwargs: dict[str, Any] = {"status": status} if status else {}
    if fire_owner:
        kwargs["expected_fire_owner"] = fire_owner
    return cron.mark_job_run(
        job_id, success, error, delivery_error=delivery_error, **kwargs
    )


def _run_with_fire_claim_heartbeat(
    cron: CronJobs, job: dict[str, Any], execute_job: JobRunner
) -> Tuple[bool, Optional[str], Optional[str]]:
    """执行体运行期间保活本 fire 认领(上游 H:2706 的同步形态)。

    起跑先验一次属主(丢了的认领不再跑,免得给别人的 run 叠一份副作用);
    运行期间 60s 一跳 compare-and-refresh(陈旧 runner 刷不动别人的认领)。
    与上游的差异:上游失联经二次采样确认后**中断**活 agent;MYIA 的同步
    执行体无法中断——失联只停跳 + 告警,过期回据由 ``mark_job_run`` 的
    owner fence 丢弃,不会双记账。"""
    claim = job.get("fire_claim")
    owner = str(claim.get("by") or "") if isinstance(claim, dict) else ""
    if not owner:
        return execute_job(job)
    job_id = str(job.get("id") or "")
    try:
        owns_fire_claim = cron.heartbeat_fire_claim(job_id, expected_owner=owner)
    except Exception:
        logger.warning(
            "Job '%s': initial fire_claim validation failed", job_id, exc_info=True
        )
        return (
            False,
            "Fire claim ownership could not be validated before execution started.",
            None,
        )
    if not owns_fire_claim:
        logger.warning(
            "Job '%s': fire claim ownership was already lost before execution", job_id
        )
        return False, "Fire claim ownership lost before execution started.", None

    stop = threading.Event()

    def _heartbeat_loop() -> None:
        while not stop.wait(FIRE_CLAIM_HEARTBEAT_SECONDS):
            try:
                if cron.heartbeat_fire_claim(job_id, expected_owner=owner):
                    continue
                # 一次 miss 是采样不是判决(#113357):静置后再采一次才算失联。
                if stop.wait(FIRE_CLAIM_MISS_CONFIRM_SECONDS):
                    return
                try:
                    if cron.heartbeat_fire_claim(job_id, expected_owner=owner):
                        continue
                except Exception:
                    logger.debug(
                        "Job '%s': fire_claim heartbeat re-confirm failed",
                        job_id,
                        exc_info=True,
                    )
                logger.warning(
                    "Job '%s': fire claim ownership lost mid-run; this stale run's "
                    "completion will be discarded by the owner fence",
                    job_id,
                )
                return
            except Exception:
                logger.debug(
                    "Job '%s': fire_claim heartbeat failed", job_id, exc_info=True
                )

    heartbeat_thread = threading.Thread(
        target=_heartbeat_loop, daemon=True, name="cron-fire-claim-heartbeat"
    )
    heartbeat_thread.start()
    try:
        return execute_job(job)
    finally:
        stop.set()
        heartbeat_thread.join(timeout=1.0)


def _process_due_job(
    cron: CronJobs,
    job: dict[str, Any],
    *,
    execute_job: JobRunner,
    dispatch_gate: Optional[DispatchGate],
) -> bool:
    """跑**一个** due job 端到端(design §3.1 步骤 8;上游
    ``_process_due_job`` H:4224 + ``_run_one_job_body`` H:3284 的账本骨架):

    宿主互斥钩子(Q2)→ fire claim(TTL=300s 写 jobs.json)→ 有限 one-shot
    派发预认领(#38758)→ claimed→running CAS → 执行体(带认领心跳)→
    ``mark_job_run``(重锚 + repeat 计数 + 终态退役)→ 账本终态。

    True = 已处理(含 claim 竞输/到限跳过等非错误路径);False = 处理中途
    抛了 Exception(已按失败记账)。BaseException 先记账再上抛(否则
    claim_dispatch 已消费的有限 one-shot 会楔死,#73973)。"""
    job_id = str(job["id"])
    label = job.get("name") or job_id
    execution_id = str(job["execution_id"])

    # (a) 宿主侧互斥钩子(Q2):fire claim 之前;advance 已消耗槽,不排队
    # 不回滚。skipped_busy 是成功语义(streak 不动),状态显式覆写。
    if dispatch_gate is not None and not dispatch_gate(job):
        logger.info("Job '%s': host busy — skipping this fire (skipped_busy)", label)
        _mark_job_run_owner_fenced(
            cron, job_id, True, None, None, "", status="skipped_busy"
        )
        _finish_execution_best_effort(
            cron,
            execution_id,
            success=False,
            error="Host busy; fire skipped (skipped_busy)",
        )
        return True

    # (b) fire claim:恰一个竞争者赢(多进程 at-most-once;TTL 让崩溃后的
    # 另一 fire 可回收)。claim 只在 worker 真正开跑时取——排队的租约不会
    # 先过期。CAS 返回持久化后的记录快照(含 _scheduled_instant)。
    claimed = cron.claim_job_for_fire(job_id, return_job=True)
    if not claimed:
        _finish_execution_best_effort(
            cron,
            execution_id,
            success=False,
            error="Fire claim lost; execution was not started.",
        )
        return True
    claimed_job = dict(claimed) if isinstance(claimed, dict) else dict(job)
    claimed_job["execution_id"] = execution_id
    # 到期身份只信派发快照(advance 之后 claim 重算的已是未来射点;
    # jobs.py _evaluate_due_job「绝不从之后的戳推断」注)。
    claimed_job["_scheduled_instant"] = job.get("_scheduled_instant")
    fire_owner = str((claimed_job.get("fire_claim") or {}).get("by") or "")

    # (c) 有限 one-shot 副作用**前**预认领派发:tick 中途死也不无限重发
    # (at-most-times;recurring/无限 repeat 直通,#38758)。
    if not cron.claim_dispatch(job_id):
        logger.info("Job '%s': one-shot dispatch limit reached — skipping", label)
        _finish_execution_best_effort(
            cron,
            execution_id,
            success=False,
            error="Dispatch claim rejected; execution was not started.",
        )
        return True

    # (d) claimed → running,恰一次、副作用开始前:输掉 CAS 说明行已被
    # 回收/换主,本派发作废。
    if cron.ledger.mark_execution_running(execution_id) is None:
        logger.warning(
            "Cron job %s lost execution ownership before start; skipping", job_id
        )
        return True

    marked = False
    try:
        logger.info("Running job '%s' (ID: %s)", label, job_id)
        success, error, delivery_error = _run_with_fire_claim_heartbeat(
            cron, claimed_job, execute_job
        )
        marked = _mark_job_run_owner_fenced(
            cron, job_id, success, error, delivery_error, fire_owner
        )
        if not marked:
            logger.warning(
                "Job '%s': completion discarded (fire claim owner changed or job "
                "removed); not recording a stale receipt",
                label,
            )
        _finish_execution_best_effort(
            cron, execution_id, success=success, error=error or delivery_error
        )
        return True
    except BaseException as exc:
        # BaseException 而非 Exception(#73973):KeyboardInterrupt/SystemExit
        # 不落 mark 会让 claim_dispatch 已消费 repeat.completed 的有限
        # one-shot 楔死(无输出、无错误、无记录直到守卫移除)。先记账再抛。
        err_text = f"{type(exc).__name__}: {exc}"
        logger.error("Error processing job %s: %s", job_id, err_text, exc_info=exc)
        if not marked:
            with contextlib.suppress(Exception):
                _mark_job_run_owner_fenced(
                    cron, job_id, False, err_text, None, fire_owner
                )
        _finish_execution_best_effort(cron, execution_id, success=False, error=err_text)
        if not isinstance(exc, Exception):
            raise
        return False
