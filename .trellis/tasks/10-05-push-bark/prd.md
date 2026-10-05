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

- [ ] AC1 schema/实现:六用例绿;group=MYIA 固定;零依赖落地。
- [ ] AC2 UI:编辑器下拉+提示文案像素回执。
- [ ] AC3 门禁:pytest/vitest/ruff 全绿;协议对账零漂移。
- [ ] AC4 真推:主人 iPhone 收到一条(AC manual,档可先 review)。
- [ ] AC5 档:与 Apprise 档的翻案条件记档(先落地者裁对方或并存由主人定)。

## 边界与红线

- 不做:通知声音/图标/时效级别(留池); Bark server 自建部署指南
  (README 一句话指路即可)。
- 红线:device key 明文拒;端点 URL 校验防 SSRF 花样 scheme(schema
  http/https 门同既有 webhook 字段先例)。
