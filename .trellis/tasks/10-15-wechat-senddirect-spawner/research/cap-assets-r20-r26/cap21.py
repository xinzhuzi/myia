"""cap21(长文本形态观察·零补丁零写入):断 L4 内 bl L3(0x435E070),
needle 门改 peer 槽=='filehelper'(+0x00 内联恒在)。发 >23B needle,
看 body 槽(+0x40~0x57)形态:内联截断 or 堆指针化。若指针化则 deref 判真体。
needle=嘻嘻~c21x + 'X'*32(43B)。"""
import lldb
import os

OUT = "/tmp/wxsend3/r21"
OFF_BP = 0x435E070
PEER = b"filehelper"

_st = {"bp": None, "slide": 0, "done": False, "n": 0, "stray": 0}


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
    bp.SetScriptCallbackFunction("cap21.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} bp={slide + OFF_BP:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        mc = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        head = _read(proc, mc, 0x58) or b""
        if head[0:16] != PEER + b"\x00" * (16 - len(PEER)):
            return False  # 杂项:静默放行(stray 不记,减 IO)
        _st["n"] += 1
        blob = _read(proc, mc, 0x270) or b""
        lines = [f"slide={_st['slide']:#x} mc={mc:#x}",
                 f"slot40_58={blob[0x40:0x58].hex()}",
                 f"msgctx270={blob.hex()}"]
        # body 槽若非内联(无 needle 前缀),尝试 +0x40 起 8B 当小端指针 deref
        if blob[0x40:0x40 + 6] != b"\xe5\x98\xbb\xe5\x98\xbb~":
            p64 = int.from_bytes(blob[0x40:0x48], "little")
            if 0x1000000000 < p64 < 0x800000000000:
                d = _read(proc, p64, 96)
                lines.append(f"deref_{p64:#x}={d.hex() if d else 'ERR'}")
        with open(f"{OUT}/hit{_st['n']}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if _st["n"] >= 3:
            _st["done"] = True
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
