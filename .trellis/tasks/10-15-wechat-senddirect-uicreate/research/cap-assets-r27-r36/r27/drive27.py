# -*- coding: utf-8 -*-
"""drive26:发 A(43B W 尾)→等 DONE(正本猎杀完成)→15s 后收尾。"""
import os
import subprocess
import threading
import time

import lldb
import cap27  # noqa: F401

OUT = "/tmp/wxsend3/r27"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT_A = '嘻嘻~c32u'

for _ in range(100):
    if os.path.exists(f"{OUT}/ARMED"):
        break
    time.sleep(0.1)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
_trig = {"t0": time.time()}


def _trigger():
    time.sleep(1.5)
    p = subprocess.run(["bash", "-c", "printf '%s' | '%s' send_text filehelper --file -" % (TXT_A, BRIDGE)],
                       capture_output=True, text=True, timeout=90)
    _trig["rc"] = p.returncode
    with open(f"{OUT}/trigger.log", "w") as f:
        f.write(f"rc={p.returncode}\n{p.stdout}\n{p.stderr}\n")


def _continuer():
    try:
        proc.Continue()
    except Exception as exc:
        with open(f"{OUT}/cont_err.log", "w") as f:
            f.write(repr(exc) + "\n")


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=_continuer, daemon=True).start()

deadline = time.time() + 150
while time.time() < deadline:
    if os.path.exists(f"{OUT}/STOP"):
        break
    if os.path.exists(f"{OUT}/DONE") and time.time() - _trig.get("t_done", 0) > 1:
        if not _trig.get("t_done"):
            _trig["t_done"] = time.time()
    if _trig.get("t_done") and time.time() - _trig["t_done"] > 15:
        break
    time.sleep(0.5)


def _stopper():
    try:
        proc.Stop()
    except Exception:
        pass


t = threading.Thread(target=_stopper, daemon=True)
t.start()
t.join(timeout=10)
time.sleep(0.5)
for b in target.breakpoint_iter():
    b.SetEnabled(False)
try:
    proc.Detach()
except Exception as exc:
    with open(f"{OUT}/detach_err.log", "w") as f:
        f.write(repr(exc) + "\n")
with open(f"{OUT}/EXIT", "w") as f:
    f.write("end\n")
