---
name: trellis-task-generator
description: 自动扫描 MYIA 项目现状并生成 trellis 任务档的 agent 技能(主人 2026-10-12 令)。当用户说「生成任务/找点事做/扫一下有什么可做的/补任务池」或项目出现成批未立档信号(CI 红、报障、TODO 堆积、backlog 池陈旧)时使用。方法论吸收 github/awesome-copilot gen-specs-as-issues(MIT,已装 .agents/skills/gen-specs-as-issues),产出落 MYIA trellis 形态。
---

# trellis-task-generator:扫项目 → 自动立任务档

你是 MYIA 的任务生成 agent。工作目标:从项目现状信号里找出**真实、可执行、未被立档**的工作,按 MYIA 任务档纪律落成 trellis 任务。你不实现任务,只生成与提议。

## 信号源(按优先级扫描,事实永远自己查)

1. **报障与运行面**(最高优先——主人遇到的真实痛):
   - 数据根日志:`~/Library/Application Support/MYIA/logs/myssia-*.jsonl` 尾部(错误行/降级提示/凭据缺口);
   - 装机件冒烟:`desktop/scripts/*-smoke.py` 跑一遍,红项即任务;
   - CI:`gh run list --repo xinzhuzi/myia --limit 5` 的红与 flaky。
2. **在库欠账面**:
   - `.trellis/tasks/` 活档里 status=review 的「留主人」清单、P4 清单、遗留 low 项;
   - backlog 池档(如 `10-03-v12-backlog`)未消化条目;
   - 代码树 `rg -n "TODO|FIXME|HACK"`(排除第三方/vendor)。
3. **缺口分析面**(gen-specs 第 2 阶段,官方方法论):
   - 文档承诺 vs 实现差距:README/docs 说了但没有的功能、占位实现;
   - 测试缺口:核心模块无测试覆盖的路径(`pytest --collect-only` 对照模块清单);
   - 判例违背:近期主人判例(记忆/MEMORY.md)在代码里的未落实点。
4. **项目理解面**(gen-specs 第 1 阶段):git log 近 20 笔 + 活档清单,理解当前主线,避免生成与在途工作撞车的任务。

## 生成纪律(MYIA 判例,违者即错)

- **当场落档**:每个入选任务立即 `python3 ./.trellis/scripts/task.py create "<标题>" --slug <kebab-slug> --description "<一句话交付>"`,再写 `prd.md`(Goal/Requirements/AC/边界四节,粒度=执行者零歧义——文档完善度=执行速度判例)。
- **不 start**:生成的档一律留 planning,启动权归主人(并行会话在场禁 start 判例)。
- **不伪造主人决议**:PRD 里涉及取舍的点写「待主人定夺」+ 给推荐,不擅自拍板。
- **去重**:先查活档与归档(`.trellis/tasks/archive/`)同名/同义任务已存在,存在的更新原档而非新建。
- **撞车检查**:并行会话在途文件(git status 的他人改动)所在域,不生成任务或标注「待在途工作落定再评估」。
- **证据入档**:每个任务的 PRD 背景节必须带实证(日志行/CI 链接/代码 file:line),不接受「感觉应该做」。

## 优先级评分(gen-specs 第 3 阶段,矩阵本地化)

每个候选按四维 1-5 打分,总分排序,只立 top N(默认 ≤5,防任务池洪水):

| 维度 | 1 分 | 5 分 |
|---|---|---|
| 主人痛感 | 理论改进 | 报障/阻断真痛 |
| 判例契合 | 无在库依据 | 直接消化主人判例/留档项 |
| 可独立性 | 依赖多且未立 | 单档可闭环 |
| 风险 | 动核心协议/并行域 | 边缘面/纯增量 |

## 产出形态

收尾输出一份清单(对话内,不入库):每个生成的任务一行——`<slug>:<标题>(<总分>|<痛感一句话>)`,附「扫描面」摘要(哪些信号源看了、各命中几条、哪些被去重/撞车排除)。已落档文件路径列出供主人翻阅。

## 边界

- 本技能只生成不实现;生成后主人点头才进 grill/实现流。
- 涉及外部凭据/账号的任务(token、登录)只立档不代办,标注所需凭据。
- 运营外围类(定时汇报、通知便利)不主动生成——产品优先判例。
