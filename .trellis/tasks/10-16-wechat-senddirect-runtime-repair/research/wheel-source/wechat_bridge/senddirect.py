"""直发通道驱动(LLDB 批式函数直调;task 10-14-wechat-sendmsg-direct
design-阶段3 §2/§3)。

2026-10-16 修正：doctor/dry-run 仅离线检查。旧活调试驱动因取消/超时
清理不可靠而停用，配置不能授权或恢复它；下文保留历史协议供离线测试。
任何新执行器须先实现用户明确的单次目标/用途/时限授权及清理验证。

形态(§3.4):桥侧 python 生成**单次 lldb 批**(attach→preflight→[expr 调用]
→postflight→detach→quit),subprocess + 硬超时驱动,无常驻调试器;lldb 内
逻辑在随包分发的 :mod:`.senddirect_probe`(经 ``command script import``
装载,全部参数经 env 传入的 request JSON——cmd 工件零内容材料)。

哨兵协议(round.sh 判例的桥内化;run_dir 内 JSON 文件,桥侧轮询):

=====================  =====================================================
``CAPTURE_ARMED.json``  capture 段断点已布并 Continue(§2.7;桥侧见此才
                       放触发发送——消「触发先于断点」竞态)
``PREFLIGHT_OK.json``  版本门+活性验全过(含 slide/ctx/attach_ms;capture
                       形态另含 template 指纹与 svc_invariants 采集值)
``PREFLIGHT_FAIL.json`` 门失败({reason, detail};未进入直发调用段)
``ARMED.json``         expr 提交前落(armed 时点;此后绝不 rollback)
``DONE.json``          调用返回({call_rc, alive};postflight 存活一并记)
``ERROR.json``         调用/探测异常({stage, detail})
=====================  =====================================================

版本门(§2.6,grill r2 定稿):**主门 = wechat.dylib arm64 切片 sha256**
(FAT 0xcafebabe 解析取 cputype==0x100000c 切片区间;纯 thin 0xfeedfacf
整文件;F10 端到端亲验算法)——禁止执行者为提速弱化回 16B 单门;副门 =
16B 锚字节。模块锁定:basename==wechat.dylib 且 __TEXT ≥128MiB 的候选
**恰好一个**(磁盘双同名 dylib 歧义,F10),S=幸存模块头部装载地址,
区间断言锚点落 __TEXT 内。服务对象活性验一律 **slide 相对量**
(vptr−S == 锚定表 svc_vtable_off;非指针不变字段逐字节比对)——绝不存
vptr 原始字节(重启即恒假阴性 → 恒 24,通道跨重启即死)。

错误族(§3.3;codes.py 已增 24,exit 1 自定义族照 send_target_not_found
判例显式 code):24 send_direct_unanchored(未调用+rollback)/
send_direct_disabled / lldb_not_found / lldb_attach_failed /
send_direct_body_too_long / send_direct_target_too_long /
send_direct_call_failed(armed 后,绝不回退绝不自动重试)/ wechat_frozen
(SIGKILL 收兵后的结构化存活报告)。

红线(§5 批准范围):attach + 只读观察 + 函数直调;禁写微信自有代码/
数据,禁注入,禁常驻,attach 不通=降级绝不硬闯。参数缓冲(expr 语句块
局部量)=「调函数」的批准范围组成部分(§2.0 界定);expr 文本是**唯一会
碰微信内存的工件**(生成函数纯函数化供 golden 直测)。

清理纪律(2026-10-15 事故后加固):run_dir 一律 ``None`` 起步、mkdtemp
赋值,finally 清理**仅当路径非空且落在系统临时目录内**——任何缺省/相对
路径形态都绝不进入 rmtree(事故判例:``Path()`` 归一化为 ``.`` 曾整删
仓库,详见错题集 S15)。
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import struct
import subprocess
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO, Callable

from .codes import (
    EXIT_GENERIC_FAILURE,
    SEND_DIRECT_UNANCHORED,
    SEND_UNCERTAIN_DEDUP,
    TIMEOUT,
    WECHAT_NOT_RUNNING,
    BridgeError,
)
from .config import BridgeConfig, myssia_home

__all__ = [
    "ANCHOR_REL_PATH",
    "ARM64_CPUTYPE",
    "CAPTURE_ARMED_NAME",
    "FAT_MAGIC",
    "LLDB_BATCH_TIMEOUT_S",
    "LLDB_SIGINT_GRACE_S",
    "MAX_INLINE_STRING_BYTES",
    "MODULE_TEXT_MIN_BYTES",
    "RECEIPT_POLL_SCHEDULE",
    "SLOT_BODY",
    "SLOT_DISPLAY",
    "SLOT_PEER",
    "SLOT_REFCOUNT",
    "TEMPLATE_BYTES",
    "THIN_MAGIC_64",
    "TRIGGER_BODY_VARIANTS",
    "AnchorTable",
    "anchor_file_path",
    "anchor_file_state",
    "backfill_anchor_invariants",
    "build_call_expr",
    "build_cmd_text",
    "load_anchor_table",
    "execute_send",
    "run_lldb_batch",
    "require_lldb",
    "slice_arm64_sha256",
    "trigger_body_for",
    "doctor_direct_channel",
]

#: 锚定表相对数据根路径(§2.6 私有路径族,不入配置键面)。
ANCHOR_REL_PATH = "wechat-bridge/send-direct-anchors.json"
#: inline23_rawlen 串容量(F3:23 容量+末字节裸长度;三槽长度门共用)。
MAX_INLINE_STRING_BYTES = 23
#: msgctx 模板尺寸(§2.7:capture 段 dump x1 起 0x230B,+0x228 引用计数
#: 槽含在内;560B 十进制字面量进 expr)。
TEMPLATE_BYTES = 0x230
#: msgctx 三串槽偏移(cap5 直捕定案:peer@+0x08/body@+0x48/display@+0x130)。
SLOT_PEER = 0x08
SLOT_BODY = 0x48
SLOT_DISPLAY = 0x130
#: 引用计数槽(+0x228 qword;两处使用均有 null 守卫 → 置 NULL=安全跳 retain)。
SLOT_REFCOUNT = 0x228
#: 触发发送正文变体(§2.7 capture_call:filehelper 真发一条换断点命中;
#: 与直发正文必须互斥——localdb 回执对账按 (username, body) 匹配,触发
#: 消息若与直发同文会假绿)。
TRIGGER_BODY_VARIANTS = ("嘻嘻~cap", "嘻嘻~cap2", "嘻嘻~cap3")
#: capture 段哨兵(探针已布 send_entry 断点并 Continue;桥侧见此才放触发)。
CAPTURE_ARMED_NAME = "CAPTURE_ARMED.json"
#: 模块锁定门槛:__TEXT ≥128MiB(主体 ~154MiB 过,84,544B 桩必拒;§2.6)。
MODULE_TEXT_MIN_BYTES = 0x8000000
#: FAT 魔数(大端 0xcafebabe;磁盘双切片形态,F10)。
FAT_MAGIC = 0xCAFEBA_BE
#: 纯 thin Mach-O 64 魔数(小端读 = 0xfeedfacf)。
THIN_MAGIC_64 = 0xFEEDFACF
#: arm64 cputype(F10:fat_arch 表大端字段)。
ARM64_CPUTYPE = 0x0100000C
#: lldb 子进程硬超时(§3.3:45s 带宽 = SIGINT → 10s 宽限 → SIGKILL)。
LLDB_BATCH_TIMEOUT_S = 45.0
LLDB_SIGINT_GRACE_S = 10.0
#: 回执轮询退避(与 send_text 同一;累计 ~30s)。
RECEIPT_POLL_SCHEDULE = (5.0, 10.0, 15.0)
#: 哨兵轮询间隔(armed 及时落 fingerprint pending)。
SENTINEL_POLL_S = 0.2
# 4.1.15 schema-3 模板路线已证伪；改标签/入口地址不能重新启用它。
RETIRED_TEMPLATE_SLICE_SHA256 = frozenset({
    "6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7",
})


def _now() -> float:
    """时钟注入点(单测换假钟;独立函数避免 import time 散布)。"""
    return time.time()


def _sleep(seconds: float) -> None:
    """sleep 注入点(回执退避的单测换装点)。"""
    time.sleep(seconds)


def _require_safe_live_driver() -> None:
    """旧执行器尚无安全授权/清理入口，拒绝所有产品活调试调用。

    SIGKILL 并不保证 PT_DETACH，daemon 触发线程还可能在调用返回后继续。
    在替代执行器完成前，不提供参数、配置或环境变量绕过；离线单测只在
    假 Popen/假 LLDB 边界注入此门，不产生任何真实授权。
    """
    raise BridgeError(
        SEND_DIRECT_UNANCHORED,
        "旧直发调试驱动无法保证取消/超时后解除附加，产品活调试入口已停用",
        fix_hint="先实现可验证清理的前台单次执行器，再取得用户明确的目标、用途、"
        "最长时限授权；禁止后台、循环重挂或失败自动重试",
    )


def _cleanup_run_dir(run_dir: Path | None) -> None:
    """run_dir 清理(事故加固:仅当非 None 且落在系统临时目录内才 rmtree)。

    2026-10-15 事故判例(S15):早期实现以 ``Path()`` 为缺省,而 ``Path("")``
    归一化为 ``PosixPath('.')``——早失败路径的 finally 因此 ``rmtree('.')``
    整删了测试运行时的当前工作目录(仓库根)。本函数把清理面钉死在
    mkdtemp 产物上:相对路径/仓库路径/任何缺省形态都到不了 rmtree。
    """
    if run_dir is None:
        return
    try:
        text = str(run_dir)
        if not text.startswith(tempfile.gettempdir()):
            return
        if run_dir.is_dir():
            shutil.rmtree(run_dir, ignore_errors=True)
    except OSError:
        pass


# --------------------------------------------------------------- 锚定表 ----


class _AnchorShapeError(ValueError):
    """锚定表形状非法(doctor 归 unknown;发送归 24,fail-closed)。"""


def _parse_hex_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise _AnchorShapeError(f"{field_name} 须为 0x 十六进制串或整数")
    text = str(value).strip().lower()
    if not text.startswith("0x"):
        raise _AnchorShapeError(f"{field_name} 须为 0x 前缀形态: {value!r}")
    try:
        return int(text, 16)
    except ValueError as exc:
        raise _AnchorShapeError(f"{field_name} 非法十六进制: {value!r}") from exc


def _parse_hex_bytes(value: Any, field_name: str) -> bytes:
    if not isinstance(value, str):
        raise _AnchorShapeError(f"{field_name} 须为 hex 串")
    text = value.strip().lower().removeprefix("0x")
    if len(text) % 2:
        raise _AnchorShapeError(f"{field_name} hex 长度须为偶数")
    try:
        return bytes.fromhex(text)
    except ValueError as exc:
        raise _AnchorShapeError(f"{field_name} 非法 hex: {value!r}") from exc


@dataclass(frozen=True)
class AnchorTable:
    """锚定表已验证形态(§2.6 schema 3 / §2.7 终版模型;全部 slide 相对量)。

    ``send_entry`` 允许 None(r4 未落)——此时版本门可验(dry-run 链路),
    但**不可调用**(:meth:`callable_for_send` False → 发送路径 24 拒调,
    不猜)。``svc_invariants`` 允许 None(§2.7:capture 轮采集后回填,
    首轮直发即完成回填);旧模型 svc 全局槽已作废(r6/r7 实扫零命中),
    ``service_ptr_mode`` 须为 observe_bp(capture 断点=send_entry 自身)。
    """

    wechat_version: str
    slice_sha256: str
    anchor_offset: int
    anchor_bytes: bytes
    pump_resume: int | None
    enqueue_a: int | None
    enqueue_b: int | None
    send_entry: int | None
    peer_slot: str
    body_slot: str
    string_form: str
    by_value: bool
    buffer_mode: str
    service_ptr_mode: str | None
    service_global_off: int | None
    queue_selector: str
    queue_delta: int
    svc_vtable_off: int | None
    svc_invariants: bytes | None

    def callable_for_send(self) -> bool:
        """发送就绪判定(§2.7 终版):F_exec 入口 + observe_bp 获取式 +
        ctx vtable 相对锚全在(svc_invariants 可缺=capture 轮回填)。"""
        return (
            self.send_entry is not None
            and self.service_ptr_mode == "observe_bp"
            and self.svc_vtable_off is not None
        )


def anchor_file_path(data_root: Path | None = None) -> Path:
    """锚定表绝对路径(数据根私有路径族;§7-4 固定路径)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / ANCHOR_REL_PATH


def anchor_file_state(data_root: Path | None = None) -> str:
    """锚定表在位态:absent / ok / malformed(doctor 三态源)。"""
    path = anchor_file_path(data_root)
    if not path.is_file():
        return "absent"
    try:
        load_anchor_table(data_root)
    except _AnchorShapeError:
        return "malformed"
    return "ok"


def backfill_anchor_invariants(
    invariants_hex: str, data_root: Path | None = None
) -> bool:
    """capture 轮采集的 ctx 非指针不变字段回填锚定表(§2.7「补
    svc_invariants」)。

    仅当现值为缺(null/缺键)时写入——已锚定值不覆盖(漂移=锚定失配,
    归 capture 段 vtable/不变量比对拒,不静默刷新)。原子写(同目录
    temp+rename);形状校验委托 :func:`_parse_hex_bytes`(fail-closed,
    坏输入直接抛、文件不动)。

    Returns:
        是否发生了写入(False=已有值/未变更)。
    """
    _parse_hex_bytes(invariants_hex, "svc_invariants_hex")
    path = anchor_file_path(data_root)
    if not path.is_file():
        return False
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    if not isinstance(raw, dict) or not isinstance(raw.get("offsets"), dict):
        return False
    if raw["offsets"].get("svc_invariants_hex") not in (None, ""):
        return False
    raw["offsets"]["svc_invariants_hex"] = invariants_hex
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(
        json.dumps(raw, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    os.replace(temp, path)
    return True


def load_anchor_table(data_root: Path | None = None) -> AnchorTable:
    """读+验证锚定表(缺文件/形状错 → _AnchorShapeError,调用方归位)。

    Raises:
        _AnchorShapeError: 文件缺位/JSON 坏/必备键缺/hex 形态错。
    """
    path = anchor_file_path(data_root)
    if not path.is_file():
        raise _AnchorShapeError(f"锚定表缺位: {path}")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise _AnchorShapeError(f"锚定表不可读或非合法 JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise _AnchorShapeError("锚定表顶层须为键值映射")
    if raw.get("schema") != 3:
        raise _AnchorShapeError(f"锚定表 schema 须为 3,当前为 {raw.get('schema')!r}")
    for key in ("wechat_version", "dylib_arm64_slice_sha256", "anchor_offset",
                "anchor_bytes_hex", "offsets"):
        if key not in raw:
            raise _AnchorShapeError(f"锚定表缺必备键 {key}")
    offsets = raw.get("offsets")
    if not isinstance(offsets, dict):
        raise _AnchorShapeError("锚定表 offsets 须为键值映射")
    slice_hex = str(raw["dylib_arm64_slice_sha256"]).strip().lower()
    if len(slice_hex) != 64:
        raise _AnchorShapeError("dylib_arm64_slice_sha256 须为 64 位 hex")
    try:
        bytes.fromhex(slice_hex)
    except ValueError as exc:
        raise _AnchorShapeError("dylib_arm64_slice_sha256 非法 hex") from exc
    arg_abi = offsets.get("arg_abi") or {}
    if not isinstance(arg_abi, dict):
        raise _AnchorShapeError("offsets.arg_abi 须为键值映射")

    def _opt_off(key: str) -> int | None:
        raw_value = offsets.get(key)
        return (
            None
            if raw_value in (None, "", "null")
            else _parse_hex_int(raw_value, key)
        )

    send_entry = _opt_off("send_entry")
    pump_resume = _opt_off("pump_resume")
    enqueue_a = _opt_off("enqueue_a")
    enqueue_b = _opt_off("enqueue_b")
    service_mode = offsets.get("service_ptr_mode")
    if service_mode not in (None, "global", "observe_bp"):
        raise _AnchorShapeError(f"service_ptr_mode 非法: {service_mode!r}")
    global_off_raw = offsets.get("service_global_off")
    service_global_off = (
        None
        if global_off_raw in (None, "", "null")
        else _parse_hex_int(global_off_raw, "service_global_off")
    )
    queue_selector = offsets.get("queue_selector", "enqueue_a")
    if queue_selector not in ("enqueue_a", "enqueue_b", "same"):
        raise _AnchorShapeError(f"queue_selector 非法: {queue_selector!r}")
    vtable_raw = offsets.get("svc_vtable_off")
    svc_vtable_off = (
        None
        if vtable_raw in (None, "", "null")
        else _parse_hex_int(vtable_raw, "svc_vtable_off")
    )
    invariants_raw = offsets.get("svc_invariants_hex")
    svc_invariants = (
        None
        if invariants_raw in (None, "")
        else _parse_hex_bytes(invariants_raw, "svc_invariants_hex")
    )
    return AnchorTable(
        wechat_version=str(raw["wechat_version"]),
        slice_sha256=slice_hex,
        anchor_offset=_parse_hex_int(raw["anchor_offset"], "anchor_offset"),
        anchor_bytes=_parse_hex_bytes(raw["anchor_bytes_hex"], "anchor_bytes_hex"),
        pump_resume=pump_resume,
        enqueue_a=enqueue_a,
        enqueue_b=enqueue_b,
        send_entry=send_entry,
        peer_slot=str(arg_abi.get("peer_slot", "x1")),
        body_slot=str(arg_abi.get("body_slot", "x2")),
        string_form=str(arg_abi.get("string_form", "inline23_rawlen")),
        by_value=bool(arg_abi.get("by_value", False)),
        buffer_mode=str(arg_abi.get("buffer_mode", "expr_local")),
        service_ptr_mode=service_mode,
        service_global_off=service_global_off,
        queue_selector=queue_selector,
        queue_delta=_parse_hex_int(offsets.get("queue_delta", "0x1c0"), "queue_delta"),
        svc_vtable_off=svc_vtable_off,
        svc_invariants=svc_invariants,
    )


# --------------------------------------------------- 切片哈希(F10 算法)----


def _arm64_file_span(handle: BinaryIO) -> tuple[int, int] | None:
    """定位切片文件区间；哈希与磁盘锚点读取共用，拒绝越界/多义表。"""
    handle.seek(0)
    head = handle.read(8)
    file_size = os.fstat(handle.fileno()).st_size
    if len(head) != 8:
        return None
    if head[:4] == b"\xca\xfe\xba\xbe":
        nfat = struct.unpack(">I", head[4:])[0]
        if not 1 <= nfat <= 16:
            return None
        table = handle.read(20 * nfat)
        if len(table) != 20 * nfat:
            return None
        spans = []
        for index in range(nfat):
            cpu, _sub, offset, size, _align = struct.unpack_from(">IIIII", table, index * 20)
            if cpu == ARM64_CPUTYPE:
                if offset < 8 + len(table) or size == 0 or offset + size > file_size:
                    return None
                spans.append((offset, size))
        return spans[0] if len(spans) == 1 else None
    if struct.unpack("<I", head[:4])[0] == THIN_MAGIC_64:
        return 0, file_size
    return None


def slice_arm64_sha256(dylib_path: Path) -> str | None:
    """磁盘 wechat.dylib 的 arm64 切片 sha256(F10 端到端亲验算法)。

    FAT(大端 0xcafebabe):解析 fat_header.nfat_arch + 20B fat_arch 表,
    取 cputype==arm64 条目对 ``[offset, offset+size)`` 区间哈希;纯 thin
    (小端 0xfeedfacf):整文件哈希;其他魔数 → None(形态未知,不猜)。
    分块读(4MiB)避免整载 ~165MiB。
    """
    digest = hashlib.sha256()
    with open(dylib_path, "rb") as handle:
        span = _arm64_file_span(handle)
        if span is None:
            return None
        handle.seek(span[0])
        remaining = span[1]
        while remaining > 0:
            chunk = handle.read(min(4 * 1024 * 1024, remaining))
            if not chunk:
                return None
            digest.update(chunk)
            remaining -= len(chunk)
    return digest.hexdigest()


def _disk_anchor_bytes(path: Path, offset: int, size: int) -> bytes:
    """按 __TEXT 的 VM/file 映射读取锚点，不能把虚拟地址当文件偏移。"""
    with path.open("rb") as handle:
        span = _arm64_file_span(handle)
        if span is None:
            raise ValueError("arm64_slice")
        start, length = span
        handle.seek(start)
        header = handle.read(32)
        if len(header) != 32 or struct.unpack_from("<II", header) != (THIN_MAGIC_64, ARM64_CPUTYPE):
            raise ValueError("arm64_header")
        count, command_size = struct.unpack_from("<II", header, 16)
        if not 1 <= count <= 4096 or not count * 8 <= command_size <= min(length - 32, 16 * 1024 * 1024):
            raise ValueError("load_commands")
        commands = handle.read(command_size)
        cursor = 0
        for _ in range(count):
            if cursor + 8 > len(commands):
                raise ValueError("load_commands")
            cmd, size_cmd = struct.unpack_from("<II", commands, cursor)
            if size_cmd < 8 or cursor + size_cmd > len(commands):
                raise ValueError("load_command_size")
            if cmd == 0x19 and size_cmd >= 72:
                name = commands[cursor + 8:cursor + 24].rstrip(b"\0")
                if name == b"__TEXT":
                    _vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", commands, cursor + 24)
                    # 锚点相对模块头部；__TEXT 含 Mach-O 头且 fileoff=0。
                    if fileoff != 0 or offset < 0 or offset + size > min(vmsize, filesize, length):
                        raise ValueError("anchor_region")
                    handle.seek(start + offset)
                    return handle.read(size)
            cursor += size_cmd
    raise ValueError("text_segment_missing")


def _validate_disk_anchor(anchor: AnchorTable) -> dict[str, Any]:
    """纯磁盘身份/字节校验；不能证明活进程、调用 ABI 或发送能力。"""
    from .system_checks import WECHAT_BUNDLE_PATH

    path = WECHAT_BUNDLE_PATH / "Contents" / "Resources" / "wechat.dylib"
    try:
        before = path.stat()
        digest = slice_arm64_sha256(path)
        matched = digest == anchor.slice_sha256
        if not matched:
            return {"anchored": "mismatch", "slice_sha256_matched": False, "reason": "slice_sha256"}
        if len(anchor.anchor_bytes) != 16:
            raise ValueError("anchor_size")
        got = _disk_anchor_bytes(path, anchor.anchor_offset, len(anchor.anchor_bytes))
        after = path.stat()
        if (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
            return {"anchored": "unknown", "slice_sha256_matched": None, "reason": "disk_changed"}
        return {
            "anchored": "ok" if got == anchor.anchor_bytes else "mismatch",
            "slice_sha256_matched": True,
            "reason": "disk_match" if got == anchor.anchor_bytes else "anchor_bytes",
        }
    except OSError:
        return {"anchored": "unknown", "slice_sha256_matched": None, "reason": "disk_unavailable"}
    except ValueError as exc:
        return {"anchored": "mismatch", "slice_sha256_matched": True, "reason": str(exc)}


# --------------------------------------------------------- 工件生成(纯)----


def _require_inline23(encoded: bytes, name: str) -> None:
    """串槽长度门(纯函数;长度=**UTF-8 字节数**非字符数,嘻嘻=6、
    8 个汉字=24 → 拒;§2.1 双长度门的函数面)。

    Raises:
        ValueError: 编码后字节数 >23(inline 容量上限;§7-6 可翻案点)。
    """
    if len(encoded) > MAX_INLINE_STRING_BYTES:
        raise ValueError(
            f"{name} UTF-8 字节长 {len(encoded)} 超过 inline23 容量 "
            f"{MAX_INLINE_STRING_BYTES}(长度=字节数,非字符数)"
        )


def trigger_body_for(body: str) -> str:
    """触发发送正文变体(§2.7 capture_call:与直发正文**互斥**)。

    互斥判据=**squash 对账形态**(去全部空白)而非精确相等——回执匹配走
    :func:`.sendui.squash`,而正文原样收 stdin(尾随 ``\\n`` 是 echo/管道
    默认形态):「嘻嘻~cap\\n」精确异文但 squash 相等 → 触发消息可替直发
    回执买单=假绿面(质询轮 P1 实证)。变体按同形态比对,首个 squash
    异文者胜(单一出处 import,防近亲漂移;探针/lldb 路径不经此函数)。
    """
    from .sendui import squash  # noqa: PLC0415 - 局部 import(桥侧调用时)

    receipt_body = squash(body)
    for variant in TRIGGER_BODY_VARIANTS:
        if squash(variant) != receipt_body:
            return variant
    raise AssertionError("变体集与正文同构(不可达:变体集恒多于 1 条)")  # pragma: no cover


def build_call_expr(
    send_entry_off: int,
    slide: int,
    ctx_addr: int,
    template_bytes: bytes,
    peer_utf8: bytes,
    body_utf8: bytes,
    display_utf8: bytes,
) -> str:
    """§2.7 终版模型 expr 文本(纯函数;唯一会碰微信内存的工件,golden 直测)。

    模板直调模型(capture_call 同会话产物):

    - ``template_bytes`` = capture 段从 F_exec 入口 x1 dump 的 0x230B
      模板(含 +0x40 堆指针等活对象引用——同会话直调,模板仍活);
    - 三串槽补丁(inline23:memset 清 24B 槽 → memcpy 装值 → 末字节裸
      长度),peer/body/display 十进制字节数组字面量(非 ASCII 安全);
    - ``+0x228`` 置 0 跳 retain(fexec_decompile 双 null 守卫实证安全);
    - 调用形态 = ``F_exec(ctx, msgctx)``(§2.7:签名 void(long, char*),
      地址=slide+send_entry_off 运行期解析值代入)。

    Raises:
        ValueError: 模板尺寸≠0x230 / 模板 +0x00 标志字节≠1(F_exec 读面
            须=1)/ 任一串槽 UTF-8 字节长 >23。
    """
    if len(template_bytes) != TEMPLATE_BYTES:
        raise ValueError(
            f"模板尺寸须为 {TEMPLATE_BYTES}(0x230)字节,当前 {len(template_bytes)}"
        )
    if template_bytes[0] != 1:
        raise ValueError(f"模板 +0x00 标志字节须=1(F_exec 读面),当前 {template_bytes[0]}")
    _require_inline23(peer_utf8, "peer")
    _require_inline23(body_utf8, "body")
    _require_inline23(display_utf8, "display")
    call_addr = slide + send_entry_off

    def _slot_patch(offset_text: str, encoded: bytes) -> str:
        literal = ",".join(str(v) for v in encoded)
        length = len(encoded)
        # (void) cast 必带:lldb 表达式语境 memset/memcpy 无声明,裸调用
        # 拒析 "unknown return type; cast the call"(质询轮 F1→F2 实弹定则)。
        return (
            f"(void)memset(msgctx+{offset_text},0,24); "
            f"(void)memcpy(msgctx+{offset_text},"
            f"(unsigned char[]){{{literal}}},{length}); "
            f"msgctx[{offset_text}+23]={length};"
        )

    return (
        "(int)({\n"
        f"  unsigned char msgctx[{TEMPLATE_BYTES}] = {{"
        + ",".join(str(v) for v in template_bytes)
        + "};\n"  # 普通串闭单括号(f-string 的 }} 转义不适用于拼接段;
        # 质询轮 P0 判例:曾输出 `}};` → lldb 解析必败于列 1152)
        f"  {_slot_patch('8', peer_utf8)}\n"
        f"  {_slot_patch('0x48', body_utf8)}\n"
        f"  {_slot_patch('0x130', display_utf8)}\n"
        f"  *(long*)(msgctx+{SLOT_REFCOUNT:#x}) = 0;\n"
        f"  ((int(*)(void*,void*))0x{call_addr:x})"
        f"((void*)0x{ctx_addr:x}, (void*)msgctx);\n"
        "})"
    )


def build_cmd_text(pid: int, probe_path: Path) -> str:
    """lldb 批式 cmd 文件文本(attach-快进-detach;条件流全在 probe 内)。"""
    return (
        f"attach -p {pid}\n"
        f'command script import "{probe_path}"\n'
        "script senddirect_probe.run()\n"
        "detach\n"
        "quit\n"
    )


# ------------------------------------------------------------ 前置检查 ----


def wechat_pid() -> int | None:
    """微信进程 pid(pgrep -x WeChat;不在 → None)。"""
    from . import system_checks as sc

    if not sc.wechat_process_running():
        return None
    try:
        completed = subprocess.run(
            ["pgrep", "-x", "WeChat"], capture_output=True, text=True, timeout=5
        )
    except (OSError, subprocess.SubprocessError):
        return None
    for line in completed.stdout.splitlines():
        line = line.strip()
        if line.isdigit():
            return int(line)
    return None


def lldb_executable() -> str | None:
    """lldb 可执行文件解析(shutil.which;缺 = xcode CLT 缺)。"""
    return shutil.which("lldb")


def require_lldb() -> str:
    """前置门:lldb 缺 → exit 1 lldb_not_found(→OCR 降级,§3.3)。"""
    found = lldb_executable()
    if found is None:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "lldb 不在 PATH(xcode Command Line Tools 缺?):直发通道不可用",
            code="lldb_not_found",
            fix_hint="xcode-select --install 后重试;或走 send_text(UI/OCR 链)",
        )
    return found


# -------------------------------------------------------- lldb 批驱动 ----


@dataclass
class BatchOutcome:
    """一次 lldb 批的桥侧观测(哨兵文件由 probe 写,本类只汇总进程面)。

    ``trigger_error``:capture_call 触发发送(§2.7)在后台线程抛出的
    异常——armed 前 = 本次直发的根因(调用方上抛);armed 后探针已捕获
    并直调,触发链异常不推翻调用结果。
    """

    returncode: int | None
    timed_out: bool
    killed: bool
    armed_seen: bool
    log_path: Path
    trigger_error: BaseException | None = None


def _read_sentinel(run_dir: Path, name: str) -> dict[str, Any] | None:
    path = run_dir / name
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def run_lldb_batch(
    lldb_path: str,
    cmd_path: Path,
    run_dir: Path,
    request_path: Path,
    *,
    timeout_s: float = LLDB_BATCH_TIMEOUT_S,
    grace_s: float = LLDB_SIGINT_GRACE_S,
    on_armed: Callable[[], None] | None = None,
    poll_s: float = SENTINEL_POLL_S,
    sleep: Callable[[float], None] = _sleep,
    monotonic: Callable[[], float] = time.monotonic,
    trigger: Callable[[], Any] | None = None,
) -> BatchOutcome:
    """spawn 单次 lldb 批并按 §3.3 杀伤序列守护(轮询 ARMED 哨兵)。

    ``trigger``(capture_call,§2.7):探针写 CAPTURE_ARMED 哨兵(断点已
    布+Continue)后**后台线程**放触发发送——不阻塞主循环对 ARMED/DONE
    的轮询;触发链异常捕获进 ``trigger_error`` 不打断守护(探针侧
    observe_timeout 自会收兵)。

    超时序:SIGINT(批余段跑 detach)→ 宽限 → SIGKILL(SIGKILL 不保证
    PT_DETACH → 微信可能残留停止态,冻结面由调用方探测,§5)。
    """
    _require_safe_live_driver()
    log_path = run_dir / "lldb-batch.log"
    environment = dict(os.environ)
    environment["SENDDIRECT_RUN_DIR"] = str(run_dir)
    environment["SENDDIRECT_REQUEST"] = str(request_path)
    killed = False
    trigger_error: list[BaseException] = []
    trigger_thread: threading.Thread | None = None

    def _fire_trigger() -> None:
        try:
            trigger()
        except BaseException as exc:  # noqa: BLE001 - 捕获面=后台线程兜底
            trigger_error.append(exc)

    with open(log_path, "wb") as log:
        process = subprocess.Popen(
            [lldb_path, "-b", "-s", str(cmd_path)],
            stdout=log,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        deadline = monotonic() + timeout_s
        timed_out = False
        armed_seen = False
        try:
            while True:
                if not armed_seen and (run_dir / "ARMED.json").is_file():
                    armed_seen = True
                    if on_armed is not None:
                        on_armed()
                if (
                    trigger is not None
                    and trigger_thread is None
                    and (run_dir / CAPTURE_ARMED_NAME).is_file()
                ):
                    trigger_thread = threading.Thread(
                        target=_fire_trigger, daemon=True
                    )
                    trigger_thread.start()
                if process.poll() is not None:
                    break
                if monotonic() >= deadline:
                    timed_out = True
                    break
                sleep(poll_s)
        finally:
            # 杀伤序列(§3.3):SIGINT(批余段跑 detach)→ 宽限 → SIGKILL。
            if process.poll() is None:
                process.send_signal(signal.SIGINT)
                grace_deadline = monotonic() + grace_s
                while process.poll() is None and monotonic() < grace_deadline:
                    sleep(poll_s)
                if process.poll() is None:
                    process.kill()
                    killed = True
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:  # pragma: no cover
                    process.kill()
    if trigger_thread is not None:
        # 触发线程收尾(sendui 链自带超时封套;守护不为其无限等)。
        trigger_thread.join(timeout=grace_s)
    returncode = process.poll()
    if not armed_seen and (run_dir / "ARMED.json").is_file():
        armed_seen = True
        if on_armed is not None:
            on_armed()
    return BatchOutcome(
        returncode=returncode,
        timed_out=timed_out,
        killed=killed,
        armed_seen=armed_seen,
        log_path=log_path,
        trigger_error=trigger_error[0] if trigger_error else None,
    )


# ------------------------------------------------------- 冻结探测(§5)----


def _alive_note() -> str:
    """杀伤/超时路径的微信存活注记(§5:桥必做存活探测;只探测不处置)。"""
    from . import system_checks as sc

    if not sc.wechat_process_running():
        return "微信进程不在(疑似崩溃,非冻结)"
    window = sc.wechat_main_window_open()
    if window is False:
        return "进程在、主窗口不可探(SIGKILL 不保证 PT_DETACH,可能残留停止态=冻结)"
    if window is None:
        return "进程在、窗口探测不可及"
    return "进程在、窗口在"


def _frozen_report(outcome: BatchOutcome, armed: bool) -> BridgeError:
    """SIGKILL 收兵路径的存活探测 + 结构化 wechat_frozen 报(绝不自动 kill)。"""
    note = _alive_note()
    if note.startswith("进程在"):
        message = (
            f"lldb 批 SIGKILL 收兵(SIGKILL 不保证 PT_DETACH,微信可能残留"
            f"停止态):{note};armed={armed}"
        )
    else:
        message = f"lldb 批 SIGKILL 收兵后微信进程不在(疑似崩溃,非冻结);armed={armed}"
    return BridgeError(
        EXIT_GENERIC_FAILURE,
        message,
        code="wechat_frozen",
        fix_hint="人工检查/重启微信后重试;桥绝不自动 kill 微信(§5 红线)",
    )


# ----------------------------------------------------------- 主执行链 ----


@dataclass
class _RunArtifacts:
    """一次直发的工件落位(0700 run_dir;finally 经 _cleanup_run_dir 全清)。

    ``run_dir`` 起步恒 None(事故加固,S15)——仅 mkdtemp 赋值后才有清理面。
    """

    run_dir: Path | None = None
    request_path: Path | None = None
    cmd_path: Path | None = None
    attach_ms: int | None = None
    slide: int | None = None
    svc: int | None = None
    call_rc: int | None = None
    receipt: str | None = None


def _unanchored(reason: str, detail: str = "") -> BridgeError:
    return BridgeError(
        SEND_DIRECT_UNANCHORED,
        f"直发版本门/活性验未过({reason}{': ' + detail if detail else ''}):"
        "直发前置条件未确认，未进入直发调用段",
        fix_hint="先核对磁盘身份、锚定表和已验收的适配；配置不能授权调试。"
        "如需发送可显式使用 send_text(UI/OCR 链)",
    )


def _default_trigger_send(config: BridgeConfig) -> Callable[[str], Any]:
    """触发发送缺省件(§2.7:filehelper 真发一条经 ax.send_text 既有链;
    合成目标同 _default_anchor_validator 判例,回执闭包缺省不挂——capture
    命中本身即触发的实证回执)。"""
    from . import ax, sendtarget  # 局部 import 防环

    trigger_target = sendtarget.SendTarget(
        username="filehelper", alias=None, display_name="", search_term="filehelper"
    )

    def _trigger(trigger_body: str) -> dict[str, Any]:
        return ax.send_text(config, trigger_target, trigger_body)

    return _trigger


def execute_send(
    config: BridgeConfig,
    target: Any,
    body: str,
    *,
    dry_run: bool = False,
    on_armed: Callable[[], None] | None = None,
    on_receipt_green: Callable[[], None] | None = None,
    receipt_query: Callable[[str, str, float], bool | None] | None = None,
    data_root: Path | None = None,
    now: Callable[[], float] | None = None,
    sleep: Callable[[float], None] | None = None,
    timeout_s: float = LLDB_BATCH_TIMEOUT_S,
    grace_s: float = LLDB_SIGINT_GRACE_S,
    lldb_path: str | None = None,
    trigger_send: Callable[[str], Any] | None = None,
) -> dict[str, Any]:
    """send_direct 主链(§3.1 步骤 6-9 + §2.7 capture_call;步骤 1-5
    前置由 CLI 分支完成)。

    ``mode=capture_call`` 接线(§2.7 终版):单次 lldb 批内完成 capture
    段(send_entry 断点 + 桥侧触发发送命中 → 读 x0=ctx/x1 0x230B 模板 →
    禁断点 → vtable/不变量采集)与 call 段(同会话三槽补丁 expr 直调,
    模板堆指针仍活)。触发发送经 ``trigger_send`` 注入(CLI 闭包复用
    ax.send_text 既有链;缺省合成 filehelper 目标)——每操作 2 发(1
    触发+1 直调)为 §2.7 定案成本。

    ``now``/``sleep`` 缺省经**模块属性**惰性解析(调用时取
    :data:`_now`/:data:`_sleep`)——CLI 级单测 monkeypatch 模块属性即可
    换假钟/免睡,不经参数穿透。

    Raises:
        BridgeError: 24(门未过,armed 前)/ 17(armed 后超时或回执未绿)/
            30(armed 前超时/capture 观察窗超时)/ 10(capture 中进程退出)/
            1(call_failed·frozen·attach_failed·触发链异常)。
    """
    now_fn = now if now is not None else _now
    sleep_fn = sleep if sleep is not None else _sleep
    started = now_fn()
    artifacts = _RunArtifacts()
    try:
        try:
            anchor = load_anchor_table(data_root)
        except _AnchorShapeError as exc:
            raise _unanchored("anchor_file", str(exc)) from exc
        if dry_run:
            report = _validate_disk_anchor(anchor)
            if report["anchored"] != "ok":
                raise _unanchored("disk_preflight", str(report.get("reason", "unknown")))
            return {
                "send": {
                    "target": {"username": target.username, "display_name": target.display_name},
                    "sent": False,
                    "dry_run": True,
                    "channel": "direct",
                    "anchor_build": anchor.wechat_version,
                    "preflight": "ok",
                    "validation": "disk_only",
                    "runtime_verified": False,
                    "adapter_ready": False,
                    "elapsed_ms": round((now_fn() - started) * 1000),
                }
            }
        if anchor.slice_sha256 in RETIRED_TEMPLATE_SLICE_SHA256:
            raise BridgeError(
                SEND_DIRECT_UNANCHORED,
                "4.1.15 的 schema-3 模板直调配方已证伪，拒绝附加或执行；"
                "当前原生适配尚未完成真实直发验收",
                fix_hint="完成正确 Task/序列化接口适配及单次授权验收；"
                "配置开启、修改锚表或沿用旧授权均不能恢复该配方",
            )
        if not dry_run and not anchor.callable_for_send():
            missing = []
            if anchor.send_entry is None:
                missing.append("send_entry")
            if anchor.service_ptr_mode is None:
                missing.append("service_ptr_mode")
            elif anchor.service_ptr_mode != "observe_bp":
                missing.append(
                    f"service_ptr_mode={anchor.service_ptr_mode}(旧模型作废,"
                    "§2.7 仅 observe_bp)"
                )
            if anchor.svc_vtable_off is None:
                missing.append("svc_vtable_off")
            raise _unanchored("anchor_incomplete", "缺 " + ",".join(missing))
        _require_safe_live_driver()
        pid = wechat_pid()
        if pid is None:
            raise BridgeError(
                WECHAT_NOT_RUNNING, "微信进程不在:直发通道前置失败"
            )
        resolved_lldb = lldb_path if lldb_path is not None else require_lldb()
        probe_path = Path(__file__).with_name("senddirect_probe.py")

        # —— 工件落位(0700 run_dir;请求含正文材料,finally 全清)——
        run_dir = Path(tempfile.mkdtemp(prefix="wechat-bridge-send-direct-"))
        os.chmod(run_dir, 0o700)
        artifacts.run_dir = run_dir
        request: dict[str, Any] = {
            "mode": "dry_run" if dry_run else "capture_call",
            "anchor": {
                "slice_sha256": anchor.slice_sha256,
                "anchor_offset": f"0x{anchor.anchor_offset:x}",
                "anchor_bytes_hex": anchor.anchor_bytes.hex(),
                "enqueue_a": None if anchor.enqueue_a is None else f"0x{anchor.enqueue_a:x}",
                "enqueue_b": None if anchor.enqueue_b is None else f"0x{anchor.enqueue_b:x}",
                "send_entry": (
                    None if anchor.send_entry is None else f"0x{anchor.send_entry:x}"
                ),
                "service_ptr_mode": anchor.service_ptr_mode,
                "service_global_off": (
                    None
                    if anchor.service_global_off is None
                    else f"0x{anchor.service_global_off:x}"
                ),
                "queue_selector": anchor.queue_selector,
                "queue_delta": f"0x{anchor.queue_delta:x}",
                "svc_vtable_off": (
                    None if anchor.svc_vtable_off is None else f"0x{anchor.svc_vtable_off:x}"
                ),
                "svc_invariants_hex": (
                    None if anchor.svc_invariants is None else anchor.svc_invariants.hex()
                ),
            },
        }
        trigger_body = trigger_body_for(body)
        if not dry_run:
            # 调用载荷(探针侧经包导入 build_call_expr 构造 expr;display 槽
            # 取 target.display_name;run_dir 0700 且 finally 全清,零内容
            # 残留——§5 隐私)。
            request["call"] = {
                "send_entry": f"0x{anchor.send_entry:x}",
                "peer": list(target.username.encode("utf-8")),
                "body": list(body.encode("utf-8")),
                "display": list((target.display_name or "").encode("utf-8")),
            }
            # capture 段载荷:needle=触发变体原字节(cap5 判别门纪律——
            # 「必须当轮正文」,自然杂散命中被拒之窗外)。
            request["capture"] = {
                "needle": list(trigger_body.encode("utf-8")),
            }
        request_path = run_dir / "request.json"
        request_path.write_text(
            json.dumps(request, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        artifacts.request_path = request_path
        cmd_path = run_dir / "lldb.cmd"
        cmd_path.write_text(build_cmd_text(pid, probe_path), encoding="utf-8")
        artifacts.cmd_path = cmd_path

        trigger_fn: Callable[[], Any] | None = None
        if not dry_run:
            sender = trigger_send if trigger_send is not None else _default_trigger_send(config)
            trigger_fn = lambda: sender(trigger_body)  # noqa: E731 - 闭包固化变体

        outcome = run_lldb_batch(
            resolved_lldb,
            cmd_path,
            run_dir,
            request_path,
            timeout_s=timeout_s,
            grace_s=grace_s,
            on_armed=on_armed,
            sleep=sleep_fn,
            trigger=trigger_fn,
        )
        armed = outcome.armed_seen

        # —— 哨兵判读(§3.1 步骤 7/8;哨兵真值优先于驱动器状态)——
        preflight_fail = _read_sentinel(run_dir, "PREFLIGHT_FAIL.json")
        preflight_ok = _read_sentinel(run_dir, "PREFLIGHT_OK.json")
        error_sentinel = _read_sentinel(run_dir, "ERROR.json")
        done_sentinel = _read_sentinel(run_dir, "DONE.json")

        if outcome.trigger_error is not None and not armed:
            # 触发发送链失败(§2.7 capture 前置)= 本次直发根因;armed 前
            # → 上抛回滚(BridgeError 原样透传族语义,杂异常包裹成契约)。
            exc = outcome.trigger_error
            if isinstance(exc, BridgeError):
                raise exc
            raise BridgeError(
                EXIT_GENERIC_FAILURE,
                f"capture 触发发送链异常: {exc!r}",
                code="send_direct_trigger_failed",
                fix_hint="触发经 send_text 既有链;先跑 send_text 验证 UI 链健康",
            ) from exc
        if preflight_fail is not None:
            reason = str(preflight_fail.get("reason", "preflight"))
            if reason == "attach":
                # attach 拒(并行调试器/权限)= 独立族,非版本失配(§3.3)。
                raise BridgeError(
                    EXIT_GENERIC_FAILURE,
                    "lldb attach 拒(并行调试器/权限):"
                    f"{preflight_fail.get('detail', '')}",
                    code="lldb_attach_failed",
                    fix_hint="排队等并行 lldb 会话收兵后重试;绝不绕过 attach 失败(§5)",
                )
            if reason == "observe_timeout":
                # capture 观察窗超时(触发未命中;§2.7)= armed 前超时族 30。
                raise BridgeError(
                    TIMEOUT,
                    "capture 段观察窗超时(send_entry 断点未见触发命中;"
                    f"{preflight_fail.get('detail', '')}):未进入调用",
                    fix_hint="确认触发链(send_text)健康后重试;armed 前,占位已回滚",
                )
            if reason in ("observe_process_state", "observe_x0"):
                # capture 等待中微信进程退出/寄存器不可读 = 微信不在族 10。
                raise BridgeError(
                    WECHAT_NOT_RUNNING,
                    "capture 段等待中微信进程异常退出:"
                    f"{preflight_fail.get('detail', '')}",
                )
            raise _unanchored(reason, str(preflight_fail.get("detail", "")))
        if error_sentinel is not None and error_sentinel.get("stage") == "attach":
            raise BridgeError(
                EXIT_GENERIC_FAILURE,
                "lldb attach 拒(并行调试器/权限):"
                f"{error_sentinel.get('detail', '')}",
                code="lldb_attach_failed",
                fix_hint="排队等并行 lldb 会话收兵后重试;绝不绕过 attach 失败(§5)",
            )
        if preflight_ok is not None:
            artifacts.attach_ms = preflight_ok.get("attach_ms")
            artifacts.slide = preflight_ok.get("slide")
            artifacts.svc = preflight_ok.get("svc")
            # capture 轮采集的 ctx 非指针不变字段回填锚定表(§2.7「补
            # svc_invariants」;仅缺值时写,已锚定值不覆盖)。
            captured_invariants = preflight_ok.get("svc_invariants_hex")
            if (
                not dry_run
                and isinstance(captured_invariants, str)
                and captured_invariants
                and anchor.svc_invariants is None
            ):
                try:
                    backfill_anchor_invariants(captured_invariants, data_root)
                except (_AnchorShapeError, OSError, ValueError):
                    pass  # 回填失败不拦发送(采集值已在哨兵,下轮再补)
        if outcome.timed_out and not armed:
            # armed 前超时 = 30 + rollback(§3.3;SIGKILL 收兵附存活注记)。
            raise BridgeError(
                TIMEOUT,
                f"lldb 批超时(armed 前 {timeout_s:.0f}s 带宽):未进入调用;"
                f"存活注记:{_alive_note()}",
            )
        if dry_run:
            # dry-run 到活性验即停(§3.1):零占位零指纹零调用,恒成功载荷。
            return {
                "send": {
                    "target": {
                        "username": target.username,
                        "display_name": target.display_name,
                    },
                    "sent": False,
                    "dry_run": True,
                    "channel": "direct",
                    "anchor_build": anchor.wechat_version,
                    "preflight": (
                        "ok"
                        if preflight_ok is not None
                        else f"unknown(哨兵缺失:rc={outcome.returncode})"
                    ),
                    "elapsed_ms": round((now_fn() - started) * 1000),
                }
            }
        if outcome.timed_out and armed:
            raise BridgeError(
                SEND_UNCERTAIN_DEDUP,
                f"lldb 批超时(armed 后 {timeout_s:.0f}s):expr 已提交,发送状态"
                f"不确定——绝不自动重试;存活注记:{_alive_note()}",
            )
        if error_sentinel is not None and error_sentinel.get("stage") == "call":
            detail = str(error_sentinel.get("detail", ""))
            receipt_state = _poll_receipt(
                receipt_query, target.username, body, started, sleep=sleep_fn, now=now_fn
            )
            if receipt_state is True:
                if on_receipt_green is not None:
                    on_receipt_green()
                return _sent_payload(target, anchor, artifacts, started, 0, "green", now=now_fn)
            raise BridgeError(
                EXIT_GENERIC_FAILURE,
                f"expr 已执行但返回异常且回执未绿:{detail}",
                code="send_direct_call_failed",
                fix_hint="人工确认发送结果;绝不自动重试(armed 后同指纹 pending 锁 120s)",
            )
        if done_sentinel is not None:
            call_rc = done_sentinel.get("call_rc")
            artifacts.call_rc = call_rc if isinstance(call_rc, int) else None
            receipt_state = _poll_receipt(
                receipt_query, target.username, body, started, sleep=sleep_fn, now=now_fn
            )
            if receipt_state is True:
                if on_receipt_green is not None:
                    on_receipt_green()
                return _sent_payload(
                    target, anchor, artifacts, started, artifacts.call_rc, "green", now=now_fn
                )
            raise BridgeError(
                SEND_UNCERTAIN_DEDUP,
                "expr 已提交且返回,但回执未绿(localdb 未见落库):发送状态"
                "不确定——绝不自动重试",
            )
        if outcome.killed:
            # SIGKILL 收兵 + 无终态哨兵 → 冻结探测 + 结构化报(§5;绝不
            # 自动 kill 微信)。
            raise _frozen_report(outcome, armed)
        if not armed:
            # 未 armed 且无哨兵(批早退/probe 未装载):形态未知,24 拒。
            raise _unanchored(
                "no_armed",
                f"批未进入调用段(armed 哨兵缺失;rc={outcome.returncode})",
            )
        # armed 但无 DONE/ERROR/杀伤(哨兵缺失的中间态):按不确定处理。
        raise BridgeError(
            SEND_UNCERTAIN_DEDUP,
            f"expr 已提交但终态哨兵缺失(rc={outcome.returncode}):发送状态"
            "不确定——绝不自动重试",
        )
    finally:
        _cleanup_run_dir(artifacts.run_dir)


def _sent_payload(
    target: Any,
    anchor: AnchorTable,
    artifacts: _RunArtifacts,
    started: float,
    call_rc: int | None,
    receipt: str,
    now: Callable[[], float] | None = None,
) -> dict[str, Any]:
    """成功应答(§3.1 形状;键序稳定供 golden 对账)。"""
    now_fn = now if now is not None else _now
    return {
        "send": {
            "target": {
                "username": target.username,
                "display_name": target.display_name,
            },
            "sent": True,
            "channel": "direct",
            "anchor_build": anchor.wechat_version,
            "lldb": {
                "attach_ms": artifacts.attach_ms,
                "call_rc": call_rc,
                "receipt": receipt,
            },
            "elapsed_ms": round((now_fn() - started) * 1000),
        }
    }


def _poll_receipt(
    receipt_query: Callable[[str, str, float], bool | None] | None,
    username: str,
    body: str,
    since_epoch: float,
    *,
    sleep: Callable[[float], None],
    now: Callable[[], float] = _now,
) -> bool | None:
    """localdb 回执终验轮询(sendui._poll_receipt 同构:0+(5,10,15)s 退避)。

    True=落库;False=查询可执行但超窗未见;None=链失败。
    """
    if receipt_query is None:
        return None
    executed = False
    for gap in (0.0,) + tuple(RECEIPT_POLL_SCHEDULE):
        if gap:
            sleep(gap)
        try:
            if receipt_query(username, body, since_epoch) is True:
                return True
            executed = True
        except Exception:  # noqa: BLE001 - 链失败如实 None/继续轮询
            continue
    return False if executed else None


# --------------------------------------------------------- doctor 探针 ----


def doctor_direct_channel(
    config: BridgeConfig,
    data_root: Path | None = None,
    *,
    validator: Callable[[], dict[str, Any]] | None = None,
    lldb_check: Callable[[], str | None] | None = None,
) -> dict[str, Any]:
    """doctor ``direct_channel`` 节；纯磁盘检查，永不默认附加进程。

    形状:``{enabled, anchored, lldb, last_anchor_build, slice_sha256_matched}``。
    anchored 的 ok 仅代表磁盘哈希及锚点匹配，runtime_verified 恒 False。
    配置开关不等于调试授权；lldb 缺失也不影响磁盘检查。validator 仅供
    离线验证器注入，不应执行应用交互。
    """
    lldb_state = "ok" if (lldb_check or lldb_executable)() is not None else "missing"
    state = anchor_file_state(data_root)
    last_build: str | None = None
    slice_matched: bool | None = None
    if state == "ok":
        try:
            anchor = load_anchor_table(data_root)
            last_build = anchor.wechat_version
        except _AnchorShapeError:
            state = "malformed"
    anchored_state = {
        "absent": "no_anchor_file",
        "malformed": "unknown",
        "ok": "unknown",
    }[state]
    if state == "ok" and config.send_direct_enabled:
        if validator is not None:
            report = validator()
        else:
            report = _default_anchor_validator(config, data_root)
        verdict = report.get("anchored")
        if verdict in ("ok", "mismatch", "unknown"):
            anchored_state = verdict
        slice_matched = report.get("slice_sha256_matched")
    return {
        "enabled": bool(config.send_direct_enabled),
        "anchored": anchored_state,
        "lldb": lldb_state,
        "last_anchor_build": last_build,
        "slice_sha256_matched": slice_matched,
        "validation": "disk_only",
        "runtime_verified": False,
    }


def _default_anchor_validator(
    config: BridgeConfig, data_root: Path | None
) -> dict[str, Any]:
    """默认只读磁盘，健康轮询不能通过 execute_send 隐式附加微信。"""
    try:
        return _validate_disk_anchor(load_anchor_table(data_root))
    except (_AnchorShapeError, OSError):
        return {"anchored": "unknown", "slice_sha256_matched": None}
