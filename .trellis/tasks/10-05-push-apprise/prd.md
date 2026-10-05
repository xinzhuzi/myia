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

- [ ] AC1 schema:apprise 入 PushChannel;targets 配即拒;明文 target 拒。
- [ ] AC2 实现:发送路径六用例绿;未装=结构化拒+doctor finding(不惊扰
      未配置用户)。
- [ ] AC3 extras:pyproject 组钉版;lock 不动;`pip install myssia[apprise]`
      后 json:// sink 真跑出报文证据。
- [ ] AC4 UI:编辑器下拉+doctor 行像素回执;文案人话。
- [ ] AC5 门禁:pytest/vitest/ruff 全绿;协议对账例零漂移(64 不动)。
- [ ] AC6 档:决议回写;主人点名清单落 notes(未点名=档挂 planning)。

## 边界与红线

- 不做:apprise API server(docker 常驻服务)形态——CLI 直发已够;
  替换/重构现有 31 通道——零触碰。
- 凭据红线:url 内 token 永不落 YAML 明文/日志(mask 先例同 telegram)。

## 放行回执(2026-10-05 深夜,主人令「都按建议去做」)

- 问题:Apprise 增量=长尾目标,主人未点名缺什么。做法:主人整体放行(2026-10-05 深夜「都按建议做」),排队第 3;开工条件=点名首个真目标(Pushover/Gotify/任一)即拆实现,或 Bark 落地后仍要长尾再启。顺序:heartbeat→bark→apprise→searxng→firecrawl。
- 执行顺序(全五档):cron-heartbeat(先做,零前置)→ push-bark → push-apprise(点名即启)→ source-searxng → firecrawl-selfhost-verify。
