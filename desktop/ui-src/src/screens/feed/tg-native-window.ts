/**
 * TG 原生视图窗口注册表(design-v9 §2.4,10-09-tg-category-entry v9)。
 *
 * AC33(预览升级)与 AC34(原生视图切换)物理上是同一个能力:应用内
 * WebviewWindow 加载 `https://web.telegram.org/k/#@<频道名>`。两入口
 * (监控台「原生网页预览」钮 / 3 级工具条「原生视图」段)统一收敛到
 * openOrFocusNative,避免同频道开出两个 /k/ 实例(每个都是完整 SPA +
 * MTProto websocket,内存 100-300MB 级)。
 *
 * 窗口管理定稿(design-v9 §2.2/§2.3 方案 A + 案 c):
 * - 独立窗(decorations 缺省 true 自带标题栏),移动/缩放/红绿灯全归 macOS
 *   原生,零几何同步代码;
 * - 每频道一窗:键/label 口径 = **t.me 频道名**(telegramChannelNameOf 从
 *   /k/ 深链反推,design-v9 §2.3「getByLabel(tg-native-<新频道>)」词面)——
 *   不用源名做键:两个源若推导出同一 t.me 频道,同频道只开一窗(聚焦复用),
 *   「同频道不出两个 /k/ 实例」的 §0 动机由键口径结构性保证;源名只进
 *   title(展示)与注意力表(段控件状态)。
 * - 重复点击 getByLabel 命中 → setFocus,未命中 → 建窗。旧「label 带时间戳
 *   防撞」(v3 AC11)反向修正:稳定 label 是聚焦语义的前提,双击双触发撞
 *   label 从缺陷变为幂等信号(tauri://error 后复查命中 = 视同 focused);
 * - 上限 3(getAll 过前缀对账,不靠本地 Map 计数):每个 /k/ 实例独立
 *   websocket,内存与连接数双帽,与 watcher max_accounts=3(web_line.py)
 *   同量级纪律。不做 LRU 自动关(悄悄关用户的窗 = 惊吓)。
 *
 * 登录态:WKWebView 持久存储(WebviewOptions incognito 缺省 false),窗亡
 * 存储不亡,重启 app 免重扫;与 watcher 的 Playwright 配置档互不相通
 * (双会话披露见 feed-screen 首开注记,design-v9 §1.3)。
 */
import { WebviewWindow } from "@tauri-apps/api/webviewWindow";

/** 原生视图窗 label 前缀(稳定 label;getAll 对账上限以此过滤) */
export const TG_NATIVE_LABEL_PREFIX = "tg-native-";

/** /k/ 深链唯一合法前缀(F8 结构性域白名单:openOrFocusNative 只收本模块
 *  口径的深链,白名单从 capabilities description 的词面约束升级为代码约束;
 *  越界 = 同步 throw,走调用方「窗口创建异常」catch 路径) */
export const TG_NATIVE_K_URL_PREFIX = "https://web.telegram.org/k/#@";

/** 原生视图窗上限(design-v9 §2.4:内存 + MTProto 连接数双帽) */
export const TG_NATIVE_WINDOW_CAP = 3;

/** 开窗四态语义:created = 新建(首开与否由 tgNativeCreatedBeforeOf 区分,
 *  供调用方条件化「首次」词面);focused = 命中既有窗聚焦;capped = 上限拒开。
 *  异步真失败不走返回值,走 onCreateError("failed")。 */
export type OpenNativeResult = "created" | "focused" | "capped";

/** 视图注意力(design-v9 §2.1 段控件「当前看哪张皮」;键 = t.me 频道名,
 *  会话内持久) */
export type NativeViewFocus = "intel" | "native";

/** 原生窗句柄子面(真实 = WebviewWindow 实例;测试缝只认这三个成员) */
export interface NativeWindowHandle {
  label: string;
  once(event: string, handler: (event: unknown) => void): Promise<unknown>;
  setFocus(): Promise<void>;
}

/** 窗口系统依赖缝(测试注入替身;真实实现绑 @tauri-apps/api webviewWindow) */
export interface NativeWindowDeps {
  getByLabel(label: string): Promise<NativeWindowHandle | null>;
  getAll(): Promise<{ label: string }[]>;
  create(label: string, options: Record<string, unknown>): NativeWindowHandle;
}

const realDeps: NativeWindowDeps = {
  getByLabel: (label) => WebviewWindow.getByLabel(label) as Promise<NativeWindowHandle | null>,
  getAll: () => WebviewWindow.getAll(),
  create: (label, options) => new WebviewWindow(label, options) as unknown as NativeWindowHandle,
};

/** 活窗登记(label → t.me 频道名)。仅作 bookkeeping,存在性判定一律实时走
 *  deps.getByLabel 对账 —— 主窗刷新(HMR/导航)后本地 Map 可能滞后于真窗,
 *  不信 Map 断存在(design-v9 §2.4)。 */
const registry = new Map<string, string>();

/** 视图注意力表(键 = t.me 频道名 → intel/native)。模块级单例 = 会话内
 *  持久;键跟窗走而非跟源走:窗亡时单点清理(见 destroyed 回调)即覆盖
 *  所有正在看该频道的源(深检 F1)。 */
const focusByKey = new Map<string, NativeViewFocus>();

/** 本会话开过窗的键集(F4b:「首次需扫码登录一次」的判据 —— created 只在
 *  首次出全量披露,关窗重开不再假预告;异步真失败时回删,重试仍按首开
 *  披露 —— 失败窗从未渲染过 QR 页,重试对用户仍是第一次)。 */
const createdOnceKeys = new Set<string>();

type DestroyedListener = (key: string, label: string) => void;
const destroyedListeners = new Set<DestroyedListener>();

/** 原生窗销毁订阅(UI 段控件回落用;返回解绑函数)。模块级监听不随组件
 *  卸载消失,主窗刷新后重挂仍能对账。 */
export function onNativeWindowDestroyed(listener: DestroyedListener): () => void {
  destroyedListeners.add(listener);
  return () => {
    destroyedListeners.delete(listener);
  };
}

/** /k/ 深链整链锚定(词表与 api.telegramChannelNameOf 的捕获组同源:
 *  [A-Za-z][A-Za-z0-9_]{2,} = t.me 用户名词表 —— 深链本体即 telegramKUrlOf
 *  按该词表构造,键提取同词表 = 同源推导闭环;整链锚定杜绝 query/尾段注入) */
const K_URL_RE = /^https:\/\/web\.telegram\.org\/k\/#@([A-Za-z][A-Za-z0-9_]{2,})$/;

/** /k/ 深链 → 注册键(锚内 t.me 频道名)。非本模块口径的 url 一律 null ——
 *  调用方(openOrFocusNative)对 null 同步 throw,白名单是代码约束不是
 *  注释约定(深检 F8)。 */
export function tgNativeKeyOf(kUrl: string | null | undefined): string | null {
  if (!kUrl) return null;
  const match = K_URL_RE.exec(kUrl);
  return match ? match[1] : null;
}

/** 窗 label:键 → `tg-native-<t.me 频道名>`(design-v9 §2.3 词面)。
 *  Tauri label 词表仅 [A-Za-z0-9-/:_],键本身出自词表 [A-Za-z0-9_],折叠
 *  规则保留作纵深防御(防未来键口径漂移时构造即炸)。 */
export function tgNativeLabelOf(key: string): string {
  return TG_NATIVE_LABEL_PREFIX + key.replace(/[^A-Za-z0-9-/:_]/g, "_");
}

/** 该频道本会话是否开过窗(「首次」词面判据,F4b) */
export function tgNativeCreatedBeforeOf(key: string): boolean {
  return createdOnceKeys.has(tgNativeLabelOf(key));
}

/** 视图注意力读取(未登记 = intel 缺省;情报视图是应用的本地时间线,
 *  永不卸载,故缺省侧永远是它) */
export function nativeViewFocusOf(key: string): NativeViewFocus {
  return focusByKey.get(key) ?? "intel";
}

/** 视图注意力登记(仅应用内存,不落 localStorage —— 会话内持久即可) */
export function setNativeViewFocus(key: string, focus: NativeViewFocus): void {
  focusByKey.set(key, focus);
}

/** 该频道原生窗是否活着(实时 getByLabel 对账,不信任本地 Map;远程窗
 *  系统查询失败一律视作不活,调用方按「未开」呈现,不抛)。 */
export async function isNativeWindowOpen(kUrl: string, deps?: Partial<NativeWindowDeps>): Promise<boolean> {
  const key = tgNativeKeyOf(kUrl);
  if (key === null) return false;
  try {
    const handle = await { ...realDeps, ...deps }.getByLabel(tgNativeLabelOf(key));
    return handle !== null;
  } catch {
    return false;
  }
}

/** 存活态单点清理:登记/注意力表回收 + 广播订阅者(深检 F1/F2:清理不依赖
 *  组件订阅者存活,组件层只负责即时 UI 镜像;真失败与窗亡同路)。
 *  forgetCreated 仅真失败走:失败窗从未渲染过 QR 页,重试对用户仍是第一次,
 *  回收首开记忆让重试重新全量披露;窗亡(destroyed)不回收 —— 本会话已
 *  披露过一次,关窗重开不再假预告「首次」(深检 F4b)。 */
function releaseNativeWindow(key: string, label: string, opts?: { forgetCreated?: boolean }): void {
  registry.delete(label);
  focusByKey.delete(key);
  if (opts?.forgetCreated) createdOnceKeys.delete(label);
  destroyedListeners.forEach((listener) => listener(key, label));
}

/**
 * 开/聚焦该频道的 /k/ 原生窗(两入口统一收敛点,design-v9 §0/§2.4)。
 *
 * kUrl 只收本模块口径的 /k/ 深链(TG_NATIVE_K_URL_PREFIX + 可推导频道名),
 * 越界同步 throw → 调用方 catch 出「窗口创建异常」注记(深检 F8)。
 *
 * 次序:getByLabel 命中 → setFocus 返 focused(聚焦不受上限拦,重复点击
 * 语义优先)→ 未命中 → 活窗数(getAll 过前缀对账)≥ 3 → capped → 建窗返
 * created 并登记 destroyed/error 监听。
 *
 * 异步失败走 onCreateError 回调(返回值承载不了迟到事件):
 * - "focused" = 双击竞态兜底(tauri://error 后复查 getByLabel 命中,另一
 *   发已建窗成功,幂等视同聚焦,调用方不误报失败);
 * - "failed" = 建窗真失败(web.telegram.org 不可达/被拒),单点清理存活态
 *   (releaseNativeWindow:登记/注意力/首开记忆回收 + 广播)后回调,调用方
 *   出回退注记(design-v9 §1.2,不自动改开 t.me/s —— 失败原因对两种目标同真)。
 */
export async function openOrFocusNative(
  kUrl: string,
  options?: {
    title?: string;
    onCreateError?: (resolved: "focused" | "failed") => void;
    deps?: Partial<NativeWindowDeps>;
  },
): Promise<OpenNativeResult> {
  const key = tgNativeKeyOf(kUrl);
  if (key === null) {
    throw new Error(`kUrl 非法:只收 ${TG_NATIVE_K_URL_PREFIX}<t.me 频道名> 深链,收到:${kUrl}`);
  }
  const deps: NativeWindowDeps = { ...realDeps, ...options?.deps };
  const label = tgNativeLabelOf(key);
  const existing = await deps.getByLabel(label);
  if (existing) {
    // 聚焦尽力而为:窗活着即语义成立,个别环境聚焦被拒不让整条链报错
    try {
      await existing.setFocus();
    } catch {
      // 聚焦失败不误报(窗已在,用户可从程序坞/「窗口」菜单点回)
    }
    return "focused";
  }
  const openNative = (await deps.getAll()).filter(
    (win) => typeof win.label === "string" && win.label.startsWith(TG_NATIVE_LABEL_PREFIX),
  );
  if (openNative.length >= TG_NATIVE_WINDOW_CAP) return "capped";
  // 尺寸对齐 TG Web 桌面版三栏最小可用宽(design-v9 §2.2 方案 A);
  // decorations 缺省 true = 自带标题栏红绿灯,零自绘关闭面
  const handle = deps.create(label, {
    url: kUrl,
    title: options?.title ?? `TG · ${key}`,
    width: 1100,
    height: 780,
    minWidth: 640,
    minHeight: 480,
  });
  registry.set(label, key);
  void handle.once("tauri://destroyed", () => {
    // 模块级单点清理(F1):注意力表随窗亡回收,不依赖组件订阅者存活 ——
    // 用户在别的渠道/层级关窗,回进该频道时段控件如实回落情报视图
    releaseNativeWindow(key, label);
  });
  void handle.once("tauri://error", () => {
    void deps
      .getByLabel(label)
      .then((race) => {
        if (race) {
          // 竞态兜底:并发另一发已建窗成功 → 幂等视同聚焦,不误报
          try {
            void race.setFocus().catch(() => undefined);
          } catch {
            // 同上,聚焦尽力而为
          }
          options?.onCreateError?.("focused");
          return;
        }
        // 真失败(F2):存活态单点清理(组件红点/段态经广播同步回落),
        // 不留「注记说失败、徽标还亮着」的矛盾同屏;回收首开记忆(重试
        // 仍按首开披露)
        releaseNativeWindow(key, label, { forgetCreated: true });
        options?.onCreateError?.("failed");
      })
      .catch(() => {
        releaseNativeWindow(key, label, { forgetCreated: true });
        options?.onCreateError?.("failed");
      });
  });
  createdOnceKeys.add(label);
  return "created";
}

/** 测试缝:清空登记/注意力/首开记忆表(注册表挂模块级,用例间需复位互不
 *  牵连) */
export function resetTgNativeForTests(): void {
  registry.clear();
  focusByKey.clear();
  createdOnceKeys.clear();
  destroyedListeners.clear();
}

/** 测试对账:当前登记的活窗 label 集(存在性真相仍以 getByLabel 为准) */
export function tgNativeRegisteredLabelsForTests(): string[] {
  return [...registry.keys()];
}
