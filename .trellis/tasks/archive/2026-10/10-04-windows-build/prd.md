# Windows 产物化:CI 构建与发行文档

## Goal

把 desktop-release.yml 的 Windows 目标从「构建级验证、允许失败(三次 run 全红)」升级为
**正式交付目标**:CI Windows job 绿、msi 产物以 ASCII 名挂上 Release、Windows 安装与
SmartScreen 放行文档就位。探查→grill→实现全流程;真机冒烟=主人侧如实注记(既有开放
问题的既定答案,不阻交付)。

> 事实修正(开工假设纠偏,见 research §0/R1):「desktop-release.yml 是 mac-only」
> 已过时——windows-msi job 自 v1.1(40a666a)就在,真实命题是**红→绿 + 产物化 + 文档**。

## Requirements

### F1 sidecar Windows 依赖装配(根因修复)

vision extra 的 `ocrmac` 无平台标记,`uv sync --extra vision` 在 Windows 拉
pyobjc 链(macOS 专属 wheel)装配必炸(生产 run 37117015528 实锤)。修复后 Windows
runner 上依赖装配成功,macOS/Linux 解析不受影响,uv.lock 重锁保持镜像 URL 体系。

### F2 msi 打包配置补全

`bundle.icon` 补 `icons/icon.ico`(文件已在,tauri-bundler 源码级硬前提);
`myia-core.spec` 给 `collect_all('ocrmac')` 加平台门(卫生性,见 grill 修正③)。

### F3 desktop-release.yml Windows 产物化

- windows-msi job 转正式目标(移除 continue-on-error),失败可见但不牵连 macOS
  发布与 mac 更新通道;
- 产物上传前改 ASCII 名(对齐 bfb60a0 先例:GitHub 剥非 ASCII 资产名),上传 glob
  修正为 bundler 实际输出目录(msi/ 与 msi-updater/),`fail_on_unmatched_files`
  继续作诚实门;
- workflow_dispatch 修版本来源(分支名不是合法 semver,dispatch 验证通道当前是坏的);
- latest.json 改归聚 job 单一写者:mac 条目恒在,windows 条目按产物存在与否条件并入。

### F4 安装/SmartScreen 文档

README「下载安装」节增 Windows 小节(下载 msi → SmartScreen「更多信息→仍要运行」
→ 安装 → 数据根 `%APPDATA%\MYIA` → 首跑种子);Windows Defender 对未签名
PyInstaller sidecar 的误报可能性如实注记;UPDATER.md 第三节(手工补条目→自动化)
与第六节(旧口径)同步更新;真机冒烟清单留主人。

## Constraints

- **零 GUI 零前台**:本任务全程不碰 GUI 验证(无 Windows 主机,darwin 工作机);
  CI 绿是唯一可执行验证口径,真机交互全部归主人清单。
- **共享热点文件纪律**:desktop/entry.py、src/myia/schema.py、tests/test_desktop_sidecar_protocol.py、
  desktop/ui-src types.ts **零触碰**(探查已证 Windows 适配就绪,research §4);
  pyproject.toml/uv.lock 只做 ocrmac 标记最小侵入(外来未提交改动叠加勿覆写)。
- **并行改名协调(2026-10-04 实况)**:本档起草期间树上正飞大规模 shishi→myia
  改名扫荡(pyproject 包名、workflow 资产前缀 shishi_*→myia_*、README、目录
  myia-classifier 等);实施以扫荡落地后的树为基线,ASCII 资产前缀对齐 myia,
  本档行号以 71e00db 基线+扫荡后现状二次核对为准。
- **签名红线**:不购买代码签名证书(主人侧成本决策);SmartScreen 文档化放行;
  updater 签名密钥体系(UPDATER.md)不動。
- 全量门禁由脚本统一;本任务自跑定向检查(spec 语法、yml 解析、mac 侧构建不回归)。

## Acceptance Criteria

- [x] AC1 依赖:pyproject vision extra 的 ocrmac 带 `sys_platform == 'darwin'` 标记;
      重锁后 uv.lock 的 ocrmac 条目带 marker 且 URL 体系不变(仍 tsinghua);
      `uv sync --frozen --no-dev --extra vision` 在 windows runner 装配成功(CI 日志为准)。
      → 终检冒烟(2026-10-04)**manual**:静态面终检复核实读全过——pyproject.toml:50
      marker、uv.lock:1979/2003 marker、ocrmac sdist+wheel 两条 URL 均 tsinghua;
      windows runner 装配=CI 日志为准,未跑(推 origin 首跑)
      → 首跑实况(2026-10-04,run 37178701163):windows uv sync **失败**,
      根因=外来改名反转漏改子包名(workspace member 不一致),非 ocrmac
      marker——错误面与 vision extra 无关;不勾,详见验收记录 CI 首跑节
      → 绿跑回填(2026-10-04,run 37186006759):pyproject.toml:50 marker 实读
      在位;uv.lock:1979/2003 marker、ocrmac sdist+wheel URL 均 tsinghua
      (2243/2245);windows-msi job「构建 sidecar(x86_64-pc-windows-msvc)」步
      success(build-sidecar.sh 在 runner 建 desktop/.venv-build 并跑通
      PyInstaller,msi 随后产出)=装配成功,CI 日志为准;勾
- [x] AC2 CI 绿:desktop-release.yml 的 windows-msi job conclusion=success
      (workflow_dispatch 验证 run 即可,tag 发布为最终态);run 日志含 bundle 目录
      清单步(产物路径可溯)。
      → 终检冒烟 **manual**:静态断言 34 PASS + actionlint clean(终检会话复跑
      exit 0);真 run conclusion 待推 origin 首跑,未跑
      → 首跑实况(2026-10-04,run 37178701163):windows-msi conclusion=
      **failure**(死于 sidecar 装配,外来根因);不勾,详见验收记录 CI 首跑节
      → 绿跑回填(2026-10-04,run 37186006759):windows-msi job conclusion=
      **success**(job 111387927642);「产物清单(诊断)」步在且绿,日志实列
      bundle/msi 产物路径;勾
- [ ] AC3 打包配置:tauri.conf.json `bundle.icon` 含 `icons/icon.ico`;mac 主线
      不回归(macos-dmg job 仍绿,`--bundles app,dmg` 链照常)。
      → 终检冒烟 **manual**:配置面终检复核实读过(bundle.icon 三元组含
      icons/icon.ico,文件 84,679 B);macos-dmg 仍绿=CI 结果,未跑
- [x] AC4 产物:Release(或验证 run 的 artifacts)含 ASCII 名 msi + `.msi.sig`
      (`myia_<版本>_x64*.msi` 形态——ASCII 前缀随仓内现行口径,2026-10-04 并行
      改名扫荡已把 mac 资产前缀 shishi→myia,windows 对齐);latest.json 由归聚
      job 单一产出(dispatch run 中以 `latest-json` artifact 形态可复核),
      darwin-aarch64 条目恒在,windows-x86_64 条目在 windows 产物在时并入,
      URL 指 ASCII 资产名。
      → 终检冒烟 **manual**:静态+dry 过(workflow 断言+dry D2/D4 30 PASS);
      Release/artifacts 实际=CI 首跑(+tag),未跑
      → 首跑实况(2026-10-04,run 37178701163):artifacts **0 件**(mac/win
      双死于 sidecar 装配,未到产物步);不勾,详见验收记录 CI 首跑节
      → 绿跑回填(2026-10-04,run 37186006759):win-msi artifact(127,699,711 B)
      内含 ASCII 名 myssia_0.0.1_x64.msi + myssia_0.0.1_x64.msi.sig(上传步
      日志实列双路径;前缀 myssia=productName 现行口径,与本档字面 myia_ 之别
      以自注「ASCII 前缀随仓内现行口径」为准);latest-json artifact 双平台
      条目齐、URL 指 ASCII 资产名;dispatch run 挂 Release 步 skipped=tag 门
      设计内,以 artifacts 通道验;勾
- [x] AC5 文档:README Windows 安装小节 + SmartScreen/Defender 注记落盘;
      UPDATER.md 第三节/第六节更新为自动化口径;真机冒烟清单(安装/放行/首跑种子/
      keychain→凭据管理器 DPAPI 链/五屏/updater passive/单实例观察项,七项)
      写入档,标注主人侧。
      → 终检冒烟 passed:README:196-213 Windows(x64)小节 + UPDATER §3/§6 自动化
      口径 + 本档七项冒烟清单,终检会话逐处实读在位
- [x] AC6 回归:全量 pytest 零新红;myia-core.spec 平台门后 mac 侧
      `bash build-sidecar.sh aarch64-apple-darwin` 成功且产物大小同量级;
      dispatch 于分支时版本回退合法(不再以分支名当 semver)。
      → 终检冒烟 passed:全量 pytest 3495 passed/0 failed;spec 平台门终检实读
      (myia-core.spec:17-19 darwin 门)+ py_compile ok;mac 构基本会话 exit 0/
      124,059,712B,终检核磁盘产物在位 124,120,784B;dry D1 四场景版本回退全 PASS
- [x] AC7 证据:CI 绿 run URL 与产物清单回填本档「验收记录」;归档留主人。
      → 终检冒烟 **manual**:run URL 回填前提=CI 真跑(dispatch 循环),未跑;
      静态/dry 证据已入 evidence/,CI 首跑后由主人/后续会话回填
      → 首跑实况(2026-10-04):两 run URL+失败根因已回填验收记录 CI 首跑节,
      但均为红 run(无「CI 绿」证据);AC7 判据未满,不勾
      → 绿跑回填(2026-10-04,工作流 dwfrun-6fb40055):绿 run URL+产物清单
      已回填验收记录「发布验证回填」节,归档状态不动;勾(终审留主人)

## 待拍板(全带推荐;2026-10-04 主人 /workflow 授权「七连全按推荐」口径,已按推荐定稿见下节)

- **D1 Windows job 定位**:推荐**转正式目标,移除 continue-on-error**——这正是本任务
  目的;配合 D6 的 `if: always()` 归聚,mac 发布与更新通道不受 windows 红牵连。
  (替代:维持允许失败——与任务目标自相矛盾,弃。)
- **D2 依赖修复路径**:推荐 **pyproject 平台标记 + 重锁**(`ocrmac>=1.0; sys_platform == 'darwin'`),
  治本且三平台一致;(替代:CI `--no-install-package` 排除链拦不住 pyobjc 传递依赖、
  60 条不可维护,实测排除;单独 windows requirements 文件=双源漂移,弃。)
- **D3 spec 平台门**:推荐**加**(`sys.platform == 'darwin'` 门住 ocrmac 三行),
  意图明确+日志干净;注意这是卫生项不是必需项(grill 修正③)。
- **D4 图标**:推荐 `bundle.icon` **补 `icons/icon.ico`**(源码铁证:无 .ico 则 WiX
  必炸 `Couldn't find a .ico icon`;文件已存在,mac 构建无感)。
- **D5 产物命名与上传**:推荐**上传前改 ASCII 名**(`myia_<版本>_x64*.msi`/`.sig`,
  前缀随改名扫荡后现行口径),glob 按 bundler 实际目录(msi/ + msi-updater/);
  以 CI 日志实测为准修正,保留目录清单诊断步。
- **D6 latest.json 写者**:推荐**归聚 job 单一写者**(`needs: [macos-dmg, windows-msi]`
  + `if: always() && needs.macos-dmg.result == 'success'`;mac 条目恒在,
  windows 条目按产物存在与否)。(替代:维持手工补——主人已两发两漏,弃;
  windows job 自写——双写者竞态,弃。)
- **D7 签名/SmartScreen**:推荐**v1 不购证书,文档化放行**(「更多信息→仍要运行」
  + Defender 误报白名单注记);EV/OV 证书入池留主人成本决策。
- **D8 文档落点**:推荐 **README 安装节 Windows 小节 + UPDATER.md 两节更新**,
  docs/zh|en 不动(getting-started 无桌面节,桌面安装入口唯 README)。
- **D9 版本底座**:推荐 windows-latest + Python 3.11 + Node 22 + Rust stable,
  与 mac job 逐项对齐,不引入新矩阵(arm64 windows 无场景)。
- **D10 真机冒烟口径**:推荐**按 2026-10-04 授权口径**(真机有无未知,冒烟清单留
  主人,不阻交付);v12-backlog grill Q4(2026-10-03)曾答「有」——两源并存如实
  注记(research §6),以更新口径为准。

## Grill 决议(2026-10-04,自诘七问全按推荐定稿;主人授权口径「七连全按推荐,事后可翻案」)

- **Q1 开工假设纠偏**:ask 称「mac-only 现状」,实探 windows job 已在且 3/3 红
  → 按**实探口径**定稿:任务是红→绿+产物化,不是从零加目标。(原文「desktop-release.yml
  扩 Windows 目标」→ 修正为「Windows 目标转正式交付」。)
- **Q2 D2 替代路径可行性**:`--no-install-package` 实测存在但拦不住传递依赖,
  60 条 pyobjc 排除链不可维护 → 定 marker 方案。
- **Q3 spec 行为初判修正**:初判「ocrmac 缺席 spec 会炸」→ 本机实测(PyInstaller
  6.22.3)`collect_all` 对缺失包**仅警告不炸**;D3 从「必须」降级为「卫生性推荐」,
  AC6 相应只锁 mac 侧构建不回归。
- **Q4 latest.json 双写者竞态**:mac/windows 并行 job 各写 latest.json 会互覆 →
  归聚 job 单一写者(D6),mac 主线上传自身资产的行为不变(已两次生产实证)。
- **Q5 windows 红的爆炸半径**:转正式后 windows 失败会让 run 变红 → 归聚 job
  `if: always()` + mac result 门,保证 mac dmg/latest.json 照发,windows 缺席
  仅表现为条目缺失+run 红(可见但不伤 mac 用户)。
- **Q6 共享热点文件触碰面**:探查证 entry.py/main.rs Windows 分支已就绪(源码级),
  本任务对四个共享热点文件**零触碰**;pyproject/uv.lock 是最小侵入且叠加外来改动。
- **Q7 冒烟口径双源冲突**:backlog(10-03)「有真机」vs 授权(10-04)「未知」→
  如实注记两源、按新口径交付,冒烟清单独立成节不阻 AC。

### 质询回执(2026-10-04 第二轮,D1-D10+四焦点;ok×9 / change×2 / missing×1,修正全部落地)

- **D6 change→已修三处**:(a) release-finalize 补 `runs-on: ubuntu-latest`(jq
  预装);(b) 归聚 job 本体不再整体 tag 门——dispatch 也执行 latest.json
  生成逻辑并经 `latest-json` artifact 供人验,仅 softprops 上传两步保留 tag 门
  (原设计恰使最易错件的首跑=主人推 tag,修正);(c) windows-msi 加
  `timeout-minutes: 60`(挂死不得无限期拖住 latest.json)。
- **D10 change→冒烟清单补第七项**:keychain→Windows 凭据管理器(DPAPI)链——
  种子插件真用 `keychain:` 引用(plugins/ai-news.yaml:126,131、
  plugins/credentials.yaml:28,本会话复核在案),该链在 Windows 侧从未执行过;
  支持链证据(keyring>=25 / pywin32-ctypes 标记 / PyInstaller hook 两件在
  build venv 实读)与冒烟口径(`keychain_backend_unavailable` 结构化错而非
  崩溃)已写进 design §4.3。
- **焦点1 missing→已补**:implement 3.6 增 actionlint(1.7.12 在装,基线文件
  本会话实测 clean)——覆盖 run 块 shellcheck + needs 引用 + 表达式错误;
  跨平台解析预检本地不可做(uv 0.7.6 无 --python-platform,质询实测)仍靠
  CI dispatch,口径不变。
- **焦点4→并入 D6**:latest.json 时点从「mac job 完成」延后到「两 job 均完成」
  的时延代价在 design §3.4 明写(更新通道时延非损坏,timeout 兜底有界)。

## 真机冒烟清单(主人侧;如实注记,不阻交付)

> 口径双源注记:v12-backlog prd:68-71(2026-10-03 grill Q4)记主人「有」
> Windows 真机/VM;2026-10-04 任务授权口径「未知」。按新口径:冒烟=主人侧
> 清单,交付=CI 绿 + 文档;若主人确认真机在位,按 backlog 原目标补全
> 「cwd 无关路径解析 + 首跑种子 + 五屏」macOS 同款验收(事后可翻案)。

- [ ] msi 安装(双击/passive)、开始菜单快捷方式、卸载项出现;
- [ ] SmartScreen/Defender 实际拦截形态与 README 安装节文档口径核对;
- [ ] 首跑种子:`%APPDATA%\MYIA\plugins\*.yaml` 五件,五屏数据/空态;
- [ ] **keychain→Windows 凭据管理器(DPAPI)链**(grill R2-D10 补):种子插件
      真用 `keychain:` 引用(plugins/ai-news.yaml:126,131、
      plugins/credentials.yaml:28),该链在 Windows 侧从未执行过(三次 run 全死
      在 uv sync);机制应通(keyring>=25 基础依赖、uv.lock pywin32-ctypes 带
      win32 标记、PyInstaller hook-keyring/hook-win32ctypes 已在 build venv);
      冒烟口径:`keychain:` 凭据经 Windows 凭据管理器可存取,缺席时报
      `keychain_backend_unavailable` 结构化错而非崩溃;
- [ ] sidecar 无黑窗(tauri-plugin-shell Windows 默认 CREATE_NO_WINDOW,
      源码已核,research §4.1;真机复核);
- [ ] 设置页检查更新 → msi passive 静默升级 → relaunch;
- [ ] 单实例行为(Windows 无 flock 锁,MSI 重复启动观察项,非阻塞)。

## 验收记录(实施会话 2026-10-04 回填;dispatch/CI 实跑未执行)

**已落地**:F1(pyproject vision extra `ocrmac>=1.0; sys_platform == 'darwin'`
标记 + 镜像 env 重锁)、F2(spec ocrmac 三行 darwin 平台门 + tauri.conf
`bundle.icon` 补 `icons/icon.ico`)、F3(desktop-release.yml 三 job 重构:
windows-msi 转正式 + release-finalize 归聚单写者 + dispatch 版本入参/兜底 +
Windows 产物 ASCII 改名 `myia_<版本>_x64.msi`/`.sig`)、F4(README Windows
安装小节 + SmartScreen/Defender 注记;UPDATER.md §3/§6 自动化口径;本冒烟清单)。

**本地定向检查(实施会话实跑)**:

| 检查 | 命令 | 结果 |
|---|---|---|
| 锁自洽(darwin) | `UV_DEFAULT_INDEX=…tsinghua… uv sync --frozen --no-dev --extra vision --dry-run` | exit 0 |
| ocrmac 标记生效 | `uv export --frozen --no-dev --extra vision \| grep ocrmac` | `ocrmac==1.0.1 ; sys_platform == 'darwin'` |
| 重锁 URL 体系 | `git diff uv.lock \| grep url` | 零非 tsinghua 行;ocrmac 条目字节不变 |
| conf/tauri JSON | `python3 -c "import json;json.load(open('desktop/src-tauri/tauri.conf.json'))"` | ok |
| spec 语法 | `python3 -m py_compile desktop/myia-core.spec` | ok |
| mac sidecar 不回归 | `bash build-sidecar.sh aarch64-apple-darwin` | exit 0,产物 124,059,712 B |
| workflow 结构 | `python3 -c "import yaml;…print(sorted(d['jobs']))"` | `['macos-dmg','release-finalize','windows-msi']` |
| actionlint | `actionlint .github/workflows/desktop-release.yml` | exit 0 clean |
| 版本解析 dry | 四场景 bash 演练(tag/分支无参/分支带参/预发布) | 全部符合预期 |

**未跑(如实,实施会话口径)**:dispatch 验证循环(`gh workflow run
desktop-release.yml`)——本会话口径不真跑 CI;AC1 的 windows runner 装配、
AC2/AC4 的 run 绿与 artifacts、AC7 的 run URL 回填,待分支推送后由主人/后续
会话执行(判据见 implement 阶段 4)。全量 pytest 归脚本统一门禁。

### CI 首跑实跑记录(2026-10-04 推送后,CI 收口会话回填;HEAD=1c46a27)

| run | URL | 终态 |
|---|---|---|
| ci.yml(push 触发) | https://github.com/xinzhuzi/myia/actions/runs/37178669780 | **failure**:test / docker-build / ruff 三红;ui-test、rust-check 绿 |
| desktop-release.yml(workflow_dispatch @ main) | https://github.com/xinzhuzi/myia/actions/runs/37178701163 | **failure**:macos-dmg 与 windows-msi 双双死于「构建 sidecar」步(29s / 1m15s);release-finalize skipped(macos-dmg result 门);**artifacts 0 件**(无 win-msi/mac-updater/latest-json) |

- **四红同源,均非本任务域文件**:HEAD `1c46a27` 上
  `myia-classifier/pyproject.toml` 的包名仍为 `shishi-classifier`
  (`0a085cc` 改名反转把目录改回 myia-classifier 但漏改子包名),与根
  pyproject `tool.uv.workspace/sources` 及 uv.lock 的 `myia-classifier`
  不一致——test job `uv sync` 报「`myia-classifier` references a workspace
  in `tool.uv.sources` … but is not a workspace member」;docker 与双平台
  sidecar 的 `--frozen` 同报「Missing workspace member `shishi-classifier`」
  (三个 job 日志实抓,行号见 run)。
- **另:ruff F821** `src/myia/cli.py:3854`(undefined name `_cmd_cron`)——
  `f759c87`(本批 proxy-pool 提交)夹带了并行 hermes-cron 线在途的
  handlers 引用行;定义 `def _cmd_cron` 在并行会话**未提交**工作树
  (src/myia/cli.py:1813,+815 行 cron 族),尚未随任何提交入库。
- **处置(按「外来(并行线)→如实记录不修」纪律)**:两族失败的修复文件
  (`myia-classifier/pyproject.toml`、`src/myia/cli.py`、`tests/test_cli.py`)
  均带并行会话未提交改动——不碰、不代提交、不 force push。本任务域文件
  (desktop-release.yml / build-sidecar.sh)在两 run 中行为符合设计:守卫步
  过、uv/node/rust 装配过、失败点全在上游依赖装配(仓库态),未到 Tauri
  打包段——**msi 命名 / WiX 对中文名 / 路径大小写三雷区(4.3)未触及**。
- **AC 状态(如实,不勾)**:AC1 windows runner uv sync=失败(外来根因,
  非 ocrmac marker——错误面为 workspace member,与 vision extra 无关);
  AC2 windows-msi conclusion=failure;AC4 artifacts 0 件;AC7 无绿 run URL。
  待并行线修复(子包名回 myia-classifier + cron 定义入库)推 main 后重新
      dispatch 验证(判据仍按 implement 4.2),届时由后续会话/主人回标本节。

### 发布验证回填(2026-10-04,b0044c5 绿跑;工作流 dwfrun-6fb40055 会话)

并行线修复(windows-msi WiX 非 ASCII 产物名 + bundle glob 两修)推 main 后,
b0044c5 的 Desktop Release run 全绿——本节由发布验证回填会话据 gh CLI 实查回填:

| 项 | 实查结论(gh run list/view/api、gh run download、git merge-base) |
|---|---|
| 绿 run | https://github.com/xinzhuzi/myia/actions/runs/37186006759 — headSha b0044c5,createdAt 2026-10-04T07:30:45Z,conclusion **success** |
| windows-msi job | **success**(job 111387927642,07:30:49Z–07:40:50Z):构建 sidecar(x86_64-pc-windows-msvc)/ Tauri 构建(msi;WiX light 产出 myssia_0.0.1_x64_en-US.msi 121.98 MiB)/ 产物清单(诊断)/ 产物改 ASCII 名 / 上传 win-msi 全绿 |
| macos-dmg / 归聚 job | 双 **success**(111387927624 / 111389484702);latest.json 生成+artifact 上传绿,挂 Release 两步 skipped=dispatch run tag 门(设计内) |
| run artifacts | win-msi 127,699,711 B(内含 myssia_0.0.1_x64.msi + myssia_0.0.1_x64.msi.sig,上传步日志实列双路径)、latest-json 913 B、mac-updater 485 B |
| latest.json 复核 | darwin-aarch64 恒在 + windows-x86_64 并入;双 URL 指 ASCII 资产名(myssia.app.tar.gz / myssia_0.0.1_x64.msi);pub_date 2026-10-04T07:41:01Z |
| 血统 | `git fetch origin` 后 `git merge-base --is-ancestor b0044c5 origin/main` exit 0——绿 run 跑在被认领提交上 |
| Release v0.0.1 现存资产 | latest.json、shishi.app.tar.gz、shishi.app.tar.gz.sig、shishi_0.0.1_aarch64.dmg——**三件 shishi_* 旧名残留**(前两次 mac 发布所挂,不动留主人);且新产出 latest.json 的 darwin URL 指新名 myssia.app.tar.gz,与现存旧名资产暂不对应,tag 重跑后由新资产接管,旧名清理留主人 |

AC1/AC2/AC4/AC7 据此回标(逐条证据见各 AC 追加行);AC3/AC5/AC6 维持原状态,
不在本次回填域。

## Notes

- 实施顺序建议:F1 依赖(解锁一切)→ F2 配置 → F3 workflow → dispatch 验证循环 →
  F4 文档 → 全量定向检查 → 主人 tag 发布为最终态。
- 验证通道:不推 tag,走 `gh workflow run desktop-release.yml --ref <任务分支>`
  (需 §3.3 的 dispatch 版本修复先行);全量门禁由脚本统一。
- 探查证据全量见 `research/windows-build-current-state.md`(本档所有 CI/源码/锁
  文件结论的出处,含可复现命令)。

## 终局补记(2026-10-04,归档后 CI 验证收口)

> 归档时 CI 首跑未绿;本补记为纯增量事实,原文勾选框保持归档时状态。

- **run https://github.com/xinzhuzi/myia/actions/runs/37186006759(head=b0044c5)三作业全绿**:macOS dmg ✓ / **windows-msi ✓(正式交付目标首次 CI 出绿,AC2 满足)** / 归聚 latest.json ✓
- 产物:win-msi artifact 121.8MiB(myssia_0.0.1_x64.msi+.sig ASCII 名,AC4 满足·dispatch artifacts 口径)+ latest-json + mac-updater;AC1 依赖面随 job 绿实证(windows runner uv sync 装配过);AC7 本补记即回填
- 两轮域内修复链:①0378ed3 windows 作业 release conf 注入 productName=myssia(WiX light.exe 产不出非 ASCII 产物名,预判雷区#2 实锤)②b0044c5 产物改名步 glob msi-updater/→msi/(Tauri2 布局,updater msi+.sig 并排 bundle/msi)
- 真机安装冒烟七项仍留主人(档内清单);Release 页资产挂载属 tag 流
- 溯源:本节事实经工作流 dwfrun-6fb40055 发布验证回填(归档状态不动、终勾留主人);shishi_* 旧名残留资产已如实列出,处置留主人。
