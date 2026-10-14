// @vitest-environment jsdom
//
// 建源向导对话框测试(PRD AC2/3/5/6/7/8):五步导航与分步校验门 / 保存链
// (干跑 error 停 + mtime 链)/ 试采链(sources.test timeout 60 →
// test.completed 内嵌摘要 + 查看详情复用 TestResultDialog)/ 闭环
// (失败→返回修改→重存带 mtime→再试采→完成态深链)/ 关闭守卫三径 + 已保存
// 文件不回收。mock sidecar 惯例同 sources.test.tsx;顶栏按钮改绑的屏级断言
// (AC1)归 sources.test.tsx 接线后补,本文件只测向导组件本身。
//
// 时序注记:test.completed 事件可能早于 sources.test 应答落地(state 仍
// launching)到达 —— 断言处用 waitFor 内重放事件(同 job_id 重复投递对
// done 态是 no-op),不靠 sleep。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import { SourceWizardDialog } from "./source-wizard-dialog";

// ---------------------------------------------------------------------------
// 协议夹具(形状对照 screens/yaml-editor/api.ts / desktop/entry.py `_m_*`)
// ---------------------------------------------------------------------------

type Handler = (params: never) => unknown;
type SidecarMap = Record<string, Handler>;

function errJson(code: string, message: string, path = "$"): string {
  return JSON.stringify({ code, path, message });
}

function wizardSidecar() {
  const state = {
    existing: [] as string[],
    savedFiles: [] as { file: string; content: string; expected_mtime: number | null }[],
    validateResult: {
      valid: true,
      findings: [] as { path: string; code: string; message: string; level: "error" | "warning" }[],
      category: null,
    },
    saveError: null as string | null,
    testJobCounter: 0,
  };
  const map: SidecarMap = {
    "yaml.list": () => ({
      config_dir: "/data/config",
      files: state.existing.map((name) => ({
        file: `/data/config/${name}`,
        name,
        parse_ok: true,
        category_id: null,
        category_name: null,
        sources: null,
        error: null,
      })),
    }),
    "yaml.validate": () => state.validateResult,
    "yaml.save": (params: never) => {
      if (state.saveError !== null) throw state.saveError;
      const { file, content, expected_mtime } = params as {
        file: string;
        content: string;
        expected_mtime: number | null;
      };
      state.savedFiles.push({ file, content, expected_mtime });
      const created = state.savedFiles.length === 1;
      return {
        file,
        written: true,
        created,
        backed_up: created ? null : `${file}.bak`,
        mtime: 222.25,
        warnings: [],
      };
    },
    "sources.test": (params: never) => {
      state.testJobCounter += 1;
      const { source } = params as { source: string };
      return { job_id: state.testJobCounter, state: "running", source };
    },
  };
  return { map, state };
}

function installSidecar(map: SidecarMap): void {
  mocks.invoke.mockImplementation(
    async (_command: string, args: { method: string; params?: unknown }) => {
      const handler = map[args.method];
      if (!handler) {
        throw errJson("method_not_found", `未知方法 ${args.method}`, "method");
      }
      return handler(args.params as never);
    },
  );
}

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

function lastCall(method: string): { params: unknown } | undefined {
  const calls = mocks.invoke.mock.calls.filter(([, args]) => (args as { method: string }).method === method);
  return calls.at(-1)?.[1] as { params: unknown } | undefined;
}

function callCount(method: string): number {
  return mocks.invoke.mock.calls.filter(([, args]) => (args as { method: string }).method === method).length;
}

let confirmSpy: ReturnType<typeof vi.spyOn>;

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
  mocks.listen.mockImplementation(async () => () => undefined);
  confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);
});
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  confirmSpy.mockRestore();
});

// ---------------------------------------------------------------------------
// 表单填充助手(受控输入逐字段点火)
// ---------------------------------------------------------------------------

function fillStep1(id = "demo-list", name = "演示列表") {
  fireEvent.change(screen.getByLabelText("品类 id(也是文件名)"), { target: { value: id } });
  fireEvent.change(screen.getByLabelText("品类名"), { target: { value: name } });
  fireEvent.change(screen.getByLabelText("抓取频率"), { target: { value: "0 10 * * *" } });
}

function fillStep2(url = "https://example.com/list") {
  fireEvent.change(screen.getByLabelText("页面地址"), { target: { value: url } });
}

function fillStep3Item(item = "div.item") {
  fireEvent.change(screen.getByLabelText("列表整条的选择器(item)"), { target: { value: item } });
}

function clickNext() {
  fireEvent.click(screen.getByRole("button", { name: "下一步" }));
}

/** 直填到第 4 步(1-3 步全过门;字段选择器逐行填) */
function arriveAtStep4() {
  fillStep1();
  clickNext();
  fillStep2();
  clickNext();
  fillStep3Item();
  fireEvent.change(screen.getByLabelText("字段 1 选择器"), { target: { value: "h3 a" } });
  fireEvent.change(screen.getByLabelText("字段 2 选择器"), { target: { value: "h3 a" } });
  clickNext();
  expect(screen.getByTestId("wizard-yaml-preview")).toBeTruthy();
}

function renderDialog() {
  const onClose = vi.fn();
  render(<SourceWizardDialog onClose={onClose} />);
  return { onClose };
}

/** test.completed 成功报文(7 条,前 2 条带字段) */
function okTestEvent(jobId: number) {
  return {
    type: "test.completed",
    job_id: jobId,
    ok: true,
    exit_code: 0,
    result: {
      command: "test",
      sources: [
        {
          source: "main",
          engine: "static_html",
          engine_configured: "static_html",
          ok: true,
          item_count: 7,
          failures: [],
          fingerprint: {
            skip_reason: null,
            verdict: "changed_or_first_fetch",
            meaning: "内容有变化或首次抓取,线上调度会正常提取",
          },
          items: [
            { fields: { title: "第一条", url: "https://example.com/a" }, dedup_key: "sha:aaa" },
            { fields: { title: "第二条", url: "https://example.com/b" }, dedup_key: "sha:bbb" },
          ],
          items_truncated: true,
        },
      ],
    },
    ts: "2026-10-14T08:00:00+00:00",
  };
}

/** 保存并等试采进入在途态(launching/running 同 testid) */
async function saveAndWaitTest() {
  fireEvent.click(screen.getByRole("button", { name: "保存" }));
  await screen.findByTestId("wizard-test-running");
}

/** 事件投递 + 断言(重放直到命中;同 job_id 对 done 态重复投递为 no-op) */
async function emitUntil(events: { emit: (payload: Record<string, unknown>) => void }, payload: Record<string, unknown>, assert: () => void) {
  await waitFor(
    () => {
      events.emit(payload);
      assert();
    },
    { timeout: 4000 },
  );
}

// ---------------------------------------------------------------------------

describe("向导:第 1 步门(AC2)", () => {
  it("id 不合正则即拦(零校验/保存请求);schedule 未选不进下一步", async () => {
    installSidecar(wizardSidecar().map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    fillStep1("Bad Id", "名字");
    fireEvent.change(screen.getByLabelText("抓取频率"), { target: { value: "" } }); // 显式不选
    clickNext();

    const errors = screen.getByTestId("wizard-step-errors");
    expect(errors.textContent).toContain("小写字母");
    expect(errors.textContent).toContain("抓取频率还没选");
    // 仍停第 1 步(第 2 步的页面地址未出现);未发任何校验/保存请求
    expect(screen.queryByLabelText("页面地址")).toBeNull();
    expect(callCount("yaml.validate")).toBe(0);
    expect(callCount("yaml.save")).toBe(0);

    // 改好后放行
    fireEvent.change(screen.getByLabelText("品类 id(也是文件名)"), { target: { value: "demo-list" } });
    fireEvent.change(screen.getByLabelText("抓取频率"), { target: { value: "0 10 * * *" } });
    clickNext();
    expect(screen.getByLabelText("页面地址")).toBeTruthy();
  });

  it("同名文件即时提示(yaml.list 预检,不拦输入)", async () => {
    const { map, state } = wizardSidecar();
    state.existing = ["demo-list.yaml", "other.yaml"];
    installSidecar(map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    fireEvent.change(screen.getByLabelText("品类 id(也是文件名)"), { target: { value: "demo-list" } });
    const warning = await screen.findByTestId("wizard-id-exists");
    expect(warning.textContent).toContain("已有同名文件 demo-list.yaml");
    expect(warning.textContent).toContain("换一个 id");

    // 提示不拦输入:换个 id 提示消失,可继续前进
    fireEvent.change(screen.getByLabelText("品类 id(也是文件名)"), { target: { value: "fresh-id" } });
    await waitFor(() => {
      expect(screen.queryByTestId("wizard-id-exists")).toBeNull();
    });
    fillStep1("fresh-id");
    clickNext();
    expect(screen.getByLabelText("页面地址")).toBeTruthy();
  });

  it("自定义 cron:第 1 步出输入框,5 段形状预检", async () => {
    installSidecar(wizardSidecar().map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    fillStep1();
    fireEvent.change(screen.getByLabelText("抓取频率"), { target: { value: "__custom__" } });
    fireEvent.change(screen.getByLabelText("自定义频率(5 段 cron)"), { target: { value: "0 9 *" } });
    clickNext();
    const errors = screen.getByTestId("wizard-step-errors");
    expect(errors.textContent).toContain("5 段 cron");

    fireEvent.change(screen.getByLabelText("自定义频率(5 段 cron)"), { target: { value: "0 9 * * *" } });
    clickNext();
    expect(screen.getByLabelText("页面地址")).toBeTruthy();
  });
});

describe("向导:第 3 步门与字段行(AC3)", () => {
  it("fields 缺 url 字段名即拦;item 为空即拦;提示人话", async () => {
    installSidecar(wizardSidecar().map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    fillStep1();
    clickNext();
    fillStep2();
    clickNext();
    expect(screen.getByLabelText("列表整条的选择器(item)")).toBeTruthy();

    // 删掉预置 url 行 → 缺 url 字段
    fireEvent.click(screen.getByRole("button", { name: "删除字段 2" }));
    fillStep3Item();
    fireEvent.change(screen.getByLabelText("字段 1 选择器"), { target: { value: "h3 a" } });
    clickNext();
    const errors = screen.getByTestId("wizard-step-errors");
    expect(errors.textContent).toContain("必须有 url");
    expect(screen.getByLabelText("列表整条的选择器(item)")).toBeTruthy(); // 仍停第 3 步

    // 补回 url 字段,item 清空也拦
    fireEvent.click(screen.getByRole("button", { name: "添加字段" }));
    fireEvent.change(screen.getByLabelText("字段 2 名字"), { target: { value: "url" } });
    fireEvent.change(screen.getByLabelText("字段 2 选择器"), { target: { value: "h3 a" } });
    fireEvent.change(screen.getByLabelText("列表整条的选择器(item)"), { target: { value: "" } });
    clickNext();
    expect(screen.getByTestId("wizard-step-errors").textContent).toContain("列表整条的选择器还没填");
  });

  it("字段行可增删;新行入产物", async () => {
    installSidecar(wizardSidecar().map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    fillStep1();
    clickNext();
    fillStep2();
    clickNext();
    expect(screen.getAllByTestId("wizard-field-row")).toHaveLength(2);

    fireEvent.click(screen.getByRole("button", { name: "添加字段" }));
    expect(screen.getAllByTestId("wizard-field-row")).toHaveLength(3);
    fireEvent.change(screen.getByLabelText("字段 3 名字"), { target: { value: "price" } });
    fireEvent.change(screen.getByLabelText("字段 3 选择器"), { target: { value: "span.price" } });

    fireEvent.click(screen.getByRole("button", { name: "删除字段 1" })); // 删 title 行 → [url, price]
    expect(screen.getAllByTestId("wizard-field-row")).toHaveLength(2);

    fillStep3Item();
    fireEvent.change(screen.getByLabelText("字段 1 选择器"), { target: { value: "h3 a" } }); // url 行
    clickNext();
    const preview = screen.getByTestId("wizard-yaml-preview").textContent ?? "";
    expect(preview).toContain('url: "h3 a@href"');
    expect(preview).toContain('price: "span.price"');
    expect(preview).not.toContain("title:");
  });
});

describe("向导:保存链(AC5)", () => {
  it("干跑有 error 停第 4 步不发保存;findings 如实展示", async () => {
    const { map, state } = wizardSidecar();
    state.validateResult = {
      valid: false,
      findings: [
        { path: "$.sources[0].url", code: "invalid_url", message: "source url 必须是 http(s) 地址", level: "error" },
      ],
      category: null,
    };
    installSidecar(map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");
    arriveAtStep4();

    fireEvent.click(screen.getByRole("button", { name: "保存" }));
    await screen.findByTestId("wizard-validate-findings");

    const findingsBox = screen.getByTestId("wizard-validate-findings");
    expect(findingsBox.textContent).toContain("还没保存");
    expect(findingsBox.textContent).toContain("invalid_url");
    expect(callCount("yaml.save")).toBe(0);
    expect(screen.getByRole("button", { name: "保存" })).toBeTruthy(); // 仍在第 4 步
  });

  it("保存成功:首存 expected_mtime=null 新建;保存后自动发起试采(timeout 60)", async () => {
    const { map, state } = wizardSidecar();
    installSidecar(map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");
    arriveAtStep4();
    await saveAndWaitTest();

    expect(state.savedFiles).toHaveLength(1);
    expect(state.savedFiles[0].file).toBe("/data/config/demo-list.yaml");
    expect(state.savedFiles[0].expected_mtime).toBeNull();
    expect(state.savedFiles[0].content).toContain("id: demo-list");
    expect(state.savedFiles[0].content).toContain('url: "https://example.com/list"');
    expect(state.savedFiles[0].content).toContain('item: "div.item"');
    // 试采参数:file + 源名 + timeout 60(AC6 前半)
    expect(lastCall("sources.test")?.params).toEqual({
      file: "/data/config/demo-list.yaml",
      source: "main",
      timeout: 60,
    });
    // 保存后 id 锁定(换文件名会让 mtime 链指向别的文件):经返回修改回到第 1 步验证
    fireEvent.click(screen.getByRole("button", { name: "返回修改" }));
    await screen.findByLabelText("列表整条的选择器(item)");
    fireEvent.click(screen.getByRole("button", { name: "上一步" }));
    fireEvent.click(screen.getByRole("button", { name: "上一步" }));
    const idInput = screen.getByLabelText("品类 id(也是文件名)") as HTMLInputElement;
    expect(idInput.disabled).toBe(true);
    expect(idInput.value).toBe("demo-list");
  });

  it("mtime_conflict:人话指路展示,留在第 4 步可改重试", async () => {
    const { map, state } = wizardSidecar();
    state.saveError = errJson("mtime_conflict", "目标文件已存在,新建意图(expected_mtime=null)撞上已有文件");
    installSidecar(map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");
    arriveAtStep4();

    fireEvent.click(screen.getByRole("button", { name: "保存" }));
    const alertBox = await screen.findByTestId("wizard-save-error");
    expect(alertBox.textContent).toContain("文件已被其他窗口改动");
    expect(alertBox.textContent).toContain("换个 id 重来");
    expect(alertBox.textContent).toContain("code=mtime_conflict");

    // 可重试:同链路再保存成功(错误随新动作清空)
    state.saveError = null;
    fireEvent.click(screen.getByRole("button", { name: "保存" }));
    await screen.findByTestId("wizard-test-running");
  });
});

describe("向导:试采链(AC6)", () => {
  it("test.completed → 内嵌摘要(引擎/条数/样例值)+ 查看详情复用 TestResultDialog;成功入完成态", async () => {
    const events = installEvents();
    const { map } = wizardSidecar();
    installSidecar(map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");
    arriveAtStep4();
    await saveAndWaitTest();

    await emitUntil(events, okTestEvent(1), () => {
      expect(screen.getByTestId("wizard-test-summary")).toBeTruthy();
    });
    const summary = screen.getByTestId("wizard-test-summary");
    expect(summary.textContent).toContain("static_html");
    expect(summary.textContent).toContain("7 条");
    expect(within(summary).getByText("第一条")).toBeTruthy();
    expect(within(summary).getByText("https://example.com/a")).toBeTruthy();

    // 查看详情 → 既有 TestResultDialog(零改动组件,原 testid/文案)
    fireEvent.click(within(summary).getByRole("button", { name: "查看详情" }));
    const detail = await screen.findByTestId("test-result-dialog");
    expect(detail.getAttribute("aria-label")).toBe("试抓结果 main");
    expect(detail.textContent).toContain("内容有变化或首次抓取");
    // 详情打开时 ESC 只关详情,不关向导(防双关丢结果)
    fireEvent.keyDown(window, { key: "Escape" });
    await waitFor(() => {
      expect(screen.queryByTestId("test-result-dialog")).toBeNull();
    });
    expect(screen.getByTestId("source-wizard-dialog")).toBeTruthy();

    // 成功 → 完成态:落盘路径 + 深链(AC7 后半)
    const done = screen.getByTestId("wizard-done");
    expect(done.textContent).toContain("/data/config/demo-list.yaml");
    expect(
      within(done)
        .getByRole("link", { name: "去补全推送等配置" })
        .getAttribute("href"),
    ).toBe(`#/yaml-editor?file=${encodeURIComponent("/data/config/demo-list.yaml")}`);
  });

  it("发起失败(test_busy)如实展示并给重试;重试再发起", async () => {
    const { map } = wizardSidecar();
    let busy = true;
    map["sources.test"] = () => {
      if (busy) {
        throw errJson("test_busy", "已有一次试抓正在进行,请等它完成后再试");
      }
      return { job_id: 9, state: "running", source: "main" };
    };
    installSidecar(map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");
    arriveAtStep4();

    fireEvent.click(screen.getByRole("button", { name: "保存" }));
    const launchError = await screen.findByTestId("wizard-test-launch-error");
    expect(launchError.textContent).toContain("test_busy");
    expect(launchError.textContent).toContain("已有一次试抓正在进行");

    busy = false;
    fireEvent.click(within(launchError).getByRole("button", { name: "重试" }));
    await screen.findByTestId("wizard-test-running");
  });
});

describe("向导:闭环(AC7)", () => {
  it("失败 → 返回修改(表单保留)→ 重存带 mtime → 再试采 → 完成关闭", async () => {
    const events = installEvents();
    const { map, state } = wizardSidecar();
    installSidecar(map);
    renderDialog();
    await screen.findByTestId("source-wizard-dialog");
    arriveAtStep4();
    await saveAndWaitTest();

    // 第一次试采:失败(事件 ok=false)
    const failedEvent = {
      type: "test.completed",
      job_id: 1,
      ok: false,
      exit_code: 1,
      error: "extract",
      data: {
        error: "extract",
        errors: [{ path: "$.sources[0].extract", message: "选择器没有命中任何元素" }],
      },
      ts: "2026-10-14T08:00:00+00:00",
    };
    await emitUntil(events, failedEvent, () => {
      expect(screen.getByTestId("wizard-test-summary").textContent).toContain("没抓到");
    });
    expect(screen.getByTestId("wizard-test-summary").textContent).toContain("选择器没有命中任何元素");

    // 返回修改:回第 3 步,表单态保留(item 仍是旧值;返回修改按钮在场)
    fireEvent.click(screen.getByRole("button", { name: "返回修改" }));
    const itemInput = await screen.findByLabelText("列表整条的选择器(item)");
    expect((itemInput as HTMLInputElement).value).toBe("div.item");

    // 改选择器 → 重存(带记住的 mtime)→ 再试采
    fireEvent.change(itemInput, { target: { value: "div.item-v2" } });
    clickNext();
    fireEvent.click(screen.getByRole("button", { name: "保存" }));
    await screen.findByTestId("wizard-test-running");

    expect(state.savedFiles).toHaveLength(2);
    expect(state.savedFiles[1].expected_mtime).toBe(222.25); // mtime 链(AC5 后半)
    expect(state.savedFiles[1].content).toContain('item: "div.item-v2"');

    // 第二次试采:成功 → 完成态
    await emitUntil(events, okTestEvent(2), () => {
      expect(screen.getByTestId("wizard-done")).toBeTruthy();
    });
    expect(screen.getByTestId("wizard-done").textContent).toContain("/data/config/demo-list.yaml");

    // 完成按钮关向导(内容已走完,不再 confirm)
    expect(confirmSpy).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "完成" }));
    expect(confirmSpy).not.toHaveBeenCalled();
  });
});

describe("向导:关闭守卫(AC8)", () => {
  it("干净表单:ESC 直接关,confirm 零调用", async () => {
    installSidecar(wizardSidecar().map);
    const { onClose } = renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    fireEvent.keyDown(window, { key: "Escape" });
    await waitFor(() => {
      expect(onClose).toHaveBeenCalledTimes(1);
    });
    expect(confirmSpy).not.toHaveBeenCalled();
  });

  it("有输入:ESC 先确认,取消留内容、确认才关;已保存文件不回收(零删除调用)", async () => {
    const events = installEvents();
    const { map } = wizardSidecar();
    installSidecar(map);
    const { onClose } = renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    arriveAtStep4();
    await saveAndWaitTest();
    await emitUntil(events, okTestEvent(1), () => {
      expect(screen.getByTestId("wizard-done")).toBeTruthy();
    });

    // 已保存未确认关闭:ESC → confirm;点「取消」(false)留在向导
    confirmSpy.mockReturnValue(false);
    fireEvent.keyDown(window, { key: "Escape" });
    expect(confirmSpy).toHaveBeenCalled();
    expect(onClose).not.toHaveBeenCalled();
    expect(screen.getByTestId("source-wizard-dialog")).toBeTruthy();

    // 确认关闭(遮罩径);已保存文件保留 = 全程零 yaml.delete
    confirmSpy.mockReturnValue(true);
    fireEvent.click(screen.getByTestId("source-wizard-overlay"));
    await waitFor(() => {
      expect(onClose).toHaveBeenCalledTimes(1);
    });
    expect(callCount("yaml.delete")).toBe(0);
  });

  it("干净表单:X 关闭钮同径直关", async () => {
    installSidecar(wizardSidecar().map);
    const { onClose } = renderDialog();
    await screen.findByTestId("source-wizard-dialog");

    fireEvent.click(screen.getByRole("button", { name: "关闭对话框" }));
    await waitFor(() => {
      expect(onClose).toHaveBeenCalledTimes(1);
    });
    expect(confirmSpy).not.toHaveBeenCalled();
  });
});
