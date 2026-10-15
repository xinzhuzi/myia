"""cap33(RunLoop Source0 终极正扫):断 __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION
(x0=perform 回调函数,x1=info)。门=扫 x1 浅层(v/v+0x18/v+0x40,+一层指针)找
needle。带正文回调=正本构造/消费现场,GOLD 记 x0(回调函数=身份!)+16 帧栈。"""
import lldb
import os

OUT = "/tmp/wxsend3/r33"
SYM = "__CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION"
NEEDLE8 = "嘻嘻~c46z".encode("utf-8")
NEEDLE16 = "嘻嘻~c46z".encode("utf-16-le")

_st = {"bp": None, "slide": 0, "n": 0, "gold": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def _has_needle(proc, v):
    if not (0x100000000 < v < 0x800000000000):
        return False
    for base in (v, v + 0x18, v + 0x40):
        blob = _read(proc, base, 0x80)
        if blob is not None:
            for pat in (NEEDLE8, NEEDLE16):
                if pat in blob:
                    return True
            # 一层指针
            for off in (0, 8, 0x10, 0x18, 0x20):
                p = int.from_bytes(blob[off:off + 8], "little") if off + 8 <= len(blob) else 0
                if 0x100000000 < p < 0x800000000000:
                    d = _read(proc, p, 0x80)
                    if d:
                        for pat in (NEEDLE8, NEEDLE16):
                            if pat in d:
                                return True
    return False


def install(debugger):
    target = debugger.GetSelectedTarget()
    bp = target.BreakpointCreateByRegex("CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM")
    bp.SetScriptCallbackFunction("cap33.on_hit")
    _st["bp"] = bp
    slide = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
            break
    _st["slide"] = slide or 0
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"locs={bp.GetNumLocations()} slide={_st['slide']:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        if _st["gold"] >= 4:
            return False
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        info = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        if not info or not _has_needle(proc, info):
            return False
        _st["gold"] += 1
        x0 = frame.FindRegister("x0")
        cb = x0.GetValueAsUnsigned() if x0 and x0.IsValid() else 0
        slide = _st["slide"]
        thread = frame.GetThread()
        lines = [f"gold={_st['gold']} cb={cb:#x} cb_rva={cb - slide:#x} info={info:#x} n={_st['n']}"]
        for i in range(min(16, thread.GetNumFrames())):
            f = thread.GetFrameAtIndex(i)
            pc = f.GetPC()
            rva = pc - slide if slide <= pc < slide + 0x10000000 else 0
            lines.append(f"  #{i} pc={pc:#x} rva={rva:#x} fn={f.GetFunctionName()}")
        with open(f"{OUT}/GOLD{_st['gold']}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if _st["gold"] >= 4:
            if _st["bp"] is not None:
                _st["bp"].SetEnabled(False)
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
