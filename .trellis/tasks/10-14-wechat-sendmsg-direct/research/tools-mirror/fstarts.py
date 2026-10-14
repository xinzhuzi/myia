# -*- coding: utf-8 -*-
"""fstarts.py — 薄片 dylib LC_FUNCTION_STARTS 反查:VA → 所属函数 (start, end)。

「薄片反查」的正数据源(design Step2.4):薄片符号表已剥光(仅 2 个定义符号),
但 LC_FUNCTION_STARTS 提供 387,126 个函数起点(load() 去重并滤 __TEXT 外后实测,
干跑日志在案;原始解码 387,129 含重复/越界条目),lldb 的 ___lldb_unnamed_symbolNNN
编号即源于此。函数起点一律取运行时断点命中地址再反查(错题集 S5:静态启发式起点=死路),
本模块只做边界包络,不猜起点。

用法:
  python3 fstarts.py --va 0x490fb20 [--thin /path/wechat_arm64_thin.dylib]
  python3 fstarts.py --va 0x490fb20 --va 0x5a2beb0 ...
模块内:load(thin) → containing(va)。
"""
from __future__ import annotations

import argparse
import bisect
import struct
import sys

DEFAULT_THIN = "/Users/zhengbingjin/Downloads/rea-wechat-decompile/wechat_arm64_thin.dylib"


def load(thin_path=DEFAULT_THIN):
    """解析薄片 → (starts 升序列表, text_end)。starts 去重升序。"""
    with open(thin_path, "rb") as fh:
        data = fh.read()
    if data[:4] != b"\xcf\xfa\xed\xfe":
        raise ValueError(f"not arm64 thin mach-o: {thin_path}")
    ncmds = struct.unpack_from("<I", data, 16)[0]
    off = 32
    fstarts = None
    text_end = None
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x26:  # LC_FUNCTION_STARTS(off/size 均为 32 位字段)
            fo, sz = struct.unpack_from("<II", data, off + 8)
            fstarts = (fo, sz)
        elif cmd == 0x19:  # LC_SEGMENT_64
            name = data[off + 8:off + 24].split(b"\0")[0].decode()
            vmaddr, vmsz = struct.unpack_from("<QQ", data, off + 24)
            if name == "__TEXT":
                text_end = vmaddr + vmsz
        off += cmdsize
    if fstarts is None:
        raise ValueError("no LC_FUNCTION_STARTS")
    fo, sz = fstarts
    blob = data[fo:fo + sz]
    starts, cur, i = [], 0, 0
    while i < len(blob):
        shift = 0
        delta = 0
        while True:
            b = blob[i]
            i += 1
            delta |= (b & 0x7F) << shift
            if not (b & 0x80):
                break
            shift += 7
        cur += delta
        starts.append(cur)
    starts = sorted(set(a for a in starts if 0 < a and (text_end is None or a <= text_end)))
    return starts, text_end or (1 << 64)


def containing(starts, va):
    """va → (start, end) 或 None(end=下一函数起点,末函数 end=None)。"""
    i = bisect.bisect_right(starts, va) - 1
    if i < 0:
        return None
    return starts[i], starts[i + 1] if i + 1 < len(starts) else None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--va", action="append", required=True, help="VA(hex,如 0x490fb20,可多次)")
    ap.add_argument("--thin", default=DEFAULT_THIN)
    args = ap.parse_args(argv)
    starts, text_end = load(args.thin)
    print(f"function starts: {len(starts)}  __TEXT end: {text_end:#x}")
    for v in args.va:
        va = int(v, 16) if not v.startswith("0x") else int(v, 16)
        c = containing(starts, va)
        if c is None:
            print(f"{va:#x}: <outside>")
            continue
        s, e = c
        size = (e - s) if e else None
        print(f"{va:#x}: func {s:#x}-{e:#x}" if e else f"{va:#x}: func {s:#x}-<end>")
        if size:
            print(f"        size={size}  offset_in_func={va - s}")


if __name__ == "__main__":
    sys.exit(main())
