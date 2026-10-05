# 执行计划:仪表盘一眼看懂

前置:读 `.trellis/spec/desktop/frontend-ui.md`(改 UI 必读检查单:token/
出处注释/测试同步/协议红线)与 prd.md/design.md。

改动面(pathspec 提交纪律):dashboard 三件 + `screens/logs/logs-screen.tsx`
(及其测试,dry→试跑两屏同改)+ `settings/label-hint.tsx` 上提
`src/components/label-hint.tsx` + settings 引用处(执行时
`grep -rn "label-hint" src/` 定位)。

## 步骤

- [x] S1 `api.ts`:`buildVerdict` 类型+纯函数(design D1 语气阶梯)+
  单测(四态/facts 逐项缺省+随窗/null 分支)。
- [x] S2 ①`label-hint.tsx` 上提 `src/components/`:消费方 3 文件改
  import 行(`field-input` / `pyenv-card` / `settings-screen`,已实核;
  pyenv-card 有并行在途改动,撞车退屏内私有复制案,见 design D4),
  scoped vitest settings 回归;②StatCell `noteKind` 参数+ⓘ HintButton
  接线(D4,ui/tooltip 基件);③活跃源格分母 `12/14`(D5);四格调用处
  显式标注 meta/alert。
- [x] S3 verdict 行组件(D2)接入屏首(无头范式首块)+ 四态组件测试
  (facts 随概览窗断言,grill Q1)。
- [x] S4 AlertList(D3)接入概览节:触发=告警或坏源非零,坏源行优先+
  品类级 findings 补位(finding.message,形状已实核);测试覆盖触发
  双口径(仅 findings / 仅坏源)、三条可点、品类补位行、皆零零占位、
  溢出口跳源管理;reason 原文直用(cli 已人话,零映射)。
- [x] S5 文案映射表落屏(D6:含 logs dry→试跑两屏同改、品类节注三态、
  aria 人话;**文案以 design D9 全稿直抄**)+ `grep -n "run"` 可见层
  审计清零(dashboard+logs)。断言实核清单:L268 用例标题、L354
  「还没有 run 记录」、L526/528「即时快照不随窗」(textContent 明文 →
  tooltip 触发后查内容);dry 徽标 dashboard/logs 各新增一枚断言(夹具
  补 dry:true 行);其余以 `grep -n "run\|坏者" dashboard-screen.test.tsx`
  复核清零,不留半新半旧;tooltip 断言触发方式照 `components/ui/
  ui-base.test.tsx` 基件自测先例(focus/pointerEnter 后查 TooltipContent)。
- [x] S6 门禁(顺序跑,全绿才进 S7):
  - `cd desktop/ui-src && npx vitest run src/screens/dashboard src/screens/settings src/screens/logs`(scoped)
  - `npm run test`(全量 vitest)
  - `npm run build`(tsc -b + vite build)
  - 根目录 `uv run pytest -q`(全量兜底,零新红)
  ——收口员亲跑复核全绿:scoped 185/185、全量 507/507、build ✓、
  pytest 4384 passed 40 skipped。
- [x] S7 视觉回执:无头冒烟(基建实址 `.zcode/smoke/bridge.mjs`+
  `__TAURI_INTERNALS__` shim 先例)或装机包刷新后
  `MYIA_SHOW_ON_START=1` 直跑二进制 + screencapture + local-ocr;
  截屏/OCR 证据入 `evidence/`(目录随本步创建);装机包按
  判例刷新换装(交付完成判定含装机包)。
  ——按无头冒烟路径取证(9 帧+探针+OCR 入 evidence/);装机包刷新
  未做(AC6 留空待办)。
  ——装机包终验主会话已补(同日夜):tauri build 重打包静默换装
  /Applications/世事.app+MYIA_SHOW_ON_START=1 亮窗取证+两级 OCR 五关键行
  全对=evidence/10-installed-app-verdict.png+installed-ocr.txt,AC6 销号。
- [x] S8 勾 AC(prd.md)→ review。

## review gates

- S3 后:verdict 四态截图自审(语义+排版)再继续 S4。
- S6 后:门禁全绿才进 S7。
- S7 后:像素回执贴档,留主人只余审美裁决。

## 回滚点

- 单提交制;`git revert` 即回滚;无协议/数据迁移,不动共享层。
