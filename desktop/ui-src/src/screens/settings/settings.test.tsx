// @vitest-environment jsdom
//
// 设置组件测试:mock sidecar(secret.set / secret.list / doctor 的 JS 假实现),
// 覆盖:LLM 凭据保存(只经 secret.set 入钥匙链、值零回显、保存即清)/
// env: 引用不经界面写 / 表单校验 / secret.set 失败结构化错误 /
// doctor 回显(凭据存在性 + enrich 现值 + findings)/ 推送凭据保存 / 代理池探测。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
// updater-card 随「更新」分区挂载:两插件模块也须 mock(真实 plugin-updater 会从
// core 导入 Resource/Channel,上面的极简 core mock 不提供;本文件不点更新按钮,
// 行为用例在 updater-card.test.tsx)。
vi.mock("@tauri-apps/plugin-updater", () => ({ check: vi.fn() }));
vi.mock("@tauri-apps/plugin-process", () => ({ relaunch: vi.fn() }));

import { SettingsScreen } from "./settings-screen";
import type {
  CredentialEntry,
  DoctorPluginReport,
  DoctorResult,
  EnrichSection,
  Finding,
  GatesSaveParams,
  GatesView,
  PluginReport,
  ProxyPoolStatus,
  SecretSetParams,
} from "@/lib/api";

// ---------------------------------------------------------------------------
// 协议夹具(types.ts 逐字段对照)
// ---------------------------------------------------------------------------

function pluginFixture(file: string, overrides?: Partial<DoctorPluginReport>): DoctorPluginReport {
  const base: PluginReport = {
    file,
    id: "stocks",
    name: "量化快讯",
    schedule: "*/30 * * * *",
    timezone: "Asia/Shanghai",
    push_channels: ["feishu_card", "telegram"],
    loaded: true,
    load_errors: null,
    sources: [],
  };
  return { ...base, next_fire_at: null, enrich: null, ...overrides };
}

function enrichFixture(model: string): EnrichSection {
  return {
    enabled: true,
    model,
    scores: ["value", "relevance", "credibility"],
    batch: 8,
    cache: true,
    budget_per_run: 40,
    cache_rows: 12,
  };
}

function credentialFixture(overrides?: Partial<CredentialEntry>): CredentialEntry {
  return {
    kind: "keychain",
    name: "myia/stocks/tg_token",
    ref: "keychain:myia/stocks/tg_token",
    paths: [{ plugin: "stocks", path: "$.push[1].target" }],
    plugins: ["stocks"],
    exists: true,
    ...overrides,
  };
}

function doctorFixture(overrides?: {
  plugins?: DoctorPluginReport[];
  credentials?: CredentialEntry[];
  findings?: Finding[];
  pools?: ProxyPoolStatus[];
  config?: string | null;
}): DoctorResult {
  const findings = overrides?.findings ?? [];
  return {
    command: "doctor",
    generated_at: "2026-10-02T10:00:00.000Z",
    db: "myssia.db",
    // 与 cli.py 同口径:healthy = 无 error 级 finding
    healthy: !findings.some((finding) => finding.severity === "error"),
    plugins: overrides?.plugins ?? [],
    credentials: {
      backend_available: true,
      backend_error: null,
      entries: overrides?.credentials ?? [],
    },
    proxy: { config: overrides?.config ?? null, pools: overrides?.pools ?? [] },
    findings,
    summary: { plugins: overrides?.plugins?.length ?? 0, sources: 0, errors: 0, warnings: 0 },
  };
}

// ---------------------------------------------------------------------------
// mock sidecar:secret.set 记名记值(值只在断言里用,绝不进 DOM)、doctor 可编程
// ---------------------------------------------------------------------------

interface SidecarState {
  secrets: Map<string, string>;
  doctor: (params: { config?: string; config_auto?: boolean }) => DoctorResult;
  /** push.test 可编程应答(G5 用例;缺省成功) */
  pushTest: (params: { channel: string; target?: string }) => unknown;
  /** gates.* 内存态(门槛件分区;缺省 = 全关空表,fail-closed 未配置态) */
  gates: GatesView;
  gatesPath: string;
  /** gates.save 最近一次收到的整份载荷(断言用;null = 尚未保存) */
  gatesSaved: GatesView | null;
  /** gates.get 拒载明细(gates.yaml 坏 = 全关态 + error 载荷,不炸设置屏) */
  gatesGetError: { source: string | null; errors: { path: string; error_type: string; message: string }[] } | null;
}

/** gates.yaml 全关缺省态(GatesConfig().to_payload 同形状) */
function gatesFixture(overrides?: Partial<GatesView>): GatesView {
  return {
    version: 1,
    paid_engines: false,
    third_party_trace: false,
    saas: {},
    platforms: {},
    analysis: {},
    ...overrides,
  };
}

function installSidecar(
  doctorImpl?: (params: { config?: string; config_auto?: boolean }) => DoctorResult,
) {
  const state: SidecarState = {
    secrets: new Map(),
    doctor: doctorImpl ?? (() => doctorFixture()),
    pushTest: (params) => ({ ok: true, channel: params.channel }),
    gates: gatesFixture(),
    gatesPath: "/home/myia/gates.yaml",
    gatesSaved: null,
    gatesGetError: null,
  };
  mocks.invoke.mockImplementation(
    async (_command: string, args: { method?: string; params?: unknown }) => {
      // pyenv 壳命令直连(10-05-desktop-managed-py-env 第 4 步):无 method 键,
      // 缺省未配置态足以供分区挂载断言(行为面全覆盖在 pyenv-card.test.tsx)
      if (_command === "pyenv_get_status") {
        return {
          state: "not_configured",
          install_path: "/home/myia/python",
          python_path: "/home/myia/python/bin/python3",
          mirror_runtime: null,
          mirror_pypi: null,
          steps: [],
        };
      }
      switch (args.method) {
        case "secret.set": {
          const { name, value } = args.params as SecretSetParams;
          state.secrets.set(name, value);
          return { name, stored: true };
        }
        case "secret.list":
          return { names: [...state.secrets.keys()].sort() };
        case "secret.delete": {
          const { name } = args.params as { name: string };
          if (!state.secrets.has(name)) {
            throw JSON.stringify({
              code: "secret_not_found",
              path: "params.name",
              message: `系统钥匙链中未找到凭据 ${name},无法删除`,
            });
          }
          state.secrets.delete(name);
          return { name, deleted: true };
        }
        case "push.test":
          return state.pushTest(args.params as { channel: string; target?: string });
        case "doctor":
          return state.doctor((args.params ?? {}) as { config?: string; config_auto?: boolean });
        case "gates.get":
          // entry.py _m_gates_get 实况:坏文件 fail-closed 不炸设置屏
          // (config 全关 + error 载荷;exists = 文件在否)
          return {
            config: state.gates,
            path: state.gatesPath,
            exists: state.gatesGetError !== null,
            error: state.gatesGetError,
          };
        case "gates.save": {
          const params = args.params as GatesSaveParams;
          state.gatesSaved = params.config;
          state.gates = params.config;
          state.gatesGetError = null; // 合法覆写即修复
          return { ok: true, path: state.gatesPath };
        }
        default:
          throw JSON.stringify({
            code: "method_not_found",
            path: "method",
            message: `未知方法 ${args.method}`,
            data: { allowed: ["doctor", "secret.list", "secret.set"] },
          });
      }
    },
  );
  return state;
}

function callsOf(method: string): unknown[] {
  return mocks.invoke.mock.calls
    // 直连壳命令(sidecar_restart / pyenv_*)无 args 对象——filter 侧容 undefined
    .filter(([, args]) => (args as { method?: string } | undefined)?.method === method)
    .map(([, args]) => (args as { params: unknown }).params);
}

async function typeByLabel(label: string, value: string): Promise<void> {
  fireEvent.change(screen.getByLabelText(label), { target: { value } });
}

/** D4 结构重做后设置屏用 useSearchParams(?section= 驱动分区),渲染须包 Router */
function renderScreen(initialEntry = "/settings") {
  return render(
    <MemoryRouter initialEntries={[initialEntry]}>
      <SettingsScreen />
    </MemoryRouter>,
  );
}

/** 经左侧分区导航切区(拆解表第 1 条:导航驱动右侧子区一屏) */
async function openSection(sectionId: string): Promise<void> {
  fireEvent.click(await screen.findByTestId(`settings-nav-${sectionId}`));
}

beforeEach(() => {
  mocks.invoke.mockReset();
});
afterEach(() => {
  cleanup(); // vitest 非 globals 模式下 RTL 不自动清理,防 DOM 跨测试污染
  vi.clearAllMocks();
});

// ---------------------------------------------------------------------------

describe("设置:LLM 凭据保存(钥匙链唯一路径,零回显)", () => {
  it("base_url+key 各写一个规范名;保存即清 key;值不出现在任何 DOM", async () => {
    const state = installSidecar();
    renderScreen();
    await typeByLabel("base_url", "https://open.bigmodel.cn/api/paas/v4");
    await typeByLabel("model", "glm-4-flash");
    await typeByLabel("LLM API Key", "sk-secret-123456");
    fireEvent.click(screen.getByRole("button", { name: "保存 LLM 凭据" }));

    await screen.findByTestId("save-status");
    // secret.set 两次:名字规范、值原样过协议(值只在协议侧,不回程)
    const setCalls = callsOf("secret.set") as SecretSetParams[];
    expect(setCalls).toContainEqual({ name: "myia/llm/base_url", value: "https://open.bigmodel.cn/api/paas/v4" });
    expect(setCalls).toContainEqual({ name: "myia/llm/api_key", value: "sk-secret-123456" });
    expect(state.secrets.get("myia/llm/api_key")).toBe("sk-secret-123456");
    // 铁律:值零回显 —— 整个 DOM 找不到 key 明文;key 输入框已清空
    expect(document.body.textContent).not.toContain("sk-secret-123456");
    expect((screen.getByLabelText("LLM API Key") as HTMLInputElement).value).toBe("");
    // 状态行只报名字
    expect(screen.getByTestId("save-status").textContent).toContain("myia/llm/api_key");
    expect(screen.getByTestId("save-status").textContent).toContain("myia/llm/base_url");
  });

  it("base_url 为 env: 引用 → 不经界面写(无 secret.set),给出入 YAML 提示", async () => {
    const state = installSidecar();
    renderScreen();
    await typeByLabel("base_url", "env:MYIA_LLM_BASE_URL");
    await typeByLabel("model", "glm-4-flash");
    fireEvent.click(screen.getByRole("button", { name: "保存 LLM 凭据" }));

    await waitFor(() => {
      expect(screen.getByText(/请把该引用直接写入品类 YAML/)).toBeTruthy();
    });
    expect(callsOf("secret.set")).toEqual([]); // 引用不是值,不写钥匙链
    expect(state.secrets.size).toBe(0);
  });

  it("model 为空不拦凭据保存(model 不经界面持久化,只有凭据走 secret.set)", async () => {
    installSidecar();
    renderScreen();
    await typeByLabel("base_url", "https://api.example.com");
    fireEvent.click(screen.getByRole("button", { name: "保存 LLM 凭据" }));

    await screen.findByTestId("save-status");
    // 只有 base_url 入钥匙链;model 不产生任何写调用
    expect(callsOf("secret.set")).toEqual([
      { name: "myia/llm/base_url", value: "https://api.example.com" },
    ]);
  });

  it("base_url 非法(既非 URL 也非引用)→ 前端校验拦下,零写调用", async () => {
    installSidecar();
    renderScreen();
    await typeByLabel("base_url", "ftp://not-allowed");
    fireEvent.click(screen.getByRole("button", { name: "保存 LLM 凭据" }));

    expect(await screen.findByText(/base_url 须为 http\(s\) 地址或 env:\/keychain: 引用/)).toBeTruthy();
    expect(callsOf("secret.set")).toEqual([]);
  });

  it("secret.set 失败 → 结构化错误态;key 明文不落 DOM", async () => {
    mocks.invoke.mockImplementation(async (_command: string, args: { method: string }) => {
      if (args.method === "secret.set") {
        throw JSON.stringify({ code: "keychain_unavailable", path: "params.name", message: "钥匙链后端不可用" });
      }
      if (args.method === "doctor") return doctorFixture();
      throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
    });
    renderScreen();
    await typeByLabel("model", "glm-4-flash");
    await typeByLabel("LLM API Key", "sk-do-not-echo");
    fireEvent.click(screen.getByRole("button", { name: "保存 LLM 凭据" }));

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("钥匙链后端不可用");
    expect(alert.textContent).toContain("code=keychain_unavailable");
    expect(alert.textContent).toContain("path=params.name");
    expect(screen.queryByTestId("save-status")).toBeNull();
    // 失败时输入保留在用户自己的输入框里(未保存),但绝无旁路回显节点
    expect((screen.getByLabelText("LLM API Key") as HTMLInputElement).value).toBe("sk-do-not-echo");
    expect(document.body.textContent).not.toContain("已写入钥匙链");
  });
});

describe("设置:doctor 验证回显", () => {
  it("挂载即 doctor:凭据存在性 / enrich 现值 / findings 结构化展示", async () => {
    installSidecar(() =>
      doctorFixture({
        plugins: [
          pluginFixture("plugins/stocks.yaml", {
            enrich: enrichFixture("glm-4-flash"),
          }),
        ],
        credentials: [
          credentialFixture(),
          credentialFixture({
            name: "myia/stocks/feishu_chat_id",
            ref: "keychain:myia/stocks/feishu_chat_id",
            exists: false,
          }),
        ],
        findings: [
          {
            severity: "error",
            scope: "credentials",
            code: "keychain_ref_missing",
            message: "钥匙链中不存在凭据 myia/stocks/feishu_chat_id",
          },
        ],
      }),
    );
    renderScreen();

    const panel = await screen.findByTestId("doctor-verify");
    expect(panel.textContent).toContain("myia/stocks/tg_token");
    expect(panel.textContent).toContain("已在钥匙链");
    expect(panel.textContent).toContain("myia/stocks/feishu_chat_id");
    expect(panel.textContent).toContain("缺失(需写入)");
    expect(panel.textContent).toContain("model=glm-4-flash");
    expect(panel.textContent).toContain("keychain_ref_missing");
    expect(panel.textContent).toContain("存在 error 级发现"); // healthy 随 findings 如实降级
  });

  it("保存后自动 doctor 复核:新凭据以 exists=true 回显", async () => {
    const state = installSidecar(() =>
      doctorFixture({
        credentials: [...[...state.secrets.keys()].map((name) => credentialFixture({ name, ref: `keychain:${name}` }))],
      }),
    );
    renderScreen();
    await screen.findByTestId("doctor-verify");

    await typeByLabel("LLM API Key", "sk-later-verify");
    fireEvent.click(screen.getByRole("button", { name: "保存 LLM 凭据" }));

    await waitFor(() => {
      expect(callsOf("doctor").length).toBeGreaterThanOrEqual(2); // 挂载一次 + 保存后一次
    });
    expect(screen.getByTestId("doctor-verify").textContent).toContain("myia/llm/api_key");
    expect(screen.getByTestId("doctor-verify").textContent).toContain("已在钥匙链");
    expect((screen.getByLabelText("LLM API Key") as HTMLInputElement).value).toBe("");
    expect(document.body.textContent).not.toContain("sk-later-verify");
  });
});

describe("设置:推送通道凭据", () => {
  it("预设位:feishu 三字段逐条写 myia/push/<ENV_KEY>;保存即清值零回显", async () => {
    const state = installSidecar();
    renderScreen();
    await openSection("push");
    await typeByLabel("feishu_card App ID", "cli_test_app");
    await typeByLabel("feishu_card App Secret", "sec_private_value");
    await typeByLabel("feishu_card 群 chat_id", "oc_room123");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));

    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({
      name: "myia/push/FEISHU_APP_ID",
      value: "cli_test_app",
    });
    expect(callsOf("secret.set")).toContainEqual({
      name: "myia/push/FEISHU_APP_SECRET",
      value: "sec_private_value",
    });
    expect(callsOf("secret.set")).toContainEqual({
      name: "myia/push/FEISHU_CHAT_ID",
      value: "oc_room123",
    });
    expect(document.body.textContent).not.toContain("sec_private_value");
    expect((screen.getByLabelText("feishu_card App Secret") as HTMLInputElement).value).toBe("");
    expect(state.secrets.get("myia/push/FEISHU_APP_SECRET")).toBe("sec_private_value");
  });

  it("预设位:空字段跳过;全空 → note 拦截零协议调用", async () => {
    installSidecar();
    renderScreen();
    await openSection("push");
    await typeByLabel("feishu_card App Secret", "only_secret");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));
    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toEqual([
      { name: "myia/push/FEISHU_APP_SECRET", value: "only_secret" },
    ]);

    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));
    expect(await screen.findByText(/至少填一个字段/)).toBeTruthy();
    expect(callsOf("secret.set")).toHaveLength(1);
  });

  it("自定义凭据位(折叠区):按 scope+名字写 myia/<scope>/<name>", async () => {
    const state = installSidecar();
    renderScreen();
    await openSection("push");
    await typeByLabel("品类 scope", "stocks");
    await typeByLabel("推送凭据名", "chat_id");
    await typeByLabel("推送凭据值", "oc_abc123private");
    fireEvent.click(screen.getByRole("button", { name: "保存自定义凭据位" }));

    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/stocks/chat_id", value: "oc_abc123private" });
    expect(document.body.textContent).not.toContain("oc_abc123private");
    expect(state.secrets.get("myia/stocks/chat_id")).toBe("oc_abc123private");
  });

  it("自定义凭据位:scope 非法 → 前端校验拦截,零协议调用", async () => {
    installSidecar();
    renderScreen();
    await openSection("push");
    await typeByLabel("品类 scope", "Stocks!");
    await typeByLabel("推送凭据值", "whatever");
    fireEvent.click(screen.getByRole("button", { name: "保存自定义凭据位" }));

    expect(await screen.findByText(/scope 须为品类 id 规则/)).toBeTruthy();
    expect(callsOf("secret.set")).toEqual([]);
  });
});

describe("设置:代理池", () => {
  it("探测走 doctor(--config=路径),逐池回显连通性", async () => {
    const seen: Array<{ config?: string } | undefined> = [];
    installSidecar((params) => {
      seen.push(params);
      return doctorFixture({
        config: params.config ?? null,
        pools: [{ pool: "main", ok: true, latency_seconds: 0.42 }],
      });
    });
    renderScreen();
    await screen.findByTestId("doctor-verify"); // 等挂载 doctor 结算,探测按钮可点
    await typeByLabel("pools YAML 路径", "config/pools.yaml");
    fireEvent.click(screen.getByRole("button", { name: "探测" }));

    await waitFor(() => {
      expect(seen.some((params) => params?.config === "config/pools.yaml")).toBe(true);
    });
    const row = await screen.findByTestId("proxy-pool-row");
    expect(row.textContent).toContain("main");
    expect(row.textContent).toContain("连通");
    expect(row.textContent).toContain("0.42s");
  });

  it("G10 探测两态:留空发 config_auto,自动命中回显配置路径 + 逐池行", async () => {
    const seen: Array<{ config?: string; config_auto?: boolean } | undefined> = [];
    installSidecar((params) => {
      seen.push(params);
      // 镜像 sidecar 语义:显式 config 赢;缺省且 config_auto → 自动命中路径
      const config = params.config ?? (params.config_auto ? "/home/myia/pools.yaml" : null);
      return doctorFixture({
        config,
        pools: config ? [{ pool: "main", ok: true, latency_seconds: 0.31 }] : [],
      });
    });
    renderScreen();
    await screen.findByTestId("doctor-verify"); // 挂载 doctor 结算(无 config/config_auto)
    expect(seen[0]).toEqual({});
    fireEvent.click(screen.getByRole("button", { name: "探测" })); // 路径留空 → 自动态

    await waitFor(() => {
      expect(seen.some((params) => params?.config_auto === true && params?.config === undefined)).toBe(true);
    });
    const row = await screen.findByTestId("proxy-pool-row");
    expect(row.textContent).toContain("main");
    expect(row.textContent).toContain("0.31s");
    expect(screen.getByTestId("proxy-config-path").textContent).toContain("/home/myia/pools.yaml");
    expect(screen.queryByTestId("proxy-auto-miss")).toBeNull(); // 命中不冒未找到
  });

  it("G10 探测两态:自动未命中 → 人话提示行;挂载初始不冒;填路径重探退场", async () => {
    const seen: Array<{ config?: string; config_auto?: boolean } | undefined> = [];
    installSidecar((params) => {
      seen.push(params);
      return doctorFixture({ config: params.config ?? null, pools: [] });
    });
    renderScreen();
    await screen.findByTestId("doctor-verify");
    // 挂载初始(未探测)不冒「未找到」——提示行只跟自动探测走
    expect(screen.queryByTestId("proxy-auto-miss")).toBeNull();
    expect(screen.queryByTestId("proxy-config-path")).toBeNull();
    expect(screen.getByLabelText("pools YAML 路径").getAttribute("placeholder")).toContain("自动探测");

    fireEvent.click(screen.getByRole("button", { name: "探测" }));
    await waitFor(() => {
      expect(seen.some((params) => params?.config_auto === true)).toBe(true);
    });
    expect(await screen.findByTestId("proxy-auto-miss")).toBeTruthy();
    expect(screen.getByTestId("proxy-auto-miss").textContent).toContain("未找到缺省 pools.yaml");
    expect(screen.getByTestId("proxy-auto-miss").textContent).toContain("填入全局配置路径");

    // 填路径重探 → 显式 config(手填赢),提示行退场
    await typeByLabel("pools YAML 路径", "config/pools.yaml");
    fireEvent.click(screen.getByRole("button", { name: "探测" }));
    await waitFor(() => {
      expect(seen.some((params) => params?.config === "config/pools.yaml")).toBe(true);
    });
    await waitFor(() => {
      expect(screen.queryByTestId("proxy-auto-miss")).toBeNull();
    });
  });

  it("池凭据写入 myia/proxy/<pool>", async () => {
    const state = installSidecar();
    renderScreen();
    await typeByLabel("代理池名", "main");
    await typeByLabel("代理凭据值", "user-ref:pass-ref");
    fireEvent.click(screen.getByRole("button", { name: "保存代理凭据" }));

    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/proxy/main", value: "user-ref:pass-ref" });
    expect(state.secrets.get("myia/proxy/main")).toBe("user-ref:pass-ref");
  });
});

// ---------------------------------------------------------------------------
// C5 凭据删除(secret.delete 危险区):79f7f7b 分区 6→4 收编时「高级」区从
// SECTIONS 移除,危险区一度困在守卫 id==="advanced" 的死分支 UI 不可达
// (本测试块当时整删)。10-05 归位:危险区随系统分区渲染(分区描述与终态
// 合同的「凭据管理」落地),死分支已删,测试块随之恢复。
// ---------------------------------------------------------------------------

describe("设置:危险区钥匙链凭据(C5;10-05 归位系统分区)", () => {
  it("系统分区挂危险区卡并列出钥匙链名(通用区不挂)", async () => {
    const state = installSidecar();
    state.secrets.set("myia/llm/api_key", "v1");
    state.secrets.set("myia/push/FEISHU_APP_ID", "v2");
    renderScreen("/settings?section=system");

    const zone = await screen.findByTestId("settings-danger-zone");
    expect(zone.textContent).toContain("危险区 · 钥匙链凭据");
    expect(zone.textContent).toContain("myia/llm/api_key");
    expect(zone.textContent).toContain("myia/push/FEISHU_APP_ID");
    expect(screen.queryByTestId("settings-section-general")).toBeNull();
  });

  it("删除凭据:inline 二次确认 → secret.delete 真调 → 清单刷新徽标消失", async () => {
    const state = installSidecar();
    state.secrets.set("myia/proxy/main", "v");
    renderScreen("/settings?section=system");
    await screen.findByTestId("settings-danger-zone");

    fireEvent.click(screen.getByRole("button", { name: "删除凭据 myia/proxy/main" }));
    fireEvent.click(screen.getByTestId("confirm-delete-myia/proxy/main"));

    await waitFor(() => {
      expect(callsOf("secret.delete")).toContainEqual({ name: "myia/proxy/main" });
    });
    await waitFor(() => {
      expect(screen.queryByText("myia/proxy/main")).toBeNull();
    });
    expect(state.secrets.has("myia/proxy/main")).toBe(false);
  });
});

// ---------------------------------------------------------------------------
// B3+C11(10-03-v112-desktop-parity):评分与反馈分区(enrich.enabled/model 写回
// yaml.read→文本手术→yaml.save(mtime 锁)→doctor 复核)+ mutateEnrichField 纯函数
// ---------------------------------------------------------------------------

const SAMPLE_YAML = `id: stocks
name: 量化快讯
enrich:
  enabled: true   # 精评开关(B3)
  model: glm-4-flash
  budget_per_run: 40
push:
  - channel: feishu_card
    enabled: true
`;

describe("mutateEnrichField 纯函数(文本手术,注释保真)", () => {
  it("改 enabled:只动命中行值段,行内注释与其余原文逐字节不动", async () => {
    const { mutateEnrichField } = await import("./api");
    const next = mutateEnrichField(SAMPLE_YAML, "enabled", "false");
    expect(next).toContain("  enabled: false   # 精评开关(B3)");
    expect(next).toContain("  model: glm-4-flash");
    expect(next).toContain("    enabled: true"); // push 节内同名键不受扰(只在 enrich 块内匹配)
    // 其余行原样(行数不变,除命中行外逐行相等)
    expect(next.split("\n")).toHaveLength(SAMPLE_YAML.split("\n").length);
  });

  it("改 model:同款手术", async () => {
    const { mutateEnrichField } = await import("./api");
    const next = mutateEnrichField(SAMPLE_YAML, "model", "glm-4.6");
    expect(next).toContain("  model: glm-4.6");
    expect(next).toContain("  enabled: true   # 精评开关(B3)");
  });

  it("无顶层 enrich 节 / 节内无该字段行 → CategoryNodeError(enrich_node_missing)", async () => {
    const { mutateEnrichField, CategoryNodeError } = await import("./api");
    expect(() => mutateEnrichField("id: stocks\n", "enabled", "false")).toThrow(CategoryNodeError);
    expect(() =>
      mutateEnrichField("enrich:\n  model: glm-4-flash\n", "budget_per_run", "10"),
    ).toThrow(/budget_per_run/);
  });
});

describe("设置:评分与反馈分区(B3+C11)", () => {
  function installYamlSidecar(options?: { saveImpl?: (params: { file: string; content: string }) => void }) {
    let mtime = 1_700_000_000;
    const state = {
      saved: null as { file: string; content: string; expected_mtime: number | null } | null,
      secrets: new Map<string, string>(),
      doctorImpl: () =>
        doctorFixture({
          plugins: [pluginFixture("plugins/stocks.yaml", { enrich: enrichFixture("glm-4-flash") })],
        }),
    };
    mocks.invoke.mockImplementation(
      async (_command: string, args: { method: string; params?: unknown }) => {
        switch (args.method) {
          case "doctor":
            return state.doctorImpl();
          case "secret.list":
            return { names: [...state.secrets.keys()].sort() };
          case "yaml.read":
            return { file: "plugins/stocks.yaml", content: SAMPLE_YAML, size: SAMPLE_YAML.length, mtime };
          case "yaml.save": {
            const params = args.params as { file: string; content: string; expected_mtime: number | null };
            if (params.expected_mtime !== mtime) {
              throw JSON.stringify({
                code: "mtime_conflict",
                path: "params.expected_mtime",
                message: "文件已被其他编辑改写,请刷新后重试",
              });
            }
            options?.saveImpl?.(params);
            state.saved = params;
            mtime += 1;
            return {
              file: params.file,
              written: true,
              created: false,
              backed_up: "plugins/stocks.yaml.bak",
              mtime,
              warnings: [],
            };
          }
          default:
            throw JSON.stringify({
              code: "method_not_found",
              path: "method",
              message: `未知方法 ${args.method}`,
            });
        }
      },
    );
    return state;
  }

  it("挂载即渲染逐品类行(doctor enrich 节);budget 只读护栏明示", async () => {
    installYamlSidecar();
    renderScreen();
    const row = await screen.findByTestId("enrich-row-plugins/stocks.yaml");
    expect(row.textContent).toContain("stocks.yaml");
    expect(row.textContent).toContain("budget_per_run = 40");
    expect(row.textContent).toContain("精评已启用");
  });

  it("停用开关(Switch 即时写回):yaml.read → 文本手术(enabled: true→false)→ yaml.save(mtime 锁)→ doctor 复核", async () => {
    const state = installYamlSidecar();
    renderScreen();
    const toggle = await screen.findByRole("switch", { name: "精评开关 plugins/stocks.yaml" });
    fireEvent.click(toggle);

    await waitFor(() => expect(state.saved).not.toBeNull());
    expect(state.saved?.file).toBe("plugins/stocks.yaml");
    expect(state.saved?.content).toContain("  enabled: false   # 精评开关(B3)");
    // enrich 节内 enabled 不再为 true(整行匹配;push 节内的同名键不受扰)
    expect(state.saved?.content).not.toMatch(/^  enabled: true/m);
    expect(state.saved?.expected_mtime).toBe(1_700_000_000);
    // 写后 doctor 复核(callsOf 不适用此 mock,断言 invoke 序列含 doctor after save)
    await waitFor(() => {
      const methods = mocks.invoke.mock.calls.map(([, args]) => (args as { method: string }).method);
      const saveAt = methods.lastIndexOf("yaml.save");
      expect(methods.slice(saveAt)).toContain("doctor");
    });
  });

  it("model 写回:与现值一致禁用保存;改值后 yaml.save 带 mtime 锁", async () => {
    const state = installYamlSidecar();
    renderScreen();
    const input = await screen.findByLabelText("精评模型 plugins/stocks.yaml");
    // 现值一致 → 保存禁用(本项目无 jest-dom,原生 disabled 直查)
    expect((screen.getByRole("button", { name: /保存 model/ }) as HTMLButtonElement).disabled).toBe(true);
    fireEvent.change(input, { target: { value: "glm-4.6" } });
    const save = screen.getByRole("button", { name: /保存 model/ }) as HTMLButtonElement;
    expect(save.disabled).toBe(false);
    fireEvent.click(save);

    await waitFor(() => expect(state.saved?.content).toContain("  model: glm-4.6"));
    expect(state.saved?.content).toMatch(/^  enabled: true\s+#/m); // enrich 节 enabled 未被扰
  });

  it("mtime_conflict 结构化透传(mtime 乐观锁);不静默吞", async () => {
    let first = true;
    installYamlSidecar({
      saveImpl: () => {
        if (first) {
          first = false;
          throw JSON.stringify({
            code: "mtime_conflict",
            path: "params.expected_mtime",
            message: "文件已被其他编辑改写,请刷新后重试",
          });
        }
      },
    });
    renderScreen();
    fireEvent.click(await screen.findByRole("switch", { name: "精评开关 plugins/stocks.yaml" }));
    // 断言限定本卡(结构重做后 vision-form 仅在「视觉」分区挂载,本区唯一 alert)
    const card = screen.getByTestId("enrich-feedback-card");
    const box = await within(card).findByRole("alert");
    expect(box.textContent).toContain("mtime_conflict");
    expect(box.textContent).toContain("已被其他编辑改写");
  });

  it("品类无 enrich 节:CategoryNodeError 行内指引(去配置编辑),不弹协议错误", async () => {
    const noEnrichYaml = "id: stocks\nname: 量化快讯\n";
    mocks.invoke.mockImplementation(
      async (_command: string, args: { method: string }) => {
        if (args.method === "doctor") {
          return doctorFixture({
            plugins: [pluginFixture("plugins/stocks.yaml", { enrich: enrichFixture("glm-4-flash") })],
          });
        }
        if (args.method === "secret.list") return { names: [] };
        if (args.method === "yaml.read") {
          return { file: "plugins/stocks.yaml", content: noEnrichYaml, size: 10, mtime: 1 };
        }
        if (args.method === "yaml.save") {
          return {
            file: "plugins/stocks.yaml",
            written: true,
            created: false,
            backed_up: null,
            mtime: 2,
            warnings: [],
          };
        }
        throw JSON.stringify({ code: "method_not_found", path: "method", message: "x" });
      },
    );
    renderScreen();
    fireEvent.click(await screen.findByRole("switch", { name: "精评开关 plugins/stocks.yaml" }));
    const note = await screen.findByTestId("enrich-node-error");
    expect(note.textContent).toContain("缺少 enrich");
    expect(note.textContent).toContain("配置编辑");
  });

  it("push 声明指引链接(在「推送」分区卡底)→ 配置编辑屏路由(HashRouter 锚点)", async () => {
    installYamlSidecar();
    renderScreen();
    await openSection("push");
    const link = await screen.findByRole("link", { name: "去配置编辑改 push 声明" });
    expect(link.getAttribute("href")).toBe("#/yaml-editor");
  });
});

// ---------------------------------------------------------------------------
// 推送测试按钮(G5 前半,10-03-feed-ux):push.test 真发一条,行内回显
// ---------------------------------------------------------------------------

describe("设置:推送测试(G5)", () => {
  it("target=预设位 keychain 引用(与真实推送同源解析);成功回显 ok 徽标", async () => {
    installSidecar();
    renderScreen();
    await openSection("push");

    fireEvent.click(screen.getByRole("button", { name: "发送测试" }));

    await waitFor(() => expect(callsOf("push.test")).toHaveLength(1));
    // channel 取表单当前选中(feishu_card);target = 预设凭据位(10-05-push-credential-journey)
    expect(callsOf("push.test")).toContainEqual({
      channel: "feishu_card",
      target: "keychain:myia/push/FEISHU_CHAT_ID",
    });
    expect(await screen.findByText("通道连通")).toBeTruthy();
    expect(screen.getByTestId("push-test-result").textContent).toContain("feishu_card");
    // 状态行绝不出现凭据值(引用名不是秘密)
    expect(document.body.textContent).not.toContain("keychain:myia/push/FEISHU_CHAT_ID");
  });

  it("失败结构化透传:env_var_missing → 通道失败徽标 + code:message 行内回显", async () => {
    const state = installSidecar();
    state.pushTest = () => {
      throw JSON.stringify({
        code: "env_var_missing",
        path: "params.channel",
        message: "环境变量 FEISHU_BOT_TOKEN 未设置",
      });
    };
    renderScreen();
    await openSection("push");

    fireEvent.click(screen.getByRole("button", { name: "发送测试" }));
    expect(await screen.findByText("通道失败")).toBeTruthy();
    const note = screen.getByTestId("push-test-result");
    expect(note.textContent).toContain("env_var_missing");
    expect(note.textContent).toContain("FEISHU_BOT_TOKEN");
  });
});

// ---------------------------------------------------------------------------
// D4 结构重做(10-03-ui-deep-imitation,对照 teardown-linear-settings 第 1/2/5/6
// 条):左分区导航(当前项高亮)+ 右侧每子区一屏(区标题+描述+卡片列)+ URL
// ?section= 驱动深链 + 危险区 Destructive Card 隔离。
// ---------------------------------------------------------------------------

describe("设置:分区导航与危险区(D4 结构重做)", () => {
  it("四分区导航齐(通用/推送/视觉/系统);缺省进通用,通用卡直见而他区卡不挂载", async () => {
    installSidecar();
    renderScreen();

    // 79f7f7b 分区 6→4:general/push/vision/system(update/advanced 已并)
    for (const id of ["general", "push", "vision", "system"]) {
      expect(screen.getByTestId(`settings-nav-${id}`)).toBeTruthy();
    }
    // 当前项高亮:aria-current 打在通用上
    expect(screen.getByTestId("settings-nav-general").getAttribute("aria-current")).toBe("true");
    expect(screen.getByTestId("settings-nav-vision").getAttribute("aria-current")).toBeNull();
    // 每子区一屏:通用区可见(LLM 表单),看图/系统卡未挂载
    expect(screen.getByTestId("settings-section-general")).toBeTruthy();
    expect(screen.getByLabelText("base_url")).toBeTruthy();
    expect(screen.queryByLabelText("本地 base_url")).toBeNull(); // VisionForm 未挂载
    expect(screen.queryByTestId("updater-status")).toBeNull(); // UpdaterCard 未挂载(其 idle 态无 status 节点,双保险)
    expect(screen.queryByTestId("settings-danger-zone")).toBeNull(); // 危险区不在通用
  });

  it("点导航切区:右列换屏 + aria-current 随迁;视觉区挂 VisionForm 两卡所需表单", async () => {
    mocks.invoke.mockImplementation(async (_command: string, args: { method: string }) => {
      if (args.method === "secret.list") return { names: [] };
      if (args.method === "doctor") return doctorFixture();
      if (args.method === "image.config.read") {
        return {
          file: "/home/vision.yaml",
          exists: true,
          config: {
            channel_default: "local",
            local: { base_url: "http://127.0.0.1:8080/v1", model: "" },
            cloud: { base_url: "https://open.bigmodel.cn/api/paas/v4", model: "glm-4.6v", api_key: null },
            ocr: { enabled: true, engine_default: "vision" },
          },
        };
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
    });
    renderScreen();
    await screen.findByTestId("doctor-verify");

    await openSection("vision");
    expect(screen.getByTestId("settings-section-vision")).toBeTruthy();
    expect(screen.queryByTestId("settings-section-general")).toBeNull(); // 每子区一屏:通用卸载
    expect(screen.getByTestId("settings-nav-vision").getAttribute("aria-current")).toBe("true");
    await waitFor(() => {
      expect((screen.getByLabelText("本地 base_url") as HTMLInputElement).value).toBe("http://127.0.0.1:8080/v1");
    });
    // 区标题+描述在位(拆解表第 2 条)
    expect(screen.getByRole("heading", { level: 2, name: "视觉" })).toBeTruthy();
  });

  it("URL ?section= 深链:直进系统区(sidecar 连接+软件更新卡直见,通用屏不挂载)", async () => {
    installSidecar();
    renderScreen("/settings?section=system");

    // 直进系统区:分区屏挂载 + 区标题 + 导航高亮随迁
    expect(screen.getByTestId("settings-section-system")).toBeTruthy();
    expect(screen.queryByTestId("settings-section-general")).toBeNull();
    expect(screen.getByTestId("settings-nav-system").getAttribute("aria-current")).toBe("true");
    expect(screen.getByRole("heading", { level: 2, name: "系统" })).toBeTruthy();
    // 系统区实锚:sidecar 核心进程卡(79f7f7b 后系统区 = sidecar + 更新)
    expect(await screen.findByText("sidecar 核心进程")).toBeTruthy();
  });

  it("非法 ?section= 值回落通用分区(不白屏)", async () => {
    installSidecar();
    renderScreen("/settings?section=nonsense");
    expect(screen.getByTestId("settings-section-general")).toBeTruthy();
    expect(screen.getByLabelText("base_url")).toBeTruthy();
  });

  it("每区保存态反馈在卡片底栏:保存中禁用按钮,成功后 save-status 留在本卡", async () => {
    let releaseSave: (() => void) | null = null;
    mocks.invoke.mockImplementation(async (_command: string, args: { method: string; params?: unknown }) => {
      if (args.method === "doctor") return doctorFixture();
      if (args.method === "secret.list") return { names: [] };
      if (args.method === "secret.set") {
        await new Promise<void>((resolve) => {
          releaseSave = resolve; // 挂起保存,冻结「保存中」态供断言
        });
        const { name, value } = args.params as SecretSetParams;
        return { name, stored: value.length > 0 };
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: "x" });
    });
    renderScreen();
    await typeByLabel("base_url", "https://api.example.com");
    const save = screen.getByRole("button", { name: "保存 LLM 凭据" }) as HTMLButtonElement;
    fireEvent.click(save);
    // 保存中:按钮禁用 + 行内保存中文案(role=status)
    await screen.findByText("保存中…");
    expect((screen.getByRole("button", { name: "保存 LLM 凭据" }) as HTMLButtonElement).disabled).toBe(true);
    (releaseSave as (() => void) | null)?.();
    const status = await screen.findByTestId("save-status");
    expect(status.textContent).toContain("myia/llm/base_url");
    expect(status.closest("[data-slot='card']")?.textContent).toContain("LLM 精评"); // 反馈留在本卡底栏
  });
});

// ---------------------------------------------------------------------------
// 分区过滤(10-04-interaction-batch 补做,census 缺口 #7「设置搜索设置项」:
// Linear settings 口径——分区导航上方过滤框实时过滤分区名,纯前端零 RPC;
// 只影响导航可见性,不改当前分区/URL 深链语义)。
// ---------------------------------------------------------------------------

describe("设置:分区过滤(census #7 补做,纯前端实时)", () => {
  it("输入「推」→ 导航只剩推送;过滤不改当前分区(右侧仍通用,内容不换不白屏)", async () => {
    installSidecar();
    renderScreen();

    fireEvent.change(screen.getByLabelText("过滤分区"), { target: { value: "推" } });
    expect(screen.getByTestId("settings-nav-push")).toBeTruthy();
    for (const id of ["general", "vision", "update", "advanced"]) {
      expect(screen.queryByTestId(`settings-nav-${id}`)).toBeNull();
    }
    // 只过滤导航:当前分区仍是缺省通用,base_url 表单照常在位
    expect(screen.getByTestId("settings-section-general")).toBeTruthy();
    expect(screen.getByLabelText("base_url")).toBeTruthy();
  });

  it("拉丁输入按 id 命中(vision→视觉)+ 大小写不敏感(PUSH 同命中)", async () => {
    installSidecar();
    renderScreen();

    fireEvent.change(screen.getByLabelText("过滤分区"), { target: { value: "vision" } });
    expect(screen.getByTestId("settings-nav-vision")).toBeTruthy();
    expect(screen.queryByTestId("settings-nav-general")).toBeNull();

    fireEvent.change(screen.getByLabelText("过滤分区"), { target: { value: "PUSH" } });
    expect(screen.getByTestId("settings-nav-push")).toBeTruthy();
    expect(screen.queryByTestId("settings-nav-vision")).toBeNull();
  });

  it("无匹配:导航全隐 + 「无匹配分区」提示,右侧仍渲染当前分区;清空即还原四区", async () => {
    installSidecar();
    renderScreen();

    fireEvent.change(screen.getByLabelText("过滤分区"), { target: { value: "xyz" } });
    for (const id of ["general", "push", "vision", "system"]) {
      expect(screen.queryByTestId(`settings-nav-${id}`)).toBeNull();
    }
    expect(screen.getByTestId("settings-section-filter-empty").textContent).toContain("无匹配分区");
    expect(screen.getByTestId("settings-section-general")).toBeTruthy(); // 不白屏

    fireEvent.change(screen.getByLabelText("过滤分区"), { target: { value: "" } });
    for (const id of ["general", "push", "vision", "system"]) {
      expect(screen.getByTestId(`settings-nav-${id}`)).toBeTruthy();
    }
    expect(screen.queryByTestId("settings-section-filter-empty")).toBeNull();
  });

  it("过滤与导航功能正交:过滤后剩余分区仍可点切区(aria-current 随迁)", async () => {
    installSidecar();
    renderScreen();

    // 「系」只命中「系统」(原「高」命中的「高级」区已在 6→4 收编中删除)
    fireEvent.change(screen.getByLabelText("过滤分区"), { target: { value: "系" } });
    await openSection("system");
    expect(screen.getByTestId("settings-section-system")).toBeTruthy();
    expect(screen.getByTestId("settings-nav-system").getAttribute("aria-current")).toBe("true");
  });
});

// ---------------------------------------------------------------------------
// 门槛件分区(10-05-plugin-market-batch 批二第 11 步):gates.get/save 三卡
// (付费通道 / 自有实例 / 分析件 D8 占位);知情警示文案铁律(design §6.4)
// + 值只经 secret.set 入钥匙链零回显 + third_party_trace 载荷保真透传(D9)
// ---------------------------------------------------------------------------

describe("设置:门槛件分区(gates)", () => {
  it("三卡渲染 + 知情文案在位;分析件=批三解锁占位(D8 非空面);官方件物化默认全关;挂载即 gates.get", async () => {
    installSidecar();
    renderScreen();
    await openSection("gates");

    expect(screen.getByTestId("settings-section-gates")).toBeTruthy();
    await screen.findByTestId("gates-paid-card");
    expect(screen.getByTestId("gates-platforms-card")).toBeTruthy();
    expect(screen.getByTestId("gates-analysis-card")).toBeTruthy();
    // 知情警示(design §6.4 文案铁律:每开关挂警示)
    expect(screen.getByTestId("gates-paid-card").textContent).toContain("按页计费");
    expect(screen.getByTestId("gates-paid-card").textContent).toContain("经对方服务器");
    expect(screen.getByTestId("gates-platforms-card").textContent).toContain("组织性不执法");
    // 分析件占位:批三解锁(D8:零分析件落地,但分区不是空面)
    expect(screen.getByTestId("gates-analysis-card").textContent).toContain("批三解锁");
    // 官方件物化(design §6.1 样例形状):zenrows/scraperapi/crawlab/worldmonitor
    // 四行齐,未配置 = 全关 + 规范钥匙串引用
    for (const name of ["zenrows", "scraperapi"]) {
      const row = screen.getByTestId(`gates-saas-row-${name}`);
      const toggle = within(row).getByRole("switch", { name: `付费引擎开关 ${name}` });
      expect(toggle.getAttribute("aria-checked")).toBe("false");
      expect(row.textContent).toContain(`myia/saas/${name}-key`);
    }
    for (const name of ["crawlab", "worldmonitor"]) {
      const row = screen.getByTestId(`gates-platform-row-${name}`);
      expect(
        within(row).getByRole("switch", { name: `自有实例开关 ${name}` }).getAttribute("aria-checked"),
      ).toBe("false");
    }
    expect(within(screen.getByTestId("gates-platform-row-crawlab")).queryByLabelText("crawlab Token 值")).toBeTruthy();
    expect(screen.queryByLabelText("worldmonitor Token 值")).toBeNull(); // worldmonitor 无凭据位(design §6.1)
    // 挂载即整读一次(gates.get);分析件占位零保存动作(D8)
    expect(callsOf("gates.get")).toHaveLength(1);
  });

  it("付费通道:总开关+逐件+key 值录入 → secret.set 入钥匙链 + gates.save 整份原子落盘;third_party_trace 透传不丢(D9)", async () => {
    const state = installSidecar();
    // CLI 设过的既有值:UI 不提供假开关(D9 无执法点),但保存载荷保真透传
    state.gates.third_party_trace = true;
    renderScreen();
    await openSection("gates");
    await screen.findByTestId("gates-paid-card");

    fireEvent.click(screen.getByRole("switch", { name: "付费通道总开关" }));
    fireEvent.click(screen.getByRole("switch", { name: "付费引擎开关 zenrows" }));
    await typeByLabel("zenrows API Key 值", "sk-zenrows-secret-value");
    fireEvent.click(screen.getByRole("button", { name: "保存付费通道" }));

    await screen.findByTestId("save-status");
    // key 值只经 secret.set 入规范名;值零回显、保存即清
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/saas/zenrows-key", value: "sk-zenrows-secret-value" });
    expect(state.secrets.get("myia/saas/zenrows-key")).toBe("sk-zenrows-secret-value");
    expect(document.body.textContent).not.toContain("sk-zenrows-secret-value");
    expect((screen.getByLabelText("zenrows API Key 值") as HTMLInputElement).value).toBe("");
    // gates.save:整份配置(总开关 + 逐件 + canonical 引用物化 + 透传 third_party_trace)
    expect(state.gatesSaved).not.toBeNull();
    expect(state.gatesSaved?.paid_engines).toBe(true);
    expect(state.gatesSaved?.third_party_trace).toBe(true);
    expect(state.gatesSaved?.saas.zenrows).toEqual({ enabled: true, api_key: "keychain:myia/saas/zenrows-key" });
    expect(state.gatesSaved?.saas.scraperapi).toEqual({ enabled: false, api_key: "keychain:myia/saas/scraperapi-key" });
    expect(state.gatesSaved?.platforms.crawlab).toEqual({
      enabled: false,
      endpoint: "",
      token: "keychain:myia/platforms/crawlab-token",
    });
    expect(state.gatesSaved?.analysis).toEqual({});
    expect(screen.getByTestId("save-status").textContent).toContain("myia/saas/zenrows-key");
  });

  it("自有实例:endpoint 非法前端拦零协议调用;改 https 后保存;token 值入钥匙链零回显", async () => {
    const state = installSidecar();
    renderScreen();
    await openSection("gates");
    await screen.findByTestId("gates-platforms-card");

    fireEvent.click(screen.getByRole("switch", { name: "自有实例开关 crawlab" }));
    await typeByLabel("crawlab endpoint", "ftp://crawlab.example.com");
    fireEvent.click(screen.getByRole("button", { name: "保存自有实例" }));

    // 前端同门校验(gates.py invalid_endpoint 口径):拦下,零 gates.save/secret.set
    expect(await screen.findByText(/endpoint 须为 http\(s\) 地址/)).toBeTruthy();
    expect(callsOf("gates.save")).toEqual([]);
    expect(state.gatesSaved).toBeNull();

    await typeByLabel("crawlab endpoint", "https://crawlab.example.com");
    await typeByLabel("crawlab Token 值", "tok-crawlab-private");
    fireEvent.click(screen.getByRole("button", { name: "保存自有实例" }));

    await screen.findByTestId("save-status");
    expect(state.gatesSaved?.platforms.crawlab).toEqual({
      enabled: true,
      endpoint: "https://crawlab.example.com",
      token: "keychain:myia/platforms/crawlab-token",
    });
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/platforms/crawlab-token", value: "tok-crawlab-private" });
    expect(document.body.textContent).not.toContain("tok-crawlab-private");
    expect((screen.getByLabelText("crawlab Token 值") as HTMLInputElement).value).toBe("");
  });

  it("gates.yaml 拒载 → 全关态仍可进(fail-closed 修复入口):警示卡 + 三卡照常渲染 + 保存后警示消除", async () => {
    const state = installSidecar();
    state.gatesGetError = {
      source: "/home/myia/gates.yaml",
      errors: [
        { path: "$", error_type: "unknown_field", message: "存在未知字段: ['oops'](允许:[…];手滑字段名不会静默失效)" },
      ],
    };
    renderScreen();
    await openSection("gates");

    // 拒载如实上屏(结构化明细),但设置屏是修复入口:三卡仍可编辑(全关默认态)
    const warn = await screen.findByTestId("gates-corrupt-warning");
    expect(warn.textContent).toContain("fail-closed");
    expect(warn.textContent).toContain("unknown_field");
    expect(screen.getByTestId("gates-paid-card")).toBeTruthy();
    expect(screen.getByTestId("gates-platforms-card")).toBeTruthy();
    expect(
      within(screen.getByTestId("gates-paid-card")).getByRole("switch", { name: "付费通道总开关" }).getAttribute("aria-checked"),
    ).toBe("false");

    // 保存任一卡 = 合法覆写修复
    fireEvent.click(screen.getByRole("switch", { name: "付费通道总开关" }));
    fireEvent.click(screen.getByRole("button", { name: "保存付费通道" }));
    await waitFor(() => {
      expect(screen.queryByTestId("gates-corrupt-warning")).toBeNull();
    });
    expect(state.gatesSaved?.paid_engines).toBe(true);
  });

  it("gates.get 未达(传输/协议层错误)→ 整屏结构化错误卡,不渲染表单", async () => {
    mocks.invoke.mockImplementation(async (_command: string, args: { method: string }) => {
      if (args.method === "doctor") return doctorFixture();
      if (args.method === "secret.list") return { names: [] };
      if (args.method === "gates.get") {
        throw JSON.stringify({
          code: "method_not_found",
          path: "method",
          message: "未知方法 gates.get",
        });
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
    });
    renderScreen();
    await openSection("gates");

    const card = await screen.findByTestId("gates-load-error");
    const box = await within(card).findByRole("alert");
    expect(box.textContent).toContain("method_not_found");
    // 协议面缺失:不出可编辑表单(与拒载 fail-closed 分支不同)
    expect(screen.queryByTestId("gates-paid-card")).toBeNull();
    expect(screen.queryByTestId("gates-platforms-card")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// Python 运行环境分区(10-05-desktop-managed-py-env 第 4 步,D1/D2):导航可达
// + 深链落点(D2 引导空态「一键跳设置」指向 ?section=python-env)。IPC 契约与
// 行为面(开始配置/双镜像/明细/同步依赖)全覆盖在 pyenv-card.test.tsx。
// ---------------------------------------------------------------------------

describe("设置:Python 运行环境分区(python-env)", () => {
  it("导航含「Python 环境」;深链 ?section=python-env 挂载 PyenvCard 并拉取 pyenv_get_status", async () => {
    installSidecar();
    renderScreen("/settings?section=python-env");

    expect(screen.getByTestId("settings-section-python-env")).toBeTruthy();
    expect(screen.getByRole("heading", { level: 2, name: "Python 运行环境" })).toBeTruthy();
    expect(screen.getByTestId("settings-nav-python-env").getAttribute("aria-current")).toBe("true");
    await screen.findByTestId("pyenv-card");
    // 挂载即拉取(契约:前端初始化以 pyenv_get_status 为准,事件只作变更通知)
    const pyenvCalls = mocks.invoke.mock.calls.filter(([command]) => command === "pyenv_get_status");
    expect(pyenvCalls.length).toBe(1);
    expect(await screen.findByTestId("pyenv-state-badge")).toBeTruthy();
    // 缺省分区(通用)不挂载本卡:零额外 IPC
  });

  it("缺省分区不拉取 pyenv(卡未挂载零 IPC);导航点击可进「Python 环境」区", async () => {
    installSidecar();
    renderScreen();
    await screen.findByTestId("doctor-verify");
    expect(screen.queryByTestId("pyenv-card")).toBeNull();
    expect(
      mocks.invoke.mock.calls.filter(([command]) => command === "pyenv_get_status").length,
    ).toBe(0);

    await openSection("python-env");
    expect(screen.getByTestId("settings-section-python-env")).toBeTruthy();
    expect(await screen.findByTestId("pyenv-card")).toBeTruthy();
  });
});
