"""cap27b(文本对象锚定+全程 watch):断 stringForType 调用返回处
(rva 0x70AC5E8;bl@0x70AC5E4 返回,x0=NSString)。命中→解文本缓冲
(UTF-8/UTF-16LE 双搜+对象内指针递归 deref)→read watch 挂 needle 字节
→驱动轮询采栈=正本全程流转链(输入框存储→按钮读取→构造→CGI)。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r28"
OFF_RET = 0x70AC5E8
NEEDLE8 = "嘻嘻~c34u".encode("utf-8")
NEEDLE16 = "嘻嘻~c34u".encode("utf-16-le")
WATCH_LEN = 32

_st = {"bp": None, "wp": None, "slide": 0, "P": 0, "n": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def _find_needle(proc, obj_addr):
    """在 obj 附近解 needle:先内联搜,再对对象内指针样逐个 deref 搜。返回命中地址或 0。"""
    blob = _read(proc, obj_addr, 0x100)
    if blob is None:
        return 0
    for pat in (NEEDLE8, NEEDLE16):
        i = blob.find(pat)
        if i >= 0:
            return obj_addr + i
    for off in range(0, len(blob) - 7, 8):
        p = int.from_bytes(blob[off:off + 8], "little")
        if 0x100000000 < p < 0x800000000000:
            d = _read(proc, p, 0x100)
            if d is None:
                continue
            for pat in (NEEDLE8, NEEDLE16):
                i = d.find(pat)
                if i >= 0:
                    return p + i
    return 0


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
    bp.SetScriptCallbackFunction("cap28.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} bp={slide + OFF_RET:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["P"]:
            return False
        _st["n"] += 1
        proc = frame.GetThread().GetProcess()
        x0 = frame.FindRegister("x0")
        obj = x0.GetValueAsUnsigned() if x0 and x0.IsValid() else 0
        if not obj:
            return False
        p = _find_needle(proc, obj)
        with open(f"{OUT}/hit{_st['n']}.txt", "w") as f:
            head = _read(proc, obj, 0x40) or b""
            f.write(f"obj={obj:#x} found={p:#x} objhead={head.hex()}\n")
        if not p:
            return False
        _st["P"] = p
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        wp = proc.GetTarget().WatchAddress(p, WATCH_LEN, True, False, lldb.SBError())
        if wp and wp.IsValid():
            _st["wp"] = wp
            with open(f"{OUT}/WATCH_ARMED", "w") as f:
                f.write(f"P={p:#x} len={WATCH_LEN}\n")
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
