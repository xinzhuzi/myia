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
