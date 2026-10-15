# -*- coding: utf-8 -*-
"""drive12 — cap19 时间线驱动(GIL 修正版):Continue 在子线程,主线程守
STOP/触发完成+宽限 → Stop → 禁断点 → Detach。"""
import os
import subprocess
import threading
import time

import lldb
import cap19  # noqa: F401

OUT = "/tmp/wxsend3/r19"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
SEND = "printf '嘻嘻~c19v' | '%s' send_text filehelper --file -" % BRIDGE

for _ in range(100):
    if os.path.exists(f"{OUT}/ARMED"):
        break
    time.sleep(0.1)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
_trig = {"rc": None, "t0": time.time()}


def _trigger():
    time.sleep(1.5)
    p = subprocess.run(["bash", "-c", SEND], capture_output=True, text=True, timeout=90)
    _trig["rc"] = p.returncode
    _trig["t_end"] = time.time()
    with open(f"{OUT}/trigger.log", "w") as f:
        f.write(f"rc={p.returncode} elapsed={_trig['t_end'] - _trig['t0']:.1f}s\n{p.stdout}\n{p.stderr}\n")
    _trig["done"] = True


def _continuer():
    try:
        proc.Continue()
    except Exception as exc:
        with open(f"{OUT}/cont_err.log", "w") as f:
            f.write(repr(exc) + "\n")


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=_continuer, daemon=True).start()

deadline = time.time() + 120
while time.time() < deadline:
    if os.path.exists(f"{OUT}/STOP"):
        break
    if _trig["rc"] is not None and time.time() - _trig.get("t_end", 0) > 12:
        break
    time.sleep(0.5)

try:
    proc.Stop()
except Exception:
    pass
time.sleep(0.5)
for b in target.breakpoint_iter():
    b.SetEnabled(False)
try:
    proc.Detach()
except Exception as exc:
    with open(f"{OUT}/detach_err.log", "w") as f:
        f.write(repr(exc) + "\n")
with open(f"{OUT}/EXIT", "w") as f:
    f.write(f"hits={cap19._st['hits']}\n")
