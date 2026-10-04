// @vitest-environment jsdom
//
// 源管理组件测试:mock sidecar(壳命令 sidecar_request 的 JS 假实现,
// 内存态模拟品类 YAML 的 sources 名单),覆盖:表格渲染与健康度三色 /
// 排序筛选分页 / 启停写回+doctor 往返复核 / 写回失败结构化错误态 / 空态 / 加载错误态 /
// 行动作「编辑」当场弹出 YAML 编辑对话框并加载该文件原文(不离开本屏)。
// 协议缺口(method_not_found)也是被测行为之一 —— sources.write 未收编前如实呈现。
// D4(10-03-ui-deep-imitation)结构性重做另测:渲染层迁 ui/table 基件(compact
// 36px 行密度/colgroup 定宽)、列宽拖拽(Ant Table 手感:拖右缘手柄实时改宽,
// 手柄点击不误触排序)、健康徽章四态语义(dot+文字)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
// C13(10-03-v112-desktop-parity):test.completed 事件经 onSidecarEvent(listen)
// 回屏 —— 捕获 handler 供用例回放事件载荷
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));
// 编辑器替身:受控 textarea(弹窗内 CodeMirror 以同款契约替身;真实渲染见
// yaml-editor/editor-pane.test.tsx)
vi.mock("@uiw/react-codemirror", () => ({
  default: (props: { value?: string; onChange?: (value: string) => void }) => (
    <textarea
      aria-label="yaml-source"
      value={props.value ?? ""}
      onChange={(event) => props.onChange?.(event.target.value)}
    />
  ),
}));

import { SourcesScreen } from "./sources-screen";
import type { DoctorResult, DoctorPluginReport, HealthResult, PluginReport, SourceReport, SourceHealthState } from "@/lib/api";

const FILE = "plugins/ai-news.yaml";
/** 写回/复核/读原文断言用完整路径:pluginFile 是回传 sidecar 的协议键(yaml.read
 * 围栏/sources.write 直开都按路径解析;5c188c0 截短名曾致 path_outside_root 回归,
 * 2026-10-05 冒烟抓获后恢复绝对路径,显示层自行 split("/").pop()) */

// ---------------------------------------------------------------------------
// 协议夹具(形状逐字段对照 src/lib/api/types.ts / desktop/entry.py)
// ---------------------------------------------------------------------------

function sourceReport(name: string, state: SourceHealthState, url = `https://example.com/${name}`): SourceReport {
  return {
    name,
    url,
    engine: "static_html",
    engine_hint: null,
    health: {
      state,
      reason: `评判原因:${state}`,
      observed: 3,
      latest: { run_id: 7, run_status: "success", item_count: 2, skip_reason: null, failed: false },
      baseline: 2,
    },
    fingerprint_skips: { observed: 5, skipped: 1 },
  };
}

function pluginReport(file: string, id: string, sources: SourceReport[]): PluginReport {
  return {
    file,
    id,
    name: `品类 ${id}`,
    schedule: "*/15 * * * *",
    timezone: "Asia/Shanghai",
    push_channels: ["feishu_card"],
    loaded: true,
    load_errors: null,
    sources,
  };
}

function healthResult(plugins: PluginReport[]): HealthResult {
  const counts = { ok: 0, degraded: 0, dead: 0, unknown: 0 };
  let sources = 0;
  for (const plugin of plugins) {
    sources += plugin.sources.length;
    for (const source of plugin.sources) counts[source.health.state] += 1;
  }
  return {
    command: "list",
    plugins_dir: "plugins",
    db: "myssia.db",
    store_error: null,
    plugins,
    summary: { plugins: plugins.length, sources, ...counts },
    healthy: counts.dead === 0,
    exit_code: 0,
  };
}

function doctorResult(file: string, sourceNames: string[]): DoctorResult {
  const plugin: DoctorPluginReport = {
    ...pluginReport(file, "ai-news", sourceNames.map((name) => sourceReport(name, "ok"))),
    next_fire_at: null,
    enrich: null,
  };
  return {
    command: "doctor",
    generated_at: "2026-10-02T10:00:00.000Z",
    db: "myssia.db",
    healthy: true,
    plugins: [plugin],
    credentials: { backend_available: true, backend_error: null, entries: [] },
    proxy: { config: null, pools: [] },
    findings: [],
    summary: { plugins: 1, sources: sourceNames.length, errors: 0, warnings: 0 },
  };
}

// ---------------------------------------------------------------------------
// mock sidecar:内存态 = 品类 YAML 的 sources 名单 + 停用暂存
// ---------------------------------------------------------------------------

type Handler = (params: never) => unknown;
type SidecarMap = Record<string, Handler>;

function okSidecar(initialSources: string[]) {
  const state = {
    enabled: [...initialSources],
    disabled: new Set<string>(),
  };
  const map: SidecarMap = {
    health: () =>
      healthResult([pluginReport(FILE, "ai-news", state.enabled.map((name) => sourceReport(name, "ok")))]),
    "yaml.read": (params: never) => {
      const { file } = params as { file: string };
      return {
        file,
        content: `# 原文注释:逐字节保真\nid: ai-news\nname: AI 新闻\nschedule: "*/15 * * * *"\n`,
        size: 64,
        mtime: 111.5,
      };
    },
    "yaml.save": (params: never) => {
      const { file } = params as { file: string };
      return { file, written: true, created: false, backed_up: `${file}.bak`, mtime: 222.25, warnings: [] };
    },
    "sources.write": (params: never) => {
      const { file, enable = [], disable = [] } = params as {
        file: string;
        enable?: string[];
        disable?: string[];
      };
      for (const name of disable) {
        state.enabled = state.enabled.filter((candidate) => candidate !== name);
        state.disabled.add(name);
      }
      for (const name of enable) {
        if (!state.enabled.includes(name)) state.enabled.push(name);
        state.disabled.delete(name);
      }
      return { file, written: true, enabled: [...state.enabled], disabled: [...state.disabled] };
    },
    doctor: (params: never) => {
      const { yamls } = params as { yamls?: string[] };
      const file = yamls?.[0] ?? FILE;
      return doctorResult(file, state.enabled);
    },
  };
  return { map, state };
}

/** 安装 mock sidecar:所有 invoke("sidecar_request") 走此分派;未知方法=结构化 404 */
function installSidecar(map: SidecarMap): void {
  mocks.invoke.mockImplementation(
    async (_command: string, args: { method: string; params?: unknown }) => {
      const handler = map[args.method];
      if (!handler) {
        throw JSON.stringify({
          code: "method_not_found",
          path: "method",
          message: `未知方法 ${args.method}`,
          data: { allowed: Object.keys(map).sort() },
        });
      }
      return handler(args.params as never);
    },
  );
}

function lastCall(method: string): { params: unknown } | undefined {
  const calls = mocks.invoke.mock.calls.filter(([, args]) => (args as { method: string }).method === method);
  return calls.at(-1)?.[1] as { params: unknown } | undefined;
}

function callCount(method: string): number {
  return mocks.invoke.mock.calls.filter(([, args]) => (args as { method: string }).method === method).length;
}

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
  // 缺省:订阅即成功、零事件(C13 用例再覆盖捕获 handler);绝不能返回
  // undefined —— 屏内 onSidecarEvent(...).then 会炸
  mocks.listen.mockImplementation(async () => () => undefined);
});
afterEach(() => {
  cleanup(); // vitest 非 globals 模式下 RTL 不自动清理,防 DOM 跨测试污染
  vi.clearAllMocks();
});

// ---------------------------------------------------------------------------

describe("源管理:表格渲染与健康度三色", () => {
  it("health 数据扁平成行:源名/URL/引擎/健康度徽标齐备", async () => {
    const { map } = okSidecar(["hacker-news", "rsshub"]);
    map.health = () =>
      healthResult([
        pluginReport(FILE, "ai-news", [
          sourceReport("hacker-news", "ok"),
          sourceReport("rsshub", "degraded"),
          sourceReport("slow-site", "dead"),
        ]),
      ]);
    installSidecar(map);

    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );

    expect(await screen.findByText("hacker-news")).toBeTruthy();
    expect(screen.getByText("https://example.com/rsshub")).toBeTruthy();
    expect(screen.getAllByText("static_html").length).toBeGreaterThan(0);
    // 三色徽标:正常(绿)/退化(琥珀)/失效(红);data-health 钉住语义,
    // 与筛选 chips(同名文案按钮)区分
    expect(document.querySelector("[data-health='ok']")?.textContent).toBe("正常");
    expect(document.querySelector("[data-health='degraded']")?.textContent).toBe("退化");
    expect(document.querySelector("[data-health='dead']")?.textContent).toBe("失效");
  });
});

describe("源管理:排序/筛选/分页", () => {
  function manyRowsSidecar() {
    const { map, state } = okSidecar([]);
    const names = Array.from({ length: 12 }, (_, index) => `source-${String(index).padStart(2, "0")}`);
    map.health = () =>
      healthResult([pluginReport(FILE, "ai-news", names.map((name) => sourceReport(name, "ok")))]);
    state.enabled = names;
    return { map, state, names };
  }

  it("12 行分两页;下一页/上一页翻动;筛选即时收窄", async () => {
    installSidecar(manyRowsSidecar().map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("source-00")).toBeTruthy();
    expect(screen.getByText(/共 12 行/)).toBeTruthy();
    expect(screen.getByText("第 1 / 2 页")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "下一页" }));
    expect(screen.getByText("第 2 / 2 页")).toBeTruthy();
    expect(screen.queryByText("source-00")).toBeNull();
    expect(screen.getByText("source-11")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "上一页" }));
    const filter = screen.getByLabelText("全局筛选") as HTMLInputElement;
    fireEvent.change(filter, { target: { value: "source-1" } });
    await waitFor(() => {
      expect(screen.getByText(/共 2 行/)).toBeTruthy(); // 00..11 中含 "source-1" 的只有 10/11
    });
    expect(screen.queryByText(/^source-0/)).toBeNull();
  });

  it("点列头排序(URL 升序),健康度 chips 过滤;排序控件为原生 button(Tab 可聚焦,Enter/Space 触发)", async () => {
    const { map } = okSidecar(["beta", "alpha"]);
    map.health = () =>
      healthResult([
        pluginReport(FILE, "ai-news", [
          sourceReport("beta", "ok", "https://example.com/beta"),
          sourceReport("alpha", "dead", "https://example.com/alpha"),
        ]),
      ]);
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("beta")).toBeTruthy();

    const urlHeader = screen.getByRole("columnheader", { name: /URL/ });
    // 键盘可达(P1):排序控件 = 列头内原生 button(type=button,默认 Tab 可聚焦;
    // Enter/Space 由 UA 合成 click —— jsdom 不模拟该合成,故此处以 focus 可达 +
    // click(即键盘激活的最终事件)断言同一 handler 生效)
    const sortButton = urlHeader.querySelector("button");
    expect(sortButton instanceof HTMLButtonElement).toBe(true);
    expect((sortButton as HTMLButtonElement).type).toBe("button");
    expect((sortButton as HTMLButtonElement).tabIndex).toBe(0);
    (sortButton as HTMLButtonElement).focus();
    expect(document.activeElement).toBe(sortButton);

    fireEvent.click(sortButton as HTMLButtonElement);
    expect(urlHeader.getAttribute("aria-sort")).toBe("ascending");
    const firstRowUrl = screen.getAllByText(/https:\/\/example\.com\//)[0];
    expect(firstRowUrl.textContent).toContain("alpha");

    fireEvent.click(screen.getByRole("button", { name: "失效" }));
    await waitFor(() => {
      expect(screen.getByText(/共 1 行/)).toBeTruthy();
    });
    expect(screen.queryByText("beta")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "全部" }));
    await waitFor(() => {
      expect(screen.getByText("beta")).toBeTruthy();
    });
  });
});

describe("源管理:启停写回 + doctor 往返复核", () => {
  it("停用:写回 sources.write(disable) → doctor(yamls) 复核一致 → 行随刷新消失并进停用区", async () => {
    const { map, state } = okSidecar(["hacker-news", "rsshub"]);
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("hacker-news")).toBeTruthy();

    fireEvent.click(screen.getByRole("switch", { name: "停用 hacker-news" }));

    expect(await screen.findByTestId("roundtrip-ok")).toBeTruthy();
    expect(screen.getByTestId("roundtrip-ok").textContent).toContain("已停用 hacker-news");
    expect(screen.getByTestId("roundtrip-ok").textContent).toContain("doctor 复核往返一致");

    // 写回参数:品类文件 + disable 名单;复核用 doctor(yamls:[file])——均走 API 层短名口径
    expect(lastCall("sources.write")?.params).toEqual({ file: FILE, disable: ["hacker-news"] });
    expect(lastCall("doctor")?.params).toEqual({ yamls: [FILE] });
    // mock 内存态(YAML 代理)真的变了;刷新后表格行消失(URL 唯一,停用区不含 URL)、进「已停用」区
    expect(state.enabled).toEqual(["rsshub"]);
    await waitFor(() => {
      expect(screen.queryByText("https://example.com/hacker-news")).toBeNull();
    });
    expect(screen.getByText("本次会话已停用(1)")).toBeTruthy();
  });

  it("再启用:停用区按钮写回 enable → doctor 复核一致 → 行回到表格", async () => {
    const { map } = okSidecar(["hacker-news"]);
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("hacker-news")).toBeTruthy();
    fireEvent.click(screen.getByRole("switch", { name: "停用 hacker-news" }));
    await screen.findByTestId("roundtrip-ok");

    fireEvent.click(screen.getByRole("button", { name: /^启用$/ }));
    const okBanner = await screen.findByTestId("roundtrip-ok");
    expect(okBanner.textContent).toContain("已启用 hacker-news");
    expect(lastCall("sources.write")?.params).toEqual({ file: FILE, enable: ["hacker-news"] });
    await waitFor(() => {
      expect(screen.getByText("hacker-news")).toBeTruthy();
    });
  });

  it("协议缺口:sidecar 无 sources.write → 结构化 method_not_found 错误态,开关不动", async () => {
    const { map } = okSidecar(["hacker-news"]);
    const withoutWrite: SidecarMap = { health: map.health, doctor: map.doctor };
    installSidecar(withoutWrite);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("hacker-news")).toBeTruthy();

    fireEvent.click(screen.getByRole("switch", { name: "停用 hacker-news" }));

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("未知方法 sources.write");
    expect(alert.textContent).toContain("code=method_not_found");
    expect(alert.textContent).toContain("sidecar 协议尚无此方法");
    // 失败即回滚呈现:开关仍可点(未写入),无「往返一致」假象
    expect(screen.queryByTestId("roundtrip-ok")).toBeNull();
    expect(screen.getByRole("switch", { name: "停用 hacker-news" })).toBeTruthy();
  });
});

describe("源管理:空态与错误态", () => {
  it("无插件 → 首跑引导态(Kestra 空态+一键 demo)", async () => {
    const { map } = okSidecar([]);
    map.health = () => healthResult([]);
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    /* 10-04-ui-kestra-anchor:零品类 YAML = 引导态,不再是死文案空态 */
    expect(await screen.findByText("还没有品类源")).toBeTruthy();
    expect(screen.getByText(/插件目录\(plugins\)下没有可加载的品类 YAML/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "一键跑 demo" })).toBeTruthy();
    expect(screen.getByTestId("first-run-guide")).toBeTruthy();
    expect(screen.getByText("需要指引?")).toBeTruthy();
  });

  it("一键跑 demo:模板落盘 + run.start + 完成态去日志屏(首跑引导闭环)", async () => {
    const { map } = okSidecar([]);
    map.health = () => healthResult([]);
    let savedFile = "";
    let savedContent = "";
    map["yaml.template"] = () => ({ content: "id: my-category\nsources: []\n" });
    map["yaml.save"] = (params: never) => {
      const { file, content } = params as { file: string; content: string };
      savedFile = file;
      savedContent = content;
      return { file, created: true, warnings: [], doctor: { ok: true, message: "doctor ok" } };
    };
    map["run.start"] = (params: never) => {
      expect((params as { yaml: string }).yaml).toBe(savedFile);
      return { run_id: 42 };
    };
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    fireEvent.click(await screen.findByRole("button", { name: "一键跑 demo" }));
    const started = await screen.findByTestId("demo-started");
    expect(started.textContent).toContain("run #42");
    expect(savedFile).toContain("myssia-demo.yaml");
    // 模板 id 段替换为 demo stem(createDraft 同款文本手术)
    expect(savedContent).toContain("id: myssia-demo");
    // 完成态带日志屏深链(采集结果去向)
    expect(screen.getByRole("link", { name: "去日志屏查看" })).toBeTruthy();
  });

  it("sidecar 不可用 → 结构化错误(code/path)+ 重试", async () => {
    mocks.invoke.mockImplementation(async () => {
      throw JSON.stringify({ code: "sidecar_not_running", path: "$", message: "sidecar 进程未运行" });
    });
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("sidecar 进程未运行");
    expect(alert.textContent).toContain("code=sidecar_not_running");
    expect(alert.textContent).toContain("path=$");
    // 重试走同一 mock(仍失败,但按钮行为可达)
    fireEvent.click(screen.getByRole("button", { name: "重试" }));
    await waitFor(() => {
      expect(mocks.invoke.mock.calls.length).toBeGreaterThanOrEqual(2);
    });
  });

  it("行动作「编辑」:当场弹出编辑对话框并加载该品类文件原文(不离开源管理屏)", async () => {
    const { map } = okSidecar(["hacker-news"]);
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("hacker-news")).toBeTruthy();

    // 编辑改为弹窗:不再是跳转链接
    expect(screen.queryByRole("link", { name: "编辑" })).toBeNull();

    fireEvent.click(screen.getByRole("button", { name: "编辑" }));

    // 模态对话框出现(遮罩 + role=dialog aria-modal),编辑器加载该文件原文
    const dialog = await screen.findByRole("dialog");
    expect(dialog.getAttribute("aria-modal")).toBe("true");
    expect(dialog.getAttribute("aria-label")).toContain("ai-news.yaml");
    await waitFor(() => {
      expect((screen.getByLabelText("yaml-source") as HTMLTextAreaElement).value).toContain("id: ai-news");
    });
    expect(lastCall("yaml.read")?.params).toEqual({ file: FILE });

    // 弹窗内保存成功 → 表格数据刷新(health 二次拉取,防编辑后展示陈旧行)
    fireEvent.change(screen.getByLabelText("yaml-source"), {
      target: { value: "# 改稿\nid: ai-news\nname: AI 新闻\nschedule: \"0 9 * * *\"\n" },
    });
    fireEvent.click(screen.getByRole("button", { name: /保存/ }));
    expect(await screen.findByTestId("save-ok")).toBeTruthy();
    await waitFor(() => {
      expect(callCount("health")).toBe(2);
    });

    // 保存后干净态关闭:ESC 直接关
    fireEvent.keyDown(window, { key: "Escape" });
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).toBeNull();
    });
  });
});

// ---------------------------------------------------------------------------
// C13(10-03-v112-desktop-parity):行「试抓」(sources.test 异步 job →
// test.completed 详情弹窗;10-05-test-result-dialog 撤贴顶横幅改模态)
// ---------------------------------------------------------------------------

describe("源管理:试抓此源(C13 → 详情弹窗)", () => {
  type EventHandler = (event: { payload: Record<string, unknown> }) => void;

  function installEvents() {
    let handler: EventHandler | null = null;
    mocks.listen.mockImplementation(async (_name: string, fn: EventHandler) => {
      handler = fn;
      return () => undefined;
    });
    return {
      emit: (payload: Record<string, unknown>) => handler?.({ payload }),
    };
  }

  it("完成即弹详情弹窗:概要/指纹判定/退化链/条目预览吃满结构化报文;ESC 关闭", async () => {
    const events = installEvents();
    const { map } = okSidecar(["local-api"]);
    map["sources.test"] = (params: never) => {
      const { source } = params as { file: string; source: string };
      return { job_id: 7, state: "running", source };
    };
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );

    await screen.findByText("local-api");
    fireEvent.click(screen.getByRole("button", { name: "试抓 local-api" }));
    // pluginFile = 完整路径回传协议(短名回归修复);试抓参数随行原样
    await waitFor(() =>
      expect(lastCall("sources.test")?.params).toEqual({ file: FILE, source: "local-api" }),
    );
    // 进行中态 = 行内试抓钮锚点(提示实时输出见日志屏);不再有「异步 job #N」横幅
    const running = await screen.findByTestId("test-running");
    expect(running.getAttribute("title")).toBe("试抓进行中,实时输出见日志屏");
    expect(document.body.textContent ?? "").not.toContain("job #");

    events.emit({
      type: "test.completed",
      job_id: 7,
      ok: true,
      exit_code: 0,
      result: {
        command: "test",
        sources: [
          {
            source: "local-api",
            url: "https://example.com/local-api",
            engine: "direct_api",
            engine_configured: "auto",
            ok: true,
            item_count: 3,
            failures: [
              {
                source: "local-api",
                engine: "static_html",
                url: "https://example.com/local-api",
                error_type: "network",
                message: "引擎链第一跳网络失败,已退化",
              },
            ],
            fingerprint: {
              skip_reason: null,
              verdict: "changed_or_first_fetch",
              meaning: "内容有变化或首次抓取,线上调度会正常提取",
            },
            items: [
              { fields: { title: "第一条", url: "https://example.com/a" }, dedup_key: "sha:aaa" },
              { fields: { title: "第二条" }, dedup_key: null, dedup_key_error: "模板缺字段 link" },
            ],
            items_truncated: true,
          },
        ],
      },
      ts: "2026-10-03T08:00:00+00:00",
    });

    // 模态弹窗自动弹出(role=dialog aria-modal),贴屏顶横幅已撤
    const dialog = await screen.findByRole("dialog");
    expect(dialog.getAttribute("aria-modal")).toBe("true");
    expect(dialog.getAttribute("aria-label")).toBe("试抓结果 local-api");
    expect(screen.getByTestId("test-result-status").textContent).toBe("成功");
    const text = dialog.textContent ?? "";
    // 概要:引擎命中 / 配置引擎 / 条数
    expect(text).toContain("direct_api");
    expect(text).toContain("auto");
    expect(text).toContain("3 条");
    // 指纹判定全文
    expect(text).toContain("内容有变化或首次抓取,线上调度会正常提取");
    // 引擎退化链逐条
    expect(text).toContain("static_html");
    expect(text).toContain("network");
    expect(text).toContain("引擎链第一跳网络失败,已退化");
    // 条目预览:dedup_key + 字段「k = v」+ 求值失败如实 + 截断标记
    const items = screen.getByTestId("test-result-items");
    const itemsText = items.textContent ?? "";
    expect(itemsText).toContain("sha:aaa");
    expect(itemsText).toContain("title = 第一条");
    expect(itemsText).toContain("模板缺字段 link");
    expect(itemsText).toContain("仅预览前 2 条");
    // 底部深链:查看采集日志
    expect(screen.getByRole("link", { name: "查看采集日志" }).getAttribute("href")).toBe("#/logs");
    // job 收尾:进行中锚点撤
    expect(screen.queryByTestId("test-running")).toBeNull();
    // 旧贴顶横幅 testid 清零(复查 L:AC1 后半的显式反向断言)
    expect(screen.queryByTestId("test-result-ok")).toBeNull();
    expect(screen.queryByTestId("test-result-fail")).toBeNull();

    // ESC 关闭(只读无 dirty 守卫)
    fireEvent.keyDown(window, { key: "Escape" });
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).toBeNull();
    });
  });

  it("失败形:事件 ok=false → error 族+data.errors 逐条入弹窗;发起被拒(test_busy)同弹窗;遮罩/X 均可关", async () => {
    const events = installEvents();
    const { map } = okSidecar(["local-api"]);
    map["sources.test"] = () => ({ job_id: 9, state: "running", source: "local-api" });
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );

    await screen.findByText("local-api");
    fireEvent.click(screen.getByRole("button", { name: "试抓 local-api" }));
    await screen.findByTestId("test-running");
    events.emit({
      type: "test.completed",
      job_id: 9,
      ok: false,
      exit_code: 1,
      error: "config",
      data: { error: "config", errors: [{ path: "$.sources", message: "源 'x' 不存在" }] },
      ts: "2026-10-03T08:00:00+00:00",
    });

    const dialog = await screen.findByTestId("test-result-dialog");
    expect(screen.getByTestId("test-result-status").textContent).toBe("失败");
    const text = dialog.textContent ?? "";
    expect(text).toContain("config");
    expect(text).toContain("$.sources:源 'x' 不存在");

    // 遮罩点击关闭
    fireEvent.click(screen.getByTestId("test-result-overlay"));
    await waitFor(() => {
      expect(screen.queryByTestId("test-result-dialog")).toBeNull();
    });

    // 发起失败(test_busy 单飞)→ 同一弹窗失败形,不静默
    map["sources.test"] = () => {
      throw JSON.stringify({
        code: "test_busy",
        path: "$",
        message: "已有试抓在执行 job_id=9(单飞)",
        data: { active_job_id: 9 },
      });
    };
    fireEvent.click(screen.getByRole("button", { name: "试抓 local-api" }));
    const busy = await screen.findByTestId("test-result-dialog");
    expect(busy.textContent).toContain("test_busy");
    expect(busy.textContent).toContain("已有试抓在执行");

    // X 关闭钮
    fireEvent.click(screen.getByRole("button", { name: "关闭对话框" }));
    await waitFor(() => {
      expect(screen.queryByTestId("test-result-dialog")).toBeNull();
    });
  });

  it("编辑模态在途时试抓完成:不叠双模态,关闭编辑后结果弹窗自然浮现(复查 M)", async () => {
    const events = installEvents();
    const { map } = okSidecar(["local-api"]);
    map["sources.test"] = () => ({ job_id: 11, state: "running", source: "local-api" });
    installSidecar(map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );

    await screen.findByText("local-api");
    fireEvent.click(screen.getByRole("button", { name: "试抓 local-api" }));
    await screen.findByTestId("test-running");

    // 编辑模态先开(行编辑钮;未改稿干净态,ESC 直关无 dirty confirm)
    fireEvent.click(screen.getByRole("button", { name: "编辑" }));
    expect(await screen.findByTestId("yaml-editor-dialog")).toBeTruthy();

    // 试抓于编辑在途时完成:不叠双模态(同 z-50 叠底 + ESC 双关会静默丢结果)
    events.emit({
      type: "test.completed",
      job_id: 11,
      ok: true,
      exit_code: 0,
      result: {
        command: "test",
        sources: [
          {
            source: "local-api",
            engine: "direct_api",
            engine_configured: "auto",
            ok: true,
            item_count: 1,
            failures: [],
            fingerprint: {
              skip_reason: null,
              verdict: "changed_or_first_fetch",
              meaning: "内容有变化或首次抓取,线上调度会正常提取",
            },
          },
        ],
      },
      ts: "2026-10-03T08:00:00+00:00",
    });
    expect(screen.queryByTestId("test-result-dialog")).toBeNull();

    // 关闭编辑弹窗(ESC)→ 结果弹窗自然浮现,结果未丢
    fireEvent.keyDown(window, { key: "Escape" });
    const dialog = await screen.findByTestId("test-result-dialog");
    expect(dialog.textContent).toContain("direct_api");
    expect(dialog.textContent).toContain("内容有变化或首次抓取");
  });
});

// ---------------------------------------------------------------------------
// 排程一览 + 品类行「跑一次」用例已随功能迁至 cron-screen.test.tsx
// (2026-10-05,主人质疑「排程一览是什么意思?没在定时任务里面?」——
// 排程一览区块与行尾跑一次钮自源管理屏移至定时任务屏底部)
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// D4(10-03-ui-deep-imitation)结构性重做:ui/table 基件迁移 + 列宽拖拽 + 紧凑密度
// ---------------------------------------------------------------------------

describe("源管理:D4 表格基件迁移(ui/table + 列宽拖拽 + compact 密度)", () => {
  function twoRowsSidecar() {
    const { map } = okSidecar(["beta", "alpha"]);
    map.health = () =>
      healthResult([
        pluginReport(FILE, "ai-news", [
          sourceReport("beta", "ok", "https://example.com/beta"),
          sourceReport("alpha", "unknown", "https://example.com/alpha"),
        ]),
      ]);
    return { map };
  }

  it("渲染层走 ui/table 基件:table-fixed + colgroup 定宽 + 36px 紧凑行", async () => {
    installSidecar(twoRowsSidecar().map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("beta")).toBeTruthy();

    const table = document.querySelector('[data-slot="table"]') as HTMLTableElement;
    expect(table.className).toContain("table-fixed");
    // colgroup:除末列(操作,吃剩余宽)外每列钉 getSize() 像素宽
    const cols = Array.from(table.querySelectorAll("col"));
    expect(cols).toHaveLength(8);
    expect(cols[0].style.width).toBe("150px"); // 源名称 size
    expect(cols[2].style.width).toBe("280px"); // URL size
    expect(cols[7].style.width).toBe(""); // 操作列不定宽
    // compact 密度:行 h-9(36px)由基件 TableRow 提供
    const compactRow = table.querySelector('[data-slot="table-row"]') as HTMLElement;
    expect(compactRow.className).toContain("h-9");
  });

  it("健康徽章四态语义:圆点 + 文字(unknown 在列,非 pill 底)", async () => {
    installSidecar(twoRowsSidecar().map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("beta")).toBeTruthy();

    const okBadge = document.querySelector("[data-health='ok']");
    const unknownBadge = document.querySelector("[data-health='unknown']");
    expect(okBadge?.textContent).toBe("正常");
    expect(unknownBadge?.textContent).toBe("未知");
    // dot+文字范式:徽标内首子元素是圆点(span,无文本)
    expect(okBadge?.querySelector("span")?.className).toContain("rounded-full");
    expect(okBadge?.querySelector("span")?.textContent).toBe("");
  });

  it("列宽拖拽(Ant Table 手感):拖右缘手柄实时改宽,手柄点击不误触排序", async () => {
    installSidecar(twoRowsSidecar().map);
    render(
      <MemoryRouter>
        <SourcesScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("beta")).toBeTruthy();

    const urlHeader = screen.getByRole("columnheader", { name: /URL/ }) as HTMLTableCellElement;
    expect(urlHeader.style.width).toBe("280px");
    // 可拖列才有手柄;启停/操作(定宽控件列)没有
    const handles = document.querySelectorAll("[data-column-resize-handle]");
    expect(handles).toHaveLength(6);
    const urlHandle = urlHeader.querySelector('[data-column-resize-handle="url"]') as HTMLElement;
    expect(urlHandle).toBeTruthy();

    // pointerdown 在手柄 → document mousemove/mouseup(TanStack 鼠标路径)
    // clientX 400→460:URL 列 280 → 340(onChange 模式拖中即变)
    fireEvent.pointerDown(urlHandle, {
      clientX: 400,
      button: 0,
    });
    fireEvent.mouseMove(document, { clientX: 460 });
    fireEvent.mouseUp(document, { clientX: 460 });
    await waitFor(() => {
      expect(urlHeader.style.width).toBe("340px");
    });
    // colgroup 同步(th 与 col 同源 getSize())
    const table = document.querySelector('[data-slot="table"]') as HTMLTableElement;
    expect(Array.from(table.querySelectorAll("col"))[2].style.width).toBe("340px");

    // 拖拽收尾的 click 停在手柄上,不冒泡成表头排序
    expect(urlHeader.getAttribute("aria-sort")).toBeNull();

    // 双击手柄复位列宽(TanStack resize 惯例)
    fireEvent.dblClick(urlHandle);
    await waitFor(() => {
      expect(urlHeader.style.width).toBe("280px");
    });
  });
});
