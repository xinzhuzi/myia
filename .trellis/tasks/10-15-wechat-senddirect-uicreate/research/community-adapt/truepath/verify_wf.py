"""truepath 锚点复验(纯读):读 L3(0x433C5F0, 8B)与 BL(0x435E070, 4B),
比对期望 fc6fbca9f65701a9 / 6079ff97。与 vfy/verify20.py 不同:本脚本
绝不 WriteMemory——FAIL 即异常,如实记录并停手(微信零伤红线)。"""
import lldb

OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"
L3_RVA = 0x433C5F0
BL_RVA = 0x435E070
L3_EXPECT = "fc6fbca9f65701a9"
BL_EXPECT = "6079ff97"


def run(debugger, tag):
    t = debugger.GetSelectedTarget()
    slide = None
    for m in t.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(t)
            break
    proc = t.GetProcess()
    err = lldb.SBError()
    d8 = proc.ReadMemory(slide + L3_RVA, 8, err) if slide else None
    d4 = proc.ReadMemory(slide + BL_RVA, 4, err) if slide else None
    l3 = d8.hex() if d8 else "READ_ERR"
    bl = d4.hex() if d4 else "READ_ERR"
    ok = (l3 == L3_EXPECT and bl == BL_EXPECT)
    print("TAG=%s slide=%s LIVE_L3=%s LIVE_BL=%s VERIFY_%s"
          % (tag, hex(slide) if slide else "NOSLIDE", l3, bl, "PASS" if ok else "FAIL"))
    with open(f"{OUT}/verify_{tag}.txt", "w") as f:
        f.write("slide=%s l3=%s expect=%s bl=%s expect=%s result=%s\n"
                % (hex(slide) if slide else "NOSLIDE", l3, L3_EXPECT, bl, BL_EXPECT,
                   "PASS" if ok else "FAIL"))
