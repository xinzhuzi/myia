# 消息屏标题层级修复(v12-backlog P3 消号)

## Goal

消息屏分区标题具备规范的语义层级(屏内 h2 起步、详情面板 h3/h4 归位),
消掉 v12-backlog 第 8 项登记的「P3 消息标题跳级」;视觉零变化。

## 背景与事实基础修正(2026-10-05 全量探查)

- P3 登记链:fe-small-batch prd:20「不入本批」→ fe-gap-census matrix.md:107
  登记「当前消息屏仅 PageHeader h1(messaging-screen.tsx:306+page-header.tsx:14),
  **未见跳级复现**,维持登记」。
- **登记口径已过时**:PageHeader 已按主人 2026-10-04「无头」指令改为
  `return null` 空壳(commit d9ae353)——全应用各屏均不再有 h1。
- 消息屏现状(本会话实核):
  - messaging-screen.tsx 零 h 标签;三个分区卡头(通道目录 :384 / 推送规则 :516 /
    告警规则 :958)走 CardTitle=div(card.tsx:28-35,`data-slot="card-title"`);
  - platform-overview.tsx 平台总览卡头同为 CardTitle div(:1146);详情面板
    平台名 h3(:1327)、小节标题 h4(:1264)——**h3/h4 悬空,其上无任何 h2**。
- 兄弟屏惯例(dashboard-screen.tsx:661 / logs-screen.tsx:767 / settings-screen.tsx:638):
  分区标题=显式 `<h2 className="text-base font-semibold text-foreground">`。
  feed/sources/cron/yaml-editor 屏无任何标题标签(屏外事实,本任务不动——勿扩大)。
- 即:P3 原文「跳级」在当下代码里的真实形态 = 首个标题即 h3(h1/h2 双缺),
  修法对齐兄弟屏 h2 惯例。

## Requirements

- R1:`CardTitle` 组件加可选 `as` prop(缺省 `"div"`,全部既有调用方渲染
  零变化;类名/`data-slot` 原样透传)。
- R2:消息屏四分区卡头改 `as="h2"`——平台总览(platform-overview.tsx:1146)、
  通道目录(messaging-screen.tsx:384)、推送规则(:516)、告警规则(:958)。
  层级终态:h2(四分区)→ h3(详情面板平台名)→ h4(小节标题),无跳级。
- R3:视觉零变化——类名不动,`as` 只换标签名。
- R4:messaging 测试补标题层级断言(四个分区 heading role / level 2)。

## Acceptance Criteria

- [x] AC1:消息屏渲染后四分区均为 `heading` role、level 2(测试断言)。
- [x] AC2:消息屏两文件内全树无标题跳级(h2→h3→h4 顺序完整)。
- [x] AC3:`npm --prefix desktop/ui-src run test` 全量绿 + `run build`(tsc)绿
  ——CardTitle 为共享组件(上游 11 调用方),门禁必须全量,不接受只跑 scoped。
  (2026-10-05 实跑:23 文件 420 passed + 8 skipped;build 1.58s 绿,仅既有
  chunk>500kB 警告;新增用例「分区标题层级」scoped 复跑 1 passed)
- [x] AC4:既有调用方零改动(git diff 仅 card.tsx + 消息屏两文件 + 测试文件);
  零协议变更(`git diff --stat -- desktop/entry.py` 为空)。
- [x] AC5:`gitnexus detect-changes -r shishi --scope staged` 无意外面。(回标见提交批注)

## Constraints

- **勿扩大**(fe-gap-census 原判):只动消息屏两文件 + card.tsx 一个 prop +
  测试;其他屏的 CardTitle 用法与无标题现状一概不动;不借机做全应用 a11y 统一。
- 零 sidecar 协议变更;不 push(推送归主人)。
- 并行会话在途(feed/dashboard/yaml-editor 屏有脏件),提交按 path 白名单分离。

## Notes

- 主人 2026-10-05 指令:「1,2,3 都做」(全景走查 / 真机冒烟 / P3 遗留小项),
  本档=第 3 件;前两件成果在同会话终报,不另立档。
- CardTitle 影响面:gitnexus impact 上游 11 直接调用方/评级 CRITICAL(共享面广);
  缓解=纯增量可选 prop(缺省路径行为不变)+ AC3 全量门禁。
- 消号回执:完成后 v12-backlog prd 第 8 项 P3 行回标「已消号」。
