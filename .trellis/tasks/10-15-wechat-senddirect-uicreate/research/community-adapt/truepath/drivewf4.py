# -*- coding: utf-8 -*-
"""truepath 第四窗 driver:ARMED4 后 1.5s printf 管道发 needle(嘻嘻~wf104);
触发返回后守望 40s;收尾禁断点/删观察点,Detach 限时守护线程,EXIT4 照写,
SIGTERM 兜底交编排器。纯读零写。"""
import os
import subprocess
import threading
import time

import lldb
import capwf4  # noqa: F401

OUT = capwf4.OUT
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT = "嘻嘻~wf104"

for _ in range(200):
    if os.path.exists(f"{OUT}/ARMED4"):
        break
    time.sleep(0.1)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
trig = {"t0": time.time(), "rc": None}


def _trigger():
    time.sleep(1.5)
    try:
        p = subprocess.run(
            ["bash", "-c", "printf '%s' | '%s' send_text filehelper --file -" % (TXT, BRIDGE)],
            capture_output=True, text=True, timeout=120)
        trig["rc"] = p.returncode
        try:
            with open(f"{OUT}/trigger4_stdout.txt", "w") as f:
                f.write((p.stdout or "")[-4000:] + "\n--stderr--\n" + (p.stderr or "")[-4000:])
        except OSError:
            pass
    except subprocess.TimeoutExpired:
        trig["rc"] = "TIMEOUT"
    with open(f"{OUT}/trigger4.log", "w") as f:
        f.write("rc=%s elapsed=%.1fs\n" % (trig["rc"], time.time() - trig["t0"]))


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=lambda: proc.Continue(), daemon=True).start()

rc_at = {"t": None}
deadline = time.time() + 170
while time.time() < deadline:
    if trig["rc"] is not None and rc_at["t"] is None:
        rc_at["t"] = time.time()
    if rc_at["t"] and time.time() - rc_at["t"] > 40:
        break
    time.sleep(0.2)

time.sleep(1.0)
for w in list(capwf4._st["w"]):
    try:
        target.DeleteWatchpoint(w.GetID())
    except Exception:
        pass
for b in target.breakpoint_iter():
    b.SetEnabled(False)


def _detach():
    try:
        proc.Detach()
    except Exception as exc:
        with open(f"{OUT}/detach4_err.log", "w") as f:
            f.write(repr(exc) + "\n")


t = threading.Thread(target=_detach, daemon=True)
t.start()
t.join(timeout=10)
with open(f"{OUT}/EXIT4", "w") as f:
    f.write("hits=%d per=%s wn=%d done=%s rc=%s detach_done=%s\n"
            % (capwf4._st["n"], capwf4._st.get("per"), capwf4._st["wn"],
               capwf4._st.get("done", ""), trig["rc"], not t.is_alive()))
