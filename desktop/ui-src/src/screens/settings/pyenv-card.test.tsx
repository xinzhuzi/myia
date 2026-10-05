// @vitest-environment jsdom
//
// 「Python 运行环境」IPC 契约测试(10-05-desktop-managed-py-env 第 4 步;
// implement.md 门:vitest 契约测试)。契约波次钉死,与壳侧 src-tauri/src/
// pyenv.rs 对齐,全量 mock Tauri IPC(不触真实壳):
// - command pyenv_get_status → {state, install_path, python_path,
//   mirror_runtime, mirror_pypi, steps:[{phase,status,error}]}
// - command pyenv_start_setup(mirror_runtime?, mirror_pypi?;前端键 camelCase)
// - command pyenv_sync_deps()
// - event pyenv-status-changed(载荷同 status 形态)
// 组件面(design §5):开始配置 / 安装路径 / Python 使用路径 / 双镜像覆盖 /
// 安装明细(状态机逐项)/ 同步依赖(D4,依赖漂移时出现)。
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
  listen: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import {
  onPyenvStatusChanged,
  parsePyenvStatus,
  pyenvGetStatus,
  pyenvStartSetup,
  pyenvSyncDeps,
  PYENV_STATUS_EVENT_NAME,
} from "./pyenv-api";
import { PyenvCard } from "./pyenv-card";

// ---------------------------------------------------------------------------
// 夹具(wire 形 = 壳侧 serde 序列化 PyenvStatus 的原样 JSON)
// ---------------------------------------------------------------------------

function wireFixture(overrides?: Partial<Record<string, unknown>>): Record<string, unknown> {
  return {
    state: "not_configured",
    install_path: "/Users/dev/Library/Application Support/MYIA/python",
    python_path: "/Users/dev/Library/Application Support/MYIA/python/bin/python3",
    mirror_runtime: null,
    mirror_pypi: null,
    steps: [],
    ...overrides,
  };
}

// ---------------------------------------------------------------------------
// IPC mock:命令按契约应答(壳桩行为 = pyenv.rs 第 2 步语义:start_setup
// 落盘镜像覆盖后重探测回包;sync_deps 重探测如实回当前态)
// ---------------------------------------------------------------------------

function installPyenvIpc(
  initial: Record<string, unknown> = wireFixture(),
  verifyResult: Record<string, unknown> = {
    ok: true,
    checks: [
      { id: "python_binary", ok: true, detail: "Python 3.12.7" },
      { id: "deps_fingerprint", ok: true, detail: "一致(a89418…)" },
      { id: "sidecar_handshake", ok: true, detail: "version 应答正常" },
    ],
  },
) {
  let current = initial;
  mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
    if (command === "pyenv_get_status") return current;
    if (command === "pyenv_start_setup") {
      const params = (args ?? {}) as { mirrorRuntime?: string; mirrorPypi?: string };
      current = {
        ...current,
        mirror_runtime: params.mirrorRuntime ?? null,
        mirror_pypi: params.mirrorPypi ?? null,
      };
      return current;
    }
    if (command === "pyenv_sync_deps") return current;
    if (command === "pyenv_verify") return verifyResult;
    throw new Error(`未预期的 IPC 命令: ${command}`);
  });
  return {
    /** 模拟壳侧广播(载荷同 status 形态) */
    emitStatus: (payload: Record<string, unknown>) => currentChannel?.({ payload }),
    setState: (next: Record<string, unknown>) => {
      current = next;
    },
  };
}

let currentChannel: ((event: { payload: unknown }) => void) | null = null;

function installListen() {
  mocks.listen.mockImplementation(
    async (_name: string, handler: (event: { payload: unknown }) => void) => {
      if (_name === PYENV_STATUS_EVENT_NAME) currentChannel = handler;
      return () => undefined;
    },
  );
}

function callsOf(command: string): unknown[] {
  return mocks.invoke.mock.calls
    .filter(([called]) => called === command)
    .map(([, args]) => args)
    .map((args) => args ?? {});
}

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
  currentChannel = null;
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  currentChannel = null;
});

// ---------------------------------------------------------------------------
// api 层契约(命令名 / 参数键 / 载荷守门 / 事件名)
// ---------------------------------------------------------------------------

describe("pyenv-api:IPC 契约(与壳侧 pyenv.rs 对齐)", () => {
  it("pyenvGetStatus:命令名 pyenv_get_status、无参;六键载荷原样消费", async () => {
    mocks.invoke.mockResolvedValue(wireFixture());
    const status = await pyenvGetStatus();
    expect(mocks.invoke).toHaveBeenCalledTimes(1);
    expect(mocks.invoke).toHaveBeenCalledWith("pyenv_get_status");
    expect(status.state).toBe("not_configured");
    expect(status.install_path).toContain("/python");
    expect(status.python_path).toContain("/python/bin/python3");
    expect(status.mirror_runtime).toBeNull();
    expect(status.mirror_pypi).toBeNull();
    expect(status.steps).toEqual([]);
  });

  it("pyenvStartSetup:参数键 camelCase(mirrorRuntime/mirrorPypi);trim 归一", async () => {
    mocks.invoke.mockResolvedValue(wireFixture());
    await pyenvStartSetup({
      mirrorRuntime: "  https://mirror.example/runtime.tar.gz  ",
      mirrorPypi: "https://mirror.example/pypi/simple",
    });
    expect(mocks.invoke).toHaveBeenCalledWith("pyenv_start_setup", {
      mirrorRuntime: "https://mirror.example/runtime.tar.gz",
      mirrorPypi: "https://mirror.example/pypi/simple",
    });
  });

  it("pyenvStartSetup:空白镜像键省略(= 清回默认源,Option 参数缺省)", async () => {
    mocks.invoke.mockResolvedValue(wireFixture());
    await pyenvStartSetup({ mirrorRuntime: "https://m.example/rt.tar.gz", mirrorPypi: "   " });
    expect(mocks.invoke).toHaveBeenCalledWith("pyenv_start_setup", {
      mirrorRuntime: "https://m.example/rt.tar.gz",
    });
    // 全空 → 空参数对象(壳侧整体替换式落盘 = 双默认源)
    await pyenvStartSetup({ mirrorRuntime: "", mirrorPypi: " " });
    expect(mocks.invoke).toHaveBeenLastCalledWith("pyenv_start_setup", {});
  });

  it("pyenvSyncDeps:命令名 pyenv_sync_deps、无参", async () => {
    mocks.invoke.mockResolvedValue(wireFixture({ state: "ready" }));
    const status = await pyenvSyncDeps();
    expect(mocks.invoke).toHaveBeenCalledWith("pyenv_sync_deps");
    expect(status.state).toBe("ready");
  });

  it("parsePyenvStatus:steps 契约形态透传(error 恒在场);未知 phase 丢弃、未知 status 按 pending", () => {
    const parsed = parsePyenvStatus(
      wireFixture({
        state: "error",
        steps: [
          { phase: "downloading", status: "done", error: null },
          { phase: "verifying", status: "failed", error: "checksum_mismatch: sha256 不符" },
          { phase: "mystery_phase", status: "done", error: null },
          { phase: "extracting", status: "weird_status", error: null },
        ],
      }),
    );
    expect(parsed.state).toBe("error");
    expect(parsed.steps).toEqual([
      { phase: "downloading", status: "done", error: null },
      { phase: "verifying", status: "failed", error: "checksum_mismatch: sha256 不符" },
      { phase: "extracting", status: "pending", error: null },
    ]);
  });

  it("parsePyenvStatus:state 非契约五态即抛(对齐破了要大声失败)", () => {
    expect(() => parsePyenvStatus(wireFixture({ state: "configuring" }))).toThrow(TypeError);
    expect(() => parsePyenvStatus("not-an-object")).toThrow(TypeError);
  });

  it("onPyenvStatusChanged:订阅 pyenv-status-changed;契约载荷解析回调,坏载荷走 onMalformed", async () => {
    const handler = vi.fn();
    const malformed = vi.fn();
    mocks.listen.mockResolvedValue(() => undefined);
    await onPyenvStatusChanged(handler, malformed);

    expect(mocks.listen).toHaveBeenCalledTimes(1);
    expect(mocks.listen.mock.calls[0][0]).toBe("pyenv-status-changed");
    const dispatch = mocks.listen.mock.calls[0][1] as (event: { payload: unknown }) => void;

    dispatch({ payload: wireFixture({ state: "ready" }) });
    expect(handler).toHaveBeenLastCalledWith(expect.objectContaining({ state: "ready" }));
    expect(malformed).not.toHaveBeenCalled();

    dispatch({ payload: wireFixture({ state: "bogus" }) });
    expect(malformed).toHaveBeenCalledTimes(1);
    expect(handler).toHaveBeenCalledTimes(1); // 坏载荷不进好通道
  });
});

// ---------------------------------------------------------------------------
// 组件面(design §5 字段全覆盖 + 状态机随事件随动)
// ---------------------------------------------------------------------------

describe("PyenvCard:设置屏「Python 运行环境」区块", () => {
  it("挂载即拉取 pyenv_get_status;未配置态字段齐(路径/镜像初值/五阶段骨架/开始配置),无同步依赖按钮", async () => {
    installPyenvIpc();
    installListen();
    render(<PyenvCard />);

    await waitFor(() => expect(callsOf("pyenv_get_status").length).toBe(1));
    expect((await screen.findByTestId("pyenv-state-badge")).textContent).toContain("未配置");
    // 路径两行如实回显(安装路径 / Python 使用路径)
    expect(screen.getByTestId("pyenv-install-path").textContent).toBe(
      "/Users/dev/Library/Application Support/MYIA/python",
    );
    expect(screen.getByTestId("pyenv-python-path").textContent).toBe(
      "/Users/dev/Library/Application Support/MYIA/python/bin/python3",
    );
    // 双镜像输入初值空(当前生效 = 默认源)
    expect((screen.getByLabelText("运行时下载源覆盖") as HTMLInputElement).value).toBe("");
    expect((screen.getByLabelText("PyPI 镜像覆盖") as HTMLInputElement).value).toBe("");
    // 安装明细 = 状态机五阶段骨架逐项(downloading…selfcheck 全等待中)
    for (const phase of ["downloading", "verifying", "extracting", "installing_deps", "selfcheck"]) {
      expect(screen.getByTestId(`pyenv-step-${phase}-status`).textContent).toContain("等待中");
    }
    // D2 显式动作在位;同步依赖不出现(仅 deps_stale)
    expect(screen.getByRole("button", { name: /开始配置/ })).toBeTruthy();
    expect(screen.queryByTestId("pyenv-sync-deps")).toBeNull();
  });

  it("双镜像覆盖:填入后点开始配置 → pyenv_start_setup 收 camelCase 双键;回包镜像回填输入框 + 动作回执", async () => {
    installPyenvIpc();
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-state-badge");

    fireEvent.change(screen.getByLabelText("运行时下载源覆盖"), {
      target: { value: "https://mirror.example/cpython.tar.gz" },
    });
    fireEvent.change(screen.getByLabelText("PyPI 镜像覆盖"), {
      target: { value: "https://pypi.tuna.tsinghua.edu.cn/simple" },
    });
    fireEvent.click(screen.getByRole("button", { name: /开始配置/ }));

    await screen.findByTestId("pyenv-action-note");
    expect(callsOf("pyenv_start_setup")).toEqual([
      {
        mirrorRuntime: "https://mirror.example/cpython.tar.gz",
        mirrorPypi: "https://pypi.tuna.tsinghua.edu.cn/simple",
      },
    ]);
    // 壳桩回包(镜像已生效)回填输入框:当前生效值可见
    expect((screen.getByLabelText("运行时下载源覆盖") as HTMLInputElement).value).toBe(
      "https://mirror.example/cpython.tar.gz",
    );
    expect((screen.getByLabelText("PyPI 镜像覆盖") as HTMLInputElement).value).toBe(
      "https://pypi.tuna.tsinghua.edu.cn/simple",
    );
  });

  it("pyenv-status-changed 事件:载荷同 status 形态,安装中态实时随动(徽标/明细/按钮禁用)", async () => {
    const ipc = installPyenvIpc();
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-state-badge");

    act(() =>
      ipc.emitStatus(
        wireFixture({
          state: "installing",
          mirror_runtime: "https://mirror.example/cpython.tar.gz",
          steps: [
            { phase: "downloading", status: "done", error: null },
            { phase: "verifying", status: "running", error: null },
          ],
        }),
      ),
    );

    expect(screen.getByTestId("pyenv-state-badge").textContent).toContain("安装中");
    expect(screen.getByTestId("pyenv-step-downloading-status").textContent).toContain("已完成");
    expect(screen.getByTestId("pyenv-step-verifying-status").textContent).toContain("进行中");
    expect(screen.getByTestId("pyenv-step-extracting-status").textContent).toContain("等待中");
    // 安装中不可重复触发(主按钮转「安装中…」);事件刷新不覆写镜像输入(防打断输入,当前无草稿=保持默认)
    expect((screen.getByRole("button", { name: /安装中/ }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByLabelText("运行时下载源覆盖") as HTMLInputElement).value).toBe("");
  });

  it("deps_stale → 「同步依赖」出现(D4);点击发 pyenv_sync_deps;ready 态不出现", async () => {
    const ipc = installPyenvIpc(wireFixture({ state: "deps_stale" }));
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-state-badge");
    expect(screen.getByTestId("pyenv-state-badge").textContent).toContain("依赖漂移");

    fireEvent.click(screen.getByTestId("pyenv-sync-deps"));
    await waitFor(() => expect(callsOf("pyenv_sync_deps").length).toBe(1));
    await screen.findByTestId("pyenv-action-note");

    // 事件转 ready:同步依赖按钮卸载(依赖漂移提示只在漂移态出现)
    act(() => ipc.emitStatus(wireFixture({ state: "ready" })));
    expect(screen.getByTestId("pyenv-state-badge").textContent).toContain("就绪");
    expect(screen.queryByTestId("pyenv-sync-deps")).toBeNull();
  });

  it("ready 态主按钮=「检查状态」(10-05 主人判例):点击发 pyenv_verify(无参);通过 → 检查通过回执,无重装入口", async () => {
    installPyenvIpc(wireFixture({ state: "ready" }));
    installListen();
    render(<PyenvCard />);

    expect((await screen.findByTestId("pyenv-state-badge")).textContent).toContain("就绪");
    // 就绪态不再出现「开始配置」——语义按态分家
    expect(screen.queryByRole("button", { name: /开始配置/ })).toBeNull();
    const verify = screen.getByRole("button", { name: /检查状态/ }) as HTMLButtonElement;
    expect(verify.disabled).toBe(false);
    expect(screen.queryByTestId("pyenv-reinstall-button")).toBeNull();

    fireEvent.click(verify);
    await waitFor(() => expect(callsOf("pyenv_verify").length).toBe(1));
    expect(Object.keys((callsOf("pyenv_verify")[0] ?? {}) as object).length).toBe(0); // 无参
    expect((await screen.findByTestId("pyenv-action-note")).textContent).toContain("检查通过");
  });

  it("体检未过 → 问题逐项上屏 + 「重新安装」入口(点击发 pyenv_start_setup);通过后回执走绿色 note", async () => {
    installPyenvIpc(wireFixture({ state: "ready" }), {
      ok: false,
      checks: [
        { id: "python_binary", ok: true, detail: "Python 3.12.7" },
        { id: "deps_fingerprint", ok: false, detail: "漂移:进度戳 aaa ≠ 随包 bbb;「同步依赖」幂等对齐,或重装" },
        { id: "sidecar_handshake", ok: false, detail: "自检 version 应答超时(30s)" },
      ],
    });
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-state-badge");

    fireEvent.click(screen.getByRole("button", { name: /检查状态/ }));
    const problems = await screen.findByTestId("pyenv-verify-problems");
    expect(problems.textContent).toContain("deps_fingerprint");
    expect(problems.textContent).toContain("漂移");
    expect(screen.getByTestId("pyenv-verify-problem-sidecar_handshake").textContent).toContain("超时");
    expect(screen.queryByTestId("pyenv-verify-problem-python_binary")).toBeNull(); // 过了的不列

    // 状态不对就重装:入口出现并发幂等链命令
    fireEvent.click(screen.getByTestId("pyenv-reinstall-button"));
    await waitFor(() => expect(callsOf("pyenv_start_setup").length).toBe(1));
  });

  it("error 态:失败步 error 文案逐项可见 + 引导重试;开始配置可点(幂等重试入口)", async () => {
    installPyenvIpc(
      wireFixture({
        state: "error",
        steps: [
          { phase: "downloading", status: "done", error: null },
          { phase: "verifying", status: "failed", error: "checksum_mismatch: sha256 不符" },
        ],
      }),
    );
    installListen();
    render(<PyenvCard />);

    expect((await screen.findByTestId("pyenv-state-badge")).textContent).toContain("异常");
    expect(screen.getByTestId("pyenv-step-verifying-error").textContent).toContain("checksum_mismatch");
    expect(screen.getByTestId("pyenv-state-hint").textContent).toContain("重试");
    expect((screen.getByRole("button", { name: /重新安装/ }) as HTMLButtonElement).disabled).toBe(false);
  });

  it("拉取失败 → 结构化错误上屏(ErrorBox),重试走同一条拉取通道", async () => {
    mocks.invoke.mockRejectedValueOnce(JSON.stringify({ code: "pyenv_probe_failed", path: "$", message: "数据根不可读" }));
    installListen();
    render(<PyenvCard />);

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("数据根不可读");
    expect(alert.textContent).toContain("code=pyenv_probe_failed");

    mocks.invoke.mockResolvedValue(wireFixture());
    fireEvent.click(screen.getByRole("button", { name: "重试" }));
    await screen.findByTestId("pyenv-state-badge");
    expect(screen.getByTestId("pyenv-state-badge").textContent).toContain("未配置");
  });
});
