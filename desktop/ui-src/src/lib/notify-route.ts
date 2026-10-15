/**
 * 通知点击深链(10-15-notify-deeplink):壳侧 mac-notification-sys
 * `wait_for_click` 拿到横幅点击后 emit `notify:navigate`(载荷 =
 * 条目 source = 会话名/feed 渠道键 + item_key = 锚定条目 dedup_key),
 * 本模块把事件转成导航:
 *
 * - 挂起槽(pendingRoute:source + itemKey):冷热两态共用——壳事件可能
 *   在 feed 屏挂载前(他屏在跑)或后到达;他屏到达 = 先
 *   router.navigate("/feed") 再由 feed 屏挂载时消费挂起槽,已在 feed =
 *   窗口事件即时消费;itemKey 让 3 级定位到具体消息(滚入视口 + 高亮),
 *   缺 = 会话级(10-15 粒度细化);
 * - 安装点 = main.tsx(router 在场;全屏恒单实例);
 * - 非事件来源的兜底:URL `?notify=<source>`(冷启动直链调试面,会话级;
 *   生产冷启动点击由系统拉起 app,壳线程已随旧进程消亡,如实不深链)。
 */
import { listen } from "@tauri-apps/api/event";

/** 挂起深链路由:source 必有(否则不存),itemKey 可缺(= 会话级)。 */
export interface NotifyRoute {
  source: string;
  itemKey: string | null;
}

let pendingRoute: NotifyRoute | null = null;

/** 存挂起路由(壳事件/URL 参数两源);source 空串不存。 */
export function setPendingNotifyChannel(
  source: string | null | undefined,
  itemKey?: string | null,
): void {
  pendingRoute =
    source && source.trim() !== ""
      ? { source, itemKey: itemKey && itemKey.trim() !== "" ? itemKey : null }
      : null;
}

/** 取走挂起路由(一次性消费;无则 null)。 */
export function takePendingNotifyChannel(): NotifyRoute | null {
  const value = pendingRoute;
  pendingRoute = null;
  return value;
}

/** feed 屏即时信号名(壳事件到达且已在 feed 屏时,屏内重开目标渠道)。 */
export const NOTIFY_ROUTE_SIGNAL = "myia:notify-route";

/**
 * 安装壳事件监听(main.tsx 一次)。非 tauri 容器(浏览器 dev/jsdom 测试)
 * 零安装零副作用——与 lib/log.ts 同款判式。
 */
export async function installNotifyNavigation(router: { navigate: (to: string) => Promise<void> | void }): Promise<void> {
  if (typeof window === "undefined" || !("__TAURI_INTERNALS__" in window)) return;
  await listen<{ source: string | null; item_key: string | null }>("notify:navigate", (event) => {
    const source = event.payload?.source ?? null;
    const itemKey = event.payload?.item_key ?? null;
    setPendingNotifyChannel(source, itemKey);
    if (source === null) return;
    window.dispatchEvent(new CustomEvent(NOTIFY_ROUTE_SIGNAL, { detail: source }));
    if (!window.location.hash.startsWith("#/feed")) {
      void router.navigate("/feed");
    }
  });
}
