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
- 装机包刷新:原判「不在本档内(提交后按主人节奏;汇报须显式声明未刷新)」;
  2026-10-06 已按 grill Q2(a) 当场重打包换装并通过像素终验,就此销号——
  详见下方「装机像素终验回执」。

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
- **装机包销号注记(2026-10-06 补)**:装机包已于 2026-10-05 23:36 随
  10-05-yaml-editor-csp-blank 修复换装(6f60904;换装包构建自当时 HEAD,
  本档 38acd34 经 `git merge-base --is-ancestor` 亲证在其祖先链——版面
  改动已随包进装机件;换装判例=退旧实例/换包/清 WKWebView 缓存,详见
  该档)。上方「装机包未刷新」声明(第 89/95 行两条)就此销号;第 99 行
  遗留项中「刷新+换装」已发生,其「换装像素终验」半项如实限定:6f60904
  档内的装机件双像素验证面向 YAML 编辑器修复面,pyenv 分区版面未见单独
  取证记录——如需按 [[packaged-app-verify-and-swap-race]] 纪律补一帧
  截屏 OCR 即可,不阻塞本档 review 态。

## grill 四决议(2026-10-06,主人令「按照 trellis 方式做完」,按推荐执行)

- **Q1(a) 装机终验过即归档**:本档唯一未销事项就是装机像素终验,终验一过即无等待项,review 态继续空转无意义——当场随收口归档。
- **Q2(a) 立即重打包换装终验**:与其把「换装像素终验」半项留档占位,不如当场做掉,归档前补齐最后一帧证据,遗留清单清零。
- **Q3(a) 状态徽标留卡内横幅,不上卡头**:卡头三件套(图标+标题+描述)是全设置屏统一词汇,状态横幅本就是卡内内容本体(D3 已定),徽标上卡头等于再开一处特殊化口子。
- **Q4(a) 守卫断言维持双向绊线**:jsdom 下断类名不断样式是最小可靠形式(D4 已定),「必含比例列宽类+必不含 max-w-4xl/hidden」双向绊线在 38acd34 已证效,不再加码。

## 装机像素终验回执(2026-10-06,按 grill Q2(a) 当场执行)

- **嵌入与指纹**:新包嵌入 HEAD `3c7986cb9388cb44beab49d99c63c90b5b4ff07c`
  (=本档复查轮档件提交);主二进制 sha256
  `186c41b9724a48469fc1ba4e14561afd29a2b691f95005b132639a87dedf6b83`,
  换装前后双验命中(codesign 两包同态失败已入 problems,不构成 hash 判据阻碍)。
- **换装五步(全按 [[packaged-app-verify-and-swap-race]] 判例)**:
  1. 验源:新包主二进制 sha256=`186c41b9…dedf6b83` 亲验命中(codesign 两包同态失败已入 problems)。
  2. 退实例:`pkill -x MYIA`(原 PID 50032 + sidecar 50037 双静默退场)。
  3. 备份换包:`/Applications/世事.app` mv 至 `/tmp/myssia-app-backup-20261006-002250/`
     再 ditto 新包入位;装后主二进制 hash 复验命中。
  4. 清缓存:`rm -rf ~/Library/WebKit/com.myssia.app` 与
     `~/Library/Caches/com.myssia.app`,ls 确认双目录已不存在。
  5. 亮窗取证:`MYIA_SHOW_ON_START=1` 直跑 `/Applications/世事.app/Contents/MacOS/MYIA&`
     (setup done 171ms + sidecar spawned),窗 id=23128(CGWindowList);
     取证全程 `screencapture -x -o -l23128`(无影 3840x2100=精确 2x,坐标换算 scale=2)。
- **导航取证**:cliclick 点左轨「设置」(屏坐标 41,1058,由 OCR 归一化坐标换算)
  → 设置默认区取证 installed-settings-nav.png → 点「Python 环境」(318,289)
  → 取证 installed-python-env.png + 镜像区裁片 03-mirror-zone.png(对照帧
  00-boot-noshadow.png)。收尾 `pkill -x MYIA`,app/sidecar 双静默,系统恢复
  安静;未 commit 未 push。注:本机 :8080 的 mlx_vlm.server 为本收口会话开始前
  已在跑的他流进程,未动;备份包保留在 `/tmp/myssia-app-backup-20261006-002250/世事.app` 未删。
- **证据图**:`.zcode/smoke/pyenv-unify/installed-python-env.png`、
  `installed-settings-nav.png`、`03-mirror-zone.png`、`00-boot-noshadow.png`。
- **OCR 四要件结论(双引擎:Vision 一级 OCR + 本机 Qwen3-VL-8B 二级,
  按 local-ocr 纪律因关键行 conf≤0.5 升级)全中**:
  - (a) 左侧「过滤分区」标题(conf 1.00)+ 七项分区导航全常驻:通用/推送/视觉/
    门槛件/装机组件/Python 环境/系统——几何一致(x≈513-676@2x 图,y 中心
    179/246/313/380/450/517/586,~67px 等距);VL 独立点数「共 7 项」逐项同名。
  - (b) 无「返回设置」:全图 grep「返回」=0 命中,VL 答「无」。
  - (c) 卡头「◎ 环境状态与安装」:Vision 坐标 (1423,235) conf 0.50,
    VL 定向复核「有,原文:环境状态与安装,Python 运行环境下方第一个大模块标题」。
  - (d) 双镜像行式:「运行时下载源覆盖」标签(x1418-1669,y1117-1145)与输入
    `https://mirror.example/cpython-3.12.7.`(x2740-3214,y1134-1168)y 带重叠=同行;
    「PyPI 镜像覆盖」标签(x1418-1630,y1240-1274)与输入
    `https://pypi.tuna.tsinghua.edu.cn/simple`(x2740-3220,y1262-1290)y 带
    重叠=同行;两行均标签左/输入右,非全宽上置;VL 独立同判「两处均为同一行
    左右排布(标签左、输入框右)」。
- **读回附录**:页状态「就绪」,安装路径
  /users/zhengbingjin/Library/Application Support/MYIA/python,Python 使用路径
  .../python/bin/python3,安装明细 5 步(下载运行时/校验 sha256/解压到数据根/
  pip 安装依赖/自检;1 已完成 4 已跳过),可选组件区(表格还原等,未装)。
  对照图 installed-settings-nav.png=设置默认「通用」区:同款过滤分区+七项导航+
  「LLM 精评与代理池凭据 + doctor 诊断」卡头,版面结构一致。
- 本回执就此销号「遗留与移交·装机包刷新 + 换装像素终验」条目的终验半项
  (其前半「刷新+换装」已于 2026-10-05 销号,见上方装机包销号注记);
  归档随 grill Q1(a) 当场执行(→ `.trellis/tasks/archive/2026-10/`)。
