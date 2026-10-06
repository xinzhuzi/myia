# implement.md — 10-06-plugin-src-remote-fetch 执行计划(先档后行,批间门禁)

> 批序设计原则:**先立新链路、后拆旧包袱**——远取先行(旧包源码仍在,随时可退),打包收窄落在远取可用之后,同发布周期内两批必须同船发布(收窄后的包没有旧直拷源码,锁缺席回退在新包上自然失效为 plugin_lock_missing,这是预期语义)。
> 每批完成即回填本档过程段 + 提交(只提交自有文件);门禁统一 `uv run --no-sync pytest -q`(全量)+ ruff;涉及 UI/tsc 面加 `npm --prefix desktop/ui-src run build`。

## 批1:远取核心模块(无前置,可先动)

1. `src/myssia/plugins/remote.py`(design D3/D4):PluginsLock pydantic schema(manifest_version/repo/tag/generated_at/assets)+ `load_plugins_lock`(缺文件=None 回退语义;坏文件 `plugin_lock_invalid`)+ `fetch_plugin_asset`(httpx 同步,trustenv,60s 超时,`plugin_fetch_failed` 带 status)+ `verify_sha256`(`integrity_mismatch` 带期望/实得)+ `extract_staging`(tarfile,py3.12 filter="data" / 3.11 手工防穿越双保险,成员剥 `plugins/<id>/` 前缀,`plugin_archive_invalid`)+ `install_remote` 编排(finally 清 .staging 残目录)。
2. 测试 `tests/plugins/test_plugin_remote_fetch.py`(design D8 表:MockTransport 四态 + 夹具 tar.gz 好/坏/zip-slip 恶意件 + staging 清残 + 成功路径落 store;零网络)。
3. 门禁:定向 pytest(tests/plugins/)+ ruff;全量 pytest 亲跑绿。

## 批2:entry.py 安装编排 + 旧包回退

1. `desktop/entry.py` `_m_plugins_bundled_install` 改三岔(design D5):锁在+条目在→`install_remote`;锁缺+包内目录有源码件→现行直拷路径零改动回退;否则 `plugin_lock_missing`。应答 `{ok, dir, version}` 契约不变;ProtocolError 包装沿现模式(entry.py:1044-1050)。
2. `list`/`uninstall`/`category_install` 核对零改动(装后 installed 态、卸载语义测试沿既有)。
3. 测试 `tests/desktop/test_bundled_plugins_install.py` 扩展:远取主路径(mock remote.install_remote 或 MockTransport 夹具锁)/旧包回退夹具(锁缺+源码在)/新包无条目结构化拒/已装未 force 拒。
4. 门禁:定向 pytest(tests/desktop/)+ 全量 pytest + ruff。

## 批3:打包收窄 + 门禁反转(与批1/2 同发布周期,顺序在后)

1. `desktop/src-tauri/tauri.conf.json`:11 组件包收敛为 plugin.yaml+README.md 两映射;增 `plugins.lock.json` 映射;删 adapter.py ×9 / render_crawl4ai.py / credhunter 子目录映射。品类/demo/fixture/myssia-src/运行时件**不动**(design D6)。
2. `desktop/resources/plugins.lock.json` 首版手工生成(批4 脚本就绪前可先由批4 脚本产出;批3 允许临时占位——**占位不得进提交**,发布前必换真锁,批5 验收钉)。
3. `tests/desktop/test_installer_resources.py` 断言反转(design D8):11 件 × 两声明必须在;全 map 键空间负断言(`*.py`/vendor/credhunter 子包/__pycache__ 不存在);docstring 重写为新规范(AC7,引主人原话+本档);品类/运行时面断言保留。与 test_pyenv_resources.py 分工核对(彼管运行时五映射,不牵连)。
4. 新锁门禁(tests/desktop/ 内):锁 11 件全覆盖 + tag/sha256(64hex)/url 前缀自洽 + resources 有锁映射。
5. 门禁:全量 pytest + ruff + `cd desktop/src-tauri && cargo check --locked`(conf 改动零源码,但按 just check 口径走全)。

## 批4:发布链脚本(可与批1 并行起步)——**未做**(收尾轮 2026-10-06 亲验:脚本/justfile 目标/真锁/锁门禁四件全缺;锁映射随本批同船=批3 偏离记录①;深审批 cb09dda 实证「同源回填 manifest.install.sha256」自指不可行,落地时需另裁;留主人裁后续)

1. `desktop/scripts/release-plugins-lock.mjs`(design D7):git archive 逐件产 dist/plugin-<id>.tar.gz + 双保险断言(vendor//__pycache__/*.pyc 不入资产)+ 计 sha256/size + 写 desktop/resources/plugins.lock.json(tag=argv)+ `gh release upload <tag> dist/plugin-*.tar.gz --clobber`。
2. justfile 新目标 `release-plugins tag=<tag>`(纯门面);`build-desktop` 不自动串(发布是显式动作)。
3. 发布流程文档:justfile 注释 + desktop README(或 docs/)「动插件源码必重跑 release-plugins」一段。
4. 门禁:脚本 `--dry-run`(只产 dist+锁不传)本机亲跑;锁门禁测试绿。

## 批5:装机外科验收 + 收口——**部分完成**(步骤1 打包验证+声明面截图留痕已做、真机点装五连无回执在档;步骤2-4 由收尾轮完成,见过程段)

1. 真包验收(静默铁律:MYIA_SMOKE_GEOMETRY 小窗无焦点,禁 open -a):沙箱构建新包 → 装机 → ①设置页随包插件卡 11 件全可见(声明面);②点装一件(proxy 类纯源码件)真网真装 → installed 版本对、`~/.myia/plugins/<id>` 树完整;③断网点装 → 结构化错误可见;④已装件(装机前预置)零扰动逐字节比对;⑤卸载重装循环。
2. AC1-AC7 逐条销号(过程段记录证据:命令+输出/像素验证留痕)。
3. `.trellis/spec` 引用落点(AC7 允许仅指向本档):desktop/sidecar-protocol.md 或 guides 加一行分发规范引用。
4. 过程/结果段回填;task.json 置 review;提交批次收口(只提交自有文件,绝不 push)。

## 停点与依赖

- 批1/2/4 无外部前置,可立即动;批3 依赖批1+2(收窄前远取必须已可用,防「包内无源码且无远取」断档)。
- 批5 依赖真发布 tag + 资产已上传(锁内 url 真可达);装机外科遵循 house 既有沙箱包流程。
- 全程不动:Rust 源码(pyenv.rs/main.rs)、InstalledPluginStore 契约、品类补种、myssia-src 随包面。

## 过程段(随做随填)

- 2026-10-06 立档:规划师-建档完成 prd/design/implement 三件套;task.json 直改 in_progress(并行会话在场,禁 CLI start,沿 10-06-telegram-telethon 判例)。
- 2026-10-06 批3 打包净化线(实施员-打包净化,与安装远取链并行):tauri.conf.json resources 11 组件包收敛为 plugin.yaml+README.md 两映射(删 adapter.py×9/render_crawl4ai.py/credhunter 整目录映射;逐文件 map 语法无需过滤脚本);test_installer_resources.py 断言反转(INV-1~3 入 docstring、11 件×两声明正面参数化+键空间恰两件精确断言+*.py/vendor/credhunter 子包/__pycache__ 全 map 负断言;品类/场景安全面原样;DESKTOP_TIER_PACKAGES 等 4 常量名值保留——test_bundled_plugins_install.py 跨文件 import)。真构建实证:`npm --prefix desktop run tauri -- build --bundles app`(既有链:clean:pycache→vite→cargo release→bundle)解包 Resources/plugins:564K→204K(du)/134,508 字节、52→32 文件、零 *.py/零 __pycache__/零 vendor/零 credhunter,Resources 根 myssia-src(125 .py)/fixture/运行时三件原样(INV-4)。门禁:test_installer_resources 49 绿+pyenv 两文件 31 绿、`uvx ruff@0.16.10 check .` 全过、`cargo check --locked` 绿、`cargo test --locked` 80 过 0 挂、vitest 577/577。**偏离记录**:①批3 的 plugins.lock.json 映射与锁门禁(条目 1 尾/2/4)未随本批——真锁由批4 发布链产出,implement 明文「占位不得进提交」,映射指向不存在文件会断打包链,故锁映射+锁门禁随批4 真锁同船;②构建期源钉注入 plugin.yaml 设计上不存在(prd 决议 D6:install.source 零扰动、机器事实源=锁),该注入口 N/A;③全量 pytest 现挂 2+若干红全在安装远取线在途文件(test_bundled_plugins_install.py 旧规范反断言两测=批2 翻案面 + 新 test_plugin_remote_fetch.py 中途态),本线不碰,收口批5 全量门禁核。
- 2026-10-06 批1+批2 安装远取链(实施员-安装远取链,与批3 打包净化并行):新核心模块 src/myssia/plugins/remote.py(锁 schema pydantic 自洽:manifest_version==1/repo https/tag 无斜杠/sha256 严格 64 位小写 hex/size>0/资产 url 必须落 {repo}/releases/download/{tag}/ 前缀/资产键过 _PLUGIN_ID_RE,载入即拒 plugin_lock_invalid 带 errors 明细;缺文件=None 回退语义)+ fetch_plugin_asset(httpx 同步 trustenv+follow_redirects 60s,非 2xx/网络层失败=plugin_fetch_failed 带 status|reason+url)+ verify_sha256(integrity_mismatch 带期望/实得/url)+ extract_staging(成员白名单:相对/无 ../无反斜杠/拒符号硬链接与设备件/plugins/<id>/ 唯一顶层前缀剥壳,py≥3.12 filter="data"+老补丁位手工双保险,mode 剥高位,违例=plugin_archive_invalid 且零残件)+ install_remote 编排(已装未 force 零网络先拒→拉→验→解包 <安装根>/.staging/<id>-4hex→InstalledPluginStore.install 同门落位,成败 finally 清残;解包期 OSError 包 io_error)。错误面全走 PluginStoreError 子系(PluginRemoteError 基类带 data 定位信息)。manifest.py install.source 升为内容寻址引用(可选 sha256——与锁共用新公开 SHA256_HEX_RE 零漂移——与 size,旧仓库 URL 零迁移向后兼容,fail-fast 路径精确到 install.*)。entry.py _m_plugins_bundled_install 三岔编排:锁在+条目在→远取;否则定位目录(_locate_bundled_plugin_dir 原样,未知 id 仍 bundled_plugin_not_found)携源码件(*.py 或非隐藏子目录)→旧包直拷回退(D3);否则 plugin_lock_missing(数据带 lock_present);锁文件坏=plugin_lock_invalid 不静默降级直拷;应答 {ok,dir,version} 契约不变,PluginStoreError 包装增远取 data 并入(errors 同旧)。**语义细化记录(对 design D5 字面)**:旧包纯声明件(firecrawl/mediacrawler 类)锁缺席时归 plugin_lock_missing——与 implement 批序注「新包锁缺席自然失效为 plugin_lock_missing 预期语义」同源取舍,防新包锁缺失时直拷声明件静默半装;过渡形态(锁在无条目+包内携源码)仍直拷自愈。InstalledPluginStore/cli.py 零改动(INV-6/INV-7;dev 通道 store.install(<本地目录>) 零锁零远取原样,加测钉死)。测试:tests/plugins/test_plugin_remote_fetch.py 45 例(全 mock 零真网:锁载入矩阵/四态拉取/sha256 对错/恶意件八形参数化/编排成败零残/已装零网络/store 门透传/本地通道/manifest 声明面向后兼容)+ tests/desktop/test_bundled_plugins_install.py 扩展 9 例(远取主路径端到端含 list 已装态对账/无锁拒/无条目拒/坏钉拒带双 digest/HTTP 失败拒带 status/坏锁拒/已装零网络/已装旧件跨成功+失败+列表+卸他件逐字节零扰动/锁在无条目+携源码回退)+ 两 map 耦合测试翻案:test_bundled_package_files_are_fully_mapped→test_bundled_declaration_files_are_mapped(反向对账收敛到声明面,源码面负断言归 test_installer_resources 键空间门)、roundtrip 翻为远取路径真官方 manifest 逐字节对账(锁条目优先于包内形态,**收窄前后两世界皆绿**,不依赖批3 在途状态)。门禁:定向 tests/plugins/+tests/desktop/ 绿;全量 pytest 主树(含批3 在途收窄 conf)4867 过 0 挂、HEAD 干净 worktree(/tmp/myia-remotefetch-check,仅本线五文件)4863 过 0 挂;uvx ruff@0.16.10 五文件全过;零新依赖(httpx 核心既有)。golden 面:tests/ 无 plugins.bundled 载荷 golden 夹具,manifest 增字段全带缺省、InstalledEntry.to_dict 未动→协议载荷逐字节不变(全量绿佐证)。未尽:批4 发布链脚本与真锁产出(锁映射随批4 同船,批3 偏离记录①)、批5 装机真网验收与 AC 逐条销号。
- 2026-10-06 批5 装机打包验证(实施员-装机验证,cb09dda 后):干净树沙箱构建 /private/tmp/myia-pkg-verify/clean(`npm --prefix desktop run tauri -- build --bundles app` 全链:clean:pycache→vite→cargo release→bundle,BUILD-EXIT=0,世事.app 17.31 MiB;evidence/pkg-build.log 全文在档);构建产物 Resources/plugins 收尾轮亲验:恰 32 件=10 声明 YAML(games/monitor/ai-news/wool/stocks/credentials/news/exposure/gpu-prices+myssia-demo)+11 组件包×(plugin.yaml+README.md),`find -name "*.py"` 计 0、零 vendor/credhunter 子包/__pycache__、plugins.lock.json 缺席(批4 未做,如实)。设置页/插件列表截图 5 张留痕(evidence/pkg-settings.png、pkg-plugins-{full,mid,tail,tail2}.png,23:10-23:14)——**收尾员模型无图像输入未亲读像素,以实施员留痕身份入档**;批5 步骤1 之②③④⑤(真网点装/断网点装/已装件零扰动真机比对/卸装循环)**无文本回执在档,不可考,如实记**——真锁缺席(批4)下远取成功路径本不可能真机验,仅回退与结构化拒可验,亦无回执。
- 2026-10-06 收尾(收尾员):地面对账四 commits 全在(0c624c4 批3/9f2dc9a 批1+2/cb09dda 深审修复/批5 验证件 evidence 不入 git 按主人令),工作树本任务源码零残留(仅任务档未跟踪,两笔补提交:任务档现状笔+收尾文档笔,排除 evidence/reports 于笔A、reports 并入笔B)。收尾轮亲跑门禁:三测试文件定向 136 passed(0.39s)+全量 pytest 4873 passed 40 skipped(113s)+ruff@0.16.10 All checks passed;验证包键空间亲验如上。spec 三处:connector-selection.md 追加硬规则「插件源码不随包」(主人收尾令原文)、sidecar-protocol.md #64 三岔语义同步(旧「目录映射→直调」描述与 9f2dc9a 漂移,核对抓出)、security-baseline.md 补远取链完整性门(锁双门/解包白名单/清残)。prd AC 勾选:AC2/3/4/5/7 勾(亲跑+commit 双据),AC1 不勾(锁面随批4,余句全验)、AC6 不勾(批4 整批未做);task.json 置 review;交付报告 reports/run-report.md。
