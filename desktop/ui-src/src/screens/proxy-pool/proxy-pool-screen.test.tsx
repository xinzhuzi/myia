// @vitest-environment jsdom
//
// 「代理池」屏组件测试(task 10-14-proxy-pool-panel R5):mock sidecar
// (sidecar_request 假实现)。覆盖:挂载零网络(只读历史)/ 探测两态分流 /
// exit_ip 渲染(undefined 同 null 显「—」)/ 每池分组·总览计数·upstream
// 保序 / 探测中禁用 / 成功率口径文案 / 空态三分支 / 探测后历史即刷 /
// 结构化错误面。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { ProxyPoolScreen } from "./proxy-pool-screen";
import type { ProxyHistoryResult, ProxyPoolRow } from "./api";

/** 宽松应答输入形状(只约束本屏实际消费的键;mock 返回值经 as never 进通道,
 *  完整 DoctorResult 形状不在组件消费面,测试不伪造) */
type PoolRowInput = ProxyPoolRow;
interface ProbeResultInput {
  generated_at: string;
  proxy: { config: string | null; pools: ProxyPoolRow[] };
  snapshot: { persisted: boolean; reason?: string };
}

function installSidecar(
  history: ProxyHistoryResult,
  handlers: Record<string, (params: never) => unknown> = {},
): void {
  mocks.invoke.mockImplementation(async (_command: string, args: { method: string; params?: unknown }) => {
    const handler = handlers[args.method];
    if (handler) return handler(args.params as never);
    if (args.method === "proxy.history") return history;
    throw JSON.stringify({
      code: "method_not_found",
      path: "method",
      message: `未知方法 ${args.method}`,
    });
  });
}

function seenMethods(): string[] {
  return mocks.invoke.mock.calls.map(([, args]) => (args as { method: string }).method);
}

function errJson(code: string, message: string): string {
  return JSON.stringify({ code, path: "params", message });
}

beforeEach(() => {
  mocks.invoke.mockReset();
});
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function renderScreen() {
  return render(
    <MemoryRouter>
      <ProxyPoolScreen />
    </MemoryRouter>,
  );
}

async function settleHistory() {
  await waitFor(() => expect(seenMethods()).toContain("proxy.history"));
}

async function clickProbe() {
  fireEvent.click(screen.getByTestId("proxy-probe-button"));
}

function emptyHistory(overrides: Partial<ProxyHistoryResult> = {}): ProxyHistoryResult {
  return {
    snapshots: [],
    count: 0,
    truncated: false,
    home_available: true,
    ...overrides,
  };
}

describe("代理池屏:挂载零网络", () => {
  it("进屏只发 proxy.history(纯读),绝不探测——seen 调用表无 proxy.probe/doctor", async () => {
    installSidecar(emptyHistory());
    renderScreen();
    await settleHistory();
    await waitFor(() => expect(screen.getByTestId("proxy-history-empty")).toBeTruthy());
    expect(seenMethods().every((method) => method === "proxy.history")).toBe(true);
    expect(seenMethods()).not.toContain("proxy.probe");
    expect(seenMethods()).not.toContain("doctor");
  });

  it("dev 无 home(home_available=false):历史区说明不落盘", async () => {
    installSidecar(emptyHistory({ home_available: false }));
    renderScreen();
    await settleHistory();
    expect(screen.getByTestId("proxy-history-dev-nohome").textContent).toContain("历史不落盘");
  });
});

describe("代理池屏:探测两态与刷新", () => {
  it("路径非空走显式 {config}(trim 后),留空走 {config_auto:true}——G10 同款", async () => {
    const probe: ProbeResultInput = {
      generated_at: "2026-10-14T09:00:00+00:00",
      proxy: { config: "/tmp/my-pools.yaml", pools: [] },
      snapshot: { persisted: true },
    };
    installSidecar(emptyHistory(), {
      "proxy.probe": (() => probe) as never,
    });
    renderScreen();
    await settleHistory();
    fireEvent.change(screen.getByLabelText("全局 pools YAML 路径"), {
      target: { value: "  /tmp/my-pools.yaml  " },
    });
    await clickProbe();
    await waitFor(() => expect(seenMethods()).toContain("proxy.probe"));
    const probeCall = mocks.invoke.mock.calls.find(
      ([, args]) => (args as { method: string }).method === "proxy.probe",
    );
    expect((probeCall?.[1] as { params?: unknown }).params).toEqual({ config: "/tmp/my-pools.yaml" });
    expect(screen.getByTestId("proxy-config-path").textContent).toContain("/tmp/my-pools.yaml");

    // 留空 → config_auto
    fireEvent.change(screen.getByLabelText("全局 pools YAML 路径"), { target: { value: "" } });
    await clickProbe();
    await waitFor(() => expect(seenMethods().filter((m) => m === "proxy.probe")).toHaveLength(2));
    const autoCall = mocks.invoke.mock.calls
      .filter(([, args]) => (args as { method: string }).method === "proxy.probe")
      .at(-1);
    expect((autoCall?.[1] as { params?: unknown }).params).toEqual({ config_auto: true });
  });

  it("探测成功后历史区即刷(落了快照 → proxy.history 二次调用)", async () => {
    installSidecar(emptyHistory(), {
      "proxy.probe": (() => ({
        generated_at: "2026-10-14T09:00:00+00:00",
        proxy: { config: null, pools: [] },
        snapshot: { persisted: true },
      })) as never,
    });
    renderScreen();
    await settleHistory();
    await clickProbe();
    await waitFor(() =>
      expect(seenMethods().filter((method) => method === "proxy.history")).toHaveLength(2),
    );
  });

  it("探测进行中:按钮禁用 + 人话等待文案;落盘失败只降级不 fail", async () => {
    let release: ((value: unknown) => void) | undefined;
    installSidecar(emptyHistory(), {
      "proxy.probe": (() => new Promise((resolve) => (release = resolve))) as never,
    });
    renderScreen();
    await settleHistory();
    await clickProbe();
    await waitFor(() => expect(screen.getByTestId("probe-waiting")).toBeTruthy());
    expect((screen.getByTestId("proxy-probe-button") as HTMLButtonElement).disabled).toBe(true);
    release?.({
      generated_at: "2026-10-14T09:00:00+00:00",
      proxy: { config: null, pools: [] },
      snapshot: { persisted: false, reason: "no_home" },
    });
    await waitFor(() =>
      expect(screen.getByTestId("probe-not-persisted").textContent).toContain("不落历史"),
    );
  });

  it("探测结构化错:ErrorBox 显 code/message", async () => {
    installSidecar(emptyHistory(), {
      "proxy.probe": (() => {
        throw errJson("config", "全局代理池配置拒载:凭据必须走 env:/keychain: 引用");
      }) as never,
    });
    renderScreen();
    await settleHistory();
    await clickProbe();
    await waitFor(() => expect(screen.getByRole("alert")).toBeTruthy());
    expect(screen.getByRole("alert").textContent).toContain("凭据必须走");
  });
});

describe("代理池屏:池卡与总览", () => {
  it("每池分组·upstream_index 保序·总览计数(已解析上游口径)·三态徽标", async () => {
    const rows: PoolRowInput[] = [
      { pool: "main", upstream_index: 1, upstreams: 2, ok: true, proxy_url: "http://***@h2:1", latency_seconds: 0.42, exit_ip: "198.51.100.2", message: "代理连通" },
      { pool: "backup", upstream_index: 0, upstreams: 1, ok: false, proxy_url: "http://***@h3:1", message: "代理链路失败", error_type: "proxy_network" },
      { pool: "main", upstream_index: 0, upstreams: 2, proxy_url: "http://***@h1:1" }, // 未探测 + 无 exit_ip 键
    ];
    installSidecar(emptyHistory(), {
      "proxy.probe": (() => ({
        generated_at: "2026-10-14T09:00:00+00:00",
        proxy: { config: "/tmp/p.yaml", pools: rows },
        snapshot: { persisted: true },
      })) as never,
    });
    renderScreen();
    await settleHistory();
    await clickProbe();
    await waitFor(() => expect(screen.getByTestId("proxy-overview")).toBeTruthy());

    // 总览:池数 2 / 已解析上游 3 / 可用 1 · 不通 1 · 未探测 1(文本连读断言)
    const overview = screen.getByTestId("proxy-overview").textContent ?? "";
    expect(overview).toMatch(/池数\s*2/);
    expect(overview).toMatch(/已解析上游\s*3/);
    expect(overview).toMatch(/可用\s*1/);
    expect(overview).toMatch(/不通\s*1/);
    expect(overview).toMatch(/未探测\s*1/);

    // 池卡:main 2 行且按 upstream_index 排序(h1 在 h2 前);backup 1 行
    const mainRows = within(screen.getByTestId("proxy-pool-card-main")).getAllByTestId("proxy-upstream-row");
    expect(mainRows).toHaveLength(2);
    expect(mainRows[0].textContent).toContain("http://***@h1:1");
    expect(mainRows[1].textContent).toContain("http://***@h2:1");
    expect(
      within(screen.getByTestId("proxy-pool-card-backup")).getAllByTestId("proxy-upstream-row"),
    ).toHaveLength(1);

    // 三态徽标
    expect(within(mainRows[1]).getByText(/连通 · 0.42s/)).toBeTruthy();
    expect(
      within(screen.getByTestId("proxy-pool-card-backup")).getByText("不通"),
    ).toBeTruthy();
    expect(within(mainRows[0]).getByText("未探测")).toBeTruthy();
    // error_type 短标签(title 提示)
    expect(
      within(screen.getByTestId("proxy-pool-card-backup")).getByText("proxy_network"),
    ).toBeTruthy();
  });

  it("exit_ip 渲染:有值显 IP;null 与缺键(兜底行)同显「—」", async () => {
    const rows: PoolRowInput[] = [
      { pool: "main", upstream_index: 0, upstreams: 3, ok: true, proxy_url: "http://***@h1:1", exit_ip: "203.0.113.7" },
      { pool: "main", upstream_index: 1, upstreams: 3, ok: true, proxy_url: "http://***@h2:1", exit_ip: null },
      { pool: "main", upstream_index: 2, upstreams: 3, ok: false, proxy_url: "http://***@h3:1", message: "代理池凭据引用无法解析: xxx" },
    ];
    installSidecar(emptyHistory(), {
      "proxy.probe": (() => ({
        generated_at: "2026-10-14T09:00:00+00:00",
        proxy: { config: "/tmp/p.yaml", pools: rows },
        snapshot: { persisted: true },
      })) as never,
    });
    renderScreen();
    await settleHistory();
    await clickProbe();
    await waitFor(() => expect(screen.getByTestId("proxy-pool-card-main")).toBeTruthy());
    const exitCells = screen.getAllByTestId("proxy-exit-ip");
    expect(exitCells.map((node) => node.textContent)).toEqual([
      "出口 IP:203.0.113.7",
      "出口 IP:—",
      "出口 IP:—",
    ]);
  });

  it("auto 态未命中缺省 pools.yaml:人话提示 + 指引设置屏链接", async () => {
    installSidecar(emptyHistory(), {
      "proxy.probe": (() => ({
        generated_at: "2026-10-14T09:00:00+00:00",
        proxy: { config: null, pools: [] },
        snapshot: { persisted: true },
      })) as never,
    });
    renderScreen();
    await settleHistory();
    await clickProbe();
    await waitFor(() => expect(screen.getByTestId("proxy-auto-miss")).toBeTruthy());
    expect(screen.getByTestId("proxy-auto-miss").textContent).toContain("未找到缺省 pools.yaml");
    const link = screen.getByRole("link", { name: "去设置屏 · 代理池卡" });
    expect(link.getAttribute("href")).toBe("/settings");
  });
});

describe("代理池屏:探测历史区", () => {
  it("每池探测成功率 + 口径文案(非流量成功率 / 仅记本屏发起)+ 条形宽度", async () => {
    const snapshot = (hour: number, mainOk: boolean, backupOk: boolean) => ({
      at: `2026-10-14T0${hour}:00:00+00:00`,
      config: null as string | null,
      pools: [
        { pool: "main", ok: mainOk, proxy_url: "http://***@h:1" },
        { pool: "backup", ok: backupOk, proxy_url: "http://***@h:2" },
      ] as PoolRowInput[],
    });
    installSidecar(
      emptyHistory({
        snapshots: [snapshot(3, true, true), snapshot(2, true, false), snapshot(1, false, false)],
        count: 3,
        truncated: true,
        skipped: 2,
      }),
    );
    renderScreen();
    await waitFor(() => expect(screen.getByTestId("proxy-history-rates")).toBeTruthy());

    // 口径红线 3 + 拷问修正③:两段文案都在同一条描述里(描述含「非流量成功率」唯一可查)
    const description = screen.getByText(/非流量成功率/).textContent ?? "";
    expect(description).toContain("探测成功率(非流量成功率)");
    expect(description).toContain("仅记本屏发起的探测");

    const rates = screen.getAllByTestId("proxy-history-rate");
    expect(rates).toHaveLength(2);
    expect(rates[0].textContent).toContain("main");
    expect(rates[0].textContent).toContain("67%(2/3)");
    expect(rates[1].textContent).toContain("backup");
    expect(rates[1].textContent).toContain("33%(1/3)");
    // 条形 = div 宽度百分比,零图表库(track aria-hidden 内的填充条)
    const bar = rates[0].querySelector('[aria-hidden] > div') as HTMLElement;
    expect(bar.style.width).toBe("67%");
    // 窗口截断 + 坏行跳过如实注记
    expect(screen.getByText(/更早的探测未拉取/)).toBeTruthy();
    expect(screen.getByText(/2 行损坏已跳过/)).toBeTruthy();
    // 快照行:时间 + 配置路径
    const rows = screen.getAllByTestId("proxy-history-snapshot");
    expect(rows).toHaveLength(3);
    expect(rows.every((row) => row.textContent?.includes("(自动探测)"))).toBe(true);
  });

  it("无历史:人话空态(点上方探测开始)", async () => {
    installSidecar(emptyHistory());
    renderScreen();
    await settleHistory();
    expect(screen.getByTestId("proxy-history-empty").textContent).toContain("尚无探测记录");
  });
});
