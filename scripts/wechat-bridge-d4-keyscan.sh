#!/usr/bin/env bash
#
# wechat-bridge-d4-keyscan.sh — 微信桥 D4 内存密钥扫描一键脚本
# (task 10-11-wechat-ui-bridge AC7 收尾,2026-10-12;固化
#  research/d4-memscan-e2e.md §5 主人单条提权命令为可自检的脚本形态)
#
# 【机理】单次只读批处理扫描,不是常驻服务:
#   0. 前置自检(darwin / 仓库 venv / 组件 / 微信进程在场 / 本地库数据根)——
#      任一缺位按 §6 错误码族诚实退出,不消耗 sudo 密码输入;
#   1. 扫描前跑一次 `wechat-bridge --probe` 对照基线(state / mem_search_enabled);
#   2. 显式开启 mem_search_enabled(主人运行本脚本 = 主人显式开启,design §4;
#      其余配置键原样保留,原配置自动备份为 config.json.pre-keyscan);
#   3. sudo 提权下调用组件 `localdb key-scan --json`:组件三重门(主人裁决
#      在案 + 配置显式开启 + root/darwin)逐门校验后,对微信进程做**一次**
#      遍历——只读 vm_read 类 mach 调用(task_for_pid / mach_vm_region /
#      mach_vm_read_overwrite,读进本进程缓冲即离手),可写私有区 32B 滑窗
#      × 离线 HMAC-SHA512 校验,全量命中才落 keys.json(数据根私有区,600,
#      sudo 会话内组件侧自动把属主归还发起 sudo 的用户);扫完进程即退,
#      零常驻、零轮询、零重试。零写内存、零注入、零调试器附加、零重签名
#      (组件源码级守卫钉死:test_source_readonly_guards)。
#   4. 扫描退出码 rc 暂存;尾部 sudo chown 属主归还兜底(旧装机件/非 sudo
#      root 会话场景,对不存在目录静默跳过)——chown 结果**不遮掩**扫描
#      退出码,(exit $rc) 原样奉还;
#   5. 扫描后再跑一次 probe 对照;收尾打印 mem_search_enabled 还原命令
#      (是否还原由主人决定;localdb query 消费 keys.json 不读该开关,
#      还原不影响查询闭环)。
#
# 【边界】
#   - sudo 密码由主人按日常习惯亲自输入;本脚本与桥、子代理全程不索要、
#     不读、不存密码。
#   - 预算:单区 64 MiB / 总 256 MiB / 段 1 MiB(组件模块常量,刻意无配置面
#     ——预算即边界);耗尽如实标 interrupted。
#   - 诚实语义:零命中/部分命中/内核拒绝 = exit 21 key_unavailable——诚实,
#     不是脚本故障。如实预告:本机微信为 hardened runtime 签名,XNU 对
#     restricted 目标的 task_for_pid 要求调用方持调试类 entitlement,root 亦
#     可能被拒(KERN_FAILURE)——该拒绝即「红线内(不重签/不 lldb)此路在本机
#     不可达」的如实信号,应答原样上报 mach 码;届时 D4 收口回落外部密钥
#     引入(keys.json,组件校验器直接消费)或长灰 degraded。
#   - 对 §5 原命令的一处确定性加固:sudo env 显式钉 HOME="$HOME"。组件
#     locate_db_storage/WECHAT_FILES_ROOT 按 Path.home() 定位微信数据
#     (system_checks.py),而本机 sudo 1.9.17p2 缺省 env_reset 会把 HOME
#     重置为 /var/root(man sudoers:「By default, the env_reset flag is
#     enabled … HOME … initialized based on the target user」)——不钉则
#     sudo 内必 exit 20 db_not_found;显式 env 变量可穿透 env_reset。
#
# 【预计时长】实测扫描速率 0.34 MiB/s(4/8/16 MiB 三档一致),256 MiB 预算
#   外推全程 ≈12 分钟;期间微信零扰动、零前台操作——扫描器不触碰窗口/AX,
#   纯内核只读调用,主人只需等待。
#
# 【用法】
#   scripts/wechat-bridge-d4-keyscan.sh            # 真跑(会请求 sudo 密码)
#   scripts/wechat-bridge-d4-keyscan.sh --dry-run  # 不提权自校验:前置检查
#     (缺位只警告不阻断)+ 缺省关路径冒烟(临时 MYIA_HOME,预期诚实
#     exit 21 key_unavailable)+ 打印真跑将执行的命令
#
# 【退出码】0 命中;10 微信不在;20 数据根缺位;21 密钥不可得(诚实拒绝/
#   零命中/部分命中/内核拒/非 darwin);2 用法/环境错;其余见 design §6。

set -euo pipefail

SMOKE_TMP=""
SCAN_STARTED=""
# 复审 low 收口(2026-10-12):中断路径(Ctrl-C/被杀)收尾段不会执行——
# 开关合并写之后若被中断,真配置停留在 mem_search_enabled=true 且用户
# 未被告知还原命令;EXIT trap 补一条中断还原提示(收尾段正常走时它
# 也会打印,属可容忍重复;SCAN_STARTED 钉住「合并写已发生」才提示)。
trap 'if [ -n "$SMOKE_TMP" ]; then rm -rf "$SMOKE_TMP"; fi
      if [ -n "$SCAN_STARTED" ]; then
        echo "[中断提示] 开关可能仍为开启态;还原: cp \"\$CONFIG_FILE.pre-keyscan\" \"\$CONFIG_FILE\" 或回全缺省(design §7),详见脚本尾部收尾段。"
      fi' EXIT

# —— 路径解析(脚本自定位,不依赖 cwd;数据根与组件 config.py myssia_home
#    同序:显式 MYIA_HOME env > darwin 缺省)——
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
COMPONENT_ROOT="$REPO_ROOT/plugins/wechat-bridge"
SCRIPT_SELF="$(basename "${BASH_SOURCE[0]}")"

MODE="${1:-run}"

MYIA_HOME="${MYIA_HOME:-$HOME/Library/Application Support/MYIA}"
CONFIG_DIR="$MYIA_HOME/wechat-bridge"
CONFIG_FILE="$CONFIG_DIR/config.json"
CONFIG_BACKUP="$CONFIG_FILE.pre-keyscan"
LOCALDB_DIR="$MYIA_HOME/wechat-localdb"
WECHAT_FILES_ROOT="$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files"

usage() {
  echo "用法: scripts/$SCRIPT_SELF [--dry-run]" >&2
  echo "  (无参)      真跑:sudo 提权一次只读批处理扫描(主人亲自输 sudo 密码)" >&2
  echo "  --dry-run   不提权自校验:前置检查 + 缺省关路径冒烟 + 打印真跑命令" >&2
}

die() { echo "✗ $1" >&2; exit "$2"; }

# —— 前置自检:real 模式缺位即诚实退出(省一次无谓的 sudo 密码输入);
#    dry-run 模式只警告不阻断(自校验重点是缺省关冒烟)——
preflight() {
  local hard="$1"
  local ok=1
  [[ "$(uname -s)" == "Darwin" ]] || { echo "✗ 非 darwin(mach 只读实现仅 macOS,组件门③同口径)" >&2; ok=0; }
  [[ -x "$PYTHON_BIN" ]] || { echo "✗ 缺 $PYTHON_BIN(仓库 .venv;铁律勿往仓库 venv 装包,缺环境先建)" >&2; ok=0; }
  [[ -f "$COMPONENT_ROOT/wechat_bridge/__main__.py" ]] || { echo "✗ 缺组件 $COMPONENT_ROOT/wechat_bridge" >&2; ok=0; }
  if ! pgrep -x WeChat >/dev/null 2>&1; then
    echo "✗ 微信进程不在(pgrep -x WeChat 零命中)→ 真跑必 exit 10;先启动微信并登录" >&2
    ok=0
  fi
  if [[ ! -d "$WECHAT_FILES_ROOT" ]]; then
    echo "✗ 本地库数据根缺位: $WECHAT_FILES_ROOT → 真跑必 exit 20" >&2
    ok=0
  fi
  if [[ "$ok" -ne 1 ]]; then
    if [[ "$hard" == "hard" ]]; then
      die "前置自检未过(见上),已止于 sudo 之前" 2
    fi
    echo "⚠ dry-run:以上前置缺位仅警告(真跑会按 §6 码族诚实退出)" >&2
  else
    echo "✓ 前置自检通过:darwin / venv / 组件 / 微信进程 / 本地库数据根"
  fi
}

run_probe() {
  local label="$1" out rc=0
  out="$(MYIA_HOME="$MYIA_HOME" PYTHONPATH="$COMPONENT_ROOT" \
    "$PYTHON_BIN" -m wechat_bridge --probe 2>/dev/null)" || rc=$?
  echo "── probe($label): exit=$rc ──"
  if [[ -n "$out" ]]; then printf '%s\n' "$out"; else echo "(probe 无 stdout 应答)"; fi
}

# —— 显式开启开关:合并写(其余配置键原样保留),原配置先备份;
#    既有配置非法 JSON 时诚实中止(load_config 本会 fail-fast exit 2,
#    不静默覆盖主人的文件)——
enable_mem_search() {
  if [[ -f "$CONFIG_FILE" ]]; then
    cp "$CONFIG_FILE" "$CONFIG_BACKUP"
SCAN_STARTED=1
    echo "已备份原配置 → $CONFIG_BACKUP"
  fi
  mkdir -p "$CONFIG_DIR"
  "$PYTHON_BIN" - "$CONFIG_FILE" <<'PYEOF'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
cfg: dict = {}
if path.is_file():
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        sys.exit(f"既有桥配置非法 JSON: {path}({exc});先修正或删除该文件再跑(不静默覆盖)")
    if isinstance(raw, dict):
        cfg = raw
cfg["mem_search_enabled"] = True
path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"已开启 mem_search_enabled=true → {path}(其余键原样保留)")
PYEOF
}

case "$MODE" in
  -h|--help)
    usage
    exit 0
    ;;
  --dry-run)
    preflight "warn"
    echo "── 自校验(不提权):缺省关路径冒烟(临时 MYIA_HOME,不触真配置/不碰微信)──"
    SMOKE_TMP="$(mktemp -d)"
    smoke_rc=0
    smoke_out="$(MYIA_HOME="$SMOKE_TMP" PYTHONPATH="$COMPONENT_ROOT" \
      "$PYTHON_BIN" -m wechat_bridge localdb key-scan --json 2>/dev/null)" || smoke_rc=$?
    printf '%s\n' "$smoke_out"
    if [[ "$smoke_rc" -eq 21 ]] && printf '%s' "$smoke_out" | grep -q 'key_unavailable'; then
      echo "✓ 自校验通过:缺省关路径诚实拒绝(exit 21 key_unavailable),未提权、未触真配置"
    else
      die "自校验不符预期:exit=$smoke_rc(预期 21 key_unavailable;应答见上)" 1
    fi
    echo ""
    echo "── 真跑将执行(固化 research/d4-memscan-e2e.md §5 + HOME 钉住加固)──"
    echo "  1) probe(前)  : MYIA_HOME=\"$MYIA_HOME\" \"$PYTHON_BIN\" -m wechat_bridge --probe"
    echo "  2) 开关合并写 : mem_search_enabled=true → $CONFIG_FILE(原配置备份至 $CONFIG_BACKUP)"
    echo "  3) 扫描(一次) : sudo env HOME=\"\$HOME\" MYIA_HOME=\"$MYIA_HOME\" \\"
    echo "                   PYTHONPATH=\"$COMPONENT_ROOT\" \\"
    echo "                   \"$PYTHON_BIN\" -m wechat_bridge localdb key-scan --json"
    echo "  4) 属主兜底   : sudo chown -R \"\$(id -u):\$(id -g)\" \"$LOCALDB_DIR\"(rc 不被吞)"
    echo "  5) probe(后) + 收尾还原提示"
    exit 0
    ;;
  run|"")
    preflight "hard"
    run_probe "扫描前"
    enable_mem_search
    echo ""
    echo "── 真跑:sudo 提权 + localdb key-scan(主人亲自输 sudo 密码;脚本/桥不读不存密码)──"
    echo "   预计 ≈12 分钟,期间微信零扰动;单次批处理,扫完即退零常驻。"
    scan_started="$(date '+%F %T')"
    scan_rc=0
    set +e
    sudo env HOME="$HOME" MYIA_HOME="$MYIA_HOME" PYTHONPATH="$COMPONENT_ROOT" \
      "$PYTHON_BIN" -m wechat_bridge localdb key-scan --json
    scan_rc=$?
    set -e
    scan_ended="$(date '+%F %T')"
    echo "── 扫描应答 exit=$scan_rc(起 $scan_started / 止 $scan_ended)──"
    # 属主归还兜底:对不存在目录静默跳过;失败只警告,绝不遮掩扫描退出码。
    if ! sudo chown -R "$(id -u):$(id -g)" "$LOCALDB_DIR" 2>/dev/null; then
      if [[ -d "$LOCALDB_DIR" ]]; then
        echo "⚠ 属主归还兜底失败(sudo 会话内组件侧已自动归还属主,通常无碍;" \
             "手跑: sudo chown -R \"$(id -u):$(id -g)\" \"$LOCALDB_DIR\")" >&2
      fi
    fi
    run_probe "扫描后"
    case "$scan_rc" in
      0)
        echo "✅ exit 0:全量命中,keys.json 已落数据根私有区(600,属主已归还)——localdb query 一步可闭环(AC7)"
        ;;
      21)
        echo "⭕ exit 21 key_unavailable:诚实拒绝/零命中/部分命中/内核拒——非脚本故障"
        echo "   (hardened runtime 下 root 亦可能被内核拒;如实预告与回落路径见脚本头注与 research §5)"
        ;;
      10)
        echo "⚠ exit 10:微信进程不在(扫描中途退出?)——重启微信登录后可重扫"
        ;;
      20)
        echo "⚠ exit 20:db_storage 定位失败——确认微信曾登录并产生本地数据"
        ;;
      *)
        echo "⚠ exit $scan_rc:见 design §6 错误码表与上方 JSON 应答"
        ;;
    esac
    echo ""
    echo "收尾还原提示(mem_search_enabled 扫完即关,design §7 缺省关口径;localdb query 消费 keys.json 不读该开关,还原不影响查询):"
    if [[ -f "$CONFIG_BACKUP" ]]; then
      echo "  cp \"$CONFIG_BACKUP\" \"$CONFIG_FILE\"   # 恢复扫描前原配置(含开启前其余键)"
    fi
    echo "  echo '{}' > \"$CONFIG_FILE\"            # 或回全缺省即关(design §7 缺文件可用)"
    exit "$scan_rc"
    ;;
  *)
    usage
    die "未知参数: $MODE" 2
    ;;
esac
