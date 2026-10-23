"""truepath 第四窗:调用链定案后的实弹。
0x5971c24(分发桥,this+0x18→0x5980a6c 主路;返回0→this+0x10→0x597d26c 兜底)。
窗口:bp 0x597d26c(兜底序列化,主路 null-getter 时必走)+ bp 0x5971c24(分发桥,
dump this/+0x10/+0x18/+0x20 实现对象与各自 vtable)。
兜底命中:深扫 x0 对象图找 needle(嘻嘻~wf*),找到即下硬件读观察点,
观察点命中 dump pc/rva/栈回溯=真·文本序列化现场。纯读零写,用后即禁。"""
import lldb
import os
import time

OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
NEEDLE = "嘻嘻~wf".encode("utf-8")
OFFS = ((0x597D26C, "fallback"), (0x5971C24, "dispatcher"))
MAX_HITS = 60
MAX_SECONDS = 150.0
MAX_W_HITS = 8

_st = {"bps": [], "slide": 0, "t0": time.time(), "n": 0, "per": {}, "w": [], "wn": 0,
       "done": "", "watch_addr": None}


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
        return None, -1
    i = raw.find(NEEDLE)
    if i < 0:
        return None, -1
    return raw[i:i + 16].split(b"\x00")[0].decode("utf-8", "replace"), i


def _vt_dump(proc, slide, lines, obj, label):
    if not _ptr(obj):
        return
    ob = _read(proc, obj, 0x40)
    if ob:
        lines.append("%s_obj@%#x=%s" % (label, obj, ob.hex()))
    vt = _u64(ob, 0) if ob else 0
    vt80 = _read(proc, vt, 0x80) if _ptr(vt) else None
    if not vt80:
        return
    slots = []
    for i in range(0, 0x80, 8):
        v = _u64(vt80, i)
        if slide <= v < slide + 0x20000000:
            slots.append("+%#x=rva%#x" % (i, v - slide))
    lines.append("%s_vtable=%#x %s" % (label, vt, " ".join(slots) if slots else vt80.hex()))


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
    info = []
    for rva, tag in OFFS:
        bp = target.BreakpointCreateByAddress(slide + rva)
        bp.SetScriptCallbackFunction("capwf4.on_hit")
        _st["bps"].append(bp)
        _st["per"][tag] = 0
        b = _read(target.GetProcess(), slide + rva, 16)
        info.append("%s rva=%#x locs=%d bytes=%s" % (tag, rva, bp.GetNumLocations(), b.hex() if b else "ERR"))
    with open(f"{OUT}/ARMED4", "w") as f:
        f.write("slide=%#x %s loaded=%s\n" % (slide, " | ".join(info), time.strftime("%H:%M:%S")))


def _deep_scan(proc, root, label, log):
    budget = [300]
    hits = []
    seen = set()

    def scan(path, addr, size, level):
        if budget[0] <= 0 or level < 0 or addr in seen or len(hits) >= 3:
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

    scan(label, root, 0x80, 4)
    return hits


def on_hit(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        n = _st["n"]
        if n > MAX_HITS or time.time() - _st["t0"] > MAX_SECONDS or _st["done"] == "WDONE":
            for b in _st["bps"]:
                b.SetEnabled(False)
            return False
        proc = frame.GetThread().GetProcess()
        slide = _st["slide"]
        pc_rva = frame.GetPC() - slide
        tag = next((t for r, t in OFFS if r == pc_rva), "?")
        _st["per"][tag] = _st["per"].get(tag, 0) + 1
        seq = _st["per"][tag]

        def reg(name):
            r = frame.FindRegister(name)
            try:
                return r.GetValueAsUnsigned() if r and r.IsValid() else 0
            except Exception:
                return 0

        regs = [reg("x%d" % i) for i in range(29)]
        fp, sp, lr = reg("x29"), reg("sp"), reg("x30")
        lines = ["hit=%d tag=%s#%d t=%.1f tid=%d pc_rva=%#x"
                 % (n, tag, seq, time.time() - _st["t0"], frame.GetThread().GetIndexID(), pc_rva)]
        lines.append("regs=" + " ".join("x%d=%#x" % (i, v) for i, v in enumerate(regs))
                     + " sp=%#x fp=%#x lr_rva=%#x" % (sp, fp, (lr - slide) if slide <= lr < slide + 0x20000000 else 0))

        if tag == "dispatcher":
            this = regs[0]
            ob = _read(proc, this, 0x40) if _ptr(this) else None
            if ob:
                lines.append("disp_obj@%#x=%s" % (this, ob.hex()))
            for off in (0x10, 0x18, 0x20):
                im = _u64(ob, off) if ob else 0
                if _ptr(im):
                    _vt_dump(proc, slide, lines, im, "impl+%#x" % off)
            _vt_dump(proc, slide, lines, this, "disp")
        else:  # fallback 0x597d26c
            _vt_dump(proc, slide, lines, regs[0], "fb_x0")
            log2 = []
            hits = []
            for ix in (0, 1, 3):
                if _ptr(regs[ix]):
                    hits = _deep_scan(proc, regs[ix], "x%d" % ix, log2)
                    if hits:
                        break
            lines.extend(log2)
            if hits:
                target = proc.GetTarget()
                path, addr, lit = hits[0]
                w = target.WatchpointCreateByAddress(addr, 8, True, False)
                if not (w and w.IsValid()):
                    w = target.WatchpointCreateByAddress(addr, 8, True, True)
                if w and w.IsValid():
                    w.SetScriptCallbackFunction("capwf4.on_watch")
                    _st["w"].append(w)
                    _st["watch_addr"] = addr
                    with open(f"{OUT}/watch4_set.txt", "a") as f:
                        f.write("fb#%d %s %s addr=%#x id=%d\n" % (seq, path, lit, addr, w.GetID()))
                    for b in _st["bps"]:
                        b.SetEnabled(False)
                    _st["done"] = "WATCHING"
                lines.append("watchpoint_created=%s" % (w and w.IsValid()))

        lines.append("needle=" + ("SEE hitfile" if tag == "fallback" else "n/a"))
        with open(f"{OUT}/hit4_{tag}_{seq}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as exc:
        try:
            with open(f"{OUT}/err4.log", "a") as f:
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
        for ix in (0, 1):
            if _ptr(regs[ix]):
                _vt_dump(proc, slide, lines, regs[ix], "w_x%d" % ix)
        with open(f"{OUT}/watch4_%d.txt" % wn, "w") as f:
            f.write("\n".join(lines) + "\n")
        if wn >= MAX_W_HITS:
            for w in _st["w"]:
                try:
                    proc.GetTarget().DeleteWatchpoint(w.GetID())
                except Exception:
                    pass
            _st["done"] = "WDONE"
    except Exception as exc:
        try:
            with open(f"{OUT}/err4.log", "a") as f:
                f.write("watch:" + repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
