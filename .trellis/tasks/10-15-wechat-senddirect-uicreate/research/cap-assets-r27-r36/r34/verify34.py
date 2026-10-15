"""verify34:窗口后双锚点字节复验(只读,不改不修)。
L3 rva 0x433C5F0 期望 8B=fc6fbca9f65701a9;bl@0x435E070 期望 4B=6079ff97。"""
import lldb

L3_RVA = 0x433C5F0
BL_RVA = 0x435E070
L3_EXPECT = "fc6fbca9f65701a9"
BL_EXPECT = "6079ff97"


def run(debugger):
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
    a8 = d8.hex() if d8 else "READ_ERR"
    a4 = d4.hex() if d4 else "READ_ERR"
    ok = a8 == L3_EXPECT and a4 == BL_EXPECT
    print("LIVE_L3=%s" % a8)
    print("LIVE_BL=%s" % a4)
    print("VERIFY_%s" % ("PASS" if ok else "FAIL"))
