# design — Windows 产物化:CI 构建与发行文档

依据:本档 prd.md(权威需求 + grill 决议)+ `research/windows-build-current-state.md`
(全部证据出处:CI run 日志、tauri-bundler/plugin-shell 源码、uv.lock 实读、本机实测)。
行号以 2026-10-04 main(71e00db)工作树为准。

---

## 0. 结论速览

| 决策点 | 结论 | 依据 |
|---|---|---|
| 根因修复 | pyproject vision extra 的 ocrmac 加 `; sys_platform == 'darwin'` 标记 + 带 tsinghua 镜像 env 重锁 | run 37117015528 日志;uv.lock pyobjc 全 macosx wheel |
| spec 平台门 | `collect_all('ocrmac')` 三行包 `if sys.platform == 'darwin':`(卫生项,缺包实测仅警告) | 本机 PyInstaller 6.22.3 实测 |
| 图标 | `bundle.icon` 追加 `icons/icon.ico`(文件已在) | tauri-bundler msi/mod.rs `.context("Couldn't find a .ico icon")` |
| workflow 结构 | 三 job:macos-dmg(不变+多传 artifact)/ windows-msi(转正式+ASCII 改名+artifacts)/ release-finalize(归聚:挂 windows 资产+写 latest.json) | D1/D5/D6 |
| dispatch | 加 `version` 入参(缺省回退 tauri.conf.json 的 0.0.1);release 上传步以 `startsWith(github.ref, 'refs/tags/')` 为门 | research §3.3(分支名非 semver 必炸) |
| 文档 | README 安装节 Windows 小节 + UPDATER.md §3/§6 改口径 + 冒烟清单主人侧 | D8/D10 |

**零触碰**:desktop/entry.py、src/myia/schema.py、tests/test_desktop_sidecar_protocol.py、
desktop/ui-src(research §4 已证装机链 Windows 适配就绪,源码级)。

---

## 1. 变更面与边界

| 文件 | 变更 | 性质 |
|---|---|---|
| `pyproject.toml:47` | `vision` 数组中 `"ocrmac>=1.0"` → `"ocrmac>=1.0; sys_platform == 'darwin'"` | 1 行,最小侵入 |
| `uv.lock` | 重锁(ocrmac 条目 + marker;**必须 `UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple` 下锁**,否则全文件 URL churn)。外来未提交改动(+5/-1)叠加勿覆写 | 生成物 |
| `desktop/myia-core.spec:13-14` | ocrmac 的 collect_all 三行加 `sys.platform == 'darwin'` 门 | 卫生项 |
| `desktop/src-tauri/tauri.conf.json:30` | icon 数组追加 `"icons/icon.ico"` | 1 行 |
| `.github/workflows/desktop-release.yml` | §3 全量(Windows job 重构 + 归聚 job + dispatch 版本 + ASCII 改名 + glob 修正) | 主战场 |
| `README.md` 「下载安装」节 | Windows 小节 + SmartScreen/Defender 注记 | 文档 |
| `desktop/UPDATER.md` §3(:62 一带)/§6(:113) | 手工补条目→归聚自动化;构建级验证旧口径→正式目标 | 文档 |
| `.github/workflows/desktop-release.yml` 头部注释 | 「已知边界」段同步(Windows 不再允许失败;latest.json 单写者) | 文档 |

## 2. 依赖修复设计(F1)

```toml
# pyproject.toml [project.optional-dependencies]
vision = [
    "ocrmac>=1.0; sys_platform == 'darwin'",   # macOS Vision 独占;Windows/Linux 无 wheel(锁内全 macosx)
    "rapidocr-onnxruntime>=1.3",
    "openai>=1.30",
    "huggingface-hub>=0.23",
]
```

- marker 语义:macOS 装配与现状逐字节等价(marker 恒真);Windows/Linux 跳过
  ocrmac 及其 pyobjc 传递链,其余 vision 依赖的 win_amd64 wheel 已在锁内
  (research §1.3 统计)。
- 重锁:`UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple uv lock`
  ——锁内 URL 体系与现状一致,预期 diff 限于 ocrmac 条目加 marker(及可能的
  hash 重排);若 diff 意外扩大,以 `git diff uv.lock` 人工核后再收。
- 运行期影响:Windows 侧看图引擎=rapidocr 单擎(ocrmac 本就 macOS-only,
  vision 双引擎按平台择一,非降级);`shishi` 核心依赖零变化。
- 兼容性:vision extra 的 macOS 消费者(装机包)无感;CI ci.yml(ubuntu)不装
  vision,不受影响。

### spec 平台门(F2b)

```python
import sys
# …
if sys.platform == 'darwin':
    tmp_ret = collect_all('ocrmac')
    datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
```

Windows 下 ocrmac 不再安装,此门让 spec 不吐两条 WARNING 并显式声明平台意图;
不加也不炸(实测),故为卫生项。**增删依赖仍改 spec 本体,勿走 CLI 重生成路径**
(绝对路径回写坑,build-sidecar.sh:116-122 注释在案)。

## 3. workflow 重构设计(F3)

### 3.1 job 拓扑

```
macos-dmg ──────┬─→ release-finalize(if: always() && needs.macos-dmg.result=='success')
windows-msi ─────┘
```

- **macos-dmg**:现有步骤全部保留(守卫/构建/ASCII 改名/latest.json 生成除外——
  latest.json 生成与上传移出,见下);新增一步 `actions/upload-artifact`
  (name: `mac-updater`,内容:`myia.app.tar.gz.sig` 一个小文件;ASCII 前缀随
  2026-10-04 改名扫荡后的现行口径,扫荡把 shishi_*→myia_*)。
  dmg/app.tar.gz/.sig 照旧由本 job 直接挂 Release(tag 场景;generate_release_notes
  留在本 job——release 的创建者)。
- **windows-msi**:移除 `continue-on-error: true`;加 `timeout-minutes: 60`
  (grill R2-D6c:挂死不得无限期拖住 latest.json);构建链照旧(uv sync 随 F1
  自然变绿);新增「产物改 ASCII 名」步 + `upload-artifact`(name: `win-msi`,
  msi + sig);**不再直接调 softprops/action-gh-release**(消除双 job 并行
  create-release 竞态,research §1.1 三次 run 中 windows 从未走到上传,竞态是
  潜伏而非已证,顺手根治)。
- **release-finalize**(新):`runs-on: ubuntu-latest`(grill R2-D6a:jq 预装),
  `needs: [macos-dmg, windows-msi]`,
  `if: always() && needs.macos-dmg.result == 'success'`:
  1. download 两个 artifacts;
  2. 写 latest.json:darwin-aarch64 条目恒在(读 mac sig artifact 内容);
     windows-x86_64 条目仅当 win artifact 存在(signature=msi.sig 内容,
     url=ASCII 资产名);`pub_date: now`;notes 沿用「世事 <版本>」格式;
  3. latest.json 无条件 `upload-artifact`(name: `latest-json`)——dispatch
     验证循环里 latest.json 生成逻辑真实执行、产物供人验(grill R2-D6b:
     首次真实运行不应是主人推 tag 时);
  4. softprops 上传两步(windows 产物存在→挂 msi+sig,不带
     generate_release_notes,release 已由 mac job 创建;挂 latest.json)
     各加 `if: startsWith(github.ref, 'refs/tags/')`——**job 本体不整体
     tag 门**(grill R2-D6b 修正:原设计把整个 job 门在 tag 后,dispatch
     循环里 latest.json 逻辑零执行,最易错件的首跑恰是主人推 tag)。

### 3.2 Windows job 关键步骤形状

```yaml
- name: 产物清单(诊断;glob 以实测为准的依据)
  shell: bash
  run: find desktop/src-tauri/target/release/bundle -type f | sort

- name: 产物改 ASCII 名(GitHub 剥非 ASCII 资产名;对齐 mac 先例 bfb60a0)
  shell: bash
  run: |
    VERSION="${VERSION_REF#v}"
    B="desktop/src-tauri/target/release/bundle"
    # updater msi(含 .sig)在 msi-updater/;常规 msi 在 msi/。发行资产取
    # updater 版(差异仅 webview 安装模式,updater 版为 DownloadBootstrapper
    # silent,首装同样适用);路径若与实测不符,以上一步清单为准修正。
    # ASCII 前缀 = myia(2026-10-04 改名扫荡后现行口径,与 mac myia_* 对齐)。
    cp "$B"/msi-updater/*_x64*.msi     "$B/myia_${VERSION}_x64.msi"
    cp "$B"/msi-updater/*_x64*.msi.sig "$B/myia_${VERSION}_x64.msi.sig"

- uses: actions/upload-artifact@v4
  with: { name: win-msi, path: …myia_*_x64.msi* }
```

- 现文件 `desktop-release.yml:233-240` 的 `bundle/msi/*.msi.sig` glob 删除
  (.sig 在 msi-updater/,`fail_on_unmatched_files` 必红;research §3.2)。
- `fail_on_unmatched_files: true` 原则保留在归聚 job 的上传步(ASCII 改名后
  路径确定性高)。

### 3.3 dispatch 版本修复(F3c)

- `workflow_dispatch: { inputs: { version: { description:…, required: false } } }`。
- 各 job 的 VERSION 取值:`inputs.version || (tag 场景: ref_name 去 v;否则
  回退读 tauri.conf.json 的 version)`——bash 实现:
  `VERSION="${{ github.event.inputs.version || github.ref_name }}"; VERSION="${VERSION#v}"`,
  再以 `jq -r .version src-tauri/tauri.conf.json` 兜底校验 semver 形态
  (不合法即报错,不用分支名硬闯 WiX `convert_version`)。
- Release 上传类步骤(mac 挂资产、归聚 job 的 softprops 两步)统一加
  `if: startsWith(github.ref, 'refs/tags/')`;**归聚 job 本体不门**——dispatch
  也执行 latest.json 生成并以 artifact 交付复核(grill R2-D6b)。dispatch run
  的价值=构建链验证(green check + win-msi/latest-json artifacts 可下载),
  不产生半成品 release——与现有「不产出半成品」守卫哲学一致
  (desktop-release.yml:11-12 注释)。
- 本任务的 CI 验证循环即走 dispatch:`gh workflow run desktop-release.yml
  --ref <任务分支>`(分支上须已含本 workflow 改动)。

### 3.4 权衡记录

- **为什么 windows 失败不挡 mac**:`if: always()` + mac result 门,mac dmg 与
  latest.json(含 mac 条目)照发;windows 失败仅表现为 run 红 + 条目缺席
  (grill Q5)。若未来要求「windows 红则不发版」,删 `if: always()` 即可,单点改。
- **latest.json 时点代价(grill R2-焦点4 补记)**:latest.json 可用时点从
  「mac job 完成」延后到「两 job 均完成」——属更新通道时延非损坏(已装客户端
  只在检查更新时拉取);windows-msi 的 `timeout-minutes: 60` 兜底挂死场景,
  最坏时延有界。
- **为什么发行资产取 updater 版 msi**:与 `.sig` 同源(latest.json 直接可用),
  免去常规/updater 双资产;两版差异仅 webview 安装模式,首装体验等价。
  若 CI 实测目录命名不符预期,以「产物清单」步的日志为准修正 glob——
  本设计不押注未实测的路径,留有日志通道。
- **为什么不改 `bundle.targets` 加 "msi"**:CI 用 `--bundles msi` 覆盖已足够;
  基础 conf 保持 mac-only 使本地 `npx tauri build`(mac 机器)不引入
  Windows bundler 依赖;本地 Windows 出包是未来场景,届时再议。

## 4. 文档设计(F4)

### 4.1 README「下载安装」节增 Windows 小节(要点)

1. 从 Releases 下载 `myia_<版本>_x64.msi`(ASCII 名,以 Releases 实际资产为准;
   前缀随仓内现行口径);
2. SmartScreen:未购买代码签名证书,首次运行弹「Windows 已保护你的电脑」→
   **「更多信息」→「仍要运行」**(与 macOS 右键打开节并列,口径对齐);
3. Windows Defender 误报可能:安装包含未签名 PyInstaller sidecar
   (`myia-core.exe`),SmartScreen/Defender 可能告警;代码开源可审计,
   GitHub Actions 公开构建日志可溯(沿用 README:190-192 的 mac 表述逻辑);
   如遇拦截,「更多信息」仍要运行 + 必要时「允许」;
4. 数据根 `%APPDATA%\MYIA`,首跑种子官方插件,首屏「运行第一个插件」;
5. 升级:设置页「检查更新」(msi passive 静默,UPDATER.md)。

### 4.2 UPDATER.md 更新

- §3(:62):Windows job 描述改为「正式目标;产物 ASCII 名挂 Release;latest.json
  windows-x86_64 条目由归聚 job 自动并入(windows 产物缺席则条目缺席)」——
  手工补条目的操作降级为「归聚失败的应急路径」;
- §6(:113):「Windows 构建级 job 允许失败」旧口径删除,替换为正式目标口径 +
  真机冒烟清单指针;
- workflow 头部注释「已知边界」段(:20-25)同步:Windows 不再 continue-on-error、
  latest.json 单写者为归聚 job、macos x86_64/universal 边界保留不动。

### 4.3 真机冒烟清单(主人侧,如实注记不阻交付)

- [ ] msi 安装(双击/passive)、开始菜单快捷方式、卸载项出现;
- [ ] SmartScreen/Defender 实际拦截形态与文档口径核对;
- [ ] 首跑种子:`%APPDATA%\MYIA\plugins\*.yaml` 五件,五屏数据/空态;
- [ ] **keychain→Windows 凭据管理器(DPAPI)链**(grill R2-D10 补):种子插件
      真用 `keychain:` 引用(plugins/ai-news.yaml:126,131、
      plugins/credentials.yaml:28),keyring→凭据管理器链在本项目 Windows 侧
      从未执行过(三次 run 全死在 uv sync);机制应通(keyring>=25 基础依赖
      pyproject.toml:20、uv.lock pywin32-ctypes 带 win32 标记、PyInstaller
      自带 hook-keyring.py/hook-win32ctypes.core.py 已在 build venv 实读,
      secrets.py 函数体内裸 import keyring 会触发 hook)——冒烟口径:`keychain:`
      凭据经 Windows 凭据管理器可存取;缺席时报 `keychain_backend_unavailable`
      结构化错而非崩溃;
- [ ] sidecar 无黑窗(CREATE_NO_WINDOW 源码已核,research §4.1;真机复核);
- [ ] 设置页检查更新 → msi passive 静默升级 → relaunch;
- [ ] 单实例行为(Windows 无 flock 锁,MSI 重复启动观察项,非阻塞)。

> 口径双源注记:v12-backlog prd:68-71(2026-10-03 grill Q4)记主人「有」
> Windows 真机/VM;2026-10-04 任务授权口径「未知」。按新口径:冒烟=主人侧
> 清单,交付=CI 绿 + 文档;若主人确认真机在位,按 backlog 原目标补全
> 「cwd 无关路径解析 + 首跑种子 + 五屏」macOS 同款验收(事后可翻案)。

## 5. 兼容性与回滚

- **macOS 主线**:零行为变化(dmg 资产仍由 mac job 挂;latest.json 内容结构
  同源,仅写者移位);AC3/AC6 用 mac job 绿 + 本机 build-sidecar.sh 冒烟兜底。
- **Linux**:pyproject marker 在 linux 恒假(与 windows 同路径),核心依赖不变;
  ci.yml(ubuntu)全量 pytest 即回归门。
- **uv.lock**:marker 变更属向后兼容锁演化;若 CI `--frozen` 与新锁不一致,
  uv 会报锁过期——重锁与 pyproject 改动必须同一提交落地。
- **回滚**:全部改动集中在 7 个文件,`git revert` 单批可退;workflow 回滚即
  回到「windows 允许失败」旧态,mac 发布链两态等价。

## 6. 风险表

| 风险 | 概率 | 处置 |
|---|---|---|
| msi/msi-updater 目录或命名与源码推断不符 | 中 | 「产物清单」步日志即真相;glob 按实测一改即可(fail_on_unmatched_files 诚实门) |
| 重锁 diff 超预期(镜像 env 失效/解析漂移) | 低 | `git diff uv.lock` 人工核;必要时锁 ocrmac 现版本不动仅加 marker |
| Windows runner 上 rapidocr/onnxruntime 收编体积或路径问题 | 低 | collect_all 已含模型数据文件;mac 同款路径已两次生产实证;CI 日志可溯 |
| WiX 对非 ASCII ProductName(世事)的模板兼容 | 低-中 | mainBinaryName 已 ASCII(MYIA),exe/shortcut 名不受累;若 candle/light 报编码错,处置=release conf 片按平台覆写 productName 为 ASCII(归聚 job 已有 conf 注入机制,单点改) |
| dispatch 验证轮次多(runner 排队) | 中 | 每轮修多点再 dispatch;不上 tag 直到 dispatch 绿 |

## 7. 与探查档的映射

R1→D1/Q1;R2→F1/D2;R3a→F2/D4;R3b→F3/D5;R4→零触碰边界;R5→F4/D8;
§3.3→F3c/D9;§6→D10/Q7。全部证据出处见 research 对应节。
