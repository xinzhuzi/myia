#!/usr/bin/env bash
#
# wechat-bridge-d4-keyscan.sh — 微信桥 D4 密钥扫描一键脚本 v2
# (task 10-13-wechat-key-subsystem;主人令 2026-10-13「固化成代码」。
#  v1 = 2026-10-12 task 10-11-wechat-ui-bridge AC7,固化 research/
#  d4-memscan-e2e.md §5;v2 换轨组件 0.4.0 管道:C 收集器 + sqlcipher
#  验证 + setuid 自愈件,EXIT trap/还原提示/chown 兜底全套保留)
#
# 【机理】单次只读批处理,不是常驻服务:
#   0. 前置自检(darwin / 仓库 venv / 组件 / 微信进程在场 / 本地库数据根 /
#      收集器可得性)——任一缺位按 §6 错误码族诚实退出,不消耗 sudo 密码;
#   1. 【v2 首段】安装 setuid 自愈件(一次 root):
#      sudo native/install-keyscanner.sh 把组件 native/collector.c 构建出的
#      收集器装为 <数据根>/wechat-localdb/bin/keyscanner(root:staff,4750)
#      ——此后扫描/自愈零 sudo(收集器自提权,只读 mach 四调用,零 exec,
#      威胁模型见安装器头注);已在位且形状合规则跳过(零 root);
#   2. 扫描前跑一次 `wechat-bridge --probe` 对照基线(state / mem_search_enabled);
#   3. 显式开启 mem_search_enabled(主人运行本脚本 = 主人显式开启,design §4;
#      其余配置键原样保留,原配置自动备份为 config.json.pre-keyscan);
#   4. 【v2 中段】走组件 0.4.0 新管道:keyscanner 在位 → 免 sudo 直接
#      `localdb key-scan`(C 收集器三模式宽收集:hex 裸串/salt 邻域/
#      x'hex' 包裹 → 候选文件私有区临时件 → 熵筛 ≥3.5bits/B → 8 并发
#      sqlcipher 试开(参数变体 4 组)→ page1 离线 HMAC 交叉验证 →
#      全量命中才落 keys.json(600));keyscanner 未装成(主人拒 sudo 等)
#      → 回落 v1 形态:sudo 提权一次批处理(同管道,收集器走组件 bin/
#      首用自动编译)。扫完进程即退,零常驻、零轮询、零重试;零写内存、
#      零注入、零调试器附加、零重签名(守卫测试钉死)。
#   5. 扫描退出码 rc 暂存;尾部 sudo chown 属主归还兜底(仅 sudo 路径需要;
#      免 sudo 路径产物本就是用户属主)——chown 结果**不遮掩**扫描退出码,
#      (exit $rc) 原样奉还;
#   6. 扫描后再跑一次 probe 对照;收尾打印 mem_search_enabled 还原命令
#      (是否还原由主人决定;注意:还原后 setuid 自愈休眠——自愈钩子
#      同走配置门,重开本脚本或手写 true 即恢复)。
#
# 【边界】
#   - sudo 密码由主人按日常习惯亲自输入;本脚本与桥、子代理全程不索要、
#     不读、不存密码。
#   - 诚实语义:零命中/部分命中/内核拒绝 = exit 21 key_unavailable——诚实,
#     不是脚本故障。如实预告:微信为 hardened runtime 签名,XNU 对
#     restricted 目标的 task_for_pid 要求调用方持调试类 entitlement,root
#     亦可能被拒(KERN_FAILURE)——该拒绝即「红线内(不重签/不 lldb)此路
#     在本机不可达」的如实信号,应答原样上报 mach 码。
#   - setuid 件威胁模型(如实):单用户本机 = 用户读自己微信内存;多用户
#     机器上 staff 组成员可借它做同款只读模式扫描——不接受则不装,
#     sudo rm <数据根>/wechat-localdb/bin/keyscanner 即回归现状。
#   - 对 HOME 的确定性加固:sudo env 显式钉 HOME="$HOME"(组件数据根解析
#     按 Path.home(),sudo 1.9.x 缺省 env_reset 会重置为 /var/root,不钉则
#     sudo 内必 exit 20 db_not_found);v2 同款钉 MYIA_HOME。
#
# 【预计时长】C 收集器全进程单遍(分钟级,2026-10-13 /tmp 同型件真跑
#   验证)+ sqlcipher 试开(熵筛后候选数 × 变体 4 组,8 并发);
#   期间微信零扰动、零前台操作。
#
# 【用法】
#   scripts/wechat-bridge-d4-keyscan.sh            # 真跑(首跑会请求一次 sudo 密码装 setuid 件)
#   scripts/wechat-bridge-d4-keyscan.sh --dry-run  # 不提权自校验:前置检查
#     (缺位只警告不阻断)+ 缺省关路径冒烟(临时 MYIA_HOME,预期诚实
#     exit 21 key_unavailable)+ 打印真跑将执行的命令
#
# 【退出码】0 命中;10 微信不在;20 数据根缺位;21 密钥不可得(诚实拒绝/
#   零命中/部分命中/内核拒/非 darwin);2 用法/环境错;其余见 design §6。

set -euo pipefail

SMOKE_TMP=""
SCAN_STARTED=""
# 复审 low 收口(2026-10-12,v1 已验):中断路径(Ctrl-C/被杀)收尾段不会
# 执行——开关合并写之后若被中断,真配置停留在 mem_search_enabled=true 且
# 用户未被告知还原命令;EXIT trap 补一条中断还原提示(收尾段正常走时它
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
INSTALLER="$COMPONENT_ROOT/native/install-keyscanner.sh"
SCRIPT_SELF="$(basename "${BASH_SOURCE[0]}")"

MODE="${1:-run}"

MYIA_HOME="${MYIA_HOME:-$HOME/Library/Application Support/MYIA}"
CONFIG_DIR="$MYIA_HOME/wechat-bridge"
CONFIG_FILE="$CONFIG_DIR/config.json"
CONFIG_BACKUP="$CONFIG_FILE.pre-keyscan"
LOCALDB_DIR="$MYIA_HOME/wechat-localdb"
KEYSCANNER="$LOCALDB_DIR/bin/keyscanner"
WECHAT_FILES_ROOT="$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files"

# keyscanner 在位判据(形状级:可执行 + setuid 位 + root:staff 属主)
keyscanner_ok() {
  [[ -x "$KEYSCANNER" ]] || return 1
  [[ "$(stat -f '%Sp' "$KEYSCANNER" 2>/dev/null)" == *4750* ]] || return 1
  [[ "$(stat -f '%Su:%Sg' "$KEYSCANNER" 2>/dev/null)" == "root:staff" ]] || return 1
  return 0
}

usage() {
  echo "用法: scripts/$SCRIPT_SELF [--dry-run]" >&2
  echo "  (无参)      真跑:首跑 sudo 一次装 setuid 自愈件(此后免 sudo)+ 新管道扫描" >&2
  echo "  --dry-run   不提权自校验:前置检查 + 缺省关路径冒烟 + 打印真跑命令" >&2
}

die() { echo "✗ $1" >&2; exit "$2"; }

# —— 前置自检:real 模式缺位即诚实退出(省一次无谓的 sudo 密码输入);
#    dry-run 模式只警告不阻断(自校验重点是缺省关冒烟)——
preflight() {
  local hard="$1"
  local ok=1
  [[ "$(uname -s)" == "Darwin" ]] || { echo "✗ 非 darwin(mach 只读收集器仅 macOS,组件门③同口径)" >&2; ok=0; }
  [[ -x "$PYTHON_BIN" ]] || { echo "✗ 缺 $PYTHON_BIN(仓库 .venv;铁律勿往仓库 venv 装包,缺环境先建)" >&2; ok=0; }
  [[ -f "$COMPONENT_ROOT/wechat_bridge/__main__.py" ]] || { echo "✗ 缺组件 $COMPONENT_ROOT/wechat_bridge" >&2; ok=0; }
  [[ -f "$COMPONENT_ROOT/native/collector.c" ]] || { echo "✗ 缺收集器源码 $COMPONENT_ROOT/native/collector.c(0.4.0 管道前置)" >&2; ok=0; }
  # 收集器可得性:keyscanner 已装 / 组件 bin/ 已编 / cc 可用,三者其一即够
  if ! keyscanner_ok \
     && [[ ! -x "$COMPONENT_ROOT/bin/collector" ]] \
     && ! command -v cc >/dev/null 2>&1; then
    echo "✗ 收集器不可得:keyscanner 未装、组件 bin/collector 未编、cc 缺位(xcode-select --install)" >&2
    ok=0
  fi
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
    echo "✓ 前置自检通过:darwin / venv / 组件(含收集器)/ 微信进程 / 本地库数据根"
  fi
}

run_probe() {
  local label="$1" out rc=0
  out="$(MYIA_HOME="$MYIA_HOME" PYTHONPATH="$COMPONENT_ROOT" \
    "$PYTHON_BIN" -m wechat_bridge --probe 2>/dev/null)" || rc=$?
  echo "── probe($label): exit=$rc ──"
  if [[ -n "$out" ]]; then printf '%s\n' "$out"; else echo "(probe 无 stdout 应答)"; fi
}

# —— 【v2 首段】setuid 自愈件安装(一次 root;已在位即跳过零 root)——
install_keyscanner() {
  if keyscanner_ok; then
    echo "✓ setuid 自愈件已在位: $KEYSCANNER(root:staff 4750)——免 sudo 扫描/自愈已激活"
    return 0
  fi
  echo "── 安装 setuid 自愈件(一次 root;此后扫描/自愈零 sudo)──"
  echo "   主人亲自输 sudo 密码;脚本/桥不读不存密码。"
  if sudo env HOME="$HOME" MYIA_HOME="$MYIA_HOME" bash "$INSTALLER"; then
    keyscanner_ok || die "安装器声称成功但形状校验不过: $KEYSCANNER" 2
    echo "✓ setuid 自愈件已装(扫描/自愈此后免 sudo)"
    return 0
  fi
  echo "⚠ setuid 件未装成(主人拒 sudo/安装器失败)——回落 v1 形态:整段 sudo 扫描" >&2
  return 1
}

# —— 显式开启开关:合并写(其余配置键原样保留),原配置先备份;
#    既有配置非法 JSON 时诚实中止(load_config 本会 fail-fast exit 2,
#    不静默覆盖主人的文件)——
enable_mem_search() {
  # 0.4.1 复审 low 修复:置位无条件化(首跑无既有配置的合并写后中断,
  # EXIT trap 同样给还原提示;原先只在备份分支置位)。
  SCAN_STARTED=1
  if [[ -f "$CONFIG_FILE" ]]; then
    cp "$CONFIG_FILE" "$CONFIG_BACKUP"
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
    echo "── 真跑将执行(v2:首段装 setuid 件 + 中段新管道;HOME/MYIA_HOME 钉住加固)──"
    echo "  1) 装 setuid 件(一次): sudo env HOME=\"\$HOME\" MYIA_HOME=\"$MYIA_HOME\" \\"
    echo "                            bash $INSTALLER   # → $KEYSCANNER(root:staff 4750)"
    echo "  2) probe(前)      : MYIA_HOME=\"$MYIA_HOME\" \"$PYTHON_BIN\" -m wechat_bridge --probe"
    echo "  3) 开关合并写      : mem_search_enabled=true → $CONFIG_FILE(备份 $CONFIG_BACKUP)"
    echo "  4) 扫描(新管道)  : MYIA_HOME=\"$MYIA_HOME\" PYTHONPATH=\"$COMPONENT_ROOT\" \\"
    echo "                         \"$PYTHON_BIN\" -m wechat_bridge localdb key-scan --json   # keyscanner 在位免 sudo"
    echo "     (未装成时回落): sudo env HOME=\"\$HOME\" MYIA_HOME=\"$MYIA_HOME\" \\"
    echo "                         PYTHONPATH=\"$COMPONENT_ROOT\" \\"
    echo "                         \"$PYTHON_BIN\" -m wechat_bridge localdb key-scan --json"
    echo "  5) 属主兜底(仅 sudo 路径): sudo chown -R \"\$(id -u):\$(id -g)\" \"$LOCALDB_DIR\"(rc 不被吞)"
    echo "  6) probe(后) + 收尾还原提示"
    exit 0
    ;;
  run|"")
    preflight "hard"
    install_keyscanner || true
    run_probe "扫描前"
    enable_mem_search
    echo ""
    SCAN_RC=0
    SCAN_SUDO=""
    if keyscanner_ok; then
      echo "── 真跑:keyscanner 免 sudo + localdb key-scan(0.4.0 新管道;收集器自提权只读单遍)──"
      echo "   期间微信零扰动;单次批处理,扫完即退零常驻。"
      scan_started="$(date '+%F %T')"
      set +e
      MYIA_HOME="$MYIA_HOME" PYTHONPATH="$COMPONENT_ROOT" \
        "$PYTHON_BIN" -m wechat_bridge localdb key-scan --json
      SCAN_RC=$?
      set -e
    else
      echo "── 真跑(回落 v1 形态):sudo 提权 + localdb key-scan(主人亲自输 sudo 密码;脚本/桥不读不存密码)──"
      echo "   期间微信零扰动;单次批处理,扫完即退零常驻。"
      SCAN_SUDO="1"
      scan_started="$(date '+%F %T')"
      set +e
      sudo env HOME="$HOME" MYIA_HOME="$MYIA_HOME" PYTHONPATH="$COMPONENT_ROOT" \
        "$PYTHON_BIN" -m wechat_bridge localdb key-scan --json
      SCAN_RC=$?
      set -e
    fi
    scan_ended="$(date '+%F %T')"
    echo "── 扫描应答 exit=$SCAN_RC(起 $scan_started / 止 $scan_ended)──"
    # 属主归还兜底(仅 sudo 路径需要;免 sudo 路径产物本就是用户属主):
    # 对不存在目录静默跳过;失败只警告,绝不遮掩扫描退出码。
    if [[ -n "$SCAN_SUDO" ]]; then
      if ! sudo chown -R "$(id -u):$(id -g)" "$LOCALDB_DIR" 2>/dev/null; then
        if [[ -d "$LOCALDB_DIR" ]]; then
          echo "⚠ 属主归还兜底失败(sudo 会话内组件侧已自动归还属主,通常无碍;" \
               "手跑: sudo chown -R \"$(id -u):$(id -g)\" \"$LOCALDB_DIR\")" >&2
        fi
      fi
    fi
    run_probe "扫描后"
    case "$SCAN_RC" in
      0)
        echo "✅ exit 0:全量命中,keys.json 已落数据根私有区(600)——localdb query 一步可闭环(AC7)"
        if keyscanner_ok; then
          echo "   setuid 自愈件在位:此后密钥轮换 → query 自动重取(须 mem_search_enabled 保持 true)"
        fi
        ;;
      21)
        echo "⭕ exit 21 key_unavailable:诚实拒绝/零命中/部分命中/内核拒——非脚本故障"
        echo "   (hardened runtime 下 root 亦可能被内核拒;如实预告与回落路径见脚本头注)"
        ;;
      10)
        echo "⚠ exit 10:微信进程不在(扫描中途退出?)——重启微信登录后可重扫" >&2
        ;;
      20)
        echo "⚠ exit 20:db_storage 定位失败——确认微信曾登录并产生本地数据" >&2
        ;;
      *)
        echo "⚠ exit $SCAN_RC:见 design §6 错误码表与上方 JSON 应答" >&2
        ;;
    esac
    echo ""
    echo "收尾还原提示(mem_search_enabled 扫完即关是缺省口径;但 setuid 自愈依赖它保持 true——"
    "还原后自愈休眠,重开本脚本或手写 true 即恢复;localdb query 消费 keys.json 不读该开关,已落密钥不受影响):"
    if [[ -f "$CONFIG_BACKUP" ]]; then
      echo "  cp \"$CONFIG_BACKUP\" \"$CONFIG_FILE\"   # 恢复扫描前原配置(含开启前其余键)"
    fi
    echo "  echo '{}' > \"$CONFIG_FILE\"            # 或回全缺省即关(design §7 缺文件可用)"
    echo "  sudo rm \"$KEYSCANNER\"                  # (可选)卸载 setuid 件即回归零 setuid 面"
    exit "$SCAN_RC"
    ;;
  *)
    usage
    die "未知参数: $MODE" 2
    ;;
esac
