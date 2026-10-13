"""内存密钥搜索(D4 豁免执行件;默认关,主人配置显式开启才生效)。

**0.4.0 管道重写**(task 10-13-wechat-key-subsystem;主人令 2026-10-13
「把获取这些密钥的方式全部固化成代码」):当日 /tmp/wxkey-c 临时件(真跑
验证)工程化——旧 Python 滑窗实现(32B 逐窗 × 逐候选 HMAC,复杂度
O(内存×库数))**退役删除**,替换为:

    C 收集器(native/collector.c,三模式宽收集)
      → 候选文件(数据根私有区临时件,600/700)
      → 熵预筛(≥3.5 bits/byte,剔除全零/文本窗)
      → 并行 sqlcipher 试开(8 并发 × 微信 4.x 参数变体 4 组)
      → 命中经 page1 离线 HMAC 交叉验证(keys.json 消费通路同款)
      → 全量命中才落 keys.json(600,与 E1 消费通路同位)

红线锚点与豁免口径(prd 红线 1/3、design §4;D4 豁免 = 主人 2026-10-11
「全部解决」令,执行边界按豁免令钉死):

- **只读**:对微信进程的内存读取全部在 C 收集器内,只做只读 mach 调用
  (``task_for_pid`` → ``mach_vm_region`` 枚举 → ``mach_vm_read`` 读段
  → ``mach_vm_deallocate`` 还缓冲);**禁写内存、禁注入、禁调试器附加、
  禁重签名**——守卫测试把写/注入/调试/exec 类 API 名单钉死在收集器源码
  之外(tests/wechat-bridge/test_localdb_key.py:本模块侧零 ctypes/mach,
  mach 逻辑只许活在 native/collector.c)。收集器 argv 白名单 = 目标 pid
  (纯数字),salt 清单走 stdin(桥侧从各库 page1 采集),候选恒走
  stdout——**零 exec、输出路径固定**,setuid 审计焦点即此。
- **单遍批处理**:收集器一次遍历扫完即退,零常驻、零轮询、零重试;扫描
  预算(候选库/盐库/段长上限)为收集器编译期常量,刻意不设配置面——
  预算即边界,边界不给人调。
- **三重门**(:func:`acquire_key_from_memory` 逐门校验):①主人 D4 豁免
  裁决在案(任务档 A4/「全部解决」令,归任务档文档承载);②配置显式
  开启(``<数据根>/wechat-bridge/config.json`` 的
  ``"mem_search_enabled": true``,缺省关);③提权在位(``task_for_pid``
  需 root:euid==0,或已安装 setuid 自愈件 ``<数据根>/wechat-localdb/
  bin/keyscanner``——root:staff 4750,native/install-keyscanner.sh 所装,
  威胁模型见该脚本头注)——不通过即拒,**绝不索要/使用密码**。
- **诚实语义**:扫不到 = 如实 exit 21 ``key_unavailable``;全部消息只
  承载形状(盐数/候选数/熵筛/试开次数/命中计数),密钥材料零落日志零
  入档(红线 6);命中 key 只落数据根私有区 ``wechat-localdb/keys.json``
  (600,落盘前经 page1 离线 HMAC 全量验证,查询一步闭合无须改码);
  候选临时件用后即清。
- **机制边界(如实预告,不包装)**:微信本机为 hardened runtime 签名
  (2026-10-11 codesign 实测 flags=0x10000(runtime)、无 get-task-allow),
  XNU 对 restricted 目标的 ``task_for_pid`` 要求调用方持调试类
  entitlement——**root 亦可能被拒(KERN_FAILURE)**;该拒绝 = 本红线内
  (不重签、不 lldb)此路在该机不可达的如实信号,原样上报,不做规避。
  2026-10-13 /tmp 三模式件真跑(本机 root)已证实可达,收集器逻辑照搬。
- **setuid 自愈**(:func:`self_heal_armed` / :func:`try_self_heal`):
  keyscanner 安装在位 + 配置门开时,localdb 查询链的密钥缺位/失效可零
  人工重取(见 wechat_bridge.localdb 自愈钩子);未安装 = 保持现状
  (key_unavailable + 一键脚本指引),零 setuid 面。自愈未闭合落
  带时间戳冷却戳(窗 = :data:`SELF_HEAL_COOLDOWN_SECONDS`,内含零重扫
  ——不可闭合态的失败退避,0.4.1 复审 medium 修复;损坏即忘却,
  绝不把自愈永久卡死;`localdb key-scan` / 一键脚本直连扫描入口,
  不受冷却门)。
- 扫描模式参考公开实现思路(0xlane/wechat-dump-rs 系 macOS 段、参考件
  wechat-mcp-macos 的校验配方),实现为本仓库自有零第三方依赖版本,
  **不拷上游代码**。
"""

from __future__ import annotations

import math
import os
import re
import shutil
import stat as stat_mod
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .codes import KEY_UNAVAILABLE, WECHAT_NOT_RUNNING, BridgeError
from .config import BridgeConfig, myssia_home
from .localdb import (
    KEY_SZ,
    LOCALDB_PRIVATE_DIR,
    _restore_owner_for_sudo,
    page1_targets,
    read_key_cache,
    verify_key_for_page,
    verify_key_mapping,
    write_key_cache,
)
from .system_checks import CHECK_TIMEOUT_SECONDS, WECHAT_PROCESS_NAME

__all__ = [
    "COLLECTOR_TIMEOUT_SECONDS",
    "ENTROPY_MIN_BITS_PER_BYTE",
    "KEYSCANNER_REL_PATH",
    "PARAM_SETS",
    "ScanReport",
    "SELF_HEAL_COOLDOWN_REL_PATH",
    "SELF_HEAL_COOLDOWN_SECONDS",
    "SQLCIPHER_TRY_TIMEOUT_SECONDS",
    "VERIFY_WORKERS",
    "acquire_key_from_memory",
    "entropy_bits_per_byte",
    "find_wechat_pids",
    "keyscanner_available",
    "keyscanner_path",
    "self_heal_armed",
    "self_heal_cooldown_path",
    "self_heal_cooldown_remaining",
    "try_open_with_sqlcipher",
    "try_self_heal",
]

# =====================================================================
# 管道常量(模块常量,非配置面;预算即边界,主人可改码但无键)
# =====================================================================

#: 熵预筛阈值(bits/byte;32B 高熵才可能是真钥匙,/tmp verify.py 已验配方)。
ENTROPY_MIN_BITS_PER_BYTE = 3.5
#: sqlcipher 试开并发数(/tmp verify.py 已验配方:8 并发)。
VERIFY_WORKERS = 8
#: 单次收集器子进程超时(秒;全进程单遍,给足余量)。
COLLECTOR_TIMEOUT_SECONDS = 1800.0
#: 单次 sqlcipher 试开超时(秒;/tmp verify.py 已验配方:15s)。
SQLCIPHER_TRY_TIMEOUT_SECONDS = 15.0
#: 数据根私有区内 setuid 自愈件落点(install-keyscanner.sh 所装)。
KEYSCANNER_REL_PATH = f"{LOCALDB_PRIVATE_DIR}/bin/keyscanner"
#: 自愈失败冷却窗(秒;复审 medium 修复:不可闭合态——微信改版零命中/
#: 部分命中/收集器超时——若不节流,每次 localdb query 都重触发全进程
#: 内存扫描(分钟级且用户无感),收集器预算 1800s 还会把失败形状从
#: exit 21 结构化 skip 拖成 bridge_timeout)。**模块常量非配置面**:
#: 预算即边界,边界不给人调;`localdb key-scan` CLI / 一键脚本直连扫描
#: 入口,不受此门。
SELF_HEAL_COOLDOWN_SECONDS = 1800.0
#: 自愈冷却戳落点(数据根私有区;内容 = 上次未闭合时间戳,零密钥材料)。
SELF_HEAL_COOLDOWN_REL_PATH = f"{LOCALDB_PRIVATE_DIR}/self_heal_cooldown.json"

#: 微信 4.x sqlcipher 参数变体 4 组(/tmp verify.py 已验配方;缺省组在前
#: ——与 E2 解密消费通路 ``PRAGMA key = "x'…'"`` 同参,命中即可直接消费)。
PARAM_SETS: list[tuple[str, ...]] = [
    (),  # sqlcipher4 缺省(= E2 消费通路参数)
    ("PRAGMA cipher_page_size = 1024;",),
    (
        "PRAGMA cipher_page_size = 4096; PRAGMA kdf_iter = 64000; "
        "PRAGMA cipher_hmac_algorithm = HMAC_SHA1;",
    ),
    ("PRAGMA cipher_compatibility = 3;",),
]

#: sqlcipher 试开命令(试开目标 = 首库文件;成功判据 = SELECT 计数应答)。
_SQLCIPHER_PROBE_SQL = "SELECT count(*) FROM sqlite_master;\n"


@dataclass
class ScanReport:
    """扫描形状报告(全部计数,零内容——红线 6;直接进 stdout 契约)。"""

    pids: list[int] = field(default_factory=list)
    salts: int = 0
    candidates: int = 0
    entropy_kept: int = 0
    sqlcipher_tries: int = 0
    sqlcipher_hits: int = 0
    canonical_verifies: int = 0

    def to_payload(self) -> dict[str, object]:
        """形状载荷(键序稳定;无任何密钥材料/进程内存内容)。"""
        return {
            "pids": list(self.pids),
            "salts": self.salts,
            "candidates": self.candidates,
            "entropy_kept": self.entropy_kept,
            "sqlcipher_tries": self.sqlcipher_tries,
            "sqlcipher_hits": self.sqlcipher_hits,
            "canonical_verifies": self.canonical_verifies,
        }


# =====================================================================
# 进程定位(只查进程表,零窗口操作——system_checks 同款纪律)
# =====================================================================


def find_wechat_pids(
    *, runner: Callable[[list[str]], "subprocess.CompletedProcess[bytes]"] | None = None
) -> list[int]:
    """微信主进程 pid 族(``pgrep -x WeChat``;只查进程表)。

    只扫主进程名精确匹配(Chromium helper/WeChatAppEx 不入扫——密钥在
    主进程登录链路持有;helper 面大而无谓,单遍批处理不烧预算)。
    """
    run = runner if runner is not None else _run_pgrep
    result = run(["pgrep", "-x", WECHAT_PROCESS_NAME])
    if result.returncode != 0:
        return []
    pids: list[int] = []
    for token in result.stdout.decode("ascii", "replace").split():
        if token.isdigit():
            pids.append(int(token))
    return pids


def _run_pgrep(argv: list[str]) -> "subprocess.CompletedProcess[bytes]":
    return subprocess.run(  # noqa: S603 - 字面量命令,无外壳
        argv, capture_output=True, timeout=CHECK_TIMEOUT_SECONDS, check=False
    )


# =====================================================================
# setuid 自愈件定位(install-keyscanner.sh 的消费面)
# =====================================================================


def keyscanner_path(*, data_root: Path | None = None) -> Path:
    """setuid 自愈件路径(<数据根>/wechat-localdb/bin/keyscanner)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / KEYSCANNER_REL_PATH


def keyscanner_available(*, data_root: Path | None = None) -> bool:
    """setuid 自愈件在位(可执行 + setuid 位;缺任一 = 未安装语义)。

    只看文件形状(存在/可执行/S_ISUID),不运行它——探针/自愈判据零成本。
    """
    path = keyscanner_path(data_root=data_root)
    try:
        mode = path.stat().st_mode
    except OSError:
        return False
    return bool(mode & stat_mod.S_IXUSR) and bool(mode & stat_mod.S_ISUID)


def _elevation_in_place(*, data_root: Path | None = None) -> bool:
    """提权在位:euid==0 或 setuid 自愈件已安装(门③判据)。"""
    return _current_euid_is_root() or keyscanner_available(data_root=data_root)


# =====================================================================
# C 收集器:构建解析 + subprocess(零 exec 白名单 argv;mock 接缝)
# =====================================================================


def _component_root() -> Path:
    """组件根(单测注入点;pip 装形态无 native/ 时如实报错)。"""
    return Path(__file__).resolve().parents[1]


def _cc_available() -> bool:
    """cc 在场性(首用自动编译的构建器;单测注入点)。"""
    return shutil.which("cc") is not None


def _compile_collector(source: Path, out_path: Path) -> None:
    """首用自动编译(cc -O2;argv 字面量,无外壳;失败结构化报错)。"""
    try:
        result = subprocess.run(  # noqa: S603 - 字面量命令,无外壳
            ["cc", "-O2", "-o", str(out_path), str(source)],
            capture_output=True,
            timeout=120.0,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"收集器编译超时(>120s,已 kill): {source.name}",
        ) from exc
    if result.returncode != 0 or not out_path.is_file():
        stderr_lines = len(result.stderr.splitlines())
        raise BridgeError(
            KEY_UNAVAILABLE,
            "收集器编译失败"
            f"(exit={result.returncode},stderr {stderr_lines} 行): {source.name}",
            fix_hint="cc 在场但编译不过 = 源码/工具链漂移;重装 Xcode CLT 或上报",
        )


def resolve_collector_binary(*, data_root: Path | None = None) -> tuple[Path, str]:
    """解析收集器二进制(优先序:setuid 自愈件 → 组件 bin/ 首用编译)。

    Returns:
        (二进制路径, 形态)——形态 ``keyscanner``(setuid 件,免 sudo)或
        ``component``(组件 bin/collector,首用自动编译;须本进程已提权)。

    Raises:
        BridgeError: exit 21——pip 装形态无 native 源码 / cc 缺位(带
            Xcode CLT 指引)/ 编译失败。
    """
    scanner = keyscanner_path(data_root=data_root)
    try:
        if scanner.stat().st_mode & stat_mod.S_IXUSR:
            return scanner, "keyscanner"
    except OSError:
        pass
    source = _component_root() / "native" / "collector.c"
    binary = _component_root() / "bin" / "collector"
    if binary.is_file() and os.access(binary, os.X_OK):
        return binary, "component"
    if not source.is_file():
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"收集器源码不在场(pip 装形态无 native/): {source}",
            fix_hint="key-scan 须组件目录形态(bin/ + native/ 随包整份);"
            "或经 pip_src 组件目录重装",
        )
    if not _cc_available():
        raise BridgeError(
            KEY_UNAVAILABLE,
            "收集器首用须编译,但 cc 不在场(Xcode Command Line Tools 缺装)",
            fix_hint="xcode-select --install 后重试;或跑一键脚本 "
            "scripts/wechat-bridge-d4-keyscan.sh(首段代装)",
        )
    binary.parent.mkdir(parents=True, exist_ok=True)
    _compile_collector(source, binary)
    return binary, "component"


def _run_collector_subprocess(
    argv: list[str], input_bytes: bytes
) -> "subprocess.CompletedProcess[bytes]":
    """收集器子进程缺省执行件(argv=[二进制, pid] 白名单,无外壳)。"""
    try:
        return subprocess.run(  # noqa: S603 - argv 白名单(本模块解析),无外壳
            argv,
            input=input_bytes,
            capture_output=True,
            timeout=COLLECTOR_TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"收集器超时(>{COLLECTOR_TIMEOUT_SECONDS:.0f}s,已 kill): {argv[0]}",
        ) from exc


CollectorRunner = Callable[[list[str], bytes], "subprocess.CompletedProcess[bytes]"]


def collect_candidates_file(
    binary: Path,
    pid: int,
    salt_hex_lines: list[str],
    *,
    data_root: Path | None = None,
    runner: CollectorRunner | None = None,
) -> tuple[Path, int]:
    """跑收集器单 pid,候选落数据根私有区临时文件(600/700)并返回(路径,行数)。

    候选文件 = 管道「候选文件」段的物化形态:收集器 stdout(路径固定)由
    桥侧写私有区临时件;盐清单(salt 采集归非提权桥侧)经 stdin 传入。
    临时件本函数不删——调用方用完负责清(try/finally)。
    """
    run = runner if runner is not None else _run_collector_subprocess
    result = run([str(binary), str(pid)], ("\n".join(salt_hex_lines) + "\n").encode())
    if result.returncode != 0:
        stderr_text = result.stderr.decode("utf-8", "replace")
        kern_note = (
            "(task_for_pid 被拒——hardened runtime 目标对无调试 entitlement "
            "调用方恒拒,root 亦可能被拒;红线内不规避,如实上报)"
            if "task_for_pid" in stderr_text
            else ""
        )
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"收集器失败(exit={result.returncode}): pid={pid} {kern_note}",
            fix_hint="exit=1 且 task_for_pid 被拒 = 内存读取途径在该机不可达的"
            "如实信号;勿重试勿变通;其余 exit 码看 stderr 诊断形状",
        )
    scan_dir = myssia_home() if data_root is None else data_root
    scan_dir = scan_dir / LOCALDB_PRIVATE_DIR / "scan"
    scan_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(scan_dir, 0o700)
    _restore_owner_for_sudo(scan_dir)
    candidates_path = scan_dir / f"candidates-{pid}.txt"
    candidates_path.write_bytes(result.stdout)
    os.chmod(candidates_path, 0o600)
    _restore_owner_for_sudo(candidates_path)
    lines = sum(1 for line in result.stdout.splitlines() if line.strip())
    return candidates_path, lines


# =====================================================================
# 验证管道:熵筛 + 并行 sqlcipher 试开 + page1 交叉验证(纯函数/mock 接缝)
# =====================================================================


def entropy_bits_per_byte(raw: bytes) -> float:
    """Shannon 熵(bits/byte;/tmp verify.py 已验配方)。"""
    if not raw:
        return 0.0
    counts = [0] * 256
    for b in raw:
        counts[b] += 1
    n = len(raw)
    ent = 0.0
    for c in counts:
        if c:
            p = c / n
            ent -= p * math.log2(p)
    return ent


SqlcipherRunner = Callable[[list[str], bytes], "subprocess.CompletedProcess[bytes]"]


def try_open_with_sqlcipher(
    db_path: Path,
    key_hex: str,
    *,
    runner: SqlcipherRunner | None = None,
) -> tuple[str | None, int]:
    """单候选试开(参数变体 4 组依序,命中即止)。

    Returns:
        (命中参数组标签,None=未开;sqlcipher 实际调用次数)——标签
        ``default`` 或分号拼接的 PRAGMA 串(/tmp verify.py 同款)。
    """
    run = runner if runner is not None else _run_sqlcipher_subprocess
    invocations = 0
    for extra in PARAM_SETS:
        sql = f"PRAGMA key = \"x'{key_hex}'\";\n" + "\n".join(extra) + "\n" + _SQLCIPHER_PROBE_SQL
        result = run(["sqlcipher", str(db_path)], sql.encode())
        invocations += 1
        out = (result.stdout or b"").decode(errors="replace")
        if result.returncode == 0 and any(
            line.strip().isdigit() for line in out.splitlines()
        ):
            return ";".join(extra) or "default", invocations
    return None, invocations


def _run_sqlcipher_subprocess(
    argv: list[str], input_bytes: bytes
) -> "subprocess.CompletedProcess[bytes]":
    """sqlcipher 试开缺省执行件(argv 字面量白名单,无外壳)。"""
    try:
        return subprocess.run(  # noqa: S603 - 字面量命令,无外壳
            argv,
            input=input_bytes,
            capture_output=True,
            timeout=SQLCIPHER_TRY_TIMEOUT_SECONDS,
            check=False,
        )
    except FileNotFoundError as exc:
        raise BridgeError(
            KEY_UNAVAILABLE,
            "sqlcipher 不在场(试开验证前置缺失;design §5.1 不静默半装)",
            fix_hint="brew install sqlcipher 后重试(组件安装前置)",
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"sqlcipher 试开超时(>{SQLCIPHER_TRY_TIMEOUT_SECONDS:.0f}s,已 kill)",
        ) from exc


def verify_candidates(
    db_storage: Path,
    targets: list[tuple[str, int, bytes]],
    candidates: list[str],
    *,
    sqlcipher_runner: SqlcipherRunner | None = None,
) -> tuple[dict[str, str], ScanReport]:
    """验证管道后半:熵筛 → 并行试开 → page1 交叉验证(纯函数;全 mock 可测)。

    - 熵筛:候选 32B 熵 < :data:`ENTROPY_MIN_BITS_PER_BYTE` 弃(全零/文本窗)。
    - 试开:首库(最小 page1 目标)开锁判真;参数变体 4 组命中即止。
    - 交叉验证:命中 key 对各库 page1 离线 HMAC(:func:`verify_key_for_page`,
      与 keys.json 消费通路同款)——**只有过 canonical 验证的条目才可能进
      keys.json**(非缺省参数组命中的 key 材料为真,但消费通路按缺省参数
      解密;过不了 canonical 的命中只计入形状,不落缓存,宁缺毋假)。

    Returns:
        (命中映射 {相对路径: key hex}, 形状报告)。
    """
    report = ScanReport(candidates=len(candidates))
    matched: dict[str, str] = {}
    if not targets or not candidates:
        return matched, report
    kept: list[str] = []
    for hex_key in candidates:
        hex_key = hex_key.strip()
        if not re.fullmatch(r"[0-9a-fA-F]{64}", hex_key):
            continue  # 形状不符(非 64-hex)弃
        if entropy_bits_per_byte(bytes.fromhex(hex_key)) >= ENTROPY_MIN_BITS_PER_BYTE:
            kept.append(hex_key.lower())
    report.entropy_kept = len(kept)
    if not kept:
        return matched, report

    primary_rel, _primary_size, _primary_page1 = targets[0]
    primary_db = db_storage / primary_rel
    hits: dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=VERIFY_WORKERS) as pool:
        futures = {
            pool.submit(
                try_open_with_sqlcipher, primary_db, hex_key, runner=sqlcipher_runner
            ): hex_key
            for hex_key in kept
        }
        for future in futures:
            label, invocations = future.result()
            report.sqlcipher_tries += invocations
            if label is not None:
                hits[futures[future]] = label
    report.sqlcipher_hits = len(hits)

    pending = [(rel, page1) for rel, _size, page1 in targets]
    for hex_key in kept:  # 候选原序稳定(命中多 key 时结果可复现)
        if hex_key not in hits:
            continue
        raw = bytes.fromhex(hex_key)
        for rel, page1 in pending:
            report.canonical_verifies += 1
            if verify_key_for_page(raw, page1):
                matched[rel] = hex_key
        pending = [(rel, page1) for rel, page1 in pending if rel not in matched]
    return matched, report


# =====================================================================
# 入口:三重门 → 收集 → 验证 → 全量命中落缓存(600)
# =====================================================================


def acquire_key_from_memory(
    db_storage: Path,
    *,
    config: BridgeConfig,
    targets: list[tuple[str, int, bytes]] | None = None,
    elevated: bool | None = None,
    pids: list[int] | None = None,
    data_root: Path | None = None,
    collector_binary: Path | None = None,
    collector_runner: CollectorRunner | None = None,
    sqlcipher_runner: SqlcipherRunner | None = None,
) -> dict[str, object]:
    """内存密钥扫描入口(三重门;缺一门即拒,exit 21 如实)。

    ``collector_binary`` = 收集器二进制注入点(单测接缝;缺省经
    :func:`resolve_collector_binary` 解析:自愈件优先,组件 bin/ 首用编译)。

    - 门② 配置::attr:`BridgeConfig.mem_search_enabled` 为真(缺省关);
    - 门③ 提权:``elevated`` 判定(缺省 = 本进程 euid==0 **或** setuid
      自愈件已安装;非 darwin 平台恒拒——mach 只读收集器仅 darwin,
      Windows 备胎线另启);不通过即拒,**绝不索要/使用密码**;
    - 目标进程族缺位 → exit 10(wechat_not_running,如实;不臆测)。

    成功 = 全量命中并落缓存,返回形状载荷(命中计数/扫描形状/缓存路径,
    **零材料**);部分命中/零命中/内核拒绝 = exit 21,消息只承载形状。

    Returns:
        dict: ``{"matched": {"count": int, "total": int},
        "scan": {...}, "cache": str}``。
    """
    # —— 门② 配置(design §4:默认关,主人显式开启)——
    if not config.mem_search_enabled:
        raise BridgeError(
            KEY_UNAVAILABLE,
            "内存密钥搜索默认关(配置门未开):mem_search_enabled=false"
            "(D4 豁免后仍须显式开启才生效——design §4)",
            fix_hint=(
                "在 <数据根>/wechat-bridge/config.json 写 "
                '{"mem_search_enabled": true} 后重试;真跑还须提权'
                "(root 或 setuid 自愈件)与主人裁决在案(三重门)"
            ),
        )
    # —— 门③ 平台(mach 只读收集器仅 darwin;绝不索要密码)——
    if not _platform_is_darwin():
        raise BridgeError(
            KEY_UNAVAILABLE,
            "内存密钥扫描仅 darwin 实现(mach 只读收集器);当前平台不支持",
            fix_hint="Windows 备胎线按 G9 判据另启(prd AC6)",
        )
    if elevated is None:
        elevated = _elevation_in_place(data_root=data_root)
    if not elevated:
        raise BridgeError(
            KEY_UNAVAILABLE,
            "内存密钥扫描须提权在位(当前非 root 且 setuid keyscanner 未安装):"
            "收集器 task_for_pid 需 root",
            fix_hint=(
                "sudo -n 不可用即止,绝不索要/使用密码;合法形态 = ①一键脚本 "
                "scripts/wechat-bridge-d4-keyscan.sh 首段安装 setuid 自愈件"
                "(一次 root,此后零人工)或 ②主人亲自单条提权命令"
                "(sudo … localdb key-scan)一次性批处理"
            ),
        )
    # —— 目标库 page1(外部注入 = 单测接缝;离线文件只读)——
    page_targets = targets if targets is not None else page1_targets(db_storage)
    if not page_targets:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"db_storage 内无可校验加密库(页大小不足): {db_storage}",
        )
    # —— 目标进程族 ——
    scan_pids = pids if pids is not None else find_wechat_pids()
    if not scan_pids:
        raise BridgeError(
            WECHAT_NOT_RUNNING,
            "微信进程不在场(pgrep -x WeChat 零命中),内存扫描无从谈起",
            fix_hint="先启动微信客户端并登录;桥不做登录流程(prd R4)",
        )
    # —— 收集器解析(注入接缝优先;自愈件优先,组件 bin/ 首用编译)——
    if collector_binary is not None:
        binary = collector_binary
    else:
        binary, _kind = resolve_collector_binary(data_root=data_root)

    # 盐清单:各库 page1 前 16B(桥侧采集,非提权;C 件 salt 邻域模式用)。
    salt_hex_seen: list[str] = []
    for _rel, _size, page1 in page_targets:
        salt_hex = page1[:16].hex()
        if salt_hex not in salt_hex_seen:
            salt_hex_seen.append(salt_hex)
    salt_hex_seen = salt_hex_seen[:64]  # 收集器盐库上界对齐

    report = ScanReport(pids=scan_pids, salts=len(salt_hex_seen))
    candidates: list[str] = []
    seen: set[str] = set()
    temp_files: list[Path] = []
    try:
        for pid in scan_pids:
            candidates_path, _lines = collect_candidates_file(
                binary,
                pid,
                salt_hex_seen,
                data_root=data_root,
                runner=collector_runner,
            )
            temp_files.append(candidates_path)
            for line in candidates_path.read_text(encoding="utf-8").splitlines():
                token = line.strip()
                if token and token not in seen:
                    seen.add(token)
                    candidates.append(token)

        matched, verify_report = verify_candidates(
            db_storage,
            page_targets,
            candidates,
            sqlcipher_runner=sqlcipher_runner,
        )
        report.candidates = verify_report.candidates
        report.entropy_kept = verify_report.entropy_kept
        report.sqlcipher_tries = verify_report.sqlcipher_tries
        report.sqlcipher_hits = verify_report.sqlcipher_hits
        report.canonical_verifies = verify_report.canonical_verifies

        if len(matched) == len(page_targets):
            cache_path = write_key_cache(matched, data_root=data_root)
            # 闭合 = 冷却理由消失:清自愈冷却戳(best-effort;一键脚本/
            # 手动 key-scan 成功后,后续 query 链失效可即刻重取,不被
            # 旧失败戳白挡一个冷却窗)。
            _clear_self_heal_cooldown(data_root=data_root)
            return {
                "matched": {"count": len(matched), "total": len(page_targets)},
                "scan": report.to_payload(),
                "cache": str(cache_path),
            }
        shape_desc = (
            f"盐={report.salts} 候选={report.candidates} 熵筛={report.entropy_kept} "
            f"试开={report.sqlcipher_tries}次(命中 {report.sqlcipher_hits})"
            f"交叉验证={report.canonical_verifies}次"
        )
        if matched:
            # 部分命中:不落缓存(缓存=全量验证子集;与 acquire_key 同纪律)。
            raise BridgeError(
                KEY_UNAVAILABLE,
                "内存扫描部分命中(不落缓存):命中 "
                f"{len(matched)}/{len(page_targets)}库;{shape_desc}",
                fix_hint="其余库的 key 不在候选族内或已随登录态轮换(G5);"
                "可重扫一次,或转外部密钥引入",
            )
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"内存扫描零命中:pid族={scan_pids} {shape_desc};"
            "三模式宽收集的候选族内无任一库的有效 key",
            fix_hint=(
                "诚实第一:扫不到就扫不到;可重扫一次,或转外部密钥引入"
                "(keys.json,600,查询前逐条重验)"
            ),
        )
    finally:
        for path in temp_files:
            try:
                path.unlink()
            except OSError:
                pass
        # 候选临时件用后即清(红线 6:密钥材料只进 keys.json 私有区)。
        if temp_files:
            scan_dir = temp_files[0].parent
            try:
                scan_dir.rmdir()  # 目录空才删;非空(并发扫描)留着
            except OSError:
                pass


def _current_euid_is_root() -> bool:
    """提权判定注入点(euid==0;单测 monkeypatch 接缝)。"""
    import os

    return os.geteuid() == 0


def _platform_is_darwin() -> bool:
    """平台判定注入点(单测 monkeypatch 接缝;system_checks 同款纪律)。"""
    import sys

    return sys.platform == "darwin"


# =====================================================================
# setuid 自愈(localdb 查询链的密钥缺位/失效重取入口)
# =====================================================================


def self_heal_armed(
    *, config: BridgeConfig | None, data_root: Path | None = None
) -> bool:
    """自愈在位判据:配置门开 + 提权在位(setuid 件或 root)。

    未在位 = 保持现状语义(key_unavailable + 一键脚本指引,零 setuid 面)。
    注意:本函数只判「武装态」(配置 + 安装形状);失败退避的冷却门在
    :func:`try_self_heal` 内部(节流是行为策略,不混进在位判据——
    doctor/诊断面读武装态不应被冷却窗谎报成未武装)。
    """
    if config is None or not config.mem_search_enabled:
        return False
    return _elevation_in_place(data_root=data_root)


def self_heal_cooldown_path(*, data_root: Path | None = None) -> Path:
    """自愈冷却戳路径(数据根私有区 wechat-localdb/self_heal_cooldown.json)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / SELF_HEAL_COOLDOWN_REL_PATH


def self_heal_cooldown_remaining(
    *, data_root: Path | None = None, now: float | None = None
) -> float:
    """距冷却窗结束的剩余秒数(0 = 可重扫;只读状态件,零扫描零成本)。

    冷却戳 = 上次自愈未闭合的时间戳件(**零密钥材料**,红线 6)。缺文件/
    坏 JSON/形状不符 → 0——**状态件损坏即忘却**,负缓存绝不把自愈永久
    卡死(宁可多扫一次,不可永久失能);时间戳在未来(时钟回拨)按整窗
    计,阻塞上界恒为 :data:`SELF_HEAL_COOLDOWN_SECONDS`。
    """
    import json
    import time

    try:
        raw = json.loads(
            self_heal_cooldown_path(data_root=data_root).read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return 0.0
    if not isinstance(raw, dict):
        return 0.0
    failed_at = raw.get("failed_at")
    if not isinstance(failed_at, (int, float)) or isinstance(failed_at, bool):
        return 0.0
    current = time.time() if now is None else now
    elapsed = current - float(failed_at)
    if elapsed < 0:
        return SELF_HEAL_COOLDOWN_SECONDS
    return max(0.0, SELF_HEAL_COOLDOWN_SECONDS - elapsed)


def _record_self_heal_failure(
    *, data_root: Path | None = None, now: float | None = None
) -> None:
    """落冷却戳(600;目录 700;sudo 下属主归还——与 keys.json 同款纪律)。"""
    import json
    import time

    stamp = self_heal_cooldown_path(data_root=data_root)
    stamp.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(stamp.parent, 0o700)
    stamp.write_text(
        json.dumps({"failed_at": time.time() if now is None else now}) + "\n",
        encoding="utf-8",
    )
    os.chmod(stamp, 0o600)
    _restore_owner_for_sudo(stamp.parent)
    _restore_owner_for_sudo(stamp)


def _clear_self_heal_cooldown(*, data_root: Path | None = None) -> None:
    """清冷却戳(best-effort:任何一次成功闭合都让冷却理由消失)。"""
    try:
        self_heal_cooldown_path(data_root=data_root).unlink()
    except OSError:
        pass  # 缺文件/删失败不拦成功路径;残留旧戳至多白挡一个窗


def try_self_heal(
    db_storage: Path,
    *,
    config: BridgeConfig,
    targets: list[tuple[str, int, bytes]] | None = None,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, str] | None:
    """自愈扫描(best-effort):全量命中 → keys.json 已落,返回缓存映射。

    供 localdb 查询链在密钥缺位/失效时零人工重取;任何未闭合(门未开/
    件未装/微信不在/零命中/部分命中)都返回 None,由调用方如实并入
    exit 21 语义——自愈绝不制造半真状态(缓存=全量验证子集纪律不变)。

    失败退避(0.4.1 复审 medium 修复):未闭合落带时间戳冷却戳,
    :data:`SELF_HEAL_COOLDOWN_SECONDS` 窗内再次进入直接 None 且**零
    扫描**——不可闭合态(微信改版零命中/部分命中/收集器超 600s query
    帽)不再逐次拉取重读微信全进程内存(分钟级且用户无感)。成功闭合
    (本函数或 ``localdb key-scan`` 直连)清戳;CLI/一键脚本不受冷却门。
    """
    if not self_heal_armed(config=config, data_root=data_root):
        return None
    if self_heal_cooldown_remaining(data_root=data_root, now=now) > 0:
        return None  # 冷却门(内部硬保证:任何调用方都绕不过节流)
    try:
        acquire_key_from_memory(
            db_storage,
            config=config,
            targets=targets,
            elevated=True,  # 提权在位性 self_heal_armed 已判(setuid 件/root)
            data_root=data_root,
        )
    except BridgeError:
        _record_self_heal_failure(data_root=data_root, now=now)
        return None  # 形状细节归调用方 notes;此处不吞成成功
    staged = read_key_cache(data_root=data_root)
    if staged is None:
        _record_self_heal_failure(data_root=data_root, now=now)
        return None
    page_targets = targets if targets is not None else page1_targets(db_storage)
    verified = verify_key_mapping(db_storage, staged, targets=page_targets)
    if page_targets and len(verified) == len(page_targets):
        # 闭合 = 冷却理由消失(与 acquire_key_from_memory 成功路径同款;
        # 本函数的合同自持:成功返回即清戳,不依赖闭合来自哪条通路)。
        _clear_self_heal_cooldown(data_root=data_root)
        return verified
    _record_self_heal_failure(data_root=data_root, now=now)
    return None
