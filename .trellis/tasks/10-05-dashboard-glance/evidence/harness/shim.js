/**
 * 浏览器内 Tauri IPC shim(S7;仿 .trellis/tasks/archive/2026-10/10-03-fe-small-batch/
 * evidence/touch-harness/shim.js 与 .zcode/smoke/dash-shot.cjs 内联 shim)。
 *
 * invoke("sidecar_request") → mock 桥 POST /rpc(拒绝值 = 错误对象 JSON 字符串,
 * 与 Rust Err(String) 同形状,client.ts toSidecarError 解析路径不变);
 * 事件订阅(plugin:event|listen)返回句柄零事件(mock 桥无 SSE,dashboard 只
 * 订阅 completed 刷新,无事件即不刷新,冒烟无碍)。window.__rpc 留调用痕
 * 供驱动脚本断言六方法全被拉过。
 */
(() => {
  const BRIDGE = "http://127.0.0.1:8790";
  let cbSeq = 0;
  window.__rpc = [];
  const invoke = async (cmd, args = {}, options) => {
    if (cmd === "sidecar_request") {
      const method = args && args.method;
      const t0 = performance.now();
      const res = await fetch(BRIDGE + "/rpc", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ method, params: (args && args.params) || {} }),
      });
      const msg = await res.json();
      const ms = Math.round(performance.now() - t0);
      if (msg && msg.error) {
        window.__rpc.push({ method, ms, err: msg.error.code });
        throw JSON.stringify(msg.error);
      }
      window.__rpc.push({ method, ms });
      return msg.result;
    }
    if (cmd.startsWith("plugin:event|") || cmd === "plugin:app|version") return 0;
    throw JSON.stringify({ code: "unsupported_command", path: "$", message: "cmd " + cmd });
  };
  window.__TAURI_INTERNALS__ = {
    invoke,
    transformCallback: () => ++cbSeq,
    unregisterCallback: () => {},
    metadata: {},
  };
})();
