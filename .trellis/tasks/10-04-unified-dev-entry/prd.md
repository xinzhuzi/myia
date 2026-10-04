# 统一开发入口:多语言工具面(uv/npm×2/cargo/docker)收口,工具版本仓内钉版

## Goal

仓库 4 套语言栈 5 个工具面无统一入口(uv/npm 双根/cargo/docker/bash 脚本),工具版本只钉在 CI yml(node 22 ×3 处,python >=3.11 浮动,rust stable 浮动),desktop 构建入口是 bash 脚本与 Windows 产品面错位。实测证据矩阵已入档;推荐 justfile 单一门面(各栈原生工具不动),版本钉版方案留决策点。

- **诉求来源**:主人 2026-10-04 晚,「插件代码/其他源码要有一个整体的管理工具吧?好多个语言有多个管理工具,感觉非常乱,解决一下」。
- **定性**:开发者体验/工程治理任务,不动产品功能。先探查复证、后统一入口,不推翻各语言原生工具。

## Requirements

### 1. 现状证据矩阵(2026-10-04 全量探查)

**语言栈 × 工具面(5 面、4 套包管理):**

| 栈 | 位置 | 包管理/锁 | 构建/测试入口 | 版本钉版现状 |
| --- | --- | --- | --- | --- |
| Python 主包+分类器 | 根 `pyproject.toml`(uv workspace,成员 `myssia-classifier/`) | uv + uv.lock(单锁覆盖双包 ✓) | `uv run --no-sync python -m pytest`、`uvx ruff@0.16.10`、mypy | `requires-python >=3.11`(下限浮动) |
| TS/React UI | `desktop/ui-src/` | npm(package-lock) | vite / vitest / tsc(4 条 scripts) | 无 engines 字段 |
| Rust Tauri 壳 | `desktop/src-tauri/` | cargo(Cargo.lock) | `cargo check --locked` / tauri build | rust stable 浮动 |
| 桌面装配 | `desktop/`(第二个 npm 根) | npm(`@tauri-apps/cli`) | `npm run sidecar` → **bash** `build-sidecar.sh`(内部再开独立 venv 跑 PyInstaller) | 无 |
| Docker | 根 `Dockerfile` + `docker/` | — | docker build / compose | 无 |
| 插件 | `plugins/`(品类 yaml + `myssia-*` adapter.py + 1 个 git 子模块 vendor/Photon) | **无独立清单(吃主 venv,刻意设计)** | — | — |

**乱点清单(与主人「感觉非常乱」对应):**

1. **无统一入口**:全栈开发要会 uv + npm(两个根)+ cargo + bash + docker 五套;同一件事命令式样各异(`uv run --no-sync python -m pytest` / `npm --prefix ui-src run build` / `cargo check --locked` / `bash build-sidecar.sh`)。没有一处 `--list` 能看到全部可用动作。
2. **版本钉版散落**:node 22 写死在 CI yml **3 处**(ci.yml:37、desktop-release.yml:77,203);Python/rust 浮动;新人本机装什么版本全靠猜,CI 与本机可静默漂移。
3. **desktop 双 npm 根**:`desktop/package.json`(tauri CLI)与 `desktop/ui-src/package.json`(UI 31 依赖)各一份 lock,`npm --prefix` 跨根调用;仓库根还有一个**空 node_modules 残留**。
4. **Windows 错位**:产品已发 Windows MSI,但 desktop 装配入口是 bash 脚本、CONTRIBUTING 全 Unix 命令——Windows 开发者无对齐路径。
5. **文档零散**:CONTRIBUTING.md 只覆盖 Python 面(18-19 行);desktop 构建知识活在脚本注释和 CI yml 里;docker 在 docker/README;无一处「从零到全栈门禁绿」的单页路径。
6. **根目录杂物**(次要,但加重「乱」感):`myia.db` + `myssia.db` 双库并存(改名残留,均已 gitignore)、`channel_*.json`、`credhunter-keystore.json`(gitignored)、`plugins/stocks.yaml.bak`(gitignored)。

**不是乱、不要动的(防过度工程):**

- Python 面已是 workspace 单锁,干净;**不给插件加 per-plugin 依赖清单**(plugin.yaml + adapter.py 吃主 venv 是刻意轻装设计);Rust/TS 目录分离是 Tauri 结构固有;各语言原生工具(uv/npm/cargo)**保留**,本任务只做统一门面与钉版,不替换不包抄。

### 2. 方案决议(2026-10-05 grill,主人按推荐全批 Q4-Q8)

| 决议点 | 定案 |
| --- | --- |
| 门面工具(Q4) | **just**:仓库根一个 `justfile` 收口全部 recipe,不替换各语言原生工具 |
| 版本钉版(Q5) | **原生文件三件套,零新工具**:`.python-version`(uv 原生读)+ `rust-toolchain.toml`(rustup 原生读)+ 两个 package.json 加 `engines.node` 且 CI 三处改 `node-version-file` |
| desktop 双 npm 根(Q6) | **保留双根**(Tauri 常见布局),只在 justfile 收口;不做 workspaces 合并(churn 大于收益) |
| Windows 对齐(Q7) | **文档化**:CONTRIBUTING 注明本地开发需 Git Bash(装 git 自带)或 WSL;justfile recipes 写跨平台无 bash-ism。不写 .ps1(事实依据:Windows CI 本就用 Git Bash 跑 build-sidecar.sh) |
| 根目录杂物(Q8) | **选 (b)**:删空根 node_modules + `plugins/stocks.yaml.bak`(均 gitignored 残留);**db/keystore/channel_*.json 全部保留不动**(运行产物、代码在用、已 ignore);CONTRIBUTING 增「仓库根运行产物说明」段治「看着乱」的根源 |

**配套设计默认**(grill 轮内已定,详见 design.md):

- `just check` 口径 = 对齐 CI 现状:ruff + tsc + cargo check(mypy 在 CI/配置/文档中均不存在,不进 check;根 `.mypy_cache` 为历史残渣,入清理清单可选删)。
- **CI 不切换到 just**:justfile 只服务本地门面,CI 保持原命令(避免给 CI 加新工具依赖);后续若想统一再翻案。
- 排期:**本档在 10-04-yaml-editor-no-scroll(P1)之后执行**。

### 3. 已知约束

- 「严禁删本机配置」:根目录 db/keystore 等清理项**逐条经主人确认**后才动,默认保留。
- 模仿纪律:justfile 写法先参考 2-3 个高星 polyglot 仓(候选:astral-sh?/tauri 生态样板)再落笔(执行期做)。
- CI 已绿是底线:justfile 是纯门面,**不得改变任何既有命令语义**;切换 CI 调用方式属可选子项,单独决策。

## Acceptance Criteria

- [x] **一门面**:`just --list` 展示全栈动作;`just test` 一条命令跑齐 pytest + vitest;`just check` 跑齐 ruff + tsc + cargo check(对齐 CI 口径);退出码如实透传(绿/红不改口)。
- [ ] **一条路走通桌面构建**:`just build-desktop` 从 sidecar 打包到 tauri build 串到底(内部调既有 build-sidecar.sh 与 npm scripts,不复制逻辑)。
- [x] **钉版单处、原生生效**:仓内新增 `.python-version`(3.12)、`rust-toolchain.toml`(stable)、两个 package.json `engines.node`(22);CI 三处 `node-version: "22"`(ci.yml:37、desktop-release.yml:77,203)收敛为 `node-version-file: desktop/package.json`;本机 `uv run python -V` 报 3.12 验证。
- [x] **Windows 路径**:justfile recipes 无 bash-ism;CONTRIBUTING 注明 Git Bash/WSL 即可本地开发(不写 .ps1)。
- [x] **新人单页**:CONTRIBUTING.md 增「一键环境」章节(install just → just setup → just test / check / build-desktop);另增「仓库根运行产物说明」段(myia.db/myssia.db 双库由来与数据根留 myia 纪律、channel_*.json、credhunter-keystore.json、*.bak)。
- [x] **清理落地**:删空根 node_modules 与 `plugins/stocks.yaml.bak`(gitignored 残留);可选顺手删历史残渣 `.mypy_cache`;db/keystore/channel_*.json 一律不动。
- [ ] **门禁**:`just test` / `just check` 全绿且与直接跑各栈命令结果一致;CI 三 workflow 照常绿(CI 未引入 just 依赖)。

## Notes

- 规模预估:约 0.5-1 天(justfile ~100 行 + 三件套钉版 + CI 三行收敛 + CONTRIBUTING 两段 + 清理);无 Windows 脚本原生化(如需另立档)。
- 2026-10-05 grill 决议已全批(Q4-Q8 按推荐),三件套齐(prd + design.md + implement.md),**start 前置条件就绪**;排期在 10-04-yaml-editor-no-scroll 之后。
