# -*- coding: utf-8 -*-
"""blscan.py — BL 直调扫描器(固化版;源 = /tmp/blscan.py 2026-10-14,/tmp 不可信判例)

对薄片 __TEXT 全量解码 BL 指令,找「谁直调了目标 VA」。已证结论存档:
0x490fb20 投递器=零 BL 调用者(纯函数指针);0x5e1d050=27743 调用点(通用 helper,
勿当发送专属)。调用链上爬用 attribute.py(其内部调本模块)。

用法:
  python3 blscan.py --callers-of 0x5e1d050 [--callers-of 0x...] [--thin PATH] [--json OUT]
模块内:iter_bl(text) / scan_callers(thin, targets)。
"""
from __future__ import annotations

import argparse
import json
import struct
import sys

DEFAULT_THIN = "/Users/zhengbingjin/Downloads/rea-wechat-decompile/wechat_arm64_thin.dylib"


def load_segments(thin_path=DEFAULT_THIN):
    """→ (data, segs, text_seg)。segs=[(fileoff, filesz, vmaddr, vmsz, name)]。"""
    with open(thin_path, "rb") as fh:
        data = fh.read()
    magic, cputype = struct.unpack_from("<II", data, 0)
    if magic != 0xFEEDFACF or cputype != 0x0100000C:
        raise ValueError(f"not arm64 thin mach-o: {thin_path}")
    ncmds = struct.unpack_from("<I", data, 16)[0]
    off = 32
    segs = []
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x19:
            name = data[off + 8:off + 24].split(b"\0")[0].decode()
            vmaddr, vmsz, fileoff, filesz = struct.unpack_from("<QQQQ", data, off + 24)
            segs.append((fileoff, filesz, vmaddr, vmsz, name))
        off += cmdsize
    text = [s for s in segs if s[4] == "__TEXT"]
    if not text:
        raise ValueError("no __TEXT")
    return data, segs, text[0]


def iter_bl(data, text_seg):
    """yield (site_va, target_va) for every BL in __TEXT(逐指令解码,无先验目标集)。

    BL: op=w>>26==0x25,imm26 有符号,目标=site+imm*4。VA 映射走段表(本薄片
    __TEXT vmaddr==fileoff==0,一般式仍按段表算,不依赖巧合)。
    """
    fileoff, filesz, vmaddr, _, _ = text_seg
    end = min(fileoff + filesz, len(data) - 8)
    for fo in range(fileoff, end, 4):
        w = int.from_bytes(data[fo:fo + 4], "little")
        if (w >> 26) != 0x25:
            continue
        imm = w & 0x3FFFFFF
        if imm & (1 << 25):
            imm -= 1 << 26
        site_va = vmaddr + (fo - fileoff)
        yield site_va, site_va + imm * 4


def scan_callers(thin_path, targets):
    """→ {target_va: [caller_site_va,...]}(单遍全扫)。"""
    data, _, text = load_segments(thin_path)
    res = {t: [] for t in targets}
    for site, tgt in iter_bl(data, text):
        if tgt in res:
            res[tgt].append(site)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--callers-of", action="append", default=[],
                    help="目标 VA(hex,可多次)")
    ap.add_argument("--thin", default=DEFAULT_THIN)
    ap.add_argument("--json", default=None, help="结果 JSON 落盘路径(缺省只打印)")
    ap.add_argument("--print-limit", type=int, default=40)
    ap.add_argument("--all-index", action="store_true",
                    help="全量 BL 目标索引(调参/校准用,输出到 --json)")
    args = ap.parse_args(argv)

    data, _, text = load_segments(args.thin)
    print(f"__TEXT file {text[0]:#x}+{text[1]:#x} (vmaddr={text[2]:#x}, fileoff==vmaddr: {text[2] == text[0]})")

    if args.all_index:
        index = {}
        for site, tgt in iter_bl(data, text):
            index.setdefault(tgt, []).append(site)
        total_bl = sum(len(v) for v in index.values())
        print(f"distinct BL targets: {len(index)}  total BL: {total_bl}")
        if args.json:
            json.dump({hex(k): v for k, v in sorted(index.items())},
                      open(args.json, "w"))
            print(f"saved {args.json}")
        return 0

    if not args.callers_of:
        ap.error("需要 --callers-of 0xVA 或 --all-index")
    targets = [int(t, 16) for t in args.callers_of]
    res = scan_callers(args.thin, targets)
    out = {}
    for t in targets:
        sites = res[t]
        out[hex(t)] = sites
        print(f"BL callers of {t:#x}: {len(sites)}")
        for s in sites[: args.print_limit]:
            print(f"    {s:#x}")
    if args.json:
        json.dump(out, open(args.json, "w"))
        print(f"saved {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
