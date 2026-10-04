"""监督守护线程 + 常驻 ticker 循环(serve / 桌面 sidecar 共用)。

MYIA 移植重写自 Hermes(NousResearch/Hermes-Agent,MIT;上游路径
``~/.hermes/hermes-agent/cron/``):

- ``cron/scheduler_thread.py``(64 行全文,2026-10-04 HEAD)——
  :class:`SupervisedTickerThread` 蓝本。上游背景(#111010):gateway 把
  ticker 跑在裸 daemon 线程上,``start`` 内部逐 tick 兜底保活,但线程本体
  一旦死掉没人能发现——gateway 继续服务、``ticker_heartbeat`` 冻结、
  job 不再发直到重启。监督层就是缺失的外壳:宿主每周期问一次
  ``restart_if_dead``,复活死在关停请求之外的 ticker。
- ``cron/scheduler_provider.py`` 的 ``InProcessCronScheduler.start`` 单
  profile 循环段(H:438-532)——:func:`run_ticker_loop` 蓝本:启动恢复 +
  首个心跳 → 守护循环(tick → 逐轮心跳,成功才盖 success 戳、错误持久化
  给独立进程的 ``cron status`` → 重锚等待)。上游的 multiplex profile/
  EMFILE 退避/can_dispatch 泄流闸(MYIA 无 gateway 泄流面)不搬;
  ``CronTickYielded`` 随 stale-code yield(D8)不搬。

MYIA 适配(任务 10-04-hermes-cron,非照抄处仅此):

- ``run_ticker_loop`` 收显式 :class:`~myia.cron.jobs.CronJobs` 与
  ``execute_job``/``dispatch_gate`` 透传(执行体注入与宿主互斥钩子见
  :mod:`myia.cron.tick`;CLI ``cron serve`` 传 None,B3 sidecar 接
  ``run_busy`` 单飞锁)。
- 上游循环把 provider ``start`` 整体包进监督线程,gateway 另有 housekeeping
  周期性 ``restart_if_dead``;MYIA 的宿主(serve 主循环 / sidecar)负责
  周期性调 :meth:`SupervisedTickerThread.restart_if_dead`。
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable, Mapping, Optional

from myia.cron.jobs import CronJobs
from myia.cron.tick import DispatchGate, JobRunner, tick

logger = logging.getLogger(__name__)

__all__ = [
    "DEFAULT_TICK_INTERVAL_SECONDS",
    "SupervisedTickerThread",
    "run_ticker_loop",
]

#: tick 间隔秒(F2.1:60s tick;``cron serve --interval`` 可覆写)。
DEFAULT_TICK_INTERVAL_SECONDS = 60.0


class SupervisedTickerThread:
    """``threading.Thread`` 形句柄,``restart_if_dead`` 复活死掉的 ticker。

    行为照抄上游 ``cron/scheduler_thread.py``:目标函数以异常逃逸才置
    ``_crashed``(一个**有意返回**的目标不是死 ticker——外部 provider 的
    start 本来就返回);stop 已请求、线程仍活、未崩过 → 不复活;复活计
    数 ``restarts`` 随 ERROR 日志留痕(停摆期间的 job 不会补发,日志明示
    去查错误日志)。"""

    def __init__(
        self,
        target: Callable[..., Any],
        *,
        args: tuple = (),
        kwargs: Optional[Mapping[str, Any]] = None,
        stop_event: threading.Event,
        name: str = "cron-ticker",
    ) -> None:
        self._target, self._args, self._kwargs = target, args, dict(kwargs or {})
        self._stop_event, self._name = stop_event, name
        self._crashed = False
        self._thread = self._spawn()
        self.restarts = 0

    def _run(self) -> None:
        try:
            self._target(*self._args, **self._kwargs)
        except BaseException:
            self._crashed = True
            raise

    def _spawn(self) -> threading.Thread:
        self._crashed = False
        return threading.Thread(target=self._run, daemon=True, name=self._name)

    def start(self) -> None:
        self._thread.start()

    def is_alive(self) -> bool:
        return self._thread.is_alive()

    def join(self, timeout: Optional[float] = None) -> None:
        self._thread.join(timeout)

    def restart_if_dead(self) -> bool:
        """ticker 死于非关停请求时复活;True = 本次复活了。"""
        if self._stop_event.is_set() or self._thread.is_alive() or not self._crashed:
            return False
        self.restarts += 1
        logger.error(
            "Cron ticker thread %r died without a stop request; restarting "
            "(restart #%d). Scheduled jobs did not fire while it was down — "
            "check the tick error log for the escaping exception.",
            self._name,
            self.restarts,
        )
        self._thread = self._spawn()
        self._thread.start()
        return True


def _guarded_store_write(
    action: Callable[..., Any], what: str, *args: Any, **kwargs: Any
) -> None:
    """marker 写失败绝不带着 ticker 线程走(上游 provider 同名助手语义)。"""
    try:
        action(*args, **kwargs)
    except Exception:
        logger.error("Cron %s store write failed", what, exc_info=True)


def run_ticker_loop(
    cron: CronJobs,
    stop_event: threading.Event,
    *,
    interval: float = DEFAULT_TICK_INTERVAL_SECONDS,
    execute_job: Optional[JobRunner] = None,
    dispatch_gate: Optional[DispatchGate] = None,
) -> None:
    """常驻循环:阻塞直至 *stop_event* 置位(``cron serve`` / sidecar 的
    ticker 目标函数;上游 ``InProcessCronScheduler.start`` 单 profile 段)。

    启动恢复 + 首个心跳先于循环——让 ``cron status`` 立即看到活 ticker;
    启动期故障只记错误,不带走线程(#111010)。每轮:tick(同步;锁被
    他宿主持有时静默 0)→ 心跳(干净 tick 才盖 success 戳、清错误 marker,
    让 status 分得清「活着但在失败」与「真在发」,#32612/#32895)→ 等待
    下一锚点(tick 超期/宿主休眠后重锚,防零长睡眠连发,#114467)。"""
    logger.info("Cron ticker started (interval=%.0fs)", interval)

    # 启动恢复与首个心跳:中断标记 + 活性凭证,必须在任何等待之前。
    try:
        recovered = cron.ledger.recover_interrupted_executions()
        if recovered:
            logger.warning(
                "Marked %d interrupted cron execution(s) unknown after restart",
                recovered,
            )
        cron.record_ticker_heartbeat()
    except BaseException as exc:
        # BaseException:启动恢复不许带走 ticker 线程;关停由 stop_event 驱动。
        logger.error("Cron startup recovery error: %s", exc, exc_info=True)
        _guarded_store_write(
            cron.record_ticker_error, "startup error", f"{type(exc).__name__}: {exc}"
        )

    next_tick = time.monotonic()
    while not stop_event.is_set():
        ok = False
        try:
            tick(
                cron,
                verbose=False,
                execute_job=execute_job,
                dispatch_gate=dispatch_gate,
            )
            ok = True
        except BaseException as exc:
            # BaseException 而非 Exception(#32612):行为不端的 SystemExit 不许
            # 无声杀掉 ticker;KeyboardInterrupt 故意吞——关停由 stop_event 驱动,
            # 吞掉后重查 stop_event 让关停干净。
            logger.error("Cron tick error: %s", exc, exc_info=True)
            _guarded_store_write(
                cron.record_ticker_error, "tick error", f"{type(exc).__name__}: {exc}"
            )
        _guarded_store_write(cron.record_ticker_heartbeat, "heartbeat", success=ok)
        if ok:
            _guarded_store_write(cron.clear_ticker_error, "error clear")
        next_tick += interval
        now = time.monotonic()
        if next_tick < now:
            next_tick = now + interval
        stop_event.wait(max(0.0, next_tick - now))
    logger.info("Cron ticker stopped")
