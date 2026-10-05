# 桌面自管 Python 环境:包体不冻结,设置页按需下载

## Goal(主人指令,2026-10-05)

「这个软件自己创造一个 py 环境,打包时不应该将这个相关的 py 软件打入包体,让用户自己在设置里面自己下载。」

桌面端从 PyInstaller onefile 冻结 sidecar(118M,Python+依赖+模型全在包内)切换为 **MYStudio 已验证的自管环境模式**;grill 五问已全批(2026-10-05,主人「按照你的建议」+ 亲自钉定运行时 URL),决议如下。

## 决议(grill 2026-10-05 定案)

- **D1(交付形态)**:myssia 自有源码**随包**交付(纯 Python,轻,版本与壳严格配对);Python 运行时与第三方依赖**一律不进包**,运行期下载安装。
- **D2(首跑体验)**:引导空态——未配置时各依赖 sidecar 的屏显「Python 运行环境未配置」卡+一键跳设置;**不自动后台下载**(主人原话:让用户自己下载),配置动作 = 设置页显式点「开始配置」。
- **D3(运行时与依赖来源,主人钉 URL)**:运行时 = **indygreg/python-build-standalone `cpython-3.12.7+20241016`**,macOS 默认源 = 主人钦定
  `https://github.com/indygreg/python-build-standalone/releases/download/20241016/cpython-3.12.7+20241016-aarch64-apple-darwin-install_only.tar.gz`
  (Windows 取同 release 的 `x86_64-pc-windows-msvc-install_only` 等效件;mac 当前只发 aarch64,与现行 dmg 单架构一致)。依赖 = 环境内 `pip install` 按**锁版清单**(随包)。**双镜像可覆盖**:运行时包 URL、PyPI index 均可在设置页替换。
- **D4(更新解耦)**:壳更新(更新包骤降,不再含 Python)与依赖更新解耦;app 更新后依赖有漂移时,设置页出现「同步依赖」一键**幂等**重跑安装链,不强制自动。
- **D5(存量迁移)**:新版首启检测旧数据根——**数据零迁移**(myssia.db/plugins/models/keychain 全兼容沿用),仅提示「新版改为自管 Python 环境,需一次性配置」引导进设置;旧冻结二进制随 app 更新自然消失。
- **D6(后续件)**:表格还原等可选重件(前议)作为该环境的可选组件,环境立好后另行立档;vision extras 转设置开关进同一环境。

## Requirements

1. 包体剥离:安装包不含 Python 运行时/第三方依赖/内置 OCR 模型;含 myssia 源码、依赖锁版清单、sidecar 入口、运行时 sha256 校验清单。
2. 设置页「Python 运行环境」区块:开始配置/安装路径/使用路径/下载源(双镜像覆盖)/安装明细;下载→校验→解压→pip→自检全链状态可见,失败可重试。
3. Rust 壳拉起改造:sidecar spawn 从冻结二进制改为 `<数据根>/python/bin/python3 + 随包入口模块`;未配置时壳不 spawn,UI 走引导空态,协议层报「未配置」结构化状态。
4. 数据根布局:`<数据根>/python/`(install_only tar.gz 解压即得)与既有 `models/` 并排;绝不写安装目录/源码目录;开发 Python 与应用 Python 分家(MYStudio 铁律)。
5. 存量迁移与更新解耦按 D4/D5。

## Acceptance Criteria

- [ ] AC1 全新 mac 装机端到端:装包(包体显著小于 118M)→ 首启引导空态 → 设置「开始配置」→ 下载钉版运行时(默认 URL=D3)→ 校验+解压数据根 → pip 锁版装依赖 → sidecar 起活(version ping 过)→ 源管理/情报流/定时全功能;断网/坏包中途失败可重试续装
      【留主人:真机「开始配置」→下载→自检→全功能目验——真机数据根(~/Library/Application Support/MYIA)无 python/、无 python-env.json,链未在真机跑过;沙箱端到端(隔离数据根+真 15MB 钉版 runtime+pip+serve)审计轮亲跑 2 passed,见收口段】
- [ ] AC2 未配置态:所有依赖 sidecar 的屏引导卡不崩溃;设置页显示路径/源/明细
      【gap,不勾:后半句 met(settings-screen.tsx:133-135 python-env 分区+pyenv-card 路径/双镜像/五阶段明细/同步依赖);前半句无载体——grep 实证 ui-src 全域 pyenv_not_ready 事件零消费者、「Python 运行环境未配置」文案零命中(壳 main.rs:241-242 发事件,设置屏外唯一 pyenv 引用=migration-banner.tsx),且 docs/zh/getting-started.md:30、docs/en:39 已把该不存在 UI 写成既有行为。第 4/6/8 步质检三次 flag 的任务级掉缝。补卡前须先修 main.rs:70-81(内层 pyenv_not_ready 被 stringify 包进外层 sidecar_not_running)】
- [x] AC3 镜像覆盖:运行时 URL 与 PyPI index 均可设置覆盖并实测生效
      → 2026-10-05 审计回标(met)。证据:tests/desktop/test_pyenv_e2e.py 双镜像经 pyenv-settings.json(与设置页 IPC 同一落盘)指向本地静态服务器,:644 断言 simple-package 记账 ≥20(索引覆盖生效)、:748 二跑零网络,审计轮亲跑 2 passed(11.74s);UI 双镜像输入+「只换 URL 不绕 sha256」hint 在 pyenv-card.tsx:241;提交 95bff40(e2e)/198b0c5(UI)。
- [x] AC4 更新解耦:壳更新不含 Python;「同步依赖」幂等(重跑结果一致、已装跳过)
      → 2026-10-05 审计回标(met)。证据:50b622c tauri build 出包 16.43 MiB 零 Python+装机 /Applications/世事.app 亲验 17M(Contents/MacOS 仅 MYIA 壳);幂等=e2e force 二跑全 skipped/零网络面/指纹不变(审计轮亲跑);「同步依赖」按钮仅 deps_stale 态渲染(pyenv-card.tsx:169-177)。
- [x] AC5 存量迁移:旧数据根数据零丢失沿用,一次性引导出现且仅出现一次
      → 2026-10-05 审计回标(met)。证据:e43481b pyenv_migration.rs 7 例夹具单测(含递归快照逐字节零丢失断言+出现且仅出现一次含模拟重启)+ vitest 8 契约例;真机旧数据根(myssia.db/plugins/models 非空)在位且无迁移标记,首启将触发横幅——真机走查留主人(注记非缺口)。
- [ ] AC6 Windows 等效链(CI 门控;真机冒烟按 win-local-build 先例留主人侧)
      【留主人:desktop-release.yml:163-168 windows-msi job 在位(50b622c 已去 sidecar/uv 段),GitHub CI 未 dispatch 实跑(第 7 步质检如实记录);真机 win 冒烟按 AC 原文明示留主人侧】
- [x] AC7 CLI/PyPI 发行通道零变化
      → 2026-10-05 审计回标(met)。证据:git log 实证本档九笔提交(08e163d…23faa27)全部只碰 desktop/、.github/、justfile、docs/、tests/desktop/,零触碰 CLI/PyPI 发行面——src/myssia/cli.py 末笔 d613310(push 批)、pyproject.toml 末笔 b864d2b(10-04);ask 所列 entry.py(fa10443)/installed.py/manifest.py 改动均属并行批非本档域。
- [ ] AC8 门禁:全量 pytest + vitest + tsc + tauri build 绿;装机冒烟+静默换装按交付纪律;docs zh/en getting-started 同步新安装叙事
      【留主人:分步门禁记录绿(aa89aa5 全量 4074+vitest 433+tsc0;198b0c5 vitest 448+tsc0;50b622c tauri build+tests/desktop 172)+docs zh/en 23faa27 已落地;但装机换装回执仅覆盖 03:06 b72fee4 过渡谱系(cc42e0d 冒烟绿),机上新形态 17M(04:21 换装)装机冒烟无回执、全量门禁未统一复跑——收口验收留主人】

## 非目标

- CLI 端发行形态不变;核心包依赖红线不动;不做运行时代码热更(仅环境与依赖管理);不做 mac x86_64 架构。

## 收口(2026-10-05 审计回填)

**口径修正(待开工令 → 已实施)**:本档 prd 立档后 AC 一直全未勾、check.jsonl/implement.jsonl 均 0 字节,呈「待开工令」形态;实际已由并行会话按同一 grill 五决议(D1-D6)分四波实施完毕(波A 第 1/2 步 → 波B 第 3/4 步 → 波C 第 5/6 步 → 波D/E 第 7/8 步),implement.md 八步全 [x] 且带逐波质检回标。档面与实际的漂移以本段修正:任务已实施,非待开工。审计中途档案已被并行会话归档(4afdd6c,2026-10-05 11:20:06,task.json 同步翻 completed 但时点在 AC 回标之前);本段与上方 AC 回标落在归档副本(archive/2026-10/10-05-desktop-managed-py-env/)上,task.json 按「有 gap 不进 review」收口规则回到 in_progress、completedAt 回退 null,归档位置与状态的一致性留主人裁定。

**核验方法**(2026-10-05,只读审计 + 域内 scoped 自检):
- 完整读档:prd.md/design.md/implement.md(93 行全)/task.json;git log --oneline -50 检索,任务落地提交九笔——08e163d(第 1 步随包交付物)/f2e0194(第 2 步壳 spawn+ENTRY_ARGS)/aa89aa5(并行收编,含 Cargo sha2/tempfile 补交+pyenv-api.ts)/cdade3e(第 3 步幂等安装链)/198b0c5(第 4 步设置屏区块)/95bff40(第 5 步沙箱端到端)/e43481b(第 6 步存量迁移)/50b622c(第 7 步打包链退役+出包)/23faa27(第 8 步双语文档),装机回执 cc42e0d。
- 审计轮亲跑:`uv run --no-sync python -m pytest tests/desktop/test_pyenv_resources.py tests/desktop/test_pyenv_packaging.py -q` → 30 passed in 1.26s;`uv run --no-sync python -m pytest tests/desktop/test_pyenv_e2e.py -q` → 2 passed in 11.74s;`uv run --no-sync ruff check`(六 pyenv 件)→ All checks passed。脚本门禁 G1(tests/plugins+tests/test_gates.py)/G2(世事 plugin list,2 件可用、0 错 0 警)均退出码 0。cargo test/全量 pytest/vitest/tsc/tauri build 本轮未复跑(scoped 限单文件),以各步质检记录与提交口径为准。
- 钉版核验:desktop/resources/runtime-manifest.json:12 mac URL 与本档 D3 逐字节一致(grep -F 双文件命中);win 为同 release 20241016 x86_64-pc-windows-msvc 等效件;Cargo.toml:24 sha2/:43 tempfile 在位(aa89aa5 补交)。
- 真机 spot check:/Applications/世事.app 为新形态 17M 包(MacOS 仅 MYIA 壳、Resources 含 myssia-src/runtime-manifest/requirements-lock,binary mtime 10-05 04:21:52);数据根 ~/Library/Application Support/MYIA 旧数据(myssia.db/plugins/models)在位,无 python/、无 python-env.json、无 pyenv-settings.json、无 pyenv-migration.json。

**结论**:AC3/AC4/AC5/AC7 勾;AC1/AC6/AC8 留真机与 CI 面验收;AC2 实质缺口不勾——D2「各依赖 sidecar 屏引导卡」全仓未落地(证据见 AC2 行),且双语文档已先行把它写成既有行为,公开发布即虚假陈述。

**留主人清单**:① AC1 真机「开始配置」→下载→自检→全功能目验(沙箱链已过,真机数据根未配置);② AC2 裁定——补 D2 引导卡(连带先修 main.rs:70-81 嵌套)或改 docs/zh:30+en:39 表述,可另立档;③ AC6 desktop-release.yml windows-msi job dispatch 演练+真机 win 冒烟;④ AC8 新形态包装机冒烟回执(03:06 b72fee4 过渡谱系有 cc42e0d 冒烟绿,04:21 新形态换装无回执)+全量门禁统一复跑;⑤ 归档(4afdd6c)与 in_progress 状态的最终裁定;⑥ 已知 low 遗留沿袭 implement.md(MYIA_PYENV_AUTOSETUP env 面随包长存 main.rs:420、镜像 URL 无 scheme 强制、docs/{zh,en}/build-windows.md 全文仍按退役 sidecar 链叙事、pyenv_install.rs:1101 同步依赖后不重启在跑 sidecar)。

## 补记(2026-10-05 午后:设置页全局版面判例落地)

**主人判例(截图质询原话)**:「设置这个里面的配置没有放到中心,布局太小家子气了,应该全局布局的,不应该缩到一处地方」。

**根因(主人窗口 931px CSS 实测)**:①配置卡被双重导航挤压——app 左轨 224px + 设置分区导航 176px + 间距后,python-env 分区仅剩 459px 宽(旧 max-w-[600px] 钳制根本未生效,宽度瓶颈在导航挤压而非列宽);②分区列注释声称对齐 Kestra「居中单列」但实现漏 mx-auto;③卡内为 Kestra SettingRow 窄行范式(w-64 右置控件、路径 truncate 截断、五阶段密集行堆),全局看呈「缩在右侧一隅的窄长条」。

**修法(本档第 4 步 UI 重排,属 AC2 同域但独立于引导卡欠账)**:
- settings-screen.tsx:python-env 分区激活时隐藏设置分区导航列并解除 md:flex-row,配置面占满主画布居中(max-w-4xl);加「返回设置」退路(深链直入走得通);其余分区维持 600px 窄列不动。
- pyenv-card.tsx:卡内改全宽元素——状态横幅(左边框随五态着色)/路径块 break-all 全显不截断/镜像输入全宽(不走 w-64 右置控件族)/五阶段竖向时间线(圆点+连接线,done✓/running 脉冲/failed✗)/底部动作条主按钮去 sm 收缩。IPC 契约与全部 data-testid 零动。

**验证**:vitest 53/53(pyenv-card 13 + settings 40);tsc -b + vite build 绿;无头冒烟(Playwright+__TAURI_INTERNALS__ shim,mock pyenv_get_status)——931×857 档卡宽 459→659 占满主画布、1512 档 896 居中(主画布内左右对称 196/196)、零横向溢出、「返回设置」回导航正常;DOM 裁切检查零命中;OCR 全文可读(路径不再截断)。VL 三条负面主张(文字重叠/左对齐未居中/导航空白)经 DOM+OCR 交叉证伪,不采信。
**装机回执(2026-10-05 12:0x)**:净室构建(git archive HEAD=bac3ce4,target 软链复用依赖缓存,cargo 13.45s)→ 世事.app 16.81 MiB + dmg 7.73 MiB;结构验过(MacOS 仅 MYIA 壳/Resources 含 myssia-src+钉版 manifest+锁版清单);UI 内容链验过(随包主 chunk 含「返回设置」与 pyenv-start-setup 锚);静默启动冒烟(open -g,PID 活、零新崩溃)→ 静默换装 /Applications/世事.app(先验源再删旧,ditto 落位 17M)。部分回填 AC8 装机冒烟欠账(04:21 新形态无回执项)。
**AC1 真机主链回执(2026-10-05 12:08)**:主人机经 MYIA_PYENV_AUTOSETUP=1 钩子(与「开始配置」同一条安装链,发布包无人设此 env、D2 产品行为不变)静默触发——75 秒全链完成:downloading/verifying/extracting/installing_deps/selfcheck 五阶段全 done,state=ready,deps_fingerprint a89418…落盘;Python 3.12.7(cpython-3.12.7+20241016 钉版)落位数据根 89M(含 94 项锁版依赖);安装链收尾 spawn_sidecar_if_idle 实证拉起常驻 sidecar(pgrep myssia_desktop_entry serve 在跑)后干净退出零残留。回填留主人清单①的真机链部分;「全功能目验」仍留主人(重开 app 即验)。注:触发面是钩子非人工点按,链本体与点按完全同源。
**装机自测回执(2026-10-05 午后二段,主人令「自己测试,别等我动手」)**:①设置页(装机件真窗口截屏验):「← 返回设置」+标题+就绪横幅+全宽路径+镜像区+五阶段时间线全「已完成」,分区导航隐藏、内容占满主画布左右留白对称——全局版面在装机件实锤;②情报流屏:工具栏/空态渲染正常零 IPC 报错(sidecar 数据面健康);③环境功能面:自管 python 透传 myssia CLI 全命令面,plugin list 真库 2/2 可用零错零警;④冷启动回执「setup done in 196 ms(sidecar spawned)」。**坑入册(换装纪律级):二进制换装后 WKWebView 缓存旧 chunk 混搭态(表现=新设计渲染但局部新件缺席,像素级 y80-185 纯背景可辨),净室构建+二进制哈希+内嵌块名三验皆过也会中招;解法=换装后清 ~/Library/Caches/com.myssia.app/{WebKit,WebsiteData} 再冷启(本次清后「返回设置」即现);后续换装链应把清 web 缓存固化为一步。**
**补记(2026-10-05 午后三段:就绪态按钮语义分家,主人判例)**:主人原话「已完成这个按钮状态就要改成检查状态,如果状态不对,就重新安装,这才是正常的功能」——落地:①壳侧新 IPC `pyenv_install::pyenv_verify`(三查=python 二进制可执行/依赖指纹 vs 随包锁版清单/sidecar version 握手【与安装链 selfcheck 同源】;只读零副作用不落戳不翻状态不碰网络);②设置卡主按钮按态分家——就绪=「检查状态」(pyenv-verify-button)、异常=「重新安装」、安装中=「安装中…」、未配置/漂移=「开始配置」;③体检未过 → 问题逐项上屏(pyenv-verify-problems)+「重新安装」入口(pyenv-reinstall-button → pyenv_start_setup 幂等链);ready/error 态提示文案同步。门禁:vitest 65(3 档)+cargo 53+tsc+build 绿;装机件像素级自测见后段回执。
**补记(2026-10-05 午后三段附:AC2 嵌套包装缺陷顺刀修)**:体检失败路径真机验证时曝光 main.rs:79-81 嵌套包装在屏裸奔(结构化 pyenv_not_ready 被整串塞进 sidecar_not_running 的 message,顶部横幅显示整块 JSON blob)——修法=unready 分支早返原样直出不再套信封;cargo check+53 测过;真机复验见装机回执。
**装机回执(2026-10-05 午后三段)**:快照树打包(git stash create b34200c0/47bc08eb,含并行 table-restore 已提交与在途接线件——打包前全量门禁在该确切树上亲跑: vitest 65+cargo 53+tsc+build 全绿)→ 换装(备份 /tmp/世事.app.bak-v3-*,清 webview 缓存)→ 双态像素级自测:**就绪态**=「检查状态」钮在位(v3 x2912/y2010 实证)+横幅干净+hint 带「可随时点检查状态复验」;**失败路径**(真藏 python 二进制)=状态翻「异常」(戳记 ready 但缺位→error,判定链如设计)+「重新安装」hint 在位+**AC2 嵌套包装修复实证:顶部横幅由整块 JSON blob 变为干净的「Python 运行环境异常…」+code=pyenv_not_ready**(1f897e2);恢复二进制后复启 sidecar 即拉起(stamp ready)。提交:f333417(按钮分家+pyenv_verify)/1f897e2(嵌套修复)。
