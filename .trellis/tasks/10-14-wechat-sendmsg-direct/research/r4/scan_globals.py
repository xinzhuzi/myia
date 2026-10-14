"""扫 wechat.dylib 数据段找 ctx 家族全局槽。
目标 qword:0x8a3913c18(ctx 本体)/0x8a3479600(ctx+8 内层)/
或任意指向 vtable==0x134d396b8 对象的堆指针(双跳验证)。
"""
import lldb

VT = 0x134D396B8
KNOWN = [0x8A3913C18, 0x8A3479600]

def install(debugger):
    target = debugger.GetSelectedTarget()
    proc = target.GetProcess()
    mod = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            mod = m
            break
    out = open("/tmp/wxsend3/global_scan.txt", "w")
    out.write(f"VT={VT:#x} KNOWN={[hex(k) for k in KNOWN]}\n")
    found = []
    for sec in mod.section_iter():
        name = sec.GetName() or ""
        if name not in ("__DATA", "__DATA_CONST", "__bss", "__common", "__data", "__const"):
            continue
        base = sec.GetLoadAddress(target)
        size = sec.GetByteSize()
        if base == 0 or size == 0 or size > 0x8000000:
            continue
        err = lldb.SBError()
        data = proc.ReadMemory(base, min(size, 0x400000), err)
        if data is None:
            out.write(f"sec {name}: read fail\n")
            continue
        out.write(f"sec {name} @{base:#x} size={min(size,0x400000):#x}\n")
        for i in range(0, len(data) - 7, 8):
            v = int.from_bytes(data[i:i+8], "little")
            if v in KNOWN:
                found.append((base + i, v, "KNOWN"))
            elif 0x800000000 < v < 0x8000000000:
                e2 = lldb.SBError()
                d2 = proc.ReadMemory(v, 8, e2)
                if e2.Success() and d2 and int.from_bytes(d2, "little") == VT:
                    found.append((base + i, v, "VT-MATCH"))
    for slot, val, kind in found[:40]:
        slide = None
        for m in target.module_iter():
            if m.file.basename == "wechat.dylib":
                slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
        out.write(f"FOUND {kind}: slot@{slot:#x} (slide+{slot-slide:#x}) -> {val:#x}\n")
    out.write(f"total={len(found)}\n")
    out.close()
    debugger.HandleCommand("detach")
    debugger.HandleCommand("quit")

def __lldb_init_module(debugger, internal_dict):
    install(debugger)
