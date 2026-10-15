"""cap36(正本全程读者链·prd Step2 观测):断粘贴转换返回 0x70AC5F4
(x19=输出槽→WeChat 串 S→deep 找 needle 得正本 Q)。命中→留档 S/Q→
写 WATCH_PENDING。驱动在 +2.5s(粘贴落定/回读前)Stop→扫 Q±32MB 堆窗
找全部 needle 副本→前 3 个挂 read watch→Continue→轮询采栈 45s。
读者栈时间轴=正本消费链:插入复制/回读复制/聚焦哨兵复制/
Return 构造取用(=构造点)/回显。纯观测不补丁。"""
import lldb
import os
import time

OUT = "/tmp/wxsend3/r36"
CONV_RET_RVA = 0x70AC5F4
NP_TXT = "嘻嘻~c38z"
N8P = NP_TXT.encode("utf-8")
N16P = NP_TXT.encode("utf-16-le")

L3_RVA = 0x433C5F0
BL_RVA = 0x435E070
L3_EXPECT = "fc6fbca9f65701a9"
BL_EXPECT = "6079ff97"

_st = {"bp": None, "slide": 0, "n": 0, "done": False, "Q": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def _log(line):
    try:
        with open(f"{OUT}/hits.log", "a") as f:
            f.write(line)
    except OSError:
        pass


def _find_needle_deep(proc, root, seen=None):
    seen = seen if seen is not None else set()

    def scan(addr, depth):
        if depth > 2 or addr in seen or not (0x100000000 < addr < 0x800000000000):
            return None
        seen.add(addr)
        blob = _read(proc, addr, 0x80)
        if blob is None:
            return None
        for pat, label in ((N16P, "u16"), (N8P, "u8")):
            i = blob.find(pat)
            if i >= 0:
                return addr + i, label
        for off in range(0, len(blob) - 7, 8):
            p = int.from_bytes(blob[off:off + 8], "little")
            if 0x100000000 < p < 0x800000000000:
                r = scan(p, depth + 1)
                if r:
                    return r
        return None

    return scan(root, 0)


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
        bp = target.BreakpointCreateByAddress(slide + CONV_RET_RVA)
        bp.SetScriptCallbackFunction("cap36.on_hit")
        _st["bp"] = bp
        with open(f"{OUT}/ARMED", "w") as f:
            f.write("slide=%#x locs=%d\n" % (slide, bp.GetNumLocations()))
    except Exception as exc:
        _log("install_err:" + repr(exc) + "\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        _st["n"] += 1
        proc = frame.GetThread().GetProcess()
        x19 = frame.FindRegister("x19")
        v = x19.GetValueAsUnsigned() if x19 and x19.IsValid() else 0
        if not v:
            return False
        slot = _read(proc, v, 8)
        s = int.from_bytes(slot, "little") if slot else 0
        found = None
        for cand in (s, v):
            if 0x100000000 < cand < 0x800000000000:
                found = _find_needle_deep(proc, cand)
                if found:
                    break
        if found is None:
            if os.path.exists(f"{OUT}/STOP") and not _st["done"]:
                if _st["bp"] is not None:
                    _st["bp"].SetEnabled(False)
                _st["done"] = True
                with open(f"{OUT}/CALLBACK_SHUTDOWN", "w") as f:
                    f.write("n=%d\n" % _st["n"])
            return False
        q, form = found
        _st["Q"] = q
        shead = _read(proc, s, 0x40)
        with open(f"{OUT}/paste_hit.txt", "w") as f:
            f.write(
                "t=%.1f x19_slot=%#x S=%#x S_head=%s Q=%#x form=%s\n"
                % (time.time(), v, s, shead.hex() if shead else "ERR", q, form)
            )
        with open(f"{OUT}/WATCH_PENDING", "w") as f:
            f.write("Q=%#x form=%s\n" % (q, form))
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        _st["done"] = True
    except Exception as exc:
        _log("hit_err:" + repr(exc) + "\n")
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
