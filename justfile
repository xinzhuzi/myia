# MYIA / myssia 统一开发入口:uv(Python workspace)+ npm ×2(desktop 双根)+ cargo(Tauri)+ docker 一家门面。
# 原则:纯门面——不替换各语言原生工具;每个 recipe 内部仍是既有原命令,
# 与 .github/workflows/ci.yml 同口径,退出码如实透传(红就是红)。
# 任务档:.trellis/tasks/10-04-unified-dev-entry(design §1 六 recipe)。
#
# 工具版本由仓内钉版文件原生约束(零新工具):
#   Python 3.12   ← .python-version(uv 原生读)
#   Rust  stable  ← desktop/src-tauri/rust-toolchain.toml(rustup 原生读)
#   Node   22     ← desktop/package.json 与 desktop/ui-src/package.json 的 engines.node
#
# Windows:在 Git Bash(装 git 自带)或 WSL 里运行——与 Windows CI 用 Git Bash
# 跑 build-sidecar.sh 的既有事实一致;不提供 PowerShell 移植。
set shell := ["bash", "-cu"]

# 一键全栈环境(幂等可重跑):uv sync --all-extras(纪律:裸 sync 卸 extras)+ 两个 npm 根 npm ci + Rust 工具链提示。
setup:
    uv sync --all-extras
    npm --prefix desktop ci --no-fund --no-audit
    npm --prefix desktop/ui-src ci --no-fund --no-audit
    @echo 'Rust: 需自装 rustup(仓内 desktop/src-tauri/rust-toolchain.toml 已钉 stable/minimal,rustup 首次进入自动安装)'

# 全栈测试:pytest + vitest(TZ 与 CI 同口径:排程/相对时间断言按 +08 编写)。
[env('TZ', 'Asia/Shanghai')]
test:
    uv run --no-sync python -m pytest -q --tb=short
    npm --prefix desktop/ui-src run test

# 只跑前端组件测试(desktop/ui-src,vitest run)。
[env('TZ', 'Asia/Shanghai')]
test-ui:
    npm --prefix desktop/ui-src run test

# 静态门禁(对齐 CI 现状):ruff(锁 0.16.10)+ tsc -b && vite build + cargo check --locked。
check:
    uvx ruff@0.16.10 check .
    npm --prefix desktop/ui-src run build
    cd desktop/src-tauri && cargo check --locked

# 桌面全链:sidecar 打包(PyInstaller,经既有 build-sidecar.sh)→ tauri build;安装包产出到 desktop/src-tauri/target/。
build-desktop:
    npm --prefix desktop run sidecar
    npm --prefix desktop run tauri build

# Docker 镜像构建检查(与 ci.yml docker-build job 同口径:本机原生架构,不 push 不打 tag)。
docker:
    docker build .
