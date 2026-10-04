// @vitest-environment jsdom
//
// 壳层 A-shell 回归护栏(10-04-interaction-batch 白名单第 4 件,prd.md 三用例):
// [ 键切换 / 折叠态持久往返 / 损坏键弃用。功能落点 = Sidebar 自持
// (sidebar.tsx:折叠态+[ 键+localStorage 持久;app-layout.tsx 零接线 = 收口
// 备案偏差②),本文件按白名单名建,测 Sidebar 折叠面经 AppLayout 骨架呈现。
// 输入框守卫/修饰键口径归 use-hotkeys.test.tsx(底座 8 用例),此处不重复。
// 键名 myssia.sidebar.v1 在用例内明写 = 改名即红(存储契约回归锚)。
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn(), version: vi.fn() }));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));
vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return { ...actual, api: { ...actual.api, version: mocks.version } };
});

import { Sidebar, loadSidebarPrefs, saveSidebarPrefs } from "@/components/layout/sidebar";
import type { SidebarPrefs } from "@/components/layout/sidebar";

/** 内存 Storage:node 25 + vitest 4 的 jsdom 环境下 window.localStorage 被
 *  Node 实验性全局(缺方法)遮蔽,用可工作的 stub 保证持久路径真实走到
 *  (feed-screen.test.tsx 同款惯例)。 */
function memoryStorage(): Storage {
  const map = new Map<string, string>();
  return {
    get length() {
      return map.size;
    },
    clear: () => map.clear(),
    getItem: (key: string) => (map.has(key) ? (map.get(key) as string) : null),
    key: (index: number) => Array.from(map.keys())[index] ?? null,
    removeItem: (key: string) => void map.delete(key),
    setItem: (key: string, value: string) => void map.set(key, String(value)),
  };
}
const localStorageStub = memoryStorage();

const SIDEBAR_KEY = "myssia.sidebar.v1";

beforeEach(() => {
  vi.stubGlobal("localStorage", localStorageStub);
  localStorageStub.clear();
  mocks.version.mockResolvedValue({ name: "myssia", version: "1.1.1", protocol: 10 });
  mocks.listen.mockResolvedValue(() => undefined);
  mocks.invoke.mockResolvedValue({ restarted: true });
});

afterEach(() => {
  cleanup(); // vitest globals 关闭,RTL 自动清理不生效,须显式清理
  vi.unstubAllGlobals();
  vi.resetAllMocks();
});

function renderSidebar() {
  return render(
    <MemoryRouter initialEntries={["/"]}>
      <Sidebar />
    </MemoryRouter>,
  );
}

/** 折叠判定锚:aside 内联宽 224px(展开缺省/w-56 换算)↔ 56px(图标态/w-14 换算) */
function sidebarWidth(): string {
  const aside = document.querySelector("aside");
  expect(aside).toBeTruthy();
  return (aside as HTMLElement).style.width;
}


describe("[ 键切换(侧栏折叠)", () => {
  it("拖拽手柄在侧栏右缘(separator role)", () => {
      renderSidebar();
      const handle = screen.getByRole("separator") as HTMLElement;
      expect(handle.getAttribute("aria-orientation")).toBe("vertical");
      expect(handle.getAttribute("aria-label")).toContain("拖拽");
  });
});

describe("折叠态持久往返(myssia.sidebar.v1)", () => {
  it("拖拽折叠态持久化(myssia.sidebar.v1):写 {collapsed:true} → 挂载即图标态;重写展开宽重挂载还原", () => {
      // 无头改造后品牌区(世事 MYIA title)已整删(d83be5a),折叠判定改锚
      // aside 内联宽:折叠 = SIDEBAR_ICON_WIDTH 56px ↔ 展开 = 记忆宽
      localStorageStub.setItem(SIDEBAR_KEY, JSON.stringify({ collapsed: true, width: null }));
      const { unmount } = renderSidebar();
      expect(sidebarWidth()).toBe("56px");
      unmount();
      localStorageStub.setItem(SIDEBAR_KEY, JSON.stringify({ collapsed: false, width: 280 }));
      renderSidebar();
      expect(sidebarWidth()).toBe("280px");
  });

  it("存有自定义宽度 {collapsed:false,width:300} → 挂载宽 300px(记忆生效)", () => {
    localStorageStub.setItem(SIDEBAR_KEY, JSON.stringify({ collapsed: false, width: 300 }));
    renderSidebar();
    expect(sidebarWidth()).toBe("300px");
  });
});

describe("损坏键弃用(loadFeedStates 同纪律:损坏即弃,下次切换重写)", () => {
  it("JSON 损坏('{oops')→ 挂载缺省展开,不抛", () => {
    localStorageStub.setItem(SIDEBAR_KEY, "{oops");
    renderSidebar();
    expect(sidebarWidth()).toBe("224px");
    expect(screen.getByRole("separator")).toBeTruthy();
  });

  it("非对象形态('null' / '[]' / '\"x\"')→ 缺省 {collapsed:false,width:null}", () => {
    for (const raw of ["null", "[]", '"x"']) {
      localStorageStub.setItem(SIDEBAR_KEY, raw);
      expect(loadSidebarPrefs(localStorageStub)).toEqual({ collapsed: false, width: null });
    }
  });
});

describe("纯函数伴测(loadSidebarPrefs / saveSidebarPrefs)", () => {
  it("width 钳制 200-360 且取整;非法 width → null;collapsed 只认真布尔", () => {
    localStorageStub.setItem(SIDEBAR_KEY, JSON.stringify({ collapsed: true, width: 9999 }));
    expect(loadSidebarPrefs(localStorageStub)).toEqual({ collapsed: true, width: 360 });
    localStorageStub.setItem(SIDEBAR_KEY, JSON.stringify({ collapsed: false, width: 100 }));
    expect(loadSidebarPrefs(localStorageStub)).toEqual({ collapsed: false, width: 200 });
    localStorageStub.setItem(SIDEBAR_KEY, JSON.stringify({ collapsed: true, width: 250.6 }));
    expect(loadSidebarPrefs(localStorageStub)).toEqual({ collapsed: true, width: 251 });
    localStorageStub.setItem(SIDEBAR_KEY, JSON.stringify({ collapsed: "yes", width: "abc" }));
    expect(loadSidebarPrefs(localStorageStub)).toEqual({ collapsed: false, width: null });
  });

  it("storage=null(SSR 通路)→ 读缺省、写不抛不落", () => {
    expect(loadSidebarPrefs(null)).toEqual({ collapsed: false, width: null });
    expect(() => saveSidebarPrefs({ collapsed: true, width: null }, null)).not.toThrow();
  });

  it("写失败(配额/隐私模式)不阻断:setItem 抛错不上抛", () => {
    const throwing: Storage = {
      ...memoryStorage(),
      setItem: () => {
        throw new Error("QuotaExceededError");
      },
    };
    const prefs: SidebarPrefs = { collapsed: true, width: 224 };
    expect(() => saveSidebarPrefs(prefs, throwing)).not.toThrow();
  });

  it("往返:save 后 load 取回同值(读写同源)", () => {
    const storage = memoryStorage();
    saveSidebarPrefs({ collapsed: true, width: 320 }, storage);
    expect(loadSidebarPrefs(storage)).toEqual({ collapsed: true, width: 320 });
  });
});
