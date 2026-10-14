// @vitest-environment jsdom
//
// 聊天媒体渲染件测试(task 10-14-wechat-media-sns R5):media_scan 扫描 → 缩略图
// 实显(cached_path 经 convertFileSrc)/视频 _thumb.jpg、点击同屏展开(组件内
// state)、wxgf 词面、media_unavailable(未配置解密件)结构化直显、空态与
// 前端预检。sidecar 全走 mock invoke;convertFileSrc 同 mock(判例同
// wechat-local.test.tsx)。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({
  invoke: mocks.invoke,
  convertFileSrc: (path: string) => `asset://mock/${path}`,
}));

import { WechatChatMedia } from "./wechat-media";

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
        });
      }
      return handler(args.params as never);
    },
  );
}

const SCAN_VIEW = {
  media: {
    chat_id: "filehelper",
    since_days: 30,
    items: [
      {
        message_ref: { ts: 1760000000, sender: "wxid_a", local_type: 3 },
        type: "image",
        key: "a1b2c3d4e5f60718293a4b5c6d7e8f90",
        files: { thumb: "/msg/attach/x/Img/a1b2_t.dat", full: "/msg/attach/x/Img/a1b2.dat" },
        status: "已解密",
        cached_path: "/cache/abcd1234.jpg",
      },
      {
        message_ref: { ts: 1760000100, sender: "wxid_a", local_type: 43 },
        type: "video",
        key: "d1b2c3d4e5f60718293a4b5c6d7e8f90",
        files: { video: "/msg/video/v.mp4", video_thumb: "/msg/video/v_thumb.jpg" },
        status: "明文直读(视频)",
      },
      {
        message_ref: { ts: 1760000200, sender: "wxid_a", local_type: 3 },
        type: "image",
        key: "e1b2c3d4e5f60718293a4b5c6d7e8f90",
        files: { thumb: "/msg/attach/x/Img/e1b2_t.dat" },
        status: "实况格式,暂不支持预览",
        cached_path: "/cache/wxgf0.wxgf",
      },
    ],
    stats: {
      messages: 3,
      image: 2,
      video: 1,
      other: 0,
      image_file_missing: 0,
      decrypted: 1,
    },
    provider: { configured: true, path: "/abs/provider" },
  },
};

beforeEach(() => {
  mocks.invoke.mockReset();
  installSidecar({});
});

afterEach(() => {
  cleanup();
});

describe("微信本机:聊天媒体分区", () => {
  it("扫描 → 列表渲染:图片缩略图实显(cached_path → 资产 src)+ 视频缩略图 + 状态词面 + 统计行", async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    installSidecar({
      "wechat_local.media_scan": (params: never) => {
        calls.push({ method: "wechat_local.media_scan", params });
        return SCAN_VIEW;
      },
    });
    render(<WechatChatMedia />);

    fireEvent.change(screen.getByLabelText("聊天图片会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-media-scan"));

    const list = await screen.findByTestId("wechat-media-list");
    const thumbs = within(list).getAllByTestId("wechat-media-thumb");
    expect(thumbs[0].getAttribute("src")).toBe("asset://mock//cache/abcd1234.jpg");
    expect(thumbs[1].getAttribute("src")).toBe("asset://mock//msg/video/v_thumb.jpg");
    expect(list.textContent).toContain("明文直读(视频)");
    expect(calls[0]?.params).toEqual({ chat_id: "filehelper", since_days: 30, decrypt: true });
    const stats = screen.getByTestId("wechat-media-stats");
    expect(stats.textContent).toContain("图片 2");
    expect(stats.textContent).toContain("已解出 1");
  });

  it("点击媒体行同屏展开(key 与路径在 mono 块)→ 再点收起", async () => {
    installSidecar({ "wechat_local.media_scan": () => SCAN_VIEW });
    render(<WechatChatMedia />);
    fireEvent.change(screen.getByLabelText("聊天图片会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-media-scan"));
    await screen.findByTestId("wechat-media-list");

    const rows = screen.getAllByTestId("wechat-media-row");
    fireEvent.click(rows[0]);
    const detail = await screen.findByTestId("wechat-media-detail");
    expect(detail.textContent).toContain("a1b2c3d4e5f60718293a4b5c6d7e8f90");
    expect(detail.textContent).toContain("cached: /cache/abcd1234.jpg");
    expect(screen.getByTestId("wechat-media-large")).toBeTruthy();

    fireEvent.click(rows[0]);
    await waitFor(() => expect(screen.queryByTestId("wechat-media-detail")).toBeNull());
  });

  it("wxgf 产物:词面「实况格式,暂不支持预览」,缩略图位走占位不出 <img>", async () => {
    installSidecar({ "wechat_local.media_scan": () => SCAN_VIEW });
    render(<WechatChatMedia />);
    fireEvent.change(screen.getByLabelText("聊天图片会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-media-scan"));
    const list = await screen.findByTestId("wechat-media-list");
    expect(list.textContent).toContain("实况格式,暂不支持预览");
    // 三项媒体:图 thumb + 视频 thumb = 恰 2 个缩略图;wxgf 走占位
    expect(within(list).getAllByTestId("wechat-media-thumb").length).toBe(2);
    expect(within(list).getAllByTestId("wechat-media-placeholder").length).toBe(1);
  });

  it("未配置解密件(media_unavailable):结构化错误 + 修复指引直显", async () => {
    installSidecar({
      "wechat_local.media_scan": () => {
        throw JSON.stringify({
          code: "media_unavailable",
          path: "$",
          message: "未配置媒体解密件,请在设置中指定可执行文件路径",
          data: {
            fix_hint:
              "wechat-bridge localdb media-decrypt set <媒体解密件可执行文件路径> 配置后重试",
          },
        });
      },
    });
    render(<WechatChatMedia />);
    fireEvent.change(screen.getByLabelText("聊天图片会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-media-scan"));
    const box = await screen.findByTestId("wechat-media-error");
    expect(box.textContent).toContain("media_unavailable");
    expect(box.textContent).toContain("media-decrypt set");
  });

  it("空会话 id:前端轻预检拒(零协议调用)", async () => {
    const calls: Array<{ method: string }> = [];
    installSidecar({
      "wechat_local.media_scan": () => {
        calls.push({ method: "wechat_local.media_scan" });
        return SCAN_VIEW;
      },
    });
    render(<WechatChatMedia />);
    fireEvent.click(screen.getByTestId("wechat-media-scan"));
    await waitFor(() =>
      expect(screen.getByTestId("wechat-media-error").textContent).toContain("不能为空"),
    );
    expect(calls).toHaveLength(0);
  });

  it("合法空态:窗口内零条媒体", async () => {
    installSidecar({
      "wechat_local.media_scan": () => ({
        media: { items: [], stats: {}, provider: { configured: false, path: null } },
      }),
    });
    render(<WechatChatMedia />);
    fireEvent.change(screen.getByLabelText("聊天图片会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-media-scan"));
    await waitFor(() =>
      expect(screen.getByTestId("wechat-media-empty").textContent).toContain("没有图片/视频消息"),
    );
  });
});
