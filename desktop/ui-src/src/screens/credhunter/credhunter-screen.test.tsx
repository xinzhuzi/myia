// @vitest-environment jsdom
//
// 凭证猎手屏测试(10-14-cred-hunter-panel §3.4 屏测试):mock sidecar
// (credhunter.keys.list fixture)。覆盖:六列渲染 / 徽章四态词表 / 视图
// 切换(高危判据 final_verified)/ provider chips / 掩码域搜索 / 排序切换 /
// 行展开证据 / 三空态文案(exists=false、高危空、无匹配)/ 列宽写读
// localStorage / 应答多余 apikey 键零渲染(G11:UI 零全文密钥)。
import { act, cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { CredhunterScreen } from "./credhunter-screen";
import { COLUMN_SIZES_STORAGE_KEY } from "./api";
import type { CredhunterKeyRecord, CredhunterKeysListResult } from "./api";

/** 缺省记录 = 本机真实冒烟素材形态(xai,hit 1763,final_verified) */
function keyRecord(overrides: Partial<CredhunterKeyRecord> = {}): CredhunterKeyRecord {
  return {
    fingerprint: "sha256-0123456789abcdef",
    masked_apikey: "xai-Hs5v…MASKED…Yc3f",
    provider: "xai",
    first_seen: "2026-09-01T12:00:00Z", // T12 时刻:常见时区本地日不变,日期断言稳
    last_seen: "2026-10-14T12:00:00Z",
    hit_count: 1763,
    sources: ["https://github.com/o/r/blob/main/.env#L1"],
    last_check: "2026-10-14T01:02:03Z",
    check_state: "final_verified",
    ...overrides,
  };
}

const XAI = keyRecord({
  sources: ["https://github.com/o/r/blob/main/.env#L1", "https://gist.github.com/o/1#file-env"],
});
const OPENAI = keyRecord({
  fingerprint: "sha256-fedcba9876543210",
  masked_apikey: "sk-Proj12…MASKED…ab9",
  provider: "openai",
  last_seen: "2026-10-12T12:00:00Z",
  hit_count: 42,
  check_state: "rejected",
});
const DEEPSEEK = keyRecord({
  fingerprint: "sha256-1122334455667788",
  masked_apikey: "dsk-9f2a…MASKED…77",
  provider: "deepseek",
  last_seen: "2026-10-13T12:00:00Z",
  hit_count: 7,
  last_check: null,
  check_state: null,
});
const ANTHROPIC = keyRecord({
  fingerprint: "sha256-99aabbccddeeff00",
  masked_apikey: "sk-ant-Yz1…MASKED…04",
  provider: "anthropic",
  last_seen: "2026-10-10T12:00:00Z",
  hit_count: 99,
  check_state: "transient",
});

/** 四条 fixture:按命中数 xai(1763) > anthropic(99) > openai(42) > deepseek(7);
 *  按最近发现 xai(10-14) > deepseek(10-13) > openai(10-12) > anthropic(10-10) */
const FOUR_KEYS: CredhunterKeyRecord[] = [XAI, OPENAI, DEEPSEEK, ANTHROPIC];

function keysList(records: CredhunterKeyRecord[], overrides: Partial<CredhunterKeysListResult> = {}): CredhunterKeysListResult {
  return {
    path: "/data/home/credhunter-keystore.json",
    exists: true,
    version: 1,
    count: records.length,
    records,
    ...overrides,
  };
}

/** 安装 sidecar mock:credhunter.keys.list → result;未知方法报错(防泄漏调用) */
function installKeys(result: unknown): void {
  mocks.invoke.mockImplementation(async (_command: string, args: { method: string }) => {
    if (args.method === "credhunter.keys.list") return result;
    throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
  });
}

function renderScreen(): ReturnType<typeof render> {
  return render(
    <MemoryRouter>
      <CredhunterScreen />
    </MemoryRouter>,
  );
}

/** 表格主体里可见的掩码行数(空态/过滤断言用) */
function maskedRows(): number {
  const table = document.querySelector("table[aria-label='密钥列表']");
  if (!table) return 0;
  return FOUR_KEYS.filter((record) => table.textContent?.includes(record.masked_apikey)).length;
}

/** 内存 Storage:node 25 + vitest 4 的 jsdom 环境下 window.localStorage 被
 *  Node 实验性全局(缺 clear 等方法)遮蔽,用可工作的 stub 保证持久路径
 *  真实走到(app-layout.test.tsx / feed-screen.test.tsx 同款惯例)。 */
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
  mocks.invoke.mockReset();
  vi.stubGlobal("localStorage", localStorageStub);
  localStorageStub.clear();
});
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("凭证猎手屏:六列与记录渲染", () => {
  it("六列表头 + 记录值(掩码/指纹副行/命中副行日期/证据计数)", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    for (const header of ["密钥", "供应商", "验证状态", "命中", "证据", "最近检查"]) {
      expect(await screen.findByText(header)).toBeTruthy();
    }
    expect(screen.getByText("xai-Hs5v…MASKED…Yc3f")).toBeTruthy();
    expect(screen.getByText("sha256-0123456789abcdef")).toBeTruthy();
    expect(screen.getByText("1763")).toBeTruthy();
    expect(screen.getByText("2026-09-01 → 2026-10-14")).toBeTruthy();
    expect(screen.getByText("2 条")).toBeTruthy();
    // 「未验证」双落点:check_state null 徽章 + last_check null 词面(同词两处,规格如此)
    expect(screen.getAllByText("未验证").length).toBeGreaterThanOrEqual(2);
  });

  it("状态徽章四态词表:已验证存活/已判死/暂不可判/未验证", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");
    expect(screen.getByText("已验证存活")).toBeTruthy();
    expect(screen.getByText("已判死")).toBeTruthy();
    expect(screen.getByText("暂不可判")).toBeTruthy();
    expect(screen.getAllByText("未验证").length).toBeGreaterThanOrEqual(2);
  });

  it("应答带多余 apikey 键也不上屏(G11:UI 零全文密钥)", async () => {
    installKeys({
      ...keysList(FOUR_KEYS),
      records: [{ ...XAI, apikey: "sk-FULLKEY-never-render-me" } as CredhunterKeyRecord & { apikey: string }],
    });
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");
    expect(document.body.textContent).not.toContain("sk-FULLKEY-never-render-me");
  });

  it("协议参数为空对象(credhunter.keys.list 空参)", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");
    const call = mocks.invoke.mock.calls.find(([command]) => command === "sidecar_request");
    expect(call?.[1]).toEqual({ method: "credhunter.keys.list", params: {} });
  });
});

describe("凭证猎手屏:视图切换(高危判据 final_verified)", () => {
  it("高危视图只剩已验证存活;全部密钥视图恢复全量", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");
    expect(maskedRows()).toBe(4);

    fireEvent.click(screen.getByRole("button", { name: "高危" }));
    await screen.findByText("共 1 条", { exact: false });
    expect(maskedRows()).toBe(1);

    fireEvent.click(screen.getByRole("button", { name: "全部密钥" }));
    await screen.findByText("共 4 条", { exact: false });
    expect(maskedRows()).toBe(4);
  });

  it("库在但高危视图空:专门文案「没有已验证存活的泄漏凭证」", async () => {
    installKeys(keysList([OPENAI, DEEPSEEK, ANTHROPIC])); // 无 final_verified
    renderScreen();
    await screen.findByText("sk-Proj12…MASKED…ab9");
    fireEvent.click(screen.getByRole("button", { name: "高危" }));
    expect(await screen.findByText("没有已验证存活的泄漏凭证")).toBeTruthy();
    expect(document.querySelector("table[aria-label='密钥列表']")).toBeNull();
  });
});

describe("凭证猎手屏:搜索与供应商过滤", () => {
  it("掩码域子串搜索(masked_apikey+provider,大小写不敏感)", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");

    fireEvent.change(screen.getByLabelText("搜索密钥"), { target: { value: "XAI" } });
    await screen.findByText("共 1 条", { exact: false });
    expect(maskedRows()).toBe(1);

    fireEvent.change(screen.getByLabelText("搜索密钥"), { target: { value: "sk-" } });
    // openai(sk-Proj)/ anthropic(sk-ant)/ deepseek(dsk- 也含 sk- 子串)= 3 条
    await screen.findByText("共 3 条", { exact: false });

    fireEvent.change(screen.getByLabelText("搜索密钥"), { target: { value: "zzz-no-match" } });
    expect(await screen.findByText("无匹配结果")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "清除过滤" }));
    await screen.findByText("共 4 条", { exact: false });
  });

  it("供应商 chips 过滤(聚合计数 + 多选 + 清除)", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByRole("group", { name: "按供应商筛选" });

    fireEvent.click(screen.getByRole("button", { name: "xai(1 个密钥)" }));
    await screen.findByText("共 1 条", { exact: false });
    expect(maskedRows()).toBe(1);

    fireEvent.click(screen.getByRole("button", { name: "deepseek(1 个密钥)" }));
    await screen.findByText("共 2 条", { exact: false });

    fireEvent.click(screen.getByRole("button", { name: "清除" }));
    await screen.findByText("共 4 条", { exact: false });
  });
});

describe("凭证猎手屏:排序切换", () => {
  it("按命中数缺省高→低;按最近发现新→旧", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");

    const table = document.querySelector("table[aria-label='密钥列表']");
    /** provider → 掩码在表格文本中的字符位置(DOM 行序) */
    const posOf = () => {
      const pos = new Map<string, number>();
      for (const record of FOUR_KEYS) pos.set(record.provider, table?.textContent?.indexOf(record.masked_apikey) ?? -1);
      return pos;
    };
    // 缺省 = 按命中数:xai(1763) > anthropic(99) > openai(42) > deepseek(7)
    const byHits = posOf();
    expect(byHits.get("xai")).toBeLessThan(byHits.get("anthropic") as number);
    expect(byHits.get("anthropic")).toBeLessThan(byHits.get("openai") as number);
    expect(byHits.get("openai")).toBeLessThan(byHits.get("deepseek") as number);

    fireEvent.click(screen.getByRole("button", { name: "按最近发现" }));
    await screen.findByText("dsk-9f2a…MASKED…77");
    // 按最近发现:xai(10-14) > deepseek(10-13) > openai(10-12) > anthropic(10-10)
    const byRecency = posOf();
    expect(byRecency.get("xai")).toBeLessThan(byRecency.get("deepseek") as number);
    expect(byRecency.get("deepseek")).toBeLessThan(byRecency.get("openai") as number);
    expect(byRecency.get("openai")).toBeLessThan(byRecency.get("anthropic") as number);
  });
});

describe("凭证猎手屏:行展开证据", () => {
  it("证据按钮展开:sources URL 明细 + 指纹 + 完整时刻;再点收起", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    const toggle = await screen.findByRole("button", { name: "展开证据 sha256-0123456789abcdef" });
    expect(document.getElementById("credhunter-key-detail-sha256-0123456789abcdef")).toBeNull();

    fireEvent.click(toggle);
    const detail = document.getElementById("credhunter-key-detail-sha256-0123456789abcdef");
    expect(detail).not.toBeNull();
    const text = detail?.textContent ?? "";
    expect(text).toContain("https://github.com/o/r/blob/main/.env#L1");
    expect(text).toContain("https://gist.github.com/o/1#file-env");
    expect(text).toContain("指纹 sha256-0123456789abcdef");
    // 完整时刻带时分(本地时区;不锚死具体钟点,防时区漂移)
    expect(text).toMatch(/首次发现 \d{4}-\d{2}-\d{2} \d{2}:\d{2}/);
    expect(within(detail as HTMLElement).getByText("证据来源(2)")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "收起证据 sha256-0123456789abcdef" }));
    expect(document.getElementById("credhunter-key-detail-sha256-0123456789abcdef")).toBeNull();
  });
});

describe("凭证猎手屏:空态与错误", () => {
  it("库未建(exists=false):专门文案 + credhunt 引导", async () => {
    installKeys({
      path: "/data/home/credhunter-keystore.json",
      exists: false,
      version: null,
      count: 0,
      records: [],
    });
    renderScreen();
    expect(await screen.findByText("凭证猎手还没有密钥库")).toBeTruthy();
    expect(screen.getByText(/猎手\(credhunt\)尚未运行或尚无命中/)).toBeTruthy();
    expect(document.querySelector("table[aria-label='密钥列表']")).toBeNull();
  });

  it("sidecar 错误:结构化错误卡 + 重试", async () => {
    mocks.invoke.mockImplementation(async () => {
      throw JSON.stringify({ code: "keystore_invalid", path: "$.version", message: "版本不符" });
    });
    renderScreen();
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("keystore_invalid");
    expect(alert.textContent).toContain("版本不符");
  });
});

describe("凭证猎手屏:列宽持久化(localStorage)", () => {
  it("预置列宽还原:provider 列渲染持久化宽度", async () => {
    window.localStorage.setItem(COLUMN_SIZES_STORAGE_KEY, JSON.stringify({ provider: 200 }));
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");
    const cols = document.querySelectorAll("table[aria-label='密钥列表'] colgroup col");
    expect(cols.length).toBe(6);
    expect((cols[1] as HTMLElement).style.width).toBe("200px"); // provider
    expect((cols[0] as HTMLElement).style.width).toBe(""); // 密钥列吃剩余,不定宽
  });

  it("拖拽列宽:写入 localStorage(key credhunter.key-table-columns.v1)", async () => {
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");

    const handle = document.querySelector('[data-column-resize-handle="provider"]');
    expect(handle).not.toBeNull();
    // TanStack v8 resize:pointerdown(非 touch)后监听 document mousemove/mouseup。
    // 真实浏览器里 pointerdown 与 mousemove 是两个宏任务(React 有机会 flush
    // setColumnSizingInfo 的 startSize/columnSizingStart);jsdom 同步连发会读到
    // 空 startSize → NaN 宽度。分两段 act 模拟真实时序。
    await act(async () => {
      handle?.dispatchEvent(new MouseEvent("pointerdown", { clientX: 300, bubbles: true }));
    });
    await act(async () => {
      document.dispatchEvent(new MouseEvent("mousemove", { clientX: 400 }));
      document.dispatchEvent(new MouseEvent("mouseup", { clientX: 400 }));
    });
    const saved = JSON.parse(window.localStorage.getItem(COLUMN_SIZES_STORAGE_KEY) ?? "{}") as Record<string, number>;
    // provider 初始 110px:delta +100 → 110*(1+100/110) = 210
    expect(saved.provider).toBe(210);
    const cols = document.querySelectorAll("table[aria-label='密钥列表'] colgroup col");
    expect((cols[1] as HTMLElement).style.width).toBe("210px");
  });

  it("损坏的持久化 JSON:整体弃用回缺省,不阻断渲染", async () => {
    window.localStorage.setItem(COLUMN_SIZES_STORAGE_KEY, "{not-json");
    installKeys(keysList(FOUR_KEYS));
    renderScreen();
    await screen.findByText("xai-Hs5v…MASKED…Yc3f");
    const cols = document.querySelectorAll("table[aria-label='密钥列表'] colgroup col");
    expect((cols[1] as HTMLElement).style.width).toBe("110px"); // 列定义初始值
  });
});
