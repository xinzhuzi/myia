import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createHashRouter, RouterProvider } from "react-router-dom";

import App from "./App.tsx";
import { ErrorBoundary } from "./components/error-boundary.tsx";
import { installUiLogging } from "./lib/log.ts";
import "./index.css";

// UI 日志面(10-07-unified-logging 批2):console 劫持(forwardConsole 模式
// → plugin JS API 落 shell.log)+ onerror/unhandledrejection 兜底,先于一切
// 渲染链安装(其后 ErrorBoundary/业务 console 全部经此落盘)。非 tauri
// 容器(浏览器 dev)零副作用。
installUiLogging();

// 数据路由(createHashRouter):hash 语义不变(桌面 webview 免服务端回退,最稳),
// 但换来 useBlocker —— 配置编辑屏的 SPA 路由级 dirty 守卫依赖它(design §3
// 「切文件/路由离开时 dirty 守卫」的路由半边;App.tsx 的 <Routes> 子树原样保留)。
const router = createHashRouter([{ path: "*", element: <App /> }]);

// 根级 ErrorBoundary(AC10):渲染崩溃 → console.error 留痕(经上方劫持链落
// shell.log)+ 极简回退(错误文本 + 重载钮)。裹在 RouterProvider 外层,
// 连路由初始化在内的整棵渲染树都在保护面内。
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ErrorBoundary>
      <RouterProvider router={router} />
    </ErrorBoundary>
  </StrictMode>,
);
