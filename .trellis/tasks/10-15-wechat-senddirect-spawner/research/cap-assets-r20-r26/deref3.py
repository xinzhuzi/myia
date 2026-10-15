import lldb
def run():
    t = lldb.debugger.GetSelectedTarget()
    p = t.GetProcess()
    e = lldb.SBError()
    d = p.ReadMemory(0x784774ab0, 96, e)
    print("BODY_TRUE=%s" % (d.hex() if d else "ERR " + str(e.GetError())))
    if d:
        print("BODY_ASCII=%s" % "".join(chr(c) if 32 <= c < 127 else "." for c in d))
