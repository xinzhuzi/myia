"""cap8(继续做完):断点命中处嵌套直调——协程上下文活体内验证。

机理:触发真发停在 F_exec 入口 → 此刻协程 current-task TLS 已就位(上轮
C++ 异常的真因) → 同一停止态内 expr 嵌套调用 F_exec(ctx, 伪造 msgctx)
= 在合法上下文里跑直调。仍在已批范围(attach+只读+函数直调;expr 局部
缓冲=批准的参数装载)。

on_hit 流:读 x0=ctx/x1=msgctx → 模板 0x230B → 三槽补丁(新变体正文)+
+0x228 置零 → EvaluateExpression(F_exec(ctx, buf)) → 记 rc/异常 → 禁断点
写 DONE → 自动继续(外层触发送随后完成)。
"""
import lldb
import os
import time

ROOT = "/tmp/wxsend3"
OUT = f"{ROOT}/r8"
OFF_FEXEC = 0x83E394
NEEDLE = b"\xe5\x98\xbb"
PEER = b"filehelper"
DISPLAY = "文件传输助手"
BODY = "嘻嘻~direct1"  # 与触发正文不同的变体

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
    bp.SetScriptCallbackFunction("cap8.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x}\n")


def _inline23(text: bytes):
    rec = bytearray(24)
    n = min(len(text), 23)
    rec[:n] = text[:n]
    rec[23] = n
    return bytes(rec)


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        target = proc.GetTarget()
        slide = _st["slide"]
        x0 = frame.FindRegister("x0")
        x1 = frame.FindRegister("x1")
        ctx = x0.GetValueAsUnsigned() if x0 and x0.IsValid() else 0
        msgctx = x1.GetValueAsUnsigned() if x1 and x1.IsValid() else 0
        template = _read(proc, msgctx, 0x230)
        if not template or NEEDLE not in template:
            return False  # 非本轮触发的命中(杂散),继续
        _st["done"] = True

        report = {"slide": slide, "ctx": ctx, "msgctx": msgctx,
                  "template_len": len(template)}
        # 模板补丁:三槽 + +0x228 置零
        buf = bytearray(template)
        buf[0x00] = 1
        buf[0x08:0x20] = _inline23(PEER)
        buf[0x48:0x60] = _inline23(BODY.encode("utf-8"))
        buf[0x130:0x148] = _inline23(DISPLAY.encode("utf-8"))
        buf[0x228:0x230] = b"\x00" * 8

        # expr:局部缓冲字面量 + 调用(十进制字节数组惯例)
        arr = ",".join(str(b) for b in buf)
        expr = (
            "(int)({\n"
            "  unsigned char m[560] = {" + arr + "};\n"
            f"  ((int(*)(void*,void*))0x{slide + OFF_FEXEC:x})"
            f"((void*)0x{ctx:x}, (void*)m);\n"
            "})"
        )
        report["expr_len"] = len(expr)
        t0 = time.time()
        options = lldb.SBExpressionOptions()
        options.SetTimeoutInMicroSeconds(40_000_000)
        options.SetUnwindOnError(True)
        options.SetIgnoreBreakpoints(True)
        value = frame.EvaluateExpression(expr, options)
        dt = int((time.time() - t0) * 1000)
        if value.IsValid() and value.GetError().Success():
            report["nested_call"] = "OK"
            report["rc"] = value.GetValueAsSigned()
        else:
            report["nested_call"] = "FAIL"
            report["err"] = str(value.GetError())[:200] if value.IsValid() else "invalid"
        report["expr_ms"] = dt

        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        with open(f"{OUT}/DONE", "w") as f:
            import json
            json.dump(report, f, ensure_ascii=False, indent=1)
    except Exception as exc:  # noqa: BLE001
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False  # 自动继续:外层触发送随后完成


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
