"""cap34b(诊断+广谱补丁·承 cap34 零命中复盘):同四断点,三处强化——
①每命中必留 hits.log(带 bp_rva+时间,解决 cap34 无命中计数的盲区);
②needle 门扩谱:x0-x28 全寄存器 + SP..SP+0x600 栈窗(UTF-8/UTF-16 双形);
③门过→16 帧栈留档+同长 forge 原位改写(cap34 同款零越界写)。
判读:hits.log 有 0x434a2ac 命中但无 needle→本实例正文流换了路径;
全无命中→worker 路径整体未走;门过且 localdb 出 forge=配方候选。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r34b"
OFFS = (0x434A2AC, 0x83C750, 0x865484, 0x866D60)
NP_TXT = "嘻嘻~c35z"
NEEDLE_TXT = NP_TXT + "Z" * 32
FP_TXT = "直发c35z赢"
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
MAX_PATCH = 40
MAX_HITLOG = 500
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


def _try_patch_at(proc, addr, found_in):
    """在 addr 处核验 needle 并同长改写。返回 patch 记录 dict 或 None。"""
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
        return {
            "addr": addr, "form": label, "span": len(forge_w),
            "wrote": err.Success(), "verified": ok, "where": found_in,
        }
    return None


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
            bp.SetScriptCallbackFunction("cap34b.on_hit")
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
        if _st["logged"] < MAX_HITLOG:
            _st["logged"] += 1
            _log("n=%d t=%.1f bp=%#x\n" % (_st["n"], time.time(), frame.GetPC() - slide))
        hit = None
        # ① 全寄存器扫
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
                    hit = _try_patch_at(proc, v + idx, "reg:%s" % reg)
                    break
            if hit:
                break
        # ② 栈窗扫(SP..SP+0x600)
        if hit is None:
            sp = frame.FindRegister("sp")
            spv = sp.GetValueAsUnsigned() if sp and sp.IsValid() else 0
            if spv:
                blob = _read(proc, spv, 0x600)
                if blob is not None:
                    for pfx in (N8P, N16P):
                        idx = blob.find(pfx)
                        if idx >= 0:
                            hit = _try_patch_at(proc, spv + idx, "stack")
                            break
        if hit is not None:
            _st["patches"] += 1
            thread = frame.GetThread()
            lines = [
                "p=%d n=%d t=%.1f bp=%#x %s addr=%#x form=%s span=%d wrote=%s verified=%s"
                % (_st["patches"], _st["n"], time.time(), frame.GetPC() - slide,
                   hit["where"], hit["addr"], hit["form"], hit["span"],
                   hit["wrote"], hit["verified"])
            ]
            for i in range(min(16, thread.GetNumFrames())):
                f2 = thread.GetFrameAtIndex(i)
                pc2 = f2.GetPC()
                rva2 = pc2 - slide if slide <= pc2 < slide + 0x10000000 else 0
                lines.append("  #%d pc=%#x rva=%#x fn=%s" % (i, pc2, rva2, f2.GetFunctionName()))
            with open(f"{OUT}/patch%d.txt" % _st["patches"], "w") as f:
                f.write("\n".join(lines) + "\n")
            _log("PATCH p=%d %s %s addr=%#x form=%s verified=%s\n"
                 % (_st["patches"], hit["where"], hit["form"], hit["addr"], hit["verified"]))
            if _st["patches"] >= MAX_PATCH:
                for b in _st["bps"]:
                    b.SetEnabled(False)
                _st["done"] = True
                with open(f"{OUT}/DONE_MANY", "w") as f:
                    f.write("patches=%d n=%d\n" % (_st["patches"], _st["n"]))
        # STOP 哨兵(驱动收尾协作)
        if os.path.exists(f"{OUT}/STOP") and not _st["done"]:
            for b in _st["bps"]:
                b.SetEnabled(False)
            _st["done"] = True
            with open(f"{OUT}/CALLBACK_SHUTDOWN", "w") as f:
                f.write("n=%d patches=%d\n" % (_st["n"], _st["patches"]))
    except Exception as exc:
        _log("hit_err:" + repr(exc) + "\n")
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
