# 执行计划:统一开发入口(justfile + 三件套 + CI 收敛 + 文档 + 清理)

> 决议:prd.md §2;技术口径:design.md。规模约 0.5-1 天。
> 前置:10-04-yaml-editor-no-scroll 已收口(排期决议 Q3)。

## 有序清单

1. [ ] **参考研究**(≤30 分钟):读 2-3 个高星 polyglot 仓 justfile(helix 等),定 recipe 组织风格。
2. [ ] **justfile 落地**(仓库根):按 design.md §1 六个 recipe;`just --list` 输出即活文档。
3. [ ] **本地验证**:`just setup` 幂等可重跑;`just test` 全绿(pytest + vitest);`just check` 全绿(ruff + tsc/vite build + cargo check);退出码如实透传(故意制造一个红验证不改口)。
4. [ ] **钉版三件套**:
   - `.python-version` = `3.12`,验证 `uv run --no-sync python -V` 报 3.12;
   - `desktop/src-tauri/rust-toolchain.toml`(stable/minimal),验证 `cargo --version` 正常;
   - 两个 package.json 加 `engines.node: "22"`(两处必须同步)。
5. [ ] **CI 收敛三处**:`ci.yml:37`、`desktop-release.yml:77/203` → `node-version-file: desktop/package.json`;diff 确认无其他 CI 改动。
6. [ ] **清理**:删根 `node_modules/`(空)、`plugins/stocks.yaml.bak`;可选删 `.mypy_cache/`;`git status` 确认三者本就 untracked(零跟踪变更)。
7. [ ] **CONTRIBUTING 两段**:「一键环境」(just 路径 + Windows Git Bash/WSL 注记)与「仓库根运行产物说明」(db 双库/channel_*.json/keystore/*.bak)。
8. [ ] **门禁**:仓库级 `uv run --no-sync python -m pytest -q` + `npx --prefix desktop/ui-src vitest run` + `tsc -b` + `cargo check` 全绿;推送后观察 ci / desktop-release 触发口径无红(CI 未引入 just,行为不变)。

## 收尾

- [ ] 单笔或两笔提交(justfile+钉版+CI / 文档+清理),AC 回填 prd.md。
- [ ] 无装机包动作(纯开发者工具面,不触产品)。

## 回滚

- 删 justfile 与三件套、还原 CI 三行、删 CONTRIBUTING 两段、还原清理项(均为 untracked/空文件,无需还原)。
