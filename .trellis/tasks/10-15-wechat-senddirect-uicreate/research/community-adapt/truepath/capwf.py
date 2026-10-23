"""truepath 勘察:断 mars stn_callback_bridge rva 0x5daad24(纯读零写)。

反汇编依据 ~/ghidra-hunt-r9/hunt_r29_out.txt:
  入口 x0=this(桥对象,尾段 x26=x0);x1..x7=参 1..7;
  栈参 [sp]=s0(尾段 x28 转发)、[sp+8] 低 16 位=s1(尾段 w27 strh 转发);
  尾段:x0=*(x26+8) 即 delegate;vtable=*delegate;blr *(vtable+0x30)。

断点打在函数第一条指令(sub sp 前),sp/参数均未动:
  每次命中 dump x0-x28+sp/fp/lr/pc、入口栈参、x0 对象 0x40、
  delegate 对象 0x40、vtable 全 0x80 字节(解 +0x30 目标 rva+目标处 0x20 字节)、
  x1..x7 参数对象 0x80 原文 + 每对象前 0x40 内指针槽一层 deref 0x40,
  并扫描 needle(嘻嘻~wf101 UTF-8)。回调一律 return False 自动续走;
  超 MAX_HITS/MAX_SECONDS 后禁断点。全程只 ReadMemory,零写零改。
"""
import lldb
import os
import time

OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
BRIDGE_RVA = 0x5DAAD24
NEEDLE = "嘻嘻~wf101".encode("utf-8")  # e5 98 bb e5 98 bb 7e 77 66 31 30 31
MAX_HITS = 96
MAX_SECONDS = 110.0

_st = {"bps": [], "slide": 0, "t0": time.time(), "n": 0, "done": "", "needle_hits": []}


def _read(proc, addr, size):
    if not isinstance(addr, int) or addr < 0x10000 or addr > 0x7FFFFFFFFFFF:
        return None
    err = lldb.SBError()
    try:
        data = proc.ReadMemory(addr, size, err)
    except Exception:
        return None
    return data if err.Success() else None


def _u64(b, off):
    if b and len(b) >= off + 8:
        return int.from_bytes(b[off:off + 8], "little")
    return 0


def _ptr(v):
    return isinstance(v, int) and 0x100000000 <= v <= 0x7FFFFFFFFFFF and (v & 7) == 0


def install(debugger):
    target = debugger.GetSelectedTarget()
    slide = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
            break
    if slide is None:
        with open(f"{OUT}/err.log", "a") as f:
            f.write("wechat.dylib not found\n")
        return
    _st["slide"] = slide
    bp = target.BreakpointCreateByAddress(slide + BRIDGE_RVA)
    bp.SetScriptCallbackFunction("capwf.on_hit")
    _st["bps"].append(bp)
    with open(f"{OUT}/ARMED", "w") as f:
        f.write("slide=%#x bridge_rva=%#x loaded=%s\n" % (slide, BRIDGE_RVA, time.strftime("%H:%M:%S")))


def on_hit(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        n = _st["n"]
        elapsed = time.time() - _st["t0"]
        if n > MAX_HITS or elapsed > MAX_SECONDS:
            for b in _st["bps"]:
                b.SetEnabled(False)
            _st["done"] = "CAPPED"
            return False
        proc = frame.GetThread().GetProcess()
        slide = _st["slide"]

        def reg(name):
            r = frame.FindRegister(name)
            try:
                return r.GetValueAsUnsigned() if r and r.IsValid() else 0
            except Exception:
                return 0

        regs = [reg("x%d" % i) for i in range(29)]
        fp, sp, lr, pc = reg("x29"), reg("sp"), reg("x30"), frame.GetPC()

        lines = ["hit=%d t=%.1f tid=%d pc_rva=%#x" % (n, time.time() - _st["t0"], frame.GetThread().GetIndexID(), pc - slide)]
        lines.append("regs=" + " ".join("x%d=%#x" % (i, v) for i, v in enumerate(regs))
                     + " sp=%#x fp=%#x lr=%#x lr_rva=%#x" % (sp, fp, lr, (lr - slide) if slide <= lr < slide + 0x20000000 else 0))

        s16 = _read(proc, sp, 16)
        if s16:
            lines.append("stack_args=s0=%#x s1_u16=%#x raw=%s" % (_u64(s16, 0), int.from_bytes(s16[8:10], "little"), s16.hex()))

        x0 = regs[0]
        o0 = _read(proc, x0, 0x40)
        if o0:
            lines.append("x0_obj@%#x=%s" % (x0, o0.hex()))
        dele = _u64(o0, 8) if o0 else 0
        od = _read(proc, dele, 0x40) if _ptr(dele) else None
        if od:
            lines.append("delegate=%#x obj=%s" % (dele, od.hex()))
        vt = _u64(od, 0) if od else 0
        vt80 = _read(proc, vt, 0x80) if _ptr(vt) else None
        if vt80:
            t30 = _u64(vt80, 0x30)
            rva30 = (t30 - slide) if slide <= t30 < slide + 0x20000000 else 0
            lines.append("vtable=%#x vt80=%s" % (vt, vt80.hex()))
            lines.append("vt30_target=%#x rva=%#x" % (t30, rva30))
            sig = _read(proc, t30, 0x20) if _ptr(t30) else None
            if sig:
                lines.append("vt30_bytes=%s" % sig.hex())
            slots = []
            for i in range(0, 0x80, 8):
                v = _u64(vt80, i)
                if slide <= v < slide + 0x20000000:
                    slots.append("+%#x=rva%#x" % (i, v - slide))
            if slots:
                lines.append("vt_slots_in_mod=" + " ".join(slots))

        found = []
        for i in range(1, 8):
            v = regs[i]
            if not _ptr(v):
                continue
            raw = _read(proc, v, 0x80)
            if not raw:
                continue
            if NEEDLE in raw:
                found.append("x%d@+%#x" % (i, raw.find(NEEDLE)))
            nd = 0
            for off in range(0, 0x40, 8):
                p = _u64(raw, off)
                if _ptr(p):
                    d2 = _read(proc, p, 0x40)
                    if d2 and NEEDLE in d2:
                        found.append("x%d->+%#x@+%#x" % (i, off, d2.find(NEEDLE)))
                    nd += 1
                    if nd >= 8:
                        break
            lines.append("x%d_obj@%#x=%s" % (i, v, raw.hex()))
        if o0 and NEEDLE in o0:
            found.append("x0obj@+%#x" % o0.find(NEEDLE))
        if od and NEEDLE in od:
            found.append("delegobj@+%#x" % od.find(NEEDLE))
        lines.append("needle=" + ("FOUND " + ",".join(found) if found else "no"))

        with open(f"{OUT}/hit{n}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if found:
            _st["needle_hits"].append(n)
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
