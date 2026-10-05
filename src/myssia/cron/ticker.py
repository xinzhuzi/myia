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

- ``run_ticker_loop`` 收显式 :class:`~myssia.cron.jobs.CronJobs` 与
  ``execute_job``/``dispatch_gate`` 透传(执行体注入与宿主互斥钩子见
  :mod:`myssia.cron.tick`;CLI ``cron serve`` 传 None,B3 sidecar 接
  ``run_busy`` 单飞锁)。
- ``heartbeat_scan`` 低频钩子(10-05-cron-heartbeat 收尾件):cron_stale
  心跳告警的兜底直扫——搭车路径(``pipeline._alert_pass`` 尾挂)在 run
  阶段自身异常中断的轮次不扫,ticker 在品类 run 之外独立周期性直扫;
  扫描体由宿主注入(pipeline 侧工厂 ``make_cron_heartbeat_scan``,
  cron/ 零 pipeline 依赖,依赖方向红线不破)。
- 上游循环把 provider ``start`` 整体包进监督线程,gateway 另有 housekeeping
  周期性 ``restart_if_dead``;MYIA 的宿主(serve 主循环 / sidecar)负责
  周期性调 :meth:`SupervisedTickerThread.restart_if_dead`。
"""

from __future__ import annotations

import logging
import threading
import time
from typing import Any, Callable, Mapping, Optional

from myssia.cron.jobs import CronJobs
from myssia.cron.tick import DispatchGate, JobRunner, tick

logger = logging.getLogger(__name__)

__all__ = [
    "DEFAULT_HEARTBEAT_SCAN_INTERVAL_SECONDS",
    "DEFAULT_TICK_INTERVAL_SECONDS",
    "SupervisedTickerThread",
    "run_ticker_loop",
]

#: tick 间隔秒(F2.1:60s tick;``cron serve --interval`` 可覆写)。
DEFAULT_TICK_INTERVAL_SECONDS = 60.0

#: 心跳告警(cron_stale)兜底扫描间隔秒(10-05-cron-heartbeat 收尾件):
#: ticker 直挂路径的节奏,与 tick 间隔解耦——停摆检测不需要 60s 级灵敏度,
#: 5 分钟既够「沉默可告警」又把评估开销压到可忽略(无规则时一次空表 SELECT)。
DEFAULT_HEARTBEAT_SCAN_INTERVAL_SECONDS = 300.0


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


def _guarded_heartbeat_scan(scan: Callable[[], Any]) -> None:
    """心跳扫描失败绝不带着 ticker 线程走(``_guarded_store_write`` 同款惯例)。

    只留 ERROR 日志,**不写 ticker 错误 marker**——marker 面 = ticker 自身
    死活(``cron status`` 活性判读),扫描失败是 cron_stale 评估侧的事,
    写进去会把「ticker 活着但心跳评估在失败」误染成「ticker 在失败」。"""
    try:
        scan()
    except Exception:
        logger.error("Cron heartbeat scan failed", exc_info=True)


def run_ticker_loop(
    cron: CronJobs,
    stop_event: threading.Event,
    *,
    interval: float = DEFAULT_TICK_INTERVAL_SECONDS,
    execute_job: Optional[JobRunner] = None,
    dispatch_gate: Optional[DispatchGate] = None,
    heartbeat_scan: Optional[Callable[[], Any]] = None,
    heartbeat_scan_interval: float = DEFAULT_HEARTBEAT_SCAN_INTERVAL_SECONDS,
) -> None:
    """常驻循环:阻塞直至 *stop_event* 置位(``cron serve`` / sidecar 的
    ticker 目标函数;上游 ``InProcessCronScheduler.start`` 单 profile 段)。

    启动恢复 + 首个心跳先于循环——让 ``cron status`` 立即看到活 ticker;
    启动期故障只记错误,不带走线程(#111010)。每轮:tick(同步;锁被
    他宿主持有时静默 0)→ 心跳(干净 tick 才盖 success 戳、清错误 marker,
    让 status 分得清「活着但在失败」与「真在发」,#32612/#32895)→ 心跳
    告警低频扫描(*heartbeat_scan* 注入时,首轮即扫、其后每
    *heartbeat_scan_interval* 秒;异常隔离沿 ``_guarded`` 惯例)→ 等待
    下一锚点(tick 超期/宿主休眠后重锚,防零长睡眠连发,#114467)。

    Args:
        heartbeat_scan: cron_stale 心跳告警的兜底扫描体(同步可调;
            ``pipeline.make_cron_heartbeat_scan`` 工厂产出)。None = 零行为
            变化(既有宿主/测试不注入时与历史完全一致)。
        heartbeat_scan_interval: 扫描间隔秒(缺省
            :data:`DEFAULT_HEARTBEAT_SCAN_INTERVAL_SECONDS`)。"""
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
    next_scan = time.monotonic()  # 首轮即扫:启动后不等一个间隔才第一次评估
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
        # 心跳告警低频扫描钩子(10-05-cron-heartbeat 收尾件):cron_stale 的
        # 兜底直扫——搭车路径(pipeline run 尾挂)在 run 阶段自身异常中断的
        # 轮次不扫,这里独立于品类跑批周期性评估(首轮即扫:停摆检测宁早勿
        # 晚;间隔门在 ticker 自身心跳落笔之后,慢扫描既不推迟活性记账也不
        # 拖累下一锚点——超期重锚逻辑天然兜住)。
        if heartbeat_scan is not None and time.monotonic() >= next_scan:
            next_scan = time.monotonic() + heartbeat_scan_interval
            _guarded_heartbeat_scan(heartbeat_scan)
        next_tick += interval
        now = time.monotonic()
        if next_tick < now:
            next_tick = now + interval
        stop_event.wait(max(0.0, next_tick - now))
    logger.info("Cron ticker stopped")
