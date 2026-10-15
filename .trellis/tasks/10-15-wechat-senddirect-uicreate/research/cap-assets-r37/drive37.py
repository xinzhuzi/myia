# -*- coding: utf-8 -*-
"""drive37:发送(needle c58s)→守望 stop 态采栈+Continue(读者链)→收尾。"""
import os
import subprocess
import threading
import time

import lldb
import cap37  # noqa: F401

OUT = "/tmp/wxsend3/r37"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT = '嘻嘻~c58s'

for _ in range(100):
    if os.path.exists(f"{OUT}/ARMED"):
        break
    time.sleep(0.1)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
_trig = {"t0": time.time()}
_st = {"whits": 0}


def _trigger():
    time.sleep(1.5)
    try:
        p = subprocess.run(["bash", "-c", "printf '%s' | '%s' send_text filehelper --file -" % (TXT, BRIDGE)],
                           capture_output=True, text=True, timeout=90)
        rc = p.returncode
    except subprocess.TimeoutExpired as e:
        rc = "TIMEOUT"
    _trig["rc"] = rc
    with open(f"{OUT}/trigger.log", "w") as f:
        f.write(f"rc={rc} elapsed={time.time() - _trig['t0']:.1f}s\n")


def _continuer():
    try:
        proc.Continue()
    except Exception as exc:
        with open(f"{OUT}/cont_err.log", "w") as f:
            f.write(repr(exc) + "\n")


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=_continuer, daemon=True).start()

STOPPED = lldb.eStateStopped
slide = cap37._st["slide"]
deadline = time.time() + 200
while time.time() < deadline:
    if os.path.exists(f"{OUT}/STOP"):
        break
    try:
        state = proc.GetState()
    except Exception:
        state = -1
    if state == STOPPED and cap37._st.get("task"):
        _st["whits"] += 1
        n = _st["whits"]
        try:
            th = proc.GetSelectedThread()
            lines = [f"whit={n} t={time.time() - _trig['t0']:.1f} tid={th.GetIndexID()}"]
            for i in range(min(14, th.GetNumFrames())):
                f = th.GetFrameAtIndex(i)
                pc = f.GetPC()
                rva = pc - slide if slide <= pc < slide + 0x10000000 else 0
                lines.append(f"  #{i} pc={pc:#x} rva={rva:#x} fn={f.GetFunctionName()}")
            with open(f"{OUT}/watch{n}.txt", "w") as f:
                f.write("\n".join(lines) + "\n")
        except Exception as exc:
            with open(f"{OUT}/err.log", "a") as f:
                f.write("stack:" + repr(exc) + "\n")
        try:
            proc.Continue()
        except Exception:
            pass
        if n >= 12:
            break
        continue
    if _trig.get("rc") is not None and time.time() - _trig.get("t_rc", time.time()) > 0:
        if not _trig.get("t_rc"):
            _trig["t_rc"] = time.time()
    if _trig.get("t_rc") and time.time() - _trig["t_rc"] > 30:
        break
    time.sleep(0.15)


def _stopper():
    try:
        proc.Stop()
    except Exception:
        pass


t = threading.Thread(target=_stopper, daemon=True)
t.start()
t.join(timeout=8)
time.sleep(0.5)
for b in target.breakpoint_iter():
    b.SetEnabled(False)
for w in target.watchpoint_iter():
    w.SetEnabled(False)
try:
    proc.Detach()
except Exception as exc:
    with open(f"{OUT}/detach_err.log", "w") as f:
        f.write(repr(exc) + "\n")
with open(f"{OUT}/EXIT", "w") as f:
    f.write(f"whits={_st['whits']} task={cap37._st['task']:#x}\n")
