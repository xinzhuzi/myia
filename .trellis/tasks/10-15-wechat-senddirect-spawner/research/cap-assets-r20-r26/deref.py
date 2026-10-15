import lldb
def run():
    t = lldb.debugger.GetSelectedTarget()
    p = t.GetProcess()
    e = lldb.SBError()
    for addr in (0x17393a150, 0x77a52c1b8, 0x783774c00):
        d = p.ReadMemory(addr, 64, e)
        print("DEREF %#x => %s" % (addr, d.hex() if d else "ERR " + str(e.GetError())))
