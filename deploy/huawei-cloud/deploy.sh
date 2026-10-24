#!/usr/bin/env bash
# deploy/huawei-cloud/deploy.sh — MYIA 功能核·华为云无头部署(design §2 契约)
#
# 契约要点(重跑安全/幂等):
#   1. 前置自检:python3≥3.11(uv 可代装)/uv(官方脚本装,本身走 mihomo 代理)/
#      git/systemd/locale UTF-8/磁盘余量;timedatectl 时区事实记录(信息性)。
#   2. 大陆网络路由(默认):git/uv 全程走本机 mihomo http://127.0.0.1:7890
#      (git -c http.proxy=…;export HTTPS_PROXY=…;老线容器 -e HTTP_PROXY=7890 同款判例)。
#      降级备选:--bundle-dir 离线件(git bundle + uv cache,零外网)。
#   3. git clone 钉 commit → /opt/myssia(已存在则 fetch+checkout,幂等)。
#   4. uv venv && uv sync --all-extras(离线备选:移植缓存 + --no-extra agent-reach)。
#   5. 数据根种子:/opt/myssia-data/config/ ← 仓 config/*.yaml(已有不覆盖,补种幂等)
#      + keychain:→env: 引用改写(表驱动,仅服务器副本)+ clash 上游 7897→7890。
#   6. EnvironmentFile 存在性+chmod 600 校验(值由主人/实施者手填,脚本不落密钥)。
#   7. systemd 单元安装(替换 __MYSSIA_USER__)+ enable + start + cron list 冒烟。
#
# 用法:
#   ./deploy.sh [--commit <sha>] [--bundle-dir <dir>] [--dry-run]
#   ./deploy.sh --self-test        # 仅演练改写表(对内嵌样例段跑 sed,打印 diff;Mac 可跑)
#
# 环境变量(可选):MYSSIA_REPO_URL / MYSSIA_APP_DIR / MYSSIA_DATA_DIR /
#   MYSSIA_ENV_FILE / MIHOMO_PROXY / MYSSIA_SERVICE_USER / UV_PYTHON
set -euo pipefail

# ------------------------------------------------------------- 可调参数
REPO_URL="${MYSSIA_REPO_URL:-https://github.com/xinzhuzi/shishi.git}"
APP_DIR="${MYSSIA_APP_DIR:-/opt/myssia}"
DATA_DIR="${MYSSIA_DATA_DIR:-/opt/myssia-data}"
ENV_FILE="${MYSSIA_ENV_FILE:-/etc/myssia/env}"
PROXY_ADDR="${MIHOMO_PROXY:-http://127.0.0.1:7890}"
SERVICE_NAME="myssia-cron"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UNIT_SRC="${SCRIPT_DIR}/myssia-cron.service"
UNIT_DST="/etc/systemd/system/${SERVICE_NAME}.service"
UV_PYTHON_DEFAULT="${UV_PYTHON:-3.12}"

DRY_RUN=0
SELF_TEST=0
PINNED_COMMIT=""
BUNDLE_DIR=""

usage() {
  sed -n '2,30p' "$0" | sed 's/^#\{1,\} \{0,1\}//'
  exit "${1:-0}"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --commit) PINNED_COMMIT="${2:?--commit 需要参数}"; shift 2 ;;
    --bundle-dir) BUNDLE_DIR="${2:?--bundle-dir 需要参数}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    --self-test) SELF_TEST=1; shift ;;
    -h|--help) usage 0 ;;
    *) echo "未知参数:$1" >&2; usage 1 ;;
  esac
done

log()  { printf '[%s] %s\n' "$(date '+%F %T')" "$*"; }
ok()   { log "✅ $*"; }
warn() { log "⚠️  $*"; }
die()  { log "❌ $*"; exit 1; }

# dry-run 包装:预演模式只打印,不执行
run() {
  if [ "$DRY_RUN" -eq 1 ]; then
    log "[dry-run] 将执行: $*"
    return 0
  fi
  "$@"
}
run_sh() {
  if [ "$DRY_RUN" -eq 1 ]; then
    log "[dry-run] 将执行: $*"
    return 0
  fi
  sh -c "$*"
}

SUDO=""
if [ "$(id -u)" -eq 0 ]; then
  if [ -z "${MYSSIA_SERVICE_USER:-}" ]; then
    die "以 root 运行时必须指定部署用户:MYSSIA_SERVICE_USER=<非 root 用户> ./deploy.sh"
  fi
  SERVICE_USER="${MYSSIA_SERVICE_USER}"
else
  SUDO="sudo"
  SERVICE_USER="${MYSSIA_SERVICE_USER:-$(id -un)}"
fi

# ------------------------------------------------- keychain→env 改写表(R3/design §3 定稿五组)
# 形态:「旧引用|新引用」。仅作用于服务器数据根副本;仓库 config 保持 keychain: 不动
# (Mac 继续用)。FEISHU2_APP_ID/SECRET 是 bot 预设字面 env 名(feishu_card.py
# BOT_APP_CREDENTIAL_KEYS),无 keychain: 引用形态 → EnvironmentFile 直填,不在本表。
REF_REWRITES=(
  "keychain:myia/firecrawl/url|env:MYIA_FIRECRAWL_URL"
  "keychain:myia/firecrawl/api-key|env:MYIA_FIRECRAWL_KEY"
  "keychain:myia/llm/local-base-url|env:MYIA_LLM_BASE_URL"
  "keychain:myia/llm/local-api-key|env:MYIA_LLM_KEY"
  "keychain:myia/push/FEISHU_ANALYST_OPEN_ID|env:FEISHU_ANALYST_OPEN_ID"
)
# proxy-pools 服务器化(实改仅 proxy-pools.yaml 生效面):Mac Clash Verge 混合口
# 7897 → 服务器 mihomo 7890(表驱动同上;sed 表达式与引用改写同编译)
POOL_REWRITE_OLD="http://127.0.0.1:7897"
POOL_REWRITE_NEW="http://127.0.0.1:7890"

# sed BRE 元字符转义(模式侧)与替换侧转义(\\ & 与分隔符 |)
sed_esc_pat() { printf '%s' "$1" | sed -e 's/[.[\*^$]/\\&/g'; }
sed_esc_repl() { printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'; }

# 预编译 sed 表达式数组(REF_REWRITES + 池改写)
SED_EXPRS=()
_rw_row() { SED_EXPRS+=("-e" "s|$(sed_esc_pat "$1")|$(sed_esc_repl "$2")|g"); }
for _row in "${REF_REWRITES[@]}"; do _rw_row "${_row%%|*}" "${_row#*|}"; done
_rw_row "$POOL_REWRITE_OLD" "$POOL_REWRITE_NEW"
unset _row _rw_row

# 对单文件应用改写;返回码:0=已改写,1=无变化,2=sed 失败
apply_rewrites() {
  local f="$1" out
  out="$(mktemp)" || return 2
  if ! sed "${SED_EXPRS[@]}" "$f" > "$out" 2>/dev/null; then rm -f "$out"; return 2; fi
  if cmp -s "$f" "$out"; then rm -f "$out"; return 1; fi
  mv "$out" "$f"; return 0
}

# dry-run/演练:打印某文件若被改写将产生的 diff(不改文件)
show_rewrite_diff() {
  local f="$1" out
  out="$(mktemp)" || return 0
  if ! sed "${SED_EXPRS[@]}" "$f" > "$out" 2>/dev/null; then rm -f "$out"; return 0; fi
  if ! cmp -s "$f" "$out"; then
    log "改写预览 diff($f):"
    diff -u "$f" "$out" || true
  else
    log "无需改写($f)"
  fi
  rm -f "$out"
}

# 样例段(自检用;覆盖 R3 五组引用 + 魔搭残留 + clash 7897)
sample_yaml() {
  cat <<'YAMLEOF'
# 样例段:覆盖 R3 定稿五组 keychain 引用 + 魔搭残留 + clash 7897 上游
push:
  - channel: feishu_card
    target: keychain:myia/push/FEISHU_ANALYST_OPEN_ID
    bot: analyst
sources:
  - name: wool-sample
    engine: firecrawl
    url: "https://example.com/"
    api_key: keychain:myia/firecrawl/api-key
    base_url: keychain:myia/firecrawl/url
  - name: prompt-sample
    engine: prompt
    engine_options:
      prompt:
        base_url: keychain:myia/llm/local-base-url
        api_key: keychain:myia/llm/local-api-key
        model: qwen3.8-27b-coder390
  - name: modelscope-residue-sample
    engine: prompt
    engine_options:
      prompt:
        base_url: keychain:myia/llm/modelscope-base-url
YAMLEOF
}

# ============================================================ --self-test 模式
# 改写表对样例段演练:打印 diff 并核验五组引用+池上游全改、魔搭残留检测样例在位。
if [ "$SELF_TEST" -eq 1 ]; then
  TMPD="$(mktemp -d /tmp/myssia-deploy-selftest.XXXXXX)"
  sample_yaml > "$TMPD/orig.yaml"
  cp "$TMPD/orig.yaml" "$TMPD/rewritten.yaml"
  apply_rewrites "$TMPD/rewritten.yaml"; rc=$?
  echo "=== 样例原文 ==="; cat "$TMPD/orig.yaml"; echo
  echo "=== 改写 diff(-u 原文 → 改写后) ==="
  diff -u "$TMPD/orig.yaml" "$TMPD/rewritten.yaml" || true
  echo
  echo "=== 池改写样例(proxy-pools.yaml 形态) ==="
  printf 'pools:\n  clash: http://127.0.0.1:7897\n' > "$TMPD/proxy-pools.yaml"
  apply_rewrites "$TMPD/proxy-pools.yaml" || true
  cat "$TMPD/proxy-pools.yaml"

  fail=0
  [ "$rc" -eq 0 ] || { echo "❌ apply_rewrites 返回码异常:${rc}"; fail=1; }
  for old in "keychain:myia/firecrawl/url" "keychain:myia/firecrawl/api-key" \
             "keychain:myia/llm/local-base-url" "keychain:myia/llm/local-api-key" \
             "keychain:myia/push/FEISHU_ANALYST_OPEN_ID"; do
    if grep -qF "$old" "$TMPD/rewritten.yaml"; then echo "❌ 残留未改:$old"; fail=1; else echo "✅ 已改写:$old"; fi
  done
  for new in "env:MYIA_FIRECRAWL_URL" "env:MYIA_FIRECRAWL_KEY" "env:MYIA_LLM_BASE_URL" \
             "env:MYIA_LLM_KEY" "env:FEISHU_ANALYST_OPEN_ID"; do
    if grep -qF "$new" "$TMPD/rewritten.yaml"; then echo "✅ 新引用在位:$new"; else echo "❌ 新引用缺失:$new"; fail=1; fi
  done
  if grep -qF "http://127.0.0.1:7890" "$TMPD/proxy-pools.yaml"; then echo "✅ clash 上游 7897→7890"; else echo "❌ 池上游未改"; fail=1; fi
  if grep -qF "keychain:myia/llm/modelscope-base-url" "$TMPD/rewritten.yaml"; then
    echo "✅ 魔搭残留不在改写表(部署步 RESIDUE 硬校验会拦)"
  else
    echo "❌ 魔搭样例被误改(不应在改写表内)"; fail=1
  fi
  rm -rf "$TMPD"
  if [ "$fail" -eq 0 ]; then ok "self-test 全过:五组引用改写 + 池上游改写 + 魔搭残留留检"; exit 0; fi
  die "self-test 有失败项"
fi

# ============================================================ 正式部署
log "deploy.sh 开始(dry-run=${DRY_RUN}, bundle=${BUNDLE_DIR:-无}, commit=${PINNED_COMMIT:-origin/main HEAD})"

# ------------------------------------------------------------ 1. 前置自检
log "—— 前置自检 ——"

command -v git >/dev/null 2>&1 || die "git 不在位:apt-get install -y git"
ok "git 在位:$(git --version)"

if [ -d /run/systemd/system ]; then ok "systemd 在位(/run/systemd/system)"; else die "systemd 不可用"; fi

# locale UTF-8(已知真风险:LANG=C 下中文条目/推送必乱码,design §6)
if locale 2>/dev/null | grep -qi 'utf-8'; then
  ok "locale UTF-8 在位:$(locale 2>/dev/null | grep -i 'LANG=' | head -1)"
else
  die "locale 非 UTF-8(中文内容会乱码)。修法:localectl set-locale LANG=C.UTF-8 后重新登录,或 /etc/default/locale 设 LANG=C.UTF-8(README §9)"
fi

# 时区事实(信息性;品类 YAML 全带 timezone: Asia/Shanghai,零依赖系统时区——design §6 时区链)
log "时区事实(信息性):"
timedatectl 2>/dev/null | head -6 || date

# 磁盘余量(uv sync --all-extras 含 playwright/chromium 约 1-2GB)
FREE_MB="$(df -Pm /opt 2>/dev/null | awk 'NR==2{print $4}')"
FREE_MB="${FREE_MB:-$(df -Pm / | awk 'NR==2{print $4}')}"
if [ "${FREE_MB:-0}" -lt 1024 ]; then
  die "磁盘余量不足:${FREE_MB}MB(<1GB;uv sync 全量 extras 需 ~2GB)"
elif [ "${FREE_MB:-0}" -lt 3072 ]; then
  warn "磁盘余量偏紧:${FREE_MB}MB(建议 ≥3GB)"
else
  ok "磁盘余量:${FREE_MB}MB"
fi

# python3 ≥3.11(不满足则 uv 代装,design §2「uv 可代装」)
SYS_PY_OK=0
if command -v python3 >/dev/null 2>&1; then
  PY3V="$(python3 -V 2>&1 | awk '{print $2}')"
  PY3MAJOR="${PY3V%%.*}"; PY3MINOR="$(echo "$PY3V" | cut -d. -f2)"
  if [ "${PY3MAJOR:-0}" -gt 3 ] || { [ "${PY3MAJOR:-0}" -eq 3 ] && [ "${PY3MINOR:-0}" -ge 11 ]; }; then
    ok "python3 ${PY3V} ≥3.11"
    SYS_PY_OK=1
  else
    warn "python3 ${PY3V} <3.11 → 将由 uv 代装 python(${UV_PYTHON_DEFAULT})"
  fi
else
  warn "python3 不在位 → 将由 uv 代装 python(${UV_PYTHON_DEFAULT})"
fi

# uv 在位;无则官方脚本装(装 uv 本身走 mihomo 代理,design §2)
if command -v uv >/dev/null 2>&1; then
  ok "uv 在位:$(uv --version | head -1)"
else
  if [ -n "$BUNDLE_DIR" ]; then
    die "uv 不在位且离线模式无法装 uv:开网络窗口先装(README §9)"
  fi
  log "uv 不在位 → 官方脚本安装(走 ${PROXY_ADDR})……"
  run_sh "curl -LsSf --proxy '${PROXY_ADDR}' https://astral.sh/uv/install.sh | env HTTPS_PROXY='${PROXY_ADDR}' HTTP_PROXY='${PROXY_ADDR}' sh" \
    || die "uv 安装失败(检查 mihomo 代理;或改用 --bundle-dir 离线备选,README §2)"
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv >/dev/null 2>&1 || die "uv 安装完仍不在 PATH:source ~/.local/bin/env 后重试"
  ok "uv 已装:$(uv --version | head -1)"
fi

# python 由 uv 代装(系统 python 不足/缺失时;装 python 走代理)
if [ "$SYS_PY_OK" -eq 0 ]; then
  if [ -n "$BUNDLE_DIR" ]; then
    run uv python install "$UV_PYTHON_DEFAULT" || die "离线模式装 python 失败(需网络窗口)"
  else
    run_sh "env HTTPS_PROXY='${PROXY_ADDR}' HTTP_PROXY='${PROXY_ADDR}' uv python install '${UV_PYTHON_DEFAULT}'" \
      || die "uv python install 失败(检查 mihomo 代理)"
  fi
fi

# mihomo 代理探活(默认路由命脉;离线备选豁免)
if [ -n "$BUNDLE_DIR" ]; then
  warn "离线备选模式(--bundle-dir):跳过外网/代理探活,git 走 bundle、uv 走移植缓存"
else
  log "mihomo 代理探活:${PROXY_ADDR} ……"
  PROBE="$(curl -x "$PROXY_ADDR" -sI --max-time 15 https://www.google.com | head -1 || true)"
  if [ -n "$PROBE" ]; then
    ok "代理探活通过:${PROBE}"
  else
    die "mihomo 代理 ${PROXY_ADDR} 不通(节点失效?06:00 自动刷节点/手动换节点后重跑;或 --bundle-dir 离线备选,README §1/§9)"
  fi
fi

# git 代理路由包装(design §2:git 全程走 mihomo)
gitp() {
  if [ -n "$BUNDLE_DIR" ]; then
    git "$@"
  else
    git -c "http.proxy=${PROXY_ADDR}" -c "https.proxy=${PROXY_ADDR}" "$@"
  fi
}
# uv 代理路由(环境变量;老线容器 -e HTTP_PROXY=7890 同款判例)
if [ -z "$BUNDLE_DIR" ] && [ "$DRY_RUN" -eq 0 ]; then
  export HTTP_PROXY="${PROXY_ADDR}" HTTPS_PROXY="${PROXY_ADDR}" \
         http_proxy="${PROXY_ADDR}" https_proxy="${PROXY_ADDR}"
fi

# ------------------------------------------------------------ 2. 目录与用户
log "—— 目录与部署用户(service user=${SERVICE_USER}) ——"
id "$SERVICE_USER" >/dev/null 2>&1 || die "部署用户 ${SERVICE_USER} 不存在:useradd -m -s /bin/bash ${SERVICE_USER}(README §1)"
run $SUDO mkdir -p "$(dirname "$ENV_FILE")" "$APP_DIR" "$DATA_DIR"
if [ "$DRY_RUN" -eq 0 ]; then
  # 数据根必须归 SERVICE_USER(sqlite 写);代码根新克隆前同归,免 root 直写
  $SUDO chown "${SERVICE_USER}" "$DATA_DIR"
  [ -d "$APP_DIR/.git" ] || $SUDO chown "${SERVICE_USER}" "$APP_DIR"
fi

# ------------------------------------------------------------ 3. 代码:clone 钉 commit(幂等)
log "—— 代码部署:${REPO_URL} → ${APP_DIR} ——"
RESOLVED=""
if [ -d "$APP_DIR/.git" ]; then
  if [ -n "$BUNDLE_DIR" ]; then
    log "已存在 $APP_DIR(幂等跳过 bundle 克隆;升 commit 走网络模式 fetch)"
    cd "$APP_DIR"
    RESOLVED="$(git rev-parse "${PINNED_COMMIT:-HEAD}")"
  else
    log "已存在 $APP_DIR → fetch origin main + checkout(幂等)"
    run gitp -C "$APP_DIR" fetch origin main || die "git fetch 失败(代理 ${PROXY_ADDR};README §9)"
    cd "$APP_DIR"
    RESOLVED="$(git rev-parse "${PINNED_COMMIT:-origin/main}")"
  fi
elif [ "$DRY_RUN" -eq 1 ]; then
  # 预演:服务器尚未克隆 → 用本仓(脚本的仓库根)作 config 面预览源
  log "[dry-run] ${APP_DIR} 不存在,将克隆;预演改写用本仓 config 面同源预览"
  cd "${SCRIPT_DIR}/../.."
  RESOLVED="$(git rev-parse HEAD)"
  APP_DIR="$(pwd)"
else
  if [ -n "$BUNDLE_DIR" ]; then
    BUNDLE_FILE="${BUNDLE_DIR}/myssia.bundle"
    [ -f "$BUNDLE_FILE" ] || die "离线件缺 myssia.bundle(=${BUNDLE_FILE};Mac 侧打包命令见 README §2)"
    run git clone "$BUNDLE_FILE" "$APP_DIR" || die "bundle 克隆失败"
    cd "$APP_DIR"
    RESOLVED="$(git rev-parse "${PINNED_COMMIT:-HEAD}")"
  else
    run gitp clone "$REPO_URL" "$APP_DIR" || die "git clone 失败(代理 ${PROXY_ADDR};README §9)"
    cd "$APP_DIR"
    RESOLVED="$(git rev-parse "${PINNED_COMMIT:-origin/main}")"
  fi
fi
run git checkout --detach "$RESOLVED" || die "checkout ${RESOLVED} 失败"
ok "钉 commit:${RESOLVED}"

# ------------------------------------------------------------ 4. uv 环境
log "—— uv 环境:venv + sync --all-extras ——"
if [ "$SYS_PY_OK" -eq 1 ]; then
  run uv venv "$APP_DIR/.venv" || die "uv venv 失败"
else
  run uv venv --python "$UV_PYTHON_DEFAULT" "$APP_DIR/.venv" || die "uv venv(代装 python ${UV_PYTHON_DEFAULT})失败"
fi
if [ -n "$BUNDLE_DIR" ]; then
  warn "离线备选:uv sync 用移植缓存(--offline)+ --no-extra agent-reach(design §2 降级备选)"
  run_sh "UV_CACHE_DIR='${BUNDLE_DIR}/uv-cache' uv sync --all-extras --no-extra agent-reach --offline" \
    || die "离线 uv sync 失败(缓存不全:改走代理模式重跑,README §9)"
else
  run_sh "uv sync --all-extras" || die "uv sync 失败(代理 ${PROXY_ADDR};降级备选 --bundle-dir,README §2)"
fi
if [ "$(id -u)" -eq 0 ] && [ "$DRY_RUN" -eq 0 ]; then
  $SUDO chown -R "${SERVICE_USER}" "$APP_DIR"   # root 代跑时归还部署用户
fi
ok "uv 环境就绪:${APP_DIR}/.venv"

# ------------------------------------- 5. 数据根种子 + 引用改写(仅服务器副本)
log "—— 数据根种子:${DATA_DIR}/config/ ← ${APP_DIR}/config/*.yaml(已有不覆盖) ——"
if [ "$DRY_RUN" -eq 0 ]; then
  mkdir -p "${DATA_DIR}/config"
fi
SEEDED=0; SKIPPED=0
for f in "$APP_DIR"/config/*.yaml; do
  [ -e "$f" ] || continue
  base="$(basename "$f")"
  target="${DATA_DIR}/config/${base}"
  if [ -e "$target" ]; then
    SKIPPED=$((SKIPPED+1))
    if [ "$DRY_RUN" -eq 1 ]; then
      log "已存在不覆盖:${base}(仅重放改写,预览如下)"
      show_rewrite_diff "$target"
    else
      # 幂等重放改写(已是 env: 形态则无变化;治愈半改写文件)
      if apply_rewrites "$target"; then
        log "改写重放有更新:${base}"
      elif [ $? -eq 2 ]; then
        die "sed 改写失败:${target}"
      fi
    fi
  else
    SEEDED=$((SEEDED+1))
    if [ "$DRY_RUN" -eq 1 ]; then
      log "将补种:${base}"
      show_rewrite_diff "$f"
    else
      cp "$f" "$target"
      if apply_rewrites "$target"; then
        log "补种+改写:${base}"
      elif [ $? -eq 2 ]; then
        die "sed 改写失败:${target}"
      else
        log "补种:${base}(无需改写)"
      fi
    fi
  fi
done
ok "种子完成:新补 ${SEEDED} 件 / 已存在跳过 ${SKIPPED} 件"

# 魔搭残留硬校验(R2b 后零出现;design §3 表行 6)
RESIDUE="$(grep -rn 'keychain:myia/llm/modelscope' "${DATA_DIR}/config/" "$APP_DIR/config/" 2>/dev/null | grep -vE ':[0-9]+:[[:space:]]*#' || true)"
if [ -n "$RESIDUE" ]; then
  log "魔搭残留(应零出现):"; echo "$RESIDUE"
  die "keychain:myia/llm/modelscope 残留 —— R2b 未生效或源过旧:先落 R2b(config/ai-token-deals.yaml 切本地 LM Studio)再部署"
fi
ok "魔搭残留:零(R2b 已生效)"

# 剩余 keychain: 引用 = 信息性报告(Mac 绑定品类 weixin/telegram 系不上云运行,属预期)
REMAINING="$(grep -rn 'keychain:' "${DATA_DIR}/config/" 2>/dev/null | grep -vE ':[0-9]+:[[:space:]]*#' || true)"
if [ -n "$REMAINING" ]; then
  warn "剩余 keychain: 引用(下列属 Mac 绑定品类,不上云运行,属预期;情报线应已全 env:):"
  echo "$REMAINING" | head -20
fi

# 部署事实落档(审计/任务档证据)
if [ "$DRY_RUN" -eq 0 ]; then
  {
    echo "deployed_at=$(date -Is)"
    echo "commit=${RESOLVED}"
    echo "repo=${REPO_URL}"
    echo "service_user=${SERVICE_USER}"
    echo "locale=$(locale 2>/dev/null | grep -i 'LANG=' | head -1)"
    timedatectl 2>/dev/null | head -6 || date
  } > "${DATA_DIR}/deploy-facts.txt"
  ok "部署事实入档:${DATA_DIR}/deploy-facts.txt"
fi

# ------------------------------------------- 6. EnvironmentFile 校验(不落密钥)
log "—— EnvironmentFile:${ENV_FILE} ——"
NEED_KEYS=(MYIA_FIRECRAWL_URL MYIA_FIRECRAWL_KEY MYIA_LLM_BASE_URL MYIA_LLM_KEY FEISHU_ANALYST_OPEN_ID FEISHU2_APP_ID FEISHU2_APP_SECRET)
if [ ! -f "$ENV_FILE" ]; then
  if [ "$DRY_RUN" -eq 1 ]; then
    warn "[dry-run] ${ENV_FILE} 不存在:将生成占位模板(chmod 600)后停,手填七值再重跑(README §3)"
  else
    warn "EnvironmentFile 不存在 → 生成占位模板(值由主人/实施者手填,脚本永不落密钥)"
    $SUDO sh -c "cat > '${ENV_FILE}'" <<'ENVEOF'
# /etc/myssia/env — myssia-cron.service EnvironmentFile(chmod 600;值不进 git 不进档)
# 逐把导出命令见 deploy/huawei-cloud/README.md §3。
# MYIA_LLM_BASE_URL 服务器侧值 = http://<Mac 局域网 IP>:1234/v1(R5 默认;Mac LM Studio 需开 0.0.0.0 监听)。
MYIA_FIRECRAWL_URL=
MYIA_FIRECRAWL_KEY=
MYIA_LLM_BASE_URL=http://MAC-IP-PLACEHOLDER:1234/v1
MYIA_LLM_KEY=
FEISHU_ANALYST_OPEN_ID=
FEISHU2_APP_ID=
FEISHU2_APP_SECRET=
ENVEOF
    $SUDO chmod 600 "$ENV_FILE"
    die "EnvironmentFile 已生成占位模板:手填七值后重跑本脚本(README §3 凭据填写表)"
  fi
else
  PERM="$(stat -c '%a' "$ENV_FILE" 2>/dev/null || stat -f '%Lp' "$ENV_FILE")"
  if [ "$PERM" != "600" ]; then
    run $SUDO chmod 600 "$ENV_FILE"
    PERM="$(stat -c '%a' "$ENV_FILE" 2>/dev/null || stat -f '%Lp' "$ENV_FILE")"
    [ "$PERM" = "600" ] || die "EnvironmentFile 权限非 600(当前 ${PERM})"
  fi
  ok "EnvironmentFile 权限 600"
  MISSING_KEYS=""
  for k in "${NEED_KEYS[@]}"; do
    $SUDO grep -qE "^[[:space:]]*${k}=" "$ENV_FILE" || MISSING_KEYS="${MISSING_KEYS} ${k}"
  done
  if [ -n "$MISSING_KEYS" ]; then die "EnvironmentFile 缺键:${MISSING_KEYS}(README §3 表)"; fi
  ok "EnvironmentFile 七键齐全(值正确性由各品类 --dry-run 装载抽测把关,AC3)"
fi

# ------------------------------------------------------------ 7. systemd 单元
log "—— systemd:${SERVICE_NAME}.service ——"
[ -f "$UNIT_SRC" ] || die "单元文件缺失:${UNIT_SRC}(deploy.sh 与 myssia-cron.service 同目录)"
if [ "$DRY_RUN" -eq 1 ]; then
  log "[dry-run] 将安装单元(替换 __MYSSIA_USER__ → ${SERVICE_USER})+ daemon-reload + enable + restart"
else
  $SUDO sed "s|__MYSSIA_USER__|${SERVICE_USER}|g" "$UNIT_SRC" > "$UNIT_DST"
  $SUDO systemctl daemon-reload
  $SUDO systemctl enable "${SERVICE_NAME}.service"
  $SUDO systemctl restart "${SERVICE_NAME}.service"
  sleep 2
  IS_ACTIVE="$(systemctl is-active "${SERVICE_NAME}.service" || true)"
  if [ "$IS_ACTIVE" != "active" ]; then
    journalctl -u "$SERVICE_NAME" -n 30 --no-pager || true
    die "service 未 active(${IS_ACTIVE});journal 见上(排障 README §9)"
  fi
  ok "systemd active + enabled"
  log "journalctl 尾部快照:"; journalctl -u "$SERVICE_NAME" -n 5 --no-pager || true
fi

# cron list 冒烟(品类装载面)
log "—— cron list 冒烟 ——"
if [ "$DRY_RUN" -eq 1 ]; then
  log "[dry-run] 将执行:MYIA_HOME=${DATA_DIR} ${APP_DIR}/.venv/bin/myssia cron list"
else
  $SUDO env MYIA_HOME="$DATA_DIR" "$APP_DIR/.venv/bin/myssia" cron list \
    || die "cron list 冒烟失败(先 journalctl -u ${SERVICE_NAME} -n 50;README §9)"
fi

ok "部署完成。后续:数据搬种(README §4)→ 影子期(§5)→ 切割(§6)"
