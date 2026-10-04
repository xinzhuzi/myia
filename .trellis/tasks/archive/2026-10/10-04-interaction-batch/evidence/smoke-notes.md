# A 档无头冒烟说明(独立质检,2026-10-04)

## 设施(仓库零改动,脚本在 /tmp/myia-qc/)

- **vite dev server**:`npm --prefix desktop/ui-src run dev`,经 **http://localhost:5173**(localhost,非 127.0.0.1)访问。
- **bridge(/tmp/myia-qc/bridge.mjs,:8787)**:spawn `.venv/bin/python desktop/entry.py serve`,`MYIA_HOME=/tmp/myia-qc/home-a`(隔离沙箱,12 条种子数据由 seed_a.py 经 SQLiteStore.save_item 直造:四个时间桶 × 品类三档 + 无品类,a2 预置服务端已读);HTTP `/rpc` 转发 stdin/stdout 行协议,`/events` SSE 推无 id 事件行,`/log` 记录全部 RPC(页面→sidecar 真链证据),全端点 CORS 放行(页面 origin :5173)。
- **shim(CDP `Page.addScriptToEvaluateOnNewDocument` 注入,先于一切应用脚本)**:`window.__TAURI_INTERNALS__.invoke/transformCallback/unregisterCallback`(`sidecar_request` → fetch bridge;`plugin:event|listen/unlisten` → 本地回调表;`sidecar_restart`/`plugin:shell|open` 记录到 `__QC_INVOKE_LOG__` 温和应答)+ `window.__TAURI_EVENT_PLUGIN_INTERNALS__.unregisterListener` + EventSource 事件泵。
- **驱动(/tmp/myia-qc/driver.mjs)**:headless Chrome(--headless=new,:9223)+ 原生 WebSocket CDP;键盘 `Input.dispatchKeyEvent`(⌘K=modifiers 4)、鼠标 `mousePressed/Released`(右键 button=right)、探针 `Runtime.evaluate`、实拍 `Page.captureScreenshot`。

## headless 工具链怪癖(影响过探针,已绕开,非产品缺陷)

1. **帧按需推进**:无截图/帧请求时 rAF 不跑 → dropdown-menu 基件的定位 rAF(fixed 无 top/left)与 palette 的聚焦 rAF 不执行,菜单滞留 body 尾默认位。绕法:开菜单后先 `captureScreenshot` 驱动一帧(P5 右键菜单点击成功正因当时有 04 截图在先)。真实窗口有连续合成帧,无此问题。
2. **CDP `dispatchMouseEvent` 的单击计数参数名是 `clickCount`**(非 clicks):漏它 Chrome 不派发 click 合成事件——所有左键点击一度全部无效(右键 contextmenu / 键盘不受影响)。
3. **evaluate 表达式以 `[` 开头会 SyntaxError**(V8/CDP 组合怪癖):数组表达式统一包 `JSON.stringify(...)` 取回。

## 结果

- **39/39 全绿**(明细 a-smoke-probe.json):j/k 巡游(落首卡/边界钳制/k 上移/focus 环/hover 让位/输入框守卫)、⌘K 命令面板(唤起/过滤/↓ 巡游 aria-activedescendant/Enter 导航/Esc 关闭/顶栏触发器)、右键菜单(四动作/标已读走 store.state.mark/标签随态)、侧栏折叠([ 键 + 底部按钮/localStorage 持久)、显示选项(未读优先浮前/按品类分组/持久);附带 B UI 链页面侧证据(能力门 version → store.state.import 一次性搬迁 → 投影生效 → 旧键保留)。
- 实拍:01 加载态、02 j/k focus 环、03 命令面板、04 右键菜单、05/06 折叠两态、07a/07b 显示菜单展开、07 品类分组。
- bridge RPC 全量日志:a-smoke-bridge-rpc.log.json。
