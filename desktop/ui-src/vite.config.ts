import { fileURLToPath, URL } from "node:url";

import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

// MYIA 桌面前端构建配置。
// - 产物输出到 desktop/ui/(tauri.conf.json build.frontendDist 指向处,不动);
//   outDir 在本目录之外,vite 默认不清空,必须显式 emptyOutDir 清掉旧产物。
// - beforeBuildCommand(desktop/src-tauri/tauri.conf.json)即 `npm run build`。
// - vitest(`npm test`)与构建共用本配置:jsdom 环境跑 5 屏组件测试
//   (screens/*/*.test.tsx 头部另有 @vitest-environment jsdom 标注,双保险)。
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  build: {
    outDir: "../ui",
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    strictPort: true,
  },
  test: {
    environment: "jsdom",
    // 组件测试统一 setup:testing-library 异步工具(findBy*/waitFor)预算
    // 放宽到 5s(setup-testing-library.ts)。断言语义不变(该发生的仍须
    // 发生),只容忍调度饥饿:全量门禁(just test = pytest 2.5min 后紧接
    // vitest,且与并行开发会话的测试循环同机竞争)高负载下 50ms 轮询会被
    // 饿死,默认 1s 预算在轮询真正跑完前就超时 → 行为正确的用例假红
    // (2026-10-14 实捕 sources ESC / dashboard run-once 两例,单独跑恒绿)。
    setupFiles: ["./src/test/setup-testing-library.ts"],
    // 单测超时 5s → 30s:同一负载家族的另一面——真定时器轮询用例(如
    // tg-account 5s 体检轮询)与多段 waitFor 串接的用例,在门禁满载下墙钟
    // 膨胀 1.6x+,5s 默认值会打出纯 runner 帧的 runWithTimeout 假红
    // (2026-10-14 门禁实捕 1 例,栈零用户帧;显式自带 timeout 的用例不受
    // 影响)。断言语义零变化;空载用例毫秒级完成不触及上限。
    testTimeout: 30_000,
  },
  // Tauri IPC 与打包环境变量前缀;clearScreen 关闭以免冲掉 sidecar 的终端日志。
  envPrefix: ["VITE_", "TAURI_"],
  clearScreen: false,
});
