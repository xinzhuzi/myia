# -*- coding: utf-8 -*-
"""truepath driver:ARMED 后 1.5s 用 printf 管道经桥的 send_text 链发 needle
(嘻嘻~wf101 → filehelper;形态照抄 main-r4/drive41.py:30)。守望到触发返回
+12s 宽限 → Stop → 禁全部断点/观察点 → detach → EXIT 文件。纯读零写。"""
import os
import subprocess
import threading
import time

import lldb
import capwf  # noqa: F401  (import 即装断点)

OUT = capwf.OUT
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT = "嘻嘻~wf101"

for _ in range(200):
    if os.path.exists(f"{OUT}/ARMED"):
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
            with open(f"{OUT}/trigger_stdout.txt", "w") as f:
                f.write((p.stdout or "")[-4000:] + "\n--stderr--\n" + (p.stderr or "")[-4000:])
        except OSError:
            pass
    except subprocess.TimeoutExpired:
        trig["rc"] = "TIMEOUT"
    with open(f"{OUT}/trigger.log", "w") as f:
        f.write("rc=%s elapsed=%.1fs\n" % (trig["rc"], time.time() - trig["t0"]))


def _continuer():
    try:
        proc.Continue()
    except Exception as exc:
        with open(f"{OUT}/cont_err.log", "w") as f:
            f.write(repr(exc) + "\n")


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=_continuer, daemon=True).start()

rc_at = {"t": None}
deadline = time.time() + 160
while time.time() < deadline:
    if trig["rc"] is not None and rc_at["t"] is None:
        rc_at["t"] = time.time()
    if rc_at["t"] and time.time() - rc_at["t"] > 12:
        break
    time.sleep(0.2)

time.sleep(1.0)


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
    f.write("hits=%d done=%s needle=%s rc=%s\n"
            % (capwf._st["n"], capwf._st.get("done", ""), capwf._st.get("needle_hits"), trig["rc"]))
