"""cap22(真体改写终验):断 L4 内 bl L3(0x435E070),门=peer 槽=='filehelper'。
发送 43B 长文本 → body 槽=SSO 长形态{ptr,len,cap};命中时刻当场 deref ptr,
验证真体以 needle 前缀开头后原位改写为同长 forge(不动 ptr/len/cap 结构)→放行。
localdb 出现 forge=阳性=配方成;兼容短形态(补槽)。零代码字节写,纯数据区。"""
import lldb
import os

OUT = "/tmp/wxsend3/r22"
OFF_BP = 0x435E070
PEER = b"filehelper"
PREFIX = "嘻嘻~c22y".encode("utf-8")          # 11B 短前缀(门内再验)
LONG_TEXT = PREFIX + b"X" * 32                  # 43B 发送文本
FORGE = "嘻嘻~直发c22y".encode("utf-8") + b"Y" * 26  # 43B 同长替换

_st = {"bp": None, "slide": 0, "done": False, "n": 0, "form": {"short": 0, "long": 0}}


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
    bp = target.BreakpointCreateByAddress(slide + OFF_BP)
    bp.SetScriptCallbackFunction("cap22.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} bp={slide + OFF_BP:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        x1 = frame.FindRegister("x1")
        mc = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        head = _read(proc, mc, 0x58) or b""
        if head[0:16] != PEER + b"\x00" * (16 - len(PEER)):
            return False
        _st["n"] += 1
        blob = _read(proc, mc, 0x270) or b""
        slot = blob[0x40:0x58]
        log = [f"n={_st['n']} mc={mc:#x} slot={slot.hex()}"]
        if slot[0:len(PREFIX)] == PREFIX:
            # 短形态:补槽(cap20 方式)
            _st["form"]["short"] += 1
            s2 = bytearray(24)
            f2 = FORGE[:23]
            s2[0:len(f2)] = f2
            s2[23] = len(f2)
            err = lldb.SBError()
            ok = proc.WriteMemory(mc + 0x40, bytes(s2), err)
            log.append(f"SHORT_PATCHED wrote={ok}")
        else:
            # 长形态:{ptr,len,cap}
            p64 = int.from_bytes(slot[0:8], "little")
            ln = int.from_bytes(slot[8:16], "little")
            if not (0x100000000 < p64 < 0x800000000000) or ln < 32 or ln > 4096:
                log.append(f"LONG_SKIP p={p64:#x} len={ln}")
            else:
                true = _read(proc, p64, ln) or b""
                log.append(f"TRUE_{ln}B={true[:64].hex()}")
                if true[0:len(PREFIX)] == PREFIX and len(true) >= len(FORGE):
                    err = lldb.SBError()
                    ok = proc.WriteMemory(p64, FORGE, err)
                    back = _read(proc, p64, len(FORGE)) or b""
                    log.append(f"LONG_PATCHED wrote={ok} back={back.hex()}")
                    _st["form"]["long"] += 1
                else:
                    log.append("TRUE_PREFIX_MISS")
        with open(f"{OUT}/hit{_st['n']}.txt", "w") as f:
            f.write("\n".join(log) + "\nmsgctx270=" + blob.hex() + "\n")
        if _st["n"] >= 3:
            _st["done"] = True
            if _st["bp"] is not None:
                _st["bp"].SetEnabled(False)
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
