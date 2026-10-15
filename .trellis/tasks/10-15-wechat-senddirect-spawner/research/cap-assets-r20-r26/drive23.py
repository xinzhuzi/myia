# -*- coding: utf-8 -*-
"""drive23:发消息 A(拿 P 挂 watch)→3s→发消息 B(触发复用读)→观察窗 45s。"""
import os
import subprocess
import threading
import time

import lldb
import cap23  # noqa: F401

OUT = "/tmp/wxsend3/r23"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT_A = '嘻嘻~c25z' + 'X' * 32
TXT_B = '嘻嘻~c26z' + 'Z' * 32

for _ in range(100):
    if os.path.exists(f"{OUT}/ARMED"):
        break
    time.sleep(0.1)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
_trig = {"rc": None, "t0": time.time(), "a_rc": None, "b_rc": None}


def _send(txt, key):
    p = subprocess.run(["bash", "-c", "printf '%s' | '%s' send_text filehelper --file -" % (txt, BRIDGE)],
                       capture_output=True, text=True, timeout=90)
    _trig[key] = p.returncode
    with open(f"{OUT}/trigger_{key}.log", "w") as f:
        f.write(f"rc={p.returncode}\n{p.stdout}\n{p.stderr}\n")


def _trigger():
    time.sleep(1.5)
    _send(TXT_A, "a_rc")
    for _ in range(60):
        if os.path.exists(f"{OUT}/WATCH_ARMED"):
            break
        time.sleep(0.5)
    time.sleep(3)
    _send(TXT_B, "b_rc")


def _continuer():
    try:
        proc.Continue()
    except Exception as exc:
        with open(f"{OUT}/cont_err.log", "w") as f:
            f.write(repr(exc) + "\n")


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=_continuer, daemon=True).start()

deadline = time.time() + 170
while time.time() < deadline:
    if os.path.exists(f"{OUT}/STOP"):
        break
    if _trig.get("b_rc") is not None and time.time() - max(_trig.get("_b_t", 0), 0) > 45:
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
for w in target.watchpoint_iter():
    w.SetEnabled(False)
try:
    proc.Detach()
except Exception as exc:
    with open(f"{OUT}/detach_err.log", "w") as f:
        f.write(repr(exc) + "\n")
with open(f"{OUT}/EXIT", "w") as f:
    f.write(f"hits={cap23._st['n']} P={cap23._st['P']:#x} whits={cap23._st['whits']}\n")
