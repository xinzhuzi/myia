# 采集日志两级界面重做(L1 摘要行→L2 详情)

## Goal

主人令(10-11 晚,/workflow 下达):采集日志从「内嵌折叠 accordion」重做为**两级界面**——
1 级每轮一行展示「本轮主要采集了什么」;2 级展示该轮日志详细内容与失败原因。
先做计划(本档 + design.md)再执行。

## Requirements(主人原话拆解)

1. **1 级界面**:每 run 一行,行内可读出「本轮采集了什么」——品类 + 采集成果摘要 +
   状态/时间/耗时;现折叠组头信息保留并升级为摘要行。
2. **2 级界面**:点行进入该轮详情——完整日志体(自动滚底/错误行高亮/复制)+
   **失败/部分轮要能看出「为什么失败」**(结构化失败原因区)。
3. UI 展示效果重新设计;信息架构从 accordion 内嵌改为两级下钻;过滤/搜索/重跑/
   状态分布条等既有工具面不丢。

## 数据真源边界(像素双真源,不造假数据)

- `run.status` 行:run_id/status/exit_code/error/started_at/finished_at/duration_ms/
  record(category、stats.items_retained 等)/history/log_run_id —— 1 级「采集了什么」
  摘要**只能从这里派生**(record + stats + error 一句话)。
- `logs.tail`(run_id, lines≤4000 环形缓冲):seq/ts/stream/line —— **惰性拉取**
  (进 2 级才拉);1 级严禁逐行拉日志(50 行 × tail = 协议风暴)。
- 2 级「为什么失败」= exit_code + error 字段 + stderr 错误行(isRowError 双信号),
  如实展示、无据可查就说无据。

## 交互动线(在库判例对齐)

- 1 级 → 点行 → 2 级;**返回钮 + Esc** 回 1 级(情报流 v8 三级界面同款动线,
  `feed-screen.tsx` 状态切级先例;Kestra Executions→Execution 详情页同物种锚)。
- 跟随策略(新 running run)默认**不自动跳级**:1 级 running 行状态芯片实时即可,
  不打扰浏览(可翻案,designer 定稿需给理由)。
- 2 级保留:复制日志、自动滚底、实时跟踪徽标;重跑钮 1/2 级都可达。

## 设计判例(必须遵守,全在库有案)

1. **物种铁律**:Kestra 同物种锚(Executions 表列 → Execution 详情页),借结构改语义。
2. 无头布局终态 + 现有 token 体系(text-2xs/gap-grid/状态芯片/Kestra 紫),不改全局 CSS。
3. **文字覆盖三层根因**:overflow-hidden/shrink-0/API 源头截断;**10-11 刚修的瀑布流
   shrink-0 塌缩(67546cd)不得回归**——2 级日志体内滚容器同律(子项 shrink-0 或
   overflow 可见,二选一须显式)。
4. **布局哨兵**:`desktop/scripts/logs-screen-smoke.py`(10-11 落)必须按新 IA 重写,
   保留「布局哨兵」性质(1 级行高 ≥40px、容器 scrollHeight>clientHeight 断言)+
   新增两级动线断言(进 2 级/返回);无头 Chromium 1685×1057 档,截图落 /tmp。
5. 详情弹窗判例只管动作反馈类提示;L2 是页面级视图(非弹窗)。
6. jsdom 无真实布局:布局断言归无头冒烟;组件测试(logs-screen.test.tsx)随新 IA
   重写,管渲染语义/交互/过滤搜索逻辑。

## 门禁(全部必过,工作流内 world.run)

- `npm --prefix desktop/ui-src run build`(tsc -b + vite)
- `npm --prefix desktop/ui-src run test`(vitest 全量;基线 35 文件 744 绿,共享树)
- `.venv/bin/python desktop/scripts/logs-screen-smoke.py`(重写后两级动线冒烟)

## 交付(workflow 外,主会话)

pathspec 提交 → design.md+PRD+实现一笔入库 → tauri 重打包 + 静默换装 →
装机冒烟像素证据 → 档转 review。

## Acceptance Criteria

- [x] AC1 1 级:50 轮行直出,行内「采集了什么」摘要可读(品类+成果+状态+时间耗时),
      accordion 折叠退役,过滤/搜索/重跑/分布条不丢。
- [x] AC2 2 级:点行进入详情,完整日志体(自动滚底/错误行高亮/复制)+ 失败原因区
      (exit_code/error/stderr 摘);成功轮不显示失败区。
- [x] AC3 动线:返回钮 + Esc 回 1 级,过滤态与列表位置保持。
- [x] AC4 门禁三件绿 + 冒烟截图(1 级/2 级各一)像素证据。
- [x] AC5 装机件刷新换装(主会话,workflow 后)。

## 边界

- 不动数据面协议与 `@/lib/api` client;logs/api.ts 可加视图派生。
- **不动其他屏幕**:`App.tsx`/`sidebar.tsx`/`feed-screen.tsx`/`browser-module.tsx`/
  `settings-screen.tsx`/`screens/tg-account/` 是并行会话在途改动(10-11 实况),
  只读参考、严禁修改。
- 工作流内**不 git commit**:改动作留工作树,主会话地面核验后 pathspec 提交。
