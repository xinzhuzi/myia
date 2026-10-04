// @vitest-environment jsdom
/**
 * 情报流组件测试 —— mock sidecar(vi.mock "@/lib/api" 的 api 门面,store.items
 * 返回夹具分页;错误用真实 SidecarRequestError 注入)。
 * 覆盖:卡片渲染(标题/来源/分类/score/时间) / 未读·星标·稍后读三态(本地持久)
 * / 游标分页加载与判停 / 结构化错误与空态。
 * D4 批(10-03-ui-deep-imitation):品类色条与未读 accent 竖条、分组时间轴、
 * hover 浮现操作簇(accent/50 行背景 + time 让位)、U 快捷键、贴形加载骨架、
 * 错误态重试;纯函数 groupFeedItems/categoryColor 边界单测。
 * fe-small-batch 批(10-03-fe-small-batch):G8 卡片「AI 摘要」(feed.enrich:
 * loading/done/cached/scores 并回/无配置 graceful)/ G9 批量标已读未读(计数
 * 同步 + localStorage)/ G12 沉淀为关键词(yaml.list/read/save 经 invoke mock,
 * mtime 乐观锁 + 手术内容断言)/ P2⑤ 搜索框焦点环归全局体系(无局部 ring 覆写)。
 * interaction-batch 批(10-04 A-feed):j/k 键盘导航(边界钳制/focus 环/输入框
 * 守卫/scrollIntoView)/ 显示选项下拉(未读优先 + 分组维度,myssia.feed.display.v1
 * 持久)/ 卡片右键菜单四动作(打开原文/复制链接/标已读/沉淀 G12 联动);
 * 纯函数 sortUnreadFirst / groupFeedItemsByCategory / load·saveFeedDisplay。
 * read-state-server 批(10-04 G9 后半):能力门分流(protocol ≥
 * READ_STATE_PROTOCOL 过门走 store.state.*,低版/失败走旧 localStorage 通路)/
 * toggle 乐观 + 失败回滚 / mark_all 全库语义与 title 真话 / 一次性导入
 * (整 map 单请求,双挂载只一发,旧键不删);纯函数 statesFromItems。
 * g9-read-all 批(10-04 R1/R2/R4):品类分组组头「本组全部已读」(mark_all 带
 * category 精确等值;未分类组不出钮、时间/不分组无入口、未过门零入口)/
 * 全库两按钮 inline 二次确认(一次点击进确认态,再点执行;取消/Esc/失焦
 * 退出零执行);品类批量失败按快照只回滚作用域内行(域外组不动)。
 */
import { cleanup, fireEvent, render, screen, waitFor, within, act } from "@testing-library/react";
import { MemoryRouter, Outlet, Route, Routes } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { CategoryFilterContext } from "@/components/layout/app-layout";

import { SidecarRequestError } from "@/lib/api";
import type {
  FeedEnrichResult,
  FeedExportResult,
  FeedItem,
  HealthResult,
  StoreItemsParams,
  StoreItemsResult,
  VersionResult,
} from "@/lib/api";

import {
  appendWatchlistKeyword,
  categoryColor,
  DEFAULT_FEED_DISPLAY,
  groupFeedItems,
  groupFeedItemsByCategory,
  loadFeedDisplay,
  READ_STATE_PROTOCOL,
  saveFeedDisplay,
  setMarkerBulk,
  sortUnreadFirst,
  statesFromItems,
} from "./api";

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    api: {
      ...actual.api,
      version: vi.fn(),
      storeItems: vi.fn(),
      health: vi.fn(),
      runStart: vi.fn(),
      feedExport: vi.fn(),
      feedEnrich: vi.fn(),
      storeStateMark: vi.fn(),
      storeStateMarkAll: vi.fn(),
      storeStateImport: vi.fn(),
    },
    onSidecarEvent: vi.fn(),
  };
});

// G2/G3 的 Tauri 壳包:open(打开原文)/ save(导出对话框)均 mock(零真实动作);
// core 的 invoke = G12 yaml.* 屏私有封装的唯一传输面,按 method 分发夹具
vi.mock("@tauri-apps/plugin-shell", () => ({ open: vi.fn() }));
vi.mock("@tauri-apps/plugin-dialog", () => ({ save: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: vi.fn() }));

const { api, onSidecarEvent } = await import("@/lib/api");
const storeItemsMock = vi.mocked(api.storeItems);
const healthMock = vi.mocked(api.health);
const runStartMock = vi.mocked(api.runStart);
const feedExportMock = vi.mocked(api.feedExport);
const feedEnrichMock = vi.mocked(api.feedEnrich);
const versionMock = vi.mocked(api.version);
const markMock = vi.mocked(api.storeStateMark);
const markAllMock = vi.mocked(api.storeStateMarkAll);
const importMock = vi.mocked(api.storeStateImport);
const onSidecarEventMock = vi.mocked(onSidecarEvent);
const shellOpenMock = vi.mocked((await import("@tauri-apps/plugin-shell")).open);
const dialogSaveMock = vi.mocked((await import("@tauri-apps/plugin-dialog")).save);
// invoke 分发 mock(untyped Mock,惯例同 settings.test.tsx 的 mocks.invoke)
const invokeMock = (await import("@tauri-apps/api/core")).invoke as unknown as import("vitest").Mock;

import { FeedScreen } from "./feed-screen";

/** 空流时 refresh 会追问 health(first_run 分叉);默认给「有插件」的最小应答 */
function healthResult(overrides: Partial<HealthResult> = {}): HealthResult {
  return {
    command: "list",
    plugins_dir: "/home/plugins",
    db: "/home/myssia.db",
    store_error: null,
    plugins: [
      {
        file: "/home/plugins/ai-news.yaml",
        id: "ai-news",
        name: "AI资讯",
        schedule: "0 8,20 * * *",
        timezone: null,
        push_channels: [],
        loaded: true,
        load_errors: null,
        sources: [],
      },
    ],
    summary: { plugins: 1, sources: 0, ok: 0, degraded: 0, dead: 0, unknown: 0 },
    healthy: true,
    first_run: false,
    exit_code: 0,
    ...overrides,
  } as HealthResult;
}

function renderScreen() {
  return render(
    <MemoryRouter>
      <FeedScreen />
    </MemoryRouter>,
  );
}

/** C8 接线路径:AppLayout 形态(Routes → Outlet context 下发品类) */
function renderScreenWithCategory(category: string | null) {
  const context: CategoryFilterContext = { category };
  return render(
    <MemoryRouter initialEntries={["/feed"]}>
      <Routes>
        <Route path="/" element={<Outlet context={context} />}>
          <Route path="feed" element={<FeedScreen />} />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}

// ---------------------------------------------------------------------------
// 夹具(形状严格对齐 types.ts:FeedItem / StoreItemsResult)
// ---------------------------------------------------------------------------

let nextItemId = 0;
function fixtureItem(overrides: Partial<FeedItem> = {}): FeedItem {
  nextItemId += 1;
  return {
    id: nextItemId,
    url: `https://example.com/item-${nextItemId}`,
    dedup_key: `dk-${nextItemId}`,
    title: `条目 ${nextItemId}`,
    source: "Example",
    content: "净化摘要内容",
    tags: ["ai"],
    category: "tech",
    scores: { tech: 0.87 },
    pushed_at: null,
    push_slot: null,
    first_seen: new Date().toISOString(),
    ...overrides,
  };
}

function result(items: FeedItem[]): StoreItemsResult {
  return { db: "myssia.db", count: items.length, items };
}

/** 能力门探测应答(仅 protocol 字段参与判定) */
function versionResult(protocol: number): VersionResult {
  return { name: "myssia", version: "test", protocol, app_version: null };
}

/**
 * G9 服务端通路用例的干净模块图:resetModules 后动态取新实例 —— 一次性
 * 搬迁的会话哨位(api.ts 模块级布尔)与 mock 实例全部归零,用例间互不
 * 牵连(mock 工厂随 resetModules 重跑,新图里的 vi.fn 是新实例)。
 */
async function importFreshScreen() {
  vi.resetModules();
  const libApi = await import("@/lib/api");
  const feedScreen = await import("./feed-screen");
  return {
    FeedScreen: feedScreen.FeedScreen,
    versionMock: vi.mocked(libApi.api.version),
    storeItemsMock: vi.mocked(libApi.api.storeItems),
    markMock: vi.mocked(libApi.api.storeStateMark),
    markAllMock: vi.mocked(libApi.api.storeStateMarkAll),
    importMock: vi.mocked(libApi.api.storeStateImport),
  };
}

// G12 夹具:plugins 目录两个 YAML(一好一坏)+ 目标原文(流式 keywords)
const G12_FILES = [
  {
    file: "/home/plugins/ai-news.yaml",
    name: "ai-news.yaml",
    parse_ok: true,
    category_id: "ai-news",
    category_name: "AI资讯",
  },
  {
    file: "/home/plugins/broken.yaml",
    name: "broken.yaml",
    parse_ok: false,
    category_id: null,
    category_name: null,
  },
];
const G12_CONTENT = "id: ai-news\nname: AI资讯\nwatchlist:\n  keywords: [LLM, Agent]\n  mute: [广告]\n";

/**
 * G12 yaml.* 三方法分发 mock(yaml.list/read/save);返回 save 调用捕获数组。
 * saveImpl 注入失败路径(如 mtime_conflict 的 JSON 串拒绝,= Rust Err 形态)。
 */
function mockYamlSidecar(options: { readContent?: string; saveImpl?: () => Promise<unknown> } = {}) {
  const readContent = options.readContent ?? G12_CONTENT;
  const saves: { file: string; content: string; expected_mtime: number }[] = [];
  invokeMock.mockImplementation(async (_command: string, args?: { method?: string; params?: Record<string, unknown> }) => {
    const method = args?.method;
    const params = args?.params ?? {};
    if (method === "yaml.list") return { plugins_dir: "/home/plugins", files: G12_FILES };
    if (method === "yaml.read") return { file: params.file, content: readContent, mtime: 111 };
    if (method === "yaml.save") {
      saves.push({
        file: String(params.file),
        content: String(params.content),
        expected_mtime: params.expected_mtime as number,
      });
      if (options.saveImpl) return options.saveImpl();
      return {
        file: params.file,
        written: true as const,
        created: false,
        backed_up: "/home/plugins/ai-news.yaml.bak",
        mtime: 222,
        warnings: [],
      };
    }
    throw JSON.stringify({ code: "method_not_found", path: "$", message: `测试未 mock 方法:${method}` });
  });
  return saves;
}

/** 内存 Storage:node 25 + vitest 4 的 jsdom 环境下 window.localStorage 被
 *  Node 实验性全局(缺方法)遮蔽,用可工作的 stub 保证本地态路径真实走到。 */
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

beforeEach(() => {
  vi.stubGlobal("localStorage", localStorageStub);
  localStorageStub.clear();
  healthMock.mockResolvedValue(healthResult());
  onSidecarEventMock.mockResolvedValue(() => {});
  // 能力门缺省 = 低一版(未过门旧通路):既有用例全部走 localStorage 语义;
  // 服务端通路用例自带 versionResult(READ_STATE_PROTOCOL) 覆写。
  versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL - 1));
});

afterEach(() => {
  cleanup(); // vitest globals 关闭,RTL 自动清理不生效,须显式清理
  vi.unstubAllGlobals();
  vi.resetAllMocks();
  nextItemId = 0;
});

// ---------------------------------------------------------------------------
// 用例
// ---------------------------------------------------------------------------

describe("FeedScreen", () => {
  it("条目卡渲染:标题 / 来源 / 分类标签 / score 徽标 / 相对时间", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();

    await screen.findByText("条目 1");
    expect(screen.getByText(/Example/)).toBeTruthy();
    expect(screen.getByText("tech")).toBeTruthy();
    expect(screen.getByText("ai")).toBeTruthy();
    expect(screen.getByText("0.87")).toBeTruthy();
    expect(screen.getByText(/刚刚/)).toBeTruthy();
  });

  it("图析行:image_ocr 条目出「图」Badge + 单行摘要(空白压平),无图条目零渲染", async () => {
    const withImage = fixtureItem({ image_ocr: "GPT-5 发布会\n  截图里的 关键数字" });
    const withoutImage = fixtureItem();
    storeItemsMock.mockResolvedValue(result([withImage, withoutImage]));
    renderScreen();

    await screen.findByText("条目 1");
    // 有图条目:「图」Badge + 压平空白的单行摘要(10-03-vision-pipeline)
    const ocrRow = screen.getByTestId(`feed-image-ocr-${withImage.id}`);
    expect(ocrRow.textContent).toContain("图");
    expect(ocrRow.textContent).toContain("GPT-5 发布会 截图里的 关键数字");
    // 无图条目:零渲染变化 —— 无图析行、无「图」Badge
    expect(screen.queryByTestId(`feed-image-ocr-${withoutImage.id}`)).toBeNull();
    expect(screen.getAllByText("图")).toHaveLength(1);
  });

  it("图析行截断:超长 image_ocr 只出前 160 字符 + 省略号(title 属性留全文)", async () => {
    const long = "字".repeat(300);
    const withImage = fixtureItem({ image_ocr: long });
    storeItemsMock.mockResolvedValue(result([withImage]));
    renderScreen();

    await screen.findByText("条目 1");
    const ocrRow = screen.getByTestId(`feed-image-ocr-${withImage.id}`);
    expect(ocrRow.textContent).toContain(`${"字".repeat(160)}…`);
    expect(ocrRow.textContent).not.toContain(`${"字".repeat(161)}`);
    // title 属性保留原文,悬停可看全量(详情展开属 v2);经 title 精确锚定文本 span
    expect(screen.getByTitle(long).textContent).toContain(`${"字".repeat(160)}…`);
  });

  it("三态(本地):点标题记已读、星标与稍后读切换,过滤页签生效", async () => {
    const items = [fixtureItem(), fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    renderScreen();
    await screen.findByText("条目 1");

    // 点标题 → 已读 → 默认「未读」过滤下消失
    fireEvent.click(screen.getByText("条目 1"));
    await waitFor(() => expect(screen.queryByText("条目 1")).toBeNull());
    expect(screen.getByText("2 / 3 条")).toBeTruthy();

    // 星标 item2 → 卡内星形按钮按下,localStorage 持久
    const card2 = screen.getByTestId(`feed-item-${items[1].id}`);
    fireEvent.click(within(card2).getByRole("button", { name: "星标" }));
    await waitFor(() =>
      expect(within(card2).getByRole("button", { name: "星标" }).getAttribute("aria-pressed")).toBe("true"),
    );
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.states.v1") ?? "{}");
    expect((persisted as Record<string, { starred?: boolean }>)[items[1].dedup_key]?.starred).toBe(true);

    // 稍后读 item3
    const card3 = screen.getByTestId(`feed-item-${items[2].id}`);
    fireEvent.click(within(card3).getByRole("button", { name: "稍后读" }));

    // 过滤页签:星标只显示 item2;稍后读只显示 item3
    fireEvent.click(screen.getByRole("button", { name: "过滤:星标" }));
    expect(screen.getByText("条目 2")).toBeTruthy();
    expect(screen.queryByText("条目 3")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "过滤:稍后读" }));
    expect(screen.getByText("条目 3")).toBeTruthy();
    expect(screen.queryByText("条目 2")).toBeNull();
  });

  it("重挂载后本地态仍在(localStorage 持久)", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    const { unmount } = renderScreen();
    await screen.findByText("条目 1");
    const card = screen.getByTestId(`feed-item-${item.id}`);
    fireEvent.click(within(card).getByRole("button", { name: "星标" }));
    unmount();

    renderScreen();
    const cardAgain = await screen.findByTestId(`feed-item-${item.id}`);
    expect(within(cardAgain).getByRole("button", { name: "星标" }).getAttribute("aria-pressed")).toBe("true");
  });

  it("分页加载:首页 50 条出「加载更早」按钮,翻页带 before/before_id 复合游标,取尽后按钮消失", async () => {
    // 页 1:50 条(ids 100..51,新→旧);页 2:30 条(ids 50..21)
    const page1: FeedItem[] = [];
    for (let id = 100; id >= 51; id -= 1) {
      page1.push(fixtureItem({ id, dedup_key: `dk-${id}`, title: `条目 ${id}` }));
    }
    const oldest = page1[page1.length - 1];
    const cursor = oldest.first_seen as string;
    const cursorId = oldest.id as number;
    const page2: FeedItem[] = [];
    for (let id = 50; id >= 21; id -= 1) {
      page2.push(fixtureItem({ id, dedup_key: `dk-${id}`, title: `条目 ${id}` }));
    }
    storeItemsMock.mockImplementation((params?: StoreItemsParams) => {
      if (params?.before) return Promise.resolve(result(page2));
      return Promise.resolve(result(page1));
    });
    renderScreen();

    const loadMore = await screen.findByRole("button", { name: "加载更早的条目" });
    expect(screen.getByText("50 / 50 条")).toBeTruthy(); // 默认「未读」过滤:计数 50/50
    fireEvent.click(loadMore);

    // 翻页请求带上页最旧条目的 (first_seen, id) 复合游标(C1:同刻条目也能推进)
    await waitFor(() => expect(storeItemsMock).toHaveBeenCalledTimes(2));
    expect(storeItemsMock).toHaveBeenNthCalledWith(1, { limit: 50 });
    expect(storeItemsMock).toHaveBeenNthCalledWith(2, { limit: 50, before: cursor, before_id: cursorId });
    await screen.findByText("条目 21");
    expect(screen.getByText("80 / 80 条")).toBeTruthy();
    // 页 2 只有 30 条 < limit → 取尽,按钮消失
    expect(screen.queryByRole("button", { name: "加载更早的条目" })).toBeNull();
  });

  it("分页判停:翻页全为已加载条目(游标停滞)时按钮消失,且不出现重复卡", async () => {
    // 防御路径:服务端把已加载条目原样再回一遍(复合游标下不应发生,保留兜底防死循环)
    const page1: FeedItem[] = [];
    for (let id = 50; id >= 1; id -= 1) {
      page1.push(fixtureItem({ id, dedup_key: `dk-${id}`, title: `条目 ${id}` }));
    }
    storeItemsMock.mockImplementation(() => Promise.resolve(result(page1)));
    renderScreen();
    const loadMore = await screen.findByRole("button", { name: "加载更早的条目" });
    fireEvent.click(loadMore);

    await waitFor(() => expect(storeItemsMock).toHaveBeenCalledTimes(2));
    // 追加 0 条 → 判停按钮消失;仍是 50 张卡、无重复
    expect(screen.queryByRole("button", { name: "加载更早的条目" })).toBeNull();
    expect(screen.getAllByTestId(/^feed-item-/)).toHaveLength(50);
  });

  it("sidecar 结构化错误上屏(store_corrupt)", async () => {
    storeItemsMock.mockRejectedValue(
      new SidecarRequestError({ code: "store_corrupt", path: "params.db", message: "库文件损坏" }),
    );
    renderScreen();

    const banner = await screen.findByTestId("feed-error");
    expect(banner.textContent).toContain("store_corrupt");
    expect(banner.textContent).toContain("库文件损坏");
  });

  it("空态:无条目给「运行第一个插件」CTA(默认未读页签同口径)", async () => {
    storeItemsMock.mockResolvedValue(result([]));
    renderScreen();

    expect(await screen.findByText("情报流还是空的")).toBeTruthy();
    expect(screen.getByRole("button", { name: /运行第一个插件/ })).toBeTruthy();
  });

  it("空态 first_run 分支:无插件给初始化引导 + 去源管理,无运行 CTA", async () => {
    storeItemsMock.mockResolvedValue(result([]));
    healthMock.mockResolvedValue(healthResult({ first_run: true, plugins: [] }));
    renderScreen();

    expect(await screen.findByText("还没有可运行的插件")).toBeTruthy();
    expect(screen.getByRole("button", { name: "去源管理" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: /运行第一个插件/ })).toBeNull();
  });

  it("空流 CTA:点击 → health 取已加载插件 → run.start(yaml) → 采集中 → completed 刷新", async () => {
    storeItemsMock.mockResolvedValue(result([]));
    runStartMock.mockResolvedValue({
      run_id: 3, state: "running", yaml: "/home/plugins/ai-news.yaml", dry: false, db: "/home/myssia.db",
    });
    let emitEvent: ((event: { type: string; run_id: number }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string; run_id: number }) => void;
      return Promise.resolve(() => {});
    });
    renderScreen();

    fireEvent.click(await screen.findByRole("button", { name: /运行第一个插件/ }));
    await waitFor(() =>
      expect(runStartMock).toHaveBeenCalledWith({ yaml: "/home/plugins/ai-news.yaml" }),
    );
    expect(await screen.findByText(/采集中\(run #3\)/)).toBeTruthy();

    // completed 事件 → done 文案 + 刷新(store.items 再被调用)
    const callsBefore = storeItemsMock.mock.calls.length;
    act(() => emitEvent?.({ type: "completed", run_id: 3 }));
    expect(await screen.findByText(/本次采集已结束/)).toBeTruthy();
    await waitFor(() => expect(storeItemsMock.mock.calls.length).toBeGreaterThan(callsBefore));
  });

  it("空流 CTA 错误路径:run_busy 结构化拒绝上屏,按钮可重试", async () => {
    storeItemsMock.mockResolvedValue(result([]));
    runStartMock.mockRejectedValue(
      new SidecarRequestError({ code: "run_busy", path: "$", message: "已有 run 在执行" }),
    );
    renderScreen();

    fireEvent.click(await screen.findByRole("button", { name: /运行第一个插件/ }));
    expect(await screen.findByText(/run_busy/)).toBeTruthy();
    expect(screen.getByRole("button", { name: /运行第一个插件/ })).toBeTruthy();
  });

  // -------------------------------------------------------------------------
  // feed-ux 批(10-03-feed-ux):C8 品类接线 / G1 搜索 / G2 展开与打开原文 / G3 导出
  // -------------------------------------------------------------------------

  it("C8 品类接线:Outlet context 品类 → storeItems 收到 category 服务端过滤;null = 不传参", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreenWithCategory("ai-news");
    await screen.findByText("条目 1");
    expect(storeItemsMock).toHaveBeenCalledWith({ limit: 50, category: "ai-news" });
  });

  it("G1 搜索:Enter 即时提交 → query 随首页与翻页透传;计数行双层如实", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    await screen.findByText("条目 1");

    fireEvent.change(screen.getByLabelText("搜索条目"), { target: { value: "GLM" } });
    fireEvent.keyDown(screen.getByLabelText("搜索条目"), { key: "Enter" });

    await waitFor(() => expect(storeItemsMock).toHaveBeenLastCalledWith({ limit: 50, query: "GLM" }));
    expect(await screen.findByTestId("feed-search-scope")).toBeTruthy();
    expect(screen.getByTestId("feed-search-scope").textContent).toContain("GLM");
  });

  it("G1 搜索空态:零命中给专属空态文案(不再误导为「情报流是空的」)", async () => {
    storeItemsMock.mockResolvedValue(result([]));
    renderScreen();
    fireEvent.change(screen.getByLabelText("搜索条目"), { target: { value: "不存在的词" } });
    fireEvent.keyDown(screen.getByLabelText("搜索条目"), { key: "Enter" });

    expect(await screen.findByTestId("feed-search-empty")).toBeTruthy();
    expect(screen.queryByText("情报流还是空的")).toBeNull();
  });

  it("R1 Mod+F:⌘F/Ctrl+F 拦截浏览器查找(preventDefault)改聚焦搜索框并全选词面", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    await screen.findByText("条目 1");

    const search = screen.getByLabelText("搜索条目") as HTMLInputElement;
    fireEvent.change(search, { target: { value: "GLM" } });

    // macOS ⌘F:事件被 preventDefault(fireEvent 返回 false)+ 焦点落搜索框 + 全选
    const notPrevented = fireEvent.keyDown(window, { key: "f", metaKey: true });
    expect(notPrevented).toBe(false);
    expect(document.activeElement).toBe(search);
    expect(search.selectionStart).toBe(0);
    expect(search.selectionEnd).toBe("GLM".length);

    // Win/Linux Ctrl+F 同通路(再次聚焦仍成立)
    fireEvent.keyDown(window, { key: "f", ctrlKey: true });
    expect(document.activeElement).toBe(search);
  });

  it("R1 Esc 即时清空:搜索态按 Esc → 词面与已提交 query 同步归零(不等 300ms 防抖)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    await screen.findByText("条目 1");

    const search = screen.getByLabelText("搜索条目") as HTMLInputElement;
    fireEvent.change(search, { target: { value: "GLM" } });
    fireEvent.keyDown(search, { key: "Enter" });
    await waitFor(() => expect(storeItemsMock).toHaveBeenLastCalledWith({ limit: 50, query: "GLM" }));

    // 防抖在途的未提交词面(GLM5)也被 Esc 一并吞掉:重查不带 query
    fireEvent.change(search, { target: { value: "GLM5" } });
    fireEvent.keyDown(search, { key: "Escape" });
    expect(search.value).toBe("");
    await waitFor(() => expect(storeItemsMock).toHaveBeenLastCalledWith({ limit: 50 }));
    // 搜索范围行随 query 归零离场(回到未过滤态)
    await waitFor(() => expect(screen.queryByTestId("feed-search-scope")).toBeNull());
  });

  it("G2 卡片展开:展开按钮出全文与元信息,再点收起回两行摘要", async () => {
    const item = fixtureItem({ content: "第一行\n第二行\n第三行" });
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    const card = screen.getByTestId(`feed-item-${item.id}`);
    const expandButton = within(card).getByRole("button", { name: "展开条目" });
    expect(expandButton.getAttribute("aria-expanded")).toBe("false");
    expect(screen.queryByTestId(`feed-expanded-${item.id}`)).toBeNull(); // 收起态无全文块

    fireEvent.click(expandButton);
    const expanded = await screen.findByTestId(`feed-expanded-${item.id}`);
    expect(expanded.textContent).toContain("第一行");
    expect(within(card).getByRole("button", { name: "收起条目" }).getAttribute("aria-expanded")).toBe("true");

    fireEvent.click(within(card).getByRole("button", { name: "收起条目" }));
    await waitFor(() => expect(screen.queryByTestId(`feed-expanded-${item.id}`)).toBeNull());
  });

  it("G2 打开原文:http(s) 条目出按钮并调 plugin-shell open;非 http(s) 不渲染按钮", async () => {
    const httpItem = fixtureItem({ url: "https://example.com/story" });
    const ftpItem = fixtureItem({ url: "ftp://files.example.com/x" });
    storeItemsMock.mockResolvedValue(result([httpItem, ftpItem]));
    renderScreen();
    await screen.findByText("条目 1");

    const httpCard = screen.getByTestId(`feed-item-${httpItem.id}`);
    fireEvent.click(within(httpCard).getByRole("button", { name: "打开原文" }));
    await waitFor(() => expect(shellOpenMock).toHaveBeenCalledWith("https://example.com/story"));

    const ftpCard = screen.getByTestId(`feed-item-${ftpItem.id}`);
    expect(within(ftpCard).queryByRole("button", { name: "打开原文" })).toBeNull();
  });

  it("G2 打开原文失败:错误回显在 feed-open-error 行", async () => {
    shellOpenMock.mockRejectedValue(new Error("shell 未授权"));
    const item = fixtureItem({ url: "https://example.com/story" });
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    fireEvent.click(within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "打开原文" }));
    expect(await screen.findByTestId("feed-open-error")).toBeTruthy();
    expect(screen.getByTestId("feed-open-error").textContent).toContain("shell 未授权");
  });

  it("G3 导出:选格式 → dialog.save 默认名带日期 → feed.export 带当前过滤 → 回显 path/count", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    dialogSaveMock.mockResolvedValue("/tmp/myssia-feed-export.jsonl");
    const exportResult: FeedExportResult = { path: "/tmp/myssia-feed-export.jsonl", count: 1, bytes: 640 };
    feedExportMock.mockResolvedValue(exportResult);

    fireEvent.click(screen.getByRole("button", { name: "导出当前视图" }));
    await waitFor(() => expect(feedExportMock).toHaveBeenCalled());
    expect(feedExportMock).toHaveBeenCalledWith({ format: "jsonl", path: "/tmp/myssia-feed-export.jsonl" });
    expect(dialogSaveMock).toHaveBeenCalledWith(
      expect.objectContaining({ defaultPath: expect.stringMatching(/^myssia-feed-\d{8}\.jsonl$/) }),
    );
    expect(await screen.findByTestId("feed-export-result")).toBeTruthy();
    expect(screen.getByTestId("feed-export-result").textContent).toContain("/tmp/myssia-feed-export.jsonl");
    expect(screen.getByTestId("feed-export-result").textContent).toContain("1 条");

    // CSV 格式切换后走 csv 词表
    fireEvent.click(screen.getByRole("button", { name: "CSV" }));
    dialogSaveMock.mockResolvedValue("/tmp/myssia-feed-export.csv");
    feedExportMock.mockResolvedValue({ path: "/tmp/myssia-feed-export.csv", count: 1, bytes: 120 });
    fireEvent.click(screen.getByRole("button", { name: "导出当前视图" }));
    await waitFor(() =>
      expect(feedExportMock).toHaveBeenLastCalledWith({ format: "csv", path: "/tmp/myssia-feed-export.csv" }),
    );
  });

  it("G3 导出:对话框取消 = 静默(零 RPC 零回显);export_path_invalid 错误回显", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    await screen.findByText("条目 1");

    dialogSaveMock.mockResolvedValue(null);
    fireEvent.click(screen.getByRole("button", { name: "导出当前视图" }));
    await waitFor(() => expect(dialogSaveMock).toHaveBeenCalled());
    expect(feedExportMock).not.toHaveBeenCalled();
    expect(screen.queryByTestId("feed-export-result")).toBeNull();

    dialogSaveMock.mockResolvedValue("/tmp/again.jsonl");
    feedExportMock.mockRejectedValue(
      new SidecarRequestError({ code: "export_write_failed", path: "params.path", message: "磁盘满" }),
    );
    fireEvent.click(screen.getByRole("button", { name: "导出当前视图" }));
    expect(await screen.findByTestId("feed-export-result")).toBeTruthy();
    expect(screen.getByTestId("feed-export-result").textContent).toContain("export_write_failed");
  });

  // -------------------------------------------------------------------------
  // vision-v2 批(10-03-vision-v2):图析详情展开(OCR 全文/逐行置信度/caption/图文件)
  // -------------------------------------------------------------------------

  it("v2 图析详情展开:OCR 全文等宽块 + 逐行置信度表 + caption 全文 + 图文件路径列表;收起回单行摘要", async () => {
    const item = fixtureItem({
      content: null,
      image_ocr: "第一段落\n第二段落",
      image_ocr_lines: [
        { text: "行一(高置信)", conf: 0.95 },
        { text: "行二(低置信)", conf: 0.5 },
      ],
      image_caption: "一张发布会舞台照片,大屏写着发布日期。",
      image_files: ["/data/images/ab/cd12.jpg"],
    });
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    const card = screen.getByTestId(`feed-item-${item.id}`);
    // 无正文但有图析 → 仍可展开(hasImageDetails)
    const expandButton = within(card).getByRole("button", { name: "展开条目" });
    // 收起态:只有单行摘要(压平),零详情块
    expect(screen.getByTestId(`feed-image-ocr-${item.id}`).textContent).toContain("第一段落 第二段落");
    expect(screen.queryByTestId(`feed-image-ocr-lines-${item.id}`)).toBeNull();
    expect(screen.queryByTestId(`feed-image-caption-${item.id}`)).toBeNull();
    expect(screen.queryByTestId(`feed-image-files-${item.id}`)).toBeNull();

    fireEvent.click(expandButton);

    // OCR 全文:等宽块保换行(摘要态的压平不复现)
    const ocrFull = await screen.findByTestId(`feed-image-ocr-${item.id}`);
    expect(ocrFull.textContent).toContain("OCR 全文");
    const ocrPre = ocrFull.querySelector("pre");
    expect(ocrPre).not.toBeNull();
    expect(ocrPre?.textContent).toBe("第一段落\n第二段落"); // 换行原样保留

    // 逐行表:文本 + 置信度百分比(0-1 → %)
    const lines = screen.getByTestId(`feed-image-ocr-lines-${item.id}`);
    expect(lines.textContent).toContain("行一(高置信)");
    expect(lines.textContent).toContain("行二(低置信)");
    expect(lines.textContent).toContain("95%");
    expect(lines.textContent).toContain("50%");

    // caption 全文
    expect(screen.getByTestId(`feed-image-caption-${item.id}`).textContent).toContain("一张发布会舞台照片,大屏写着发布日期。");

    // 图文件:「图文件 N 张(路径)」文本列表(v2.2 再做图片本尊)
    const files = screen.getByTestId(`feed-image-files-${item.id}`);
    expect(files.textContent).toContain("图文件 1 张");
    expect(files.textContent).toContain("/data/images/ab/cd12.jpg");

    // 收起 → 回单行摘要,详情块消失
    fireEvent.click(within(card).getByRole("button", { name: "收起条目" }));
    await waitFor(() => expect(screen.queryByTestId(`feed-image-ocr-lines-${item.id}`)).toBeNull());
    expect(screen.getByTestId(`feed-image-ocr-${item.id}`).textContent).toContain("第一段落 第二段落");
  });

  it("v2 无图析条目:无正文且无图析 → 无展开按钮;有正文无图析 → 展开只显正文零图析块", async () => {
    const bare = fixtureItem({ content: null });
    const textOnly = fixtureItem({ content: "纯文本摘要" });
    storeItemsMock.mockResolvedValue(result([bare, textOnly]));
    renderScreen();
    await screen.findByText("条目 1");

    const bareCard = screen.getByTestId(`feed-item-${bare.id}`);
    expect(within(bareCard).queryByRole("button", { name: "展开条目" })).toBeNull();

    const textCard = screen.getByTestId(`feed-item-${textOnly.id}`);
    fireEvent.click(within(textCard).getByRole("button", { name: "展开条目" }));
    await screen.findByTestId(`feed-expanded-${textOnly.id}`);
    expect(screen.queryByTestId(`feed-image-ocr-lines-${textOnly.id}`)).toBeNull();
    expect(screen.queryByTestId(`feed-image-caption-${textOnly.id}`)).toBeNull();
    expect(screen.queryByTestId(`feed-image-files-${textOnly.id}`)).toBeNull();
    expect(screen.queryByTestId(`feed-image-ocr-${textOnly.id}`)).toBeNull();
  });

  it("v2 仅图析单键也能展开:image_ocr_lines 独有(无 ocr 全文)时逐行表可见", async () => {
    const item = fixtureItem({
      content: null,
      image_ocr_lines: [{ text: "仅逐行", conf: 0.88 }],
    });
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    const card = screen.getByTestId(`feed-item-${item.id}`);
    fireEvent.click(within(card).getByRole("button", { name: "展开条目" }));
    const lines = await screen.findByTestId(`feed-image-ocr-lines-${item.id}`);
    expect(lines.textContent).toContain("仅逐行");
    expect(lines.textContent).toContain("88%");
    // 无 image_ocr → 摘要行/全文块零渲染
    expect(screen.queryByTestId(`feed-image-ocr-${item.id}`)).toBeNull();
  });

  // -------------------------------------------------------------------------
  // D4 批(10-03-ui-deep-imitation):品类色条 / 分组时间轴 / hover 浮现 /
  // U 快捷键 / 三态(贴形骨架、错误重试);teardown-linear-activity #4/5/6/11
  // -------------------------------------------------------------------------

  it("D4 品类色条与未读竖条:未读 = accent 竖条,已读 = 品类色(inline),已读无品类零色件", async () => {
    // jsdom 把 inline 的 #rrggbb 规范化为 rgb() —— 断言前同法换算期望值
    const asRgb = (hex: string) => {
      const value = Number.parseInt(hex.slice(1), 16);
      return `rgb(${(value >> 16) & 255}, ${(value >> 8) & 255}, ${value & 255})`;
    };
    const unread = fixtureItem({ category: "ai-news" });
    const read = fixtureItem({ category: "stocks" });
    const readNoCategory = fixtureItem({ category: null });
    localStorageStub.setItem(
      "myssia.feed.states.v1",
      JSON.stringify({
        [read.dedup_key]: { read: true },
        [readNoCategory.dedup_key]: { read: true },
      }),
    );
    storeItemsMock.mockResolvedValue(result([unread, read, readNoCategory]));
    renderScreen();
    await screen.findByText("条目 1");
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));

    // 未读卡:data-unread=true,竖条 = accent(bg-primary),无 inline 色
    const unreadCard = screen.getByTestId(`feed-item-${unread.id}`);
    expect(unreadCard.getAttribute("data-unread")).toBe("true");
    const unreadStrip = screen.getByTestId(`feed-strip-${unread.id}`);
    expect(unreadStrip.className).toContain("bg-primary");
    expect(unreadStrip.style.backgroundColor).toBe("");

    // 已读卡:竖条 = 品类色(opacity-70 + inline backgroundColor)
    const readCard = screen.getByTestId(`feed-item-${read.id}`);
    expect(readCard.getAttribute("data-unread")).toBe("false");
    const readStrip = screen.getByTestId(`feed-strip-${read.id}`);
    expect(readStrip.className).toContain("opacity-70");
    expect(readStrip.style.backgroundColor).toBe(asRgb(categoryColor("stocks") as string));

    // 品类徽标着色同源(色条与徽标一色)
    const chip = screen.getByText("ai-news");
    expect(chip.style.color).toBe(asRgb(categoryColor("ai-news") as string));

    // 已读且无品类:零色件(无竖条)
    expect(screen.queryByTestId(`feed-strip-${readNoCategory.id}`)).toBeNull();
  });

  it("D4 hover 浮现操作:行背景 accent/50,操作簇 opacity-0→hover 显(focus-within 可达),time 让位", async () => {
    const item = fixtureItem({ url: "https://example.com/story" });
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    const card = await screen.findByTestId(`feed-item-${item.id}`);

    // teardown #5:行 hover 背景 = accent/50
    expect(card.className).toContain("hover:bg-accent/50");
    // 操作簇:平时 opacity-0,hover/focus-within 显(浮现动效走 token)
    const actions = card.querySelector("[data-feed-actions]");
    expect(actions).not.toBeNull();
    expect(actions?.className).toContain("opacity-0");
    expect(actions?.className).toContain("group-hover/feed-item:opacity-100");
    expect(actions?.className).toContain("focus-within:opacity-100");
    // 操作簇内动作齐全(反馈/原文/星标/稍后读/已读)
    for (const name of ["好评", "差评", "打开原文", "星标", "稍后读", "标记已读"]) {
      expect(within(actions as HTMLElement).getByRole("button", { name })).toBeTruthy();
    }
    // 右对齐相对时间(teardown #4):独立 time 元素,hover 让位给操作簇
    const time = card.querySelector("time");
    expect(time?.className).toContain("text-2xs");
    expect(time?.className).toContain("group-hover/feed-item:opacity-0");
    expect(time?.textContent).toContain("刚刚");
  });

  it("D4 分组时间轴:今日条目落「今天」sticky 组头(计数如实,同组单头)", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    renderScreen();

    const header = await screen.findByTestId("feed-group-今天");
    expect(header.textContent).toContain("今天");
    expect(header.textContent).toContain("2 条");
    expect(header.className).toContain("sticky");
    expect(screen.getAllByTestId("feed-group-今天")).toHaveLength(1);
  });

  it("D4 U 快捷键:hover 进入卡后按 U 切已读(未读过滤下离场);输入框内敲 u 不触发", async () => {
    const item = fixtureItem();
    const other = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item, other]));
    renderScreen();
    await screen.findByText("条目 1");

    fireEvent.mouseEnter(screen.getByTestId(`feed-item-${item.id}`));
    fireEvent.keyDown(window, { key: "u" });
    // 当前卡转已读 → 默认「未读」过滤下消失;另一卡不受牵连
    await waitFor(() => expect(screen.queryByTestId(`feed-item-${item.id}`)).toBeNull());
    expect(screen.getByTestId(`feed-item-${other.id}`).getAttribute("data-current")).toBe("false");

    // 输入框内敲 u:守卫生效(另一张卡不被切已读)
    const search = screen.getByLabelText("搜索条目");
    fireEvent.change(search, { target: { value: "u" } });
    fireEvent.keyDown(search, { key: "u" });
    expect(screen.getByTestId(`feed-item-${other.id}`).getAttribute("data-unread")).toBe("true");
  });

  it("D4 加载态:贴形骨架(feed-loading)常驻至首页应答,应答后卸载", async () => {
    let resolveItems: ((value: StoreItemsResult) => void) | undefined;
    storeItemsMock.mockImplementation(
      () => new Promise<StoreItemsResult>((resolve) => {
        resolveItems = resolve;
      }),
    );
    renderScreen();

    expect(await screen.findByTestId("feed-loading")).toBeTruthy();
    expect(screen.queryByTestId(/^feed-item-/)).toBeNull();
    act(() => resolveItems?.(result([fixtureItem()])));
    await screen.findByTestId("feed-item-1");
    expect(screen.queryByTestId("feed-loading")).toBeNull();
  });

  it("D4 错误态:结构化错误卡带重试按钮,点击重发 store.items 并恢复", async () => {
    storeItemsMock.mockRejectedValueOnce(
      new SidecarRequestError({ code: "store_corrupt", path: "params.db", message: "库文件损坏" }),
    );
    storeItemsMock.mockResolvedValueOnce(result([fixtureItem()]));
    renderScreen();

    const banner = await screen.findByTestId("feed-error");
    expect(banner.textContent).toContain("store_corrupt");
    // 错误态与空态互斥(质检修):错误卡在场时不得再落入空态 CTA
    // (store 损坏下「运行第一个插件」必失败,两卡叠加语义矛盾)
    expect(screen.queryByTestId("feed-run-cta")).toBeNull();
    expect(screen.queryByText("情报流还是空的")).toBeNull();
    fireEvent.click(within(banner).getByRole("button", { name: "重试" }));
    await screen.findByTestId("feed-item-1");
    expect(screen.queryByTestId("feed-error")).toBeNull();
  });

  // -------------------------------------------------------------------------
  // fe-small-batch 批(10-03-fe-small-batch):G8 AI 摘要 / G9 批量 /
  // G12 沉淀为关键词 / P2⑤ 搜索框焦点环
  // -------------------------------------------------------------------------

  it("G8 AI 摘要:点击 → feed.enrich(dedup_key)→ 复合分/模型/维度分/缓存命中上屏,scores 并回刷新徽标", async () => {
    const item = fixtureItem({ scores: { tech: 0.87 } });
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");
    expect(screen.getByText("0.87")).toBeTruthy(); // 初始分数徽标

    feedEnrichMock.mockResolvedValue({
      item_id: item.id,
      model: "test-model",
      scores: { 相关性: 8, 新颖性: 6 },
      score: 7.2,
      cached: true,
    } as FeedEnrichResult);

    fireEvent.click(within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "AI 摘要" }));
    expect(feedEnrichMock).toHaveBeenCalledWith({ item: item.dedup_key });

    const block = await screen.findByTestId(`feed-enrich-${item.id}`);
    expect(block.textContent).toContain("7.20");
    expect(block.textContent).toContain("test-model");
    expect(block.textContent).toContain("缓存命中");
    expect(block.textContent).toContain("相关性 8");
    // scores 并回本地列表:分数徽标 0.87 → 8.00(维度最大分)
    await waitFor(() => expect(screen.getByText("8.00")).toBeTruthy());
    expect(screen.queryByText("0.87")).toBeNull();
  });

  it("G8 loading 态:请求在途按钮禁用 + 「精评中…」行", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    feedEnrichMock.mockImplementation(() => new Promise<FeedEnrichResult>(() => {}));
    const button = within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "AI 摘要" });
    fireEvent.click(button);

    expect(await screen.findByTestId(`feed-enrich-loading-${item.id}`)).toBeTruthy();
    expect(button.getAttribute("disabled")).not.toBeNull();
  });

  it("G8 无配置 graceful:enrich_not_configured 明示「无精评配置」(不伪装成传输错误),按钮可重试", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    feedEnrichMock.mockRejectedValue(
      new SidecarRequestError({
        code: "enrich_not_configured",
        path: "params.item",
        message: "无法精评:品类 'tech' 未启用 enrich",
        data: { category: "tech", reason: "enrich_disabled" },
      }),
    );
    const button = within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "AI 摘要" });
    fireEvent.click(button);

    const error = await screen.findByTestId(`feed-enrich-error-${item.id}`);
    expect(error.textContent).toContain("无精评配置");
    expect(error.textContent).toContain("未启用 enrich");
    expect(error.getAttribute("title")).toContain("enrich_not_configured");
    await waitFor(() => expect(button.getAttribute("disabled")).toBeNull());
  });

  it("G9 全部标已读:二次确认后生效 → 计数同步 0/3 + 本地持久;全部标未读可还原", async () => {
    const items = [fixtureItem(), fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    renderScreen();
    await screen.findByText("条目 1");
    expect(screen.getByText("3 / 3 条")).toBeTruthy();

    // R2:一次点击只进确认态,再点「确认」才生效(两路同门,未过门不豁免)
    fireEvent.click(screen.getByRole("button", { name: "全部标已读" }));
    fireEvent.click(screen.getByRole("button", { name: "确认全部标已读" }));

    // 默认「未读」过滤:计数 0/3、卡片全部离场、空态如实
    await waitFor(() => expect(screen.getByText("0 / 3 条")).toBeTruthy());
    expect(screen.queryByTestId(/^feed-item-/)).toBeNull();
    expect(screen.getByText("没有未读条目")).toBeTruthy();
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.states.v1") ?? "{}");
    for (const item of items) {
      expect((persisted as Record<string, { read?: boolean }>)[item.dedup_key]?.read).toBe(true);
    }

    fireEvent.click(screen.getByRole("button", { name: "全部标未读" }));
    fireEvent.click(screen.getByRole("button", { name: "确认全部标未读" }));
    await waitFor(() => expect(screen.getByText("3 / 3 条")).toBeTruthy());
    expect(screen.getAllByTestId(/^feed-item-/)).toHaveLength(3);
  });

  it("G9 空载时批量按钮禁用(无事可做不诱点击)", async () => {
    storeItemsMock.mockResolvedValue(result([]));
    renderScreen();
    await screen.findByText("情报流还是空的");
    expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("disabled")).not.toBeNull();
    expect(screen.getByRole("button", { name: "全部标未读" }).getAttribute("disabled")).not.toBeNull();
  });

  it("P2⑤:搜索框焦点环归全局 :focus-visible 体系(无局部 ring-1/focus-visible 覆写)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    await screen.findByText("条目 1");
    const input = screen.getByLabelText("搜索条目");
    expect(input.className).not.toContain("ring-1");
    expect(input.className).not.toContain("focus-visible");
  });

  it("G12 沉淀为关键词:面板只列 parse_ok 目标,词面默认条目标题;read(mtime)→ 手术 → save → 回执带 .bak", async () => {
    const item = fixtureItem({ title: "GLM-5 发布" });
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("GLM-5 发布");
    const card = screen.getByTestId(`feed-item-${item.id}`);

    const saves = mockYamlSidecar();
    fireEvent.click(within(card).getByRole("button", { name: "沉淀为关键词" }));

    const panel = await screen.findByTestId(`feed-keyword-pin-${item.id}`);
    // 目标下拉只列可解析文件(坏文件不给选:写入必过校验,不往死路上引)
    const select = within(panel).getByLabelText("目标品类 YAML") as HTMLSelectElement;
    const options = Array.from(select.querySelectorAll("option"));
    expect(options).toHaveLength(1);
    expect(options[0]?.textContent).toContain("ai-news.yaml");
    // 词面默认 = 条目标题(可改)
    expect((within(panel).getByLabelText("沉淀关键词") as HTMLInputElement).value).toBe("GLM-5 发布");

    fireEvent.click(within(panel).getByRole("button", { name: "写入" }));

    await waitFor(() => expect(saves).toHaveLength(1));
    expect(invokeMock).toHaveBeenCalledWith("sidecar_request", {
      method: "yaml.read",
      params: { file: "/home/plugins/ai-news.yaml" },
    });
    // 手术内容:keywords 闭括号前追加新词,注释/其余行(含 id 行)逐字节不动;
    // expected_mtime = read 带回的乐观锁基线
    expect(saves[0]).toEqual({
      file: "/home/plugins/ai-news.yaml",
      content: "id: ai-news\nname: AI资讯\nwatchlist:\n  keywords: [LLM, Agent, GLM-5 发布]\n  mute: [广告]\n",
      expected_mtime: 111,
    });
    const note = await screen.findByTestId(`feed-keyword-note-${item.id}`);
    expect(note.textContent).toContain("已写入 ai-news.yaml");
    expect(note.textContent).toContain(".bak");
  });

  it("G12 词已在列表:already_present 零写入(save 不发),回执如实", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    const saves = mockYamlSidecar();
    const card = screen.getByTestId(`feed-item-${item.id}`);
    fireEvent.click(within(card).getByRole("button", { name: "沉淀为关键词" }));
    const panel = await screen.findByTestId(`feed-keyword-pin-${item.id}`);
    fireEvent.change(within(panel).getByLabelText("沉淀关键词"), { target: { value: "LLM" } });
    fireEvent.click(within(panel).getByRole("button", { name: "写入" }));

    const note = await screen.findByTestId(`feed-keyword-note-${item.id}`);
    expect(note.textContent).toContain("已在目标 YAML");
    await waitFor(() =>
      expect(invokeMock).toHaveBeenCalledWith("sidecar_request", { method: "yaml.read", params: expect.anything() }),
    );
    expect(saves).toHaveLength(0);
  });

  it("G12 mtime_conflict:save 乐观锁拒绝 → 结构化码原样明示", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    mockYamlSidecar({
      saveImpl: () =>
        Promise.reject(JSON.stringify({ code: "mtime_conflict", path: "params.file", message: "文件已被其他进程修改" })),
    });
    const card = screen.getByTestId(`feed-item-${item.id}`);
    fireEvent.click(within(card).getByRole("button", { name: "沉淀为关键词" }));
    const panel = await screen.findByTestId(`feed-keyword-pin-${item.id}`);
    fireEvent.click(within(panel).getByRole("button", { name: "写入" }));

    const note = await screen.findByTestId(`feed-keyword-note-${item.id}`);
    expect(note.textContent).toContain("mtime_conflict");
    expect(note.textContent).toContain("文件已被其他进程修改");
  });

  it("G12 清单拉取失败:list_error 明示 + 重试入口", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    renderScreen();
    await screen.findByText("条目 1");

    invokeMock.mockImplementation(async () => {
      throw JSON.stringify({ code: "source_dir_unreadable", path: "$", message: "插件目录不可读" });
    });
    const card = screen.getByTestId(`feed-item-${item.id}`);
    fireEvent.click(within(card).getByRole("button", { name: "沉淀为关键词" }));

    const error = await screen.findByTestId(`feed-keyword-list-error-${item.id}`);
    expect(error.textContent).toContain("source_dir_unreadable");
    expect(within(error).getByRole("button", { name: "重试" })).toBeTruthy();
  });
});

// ---------------------------------------------------------------------------
// interaction-batch 批(10-04 A-feed):j/k 键盘导航 / 显示选项下拉 /
// 右键上下文菜单(ui/context-menu.tsx 本批自建基件)
// ---------------------------------------------------------------------------

describe("FeedScreen · interaction-batch(A-feed)", () => {
  it("j/k 巡游:首按 j 选中首卡(focus 环可见),j/k 上下移,首末边界钳制不回绕", async () => {
    const items = [fixtureItem(), fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    // jsdom 无 scrollIntoView 实现:注入 spy 断言「最近侧滚入」调用(测后还原)
    const originalScroll = Element.prototype.scrollIntoView;
    Element.prototype.scrollIntoView = vi.fn();
    try {
      renderScreen();
      await screen.findByText("条目 1");

      const first = screen.getByTestId(`feed-item-${items[0].id}`);
      expect(first.getAttribute("data-current")).toBe("false"); // 未选中
      fireEvent.keyDown(window, { key: "j" });
      expect(first.getAttribute("data-current")).toBe("true");
      expect(first.getAttribute("data-nav-focused")).toBe("true");
      expect(first.className).toContain("ring-1"); // focus 环可见(A-feed 要点)
      expect(first.className).toContain("ring-primary");
      expect(Element.prototype.scrollIntoView).toHaveBeenCalledWith({ block: "nearest" });

      // 首卡 k:钳制原地不动(不回绕到末卡)
      fireEvent.keyDown(window, { key: "k" });
      expect(first.getAttribute("data-current")).toBe("true");

      // j → 第二卡;前卡让位
      fireEvent.keyDown(window, { key: "j" });
      const second = screen.getByTestId(`feed-item-${items[1].id}`);
      expect(second.getAttribute("data-current")).toBe("true");
      expect(first.getAttribute("data-current")).toBe("false");

      // 末卡再 j:钳制原地不动(不回绕回首卡)
      fireEvent.keyDown(window, { key: "j" });
      fireEvent.keyDown(window, { key: "j" });
      expect(screen.getByTestId(`feed-item-${items[2].id}`).getAttribute("data-current")).toBe("true");
      fireEvent.keyDown(window, { key: "j" });
      expect(screen.getByTestId(`feed-item-${items[2].id}`).getAttribute("data-current")).toBe("true");
    } finally {
      Element.prototype.scrollIntoView = originalScroll;
    }
  });

  it("j/k focus 环只在键盘巡游时呈现:hover 进入卡让环退出(data-current 仍在)", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    renderScreen();
    const first = await screen.findByTestId(`feed-item-${items[0].id}`);

    fireEvent.keyDown(window, { key: "j" });
    expect(first.className).toContain("ring-1");
    fireEvent.mouseEnter(first);
    expect(first.className).not.toContain("ring-1"); // hover = 背景态,focus 环让位
    expect(first.getAttribute("data-current")).toBe("true"); // 当前卡仍随 hover
  });

  it("j/k 守卫:输入框内敲 j 不动当前卡;⌘/Ctrl/Alt 修饰键不触发", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    renderScreen();
    await screen.findByText("条目 1");

    const search = screen.getByLabelText("搜索条目");
    fireEvent.change(search, { target: { value: "jk" } });
    fireEvent.keyDown(search, { key: "j" });
    fireEvent.keyDown(window, { key: "j", metaKey: true });
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    for (const item of items) {
      expect(screen.getByTestId(`feed-item-${item.id}`).getAttribute("data-current")).toBe("false");
    }

    // 守卫外正常路径仍在:window 上裸按 j 选中首卡
    fireEvent.keyDown(window, { key: "j" });
    expect(screen.getByTestId(`feed-item-${items[0].id}`).getAttribute("data-current")).toBe("true");
  });

  it("j/k + U 联动:j 选中后按 U 切已读(默认未读过滤下当前卡离场)", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    renderScreen();
    await screen.findByText("条目 1");

    fireEvent.keyDown(window, { key: "j" });
    fireEvent.keyDown(window, { key: "u" });
    await waitFor(() => expect(screen.queryByTestId(`feed-item-${items[0].id}`)).toBeNull());
    expect(screen.getByTestId(`feed-item-${items[1].id}`).getAttribute("data-current")).toBe("false");
  });

  it("显示选项 · 未读优先:开启后未读浮前(两类各自稳定保序),localStorage 持久", async () => {
    const unreadA = fixtureItem({ title: "未读甲" });
    const readB = fixtureItem({ title: "已读乙" });
    const unreadC = fixtureItem({ title: "未读丙" });
    localStorageStub.setItem(
      "myssia.feed.states.v1",
      JSON.stringify({ [readB.dedup_key]: { read: true } }),
    );
    storeItemsMock.mockResolvedValue(result([unreadA, readB, unreadC]));
    renderScreen();
    await screen.findByText("未读甲");
    // 全部视图:排序变化可观察(未读过滤下已读不可见)
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    const order = () =>
      screen.getAllByTestId(/^feed-item-/).map((node) => node.getAttribute("data-item-key"));
    expect(order()).toEqual([unreadA.dedup_key, readB.dedup_key, unreadC.dedup_key]);

    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "未读优先" }));

    // 未读甲/丙 浮前(原序),已读乙沉底(稳定保序,不乱序)
    await waitFor(() =>
      expect(order()).toEqual([unreadA.dedup_key, unreadC.dedup_key, readB.dedup_key]),
    );
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.display.v1") ?? "{}");
    expect((persisted as { unreadFirst?: boolean }).unreadFirst).toBe(true);
  });

  it("显示选项 · 分组维度:时间四桶(缺省)→ 按品类(色点同 categoryColor)→ 不分组(平铺)", async () => {
    const tech1 = fixtureItem({ category: "tech", title: "技一" });
    const news2 = fixtureItem({ category: "news", title: "闻二" });
    const tech3 = fixtureItem({ category: "tech", title: "技三" });
    const none4 = fixtureItem({ category: null, title: "无类四" });
    storeItemsMock.mockResolvedValue(result([tech1, news2, tech3, none4]));
    renderScreen();
    await screen.findByText("技一");

    // 缺省 = 时间四桶(既有 D4 行为不动)
    expect(screen.getByTestId("feed-group-今天").textContent).toContain("4 条");

    // 按品类分组:组头 = 品类首次出现顺序,tech 组头带 categoryColor 同源色点
    const asRgb = (hex: string) => {
      const value = Number.parseInt(hex.slice(1), 16);
      return `rgb(${(value >> 16) & 255}, ${(value >> 8) & 255}, ${value & 255})`;
    };
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "按品类分组" }));
    const techHeader = await screen.findByTestId("feed-group-tech");
    expect(techHeader.textContent).toContain("2 条");
    expect(screen.getByTestId("feed-group-news").textContent).toContain("1 条");
    expect(screen.getByTestId("feed-group-未分类").textContent).toContain("1 条");
    const dot = techHeader.querySelector("[data-group-color]");
    expect(dot).not.toBeNull();
    expect((dot as HTMLElement).style.backgroundColor).toBe(asRgb(categoryColor("tech") as string));
    // 无分类组头无色点(色件零渲染纪律)
    expect(screen.getByTestId("feed-group-未分类").querySelector("[data-group-color]")).toBeNull();

    // 不分组:组头全消、四卡平铺
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "不分组(平铺)" }));
    await waitFor(() => expect(screen.queryByTestId("feed-group-tech")).toBeNull());
    expect(screen.queryByTestId(/^feed-group-/)).toBeNull();
    expect(screen.getAllByTestId(/^feed-item-/)).toHaveLength(4);
    expect(screen.getByTestId("feed-flat-list")).toBeTruthy();

    // 持久:groupMode = none(重开菜单勾选态同步)
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.display.v1") ?? "{}");
    expect((persisted as { groupMode?: string }).groupMode).toBe("none");
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    const menu = await screen.findByRole("menu");
    expect(within(menu).getByRole("menuitem", { name: "不分组(平铺)" }).querySelector("svg")).not.toBeNull();
    expect(within(menu).getByRole("menuitem", { name: "时间分组(今天 / 昨天 / 7 天内 / 更早)" }).querySelector("svg")).toBeNull();
  });

  it("右键菜单:四动作齐(打开原文/复制链接/标记已读/沉淀为关键词),动作生效且选后自闭", async () => {
    const item = fixtureItem({ url: "https://example.com/story" });
    storeItemsMock.mockResolvedValue(result([item]));
    // navigator.clipboard 在 jsdom 缺席:注入 stub(测后还原)
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
    try {
      renderScreen();
      fireEvent.click(screen.getByRole("button", { name: "过滤:全部" })); // 标已读后卡仍在场
      const card = await screen.findByTestId(`feed-item-${item.id}`);

      fireEvent.contextMenu(card);
      const menu = await screen.findByRole("menu");
      expect(within(menu).getAllByRole("menuitem").map((node) => node.textContent)).toEqual([
        "打开原文",
        "复制链接",
        "标记已读",
        "沉淀为关键词…",
      ]);

      // 标记已读:切已读 + 菜单选后自闭(120ms 离场)
      fireEvent.click(within(menu).getByRole("menuitem", { name: "标记已读" }));
      await waitFor(() => expect(card.getAttribute("data-unread")).toBe("false"));
      await waitFor(() => expect(screen.queryByRole("menu")).toBeNull(), { timeout: 1000 });

      // 标签随状态切换(已读 → 标记未读);打开原文走 plugin-shell open 同门
      fireEvent.contextMenu(card);
      const menu2 = await screen.findByRole("menu");
      expect(within(menu2).getByRole("menuitem", { name: "标记未读" })).toBeTruthy();
      fireEvent.click(within(menu2).getByRole("menuitem", { name: "打开原文" }));
      await waitFor(() => expect(shellOpenMock).toHaveBeenCalledWith("https://example.com/story"));

      // 复制链接:navigator.clipboard.writeText
      fireEvent.contextMenu(card);
      fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "复制链接" }));
      await waitFor(() => expect(writeText).toHaveBeenCalledWith("https://example.com/story"));

      // 沉淀为关键词:直调卡内 openPin → G12 就地面板打开(面板本尊零改)
      const saves = mockYamlSidecar();
      expect(saves).toHaveLength(0);
      fireEvent.contextMenu(card);
      fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: /沉淀为关键词/ }));
      expect(await screen.findByTestId(`feed-keyword-pin-${item.id}`)).toBeTruthy();
    } finally {
      Reflect.deleteProperty(navigator, "clipboard");
    }
  });

  it("右键菜单:Esc 关闭;非 http(s) 条目「打开原文/复制链接」禁用(同 URL 门),标已读仍可用", async () => {
    const ftp = fixtureItem({ url: "ftp://files.example.com/x" });
    storeItemsMock.mockResolvedValue(result([ftp]));
    renderScreen();
    const card = await screen.findByTestId(`feed-item-${ftp.id}`);

    fireEvent.contextMenu(card);
    const menu = await screen.findByRole("menu");
    expect(within(menu).getByRole("menuitem", { name: "打开原文" }).getAttribute("disabled")).not.toBeNull();
    expect(within(menu).getByRole("menuitem", { name: "复制链接" }).getAttribute("disabled")).not.toBeNull();
    expect(within(menu).getByRole("menuitem", { name: "标记已读" }).getAttribute("disabled")).toBeNull();

    fireEvent.keyDown(menu, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("menu")).toBeNull(), { timeout: 1000 });
  });
});

// ---------------------------------------------------------------------------
// read-state-server 批(10-04 G9 后半):服务端通路(干净模块图)+ 能力门分流
// ---------------------------------------------------------------------------

describe("FeedScreen · read-state-server(G9 服务端通路)", () => {
  it("能力门过门:toggle 走 store.state.mark(乐观翻转),不写 localStorage", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markMock.mockResolvedValue({ updated: 1 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    const card = await screen.findByTestId("feed-item-1");
    // 过门生效的可见标志:批量按钮 title 换全库真话
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );
    const star = within(card).getByRole("button", { name: "星标" });
    fireEvent.click(star);
    await waitFor(() =>
      expect(fresh.markMock).toHaveBeenCalledWith({ keys: ["dk-1"], marker: "starred", value: true }),
    );
    await waitFor(() => expect(star.getAttribute("aria-pressed")).toBe("true"));
    // 服务端是唯一真源:本地快照零写入
    expect(localStorageStub.getItem("myssia.feed.states.v1")).toBeNull();
  });

  it("toggle 乐观 + 失败回滚:mark 拒绝 → 条目态回翻 + feed-mark-error 错误码原样明示", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    let rejectMark: ((err: unknown) => void) | undefined;
    fresh.markMock.mockImplementation(
      () => new Promise((_resolve, reject) => {
        rejectMark = reject;
      }),
    );
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    const card = await screen.findByTestId("feed-item-1");
    const star = within(card).getByRole("button", { name: "星标" });
    fireEvent.click(star);
    // 乐观:请求在途即按下
    await waitFor(() => expect(star.getAttribute("aria-pressed")).toBe("true"));
    expect(fresh.markMock).toHaveBeenCalledWith({ keys: ["dk-1"], marker: "starred", value: true });
    act(() =>
      rejectMark?.(new SidecarRequestError({ code: "internal_error", path: "$", message: "写库失败" })),
    );
    // 回滚:回到调用前真值(未星标)
    await waitFor(() => expect(star.getAttribute("aria-pressed")).toBe("false"));
    const error = await screen.findByTestId("feed-mark-error");
    expect(error.textContent).toContain("internal_error");
    expect(error.textContent).toContain("写库失败");
  });

  it("全部标已读 = 全库语义:点击发 store.state.mark_all(不按已加载 keys);title 真话;就地翻转不整页重拉", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 99 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByText("条目 1");
    const readAll = screen.getByRole("button", { name: "全部标已读" });
    await waitFor(() => expect(readAll.getAttribute("title")).toContain("全库"));
    // title 真话:含未翻页(全库),不再含「本地态/已加载」旧注记
    const title = readAll.getAttribute("title") ?? "";
    expect(title).toContain("未翻页");
    expect(title).not.toContain("本地态");
    expect(title).not.toContain("已加载");
    fireEvent.click(readAll);
    // R2:一次点击只进确认态;确认态 title 延续全库真话(进确认态不掉如实度)
    const confirm = screen.getByRole("button", { name: "确认全部标已读" });
    expect(confirm.getAttribute("title") ?? "").toContain("全库");
    expect(confirm.getAttribute("title") ?? "").not.toContain("已加载");
    fireEvent.click(confirm);
    await waitFor(() => expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: true }));
    expect(fresh.markMock).not.toHaveBeenCalled(); // 全库单 UPDATE,不逐键置位
    // 就地翻转已加载行:默认「未读」过滤 0/2、卡片离场;不整页重拉
    await waitFor(() => expect(screen.getByText("0 / 2 条")).toBeTruthy());
    expect(screen.queryByTestId(/^feed-item-/)).toBeNull();
    expect(fresh.storeItemsMock).toHaveBeenCalledTimes(1);
  });

  it("全部标未读失败:按调用前快照回滚(不瞎翻)+ feed-mark-error 明示", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    let rejectAll: ((err: unknown) => void) | undefined;
    fresh.markAllMock.mockImplementation(
      () => new Promise((_resolve, reject) => {
        rejectAll = reject;
      }),
    );
    fresh.storeItemsMock.mockResolvedValue(result([
      fixtureItem({ read: true, title: "已读甲" }),
      fixtureItem({ title: "未读乙" }),
    ]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByText("未读乙");
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    await screen.findByText("已读甲");
    fireEvent.click(screen.getByRole("button", { name: "全部标未读" }));
    fireEvent.click(screen.getByRole("button", { name: "确认全部标未读" }));
    await waitFor(() => expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: false }));
    // 乐观:两卡都翻未读
    await waitFor(() => expect(screen.getByTestId("feed-item-1").getAttribute("data-unread")).toBe("true"));
    expect(screen.getByTestId("feed-item-2").getAttribute("data-unread")).toBe("true");
    act(() =>
      rejectAll?.(new SidecarRequestError({ code: "store_corrupt", path: "$", message: "库损坏" })),
    );
    // 快照回滚:甲回已读、乙保持未读
    await waitFor(() => expect(screen.getByTestId("feed-item-1").getAttribute("data-unread")).toBe("false"));
    expect(screen.getByTestId("feed-item-2").getAttribute("data-unread")).toBe("true");
    const error = await screen.findByTestId("feed-mark-error");
    expect(error.textContent).toContain("store_corrupt");
  });

  it("一次性导入:map 非空 + 过门 → 单请求整 map(dedup_key/id:<n>/id:<url> 三形态);双挂载只一发;旧键不删", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.importMock.mockResolvedValue({ imported: 2, skipped: 1 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    const map = {
      "dk-1": { read: true },
      "id:9": { starred: true },
      "id:https://example.com/x": { later: true },
    };
    localStorageStub.setItem("myssia.feed.states.v1", JSON.stringify(map));
    const first = render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await waitFor(() => expect(fresh.importMock).toHaveBeenCalledTimes(1));
    // 整 map 一个请求(逐键 RPC = N 往返,否)
    expect(fresh.importMock).toHaveBeenCalledWith({ states: map });
    first.unmount();
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByTestId("feed-item-1"); // 第二次挂载完成渲染
    expect(fresh.importMock).toHaveBeenCalledTimes(1); // 会话哨位:双挂载只一发
    // 旧键保留不删(降级回旧 build 的回滚路径,Q2.3)
    expect(localStorageStub.getItem("myssia.feed.states.v1")).toBe(JSON.stringify(map));
  });

  it("一次性导入:map 空 → 过门也不发 import", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByTestId("feed-item-1");
    // 等能力门真正翻到服务端通路(title 现全库语义)再断言不发
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );
    expect(fresh.importMock).not.toHaveBeenCalled();
  });
});

describe("FeedScreen · read-state-server 能力门分流(未过门 = 旧通路原样)", () => {
  it("低一版 protocol:旧 localStorage 通路照常(写 myssia.feed.states.v1),零 store.state.* 调用", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL - 1));
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    const card = await screen.findByTestId("feed-item-1");
    // 未过门生效的可见标志:title 仍是本地态注记
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("本地态"),
    );
    fireEvent.click(within(card).getByRole("button", { name: "星标" }));
    await waitFor(() => {
      const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.states.v1") ?? "{}");
      expect((persisted as Record<string, { starred?: boolean }>)["dk-1"]?.starred).toBe(true);
    });
    expect(markMock).not.toHaveBeenCalled();
    expect(markAllMock).not.toHaveBeenCalled();
    expect(importMock).not.toHaveBeenCalled();
  });

  it("version 调用失败:按未过门处理,旧通路照常(拒绝不阻断情报流)", async () => {
    versionMock.mockRejectedValue(
      new SidecarRequestError({ code: "sidecar_unavailable", path: "$", message: "sidecar 未起" }),
    );
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    await screen.findByTestId("feed-item-1");
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("本地态"),
    );
    fireEvent.click(screen.getByText("条目 1")); // 标题点击 = 记已读(旧通路本地生效)
    await waitFor(() => expect(screen.queryByTestId("feed-item-1")).toBeNull()); // 未读过滤下离场
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.states.v1") ?? "{}");
    expect((persisted as Record<string, { read?: boolean }>)["dk-1"]?.read).toBe(true);
    expect(markMock).not.toHaveBeenCalled();
    expect(importMock).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// g9-read-all 批(10-04 R1/R2/R4):品类分组组头「本组全部已读」(mark_all 带
// category 精确等值 = 该品类全库含未翻页;未分类组不出钮、时间/不分组无入口、
// 未过门零入口)+ 全库两按钮 inline 二次确认(确认/取消/Esc/失焦四态)
// ---------------------------------------------------------------------------

describe("FeedScreen · g9-read-all(品类批量入口 + 全库二次确认)", () => {
  it("R1 品类组头「本组全部已读」:以该组 category 调 mark_all(精确等值)+ 就地翻转只落该组已加载行;未分类组不出钮(红线)", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 5 });
    const techA = fixtureItem({ category: "tech", title: "技甲" });
    const techB = fixtureItem({ category: "tech", title: "技乙" });
    const news = fixtureItem({ category: "news", title: "闻丙" });
    const bare = fixtureItem({ category: null, title: "无类丁" });
    fresh.storeItemsMock.mockResolvedValue(result([techA, techB, news, bare]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByText("技甲");
    // 就地翻转可观察性:切「全部」过滤(默认未读过滤下翻已读即离场)
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    await screen.findByText("无类丁");
    // 过门生效(title 全库)后切品类分组
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "按品类分组" }));
    await screen.findByTestId("feed-group-tech");

    // 组头钮文案(R4):该品类全库(含未翻页)真话,品类名如实入文案
    const groupButton = screen.getByTestId("feed-group-mark-all-tech");
    expect(groupButton.getAttribute("title")).toContain("全库");
    expect(groupButton.getAttribute("title")).toContain("未翻页");
    expect(groupButton.getAttribute("title")).toContain("tech");
    expect(groupButton.getAttribute("aria-label")).toContain("全库");
    expect(groupButton.getAttribute("aria-label")).toContain("未翻页");
    // 未分类组不出钮(红线:null 传 category 等于全库置位)—— 组头零按钮
    expect(within(screen.getByTestId("feed-group-未分类")).queryByRole("button")).toBeNull();
    // 全场只有品类组出钮:tech/news 各一枚,共 2(未分类不计)
    expect(screen.getAllByTestId(/^feed-group-mark-all-/)).toHaveLength(2);

    // 豁免二次确认:一次点击即执行(确认钮簇不出场)
    fireEvent.click(groupButton);
    await waitFor(() =>
      expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: true, category: "tech" }),
    );
    expect(screen.queryByTestId("feed-confirm-all-group")).toBeNull();
    // 就地翻转只落 tech 组:技甲/技乙已读,闻丙/无类丁不受牵连;不整页重拉
    await waitFor(() =>
      expect(screen.getByTestId(`feed-item-${techA.id}`).getAttribute("data-unread")).toBe("false"),
    );
    expect(screen.getByTestId(`feed-item-${techB.id}`).getAttribute("data-unread")).toBe("false");
    expect(screen.getByTestId(`feed-item-${news.id}`).getAttribute("data-unread")).toBe("true");
    expect(screen.getByTestId(`feed-item-${bare.id}`).getAttribute("data-unread")).toBe("true");
    expect(fresh.storeItemsMock).toHaveBeenCalledTimes(1);
  });

  it("R1 品类组头批量失败:按调用前快照回滚(只回滚该组已加载行,域外组不动)+ feed-mark-error 明示", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    let rejectAll: ((err: unknown) => void) | undefined;
    fresh.markAllMock.mockImplementation(
      () => new Promise((_resolve, reject) => {
        rejectAll = reject;
      }),
    );
    const techRead = fixtureItem({ category: "tech", read: true, title: "技已读甲" });
    const techUnread = fixtureItem({ category: "tech", title: "技未读乙" });
    const newsUnread = fixtureItem({ category: "news", title: "闻未读丙" });
    fresh.storeItemsMock.mockResolvedValue(result([techRead, techUnread, newsUnread]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByText("技未读乙");
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    await screen.findByText("技已读甲");
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "按品类分组" }));
    fireEvent.click(await screen.findByTestId("feed-group-mark-all-tech"));
    await waitFor(() =>
      expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: true, category: "tech" }),
    );
    // 乐观:tech 组两行都翻已读(乙是真翻转);news 组不动
    await waitFor(() =>
      expect(screen.getByTestId(`feed-item-${techUnread.id}`).getAttribute("data-unread")).toBe("false"),
    );
    expect(screen.getByTestId(`feed-item-${techRead.id}`).getAttribute("data-unread")).toBe("false");
    act(() =>
      rejectAll?.(new SidecarRequestError({ code: "store_corrupt", path: "$", message: "库损坏" })),
    );
    // 快照回滚:甲本就已读(回 true)、乙回未读;域外 news 丙全程未读不受牵连
    await waitFor(() =>
      expect(screen.getByTestId(`feed-item-${techUnread.id}`).getAttribute("data-unread")).toBe("true"),
    );
    expect(screen.getByTestId(`feed-item-${techRead.id}`).getAttribute("data-unread")).toBe("false");
    expect(screen.getByTestId(`feed-item-${newsUnread.id}`).getAttribute("data-unread")).toBe("true");
    const error = await screen.findByTestId("feed-mark-error");
    expect(error.textContent).toContain("store_corrupt");
  });

  it("R1 组头入口只属品类分组模式:时间分组组头零批量钮;不分组无组头可挂", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 1 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem({ category: "tech" })]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByText("条目 1");
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );

    // 缺省时间分组:组头只有文案/计数/分隔线,零批量钮(入口不属此模式)
    const timeHeader = screen.getByTestId("feed-group-今天");
    expect(within(timeHeader).queryByRole("button")).toBeNull();
    expect(screen.queryByTestId(/^feed-group-mark-all-/)).toBeNull();

    // 不分组:组头全消,无组头可挂批量钮
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "不分组(平铺)" }));
    await waitFor(() => expect(screen.queryByTestId(/^feed-group-/)).toBeNull());
    expect(screen.queryByTestId(/^feed-group-mark-all-/)).toBeNull();
    expect(fresh.markAllMock).not.toHaveBeenCalled();
  });

  it("R2 全库两按钮二次确认:一次点击只进确认态(零 RPC),再点「确认」才执行;取消 / Esc / 失焦三路退出且零执行", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 99 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByText("条目 1");
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );

    // 一次点击:进确认态 —— 常规两钮让位给「确认/取消」,mark_all 未发;
    // 确认态文案延续全库真话(过门不出现「已加载/本地态」字样,R4)
    fireEvent.click(screen.getByRole("button", { name: "全部标已读" }));
    const confirm = screen.getByRole("button", { name: "确认全部标已读" });
    expect(confirm.getAttribute("title") ?? "").toContain("全库");
    expect(confirm.getAttribute("title") ?? "").not.toContain("已加载");
    expect(confirm.getAttribute("title") ?? "").not.toContain("本地态");
    expect(screen.queryByRole("button", { name: "全部标已读" })).toBeNull();
    expect(screen.queryByRole("button", { name: "全部标未读" })).toBeNull();
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // Esc 退出:回到常规两钮,零执行
    fireEvent.keyDown(window, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(screen.getByRole("button", { name: "全部标已读" })).toBeTruthy();
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // 「取消」退出:零执行
    fireEvent.click(screen.getByRole("button", { name: "全部标已读" }));
    fireEvent.click(screen.getByRole("button", { name: "取消" }));
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // 失焦退出:blur 出确认钮簇即退
    fireEvent.click(screen.getByRole("button", { name: "全部标已读" }));
    fireEvent.blur(screen.getByTestId("feed-confirm-all-group"));
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // 再点执行:确认后 mark_all({marker:"read", value:true})发出;就地翻转已加载行
    fireEvent.click(screen.getByRole("button", { name: "全部标已读" }));
    fireEvent.click(screen.getByRole("button", { name: "确认全部标已读" }));
    await waitFor(() => expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: true }));
    await waitFor(() => expect(screen.getByText("0 / 2 条")).toBeTruthy());
  });

  it("未过门:品类分组组头无批量入口(旧通路无品类作用域,store.state.* 零调用)", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL - 1));
    storeItemsMock.mockResolvedValue(result([fixtureItem({ category: "tech" }), fixtureItem({ category: null })]));
    renderScreen();
    await screen.findByText("条目 1");
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "按品类分组" }));
    await screen.findByTestId("feed-group-tech");
    // 未过门:全屏无品类组头批量钮;store.state.* 全家零调用
    expect(screen.queryByTestId(/^feed-group-mark-all-/)).toBeNull();
    expect(within(screen.getByTestId("feed-group-tech")).queryByRole("button")).toBeNull();
    expect(markAllMock).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// D4 纯函数(api.ts):groupFeedItems 时间分桶边界 / categoryColor 稳定性
// ---------------------------------------------------------------------------

describe("feed D4 纯函数(api.ts)", () => {
  it("groupFeedItems:四桶按 今天/昨天/7天内/更早 边界落位,空桶不出组", () => {
    const now = new Date(2026, 9, 3, 12, 0); // 2026-10-03 正午(本地时区)
    const at = (iso: string) => fixtureItem({ first_seen: iso });
    const items = [
      at("2026-10-03T10:00:00"), // 今天
      at("2026-10-03T00:00:00"), // 今天(0 点边界含)
      at("2026-10-02T23:59:00"), // 昨天
      at("2026-09-30T10:00:00"), // 7 天内
      at("2026-09-26T00:00:00"), // 7 天内(7 天窗下边界含)
      at("2026-09-25T23:59:00"), // 更早
      at("不是时间"), // 更早(first_seen 无效归更早)
    ];
    const groups = groupFeedItems(items, now);
    expect(groups.map((group) => group.label)).toEqual(["今天", "昨天", "7 天内", "更早"]);
    expect(groups[0].items).toHaveLength(2);
    expect(groups[1].items).toHaveLength(1);
    expect(groups[2].items).toHaveLength(2);
    expect(groups[3].items).toHaveLength(2);
  });

  it("groupFeedItems:空桶过滤 + 桶内顺序保持(新→旧原序)", () => {
    const now = new Date(2026, 9, 3, 12, 0);
    const a = fixtureItem({ first_seen: "2026-10-03T09:00:00" });
    const b = fixtureItem({ first_seen: "2026-10-03T08:00:00" });
    const c = fixtureItem({ first_seen: "2026-09-01T08:00:00" });
    const groups = groupFeedItems([a, b, c], now);
    expect(groups.map((group) => group.key)).toEqual(["today", "earlier"]);
    expect(groups[0].items).toEqual([a, b]);
    expect(groups[1].items).toEqual([c]);
  });

  it("categoryColor:同品类恒同色(6 位 hex 色板内),空品类 null", () => {
    expect(categoryColor(null)).toBeNull();
    expect(categoryColor(undefined)).toBeNull();
    for (const category of ["ai-news", "stocks", "news", "wool", "monitor", "tech"]) {
      const color = categoryColor(category);
      expect(color).toMatch(/^#[0-9a-f]{6}$/);
      expect(categoryColor(category)).toBe(color); // 稳定散列:两次调用同色
    }
  });
});

// ---------------------------------------------------------------------------
// fe-small-batch 纯函数(api.ts):appendWatchlistKeyword 文本手术四形态 /
// 查重零写入 / id 行不动(跨文件 id 查重不破);setMarkerBulk 批量置位
// ---------------------------------------------------------------------------

describe("feed fe-small-batch 纯函数(api.ts)", () => {
  it("appendWatchlistKeyword 流式列表:闭括号前追加,尾随注释与其余行逐字节不动(id 行原样)", () => {
    const content = "# 顶注\nid: ai-news\nname: AI资讯\nwatchlist:\n  keywords: [LLM, Agent]  # 关注词\n  mute: [广告]\n";
    const outcome = appendWatchlistKeyword(content, "多模态");
    expect(outcome).toEqual({
      ok: true,
      content: "# 顶注\nid: ai-news\nname: AI资讯\nwatchlist:\n  keywords: [LLM, Agent, 多模态]  # 关注词\n  mute: [广告]\n",
    });
  });

  it("appendWatchlistKeyword 流式空表 []:首词入表;词已在(流式)→ already_present", () => {
    expect(appendWatchlistKeyword("watchlist:\n  keywords: []\n", "首词")).toEqual({
      ok: true,
      content: "watchlist:\n  keywords: [首词]\n",
    });
    expect(appendWatchlistKeyword("watchlist:\n  keywords: [LLM, Agent]\n", "LLM")).toEqual({
      ok: false,
      reason: "already_present",
    });
  });

  it("appendWatchlistKeyword 块式列表:末项后追加同缩进行,后续节点(mute)不动;词已在(块式)→ already_present", () => {
    const content = "id: ai-news\nwatchlist:\n  keywords:\n    - LLM\n    - Agent\n  mute:\n    - 广告\n";
    expect(appendWatchlistKeyword(content, "新词")).toEqual({
      ok: true,
      content: "id: ai-news\nwatchlist:\n  keywords:\n    - LLM\n    - Agent\n    - 新词\n  mute:\n    - 广告\n",
    });
    expect(appendWatchlistKeyword(content, "Agent")).toEqual({ ok: false, reason: "already_present" });
  });

  it("appendWatchlistKeyword 空值键行:keywords: 直接起首项;null 值先落定键行再起项", () => {
    expect(appendWatchlistKeyword("watchlist:\n  keywords:\n  mute: []\n", "首词")).toEqual({
      ok: true,
      content: "watchlist:\n  keywords:\n    - 首词\n  mute: []\n",
    });
    expect(appendWatchlistKeyword("watchlist:\n  keywords: null\n", "落定词")).toEqual({
      ok: true,
      content: "watchlist:\n  keywords:\n    - 落定词\n",
    });
  });

  it("appendWatchlistKeyword 无 keywords 键:有 watchlist 键补块;连 watchlist 都没有则末尾整节追加", () => {
    expect(appendWatchlistKeyword("id: x\nwatchlist:\n  mute: [广告]\n", "补词")).toEqual({
      ok: true,
      content: "id: x\nwatchlist:\n  keywords:\n    - 补词\n  mute: [广告]\n",
    });
    expect(appendWatchlistKeyword("id: x\n", "末词")).toEqual({
      ok: true,
      content: "id: x\nwatchlist:\n  keywords:\n    - 末词\n",
    });
    expect(appendWatchlistKeyword("", "孤词")).toEqual({
      ok: true,
      content: "watchlist:\n  keywords:\n    - 孤词\n",
    });
  });

  it("appendWatchlistKeyword 边界:标量值 keywords_unparsed / 空词 / 超长(>64);特殊字符词双引号转义", () => {
    expect(appendWatchlistKeyword("watchlist:\n  keywords: LLM\n", "新词")).toEqual({
      ok: false,
      reason: "keywords_unparsed",
    });
    expect(appendWatchlistKeyword("watchlist:\n  keywords: []\n", "  ")).toEqual({ ok: false, reason: "empty_keyword" });
    expect(appendWatchlistKeyword("watchlist:\n  keywords: []\n", "词".repeat(65))).toEqual({
      ok: false,
      reason: "keyword_too_long",
    });
    const quoted = appendWatchlistKeyword("watchlist:\n  keywords: []\n", "a,b:c");
    expect(quoted).toEqual({ ok: true, content: "watchlist:\n  keywords: [\"a,b:c\"]\n" });
  });

  it("setMarkerBulk:全部置 read=true 逐条落键;置回 false 时无其他标记的键剪除", () => {
    const items = [fixtureItem(), fixtureItem()];
    const states = { [items[1].dedup_key]: { starred: true } };
    const allRead = setMarkerBulk(items, states, "read", true);
    expect(allRead[items[0].dedup_key]).toEqual({ read: true });
    expect(allRead[items[1].dedup_key]).toEqual({ starred: true, read: true });
    const backUnread = setMarkerBulk(items, allRead, "read", false);
    expect(backUnread[items[0].dedup_key]).toBeUndefined();
    // 有其他标记的键保留显式 read:false(与 toggleMarker 的存储纪律一致:
    // 显式 false 与缺省同义,只有三态全 false 才剪键)
    expect(backUnread[items[1].dedup_key]).toEqual({ starred: true, read: false });
  });
});

// ---------------------------------------------------------------------------
// interaction-batch 纯函数(api.ts):sortUnreadFirst 稳定保序 /
// groupFeedItemsByCategory 品类分组 / load·saveFeedDisplay 本地持久纪律
// ---------------------------------------------------------------------------

describe("feed interaction-batch 纯函数(api.ts)", () => {
  it("sortUnreadFirst:未读浮前已读沉底,两类各自稳定保序;全同态原序零变动", () => {
    const a = fixtureItem();
    const b = fixtureItem();
    const c = fixtureItem();
    const d = fixtureItem();
    const states = {
      [b.dedup_key]: { read: true },
      [d.dedup_key]: { read: true },
    };
    expect(sortUnreadFirst([a, b, c, d], states).map((item) => item.dedup_key)).toEqual([
      a.dedup_key,
      c.dedup_key,
      b.dedup_key,
      d.dedup_key,
    ]);
    // 全未读 / 全已读:原序不变
    expect(sortUnreadFirst([d, c], {}).map((item) => item.id)).toEqual([d.id, c.id]);
    const allRead = { [d.dedup_key]: { read: true }, [c.dedup_key]: { read: true } };
    expect(sortUnreadFirst([d, c], allRead).map((item) => item.id)).toEqual([d.id, c.id]);
    // 不改原数组(返回新序)
    const source = [b, a];
    sortUnreadFirst(source, { [a.dedup_key]: { read: true } });
    expect(source.map((item) => item.id)).toEqual([b.id, a.id]);
  });

  it("groupFeedItemsByCategory:品类按首次出现出组,组内原序,无品类归「未分类」色 null,色同 categoryColor", () => {
    const t1 = fixtureItem({ category: "tech" });
    const n1 = fixtureItem({ category: "news" });
    const t2 = fixtureItem({ category: "tech" });
    const bare = fixtureItem({ category: null });
    const groups = groupFeedItemsByCategory([t1, n1, t2, bare]);
    expect(groups.map((group) => group.key)).toEqual(["tech", "news", null]);
    expect(groups[0].items).toEqual([t1, t2]); // 组内保持传入原序
    expect(groups[1].items).toEqual([n1]);
    expect(groups[2].label).toBe("未分类");
    expect(groups[2].color).toBeNull(); // 无品类零色件
    expect(groups[0].color).toBe(categoryColor("tech")); // 色同源
    expect(groups[0].label).toBe("tech");
    // 空入空出
    expect(groupFeedItemsByCategory([])).toEqual([]);
  });

  it("loadFeedDisplay / saveFeedDisplay:往返持久;损坏 JSON/非对象回缺省;字段非法逐字段回缺省;storage 缺席 = 缺省", () => {
    const storage = memoryStorage();
    expect(loadFeedDisplay(storage)).toEqual(DEFAULT_FEED_DISPLAY); // 无键 = 缺省

    saveFeedDisplay({ unreadFirst: true, groupMode: "category" }, storage);
    expect(loadFeedDisplay(storage)).toEqual({ unreadFirst: true, groupMode: "category" });

    storage.setItem("myssia.feed.display.v1", "{oops"); // JSON 损坏
    expect(loadFeedDisplay(storage)).toEqual(DEFAULT_FEED_DISPLAY);
    storage.setItem("myssia.feed.display.v1", JSON.stringify(["bad", "shape"])); // 非对象
    expect(loadFeedDisplay(storage)).toEqual(DEFAULT_FEED_DISPLAY);

    // 单字段非法逐字段回落,合法字段保留
    storage.setItem("myssia.feed.display.v1", JSON.stringify({ unreadFirst: "yes", groupMode: "bogus" }));
    expect(loadFeedDisplay(storage)).toEqual(DEFAULT_FEED_DISPLAY);
    storage.setItem("myssia.feed.display.v1", JSON.stringify({ unreadFirst: true }));
    expect(loadFeedDisplay(storage)).toEqual({ unreadFirst: true, groupMode: "time" });
    storage.setItem("myssia.feed.display.v1", JSON.stringify({ groupMode: "none" }));
    expect(loadFeedDisplay(storage)).toEqual({ unreadFirst: false, groupMode: "none" });

    expect(loadFeedDisplay(null)).toEqual(DEFAULT_FEED_DISPLAY); // storage 缺席
  });
});

// ---------------------------------------------------------------------------
// read-state-server 纯函数(api.ts):statesFromItems 条目派生状态源
// ---------------------------------------------------------------------------

describe("feed read-state-server 纯函数(api.ts)", () => {
  it("statesFromItems:三键真值产键、全缺省/false 不产键(与 loadFeedStates 缺省语义对齐);键 = itemKey 同源", () => {
    const read = fixtureItem({ read: true });
    const all = fixtureItem({ read: true, starred: true, later: true });
    const bare = fixtureItem();
    const explicitFalse = fixtureItem({ read: false, starred: false, later: false });
    const noDedup = fixtureItem({ id: 9, dedup_key: "", starred: true }); // itemKey 兜底形态 id:<n>
    const states = statesFromItems([read, all, bare, explicitFalse, noDedup]);
    expect(states[read.dedup_key]).toEqual({ read: true });
    expect(states[all.dedup_key]).toEqual({ read: true, starred: true, later: true });
    expect(states[bare.dedup_key]).toBeUndefined();
    expect(states[explicitFalse.dedup_key]).toBeUndefined();
    expect(states["id:9"]).toEqual({ starred: true });
    expect(statesFromItems([])).toEqual({}); // 空入空出
  });
});
