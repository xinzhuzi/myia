# 装机包 plugins 发现/一键安装接线(壳 env 注入 + sidecar 两新方法 + 设置屏新分区)

## Goal

装机包内已随包分发的官方插件组件包(Resources/plugins/<pkg>,10 件)目前只有启动时的品类 YAML 补种面,没有「发现可装件 + 一键安装」的通道。本件接通:壳层把资源目录锚点经 env 注入 sidecar(单一事实源),sidecar 暴露 `plugins.bundled.list` / `plugins.bundled.install` 两新方法,设置屏新增「装机组件」分区逐包展示与一键装(整目录拷贝过 manifest 校验,复用市场安装语义)。

母任务计划定案(2026-10-05 傍晚收口后,基线上下文 ⑥):plugin-market-batch AC5 收口注记「发现/一键安装接线不在本件范围后续件另立」即本件。

## Requirements

1. **壳层发现通道(Rust)**:main.rs `spawn_sidecar` 段(:193-203,PYTHONPATH/MYIA_HOME/MYIA_APP_VERSION 同点)增注 env `MYIA_BUNDLED_PLUGINS=resource_dir()/plugins`(pyenv.rs RESOURCE_SRC_DIR 同源锚点判例,4986c58 myssia-src 同款):
   - **release 且 env 未显式设才注入**(MYIA_HOME 同款「已设则原样继承不夺权」惯例;自动化冒烟可直跑二进制显式注入);
   - **dev 构建定死不注入**(dev 态 resource_dir 无组件包,注入会枚举仓库 plugins/ 20 件含未打包 myssia-crawlab/myssia-credentials 等,断言数字两态漂;dev=空表是稳定契约);
   - 注入逻辑抽纯函数(`pyenv.rs`),cargo 单测断言两态(基线 53+1)。
2. **sidecar 协议(entry.py,单一事实源 = `_HANDLERS` 62→64)**:
   - `plugins.bundled.list` → 枚举 env 指向目录下含 plugin.yaml 的子目录,逐包 manifest 摘要(id/name/version/tier/gate/provides/requires——**manifest 无 description 字段,定案字段列表按实况修正,不硬凑**)+已装态(对齐 `InstalledPluginStore.entries()` 的 plugin_id,installed/installed_version)+条目级 findings(坏 manifest 也入列不整表炸,沿 yaml.list「坏文件也入列」先例);
   - env 未设/目录不存在 = 合法空表(`{dir: null, count: 0, plugins: []}`——如实,不虚构);
   - `plugins.bundled.install {id, force?}` → id 过 `_PLUGIN_ID_RE` 同门防穿越(manifest.py 同源正则,installed.py:397 `_safe_plugin_id` 同口径),id→目录映射后直调 `InstalledPluginStore.install`(:267,与 cli.py:4097-4119 同门:manifest 校验→版本矩阵→整目录拷贝绝不半装);已装未 force/版本不兼容未 force → PluginStoreError 结构化透传(code 原文:already_installed/incompatible_version/…);应答 `{ok, dir, version}`;
   - 新错误码:`bundled_plugins_unavailable`(env 未设/目录不可达——dev/旧包如实态)、`bundled_plugin_not_found`(id 合法但目录内无此件)。
3. **盘点数字单一事实源**:desktop/src-tauri/tauri.conf.json `bundle.resources`(亲数 45 键)为唯一权威——组件包 10 件(DESKTOP_TIER_PACKAGES 9 + STUB_ONLY_PACKAGES 1 mediacrawler,恰对 tests/desktop/test_installer_resources.py 既有守卫);`plugins.bundled.list` 装机态断言数=10(测试从 resources 映射重建目录树,动态对账 resources↔list,不硬编码孤数)。
4. **裁剪面(如实记档防 review 叙述自相矛盾)**:
   - 品类 YAML 进包 8 件不进发现/安装面(安装语义不同:拷 plugins 根平铺+id 冲突需定义;启动补种已覆盖;yaml-editor 屏可自建——留池档);
   - 卸载本期不做:UI 卸载按钮裁(控制协议面;CLI `myssia plugin remove` 在库 cli.py:991+store.remove installed.py:358),卡片文案明示「卸载走 CLI;随包原件只读永不删,卸载=删安装根拷贝可重装」——留池档可翻案;
   - monitor.yaml/credentials.yaml 不在 resources 映射(仓库平铺 10 件差 2,PRD 写明差异)。
5. **UI(ui-src)**:settings-screen.tsx SECTIONS 加「装机组件」分区(与 GatesForm/PyenvCard 平级的渲染分支)+ 独立卡片文件 BundledPluginsCard(沿 pyenv-card.tsx 独立文件先例):
   - 逐包行:名称/版本/tier 徽章/gate 徽章(如有)/已装态徽章(已装 ok/未装 outline)/installed_version(与随包版本不同→「可重装更新」)/安装·重装按钮/findings 行内展示;
   - 空态如实:dir=null(dev 态)→「未发现随包插件目录(dev 形态或旧包);此分区在正式安装包内可用」;
   - vendor 缺失不在安装时检查、不伪造完整性(osint/theharvester 运行时走 adapter 既有结构化 `vendor_missing` 指引,tests/plugins 已钉);
   - TS 契约面沿 pyenv-api.ts 先例新文件(types+invoke 封装+parse 守门,invoke("sidecar_request") 屏私有封装,不进共享门面)。
6. **协议文档三处同步**:sidecar-protocol.md 注册表 62→64(新增 #63/#64 行)+分组批注段(本流段)+错误码表(新两码+透传族补 PluginStoreError code 透传)+变更纪律段(屏私有封装面对账注记);PROTOCOL_VERSION 维持 10(两新方法循 gates 批二「地基路」先例不 bump:旧壳+新 UI 组合经 method_not_found 结构化降级不白屏;g10 config_auto 同款注记)。
7. **测试**:tests/desktop 新文件(list 枚举断言 10/空 env 合法空/install 真拷贝 tmp 沙箱/坏 manifest 条目 finding/穿越 id 拒/已装未 force 拒→force 重装/版本不兼容透传+force 强装/env 未设 install 拒/id 不在目录拒/params 形状/已装态对齐)+ 既有协议对账例随 64 态更新 +vitest 卡片渲染/调用桩/已装徽章/findings/空态+设置屏分区接线例。

## Acceptance Criteria

- [x] AC1 壳层:release+未显式设 → 注入 env 值 = resource_dir/plugins;dev/已显式设 → 不注入不夺权(cargo 单测两态断言,基线 53+1=54)。
  证据:pyenv.rs `bundled_plugins_env_value`(纯函数)与 `bundled_plugins_dir`/常量 `RESOURCE_BUNDLED_PLUGINS_DIR`/`BUNDLED_PLUGINS_ENV`;main.rs `spawn_sidecar` spawn 段注入(:204-211,MYIA_APP_VERSION 同点纯加法);cargo 单测 `bundled_plugins_env_value_release_only_and_not_displacing` 四态断言(release+未设→Some(.../plugins)、dev→None、已设→None×2、拼装与公开常量一致)。亲跑 `cargo test`(desktop/src-tauri)→ **54 passed; 0 failed**(基线 53+1)。编辑前 gitnexus impact 亲跑:`spawn_sidecar` upstream 7/HIGH(生命周期核心函数天然高连接度;变更为追加一行 env 的加法,同 MYIA_APP_VERSION C10 先例),四门禁兜底。
- [x] AC2 sidecar list:从 tauri.conf resources 映射重建目录树 → list 恰 10 件、逐件三件套可枚举;空 env/目录不存在 → 合法空表 {dir:null,count:0,plugins:[]};坏 manifest 条目入列带 finding(manifest_invalid)不整表炸。
  证据:`test_list_rebuilt_installer_tree_yields_exactly_ten_packages`(rebuild_bundled_tree 从 resources 逐键重建,count==len(BUNDLED_PACKAGES)==10,id 集恰为 DESKTOP_TIER_PACKAGES+STUB_ONLY_PACKAGES,逐件摘要键集恰 14 键契约面)、`test_list_empty_env_is_legal_empty_state`、`test_list_env_points_to_missing_dir_is_also_empty`、`test_list_bad_manifest_is_entry_level_finding_not_table_failure`(坏件 id=None+manifest_invalid;平铺品类 YAML 不进清单)、`test_list_dir_name_manifest_id_mismatch_surfaces_warning`、`test_list_installed_state_aligns_with_install_root`(已装 0.9/随包 1.0 对照)。真装机树冒烟(只读):`MYIA_BUNDLED_PLUGINS=/Applications/世事.app/Contents/Resources/plugins` → count=10、ids 恰 10 件、proxy compatible_current=True。
- [x] AC3 sidecar install:tmp 沙箱真拷贝(安装根下目录+manifest/README/adapter/子目录逐字节一致,应答 {ok,dir,version});已装未 force → already_installed 结构化拒;force=true → 重装成功(先清后拷);版本不兼容未 force → incompatible_version 拒、force 强装 compatible_current 如实 false+finding;穿越 id(../x、a/b、..、大写、过短、前导连字符)→ invalid_params;env 未设 → bundled_plugins_unavailable;id 合法不在目录 → bundled_plugin_not_found;坏 manifest 源 → manifest_invalid 且安装根零目录(绝不半装);已装态对齐。
  证据:`test_install_copies_directory_into_install_root`、`test_install_already_installed_without_force_is_structured_reject`(含 force 重装陈旧文件清除+list 翻真)、`test_install_incompatible_version_rejected_and_force_overrides`、`test_install_traversal_ids_are_rejected_before_any_lookup`(数字开头 123 归 not_found 组如实断言)、`test_install_without_env_is_unavailable_structured_reject`、`test_install_unknown_id_in_bundled_tree_is_not_found`、`test_install_params_shape_is_validated`、`test_install_bad_manifest_source_is_rejected_not_half_installed`、`test_install_locates_by_manifest_id_when_dir_name_differs`(manifest id 兜底映射,按 manifest id 落目录)、`test_bundled_methods_on_rebuilt_installer_tree_roundtrip`(真 myssia-proxy manifest 走通同门)。真装机树冒烟:install myssia-proxy → ok=True v1.1.0 落 /tmp 沙箱;list 翻真 installed=True;二装未 force → already_installed;随包原件未动(source intact=True)。
- [x] AC4 UI:vitest 分区导航+逐包行渲染(名称/版本/tier 徽章/已装态徽章/findings)+安装按钮调用桩(list 刷新)+空态如实(dir=null 提示)+卸载指引文案;tsc -b 零错。
  证据:`bundled-plugins-card.test.tsx` 8 例(发现渲染含「可重装更新」对照与 vendor_missing 卸载指引文案、坏 manifest findings 行内+安装钮禁用、空态零虚构、未装件发 {id} 零 force 键+装后回读 list≥2、已装件发 {id,force:true}、incompatible_version 结构化上屏零成功回执、parse 双守门);`settings.test.tsx` +1 例(installer-plugins 深链直进、卡片挂载、空态块、导航项);亲跑 `npx vitest run` 全量 → **26 files / 474 passed**(基线 465+9);`npx tsc -b --force` → 零错(exit=0)。
- [x] AC5 协议:注册表 64 行+批注段+错误码表(含透传族)三处同步;全量对账例(data.allowed==sorted(_HANDLERS)==注册表逐行)绿;PROTOCOL_VERSION=10 不动(注记在档)。
  证据:sidecar-protocol.md 标题 62→64+#63/#64 两行(git diff 亲证既有 62 行零漂移)+bundled-plugins-install 批注段(不 bump 理由:gates 批二「地基路」先例,旧壳+新 UI 经 method_not_found 结构化降级)+错误码表「随包插件一键装」行+透传族 PluginStoreError.code 段+变更纪律屏私有封装面注记;`test_method_registry_full_reconciliation` 绿(动态断);`test_method_registry_allowed_matches_handlers` 随 64 态更新(len==64+两新方法成员断言);亲验 `PYTHONPATH=src uv run --no-sync python -c` → HANDLERS: 64 / PROTOCOL_VERSION: 10。
- [x] AC6 门禁:uv run --no-sync pytest tests/desktop 全绿(installer resources 40 例基线之上新增);ui-src npx vitest run 全绿;cargo test(desktop/src-tauri)54 passed;npx tsc -b 零错;ruff 零新红;gitnexus impact(编辑既有符号 spawn_sidecar/_HANDLERS 前亲跑)+detect-changes 亲跑;git commit --only 本流文件。
  证据(全部本机亲跑,2026-10-05):`uv run --no-sync pytest tests/desktop -q` → **240 passed**(基线 224+16 新例);`npx vitest run` → **474 passed**(26 files);`cargo test`(desktop/src-tauri)→ **54 passed**;`npx tsc -b --force` 零错;`uv run --no-sync ruff check .` → All checks passed;`gitnexus impact` 亲跑:`_HANDLERS`(Variable,uid 消歧)双向 0/LOW、`_m_plugins_list` upstream 0/LOW、`spawn_sidecar` upstream 7/HIGH(加法 env 注入,C10 MYIA_APP_VERSION 同款先例,diff 亲证纯加 hunk);`gitnexus detect-changes -r shishi --scope unstaged` 亲跑:7 文件 22 符号 critical——git diff -U0 亲证改动全为纯加 hunk(entry.py 5 hunk 唯一既有行变化=import 一行扩多行;main.rs 1 hunk 11 行纯加;pyenv.rs 3 hunk 纯加),报出的 myssia_home/_item_dict/schedule_respawn/Detection/lock_fingerprint 等均为行号漂移归因噪声(其 hunk 在 diff 中不存在);受影响流全在 sidecar spawn 生命周期链=env 注入预期面。

## 完成纪要(2026-10-05)

- 实现面四层:壳 Rust(main.rs spawn 段 env 注入 11 行+pyenv.rs 纯函数/常量/单测 52 行)、sidecar(entry.py 两新方法+辅助 189 行+_HANDLERS 2 行+常量/imports)、协议文档(注册表+批注+错误码+变更纪律四处)、前端(bundled-plugins-api.ts+bundled-plugins-card.tsx+settings-screen 分区接线)。tauri.conf.json 零改动(组件包 10 件映射批三已齐,test_installer_resources.py 既有 40 例守卫)。
- 与定案的唯一修正:manifest 摘要无 description 字段(schema 实况:manifest.py PluginManifest 无此键),按实况以 id/name/version/tier/gate/compatible(+兼容判定)/requires/provides 摘要,PRD/注册表行如实记载。
- 安装来源发现锚点双层防线:壳层 env 注入(release-only)是装机态通道;sidecar `_bundled_plugins_root()` 对 env 未设/目录不存在均回合法空表——dev 形态/旧包/自动化未注入三态都如实,不虚构清单。
- 装机真包验证口径:当前装机包(1e231f4 等值)不含本流改动,装机态 UI 全链需 owner 重打包后验;本流以真包 Resources/plugins 树(只读发现+安装指 /tmp 沙箱)冒烟代替,10 件发现/一键装/重装拒/原件未动全绿。真机上重装旧包会覆盖安装根拷贝,装机包 Resources 原件只读——数据面无风险。

## Notes

- 与市场面(myssia plugin install CLI)语义同源:本件只是把「安装来源」从本地路径换成随包 Resources 目录,装卸门(manifest 校验/版本矩阵/绝不半装)零新增。
- vendor 许可红线:osint/theHarvester 的 vendor/ submodule 不随包分发(test_installer_resources.py 已钉守卫);装机上 vendor 缺失走 adapter 既有结构化 vendor_missing 指引,本件零改动零新指引(卡片描述如实提及)。
- 留池档可翻案:装机组件 UI 卸载按钮(本期裁);品类 YAML 8 件进发现/安装面(安装语义不同)。
- 母任务计划定案原文见基线上下文(本 PRD 忠实落实,唯一修正:description 字段 manifest schema 无此键)。

## 收口回执(2026-10-05 归档轮)

- 收口门禁(收口准备轮亲跑,回执落 3470b59 journal 段;本流 f77f894 已在其树内):全量 `uv run --no-sync pytest -q` → **4284 passed / 40 skipped / 0 failed**(tests/desktop 240 passed = 基线 224+本流 16);vitest 全量 **474**(=465+本流 9);`cargo check --locked` + `cargo test` → **54 passed**;协议对账 64 三方一致(#63/#64 注册表行在列,归档轮本机复跑 `-k method_registry` → 2 passed 亲验);`tsc -b --force` 零错;ruff 全绿。
- CI:run 37304222631(main @ 3470b59,含本流 f77f894)→ **success**;归档轮 `gh run view` 亲验 + `merge-base --is-ancestor` 亲证 f77f894 ∈ 3470b59。
- **受阻如实注(装机链验证)**:双保险判据中「直跑新装二进制+截图」结构性依赖 owner 重打包——现装 /Applications/世事.app 二进制 mtime(2026-10-05 16:28)早于 f77f894 提交时间(19:24:44),grep `MYIA_BUNDLED_PLUGINS` 零命中(对照 `MYIA_APP_VERSION` 命中 1)坐实旧包不含本轮壳层 env 注入与 sidecar 两新方法;重打包后补验 `#/settings?section=installer-plugins` 应见 10 件(Resources/plugins 亲验 18 项=10 组件包+8 品类 YAML,与断言口径一致)。代码面全量门禁已绿,机房实况同 table-restore AC4 先例。
- 收口处置:归档至 archive/2026-10/;留池可翻案两件(UI 卸载按钮/品类 YAML 进发现面)已在 Notes 记档。

## 补验销号(2026-10-05 晚,重打包落地后;尾部纯增量补记,原文不改)

「收口回执」受阻注记的装机链验证当晚闭环。重打包=并行会话(/tmp/myia-refresh
回执:build.exit=0、install.ts=20261005-195431 head=9c287b1;新二进制 mtime
19:51:50,grep `MYIA_BUNDLED_PLUGINS` 命中 1——旧包零命中对照,换装到位):

- **壳层 release 注入(进程级亲证)**:装机版经 `open -g` 无覆盖启动
  (launchctl getenv 全空、open 不透传 shell env),其 sidecar 进程 env 实读
  (ps eww)含 `MYIA_BUNDLED_PLUGINS=/Applications/世事.app/Contents/Resources/plugins`
  (+MYIA_APP_VERSION=0.0.1/MYIA_HOME=真根同点)——AC1 注入逻辑在装机 release
  构建真实生效,非仅 cargo 单测口径。
- **UI 像素(installer-plugins.png,20:01:42)**:`#/settings` 装机组件卡全
  10 件渲染(逐件名称/id/版本/tier 徽章/能力/未装态/安装钮,OCR 与
  DESKTOP_TIER_PACKAGES 9+STUB_ONLY 1 逐件对上),随包原件只读与
  vendor_missing 指引文案在屏——受阻注记所记「#/settings?section=
  installer-plugins 应见 10 件」验讫(AC4 装机态)。
- **sidecar 四连探针(销号会话亲跑;生产 spawn 同款组合=真数据根 python+
  装机包 Resources/myssia-src,MYIA_HOME/MYIA_PLUGIN_DIR 隔离到一次性根)**:
  list → count=10/compat=10;install myssia-proxy → {ok,version:"1.1.0"}
  落隔离根(README/adapter/plugin.yaml 齐);回读 list installed 翻真;二装
  未 force → `already_installed` 结构化拒带指引。回执
  /tmp/myia-bundled-probe.*/out.jsonl。
- 附注:验中主人曾在补验线沙箱实例(手工预置 python→detect「无戳但 python
  在→Ready 兜底」、python-env.json 不存在)点「检查状态」见
  `[deps_fingerprint] 进度戳无依赖指纹`——系一次性沙箱根的如实态非真机故障;
  真机根 state=ready+指纹 a89418… 与新包随包 requirements-lock.txt sha256
  逐字节一致,三查全绿。「补验沙箱窗自标识」改进项已落 v12-backlog 池第 9 项。
