# 机器人凭据屏:设置推送分区抽独立屏 + 凭据位扩全通道

主人选型(2026-10-11):侧栏「配置」组抽「机器人凭据」独立屏,与账号屏并列(账号/机器人语义各是各);同时凭据表单从 5 通道预设扩到已实装全通道。

## 背景

- 裁定语义(10-11-platform-account-config):本身账号 ≠ 推送机器人。配置组现有 YAML配置/Telegram/飞书/微信(账号面);机器人凭据面在 设置→推送,且**表单只预设 5 通道**(feishu_card/telegram/webhook/bark/apprise),其余通道(qqbot/wecom/dingtalk/slack/discord/email 等)凭据无 GUI,只能 YAML/keychain 手工。
- 主人问「其他渠道怎么没有」→ 选定:抽屏 + 扩全通道。

## 方案

1. **抽屏**:设置→推送分区(settings-screen.tsx 通道清单式配置:通道 Select + 凭据表单 + 保存(secret.set)+ 发送测试(push.test)+ 自定义凭据位兜底)抽为独立屏 `/bot-credentials`,侧栏「配置」组挂「机器人凭据」条目(与 Telegram/飞书/微信并列);设置屏原分区摘除留注释(照 Telegram 分区抽出先例)。
2. **扩通道**:PUSH_FIELDS_BY_CHANNEL 按「已实装通道集合」(platform-overview implemented 集合为基准)补齐凭据位;多字段通道(email/matrix/feishu_card 双字段)按字段集铺开;自定义凭据位兜底保留。
3. **发送测试**:逐通道 target 惯例对照 PUSH_TEST_TARGET_KEY 既有 5 例;push.test 协议不动。

## 决议与 AC(2026-10-11 探查回填定稿)

- **范围**:已实装 28 平台 − weixin(零凭据)− 4 extras 壳 = 23 家真凭据通道 + webhook/bark/apprise 已表内 3 家 = **GUI 凭据面 26 家**。
- **A/B 两派如实注明(探查最大发现)**:19 家新通道为 B 派(裸 resolve_credential,无 myia/push/<键> 钥匙链回退)——卡底条件提示段注明「品类 YAML 引用须写 keychain:myia/push/<键>,此处保存值即生效;发送测试传的就是该引用」;signal/bluebubbles 为 A 派先例。后端逐家迁 A 派属后续可选(改运行时语义,待主人拍板)。
- **webhook 型 URL 内嵌密钥统一按 password 位**(dingtalk/google_chat/teams)。

## Acceptance Criteria

- [x] AC1 抽屏:设置→推送分区整体迁 /bot-credentials 独立屏挂配置组(设置屏分区 5→4,原位留注释);IA 断言同步
- [x] AC2 扩通道:26 家全量凭据位(逐家源码核实);PUSH_SECRET_NAME_BY_CHANNEL/PUSH_TEST_TARGET_KEY/labels 三表齐
- [x] AC3 B 派提示:19 家条件提示段(keychain 引用口径);A 派(signal/bluebubbles)无此段
- [x] AC4 测试:预设位/空字段/自定义位/scope 拦截/bark/apprise/发送测试成败 8 用例;settings.test 推送块随屏迁移
- [x] AC5 门禁:vitest 716/716(全量)+ tsc + vite;pytest 零 Python 改动
- [x] AC6 交付:入库 + 装机包刷新换装 + 无头像素复验

## 结果(交付回执,2026-10-11 晚)

- **两笔入库**:feat 屏+扩通道 / fix 扩通道漏两表(装机像素复验抓出:下拉恒 5 家根因 = PUSH_CHANNELS 派生自 PUSH_SECRET_NAME_BY_CHANNEL,扩通道时漏补该表与 PUSH_TEST_TARGET_KEY——「cargo 指纹漏判 ui 改动须 touch main.rs」在册坑二次踩中,重打包 touch 后解决)。
- **门禁**:vitest 全量 716/716;tsc -b 绿;vite build 绿;pytest 零 Python 改动(全量 5089 基线在案)。
- **装机**:两轮换装备份 /tmp/myssia-botcred26fix-backup-20261011-183725、/tmp/myssia-final-backup-20261011-184357;strict verify 过;WKWebView 缓存清;装机无头像素复验 **12/12 全 PASS**(机器人凭据屏 26 通道下拉 + QQ 机器人 B 派提示 + 飞书/微信屏 + 配置编辑搜索与打开位置);package_smoke 全 PASS。
- **如实声明**:①B 派 19 通道的真实推送要吃到 GUI 存的值,品类 YAML 引用须写 keychain: 形态(卡底已注明);后端迁 A 派待主人拍板;②「发送测试」对全部通道可直接验连通;③通道声明/启停仍在品类 YAML。

## Notes

- 协议面 secret.set/push.test 不动;channel 通道声明/启停仍在品类 YAML(写回走 /yaml-editor)。
- UI 范式:/bot-credentials 独立屏(PageHeader 无头)+ 侧栏配置组 + 命令面板;IA 断言同步。
