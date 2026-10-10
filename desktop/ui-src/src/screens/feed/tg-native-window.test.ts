// @vitest-environment jsdom
/**
 * TG 原生视图窗口注册表单测(design-v9 §2.4/§6,10-09-tg-category-entry v9;
 * 深检第 1 轮 F1/F2/F4/F4b/F8 随动)。被测模块把 WebviewWindow 系统依赖收敛
 * 成 NativeWindowDeps 注入缝,本文件全程用假窗替身(零 @tauri-apps mock、零
 * 真实窗口);注册表/注意力/首开记忆挂模块级,each beforeEach reset 互不牵连。
 * 覆盖:created(构造参数)/ focused(命中聚焦,构造零次)/ 竞态幂等(error
 * 后复查命中 = focused 不误报)/ capped(前缀对账,main 不计)/ destroyed
 * (登记 + 注意力表模块级回收 F1 + 订阅广播 + 解绑)/ 异步真失败(存活态
 * 单点清理 + 广播 F2 + 首开记忆回收)/ 键口径 = t.me 频道名(两源同频道
 * 聚焦复用同窗 F4)/ 越界 kUrl 同步 throw(F8 结构性白名单)/ 首开记忆
 * (F4b:created 记忆、destroyed 不回收、failed 回收)/ isNativeWindowOpen
 * (实时对账,查询抛错 = false)/ label 折叠 / 注意力表会话内持久。
 */
import { beforeEach, describe, expect, it, vi } from "vitest";

import {
  isNativeWindowOpen,
  nativeViewFocusOf,
  onNativeWindowDestroyed,
  openOrFocusNative,
  resetTgNativeForTests,
  setNativeViewFocus,
  tgNativeCreatedBeforeOf,
  tgNativeKeyOf,
  tgNativeLabelOf,
  tgNativeRegisteredLabelsForTests,
  TG_NATIVE_K_URL_PREFIX,
  TG_NATIVE_LABEL_PREFIX,
  type NativeWindowDeps,
  type NativeWindowHandle,
} from "./tg-native-window";

const K_URL = "https://web.telegram.org/k/#@mihomo_party";

/** 可控假窗:once 捕获事件回调(测试手动 __fire 触发),setFocus 记调用;
 *  destroyed 拟真 = 同步把自己从窗口系统摘除(真实系统销毁即从 getAll 消失,
 *  getByLabel 随之 miss)。 */
function fakeHandle(label: string, onFire?: (event: string) => void): NativeWindowHandle & { __fire(event: string): void } {
  const callbacks = new Map<string, (event: unknown) => void>();
  return {
    label,
    once: vi.fn(async (event: string, handler: (event: unknown) => void) => {
      callbacks.set(event, handler);
      return () => undefined;
    }),
    setFocus: vi.fn(async () => undefined),
    __fire: (event: string) => {
      onFire?.(event);
      callbacks.get(event)?.({ event, payload: null });
    },
  };
}

type FakeHandle = ReturnType<typeof fakeHandle>;

/** 假窗口系统:existing = 预置活窗 label 集;create 把新窗登记进同一张表 */
function fakeDeps(existing: string[] = []): NativeWindowDeps & {
  create: ReturnType<typeof vi.fn>;
  handles: Map<string, FakeHandle>;
} {
  const handles = new Map<string, FakeHandle>();
  for (const label of existing) handles.set(label, fakeHandle(label));
  const deps = {
    handles,
    getByLabel: vi.fn(async (label: string) => handles.get(label) ?? null),
    getAll: vi.fn(async () => [...handles.keys()].map((label) => ({ label }))),
    create: vi.fn((label: string, _options: Record<string, unknown>) => {
      const handle = fakeHandle(label, (event) => {
        if (event === "tauri://destroyed") handles.delete(label);
      });
      handles.set(label, handle);
      return handle;
    }),
  };
  return deps;
}

describe("tg-native-window 注册表(v9 原生视图窗口管理)", () => {
  beforeEach(() => {
    resetTgNativeForTests();
  });

  it("created:getByLabel 未命中 → 构造一次,参数 = t.me 频道名 label(F4 键口径)+ /k/ url + title + TG Web 桌面尺寸;decorations/incognito 恒不设", async () => {
    const deps = fakeDeps();
    const result = await openOrFocusNative(K_URL, { title: "TG · mihomo_party", deps });
    expect(result).toBe("created");
    expect(deps.create).toHaveBeenCalledTimes(1);
    expect(deps.create).toHaveBeenCalledWith(
      "tg-native-mihomo_party",
      expect.objectContaining({
        url: K_URL,
        title: "TG · mihomo_party",
        width: 1100,
        height: 780,
        minWidth: 640,
        minHeight: 480,
      }),
    );
    const options = deps.create.mock.calls[0][1] as Record<string, unknown>;
    // decorations 缺省 true = 独立窗自带标题栏红绿灯(方案 A);incognito 缺省
    // false = 登录态持久,任何人加 true = 每次重扫(design-v9 §4 设计回归)
    expect(options).not.toHaveProperty("decorations");
    expect(options).not.toHaveProperty("incognito");
    expect(tgNativeRegisteredLabelsForTests()).toEqual(["tg-native-mihomo_party"]);
  });

  it("F4 键口径 = t.me 频道名:两源(不同 title)推导出同频道 → 第二次聚焦复用同窗,零双实例", async () => {
    const deps = fakeDeps();
    await expect(
      openOrFocusNative(K_URL, { title: "TG · source-a", deps }),
    ).resolves.toBe("created");
    await expect(
      openOrFocusNative(K_URL, { title: "TG · source-b", deps }),
    ).resolves.toBe("focused");
    expect(deps.create).toHaveBeenCalledTimes(1); // 同频道只建一窗
    expect(deps.handles.get("tg-native-mihomo_party")?.setFocus).toHaveBeenCalledTimes(1);
  });

  it("focused:getByLabel 命中 → 构造零次 + setFocus 一次;setFocus 被拒仍返 focused(聚焦尽力而为,窗活即语义成立)", async () => {
    const handle = fakeHandle("tg-native-mihomo_party");
    const deps: NativeWindowDeps = {
      getByLabel: vi.fn(async () => handle),
      getAll: vi.fn(async () => []),
      create: vi.fn(),
    };
    const result = await openOrFocusNative(K_URL, { deps });
    expect(result).toBe("focused");
    expect(deps.create).not.toHaveBeenCalled();
    expect(handle.setFocus).toHaveBeenCalledTimes(1);
    // 聚焦被拒:不让整条链报错(窗已在,用户可从程序坞点回)
    const rejecting: NativeWindowDeps = {
      getByLabel: vi.fn(async () => ({ ...handle, setFocus: vi.fn(async () => { throw new Error("denied"); }) })),
      getAll: vi.fn(async () => []),
      create: vi.fn(),
    };
    await expect(openOrFocusNative(K_URL, { deps: rejecting })).resolves.toBe("focused");
  });

  it("竞态幂等:构造即触发 tauri://error + 复查 getByLabel 命中 → onCreateError('focused') 不误报", async () => {
    // 命中分支:并发另一发已建窗(复查读得到)→ 幂等视同聚焦
    const twin = fakeHandle("tg-native-mihomo_party");
    let own: FakeHandle | null = null;
    const raceDeps: NativeWindowDeps = {
      // 竞态剧本:首查 miss(own 未落)→ 建窗后复查命中(twin 已被并发发登记)
      getByLabel: vi.fn(async (label: string) => (label === "tg-native-mihomo_party" && own !== null ? twin : null)),
      getAll: vi.fn(async () => []),
      create: vi.fn((label: string) => {
        own = fakeHandle(label);
        return own;
      }),
    };
    const onRaceFocused = vi.fn();
    expect(await openOrFocusNative(K_URL, { deps: raceDeps, onCreateError: onRaceFocused })).toBe("created");
    expect(onRaceFocused).not.toHaveBeenCalled();
    // own 由 create 闭包落值(TS CFA 不追闭包赋值,显式放宽再取)
    (own as FakeHandle | null)?.__fire("tauri://error");
    await vi.waitFor(() => expect(onRaceFocused).toHaveBeenCalledWith("focused"));
    expect(raceDeps.create).toHaveBeenCalledTimes(1); // 零重建
    expect(twin.setFocus).toHaveBeenCalledTimes(1);
  });

  it("F2 异步真失败:error + 复查 miss → 存活态单点清理(登记/注意力回收)+ destroyed 广播,不留「注记失败、徽标还亮」矛盾", async () => {
    const failDeps = fakeDeps();
    const onFailed = vi.fn();
    const onDestroyed = vi.fn();
    const unlisten = onNativeWindowDestroyed(onDestroyed);
    setNativeViewFocus("mihomo_party", "native"); // 模拟 .then("created") 已落的注意力
    expect(await openOrFocusNative(K_URL, { deps: failDeps, onCreateError: onFailed })).toBe("created");
    const failedHandle = failDeps.handles.get("tg-native-mihomo_party");
    failDeps.handles.delete("tg-native-mihomo_party"); // 真失败:窗从未活过,复查读不到
    failedHandle?.__fire("tauri://error");
    await vi.waitFor(() => expect(onFailed).toHaveBeenCalledWith("failed"));
    // 单点清理三件套:登记回收 + 注意力回收(F1 同门)+ 广播(F2)
    expect(tgNativeRegisteredLabelsForTests()).toEqual([]);
    expect(nativeViewFocusOf("mihomo_party")).toBe("intel");
    expect(onDestroyed).toHaveBeenCalledWith("mihomo_party", "tg-native-mihomo_party");
    unlisten();
  });

  it("capped:getAll 过 tg-native- 前缀对账(main 不计)≥3 → 零构造;上限满但窗已开 = 聚焦优先不受拦", async () => {
    const deps = fakeDeps([
      "main",
      `${TG_NATIVE_LABEL_PREFIX}xa1`,
      `${TG_NATIVE_LABEL_PREFIX}x2c`,
      `${TG_NATIVE_LABEL_PREFIX}x3d`,
    ]);
    // 未开过的新频道:计数满 3 → capped 零构造
    const result = await openOrFocusNative("https://web.telegram.org/k/#@xb1", { deps });
    expect(result).toBe("capped");
    expect(deps.create).not.toHaveBeenCalled();
    // 重复点击语义优先:命中既有窗不因上限被拒
    const focused = await openOrFocusNative("https://web.telegram.org/k/#@xa1", { deps });
    expect(focused).toBe("focused");
    expect(deps.create).not.toHaveBeenCalled();
  });

  it("F1 destroyed 模块级清理:窗亡 → 登记 + 注意力表回收(不依赖订阅者)、订阅者收 (key,label)、解绑后不再收;再开 = created", async () => {
    const deps = fakeDeps();
    const onDestroyed = vi.fn();
    const unlisten = onNativeWindowDestroyed(onDestroyed);
    await openOrFocusNative(K_URL, { deps });
    setNativeViewFocus("mihomo_party", "native"); // 用户看过原生视图
    const handle = deps.handles.get("tg-native-mihomo_party");
    expect(handle).toBeTruthy();
    handle!.__fire("tauri://destroyed");
    // 深检 F1:注意力表随窗亡模块级回收 —— 用户在别的渠道/层级关窗,回进
    // 该频道时 nativeViewFocusOf 读到 intel,段控件不再亮「原生视图」active
    expect(nativeViewFocusOf("mihomo_party")).toBe("intel");
    expect(tgNativeRegisteredLabelsForTests()).toEqual([]);
    expect(onDestroyed).toHaveBeenCalledWith("mihomo_party", "tg-native-mihomo_party");
    // 再开 = created(注册表已回收,不复用旧态)
    await expect(openOrFocusNative(K_URL, { deps })).resolves.toBe("created");
    expect(deps.create).toHaveBeenCalledTimes(2);
    unlisten();
    onDestroyed.mockClear();
    deps.handles.get("tg-native-mihomo_party")?.__fire("tauri://destroyed");
    expect(onDestroyed).not.toHaveBeenCalled();
  });

  it("F8 结构性域白名单:非 /k/ 深链(t.me 原链/任意域/前缀对但推导不出)同步 throw,走调用方异常 catch 路径", async () => {
    const deps = fakeDeps();
    await expect(openOrFocusNative("https://t.me/s/mihomo_party", { deps })).rejects.toThrow(TG_NATIVE_K_URL_PREFIX);
    await expect(openOrFocusNative("https://example.com/k/#@mihomo_party", { deps })).rejects.toThrow();
    // 前缀合法但频道名推导不出(/k/ 页锚不是 t.me 用户名词表)
    await expect(openOrFocusNative(`${TG_NATIVE_K_URL_PREFIX}+invite`, { deps })).rejects.toThrow();
    expect(deps.create).not.toHaveBeenCalled(); // 越界零构造
    expect(tgNativeRegisteredLabelsForTests()).toEqual([]);
  });

  it("F4b 首开记忆:created 记忆;destroyed 不回收(关窗重开不假预告);failed 回收(失败窗从未渲染,重试按首开)", async () => {
    const deps = fakeDeps();
    expect(tgNativeCreatedBeforeOf("mihomo_party")).toBe(false);
    await openOrFocusNative(K_URL, { deps });
    expect(tgNativeCreatedBeforeOf("mihomo_party")).toBe(true);
    // 窗亡:记忆保留 —— 重开不再出「首次需扫码登录一次」全量注记
    deps.handles.get("tg-native-mihomo_party")?.__fire("tauri://destroyed");
    expect(tgNativeCreatedBeforeOf("mihomo_party")).toBe(true);
    // 真失败:记忆回收 —— 重试仍按首开全量披露
    const failDeps = fakeDeps();
    await openOrFocusNative(K_URL, { deps: failDeps });
    const failedHandle = failDeps.handles.get("tg-native-mihomo_party");
    failDeps.handles.delete("tg-native-mihomo_party");
    failedHandle?.__fire("tauri://error");
    await vi.waitFor(() => expect(tgNativeCreatedBeforeOf("mihomo_party")).toBe(false));
  });

  it("构造同步 throw(注入缝)原样上抛,登记零残留", async () => {
    const deps: NativeWindowDeps = {
      getByLabel: vi.fn(async () => null),
      getAll: vi.fn(async () => []),
      create: vi.fn(() => {
        throw new Error("sync boom");
      }),
    };
    await expect(openOrFocusNative(K_URL, { deps })).rejects.toThrow("sync boom");
    expect(tgNativeRegisteredLabelsForTests()).toEqual([]);
  });

  it("isNativeWindowOpen:实时 getByLabel 对账(开 → true,销毁 → false);查询抛错/非法 kUrl = false 不抛", async () => {
    const deps = fakeDeps();
    await expect(isNativeWindowOpen(K_URL, deps)).resolves.toBe(false);
    await openOrFocusNative(K_URL, { deps });
    await expect(isNativeWindowOpen(K_URL, deps)).resolves.toBe(true);
    deps.handles.get("tg-native-mihomo_party")?.__fire("tauri://destroyed");
    await expect(isNativeWindowOpen(K_URL, deps)).resolves.toBe(false);
    const badDeps: NativeWindowDeps = {
      getByLabel: vi.fn(async () => {
        throw new Error("boom");
      }),
      getAll: vi.fn(async () => []),
      create: vi.fn(),
    };
    await expect(isNativeWindowOpen(K_URL, badDeps)).resolves.toBe(false);
    await expect(isNativeWindowOpen("https://t.me/s/mihomo_party", deps)).resolves.toBe(false);
  });

  it("tgNativeKeyOf/tgNativeLabelOf:/k/ 深链反推 t.me 频道名;非本模块口径 = null;label 越界字符折叠 _ 纵深防御", () => {
    expect(tgNativeKeyOf(K_URL)).toBe("mihomo_party");
    expect(tgNativeKeyOf("https://web.telegram.org/k/#@durov")).toBe("durov");
    // 只认 /k/ 深链口径(F8):t.me 原链/镜像链不是本模块入参
    expect(tgNativeKeyOf("https://t.me/s/mihomo_party")).toBeNull();
    expect(tgNativeKeyOf("https://web.telegram.org/k/#@+invite")).toBeNull();
    expect(tgNativeKeyOf(null)).toBeNull();
    expect(tgNativeLabelOf("mihomo_party")).toBe("tg-native-mihomo_party");
    expect(tgNativeLabelOf("频道 名")).toBe("tg-native-____"); // 折叠防构造即炸(纵深防御)
  });

  it("视图注意力表:缺省 intel;分键登记,会话内持久(读侧不随读取消耗);reset 清空", () => {
    expect(nativeViewFocusOf("mihomo_party")).toBe("intel");
    setNativeViewFocus("mihomo_party", "native");
    setNativeViewFocus("durov", "intel");
    expect(nativeViewFocusOf("mihomo_party")).toBe("native");
    expect(nativeViewFocusOf("durov")).toBe("intel");
    expect(nativeViewFocusOf("other")).toBe("intel"); // 未登记 = 缺省情报视图
    resetTgNativeForTests();
    expect(nativeViewFocusOf("mihomo_party")).toBe("intel");
  });
});
