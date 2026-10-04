# Design — Windows 真机本地打包与冒烟

## 1. 通道与拓扑

```
Mac(本会话,MYIA 仓) --免密SSH(cmd)--> Windows 真机 <用户>@<局域网IP>
                                          ├─ UGit 5.54.0(自带 git 2.x)
                                          ├─ Git for Windows 2.55(Git Bash)
                                          ├─ Node v24.12 / Python 3.12
                                          ├─ VS2022 Community + VS18 Enterprise(VC.Tools.x86.x64)
                                          ├─ 待装:uv、rustup(stable-msvc)
                                          └─ GitHub/npm/PyPI/rustup/astral 直连 200 OK
```

- 所有远端操作走 `ssh -o BatchMode=yes <用户>@<局域网IP> "<cmd>"`(cmd 默认 shell);需要 bash 的步骤显式调 `"C:\Program Files\Git\bin\bash.exe" -lc "..."`。
- **长任务模式**(工程纪律):`ssh ... "cmd > log 2>&1 && echo 0 > exit.file || echo 1 > exit.file"` 挂 Mac 侧 run_in_background,回看用 `TaskOutput`,禁 sleep 轮询。
- Windows 侧工作目录:`D:\dev\myia`(D 盘 419GB 空闲,`D:\dev` 已存在;路径短——PyInstaller/cargo 长路径风险低)。

## 2. 构建链:CI windows-msi job → 真机等价映射

| CI(runner) | 真机等价 | 备注 |
|---|---|---|
| actions/checkout | `ugit clone https://github.com/xinzhuzi/myia.git`(R1 点名 UGit) | 克隆后记录 commit;UGit 失败兜底=UGit 自带 git.exe → 系统 git |
| setup-uv(python 3.11) | `irm https://astral.sh/uv/install.ps1 \| iex` | 兜底:`D:\Python312\python.exe -m pip install uv`;requires-python>=3.11,uv 自管 python 亦可 |
| setup-node 22 | 已有 Node v24.12 | **与 CI 差异①**:无 engines 锁,@tauri-apps/cli^2 与 vite5 兼容 24,风险低 |
| dtolnay/rust-toolchain stable | `rustup-init.exe -y --default-toolchain stable-x86_64-pc-windows-msvc` | MSVC 已在(vswhere 实证),rustup 直接探测复用,免 VS Build Tools 大下载 |
| rust-cache | 无(首构建全量) | **与 CI 差异②**:首跑 cargo 全量编译,预计 5–20 分钟 |
| npm ci(desktop)+ npm ci(ui-src) | 同命令直跑 | |
| `bash build-sidecar.sh x86_64-pc-windows-msvc` | Git Bash 直跑同脚本 | 脚本自带 Windows 适配(venv Scripts/、DATA_SEP=';'、MINGW 主机判定) |
| 解析 version + 写 tauri.release.conf.json(secrets 注入) | 写 `tauri.local.conf.json` 最小片 | **与 CI 差异③(核心)**:无 updater secrets → 不签名、不 createUpdaterArtifacts;只留 `{"productName":"myssia"}`——躲 WiX 非 ASCII 产物名雷(在册:WiX light.exe 产不出"世事"名;CI 同法 overlay)。版本沿用基础 conf 0.0.1 |
| `npx tauri build --bundles msi --config ...`(MYIA_SIDECAR_SKIP=1) | 同命令 | WiX 由 tauri CLI 自动下载到 %LOCALAPPDATA%\tauri(GitHub 直连 200,可行) |
| 产物改 ASCII 名 / 上传 artifact / Release | 不做 | 本地验证不发布(tag 驱动纪律) |

## 3. 关键决策

- **D1 不签名构建**:updater 私钥只在 GitHub Secrets,本地不可能也不应该拿到。基础 conf 占位符+不开签名=本地无钥构建不破(CI 注释在案)。代价:该 MSI 不能用于 updater 升级验证——不在本任务范围。
- **D2 productName overlay 而非改基础 conf**:基础 conf 的 productName="世事" 是 mac 正式显示名,不能为 Windows 动它;overlay 片只影响本次构建产物,零入库(文件加 .gitignore 检查,不入库不提交)。
- **D3 克隆用 ugit CLI**:R1 明示。ugit clone 语义=克隆到 CWD;先 `cd /d D:\dev` 再 clone。若 ugit clone 触发 GUI/失败,降级链:UGit 自带 git.exe → 系统 git,证据里记明实际用哪条。
- **D4 静默安装优先,提权走 schtasks**:`msiexec /i <msi> /qn /norestart /L*v` 直跑;若 SSH 非提升上下文导致 1603/1925,用 `schtasks /create ... /rl highest + /run` 免 UAC 弹窗完成提升安装(家机无人值守前提);仍失败才留主人手装(违反则任务降档,AC5 打 ✗ 如实回填)。
- **D5 冒烟后杀进程、保留安装**:按静默后台纪律不霸屏;但装机状态保留(RustDesk 目验留给主人;交付完成判定含装机包判例)。
- **D6 Trellis 并行纪律**:并行会话在场,`task.py start/finish` 禁用——task.json 直改 status:planning→in_progress→review。

## 4. 风险与兜底

| 风险 | 概率 | 兜底 |
|---|---|---|
| ugit clone 实为 GUI 唤起/行为不明 | 中 | 探测 60s 无 .git 即降级 D3 链 |
| crates.io 拉取被拦(HEAD 403 前科) | 低 | cargo 走 index.crates.io 稀疏索引;真被拦再换 `[source.crates-io] replace-with` 镜像(字节镜像 rsproxy) |
| PyPI 慢(vision extra 含 onnxruntime 大 wheel) | 中 | UV_DEFAULT_INDEX 切清华 tuna;再不行砍 --extra vision?——不砍,CI 怎么锁真机怎么来,慢就等 |
| PyInstaller onefile 在 Win Defender 首扫慢 | 中 | 已知现象非失败;后台模式天然容忍 |
| msiexec 需提权 | 中 | D4 schtasks 通道 |
| Node 24 兼容性 | 低 | 出错再装 Node 22 LTS(D 盘并存,不动 24) |
| rustup 下载 rust-std 慢 | 低 | static.rust-lang.org 直连已 200;超时重跑(断点续传) |

## 5. 回滚

- Windows 侧:安装产物可 `msiexec /x <msi> /qn` 卸载;`D:\dev\myia` 整目录可删;uv(%USERPROFILE%\.local\bin)与 rust(%USERPROFILE%\.cargo\.rustup)保留(通用工具链,删需主人令)。
- Mac 侧:只新增 `.trellis/tasks/10-05-win-local-build/`,零代码改动,无回滚面。
