"""cap16(直发验证终轮):断 L3=FUN_0433c5f0(同步 spawner)——
真发捕四参模板(x0 svc/x1 msgctx 0x270/x2 continuation 0x40/x3 flag)
→ 同会话 expr 直调(三槽补丁+原样 continuation)→ 回执验证。
needle=嘻嘻~c16s;失败红线=异常即停零伤。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r16"
OFF_L3 = 0x433C5F0
NEEDLE = "嘻嘻~c16s".encode("utf-8")

_st = {"bp": None, "slide": 0, "done": False, "t0": time.time()}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def install(debugger):
    target = debugger.GetSelectedTarget()
    slide = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().getLoadAddress if False else m.GetObjectFileHeaderAddress().GetLoadAddress(target)
            break
    if slide is None:
        return
    _st["slide"] = slide
    bp = target.BreakpointCreateByAddress(slide + OFF_L3)
    bp.SetScriptCallbackFunction("cap16.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        slide = _st["slide"]
        x0 = frame.FindRegister("x0")
        x1 = frame.FindRegister("x1")
        x2 = frame.FindRegister("x2")
        x3 = frame.FindRegister("x3")
        svc = x0.GetValueAsUnsigned() if x0 and x0.IsValid() else 0
        mc = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        ct = x2.GetValueAsUnsigned() if x2 and x2.IsValid() else 0
        fl = x3.GetValueAsUnsigned() if x3 and x3.IsValid() else 0
        blob = _read(proc, mc, 0x270) or b""
        if NEEDLE not in blob:
            with open(f"{OUT}/stray.log", "a") as f:
                f.write(f"svc={svc:#x} mc={mc:#x} ct={ct:#x} fl={fl:#x} len={len(blob)}\n")
            return False
        _st["done"] = True
        cont = _read(proc, ct, 0x40) or b""
        svc_hex = (_read(proc, svc, 0x20) or b"").hex()
        lines = [f"slide={slide:#x} svc={svc:#x} mc={mc:#x} ct={ct:#x} flag={fl:#x}",
                 f"svc_hex={svc_hex}",
                 f"msgctx270={blob.hex()}",
                 f"cont40={cont.hex()}"]
        with open(f"{OUT}/hit1.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        with open(f"{OUT}/DONE", "w") as f:
            f.write("hit1\n")
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
