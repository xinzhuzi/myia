"""纯读诊断:反汇编 0x5980a6c 的调用者(含 lr rva 0x5971cb8 的函数)与
enter 内 getter 0x5980d74,写 disdiag.txt。零断点零写入。"""
import lldb

OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-15-wechat-senddirect-uicreate/research/community-adapt/truepath"


def run(debugger):
    t = debugger.GetSelectedTarget()
    slide = None
    for m in t.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(t)
            break
    out = open(f"{OUT}/disdiag.txt", "w")
    out.write("slide=%#x\n" % slide)
    for rva in (0x5971cb8, 0x5980d74):
        a = slide + rva
        sa = t.ResolveLoadAddress(a)
        fn = sa.GetFunction()
        if not (fn and fn.IsValid()):
            fn = None
            sym = sa.GetSymbol()
            if sym and sym.IsValid():
                s = sym.GetStartAddress().GetLoadAddress(t)
                e = sym.GetEndAddress().GetLoadAddress(t)
                out.write("== rva=%#x sym_rva=[%#x,%#x] name=%s\n" % (rva, s - slide, e - slide, sym.GetName()))
                if s and e and e > s:
                    insts = t.ReadInstructions(lldb.SBAddress(s, t), 4000)
                    for i in insts:
                        out.write("%#x: %s %s\n" % (i.GetAddress().GetLoadAddress(t) - slide,
                                                     i.GetMnemonic(t), i.GetOperands(t)))
                    continue
            out.write("== rva=%#x NO-BOUNDS\n" % rva)
            continue
        s = fn.GetStartAddress().GetLoadAddress(t)
        e = fn.GetEndAddress().GetLoadAddress(t)
        out.write("== rva=%#x fn_rva=[%#x,%#x] name=%s\n" % (rva, s - slide, e - slide, fn.GetName()))
        insts = t.ReadInstructions(lldb.SBAddress(s, t), 4000)
        for i in insts:
            out.write("%#x: %s %s\n" % (i.GetAddress().GetLoadAddress(t) - slide,
                                         i.GetMnemonic(t), i.GetOperands(t)))
    out.close()
    print("DISDIAG_DONE")
