# -*- coding: utf-8 -*-
"""refscan3.py — 页级 ADRP 取址扫描器(固化版;源 = /tmp/refscan3.py,/tmp 不可信判例)

ADRP(+后继)页级匹配定位「谁取了此页地址」。错题集 S3 铁律:取址扫描一律页级匹配
(精确匹配会被寄存器折叠骗,已证);页级零命中≠死路(0x46391ac 前科),结果只作
线索不作判据。默认页=10-14 晚原脚本五目标(含 xkey 校准页=已知引用自检用例)。

用法:
  python3 refscan3.py [--page 0xVA ...] [--thin PATH] [--json OUT]
不传 --page = 原五默认页(行为与 /tmp/refscan3.py 等价,校准基线)。
"""
from __future__ import annotations

import argparse
import json
import struct
import sys

DEFAULT_THIN = "/Users/zhengbingjin/Downloads/rea-wechat-decompile/wechat_arm64_thin.dylib"
DEFAULT_TEXT_END = 0x9B34000  # /tmp 版硬编码;--thin 换文件时由段表自动覆盖
# 10-14 晚原脚本默认五页(校准基线;0x88bce87=已知引用 XOR 键表,S3 自检页)
LEGACY_PAGES = {
    "SUBMITTER_pg": 0x490FB20 & ~0xFFF,
    "CALLBACK_pg": 0x46391AC & ~0xFFF,
    "taskstr_pg": 0x89E9510 & ~0xFFF,
    "nsmsg_pg": 0x986E82E & ~0xFFF,
    "xkey_pg": 0x88BCE87 & ~0xFFF,
}


def scan_pages(thin_path, pages):
    """→ {name: [site_va,...]}。pages={name: page_va};ADRP 位域:1 10000 rd。"""
    with open(thin_path, "rb") as fh:
        data = fh.read()
    ncmds = struct.unpack_from("<I", data, 16)[0]
    off = 32
    text_end = DEFAULT_TEXT_END
    text = None
    for _ in range(ncmds):
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x19:
            name = data[off + 8:off + 24].split(b"\0")[0].decode()
            vmaddr, vmsz, fileoff, filesz = struct.unpack_from("<QQQQ", data, off + 24)
            if name == "__TEXT":
                text = (fileoff, filesz, vmaddr)
                text_end = vmaddr + vmsz
        off += cmdsize
    fileoff, _, vmaddr = text
    res = {k: [] for k in pages}
    for fo in range(fileoff, min(text_end, len(data) - 16), 4):
        w = int.from_bytes(data[fo:fo + 4], "little")
        if (w >> 31) != 1 or ((w >> 24) & 0x1F) != 0x10:  # ADRP
            continue
        immlo = (w >> 29) & 3
        immhi = (w >> 5) & 0x7FFFF
        imm = (immhi << 2) | immlo
        if imm & (1 << 20):
            imm -= 1 << 21
        site_va = vmaddr + (fo - fileoff)
        page = (site_va & ~0xFFF) + (imm << 12)
        for name, tp in pages.items():
            if page == tp:
                res[name].append(site_va)
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--page", action="append", default=[],
                    help="页地址 VA(hex);缺省=原五默认页(校准基线)")
    ap.add_argument("--thin", default=DEFAULT_THIN)
    ap.add_argument("--json", default=None)
    ap.add_argument("--print-limit", type=int, default=20)
    args = ap.parse_args(argv)

    if args.page:
        pages = {f"page_{p}": int(p, 16) & ~0xFFF for p in args.page}
    else:
        pages = dict(LEGACY_PAGES)

    res = scan_pages(args.thin, pages)
    for k in pages:
        print(f"{k} ({pages[k]:#x}): {len(res[k])} ADRP sites")
        print("   ", [hex(x) for x in res[k][: args.print_limit]])
    if args.json:
        json.dump(res, open(args.json, "w"))
        print(f"saved {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
