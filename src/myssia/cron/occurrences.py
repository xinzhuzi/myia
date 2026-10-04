"""精确的调度身份,独立于可变的 jobs.json 派发戳。

上游蓝本:``~/.hermes/hermes-agent/cron/occurrences.py``(102 行全文,
2026-10-04 HEAD)。NousResearch/Hermes-Agent,MIT——逐函数对照重写为 MYIA
风格,非整块拷贝。

MYIA 适配(任务 10-04-hermes-cron,非照抄处仅此):

- ``scheduled_instant`` 复用 :func:`myia.cron.executions.canonical_scheduled_
  instant`(executions.py 已实现同一语义——aware ISO → UTC ISO、naive/垃圾
  → None——A3 时即注明「occurrences.py(A5)复用本函数,勿重复实现」;
  此处以别名再导出保住上游函数名)。
- ``completed_occurrence`` 增加 ``ledger`` 关键字参数:上游引模块级
  ``_transaction``,MYIA 账本是显式 :class:`~myia.cron.executions.
  ExecutionLedger` 实例,经其公开 :meth:`transaction` 走同一纪律
  (进程内锁 + 必关连接)。
- ``pending_slot_stamp``/``unclaimed_pending_slot`` 经惰性 import 引
  ``myia.cron.jobs`` 的 :func:`~myia.cron.jobs.machine_id` /
  :func:`~myia.cron.jobs.claim_is_live` /
  :func:`~myia.cron.jobs.job_running_in_this_process`(上游同款双向惰性
  import 防 jobs ↔ occurrences 循环)。
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Optional

from myia.cron.constants import FIRE_CLAIM_SKEW_SECONDS, FIRE_CLAIM_TTL_SECONDS
from myia.cron.executions import ExecutionLedger, canonical_scheduled_instant

logger = logging.getLogger(__name__)

__all__ = [
    "completed_occurrence",
    "pending_slot_stamp",
    "scheduled_instant",
    "unclaimed_pending_slot",
]

# 到期身份规范化 = 账本列的规范化(同一函数,勿重复实现;executions.py A3 注)。
scheduled_instant = canonical_scheduled_instant


def completed_occurrence(
    job: dict[str, Any],
    instant: Any,
    *,
    ledger: ExecutionLedger,
) -> bool:
    """该 occurrence 是否已有**完成**的执行(到期身份去重闸)。

    unknown/failed/被裁剪的尝试都证明不了完成:保持可发。仅有据可查的毒行
    ——完成时刻早于其所认领 occurrence(早于 earliest_real)——被忽略。

    两处去重闸(due 扫描与 fire 认领)在 True 时都**不**跑 run、不落账本行
    地消费掉该槽,所以下面的告警是跳过留下的唯一痕迹(上游 #111414)。
    账本异常按「查不了」处理返回 False(fail-open:宁可潜在重发,不可静默
    吞掉整个调度)。
    """
    instant = scheduled_instant(instant)
    if instant is None:
        return False
    # 偏斜早到的 fire(见 claim_job_for_fire)合法地在其槽前一点完成。
    earliest_real = datetime.fromisoformat(instant) - timedelta(
        seconds=FIRE_CLAIM_SKEW_SECONDS
    )
    try:
        with ledger.transaction() as conn:
            rows = conn.execute(
                "SELECT id, finished_at, claimed_at FROM executions "
                "WHERE job_id=? AND scheduled_instant=? "
                "AND status='completed'",
                (str(job["id"]), instant),
            ).fetchall()
        for row in rows:
            completed_at = scheduled_instant(row["finished_at"] or row["claimed_at"])
            # 遗留或残缺时间戳仍是完成证明;只有**确诊**的毒行——完成记录早于
            # 其认领的 occurrence——才忽略。
            if (
                completed_at is None
                or datetime.fromisoformat(completed_at) >= earliest_real
            ):
                logger.warning(
                    "Job '%s' (%s): scheduled occurrence %s was already completed by execution "
                    "%s (finished %s); skipping the due slot without a new run",
                    job.get("name", job.get("id")),
                    job.get("id"),
                    instant,
                    row["id"],
                    row["finished_at"] or row["claimed_at"],
                )
                return True
        return False
    except Exception:
        logger.warning(
            "Cannot check completed occurrence for job %s", job["id"], exc_info=True
        )
        return False


# --- pending slot:tick 从排程上拿走、却尚未认领的 occurrence ------------------
#
# tick 在派发**前**推进 recurring job 的 ``next_run_at``(at-most-once:run
# 中途崩溃不得在每次重启时重发)。这留下一个窗口——推进已做、fire 认领未取
# (解释器收尾、执行池拒活、进程被杀)——进程在窗口内退出就**无声丢掉**该
# occurrence:重启后的扫描看到未来的 ``next_run_at``,什么都没跑过(#107485)。
# ``pending_slot`` 是该窗口的持久记录:due 扫描用「存储的精确射点 + 戳记属主」
# 盖章,``claim_job_for_fire``(副作用可能存在的分界点)清除它,schedule 的
# 任何显式改写丢弃它。属主可证已死(或租约已过)仍 pending 的槽从未被认领,
# 所以**恰恢复一次**为 due 射点,随后按普通迟到 / fast-forward 策略流动——
# 绝不 N 连重放。


def pending_slot_stamp(next_run: Any, now: datetime) -> dict[str, Any]:
    """即将交给派发器的 recurring occurrence 的存储值。"""
    from myia.cron.jobs import machine_id

    return {"scheduled_at": next_run, "at": now.isoformat(), "by": machine_id()}


def unclaimed_pending_slot(job: dict[str, Any], now: datetime) -> Optional[str]:
    """派发器从未认领的槽的存储射点,或 None。

    非 recurring job、残缺戳记(绝不当作 fire 信号)、本进程仍在跑的 job
    (其排队 worker 会自行认领并清槽)都返回 None。**本进程**戳的、job 却
    不在本进程跑 = 孤儿戳(派发被拒)。**他进程**戳的在 fire-claim 租期内
    仍尊重——同一存储上的第二个活宿主正在派发中,不是死了。"""
    from myia.cron.jobs import claim_is_live, job_running_in_this_process, machine_id

    pending = job.get("pending_slot")
    if not isinstance(pending, dict):
        return None
    slot = pending.get("scheduled_at")
    if (job.get("schedule") or {}).get("kind") not in {
        "cron",
        "interval",
    } or not isinstance(slot, str):
        return None
    try:
        datetime.fromisoformat(slot)
    except ValueError:
        return None
    if job_running_in_this_process(str(job.get("id", ""))):
        return None
    if pending.get("by") != machine_id() and claim_is_live(
        pending, now, FIRE_CLAIM_TTL_SECONDS
    ):
        return None
    return slot
