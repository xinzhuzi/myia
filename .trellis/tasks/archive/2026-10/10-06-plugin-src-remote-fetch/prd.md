# PRD:插件分发新规范——声明随包、源码远取(10-06-plugin-src-remote-fetch)

> 立档:2026-10-06 · 来历:主人令已批立项(「按照新规范,先做个计划,然后执行」)
> 优先级:P1 · 类型:打包规范改造 + 安装动线改造(源码面桌面侧,零 Rust 逻辑改动)
> 规范出处(主人原话,2026-10-06):**「是这些源码不能随包,但是这些配置可以」**

## 1. 规范不变量(本档宪法,一切设计与实现不得违背)

| # | 不变量 | 判定口径 |
|---|--------|---------|
| INV-1 | 装机包内插件组件包**只准携带配置/声明件**:`plugin.yaml` + `README.md` | Resources/plugins/<id>/ 下出现其余任何文件即违例 |
| INV-2 | 插件**源码不得进包**:adapter.py、场景件(如 render_crawl4ai.py)、自有子包(如 credhunter/) | 同上 |
| INV-3 | **数据件不得进包**:vendor/(submodule 上游源码)、缓存(__pycache__ 等) | 同上 |
| INV-4 | **MYIA 自身 python 核心(myssia-src/)是产品本体,不属此列**——随包不变 | src/myssia + entry.py + runtime 五映射照旧 |
| INV-5 | 安装动线**远取必须内容寻址**(release tag 或 commit sha + sha256);失败=**结构化错误,零静默** | 装出的每一件可追溯到锁钉的字节 |
| INV-6 | **已装机旧件零扰动**:~/.myia/plugins/<id> 已装件不迁、不改、不删;卸载/版本语义不变 | InstalledPluginStore 契约零变更 |
| INV-7 | dev / 本地仓库通道保留:`myssia plugin install plugins/<id>`(cli.py:4519)照常;dev 构建不注入 MYIA_BUNDLED_PLUGINS 语义照旧 | pyenv.rs:255 零改动 |

## 2. 违例矩阵(2026-10-06 实测基线)

测量物:`desktop/src-tauri/tauri.conf.json` bundle.resources 现映射 + 实构建包 `desktop/src-tauri/target/release/bundle/macos/世事.app/Contents/Resources/plugins`(564K 实测)+ 仓库 plugins/ 源树。

**11 个随包组件包分型**:

| 分型 | 件 | 现随包内容 | 违 INV-? |
|------|----|-----------|----------|
| 纯声明(合规样板) | myssia-firecrawl、myssia-mediacrawler | plugin.yaml + README.md | 无 ✓ |
| 带 adapter.py 源码 | myssia-maigret / myssia-media / myssia-proxy / myssia-snownlp / myssia-yake | plugin.yaml + README.md + adapter.py | INV-2 |
| 带 adapter.py + 第二源码件 | myssia-urlwatch | 上述 + render_crawl4ai.py | INV-2 |
| 源码 + 自有子包(数据件) | myssia-credhunter | 上述 + credhunter/ 整目录(216K,13 个 tracked 文件,adapter compile+exec 自举依赖) | INV-2 + INV-3 |
| 源码(上游 vendor 仓内 submodule,现未随包) | myssia-osint(vendor/Photon 204K)、myssia-theharvester(vendor/theHarvester 5.3M) | 仅 plugin.yaml + README + adapter.py;vendor 以 .gitmodules submodule 钉、**刻意不随包**(GPL 分发红线,test_installer_resources.py 头注既有裁定) | INV-2(adapter 面) |

**与立项矩阵的对账(诚实记录)**:立项时给的矩阵按「插件目录整目录口径」计(osint 204K/theharvester 5.3M 计入 vendor、__pycache__ 计 4 件、合计约 6MB);本档实测按「resources 实映射口径」:osint/theharvester 的 vendor **现就不在映射内**(既有 GPL 红线裁定先行),__pycache__ 由 beforeBuildCommand `npm run clean:pycache`(tauri.conf.json:8)+ 逐文件映射天然排除(实测包内 0 个)。**两边规范结论一致:9/11 件带源码违 INV-2,credhunter 另违 INV-3;收窄后随包面从 564K 降至声明级(约 40K 内)**。差异仅是分型口径,不影响任何 R/AC。

**既有事实基础**:

- manifest `install.source` 字段(schema 见 src/myssia/plugins/manifest.py:117-119「供人与 agent 追溯」)已在 21 处 plugin.yaml 声明 `https://github.com/xinzhuzi/myia.git`(grep 实测)——远端源概念有雏形但**仅人读,机器从未消费**;且该 URL 是远端改名(myia→shishi)前的旧指针,仓库现远端实为 `https://github.com/xinzhuzi/shishi`(2026-10-06 `git ls-remote` 实测可达且 HEAD=1accccd 与本地一致)。
- 现安装链:`plugins.bundled.install`(desktop/entry.py:1014-1051)从包内 `MYIA_BUNDLED_PLUGINS` 目录直拷 → `InstalledPluginStore.install`(src/myssia/plugins/installed.py:267,manifest 校验→版本矩阵→整目录拷贝绝不半装)。包内没源码后此链必断——远取即为此而生。
- 内容寻址 + 远取 + sha256 校验的仓内判例:desktop/resources/runtime-manifest.json(Python 运行时按 url+sha256+archive 下载校验)——本设计照此形态。
- GitHub release 面已存在:repo 有 v0.0.1 release(2026-10-03,gh release list 实测)。

## 3. 需求(R)

- **R1 打包收窄**:tauri.conf.json resources 对 11 组件包只保留 plugin.yaml + README.md 两映射;新增随包 `plugins.lock.json`(远取锁,见 R3);删除 adapter.py / render_crawl4ai.py / credhunter 子目录等全部源码与数据件映射。品类 YAML(monitor/credentials/官方 7 件等)与 demo 件、fixture plugin.yaml 属「配置」,**维持随包不变**。
- **R2 远取安装动线**:`plugins.bundled.install {id, force?}` 改为:读包内 plugins.lock.json → 按 url 拉组件包 tar.gz → sha256 校验 → 安全解包到数据根暂存 → 走既有 `InstalledPluginStore.install` 同门(manifest 校验/版本矩阵/整目录拷贝/绝不半装/已装未 force 拒)。落点、版本钉、卸载语义与 CLI 完全不变。
- **R3 远取锁(内容寻址事实源)**:单文件 `plugins.lock.json` 随包,记 `{repo, tag, assets: {<id>: {url, sha256, size}}}`;由发布前置脚本生成(打包 plugins/<id> → 上传 release 资产 → 记 sha256)。**机器事实源是锁,plugin.yaml install.source 仍归人读溯源**(决议 D6)。
- **R4 结构化失败词表**:无锁/无条目(`plugin_lock_missing`)、网络失败(`plugin_fetch_failed`,带 HTTP 状态)、校验不符(`integrity_mismatch`)、包损坏(`plugin_archive_invalid`)——全部 ProtocolError 结构化应答+中文消息,UI 可见,零静默零半装。
- **R5 兼容三层**:①旧装机包(带源码)安装路径仍可用——锁缺席时回退现「包内直拷」路径(决议 D3);②已装机已装件零扰动(INV-6);③dev/本地 checkout 通道照旧(INV-7)。
- **R6 门禁与发布流程**:①test_installer_resources.py 断言**反转**为新规范(声明两件必须在;源码/vendor/子包/pycache 必须不在);②新增锁覆盖门禁(11 件全有条目 + 格式钉);③远取全 mock 测试(httpx MockTransport + 夹具 tar.gz,零网络,repo 测试纪律);④justfile 增发布前置目标(产锁+传资产),文档同步。

## 4. 验收标准(AC)

> 勾选口径(收尾员 2026-10-06):亲跑/亲验=勾;commit 记录+过程段在档的按记录引注;未做=不勾留因。

- [x] **AC1(打包合规)**:新构建包 Resources/plugins 下 11 组件包目录**仅** plugin.yaml+README.md(逐件逐文件断言);包内零 `*.py`、零 vendor/、零 __pycache__、零 credhunter/ 子目录;根级多出 plugins.lock.json。门禁测试钉死,回退即红。——**全部达成**:前两句已验并钉死(test_installer_resources.py 49 例门禁反转,commit 0c624c4;收尾轮亲验验证包构建产物:Resources/plugins 恰 32 件,`find -name "*.py"` 计 0);末句「根级 plugins.lock.json」随批4 收口(2026-10-06 主人令「按照你的建议做完」):真锁 desktop/resources/plugins.lock.json(tag v0.0.2,11 件 sha256/size/version 实测值)入树+tauri.conf resources 映射+锁门禁 tests/desktop/test_plugins_lock.py(真载入器解析/恰覆盖 ALL_BUNDLED_PACKAGES/tag v* 形态/条目内容寻址自洽/resources 有映射)——坏包窗口封口,锁缺席/欠件即 CI 红
- [x] **AC2(远取安装)**:装机态 `plugins.bundled.install {id}` 按锁拉包→sha256 校验→落 `~/.myia/plugins/<id>`,应答 `{ok, dir, version}` 契约不变;装后 `plugins.bundled.list` 该件 installed=true 版本对;已装未 force 结构化拒;`plugins.bundled.uninstall` 照旧可卸。全 mock 测试绿。——tests/plugins/test_plugin_remote_fetch.py(45 例)+tests/desktop/test_bundled_plugins_install.py(远取主路径端到端含 list 已装态对账/已装零网络先拒)全 mock 绿,commit 9f2dc9a;收尾轮亲跑三测试文件 136 passed(0.39s)。注:真机点装随批4(真锁不存在时真机只能验回退与结构化拒,远取成功路径不可能真机验)
- [x] **AC3(失败面)**:四类失败(R4 词表)各至少一测:错误码原文、data 带 url/sha256 期望实得等定位信息、零半装残目录(暂存目录失败即清)。——plugin_lock_missing/plugin_fetch_failed(带 status)/integrity_mismatch(带期望/实得/url;深审批 cb09dda 加 size 前置对账 expected_size/actual_size)/plugin_archive_invalid(恶意件八形参数化)全覆盖,零残件 finally 断言;commits 9f2dc9a+cb09dda;收尾轮亲跑 136 passed 含此面
- [x] **AC4(旧包零扰动)**:锁缺席 + 包内有源码(旧包形态夹具)→ 回退包内直拷安装成功;已装件目录在新链路任何操作后逐字节不变。——回退夹具+「已装旧件跨成功+失败+列表+卸他件四操作逐字节零扰动」测试,commit 9f2dc9a;深审批 cb09dda 复验 D3 旧包回退六形态+__pycache__ 污染拒;收尾轮亲跑绿
- [x] **AC5(dev 通道)**:仓库 checkout 上 `myssia plugin install plugins/myssia-proxy` 照常(既有测试不红);dev 构建不注入 MYIA_BUNDLED_PLUGINS,list 合法空态不变。——dev 本地目录直装通道零锁零远取加测钉死(9f2dc9a INV-6/7);收尾轮亲跑全量 pytest 4873 passed 40 skipped(113s),含 CLI/入口全链
- [x] **AC6(发布链)**:`just <新目标>` 一条命令产 dist 资产 + plugins.lock.json(11 件全覆盖,sha256/size 实测值);锁格式与覆盖率有离线门禁测试;发布流程文档(desktop README 或 justfile 注释)更新。——**达成**(批4 收口轮 2026-10-06,主人令「按照你的建议做完」):`just release-plugins <tag> [--dry-run]` 门面落 justfile(含纪律注释);desktop/scripts/release-plugins-lock.mjs 零依赖 node(git archive 逐件+:(exclude)vendor+tar 成员双保险断言+确定性复跑同 sha 实证+dist 与锁逐字节 sha 一致亲验);真锁已产(tag v0.0.2,11 件实测值);锁门禁 tests/desktop/test_plugins_lock.py;文档=justfile 注释(desktop README 不存在,落点按 D7 允许)。**资产上传是显式发布动作未执行**(v0.0.2 release 时跑 `just release-plugins v0.0.2` 即传,gh --clobber 幂等)——发布窗动作,非缺陷;manifest.install.sha256 回填自指不可行维持 cb09dda 裁定(锁为唯一机器事实源,声明面漂移走 warning)
- [x] **AC7(规范入档)**:INV-1~3 写入 test_installer_resources.py 模块 docstring(替代旧「源码面随包」裁定文案);`.trellis/spec` 相应指南补一条分发规范引用(落点 implement 定,允许仅指向本档)。——docstring 重写入档(0c624c4);spec 落点收尾轮落地:connector-selection.md 硬规则「插件源码不随包」+sidecar-protocol.md #64 三岔语义同步+security-baseline.md 远取完整性门(本收尾笔)

## 5. 决议节(待裁点已按推荐自决,全部可翻案)

| # | 裁点 | 决议(推荐采纳) | 备选与翻案条件 |
|---|------|----------------|---------------|
| D1 | 远取载体 | **per-plugin release 资产 tar.gz + 锁钉 tag+sha256**(合主人「release tag + sha256」措辞;单件 KB~百 KB 级;gh release 判例已有) | 整仓 codeload tar.gz(实测压缩 68MB,过重,弃);git clone 按_sha(需用户机 git 二进制,Windows 不保,弃)。翻案条件:若发布资产流程成为负担→退整仓 tar + 数据根缓存 |
| D2 | 锁形状/落点 | 单文件 `plugins.lock.json` 放 Resources/plugins 根(pyenv.rs 零改动,env 注入目录现成);schema `{manifest_version, repo, tag, assets:{id:{url,sha256,size}}}` | 每包一锁(冗余,弃);锁进 plugin.yaml(混人读/机读语义,弃) |
| D3 | 旧「包内直拷」路径 | **保留为锁缺席时的回退**(旧装机包自愈,零硬切风险),不设删除时点 | 硬切删除(翻案条件:确认存量旧装机包可忽略时) |
| D4 | 远取代码落点 | 新核心模块 `src/myssia/plugins/remote.py`(锁 schema + fetch + sha256 + 安全解包;sidecar 与未来 CLI/市场面复用;测试进 tests/plugins/) | entry.py 私有函数(sidecar 独占,复用差,弃) |
| D5 | vendor(theHarvester/Photon) | **不进远取资产**(GPL 零分发红线沿既有裁定;装机 vendor_missing 结构化指引既有)。「点装即全功能」留增强批:按 manifest vendor.pin(SRC 已有,如 theharvester plugin.yaml pin ba853666)直连上游 tar.gz,链接者形态 | vendor 随资产分发(越 GPL 红线,不取);翻案:主人若要开箱即用,加批5 上游 vendor 远取 |
| D6 | plugin.yaml install.source 旧 URL(myia.git ×21) | **零扰动不批量改**(纯人读字段,机器事实源=锁);锁内 repo 用现远端 shishi | 顺手批量改 shishi(纯文档面,可翻案加急件) |
| D7 | 版本升级语义 | 复用 force 覆盖装;不做「远端版本>已装自动升级」比对(UI 后续增强) | 自动升级(需 store 契约扩展,超出本档 INV-6,不取) |
| D8 | 暂存与缓存 | 暂存目录 `~/.myia/plugins/.staging/<id>-<短随机>`(同文件系统原子 rename 进 store;失败清残);**不做 tar 包磁盘缓存**(单件小,缓存复杂度不值) | 缓存层(翻案条件:D1 翻到整仓 tar 时必须加) |

## 6. 边界(非目标)

- 不动 Rust 逻辑(pyenv.rs/main.rs 零源码改动;仅 tauri.conf.json 资源表收窄)。
- 不动 InstalledPluginStore 契约、不动品类补种(_seed_first_run)、不动 myssia-src 随包面。
- 不做插件市场远端索引/自动发现(锁只服务「已声明 11 件的源码远取」)。
- 不做 vendor 上游自动拉取(D5 留增强)、不做代理配置面(httpx 沿 trustenv 读 HTTPS_PROXY 既有行为)。

## 7. 风险

| 风险 | 处置 |
|------|------|
| GitHub release 资产被删/重传 → 装机报 integrity_mismatch | 结构化错是设计内应答;可后补 CI 巡检锁健康(非本档 AC) |
| test_installer_resources.py 现钉旧行为,反转幅度大 | 批2 专项翻案该文件,与 test_pyenv_resources.py 分工(彼管运行时五映射)核对不变 |
| 装机真网验收受环境限制 | 核心链路全 mock;装机验收走 house 装机外科流程(沙箱包 + MYIA_SMOKE_GEOMETRY 小窗,静默铁律) |
| 锁时点纪律:发布后补插件修复需重产锁+重传资产 | just 目标幂等可重跑;发布文档写明步骤(AC6) |
| 资产上传需发布机 gh 权限 | 发布本就需 gh;零新增凭据面 |
