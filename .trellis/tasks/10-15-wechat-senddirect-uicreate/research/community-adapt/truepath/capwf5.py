"""truepath 第五窗(终局手段):不再猜函数——堆内直搜 needle。
心跳 bp 0x597d26c(实测 ~0.5Hz 热点,自动续走)。两路扫描:
A) driver 线程在进程 RUNNING 态尝试活体扫描(失败无害);
B) 心跳命中(停机态)时按需补扫一次(t≥6s,timebox 25s)。
找到 needle → 立即下硬件读观察点(≤3 个,停机态)→ 观察点命中
dump pc/rva/栈回溯 = 真·文本序列化现场。纯读零写,用后即禁。"""
import lldb
import os
import time

OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
NEEDLE = "嘻嘻~wf".encode("utf-8")
HB_RVA = 0x597D26C
MAX_W_HITS = 10
MAX_SECONDS = 150.0

_st = {"bp": None, "slide": 0, "t0": time.time(), "n": 0, "wn": 0, "done": "",
       "scan_hits": [], "scans": 0, "watched": False, "w": []}


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
    bp = target.BreakpointCreateByAddress(slide + HB_RVA)
    bp.SetScriptCallbackFunction("capwf5.on_hb")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED5", "w") as f:
        f.write("slide=%#x hb_rva=%#x locs=%d loaded=%s\n"
                % (slide, HB_RVA, bp.GetNumLocations(), time.strftime("%H:%M:%S")))


def _iter_regions(proc):
    """自适应枚举内存区(lldb 版本 API 差异:GetMemoryRegionAtIndex 出参式 vs GetRegionAtIndex)。"""
    rl = proc.GetMemoryRegions()
    out = []
    n = rl.GetSize() if hasattr(rl, "GetSize") else 0
    for i in range(n):
        got = None
        try:
            r = lldb.SBMemoryRegionInfo()
            if rl.GetMemoryRegionAtIndex(i, r):
                got = r
        except Exception:
            got = None
        if got is None:
            try:
                got = rl.GetRegionAtIndex(i)
            except Exception:
                got = None
        if got is not None:
            out.append(got)
    return out, n


def heap_scan(proc, tag, byte_budget=1200 * 1024 * 1024, max_seconds=12.0, max_hits=24):
    """枚举可写内存区,分块(8MB)搜 needle 前缀。返回命中列表 [(addr, ctx48)]。"""
    t0 = time.time()
    hits = []
    covered = 0
    regions, n_reg = _iter_regions(proc)
    for i in range(n_reg):
        r = regions.GetRegionAtIndex(i)
        try:
            if not r.IsWritable():
                continue
            sa = r.GetBaseAddress()
            if not sa.IsValid():
                continue
            base = sa.GetLoadAddress(proc.GetTarget())
            if base <= 0 or base > 0x7FFFFFFFFFFF:
                continue
            size = r.GetByteSize()
        except Exception:
            continue
        if not base or size <= 0 or size > 64 * 1024 * 1024:
            continue
        off = 0
        while off < size:
            if time.time() - t0 > max_seconds or covered > byte_budget or len(hits) >= max_hits:
                break
            chunk = _read(proc, base + off, min(8 * 1024 * 1024, size - off))
            if chunk:
                covered += len(chunk)
                pos = chunk.find(NEEDLE)
                while pos >= 0 and len(hits) < max_hits:
                    a = base + off + pos
                    ctx = chunk[max(0, pos - 16):pos + 48]
                    hits.append((a, ctx))
                    pos = chunk.find(NEEDLE, pos + 8)
            off += 8 * 1024 * 1024
        if time.time() - t0 > max_seconds or covered > byte_budget or len(hits) >= max_hits:
            break
    lines = ["scan=%s tag=%s elapsed=%.1fs regions=%d covered=%dMB hits=%d"
             % (_st["scans"], tag, time.time() - t0, n_reg, covered // (1024 * 1024), len(hits))]
    for a, ctx in hits:
        lines.append("  addr=%#x ctx=%s" % (a, ctx.hex()))
    with open(f"{OUT}/scan5_{tag}.txt", "w") as f:
        f.write("\n".join(lines) + "\n")
    return hits


def set_watch(target, addrs):
    made = []
    for a in addrs[:3]:
        w = target.WatchpointCreateByAddress(a, 8, True, False)
        if not (w and w.IsValid()):
            w = target.WatchpointCreateByAddress(a, 8, True, True)
        if w and w.IsValid():
            w.SetScriptCallbackFunction("capwf5.on_watch")
            _st["w"].append(w)
            made.append(a)
    _st["watched"] = bool(made)
    with open(f"{OUT}/watch5_set.txt", "w") as f:
        f.write(" ".join("%#x" % a for a in made) + "\n")
    return made


def on_hb(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        if _st["watched"] or _st["done"] or time.time() - _st["t0"] > MAX_SECONDS:
            if _st["bp"]:
                _st["bp"].SetEnabled(False)
            return False
        t = time.time() - _st["t0"]
        proc = frame.GetThread().GetProcess()
        if _st["scan_hits"]:
            set_watch(proc.GetTarget(), [a for a, _ in _st["scan_hits"]])
            if _st["bp"]:
                _st["bp"].SetEnabled(False)
            _st["done"] = "WATCHING"
            return False
        if t >= 8.0 and _st["scans"] < 2:
            _st["scans"] += 1
            hits = heap_scan(proc, "stop%d" % _st["scans"])
            if hits:
                _st["scan_hits"] = hits
                set_watch(proc.GetTarget(), [a for a, _ in hits])
                if _st["bp"]:
                    _st["bp"].SetEnabled(False)
                _st["done"] = "WATCHING"
    except Exception as exc:
        try:
            with open(f"{OUT}/err5.log", "a") as f:
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
        for i in range(min(20, th.GetNumFrames())):
            f = th.GetFrameAtIndex(i)
            fpc = f.GetPC()
            frva = fpc - slide if slide <= fpc < slide + 0x20000000 else 0
            lines.append("  #%d pc=%#x rva=%#x fn=%s" % (i, fpc, frva, f.GetFunctionName()))
        for ix in (0, 1):
            v = regs[ix]
            if _ptr(v):
                ob = _read(proc, v, 0x20)
                if ob:
                    vt = _u64(ob, 0)
                    vt80 = _read(proc, vt, 0x80) if _ptr(vt) else None
                    slots = []
                    if vt80:
                        for i in range(0, 0x80, 8):
                            sv = _u64(vt80, i)
                            if slide <= sv < slide + 0x20000000:
                                slots.append("+%#x=rva%#x" % (i, sv - slide))
                    lines.append("w_x%d_obj@%#x=%s vt=%s" % (ix, v, ob.hex(), " ".join(slots) if slots else ""))
        with open(f"{OUT}/watch5_%d.txt" % wn, "w") as f:
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
            with open(f"{OUT}/err5.log", "a") as f:
                f.write("watch:" + repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
