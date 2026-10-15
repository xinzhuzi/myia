"""cap20(cap19 区分实验·断点收窄版):改断 L4 内 call L3 的 bl 指令
(0x435E070;L3 入口 0x433c5f0 有 3 个代码 caller,入站/杂项走兄弟 caller
0x43527f4/0x435ee58,发送链实证走 L4→L3——HuntR20 查证)。
此处寄存器 x0-x3 = L3 四参,槽位几何与 cap16/18/19 一致(msgctx=x1)。
全命中补丁(≤5):needle 门只读 x1 头 0x58(body 槽 +0x40~0x57)减停机时延;
首命中另 dump 0x270 全量留证。判据:补丁版正文落 localdb=阳性(cap18 补错跳);
仅原文=阴性(内容按 msg-id 在别处)。needle=嘻嘻~c20w(13B) forge=嘻嘻~直发c20w(16B)。"""
import lldb
import os

OUT = "/tmp/wxsend3/r20"
OFF_BP = 0x435E070  # L4(FUN_0435df74) 内 bl 0x0433c5f0 指令地址
NEEDLE = "嘻嘻~c20w".encode("utf-8")
FORGED = "嘻嘻~直发c20w".encode("utf-8")

_st = {"bp": None, "slide": 0, "done": False, "n": 0, "stray": 0}


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
    bp.SetScriptCallbackFunction("cap20.on_hit")
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
        if NEEDLE not in head:
            _st["stray"] += 1
            with open(f"{OUT}/stray.log", "a") as f:
                f.write(f"mc={mc:#x}\n")
            return False
        _st["n"] += 1
        err = lldb.SBError()
        if _st["n"] == 1:
            blob = _read(proc, mc, 0x270) or b""
            with open(f"{OUT}/hit1.txt", "w") as f:
                f.write(f"slide={_st['slide']:#x} mc={mc:#x}\nmsgctx270={blob.hex()}\n")
        slot2 = bytearray(24)
        slot2[0:len(FORGED)] = FORGED
        slot2[23] = len(FORGED)
        ok = proc.WriteMemory(mc + 0x40, bytes(slot2), err)
        with open(f"{OUT}/PATCHED", "a") as f:
            f.write(f"n={_st['n']} mc={mc:#x} wrote={ok} err={err.Success()} forged={FORGED.decode()}\n")
        if _st["n"] >= 5:
            _st["done"] = True
            if _st["bp"] is not None:
                _st["bp"].SetEnabled(False)
    except Exception as exc:
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(repr(exc) + "\n")
        except OSError:
            pass
    return False  # 放行:真实 L4→L3 链带补丁正文跑


def __lldb_init_module(debugger, internal_dict):
    install(debugger)
