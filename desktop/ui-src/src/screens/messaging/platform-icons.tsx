/**
 * 平台头像(task 10-03-messaging-hermes-look R1)—— 平台身份芯片,画法照上游
 * Hermes 蓝本(~/.hermes/hermes-agent/apps/desktop/src/app/messaging/platform-icon.tsx
 * + components/ui/avatar-chip.tsx)在 MYIA 栈内重排:
 *
 * PlatformAvatar = 24px 方形芯片(size-6 + rounded-md + place-items-center):
 *  - kind="brand" 精确标:品牌色 16% tint 底(color-mix)+ 原生品牌色画字形,
 *    字形约 14px(size-[58%],24px 芯片内——上游 GLYPH_CLASS 同比例);
 *  - kind="brand" + monogram:品牌方未发布可用简化标(Simple Icons 已按品牌方
 *    要求移除飞书)→ 品牌色底上画官方字形——飞书官方标本身就是「飞」字符,
 *    与上游对 Slack 的 monogram 处理同一范式;
 *  - kind="generic" 通用标:无官方品牌标可用的平台用 lucide 通用图标——已实装
 *    但无品牌标(email/sms/irc/simplex + a2a/buzz/raft 等,W3 转实装)全灰
 *    bg-muted;未实装 W3 再弱一档 bg-muted/50(波次由 wave 字段区分,W2 未
 *    实装已清零)。
 *
 * 图标即数据(定调:SVG 路径数据直接采用):Telegram 字形逐字符采用
 * Simple Icons 官方字形(采集自 @icons-pack/react-simple-icons 13.11.1 的
 * SiTelegram.mjs,viewBox 0 0 24 24 / fill currentColor / 品牌色 #26A5E4),
 * 不引第三方图标包——依赖红线;飞书品牌蓝 #3370FF 为开放平台官方主色。
 * 状态三色(绿/黄/灰)不在此文件——那走 MYIA 语义 tokens(platform-overview
 * 的 StatePill),品牌色与状态色两套语言互不混用(与上游一致)。
 */
import { Bot, Mail, MessageSquareText, Webhook } from "lucide-react";
import type { ComponentType, SVGProps } from "react";

import { cn } from "@/lib/utils";

// ---------------------------------------------------------------------------
// 精确官方标(SVG 路径数据直接采用;图标是数据,一字符未改)
// ---------------------------------------------------------------------------

/** Simple Icons「Telegram」官方字形(fill=currentColor,24×24;路径数据直接采用)。 */
function TelegramGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
    </svg>
  );
}

/** Simple Icons「ntfy」官方字形(fill=currentColor,24×24;路径数据直接采用,
 * 采集自 simple-icons develop 分支 icons/ntfy.svg——依赖红线,不引图标包)。 */
function NtfyGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M12.597 13.693v2.156h6.205v-2.156ZM5.183 6.549v2.363l3.591 1.901.023.01-.023.009-3.591 1.901v2.35l.386-.211 5.456-2.969V9.729ZM3.659 2.037C1.915 2.037.42 3.41.42 5.154v.002L.438 18.73 0 21.963l5.956-1.583h14.806c1.744 0 3.238-1.374 3.238-3.118V5.154c0-1.744-1.493-3.116-3.237-3.117h-.001zm0 2.2h17.104c.613.001 1.037.447 1.037.917v12.108c0 .47-.424.916-1.038.916H5.633l-3.026.915.031-.179-.017-13.76c0-.47.424-.917 1.038-.917z" />
    </svg>
  );
}

/** Simple Icons「WhatsApp」官方字形(fill=currentColor,24×24;路径数据直接
 * 采用,采集自 simple-icons develop 分支 icons/whatsapp.svg——依赖红线,
 * 不引图标包)。 */
function WhatsAppGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
    </svg>
  );
}

/** Simple Icons「Matrix」官方字形(fill=currentColor,24×24;路径数据直接
 * 采用,采集自 simple-icons develop 分支 icons/matrix.svg——依赖红线,
 * 不引图标包)。 */
function MatrixGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M.632.55v22.9H2.28V24H0V0h2.28v.55zm7.043 7.26v1.157h.033c.309-.443.683-.784 1.117-1.024.433-.245.936-.365 1.5-.365.54 0 1.033.107 1.481.314.448.208.785.582 1.02 1.108.254-.374.6-.706 1.034-.992.434-.287.95-.43 1.546-.43.453 0 .872.056 1.26.167.388.11.716.286.993.53.276.245.489.559.646.951.152.392.23.863.23 1.417v5.728h-2.349V11.52c0-.286-.01-.559-.032-.812a1.755 1.755 0 0 0-.18-.66 1.106 1.106 0 0 0-.438-.448c-.194-.11-.457-.166-.785-.166-.332 0-.6.064-.803.189a1.38 1.38 0 0 0-.48.499 1.946 1.946 0 0 0-.231.696 5.56 5.56 0 0 0-.06.785v4.768h-2.35v-4.8c0-.254-.004-.503-.018-.752a2.074 2.074 0 0 0-.143-.688 1.052 1.052 0 0 0-.415-.503c-.194-.125-.476-.19-.854-.19-.111 0-.259.024-.439.074-.18.051-.36.143-.53.282-.171.138-.319.337-.439.595-.12.259-.18.6-.18 1.02v4.966H5.46V7.81zm15.693 15.64V.55H21.72V0H24v24h-2.28v-.55z" />
    </svg>
  );
}

/** Simple Icons「Google Chat」官方字形(fill=currentColor,24×24;路径数据
 * 直接采用,采集自 simple-icons develop 分支 icons/googlechat.svg——依赖
 * 红线,不引图标包)。 */
function GoogleChatGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M1.637 0C.733 0 0 .733 0 1.637v16.5c0 .904.733 1.636 1.637 1.636h3.955v3.323c0 .804.97 1.207 1.539.638l3.963-3.96h11.27c.903 0 1.636-.733 1.636-1.637V5.592L18.408 0Zm3.955 5.592h12.816v8.59H8.455l-2.863 2.863Z" />
    </svg>
  );
}

/** Simple Icons「Discord」官方字形(fill=currentColor,24×24;路径数据直接
 * 采用,采集自 simple-icons develop 分支 icons/discord.svg——依赖红线,
 * 不引图标包)。 */
function DiscordGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189Z" />
    </svg>
  );
}

/** Simple Icons「LINE」官方字形(fill=currentColor,24×24;路径数据直接
 * 采用,采集自 simple-icons develop 分支 icons/line.svg——依赖红线,
 * 不引图标包)。 */
function LineGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M19.365 9.863c.349 0 .63.285.63.631 0 .345-.281.63-.63.63H17.61v1.125h1.755c.349 0 .63.283.63.63 0 .344-.281.629-.63.629h-2.386c-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63h2.386c.346 0 .627.285.627.63 0 .349-.281.63-.63.63H17.61v1.125h1.755zm-3.855 3.016c0 .27-.174.51-.432.596-.064.021-.133.031-.199.031-.211 0-.391-.09-.51-.25l-2.443-3.317v2.94c0 .344-.279.629-.631.629-.346 0-.626-.285-.626-.629V8.108c0-.27.173-.51.43-.595.06-.023.136-.033.194-.033.195 0 .375.104.495.254l2.462 3.33V8.108c0-.345.282-.63.63-.63.345 0 .63.285.63.63v4.771zm-5.741 0c0 .344-.282.629-.631.629-.345 0-.627-.285-.627-.629V8.108c0-.345.282-.63.63-.63.346 0 .628.285.628.63v4.771zm-2.466.629H4.917c-.345 0-.63-.285-.63-.629V8.108c0-.345.285-.63.63-.63.348 0 .63.285.63.63v4.141h1.756c.348 0 .629.283.629.63 0 .344-.282.629-.629.629M24 10.314C24 4.943 18.615.572 12 .572S0 4.943 0 10.314c0 4.811 4.27 8.842 10.035 9.608.391.082.923.258 1.058.59.12.301.079.766.038 1.08l-.164 1.02c-.045.301-.24 1.186 1.049.645 1.291-.539 6.916-4.078 9.436-6.975C23.176 14.393 24 12.458 24 10.314" />
    </svg>
  );
}

/** Simple Icons「Mattermost」官方字形(fill=currentColor,24×24;路径数据
 * 直接采用,采集自 simple-icons develop 分支 icons/mattermost.svg——依赖
 * 红线,不引图标包)。 */
function MattermostGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M12.081 0C7.048-.034 2.339 3.125.637 8.153c-2.125 6.276 1.24 13.086 7.516 15.21 6.276 2.125 13.086-1.24 15.21-7.516 1.727-5.1-.172-10.552-4.311-13.557l.126 2.547c2.065 2.282 2.88 5.512 1.852 8.549-1.534 4.532-6.594 6.915-11.3 5.321-4.708-1.593-7.28-6.559-5.745-11.092 1.031-3.046 3.655-5.121 6.694-5.67l1.642-1.94A4.87 4.87 0 0 0 12.08 0zm3.528 1.094a.284.284 0 0 0-.123.024l-.004.001a.33.33 0 0 0-.109.071c-.145.142-.657.828-.657.828L13.6 3.4l-1.3 1.585-2.232 2.776s-1.024 1.278-.798 2.851c.226 1.574 1.396 2.34 2.304 2.648.907.307 2.302.408 3.438-.704 1.135-1.112 1.098-2.75 1.098-2.75l-.087-3.56-.07-2.05-.047-1.775s.01-.856-.02-1.057a.33.33 0 0 0-.035-.107l-.006-.012-.007-.011a.277.277 0 0 0-.229-.14z" />
    </svg>
  );
}

/** Simple Icons「Home Assistant」官方屋形标(fill=currentColor,24×24;路径
 * 数据直接采用,采集自 simple-icons 13.21.0 icons/homeassistant.svg,品牌色
 * 数据同源 #18BCF2(hex 元数据源 home-assistant/assets 官方仓库)——依赖
 * 红线,不引图标包)。 */
function HomeAssistantGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <path d="M22.939 10.627 13.061.749a1.505 1.505 0 0 0-2.121 0l-9.879 9.878C.478 11.21 0 12.363 0 13.187v9c0 .826.675 1.5 1.5 1.5h9.227l-4.063-4.062a2.034 2.034 0 0 1-.664.113c-1.13 0-2.05-.92-2.05-2.05s.92-2.05 2.05-2.05 2.05.92 2.05 2.05c0 .233-.041.456-.113.665l3.163 3.163V9.928a2.05 2.05 0 0 1-1.15-1.84c0-1.13.92-2.05 2.05-2.05s2.05.92 2.05 2.05a2.05 2.05 0 0 1-1.15 1.84v8.127l3.146-3.146A2.051 2.051 0 0 1 18 12.239c1.13 0 2.05.92 2.05 2.05s-.92 2.05-2.05 2.05c-.25 0-.488-.047-.709-.13L12.9 20.602v3.088h9.6c.825 0 1.5-.675 1.5-1.5v-9c0-.825-.477-1.977-1.061-2.561z"/>
    </svg>
  );
}

/** Photon 官方标(三条斜圆角杆,即 Photon logo mark;fill=currentColor,
 * 24×24)——SVG 数据直接采用自蓝本 platform-icon.tsx 的 PhotonIcon
 * (~/.hermes/hermes-agent/apps/desktop/src/app/messaging/platform-icon.tsx
 * 「three diagonal rounded bars (the Photon logo mark)」,NousResearch/
 * Hermes-Agent,MIT),品牌色 #6366F1 同源(图标即数据,一字符未改)。 */
function PhotonGlyph(props: SVGProps<SVGSVGElement>) {
  return (
    <svg fill="currentColor" viewBox="0 0 24 24" {...props}>
      <rect height="10" rx="1.25" transform="rotate(15 14 7.5)" width="2.5" x="12.75" y="2.5" />
      <rect height="10" rx="1.25" transform="rotate(15 8 13)" width="2.5" x="6.75" y="8" />
      <rect height="10" rx="1.25" transform="rotate(15 16 18)" width="2.5" x="14.75" y="13" />
    </svg>
  );
}

/** 未登记平台兜底:名称首字 monogram(上游 monogramFor 同语义;中文取首汉字)。 */
export const monogramFor = (name: string): string => name.trim().charAt(0).toUpperCase();

// ---------------------------------------------------------------------------
// 平台图标规格表(28 平台全覆盖;清单与 platform-overview 波次表同源)
// ---------------------------------------------------------------------------

/** 头像芯片规格:brand = 品牌色底画精确标/monogram;generic = 灰通用标随波次。 */
export interface PlatformIconSpec {
  /** 品牌字形(精确官方标);generic 条目必填,lucide 通用图标也是 SVG 组件。 */
  Icon?: ComponentType<SVGProps<SVGSVGElement>>;
  /** 品牌原生色(品牌色是数据,非主题 token;仅 brand 用)。 */
  color?: string;
  kind: "brand" | "generic";
  /** 品牌方未发布可用字形时的官方字形 monogram(如飞书官方标即「飞」)。 */
  monogram?: string;
  /** generic 专属:未实装波次(已实装的无标平台不带 wave → 全灰档)。 */
  wave?: "W2" | "W3";
}

/** 28 平台(16 已实装精确标 + 11 已实装无标全灰 + 1 未实装通用标);键与
 * IMPLEMENTED/UPCOMING 平台 id 一一对应。
 * W2 转实装(task 10-03-messaging-w2-platforms):ntfy = Simple Icons 官方字形
 * (品牌色 #317F6F,simple-icons 数据);钉钉/企微品牌方无可用简化标(与飞书
 * 同款 monogram 处理)——钉钉蓝 #0089FF(开放平台主站主色)、企微标准蓝
 * #267EF0(官方「应用色值表」blue_btn,developer.work.weixin.qq.com 94594)。
 * W3 转实装(task 10-03-messaging-w3-longtail):email/sms/irc/simplex 四家
 * 无可核订的官方品牌标(email/irc 是协议无单一品牌,sms 的 Twilio 红与
 * simplex 品牌色未经官方数据源核订)——不虚构品牌色,保留 lucide 通用标
 * 全灰档(wave 移除,与未实装 W3 弱一档区分);whatsapp_cloud/matrix/
 * google_chat 三家官方字形与品牌色均核订自 simple-icons 13(#25D366/
 * #000000/#34A853),teams 无 simple-icons 条目(Microsoft 系未收录)→
 * 官方品牌紫 #6264A7(Microsoft Teams UI Toolkit --brand-color)+
 * 「T」monogram(钉钉/企微同范式)。 */
export const PLATFORM_ICON_SPECS: Record<string, PlatformIconSpec> = {
  // —— 已实装精确标 ——
  feishu: { color: "#3370FF", kind: "brand", monogram: "飞" },
  telegram: { Icon: TelegramGlyph, color: "#26A5E4", kind: "brand" },
  ntfy: { Icon: NtfyGlyph, color: "#317F6F", kind: "brand" },
  dingtalk: { color: "#0089FF", kind: "brand", monogram: "钉" },
  wecom: { color: "#267EF0", kind: "brand", monogram: "企" },
  // 微信随 10-03-messaging-weixin-bridge 转实装:generic → brand 精确标
  // (官方绿 #07C160 + 「微」monogram,钉钉/企微同范式)
  weixin: { color: "#07C160", kind: "brand", monogram: "微" },
  // —— 已实装 W3 长尾(10-03-messaging-w3-longtail 转实装):官方品牌标已
  //    核订(simple-icons 13 字形+色;teams 走官方紫 monogram) ——
  whatsapp_cloud: { Icon: WhatsAppGlyph, color: "#25D366", kind: "brand" },
  matrix: { Icon: MatrixGlyph, color: "#000000", kind: "brand" },
  google_chat: { Icon: GoogleChatGlyph, color: "#34A853", kind: "brand" },
  teams: { color: "#6264A7", kind: "brand", monogram: "T" },
  // 组一转实装:discord/line/mattermost = simple-icons 13 官方字形+品牌色
  // (#5865F2/#00C300/#0058CC,cdn.simpleicons.org 核订);slack 已被
  // simple-icons 按品牌方要求移除(同飞书)→ 官方品牌茄紫 #4A154B
  // (Slack brand palette 主色)+ 「S」monogram(上游蓝本同款处理)。
  slack: { color: "#4A154B", kind: "brand", monogram: "S" },
  discord: { Icon: DiscordGlyph, color: "#5865F2", kind: "brand" },
  line: { Icon: LineGlyph, color: "#00C300", kind: "brand" },
  mattermost: { Icon: MattermostGlyph, color: "#0058CC", kind: "brand" },
  // 组三转实装:homeassistant = simple-icons 13 官方屋形字形 + 品牌蓝
  // #18BCF2(官方字形/色数据源见上方 HomeAssistantGlyph 注释)。
  homeassistant: { Icon: HomeAssistantGlyph, color: "#18BCF2", kind: "brand" },
  // —— 已实装 W3 长尾(10-03-messaging-w3-longtail 转实装):无官方品牌标
  //    可核订 → generic 全灰档(不带 wave,与未实装 W3 弱一档区分) ——
  email: { Icon: Mail, kind: "generic" },
  sms: { Icon: MessageSquareText, kind: "generic" },
  irc: { Icon: MessageSquareText, kind: "generic" },
  simplex: { Icon: MessageSquareText, kind: "generic" },
  // 组一/组三转实装(本片):qqbot/msgraph_webhook/bluebubbles/yuanbao
  // 四家品牌色/字形未经官方数据源核订(不虚构)→ 通用标全灰档,同上四家。
  qqbot: { Icon: MessageSquareText, kind: "generic" },
  msgraph_webhook: { Icon: Webhook, kind: "generic" },
  bluebubbles: { Icon: MessageSquareText, kind: "generic" },
  yuanbao: { Icon: MessageSquareText, kind: "generic" },
  // signal 出壳(10-05-push-reliability-batch R3):从 UPCOMING 转实装,
  // 图标规格随出壳同步——未实装弱档的 wave 字段退役,与上四家同走
  // generic 全灰档(signal 品牌蓝 #3A76F0 未核订官方数据源,不虚构)。
  signal: { Icon: MessageSquareText, kind: "generic" },
  // 组三收尾转实装(本片):photon = 蓝本自带官方 logo mark(三斜杆
  // PhotonGlyph)+ 品牌色 #6366F1(蓝本 platform-icon.tsx 同源)→ brand;
  // a2a/buzz/raft 品牌色/字形无可核订官方数据源(a2a 是 LF 协议标准无单一
  // 品牌方;buzz/raft 蓝本未给标)→ 通用标全灰档(不带 wave),不虚构。
  photon: { Icon: PhotonGlyph, color: "#6366F1", kind: "brand" },
  a2a: { Icon: Bot, kind: "generic" },
  buzz: { Icon: MessageSquareText, kind: "generic" },
  raft: { Icon: MessageSquareText, kind: "generic" },
};

// ---------------------------------------------------------------------------
// 芯片组件(上游 AvatarChip 画法:品牌色 16% tint + currentColor 字形)
// ---------------------------------------------------------------------------

interface PlatformAvatarProps {
  platformId: string;
  platformName: string;
  className?: string;
}

/**
 * 平台身份芯片:平台行/详情头/目录速览共用同一画法(上游「一种画法,处处
 * 同款」的纪律)。24px 方形;brand 用品牌色 tint 底,generic 用灰底(已实装
 * 全灰 / 未实装 W3 弱一档),未登记平台用中性底 + 名称首字 monogram 兜底。
 */
export function PlatformAvatar({ className, platformId, platformName }: PlatformAvatarProps) {
  const spec = PLATFORM_ICON_SPECS[platformId];
  const chipClass = cn(
    "relative inline-grid size-6 shrink-0 place-items-center rounded-md font-medium",
    className,
  );

  if (!spec) {
    return (
      <span
        aria-hidden="true"
        className={cn(chipClass, "bg-muted text-xs text-muted-foreground")}
        data-testid={`platform-avatar-${platformId}`}
      >
        {monogramFor(platformName)}
      </span>
    );
  }

  if (spec.kind === "generic") {
    const Icon = spec.Icon!;
    return (
      <span
        aria-hidden="true"
        className={cn(
          chipClass,
          // 灰态随实装状态:已实装无标平台全灰;未实装 W3 底与字形各再弱一档
          spec.wave === "W3" ? "bg-muted/50 text-muted-foreground/60" : "bg-muted text-muted-foreground",
        )}
        data-testid={`platform-avatar-${platformId}`}
      >
        <Icon className="size-3.5" />
      </span>
    );
  }

  const Icon = spec.Icon;
  return (
    <span
      aria-hidden="true"
      className={chipClass}
      data-testid={`platform-avatar-${platformId}`}
      style={{
        // 品牌色 16% tint 底(上游 AvatarChip 同比例);品牌色是数据非主题 token
        backgroundColor: `color-mix(in srgb, ${spec.color} 16%, transparent)`,
        color: spec.color,
      }}
    >
      {Icon ? <Icon className="size-[58%]" /> : (spec.monogram ?? monogramFor(platformName))}
    </span>
  );
}
