# UI 杂批:设置 tooltip 翻案 + 沙箱窗自标识 + CI actions 升版

## Goal

三件互不相干的小批合一档(池档 `10-03-v12-backlog` 第 8 项 tooltip 翻案 +
第 9 项沙箱窗自标识;CI 升版独立小件),单笔任务交付,不拆档。

## 背景与实态核验(2026-10-05 建档轮亲核)

- **tooltip 基件已在库**:`desktop/ui-src/src/components/ui/tooltip.tsx` 为自研
  实现(头部注释明示「无 @radix-ui/react-tooltip 依赖(任务红线不装包)」),
  API = Radix 三件套形状(Tooltip/TooltipTrigger/TooltipContent),自带
  role="tooltip" + aria-describedby 接通,基件自测在 `ui-base.test.tsx:164-183`。
  **package.json 无 @radix-ui/react-tooltip 属预期(红线),本任务不装包、
  不重写基件,只做池档口径的「直接消费」**——任务书「新增 ui/tooltip.tsx +
  不在则 npm 安装」以库内事实为准修正:文件在、红线在,翻案方案本意即消费。
- **沙箱判定先例**:`main.rs` 的 `data_root()`(:316)/`acquire_instance_lock()`
  (:366)均以 `std::env::var_os("MYIA_HOME")` 是否有值为「显式实例域」判据
  (壳未设时根本不设此 env,只 spawn 时注入子进程),单实例锁注释明写
  「验证流用 MYIA_HOME 沙箱时属独立实例域(沙箱=独立环境,合理)」。
- **actions 版本核实**(gh api releases 亲验 2026-10-05):actions/checkout
  v5.1.0 存在(最新已到 v7.0.1);astral-sh/setup-uv v6.0.0 存在(最新已到
  v10.2.0)。任务口径保守小步:checkout v4→v5、setup-uv v5→v6,不追最新。

## Requirements

### ① 设置 tooltip 翻案(池档第 8 项裁撤后翻案极小方案)

设置屏挑 5 个高困惑字段挂既有 tooltip 基件,文案人话零行话:

| # | 字段 | 位置 | 挂点 |
|---|------|------|------|
| 1 | 预算护栏 budget_per_run(只读回显,为何改不了是困惑点) | settings-screen.tsx EnrichFeedbackCard 逐品类行 | SettingRow label |
| 2 | 代理池「池名」(拼进钥匙链凭据名的命名规则) | settings-screen.tsx 代理池卡 | FieldInput label |
| 3 | gates SaaS「API Key 值」(只入钥匙链、配置存引用、留空不覆盖) | settings-screen.tsx 门槛件付费通道卡 | FieldInput label |
| 4 | 运行时镜像源覆盖 | pyenv-card.tsx MirrorField | label |
| 5 | PyPI 镜像覆盖 | pyenv-card.tsx MirrorField | label |

- 实现面:设置屏私有小组件(label + 问号图标 TooltipTrigger),FieldInput /
  MirrorField 加可选 labelHint prop,SettingRow label 直接传节点。
- 样式遵守 frontend-ui.md:图标 size-3.5 / muted-foreground 色,零 arbitrary 值。
- vitest a11y 断言:悬停/聚焦图标 → tooltip 出现 + trigger 的
  aria-describedby 挂通 tooltip id(与基件自测同口径,业务消费面再钉一例)。

### ② 沙箱窗自标识(池档第 9 项)

显式 `MYIA_HOME` env(补验/自动化拉起的独立数据根)时主窗标题加
「(沙箱)」后缀;未设零行为变化。实现取最小面 = Rust 侧 setup:

- 纯函数 `sandbox_title(base, myia_home)`(is_some() 判定,与
  data_root/acquire_instance_lock 的 var_os 分支同源)+ setup 内调用
  `window.set_title`。
- Rust 单测:Some → 后缀、None → 透传。

### ③ CI actions 版本升级(消 Node20 弃用警告)

- `.github/workflows/ci.yml`:actions/checkout v4→v5(5 处)、
  astral-sh/setup-uv v5→v6(2 处)。
- `.github/workflows/desktop-release.yml`:actions/checkout v4→v5(4 处,
  同款顺带;setup-uv 不存在于此文件)。
- 其余 actions(setup-node@v4 / rust-cache@v2 / upload-artifact@v4 /
  action-gh-release@v2)不在本批范围,不动。
- 改完 yaml 语法自检(actionlint 有则跑,否则 python yaml 解析两文件)。

## Acceptance Criteria

- [x] AC1:5 个字段 tooltip 挂通,vitest a11y 断言过;npm test 全量绿。
  **回执(2026-10-05)**:挂的字段清单 = ①预算护栏行(settings-screen.tsx
  EnrichFeedbackCard 逐品类 SettingRow label,品类名问号)②代理池「池名」
  (凭据命名规则 myia/proxy/<池名>)③gates SaaS「API Key 值」(钥匙链引用/
  留空不覆盖,zenrows 行内定位断言)④运行时下载源覆盖(pyenv-card MirrorField)
  ⑤PyPI 镜像覆盖(同)。实态 = 新组件 `label-hint.tsx`(HintButton/LabelHint
  两导出)消费既有 ui/tooltip 基件;FieldInput/MirrorField 加可选 labelHint
  prop(不传渲染路径逐字节等价)。**a11y 坑位回执**:问号 button 嵌 `<label>`
  内会让 label 同时标注 Input 与 button(button 是 labelable element,
  getByLabelText 双匹配)——HintButton 一律在 label 外作兄弟节点,
  label-hint.tsx 头注钉死该纪律。断言 = 悬停 300ms 出 tooltip +
  aria-describedby 接通 tooltip id,settings.test.tsx 两例 + pyenv-card.test.tsx
  一例。npm test 全量 **477 passed**(基线 474 + 新 3)。
- [x] AC2:显式 MYIA_HOME 时主窗标题带「(沙箱)」后缀;cargo 门禁过。
  **回执**:实态 = Rust 纯函数 `sandbox_title(base, myia_home)`(main.rs,
  var_os 有值即加后缀,与 data_root/acquire_instance_lock 单实例锁同口径)
  + setup 内 `window.set_title`(置 MYIA_SMOKE_ROUTE 冒烟路由/亮窗之前,
  截图产物即带标识);未设零行为变化。cargo check --locked 绿 +
  cargo test **56 passed**(基线 54 + 新 2:Some 加后缀含指向默认根的显式
  设置/None 透传)。
- [x] AC3:两 workflow 升版落盘 + yaml 自检过。**回执(前后对照)**:
  actions/checkout v4→v5 = ci.yml ×5 + desktop-release.yml ×3(共 8 处,
  建档时估 ×9 系笔误,desktop-release 实为 3 处);astral-sh/setup-uv
  v5→v6 = ci.yml ×2(desktop-release.yml 无 setup-uv)。版本存在性 gh api
  releases 亲验:checkout v5.1.0(最新已 v7.0.1)、setup-uv v6.0.0(最新已
  v10.2.0)——按任务口径保守小步不追最新。自检 = python yaml 解析两文件 OK
  (ci 5 jobs / release 3 jobs)+ actionlint 全仓零新增告警(仅
  pypi-publish.yml 既有 SC2086 info 一条,非本批文件未动)。
- [x] AC4:门禁全绿。**回执**:desktop/ui-src `npm test` **477 passed(26
  files)** / `tsc -b` 零错 / `vite build` 过(1.64s,产物落 gitignored
  ../ui);desktop/src-tauri `cargo check --locked` 绿 / `cargo test --locked`
  **56 passed 0 failed**。
- [x] AC5:提交用 git commit --only 明确路径,不推远端;task.json 置 review。
  **回执**:三笔代码(tooltip / 沙箱标识 / CI 升版)+ 一笔 docs(task) 档案,
  hash 见任务档 task.json.commit 注记;gitnexus impact FieldInput upstream
  = 6 直接调用者 7 流(CRITICAL 标签源自调用广度;diff 亲证可选 prop 纯加法、
  不传时渲染路径逐字节等价,全量 vitest 兜底);detect-changes staged 核验
  归属仅本任务文件。

## 约束

- 不装任何 npm 新依赖(不装 @radix-ui/react-tooltip,基件红线)。
- 不动 sidecar 协议(纯 UI 消费 + Rust 壳侧标题,零协议面)。
- 并行会话在场:只动本任务文件,绝不 git add -A。
