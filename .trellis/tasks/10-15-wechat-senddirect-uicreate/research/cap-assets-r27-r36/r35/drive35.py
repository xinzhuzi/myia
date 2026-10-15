# -*- coding: utf-8 -*-
"""drive24:A 发送→挂 read watch→B 发送→守望循环发现进程 stopped 采集栈+Continue。"""
import os
import subprocess
import threading
import time

import lldb
import cap35  # noqa: F401

OUT = "/tmp/wxsend3/r24"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT_A = '嘻嘻~c52r'
TXT_B = '嘻嘻~c53r'

for _ in range(100):
    if os.path.exists(f"{OUT}/ARMED"):
        break
    time.sleep(0.1)

dbg = lldb.debugger
target = dbg.GetSelectedTarget()
proc = target.GetProcess()
_trig = {"t0": time.time()}
_st = {"whits": 0}


def _send(txt, key):
    try:
        p = subprocess.run(["bash", "-c", "printf '%s' | '%s' send_text filehelper --file -" % (txt, BRIDGE)],
                           capture_output=True, text=True, timeout=90)
        rc = p.returncode
        out, err = p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        rc, out, err = "TIMEOUT", str(e), ""
    _trig[key] = rc
    with open(f"{OUT}/trigger_{key}.log", "w") as f:
        f.write(f"rc={rc}\n{out}\n{err}\n")


def _trigger():
    time.sleep(1.5)
    _send(TXT_A, "a_rc")
    for _ in range(120):
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

STOPPED = lldb.eStateStopped
slide = cap35._st["slide"]
deadline = time.time() + 170
last_t = time.time()
while time.time() < deadline:
    if os.path.exists(f"{OUT}/STOP"):
        break
    try:
        state = proc.GetState()
    except Exception:
        state = -1
    if state == STOPPED and cap35._st.get("P"):
        # watchpoint/breakpoint 触发停机:采集触发线程栈
        _st["whits"] += 1
        try:
            th = proc.GetSelectedThread()
            lines = [f"whit={_st['whits']} t={time.time() - _trig['t0']:.1f} tid={th.GetIndexID()}"]
            for i in range(min(16, th.GetNumFrames())):
                f = th.GetFrameAtIndex(i)
                pc = f.GetPC()
                rva = pc - slide if slide <= pc < slide + 0x10000000 else 0
                lines.append(f"  #{i} pc={pc:#x} rva={rva:#x} fn={f.GetFunctionName()}")
            with open(f"{OUT}/watch{_st['whits']}.txt", "w") as f:
                f.write("\n".join(lines) + "\n")
        except Exception as exc:
            with open(f"{OUT}/err.log", "a") as f:
                f.write("stack:" + repr(exc) + "\n")
        try:
            proc.Continue()
        except Exception as exc:
            with open(f"{OUT}/err.log", "a") as f:
                f.write("cont:" + repr(exc) + "\n")
        last_t = time.time()
    if _trig.get("b_rc") is not None and time.time() - last_t > 45:
        break
    time.sleep(0.2)


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
    f.write(f"P={cap35._st['P']:#x} whits={_st['whits']}\n")
