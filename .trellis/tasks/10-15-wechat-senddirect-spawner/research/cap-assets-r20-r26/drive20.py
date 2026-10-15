# -*- coding: utf-8 -*-
"""drive20 — cap20 时间线驱动(drive19 GIL 修正版底子):
Continue 在子线程;主线程守 STOP/触发完成+宽限(25s,覆盖 12-30s 回显窗)
→ Stop 守护线程化(卡死不再冻结主流程)→ 禁断点 → Detach → EXIT(修 'hits'键 bug)。"""
import os
import subprocess
import threading
import time

import lldb
import cap20  # noqa: F401

OUT = "/tmp/wxsend3/r20"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
SEND = "printf '嘻嘻~c20w' | '%s' send_text filehelper --file -" % BRIDGE

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

deadline = time.time() + 150
while time.time() < deadline:
    if os.path.exists(f"{OUT}/STOP"):
        break
    if _trig["rc"] is not None and time.time() - _trig.get("t_end", 0) > 25:
        break
    time.sleep(0.5)


def _stopper():
    try:
        proc.Stop()
    except Exception as exc:
        with open(f"{OUT}/stop_err.log", "w") as f:
            f.write(repr(exc) + "\n")


t_stop = threading.Thread(target=_stopper, daemon=True)
t_stop.start()
t_stop.join(timeout=10)  # Stop 卡死不冻结主流程(红线2:挂死由外部 SIGTERM 收)
time.sleep(0.5)
for b in target.breakpoint_iter():
    b.SetEnabled(False)
try:
    proc.Detach()
except Exception as exc:
    with open(f"{OUT}/detach_err.log", "w") as f:
        f.write(repr(exc) + "\n")
with open(f"{OUT}/EXIT", "w") as f:
    f.write(f"hits={cap20._st['n']} stray={cap20._st['stray']} done={cap20._st['done']}\n")
