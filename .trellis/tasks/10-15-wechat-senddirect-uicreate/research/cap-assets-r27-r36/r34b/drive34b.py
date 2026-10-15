# -*- coding: utf-8 -*-
"""drive34b:等 ARMED→发 needle(嘻嘻~c35z+Z×32)→rc 后沉降 12s→写 STOP
(由回调线程自禁断点,规避脚本线程 Stop/Detach 死锁)→等
EXIT/CALLBACK_SHUTDOWN 25s→兜底守护线程 Detach→EXIT。"""
import os
import subprocess
import threading
import time

import lldb
import cap34b  # noqa: F401

OUT = "/tmp/wxsend3/r34b"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT = "嘻嘻~c35z" + "Z" * 32

armed_ok = False
for _ in range(100):
    if os.path.exists(f"{OUT}/ANCHOR_MISMATCH") or os.path.exists(f"{OUT}/ARMED"):
        armed_ok = os.path.exists(f"{OUT}/ARMED") and not os.path.exists(f"{OUT}/ANCHOR_MISMATCH")
        break
    time.sleep(0.1)

if not armed_ok:
    with open(f"{OUT}/EXIT", "w") as f:
        f.write("abort: anchor mismatch or arm fail\n")
    raise SystemExit(0)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
_trig = {"t0": time.time(), "rc": None}


def _trigger():
    time.sleep(1.5)
    p = subprocess.run(
        ["bash", "-c", "printf '%s' | '%s' send_text filehelper --file -" % (TXT, BRIDGE)],
        capture_output=True, text=True, timeout=120,
    )
    _trig["rc"] = p.returncode
    _trig["t_rc"] = time.time()
    with open(f"{OUT}/trigger.log", "w") as f:
        f.write("rc=%d elapsed=%.1fs\n%s\n%s\n" % (p.returncode, time.time() - _trig["t0"], p.stdout, p.stderr))


def _continuer():
    try:
        proc.Continue()
    except Exception as exc:
        with open(f"{OUT}/cont_err.log", "w") as f:
            f.write(repr(exc) + "\n")


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=_continuer, daemon=True).start()

deadline = time.time() + 200
while time.time() < deadline:
    rc_t = _trig.get("t_rc")
    if rc_t is not None and time.time() - rc_t > 12:
        break
    time.sleep(0.5)

with open(f"{OUT}/STOP", "w") as f:
    f.write("stop\n")
# 等回调线程自禁(热断点应秒级再来一击;冷则超时)
for _ in range(50):
    if os.path.exists(f"{OUT}/CALLBACK_SHUTDOWN") or os.path.exists(f"{OUT}/DONE_MANY"):
        break
    time.sleep(0.5)


def _detacher():
    try:
        proc.Detach()
    except Exception as exc:
        with open(f"{OUT}/detach_err.log", "w") as f:
            f.write(repr(exc) + "\n")


t = threading.Thread(target=_detacher, daemon=True)
t.start()
t.join(timeout=8)
with open(f"{OUT}/EXIT", "w") as f:
    f.write(
        "n=%d patches=%d rc=%s elapsed=%.1fs\n"
        % (cap34b._st["n"], cap34b._st["patches"], _trig["rc"], time.time() - _trig["t0"])
    )
