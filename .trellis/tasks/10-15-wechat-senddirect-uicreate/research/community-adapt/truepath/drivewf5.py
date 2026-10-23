# -*- coding: utf-8 -*-
"""truepath 第五窗 driver:ARMED5 后 1.5s 发 needle(嘻嘻~wf107);
t=2s 起驱动线程尝试 RUNNING 态活体堆扫(每 4s 一次至 t=28s,失败无害,
停机扫由心跳兜底);触发返回后守望 40s;收尾禁断点/删观察点+限时 Detach,
EXIT5 照写,SIGTERM 兜底交编排器。纯读零写。"""
import os
import subprocess
import threading
import time

import lldb
import capwf5

OUT = capwf5.OUT
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT = "嘻嘻~wf107"

for _ in range(200):
    if os.path.exists(f"{OUT}/ARMED5"):
        break
    time.sleep(0.1)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
trig = {"t0": time.time(), "rc": None}


def _trigger():
    time.sleep(1.5)
    rcs = []
    for attempt in (1, 2):
        try:
            p = subprocess.run(
                ["bash", "-c", "printf '%s' | '%s' send_text filehelper --file -" % (TXT, BRIDGE)],
                capture_output=True, text=True, timeout=120)
            rcs.append(p.returncode)
            if attempt == 1:
                try:
                    with open(f"{OUT}/trigger5_stdout.txt", "w") as f:
                        f.write((p.stdout or "")[-4000:] + "\n--stderr--\n" + (p.stderr or "")[-4000:])
                except OSError:
                    pass
            if p.returncode == 0:
                break
        except subprocess.TimeoutExpired:
            rcs.append("TIMEOUT")
        time.sleep(8)
    trig["rc"] = rcs[-1] if rcs else "NONE"
    with open(f"{OUT}/trigger5.log", "w") as f:
        f.write("rcs=%s final=%s elapsed=%.1fs\n" % (rcs, trig["rc"], time.time() - trig["t0"]))


def _live_scanner():
    i = 0
    while i < 7 and not capwf5._st["watched"] and time.time() - capwf5._st["t0"] < 40:
        time.sleep(4)
        i += 1
        if capwf5._st["watched"] or trig["rc"] is None and time.time() - capwf5._st["t0"] < 6:
            continue
        try:
            capwf5._st["scans"] += 1
            hits = capwf5.heap_scan(proc, "live%d" % i)
            if hits:
                capwf5._st["scan_hits"] = hits
                with open(f"{OUT}/live_found.txt", "w") as f:
                    f.write("live scan %d found %d\n" % (i, len(hits)))
                break
        except Exception as exc:
            with open(f"{OUT}/live_scan_err.log", "a") as f:
                f.write(repr(exc) + "\n")


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=lambda: proc.Continue(), daemon=True).start()
threading.Thread(target=_live_scanner, daemon=True).start()

rc_at = {"t": None}
deadline = time.time() + 170
while time.time() < deadline:
    if trig["rc"] is not None and rc_at["t"] is None:
        rc_at["t"] = time.time()
    if rc_at["t"] and time.time() - rc_at["t"] > 40:
        break
    time.sleep(0.2)

time.sleep(1.0)
for w in list(capwf5._st["w"]):
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
        with open(f"{OUT}/detach5_err.log", "w") as f:
            f.write(repr(exc) + "\n")


t = threading.Thread(target=_detach, daemon=True)
t.start()
t.join(timeout=10)
with open(f"{OUT}/EXIT5", "w") as f:
    f.write("hb=%d scans=%d wn=%d done=%s rc=%s detach_done=%s\n"
            % (capwf5._st["n"], capwf5._st["scans"], capwf5._st["wn"],
               capwf5._st.get("done", ""), trig["rc"], not t.is_alive()))
