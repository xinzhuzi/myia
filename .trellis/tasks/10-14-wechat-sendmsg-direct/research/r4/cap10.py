"""cap10(TLS 最后一跳):F_exec 命中时读 TLS 基址,扫全部 TLS 槽,
追哪个槽的值通向含 F_exec 指针值的堆块(=协程帧/current-task)。

arm64 macOS:TPIDRROEL0(只读 TLS 基址寄存器)→ 附近为本线程 TLS 区。
流程:bp F_exec 入口(needle 门)→ 读 tpidrro_el0 → dump TLS±0x800 →
对每个疑似指针值 deref 0x200 搜 F_exec 值 → 报告 TLS 偏移→堆块→槽位。
同时搜 ctx/msgctx 值(实参块定位)。只读;命中禁断点写 DONE;异常吞。
"""
import lldb
import os

ROOT = "/tmp/wxsend3"
OUT = f"{ROOT}/r10"
OFF_FEXEC = 0x83E394
NEEDLE = b"\xe5\x98\xbb"

os.makedirs(OUT, exist_ok=True)
_st = {"bp": None, "slide": 0, "done": False}


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
    bp = target.BreakpointCreateByAddress(slide + OFF_FEXEC)
    bp.SetScriptCallbackFunction("cap10.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        slide = _st["slide"]
        fexec = slide + OFF_FEXEC

        x0 = frame.FindRegister("x0")
        x1 = frame.FindRegister("x1")
        ctx = x0.GetValueAsUnsigned() if x0 and x0.IsValid() else 0
        msgctx = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        blob = _read(proc, msgctx, 0x230) or b""
        if NEEDLE not in blob:
            with open(f"{OUT}/stray.log", "a") as f:
                f.write(f"x0={ctx:#x} x1={msgctx:#x} blob_len={len(blob)}\n")
            return False
        _st["done"] = True

        # TLS 基址:寄存器名不可读(cap10 实证)→ expr pthread_self()
        # (Darwin arm64:pthread_self() 返回值 == tpidrro_el0 == pthread 结构基址)
        tls_base = 0
        opts = lldb.SBExpressionOptions()
        opts.SetTimeoutInMicroSeconds(3_000_000)
        v = frame.EvaluateExpression("(unsigned long)pthread_self()", opts)
        if v.IsValid() and v.GetError().Success():
            tls_base = v.GetValueAsUnsigned()

        with open(f"{OUT}/hit1.txt", "w") as f:
            f.write(f"slide={slide:#x} fexec={fexec:#x}\nctx={ctx:#x} msgctx={msgctx:#x}\ntls_base={tls_base:#x}\n\n")
            if not tls_base:
                f.write("TLS 基址寄存器不可读,终止\n")
            else:
                fexec8 = fexec.to_bytes(8, "little")
                ctx8 = ctx.to_bytes(8, "little")
                msg8 = msgctx.to_bytes(8, "little")
                data = _read(proc, tls_base, 0x1000) or b""
                f.write(f"== TLS 区 {tls_base:#x} 0x1000 扫描 ==\n")
                found_frames = set()
                for off in range(0, len(data) - 7, 8):
                    v = int.from_bytes(data[off:off + 8], "little")
                    if not (0x100000000 < v < 0x8000000000):
                        continue
                    blk = _read(proc, v, 0x300)
                    if not blk:
                        continue
                    p = blk.find(fexec8)
                    if p >= 0:
                        f.write(f"★ TLS+{off:#x} → 堆块 {v:#x} 含 F_exec @块内+{p:#x}\n")
                        found_frames.add(v)
                        # 该块同时搜 ctx/msgctx
                        pc_ = blk.find(ctx8)
                        pm = blk.find(msg8)
                        if pc_ >= 0:
                            f.write(f"   ☆ 同块 ctx @+{pc_:#x}\n")
                        if pm >= 0:
                            f.write(f"   ☆ 同块 msgctx @+{pm:#x}\n")
                        f.write(f"   块 dump 头 0x100:\n")
                        for i in range(0, 0x100, 16):
                            c = blk[i:i + 16]
                            f.write(f"   {v+i:#x}  {c.hex(' '):<48} {''.join(chr(b) if 32<=b<127 else '.' for b in c)}\n")
                if not found_frames:
                    f.write("(TLS 区一级 deref 未命中 F_exec;二级待续)\n")
                    # 二级:TLS 槽→堆块→块内指针→再 deref
                    for off in range(0, len(data) - 7, 8):
                        v = int.from_bytes(data[off:off + 8], "little")
                        if not (0x100000000 < v < 0x8000000000):
                            continue
                        blk = _read(proc, v, 0x200)
                        if not blk:
                            continue
                        for k in range(0, len(blk) - 7, 8):
                            v2 = int.from_bytes(blk[k:k + 8], "little")
                            if not (0x100000000 < v2 < 0x8000000000) or v2 == v:
                                continue
                            b2 = _read(proc, v2, 0x200)
                            if b2 and fexec8 in b2:
                                f.write(f"★★ TLS+{off:#x} → {v:#x} +{k:#x} → {v2:#x} 含 F_exec(二级)\n")
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
