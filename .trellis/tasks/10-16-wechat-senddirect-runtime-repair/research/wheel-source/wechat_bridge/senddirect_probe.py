"""lldb 内嵌直发探针(随包分发;task 10-14-wechat-sendmsg-direct 阶段3
§2.7 终版模型)。

本文件在 **lldb 进程内**运行(``command script import`` 装载,cmd 批调
``senddirect_probe.run()``);全部参数来自 env ``SENDDIRECT_REQUEST`` 指向
的 request JSON(桥侧 senddirect 写入),哨兵写 ``SENDDIRECT_RUN_DIR``:
CAPTURE_ARMED/PREFLIGHT_OK/PREFLIGHT_FAIL/ARMED/DONE/ERROR(round.sh
判例的桥内化)。

红线:只读观察 + 函数直调;**绝不写微信自有代码/数据**(expr 语句块局部
缓冲 = 批准范围的参数装载,§2.0);capture 段断点「使能→命中→立即禁用
→删除」;全程零常驻。

preflight 门序(§2.6,grill r2 定稿):

1. 模块锁定:basename==wechat.dylib 且 __TEXT ≥128MiB 的候选**恰好一个**
   (磁盘 Resources FAT 主体 + Frameworks 桩双同名歧义,F10);S=幸存模块
   头部装载地址;区间断言锚点落 __TEXT 内;
2. 副门:``S+anchor_offset`` 16B 锚字节逐字节比对(指令字节与 slide 无关);
3. 主门:模块磁盘文件 arm64 **切片 sha256**(FAT 大端解析取 cputype==arm64
   区间 / 纯 thin 整文件;≈165MiB 读 ≈1-2s)——禁止弱化回 16B 单门。

capture_call 模式(§2.7 终版,mode=capture_call|call):

4. capture 段:断点=anchors.send_entry(F_exec 入口)自身;Continue 后写
   CAPTURE_ARMED 哨兵(桥侧见此才放触发发送——经 send_text 既有链真发
   filehelper 嘻嘻变体);命中判别门=needle(触发变体原字节,cap5 纪律)
   扫 x1 模板块,杂散命中继续等;命中读 x0=ctx、dump x1 起 0x230B=模板;
   finally 禁用+删除断点;验模板 +0x00 标志=1 与 ctx vtable−slide(§2.5
   slide 相对量定则);采集 ctx+8..+0x20 非指针不变字段(桥侧回填锚定表
   svc_invariants_hex);PREFLIGHT_OK 记形状(template 只记指纹,零内容);
5. call 段(同会话,模板堆指针仍活):经包导入桥侧 build_call_expr 构造
   三槽补丁 expr(+0x228 置 0 跳 retain)→ ARMED 哨兵 →
   EvaluateExpression 直调 → postflight(返回值+进程存活)→ DONE。

dry_run/observe 模式:dry_run=**门即止**(模块锁定+锚字节+切片哈希,
零断点零等待零触发,§3.1「可无限重跑」契约面;§2.7 终版锚定表下
活性验= capture 轮产物,passive 观察不存在);observe=r4a 取证形态
(自然任务观察,记录不比对)。
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
#: capture 段观察窗(§2.7:桥侧触发发送经 UI 链,数秒级;窗宽盖触发全链)。
#: 预算算术(质询轮 P2 定则,端到端必须 ≤ 桥侧 45s 带宽):
#: attach+门 ≤8s + capture ≤20s + expr ≤15s ≈ 43s ≤ 45s——晚命中+慢 expr
#: 不再落进桥侧 SIGKILL 窗(expr 中途被杀=微信残留停止态自招)。
CAPTURE_WAIT_S = 20.0
#: msgctx 模板尺寸(§2.7:x1 起 0x230B;与桥侧 senddirect.TEMPLATE_BYTES 同值,
#: 探针独立常量防包依赖漂移)。
TEMPLATE_BYTES = 0x230
#: ctx 非指针不变字段采集窗(slide 相对量锚定面,§2.5)。
CTX_INVARIANTS_OFFSET = 8
CTX_INVARIANTS_LEN = 24
EXPR_TIMEOUT_US = 15_000_000  # 15s(预算算术见 CAPTURE_WAIT_S 注)


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


def _capture_template(target, proc, request, slide: int):
    """capture 段(§2.7):断点=send_entry;等触发命中;读 x0=ctx 与
    x1 起 0x230B 模板;禁用+删除断点;验形+采集锚定面。

    判别门(两级):命中线程 stop reason=断点 + x1 模板块含 needle
    (触发变体原字节;cap5 纪律——自然杂散命中继续等,绝不取首击)。

    Returns:
        (ctx, template_bytes, vtable_off, invariants_bytes)

    Raises:
        PreflightFail: observe_timeout(窗内无 needle 命中)/
            observe_process_state(等待中进程退出)/observe_x0(寄存器
            不可读)/capture_template_flag(模板 +0x00≠1)/
            svc_vtable_mismatch(ctx 非 §2.7 锚定形态)。
    """
    import lldb  # noqa: PLC0415 - lldb 仅进程内可得

    anchor = request["anchor"]
    send_entry_raw = anchor.get("send_entry")
    if send_entry_raw in (None, ""):
        raise PreflightFail("send_entry", "锚定表缺 send_entry(capture 不可行)")
    send_entry = _hex_int(send_entry_raw, "send_entry")
    vtable_raw = anchor.get("svc_vtable_off")
    if vtable_raw in (None, ""):
        raise PreflightFail("svc_vtable_off", "锚定表缺 ctx vtable 相对偏移")
    expected_vtable = _hex_int(vtable_raw, "svc_vtable_off")
    capture_req = request.get("capture")
    if not isinstance(capture_req, dict):
        raise PreflightFail("capture_needle", "request 缺 capture 载荷")
    try:
        needle = bytes(int(v) for v in capture_req.get("needle", []))
    except (TypeError, ValueError) as exc:
        raise PreflightFail("capture_needle", f"needle 非字节清单: {exc}") from exc
    if not needle:
        raise PreflightFail("capture_needle", "request 缺 capture.needle(触发正文)")

    bp = target.BreakpointCreateByAddress(slide + send_entry)
    template: bytes | None = None
    ctx = 0
    try:
        # capture 段切 async(2026-10-15 装机实证 bug:lldb 命令文件批
        # (-b -s)SBDebugger 缺省 **sync**,Continue() 阻塞至进程再停——而
        # CAPTURE_ARMED 在 Continue 返回后才写,桥侧见哨兵才放触发发送
        # → 触发永放不出 = 自死锁,45s 批超时 rc=30、零哨兵零出站;
        # /tmp/wxsend6/async_test.{cmd,py,log} 实证 async_default=False 且
        # Continue 不归)。async 下 Continue 立即返回,轮询循环按设计跑;
        # finally 恢复 sync(调用段 EvaluateExpression 保持批缺省形态)。
        lldb.debugger.SetAsync(True)
        proc.Continue()  # 断点已布,微信恢复运行等待触发链命中
        _write_sentinel(
            "CAPTURE_ARMED.json", {"t": time.time(), "bp": hex(slide + send_entry)}
        )
        deadline = time.monotonic() + CAPTURE_WAIT_S
        while time.monotonic() < deadline:
            state = proc.GetState()
            if state in (lldb.eStateExited, lldb.eStateInvalid):
                raise PreflightFail(
                    "observe_process_state", f"capture 等待中进程退出 state={state}"
                )
            if state != lldb.eStateStopped:
                time.sleep(0.05)
                continue
            hit_ctx = 0
            hit_x1 = 0
            for thread in proc:
                if thread.GetStopReason() != lldb.eStopReasonBreakpoint:
                    continue
                frame0 = thread.GetFrameAtIndex(0)
                reg_x0 = frame0.FindRegister("x0")
                reg_x1 = frame0.FindRegister("x1")
                hit_ctx = (
                    reg_x0.GetValueAsUnsigned() if reg_x0 and reg_x0.IsValid() else 0
                )
                hit_x1 = (
                    reg_x1.GetValueAsUnsigned() if reg_x1 and reg_x1.IsValid() else 0
                )
                break
            if hit_ctx and hit_x1:
                block = _read_mem(proc, hit_x1, TEMPLATE_BYTES)
                if block and needle in block:
                    ctx = hit_ctx
                    template = block
                    break
            proc.Continue()  # 杂散命中(非触发):继续等
    finally:
        # 命中即禁断点→删除(§2.0 收兵序;直调段零断点);恢复 sync 缺省
        # (capture 段异常路径同样归位——批余段 detach/quit 与调用段 expr
        # 均按批缺省形态跑)。
        bp.SetEnabled(False)
        target.BreakpointDelete(bp.GetID())
        lldb.debugger.SetAsync(False)
    if template is None:
        raise PreflightFail(
            "observe_timeout",
            f"{CAPTURE_WAIT_S:.0f}s 观察窗内未见触发命中(needle 未中)",
        )
    if template[0] != 1:
        raise PreflightFail(
            "capture_template_flag", f"模板 +0x00 标志字节≠1: {template[0]}"
        )
    vptr_data = _read_mem(proc, ctx, 8)
    if not vptr_data or len(vptr_data) < 8:
        raise PreflightFail("svc_unreadable", hex(ctx))
    vptr = _qword(vptr_data)
    vtable_off = vptr - slide
    if vtable_off != expected_vtable:
        raise PreflightFail(
            "svc_vtable_mismatch",
            f"ctx vptr−S={vtable_off:#x} ≠ 锚定 {expected_vtable:#x}"
            "(ctx 非 §2.7 锚定形态)",
        )
    invariants = _read_mem(
        proc, ctx + CTX_INVARIANTS_OFFSET, CTX_INVARIANTS_LEN
    )
    return ctx, template, vtable_off, invariants or b""


def run() -> None:
    """cmd 批唯一入口:preflight → [capture] → [expr 调用] → postflight。"""
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

        mode = str(request.get("mode", "capture_call"))
        if mode in ("capture_call", "call"):
            # —— capture 段(§2.7):ctx/模板同会话采集,活性验 slide 相对量 ——
            ctx, template, vtable_off, invariants = _capture_template(
                target, proc, request, slide
            )
            _write_sentinel(
                "PREFLIGHT_OK.json",
                {
                    "slide": slide,
                    "svc": ctx,
                    "attach_ms": int((time.time() - attach_started) * 1000),
                    "slice_sha256": slice_sha,
                    "svc_vtable_off": vtable_off,
                    "svc_invariants_hex": (
                        invariants.hex()
                        if len(invariants) == CTX_INVARIANTS_LEN
                        else None
                    ),
                    "template_sha256": hashlib.sha256(template).hexdigest(),
                    "template_len": len(template),
                },
            )
        elif mode == "dry_run":
            # dry-run = 版本门实测面(§3.1「可无限重跑」契约):**门即止**,
            # 零断点零等待零触发。§2.7 终版锚定表(observe_bp)下活性验是
            # capture 轮产物,passive 观察不存在——旧径(等自然任务 10s)在
            # 空闲微信上必败 observe_timeout → dry-run 恒 30(质询轮 P1 实证,
            # doctor 锚定验证随之恒 unknown)。
            _write_sentinel(
                "PREFLIGHT_OK.json",
                {
                    "slide": slide,
                    "attach_ms": int((time.time() - attach_started) * 1000),
                    "slice_sha256": slice_sha,
                },
            )
            return
        else:
            # observe = r4a 取证形态(自然任务观察,记录不比对)。
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
            return
    except PreflightFail as exc:
        _write_sentinel(
            "PREFLIGHT_FAIL.json", {"reason": exc.reason, "detail": exc.detail}
        )
        return  # 批余段(cmd 文件的 detach/quit)自然收兵,零调用
    except Exception as exc:  # noqa: BLE001 - 哨兵协议绝不裸抛
        _write_sentinel("ERROR.json", {"stage": "preflight", "detail": repr(exc)})
        return

    # —— 调用段(§2.7 三槽补丁;armed 哨兵 = expr 提交前;dry_run/observe
    # 已在上方 return,此处仅 capture_call/call 到达)——
    call = request.get("call")
    if not isinstance(call, dict):
        _write_sentinel("ERROR.json", {"stage": "call", "detail": "request 缺 call 载荷"})
        return
    try:
        bridge = _bridge_module()
        expr_text = bridge.build_call_expr(
            _hex_int(call["send_entry"], "send_entry"),
            slide,
            ctx,
            template,
            bytes(int(v) for v in call.get("peer", [])),
            bytes(int(v) for v in call.get("body", [])),
            bytes(int(v) for v in call.get("display", [])),
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
        state = proc.GetState()
        alive = state not in (lldb.eStateExited, lldb.eStateInvalid)
        if not alive:
            _write_sentinel(
                "ERROR.json",
                {"stage": "call", "detail": f"调用后微信进程退出(state={state})"},
            )
        elif value.IsValid() and value.GetError().Success():
            _write_sentinel(
                "DONE.json",
                {
                    "call_rc": value.GetValueAsSigned(),
                    "alive": True,
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
