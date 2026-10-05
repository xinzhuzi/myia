# 技术设计:统一开发入口(justfile 门面 + 原生钉版三件套)

> 决议见 prd.md §2(just / 三件套 / 保留双根 / 文档化 Windows / 清理 b)。
> 原则:**纯门面**——不改任何既有命令语义,不替换各语言原生工具,CI 不引入 just 依赖。

## 1. justfile 设计(仓库根,约 100 行)

写法参考:先读 2-3 个高星 polyglot 仓的 justfile(执行期做,候选 helix-editor/helix、astral 生态仓),借结构不抄码。

**Recipe 清单**(初稿,执行期可按实测微调):

| recipe | 内部命令 | 说明 |
| --- | --- | --- |
| `setup` | `uv sync --all-extras` + `npm --prefix desktop ci` + `npm --prefix desktop/ui-src ci` + rustup 提示 | 一键环境;**本机 uv sync 一律 --all-extras**(纪律:裸 sync 卸 extras);CI 不走此 recipe |
| `test` | `uv run --no-sync python -m pytest -q` + `npm --prefix desktop/ui-src run test` | 全栈测试(vitest run) |
| `check` | `uvx ruff@0.16.10 check .` + `npm --prefix desktop/ui-src run build`(含 tsc -b) + `cargo check --locked`(cwd=desktop/src-tauri) | 对齐 CI 现状口径(mypy 不存在故不进) |
| `test-ui` | `npm --prefix desktop/ui-src run test` | 单跑前端 |
| `build-desktop` | `npm --prefix desktop run sidecar` + `npm --prefix desktop run tauri build` | 桌面全链(内部仍是 build-sidecar.sh + tauri CLI) |
| `docker` | `docker build .` | 与 CI docker job 同口径 |

**跨平台约束**(决议 Q7):

- recipes 只用原生命令行,无 bash-ism(无 pipe/`&&` 依赖 shell 语义处用 just 原生依赖声明 `A: B C`);
- 文件头 `set shell := ["bash", "-cu"]`:macOS/Linux 原生;Windows 经 Git Bash(装 git 自带)——与 Windows CI 跑 build-sidecar.sh 的既有事实一致,CONTRIBUTING 注明。

## 2. 钉版三件套(零新工具,各被对应工具原生读取)

| 文件 | 内容 | 生效机制 |
| --- | --- | --- |
| `.python-version`(仓库根) | `3.12` | uv 原生读取(本机 venv 实况 cpython-3.12.11);CI setup-uv 亦尊重 |
| `desktop/src-tauri/rust-toolchain.toml` | `channel = "stable"`(+ `profile = "minimal"`) | rustup 向上查找生效;与 CI dtolnay/rust-toolchain@stable 一致(不做精确版本锁,升级随 stable,如需精确锁再翻案) |
| `desktop/package.json` 与 `desktop/ui-src/package.json` | `"engines": { "node": "22" }` | CI `node-version-file: desktop/package.json` 读 engines;两处 engines 必须同步 |

**CI 收敛**(三处,机械替换):`ci.yml:37`、`desktop-release.yml:77`、`desktop-release.yml:203` 的 `node-version: "22"` → `node-version-file: desktop/package.json`。其余 CI 命令一律不动。

## 3. 清理清单(决议 Q8-b,全部 gitignored 残留,零风险)

- 删:根 `node_modules/`(空目录)、`plugins/stocks.yaml.bak`(冒烟残留)、可选 `.mypy_cache/`(历史残渣,mypy 已不在任何口径中)。
- **不动**:`myia.db` / `myssia.db`(运行库,数据根纪律留 myia 名)、`channel_*.json`(管道在用)、`credhunter-keystore.json`(密钥库)——以 CONTRIBUTING 说明段代替物理清理。

## 4. 文档(CONTRIBUTING.md 两段)

1. **一键环境**:`brew install just` → `just setup` → `just test` / `just check` / `just build-desktop`;Windows 注 Git Bash/WSL;工具版本由三件套自动约束(uv/rustup/setup-node 原生读取)。
2. **仓库根运行产物说明**:逐个说明 db 双库(改名与数据根纪律)、channel_*.json、keystore、*.bak 为何在根目录、为何不入库(gitignore 口径)。

## 5. 兼容与回滚

- 纯增量:justfile + 3 个钉版文件 + CI 三行替换 + 文档两段 + 删两个空/残留文件;不改任何构建逻辑。
- 回滚 = 反向操作(删文件、还原 CI 三行),零残留、零数据迁移。
- 风险点:CI `node-version-file` 读 engines 需要 setup-node v4(当前 @v4 ✓);`rust-toolchain.toml` 若与 CI action 冲突以 action 显式 toolchain 为准(不冲突:同为 stable)。
