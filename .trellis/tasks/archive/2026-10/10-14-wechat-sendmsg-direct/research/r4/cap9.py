"""cap9(任务生命周期追踪):F_exec 恢复现场反查任务对象→三值槽位定位。

机理:F_exec 入口命中时,父帧(蹦床 0xa6b590 族)的 x0=它正在恢复的任务/
协程对象。dump 该对象+两级上游,搜索三个已知值的槽位:
  ① resume 值 = slide+0x83e394(F_exec 自身)
  ② ctx 值 = 本帧 x0
  ③ msgctx 值 = 本帧 x1
命中槽位=任务→(resume,实参)映射=伪造配方最后拼图。
纪律:只读;命中禁断点写 DONE;异常吞;自动继续。
"""
import lldb
import os

ROOT = "/tmp/wxsend3"
OUT = f"{ROOT}/r9"
OFF_FEXEC = 0x83E394
NEEDLE = b"\xe5\x98\xbb"

os.makedirs(OUT, exist_ok=True)
_st = {"bp": None, "slide": 0, "done": False}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


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
    bp = target.BreakpointCreateByAddress(slide + OFF_FEXEC)
    bp.SetScriptCallbackFunction("cap9.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        target = proc.GetTarget()
        slide = _st["slide"]
        fexec = slide + OFF_FEXEC

        x0 = frame.FindRegister("x0")
        x1 = frame.FindRegister("x1")
        ctx = x0.GetValueAsUnsigned() if x0 and x0.IsValid() else 0
        msgctx = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        blob = _read(proc, msgctx, 0x230) or b""
        if NEEDLE not in blob:
            return False  # 杂散
        _st["done"] = True

        with open(f"{OUT}/hit1.txt", "w") as f:
            f.write(f"slide={slide:#x} fexec={fexec:#x}\nctx={ctx:#x} msgctx={msgctx:#x}\n\n")
            # 父帧链:蹦床与其上游,各读 x0(它们恢复的对象)
            thread = frame.GetThread()
            candidates = []
            for idx in range(1, min(6, thread.GetNumFrames())):
                fr = thread.GetFrameAtIndex(idx)
                if not fr.IsValid():
                    continue
                pc = fr.GetPCAddress().GetLoadAddress(target)
                rx0 = fr.FindRegister("x0")
                v = rx0.GetValueAsUnsigned() if rx0 and rx0.IsValid() else 0
                f.write(f"#frame{idx}: pc+{(pc - slide):#x} x0={v:#x}\n")
                if v > 0x10000:
                    candidates.append((idx, v))
            # 候选对象 dump+三值搜索
            for idx, obj in candidates[:4]:
                data = _read(proc, obj, 0x400)
                if not data:
                    continue
                f.write(f"\n== 对象(帧{idx} x0)@{obj:#x} 0x400 ==\n")
                f.write(_hexdump(data, obj) + "\n")
                for label, val in (("F_exec", fexec), ("ctx", ctx), ("msgctx", msgctx)):
                    needle8 = val.to_bytes(8, "little")
                    off = 0
                    while True:
                        pos = data.find(needle8, off)
                        if pos < 0:
                            break
                        f.write(f"  ★ {label} 槽: 对象+{pos:#x} = {val:#x}\n")
                        off = pos + 8
            # msgctx 自身也搜 F_exec/ctx(状态可能内联)
            for label, val in (("F_exec@msgctx", fexec), ("ctx@msgctx", ctx)):
                pos = blob.find(val.to_bytes(8, "little"))
                if pos >= 0:
                    f.write(f"  ★ {label} 槽: msgctx+{pos:#x}\n")
            # 宽域扫描:栈 32KB + ctx 邻域 ±2KB,搜 F_exec 指针值(任务 resume 字段)
            sp = frame.FindRegister("sp")
            spv = sp.GetValueAsUnsigned() if sp and sp.IsValid() else 0
            f.write(f"\nsp={spv:#x}\n== 宽域 F_exec 值扫描 ==\n")
            for label, base, size in (
                ("栈下", max(0x1000, spv - 0x4000), 0x4000),
                ("栈上", spv, 0x4000),
                ("ctx邻域", max(0x1000, ctx - 0x2000), 0x4000),
            ):
                data = _read(proc, base, size)
                if not data:
                    continue
                needle8 = fexec.to_bytes(8, "little")
                off = 0
                while True:
                    pos = data.find(needle8, off)
                    if pos < 0:
                        break
                    f.write(f"  ★ F_exec 值 @ {label} {base + pos:#x}(sp{base + pos - spv:+#x})\n")
                    off = pos + 8
                # 同时搜 msgctx 指针(任务状态块应含它)
                needle8m = msgctx.to_bytes(8, "little")
                off = 0
                while True:
                    pos = data.find(needle8m, off)
                    if pos < 0:
                        break
                    f.write(f"  ☆ msgctx 值 @ {label} {base + pos:#x}(sp{base + pos - spv:+#x})\n")
                    off = pos + 8
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
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
