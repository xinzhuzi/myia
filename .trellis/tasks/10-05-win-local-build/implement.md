# Implement — Windows 真机本地打包与冒烟(逐步执行单)

> **执行状态:2026-10-05 全部完成,8/8 AC 绿**。实际执行与下述计划的偏差四处在 evidence/build-win.md:ugit clone GUI 耦合降级 UGit 自带 git(§1 坑1)、URL 级代理覆盖键修正(§1 坑2)、PATH 前置 Git Bash 躲 WSL bash 存根(§6 坑3)、SSH 无桌面上下文改 schtasks 交互会话+`MYIA_SHOW_ON_START=1` 亮窗(§8 坑3/坑4)。各步 ✓ 如下。

> 通道总纲:Mac 本会话 → `ssh -o BatchMode=yes <用户>@<局域网IP> "<cmd>"`(远端默认 shell=cmd.exe)。
> 长任务(≥1 分钟)一律 **后台模式**:`run_in_background` + 远端日志文件 + 退出码文件(`&& echo 0 > <file>.exit || echo 1 > <file>.exit`),用 TaskOutput 回看,**禁 sleep 轮询**。
> Windows 侧日志/退出码文件统一放 `D:\dev\winbuild-log\`(首步创建)。
> 每步完成:在本文件勾选 + evidence/build-win.md 追记(实际命令/耗时/坑)。

---

## S0 前置与环境盘点(✅ 会话首探已完成,2026-10-05)

已核实(证据见 evidence/build-win.md §盘点):

- SSH 免密通(`SSH_OK`,家目录 `%USERPROFILE%`);本机同网段 <同网段本机IP>,直连真实。
- UGit 5.54.0:`%USERPROFILE%\AppData\Local\UGit\bin\ugit(.bat)` + 自带 git;`ugit clone <url|slug> [-b branch]` 子命令存在。
- Git for Windows 2.55(Git Bash:`C:\Program Files\Git\bin\bash.exe`);Node v24.12(D:\nodejs);Python 3.12(D:\Python312)。
- MSVC 在:vswhere 实证 `C:\Program Files\Microsoft Visual Studio\18\Enterprise` 与 `...\2022\Community` 均含 VC.Tools.x86.x64。
- **缺**:cargo/rustc/rustup、uv。
- 网络:github.com / api.github.com / registry.npmjs.org / pypi.org / static.rust-lang.org / astral.sh 直连全 200;crates.io API HEAD 403(bot 拦 HEAD,cargo 实走稀疏索引,待 S7 实证)。
- 磁盘:C 269G / D 419.8G / E 649.7G / F 10.8T 空闲;`D:\dev` 已存在。
- Mac 侧:origin=`https://github.com/xinzhuzi/myia.git`;远端 main HEAD=02a438f(并行会话在推,以克隆时实际为准);本地仓零改动。

## S1 建日志目录 + UGit 克隆(AC1)

```bash
# 1) 建远端日志目录 + 目标目录定位(若 D:\dev\myia 已存在则停下人工确认,勿覆盖)
ssh <用户>@<局域网IP> "mkdir D:\dev\winbuild-log 2>nul & if exist D:\dev\myia (echo TARGET_EXISTS) else (echo TARGET_FREE)"

# 2) ugit clone(ugit 克隆到 CWD → 先 cd /d D:\dev)
ssh <用户>@<局域网IP> "cd /d D:\dev && ugit clone https://github.com/xinzhuzi/myia.git"

# 3) 验证:工作树 + commit + 大小
ssh <用户>@<局域网IP> "cd /d D:\dev\myia && git rev-parse HEAD && git log --oneline -2 && dir /s /a:-d | findstr /C:\"个文件\""
```

- **预期**:clone 输出 UGit/clone 完成信息;`git rev-parse HEAD` 出 40 位 hash(记入 evidence);仓库含 `src\`、`desktop\`、`myia-classifier\`、`pyproject.toml`。
- **失败兜底**(D3 链,按序降级,每次降级在 evidence 记明原因):
  1. `ssh ... "cd /d D:\dev && \"%USERPROFILE%\AppData\Local\UGit\app-5.54.0\resources\app\git\cmd\git.exe\" clone https://github.com/xinzhuzi/myia.git"`
  2. `ssh ... "cd /d D:\dev && git clone https://github.com/xinzhuzi/myia.git"`
- **坑**:ugit 若弹 GUI 无输出——观察 60s 内 `D:\dev\myia\.git` 是否出现,无则降级。
- **预计耗时**:1–5 分钟(仓库+git 历史约几十 MB,GitHub 直连)。

## S2 安装 uv(AC2 前半)

```bash
# 1) 官方安装器(PowerShell,装到 %USERPROFILE%\.local\bin)
ssh <用户>@<局域网IP> "powershell -NoProfile -ExecutionPolicy Bypass -Command \"irm https://astral.sh/uv/install.ps1 | iex\""

# 2) 新开会话验证(PATH 已刷新;不行就全路径 %USERPROFILE%\.local\bin\uv.exe)
ssh <用户>@<局域网IP> "uv --version || %USERPROFILE%\.local\bin\uv.exe --version"
```

- **预期**:`uv 0.9.x` 之类版本号。
- **失败兜底**:`ssh ... "D:\Python312\python.exe -m pip install uv"`(装到 D:\Python312\Scripts,验证同路径)。
- **预计耗时**:1 分钟内。

## S3 安装 Rust(rustup + stable-msvc)(AC2 后半)

```bash
# 1) 下载 rustup-init 并无人值守安装;已有 MSVC 会被探测复用,-y 免交互
ssh <用户>@<局域网IP> "curl -L -o %TEMP%\rustup-init.exe https://win.rustup.rs/x86_64 && %TEMP%\rustup-init.exe -y --default-toolchain stable-x86_64-pc-windows-msvc"

# 2) 新会话验证(装到 %USERPROFILE%\.cargo;新 SSH 会话自动带 PATH)
ssh <用户>@<局域网IP> "cargo --version && rustc -vV | findstr host"
```

- **预期**:`cargo 1.8x.x`;`host: x86_64-pc-windows-msvc`;**绝不能是 gnu 后缀**(gnu 会缺 MSVC 链接器语义)。
- **失败兜底**:rustup 探测不到 MSVC 时报 VS Installer 交互——改用 `--default-host x86_64-pc-windows-msvc` 重跑;仍不行人工核对 vswhere 输出。
- **预计耗时**:2–6 分钟(工具链 ~500MB 下载)。

## S4 npm 依赖安装(desktop + ui-src)

```bash
ssh <用户>@<局域网IP> "cd /d D:\dev\myia\desktop && npm ci --no-fund --no-audit && cd ui-src && npm ci --no-fund --no-audit && echo NPM_CI_ALL_OK"
```

- **预期**:两段 npm ci 都 0 退出,尾行 `NPM_CI_ALL_OK`;`desktop\node_modules\` 与 `ui-src\node_modules\` 出现,`desktop\node_modules\.bin\tauri.cmd` 存在。
- **失败兜底**:registry 慢/超时 → 加 `--registry=https://registry.npmmirror.com` 重跑(仅此会话参数,不改机器全局配置);Node 24 兼容报错才考虑装 22 并存。
- **预计耗时**:1–4 分钟。

## S5 构建 Python sidecar(AC3)

Git Bash 下跑(脚本自带 Windows 适配:venv Scripts/、DATA_SEP=`;`、MINGW 主机判定):

```bash
# 后台模式(首次 uv sync 拉 PyPI + onnxruntime 大 wheel,分钟级)
ssh <用户>@<局域网IP> "\"C:\Program Files\Git\bin\bash.exe\" -lc \"cd /d/dev/myia/desktop && bash build-sidecar.sh x86_64-pc-windows-msvc\" > D:\dev\winbuild-log\sidecar.log 2>&1 && echo 0 > D:\dev\winbuild-log\sidecar.exit || echo 1 > D:\dev\winbuild-log\sidecar.exit"
# ↑ 整条挂 run_in_background;完成后 TaskOutput 回看 + 远端核验:

ssh <用户>@<局域网IP> "type D:\dev\winbuild-log\sidecar.exit & dir D:\dev\myia\desktop\src-tauri\binaries"
```

- **预期**:exit=0;`myssia-core-x86_64-pc-windows-msvc.exe` 产出,体积 >30MB;日志尾行 `sidecar built: ...`。
- **脚本内建行为**(知悉勿惊):建隔离 venv `desktop\.venv-build`(uv sync --frozen --no-dev --extra vision);PyInstaller onefile 走手维 `myssia-core.spec`;缓存隔离 `desktop\.pyinstaller-cache`。
- **失败兜底**:
  - uv 不在 bash PATH → 脚本自己会报"未找到 uv";用 `PATH="$HOME/.local/bin:$PATH"` 前缀重跑。
  - PyPI 拉包慢/超时 → 重跑一次(缓存续传);再失败 → `UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple` 前缀重跑(仅命令级,不改全局)。
  - PyInstaller 阶段 Defender 首扫拖慢 → 已知现象,等,勿杀。
- **预计耗时**:3–10 分钟(vision extra 的 onnxruntime wheel ~100MB+)。

## S6 写本地 overlay 配置片(躲 WiX 非 ASCII 雷)

```bash
ssh <用户>@<局域网IP> "echo {\"productName\": \"myssia\"} > D:\dev\myia\desktop\src-tauri\tauri.local.conf.json && type D:\dev\myia\desktop\src-tauri\tauri.local.conf.json"
```

- **预期**:文件内容 `{"productName": "myssia"}`(单行 JSON,Tauri config 合并语义=浅合并覆盖 productName;版本沿用基础 conf 0.0.1;不开签名/不产 updater 包)。
- **该文件本地专用不入库**:验证 `git status --short` 显示 untracked 即可,**不提交**(与 CI 的 tauri.release.conf.json 同样 CI/本地-only 定位)。
- **为什么必须**:基础 conf productName="世事"(非 ASCII),WiX light.exe 产不出非 ASCII 产物名(在册坑,CI 用同法 overlay)。产物将命名 `myssia_0.0.1_x64_en-US.msi`。

## S7 Tauri 构建 MSI(AC4)

```bash
# 后台模式(cargo 首跑全量编译 + WiX 自动下载,10–25 分钟级)
ssh <用户>@<局域网IP> "cd /d D:\dev\myia\desktop && set MYIA_SIDECAR_SKIP=1&& npx tauri build --bundles msi --config src-tauri/tauri.local.conf.json > D:\dev\winbuild-log\tauri.log 2>&1 && echo 0 > D:\dev\winbuild-log\tauri.exit || echo 1 > D:\dev\winbuild-log\tauri.exit"
# ↑ 挂 run_in_background;完成后:

ssh <用户>@<局域网IP> "type D:\dev\winbuild-log\tauri.exit & dir /s /b D:\dev\myia\desktop\src-tauri\target\release\bundle\msi"
```

- **说明**:`MYIA_SIDECAR_SKIP=1` 让 beforeBuildCommand 链(`npm run sidecar && npm run build`)复用 S5 产物不重打包;注意 cmd 里 `set X=1&&`(等号紧贴 &&,防变量值尾带空格)。`npm run build` 会真实跑 vite 构建 `ui-src → ui\`(冒烟必需)。
- **预期**:exit=0;`bundle\msi\` 下出现 `myssia_0.0.1_x64_en-US.msi`(约 100–130MB)。
- **失败兜底**:
  - WiX 下载失败(GitHub release 直连已 200,低概率)→ 重跑一次。
  - crates.io 拉包失败 → `%USERPROFILE%\.cargo\config.toml` 写 rsproxy 镜像再跑(改的是新增文件,可回滚删除)。
  - sidecar 被重复打包(说明 SKIP 没生效)→ 无害,只是多花几分钟。
- **预计耗时**:10–25 分钟(Rust 首编大头)+ vite 构建 1–2 分钟。

## S8 静默安装 MSI(AC5)

```bash
# 1) 找到产物全名(上一步已知,占位 <MSI>)
ssh <用户>@<局域网IP> "dir /b D:\dev\myia\desktop\src-tauri\target\release\bundle\msi"

# 2) 静默安装(退出码:0=成,3010=成需重启,1603/1925=权限/失败)
ssh <用户>@<局域网IP> "msiexec /i D:\dev\myia\desktop\src-tauri\target\release\bundle\msi\<MSI> /qn /norestart /L*v D:\dev\winbuild-log\msi-install.log & echo EXITCODE=%ERRORLEVEL%"

# 3) 失败(1603/1925)时:schtasks 免 UAC 提权通道
ssh <用户>@<局域网IP> "schtasks /create /tn myssia-install /tr \"msiexec /i D:\dev\myia\desktop\src-tauri\target\release\bundle\msi\<MSI> /qn /norestart /L*v D:\dev\winbuild-log\msi-install.log\" /sc once /st 23:59 /rl highest /f && schtasks /run /tn myssia-install"
# 查询结果直到 LastResult 出 0/3010:
ssh <用户>@<局域网IP> "schtasks /query /tn myssia-install /v /fo list | findstr /i result & type D:\dev\winbuild-log\msi-install.log | findstr /i \"error\""

# 4) 定位安装落点(mainBinaryName=MYIA → MYIA.exe)
ssh <用户>@<局域网IP> "dir /s /b \"C:\Program Files\myssia\MYIA.exe\" 2>nul & dir /s /b \"C:\Program Files (x86)\myssia\MYIA.exe\" 2>nul & powershell -NoProfile -Command \"Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*, HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* -ErrorAction SilentlyContinue | Where-Object DisplayName -like '*myssia*' | Select DisplayName, InstallLocation | Format-List\""
```

- **预期**:EXITCODE=0;`MYIA.exe` 落盘(典型 `C:\Program Files\myssia\MYIA.exe`),注册表 DisplayName=myssia。
- **预计耗时**:1–3 分钟。

## S9 启动冒烟(AC6)

```bash
# 1) 启动(不抢焦点:PowerShell Start-Process 默认不置前台;家机无人值守,可接受)
ssh <用户>@<局域网IP> "powershell -NoProfile -Command \"Start-Process '<S8定位到的MYIA.exe全路径>'\""

# 2) 等 20 秒后核验:双进程 + 窗口标题 + 应用数据目录(identifier=com.myssia.app)
ssh <用户>@<局域网IP> "tasklist | findstr /i \"MYIA myssia-core\" & powershell -NoProfile -Command \"Get-Process MYIA -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,MainWindowTitle | Format-List\" & dir /b %APPDATA%\com.myssia.app 2>nul"

# 3) 冒烟完成,收进程(静默纪律:不霸屏;安装保留)
ssh <用户>@<局域网IP> "taskkill /im MYIA.exe /f 2>nul & taskkill /im myssia-core-x86_64-pc-windows-msvc.exe /f 2>nul & echo SMOKE_DONE"
```

- **预期**:MYIA.exe + myssia-core-x86_64-pc-windows-msvc.exe 两进程同帧;MainWindowTitle 非空(如"世事")或 `%APPDATA%\com.myssia.app` 目录生成,至少其一;WebView2 Win11 内置无需装。
- **失败排查**:sidecar 没起 → 查 `%APPDATA%\com.myssia.app\logs`(或 `myssia-core` 相关日志);窗口空标题但进程在 → 数据目录作准。
- **预计耗时**:1 分钟。

## S10 收尾(AC7 / AC8)

1. `evidence/build-win.md` 落盘:盘点记录、每步实际命令+耗时、坑与解法、与 CI 差异清单(①Node 24 vs 22、②无 rust-cache 首编全量、③不签名/无 updater 产物、④ugit 通道)、AC 逐条勾选证据。
2. Windows 侧:保留安装与 `D:\dev\myia`(装机包判例);`D:\dev\winbuild-log` 保留供主人翻阅;不动 uv/rust(通用工具链)。
3. Mac 侧:本文件勾选 + prd.md AC 勾选;task.json 直改 status→review(并行会话在场,禁 start/finish);三件套+evidence 提交入库(仅 `.trellis/tasks/10-05-win-local-build/`,零代码改动,detect-changes 可豁免——纯文档)。
4. 主人侧遗留(不阻交付,写入 prd/复查):RustDesk 打开真机目验 UI;如需卸载 `msiexec /x <MSI> /qn`。

## 验证命令总表(门禁)

| 节点 | 命令 | 判据 |
|---|---|---|
| S1 | `ssh ... "cd /d D:\dev\myia && git rev-parse HEAD"` | 40 位 hash,记 evidence |
| S2/S3 | `uv --version` / `cargo --version && rustc -vV \| findstr host` | 版本可打印,host=msvc |
| S5 | `dir ...\binaries\myssia-core-x86_64-pc-windows-msvc.exe` | 存在,>30MB |
| S7 | `dir /s /b ...\bundle\msi\*.msi` | ASCII 名 msi 存在 |
| S8 | `echo %ERRORLEVEL%` / schtasks LastResult | 0 或 3010 |
| S9 | tasklist 双进程 + 标题/数据目录 | 至少一据成立 |
