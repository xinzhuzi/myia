/**
 * 「机器人凭据」独立屏(10-11-bot-credentials-screen:主人令渠道本名制后,
 * 配置组与账号屏并列的机器人面;自设置屏「推送」分区抽出,设置屏原分区摘除)。
 *
 * 裁定语义(与 10-11-platform-account-config 同源):推送机器人凭据(App
 * token/webhook/设备键)= 机器人配置,归本屏;本身账号(个人授权态)归
 * 各账号屏。凭据入钥匙链 myia/push/<ENV_KEY>,运行时 env 缺失自动回退;
 * 通道声明/启停/阈值路由在品类 YAML push: 节(写回走 /yaml-editor)。
 *
 * 结构(自 settings-screen 原样搬迁,零行为漂移):
 *   通道 Select → 预设凭据位表单(逐字段 secret.set,空字段跳过不覆盖)
 *   → 保存推送凭据 + 发送测试(push.test 真发,与真实推送同源解析)
 *   → 自定义凭据位折叠区(scope+名字+值,品类 YAML 手写 keychain: 引用用)
 * 扩通道:PUSH_FIELDS_BY_CHANNEL 按「已实装通道集合」补齐(探查表回填中)。
 */
import { Save, Send } from "lucide-react";
import { useCallback, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { api, type SidecarRequestError } from "@/lib/api";

import { asSidecarError, saveSecret, pushSecretName, validatePushForm } from "../settings/api";
import { ErrorBox } from "../settings/error-box";
import { FieldInput } from "../settings/field-input";
import { SettingRow } from "../settings/settings-row";

// ---------------------------------------------------------------------------
// 通道映射(自 settings-screen.tsx:91-148 原样搬迁;扩通道在探查表回填后补)
// ---------------------------------------------------------------------------

/** 通道 → 规范凭据名缺省(target 语义:feishu 卡的 chat_id / tg 的 bot token / webhook 地址 / bark 的 device key / apprise 的目标串) */
const PUSH_SECRET_NAME_BY_CHANNEL: Record<string, string> = {
  feishu_card: "chat_id",
  telegram: "token",
  webhook: "url",
  // bark(10-05-push-bark):target = device key(在 iPhone Bark App 里复制)
  bark: "device_key",
  // apprise(10-05-push-apprise):target = Apprise 目标串(bark://… 等多目标)
  apprise: "targets",
  // ── 扩通道 target 缺省凭据名(10-11 探查表逐家核实;PUSH_CHANNELS 即此表 keys)──
  ntfy: "NTFY_TARGET",
  dingtalk: "DINGTALK_WEBHOOK_URL",
  wecom: "WECOM_TUSER",
  email: "EMAIL_TO",
  sms: "SMS_TO",
  irc: "IRC_CHANNEL",
  simplex: "SIMPLEX_CHAT",
  whatsapp_cloud: "WHATSAPP_CLOUD_TO",
  google_chat: "GOOGLE_CHAT_WEBHOOK_URL",
  teams: "TEAMS_WEBHOOK_URL",
  matrix: "MATRIX_ROOM_ID",
  slack: "SLACK_CHANNEL",
  discord: "DISCORD_CHANNEL_ID",
  line: "LINE_TO",
  mattermost: "MATTERMOST_CHANNEL_ID",
  homeassistant: "HASS_TARGET",
  qqbot: "QQBOT_TARGET",
  msgraph_webhook: "MSGRAPH_WEBHOOK_CHAT_ID",
  bluebubbles: "BLUEBUBBLES_CHAT",
  signal: "SIGNAL_CHAT",
  a2a: "A2A_PEER",
};
type PushChannel = keyof typeof PUSH_SECRET_NAME_BY_CHANNEL;

/**
 * 通道 → 预设凭据位(10-05-push-credential-journey:填一次即可真收推送)。
 * 键 = 环境变量名(钥匙链规范名 myia/push/<键> 与运行时 env: 回退同口径);
 * password 位只写不回显;optional 位留空不保存(不覆盖已录值)。
 */
const PUSH_FIELDS_BY_CHANNEL: Record<
  PushChannel,
  { key: string; label: string; password?: boolean; optional?: boolean; hint: string }[]
> = {
  feishu_card: [
    { key: "FEISHU_APP_ID", label: "App ID", hint: "飞书开放平台 → 开发者后台 → 应用详情" },
    { key: "FEISHU_APP_SECRET", label: "App Secret", password: true, hint: "同应用详情页;保存后 token 自动续期,无需手工换" },
    { key: "FEISHU_CHAT_ID", label: "群 chat_id", optional: true, hint: "可选;消息屏「刷新」列群目录可查;不填则按规则的推送对象" },
  ],
  telegram: [
    { key: "TELEGRAM_BOT_TOKEN", label: "Bot Token", password: true, hint: "@BotFather 建 bot 后回复的令牌" },
    { key: "TELEGRAM_CHAT_ID", label: "chat_id", optional: true, hint: "可选;给 bot 发条消息后消息屏目录自动记下会话" },
  ],
  webhook: [{ key: "MYIA_WEBHOOK_URL", label: "接收端点 URL", hint: "POST JSON 的接收端(自建服务 / n8n 等)" }],
  // bark(10-05-push-bark):iOS 即时推送;唯一凭据位 = device key
  bark: [
    { key: "BARK_DEVICE_KEY", label: "Device Key", password: true, hint: "在 iPhone 的 Bark App 里复制;凭据保存进系统钥匙串" },
  ],
  // apprise(10-05-push-apprise):统一推送;唯一凭据位 = Apprise 目标串
  apprise: [
    { key: "APPRISE_URL", label: "Apprise 推送目标", password: true, hint: "Apprise 目标地址,如 bark://… 或 pushover://…,逗号或换行分隔多个;凭据保存进系统钥匙串" },
  ],
  // ── 10-11-bot-credentials-screen 扩通道:已实装全通道凭据位(探查表逐家核实;
  //    B 派通道 = 裸 resolve_credential 无钥匙链回退,品类 YAML 引用须写
  //    keychain:myia/push/<键> 才吃到此处保存值 —— 卡底条件提示段如实注明)──
  ntfy: [
    { key: "NTFY_TARGET", label: "topic 完整地址", hint: "{server}/{topic} 形态(如 https://ntfy.sh/myia-alerts);YAML 引用写 keychain:myia/push/NTFY_TARGET" },
    { key: "NTFY_TOKEN", label: "鉴权 Token", password: true, optional: true, hint: "可选;ntfy 服务器开启鉴权时填" },
  ],
  dingtalk: [
    { key: "DINGTALK_WEBHOOK_URL", label: "Webhook URL", password: true, hint: "钉钉群机器人 webhook(内嵌 token,等同密钥)" },
    { key: "DINGTALK_SECRET", label: "加签 Secret", password: true, optional: true, hint: "可选;加签安全设置的 SEC 密钥(经品类 YAML dingtalk_secret: 接线)" },
  ],
  wecom: [
    { key: "WECOM_CORPID", label: "企业 ID(corpid)", hint: "企业微信管理后台 → 我的企业 → 企业信息" },
    { key: "WECOM_CORPSECRET", label: "应用 Secret", password: true, hint: "自建应用的 Secret" },
    { key: "WECOM_AGENTID", label: "AgentId", hint: "自建应用的 AgentId(纯数字)" },
    { key: "WECOM_TUSER", label: "缺省收件 userid", optional: true, hint: "可选;单发缺省收件人,多人管道符分隔" },
  ],
  email: [
    { key: "EMAIL_ADDRESS", label: "发件人地址", hint: "SMTP 账号邮箱" },
    { key: "EMAIL_PASSWORD", label: "授权码", password: true, optional: true, hint: "可选;SMTP 授权码(留空 = 匿名投递合法态)" },
    { key: "EMAIL_SMTP_HOST", label: "SMTP 主机", hint: "如 smtp.gmail.com" },
    { key: "EMAIL_SMTP_PORT", label: "SMTP 端口", optional: true, hint: "可选;留空按安全策略推导 587/465" },
    { key: "EMAIL_SMTP_SECURITY", label: "安全策略", optional: true, hint: "可选;starttls/tls/none" },
    { key: "EMAIL_TO", label: "收件地址", optional: true, hint: "可选;测试与缺省收件人" },
  ],
  sms: [
    { key: "TWILIO_ACCOUNT_SID", label: "Account SID", hint: "Twilio 控制台 Account SID" },
    { key: "TWILIO_AUTH_TOKEN", label: "Auth Token", password: true, hint: "Twilio 控制台 Auth Token" },
    { key: "TWILIO_PHONE_NUMBER", label: "发信号码", hint: "E.164 形态(如 +861…)" },
    { key: "SMS_TO", label: "收件号码", optional: true, hint: "可选;E.164 形态" },
  ],
  irc: [
    { key: "IRC_SERVER", label: "服务器", hint: "irc 服务器地址:端口" },
    { key: "IRC_NICK", label: "昵称", hint: "实际使用 {nick}-push" },
    { key: "IRC_CHANNEL", label: "频道", optional: true, hint: "可选;#频道 或 nick 私信" },
    { key: "IRC_SERVER_PASSWORD", label: "服务器密码", password: true, optional: true, hint: "可选" },
    { key: "IRC_NICKSERV_PASSWORD", label: "NickServ 密码", password: true, optional: true, hint: "可选" },
  ],
  simplex: [
    { key: "SIMPLEX_WS_URL", label: "smp 服务地址", optional: true, hint: "可选;缺省 ws://127.0.0.1:5225;需装 myssia[simplex]" },
    { key: "SIMPLEX_CHAT", label: "会话", optional: true, hint: "可选;group:id 或 DM 名" },
  ],
  whatsapp_cloud: [
    { key: "WHATSAPP_CLOUD_TOKEN", label: "永久令牌", password: true, hint: "Meta 开发者后台永久访问令牌" },
    { key: "WHATSAPP_CLOUD_PHONE_NUMBER_ID", label: "号码 ID", hint: "Meta 开发者后台电话号码 ID" },
    { key: "WHATSAPP_CLOUD_TO", label: "收件号码", optional: true, hint: "可选;E.164 形态" },
  ],
  google_chat: [
    { key: "GOOGLE_CHAT_WEBHOOK_URL", label: "Webhook URL", password: true, hint: "Google Chat 群空间 Incoming Webhook(内嵌 key,等同密钥)" },
  ],
  teams: [
    { key: "TEAMS_WEBHOOK_URL", label: "Webhook URL", password: true, hint: "Teams 频道 Incoming Webhook(内嵌凭据,等同密钥)" },
  ],
  matrix: [
    { key: "MATRIX_HOMESERVER", label: "Homeserver 基址", hint: "如 https://matrix.org" },
    { key: "MATRIX_ACCESS_TOKEN", label: "Access Token", password: true, hint: "Bearer 令牌(客户端设置页取)" },
    { key: "MATRIX_ROOM_ID", label: "房间 ID", optional: true, hint: "可选;!id: 或 #alias: 形态" },
  ],
  slack: [
    { key: "SLACK_BOT_TOKEN", label: "Bot Token", password: true, hint: "xoxb- 开头(OAuth & Permissions)" },
    { key: "SLACK_CHANNEL", label: "频道 ID", optional: true, hint: "可选;C/G/D/U/W 开头 id" },
  ],
  discord: [
    { key: "DISCORD_BOT_TOKEN", label: "Bot Token", password: true, hint: "Discord 开发者门户 → Bot 页" },
    { key: "DISCORD_CHANNEL_ID", label: "频道 ID", optional: true, hint: "可选;snowflake id(开发者模式复制)" },
  ],
  line: [
    { key: "LINE_CHANNEL_ACCESS_TOKEN", label: "Channel Access Token", password: true, hint: "LINE Developers 控制台长寿命 token" },
    { key: "LINE_TO", label: "收件 ID", optional: true, hint: "可选;U/C/R 开头 id" },
  ],
  mattermost: [
    { key: "MATTERMOST_TOKEN", label: "Bot Token", password: true, hint: "Bearer 令牌(REST 直发;webhook 退路可免)" },
    { key: "MATTERMOST_SERVER", label: "服务器地址", hint: "REST 直发必填(如 https://mm.example.com)" },
    { key: "MATTERMOST_CHANNEL_ID", label: "频道 ID", optional: true, hint: "可选;26 位 id 或整条 webhook URL" },
  ],
  homeassistant: [
    { key: "HASS_URL", label: "实例基址", hint: "如 http://homeassistant.local:8123" },
    { key: "HASS_TOKEN", label: "长期令牌", password: true, hint: "用户页 → 安全 → 长期访问令牌" },
    { key: "HASS_TARGET", label: "notify 目标", optional: true, hint: "可选;notify 服务目标名" },
  ],
  qqbot: [
    { key: "QQBOT_APP_ID", label: "AppID", hint: "QQ 开放平台(qq.com)机器人 AppID —— 官方机器人身份,非个人 QQ 号" },
    { key: "QQBOT_CLIENT_SECRET", label: "Client Secret", password: true, hint: "机器人密钥;成对换 access_token(自动续期)" },
    { key: "QQBOT_TARGET", label: "推送对象", optional: true, hint: "可选;group:/c2c:/guild: 前缀 + openid(群聊主动消息每月限 4 条/群)" },
  ],
  msgraph_webhook: [
    { key: "MSGRAPH_WEBHOOK_TENANT_ID", label: "租户 ID", hint: "Azure AD 租户 id" },
    { key: "MSGRAPH_WEBHOOK_CLIENT_ID", label: "应用(客户端)ID", hint: "Azure AD 应用注册 id" },
    { key: "MSGRAPH_WEBHOOK_CLIENT_SECRET", label: "客户端密码", password: true, hint: "应用注册的证书与密码 → 客户端密码值" },
    { key: "MSGRAPH_WEBHOOK_CHAT_ID", label: "chat_id", optional: true, hint: "可选;19: 前缀 Teams 群会话 id" },
  ],
  bluebubbles: [
    { key: "BLUEBUBBLES_SERVER_URL", label: "服务端地址", hint: "BlueBubbles Server 地址(iMessage 桥)" },
    { key: "BLUEBUBBLES_PASSWORD", label: "API 密码", password: true, hint: "BlueBubbles Server 设置页密码" },
    { key: "BLUEBUBBLES_CHAT", label: "会话", optional: true, hint: "可选;GUID / +手机号 / 邮箱" },
  ],
  signal: [
    { key: "SIGNAL_HTTP_URL", label: "守护进程地址", hint: "signal-cli-rest-api 地址" },
    { key: "SIGNAL_ACCOUNT", label: "发送账号", hint: "E.164 形态发信号码" },
    { key: "SIGNAL_CHAT", label: "会话", optional: true, hint: "可选;群组 id 或号码" },
  ],
  a2a: [
    { key: "A2A_PEER", label: "对端基址", hint: "A2A 对端 URL" },
    { key: "A2A_TOKEN", label: "Bearer Token", password: true, optional: true, hint: "可选;留空 = 无鉴权合法态" },
  ],
};

/** 通道 → 「发送测试」的目标凭据键(push.test target = keychain:myia/push/<键>) */
const PUSH_TEST_TARGET_KEY: Record<PushChannel, string> = {
  feishu_card: "FEISHU_CHAT_ID",
  telegram: "TELEGRAM_CHAT_ID",
  webhook: "MYIA_WEBHOOK_URL",
  bark: "BARK_DEVICE_KEY",
  apprise: "APPRISE_URL",
  ntfy: "NTFY_TARGET",
  dingtalk: "DINGTALK_WEBHOOK_URL",
  wecom: "WECOM_TUSER",
  email: "EMAIL_TO",
  sms: "SMS_TO",
  irc: "IRC_CHANNEL",
  simplex: "SIMPLEX_CHAT",
  whatsapp_cloud: "WHATSAPP_CLOUD_TO",
  google_chat: "GOOGLE_CHAT_WEBHOOK_URL",
  teams: "TEAMS_WEBHOOK_URL",
  matrix: "MATRIX_ROOM_ID",
  slack: "SLACK_CHANNEL",
  discord: "DISCORD_CHANNEL_ID",
  line: "LINE_TO",
  mattermost: "MATTERMOST_CHANNEL_ID",
  homeassistant: "HASS_TARGET",
  qqbot: "QQBOT_TARGET",
  msgraph_webhook: "MSGRAPH_WEBHOOK_CHAT_ID",
  bluebubbles: "BLUEBUBBLES_CHAT",
  signal: "SIGNAL_CHAT",
  a2a: "A2A_PEER",
};
/** 通道 → 下拉显示名(既有 5 通道 = 原名零漂移;扩通道带人话标注) */
const PUSH_CHANNEL_LABELS: Record<PushChannel, string> = {
  feishu_card: "feishu_card(飞书)",
  telegram: "telegram",
  webhook: "webhook",
  bark: "Bark(iOS 推送)",
  apprise: "Apprise(统一推送)",
  ntfy: "ntfy",
  dingtalk: "钉钉机器人",
  wecom: "企业微信",
  email: "Email(SMTP)",
  sms: "SMS(Twilio)",
  irc: "IRC",
  simplex: "SimpleX",
  whatsapp_cloud: "WhatsApp Cloud",
  google_chat: "Google Chat",
  teams: "Microsoft Teams",
  matrix: "Matrix",
  slack: "Slack",
  discord: "Discord",
  line: "LINE",
  mattermost: "Mattermost",
  homeassistant: "Home Assistant",
  qqbot: "QQ 机器人(官方)",
  msgraph_webhook: "MS Graph Webhook",
  bluebubbles: "BlueBubbles(iMessage)",
  signal: "Signal",
  a2a: "A2A 对端",
};
const PUSH_CHANNELS = Object.keys(PUSH_SECRET_NAME_BY_CHANNEL) as PushChannel[];

/**
 * B 派通道(裸 resolve_credential,无 myia/push/<键> 钥匙链回退;10-11 探查
 * 逐家核实):表单保存的值要吃到真实推送,品类 YAML 的凭据引用须写
 * ``keychain:myia/push/<键>`` 形态(发送测试按钮传显式 keychain: 引用,
 * 可直接验连通)。A 派(signal/bluebubbles 及原 5 通道)env 缺失自动回退,
 * 无此注意。 */
const KEYCHAIN_REF_REQUIRED_CHANNELS = new Set<PushChannel>([
  "ntfy", "dingtalk", "wecom", "email", "sms", "irc", "simplex", "whatsapp_cloud",
  "google_chat", "teams", "matrix", "slack", "discord", "line", "mattermost",
  "homeassistant", "qqbot", "msgraph_webhook", "a2a",
]);

interface PushForm {
  channel: PushChannel;
  scope: string;
  secretName: string;
  value: string;
}

/**
 * 每卡保存态(D4「每区保存态反馈」;自 settings-screen 原样搬迁)。
 * nextStep(push-last-mile ⑤):保存成功后的「下一步」引导行(含锚点),
 * A 派指消息屏勾对象、B 派先去 YAML配置 贴引用再去消息屏。
 */
type CardSaveState =
  | { kind: "saving" }
  | { kind: "saved"; names: string[]; note: string | null; nextStep?: React.ReactNode }
  | { kind: "note"; note: string }
  | { kind: "error"; error: SidecarRequestError };

/** 复制 keychain 引用(push-last-mile ④):clipboard 尽力而为——不可用/
 *  权限拒 = 静默(feed 屏 copyLink 同款,轻动作不打断表单)。 */
function copyKeychainRef(ref: string): void {
  try {
    void navigator.clipboard?.writeText(ref)?.catch(() => {});
  } catch {
    // 老 webview 无剪贴板 API:静默
  }
}

/** 卡片底部保存条:状态反馈在左、保存动作在右(拆解表第 5 条输入类的显式保存) */
function CardSaveBar({
  state,
  savingLabel,
  action,
}: {
  state: CardSaveState | null;
  savingLabel: string;
  action: React.ReactNode;
}) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2 border-t border-border/60 pt-3">
      <div className="min-w-0 flex-1">
        {state?.kind === "saving" ? (
          <span role="status" className="text-xs text-muted-foreground">
            {savingLabel}
          </span>
        ) : null}
        {state?.kind === "saved" ? (
          <div role="status" data-testid="save-status" className="text-xs text-ok">
            已写入钥匙串:{state.names.join("、")}(值不回显)
            {state.note ? <span className="mt-0.5 block text-2xs text-muted-foreground">{state.note}</span> : null}
            {state.nextStep ? (
              <span data-testid="save-next-step" className="mt-0.5 block text-2xs text-muted-foreground">
                {state.nextStep}
              </span>
            ) : null}
          </div>
        ) : null}
        {state?.kind === "note" ? (
          <p role="note" data-testid="save-note" className="text-xs text-muted-foreground">
            {state.note}
          </p>
        ) : null}
        {state?.kind === "error" ? <ErrorBox error={state.error} /> : null}
      </div>
      {action}
    </div>
  );
}

export function BotCredentialsScreen() {
  const [push, setPush] = useState<PushForm>({ channel: "feishu_card", scope: "", secretName: "chat_id", value: "" });
  const [pushErrors, setPushErrors] = useState<Partial<Record<"scope" | "secretName" | "value", string>>>({});
  /** 预设凭据位值(10-05-push-credential-journey):{ENV_KEY: 值},按通道字段集读写 */
  const [pushValues, setPushValues] = useState<Record<string, string>>({});
  const [pushSave, setPushSave] = useState<CardSaveState | null>(null);
  const [pushTesting, setPushTesting] = useState(false);
  const [pushTestNote, setPushTestNote] = useState<string | null>(null);
  const [pushTestOk, setPushTestOk] = useState<boolean | null>(null);

  const handlePushSave = useCallback(async () => {
    const formError = validatePushForm(push);
    if (formError === "scope_invalid") {
      setPushErrors({ scope: "scope 须为品类 id 规则:小写字母/数字开头,可含连字符" });
      return;
    }
    if (formError === "name_invalid") {
      setPushErrors({ secretName: "凭据名段须为字母/数字开头,可含点/连字符/下划线" });
      return;
    }
    if (formError === "value_empty") {
      setPushErrors({ value: "凭据值必填" });
      return;
    }
    setPushErrors({});
    setPushSave({ kind: "saving" });
    try {
      const record = await saveSecret(pushSecretName(push.scope.trim(), push.secretName.trim()), push.value);
      setPushSave({
        kind: "saved",
        names: [record.name],
        note: "通道凭据已入钥匙串;品类 YAML push[].target 侧以 keychain:myia/<scope>/<name> 引用(通道声明写回属协议缺口)。",
      });
      setPush((prev) => ({ ...prev, value: "" }));
    } catch (error) {
      setPushSave({ kind: "error", error: asSidecarError(error) });
    }
  }, [push]);

  /** push.test 真发一条测试消息(channel 取表单当前选中;scope 已填则 target
   *  引用 keychain:myia/<scope>/<secretName>,缺省走通道默认 env 引用链)。 */
  const handlePushTest = useCallback(
    async (explicitTarget?: string) => {
      setPushTesting(true);
      setPushTestNote(null);
      setPushTestOk(null);
      let target = explicitTarget;
      if (!target) {
        const scope = push.scope.trim();
        const name = push.secretName.trim() || PUSH_SECRET_NAME_BY_CHANNEL[push.channel] || "";
        target = scope && name ? `keychain:myia/${scope}/${name}` : undefined;
      }
      try {
        const result = await api.pushTest({ channel: push.channel, ...(target ? { target } : {}) });
        setPushTestOk(true);
        setPushTestNote(
          result.preview
            ? `测试消息已发(stdout 通道预览):${result.preview.slice(0, 200)}`
            : `测试消息已发(${result.channel})——请到对应客户端查收。`,
        );
      } catch (error) {
        const failure = asSidecarError(error);
        setPushTestOk(false);
        setPushTestNote(`发送失败(${failure.code}):${failure.message}`);
      } finally {
        setPushTesting(false);
      }
    },
    [push.channel, push.scope, push.secretName],
  );

  /** 预设凭据位保存:逐非空字段写 myia/push/<ENV_KEY>;空字段跳过不覆盖
   *  (清除走设置危险区 secret.delete)。 */
  const handlePresetSave = useCallback(async () => {
    const fields = PUSH_FIELDS_BY_CHANNEL[push.channel];
    const entries = fields
      .map((field) => ({ field, value: (pushValues[field.key] ?? "").trim() }))
      .filter((entry) => entry.value !== "");
    if (entries.length === 0) {
      setPushSave({ kind: "note", note: "至少填一个字段再保存;留空的字段不会覆盖已录入的值。" });
      return;
    }
    setPushSave({ kind: "saving" });
    try {
      const names: string[] = [];
      for (const entry of entries) {
        const record = await saveSecret(`myia/push/${entry.field.key}`, entry.value);
        names.push(record.name);
      }
      // push-last-mile ③⑤:保存成功反馈按 A/B 派分流——A 派 env 缺失自动回退,
      // 引导直接去消息屏勾对象;B 派无钥匙链回退,note 指向上方常驻逐键引用
      // 清单,下一步先去 YAML配置 贴 keychain: 引用再去消息屏(普通锚点跳屏)。
      const needsKeychainRef = KEYCHAIN_REF_REQUIRED_CHANNELS.has(push.channel);
      setPushSave({
        kind: "saved",
        names,
        note: needsKeychainRef
          ? "已入钥匙串;真实推送要品类 YAML 写 keychain:myia/push/<键> 引用(见上方引用清单),可先点「发送测试」验连通。"
          : "已入钥匙串;运行时 env 缺失会自动用这些值(发送测试与真实推送同源)。",
        nextStep: needsKeychainRef ? (
          <>
            下一步:去
            <a href="#/yaml-editor" className="underline underline-offset-2 hover:text-foreground">
              YAML配置
            </a>
            贴 keychain: 引用,再去
            <a href="#/messaging" className="underline underline-offset-2 hover:text-foreground">
              消息屏
            </a>
            勾对象。
          </>
        ) : (
          <>
            下一步:去
            <a href="#/messaging" className="underline underline-offset-2 hover:text-foreground">
              消息屏
            </a>
            勾推送对象(飞书先点刷新,Telegram 先给机器人发条消息)。
          </>
        ),
      });
      setPushValues({});
    } catch (error) {
      setPushSave({ kind: "error", error: asSidecarError(error) });
    }
  }, [push.channel, pushValues]);

  return (
    <div className="flex flex-col gap-block pb-block">
      <div className="px-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Send className="size-4 text-muted-foreground" />
              机器人凭据
            </CardTitle>
            <CardDescription>
              按通道填一次凭据(入钥匙串 myia/push/*);「发送测试」与真实推送同源;通道启停与阈值路由在品类
              YAML push: 节。部分通道(下拉选项带标注)不走钥匙串回退:品类 YAML 的凭据引用须写 keychain: 形态,详见该通道内提示
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-1">
            <div className="divide-y divide-border/60">
              <SettingRow label="通道" description="通道启停与阈值路由在品类 YAML push: 节">
                <Select
                  value={push.channel}
                  onValueChange={(channel) =>
                    setPush((prev) => ({
                      ...prev,
                      channel: channel as PushChannel,
                      secretName: PUSH_SECRET_NAME_BY_CHANNEL[channel] ?? prev.secretName,
                    }))
                  }
                >
                  <SelectTrigger aria-label="推送通道" className="w-64 min-w-0 flex-1 sm:flex-none">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {PUSH_CHANNELS.map((channel) => (
                      <SelectItem key={channel} value={channel}>
                        {PUSH_CHANNEL_LABELS[channel]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </SettingRow>
              {PUSH_FIELDS_BY_CHANNEL[push.channel].map((field) => (
                <FieldInput
                  key={field.key}
                  label={field.label}
                  aria-label={`${push.channel} ${field.label}`}
                  type={field.password ? "password" : "text"}
                  autoComplete="new-password"
                  placeholder={`写入 myia/push/${field.key};永不回显`}
                  value={pushValues[field.key] ?? ""}
                  onChange={(event) =>
                    setPushValues((prev) => ({ ...prev, [field.key]: event.target.value }))
                  }
                  hint={field.hint}
                />
              ))}
              {push.channel === "bark" ? (
                // bark 端点非凭据(不进钥匙链),引导写在品类 YAML;10-05-push-bark
                <p data-testid="bark-endpoint-hint" className="px-1 pb-1 text-2xs text-muted-foreground">
                  推送端点 bark_endpoint:留空 = 官方服务(api.day.app);自建 bark-server
                  填主机地址(如 http://192.168.1.10:8080)——写在品类 YAML push: 节
                </p>
              ) : null}
              {push.channel === "apprise" ? (
                // apprise 目标走凭据引用,值为目标串;10-05-push-apprise
                <p data-testid="apprise-target-hint" className="px-1 pb-1 text-2xs text-muted-foreground">
                  目标走 env:/keychain: 引用,值为 Apprise 目标串(bark://…、pushover://…
                  可逗号分隔多个);需装可选依赖(pip install "myssia[apprise]" 或
                  uv sync --extra apprise),未装时发送会明确报错、不影响其他通道
                </p>
              ) : null}
              {KEYCHAIN_REF_REQUIRED_CHANNELS.has(push.channel) ? (
                // B 派通道(裸 resolve_credential):无钥匙链回退,常驻逐键引用
                // 清单(push-last-mile ④)——遍历该通道全部凭据键,品类 YAML 照
                // 抄即可;展示源是 PUSH_FIELDS_BY_CHANNEL(非测试目标键)。
                <div className="flex flex-col gap-1 px-1 pb-1">
                  <p data-testid="keychain-ref-hint" className="text-2xs text-muted-foreground">
                    注意:本通道凭据解析不走钥匙串回退——真实推送要品类 YAML 按下面的清单写
                    <code className="mx-1 font-mono">keychain:myia/push/&lt;键&gt;</code>
                    引用,此处保存的值即生效;「发送测试」传的就是该引用,可直接验连通。
                  </p>
                  <ul data-testid="keychain-ref-list" className="flex flex-col gap-1">
                    {PUSH_FIELDS_BY_CHANNEL[push.channel].map((field) => (
                      <li
                        key={field.key}
                        data-testid={`keychain-ref-row-${field.key}`}
                        className="flex min-w-0 items-center gap-2 text-2xs text-muted-foreground"
                      >
                        <span className="shrink-0">{field.label} →</span>
                        <code className="min-w-0 truncate font-mono">keychain:myia/push/{field.key}</code>
                        <button
                          type="button"
                          aria-label={`复制 ${field.label} 引用`}
                          data-testid={`keychain-ref-copy-${field.key}`}
                          className="shrink-0 rounded-md border border-border/60 px-1.5 py-0.5 transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent/60 hover:text-foreground"
                          onClick={() => copyKeychainRef(`keychain:myia/push/${field.key}`)}
                        >
                          复制
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : null}
            </div>
            <CardSaveBar
              state={pushSave}
              savingLabel="保存中…"
              action={
                <div className="flex flex-wrap items-center gap-2">
                  <Button
                    size="sm"
                    onClick={() => void handlePresetSave()}
                    disabled={pushSave?.kind === "saving" || pushTesting}
                  >
                    <Save className="size-3.5" />
                    保存推送凭据
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() =>
                      void handlePushTest(`keychain:myia/push/${PUSH_TEST_TARGET_KEY[push.channel]}`)
                    }
                    disabled={pushTesting}
                    title="真发一条测试消息:发到该通道预设凭据,与真实推送走同一解析"
                  >
                    <Send className={pushTesting ? "size-3.5 animate-pulse" : "size-3.5"} />
                    {pushTesting ? "发送中…" : "发送测试"}
                  </Button>
                  {pushTestOk === true ? <Badge variant="ok">通道连通</Badge> : null}
                  {pushTestOk === false ? <Badge variant="destructive">通道失败</Badge> : null}
                </div>
              }
            />
            {pushTestNote ? (
              <p
                role={pushTestOk === false ? "alert" : "status"}
                data-testid="push-test-result"
                className={pushTestOk === false ? "text-xs text-destructive" : "text-xs text-muted-foreground"}
              >
                {pushTestNote}
              </p>
            ) : null}
            <details className="border-t border-border/60 pt-2 text-2xs text-muted-foreground">
              <summary className="cursor-pointer select-none">
                自定义凭据(高级:品类 YAML 手写 keychain: 引用时才用;日常接入填上方预设字段即可)
              </summary>
              <div className="mt-2 flex flex-col gap-2">
                <FieldInput
                  label="品类 scope"
                  aria-label="品类 scope"
                  placeholder="stocks"
                  value={push.scope}
                  onChange={(event) => setPush((prev) => ({ ...prev, scope: event.target.value }))}
                  error={pushErrors.scope}
                  hint="凭据引用键段:myia/<scope>/<凭据名>"
                />
                <FieldInput
                  label="凭据名段"
                  aria-label="推送凭据名"
                  placeholder={PUSH_SECRET_NAME_BY_CHANNEL[push.channel]}
                  value={push.secretName}
                  onChange={(event) => setPush((prev) => ({ ...prev, secretName: event.target.value }))}
                  error={pushErrors.secretName}
                  hint="通道目标凭据名(feishu 卡 chat_id / tg token / webhook url / bark device_key / apprise targets)"
                />
                <FieldInput
                  label="凭据值"
                  aria-label="推送凭据值"
                  type="password"
                  autoComplete="new-password"
                  placeholder="写入 myia/<scope>/<name>;永不回显"
                  value={push.value}
                  onChange={(event) => setPush((prev) => ({ ...prev, value: event.target.value }))}
                  error={pushErrors.value}
                />
                <div>
                  <Button size="sm" variant="outline" onClick={() => void handlePushSave()}>
                    <Save className="size-3.5" />
                    保存自定义凭据位
                  </Button>
                </div>
              </div>
            </details>
            <div className="flex flex-wrap items-center gap-1.5 border-t border-border/60 pt-2 text-2xs text-muted-foreground">
              <span>推送通道声明(push: 节)与阈值路由在品类 YAML:</span>
              {/* HashRouter 路由:普通锚点即可跳YAML配置屏,不引 Router context 依赖 */}
              <a href="#/yaml-editor" className="underline underline-offset-2 hover:text-foreground">
                去YAML配置改 push 声明
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
