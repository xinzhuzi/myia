// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { convertFileSrc, invoke } from "@tauri-apps/api/core";
import { FeedLocalImages } from "./feed-local-images";

vi.mock("@tauri-apps/api/core", () => ({ invoke: vi.fn(), convertFileSrc: vi.fn() }));
beforeEach(() => {
  vi.resetAllMocks();
  vi.mocked(convertFileSrc).mockImplementation((path) => `asset://localhost${path}`);
});
afterEach(cleanup);

describe("persisted feed images", () => {
  it("never converts paths until the shell authorizes them", async () => {
    vi.mocked(invoke).mockRejectedValue("outside root");
    render(<FeedLocalImages paths={["/private/secret.png"]} />);
    await screen.findByText("图片不可预览，文件可能已移动或不在保存目录内");
    expect(convertFileSrc).not.toHaveBeenCalled();
    expect(screen.queryByRole("img")).toBeNull();
    expect(screen.getByText("/private/secret.png")).toBeTruthy();
  });

  it("loads authorized thumbnails, expands at natural size, and degrades on error", async () => {
    vi.mocked(invoke).mockResolvedValue("/data/images/image.png");
    render(<FeedLocalImages paths={["/data/images/image.png"]} />);
    const img = await screen.findByRole("img", { name: "已保存配图 1" });
    expect(screen.getByText("图片加载中…")).toBeTruthy();
    fireEvent.load(img);
    const toggle = screen.getByRole("button", { name: "查看图片 1 原尺寸" });
    fireEvent.click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    expect(img.className).toContain("max-w-none");
    fireEvent.click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    fireEvent.error(img);
    expect(screen.getByText("图片加载失败，可核对下方保存路径")).toBeTruthy();
    expect(screen.queryByRole("img")).toBeNull();
    expect(invoke).toHaveBeenCalledWith("feed_image_path", { path: "/data/images/image.png" });
  });

  it("ignores malformed containers and rejects blank, relative, URL and traversal inputs", async () => {
    const { rerender } = render(<FeedLocalImages paths="not-an-array" />);
    expect(screen.queryByText(/图文件/)).toBeNull();
    rerender(<FeedLocalImages paths={[null, {}, "", "../image.png", "https://x/a.png", "/data/images/../secret.png"]} />);
    expect(invoke).not.toHaveBeenCalled();
    expect(convertFileSrc).not.toHaveBeenCalled();
  });

  it("discards authorization replies after unmount", async () => {
    let resolve!: (value: string) => void;
    vi.mocked(invoke).mockImplementation(() => new Promise<string>((done) => { resolve = done; }) as never);
    const { unmount } = render(<FeedLocalImages paths={["/data/images/image.png"]} />);
    unmount();
    resolve("/data/images/image.png");
    await waitFor(() => expect(convertFileSrc).not.toHaveBeenCalled());
  });

  it("accepts canonical Windows paths after shell authorization", async () => {
    const path = String.raw`\\?\C:\MYIA\images\image.png`;
    vi.mocked(invoke).mockResolvedValue(path);
    render(<FeedLocalImages paths={[path]} />);
    await screen.findByRole("img", { name: "已保存配图 1" });
    expect(convertFileSrc).toHaveBeenCalledWith(path);
  });
});
