"""双断点只读捕捉 v2(10-14 参数语义实证轮):

- slide+0x43f88e4(RPC 真调度器,主线程,真发即命中;hit4 实证)
- slide+0x490fb20(mars 通用任务投递器,任何网络任务都过;hit3 实证)

v2 要点(修 v1 实战暴露的问题):
- SBFrame 无 GetIdx → GetFrameID(v1 251 个 ERR 的根因);
- 043f88e4 是 RPC 家族调度器、0490fb20 任何网络任务都过 → 杂散极多:
  轻路径先抓 x0+指针追,判别门(转储含 b"filehelper")不过只记一行
  stray 日志、零重落盘;过了才全量 dump(寄存器 blob/栈符号化/x0 8KB)
  并禁用全部断点写 DONE(kill 前防残留 int3 的回调侧保证);
- 绝不写微信内存;异常全吞;命中自动继续(return False)。
"""
import lldb
import os
import time

ROOT = "/tmp/wxsend3"
OUT = f"{ROOT}/hits"
OFF_SEND = 0x43F88E4
OFF_SUBM = 0x490FB20
MAX_SUBM_HITS = 400    # 只数不落盘,上限防爆日志
MAX_SEND_HITS = 400
MAX_PTR_CHASE = 40
PTR_CHUNK = 512

os.makedirs(OUT, exist_ok=True)
_state = {"subm": 0, "send": 0, "bps": [], "lo": 0, "hi": 0, "slide": 0, "done": False,
          "needle": b"filehelper"}


def _load_needle():
    """判别门 needle:优先 /tmp/wxsend3/needle.bin(当轮正文原字节),
    缺席则回落 filehelper(会话对象也含——过宽,仅兜底)。"""
    try:
        with open(f"{ROOT}/needle.bin", "rb") as f:
            nd = f.read().strip()
        if nd:
            _state["needle"] = nd
    except OSError:
        pass


def install(debugger):
    _load_needle()
    target = debugger.GetSelectedTarget()
    slide = mod = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
            mod = m
            break
    if not slide:
        with open(f"{ROOT}/ERROR", "w") as f:
            f.write("wechat.dylib not found in target modules\n")
        raise RuntimeError("wechat.dylib not found")
    text = mod.FindSection("__TEXT")
    tsize = text.GetByteSize() if text.IsValid() else 0x9000000
    _state.update(slide=slide, lo=slide, hi=slide + tsize)
    bp_send = target.BreakpointCreateByAddress(slide + OFF_SEND)
    bp_send.SetScriptCallbackFunction("cap2.on_send")
    bp_subm = target.BreakpointCreateByAddress(slide + OFF_SUBM)
    bp_subm.SetScriptCallbackFunction("cap2.on_subm")
    _state["bps"] = [bp_send, bp_subm]
    with open(f"{ROOT}/ARMED", "w") as f:
        f.write(
            f"slide={slide:#x}\n"
            f"send_bp={slide + OFF_SEND:#x} id={bp_send.GetID()}\n"
            f"subm_bp={slide + OFF_SUBM:#x} id={bp_subm.GetID()}\n"
            f"text=[{slide:#x},{slide + tsize:#x})\n"
            f"t={time.time()}\n"
        )


def shutdown():
    """cmd 文件 continue 之后/收兵前调用:全禁用断点,幂等。"""
    try:
        target = lldb.debugger.GetSelectedTarget()
        target.DisableAllBreakpoints()
        for bp in _state.get("bps", []):
            bp.SetEnabled(False)
        with open(f"{ROOT}/SHUTDOWN_OK", "w") as f:
            f.write(f"send_hits={_state['send']} subm_hits={_state['subm']}\n")
    except Exception as exc:  # noqa: BLE001
        with open(f"{ROOT}/SHUTDOWN_ERR", "w") as f:
            f.write(repr(exc) + "\n")


def _rd(proc, addr, n):
    err = lldb.SBError()
    try:
        data = proc.ReadMemory(addr, n, err)
    except Exception:
        return None
    return data if err.Success() else None


def _ptrish(v):
    return 0x100000000 <= v < 0x800000000000


def _sym(target, addr):
    try:
        sa = target.ResolveLoadAddress(addr)
        if not sa.IsValid():
            return f"{addr:#x} (?)"
        modn = (sa.GetModule().GetFileSpec().basename if sa.GetModule() and sa.GetModule().GetFileSpec() else "?")
        sym = sa.GetSymbol()
        name = sym.GetName() if sym and sym.IsValid() else "?"
        return f"{addr:#x} {modn}`{name}+{sa.GetOffset():#x}"
    except Exception as exc:  # noqa: BLE001
        return f"{addr:#x} (sym-err {exc})"


def _chase_files(tag, parent, data, proc, report):
    """matched 全量路径:x0 缓冲内指针逐个追 512B 落盘并登记映射。"""
    n = 0
    for off in range(0, len(data) - 7, 8):
        v = int.from_bytes(data[off:off + 8], "little")
        if not _ptrish(v):
            continue
        blob = _rd(proc, v, PTR_CHUNK)
        if not blob:
            continue
        fn = f"{tag}_ptr{off:04x}.bin"
        with open(f"{OUT}/{fn}", "wb") as f:
            f.write(blob)
        report.append(f"  {parent}+{off:#x} -> {v:#x} => {fn}")
        n += 1
        if n >= MAX_PTR_CHASE:
            report.append("  (ptr-chase cap)")
            break


def _light_blobs(frame, regs, proc):
    """轻路径:regs+x0 4KB+其中指针追 512B(内存里,不落盘)。"""
    blobs = []
    x0 = _rd(proc, regs["x0"], 4096)
    if x0:
        blobs.append(x0)
        n = 0
        for off in range(0, len(x0) - 7, 8):
            v = int.from_bytes(x0[off:off + 8], "little")
            if not _ptrish(v):
                continue
            b = _rd(proc, v, PTR_CHUNK)
            if b:
                blobs.append(b)
                n += 1
                if n >= MAX_PTR_CHASE:
                    break
    return blobs


def _get_regs(frame, names):
    regs = {}
    for r in names:
        v = frame.FindRegister(r)
        regs[r] = v.GetValueAsUnsigned() if v and v.IsValid() else 0
    return regs


def _matched(blobs):
    nd = _state.get("needle") or b"filehelper"
    return any(nd in b for b in blobs if b)


def _stray(kind, note):
    with open(f"{OUT}/stray.log", "a") as f:
        f.write(f"{time.time():.3f} {kind} {note}\n")


def _full_dump(tag, frame, regs, proc, report):
    thread = frame.GetThread()
    target = proc.GetTarget()
    x0 = _rd(proc, regs["x0"], 12288)
    if x0:
        with open(f"{OUT}/{tag}_x0.bin", "wb") as f:
            f.write(x0)
        report.append(f"x0 {regs['x0']:#x} -> {tag}_x0.bin ({len(x0)}B)")
        _chase_files(tag, "x0", x0, proc, report)
    for r in ("x1", "x2", "x3", "x4", "x5", "x6", "x7"):
        v = regs[r]
        if _ptrish(v):
            b = _rd(proc, v, 1024)
            if b:
                with open(f"{OUT}/{tag}_{r}.bin", "wb") as f:
                    f.write(b)
                report.append(f"{r} {v:#x} -> {tag}_{r}.bin")
                _chase_files(tag, r, b, proc, report)
    st = _rd(proc, regs["sp"], 1024)
    if st:
        with open(f"{OUT}/{tag}_stack.bin", "wb") as f:
            f.write(st)
        report.append(f"stack {regs['sp']:#x} -> {tag}_stack.bin")
        lo, hi, slide = _state["lo"], _state["hi"], _state["slide"]
        for off in range(0, len(st) - 7, 8):
            v = int.from_bytes(st[off:off + 8], "little")
            if lo <= v < hi:
                report.append(f"  [sp+{off:#x}] dylib+{v - slide:#x}  {_sym(target, v)}")
    report.append(f"lr: {_sym(target, regs['lr'])}")
    report.append(f"pc: {_sym(target, regs['pc'])}")
    try:
        for fr in thread.frames:
            report.append(f"  frame#{fr.GetFrameID()} {_sym(target, fr.GetPC())}")
    except Exception as exc:  # noqa: BLE001
        report.append(f"  (frame walk err {exc})")
    report.append("BT:")
    report.append(str(thread))


def _finish_all(tag):
    """判别门命中:禁全部断点 + DONE。"""
    try:
        for bp in _state.get("bps", []):
            bp.SetEnabled(False)
    except Exception:
        pass
    _state["done"] = True
    with open(f"{ROOT}/DONE", "w") as f:
        f.write(f"matched=yes tag={tag} send_hits={_state['send']} subm_hits={_state['subm']}\n")


def on_send(frame, bp_loc, internal_dict):
    tag = "send_err"
    try:
        _state["send"] += 1
        i = _state["send"] - 1
        regs = _get_regs(frame, ("x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "sp", "fp", "lr", "pc"))
        proc = frame.GetThread().GetProcess()
        blobs = _light_blobs(frame, regs, proc)
        if not _matched(blobs):
            _stray("send", f"#{i} x0={regs['x0']:#x} lr={regs['lr']:#x} tid={frame.GetThread().GetIndexID()}")
            if _state["send"] >= MAX_SEND_HITS:
                bp_loc.GetBreakpoint().SetEnabled(False)
            return False
        tag = f"hit_send{i}"
        report = [
            f"== {tag} t={time.time():.3f} MATCHED ==",
            f"thread={frame.GetThread().GetName()} tid={frame.GetThread().GetIndexID()}",
            "regs: " + " ".join(f"{k}={v:#x}" for k, v in regs.items()),
        ]
        _full_dump(tag, frame, regs, proc, report)
        with open(f"{OUT}/{tag}.txt", "w") as f:
            f.write("\n".join(report) + "\n")
        _finish_all(tag)
    except Exception as exc:  # noqa: BLE001 — 取证回调绝不抛
        with open(f"{OUT}/{tag}_ERR.txt", "w") as f:
            f.write(repr(exc) + "\n")
    return False


def on_subm(frame, bp_loc, internal_dict):
    tag = "subm_err"
    try:
        _state["subm"] += 1
        i = _state["subm"] - 1
        regs = _get_regs(frame, ("x0", "x1", "x2", "x3", "x4", "x5", "sp", "lr"))
        proc = frame.GetThread().GetProcess()
        blobs = []
        for r in ("x0", "x3", "x4", "x5"):
            if _ptrish(regs[r]):
                b = _rd(proc, regs[r], 1024)
                if b:
                    blobs.append(b)
        if not _matched(blobs):
            if _state["subm"] >= MAX_SUBM_HITS:
                bp_loc.GetBreakpoint().SetEnabled(False)
            return False
        tag = f"hit_subm{i}"
        report = [
            f"== {tag} t={time.time():.3f} MATCHED ==",
            f"thread={frame.GetThread().GetName()} tid={frame.GetThread().GetIndexID()}",
            "regs: " + " ".join(f"{k}={v:#x}" for k, v in regs.items()),
        ]
        for r in ("x0", "x1", "x2", "x3", "x4", "x5"):
            if _ptrish(regs[r]):
                b = _rd(proc, regs[r], 2048)
                if b:
                    with open(f"{OUT}/{tag}_{r}.bin", "wb") as f:
                        f.write(b)
                    report.append(f"{r} {regs[r]:#x} -> {tag}_{r}.bin")
        report.append(f"lr: {_sym(proc.GetTarget(), regs['lr'])}")
        try:
            for fr in frame.GetThread().frames:
                report.append(f"  frame#{fr.GetFrameID()} {_sym(proc.GetTarget(), fr.GetPC())}")
        except Exception as exc:  # noqa: BLE001
            report.append(f"  (frame walk err {exc})")
        with open(f"{OUT}/{tag}.txt", "w") as f:
            f.write("\n".join(report) + "\n")
        _finish_all(tag)
    except Exception as exc:  # noqa: BLE001
        with open(f"{OUT}/{tag}_ERR.txt", "w") as f:
            f.write(repr(exc) + "\n")
    return False
