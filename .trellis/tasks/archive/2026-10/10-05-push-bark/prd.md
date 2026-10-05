# Bark 原生推送通道(iOS 即时通知,零依赖小件)

## Goal

push 层新增 `bark` 原生通道:HTTP POST 一发即达 iOS(APNs 经 Bark 服务端),
**零第三方依赖、十行级实现**。定位=主人 iPhone 高频通知场景的即时性补位
(远超 TG/飞书的到达延迟)。

## 背景与现状(锚点)

- grill Q4 决议:**与 Apprise 档(10-05-push-apprise)不互斥但相关**——
  Apprise 原生含 `bark://`(一个依赖 160+ 目标);本档价值=零依赖原生
  (不想为 Bark 单独引 apprise 依赖时)。**翻案条件**:若 Apprise 档先落地
  且主人接受其依赖,本档可裁,档内记档即可。
- 通道注册:push/__init__.py :141/:180 注册表加一行+push/bark.py 新文件
  (telegram.py 最薄蓝本,~40 行预期)。
- 凭据纪律:device key 走 `target` 字段 env:/keychain: 引用(schema.py:788
  明文启动拒);端点非密(公共 Bark 服务或自建主机地址),可落 YAML。
- Bark 协议事实:`POST {endpoint}/{device_key}`,JSON 体 {title, body,
  group, sound?, icon?…};官方端点 https://api.day.app,自建同构
  (docker finb/bark-server)。

## Requirements

1. **schema**:PushChannel 增 `"bark"`;可选字段 `bark_endpoint: str | None`
   (缺省 `https://api.day.app`;自建填 `http://<host>:8080`);**不进
   CHANNEL_PLATFORMS 目录寻址**(同 webhook:配 targets 拒——Bark 无目录
   语义);`target`=device key 凭据引用。
2. **push/bark.py**:POST JSON,成功=2xx;`group` 固定 `"MYIA"`(iOS 通知
   分组聚合,信息流不刷屏);`sound`/`icon`/`level` 留池不实现(YAGIDA,
   需要时加可选字段);4xx/超时→结构化 PushError 透传(delivery 重试走
   既有 timeout/retries 字段,零新配置)。
3. **UI 美化**:yaml-editor 通道下拉增「Bark(iOS 推送)」;选中时
   target 提示「device key 走 env:/keychain: 引用(在 Bark App 里复制)」;
   bark_endpoint 字段提示「留空=官方服务;自建填主机地址」。doctor 零新增
   (endpoint 可达性不预检,send-time 错误即推送失败面,同其他通道)。
4. **协议面**:零改动(纯管线侧)。

## 测试

- tests/push/test_bark.py(mock httpx transport,先例:tests/push 既有
  通道用例):①200 成功(断言 URL 拼 endpoint/key+JSON 体 title/body/
  group=MYIA)②404(坏 key)→结构化错误含状态码 ③超时→透传 ④明文
  target 拒 ⑤自建 endpoint 拼接 ⑥配 targets 拒。
- schema 用例:literal 增员;bark_endpoint 校验(http/https scheme 门)。
- vitest:yaml-editor 下拉含 Bark+两处提示文案断言。

## 验证

- 离线:mock 全覆盖(上列)。
- 真跑(AC 留主人):主人从 Bark App 复制 key 进 keychain,发一条真推
  到 iPhone(30 秒人肉验证;AC 标 manual,不阻塞档收口)。

## Acceptance Criteria

- [x] AC1 schema/实现:六用例绿;group=MYIA 固定;零依赖落地。
  (tests/push/test_bark.py 13 用例:mock 六用例 + schema 面 + 管线下传;
  零第三方依赖——仅 httpx 既有栈;group=MYIA 断言钉死。)
- [x] AC2 UI:编辑器下拉+提示文案像素回执。
  (通道选择面 rg 定位=设置→推送表单——yaml-editor 为纯文本编辑器无通道
  下拉,PRD 所指消费点即此。回执=vitest DOM 断言(下拉项「Bark(iOS
  推送)」可选 + 两处提示文案在位 + device key 写 myia/push/
  BARK_DEVICE_KEY),48/48 绿;无头截图未做,像素级留装机批可补。)
- [x] AC3 门禁:pytest/vitest/ruff 全绿;协议对账零漂移。
  (定向亲跑:pytest tests/push+pipeline+test_schema+desktop 1556 绿 /
  alerts+cron+cli+docs+smoke 710 绿 / test_skill_doc+test_docs 135 绿;
  vitest settings 48/48 绿 + tsc 0 错;ruff 九文件绿。全量门禁归脚本
  统一跑。协议面零改动(纯管线侧);文档对账六件同步
  SKILL/write-a-plugin×3/schema×2 + 两 refs 测试表锁 env:BARK_DEVICE_KEY。)
- [ ] AC4 真推:主人 iPhone 收到一条(AC manual,档可先 review)。
  (验法:装 Bark App → 复制 device key → 设置→推送 选 Bark(iOS 推送)
  粘贴保存 → 点「发送测试」→ iPhone 锁屏见 MYIA 组通知即验。)
- [x] AC5 档:与 Apprise 档的翻案条件记档(先落地者裁对方或并存由主人定)。
  (已记于「背景与现状」:Apprise 原生含 bark://;本档=零依赖原生路线,
  两者不互斥,翻案权在主人。)

## 边界与红线

- 不做:通知声音/图标/时效级别(留池); Bark server 自建部署指南
  (README 一句话指路即可)。
- 红线:device key 明文拒;端点 URL 校验防 SSRF 花样 scheme(schema
  http/https 门同既有 webhook 字段先例)。

## 放行回执(2026-10-05 深夜,主人令「都按建议去做」)

- 问题:iPhone 通知高频与否未知。做法:主人整体放行,排队第 2(零依赖小件先行);真推 AC manual 留主人=装 Bark App 复制 key 入 keychain 发一条即验;验后不高频通道留着零成本。
- 执行顺序(全五档):cron-heartbeat(先做,零前置)→ push-bark → push-apprise(点名即启)→ source-searxng → firecrawl-selfhost-verify。

## 实施回执(2026-10-05)

- **schema**(src/myssia/schema.py):PushChannel/PUSH_CHANNELS 增 `bark`;
  可选字段 `bark_endpoint`(非凭据,缺省 None=官方端点,常量定值在 push 层);
  http(s)+netloc scheme 门(code invalid_url,source url 先例);入
  _CHANNEL_OPTIONAL_FIELD_HOSTS(仅 bark 可配);**不进 CHANNEL_PLATFORMS**
  ——targets 即拒/target 必填走既有 platform-is-None 分支,零新校验逻辑。
- **通道**(src/myssia/push/bark.py,~200 行含注释):one-shot
  `POST {endpoint}/{device_key}` JSON {title, body, group:"MYIA"};title=
  card_title 跨通道一致;body 1024 字符截断(APNs 4KB 整包上限,CJK 3
  字节/字符预算);2xx 成功,4xx/超时结构化 PushSendError 透传(bark_api_error
  含 HTTP 状态码+体片段,死信分类按文本命中;http_error 含异常类型名);
  device key=env:BARK_DEVICE_KEY 引用,env 缺失回退钥匙链 myia/push/
  BARK_DEVICE_KEY(设置表单存入位);端点构造期形态门(ValueError fail-fast,
  schema 已拒 YAML 侧花样新 scheme);无重试环/无分段/无目录寻址
  (supports_targeting=False)。
- **接线**:push/__init__.py CHANNELS 增一行(不进 PLATFORMS);
  pipeline._W2_CHANNEL_FIELD_KWARGS 增 bark 行(bark_endpoint 下传)。
- **测试**:tests/push/test_bark.py 新文件 13 用例(mock transport 六用例:
  成功断言 URL+JSON 体/404 坏 key/超时零重试/明文 target 拒零请求/自建
  endpoint 尾斜杠容忍/targets 拒;schema 面:词表增员+不进 PLATFORMS/
  scheme 门三态/宿主守门/最小条目+自建落位;管线下传真 _build_channel)。
  受波及钉版三处如实更新:test_push_channels.py(集员+计数 31+
  非寻址集 {webhook,stdout,bark})、test_push_schema_targets.py
  (PUSH_CHANNELS 计数 31)、test_push.py(注册表钉死集增员)。
- **UI**(desktop/ui-src settings-screen.tsx):通道下拉增
  「Bark(iOS 推送)」(PUSH_CHANNEL_LABELS,既有通道=原名零漂移);
  Device Key 预设位(password,写 myia/push/BARK_DEVICE_KEY);两处提示
  文案=字段 hint「在 iPhone 的 Bark App 里复制;凭据走 env:/keychain:
  引用(保存即入钥匙链)」+ 选中 bark 时的端点说明行「bark_endpoint:
  留空 = 官方服务(api.day.app);自建 bark-server 填主机地址——写在品类
  YAML push: 节」;「发送测试」自动带 keychain:myia/push/BARK_DEVICE_KEY
  (PUSH_TEST_TARGET_KEY 增行)。vitest 新增 bark 用例(需补 Radix Select
  jsdom 桩:pointer capture+scrollIntoView,dashboard/logs 屏同款,退出还原)。
- **文档对账**(六件+两测试表):skill/SKILL.md(枚举行/§2.13 channel+
  targets 行/bark_endpoint 行/凭据约定段)、docs/write-a-plugin.md(通道
  词表行+凭据 bullet,含自建 docker finb/bark-server 一句话指路)、
  docs/{zh,en}/write-a-plugin.md(凭据 bullet)、docs/{zh,en}/schema.md
  (PUSH_CHANNELS 行+channel 行+bark_endpoint 行);tests/test_skill_doc.py
  与 tests/test_docs.py 的 _CHANNEL_CREDENTIAL_ENV_REFS 增
  env:BARK_DEVICE_KEY(锁三处文档不悬空)。注:zh/en schema.md 的
  channel 行此前已缺 weixin(既有漂移,非本流引入,未顺手改)。
- **零第三方依赖**:仅 httpx 既有栈;doctor 零新增(endpoint 可达性不
  预检,send-time 错误即推送失败面,同其他通道);协议面零改动。

## 归档会话注记(2026-10-06,「余量全清」收口段)

- AC1/2/3/5 已勾(实施回执在档);**AC4 真推 manual 留主人不阻断归档**
  (prd 明文「档可先 review」;验法:装 Bark App→复制 device key→设置→
  推送选 Bark 粘贴保存→「发送测试」→iPhone 锁屏见 MYIA 组通知即验)。
- AC3 门禁半边收口补:统一批全量亲跑绿(pytest 4461/40/0+vitest 523+
  tsc/vite build+cargo check/test 56+ruff)+CI 绿(run 37352272165,
  success,headSha ff3e4a9)。
- 提交链 208a599+8ba0285;与 Apprise 并存决议两档互记,取舍留主人。
