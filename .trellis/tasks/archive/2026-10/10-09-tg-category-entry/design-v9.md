# 情报流 v9 设计稿 · TG 原生网页视图(预览升级 /k/ + 原生视图切换)

> 主人令(2026-10-10,prd.md:183-186 AC33-AC36):要么按网页版 TG 布局写,要么直接加载网页。深探结论(本会话逐项复核,证据见下):iframe 被 `x-frame-options: deny` 封死(**本会话实跑复证**:`curl -sI https://web.telegram.org/k/` → `x-frame-options: deny`,2026-10-11);WebviewWindow 开远程 URL 可行(内置浏览器预览同款能力已上线,`feed-screen.tsx:2722-2740`);/k/ 登录态核心在 MTProto 密钥(watcher 的 Playwright 配置档与 WKWebView 存储互不相通),跨浏览器注入不可行,需内嵌页内扫码一次,登录态持久。
>
> 事实底座(全部本会话实读,引注 = 文件:行号):
> - **预览现状**:`tgPreviewUrl` useMemo(`feed-screen.tsx:2713-2721`)遍历 `streamItems` 取该渠道最新可推导条目;`openTgPreview`(`:2722-2740`)`new WebviewWindow(\`tg-preview-${Date.now()}\`, {url, width:460, height:780})` + `tauri://error` → 条内注记 `tgPreviewNote`;`WebviewWindow` 自 `@tauri-apps/api/webviewWindow`(`:117`,实测安装版 **2.12.1**,`ui-src/node_modules/@tauri-apps/api/package.json:3`)。
> - **镜像推导**:`telegramMirrorUrlOf`(`feed/api.ts:764-770`)正则认 `t.me/<频道>/(id)?`、`t.me/s/<频道>/(id)?`、`t.me/<频道>` 三形,`+邀请链`/非 t.me/空 = null 不猜;纯函数用例 9 断言钉死(`feed-screen.test.tsx:3334-3349`)。
> - **监控台条**:3 级专属(`feed-screen.tsx:3573-3657`),testid 六件 `feed-tg-console`/`-live`/`-login`/`-preview`/`-history`/`-preview-note`;`isTgChannel = chatView = channelCardKindOf(...) === "tg"`(`:2423-2427`);phase 机件 idle/loading/ok/error(`:2437-2459`);`startWebLogin` 走 `telegramWebLogin(account)`(`:2687-2705`)。
> - **权限面**:`capabilities/default.json:14` 仅 `core:webview:allow-create-webview-window`;`windows: ["main"]`(`:5-7`)——新开窗不在列表 = 零 ACL(远程页拿不到任何 IPC 能力,description 安全注记在案 `:4`)。
> - **watcher 账号与配置档**:账号键规约 `telegram-<标识>`(`web_line.py:73` `ACCOUNT_KEY_RE`);配置档 = Playwright persistent context `<数据根>/telegram-web/<账号键>/`(`web_line.py:66` `PROFILE_ROOT_DIR`;模块 docstring「cookies/localStorage 落配置档」;`web_host.py:354-357` 起容),0700/0600 硬化(`web_host.py:432-434`);`WEB_ORIGIN = "https://web.telegram.org"`(`web_line.py:79`);单键 fatal 停键不复活不带走他人(`web_host.py:539-553`)。
> - **telegram.status**:`web.accounts[]` 行 = `{account, logged_in, logged_in_at, login_in_progress}`(`settings/telegram-api.ts:23-36`);`telegramGetStatus()` = RPC `telegram.status`(`:48-49`);`telegramWebLogin` = `browserOpen("tg_web_login", account, {force})` 单入口(`:57-60`)。后端 `web_host.py:517-535` `status()` 出运行态;feed 侧消费同源(`feed-screen.tsx:108` 引 settings/telegram-api)。
> - **WebviewWindow API 面**(2.12.1 typings 实测):`getByLabel(label) → Promise<WebviewWindow|null>`(`webviewWindow.d.ts:94`);Window 事件 `onResized:1636`/`onMoved:1658`/`onCloseRequested:1687`/`onFocusChanged:1739`/`onScaleChanged:1765`,方法 `setFocus:1244`/`setPosition:1172`/`setSize:1110`/`outerPosition:430`/`outerSize:454`;WindowOptions `decorations:2106`/`alwaysOnTop:2108`/`title/width/height/resizable`;WebviewOptions `url:553`/`incognito:595`(缺省 false = 持久存储);生命周期事件 `tauri://created`/`tauri://error`(window.d.ts:250-253)、`tauri://destroyed`(event.d.ts:85 `TauriEvent.WINDOW_DESTROYED`)。
> - **⚠ eval 实锤(推翻任务问句预设)**:`@tauri-apps/api` **2.12.1 的 JS 侧没有 `eval()`**——全包 grep 仅 `core.d.ts:54` 一处注释提及;`Webview` 类方法全列(setSize/setPosition/setFocus/show/hide/setZoom/close/reparent/clearAllBrowsingData)无 eval。跨窗改 hash 必须 Rust 命令中转或关窗重建(§2.3)。
> - **Rust 命令注册点**:`main.rs:746` `generate_handler![]`(若需加命令在此)。
> - **测试/冒烟资产**:`feed-screen.test.tsx` WebviewWindow mock(`:150,168-169`)与 AC11 开窗断言(`:3302-3330`)现成同门;冒烟 `desktop/scripts/feed-card-smoke.py` 锚 `feed-tg-console`(`:288,293,365`)。
>
> **对 AC33「推导不出 → 回退 t.me/s」的一处如实澄清**:/k/ 与 t.me/s **同源推导**(都从 t.me url 提取频道名)——频道名推导不出时两者同样不可得,「静态回退到镜像」在推导层是死分支(等价于置灰)。本稿把回退落在**有实义的位置**:/k/ 运行时开窗失败 → 注记指引系统浏览器直开 t.me/s(§1.2);此为对 PRD 词面的工程化澄清,非缩水,已标注待主人验收时确认。

---

## 0. 总览:①②同轨,一个窗口注册表

AC33(预览升级)与 AC34(原生视图切换)物理上是**同一个能力**:都是「应用内 WebviewWindow 加载 `/k/#@<频道名>`」。若两钮各自开窗,同频道会出两个 /k/ 实例(每个都是完整 SPA + MTProto websocket,内存 100-300MB 级)。故统一:

```
                    ┌────────────────────────────────────────┐
 监控台「内置浏览器预览」钮 ──┐                                │
                            ├──→ tgNativeWindows.openOrFocus ──→ WebviewWindow
 3 级工具条「原生视图」段   ──┘    (新模块 tg-native-window.ts)      label: tg-native-<频道名>
                                                                  url:  /k/#@<频道名>
                                                                  登录态:WKWebView 持久存储
```

- 段控件「原生视图」= 关注点切换(开窗/聚焦并标记 active);「情报视图」= 应用内本地时间线,**永不卸载**(③ 两张数据皮的根基:watcher 挂了本地线还能看历史,内嵌页挂了/没登录本地线照常)。
- 旧 `tg-preview-<时间戳>` 标签与 t.me/s 直开逻辑**退役**,由统一注册表接管;t.me/s 降级为运行时回退指引(§1.2)与推导失败时的置灰说明词。

## 1. ① 预览升级(AC33)

### 1.1 URL 推导(纯函数,重构不改行为)

`feed/api.ts` 新增两件,`telegramMirrorUrlOf` 内部重构为共用提取器(9 条存量断言零改动全绿):

```ts
/** t.me 链 → 频道用户名(共用提取器;认不出 = null 不猜) */
export function telegramChannelNameOf(url: string | null | undefined): string | null;
//  正则核 = 现 telegramMirrorUrlOf 的捕获组原样搬迁(api.ts:766)

/** 频道名 → /k/ 原生页锚(频道名词表 [A-Za-z0-9_],无需编码) */
export function telegramKUrlOf(url: string | null | undefined): string | null;
//  telegramChannelNameOf 命中 → `https://web.telegram.org/k/#@<name>`
```

- `#@<username>` 是 /k/ 的官方深链形态:登录后自动落到该频道。`WEB_ORIGIN` 同锚(`web_line.py:79`),但**不共用 watcher 常量**——前端不 import Python 侧,URL 字面量落在 api.ts 注释里注明同源。
- `tgPreviewUrl` useMemo(`feed-screen.tsx:2713-2721`)升级:遍历逻辑原样,取值改 `telegramKUrlOf(item.url)`;按钮 title 分档(下表)。
- **回退语义(诚实)**:频道名推导不出 = /k/ 与 t.me/s 同时不可得(同源),按钮置灰,title 写全:「暂无可推导的 t.me 公开链接(私有频道或条目无链接),原生预览与公开镜像均不可用」。PRD「回退 t.me/s」落运行时,见 1.2。

### 1.2 运行时回退与失败注记

- 开窗失败(`tauri://error`,既有机件 `feed-screen.tsx:2732-2736` 同门)→ `tgPreviewNote` 分两档:
  - /k/ 打不开(web.telegram.org 不可达/被墙/窗口被拒):「原生网页版打开失败——可稍后重试,或点条目『打开原文』用系统浏览器直看;私有频道无公开镜像。」(**有实义的镜像回退**:「打开原文」直达 t.me 原链,shell:allow-open 已授权 https?:// 全域,capabilities/default.json:16-25)
  - 窗口创建异常(同步 throw):沿用现词面(`:2738`)。
- 不做「/k/ 失败自动改开 t.me/s 窗」:失败原因(断网 vs 被墙 vs TG 挂了)对两种目标同真,自动重开只会在断网时连开两个失败窗;给指引不给惊吓。

### 1.3 未登录 QR 流与双会话披露(③ 前半)

- 未扫码时 /k/ 自带 QR 登录页(TG 官方流,零我们注入)。**如实告知**(按钮 title + 首开注记):「网页版需扫码登录一次;登录会触发 TG 的『新设备登录』安全提醒(服务端推送,属预期,可在 TG 设置→设备里核对);登录态存本机 WKWebView,此后免扫、重启 app 仍有效。」
- **双会话如实披露(设计约束,不可跨浏览器注入的落点)**:watcher 登录态在 Playwright 配置档 `<数据根>/telegram-web/<账号键>/`(`web_host.py:354-378`,docstring 钉死「多账号互不相通、登录态=配置档文件」);应用内 /k/ 窗的登录态在 WKWebView 数据存储——**两套互不相通,各扫一次**。监控台既有「扫码登录网页版」钮(`feed-tg-console-login`,`:3598-3611`,走 browser.open 拉 Playwright headed 窗)服务 watcher,保留不动;/k/ 窗内扫码服务原生视图。推荐扫**同一账号**(多会话 TG 官方支持);与 web_line.py docstring 的关联风险披露同口径:同机同出口多会话可被 TG 关联,只读监控风险低,建议小号者两处都扫小号。
- 监控台「未登录」警示词面(`:3591-3593`)不混入 /k/ 语义(它说的是 watcher 登录态);/k/ 的未登录提示只挂在原生视图自己的 title/注记里,两条登录线词面不串台。

## 2. ② 原生视图切换(AC34)

### 2.1 入口与形态

- 3 级 TG 渠道详情工具条(`feed-toolbar`,`feed-screen.tsx:3374`)渠道名右侧加**双段控件**(KsFilter 分段同门,读态分段 `:3392-3419` 样式基):
  - `feed-tg-view-intel`「情报视图」(缺省 active):应用内时间线,搜索/已读/导出/键盘全量照旧,零变化;
  - `feed-tg-view-native`「原生视图」:调 `openOrFocusNative(频道名, kUrl)`;窗口存活期间该段保持 active(红点徽标),窗口关(tauri://destroyed)→ 段回落「情报视图」。
- **语义如实**:「切换到原生视图」= 开/聚焦独立窗口并把**注意力焦点**标到原生侧;应用内内容不卸载不替换(iframe 封死的前提下「原生视图内嵌在本窗」物理不可达,见事实底座 curl 实证)。段控件表达「当前看哪张皮」,不是排他渲染开关。
- **网站/日报渠道:整组不渲染**(③ 如实无钮)——门 = 既有 `isTgChannel`(`:2427`),与监控台条同门判定,零新判定面。

### 2.2 决策点一:窗口管理 —— A 独立窗 vs B 覆盖主窗跟随(方案+取舍+推荐)

**方案 A:独立窗口(decorations: true,自带标题栏)——推荐**

- 开窗参数:`WebviewWindow(label, { url: kUrl, title: "TG · <频道名>", width: 1100, height: 780, minWidth: 640, minHeight: 480 })`(尺寸对齐 TG Web 桌面版三栏最小可用宽;`decorations` 缺省 true,WindowOptions `window.d.ts:2106`)。
- 优点:移动/缩放/最小化/红绿灯全归 macOS 原生,零我们写的同步代码;独立于主窗生命周期(主窗最小化原生视图照用);多窗口(Dock/「窗口」菜单)原生管理;脆弱面 ≈ 0。
- 代价:与主窗无几何关系(用户自己摆);任务台多一个窗位。

**方案 B:无边框窗覆盖主窗内容区 + 事件跟随主窗移动缩放**

- 需监听的主窗事件清单(typings 实证全列):`onMoved:1658`/`onResized:1636`(跟随几何)、`onScaleChanged:1765`(显示器切换/缩放,必须换算物理/逻辑坐标,`outerPosition:430`/`outerSize:454` 读主窗 + `setPosition:1172`/`setSize:1110` 写子窗)、`onFocusChanged:1739`(焦点礼让:点子窗不能把主窗抢回顶部)、`onCloseRequested:1687`(主窗关 → 先关子窗)。macOS 还需补 Spaces/全屏切换的位移(事件系统**不覆盖**,要轮询 `outerPosition` 兜底)。
- 脆弱性(如实):①拖拽主窗时 move 事件经 IPC 逐发,子窗 `setPosition` 异步追,实测这类「窗口追逐」必有可见抖动/滞后帧;②无边框(`decorations: false`)+ 远程页 = **无法注入关闭/拖拽区**(页面是 TG 的,eval JS 侧不存在,§2.3)——关窗要么靠 Esc 快捷键(焦点在远程页内时我们要拦键盘,又是注入面),要么靠主窗段控件「情报视图」回收,交互别扭;③主窗最大化/进全屏/多显示器拖越时坐标系换算是 bug 温床。
- **推荐 A**,理由一句话:B 用 5+ 事件监听 + 坐标换算 + 键盘拦截买一个「贴着主窗」的观感,换来抖动与三处脆弱面;A 零同步代码零抖动,AC34 的「跟随主窗位置或独立窗口,计划阶段定」本就留了 A 这个选项。**无边框如实弃用**:AC34 词面「无边框 WebviewWindow」在独立窗形态下等价于「没有红绿灯不能关不能拖」——无边框只在 B(内嵌面板观感)里成立,选 A 即如实偏离该词面,此处标注待主人验收。

### 2.3 决策点二:切渠道时已开窗口如何导航(问句「WebviewWindow eval 改 hash?」的如实回答)

**JS 侧 eval 不存在(2.12.1 实测,事实底座⚠)**,三案:

| 案 | 做法 | 取舍 |
|---|---|---|
| a. Rust 命令中转 eval | `main.rs:746` 加 `tg_native_navigate(label, hash)` → Rust 侧 `webview.eval("location.hash=...")`(Rust API 有 eval) | 能改 hash 不重建;**代价**:新增一条自定义命令权限面(capabilities 需给 main 加 `allow-tg-native-navigate`;TG 窗不在 windows 列表拿不到它,越权面可控但 ACL 描述要重写);且 eval 注入远程页时机(page ready 与否)要赌 |
| b. 关旧窗开新窗 | 销毁旧频道窗 → 以新 `kUrl` 建窗 | 零新权限零注入;登录态在 WKWebView 存储**不随窗亡**(存储按 app 持久,非按窗),免重扫;代价:重载闪 1-2s、滚动位丢 |
| c. **每频道一窗,导航退化成聚焦(推荐)** | 切频道 = `getByLabel(tg-native-<新频道>)` 命中 → `setFocus()`,未命中 → 建新窗 | **根本不需要导航**;每窗 URL 固定 `#@<自己频道>`,频道间零纠缠;代价是多窗内存(由 §2.4 上限封顶) |

- **推荐 c**,与「重复点击=聚焦」语义自然合一;a 留作单窗派生需求的备件(若主人坚持「只允许一个 /k/ 窗」再启用 a,届时权限面按 capabilities description 惯例写明);b 是 a 的免权限替身。
- 每窗各自的 websocket 各自收推 —— 多窗同时在线多路 MTProto 连接,TG 服务端按会话容忍;上限 3 封顶(§2.4)即封顶连接数,与 web_line 缺省 `max_accounts=3` 同量级纪律(`web_line.py:25-26`)。

### 2.4 重复点击 / 生命周期 / 上限

新模块 `ui-src/src/screens/feed/tg-native-window.ts`(注册表与 React 解耦,可单测):

```
openOrFocusNative(channel: string, kUrl: string) →
  "created" | "focused" | "capped"     // 三态返回,调用方出对应注记
```

- **重复点击**:`WebviewWindow.getByLabel('tg-native-<channel>')`(`webviewWindow.d.ts:94`)命中 → `setFocus()`(`window.d.ts:1244`)返回 `"focused"`,不重建;未命中 → 建窗。**竞态兜底**:双击双触发都看到 null 时,第二发构造会撞 label → `tauri://error`(window.d.ts:253 同门);error 处理器里再 `getByLabel` 复查,命中即视同 `"focused"`(幂等),不误报失败。旧代码「label 带时间戳防撞」(`feed-screen.tsx:2725-2726`)在此**反向修正**:稳定 label 是聚焦语义的前提,撞 label 从缺陷变为幂等信号。
- **存活登记与回收**:Map<label, {channel, dispose}> 建窗时登记;`once("tauri://destroyed", ...)`(event.d.ts:85)删登记 + 通知 UI 段回落(Rsc 层用轻量 store 或 feed-screen 内 useEffect 订阅模块事件);**主窗刷新(HMR/导航)不死锁**:注册表挂模块级,残留 handle 由 `getByLabel` 实时对账(不信任本地 Map 的存在性,只用作 active 徽标与计数)。
- **关闭路径**:红绿灯关 = TG 窗自我销毁 → destroyed 回收(无需 `onCloseRequested`,我们不拦);app 退出 = 进程亡,全部 webview 随终,存储留下(下次开免扫);3→2 级返回**不关窗**(独立窗哲学:开了归用户管),段控件随之卸载、注册表与 destroyed 监听照常活着(模块级,不随组件卸载)。
- **上限 = 3**:`openOrFocusNative` 在活窗数(以 `WebviewWindow.getAll()` 过 `tg-native-` 前缀对账,不靠 Map 计数)≥3 时返回 `"capped"`,条内注记:「原生视图窗口已达上限 3——可在程序坞/『窗口』菜单找到既有窗口,关闭其一后再开」。不做 LRU 自动关(悄悄关用户的窗 = 惊吓);3 的依据:每个 /k/ 实例是完整 SPA + 独立 MTProto websocket(§2.3),内存与连接数双帽,与 watcher `max_accounts=3`(`web_line.py:25-26`)同量级。

## 3. 边界与如实披露(③ 全项)

| 边界 | 处置 | 依据 |
|---|---|---|
| 网站/日报渠道 | 工具条不出段控件、监控台条本就不出(`:3573` isTgChannel 门)——**如实无钮**,不做禁用灰钮占位 | `feed-screen.tsx:2423-2427` |
| 未扫码(全账号未登录) | /k/ 窗显示 TG 官方 QR 登录页;首开 title+注记告知「扫码一次 + 触发 TG 新登录安全提醒」(§1.3);监控台「未登录」词面只说 watcher,不串台 | `:3591-3593` 词面分工 |
| watcher 挂/停键 | 内嵌页完全不受影响(自带 MTProto websocket 直连 TG);本地时间线停更由监控台 phase/告警面如实呈现——**两张数据皮互为冗余**,这正是「情报视图永不卸载」的价值 | `web_host.py:539-553` 单键失效隔离;curl 实证 /k/ 独立可达 |
| /k/ 被 TG 改版/下线 | 窗内是 TG 自己的页面,改版自愈;域名级不可达 = 开窗注记指引(§1.2);无选择器脆弱面(对比 watcher 的 `tg_web_dom_stale` 哨兵,web_line.py docstring) | — |
| 登出(用户在 /k/ 页内主动登出) | 窗回落 QR 页,登录态本地残留无害;不拦截不告警,docstring 口径:登录态=本机文件,登出=服务端删会话 | `web_line.py` 凭据纪律同门 |

## 4. 安全与权限

- **权限面(实施修正,2026-10-11 深检回写)**:原稿「零新增权限」目标被仓库实况推翻一处 —— `setFocus` 聚焦语义必需 `core:window:allow-set-focus` 单授权:**`core:window:default` 仅 28 项只读 getter 不含 set_focus**(实证 = tauri crate 自带权限参考 `~/.cargo/registry/src/*/tauri-2.12.1/permissions/window/autogenerated/reference.md`,default 集恰 28 项、allow-set-focus 单列;`get_all_windows` 已由 `core:default` 覆盖)。除此之外 c 案(每频道一窗)不加命令;沿用 `core:webview:allow-create-webview-window`,description 已改写——URL 从「固定 t.me/s」放宽为「固定 web.telegram.org/k/ 或 t.me/s(域白名单已升级为代码约束:openOrFocusNative 只收 `https://web.telegram.org/k/#@<名>` 深链,越界同步 throw,深检 F8)」。若主人选 a 案才新增命令权限(§2.3 表)。
- 远程页零 IPC(TG 窗不在任何 capability 的 windows 列表)不变——这是「被攻破的远程页拿不到任何能力」的既有安全注记(`capabilities/default.json:4`),升级后依然成立,/k/ 与 t.me/s 同待遇。
- `incognito` **不设**(缺省 false = 持久存储,webview.d.ts:595)——登录态持久的机制本体;任何人不许加 `incognito: true`(加了 = 每次重扫,设计回归)。

## 5. 实施切分(机件清单)

1. `feed/api.ts`:`telegramChannelNameOf` 提取 + `telegramKUrlOf` 新增 + `telegramMirrorUrlOf` 重构共用(行为零变)。
2. `feed/tg-native-window.ts`(新):注册表 + `openOrFocusNative`(created/focused/capped)+ destroyed 订阅;`WebviewWindow` 工厂函数参数注入(测试缝)。
3. `feed-screen.tsx`:`tgPreviewUrl` 改用 `telegramKUrlOf`;`openTgPreview` 改调注册表;监控台预览钮 title/置灰词面换新;工具条加双段控件(仅 isTgChannel);active 徽标订阅。
4. `capabilities/default.json`:description 改写(URL 域放宽注记)+ **新增 `core:window:allow-set-focus` 单权限**(§4 实施修正:聚焦语义必需,原稿「权限数组零变」据此作废)。
5. `feed-card-smoke.py`:新增段控件与预览钮锚(§6)。

## 6. ④ 测试与冒烟随动清单

**纯函数(vitest,feed-screen.test.tsx「纯函数」describe 同门,`:3334` 旁)**
- `telegramKUrlOf`:消息锚/预览链/纯频道链 → `/k/#@<名>`(9 断言镜像 `telegramMirrorUrlOf` 用例表);邀请链/非 t.me/空 → null。
- `telegramMirrorUrlOf` 存量 9 断言**零改动**跑绿(重构不改行为的行为学证明)。

**注册表单测(tg-native-window.test.ts,WebviewWindow mock 同门 `:150`)**
- created:未命中 getByLabel → 构造参数断言(label 前缀 `tg-native-`、url=`/k/#@名`、title、尺寸、decorations 缺省);
- focused:getByLabel 命中 → 构造零次 + setFocus 调一次;
- 竞态幂等:构造即触发 `tauri://error` + 复查命中 → 返回 "focused" 不误报;
- capped:`getAll()` 计 3 → 返回 "capped" 零构造;
- destroyed:触发销毁回调 → 计数回落、再开 = created。

**组件测试(feed-screen.test.tsx)**
- 段控件仅 TG 渠道渲染(site/daily `queryByTestId` 全空,③ 钉死);
- 点「原生视图」→ `openOrFocusNative` 收到 (频道名, /k/ url);窗口存活段 active、destroyed 后回落(模块 mock);
- 预览钮升级:url 带 t.me 锚 → 构造 `url: /k/#@mihomo_party`(改造既有 AC11 用例 `:3302-3330` 断言);条目无 t.me 链 → 置灰 + 新置灰词面;
- 开窗失败 → `feed-tg-console-preview-note` 出「原生网页版打开失败…」(改造既有注记用例);
- 未登录(tgWebline accounts 全 logged_in:false)→ 首开注记含「扫码登录一次」与「安全提醒」词面(③ 披露钉进测试)。

**冒烟(desktop/scripts/feed-card-smoke.py,锚 `:288` 同门)**
- 3 级 TG:`feed-tg-view-toggle` 段在场 + `feed-tg-view-native` 可点 + `feed-tg-console-preview` 词面含「原生」;site 渠道段控件 count==0。

**门禁**:vitest 全量 + build + 上述冒烟 + pytest desktop/store(权限/description 改动不触 Python 面,跑全套为惯例回归)。

## 7. 风险与开放问题(待主人验收裁决)

1. **AC34「无边框」词面偏离**(§2.2):推荐独立窗带标题栏;若主人坚持无边框 → 只能走 B 覆盖方案,接受抖动与自绘关闭交互,或 a 案 eval 注入自绘悬浮钮(注入远程页,脆弱)。**默认按 A 实施**。
2. **AC33「回退 t.me/s」澄清**(卷首注):推导层回退是死分支,已落运行时回退;若主人要「按钮双态手动切换」(/k/ 与镜像两个钮),加一钮即可,零机件冲突。
3. **多会话关联风险**(§1.3):/k/ 扫码 = TG 账号新增一个活跃会话;与小号建议同口径披露,不阻断。
4. **eval 缺席的远期**:若未来 Tauri JS API 补回 eval,§2.3 a 案可平替 c 案的「单窗派生」需求;本稿不预埋。
