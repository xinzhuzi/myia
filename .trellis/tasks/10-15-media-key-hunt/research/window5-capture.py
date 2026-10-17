"""单次授权读窗 v4(第三窗:2026-10-16 凌晨授权)。
v2 教训修正:*DAT 先解引用再走偏移;v3 教训修正:stdout 先行+输出目录兜底;
PID 动态取(微信已重启换实例)。零断点零 continue,attach→锚点→纯读→detach。"""
import json
import signal
import subprocess
import time
from pathlib import Path

import lldb

ANCHOR_RVA = 0x433C5F0
ANCHOR_MAGIC = bytes.fromhex('fc6fbca9f65701a9')
CACHE_KEY_RVA = 0xA51EEC0
SVC_DAT_RVA = 0xA45DF38      # 指针变量:*DAT = 服务对象(vtable ≈ slide+0x9e92400)
SVC_SP_OFF = 0x68            # 对象+0x68 shared_ptr → key 对象
KEYOBJ_MASKED_OFF = 0x228    # key 对象 +0x228 掩码串 std::string(32B)
KEYOBJ_REGISTRY_OFF = 0xE0
DEFAULT_KEY_RVA = 0xA49C658


def _read(process, addr, n):
    err = lldb.SBError()
    data = process.ReadMemory(addr, n, err)
    return bytes(data) if err.Success() and data is not None else None


def _module_base(target):
    for m in target.module_iter():
        spec = m.GetFileSpec()
        if spec is not None and spec.GetFilename() == 'wechat.dylib':
            return m.GetObjectFileHeaderAddress().GetLoadAddress(target)
    return None


def _dump_string_slots(process, addr, tag, out):
    hdr = _read(process, addr, 24)
    if hdr is None:
        out[tag] = {'addr': hex(addr), 'hdr': None}
        return
    entry = {'addr': hex(addr), 'hdr': hdr.hex()}
    for i, name in enumerate(('w0', 'w1', 'w2')):
        v = int.from_bytes(hdr[i * 8:(i + 1) * 8], 'little')
        entry[name] = hex(v)
        if 0x100000000 <= v < 0x800000000000:
            blob = _read(process, v, 64)
            if blob is not None:
                entry[name + '_deref64'] = blob.hex()
    out[tag] = entry


def main():
    pid = int(subprocess.run(['pgrep', '-x', 'WeChat'], capture_output=True, text=True).stdout.split()[0])
    result = {'pid': pid, 'outcome': 'error', 'anchor_ok': False}
    out = {}
    prev = {s: signal.signal(s, signal.SIG_IGN) for s in (signal.SIGTERM, signal.SIGINT)}
    dbg = lldb.SBDebugger.Create()
    target = None
    process = None
    t0 = time.monotonic()
    try:
        dbg.SetAsync(True)
        target = dbg.CreateTarget('/Applications/WeChat.app/Contents/MacOS/WeChat')
        listener = lldb.SBListener('media-window-4')
        err = lldb.SBError()
        process = target.AttachToProcessWithID(listener, pid, err)
        if not err.Success() or not process.IsValid():
            result['outcome'] = 'attach_failed'
        else:
            base = None
            for _ in range(3):
                base = _module_base(target)
                if base:
                    break
                ev = lldb.SBEvent()
                listener.WaitForEvent(1, ev)
            if not base:
                result['outcome'] = 'module_missing'
            else:
                result['slide'] = hex(base)
                if _read(process, base + ANCHOR_RVA, 8) != ANCHOR_MAGIC:
                    result['outcome'] = 'anchor_mismatch'
                else:
                    result['anchor_ok'] = True
                    _dump_string_slots(process, base + CACHE_KEY_RVA, 'cache_key', out)
                    dat = _read(process, base + SVC_DAT_RVA, 8)
                    if dat is not None:
                        out['svc_dat_raw'] = dat.hex()
                        svc = int.from_bytes(dat, 'little')
                        if 0x100000000 <= svc < 0x800000000000:
                            vt = _read(process, svc, 8)
                            out['svc_vtable'] = vt.hex() if vt else None
                            out['svc_obj_head'] = (_read(process, svc, 0x100) or b'').hex()
                            sp = _read(process, svc + SVC_SP_OFF, 16)
                            if sp is not None:
                                out['svc_sp_raw'] = sp.hex()
                                keyobj = int.from_bytes(sp[:8], 'little')
                                if 0x100000000 <= keyobj < 0x800000000000:
                                    _dump_string_slots(process, keyobj + KEYOBJ_MASKED_OFF, 'keyobj_masked', out)
                                    _dump_string_slots(process, keyobj + KEYOBJ_REGISTRY_OFF, 'keyobj_registry', out)
                                    out['keyobj_100_300'] = (_read(process, keyobj + 0x100, 0x200) or b'').hex()
                    _dump_string_slots(process, base + DEFAULT_KEY_RVA, 'default_key', out)
                    result['outcome'] = 'read_done'
    except Exception as exc:  # noqa: BLE001
        result['outcome'] = 'error'
        result['error'] = f'{type(exc).__name__}: {exc}'
    finally:
        try:
            if process is not None and process.IsValid():
                if process.GetState() not in (lldb.eStateDetached, lldb.eStateExited):
                    release = process.Detach(False)
                    result['detached'] = bool(release.Success())
                else:
                    result['detached'] = process.GetState() == lldb.eStateDetached
        except Exception as exc:  # noqa: BLE001
            result['detach_error'] = str(exc)
        for s, h in prev.items():
            signal.signal(s, signal.SIG_DFL if h is None else h)
        result['elapsed_seconds'] = round(time.monotonic() - t0, 3)
        print('WINDOW4_RESULT', json.dumps({'result': result, 'reads': out}), flush=True)
        try:
            d = Path('/tmp/wx-media-window-5')
            d.mkdir(parents=True, exist_ok=True)
            d.chmod(0o700)
            (d / 'globals.json').write_text(json.dumps({'result': result, 'reads': out}, indent=1))
            (d / 'globals.json').chmod(0o600)
        except OSError:
            print('WINDOW4_PERSIST_FAILED stdout above is authoritative', flush=True)


main()
