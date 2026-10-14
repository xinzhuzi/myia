# -*- coding: utf-8 -*-
"""test_offline.py — Phase 0 全离线干跑自验(零微信、零发送、零 attach;R2 版=grill 六条落实后)。

覆盖:
  A. cap.py v2.1:vmmap 解析(真样例奇偶)/窗口开关/TTL/线程过滤/全命中(活体枚举路径)/
     跨 4MB 块+重叠区去重/不可读区间/未命中保持开窗/两区间源皆无=关窗禁断点/回调异常安全/
     区间源优先级(活体枚举>vmmap 回退)/仅 aux 命中=weak 不烧窗。
  B. 固化等价:tools/blscan.py、tools/refscan3.py 与 /tmp 版产物(根目录 blscan.json /
     refscan3.json)逐点等价。
  C. attribute.py:假 hit(lr=真 BL 调用点+4+slide)→ 调用者反查 → 上游非空;
     slide 错/函数表边界 → 判不确定退出;BT 帧映射。

用法:python3 test_offline.py  → 干跑日志落 <ROOT>/dryrun/phase0-dryrun.log
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

import blscan  # noqa: E402
import cap  # noqa: E402
import fstarts  # noqa: E402
import refscan3  # noqa: E402

DRYRUN = os.path.join(ROOT, "dryrun")
LOG_PATH = os.path.join(DRYRUN, "phase0-dryrun.log")
_log_fh = None


def log(msg=""):
    print(msg)
    _log_fh.write(msg + "\n")
    _log_fh.flush()


FAILS = []


def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    log(f"[{tag}] {name}" + (f"  {detail}" if detail else ""))
    if not cond:
        FAILS.append(name)


# ---------------------------------------------------------------- 假 lldb 对象

class FakeSBError(cap._FakeSBError):
    pass


class FakeReg:
    def __init__(self, value):
        self.value, self.valid = value, True

    def IsValid(self):
        return self.valid

    def GetValueAsUnsigned(self):
        return self.value


class FakeBreakpoint:
    def __init__(self):
        self.enabled = True

    def SetEnabled(self, v):
        self.enabled = bool(v)


class FakeBpLoc:
    def __init__(self, bp):
        self.bp = bp

    def GetBreakpoint(self):
        return self.bp


class FakeRegionList:
    """假 SBMemoryRegionList(out-param 填充形态,同 /tmp/grill_regioncheck.py 验证过的 API)。"""

    def __init__(self, regions):
        self._regions = regions  # [(base, end, readable, executable)]

    def GetSize(self):
        return len(self._regions)

    def GetMemoryRegionAtIndex(self, i, out):
        if 0 <= i < len(self._regions):
            out._fill(*self._regions[i])
            return True
        return False


class FakeProcess:
    """区间表+探针布置式假内存:ReadMemory 返回零填充并拼接探针片段。

    native_regions=活体枚举区域表(GetMemoryRegions 路径);native_raises=枚举抛错
    (测回退)。缺省 GetMemoryRegions 返回空列表(=launch 停 main 态亲测形态→回退)。
    """

    def __init__(self, regions, placements=(), native_regions=None, native_raises=False):
        self.regions = regions            # [(start, end, name, readable)] ReadMemory 判据
        self.placements = list(placements)  # [(addr, bytes)]
        self.native_regions = native_regions
        self.native_raises = native_raises
        self.read_count = 0
        self.read_bytes = 0

    def GetMemoryRegions(self):
        if self.native_raises:
            raise RuntimeError("fake native enum failure")
        return FakeRegionList(self.native_regions or [])

    def ReadMemory(self, addr, size, err):
        self.read_count += 1
        reg = next((r for r in self.regions if r[0] <= addr and addr + size <= r[1]), None)
        if reg is None or not reg[3]:
            err.SetErrorToGenericError()
            return None
        buf = bytearray(size)
        for paddr, pbytes in self.placements:
            if paddr < addr or paddr + len(pbytes) > addr + size:
                continue
            buf[paddr - addr:paddr - addr + len(pbytes)] = pbytes
        self.read_bytes += size
        return bytes(buf)


class FakeThread:
    def __init__(self, name, proc, idx=17, pc=0x205E1D050, regs=None):
        self.name, self.proc, self.idx, self.pc = name, proc, idx, pc
        self.regs = regs or {}

    def GetName(self):
        return self.name

    def GetIndexID(self):
        return self.idx

    def GetProcess(self):
        return self.proc

    def __str__(self):
        return (f"thread #17: tid = 0x739da7b, {self.pc:#018x} wechat.dylib`___lldb_unnamed_symbol259343, "
                f"name = '{self.name}', stop reason = breakpoint 1.1")


class FakeFrame:
    def __init__(self, thread, regs=None, raise_on=None):
        # regs 显式传入优先,否则继承 thread.regs(hit 帧寄存器挂在线程上)
        self.thread, self.raise_on = thread, raise_on
        self.regs = dict(regs) if regs is not None else dict(thread.regs)

    def GetThread(self):
        return self.thread

    def GetPC(self):
        return self.thread.pc

    def FindRegister(self, r):
        if self.raise_on and r == self.raise_on:
            raise RuntimeError("fake register read failure")
        return FakeReg(self.regs.get(r, 0))


# ---------------------------------------------------------------- A. cap.py

SLIDE = 0x200000000
XI_UTF8 = "嘻嘻".encode("utf-8")
XI_UTF16 = "嘻嘻".encode("utf-16-le")

# 合成 vmmap:R1=12MB 可读(含跨块探针),R2=64KB 可读(无探针),R3=64KB 不可读,
# 外加 guard/metadata 行验证排除逻辑。探针地址一律由基址计算,禁手拼(防掉位)。
R1 = (0x500000000, 0x500000000 + 12 * 1024 * 1024, "MALLOC_SMALL", True)
R2 = (0x600000000, 0x600000000 + 64 * 1024, "MALLOC_TINY", True)
R3 = (0x700000000, 0x700000000 + 64 * 1024, "MALLOC_LARGE", False)
P_EDGE = R1[0] + 0x400000 - 5          # filehelper 恰横跨首个 4MB 块边界
P_OVERLAP = R1[0] + 0x400000 - 10      # filehelper 10B 全落块尾 19B 重叠区(双扫→去重)
P_XI8 = R1[0] + 0x800123               # 嘻嘻 utf-8
P_XI16 = R1[0] + 0x800500              # 嘻嘻 utf-16-le
NATIVE_R = [(R1[0], R1[1], True, False), (R2[0], R2[1], True, False),
            (R3[0], R3[1], True, False)]  # 活体枚举形态区域表(可读非可执行)
SYNTH_VMMAP = f"""
MALLOC_SMALL               {R1[0]:x}-{R1[1]:x}    [12M] rw-/rwx SM=PRV DefaultMallocZone_0x500000000
MALLOC_TINY                {R2[0]:x}-{R2[1]:x}    [64K] rw-/rwx SM=PRV DefaultMallocZone_0x500000000
MALLOC_LARGE               {R3[0]:x}-{R3[1]:x}    [64K] rw-/rwx SM=PRV
MALLOC guard page          1004a8000-100664000    [1776K] ---/--- SM=SHM
MALLOC metadata            1006b0000-1006b4000    [16K] r--/rwx SM=PRV
MALLOC_SMALL (empty)       4e8300000-4e8304000    [16K] rw-/rwx SM=PRV
"""


def fresh_env(tmp, placements):
    """每用例独立的 hits 目录 + vmmap 文件 + 配置复位。"""
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.makedirs(tmp)
    vmmap_path = os.path.join(tmp, "vmmap.txt")
    with open(vmmap_path, "w") as fh:
        fh.write(SYNTH_VMMAP)
    cap.configure(hit_dir=tmp, vmmap_path=vmmap_path)
    cap.WINDOW.enabled = False
    return vmmap_path


def hit_files(tmp):
    return [f for f in os.listdir(tmp) if f.startswith("hit_")]


def weak_files(tmp):
    return [f for f in os.listdir(tmp) if f.startswith("weak_")]


def window_log(tmp):
    p = os.path.join(tmp, "window.log")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def test_cap():
    log("\n===== A. cap.py v2 干跑 =====")

    # A1 真样例奇偶(vmmap.sample.txt=10-14 真快照拷贝)
    sample = open(os.path.join(TOOLS, "samples", "vmmap.sample.txt"), encoding="utf-8",
                  errors="replace").read()
    regions = cap.parse_vmmap_text(sample)
    total_mb = sum(e - s for s, e, _ in regions) / 1048576
    check("A1 vmmap 真样例解析:区间>100 且全部可读、无 guard/metadata",
          len(regions) > 100 and all("guard" not in n and "metadata" not in n for _, _, n in regions),
          f"regions={len(regions)} total={total_mb:.0f}MB")

    # A2 窗口默认关:断点即使使能,零动作零落盘
    tmp = os.path.join(DRYRUN, "test-hits-A2")
    fresh_env(tmp, [])
    bp = FakeBreakpoint()
    proc = FakeProcess([R1])
    frame = FakeFrame(FakeThread("coroutine *999", proc, regs={"lr": 0x11}))
    ret = cap.on_hit(frame, FakeBpLoc(bp), None)
    check("A2 窗口关=零动作(return False、零 ReadMemory、无落盘、断点不动)",
          ret is False and proc.read_count == 0 and not hit_files(tmp)
          and bp.enabled and window_log(tmp) == "")

    # A3 线程名过滤:非协程线程直接放行,不扫堆
    tmp = os.path.join(DRYRUN, "test-hits-A3")
    fresh_env(tmp, [])
    bp = FakeBreakpoint()
    proc = FakeProcess([R1])
    cap.arm()
    ret = cap.on_hit(FakeFrame(FakeThread("com.apple.main-thread", proc)), FakeBpLoc(bp), None)
    wl = window_log(tmp)
    check("A3 线程过滤(非 coroutine/mars::stn)=零扫堆、记 filter、窗保持开、断点保持使能",
          ret is False and proc.read_count == 0 and "filter:" in wl
          and cap.WINDOW.enabled and bp.enabled)

    # A4 全命中(活体枚举路径):primary(嘻嘻)命中=写 hit+关窗+禁断点+自动继续,
    #    aux(filehelper)同帧记录为 aux-hit;区域源=lldb-native
    tmp = os.path.join(DRYRUN, "test-hits-A4")
    fresh_env(tmp, [])
    bp = FakeBreakpoint()
    placements = [
        (P_EDGE, b"filehelper"),   # aux:横跨首个 4MB 块边界(前 5 字节在块1、后 5 在块2)
        (P_XI8, XI_UTF8),          # primary
        (P_XI16, XI_UTF16),        # primary
    ]
    proc = FakeProcess([R1, R2, R3], placements, native_regions=NATIVE_R)
    cap.arm()
    regs = {f"x{i}": R1[0] + 0x800100 + i for i in range(8)}
    regs.update({"sp": 0x17175AA10, "lr": SLIDE + 0x31AB38C})
    ret = cap.on_hit(FakeFrame(FakeThread("coroutine *999", proc, regs=regs)), FakeBpLoc(bp), None)
    files = hit_files(tmp)
    ok = (ret is False and len(files) == 1 and not weak_files(tmp)
          and not cap.WINDOW.enabled and not bp.enabled)
    detail = f"files={files} window.enabled={cap.WINDOW.enabled} bp.enabled={bp.enabled}"
    if ok:
        text = open(os.path.join(tmp, files[0]), encoding="utf-8").read()
        ok = ok and "pc = " in text and f"lr = {SLIDE + 0x31AB38C:#x}" in text
        ok = ok and "regions_source: lldb-native" in text
        ok = ok and f"probe-hit: 嘻嘻/utf8 @ {P_XI8:#x}" in text
        ok = ok and f"probe-hit: 嘻嘻/utf16le @ {P_XI16:#x}" in text
        ok = ok and f"aux-hit: filehelper/utf8 @ {P_EDGE:#x}" in text
        ok = ok and "BT:" in text and "filehelper" in text          # ctx 含探针原文
        ok = ok and "mem[x0] = " in text                            # 寄存器指向内存 160B 已录
        ok = ok and "scanned_bytes: " in text and " failed: 1\n" in text  # R3 不可读恰 1 块
        ok = ok and "HIT ->" in window_log(tmp)
    check("A4 全命中[活体枚举](hit/关窗/禁断点/自继续/分级 aux/统计上下文)", ok, detail)

    # A5 跨块命中:P_EDGE 横跨 4MB 块边界(前块只含前 5 字节,仅后块完整含)→ 恰一次
    #    (注意不能与 P_OVERLAP 同 FakeProcess:P_EDGE/P_OVERLAP 相距 5B<10B 探针长,
    #     假件按序 splice 会互相覆盖制造伪影——非 cap 缺陷)
    tmp = os.path.join(DRYRUN, "test-hits-A5")
    fresh_env(tmp, [])
    proc = FakeProcess([R1], [(P_EDGE, b"filehelper")])
    cap.arm()
    hits, stats = cap.scan_regions(proc, cap.parse_vmmap_text(SYNTH_VMMAP)[:1])
    ok = [h[1] for h in hits] == [P_EDGE]
    check(f"A5a 探针横跨 4MB 块边界仍命中 @{P_EDGE:#x} 恰一次", ok,
          f"hits={[hex(h[1]) for h in hits]} chunks={stats['chunks']}")

    # A5b 重叠区去重:P_OVERLAP 10B 全落块尾 19B 重叠区 → 前后两块各命中一次(生成器层
    #    yield×2),scan_regions 去重后恰 1 条
    proc = FakeProcess([R1], [(P_OVERLAP, b"filehelper")])
    reg1 = cap.parse_vmmap_text(SYNTH_VMMAP)[:1][0]
    gen = cap.scan_region(proc, reg1[0], reg1[1], reg1[2])
    raw = []
    while True:
        try:
            raw.append(next(gen))
        except StopIteration:
            break
    hits2, _ = cap.scan_regions(proc, cap.parse_vmmap_text(SYNTH_VMMAP)[:1])
    check(f"A5b 重叠区@{P_OVERLAP:#x} 原始双命中→去重恰 1 条",
          len(raw) == 2 and all(a == P_OVERLAP for _, a, _ in raw)
          and [h[1] for h in hits2] == [P_OVERLAP],
          f"raw={[hex(a) for _, a, _ in raw]} dedup={[hex(h[1]) for h in hits2]}")

    # A6 未命中:窗保持开、断点保持使能、记 miss、无 hit 文件
    tmp = os.path.join(DRYRUN, "test-hits-A6")
    fresh_env(tmp, [])
    bp = FakeBreakpoint()
    proc = FakeProcess([R1, R2, R3])  # 零探针
    cap.arm()
    ret = cap.on_hit(FakeFrame(FakeThread("mars::stn-3", proc)), FakeBpLoc(bp), None)
    wl = window_log(tmp)
    check("A6 双探皆无=窗口错失(miss 记账、窗开、断点使能、无 hit 文件)",
          ret is False and "miss:" in wl and cap.WINDOW.enabled and bp.enabled
          and not hit_files(tmp))

    # A7 区间表缺失:不确定态=关窗+禁断点+ERROR 记账
    tmp = os.path.join(DRYRUN, "test-hits-A7")
    fresh_env(tmp, [])
    cap.configure(vmmap_path=os.path.join(tmp, "不存在.txt"))
    bp = FakeBreakpoint()
    proc = FakeProcess([R1])
    cap.arm()
    ret = cap.on_hit(FakeFrame(FakeThread("coroutine *1", proc)), FakeBpLoc(bp), None)
    check("A7 vmmap 区间表缺失=关窗+禁断点+ERROR(uncertain-never-retry)",
          ret is False and not cap.WINDOW.enabled and not bp.enabled
          and "ERROR" in window_log(tmp) and proc.read_count == 0)

    # A8 回调异常安全(两注入点):①帧捕获寄存器读取抛 ②堆扫 ReadMemory 抛;
    #    均须:吞异常+关窗+禁断点+callback-error 记账+异常取证件落盘(保帧)
    for tag, frame_or_proc in (("reg", None), ("mem", None)):
        tmp = os.path.join(DRYRUN, f"test-hits-A8-{tag}")
        fresh_env(tmp, [])
        bp = FakeBreakpoint()
        cap.arm()
        if tag == "reg":
            frame = FakeFrame(FakeThread("coroutine *1", FakeProcess([R1]), regs={"x0": 1}),
                              raise_on="x0")
        else:
            class RaisingProc(FakeProcess):
                def ReadMemory(self, addr, size, err):
                    raise RuntimeError("fake ReadMemory crash")

            frame = FakeFrame(FakeThread("coroutine *1", RaisingProc([R1]), regs={"lr": 0x11}))
        ret = cap.on_hit(frame, FakeBpLoc(bp), None)
        err_files = hit_files(tmp)
        ok = (ret is False and not cap.WINDOW.enabled and not bp.enabled
              and "callback-error" in window_log(tmp) and len(err_files) == 1)
        if ok and tag == "mem":  # mem 注入发生在帧捕获之后 → 异常件里必须已含帧文本
            etext = open(os.path.join(tmp, err_files[0]), encoding="utf-8").read()
            ok = "thread: coroutine *1" in etext and "ERROR:" in etext
        check(f"A8-{tag} 回调异常=吞掉+关窗+禁断点+记账" + ("+异常取证件保帧" if tag == "mem" else ""),
              ok, f"files={err_files}")

    # A9 区间源优先级:活体枚举与 vmmap 快照并存 → 用活体(regions_source=lldb-native)
    tmp = os.path.join(DRYRUN, "test-hits-A9")
    fresh_env(tmp, [])                       # vmmap 文件在位,但不应被读
    bp = FakeBreakpoint()
    proc = FakeProcess([R1], [(P_XI8, XI_UTF8)], native_regions=[(R1[0], R1[1], True, False)])
    cap.arm()
    ret = cap.on_hit(FakeFrame(FakeThread("coroutine *1", proc, regs={"lr": 0x11})),
                     FakeBpLoc(bp), None)
    files = hit_files(tmp)
    ok = ret is False and len(files) == 1 and not bp.enabled
    if ok:
        text = open(os.path.join(tmp, files[0]), encoding="utf-8").read()
        ok = ("regions_source: lldb-native" in text and "region=lldb-region" in text)
    check("A9 区间源优先级:活体枚举在→vmmap 快照不读(S10 勘误形态)", ok, f"files={files}")

    # A10 活体枚举失败(异常)→ 回退 vmmap 快照(滞后风险已知)
    tmp = os.path.join(DRYRUN, "test-hits-A10")
    fresh_env(tmp, [])
    bp = FakeBreakpoint()
    proc = FakeProcess([R1], [(P_XI8, XI_UTF8)], native_raises=True)
    cap.arm()
    ret = cap.on_hit(FakeFrame(FakeThread("coroutine *1", proc, regs={"lr": 0x11})),
                     FakeBpLoc(bp), None)
    files = hit_files(tmp)
    ok = ret is False and len(files) == 1
    if ok:
        text = open(os.path.join(tmp, files[0]), encoding="utf-8").read()
        ok = "regions_source: vmmap-snapshot" in text and "probe-hit: 嘻嘻/utf8" in text
    check("A10 活体枚举失败→回退 vmmap 快照(命中仍成立)", ok, f"files={files}")

    # A11 weak:仅 filehelper(堆内陈旧串常态)→ weak 取证件、窗不烧、断点保持使能;
    #     同窗第二次 weak 不重复落盘
    tmp = os.path.join(DRYRUN, "test-hits-A11")
    fresh_env(tmp, [])
    bp = FakeBreakpoint()
    proc = FakeProcess([R1], [(P_EDGE, b"filehelper")], native_regions=[(R1[0], R1[1], True, False)])
    cap.arm()
    frame = FakeFrame(FakeThread("coroutine *1", proc, regs={"lr": 0x11}))
    ret = cap.on_hit(frame, FakeBpLoc(bp), None)
    w1 = weak_files(tmp)
    ok = (ret is False and len(w1) == 1 and not hit_files(tmp)
          and cap.WINDOW.enabled and bp.enabled and "WEAK ->" in window_log(tmp))
    ret2 = cap.on_hit(frame, FakeBpLoc(bp), None)
    ok = ok and ret2 is False and len(weak_files(tmp)) == 1 and cap.WINDOW.enabled and bp.enabled
    check("A11 仅 aux(filehelper)命中=weak 取证件一份、窗不烧、断点保持使能(防 S1 同型烧窗)",
          ok, f"weak={w1} window.enabled={cap.WINDOW.enabled} bp.enabled={bp.enabled}")

    # A12 TTL:arm 超时后首个命中=关窗+禁断点+零扫堆(30s 噪声界落码)
    tmp = os.path.join(DRYRUN, "test-hits-A12")
    fresh_env(tmp, [])
    bp = FakeBreakpoint()
    proc = FakeProcess([R1], [(P_XI8, XI_UTF8)], native_regions=[(R1[0], R1[1], True, False)])
    cap.arm(timeout_s=0.01)
    time.sleep(0.02)
    ret = cap.on_hit(FakeFrame(FakeThread("coroutine *1", proc, regs={"lr": 0x11})),
                     FakeBpLoc(bp), None)
    check("A12 窗口 TTL 过期=关窗+禁断点+零扫堆+记账",
          ret is False and not cap.WINDOW.enabled and not bp.enabled
          and proc.read_count == 0 and "ttl-expired" in window_log(tmp)
          and not hit_files(tmp) and not weak_files(tmp))


# ---------------------------------------------------------------- B. 固化等价

def test_parity():
    log("\n===== B. blscan/refscan3 固化等价(对 /tmp 版既有产物)=====")
    old_bl = json.load(open(os.path.join(ROOT, "blscan.json")))
    t0 = time.time()
    new_bl = blscan.scan_callers(blscan.DEFAULT_THIN, [0x490FB20, 0x5E1D050])
    dt = time.time() - t0
    check("B1 blscan:rpc_stub(0x5e1d050) 调用点集合与 blscan.json 逐点等价",
          new_bl[0x5E1D050] == old_bl["rpc_stub_callers"],
          f"n={len(new_bl[0x5E1D050])} vs 旧={len(old_bl['rpc_stub_callers'])} ({dt:.0f}s)")
    check("B2 blscan:submitter(0x490fb20) 仍零调用点(纯函数指针结论不翻案)",
          new_bl[0x490FB20] == old_bl["submitter_callers"] == [],
          f"n={len(new_bl[0x490FB20])}")

    old_ref = json.load(open(os.path.join(ROOT, "refscan3.json")))
    new_ref = refscan3.scan_pages(refscan3.DEFAULT_THIN, refscan3.LEGACY_PAGES)
    same = all(new_ref[k] == old_ref[k] for k in refscan3.LEGACY_PAGES if k in old_ref)
    have_all = set(new_ref) == set(k for k in old_ref if k in refscan3.LEGACY_PAGES)
    check("B3 refscan3:五默认页 ADRP 站点集合与 refscan3.json 等价",
          same and have_all,
          f"counts={ {k: len(new_ref[k]) for k in new_ref} }")
    check("B4 refscan3:S3 校准页(xkey=已知引用)自检非零",
          len(new_ref.get("xkey_pg", [])) > 0, f"xkey={len(new_ref.get('xkey_pg', []))}")


# ---------------------------------------------------------------- C. attribute.py

def test_attribute():
    log("\n===== C. attribute.py 归因链干跑(假 hit 构造)=====")
    starts, text_end = fstarts.load()
    log(f"薄片 function starts={len(starts)} __TEXT end={text_end:#x}")

    # 选型:真 BL 调用点 s(来自 blscan.json rpc 调用点),满足
    #   ① s 与 s+4 同属函数 F(lr=返回地址必须落在 F 内);
    #   ② F 入口自身有 BL 调用者(上游非空,可演示逐层上爬)。
    old_bl = json.load(open(os.path.join(ROOT, "blscan.json")))
    all_targets = set()
    data, _, text_seg = blscan.load_segments()
    for _site, tgt in blscan.iter_bl(data, text_seg):
        all_targets.add(tgt)
    chosen = None
    for s in old_bl["rpc_stub_callers"]:
        f1, f2 = fstarts.containing(starts, s), fstarts.containing(starts, s + 4)
        if f1 and f2 and f1[0] == f2[0] and f1[0] in all_targets and f1[0] != 0x5E1D050:
            chosen = (s, f1[0], f1[1])
            break
    check("C0 选型:找到演示用真调用点(同帧内返回地址+上游可再爬)",
          chosen is not None)
    if not chosen:
        return
    s, f_start, f_end = chosen
    log(f"  选定 s={s:#x} → F={f_start:#x}-{f_end:#x}")

    tmp = os.path.join(DRYRUN, "test-hits-C")
    os.makedirs(tmp, exist_ok=True)
    lr = s + 4 + SLIDE
    bt_addr1 = f_start + SLIDE
    bt_addr2 = 0x5E1D050 + SLIDE
    fake_hit = os.path.join(tmp, "hit_fake.txt")
    with open(fake_hit, "w", encoding="utf-8") as fh:
        fh.write(f"thread: coroutine *999 tid=17\npc = {SLIDE + 0x5E1D050:#x}\n")
        for i in range(8):
            fh.write(f"x{i} = {0x50800100 + i:#x}\n")
        fh.write(f"sp = {0x17175AA10:#x}\nlr = {lr:#x}\n")
        fh.write("mem[x3] = b'fake'\nBT:\n")
        fh.write(f"thread #17: tid = 0x739da7b, {bt_addr1:#018x} wechat.dylib`___lldb_unnamed_symbol, "
                 f"name = 'coroutine *999', stop reason = breakpoint 1.1 {bt_addr2:#x}\n")
        fh.write("--- heap scan ---\nprobe-hit: 嘻嘻/utf8 @ 0x50800123 region=MALLOC_SMALL\n")

    # C1 正常归因
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, os.path.join(TOOLS, "attribute.py"),
                        "--hit", fake_hit, "--slide", hex(SLIDE),
                        "--outdir", os.path.join(tmp, "attr")],
                       capture_output=True, text=True, env=env)
    log("  attribute stdout:\n    " + r.stdout.strip().replace("\n", "\n    "))
    ok = r.returncode == 0
    attr_json = os.path.join(tmp, "attr", "attr_hit_fake.json")
    if ok:
        out = json.load(open(attr_json, encoding="utf-8"))
        ok = ok and int(out["caller_func"]["start"], 16) == f_start
        ok = ok and int(out["lr"]["va"], 16) == s + 4
        ok = ok and len(out["upstream_call_sites"]) >= 1
        bt_map = {int(b["func_start"], 16) for b in out["bt_frames"]}
        ok = ok and bt_map == {f_start, 0x5E1D050}
        log(f"  caller={out['caller_func']['start']} upstream={len(out['upstream_call_sites'])} "
            f"bt_funcs={ {hex(x) for x in bt_map} }")
    check("C1 假 hit 归因:lr→调用者函数正确+上游 BL 调用点非空+BT 帧映射", ok,
          f"rc={r.returncode} err={r.stderr.strip()[:200]}")

    # C2 slide 错 → 判不确定,退出码 3,绝不猜
    r2 = subprocess.run([sys.executable, os.path.join(TOOLS, "attribute.py"),
                         "--hit", fake_hit, "--slide", hex(0x1000)],
                        capture_output=True, text=True, env=env)
    check("C2 slide 错(VA 落 __TEXT 外)=判不确定退出(rc=3),不产归因",
          r2.returncode == 3 and "uncertain-never-retry" in r2.stderr,
          f"rc={r2.returncode}")

    # C3 无 lr 的残缺 hit → 拒归因
    bad = os.path.join(tmp, "hit_bad.txt")
    open(bad, "w").write("thread: x tid=1\nx0 = 0x1\n")
    r3 = subprocess.run([sys.executable, os.path.join(TOOLS, "attribute.py"),
                         "--hit", bad, "--slide", hex(SLIDE)],
                        capture_output=True, text=True, env=env)
    check("C3 残缺 hit(无 lr)=拒绝归因(rc=2)", r3.returncode == 2)

    # C4 lr−slide 落首函数起点之前(函数表边界,containing=None)→ rc=3 干净退出不裸崩
    edge = os.path.join(tmp, "hit_edge.txt")
    with open(edge, "w") as fh:
        fh.write(f"thread: coroutine *1 tid=2\nlr = {SLIDE + 0x1000:#x}\n")
    r4 = subprocess.run([sys.executable, os.path.join(TOOLS, "attribute.py"),
                         "--hit", edge, "--slide", hex(SLIDE)],
                        capture_output=True, text=True, env=env)
    check("C4 lr−slide 落函数表边界(None)=rc=3 带说明,不裸崩",
          r4.returncode == 3 and "无所属函数" in r4.stderr, f"rc={r4.returncode}")


def main():
    global _log_fh
    os.makedirs(DRYRUN, exist_ok=True)
    _log_fh = open(LOG_PATH, "w", encoding="utf-8")
    log(f"Phase 0 离线干跑 {time.strftime('%Y-%m-%d %H:%M:%S')}  python={sys.version.split()[0]}")
    log(f"TOOLS={TOOLS}\nROOT={ROOT}")
    test_cap()
    test_parity()
    test_attribute()
    log("\n===== 门 1 判据汇总 =====")
    log(f"FAIL 数: {len(FAILS)}" + (f"  {FAILS}" if FAILS else ""))
    log(f"干跑日志: {LOG_PATH}")
    _log_fh.close()
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
