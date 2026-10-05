# 推送/装机收口回执(2026-10-05,10-05-plugin-market-batch)

> 回填会话:文档收口者(2026-10-05 午后,回填时点 HEAD=origin/main=4986c58,工作树仅余 journal 禁入脏件)。
> 标注口径:「本次实测」=本会话亲跑命令/亲读文件;「引自回执」=换装会话原始汇报,本会话未复验;「主人终态」=收口矛盾上报后主人裁示附带的终态实况(其中可实测的关键面本会话已复核,见文内)。
> 收口矛盾处置存照:收口指令原定提交信息称「CI 绿回执」,经 `gh run view` 实查 run 37264825568 conclusion=failure,上报后主人裁示按终态实况如实落档(选 A),不粉饰为绿。

## 一、推送与 CI 回执

**基线推送(收口指令指定 run)**:sha `18558c05`,run **37264825568**(event=push,branch=main,2026-10-05T04:44:25Z)。本次实测(gh run view/run list/--log-failed)conclusion=**failure**,工位明细:

| 工位 | 结论 |
|---|---|
| Python lint(ruff minimal set) | success |
| Docker image build check | success |
| Rust compile check(desktop/src-tauri) | success |
| UI component tests(desktop/ui-src) | **failure**(仅该 sha 红;自 8818401 的 run 37265937040 起复绿) |
| test(pytest) | **failure** 9 例,双归因见下 |

pytest 9 红双归因(本次实测失败日志逐条读出):

1. `tests/desktop/test_pyenv_resources.py::test_components_resource_declared_and_present` ×1——`resources 缺映射 '../resources/components.json' -> 'components.json'`。归因=18558c0 漏件,**40ac920 已修**(tauri.conf resources 映射补提交),已随本轮推送上 origin。
2. `tests/vision/test_vision_table.py::TestRunTableEngine` ×8——`ModuleNotFoundError: No module named 'numpy'`。归因=**CI 环境缺装**(非代码红):本地 HEAD 本次实测同款命令 `uv run --no-sync python -m pytest -q --tb=line tests/desktop/test_pyenv_resources.py tests/vision/test_vision_table.py` = **52 passed, 1 skipped**(0.54s)。定性 CI 环境债务,记 notCovered/遗留(见 §四-1)。

**推送终态(主人终态+本次实测复核)**:8818401..**4986c58** 共 6 笔已推 origin(f1543dd/781ee9c/654c225/40ac920/3ead799/4986c58);`git rev-parse origin/main` = 4986c58f5321… 亲验一致。**4986c58=entry.py 补种锚点修复+协议测试随更**(desktop/entry.py +29/-9、tests/desktop/test_desktop_sidecar_protocol.py +27,git show --stat 亲验)——即换装会话原「已修复但源码未提交」两件,现已入库。

**新 run**:37268141209 @4986c58(2026-10-05T05:31:04Z 起)收口时点 status=**in_progress**(重跑中,结果未出)。主人裁示:新 run 结果不阻塞收口,回执如实记「修复已推、CI 重跑中、上轮红因双归因」。main 末绿 run=37260642705@ef6846c(03:44:40Z,gh run list 亲验);37264825568 之后至 8818401 的 4 个 run 全为 failure(UI 红自 8818401 消,pytest 9 红同因存续)。

## 二、净室构建回执

- **入口**:`/tmp/myia-cleanbuild`(非 git 树,仓库快照拷贝;desktop/entry.py 于 13:14 手工同步同款修复,`entry.py.orig` 237226B 留证,本次实测在位)。
- **产物**:`/tmp/myia-cleanbuild/desktop/src-tauri/target/release/bundle/macos/世事.app`。
- **自验(本次实测)**:exec(MacOS/MYIA)sha=`ed9ec422`;`Resources/myssia-src/entry.py:522` 修复锚点在位(`if src_root.name == "myssia-src":`);`Resources/components.json` 随包(python3 解析实读:顶层 dict,`components` 列表=['table']);`Resources/plugins` 18 项=9 品类 YAML(ai-news/exposure/games/gpu-prices/myssia-demo/news/stocks/wool+demo)+9 桌面件目录。
- Info.plist 双构建均 0.0.1、本轮 Rust 未动(引自回执;与 exec sha 未变互证)。

## 三、换装回执(含 13:16:16 反覆盖事故与回装终态)

**数据根**:`~/Library/Application Support/MYIA`(壳侧 main.rs:305-314 MYIA_HOME 注入规则,本次实测亲读)。

**时序复原**(四份 /tmp 备份+stat mtime 交叉实测;执行主体归属按主人终态):

| 时刻(10-05 本地) | 事件 | 证据 |
|---|---|---|
| 13:04:56 | 原始包备份 → `/tmp/世事.app.bak-20261005-130456`(exec d45c4dd6,entry.py 无锚点,components.json 有) | 实测 |
| ~13:14 | 修复前构建曾装入(exec ed9ec422 无锚点,后被 table 线备份为 bak-table-131425) | 实测(备份内容) |
| 13:15:44 | 备份 → `/tmp/世事.app.bak-20261005-131544-r1`(exec **99c6b3ca**,无锚点,无 components.json)——内容与换装回执对「-r1」的描述(ed9ec422+死补种)不符,错位注记见 §四-4 | 实测 |
| 13:16:04 | **修复版装入 /Applications**(Info.plist mtime;exec ed9ec422+锚点+components.json)并启动 → 补种落位 | 实测(mtime)+补种面实测 |
| 13:16:16 | **并行 table 线反覆盖**:备份修复版 → `/tmp/世事.app.bak-table2-131616`(ed9ec422+锚点+components.json,本次实测=修复版快照),换入其自家构建 86448d35(entry.py 无锚点——修复彼时未提交,git 打包面带不上;managed 形态补种就此失效) | 实测 |
| 13:31:11 | **修复版回装 /Applications**(主人终态;table 线包备份 → `/tmp/世事.app.bak-tableline-133111`,实测在位) | 实测复核 |

**现行装机包(回装后本次实测)**:`/Applications/世事.app` exec=`ed9ec422`、`Resources/myssia-src/entry.py` 锚点**在位**、components.json 有、app mtime 13:31:11。回装后亲验(主人终态列示,补种面本会话独立复测一致):进程活;games/news/exposure 补种在位;ai-news 用户本未覆盖;旧名 myia-demo.yaml 遗留并存。

**补种实证(本次实测,数据根)**:

- 补种四件落位 `~/Library/Application Support/MYIA/plugins/`,与随包源逐字节 sha 一致:exposure=`7f6d8e65`、games=`092a077d`、myssia-demo=`9df680ec`、news=`a68b3f4f`(数据根 vs 包内 Resources/plugins 同名件 shasum 对比,八值两两相同)。
- **不覆盖语义(AC5)**:ai-news.yaml 数据根用户本 `743847a6` ≠ 包内 `181ae05e`——用户改本未被覆盖(引自回执的尺寸口径 8606/8610,本次以 sha 复证同结论)。
- `.seeded` 标记:内容 `2026-10-03T02:53:08.097+00:00`、mtime 定格 Oct 3 10:53(首次补种时刻定格、复种不重写语义,entry.py `_seed_first_run` marker 逻辑亲读互证)。
- 旧名 `myia-demo.yaml` 与 `myssia-demo.yaml` 并存(遗留,§四-2)。

**门槛缺省态(本次实测)**:数据根无 gates.yaml(fd 全搜 `~/Library/Application Support` 无命中);`MYIA_HOME=<数据根> uv run --no-sync myssia gates show --json` = `{"exists": false, "config": {"paid_engines": false, "third_party_trace": false, …}}`,exit 0——fail-closed 全关缺省成立。

**未复验项(引自回执,如实注)**:启动 ring 日志文字证据(sidecar『品类补种 4 件』行写进程内 ring,统一日志 grep 不到,以文件级证据为准);二次启动幂等 sha/mtime 零变化;既有五件与换装前快照逐件比对;设置面 UI 未开窗直验(守静默纪律不抢焦点不截图)。

**根治面(主人终态+实测)**:entry.py 补种锚点修复已提交推送(4986c58)——此后任何线从 git 重打的包都自带修复,反覆盖不再伤补种。

## 四、遗留

1. **numpy CI 环境缺装 8 红**(tests/vision/test_vision_table.py):本地两文件亲跑全绿,CI `uv run --no-sync` 环境缺 numpy;待 CI 依赖面修(环境债务,非代码红)。新 run 37268141209 结果未出,若仍红预期即此因。
2. **旧名 demo yaml 保留**:数据根 myia-demo.yaml(旧名)与 myssia-demo.yaml 并存,未清理(用户数据不动的裁量,如实记)。
3. **Resources 市场面包安装接线未做**(Resources/plugins/<pkg> 作市场安装来源的发现/一键通道),prd AC5 已注「后续件另立」。
4. **备份名/内容错位注记**:`-r1` 备份实测内容(99c6b3ca/无 components.json)与换装回执描述(「修复前 ed9ec422+死补种资源」)不符——该描述与 bak-table-131425 内容吻合(时线:table 线 13:14:25 前后换件所致)。以本回执 §三备份表实测内容为准。
5. **设置面 UI 未开窗直验**;启动 ring 日志文字/二次启动幂等/五件快照比对引自回执未复验(§三末条)。
6. **反覆盖事故存档**:table 线 13:16:16 反覆盖使修复版在 /Applications 仅存活 12 秒;已回装终态如 §三,备份链五份(/tmp 四份+tableline 一份)全在位可溯源。
