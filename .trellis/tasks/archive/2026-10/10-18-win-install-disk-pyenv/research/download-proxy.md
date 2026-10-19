# Windows 下载代理坑:壳侧 reqwest 的系统代理行为定论

任务:10-18-win-install-disk-pyenv 探查项③。日期:2026-10-18。
方法:核本仓 Cargo.toml/Cargo.lock + cargo registry 里 reqwest 0.13.5 与
hyper-util 0.1.21 源码(行号可复核)。

## 下载栈是什么

pyenv 安装链下载 python-build-standalone 走**壳侧 Rust reqwest**:
`pyenv_install.rs::download_runtime` → `reqwest::blocking::Client::builder()`
(rustls + ring process provider,与 updater 同栈)。**没有** `.no_proxy()`
也没有 `.proxy()` → `auto_sys_proxy` 默认开 → `ProxyMatcher::system()`
(reqwest async_impl/client.rs L410-418)。

## 会不会吃系统死代理 7897:会(Windows)

关键在特性全图可加:Cargo 特性是按 crate 全图合并的,本仓
`reqwest = { default-features = false, features = ["blocking",
"rustls-no-provider"] }` 关掉了 default(含 `system-proxy`)也**没用**——
`tauri-plugin-updater = "2"`(Cargo.toml L32,默认特性)自带
`system-proxy = ["reqwest/system-proxy"]`(tauri-plugin-updater-2.13.1
Cargo.toml L74)→ `hyper-util/client-proxy-system`。Cargo.lock 里 hyper-util
的依赖含 `windows-registry` + `system-configuration`(即该特性已开)。

`Matcher::from_system()`(hyper-util matcher.rs L238-249)= **env 先读、
Windows 注册表补位**:

1. 先读 env:`ALL_PROXY` / `HTTP_PROXY` / `HTTPS_PROXY` / `NO_PROXY`
   (L228-236 from_env);
2. Windows 下再读 WinINET 注册表 `HKCU\...\Internet Settings`
   `ProxyEnable=1` + `ProxyServer`(win::with_system,L695-715)——
   **只在 env 留空的槽补位**(`if builder.http.is_empty()`),`ProxyOverride`
   同理只填空的 NO 列表。

所以:Windows 系统代理开着且指向死端口 7897(用户装过 Clash 类又没关)→
壳下载运行时 tar.gz 走 127.0.0.1:7897 → 连接失败 → `network_failed:` 报错。
**「WinINET 系统代理 reqwest 默认不吃」的说法在本仓不成立**——那是
system-proxy 特性关掉时的行为,updater 把它拉回来了。

## 逃生口(按优先级)

1. **强制全直连:`set NO_PROXY=*`**——hyper-util DomainMatcher 对 `*` 特判
   全匹配(matcher.rs L529-530 `else if d == "*" { return true; }`),匹配
   顺序在代理判定**之前**(intercept L122-126 先查 no 列表)→ 注册表代理
   再开着也直连。装前同 cmd 注入:`cmd /c "set NO_PROXY=*&& …exe"`。
2. 按域放行:`NO_PROXY=github.com,objects.githubusercontent.com`(运行时
   manifest 默认源域;自建镜像则加镜像域)。
3. 换活代理:`HTTPS_PROXY=http://127.0.0.1:<活端口>`(env 优先于注册表,
   注册表只补空槽)。
4. **陷阱:只清空/删除 `HTTP_PROXY`/`HTTPS_PROXY` env 不会变直连**——env
   空了注册表 WinINET 值会补位。真断代理要么 `NO_PROXY=*`,要么关系统代理
   (设置→网络→代理)。

## pip 段不受 WinINET 影响

安装链依赖段是 `python -m pip` 子进程(pip 的 requests/urllib 栈只读 env
代理变量,不读 WinINET 注册表):系统死代理开着但 env 未设 → pip 直连;
env 设了代理 → pip 同走。组件 pip / playwright 段同构。
