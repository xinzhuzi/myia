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
 * topbar-cleanup 归位批(10-04):屏内品类下拉(health().categories 词汇源,
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
 * tg-channel-card 批(10-08,主人令「TG 渠道要单独做界面……单独一个卡片,
 * 点击进去才是详情」):流内(全部条目/品类流)TG 条目按渠道聚合置顶渠道
 * 卡区(频道名+最新预览+条数/未读+未读竖条),TG 消息卡不再逐条进流;点
 * 卡进 source 作用域消息流(气泡详情),面包屑「全部条目」中间层一键回流;
 * 全 TG 流不误现空态;j/k 巡游只落真实渲染卡;纯函数 telegramChannelCards /
 * channelDisplayName。
 * v6 渠道瀑布流重写(10-09,主人三次纠偏最终定调「卡片 = 信息获取渠道」):
 *  首屏 = 渠道瀑布流(AC20:渠道全集 = health sources ∪ 已加载 source,
 *  零条目渠道出卡;卡 = 类型徽标 TG/网站/日报 + 渠道名 + cardDigest 预览 +
 *  今日 N · 未读 M)/ 搜索 = 客户端过滤渠道卡(AC21)/ 点卡进渠道条目流
 *  详情(AC22:TG = 聊天时间线,网站/日报 = 条目瀑布流,条目弹窗,TG 顶部
 *  监控台)/ 旧 chips·消息墙首屏·全库检索退场(AC23);键盘 j-k-Enter 随
 *  形态归位,U 在墙上降级无操作;读态分段/显示选项归渠道详情。渠道网格/
 *  搜索过滤/渠道详情/TG 聊天/监控台/详情弹窗用例随新 IA 重写,旧三级导航
 *  与 chips 用例删除;纯函数增 channelCardKindOf / feedChannelCards /
 *  filterChannelsByQuery。
 * v7 双栏监控台重写(10-10,主人定调「右侧是群组,左侧是群组中的数据」,
 * design-v7.md 照稿实施):右栏 aside = ChannelRow 行列表(搜索置顶过滤/
 * 类型头像 chip/选中 bg-accent 高亮/未读徽标;feed-count = 右栏脚注独占,
 * 选中态条目计数改 feed-stream-count —— 复审 R1-1 消歧)+ 左栏 section =
 * 工具条分叉(总览:批量/导出/刷新;选中:总览钮/读态分段/feed-stream-count/
 * feed-day-window/显示选项)+ TG 监控台降常驻条(工具条下不随滚,R2 吸收:
 * tgStatusPhase 三态,首拉在途无「状态未知」闪现)+ 时间线(TG 气泡/网站
 * 单列 feed-stream-list)+ 总览引导空态(feed-overview 统计行,catalogLoaded
 * 门防 CTA 闪现)。数据接线 = 双缓冲(catalogItems 喂右栏聚合,streamItems
 * 喂左栏流;states = 双缓冲并集投影,选中内标读右栏徽标即时降)。键盘双环:
 * j/k = 右栏行,Shift+J/K = 左栏条目,Enter/U 落点跟随当前环,U 右栏环 =
 * 当前渠道已加载条目一键标已读(triage),Esc 清选中回总览(弹窗开着让位),
 * Mod+F 直聚焦右栏搜索框;R1 吸收:feed-stream-count title 无「当日窗」残词。
 */
import { cleanup, fireEvent, render, screen, waitFor, within, act } from "@testing-library/react";
import { MemoryRouter, useLocation } from "react-router-dom";
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
  applySourceStats,
  aggregateTypeCards,
  appendWatchlistKeyword,
  bodyWithoutTitleDup,
  categoryColor,
  channelDisplayName,
  channelCardKindOf,
  COUNT_PROTOCOL,
  channelKindOf,
  chatSenderOf,
  chatTimeOf,
  dayWindowStart,
  foldSnsMomentCards,
  snsMomentAuthor,
  snsStreamSources,
  DEFAULT_FEED_DISPLAY,
  dealPriceView,
  engineMapFromHealth,
  feedChannelCards,
  fetchFeedPage,
  filterChannelsByQuery,
  filterTypesByQuery,
  groupFeedItems,
  inDayWindow,
  isLaterResurface,
  LATER_RESURFACE_DAYS,
  loadFeedDisplay,
  mergeFreshItems,
  READ_STATE_PROTOCOL,
  saveFeedDisplay,
  setMarkerBulk,
  cardDigest,
  sortUnreadFirst,
  STATS_PROTOCOL,
  statesFromItems,
  telegramKUrlOf,
  telegramMirrorUrlOf,
  CHANNEL_CARD_LABELS,
  CHANNEL_CARD_ORDER,
  type SourceStatsRow,
} from "./api";
import type { WechatLocalProbeView } from "@/screens/messaging/api";
import { resetTgNativeForTests } from "./tg-native-window";

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    api: {
      ...actual.api,
      version: vi.fn(),
      storeItems: vi.fn(),
      storeSourceStats: vi.fn(),
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
vi.mock("@tauri-apps/api/core", () => ({ invoke: vi.fn(), convertFileSrc: vi.fn((path: string) => `asset://localhost${path}`) }));
// AC11 内置浏览器预览(v9 升级原生视图注册表):开窗面整体 mock(零真实
// 窗口;断言只认构造调用);注册表存在性对账走静态 getByLabel/getAll,
// 一并给 mock(缺省 miss/空集 = 全部视作未开,用例内按需改写)
vi.mock("@tauri-apps/api/webviewWindow", () => {
  const WebviewWindow = vi.fn() as unknown as import("vitest").Mock & {
    getByLabel: import("vitest").Mock;
    getAll: import("vitest").Mock;
  };
  WebviewWindow.getByLabel = vi.fn(async () => null);
  WebviewWindow.getAll = vi.fn(async () => []);
  return { WebviewWindow };
});

const { api, onSidecarEvent } = await import("@/lib/api");
const storeItemsMock = vi.mocked(api.storeItems);
const sourceStatsMock = vi.mocked(api.storeSourceStats);
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
const WebviewWindowMock = (await import("@tauri-apps/api/webviewWindow"))
  .WebviewWindow as unknown as import("vitest").Mock;
// 注册表静态面(v9):存在性对账唯一真相源,组件用例按场景改写应答
const webviewGetByLabelMock = (WebviewWindowMock as unknown as { getByLabel: import("vitest").Mock })
  .getByLabel;
const webviewGetAllMock = (WebviewWindowMock as unknown as { getAll: import("vitest").Mock }).getAll;

/** 原生窗建窗调用(invoke 通道,10-12 返回钮批后的断言面:
 *  此前断言 WebviewWindow 构造,现断言 Rust 命令载荷)。 */
const nativeOpenCalls = () =>
  invokeMock.mock.calls.filter(([cmd]) => cmd === "tg_native_open") as [string, Record<string, unknown>][];

import { FeedScreen } from "./feed-screen";

/** 空流时 refresh 会追问 health(first_run 分叉);默认给「有品类」的最小应答 */
function healthResult(overrides: Partial<HealthResult> = {}): HealthResult {
  return {
    command: "list",
    config_dir: "/home/config",
    db: "/home/myssia.db",
    store_error: null,
    categories: [
      {
        file: "/home/config/ai-news.yaml",
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
    summary: { categories: 1, sources: 0, ok: 0, degraded: 0, dead: 0, unknown: 0 },
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

/** 路由探针(command-palette.test.tsx 同款惯例):读当前 pathname。本文件
 *  无 useNavigate mock 先例,导航类断言走真实路由落点,不引 react-router
 *  整体 mock。 */
function LocationProbe() {
  const location = useLocation();
  return <div data-testid="location-probe">{location.pathname}</div>;
}

/** 路由探针·带查询串(B3 深链断言:?file= 预选词进 search,不进 pathname) */
function FullLocationProbe() {
  const location = useLocation();
  return <div data-testid="location-full-probe">{`${location.pathname}${location.search}`}</div>;
}

/** v8 惯用入口:渲染 1 级类型卡墙(落地页;等类型卡形骨架卸载即铺底应答,
 *  类型卡在场)。 */
async function renderOverview() {
  renderScreen();
  await waitFor(() => expect(screen.queryByTestId("feed-types-loading")).toBeNull());
}

/** 渠道源 → 类型卡 kind(夹具导航用;与 channelCardKindOf 前缀规约同门 ——
 *  telegram-/tg- 前缀 = tg,其余 = site;daily 夹具直接传 kind)。 */
function kindOfSource(source: string): "tg" | "site" | "daily" {
  return /^(telegram|tg)[-_.]/i.test(source) ? "tg" : "site";
}

/** v8 惯用入口:1 级 → 点类型卡进 2 级渠道列表(等 feed-channel-list 在场)。 */
async function openChannelList(kind: "tg" | "site" | "daily" = "site") {
  fireEvent.click(await screen.findByTestId(`feed-type-card-${kind}`));
  await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
}

/**
 * v8 惯用入口:渲染并下钻到 3 级渠道详情(1→2→3 层层进入,AC30 动线:
 * 点类型卡 → 2 级行列表 → 点渠道行 → source 作用域查询)。等作用域查询
 * 发出且应答落地(末次调用带 source)—— 缺刻=骨架/空态短暂在场的瞬态。
 * 缺省 "Example" = 夹具默认源(site 档);kind 缺省按源名前缀派生。
 */
async function renderChannelDetail(source = "Example", kind?: "tg" | "site" | "daily") {
  renderScreen();
  await openChannelList(kind ?? kindOfSource(source));
  fireEvent.click(screen.getByTestId(`feed-channel-row-${source}`));
  await waitFor(() =>
    expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source })),
  );
}

/** importFreshScreen 图的 3 级下钻入口(read-state-server 系用例;同
 *  renderChannelDetail,但 mock 实例取 fresh 图)。 */
async function renderFreshChannelDetail(
  fresh: Awaited<ReturnType<typeof importFreshScreen>>,
  source = "Example",
  kind?: "tg" | "site" | "daily",
) {
  render(
    <MemoryRouter>
      <fresh.FeedScreen />
    </MemoryRouter>,
  );
  fireEvent.click(await freshScreenFind(fresh, `feed-type-card-${kind ?? kindOfSource(source)}`));
  await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
  fireEvent.click(screen.getByTestId(`feed-channel-row-${source}`));
  await waitFor(() =>
    expect(fresh.storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source })),
  );
}

/** fresh 模块图 findByTestId(screen 同签名;fresh 图的 RTL screen 是同一
 *  全局,直接复用 screen.findByTestId,包一层只为可读性)。 */
async function freshScreenFind(
  _fresh: Awaited<ReturnType<typeof importFreshScreen>>,
  testId: string,
): Promise<HTMLElement> {
  return screen.findByTestId(testId);
}

/** 品类下拉选项用 CategoryReport 夹具(形状对齐 types.ts;字段按需覆写) */
function categoryEntry(overrides: Partial<HealthResult["categories"][number]> = {}): HealthResult["categories"][number] {
  return {
    file: "/home/config/x.yaml",
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

// G12 夹具:config 目录两个 YAML(一好一坏)+ 目标原文(流式 keywords)
const G12_FILES = [
  {
    file: "/home/config/ai-news.yaml",
    name: "ai-news.yaml",
    parse_ok: true,
    category_id: "ai-news",
    category_name: "AI资讯",
  },
  {
    file: "/home/config/broken.yaml",
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
    if (method === "yaml.list") return { config_dir: "/home/config", files: G12_FILES };
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
        backed_up: "/home/config/ai-news.yaml.bak",
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
    await renderChannelDetail();

    const card = await screen.findByTestId("feed-item-1");
    expect(within(card).getByText(/Example/)).toBeTruthy();
    expect(within(card).getByText("tech")).toBeTruthy();
    expect(within(card).getByText("ai")).toBeTruthy();
    expect(within(card).getByText("0.87")).toBeTruthy();
    expect(within(card).getByText(/刚刚/)).toBeTruthy();
  });

  it("图析行:image_ocr 条目出「图」Badge + 单行摘要(空白压平),无图条目零渲染", async () => {
    const withImage = fixtureItem({ image_ocr: "GPT-5 发布会\n  截图里的 关键数字" });
    const withoutImage = fixtureItem();
    storeItemsMock.mockResolvedValue(result([withImage, withoutImage]));
    await renderChannelDetail();

    // 就位锚取卡 testid(右栏行预览与卡标题同词面,findByText 会多匹配)
    await screen.findByTestId(`feed-item-${withImage.id}`);
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
    await renderChannelDetail();

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
    await renderChannelDetail();
    await screen.findByText("条目 1");

    // 点标题 → 详情弹窗(弹开即记已读)→ Esc 关闭 → 已读卡在「未读」过滤下消失
    fireEvent.click(screen.getByText("条目 1"));
    expect(screen.getByTestId("feed-detail-dialog")).toBeTruthy();
    // 整屏画布(2026-10-11 主人令「弹框太小,要整个界面」):标记在 + 正文
    // 去内滚帽(主滚动区承接,不再 max-h-72 小窗内滚)
    expect(screen.getByTestId("feed-detail-dialog").getAttribute("data-fullcanvas")).toBe("true");
    expect(screen.getByTestId("feed-detail-content").className).not.toContain("max-h-72");
    fireEvent.keyDown(screen.getByRole("dialog"), { key: "Escape" });
    await waitFor(() => expect(screen.queryByTestId("feed-detail-dialog")).toBeNull());
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
    const first = renderScreen();
    // 条目卡在 3 级渠道详情里(v8 三级下钻):两次挂载都走 1→2→3 全程
    await openChannelList();
    fireEvent.click(await screen.findByTestId("feed-channel-row-Example"));
    const card = await screen.findByTestId(`feed-item-${item.id}`);
    fireEvent.click(within(card).getByRole("button", { name: "星标" }));
    first.unmount();

    await renderChannelDetail();
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
    await renderChannelDetail();

    const loadMore = await screen.findByRole("button", { name: "加载更早的条目" });
    // F2:hasMore(满页)时词面如实「已加载 N 条」,不再以全量词面静默低估
    // (v7:选中态条目计数 testid = feed-stream-count,右栏脚注独占 feed-count)
    expect(screen.getByTestId("feed-stream-count").textContent).toContain("已加载 50 / 50 条");
    fireEvent.click(loadMore);

    // 翻页请求带上页最旧条目的 (first_seen, id) 复合游标(C1:同刻条目也能推进;
    // v7 调用序 = 右栏铺底 → 选中渠道重查(source 作用域)→ 翻页,按形断言)
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenCalledWith({
        limit: 50,
        before: cursor,
        before_id: cursorId,
        source: "Example",
      }));
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
    await renderChannelDetail();
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
    healthMock.mockResolvedValue(healthResult({ first_run: true, categories: [] }));
    renderScreen();

    expect(await screen.findByText("还没有可运行的插件")).toBeTruthy();
    expect(screen.getByRole("button", { name: "去源管理" })).toBeTruthy();
    expect(screen.queryByRole("button", { name: /运行第一个插件/ })).toBeNull();
  });

  it("空流 CTA:点击 → health 取已加载插件 → run.start(yaml) → 采集中 → completed 刷新", async () => {
    storeItemsMock.mockResolvedValue(result([]));
    runStartMock.mockResolvedValue({
      run_id: 3, state: "running", yaml: "/home/config/ai-news.yaml", dry: false, db: "/home/myssia.db",
    });
    let emitEvent: ((event: { type: string; run_id: number }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string; run_id: number }) => void;
      return Promise.resolve(() => {});
    });
    renderScreen();

    fireEvent.click(await screen.findByRole("button", { name: /运行第一个插件/ }));
    await waitFor(() =>
      expect(runStartMock).toHaveBeenCalledWith({ yaml: "/home/config/ai-news.yaml" }),
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
  // v7 双栏监控台(AC25/AC26):右栏行列表 / 搜索过滤 / 选中动线。
  // v6 渠道瀑布流落地页与 feed-back-to-wall 动线随双栏收编退役。
  // -------------------------------------------------------------------------

  it("1 级类型卡墙(v8 AC29):类型以现存源划分出卡(渠道数 = 成员全集),竖版 min-h,计数已加载口径 title;渠道行退到 2 级", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "telegram", sources: [sourceEntry("telegram-durov", "tg_web")] }),
          categoryEntry({ id: "daily", sources: [sourceEntry("daily-digest", "prompt")] }),
          categoryEntry({ id: "web", sources: [sourceEntry("openai-news", "static_html")] }),
        ],
      }),
    );
    const anchor = dayWindowStart().getTime();
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({ source: "telegram-durov", title: "TG 最新消息", first_seen: new Date(anchor + 60_000).toISOString() }),
        fixtureItem({ source: "openai-news", title: "网页新闻", first_seen: new Date(anchor + 30_000).toISOString() }),
      ]),
    );
    await renderOverview();

    // 1 级:三类型卡直出(词表序 tg → site → daily),卡墙容器在场;渠道行不在此级
    expect(screen.getByTestId("feed-types-wall")).toBeTruthy();
    const tgCard = screen.getByTestId("feed-type-card-tg");
    const siteCard = screen.getByTestId("feed-type-card-site");
    const dailyCard = screen.getByTestId("feed-type-card-daily");
    // 卡序固定词表序(DOM 序 tg < site < daily)
    expect(tgCard.compareDocumentPosition(siteCard) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(siteCard.compareDocumentPosition(dailyCard) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    // 渠道数 = 成员全集(health 枚举完整)
    expect(tgCard.getAttribute("data-channels")).toBe("1");
    expect(siteCard.getAttribute("data-channels")).toBe("1");
    expect(dailyCard.getAttribute("data-channels")).toBe("1");
    // 竖版锚(min-h-[340px],主人「卡片高度 > 宽度」钉死)
    expect(tgCard.className).toContain("min-h-[340px]");
    // 等分契约(主人「高度宽度要一致」10-15):grid 等宽列 + 等高行,卡满格;
    // 瀑布流遗物(break-inside-avoid / mb-4)不得回流
    const wall = screen.getByTestId("feed-types-wall");
    expect(wall.className).toContain("grid");
    expect(wall.className).toContain("[grid-auto-rows:1fr]");
    expect(tgCard.className).toContain("h-full");
    expect(tgCard.className).not.toContain("break-inside-avoid");
    // 计数 title 已加载口径(未过 STATS 门,version 缺省 = 9;词面在 title)
    expect(tgCard.textContent).toContain("今日 1 条");
    expect(tgCard.textContent).toContain("未读 1");
    expect(within(tgCard).getAllByTitle(/已加载口径/).length).toBeGreaterThan(0);
    // 卡内最新预览带渠道名;1 级零渠道行、零条目卡
    expect(tgCard.textContent).toContain("durov");
    expect(screen.queryByTestId("feed-channel-list")).toBeNull();
    expect(screen.queryByTestId(/^feed-item-/)).toBeNull();

    // 2 级(TG):渠道行直出,行形/徽标/脚注全保留
    await openChannelList("tg");
    const tgRow = await screen.findByTestId("feed-channel-row-telegram-durov");
    expect(tgRow.getAttribute("data-channel-kind")).toBe("tg");
    expect(tgRow.textContent).toContain("净化摘要内容");
    expect(screen.getByTestId("feed-channel-unread-telegram-durov").textContent).toBe("1");
    // 未读徽标 title 注明已加载口径(stats 门未过 = loaded 缺省档)
    expect(screen.getByTestId("feed-channel-unread-telegram-durov").getAttribute("title")).toContain("已加载口径");
    expect(screen.getByTestId("feed-count").textContent).toContain("1 个渠道");
  });

  it("1 级类型卡聚合(v8):统计行退役,计数由类型卡承载(渠道数/今日 Σ/未读 Σ);1 级零读态分段零条目卡", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    await renderOverview();
    // 单一渠道(Example → site)→ 单一类型卡:渠道数 1、今日 2、未读 2
    // (纯派生 catalog 口径,stats 门未过)
    const siteCard = screen.getByTestId("feed-type-card-site");
    expect(siteCard.getAttribute("data-channels")).toBe("1");
    expect(siteCard.textContent).toContain("今日 2 条");
    expect(siteCard.textContent).toContain("未读 2");
    // sr-only 作用域词 = 全部情报(v7 总览词保留为屏级播报,不占视觉位)
    expect(screen.getByText("全部情报")).toBeTruthy();
    // 1 级:零条目卡、零读态分段、零渠道行(v8 = 卡 + 搜索的纯类型页)
    expect(screen.queryByTestId(/^feed-item-/)).toBeNull();
    expect(screen.queryByRole("group", { name: "读态过滤" })).toBeNull();
    expect(screen.queryByTestId("feed-channel-list")).toBeNull();
  });

  it("health 失败:类型卡退化为已加载条目 source(前缀判定 TG),不拦情报流", async () => {
    healthMock.mockRejectedValue(new Error("sidecar 未连接"));
    storeItemsMock.mockResolvedValue(result([fixtureItem({ source: "telegram-durov" })]));
    await renderOverview();
    // engine 词表缺席 → 前缀规约兜底:telegram-durov 落 TG 类型卡
    const tgCard = await screen.findByTestId("feed-type-card-tg");
    expect(tgCard.getAttribute("data-channels")).toBe("1");
    await openChannelList("tg");
    expect(screen.getByTestId("feed-channel-row-telegram-durov").getAttribute("data-channel-kind")).toBe("tg");
  });

  it("选中动线(v8 AC30,1→2→3 层层进入):点类型卡 → 2 级行列表 → 点行 = store.items 带 source 精确等值;返回钮回 2 级(本级无持久选中)", async () => {
    const newsA = fixtureItem({ source: "openai-news", title: "闻甲" });
    const newsB = fixtureItem({ source: "hf-blog", title: "闻乙" });
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result([newsA, newsB].filter((item) => !params?.source || item.source === params.source))),
    );
    renderScreen();

    // 1 级:site 类型卡(两渠道成员)→ 2 级行列表
    await openChannelList("site");
    expect(screen.getByTestId("feed-type-title").textContent).toContain("网站 · 2 个渠道");

    // 点行 → 3 级:流查询带 source 精确等值;他渠道条目不混;行无持久选中
    fireEvent.click(await screen.findByTestId("feed-channel-row-openai-news"));
    await screen.findByText("闻甲");
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith({ limit: 50, source: "openai-news" }),
    );
    expect(screen.queryByText("闻乙")).toBeNull();
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("openai-news");
    expect(screen.queryByTestId("feed-channel-list")).toBeNull(); // 3 级整页,行列表不在场

    // 返回钮回 2 级:行列表回归(catalog 常驻不重拉),本级无持久选中(v8 §2.3)
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    expect(await screen.findByTestId("feed-channel-row-hf-blog")).toBeTruthy();
    expect(screen.getByTestId("feed-channel-row-openai-news").getAttribute("data-selected")).toBe("false");

    // 再退:返回类型钮回 1 级卡墙
    fireEvent.click(screen.getByTestId("feed-back-to-types"));
    expect(await screen.findByTestId("feed-types-wall")).toBeTruthy();
  });

  it("Esc 回退链(v8 §7,3→2→1):3 级 Esc 回 2 级、2 级 Esc 回 1 级、1 级 no-op;详情弹窗开着 Esc 只关弹窗(弹窗守卫让位,复审铁律)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    await renderChannelDetail();
    // 弹窗开着:Esc 归 Radix 关弹窗(冒泡线挂 overlay),层级保持
    fireEvent.click(await screen.findByText("条目 1"));
    expect(screen.getByTestId("feed-detail-dialog")).toBeTruthy();
    fireEvent.keyDown(screen.getByRole("dialog"), { key: "Escape" });
    await waitFor(() => expect(screen.queryByTestId("feed-detail-dialog")).toBeNull());
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("Example");

    // 弹窗已闭:Esc 回上一级(3 → 2,渠道行列表回归、条目流退场)
    fireEvent.keyDown(window, { key: "Escape" });
    expect(await screen.findByTestId("feed-channel-list")).toBeTruthy();
    expect(screen.getByTestId("feed-channel-row-Example").getAttribute("data-selected")).toBe("false");
    expect(screen.queryByTestId("feed-item-1")).toBeNull();

    // 2 级再按 Esc:回 1 级(类型卡墙)
    fireEvent.keyDown(window, { key: "Escape" });
    expect(await screen.findByTestId("feed-types-wall")).toBeTruthy();

    // 1 级再按 Esc:no-op(卡墙仍在,零状态变化)
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.getByTestId("feed-types-wall")).toBeTruthy();

    // 2 级搜索词面 Esc 在框内 = 清词(框守卫),不回退层级
    await openChannelList("site");
    const search = screen.getByLabelText("搜索渠道") as HTMLInputElement;
    fireEvent.change(search, { target: { value: "Ex" } });
    fireEvent.keyDown(search, { key: "Enter" });
    expect(screen.getByTestId("feed-count").textContent).toContain("命中 1 / 1 个渠道");
    fireEvent.keyDown(search, { key: "Escape" });
    expect(await screen.findByTestId("feed-channel-row-Example")).toBeTruthy();
  });

  it("浮层 Esc 让位收口(深检 C1,P1):3 级关「显示选项」下拉 / 卡片右键菜单的 Esc 只关浮层不回退层级(基件已 preventDefault,window 侧 defaultPrevented 让位)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    await renderChannelDetail();
    await screen.findByTestId("feed-item-1");

    // ① 显示选项下拉:开 → Esc 关菜单 → 层级保持(不被踢回 2 级)
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    const menu = await screen.findByRole("menu");
    fireEvent.keyDown(menu, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("menu")).toBeNull());
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("Example");
    expect(screen.getByTestId("feed-item-1")).toBeTruthy();

    // ② 卡片右键菜单:同象复验(菜单自闭,层级保持)
    fireEvent.contextMenu(screen.getByTestId("feed-item-1"));
    const ctxMenu = await screen.findByRole("menu");
    fireEvent.keyDown(ctxMenu, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("menu")).toBeNull(), { timeout: 1000 });
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("Example");
    expect(screen.getByTestId("feed-item-1")).toBeTruthy();

    // ③ 无浮层时裸 Esc 照旧回上一级(C1 收口不误伤既有语义)
    fireEvent.keyDown(window, { key: "Escape" });
    expect(await screen.findByTestId("feed-channel-list")).toBeTruthy();
  });

  it("搜索(v8 §4.3):1 级搜「Tg」仅 TG 类型卡直出(别名前缀);2 级搜「Tg」渠道行直出、网站行不混;清空恢复;零命中给行内专属空态", async () => {
    // 主人实测回归锚(10-09「搜 Tg 出不来 telegram 卡片」):
    // TG 最后入库在昨日(当日窗外)—— 类型卡/渠道行集合不受当日窗裁剪
    const tg = fixtureItem({
      source: "telegram-durov",
      title: "昨日 TG 消息",
      first_seen: new Date(Date.now() - 3 * 86_400_000).toISOString(),
    });
    const web = fixtureItem({ source: "openai-news", title: "网页新闻" });
    storeItemsMock.mockResolvedValue(result([tg, web]));
    await renderOverview();

    // 1 级:搜「Tg」= 类型别名前缀命中 → 仅 TG 类型卡(feed-type-search)
    const typeSearch = screen.getByLabelText("搜索类型") as HTMLInputElement;
    fireEvent.change(typeSearch, { target: { value: "Tg" } });
    expect(await screen.findByTestId("feed-type-card-tg")).toBeTruthy();
    await waitFor(() => expect(screen.queryByTestId("feed-type-card-site")).toBeNull());
    // 清空恢复全量(Esc 即时)
    fireEvent.keyDown(typeSearch, { key: "Escape" });
    expect(await screen.findByTestId("feed-type-card-site")).toBeTruthy();
    // 1 级零命中:卡墙位行内小空态
    fireEvent.change(typeSearch, { target: { value: "微信" } });
    expect(await screen.findByTestId("feed-type-search-empty")).toBeTruthy();
    expect(screen.getByTestId("feed-type-search-empty").textContent).toContain("没有匹配的类型");
    fireEvent.keyDown(typeSearch, { key: "Escape" });

    // 2 级(site 下渠道列表里搜 Tg 不命中;TG 语义在 TG 类型卡内)
    await openChannelList("tg");
    await screen.findByTestId("feed-channel-row-telegram-durov");
    const search = screen.getByLabelText("搜索渠道") as HTMLInputElement;
    fireEvent.change(search, { target: { value: "Tg" } });
    fireEvent.keyDown(search, { key: "Enter" });
    expect(await screen.findByTestId("feed-channel-row-telegram-durov")).toBeTruthy();
    expect(screen.getByTestId("feed-count").textContent).toContain("命中 1 / 1 个渠道");
    expect(screen.getByTestId("feed-channel-search-note").textContent).toContain("Tg");
    // 清空恢复全量(Esc 即时,不等防抖;搜索注退场)
    fireEvent.keyDown(search, { key: "Escape" });
    await waitFor(() => expect(screen.queryByTestId("feed-channel-search-note")).toBeNull());
    await waitFor(() => expect(screen.getByTestId("feed-count").textContent).toContain("1 个渠道"));

    // 2 级零命中:行内小空态文案(不再误导为「情报流是空的」)
    fireEvent.change(search, { target: { value: "不存在的渠道" } });
    fireEvent.keyDown(search, { key: "Enter" });
    expect(await screen.findByTestId("feed-search-empty")).toBeTruthy();
    expect(screen.getByTestId("feed-search-empty").textContent).toContain("没有匹配的渠道");
  });

  it("头部件随级分叉(v8 §1.4/§3.1):1 级 = 搜索+刷新+⋯菜单(批量/导出收纳),无读态分段无 feed-toolbar;3 级 = 返回/读态分段/条目计数/显示选项,无批量无导出;刷新钮重发当前域查询", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderOverview();
    await screen.findByTestId("feed-type-card-site");

    // 1 级头部:类型搜索 + 刷新 + ⋯ 菜单;读态分段/显示选项/返回钮/feed-toolbar 不渲染;
    // 批量/导出 = 菜单项收纳(非 button 面);渠道搜索不在此级
    expect(screen.queryByTestId("feed-toolbar")).toBeNull();
    expect(screen.queryByRole("group", { name: "读态过滤" })).toBeNull();
    expect(screen.queryByRole("button", { name: "显示选项" })).toBeNull();
    expect(screen.queryByTestId("feed-back-to-types")).toBeNull();
    expect(screen.queryByTestId("feed-back-to-channels")).toBeNull();
    expect(screen.queryByLabelText("搜索渠道")).toBeNull();
    expect(screen.getByLabelText("搜索类型")).toBeTruthy();
    expect(screen.getAllByRole("button", { name: "刷新" })).toHaveLength(1);
    expect(screen.queryByTestId("feed-stream-count")).toBeNull(); // 条目计数仅 3 级
    // ⋯ 菜单:导出 JSONL/CSV + 批量标读(全库级动作收纳)
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const menu = await screen.findByRole("menu");
    for (const name of ["导出 JSONL", "导出 CSV", "全部标已读…", "全部标未读…"]) {
      expect(within(menu).getByRole("menuitem", { name })).toBeTruthy();
    }
    fireEvent.keyDown(menu, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("menu")).toBeNull());
    const overviewCalls = storeItemsMock.mock.calls.length;
    fireEvent.click(screen.getByRole("button", { name: "刷新" }));
    await waitFor(() => expect(storeItemsMock.mock.calls.length).toBeGreaterThan(overviewCalls));

    // 3 级工具条:返回钮 + 读态分段 + 显示选项 + feed-stream-count;批量/导出菜单不渲染
    await openChannelList("site");
    fireEvent.click(screen.getByTestId("feed-channel-row-Example"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "Example" })),
    );
    await screen.findByText("条目 1");
    const detailToolbar = screen.getByTestId("feed-toolbar");
    const segmented = within(detailToolbar).getByRole("group", { name: "读态过滤" });
    for (const label of ["未读", "星标", "稍后读", "全部"]) {
      expect(within(segmented).getByRole("button", { name: `过滤:${label}` })).toBeTruthy();
    }
    expect(within(detailToolbar).getByRole("button", { name: "显示选项" })).toBeTruthy();
    expect(within(detailToolbar).getByTestId("feed-back-to-channels")).toBeTruthy();
    expect(within(detailToolbar).queryByRole("button", { name: "更多操作" })).toBeNull();
    expect(screen.getByTestId("feed-stream-count")).toBeTruthy();

    // 3 级刷新:重发带 source 的作用域查询
    const calls = storeItemsMock.mock.calls.length;
    fireEvent.click(within(detailToolbar).getByRole("button", { name: "刷新" }));
    await waitFor(() => expect(storeItemsMock.mock.calls.length).toBeGreaterThan(calls));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "Example" })),
    );
  });

  it("R1 Mod+F(v8 三级落点):⌘F/Ctrl+F 拦截浏览器查找(preventDefault)改聚焦当前级搜索框并全选词面 —— 1 级类型搜索 / 2 级渠道搜索", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderOverview();
    await screen.findByTestId("feed-type-card-site");

    // 1 级:聚焦类型搜索
    const typeSearch = screen.getByLabelText("搜索类型") as HTMLInputElement;
    fireEvent.change(typeSearch, { target: { value: "GLM" } });
    const notPrevented = fireEvent.keyDown(window, { key: "f", metaKey: true });
    expect(notPrevented).toBe(false);
    expect(document.activeElement).toBe(typeSearch);
    expect(typeSearch.selectionStart).toBe(0);
    expect(typeSearch.selectionEnd).toBe("GLM".length);

    // 清词后下钻 2 级:聚焦渠道搜索
    fireEvent.keyDown(typeSearch, { key: "Escape" });
    await openChannelList("site");
    const search = screen.getByLabelText("搜索渠道") as HTMLInputElement;
    fireEvent.change(search, { target: { value: "Ex" } });
    fireEvent.keyDown(window, { key: "f", ctrlKey: true });
    expect(document.activeElement).toBe(search);
    expect(search.selectionStart).toBe(0);
    expect(search.selectionEnd).toBe("Ex".length);
  });

  it("Mod+F 在 3 级(渠道内检索框;检索词独立不跨级)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderChannelDetail();
    await screen.findByText("条目 1");
    // 拦截照常(preventDefault),落点 = 渠道内检索框;时间线原地不动
    const notPrevented = fireEvent.keyDown(window, { key: "f", metaKey: true });
    expect(notPrevented).toBe(false);
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("Example");
    await waitFor(() => expect(document.activeElement).toBe(screen.getByLabelText("渠道内检索")));
  });

  it("G2 卡片展开:展开按钮出全文与元信息,再点收起回两行摘要", async () => {
    const item = fixtureItem({ content: "第一行\n第二行\n第三行" });
    storeItemsMock.mockResolvedValue(result([item]));
    await renderChannelDetail();
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
    await renderChannelDetail();
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
    await renderChannelDetail();
    await screen.findByText("条目 1");

    fireEvent.click(within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "打开原文" }));
    expect(await screen.findByTestId("feed-open-error")).toBeTruthy();
    expect(screen.getByTestId("feed-open-error").textContent).toContain("shell 未授权");
  });

  it("G3 导出(v8 ⋯ 菜单直选格式):菜单项 → dialog.save 默认名带日期 → feed.export 全库直出 → 回显 path/count;CSV 菜单项同门", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    await renderOverview();
    await screen.findByTestId("feed-type-card-site");

    dialogSaveMock.mockResolvedValue("/tmp/myssia-feed-export.jsonl");
    const exportResult: FeedExportResult = { path: "/tmp/myssia-feed-export.jsonl", count: 1, bytes: 640 };
    feedExportMock.mockResolvedValue(exportResult);

    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "导出 JSONL" }));
    await waitFor(() => expect(feedExportMock).toHaveBeenCalled());
    expect(feedExportMock).toHaveBeenCalledWith({ format: "jsonl", path: "/tmp/myssia-feed-export.jsonl" });
    expect(dialogSaveMock).toHaveBeenCalledWith(
      expect.objectContaining({ defaultPath: expect.stringMatching(/^myssia-feed-\d{8}\.jsonl$/) }),
    );
    expect(await screen.findByTestId("feed-export-result")).toBeTruthy();
    expect(screen.getByTestId("feed-export-result").textContent).toContain("/tmp/myssia-feed-export.jsonl");
    expect(screen.getByTestId("feed-export-result").textContent).toContain("1 条");

    // CSV 菜单项直选 csv 词表(格式切换态退役,菜单直选)
    dialogSaveMock.mockResolvedValue("/tmp/myssia-feed-export.csv");
    feedExportMock.mockResolvedValue({ path: "/tmp/myssia-feed-export.csv", count: 1, bytes: 120 });
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "导出 CSV" }));
    await waitFor(() =>
      expect(feedExportMock).toHaveBeenLastCalledWith({ format: "csv", path: "/tmp/myssia-feed-export.csv" }),
    );
  });

  it("G3 导出:对话框取消 = 静默(零 RPC 零回显);export_write_failed 错误回显", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderOverview();
    await screen.findByTestId("feed-type-card-site");

    dialogSaveMock.mockResolvedValue(null);
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "导出 JSONL" }));
    await waitFor(() => expect(dialogSaveMock).toHaveBeenCalled());
    expect(feedExportMock).not.toHaveBeenCalled();
    expect(screen.queryByTestId("feed-export-result")).toBeNull();

    dialogSaveMock.mockResolvedValue("/tmp/again.jsonl");
    feedExportMock.mockRejectedValue(
      new SidecarRequestError({ code: "export_write_failed", path: "params.path", message: "磁盘满" }),
    );
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "导出 JSONL" }));
    expect(await screen.findByTestId("feed-export-result")).toBeTruthy();
    expect(screen.getByTestId("feed-export-result").textContent).toContain("export_write_failed");
  });

  it("G3 导出收纳 ⋯ 菜单(§1.4,拷问 R1-Q3):导出菜单项在刷新钮之后的溢出面内可达(无头化回归闸)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderOverview();
    await screen.findByTestId("feed-type-card-site");

    // 1 级头部 = 搜索 + 刷新 + ⋯ 菜单(2 视觉位);导出/批量在菜单内可达
    const refresh = screen.getByRole("button", { name: "刷新" });
    const moreTrigger = screen.getByRole("button", { name: "更多操作" });
    expect(refresh.compareDocumentPosition(moreTrigger) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    fireEvent.click(moreTrigger);
    const menu = await screen.findByRole("menu");
    expect(within(menu).getByRole("menuitem", { name: "导出 JSONL" })).toBeTruthy();
    expect(within(menu).getByRole("menuitem", { name: "导出 CSV" })).toBeTruthy();
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
    await renderChannelDetail();
    // 就位锚取卡 testid(item 无正文 → 右栏行预览回退标题,findByText 会多匹配)
    await screen.findByTestId(`feed-item-${item.id}`);

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
    await renderChannelDetail();
    // 就位锚取卡 testid(bare 无正文 → 右栏行预览回退标题,findByText 会多匹配)
    await screen.findByTestId(`feed-item-${bare.id}`);

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
    await renderChannelDetail();
    // 就位锚取卡 testid(item 无正文 → 右栏行预览回退标题,findByText 会多匹配)
    await screen.findByTestId(`feed-item-${item.id}`);

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

  it("D4 品类色条与未读竖条(F4 修后口径):未读 = accent 竖条;已读 = 统一降饱和灰(品类色不再落竖条,只留品类徽章通道)", async () => {
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
    await renderChannelDetail();
    await screen.findByText("条目 1");
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));

    // 未读卡:data-unread=true,竖条 = 品牌紫亮档 #9869f7(primary-300,卡底
    // 4.40:1 过非文字 3:1;#631bf3 2.30:1 验收挑刺后提档),无 inline 色
    const unreadCard = screen.getByTestId(`feed-item-${unread.id}`);
    expect(unreadCard.getAttribute("data-unread")).toBe("true");
    const unreadStrip = screen.getByTestId(`feed-strip-${unread.id}`);
    expect(unreadStrip.className).toContain("bg-[#9869f7]");
    expect(unreadStrip.style.backgroundColor).toBe("");

    // 已读卡(F4):竖条 = 统一降饱和灰(bg-muted-foreground/40),品类色散列
    // 可落紫系与未读 accent 同色相 —— 读态不再吃品类色
    const readCard = screen.getByTestId(`feed-item-${read.id}`);
    expect(readCard.getAttribute("data-unread")).toBe("false");
    const readStrip = screen.getByTestId(`feed-strip-${read.id}`);
    expect(readStrip.className).toContain("bg-muted-foreground/40");
    expect(readStrip.style.backgroundColor).toBe("");
    // 已读标题降档(F4):与未读纯白拉开
    const readTitleBtn = within(readCard).getByText("条目 2").closest("button");
    expect(readTitleBtn?.className).toContain("text-muted-foreground");

    // 品类徽标着色同源(色条通道退役后,品类色只承担徽章)
    const chip = screen.getByText("ai-news");
    expect(chip.style.color).toBe(asRgb(categoryColor("ai-news") as string));

    // 已读且无品类:竖条恒在(统一灰档,不再按品类有无而消失)
    expect(screen.getByTestId(`feed-strip-${readNoCategory.id}`).className).toContain("bg-muted-foreground/40");
  });

  it("D4 hover 浮现操作:行背景 accent/50,操作簇 opacity-0→hover 显(focus-within 可达),time 让位", async () => {
    const item = fixtureItem({ url: "https://example.com/story" });
    storeItemsMock.mockResolvedValue(result([item]));
    await renderChannelDetail();
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

  it("网站渠道条目流(v7 §2.3)单列纵向列表:零时间组头,feed-stream-list 容器在场(时间语义由卡面相对时间承担)", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    await renderChannelDetail();

    expect(await screen.findByTestId("feed-item-1")).toBeTruthy();
    expect(screen.queryByTestId(/^feed-group-/)).toBeNull();
    // v6 columns 多列瀑布流降为单列列表(名实相符:feed-waterfall → feed-stream-list)
    const list = screen.getByTestId("feed-stream-list");
    expect(list.className).toContain("flex-col");
    expect(list.className).toContain("mx-auto"); // v9:居中窄列(TG 网页版宽屏同款)
    expect(list.className).not.toContain("columns");
  });

  it("D4 U 快捷键(渠道详情内):hover 进入条目卡后按 U 切已读(未读过滤下离场)", async () => {
    const item = fixtureItem();
    const other = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item, other]));
    await renderChannelDetail();
    await screen.findByText("条目 1");

    fireEvent.mouseEnter(screen.getByTestId(`feed-item-${item.id}`));
    fireEvent.keyDown(window, { key: "u" });
    // 当前卡转已读 → 默认「未读」过滤下消失;另一卡不受牵连
    await waitFor(() => expect(screen.queryByTestId(`feed-item-${item.id}`)).toBeNull());
    expect(screen.getByTestId(`feed-item-${other.id}`).getAttribute("data-current")).toBe("false");
  });

  it("D4 加载态:1 级类型卡形骨架(feed-types-loading)常驻至铺底应答,应答后卸载(冷启动无 CTA 闪现)", async () => {
    // 挂载首发 = 全库铺底查询(catalog 域):挂起期间卡形骨架常驻
    const resolvers: Array<(value: StoreItemsResult) => void> = [];
    storeItemsMock.mockImplementation(
      () => new Promise<StoreItemsResult>((resolve) => {
        resolvers.push(resolve);
      }),
    );
    renderScreen();

    expect(await screen.findByTestId("feed-types-loading")).toBeTruthy();
    expect(screen.queryByTestId(/^feed-type-card-/)).toBeNull();
    // 冷启动防闪(§1.5):catalog 在途一拍,空态主体(firstRun/CTA)不出
    expect(screen.queryByTestId("feed-run-cta")).toBeNull();
    expect(screen.queryByText("情报流还是空的")).toBeNull();
    act(() => resolvers.splice(0).forEach((resolve) => resolve(result([fixtureItem()]))));
    await screen.findByTestId("feed-type-card-site");
    expect(screen.queryByTestId("feed-types-loading")).toBeNull();
  });

  it("D4 错误态:结构化错误卡带重试按钮,点击重发 store.items 并恢复(catalog 域错落 1 级主体位)", async () => {
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
    await screen.findByTestId("feed-type-card-site");
    expect(screen.queryByTestId("feed-error")).toBeNull();
  });

  // -------------------------------------------------------------------------
  // fe-small-batch 批(10-03-fe-small-batch):G8 AI 摘要 / G9 批量 /
  // G12 沉淀为关键词 / P2⑤ 搜索框焦点环
  // -------------------------------------------------------------------------

  it("G8 AI 摘要:点击 → feed.enrich(dedup_key)→ 复合分/模型/维度分/缓存命中上屏,scores 并回刷新徽标", async () => {
    const item = fixtureItem({ scores: { tech: 0.87 } });
    storeItemsMock.mockResolvedValue(result([item]));
    await renderChannelDetail();
    await screen.findByText("条目 1");
    expect(screen.getByText("0.87")).toBeTruthy(); // 初始分数徽标

    feedEnrichMock.mockResolvedValue({
      item_id: item.id,
      model: "test-model",
      scores: { 相关性: 8, 新颖性: 6 },
      score: 7.2,
      cached: true,
    } as FeedEnrichResult);

    fireEvent.click(within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "AI 评分" }));
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

  it("G8 loading 态:请求在途按钮禁用 + 「评分中…」行", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    await renderChannelDetail();
    await screen.findByText("条目 1");

    feedEnrichMock.mockImplementation(() => new Promise<FeedEnrichResult>(() => {}));
    const button = within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "AI 评分" });
    fireEvent.click(button);

    expect(await screen.findByTestId(`feed-enrich-loading-${item.id}`)).toBeTruthy();
    expect(button.getAttribute("disabled")).not.toBeNull();
  });

  it("G8 无配置 graceful:enrich_not_configured 明示「未配置 AI 评分」(不伪装成传输错误),按钮可重试", async () => {
    const item = fixtureItem();
    storeItemsMock.mockResolvedValue(result([item]));
    await renderChannelDetail();
    await screen.findByText("条目 1");

    feedEnrichMock.mockRejectedValue(
      new SidecarRequestError({
        code: "enrich_not_configured",
        path: "params.item",
        message: "无法进行 AI 评分:品类 'tech' 未启用 AI 评分;到 设置 的 AI 评分区启用该品类并配好模型端点",
        data: { category: "tech", reason: "enrich_disabled" },
      }),
    );
    const button = within(screen.getByTestId(`feed-item-${item.id}`)).getByRole("button", { name: "AI 评分" });
    fireEvent.click(button);

    const error = await screen.findByTestId(`feed-enrich-error-${item.id}`);
    expect(error.textContent).toContain("未配置 AI 评分");
    expect(error.textContent).toContain("未启用 AI 评分");
    expect(error.getAttribute("title")).toContain("enrich_not_configured");
    await waitFor(() => expect(button.getAttribute("disabled")).toBeNull());
  });

  it("G9 全部标已读(1 级 ⋯ 菜单发起,全库语义):菜单项 → 头部确认簇(拷问 R1-Q3 兄弟位)→ 二次确认生效 → 类型卡未读即时清零 + 本地持久;全部标未读可还原", async () => {
    const items = [fixtureItem(), fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    await renderOverview();
    const siteCard = await screen.findByTestId("feed-type-card-site");
    expect(siteCard.textContent).toContain("未读 3");

    // R2:一次点击(菜单项)只进确认态,再点「确认」才生效(两路同门,未过门不豁免)
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" }));
    // 菜单按默认行为关闭,确认簇渲染在头部(菜单外兄弟位,拷问 R1-Q3)
    await waitFor(() => expect(screen.queryByRole("menu")).toBeNull());
    const confirm = await screen.findByRole("button", { name: "确认全部标已读" });
    expect(screen.getByTestId("feed-confirm-all-group")).toBeTruthy();
    fireEvent.click(confirm);

    // 批量入口在 1 级(3 级渠道语境不出钮):类型卡未读就地清零
    await waitFor(() => expect(screen.getByTestId("feed-type-card-site").textContent).toContain("未读 0"));
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.states.v1") ?? "{}");
    for (const item of items) {
      expect((persisted as Record<string, { read?: boolean }>)[item.dedup_key]?.read).toBe(true);
    }

    // 全部标未读还原:同一条菜单 → 确认簇动线
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标未读…" }));
    fireEvent.click(await screen.findByRole("button", { name: "确认全部标未读" }));
    await waitFor(() => expect(screen.getByTestId("feed-type-card-site").textContent).toContain("未读 3"));
  });

  it("G9 无未读时批量菜单项禁用(过门读态派生;空库 = 零源空态 CTA 另测)", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    storeItemsMock.mockResolvedValue(result([fixtureItem({ read: true }), fixtureItem({ read: true })]));
    await renderOverview();
    await screen.findByTestId("feed-type-card-site");
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const item = within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" });
    // 禁用菜单项 = 原生 disabled 属性(ui/dropdown-menu 投影,零 RPC 面)
    expect(item.getAttribute("disabled")).not.toBeNull();
  });

  it("P2⑤:搜索框焦点环归全局 :focus-visible 体系(无局部 ring-1/focus-visible 覆写)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderOverview();
    await openChannelList("site");
    const input = screen.getByLabelText("搜索渠道");
    expect(input.className).not.toContain("ring-1");
    expect(input.className).not.toContain("focus-visible");
  });

  it("G12 沉淀为关键词:面板只列 parse_ok 目标,词面默认条目标题;read(mtime)→ 手术 → save → 回执带 .bak", async () => {
    const item = fixtureItem({ title: "GLM-5 发布" });
    storeItemsMock.mockResolvedValue(result([item]));
    await renderChannelDetail();
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
      params: { file: "/home/config/ai-news.yaml" },
    });
    // 手术内容:keywords 闭括号前追加新词,注释/其余行(含 id 行)逐字节不动;
    // expected_mtime = read 带回的乐观锁基线
    expect(saves[0]).toEqual({
      file: "/home/config/ai-news.yaml",
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
    await renderChannelDetail();
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
    await renderChannelDetail();
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
    await renderChannelDetail();
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

describe("FeedScreen · interaction-batch(A-feed,v8 三层单环)", () => {
  it("2 级渠道行 j/k 巡游(v8 §7,v7 机件原样):首按 j 选中首行(focus 环可见),j/k 上下移,首末边界钳制不回绕;Enter 打开当前行渠道", async () => {
    // first_seen 显式钉死递减(a 新→c 旧):渠道行按 latest 活跃优先排序
    // (feedChannelCards,api.ts),缺省夹具取创建毫秒 —— 同毫秒平局走 key
    // 字典序恰为 a,b,c,跨毫秒则行序随机排列,j 落首行不再必是 a(门禁
    // 实录的 1-in-N 偶发红);钉时间后行序恒定
    const items = [
      fixtureItem({ source: "a-source", title: "甲", first_seen: new Date(Date.now() - 60_000).toISOString() }),
      fixtureItem({ source: "b-source", title: "乙", first_seen: new Date(Date.now() - 120_000).toISOString() }),
      fixtureItem({ source: "c-source", title: "丙", first_seen: new Date(Date.now() - 180_000).toISOString() }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(items.filter((item) => !params?.source || item.source === params.source))),
    );
    // jsdom 无 scrollIntoView 实现:注入 spy 断言「最近侧滚入」调用(测后还原)
    const originalScroll = Element.prototype.scrollIntoView;
    Element.prototype.scrollIntoView = vi.fn();
    try {
      await renderOverview();
      await openChannelList("site");
      const first = screen.getByTestId("feed-channel-row-a-source");
      expect(first.getAttribute("data-current")).toBe("false"); // 未巡游
      fireEvent.keyDown(window, { key: "j" });
      expect(first.getAttribute("data-current")).toBe("true");
      expect(first.getAttribute("data-nav-focused")).toBe("true");
      expect(first.className).toContain("ring-1"); // focus 环可见(A-feed 要点)
      expect(first.className).toContain("ring-primary");
      expect(Element.prototype.scrollIntoView).toHaveBeenCalledWith({ block: "nearest" });

      // 首行 k:钳制原地不动(不回绕到末行)
      fireEvent.keyDown(window, { key: "k" });
      expect(first.getAttribute("data-current")).toBe("true");

      // j → 第二行;前行让位
      fireEvent.keyDown(window, { key: "j" });
      const second = screen.getByTestId("feed-channel-row-b-source");
      expect(second.getAttribute("data-current")).toBe("true");
      expect(first.getAttribute("data-current")).toBe("false");

      // 末行再 j:钳制原地不动(不回绕回首行)
      fireEvent.keyDown(window, { key: "j" });
      fireEvent.keyDown(window, { key: "j" });
      expect(screen.getByTestId("feed-channel-row-c-source").getAttribute("data-current")).toBe("true");
      fireEvent.keyDown(window, { key: "j" });
      expect(screen.getByTestId("feed-channel-row-c-source").getAttribute("data-current")).toBe("true");

      // Enter = 打开当前行渠道(AC30 键盘动线):3 级载入该渠道流
      fireEvent.keyDown(window, { key: "Enter" });
      await waitFor(() =>
        expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "c-source" })),
      );
      expect(screen.getByTestId("feed-stream-title").textContent).toContain("c-source");
    } finally {
      Element.prototype.scrollIntoView = originalScroll;
    }
  });

  it("2 级 U triage(未过门本地通路):j 落行 + U = 该渠道已加载条目一键标已读(localStorage 持久,行徽标即时熄灭);已加载 0 条 = 无操作", async () => {
    // first_seen 显式钉死递减:渠道行按 latest 活跃优先排序,「j 落首行 =
    // a-source」依赖行序确定(同 flake 机理注,见 j/k 巡游用例)
    const item = fixtureItem({ source: "a-source", first_seen: new Date(Date.now() - 60_000).toISOString() });
    const other = fixtureItem({ source: "b-source", first_seen: new Date(Date.now() - 120_000).toISOString() });
    storeItemsMock.mockResolvedValue(result([item, other]));
    await renderOverview();
    await openChannelList("site");
    await screen.findByTestId("feed-channel-row-a-source");

    // j 落首行(a-source)→ U = a-source 已加载条目全部标已读(triage 动作)
    fireEvent.keyDown(window, { key: "j" });
    fireEvent.keyDown(window, { key: "u" });
    // 本地通路写 localStorage;行徽标即时熄灭(b-source 行不受牵连)
    await waitFor(() =>
      expect(screen.getByTestId("feed-channel-row-a-source").getAttribute("data-unread")).toBe("false"),
    );
    const persisted: unknown = JSON.parse(localStorageStub.getItem("myssia.feed.states.v1") ?? "{}");
    expect((persisted as Record<string, { read?: boolean }>)[item.dedup_key]?.read).toBe(true);
    expect((persisted as Record<string, { read?: boolean }>)[other.dedup_key]?.read).toBeUndefined();

    // ── 第二幕(独立挂载):已加载 0 条 = 无操作,零写入 ──
    cleanup();
    localStorageStub.clear();
    healthMock.mockResolvedValue(
      healthResult({
        categories: [categoryEntry({ id: "idle", sources: [sourceEntry("idle-source", "static_html")] })],
      }),
    );
    storeItemsMock.mockResolvedValue(result([]));
    renderScreen();
    await openChannelList("site");
    await screen.findByTestId("feed-channel-row-idle-source");
    fireEvent.keyDown(window, { key: "j" });
    fireEvent.keyDown(window, { key: "u" });
    await waitFor(() => expect(screen.getByTestId("feed-channel-row-idle-source").getAttribute("data-current")).toBe("true"));
    expect(localStorageStub.getItem("myssia.feed.states.v1")).toBeNull();
  });

  it("2 级 U 在场校验(深检 C3,P2):搜索收窄把巡游行过滤出局后按 U 零操作(与 Enter 同门);搜索清巡游行回场后 U 照常 triage", async () => {
    // first_seen 显式钉死递减(行序确定,「j 落 a-source」不再赌毫秒平局)
    const itemA = fixtureItem({ source: "a-source", title: "甲", first_seen: new Date(Date.now() - 60_000).toISOString() });
    const itemB = fixtureItem({ source: "b-source", title: "乙", first_seen: new Date(Date.now() - 120_000).toISOString() });
    storeItemsMock.mockResolvedValue(result([itemA, itemB]));
    await renderOverview();
    await openChannelList("site");
    await screen.findByTestId("feed-channel-row-a-source");

    // j 巡游环落 a-source → 搜索收窄只留 b-source(a-source 行离场)
    fireEvent.keyDown(window, { key: "j" });
    expect(screen.getByTestId("feed-channel-row-a-source").getAttribute("data-current")).toBe("true");
    const search = screen.getByLabelText("搜索渠道") as HTMLInputElement;
    fireEvent.change(search, { target: { value: "b" } });
    fireEvent.keyDown(search, { key: "Enter" });
    await waitFor(() => expect(screen.queryByTestId("feed-channel-row-a-source")).toBeNull());
    // 焦点出输入框后按 U:listCurrentKey 指向的 a-source 已不在场 → 零操作
    search.blur();
    fireEvent.keyDown(window, { key: "u" });
    expect(screen.getByTestId("feed-channel-row-b-source").getAttribute("data-unread")).toBe("true");
    expect(localStorageStub.getItem("myssia.feed.states.v1")).toBeNull();

    // 对照:清搜索 a-source 回场(环仍在)→ U 照常 triage
    fireEvent.keyDown(search, { key: "Escape" });
    await screen.findByTestId("feed-channel-row-a-source");
    search.blur();
    fireEvent.keyDown(window, { key: "u" });
    await waitFor(() =>
      expect(screen.getByTestId("feed-channel-row-a-source").getAttribute("data-unread")).toBe("false"),
    );
    expect(screen.getByTestId("feed-channel-row-b-source").getAttribute("data-unread")).toBe("true");
  });

  it("3 级条目 j/k 巡游(v8 §7,Shift 层退役):j 选中首条目(focus 环可见),边界钳制;hover 让环退出", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    await renderChannelDetail();
    const first = await screen.findByTestId(`feed-item-${items[0].id}`);
    const second = screen.getByTestId(`feed-item-${items[1].id}`);

    // 裸 j:条目环,首按落首卡(v8 恢复 v6 旧语义,Shift 层消亡)
    fireEvent.keyDown(window, { key: "j" });
    expect(first.getAttribute("data-current")).toBe("true");
    expect(first.getAttribute("data-nav-focused")).toBe("true");
    expect(first.className).toContain("ring-1");
    // k 首卡:钳制原地不动(不回绕末卡)
    fireEvent.keyDown(window, { key: "k" });
    expect(first.getAttribute("data-current")).toBe("true");
    // j → 第二卡,前卡让位
    fireEvent.keyDown(window, { key: "j" });
    expect(second.getAttribute("data-current")).toBe("true");
    expect(first.getAttribute("data-current")).toBe("false");

    // hover 进入卡让环退出(data-current 仍在)
    fireEvent.mouseEnter(second);
    expect(second.className).not.toContain("ring-1");
    expect(second.getAttribute("data-current")).toBe("true");
  });

  it("三层单环隔离(v8 §7):1 级 j/k 只动类型卡环;3 级 j/k 只动条目环;各级环互不串扰", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    await renderOverview();
    await screen.findByTestId("feed-type-card-site");

    // 1 级:j 落类型卡环(tg 卡序在 site 前?卡序 = 词表序,visibleTypes 首位)
    fireEvent.keyDown(window, { key: "j" });
    const card = screen.getByTestId("feed-type-card-site");
    const tgCard = screen.queryByTestId("feed-type-card-tg");
    const firstCard = tgCard ?? card;
    expect(firstCard.getAttribute("data-current")).toBe("true");

    // 3 级:条目环独立(类型卡环状态不串入条目;渠道行零巡游面)
    await openChannelList("site");
    fireEvent.click(screen.getByTestId("feed-channel-row-Example"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "Example" })),
    );
    fireEvent.keyDown(window, { key: "j" });
    await waitFor(() =>
      expect(screen.getByTestId("feed-item-1").getAttribute("data-current")).toBe("true"),
    );
    expect(screen.getByTestId("feed-item-1").getAttribute("data-nav-focused")).toBe("true");
    expect(screen.queryByTestId("feed-type-card-site")).toBeNull(); // 3 级无类型卡

    // Enter = 开当前条目详情弹窗(3 级落点)
    fireEvent.keyDown(window, { key: "Enter" });
    expect(screen.getByTestId("feed-detail-dialog")).toBeTruthy();
  });

  it("j/k 守卫(2 级):输入框内敲 j 不动渠道行;⌘/Ctrl/Alt 修饰键不触发", async () => {
    // first_seen 显式钉死递减(行序确定,「裸 j 选中首行 a-source」不再赌毫秒平局)
    const items = [
      fixtureItem({ source: "a-source", title: "甲", first_seen: new Date(Date.now() - 60_000).toISOString() }),
      fixtureItem({ source: "b-source", title: "乙", first_seen: new Date(Date.now() - 120_000).toISOString() }),
    ];
    storeItemsMock.mockResolvedValue(result(items));
    await renderOverview();
    await openChannelList("site");
    await screen.findByTestId("feed-channel-row-a-source");

    const search = screen.getByLabelText("搜索渠道");
    fireEvent.change(search, { target: { value: "jk" } });
    fireEvent.keyDown(search, { key: "j" });
    fireEvent.keyDown(window, { key: "j", metaKey: true });
    fireEvent.keyDown(window, { key: "k", ctrlKey: true });
    for (const key of ["a-source", "b-source"]) {
      expect(screen.getByTestId(`feed-channel-row-${key}`).getAttribute("data-current")).toBe("false");
    }

    // 守卫外正常路径仍在:window 上裸按 j 选中首行渠道
    fireEvent.keyDown(window, { key: "j" });
    expect(screen.getByTestId("feed-channel-row-a-source").getAttribute("data-current")).toBe("true");
  });

  it("渠道行 Space 键激活(深检 F5):role=button 的 ARIA 双键语义 —— 空格与 Enter 同门进 3 级渠道详情", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem({ source: "a-source" })]));
    await renderOverview();
    await openChannelList("site");
    const row = await screen.findByTestId("feed-channel-row-a-source");
    row.focus();
    fireEvent.keyDown(row, { key: " " });
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "a-source" })),
    );
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("a-source");
  });

  it("3 级 j + U 联动:j 选中条目后按 U 切已读(默认未读过滤下当前卡离场)", async () => {
    const items = [fixtureItem(), fixtureItem()];
    storeItemsMock.mockResolvedValue(result(items));
    await renderChannelDetail();
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
    await renderChannelDetail();
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

  it("显示选项 · 分组维度(v5):瀑布流恒平铺零组头;时间/不分组两档持久(时间档在聊天视图出日期胶囊)", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    await renderChannelDetail();
    await screen.findByText("条目 1");

    // 瀑布流(v5 首屏)恒平铺:任何 groupMode 下根作用域零组头
    expect(screen.queryByTestId(/^feed-group-/)).toBeNull();

    // 菜单只有 时间/不分组 两档(品类维度随三级页退役,见 chips 用例)
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    const menu = await screen.findByRole("menu");
    expect(within(menu).queryByRole("menuitem", { name: "按品类分组" })).toBeNull();
    expect(within(menu).getByRole("menuitem", { name: "时间分组(今天 / 昨天 / 7 天内 / 更早)" }).querySelector("svg")).not.toBeNull();

    // 不分组:持久 groupMode = none(重开菜单勾选态同步)
    fireEvent.click(screen.getByRole("button", { name: "显示选项" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "不分组(平铺)" }));
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
      await renderChannelDetail();
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
    await renderChannelDetail();
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
    // 过门生效的可见标志(渠道墙):批量按钮 title 换全库真话
    await renderFreshChannelDetail(fresh);
    const card = screen.getByTestId("feed-item-1");
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
    await renderFreshChannelDetail(fresh);
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

  it("全部标已读 = 全库语义(1 级菜单入口):菜单项发起 → store.state.mark_all(不按已加载 keys);title 真话;类型卡未读就地归零不整页重拉", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 99 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByTestId("feed-type-card-site");
    // 菜单项 title 真话:含未翻页(全库),不再含「本地态/已加载」旧注记
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const readAll = within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" });
    await waitFor(() => expect(readAll.getAttribute("title")).toContain("全库"));
    const title = readAll.getAttribute("title") ?? "";
    expect(title).toContain("未翻页");
    expect(title).not.toContain("本地态");
    expect(title).not.toContain("已加载");
    fireEvent.click(readAll);
    // R2:一次点击只进确认态;确认态 title 延续全库真话(进确认态不掉如实度)
    const confirm = await screen.findByRole("button", { name: "确认全部标已读" });
    expect(confirm.getAttribute("title") ?? "").toContain("全库");
    expect(confirm.getAttribute("title") ?? "").not.toContain("已加载");
    fireEvent.click(confirm);
    await waitFor(() => expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: true }));
    expect(fresh.markMock).not.toHaveBeenCalled(); // 全库单 UPDATE,不逐键置位
    // 就地翻转已加载行:类型卡未读即时清零;不整页重拉
    await waitFor(() =>
      expect(screen.getByTestId("feed-type-card-site").textContent).toContain("未读 0"),
    );
    // 挂载仅 1 发 catalog 铺底查询,mark_all 后不再整页重拉
    expect(fresh.storeItemsMock.mock.calls.length).toBe(1);
  });

  it("全部标未读失败:按调用前快照回滚(不瞎翻)+ feed-mark-error 明示(1 级菜单入口)", async () => {
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
    await screen.findByTestId("feed-type-card-site");
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标未读…" }));
    fireEvent.click(await screen.findByRole("button", { name: "确认全部标未读" }));
    await waitFor(() => expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: false }));
    // 乐观:类型卡未读 1 → 2(甲乙都翻未读)
    await waitFor(() =>
      expect(screen.getByTestId("feed-type-card-site").textContent).toContain("未读 2"),
    );
    act(() =>
      rejectAll?.(new SidecarRequestError({ code: "store_corrupt", path: "$", message: "库损坏" })),
    );
    // 快照回滚:未读回到 1(甲回已读、乙保持未读)
    await waitFor(() =>
      expect(screen.getByTestId("feed-type-card-site").textContent).toContain("未读 1"),
    );
    const error = await screen.findByTestId("feed-mark-error");
    expect(error.textContent).toContain("store_corrupt");
  });

  it("2 级 U triage(过门服务端通路):单请求 storeStateMark(keys 数组),乐观双缓冲翻 —— 行徽标即时熄灭;失败按快照回滚", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markMock.mockResolvedValue({ updated: 2 });
    fresh.storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({ source: "t-a", title: "消息甲", url: "https://t.me/a/1" }),
        fixtureItem({ source: "t-a", title: "消息乙", url: "https://t.me/a/2" }),
      ]),
    );
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    // 2 级:t-a 无 telegram 前缀 = site 档 → site 类型卡 → 行列表;j 落 t-a 行 + U
    await openChannelList("site");
    await screen.findByTestId("feed-channel-row-t-a");
    fireEvent.keyDown(window, { key: "j" });
    fireEvent.keyDown(window, { key: "u" });
    // 单请求 keys 数组协议(既有 storeStateMark;非逐键 N 发)
    await waitFor(() =>
      expect(fresh.markMock).toHaveBeenCalledWith({
        keys: expect.arrayContaining(["dk-1", "dk-2"]),
        marker: "read",
        value: true,
      }),
    );
    expect(fresh.markMock).toHaveBeenCalledTimes(1);
    // 乐观双缓冲翻:行徽标即时熄灭
    await waitFor(() =>
      expect(screen.getByTestId("feed-channel-row-t-a").getAttribute("data-unread")).toBe("false"),
    );
  });

  it("双缓冲联动(v7 §3.2 机件保留,深检 C2):3 级内单条标读(条目仅存 streamItems)→ 双缓冲同翻,回 2 级行徽标即时降 + 失败回滚徽标回升;localStorage 零写入", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markMock.mockResolvedValue({ updated: 1 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem(), fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    // 3 级:下钻前 2 级行徽标 = catalog 铺底聚合(3 未读)
    await openChannelList("site");
    const row = screen.getByTestId("feed-channel-row-Example");
    expect(within(row).getByTestId("feed-channel-unread-Example").textContent).toBe("3");
    fireEvent.click(row);
    await screen.findByTestId("feed-item-1");

    // 单条标读(卡内悬停簇「标记已读」钮;条目仅存于 streamItems,states =
    // 双缓冲并集投影):单键 store.state.mark
    fireEvent.click(within(screen.getByTestId("feed-item-1")).getByRole("button", { name: "标记已读" }));
    await waitFor(() =>
      expect(fresh.markMock).toHaveBeenCalledWith({ keys: ["dk-1"], marker: "read", value: true }),
    );
    // 服务端唯一真源:本地快照零写入
    expect(localStorageStub.getItem("myssia.feed.states.v1")).toBeNull();

    // 回 2 级:徽标即时降(catalog 半边已同步翻,3 未读 → 2)
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    await waitFor(() =>
      expect(within(screen.getByTestId("feed-channel-row-Example")).getByTestId("feed-channel-unread-Example").textContent).toBe("2"),
    );

    // 失败回滚:下钻后第二条标读被拒 → 乐观翻按快照回升,徽标回到 2
    fireEvent.click(await screen.findByTestId("feed-channel-row-Example"));
    await screen.findByTestId("feed-item-2");
    fresh.markMock.mockRejectedValueOnce(
      new SidecarRequestError({ code: "internal_error", path: "$", message: "写库失败" }),
    );
    fireEvent.click(within(screen.getByTestId("feed-item-2")).getByRole("button", { name: "标记已读" }));
    const error = await screen.findByTestId("feed-mark-error");
    expect(error.textContent).toContain("internal_error");
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    await waitFor(() =>
      expect(within(screen.getByTestId("feed-channel-row-Example")).getByTestId("feed-channel-unread-Example").textContent).toBe("2"),
    );
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
    await screen.findByTestId("feed-type-card-site"); // 第二次挂载完成渲染
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
    await screen.findByTestId("feed-type-card-site");
    // 等能力门真正翻到服务端通路(⋯ 菜单项 title 现全库语义)再断言不发
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const importMenu = await screen.findByRole("menu");
    await waitFor(() =>
      expect(within(importMenu).getByRole("menuitem", { name: "全部标已读…" }).getAttribute("title")).toContain("全库"),
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
    await renderFreshChannelDetail(fresh);
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
    renderScreen();
    // 未过门生效的可见标志(1 级菜单):批量菜单项 title 仍是本地态注记
    await screen.findByTestId("feed-type-card-site");
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const gateMenu = await screen.findByRole("menu");
    await waitFor(() =>
      expect(within(gateMenu).getByRole("menuitem", { name: "全部标已读…" }).getAttribute("title")).toContain("本地态"),
    );
    fireEvent.keyDown(gateMenu, { key: "Escape" });
    // 条目卡在 3 级(v8 下钻):点类型卡 → 渠道行 → 星标
    await openChannelList("site");
    fireEvent.click(screen.getByTestId("feed-channel-row-Example"));
    const card = await screen.findByTestId("feed-item-1");
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
    await screen.findByTestId("feed-type-card-site");
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const failGateMenu = await screen.findByRole("menu");
    await waitFor(() =>
      expect(within(failGateMenu).getByRole("menuitem", { name: "全部标已读…" }).getAttribute("title")).toContain("本地态"),
    );
    fireEvent.keyDown(failGateMenu, { key: "Escape" });
    await openChannelList("site");
    fireEvent.click(screen.getByTestId("feed-channel-row-Example"));
    await screen.findByTestId("feed-item-1");
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

// ---------------------------------------------------------------------------
// g9-read-all 批(v6 迁移):全库批量入口在渠道墙工具条(品类维度随 AC23
// 退场,mark_all 恒全库语义)+ inline 二次确认(确认/取消/Esc/失焦四态)
// ---------------------------------------------------------------------------

describe("FeedScreen · g9-read-all(全库批量入口 + 二次确认,v8 1 级头部)", () => {
  it("批量入口唯一性:入口只在 1 级 ⋯ 菜单(组头零处可挂;3 级渠道语境零菜单零批量)", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 1 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByTestId("feed-type-card-site");
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const uniqueMenu = await screen.findByRole("menu");
    await waitFor(() =>
      expect(within(uniqueMenu).getByRole("menuitem", { name: "全部标已读…" }).getAttribute("title")).toContain("全库"),
    );
    fireEvent.keyDown(uniqueMenu, { key: "Escape" });

    // 1 级零组头:feed-group-* 不存在(组头批量入口无处可挂)
    expect(screen.queryByTestId(/^feed-group-/)).toBeNull();
    expect(screen.queryByTestId(/^feed-group-mark-all-/)).toBeNull();
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // 3 级渠道详情:批量菜单不渲染(mark_all 无 source 参数,范围不实则不出现)
    await openChannelList("site");
    fireEvent.click(screen.getByTestId("feed-channel-row-Example"));
    await screen.findByTestId("feed-item-1");
    expect(screen.queryByRole("button", { name: "更多操作" })).toBeNull();
    expect(screen.queryByRole("button", { name: "全部标已读" })).toBeNull();
  });

  it("R2 全库两按钮二次确认(菜单项发起、确认簇渲染在头部菜单外兄弟位,拷问 R1-Q3):一次点击只进确认态(零 RPC),再点「确认」才执行;取消 / Esc / 失焦三路退出且零执行", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 99 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByTestId("feed-type-card-site");

    // 一次点击(菜单项):菜单按默认行为关闭,确认簇在头部 —— mark_all 未发;
    // 确认态文案延续全库真话(过门不出现「已加载/本地态」字样,R4)
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" }));
    await waitFor(() => expect(screen.queryByRole("menu")).toBeNull());
    const confirm = await screen.findByRole("button", { name: "确认全部标已读" });
    expect(screen.getByTestId("feed-confirm-all-group")).toBeTruthy();
    expect(confirm.getAttribute("title") ?? "").toContain("全库");
    expect(confirm.getAttribute("title") ?? "").not.toContain("已加载");
    expect(confirm.getAttribute("title") ?? "").not.toContain("本地态");
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // Esc 退出:确认簇消失,零执行(1 级 Esc 本无回退语义,与确认收口无冲突)
    fireEvent.keyDown(window, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // 「取消」退出:零执行
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" }));
    fireEvent.click(await screen.findByRole("button", { name: "取消" }));
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // 失焦退出:blur 出确认钮簇即退
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" }));
    fireEvent.blur(await screen.findByTestId("feed-confirm-all-group"));
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(fresh.markAllMock).not.toHaveBeenCalled();

    // 再点执行:确认后 mark_all({marker:"read", value:true})发出;类型卡未读就地归零
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" }));
    fireEvent.click(await screen.findByRole("button", { name: "确认全部标已读" }));
    await waitFor(() => expect(fresh.markAllMock).toHaveBeenCalledWith({ marker: "read", value: true }));
    await waitFor(() =>
      expect(screen.getByTestId("feed-type-card-site").textContent).toContain("未读 0"),
    );
  });

  it("未过门:批量菜单项走本地通路语义(title 本地态真话,store.state.mark_all 零调用)", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL - 1));
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    renderScreen();
    await screen.findByTestId("feed-type-card-site");
    // 未过门:菜单项 title = 本地态真话(不宣称全库服务端持久)
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    const localMenu = await screen.findByRole("menu");
    await waitFor(() =>
      expect(within(localMenu).getByRole("menuitem", { name: "全部标已读…" }).getAttribute("title")).toContain("本地态"),
    );
    expect(markAllMock).not.toHaveBeenCalled();
  });

  it("质检件一键盘焦点:进入确认态后焦点自动落确认主钮(菜单关闭后 autoFocus 补位不回落 body);Esc 仍取消且零执行", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.markAllMock.mockResolvedValue({ updated: 99 });
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    render(
      <MemoryRouter>
        <fresh.FeedScreen />
      </MemoryRouter>,
    );
    await screen.findByTestId("feed-type-card-site");

    // 键盘路径:菜单项点击进确认态,菜单已关 —— autoFocus 补位,焦点落
    // 确认主钮(键盘/读屏用户无需重 Tab 定位;不回落 body)
    fireEvent.click(screen.getByRole("button", { name: "更多操作" }));
    fireEvent.click(within(await screen.findByRole("menu")).getByRole("menuitem", { name: "全部标已读…" }));
    const confirm = await screen.findByRole("button", { name: "确认全部标已读" });
    expect(document.activeElement).toBe(confirm);

    // Esc 全局收口不被程序化初始焦点破坏:确认态退出、零执行
    fireEvent.keyDown(confirm, { key: "Escape" });
    await waitFor(() => expect(screen.queryByRole("button", { name: "确认全部标已读" })).toBeNull());
    expect(fresh.markAllMock).not.toHaveBeenCalled();
  });

  it("质检件二知会:「过滤:未读」钮 title(v6 归渠道详情)注明会隐藏已读条目,其余页签不带(最小面)", async () => {
    const fresh = await importFreshScreen();
    fresh.versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    fresh.storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderFreshChannelDetail(fresh);
    const unread = screen.getByRole("button", { name: "过滤:未读" });
    expect(unread.getAttribute("title")).toContain("已读");
    expect(unread.getAttribute("title")).toContain("全部");
    // 知会特定于未读口径;其余页签零附加文案
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
// feed-channel-groups(10-06):品类分组下渠道二级分组 + 五档差异化卡面 +
// 实时滚动 + 当日窗 03:00 视图清零
// ---------------------------------------------------------------------------

/** health 夹具源条目(SourceReport 形状;engine = 渠道类型判定词表源) */
function sourceEntry(name: string, engine: string): HealthResult["categories"][number]["sources"][number] {
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

describe("FeedScreen · feed-channel-groups(渠道流差异化 + 实时滚动 + 当日窗,v8 迁移)", () => {
  it("类型分列(v8 AC30):TG 与网页各归类型卡,2 级行类型属性各显;点行各进各的 3 级流(TG = 聊天时间线,网站 = 条目单列)", async () => {
    const items = [
      fixtureItem({ source: "telegram-durov", title: "消息正文甲", content: "气泡内摘要" }),
      fixtureItem({ source: "openai-news", title: "新闻标题乙", category: "tech" }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(items.filter((item) => !params?.source || item.source === params.source))),
    );
    await renderOverview();

    // 1 级:两类型卡并列(tg / site 各自成员)
    expect(screen.getByTestId("feed-type-card-tg")).toBeTruthy();
    expect(screen.getByTestId("feed-type-card-site")).toBeTruthy();

    // TG 卡 → 2 级行(tg)→ 点行 → 聊天时间线(气泡 + 频道名行),网页条目不混
    await openChannelList("tg");
    const tgRow = await screen.findByTestId("feed-channel-row-telegram-durov");
    expect(tgRow.getAttribute("data-channel-kind")).toBe("tg");
    fireEvent.click(tgRow);
    expect(await screen.findByTestId("feed-tg-bubble-1")).toBeTruthy();
    expect(screen.queryByText("新闻标题乙")).toBeNull();
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("durov");

    // 回 2 级 → 回 1 级 → site 卡 → 点网页行 → 条目单列(news 卡),TG 气泡不混
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-back-to-types"));
    await openChannelList("site");
    fireEvent.click(await screen.findByTestId("feed-channel-row-openai-news"));
    const newsCard = await screen.findByTestId("feed-item-2");
    expect(newsCard.getAttribute("data-kind")).toBe("news");
    expect(screen.queryByTestId("feed-tg-bubble-1")).toBeNull();
  });

  it("urlwatch 渠道详情(engine 映射):「有更新」徽标 + 目标页链接(watch_page)+ 展开 diff 明细", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [categoryEntry({ id: "ai-news", sources: [sourceEntry("anthropic-news-watch", "urlwatch")] })],
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
    await renderChannelDetail("anthropic-news-watch");
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

  it("prompt 日报渠道详情(engine 映射):markdown 文档视图可折叠——收起单行摘要,展开出标题/列表/加粗", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [categoryEntry({ id: "ai-vendor-watch", sources: [sourceEntry("ai-vendor-watch", "prompt")] })],
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
    renderScreen();
    // 渠道行类型属性 = 日报(prompt engine)→ 2 级点行进 3 级流
    await openChannelList("daily");
    const wallCard = await screen.findByTestId("feed-channel-row-ai-vendor-watch");
    expect(wallCard.getAttribute("data-channel-kind")).toBe("daily");
    fireEvent.click(wallCard);
    await screen.findByTestId("feed-item-1");
    const card = screen.getByTestId("feed-item-1");
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

  it("games 价格优惠渠道详情:现价突出 + 原价划线 + 限免徽标(Epic 形态);CS 美元形态同渲(两渠道各进各的详情)", async () => {
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
    renderScreen();
    // Epic 渠道:2 级点行进 3 级流,价格优惠行直出
    await openChannelList("site");
    fireEvent.click(await screen.findByTestId("feed-channel-row-epic-free"));
    await screen.findByText("Epic 限免游戏");
    const epic = screen.getByTestId("feed-item-1");
    expect(epic.getAttribute("data-kind")).toBe("deal");
    const epicPrice = within(epic).getByTestId("feed-deal-price-1");
    expect(within(epicPrice).getByText("限免")).toBeTruthy();
    expect(within(epicPrice).getByText("¥0.00")).toBeTruthy();
    expect(within(epicPrice).getByText("¥39.00")).toBeTruthy(); // 原价分→元

    // 回 2 级 → CS 渠道流:美元形态
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-channel-row-cheapshark"));
    const cs = await screen.findByTestId("feed-item-2");
    const csPrice = within(cs).getByTestId("feed-deal-price-2");
    expect(within(csPrice).getByText("$0.50")).toBeTruthy();
    expect(within(csPrice).getByText("$16.99")).toBeTruthy();
    expect(within(csPrice).getByText("-97%")).toBeTruthy(); // savings_pct 字符串解析取整
    expect(within(csPrice).queryByText("限免")).toBeNull(); // CS 实测无 0 元 deal
  });

  it("实时滚动(1 级):cron.completed 事件 → catalog 静默合流,类型卡渠道数即时扩张(已加载渠道零扰动)", async () => {
    let emitEvent: ((event: { type: string }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string }) => void;
      return Promise.resolve(() => {});
    });
    const existing = fixtureItem({ source: "old-source", title: "旧行" });
    const fresh = fixtureItem({ source: "new-source", title: "新行" });
    // 铺底查询(挂载首发)只回旧行;事件后的 liveRefreshCatalog 才见新行
    let served = 0;
    storeItemsMock.mockImplementation(() => {
      served += 1;
      return Promise.resolve(result(served <= 1 ? [existing] : [fresh, existing]));
    });
    await renderOverview();
    const siteCard = await screen.findByTestId("feed-type-card-site");
    expect(siteCard.getAttribute("data-channels")).toBe("1");
    await openChannelList("site");
    expect(await screen.findByTestId("feed-channel-row-old-source")).toBeTruthy();
    expect(screen.queryByTestId("feed-channel-row-new-source")).toBeNull();

    // 事件合流后回 1 级:site 卡渠道数 1 → 2(新渠道进入成员集)
    fireEvent.click(screen.getByTestId("feed-back-to-types"));
    act(() => emitEvent?.({ type: "cron.completed" }));
    await waitFor(() =>
      expect(screen.getByTestId("feed-type-card-site").getAttribute("data-channels")).toBe("2"),
    );
    await openChannelList("site");
    expect(await screen.findByTestId("feed-channel-row-new-source")).toBeTruthy();
    expect(screen.getByTestId("feed-channel-row-old-source")).toBeTruthy(); // 已加载渠道零扰动
  });

  it("当日窗只作用于类型卡「今日」计数(v8 §5.2 口径,深检 F1 定案):窗外条目不计今日、未读不限窗;3 级渠道流全量直出(读态过滤照走)", async () => {
    const start = dayWindowStart();
    const outOfWindow = fixtureItem({
      title: "窗前旧条目",
      first_seen: new Date(start.getTime() - 3_600_000).toISOString(), // 窗起点前 1h,必在窗外
    });
    const inWindow = fixtureItem({ title: "窗内新条目" }); // now,必在窗内
    storeItemsMock.mockResolvedValue(result([outOfWindow, inWindow]));
    // 1 级类型卡:「今日」按窗计(窗外不计今日);未读不限窗(2 条)
    await renderOverview();
    const siteCard = screen.getByTestId("feed-type-card-site");
    expect(siteCard.textContent).toContain("今日 1 条");
    expect(siteCard.textContent).toContain("未读 2");
    await openChannelList("site");
    const row = screen.getByTestId("feed-channel-row-Example");
    expect(row.getAttribute("data-unread")).toBe("true");
    // 3 级:全量直出 —— 窗外条目在场(「加载更早」所见即所得的前提)
    fireEvent.click(row);
    await screen.findByText("窗前旧条目");
    expect(screen.getByText("窗内新条目")).toBeTruthy();
    expect(screen.getByTestId("feed-stream-count").textContent).toContain("2 / 2 条");
    expect(screen.getByTestId("feed-day-window").textContent).toContain("全量");
  });

  it("加载更早 × 窗界(深检 F8②):翻页加载的窗外条目即时可见,「点了加载不见卡」不再发生", async () => {
    const start = dayWindowStart();
    const page1: FeedItem[] = [];
    for (let i = 0; i < 50; i += 1) {
      page1.push(fixtureItem({ title: `窗内条目 ${i}`, first_seen: new Date().toISOString() }));
    }
    const page2 = [
      fixtureItem({
        title: "窗外旧条目",
        first_seen: new Date(start.getTime() - 3_600_000).toISOString(),
      }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) => {
      if (params?.before) return Promise.resolve(result(page2));
      return Promise.resolve(result(page1));
    });
    await renderChannelDetail();
    // 首页满页 → hasMore;翻页加载窗外条目:详情已无当日窗,所见即所得
    fireEvent.click(await screen.findByRole("button", { name: "加载更早的条目" }));
    expect(await screen.findByText("窗外旧条目")).toBeTruthy();
    expect(screen.getByTestId("feed-day-window").textContent).toContain("全量");
  });

  it("渠道详情空态阶梯(深检 F1/F4 后语义):未读无剩给「看全部条目(含已读)」,历史态已读未读全显且分段隐藏,退出回读态视图", async () => {
    // 过服务端读态门:已读态走条目派生(未过门通路只认 localStorage,条目
    // read 字段不参与过滤 —— fixture 注记同门)
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    storeItemsMock.mockResolvedValue(result([fixtureItem({ title: "三天前的已读入库", read: true })]));
    await renderChannelDetail();
    // 默认未读档:唯一条目已读 → 空态;给「看全部条目」直达(死胡同根除)
    expect(await screen.findByTestId("feed-empty-history")).toBeTruthy();
    fireEvent.click(screen.getByTestId("feed-empty-history"));
    // 历史态:已读未读全显,知会词换「全部历史」
    expect(await screen.findByText("三天前的已读入库")).toBeTruthy();
    expect(screen.getByTestId("feed-day-window").textContent).toContain("全部历史");
    // 深检 F4:历史态读态过滤不生效,分段随之隐藏(不给死控件)
    expect(screen.queryByRole("group", { name: "读态过滤" })).toBeNull();
    // 退出历史:回读态视图(未读档下已读条目重新离场)
    fireEvent.click(screen.getByTestId("feed-history-exit"));
    await waitFor(() => expect(screen.queryByText("三天前的已读入库")).toBeNull());
    // 回读态后显式切「全部」:已读条目回来(档位语义自洽,不依赖默认档)
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    await waitFor(() => expect(screen.getByText("三天前的已读入库")).toBeTruthy());
  });
});

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
    const categories = [
      categoryEntry({ sources: [sourceEntry("a", "urlwatch"), sourceEntry("b", "static_html")] }),
      categoryEntry({ sources: [sourceEntry("a", "prompt")] }), // 同名源首现优先
      categoryEntry({ sources: [] }),
    ];
    const engines = engineMapFromHealth(categories);
    expect(engines.get("a")).toBe("urlwatch");
    expect(engines.get("b")).toBe("static_html");
    expect(engines.size).toBe(2);
    expect(engineMapFromHealth([]).size).toBe(0);
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

describe("FeedScreen · v8 三级首屏(AC29,v7 双栏首屏用例迁移)", () => {
  /** v8 夹具:2 条 TG(同渠道)+ 1 条网页新闻;store.items mock 按
   *  source 精确过滤(选中作用域同门;source_kind/category 随 IA 退场,
   *  不再传)。 */
  function mockStoreV12() {
    const items = [
      fixtureItem({
        source: "telegram-mihomo_party_group",
        title: "🎉 Clash Party Dev Build 开发版本发布",
        content: "基于版本: 1.9.5",
      }),
      fixtureItem({ source: "telegram-mihomo_party_group", title: "🎉 Clash Party 1.9.4" }),
      fixtureItem({ source: "openai-news", title: "新闻标题丙", category: "tech" }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(
          items.filter((item) => {
            if (params?.source && item.source !== params.source) return false;
            return true;
          }),
        ),
      ),
    );
  }

  it("1 级首屏 = 类型卡瀑布流(v8 AC29):类型卡直出(TG/网站),零渠道行零 chips 零消息卡;旧 IA 面全退场", async () => {
    mockStoreV12();
    await renderOverview();
    // 类型卡墙 + 两类型卡(engine/前缀判定;daily 零成员不出卡)
    expect(screen.getByTestId("feed-types-wall")).toBeTruthy();
    const tgCard = await screen.findByTestId("feed-type-card-tg");
    expect(tgCard.getAttribute("data-channels")).toBe("1");
    expect(tgCard.textContent).toContain("mihomo_party_group"); // 预览带渠道名(词表)
    expect(screen.getByTestId("feed-type-card-site").getAttribute("data-channels")).toBe("1");
    // 旧 IA 面(双栏右栏/瀑布流/chips/导航行/源大类卡/面包屑)随三级化撤销
    expect(screen.queryByTestId("feed-channel-list")).toBeNull();
    expect(screen.queryByTestId("feed-channel-wall")).toBeNull();
    expect(screen.queryByTestId("feed-waterfall")).toBeNull();
    expect(screen.queryByTestId("feed-chips")).toBeNull();
    expect(screen.queryByTestId("feed-kind-wall")).toBeNull();
    expect(screen.queryByTestId("feed-drill-all")).toBeNull();
    expect(screen.queryByTestId("feed-tg-channels")).toBeNull();
    expect(screen.queryByTestId("feed-breadcrumb")).toBeNull();
    expect(screen.queryByTestId("feed-overview")).toBeNull(); // v7 引导空态退役
  });

  it("TG 渠道行 = 聊天视图(气泡时间线 + 日期胶囊);返回钮回 2 级渠道行", async () => {
    mockStoreV12();
    await renderOverview();
    await openChannelList("tg");
    // 点 TG 行 → 3 级聊天视图:气泡时间线 + 居中日期胶囊;网页条目不混
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-mihomo_party_group"));
    expect(await screen.findByTestId("feed-tg-bubble-1")).toBeTruthy();
    expect(screen.getByTestId("feed-tg-bubble-2")).toBeTruthy();
    expect(screen.queryByTestId("feed-item-3")).toBeNull();
    expect(screen.getByTestId("feed-group-今天").className).toContain("rounded-full");
    // 返回钮回 2 级(气泡卡退场,渠道行回归;openai-news 属 site 类型不在此级)
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    expect(await screen.findByTestId("feed-channel-row-telegram-mihomo_party_group")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-bubble-1")).toBeNull();
  });

  it("低版本 sidecar(protocol 11)回退语义:同构三级,请求零 source_kind 零 with_total 零 source_stats", async () => {
    mockStoreV12();
    versionMock.mockResolvedValue(versionResult(11));
    await renderOverview();
    await openChannelList("tg");
    expect(await screen.findByTestId("feed-channel-row-telegram-mihomo_party_group")).toBeTruthy();
    // 回退 = 查询面不携新参数(source_kind/with_total 全零),UI 不报错不缺行;
    // stats 门未过 → store.source_stats 零调用(不发 RPC 试错)
    expect(
      storeItemsMock.mock.calls.every((call) => {
        const params = call[0] as StoreItemsParams | undefined;
        return params?.source_kind === undefined && params?.with_total === undefined;
      }),
    ).toBe(true);
    expect(sourceStatsMock).not.toHaveBeenCalled();
  });

  it("短消息渠道行预览回退(深检 F6):TG 常态 title==content≤100 字,digest 去重为 null 时回退渲染标题,预览行不消失", async () => {
    const text = "Clash Party 1.9.5 发布,修复若干问题并优化内核。"; // <100 字,入库形态 title=content=text
    storeItemsMock.mockResolvedValue(
      result([fixtureItem({ source: "telegram-durov", title: text, content: text })]),
    );
    await renderOverview();
    await openChannelList("tg");
    const row = await screen.findByTestId("feed-channel-row-telegram-durov");
    expect(row.textContent).toContain(text); // 预览行 = 标题回退,不因同文形态消失
    expect(row.textContent).toContain("durov");
  });
});

describe("FeedScreen · 渠道行零条目也出行(v8 AC30,v6 AC20 迁移)", () => {
  it("health 源无条目 = 出行给知会词(零条目渠道不消失);未读徽标不渲染", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "live", sources: [sourceEntry("live-source", "static_html")] }),
          categoryEntry({ id: "idle", sources: [sourceEntry("idle-source", "static_html")] }),
        ],
      }),
    );
    storeItemsMock.mockResolvedValue(result([fixtureItem({ source: "live-source" })]));
    await renderOverview();
    await openChannelList("site");
    expect(await screen.findByTestId("feed-channel-row-live-source")).toBeTruthy();
    const idle = screen.getByTestId("feed-channel-row-idle-source");
    expect(idle.textContent).toContain("今日暂无新条目");
    expect(idle.getAttribute("data-unread")).toBe("false");
    expect(screen.queryByTestId("feed-channel-unread-idle-source")).toBeNull();
  });
});

describe("FeedScreen · tg-category-entry 监控台(v7:TG 选中左栏顶部常驻条,AC25/AC26)", () => {
  const statusPayload = (loggedIn: boolean) => ({
    bot: { configured: false, error: null },
    session: { exists: false },
    web: {
      accounts: [
        { account: "telegram-alt1", logged_in: loggedIn, logged_in_at: loggedIn ? "2026-10-09T01:00:00" : null, login_in_progress: false, login_note: null },
      ],
    },
  });

  /** v7 监控台世界:health 给 TG 渠道(tg_web 引擎,零条目也出行)+
   *  tech 网页渠道;点 TG 行 = 选中 TG 渠道(监控台条落点)。 */
  function mockConsoleWorld(items: FeedItem[]) {
    // 过服务端读态门:seed 的 read:true 才进状态派生(未过门通路只认
    // localStorage,条目字段不参与过滤 —— fixture 注记同门)
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "telegram", name: "Telegram 监控", sources: [sourceEntry("telegram-seed", "tg_web")] }),
          categoryEntry({ id: "tech", name: "科技", sources: [sourceEntry("tech-source", "static_html")] }),
        ],
      }),
    );
    const seeded = [
      fixtureItem({
        source: "tech-source",
        title: "科技今日一条",
      }),
      ...items,
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(seeded.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  async function openTelegramChannel() {
    // v8 三级导航:1 级 TG 类型卡 → 2 级渠道行 → 3 级详情(监控台落点)
    fireEvent.click(await screen.findByTestId("feed-type-card-tg"));
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
  }

  it("TG 渠道选中 → 监控台常驻条(工具条下不随滚):未登录给扫码入口(浏览器单入口),已登录显监控中;网站渠道无此条", async () => {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") return statusPayload(false);
      if (args?.method === "browser.open") return { started: true, op_id: "op-1", kind: "tg_web_login" };
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    mockConsoleWorld([]);
    renderScreen();
    await openTelegramChannel();
    // 监控台条:未登录 → 扫码入口
    const consoleCard = await screen.findByTestId("feed-tg-console");
    expect(within(consoleCard).queryByTestId("feed-tg-console-login")).toBeTruthy();
    // 原生网页预览(v9):该渠道条目缺 t.me 链 → 置灰 + 新置灰词面
    // (/k/ 与 t.me/s 镜像同源推导,频道名推导不出 = 两者同不可得,v9 §1.1)
    const previewBtn = within(consoleCard).getByTestId("feed-tg-console-preview");
    expect(previewBtn.getAttribute("disabled")).not.toBeNull();
    expect(previewBtn.getAttribute("title")).toContain("暂无 t.me 公开链接");
    expect(previewBtn.getAttribute("title")).toContain("原生预览与公开镜像均不可用");
    // 「原生视图」段同门置灰(同一推导);段控件本体在场(isTgChannel 渠道)
    const viewToggle = screen.getByTestId("feed-tg-view-toggle");
    expect(within(viewToggle).getByTestId("feed-tg-view-native").getAttribute("disabled")).not.toBeNull();
    expect(within(viewToggle).getByTestId("feed-tg-view-native").getAttribute("title")).toContain("均不可用");
    fireEvent.click(within(consoleCard).getByTestId("feed-tg-console-login"));
    await waitFor(() =>
      expect(invokeMock).toHaveBeenCalledWith(
        "sidecar_request",
        expect.objectContaining({ method: "browser.open" }),
      ),
    );
    // 空态如实分叉(深检 F2):未登录不说「在线」,指路上方监控台扫码
    expect(await screen.findByText("未登录,暂无新消息入库")).toBeTruthy();
    expect(screen.queryByText(/监控在线/)).toBeNull();

    // 已登录口径:重挂载换应答,显「监控中」且无登录钮
    cleanup();
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") return statusPayload(true);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    renderScreen();
    await openTelegramChannel();
    expect((await screen.findByTestId("feed-tg-console-live")).textContent).toContain("监控中 · telegram-alt1");
    expect(screen.queryByTestId("feed-tg-console-login")).toBeNull();

    // 切网站(tech)渠道:回 2 级 → site 卡 → 点行,监控台条卸载(非 TG 渠道)
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-back-to-types"));
    await openChannelList("site");
    fireEvent.click(await screen.findByTestId("feed-channel-row-tech-source"));
    await screen.findByText("科技今日一条");
    expect(screen.queryByTestId("feed-tg-console")).toBeNull();
    // v9:网站渠道整组不渲染切换段(与监控台条同门 isTgChannel,如实无钮)
    expect(screen.queryByTestId("feed-tg-view-toggle")).toBeNull();
  });

  it("R2 吸收:状态 RPC 首拉在途 = 监控台条与「状态未知」卡都不出(不闪现);应答落地才落条", async () => {
    let resolveStatus: ((value: unknown) => void) | undefined;
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") {
        return new Promise((resolve) => {
          resolveStatus = resolve;
        });
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    mockConsoleWorld([]);
    renderScreen();
    await openTelegramChannel();
    // 在途窗:两卡都不在(v6 双态门下此处闪「状态未知」一拍,R2 根除)
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "telegram-seed" })),
    );
    expect(screen.queryByTestId("feed-tg-console")).toBeNull();
    expect(screen.queryByTestId("feed-tg-status-unknown")).toBeNull();
    expect(screen.queryByText("监控状态未知")).toBeNull();
    // 应答落地:监控台条落位(已登录口径)
    act(() => resolveStatus?.(statusPayload(true)));
    expect(await screen.findByTestId("feed-tg-console-live")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-status-unknown")).toBeNull();
  });

  it("进会话即已读(10-12-tg-session-read):TG 会话选中 → mark_all 带 source 全量已读 + 未读档顺手切「全部」(刚点进来的消息不消失)", async () => {
    invokeMock.mockImplementation(async (command: string, args?: { method?: string }) => {
      if (command === "tg_native_open") return null;
      if (args?.method === "telegram.status") return statusPayload(true);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${command}/${args?.method}` });
    });
    markAllMock.mockResolvedValue({ updated: 3 });
    mockConsoleWorld([
      fixtureItem({
        source: "telegram-seed",
        title: "点进来的未读一条",
        url: "https://t.me/mihomo_party/1202",
        first_seen: new Date(dayWindowStart().getTime() + 5 * 60_000).toISOString(),
      }),
    ]);
    renderScreen();
    await openTelegramChannel();
    // 源级全量已读(角标口径 = source_stats 全库未读,keys 级不清零)
    await waitFor(() =>
      expect(markAllMock).toHaveBeenCalledWith({ marker: "read", value: true, source: "telegram-seed" }),
    );
    // 未读档被切「全部」:刚读的消息留在时间线(TG 聊天语义)
    await waitFor(() => expect(screen.getByText("点进来的未读一条")).toBeTruthy());
  });

  it("监控台历史入口(深检 F1 后语义 = 已读未读全显):已读条目在未读档外可达,知会词换「全部历史」;退出回读态视图", async () => {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") return statusPayload(true);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    const oldReadItem = fixtureItem({
      source: "telegram-seed",
      title: "三天前的已读入库",
      read: true,
    });
    mockConsoleWorld([oldReadItem]);
    renderScreen();
    await openTelegramChannel();
    // 进会话即已读(10-12-tg-session-read):入口自动全量标已读 + 未读档
    // 顺手切「全部」(刚读的留在眼前)——历史语义的验收改为显式回未读档:
    // 唯一条目已读 → 空态;监控台「看全部历史消息(含已读)」直达
    fireEvent.click(await screen.findByRole("button", { name: "过滤:未读" }));
    // 监控台「看全部历史消息(含已读)」直达(已读条目在未读档外可达)
    fireEvent.click(await screen.findByTestId("feed-tg-console-history"));
    expect(await screen.findByText("三天前的已读入库")).toBeTruthy();
    expect(screen.getByTestId("feed-day-window").textContent).toContain("全部历史");
    // 退出历史:回读态视图,已读条目重新离场
    fireEvent.click(screen.getByTestId("feed-history-exit"));
    await waitFor(() => expect(screen.queryByText("三天前的已读入库")).toBeNull());
    // 回读态后显式切「全部」:已读条目回来(档位语义自洽,不依赖默认档)
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    await waitFor(() => expect(screen.getByText("三天前的已读入库")).toBeTruthy());
  });

  it("监控台「管理」钮(v10):点击 → 真实路由落 /tg-account(管理入口随独立屏迁,回归锚)", async () => {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") return statusPayload(true);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    mockConsoleWorld([]);
    // 探针与屏同挂(裸 MemoryRouter 无 Routes,FeedScreen 不因换路由卸载)
    render(
      <MemoryRouter>
        <LocationProbe />
        <FeedScreen />
      </MemoryRouter>,
    );
    await openTelegramChannel();
    const consoleCard = await screen.findByTestId("feed-tg-console");
    fireEvent.click(within(consoleCard).getByRole("button", { name: "管理" }));
    await waitFor(() =>
      expect(screen.getByTestId("location-probe").textContent).toBe("/tg-account"),
    );
  });

  it("telegram.status 拉取失败(深检 F8①/F2):监控台缺席,空态不称「在线」给重试拉状态", async () => {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") {
        throw JSON.stringify({ code: "internal_error", path: "$", message: "状态服务未就绪" });
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    mockConsoleWorld([]);
    renderScreen();
    await openTelegramChannel();
    // 监控台整体缺席(失败不进状态条,v2 同门)
    expect(screen.queryByTestId("feed-tg-console")).toBeNull();
    // 空态如实「状态未知」+ 重试,不再无条件称「监控在线」、不指路缺席的监控台
    const unknown = await screen.findByTestId("feed-tg-status-unknown");
    expect(unknown.textContent).toContain("监控状态未知");
    expect(unknown.textContent).not.toContain("监控台");
    expect(screen.queryByText(/监控在线/)).toBeNull();
    // 重试钮真实重拉 telegram.status
    const statusCalls = () => invokeMock.mock.calls.filter(([, args]) => (args as { method?: string })?.method === "telegram.status").length;
    const before = statusCalls();
    fireEvent.click(screen.getByRole("button", { name: "重试拉取状态" }));
    await waitFor(() => expect(statusCalls()).toBeGreaterThan(before));
  });

  it("原生网页预览(v9 AC11 升级):最新条目 url 推导 /k/ 深链 → 注册表应用内开窗(label tg-native-*,title/尺寸定稿);窗口仅展示,入库归后台 watcher;首开注记如实披露扫码+安全提醒", async () => {
    invokeMock.mockImplementation(async (command: string, args?: { method?: string }) => {
      // 返回钮批(10-12):建窗走 Rust 命令(invoke 通道;getByLabel 缺省
      // miss → create 桩句柄,事件监听降级不碍本用例断言面)
      if (command === "tg_native_open") return null;
      if (args?.method === "telegram.status") return statusPayload(true);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${command}/${args?.method}` });
    });
    // url 带消息锚可推导(渠道内最新一条)
    mockConsoleWorld([
      fixtureItem({
        source: "telegram-seed",
        title: "频道最新一条",
        url: "https://t.me/mihomo_party/1201",
        first_seen: new Date(dayWindowStart().getTime() + 3 * 60_000).toISOString(),
      }),
    ]);
    WebviewWindowMock.mockClear();
    // vitest 4:vi.fn(箭头实现)不可 new(注册表 realDeps.create 走真实构造,
    // 不再吃旧 AC11「调用已记、构造异常被 try/catch 吞进注记」的巧合绿灯)
    WebviewWindowMock.mockImplementation(function () {
      return { once: vi.fn(async () => () => undefined) };
    });
    renderScreen();
    await openTelegramChannel();
    const consoleCard = await screen.findByTestId("feed-tg-console");
    const previewBtn = within(consoleCard).getByTestId("feed-tg-console-preview");
    expect(previewBtn.getAttribute("disabled")).toBeNull();
    // 词面升级(v9):钮面含「原生」,title 如实告知 QR 登录一次 + 安全提醒属预期
    expect(previewBtn.textContent).toContain("原生");
    expect(previewBtn.getAttribute("title")).toContain("首次需扫码登录一次");
    expect(previewBtn.getAttribute("title")).toContain("安全提醒");
    expect(previewBtn.getAttribute("title")).toContain("https://web.telegram.org/k/#@mihomo_party");
    fireEvent.click(previewBtn);
    // 开窗断言(返回钮批 10-12 后:断言 Rust 命令载荷):稳定 label =
    // tg-native-<t.me 频道名>(深检 F4 键口径:与源名解耦,两源同频道聚焦
    // 复用同窗)+ /k/ 深链 + design-v9 §2.2 方案 A 定稿尺寸(最小尺寸由
    // Rust 命令侧钳制,载荷不带)
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    expect(nativeOpenCalls()[0]?.[1]).toEqual(
      expect.objectContaining({
        label: "tg-native-mihomo_party",
        url: "https://web.telegram.org/k/#@mihomo_party",
        title: "TG · seed",
        width: 1100,
        height: 780,
      }),
    );
    // 首开注记(design-v9 §1.3 双会话披露):扫码一次 + 触发安全提醒属预期
    const note = await screen.findByTestId("feed-tg-console-preview-note");
    expect(note.textContent).toContain("扫码登录一次");
    expect(note.textContent).toContain("安全提醒");
    expect(note.textContent).toContain("免扫");
    // 段控件随开窗落「原生视图」active + 红点徽标(窗口存活)
    await waitFor(() =>
      expect(screen.getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("true"),
    );
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeTruthy();
  });
});

// ---------------------------------------------------------------------------
// tg-chat-two-pane(10-11,主人令「左侧是群列表,点击后,展示出来右侧的群
// 内容」+「UI 布局要按照 tg 的群对话方式进行布局」):3 级 TG 情报视图 =
// TG 群对话式双栏(左监控群列表 + 右聊天时间线)。落点判例:v7 双栏错粒度
// 在 2 级,本次 3 级是主人明令,不属翻案。
// ---------------------------------------------------------------------------

describe("FeedScreen · tg-chat-two-pane(3 级 TG 群对话式双栏,10-11)", () => {
  const statusPayload = (loggedIn: boolean) => ({
    bot: { configured: false, error: null },
    session: { exists: false },
    web: {
      accounts: [
        { account: "telegram-alt1", logged_in: loggedIn, logged_in_at: loggedIn ? "2026-10-09T01:00:00" : null, login_in_progress: false, login_note: null },
      ],
    },
  });

  /** 双栏世界:health 给 TG 监控群(缺省两群:clashv8 = 主人装机实况主例 +
   *  alpha)与 tech 网页渠道;storeItems 按参数分源过滤(v9 mockNativeWorld
   *  同门)。单群退化 = groups 只传 clashv8(AC4①)。 */
  function mockTwoPaneWorld(items: FeedItem[], groups: string[] = ["telegram-clashv8", "telegram-alpha"]) {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") return statusPayload(true);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({
            id: "telegram",
            name: "Telegram 监控",
            sources: groups.map((name) => sourceEntry(name, "tg_web")),
          }),
          categoryEntry({ id: "tech", name: "科技", sources: [sourceEntry("tech-source", "static_html")] }),
        ],
      }),
    );
    const seeded = [
      fixtureItem({ source: "tech-source", title: "科技今日一条" }),
      ...items,
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(seeded.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  /** 下钻入口:1 级 TG 类型卡 → 2 级行 → 3 级(群列表默认选中该渠道)。 */
  async function openTgGroup(key: string) {
    fireEvent.click(await screen.findByTestId("feed-type-card-tg"));
    fireEvent.click(await screen.findByTestId(`feed-channel-row-${key}`));
  }

  it("AC1/AC4① 左栏渲染群行:单群(clashv8 实况)退化照常渲染单行并默认选中;行 = 渠道名/最近预览/相对时间/未读徽标", async () => {
    const anchor = dayWindowStart().getTime();
    mockTwoPaneWorld(
      [
        fixtureItem({
          source: "telegram-clashv8",
          title: "clashv8 群消息",
          first_seen: new Date(anchor + 60_000).toISOString(),
        }),
      ],
      ["telegram-clashv8"], // 单群退化态
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");

    // 左栏在场;单群单行照常渲染,默认选中 = 当前深链渠道(AC1)
    // (裁⑥:用户可见词 = 监控会话,testid 前缀 feed-tg-group-* 结构词不动)
    const pane = await screen.findByTestId("feed-tg-group-pane");
    expect(pane.getAttribute("aria-label")).toBe("监控会话列表");
    const row = screen.getByTestId("feed-channel-row-telegram-clashv8");
    expect(row.getAttribute("data-selected")).toBe("true");
    expect(row.getAttribute("data-channel-kind")).toBe("tg");
    // TG 聊天列表行四件套:渠道名 / 最近消息预览 / 相对时间 / 未读徽标
    expect(row.textContent).toContain("clashv8");
    expect(row.textContent).toContain("净化摘要内容");
    expect(row.querySelector("time")).not.toBeNull();
    expect(within(row).getByTestId("feed-channel-unread-telegram-clashv8").textContent).toBe("1");
  });

  it("AC2 点击左栏另一群 → viewSource 切换 + 流式重载(mock 断言),不退出 3 级、不经过 2 级;选中态迁移", async () => {
    const anchor = dayWindowStart().getTime();
    mockTwoPaneWorld([
      fixtureItem({
        source: "telegram-clashv8",
        title: "clashv8 群消息",
        first_seen: new Date(anchor + 60_000).toISOString(),
      }),
      fixtureItem({
        source: "telegram-alpha",
        title: "alpha 群消息",
        first_seen: new Date(anchor + 30_000).toISOString(),
      }),
    ]);
    renderScreen();
    await openTgGroup("telegram-clashv8");
    expect(await screen.findByText("clashv8 群消息")).toBeTruthy();
    expect(screen.getByTestId("feed-channel-row-telegram-alpha").getAttribute("data-selected")).toBe("false");

    // 点左栏另一群:store.items 带 source 精确等值重发(既有流式机制复用)
    fireEvent.click(screen.getByTestId("feed-channel-row-telegram-alpha"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "telegram-alpha" })),
    );
    // 不退出 3 级、不经过 2 级:类型卡墙与 2 级行列表都不在场
    expect(screen.queryByTestId("feed-types-wall")).toBeNull();
    expect(screen.queryByTestId("feed-channel-list")).toBeNull();
    // 右栏换成 alpha 时间线,旧群条目离场;左栏选中态迁移
    expect(await screen.findByText("alpha 群消息")).toBeTruthy();
    expect(screen.queryByText("clashv8 群消息")).toBeNull();
    expect(screen.getByTestId("feed-channel-row-telegram-alpha").getAttribute("data-selected")).toBe("true");
    expect(screen.getByTestId("feed-channel-row-telegram-clashv8").getAttribute("data-selected")).toBe("false");
  });

  it("AC3 聊天头:群名大字 + 监控状态行(监控中·账号·自时间)+ 三动作钮;工具条与时间线保留", async () => {
    const anchor = dayWindowStart().getTime();
    mockTwoPaneWorld(
      [
        fixtureItem({
          source: "telegram-clashv8",
          title: "clashv8 群消息",
          url: "https://t.me/clashv8/101",
          first_seen: new Date(anchor + 60_000).toISOString(),
        }),
      ],
      ["telegram-clashv8"],
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");

    // 聊天头:群名(feed-stream-title 随迁,大字段)
    const header = await screen.findByTestId("feed-tg-chat-header");
    expect(within(header).getByTestId("feed-stream-title").textContent).toContain("clashv8");
    // 监控状态行:监控中 · 账号 · 自时间(原监控台状态行词面,来自 console 状态数据)
    const live = within(header).getByTestId("feed-tg-console-live");
    expect(live.textContent).toContain("监控中 · telegram-alt1");
    expect(live.textContent).toContain("自 2026-10-09 01:00");
    // 三动作钮:原生网页预览 / 管理 / 看全部历史消息(监控台大卡压缩条内)
    expect(within(header).getByTestId("feed-tg-console-preview").getAttribute("disabled")).toBeNull();
    expect(within(header).getByRole("button", { name: "管理" })).toBeTruthy();
    expect(within(header).getByTestId("feed-tg-console-history")).toBeTruthy();
    // 工具条保留可用:读态分段 / 渠道内检索 / 显示选项 / 刷新(AC3 后半)
    const toolbar = screen.getByTestId("feed-toolbar");
    expect(within(toolbar).getByRole("group", { name: "读态过滤" })).toBeTruthy();
    expect(within(toolbar).getByLabelText("渠道内检索")).toBeTruthy();
    expect(within(toolbar).getByRole("button", { name: "显示选项" })).toBeTruthy();
    expect(within(toolbar).getByRole("button", { name: "刷新" })).toBeTruthy();
    // 聊天时间线照常渲染
    expect(await screen.findByTestId("feed-chat-timeline")).toBeTruthy();
  });

  it("AC4② 零监控群引导空态(防御位):引导到 Telegram 屏添加监控群", async () => {
    // 可达路径构造:health 失败(engine 词表缺席,渠道全集退化为已加载条目
    // source)+ version 挂起 → 下钻完成后放行 COUNT_PROTOCOL 门 → countReady
    // 翻转触发 refreshCatalog 整页替换;此刻 catalog 域改答零条目 = 渠道全集
    // 真清空(health 源在场则行恒在,无法达零),左栏落零群空态。正常动线
    // 3 级 TG 必有 ≥1 群(入口来自该列表),此态为防御位 + 语义自文档。
    let resolveVersion: ((value: VersionResult) => void) | undefined;
    versionMock.mockImplementation(
      () => new Promise<VersionResult>((resolve) => { resolveVersion = resolve; }),
    );
    mockTwoPaneWorld(
      [fixtureItem({ source: "telegram-clashv8", title: "clashv8 群消息" })],
      ["telegram-clashv8"],
    );
    healthMock.mockRejectedValue(new Error("sidecar 未连接"));
    renderScreen();
    await openTgGroup("telegram-clashv8");
    expect(await screen.findByTestId("feed-channel-row-telegram-clashv8")).toBeTruthy();

    // 门翻转后的 catalog 重拉改答零条目(stream 域照常供流)
    const streamItem = fixtureItem({ source: "telegram-clashv8", title: "clashv8 群消息" });
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(params?.source ? [streamItem] : [])),
    );
    await act(async () => {
      resolveVersion?.(versionResult(COUNT_PROTOCOL));
    });
    const empty = await screen.findByTestId("feed-tg-group-empty");
    expect(empty.textContent).toContain("还没有监控会话");
    expect(empty.textContent).toContain("Telegram");
    expect(empty.textContent).toContain("添加监控会话");
  });
});

// ---------------------------------------------------------------------------
// tg-multi-account-groups v5 追批(10-11,主人令「TG 二级界面要展示账号列表,
// 再展示群列表」,AC36-49):2 级 Telegram 页渠道列表区之上加账号区 ——
// 数据 = telegram.status web.accounts(v4 身份面同源,3 级监控台共此一拉)。
// ---------------------------------------------------------------------------

describe("FeedScreen · tg-multi-account-groups v5(2 级 Telegram 账号区)", () => {
  /** status 应答:三账号 —— 甲已登录(带备注名/user_id/自时间);乙未登录
   *  (无备注/user_id,主显示回退键名、user_id 位给 —);丙登录中
   *  (login_in_progress,补B 第三档)。 */
  const twoAccountPayload = {
    bot: { configured: false, error: null },
    session: { exists: false },
    web: {
      accounts: [
        { account: "tg-alt1", logged_in: true, logged_in_at: "2026-10-09T01:00:00", label: "主力号", user_id: "10086", login_in_progress: false, login_note: null },
        { account: "tg-alt2", logged_in: false, logged_in_at: null, label: null, user_id: null, login_in_progress: false, login_note: null },
        { account: "tg-alt3", logged_in: false, logged_in_at: null, label: null, user_id: null, login_in_progress: true, login_note: null },
      ],
    },
  };
  const zeroAccountPayload = {
    bot: { configured: false, error: null },
    session: { exists: false },
    web: { accounts: [] },
  };

  /** 账号区世界:health 给 TG 源与 tech 网页源,条目两源各一(2 级用例,
   *  不下钻 3 级)。 */
  function mockAccountsWorld() {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "telegram", name: "Telegram 监控", sources: [sourceEntry("telegram-seed", "tg_web")] }),
          categoryEntry({ id: "tech", name: "科技", sources: [sourceEntry("tech-source", "static_html")] }),
        ],
      }),
    );
    const seeded = [
      fixtureItem({ source: "tech-source", title: "科技今日一条" }),
      fixtureItem({ source: "telegram-seed", title: "seed 群消息" }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(seeded.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  function mockStatus(payload: unknown) {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") return payload;
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
  }

  const statusCalls = () =>
    invokeMock.mock.calls.filter(([, args]) => (args as { method?: string })?.method === "telegram.status").length;

  it("v5 账号区渲染:区头「账号 · N」贴群列表区头词面;行 = 备注名主显示/键名·user_id 小字/登录态三档●○/行身可激活/管理钮;群列表照旧;网站 2 级零变化", async () => {
    mockAccountsWorld();
    mockStatus(twoAccountPayload);
    await renderOverview();
    await openChannelList("tg");

    // 区头:账号 · 3(词面风格 = 群列表区头「TG · N 个渠道」同款)
    await screen.findByTestId("feed-tg-accounts");
    expect(screen.getByTestId("feed-tg-accounts-title").textContent).toBe("账号 · 3");
    // 行甲:备注名「主力号」主显示 + 内部键名·user_id 小字 + 已登录 ●(ok 档)
    const rowA = await screen.findByTestId("feed-tg-account-row-tg-alt1");
    expect(within(rowA).getByText("主力号")).toBeTruthy();
    expect(rowA.textContent).toContain("tg-alt1 · 10086");
    const dotA = within(rowA).getByText("●");
    expect(dotA.className).toContain("text-ok");
    expect(within(rowA).getByRole("button", { name: "管理 主力号" })).toBeTruthy();
    // 行乙:无备注回退键名主显示,user_id 缺席给 —,未登录 ○
    const rowB = screen.getByTestId("feed-tg-account-row-tg-alt2");
    expect(within(rowB).getByText("tg-alt2")).toBeTruthy();
    expect(rowB.textContent).toContain("tg-alt2 · —");
    expect(within(rowB).getByText("○")).toBeTruthy();
    expect(within(rowB).getByRole("button", { name: "管理 tg-alt2" })).toBeTruthy();
    // 行丙(补B 第三档):登录中 —— 点色 warning + sr-only 态词,字形仍 ○
    const rowC = screen.getByTestId("feed-tg-account-row-tg-alt3");
    const dotC = within(rowC).getByText("○");
    expect(dotC.className).toContain("text-warning");
    expect(within(rowC).getByText("登录中", { selector: ".sr-only" })).toBeTruthy();
    // 补C:行身可激活(role=button + tabIndex,行身点击/键盘 = 管理跳转同义)
    expect(rowC.getAttribute("role")).toBe("button");
    expect(rowC.getAttribute("tabindex")).toBe("0");
    expect(within(rowC).getByText("登录中", { selector: ".sr-only" }).className).toContain("sr-only");
    // 群列表区照旧零变化:搜索框/渠道行/未读徽标原样在场
    expect(screen.getByLabelText("搜索渠道")).toBeTruthy();
    expect(screen.getByTestId("feed-channel-row-telegram-seed")).toBeTruthy();
    // 网站 2 级零变化:账号区仅 telegram 类型页(site 页整区不出)
    fireEvent.click(screen.getByTestId("feed-back-to-types"));
    await openChannelList("site");
    expect(screen.queryByTestId("feed-tg-accounts")).toBeNull();
  });

  it("v5 账号区加载与空态:status 在途 = 骨架行(区头无计数),空态不出;零账号应答落地 = 引导空态 + 跳转钮", async () => {
    mockAccountsWorld();
    let resolveStatus: ((value: unknown) => void) | undefined;
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") {
        return new Promise((resolve) => {
          resolveStatus = resolve;
        });
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    await renderOverview();
    await openChannelList("tg");
    // 在途:骨架在场,空态与计数词面都不出(不把加载中误述成没有)
    expect(await screen.findByTestId("feed-tg-accounts-loading")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-accounts-empty")).toBeNull();
    expect(screen.queryByTestId("feed-tg-accounts-list")).toBeNull();
    expect(screen.getByTestId("feed-tg-accounts-title").textContent).toBe("账号");
    // 应答 = 零账号:引导空态(指路 Telegram 屏)+ 跳转钮 + 区头落计数
    await act(async () => {
      resolveStatus?.(zeroAccountPayload);
    });
    const empty = await screen.findByTestId("feed-tg-accounts-empty");
    expect(empty.textContent).toContain("Telegram");
    expect(within(empty).getByTestId("feed-tg-accounts-goto")).toBeTruthy();
    expect(screen.getByTestId("feed-tg-accounts-title").textContent).toBe("账号 · 0");
  });

  it("v5 账号区管理跳转:行尾「管理」钮真实路由落 /tg-account(消费方只读跳转,管理面不搬)", async () => {
    mockAccountsWorld();
    mockStatus(twoAccountPayload);
    // 探针与屏同挂(裸 MemoryRouter 无 Routes;监控台「管理」钮用例同门)
    render(
      <MemoryRouter>
        <LocationProbe />
        <FeedScreen />
      </MemoryRouter>,
    );
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-tg-account-manage-tg-alt1"));
    await waitFor(() =>
      expect(screen.getByTestId("location-probe").textContent).toBe("/tg-account"),
    );
  });

  it("v5 账号区 error 态:「监控状态暂时不可用」+ 重试真实重发 + 跳转钮并列(补A:2 级不再是唯一 error 无重试的 TG 面)", async () => {
    mockAccountsWorld();
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") {
        throw JSON.stringify({ code: "internal_error", path: "$", message: "状态服务未就绪" });
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    await renderOverview();
    await openChannelList("tg");
    // error 独立分支:词面 + 重试 + 跳转并列;ok-空态分支不出(词面不吞 error)
    const err = await screen.findByTestId("feed-tg-accounts-error");
    expect(err.textContent).toContain("监控状态暂时不可用");
    expect(within(err).getByTestId("feed-tg-accounts-retry")).toBeTruthy();
    expect(within(err).getByTestId("feed-tg-accounts-goto")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-accounts-empty")).toBeNull();
    // 重试真实重发 telegram.status
    const before = statusCalls();
    fireEvent.click(within(err).getByTestId("feed-tg-accounts-retry"));
    await waitFor(() => expect(statusCalls()).toBeGreaterThan(before));
  });

  it("v5 账号区取数纪律:site 2 级 telegram.status 零调用;TG 2→3→2 跨级往返仅 1 发(同源共拉不另起)", async () => {
    mockAccountsWorld();
    mockStatus(twoAccountPayload);
    await renderOverview();
    // site 2 级:账号区不在场,status 零调用
    await openChannelList("site");
    expect(statusCalls()).toBe(0);
    // TG 2 级:首拉恰 1 发
    fireEvent.click(screen.getByTestId("feed-back-to-types"));
    await openChannelList("tg");
    await screen.findByTestId("feed-tg-accounts");
    await waitFor(() => expect(statusCalls()).toBe(1));
    // 2→3→2 跨级往返:tgStatusNeeded 恒真,deps 不翻转不重发
    fireEvent.click(screen.getByTestId("feed-channel-row-telegram-seed"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "telegram-seed" })),
    );
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
    expect(statusCalls()).toBe(1);
  });
});

// ---------------------------------------------------------------------------
// tg-chat-two-pane 补批(grill 一轮 + 裁②/裁⑥):Enter 错位修复 / 历史出口
// 就近 / 状态空窗头部化 / 切群滚动定位。
// ---------------------------------------------------------------------------

describe("FeedScreen · tg-chat-two-pane 补批(grill 一轮)", () => {
  const statusPayload = (loggedIn: boolean) => ({
    bot: { configured: false, error: null },
    session: { exists: false },
    web: {
      accounts: [
        { account: "telegram-alt1", logged_in: loggedIn, logged_in_at: loggedIn ? "2026-10-09T01:00:00" : null, login_in_progress: false, login_note: null },
      ],
    },
  });

  /** 补批世界:双群(缺省 clashv8 + alpha)或单群;status 行为可注(缺省已
   *  登录应答;"pending"/"fail" 供补④)。 */
  function mockGrillWorld(
    items: FeedItem[],
    groups: string[] = ["telegram-clashv8", "telegram-alpha"],
    statusImpl?: () => Promise<unknown>,
  ) {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") {
        if (statusImpl) return statusImpl();
        return statusPayload(true);
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({
            id: "telegram",
            name: "Telegram 监控",
            sources: groups.map((name) => sourceEntry(name, "tg_web")),
          }),
          categoryEntry({ id: "tech", name: "科技", sources: [sourceEntry("tech-source", "static_html")] }),
        ],
      }),
    );
    const seeded = [
      fixtureItem({ source: "tech-source", title: "科技今日一条" }),
      ...items,
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(seeded.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  async function openTgGroup(key: string) {
    fireEvent.click(await screen.findByTestId("feed-type-card-tg"));
    fireEvent.click(await screen.findByTestId(`feed-channel-row-${key}`));
  }

  it("补①+裁② 焦点在左栏会话行按 Enter = 切群(不弹条目详情弹窗);j/k 环不进左栏集合", async () => {
    const anchor = dayWindowStart().getTime();
    mockGrillWorld([
      fixtureItem({ source: "telegram-clashv8", title: "clashv8 群消息", first_seen: new Date(anchor + 60_000).toISOString() }),
      fixtureItem({ source: "telegram-alpha", title: "alpha 群消息", first_seen: new Date(anchor + 30_000).toISOString() }),
    ]);
    renderScreen();
    await openTgGroup("telegram-clashv8");
    await screen.findByText("clashv8 群消息");

    // Tab 语义等价 = row.focus()(行根 div[role=button] tabIndex=0,裁②左栏
    // 巡行面);Enter 归行内激活 = openChannel,不落全局条目详情弹窗
    const alphaRow = screen.getByTestId("feed-channel-row-telegram-alpha");
    alphaRow.focus();
    expect(document.activeElement).toBe(alphaRow);
    fireEvent.keyDown(window, { key: "Enter" });
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "telegram-alpha" })),
    );
    expect(screen.queryByTestId("feed-detail-dialog")).toBeNull();
    expect(await screen.findByText("alpha 群消息")).toBeTruthy();

    // 裁②轻断言:j/k 巡游落右栏条目环,左栏行不进集合(navFocused 恒 false)
    fireEvent.keyDown(window, { key: "j" });
    await waitFor(() => expect(alphaRow.getAttribute("data-nav-focused")).toBe("false"));
    expect(screen.queryByTestId("feed-detail-dialog")).toBeNull();
  });

  it("补③ 历史出口就近:非历史态词面照旧;进入历史 = 头部同钮转「退出历史」,点击即退场(知会词回全量)", async () => {
    const anchor = dayWindowStart().getTime();
    mockGrillWorld(
      [fixtureItem({ source: "telegram-clashv8", title: "clashv8 群消息", first_seen: new Date(anchor + 60_000).toISOString() })],
      ["telegram-clashv8"],
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");
    const histBtn = await screen.findByTestId("feed-tg-console-history");
    expect(histBtn.textContent).toContain("看全部历史消息(含已读)");
    // 进入历史(该条目已读 → 未读档外可达,历史态知会词换「全部历史」)
    fireEvent.click(histBtn);
    expect(await screen.findByText("clashv8 群消息")).toBeTruthy();
    expect(screen.getByTestId("feed-day-window").textContent).toContain("全部历史");
    // 出口就近:同一颗按钮词面转「退出历史」,点击即退场
    await waitFor(() => expect(histBtn.textContent).toContain("退出历史"));
    fireEvent.click(histBtn);
    await waitFor(() => expect(histBtn.textContent).toContain("看全部历史消息(含已读)"));
    await waitFor(() =>
      expect(screen.getByTestId("feed-day-window").textContent).toContain("全量"),
    );
  });

  it("补④ 状态空窗头部化(在途):占位词在场不空窗,压缩条不出;放行应答 = 占位词退场压缩条落位", async () => {
    const anchor = dayWindowStart().getTime();
    let resolveStatus: ((value: unknown) => void) | undefined;
    mockGrillWorld(
      [fixtureItem({ source: "telegram-clashv8", title: "clashv8 群消息", first_seen: new Date(anchor + 60_000).toISOString() })],
      ["telegram-clashv8"],
      () => new Promise((resolve) => { resolveStatus = resolve; }),
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");
    // 在途:头部占位词(不引 Skeleton),压缩条与「状态未知」卡都不出
    expect(await screen.findByTestId("feed-tg-console-loading")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-console")).toBeNull();
    expect(screen.queryByTestId("feed-tg-status-unknown")).toBeNull();
    // 放行已登录应答:占位词退场,压缩条落位
    await act(async () => {
      resolveStatus?.(statusPayload(true));
    });
    expect(await screen.findByTestId("feed-tg-console-live")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-console-loading")).toBeNull();
  });

  it("补④ 状态空窗头部化(失败且条目在场):warning 行 + 就近重试真实重拉;零条目兜底卡不出、时间线不断", async () => {
    const anchor = dayWindowStart().getTime();
    const statusCalls = () =>
      invokeMock.mock.calls.filter(([, args]) => (args as { method?: string })?.method === "telegram.status").length;
    mockGrillWorld(
      [fixtureItem({ source: "telegram-clashv8", title: "clashv8 群消息", first_seen: new Date(anchor + 60_000).toISOString() })],
      ["telegram-clashv8"],
      async () => {
        throw JSON.stringify({ code: "internal_error", path: "$", message: "状态服务未就绪" });
      },
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");
    // 失败但条目在场:头部 warning 行 + 重试钮;时间线照常(阅读不断),
    // 零条目兜底卡(feed-tg-status-unknown)不出
    const warn = await screen.findByTestId("feed-tg-console-unavailable");
    expect(warn.textContent).toContain("监控状态暂时不可用");
    expect(await screen.findByText("clashv8 群消息")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-status-unknown")).toBeNull();
    // 就近重试:真实重发 telegram.status
    const before = statusCalls();
    fireEvent.click(within(warn).getByRole("button", { name: "重试" }));
    await waitFor(() => expect(statusCalls()).toBeGreaterThan(before));
  });

  it("补⑤ 切群滚动定位(可选断言):viewSource 变化 → 选中行 scrollIntoView(block:nearest)", async () => {
    const anchor = dayWindowStart().getTime();
    mockGrillWorld([
      fixtureItem({ source: "telegram-clashv8", title: "clashv8 群消息", first_seen: new Date(anchor + 60_000).toISOString() }),
      fixtureItem({ source: "telegram-alpha", title: "alpha 群消息", first_seen: new Date(anchor + 30_000).toISOString() }),
    ]);
    // jsdom 无滚动实现:beforeAll 的 no-op 桩上再 spy 记调用,finally 还原回桩
    const spy = vi.spyOn(Element.prototype, "scrollIntoView").mockImplementation(() => {});
    try {
      renderScreen();
      await openTgGroup("telegram-clashv8");
      await screen.findByText("clashv8 群消息");
      const callsBaseline = spy.mock.calls.length; // 进 3 级首次定位已发生
      fireEvent.click(screen.getByTestId("feed-channel-row-telegram-alpha"));
      await waitFor(() => expect(spy.mock.calls.length).toBeGreaterThan(callsBaseline));
      expect(spy.mock.calls[spy.mock.calls.length - 1][0]).toEqual({ block: "nearest" });
    } finally {
      spy.mockRestore();
    }
  });
});

describe("feed 内置浏览器预览 纯函数(api.ts,10-09-tg-category-entry v3)", () => {
  it("telegramMirrorUrlOf:消息锚/预览链/纯频道链 → t.me/s/<频道名>;邀请链/非 t.me/空 = null 不猜", () => {
    // bot/网页线消息锚(AC11 主例:mihomo_party 最新条目)
    expect(telegramMirrorUrlOf("https://t.me/mihomo_party/1201")).toBe("https://t.me/s/mihomo_party");
    // 已是预览链(带消息 id)→ 剥回频道根
    expect(telegramMirrorUrlOf("https://t.me/s/durov/548")).toBe("https://t.me/s/durov");
    // 纯频道链
    expect(telegramMirrorUrlOf("https://t.me/durov")).toBe("https://t.me/s/durov");
    expect(telegramMirrorUrlOf("https://t.me/durov/")).toBe("https://t.me/s/durov");
    // http + query 照样认
    expect(telegramMirrorUrlOf("http://t.me/s/mihomo_party?single")).toBe("https://t.me/s/mihomo_party");
    // 不猜:私有邀请链 / 非 t.me 域 / 空刻
    expect(telegramMirrorUrlOf("https://t.me/+AbCdEf_123")).toBeNull();
    expect(telegramMirrorUrlOf("https://example.com/item-1")).toBeNull();
    expect(telegramMirrorUrlOf("")).toBeNull();
    expect(telegramMirrorUrlOf(null)).toBeNull();
  });
});

describe("feed 原生视图 纯函数(api.ts,10-09-tg-category-entry v9)", () => {
  it("telegramKUrlOf:三种 t.me 形态 → /k/#@<频道名> 深链(9 断言镜像 telegramMirrorUrlOf 用例表);邀请链/非 t.me/空 = null 不猜", () => {
    // bot/网页线消息锚(v9 主例:mihomo_party 最新条目 → 登录后自动落频道)
    expect(telegramKUrlOf("https://t.me/mihomo_party/1201")).toBe("https://web.telegram.org/k/#@mihomo_party");
    // 已是预览链(带消息 id)→ 剥回频道根
    expect(telegramKUrlOf("https://t.me/s/durov/548")).toBe("https://web.telegram.org/k/#@durov");
    // 纯频道链
    expect(telegramKUrlOf("https://t.me/durov")).toBe("https://web.telegram.org/k/#@durov");
    expect(telegramKUrlOf("https://t.me/durov/")).toBe("https://web.telegram.org/k/#@durov");
    // http + query 照样认(频道名词表 [A-Za-z0-9_],无需编码)
    expect(telegramKUrlOf("http://t.me/s/mihomo_party?single")).toBe("https://web.telegram.org/k/#@mihomo_party");
    // v9 深检补形:watcher 落库条目的内部形态 url(#tg-<chatId>-<msgId>)
    // → /k/#<chatId>(主人在装机实机上点「原生视图」无反应的根因:此前
    // 只认 t.me 形态,真实 TG 条目全部推导 null → 按钮恒 disabled)
    expect(telegramKUrlOf("https://web.telegram.org#tg--2349572233-4294967408")).toBe(
      "https://web.telegram.org/k/#-2349572233",
    );
    expect(telegramKUrlOf("https://web.telegram.org#tg--1001234567890-42")).toBe(
      "https://web.telegram.org/k/#-1001234567890",
    );
    expect(telegramKUrlOf("https://web.telegram.org#tg-12345-7")).toBe(
      "https://web.telegram.org/k/#12345",
    );
    expect(telegramKUrlOf("https://web.telegram.org#tg-bad")).toBeNull();
    expect(telegramKUrlOf("https://web.telegram.org#tg--abc-def")).toBeNull();
    // 不猜(与 t.me/s 镜像同源死分支:/k/ 与镜像都靠 t.me 链提频道名,推导不出两者同不可得)
    expect(telegramKUrlOf("https://t.me/+AbCdEf_123")).toBeNull();
    expect(telegramKUrlOf("https://example.com/item-1")).toBeNull();
    expect(telegramKUrlOf("")).toBeNull();
    expect(telegramKUrlOf(null)).toBeNull();
  });
});

describe("FeedScreen · v9 原生视图切换(design-v9 照稿)", () => {
  const statusPayload = (loggedIn: boolean) => ({
    bot: { configured: false, error: null },
    session: { exists: false },
    web: {
      accounts: [
        { account: "telegram-alt1", logged_in: loggedIn, logged_in_at: loggedIn ? "2026-10-09T01:00:00" : null, login_in_progress: false, login_note: null },
      ],
    },
  });

  /** v9 世界 = 监控台世界同门 + 可推导 t.me 链条目(段控件/预览钮双活) */
  function mockNativeWorld(items: FeedItem[]) {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "telegram", name: "Telegram 监控", sources: [sourceEntry("telegram-seed", "tg_web")] }),
          categoryEntry({ id: "tech", name: "科技", sources: [sourceEntry("tech-source", "static_html")] }),
          categoryEntry({ id: "daily", name: "日报", sources: [sourceEntry("daily-digest", "prompt")] }),
        ],
      }),
    );
    const seeded = [
      fixtureItem({ source: "tech-source", title: "科技今日一条" }),
      fixtureItem({
        source: "telegram-seed",
        title: "频道最新一条",
        url: "https://t.me/mihomo_party/1201",
        first_seen: new Date(dayWindowStart().getTime() + 3 * 60_000).toISOString(),
      }),
      ...items,
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(seeded.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  function mockStatusOnly(loggedIn: boolean) {
    invokeMock.mockImplementation(async (command: string, args?: { method?: string }) => {
      // 返回钮批(10-12):原生窗改走 Rust 命令建窗(invoke 通道)
      if (command === "tg_native_open") return null;
      if (args?.method === "telegram.status") return statusPayload(loggedIn);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${command}/${args?.method}` });
    });
  }


  /** 假窗 once 捕获器:注册表建窗时登记事件回调,测试手动触发生命周期;
   *  同时留存最后建出的句柄(活窗对账要把它喂给 getByLabel,见 destroyed
   *  用例 —— 存活判定实时走系统查询,建窗后 mock 需自洽地「查得到」)。
   *  返回钮批(10-12):建窗走 invoke(tg_native_open) 通道 —— 捕获器在
   *  invoke 应答时铸假窗并即时挂 getByLabel(建窗链 create 的句柄即它),
   *  构造 mock 不再被走。 */
  function captureOnceHandlers() {
    const handlers = new Map<string, (event: unknown) => void>();
    let lastHandle: Record<string, unknown> | null = null;
    invokeMock.mockImplementation(async (command: string, args?: { method?: string; label?: string }) => {
      if (command === "tg_native_open") {
        const label = String(args?.label ?? "tg-native-mihomo_party");
        lastHandle = {
          label,
          once: vi.fn(async (event: string, handler: (event: unknown) => void) => {
            handlers.set(event, handler);
            return () => undefined;
          }),
          setFocus: vi.fn(async () => undefined),
        };
        webviewGetByLabelMock.mockImplementation(
          async (q: string) =>
            lastHandle && (lastHandle as { label: string }).label === q ? lastHandle : null,
        );
        return null;
      }
      if (args?.method === "telegram.status") return statusPayload(true);
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${command}/${args?.method}` });
    });
    return { handlers, handle: () => lastHandle };
  }

  beforeEach(() => {
    // 注册表/注意力表挂模块级(v9 会话内持久语义),用例间复位互不牵连
    resetTgNativeForTests();
    WebviewWindowMock.mockReset();
    // function 实现(非箭头):vi.fn(箭头)在 vitest 4 不可 new,注册表
    // realDeps.create 走真实构造,箭头实现会让建窗链误入「窗口创建异常」
    WebviewWindowMock.mockImplementation(function () {
      return { once: vi.fn(async () => () => undefined) };
    });
    webviewGetByLabelMock.mockReset();
    webviewGetByLabelMock.mockResolvedValue(null);
    webviewGetAllMock.mockReset();
    webviewGetAllMock.mockResolvedValue([]);
  });

  it("段控件仅 TG 渠道渲染(③ 如实无钮):网站/日报渠道详情 feed-tg-view-toggle 全空,TG 渠道在场且缺省「情报视图」active", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    // 网站 3 级
    await renderChannelDetail("tech-source", "site");
    await screen.findByText("科技今日一条");
    expect(screen.queryByTestId("feed-tg-view-toggle")).toBeNull();
    expect(screen.queryByTestId("feed-tg-view-intel")).toBeNull();
    expect(screen.queryByTestId("feed-tg-view-native")).toBeNull();
    // 日报 3 级
    cleanup();
    await renderChannelDetail("daily-digest", "daily");
    expect(screen.queryByTestId("feed-tg-view-toggle")).toBeNull();
    // TG 3 级:段控件在场,缺省 intel active、原生段可点(条目带 t.me 链可推导)
    cleanup();
    await renderChannelDetail("telegram-seed", "tg");
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    expect(toggle.getAttribute("aria-label")).toBe("视图切换");
    const intel = within(toggle).getByTestId("feed-tg-view-intel");
    const native = within(toggle).getByTestId("feed-tg-view-native");
    expect(intel.getAttribute("aria-pressed")).toBe("true");
    expect(native.getAttribute("aria-pressed")).toBe("false");
    expect(native.getAttribute("disabled")).toBeNull();
    expect(native.getAttribute("title")).toContain("首次需扫码登录一次");
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeNull(); // 窗未开,徽标不亮
  });

  it("点「原生视图」→ openOrFocusNative 收 (源名, /k/ url):建窗 + 段落 native active + 红点徽标;切「情报视图」= 注意力回落但徽标不灭(不关窗,独立窗归用户管)", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    expect(nativeOpenCalls()[0]?.[1]).toEqual(
      expect.objectContaining({
        label: "tg-native-mihomo_party",
        url: "https://web.telegram.org/k/#@mihomo_party",
      }),
    );
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("true"),
    );
    expect(within(toggle).getByTestId("feed-tg-view-intel").getAttribute("aria-pressed")).toBe("false");
    // 徽标在 openOrFocusNative 完成回调入态,晚于点击态的 aria-pressed 一拍
    // (全量并行高负载下不同 tick)——waitFor 钉住,窗真亡时依旧红(不掩盖回归)
    await waitFor(() => expect(screen.queryByTestId("feed-tg-view-native-live")).toBeTruthy());
    // 存活 title 分档(深检 F7d):窗活着 → 指引程序坞/「窗口」菜单唤回
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("title")).toContain("原生窗口已打开"),
    );
    // 切「情报视图」:段回落,但窗不死 → 红点徽标仍在(两张数据皮互为冗余)
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-intel"));
    expect(within(toggle).getByTestId("feed-tg-view-intel").getAttribute("aria-pressed")).toBe("true");
    expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("false");
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeTruthy();
    // 活窗对账自洽(再进 effect 查 getByLabel,徽标不被冲掉)
    webviewGetByLabelMock.mockResolvedValue({
      label: "tg-native-mihomo_party",
      once: vi.fn(async () => () => undefined),
      setFocus: vi.fn(async () => undefined),
    });
    // 深检 N2:intel 点击写频道名键(与读侧/原生侧同口径)→ 3→2→3 再进
    // intel 保持,不弹回 native(键失配时模块表残留 native 会赢)
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggleReenter = await screen.findByTestId("feed-tg-view-toggle");
    await waitFor(() =>
      expect(within(toggleReenter).getByTestId("feed-tg-view-intel").getAttribute("aria-pressed")).toBe("true"),
    );
    expect(within(toggleReenter).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("false");
    // 徽标依赖再进 effect 的 getByLabel 异步对账(上方 mock resolved),比段
    // 状态晚一拍(全量并行下放大)——同上 waitFor;窗亡时徽标不亮照样红
    await waitFor(() =>
      expect(screen.queryByTestId("feed-tg-view-native-live")).toBeTruthy(), // 窗活着,徽标存活
    );
  });

  it("切换态会话内持久 + destroyed 回落:窗亡(tauri://destroyed)→ 徽标退场、段回落情报视图;3→2→3 再进注意力保持上次落点", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    const captured = captureOnceHandlers();
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("true"),
    );
    // 窗已活:存活对账自洽(注册表存在性真相 = getByLabel,查询应命中)
    webviewGetByLabelMock.mockResolvedValue(captured.handle());
    // 3→2 返回再进:注意力随模块级表恢复(会话内持久),徽标随对账恢复
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggleAgain = await screen.findByTestId("feed-tg-view-toggle");
    await waitFor(() =>
      expect(within(toggleAgain).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("true"),
    );
    await waitFor(() => expect(screen.queryByTestId("feed-tg-view-native-live")).toBeTruthy());
    // 窗亡:destroyed 回调(注册表建窗时登记)→ 徽标退场 + 段回落「情报视图」
    await waitFor(() => expect(captured.handlers.has("tauri://destroyed")).toBe(true));
    await act(async () => {
      captured.handlers.get("tauri://destroyed")?.({ event: "tauri://destroyed", payload: null });
    });
    await waitFor(() =>
      expect(within(toggleAgain).getByTestId("feed-tg-view-intel").getAttribute("aria-pressed")).toBe("true"),
    );
    expect(within(toggleAgain).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("false");
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeNull();
  });

  it("重复点击 = 聚焦(getByLabel 命中):构造零次、setFocus 一次、段照常落 native 且无首开注记(不重复披露)", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    webviewGetByLabelMock.mockResolvedValue({
      label: "tg-native-mihomo_party",
      once: vi.fn(async () => () => undefined),
      setFocus: vi.fn(async () => undefined),
    });
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("true"),
    );
    expect(nativeOpenCalls()).toHaveLength(0); // 零重建
    expect(webviewGetByLabelMock).toHaveBeenCalledWith("tg-native-mihomo_party");
    expect(screen.queryByTestId("feed-tg-console-preview-note")).toBeNull(); // focused 不重复首开披露
  });

  it("上限 3(getAll 过 tg-native- 前缀对账,main 不计):第 4 窗拒开 → 注记指引找窗,零构造", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    webviewGetAllMock.mockResolvedValue([
      { label: "main" },
      { label: "tg-native-a" },
      { label: "tg-native-b" },
      { label: "tg-native-c" },
    ]);
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() => expect(screen.getByTestId("feed-tg-console-preview-note").textContent).toContain("上限 3"));
    expect(nativeOpenCalls()).toHaveLength(0);
  });

  it("开窗失败(tauri://error + 复查 miss)→ 注记「原生网页版打开失败…」给打开原文回退指引,不自动改开镜像", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    const captured = captureOnceHandlers();
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    await waitFor(() => expect(captured.handlers.has("tauri://error")).toBe(true));
    // 时序钉死(返回钮批后建窗走 invoke,.then 链多一拍):先等调用方
    // created 分支的首开注记落定再点火,否则晚到的首开注记覆盖失败词面;
    // 复查剧本 = 窗亡(getByLabel 置 miss;捕获器建窗时挂的是命中面)
    await waitFor(() =>
      expect(screen.getByTestId("feed-tg-console-preview-note").textContent).toContain("扫码登录一次"),
    );
    webviewGetByLabelMock.mockResolvedValue(null);
    await act(async () => {
      captured.handlers.get("tauri://error")?.({ event: "tauri://error", payload: null });
    });
    // 复查 getByLabel 仍 miss(缺省 null)→ 真失败词面(design-v9 §1.2)
    const note = await screen.findByTestId("feed-tg-console-preview-note");
    expect(note.textContent).toContain("原生网页版打开失败");
    expect(note.textContent).toContain("打开原文");
    // 深检 F2/F7b:真失败不只出注记 —— 先行 created 落下的存活态被注册表
    // 广播单点冲掉,不留「注记说失败、红点还亮、段还 native」矛盾同屏
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("false"),
    );
    expect(within(toggle).getByTestId("feed-tg-view-intel").getAttribute("aria-pressed")).toBe("true");
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeNull();
  });

  it("深检 F7a/F1:窗亡发生在用户不在观期间(切走再关)→ 回进该渠道段控件如实回落情报视图,不亮残留 native", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    const captured = captureOnceHandlers();
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("true"),
    );
    // 切到网站渠道(注意力/存活镜像换道,destroyed 订阅由模块级持有不受
    // 组件换道影响):回 1 级 → site 列表 → tech 渠道
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-back-to-types"));
    await openChannelList("site");
    fireEvent.click(await screen.findByTestId("feed-channel-row-tech-source"));
    await screen.findByText("科技今日一条");
    // 不在观期间红绿灯关 A 窗:模块级清理(F1)回收注意力表并广播
    webviewGetByLabelMock.mockResolvedValue(null); // 系统里窗已死,对账自洽
    await act(async () => {
      captured.handlers.get("tauri://destroyed")?.({ event: "tauri://destroyed", payload: null });
    });
    // 回进 A(网站详情 → 回 1 级 → tg 列表 → telegram-seed):
    // 段控件读模块表 = intel,存活对账 = 不活 —— 两信号一致
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-back-to-types"));
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggleAgain = await screen.findByTestId("feed-tg-view-toggle");
    await waitFor(() =>
      expect(within(toggleAgain).getByTestId("feed-tg-view-intel").getAttribute("aria-pressed")).toBe("true"),
    );
    expect(within(toggleAgain).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("false");
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeNull();
  });

  it("深检 F3/F7c:telegram.status 失败(监控台条缺席)时段控件仍可点,注记在独立节点可见(capped/failed 指引不静默丢)", async () => {
    // status RPC 失败 → phase=error → 监控台条/预览钮都不出;段控件 gate 只认 isTgChannel
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "telegram.status") {
        throw JSON.stringify({ code: "internal_error", path: "$", message: "状态服务未就绪" });
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    mockNativeWorld([]);
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    // phase=error:监控台条与预览钮都不出(条 gate 严一档),空态在转
    await waitFor(() => expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "telegram-seed" })));
    expect(screen.queryByTestId("feed-tg-console")).toBeNull();
    expect(screen.queryByTestId("feed-tg-console-preview")).toBeNull();
    // 段控件 gate 只认 isTgChannel,照常可点
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    // 建窗成功 + 首开注记落在与监控台条同层的独立节点(gate 只认 isTgChannel)
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    const note = await screen.findByTestId("feed-tg-console-preview-note");
    expect(note.textContent).toContain("扫码登录一次");
  });

  it("深检 F4b:同会话关窗重开不再假预告「首次」——二次 created 无全量扫码注记(title 词面恒在)", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    const captured = captureOnceHandlers();
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    expect((await screen.findByTestId("feed-tg-console-preview-note")).textContent).toContain("扫码登录一次");
    // 关窗(destroyed)→ 再点开:窗口重建但注意力记忆在,全量「首次」注记不重现
    webviewGetByLabelMock.mockResolvedValue(null); // 窗亡对账自洽(再开走重建)
    await act(async () => {
      captured.handlers.get("tauri://destroyed")?.({ event: "tauri://destroyed", payload: null });
    });
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("false"),
    );
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(2));
    await waitFor(() =>
      expect(within(toggle).getByTestId("feed-tg-view-native").getAttribute("aria-pressed")).toBe("true"),
    );
    // 深检 N1:存活态跟「窗建成」走不跟「首开披露」走 —— 重开窗活着,红点必须亮
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-console-preview-note")).toBeNull(); // 不重复披露
  });

  it("深检 F7f 组件层双击竞态:连点两发 → 第二发撞窗聚焦(created×1 + focused×1),不误报失败注记,存活态/段态收敛一致", async () => {
    mockStatusOnly(true);
    mockNativeWorld([]);
    // 时序剧本(仿注册表 raceDeps):首查 miss(建窗)→ 第二发查命中(聚焦)。
    // fireEvent 同步派发两 click,两发的 getByLabel 在任一 create 前依次发生:
    // 第 1 发吃 Once(null),第 2 发读得 twin → 幂等视同聚焦
    const twin = {
      label: "tg-native-mihomo_party",
      once: vi.fn(async () => () => undefined),
      setFocus: vi.fn(async () => undefined),
    };
    WebviewWindowMock.mockImplementation(function () {
      return {
        label: "tg-native-mihomo_party",
        once: vi.fn(async () => () => undefined),
        setFocus: vi.fn(async () => undefined),
      };
    });
    webviewGetByLabelMock.mockReset();
    webviewGetByLabelMock.mockResolvedValueOnce(null);
    webviewGetByLabelMock.mockResolvedValue(twin);
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    const nativeBtn = within(toggle).getByTestId("feed-tg-view-native");
    fireEvent.click(nativeBtn);
    fireEvent.click(nativeBtn); // 双击双触发
    // 第 1 发 created(构造恰一次)+ 第 2 发 focused(零重建,聚焦一次)
    await waitFor(() => expect(nativeOpenCalls()).toHaveLength(1));
    await waitFor(() => expect(twin.setFocus).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(nativeBtn.getAttribute("aria-pressed")).toBe("true"),
    );
    expect(screen.queryByTestId("feed-tg-view-native-live")).toBeTruthy();
    // 不误报失败:首开披露在(created && firstOpen),但绝无「打开失败」词面
    const note = await screen.findByTestId("feed-tg-console-preview-note");
    expect(note.textContent).toContain("扫码登录一次");
    expect(note.textContent).not.toContain("打开失败");
  });

  it("登录前(tgWebline accounts 全 logged_in:false)→ 首开注记含「扫码登录一次」与「安全提醒」词面(③ 披露钉进测试);监控台未登录词面与 /k/ 线不串台", async () => {
    mockStatusOnly(false);
    mockNativeWorld([]);
    renderScreen();
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-seed"));
    const toggle = await screen.findByTestId("feed-tg-view-toggle");
    fireEvent.click(within(toggle).getByTestId("feed-tg-view-native"));
    const note = await screen.findByTestId("feed-tg-console-preview-note");
    expect(note.textContent).toContain("扫码登录一次");
    expect(note.textContent).toContain("安全提醒");
    expect(note.textContent).toContain("属预期");
    // 词面分工:监控台「未登录」警示只说 watcher 的 7×24 监控,不混 /k/ 语义
    expect(screen.getByText(/未登录 —— 扫码登录网页版/).textContent).not.toContain("原生视图");
  });
});

describe("FeedScreen · 聊天主页风格形态锚(10-09 v4,v7 左栏落点)", () => {
  it("TG 气泡形态(10-13 随迁):泡体单箱零双泡 —— 根 = 纯布局层(零边框零着色,w-fit/min-w/max-w 72% 锚),未读亮泡在气泡 div,组尾不对称尾角;泡底展开钮(hover 浮现)+时间同排;展开态富块不在着色泡内(P2-3 延续)", async () => {
    // 条目数组造在实现外(mockImplementation 每调用重造会让 id 漂移,查
    // feed-item-1 永远落空——10-09 形态锚用例踩坑实录);image_ocr 备展开态
    // 富块(OCR 块,P2-3 断言锚)
    const chatItems = [fixtureItem({ source: "telegram-durov", title: "消息甲", content: "摘要甲", tags: ["ai"], image_ocr: "配图文字" })];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(chatItems.filter((item) => !params?.source || item.source === params.source)),
      ),
    );
    // v7:TG 气泡卡在 TG 渠道选中的聊天时间线里(点右栏 TG 行进入)
    await renderChannelDetail("telegram-durov");
    const card = await screen.findByTestId("feed-item-1");
    expect(card.className).toContain("w-fit");
    expect(card.className).toContain("max-w-");
    // 10-13 气泡重做:根不再画框着色(双泡观感根除),泡体 = 唯一可见箱
    // (bg-muted 实色卡面档无边框;单条消息自成一组 = 组尾,rounded-bl-md 尾角)
    const bubble = within(card).getByTestId("feed-tg-bubble-1");
    expect(bubble.className).toContain("bg-muted");
    expect(bubble.className).toContain("rounded-bl-md");
    expect(bubble.className).toContain("rounded-2xl");
    expect(card.className).not.toContain("bg-card");
    expect(card.className).not.toContain("border");
    expect(card.className).not.toContain("bg-primary/10");
    expect(within(card).queryByTestId("feed-strip-1")).toBeNull();
    expect(within(card).queryByText("ai")).toBeNull();
    // 泡底时间(追加批⑥):聊天语境三档词面,fresh 夹具 = 今天 HH:mm
    const footer = within(card).getByText(/^(今天|昨天) \d{2}:\d{2}$/).closest("div");
    expect(footer?.className).toContain("justify-end");
    // 内联展开钮在泡底行(hover/键盘聚焦浮现,静态裸 chevron 退役):
    // 点击翻转为「收起条目」(与详情弹窗并存),键盘聚焦可拉回可见
    const expandButton = within(footer as HTMLElement).getByRole("button", { name: "展开条目" });
    expect(expandButton.className).toContain("opacity-0");
    expect(expandButton.className).toContain("focus-visible:opacity-100");
    fireEvent.click(expandButton);
    expect(within(footer as HTMLElement).getByRole("button", { name: "收起条目" })).toBeTruthy();
    // P2-3:展开态富块(OCR 全文块)是泡外兄弟节点,落在时间线底色上,
    // 不在着色泡内(双泡观感根除;正文/标题仍在泡内)
    const ocrBlock = within(card).getByTestId("feed-image-ocr-1");
    expect(bubble.contains(ocrBlock)).toBe(false);
    expect(card.contains(ocrBlock)).toBe(true);
    expect(within(bubble as HTMLElement).queryByTestId("feed-image-ocr-1")).toBeNull();
  });

  it("日期胶囊(v7):TG 渠道左栏聊天视图分组头走居中胶囊(rounded-full+mx-auto);网站渠道条目单列零组头", async () => {
    const chipItems = [
      fixtureItem({ source: "telegram-durov", title: "消息甲", category: "telegram-groups" }),
      fixtureItem({ source: "openai-news", title: "新闻乙", category: "tech" }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(chipItems.filter((item) => !params?.source || item.source === params.source)),
      ),
    );

    // 1 级(v8 首屏):零组头
    await renderOverview();
    expect(screen.queryByTestId(/^feed-group-/)).toBeNull();
    // TG 卡 → 2 级点渠道行 → 3 级聊天视图:居中日期胶囊
    await openChannelList("tg");
    fireEvent.click(await screen.findByTestId("feed-channel-row-telegram-durov"));
    const chip = await screen.findByTestId("feed-group-今天");
    expect(chip.className).toContain("rounded-full");
    expect(chip.className).toContain("mx-auto");
  });
});

describe("feed tg-channel-card 纯函数(api.ts,10-08-tg-channel-card)", () => {
  it("channelDisplayName:去 telegram-/tg- 前缀(含 _ . 形)显频道本名;F9 起 rss-/hnrss-/urlwatch-/engine- 协议载体前缀同剥;词表外全称直出;null = 未知来源", () => {
    expect(channelDisplayName("telegram-durov")).toBe("durov");
    expect(channelDisplayName("tg-openai_news")).toBe("openai_news");
    expect(channelDisplayName("telegram_mihomo")).toBe("mihomo");
    expect(channelDisplayName("telegram-")).toBe("telegram-"); // 前缀后空,不猜
    // F9:协议载体前缀家族同剥(网页卡源名行 / L2 渠道行共用此词表)
    expect(channelDisplayName("rss-economist")).toBe("economist");
    expect(channelDisplayName("hnrss-frontpage")).toBe("frontpage");
    expect(channelDisplayName("urlwatch-blog")).toBe("blog");
    expect(channelDisplayName("engine_prompt_daily")).toBe("prompt_daily");
    // 词表外不猜:非前缀源全称直出
    expect(channelDisplayName("openai-news")).toBe("openai-news");
    expect(channelDisplayName("steam-specials")).toBe("steam-specials");
    expect(channelDisplayName(null)).toBe("未知来源");
  });
});

// ---------------------------------------------------------------------------
// 深审修复批(feed 面):F1 L1/L2 按品类查询(假空态)/ F2 请求序号守卫 /
// F4 markdown 链接受控门 / F5 价格键宽容解析 / F6 热键守卫补 <select>
// (F3 作用域收窄并入 g9-read-all 批重写;F7 分组口径并入 D4 纯函数批)
// ---------------------------------------------------------------------------

describe("FeedScreen · 深审修复批(F2/F4/F5/F6,v7 双缓冲双票迁移)", () => {
  /** 按请求参数记账的 deferred 捕获(v7 双缓冲:catalog(无 source)与
   *  stream(带 source)两域并发在途,须按参数取票,防 splice 序错位)。 */
  function paramDeferreds() {
    const pending: Array<{
      source?: string;
      before?: string;
      resolve: (value: StoreItemsResult) => void;
    }> = [];
    const impl = (params?: StoreItemsParams) =>
      new Promise<StoreItemsResult>((resolve) => {
        pending.push({ source: params?.source, before: params?.before, resolve });
      });
    const take = (match: { source?: string }) => {
      const index = pending.findIndex((entry) => entry.source === match.source);
      const entry = pending.splice(index === -1 ? 0 : index, 1)[0];
      if (!entry) throw new Error(`paramDeferreds:无在途请求可取(source=${match.source ?? "无"})`);
      return entry.resolve;
    };
    return { pending, impl, take };
  }

  it("F2 竞态一:refresh 慢应答不覆盖 liveRefreshStream 已并入的新行(请求序号守卫;选中渠道内)", async () => {
    let emitEvent: ((event: { type: string }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string }) => void;
      return Promise.resolve(() => {});
    });
    const existing = fixtureItem({ title: "旧行" });
    const fresh = fixtureItem({ title: "新行" });
    const calls = paramDeferreds();
    storeItemsMock.mockImplementation(calls.impl);
    renderScreen();
    // 铺底应答旧行 → 1→2→3 下钻选中渠道
    await waitFor(() => expect(calls.pending.length).toBeGreaterThan(0));
    act(() => calls.pending.splice(0).forEach((entry) => entry.resolve(result([existing]))));
    await openChannelList("site");
    fireEvent.click(await screen.findByTestId("feed-channel-row-Example"));
    await waitFor(() => expect(calls.pending.some((entry) => entry.source === "Example")));
    act(() => calls.take({ source: "Example" })(result([existing])));
    await screen.findByText("旧行");
    expect(screen.queryByText("新行")).toBeNull();

    // 手点刷新(stream 票 N,应答挂起)→ 事件双刷:liveRefreshStream(票 N+1)
    // 先回,带回新行(catalog 域旧票不受牵连,双票互不踩)
    fireEvent.click(screen.getByRole("button", { name: "刷新" }));
    const refreshDefer = calls.take({ source: "Example" });
    act(() => emitEvent?.({ type: "cron.completed" }));
    const liveStreamDefer = calls.take({ source: "Example" });
    act(() => calls.take({ source: undefined })(result([existing]))); // liveRefreshCatalog 先落(静默)
    act(() => liveStreamDefer(result([fresh, existing])));
    expect(await screen.findByText("新行")).toBeTruthy(); // liveRefreshStream 已并入

    // refresh 的旧应答(无新行)回场:对票失败丢弃,不整页覆盖掉新行
    act(() => refreshDefer(result([existing])));
    await waitFor(() => expect(screen.getByText("新行")).toBeTruthy()); // 新行仍在场
    expect(screen.getByText("旧行")).toBeTruthy();
  });

  it("F2 竞态二:切渠道后在途的旧域 liveRefreshStream 应答丢弃(旧渠道行不混进新渠道流)", async () => {
    let emitEvent: ((event: { type: string }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string }) => void;
      return Promise.resolve(() => {});
    });
    const itemA = fixtureItem({ source: "t-a", title: "域内行" });
    const itemB = fixtureItem({ source: "t-b", title: "乙渠道行" });
    const foreign = fixtureItem({ title: "全局外性行", source: "t-a" });
    const calls = paramDeferreds();
    storeItemsMock.mockImplementation(calls.impl);
    renderScreen();
    // 铺底(全域两渠道)→ 1→2→3 下钻选中 A 渠道(t-a 无前缀 = site 档)
    await waitFor(() => expect(calls.pending.length).toBeGreaterThan(0));
    act(() => calls.pending.splice(0).forEach((entry) => entry.resolve(result([itemA, itemB]))));
    await openChannelList("site");
    fireEvent.click(await screen.findByTestId("feed-channel-row-t-a"));
    await waitFor(() => expect(calls.pending.some((entry) => entry.source === "t-a")));
    act(() => calls.take({ source: "t-a" })(result([itemA])));
    await screen.findByText("域内行");

    // 事件 liveRefreshStream(旧域 t-a,票 N)在途未答 → 回 2 级 → 选 B 渠道。
    // 回 2 级 = 离开 3 级清流态;catalog liveRefresh 应答先落,行列表不缺行。
    act(() => emitEvent?.({ type: "cron.completed" }));
    const staleLiveDefer = calls.take({ source: "t-a" });
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    await waitFor(() => expect(calls.pending.some((entry) => entry.source === undefined)));
    act(() => calls.take({ source: undefined })(result([itemA, itemB])));
    fireEvent.click(await screen.findByTestId("feed-channel-row-t-b"));
    await waitFor(() => expect(calls.pending.some((entry) => entry.source === "t-b")));
    act(() => calls.take({ source: "t-b" })(result([itemB])));
    await screen.findByText("乙渠道行");

    // 旧域 liveRefreshStream 应答回场(带回 t-a 行):对票失败丢弃,不混入 B 渠道流
    act(() => staleLiveDefer(result([foreign, itemA])));
    await waitFor(() => expect(screen.queryByText("域内行")).toBeNull());
    expect(screen.getByText("乙渠道行")).toBeTruthy();
  });

  it("F4:markdown 文档链接走 openInBrowser 受控门(默认导航被拦,shell.open 收到 URL)", async () => {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [categoryEntry({ id: "ai-vendor-watch", sources: [sourceEntry("ai-vendor-watch", "prompt")] })],
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
    await renderChannelDetail("ai-vendor-watch", "daily"); // prompt engine → 日报档
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

  it("F6:u/j/k 热键守卫补 <select> —— 下拉聚焦时敲 j 不巡游(无 focus 环;渠道详情内)", async () => {
    mockYamlSidecar();
    storeItemsMock.mockResolvedValue(result([fixtureItem({ title: "甲" }), fixtureItem({ title: "乙" })]));
    await renderChannelDetail();
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
    // 对照:非输入目标上敲裸 j 正常巡游(首卡亮环;v8 三层单环:3 级条目直属 j/k)
    fireEvent.keyDown(window, { key: "j" });
    await waitFor(() => {
      const cards = screen.getAllByTestId(/^feed-item-/);
      expect(cards.some((node) => node.getAttribute("data-nav-focused") === "true")).toBe(true);
    });
  });
});

/** 关详情弹窗:Esc 关闭 + 等离场卸载(dialog.tsx EXIT_UNMOUNT_MS=120ms) */
async function closeDetailDialog() {
  fireEvent.keyDown(screen.getByRole("dialog"), { key: "Escape" });
  await waitFor(() => expect(screen.queryByTestId("feed-detail-dialog")).toBeNull());
}

describe("FeedScreen · 消息详情弹窗(点击信息弹出详情)", () => {
  it("点标题开弹窗:标题全文 / 元信息簇(来源/品类/时间/评分)/ 动作簇齐;弹开即记已读", async () => {
    const item = fixtureItem({ source: "openai-news", category: "tech", scores: { tech: 0.92 } });
    storeItemsMock.mockResolvedValue(result([item]));
    await renderChannelDetail("openai-news");
    fireEvent.click(await screen.findByText("条目 1"));

    const dialog = screen.getByTestId("feed-detail-dialog");
    expect(within(dialog).getByTestId("feed-detail-title").textContent).toContain("条目 1");
    const meta = within(dialog).getByTestId("feed-detail-meta");
    expect(meta.textContent).toContain("openai-news"); // 来源渠道
    expect(meta.textContent).toContain("tech"); // 品类
    expect(meta.textContent).toContain("0.92"); // 精评评分
    // 动作簇:复用卡内既有实现(👍👎 反馈/打开原文/复制链接/星标/稍后读/
    // 已读切换);弹开即记已读 → 已读钮呈「标记未读」向
    for (const name of ["好评", "差评", "打开原文", "复制链接", "星标", "稍后读", "标记未读"]) {
      expect(within(dialog).getByRole("button", { name })).toBeTruthy();
    }
    // 弹开即记已读:关闭后卡在「未读」过滤下离场
    await closeDetailDialog();
    await waitFor(() => expect(screen.queryByText("条目 1")).toBeNull());
  });

  it("Esc 与遮罩点击两条关闭路都通;关闭后列表回归", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    await renderChannelDetail();
    fireEvent.click(await screen.findByText("条目 1"));
    expect(screen.getByTestId("feed-detail-dialog")).toBeTruthy();
    await closeDetailDialog(); // Esc 路

    // 遮罩点击路(mousedown 落在 overlay 本尊)
    fireEvent.click(await screen.findByText("条目 2"));
    fireEvent.mouseDown(document.querySelector('[data-slot="dialog-overlay"]') as Element);
    await waitFor(() => expect(screen.queryByTestId("feed-detail-dialog")).toBeNull());
  });

  it("弹窗内动作生效:星标翻转即时回显(aria-pressed),与卡面同一状态源", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem(), fixtureItem()]));
    await renderChannelDetail();
    fireEvent.click(await screen.findByText("条目 1")); // 弹开即已读,卡离场,弹窗驻留
    const dialog = screen.getByTestId("feed-detail-dialog");
    const star = within(dialog).getByRole("button", { name: "星标" });
    expect(star.getAttribute("aria-pressed")).toBe("false");
    fireEvent.click(star);
    await waitFor(() =>
      expect(within(dialog).getByRole("button", { name: "星标" }).getAttribute("aria-pressed")).toBe("true"),
    );
  });

  it("TG 气泡/收起态正文区点击同门开弹窗;「展开条目」内联路径并存不弹窗", async () => {
    storeItemsMock.mockResolvedValue(
      result([fixtureItem({ source: "telegram-durov", title: "消息正文甲", content: "气泡内摘要" })]),
    );
    await renderChannelDetail("telegram-durov");
    const card = await screen.findByTestId("feed-item-1");

    // 内联展开条目:就地展开正文(TG 展开正文在气泡内),零弹窗(v2.1 明确保留并存)
    fireEvent.click(within(card).getByRole("button", { name: "展开条目" }));
    expect(within(card).getByRole("button", { name: "收起条目" })).toBeTruthy();
    expect(screen.queryByTestId("feed-detail-dialog")).toBeNull();

    // 气泡标题点击 → 弹窗(标题全文 + 正文全文)
    const bubble = within(card).getByTestId("feed-tg-bubble-1");
    const bubbleTitle = "消息正文甲";
    fireEvent.click(within(bubble).getByRole("button", { name: bubbleTitle }));
    expect(screen.getByTestId("feed-detail-dialog")).toBeTruthy();
    expect(screen.getByTestId("feed-detail-title").textContent).toContain("消息正文甲");
    expect(screen.getByTestId("feed-detail-content").textContent).toContain("气泡内摘要");
    await closeDetailDialog();
  });

  it("图析条目弹窗:OCR 全文与 VL 图说在场(卡面摘要行的全文面)", async () => {
    storeItemsMock.mockResolvedValue(
      result([fixtureItem({ image_ocr: "GPT-5 发布会\n关键数字 42", image_caption: "发布会主视觉" })]),
    );
    await renderChannelDetail();
    fireEvent.click(await screen.findByText("条目 1"));
    expect(screen.getByTestId("feed-detail-ocr").textContent).toContain("关键数字 42");
    expect(screen.getByTestId("feed-detail-caption").textContent).toContain("发布会主视觉");
    await closeDetailDialog();
  });
});

// ---------------------------------------------------------------------------
// 审计整改批(10-08 v2.1):F2 计数口径 / F3 节头细条 / F5 墙层巡游 /
// F6 可见作用域标题 / F10 墙卡次级概览
// ---------------------------------------------------------------------------

describe("FeedScreen · 审计整改批(F2/F5/F6,v5 词面落位)", () => {
  /** v5 夹具:TG 两条(同渠道,较新)+ 网页两条(两源,较旧,category=tech);
   *  刻度显式给,卡序确定(first_seen 新→旧)。options.total = 模拟 sidecar
   *  v13 with_total 应答的 total(仅请求带 with_total 才回带,与旧 sidecar
   *  忽略未知参数同门;缺省不回带 = F2 半程词面路径)。 */
  function mockStoreV12(options: { webExtra?: number; total?: number } = {}) {
    // 时间戳相对刻度 + 当日窗锚地板钳制(10-09 教训:硬编码日期在 03:00
    // 翻面后出窗;纯 now-N 小时在 03:00-05:00 跑同样出窗 —— 以
    // dayWindowStart()+递增分钟为地板,永在窗内且 t2>t1 保序)。
    const anchor = dayWindowStart().getTime();
    const inWindow = (ms: number, floorMin: number) =>
      new Date(Math.max(ms, anchor + floorMin * 60_000)).toISOString();
    const t1 = inWindow(Date.now() - 2 * 3_600_000, 1); // 网页侧,较旧
    const t2 = inWindow(Date.now() - 1 * 3_600_000, 2); // IM 侧,较新
    const total = 2 + (options.webExtra ?? 0);
    const items = [
      fixtureItem({ source: "telegram-mihomo_party_group", title: "🎉 Clash Party Dev Build 开发版本发布", content: "基于版本: 1.9.5", first_seen: t2 }),
      fixtureItem({ source: "telegram-mihomo_party_group", title: "🎉 Clash Party 1.9.4", first_seen: t2 }),
      fixtureItem({ source: "openai-news", title: "新闻标题丙", category: "tech", first_seen: t1 }),
      ...Array.from({ length: total - 3 }, (_, index) =>
        fixtureItem({ source: "hnrss-frontpage", title: `HN 条目 ${index + 1}`, category: "tech", first_seen: t1 }),
      ),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) => {
      const rows = items.filter((item) => {
        if (params?.category && item.category !== params.category) return false;
        if (params?.source && item.source !== params.source) return false;
        return true;
      });
      return Promise.resolve({
        ...result(rows),
        // v13 同门:仅 with_total 请求回带 total;options.total 缺省 = 同 WHERE
        // 行数(语义忠实),显式给值则模拟「库里有未加载条目」的截断场景
        ...(params?.with_total ? { total: options.total ?? rows.length } : {}),
      });
    });
  }

  it("F5 补充:消息卡上裸 j + Enter = 开详情弹窗(v8 三层单环:3 级条目直属 j/k;button 聚焦时 Enter 归原生)", async () => {
    mockStoreV12();
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    markMock.mockResolvedValue({ updated: 1 }); // Enter 开详情即记已读,走服务端置位
    await renderChannelDetail("telegram-mihomo_party_group"); // TG 渠道 3 级:气泡时间线
    // 等时间线渲染就位再巡游(renderChannelDetail 只等查询发出,不等应答渲染)
    await screen.findByTestId("feed-chat-timeline");
    // 裸 j 未选中落首卡(展示序首卡 = item-1),Enter 开详情
    fireEvent.keyDown(window, { key: "j" });
    await waitFor(() =>
      expect(screen.getByTestId("feed-item-1").getAttribute("data-nav-focused")).toBe("true"),
    );
    fireEvent.keyDown(window, { key: "Enter" });
    expect(screen.getByTestId("feed-detail-dialog")).toBeTruthy();
    expect(screen.getByTestId("feed-detail-title").textContent).toContain("🎉 Clash Party Dev Build 开发版本发布");
    await closeDetailDialog();
  });

  it("F2:hasMore 时词面「已加载 N 条(首页截断)」(v7 条目计数 = feed-stream-count,右栏脚注独占 feed-count)", async () => {
    // hnrss 渠道 50 条(源作用域首页满页)→ 左栏流 hasMore
    mockStoreV12({ webExtra: 51 });
    await renderChannelDetail("hnrss-frontpage");
    fireEvent.click(screen.getByRole("button", { name: "过滤:全部" }));
    const count = await screen.findByTestId("feed-stream-count");
    await waitFor(() =>
      expect(count.textContent).toContain("已加载 50 条(首页截断,更早条目未计入)"),
    );
    expect(count.textContent).not.toContain("共 103 条");
  });

  it("F2 根治(protocol ≥ 13):with_total 应答在场 → 词面「已加载 X · 共 T 条」+ title 注记口径(R1:无「当日窗」残词)", async () => {
    // 过 COUNT_PROTOCOL 门(protocol 13)→ 首拉带 with_total;total(103)
    // > 已加载(53)→ T 在词面;旧 sidecar(v12)回落上一用例的半程词面
    mockStoreV12({ webExtra: 51, total: 103 });
    versionMock.mockResolvedValue(versionResult(COUNT_PROTOCOL));
    await renderChannelDetail("hnrss-frontpage");
    // 工具条:「已加载 50 / 50 · 共 103 条」(缺省未读过滤档,X = 可见/已加载,
    // T = 同 WHERE 全量;50 条全未读故可见=已加载)
    const count = await screen.findByTestId("feed-stream-count");
    await waitFor(() => expect(count.textContent).toContain("已加载 50 / 50 · 共 103 条"));
    expect(count.getAttribute("title")).toContain("全量计数");
    expect(count.getAttribute("title")).toContain("已加载口径");
    // R1 吸收(v6 残留词面「已加载 N 条为当日窗视图首页」根除)
    expect(count.getAttribute("title")).not.toContain("当日窗");
    // 请求面实锤:过门后 store.items 确带 with_total(F2 根治的数据源)
    expect(storeItemsMock.mock.calls.some((call) => (call[0] as StoreItemsParams | undefined)?.with_total === true)).toBe(true);
  });

  it("F2 根治回落面:未过 COUNT_PROTOCOL 门(protocol 12)不发 with_total、total 态不出现", async () => {
    mockStoreV12({ webExtra: 51, total: 103 });
    await renderChannelDetail("hnrss-frontpage"); // versionMock = 缺省 9 < COUNT_PROTOCOL(13),门未过
    // 门未过 → 请求零 with_total(sidecar v12 忽略未知参数属预期,不报错;
    // 应答自然无 total 键 → UI 不采信不存在的数据)
    expect(storeItemsMock.mock.calls.some((call) => (call[0] as StoreItemsParams | undefined)?.with_total === true)).toBe(false);
    // 词面维持 F2 半程:截断如实,无「共 T」全量词面
    const count = await screen.findByTestId("feed-stream-count");
    await waitFor(() => expect(count.textContent).toContain("已加载 50 / 50 条"));
    expect(count.textContent).not.toContain("共 103 条");
  });

  it("F6:作用域词随级切换(v8:1 级 sr-only 全部情报 → 3 级渠道名;逐级回退词面复原)", async () => {
    mockStoreV12();
    await renderOverview();
    // 1 级:作用域词保留为 sr-only 播报(不占视觉位,§1.4)
    expect(screen.getByText("全部情报")).toBeTruthy();
    await openChannelList("site");
    fireEvent.click(await screen.findByTestId("feed-channel-row-openai-news"));
    await waitFor(() =>
      expect(screen.getByTestId("feed-stream-title").textContent).toContain("openai-news"),
    );
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    fireEvent.click(await screen.findByTestId("feed-back-to-types"));
    await screen.findByTestId("feed-type-card-tg");
    expect(screen.getByText("全部情报")).toBeTruthy();
  });
});

describe("feed 审计整改 纯函数(api.ts)", () => {
  it("F8:tech 落淡紫档 #cdb6fb(卡底 9.02:1 过 AA)——不再落 #8b5cf6(3.83:1 欠档)", () => {
    expect(categoryColor("tech")).toBe("#cdb6fb");
    // 色板全体仍非空、稳定:同品类恒同色
    expect(categoryColor("tech")).toBe(categoryColor("tech"));
  });

});

// ---------------------------------------------------------------------------
// 验收挑刺整改批(10-08 v2.2):①正文复述标题(bodyWithoutTitleDup 一门
// 四处消费)② TG 分节节内卡省频道名行 ③ 未读竖条提亮 primary-300
// ⑤ 弹窗动作簇权重理顺(④ 墙层满宽密度 = 设计取向,记录备审不动码)
// ---------------------------------------------------------------------------

describe("feed 验收整改 纯函数(api.ts)", () => {
  it("bodyWithoutTitleDup:剥与标题逐字重复的开头(含冒号),正文整段 = 标题 → null,无标题/不重复 → 原文,保换行原格式", () => {
    // TG 消息形态:title = 首行,content = 全文
    expect(
      bodyWithoutTitleDup({ title: "发布 v2", content: "发布 v2\n基于版本: 1.9.5" }),
    ).toBe("基于版本: 1.9.5");
    // 中文冒号衔接同剥
    expect(bodyWithoutTitleDup({ title: "发布", content: "发布：正文内容" })).toBe("正文内容");
    // 正文整段 = 标题 → null(无独有信息,消费侧不渲染重复行)
    expect(bodyWithoutTitleDup({ title: "同文", content: "同文" })).toBeNull();
    expect(bodyWithoutTitleDup({ title: "同文", content: "  同文  " })).toBeNull();
    // 不以标题开头 → 原文原样(保换行)
    expect(bodyWithoutTitleDup({ title: "甲", content: "乙\n丙" })).toBe("乙\n丙");
    // 无标题 / 空正文
    expect(bodyWithoutTitleDup({ title: "", content: "正文" })).toBe("正文");
    expect(bodyWithoutTitleDup({ title: "甲", content: "  " })).toBeNull();
    expect(bodyWithoutTitleDup({ title: "甲", content: null })).toBeNull();
  });

  it("cardDigest 与 bodyWithoutTitleDup 同门(v3 去重语义不回归):去重后压平取头、超长省略号", () => {
    const tg = fixtureItem({
      source: "telegram-a",
      title: "🎉 Clash Party Dev Build 开发版本发布",
      content: "🎉 Clash Party Dev Build 开发版本发布 基于版本: 1.9.5",
    });
    expect(cardDigest(tg)).toBe("基于版本: 1.9.5");
    // 正文整段 = 标题:digest 落 null(不回事件词;watch 词仅 content 全空)
    expect(cardDigest(fixtureItem({ source: "telegram-a", title: "同文", content: "同文" }))).toBeNull();
  });
});

describe("FeedScreen · 验收整改批(正文去重/节内省频道名/弹窗权重)", () => {
  it("① TG 气泡收起正文行不再复述标题;正文整段 = 标题时正文行消失;展开态仍全文", async () => {
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({
          source: "telegram-durov",
          title: "🎉 Clash Party v2 发布",
          content: "🎉 Clash Party v2 发布\n基于版本: 1.9.5",
        }),
      ]),
    );
    await renderChannelDetail("telegram-durov");
    const card = await screen.findByTestId("feed-item-1");
    const bubble = within(card).getByTestId("feed-tg-bubble-1");
    // 收起态:正文行只剩独有信息(版本号),标题不复述 —— 全文词面仅标题按钮 1 处
    expect(within(bubble).getAllByText("🎉 Clash Party v2 发布")).toHaveLength(1);
    expect(within(bubble).getByText("基于版本: 1.9.5")).toBeTruthy();
    // 展开态 = 全文位:原文整体在场(含复述,展开是显式要全文)
    fireEvent.click(within(card).getByRole("button", { name: "展开条目" }));
    expect(within(bubble).getAllByText(/🎉 Clash Party v2 发布/)).toHaveLength(2);
  });

  it("① 收起摘要行(新闻卡)去标题前缀;正文整段 = 标题 → 摘要行不渲染", async () => {
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({ title: "OpenAI 发布 G-6", content: "OpenAI 发布 G-6 详见官网公告与模型卡。", source: "openai-news" }),
        fixtureItem({ title: "复读机条目", content: "复读机条目", source: "openai-news" }),
      ]),
    );
    await renderChannelDetail("openai-news");
    const card1 = await screen.findByTestId("feed-item-1");
    // 摘要行只剩独有信息;标题词面全卡仅标题按钮 1 处
    expect(within(card1).getAllByText(/OpenAI 发布 G-6/)).toHaveLength(1);
    expect(within(card1).getByText(/详见官网公告与模型卡/)).toBeTruthy();
    // 正文 = 标题:无摘要行(标题词面 1 处),不再同屏读两遍
    const card2 = await screen.findByTestId("feed-item-2");
    expect(within(card2).getAllByText("复读机条目")).toHaveLength(1);
  });

  it("① 详情弹窗正文去标题重复开头;正文整段 = 标题 → 正文块零渲染", async () => {
    storeItemsMock.mockResolvedValue(
      result([
        fixtureItem({
          source: "telegram-durov",
          title: "🎉 Clash Party v2 发布",
          content: "🎉 Clash Party v2 发布\n基于版本: 1.9.5",
        }),
      ]),
    );
    await renderChannelDetail("telegram-durov");
    fireEvent.click(await screen.findByTestId("feed-item-1"));
    fireEvent.click(within(screen.getByTestId("feed-tg-bubble-1")).getByRole("button", { name: "🎉 Clash Party v2 发布" }));
    const dialog = screen.getByTestId("feed-detail-dialog");
    // 弹窗正文只剩独有信息,标题词面全弹窗仅 DialogTitle 1 处(04/05 图病灶)
    expect(within(dialog).getAllByText(/🎉 Clash Party v2 发布/)).toHaveLength(1);
    expect(within(dialog).getByTestId("feed-detail-content").textContent).toBe("基于版本: 1.9.5");
    await closeDetailDialog();
  });

  it("② TG 渠道详情气泡卡泡顶频道名行退役(10-13 气泡重做:群名一词一源只在聊天头,每条重复 = 冗余),相对时间保留", async () => {
    mockStoreV12Acceptance();
    await renderChannelDetail("telegram-mihomo_party_group");
    // 时间线内零频道名词面(词表名只随聊天头 feed-stream-title;断言收窄
    // 时间线,排除工具条作用域词/sr-only 播报的同名词面)
    const timeline = screen.getByTestId("feed-chat-timeline");
    expect(within(timeline).queryAllByText("mihomo_party_group")).toHaveLength(0);
    // 聊天头一词一源在场
    expect(screen.getByTestId("feed-stream-title").textContent).toContain("mihomo_party_group");
    // 卡头时间仍在(卡面元信息不缺;追加批⑥:聊天语境三档词面,夹具
    //  first_seen = now → 今天 HH:mm;组头胶囊「今天 · N 条」不同词形不混.match)
    expect(within(timeline).getAllByText(/^(今天|昨天) \d{2}:\d{2}$/).length).toBeGreaterThanOrEqual(2);
  });

  it("⑤ 弹窗动作簇:打开原文 = 唯一实底主钮(default),复制链接/星标/稍后读/标记未读 = ghost 同档", async () => {
    storeItemsMock.mockResolvedValue(result([fixtureItem()]));
    await renderChannelDetail();
    fireEvent.click(await screen.findByText("条目 1"));
    const actions = within(screen.getByTestId("feed-detail-dialog")).getByTestId("feed-detail-actions");
    expect(within(actions).getByRole("button", { name: "打开原文" }).className).toContain("bg-primary");
    for (const name of ["复制链接", "星标", "稍后读", "标记未读"]) {
      const button = within(actions).getByRole("button", { name });
      expect(button.className).not.toContain("bg-primary");
      expect(button.className).toContain("hover:bg-accent"); // ghost 同档标记
    }
    // 「标记未读」是弹开即已读的撤销口:title 语义明示
    expect(within(actions).getByRole("button", { name: "标记未读" }).getAttribute("title")).toContain("撤销");
    await closeDetailDialog();
  });
});

/** 验收批 v2 夹具(与 tg-channel-card v2 同门:两 TG 同渠道 + 一网页) */
function mockStoreV12Acceptance() {
  const items = [
    fixtureItem({ source: "telegram-mihomo_party_group", title: "🎉 甲", content: "甲正文" }),
    fixtureItem({ source: "telegram-mihomo_party_group", title: "🎉 乙", content: "乙正文" }),
    fixtureItem({ source: "openai-news", title: "新闻标题丙", category: "tech" }),
  ];
  storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
    Promise.resolve(
      result(
        items.filter((item) => {
          if (params?.source && item.source !== params.source) return false;
          return true;
        }),
      ),
    ),
  );
}



// ---------------------------------------------------------------------------
// 渠道卡纯函数(api.ts,v6 渠道瀑布流):类型判定 / 渠道全集聚合 / 搜索过滤
// ---------------------------------------------------------------------------

describe("feed 渠道卡 纯函数(api.ts,v8 前缀优先修订)", () => {
  it("channelCardKindOf(v8 §4.2 前缀优先):telegram-/tg- 前缀先判 → tg(engine 词表不抢判);再 DAILY_ENGINES → daily;再 TG_ENGINES;其余 → site", () => {
    // 前缀优先实锤(设计稿 §4.2 判定矛盾翻正):durov 挂 static_html(t.me
    // 公开镜像采集线)曾因 engine 先判被误归 site —— 前缀优先后归 TG
    expect(channelCardKindOf("telegram-durov", "static_html")).toBe("tg");
    expect(channelCardKindOf("telegram-mihomo_party_group", "telegram")).toBe("tg");
    expect(channelCardKindOf("telegram-mihomo_party_group", "tg_web")).toBe("tg");
    expect(channelCardKindOf("tg-openai_news", "urlwatch")).toBe("tg");
    // 日报引擎(prompt/store_report;无前缀命中时 engine 词表判)
    expect(channelCardKindOf("ai-vendor-watch", "prompt")).toBe("daily");
    expect(channelCardKindOf("daily-digest", "store_report")).toBe("daily");
    // TG 线引擎(无前缀命中的源名,engine 补判)
    expect(channelCardKindOf("x", "telethon")).toBe("tg");
    expect(channelCardKindOf("x", "bot")).toBe("tg");
    // 网站:urlwatch/rss 类与其余 engine(static_html/direct_api/auto…)
    expect(channelCardKindOf("anthropic-news-watch", "urlwatch")).toBe("site");
    expect(channelCardKindOf("openai-news", "static_html")).toBe("site");
    expect(channelCardKindOf("hnrss-frontpage", "hnrss")).toBe("site");
    expect(channelCardKindOf("w", "未知引擎")).toBe("site");
    // engine 缺席(health 词表外的纯条目侧源):前缀兜底不变
    expect(channelCardKindOf("telegram-durov", null)).toBe("tg");
    expect(channelCardKindOf("tg-openai_news", undefined)).toBe("tg");
    expect(channelCardKindOf("openai-news", null)).toBe("site");
    expect(channelCardKindOf("openai-news", "")).toBe("site");
  });

  it("feedChannelCards:全集 = engine 词表键 ∪ 条目 source 去重;零条目渠道出卡今日 0;今日按窗计,未读不限窗;latest 取最大刻;最新在前零条目沉底", () => {
    const windowStart = dayWindowStart(new Date(2026, 9, 6, 14, 0)); // 2026-10-06 03:00
    const at = (h: number) => new Date(2026, 9, 6, h, 0).toISOString();
    const tgNew = fixtureItem({ source: "telegram-a", title: "a-新", first_seen: at(12) });
    const tgOld = fixtureItem({ source: "telegram-a", title: "a-旧", first_seen: at(1) }); // 窗外(01:00 < 03:00)
    const web = fixtureItem({ source: "openai-news", title: "网页", first_seen: at(10) });
    const states = { [tgNew.dedup_key]: { read: true } };
    const engines = new Map([
      ["telegram-a", "tg_web"],
      ["daily-digest", "prompt"], // 零条目渠道(health 独有)
    ]);
    const cards = feedChannelCards([tgNew, tgOld, web], states, engines, windowStart, new Date(2026, 9, 6, 14, 0));
    // 排序:最新刻在前(telegram-a 12:00 > openai-news 10:00),零条目沉底
    expect(cards.map((card) => card.key)).toEqual(["telegram-a", "openai-news", "daily-digest"]);
    expect(cards[0].kind).toBe("tg");
    expect(cards[0].label).toBe("a");
    expect(cards[0].today).toBe(1); // 窗内 1(12:00);窗外 1(01:00)不计今日
    expect(cards[0].unread).toBe(1); // 未读不限窗:a-新已读,a-旧(窗外)未读 → 1
    expect(cards[0].latest?.title).toBe("a-新");
    expect(cards[1].kind).toBe("site");
    expect(cards[1].today).toBe(1);
    expect(cards[1].unread).toBe(1);
    // 零条目渠道也出卡:今日 0,latest null,日报徽标
    expect(cards[2].kind).toBe("daily");
    expect(cards[2].today).toBe(0);
    expect(cards[2].unread).toBe(0);
    expect(cards[2].latest).toBeNull();
    // 空入空出
    expect(feedChannelCards([], {}, new Map(), windowStart)).toEqual([]);
  });

  it("filterChannelsByQuery:渠道名/源 id 包含匹配(大小写不敏感);空串全量原样", () => {
    const cards = feedChannelCards(
      [fixtureItem({ source: "telegram-mihomo_party_group" })],
      {},
      new Map([
        ["telegram-mihomo_party_group", "tg_web"],
        ["openai-news", "static_html"],
      ]),
      dayWindowStart(),
    );
    // 搜「Tg」(主人实测词)直出全部 TG 渠道卡:t、g 不相邻,字面包含碰不到
    // "telegram" —— 类型别名同认(kind=tg 的别名表命中即直出)
    expect(cards.map((card) => card.key)).toEqual(["telegram-mihomo_party_group", "openai-news"]);
    expect(filterChannelsByQuery(cards, "Tg").map((card) => card.key)).toEqual(["telegram-mihomo_party_group"]);
    expect(filterChannelsByQuery(cards, "Tele").map((card) => card.key)).toEqual(["telegram-mihomo_party_group"]);
    // 源 id 字面包含匹配照常;别名只认前缀("tgg" 不算)
    expect(filterChannelsByQuery(cards, "MIHOMO").map((card) => card.key)).toEqual(["telegram-mihomo_party_group"]);
    expect(filterChannelsByQuery(cards, "news").map((card) => card.key)).toEqual(["openai-news"]);
    expect(filterChannelsByQuery(cards, "tgg")).toEqual([]);
    // 渠道名(词表名)匹配
    expect(filterChannelsByQuery(cards, "MIHOMO").map((card) => card.key)).toEqual(["telegram-mihomo_party_group"]);
    // 空串/纯空白 = 全量原样
    expect(filterChannelsByQuery(cards, "")).toBe(cards);
    expect(filterChannelsByQuery(cards, "  ")).toBe(cards);
    // 零命中 = 空数组
    expect(filterChannelsByQuery(cards, "不存在的渠道")).toEqual([]);
  });
});

// ---------------------------------------------------------------------------
// v8 三级界面 屏幕面新增用例(AC29-32:有源零条目并存 / stats 门双词面 /
// 3 级渠道内检索四象限,拷问 R1-Q2 三断言)
// ---------------------------------------------------------------------------

describe("FeedScreen · v8 三级界面(AC29-32 新增面)", () => {
  it("有源零条目态(拷问 R1-Q5):零值类型卡照出(卡内知会词)+ 卡墙之下并置 CTA 卡 —— 卡答渠道,CTA 答数据", async () => {
    // health 有源(零条目)→ channelCards 非空、catalogItems 空
    healthMock.mockResolvedValue(
      healthResult({
        categories: [categoryEntry({ id: "idle", sources: [sourceEntry("idle-source", "static_html")] })],
      }),
    );
    storeItemsMock.mockResolvedValue(result([]));
    renderScreen();

    // 零值卡在场(idle-source → site 档;卡内「暂无入库条目」)+ CTA 卡并存
    const siteCard = await screen.findByTestId("feed-type-card-site");
    expect(siteCard.textContent).toContain("暂无入库条目");
    expect(siteCard.textContent).toContain("今日 0 条");
    const cta = screen.getByTestId("feed-run-cta");
    expect(cta.textContent).toContain("插件已就绪,还没有任何入库条目");
    expect(screen.getByRole("button", { name: /运行第一个插件/ })).toBeTruthy();
  });

  it("stats 门过(version 14):1 级卡全库口径 title + store.source_stats 拉取;2 级行 statsScope=full 词面 + 50 条外源行预览 stats 回退", async () => {
    versionMock.mockResolvedValue(versionResult(STATS_PROTOCOL));
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "web", sources: [sourceEntry("openai-news", "static_html")] }),
          categoryEntry({ id: "hot", sources: [sourceEntry("hot-outside", "static_html")] }),
        ],
      }),
    );
    storeItemsMock.mockResolvedValue(
      result([fixtureItem({ source: "openai-news", title: "catalog 内标题", content: "净化摘要内容" })]),
    );
    sourceStatsMock.mockResolvedValue({
      db: "myssia.db",
      rows: [
        { source: "openai-news", total: 40, today: 30, unread: 20, latest_first_seen: new Date().toISOString(), latest_title: "stats 全库标题" },
        { source: "hot-outside", total: 7, today: 5, unread: 3, latest_first_seen: new Date().toISOString(), latest_title: "墙外最新一条" },
      ],
    });
    await renderOverview();

    // 过门即拉分源统计(全库真值源,门先行不发试错)
    await waitFor(() => expect(sourceStatsMock).toHaveBeenCalledWith({ since: expect.any(String) }));
    // 1 级卡:今日/未读被 stats 覆写(openai-news 30/20 + hot-outside 5/3 归并)
    const siteCard = await screen.findByTestId("feed-type-card-site");
    await waitFor(() => expect(siteCard.textContent).toContain("今日 35 条"));
    expect(siteCard.textContent).toContain("未读 23");
    expect(within(siteCard).getAllByTitle(/全库口径/).length).toBeGreaterThan(0);
    // 预览行 = stats 全库标题(catalog 最新条目刻被 stats 覆盖比较,取 stats title)
    expect(siteCard.textContent).toContain("stats 全库标题");

    // 2 级行:statsScope=full 词面 + 墙外源(50 条外活跃源)预览回退
    await openChannelList("site");
    const openaiRow = await screen.findByTestId("feed-channel-row-openai-news");
    await waitFor(() =>
      expect(screen.getByTestId("feed-channel-unread-openai-news").getAttribute("title")).toContain("全库口径"),
    );
    expect(openaiRow.getAttribute("data-unread")).toBe("true");
    const hotRow = screen.getByTestId("feed-channel-row-hot-outside");
    expect(hotRow.textContent).toContain("墙外最新一条"); // stats 回填消灭「今日暂无新条目」假知会
    expect(hotRow.textContent).not.toContain("今日暂无新条目");
    // 未过门回落面(version < 14)零 RPC 试错,由「低版本 sidecar」用例盖
  });

  it("3 级渠道内检索(拷问 R1-Q2 三断言):命中直出(未读命中可见)/ 零命中专属空态 + 读态分段隐藏 / 清空恢复分段与过滤;翻页游标携带 query", async () => {
    const readHit = fixtureItem({ title: "已读命中甲", read: true });
    const unreadOther = fixtureItem({ title: "未读条目乙" });
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    storeItemsMock.mockImplementation((params?: StoreItemsParams) => {
      const pool = [readHit, unreadOther];
      const rows = params?.query
        ? pool.filter((item) => item.title.includes(params.query!))
        : pool;
      return Promise.resolve({ ...result(rows), ...(params?.with_total ? { total: rows.length } : {}) });
    });
    await renderChannelDetail();

    // 缺省未读档:已读命中甲不可见;读态分段在场
    await screen.findByText("未读条目乙");
    expect(screen.queryByText("已读命中甲")).toBeNull();
    expect(screen.getByRole("group", { name: "读态过滤" })).toBeTruthy();

    // 检索态:分段整体隐藏(不给死控件)+ **已读**命中在检索命中中可见(全量直出,
    // 不限读态 —— 拷问 R1-Q2 断言二)
    const search = screen.getByLabelText("渠道内检索") as HTMLInputElement;
    fireEvent.change(search, { target: { value: "命中" } });
    fireEvent.keyDown(search, { key: "Enter" });
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ query: "命中" })),
    );
    expect(await screen.findByText("已读命中甲")).toBeTruthy();
    expect(screen.queryByText("未读条目乙")).toBeNull(); // 服务端 query 过滤生效
    expect(screen.queryByRole("group", { name: "读态过滤" })).toBeNull();
    expect(screen.getByTestId("feed-day-window").textContent).toContain("检索中 · 渠道内全量(不限读态)");
    expect(screen.getByTestId("feed-stream-search-note").textContent).toContain("命中");

    // 渠道内检索零命中:独立空态(防与 2 级 feed-search-empty 混)
    fireEvent.change(search, { target: { value: "不存在的词" } });
    fireEvent.keyDown(search, { key: "Enter" });
    expect(await screen.findByTestId("feed-stream-search-empty")).toBeTruthy();
    expect(screen.getByTestId("feed-stream-search-empty").textContent).toContain("没有匹配");

    // 清空恢复:分段回归 + 未读过滤生效(已读命中甲重新离场 —— 拷问 R1-Q2 断言三)
    fireEvent.keyDown(search, { key: "Escape" });
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.not.objectContaining({ query: expect.anything() })),
    );
    await screen.findByText("未读条目乙");
    expect(screen.queryByText("已读命中甲")).toBeNull();
    expect(screen.getByRole("group", { name: "读态过滤" })).toBeTruthy();

    // 检索态重查请求形状:query 与 source 同 WHERE(§4.3;翻页 loadMore 同参)
    fireEvent.change(search, { target: { value: "检索词" } });
    fireEvent.keyDown(search, { key: "Enter" });
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ query: "检索词", source: "Example" })),
    );
  });
});

// ---------------------------------------------------------------------------
// v8 三级界面 纯函数(api.ts):类型卡聚合(§5.2 诚实口径)/ stats 覆写与
// 预览回填(§2.3 拷问 R1-Q4 同根面)/ 类型搜索(§1.3)/ query 透传(§4.3)
// ---------------------------------------------------------------------------

describe("feed v8 三级界面 纯函数(api.ts)", () => {
  const statsRow = (overrides: Partial<SourceStatsRow> & { source: string | null }): SourceStatsRow => ({
    total: 10,
    today: 3,
    unread: 2,
    latest_first_seen: new Date(dayWindowStart().getTime() + 60_000).toISOString(),
    latest_title: "stats 最新标题",
    ...overrides,
  });

  it("aggregateTypeCards:成员归并(stats 全库真值)+ 卡序固定词表序 + 零渠道类型不出卡 + previews 按最新排序(帽 5)", () => {
    const engines = new Map([
      ["telegram-a", "tg_web"],
      ["telegram-b", "tg_web"],
      ["openai-news", "static_html"],
      ["daily-digest", "store_report"],
    ]);
    const cards = feedChannelCards(
      [fixtureItem({ source: "telegram-a", first_seen: new Date(dayWindowStart().getTime() + 120_000).toISOString() })],
      {},
      engines,
      dayWindowStart(),
    );
    const stats = [
      statsRow({ source: "telegram-a", today: 5, unread: 4 }),
      statsRow({ source: "telegram-b", today: 1, unread: 1 }),
      statsRow({ source: "openai-news", today: 7, unread: 6 }),
      statsRow({ source: "daily-digest", today: 0, unread: 0 }),
    ];
    const types = aggregateTypeCards(cards, stats);
    // 卡序固定词表序 tg → site → daily;零成员类型(daily 在 engines 有源则出)
    expect(types.map((type) => type.kind)).toEqual(["tg", "site", "daily"]);
    const tg = types[0];
    expect(tg.channels).toBe(2); // telegram-a + telegram-b(health 半边零条目渠道)
    expect(tg.today).toBe(6); // stats 全库真值归并(5 + 1)
    expect(tg.unread).toBe(5);
    expect(tg.statsApplied).toBe(true);
    expect(tg.label).toBe("TG");
    // previews = 成员源按 latest_first_seen 降序(帽 5;stats title 优先)
    expect(tg.previews.length).toBe(2);
    expect(tg.previews[0].channelLabel).toBe("a");
    expect(tg.previews[0].latestTitle).toBe("stats 最新标题");
    // 未过门(statsRows = null)回退 catalog 已加载口径 + statsApplied=false
    const fallback = aggregateTypeCards(cards, null);
    expect(fallback[0].statsApplied).toBe(false);
    expect(fallback[0].today).toBe(cards.find((card) => card.kind === "tg")!.today);
    // 零成员类型不出卡(engines 无 daily 源时不猜)
    const noDaily = aggregateTypeCards(
      feedChannelCards([], {}, new Map([["openai-news", "static_html"]]), dayWindowStart()),
      [statsRow({ source: "openai-news" })],
    );
    expect(noDaily.map((type) => type.kind)).toEqual(["site"]);
  });

  it("aggregateTypeCards:previews 帽 = 5(成员 >5 按 latest_first_seen 降序截断,第 6 旧源不入)", () => {
    const engines = new Map([
      ["telegram-a", "tg_web"],
      ["telegram-b", "tg_web"],
      ["telegram-c", "tg_web"],
      ["telegram-d", "tg_web"],
      ["telegram-e", "tg_web"],
      ["telegram-f", "tg_web"],
    ]);
    const cards = feedChannelCards([], {}, engines, dayWindowStart());
    const minute = 60_000;
    const stats = ["a", "b", "c", "d", "e", "f"].map((suffix, index) =>
      statsRow({
        source: `telegram-${suffix}`,
        latest_first_seen: new Date(dayWindowStart().getTime() + (6 - index) * minute).toISOString(),
        latest_title: `标题 ${suffix}`,
      }),
    );
    const types = aggregateTypeCards(cards, stats);
    const tg = types[0];
    expect(tg.channels).toBe(6);
    // 帽 = 5:a~f 六源按 latest_first_seen 降序(a 最新),f(最旧)截断在外
    expect(tg.previews.length).toBe(5);
    expect(tg.previews.map((preview) => preview.channelLabel)).toEqual(["a", "b", "c", "d", "e"]);
    expect(tg.previews[4].latestTitle).toBe("标题 e");
  });

  it("aggregateTypeCards:NULL source 行归「网站」卡 today/unread、不计渠道数(它不是渠道)", () => {
    const cards = feedChannelCards(
      [fixtureItem({ source: "openai-news" })],
      {},
      new Map([["openai-news", "static_html"]]),
      dayWindowStart(),
    );
    const stats = [
      statsRow({ source: null, today: 9, unread: 8 }),
      statsRow({ source: "openai-news", today: 1, unread: 1 }),
    ];
    const types = aggregateTypeCards(cards, stats);
    const site = types.find((type) => type.kind === "site")!;
    expect(site.channels).toBe(1); // NULL 行不计渠道数
    expect(site.today).toBe(10); // 9(NULL)+ 1(成员)
    expect(site.unread).toBe(9);
    // tg/daily 不沾 NULL 行(两档零成员本就不出卡,site 独占)
  });

  it("applySourceStats:today/unread 覆写为全库真值 + statsLatestTitle/Seen 回填(50 条外活跃源行预览回退);无行渠道原样", () => {
    const inCatalog = fixtureItem({ source: "openai-news", title: "catalog 内标题" });
    const cards = feedChannelCards(
      [inCatalog],
      {},
      new Map([
        ["openai-news", "static_html"],
        ["hot-source-outside", "static_html"], // catalog 首页 50 外的活跃源(零条目)
      ]),
      dayWindowStart(),
    );
    const stats = [
      statsRow({ source: "openai-news", today: 42, unread: 17, latest_title: "stats 覆写标题" }),
      statsRow({ source: "hot-source-outside", today: 5, unread: 3, latest_title: "墙外最新一条", latest_first_seen: new Date(dayWindowStart().getTime() + 30_000).toISOString() }),
    ];
    const applied = applySourceStats(cards, stats);
    const openai = applied.find((card) => card.key === "openai-news")!;
    expect(openai.today).toBe(42);
    expect(openai.unread).toBe(17);
    expect(openai.statsLatestTitle).toBe("stats 覆写标题");
    expect(openai.statsLatestSeen).not.toBeNull();
    // 零条目渠道(catalog 无条目 → card.latest = null)拿到 stats 预览回填
    const hot = applied.find((card) => card.key === "hot-source-outside")!;
    expect(hot.latest).toBeNull();
    expect(hot.statsLatestTitle).toBe("墙外最新一条");
    // stats 无行的渠道原样返回(零条目 0 值已是事实)
    const untouched = applySourceStats(cards, [statsRow({ source: "openai-news" })]);
    expect(untouched.find((card) => card.key === "hot-source-outside")!.statsLatestTitle).toBeUndefined();
  });

  it("filterTypesByQuery:类型别名前缀命中(搜「Tg」直出 TG 卡)/ 名字包含 / 空串全量原样", () => {
    const types = aggregateTypeCards(
      feedChannelCards(
        [fixtureItem({ source: "telegram-a" }), fixtureItem({ source: "openai-news" })],
        {},
        new Map([
          ["telegram-a", "tg_web"],
          ["openai-news", "static_html"],
        ]),
        dayWindowStart(),
      ),
      null,
    );
    // 「Tg」= tg 别名前缀(v6.1 主人实测路径同门),TG 卡独显
    expect(filterTypesByQuery(types, "Tg").map((type) => type.kind)).toEqual(["tg"]);
    // 「日报」= daily 别名整词
    expect(filterTypesByQuery(types, "网站").map((type) => type.kind)).toEqual(["site"]);
    // 类型名包含匹配(「站」∈ 网站)
    expect(filterTypesByQuery(types, "站").map((type) => type.kind)).toEqual(["site"]);
    // 空串/纯空白 = 全量原样
    expect(filterTypesByQuery(types, "")).toBe(types);
    expect(filterTypesByQuery(types, " ")).toBe(types);
    // 零命中 = 空数组(别名只认前缀,「tgg」不算)
    expect(filterTypesByQuery(types, "tgg")).toEqual([]);
  });

  it("fetchFeedPage:query 参透传(v8 §4.3 重挂,服务端渠道内检索底座)", async () => {
    const storeItemsSpy = vi.mocked(api.storeItems);
    storeItemsSpy.mockResolvedValue({ db: "t.db", count: 0, items: [] });
    await fetchFeedPage({ cursor: null, cursorId: null, source: "telegram-a", query: "版本" });
    expect(storeItemsSpy).toHaveBeenLastCalledWith(
      expect.objectContaining({ source: "telegram-a", query: "版本" }),
    );
    // query 空 = 不传参(旧 sidecar 忽略未知参数属预期,无参零面)
    await fetchFeedPage({ cursor: null, cursorId: null, source: null, query: null });
    const last = storeItemsSpy.mock.calls.at(-1)![0] as StoreItemsParams;
    expect(last.query).toBeUndefined();
    expect(last.source).toBeUndefined();
    // 翻页游标与 query 同 WHERE(检索态「加载更早」照常)
    await fetchFeedPage({ cursor: "2026-10-10T00:00:00Z", cursorId: 7, source: "a", query: "x" });
    expect(storeItemsSpy).toHaveBeenLastCalledWith(
      expect.objectContaining({ before: "2026-10-10T00:00:00Z", before_id: 7, source: "a", query: "x" }),
    );
  });
});

// ---------------------------------------------------------------------------
// weixin-feed-channel(10-12,主令翻案 G3:微信消息入情报流):类型卡第四档 +
// 聊天双栏/气泡渲染共用 + 2 级桥状态区 + 3 级 wx 监控台三态 + 空态阶梯 +
// 搜索别名 + 进会话即已读(深链/登录/原生预览 = 有意缺席,不造假)
// ---------------------------------------------------------------------------

describe("FeedScreen · weixin-feed-channel(微信入情报流,10-12)", () => {
  /** wechat_local.probe 夹具(形状对齐 messaging/api.ts WechatLocalProbeView;
   *  与消息屏 wechat-local.test.tsx probeFixture 同源) */
  const probePayload = (overrides: Partial<WechatLocalProbeView> = {}): WechatLocalProbeView => ({
    ok: true,
    state: "ok",
    checks: { bridge_component: "ok", wechat_process: "ok", screen_recording: "ok" },
    wechat_version: "4.1.15",
    bridge_version: "0.3.1",
    reasons: [],
    ...overrides,
  });

  /** 微信世界:health 给 weixin 品类单源(wechat_local 引擎,源名全称律
   *  weixin-<会话名>)+ telegram/tech 对照渠道;store.items 按源过滤。 */
  function mockWxWorld(items: FeedItem[] = []) {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "weixin", name: "微信监控", sources: [sourceEntry("weixin-测试会话", "wechat_local")] }),
          categoryEntry({ id: "telegram", name: "Telegram 监控", sources: [sourceEntry("telegram-seed", "tg_web")] }),
          categoryEntry({ id: "tech", name: "科技", sources: [sourceEntry("tech-source", "static_html")] }),
        ],
      }),
    );
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(items.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  /** 探针分发 mock(wechat_local.probe;probe = null → 传输层错误形态) */
  function mockProbe(probe: WechatLocalProbeView | null) {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "wechat_local.probe") {
        if (probe === null) {
          throw JSON.stringify({ code: "transport_error", path: "$", message: "探针不可达" });
        }
        return probe;
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
  }

  /** 1 级点微信类型卡 → 2 级渠道列表 */
  async function openWxList() {
    fireEvent.click(await screen.findByTestId("feed-type-card-wx"));
    await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
  }

  /** 1→2→3 下钻微信渠道详情(等作用域查询发出) */
  async function openWxChannel() {
    await openWxList();
    fireEvent.click(await screen.findByTestId("feed-channel-row-weixin-测试会话"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "weixin-测试会话" })),
    );
  }

  it("类型卡第四档(1 级):wx 卡词面「微信」,词表序 tg → wx → site(IM 双档相邻),零条目也出卡(health 声明源)", async () => {
    mockProbe(probePayload());
    // 微信零条目(tech 有条目):声明源即成员,wx 卡照出
    mockWxWorld([fixtureItem({ source: "tech-source", title: "网页新闻" })]);
    await renderOverview();
    // 词表序:类型卡 DOM 顺序 = CHANNEL_CARD_ORDER 过滤有成员档(tg → wx → site;daily 无成员不出)
    const kinds = screen
      .getAllByTestId(/^feed-type-card-/)
      .map((node) => node.getAttribute("data-testid")?.replace("feed-type-card-", ""));
    expect(kinds).toEqual(["tg", "wx", "site"]);
    // 词面「微信」(G7 显示名)+ 渠道数 + 零条目知会词
    const wxCard = screen.getByTestId("feed-type-card-wx");
    expect(wxCard.textContent).toContain("微信");
    expect(wxCard.textContent).toContain("1 个渠道");
    expect(wxCard.textContent).toContain("暂无入库条目");
  });

  it("2 级桥状态区(镜像 TG 账号区结构):wx 页出 probe 单卡(三态词 + 版本行 + 动线钮);TG/site 页零出现;探针失败给重试", async () => {
    mockProbe(probePayload());
    mockWxWorld([]);
    await renderOverview();
    await openWxList();
    const bridge = await screen.findByTestId("feed-wx-bridge-card");
    // 三态词(● 在线 · 微信 4.1.15)+ 版本行(微信/桥组件)
    expect(bridge.textContent).toContain("在线");
    expect(bridge.textContent).toContain("微信 4.1.15");
    expect(bridge.textContent).toContain("桥组件 0.3.1");
    expect(within(bridge).getByTestId("feed-wx-bridge-manage")).toBeTruthy();
    // 区头词面随三态
    expect(screen.getByTestId("feed-wx-bridge-title").textContent).toContain("桥状态 · 在线");

    // 降级态:首因人话 + 原因逐条(码名 + 修复指引,消息屏同款)
    cleanup();
    mockProbe(probePayload({ ok: false, state: "degraded", reasons: [{ code: "wechat_not_running", fix_hint: "打开微信桌面客户端" }] }));
    renderScreen();
    await openWxList();
    const degraded = await screen.findByTestId("feed-wx-bridge-card");
    expect(degraded.textContent).toContain("降级");
    expect(within(degraded).getByTestId("feed-wx-bridge-reasons").textContent).toContain("打开微信桌面客户端");

    // 探针失败:重试 + 跳转并列(TG 账号区 error 分支同门);重试真实重发 probe
    cleanup();
    mockProbe(null);
    renderScreen();
    await openWxList();
    const errorArea = await screen.findByTestId("feed-wx-bridge-error");
    const probeCalls = () =>
      invokeMock.mock.calls.filter(([, args]) => (args as { method?: string })?.method === "wechat_local.probe").length;
    const before = probeCalls();
    fireEvent.click(within(errorArea).getByTestId("feed-wx-bridge-retry"));
    await waitFor(() => expect(probeCalls()).toBeGreaterThan(before));

    // TG 2 级/site 2 级:桥状态区零出现(镜像 TG 账号区仅 tg 页)
    cleanup();
    mockProbe(probePayload());
    renderScreen();
    await openChannelList("tg");
    await screen.findByTestId("feed-tg-accounts");
    expect(screen.queryByTestId("feed-wx-bridge")).toBeNull();
    fireEvent.click(screen.getByTestId("feed-back-to-types"));
    await openChannelList("site");
    await screen.findByTestId("feed-channel-row-tech-source");
    expect(screen.queryByTestId("feed-wx-bridge")).toBeNull();
  });

  it("2 级桥状态区动线钮:「到消息屏处理」真实路由落 /messaging(消息屏微信区,路由已有)", async () => {
    mockProbe(probePayload());
    mockWxWorld([]);
    render(
      <MemoryRouter>
        <LocationProbe />
        <FeedScreen />
      </MemoryRouter>,
    );
    await openWxList();
    fireEvent.click(await screen.findByTestId("feed-wx-bridge-manage"));
    await waitFor(() => expect(screen.getByTestId("location-probe").textContent).toBe("/messaging"));
  });

  it("3 级微信渠道:聊天双栏共用(左栏监控会话 data-im-kind=wx)+ 气泡卡 data-kind=weixin + 泡顶会话名行退役(10-13:一词一源在聊天头);wechat-local:// 锚「打开原文」如实缺席", async () => {
    mockProbe(probePayload());
    const wxItem = fixtureItem({
      source: "weixin-测试会话",
      title: "微信消息甲",
      content: "正文一行",
      url: "wechat-local://chat/%E6%B5%8B%E8%AF%95#wx-abc123def4567890",
    });
    mockWxWorld([wxItem]);
    renderScreen();
    await openWxChannel();
    // 双栏:左栏监控会话(结构 testid feed-tg-group-* 不动,data-im-kind 区分 IM 档;
    // wx 档行 = WxMonitorRow,10-13 B1 起 testid 走 wx-monitor-* 契约词)
    const pane = await screen.findByTestId("feed-tg-group-pane");
    expect(pane.getAttribute("data-im-kind")).toBe("wx");
    expect(within(pane).getByTestId("wx-monitor-row-weixin-测试会话")).toBeTruthy();
    // 气泡卡:data-kind=weixin(五档判定),气泡结构词共用
    const card = await screen.findByTestId(`feed-item-${wxItem.id}`);
    expect(card.getAttribute("data-kind")).toBe("weixin");
    expect(within(card).getByTestId(`feed-tg-bubble-${wxItem.id}`)).toBeTruthy();
    // 泡顶会话名行退役(10-13 气泡重做):群名一词一源只在聊天头
    expect(within(card).queryByText("测试会话")).toBeNull();
    // wechat-local:// 自定义锚不可打开 →「打开原文」如实缺席(有意,§2.3)
    expect(within(card).queryByRole("button", { name: "打开原文" })).toBeNull();
    // 聊天头:wx 专属 testid(feed-wx-chat-header),会话名大字
    expect(screen.getByTestId("feed-wx-chat-header").textContent).toContain("测试会话");
  });

  it("气泡内图片槽(10-16 Phase 2):带 image_files 的 wx 消息泡内出图片区(合成路径);空 image_files 零渲染", async () => {
    mockProbe(probePayload());
    // 合成路径(私有数据红线:测试不碰真实 media-cache 件);invoke 未 mock
    // feed_image_path → SavedImage 走拒授权降级态,槽位结构照常在场
    const withImages = fixtureItem({
      source: "weixin-测试会话",
      title: "微信图片消息",
      content: null,
      url: "wechat-local://chat/x#wx-img001",
      image_files: ["/data/wechat-localdb/media-cache/synthetic-a1b2.jpg"],
    });
    const withoutImages = fixtureItem({
      source: "weixin-测试会话",
      title: "微信纯文字消息",
      content: "无图正文",
      url: "wechat-local://chat/x#wx-txt002",
    });
    mockWxWorld([withImages, withoutImages]);
    renderScreen();
    await openWxChannel();
    // 带图条目:泡内图片槽在场(feed-wx-bubble-image 契约词),列表形态
    // 含张数与路径词面
    const imageCard = await screen.findByTestId(`feed-item-${withImages.id}`);
    const slot = within(imageCard).getByTestId("feed-wx-bubble-image");
    expect(slot.textContent).toContain("图文件 1 张");
    expect(slot.textContent).toContain("/data/wechat-localdb/media-cache/synthetic-a1b2.jpg");
    // 空图条目:槽位整体缺席(空 image_files 不渲染)
    const textCard = screen.getByTestId(`feed-item-${withoutImages.id}`);
    expect(within(textCard).queryByTestId("feed-wx-bubble-image")).toBeNull();
  });

  it("3 级左栏平台隔离(主人令 2026-10-13「微信是微信,TG是TG,不同渠道,要展示不同的群,不能混在一起」):wx 渠道左栏只列 wx 会话,telegram 对照源不混列", async () => {
    mockProbe(probePayload());
    // telegram-seed 为 health 声明源(零条目也成卡)——混列时代它会出现在 wx 左栏
    mockWxWorld([]);
    renderScreen();
    await openWxChannel();
    const pane = await screen.findByTestId("feed-tg-group-pane");
    expect(pane.getAttribute("data-im-kind")).toBe("wx");
    expect(within(pane).getByTestId("wx-monitor-row-weixin-测试会话")).toBeTruthy();
    expect(within(pane).queryByTestId("feed-channel-row-telegram-seed")).toBeNull();
  });

  // ── 10-13-wechat-monitor-ui B 线:3 级 wx 监控台群列表内容化(B1/B2/B3)──

  /** wx 源健康度夹具(evaluate_source_health 形状;按需覆写 latest/skip) */
  function wxHealth(
    overrides: Partial<NonNullable<HealthResult["categories"][number]["sources"][number]["health"]>> = {},
  ) {
    return {
      state: "ok" as const,
      reason: "本轮产出 2 条",
      observed: 3,
      latest: { run_id: 1, run_status: "success", item_count: 2, skip_reason: null, failed: false },
      baseline: null,
      ...overrides,
    };
  }

  /** 双 wx 源世界(源名 = 生产实名 TMS/AI中转站,前缀律 weixin-<群显示名>);
   *  healthOverrides 按源名注入健康度,store.items 按源过滤。 */
  function mockWxMonitorWorld(
    healthOverrides: Record<string, ReturnType<typeof wxHealth>> = {},
    items: FeedItem[] = [],
  ) {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({
            id: "weixin",
            name: "微信监控",
            sources: [
              { ...sourceEntry("weixin-TMS 中转站交流", "wechat_local"), health: wxHealth(healthOverrides["weixin-TMS 中转站交流"]) },
              { ...sourceEntry("weixin-AI中转站-♾️ AI Token", "wechat_local"), health: wxHealth(healthOverrides["weixin-AI中转站-♾️ AI Token"]) },
            ],
          }),
        ],
      }),
    );
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(items.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  /** 双 wx 源世界下钻:2 级点 TMS 行进 3 级(等作用域查询发出) */
  async function openWxMonitorChannel() {
    await openWxList();
    fireEvent.click(await screen.findByTestId("feed-channel-row-weixin-TMS 中转站交流"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(
        expect.objectContaining({ source: "weixin-TMS 中转站交流" }),
      ),
    );
  }

  it("B1 微信群列表按源渲染:health 声明源即成行(源驱动零硬编码群名),状态词=监控中,展示名剥 weixin- 前缀,telegram 不混列", async () => {
    mockProbe(probePayload());
    mockWxMonitorWorld();
    renderScreen();
    await openWxMonitorChannel();
    const pane = await screen.findByTestId("feed-tg-group-pane");
    // 两声明源各一行(wx-monitor-row-<源名全称>);头像 tint 档 = CHANNEL_ROW_AVATAR_TONE.wx
    const tmsRow = within(pane).getByTestId("wx-monitor-row-weixin-TMS 中转站交流");
    const aiRow = within(pane).getByTestId("wx-monitor-row-weixin-AI中转站-♾️ AI Token");
    // 健康度 ok + 无 skip → 状态词「监控中」(域词,B2 映射)
    expect(within(tmsRow).getByTestId("wx-monitor-status-weixin-TMS 中转站交流").textContent).toContain("监控中");
    expect(within(aiRow).getByTestId("wx-monitor-status-weixin-AI中转站-♾️ AI Token").textContent).toContain("监控中");
    // 展示名 = channelDisplayName 剥 weixin- 前缀(群本名)
    expect(tmsRow.textContent).toContain("TMS 中转站交流");
    // 平台隔离延续:telegram 源不混列(此世界未声明,行缺席)
    expect(within(pane).queryByTestId("wx-monitor-row-telegram-seed")).toBeNull();
  });

  it("B2 密钥缺失灰行与跳转:最近 run skip_reason=key_unavailable → 灰行(data-key-missing)+「密钥缺失」+「去获取密钥」跳 /weixin;健康源对照无钮;其余降级走域词「降级」", async () => {
    mockProbe(probePayload());
    mockWxMonitorWorld({
      // 生产语义锚:empty_ok 品类下 key skip 健康度可判 ok,skip 一票定密钥缺失
      "weixin-TMS 中转站交流": wxHealth({
        state: "ok",
        reason: "empty_ok:0 条合法",
        latest: { run_id: 9, run_status: "success", item_count: 0, skip_reason: "key_unavailable", failed: false },
      }),
      "weixin-AI中转站-♾️ AI Token": wxHealth({
        state: "degraded",
        reason: "最新一轮采集失败(未满连续 3 次的死线)",
        latest: { run_id: 8, run_status: "success", item_count: 0, skip_reason: null, failed: true },
      }),
    });
    render(
      <MemoryRouter>
        <LocationProbe />
        <FeedScreen />
      </MemoryRouter>,
    );
    await openWxMonitorChannel();
    const pane = await screen.findByTestId("feed-tg-group-pane");
    // 密钥缺失灰行:标记 + 词 + 动线钮;预览位让给钮
    const tmsRow = within(pane).getByTestId("wx-monitor-row-weixin-TMS 中转站交流");
    expect(tmsRow.getAttribute("data-key-missing")).toBe("true");
    expect(within(tmsRow).getByTestId("wx-monitor-status-weixin-TMS 中转站交流").textContent).toContain("密钥缺失");
    expect(within(tmsRow).getByTestId("wx-monitor-goto-acquire")).toBeTruthy();
    expect(within(tmsRow).queryByTestId("wx-monitor-latest-weixin-TMS 中转站交流")).toBeNull();
    // 降级(非密钥):域词「降级」+ 无密钥钮
    const aiRow = within(pane).getByTestId("wx-monitor-row-weixin-AI中转站-♾️ AI Token");
    expect(aiRow.getAttribute("data-key-missing")).toBe("false");
    expect(within(aiRow).getByTestId("wx-monitor-status-weixin-AI中转站-♾️ AI Token").textContent).toContain("降级");
    expect(within(aiRow).queryByTestId("wx-monitor-goto-acquire")).toBeNull();
    // 跳转:去获取密钥 → /weixin(密钥状态行 = A 线卡内锚,跳屏即止)
    fireEvent.click(within(tmsRow).getByTestId("wx-monitor-goto-acquire"));
    await waitFor(() => expect(screen.getByTestId("location-probe").textContent).toBe("/weixin"));
  });

  it("B1 最新一条预览与相对时间:cardDigest 预览 + 相对时间 time 元素(dateTime 锚);零条目源 = 知会词 + 无时间", async () => {
    mockProbe(probePayload());
    const seen = new Date().toISOString();
    mockWxMonitorWorld(
      {},
      [
        fixtureItem({
          source: "weixin-TMS 中转站交流",
          title: "群消息标题",
          content: "预览正文一行",
          first_seen: seen,
        }),
      ],
    );
    renderScreen();
    await openWxMonitorChannel();
    const pane = await screen.findByTestId("feed-tg-group-pane");
    const tmsRow = within(pane).getByTestId("wx-monitor-row-weixin-TMS 中转站交流");
    // cardDigest 复用:正文(与标题不重复)压平取头
    expect(within(tmsRow).getByTestId("wx-monitor-latest-weixin-TMS 中转站交流").textContent).toContain("预览正文一行");
    // 相对时间:time 元素 + dateTime 锚(ChannelRow 同门;词面 = formatRelativeTime 域词)
    const time = tmsRow.querySelector("time");
    expect(time).toBeTruthy();
    expect(time?.getAttribute("dateTime")).toBe(seen);
    expect(time?.textContent ?? "").toMatch(/^(刚刚|\d+ (分钟|小时|天)前|\d{4}-)/);
    // 零条目源(未入库):知会词 + 无 time 元素
    const aiRow = within(pane).getByTestId("wx-monitor-row-weixin-AI中转站-♾️ AI Token");
    expect(within(aiRow).getByTestId("wx-monitor-latest-weixin-AI中转站-♾️ AI Token").textContent).toContain("暂无入库消息");
    expect(aiRow.querySelector("time")).toBeNull();
  });

  it("B3 去配置跳转链路:右栏底「去配置监控群 →」→ /yaml-editor 深链预选 weixin.yaml(?file=);清单无 weixin.yaml/拉取失败 = 跳屏手选回退", async () => {
    // yaml.list 应答(weixin.yaml 在列;G12 夹具同形)
    const yamlFiles = [
      { file: "/home/config/weixin.yaml", name: "weixin.yaml", parse_ok: true, category_id: "weixin", category_name: "微信监控" },
      { file: "/home/config/ai-news.yaml", name: "ai-news.yaml", parse_ok: true, category_id: "ai-news", category_name: "AI资讯" },
    ];
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "wechat_local.probe") return probePayload();
      if (args?.method === "yaml.list") return { config_dir: "/home/config", files: yamlFiles };
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    mockWxMonitorWorld();
    render(
      <MemoryRouter>
        <FullLocationProbe />
        <FeedScreen />
      </MemoryRouter>,
    );
    await openWxMonitorChannel();
    const pane = await screen.findByTestId("feed-tg-group-pane");
    const gotoConfig = within(pane).getByTestId("wx-monitor-goto-config");
    expect(gotoConfig.textContent).toContain("去配置监控群");
    fireEvent.click(gotoConfig);
    await waitFor(() =>
      expect(screen.getByTestId("location-full-probe").textContent).toBe(
        `/yaml-editor?file=${encodeURIComponent("/home/config/weixin.yaml")}`,
      ),
    );

    // 回退:清单无 weixin.yaml → 跳屏手选(不猜文件名)
    cleanup();
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "wechat_local.probe") return probePayload();
      if (args?.method === "yaml.list") return { config_dir: "/home/config", files: yamlFiles.slice(1) };
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
    render(
      <MemoryRouter>
        <FullLocationProbe />
        <FeedScreen />
      </MemoryRouter>,
    );
    await openWxMonitorChannel();
    fireEvent.click(within(await screen.findByTestId("feed-tg-group-pane")).getByTestId("wx-monitor-goto-config"));
    await waitFor(() => expect(screen.getByTestId("location-full-probe").textContent).toBe("/yaml-editor"));
  });

  it("3 级 wx 监控台三态:ok = ● 桥在线 · 微信版本 + 管理/历史钮(无扫码登录、无原生网页预览、无原生视图段 = 有意缺席);degraded/unavailable 如实", async () => {
    mockProbe(probePayload());
    mockWxWorld([
      fixtureItem({ source: "weixin-测试会话", title: "桥在线时的一条", first_seen: new Date().toISOString() }),
    ]);
    renderScreen();
    await openWxChannel();
    const consoleBar = await screen.findByTestId("feed-wx-console");
    // ok 态:桥在线 + 微信版本
    expect(within(consoleBar).getByTestId("feed-wx-console-live").textContent).toContain("桥在线");
    expect(within(consoleBar).getByTestId("feed-wx-console-live").textContent).toContain("微信 4.1.15");
    // TG 专属件零出现:无扫码登录钮、无原生网页预览钮、无「原生视图」段
    expect(within(consoleBar).queryByTestId("feed-tg-console-login")).toBeNull();
    expect(within(consoleBar).queryByTestId("feed-tg-console-preview")).toBeNull();
    expect(screen.queryByTestId("feed-tg-view-toggle")).toBeNull();
    // 三件套之二:管理 + 看全部历史(openHistory 复用)
    expect(within(consoleBar).getByTestId("feed-wx-console-manage")).toBeTruthy();
    fireEvent.click(within(consoleBar).getByTestId("feed-wx-console-history"));
    expect(await screen.findByTestId("feed-history-exit")).toBeTruthy();
    expect(screen.getByTestId("feed-day-window").textContent).toContain("全部历史");

    // degraded:首因人话(title 留码名结构词)
    cleanup();
    mockProbe(probePayload({ ok: false, state: "degraded", reasons: [{ code: "wechat_not_running", fix_hint: "打开微信桌面客户端" }] }));
    renderScreen();
    await openWxChannel();
    const degradedBar = await screen.findByTestId("feed-wx-console");
    expect(within(degradedBar).getByTestId("feed-wx-console-degraded").textContent).toContain("打开微信桌面客户端");

    // bridge_unavailable:○ 词面 + 首因
    cleanup();
    mockProbe(probePayload({ ok: false, state: "bridge_unavailable", reasons: [{ code: "component_missing", fix_hint: "到设置装 wechat-bridge 组件" }] }));
    renderScreen();
    await openWxChannel();
    const unavailableBar = await screen.findByTestId("feed-wx-console");
    expect(within(unavailableBar).getByTestId("feed-wx-console-unavailable").textContent).toContain("桥不可用");
    expect(within(unavailableBar).getByTestId("feed-wx-console-unavailable").textContent).toContain("到设置装 wechat-bridge 组件");
  });

  it("3 级监控台「管理」钮:真实路由落 /messaging(微信本机工作区在消息屏,非独立屏)", async () => {
    mockProbe(probePayload());
    mockWxWorld([]);
    render(
      <MemoryRouter>
        <LocationProbe />
        <FeedScreen />
      </MemoryRouter>,
    );
    await openWxChannel();
    fireEvent.click(await screen.findByTestId("feed-wx-console-manage"));
    await waitFor(() => expect(screen.getByTestId("location-probe").textContent).toBe("/messaging"));
  });

  it("空态阶梯 wx 分支(probe 三态驱动):桥不可用 → 引导卡指向消息屏引导卡;桥在线 → 「桥在线,暂无未读新消息」(如实披露当前会话语义);探针失败 → 桥状态未知 + 重试", async () => {
    // 桥不可用:主令「unavailable 时引导文案指向消息屏引导卡」
    mockProbe(probePayload({ ok: false, state: "bridge_unavailable", reasons: [{ code: "wechat_not_running", fix_hint: "打开微信桌面客户端" }] }));
    mockWxWorld([fixtureItem({ source: "tech-source", title: "网页新闻" })]);
    renderScreen();
    await openWxChannel();
    const unavailable = await screen.findByTestId("feed-wx-bridge-unavailable");
    expect(unavailable.textContent).toContain("桥不可用");
    expect(within(unavailable).getByRole("button", { name: "到消息屏看引导" })).toBeTruthy();

    // 桥在线:新消息预期词 + 像素链「当前打开会话」语义如实披露
    cleanup();
    mockProbe(probePayload());
    renderScreen();
    await openWxChannel();
    const online = await screen.findByTestId("feed-wx-online");
    expect(online.textContent).toContain("桥在线,暂无未读新消息");
    expect(online.textContent).toContain("当前打开的会话");

    // 探针失败:桥状态未知 + 重试(TG 状态未知卡同门);重试真实重发 probe
    cleanup();
    mockProbe(null);
    renderScreen();
    await openWxChannel();
    const unknown = await screen.findByTestId("feed-wx-status-unknown");
    expect(unknown.textContent).toContain("桥状态未知");
    const probeCalls = () =>
      invokeMock.mock.calls.filter(([, args]) => (args as { method?: string })?.method === "wechat_local.probe").length;
    const before = probeCalls();
    fireEvent.click(within(unknown).getByRole("button", { name: "重试拉取状态" }));
    await waitFor(() => expect(probeCalls()).toBeGreaterThan(before));
  });

  it("搜索别名:1 级搜「微信」/「wx」仅 wx 类型卡直出(CHANNEL_KIND_ALIASES wx 档);清空恢复全量", async () => {
    mockProbe(probePayload());
    mockWxWorld([
      fixtureItem({ source: "telegram-seed", title: "TG 一条" }),
      fixtureItem({ source: "tech-source", title: "网页新闻" }),
    ]);
    await renderOverview();
    const typeSearch = screen.getByLabelText("搜索类型") as HTMLInputElement;
    // 「微信」:主路径(主人搜中文俗名)
    fireEvent.change(typeSearch, { target: { value: "微信" } });
    expect(await screen.findByTestId("feed-type-card-wx")).toBeTruthy();
    await waitFor(() => expect(screen.queryByTestId("feed-type-card-tg")).toBeNull());
    await waitFor(() => expect(screen.queryByTestId("feed-type-card-site")).toBeNull());
    fireEvent.keyDown(typeSearch, { key: "Escape" });
    await screen.findByTestId("feed-type-card-site");
    // 「wx」:缩写别名同认
    fireEvent.change(typeSearch, { target: { value: "wx" } });
    expect(await screen.findByTestId("feed-type-card-wx")).toBeTruthy();
    await waitFor(() => expect(screen.queryByTestId("feed-type-card-site")).toBeNull());
    await waitFor(() => expect(screen.queryByTestId("feed-type-card-tg")).toBeNull());
    fireEvent.keyDown(typeSearch, { key: "Escape" });
  });

  it("进会话即已读(wx 同享 chatView 语义):微信会话选中 → mark_all 带 source 全量已读 + 未读档顺手切「全部」", async () => {
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    markAllMock.mockResolvedValue({ updated: 1 });
    mockProbe(probePayload());
    mockWxWorld([
      fixtureItem({
        source: "weixin-测试会话",
        title: "点进来的未读一条",
        first_seen: new Date(dayWindowStart().getTime() + 5 * 60_000).toISOString(),
      }),
    ]);
    renderScreen();
    await openWxChannel();
    // 源级全量已读(角标口径 = source_stats 全库未读)
    await waitFor(() =>
      expect(markAllMock).toHaveBeenCalledWith({ marker: "read", value: true, source: "weixin-测试会话" }),
    );
    // 未读档被切「全部」:刚读的消息留在时间线(TG 聊天语义同款)
    await waitFor(() => expect(screen.getByText("点进来的未读一条")).toBeTruthy());
  });

  it("wx 档同套泡形(10-13 气泡重做,平台区分只走点缀色):发信人标签同规则拆显,平台图标随发信人行(不整行重复渠道名)", async () => {
    mockProbe(probePayload());
    const wxSenderItem = fixtureItem({
      source: "weixin-测试会话",
      title: "i: wx 消息一条",
      content: null,
      url: "wechat-local://chat/%E6%B5%8B%E8%AF%95#wx-abc123def4567890",
    });
    mockWxWorld([wxSenderItem]);
    renderScreen();
    await openWxChannel();
    const card = await screen.findByTestId(`feed-item-${wxSenderItem.id}`);
    // 同一套拆分与标签(TG/weixin 两档同一泡形,不分叉两套布局)
    expect(within(card).getByText("i")).toBeTruthy();
    expect(within(card).getByRole("button", { name: "wx 消息一条" })).toBeTruthy();
    // 渠道名行退役在 wx 档同样成立(群名只在聊天头)
    expect(within(card).queryByText("测试会话")).toBeNull();
  });
});

describe("feed weixin 档 纯函数(api.ts,10-12-weixin-feed-channel)", () => {
  it("channelKindOf:weixin-/wx- 前缀 → weixin 档(列 TELEGRAM 之后、engine 之前;engine 词表不参与条目档判定)", () => {
    // 前缀规约(源名全称律 weixin-<会话名>)+ wx- 旧缩写同收
    expect(channelKindOf({ source: "weixin-测试会话", category: null })).toBe("weixin");
    expect(channelKindOf({ source: "wx-测试会话", category: null })).toBe("weixin");
    // 前缀优先:engine=wechat_local 不抢判(条目档判定只有前缀,§2.5 A 表)
    expect(
      channelKindOf({ source: "别的源", category: null }, new Map([["别的源", "wechat_local"]])),
    ).toBe("news");
    // telegram 前缀仍最优先
    expect(channelKindOf({ source: "telegram-durov", category: null })).toBe("telegram");
    // 价格键/品类判定不被 weixin 前缀遮蔽以外的路径影响
    expect(channelKindOf({ source: "weixin-x", category: "games" })).toBe("weixin");
  });

  it("channelCardKindOf:weixin-/wx- 前缀 → wx(前缀优先);engine wechat_local → wx;其余照旧 site/daily/tg", () => {
    // 前缀优先(static_html 等任意 engine 不抢判;engine 大小写宽容)
    expect(channelCardKindOf("weixin-测试会话", "static_html")).toBe("wx");
    expect(channelCardKindOf("weixin-测试会话", null)).toBe("wx");
    expect(channelCardKindOf("wx-foo", undefined)).toBe("wx");
    // engine 词表(无前缀命中的源名,engine 补判)
    expect(channelCardKindOf("x", "wechat_local")).toBe("wx");
    expect(channelCardKindOf("x", "WeChat_Local")).toBe("wx");
    // 既有档不受扰:telegram 前缀/daily 词表/其余 site
    expect(channelCardKindOf("telegram-durov", "static_html")).toBe("tg");
    expect(channelCardKindOf("daily-digest", "prompt")).toBe("daily");
    expect(channelCardKindOf("openai-news", "static_html")).toBe("site");
  });

  it("channelDisplayName:剥 weixin-/wx- 协议载体前缀显会话本名(一词一源;前缀后空残余回源名)", () => {
    expect(channelDisplayName("weixin-测试会话")).toBe("测试会话");
    expect(channelDisplayName("wx-测试会话")).toBe("测试会话");
    expect(channelDisplayName("weixin-")).toBe("weixin-"); // 空残余回源名,不猜
    expect(channelDisplayName("telegram-durov")).toBe("durov"); // 既有词表不受扰
    expect(channelDisplayName(null)).toBe("未知来源");
  });

  it("类型卡词表:CHANNEL_CARD_LABELS wx = 「微信」(G7 显示名);CHANNEL_CARD_ORDER = tg → wx → site → daily(IM 双档相邻)", () => {
    expect(CHANNEL_CARD_LABELS.wx).toBe("微信");
    expect(CHANNEL_CARD_LABELS.tg).toBe("TG");
    expect(CHANNEL_CARD_ORDER).toEqual(["tg", "wx", "site", "daily"]);
  });

  it("feedChannelCards/aggregateTypeCards:weixin-<会话> 声明源(wechat_local)出 wx 档卡(零条目也出);归并出「微信」类型卡成员", () => {
    const windowStart = dayWindowStart(new Date(2026, 9, 12, 14, 0));
    const at = (h: number) => new Date(2026, 9, 12, h, 0).toISOString();
    const wxMsg = fixtureItem({ source: "weixin-测试会话", title: "会话一条", first_seen: at(10) });
    const engines = new Map<string, string>([
      ["weixin-测试会话", "wechat_local"],
      ["weixin-另一个会话", "wechat_local"], // 零条目声明源
    ]);
    const cards = feedChannelCards([wxMsg], {}, engines, windowStart, new Date(2026, 9, 12, 14, 0));
    const wxCards = cards.filter((card) => card.kind === "wx");
    expect(wxCards.map((card) => card.key)).toEqual(["weixin-测试会话", "weixin-另一个会话"]);
    expect(wxCards[0].label).toBe("测试会话"); // 前缀剥除
    expect(wxCards[0].today).toBe(1);
    // 零条目渠道也出卡(health 声明源)
    expect(wxCards[1].today).toBe(0);
    expect(wxCards[1].latest).toBeNull();
    // 归并:wx 档出「微信」类型卡,成员 = 2 渠道
    const types = aggregateTypeCards(cards, null);
    const wxType = types.find((type) => type.kind === "wx");
    expect(wxType?.label).toBe("微信");
    expect(wxType?.channels).toBe(2);
    expect(wxType?.today).toBe(1);
    expect(wxType?.previews[0]?.channelLabel).toBe("测试会话");
  });

  it("filterChannelsByQuery/filterTypesByQuery:wx 档别名(「微信」「wx」「wechat」)直出;「w」前缀命中;零命中如实空", () => {
    const cards = feedChannelCards(
      [fixtureItem({ source: "weixin-测试会话" })],
      {},
      new Map([
        ["weixin-测试会话", "wechat_local"],
        ["openai-news", "static_html"],
      ]),
      dayWindowStart(),
    );
    // 「微信」:字面包含碰不到 "weixin-测试会话" 的拼音外词面 —— 别名补上
    expect(filterChannelsByQuery(cards, "微信").map((card) => card.key)).toEqual(["weixin-测试会话"]);
    expect(filterChannelsByQuery(cards, "wx").map((card) => card.key)).toEqual(["weixin-测试会话"]);
    expect(filterChannelsByQuery(cards, "wechat").map((card) => card.key)).toEqual(["weixin-测试会话"]);
    // 别名前缀语义如实:「we」同时命中 wx(weixin/wechat)与 site(web)别名,非 wx 独占
    expect(filterChannelsByQuery(cards, "we").map((card) => card.key)).toEqual(["weixin-测试会话", "openai-news"]);
    // 既有档不受扰 + 零命中
    expect(filterChannelsByQuery(cards, "Tg").map((card) => card.key)).toEqual([]);
    expect(filterChannelsByQuery(cards, "不存在的渠道")).toEqual([]);
    // 类型级(filterTypesByQuery 同门)
    const types = aggregateTypeCards(cards, null);
    expect(filterTypesByQuery(types, "微信").map((type) => type.kind)).toEqual(["wx"]);
    expect(filterTypesByQuery(types, "wx").map((type) => type.kind)).toEqual(["wx"]);
  });
});

// ---------------------------------------------------------------------------
// 气泡重做批(10-13,主人令「这个布局不好看,你给我搞的好看一点」:
// 泡顶渠道名行退役 / 发信人词面拆分标签 / 连续同发信人合并 / 时间线列宽锚)
// ---------------------------------------------------------------------------

describe("FeedScreen · 气泡重做(10-13 气泡布局好看一点)", () => {
  /** chatSenderOf 守卫单测(词表层,api.ts;数据层不动) */
  it("chatSenderOf:「YkC: 消息」拆人名与正文;守卫从紧 —— 纯数字时间/URL scheme/冒号后空不拆;无前缀原样 null", () => {
    // 常规拆分(实况词形:i: / YkC: / 中文名)
    expect(chatSenderOf("YkC: 今天更新了")).toEqual({ sender: "YkC", body: "今天更新了" });
    expect(chatSenderOf("i: 收到")).toEqual({ sender: "i", body: "收到" });
    expect(chatSenderOf("张三: 你好")).toEqual({ sender: "张三", body: "你好" });
    // 冒号后换行(发信人独占一行的实况形态)也拆
    expect(chatSenderOf("YkC:\n第二条消息")).toEqual({ sender: "YkC", body: "第二条消息" });
    // 守卫:纯数字(时间 10:30 开会)/纯符号不是人
    expect(chatSenderOf("10:30 开会")).toBeNull();
    expect(chatSenderOf("::: x")).toBeNull();
    // 守卫:URL scheme 词与链接尾巴(https://…)不拆
    expect(chatSenderOf("https://example.com/a")).toBeNull();
    expect(chatSenderOf("wechat-local://chat/x#wx-1")).toBeNull();
    // 守卫:冒号后空 = 不猜
    expect(chatSenderOf("YkC:")).toBeNull();
    expect(chatSenderOf("YkC: ")).toBeNull();
    // 无前缀(标题无冒号)= null,原样直出
    expect(chatSenderOf("🎉 Clash Party v2 发布")).toBeNull();
  });

  it("发信人标签:泡内上方小型标签显拆出的人名,正文剥「发信人: 」前缀直出(词面归位,数据层不动)", async () => {
    const chatItems = [
      fixtureItem({ source: "telegram-durov", title: "YkC: 新版本已经推流", content: "YkC: 新版本已经推流\n变更点见频道公告" }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(chatItems.filter((item) => !params?.source || item.source === params.source)),
      ),
    );
    await renderChannelDetail("telegram-durov");
    const card = await screen.findByTestId("feed-item-1");
    // 泡内发信人标签在("YkC" 词面在场)
    expect(within(card).getByText("YkC")).toBeTruthy();
    // 正文剥前缀:标题按钮名 = 前缀后的正文,「YkC: 新版本已经推流」整词直出不复现
    expect(within(card).queryByRole("button", { name: "YkC: 新版本已经推流" })).toBeNull();
    expect(within(card).getByRole("button", { name: "新版本已经推流" })).toBeTruthy();
    // 无前缀消息:零发信人标签(不硬造)
    cleanup();
    const plainItems = [fixtureItem({ source: "telegram-durov", title: "普通消息无前缀" })];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(plainItems.filter((item) => !params?.source || item.source === params.source)),
      ),
    );
    await renderChannelDetail("telegram-durov");
    const plainCard = await screen.findByTestId(`feed-item-${plainItems[0].id}`);
    expect(within(plainCard).queryByText("YkC")).toBeNull();
    expect(within(plainCard).getByRole("button", { name: "普通消息无前缀" })).toBeTruthy();
  });

  it("连续同发信人合并成组(TG 同款):组内首条显发信人标签,后续条省略;换发信人重显;组尾才有尾角 rounded-bl-md", async () => {
    const chatItems = [
      fixtureItem({ source: "telegram-durov", title: "i: 第一条", first_seen: new Date(Date.now() - 30_000).toISOString() }),
      fixtureItem({ source: "telegram-durov", title: "i: 第二条", first_seen: new Date(Date.now() - 20_000).toISOString() }),
      fixtureItem({ source: "telegram-durov", title: "YkC: 第三条换人了", first_seen: new Date(Date.now() - 10_000).toISOString() }),
    ];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(chatItems.filter((item) => !params?.source || item.source === params.source)),
      ),
    );
    await renderChannelDetail("telegram-durov");
    const card1 = await screen.findByTestId("feed-item-1");
    const card2 = await screen.findByTestId("feed-item-2");
    const card3 = await screen.findByTestId("feed-item-3");
    // 组首(i 第一条)显发信人;组内后续(第二条)省略
    expect(within(card1).getByText("i")).toBeTruthy();
    expect(within(card2).queryByText("i")).toBeNull();
    // 换发信人重显
    expect(within(card3).getByText("YkC")).toBeTruthy();
    // 组尾不对称尾角:每组的最后一条有 rounded-bl-md,组内后续条全 2xl 无尾角
    expect(within(card2).getByTestId("feed-tg-bubble-2").className).toContain("rounded-bl-md");
    expect(within(card1).getByTestId("feed-tg-bubble-1").className).not.toContain("rounded-bl-md");
  });

  it("时间线列宽锚定:聊天时间线居中舒适列(max-w-[760px] mx-auto),卡根带 min-w 保底 + max-w 72% 封顶(右缘不再乱缩)", async () => {
    const chatItems = [fixtureItem({ source: "telegram-durov", title: "短消息" })];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(
        result(chatItems.filter((item) => !params?.source || item.source === params.source)),
      ),
    );
    await renderChannelDetail("telegram-durov");
    const timeline = await screen.findByTestId("feed-chat-timeline");
    expect(timeline.className).toContain("max-w-[760px]");
    expect(timeline.className).toContain("mx-auto");
    const card = await screen.findByTestId("feed-item-1");
    expect(card.className).toContain("min-w-[13rem]");
    expect(card.className).toContain("max-w-[min(100%,72%)]");
  });
});

// ---------------------------------------------------------------------------
// 群信息面板动线(10-13-wechat-groupinfo R2):微信群行右键 →「群信息」→
// 详情弹窗(真拉壳侧 wechat_group_info;契约 = 任务档 prd「group-info 应答
// 契约 v1」,载荷按钉死形状夹具)。面板本体细则(wx-groupinfo-*)在
// wx-groupinfo-panel.test.tsx 穷尽,此处只验挂点动线与行/弹窗联动。
// ---------------------------------------------------------------------------

describe("FeedScreen · 群信息面板动线(10-13-wechat-groupinfo R2)", () => {
  /** wechat_group_info 夹具(prd 契约 v1 全量形状;双成员含群主标记) */
  const groupInfoPayload = {
    chat_id: "50438708676@chatroom",
    display_name: "测试会话",
    member_count: 2,
    owner: { username: "wxid_owner", display: "老王" },
    announcement: { text: "本群仅供技术交流。", editor_display: null, published_at: null },
    status: null,
    members: [
      { username: "wxid_owner", display: "老王", remark: null, is_owner: true },
      { username: "wxid_a", display: "花开相随", remark: null, is_owner: false },
    ],
  };

  /** 微信世界(单 wx 源)+ invoke 按命令名/method 双通道分发(探针走
   *  sidecar_request 载荷 method,群信息走壳侧裸命令) */
  function mockWxChannelWorld() {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "weixin", name: "微信监控", sources: [sourceEntry("weixin-测试会话", "wechat_local")] }),
        ],
      }),
    );
    storeItemsMock.mockImplementation(() => Promise.resolve(result([])));
    invokeMock.mockImplementation(async (command: string, args?: { method?: string }) => {
      if (command === "wechat_group_info") return groupInfoPayload;
      if (args?.method === "wechat_local.probe") {
        return {
          ok: true,
          state: "ok",
          checks: { bridge_component: "ok", wechat_process: "ok", screen_recording: "ok" },
          wechat_version: "4.1.15",
          bridge_version: "0.3.1",
          reasons: [],
        };
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method ?? command}` });
    });
  }

  it("右键微信群行 →「群信息」→ 详情弹窗:群名/群主 wxid 灰字/群主标记/成员 N 人上屏,寻址键剥前缀,导出留位禁用", async () => {
    mockWxChannelWorld();
    await renderOverview();
    // 1→2→3 下钻(3 级左栏才有 WxMonitorRow 家族)
    fireEvent.click(await screen.findByTestId("feed-type-card-wx"));
    await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
    fireEvent.click(screen.getByTestId("feed-channel-row-weixin-测试会话"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "weixin-测试会话" })),
    );
    // 右键群行 → 应用内菜单「群信息」(portal 出屏,screen 全局可达)
    fireEvent.contextMenu(screen.getByTestId("wx-monitor-row-weixin-测试会话"));
    fireEvent.click(await screen.findByRole("menuitem", { name: "群信息" }));
    // 弹窗渲染(契约钉死字段逐项上屏)
    expect(await screen.findByTestId("wx-groupinfo-dialog")).toBeTruthy();
    expect(screen.getByTestId("wx-groupinfo-name").textContent).toBe("测试会话");
    expect(screen.getByTestId("wx-groupinfo-owner").textContent).toContain("老王");
    expect(screen.getByTestId("wx-groupinfo-member-count").textContent).toBe("成员 2 人");
    const members = screen.getByTestId("wx-groupinfo-members");
    expect(within(members).getByTestId("wx-groupinfo-member-wxid_owner").textContent).toContain("群主");
    expect(within(members).getByTestId("wx-groupinfo-member-wxid_a").textContent).toContain("花开相随");
    // 导出钮(R3 态机随迁:面板侧 idle 可点,导出中才禁用;词面「导出」)
    const exportButton = screen.getByTestId("wx-groupinfo-export") as HTMLButtonElement;
    expect(exportButton.disabled).toBe(false);
    expect(exportButton.getAttribute("title")).toBe("导出");
    // 寻址键:源名剥 weixin- 前缀(名→id 解析在壳侧命令内,api 模块头注「寻址」节)
    expect(invokeMock).toHaveBeenCalledWith("wechat_group_info", { chat: "测试会话" });
  });

  it("弹窗开着 Esc 只关弹窗不回退层级(浮层让位收口判例)", async () => {
    mockWxChannelWorld();
    await renderOverview();
    fireEvent.click(await screen.findByTestId("feed-type-card-wx"));
    await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
    fireEvent.click(screen.getByTestId("feed-channel-row-weixin-测试会话"));
    await waitFor(() =>
      expect(storeItemsMock).toHaveBeenLastCalledWith(expect.objectContaining({ source: "weixin-测试会话" })),
    );
    fireEvent.contextMenu(screen.getByTestId("wx-monitor-row-weixin-测试会话"));
    fireEvent.click(await screen.findByRole("menuitem", { name: "群信息" }));
    await screen.findByTestId("wx-groupinfo-dialog");
    fireEvent.keyDown(screen.getByRole("dialog"), { key: "Escape" });
    await waitFor(() => expect(screen.queryByTestId("wx-groupinfo-dialog")).toBeNull());
    // 弹窗关闭后仍停在 3 级(聊天头在场 = 未回退层级)
    expect(screen.getByTestId("feed-wx-chat-header")).toBeTruthy();
  });

  it("聊天头群信息入口(R2「从群行/聊天头进」的聊天头一半):群名旁小钮 → 同款弹窗真拉数据,寻址键剥前缀", async () => {
    mockWxChannelWorld();
    await renderOverview();
    fireEvent.click(await screen.findByTestId("feed-type-card-wx"));
    await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
    fireEvent.click(screen.getByTestId("feed-channel-row-weixin-测试会话"));
    // wx 聊天头:群名旁「群信息」入口在场(词面人话,title 指明看什么)
    const headerButton = await screen.findByTestId("feed-wx-chat-header-groupinfo");
    expect(headerButton.textContent).toContain("群信息");
    expect(headerButton.getAttribute("title")).toContain("群公告");
    fireEvent.click(headerButton);
    // 同款弹窗动线:契约字段上屏 + 寻址键剥前缀传壳侧
    expect(await screen.findByTestId("wx-groupinfo-dialog")).toBeTruthy();
    expect(screen.getByTestId("wx-groupinfo-member-count").textContent).toBe("成员 2 人");
    expect(invokeMock).toHaveBeenCalledWith("wechat_group_info", { chat: "测试会话" });
  });
});

// ---------------------------------------------------------------------------
// 朋友圈合流批(10-13-wechat-sns-merge,主人令「朋友圈与朋友圈互动放到
// 一起,不要分开;要表明朋友圈是谁发的,不能光有信息没有发表人」):
// 双源合单行(2 级 + 左栏)/ 右栏双源混排 / 动态发帖人必显(raw.nickname
// 协议白名单投影,缺失回落「微信好友」)/ 互动通知轻量行内态
// ---------------------------------------------------------------------------

describe("FeedScreen · 朋友圈合流(10-13-wechat-sns-merge)", () => {
  /** 双 sns 源世界(health 声明朋友圈动态/互动两源 + store.items 按源过滤) */
  function mockSnsWorld(items: FeedItem[] = []) {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({
            id: "weixin",
            name: "微信监控",
            sources: [sourceEntry("weixin-朋友圈", "wechat_local"), sourceEntry("weixin-朋友圈互动", "wechat_local")],
          }),
        ],
      }),
    );
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(items.filter((item) => !params?.source || item.source === params.source))),
    );
  }

  /** sns 探针 ok(wechat_local.probe;进 wx 渠道即拉) */
  function mockSnsProbe() {
    invokeMock.mockImplementation(async (_command: string, args?: { method?: string }) => {
      if (args?.method === "wechat_local.probe") {
        return {
          ok: true, state: "ok", checks: {}, wechat_version: "4.0.3", bridge_version: "1.0", reasons: [],
        };
      }
      throw JSON.stringify({ code: "method_not_found", path: "$", message: `未 mock:${args?.method}` });
    });
  }

  async function openSnsChannel() {
    fireEvent.click(await screen.findByTestId("feed-type-card-wx"));
    await waitFor(() => expect(screen.getByTestId("feed-channel-list")).toBeTruthy());
    fireEvent.click(screen.getByTestId("feed-channel-row-weixin-朋友圈"));
    // 双源并列取数:两调用齐落地即达(并行双发,先后不保证,不押 last call)
    await waitFor(() => {
      expect(storeItemsMock).toHaveBeenCalledWith(expect.objectContaining({ source: "weixin-朋友圈" }));
      expect(storeItemsMock).toHaveBeenCalledWith(expect.objectContaining({ source: "weixin-朋友圈互动" }));
    });
  }

  it("AC1 合流:2 级与左栏单行「朋友圈」(互动源不单列),右栏双源并列取数且时间线按 first_seen 混排", async () => {
    mockSnsProbe();
    const noticeOld = fixtureItem({
      source: "weixin-朋友圈互动", title: "猫三三 赞了朋友圈动态",
      first_seen: new Date(Date.now() - 30 * 60_000).toISOString(), content: null,
      url: "wechat-local://sns/notice/9#wxsnsn-9",
    });
    const moment = fixtureItem({
      source: "weixin-朋友圈", title: "周末爬山", nickname: "猫三三",
      first_seen: new Date(Date.now() - 10 * 60_000).toISOString(), content: "周末爬山",
      url: "wechat-local://sns/f1#wxsns-f1",
    });
    const noticeNew = fixtureItem({
      source: "weixin-朋友圈互动", title: "阿四 评论了朋友圈动态:带我一个",
      first_seen: new Date(Date.now() - 2 * 60_000).toISOString(), content: null,
      url: "wechat-local://sns/notice/10#wxsnsn-10",
    });
    mockSnsWorld([noticeOld, moment, noticeNew]);
    renderScreen();
    await openSnsChannel();
    // 双源并列取数(source 精确等值,无 IN 查询;如实选择:双发前端混排)
    expect(storeItemsMock).toHaveBeenCalledWith(expect.objectContaining({ source: "weixin-朋友圈" }));
    expect(storeItemsMock).toHaveBeenCalledWith(expect.objectContaining({ source: "weixin-朋友圈互动" }));
    // 时间线混排(first_seen 新→旧):互动新帖在最前,动态居中,互动旧帖垫底
    const timeline = await screen.findByTestId("feed-chat-timeline");
    const domOrder = [...timeline.querySelectorAll("[data-item-key]")].map(
      (node) => node.getAttribute("data-testid") ?? "",
    );
    expect(domOrder).toEqual([
      `feed-item-${noticeNew.id}`,
      `feed-item-${moment.id}`,
      `feed-item-${noticeOld.id}`,
    ]);
    // 左栏合流单行:朋友圈行在场,互动源不单列
    const pane = await screen.findByTestId("feed-tg-group-pane");
    expect(within(pane).getByTestId("wx-monitor-row-weixin-朋友圈")).toBeTruthy();
    expect(within(pane).queryByTestId("wx-monitor-row-weixin-朋友圈互动")).toBeNull();
    // 2 级渠道列表同单行(回 2 级验)
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    expect(await screen.findByTestId("feed-channel-row-weixin-朋友圈")).toBeTruthy();
    expect(screen.queryByTestId("feed-channel-row-weixin-朋友圈互动")).toBeNull();
  });

  it("AC2 发帖人必显:动态泡发帖人小签 = raw.nickname 投影,同人合并组内首条显;缺失回落「微信好友」不猜", async () => {
    mockSnsProbe();
    const moments = [
      fixtureItem({ source: "weixin-朋友圈", title: "今天打卡第三天", nickname: "猫三三",
        first_seen: new Date(Date.now() - 30 * 60_000).toISOString(), content: "今天打卡第三天" }),
      fixtureItem({ source: "weixin-朋友圈", title: "配图是公园门口", nickname: "猫三三",
        first_seen: new Date(Date.now() - 29 * 60_000).toISOString(), content: "配图是公园门口" }),
      fixtureItem({ source: "weixin-朋友圈", title: "无 nickname 的动态", nickname: undefined,
        first_seen: new Date(Date.now() - 20 * 60_000).toISOString(), content: null }),
    ];
    mockSnsWorld(moments);
    renderScreen();
    await openSnsChannel();
    // 展示序 = first_seen 新→旧:m3(无 nickname)> m2 > m1;同人组 {m2,m1}
    // 的组首是较新的 m2(时间线顶部第一条),m1 为组内延续条
    const card1 = await screen.findByTestId(`feed-item-${moments[0].id}`);
    const card2 = await screen.findByTestId(`feed-item-${moments[1].id}`);
    const card3 = await screen.findByTestId(`feed-item-${moments[2].id}`);
    // 组首显发帖人;同人后续条省略(合并机制对朋友圈动态同样生效)
    expect(within(card2).getByText("猫三三")).toBeTruthy();
    expect(within(card1).queryByText("猫三三")).toBeNull();
    // raw 缺失 = 词面回落「微信好友」,不猜真名
    expect(within(card3).getByText("微信好友")).toBeTruthy();
    // 正文原样(title 不做发信人前缀剥除,归属以 nickname 为准)
    expect(within(card1).getByRole("button", { name: "今天打卡第三天" })).toBeTruthy();
  });

  it("AC3 互动通知轻量行内态:无泡箱小字行 + 时间随行;点击仍开详情弹窗(feed-item-/data-* 语义保留)", async () => {
    mockSnsProbe();
    const notice = fixtureItem({
      source: "weixin-朋友圈互动", title: "猫三三 赞了朋友圈动态",
      first_seen: new Date(Date.now() - 5 * 60_000).toISOString(), content: null,
      url: "wechat-local://sns/notice/9#wxsnsn-9",
    });
    mockSnsWorld([notice]);
    renderScreen();
    await openSnsChannel();
    const card = await screen.findByTestId(`feed-item-${notice.id}`);
    expect(card.getAttribute("data-kind")).toBe("weixin");
    // 词面保持(who 已在 title);无泡箱(非气泡不冒充 feed-tg-bubble-*)
    expect(within(card).getByText("猫三三 赞了朋友圈动态")).toBeTruthy();
    expect(within(card).queryByTestId(`feed-tg-bubble-${notice.id}`)).toBeNull();
    // 点击语义保留:开详情弹窗
    fireEvent.click(within(card).getByRole("button", { name: "猫三三 赞了朋友圈动态" }));
    expect(screen.getByTestId("feed-detail-dialog")).toBeTruthy();
    await closeDetailDialog();
  });

  it("纯函数:snsStreamSources 双源展开(任一 sns 源都给合流,非 sns 原样);snsMomentAuthor 词面守卫;foldSnsMomentCards 求和取新折叠", () => {
    // 取数源集
    expect(snsStreamSources("weixin-朋友圈")).toEqual(["weixin-朋友圈", "weixin-朋友圈互动"]);
    expect(snsStreamSources("weixin-朋友圈互动")).toEqual(["weixin-朋友圈", "weixin-朋友圈互动"]);
    expect(snsStreamSources("weixin-测试会话")).toEqual(["weixin-测试会话"]);
    expect(snsStreamSources(null)).toEqual([]);
    // 发帖人词面守卫(缺失/空白/异型 = null 回落,不猜)
    expect(snsMomentAuthor({ source: "weixin-朋友圈", nickname: "猫三三" } as FeedItem)).toBe("猫三三");
    expect(snsMomentAuthor({ source: "weixin-朋友圈", nickname: "   " } as FeedItem)).toBeNull();
    expect(snsMomentAuthor({ source: "weixin-朋友圈", nickname: undefined } as FeedItem)).toBeNull();
    expect(snsMomentAuthor({ source: "weixin-测试会话", nickname: "猫三三" } as FeedItem)).toBeNull();
    // 卡折叠:计数求和、latest/statsLatest 取较新一侧、互动卡退场、主源守位
    const momentCard = { key: "weixin-朋友圈", label: "朋友圈", kind: "wx" as const, today: 2, unread: 1, latest: null, statsLatestSeen: "2026-10-13T10:00:00Z" };
    const noticeCard = { key: "weixin-朋友圈互动", label: "朋友圈互动", kind: "wx" as const, today: 3, unread: 2, latest: null, statsLatestSeen: "2026-10-13T12:00:00Z" };
    const otherCard = { key: "weixin-测试会话", label: "测试会话", kind: "wx" as const, today: 1, unread: 0, latest: null };
    const folded = foldSnsMomentCards([momentCard, noticeCard, otherCard]);
    expect(folded.map((card) => card.key)).toEqual(["weixin-朋友圈", "weixin-测试会话"]);
    expect(folded[0].today).toBe(5);
    expect(folded[0].unread).toBe(3);
    expect(folded[0].statsLatestSeen).toBe("2026-10-13T12:00:00Z");
    // 无 sns 卡世界 = 原样返回(既有渠道零扰动)
    expect(foldSnsMomentCards([otherCard])).toEqual([otherCard]);
  });
});

// ---------------------------------------------------------------------------
// 聊天工作台追加批(10-13 同域追加七件):①左栏会话搜索 / ②新消息到达
// 锚定+回到最新浮钮 / ③未读分割线 / ④顶栏等高 / ⑤会话字母头像 / ⑥时间
// 三档词面(chatTimeOf 纯函数 + 泡面接线随迁断言)/ ⑦极窄窗口左栏折叠
// ---------------------------------------------------------------------------

describe("FeedScreen · 聊天工作台追加批(10-13 同域追加七件)", () => {
  /** 双 TG 群世界(clashv8/alpha;health 声明源即成行,items 提槽可换答,
   *  与 tg-chat-two-pane mockTwoPaneWorld 同门但可变应答) */
  function mockGroupsWorld(initial: FeedItem[] = []) {
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({
            id: "telegram",
            name: "Telegram 监控",
            sources: [sourceEntry("telegram-clashv8", "tg_web"), sourceEntry("telegram-alpha", "tg_web")],
          }),
        ],
      }),
    );
    const items = [...initial];
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(items.filter((item) => !params?.source || item.source === params.source))),
    );
    return items;
  }

  /** 下钻入口:1 级 TG 类型卡 → 2 级行 → 3 级(群列表默认选中该渠道)。 */
  async function openTgGroup(key: string) {
    fireEvent.click(await screen.findByTestId("feed-type-card-tg"));
    fireEvent.click(await screen.findByTestId(`feed-channel-row-${key}`));
  }

  it("① 左栏会话搜索:即输即滤纯客户端过滤(零服务端查询,与右栏 streamQuery 通路互不相干),零命中一行空态,Esc 清词恢复", async () => {
    mockGroupsWorld();
    renderScreen();
    await openTgGroup("telegram-clashv8");
    const pane = await screen.findByTestId("feed-tg-group-pane");
    const search = within(pane).getByTestId("feed-tg-group-search");
    expect(within(pane).getByTestId("feed-channel-row-telegram-clashv8")).toBeTruthy();
    expect(within(pane).getByTestId("feed-channel-row-telegram-alpha")).toBeTruthy();

    // 输入即滤(不防抖等待):alpha 命中,clashv8 行离场
    fireEvent.change(search, { target: { value: "alpha" } });
    expect(within(pane).getByTestId("feed-channel-row-telegram-alpha")).toBeTruthy();
    expect(within(pane).queryByTestId("feed-channel-row-telegram-clashv8")).toBeNull();
    // 零命中:一行空态(testid feed-tg-group-search-empty)
    fireEvent.change(search, { target: { value: "zzz" } });
    const empty = screen.getByTestId("feed-tg-group-search-empty");
    expect(empty.textContent).toContain("没有匹配的会话");
    expect(empty.textContent).toContain("zzz");
    // 客户端过滤零服务端查询:storeItems 全部调用不带 query(检索词不进
    // 数据域 —— 右栏 streamQuery 才是服务端全文检索,两域互不相干)
    for (const call of storeItemsMock.mock.calls) {
      expect((call[0] as StoreItemsParams | undefined)?.query ?? null).toBeNull();
    }
    // Esc 清词(三级搜索框同门框守卫):全量恢复
    fireEvent.keyDown(search, { key: "Escape" });
    expect(within(pane).getByTestId("feed-channel-row-telegram-clashv8")).toBeTruthy();
    expect(screen.queryByTestId("feed-tg-group-search-empty")).toBeNull();
  });

  it("⑤ 会话字母头像:左栏行 = key-hash 色底(内联 style)+ 会话名首字母 + 平台角标;2 级渠道行保持类型图标不换", async () => {
    mockGroupsWorld();
    renderScreen();
    await openTgGroup("telegram-clashv8");
    const pane = await screen.findByTestId("feed-tg-group-pane");
    const row = within(pane).getByTestId("feed-channel-row-telegram-clashv8");
    // 头像位:首字母(clashv8 → C)+ 8 色轮转色底(内联 style = chatSenderTone
    // 同体系,非类型档色)+ 角标 svg(平台 icon 缩角标)
    const avatar = row.querySelector("span[style]");
    expect(avatar).not.toBeNull();
    expect(avatar?.textContent).toContain("C");
    expect((avatar as HTMLElement).style.backgroundColor).not.toBe("");
    expect(avatar?.querySelector("svg")).not.toBeNull();
    // 2 级渠道行不换(类型导航语境保留类型图标 chip,无内联色)
    fireEvent.click(screen.getByTestId("feed-back-to-channels"));
    const l2row = await screen.findByTestId("feed-channel-row-telegram-clashv8");
    expect(l2row.querySelector("span[style]")).toBeNull();
  });

  it("④⑦ 顶栏等高与极窄折叠:左栏区头与聊天头同 min-h-11 + py-2.5(border-b 连线);左栏 aside hidden lg:flex(lg 起显示,右栏 flex-1 自适应)", async () => {
    mockGroupsWorld();
    renderScreen();
    await openTgGroup("telegram-clashv8");
    const pane = await screen.findByTestId("feed-tg-group-pane");
    // ⑦:lg 以下隐藏(lg:flex 起显示)
    expect(pane.className).toContain("hidden");
    expect(pane.className).toContain("lg:flex");
    // ④:两栏顶栏同档(min-h-11 + py-2.5)
    const paneHeader = pane.querySelector("div");
    const chatHeader = await screen.findByTestId("feed-tg-chat-header");
    for (const bar of [paneHeader, chatHeader]) {
      expect(bar?.className).toContain("min-h-11");
      expect(bar?.className).toContain("py-2.5");
    }
  });

  it("② 新消息到达锚定:贴最新端(≤80px)新条目头部到达自动回顶;中段翻阅不打扰;「回到最新」浮钮一键回位", async () => {
    let emitEvent: ((event: { type: string }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string }) => void;
      return Promise.resolve(() => {});
    });
    const anchor = dayWindowStart().getTime();
    const items = mockGroupsWorld([
      fixtureItem({ source: "telegram-clashv8", title: "旧行", first_seen: new Date(anchor + 60_000).toISOString() }),
    ]);
    renderScreen();
    await openTgGroup("telegram-clashv8");
    await screen.findByText("旧行");
    const scroll = screen.getByTestId("feed-chat-scroll");

    // 中段翻阅(scrollTop=300 > 阈值):新条目头部到达不锚(scrollTop 不动)
    scroll.scrollTop = 300;
    fireEvent.scroll(scroll);
    items.unshift(
      fixtureItem({ source: "telegram-clashv8", title: "新到甲", first_seen: new Date(anchor + 120_000).toISOString() }),
    );
    await act(async () => {
      await emitEvent?.({ type: "completed" });
    });
    await screen.findByText("新到甲");
    expect(scroll.scrollTop).toBe(300);
    // 翻阅态出「回到最新」浮钮,一键回顶后浮钮退场
    fireEvent.click(await screen.findByTestId("feed-chat-back-to-latest"));
    expect(scroll.scrollTop).toBe(0);
    expect(screen.queryByTestId("feed-chat-back-to-latest")).toBeNull();

    // 贴最新端(scrollTop=50 ≤ 80 阈值):再进新条目 → 锚定回顶(50 → 0)
    scroll.scrollTop = 50;
    fireEvent.scroll(scroll);
    items.unshift(
      fixtureItem({ source: "telegram-clashv8", title: "新到乙", first_seen: new Date(anchor + 180_000).toISOString() }),
    );
    await act(async () => {
      await emitEvent?.({ type: "completed" });
    });
    await screen.findByText("新到乙");
    expect(scroll.scrollTop).toBe(0);
  });

  it("③ 未读分割线:最早一条未读(最底未读)与更早已读之间画「未读」细线;全部已读不画;未读块到列表末尾不画", async () => {
    // 服务端读态通路(读态源 = items.read 投影,statesFromItems);catalog 域
    // 给空答 —— 进会话自动已读只翻 catalog 副本,不冲掉 stream 侧 read 字段
    versionMock.mockResolvedValue(versionResult(READ_STATE_PROTOCOL));
    markAllMock.mockResolvedValue({ updated: 4 });
    healthMock.mockResolvedValue(
      healthResult({
        categories: [
          categoryEntry({ id: "telegram", name: "Telegram 监控", sources: [sourceEntry("telegram-clashv8", "tg_web")] }),
        ],
      }),
    );
    const anchor = dayWindowStart().getTime();
    const at = (minute: number) => new Date(anchor + minute * 60_000).toISOString();
    const u2 = fixtureItem({ source: "telegram-clashv8", title: "未读新", first_seen: at(4) });
    const u1 = fixtureItem({ source: "telegram-clashv8", title: "未读早", first_seen: at(3) });
    const r1 = fixtureItem({ source: "telegram-clashv8", title: "已读近", first_seen: at(2), read: true });
    const r2 = fixtureItem({ source: "telegram-clashv8", title: "已读远", first_seen: at(1), read: true });
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(params?.source ? [u2, u1, r1, r2] : [])),
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");
    await screen.findByText("未读早");
    // 分割线上邻 = 最早一条未读(u1,新→旧序中最底未读),下邻 = 更早已读(r1)
    const divider = screen.getByTestId("feed-chat-unread-divider");
    expect(divider.previousElementSibling?.getAttribute("data-testid")).toBe(`feed-item-${u1.id}`);
    expect(divider.nextElementSibling?.getAttribute("data-testid")).toBe(`feed-item-${r1.id}`);
    expect(divider.textContent).toContain("未读");

    // 全部已读:分割线退场(全部已读不画)
    cleanup();
    const readAll = [u2, u1, r1, r2].map((item) => ({ ...item, read: true }));
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(params?.source ? readAll : [])),
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");
    await screen.findByText("未读早");
    expect(screen.queryByTestId("feed-chat-unread-divider")).toBeNull();

    // 未读块到列表末尾(全部未读):无已读可分界,悬空线不画
    cleanup();
    const noneRead = [u2, u1, r1, r2].map((item) => ({ ...item, read: undefined }));
    storeItemsMock.mockImplementation((params?: StoreItemsParams) =>
      Promise.resolve(result(params?.source ? noneRead : [])),
    );
    renderScreen();
    await openTgGroup("telegram-clashv8");
    await screen.findByText("未读早");
    expect(screen.queryByTestId("feed-chat-unread-divider")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// chatTimeOf 纯函数(追加批⑥):聊天语境三档时间词面,now 注入可测
// ---------------------------------------------------------------------------

describe("chatTimeOf(追加批⑥,纯函数)", () => {
  it("三档词面:今天 HH:mm / 昨天 HH:mm / M月D日;跨日边界与当日窗同锚(03:00,与时间分组同门);缺失/异形回落", () => {
    const now = new Date(2026, 9, 13, 10, 0); // 2026-10-13 10:00(窗锚后)
    expect(chatTimeOf(new Date(2026, 9, 13, 9, 5).toISOString(), now)).toBe("今天 09:05");
    // 03:00 窗锚语义:当日 00:00 属上一窗(与时间分组「昨天(上一窗口)」
    // 同门 —— 组头/泡面同锚,同屏不打架)
    expect(chatTimeOf(new Date(2026, 9, 13, 0, 0).toISOString(), now)).toBe("昨天 00:00");
    expect(chatTimeOf(new Date(2026, 9, 12, 23, 59).toISOString(), now)).toBe("昨天 23:59");
    expect(chatTimeOf(new Date(2026, 9, 12, 3, 0).toISOString(), now)).toBe("昨天 03:00");
    expect(chatTimeOf(new Date(2026, 9, 10, 8, 1).toISOString(), now)).toBe("10月10日");
    expect(chatTimeOf(new Date(2025, 11, 30, 8, 0).toISOString(), now)).toBe("12月30日");
    // 跨日边界(相对 now):now 在窗锚前(02:00)→ 当日 03:00 前的刻属上一窗
    const early = new Date(2026, 9, 13, 2, 0);
    expect(chatTimeOf(new Date(2026, 9, 13, 1, 30).toISOString(), early)).toBe("今天 01:30");
    expect(chatTimeOf(new Date(2026, 9, 12, 2, 30).toISOString(), early)).toBe("昨天 02:30");
    // 缺失/异形(与 formatRelativeTime 同守卫)
    expect(chatTimeOf(null)).toBe("—");
    expect(chatTimeOf("not-a-date")).toBe("not-a-date");
  });
});
