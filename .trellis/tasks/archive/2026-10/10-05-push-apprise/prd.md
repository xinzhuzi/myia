# Apprise 推送统一通道(长尾目标一个依赖通吃)

## Goal

push 层新增 `apprise` 通道:一个 pip 依赖(extras 可选)解锁 ~160 个推送目标
(Pushover/Gotify/Bark/discord-webhook 变体等长尾),凭据引用体系与现有
纪律零妥协。**不替代**现有 31 通道——只为长尾目标服务。

## 背景与现状(锚点)

- 推送面实况:PushChannel Literal **31 成员**(schema.py:229;grill 抓出
  本档前身「现 6 通道」口径失实已修正)——slack/discord/teams/matrix/
  mattermost/…已在,Apprise 真实增量=长尾目标(Pushover/Gotify/Bark 等)。
- 通道实现先例:push/__init__.py 注册表(:141 主表+:155 `_W3_LONGTAIL_CHANNELS`
  字典注册,加通道=新文件+一行注册);telegram.py 为最薄蓝本。
- 凭据纪律:schema.py:788 明文凭据启动即拒——**apprise URL 内含 token,
  必须走 env:/keychain: 引用,不落 YAML 明文**。
- extras 先例:pyproject:58-63 trafilatura 组(钉版/不进核心/不进 all/
  桌面锁不进);apprise 同构。
- 许可:MIT(caronc/apprise);bark:// 支持原生在内(grill 事实核查)。

## grill 决议(2026-10-05 深夜轮)

- Q2/Q3:不立即抢跑——档立好后**主人先点名真正缺的推送目标**再开工;
  若点名结果=高频目标已有原生通道,本档可降级或裁撤。
- 与 Bark 档(10-05-push-bark)关系:apprise 含 bark://;两者不互斥
  (原生 Bark=零依赖,apprise=长尾),主人可只取其一。

## Requirements

1. **schema**:PushChannel 增 `"apprise"`;**不进 CHANNEL_PLATFORMS 目录
   寻址**(同 webhook/stdout 先例:配 `targets` 即拒——apprise 目标=URL
   串,无目录语义);`target` 字段走凭据引用,解析值为 apprise 原生 URL
   串(支持逗号/换行分隔多目标,Apprise 原生语法,一引用多目标)。
2. **push/apprise.py**:沿 telegram.py 形态;`apprise.Apprise().add(urls)`
   + `notify(title=…, body=…)`;**导入失败(未装)= send-time 结构化
   `PushError(apprise_unavailable)` + doctor finding `apprise_not_installed`**
   (消息内带安装命令 `pip install "myssia[apprise]"`;不告警未配置用户
   ——没配该通道=正常态,同 TG 凭据不可解析 INFO 先例)。
3. **pyproject**:`apprise = ["apprise>=1.9,<2"]`(钉版防破坏性漂移;
   不进核心不进 all;requirements-lock.txt 不动=桌面锁不进)。
4. **UI 美化**:
   - yaml-editor 通道下拉增 apprise,target 提示文案:「填 env:/keychain:
     引用,值为 Apprise 目标串(bark://…、pushover://… 可逗号分隔多个)」;
   - doctor 屏:apprise_not_installed finding 行内展示安装命令(沿
     vendor_missing 指引行先例,人话零行话);
   - messaging 屏目录**不加**(无目录语义,与 webhook 同)。
5. **协议面**:零新方法(纯管线侧);doctor findings 键内新增若涉及
   载荷形状→加法可选字段,PROTOCOL_VERSION 维持(gates 先例)。

## 测试

- tests/push/test_apprise.py(mock apprise 注入 sys.modules,trafilatura
  先例):①URL 串多目标解析(add 调用次数)②明文 target 拒(启动即拒
  用例)③env/keychain 引用解析 ④未装→结构化 apprise_unavailable+
  doctor finding ⑤notify 抛错→透传不吞 ⑥标题/正文映射。
- schema 用例:literal 增员;apprise 配 targets 拒。
- vitest:yaml-editor 通道下拉含 apprise+提示文案;doctor finding 行
  (若 UI 动了 doctor 渲染面)。

## 验证(判例口径:AI 验到像素)

- 真跑:Apprise 原生 `json://` 磁盘 sink 作离线目标——真发一轮推送,
  落盘报文取证(title/body/目标数;零外网零账号)。
- 装机件:设置/yaml-editor 选 apprise 通道像素+doctor finding 行像素
  (截屏+OCR 回执);装机包随下批刷新。

## Acceptance Criteria

- [x] AC1 schema:apprise 入 PushChannel;targets 配即拒;明文 target 拒。
      (schema.py:PushChannel Literal + PUSH_CHANNELS 增员 32 通道,不进
      CHANNEL_PLATFORMS;tests/push/test_apprise.py:targets→
      targeting_not_supported、明文→load 期 credential_plaintext +
      发送期 invalid_credential_ref 双层拒。)
- [x] AC2 实现:发送路径六用例绿;未装=结构化拒+doctor finding(不惊扰
      未配置用户)。(tests/push/test_apprise.py 17 用例:多目标 add×3+
      notify×1/明文拒零 apprise 触碰/keychain 回退/未装
      apprise_unavailable 带安装命令+doctor apprise_not_installed 且
      未配置品类零 finding/notify False 与 add 拒序号文案透传(目标串
      值永不进文案)/标题=card_title+body=bark 版式。)
- [x] AC3 extras:pyproject 组钉版;lock 不动;`pip install myssia[apprise]`
      后 json:// sink 真跑出报文证据。(pyproject `apprise = ["apprise>=1.9,<2"]`
      不进 core/all;requirements-lock.txt 桌面锁不动;uv.lock 随 extras
      合法收录 apprise 1.13.1+传递件(markdown/oauthlib/requests-oauthlib,
      simplex 先例;uv lock --check 绿)。真跑 2026-10-06:`uv run --with
      'apprise>=1.9,<2'` 临时装 1.13.1,本机 127.0.0.1 json:// sink 收到
      1 份 POST(application/json):title=「📡 羊毛日报 10-06 · 上午摘要」
      (card_title 跨通道一致)、message=两行「▸ 标题 · URL」——零外网
      零账号,零 uv.lock 之外的仓改动。)
- [x] AC4 UI:编辑器下拉+doctor 行像素回执;文案人话。(设置→推送下拉增
      「Apprise(统一推送)」+APPRISE_URL 预设位+apprise-target-hint 文案
      (env:/keychain: 引用/目标串/逗号分隔多个/未装明确报错不影响其他
      通道);vitest settings 49/49 含新 apprise 用例。doctor finding 行
      =通用 findings 渲染面(warning 级,文案自带安装命令),零专属 UI
      改动即人话可达;装机件像素留装机批,同 bark AC4 判例。)
- [x] AC5 门禁:pytest/vitest/ruff 全绿;协议对账例零漂移(64 不动)。
      (定向亲跑全绿:pytest push+schema+cli+smoke+pipeline 1489/desktop
      257/gates 83/docs+skill_doc 135、vitest settings 49/49、tsc 0 错、
      ruff 十文件绿;协议面零改动零 bump,doctor findings 加法载荷
      (R5 先例)。全量门禁归脚本统一跑。**复核纠偏 2026-10-06**:
      「docs+skill_doc 135 全绿」只在提交前工作树成立——65e1b96 的
      git add schema.py 把并行任务 10-06-ai-news-sources 同窗写入工作树
      的 urlwatch 两行(ENGINES+EngineName)一并收进提交,提交态 HEAD
      的 skill/SKILL.md 枚举行缺 urlwatch → test_skill_doc 1 挂(实现员
      复跑亲证 24 passed 1 failed);补笔 SKILL.md ENGINES 行 urlwatch
      token 后复跑 skill_doc 25 + docs 110 + schema/smoke/gates/engines
      591 + push/cli 1297 全绿。详见下方复核处置。)
- [x] AC6 档:决议回写;主人点名清单落 notes(未点名=档挂 planning)。
      (原门「主人先点名缺的目标」由 2026-10-06 主人令「剩下的问题全部
      做完」整批放行覆盖,task.json notes 记档;档置 review。)

## 边界与红线

- 不做:apprise API server(docker 常驻服务)形态——CLI 直发已够;
  替换/重构现有 31 通道——零触碰。
- 凭据红线:url 内 token 永不落 YAML 明文/日志(mask 先例同 telegram)。

## 放行回执(2026-10-05 深夜,主人令「都按建议去做」)

- 问题:Apprise 增量=长尾目标,主人未点名缺什么。做法:主人整体放行(2026-10-05 深夜「都按建议做」),排队第 3;开工条件=点名首个真目标(Pushover/Gotify/任一)即拆实现,或 Bark 落地后仍要长尾再启。顺序:heartbeat→bark→apprise→searxng→firecrawl。
- 执行顺序(全五档):cron-heartbeat(先做,零前置)→ push-bark → push-apprise(点名即启)→ source-searxng → firecrawl-selfhost-verify。

## 实施回执(2026-10-06,队列工作流实施员)

- **解锁**:原门「主人先点名缺的目标」由 2026-10-06 主人令「剩下的问题全部
  做完」整批放行覆盖(heartbeat 833b331/bark 208a599 均已 review,apprise
  排位第 3 到点)。
- **交付面**:pyproject extras(钉版 >=1.9,<2,不进 core/all,桌面锁
  requirements-lock.txt 不动;uv.lock 随 extras 合法收录,uv lock --check 绿)
  |schema(Literal+PUSH_CHANNELS 32 员,不进 CHANNEL_PLATFORMS,零新校验
  逻辑走 platform-is-None 分支)|push/apprise.py(bark 最薄面+simplex 依赖门:
  send 期惰性 import,未装=apprise_unavailable 带安装命令;target=凭据引用,
  解析值=逗号/换行多目标串,parse_targets 逐目标 add(拒收报序号不报内容,
  凭据红线)+一次 notify 广播;notify False=apprise_notify_failed 透传;
  env 缺失回退 myia/push/APPRISE_URL;body=bark 版式 1024 截断,title=
  card_title)|CHANNELS 注册(不进 PLATFORMS)+__all__|cli.py doctor
  apprise_not_installed warning(table_dependency_missing 先例:配了才披露,
  未配置用户零 finding)|测试新文件 17 用例(mock apprise 注入 sys.modules,
  crawl4ai/trafilatura 先例)+受波及钉版四处(test_push_channels 计数 32/
  非寻址四员、test_push_schema_targets 32、test_push 钉死集、两 refs 表锁
  env:APPRISE_URL)|UI 设置→推送四记录+hint 段+vitest 新用例|文档对账六件
  (skill/根+zh+en write-a-plugin/zh+en schema)。
- **kwargs 接线注记**:apprise 无通道专属可选字段(仅 target/template),
  走 pipeline._build_channel 通用下传路,test_build_channel_wires_target
  钉死;_W2_CHANNEL_FIELD_KWARGS 零改动。
- **真跑证据**(AC3,2026-10-06):apprise 1.13.1(uv run --with 临时装)
  → json://127.0.0.1 sink 1 份 POST:title=「📡 羊毛日报 10-06 · 上午摘要」、
  message=「▸ AC3 真跑条目一 · https://example.com/1
▸ AC3 真跑条目二 ·
  https://example.com/2」;零外网零账号。
- **边界守住**:apprise API server 形态不做;既有 31 通道零触碰(bark 之外
  仅注册表一行+__all__ 一行);URL token 永不落 YAML/日志/错误文案
  (add 拒收只报序号,test ⑤ 断言值不进文案)。
- **移交**:装机件像素(设置屏 apprise 下拉+真实 doctor finding 行)随下批
  装机包刷新;doctor 屏 finding 行走通用渲染面无专属 UI 需求。

## 复核处置(2026-10-06,复核轮)

- **红门(已修)**:65e1b96 的 `git add src/myssia/schema.py` 把并行任务
  10-06-ai-news-sources 同窗写入工作树的 urlwatch 两行(schema.py ENGINES
  元组+EngineName Literal,注释自署 10-06)一并收进提交(git log -S
  '"urlwatch"' -- src/myssia/schema.py 全史仅此一笔),而 skill/SKILL.md
  ENGINES 枚举行未含 urlwatch → 提交态 HEAD test_skill_doc 1 挂
  (test_skill_enum_table_matches_schema_constants 报「文档缺失
  ['urlwatch']」)。根因:同仓多会话共享工作树,我 docs 测试跑完到
  git add 之间并行会话改了 schema.py,add 前只对 uv.lock 做了逐块 diff
  审查、未对 schema.py 复核全量 diff——教训:add 须逐文件 diff 亲验。
  修法按复核处方:SKILL.md:57 ENGINES 行补 `urlwatch` token(本档补笔);
  复跑 skill_doc 25 + docs 110 + schema/smoke/gates/engines 591 passed
  8 skipped + push/cli 1297 全绿。
- **范围收编(如实认领)**:65e1b96 提交信息「--only 本流路径」与回执
  「并行在途文件未触碰」失实——schema.py 的 urlwatch 半件属并行任务
  10-06-ai-news-sources,其配套 engines/registry.py ENGINE_REGISTRY 注册
  与 engines/urlwatch.py 仍留工作树未提交(其归属不变,由 10-06 收口)。
  提交态孤立后果:HEAD 下显式 engine: urlwatch 可过 schema 但
  ENGINE_REGISTRY 无此键,解析必失败(bisect 不友好中间态);处置取
  「补 SKILL.md token 保门禁绿 + 引擎面归 10-06 收口」而非回滚他人
  半件(回滚=触碰并行会话内容决策,风险更大;复核处方亦认可两途)。
- **证据指针澄清(次要)**:AC3 真跑报文无独立仓内工件(报文全文以
  引文录档内 AC3,取证脚本为一次性 /tmp 脚本未入库);复核已独立重跑
  证实(1 份 POST/application/json/title/message 与档记一致),AC3
  判定维持成立。

## 收口回执(2026-10-06,「余量全清」归档会话)

- **AC5 门禁半边回填(CI 绿)**:统一批全量门禁亲跑绿——pytest 全量
  4461 passed/40 skipped/0 failed(基线 4397→+64,含本档 17 用例)、
  vitest 523(26 文件,基线 508→+15 含 settings apprise 用例)、tsc -b
  零错、vite build 绿、cargo check --locked 零告警、cargo test 56/0、
  ruff 全仓绿;推送后 CI 绿(run 37352272165,conclusion=success,
  headSha ff3e4a9,gh run view 亲验)。AC5 复选框据此全勾成立。
- **AC4 装机像素**:维持「留装机批」注记(设置屏 apprise 下拉+真实
  doctor finding 行截图),随终轮装机刷新批补帧,同 bark AC4 判例。
- 归档:本档随「余量全清」收口段归档(task.py archive --no-commit,
  status review→completed 2026-10-06);提交链 65e1b96(实现 20 文件
  772 插入)+0d9380b(档置 review)+56d7b9f(复核处置);与 bark 并存
  决议(bark=零依赖快路/apprise=长尾统一)已在两档与 docs 六件承载,
  裁撤取舍留主人。
