import lldb

def run(debugger):
    t = debugger.GetSelectedTarget()
    slide = None
    for m in t.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(t)
            break
    proc = t.GetProcess()
    addr = slide + 0x433C5F0
    err = lldb.SBError()
    data = proc.ReadMemory(addr, 8, err)
    if not err.Success():
        print("READ_ERR", err.GetError())
        return
    print("LIVE_BYTES=%s" % data.hex())
    if data.hex() != "fc6fbca9f65701a9":
        werr = lldb.SBError()
        proc.WriteMemory(addr, bytes.fromhex("fc6fbca9f65701a9"), werr)
        print("RESTORED=%s" % werr.Success())
    else:
        print("INTACT")
