#!/opt/homebrew/bin/python3
"""装机包自动冒烟(package_smoke)——测 /Applications 里的真件,不是开发树。

用法(工作流统一执行;纪律:分钟级命令后台跑 + 日志文件 + 退出码文件):
    /opt/homebrew/bin/python3 desktop/ui-src/e2e/package_smoke.py

对象(以实存为准):
    /Applications/世事.app,缺则回落 /Applications/MYIA.app

两部分:
  A. 真机启动断言 —— open -g 静默启动装好的 app(不抢焦点;经
     `open --env MYIA_HOME=<沙箱>` 注入独立数据根 = 独立 .instance.lock,
     os-etiquette 铁律 6/7:全壳冒烟禁裸拉,open 不透传 shell env)→
     pgrep 断言 MYIA 主进程 + myssia-core sidecar 子进程同存活(PyInstaller
     onefile 为 父→子 两进程,认祖即可)→ CGWindowList(.optionAll) 断言窗口
     存在(在册坑:System Events 窗口计数 0 ≠ 无窗口,CGWindowList 才是权威;
     隐藏窗口亦列出)→ 断言数据根生成(.instance.lock/myssia.db/plugins 种子)
     → osascript 安静退出并确认进程退净。
  B. 包内件行为断言 —— 从 .app 包内提取真件:① UI dist:Tauri 2 release 把
     frontendDist 静态件以 brotli 压缩内嵌进 MYIA 主二进制(tauri-codegen
     embedded_assets,phf_map 的 (key:&str, value:&[u8]) 胖指针落在
     __DATA_CONST/__const),本脚本解析 Mach-O 定位胖指针 → 切片 →
     `brotli` CLI 解压成可服务的静态目录;② sidecar 二进制:
     Contents/MacOS/myssia-core 原位直跑(serve,stdio JSON-RPC,python 直连,
     零 node 依赖)。Playwright 加载解出的 UI dist + 注入 __TAURI_INTERNALS__
     shim(invoke 桥到沙箱 sidecar;含 __TAURI_EVENT_PLUGIN_INTERNALS__ no-op,
     在册坑),浏览器用 playwright 缓存的 Chrome for Testing(executable_path)。

     五组行为断言:
       1) 品类文件清单非空且含装机种子品类(随包 Resources/plugins 全集);
       2) 长品类文件滚动:.cm-scroller scrollH>clientH 且编程置 scrollTop 生效
          (10-04-yaml-editor-no-scroll 主修;另滚到尾行断言尾行可见=内容完整);
       3) ⌘F 开搜索面板后按 ESC:面板关闭且编辑对话框仍在(次修,defaultPrevented
          守卫);
       4) 中文文本插入:keyboard.type「测试中文输入」落到 .cm-content;
       5) 保存回路:保存后沙箱盘上文件含编辑内容且 .bak 留底(旧文原文)。

     已知不在此列(如实声明):真实 IME 组合输入无头不可模拟——第 4 组只是
     直接文本插入,组合输入(输入法候选/组字)须主人目验;此说明会打到 stdout。

沙箱纪律:全程 mkdtemp 沙箱 MYIA_HOME,严禁碰本机真实数据根
(~/Library/Application Support/MYIA);沙箱与临时进程 finally 清理。

依赖:/opt/homebrew/bin/python3 + playwright(py 包)、brotli CLI
(/opt/homebrew/bin/brotli)、Chrome for Testing
(~/Library/Caches/ms-playwright/chromium-1243;缺则按 chromium-* 回落最新)。

退出码:0 = 全部 PASS;1 = 任一 FAIL(含缺依赖等,尾部汇总失败清单);
2 = 找不到装机包(未安装/未换装)。整体自限 10 分钟(SIGALRM),超时按 FAIL
收口并清理。截图落 desktop/ui-src/e2e/artifacts/(已 .gitignore)。
"""

from __future__ import annotations

import ctypes
import json
import os
import plistlib
import queue
import re
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

# --------------------------------------------------------------------------
# 常量
# --------------------------------------------------------------------------
APP_CANDIDATES = ["/Applications/世事.app", "/Applications/MYIA.app"]
BUNDLE_ID = "com.myssia.app"
PLAYWRIGHT_CHROME_PRIMARY = (
    "/Users/zhengbingjin/Library/Caches/ms-playwright/chromium-1243/"
    "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
)
PLAYWRIGHT_CACHE = Path.home() / "Library/Caches/ms-playwright"
BROTLI_CANDIDATES = ["/opt/homebrew/bin/brotli", "/usr/local/bin/brotli", "/opt/local/bin/brotli"]
OVERALL_TIMEOUT_S = 600  # 整体自限 10 分钟
TYPED_ZH = "测试中文输入"
ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"

# Mach-O 胖指针扫描的节(键串/字节流常驻 rodata/data const)
POINTER_SECTIONS = {("__TEXT", "__const"), ("__DATA_CONST", "__const"), ("__DATA", "__const"), ("__DATA", "__data")}
# Tauri asset key 形如 /index.html、/assets/index-xxxx.js(AssetKey 规范化后带前导 /)
ASSET_KEY_RE = re.compile(
    r"^/[A-Za-z0-9._~@+-]+(?:/[A-Za-z0-9._~@+-]+)*"
    r"\.(?:html|js|mjs|css|svg|png|ico|json|txt|map|woff2?|ttf|wasm)$"
)
MAX_ASSET_BYTES = 64 * 1024 * 1024

MIME = {
    ".html": "text/html; charset=utf-8", ".js": "application/javascript", ".mjs": "application/javascript",
    ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png",
    ".ico": "image/x-icon", ".json": "application/json", ".txt": "text/plain; charset=utf-8",
    ".map": "application/json", ".woff": "font/woff", ".woff2": "font/woff2",
    ".ttf": "font/ttf", ".wasm": "application/wasm",
}


class SmokeTimeout(Exception):
    pass


class Report:
    """断言台账:每条即时打印 PASS/FAIL,尾部汇总失败清单,退出码说话。"""

    def __init__(self) -> None:
        self.failures: list[tuple[str, str]] = []

    def check(self, name: str, ok: bool, detail: str = "") -> bool:
        line = f"{'PASS' if ok else 'FAIL'} [{name}]"
        if detail:
            line += f" {detail}"
        print(line, flush=True)
        if not ok:
            self.failures.append((name, detail))
        return ok

    def summary(self) -> int:
        print("-" * 72, flush=True)
        if not self.failures:
            print("SMOKE RESULT: 全部 PASS", flush=True)
            return 0
        print(f"SMOKE RESULT: {len(self.failures)} 项 FAIL,失败清单:", flush=True)
        for name, detail in self.failures:
            print(f"  - [{name}] {detail}", flush=True)
        return 1


REPORT = Report()


def say(*args: object) -> None:
    print(*args, flush=True)


# --------------------------------------------------------------------------
# 小工具
# --------------------------------------------------------------------------
def run_cmd(argv: list[str], timeout: float = 30.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout)


def pgrep_exact(name: str) -> list[int]:
    r = subprocess.run(["pgrep", "-x", name], capture_output=True, text=True)
    if r.returncode != 0:
        return []
    return sorted(int(x) for x in r.stdout.split())


def process_ppid(pid: int) -> int | None:
    r = subprocess.run(["ps", "-o", "ppid=", "-p", str(pid)], capture_output=True, text=True)
    out = r.stdout.strip()
    return int(out) if out.isdigit() else None


def ancestor_pids(pid: int, hops: int = 12) -> set[int]:
    """向上收集祖先进程 pid(防 PyInstaller onefile 父->子多一层)。"""
    seen: set[int] = set()
    cur = pid
    for _ in range(hops):
        ppid = process_ppid(cur)
        if ppid is None or ppid <= 1 or ppid in seen:
            break
        seen.add(ppid)
        cur = ppid
    return seen


def find_brotli() -> str | None:
    for cand in BROTLI_CANDIDATES:
        if Path(cand).is_file():
            return cand
    return shutil.which("brotli")


def find_chrome() -> str | None:
    if Path(PLAYWRIGHT_CHROME_PRIMARY).is_file():
        return PLAYWRIGHT_CHROME_PRIMARY
    # 回落:playwright 缓存里最新 chromium-*(版本漂移兜底)
    cands = sorted(PLAYWRIGHT_CACHE.glob("chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"))
    return str(cands[-1]) if cands else None


# --------------------------------------------------------------------------
# Mach-O 内嵌 UI dist 提取(Tauri 2 embedded assets → brotli 流)
# --------------------------------------------------------------------------
def macho_file_sections(data: bytes) -> list[tuple[str, str, int, int, int]]:
    """解析 64 位 LE Mach-O 的 file-backed 节表:(segname, sectname, addr, size, offset)。"""
    if data[:4] != b"\xcf\xfa\xed\xfe":
        raise ValueError(f"不是 64 位 LE Mach-O(magic={data[:4].hex()})")
    ncmds = struct.unpack_from("<I", data, 16)[0]
    off = 32  # mach_header_64 定长
    sects: list[tuple[str, str, int, int, int]] = []
    for _ in range(ncmds):
        if off + 8 > len(data):
            break
        cmd, cmdsize = struct.unpack_from("<II", data, off)
        if cmd == 0x19:  # LC_SEGMENT_64
            segname = data[off + 8 : off + 24].rstrip(b"\0").decode("ascii", "replace")
            nsects = struct.unpack_from("<I", data, off + 64)[0]
            base = off + 72
            for i in range(nsects):
                e = base + i * 80  # section_64 定长
                sectname = data[e : e + 16].rstrip(b"\0").decode("ascii", "replace")
                addr, size = struct.unpack_from("<QQ", data, e + 32)
                foff = struct.unpack_from("<I", data, e + 48)[0]
                if size and foff:
                    sects.append((segname, sectname, addr, size, foff))
        if cmdsize <= 0:
            break
        off += cmdsize
    return sects


def extract_embedded_dist(binary: Path, out_dir: Path, brotli_bin: str) -> list[str]:
    """从 Tauri 2 主二进制提取 frontendDist 静态件到 out_dir,返回落盘相对路径列表。

    布局依据(tauri-codegen 2.7.1 embedded_assets.rs:391-404):phf_map! 的
    entry 是 ((&str 胖指针), (&[u8] 胖指针)),rustc 以 (ptr,len,ptr,len)
    四连 qword 落 const 节;字节流是独立 brotli 压缩静态(include_bytes!)。
    本函数对四连 qword 做形状筛选(键串过 asset 名正则 + 数据落 file-backed 节),
    命中即切片送 brotli CLI 解压。已在 /Applications/世事.app 实物上验证
    (6 件:index.html/图标 svg/3 js/1 css 全解出)。
    """
    data = binary.read_bytes()
    sects = macho_file_sections(data)
    if not sects:
        raise ValueError("Mach-O 节表为空")

    def vm2off(vm: int) -> int | None:
        for _, _, addr, size, foff in sects:
            if addr <= vm < addr + size:
                return foff + (vm - addr)
        return None

    entries: dict[str, set[tuple[int, int]]] = {}
    for seg, sect, _addr, size, foff in sects:
        if (seg, sect) not in POINTER_SECTIONS:
            continue
        body = data[foff : foff + size]
        for i in range(0, max(len(body) - 32, 0), 8):
            q_key_ptr, q_key_len, q_dat_ptr, q_dat_len = struct.unpack_from("<4Q", body, i)
            if not (0 < q_key_len < 256) or q_dat_len <= 0 or q_dat_len > MAX_ASSET_BYTES:
                continue
            key_off = vm2off(q_key_ptr)
            dat_off = vm2off(q_dat_ptr)
            if key_off is None or dat_off is None:
                continue
            try:
                key = data[key_off : key_off + q_key_len].decode("utf-8")
            except UnicodeDecodeError:
                continue
            if not ASSET_KEY_RE.match(key):
                continue
            entries.setdefault(key, set()).add((dat_off, q_dat_len))

    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    for key, cands in sorted(entries.items()):
        rel = key.lstrip("/")
        dest = out_dir / rel
        for dat_off, dat_len in sorted(cands):
            tmp = out_dir / f".{rel.replace('/', '_')}.br"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_bytes(data[dat_off : dat_off + dat_len])
            r = subprocess.run([brotli_bin, "-d", "-c", str(tmp)], capture_output=True, timeout=60)
            tmp.unlink(missing_ok=True)
            if r.returncode == 0 and r.stdout:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(r.stdout)
                written.append(rel)
                break
    return sorted(written)


# --------------------------------------------------------------------------
# CGWindowList(ctypes;pyobjc 不在 /opt/homebrew/bin/python3,手搓 CoreGraphics)
# --------------------------------------------------------------------------
def cg_windows_owned_by(pid: int) -> list[dict]:
    """CGWindowListCopyWindowInfo(optionAll) 里 owner==pid 的窗口(隐藏窗亦列)。"""
    cg = ctypes.CDLL("/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics")
    cf = ctypes.CDLL("/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation")
    for fn, argt, rest in [
        ("CFArrayGetCount", [ctypes.c_void_p], ctypes.c_long),
        ("CFArrayGetValueAtIndex", [ctypes.c_void_p, ctypes.c_long], ctypes.c_void_p),
        ("CFDictionaryGetValue", [ctypes.c_void_p, ctypes.c_void_p], ctypes.c_void_p),
        ("CFNumberGetValue", [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p], ctypes.c_ubyte),
        ("CFStringCreateWithCString", [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32], ctypes.c_void_p),
        ("CFStringGetCString", [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_uint32], ctypes.c_ubyte),
    ]:
        fn_ = getattr(cf, fn)
        fn_.argtypes = argt
        fn_.restype = rest
    cg.CGWindowListCopyWindowInfo.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    cg.CGWindowListCopyWindowInfo.restype = ctypes.c_void_p
    UTF8 = 0x08000100

    def cfstr(s: str) -> int:
        return cf.CFStringCreateWithCString(None, s.encode(), UTF8)

    def dstr(d: int, key: str) -> str | None:
        v = cf.CFDictionaryGetValue(d, cfstr(key))
        if not v:
            return None
        buf = ctypes.create_string_buffer(256)
        return buf.value.decode("utf-8", "replace") if cf.CFStringGetCString(v, buf, 256, UTF8) else None

    def dint(d: int, key: str) -> int | None:
        v = cf.CFDictionaryGetValue(d, cfstr(key))
        if not v:
            return None
        out = ctypes.c_int64(0)
        return out.value if cf.CFNumberGetValue(v, 4, ctypes.byref(out)) else None  # 4=kCFNumberSInt64Type

    arr = cg.CGWindowListCopyWindowInfo(0, 0)  # 0 = kCGWindowListOptionAll
    if not arr:
        return []
    hits = []
    for i in range(cf.CFArrayGetCount(ctypes.c_void_p(arr))):
        d = cf.CFArrayGetValueAtIndex(ctypes.c_void_p(arr), i)
        if d and dint(d, "kCGWindowOwnerPID") == pid:
            hits.append({"num": dint(d, "kCGWindowNumber"), "layer": dint(d, "kCGWindowLayer"),
                         "owner": dstr(d, "kCGWindowOwnerName")})
    return hits


# --------------------------------------------------------------------------
# 包内 sidecar(stdio JSON-RPC)+ HTTP 桥(python 直连,零 node 依赖)
# --------------------------------------------------------------------------
class SidecarProcess:
    """spawn 包内 myssia-core serve;行式 JSON-RPC 应答回递 + 无 id 事件广播。"""

    def __init__(self, binary: Path, home: Path, stderr_path: Path, env_extra: dict[str, str] | None = None) -> None:
        env = {**os.environ, "MYIA_HOME": str(home), **(env_extra or {})}
        env.pop("MYIA_PLUGIN_DIR", None)  # 市场安装根随沙箱 home,防外泄
        self.stderr_path = stderr_path
        self._stderr = open(stderr_path, "wb")
        self.proc = subprocess.Popen(
            [str(binary), "serve"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self._stderr, env=env,
        )
        self._lock = threading.Lock()
        self._cond = threading.Condition(self._lock)
        self._pending: dict[int, dict | None] = {}
        self._next_id = 1
        self.event_queues: list[queue.Queue[str]] = []
        self.non_json_lines = 0
        self._reader = threading.Thread(target=self._pump, daemon=True, name="sidecar-reader")
        self._reader.start()

    def _pump(self) -> None:
        assert self.proc.stdout is not None
        for raw in iter(self.proc.stdout.readline, b""):
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                self.non_json_lines += 1
                continue
            if "id" in obj and ("result" in obj or "error" in obj):
                with self._cond:
                    self._pending[obj["id"]] = obj
                    self._cond.notify_all()
            elif "type" in obj:
                with self._lock:
                    for q in self.event_queues:
                        q.put(line)

    def subscribe(self) -> "queue.Queue[str]":
        q: queue.Queue[str] = queue.Queue()
        with self._lock:
            self.event_queues.append(q)
        return q

    def request(self, method: str, params: dict, timeout: float = 90.0) -> dict:
        """一次 JSON-RPC 往返;sidecar error 以 RuntimeError 携错误对象抛出。"""
        with self._cond:
            rid = self._next_id
            self._next_id += 1
        line = json.dumps({"id": rid, "method": method, "params": params}, ensure_ascii=False) + "\n"
        assert self.proc.stdin is not None
        with self._cond:
            try:
                self.proc.stdin.write(line.encode("utf-8"))
                self.proc.stdin.flush()
            except (BrokenPipeError, OSError) as exc:
                raise RuntimeError(f"sidecar 进程未运行(write 失败:{exc})") from exc
            deadline = time.monotonic() + timeout
            while rid not in self._pending:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"sidecar 应答超时({timeout}s): {method}")
                self._cond.wait(remaining)
            reply = self._pending.pop(rid)
        if "error" in reply:
            raise RuntimeError(f"sidecar error({method}): {json.dumps(reply['error'], ensure_ascii=False)}")
        return reply.get("result")

    def close(self) -> None:
        """关 stdin = EOF 干净退出(design §2.1②);超时才升级 terminate/kill。"""
        try:
            if self.proc.stdin and not self.proc.stdin.closed:
                self.proc.stdin.close()
            try:
                self.proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait(timeout=10)
        finally:
            try:
                self._stderr.close()
            except OSError:
                pass


class BridgeServer(ThreadingHTTPServer):
    """同源 HTTP 桥:静态(解包 UI dist)+ /rpc + /events(SSE)。"""

    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, www_dir: Path, sidecar: SidecarProcess) -> None:
        self.www_dir = www_dir
        self.sidecar = sidecar
        super().__init__(("127.0.0.1", 0), BridgeHandler)


class BridgeHandler(BaseHTTPRequestHandler):
    server: BridgeServer

    def log_message(self, fmt: str, *args: object) -> None:  # 安静:不打默认访问日志
        pass

    def _cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "content-type")

    def do_OPTIONS(self) -> None:  # noqa: N802(BaseHTTPRequestHandler 约定)
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = unquote(urlparse(self.path).path)
        if path == "/events":
            self._events()
            return
        if path == "/health":
            body = b'{"ok":true}'
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self._cors()
            self.end_headers()
            self.wfile.write(body)
            return
        self._static(path)

    def _static(self, path: str) -> None:
        rel = path.lstrip("/") or "index.html"
        target = (self.server.www_dir / rel).resolve()
        if not str(target).startswith(str(self.server.www_dir.resolve()) + os.sep) or not target.is_file():
            self.send_response(404)
            self._cors()
            self.end_headers()
            return
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", MIME.get(target.suffix.lower(), "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _events(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self._cors()
        self.end_headers()
        q = self.server.sidecar.subscribe()
        try:
            self.wfile.write(b":open\n\n")
            self.wfile.flush()
            while True:
                try:
                    line = q.get(timeout=15)
                    self.wfile.write(f"data: {line}\n\n".encode("utf-8"))
                except queue.Empty:
                    self.wfile.write(b":keepalive\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/rpc":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode("utf-8"))
            method, params = payload["method"], payload.get("params") or {}
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError) as exc:
            body = json.dumps({"code": "invalid_params", "path": "$", "message": f"bridge 收到非法请求: {exc}"}).encode()
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self._cors()
            self.end_headers()
            self.wfile.write(body)
            return
        try:
            result = self.server.sidecar.request(method, params, timeout=120.0)
            body = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self._cors()
            self.end_headers()
            self.wfile.write(body)
        except RuntimeError as exc:  # sidecar 结构化错误 → 500 + 错误对象 JSON 文本
            # 与 Rust Err(String)/壳侧同形状:前端 toSidecarError 按 reject 值字符串解析
            try:
                err_obj = json.loads(str(exc).split("sidecar error", 1)[-1].split(": ", 1)[-1])
            except (json.JSONDecodeError, IndexError):
                err_obj = {"code": "bridge_error", "path": "$", "message": str(exc)}
            body = json.dumps(err_obj, ensure_ascii=False).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self._cors()
            self.end_headers()
            self.wfile.write(body)
        except TimeoutError as exc:
            body = json.dumps({"code": "bridge_timeout", "path": "$", "message": str(exc)}).encode()
            self.send_response(504)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self._cors()
            self.end_headers()
            self.wfile.write(body)


# 浏览器内 Tauri IPC shim(同源版;先例:10-04-yaml-editor-no-scroll/evidence/shim.js
# + 10-03-fe-small-batch bridge.mjs)。含 __TAURI_EVENT_PLUGIN_INTERNALS__ no-op(在册坑:
# 新版 @tauri-apps/api unlisten 走它,缺了路由切换即抛 pageerror)。
SHIM_JS = r"""
(() => {
  let cbId = 0;
  const callbacks = new Map();
  const listeners = {};
  const ensureSSE = () => {
    if (window.__myiaSSE) return;
    const es = new EventSource("/events");
    es.onmessage = (message) => {
      let payload;
      try { payload = JSON.parse(message.data); } catch { return; }
      for (const handlerId of listeners["sidecar://event"] ?? []) {
        const entry = callbacks.get(handlerId);
        if (entry) {
          entry.cb({ event: "sidecar://event", id: 0, payload });
          if (entry.once) callbacks.delete(handlerId);
        }
      }
    };
    window.__myiaSSE = es;
  };
  window.__TAURI_INTERNALS__ = {
    transformCallback(callback, once = false) {
      const id = ++cbId;
      callbacks.set(id, { cb: callback, once });
      return id;
    },
    unregisterCallback(id) { callbacks.delete(id); },
    async invoke(cmd, args = {}, options) {
      if (cmd === "plugin:event|listen") {
        (listeners[args.event] ?? (listeners[args.event] = [])).push(args.handler);
        ensureSSE();
        return Date.now();
      }
      if (cmd === "plugin:event|unlisten") return undefined;
      if (cmd !== "sidecar_request") return undefined;
      const response = await fetch("/rpc", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(args),
      });
      if (!response.ok) throw await response.text();
      return await response.json();
    },
  };
})();
(() => {
  window.__TAURI_EVENT_PLUGIN_INTERNALS__ = window.__TAURI_EVENT_PLUGIN_INTERNALS__ ?? {
    unregisterListener() {},
  };
})();
"""


# --------------------------------------------------------------------------
# Part A:真机启动断言
# --------------------------------------------------------------------------
def part_a(app_dir: Path, cleanups: list) -> None:
    say("=" * 72)
    say(f"PART A 真机启动断言:{app_dir}")
    say("=" * 72)

    # A0 预检:已有实例在跑则无法做启动断言(单实例锁会让新实例转激活旧实例后退出)
    pre_main = pgrep_exact("MYIA")
    pre_side = pgrep_exact("myssia-core")
    if not REPORT.check("A0-预检无既有实例", not pre_main and not pre_side,
                        f"MYIA={pre_main} myssia-core={pre_side}" if (pre_main or pre_side) else "环境干净"):
        say("  环境不干净(主人或他线在跑 app),Part A 无法做启动断言,跳过本部分")
        return

    sandbox = Path(tempfile.mkdtemp(prefix="myia-smoke-a-"))
    cleanups.append(lambda: shutil.rmtree(sandbox, ignore_errors=True))
    say(f"  沙箱数据根 MYIA_HOME={sandbox}(独立 .instance.lock 域,不碰真根)")

    # A1 open -g 静默启动(--env 通道:open 不透传 shell env,os-etiquette 铁律 7)
    r = run_cmd(["open", "--env", f"MYIA_HOME={sandbox}", "-g", str(app_dir)], timeout=30)
    REPORT.check("A1-open -g 静默启动", r.returncode == 0, f"rc={r.returncode} err={r.stderr.strip()[:120]}")

    # A2 主进程 + sidecar 同存活(pgrep;onefile 是 父->子 两进程,认祖即子进程)
    main_pid: int | None = None
    side_pids: list[int] = []
    for _ in range(60):
        time.sleep(1.0)
        mains = pgrep_exact("MYIA")
        sides = pgrep_exact("myssia-core")
        if mains and sides:
            main_pid, side_pids = mains[0], sides
            break
    REPORT.check("A2-MYIA 主进程存活(pgrep -x MYIA)", main_pid is not None, f"pid={main_pid}")
    is_child = any(main_pid in ancestor_pids(sp) for sp in side_pids) if main_pid else False
    REPORT.check("A3-myssia-core sidecar 子进程存活(pgrep -x myssia-core,祖含 MYIA)",
                 bool(side_pids) and is_child, f"sidecars={side_pids} 祖链含主进程={is_child}")

    # A4 窗口存在(CGWindowList optionAll;隐藏窗亦列,System Events 会假阴性,在册坑)
    windows: list[dict] = []
    a4_reported = False
    if main_pid:
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            try:
                windows = cg_windows_owned_by(main_pid)
            except Exception as exc:  # noqa: BLE001 — ctypes 失败要如实入失败明细
                REPORT.check("A4-窗口存在(CGWindowList optionAll)", False, f"ctypes 异常: {exc}")
                a4_reported = True
                break
            if windows:
                break
            time.sleep(1.0)
        if not a4_reported:
            REPORT.check("A4-窗口存在(CGWindowList optionAll)", bool(windows),
                         f"{len(windows)} 窗口 {windows[:2]}" if windows else "optionAll 无本 pid 窗口")
    else:
        REPORT.check("A4-窗口存在(CGWindowList optionAll)", False, "主进程未存活,无从断言")

    # A5 数据根生成(锁/库/种子插件)
    def sandbox_state() -> dict:
        yamls = sorted(p.name for p in (sandbox / "plugins").glob("*.y*ml")) if (sandbox / "plugins").is_dir() else []
        return {
            "lock": (sandbox / ".instance.lock").exists(),
            "db": (sandbox / "myssia.db").exists(),
            "yamls": yamls,
        }
    state = {"yamls": []}
    for _ in range(60):
        state = sandbox_state()
        if state["lock"] and state["db"] and state["yamls"]:
            break
        time.sleep(1.0)
    REPORT.check("A5-数据根生成(.instance.lock+myssia.db+种子品类)",
                 state["lock"] and state["db"] and bool(state["yamls"]),
                 f"lock={state['lock']} db={state['db']} 种子={state['yamls']}")

    # A6 安静退出(osascript quit;0.5-3s 内退净;兜底 TERM)
    run_cmd(["osascript", "-e", f'tell application id "{BUNDLE_ID}" to quit'], timeout=30)
    exited = False
    for _ in range(30):
        time.sleep(0.5)
        if not pgrep_exact("MYIA"):
            exited = True
            break
    if not exited:
        run_cmd(["pkill", "-TERM", "-x", "MYIA"], timeout=15)
        for _ in range(20):
            time.sleep(0.5)
            if not pgrep_exact("MYIA"):
                exited = True
                break
    side_gone = not pgrep_exact("myssia-core")
    if not side_gone:  # 孤儿 sidecar 兜底(stdin EOF 应已自清,防万一)
        run_cmd(["pkill", "-TERM", "-x", "myssia-core"], timeout=15)
        time.sleep(2.0)
        side_gone = not pgrep_exact("myssia-core")
    REPORT.check("A6-安静退出(osascript quit)", exited and side_gone,
                 f"主进程退净={exited} sidecar 退净={side_gone}")


# --------------------------------------------------------------------------
# Part B:包内件行为断言
# --------------------------------------------------------------------------
def part_b(app_dir: Path, cleanups: list) -> None:
    say("=" * 72)
    say(f"PART B 包内件行为断言:{app_dir}")
    say("=" * 72)

    main_binary = app_dir / "Contents/MacOS/MYIA"
    sidecar_binary = app_dir / "Contents/MacOS/myssia-core"
    bundle_plugins = app_dir / "Contents/Resources/plugins"
    seed_names = sorted(p.name for p in bundle_plugins.glob("*.y*ml")) if bundle_plugins.is_dir() else []

    # X0 提取包内 UI dist(Mach-O 内嵌 brotli 资产)
    brotli_bin = find_brotli()
    if not REPORT.check("X0a-brotli CLI 可用", brotli_bin is not None, f"{brotli_bin}"):
        return
    www_dir = Path(tempfile.mkdtemp(prefix="myia-smoke-www-"))
    cleanups.append(lambda: shutil.rmtree(www_dir, ignore_errors=True))
    try:
        files = extract_embedded_dist(main_binary, www_dir, brotli_bin)
    except Exception as exc:  # noqa: BLE001 — 提取失败要如实带明细
        REPORT.check("X0b-提取内嵌 UI dist", False, f"异常: {exc}")
        return
    idx = www_dir / "index.html"
    idx_ok = idx.is_file() and (b"<script" in idx.read_bytes() or b"id=\"root\"" in idx.read_bytes())
    REPORT.check("X0b-提取内嵌 UI dist", len(files) >= 3 and idx_ok,
                 f"{len(files)} 件: {', '.join(files)}; index.html 合式={idx_ok}")

    # 依赖前置检查(缺了就别白拉 sidecar)
    chrome = find_chrome()
    if not REPORT.check("B0-Chrome for Testing 可用", chrome is not None, f"{chrome}"):
        return
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        REPORT.check("B0-playwright(py 包) 可用", False, f"{exc}(/opt/homebrew pip 装 playwright)")
        return

    # S0 spawn 包内 sidecar(沙箱 MYIA_HOME;MYIA_APP_VERSION 对齐 Info.plist)
    app_version = "0.0.1"
    try:
        with open(app_dir / "Contents/Info.plist", "rb") as fh:
            app_version = plistlib.load(fh).get("CFBundleShortVersionString", "0.0.1")
    except (OSError, plistlib.InvalidFileException):
        pass
    sandbox = Path(tempfile.mkdtemp(prefix="myia-smoke-b-"))
    cleanups.append(lambda: shutil.rmtree(sandbox, ignore_errors=True))
    stderr_log = ARTIFACTS_DIR / "partb-sidecar.stderr.log"
    say(f"  沙箱 MYIA_HOME={sandbox} sidecar stderr→{stderr_log}")
    sidecar: SidecarProcess | None = None
    server: BridgeServer | None = None
    try:
        sidecar = SidecarProcess(sidecar_binary, sandbox, stderr_log, {"MYIA_APP_VERSION": app_version})
        cleanups.append(sidecar.close)
        version = sidecar.request("version", {}, timeout=120.0)  # onefile 解压首启慢
        say(f"  sidecar version 应答:{json.dumps(version, ensure_ascii=False)[:160]}")
        seeded = sorted(p.name for p in (sandbox / "plugins").glob("*.y*ml")) if (sandbox / "plugins").is_dir() else []
        seeds_ok = REPORT.check("S0-包内 sidecar 沙箱首跑+种子(随包官方插件全量)",
                                bool(seed_names) and seeded == seed_names,
                                f"随包={seed_names} 沙箱={seeded}")

        server = BridgeServer(www_dir, sidecar)
        cleanups.append(server.shutdown)
        threading.Thread(target=server.serve_forever, daemon=True, name="bridge-http").start()
        origin = f"http://127.0.0.1:{server.server_address[1]}"
        say(f"  桥同源服务:{origin}(静态 UI + /rpc + /events)")

        if not seeds_ok:
            say("  种子未落,后续 UI 断言无从谈起,提前收口")
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path=chrome)
            try:
                context = browser.new_context(viewport={"width": 1600, "height": 1000})
                page = context.new_page()
                page.add_init_script(SHIM_JS)
                page.on("console", lambda m: say(f"  [console.{m.type}] {m.text[:180]}") if m.type in ("error", "warning") else None)
                page.on("pageerror", lambda e: say(f"  [pageerror] {str(e)[:180]}"))
                drive_ui(page, origin, sandbox, seed_names)
            finally:
                browser.close()
    finally:
        if server:
            try:
                server.shutdown()
            except Exception:  # noqa: BLE001 — 收尾尽力
                pass
        if sidecar:
            sidecar.close()


def drive_ui(page, origin: str, sandbox: Path, seed_names: list[str]) -> None:
    """五组行为断言(选择器先例:evidence/probe.py + yaml-editor-dialog.tsx testid)。"""
    shot = lambda name: page.screenshot(path=str(ARTIFACTS_DIR / name))  # noqa: E731

    # ---- B1 品类文件清单非空且含装机种子品类(#/yaml-editor 左栏清单)----
    page.goto(f"{origin}/#/yaml-editor")
    page.wait_for_selector("[data-testid='yaml-file-list'] ul[aria-label='品类文件清单'] li", timeout=30000)
    page.wait_for_timeout(1200)  # yaml.list 应答渲染
    entry_count = page.locator("[data-testid='yaml-file-list'] ul[aria-label='品类文件清单'] li").count()
    list_text = page.inner_text("[data-testid='yaml-file-list']")
    missing = [n for n in seed_names if n not in list_text]
    REPORT.check("B1-品类文件清单非空且含装机种子品类", entry_count > 0 and not missing,
                 f"清单 {entry_count} 项,缺种子={missing or '无'}")
    shot("b1-yaml-file-list.png")

    # 选行数最多的品类(磁盘真值),走源管理行内编辑弹窗(报障入口)
    def line_count(name: str) -> int:
        try:
            return len((sandbox / "plugins" / name).read_text(encoding="utf-8").splitlines())
        except OSError:
            return -1
    longest = max(seed_names, key=line_count)
    longest_path = sandbox / "plugins" / longest
    disk_before = longest_path.read_text(encoding="utf-8")
    say(f"  行数最多品类:{longest}({line_count(longest)} 行)")

    page.goto(f"{origin}/#/sources")
    edit_btn = page.locator(f"button[title^='弹出编辑对话框'][title*='{longest}']").first
    edit_btn.wait_for(state="visible", timeout=30000)
    edit_btn.click()
    page.wait_for_selector("[data-testid='yaml-editor-dialog']", timeout=15000)
    page.wait_for_selector(".cm-content", timeout=15000)
    page.wait_for_timeout(1000)  # CM 视口渲染落定
    shown_path = page.locator("[data-testid='editor-path']").inner_text()
    REPORT.check("B2-0-编辑弹窗打开(源管理行内编辑)", longest in shown_path, f"editor-path={shown_path}")

    # ---- B2 长品类滚动(scrollH>clientH + 编程 scrollTop 生效 + 尾行可见)----
    metrics = page.evaluate(
        """() => {
          const s = document.querySelector('.cm-scroller');
          if (!s) return null;
          return { scrollH: s.scrollHeight, clientH: s.clientHeight, top: s.scrollTop };
        }"""
    )
    scrollable = metrics and metrics["scrollH"] > metrics["clientH"]
    REPORT.check("B2-1-.cm-scroller scrollH>clientH(可滚)", bool(scrollable),
                 f"metrics={metrics}" if metrics else "找不到 .cm-scroller")
    scrolled = page.evaluate(
        """() => {
          const s = document.querySelector('.cm-scroller');
          const target = Math.floor((s.scrollHeight - s.clientHeight) / 2);
          s.scrollTop = target;
          return { target, after: s.scrollTop };
        }"""
    )
    REPORT.check("B2-2-编程置 scrollTop 生效", scrolled and scrolled["after"] > 0,
                 f"target={scrolled['target'] if scrolled else None} after={scrolled['after'] if scrolled else None}")
    tail_token = next((ln.strip() for ln in reversed(disk_before.splitlines()) if ln.strip()), "")
    page.evaluate("() => { const s = document.querySelector('.cm-scroller'); s.scrollTop = s.scrollHeight; }")
    tail_visible = False
    for _ in range(10):  # CM6 虚拟渲染随滚动物化,短轮询至尾行出现
        page.wait_for_timeout(300)
        text = page.evaluate("() => document.querySelector('.cm-content')?.innerText ?? ''")
        if tail_token and tail_token[:24] in text:
            tail_visible = True
            break
    REPORT.check("B2-3-滚到尾行可见(内容完整)", tail_visible, f"尾行 token={tail_token[:40]!r}")
    shot("b2-dialog-scrolled.png")

    # ---- B3 ⌘F 搜索面板 + ESC:面板关、弹窗在(defaultPrevented 守卫)----
    page.click(".cm-content")
    page.keyboard.press("Meta+f")
    panel_ok = False
    try:
        page.wait_for_selector(".cm-panel.cm-search", timeout=5000)
        panel_ok = True
    except Exception:  # noqa: BLE001 — Playwright 超时走断言,不走异常
        panel_ok = False
    REPORT.check("B3-1-⌘F 打开搜索面板(.cm-panel.cm-search)", panel_ok)
    shot("b3-search-panel.png")
    page.keyboard.press("Escape")
    page.wait_for_timeout(600)
    panel_gone = page.evaluate("() => !document.querySelector('.cm-panel.cm-search')")
    dialog_alive = page.evaluate("() => !!document.querySelector('[data-testid=\"yaml-editor-dialog\"]')")
    REPORT.check("B3-2-ESC 后面板关且编辑对话框仍在", panel_gone and dialog_alive,
                 f"面板已关={panel_gone} 弹窗仍在={dialog_alive}")
    shot("b3-after-esc.png")

    # ---- B4 中文文本插入(直接文本插入;真实 IME 组合输入无头测不了,见 stdout 说明)----
    say("  [不在此列] 真实 IME 组合输入(输入法组字/候选)无头环境不可模拟,本组仅验证"
        " keyboard.type 直接文本插入落到 .cm-content;组合输入请主人装机后人工敲一段中文目验。")
    page.click(".cm-content")
    page.keyboard.type(TYPED_ZH, delay=40)
    page.wait_for_timeout(500)
    content_text = page.evaluate("() => document.querySelector('.cm-content')?.innerText ?? ''")
    title_text = page.evaluate(
        "() => document.querySelector('[data-testid=\"editor-title\"]')?.textContent ?? ''"
    )
    typed_ok = TYPED_ZH in content_text
    dirty_shown = " *" in title_text  # 文件名后缀脏标记(editor-title 含路径子 span,用包含不用尾缀)
    REPORT.check("B4-中文文本插入落到 .cm-content", typed_ok and dirty_shown,
                 f"含「{TYPED_ZH}」={typed_ok} 标题脏标记(*)={dirty_shown}")
    shot("b4-chinese-typed.png")

    # ---- B5 保存回路:保存 → 沙箱盘文件变更 + .bak 留底 ----
    save_btn = page.locator("[data-testid='yaml-editor-dialog'] button:has-text('保存')").first
    save_btn.click(timeout=15000)  # click 自动等 dirty 解禁
    save_ok = False
    try:
        page.wait_for_selector("[data-testid='save-ok']", timeout=30000)
        save_ok = True
    except Exception:  # noqa: BLE001
        save_ok = False
    disk_after = longest_path.read_text(encoding="utf-8") if longest_path.is_file() else ""
    bak_path = longest_path.with_suffix(longest_path.suffix + ".bak")
    bak_content = bak_path.read_text(encoding="utf-8") if bak_path.is_file() else None
    REPORT.check("B5-保存回路:盘上文件含编辑且 .bak 留底(旧文原文)",
                 save_ok and TYPED_ZH in disk_after and disk_after != disk_before
                 and bak_content is not None and bak_content == disk_before,
                 f"save-ok UI={save_ok} 盘含编辑={TYPED_ZH in disk_after} "
                 f".bak={bak_path.name if bak_path.is_file() else '缺失'} .bak==旧文={bak_content == disk_before if bak_content is not None else False}")
    shot("b5-saved.png")


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def find_app() -> Path | None:
    for cand in APP_CANDIDATES:
        if Path(cand).is_dir():
            return Path(cand)
    return None


def on_alarm(signum: int, frame: object) -> None:
    raise SmokeTimeout(f"整体超时(>{OVERALL_TIMEOUT_S}s)自限熔断")


def main() -> int:
    signal.signal(signal.SIGALRM, on_alarm)
    signal.alarm(OVERALL_TIMEOUT_S)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    app_dir = find_app()
    if app_dir is None:
        say(f"找不到装机包(候选:{', '.join(APP_CANDIDATES)})——先安装/换装再跑冒烟")
        return 2
    say(f"冒烟对象:{app_dir}")
    say(f"截图目录:{ARTIFACTS_DIR}")

    cleanups: list = []
    exit_code = 2
    try:
        part_a(app_dir, cleanups)
        part_b(app_dir, cleanups)
        exit_code = REPORT.summary()
    except SmokeTimeout as exc:
        REPORT.check("ZZ-整体超时熔断", False, str(exc))
        exit_code = REPORT.summary()
    except Exception as exc:  # noqa: BLE001 — 冒烟脚本自身崩溃也要如实带明细退出
        import traceback

        traceback.print_exc()
        REPORT.check("ZZ-脚本异常", False, f"{type(exc).__name__}: {exc}")
        exit_code = REPORT.summary()
    finally:
        # 沙箱与临时进程兜底清理(幂等;Part A/B 的常规收尾已各自做过)
        if pgrep_exact("MYIA"):  # Part A 异常中断遗留才触达
            run_cmd(["osascript", "-e", f'tell application id "{BUNDLE_ID}" to quit'], timeout=20)
            time.sleep(2.0)
            if pgrep_exact("MYIA"):
                run_cmd(["pkill", "-TERM", "-x", "MYIA"], timeout=10)
        for cleanup in cleanups:
            try:
                cleanup()
            except Exception:  # noqa: BLE001 — 收尾尽力而为
                pass
        signal.alarm(0)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
