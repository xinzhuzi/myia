"""cap30(目的地锚定):断 0x70AC5F0(fn384597+124 的 bl 382402 指令)——
x0=NSString 源(needle 门 deref 判),x8=拷贝目的地结构(QString)。
命中→dump x0/x8→解析 x8 结构(内联 or *x8 指针)→write watch 挂字符缓冲
→轮询采栈=文本搬运链(输入框存储/构造)。"""
import lldb
import os

OUT = "/tmp/wxsend3/r30"
OFF_CALL = 0x70AC5F0
NEEDLE8 = "嘻嘻~c38w".encode("utf-8")
NEEDLE16 = "嘻嘻~c38w".encode("utf-16-le")
WATCH_LEN = 32

_st = {"bp": None, "wp": None, "slide": 0, "P": 0, "n": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    return proc.ReadMemory(addr, size, err) if err.Success() else None


def _find_needle(proc, obj_addr):
    blob = _read(proc, obj_addr, 0x100)
    if blob is None:
        return 0
    for pat in (NEEDLE8, NEEDLE16):
        i = blob.find(pat)
        if i >= 0:
            return obj_addr + i
    for off in range(0, len(blob) - 7, 8):
        p = int.from_bytes(blob[off:off + 8], "little")
        if 0x100000000 < p < 0x800000000000:
            d = _read(proc, p, 0x100)
            if d is None:
                continue
            for pat in (NEEDLE8, NEEDLE16):
                i = d.find(pat)
                if i >= 0:
                    return p + i
    return 0


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
    bp = target.BreakpointCreateByAddress(slide + OFF_CALL)
    bp.SetScriptCallbackFunction("cap30.on_hit")
    _st["bp"] = bp
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} bp={slide + OFF_CALL:#x}\n")


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["P"]:
            return False
        _st["n"] += 1
        proc = frame.GetThread().GetProcess()
        x0 = frame.FindRegister("x0")
        x8 = frame.FindRegister("x8")
        obj = x0.GetValueAsUnsigned() if x0 and x0.IsValid() else 0
        dst = x8.GetValueAsUnsigned() if x8 and x8.IsValid() else 0
        if not obj or not dst:
            return False
        p = _find_needle(proc, obj)
        if not p:
            return False
        _st["P"] = p
        dstblob = _read(proc, dst, 0x40) or b""
        # 解析目的地:x8 结构首 8B 若是堆指针,deref 判是否字符缓冲;否则 x8 自身即缓冲区起点
        watch_addr = 0
        q0 = int.from_bytes(dstblob[0:8], "little")
        cand = []
        if 0x100000000 < q0 < 0x800000000000:
            cand.append(("deref_x8", q0))
        cand.append(("x8_inline", dst))
        with open(f"{OUT}/hit{_st['n']}.txt", "w") as f:
            f.write(f"obj={obj:#x} needle_at={p:#x} x8_dst={dst:#x} dst_head={dstblob.hex()}\n")
        for tag, a in cand:
            d = _read(proc, a, 0x40)
            if d and (NEEDLE16[:8] in d or NEEDLE8[:6] in d):
                watch_addr = a
                _st["wtag"] = tag
                break
        if not watch_addr:
            # 目的地此刻还是空(拷贝未发生):直接 watch x8 结构起点(write 捕获拷贝)
            watch_addr = dst
            _st["wtag"] = "x8_struct"
        if _st["bp"] is not None:
            _st["bp"].SetEnabled(False)
        wp = proc.GetTarget().WatchAddress(watch_addr, WATCH_LEN, False, True, lldb.SBError())
        if wp and wp.IsValid():
            _st["wp"] = wp
            with open(f"{OUT}/WATCH_ARMED", "w") as f:
                f.write(f"P={p:#x} watch={watch_addr:#x} tag={_st['wtag']}\n")
        else:
            with open(f"{OUT}/WATCH_FAIL", "w") as f:
                f.write("invalid\n")
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
