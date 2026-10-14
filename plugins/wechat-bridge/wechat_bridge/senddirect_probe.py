"""lldb 内嵌直发探针(随包分发;task 10-14-wechat-sendmsg-direct 阶段3 §2)。

本文件在 **lldb 进程内**运行(``command script import`` 装载,cmd 批调
``senddirect_probe.run()``);全部参数来自 env ``SENDDIRECT_REQUEST`` 指向
的 request JSON(桥侧 senddirect 写入),哨兵写 ``SENDDIRECT_RUN_DIR``:
PREFLIGHT_OK/PREFLIGHT_FAIL/ARMED/DONE/ERROR(round.sh 判例的桥内化)。

红线:只读观察 + 函数直调;**绝不写微信自有代码/数据**(expr 语句块局部
缓冲 = 批准范围的参数装载,§2.0);observe 模式断点「使能→命中→立即
禁用」;全程零常驻。

preflight 门序(§2.6,grill r2 定稿):

1. 模块锁定:basename==wechat.dylib 且 __TEXT ≥128MiB 的候选**恰好一个**
   (磁盘 Resources FAT 主体 + Frameworks 桩双同名歧义,F10);S=幸存模块
   头部装载地址;区间断言锚点落 __TEXT 内;
2. 副门:``S+anchor_offset`` 16B 锚字节逐字节比对(指令字节与 slide 无关);
3. 主门:模块磁盘文件 arm64 **切片 sha256**(FAT 大端解析取 cputype==arm64
   区间 / 纯 thin 整文件;≈165MiB 读 ≈1-2s)——禁止弱化回 16B 单门;
4. 服务对象获取:global(读 ``S+service_global_off`` 槽)或 observe_bp
   (enqueue 断点等自然任务命中读 x0;§2.5 式 B);
5. 活性验(slide 相对量):``vptr−S == svc_vtable_off`` + 非指针不变字段
   逐字节比对——绝不比对 vptr 原始值(重启即假阴性)。

observe 模式(r4a 零出站取证):不比对,记录 {q, svc, vptr−S, 不变字段}
到 PREFLIGHT_OK 哨兵——服务对象锚定值的采集面。
"""

from __future__ import annotations

import hashlib
import json
import os
import struct
import time

RUN_DIR = os.environ.get("SENDDIRECT_RUN_DIR", "")
REQUEST_PATH = os.environ.get("SENDDIRECT_REQUEST", "")

FAT_MAGIC_BE = b"\xca\xfe\xba\xbe"
THIN_MAGIC_64_LE = 0xFEEDFACF
ARM64_CPUTYPE = 0x0100000C
MODULE_TEXT_MIN_BYTES = 0x8000000
OBSERVE_WAIT_S = 10.0
EXPR_TIMEOUT_US = 40_000_000  # 40s(< 桥侧 45s 带宽)


class PreflightFail(Exception):
    """门失败(reason 进 PREFLIGHT_FAIL 哨兵;未调用,零风险)。"""

    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason
        self.detail = detail


def _write_sentinel(name: str, payload: dict) -> None:
    if not RUN_DIR:
        return
    with open(os.path.join(RUN_DIR, name), "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=1)


def _load_request() -> dict:
    if not REQUEST_PATH:
        raise PreflightFail("no_request", "SENDDIRECT_REQUEST 未注入")
    try:
        with open(REQUEST_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        raise PreflightFail("request_unreadable", repr(exc)) from exc
    if not isinstance(data, dict):
        raise PreflightFail("request_shape", "request 顶层须为键值映射")
    return data


def _bridge_module():
    """导入桥包的 senddirect 模块(单一 expr 生成出处;包纯 stdlib 可入)。

    探针随包分发于 ``wechat_bridge/`` 内,父目录即组件根——sys.path 插入
    后 ``from wechat_bridge import senddirect`` 与桥侧同一函数,防近亲漂移。
    """
    import sys

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root not in sys.path:
        sys.path.insert(0, root)
    from wechat_bridge import senddirect  # noqa: PLC0415

    return senddirect


def _read_mem(proc, addr: int, size: int):
    import lldb  # noqa: PLC0415 - lldb 仅进程内可得

    err = lldb.SBError()
    try:
        data = proc.ReadMemory(addr, size, err)
    except Exception:  # noqa: BLE001
        return None
    return data if err.Success() else None


def _hex_int(value, field: str) -> int:
    """request 偏移字段宽容解析(2026-10-15 装机实证 bug 修正)。

    桥侧 request 各偏移字段应为 ``0x`` 串形态;裸 int 直传时旧实现
    ``int(str(x), 16)`` 会把**十进制**串按十六进制再解析(0x490fb20=
    76631072 → 误读 0x76610336,装机 dry-run 实证踩中)——int 直收,
    串形态仍按 16 解析(兼容 ``0x`` 前缀与裸 hex)。
    """
    if isinstance(value, bool):
        raise PreflightFail("request_shape", f"{field} 不可为布尔")
    if isinstance(value, int):
        return value
    text = str(value).strip().lower().removeprefix("0x")
    try:
        return int(text, 16)
    except ValueError as exc:
        raise PreflightFail("request_shape", f"{field} 非法: {value!r}") from exc


def _slice_arm64_sha256(file_path: str) -> str | None:
    """磁盘 dylib 的 arm64 切片 sha256(与桥侧 senddirect.slice_arm64_sha256
    同算法;lldb 进程内独立实现,避免包依赖)。"""
    digest = hashlib.sha256()
    try:
        with open(file_path, "rb") as handle:
            head = handle.read(8)
            if len(head) < 8:
                return None
            if head[:4] == FAT_MAGIC_BE:
                nfat = struct.unpack(">I", head[4:8])[0]
                if nfat == 0 or nfat > 16:
                    return None
                table = handle.read(20 * nfat)
                if len(table) < 20 * nfat:
                    return None
                chosen = None
                for index in range(nfat):
                    cputype, _cpusub, offset, size = struct.unpack_from(
                        ">IIII", table, index * 20
                    )
                    if cputype == ARM64_CPUTYPE:
                        chosen = (offset, size)
                        break
                if chosen is None:
                    return None
                handle.seek(chosen[0])
                remaining = chosen[1]
            elif struct.unpack("<I", head[:4])[0] == THIN_MAGIC_64_LE:
                handle.seek(0)
                remaining = os.fstat(handle.fileno()).st_size
            else:
                return None
            while remaining > 0:
                chunk = handle.read(min(4 * 1024 * 1024, remaining))
                if not chunk:
                    return None
                digest.update(chunk)
                remaining -= len(chunk)
    except OSError:
        return None
    return digest.hexdigest()


def _lock_module(target):
    """§2.6 模块锁定(basename+尺寸门槛+唯一性;绝不取主 Executable)。"""
    candidates = [
        module
        for module in target.module_iter()
        if module.file.basename == "wechat.dylib"
    ]
    survivors = []
    for module in candidates:
        text = module.FindSection("__TEXT")
        if text.IsValid() and text.GetByteSize() >= MODULE_TEXT_MIN_BYTES:
            survivors.append((module, text))
    if len(survivors) != 1:
        raise PreflightFail(
            "module_lock",
            f"wechat.dylib 候选 {len(candidates)} 个、过尺寸门槛 "
            f"{len(survivors)} 个(须恰好 1;双同名歧义/模块缺失)",
        )
    module, text = survivors[0]
    slide = module.GetObjectFileHeaderAddress().GetLoadAddress(target)
    if not slide:
        raise PreflightFail("slide", "模块头部装载地址不可得")
    text_lo = text.GetLoadAddress(target)
    text_hi = text_lo + text.GetByteSize()
    return module, slide, text_lo, text_hi


def _qword(data: bytes, offset: int = 0) -> int:
    return int.from_bytes(data[offset:offset + 8], "little")


def _resolve_service(
    target, proc, request, slide: int, text_lo: int, text_hi: int
) -> tuple[int, int, int]:
    """服务对象获取(§2.5 两式)→ (svc, q, vptr)。

    observe 模式(mode=observe)下不比对锚定值,记录采集面(r4a)。"""
    anchor = request["anchor"]
    mode = str(request.get("mode", "call"))
    queue_delta = _hex_int(anchor.get("queue_delta", "0x1c0"), "queue_delta")
    ptr_mode = anchor.get("service_ptr_mode")

    if ptr_mode == "global":
        off_raw = anchor.get("service_global_off")
        if off_raw in (None, ""):
            raise PreflightFail("service_global_off", "锚定表缺 global 槽偏移")
        slot = slide + _hex_int(off_raw, "service_global_off")
        data = _read_mem(proc, slot, 8)
        if not data or len(data) < 8:
            raise PreflightFail("global_slot_unreadable", hex(slot))
        svc = _qword(data)
    elif ptr_mode == "observe_bp" or mode == "observe":
        import lldb  # noqa: PLC0415 - lldb 仅进程内可得

        bp_off_raw = anchor.get("enqueue_a")
        if bp_off_raw in (None, ""):
            raise PreflightFail("enqueue_a", "锚定表缺 enqueue 偏移(observe 不可行)")
        bp = target.BreakpointCreateByAddress(slide + _hex_int(bp_off_raw, "enqueue_a"))
        try:
            proc.Continue()
            deadline = time.monotonic() + OBSERVE_WAIT_S
            stopped = False
            while time.monotonic() < deadline:
                state = proc.GetState()
                if state == lldb.eStateStopped:
                    stopped = True
                    break
                if state in (lldb.eStateExited, lldb.eStateInvalid):
                    raise PreflightFail("observe_process_state", str(state))
                time.sleep(0.05)
            if not stopped:
                raise PreflightFail("observe_timeout", f"{OBSERVE_WAIT_S:.0f}s 无自然任务命中")
            q = 0
            for thread in proc:
                if thread.GetStopReason() != lldb.eStopReasonBreakpoint:
                    continue
                x0 = thread.GetFrameAtIndex(0).FindRegister("x0")
                if x0 and x0.IsValid():
                    q = x0.GetValueAsUnsigned()
                break
            if not q:
                raise PreflightFail("observe_x0", "断点命中线程 x0 不可读")
            svc = q - queue_delta
        finally:
            bp.SetEnabled(False)
            target.BreakpointDelete(bp.GetID())
    else:
        raise PreflightFail("service_ptr_mode", f"锚定表未定服务对象获取式: {ptr_mode!r}")

    vptr_data = _read_mem(proc, svc, 8)
    if not vptr_data or len(vptr_data) < 8:
        raise PreflightFail("svc_unreadable", hex(svc))
    vptr = _qword(vptr_data)
    if not (text_lo <= vptr < text_hi):
        raise PreflightFail("svc_vptr_outside_text", f"vptr={vptr:#x} 不在 __TEXT")
    return svc, (svc + queue_delta), vptr


def _validate_liveness(proc, request, slide: int, svc: int, vptr: int) -> dict:
    """活性验(slide 相对量;observe 模式=记录不比对)。"""
    anchor = request["anchor"]
    observe = str(request.get("mode", "call")) == "observe"
    vtable_off_raw = anchor.get("svc_vtable_off")
    report = {"svc": svc, "svc_vtable_off": vptr - slide}
    if observe:
        inv = _read_mem(proc, svc + 8, 24)
        if inv:
            report["svc_invariants_hex"] = inv.hex()
        return report
    if vtable_off_raw in (None, ""):
        raise PreflightFail("svc_vtable_off", "锚定表缺 vtable 相对偏移")
    expected_vtable = _hex_int(vtable_off_raw, "svc_vtable_off")
    if (vptr - slide) != expected_vtable:
        raise PreflightFail(
            "svc_vtable_mismatch",
            f"vptr−S={(vptr - slide):#x} ≠ 锚定 {expected_vtable:#x}(服务对象非锚定形态)",
        )
    inv_hex = anchor.get("svc_invariants_hex")
    if inv_hex:
        current = _read_mem(proc, svc + 8, len(bytes.fromhex(str(inv_hex))))
        if current is None or current.hex() != str(inv_hex):
            raise PreflightFail("svc_invariants_mismatch", "非指针不变字段漂移")
    return report


def run() -> None:
    """cmd 批唯一入口:preflight → [expr 调用] → postflight(条件流全在此)。"""
    import lldb  # noqa: PLC0415

    attach_started = time.time()
    try:
        request = _load_request()
        target = lldb.debugger.GetSelectedTarget()
        proc = target.GetProcess()
        if not proc.IsValid():
            raise PreflightFail("attach", "进程不可得(attach 失败)")

        module, slide, text_lo, text_hi = _lock_module(target)

        anchor = request["anchor"]
        anchor_offset = _hex_int(anchor["anchor_offset"], "anchor_offset")
        if not (slide + anchor_offset >= text_lo and slide + anchor_offset + 16 <= text_hi):
            raise PreflightFail(
                "anchor_region", f"锚点 {anchor_offset:#x} 不在 __TEXT 区间内"
            )
        want_bytes = bytes.fromhex(str(anchor["anchor_bytes_hex"]))
        got = _read_mem(proc, slide + anchor_offset, len(want_bytes))
        if got is None or got != want_bytes:
            raise PreflightFail(
                "anchor_bytes", f"16B 锚字节不符(微信已换包?): got={getattr(got, 'hex', lambda: None)()}"
            )

        disk_path = module.file.fullpath
        slice_sha = _slice_arm64_sha256(disk_path)
        if slice_sha is None:
            raise PreflightFail("slice_format_unknown", f"磁盘形态未知: {disk_path}")
        if slice_sha != str(anchor["slice_sha256"]).lower():
            raise PreflightFail(
                "slice_sha256", f"arm64 切片哈希不符(微信已换包): {slice_sha[:12]}…"
            )

        svc, q, vptr = _resolve_service(target, proc, request, slide, text_lo, text_hi)
        liveness = _validate_liveness(proc, request, slide, svc, vptr)
        _write_sentinel(
            "PREFLIGHT_OK.json",
            {
                "slide": slide,
                "svc": svc,
                "q": q,
                "attach_ms": int((time.time() - attach_started) * 1000),
                "slice_sha256": slice_sha,
                **liveness,
            },
        )
    except PreflightFail as exc:
        _write_sentinel(
            "PREFLIGHT_FAIL.json", {"reason": exc.reason, "detail": exc.detail}
        )
        return  # 批余段(cmd 文件的 detach/quit)自然收兵,零调用
    except Exception as exc:  # noqa: BLE001 - 哨兵协议绝不裸抛
        _write_sentinel("ERROR.json", {"stage": "preflight", "detail": repr(exc)})
        return

    mode = str(request.get("mode", "call"))
    if mode in ("dry_run", "observe"):
        return  # 到活性验即停(§3.1 dry-run;observe=取证形态)

    # —— 调用段(§2.1 主配方;armed 哨兵 = expr 提交前)——
    call = request.get("call")
    if not isinstance(call, dict):
        _write_sentinel("ERROR.json", {"stage": "call", "detail": "request 缺 call 载荷"})
        return
    try:
        bridge = _bridge_module()
        expr_text = bridge.build_call_expr(
            _hex_int(call["send_entry"], "send_entry"),
            slide,
            svc,
            bytes(int(v) for v in call.get("peer", [])),
            bytes(int(v) for v in call.get("body", [])),
            by_value=bool(call.get("by_value", False)),
        )
    except Exception as exc:  # noqa: BLE001 - 工件构造失败绝不进调用
        _write_sentinel("ERROR.json", {"stage": "call", "detail": f"expr 构造失败: {exc!r}"})
        return
    _write_sentinel("ARMED.json", {"t": time.time()})
    try:
        thread = proc.GetSelectedThread()
        frame = thread.GetSelectedFrame()
        options = lldb.SBExpressionOptions()
        options.SetTimeoutInMicroSeconds(EXPR_TIMEOUT_US)
        options.SetUnwindOnError(True)  # 调用出错时回滚栈帧(进程保全方向)
        options.SetIgnoreBreakpoints(True)  # 直调全程零断点(§2.0)
        value = frame.EvaluateExpression(expr_text, options)
        if value.IsValid() and value.GetError().Success():
            _write_sentinel(
                "DONE.json",
                {
                    "call_rc": value.GetValueAsSigned(),
                    "expr_ms": int((time.time() - attach_started) * 1000),
                },
            )
        else:
            detail = ""
            if value.IsValid():
                detail = str(value.GetError())
            _write_sentinel("ERROR.json", {"stage": "call", "detail": detail or "invalid SBValue"})
    except Exception as exc:  # noqa: BLE001
        _write_sentinel("ERROR.json", {"stage": "call", "detail": repr(exc)})
