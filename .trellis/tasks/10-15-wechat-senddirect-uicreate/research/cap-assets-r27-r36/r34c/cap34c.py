"""cap34c(出站链定向补丁·承 34b 零命中复盘):同四断点。三处强化——
①栈窗 0x4000(34b 的 0x600 不及 cap32 GOLD 的 needle 结构体距 SP ~0x1260);
②回溯签名门:仅当 16 帧栈含出站链签名(0x435e074 L4/0x433c6f0 协程入口)
  才允许补丁——0x434a2ac 同时服务回显二遍(spawner cap14),盲补回显侧
  会在 localdb 假阳性(线正库假);回显形命中只留档(ECHO_SKIP);
③门过→窗内全部 needle 出现处同长 forge 改写(一次命中清全部副本)。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r34c"
OFFS = (0x434A2AC, 0x83C750, 0x865484, 0x866D60)
NP_TXT = "嘻嘻~c36z"
NEEDLE_TXT = NP_TXT + "Z" * 32
FP_TXT = "直发c36z赢"
FORGE_TXT = FP_TXT + "F" * 32

N8P = NP_TXT.encode("utf-8")
N8 = NEEDLE_TXT.encode("utf-8")
F8 = FORGE_TXT.encode("utf-8")
N16P = NP_TXT.encode("utf-16-le")
N16 = NEEDLE_TXT.encode("utf-16-le")
F16 = FORGE_TXT.encode("utf-16-le")

L3_RVA = 0x433C5F0
BL_RVA = 0x435E070
L3_EXPECT = "fc6fbca9f65701a9"
BL_EXPECT = "6079ff97"
OUT_SIG = (0x435E074, 0x433C6F0)          # 出站链签名帧(L4 返回址/协程入口)
STACK_WIN = 0x4000
MAX_PATCH = 40
MAX_HITLOG = 600
REGS = tuple("x%d" % i for i in range(0, 29))

_st = {"bps": [], "slide": 0, "n": 0, "patches": 0, "done": False, "logged": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def _log(line):
    try:
        with open(f"{OUT}/hits.log", "a") as f:
            f.write(line)
    except OSError:
        pass


def _frames_rva(thread, slide, n=16):
    out = []
    for i in range(min(n, thread.GetNumFrames())):
        f2 = thread.GetFrameAtIndex(i)
        pc = f2.GetPC()
        rva = pc - slide if slide <= pc < slide + 0x10000000 else 0
        out.append((pc, rva, f2.GetFunctionName()))
    return out


def install(debugger):
    try:
        target = debugger.GetSelectedTarget()
        slide = None
        for m in target.module_iter():
            if m.file.basename == "wechat.dylib":
                slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
                break
        if slide is None:
            with open(f"{OUT}/ARMED", "w") as f:
                f.write("FAIL no wechat.dylib\n")
            return
        _st["slide"] = slide
        d8 = _read(target.GetProcess(), slide + L3_RVA, 8)
        d4 = _read(target.GetProcess(), slide + BL_RVA, 4)
        a8 = d8.hex() if d8 else "READ_ERR"
        a4 = d4.hex() if d4 else "READ_ERR"
        with open(f"{OUT}/anchor_pre.txt", "w") as f:
            f.write(f"l3={a8} bl={a4}\n")
        if a8 != L3_EXPECT or a4 != BL_EXPECT:
            with open(f"{OUT}/ANCHOR_MISMATCH", "w") as f:
                f.write(f"l3={a8} bl={a4}\n")
            return
        for off in OFFS:
            bp = target.BreakpointCreateByAddress(slide + off)
            bp.SetScriptCallbackFunction("cap34c.on_hit")
            _st["bps"].append(bp)
        with open(f"{OUT}/ARMED", "w") as f:
            f.write(f"slide={slide:#x} locs={[b.GetNumLocations() for b in _st['bps']]}\n")
    except Exception as exc:
        _log("install_err:" + repr(exc) + "\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        _st["n"] += 1
        proc = frame.GetThread().GetProcess()
        slide = _st["slide"]
        thread = frame.GetThread()
        frs = _frames_rva(thread, slide)
        if _st["logged"] < MAX_HITLOG:
            _st["logged"] += 1
            _log("n=%d t=%.1f bp=%#x fr6=%s\n"
                 % (_st["n"], time.time(), frame.GetPC() - slide,
                    ",".join("%#x" % r for _, r, _ in frs[:6])))
        # 找 needle:寄存器邻域 + 宽栈窗
        spots = []
        for reg in REGS:
            r = frame.FindRegister(reg)
            v = r.GetValueAsUnsigned() if r and r.IsValid() else 0
            if not (0x100000000 < v < 0x800000000000):
                continue
            blob = _read(proc, v, 0x140)
            if blob is None:
                continue
            for pfx in (N8P, N16P):
                idx = blob.find(pfx)
                if idx >= 0:
                    spots.append((v + idx, "reg:%s" % reg))
        sp = frame.FindRegister("sp")
        spv = sp.GetValueAsUnsigned() if sp and sp.IsValid() else 0
        stack_blob = _read(proc, spv, STACK_WIN) if spv else None
        if stack_blob is not None:
            for pfx, tag in ((N8P, "stack8"), (N16P, "stack16")):
                start = 0
                while True:
                    idx = stack_blob.find(pfx, start)
                    if idx < 0:
                        break
                    spots.append((spv + idx, tag))
                    start = idx + 1
        if not spots:
            # STOP 哨兵(驱动收尾协作)
            if os.path.exists(f"{OUT}/STOP") and not _st["done"]:
                for b in _st["bps"]:
                    b.SetEnabled(False)
                _st["done"] = True
                with open(f"{OUT}/CALLBACK_SHUTDOWN", "w") as f:
                    f.write("n=%d patches=%d\n" % (_st["n"], _st["patches"]))
            return False
        # 有 needle:判出站/回显
        outbound = any(r in OUT_SIG for _, r, _ in frs)
        lines = ["n=%d t=%.1f bp=%#x outbound=%s spots=%d sp=%#x"
                 % (_st["n"], time.time(), frame.GetPC() - slide, outbound, len(spots), spv)]
        for pc, rva, fn in frs:
            lines.append("  #pc=%#x rva=%#x fn=%s" % (pc, rva, fn))
        if not outbound:
            lines.append("  ECHO_SKIP(非出站签名,只留档不补丁)")
            with open(f"{OUT}/echo%d.txt" % _st["n"], "w") as f:
                f.write("\n".join(lines) + "\n")
            _log("ECHO_SKIP n=%d spots=%d\n" % (_st["n"], len(spots)))
            return False
        # 出站:窗内全部出现处逐个核验+同长改写
        plog = []
        for addr, where in spots:
            for pfx, full, forge, label in ((N8P, N8, F8, "u8"), (N16P, N16, F16, "u16")):
                exact = _read(proc, addr, len(full))
                if exact is None or exact[: len(pfx)] != pfx:
                    continue
                span = full if exact == full else pfx
                forge_w = forge[: len(span)]
                err = lldb.SBError()
                proc.WriteMemory(addr, forge_w, err)
                back = _read(proc, addr, len(forge_w))
                ok = err.Success() and back == forge_w
                plog.append("addr=%#x where=%s form=%s span=%d wrote=%s verified=%s"
                            % (addr, where, label, len(forge_w), err.Success(), ok))
                break
        _st["patches"] += 1
        with open(f"{OUT}/patch%d.txt" % _st["patches"], "w") as f:
            f.write("\n".join(lines + ["  " + p for p in plog]) + "\n")
        _log("PATCH p=%d spots=%d %s\n" % (_st["patches"], len(spots), ";".join(plog)))
        if _st["patches"] >= MAX_PATCH:
            for b in _st["bps"]:
                b.SetEnabled(False)
            _st["done"] = True
            with open(f"{OUT}/DONE_MANY", "w") as f:
                f.write("patches=%d n=%d\n" % (_st["patches"], _st["n"]))
    except Exception as exc:
        _log("hit_err:" + repr(exc) + "\n")
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
