// @vitest-environment jsdom
//
// 根级 ErrorBoundary 测试(10-07-unified-logging 批2;AC10):渲染崩溃 →
// 极简回退(错误文本 + 重新加载钮)+ console.error 留痕(errorboundary:
// 前缀,装机经 lib/log 劫持链落 shell.log——本测试只钉 console 调用,
// 转发链由 log.test.ts 单独把守)。
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ErrorBoundary } from "./error-boundary";

function Boom(): never {
  throw new Error("子树渲染崩溃样张");
}

describe("components · ErrorBoundary", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  it("正常子树:原样渲染,零介入", () => {
    const errorSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    render(
      <ErrorBoundary>
        <p>健康内容</p>
      </ErrorBoundary>,
    );
    expect(screen.getByText("健康内容")).toBeTruthy();
    expect(screen.queryByTestId("error-boundary")).toBeNull();
    expect(errorSpy).not.toHaveBeenCalledWith(
      expect.stringContaining("errorboundary:"),
      expect.anything(),
    );
  });

  it("渲染崩溃:极简回退(错误文本 + 重新加载钮)+ console.error 留痕", () => {
    const errorSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    render(
      <ErrorBoundary>
        <Boom />
      </ErrorBoundary>,
    );

    const fallback = screen.getByTestId("error-boundary");
    expect(fallback.textContent).toContain("子树渲染崩溃样张");
    const reload = screen.getByTestId("error-boundary-reload");
    expect(reload.textContent).toBe("重新加载");
    // 留痕:崩溃错误经 console.error(errorboundary: 前缀,含堆栈首行参数)
    expect(errorSpy).toHaveBeenCalledWith(
      expect.stringContaining("errorboundary: 渲染崩溃: 子树渲染崩溃样张"),
      expect.anything(),
    );
  });

  it("重新加载钮 → window.location.reload()", () => {
    vi.spyOn(console, "error").mockImplementation(() => {});
    const reloadSpy = vi.fn();
    Object.defineProperty(window, "location", {
      value: { ...window.location, reload: reloadSpy },
      writable: true,
    });
    render(
      <ErrorBoundary>
        <Boom />
      </ErrorBoundary>,
    );

    fireEvent.click(screen.getByTestId("error-boundary-reload"));
    expect(reloadSpy).toHaveBeenCalledTimes(1);
  });
});
