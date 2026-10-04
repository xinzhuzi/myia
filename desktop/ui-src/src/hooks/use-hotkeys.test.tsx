// @vitest-environment jsdom
//
// use-hotkeys 底座测试(快捷键注册表 + 输入框守卫 + 清理):
// 单键触发 / 输入框守卫三形(INPUT/TEXTAREA/contentEditable)/ 修饰键口径
// (单键遇 ⌘/Ctrl/Alt 不认领;mod+k 认 ⌘ 与 Ctrl)/ allowInInput 放行 /
// 卸载清理 / handler 刷新(旧闭包不残留)。
import { act, cleanup, render, renderHook } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useHotkeys } from "@/hooks/use-hotkeys";

function pressKey(key: string, init: KeyboardEventInit = {}) {
  act(() => {
    window.dispatchEvent(new KeyboardEvent("keydown", { key, bubbles: true, ...init }));
  });
}

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe("useHotkeys(底座:注册表+输入框守卫+清理)", () => {
  it("单键命中触发 handler(“[” 侧栏折叠键)", () => {
    const handler = vi.fn();
    renderHook(() => useHotkeys({ "[": handler }));

    pressKey("[");
    expect(handler).toHaveBeenCalledTimes(1);
  });

  it("未注册的键不触发;同一次声明多条键各自由各自 handler 接", () => {
    const bracket = vi.fn();
    const k = vi.fn();
    renderHook(() => useHotkeys({ "[": bracket, k }));

    pressKey("x");
    expect(bracket).not.toHaveBeenCalled();
    expect(k).not.toHaveBeenCalled();

    pressKey("k");
    expect(k).toHaveBeenCalledTimes(1);
    expect(bracket).not.toHaveBeenCalled();
  });

  it("输入框守卫:INPUT/TEXTAREA/contentEditable 内敲键不触发", () => {
    const handler = vi.fn();
    function Harness() {
      useHotkeys({ "[": handler });
      return (
        <div>
          <input data-testid="in-input" />
          <textarea data-testid="in-textarea" />
          <div data-testid="in-editable" contentEditable />
        </div>
      );
    }
    const { getByTestId } = render(<Harness />);

    for (const testId of ["in-input", "in-textarea", "in-editable"]) {
      act(() => {
        getByTestId(testId).dispatchEvent(
          new KeyboardEvent("keydown", { key: "[", bubbles: true }),
        );
      });
    }
    expect(handler).not.toHaveBeenCalled();
  });

  it("单键遇修饰键不认领(⌘[ / Ctrl[ / Alt[ 不算 “[”);shift 不拦截", () => {
    const handler = vi.fn();
    renderHook(() => useHotkeys({ "[": handler }));

    pressKey("[", { metaKey: true });
    pressKey("[", { ctrlKey: true });
    pressKey("[", { altKey: true });
    expect(handler).not.toHaveBeenCalled();

    pressKey("[", { shiftKey: true });
    expect(handler).toHaveBeenCalledTimes(1);
  });

  it("mod+单键:⌘ 与 Ctrl 都认,裸按不认", () => {
    const handler = vi.fn();
    renderHook(() => useHotkeys({ "mod+k": handler }));

    pressKey("k");
    expect(handler).not.toHaveBeenCalled();

    pressKey("k", { metaKey: true });
    pressKey("K", { ctrlKey: true }); // 主键大小写不敏感
    expect(handler).toHaveBeenCalledTimes(2);
  });

  it("allowInInput: true 在输入框内放行", () => {
    const handler = vi.fn();
    function Harness() {
      useHotkeys({ escape: handler }, { allowInInput: true });
      return <input data-testid="in-input" />;
    }
    const { getByTestId } = render(<Harness />);

    act(() => {
      getByTestId("in-input").dispatchEvent(
        new KeyboardEvent("keydown", { key: "Escape", bubbles: true }),
      );
    });
    expect(handler).toHaveBeenCalledTimes(1);
  });

  it("清理:卸载后监听器移除,再按键不触发", () => {
    const handler = vi.fn();
    const { unmount } = renderHook(() => useHotkeys({ "[": handler }));

    unmount();
    pressKey("[");
    expect(handler).not.toHaveBeenCalled();
  });

  it("handler 刷新:重渲染换 handler 后按键走新闭包(旧闭包不残留)", () => {
    const first = vi.fn();
    const second = vi.fn();
    const { rerender } = renderHook(({ h }) => useHotkeys({ "[": h }), {
      initialProps: { h: first as (event: KeyboardEvent) => void },
    });

    rerender({ h: second });
    pressKey("[");
    expect(first).not.toHaveBeenCalled();
    expect(second).toHaveBeenCalledTimes(1);
  });
});
