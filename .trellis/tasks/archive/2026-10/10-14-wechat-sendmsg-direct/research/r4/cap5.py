"""cap5(r4 终捕):断 FUN_0083e394(协程体/RPC 执行体)入口,抓 param_1/param_2 真身。

目的:直调配方的活对象模板——param_2(任务结构,串源=+8)与 param_1(ctx,
含 +8→+0x198 vtable 链)。命中门:param_2 可达 needle(嘻嘻)。
落盘:x0/x1 对象各 0x600、回溯、寄存器、chase 日志。
纪律:只读;命中禁全部断点写 DONE;异常吞;自动继续。
"""
import lldb
import os

ROOT = "/tmp/wxsend3"
OUT = f"{ROOT}/r5"
OFF_BODY = 0x83E394
NEEDLE = b"\xe5\x98\xbb"
CHUNK = 512
MAX_CHASE = 80

os.makedirs(OUT, exist_ok=True)
_st = {"bp": None, "slide": 0, "done": False, "n": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    d = proc.ReadMemory(addr, size, err)
    return d if err.Success() else None


def _hexdump(data, base):
    out = []
    for i in range(0, len(data), 16):
        c = data[i:i + 16]
        out.append(f"{base+i:#x}  {' '.join(f'{b:02x}' for b in c):<48} {''.join(chr(b) if 32<=b<127 else '.' for b in c)}")
    return "\n".join(out)


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
    bp = target.BreakpointCreateByAddress(slide + OFF_BODY)
    bp.SetScriptCallbackFunction("cap5.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} body_bp@{slide+OFF_BODY:#x}\n")


def _chase(proc, seeds):
    seen = set()
    q = list(seeds)
    while q and len(seen) < MAX_CHASE:
        p = q.pop(0)
        if not isinstance(p, int) or p < 0x1000 or p in seen:
            continue
        seen.add(p)
        d = _read(proc, p, CHUNK)
        if d is None:
            continue
        if NEEDLE in d and b"filehelper" in d:
            return p, d
        for i in range(0, len(d) - 7, 8):
            v = int.from_bytes(d[i:i + 8], "little")
            if 0x100000000 < v < 0x800000000000:
                q.append(v)
    return None, None


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        target = proc.GetTarget()
        slide = _st["slide"]

        def reg(n):
            v = frame.FindRegister(n)
            return v.GetValueAsUnsigned() if v and v.IsValid() else 0

        x0, x1 = reg("x0"), reg("x1")
        _st["n"] += 1
        hit_ptr, _ = _chase(proc, [x1, x0])
        if hit_ptr is None:
            if _st["n"] % 20 == 1:
                with open(f"{OUT}/stray.log", "a") as f:
                    f.write(f"#{_st['n']} x0={x0:#x} x1={x1:#x}\n")
            return False

        with open(f"{OUT}/hit1.txt", "w") as f:
            f.write(f"slide={slide:#x}\nx0(param_1)={x0:#x} x1(param_2)={x1:#x} lr={reg('lr'):#x}\n")
            f.write(f"needle 载体:{hit_ptr:#x}\n\n")
            f.write("== param_1 对象 0x600 ==\n" + _hexdump(_read(proc, x0, 0x600) or b"", x0) + "\n")
            f.write("== param_2 对象 0x600(串源 +8) ==\n" + _hexdump(_read(proc, x1, 0x600) or b"", x1) + "\n")
            f.write("\nBT:\n")
            for fr in frame.GetThread():
                pc = fr.GetPCAddress().GetLoadAddress(target)
                mod = fr.GetModule().GetFileSpec().GetFilename() if fr.GetModule() else "?"
                off = pc - slide if mod == "wechat.dylib" else -1
                f.write(f"  #{fr.GetFrameID()}: {pc:#x} [{mod}] +{off:#x}\n")
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        _st["done"] = True
        with open(f"{OUT}/DONE", "w") as f:
            f.write("hit1\n")
    except Exception as exc:  # noqa: BLE001
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
