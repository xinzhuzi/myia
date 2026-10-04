# Evidence — Windows 真机本地打包与冒烟(10-05-win-local-build)

机器:zbj @ 192.168.0.101(Windows 11,build 10.0.26200.9445);通道:免密 SSH(默认 shell=cmd)。
日志目录(Windows 侧):`D:\dev\winbuild-log\`(clone/rustup/sidecar/tauri/msi-install 各 .log+.exit)。

## §0 环境盘点(2026-10-05 会话首探)

| 项 | 状态 |
|---|---|
| UGit 5.54.0 | ✅ 已装(`C:\Users\ZBJ\AppData\Local\UGit\bin\ugit(.bat)` + 自带 git);`ugit clone <url> [-b]` 子命令存在 |
| Git for Windows | ✅ 2.55.0.windows.5(Git Bash:`C:\Program Files\Git\bin\bash.exe`) |
| Node / npm | ✅ v24.12.0(D:\nodejs);registry=官方 npmjs |
| Python | ✅ 3.12(D:\Python312) |
| MSVC | ✅ VS2022 Community + VS18 Enterprise 均含 VC.Tools.x86.x64(vswhere 实证) |
| cargo/rustc/rustup | ❌ 缺 → S3 装 |
| uv | ❌ 缺 → S2 装(已装 0.12.23,`C:\Users\ZBJ\.local\bin`,新会话 PATH 生效) |
| 网络 | github.com / api.github.com / registry.npmjs.org / pypi.org / static.rust-lang.org / astral.sh 直连 200;crates.io API HEAD 403(bot 拦 HEAD,非不可用) |
| 磁盘 | C 269G / D 419.8G / E 649.7G / F 10.8T 空闲 |
| RustDesk | 21118 可达(留主人目验通道,本次不用) |

## §1 S1 克隆(坑 ×2)

### 坑 1:ugit clone 是 GUI 耦合的
`ugit clone https://github.com/xinzhuzi/myia.git` 0.4s 静默返回,**零克隆**:无 `D:\dev\myia`,只留下一个空文件 `D:\dev\nul`(UGit 内部把输出重定向到 `nul`,其执行环境把 Windows 设备名当普通文件名)。判定:ugit CLI 的 clone 会唤起 GUI 等人点击,无人值守不可用。
**处置**:降级 UGit 通道的下一级——UGit 自带 git.exe 直跑 `clone`(仍是 UGit 的 git,符合主人"用 ugit 下载"意图;系统 git 作末级兜底,未用上)。

### 坑 2:git 的 URL 级代理指向未启动的本地代理
第一次用 UGit git.exe 克隆失败:
```
fatal: unable to access 'https://github.com/xinzhuzi/myia.git/':
Failed to connect to 127.0.0.1 port 7897 after 2066 ms: Couldn't connect to server
```
定位过程:
1. `set | findstr /i proxy` → 无 env 代理变量;
2. `type %USERPROFILE%\.gitconfig` → 末段有 **URL 级作用域**代理:
   `[http "https://github.com/"] proxy = http://127.0.0.1:7897`(7897=Clash Verge 混合口,netstat 证当前未监听);
3. 第一次修复尝试 `-c http.proxy= -c https.proxy=` **无效**——URL 级 `http.<url>.proxy` 优先于全局 `http.proxy`,覆盖键必须精确同域:`-c http.https://github.com/.proxy=`。

**处置**(守"严禁删本机配置"纪律,零改动 .gitconfig):命令级空覆盖
```
git -c http.proxy= -c http.https://github.com/.proxy= clone --progress https://github.com/xinzhuzi/myia.git D:\dev\myia
```
⚠️ 顺带发现(只报位置不改):`.gitconfig` 的 `[credential "https://cnb.cool"]` 段存有明文密码(`credential.helper=store` 风格),建议主人换凭据管理器。

### 结果
✅ 第三轮(命令级 URL 级空覆盖)克隆成功:**7470 objects / 61.07 MiB**(UGit 自带 git.exe 直连 GitHub,~1–2 MiB/s)。
- commit:**`1590546`**(1590546bb908774953562292a924ebc06e8aadc9;克隆时点 GitHub main HEAD,含并行会话 tests-module-grouping 收尾等 3 笔)
- 落点:`D:\dev\myia`;克隆动因链=ugit CLI(GUI 耦合不可用)→ UGit 自带 git.exe(✅ 实际使用,仍属 UGit 通道)→ 系统 git(未用上)。AC1 勾。

## §2 S2 uv

`irm https://astral.sh/uv/install.ps1 | iex` → `uv 0.12.23`(46b84fd0b 2026-10-03, x86_64-pc-windows-msvc),装于 `C:\Users\ZBJ\.local\bin`,新 SSH 会话 PATH 直接可用。✅ AC2 前半。

## §3 S3 Rust

`curl -L -o %TEMP%\rustup-init.exe https://win.rustup.rs/x86_64 && rustup-init.exe -y --default-toolchain stable-x86_64-pc-windows-msvc`:
- **cargo 1.99.0 (5f94df478 2026-08-27)**;`rustc -vV` → `host: x86_64-pc-windows-msvc` ✅(正中预期,非 gnu);
- 已装 MSVC(VS2022/VS18)被 rustup 直接探测复用,零 VS Build Tools 下载;总耗时约 2 分钟(含 ~500MB 工具链)。✅ AC2 后半。

## §4 S6 overlay(WiX 非 ASCII 雷)

`echo {"productName": "myssia"} > desktop\src-tauri\tauri.local.conf.json`——单行 JSON,Tauri config 浅合并只覆盖 productName;git status 确认 untracked(本地专用,不入库)。✅

## §5 S4 npm ci + S5 sidecar(并行后台)

- **S4 npm ci ×2**:`npm ci --no-fund --no-audit`(desktop → ui-src 两段串联)exit=0;`desktop\node_modules\.bin\tauri.cmd` 在。✅
- **S5 sidecar**(Git Bash:`"C:\Program Files\Git\bin\bash.exe" -c "cd /d/dev/myia/desktop && bash build-sidecar.sh x86_64-pc-windows-msvc"`)exit=0,耗时约 2 分钟:
  - uv sync --frozen --no-dev --extra vision 直连 PyPI 一次过(未动镜像);
  - PyInstaller(手维 myssia-core.spec)onefile 成功;
  - 产物 `desktop\src-tauri\binaries\myssia-core-x86_64-pc-windows-msvc.exe` = **123,322,789 字节(≈117.6MB)**,>30MB 判据 ✅(AC3 勾;与 mac 侧装机 132MB 同量级)。

## §6 S7 tauri build(坑 ×1:WSL bash 存根)

第一次跑 `npx tauri build`:beforeBuildCommand `npm run sidecar` → `bash build-sidecar.sh` 里的 `bash` 被 PATH 解析到 **WSL 存根**(`WindowsApps\bash.exe`,机器无 WSL 发行版,打印 UTF-16 报错后退出 1)。CI runner 上 bash 就是 Git Bash,真机差异。
**处置**:命令级 `set "PATH=C:\Program Files\Git\bin;%PATH%"` 前置 Git Bash(零机器配置改动),重跑即过。
第二次跑 exit=0,**WiX 一发过**(productName=myssia overlay 生效,非 ASCII 雷未触发;tauri CLI 自动下载 WiX 成功):
```
Finished 1 bundle at:
D:\dev\myia\desktop\src-tauri\target\release\bundle\msi\myssia_0.0.1_x64_en-US.msi (122.41 MiB)
```
Rust 全量首编该机约 5 分钟内完成(配置猛),总链(npm ci→sidecar→tauri build)克隆后 ~10 分钟内跑完。✅ AC4(MSI=128,356,352 字节,与 CI 产物 121.8MiB 同量级)。

## §7 S8 静默安装

`msiexec /i myssia_0.0.1_x64_en-US.msi /qn /norestart /L*v msi-install.log` → **EXIT=0 一发过**(SSH 会话上下文即有足够权限,未动 schtasks 提权预案)。
- 安装落点:`C:\Program Files\myssia\`(MYIA.exe + myssia-core.exe + plugin.yaml + plugins + 卸载快捷方式);
- 注册表:DisplayName=myssia / DisplayVersion=0.0.1 / InstallLocation=C:\Program Files\myssia\;
- MSI 日志实证 WebView2 已在本机(`INSTALLED_WEBVIEW2_VERSION=154.0.4258.53`,故未触发 bootstrapper)。✅ AC5

## §8 S9 启动冒烟(坑 ×2:SSH 无桌面上下文 + Windows 静默启动无唤出路径)

### 坑 3:SSH 会话启动 GUI 应用秒退(exit 0)
`Start-Process MYIA.exe` 经 SSH 启动 → 进程即退(0),无窗口无数据目录。根因:OpenSSH 会话是无桌面的非交互上下文,WebView2 应用初始化即退出。**处置**:经 `schtasks /create + /run` 在交互会话(用户桌面)启动——三进程全活(MYIA.exe + myssia-core.exe ×2,PyInstaller onefile 引导+载荷双进程属正常形态)。

### 坑 4(产品发现,非本任务施工缺陷):Windows 发布包静默启动后无唤出路径
`main.rs:357-371`(10-03-quiet-launch):发布包主窗口 `visible:false` 出厂,亮窗三途径=dev 构建 / `MYIA_SHOW_ON_START=1` / macOS Dock Reopen(`#[cfg(target_os="macos")]`)。**Windows 无 Dock、无托盘图标、single-instance 是自持 flock(macOS 导向)——普通 Windows 用户双击图标永远看不到窗口**。macOS 的 Reopen 亮窗路径在 Windows 无等价物。→ 已列入遗留清单第 1 条,建议 Windows 侧补:启动即亮窗 或 托盘图标 或 second-instance 唤出。
自动化验证正路(注释点名):`MYIA_SHOW_ON_START=1` 直跑二进制——批处理 `set MYIA_SHOW_ON_START=1 && start MYIA.exe` 经 schtasks 跑。

### 冒烟证据(亮窗后)
- 截图(schtasks 在交互会话拍屏,scp 回传,Vision OCR 读出)含 MYIA 仪表盘真实渲染文字:`10源 • ok + degraded`、`今日(UTC)run 的 ok 推送 • 受 runs.list 20 条上限`、`告警`、`doctor error+warning 发现`、`14天`——**窗口渲染出真实 UI 内容**(截图混有主人浏览器内容,app 窗口叠于其上);
- 数据根:`%APPDATA%\MYIA` 目录生成(sidecar 数据根 Windows 落位正确);
- 进程:MYIA + myssia-core 同帧存活≥40s,Responding=True。
✅ AC6(进程双活+窗口实渲染;MainWindowHandle=0 系 Tauri 无头标题栏形态,截图证据为准)

### 冒烟后清理
taskkill 双进程;删除 schtasks 冒烟三任务(myssia-smoke/shot/show);**装机保留**(AC8);`D:\dev\myia` 仓库与 `D:\dev\winbuild-log` 日志保留供主人翻阅;ugit 首次失败遗留的 0 字节 `D:\dev\nul`(设备名语法钉子)无害保留并在此记档。

## §9 与 CI 差异清单(完整版)

| # | 差异 | 影响 |
|---|---|---|
| ① | Node v24.12(CI 22) | 无碍,全链绿 |
| ② | 无 rust-cache,首编全量 | 真机 ~5 分钟,一次性成本 |
| ③ | 不签名/无 updater 产物(无 secrets) | 该 MSI 不可用于 updater 升级验证——按设计,不涉发布 |
| ④ | 克隆=UGit 自带 git(CI actions/checkout) | UGit 通道达成主人意图;ugit CLI 本体 GUI 耦合不可无人值守 |
| ⑤ | bash 解析:CI=Git Bash,真机默认=WSL 存根 | PATH 前置 Git Bash 解决(命令级) |
| ⑥ | Windows 静默启动无唤出路径(CI 不跑安装冒烟) | 产品发现,见 §8 坑 4 |

## §复查与遗留

1. **[产品缺口·建议另立任务] Windows 发布包静默启动后无唤出路径**(§8 坑 4)——Windows 是正式交付目标(10-04-windows-build),首装用户双击无窗口是交付级 UX 缺陷。修复方向三选一:Windows 侧启动即 show / 加托盘 / single-instance 二次启动唤出。主人裁决。
2. RustDesk 目验留主人:装机状态保留,连上后跑 `D:\dev\winbuild-log\myia-show.cmd`(已留机)即可亮窗过目;或开始菜单 myssia 图标双击(将静默——见遗留 1)。
3. ugit CLI 的 `clone` GUI 耦合已记档;若主人想用 UGit 图形界面克隆,需人在机器上点。
4. WebView2 已在机(154.0.4258.53),无需随包分发处置;但其他目标用户机器若无 WebView2,MSI 的 downloadBootstrapper 模式在无网/被墙环境会失败——发布文档口径问题,不阻本任务。
5. 本次全链未遇 crates.io 拦截(HEAD 403 只是 bot 拦 curl 探测,cargo 稀疏索引直连全过)、npm/PyPI 直连全过,无需镜像。
6. 主人 `.gitconfig` 明文凭据(cnb.cool)与 git 代理指向未启动的 7897——已提醒,未动。
