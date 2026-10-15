"""cap32(按钮窗管线帧正扫):断三重奏(0x83c750/0x865484/0x866d60)
+CAND3 worker(0x434a2ac)。命中时扫 x0-x3 浅层 deref 找 needle——
带正文的帧=构造/编码现场,记 16 帧栈(GOLD)。不带:静默放行。"""
import lldb
import os

OUT = "/tmp/wxsend3/r32"
OFFS = (0x83C750, 0x865484, 0x866D60, 0x434A2AC)
NEEDLE8 = "嘻嘻~c42y".encode("utf-8")
NEEDLE16 = "嘻嘻~c42y".encode("utf-16-le")

_st = {"bps": [], "slide": 0, "n": 0, "gold": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def _regs_have_needle(proc, frame):
    for reg in ("x0", "x1", "x2", "x3"):
        r = frame.FindRegister(reg)
        v = r.GetValueAsUnsigned() if r and r.IsValid() else 0
        if not (0x100000000 < v < 0x800000000000):
            continue
        for base in (v, v + 0x18, v + 0x40):
            blob = _read(proc, base, 0x80)
            if blob is None:
                continue
            for pat in (NEEDLE8, NEEDLE16):
                if pat in blob:
                    return reg, base
    return None


def install(debugger):
    target = debugger.GetSelectedTarget()
    slide = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
            break
    if slide is None:
        return
    _st["slide"] = slide
    for off in OFFS:
        bp = target.BreakpointCreateByAddress(slide + off)
        bp.SetScriptCallbackFunction("cap32.on_hit")
        _st["bps"].append(bp)
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} offs={[hex(o) for o in OFFS]}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        if _st["gold"] >= 3:
            return False
        proc = frame.GetThread().GetProcess()
        hit = _regs_have_needle(proc, frame)
        if not hit:
            return False
        _st["gold"] += 1
        reg, addr = hit
        thread = frame.GetThread()
        slide = _st["slide"]
        lines = [f"gold={_st['gold']} reg={reg} hit_at={addr:#x} bp_rva={frame.GetPC() - slide:#x} t_n={_st['n']}"]
        for i in range(min(16, thread.GetNumFrames())):
            f = thread.GetFrameAtIndex(i)
            pc = f.GetPC()
            rva = pc - slide if slide <= pc < slide + 0x10000000 else 0
            lines.append(f"  #{i} pc={pc:#x} rva={rva:#x} fn={f.GetFunctionName()}")
        with open(f"{OUT}/GOLD{_st['gold']}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if _st["gold"] >= 3:
            for b in _st["bps"]:
                b.SetEnabled(False)
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
