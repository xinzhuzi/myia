/**
 * 系统级确认弹窗(全 App 确认类弹窗的唯一入口;散用 window.confirm 属违例):
 * - Tauri 桌面 = @tauri-apps/plugin-dialog 原生 confirm(macOS = NSAlert 系统弹窗,
 *   Windows = 原生 MessageBox;10-14-native-system-dialog),带标题/图标/动词化按钮;
 * - 非 Tauri 环境(jsdom 测试、浏览器直开)= window.confirm 回退,正文文案原样
 *   透传(既有 spy 断言零改动)。
 * Tauri 判定 = window.__TAURI_INTERNALS__(生产由 Tauri 注入;无头冒烟 shim 同款事实源)。
 * 权限面 = capabilities/default.json 的 dialog:allow-confirm 单条(dialog:default
 * 仅含 message/save/open,实证插件 permissions/default.toml)。
 */
export interface SystemConfirmOptions {
  /** 弹窗标题(破框直言,如「删除定时任务」;缺省由系统显示应用名) */
  title?: string;
  /** 正文(沿用原 window.confirm 文案;\n 原生弹窗按换行渲染) */
  message: string;
  /** 图标语义:破坏性操作 warning(黄三角),中性询问 info;确认类默认警示 */
  kind?: "info" | "warning";
  /** 确认钮文案(动词,如「删除」);缺省「确定」 */
  okLabel?: string;
  /** 取消钮文案;缺省「取消」 */
  cancelLabel?: string;
}

export async function systemConfirm(options: SystemConfirmOptions): Promise<boolean> {
  if (typeof window !== "undefined" && "__TAURI_INTERNALS__" in window) {
    const dialog = await import("@tauri-apps/plugin-dialog");
    try {
      return await dialog.confirm(options.message, {
        title: options.title,
        kind: options.kind ?? "warning",
        okLabel: options.okLabel ?? "确定",
        cancelLabel: options.cancelLabel ?? "取消",
      });
    } catch (error) {
      // 原生通道故障(ACL 拒/插件崩)= 安全缺省「取消」:破坏性动作绝不在
      // 无确认下放行;守卫类(放弃/关闭)同样按取消留人,重试即恢复。
      // 实锤教训:旧包 polyfill 的同类拒绝只留 unhandledrejection,静默断肢。
      console.error("systemConfirm 原生 confirm 失败,按取消处理", error);
      return false;
    }
  }
  return window.confirm(options.message);
}
