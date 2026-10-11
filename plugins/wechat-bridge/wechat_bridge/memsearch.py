"""内存密钥搜索(D4 豁免执行件;默认关,主人配置显式开启才生效)。

红线锚点与豁免口径(prd 红线 1/3、design §4;D4 豁免 = 主人 2026-10-11
「全部解决」令,执行边界按豁免令钉死):

- **只读**:对微信进程只做 vm_read 类只读系统调用(``task_for_pid`` 取
  task port → ``mach_vm_region`` 枚举区 → ``mach_vm_read_overwrite``
  读段,取数即离手);**禁写内存、禁注入、禁调试器附加、禁重签名**——
  守卫测试把写/注入/调试类 API 名单钉死在本模块源码之外
  (tests/wechat-bridge/test_localdb_key.py)。
- **单遍批处理**:一次遍历扫完即退,零常驻、零轮询、零重试;扫描预算
  (单区上限/总预算/段长)为模块常量,刻意不设配置面——预算即边界,
  边界不给人调。
- **三重门**(:func:`acquire_key_from_memory` 逐门校验):①主人 D4 豁免
  裁决在案(任务档 A4/「全部解决」令,归任务档文档承载);②配置显式
  开启(``<数据根>/wechat-bridge/config.json`` 的
  ``"mem_search_enabled": true``,缺省关——design §4「开关默认关,
  主人显式开启才生效」;2026-10-11 豁免令把 E1 空壳期的「无配置键」
  口径改写为配置可启);③提权在位(``task_for_pid`` 需 root;
  ``elevated`` 判定不通过即拒,**绝不索要/使用密码**)。
- **诚实语义**:扫不到 = 如实 exit 21 ``key_unavailable``;全部消息只
  承载形状(区数/字节数/候选数/校验次数),密钥材料零落日志零入档
  (红线 6);命中 key 只落数据根私有区 ``wechat-localdb/keys.json``
  (600,与 E1 :func:`wechat_bridge.localdb.resolve_keys` 消费通路同位,
  落盘前经 page1 离线 HMAC 全量验证,查询一步闭合无须改码)。
- **机制边界(如实预告,不包装)**:微信本机为 hardened runtime 签名
  (2026-10-11 codesign 实测 flags=0x10000(runtime)、无 get-task-allow),
  XNU 对 restricted 目标的 ``task_for_pid`` 要求调用方持调试类
  entitlement——**root 亦可能被拒(KERN_FAILURE)**;该拒绝 = 本红线内
  (不重签、不 lldb)此路在该机不可达的如实信号,原样上报,不做规避。
  4.1.x 密钥亦已不以 hex 文本存内存(research/localdb-e2e.md §1.3 三方
  旁证),滑窗候选即原始 32 字节窗,不预设 hex 路径。
- 扫描模式参考公开实现思路(0xlane/wechat-dump-rs 系 macOS 段、参考件
  wechat-mcp-macos 的校验配方),实现为本仓库自有零第三方依赖版本,
  **不拷上游代码**。
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence

from .codes import KEY_UNAVAILABLE, WECHAT_NOT_RUNNING, BridgeError
from .config import BridgeConfig
from .localdb import KEY_SZ, page1_targets, verify_key_for_page, write_key_cache
from .system_checks import CHECK_TIMEOUT_SECONDS, WECHAT_PROCESS_NAME

__all__ = [
    "SCAN_CHUNK_BYTES",
    "SCAN_REGION_MAX_BYTES",
    "SCAN_TOTAL_BUDGET_BYTES",
    "ScanReport",
    "acquire_key_from_memory",
    "find_wechat_pids",
    "iter_process_regions",
    "scan_region_buffers",
]

# =====================================================================
# 扫描预算(模块常量,非配置面;单遍批处理的边界即此,主人可改码但无键)
# =====================================================================

#: 单区字节上限(更大的区整区跳过并如实计数——巨型文件映射不在堆密钥
#: 预期内;上限在区源头执行:区尺寸只在枚举处已知,段流上判无意义)。
SCAN_REGION_MAX_BYTES = 64 * 1024 * 1024
#: 单次批处理的总字节预算(全进程族累计;耗尽即停,如实标 interrupted)。
SCAN_TOTAL_BUDGET_BYTES = 256 * 1024 * 1024
#: 单段读取长度(mach_vm_read_overwrite 每呼的缓冲上限)。
SCAN_CHUNK_BYTES = 1024 * 1024

# —— mach 常量(mach/vm_region.h 与 mach/kern_return.h;只读语义所需子集)——
_VM_PROT_READ = 0x01
_VM_PROT_WRITE = 0x02
_KERN_SUCCESS = 0
_VM_REGION_BASIC_INFO_64 = 9

#: 段流产出形态:``(区号, kind, data)``;kind 三值——
#: ``data``(可扫内容段)/ ``filtered``(非可写私有区,滤除计数)/
#: ``cap``(超单区上限,整区跳过计数)。滤除与跳过在源头记账(区尺寸
#: 与保护位只在枚举处已知),段消费方只对 ``data`` 段做滑窗校验。
RegionChunk = tuple[int, str, bytes]


@dataclass
class ScanReport:
    """扫描形状报告(全部计数,零内容——红线 6;直接进 stdout 契约)。"""

    pids: list[int] = field(default_factory=list)
    regions_scanned: int = 0
    regions_skipped_cap: int = 0
    regions_filtered: int = 0
    bytes_scanned: int = 0
    windows: int = 0
    verifies: int = 0
    interrupted: bool = False

    def to_payload(self) -> dict[str, object]:
        """形状载荷(键序稳定;无任何密钥材料/进程内存内容)。"""
        return {
            "pids": list(self.pids),
            "regions_scanned": self.regions_scanned,
            "regions_skipped_cap": self.regions_skipped_cap,
            "regions_filtered": self.regions_filtered,
            "bytes_scanned": self.bytes_scanned,
            "windows": self.windows,
            "verifies": self.verifies,
            "interrupted": self.interrupted,
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
# 只读内存段源(mach 只读三呼;独立函数 = 合成注入的接缝)
# =====================================================================


def iter_process_regions(pid: int) -> Iterator[RegionChunk]:
    """逐区产出微信进程内存段(**只读**,mach_vm_read 类)。

    - 只 ``mach_vm_read_overwrite`` 读段(读进本进程缓冲即离手),区枚举
      ``mach_vm_region`` 基础信息;**零写、零注入、零调试语义**。
    - 记账三态:非「可读可写且非 shared」的区产出 ``filtered`` 标记
      (malloc 堆焦点:文件只读映射/只执行/JIT 区滤除,预算不烧无谓区);
      大于 :data:`SCAN_REGION_MAX_BYTES` 的可写区产出 ``cap`` 标记整区
      跳过(区尺寸只在源头已知,跳读即不读)。
    - 区中途失读(KERN_INVALID_ADDRESS 等)即弃该区剩余,继续下一区。

    Raises:
        BridgeError: exit 21 —— ``task_for_pid`` 被内核拒(hardened
            runtime 目标对无调试 entitlement 的调用方恒拒,root 亦然),
            mach 码原样上报,不做任何规避。
    """
    import ctypes

    libc = ctypes.CDLL("/usr/lib/libSystem.B.dylib", use_errno=True)

    mach_port_t = ctypes.c_uint32
    kern_return_t = ctypes.c_int

    libc.mach_task_self.restype = mach_port_t
    libc.mach_task_self.argtypes = []
    libc.task_for_pid.restype = kern_return_t
    libc.task_for_pid.argtypes = [mach_port_t, ctypes.c_int, ctypes.POINTER(mach_port_t)]
    libc.mach_port_deallocate.restype = kern_return_t
    libc.mach_port_deallocate.argtypes = [mach_port_t, mach_port_t]
    libc.mach_vm_region.restype = kern_return_t
    libc.mach_vm_region.argtypes = [
        mach_port_t,
        ctypes.POINTER(ctypes.c_uint64),  # address(进出场)
        ctypes.POINTER(ctypes.c_uint64),  # size(出场)
        ctypes.c_int,  # flavor
        ctypes.c_void_p,  # info(基础信息结构)
        ctypes.POINTER(ctypes.c_uint32),  # infoCnt
        ctypes.POINTER(mach_port_t),  # object_name
    ]
    libc.mach_vm_read_overwrite.restype = kern_return_t
    libc.mach_vm_read_overwrite.argtypes = [
        mach_port_t,
        ctypes.c_uint64,  # address
        ctypes.c_uint64,  # size
        ctypes.c_uint64,  # data(本进程缓冲地址)
        ctypes.POINTER(ctypes.c_uint64),  # outsize
    ]

    class VMRegionBasicInfo64(ctypes.Structure):
        """mach/vm_region.h ``vm_region_basic_info_data_64_t``(40B = 10 natural)。"""

        _fields_ = [
            ("protection", ctypes.c_int32),
            ("max_protection", ctypes.c_int32),
            ("inheritance", ctypes.c_uint32),
            ("shared", ctypes.c_uint32),
            ("reserved", ctypes.c_uint32),
            ("offset", ctypes.c_uint64),
            ("behavior", ctypes.c_int32),
            ("user_wired_count", ctypes.c_uint16),
        ]

    task_self = libc.mach_task_self()
    target = mach_port_t(0)
    kr = libc.task_for_pid(task_self, int(pid), ctypes.byref(target))
    if kr != _KERN_SUCCESS:
        raise BridgeError(
            KEY_UNAVAILABLE,
            "task_for_pid 被内核拒绝(mach kern=" + str(int(kr))
            + f";pid={pid})——微信为 hardened runtime 签名(本机 codesign 实测 "
            "flags=0x10000),无调试 entitlement 的调用方 root 亦拒;红线内"
            "(不重签/不 lldb)不做规避,如实上报",
            fix_hint="该拒绝 = 内存读取途径在本机不可达的如实信号;勿重试勿变通",
        )
    try:
        address = ctypes.c_uint64(0)
        size = ctypes.c_uint64(0)
        info = VMRegionBasicInfo64()
        info_cnt = ctypes.c_uint32(ctypes.sizeof(info) // 4)
        object_name = mach_port_t(0)
        chunk = ctypes.create_string_buffer(SCAN_CHUNK_BYTES)
        outsize = ctypes.c_uint64(0)
        region_no = 0
        while True:
            info_cnt.value = ctypes.sizeof(info) // 4
            kr = libc.mach_vm_region(
                target,
                ctypes.byref(address),
                ctypes.byref(size),
                _VM_REGION_BASIC_INFO_64,
                ctypes.byref(info),
                ctypes.byref(info_cnt),
                ctypes.byref(object_name),
            )
            if kr != _KERN_SUCCESS:
                break  # KERN_INVALID_ADDRESS = 地址空间走完,单遍正常终止
            region_start, region_size = address.value, size.value
            address.value = region_start + region_size
            prot = info.protection
            if (prot & _VM_PROT_READ) == 0 or (prot & _VM_PROT_WRITE) == 0 or info.shared:
                yield region_no, "filtered", b""
                region_no += 1
                continue
            if region_size > SCAN_REGION_MAX_BYTES:
                yield region_no, "cap", b""
                region_no += 1
                continue
            offset = 0
            while offset < region_size:
                take = min(SCAN_CHUNK_BYTES, region_size - offset)
                outsize.value = 0
                kr = libc.mach_vm_read_overwrite(
                    target,
                    region_start + offset,
                    take,
                    ctypes.addressof(chunk),
                    ctypes.byref(outsize),
                )
                if kr != _KERN_SUCCESS or outsize.value == 0:
                    break  # 区中途缩水/失读:弃该区剩余,继续下一区
                yield region_no, "data", chunk.raw[: outsize.value]
                offset += outsize.value
            region_no += 1
    finally:
        libc.mach_port_deallocate(task_self, target)


# =====================================================================
# 滑窗候选 + 离线校验(纯函数;合成内存可全链单测)
# =====================================================================


def scan_region_buffers(
    targets: Sequence[tuple[str, int, bytes]],
    buffers: Iterable[RegionChunk],
    *,
    total_budget: int = SCAN_TOTAL_BUDGET_BYTES,
    verifier: Callable[[bytes, bytes], bool] = verify_key_for_page,
) -> tuple[dict[str, str], ScanReport]:
    """对内存段流做 32B 滑窗候选提取 + page1 离线 HMAC 校验(纯函数)。

    - **预算边界**:累计字节超 ``total_budget`` 即停(如实标 interrupted;
      末段只取预算内前缀,不超收)。
    - **跨段拼接**:同区相邻段间携带 31 字节重叠,跨段横卧的 key 恰好
      覆盖一次;换区即清(区地址不连续,不造假拼接)。
    - **校验顺序**(与 E1 :func:`wechat_bridge.localdb.acquire_key` 同构):
      先对首库(最小 page1)逐候选校验,命中即交叉验证其余库;
      只在**全量命中**时返回映射(缓存=全量验证子集,半套不落)。

    Returns:
        (命中映射 {相对路径: key hex}, 形状报告)。
    """
    report = ScanReport()
    matched: dict[str, str] = {}
    if not targets:
        return matched, report
    primary_rel, _primary_size, primary_page1 = targets[0]
    remaining_targets = [(rel, page1) for rel, _size, page1 in targets[1:]]

    carry = b""
    current_region: int | None = None
    budget_left = total_budget
    for region_no, kind, chunk in buffers:
        if kind == "filtered":
            report.regions_filtered += 1
            continue
        if kind == "cap":
            report.regions_skipped_cap += 1
            continue
        if region_no != current_region:
            current_region = region_no
            carry = b""
            report.regions_scanned += 1
        if budget_left <= 0:
            report.interrupted = True
            break
        take = min(len(chunk), budget_left)
        if take < len(chunk):
            report.interrupted = True
        data = carry + chunk[:take]
        budget_left -= take
        report.bytes_scanned += take
        limit = len(data) - KEY_SZ + 1
        if limit <= 0:
            carry = data  # 不足一个窗:整段留作下段的拼接头
            continue
        carry = data[limit:]
        for off in range(limit):
            candidate = data[off : off + KEY_SZ]
            report.windows += 1
            report.verifies += 1
            if verifier(candidate, primary_page1):
                hex_key = candidate.hex()
                matched[primary_rel] = hex_key
                for rel2, page1_2 in remaining_targets:
                    if rel2 in matched:
                        continue
                    report.verifies += 1
                    if verifier(candidate, page1_2):
                        matched[rel2] = hex_key
                if len(matched) == len(targets):
                    return matched, report  # 全量命中:单遍批处理即刻收工
    return matched, report


# =====================================================================
# 入口:三重门 → 单遍扫描 → 全量命中落缓存(600)
# =====================================================================


def acquire_key_from_memory(
    db_storage: Path,
    *,
    config: BridgeConfig,
    targets: list[tuple[str, int, bytes]] | None = None,
    elevated: bool | None = None,
    pids: list[int] | None = None,
    region_source: Callable[[int], Iterator[RegionChunk]] | None = None,
) -> dict[str, object]:
    """内存密钥扫描入口(三重门;缺一门即拒,exit 21 如实)。

    - 门② 配置::attr:`BridgeConfig.mem_search_enabled` 为真(缺省关);
    - 门③ 提权:``elevated`` 判定(缺省 = 本进程 euid==0;非 darwin 平台
      恒拒——mach 只读实现仅 darwin,Windows 备胎线另启);不通过即拒,
      **绝不索要/使用密码**(豁免令边界:sudo -n 不可用即止);
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
                '{"mem_search_enabled": true} 后重试;真跑还须提权(root)'
                "与主人裁决在案(三重门)"
            ),
        )
    # —— 门③ 提权 + 平台(mach 只读实现仅 darwin;绝不索要密码)——
    if not _platform_is_darwin():
        raise BridgeError(
            KEY_UNAVAILABLE,
            "内存密钥扫描仅 darwin 实现(mach 只读段源);当前平台不支持",
            fix_hint="Windows 备胎线按 G9 判据另启(prd AC6)",
        )
    if elevated is None:
        elevated = _current_euid_is_root()
    if not elevated:
        raise BridgeError(
            KEY_UNAVAILABLE,
            "内存密钥扫描须提权(当前非 root):task_for_pid 对受限进程恒拒",
            fix_hint=(
                "sudo -n 不可用即止,绝不索要/使用密码;合法形态 = 主人亲自"
                "单条提权命令(sudo … localdb key-scan)一次性批处理"
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
    source = region_source if region_source is not None else iter_process_regions

    matched: dict[str, str] = {}
    report = ScanReport(pids=scan_pids)
    budget_left = SCAN_TOTAL_BUDGET_BYTES
    for pid in scan_pids:
        pid_matched, pid_report = scan_region_buffers(
            page_targets,
            source(pid),
            total_budget=budget_left,
        )
        budget_left -= pid_report.bytes_scanned
        matched.update(pid_matched)
        report.regions_scanned += pid_report.regions_scanned
        report.regions_skipped_cap += pid_report.regions_skipped_cap
        report.regions_filtered += pid_report.regions_filtered
        report.bytes_scanned += pid_report.bytes_scanned
        report.windows += pid_report.windows
        report.verifies += pid_report.verifies
        report.interrupted = report.interrupted or pid_report.interrupted
        if len(matched) == len(page_targets):
            break  # 全量命中:单遍批处理即刻收工

    if len(matched) == len(page_targets):
        cache_path = write_key_cache(matched)
        return {
            "matched": {"count": len(matched), "total": len(page_targets)},
            "scan": report.to_payload(),
            "cache": str(cache_path),
        }
    scanned_desc = (
        f"区={report.regions_scanned}(滤除非堆区 {report.regions_filtered}/"
        f"跳过超大区 {report.regions_skipped_cap}) 字节={report.bytes_scanned} "
        f"滑窗={report.windows} 校验={report.verifies}次"
        + ("(预算耗尽截断)" if report.interrupted else "")
    )
    if matched:
        # 部分命中:不落缓存(缓存=全量验证子集;与 acquire_key 同纪律)。
        raise BridgeError(
            KEY_UNAVAILABLE,
            "内存扫描部分命中(不落缓存):命中 "
            f"{len(matched)}/{len(page_targets)}库;{scanned_desc}",
            fix_hint=(
                "其余库的 key 不在已扫预算内或已随登录态轮换(G5);"
                "可调大预算(模块常量)重扫一次,或转外部密钥引入"
            ),
        )
    raise BridgeError(
        KEY_UNAVAILABLE,
        f"内存扫描零命中:pid族={scan_pids} {scanned_desc};"
        "可写私有区的已扫预算内未见任一库的有效 key",
        fix_hint=(
            "诚实第一:扫不到就扫不到;可调大预算(模块常量)重扫一次,"
            "或转外部密钥引入(keys.json,600,查询前逐条重验)"
        ),
    )


def _current_euid_is_root() -> bool:
    """提权判定注入点(euid==0;单测 monkeypatch 接缝)。"""
    import os

    return os.geteuid() == 0


def _platform_is_darwin() -> bool:
    """平台判定注入点(单测 monkeypatch 接缝;system_checks 同款纪律)。"""
    import sys

    return sys.platform == "darwin"
