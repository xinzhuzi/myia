"""LLDB 断点回调:命中即写寄存器+回溯到 /tmp/wxsend2/hit.txt,自动继续,
并自禁用断点(恢复原始字节,防残留 int3)。零交互,批式安全。"""
import lldb

HIT_PATH = "/tmp/wxsend2/hit3.txt"


def on_hit(frame, bp_loc, internal_dict):
    try:
        thread = frame.GetThread()
        proc = thread.GetProcess()
        with open(HIT_PATH, "w") as out:
            out.write(f"thread: {thread.GetName()} tid={thread.GetIndexID()}\n")
            for r in ("x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "sp", "lr"):
                v = frame.FindRegister(r)
                out.write(f"{r} = {v.GetValueAsUnsigned():#x}\n" if v and v.IsValid() else f"{r} = ?\n")
            # x1/x2 若是 C 字符串/NSString,读出来(payload 线索)
            for r in ("x0", "x1", "x2", "x3"):
                v = frame.FindRegister(r)
                if not (v and v.IsValid()):
                    continue
                addr = v.GetValueAsUnsigned()
                if addr > 0x1000:
                    err = lldb.SBError()
                    data = proc.ReadMemory(addr, 160, err)
                    if err.Success() and data:
                        printable = bytes(b for b in data if 32 <= b < 127 or b >= 0x80)
                        out.write(f"mem[{r}] = {printable[:120]!r}\n")
            out.write("BT:\n")
            out.write(str(thread))
            out.write("\nMEM-X4-X5:\n")
            for r in ("x4", "x5"):
                v = frame.FindRegister(r)
                if v and v.IsValid():
                    addr = v.GetValueAsUnsigned()
                    err2 = lldb.SBError()
                    data = proc.ReadMemory(addr, 200, err2) if addr > 0x10000 else None
                    if data:
                        out.write(f"mem[{r}] = {bytes(b for b in data if 32 <= b < 127 or b >= 0x80)!r}\n")
        bp = bp_loc.GetBreakpoint()
        bp.SetEnabled(False)
    except Exception as exc:  # noqa: BLE001 - 取证回调绝不抛
        with open(HIT_PATH, "a") as out:
            out.write(f"callback-error: {exc}\n")
    return False  # 自动继续,不停进程
