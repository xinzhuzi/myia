#!/usr/bin/env bash
#
# install-keyscanner.sh — wechat-bridge 密钥收集器 setuid 自愈件安装器
# (task 10-13-wechat-key-subsystem;主人令 2026-10-13「固化成代码」)
#
# 【职责】把组件 native/collector.c 构建出的收集器二进制安装为
#   <数据根>/wechat-localdb/bin/keyscanner(root:staff,4750)——此后桥的
#   localdb key-scan 与密钥自愈钩子零 sudo 运行(setuid 件自提权,只读
#   mach 扫描;一次安装,长期自愈)。
#
# 【威胁模型(如实,不包装)】
#   - keyscanner 是 setuid root 的**只读**收集器:task_for_pid /
#     mach_vm_region / mach_vm_read / mach_vm_deallocate 四个只读 mach
#     调用,零写零注入零 exec(argv 白名单=pid,候选恒走 stdout;
#     守卫测试 tests/wechat-bridge/test_localdb_key.py 钉死源码)。
#   - 4750 root:staff = 仅本机用户组可执行;预期形态是**单用户本机**
#     (用户读自己微信的内存)。多用户机器上,staff 组成员可用它对任意
#     pid 做同款只读模式扫描(hex 串/salt 邻域形态候选,非任意内存转储)
#     ——这是已知的、接受的边界;不接受该边界的机器不要安装本件,
#     桥保持 sudo 单次批处理形态(不装此件即零 setuid 面)。
#   - 卸载:sudo rm <数据根>/wechat-localdb/bin/keyscanner 即回归
#     「未安装=保持现状」语义(桥自动回落 key_unavailable + 一键脚本指引)。
#
# 【用法】(须 root;一键脚本 scripts/wechat-bridge-d4-keyscan.sh 首段即此形态)
#   sudo env HOME="$HOME" MYIA_HOME="${MYIA_HOME:-…}" \
#     bash plugins/wechat-bridge/native/install-keyscanner.sh
#
# 【退出码】0 装好(或已装且校验同源);1 构建失败/安装失败;2 环境/用法错。
set -euo pipefail

NATIVE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPONENT_ROOT="$(cd "$NATIVE_DIR/.." && pwd)"
COLLECTOR_SRC="$NATIVE_DIR/collector.c"
DATA_ROOT="${MYIA_HOME:-$HOME/Library/Application Support/MYIA}"
KEYSCANNER_DIR="$DATA_ROOT/wechat-localdb/bin"
KEYSCANNER="$KEYSCANNER_DIR/keyscanner"

die() { echo "✗ $1" >&2; exit "${2:-1}"; }

[[ "$(uname -s)" == "Darwin" ]] || die "非 darwin(mach 只读收集器仅 macOS)" 2
[[ -f "$COLLECTOR_SRC" ]] || die "缺收集器源码: $COLLECTOR_SRC" 2
[[ "$(id -u)" == "0" ]] || die "须 root 运行(sudo bash $0;一键脚本首段代跑)" 2

# 构建到组件 bin/(首用编译的同一落点;不可写则退临时目录——装机只取二进制)
BUILD_OUT="$COMPONENT_ROOT/bin/collector"
mkdir -p "$(dirname "$BUILD_OUT")" 2>/dev/null || true
if ! touch "$BUILD_OUT.probe" 2>/dev/null; then
  BUILD_OUT="$(mktemp -t keyscanner_build)"
  echo "⚠ 组件 bin/ 不可写,构建退至临时件: $BUILD_OUT"
else
  rm -f "$BUILD_OUT.probe"
fi
CC_BIN="$(command -v cc || true)"
[[ -n "$CC_BIN" ]] || die "缺 cc(Xcode Command Line Tools):xcode-select --install 后重试" 1
echo "── 构建 collector($CC_BIN -O2)──"
"$CC_BIN" -O2 -o "$BUILD_OUT" "$COLLECTOR_SRC" || die "编译失败: $COLLECTOR_SRC" 1

# 安装:私有区目录 700 属主归还发起用户;二进制 root:staff 4750
echo "── 安装 setuid 件 → $KEYSCANNER ──"
SUDO_UID_V="${SUDO_UID:-}"; SUDO_GID_V="${SUDO_GID:-}"
mkdir -p "$KEYSCANNER_DIR"
chmod 700 "$KEYSCANNER_DIR"
if [[ -n "$SUDO_UID_V" && -n "$SUDO_GID_V" ]]; then
  chown -R "$SUDO_UID_V:$SUDO_GID_V" "$DATA_ROOT/wechat-localdb" 2>/dev/null || true
fi
install -o root -g staff -m 4750 "$BUILD_OUT" "$KEYSCANNER" \
  || die "install 失败(root:staff 4750): $KEYSCANNER" 1

# 就地校验:形状(属主/权限)+ 可执行
MODE="$(stat -f '%Sp' "$KEYSCANNER")"
OWNER="$(stat -f '%Su:%Sg' "$KEYSCANNER")"
[[ "$OWNER" == "root:staff" ]] || die "属主不符: $OWNER(预期 root:staff)" 1
[[ "$MODE" == *4750* ]] || die "权限不符: $MODE(预期 4750)" 1
echo "✅ keyscanner 已装: $KEYSCANNER($OWNER $MODE)"
echo "   此后 localdb key-scan / 密钥自愈零 sudo(收集器自提权,只读单遍);"
echo "   卸载即回归现状: sudo rm '$KEYSCANNER'"
exit 0
