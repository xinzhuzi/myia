"""cap7(选项 a):断 spawner FUN_06fda37c 入口抓实参。

假设:F_exec 需协程栈(同步直调抛异常实证);spawner 跑在业务链普通栈
(cap5 BT 帧 #6=0x6fda778 由主线程调用链到达)→ 可 expr 直调的安全层。
目标:确定 (x0, x1, x2) 哪个=可伪造 msgctx、哪个=ctx 包装;x2 是否简单值。
命中门:x0/x1/x2 指针追 needle(嘻嘻)。落盘:三参对象各 0x400+BT+chase。
纪律:只读;命中禁断点写 DONE;异常吞;自动继续。
"""
import lldb
import os

ROOT = "/tmp/wxsend3"
OUT = f"{ROOT}/r7"
OFF_SPAWNER = 0x6FDA37C
NEEDLE = b"\xe5\x98\xbb"
CHUNK = 1024
MAX_CHASE = 100

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
    bp = target.BreakpointCreateByAddress(slide + OFF_SPAWNER)
    bp.SetScriptCallbackFunction("cap7.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} spawner_bp@{slide+OFF_SPAWNER:#x}\n")


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
        if NEEDLE in d:
            return p
        for i in range(0, len(d) - 7, 8):
            v = int.from_bytes(d[i:i + 8], "little")
            if 0x100000000 < v < 0x8000000000:
                q.append(v)
    return None


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

        x0, x1, x2, lr = reg("x0"), reg("x1"), reg("x2"), reg("lr")
        sp = reg("sp")
        _st["n"] += 1
        carrier = _chase(proc, [x0, x1, x2])
        stack_hit = None
        for base, size in ((sp, 0x3000), (max(0x1000, sp - 0x1000), 0x1000)):
            sd = _read(proc, base, size)
            if sd and NEEDLE in sd and b"filehelper" in sd:
                stack_hit = base + sd.find(NEEDLE)
                break
        if carrier is None and stack_hit is not None:
            carrier = stack_hit
            if _st["n"] % 20 == 1:
                with open(f"{OUT}/stray.log", "a") as f:
                    f.write(f"#{_st['n']} x0={x0:#x} x1={x1:#x} x2={x2:#x}\n")
            return False

        with open(f"{OUT}/hit1.txt", "w") as f:
            f.write(f"slide={slide:#x}\nx0={x0:#x} x1={x1:#x} x2={x2:#x}(={x2}) x3={reg('x3')} lr={lr:#x}(+{lr-slide:#x})\n")
            f.write(f"needle 载体:{carrier:#x}" + (f"(栈窗@sp+{carrier-sp:#x})" if stack_hit else "") + "\n\n")
            f.write("== x0 对象 0x400 ==\n" + _hexdump(_read(proc, x0, 0x400) or b"", x0) + "\n")
            f.write("== x1 对象 0x400 ==\n" + _hexdump(_read(proc, x1, 0x400) or b"", x1) + "\n")
            if 0x100000000 < x2 < 0x8000000000:
                f.write("== x2 对象 0x200 ==\n" + _hexdump(_read(proc, x2, 0x200) or b"", x2) + "\n")
            else:
                f.write(f"x2 = 标量 {x2}(={x2})\n")
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
