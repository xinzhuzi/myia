# 配置组多平台账号配置:微信/QQ/飞书等账号登录态管理

## 裁定语义(主人两轮纠偏钉死,2026-10-11)

**「本身账号」与「推送机器人」是两个不同的东西,严禁混淆:**

- **本身账号** = 用户个人的平台身份登录态(如 Telegram 网页线账号 telegram-alt1:主人自己的账号,扫码/验证码登录、账号列表、登录/删除/状态灯)。→ **本任务范围,归侧栏「配置」组**。
- **推送机器人** = bot 身份(telegram bot token、飞书自建应用 App ID/Secret、QQ 官方机器人 token、企业微信应用)——用来收发推送的机器人凭据。→ **不属本任务**,它们归「设置→推送」/消息屏,现有能力不动、不搬、不混入。

判定口径:配置卡上写的凭据如果是「应用的」(开放平台注册的应用/机器人),那是机器人配置;如果是「我这个人的登录态」,才是本任务的账号配置。

## Goal

侧栏「配置」组下,除 Telegram 外补齐微信、QQ、飞书等平台的**本身账号**配置入口(范式对齐 Telegram 配置卡:账号列表/登录/删除/状态灯)。

## 现状(2026-10-11 三路探查结论)

| 平台 | 现有通道(机器人,不属本任务) | 本身账号接入途径 | 可行性 |
|---|---|---|---|
| Telegram | bot token | ✅ 已落地:网页线 tg_web(浏览器登录,MYIA 自持登录态)+ Telethon(待 api_id) | 已完成 |
| 微信 | weixin 桥(Hermes iLink Bot) | 登录态全在 Hermes 私有域,**单活模型**(env 一组账号);MYIA 红线=不读私有内容/不写目录/不 vendor | 受限:不改上游只能做「账号档列表(只读文件名)+状态灯+引导终端扫码」;卡内登录/删除/多账号需上游新契约 |
| QQ | qqbot(官方机器人 AppID+Secret) | 官方**无个人 API**;唯一途径=第三方 NTQQ 族(NapCat/LLOneBot/Lagrange → 本机 OneBot HTTP/WS)——违反 ToS,2025 起封号检测加严,且需常驻双向收发(风险高于 tg_web 只读) | 技术可对接(仓库零基础),**合规风险待主人裁定** |
| 飞书 | feishu_card(自建应用 App ID/Secret) | user_access_token(OAuth 授权码/扫码;2h 有效+refresh 30 天无感续期)——但必须挂在自建应用下,语义是「用户对应用的授权态」;仓库零基础(OAuth 回调/刷新存储均无) | 可做,需新建 OAuth 面;凭据存储对齐钥匙链 `myia/feishu/<账号键>/…` |

**UI/存储范式(照 Telegram 模板)**:协议快照读(`*.status`)+ 浏览器模块单入口登录(`browser.open` kind 登记)+ 数据根目录即账号(`<数据根>/<platform>-web/<账号键>/`,0700/0600)+ 独立屏挂侧栏「配置」组;新增一张卡的成本 ≈ entry.py 两方法 + 一个领域模块 + 三个 UI 文件 + 四处注册行,**Rust 壳零改动**。

## 决议(2026-10-11,AskUserQuestion 未答 → 按推荐自主开工,主人可随时翻案)

- **D1 首发范围**:飞书账号线 + 微信受限状态卡。QQ 不做(见 D2)。
- **D2 QQ**:不接第三方 NTQQ 协议(封号风险 + 常驻双向风险面),QQ 只留官方机器人通道;若主人日后要接,翻案后挂独立档。
- **D3 微信**:接受受限形态——桥接状态灯 + 账号档有无 + 登录指引(引导终端 `hermes gateway setup` 扫码);**不做**账号文件名列表(探查明示「列文件名是否越红线需裁决」,保守避开)、不做卡内登录/删除(等 Hermes 上游契约)。
- **D4 UI(2026-10-11 主人令渠道本名制推翻原总屏方案)**:「平台账号」这个抽象词不存在——渠道入口以本名呈现。侧栏「配置」组 = YAML配置 / Telegram / **飞书**(/feishu)/ **微信**(/weixin),各渠道独立屏与 Telegram 平级;协议面 platform_accounts.* 聚合快照不动(内部契约,不出 UI)。原「平台账号」总屏/总卡删除。

## Acceptance Criteria

- [x] AC1 飞书账号·授权流:设置过 App ID/Secret(keychain 已在册)的前提下,「添加账号」= 构造飞书 OAuth 授权 URL(user_access_token 授权码流程)经系统浏览器打开 + sidecar 起本地 HTTP 回调端点(仅 127.0.0.1,镜像 feishu_callback 安全口径)接收 code → 换 user_access_token + refresh_token → 入钥匙链 `myia/feishu/<账号键>/user_access_token`、`/refresh_token`
- [x] AC2 飞书账号·存储与键规约:账号键全称律 `feishu-<标识>`(镜像 ACCOUNT_KEY_RE);label 存登录标记;删除=清该账号键全部钥匙链项(登录/刷新中拒删,镜像 telegram.web.delete 口径)
- [x] AC3 飞书账号·状态灯:探针=用 refresh_token 无感刷新可成功 → 绿;refresh 失效 → 灰(指引重授权);刷新出的新 token 对回写钥匙链(续期闭环)
- [x] AC4 微信段:桥接状态灯(bin_found/weixin_configured/gateway_alive 三布尔,复用 probe_bridge,零新契约)+「已配置账号档:有/无」+ 登录指引(命令展示+复制);诚实披露单活模型与红线
- [x] AC5 协议面:entry.py 新增 `platform_accounts.status`(feishu 账号数组+weixin 桥三布尔聚 aggregate)、`feishu_account.delete`、OAuth 回调端点生命周期管理(起/停);PROTOCOL_VERSION +1 并补版本史;Rust 壳零改动
- [x] AC6 UI:侧栏「配置」组加「平台账号」入口 + /platform-accounts 独立屏(镜像 tg-account 范式:PageHeader 无头、卡面段落、StatusDot、命令面板深链);添加授权流有轮询对账(镜像 telegram-card 5s×24)
- [x] AC7 测试与门禁:领域层(OAuth 换 token/刷新闭环/键规约/删除护栏)pytest;UI vitest(三态渲染/授权发起/删除护栏/微信段);全量 pytest+vitest+tsc+cargo build 绿
- [x] AC8 交付:入库 + 装机包刷新换装 + 无头冒烟;主人侧前置(飞书开放平台应用配置 OAuth 重定向 URL)与真机授权留指引

## Notes

- 复杂任务:探查 → grill 决议(各平台账号接入机制/用途语义/范围)→ design/implement → 实现。
- 链接者架构红线:一切外部件(协议实现/桥接件)走设置下载组件,永不改上游。
- 主人判例参照:详情弹窗不做横幅;UI 物种铁律;静默铁律(登录窗口拉起属主人明示动作除外,如 tg_web 添加账号)。

## 结果(交付回执,2026-10-11)

- **三笔入库**:`feat(desktop) 平台账号协议面 v15`(feishu_account.py 领域层 + entry.py 四方法 + OAuth 回调端点 + 协议注册表 +4 行)/ `feat(desktop) 「平台账号」独立屏`(卡 + api + 路由 + 侧栏 + 命令面板)/ `docs(task)` 决议+design。
- **门禁**:pytest 全量 5089 passed(pyenv e2e 协议版本钉死 14→15 随批修正后过);协议注册表对账 178/178;vitest 全量 710/710(卡测 7 用例);tsc -b + vite build 绿;Rust 壳零改动。
- **装机**:tauri build exit 0(世事.app 17.84MiB + DMG 0.0.3);备份 `/tmp/myssia-platform-accounts-backup-20260111-135918` 后 ditto 换装;strict verify 过;WKWebView 缓存清;包内 Python 源(`Resources/myssia-src/entry.py`)实证 `platform_accounts` 9 处命中;装机无头冒烟全 PASS(A0-A6)。
- **如实声明**:①授权流的真实闭环(飞书页登录→回调换 token)需主人侧前置——飞书开放平台应用安全设置登记重定向 URL `http://127.0.0.1:8731/callback`(未登记授权页报 redirect_uri 不合法,卡面有指引),真机授权留主人;②微信段按 D3 为受限形态(状态灯+指引),账号列表/卡内登录待 Hermes 上游契约;③QQ 按 D2 未接第三方协议,留官方机器人。

## 追记:渠道本名制落地(2026-10-11 晚,主人令)

- **主人裁定**:「平台账号,没有这个渠道,飞书就是飞书,不能叫做平台账号」——渠道入口以本名呈现,不用抽象总类词。
- **落地**(commit refactor 渠道本名制):总屏/总卡删除,拆为「飞书」(/feishu)+「微信」(/weixin)两张独立卡、独立屏,侧栏「配置」组 = YAML配置 / Telegram / 飞书 / 微信;命令面板与 IA 断言同步(导航十一屏)。协议面 platform_accounts.* 聚合快照不动(内部契约不出 UI)。
- **门禁**:vitest 713/713(卡测拆分 10 用例)、tsc、vite build;pytest 未涉(零 Python 改动)。
- **装机像素复验(无头桥真件)10/10 全 PASS**:飞书屏(空态/表单/8731 指引)、微信屏(**真实桥数据**:桥可用+CLI 真实路径+账号档已配置+gateway 在跑)、配置编辑(搜索 3/14 过滤+清空恢复+「打开位置」在场启用不真点)。截图 /tmp/verify-feishu.png、/tmp/verify-weixin.png、/tmp/verify-yaml-editor.png;换装备份 /tmp/myssia-rename2-backup-20261011-180441;装机冒烟全 PASS。
