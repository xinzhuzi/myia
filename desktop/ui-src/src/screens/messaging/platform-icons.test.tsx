// @vitest-environment jsdom
//
// 平台头像芯片(task 10-03-messaging-hermes-look R1)组件测试:
// 28 平台规格表全覆盖(键集与波次表一一对应)、telegram 精确官方标(SVG
// path 数据直接采用)、feishu 官方字形 monogram(飞书官方标即「飞」)、
// generic 灰态分档(已实装无标全灰 / 未实装 W3 弱一档)、未登记平台兜底
// monogram。品牌色是数据非主题 token;状态三色不在本文件(在 StatePill)。
import { cleanup, render } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import {
  monogramFor,
  PLATFORM_ICON_SPECS,
  PlatformAvatar,
} from "./platform-icons";
import { IMPLEMENTED_PLATFORMS, UPCOMING_PLATFORMS } from "./platform-overview";

// vitest 非 globals 模式下 RTL 不自动清理,防 DOM 跨用例污染(与消息屏主测试同范式)
afterEach(() => {
  cleanup();
});

describe("平台头像:规格表全覆盖", () => {
  it("28 平台全部有规格;已实装 28 家(16 brand 精确标 + 12 无标全灰档),未实装清零(signal 10-05 出壳)", () => {
    const expected = [
      ...IMPLEMENTED_PLATFORMS.map((p) => p.id),
      ...UPCOMING_PLATFORMS.map((p) => p.id),
    ];
    expect(Object.keys(PLATFORM_ICON_SPECS).sort()).toEqual([...expected].sort());
    expect(Object.keys(PLATFORM_ICON_SPECS)).toHaveLength(28);
    // W2 转实装的四家(ntfy/钉钉/企微/微信)已从 UPCOMING 移入 IMPLEMENTED
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("ntfy");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("weixin");
    // W3 转实装的四家(email/sms/irc/simplex,10-03-messaging-w3-longtail)
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("email");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("simplex");
    // W3 转实装的另四家(whatsapp_cloud/matrix/google_chat/teams,同任务)
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("whatsapp_cloud");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("teams");
    // W3 组三 homeassistant 转实装(10-03-messaging-w3-longtail,同任务)
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("homeassistant");
    // W3 组一四家转实装(slack/discord/line/mattermost,10-03-messaging-w3-longtail)
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("slack");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("mattermost");
    // W3 组一/组三四家转实装(qqbot/msgraph_webhook 出站实装;bluebubbles/
    // yuanbao extras 壳,10-03-messaging-w3-longtail 本片)
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("qqbot");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("msgraph_webhook");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("bluebubbles");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("yuanbao");
    // W3 组三收尾四家转实装(a2a 出站实装;buzz/photon/raft extras 壳)
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("a2a");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("photon");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("buzz");
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("raft");
    // signal 出壳转实装(10-05-push-reliability-batch R3):UPCOMING 至此清零
    expect(IMPLEMENTED_PLATFORMS.map((p) => p.id)).toContain("signal");
    expect(UPCOMING_PLATFORMS).toEqual([]);
    for (const id of [
      "weixin",
      "email",
      "whatsapp_cloud",
      "teams",
      "homeassistant",
      "slack",
      "mattermost",
      "qqbot",
      "msgraph_webhook",
      "bluebubbles",
      "yuanbao",
      "a2a",
      "photon",
      "buzz",
      "raft",
      "signal",
    ]) {
      expect(UPCOMING_PLATFORMS.map((p) => p.id)).not.toContain(id);
    }

    for (const id of IMPLEMENTED_PLATFORMS.map((p) => p.id)) {
      const spec = PLATFORM_ICON_SPECS[id];
      if (spec.kind === "brand") {
        expect(spec.color).toMatch(/^#[0-9A-Fa-f]{6}$/); // 品牌色是数据(官方主色)
      } else {
        // W3 转实装但无官方品牌标可核订 → generic 全灰档(不带未实装波次)
        expect(spec.Icon).toBeTruthy(); // 通用标必填(lucide 也是 SVG 组件)
        expect(spec.wave).toBeUndefined();
      }
    }
    const waves = new Set<string>();
    for (const platform of UPCOMING_PLATFORMS) {
      const spec = PLATFORM_ICON_SPECS[platform.id];
      expect(spec.kind).toBe("generic");
      expect(spec.Icon).toBeTruthy(); // 通用标必填(lucide 也是 SVG 组件)
      expect(spec.wave).toBe(platform.wave);
      waves.add(spec.wave ?? "");
    }
    expect(waves).toEqual(new Set()); // 未实装清零(signal 10-05 出壳后)
  });
});

describe("平台头像:芯片画法", () => {
  it("telegram 精确官方标:svg path 数据直接采用,viewBox 24×24,fill=currentColor", () => {
    const { container } = render(
      <PlatformAvatar platformId="telegram" platformName="Telegram" />,
    );
    const svg = container.querySelector("svg");
    expect(svg).toBeTruthy();
    expect(svg?.getAttribute("viewBox")).toBe("0 0 24 24");
    expect(svg?.getAttribute("fill")).toBe("currentColor");
    // Simple Icons「Telegram」官方字形的开头(路径数据直接采用;一字符未改)
    expect(svg?.querySelector("path")?.getAttribute("d")).toMatch(/^M11\.944 0A12 12 0 0 0 0 12/);
    expect(svg?.querySelector("title")).toBeNull(); // aria-hidden 装饰性用,无 title
  });

  it("feishu 官方字形 monogram:品牌色 tint 底 +「飞」字符(飞书官方标即「飞」)", () => {
    const { container, getByTestId } = render(
      <PlatformAvatar platformId="feishu" platformName="飞书" />,
    );
    const chip = getByTestId("platform-avatar-feishu");
    expect(chip.textContent).toBe("飞");
    expect(chip.getAttribute("aria-hidden")).toBe("true");
    expect(container.querySelector("svg")).toBeNull(); // monogram 路线不出 svg
    // jsdom 会把 #3370FF 归一化为 rgb 形式;断言口径 = 品牌色 16% tint 底
    expect(chip.style.backgroundColor).toContain("color-mix(in srgb, rgb(51, 112, 255) 16%, transparent)");
    expect(chip.style.color).toContain("rgb(51, 112, 255)");
  });

  it("signal 出壳(10-05 R3)后不再走未实装弱灰档:UPCOMING 清零,generic 全灰档", () => {
    // 未实装名单清零(signal 是最后一家,10-05-push-reliability-batch R3 出壳)
    // ——「未实装 W3 弱一档」渲染分支(spec.wave==="W3")已无规格引用;
    // signal 图标规格的 wave 字段随出壳退役,与已实装无标平台同走全灰档。
    expect(UPCOMING_PLATFORMS).toEqual([]);
    expect(UPCOMING_PLATFORMS.filter((p) => p.wave === "W2")).toEqual([]);
    const { getByTestId } = render(<PlatformAvatar platformId="signal" platformName="Signal" />);
    const chip = getByTestId("platform-avatar-signal");
    expect(chip.querySelector("svg")).toBeTruthy(); // lucide 通用标也是 SVG
    expect(chip.className.split(/\s+/)).toContain("bg-muted"); // 全灰档
    expect(chip.className.split(/\s+/)).toContain("text-muted-foreground");
    expect(chip.className.split(/\s+/)).not.toContain("bg-muted/50"); // 不用未实装弱档
  });

  it("W3 转实装十二家无官方品牌标(email/sms/irc/simplex + qqbot/msgraph_webhook/bluebubbles/yuanbao + a2a/buzz/raft + signal 10-05 出壳)→ generic 全灰档(不带波次)", () => {
    // 10-03-messaging-w3-longtail + 10-05-push-reliability-batch R3:十二家
    // 无可核订官方标,不虚构品牌色;已实装全灰(a2a 是 LF 协议标准无单一
    // 品牌方,buzz/raft 蓝本未给标,signal 品牌蓝未核订)。
    for (const id of [
      "email",
      "sms",
      "irc",
      "simplex",
      "qqbot",
      "msgraph_webhook",
      "bluebubbles",
      "yuanbao",
      "a2a",
      "buzz",
      "raft",
      "signal",
    ]) {
      const { getByTestId } = render(<PlatformAvatar platformId={id} platformName={id} />);
      const chip = getByTestId(`platform-avatar-${id}`);
      expect(chip.querySelector("svg")).toBeTruthy(); // lucide 通用标
      expect(chip.className.split(/\s+/)).toContain("bg-muted"); // 全灰档
      expect(chip.className.split(/\s+/)).toContain("text-muted-foreground");
      expect(chip.className.split(/\s+/)).not.toContain("bg-muted/50"); // 不用未实装弱档
    }
  });

  it("photon 转实装(组三收尾本片):蓝本官方 logo mark(三条斜圆角杆)品牌色 #6366F1,不再走未实装弱灰档", () => {
    // 蓝本 platform-icon.tsx 的 PhotonIcon(SVG 数据直接采用,一字符未改)
    // + 品牌色 #6366F1 同源;photon 是壳通道但标是官方的——标与状态两套
    // 语言(状态色在 platform-overview 的 StatePill),不因壳降档。
    const { getByTestId } = render(<PlatformAvatar platformId="photon" platformName="Photon" />);
    const chip = getByTestId("platform-avatar-photon");
    const svg = chip.querySelector("svg");
    expect(svg?.getAttribute("viewBox")).toBe("0 0 24 24");
    expect(svg?.getAttribute("fill")).toBe("currentColor");
    expect(svg?.querySelectorAll("rect")).toHaveLength(3); // 三条斜圆角杆(logo mark)
    expect(chip.style.color).toContain("rgb(99, 102, 241)"); // #6366F1 蓝本品牌色
    expect(chip.style.backgroundColor).toContain(
      "color-mix(in srgb, rgb(99, 102, 241) 16%, transparent)",
    );
  });

  it("W3 转实装另四家:whatsapp/matrix/google_chat 官方字形品牌色;teams 官方紫 monogram", () => {
    // 10-03-messaging-w3-longtail:三家字形与品牌色核订自 simple-icons 13;
    // teams 无 simple-icons 条目(Microsoft 系未收录)→ 官方紫 #6264A7
    // (Teams UI Toolkit --brand-color)+「T」monogram(钉钉/企微同范式)。
    const { getByTestId, rerender } = render(
      <PlatformAvatar platformId="whatsapp_cloud" platformName="WhatsApp" />,
    );
    const whatsapp = getByTestId("platform-avatar-whatsapp_cloud");
    expect(whatsapp.querySelector("svg")?.getAttribute("viewBox")).toBe("0 0 24 24");
    // Simple Icons「WhatsApp」官方字形开头(路径数据直接采用;一字符未改)
    expect(whatsapp.querySelector("path")?.getAttribute("d")).toMatch(/^M17\.472 14\.382c/);
    expect(whatsapp.style.color).toContain("rgb(37, 211, 102)"); // #25D366

    rerender(<PlatformAvatar platformId="matrix" platformName="Matrix" />);
    const matrix = getByTestId("platform-avatar-matrix");
    expect(matrix.querySelector("path")?.getAttribute("d")).toMatch(/^M\.632\.55v22\.9H2\.28V24H0V0h2\.28v\.55z/);
    expect(matrix.style.color).toContain("rgb(0, 0, 0)"); // #000000(Matrix 官方黑)

    rerender(<PlatformAvatar platformId="google_chat" platformName="Google Chat" />);
    const googleChat = getByTestId("platform-avatar-google_chat");
    expect(googleChat.querySelector("path")?.getAttribute("d")).toMatch(/^M1\.637 0C\.733 0 0 \.733/);
    expect(googleChat.style.color).toContain("rgb(52, 168, 83)"); // #34A853

    rerender(<PlatformAvatar platformId="teams" platformName="Microsoft Teams" />);
    const teams = getByTestId("platform-avatar-teams");
    expect(teams.textContent).toBe("T"); // 无官方字形条目 → 官方紫 monogram
    expect(teams.style.color).toContain("rgb(98, 100, 167)"); // #6264A7
  });

  it("homeassistant 转实装(W3 组三):官方屋形标 + 品牌蓝 tint 底(不再走未实装弱灰档)", () => {
    // 10-03-messaging-w3-longtail:字形与品牌蓝 #18BCF2 均核订自 simple-icons
    // 13(源 home-assistant/assets 官方仓库),telegram/ntfy 同范式。
    const { getByTestId } = render(
      <PlatformAvatar platformId="homeassistant" platformName="Home Assistant" />,
    );
    const chip = getByTestId("platform-avatar-homeassistant");
    expect(chip.querySelector("svg")?.getAttribute("viewBox")).toBe("0 0 24 24");
    // Simple Icons「Home Assistant」官方屋形标开头(路径数据直接采用;一字符未改)
    expect(chip.querySelector("path")?.getAttribute("d")).toMatch(/^M22\.939 10\.627 13\.061\.749/);
    expect(chip.style.color).toContain("rgb(24, 188, 242)"); // #18BCF2 HA 官方蓝
  });

  it("W3 组一转实装四家:discord/line/mattermost 官方字形品牌色;slack 官方茄紫 monogram", () => {
    // 10-03-messaging-w3-longtail:三家字形与品牌色核订自 simple-icons 13
    // (#5865F2/#00C300/#0058CC,cdn.simpleicons.org);slack 已被 simple-icons
    // 按品牌方要求移除(同飞书)→ 官方品牌茄紫 #4A154B(Slack brand palette
    // 主色)+「S」monogram(上游蓝本对 Slack 同款处理)。
    const { getByTestId, rerender } = render(
      <PlatformAvatar platformId="slack" platformName="Slack" />,
    );
    const slack = getByTestId("platform-avatar-slack");
    expect(slack.querySelector("svg")).toBeNull(); // monogram 路线不出 svg
    expect(slack.textContent).toBe("S");
    expect(slack.style.color).toContain("rgb(74, 21, 75)"); // #4A154B 官方茄紫

    rerender(<PlatformAvatar platformId="discord" platformName="Discord" />);
    const discord = getByTestId("platform-avatar-discord");
    expect(discord.querySelector("svg")?.getAttribute("viewBox")).toBe("0 0 24 24");
    // Simple Icons「Discord」官方字形开头(路径数据直接采用;一字符未改)
    expect(discord.querySelector("path")?.getAttribute("d")).toMatch(/^M20\.317 4\.3698a19\.7913/);
    expect(discord.style.color).toContain("rgb(88, 101, 242)"); // #5865F2

    rerender(<PlatformAvatar platformId="line" platformName="LINE" />);
    const line = getByTestId("platform-avatar-line");
    expect(line.querySelector("path")?.getAttribute("d")).toMatch(/^M19\.365 9\.863c\.349 0 \.63\.285/);
    expect(line.style.color).toContain("rgb(0, 195, 0)"); // #00C300

    rerender(<PlatformAvatar platformId="mattermost" platformName="Mattermost" />);
    const mattermost = getByTestId("platform-avatar-mattermost");
    expect(mattermost.querySelector("path")?.getAttribute("d")).toMatch(/^M12\.081 0C7\.048-\.034 2\.339 3\.125/);
    expect(mattermost.style.color).toContain("rgb(0, 88, 204)"); // #0058CC
  });

  it("W2 转实装三家:ntfy 官方字形品牌色;钉钉/企微官方主色 monogram(与飞书同范式)", () => {
    const { getByTestId, rerender } = render(<PlatformAvatar platformId="ntfy" platformName="ntfy" />);
    const ntfy = getByTestId("platform-avatar-ntfy");
    // Simple Icons「ntfy」官方字形(SVG path 直接采用),品牌色 #317F6F(simple-icons 数据)
    expect(ntfy.querySelector("svg")?.getAttribute("viewBox")).toBe("0 0 24 24");
    expect(ntfy.style.color).toContain("rgb(49, 127, 111)"); // #317F6F
    expect(ntfy.textContent!.trim()).toBe(""); // 字形路线不出 monogram

    rerender(<PlatformAvatar platformId="dingtalk" platformName="钉钉" />);
    const dingtalk = getByTestId("platform-avatar-dingtalk");
    expect(dingtalk.textContent).toBe("钉"); // 品牌方无可用简化标 → 官方主色 + 字符
    expect(dingtalk.style.color).toContain("0, 137, 255"); // #0089FF 钉钉蓝

    rerender(<PlatformAvatar platformId="wecom" platformName="企业微信" />);
    const wecom = getByTestId("platform-avatar-wecom");
    expect(wecom.textContent).toBe("企");
    expect(wecom.style.color).toContain("38, 126, 240"); // #267EF0 企微标准蓝(官方色值表 blue_btn)

    // 微信(10-03-messaging-weixin-bridge 转实装):官方绿 + 「微」monogram
    rerender(<PlatformAvatar platformId="weixin" platformName="微信" />);
    const weixin = getByTestId("platform-avatar-weixin");
    expect(weixin.textContent).toBe("微");
    expect(weixin.style.color).toContain("7, 193, 96"); // #07C160 微信官方绿
  });

  it("未登记平台兜底:中性底 + 名称首字 monogram(上游 monogramFor 同语义)", () => {
    const { getByTestId } = render(
      <PlatformAvatar platformId="not-yet-registered" platformName="某新平台" />,
    );
    const chip = getByTestId("platform-avatar-not-yet-registered");
    expect(chip.textContent).toBe("某");
    expect(chip.className).toContain("bg-muted");
  });

  it("className 透传:调用方可改芯片尺寸(详情头/平台行共用同一画法)", () => {
    const { getByTestId } = render(
      <PlatformAvatar className="size-7" platformId="telegram" platformName="Telegram" />,
    );
    expect(getByTestId("platform-avatar-telegram").className).toContain("size-7");
  });
});

describe("平台头像:monogramFor 纯函数", () => {
  it("名称首字;中文取首汉字,西文取大写首字母,首尾空白剔除", () => {
    expect(monogramFor("飞书")).toBe("飞");
    expect(monogramFor("telegram")).toBe("T");
    expect(monogramFor("  Slack ")).toBe("S");
    expect(monogramFor("ntfy")).toBe("N");
  });
});
