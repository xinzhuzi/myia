// UI 日志面(10-07-unified-logging 批2;design §6 AC10)。
//
// 机制按 grill 轮 1 勘误①:tauri-plugin-log 的 Webview target 方向是
// Rust→webview 显示,**不捕获**前端 console——UI console 汇入正路 = 官方
// 文档 forwardConsole 用户态模式:劫持 console.* 原样执行后调
// @tauri-apps/plugin-log JS fn(invoke plugin:log|log,Rust 端记
// target=webview 流入全部 targets → <数据根>/logs/shell.log)。
// attachConsole 是反向订阅(Rust 日志打到 webview 控制台),弃。
//
// 非 tauri 容器(浏览器 dev)零副作用:__TAURI_INTERNALS__ 不在场即只走
// 原生 console,不尝试 invoke。决议④:UI 日志只落 shell 文件,不进日志屏。
import { error as pluginError, info as pluginInfo, warn as pluginWarn } from "@tauri-apps/plugin-log";

/** 劫持安装旗(幂等:重复调用零重挂,防 handler 翻倍转发)。 */
const installed = { console: false, errors: false };
/** 卸装凭据(console 原函数 + 兜底 handler 引用;测试隔离用)。 */
const uninstallHandles: Array<() => void> = [];

/** tauri 容器判定(webview 注入 __TAURI_INTERNALS__;浏览器 dev 无此件)。 */
function inTauriContainer(): boolean {
  return typeof window !== "undefined" && "__TAURI_INTERNALS__" in window;
}

/** 单值格式化:Error 取 name+message+堆栈首行,对象 JSON 化(失败回 String)。 */
function formatValue(value: unknown): string {
  if (value instanceof Error) {
    const firstStackLine = value.stack?.split("\n", 2)[1]?.trim() ?? "";
    return firstStackLine
      ? `${value.name}: ${value.message} @ ${firstStackLine}`
      : `${value.name}: ${value.message}`;
  }
  if (typeof value === "string") return value;
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

/** 多参数拼一条消息(空格分隔,与 console 展示语义一致)。 */
function formatArgs(args: unknown[]): string {
  return args.map(formatValue).join(" ");
}

type PluginLevel = "info" | "warn" | "error";

const pluginByLevel: Record<PluginLevel, (message: string) => Promise<void>> = {
  info: pluginInfo,
  warn: pluginWarn,
  error: pluginError,
};

/** 单条转发(invoke 失败静默:非 tauri 容器兜底,日志链不得反噬 UI)。 */
function forward(level: PluginLevel, message: string): void {
  if (!inTauriContainer()) return;
  pluginByLevel[level](message).catch(() => {});
}

/**
 * 劫持 console.log/info/warn/error(决议⑥全劫持四档):原函数先执行
 * (devtools 展示语义不变),再按级转发 plugin JS API 落 shell.log。
 * console.log 无独立 log 级(plugin JS 面按 log-crate 五级),按官方
 * forwardConsole 模式映 info。幂等。
 */
export function installConsoleForward(): void {
  if (installed.console) return;
  installed.console = true;
  const pairs = [
    { consoleFn: "log", level: "info" },
    { consoleFn: "info", level: "info" },
    { consoleFn: "warn", level: "warn" },
    { consoleFn: "error", level: "error" },
  ] as const;
  for (const { consoleFn, level } of pairs) {
    const original = console[consoleFn].bind(console);
    uninstallHandles.push(() => {
      console[consoleFn] = original;
    });
    console[consoleFn] = (...args: unknown[]) => {
      original(...args);
      forward(level, formatArgs(args));
    };
  }
}

/**
 * 全局错误兜底:window.onerror(addEventListener "error";ErrorEvent 五参
 * 形态)+ unhandledrejection(Promise 未捕获拒绝)→ 前缀化(来源+消息+
 * 位置/堆栈首行)经 forward 落盘。不走 console.error 转发:console 劫持下
 * 会双份,且未捕获错误 webview 运行时本就原生报告 devtools。幂等。
 */
export function installGlobalErrorHandlers(): void {
  if (installed.errors) return;
  installed.errors = true;
  const onError = (event: ErrorEvent) => {
    // event.error 优先(带堆栈);裸 ErrorEvent 仅有 message+位置
    const detail = formatValue(event.error ?? event.message);
    const location = event.filename
      ? ` @ ${event.filename}:${event.lineno}:${event.colno}`
      : "";
    forward("error", `window.onerror: ${detail}${location}`);
  };
  const onRejection = (event: PromiseRejectionEvent) => {
    forward("error", `unhandledrejection: ${formatValue(event.reason)}`);
  };
  window.addEventListener("error", onError);
  window.addEventListener("unhandledrejection", onRejection);
  uninstallHandles.push(() => {
    window.removeEventListener("error", onError);
    window.removeEventListener("unhandledrejection", onRejection);
  });
}

/** App 启动接线入口(main.tsx 调用一次):console 劫持 + 错误兜底。 */
export function installUiLogging(): void {
  installConsoleForward();
  installGlobalErrorHandlers();
}

/**
 * 撤安装(**仅测试隔离用**):复位安装旗 + 还原 console 原函数 + 摘兜底
 * handler。生产链路不调用(App 生命周期内常驻)。
 */
export function __uninstallForTests(): void {
  while (uninstallHandles.length > 0) {
    uninstallHandles.pop()?.();
  }
  installed.console = false;
  installed.errors = false;
}
