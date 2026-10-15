"""cap27a(剪贴板读取锚点):符号断 -[NSPasteboard dataForType:]。
微信粘贴(cmd+V)必经;群消息不碰剪贴板=天然安静。全记录命中
(限 12 次):时间+16 帧栈。判读:命中时序≈粘贴时刻,栈=Qt paste 链。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r27"
SYM = "-[NSPasteboard dataForType:]"

_st = {"bp": None, "t0": time.time(), "n": 0}


def install(debugger):
    target = debugger.GetSelectedTarget()
    bp = target.BreakpointCreateByName(SYM)
    if not bp.IsValid() or bp.GetNumLocations() == 0:
        bp = target.BreakpointCreateByName("-[NSPasteboard _dataForType:index:usesPboardTypes:combinesItems:securityScoped:]")
    bp.SetScriptCallbackFunction("cap27.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"sym_locs={bp.GetNumLocations()}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        n = _st["n"]
        thread = frame.GetThread()
        lines = [f"n={n} t={time.time() - _st['t0']:.1f} tid={thread.GetIndexID()}"]
        for i in range(min(16, thread.GetNumFrames())):
            f = thread.GetFrameAtIndex(i)
            lines.append(f"  #{i} pc={f.GetPC():#x} fn={f.GetFunctionName()}")
        with open(f"{OUT}/hit{n}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if n >= 12:
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
