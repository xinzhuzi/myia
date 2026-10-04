# 执行计划——桌面自管 Python 环境

前置:PRD 决议 D1-D6 与 design.md 已定案(2026-10-05 主人批);执行按序,每步带验证门。

## 顺序清单

- [x] 1. 随包交付物:myssia 源码打包进 tauri resources + 入口模块(`myssia_desktop_entry`,复用 entry.py 协议面)+ `runtime-manifest.json`(钉主人 URL+sha256 实算+win 等效件)+ `requirements-lock.txt`
      门:resources 内容清单核验;锁版清单与 pyproject 一致性测试
      → 2026-10-05 回标(波A)。门禁:随包交付物 门禁(uv)绿。质检:忠实于 implement.md 第 1 条与 design.md §2;D1-D6 无违背,IPC 契约与并行第 2 步对齐,未发现漏验。逐项实证:(1) D3 钉版——脚本逐字节比对 PRD 决议原文与 manifest mac URL 完全一致;独立下载双包复算:mac sha256=4c18852b…f9508/15,641,754B、win f05531bf…d547a/38,116,958B,与 manifest 及自述尺寸全对;tar -tzf 实证两包根目录 python/、mac python/bin/python3、win python/python.exe、pip 自带(mac bin/pip + win Lib/site-packages/pip 24.1.2,862 文件)、win 为同 release 20241016 x86_64-pc-windows-msvc-install_only。(2) D1——六文件改动域干净:tauri.conf.json 仅 +5 resources 映射(externalBin 未动);src/myssia 纯 Python(非 .py 仅 2 个 enrich prompt JSON 包数据,2.3M);运行时/依赖零进包;入口包直载同父 entry.py 复用协议面,与 tests/desktop/test_desktop_sidecar_protocol.py:33-35 同一 importlib 手法,无拷贝。(3) D2/D4——改动域内无任何下载逻辑;锁版清单全 name==version 钉版(禁 editable/路径/URL 有测试把守),uv export --frozen 再生 diff 仅文件头注释 + classifier 钉版行(自述「唯一手改」属实),pip -r 重跑幂等基础成立。(4) 零重叠声明——git diff 实证 desktop/entry.py 改动全为 gates.get/save(并行 plugin-market 批)、main.rs/Cargo.toml 改动全为 pyenv 探测(第 2 步),第 1 步未碰任何 Rust/entry.py。(5) tauri 映射语义——cargo registry 内 tauri-utils 2.10.1 源码(resources.rs next_pattern/resource_from_path)实读核实:map 形非 glob 目录源=Walk 递归+strip_prefix 结构保真,glob 形拍平文件名——选型正确,包结构可保。(6) IPC 对齐——pyenv.rs(第 2 步在途)ENTRY_ARGS=[-m,myssia_desktop_entry,serve] 与 __main__.py argv 契约一致(serve→serve 循环/其余直通,镜像 entry.py:4990-4994 __main__ 语义,cli_main None=sys.argv[1:] 口径同 cli.py:5495);RESOURCE_SRC_DIR=myssia-src、RESOURCE_LOCK_FILE=requirements-lock.txt 与映射 dest 一致;python_bin 路径(python/bin/python3、python/python.exe)与 pyenv.rs 硬编码一致;manifest 平台键=Rust target triple 且为资产文件名片段(测试三方互证)。(7) 定向验证——uv run --no-sync python -m pytest tests/desktop/test_pyenv_resources.py -q = 20 passed in 0.43s(未跑全量,遵嘱);ruff check 新 Python 文件全绿;npx tauri info 无 error/warning。双门(resources 内容清单核验/锁版↔pyproject 一致性测试)均有测试落地且实跑通过。质检未跑:tests/desktop 全目录 155(自述数,未复跑)、tauri build(第 7 步门)。
      遗留(low,desktop/src-tauri/tauri.conf.json:48-50):本机开发构建会把 gitignored __pycache__ 打进包体(目录直映射 map 形 Walk 递归无排除,本机 src/myssia 下 __pycache__ 实测 6.0M、desktop/myssia_desktop_entry/__pycache__ 亦在)——CI 干净新检出台面不受影响(gitignore 第 48 行),Python 按 mtime+size 校验 pyc 不构成正确性问题;非违背,归第 7 步打包链裁量(确认加排除或打包前清理)。
      遗留(low,desktop/resources/requirements-lock.txt:4-6):锁版再生成依赖人工重做 classifier 钉版替换(-e ./myssia-classifier 行→PyPI myssia-classifier==0.0.1,uv export 原生产物含 -e 行桌面 pip 装不了,须按文件头注释手改);已有 test_requirements_lock_classifier_pypi_pin 把守,但流程依赖人读注释。design.md 标注 --require-hashes 可选加强未开,同为已知留白,非本步门。
      实现摘要:交付五件——(1) tauri.conf.json resources +5 映射(../../src/myssia→myssia-src/myssia、../entry.py→myssia-src/entry.py、../myssia_desktop_entry→myssia-src/myssia_desktop_entry、../resources/runtime-manifest.json→runtime-manifest.json、../resources/requirements-lock.txt→requirements-lock.txt;externalBin 未动退役归第 7 步;未碰 src-tauri/src 下任何 Rust 文件,与并行第 2 步零重叠;目录映射语义按 tauri-utils 2.10.1 源码实读核实,map 形非 glob 目录源=递归 Walk、相对结构保真到 dest,resources.rs:225-236/293-309)。(2) 入口包 desktop/myssia_desktop_entry/{__init__,__main__}.py:importlib 直载同父 entry.py 复用协议面(与 tests/desktop/test_desktop_sidecar_protocol.py:33-35 同一手法,零拷贝防漂移);__main__ 镜像 entry.py __main__ 语义(serve→serve();其余→cli_main(argv));开发树(desktop/)与资源树(Resources/myssia-src/)同形布局,ENTRY_PY 相对定位两态恒成立;desktop/entry.py 一字未动。(3) desktop/resources/runtime-manifest.json:mac URL=主人 D3 钉定原文逐字节一致,win=同 release 20241016 x86_64-pc-windows-msvc-install_only 等效件;sha256 均下载原包实算且 shasum 二次复算一致;tar -tzf 实证两包根目录均 python/、pip 自带;平台键用 Rust target triple(与资产文件名片段一致,第 2 步壳可按 build triple 取条目)。(4) desktop/resources/requirements-lock.txt:uv export --frozen --no-dev --no-emit-project 冻结解析产物,唯一手改=workspace 成员 classifier -e 行钉为 PyPI myssia-classifier==0.0.1(PyPI 实查已发布,uv.lock 解析版本同 0.0.1,满足 pyproject >=0.0.1,<0.1)。(5) tests/desktop/test_pyenv_resources.py 20 例四组:resources 声明↔磁盘实况逐条、manifest 钉版/指纹/布局自洽三方互证、锁版↔pyproject 逐条 name==version 校验(packaging.SpecifierSet 实校验)+禁 editable/路径/URL+classifier 钉版单守、入口包与直载 entry.py 的 PROTOCOL_VERSION/_HANDLERS 零漂移+真进程冒烟(PYTHONPATH=desktop:src、MYIA_HOME 沙箱:serve version 往返应答 protocol=10 且 EOF 退出 0;--version 直通 rc=0)。验证(实施会话实跑):tests/desktop/test_pyenv_resources.py 20 过;tests/desktop 全目录(含并行会话在途改动)155 过;tests/test_docs.py+test_smoke.py 115 过;npx tauri info 配置解析无误。遗留注记:(a) __pycache__ 归第 7 步打包链裁量;(b) tauri build 包体实测(<118M)与 desktop-release.yml 适配是第 7 步门,本步未跑;(c) 锁版再生成需按文件头注释重做 classifier 钉版,已有测试把守。
- [x] 2. Rust 壳:环境探测(就绪/未配置/依赖漂移三态)+ spawn 改造 + `pyenv_not_ready` 空态事件
      门:壳侧单测;未配置态启动不崩(UI 空态可见)
      → 2026-10-05 回标(波A)。门禁:Rust 壳三态与 spawn 门禁(cargo)绿。质检:高危发现(spawn 缺 serve 尾参、与第 1 步入口模块 argv 契约冲突)已闭合,修复走壳侧且形态正确——pyenv.rs:47 新增常量 ENTRY_ARGS=["-m", ENTRY_MODULE, "serve"](注释钉死契约出处:第 1 步 __main__.py 要求 argv[0]=="serve" 才进 RPC;明示 design §4 字面省了 serve 尾参、以入口模块 argv 契约与第 1 步测试为准);main.rs:184 改用 .args(pyenv::ENTRY_ARGS);pyenv.rs:519-522 新增回归测试 entry_args_pin_serve_argv_contract 钉死 argv 防回退。质检亲验:cd desktop/src-tauri && cargo test → 19 passed(18 原有+1 新回归);就绪态 stub python 沙箱冒烟(MYIA_HOME=mktemp 根)→ stub 实收 ARGV="-m myssia_desktop_entry serve",MYIA_HOME/PYTHONPATH 注入不变,「setup done(sidecar spawned)」。真进程 serve version 往返未跑(本机 dev python 缺 apscheduler,此前实证 -m 即 import 断),该链由第 1 步门禁 tests/desktop/test_pyenv_resources.py:275(钉同一 argv 形态做真进程 serve 往返)覆盖,本轮未跑该 pytest。
      遗留(medium,desktop/src-tauri/src/main.rs:71):中危发现未随本轮修复——sidecar_request 未就绪分支仍将 unready_error 内层 {code:pyenv_not_ready,data:status} stringify 后包进外层 {code:sidecar_not_running}(main.rs:71-79),前端 client.ts:128-142 一层解析拿不到 pyenv 状态;非本次复查范围,如实注记,第 4 步前端落地前仍建议修。
      实现摘要:修复质检唯一高危项(spawn 缺 serve 尾参致就绪主链断)。根因:按 design.md §4 字面写 .args(["-m", ENTRY_MODULE]),而第 1 步落地的 desktop/myssia_desktop_entry/__main__.py:26-30 要求 argv[0]=="serve" 才 entry.serve(),否则 cli_main(args)——cli.py:5518-5520 空参 print_help 退出 EXIT_OK,sidecar 起即死(respawn 烧尽转 dead)。修复三件:pyenv.rs 新增 pub const ENTRY_ARGS: [&str; 3] = ["-m", ENTRY_MODULE, "serve"] 并注释钉死 argv 契约出处;main.rs spawn_sidecar 改 .args(pyenv::ENTRY_ARGS),spawn_sidecar 与 pyenv.rs 模块头注释同步补 serve 说明;新增回归测试 entry_args_pin_serve_argv_contract 防尾参回退。验证(全部实跑):cd desktop/src-tauri && cargo test → 19 passed 0 failed(18 旧+1 新);cargo check --locked → Finished 干净,警告/错误 grep 计 0;rustfmt --edition 2021 src/pyenv.rs 后 fmt-clean。沙箱冒烟双态复验(debug 二进制 + mktemp MYIA_HOME):①就绪态 stub python 实被拉起,argv 恰为「-m myssia_desktop_entry serve」,MYIA_HOME=沙箱根、MYIA_APP_VERSION=0.0.1、PYTHONPATH=<resource_dir>/myssia-src,日志「sidecar spawned」,进程 5s 存活;②未配置态(空根)回归尤在:5s 存活、stderr「Python 运行环境未就绪(state=NotConfigured),不 spawn sidecar」+「setup done…skipped(环境未就绪)」。未跑:tauri build/vitest/tsc/pytest(全量门归脚本);未碰 tauri.conf.json/desktop/resources/tests(第 1 步域)。
      主人侧待办:tauri build / vitest / tsc / 全量 pytest 未跑,归脚本统一全量门禁;UI 空态可见(引导卡渲染)与真链路 serve version 握手端到端分别属第 4/5 步波次,本步 stub 冒烟已验 argv/env 注入契约与第 1 步入口模块对齐。
- [ ] 3. 安装链执行器(壳内):状态机+幂等进度戳+sha256 校验+磁盘预检+错误分类
      门:单测(含坏包/中断重试);本地静态服务器钉版文件全链真跑
- [ ] 4. 设置屏区块:开始配置/路径/双镜像覆盖/安装明细/同步依赖
      门:vitest+tsc;IPC 契约测试
- [ ] 5. 依赖安装与自检:pip 锁版装 + sidecar version ping 自检
      门:沙箱数据根端到端(AC1 主链)
- [ ] 6. 存量迁移:首启检测+一次性引导(D5)
      门:旧数据根夹具测试,数据零丢失断言
- [ ] 7. 打包链收口:build-sidecar.sh/spec 退役注记、desktop-release.yml 适配、tauri.conf externalBin→resources
      门:tauri build 出包且包体显著小于 118M;CI 门控绿
- [ ] 8. 文档与装机:docs zh/en getting-started 新安装叙事;装机冒烟+静默换装
      门:AC1-AC5 逐条回标;AC6 Windows 真机留主人侧;AC7/AC8 核验

## 回滚点

- 任一步后均可回退:数据根布局不变,旧冻结版包可直接重装回落(数据无损)
- 打包链退役放最后一步,之前任一态都可双轨(冻结版照发)

## 风险盯点

- python-build-standalone 下载源可用性(镜像覆盖是正门)
- pip 国内连通性(索引覆盖是正门)
- 依赖锁版与 myssia 源码随包版本漂移 → 同步依赖按钮兜底(D4)
