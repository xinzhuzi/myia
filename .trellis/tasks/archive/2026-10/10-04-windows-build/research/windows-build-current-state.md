# 探查:Windows 产物化现状(2026-10-04,本会话实测)

依据:任务授权口径(交付=CI Windows 目标绿 + 安装/SmartScreen 文档,真机冒烟留主人)
+ v12-backlog prd 第 1 项(`.trellis/tasks/10-03-v12-backlog/prd.md:11-16`)。
以下所有行号/命令输出均为 2026-10-04 本会话在 main(71e00db)工作树上实测;
GitHub 侧证据经 `gh`(已登录)拉取。

---

## 0. 结论速览(先纠一个事实)

| # | 事实 | 证据 |
|---|---|---|
| R1 | **「desktop-release.yml 是 mac-only」的开工假设已过时**:windows-msi job 自 v1.1(40a666a)就存在,但 `continue-on-error: true` 且**三次真实 run 全红**,全部死在「构建 sidecar」一步 | `git log -S "windows-msi"` → 40a666a;§1 run 清单 |
| R2 | **Windows 红的根因唯一且已实锤**:`uv sync --extra vision` 拉 `ocrmac` → `pyobjc-framework-vision` 在 Windows 只有 sdist(macosx 专属 wheel),sdist 构建即炸 | run 37117015528 失败日志(§1.2);uv.lock:2142-2153、2891-2910 |
| R3 | 修好 R2 后还有**两个必然连环炸**:(a) `tauri.conf.json` 的 `bundle.icon` 无 `.ico` → WiX 打包直接报 `Couldn't find a .ico icon`;(b) msi 文件名含非 ASCII `世事` → GitHub 剥名(仓内 bfb60a0 已实证的同款坑),且现 workflow 上传 glob 与 bundler 实际输出目录不符 | tauri-bundler 源码(§3.1/§3.2);desktop-release.yml:233-240 |
| R4 | 装机链其余环节(rust 壳、sidecar spawn、数据根、插件资源)对 Windows 的适配**已就绪**,有源码级证据,无需动 desktop/entry.py / main.rs | §4 |
| R5 | 文档面:README 安装节仅 macOS;UPDATER.md 第三节维持「windows latest.json 手工补」;SmartScreen/签名零文档 | README.md:181-195;desktop/UPDATER.md:62、113 |

任务的真实命题因此不是「从零加 Windows 目标」,而是 **「Windows 目标从构建级验证(红)转正式交付(绿)+ 发行文档」**。

---

## 1. CI 现状(gh 实测)

### 1.1 desktop-release.yml 全部历史 run

`gh run list -R xinzhuzi/shishi --workflow=desktop-release.yml`:

| run | 触发 | 结论 | windows-msi job | macos-dmg job |
|---|---|---|---|---|
| 37095582342 | push v1.1.1(tag 已删) | success | **failure** | success |
| 37115937735 | push v0.0.1 | success | **failure** | success |
| 37117015528 | push v0.0.1 | success | **failure** | success |

(workflow 总结论 success 是因为 windows job `continue-on-error: true`;远端现存 tag 仅 v0.0.1。)

### 1.2 根因日志(run 37117015528,`gh run view --log-failed`)

```
cause: Call to `setuptools.build_meta.get_requires_for_build_wheel` failed (exit code 1)
  File ".../pyobjc-framework-vision/12.2.2/.../src/pyobjc_setup.py", line 470, in Extension
    if "clang" in get_config_var("CC"):
TypeError: argument of type 'NoneType' is not iterable
hint: `pyobjc-framework-vision` (v12.2.2) was included because `shishi[vision]` (v0.0.1)
      depends on `ocrmac` (v1.0.1) which depends on `pyobjc-framework-vision`
```

死在 `desktop/build-sidecar.sh:83` 的 `UV_PROJECT_ENVIRONMENT="$VENV" uv sync --frozen --no-dev --extra vision --project "$ROOT_DIR"`,即依赖装配期,PyInstaller 还没开跑。

### 1.3 依赖侧证据(uv.lock 实读)

- `ocrmac 1.0.1`(uv.lock:2142-2153):wheel 是 `py3-none-any`,但依赖 `pyobjc-framework-vision` → `pyobjc-core` + `pyobjc-framework-cocoa/coreml/quartz`;`pyobjc-framework-vision 12.2.2`(uv.lock:2891-2910)的 wheel **全部是 `macosx_*`**,Windows 只能走 sdist,sdist 在非 macOS 上构建必炸(1.2 的 TypeError 即此)。
- pyproject 的 vision extra 无平台标记:pyproject.toml:47 `vision = ["ocrmac>=1.0", "rapidocr-onnxruntime>=1.3", "openai>=1.30", "huggingface-hub>=0.23"]`。
- vision extra 其余依赖的 Windows wheel 均已锁(awk 全块统计):onnxruntime 4 个 `win_amd64`、selectolax 11 个、pydantic-core 6 个;keyring 的 win 侧依赖 `pywin32-ctypes` 带 `sys_platform == 'win32'` 标记已在锁内(uv.lock:1523)。**→ ocrmac/pyobjc 是唯一 Windows 装不上的链。**
- uv 版本 0.7.6(本机实测),`uv sync` 无 `--no-package`,有 `--no-install-package`(仅跳过指定包本身,拦不住 ocrmac 的传递依赖 pyobjc,不可行——排除)。
- **锁文件坑**:uv.lock 全部 URL 指向 tsinghua 镜像,但仓内无 uv.toml / `[tool.uv] index` / UV_* env → 当初是持 `UV_DEFAULT_INDEX` 锁的。**重锁必须带同镜像 env,否则全文件 URL churn**;且 uv.lock 当前有外来未提交改动(+5/-1,并行会话),实施时叠加勿覆写。

## 1.5 PyInstaller spec 对缺失包的行为(本机实测)

`desktop/.venv-build/bin/python`(PyInstaller 6.22.3)实跑:

```
from PyInstaller.utils.hooks import collect_all
collect_all('totally_missing_pkg_xyz')
→ 14 WARNING: collect_data_files - skipping … as it is not a package.
→ 14 WARNING: collect_dynamic_libs - skipping …
→ no-exception: [0, 0, 0]
```

**修正一个初判**:我最初判断 myia-core.spec:13 的 `collect_all('ocrmac')` 在 ocrmac 缺席时会炸——实测只警告不炸。即 pyproject 标记修复后,Windows 上 spec 可以不改也能跑;给 ocrmac 加平台门属于卫生性改动(日志干净+意图明确),不是必需。→ 记入 prd grill 修正。

---

## 2. 打包配置现状(tauri.conf.json 实读,desktop/src-tauri/tauri.conf.json)

- `bundle.icon: ["icons/icon.icns", "icons/icon.png"]`(:30)——**无 `.ico`**。`icons/icon.ico` 文件本身存在(84,679 字节,2026-10-03 生成,与 icns 同批),只是没进 icon 列表。
- `bundle.targets: ["app", "dmg"]`(:29)——mac-only;CI 靠 `--bundles msi` 覆盖,基础 conf 无需为 CI 改(本地 Windows 出包暂无场景)。
- `mainBinaryName: "MYIA"`(:4)+ sidecar 名 `myia-core`:NTFS 与 APFS 同为大小写不敏感,`myia-core` ≠ `MYIA` 不撞名——仓教训(build-sidecar.sh:112-113 注释)在 Windows 同纪律成立,现状已规避。
- `productName: "世事"`(:3)→ msi 文件名前缀非 ASCII(§3.2)。
- `plugins.updater.windows.installMode: "passive"`(:49-51):Windows 静默升级配置已备。
- CSP `connect-src … http://ipc.localhost`(:24):Windows 的 IPC origin 已放行。
- externalBin `binaries/myia-core`(:31)+ 脚本按 triple 产出 `myia-core-x86_64-pc-windows-msvc.exe`。

## 3. tauri-bundler 源码级核验(zread 直读上游 master)

### 3.1 `.ico` 是 msi 打包硬前提

`crates/tauri-bundler/src/bundle/windows/msi/mod.rs`:

```rust
let icon_path = … else {
    settings.icon_files().flatten()
      .find(|i| i.extension() == Some(OsStr::new("ico")))
      .context("Couldn't find a .ico icon")?
};
```

icon 列表无 `.ico` 时 WiX 打包**必炸**——这是 R2 修好后的第一颗连环雷(R3a)。

### 3.2 msi 输出文件名与目录

- 输出名 = `{productName}_{version}_{arch}_{language}.msi`(`app_installer_output_path`),默认语言 en-US → `世事_<ver>_x64_en-US.msi`。GitHub 剥非 ASCII 资产名(仓内 bfb60a0 实证,workflow:112-114 注释在案)→ **上传前必须改 ASCII 名**(R3b),且 latest.json 的 windows URL 必须指 ASCII 名。
- 目录:常规 msi → `bundle/msi/`;**updater msi(+`.msi.sig`)→ `bundle/msi-updater/`**(`WIX_OUTPUT_FOLDER_NAME="msi"` / `WIX_UPDATER_OUTPUT_FOLDER_NAME="msi-updater"`,util.rs)。现 workflow 上传 glob 写的是 `bundle/msi/*.msi.sig`(desktop-release.yml:240)——`.sig` 根本不在该目录,`fail_on_unmatched_files: true` 必红(R3 的第二半;此步从未被执行到过,属潜伏雷)。updater 版 msi 与常规版的差异仅在 webview 安装模式(updater 固定 DownloadBootstrapper silent),作发行资产二选一即可。
- externalBin 落位:`generate_binaries_data` 把 `myia-core-x86_64-pc-windows-msvc.exe` 去 `-<target>` 后缀拷进临时目录随包安装 → 装机后与 MYIA.exe 同目录的 `myia-core.exe`(§4.2 的 sidecar 解析与之闭环)。

### 3.3 workflow_dispatch 现状是坏的(顺带发现)

release conf 片的版本取 `${{ github.ref_name }}` 去掉 `v` 前缀(desktop-release.yml:94-99):dispatch 于分支时 ref_name=分支名 → `version: "10-04-windows-build"` → WiX `convert_version` semver 解析必炸(mac 侧 tauri 同样要 semver)。三次 run 全是 tag push,dispatch 从未被行使,所以没暴露。**实施时须给 dispatch 加版本入参/缺省回退,否则本任务的 CI 验证循环(不推 tag)无法走通**——这是实施期的主要验证通道,必须修。

## 4. 装机链其余环节(已就绪,有源码证据,零改动)

1. **rust 壳 spawn**:`main.rs:153` `app.shell().sidecar("myia-core")`;tauri-plugin-shell `Command::new` 在 Windows 默认 `creation_flags(CREATE_NO_WINDOW)`(plugins-workspace `plugins/shell/src/process/mod.rs`,`const CREATE_NO_WINDOW: u32 = 0x0800_0000`)→ PyInstaller `console=True` 的 sidecar 在 Windows **不会弹黑窗**(曾列风险,源码核销)。`relative_command_path` 在 Windows 自动补 `.exe`,`myia-core` → `myia-core.exe` 解析闭环。
2. **数据根**:`main.rs:243-254` `myia_home_dir` Windows = `AppData\Roaming\MYIA`(预建);entry.py:388-397 `myia_home()` win32 走 `%APPDATA%\MYIA`(env 缺失回退拼路径),两侧一致。
3. **插件资源**:entry.py:411-429 `_bundle_plugins_dir` 候选含 `exe.parent/"plugins"`(Windows/Linux 资源保持相对结构落 exe 旁)——tauri.conf resources 映射的 `plugins/*.yaml` 命中该候选;首跑种子逻辑(spec python/index.md「桌面发行数据根」节)平台无关。
4. **build-sidecar.sh 的 Windows 形状已在**:主机三元组推断(MINGW/MSYS)、`Scripts/python.exe` 双探测(:76-77)、`DATA_SEP=";"`(:103-104)、`.exe` 后缀(:57-59)、PYINSTALLER_CONFIG_DIR 私有缓存(:109)。spec 的 datas 走元组,天然免疫 add-data 分隔符坑。
5. **CRLF**:entry.py:1171 注释在案,yaml 写回 `newline=""` 已处理(10-03-yaml-editor)。
6. **单实例锁/焦点让渡**:main.rs:279-308 为 `#[cfg(target_os = "macos")]`,Windows 下自然不编译不生效(单实例在 Windows 靠 MSI 升级码/快捷方式约束较弱,记入真机冒烟清单观察项,非本任务改码项)。

## 5. 文档现状

- README.md:181-195「下载安装(桌面应用)」仅 macOS(右键打开绕 Gatekeeper);Windows 安装/SmartScreen 零文档。
- desktop/UPDATER.md:62(第三节)Windows 条目「手工补 latest.json」;:113(第六节)Windows 构建级允许失败的旧口径——产物化后两处都要改。
- docs/zh|en/getting-started.md 是 CLI 源码安装向导(桌面安装入口只在 README),桌面 Windows 文档收 README 一处即可,双语不动(getting-started 无桌面节)。
- ci.yml 全部 ubuntu-latest(Python 测试矩阵无 Windows)——超出本任务域,注记不动。

## 6. 上游/口径双源冲突(如实注记)

- v12-backlog prd:68-71 记 2026-10-03 grill Q4 主人答「Windows 真机/VM:**有**」;
- 2026-10-04 任务授权口径:「主人有无 Windows 真机未知——交付=CI Windows 目标绿+安装/SmartScreen 文档,真机冒烟留主人」。
两源并存,以更新的授权口径为准(冒烟=主人侧清单,不阻交付),prd 待拍板 D10 如实记录两源。

## 7. 本会话执行的检查清单(可复现)

| 检查 | 命令 | 结果 |
|---|---|---|
| run 历史 | `gh run list -R xinzhuzi/shishi --workflow=desktop-release.yml` | 3 run,见 §1.1 |
| windows job 结论 | `gh run view <id> --json jobs --jq …`(×3) | 均 failure,死在构建 sidecar |
| 根因日志 | `gh run view 37117015528 --log-failed` | pyobjc 链,见 §1.2 |
| collect_all 缺包行为 | `desktop/.venv-build/bin/python -c …`(PyInstaller 6.22.3) | 仅警告不炸,§1.5 |
| win wheel 覆盖 | `awk` 全块统计 uv.lock | onnxruntime/selectolax/pydantic-core 均有 win_amd64;pyobjc 仅 macosx |
| uv 能力 | `uv --version` / `uv sync --help` | 0.7.6;`--no-install-package` 在,`--no-package` 不在 |
| 图标资产 | `ls -la desktop/src-tauri/icons/icon.ico` | 存在 84,679 B |
| 远端 tag | `git ls-remote --tags origin` | 仅 v0.0.1(v1.1.1 已删) |
| bundler 源码 | zread 直读 tauri master `msi/mod.rs`、`util.rs`、plugin-shell `process/mod.rs` | §3、§4.1 |

未做(如实):未在本机跑 Windows 构建(darwin 主机,PyInstaller 不可交叉编译,build-sidecar.sh:52-56 会拦);未推 tag/dispatch 触发新 run(发布动作归主人,实施期验证通道见 §3.3)。

---

## 8. 追记:起草期间树况漂移(2026-10-04 ~10:58 实测)

本档探查基于 71e00db 基线(外来未提交 24 项)。起草收尾时 `git status --porcelain`
已膨胀到 271 项——并行会话在飞**大规模 shishi→myia 改名扫荡**,已实证波及:

- `pyproject.toml`:project name `shishi`→`myia`(vision extra 行内容未动);
- `.github/workflows/desktop-release.yml`:mac 资产 ASCII 前缀 `shishi_*`→`myia_*`
  (diff 9+/9-,windows 段未动——本任务主战场尚无人碰);
- README(徽章 repo 链接 xinzhuzi/myia、CLI 名 `myia run` 等)、目录
  `myia-classifier` 重命名(git diff 通览)。

对本档结论的影响:R1-R5、§1-§7 的**事实与根因全部不受影响**(改名不改依赖链、
bundler 行为、CI 结论);受影响的只有**实施基线**——ASCII 资产前缀应对齐
`myia`(prd Constraints「并行改名协调」、design §3.2/§4.1 已按此定稿),行号
引用实施时以扫荡后现状二次核对。探查期间执行的 gh 命令以 `xinzhuzi/shishi` 为
repo 参数(当时实况),实施期若远端同步改名则以新名为准。
