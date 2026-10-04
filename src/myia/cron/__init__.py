"""shishi.cron — 通用定时任务底座(任务 10-04-hermes-cron Stage A)。

蓝本:Hermes cron/ 子系统(NousResearch/Hermes-Agent,MIT;上游路径
``~/.hermes/hermes-agent/cron/``)。移植纪律:逐文件对照上游重写为 MYIA
风格,模块 docstring 各自标注上游文件与行号;偏离(如 croniter →
APScheduler ``CronTrigger`` + dow 归一化层,偏离 D1)只出现在任务档
``.trellis/tasks/10-04-hermes-cron/design.md`` §6 偏离表,逐条带理由。

包内模块按 implement.md Stage A/B 自底向上落地:``constants``(fire-claim
时序常量)、``schedule``(schedule 解析 + next-run 计算)已就位;store /
executions / jobs / occurrences / tick / ticker / runner 随后续步骤补齐。
公共 API 的统一导出(``__all__`` 再导出)留到子模块齐后一并做,当前各子
模块独立导入使用。
"""
