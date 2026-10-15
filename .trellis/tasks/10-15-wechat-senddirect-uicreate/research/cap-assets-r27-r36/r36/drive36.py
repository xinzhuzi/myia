# -*- coding: utf-8 -*-
"""drive36:等 ARMED→发 needle→等 WATCH_PENDING(粘贴转换命中)→+2.5s
Stop→扫 Q±32MB 找 needle 副本→前 3 挂 read watch→Continue→轮询采栈
(WATCH_ARMED 后 45s)→STOP 哨兵→禁全部→detach→EXIT。"""
import os
import subprocess
import threading
import time

import lldb
import cap36  # noqa: F401

OUT = "/tmp/wxsend3/r36"
BRIDGE = os.path.expanduser("~/.myia/plugins/wechat-bridge/bin/wechat-bridge")
TXT = "嘻嘻~c38z"
SCAN_HALF = 0x2000000          # ±32MB
SCAN_STEP = 0x400000           # 4MB 步进
N8P = TXT.encode("utf-8")
N16P = TXT.encode("utf-16-le")
PATTERNS = (N16P, N8P)         # u16 优先(本窗 needle 短,内联形态)


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def scan_copies(proc, q):
    base = q - SCAN_HALF
    total = SCAN_HALF * 2
    step = SCAN_STEP
    overlap = max(len(p) for p in PATTERNS) - 1
    prev_tail = b""
    found = []
    for off in range(0, total, step):
        chunk = _read(proc, base + off, step)
        if chunk is None:
            for sub in range(0, step, 0x10000):
                c2 = _read(proc, base + off + sub, 0x10000)
                if c2 is None:
                    prev_tail = b""
                    continue
                hay = prev_tail + c2
                for pat in PATTERNS:
                    idx = hay.find(pat)
                    while idx >= 0:
                        a = base + off + sub - len(prev_tail) + idx
                        if a > 0:
                            found.append(a)
                        idx = hay.find(pat, idx + 1)
                prev_tail = c2[-overlap:]
            continue
        hay = prev_tail + chunk
        for pat in PATTERNS:
            idx = hay.find(pat)
            while idx >= 0:
                a = base + off - len(prev_tail) + idx
                if a > 0:
                    found.append(a)
                idx = hay.find(pat, idx + 1)
        prev_tail = chunk[-overlap:]
    return sorted(set(found))


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
_w = {"armed_t": None, "count": 0}


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


def _capture(thread, tag):
    slide = cap36._st["slide"]
    lines = ["cap=%d t=%.1f tag=%s" % (_w["count"], time.time(), tag)]
    for i in range(min(12, thread.GetNumFrames())):
        f2 = thread.GetFrameAtIndex(i)
        pc = f2.GetPC()
        rva = pc - slide if slide <= pc < slide + 0x10000000 else 0
        lines.append("  #%d pc=%#x rva=%#x fn=%s" % (i, pc, rva, f2.GetFunctionName()))
    with open(f"{OUT}/read%d.txt" % _w["count"], "w") as f:
        f.write("\n".join(lines) + "\n")


def _watch_steward():
    # 等 WATCH_PENDING(转换命中,驱动侧接管)
    for _ in range(600):
        if os.path.exists(f"{OUT}/WATCH_PENDING"):
            break
        time.sleep(0.25)
    else:
        return
    time.sleep(2.5)
    q = cap36._st["Q"]
    try:
        proc.Stop()
        time.sleep(0.3)
        copies = scan_copies(proc, q)
        picks = [a for a in copies if abs(a - q) > 0x100][:3]
        werr = lldb.SBError()
        armed = []
        for a in picks:
            wp = target.WatchAddress(a, 0x20, True, False, werr)
            if wp and wp.IsValid():
                armed.append(a)
        with open(f"{OUT}/WATCH_ARMED", "w") as f:
            f.write("Q=%#x copies=%d picks=%s\n" % (q, len(copies), [hex(a) for a in picks]))
        _w["armed_t"] = time.time()
        proc.Continue()
    except Exception as exc:
        with open(f"{OUT}/steward_err.log", "w") as f:
            f.write(repr(exc) + "\n")
        try:
            proc.Continue()
        except Exception:
            pass


def _poller():
    # 采栈循环:只在 watch 停机时抓栈并 Continue
    while True:
        if _w["armed_t"] is None:
            if os.path.exists(f"{OUT}/STOP") or time.time() - _trig["t0"] > 170:
                return
            time.sleep(0.05)
            continue
        if time.time() - _w["armed_t"] > 45 or os.path.exists(f"{OUT}/STOP"):
            return
        try:
            if proc.GetState() == lldb.eStateStopped:
                hit = False
                for th in proc:
                    if th.GetStopReason() == lldb.eStopReasonWatchpoint:
                        _w["count"] += 1
                        _capture(th, "wp")
                        hit = True
                        break
                proc.Continue()
                if not hit and _w["count"] == 0:
                    pass  # bp 停机自动续
        except Exception:
            pass
        time.sleep(0.025)


def _continuer():
    time.sleep(0.2)
    try:
        proc.Continue()
    except Exception:
        pass


threading.Thread(target=_trigger, daemon=True).start()
threading.Thread(target=_continuer, daemon=True).start()
threading.Thread(target=_watch_steward, daemon=True).start()
threading.Thread(target=_poller, daemon=True).start()

deadline = time.time() + 190
while time.time() < deadline:
    if os.path.exists(f"{OUT}/STOP"):
        break
    rc_t = _trig.get("t_rc")
    wt = _w.get("armed_t")
    if rc_t is not None and wt is not None and time.time() - wt > 50:
        break
    if rc_t is not None and wt is None and time.time() - rc_t > 40:
        break
    time.sleep(0.5)

with open(f"{OUT}/STOP", "w") as f:
    f.write("stop\n")
time.sleep(1.0)


def _stopper():
    try:
        proc.Stop()
    except Exception:
        pass


t = threading.Thread(target=_stopper, daemon=True)
t.start()
t.join(timeout=8)
time.sleep(0.3)
for b in target.breakpoint_iter():
    b.SetEnabled(False)
for w in target.watchpoint_iter():
    w.SetEnabled(False)


def _detacher():
    try:
        proc.Detach()
    except Exception as exc:
        with open(f"{OUT}/detach_err.log", "w") as f:
            f.write(repr(exc) + "\n")


t2 = threading.Thread(target=_detacher, daemon=True)
t2.start()
t2.join(timeout=8)
with open(f"{OUT}/EXIT", "w") as f:
    f.write(
        "n=%d Q=%#x reads=%d rc=%s elapsed=%.1fs\n"
        % (cap36._st["n"], cap36._st["Q"], _w["count"], _trig["rc"], time.time() - _trig["t0"])
    )
