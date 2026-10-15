"""cap26(正本猎杀终验):三断点(L4 bl@0x435E070/兄弟A bl@0x4352830/兄弟B b@0x435ee8c)
+干净 peer 门。A(43B)首命中(spawn 时刻)→读 mc 拿 needle 特征→扫 P±32MB 堆窗
找全部 needle 出现→逐处原位改写同长 forge(排除 mc 槽与 P 副本自身照改不误:
副本改了无妨,正本改了=传导)→放行→localdb 判据。"""
import lldb
import os

OUT = "/tmp/wxsend3/r26"
OFFS = (0x435E070, 0x4352830, 0x435EE8C)
PEER = b"filehelper"
PREFIX = "嘻嘻~c31w".encode("utf-8")      # A 文本前缀(11B)
SUFFIX_MARK = b"W" * 32                    # A 文本 32 个 W(与 forge 的 V 区分)
NEEDLE_FULL = PREFIX + SUFFIX_MARK         # 43B 完整特征
FORGE = "嘻嘻~直发c31w".encode("utf-8") + b"V" * 26  # 43B 同长

_st = {"bps": [], "slide": 0, "P": 0, "done": False}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


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
    for off in OFFS:
        bp = target.BreakpointCreateByAddress(slide + off)
        bp.SetScriptCallbackFunction("cap26.on_bp")
        _st["bps"].append(bp)
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x}\n")


def on_bp(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        mc = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        head = _read(proc, mc, 0x58) or b""
        if head[0:16] != PEER + b"\x00" * (16 - len(PEER)):
            return False
        blob = _read(proc, mc, 0x270) or b""
        slot = blob[0x40:0x58]
        p64 = int.from_bytes(slot[0:8], "little")
        ln = int.from_bytes(slot[8:16], "little")
        true = _read(proc, p64, ln) if 0x100000000 < p64 < 0x800000000000 and 0 < ln <= 4096 else None
        if not true or true[0:len(PREFIX)] != PREFIX:
            return False  # 等 A 的发送跳(长形态+前缀吻合)
        _st["done"] = True
        for b in _st["bps"]:
            b.SetEnabled(False)
        _st["P"] = p64
        # —— 正本猎杀:扫 P±32MB(4MB 步进,含跨块) ——
        found = []
        base = p64 - 0x2000000
        total = 0x4000000
        step = 0x400000
        overlap = len(NEEDLE_FULL) - 1
        prev_tail = b""
        for off in range(0, total, step):
            chunk = _read(proc, base + off, step) 
            if chunk is None:
                # 逐 64KB 兜底读(跳过不可读洞)
                for sub in range(0, step, 0x10000):
                    c2 = _read(proc, base + off + sub, 0x10000)
                    if c2 is None:
                        prev_tail = b""
                        continue
                    hay = prev_tail + c2
                    idx = hay.find(NEEDLE_FULL)
                    while idx >= 0:
                        addr = base + off + sub - len(prev_tail) + idx
                        if addr >= 0:
                            found.append(addr)
                        idx = hay.find(NEEDLE_FULL, idx + 1)
                    prev_tail = c2[-overlap:]
                continue
            hay = prev_tail + chunk
            idx = hay.find(NEEDLE_FULL)
            while idx >= 0:
                addr = base + off - len(prev_tail) + idx
                found.append(addr)
                idx = hay.find(NEEDLE_FULL, idx + 1)
            prev_tail = chunk[-overlap:]
        # 去重排序
        found = sorted(set(a for a in found if a > 0))
        patched = []
        err = lldb.SBError()
        for a in found:
            ok = proc.WriteMemory(a, FORGE, err)
            back = _read(proc, a, len(FORGE)) or b""
            patched.append((a, bool(ok), back[0:17] == FORGE[0:17]))
        with open(f"{OUT}/HUNT.txt", "w") as f:
            f.write(f"P={p64:#x} mc={mc:#x} found={len(found)}\n")
            for a, ok, ver in patched:
                f.write(f"addr={a:#x} wrote={ok} verified={ver}\n")
        with open(f"{OUT}/DONE", "w") as f:
            f.write(f"found={len(found)} patched={sum(1 for _, _, v in patched if v)}\n")
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
