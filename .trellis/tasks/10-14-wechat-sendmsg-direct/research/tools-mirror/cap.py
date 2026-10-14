# -*- coding: utf-8 -*-
"""cap.py v2.1 — LLDB 断点捕获枪(堆扫升级版,Phase 0 产物;v2.1=grill R2 六条落实)

相对 v2(grill R2 拷问后修订):
  1. 堆扫区间源改为 **LLDB 活体枚举优先**:本机 lldb-1703 有零参 SBProcess.GetMemoryRegions()
     (grill 轮 attach 态亲证:39/60 可读数据区可枚举可读;访问器=GetRegionBase/GetRegionEnd/
     IsReadable/IsExecutable)。vmmap 快照文本降级为回退源(快照滞后=hit 时新增堆区漏扫)。
     注:launch 停 main 态枚举返回空(亲测 0/0)——空列表一律按「不可用」回退,不当「无堆区」。
     S10 勘误在案:ax-gate-exp 原文记的是「无 GetNumMemoryRegions」(旧 API),非「无区域枚举」。
  2. 探针分级(防烧窗):HIT_PROBES=内容探「嘻嘻」=唯一烧窗判据;AUX_PROBES=目标探
     「filehelper」只记录不烧窗(堆内陈旧串常在,OR 判据=S1 同型误标,grill R2-high)。
     仅 aux 命中 → weak 取证件(每窗一份)落盘,窗保持开、断点保持使能,继续等 primary。
  3. 窗口 TTL:arm(timeout_s=30) 默认 30s 噪声界;过期后首个命中=关窗+禁断点(防全堆扫
     反复冻结微信)。
  4. 扫描去重:块尾重叠区(探针级回退)同 label 同地址只计一次。
  5. 帧先进缓冲,v2 已有:异常路径保帧取证。

升级点(相对上级目录 cap.py=并行会话遗产,原样不动):堆扫(ReadMemory 分块 4MB+探针级
重叠防跨块漏检+双探针 filehelper/嘻嘻)/线程名过滤/窗口使能开关/自禁用自继续。
禁用 lldb `memory find` 命令形态(design Step 前置-3)。

离线自验:tools/test_offline.py 用假 lldb 对象干跑全部路径(假 hit 构造),零微信零发送。
真机冒烟(not-run 声明,Phase 1 步①升格):attach→禁用态布防→立即 detach,on_hit 回调
全路径在真 attach 态从未执行,首次实战前必须先冒烟。

产物落盘(红线):一律 <ROOT>/hits/ 下;ROOT=本文件上级目录(勘察目录)。/tmp 不可信。
"""

from __future__ import annotations

import io
import os
import re
import time

try:  # 真实环境=lldb 内 import;离线干跑=注入假对象(test_offline.py)
    import lldb  # type: ignore
except ImportError:  # pragma: no cover - 离线干跑路径
    lldb = None  # type: ignore

# ---------------------------------------------------------------- 配置(驱动侧可 cap.configure(...) 覆写)

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_TOOLS_DIR)
HIT_DIR = os.path.join(_ROOT, "hits")                 # hit/weak/窗口日志落此
VMMAP_PATH = os.path.join(_ROOT, "hits", "vmmap.txt")  # 原生枚举不可用时的回退区间表

CHUNK_BYTES = 4 * 1024 * 1024                         # ReadMemory 分块(design: 每块 4MB)
CONTEXT_BYTES = 128                                   # 命中前后上下文(design: 前后 128B)
MAX_MISS_LOG = 50                                     # 窗口内未命中/被滤命中记条上限(防日志无界)
WINDOW_TTL_S = 30.0                                   # 窗口噪声界(design「30s 窗内任务个位数」)

# 探针分级(grill R2 裁:filehelper=常驻联系人,堆内可有陈旧串,OR 判据会烧窗——S1 同型):
#   HIT_PROBES = 内容探「嘻嘻」=唯一烧窗判据(运行时新落堆的明文);
#   AUX_PROBES = 目标探「filehelper」只记录不烧窗(weak 取证),窗保持开等真发送。
# utf-16-le 变体:NSString 堆副本可能 utf-16,只增不漏。
HIT_PROBES = (
    ("嘻嘻/utf8", "嘻嘻".encode("utf-8")),
    ("嘻嘻/utf16le", "嘻嘻".encode("utf-16-le")),
)
AUX_PROBES = (
    ("filehelper/utf8", b"filehelper"),
    ("filehelper/utf16le", "filehelper".encode("utf-16-le")),
)
DEFAULT_PROBES = HIT_PROBES + AUX_PROBES              # scan_regions 显式传 probes 时的全量表
# design Step2.1:仅 coroutine */mars::stn 前缀线程做堆扫('coroutine' 前缀即覆盖 'coroutine *NNN')
THREAD_PREFIXES = ("coroutine", "mars::stn")

PROBES: tuple = DEFAULT_PROBES


def configure(hit_dir=None, vmmap_path=None, probes=None, thread_prefixes=None,
              chunk_bytes=None, context_bytes=None, max_miss_log=None,
              hit_probes=None, aux_probes=None, window_ttl_s=None):
    """驱动/测试覆写配置;None=不改。"""
    global HIT_DIR, VMMAP_PATH, PROBES, THREAD_PREFIXES, HIT_PROBES, AUX_PROBES
    global CHUNK_BYTES, CONTEXT_BYTES, MAX_MISS_LOG, WINDOW_TTL_S, _REGION_CACHE
    if hit_dir is not None:
        HIT_DIR = hit_dir
    if vmmap_path is not None:
        VMMAP_PATH = vmmap_path
        _REGION_CACHE = None
    if probes is not None:
        PROBES = tuple(probes)
    if hit_probes is not None:
        HIT_PROBES = tuple(hit_probes)
    if aux_probes is not None:
        AUX_PROBES = tuple(aux_probes)
    if thread_prefixes is not None:
        THREAD_PREFIXES = tuple(thread_prefixes)
    if chunk_bytes is not None:
        CHUNK_BYTES = int(chunk_bytes)
    if context_bytes is not None:
        CONTEXT_BYTES = int(context_bytes)
    if max_miss_log is not None:
        MAX_MISS_LOG = int(max_miss_log)
    if window_ttl_s is not None:
        WINDOW_TTL_S = float(window_ttl_s)


# ---------------------------------------------------------------- 窗口开关(+TTL)

class _Window:
    """窗口使能开关。默认关。开=允许回调做捕获+堆扫;关=回调零动作直接放行。

    TTL(design「30s 噪声界」落码):arm 时定 deadline;过期后首个命中自关窗+禁断点,
    防协程线程反复触发 241MB 级全堆扫冻结微信。
    """

    def __init__(self):
        self.enabled = False
        self.armed_at = None
        self.expires_at = None
        self.closed_at = None
        self.close_reason = None
        self.weak_written = False

    def arm(self, reason="driver", timeout_s=None):
        self.enabled = True
        self.armed_at = time.time()
        self.expires_at = self.armed_at + (timeout_s if timeout_s is not None else WINDOW_TTL_S)
        self.closed_at = None
        self.close_reason = None
        self.weak_written = False

    def close(self, reason):
        if self.enabled:
            self.enabled = False
            self.closed_at = time.time()
            self.close_reason = reason

    def expired(self):
        return self.enabled and self.expires_at is not None and time.time() > self.expires_at


WINDOW = _Window()


def arm(reason="driver", timeout_s=None):
    """开窗(设计流程:主人说「发」→ 3s 内驱动侧调用;timeout_s 缺省=WINDOW_TTL_S)。"""
    WINDOW.arm(reason, timeout_s)


def disarm(reason="driver"):
    """手动关窗。"""
    WINDOW.close(reason)


# ---------------------------------------------------------------- SBError/RegionInfo 间接层(离线可注入)

class _FakeSBError:
    def __init__(self):
        self._ok = True
        self._msg = ""

    def SetErrorToGenericError(self, msg="fake error"):
        self._ok = False
        self._msg = msg

    def Success(self):
        return self._ok

    def GetCString(self):
        return self._msg

    def fail(self, msg="read failed"):
        self._ok = False
        self._msg = msg


class _FakeRegionInfo:
    """离线假 SBMemoryRegionInfo(out-param 形态:构造零参,由 list 填充)。"""

    def __init__(self):
        self._base = self._end = 0
        self._readable = self._executable = False

    def _fill(self, base, end, readable, executable):
        self._base, self._end = base, end
        self._readable, self._executable = readable, executable

    def IsReadable(self):
        return self._readable

    def IsExecutable(self):
        return self._executable

    def GetRegionBase(self):
        return self._base

    def GetRegionEnd(self):
        return self._end


def _new_error():
    if lldb is not None:
        return lldb.SBError()
    return _FakeSBError()


# ---------------------------------------------------------------- 区间表:活体枚举优先,vmmap 快照回退

def regions_from_process(proc):
    """LLDB 活体区域枚举(S10 勘误后首选源)。→ [(start, end, name)] 或 None。

    零参 GetMemoryRegions()(grill 轮 attach 态亲证可用);过滤=可读且非可执行
    (数据区,与 grill 验证形态一致)。异常/空列表/访问器不齐 → None(回退 vmmap,
    空≠无堆区:launch 停 main 态亲测返回空)。
    """
    try:
        lst = proc.GetMemoryRegions()
        if lst is None:
            return None
        cls = getattr(lldb, "SBMemoryRegionInfo", None) if lldb is not None else _FakeRegionInfo
        if cls is None:
            return None
        out = []
        for i in range(lst.GetSize()):
            r = cls()
            if not lst.GetMemoryRegionAtIndex(i, r):
                continue
            if not (r.IsReadable() and not r.IsExecutable()):
                continue
            base, end = r.GetRegionBase(), r.GetRegionEnd()
            if end > base:
                out.append((base, end, "lldb-region"))
        return out or None
    except Exception:
        return None


_RANGE_RE = re.compile(r"^([0-9a-fA-F]+)-([0-9a-fA-F]+)$")
_PERM_RE = re.compile(r"^([r-][w-][x-])/([r-][w-][x-])$")
_HEAP_KINDS = ("MALLOC", "MALLOC_TINY", "MALLOC_SMALL", "MALLOC_LARGE",
               "MALLOC_MEDIUM", "MALLOC_NANO", "MALLOC_RECYCL")


def parse_vmmap_text(text):
    """解析 vmmap 快照文本 → [(start, end, name)](回退源)。

    只收堆区(kind 前缀如上,排除 metadata/guard page),且当前权限可读(r 开头)。
    输入示例行:
      MALLOC_SMALL (empty)  4e8300000-4e8304000  [ 16K  16K  16K  0K] rw-/rwx SM=PRV  ...
      MALLOC guard page     1004a8000-100664000  [ ... ] ---/--- SM=SHM        ← 排除
    """
    regions = []
    for line in text.splitlines():
        tokens = line.split()
        if not tokens or not tokens[0].startswith("MALLOC"):
            continue
        idx = next((i for i, t in enumerate(tokens) if _RANGE_RE.match(t)), None)
        if idx is None:
            continue
        name = " ".join(tokens[:idx])
        first = name.split(" ")[0]
        if first not in _HEAP_KINDS or "metadata" in name or "guard" in name:
            continue
        m = _RANGE_RE.match(tokens[idx])
        start, end = int(m.group(1), 16), int(m.group(2), 16)
        if end <= start:
            continue
        cur = None
        for t in tokens[idx + 1:]:
            pm = _PERM_RE.match(t)
            if pm:
                cur = pm.group(1)
                break
        if cur is None or "r" not in cur:
            continue
        regions.append((start, end, name))
    return regions


_REGION_CACHE = None
_REGION_CACHE_PATH = None


def load_regions(path=None):
    """读 vmmap 快照文件 → 区间表(回退源,带缓存)。文件缺失/无堆区 → None。"""
    global _REGION_CACHE, _REGION_CACHE_PATH
    path = path or VMMAP_PATH
    if _REGION_CACHE is not None and path == _REGION_CACHE_PATH:
        return _REGION_CACHE
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            regions = parse_vmmap_text(fh.read())
    except OSError:
        return None
    _REGION_CACHE, _REGION_CACHE_PATH = regions, path
    return regions


# ---------------------------------------------------------------- 堆扫(纯逻辑,proc 注入)

def scan_region(proc, start, end, name, probes=None, chunk_bytes=None, context_bytes=None):
    """单区间分块扫。yield (label, addr, context_bytes);统计经 StopIteration.value 返回。

    跨块防护:下一块起点回退 max(探针长)-1 字节,探针横跨 4MB 边界不漏
    (重叠区双命中由 scan_regions 去重)。ReadMemory 失败的块跳过计数,不让整轮挂掉。
    """
    probes = probes or PROBES
    chunk = chunk_bytes or CHUNK_BYTES
    ctx = context_bytes if context_bytes is not None else CONTEXT_BYTES
    max_probe = max(len(p) for _, p in probes)
    overlap = max_probe - 1
    pos = start
    stats = {"chunks": 0, "chunks_failed": 0, "bytes": 0}
    while pos < end:
        size = min(chunk, end - pos)
        stats["chunks"] += 1
        err = _new_error()
        data = proc.ReadMemory(pos, size, err)
        if not (err.Success() and data):
            stats["chunks_failed"] += 1
            pos += size
            continue
        stats["bytes"] += len(data)
        for label, pat in probes:
            i = data.find(pat)
            while i != -1:
                addr = pos + i
                cs = max(start, addr - ctx)
                ce = min(end, addr + ctx + len(pat))
                cerr = _new_error()
                cdata = proc.ReadMemory(cs, ce - cs, cerr)
                context = cdata if (cerr.Success() and cdata) else b""
                yield label, addr, context
                i = data.find(pat, i + 1)
        pos += size - (overlap if pos + size < end else 0)
    return stats


def scan_regions(proc, regions, probes=None, chunk_bytes=None, context_bytes=None):
    """全区间扫。→ (hits, stats)。hits=[(label, addr, context, region_name)] 去重(同 label 同 addr 一次)。"""
    probes = probes or PROBES
    hits, seen = [], set()
    stats = {"chunks": 0, "chunks_failed": 0, "bytes": 0, "regions": len(regions)}
    for start, end, name in regions:
        gen = scan_region(proc, start, end, name, probes, chunk_bytes, context_bytes)
        try:
            while True:
                label, addr, context = next(gen)
                key = (label, addr)
                if key in seen:  # 块尾重叠区双扫去重
                    continue
                seen.add(key)
                hits.append((label, addr, context, name))
        except StopIteration as stop:
            st = stop.value
            if st:
                for k in ("chunks", "chunks_failed", "bytes"):
                    stats[k] += st[k]
    return hits, stats


# ---------------------------------------------------------------- 回调

def _thread_ok(name):
    return any(name.startswith(p) for p in THREAD_PREFIXES)


def _log(path, text):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(f"[{time.strftime('%H:%M:%S')}] {text}\n")
    except OSError:
        pass  # 日志失败不致命,主链路继续


def _miss_count():
    path = os.path.join(HIT_DIR, "window.log")
    try:
        with open(path, encoding="utf-8") as fh:
            return sum(1 for ln in fh if "miss:" in ln or "filter:" in ln)
    except OSError:
        return 0


def _capture_frame(frame, out):
    """v1 cap.py 原样能力:x0-x7/sp/lr/pc + mem[x0..x3] 160B + BT + mem[x4/x5]。"""
    thread = frame.GetThread()
    proc = thread.GetProcess()
    out.write(f"thread: {thread.GetName()} tid={thread.GetIndexID()}\n")
    pc = frame.GetPC()
    out.write(f"pc = {pc:#x}\n")
    regs = {}
    for r in ("x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "sp", "lr"):
        v = frame.FindRegister(r)
        if v and v.IsValid():
            regs[r] = v.GetValueAsUnsigned()
            out.write(f"{r} = {regs[r]:#x}\n")
        else:
            out.write(f"{r} = ?\n")
    for r in ("x0", "x1", "x2", "x3"):
        addr = regs.get(r, 0)
        if addr > 0x1000:
            err = _new_error()
            data = proc.ReadMemory(addr, 160, err)
            if err.Success() and data:
                printable = bytes(b for b in data if 32 <= b < 127 or b >= 0x80)
                out.write(f"mem[{r}] = {printable[:120]!r}\n")
    out.write("BT:\n")
    out.write(str(thread))
    out.write("\nMEM-X4-X5:\n")
    for r in ("x4", "x5"):
        addr = regs.get(r, 0)
        if addr > 0x10000:
            err = _new_error()
            data = proc.ReadMemory(addr, 200, err)
            if err.Success() and data:
                printable = bytes(b for b in data if 32 <= b < 127 or b >= 0x80)
                out.write(f"mem[{r}] = {printable!r}\n")
    return regs


def _disable_bp(bp_loc):
    bp = bp_loc.GetBreakpoint()
    bp.SetEnabled(False)


def _write_hit(frame_buf, primary_hits, aux_hits, stats, elapsed_ms, regions_source,
               error=None):
    """primary 命中(或异常)取证件。error≠None=异常路径(保帧)。"""
    os.makedirs(HIT_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join(HIT_DIR, f"hit_{ts}_{int(time.time() * 1000) % 1000:03d}.txt")
    with open(path, "w", encoding="utf-8") as out:
        out.write(frame_buf)
        out.write("--- heap scan ---\n")
        if error is not None:
            out.write(f"ERROR: {error!r}\n")
        else:
            out.write(f"regions_source: {regions_source}\n")
            out.write(f"vmmap_regions: {stats['regions']}\n")
            out.write(f"scanned_bytes: {stats['bytes']}\n")
            out.write(f"chunks: {stats['chunks']} failed: {stats['chunks_failed']}\n")
            out.write(f"scan_elapsed_ms: {elapsed_ms:.0f}\n")
            for label, addr, context, name in primary_hits:
                out.write(f"probe-hit: {label} @ {addr:#x} region={name}\n")
                out.write(f"ctx: {context!r}\n")
            for label, addr, context, name in aux_hits:
                out.write(f"aux-hit: {label} @ {addr:#x} region={name}\n")
                out.write(f"ctx: {context!r}\n")
    _log(os.path.join(HIT_DIR, "window.log"), f"HIT -> {path}" + (" (ERROR)" if error else ""))
    return path


def _write_weak(frame_buf, aux_hits, stats, elapsed_ms, regions_source):
    """仅 aux(目标探)命中=陈旧串可能:取证一份(每窗一份),窗不烧。→ path 或 None(已写过)。"""
    if WINDOW.weak_written:
        return None
    WINDOW.weak_written = True
    os.makedirs(HIT_DIR, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    path = os.path.join(HIT_DIR, f"weak_{ts}_{int(time.time() * 1000) % 1000:03d}.txt")
    with open(path, "w", encoding="utf-8") as out:
        out.write(frame_buf)
        out.write("--- heap scan (WEAK) ---\n")
        out.write("WEAK: 仅目标探(filehelper)命中,无内容探(嘻嘻)——陈旧串可能,窗不烧,继续等真发送\n")
        out.write(f"regions_source: {regions_source}\n")
        out.write(f"scanned_bytes: {stats['bytes']}\n")
        out.write(f"chunks: {stats['chunks']} failed: {stats['chunks_failed']}\n")
        for label, addr, context, name in aux_hits:
            out.write(f"aux-hit: {label} @ {addr:#x} region={name}\n")
            out.write(f"ctx: {context!r}\n")
    _log(os.path.join(HIT_DIR, "window.log"), f"WEAK -> {path}(窗保持开)")
    return path


def on_hit(frame, bp_loc, internal_dict):
    """断点回调。return False=自动继续不停进程(v1 纪律)。

    顺序:窗口开关 → TTL 检查 → 线程名过滤 → 帧捕获(先进缓冲,异常也保帧)
    → 区间源(活体枚举优先,vmmap 回退)→ 堆扫 → 分级判据:
      primary(嘻嘻)命中  = 写 hit + 关窗 + 禁断点(真发送窗口到手);
      仅 aux(filehelper) = weak 取证件(每窗一份),窗保持开、断点保持使能;
      双探皆无            = miss 记账,窗保持开(design Step2.2:重开窗口再来,勿换弱先验)。
    TTL 过期 / 异常 / 两区间源皆无:关窗+禁断点(不确定态绝不留枪,uncertain-never-retry)。
    """
    buf = io.StringIO()
    try:
        if not WINDOW.enabled:
            return False
        if WINDOW.expired():
            WINDOW.close("ttl-expired")
            _disable_bp(bp_loc)
            _log(os.path.join(HIT_DIR, "window.log"),
                 "ttl-expired: 窗超时自关(30s 噪声界),bp 已禁;重开须重新 arm+enable")
            return False
        thread = frame.GetThread()
        name = thread.GetName() or ""
        if not _thread_ok(name):
            if _miss_count() < MAX_MISS_LOG:
                _log(os.path.join(HIT_DIR, "window.log"), f"filter: thread={name!r}")
            return False

        _capture_frame(frame, buf)

        proc = thread.GetProcess()
        regions = regions_from_process(proc)
        regions_source = "lldb-native"
        if not regions:
            regions = load_regions()
            regions_source = "vmmap-snapshot(滞后:hit 时新增堆区不扫)"
        if not regions:
            WINDOW.close("no-regions")
            _disable_bp(bp_loc)
            _log(os.path.join(HIT_DIR, "window.log"),
                 f"ERROR: 活体枚举与 vmmap 区间表({VMMAP_PATH})皆不可用 -> window closed, bp disabled")
            return False

        t0 = time.time()
        hits, stats = scan_regions(proc, regions, probes=HIT_PROBES + AUX_PROBES)
        elapsed_ms = (time.time() - t0) * 1000.0
        primary_labels = {label for label, _ in HIT_PROBES}
        primary = [h for h in hits if h[0] in primary_labels]
        aux = [h for h in hits if h[0] not in primary_labels]
        if primary:
            path = _write_hit(buf.getvalue(), primary, aux, stats, elapsed_ms, regions_source)
            WINDOW.close(f"hit:{path}")
            _disable_bp(bp_loc)
        elif aux:
            _write_weak(buf.getvalue(), aux, stats, elapsed_ms, regions_source)
        else:
            if _miss_count() < MAX_MISS_LOG:
                _log(os.path.join(HIT_DIR, "window.log"),
                     f"miss: thread={name!r} scanned={stats['bytes']}B probes-none (窗口错失或过滤过狠,重开窗口再来)")
    except Exception as exc:  # noqa: BLE001 - 取证回调绝不抛;不确定态=关窗+禁断点+异常保帧
        WINDOW.close("callback-error")
        try:
            _write_hit(buf.getvalue(), [], [], {}, 0.0, "-", error=exc)
        except Exception:
            pass
        try:
            _disable_bp(bp_loc)
        except Exception:
            pass
        _log(os.path.join(HIT_DIR, "window.log"), f"callback-error: {exc!r} -> window closed, bp disabled")
    return False
