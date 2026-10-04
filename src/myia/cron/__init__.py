"""myia.cron — 通用定时任务底座(任务 10-04-hermes-cron Stage A)。

蓝本:Hermes cron/ 子系统(NousResearch/Hermes-Agent,MIT;上游路径
``~/.hermes/hermes-agent/cron/``)。移植纪律:逐文件对照上游重写为 MYIA
风格,模块 docstring 各自标注上游文件与行号;偏离(如 croniter →
APScheduler ``CronTrigger`` + dow 归一化层,偏离 D1)只出现在任务档
``.trellis/tasks/10-04-hermes-cron/design.md`` §6 偏离表,逐条带理由。

包内模块按 implement.md Stage A/B 自底向上落地:``constants``(fire-claim
时序常量)、``schedule``(schedule 解析 + next-run 计算)、``store``
(jobs.json 注册表)、``executions``(执行账本)、``jobs``(生命周期 +
到期扫描 + 心跳标记)、``occurrences``(到期身份去重 + pending_slot)已
就位;tick / ticker / runner / summary 随 Stage A6/B1 补齐。

公共 API 的统一再导出对照上游 ``cron/__init__.py``(上游再导出 jobs 的
create/get/list/... 函数族与 ``tick``;MYIA 的生命周期挂在显式
:class:`myia.cron.jobs.CronJobs` 实例上,故再导出类与模块级助手,
``tick`` 随 A6 补)。
"""

from myia.cron.constants import (
    CLAIM_TTL_INACTIVITY_HEADROOM,
    FIRE_CLAIM_SKEW_SECONDS,
    FIRE_CLAIM_TTL_SECONDS,
)
from myia.cron.executions import ExecutionLedger
from myia.cron.jobs import (
    COMPLETED_ONESHOT_RETENTION_DAYS,
    AmbiguousJobReference,
    CronJobs,
)
from myia.cron.occurrences import (
    completed_occurrence,
    pending_slot_stamp,
    scheduled_instant,
    unclaimed_pending_slot,
)
from myia.cron.schedule import (
    compute_next_run,
    normalize_dow,
    normalize_repeat_value,
    parse_duration,
    parse_schedule,
    resolve_zone,
)
from myia.cron.store import CronJobStore

__all__ = [
    "CLAIM_TTL_INACTIVITY_HEADROOM",
    "COMPLETED_ONESHOT_RETENTION_DAYS",
    "FIRE_CLAIM_SKEW_SECONDS",
    "FIRE_CLAIM_TTL_SECONDS",
    "AmbiguousJobReference",
    "CronJobStore",
    "CronJobs",
    "ExecutionLedger",
    "completed_occurrence",
    "compute_next_run",
    "normalize_dow",
    "normalize_repeat_value",
    "parse_duration",
    "parse_schedule",
    "pending_slot_stamp",
    "resolve_zone",
    "scheduled_instant",
    "unclaimed_pending_slot",
]
