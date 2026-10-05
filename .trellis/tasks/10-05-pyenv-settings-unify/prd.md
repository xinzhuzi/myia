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
      ✅ settings 目录 vitest 115/115(7 文件)
- [x] AC6: 桌面前端门禁绿:settings 相关 vitest + tsc/build。
      ✅ tsc --noEmit 0 错 + npm run build(tsc -b + vite build)绿

## 实施回执

- 提交:38acd34(fix(desktop),--only 六路径;随档循 G1 收编 label-hint 上提件
  = 改名+field-input 导入行,10-05-dashboard-glance 在途件注记在 commit)。
- 像素实证:.zcode/smoke/pyenv-unify-shot.cjs(vite 5213 + bridge 39885 +
  pyenv stub 就绪态)全页截图 /tmp/pyenv-unify.png;DOM 探针 + local-ocr 一级
  双证:导航列常驻(七分区项)、比例列宽、无返回钮、卡头、双 FieldInput、
  状态横幅/路径/时间线/组件行全渲染。
- gitnexus detect-changes(worktree):我方符号仅 PyenvCard/SettingsScreen,
  影响流均 UI 局部(4-5 步),无高危。
- 装机包未刷新(本档边界内声明;换装像素终验留装机节奏)。

## 边界

- 不动 pyenv-api.ts IPC 契约、壳侧、五态状态机、组件开关行为。
- 不动其他分区版面;不动 migration-banner / pyenv-gate-banner 深链落点。
- 装机包刷新不在本档内(提交后按主人节奏;汇报须显式声明未刷新)。
