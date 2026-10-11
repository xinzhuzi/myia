import { useEffect } from "react";

import { Navigate, Route, Routes } from "react-router-dom";

import { AppLayout } from "@/components/layout/app-layout";
import { CronScreen } from "@/screens/cron/cron-screen";
import { DashboardScreen } from "@/screens/dashboard/dashboard-screen";
import { FeedScreen } from "@/screens/feed/feed-screen";
import { LogsScreen } from "@/screens/logs/logs-screen";
import { MessagingScreen } from "@/screens/messaging/messaging-screen";
import { SettingsScreen } from "@/screens/settings/settings-screen";
import { SourcesScreen } from "@/screens/sources/sources-screen";
import { TgAccountScreen } from "@/screens/tg-account/tg-account-screen";
import { PlatformAccountsScreen } from "@/screens/platform-accounts/platform-accounts-screen";
import { YamlEditorScreen } from "@/screens/yaml-editor/yaml-editor-screen";

/**
 * 九屏路由(HashRouter:桌面 webview 下免服务端回退,最稳)。
 * 「/」= 仪表盘;未知路径一律回落仪表盘。
 *
 * 路由接的是 @/screens/* 真实实现(自带 health/doctor/run/logs 数据流)。
 * C 阶段的 @/routes/* 占位骨架已删(E4,10-03-v112-desktop-parity 顺风车:
 * 五屏真实实现在 v1.1 评审前从未进过打包产物,骨架页备查价值已尽,
 * B3「评分与反馈」分区落地后骨架里的参考位也失效)。
 *
 * /image 看图屏已拆(10-03-vision-pipeline 拍板①:图片理解并入情报管线,
 * 配置面留在设置屏 VisionForm;feed 屏出「图析」行)。
 * /yaml-editor = YAML配置(10-03-yaml-editor;原「配置编辑」,v10 随侧栏
 * 配置分组更名):品类 YAML 原文编辑屏,
 * 源管理行「编辑」带 ?file= 预选(位次=源管理之后,与侧栏一致)。
 * /messaging = 消息(10-03-messaging-ui):通道目录 + 推送规则挑对象,
 * 位次=采集之后、配置组之前(与侧栏一致;v10 原「配置编辑之后」注记随
 * 分组重排失真,一并更正);命名直白用「消息」,不用行话。
 * /cron = 定时任务(10-04-cron-ui):cron.* 九方法管理屏,位次=源管理之后
 * (与侧栏一致);与 CLI `myssia cron` 同一批 job 数据。
 * /tg-account = TG 账号(10-11-tg-multi-account-groups v10):Telegram 监控卡
 * 自设置屏抽出的独立屏,归侧栏「配置」组(位次=推送之后,与侧栏一致)。
 */
export default function App() {
  // 白窗修复握手(10-06-smoke-window-politeness R1):首屏挂载完成即通知壳层
  // 「可以亮窗了」——壳层把验证性亮窗(SMOKE_ROUTE/SHOW_ON_START)门控到此刻,
  // 窗口一出现就是成品而非白屏。动态 import:浏览器 dev 容器无 tauri api 时静默。
  useEffect(() => {
    void import("@tauri-apps/api/event")
      .then(({ emit }) => emit("myia:ui-ready"))
      .catch(() => {});
  }, []);

  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<DashboardScreen />} />
        <Route path="feed" element={<FeedScreen />} />
        <Route path="sources" element={<SourcesScreen />} />
        <Route path="cron" element={<CronScreen />} />
        <Route path="yaml-editor" element={<YamlEditorScreen />} />
        <Route path="messaging" element={<MessagingScreen />} />
        <Route path="logs" element={<LogsScreen />} />
        <Route path="tg-account" element={<TgAccountScreen />} />
        <Route path="platform-accounts" element={<PlatformAccountsScreen />} />
        <Route path="settings" element={<SettingsScreen />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
