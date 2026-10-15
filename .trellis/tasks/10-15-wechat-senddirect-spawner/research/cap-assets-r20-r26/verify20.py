import lldb
import os

# 双模式:基线模式把两个锚点字节写入 baseline.txt;复验模式比对并按需还原 L3。
OUT = "/tmp/wxsend3/r20"
L3_RVA = 0x433C5F0
BL_RVA = 0x435E070  # L4 内 bl L3 指令
L3_EXPECT = "fc6fbca9f65701a9"


def run(debugger, mode):
    t = debugger.GetSelectedTarget()
    slide = None
    for m in t.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(t)
            break
    proc = t.GetProcess()
    err = lldb.SBError()
    d8 = proc.ReadMemory(slide + L3_RVA, 8, err)
    d4 = proc.ReadMemory(slide + BL_RVA, 4, err)
    print("LIVE_L3=%s" % (d8.hex() if d8 else "READ_ERR"))
    print("LIVE_BL=%s" % (d4.hex() if d4 else "READ_ERR"))
    if mode == "baseline":
        with open(f"{OUT}/baseline.txt", "w") as f:
            f.write("l3=%s\nbl=%s\n" % (d8.hex(), d4.hex()))
        print("BASELINE_WRITTEN")
        return
    # 复验模式
    ok = True
    if d8.hex() != L3_EXPECT:
        werr = lldb.SBError()
        proc.WriteMemory(slide + L3_RVA, bytes.fromhex(L3_EXPECT), werr)
        print("L3_RESTORED=%s" % werr.Success())
        ok = False
    else:
        print("L3_INTACT")
    try:
        with open(f"{OUT}/baseline.txt") as f:
            bl_expect = dict(line.strip().split("=") for line in f if "=" in line)["bl"]
    except Exception:
        bl_expect = None
    if bl_expect and d4.hex() != bl_expect:
        print("BL_MISMATCH expect=%s" % bl_expect)
        ok = False
    else:
        print("BL_INTACT")
    print("VERIFY_%s" % ("PASS" if ok else "FIXED_OR_FAIL"))
