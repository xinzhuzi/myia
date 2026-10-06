# 日志健康批:cron 数据根统一 + doctor 空集误报 + 推送失败日志聚合

> **骨架补记(2026-10-06 三段纪律巡检)**:本档开工时未建 prd,工作与回执先行落在 task.json 与提交信息(先档后行形态缺口,如实记);本文件为巡检补的回填骨架,需求原文与验收证据以下列指针为准,未新造内容。

## Goal

主人 2026-10-06 令「都做完,再深度检查,测试」。三件(原文=task.json description):①cron 子命令数据根解析与 run/doctor 不一致(cwd 缺省不吃 MYIA_HOME,仓库目录跑 cron 会把 jobs.json 建进仓库——本日实测踩中)统一为 MYIA_HOME 感知;②doctor 把合法空集误诊 source_degraded(gog-free 0 元查询空集=正常)加 empty_ok 语义;③wool 类逐条推送失败同因 WARNING×31 刷屏,同批同因聚合降噪。

## Requirements

- 未回填(开工时未立 prd;需求原文以 task.json description 三件为准,提交 43683c9 提交信息逐条对应落地面)

## Acceptance Criteria

- [x] 三件套全落地+测试 +5+门禁全量 pytest 4541/0+ruff 净+vitest 绿+四项深度复检全过(含仓库零污染、wool 35→7 警告、games 语义零变化)——回执=提交 5de3b36 提交信息;task.json status=review、commit=43683c9
- [ ] (补位)档重启时 AC 以 task.json description 为准回填

## 过程(执行流水,回填位)

- [x] 实现+测试:提交 43683c9(9 文件 +174/−21——cli.py `_cron_default_db` 11 子命令/schema.py empty_ok 字段/push digest.py 同因聚合/games.yaml/SKILL.md 字段表/测试三件 +5)
- [x] 置 review+档务:提交 5de3b36
- [ ] (空位;档重启由此续填)

## 结果(验收回执,完工填)

- [x] 门禁与四项深度复检回执:5de3b36 提交信息在案(4541/0、ruff 净、vitest 绿;仓库零污染/wool 35→7/games 语义零变化)
- [ ] 主人验收(owner review 在途;task.json completedAt=null)
