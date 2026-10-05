# Python 环境分区版面拉齐(撤特殊化)

## 背景

10-05-desktop-managed-py-env 落地时,bac3ce4 判例把 python-env 分区做成「体验面」:
激活时隐藏左侧分区导航、内容列改 max-w-4xl 独占居中、顶部挂「← 返回设置」退路;
pyenv 卡内也弃用全设置屏统一的行式词汇(无 CardHeader、镜像输入 label 上/输入全宽)。

主人 2026-10-05 晚看图裁决(两张截图对照:python-env 全屏独占 vs 系统区标准版面):
**「这个地方的 UI 设置、布局、显示隐藏,要像其他的一样,Python 环境这个太特殊了,需要改」**
——撤特殊化,与其他分区同版面。此裁决推翻 bac3ce4 判例在 python-env 的适用
(该判例如仍适用于其他「体验型配置面」,由后续个案再议,本档不扩大)。

## 需求

1. **分区导航常驻**:python-env 激活时左侧「过滤分区 + 分区导航」列不再隐藏,
   外层容器不再因 python-env 解除 `md:flex-row`。
2. **内容列回归标准列宽**:python-env 弃 `max-w-4xl` 独占,与各区同用
   `md:max-w-[75%] lg:max-w-[67%] xl:max-w-[58%]` 比例列。
3. **删「← 返回设置」按钮**:导航在,退路不需要。
4. **pyenv 卡结构回归卡片词汇**:补 `CardHeader`(图标+标题+描述,与
   sidecar 核心进程/软件更新/装机组件卡同款);私有 `MirrorField`
   (label 上/输入全宽)换成全设置屏统一 `FieldInput`(label 左/输入右 w-64,
   labelHint 问号提示由 FieldInput 内建)。
5. **内容件保留**:状态横幅/路径块/五阶段时间线/可选组件行/底部动作条为内容本体,
   不属版面特殊化,原样保留(测试全走 aria-label/testid,不受行式变化影响)。

## 验收标准

- [x] AC1: python-env 激活时 `settings-nav` 可见(无 `hidden` 类),
      外层容器恒为 `md:flex-row`;深链 `?section=python-env` 不变。
      ✅ 38acd34 守卫断言过 + 无头 DOM 探针 navColumnClass=`flex shrink-0 flex-col gap-2 md:w-44`
- [x] AC2: python-env 内容列 className 不含 `max-w-4xl`,
      与其他分区同列宽类。
      ✅ 断言含 `xl:max-w-[58%]` + 探针 sectionClass 同款
- [x] AC3: 全设置屏不再出现「返回设置」按钮。
      ✅ queryByRole null + 探针 backBtn=false + OCR 全文无此串
- [x] AC4: pyenv 卡渲染 CardHeader(图标+标题+描述);镜像两输入为
      FieldInput 行(aria-label 不变:`运行时下载源覆盖`/`PyPI 镜像覆盖`)。
      ✅ 探针 cardHeaderTitle=「环境状态与安装」/ mirrorInputs=2;pyenv-card 16 测零改动全过
- [x] AC5: settings.test.tsx 增守卫断言(AC1-3 的回归守卫);
      pyenv-card.test.tsx 全量零改动通过。
      ✅ settings 目录 vitest 115/115(7 文件);镜像迁移在 38acd34 时点确实
      零改动过,复查轮又补 CardTitle/CardDescription 卡头断言(16/16 绿)
- [x] AC6: 桌面前端门禁绿:settings 相关 vitest + tsc/build。
      ✅ tsc --noEmit 0 错 + npm run build(tsc -b + vite build)绿

## 决策记录(实现口径)

- **D1 卡标题不复读分区标题**:单卡区,卡头若照抄 h2「Python 运行环境」即上下两口吃;
  取「环境状态与安装」——概括卡内两大面(状态横幅/明细),与兄弟卡
  (sidecar 核心进程/软件更新/装机组件)「具体名词」命名法一致。
- **D2 镜像输入换 FieldInput,不保留 MirrorField**:输入行是「像其他的一样」的最直接
  触点——label 左/输入右 w-64/问号提示内建,全设置屏同一词汇;aria-label 原值保留,
  pyenv-card 16 个既有测试零改动通过即是迁移无感证明。私有组件删除,不留死码。
- **D3 内容件保留**:状态横幅(五态左边框)/路径块 break-all 全显/五阶段竖向时间线/
  组件行/底部动作条是内容本体,非版面特殊化;卡内分组 h3 有 bundled-plugins 卡先例,
  「环境信息/镜像源覆盖/安装明细/可选组件」分组结构保留。
- **D4 守卫断言断类名不断样式**:jsdom 不渲染 CSS,「导航列可见」只能落成
  `settings-nav` 父列 className 无 `hidden`;列宽一致性落成 section className
  含 `xl:max-w-[58%]` 且不含 `max-w-4xl`。防回归的最小可靠形式。
- **D5 撤特殊化不等于删注释**:settings-screen/pyenv-card 两处头注改写为
  「曾按 bac3ce4 判例特殊化,现撤」——判例翻案史留在线,防后人看旧档复刻。

## 复查轮(主人质询「没有其他问题了吗」后的深化自查,2026-10-05 深夜)

| 检查面 | 手段 | 结论 |
| --- | --- | --- |
| 活水 spec 是否钉了旧判例 | grep `.trellis/spec/`(全局版面/独占/占满/体验型配置/max-w-4xl/返回设置) | 零命中(两处「独占」命中系 darwin 平台标记与 TG 单轮询,无关) |
| zh/en 文档是否描述旧版面 | grep `docs/`+README(返回设置/全局版面/占满主画布/独占) | 零命中(命中系 TG token 轮询语义,无关) |
| 前端源码残留 | grep `desktop/ui-src/src`(max-w-4xl/返回设置) | 仅守卫断言与翻案注释(正确用法),零 UI 残留 |
| 合并树全量回归 | 全量 vitest(含并行线在途 dashboard/logs 文件) | 26 文件 508/508 绿——我方提交与并行 WIP 合并零红 |
| 卡头断言深化 | pyenv-card.test 补 CardTitle/CardDescription 断言(AC4 卡头半边的档级守卫) | 16/16 绿 |
| 判例记忆同步 | memory `desktop-managed-py-env-directive` + MEMORY.md 索引 | bac3ce4 已标「被推翻」,现行口径=设置内所有分区同一版面 |

## 实施回执

- 提交一(实现):38acd34(fix(desktop),--only 六路径;随档循 G1 收编 label-hint 上提件
  = 改名+field-input 导入行,10-05-dashboard-glance 在途件注记在 commit)。
- 像素实证:.zcode/smoke/pyenv-unify-shot.cjs(vite 5213 + bridge 39885 +
  pyenv stub 就绪态)全页截图 /tmp/pyenv-unify.png;DOM 探针 + local-ocr 一级
  双证:导航列常驻(七分区项)、比例列宽、无返回钮、卡头、双 FieldInput、
  状态横幅/路径/时间线/组件行全渲染。
- gitnexus detect-changes(worktree):我方符号仅 PyenvCard/SettingsScreen,
  影响流均 UI 局部(4-5 步),无高危。
- 提交二(档):de17cd6(task 置 review + AC 回填)。
- 提交三(复查轮):pyenv-card.test 卡头断言 + 本档深化(决策记录/复查轮/
  遗留与移交)。
- 装机包未刷新(本档边界内声明;换装像素终验留装机节奏)。

## 边界

- 不动 pyenv-api.ts IPC 契约、壳侧、五态状态机、组件开关行为。
- 不动其他分区版面;不动 migration-banner / pyenv-gate-banner 深链落点。
- 装机包刷新不在本档内(提交后按主人节奏;汇报须显式声明未刷新)。

## 遗留与移交

- **装机包刷新 + 换装像素终验**:当前安装的 app 仍是旧版面;重打包换装后按
  [[packaged-app-verify-and-swap-race]] 纪律(先验源再删旧+清 WKWebView 缓存)
  截屏 OCR 终验导航常驻。可与并行线(dashboard-glance 也在等装机)合批重打包。
- **取证脚本**:`.zcode/smoke/pyenv-unify-shot.cjs`(pyenv stub 就绪态无头截图,
  不入库);其 playwright require 路径随 npx 缓存漂移,复用前先换最新
  `~/.npm/_npx/<hash>` 哈希(本次已漂移两轮:705bc6→9833c1→cbf1b8)。
- **label-hint 上提件收编注记**:38acd34 循 G1 收编了 dashboard-glance 线的
  label-hint 改名(screens/settings→components)+field-input 导入行;该线后续
  提交 dashboard 侧导入时应知悉改名已入库。
- **翻案史可溯**:bac3ce4(旧判例)→ 本档 38acd34(推翻)在 git 与 memory
  双线留痕;若主人日后要让某「体验型配置面」独占画布,须个案明示,不再默认。
