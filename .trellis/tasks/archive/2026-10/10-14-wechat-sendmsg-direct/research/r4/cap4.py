"""r4 钉入轮(10-15,P-0 已裁后):入队侧断点定位 F_send + 三必验项。

断 slide+0x000a6060(enqueue_a)/slide+0x000a5ed0(enqueue_b)
——签名 F(q, name, cmdid, task)(design §0-F1)。
判别门:追 x0/x3 指针链找当轮正文 needle(嘻嘻 E5 98 BB);命中才全量落盘:
  寄存器/回溯(全帧 module+offset)/x3 与 q 转储/命中链指针;
三必验项:
  V1 0x1c0 形:svc = x0-0x1c0;读 svc+0x1c0 应={堆指针, 序号, 0}(q 自身);
  V2 svc_vtable_off = *(uint64*)svc − slide(记录,供桥活性验);
  V3 svc_invariants = svc+0x08..+0x18 非指针区 16B(记录);
纪律:只读零写;命中后禁用全部断点(防残留 int3);异常全吞;自动继续。
"""
import lldb
import os

ROOT = "/tmp/wxsend3"
OUT = f"{ROOT}/r4"
OFF_ENQ_A = 0xA6060
OFF_ENQ_B = 0xA5ED0
NEEDLE = b"\xe5\x98\xbb"  # 嘻嘻
PTR_CHUNK = 1024
MAX_CHASE = 120

os.makedirs(OUT, exist_ok=True)
_st = {"bps": [], "slide": 0, "done": False, "hits": 0}


def _read(proc, addr, size):
    err = lldb.SBError()
    data = proc.ReadMemory(addr, size, err)
    return data if err.Success() else None


def _hexdump(data, base):
    lines = []
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        hexs = " ".join(f"{b:02x}" for b in chunk)
        asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"{base + i:#x}  {hexs:<48} {asc}")
    return "\n".join(lines)


def install(debugger):
    target = debugger.GetSelectedTarget()
    slide = None
    for m in target.module_iter():
        if m.file.basename == "wechat.dylib":
            slide = m.GetObjectFileHeaderAddress().GetLoadAddress(target)
            break
    if slide is None:
        return
    _st["slide"] = slide
    for off in (OFF_ENQ_A, OFF_ENQ_B):
        bp = target.BreakpointCreateByAddress(slide + off)
        bp.SetScriptCallbackFunction("cap4.on_hit")
        _st["bps"].append(bp)
    with open(f"{OUT}/ARMED", "w") as f:
        f.write(f"slide={slide:#x} bps={[hex(b.id) for b in _st['bps']]}\n")


def _chase(proc, ptrs):
    """从候选指针集追 needle;返回 (命中指针, needle 所在地址, 转储行)。"""
    seen = set()
    queue = list(ptrs)
    logs = []
    while queue and len(seen) < MAX_CHASE:
        p = queue.pop(0)
        if not isinstance(p, int) or p < 0x1000 or p in seen:
            continue
        seen.add(p)
        data = _read(proc, p, PTR_CHUNK)
        if data is None:
            continue
        logs.append(f"ptr {p:#x}: {data[:48].hex()}")
        idx = data.find(NEEDLE)
        if idx >= 0:
            return p, p + idx, logs
        for i in range(0, len(data) - 7, 8):
            v = int.from_bytes(data[i:i + 8], "little")
            if 0x100000000 < v < 0x800000000000:
                queue.append(v)
    return None, None, logs


def on_hit(frame, bp_loc, internal_dict):
    try:
        if _st["done"]:
            return False
        proc = frame.GetThread().GetProcess()
        target = proc.GetTarget()
        slide = _st["slide"]

        def reg(name):
            v = frame.FindRegister(name)
            return v.GetValueAsUnsigned() if v and v.IsValid() else 0

        x0, x1, x2, x3 = reg("x0"), reg("x1"), reg("x2"), reg("x3")
        # 判别门(v2):追指针找「同对象双证据」=filehelper(对端)+ needle(正文)
        # ——hit1 复盘:cmdid=100000 疑为 send 族真值(协程 cmdid≠CGI reqid),硬门误杀;
        # 旧堆残留只含 needle 不含 filehelper+needle 同对象,双证据门更强。
        task_data = _read(proc, x3, 0x400) or b""
        direct = task_data.find(NEEDLE)
        ptrs = [x0, x3]
        for buf in (task_data, _read(proc, x0, 0x200) or b""):
            for i in range(0, len(buf) - 7, 8):
                v = int.from_bytes(buf[i:i + 8], "little")
                if 0x100000000 < v < 0x800000000000:
                    ptrs.append(v)
        hit_ptr, needle_addr, chase_log = _chase(proc, ptrs)

        _st["hits"] += 1
        if direct < 0 and hit_ptr is None:
            if _st["hits"] % 50 == 1:
                with open(f"{OUT}/stray.log", "a") as f:
                    f.write(f"hit#{_st['hits']} x0={x0:#x} x2={x2:#x} 无 needle\n")
            return False  # 杂散(非本轮正文),继续

        # ===== 命中:全量落盘 =====
        n = _st["hits"]
        tag = f"hit{n}"
        with open(f"{OUT}/{tag}.txt", "w") as f:
            f.write(f"slide={slide:#x}\nx0(q)={x0:#x} x1(name)={x1:#x} x2(cmdid)={x2:#x}(={x2}) x3(task)={x3:#x}\n")
            f.write(f"needle@{needle_addr:#x}(via ptr {hit_ptr:#x})\n")
            f.write(f"task+0..0x400:\n{_hexdump(task_data, x3)}\n")
            f.write(f"q region:\n{_hexdump(_read(proc, x0, 0x100) or b'', x0)}\n")
            # V1: 0x1c0 形验证(svc = x0-0x1c0)
            svc = x0 - 0x1C0
            svc_data = _read(proc, svc, 0x1D8 + 0x40) or b""
            f.write(f"\nsvc=x0-0x1c0={svc:#x} vptr={int.from_bytes(svc_data[:8],'little'):#x}\n")
            f.write(f"V1 svc+0x1c0: {svc_data[0x1c0:0x1d8].hex()}\n")
            vptr = int.from_bytes(svc_data[:8], "little")
            f.write(f"V2 svc_vtable_off = vptr-slide = {vptr - slide:#x}\n")
            f.write(f"V3 svc_invariants(+0x08..+0x18) = {svc_data[8:24].hex()}\n")
            f.write(f"chase_log:\n" + "\n".join(chase_log[:20]) + "\n")
            # msgctx 定位:needle 所在对象(命中指针即 msgctx 或含 msgctx)
            if hit_ptr is not None:
                mdata = _read(proc, max(0, hit_ptr - 0x800), 0x4000) or b""
                f.write(f"\nmsgctx dump(needle 载体 {hit_ptr:#x}):\n{_hexdump(mdata, hit_ptr - 0x800)}\n")
            # 回溯:全帧
            f.write("\nBT:\n")
            thread = frame.GetThread()
            for fr in thread:
                pc = fr.GetPCAddress().GetLoadAddress(target)
                mod = fr.GetModule().GetFileSpec().GetFilename() if fr.GetModule() else "?"
                sym = fr.GetSymbol()
                symname = sym.GetName() if sym and sym.IsValid() else ""
                inlide = pc - slide if mod == "wechat.dylib" else -1
                f.write(f"  #{fr.GetFrameID()}: {pc:#x} [{mod}] +{inlide:#x} {symname}\n")
        # 禁用全部断点并写 DONE(kill 前防 int3 残留)
        for bp in _st["bps"]:
            bp.SetEnabled(False)
        _st["done"] = True
        with open(f"{OUT}/DONE", "w") as f:
            f.write(f"{tag}\n")
    except Exception as exc:  # noqa: BLE001
        try:
            with open(f"{OUT}/err.log", "a") as f:
                f.write(f"{exc}\n")
        except OSError:
            pass
    return False  # 永不真正停进程


def __lldb_init_module(debugger, internal_dict):
    """lldb command script import 时自动布防(缺此钩子 ARMED 不落)。"""
    import lldb as _l
    debugger.HandleCommand("process status")
    # attach 后 target 已就绪,直接 install
    install(debugger)
