# cron 心跳告警(品类久未成功触发,监控自己的调度健康)

## Goal

告警规则族新增「cron 心跳/僵尸调度」规则类型:**某品类超过阈值时间没有
成功触发**即告警(healthchecks.io 式 dead-man switch 的原生内建版)。
监控对象=MYIA 自身的调度健康——cron 挂了/品类配置坏了/任务一直失败,
主人现在只能靠不发消息「猜」,此件让沉默本身可告警。

## 背景与现状(锚点)

- 告警族在库:src/myssia/alerts/(engine.py 周期评估+rule.py
  CompiledAlertRule;规则经 alerts.save/fired 协议方法,10-04-alert-rules
  落地);告警走推送通道定向出站(W1 决议)。
- 调度账本在库:src/myssia/cron/executions.py(逐次执行记录,含成功/
  失败态)——**评估的数据源现成,零新采集**。
- cron 宿主与桌面 entry.py 均有周期循环;评估挂点选 alerts engine 周期
  评估侧(零 cron 侵入,见 R1)。
- grill Q7 决议:立项,原生件零外部依赖;主人令「都深化」后成档。

## Requirements

1. **规则类型 `cron_stale`**(rule.py 新类型,沿既有规则形态):
   - 参数:`category`(品类 id;可选 `job_id` 精确到单任务,缺省=品类级
     聚合)、`threshold_hours`(绝对小时数,**或**缺省=auto:2× 该品类
     schedule 期望间隔,auto 口径=从 jobs.json/schedule 推期望,推不出
     则要求显式 threshold——fail-fast 不猜);
   - 语义:距**上一次成功执行**(executions 账本查成功态;从未成功过=
     自安装/启用起算,账本无记录且超阈值也告警,首跑冷静期=1×期望间隔
     防装完即报)超阈值 → fire;
   - 防轰炸:fire 后进入冷却(冷却=threshold 重置,即恢复前不重复 fire;
     恢复=新成功出现 → 若告警族有 resolve 语义沿既有,无则发一条
     「已恢复」通知后清冷却)——**沿 alerts engine 既有冷却机制,零新
     状态机**(若 engine 无冷却,补通用冷却字段,所有规则受益)。
2. **评估挂点**:alerts engine 周期评估内(cron tick 触发或自有周期,
  沿 engine.py 现状定);**cron/ 侧零改动**为目标(只读账本)。
3. **协议面**:alerts.save 载荷新 type 枚举值 `cron_stale`+两参数键——
   加法可选字段,PROTOCOL_VERSION 维持(gates 先例);fired 应答零新键
   (detail 文案人话:「品类 X 已 N 小时无成功采集」)。
4. **UI 美化(消息屏告警面板)**:
   - 规则编辑器(messaging-screen.tsx:92-95 先例)类型下拉增「品类久未
     触发(心跳)」;选中后参数表单:品类下拉(源管理同源数据)+阈值
     输入+「自动(2× 期望间隔)」勾选态;
   - 表单文案人话:「盯着自己的定时任务——太久没跑成一条就喊你」;
   - fired 卡片:告警条目显示品类+静默时长+「查看执行历史」链接跳
     cron 屏(既有路由,零新屏);
   - a11y:阈值输入 label/单位(小时)分离,沿 ui-chore-batch label
     纪律(label 内禁嵌 labelable,spec 第 7 条)。
5. **CLI 面**:`myssia alerts` 既有命令族零改动(规则类型经既有 save
   通路人,天然支持)。

## 测试

- alerts 用例(造 executions 账本,纯 pytest):①久未成功→fire(断言
  detail 文案含品类与时长)②新鲜→静默 ③从未成功+超冷静期→fire
  ④冷却期内不重复 fire ⑤恢复→恢复通知+冷却清 ⑥auto 阈值推算
  (schedule 可推/推不出要求显式)⑦job_id 精确模式 ⑧schema:type
  枚举+参数校验(负数/零 threshold 拒)。
- 协议对账:alerts.save 载荷新 type 走既有对账例形态(加法可选,
  版本不动断言)。
- vitest:类型下拉+参数表单渲染(勾选自动态切换)+提交桩载荷形状
  {type:"cron_stale",category,threshold}+fired 卡文案与跳转链接+
  a11y 断言。

## 验证

- 真跑:沙箱数据根 MYIA_HOME 下造账本(改时间戳)→ 告警真实落库+
  推送 dry-run(stdout 通道)截图取证;
- 装机件:消息屏告警面板新类型表单+fired 卡像素(截屏+OCR 回执);
  装机包随下批刷新。

## Acceptance Criteria

- [ ] AC1 规则语义:八用例绿(含冷静期/冷却/auto 推算 fail-fast)。
- [ ] AC2 协议:加法可选字段;对账例绿;PROTOCOL_VERSION 不动。
- [ ] AC3 UI:表单三态(手填/自动勾选/品类选择)+fired 卡+跳转,像素
      回执在档;a11y 纪律沿 spec。
- [ ] AC4 真跑:沙箱账本驱动端到端(落库+stdout 通道)证据。
- [ ] AC5 门禁:全量 pytest/vitest/tsc/ruff 绿;gitnexus impact(rule.py
      符号)亲跑报半径。
- [ ] AC6 cron 零侵入:diff 亲证 src/myssia/cron/ 零改动(或如有必要
      改动,注记理由与账本只读口径)。

## 边界与红线

- 不做:外部 healthchecks.io 集成(原生件已覆盖);短信/电话级紧急升级
  (推送通道即上限);跨品类全局一条规则(逐品类/逐任务显式配,防误报面)。
- 红线:评估只读账本零写入;冷却语义不新建状态机(沿 engine 既有或
  补通用件)。

## 实施回执(2026-10-05 深夜第一批:引擎与存储面)

- **store v9**(sqlite.py):alert_rules 增 `kind`(缺省 'item')/`params`(JSON)两列;迁移幂等守卫(v6 PRAGMA 先例);INSERT/UPDATE/行映射三路带新列。既有行零漂移(=item/NULL)。
- **构造门**(rule.py):kind 越表拒;cron_stale 强制 scope 钉品类+when 占位 'true'+params 形状(threshold_hours>0 或 auto 二选一,可选 job_id);item 带 params 拒(防误配)。
- **引擎**(engine.py):run_pass 按 kind 过滤(cron_stale 零进条目路径);新 `heartbeat_pass()`——阈值=显式或 2×账本观测节奏夹 [1,168]h(观测不足 WARNING 跳过 fail-fast);从未成功以规则年龄当冷静期;**冷却=dedup_key 带时间桶过 record_fired UNIQUE 门闩,零新状态机**;恢复=近两桶 stale 行在场且未恢复过 → 恢复通知(同 UNIQUE 冷却);push 动作按**规则品类**解析通道(channel_resolver_for 注入,禁止借用评估宿主品类凭据);合成通知 `_HeartbeatNotice`(Item 鸭子形,myssia-alert: 伪协议,引擎不 import Pipeline 依赖方向红线)。
- **账本只读**(executions.py):`last_completed_at(job_ids)`(部分索引覆盖)+`completed_gap_hours(job_ids)`(中位间隔,<2 次观测 None);零写入。
- **UI**(messaging-screen.tsx+api.ts):类型单选(条件/心跳);心跳态 when 让位阈值组(数字输入+「自动」勾选,htmlFor 兄弟位 a11y 沿 ui-chore spec 第 7 条);scope 全局项知情禁用;预检换心跳专属(品类钉死+阈值两态);行内「心跳」徽章+阈值摘要(不露裸 when true);AlertRuleView/Input 加法可选 kind/params(旧壳新 UI 双向不炸)。
- **测试**:tests/alerts/test_heartbeat.py 新 25 例(迁移/构造门九拒/心跳语义含冷静期-冷却-恢复-auto 两态-push 按规则品类/双向零漂移/账本两查询);messaging vitest 新 3 例(表单两态+载荷形状+行徽章);版本金丝雀 8→9 六处随 v9 更新(refused 例改 SCHEMA_VERSION+1 免再漂)。
- **门禁(亲跑)**:定向 pytest tests/alerts+store/pipeline 金丝雀+sidecar 单例 159 绿;全量 `uv run --no-sync pytest -q` → **4366 passed / 40 skipped / 0 failed**(9 例版本金丝雀随 v9 更新后全绿);vitest 全量 26 文件 **488 passed**;`tsc -b --force` 零错;ruff 全绿。真跑证据 /tmp/myia-heartbeat-evidence/e2e.json(账本节奏 4h→auto 阈值 8h;fire 文案含品类与时长;同桶冷却 0 复发)。
- **接线三件(第二批,随 /workflow 队列首件)**:①entry.py `_alert_rule_from_payload` 放行 kind/params(现未知键拒,UI 保存过不去)+alerts.list/save 视图透传;②pipeline 告警段挂 heartbeat_pass(账本/jobs 解析器注入:品类→job_ids→last_completed/gaps);③sidecar-protocol.md alerts.save 行补 kind/params 加法注记(版本不 bump 循 gates 先例)。当时 entry.py/协议文档被并行线占用(bundled-plugins-batch2),现已落地解禁。
- AC 状态:AC1 ✅(语义全测)AC2 ◐(store 面落地;entry 载荷门+文档注记=接线批)AC3 ◐(组件+vitest;真机像素归接线批随装机)AC4 ◐(引擎级真跑证据在档;宿主端到端归接线批)AC5 ✅(全量四门禁绿;impact 待接线批补)AC6 ✅(cron/ 仅增两只读查询,diff 亲证零写入)。

## 实施回执(2026-10-05 第二批:接线三件)

- **①entry.py 载荷门**:`_ALERT_RULE_INPUT_KEYS` 放行 `kind`/`params`(加法可选);`_alert_rule_from_payload` 只做类型形状门(kind 字符串缺省 'item'/params 映射或 null),语义门(kind 越表/cron_stale 形状/item 带 params 拒)统一走既有 `compile_rule`——与读库同门零第二实现;`_alert_rule_views` 随全字段透传两键(旧载荷零漂移,新 UI 按回显渲染心跳表单)。
- **②pipeline.py 挂点**:`_alert_pass` 尾挂 `_heartbeat_pass`(engine.run_pass 之后同段收口,共享外层 WARNING 隔离;无 cron_stale 规则零开销——不读 jobs.json/账本,不建 cron 目录)。账本解析器注入:品类→job_ids 经 `CronJobStore.load_jobs`(jobs.json 缺失=无 job 不建目录)分组(`_cron_jobs_by_category`:job 绝对 YAML 路径 stem 直配 > YAML id 兜底,entry 随包定位同款双路);`ExecutionLedger.last_completed_at`/`completed_gap_hours` 只读驱动(ISO 文本→aware datetime,naive 按本地解释);push 通道 `_category_config_for_heartbeat`:job 自身 YAML 优先(调度器真跑的就是它;**加载失败=降级不换源**——转投 plugins 根同名文件等于借别份配置的凭据)→ plugins 根(stem>id)兜底;`_build_channel` 同门。
- **③sidecar-protocol.md**:方法表 45 行 alerts.save + 契约段构造门清单补 kind/params 加法可选注记(PROTOCOL_VERSION 不 bump,gates 加法先例)。
- **引擎接口补完**(接线必要件):`heartbeat_pass` 的 `channel_resolver_for` 单参(category)无法表达「规则明配 stdout 而品类只有 telegram 必须降级」——扩为 (category, channel_name) 两参,品类定凭据来源/通道名定投递面;仅两个既有测试 lambda 随改,零其他调用方(grep 亲证)。
- **测试新增**:心跳文件 +3(管线端到端接线:stale fire 通道按规则品类解析宿主零 push 照发/新鲜静默/零心跳规则零 cron 足迹——目录不建);桌面协议 +2(kind/params 存取往返+旧载荷零漂移+全量替换双向透传;坏形状五例走 compile_rule 整批零写入——含视图派生字段回传被未知键门拒的口径注记)。
- **门禁(亲跑定向)**:pytest tests/alerts/+tests/pipeline/ 188 绿;tests/desktop/test_desktop_sidecar_protocol.py+tests/store/ 266 绿;tests/cron/ 320 绿(cron 零回归);vitest 定向 messaging-screen 56 绿;定向 ruff 六文件绿。全量门禁由统一脚本收口。
- **gitnexus impact(亲跑,AC5 补)**:`last_completed_at`/`completed_gap_hours` 各 LOW 风险、上游各仅 1 直接调用方=本批新注入的 `Pipeline.last_success_at`/`Pipeline.cadence_hours` 闭包(索引先 `analyze --index-only` 刷新——首轮增量写半程卡 incrementalInProgress,重跑后完成);detect-changes 本流符号:`_alert_rule_from_payload`/`_alert_rule_views`/`_ALERT_RULE_INPUT_KEYS`+新接线三流程,零既有流程改道。
- **真跑(AC4 宿主端到端)**:/tmp/myia-heartbeat-evidence/batch2-wiring.json(+脚本 batch2-wiring.py)——隔离数据根,①规则经 `entry._m_alerts_save`(UI 同款 kind/params 载荷)落库;②jobs.json+账本成功执行回拨 30h;③真 `Pipeline.run()`(宿主品类 server,本地 HTTP 源真采集 2 条,真时钟零注入)→ 心跳 fire:`cron-stale:ai-news:82926`,文案「已 30 小时无成功采集」,action_status=sent,**stdout 通道真发卡片行**(url=myssia-alert://heartbeat/ai-news);④二次 run 同桶 UNIQUE 门闩零复发;alerts.list 视图 kind/params/fired_count=1/last_fired_at 全量回显。
- AC 状态(累计):AC1 ✅ AC2 ✅(载荷门+对账例+文档注记,PROTOCOL_VERSION 实读不动)AC3 ◐→保存链路证据齐(协议往返+56 vitest;真机像素仍归装机批)AC4 ✅(宿主端到端+stdout 通道证据在档)AC5 ✅(第一批全量四门禁+本批 impact 亲跑;全量复跑归统一脚本)AC6 ✅(本批 cron/ 零改动,只消费公共读路径)。

## 实施回执(2026-10-05 第三批:复核处置)

复核两条均属实、均修复(无反驳项):

- **处置① job_id 精确模式落地(复核:构造门接受但全链零消费者)**——属实:engine.heartbeat_pass 只按 rule.scope 聚合、pipeline job_ids_for 同样品类级,PRD 需求 1「可选 job_id 精确到单任务」与测试清单⑦未兑现,而回执曾声明「AC1 ✅(语义全测)」——**该声明在 job_id 面为过度声明,特此更正**。修复:引擎观测集改按 (品类, job_id) 取——`last_success_at`/`cadence_hours` 解析器扩两参(job_id None=品类级聚合缺省);dedup 身份前缀带 job_id(`cron-stale:<品类>:<job_id>:<桶>`,UNIQUE=(rule_id,dedup_key) 下品类级/精确级规则互不挤占,恢复通知同前缀精确查);文案点名任务(「品类 X 的任务 job-y 已 N 小时无成功采集」);pipeline `job_ids_for` 精确分支直接返回 `[job_id]`。测试新 4 例:引擎级「健康同品类任务掩蔽不了被盯任务停摆」+品类级聚合掩蔽对照组(精确模式存在的理由)+恢复按 job 身份去重;接线级两 job(1h/30h)钉 job-b fire 点名。真跑:/tmp/myia-heartbeat-evidence/batch3-review.json——「盯 job-b」fire `cron-stale:ai-news:job-b:82926` 文案点名 job-b,同账本「品类级」规则被 job-a 健康掩蔽静默(该参数目的的实证)。
- **处置② 账本缺位零足迹守卫(复核:「评估只读账本零写入」红线窄边破口)**——属实:心跳规则在场+jobs.json 在场+executions.db 缺位(job 建好从未派发)时,`ExecutionLedger._connect` 的 mkdir+DDL 会自建 executions.db(复核亲测复现),executions.py「全部只读零写入」与 pipeline「零写入」声明在该边为假。修复:pipeline `_heartbeat_pass` 以 `db_path.exists()` 守卫——账本缺位 = 零执行记录(与空表查询同结果:never-succeeded 走规则年龄冷静期),不实例化不进连接零建库;executions.py 段注记改精确(查询零写入;连接期 DDL 自建库,红线由调用侧守卫达成)。测试新 1 例:jobs.json 在场+账本缺位 → 真 run 后 cron/ 目录清单前后一致(复核曾多出 executions.db 的窄边)+冷静期静默。真跑:batch3-review.json `executions_db_created: false`,cron/ 前后 [.jobs.lock, jobs.json, output] 一致。
- **门禁(亲跑定向)**:pytest tests/alerts/ 33(心跳文件,新 5)+tests/alerts/+tests/pipeline/ 193 绿;tests/desktop/test_desktop_sidecar_protocol.py+tests/store/+tests/cron/ 586 绿;定向 ruff 四文件绿。全量归统一脚本。
- AC 状态(累计更正):AC1 ✅(**补齐后成立**:八用例含⑦ job_id 精确模式全测;此前缺⑦的声明已更正)AC2 ✅ AC3 ◐(同前)AC4 ✅(三份真跑证据在档:b2 引擎级/batch2 宿主端到端/batch3 复核两条)AC5 ✅ AC6 ✅(账本缺位守卫后「只读零写入」红线全边成立,cron/ 本体三批累计仅注记级改动)。
