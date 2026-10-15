"""cap25(三断点 watch 终验):L3 的 3 个 caller call site 齐挂
(L4 bl@0x435E070 / 兄弟A bl@0x4352830 / 兄弟B b@0x435ee8c;x1=msgctx 同几何)。
首条 peer=filehelper 命中→拿真体 P→禁三断点→挂 read watch→B 消息读 P 时
守望循环采栈+Continue。门失败也留痕(不静默)。"""
import lldb
import os

OUT = "/tmp/wxsend3/r25"
OFFS = (0x435E070, 0x4352830, 0x435EE8C)
PEER = b"filehelper"
PREFIX = "嘻嘻~c29z".encode("utf-8")

_st = {"bps": [], "wp": None, "slide": 0, "P": 0, "len": 0, "n": 0}


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
    for off in OFFS:
        bp = target.BreakpointCreateByAddress(slide + off)
        bp.SetScriptCallbackFunction("cap25.on_bp")
        _st["bps"].append(bp)
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} offs={[hex(o) for o in OFFS]}\n")


def on_bp(frame, bp_loc, internal_dict):
    try:
        if _st["P"]:
            return False
        _st["n"] += 1
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        mc = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        head = _read(proc, mc, 0x58) or b""
        with open(f"{OUT}/bp{_st['n']}.txt", "a") as f:
            f.write(f"pc_rva={frame.GetPC() - _st['slide']:#x} mc={mc:#x} head16={head[0:16].hex()}\n")
        if head[0:16] != PEER + b"\x00" * (16 - len(PEER)):
            return False
        blob = _read(proc, mc, 0x270) or b""
        slot = blob[0x40:0x58]
        if slot[0:len(PREFIX)] == PREFIX:
            with open(f"{OUT}/note.log", "a") as f:
                f.write("short-form hit (unexpected)\n")
            return False
        p64 = int.from_bytes(slot[0:8], "little")
        ln = int.from_bytes(slot[8:16], "little")
        true = _read(proc, p64, ln) if 0x100000000 < p64 < 0x800000000000 and 0 < ln <= 4096 else None
        with open(f"{OUT}/hit1.txt", "w") as f:
            f.write(f"mc={mc:#x} slot={slot.hex()} true={true.hex() if true else 'ERR'}\n")
        if not true or true[0:len(PREFIX)] != PREFIX:
            return False
        _st["P"] = p64
        _st["len"] = ln
        for b in _st["bps"]:
            b.SetEnabled(False)
        target = proc.GetTarget()
        wp = target.WatchAddress(p64, ln, True, False, lldb.SBError())
        if wp and wp.IsValid():
            _st["wp"] = wp
            with open(f"{OUT}/WATCH_ARMED", "w") as f:
                f.write(f"P={p64:#x} len={ln}\n")
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
