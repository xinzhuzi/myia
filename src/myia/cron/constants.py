"""Fire-claim 时序常量(job 存储与同胞模块共享)。

MYIA 移植重写自 Hermes ``cron/constants.py``(NousResearch/Hermes-Agent,
MIT;上游路径 ``~/.hermes/hermes-agent/cron/constants.py``,17 行全文)。
常量名与值逐字保留,仅注释改写为 MYIA 语境(上游 HERMES_CRON_TIMEOUT
不活跃超时在本任务改为墙钟 ``run_timeout``,偏离 D12,见任务档
design.md §6)。

刻意零 import:长命进程在启动期缓存的 ``cron.jobs`` 对象可能落后于新从
磁盘树加载的同胞模块,后者必须能独立解析这些值(上游同款约束)。
"""

from __future__ import annotations

__all__ = [
    "CLAIM_TTL_INACTIVITY_HEADROOM",
    "FIRE_CLAIM_SKEW_SECONDS",
    "FIRE_CLAIM_TTL_SECONDS",
]

#: fire_claim 认领存活期(秒;心跳节奏 60s)。认领、one-shot re-arm、
#: 过期恢复共用同一个值,三处口径不可能不一致(上游同款注释)。
FIRE_CLAIM_TTL_SECONDS = 300

#: fire 早到认领仍有效的时钟偏斜窗(秒)。宿主侧 fire 可比存储的
#: ``next_run_at`` 早到几秒(fire 调度方的时钟跑在我们前面);该窗内的
#: 早到认领仍持有 slot,更早的才是 off-tick 的手动/面板 fire。
FIRE_CLAIM_SKEW_SECONDS = 60

#: claim TTL 相对不活跃上限的倍数头寸。超时是*不活跃*上限而非墙钟帽——
#: 健康运行可合法超过它,TTL 恰等于超时会误杀活认领(MYIA 侧对应
#: ``run_timeout``,D12;上游对应 HERMES_CRON_TIMEOUT)。
CLAIM_TTL_INACTIVITY_HEADROOM = 3
