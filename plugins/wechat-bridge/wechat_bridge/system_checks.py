"""系统事实检查器(探针的原料;全部**只读**,零前台扰动)。

静默铁律(prd 红线 4)在本模块的落法:

- 进程存在性 = ``pgrep -x WeChat``(只查进程表);
- 版本号 = ``plistlib`` 直读 ``/Applications/WeChat.app/Contents/Info.plist``
  (纯文件读;不走 ``defaults`` 子进程也不碰 app 运行态);
- AX 权限 = ``AXIsProcessTrusted``(ctypes 直呼 ApplicationServices;该 API
  **永不弹框不抢焦点**——弹框语义在 ``AXIsProcessTrustedWithOptions`` 的
  prompt 选项,本桥不碰它);
- 主窗口 = ``CGWindowListCopyWindowInfo``(pyobjc Quartz;纯窗口列表快照,
  不激活不枚举 AX 树);pyobjc 缺位 → ``unknown`` 如实上报,不臆测;
- 本地库落盘 = 纯目录存在性 + 计数(只看形状,不进库不碰密钥材料)。

每个检查器都是模块级函数 = 单测的注入点(tests 全 mock,CI 无微信全绿)。
"""

from __future__ import annotations

import plistlib
import subprocess
from pathlib import Path
from typing import Any

from .codes import TIMEOUT, BridgeError

__all__ = [
    "CHECK_TIMEOUT_SECONDS",
    "WECHAT_BUNDLE_PATH",
    "WECHAT_PROCESS_NAME",
    "WECHAT_OWNER_NAMES",
    "wechat_process_running",
    "wechat_version",
    "ax_permission_trusted",
    "wechat_ax_node_count",
    "wechat_main_window_open",
    "localdb_storage_accounts",
    "localdb_key_available",
    "WECHAT_FILES_ROOT",
]

#: 微信进程名(pgrep -x 精确匹配;2026-10-11 本机实测形态)。
WECHAT_PROCESS_NAME = "WeChat"
#: 微信窗口属主名(CGWindowList kCGWindowOwnerName 实测两种形态:zh-CN 系统为
#: 「微信」,en 系统为 "WeChat"——只匹配后者会把 zh-CN 系统的窗口态恒判 False,
#: 2026-10-11 实测踩中并修正)。pixel 层窗口定位同源对账。
WECHAT_OWNER_NAMES = ("微信", "WeChat")
#: 微信 app 缺省安装位(版本号读取;非 guessing——装在别处时如实 unknown)。
WECHAT_BUNDLE_PATH = Path("/Applications/WeChat.app")
#: 本地库数据根(prd Notes/research §7.1 实测布局;只读定位用)。
WECHAT_FILES_ROOT = (
    Path.home()
    / "Library"
    / "Containers"
    / "com.tencent.xinWeChat"
    / "Data"
    / "Documents"
    / "xwechat_files"
)
#: 单个检查子进程的超时上限(§6 exit 30 的挂点;秒,模块常量不设配置口)。
CHECK_TIMEOUT_SECONDS = 10.0


def _run_command(argv: list[str], timeout: float = CHECK_TIMEOUT_SECONDS) -> subprocess.CompletedProcess[bytes]:
    """带超时 kill 兜底的子进程运行(weixin.py ``run_bridge_command`` 同构的
    同步版;超时 → :class:`BridgeError`(exit 30 timeout)。"""
    try:
        return subprocess.run(  # noqa: S603 - argv 白名单内字面量,无外壳
            argv,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            TIMEOUT,
            f"检查子进程超时({' '.join(argv[:2])}…,{timeout:.0f}s 未退出,已 kill)",
            fix_hint="重试;持续超时说明系统层挂起,先查进程表",
        ) from exc


def wechat_process_running() -> bool:
    """微信进程存在性(``pgrep -x``;只查进程表,零窗口操作)。"""
    result = _run_command(["pgrep", "-x", WECHAT_PROCESS_NAME])
    return result.returncode == 0


def wechat_version() -> str | None:
    """微信版本号(plistlib 直读 Info.plist;缺位/不可读 → None 如实)。"""
    plist = WECHAT_BUNDLE_PATH / "Contents" / "Info.plist"
    if not plist.is_file():
        return None
    try:
        with plist.open("rb") as handle:
            data = plistlib.load(handle)
    except (OSError, plistlib.InvalidFileException):
        return None
    version = data.get("CFBundleShortVersionString")
    return str(version) if version else None


def ax_permission_trusted() -> bool | None:
    """辅助功能权限自检(``AXIsProcessTrusted``,无弹框语义)。

    Returns:
        True/False = 权限在/缺;None = 判定不可及(framework 加载失败,
        非 darwin 等)——**unknown 如实上报**,不把「测不了」伪装成结论。
    """
    try:
        import ctypes
    except ImportError:  # pragma: no cover - CPython 恒有 ctypes,防御性
        return None
    if not sys_darwin():
        return None
    try:
        framework = ctypes.CDLL(
            "/System/Library/Frameworks/ApplicationServices.framework/"
            "ApplicationServices"
        )
    except OSError:
        return None
    framework.AXIsProcessTrusted.restype = ctypes.c_bool
    framework.AXIsProcessTrusted.argtypes = []
    return bool(framework.AXIsProcessTrusted())


def sys_darwin() -> bool:
    """平台判定(独立小函数 = 单测注入点)。"""
    import sys

    return sys.platform == "darwin"


def screen_recording_granted() -> bool | None:
    """屏幕录制 TCC 授权检测(像素链读路径的真实前置;2026-10-12 勘误引入)。

    用 CGWindowListCreateImage 截主屏 10x10:返回 None = 无屏幕录制权限
    (TCC 拒绝的实锤形状);出图(含全黑,暗屏/锁屏误判归运行时 pixel 黑图
    fix_hint,不在探针层猜)视为已授权。非 darwin 平台返回 None(不判)。
    """
    if not sys_darwin():
        return None
    try:
        import Quartz

        img = Quartz.CGWindowListCreateImage(
            Quartz.CGRectMake(0, 0, 10, 10),
            Quartz.kCGWindowListOptionOnScreenOnly,
            Quartz.kCGNullWindowID,
            Quartz.kCGWindowImageDefault,
        )
        if img is None:
            return False
        return True
    except Exception:
        return None


def wechat_ax_node_count(*, runner=None) -> int | None:
    """微信进程 AX 树节点计数 = **全部窗口子树的深度枚举节点数**取最大
    (只读 osascript 查询;task 10-14-wechat-send-text design §D-1/§J-22;
    0.8.1 修正)。

    **不绑 ``window 1``**(§J-22:多窗时 z-order 首窗未必主窗)且**不直查
    第一层 count**:真机 dry-run 实证(/tmp/wxsend-e2e/axwalk2-out.txt)
    4.1.15 窗口直查 UI elements 恒 ~4(AXGroup + 标题栏钮),Qt 命名树挂
    AXGroup 下深层——计数必须 BFS 逐层枚举(节点预算上限 400,门开实测
    ~122)。

    判据消费方(axui.probe_wechat_ax / doctor):>5 = 门开;≤5 = closed
    (Qt AX 门未开,REV 判据);脚本失败/进程不在/非整数 → None(unknown
    如实)。

    probe 副作用如实注记:本查询即一次无障碍查询,自然触发 QNSView
    activateQtAccessibility(REV:20-24,微信自身行为,非前台扰动)。
    """
    script = (
        'tell application "System Events"\n'
        '  repeat with pname in {"微信", "WeChat"}\n'
        "    try\n"
        "      tell process (pname as text)\n"
        "        set maxCount to 0\n"
        "        repeat with w in windows\n"
        "          set wRef to contents of w\n"
        "          set total to 0\n"
        "          set theQueue to {wRef}\n"
        "          set budget to 400\n"
        "          repeat while (count of theQueue) > 0 and budget > 0\n"
        "            set nextQueue to {}\n"
        "            repeat with elem in theQueue\n"
        "              try\n"
        "                set kids to UI elements of elem\n"
        "              on error\n"
        "                set kids to {}\n"
        "              end try\n"
        "              repeat with kid in kids\n"
        "                if budget > 0 then\n"
        "                  set total to total + 1\n"
        "                  set budget to budget - 1\n"
        "                  copy kid to end of nextQueue\n"
        "                end if\n"
        "              end repeat\n"
        "            end repeat\n"
        "            set theQueue to nextQueue\n"
        "          end repeat\n"
        "          if total > maxCount then set maxCount to total\n"
        "        end repeat\n"
        "        return maxCount\n"
        "      end tell\n"
        "    end try\n"
        "  end repeat\n"
        "end tell\n"
    )
    run = runner if runner is not None else _run_command
    try:
        result = run(["osascript", "-e", script])
    except BridgeError:
        return None  # 超时族 → 探测不可及(unknown),不拦状态查询
    if result.returncode != 0:
        return None
    try:
        return int(result.stdout.decode("utf-8", "replace").strip())
    except ValueError:
        return None


def wechat_main_window_open() -> bool | None:
    """微信主窗口在否(CGWindowList 全量快照按属主过滤;零激活零枚举)。

    「在」的语义(2026-10-11 D2 像素链实测定论后修订):CGWindowList 在册
    即真——**ordered-off(托盘/后台)窗口同样可被 ``screencapture -l`` 截出
    完整合成帧**(出图/黑图/失败三态判定的「出图」,证据
    research/pixel-chain-e2e.md),像素读通道不要求窗口 ordered-on。

    Returns:
        True = 至少一个属主为 微信/WeChat 的窗口(含 ordered-off);
        False = 零窗口;None = 判定不可及(pyobjc 缺位/非 darwin)→ unknown 如实。
    """
    if not sys_darwin():
        return None
    try:
        import Quartz  # pyobjc;仓库 venv 在场,装机态属组件可选依赖
    except ImportError:
        return None
    try:
        window_list = Quartz.CGWindowListCopyWindowInfo(
            Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID
        )
    except Exception:  # noqa: BLE001 - 窗口快照失败按不可及处理,不臆测
        return None
    for window in window_list or []:
        owner = window.get(Quartz.kCGWindowOwnerName)
        if owner in WECHAT_OWNER_NAMES:
            return True
    return False


def localdb_storage_accounts(root: Path | None = None) -> int | None:
    """本地库落盘定位(纯目录计数:带 ``db_storage/`` 的账号目录数)。

    只看目录形状,不进库、不碰密钥材料(prd 红线 6:证据只留形状)。
    数据根本身缺位 → None(定位失败,§6 exit 20 的原料);有根无账号 → 0。
    """
    base = root if root is not None else WECHAT_FILES_ROOT
    if not base.is_dir():
        return None
    count = 0
    for child in base.iterdir():
        if child.is_dir() and (child / "db_storage").is_dir():
            count += 1
    return count


def localdb_key_available() -> bool:
    """本地库密钥可用性(Phase E1 真判据:验证通过的密钥缓存在场即真)。

    判据 = 数据根私有区 ``wechat-localdb/keys.json``(:data:`LOCALDB_KEYS_REL_PATH`,
    600 权限)存在且含至少一条验证通过的 key——该缓存**只在** :func:
    `wechat_bridge.localdb.acquire_key` 全量校验命中时落盘,故本检查零成本
    (一个小文件存在性)且不谎报。E1 实测(2026-10-11):零内存途径 0 命中
    → 缓存恒缺省 → False 如实(D4 待主人裁决)。
    """
    from .config import LOCALDB_KEYS_REL_PATH, myssia_home

    path = myssia_home() / LOCALDB_KEYS_REL_PATH
    if not path.is_file():
        return False
    try:
        import json

        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return isinstance(raw, dict) and bool(raw)


def check_summary(value: Any) -> str:
    """检查值 → checks 字典的字符串态(ok/fail/unknown;probe 载荷形状)。"""
    if value is True:
        return "ok"
    if value is False:
        return "fail"
    if value is None:
        return "unknown"
    return str(value)
