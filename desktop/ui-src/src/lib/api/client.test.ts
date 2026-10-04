// @vitest-environment jsdom
//
// 共享 client 的 feed-ux 批新增封装测试(10-03-feed-ux 步骤 4):
// feedExport / schedulePreview / pushTest 三封装 —— 方法名与参数形状透传
// (契约对账 entry.py `_HANDLERS` 同名方法),错误经 SidecarRequestError 归一。
import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: vi.fn() }));

import { api, SidecarRequestError } from "@/lib/api";

beforeEach(() => {
  mocks.invoke.mockReset();
});

describe("api 门面方法集(对账 _HANDLERS 键)", () => {
  it("feed-ux 三方法在门面上(与 entry.py 注册同名)", () => {
    expect(typeof api.feedExport).toBe("function");
    expect(typeof api.schedulePreview).toBe("function");
    expect(typeof api.pushTest).toBe("function");
  });

  it("read-state-server 三方法在门面上(与 entry.py 注册同名,10-04 G9)", () => {
    expect(typeof api.storeStateMark).toBe("function");
    expect(typeof api.storeStateMarkAll).toBe("function");
    expect(typeof api.storeStateImport).toBe("function");
  });

  it("cron-ui 批十方法在门面上(cron.* 九方法 + yamlList 复用,与 entry.py 注册同名)", () => {
    expect(typeof api.cronList).toBe("function");
    expect(typeof api.cronCreate).toBe("function");
    expect(typeof api.cronEdit).toBe("function");
    expect(typeof api.cronPause).toBe("function");
    expect(typeof api.cronResume).toBe("function");
    expect(typeof api.cronRun).toBe("function");
    expect(typeof api.cronRemove).toBe("function");
    expect(typeof api.cronStatus).toBe("function");
    expect(typeof api.cronRuns).toBe("function");
    expect(typeof api.yamlList).toBe("function");
  });
});

describe("cron-ui 批封装(cron.* + yaml.list)", () => {
  it("cronList:透传 all 到 cron.list;result 形状透传", async () => {
    mocks.invoke.mockResolvedValue({ db: "/h/db.sqlite", data_root: "/h", count: 0, jobs: [] });
    const result = await api.cronList({ all: true });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "cron.list",
      params: { all: true },
    });
    expect(result.count).toBe(0);
  });

  it("cronCreate:全字段 payload 透传到 cron.create", async () => {
    mocks.invoke.mockResolvedValue({ job: { id: "a1b2c3d4e5f6" } });
    const params = {
      schedule: "every monday 9am",
      category: "/p/news.yaml",
      name: "周一晨报",
      deliver: "local",
      failure_deliver: "feishu:ops",
      timezone: "Asia/Shanghai",
      config: "/p/pools.yaml",
      paused_reason: "待审核",
      repeat: 3,
      run_timeout: 600,
      dry_run: true,
      paused: false,
    };
    await api.cronCreate(params);
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "cron.create",
      params,
    });
  });

  it("cronEdit:job + 部分更新字段透传到 cron.edit", async () => {
    mocks.invoke.mockResolvedValue({ job: { id: "a1b2c3d4e5f6" } });
    await api.cronEdit({ job: "a1b2c3d4e5f6", deliver: "feishu:group" });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "cron.edit",
      params: { job: "a1b2c3d4e5f6", deliver: "feishu:group" },
    });
  });

  it("cronPause:单 job 形态透传 job+reason;all 形态只带 all", async () => {
    mocks.invoke.mockResolvedValue({ job: { id: "a1b2c3d4e5f6" } });
    await api.cronPause({ job: "晨报", reason: "排查投递" });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "cron.pause",
      params: { job: "晨报", reason: "排查投递" },
    });
    mocks.invoke.mockResolvedValue({ estopped: true, marker: "2026-10-04T10:00:00+08:00" });
    const all = await api.cronPause({ all: true });
    expect(mocks.invoke).toHaveBeenLastCalledWith("sidecar_request", {
      method: "cron.pause",
      params: { all: true },
    });
    expect(all).toEqual({ estopped: true, marker: "2026-10-04T10:00:00+08:00" });
  });

  it("cronResume:单 job(at 重挂)与 all 两形态各自透传", async () => {
    mocks.invoke.mockResolvedValue({ job: { id: "a1b2c3d4e5f6" } });
    await api.cronResume({ job: "a1b2c3d4e5f6", at: "2026-10-05T09:00:00+08:00" });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "cron.resume",
      params: { job: "a1b2c3d4e5f6", at: "2026-10-05T09:00:00+08:00" },
    });
    mocks.invoke.mockResolvedValue({ estopped: false, cleared: true });
    await api.cronResume({ all: true });
    expect(mocks.invoke).toHaveBeenLastCalledWith("sidecar_request", {
      method: "cron.resume",
      params: { all: true },
    });
  });

  it("cronRun / cronRemove / cronStatus:invoke 形状与 result 透传", async () => {
    mocks.invoke.mockResolvedValue({ job: { id: "a1b2c3d4e5f6", manual_run_at: "2026-10-04T10:00:10+08:00" } });
    await api.cronRun({ job: "晨报" });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "cron.run",
      params: { job: "晨报" },
    });
    mocks.invoke.mockResolvedValue({ removed: true, job_id: "a1b2c3d4e5f6", name: "晨报" });
    const removed = await api.cronRemove({ job: "a1b2c3d4e5f6" });
    expect(mocks.invoke).toHaveBeenLastCalledWith("sidecar_request", {
      method: "cron.remove",
      params: { job: "a1b2c3d4e5f6" },
    });
    expect(removed.removed).toBe(true);
    mocks.invoke.mockResolvedValue({
      db: "/h/db.sqlite", data_root: "/h", ticker_alive: true,
      heartbeat_age_seconds: 3, last_success_age_seconds: 60, last_error: null,
      estopped: false, jobs_total: 2, jobs_enabled: 1, next_due_at: "2026-10-05T09:00:00+08:00",
    });
    const status = await api.cronStatus();
    expect(mocks.invoke).toHaveBeenLastCalledWith("sidecar_request", {
      method: "cron.status",
      params: {},
    });
    expect(status.ticker_alive).toBe(true);
  });

  it("cronRuns:job+limit 透传到 cron.runs", async () => {
    mocks.invoke.mockResolvedValue({ db: "/h/db.sqlite", count: 0, executions: [] });
    await api.cronRuns({ job: "晨报", limit: 10 });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "cron.runs",
      params: { job: "晨报", limit: 10 },
    });
  });

  it("yamlList:零参调用 yaml.list;files 形状透传", async () => {
    mocks.invoke.mockResolvedValue({
      plugins_dir: "/p",
      files: [{ file: "/p/news.yaml", name: "news.yaml", parse_ok: true, category_id: "news", category_name: "新闻", sources: 3, error: null }],
    });
    const result = await api.yamlList();
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "yaml.list",
      params: {},
    });
    expect(result.files).toHaveLength(1);
    expect(result.files[0]?.parse_ok).toBe(true);
  });

  it("cron_create_failed 经 SidecarRequestError 抛出(code 原文)", async () => {
    mocks.invoke.mockRejectedValue(
      JSON.stringify({ code: "cron_create_failed", path: "params", message: "schedule 解析失败:未知形态「foo」" }),
    );
    const error = await api.cronCreate({ schedule: "foo", category: "/p/news.yaml" }).catch((err) => err);
    expect(error).toBeInstanceOf(SidecarRequestError);
    expect(error.code).toBe("cron_create_failed");
    expect(error.message).toContain("schedule 解析失败");
  });
});

describe("storeStateMark / storeStateMarkAll / storeStateImport(G9)", () => {
  it("mark:透传 keys/marker/value 到 store.state.mark;result 形状透传", async () => {
    mocks.invoke.mockResolvedValue({ updated: 2 });
    const result = await api.storeStateMark({ keys: ["dk-1", "dk-2"], marker: "read", value: true });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "store.state.mark",
      params: { keys: ["dk-1", "dk-2"], marker: "read", value: true },
    });
    expect(result.updated).toBe(2);
  });

  it("mark_all:透传 marker/value(可选 category)到 store.state.mark_all", async () => {
    mocks.invoke.mockResolvedValue({ updated: 7 });
    await api.storeStateMarkAll({ marker: "read", value: false });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "store.state.mark_all",
      params: { marker: "read", value: false },
    });
    await api.storeStateMarkAll({ marker: "starred", value: true, category: "ai-news" });
    expect(mocks.invoke).toHaveBeenLastCalledWith("sidecar_request", {
      method: "store.state.mark_all",
      params: { marker: "starred", value: true, category: "ai-news" },
    });
  });

  it("import:整 map 单请求透传到 store.state.import;imported/skipped 形状透传", async () => {
    mocks.invoke.mockResolvedValue({ imported: 2, skipped: 1 });
    const states = { "dk-1": { read: true }, "id:9": { starred: true }, "id:https://x": { later: true } };
    const result = await api.storeStateImport({ states });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "store.state.import",
      params: { states },
    });
    expect(result).toEqual({ imported: 2, skipped: 1 });
  });
});

describe("feedExport(G3)", () => {
  it("透传 format/path + 当前过滤视图(category × query)到 feed.export", async () => {
    mocks.invoke.mockResolvedValue({ path: "/tmp/f.jsonl", count: 3, bytes: 900 });
    const result = await api.feedExport({
      format: "jsonl",
      path: "/tmp/f.jsonl",
      category: "news",
      query: "rss",
    });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "feed.export",
      params: { format: "jsonl", path: "/tmp/f.jsonl", category: "news", query: "rss" },
    });
    expect(result.count).toBe(3);
  });

  it("export_path_invalid 经 SidecarRequestError 抛出(code 原文)", async () => {
    mocks.invoke.mockRejectedValue(
      JSON.stringify({ code: "export_path_invalid", path: "params.path", message: "导出路径必须是绝对路径" }),
    );
    const error = await api.feedExport({ format: "csv", path: "relative.csv" }).catch((err) => err);
    expect(error).toBeInstanceOf(SidecarRequestError);
    expect(error.code).toBe("export_path_invalid");
  });
});

describe("schedulePreview(G4)", () => {
  it("透传 file/count 到 schedule.preview;result 形状透传", async () => {
    mocks.invoke.mockResolvedValue({
      file: "/p/demo.yaml",
      schedule: "0 9 * * *",
      timezone: null,
      runs: ["2026-10-04T09:00:00+08:00"],
    });
    const result = await api.schedulePreview({ file: "/p/demo.yaml", count: 5 });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "schedule.preview",
      params: { file: "/p/demo.yaml", count: 5 },
    });
    expect(result.schedule).toBe("0 9 * * *");
    expect(result.runs).toHaveLength(1);
  });
});

describe("pushTest(G5 前半)", () => {
  it("透传 channel/target 到 push.test;stdout 通道 preview 回显", async () => {
    mocks.invoke.mockResolvedValue({ ok: true, channel: "stdout", preview: "MYIA 推送测试" });
    const result = await api.pushTest({ channel: "stdout" });
    expect(mocks.invoke).toHaveBeenCalledWith("sidecar_request", {
      method: "push.test",
      params: { channel: "stdout" },
    });
    expect(result.preview).toContain("MYIA 推送测试");
  });

  it("通道结构化错误(如 env_var_missing)code 原文透传", async () => {
    mocks.invoke.mockRejectedValue(
      JSON.stringify({ code: "env_var_missing", path: "params.channel", message: "FEISHU_BOT_TOKEN 未设置" }),
    );
    const error = await api.pushTest({ channel: "feishu_card" }).catch((err) => err);
    expect(error).toBeInstanceOf(SidecarRequestError);
    expect(error.code).toBe("env_var_missing");
  });
});
