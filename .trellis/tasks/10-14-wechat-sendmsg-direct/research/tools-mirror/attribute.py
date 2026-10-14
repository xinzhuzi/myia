# -*- coding: utf-8 -*-
"""attribute.py — hit 文件归因链:lr 定调用者 → 薄片反查 → blscan 上游。

design Step2.4 正解实现:
  hit 文件里 lr(运行时 slid 地址)→ 减 slide 得薄片 VA → LC_FUNCTION_STARTS
  反查所属函数(lr=最近一次 call 的返回地址,其所属函数=断点目标函数的直接上游)
  → 对该函数入口跑 BL 扫描得上上游调用点 → 每个调用点再反查所属函数 = 上游函数表。
  BT 帧地址附带给映射(补充证据,不作主链)。

纪律:slide 必须显式传(--slide);VA 落 __TEXT 外=slide 错/换包 → 判不确定,报错退出,
绝不猜。产物落 <ROOT>/attribution/。

用法:
  python3 attribute.py --hit <hit文件> --slide 0x200000000 [--thin PATH]
  # slide 取法(lldb):image list -o -f | rg wechat.dylib
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blscan  # noqa: E402
import fstarts  # noqa: E402

_TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_TOOLS)
OUT_DIR = os.path.join(ROOT, "attribution")

_REG_RE = re.compile(r"^(\w+) = (0x[0-9a-f]+|\?)$")
_BT_ADDR_RE = re.compile(r"0x[0-9a-f]{9,16}")


def parse_hit(path):
    """→ (registers, thread_line, bt_text, extra_lines)。兼容 v1(hit3)与 v2(堆扫版)格式。"""
    regs, thread_line, bt_lines, extra = {}, None, [], []
    in_bt = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("thread:"):
                thread_line = line
                in_bt = False
            elif line == "BT:":
                in_bt = True
            elif line.startswith("--- heap scan ---"):
                in_bt = False
            elif in_bt:
                bt_lines.append(line)
            else:
                m = _REG_RE.match(line)
                if m:
                    regs[m.group(1)] = None if m.group(2) == "?" else int(m.group(2), 16)
                else:
                    extra.append(line)
    return regs, thread_line, "\n".join(bt_lines), extra


def bt_frames(bt_text, slide, text_end, starts):
    """BT 文本里的运行时地址 → [{runtime,va,func_start,func_end}];只留落在 __TEXT 的。"""
    out, seen = [], set()
    for tok in _BT_ADDR_RE.findall(bt_text):
        rt = int(tok, 16)
        va = rt - slide
        if not (0 <= va < text_end) or va in seen:
            continue
        seen.add(va)
        f = fstarts.containing(starts, va)
        out.append({"runtime": rt, "va": va, "func_start": f[0], "func_end": f[1]})
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hit", required=True, help="hit 文件路径(cap.py 产物)")
    ap.add_argument("--slide", required=True, help="lldb image list -o 的 slide(hex)")
    ap.add_argument("--thin", default=fstarts.DEFAULT_THIN)
    ap.add_argument("--outdir", default=OUT_DIR)
    ap.add_argument("--upstream-limit", type=int, default=60, help="上游调用点展示上限")
    args = ap.parse_args(argv)

    slide = int(args.slide, 16)
    regs, thread_line, bt_text, extra = parse_hit(args.hit)
    lr = regs.get("lr")
    if lr is None:
        print("ERROR: hit 文件无 lr 寄存器行,无法归因", file=sys.stderr)
        return 2

    starts, text_end = fstarts.load(args.thin)
    lr_va = lr - slide
    if not (0 <= lr_va < text_end):
        print(f"ERROR: lr-slide={lr_va:#x} 落 __TEXT[0,{text_end:#x}) 外 —— slide 错或已换包,"
              f"判不确定,停(uncertain-never-retry)。lr={lr:#x} slide={slide:#x}", file=sys.stderr)
        return 3
    caller = fstarts.containing(starts, lr_va)
    if caller is None:
        print(f"ERROR: lr-slide={lr_va:#x} 在 __TEXT 内但无所属函数(首函数起点 {starts[0]:#x} 之前/函数表边界)——"
              f"判不确定,停(uncertain-never-retry)。lr={lr:#x} slide={slide:#x}", file=sys.stderr)
        return 3
    c_start, c_end = caller
    print(f"[hit] {args.hit}")
    print(f"[lr] runtime={lr:#x} slide={slide:#x} va={lr_va:#x}")
    print(f"[caller] func {c_start:#x}-{(c_end or 0):#x} size={(c_end - c_start) if c_end else '?'} "
          f"lr_offset_in_func={lr_va - c_start}")

    up_sites = blscan.scan_callers(args.thin, [c_start])[c_start]
    print(f"[upstream] BL callers of caller entry {c_start:#x}: {len(up_sites)}")

    up_funcs = {}
    for s in up_sites:
        f = fstarts.containing(starts, s)
        up_funcs.setdefault(f[0], {"start": f[0], "end": f[1], "call_sites": []})["call_sites"].append(s)

    bt = bt_frames(bt_text, slide, text_end, starts)
    bt_out = bt

    os.makedirs(args.outdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.hit))[0]
    result = {
        "hit_file": os.path.abspath(args.hit),
        "slide": slide,
        "thread": thread_line,
        "registers": {k: (v if v is None else hex(v)) for k, v in regs.items()},
        "lr": {"runtime": hex(lr), "va": hex(lr_va)},
        "caller_func": {"start": hex(c_start), "end": hex(c_end) if c_end else None,
                        "size": (c_end - c_start) if c_end else None,
                        "lr_offset": lr_va - c_start},
        "upstream_call_sites": [hex(s) for s in up_sites],
        "upstream_funcs": [
            {"start": hex(d["start"]), "end": hex(d["end"]) if d["end"] else None,
             "call_sites": [hex(s) for s in d["call_sites"]]}
            for d in sorted(up_funcs.values(), key=lambda d: d["start"])
        ],
        "bt_frames": [{"runtime": hex(b["runtime"]), "va": hex(b["va"]),
                       "func_start": hex(b["func_start"]),
                       "func_end": hex(b["func_end"]) if b["func_end"] else None}
                      for b in bt_out],
    }
    jpath = os.path.join(args.outdir, f"attr_{base}.json")
    with open(jpath, "w", encoding="utf-8") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=1)

    tpath = os.path.join(args.outdir, f"attr_{base}.txt")
    with open(tpath, "w", encoding="utf-8") as fh:
        fh.write(f"hit: {args.hit}\nslide: {slide:#x}\n{thread_line}\n")
        fh.write(f"lr: runtime {lr:#x} -> va {lr_va:#x}\n")
        fh.write(f"caller: {c_start:#x}-{c_end:#x}\n")
        fh.write(f"upstream BL callers of {c_start:#x}: {len(up_sites)}\n")
        for d in sorted(up_funcs.values(), key=lambda d: d["start"])[: args.upstream_limit]:
            fh.write(f"  up-func {d['start']:#x}-{d['end']:#x} sites={len(d['call_sites'])}\n")
        fh.write(f"bt frames mapped: {len(bt_out)}\n")
        for b in bt_out:
            fh.write(f"  bt {b['runtime']:#x} -> {b['va']:#x} in func {b['func_start']:#x}\n")
        fh.write(f"next: 对 up-func 入口继续 attribute(需其命中帧)或 DecompileTargets 反编译 {c_start:#x}\n")
    print(f"[out] {jpath}\n[out] {tpath}")
    if bt_out:
        for b in bt_out[:10]:
            print(f"[bt] {b['runtime']:#x} -> va {b['va']:#x} func {b['func_start']:#x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
