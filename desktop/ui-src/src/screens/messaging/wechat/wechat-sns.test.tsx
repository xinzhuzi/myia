// @vitest-environment jsdom
//
// 朋友圈分区组件测试(task 10-14-wechat-media-sns R5):时间线渲染(发帖人/
// 时间/正文/媒体位徽标)、导出触发与产物路径回报、结构化错误直显、合法空态。
// sidecar 全走 mock invoke(桥命令族零真跑;判例同 wechat-local.test.tsx)。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { WechatSnsTimeline } from "./wechat-sns";

type Handler = (params: never) => unknown;
type SidecarMap = Record<string, Handler>;

function installSidecar(map: SidecarMap): void {
  mocks.invoke.mockImplementation(
    async (_command: string, args: { method: string; params?: unknown }) => {
      const handler = map[args.method];
      if (!handler) {
        throw JSON.stringify({
          code: "method_not_found",
          path: "method",
          message: `未知方法 ${args.method}`,
          data: { allowed: Object.keys(map).sort() },
        });
      }
      return handler(args.params as never);
    },
  );
}

const FEED_ENTRY = {
  id: "9001",
  username: "wxid_a",
  nickname: "昵称甲",
  create_time: 1760000000,
  text: "合成朋友圈正文",
  media_count: 2,
  media_types: ["2", "2"],
  ref_username: null,
  ref_nickname: null,
};

beforeEach(() => {
  mocks.invoke.mockReset();
  installSidecar({});
});

afterEach(() => {
  cleanup();
});

describe("微信本机:朋友圈分区", () => {
  it("拉取朋友圈 → 时间线渲染(发帖人/时间/正文/媒体位徽标);params 带 since_days", async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    installSidecar({
      "wechat_local.sns_feed": (params: never) => {
        calls.push({ method: "wechat_local.sns_feed", params });
        return { sns: { feed: [FEED_ENTRY] } };
      },
    });
    render(<WechatSnsTimeline />);

    fireEvent.click(screen.getByTestId("wechat-sns-load"));
    const timeline = await screen.findByTestId("wechat-sns-timeline");
    expect(within(timeline).getByText("昵称甲")).toBeTruthy();
    expect(within(timeline).getByText("合成朋友圈正文")).toBeTruthy();
    expect(within(timeline).getByText("图片 ×2")).toBeTruthy();
    expect(calls[0]?.params).toEqual({ since_days: 30 });
  });

  it("导出 → sns_export 触发(格式/天数透传)→ 回报产物路径与文件数", async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    installSidecar({
      "wechat_local.sns_export": (params: never) => {
        calls.push({ method: "wechat_local.sns_export", params });
        return {
          sns_export: {
            format: "html",
            out_dir: "/data/wechat-localdb/exports/sns-20261014-010203",
            files: ["index.html"],
            with_media: false,
            stats: { entries: 12 },
          },
        };
      },
    });
    render(<WechatSnsTimeline />);

    fireEvent.click(screen.getByTestId("wechat-sns-export"));
    const box = await screen.findByTestId("wechat-sns-export-result");
    expect(box.textContent).toContain("已导出");
    expect(box.textContent).toContain("1 个文件");
    expect(box.textContent).toContain("/data/wechat-localdb/exports/sns-20261014-010203");
    expect(calls[0]?.params).toEqual({ format: "html", since_days: 30 });
  });

  it("导出格式切「数据」→ format=json 透传", async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    installSidecar({
      "wechat_local.sns_export": (params: never) => {
        calls.push({ method: "wechat_local.sns_export", params });
        return {
          sns_export: {
            format: "json",
            out_dir: "/tmp/out",
            files: ["sns-export.json"],
            with_media: false,
            stats: {},
          },
        };
      },
    });
    render(<WechatSnsTimeline />);
    fireEvent.change(screen.getByLabelText("导出格式"), { target: { value: "json" } });
    fireEvent.click(screen.getByTestId("wechat-sns-export"));
    await screen.findByTestId("wechat-sns-export-result");
    expect(calls[0]?.params).toEqual({ format: "json", since_days: 30 });
  });

  it("拉取失败(key_unavailable):结构化错误 + 修复指引直显", async () => {
    installSidecar({
      "wechat_local.sns_feed": () => {
        throw JSON.stringify({
          code: "key_unavailable",
          path: "$",
          message: "本地库密钥不可得",
          data: { fix_hint: "先在设置里完成取钥" },
        });
      },
    });
    render(<WechatSnsTimeline />);
    fireEvent.click(screen.getByTestId("wechat-sns-load"));
    const box = await screen.findByTestId("wechat-sns-error");
    expect(box.textContent).toContain("key_unavailable");
    expect(box.textContent).toContain("先在设置里完成取钥");
  });

  it("合法空态:窗口内零条动态", async () => {
    installSidecar({ "wechat_local.sns_feed": () => ({ sns: { feed: [] } }) });
    render(<WechatSnsTimeline />);
    fireEvent.click(screen.getByTestId("wechat-sns-load"));
    await waitFor(() =>
      expect(screen.getByTestId("wechat-sns-empty").textContent).toContain("没有朋友圈动态"),
    );
  });

  it("天数非法:前端轻预检拒(零协议调用)", async () => {
    const calls: Array<{ method: string }> = [];
    installSidecar({
      "wechat_local.sns_feed": () => {
        calls.push({ method: "wechat_local.sns_feed" });
        return { sns: { feed: [] } };
      },
    });
    render(<WechatSnsTimeline />);
    fireEvent.change(screen.getByLabelText("朋友圈天数"), { target: { value: "0" } });
    fireEvent.click(screen.getByTestId("wechat-sns-load"));
    await waitFor(() =>
      expect(screen.getByTestId("wechat-sns-error").textContent).toContain("天数须为正整数"),
    );
    expect(calls).toHaveLength(0);
  });
});
