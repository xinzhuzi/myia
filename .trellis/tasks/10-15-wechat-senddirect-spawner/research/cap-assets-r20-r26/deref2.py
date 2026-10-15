import lldb
def run():
    t = lldb.debugger.GetSelectedTarget()
    p = t.GetProcess()
    e = lldb.SBError()
    # hit1 mc=0x7762c8918, PATCHED n=2 mc=0x77a6ce418; 宿主=mc-0x30
    for mc in (0x7762c8918, 0x77a6ce418):
        for off, size in ((-0x30, 0x60),):
            d = p.ReadMemory(mc + off, size, e)
            print("MC %#x host(%#x) => %s" % (mc, mc - 0x30, d.hex() if d else "ERR " + str(e.GetError())))
    print("SVC_EXPECT=0x77e72d698")
