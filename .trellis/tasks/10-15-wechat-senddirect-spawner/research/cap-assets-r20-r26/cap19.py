"""cap18(原地补丁终验):断 L3 入口→needle 门→就地改写活 msgctx
正文槽(+0x40 inline23+len 字节)→放行真实调用链发送补丁正文。
零直调零构造;微信侧=正常发送。正文=嘻嘻~直发c19v(13B)。"""
import lldb
import os

OUT = "/tmp/wxsend3/r19"
OFF_L3 = 0x433C5F0
NEEDLE = "嘻嘻~c19v".encode("utf-8")
FORGED = "嘻嘻~直发c19v".encode("utf-8")

_st = {"bp": None, "slide": 0, "done": False}


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
    bp = target.BreakpointCreateByAddress(slide + OFF_L3)
    bp.SetScriptCallbackFunction("cap18.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        mc = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        blob = _read(proc, mc, 0x270) or b""
        if NEEDLE not in blob:
            return False
        _st["n"] = _st.get("n", 0) + 1
        err = lldb.SBError()
        slot = bytearray(blob[0x40:0x40 + 24])
        slot2 = bytearray(24)
        slot2[0:len(FORGED)] = FORGED
        slot2[23] = len(FORGED)
        ok = proc.WriteMemory(mc + 0x40, bytes(slot2), err)
        with open(f"{OUT}/PATCHED", "w") as f:
            f.write(f"mc={mc:#x} wrote={ok} err={err.Success()} forged={FORGED.decode()}\n")
        with open(f"{OUT}/PATCH{_st['n']}", "w") as f:
            f.write(f"mc={mc:#x}\n")
        if _st["n"] >= 5:
            _st["done"] = True
            if _st["bp"] is not None:
                _st["bp"].SetEnabled(False)
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False  # 放行:真实 L3 带补丁正文跑


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
