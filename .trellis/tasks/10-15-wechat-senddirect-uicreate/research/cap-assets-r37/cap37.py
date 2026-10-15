"""cap37(窗口2:Req2Buf 组锁定):断 MMStartTask(0x597eda0),时域门=
发送窗内首个命中→dump task→read watch 挂 task 头 0x100→轮询采栈。
读者=protobuf 编码/Req2Buf 族;与 4.1.12 组 delta(enter+0x80=blrX8,
enter+0xEC8=exit)交叉验证。零写入。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r37"
OFF_MMST = 0x597EDA0
PREFIX = "嘻嘻~c58s".encode("utf-8")[:6]  # 时域门不判内容,记录用

_st = {"bp": None, "slide": 0, "t0": time.time(), "armed": False, "task": 0}


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
    bp = target.BreakpointCreateByAddress(slide + OFF_MMST)
    bp.SetScriptCallbackFunction("cap37.on_mmst")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} t0={_st['t0']:.0f}\n")


def on_mmst(frame, bp_loc, internal_dict):
    try:
        if _st["armed"]:
            return False
        t = time.time() - _st["t0"]
        if not (4.0 < t < 40.0):
            return False
        _st["armed"] = True
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        task = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        _st["task"] = task
        tb = _read(proc, task, 0x100) or b""
        with open(f"{OUT}/task.txt", "w") as f:
            f.write(f"t={t:.1f} task={task:#x}\ntask100={tb.hex()}\n")
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        wp = proc.GetTarget().WatchAddress(task, 0x100, True, False, lldb.SBError())
        if wp and wp.IsValid():
            _st["wp"] = wp
            with open(f"{OUT}/WATCH_ARMED", "w") as f:
                f.write(f"task={task:#x}\n")
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
