"""cap31(正本堆缓冲锚定):断 0x70AC5F4(bl 382402 返回处)。
x19=输出槽(callee-saved);*x19=字符串结构 S(382402 填:vptr/cap/len/缓冲)。
dump S(+二级指针)找 needle(UTF-8 先,UTF-16 兜底)→write watch 挂堆缓冲 Q
→轮询采栈=正本搬运链。"""
import lldb
import os

OUT = "/tmp/wxsend3/r31"
OFF_RET = 0x70AC5F4
NEEDLE8 = "嘻嘻~c40y".encode("utf-8")
NEEDLE16 = "嘻嘻~c40y".encode("utf-16-le")
WATCH_LEN = 32

_st = {"bp": None, "wp": None, "slide": 0, "P": 0, "n": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def _find_needle_deep(proc, root):
    """root 处是字符串结构:先 root 内搜,再对 root 前 0x20 内每个指针 deref 搜(两层)。"""
    seen = set()

    def scan(addr, depth):
        if depth > 2 or addr in seen or not (0x100000000 < addr < 0x800000000000):
            return 0
        seen.add(addr)
        blob = _read(proc, addr, 0x80)
        if blob is None:
            return 0
        for pat in (NEEDLE8, NEEDLE16):
            i = blob.find(pat)
            if i >= 0:
                return addr + i
        for off in range(0, len(blob) - 7, 8):
            p = int.from_bytes(blob[off:off + 8], "little")
            if 0x100000000 < p < 0x800000000000:
                r = scan(p, depth + 1)
                if r:
                    return r
        return 0

    return scan(root, 0)


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
    bp = target.BreakpointCreateByAddress(slide + OFF_RET)
    bp.SetScriptCallbackFunction("cap31.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} bp={slide + OFF_RET:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["P"]:
            return False
        _st["n"] += 1
        proc = frame.GetThread().GetProcess()
        x19 = frame.FindRegister("x19")
        slot = x19.GetValueAsUnsigned() if x19 and x19.IsValid() else 0
        if not slot:
            return False
        slot_blob = _read(proc, slot, 8) or b""
        s = int.from_bytes(slot_blob, "little")
        with open(f"{OUT}/hit{_st['n']}.txt", "w") as f:
            f.write(f"x19_slot={slot:#x} S={s:#x}\n")
        if not (0x100000000 < s < 0x800000000000):
            return False
        sblob = _read(proc, s, 0x40) or b""
        with open(f"{OUT}/hit{_st['n']}.txt", "a") as f:
            f.write(f"S_head={sblob.hex()}\n")
        q = _find_needle_deep(proc, s)
        if not q:
            return False
        _st["P"] = q
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        wp = proc.GetTarget().WatchAddress(q, WATCH_LEN, False, True, lldb.SBError())
        if wp and wp.IsValid():
            _st["wp"] = wp
            with open(f"{OUT}/WATCH_ARMED", "w") as f:
                f.write(f"Q={q:#x} len={WATCH_LEN}\n")
        else:
            with open(f"{OUT}/WATCH_FAIL", "w") as f:
                f.write("invalid\n")
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
