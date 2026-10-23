"""truepath 第二窗:桥 0x5daad24(命题)+ 阳性对照 0x5980a6c(黄金已证发送必中)
+ blr 位点 0x5980c44/0x5980ca4(json blrX8;命中时 x8=序列化虚调用目标)。
桥命中:全量 vtable dump(同 capwf);对照命中:x0/x1 对象图两层 needle 扫描;
blr 命中:dump x8 目标 rva+x0 对象与 vtable。纯读零写,自动续走。
needle 扫描用前缀「嘻嘻~wf」匹配并报出完整字面(wf101=第一窗残流/wf102=本窗新鲜)。"""
import lldb
import os
import time

OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
NEEDLE = "嘻嘻~wf".encode("utf-8")  # 前缀:e5 98 bb e5 98 bb 7e 77 66
OFFS = ((0x5DAAD24, "bridge"), (0x5980A6C, "req2buf_enter"), (0x5980C44, "blrA"), (0x5980CA4, "blrB"))
MAX_HITS = 96
MAX_SECONDS = 150.0

_st = {"bps": [], "slide": 0, "t0": time.time(), "n": 0, "done": "", "per": {}, "needle_hits": []}


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


def _find(raw):
    """返回 '字面@+偏移' 或 None(前缀命中,字面含尾缀区分 wf101/wf102)。"""
    if not raw:
        return None
    i = raw.find(NEEDLE)
    if i < 0:
        return None
    lit = raw[i:i + 16].split(b"\x00")[0].decode("utf-8", "replace")
    return "%s@+%#x" % (lit, i)


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
        bp.SetScriptCallbackFunction("capwf2.on_hit")
        _st["bps"].append(bp)
        _st["per"][tag] = 0
        b = _read(target.GetProcess(), slide + rva, 16)
        info.append("%s rva=%#x locs=%d bytes=%s" % (tag, rva, bp.GetNumLocations(), b.hex() if b else "ERR"))
    with open(f"{OUT}/ARMED2", "w") as f:
        f.write("slide=%#x %s loaded=%s\n" % (slide, " | ".join(info), time.strftime("%H:%M:%S")))


def disdump(debugger):
    """attach 后、续走前:四位点现场 dis 前几条,验证地址语义与 Ghidra hunt 一致。"""
    slide = _st["slide"]
    if not slide:
        return
    for rva, tag in OFFS:
        print("== dis %s rva=%#x addr=%#x ==" % (tag, rva, slide + rva))
        debugger.HandleCommand("dis -s %#x -c 3" % (slide + rva))


def _dump_vtable(proc, slide, lines, obj_ptr, label):
    """dump *obj_ptr 的 vtable 全 0x80 + 各槽 rva + +0x10/+0x30 目标字节。"""
    if not _ptr(obj_ptr):
        return None
    ob = _read(proc, obj_ptr, 0x40)
    if ob:
        lines.append("%s_obj@%#x=%s" % (label, obj_ptr, ob.hex()))
    vt = _u64(ob, 0) if ob else 0
    vt80 = _read(proc, vt, 0x80) if _ptr(vt) else None
    if not vt80:
        return None
    lines.append("%s_vtable=%#x vt80=%s" % (label, vt, vt80.hex()))
    slots = []
    for i in range(0, 0x80, 8):
        v = _u64(vt80, i)
        if slide <= v < slide + 0x20000000:
            slots.append("+%#x=rva%#x" % (i, v - slide))
    if slots:
        lines.append("%s_vt_slots_in_mod=" % label + " ".join(slots))
    for i in (0x10, 0x30):
        t = _u64(vt80, i)
        if _ptr(t):
            sig = _read(proc, t, 0x20)
            rva = t - slide if slide <= t < slide + 0x20000000 else 0
            lines.append("%s_vt+%#x_target=%#x rva=%#x bytes=%s" % (label, i, t, rva, sig.hex() if sig else ""))
    return vt80


def on_hit(frame, bp_loc, internal_dict):
    try:
        _st["n"] += 1
        n = _st["n"]
        elapsed = time.time() - _st["t0"]
        if n > MAX_HITS or elapsed > MAX_SECONDS:
            for b in _st["bps"]:
                b.SetEnabled(False)
            _st["done"] = "CAPPED"
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
        found = []

        if tag == "bridge":
            s16 = _read(proc, sp, 16)
            if s16:
                lines.append("stack_args=s0=%#x s1_u16=%#x raw=%s"
                             % (_u64(s16, 0), int.from_bytes(s16[8:10], "little"), s16.hex()))
            x0 = regs[0]
            o0 = _read(proc, x0, 0x40)
            if o0:
                lines.append("x0_obj@%#x=%s" % (x0, o0.hex()))
                hit = _find(o0)
                if hit:
                    found.append("x0obj:" + hit)
            dele = _u64(o0, 8) if o0 else 0
            od = _read(proc, dele, 0x40) if _ptr(dele) else None
            if od:
                lines.append("delegate=%#x obj=%s" % (dele, od.hex()))
                hit = _find(od)
                if hit:
                    found.append("delegobj:" + hit)
                _dump_vtable(proc, slide, lines, dele, "deleg")
            for i in range(1, 8):
                v = regs[i]
                if not _ptr(v):
                    continue
                raw = _read(proc, v, 0x80)
                if not raw:
                    continue
                hit = _find(raw)
                if hit:
                    found.append("x%d:%s" % (i, hit))
                nd = 0
                for off in range(0, 0x40, 8):
                    p = _u64(raw, off)
                    if _ptr(p):
                        d2 = _read(proc, p, 0x40)
                        hit = _find(d2)
                        if hit:
                            found.append("x%d->+%#x:%s" % (i, off, hit))
                        nd += 1
                        if nd >= 8:
                            break
                lines.append("x%d_obj@%#x=%s" % (i, v, raw.hex()))

        elif tag == "req2buf_enter":
            budget = [80]

            def scan(label, addr, size, level):
                if budget[0] <= 0:
                    return
                raw = _read(proc, addr, size)
                if not raw:
                    return
                budget[0] -= 1
                hit = _find(raw)
                if hit:
                    found.append("%s:%s" % (label, hit))
                    i = raw.find(NEEDLE)
                    lines.append("NEEDLE_CTX %s=%s" % (label, raw[max(0, i - 24):i + 48].hex()))
                if level <= 0:
                    return
                for off in range(0, min(len(raw), 0x80), 8):
                    if budget[0] <= 0:
                        return
                    p = _u64(raw, off)
                    if _ptr(p):
                        scan("%s->+%#x" % (label, off), p, 0x40, level - 1)

            _dump_vtable(proc, slide, lines, regs[0], "x0")
            scan("x0", regs[0], 0x80, 2)
            scan("x1", regs[1], 0x80, 2)
            scan("x3", regs[3], 0x40, 1)

        else:  # blrA / blrB:x8=虚调用目标
            x8 = regs[8]
            rva8 = x8 - slide if slide <= x8 < slide + 0x20000000 else 0
            lines.append("blr_target_x8=%#x rva=%#x" % (x8, rva8))
            sig = _read(proc, x8, 0x20) if _ptr(x8) else None
            if sig:
                lines.append("blr_target_bytes=%s" % sig.hex())
            _dump_vtable(proc, slide, lines, regs[0], "blr_x0obj")
            for ix in (0, 1):
                raw = _read(proc, regs[ix], 0x80) if _ptr(regs[ix]) else None
                if raw:
                    hit = _find(raw)
                    if hit:
                        found.append("blr_x%d:%s" % (ix, hit))

        lines.append("needle=" + ("FOUND " + ",".join(found) if found else "no"))
        with open(f"{OUT}/hit2_{tag}_{seq}.txt", "w") as f:
            f.write("\n".join(lines) + "\n")
        if found:
            _st["needle_hits"].append("%s#%d" % (tag, seq))
    except Exception as exc:
        try:
            with open(f"{OUT}/err2.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
