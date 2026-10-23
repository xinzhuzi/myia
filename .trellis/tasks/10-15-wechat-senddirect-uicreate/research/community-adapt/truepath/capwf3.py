"""truepath 第三窗:在 MMStartTask 0x597eda0(ADAPT-STATUS 实锤:真实发送命中3次)
截住发送任务,深扫 x0/x1 对象图找 needle(嘻嘻~wf*),对 needle 首地址下
硬件读观察点 → 谁读这段文本谁就是真·文本序列化现场;命中 dump pc/全寄存器/
栈回溯 rva。观察点/断点用后即禁;纯读零写零 patch。"""
import lldb
import os
import time

OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
NEEDLE = "嘻嘻~wf".encode("utf-8")
START_RVA = 0x597EDA0
MAX_W_HITS = 8
MAX_SECONDS = 150.0
SCAN_BUDGET = 400
SCAN_DEPTH = 5

_st = {"bp": None, "slide": 0, "t0": time.time(), "n": 0, "w": [], "wn": 0, "done": "", "found": []}


def _read(proc, addr, size):
    if not isinstance(addr, int) or addr < 0x10000 or addr > 0x7FFFFFFFFFFF:
        return None
    err = lldb.SBError()
    try:
        data = proc.ReadMemory(addr, size, err)
    except Exception:
        return None
    return data if err.Success() else None


def _u64(b, off):
    if b and len(b) >= off + 8:
        return int.from_bytes(b[off:off + 8], "little")
    return 0


def _ptr(v):
    return isinstance(v, int) and 0x100000000 <= v <= 0x7FFFFFFFFFFF and (v & 7) == 0


def _lit(raw):
    if not raw:
        return None
    i = raw.find(NEEDLE)
    if i < 0:
        return None, -1
    return raw[i:i + 16].split(b"\x00")[0].decode("utf-8", "replace"), i


def install(debugger):
    target = debugger.GetSelectedTarget()
    slide = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
            break
    if slide is None:
        return
    _st["slide"] = slide
    bp = target.BreakpointCreateByAddress(slide + START_RVA)
    bp.SetScriptCallbackFunction("capwf3.on_start")
    _st["bp"] = bp
    b = _read(target.GetProcess(), slide + START_RVA, 8)
    with open(f"{OUT}/ARMED3", "w") as f:
        f.write("slide=%#x start_rva=%#x locs=%d bytes=%s loaded=%s\n"
                % (slide, START_RVA, bp.GetNumLocations(), b.hex() if b else "ERR", time.strftime("%H:%M:%S")))


def _deep_scan(proc, root, label, log):
    """BFS 扫 root 对象图找 needle;返回 [(路径, 地址, 字面)]。"""
    budget = [SCAN_BUDGET]
    hits = []
    seen = set()

    def scan(path, addr, size, level):
        if budget[0] <= 0 or level < 0 or addr in seen or len(hits) >= 4:
            return
        seen.add(addr)
        raw = _read(proc, addr, size)
        if not raw:
            return
        budget[0] -= 1
        lit, i = _lit(raw)
        if lit:
            hits.append((path, addr + i, lit))
            log.append("NEEDLE %s+%#x=%s addr=%#x" % (path, i, lit, addr + i))
            log.append("CTX %s=%s" % (path, raw[max(0, i - 32):i + 48].hex()))
        if level == 0:
            return
        for off in range(0, min(len(raw), 0x60), 8):
            p = _u64(raw, off)
            if _ptr(p):
                scan("%s+%#x" % (path, off), p, 0x40, level - 1)

    scan(label, root, 0x80, SCAN_DEPTH)
    return hits


def on_start(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        n = _st["n"]
        if time.time() - _st["t0"] > MAX_SECONDS or _st["done"]:
            if _st["bp"]:
                _st["bp"].SetEnabled(False)
            return False
        proc = frame.GetThread().GetProcess()
        slide = _st["slide"]

        def reg(name):
            r = frame.FindRegister(name)
            try:
                return r.GetValueAsUnsigned() if r and r.IsValid() else 0
            except Exception:
                return 0

        regs = [reg("x%d" % i) for i in range(29)]
        log = ["start=%d t=%.1f tid=%d" % (n, time.time() - _st["t0"], frame.GetThread().GetIndexID())]
        log.append("regs=" + " ".join("x%d=%#x" % (i, v) for i, v in enumerate(regs)) + " lr_rva=%#x"
                   % ((reg("x30") - slide) if slide <= reg("x30") < slide + 0x20000000 else 0))
        hits = []
        for ix in (1, 0):
            if _ptr(regs[ix]):
                hits = _deep_scan(proc, regs[ix], "x%d" % ix, log)
                if hits:
                    break
        with open(f"{OUT}/start{n}.txt", "w") as f:
            f.write("\n".join(log) + "\n")
        if not hits:
            return False
        # needle 在手:下硬件读观察点(至多 2 个),禁 StartTask 断点
        target = proc.GetTarget()
        for path, addr, lit in hits[:2]:
            w = target.WatchpointCreateByAddress(addr, 8, True, False)
            if not (w and w.IsValid()):
                w = target.WatchpointCreateByAddress(addr, 8, True, True)  # arm64 兜底:读写都断
            if w and w.IsValid():
                w.SetScriptCallbackFunction("capwf3.on_watch")
                _st["w"].append(w)
                with open(f"{OUT}/watch_set.txt", "a") as f:
                    f.write("start=%d %s %s addr=%#x id=%d\n" % (n, path, lit, addr, w.GetID()))
        if _st["bp"]:
            _st["bp"].SetEnabled(False)
        _st["done"] = "WATCHING"
    except Exception as exc:
        try:
            with open(f"{OUT}/err3.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def on_watch(frame, wp, internal_dict):
    try:
        _st["wn"] += 1
        wn = _st["wn"]
        proc = frame.GetThread().GetProcess()
        slide = _st["slide"]
        th = frame.GetThread()

        def reg(name):
            r = frame.FindRegister(name)
            try:
                return r.GetValueAsUnsigned() if r and r.IsValid() else 0
            except Exception:
                return 0

        regs = [reg("x%d" % i) for i in range(29)]
        pc = frame.GetPC()
        rva = pc - slide if slide <= pc < slide + 0x20000000 else 0
        lines = ["watch=%d t=%.1f tid=%d pc=%#x rva=%#x fn=%s"
                 % (wn, time.time() - _st["t0"], th.GetIndexID(), pc, rva, frame.GetFunctionName())]
        lines.append("regs=" + " ".join("x%d=%#x" % (i, v) for i, v in enumerate(regs)))
        for i in range(min(18, th.GetNumFrames())):
            f = th.GetFrameAtIndex(i)
            fpc = f.GetPC()
            frva = fpc - slide if slide <= fpc < slide + 0x20000000 else 0
            lines.append("  #%d pc=%#x rva=%#x fn=%s" % (i, fpc, frva, f.GetFunctionName()))
        # 观察点现场对象:vtable 判读(x0/x1)
        for ix in (0, 1):
            v = regs[ix]
            if _ptr(v):
                ob = _read(proc, v, 0x20)
                if ob:
                    lines.append("w_x%d_obj@%#x=%s" % (ix, v, ob.hex()))
                    vt = _u64(ob, 0)
                    vt80 = _read(proc, vt, 0x80) if _ptr(vt) else None
                    if vt80:
                        slots = []
                        for i in range(0, 0x80, 8):
                            sv = _u64(vt80, i)
                            if slide <= sv < slide + 0x20000000:
                                slots.append("+%#x=rva%#x" % (i, sv - slide))
                        lines.append("w_x%d_vt=%s" % (ix, " ".join(slots) if slots else vt80.hex()))
        with open(f"{OUT}/watch%d.txt" % wn, "w") as f:
            f.write("\n".join(lines) + "\n")
        if wn >= MAX_W_HITS or time.time() - _st["t0"] > MAX_SECONDS:
            for w in _st["w"]:
                try:
                    proc.GetTarget().DeleteWatchpoint(w.GetID())
                except Exception:
                    pass
            _st["done"] = "WDONE"
    except Exception as exc:
        try:
            with open(f"{OUT}/err3.log", "a") as f:
                f.write("watch:" + repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
