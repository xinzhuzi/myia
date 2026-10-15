"""cap23(read-watch 抓正文消费者):断 0x435E070 门=peer filehelper,
消息 A(43B)命中→拿 body 真体堆地址 P→禁断点→挂 read watchpoint→
消息 B 复用 P 时,读 P 的现场回溯 12 帧=正文消费层(CGI 构造/创建层)。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r23"
OFF_BP = 0x435E070
PEER = b"filehelper"
PREFIX = "嘻嘻~c25z".encode("utf-8")

_st = {"bp": None, "wp": None, "slide": 0, "P": 0, "n": 0, "whits": 0, "done": False}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


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
    bp = target.BreakpointCreateByAddress(slide + OFF_BP)
    bp.SetScriptCallbackFunction("cap23.on_bp")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x}\n")


def on_bp(frame, bp_loc, internal_dict):
    try:
        if _st["P"]:
            return False
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        mc = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        head = _read(proc, mc, 0x58) or b""
        if head[0:16] != PEER + b"\x00" * (16 - len(PEER)):
            return False
        blob = _read(proc, mc, 0x270) or b""
        slot = blob[0x40:0x58]
        if slot[0:len(PREFIX)] == PREFIX:
            return False  # 意外短形态,跳过
        p64 = int.from_bytes(slot[0:8], "little")
        ln = int.from_bytes(slot[8:16], "little")
        true = _read(proc, p64, ln) if 0x100000000 < p64 < 0x800000000000 and 0 < ln <= 4096 else None
        with open(f"{OUT}/hit1.txt", "w") as f:
            f.write(f"mc={mc:#x} slot={slot.hex()} true={true.hex() if true else 'ERR'}\n")
        if not true or true[0:len(PREFIX)] != PREFIX:
            return False
        _st["P"] = p64
        _st["len"] = ln
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        target = frame.GetThread().GetProcess().GetTarget()
        wp = target.WatchAddress(p64, ln, True, False, lldb.SBError())  # read watch
        if wp.IsValid():
            wp.SetScriptCallbackFunction("cap23.on_watch")
            _st["wp"] = wp
            with open(f"{OUT}/WATCH_ARMED", "w") as f:
                f.write(f"P={p64:#x} len={ln}\n")
        else:
            with open(f"{OUT}/WATCH_FAIL", "w") as f:
                f.write("invalid wp\n")
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def on_watch(frame, wp, internal_dict):
    try:
        _st["whits"] += 1
        thread = frame.GetThread()
        slide = _st["slide"]
        lines = [f"whit={_st['whits']} t={time.time():.1f}"]
        for i in range(min(14, thread.GetNumFrames())):
            f = thread.GetFrameAtIndex(i)
            pc = f.GetPC()
            rva = pc - slide if slide <= pc < slide + 0x10000000 else 0
            lines.append(f"  #{i} pc={pc:#x} rva={rva:#x} fn={f.GetFunctionName()}")
        with open(f"{OUT}/watch{_st['whits']}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if _st["whits"] >= 12:
            if _st["wp"] is not None:
                _st["wp"].SetEnabled(False)
            _st["done"] = True
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
