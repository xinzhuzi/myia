/**
 * 平台总览(task 10-03-messaging-hermes-look R2/R3):消息屏最上区,布局照上游
 * Hermes 蓝本(~/.hermes/hermes-agent/apps/desktop/src/app/messaging/index.tsx)
 * 的「左列平台卡 + 右栏详情面板」(MasterDetail)结构重排 —— MYIA 栈内贴近,
 * 不逐字拷贝 TSX:
 *
 * - 左列:平台卡网格(头像 + 名称 + 状态点;R1 头像芯片见 platform-icons)。
 *   点击卡选中,右栏切换内容;窄屏(<lg)折叠为上下布局。
 * - 右栏:详情面板 = 平台描述 / 三态状态说明(证据来源)/ 出站凭据指南
 *   (platforms 任务 R4 内容移入此处,左卡不再内嵌展开)/ 已连接时的目录
 *   条目速览(只读;改名/别名编辑仍在下方「通道目录」)。
 * - 三态色彩(R3,走 MYIA 语义 tokens,不硬编码色值):已连接=绿(--ok)、
 *   需要设置=黄(--warning)、即将支持=灰(--muted/--muted-foreground);
 *   状态点(StateDotTone)+ 状态胶囊(StatePill)+ 卡片描边共用同一套
 *   tone 映射,筛选 tabs 激活态与对应 tone 呼应。第四态 bridge_unavailable
 *   (微信桥接灰「需本机 Hermes」,10-03-messaging-weixin-bridge D4)复用
 *   coming_soon 的 muted 灰值;微信卡不走通用三态派生(凭据不在 MYIA 侧,
 *   永黄不了),状态来自 sidecar bridge.status 探测。
 * - 筛选(全部/已连接/未启用)沿用;切筛选时若当前选中平台不再匹配,选中
 *   栏自动切入该筛选下第一张卡(上游 handleStatusFilter 同交互流)。
 * - 三态派生纯函数(目录桶 + secret.list 名单 → 状态)零协议往返,见下方。
 * - token 贯彻(task 10-03-ui-deep-imitation,结构零动):辅文/标识 11px 与
 *   代码块 10px 统一落阶梯 text-2xs(10px 属阶外值,就近日拢 11px);详情头
 *   15px→text-base(14px,阶内);平台卡 hover 过渡走动效 token
 *   duration-(--duration-fast)+ease-out-expo(与 ui 基件同款)。
 */
import { useMemo, useState } from "react";
import type { ReactNode } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

import { isDeadEntry, type BridgeStatusView, type ChannelEntry } from "./api";
import { PlatformAvatar } from "./platform-icons";

// ---------------------------------------------------------------------------
// 平台清单(前端常量;数据源:父任务 10-03-hermes-messaging PRD W1/W2/W3 波次表)
// ---------------------------------------------------------------------------

/** 一条出站凭据 key 的说明(与 run 时实际读取的环境变量名一一对应)。 */
export interface PlatformGuideKey {
  /** 凭据 key(环境变量名;协议面只出名,值永不出)。 */
  key: string;
  /** 用途,直白中文一句话。 */
  purpose: string;
}

/** 指南一步:纯文本,或「文字 + 命令块」(curl 等可复制命令)。 */
export type PlatformGuideStep = string | { text: string; code: string };

/** 已实装平台的出站凭据指南(R4;唯一入口在右栏详情面板)。 */
export interface PlatformGuide {
  keys: PlatformGuideKey[];
  steps: PlatformGuideStep[];
}

/**
 * 目录条目的来源形态(状态说明/空目录文案按它分流,W2 起三平台为 manual):
 * - auto:平台列表 API 主动发现(飞书 im/v1/chats);
 * - passive:无发现 API,条目随入站消息被动积累(Telegram);
 * - manual:无自动发现(蓝本事实)——条目只能直达 id 或别名手工登记
 *   (ntfy/钉钉/企微,task 10-03-messaging-w2-platforms)。
 */
export type PlatformDiscovery = "auto" | "passive" | "manual";

/** 已实装平台(目录/发送链路已入库,状态真实派生)。 */
export interface ImplementedPlatform {
  id: string;
  name: string;
  /** 接入波次(W1 先行 / W2 消息平台第二批 / W3 长尾批)。 */
  wave: "W1" | "W2" | "W3";
  /** 详情面板头部的一行直白描述(只陈述已实装的事实,不预告功能)。 */
  description: string;
  guide: PlatformGuide;
  discovery: PlatformDiscovery;
}

/** 未实装平台(W2/W3 波次;灰卡「即将支持」)。 */
export interface UpcomingPlatform {
  id: string;
  name: string;
  wave: "W2" | "W3";
}

export const IMPLEMENTED_PLATFORMS: readonly ImplementedPlatform[] = [
  {
    id: "feishu",
    name: "飞书",
    wave: "W1",
    discovery: "auto",
    description: "飞书开放平台机器人(W1 已实装):tenant_access_token 出站卡片发送 + 群目录发现;凭据经环境变量注入 run。",
    guide: {
      keys: [
        {
          key: "FEISHU_BOT_TOKEN",
          purpose: "tenant_access_token(应用级令牌);出站卡片发送与群目录发现共用,run 时读环境变量",
        },
      ],
      steps: [
        "打开飞书开放平台(open.feishu.cn)→ 开发者后台 → 「创建企业自建应用」,记下应用的 App ID 与 App Secret。",
        "在应用里添加「机器人」能力;「权限管理」开通 im:message:send_as_bot(以机器人身份发消息)和 im:chat:readonly(读机器人所在群列表,目录发现用)。",
        "「版本管理与发布」发布版本并让组织管理员审核通过;把机器人拉进要推送的群。",
        {
          text: "手工换 tenant token:在终端执行下面这条(把 cli_xxx / xxx 换成你的 App ID / App Secret),应答里的 tenant_access_token 字段就是令牌;细节以开放平台文档「获取 tenant_access_token 内部接口」页为准。",
          code: 'curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \\\n  -H "Content-Type: application/json" \\\n  -d \'{"app_id":"cli_xxx","app_secret":"xxx"}\'',
        },
        "把令牌写入环境变量 FEISHU_BOT_TOKEN(例如在 ~/.zshrc 加一行 export FEISHU_BOT_TOKEN=t-xxx,重开终端/应用后生效)。注意令牌有效期约 2 小时,过期后按上一步重换并更新环境变量。",
        "回到本屏点飞书分组里的「刷新」列出群目录,再到下区「推送规则」勾选推送对象。",
      ],
    },
  },
  {
    id: "telegram",
    name: "Telegram",
    wave: "W1",
    discovery: "passive",
    description: "Telegram Bot API(W1 已实装):BotFather 令牌出站发送 + 会话随真实 bot 流量被动积累入目录。",
    guide: {
      keys: [
        {
          key: "TELEGRAM_BOT_TOKEN",
          purpose: "机器人令牌;出站发送与被动目录积累共用,run 时读环境变量",
        },
        {
          key: "TELEGRAM_CHAT_ID",
          purpose: "缺省推送会话的数字 chat_id;只在规则没写 targets 的旧式用法里生效",
        },
      ],
      steps: [
        "在 Telegram 里找 @BotFather 发送 /newbot,按提示给机器人起显示名和用户名(用户名须以 bot 结尾);BotFather 最后回复的 HTTP API token 就是 TELEGRAM_BOT_TOKEN。",
        "拿 chat_id:找 @userinfobot 发任意消息,它回复里的 Id 就是你自己的数字 chat_id(与机器人的私聊会话就用它)。",
        "群聊不必手抄 id:把机器人拉进群、在群里发条消息,本屏目录会直接记下该群;私聊目录同理——不给机器人发消息,目录里就不会有会话。",
        "把令牌与 chat_id 写入环境变量 TELEGRAM_BOT_TOKEN 与 TELEGRAM_CHAT_ID(例如在 ~/.zshrc 里 export,重开终端/应用后生效)。",
        "给机器人发条消息后回本屏刷新:目录出现该会话,即可在「推送规则」里勾选它。",
      ],
    },
  },
  {
    id: "ntfy",
    name: "ntfy",
    wave: "W2",
    discovery: "manual",
    description:
      "ntfy 通知(W2 已实装):one-shot POST 到 {server}/{topic},纯文本/可选 markdown;topic 即地址,无目录概念,推送对象直达或别名登记。",
    guide: {
      keys: [
        {
          key: "NTFY_TARGET",
          purpose: "{server}/{topic} 整串(如 https://ntfy.sh/my-alerts);run 时读环境变量,规则写 targets 时可省(公共 ntfy.sh 兜底)",
        },
        {
          key: "NTFY_TOKEN",
          purpose: "可选鉴权:自建 server 开了访问控制时填(access token 或 user:pass);公共匿名 topic 不用配",
        },
      ],
      steps: [
        "选 server:公共 ntfy.sh 开箱即用(无需注册);要私有部署可在自己机器上跑 ntfy 容器(binaries/docker,见 docs.ntfy.sh 的 install 页)。",
        "定一个 topic 名(字母/数字/-/_,如 my-games-alerts);手机装 ntfy App(或开 ntfy.sh 网页)订阅同名 topic——订阅即接收,无需服务端登记。",
        {
          text: "冒烟一发确认链路(手机订阅 my-games-alerts 后执行,应立刻收到通知):",
          code: 'curl -d "hello from MYIA" https://ntfy.sh/my-games-alerts',
        },
        "把整串写入环境变量 NTFY_TARGET(如 export NTFY_TARGET=https://ntfy.sh/my-games-alerts);需要鉴权的自建 server 再配 NTFY_TOKEN。",
        "推送规则里 targets 直达写 ntfy:my-games-alerts;常用地名可在数据根 channel_aliases.json 登记别名(ntfy 无自动发现,别名/直达是仅有的两条寻址路)。",
      ],
    },
  },
  {
    id: "dingtalk",
    name: "钉钉",
    wave: "W2",
    discovery: "manual",
    description:
      "钉钉自定义机器人 webhook(W2 已实装):msgtype=text 群消息;可选加签(HMAC-SHA256,MYIA 增量);一个 webhook = 一个群,无目录发现。",
    guide: {
      keys: [
        {
          key: "DINGTALK_WEBHOOK_URL",
          purpose: "自定义机器人的完整 webhook URL(内嵌 access_token,即投递端点);run 时读环境变量",
        },
        {
          key: "DINGTALK_SECRET",
          purpose: "可选:机器人安全设置选了「加签」时的 SEC 密钥(经品类 YAML 的 dingtalk_secret 引用配置);不配 = 裸 webhook",
        },
      ],
      steps: [
        "在钉钉电脑端打开要推送的群 → 右上角群设置 → 机器人 → 添加机器人 → 自定义。",
        "安全设置三选一:自定义关键词(消息须含该词)/ 加签(推荐,拿 SEC 密钥)/ IP 白名单;记下勾选项——推送被 310000 拒绝时先回这里核对。",
        "完成添加后复制 Webhook 地址(https://oapi.dingtalk.com/robot/send?access_token=…),写入环境变量 DINGTALK_WEBHOOK_URL。",
        "安全设置选了「加签」:把 SEC 密钥存入钥匙链或环境变量,品类 YAML 的 push 条目配 dingtalk_secret: env:DINGTALK_SECRET(或 keychain: 引用)。",
        {
          text: "冒烟一发确认链路(把 URL 换成你的 webhook,群里应立刻收到):",
          code: 'curl -s https://oapi.dingtalk.com/robot/send?access_token=xxxx \\\n  -H "Content-Type: application/json" \\\n  -d \'{"msgtype":"text","text":{"content":"hello from MYIA"}}\'',
        },
        "多群 = 多个机器人:每个群的 webhook 在规则 targets 里直达写 dingtalk:<完整 webhook URL>,或别名登记;webhook URL 是凭据,别名文件是本机私有数据。",
      ],
    },
  },
  {
    id: "wecom",
    name: "企业微信",
    wave: "W2",
    discovery: "manual",
    description:
      "企业微信自建应用(W2 已实装):corpid+secret 换 access_token(7200s 缓存)发 text 私聊(touser);群聊/markdown 为蓝本外能力,未实装。",
    guide: {
      keys: [
        {
          key: "WECOM_CORPID",
          purpose: "企业 ID(管理后台「我的企业」页);run 时读环境变量",
        },
        {
          key: "WECOM_CORPSECRET",
          purpose: "自建应用的 Secret(应用详情页);换 access_token 用",
        },
        {
          key: "WECOM_AGENTID",
          purpose: "自建应用的 AgentId(应用详情页,数值串)",
        },
        {
          key: "WECOM_TUSER",
          purpose: "缺省推送对象:成员 userid(通讯录成员详情页);规则写 targets 时可省",
        },
      ],
      steps: [
        "浏览器打开企业微信管理后台 work.weixin.qq.com(需管理员)→ 应用管理 → 自建 → 创建应用,记下 AgentId 与 Secret。",
        "「我的企业」页复制企业 ID(CorpId);把三者分别写入环境变量 WECOM_CORPID / WECOM_CORPSECRET / WECOM_AGENTID。",
        "收件人 userid:管理后台通讯录点开成员,详情页的「账号」就是 userid;把要推送的成员拉进应用可见范围(60021/60020 报错先查可见范围与可信 IP)。",
        "应用详情页「企业可信 IP」填本机出口 IP——调用 message/send 的机器必须在名单内,否则报 60020(不安全的访问 IP)。",
        "推送规则:targets 直达写 wecom:<userid>(如 wecom:ZhangSan),常用人名别名登记;单发也可配 target: env:WECOM_TUSER 走缺省收件人。",
      ],
    },
  },
  {
    id: "weixin",
    name: "微信",
    wave: "W2",
    discovery: "manual",
    description:
      "微信桥接(W2 已实装,task 10-03-messaging-weixin-bridge):微信无官方出站 API,本通道是桥接实现——出站经本机常驻 Hermes-Agent 持有微信登录态与 context_token。无 Hermes 的环境此平台不可用,这是如实披露,不是缺陷。",
    guide: {
      // keys 段为空是刻意事实:MYIA 侧零凭据(登录态只存 Hermes 侧),
      // 没有任何环境变量/钥匙链可录(R2「不装可用」)。
      keys: [],
      steps: [
        "安装 Hermes-Agent(NousResearch/Hermes-Agent)并完成初始化;缺省 CLI 路径 ~/.hermes/hermes-agent/.hermes/bin/hermes,装在别处时在品类 YAML 的 push 条目配 weixin_hermes_bin: <路径>。",
        "在 Hermes 侧执行 hermes gateway setup 扫码登录微信;登录态与 context_token 只存 Hermes 侧,MYIA 不持有任何微信凭据(本指南无密钥可录)。",
        {
          text: "自查推送对象的 peer id(会话地址,形如 xxx@im.wechat 私聊 / xxx@chatroom 群):",
          code: "~/.hermes/hermes-agent/.hermes/bin/hermes send --list weixin",
        },
        "推送规则 targets 直达写 weixin:<peer id>;常用对象可在数据根 channel_aliases.json 登记别名(微信无自动发现,直达/别名是仅有的两条寻址路)。",
        "注意:对方长期没给 bot 发过消息时,冷发送会得到「会话未就绪」指引(先让对方发条消息再推)——这是微信协议的固有限制,不是故障;修复后无需任何配置变更。",
      ],
    },
  },
  // W3 长尾转实装(task 10-03-messaging-w3-longtail 组二/组三):email/sms/irc/
  // simplex 四家适配器已入库(注册见 src/myssia/push/__init__.py 的
  // _W3_LONGTAIL_CHANNELS/PLATFORMS),伞任务验收项「UI 卡转实装+凭据指南落地」。
  {
    id: "email",
    name: "邮件",
    wave: "W3",
    discovery: "manual",
    description:
      "邮件 SMTP 出站(W3 已实装):smtplib 纯标准库一封一报,tls(465 隐式)/ starttls(587)缺省按端口推导;收件人直达 email:<地址> 或别名登记,无目录发现。",
    guide: {
      keys: [
        { key: "EMAIL_ADDRESS", purpose: "发件人地址(From);run 时读环境变量" },
        {
          key: "EMAIL_PASSWORD",
          purpose: "SMTP 密码/授权码;不配 = 匿名投递(本机中继 localhost:25 合法态)",
        },
        { key: "EMAIL_SMTP_HOST", purpose: "SMTP 服务器主机(必需,如 smtp.qq.com);run 时读环境变量" },
        { key: "EMAIL_SMTP_PORT", purpose: "端口(可选;缺省 587,填 465 自动走隐式 TLS)" },
        { key: "EMAIL_SMTP_SECURITY", purpose: "可选 tls/starttls/plain;缺省按端口推导" },
        { key: "EMAIL_TO", purpose: "缺省收件人地址;规则写 targets 时可省" },
      ],
      steps: [
        "准备一个发件邮箱:QQ/163 等在邮箱设置里开启 SMTP 服务并生成「授权码」(不是登录密码);Gmail 用账户页的应用专用密码。",
        "把发件人与服务器写入环境变量:export EMAIL_ADDRESS=you@example.com、EMAIL_PASSWORD=授权码、EMAIL_SMTP_HOST=smtp.example.com(端口可省:缺省 587 走 STARTTLS,填 465 自动改走隐式 TLS)。",
        "收件人:推送规则 targets 直达写 email:addr@example.com;单发也可配 target: env:EMAIL_TO 走缺省收件人。",
        "邮箱无「列出联系人」API(蓝本事实):常用收件人在数据根 channel_aliases.json 登记别名;标题与摘要正文一致,可选用户模板自定排版。",
        "内网本机中继:机器上有 localhost:25 中继时可完全不配 EMAIL_PASSWORD(匿名投递,合法态不报错)。",
      ],
    },
  },
  {
    id: "sms",
    name: "短信",
    wave: "W3",
    discovery: "manual",
    description:
      "短信 Twilio REST 出站(W3 已实装):one-shot POST Messages.json(HTTP Basic 鉴权),单条上限 1600 字符超长截断;收信号码直达 sms:<E.164> 或别名登记,无目录发现。",
    guide: {
      keys: [
        { key: "TWILIO_ACCOUNT_SID", purpose: "Twilio 账号 SID(Console 首页);run 时读环境变量" },
        { key: "TWILIO_AUTH_TOKEN", purpose: "Twilio Auth Token(Console 首页);与 SID 拼 HTTP Basic" },
        { key: "TWILIO_PHONE_NUMBER", purpose: "发信号码(E.164,须是 Twilio 名下号码)" },
        { key: "SMS_TO", purpose: "缺省收信号码(E.164);规则写 targets 时可省" },
      ],
      steps: [
        "注册 Twilio(console.twilio.com)→ Console 首页记下 Account SID 与 Auth Token。",
        "号码:Console → Phone Numbers → Buy a number 购入可发短信的号码;trial 账号只能发给已验证号码,发中国大陆手机号需先在 Geographic Permissions 申请地理权限(资费较高,先核对)。",
        "把三者写入环境变量:export TWILIO_ACCOUNT_SID=AC…、TWILIO_AUTH_TOKEN=…、TWILIO_PHONE_NUMBER=+1…(必须 E.164 形态,否则发送期报 invalid_credential_ref)。",
        "收信号码:targets 直达写 sms:+8613800138000(E.164);单发也可配 target: env:SMS_TO。",
        "短信无「列出可达对象」API:常用收件人在数据根 channel_aliases.json 登记别名;正文超 1600 字符自动截断(不拆多条)。",
      ],
    },
  },
  {
    id: "irc",
    name: "IRC",
    wave: "W3",
    discovery: "manual",
    description:
      "IRC 出站(W3 已实装):纯标准库 asyncio 一次性会话(NICK → JOIN → 分段 PRIVMSG → QUIT,缺省 6697 TLS);频道直达 irc:<#频道> 或别名登记,无目录发现。",
    guide: {
      keys: [
        { key: "IRC_SERVER", purpose: "IRC 服务器主机(公共网络如 irc.libera.chat 或自建);run 时读环境变量" },
        {
          key: "IRC_NICK",
          purpose: "bot 昵称;一次性会话实际用 {nick}-push,不与常驻客户端抢注",
        },
        { key: "IRC_CHANNEL", purpose: "缺省目标(#频道 或裸 nick DM);规则写 targets 时可省" },
        { key: "IRC_SERVER_PASSWORD", purpose: "可选服务器 PASS 密码;不配则不发 PASS" },
        { key: "IRC_NICKSERV_PASSWORD", purpose: "可选 NickServ 密码(注册 nick 完成后 IDENTIFY);不配则跳过" },
      ],
      steps: [
        "选网络与频道(公共网络如 libera.chat,或自建 ircd);确认要用的 nick 可用,需保号则在 NickServ 注册。",
        "环境变量:export IRC_SERVER=irc.libera.chat、IRC_NICK=myssia-push;缺省端口 6697 走 TLS。",
        "可选:IRC_SERVER_PASSWORD(服务器 PASS)、IRC_NICKSERV_PASSWORD(NickServ IDENTIFY)。",
        "频道目标:targets 直达写 irc:#频道名;裸 nick DM 不设直达(与中文别名撞形),经别名登记后按名寻址。",
        "IRC 无列表 API(蓝本事实):无自动发现,条目唯一来源 = 直达 + channel_aliases.json 别名;正文按 510 字节行预算自动分段。",
      ],
    },
  },
  {
    id: "simplex",
    name: "SimpleX",
    wave: "W3",
    discovery: "auto",
    description:
      "SimpleX 出站(W3 已实装):本机 simplex-chat 守护进程的 WebSocket JSON API,超长按 8000 字符切块;22 家长尾平台中唯一的目录发现(/contacts + /groups)。",
    guide: {
      keys: [
        {
          key: "SIMPLEX_WS_URL",
          purpose: "守护进程 WS 地址(可选;缺省 ws://127.0.0.1:5225,本机服务模式)",
        },
        {
          key: "SIMPLEX_CHAT",
          purpose: "缺省会话(group:<id> 或 DM 显示名的引用);规则写 targets 时可省",
        },
      ],
      steps: [
        "本机安装 simplex-chat 并以服务模式启动守护进程(simplex-chat -p 5225 类;用法见 simplex.chat 文档的 CLI/服务模式页)。",
        "安装 WS 客户端库(可选依赖,缺装时发送/发现报 dependency_missing 并附安装命令):pip install 'myssia[simplex]' 或 uv add 'myssia[simplex]'。",
        "地址缺省 ws://127.0.0.1:5225;改端口时把 SIMPLEX_WS_URL 配成指向新地址的 env: 引用。",
        "推送对象:群直达写 simplex:group:<群 id>;DM 按显示名寻址——回本屏点 SimpleX 组的「刷新」列出联系人与群(长尾平台里唯一的目录发现)。",
      ],
    },
  },
  // W3 长尾转实装(task 10-03-messaging-w3-longtail 组一/组二):whatsapp_cloud/
  // google_chat/teams/matrix 四家适配器已入库(注册见 src/myssia/push/__init__.py
  // 的 _W3_LONGTAIL_CHANNELS/PLATFORMS),伞任务验收项「UI 卡转实装+凭据指南落地」。
  {
    id: "whatsapp_cloud",
    name: "WhatsApp",
    wave: "W3",
    discovery: "manual",
    description:
      "WhatsApp Cloud API(W3 已实装):Graph POST 到 /{phone_number_id}/messages + Bearer 永久访问令牌,text 按 4096 官方上限分段;收件人直达 E.164 号码,无自动发现。",
    guide: {
      keys: [
        {
          key: "WHATSAPP_CLOUD_TOKEN",
          purpose: "永久访问令牌(System User 令牌);run 时读环境变量,发送期才解析",
        },
        {
          key: "WHATSAPP_CLOUD_PHONE_NUMBER_ID",
          purpose: "发送方电话号码 id(Cloud API 注册号码,Meta 开发者后台 API Setup 页);run 时读环境变量",
        },
        {
          key: "WHATSAPP_CLOUD_TO",
          purpose: "缺省收件人 wa_id(E.164);规则写 targets 时可省",
        },
      ],
      steps: [
        "打开 developers.facebook.com → My Apps → Create App(类型选 Business)→ 添加 WhatsApp 产品;「WhatsApp → API Setup」页记下电话号码 id(Phone number ID),写入环境变量 WHATSAPP_CLOUD_PHONE_NUMBER_ID。",
        "换永久令牌:同一 App 的 Business 设置里创建 System User 并授权 whatsapp_business_messaging,生成永久访问令牌(Permanent token)写入 WHATSAPP_CLOUD_TOKEN——API Setup 页给的临时令牌 24 小时过期,不宜常驻。",
        "接收方号码须先在该页「To」管理过(五档验证/模板会话内),否则报 131030「不在允许名单」;把常用收件人登记后再发。",
        {
          text: "冒烟一发确认链路(把 id/令牌/号码换成你的,应答含 messages[].id 即 wamid):",
          code: 'curl -X POST "https://graph.facebook.com/v20.0/$WHATSAPP_CLOUD_PHONE_NUMBER_ID/messages" \\\n  -H "Authorization: Bearer $WHATSAPP_CLOUD_TOKEN" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"messaging_product":"whatsapp","recipient_type":"individual","to":"+8613800000000","type":"text","text":{"body":"hello from MYIA","preview_url":true}}\'',
        },
        "推送规则 targets 直达写 whatsapp_cloud:+8613800000000(E.164);WhatsApp 无「列出收件人」API(蓝本事实),常用人名在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  {
    id: "google_chat",
    name: "Google Chat",
    wave: "W3",
    discovery: "manual",
    description:
      "Google Chat(W3 已实装):空间 incoming webhook 直发(one-shot POST,text 按 4000 上限拆条);URL 内嵌 key/token 即凭据,零 SA 密钥文件(蓝本 SA 形态不移植)。",
    guide: {
      keys: [
        {
          key: "GOOGLE_CHAT_WEBHOOK_URL",
          purpose: "空间 incoming webhook 完整 URL(chat.googleapis.com/…,key/token 内嵌);run 时读环境变量",
        },
      ],
      steps: [
        "浏览器打开 chat.google.com 进入要推送的空间 → 点空间名 →「应用与集成」(Apps & integrations)。",
        "「Webhook」→「添加 Webhook」,起个名字(如 MYIA 推送)→ 保存后复制 URL(https://chat.googleapis.com/v1/spaces/<id>/messages?key=…&token=…)。",
        "把整串 URL 写入环境变量 GOOGLE_CHAT_WEBHOOK_URL(URL 内嵌凭据,等同密钥保管,不要提交进仓库)。",
        {
          text: "冒烟一发确认链路(空间里应立刻出现消息;2xx 即成功):",
          code: 'curl -s -X POST "$GOOGLE_CHAT_WEBHOOK_URL" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"text":"hello from MYIA"}\'',
        },
        "推送规则 targets 直达写 google_chat:<完整 webhook URL>(一个 webhook = 一个空间);常用地名在数据根 channel_aliases.json 登记别名(Chat 无自动发现,蓝本事实)。",
      ],
    },
  },
  {
    id: "teams",
    name: "Microsoft Teams",
    wave: "W3",
    discovery: "manual",
    description:
      "Microsoft Teams(W3 已实装):Power Automate Workflows incoming webhook 直发 Adaptive Card(2xx 即成功,应答是字面 1);旧 O365 connector 已被微软退役,webhookb2 是现行官方路径。",
    guide: {
      keys: [
        {
          key: "TEAMS_WEBHOOK_URL",
          purpose: "Workflows incoming webhook 完整 URL(https://<tenant>.webhook.office.com/webhookb2/…);run 时读环境变量",
        },
      ],
      steps: [
        "打开 make.powerautomate.com(Power Automate)→ 创建 → 搜模板「Post to a channel when a webhook request is received」(收到 Teams webhook 请求时发布到频道)。",
        "配置目标团队与频道并创建;流程详情页复制给出的 URL(https://<tenant>.webhook.office.com/webhookb2/…)——注意旧 O365 connector(outlook.office.com/webhook)已于 2024-2025 退役,别再用那条路。",
        "把 URL 写入环境变量 TEAMS_WEBHOOK_URL(webhookb2 路径段本身是凭据,等同密钥保管)。",
        {
          text: "冒烟一发确认链路(频道里应立刻出现卡片,应答是字面 1 不是 JSON):",
          code: 'curl -s -X POST "$TEAMS_WEBHOOK_URL" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"type":"message","attachments":[{"contentType":"application/vnd.microsoft.card.adaptive","content":{"type":"AdaptiveCard","version":"1.4","body":[{"type":"TextBlock","text":"hello from MYIA","wrap":true}]}}]}\'',
        },
        "推送规则 targets 直达写 teams:<完整 webhook URL>(一个 webhook = 一个频道);常用频道在数据根 channel_aliases.json 登记别名(Teams 无自动发现,蓝本事实)。",
      ],
    },
  },
  {
    id: "matrix",
    name: "Matrix",
    wave: "W3",
    discovery: "manual",
    description:
      "Matrix 出站(W3 已实装):任意 homeserver 的 Client-Server API 发 m.room.message 纯文本(Bearer token,#别名 先解析成房间 id,按 16000 分段);纯 REST 零新依赖,蓝本 mautrix/E2EE 不在出站范围。",
    guide: {
      keys: [
        {
          key: "MATRIX_HOMESERVER",
          purpose: "homeserver 基址(公共 https://matrix.org 或自建 matrix.example.com);run 时读环境变量",
        },
        {
          key: "MATRIX_ACCESS_TOKEN",
          purpose: "账号 access token(Bearer 鉴权);run 时读环境变量,发送期才解析",
        },
        {
          key: "MATRIX_ROOM_ID",
          purpose: "缺省房间(!id:server 或 #别名:server);规则写 targets 时可省",
        },
      ],
      steps: [
        "选 homeserver:公共 matrix.org 直接注册即可;自建可部署 Synapse/Conduit(部署见 matrix.org 的 self-hosting 文档)。把基址写入环境变量 MATRIX_HOMESERVER。",
        "用推送专用账号登录 Element 客户端,「设置 → 帮助与关于 → 高级」里的访问令牌即 MATRIX_ACCESS_TOKEN(或走下方 login 接口拿);让该账号加入要推送的房间。",
        {
          text: "不进 Element 也可直接 login 拿令牌(应答里的 access_token 字段):",
          code: 'curl -X POST "https://matrix.org/_matrix/client/v3/login" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"type":"m.login.password","identifier":{"type":"m.id.user","user":"myssia-bot"},"password":"xxx"}\'',
        },
        "房间地址取原生 id(!opaque:server.tld)或别名(#name:server.tld)——发送端点只收房间 id,别名会自动经 directory 端点解析。",
        "推送规则 targets 直达写 matrix:!room:server.tld 或 matrix:#alias:server.tld;CS API 无带名称的房间列表(蓝本事实),常用房间在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  // W3 长尾转实装(task 10-03-messaging-w3-longtail 组一):slack/discord/line/
  // mattermost 四家适配器已入库(注册见 src/myssia/push/__init__.py 的
  // _W3_LONGTAIL_CHANNELS/PLATFORMS),伞任务验收项「UI 卡转实装+凭据指南落地」。
  {
    id: "slack",
    name: "Slack",
    wave: "W3",
    discovery: "manual",
    description:
      "Slack Bot API(W3 已实装):xoxb bot token 经 chat.postMessage 出站(text 39000 上限分段);U/W 用户 id 发送期自动 conversations.open 换 DM 会话再投递;无目录发现,直达/别名两条寻址路。",
    guide: {
      keys: [
        {
          key: "SLACK_BOT_TOKEN",
          purpose: "bot token(xoxb- 开头);chat.postMessage 出站用,run 时读环境变量",
        },
        {
          key: "SLACK_CHANNEL",
          purpose: "可选:单目标推送的频道 id 引用(推荐名 env:SLACK_CHANNEL);规则写 targets 时可省",
        },
      ],
      steps: [
        "浏览器打开 api.slack.com/apps → Create New App → From scratch,起名创建(细节以 Slack 官方文档为准)。",
        "App 详情 → OAuth & Permissions → Bot Token Scopes 添加 chat:write(以 bot 身份发消息);要用 U/W 用户 id 直发 DM 再加 im:write(conversations.open 换 DM 会话)。",
        "Install to Workspace 安装应用 → 复制 Bot User OAuth Token(xoxb- 开头)写入环境变量 SLACK_BOT_TOKEN(例如在 ~/.zshrc 加一行 export,重开终端/应用后生效)。",
        "把 bot 邀请进要推送的频道(频道里 /invite @应用名);频道 id 以 C 开头(公开频道)/ G(私有群)/ D(DM 会话)/ U 或 W(用户)。",
        {
          text: "冒烟一发确认链路(把 token 与频道 id 换成你的,频道应立刻收到,应答 ok 为 true):",
          code: 'curl -s -X POST https://slack.com/api/chat.postMessage \\\n  -H "Authorization: Bearer xoxb-xxx" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"channel":"C0123ABCDEF","text":"hello from MYIA"}\'',
        },
        "推送规则 targets 直达写 slack:C…/G…/D…/U…/W…(U/W 发送期自动换 DM);slack 无自动发现(蓝本事实),常用地名在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  {
    id: "discord",
    name: "Discord",
    wave: "W3",
    discovery: "manual",
    description:
      "Discord Bot REST(W3 已实装):Bot token 直发 /channels/{id}/messages(content 2000 硬上限分段;话题定向改投话题端点);无目录发现,直达/别名两条寻址路。",
    guide: {
      keys: [
        {
          key: "DISCORD_BOT_TOKEN",
          purpose: "bot token;REST 出站用,run 时读环境变量",
        },
        {
          key: "DISCORD_CHANNEL_ID",
          purpose: "可选:单目标推送的频道 id 引用(17-20 位数字 snowflake);规则写 targets 时可省",
        },
      ],
      steps: [
        "浏览器打开 discord.com/developers/applications → New Application,起名创建(细节以 Discord 官方 Developer Portal 文档为准)。",
        "应用详情 → Bot → Reset Token 复制 bot token(只显示一次)写入环境变量 DISCORD_BOT_TOKEN。",
        "OAuth2 → URL Generator:scopes 勾 bot,复制生成的邀请链接在浏览器打开,把 bot 拉进你的服务器(给它 Send Messages 权限)。",
        "Discord 客户端开开发者模式(用户设置 → 高级 → 开发者模式);右键要推送的频道 → 复制频道 ID(17-20 位数字)。",
        {
          text: "冒烟一发确认链路(把 token 与频道 id 换成你的,频道应立刻收到):",
          code: 'curl -s -X POST https://discord.com/api/v10/channels/<频道id>/messages \\\n  -H "Authorization: Bot <token>" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"content":"hello from MYIA"}\'',
        },
        "推送规则 targets 直达写 discord:<snowflake 频道 id>;discord 无自动发现(蓝本事实),常用地名在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  {
    id: "line",
    name: "LINE",
    wave: "W3",
    discovery: "manual",
    description:
      "LINE Messaging API(W3 已实装):channel access token 经 message/push 出站,一次最多 5 泡(每泡 4500 字,超长丢弃并告警);无目录发现,直达/别名两条寻址路。",
    guide: {
      keys: [
        {
          key: "LINE_CHANNEL_ACCESS_TOKEN",
          purpose: "长寿命 channel access token;push 出站用,run 时读环境变量",
        },
        {
          key: "LINE_TO",
          purpose: "可选:单目标推送的接收方 id 引用(U/C/R 形态);规则写 targets 时可省",
        },
      ],
      steps: [
        "浏览器打开 developers.line.biz(Line Developers Console)→ 创建 provider → 在其下创建 Messaging API 频道(细节以 LINE 官方文档为准)。",
        "频道页 Messaging API 设定 → Channel access token (long-lived) → Issue,复制长寿命 token 写入环境变量 LINE_CHANNEL_ACCESS_TOKEN。",
        "接收方 id:用户 U / 群组 C / 聊天室 R(33 位十六进制)。注意官方约束:用户类接收方须已把该官方账号(bot)加为好友,push 才送得到;群组/聊天室 id 官方只经 webhook 事件下发,MYIA 零入站拿不到——推送对象优先用用户 U id。",
        {
          text: "冒烟一发确认链路(把 token 与接收方 id 换成你的,HTTP 200 + 空 body 即成功):",
          code: 'curl -s -X POST https://api.line.me/v2/bot/message/push \\\n  -H "Authorization: Bearer <token>" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"to":"U0000ffffffff0000ffffffff0000ffff","messages":[{"type":"text","text":"hello from MYIA"}]}\'',
        },
        "推送规则 targets 直达写 line:U…/C…/R…;line 无自动发现(蓝本事实),常用地名在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  {
    id: "mattermost",
    name: "Mattermost",
    wave: "W3",
    discovery: "manual",
    description:
      "Mattermost 自建服务器(W3 已实装):REST /api/v4/posts(Bearer token,4000 上限分段)主路 + incoming webhook 退路(按解析值形态分发);无目录发现(蓝本走常驻 websocket,出站-only 不含),直达/别名两条寻址路。",
    guide: {
      keys: [
        {
          key: "MATTERMOST_TOKEN",
          purpose: "personal/team access token(Bearer);REST 路出站用,run 时读环境变量",
        },
        {
          key: "MATTERMOST_SERVER",
          purpose: "自建服务器 base URL(如 https://mm.example.com);REST 路必填,webhook 路 URL 自带 host",
        },
        {
          key: "MATTERMOST_CHANNEL_ID",
          purpose: "可选:单目标推送的引用——26 位 channel id(REST 路)或整条 incoming webhook URL(webhook 路);规则写 targets 时可省",
        },
      ],
      steps: [
        "需要一个 Mattermost 服务器(自建部署或云版;部署文档见 mattermost.com)——它是自建协作平台,没有官方托管外的公共实例。",
        "personal access token:需管理员在 System Console 开启后,个人设置 → Security → Personal Access Token → Add,复制 token 写入环境变量 MATTERMOST_TOKEN;服务器地址写入 MATTERMOST_SERVER。",
        "channel id(26 位小写字母数字):点频道名 → View Info 面板可见/复制(版本较旧时在 System Console → User Management → Channels 可查;以 Mattermost 官方文档为准)。",
        "webhook 退路(免 token/server):管理员开 Incoming Webhook 后,频道 → Integrations → Incoming Webhook 创建,得到的整条 URL(https://…/hooks/xxx)直接作为 target 引用的解析值。",
        {
          text: "冒烟一发确认链路(REST 路;把 server/token/频道 id 换成你的,应答 201):",
          code: 'curl -s -X POST https://mm.example.com/api/v4/posts \\\n  -H "Authorization: Bearer <token>" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"channel_id":"<26位channel id>","message":"hello from MYIA"}\'',
        },
        "推送规则 targets 直达写 mattermost:<26位 channel id>;无自动发现(蓝本走常驻 websocket 会话,MYIA 出站-only 不含),常用地名在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  // W3 长尾转实装(task 10-03-messaging-w3-longtail 组三):homeassistant 适配器
  // 已入库(注册见 src/myssia/push/__init__.py 的 _W3_LONGTAIL_CHANNELS/
  // PLATFORMS),UI 卡随转(伞任务验收项「UI 卡转实装+凭据指南落地」)。
  {
    id: "homeassistant",
    name: "Home Assistant",
    wave: "W3",
    discovery: "manual",
    description:
      "Home Assistant 通知出站(W3 已实装):one-shot POST /api/services/notify/notify(Bearer 长期访问令牌),标题+正文(超 4096 截断);HA 无「列出通知目标」API(蓝本事实),推送对象直达目标名或别名登记。",
    guide: {
      keys: [
        {
          key: "HASS_URL",
          purpose: "HA 实例基址(浏览器打开 Home Assistant 的那个地址,如 http://homeassistant.local:8123);run 时读环境变量,不配不猜",
        },
        {
          key: "HASS_TOKEN",
          purpose: "长期访问令牌(HA 用户页「安全」标签创建);出站调用的 Bearer 凭据,run 时读环境变量",
        },
        {
          key: "HASS_TARGET",
          purpose: "可选缺省通知目标;仅在品类 YAML 显式配 target: env:HASS_TARGET 且规则没写 targets 时生效",
        },
      ],
      steps: [
        "确认 HA 实例的访问地址(浏览器里打开 Home Assistant 的那个地址,如 http://homeassistant.local:8123),写入环境变量 HASS_URL。",
        "创建长期访问令牌:HA 左下角点自己的用户名 → 「安全」标签页拉到底 → 「长期访问令牌」→ 创建,起个名(如 myssia-push)并复制,写入环境变量 HASS_TOKEN。",
        "确认通知目标:手机装 Home Assistant Companion App 并登录,目标名形如 mobile_app_<设备名>;或用 HA 里配置好的 notify 实体/群组(如 notify.mobile)——目标名就是推送地址。",
        {
          text: "冒烟一发确认链路(把地址/令牌/目标换成你的;HA 通知或手机 App 应立刻收到):",
          code: 'curl -X POST http://homeassistant.local:8123/api/services/notify/notify \\\n  -H "Authorization: Bearer $HASS_TOKEN" \\\n  -H "Content-Type: application/json" \\\n  -d \'{"title":"hello","message":"hello from MYIA","target":"mobile_app_pixel"}\'',
        },
        "推送规则:targets 直达写 homeassistant:<目标名>(如 homeassistant:mobile_app_pixel);只推固定目标时也可配 target: env:HASS_TARGET 走缺省。HA 无「列出通知目标」的 API,常用目标在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  // W3 长尾转实装·组一/组三(task 10-03-messaging-w3-longtail,伞验收项
  // 「UI 卡转实装+凭据指南落地」):qqbot/msgraph_webhook 有 one-shot 出站;
  // bluebubbles/yuanbao 是 PRD R3 的 extras 壳——寻址已接线,发送路待
  // extras 实装(状态/说明走 EXTRAS_SHELL_PLATFORM_IDS 分支如实披露)。
  {
    id: "qqbot",
    name: "QQ 机器人",
    wave: "W3",
    discovery: "manual",
    description:
      "QQ 开放平台机器人(W3 已实装):AppID+ClientSecret 换 access_token,主动消息 REST 直发(c2c:/group:/guild: 三寻址形态;群聊有每月主动额度);无目录发现,直达/别名登记。",
    guide: {
      keys: [
        {
          key: "QQBOT_APP_ID",
          purpose: "机器人 AppID(QQ 开放平台管理后台「开发设置」页);换 access_token 用,run 时读环境变量",
        },
        {
          key: "QQBOT_CLIENT_SECRET",
          purpose: "机器人的 ClientSecret(同页「开发设置」);与 AppID 成对使用",
        },
        {
          key: "QQBOT_TARGET",
          purpose: "可选缺省推送对象(值如 group:ABCDEF / c2c:xxx / guild:999);规则写 targets 时可省",
        },
      ],
      steps: [
        "打开 QQ 机器人开放平台管理后台(bot.q.qq.com)→ 选择/创建机器人,「开发设置」页记下 AppID 与 ClientSecret。",
        "把两者写入环境变量 QQBOT_APP_ID 与 QQBOT_CLIENT_SECRET(例如在 ~/.zshrc 里 export,重开终端/应用后生效);发送期自动换 access_token(2024-04 后的 QQBot 新鉴权形态),无需手工管 token。",
        "拿推送对象 id:主动消息无「列出会话」API(MYIA 又零入站)——群 group_openid / 用户 openid 只能从机器人真实交互的官方回调或后台数据获得,频道 channel_id 在频道设置可见。",
        "推送规则 targets 直达写 qqbot:group:<group_openid> / qqbot:c2c:<openid> / qqbot:guild:<channel_id>;单发也可配 target: env:QQBOT_TARGET 走缺省对象;常用对象在数据根 channel_aliases.json 登记别名。",
        "注意主动消息额度(官方:群聊每月 4 条/群):额度耗尽时官方错误原样上抛,是配额事实不是故障;正文超 2000 字符自动按行边界拆多条(每条计入额度)。",
      ],
    },
  },
  {
    id: "msgraph_webhook",
    name: "MS Graph Webhook",
    wave: "W3",
    discovery: "manual",
    description:
      "Microsoft Teams/Graph 群聊直发(W3 已实装):Azure 应用 client credentials 换 token,POST /chats/{id}/messages(app-only,需应用权限 Chat.ReadWrite);只寻址 1:1/群聊 chat,团队频道走 teams 通道;无目录发现。",
    guide: {
      keys: [
        {
          key: "MSGRAPH_WEBHOOK_TENANT_ID",
          purpose: "Azure 租户(目录)ID(应用注册「概述」页);拼 token 端点 URL 用,run 时读环境变量",
        },
        {
          key: "MSGRAPH_WEBHOOK_CLIENT_ID",
          purpose: "应用程序(客户端)ID(同页);client credentials 三件套之一",
        },
        {
          key: "MSGRAPH_WEBHOOK_CLIENT_SECRET",
          purpose: "客户端密码的「值」(「证书和密码」页,只显示一次);三件套之一",
        },
        {
          key: "MSGRAPH_WEBHOOK_CHAT_ID",
          purpose: "可选缺省接收 chat(19: 前缀 Graph chat id);规则写 targets 时可省",
        },
      ],
      steps: [
        "浏览器打开 Azure 门户 portal.azure.com(需管理员)→ Microsoft Entra ID → 应用注册 → 新注册,记下「目录(租户) ID」与「应用程序(客户端) ID」。",
        "「证书和密码」→ 新建客户端密码并立刻复制「值」(离开页面后不可再看);三者写入环境变量 MSGRAPH_WEBHOOK_TENANT_ID / MSGRAPH_WEBHOOK_CLIENT_ID / MSGRAPH_WEBHOOK_CLIENT_SECRET。",
        "「API 权限」→ 添加权限 → Microsoft Graph → 应用权限(不是委托权限)→ Chat.ReadWrite → 回列表点「代表 {租户} 授予管理员同意」——app-only 发 chat 消息的官方路径。",
        "拿 chat id(形如 19:…@unq.gbl.spaces 私聊 / 19:…@thread.v2 群聊):从 Teams 会话或 Graph 查询获得;写入 MSGRAPH_WEBHOOK_CHAT_ID,或规则 targets 直达写 msgraph_webhook:19:…。",
        "边界如实:团队频道消息需 RSC 已装 bot(不在本通道,频道场景走 teams 通道的 Workflows webhook);无自动发现(app-only 无会话列表),常用会话别名登记。",
      ],
    },
  },
  {
    id: "bluebubbles",
    name: "BlueBubbles",
    wave: "W3",
    discovery: "manual",
    description:
      "BlueBubbles iMessage 桥(W3 壳通道):寻址面已接线(chat GUID/手机号直达),发送路待 extras 实装——出站依赖自建 BlueBubbles 服务端(常驻 macOS),当前发送如实报 dependency_missing,不假装可用。",
    guide: {
      // keys 段为空是刻意事实(同微信桥接的零凭据面):壳通道当前不读
      // 任何环境变量——发送门在 extras 实装 + 服务端部署;服务端
      // password 凭据项待发送路实装后补录。
      keys: [],
      steps: [
        "现状如实:本平台是 W3 实装的 extras 壳——寻址已可用,发送路待 extras 实装批次;当前推送会报 dependency_missing(依赖未提供),不是配置错误。",
        "部署 BlueBubbles 服务端(https://bluebubbles.app,常驻 macOS 并接管 Messages.app 的 iMessage 桥):这是外部系统级依赖,不是 pip 包。",
        "推送对象先行接线:直达写 bluebubbles:iMessage;… / SMS;… chat GUID 或 +手机号(新会话按地址直开);常用对象在数据根 channel_aliases.json 登记别名(无自动发现——chat 列表 API 需常驻服务端)。",
        "等 extras 实装批次提供发送路(纯 httpx,无额外 pip 依赖;届时本指南补服务端 password 凭据项)。",
      ],
    },
  },
  {
    id: "yuanbao",
    name: "元宝",
    wave: "W3",
    discovery: "manual",
    description:
      "腾讯元宝(W3 壳通道):寻址面已接线(direct:/group:/裸 id 直达),发送路待 extras 实装——元宝无 one-shot HTTP 出站(蓝本事实:常驻 WebSocket 网关),当前发送如实报 dependency_missing,不假装可用。",
    guide: {
      // keys 段为空是刻意事实:壳通道当前不读任何环境变量——蓝本凭据
      // (YUANBAO_APP_ID/APP_SECRET)属常驻 WS 网关客户端,MYIA 壳尚未
      // 读取;待 extras 实装后补录。
      keys: [],
      steps: [
        "现状如实:元宝无 one-shot HTTP 出站(蓝本事实:出站走常驻 WebSocket 网关,sign-token → AUTH_BIND → 心跳);本平台是 W3 实装的结构化报错壳,当前推送恒报 dependency_missing,不是配置错误。",
        "MYIA 推送层是单发 one-shot 契约:常驻 WS 客户端随后续 extras 提供(依赖 uv add websockets;蓝本凭据 YUANBAO_APP_ID/YUANBAO_APP_SECRET,届时本指南补凭据项)。",
        "寻址先行接线:直达写 yuanbao:direct:<account_id> / group:<group_code> / 裸 id;常用会话别名登记(无自动发现)。",
        "急需元宝触达的可先改用其余 one-shot 通道(email/sms/homeassistant/ntfy/webhook)。",
      ],
    },
  },
  // W3 长尾转实装·组三收尾(task 10-03-messaging-w3-longtail,伞验收项
  // 「UI 卡转实装+凭据指南落地」):a2a 有官方 HTTP 出站(A2A v1.0
  // JSON-RPC);buzz/photon/raft 是 PRD R3 的 extras 壳——寻址已接线,
  // 发送路待 extras 实装(状态/说明走 EXTRAS_SHELL_PLATFORM_IDS 分支如实披露)。
  {
    id: "a2a",
    name: "A2A",
    wave: "W3",
    discovery: "manual",
    description:
      "A2A 协议 v1.0 出站(W3 已实装):对端基址上一次 one-shot JSON-RPC SendMessage(A2A-Version: 1.0 头 + 单 text Part);无目录发现(Agent Card 描述对端能力而非会话列表),对端直达 URL 或别名登记。",
    guide: {
      keys: [
        {
          key: "A2A_PEER",
          purpose: "对端基址 URL(http(s):// 形态,如 https://agent.example.com);经品类 YAML 的 target: env:A2A_PEER 绑定,发送期读环境变量",
        },
        {
          key: "A2A_TOKEN",
          purpose: "可选:对端要求 Bearer 鉴权时的令牌;缺省引用 env:A2A_TOKEN,env 缺席 = 无鉴权(局域对端合法态)",
        },
      ],
      steps: [
        "确认对端:任何 A2A v1.0 agent 的 HTTP 端点基址(Linux Foundation 开放标准);对端在 Agent Card 里另配 RPC URL 时,把该 RPC URL 本身登记为基址即可(MYIA 不多抓一次 /.well-known/agent-card.json,推送场景省一次 GET)。",
        "把基址写入环境变量 A2A_PEER(例如 ~/.zshrc 里 export A2A_PEER=https://agent.example.com);对端要求鉴权再配 A2A_TOKEN。",
        "品类 YAML 的 push 条目写 channel: a2a 与 target: env:A2A_PEER(与钉钉 dingtalk_secret 同款 env: 引用形态);规则写 targets 定向时可省 target(schema 允许)。",
        {
          text: "冒烟一发确认链路(2xx 即对端已受理;result 载荷不解析,推送只认受理):",
          code: 'curl -s -X POST "$A2A_PEER" \\\n  -H "Content-Type: application/json" \\\n  -H "A2A-Version: 1.0" \\\n  -d \'{"jsonrpc":"2.0","id":"smoke-1","method":"SendMessage","params":{"message":{"role":"ROLE_USER","parts":[{"text":"hello from MYIA","mediaType":"text/plain"}],"messageId":"smoke-1","contextId":"smoke-1"}}}\'',
        },
        "推送规则 targets 直达写 a2a:<对端基址 URL>;a2a 无自动发现(蓝本事实),常用对端在数据根 channel_aliases.json 登记别名。",
      ],
    },
  },
  {
    id: "buzz",
    name: "Buzz",
    wave: "W3",
    discovery: "manual",
    description:
      "Buzz(W3 壳通道):Block 开源 Nostr 协作平台,寻址面已接线(频道 UUID 直达),发送路待 extras 实装——蓝本中继读写全经 buzz CLI 子进程 + Nostr 签名,无 one-shot HTTP 出站(蓝本事实),当前发送如实报 dependency_missing,不假装可用。",
    guide: {
      // keys 段为空是刻意事实(同上两壳):壳通道当前不读任何环境变量——
      // 中继地址/Nostr 私钥(BUZZ_RELAY_URL/BUZZ_PRIVATE_KEY)属 CLI 桥接
      // 的前置项,待 extras 实装后补录。
      keys: [],
      steps: [
        "现状如实:本平台是 W3 实装的 extras 壳——寻址已可用,发送路待 extras 实装批次;当前推送会报 dependency_missing(依赖未提供),不是配置错误。",
        "修复路径(错误文案同款携带):安装 buzz CLI(https://github.com/block/buzz,置于 PATH 或配 BUZZ_CLI_PATH),并备好 Nostr 中继地址与私钥(BUZZ_RELAY_URL / BUZZ_PRIVATE_KEY,nsec 或 hex)——CLI 桥接随后续 extras 批次评估,届时本指南补凭据项。",
        "推送对象先行接线:直达写 buzz:<频道 UUID>;常用频道在数据根 channel_aliases.json 登记别名(无自动发现——频道列表只在 buzz CLI 侧)。",
      ],
    },
  },
  {
    id: "photon",
    name: "Photon",
    wave: "W3",
    discovery: "manual",
    description:
      "Photon(W3 壳通道):Spectrum 平台(含 iMessage),寻址面已接线(space id 的 UUID 形态 / 裸 E.164 号码直达),发送路待 extras 实装——蓝本收发均走 spectrum-ts SDK 的 gRPC 长流(经 Node sidecar),无 one-shot HTTP 出站,当前发送如实报 dependency_missing,不假装可用。",
    guide: {
      // keys 段为空是刻意事实(同上壳):PHOTON_PROJECT_ID/PHOTON_PROJECT_SECRET
      // 属 Node sidecar 的凭据,待 extras 实装后补录。
      keys: [],
      steps: [
        "现状如实:本平台是 W3 实装的 extras 壳——寻址已可用,发送路待 extras 实装批次;当前推送会报 dependency_missing(依赖未提供),不是配置错误。",
        "修复路径(错误文案同款携带):部署 Node sidecar(spectrum-ts SDK,https://photon.codes/,蓝本 sidecar/package.json 精确锁版 + npm ci)并配置 PHOTON_PROJECT_ID/PHOTON_PROJECT_SECRET(app.photon.codes 项目凭据)——随后续 extras 批次评估,届时本指南补凭据项。",
        "推送对象先行接线:直达写 photon:<UUID(space id)或 +E.164 号码>(蓝本文档 space id/E.164 两形态,DM 由号码解析);常用会话别名登记(无自动发现——会话列表依赖 Spectrum SDK 长流)。",
      ],
    },
  },
  {
    id: "raft",
    name: "Raft",
    wave: "W3",
    discovery: "manual",
    description:
      "Raft(W3 壳通道):工作区协作平台,寻址面已接线(别名登记;蓝本 chat_id 是运行期会话标识,无直达形态),发送路待 extras 实装——蓝本读写全经 Raft CLI 子进程 + 本地唤醒桥,无 one-shot HTTP 出站,当前发送如实报 dependency_missing,不假装可用。",
    guide: {
      // keys 段为空是刻意事实(同上壳):RAFT_PROFILE 是工作区 agent 标识,
      // 属 CLI 桥接前置项,待 extras 实装后补录。
      keys: [],
      steps: [
        "现状如实:本平台是 W3 实装的 extras 壳——寻址已可用,发送路待 extras 实装批次;当前推送会报 dependency_missing(依赖未提供),不是配置错误。",
        "修复路径(错误文案同款携带):安装 Raft CLI(https://raft.build)并在工作区登记 agent profile(RAFT_PROFILE)——CLI 桥接随后续 extras 批次评估,届时本指南补凭据项。",
        "推送对象先行接线:raft 无直达形态(蓝本 chat_id 形态无公开成文约束,MYIA 不猜)——目标一律在数据根 channel_aliases.json 登记别名(目录精确名/唯一前缀可寻址)。",
      ],
    },
  },
];

/** W3 未实装平台(父任务 PRD 波次表登记锚点;灰卡,零交互)。微信已于
 * 10-03-messaging-weixin-bridge 转实装(桥接,见 IMPLEMENTED_PLATFORMS);
 * ntfy/钉钉/企微已于 10-03-messaging-w2-platforms 转实装;
 * slack/discord/line/mattermost(组一)、whatsapp_cloud/google_chat/teams/
 * matrix(组二)与 email/sms/irc/simplex/homeassistant(组三)已于
 * 10-03-messaging-w3-longtail 转实装;qqbot/msgraph_webhook(组一)与
 * bluebubbles/yuanbao、a2a(组三出站)与 buzz/photon/raft(组三 extras
 * 壳)亦已转实装(见 IMPLEMENTED_PLATFORMS);余下 signal(需 signal-cli
 * 守护进程,蓝本事实见伞任务 PRD 波次表)。 */
export const UPCOMING_PLATFORMS: readonly UpcomingPlatform[] = [
  { id: "signal", name: "Signal", wave: "W3" },
];

/** 未实装平台的详情描述(按波次;不虚构平台功能,只说排期与实装后的去处)。 */
const UPCOMING_DESCRIPTION: Record<"W2" | "W3", string> = {
  W2: "尚未实装;已排入 W2(近期)波次。实装后此处将给出出站凭据指南与目录速览。",
  W3: "尚未实装;在 W3(远期)波次排期中。实装后此处将给出出站凭据指南与目录速览。",
};

// ---------------------------------------------------------------------------
// 三态派生(纯函数,零协议往返、零后端概念)
// ---------------------------------------------------------------------------

/** 平台卡四态:已连接 / 需要设置 / 即将支持 / 需本机 Hermes(微信桥接灰态,
 * task 10-03-messaging-weixin-bridge D4:微信凭据不在 MYIA 侧,黄态「按凭据
 * 指南录入」是误导,永黄不了——桥接探测可用=绿,否则=灰)。 */
export type PlatformCardStatus = "connected" | "needs_setup" | "coming_soon" | "bridge_unavailable";

/** 筛选档(R2):全部 / 已连接 / 未启用。 */
export type PlatformFilter = "all" | "connected" | "disabled";

/** 一张平台卡的视图模型(左网格渲染、筛选与详情面板的最小完整单元)。 */
export interface PlatformCard {
  id: string;
  name: string;
  wave: "W1" | "W2" | "W3";
  status: PlatformCardStatus;
  /** 目录条数(仅已实装平台有;灰卡恒 0)。 */
  directoryCount: number;
  /** 钥匙链探测命中的凭据名(状态说明里展示「已录几项」;空 = 无钥匙链证据)。 */
  matchedSecretNames: string[];
  guide: PlatformGuide | null;
  /** 详情面板头部的一行描述(已实装 = 事实描述;未实装 = 波次排期说明)。 */
  description: string;
  /** 目录来源(已实装平台才有;灰卡无目录概念,恒 undefined)。 */
  discovery?: PlatformDiscovery;
  /** 桥接探测结果(仅微信卡携带;null = 探测未完成/失败,如实按不可用呈现)。 */
  bridge: BridgeStatusView | null;
}

/**
 * 钥匙链名单里挑出该平台的凭据名(探测口径,secret.list 返回名)。
 *
 * 命中两种形态之一:`myia/<platform>/<name>`(scope=平台 id)或任意
 * scope 下叶子名等于该平台凭据 key(如 `myia/push/FEISHU_BOT_TOKEN`)。
 */
export function matchSecretNames(
  platformId: string,
  credentialKeys: readonly string[],
  allNames: readonly string[],
): string[] {
  return allNames.filter((name) => {
    if (!name.startsWith("myia/")) return false;
    const rest = name.slice("myia/".length);
    const slash = rest.indexOf("/");
    if (slash <= 0) return false;
    const scope = rest.slice(0, slash);
    const leaf = rest.slice(slash + 1);
    return scope === platformId || credentialKeys.includes(leaf);
  });
}

/**
 * 已实装平台 → 已连接 / 需要设置(纯前端派生)。
 *
 * 已连接 = 凭据可解析(钥匙链探测命中)**或** 目录桶非空 —— 目录条目只能
 * 经一次成功的发现(feishu)或真实 bot 流量(telegram 被动积累)进入,
 * 非空即「凭据当时可用且刷新成功」的前端可见证据(env: 令牌不在钥匙链,
 * 这条信号覆盖它)。两条证据都没有 = 凭据缺失 → 需要设置。
 */
export function deriveImplementedStatus(
  bucket: readonly ChannelEntry[],
  matchedSecretNames: readonly string[],
): "connected" | "needs_setup" {
  const credentialsFound = matchedSecretNames.length > 0;
  const refreshSucceeded = bucket.length > 0;
  return credentialsFound || refreshSucceeded ? "connected" : "needs_setup";
}

/** W3 extras 壳通道(10-03-messaging-w3-longtail PRD R3:bluebubbles 需
 * 自建服务端、yuanbao 需常驻 WS 网关、buzz/photon/raft 需 CLI/Node
 * sidecar 桥——蓝本均无 one-shot HTTP 出站):寻址已实装,发送路待
 * extras——状态不随钥匙链/目录证据派生(别名目录条目 ≠ 可发送,绿态
 * 「已连接」是误导),恒 needs_setup;说明走壳分支如实披露(R2「不装
 * 可用」)。 */
const EXTRAS_SHELL_PLATFORM_IDS: ReadonlySet<string> = new Set([
  "bluebubbles",
  "yuanbao",
  "buzz",
  "photon",
  "raft",
]);

/** 目录桶 + 钥匙链名单 + 微信桥接探测 → 全量平台卡(已实装在前,波次序在后)。
 *
 * 微信卡不走通用 deriveImplementedStatus(凭据不在 MYIA 侧,
 * 永黄不了):bridge.status available → connected,否则(含探测缺位/
 * 失败的 null)→ bridge_unavailable 灰态。extras 壳通道
 * (:data:`EXTRAS_SHELL_PLATFORM_IDS`)同不走通用派生:恒 needs_setup
 * (发送路待 extras,目录/钥匙链证据都不构成「可发送」)。第三参缺省
 * 不传 = 其余平台卡逐字段不变(向后兼容;微信按灰态呈现)。
 */
export function buildPlatformCards(
  directory: Record<string, readonly ChannelEntry[]>,
  secretNames: readonly string[],
  bridgeStatus?: BridgeStatusView | null,
): PlatformCard[] {
  return [
    ...IMPLEMENTED_PLATFORMS.map((platform) => {
      const bucket = directory[platform.id] ?? [];
      const matched = matchSecretNames(
        platform.id,
        platform.guide.keys.map((entry) => entry.key),
        secretNames,
      );
      const isBridge = platform.id === "weixin";
      const isShell = EXTRAS_SHELL_PLATFORM_IDS.has(platform.id);
      return {
        id: platform.id,
        name: platform.name,
        wave: platform.wave,
        status: isBridge
          ? bridgeStatus?.available
            ? ("connected" as const)
            : ("bridge_unavailable" as const)
          : isShell
            ? ("needs_setup" as const)
            : deriveImplementedStatus(bucket, matched),
        directoryCount: bucket.length,
        matchedSecretNames: matched,
        guide: platform.guide,
        description: platform.description,
        discovery: platform.discovery,
        bridge: isBridge ? (bridgeStatus ?? null) : null,
      };
    }),
    ...UPCOMING_PLATFORMS.map((platform) => ({
      id: platform.id,
      name: platform.name,
      wave: platform.wave,
      status: "coming_soon" as const,
      directoryCount: 0,
      matchedSecretNames: [],
      guide: null,
      description: UPCOMING_DESCRIPTION[platform.wave],
      discovery: undefined,
      bridge: null,
    })),
  ];
}

/** 筛选档判定:未启用 = 需要设置(已实装凭据缺失)+ 即将支持(未实装)。 */
export function matchesFilter(card: PlatformCard, filter: PlatformFilter): boolean {
  if (filter === "all") return true;
  if (filter === "connected") return card.status === "connected";
  return card.status !== "connected";
}

// ---------------------------------------------------------------------------
// 展示常量(三态文案与 tone 映射;文案直白中文,tone 走 MYIA 语义 tokens)
// ---------------------------------------------------------------------------

const STATUS_LABEL: Record<PlatformCardStatus, string> = {
  connected: "已连接",
  needs_setup: "需要设置",
  coming_soon: "即将支持",
  bridge_unavailable: "需本机 Hermes",
};

/** 状态点 tone(R3):绿 --ok / 黄 --warning / 灰 --muted-foreground,全走语义 token。
 * 桥接灰态(bridge_unavailable)复用 coming_soon 的 muted 组(D4 同款灰值)。 */
const STATUS_DOT_TONE: Record<PlatformCardStatus, string> = {
  connected: "bg-ok",
  needs_setup: "bg-warning",
  coming_soon: "bg-muted-foreground/50",
  bridge_unavailable: "bg-muted-foreground/50",
};

/** 状态胶囊 tone(R3):与 Badge 语义色变体同源(border/bg/text 三段全 token)。 */
const STATE_PILL_TONE: Record<PlatformCardStatus, string> = {
  connected: "border-ok/30 bg-ok/10 text-ok",
  needs_setup: "border-warning/30 bg-warning/10 text-warning",
  coming_soon: "border-border bg-muted/50 text-muted-foreground",
  bridge_unavailable: "border-border bg-muted/50 text-muted-foreground",
};

/** 左卡描边 tone(R3):已连接绿框 / 需要设置黄框 / 即将支持中性灰框。
 * (终审修整注:VL 指认「描边粗细不一」;messaging-screen.test.tsx 的 AC2
 * 断言锁死三态档位(ok/30、warning/30、border/60),描边档位保持设计,
 * 等高(h-full+items-stretch)与卡距统一由本轮其他修复承担。) */
const CARD_BORDER_TONE: Record<PlatformCardStatus, string> = {
  connected: "border-ok/30",
  needs_setup: "border-warning/30",
  coming_soon: "border-border/60",
  bridge_unavailable: "border-border/60",
};

/** 筛选 tab 激活态 tone(R3):全部=品牌青 / 已连接=绿 / 未启用=黄(可行动子集)。 */
const FILTER_TONE_CLASS: Record<PlatformFilter, string> = {
  all: "border-primary/40 bg-primary/10 text-primary",
  connected: "border-ok/40 bg-ok/10 text-ok",
  disabled: "border-warning/40 bg-warning/10 text-warning",
};

const FILTER_LABEL: Record<PlatformFilter, string> = {
  all: "全部",
  connected: "已连接",
  disabled: "未启用",
};

const FILTER_ORDER: readonly PlatformFilter[] = ["all", "connected", "disabled"];

// ---------------------------------------------------------------------------
// 组件
// ---------------------------------------------------------------------------

interface PlatformOverviewProps {
  /** 与消息屏同款加载态;error 时本区不渲染(ErrorBox 已在屏顶如实报错)。 */
  status: "loading" | "error" | "ready";
  /** channels.list 的 platforms 视图(平台 → 目录桶;详情面板目录速览用)。 */
  directory: Record<string, ChannelEntry[]>;
  /** secret.list 名单(凭据探测;钥匙链不可用时为空 = 降级无证据)。 */
  secretNames: string[];
  /** 死信键清单(`platform:chat_id`;目录速览的死信徽标用)。 */
  dead: string[];
  /** bridge.status 探测(微信卡状态派生;null/缺省 = 灰态「需本机 Hermes」)。 */
  bridgeStatus?: BridgeStatusView | null;
}

/**
 * 平台总览区:筛选 tabs(与状态 tone 呼应)+ 左平台卡网格 / 右详情面板
 * 双栏(R2;窄屏折叠上下布局)。凭据指南唯一入口在右栏详情面板。
 */
export function PlatformOverview({
  bridgeStatus,
  dead,
  directory,
  secretNames,
  status,
}: PlatformOverviewProps) {
  const [filter, setFilter] = useState<PlatformFilter>("all");
  // 缺省选中第一张已实装卡(上游 platformIds[0] 同缺省);详情面板随之就位
  const [selectedId, setSelectedId] = useState<string>(IMPLEMENTED_PLATFORMS[0]?.id ?? "");

  const cards = useMemo(
    () => buildPlatformCards(directory, secretNames, bridgeStatus),
    [directory, secretNames, bridgeStatus],
  );
  const counts = useMemo(() => {
    const connected = cards.filter((card) => card.status === "connected").length;
    return { all: cards.length, connected, disabled: cards.length - connected };
  }, [cards]);
  const visible = useMemo(() => cards.filter((card) => matchesFilter(card, filter)), [cards, filter]);
  // 选中卡从全量卡里找(非 visible):平台状态自行变化离开筛选时,详情栏
  // 保持打开 —— 只有「点击筛选 tab」这一个动作会带动选中切换(上游同交互流)。
  const selected = useMemo(
    () => cards.find((card) => card.id === selectedId) ?? cards[0] ?? null,
    [cards, selectedId],
  );

  function handleFilter(next: PlatformFilter) {
    setFilter(next);
    // 切筛选后若当前选中平台不再匹配,选中栏切入该筛选下第一张卡
    if (selected && !matchesFilter(selected, next)) {
      const first = cards.find((card) => matchesFilter(card, next));
      if (first) {
        setSelectedId(first.id);
      }
    }
  }

  if (status === "error") return null;

  return (
    <div className="px-6" data-testid="platform-overview">
      <Card>
        {/* R2 刀3:卡头层级化(与消息屏其余卡同款 CardTitle/CardDescription) */}
        <CardHeader>
          <CardTitle as="h2">平台总览</CardTitle>
          <CardDescription>
            左列点选平台,右栏看详情:状态说明 / 出站凭据指南 / 目录速览;灰卡平台按波次排期,尚未实装
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">

          {status === "loading" ? (
            <div className="flex flex-col gap-2" aria-label="加载中">
              {[0, 1, 2].map((index) => (
                <Skeleton key={index} className="h-9 w-full" />
              ))}
            </div>
          ) : (
            <>
              <div className="flex flex-wrap items-center gap-1.5" role="group" aria-label="平台筛选">
                {FILTER_ORDER.map((id) => (
                  <Button
                    key={id}
                    size="sm"
                    variant="outline"
                    className={cn(
                      "rounded-full",
                      filter === id ? FILTER_TONE_CLASS[id] : "text-muted-foreground",
                    )}
                    aria-pressed={filter === id}
                    data-testid={`platform-filter-${id}`}
                    onClick={() => handleFilter(id)}
                  >
                    {FILTER_LABEL[id]}({counts[id]})
                  </Button>
                ))}
              </div>

              {/* R2 双栏:左平台卡网格 + 右详情面板;窄屏(<lg)折叠上下布局。
                  终审修整:网格 items-stretch + 卡 h-full(同行等高)+ gap-1.5→2
                  (VL 指认「钉钉/企微明显短于飞书」——auto-fill 行内卡高被内容
                  与对齐方式搅出不齐,显式拉伸钉死) */}
              <div className="grid grid-cols-1 items-start gap-3 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
                <ul
                  className="grid grid-cols-[repeat(auto-fill,minmax(150px,1fr))] items-stretch gap-2"
                  data-testid="platform-card-list"
                  aria-label="平台卡列表"
                >
                  {visible.map((card) => (
                    <li key={card.id}>
                      <PlatformCardButton
                        card={card}
                        selected={selected?.id === card.id}
                        onSelect={() => setSelectedId(card.id)}
                      />
                    </li>
                  ))}
                  {visible.length === 0 ? (
                    <li className="col-span-full text-xs text-muted-foreground">该筛选下暂无平台。</li>
                  ) : null}
                </ul>

                <div
                  className="min-w-0 rounded-md border border-border bg-muted/20 p-4"
                  data-testid="platform-detail"
                  aria-label="平台详情面板"
                >
                  {selected ? (
                    <PlatformDetailPanel card={selected} dead={dead} directory={directory} />
                  ) : (
                    <p className="text-xs text-muted-foreground">暂无平台。</p>
                  )}
                </div>
              </div>
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

/** 左列平台卡(R2):头像 + 名称 + 状态点;点击选中(右栏切换详情)。 */
function PlatformCardButton({
  card,
  selected,
  onSelect,
}: {
  card: PlatformCard;
  selected: boolean;
  onSelect: () => void;
}) {
  return (
    <button
      type="button"
      aria-pressed={selected}
      className={cn(
        "flex h-full w-full items-center gap-2 rounded-md border p-2 text-left transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent/60 hover:text-accent-foreground",
        card.status === "coming_soon" && "opacity-70",
        CARD_BORDER_TONE[card.status],
        // 选中态:品牌青环 + 浅底,叠加在中性描边之上(状态色由状态点承担)
        selected && "bg-primary/10 ring-1 ring-primary/40",
      )}
      data-testid={`platform-card-${card.id}`}
      onClick={onSelect}
    >
      <PlatformAvatar platformId={card.id} platformName={card.name} />
      <span className="min-w-0 flex-1 truncate text-xs font-medium text-foreground">{card.name}</span>
      <StatusDotTone status={card.status} />
    </button>
  );
}

/** 状态点(照上游 StatusDot 画法:1.5px 圆点,tone 全走语义 token)。 */
function StatusDotTone({ status }: { status: PlatformCardStatus }) {
  return (
    <span aria-hidden="true" className={cn("inline-block size-1.5 shrink-0 rounded-full", STATUS_DOT_TONE[status])} />
  );
}

/** 详情栏小节标题(照上游 SectionTitle 节奏:小号大写间距,中文取 tracking-wide)。 */
function SectionTitle({ children }: { children: ReactNode }) {
  return <h4 className="text-2xs font-semibold tracking-wide text-muted-foreground">{children}</h4>;
}

/** 状态说明文案(四态证据来源;连接态列命中信号,缺配置态给下一步动作,
 * 桥接灰态带修复指引——R2「不装可用」的如实披露)。 */
function statusExplanation(card: PlatformCard): string {
  if (card.status === "coming_soon") {
    return `${card.wave} 波次排期平台,尚未实装:无凭据可言,目录恒空;实装节奏见接入路线图。`;
  }
  if (card.bridge) {
    if (card.status === "connected") {
      return "已连接:本机 Hermes 桥接探测通过(CLI 在场 + 微信已扫码登录)。该平台无自动发现:推送对象在规则里写直达 peer id(weixin:xxx@im.wechat),或用别名登记。";
    }
    const cause =
      card.bridge.reason === "weixin_not_configured"
        ? "Hermes 在场但微信未扫码登录"
        : card.bridge.bin_found
          ? "Hermes 微信账号文件缺失"
          : "未找到可用的 Hermes CLI";
    return `需本机 Hermes:微信无官方出站 API,本通道是桥接实现(${cause})。${
      card.bridge.fix_hint ?? "安装 Hermes-Agent 并在其侧扫码登录微信"
    }。修复后回本屏刷新即转绿;无 Hermes 的环境此平台不可用——这是如实披露的边界,不是故障。`;
  }
  if (EXTRAS_SHELL_PLATFORM_IDS.has(card.id)) {
    return "需要设置:该平台是 W3 实装的 extras 壳——寻址已接线,发送路依赖外部服务/CLI(BlueBubbles 服务端、元宝常驻 WS 网关、buzz CLI、photon Node sidecar、Raft CLI),待 extras 实装批次,当前发送会如实报 dependency_missing。MYIA 侧暂无凭据可录(钥匙链恒空是预期,不是缺配置);推送规则可先写直达 id 或别名登记,部署与实装指引见下方「出站凭据指南」。";
  }
  if (card.status === "connected") {
    const signals = [
      card.matchedSecretNames.length > 0 ? `钥匙链命中 ${card.matchedSecretNames.length} 项凭据名` : null,
      card.directoryCount > 0 ? `目录非空(${card.directoryCount} 个会话)` : null,
    ]
      .filter(Boolean)
      .join("、");
    return `已连接:${signals || "信号已就绪"}。${
      card.discovery === "manual"
        ? "该平台无自动发现:推送对象在规则里写直达 id,或用别名登记。"
        : "可直接在下方「推送规则」勾选该平台目录里的会话为推送对象。"
    }`;
  }
  if (card.discovery === "manual") {
    return "需要设置:钥匙链未探测到该平台凭据名,且目录为空。按下方「出站凭据指南」录入凭据;该平台无自动发现(蓝本事实),推送对象在规则里写直达 id(如 ntfy:my-alerts)或用别名文件登记。";
  }
  return "需要设置:钥匙链未探测到该平台凭据名,且目录为空(无一次成功发现或真实 bot 流量的证据)。按下方「出站凭据指南」录入凭据,再到下方「通道目录」点该平台的「刷新」验证。";
}

/** 右栏详情面板(R2):描述 / 状态说明 / 凭据指南 / 已连接时的目录速览。 */
function PlatformDetailPanel({
  card,
  dead,
  directory,
}: {
  card: PlatformCard;
  dead: string[];
  directory: Record<string, ChannelEntry[]>;
}) {
  const bucket = card.status === "coming_soon" ? [] : (directory[card.id] ?? []);
  return (
    <div className="flex flex-col gap-4">
      {/* 头(照上游 PlatformDetail header:头像 + 名称 + 状态胶囊 + 描述) */}
      <header className="flex items-start gap-3">
        <PlatformAvatar platformId={card.id} platformName={card.name} />
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <h3 className="min-w-0 truncate text-base font-semibold tracking-tight text-foreground">
              {card.name}
            </h3>
            <StatePill status={card.status}>{STATUS_LABEL[card.status]}</StatePill>
          </div>
          <p className="mt-1 text-xs leading-relaxed text-muted-foreground">{card.description}</p>
          <p className="truncate font-mono text-2xs text-muted-foreground">{card.id}</p>
        </div>
      </header>

      <section>
        <SectionTitle>状态说明</SectionTitle>
        <p className="mt-1.5 text-xs leading-relaxed text-muted-foreground">{statusExplanation(card)}</p>
      </section>

      {card.guide ? (
        <section className="flex flex-col gap-2">
          <SectionTitle>出站凭据指南</SectionTitle>
          <PlatformGuideView guide={card.guide} platformId={card.id} />
        </section>
      ) : null}

      {card.status === "connected" ? (
        <section className="flex flex-col gap-2">
          <SectionTitle>目录速览</SectionTitle>
          <DirectoryQuickView
            bucket={bucket}
            dead={dead}
            platformId={card.id}
            discovery={card.discovery}
          />
        </section>
      ) : null}
    </div>
  );
}

/** 状态胶囊(照上游 StatePill 画法:胶囊 + 内嵌状态点 + 文案,tone 走语义 token)。 */
function StatePill({ children, status }: { children: string; status: PlatformCardStatus }) {
  return (
    <span
      className={cn(
        "inline-flex shrink-0 items-center gap-1.5 rounded-full border px-2 py-0.5 text-2xs",
        STATE_PILL_TONE[status],
      )}
    >
      <StatusDotTone status={status} />
      {children}
    </span>
  );
}

/** 目录速览(R2;已连接时):只读条目列表;改名/别名/死信处理仍在下方「通道目录」。 */
function DirectoryQuickView({
  bucket,
  dead,
  platformId,
  discovery,
}: {
  bucket: ChannelEntry[];
  dead: string[];
  platformId: string;
  discovery?: PlatformDiscovery;
}) {
  if (bucket.length === 0) {
    if (discovery === "manual") {
      return (
        <p className="text-2xs leading-relaxed text-muted-foreground">
          目录为空:{platformId} 无自动发现(蓝本事实)——推送规则里写直达 id,或手工编辑数据根的
          channel_aliases.json 登记对象(别名文件是本机私有数据)。
        </p>
      );
    }
    return (
      <p className="text-2xs leading-relaxed text-muted-foreground">
        目录为空:到下方「通道目录」点 {platformId} 组的「刷新」(飞书主动发现)或等会话被动进入(telegram 随
        bot 流量积累)。
      </p>
    );
  }
  return (
    <div className="flex flex-col gap-1.5">
      <p className="text-2xs text-muted-foreground">
        {bucket.length} 个会话;只读速览,改名 / 别名 / 死信处理在下方「通道目录」。
      </p>
      <ul className="flex flex-col gap-1">
        {bucket.map((entry) => (
          <li
            key={entry.chat_id}
            className="flex items-center justify-between gap-2 rounded-md border border-border/50 px-2.5 py-1.5"
          >
            <span className="flex min-w-0 items-center gap-1.5 text-xs">
              <Badge variant="outline">{entry.type}</Badge>
              <span className="truncate font-medium text-foreground">{entry.name}</span>
              {isDeadEntry(entry, dead) ? <Badge variant="destructive">死信</Badge> : null}
            </span>
            <span className="shrink-0 font-mono text-2xs text-muted-foreground">{entry.chat_id}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

/** 出站凭据指南面板(R4 内容移入详情栏):凭据 key 用途 + 获取步骤(中文直白)。 */
function PlatformGuideView({ guide, platformId }: { guide: PlatformGuide; platformId: string }) {
  return (
    <div
      className="flex flex-col gap-2 rounded-md bg-muted/30 p-2.5"
      data-testid={`platform-guide-${platformId}`}
    >
      <p className="text-xs font-medium text-foreground">定向推送只需要这些;凭据只覆盖出站,入站项零出现。</p>
      <div className="flex flex-col gap-1">
        {guide.keys.map((entry) => (
          <p key={entry.key} className="text-2xs leading-relaxed text-muted-foreground">
            <span className="font-mono text-foreground">{entry.key}</span> — {entry.purpose}
          </p>
        ))}
      </div>
      <ol className="flex list-decimal flex-col gap-1.5 pl-4 text-2xs leading-relaxed text-muted-foreground">
        {guide.steps.map((step, index) => (
          <li key={index}>
            {typeof step === "string" ? (
              step
            ) : (
              <>
                {step.text}
                <code className="mt-1 block overflow-x-auto rounded bg-background px-2 py-1 font-mono text-2xs whitespace-pre-wrap text-foreground">
                  {step.code}
                </code>
              </>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}
