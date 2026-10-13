// vitest 全局 setup(vite.config.ts test.setupFiles;2026-10-14 六域接线
// 批的门禁去 flake 面)。
//
// 只做一件事:把 @testing-library/dom 异步工具(findBy*/waitFor)的全局
// 预算从默认 1000ms 放宽到 5000ms。**断言语义零变化**——该发生的交互仍
// 须在预算内发生;放宽的只是调度饥饿容错:
//
// - 全量门禁 `just test` = pytest(约 2.5 分钟满载)后紧接 vitest,且开发
//   机常与并行会话的测试循环同机竞争;此负载下 testing-library 的 50ms
//   轮询定时器会被饿死,默认 1s 预算在轮询真正执行前就墙钟超时。
// - 实捕两例(均为关闭/刷新链路同步、行为正确、单独跑恒绿的用例):
//   sources.test.tsx「完成即弹详情弹窗…ESC 关闭」与 dashboard-screen
//   .test.tsx「跑一次:run.start → completed 事件 → 刷新」——高负载全量
//   跑 1/5 概率假红。
// - CI 空载时用例毫秒级完成,5s 上限几乎不被触及,不掩盖真实慢路径。
//
// 用例内显式传 `{ timeout }` 的仍按用例值为准(configure 只改默认)。
import { configure } from "@testing-library/dom";

configure({ asyncUtilTimeout: 5000 });
