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
 * category 精确等值;未分类组不出钮、时间/不分组无组头入口)/
 * 全库两按钮 inline 二次确认(一次点击进确认态,再点执行;取消/Esc/失焦
 * 退出零执行);品类批量失败按快照只回滚作用域内行(域外组不动)。
 * topbar-cleanup 归位批(10-04):屏内品类下拉(health().plugins 词汇源,
 * value = 品类 id 服务端精确等值,「全部品类」= 不传参;不再吃 Outlet
 * context)+ 工具条一行收纳(KsFilter:品类下拉 + 读态分段 + 搜索 + 刷新
 * 同容器,刷新自页头迁入);纯函数 categoryOptionsFromHealth。
 * fe-gap-leftovers 批(10-05 ①):later 到期重现——稍后读条目放入超
 *  LATER_RESURFACE_DAYS(7 天,与时间分组「更早」同界)即并入未读视图
 *  (服务端通路屏测 + 纯函数 isLaterResurface/applyFeedFilter 边界);
 *  书签 title 知会到期规则。
 * feed-channel-groups 批(10-06,主人令「情报流也要分渠道」+「不同渠道
 *  表现的方式不一样」+「不停地过信息日志,每天凌晨 3 点清零」):品类分组
 *  下渠道二级分组 / 五档差异化卡面(telegram 气泡 · watch 变更事件 ·
 *  document 日报 markdown · deal 价格行 · news 现状)/ 实时滚动
 *  (completed·cron.completed 事件前插新键)+ 当日窗 03:00 视图清零
 *  (滚动流受窗,星标/稍后读跨窗);纯函数 channelKindOf /
 *  engineMapFromHealth / groupFeedItemsByChannel / dealPriceView /
 *  dayWindowStart / inDayWindow / mergeFreshItems。
 */
import { cleanup, fireEvent, render, screen, waitFor, within, act } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterAll, beforeAll, afterEach, beforeEach, describe, expect, it, vi } from "vitest";

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
  applyFeedFilter,
  appendWatchlistKeyword,
  categoryColor,
  categoryOptionsFromHealth,
  channelKindOf,
  dayWindowStart,
  DEFAULT_FEED_DISPLAY,
  dealPriceView,
  engineMapFromHealth,
  groupFeedItems,
  groupFeedItemsByCategory,
  groupFeedItemsByChannel,
  inDayWindow,
  isLaterResurface,
  LATER_RESURFACE_DAYS,
  loadFeedDisplay,
  mergeFreshItems,
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

/** 三级下钻(10-06):进入「全部条目 · 滚动流」L3(全局流 = 原平铺视图语义) */
async function openAllStream() {
  fireEvent.click(await screen.findByTestId("feed-drill-all"));
}

/** 惯用入口:渲染 L1 + 下钻全局滚动流(卡片/工具条用例的公共前置) */
async function renderStream() {
  renderScreen();
  await openAllStream();
}

/** 品类下拉选项用 PluginReport 夹具(形状对齐 types.ts;字段按需覆写) */
function pluginEntry(overrides: Partial<HealthResult["plugins"][number]> = {}): HealthResult["plugins"][number] {
  return {
    file: "/home/plugins/x.yaml",
    id: "x",
    name: null,
    schedule: null,
    timezone: null,
    push_channels: [],
    loaded: true,
    load_errors: null,
    sources: [],
    ...overrides,
  };
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

// Radix Select 2.x 在 jsdom 里开品类下拉需要的指针捕获/滚动桩(topbar-cleanup
// 归位批;同款见 logs-screen.test.tsx / dashboard-screen.test.tsx beforeAll)。
// scrollIntoView 落 Element.prototype(与下方 j/k 用例的 spy 同层 —— 落
// HTMLElement.prototype 会遮蔽该 spy,断言不到「最近侧滚入」调用)
beforeAll(() => {
  window.HTMLElement.prototype.hasPointerCapture = () => false;
  window.HTMLElement.prototype.releasePointerCapture = () => {};
  Element.prototype.scrollIntoView = () => {};
});
afterAll(() => {
  // 桩留在原型上会外溢到同 worker 的其他测试文件,退出时还原
  delete (window.HTMLElement.prototype as Partial<HTMLElement>).hasPointerCapture;
  delete (window.HTMLElement.prototype as Partial<HTMLElement>).releasePointerCapture;
  delete (Element.prototype as Partial<Element>).scrollIntoView;
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
    await renderStream();

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
    await renderStream();

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
    await renderStream();

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
    await renderStream();
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
    await openAllStream();
    await screen.findByText("条目 1");
    const card = screen.getByTestId(`feed-item-${item.id}`);
    fireEvent.click(within(card).getByRole("button", { name: "星标" }));
    unmount();

    await renderStream();
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
    await renderStream();

    const loadMore = await screen.findByRole("button", { name: "加载更早的条目" });
    expect(screen.getByText("50 / 50 条")).toBeTruthy(); // 默认「未读」过滤:计数 50/50
    fireEvent.click(loadMore);

    // 翻页请求带上页最旧条目的 (first_seen, id) 复合游标(C1:同刻条目也能推进;
    // 三级下钻后调用序 = L1 首页 → 下钻 L3-all 同参重查 → 翻页,按形断言)
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenCalledWith({ limit: 50, before: cursor, before_id: cursorId }));
    expect(storeItemsMock).toHaveBeenCalledWith({ limit: 50 });
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
    await renderStream();
    const loadMore = await screen.findByRole("button", { name: "加载更早的条目" });
    fireEvent.click(loadMore);

    await waitFor(() => expect(storeItemsMock.mock.calls.length).toBeGreaterThanOrEqual(3));
    // 追加 0 条 → 判停按钮消失;仍是 50 张卡、无重复(L1 首页 + 下钻重查 + 翻页 ≥3 发)
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
  // feed-ux 批(10-03-feed-ux)+ topbar-cleanup 品类归位(10-04):品类接线 /
  // G1 搜索 / G2 展开与打开原文 / G3 导出
  // -------------------------------------------------------------------------

  it("三级下钻作用域(10-06):L1 品类 → L2 渠道 → L3 渠道流 = store.items 带 category+source 精确等值;面包屑回退复称全库", async () => {
    const newsA = fixtureItem({ category: "ai-news", source: "openai-news", title: "闻甲" });
    const newsB = fixtureItem({ category: "ai-news", source: "hf-blog", title: "闻乙" });
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(
          [newsA, newsB].filter(
            (item) =>
              (!params?.category || item.category === params.category) &&
              (!params?.source || item.source === params.source),
          ),
        ),
      ),
    );
    renderScreen();

    // L1:品类行(health 词汇源回显名称)→ 点击进 L2
    fireEvent.click(await screen.findByTestId("feed-drill-cat-ai-news"));
    const channel = await screen.findByTestId("feed-drill-ch-openai-news");
    expect(within(channel).getByText("openai-news")).toBeTruthy();
    expect(within(channel).getByText(/新闻渠道/)).toBeTruthy();

    // L2 → L3:渠道流查询带 category+source 精确等值
    fireEvent.click(channel);
    await screen.findByText("闻甲");
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith({ limit: 50, category: "ai-news", source: "openai-news" }),
    );
    expect(screen.queryByText("闻乙")).toBeNull(); // 渠道流只回本渠道行

    // 渠道 × 搜索叠加:query 随游标透传,作用域行如实注明品类 × 渠道
    fireEvent.change(screen.getByLabelText("搜索条目"), { target: { value: "GLM" } });
    fireEvent.keyDown(screen.getByLabelText("搜索条目"), { key: "Enter" });
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith({
        limit: 50,
        category: "ai-news",
        source: "openai-news",
        query: "GLM",
      }),
    );
    expect(screen.getByTestId("feed-search-scope").textContent).toContain("ai-news");
    expect(screen.getByTestId("feed-search-scope").textContent).toContain("openai-news");

    // 面包屑回退:渠道 → 品类(深审 F1:L2 计数源 = 品类查询页,source 摘除,
    // 概览面不带 query——搜索词只属 L3 流)→ 情报流 L1
    fireEvent.click(screen.getByTestId("feed-crumb-category"));
    await waitFor(() => {
      const last = storeItemsMock.mock.calls[storeItemsMock.mock.calls.length - 1][0] as StoreItemsParams;
      expect(last.source).toBeUndefined();
      expect(last.category).toBe("ai-news");
      expect(last.query).toBeUndefined();
    });
    // L2 头部可见(渠道行);回 L1:全局行在场
    expect(await screen.findByTestId("feed-drill-ch-openai-news")).toBeTruthy();
    fireEvent.click(screen.getByTestId("feed-crumb-home"));
    expect(await screen.findByTestId("feed-drill-all")).toBeTruthy();
  });

  it("L1 品类行词汇源:health().plugins id 去重 + 名称回显 + null id 不入;health 失败仍列已加载条目品类", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem({ category: "tech" })]));
    const first = renderScreen();

    // 缺省 health(单插件 ai-news)+ 已加载条目品类 tech:L1 两行(选项序在前)
    const rowIds = () =>
      screen.getAllByTestId(/^feed-drill-cat-/).map((node) => node.getAttribute("data-testid"));
    await waitFor(() => expect(rowIds()).toEqual(["feed-drill-cat-ai-news", "feed-drill-cat-tech"]));
    expect(screen.getByTestId("feed-drill-cat-ai-news").textContent).toContain("AI资讯"); // 名称回显
    first.unmount();

    // 多插件(同 id 去重首现优先 / null id 不入 / name 缺省回 id):重挂载拉新清单
    healthMock.mockResolvedValue(
      healthResult({
        plugins: [
          pluginEntry({ file: "/home/plugins/stocks.yaml", id: "stocks", name: null }),
          pluginEntry({ file: "/home/plugins/ai-news.yaml", id: "ai-news", name: "AI资讯" }),
          pluginEntry({ file: "/home/plugins/dup.yaml", id: "ai-news", name: "重复id后现" }),
          pluginEntry({ file: "/home/plugins/broken.yaml", id: null, name: "坏插件" }),
        ],
      }),
    );
    const second = renderScreen();
    await waitFor(() =>
      expect(screen.getAllByTestId(/^feed-drill-cat-/).map((node) => node.getAttribute("data-testid"))).toEqual([
        "feed-drill-cat-ai-news",
        "feed-drill-cat-stocks",
        "feed-drill-cat-tech",
      ]),
    );
    expect(screen.getByTestId("feed-drill-cat-stocks").textContent).toContain("stocks"); // name 缺省回 id
    second.unmount();

    // health 失败:不拦情报流,品类行收敛为已加载条目品类(选项词表空)
    healthMock.mockRejectedValue(new Error("sidecar 未连接"));
    renderScreen();
    await waitFor(() =>
      expect(screen.getAllByTestId(/^feed-drill-cat-/).map((node) => node.getAttribute("data-testid"))).toEqual([
        "feed-drill-cat-tech",
      ]),
    );
  });

  it("工具条一行收纳(KsFilter):品类下拉 + 读态分段 + 搜索 + 刷新同容器;刷新钮(KsFilter refresh 位,自页头迁入)重发查询", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderStream();
    await screen.findByText("条目 1");

    // 一行工具条:读态分段组 / 搜索框 / 刷新钮同容器(品类选择 = L1/L2
    // 层级本体,下拉退役 —— 10-06 三级下钻)
    const toolbar = screen.getByTestId("feed-toolbar");
    expect(within(toolbar).queryByRole("combobox")).toBeNull();
    const segmented = within(toolbar).getByRole("group", { name: "读态过滤" });
    for (const label of ["未读", "星标", "稍后读", "全部"]) {
      expect(within(segmented).getByRole("button", { name: `过滤:${label}` })).toBeTruthy();
    }
    expect(within(toolbar).getByLabelText("搜索条目")).toBeTruthy();
    expect(within(toolbar).getByRole("button", { name: "显示选项" })).toBeTruthy();

    // 刷新迁入工具条(全屏仅此一枚「刷新」钮):点击重发 store.items
    expect(screen.getAllByRole("button", { name: "刷新" })).toHaveLength(1);
    const calls = storeItemsMock.mock.calls.length;
    fireEvent.click(within(toolbar).getByRole("button", { name: "刷新" }));
    await waitFor(() => expect(storeItemsMock.mock.calls.length).toBeGreaterThan(calls));
  });

  it("G1 搜索:Enter 即时提交 → query 随首页与翻页透传;计数行双层如实", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderStream();
    await screen.findByText("条目 1");

    fireEvent.change(screen.getByLabelText("搜索条目"), { target: { value: "GLM" } });
    fireEvent.keyDown(screen.getByLabelText("搜索条目"), { key: "Enter" });

    await waitFor(() => expect(storeItemsMock).toHaveBeenLastCalledWith({ limit: 50, query: "GLM" }));
    expect(await screen.findByTestId("feed-search-scope")).toBeTruthy();
    expect(screen.getByTestId("feed-search-scope").textContent).toContain("GLM");
  });

  it("G1 搜索空态:零命中给专属空态文案(不再误导为「情报流是空的」)", async () => {
    let empty = false;
    storeItemsMock.mockImplementation(() => Promise.resolve(result(empty ? [] : [fixtureItem()])));
    await renderStream();
    await screen.findByText("条目 1");
    empty = true;
    fireEvent.change(screen.getByLabelText("搜索条目"), { target: { value: "不存在的词" } });
    fireEvent.keyDown(screen.getByLabelText("搜索条目"), { key: "Enter" });

    expect(await screen.findByTestId("feed-search-empty")).toBeTruthy();
    expect(screen.queryByText("情报流还是空的")).toBeNull();
  });

  it("R1 Mod+F:⌘F/Ctrl+F 拦截浏览器查找(preventDefault)改聚焦搜索框并全选词面", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
    await screen.findByText("条目 1");

    fireEvent.click(within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "打开原文" }));
    expect(await screen.findByTestId("feed-open-error")).toBeTruthy();
    expect(screen.getByTestId("feed-open-error").textContent).toContain("shell 未授权");
  });

  it("G3 导出:选格式 → dialog.save 默认名带日期 → feed.export 带当前过滤 → 回显 path/count", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    await renderStream();
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
    await renderStream();
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

  it("G3 导出组在工具条右端可达(10-05 自 PageHeader.actions 迁入;无头化回归闸)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderStream();
    await screen.findByText("条目 1");

    // 无头化(d9ae353)后 PageHeader 返回 null,actions 不再渲染 —— 导出组
    // 必须落在 feed-toolbar 内才是可达入口;且次序在刷新钮之后(工具条右端)
    const toolbar = within(screen.getByTestId("feed-toolbar"));
    expect(toolbar.getByRole("group", { name: "导出格式" })).toBeTruthy();
    expect(toolbar.getByRole("button", { name: "JSONL" })).toBeTruthy();
    expect(toolbar.getByRole("button", { name: "CSV" })).toBeTruthy();
    const refresh = toolbar.getByRole("button", { name: "刷新" });
    const exportButton = toolbar.getByRole("button", { name: "导出当前视图" });
    expect(refresh.compareDocumentPosition(exportButton) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();

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
    await renderStream();
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
    // F1 后挂载并发两路(全局流 + 按品类概览):全部挂起才不误卸骨架
    const resolvers: Array<(value: StoreItemsResult) => void> = [];
    storeItemsMock.mockImplementation(
      () => new Promise<StoreItemsResult>((resolve) => {
        resolvers.push(resolve);
      }),
    );
    renderScreen();

    expect(await screen.findByTestId("feed-loading")).toBeTruthy();
    expect(screen.queryByTestId(/^feed-item-/)).toBeNull();
    act(() => resolvers.splice(0).forEach((resolve) => resolve(result([fixtureItem()]))));
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    await waitFor(() => expect(resolvers.length).toBeGreaterThan(0));
    act(() => resolvers.splice(0).forEach((resolve) => resolve(result([fixtureItem()]))));
    await screen.findByTestId("feed-item-1");
    expect(screen.queryByTestId("feed-loading")).toBeNull();
  });

  it("D4 错误态:结构化错误卡带重试按钮,点击重发 store.items 并恢复", async () => {
    storeItemsMock.mockRejectedValueOnce(
      new SidecarRequestError({ code: "store_corrupt", path: "params.db", message: "库文件损坏" }),
    );
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();

    const banner = await screen.findByTestId("feed-error");
    expect(banner.textContent).toContain("store_corrupt");
    // 错误态与空态互斥(质检修):错误卡在场时不得再落入空态 CTA
    // (store 损坏下「运行第一个插件」必失败,两卡叠加语义矛盾)
    expect(screen.queryByTestId("feed-run-cta")).toBeNull();
    expect(screen.queryByText("情报流还是空的")).toBeNull();
    fireEvent.click(within(banner).getByRole("button", { name: "重试" }));
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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

  it("G9 无未读时批量按钮禁用(过门读态派生;空库 L3 无入口 = L1 空态 CTA 另测)", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    storeItemsMock.mockResolvedValue(result([fixtureItem({ read: true }), fixtureItem({ read: true })]));
    await renderStream();
    // 默认「未读」过滤下全已读即离场;先切「全部」保卡片在场再断言禁用
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    await screen.findByText("条目 1");
    await screen.findByText("条目 2");
    expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("disabled")).not.toBeNull();
  });

  it("P2⑤:搜索框焦点环归全局 :focus-visible 体系(无局部 ring-1/focus-visible 覆写)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderStream();
    await screen.findByText("条目 1");
    const input = screen.getByLabelText("搜索条目");
    expect(input.className).not.toContain("ring-1");
    expect(input.className).not.toContain("focus-visible");
  });

  it("G12 沉淀为关键词:面板只列 parse_ok 目标,词面默认条目标题;read(mtime)→ 手术 → save → 回执带 .bak", async () => {
    const item = fixtureItem({ title: "GLM-5 发布" });
    storeItemsMock.mockResolvedValue(result([item]));
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
      await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
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
    await renderStream();
    await screen.findByText("技一");

    // 缺省 = 时间四桶(既有 D4 行为不动)
    expect(screen.getByTestId("feed-group-今天").textContent).toContain("4 条");

    // 三级下钻(10-06)后品类分组退役:菜单只有 时间/不分组 两档;品类维度
    // = L1/L2 层级本体(见 L1/L2 下钻用例),组头色点随品类分组一并退役
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    const menu = await screen.findByRole("menu");
    expect(within(menu).queryByRole("menuitem", { name: "按品类分组" })).toBeNull();
    expect(within(menu).getByRole("menuitem", { name: "时间分组(今天 / 昨天 / 7 天内 / 更早)" }).querySelector("svg")).not.toBeNull();

    // 不分组:组头全消、四卡平铺
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "不分组(平铺)" }));
    await waitFor(() => expect(screen.queryByTestId(/^feed-group-/)).toBeNull());
    expect(screen.getAllByTestId(/^feed-item-/)).toHaveLength(4);
    expect(screen.getByTestId("feed-flat-list")).toBeTruthy();

    // 持久:groupMode = none(重开菜单勾选态同步)
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.display.v1") ?? "{}");
    expect((persisted as { groupMode?: string }).groupMode).toBe("none");
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    const menu2 = await screen.findByRole("menu");
    expect(within(menu2).getByRole("menuitem", { name: "不分组(平铺)" }).querySelector("svg")).not.toBeNull();
    expect(within(menu2).getByRole("menuitem", { name: "时间分组(今天 / 昨天 / 7 天内 / 更早)" }).querySelector("svg")).toBeNull();
  });

  it("右键菜单:四动作齐(打开原文/复制链接/标记已读/沉淀为关键词),动作生效且选后自闭", async () => {
    const item = fixtureItem({ url: "https://example.com/story" });
    storeItemsMock.mockResolvedValue(result([item]));
    // navigator.clipboard 在 jsdom 缺席:注入 stub(测后还原)
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
    try {
      await renderStream();
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
    await renderStream();
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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
    // L1 首页 + 下钻 L3-all 同参重查 = 2 发流查询(F1 概览按品类另发,不计),
    // mark_all 后不再整页重拉
    const streamCalls = fresh.storeItemsMock.mock.calls.filter(
      ([params]) => !(params as StoreItemsParams | undefined)?.category,
    );
    expect(streamCalls.length).toBe(2);
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    await screen.findByTestId("feed-item-1");
    // 等能力门真正翻到服务端通路(title 现全库语义)再断言不发
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );
    expect(fresh.importMock).not.toHaveBeenCalled();
  });

  it("① later 到期重现:已读+稍后读超窗条目回未读流(书签 title 知会);未到期只在稍后读桶", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    const daysAgoIso = (days: number) => new Date(Date.now() - days * 86_400_000).toISOString();
    const due = fixtureItem({
      id: 101,
      title: "到期稍后读条目",
      read: true,
      later: true,
      first_seen: daysAgoIso(LATER_RESURFACE_DAYS + 3),
    });
    const notDue = fixtureItem({
      id: 102,
      title: "未到期稍后读条目",
      read: true,
      later: true,
      first_seen: daysAgoIso(1),
    });
    fresh.storeItemsMock.mockResolvedValue(result([due, notDue]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    // 默认「未读」视图:两条都已读——到期条目重现,未到期不现;计数行如实
    await screen.findByText("到期稍后读条目");
    expect(screen.queryByText("未到期稍后读条目")).toBeNull();
    expect(screen.getByText("1 / 2 条")).toBeTruthy();
    // 书签 title 知会到期规则(a11y label 兄弟位)
    const bookmark = within(screen.getByTestId("feed-item-101")).getByRole("button", { name: "稍后读" });
    expect(bookmark.getAttribute("title")).toContain("回到未读");
    // 稍后读桶:两条全量可见(桶内不分到期与否)
    fireEvent.click(screen.getByRole("button", { name: "过滤:稍后读" }));
    expect(screen.getByText("到期稍后读条目")).toBeTruthy();
    expect(screen.getByText("未到期稍后读条目")).toBeTruthy();
    expect(screen.getByText("2 / 2 条")).toBeTruthy();
  });
});

describe("FeedScreen · read-state-server 能力门分流(未过门 = 旧通路原样)", () => {
  it("低一版 protocol:旧 localStorage 通路照常(写 myssia.feed.states.v1),零 store.state.* 调用", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL - 1));
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderStream();
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
    await renderStream();
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
  it("R1 L2 品类头「本品类窗内已读」(深审 F3):逐键置位窗内已加载行(mark keys),不走全库 mark_all;UI 所见 = 实际作用域;反向出口同门", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markMock.mockResolvedValue({ updated: 2 });
    const start = dayWindowStart();
    const techA = fixtureItem({ category: "tech", source: "t-a", title: "技甲" });
    const techB = fixtureItem({ category: "tech", source: "t-b", title: "技乙" });
    const techStale = fixtureItem({
      category: "tech",
      source: "t-a",
      title: "技窗外旧",
      first_seen: new Date(start.getTime() - 3_600_000).toISOString(),
    });
    fresh.storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result([techA, techB, techStale].filter((item) => !params?.category || item.category === params.category))),
    );
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    // L1 → L2(tech):头部出窗内批量钮(F3 作用域收窄后)
    fireEvent.click(await screen.findByTestId("feed-drill-cat-tech"));
    const groupButton = await screen.findByTestId("feed-category-mark-all");
    const reverseButton = await screen.findByTestId("feed-category-mark-unread");
    // 钮文案:作用域=当日窗内已加载行(title 如实,不再宣称全库)
    expect(groupButton.getAttribute("title")).toContain("当日窗内已加载");
    expect(groupButton.getAttribute("title")).toContain("2");
    expect(groupButton.getAttribute("title")).not.toContain("全库");
    expect(reverseButton.getAttribute("title")).toContain("反向出口");
    // 未读计数可观察:L2 行先见 未读 2(窗外旧条目不计入行计数)
    expect(screen.getByTestId("feed-drill-ch-t-a").textContent).toContain("未读 1");
    expect(screen.getByTestId("feed-drill-ch-t-b").textContent).toContain("未读 1");

    // 一次点击即执行:逐键置位**窗内两键**(窗外旧键不入),零 mark_all
    fireEvent.click(groupButton);
    await waitFor(() =>
      expect(fresh.markMock).toHaveBeenCalledWith({ keys: [techA.dedup_key, techB.dedup_key], marker: "read", value: true }),
    );
    expect(fresh.markAllMock).not.toHaveBeenCalled();
    expect(screen.queryByTestId("feed-confirm-all-group")).toBeNull();
    // 就地翻转只落窗内行(渠道行未读归零)
    await waitFor(() => expect(screen.getByTestId("feed-drill-ch-t-a").textContent).toContain("未读 0"));
    expect(screen.getByTestId("feed-drill-ch-t-b").textContent).toContain("未读 0");

    // 反向出口:窗内未读逐键翻回(误触可逆)
    fireEvent.click(reverseButton);
    await waitFor(() =>
      expect(fresh.markMock).toHaveBeenCalledWith({ keys: [techA.dedup_key, techB.dedup_key], marker: "read", value: false }),
    );
    await waitFor(() => expect(screen.getByTestId("feed-drill-ch-t-a").textContent).toContain("未读 1"));
  });

  it("R1 L2 品类批量失败(深审 F3):按调用前快照回滚(窗内计数回真值),feed-mark-error 在 L3 流区明示", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    let rejectMark: ((err: unknown) => void) | undefined;
    fresh.markMock.mockImplementation(
      () => new Promise((_resolve, reject) => {
        rejectMark = reject;
      }),
    );
    const techRead = fixtureItem({ category: "tech", source: "t-a", read: true, title: "技已读甲" });
    const techUnread = fixtureItem({ category: "tech", source: "t-b", title: "技未读乙" });
    fresh.storeItemsMock.mockResolvedValue(result([techRead, techUnread]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    fireEvent.click(await screen.findByTestId("feed-drill-cat-tech"));
    fireEvent.click(await screen.findByTestId("feed-category-mark-all"));
    await waitFor(() =>
      expect(fresh.markMock).toHaveBeenCalledWith({ keys: [techRead.dedup_key, techUnread.dedup_key], marker: "read", value: true }),
    );
    // 乐观:窗内未读计数翻 0
    await waitFor(() => expect(screen.getByTestId("feed-drill-ch-t-b").textContent).toContain("未读 0"));
    act(() =>
      rejectMark?.(new SidecarRequestError({ code: "store_corrupt", path: "$", message: "库损坏" })),
    );
    // 快照回滚:乙回未读(计数 1),甲本就已读不动
    await waitFor(() => expect(screen.getByTestId("feed-drill-ch-t-b").textContent).toContain("未读 1"));
    expect(screen.getByTestId("feed-drill-ch-t-a").textContent).toContain("未读 0");
    // 错误回执挂 L3 流区:面包屑回渠道流后可见(markError 在列表区渲染)
    fireEvent.click(screen.getByTestId("feed-drill-ch-t-b"));
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
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

  it("未过门:L2 品类头无批量入口(旧通路无品类作用域,store.state.* 零调用)", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL - 1));
    storeItemsMock.mockResolvedValue(result([fixtureItem({ category: "tech" })]));
    renderScreen();
    fireEvent.click(await screen.findByTestId("feed-drill-cat-tech"));
    await screen.findByTestId("feed-l2");
    // 未过门:L2 头部无「本品类全部已读」;store.state.* 全家零调用
    expect(screen.queryByTestId("feed-category-mark-all")).toBeNull();
    expect(markAllMock).not.toHaveBeenCalled();
  });

  it("质检件一键盘焦点:进入确认态后焦点自动落确认主钮(触发钮卸载不回落 body);Esc 仍取消且零执行", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 99 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    await screen.findByText("条目 1");
    await waitFor(() =>
      expect(screen.getByRole("button", { name: "全部标已读" }).getAttribute("title")).toContain("全库"),
    );

    // 键盘路径:一次点击进确认态,触发钮已卸载 —— autoFocus 补位,焦点落
    // 确认主钮(键盘/读屏用户无需重 Tab 定位;不回落 body)
    fireEvent.click(screen.getByRole("button", { name: "全部标已读" }));
    const confirm = screen.getByRole("button", { name: "确认全部标已读" });
    expect(document.activeElement).toBe(confirm);

    // Esc 全局收口不被程序化初始焦点破坏:确认态退出、回到常规两钮、零执行
    fireEvent.keyDown(confirm, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(screen.getByRole("button", { name: "全部标已读" })).toBeTruthy();
    expect(fresh.markAllMock).not.toHaveBeenCalled();
  });

  it("质检件二知会:「过滤:未读」钮 title 注明会隐藏全已读分组(含批量入口),其余页签不带(最小面)", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    await screen.findByText("条目 1");
    const unread = screen.getByRole("button", { name: "过滤:未读" });
    expect(unread.getAttribute("title")).toContain("全已读");
    expect(unread.getAttribute("title")).toContain("全部");
    // 知会特定于未读口径(组头随过滤后集合渲染的边界);其余页签零附加文案
    expect(screen.getByRole("button", { name: "过滤:星标" }).getAttribute("title")).toBeNull();
    expect(screen.getByRole("button", { name: "过滤:稍后读" }).getAttribute("title")).toBeNull();
    expect(screen.getByRole("button", { name: "过滤:全部" }).getAttribute("title")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// D4 纯函数(api.ts):groupFeedItems 时间分桶边界 / categoryColor 稳定性
// ---------------------------------------------------------------------------

describe("feed D4 纯函数(api.ts)", () => {
  it("groupFeedItems:四桶按 今天/昨天(上一窗口)/7天内/更早 边界落位(03:00 窗锚口径,深审 F7),空桶不出组", () => {
    const now = new Date(2026, 9, 3, 12, 0); // 2026-10-03 正午(本地时区)
    const at = (iso: string) => fixtureItem({ first_seen: iso });
    const items = [
      at("2026-10-03T10:00:00"), // 今天(本窗 03:00 起)
      at("2026-10-03T03:00:00"), // 今天(窗锚边界含)
      at("2026-10-03T02:59:00"), // 昨天(上一窗口)—— 00:00-03:00 属上一窗
      at("2026-10-02T12:00:00"), // 昨天(上一窗口)
      at("2026-09-30T10:00:00"), // 7 天内
      at("2026-09-26T03:00:00"), // 7 天内(窗锚 7 天下边界含:10-03T03:00 − 7d)
      at("2026-09-26T02:59:00"), // 更早(7 天界外一分)
      at("不是时间"), // 更早(first_seen 无效归更早)
    ];
    const groups = groupFeedItems(items, now);
    expect(groups.map((group) => group.label)).toEqual(["今天", "昨天(上一窗口)", "7 天内", "更早"]);
    expect(groups[0].items).toHaveLength(2);
    expect(groups[1].items).toHaveLength(2);
    expect(groups[2].items).toHaveLength(2);
    expect(groups[3].items).toHaveLength(2);
  });

  it("groupFeedItems:00:00-03:00 条目组头标「昨天(上一窗口)」(F7 口径修正 —— 03:00 清零语义下它们是昨窗尾段,日历「今天」是错标)", () => {
    const now = new Date(2026, 9, 3, 14, 0); // 当天 14:00:当前窗 = 10-03 03:00 起
    const at = (iso: string) => fixtureItem({ first_seen: iso });
    const groups = groupFeedItems([at("2026-10-03T10:00:00"), at("2026-10-03T01:00:00")], now);
    // 10:00 在本窗 → 「今天」;01:00(00:00-03:00 时段)→ 昨窗尾段,组头如实
    expect(groups.map((group) => group.label)).toEqual(["今天", "昨天(上一窗口)"]);
    // 凌晨视角(now 在窗前半段):昨日下午条目仍在**当前窗内**→「今天」,
    // 组头与滚动窗所见一致(窗口对齐的另一面)
    const lateNight = groupFeedItems([at("2026-10-02T20:00:00")], new Date(2026, 9, 3, 1, 30));
    expect(lateNight.map((group) => group.label)).toEqual(["今天"]);
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

// ---------------------------------------------------------------------------
// later 到期重现 纯函数(api.ts ①,10-05-fe-gap-leftovers):isLaterResurface
// 时效判定边界 / applyFeedFilter 未读视图并入到期稍后读
// ---------------------------------------------------------------------------

describe("feed later 到期重现 纯函数(api.ts)", () => {
  const NOW = new Date("2026-10-06T12:00:00");
  const daysAgoIso = (days: number) => new Date(NOW.getTime() - days * 86_400_000).toISOString();

  it("isLaterResurface:later+超窗=到期(含边界整 7 天);未超窗/无 later/first_seen 缺失或无效 = 不到期", () => {
    const laterState = { later: true };
    expect(isLaterResurface(fixtureItem({ first_seen: daysAgoIso(8) }), laterState, NOW)).toBe(true);
    expect(isLaterResurface(fixtureItem({ first_seen: daysAgoIso(7) }), laterState, NOW)).toBe(true); // 边界含
    expect(isLaterResurface(fixtureItem({ first_seen: daysAgoIso(6) }), laterState, NOW)).toBe(false);
    expect(isLaterResurface(fixtureItem({ first_seen: daysAgoIso(8) }), { read: true }, NOW)).toBe(false); // 无 later
    expect(isLaterResurface(fixtureItem({ first_seen: daysAgoIso(8) }), undefined, NOW)).toBe(false);
    expect(isLaterResurface(fixtureItem({ first_seen: null }), laterState, NOW)).toBe(false); // 缺刻
    expect(isLaterResurface(fixtureItem({ first_seen: "not-a-date" }), laterState, NOW)).toBe(false); // 无效刻
    expect(isLaterResurface(fixtureItem({ first_seen: daysAgoIso(8) }), { later: true, read: true }, NOW)).toBe(true); // 已读不影响
  });

  it("applyFeedFilter:未读视图并入到期稍后读(已读+later+超窗);未到期已读仍只在稍后读桶;桶内全量可见", () => {
    const due = fixtureItem({ title: "due", first_seen: daysAgoIso(9) });
    const notDue = fixtureItem({ title: "fresh", first_seen: daysAgoIso(1) });
    const plainRead = fixtureItem({ title: "read", first_seen: daysAgoIso(9) });
    const plainUnread = fixtureItem({ title: "unread", first_seen: daysAgoIso(9) });
    const items = [due, notDue, plainRead, plainUnread];
    const states = {
      [due.dedup_key]: { read: true, later: true },
      [notDue.dedup_key]: { read: true, later: true },
      [plainRead.dedup_key]: { read: true },
    };
    // 未读 = 真·未读 + 到期稍后读(plainRead 已读未稍后读 = 不重现;保序)
    expect(applyFeedFilter(items, states, "unread", NOW).map((item) => item.title)).toEqual([
      "due",
      "unread",
    ]);
    // 稍后读桶:到期与否全量可见,过滤语义不动
    expect(applyFeedFilter(items, states, "later", NOW).map((item) => item.title)).toEqual(["due", "fresh"]);
    // 全部:不过滤,now 不参与
    expect(applyFeedFilter(items, states, "all", NOW)).toHaveLength(4);
    // 不传 now = 当前时刻缺省(新鲜夹具不到期,回归既有三态口径)
    expect(applyFeedFilter([plainUnread], {}, "unread")).toEqual([plainUnread]);
  });
});

// ---------------------------------------------------------------------------
// topbar-cleanup 纯函数(api.ts):categoryOptionsFromHealth 品类下拉词汇源
// ---------------------------------------------------------------------------

describe("feed topbar-cleanup 纯函数(api.ts)", () => {
  it("categoryOptionsFromHealth:id 去重(首现优先)+ name 缺省回 id + null id 不入 + id 排序稳定", () => {
    const plugins = [
      pluginEntry({ id: "stocks", name: null }), // name 缺省回 id
      pluginEntry({ id: "ai-news", name: "AI资讯" }),
      pluginEntry({ id: "ai-news", name: "重复id后现" }), // 同 id 去重,首现优先
      pluginEntry({ id: null, name: "坏插件" }), // 装不上(id=null)不入选项
    ];
    expect(categoryOptionsFromHealth(plugins)).toEqual([
      { id: "ai-news", label: "AI资讯" },
      { id: "stocks", label: "stocks" },
    ]);
    expect(categoryOptionsFromHealth([])).toEqual([]); // 空入空出
  });
});

// ---------------------------------------------------------------------------
// feed-channel-groups(10-06):品类分组下渠道二级分组 + 五档差异化卡面 +
// 实时滚动 + 当日窗 03:00 视图清零
// ---------------------------------------------------------------------------

/** health 夹具源条目(SourceReport 形状;engine = 渠道类型判定词表源) */
function sourceEntry(name: string, engine: string): HealthResult["plugins"][number]["sources"][number] {
  return {
    name,
    url: "https://example.com",
    engine,
    engine_hint: null,
    health: {
      state: "unknown",
      reason: "无观测",
      observed: 0,
      latest: null,
      baseline: null,
    },
    fingerprint_skips: { observed: 0, skipped: 0 },
  };
}

describe("FeedScreen · feed-channel-groups(渠道分组+差异化+实时滚动+当日窗)", () => {
  it("L1 品类计数 → L2 渠道行(类型词+计数)→ L3 渠道内卡片:三级路径逐层可用", async () => {
    const items = [
      fixtureItem({ category: "tech", source: "anthropic-news-watch", title: "闻甲" }),
      fixtureItem({ category: "tech", source: "openai-news", title: "闻乙" }),
      fixtureItem({ category: "tech", source: "openai-news", title: "闻丙" }),
      fixtureItem({ category: "news", source: "linuxsb", title: "闻丁" }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(
          items.filter(
            (item) =>
              (!params?.category || item.category === params.category) &&
              (!params?.source || item.source === params.source),
          ),
        ),
      ),
    );
    renderScreen();

    // L1:置顶全局行 + 品类行(tech/news,含今日计数)
    const allRow = await screen.findByTestId("feed-drill-all");
    // 计数随 store.items 异步应答补齐(行先以零计数渲染)——waitFor 等数据
    // 落地再断(与 F1 用例同款竞态钉法);同批渲染的品类行计数随即可断。
    await waitFor(() => expect(allRow.textContent).toContain("3 渠道")); // 4 条 × 3 渠道(anthropic/openai/linuxsb)
    const techRow = await screen.findByTestId("feed-drill-cat-tech");
    expect(techRow.textContent).toContain("3 条");
    expect(screen.getByTestId("feed-drill-cat-news").textContent).toContain("1 条");

    // L2:tech 品类下两渠道(首现顺序),行带源名 + 类型词 + 窗内计数
    fireEvent.click(techRow);
    const channelA = await screen.findByTestId("feed-drill-ch-anthropic-news-watch");
    expect(channelA.textContent).toContain("anthropic-news-watch");
    expect(channelA.textContent).toContain("新闻渠道");
    expect(channelA.textContent).toContain("1 条");
    const channelB = screen.getByTestId("feed-drill-ch-openai-news");
    expect(channelB.textContent).toContain("2 条");
    expect(screen.queryByTestId("feed-drill-ch-linuxsb")).toBeNull(); // 他品类渠道不在场
    // 置顶「全部渠道」行
    expect(screen.getByTestId("feed-drill-cat-all")).toBeTruthy();

    // L3:点渠道行进该渠道消息流,卡片只落本渠道
    fireEvent.click(channelB);
    expect(await screen.findByText("闻乙")).toBeTruthy();
    expect(screen.getByText("闻丙")).toBeTruthy();
    expect(screen.queryByText("闻甲")).toBeNull();
    expect(screen.queryByText("闻丁")).toBeNull();
  });

  it("telegram 消息卡:气泡 + 频道名(去平台前缀)+ 时间;元信息行不重复源名", async () => {
    storeItemsMock.mockResolvedValue(
      result([fixtureItem({ source: "telegram-durov", title: "消息正文甲", content: "气泡内摘要" })]),
    );
    await renderStream();
    const card = await screen.findByTestId("feed-item-1");
    expect(card.getAttribute("data-kind")).toBe("telegram");
    // 气泡在场(testid 挂气泡容器),正文在气泡内
    const bubble = within(card).getByTestId("feed-tg-bubble-1");
    expect(within(bubble).getByText("消息正文甲")).toBeTruthy();
    // 频道名行:去 telegram- 前缀显频道本名;元信息行不重复源名
    expect(within(card).getByText("durov")).toBeTruthy();
    expect(within(card).queryByText("telegram-durov")).toBeNull();
    // 时间在频道名行(等宽相对时间)
    expect(within(card).getAllByText(/刚刚|分钟前|小时前|天前|\d{4}-/).length).toBeGreaterThan(0);
  });

  it("urlwatch 变更事件(engine 映射):「有更新」徽标 + 目标页链接(watch_page)+ 展开 diff 明细", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        plugins: [pluginEntry({ id: "ai-news", sources: [sourceEntry("anthropic-news-watch", "urlwatch")] })],
      }),
    );
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({
          source: "anthropic-news-watch",
          title: "Anthropic 官网有更新",
          content: "+ Claude 5 发布",
          watch_event: "changed",
          watch_page: "https://www.anthropic.com/news",
          url: "https://www.anthropic.com/news#watch-abc123def0",
        }),
      ]),
    );
    await renderStream();
    const card = await screen.findByTestId("feed-item-1");
    expect(card.getAttribute("data-kind")).toBe("watch");
    expect(within(card).getByTestId("feed-watch-badge-1").textContent).toContain("有更新");
    // 目标页链接 = watch_page 主机名(条目 url 是 #watch-<sha> 锚)
    const target = within(card).getByTestId("feed-watch-target-1");
    expect(target.textContent).toContain("www.anthropic.com");
    // 展开:diff 变更明细(等宽块)
    fireEvent.click(within(card).getByRole("button", { name: "展开条目" }));
    const diff = await within(card).findByTestId("feed-watch-diff-1");
    expect(diff.textContent).toContain("+ Claude 5 发布");
  });

  it("prompt 日报(engine 映射):markdown 文档视图可折叠——收起单行摘要,展开出标题/列表/加粗", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        plugins: [pluginEntry({ id: "ai-vendor-watch", sources: [sourceEntry("ai-vendor-watch", "prompt")] })],
      }),
    );
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({
          source: "ai-vendor-watch",
          title: "AI 厂商日报",
          content: "## 厂商动态\n\n- OpenAI 发模型\n- Anthropic 发论文\n\n**重点** 与 `代码`",
        }),
      ]),
    );
    await renderStream();
    const card = await screen.findByTestId("feed-item-1");
    expect(card.getAttribute("data-kind")).toBe("document");
    // 收起:文档体不出场(单行摘要形态)
    expect(within(card).queryByTestId("feed-doc-body-1")).toBeNull();
    fireEvent.click(within(card).getByRole("button", { name: "展开条目" }));
    const body = await within(card).findByTestId("feed-doc-body-1");
    // markdown-lite:## 标题 / 列表项 / **加粗** / `代码`
    expect(within(body).getByText("厂商动态")).toBeTruthy();
    expect(within(body).getByText("OpenAI 发模型")).toBeTruthy();
    expect(within(body).getByText("Anthropic 发论文")).toBeTruthy();
    expect(within(body).getByText("重点")).toBeTruthy();
    expect(within(body).getByText("代码")).toBeTruthy();
  });

  it("games 价格优惠行:现价突出 + 原价划线 + 限免徽标(Epic 形态);CS 美元形态同渲", async () => {
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({
          category: "games",
          source: "epic-free",
          title: "Epic 限免游戏",
          price_text: "¥0.00",
          final_price: 0,
          original_price: 3900,
          discount_pct: 100,
        }),
        fixtureItem({
          category: "games",
          source: "cheapshark",
          title: "多店折扣",
          sale_price: "0.50",
          normal_price: "16.99",
          savings_pct: "97.057092",
        }),
      ]),
    );
    await renderStream();
    await screen.findByText("Epic 限免游戏");
    const epic = screen.getByTestId("feed-item-1");
    expect(epic.getAttribute("data-kind")).toBe("deal");
    const epicPrice = within(epic).getByTestId("feed-deal-price-1");
    expect(within(epicPrice).getByText("限免")).toBeTruthy();
    expect(within(epicPrice).getByText("¥0.00")).toBeTruthy();
    expect(within(epicPrice).getByText("¥39.00")).toBeTruthy(); // 原价分→元
    const cs = screen.getByTestId("feed-item-2");
    const csPrice = within(cs).getByTestId("feed-deal-price-2");
    expect(within(csPrice).getByText("$0.50")).toBeTruthy();
    expect(within(csPrice).getByText("$16.99")).toBeTruthy();
    expect(within(csPrice).getByText("-97%")).toBeTruthy(); // savings_pct 字符串解析取整
    expect(within(csPrice).queryByText("限免")).toBeNull(); // CS 实测无 0 元 deal
  });

  it("实时滚动:cron.completed 事件 → 首页新键前插进流(已加载行零扰动)", async () => {
    let emitEvent: ((event: { type: string }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string }) => void;
      return Promise.resolve(() => {});
    });
    const existing = fixtureItem({ title: "旧行" });
    const fresh = fixtureItem({ title: "新行" });
    // 流查询(L1 首页 + 下钻 L3-all)前两发只回旧行;事件后的 liveRefresh 才见
    // 新行(F1 概览按品类另发,不计流查询序 —— 概览恒回旧行不扰断言)
    let streamServed = 0;
    storeItemsMock.mockImplementation((params?: StoreItemsParams) => {
      if (params?.category) return Promise.resolve(result([existing]));
      streamServed += 1;
      return Promise.resolve(result(streamServed <= 2 ? [existing] : [fresh, existing]));
    });
    await renderStream();
    await screen.findByText("旧行");
    expect(screen.queryByText("新行")).toBeNull();

    act(() => emitEvent?.({ type: "cron.completed" }));
    expect(await screen.findByText("新行")).toBeTruthy();
    expect(screen.getByText("旧行")).toBeTruthy(); // 前插不弃已加载行
  });

  it("当日窗 03:00 清零:滚动流(未读/全部)窗内条目离场、视图如实计数;星标跨窗可见;窗锚知会在场", async () => {
    const start = dayWindowStart();
    const outOfWindow = fixtureItem({
      title: "窗前旧条目",
      first_seen: new Date(start.getTime() - 3_600_000).toISOString(), // 窗起点前 1h,必在窗外
    });
    const inWindow = fixtureItem({ title: "窗内新条目" }); // now,必在窗内
    // 窗外条目滚动流永不可见 → 星标走本地态预置(旧通路,与三态测试同门)
    localStorageStub.setItem(
      "myssia.feed.states.v1",
      JSON.stringify({ [outOfWindow.dedup_key]: { starred: true } }),
    );
    storeItemsMock.mockResolvedValue(result([outOfWindow, inWindow]));
    await renderStream();
    // 默认未读:窗外条目离场(视图清零语义),窗锚知会在场
    await screen.findByText("窗内新条目");
    expect(screen.queryByText("窗前旧条目")).toBeNull();
    expect(screen.getByTestId("feed-day-window").textContent).toContain("03:00");
    expect(screen.getByText("1 / 2 条")).toBeTruthy(); // 计数行如实(1 可见 / 2 已加载)
    // 全部:同样受窗
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    await screen.findByText("窗内新条目");
    expect(screen.queryByText("窗前旧条目")).toBeNull();
    // 星标 = 显式留存,跨窗可见;星标桶不受窗,窗锚知会退场
    fireEvent.click(screen.getByRole("button", { name: "过滤:星标" }));
    expect(await screen.findByText("窗前旧条目")).toBeTruthy();
    expect(screen.queryByTestId("feed-day-window")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// feed-channel-groups 纯函数(api.ts):渠道类型判定 / engine 映射 / 渠道
// 分组 / 价格视图 / 当日窗 / 实时滚动合并
// ---------------------------------------------------------------------------

describe("feed channel-groups 纯函数(api.ts)", () => {
  it("channelKindOf:前缀 telegram > engine urlwatch·watch_event > engine prompt·store_report > 品类·价格键 > news", () => {
    const engines = new Map([
      ["anthropic-news-watch", "urlwatch"],
      ["ai-vendor-watch", "prompt"],
      ["daily-digest", "store_report"],
    ]);
    // telegram 前缀(telegram- 规约 + tg- 旧缩写 + 下划线形),engine 映射不抢判
    expect(channelKindOf({ source: "telegram-durov", category: null }, engines)).toBe("telegram");
    expect(channelKindOf({ source: "tg-openai_news", category: null }, new Map([["tg-openai_news", "urlwatch"]]))).toBe("telegram");
    // watch:engine 映射 / watch_event 字段兜底(旧 sidecar 无映射)
    expect(channelKindOf({ source: "anthropic-news-watch", category: null }, engines)).toBe("watch");
    expect(channelKindOf({ source: "x", category: null, watch_event: "changed" })).toBe("watch");
    // document:prompt / store_report
    expect(channelKindOf({ source: "ai-vendor-watch", category: null }, engines)).toBe("document");
    expect(channelKindOf({ source: "daily-digest", category: null }, engines)).toBe("document");
    // deal:品类 games/wool;价格键在场(异品类也认);无 engine 映射时字段自判
    expect(channelKindOf({ source: "epic-free", category: "games" })).toBe("deal");
    expect(channelKindOf({ source: "any", category: "wool" })).toBe("deal");
    expect(channelKindOf({ source: "any", category: "other", price_text: "¥0.00" })).toBe("deal");
    expect(channelKindOf({ source: "any", category: "other", final_price: 1360 })).toBe("deal");
    expect(channelKindOf({ source: "any", category: "other", sale_price: "0.50" })).toBe("deal");
    // news:缺省;null source 安全
    expect(channelKindOf({ source: "openai-news", category: "ai-news" })).toBe("news");
    expect(channelKindOf({ source: null, category: null })).toBe("news");
  });

  it("engineMapFromHealth:源名→engine 首现优先去重;空/无源插件空映射", () => {
    const plugins = [
      pluginEntry({ sources: [sourceEntry("a", "urlwatch"), sourceEntry("b", "static_html")] }),
      pluginEntry({ sources: [sourceEntry("a", "prompt")] }), // 同名源首现优先
      pluginEntry({ sources: [] }),
    ];
    const engines = engineMapFromHealth(plugins);
    expect(engines.get("a")).toBe("urlwatch");
    expect(engines.get("b")).toBe("static_html");
    expect(engines.size).toBe(2);
    expect(engineMapFromHealth([]).size).toBe(0);
  });

  it("groupFeedItemsByChannel:首次出现顺序出组 + 组内保序 + null 源归未知来源 + 组类型取首条判定", () => {
    const a1 = fixtureItem({ source: "a", title: "a1" });
    const b1 = fixtureItem({ source: "b", title: "b1" });
    const a2 = fixtureItem({ source: "a", title: "a2" });
    const bare = fixtureItem({ source: null, title: "bare" });
    const groups = groupFeedItemsByChannel([a1, b1, a2, bare]);
    expect(groups.map((group) => group.key)).toEqual(["a", "b", null]);
    expect(groups[0].items.map((item) => item.title)).toEqual(["a1", "a2"]);
    expect(groups[1].items.map((item) => item.title)).toEqual(["b1"]);
    expect(groups[2].label).toBe("未知来源");
    expect(groups[0].kind).toBe("news");
    // engine 映射参与组类型判定
    const watchGroups = groupFeedItemsByChannel(
      [fixtureItem({ source: "w", watch_event: "changed" })],
      new Map([["w", "urlwatch"]]),
    );
    expect(watchGroups[0].kind).toBe("watch");
  });

  it("dealPriceView:games 四源形态——Epic 限免(price_text+分 int+100%)/ Steam 折扣(分 int)/ CS 美元串 / GOG 限免析取", () => {
    // Epic 限免:price_text 直出 + 原价分→元 + 限免
    expect(
      dealPriceView({ price_text: "¥0.00", final_price: 0, original_price: 3900, discount_pct: 100 }),
    ).toEqual({ current: "¥0.00", original: "¥39.00", discount: 100, free: true });
    // Steam 折扣:final/original 分 int → 元;80% 非限免
    expect(
      dealPriceView({ final_price: 1360, original_price: 6800, discount_pct: 80 }),
    ).toEqual({ current: "¥13.60", original: "¥68.00", discount: 80, free: false });
    // CheapShark 美元串:sale/normal 直出 + savings_pct 字符串取整
    expect(
      dealPriceView({ sale_price: "0.50", normal_price: "16.99", savings_pct: "97.057092", final_price: "0.50" }),
    ).toEqual({ current: "$0.50", original: "$16.99", discount: 97, free: false });
    // GOG 限免析取:sale 0 且 normal>0(字符串形态)
    expect(
      dealPriceView({ sale_price: "0.00", normal_price: "19.99", final_price: "0.00" }),
    ).toEqual({ current: "$0.00", original: "$19.99", discount: null, free: true });
    // 无任何价格键:current null(消费侧不渲价格块)
    expect(dealPriceView({})).toEqual({ current: null, original: null, discount: null, free: false });
  });

  it("dayWindowStart:03:00 锚——当日 03:00 后取当日锚,前取昨日锚,整点含边界", () => {
    expect(dayWindowStart(new Date(2026, 9, 6, 14, 30)).getTime()).toBe(new Date(2026, 9, 6, 3, 0).getTime());
    expect(dayWindowStart(new Date(2026, 9, 6, 3, 0)).getTime()).toBe(new Date(2026, 9, 6, 3, 0).getTime()); // 整点含
    expect(dayWindowStart(new Date(2026, 9, 6, 2, 59)).getTime()).toBe(new Date(2026, 9, 5, 3, 0).getTime());
    expect(dayWindowStart(new Date(2026, 9, 6, 0, 0)).getTime()).toBe(new Date(2026, 9, 5, 3, 0).getTime()); // 跨月窗口同构
  });

  it("inDayWindow:窗起含边界、窗前不含、缺失/无效刻保守放行(不静默藏数据)", () => {
    const start = new Date(2026, 9, 6, 3, 0);
    expect(inDayWindow("2026-10-06T03:00:00", start)).toBe(true); // 含边界
    expect(inDayWindow("2026-10-06T10:00:00", start)).toBe(true);
    expect(inDayWindow("2026-10-06T02:59:59", start)).toBe(false);
    expect(inDayWindow(null, start)).toBe(true); // 缺刻保守放行
    expect(inDayWindow("not-a-date", start)).toBe(true); // 无效刻同
  });

  it("mergeFreshItems:首页新键前插 + 已加载行全保 + added 计数;全旧零扰动", () => {
    const old1 = fixtureItem({ title: "旧一" });
    const old2 = fixtureItem({ title: "旧二" });
    const fresh1 = fixtureItem({ title: "新一" });
    const merged = mergeFreshItems([old1, old2], [fresh1, old1]);
    expect(merged.added).toBe(1);
    expect(merged.items.map((item) => item.title)).toEqual(["新一", "旧一", "旧二"]); // 前插保序
    expect(mergeFreshItems([old1], [old1]).added).toBe(0); // 无新键零扰动
  });
});

// ---------------------------------------------------------------------------
// 深审修复批(feed 面):F1 L1/L2 按品类查询(假空态)/ F2 请求序号守卫 /
// F4 markdown 链接受控门 / F5 价格键宽容解析 / F6 热键守卫补 <select>
// (F3 作用域收窄并入 g9-read-all 批重写;F7 分组口径并入 D4 纯函数批)
// ---------------------------------------------------------------------------

describe("FeedScreen · 深审修复批(F1/F2/F4/F5/F6)", () => {
  it("F1:L1 计数与 L2 渠道列表按品类查询 —— 全局首页外的长尾品类不再假空态/假零", async () => {
    // 全局首页被 hot 品类占满;wool 品类有条目但一条都不进全局首页
    healthMock.mockResolvedValue(
      healthResult({
        plugins: [
          pluginEntry({ id: "ai-news", name: "AI资讯" }),
          pluginEntry({ id: "wool", name: "羊毛情报" }),
        ],
      }),
    );
    const hot = [
      fixtureItem({ category: "hot", source: "hot-a", title: "热一" }),
      fixtureItem({ category: "hot", source: "hot-b", title: "热二" }),
    ];
    const woolA = fixtureItem({ category: "wool", source: "wool-a", title: "羊毛甲" });
    const woolB = fixtureItem({ category: "wool", source: "wool-b", title: "羊毛乙" });
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(params?.category === "wool" ? [woolA, woolB] : hot)),
    );
    renderScreen();

    // L1:wool 行计数来自品类查询页(旧实现只吃全局首页 → 假零「0 条」;
    // waitFor 等概览页落地 —— 行渲染先于概览应答属正常竞态)
    const woolRow = await screen.findByTestId("feed-drill-cat-wool");
    await waitFor(() => expect(woolRow.textContent).toContain("2 条"));
    expect(woolRow.textContent).toContain("2 渠道");
    // 品类查询确实发出(store.items 带 category 游标,勿全量拉)
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenCalledWith({ limit: 50, category: "wool" }),
    );

    // L2:wool 渠道行在场(旧实现 = 过滤全局首页 → 假空态);行计数如实
    fireEvent.click(woolRow);
    const channelB = await screen.findByTestId("feed-drill-ch-wool-b");
    expect(channelB.textContent).toContain("wool-b");
    expect(channelB.textContent).toContain("今日 1 条");
    expect(screen.getByTestId("feed-drill-ch-wool-a").textContent).toContain("今日 1 条");
    expect(screen.queryByText("该品类暂无窗内条目")).toBeNull();
    // 下钻渠道流:条目本尊可见(端到端:品类查询 → 渠道行 → 消息)
    fireEvent.click(channelB);
    expect(await screen.findByText("羊毛乙")).toBeTruthy();
  });

  it("F2 竞态一:refresh 慢应答不覆盖 liveRefresh 已并入的新行(请求序号守卫)", async () => {
    let emitEvent: ((event: { type: string }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string }) => void;
      return Promise.resolve(() => {});
    });
    const existing = fixtureItem({ title: "旧行" });
    const fresh = fixtureItem({ title: "新行" });
    const deferreds: Array<(value: StoreItemsResult) => void> = [];
    storeItemsMock.mockImplementation(
      () => new Promise<StoreItemsResult>((resolve) => { deferreds.push(resolve); }),
    );
    renderScreen();
    // L1 挂载(全局流 + 概览)全部应答旧行
    await waitFor(() => expect(deferreds.length).toBeGreaterThan(0));
    act(() => deferreds.splice(0).forEach((resolve) => resolve(result([existing]))));
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    await waitFor(() => expect(deferreds.length).toBeGreaterThan(0));
    act(() => deferreds.splice(0).forEach((resolve) => resolve(result([existing]))));
    await screen.findByText("旧行");
    expect(screen.queryByText("新行")).toBeNull();

    // 手点刷新(票 N,应答挂起)→ 事件 liveRefresh(票 N+1)先回,带回新行
    fireEvent.click(screen.getByRole("button", { name: "刷新" }));
    const refreshDefer = deferreds.splice(0)[0];
    act(() => emitEvent?.({ type: "cron.completed" }));
    const liveDefer = deferreds.splice(0)[0];
    act(() => liveDefer(result([fresh, existing])));
    expect(await screen.findByText("新行")).toBeTruthy(); // liveRefresh 已并入

    // refresh 的旧应答(无新行)回场:对票失败丢弃,不整页覆盖掉新行
    act(() => refreshDefer(result([existing])));
    await waitFor(() => expect(screen.getByText("新行")).toBeTruthy()); // 新行仍在场
    expect(screen.getByText("旧行")).toBeTruthy();
  });

  it("F2 竞态二:切作用域后在途的旧域 liveRefresh 应答丢弃(全局行不混进渠道流)", async () => {
    let emitEvent: ((event: { type: string }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string }) => void;
      return Promise.resolve(() => {});
    });
    const scoped = fixtureItem({ category: "tech", source: "t-a", title: "域内行" });
    const foreign = fixtureItem({ title: "全局外性行" });
    const deferreds: Array<(value: StoreItemsResult) => void> = [];
    storeItemsMock.mockImplementation(
      () => new Promise<StoreItemsResult>((resolve) => { deferreds.push(resolve); }),
    );
    renderScreen();
    await waitFor(() => expect(deferreds.length).toBeGreaterThan(0));
    act(() => deferreds.splice(0).forEach((resolve) => resolve(result([scoped]))));
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    await waitFor(() => expect(deferreds.length).toBeGreaterThan(0));
    act(() => deferreds.splice(0).forEach((resolve) => resolve(result([scoped]))));
    await screen.findByText("域内行");

    // 事件 liveRefresh(全局域,票 N)在途未答 → 下钻渠道(refresh 票 N+1)
    act(() => emitEvent?.({ type: "cron.completed" }));
    const staleLiveDefer = deferreds.splice(0)[0];
    fireEvent.click(screen.getByTestId("feed-crumb-home"));
    await waitFor(() => expect(deferreds.length).toBeGreaterThan(0));
    const l1RefreshDefer = deferreds.splice(0, 1)[0];
    act(() => l1RefreshDefer(result([scoped])));
    await screen.findByTestId("feed-drill-all");

    // 旧域 liveRefresh 应答回场(带回全局外性行):对票失败丢弃,不混入
    act(() => staleLiveDefer(result([foreign, scoped])));
    // 回 L3 全局流验证:外性行未并入(仅 scoped 在场)
    fireEvent.click(await screen.findByTestId("feed-drill-all"));
    await screen.findByText("域内行");
    await waitFor(() => expect(screen.queryByText("全局外性行")).toBeNull());
  });

  it("F4:markdown 文档链接走 openInBrowser 受控门(默认导航被拦,shell.open 收到 URL)", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        plugins: [pluginEntry({ id: "ai-vendor-watch", sources: [sourceEntry("ai-vendor-watch", "prompt")] })],
      }),
    );
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({
          source: "ai-vendor-watch",
          title: "AI 厂商日报",
          content: "详见 https://example.com/full-report 全文",
        }),
      ]),
    );
    await renderStream();
    const card = await screen.findByTestId("feed-item-1");
    fireEvent.click(within(card).getByRole("button", { name: "展开条目" }));
    const body = await within(card).findByTestId("feed-doc-body-1");
    const link = within(body).getByTitle("在浏览器打开:https://example.com/full-report");
    fireEvent.click(link);
    await waitFor(() => expect(shellOpenMock).toHaveBeenCalledWith("https://example.com/full-report"));
  });

  it("F5:dealPriceView 数值键字符串形态宽容解析(final_price/original_price/discount_pct 三键)", () => {
    // 字符串数值照常换算(旧实现 typeof number 严判 → 静默降级 null 不渲价格)
    expect(
      dealPriceView({ final_price: "1360", original_price: "6800", discount_pct: "80" }),
    ).toEqual({ current: "¥13.60", original: "¥68.00", discount: 80, free: false });
    // 字符串 0 / 100% 限免析取照常
    expect(dealPriceView({ final_price: "0", discount_pct: "100" }).free).toBe(true);
    // 布尔/空串/非数值不猜(null 语义保持;布尔绕过类型 = 运行时防御面)
    expect(
      dealPriceView({ discount_pct: true } as unknown as Parameters<typeof dealPriceView>[0]).discount,
    ).toBeNull();
    expect(dealPriceView({ final_price: "" }).current).toBeNull();
    expect(dealPriceView({ final_price: "abc", original_price: "x" }).original).toBeNull();
  });

  it("F6:u/j/k 热键守卫补 <select> —— 下拉聚焦时敲 j 不巡游(无 focus 环)", async () => {
    mockYamlSidecar();
    storeItemsMock.mockResolvedValue(result([fixtureItem({ title: "甲" }), fixtureItem({ title: "乙" })]));
    await renderStream();
    const first = await screen.findByTestId("feed-item-1");
    // 开卡内沉淀面板(目标 YAML <select> 在场)并聚焦
    fireEvent.click(within(first).getByRole("button", { name: "沉淀为关键词" }));
    const select = await screen.findByLabelText("目标品类 YAML");
    fireEvent.focus(select);
    fireEvent.keyDown(select, { key: "j" });
    // 守卫生效:无任何卡进入键盘巡游态
    await waitFor(() => {
      const cards = screen.getAllByTestId(/^feed-item-/);
      expect(cards.every((node) => node.getAttribute("data-nav-focused") === "false")).toBe(true);
    });
    // 对照:非输入目标上敲 j 正常巡游(首卡亮环)
    fireEvent.keyDown(window, { key: "j" });
    await waitFor(() => {
      const cards = screen.getAllByTestId(/^feed-item-/);
      expect(cards.some((node) => node.getAttribute("data-nav-focused") === "true")).toBe(true);
    });
  });
});
