# 装机组件域扩批(前轮四件翻案一次收口)

## Goal

前轮 10-05-bundled-plugins-install 归档时留池四件(主人令全部翻案解决):
①trafilatura 进装机组件表 ②装机组件卡卸载按钮 ③品类 YAML 进发现/安装面
④monitor.yaml/credentials.yaml 随包映射。本件一次收口四件,域界:desktop 域
+ plugins 组件资源 + 任务档;`src/myssia/` 引擎域零触碰(components.json
相关的 doctor 探测面本件不动——trafilatura 无 doctor 探测,见 R1)。

## 现场实况(2026-10-05 亲读)

- `desktop/resources/components.json` 现单件 table;壳侧 `pyenv_components.rs`
  `load_registry` 全动态零 id 锁(测试常量 TABLE_PIP_SPEC 只是测试基准)→
  注册表加条目壳侧自动出现,UI 自动渲染(COMPONENT_META 未知 id 退原 id)。
- CLI `myssia plugin remove`(:4125)= `InstalledPluginStore.remove`
  (installed.py:358):删安装根 `<install_root>/<id>` 整目录;错误码
  `invalid_plugin_id`/`not_installed`/`io_error`;返回 `{id, path, removed}`。
  随包原件只读永不删。
- `plugins.bundled.list` 应答现 `{dir, count, plugins}`(count=组件包数);
  `_bundled_plugin_views` 跳过平铺 YAML(`# 平铺品类 YAML/散落文件不是组件包`)。
- tauri.conf resources 45 键:品类平铺 YAML 8 件(ai-news/wool/stocks/
  gpu-prices/games/news/exposure/myssia-demo)+ 组件包 10 件目录映射;
  monitor.yaml/credentials.yaml 在仓库 plugins/ 但未随包。
- 品类 YAML 文件名与 `id:` 字段一一对应(`<id>.yaml`,10 件全核);
  品类 id 门 = `CATEGORY_ID_RE`(schema.py:287,`^[a-z0-9][a-z0-9_-]{0,63}$`)。
- 门禁基线:pytest tests/desktop 240;vitest 474(近轮 477);cargo test
  (src-tauri)56(并行流已涨,以本轮亲跑为准);注册表 64 行。

## Requirements(四件决议)

### R1 trafilatura 进装机组件表

- `components.json` 加第二件:`{id: "trafilatura", pip_spec:
  "trafilatura>=2.3,<3 selectolax<1", label: "正文抽取兜底", description:
  人话——static_html 引擎正文抽取兜底,零配置;缺省关,开关 =
  MYIA_EXTRACT_FALLBACK 环境变量(=1 才启用);缺装时兜底结构化降级不拦核心}。
- pip_spec 与 pyproject extras `myssia[trafilatura]` 逐字符同字串(主件也用
  extras 原窗,不钉版——与 table 主件钉 ==3.0.2 不同:trafilatura extras
  本身是双约束窗 `>=2.3,<3`,钉版反而制造第三种口径)。
- **形状正则连带扩**:test_pyenv_resources.py 的 spec 形状正则现只支持单约束
  token,`trafilatura>=2.3,<3` 含逗号多约束——正则扩为支持逗号分隔约束组。
- UI:`pyenv-card.tsx` COMPONENT_META 补 trafilatura 文案条目(label/
  description 人话;注册表驱动自动出现,文案层补齐)。
- 测试:仿 `test_table_component_matches_pyproject_extras` 补 trafilatura 侧
  交叉对齐(extras ↔ components.json 件集+字串一致);仿
  `test_table_component_closure_three_way` 的三方锁**如实降为两方**——
  doctor 探测面不存在(trafilatura 是 env 开关非品类声明件,static_html.py
  惰性 import 自带结构化降级,无 images.table 式 doctor 探测),测试注释写明
  降维理由。pyenv 侧钉版常量实况=零 id 锁,无需改壳。

### R2 装机组件卡卸载按钮

- sidecar 新方法 `plugins.bundled.uninstall {id}`:直调
  `InstalledPluginStore.remove`(与 install 同门直调 store,不走 CLI 子进程,
  取既有结构最合身);**不依赖 bundled root**(卸载 = 删安装根拷贝,与随包
  目录无关,dev/装机态均可用,档记);id 过 `_PLUGIN_ID_RE` 同门 →
  invalid_params;PluginStoreError code 原文透传(not_installed/io_error);
  应答 `{ok, id, path}`。
- 注册表 64→65(+#66 见 R3);协议文档三处同步:#65/#66 注册表行 + 批注段
  (本批段)+ 错误码表(uninstall 面 not_installed 透传归透传族注记);
  `test_method_registry_full_reconciliation` 动态断言自动跟上,
  `test_method_registry_allowed_matches_handlers` 随 66 态更新;PROTOCOL_VERSION
  维持 10(循 bundled 批「地基路」先例:旧壳+新 UI 组合 method_not_found
  结构化降级不白屏,注记在档)。
- UI:已装行加「卸载」钮(普通确认 `window.confirm`,卸载非危险操作——
  不循钥匙链删除二次确认判例;确认后调 uninstall,回读 list 刷新,note 回显
  「已卸载(随包原件只读,可随时重装)」);文案行更新(原「卸载走 CLI,
  本屏不提供」改为本屏可卸载)。未装行零卸载钮。
- 测试:pytest(uninstall 真删 tmp 沙箱目录/未装 not_installed/穿越 id
  invalid_params 先于任何查找/params 形状(缺 id)/卸载后 list
  installed 翻假/随包原件未动/uninstall 不依赖 env(dev 态可卸))+ vitest
  (已装行卸载钮渲染+确认后调用桩+取消不调/未装行零卸载钮/not_installed
  结构化上屏/卸载后回读刷新)。

### R3 品类 YAML 进发现/安装面

- **发现**:`plugins.bundled.list` 应答加 `categories` 数组(与 `plugins`
  并列;`count` 键语义不变=组件包数,兼容既有契约/测试/UI):枚举随包目录
  平铺 `*.yaml`/`*.yml`(非递归,与 `_seed_first_run` 同款 glob 口径),逐件
  `{file, path, id, name, schedule, exists, findings}`——id/name/schedule 经
  `load_category_file` 实读(坏 YAML → id=None + 条目级 finding
  `category_invalid`,不整表炸,沿 yaml.list 先例);`exists` = 数据根
  plugins/ 下同名文件存在(对齐补种落点)。env 未设 = categories 空数组
  (与 plugins 空表同态)。
- **安装**:sidecar 新方法 `plugins.bundled.category_install {id, force?}`:
  id 过 `CATEGORY_ID_RE`(schema 同源防穿越)→ 随包平铺 YAML 内按 id 定位
  (YAML id 字段直配 > 文件名 stem 兜底)→ `load_category_file` 校验通过才装
  (坏件拒零拷贝)→ 拷到 `<plugins_dir>/<源文件名>`(平铺,与补种同落点);
  **已有同名文件未 force → `category_exists` 结构化拒(如实「已存在」不覆盖,
  与 `_seed_first_run` 绝不覆盖语义对齐不打架:补种=自动补缺永不覆盖,安装面
  =显式知情,force 才覆盖)**;应答 `{ok, file, path}`;env 未设 →
  `bundled_plugins_unavailable`;id 合形不在目录 →
  `bundled_category_not_found`。
- **id/冲突定义(写档钉死)**:品类 id = YAML `id:` 字段(CATEGORY_ID_RE);
  冲突 = 数据根 plugins/ 下**同名文件**存在(文件级,内容同否不判——如实);
  与组件包零冲突(组件包落子目录 `<install_root>/<plugin_id>`,品类落平铺
  文件 `<plugins_dir>/<file>`,两种形状互不占据);品类无卸载面(补种只补
  不删,卸载品类 = 数据根删文件,yaml-editor 屏可达,本期不做)。
- 注册表 65→66;协议文档 #66 行 + 批注 + 错误码表(category_exists/
  bundled_category_not_found 新码)。
- UI:装机组件卡内分两节——现有「组件包」行 + 新「品类配置」分区行
  (名称/id/排程/已存在徽章(已存在 ok/未存在 outline)/安装·覆盖按钮
  (exists → 「覆盖(需确认)」发 force)/findings 行内);空态文案不变。
- 测试:pytest(list categories 枚举重建树 10 件(R4 落地后)/坏 YAML 条目
  finding/exists 对齐数据根实况/install 真拷平铺/已存在未 force 拒→force
  覆盖内容翻新/穿越 id 拒/env 未设拒/id 不在目录拒/params 形状/补种先跑后
  exists=true 且 install 未 force 拒——两语义对齐不打架)+ vitest(品类
  分区渲染/安装调用桩(未存在发 {id} 零 force,已存在发 {id,force:true})/
  findings 行内/结构化错误上屏)。

### R4 monitor.yaml/credentials.yaml 随包映射

- **安全裁定(亲读两文件全文)**:monitor.yaml 只含
  `keychain:myia/monitor/token` 引用 + `env:FEISHU_CHAT_ID` 引用 +
  `https://my-monitor.example.com` 占位 endpoint;credentials.yaml 只含
  `keychain:myia/credentials/token`/`keychain:myia/credhunter/github-token`
  引用 + `https://aipocket.example.com` 占位 + `https://api.github.com`
  公共锚点。**零明文凭据,安全 → 落映射**(不跳过)。
- tauri.conf.json resources 增两映射 `../../plugins/monitor.yaml →
  plugins/monitor.yaml`、`../../plugins/credentials.yaml →
  plugins/credentials.yaml`。
- tests/desktop/test_installer_resources.py:OFFICIAL_CATEGORY_YAMLS 常量
  8→10 件(**主人令口径「10→12」与实况差 2:品类断言面现 8 件(7 官方+demo),
  +2=10;「12」疑把非品类件计入,以实况为准如实注记**);随包 plugins 面总件
  数 18→20(10 组件包+10 品类)。
- 连带语义(如实注记不另立件):两件进包后启动补种会自动补到用户数据根
  (品类全量补缺既有语义);无凭据时 monitor/credentials 如实空态
  (credhunter 无 token 该源不启用 spec §2;plugin 节失败不拦核心 iron law);
  plugins.bundled.list categories 装机态 8→10 件。

## Acceptance Criteria

- [x] AC1(R1):components.json 两件在册;trafilatura pip_spec 与 extras
  `myssia[trafilatura]` 逐字符同字串(交叉对齐测试锁);形状正则支持逗号
  多约束;UI COMPONENT_META 补文案;壳侧零改动(cargo 既有基线绿)。
  证据:components.json 第二条目(id=trafilatura/label「正文抽取兜底」/
  description 含 MYIA_EXTRACT_FALLBACK 开关与缺省关语义);原形状正则
  `[^\s]+` 约束段**天然容忍逗号多约束**(亲验 trafilatura>=2.3,<3 匹配,
  实况降为注释记档,零改正则);形状检查循环从 table-only 扩为全条目遍历;
  `test_trafilatura_component_matches_pyproject_extras`(extras↔components.json
  逐字符同字串锁——sorted 对比绕开 Requirement 归一化重排;三方锁如实降为
  两方:doctor 无 trafilatura 探测面(env 开关件非品类声明件),测试注释
  写明降维理由;pyenv 侧 load_registry 零 id 锁亲证);pyenv-card.tsx
  COMPONENT_META 补 trafilatura 文案;壳侧零改动。
- [x] AC2(R2):`plugins.bundled.uninstall` 全语义(dev 态可卸/not_installed
  透传/穿越拒/真删+list 翻假);UI 已装行卸载钮(普通确认/取消不调/回执
  note);注册表+协议文档三处同步。
  证据:entry.py `_m_plugins_bundled_uninstall`(直调 InstalledPluginStore.
  remove 同门;不依赖 bundled root——dev 形态可卸档记在协议文档 #65 行);
  pytest `test_uninstall_removes_install_root_copy_only`(真删+随包原件未动
  +list 翻假+可重装)/`test_uninstall_not_installed_is_structured_reject`/
  `test_uninstall_does_not_require_bundled_env`/`test_uninstall_traversal_and_
  shape_are_rejected`;vitest 卸载组 3 例(普通一次确认发 {id}+回执「已卸
  载…可随时重装」+回读翻未装/取消零调用/not_installed 结构化上屏)+
  未装行零卸载钮断言并入发现面首例。
- [x] AC3(R3):list 应答带 categories(装机态 10 件/坏件条目 finding/exists
  对齐);category_install 真拷平铺/已存在拒 force 才覆盖/补种语义互不打架;
  id/冲突定义在协议文档钉死;UI 品类分区;注册表 66 终值。
  证据:entry.py `_bundled_category_views`(load_category_file 实读 id/name/
  schedule,坏件 category_invalid 条目级)+`_locate_bundled_category_yaml`
  (stem 直配>id 兜底)+`_m_plugins_bundled_category_install`(CATEGORY_ID_RE
  门→校验通过才装→tmp+rename 原子平铺拷;category_exists/bundled_category_
  not_found 新码);协议文档 #66 行钉死 id/冲突定义(品类 id=YAML id 字段;
  冲突=数据根同名文件文件级;与组件包子目录/平铺文件零冲突);pytest 品类
  组 7 例(重建树 10 件对账/坏 YAML 条目 finding/真拷+tmp 零残留/已存在拒
  →force 覆盖内容翻新/防线矩阵(含 CATEGORY_ID_RE 1-64 与 PLUGIN_ID_RE
  2-64 差异如实)/id_mismatch 件定位/**补种对齐红线例**:serve 启动补种
  自动补缺 10 件→手改件逐字节保留→安装面对补种拷的件未 force 拒);
  vitest 品类组 4 例(渲染/未存在零确认发 {id}/已存在确认发 {id,force:true}
  +取消零调用/坏件禁装+category_exists 上屏);注册表 64→66,#63 行注连带
  更新,`test_method_registry_full_reconciliation` 动态断言绿(亲跑 -k
  method_registry → 2 passed),`test_method_registry_allowed_matches_handlers`
  随 66 态(len==66+两新方法在列);PROTOCOL_VERSION=10 不动(批注段注记)。
- [x] AC4(R4):安全裁定在档(两文件全文物证:纯引用模板零明文);resources
  47 键;test_installer_resources 品类 10 件;补种连带语义注记。
  证据:亲读 monitor.yaml/credentials.yaml 全文——只含 keychain:myia/*
  引用、env:FEISHU_CHAT_ID 引用、example.com/api.github.com 占位锚点,
  **零明文凭据 → 裁定安全落映射**(tauri.conf.json resources 45→47 键);
  test_installer_resources OFFICIAL_CATEGORY_YAMLS 8→10(**主人令口径
  「10→12」与实况差 2:品类断言面原 8 件(7 官方+demo)+2=10;「12」疑把
  非品类件计入,以实况为准如实注记**);`test_scenario_category_yaml_is_
  credential_template_only` 参数化守卫(凭据承载键值只许 keychain:/env:
  引用模板+Bearer/列表前缀剥离,未来加明文即红)+补种连带语义注记
  (无凭据如实空态:credhunter 无 token 该源不启用;plugin 节失败不拦核心)。
- [x] AC5 门禁:见下方完成纪要。

## 完成纪要(2026-10-05)

- **门禁数字(全部本机亲跑)**:`uv run --no-sync pytest tests/desktop -q`
  → **254 passed, 1 failed**——唯一失败 `test_store_state_v7_database_
  migrates_on_protocol_open` 断言 schema_version=="8",而**并行 engines 域
  流**已把工作树 `src/myssia/store/sqlite.py` SCHEMA_VERSION 升 9(未提交
  改动,git diff --stat 亲证),归对方域中间态收口(对方 schema 升版须连带
  改该断言);除该例外全绿(本批 +15 例:uninstall 4+品类 7+installer 4+
  pyenv_resources 1,基线 240);另有一次全量跑出 40 failed 的抖动(含
  test_pyenv_e2e),单独复跑 2 passed、再全量仅余上述 1 例——并行会话同刻
  活动所致资源竞争,以多次复跑众数为准。`npx vitest run`(ui-src)→
  **485 passed**(26 files,基线 477+8 新例);`npx tsc -b --force` 零错;
  `cargo check --locked` + `cargo test`(src-tauri)→ **56 passed**(基线
  不变,壳侧零改动);`uv run --no-sync ruff check desktop/entry.py
  tests/desktop/` → All checks passed;协议对账 `-k method_registry` →
  2 passed(注册表 66 三方一致);`PYTHONPATH=src uv run --no-sync python -c`
  亲验 HANDLERS: 66 / PROTOCOL_VERSION: 10。
- **gitnexus**:编辑前 impact 亲跑——`_HANDLERS`(Variable uid 消歧)
  upstream 0/LOW;`_m_plugins_bundled_list`/`_bundled_plugin_views` 索引未
  收录(前轮新符号),grep 兜底=调用面仅 _HANDLERS 注册与 wire 消费(LOW);
  `detect-changes --scope unstaged` 亲跑:29 文件 53 符号(混并行 alerts/
  messaging 流与行号漂移归因噪声),git diff -U0 亲证本流 entry.py 改动全在
  bundled 族(docstring 扩+空态应答加键+两新方法+_HANDLERS 两行纯加),
  报出的 _m_store_state_*/_m_secret_*/_m_feed_export 等符号 hunk 在本流
  diff 中不存在(纯行号漂移)。
- **并行纪律执行**:src/myssia/ 引擎域零触碰(store schema 9 与 messaging/
  alerts UI 改动均为对方工作树实况);cli.py 零触碰;提交 git commit --only
  本流 14 路径。
- 装机真包验证口径同前轮:装机包 UI 全链需 owner 重打包后验(Resources/
  plugins 面 18→20 项);本流以 resources 重建树测试(10 组件包+10 品类
  动态对账)+ dev 形态空态断言兜底。

## Notes

- 并行会话纪律:engines 域流在动 src/myssia/engines+schema+docs,本件零触碰;
  cli.py 零触碰(trafilatura 无 doctor 探测面,无需动);只动 desktop 域+
  plugins 组件资源+任务档。
- 前轮「装机真包验证口径」同款:装机包 UI 全链需重打包后验,本流以 resources
  重建树测试 + dev 形态空态断言兜底。
