"""自管 Python 环境沙箱端到端(10-05-desktop-managed-py-env implement.md
第 5 条门 / AC1 主链):真壳(debug 二进制)+ 真钉版运行时 + 真 pip + 真 serve。

design §8「本地起静态服务器供运行时 tar.gz(钉版文件本地化)全链真跑」在第 3
步以合成归档落地(壳内 cargo test);本文件补齐真件面,覆盖第 3 步回标注明的
主人侧待办「真运行时端到端:15-38MB 钉版 cpython + 真 pip 依赖 + 真 serve 握手
的沙箱数据根全链真跑(MYIA_HOME 隔离)」与遗留(low,pyenv_install.rs:1033)
「AppHandle 胶水层(安装线程 → ready → spawn_sidecar_if_idle → app.shell()
拉进程)必须真跑覆盖」:

- 本地静态服务器双职能:①钉版运行时 tar.gz(15MB 真件,本地化缓存,sha256
  恒校验 manifest 钉值);②PEP 503 simple 索引(锁版清单 wheels 本地化)——
  壳安装链经 ``pyenv-settings.json`` 双镜像覆盖指向本地(AC3 索引覆盖生效的
  实证:pip 逐包请求全部落在本地服务器,记账断言)。
- 壳驱动方式:``MYIA_PYENV_AUTOSETUP`` 冒烟钩子(main.rs,同 MYIA_SMOKE_ROUTE
  先例;产品行为不变,D2「用户显式点开始配置」语义保留——钩子=测试替用户点)。
  经此钩子真跑第 3 步 AppHandle 胶水:start_install_thread → install_thread_main
  → run_chain 五阶段 → ready 戳 → spawn_sidecar_if_idle 自动拉起常驻 sidecar。
- 全功能冒烟:同一沙箱 + 同一自管 python + 同一随包源码另起 serve 进程,逐方法
  RPC 往返(源管理 plugins.list/health、情报流 store.items/runs.list/logs.tail、
  定时 cron.list/cron.status 等;写路径与涉外网方法不进离线端到端)。
- 幂等二跑(AC4):``MYIA_PYENV_AUTOSETUP=force`` 重跑安装链——已装步全
  skipped、不重下运行时、pip 已装跳过(不触碰本地索引)、自检恒重跑作终门。

缓存(首跑需网络,之后离线可复跑):``MYIA_TEST_CACHE`` 或缺省
``~/Library/Caches/myia-pyenv-e2e``;运行时 tar.gz 与锁版 wheels 均本地化,
清单变脸自动重下(marker = 锁版清单 sha256)。仅 mac aarch64(与 dmg 单架构
一致);Windows 等效链归 AC6/CI,真机冒烟留主人侧。
"""

from __future__ import annotations

import json
import os
import platform
import queue
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
import urllib.request
from collections import Counter
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DESKTOP = REPO_ROOT / "desktop"
SRC_TAURI = DESKTOP / "src-tauri"
LOCK_FILE = DESKTOP / "resources" / "requirements-lock.txt"
MANIFEST_FILE = DESKTOP / "resources" / "runtime-manifest.json"
TAURI_CONF = SRC_TAURI / "tauri.conf.json"

#: 本机平台键 = manifest 平台键 = Rust target triple(测试仅 mac aarch64,
#: 与现行 dmg 单架构一致;skip 见 pytestmark)。
HOST_TRIPLE = "aarch64-apple-darwin"

#: 钉版文件本地化缓存根(首跑需网络下载;复跑离线)。
CACHE_ROOT = Path(
    os.environ.get("MYIA_TEST_CACHE")
    or (Path.home() / "Library" / "Caches" / "myia-pyenv-e2e")
)

#: 安装链全链(下载 15MB 本地 + 解压 + pip 26 wheels 本地 + 自检)预算;
#: 本地静态服务器下实际秒级-分钟级,600s 为慢机/CI 富余。
CHAIN_TIMEOUT = 600
#: force 二跑预算(全 skipped + 自检秒级)。
RERUN_TIMEOUT = 180
#: 安装链 ready 后 sidecar 自动拉起(spawn_sidecar_if_idle)的观察窗。
SIDECAR_SPAWN_TIMEOUT = 30

pytestmark = [
    pytest.mark.skipif(
        sys.platform != "darwin" or platform.machine() != "arm64",
        reason="AC1 沙箱端到端仅 mac aarch64(现行 dmg 单架构);Windows 等效链归 AC6/CI",
    ),
]


def _sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest_entry() -> dict:
    """manifest 本平台条目(钉版权威:url + sha256 + 布局)。"""
    manifest = json.loads(MANIFEST_FILE.read_text())
    entry = manifest["platforms"].get(HOST_TRIPLE)
    assert entry, f"runtime-manifest 缺 {HOST_TRIPLE} 条目"
    return entry


# ---------------------------------------------------------------------------
# 夹具:钉版文件本地化(runtime tar.gz + 锁版 wheels)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def pinned_runtime() -> Path:
    """钉版运行时 tar.gz(design §8「钉版文件本地化」):缓存优先,缺则按
    manifest 钉 URL 下载(首跑需网络);sha256 恒校验 manifest 钉值(镜像/
    缓存绕不过校验,与壳安装链同一条铁律)。"""
    entry = _manifest_entry()
    cache = CACHE_ROOT / "runtime" / f"cpython-{HOST_TRIPLE}.tar.gz"
    if not cache.is_file():
        cache.parent.mkdir(parents=True, exist_ok=True)
        part = cache.with_suffix(".tar.gz.part")
        try:
            with urllib.request.urlopen(entry["url"], timeout=300) as resp, part.open("wb") as fh:
                shutil.copyfileobj(resp, fh)
        except OSError as exc:
            pytest.skip(f"钉版运行时缓存缺失且下载失败(首跑需网络): {exc}")
        part.rename(cache)
    actual = _sha256_file(cache)
    assert actual == entry["sha256"], (
        f"钉版运行时 sha256 与 manifest 钉值不符: 期望 {entry['sha256']},实得 {actual}"
        f"(缓存 {cache} 损坏?删缓存重跑)"
    )
    return cache


@pytest.fixture(scope="session")
def wheels_dir(pinned_runtime: Path) -> Path:
    """锁版清单 wheels 本地化:钉版 python 自身 ``pip download``(解释器与
    安装目标 ABI 一致);缓存 marker = 锁版清单 sha256,清单变脸自动重下。"""
    out = CACHE_ROOT / "wheels"
    lock_sha = _sha256_file(LOCK_FILE)
    marker = out / ".lock-sha256"
    if (
        marker.is_file()
        and marker.read_text().strip() == lock_sha
        and any(out.glob("*.whl"))
    ):
        return out
    out.mkdir(parents=True, exist_ok=True)
    for stale in out.iterdir():
        shutil.rmtree(stale) if stale.is_dir() else stale.unlink()
    with tempfile.TemporaryDirectory(prefix="pyenv-e2e-dl-") as tmp:
        # 解压用系统 tar(与壳安装链 flate2/tar 等价的 install_only 布局)。
        subprocess.run(
            ["tar", "-xzf", str(pinned_runtime), "-C", tmp], check=True, timeout=300
        )
        python_bin = Path(tmp) / "python" / "bin" / "python3"
        assert python_bin.is_file(), "钉版归档布局异常:缺 python/bin/python3"
        result = subprocess.run(
            [
                python_bin,
                "-m",
                "pip",
                "download",
                "--no-input",
                "--disable-pip-version-check",
                "--no-deps",
                "-r",
                str(LOCK_FILE),
                "-d",
                str(out),
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.returncode != 0:
            pytest.skip(
                "锁版 wheels 缓存缺失且 pip download 失败(首跑需网络): "
                f"{result.stderr[-800:]}"
            )
        # 构建后端本地化(10-06-telegram-telethon B4):锁版清单自此含
        # sdist-only 件(pyaes —— telethon 闭包,PyPI 无轮),pip 装它走
        # build isolation 要在**本索引**里解 setuptools/wheel(隔离子进程
        # 与主进程同 --index-url)。不种这对轮,sdist 构建在离线沙箱必炸
        # (实测 2026-10-08:Could not find setuptools>=40.8.0)。
        result = subprocess.run(
            [
                python_bin,
                "-m",
                "pip",
                "download",
                "--no-input",
                "--disable-pip-version-check",
                "--no-deps",
                "setuptools",
                "wheel",
                "-d",
                str(out),
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )
        if result.returncode != 0:
            pytest.skip(
                "构建后端 wheels(setuptools/wheel,sdist-only 锁件的构建前提)"
                f"缓存缺失且 pip download 失败(首跑需网络): {result.stderr[-800:]}"
            )
    marker.write_text(lock_sha + "\n")
    return out


# ---------------------------------------------------------------------------
# 夹具:壳 debug 二进制 + 随包 resources 就位
# ---------------------------------------------------------------------------


def _sync_resources(resource_dir: Path) -> None:
    """复刻 tauri CLI 的 resources 拷贝(直跑 cargo 产物不经 CLI,resources
    须测试自持):按 tauri.conf bundle.resources 映射,源(相对 src-tauri/)→
    dest(相对 resource_dir);dest 先清再拷,目录排除 __pycache__(缓存树
    不进资源,防陈旧 pyc 干扰)。"""
    conf = json.loads(TAURI_CONF.read_text())
    mapping = conf["bundle"]["resources"]
    assert isinstance(mapping, dict), "resources 映射形态漂移(map → glob?)"
    for src_rel, dest_rel in mapping.items():
        src = (SRC_TAURI / src_rel).resolve()
        assert src.exists(), f"tauri.conf resources 源缺位: {src}"
        dest = resource_dir / dest_rel
        if dest.is_dir():
            shutil.rmtree(dest)
        elif dest.exists():
            dest.unlink()
        if src.is_dir():
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__"))
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)


@pytest.fixture(scope="session")
def shell_paths(pinned_runtime: Path) -> tuple[Path, Path]:
    """cargo build debug 壳 + resources 就位;返回 (二进制, resource_dir)。
    resource_dir = target/debug(debug 直跑非 bundle,tauri resource_dir 解析
    为 exe 所在目录——本仓实况已证,见 target/debug 下既有 resources 结构)。"""
    subprocess.run(
        ["cargo", "build", "--manifest-path", str(SRC_TAURI / "Cargo.toml")],
        check=True,
        timeout=1800,
    )
    exe = SRC_TAURI / "target" / "debug" / "myssia-desktop"
    assert exe.is_file(), f"debug 壳二进制缺位: {exe}"
    resource_dir = SRC_TAURI / "target" / "debug"
    _sync_resources(resource_dir)
    return exe, resource_dir


# ---------------------------------------------------------------------------
# 本地静态服务器:钉版 runtime + PEP 503 simple 索引(记账可断言)
# ---------------------------------------------------------------------------


class _Recording:
    """线程安全请求记账(断言「索引覆盖生效/不重下」用)。"""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counts: Counter[str] = Counter()

    def hit(self, key: str) -> None:
        with self._lock:
            self._counts[key] += 1

    def get(self, key: str) -> int:
        with self._lock:
            return self._counts[key]


_WHEEL_NAME_RE = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._]*?)-\d.*\.(?:whl|tar\.gz|zip)$")


def _wheel_groups(wheels: Path) -> dict[str, list[str]]:
    """wheels 目录 → {PEP503 规范包名: [文件名]}(钉版清单全 wheel,本归组
    兼容 sdist 文件名以防将来清单变脸)。"""
    groups: dict[str, list[str]] = {}
    for f in sorted(wheels.iterdir()):
        if f.name.startswith("."):
            continue
        match = _WHEEL_NAME_RE.match(f.name)
        assert match, f"wheels 缓存文件名不可解析: {f.name}"
        canon = re.sub(r"[-_.]+", "-", match.group(1)).lower()
        groups.setdefault(canon, []).append(f.name)
    return groups


class _LocalServer:
    """本地静态服务器:/runtime.tar.gz(钉版真件)+ /simple/<pkg>/(PEP 503
    HTML)+ /wheels/<file>;pip 24.x 对 localhost http 索引免 trusted-host
    (实测),与壳 run_pip 只透传 --index-url 的 argv 形态一致。"""

    def __init__(self, runtime: Path, wheels: Path) -> None:
        self._runtime = runtime
        self._wheels = wheels
        self._groups = _wheel_groups(wheels)
        self.recording = _Recording()
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def _send(self, status: int, body: bytes, content_type: str) -> None:
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self) -> None:  # http.server 大小写约定
                path = self.path.split("?")[0]
                if path == "/runtime.tar.gz":
                    outer.recording.hit("runtime")
                    self._send(200, outer._runtime.read_bytes(), "application/gzip")
                elif path.rstrip("/") == "/simple":
                    outer.recording.hit("simple-root")
                    links = "".join(
                        f'<a href="/simple/{escape(pkg)}/">{escape(pkg)}</a><br/>\n'
                        for pkg in sorted(outer._groups)
                    )
                    self._send(
                        200,
                        f"<!DOCTYPE html><html><body>\n{links}</body></html>".encode(),
                        "text/html",
                    )
                elif path.startswith("/simple/"):
                    pkg = path[len("/simple/") :].strip("/")
                    files = outer._groups.get(pkg)
                    if files is None:
                        outer.recording.hit("404")
                        self._send(404, b"no such package", "text/plain")
                        return
                    outer.recording.hit("simple-package")
                    links = "".join(
                        f'<a href="/wheels/{escape(name)}">{escape(name)}</a><br/>\n'
                        for name in files
                    )
                    self._send(
                        200,
                        f"<!DOCTYPE html><html><body>\n{links}</body></html>".encode(),
                        "text/html",
                    )
                elif path.startswith("/wheels/"):
                    name = path[len("/wheels/") :]
                    target = outer._wheels / name
                    if not target.is_file():
                        outer.recording.hit("404")
                        self._send(404, b"no such file", "text/plain")
                        return
                    outer.recording.hit("wheel-file")
                    self._send(200, target.read_bytes(), "application/octet-stream")
                else:
                    outer.recording.hit("404")
                    self._send(404, b"not found", "text/plain")

            def log_message(self, *args: object) -> None:  # 静音默认访问日志
                return

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    @property
    def port(self) -> int:
        return self._server.server_address[1]

    def runtime_url(self) -> str:
        return f"http://127.0.0.1:{self.port}/runtime.tar.gz"

    def pypi_index_url(self) -> str:
        return f"http://127.0.0.1:{self.port}/simple"

    def close(self) -> None:
        self._server.shutdown()
        self._server.server_close()


@pytest.fixture()
def local_server(pinned_runtime: Path, wheels_dir: Path):
    server = _LocalServer(pinned_runtime, wheels_dir)
    yield server
    server.close()


# ---------------------------------------------------------------------------
# 壳驱动与观察
# ---------------------------------------------------------------------------


def _start_shell(
    exe: Path, sandbox: Path, server: _LocalServer, mode: str, log_path: Path
) -> subprocess.Popen:
    """预写双镜像覆盖(pyenv-settings.json,与设置页 IPC 同一落盘文件)指向
    本地静态服务器,以 MYIA_PYENV_AUTOSETUP 冒烟钩子拉起安装链(替用户点
    「开始配置」,产品行为不变)。独立进程组便于整组收尾。"""
    sandbox.mkdir(parents=True, exist_ok=True)
    settings = {
        "mirror_runtime": server.runtime_url(),
        "mirror_pypi": server.pypi_index_url(),
    }
    (sandbox / "pyenv-settings.json").write_text(json.dumps(settings, indent=2))
    env = os.environ.copy()
    env["MYIA_HOME"] = str(sandbox)
    env["MYIA_PYENV_AUTOSETUP"] = mode
    log = log_path.open("wb")
    proc = subprocess.Popen(
        [str(exe)],
        env=env,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    proc._e2e_log_handle = log  # type: ignore[attr-defined] 收尾统一关
    return proc


def _shell_log_tail(log_path: Path, limit: int = 3000) -> str:
    try:
        return log_path.read_text(errors="replace")[-limit:]
    except OSError:
        return "<壳日志不可读>"


def _wait_stamp_state(
    sandbox: Path,
    expected: str,
    timeout: float,
    log_path: Path,
    require_transition: bool = False,
) -> dict:
    """轮询安装链进度戳(python-env.json)至终态;error 即失败并带壳日志尾。

    ``require_transition``:重跑场景必须先观察到「相对基线变化的新戳」才认
    终态——上一轮的 ready 旧戳在新链落首戳之前仍在盘上,只看 state 会假就绪
    (新链初始戳 steps 即携带 skipped 判定,内容必异于旧终戳)。
    """
    stamp_path = sandbox / "python-env.json"
    baseline = stamp_path.read_text() if (require_transition and stamp_path.is_file()) else None
    deadline = time.monotonic() + timeout
    last: dict | None = None
    while time.monotonic() < deadline:
        if stamp_path.is_file():
            try:
                text = stamp_path.read_text()
                stamp = json.loads(text)
            except (OSError, json.JSONDecodeError):
                stamp = None
                text = None
            if isinstance(stamp, dict):
                last = stamp
                if baseline is not None and text == baseline:
                    time.sleep(2)
                    continue  # 仍是上一轮旧戳
                state = stamp.get("state")
                if state == expected:
                    return stamp
                if state == "error":
                    pytest.fail(
                        f"安装链终态 error(期望 {expected}): {json.dumps(stamp, ensure_ascii=False)}\n"
                        f"壳日志尾:\n{_shell_log_tail(log_path)}"
                    )
        time.sleep(2)
    pytest.fail(
        f"等待安装链 state={expected} 超时({timeout:.0f}s);最后戳: {json.dumps(last, ensure_ascii=False)}\n"
        f"壳日志尾:\n{_shell_log_tail(log_path)}"
    )


def _find_serve_pids(sandbox: Path) -> list[int]:
    """找「本沙箱」的常驻 sidecar 进程(壳 spawn 的
    ``python3 -m myssia_desktop_entry serve``):按 MYIA_HOME env 过滤,绝不
    误伤用户真机在跑的 MYIA 实例。"""
    result = subprocess.run(
        ["pgrep", "-f", "myssia_desktop_entry serve"],
        capture_output=True,
        text=True,
    )
    pids: list[int] = []
    for token in result.stdout.split():
        pid = int(token)
        info = subprocess.run(
            ["ps", "eww", "-o", "command=", "-p", str(pid)],
            capture_output=True,
            text=True,
        ).stdout
        if str(sandbox) in info:
            pids.append(pid)
    return pids


def _stop_shell(proc: subprocess.Popen, timeout: float = 15) -> None:
    """整组收尾(壳 + 其 spawn 的 sidecar 同组;tauri-plugin-shell 子进程继承
    进程组);SIGTERM 宽限后 SIGKILL 兜底。"""
    handle = getattr(proc, "_e2e_log_handle", None)
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        pass
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        proc.wait(timeout=timeout)
    if handle is not None:
        handle.close()


def _kill_sandbox_serves(sandbox: Path) -> None:
    """兜底清沙箱 serve 孤儿(壳被 SIGKILL 时 plugin-shell 子进程可能残留)。"""
    for pid in _find_serve_pids(sandbox):
        try:
            os.kill(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass


def _pip_list(python_bin: Path) -> dict[str, str]:
    """沙箱自管 python 的已装清单(name → version;大小写归一)。"""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    result = subprocess.run(
        [python_bin, "-m", "pip", "list", "--format=json"],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )
    assert result.returncode == 0, f"pip list 失败: {result.stderr[-800:]}"
    rows = json.loads(result.stdout)
    return {row["name"].lower().replace("_", "-"): row["version"] for row in rows}


class ServeClient:
    """常驻 serve 进程的逐行 RPC 客户端(与壳侧 sidecar 协议同一条线:
    请求行 {"id","method","params"} → 应答行 {"id","result"};EOF → 干净退出)。

    与壳内常驻 sidecar 同源 argv/env(自管 python -m myssia_desktop_entry
    serve + PYTHONPATH=随包源码 + MYIA_HOME=沙箱),验证「全功能」落在与
    壳完全相同的二进制与数据根上(壳 IPC 应答不经外部,此为等价观察面)。
    """

    def __init__(self, python_bin: Path, sandbox: Path, resource_dir: Path) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(resource_dir / "myssia-src")
        env["MYIA_HOME"] = str(sandbox)
        env["MYIA_APP_VERSION"] = "0.0.1"
        self._stderr = tempfile.TemporaryFile(mode="w+b")
        self.proc = subprocess.Popen(
            [python_bin, "-m", "myssia_desktop_entry", "serve"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self._stderr,
            text=True,
            env=env,
        )
        self._lines: queue.Queue[str | None] = queue.Queue()
        threading.Thread(target=self._reader, daemon=True).start()

    def _reader(self) -> None:
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            self._lines.put(line)
        self._lines.put(None)

    def _stderr_tail(self) -> str:
        self._stderr.seek(0)
        return self._stderr.read().decode(errors="replace")[-1500:]

    def call(self, request_id: int, method: str, params: dict | None = None) -> dict:
        assert self.proc.stdin is not None
        self.proc.stdin.write(
            json.dumps({"id": request_id, "method": method, "params": params or {}}) + "\n"
        )
        self.proc.stdin.flush()
        try:
            line = self._lines.get(timeout=90)
        except queue.Empty as exc:
            raise AssertionError(f"{method} 应答超时;stderr 尾:\n{self._stderr_tail()}") from exc
        assert line, f"{method} 无应答即退出;stderr 尾:\n{self._stderr_tail()}"
        reply = json.loads(line)
        assert "error" not in reply, f"{method} 报错: {reply}"
        assert reply.get("id") == request_id
        result = reply.get("result")
        assert isinstance(result, dict), f"{method} 应答 result 形态异常: {reply}"
        return result

    def close(self) -> None:
        """EOF → serve 干净退出契约(entry.py serve 循环);退出码 0。"""
        assert self.proc.stdin is not None
        self.proc.stdin.close()
        try:
            code = self.proc.wait(timeout=60)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=30)
            raise AssertionError(f"serve 未随 EOF 退出;stderr 尾:\n{self._stderr_tail()}")
        finally:
            self._stderr.close()
        assert code == 0, f"serve 退出码 {code};stderr 尾已随上文的失败信息输出"


# ---------------------------------------------------------------------------
# 测试:AC1 主链 + AC4 幂等二跑
# ---------------------------------------------------------------------------


def test_fresh_sandbox_full_chain(
    tmp_path: Path,
    shell_paths: tuple[Path, Path],
    local_server: _LocalServer,
) -> None:
    """AC1 主链(全新沙箱数据根,MYIA_HOME 隔离):下载钉版运行时(本地静态
    服务器真件)→ sha256 校验 → 解压数据根 → pip 锁版装(本地 PyPI 索引,
    覆盖生效)→ 自检 version ping(壳内)→ ready 戳 → sidecar 自动拉起 →
    全功能 RPC 冒烟。"""
    exe, resource_dir = shell_paths
    sandbox = tmp_path / "home"
    log_path = tmp_path / "shell.log"
    entry = _manifest_entry()
    proc = _start_shell(exe, sandbox, local_server, mode="1", log_path=log_path)
    try:
        stamp = _wait_stamp_state(sandbox, "ready", CHAIN_TIMEOUT, log_path)

        # 五阶段全 done(AC1 主链逐段:下载→校验→解压→装→自检)。
        statuses = {step["phase"]: step["status"] for step in stamp["steps"]}
        assert [
            statuses[phase]
            for phase in (
                "downloading",
                "verifying",
                "extracting",
                "installing_deps",
                "selfcheck",
            )
        ] == ["done"] * 5, f"五阶段步进: {stamp['steps']}"

        # 依赖指纹 = 随包锁版清单 sha256(壳读 resource_dir 拷贝件,与本测试
        # 的桌面源文件同内容——_sync_resources 刚同步)。
        assert stamp["deps_fingerprint"] == _sha256_file(resource_dir / "requirements-lock.txt")

        # 真钉版运行时就位:python 可执行、版本恰 3.12.7(D3 钉版)。
        python_bin = sandbox / "python" / "bin" / "python3"
        assert python_bin.is_file(), f"钉版 python 缺位: {python_bin}"
        version = subprocess.run(
            [python_bin, "--version"], capture_output=True, text=True, timeout=60
        )
        assert "Python 3.12.7" in version.stdout, version.stdout

        # pip 锁版装真落沙箱(锁版清单代表包逐版钉死,含 classifier PyPI 钉版)。
        packages = _pip_list(python_bin)
        for name, expected in (
            ("apscheduler", "3.11.3"),
            ("httpx", "0.28.1"),
            ("pydantic", "2.13.5"),
            ("pydantic-core", "2.46.5"),
            ("myssia-classifier", "0.0.1"),
        ):
            assert packages.get(name) == expected, (
                f"锁版依赖 {name}=={expected} 未按钉版装上(实得 {packages.get(name)})"
            )

        # 本地静态服务器记账:运行时恰下载一次;pip 索引解析与 wheel 拉取
        # 全部落在本地镜像(AC3 索引覆盖生效的实证,26 包闭包)。
        assert local_server.recording.get("runtime") == 1, "钉版运行时应恰经本地镜像下载一次"
        assert local_server.recording.get("simple-package") >= 20, (
            "pip 应逐包请求本地 PyPI 索引(索引覆盖生效): "
            f"{local_server.recording.get('simple-package')}"
        )
        assert local_server.recording.get("wheel-file") >= 20, (
            "pip 应从本地镜像拉取 wheel: "
            f"{local_server.recording.get('wheel-file')}"
        )

        # 归档缓存保留且指纹=manifest 钉值(幂等续装基础;坏包即删的对称面)。
        archive = sandbox / "downloads" / f"runtime-{HOST_TRIPLE}.tar.gz"
        assert archive.is_file(), f"运行时归档缓存缺位: {archive}"
        assert _sha256_file(archive) == entry["sha256"]

        # sidecar 自动拉起(遗留 pyenv_install.rs:1033 闭环:安装线程 ready →
        # spawn_sidecar_if_idle → app.shell() 拉真进程;argv 契约含 serve 尾参)。
        deadline = time.monotonic() + SIDECAR_SPAWN_TIMEOUT
        serve_pids: list[int] = []
        while time.monotonic() < deadline:
            serve_pids = _find_serve_pids(sandbox)
            if serve_pids:
                break
            time.sleep(1)
        assert serve_pids, (
            f"安装 ready 后 {SIDECAR_SPAWN_TIMEOUT}s 内未见常驻 sidecar 进程\n"
            f"壳日志尾:\n{_shell_log_tail(log_path)}"
        )

        # 全功能冒烟:同一沙箱 + 同一自管 python + 同一随包源码另起 serve,
        # 逐方法 RPC 往返(源管理/情报流/定时;只读面,写路径涉外网不进离线链)。
        client = ServeClient(python_bin, sandbox, resource_dir)
        try:
            version_result = client.call(1, "version")
            assert version_result["name"] == "myssia"
            assert version_result["protocol"] == 10
            assert version_result["app_version"] == "0.0.1"
            smoke_methods = [
                ("health", 2),  # 源管理:插件清单 + 源健康度聚合
                ("plugins.list", 3),  # 源管理
                ("store.items", 4),  # 情报流:物品库
                ("runs.list", 5),  # 情报流:采集运行记录
                ("logs.tail", 6),  # 情报流:日志
                ("cron.list", 7),  # 定时:任务清单
                ("cron.status", 8),  # 定时:调度器状态
                ("alerts.list", 9),
                ("channels.list", 10),
            ]
            for method, request_id in smoke_methods:
                client.call(request_id, method)
        finally:
            client.close()
    finally:
        _stop_shell(proc)
        _kill_sandbox_serves(sandbox)


def test_force_rerun_idempotent(
    tmp_path: Path,
    shell_paths: tuple[Path, Path],
    pinned_runtime: Path,
    wheels_dir: Path,
) -> None:
    """AC4 幂等(真件二跑):MYIA_PYENV_AUTOSETUP=force 对已 ready 沙箱重跑
    安装链——已装步全 skipped、运行时不重下、pip 已装跳过(不触碰本地索引)、
    自检恒重跑作终门;ready 戳与依赖指纹不变。"""
    exe, resource_dir = shell_paths
    sandbox = tmp_path / "home"

    # 第一轮:全新沙箱走完整主链至 ready。
    first_server = _LocalServer(pinned_runtime, wheels_dir)
    first_log = tmp_path / "shell-first.log"
    proc = _start_shell(exe, sandbox, first_server, mode="1", log_path=first_log)
    try:
        first_stamp = _wait_stamp_state(sandbox, "ready", CHAIN_TIMEOUT, first_log)
    finally:
        _stop_shell(proc)
        _kill_sandbox_serves(sandbox)
    first_server.close()
    fingerprint = first_stamp["deps_fingerprint"]

    # 第二轮:force 重跑(新服务器实例,记账从零起——只观察本轮网络面)。
    second_server = _LocalServer(pinned_runtime, wheels_dir)
    second_log = tmp_path / "shell-second.log"
    proc = _start_shell(exe, sandbox, second_server, mode="force", log_path=second_log)
    try:
        stamp = _wait_stamp_state(
            sandbox, "ready", RERUN_TIMEOUT, second_log, require_transition=True
        )

        statuses = {step["phase"]: step["status"] for step in stamp["steps"]}
        assert [
            statuses[phase]
            for phase in (
                "downloading",
                "verifying",
                "extracting",
                "installing_deps",
                "selfcheck",
            )
        ] == ["skipped", "skipped", "skipped", "skipped", "done"], (
            f"幂等二跑步进(前四步应 skipped,自检恒重跑): {stamp['steps']}"
        )
        # 已装步零网络面:运行时不重下、pip 已装跳过(不解析索引、不拉 wheel)。
        assert second_server.recording.get("runtime") == 0, "幂等二跑不得重下运行时"
        assert second_server.recording.get("simple-package") == 0, (
            "pip 已装跳过不得触碰索引(Requirement already satisfied 不查 index): "
            f"{second_server.recording.get('simple-package')}"
        )
        assert second_server.recording.get("wheel-file") == 0, "幂等二跑不得重拉 wheel"
        # ready 戳与依赖指纹不变(重跑结果一致,AC4)。
        assert stamp["deps_fingerprint"] == fingerprint
        assert (sandbox / "python" / "bin" / "python3").is_file()
    finally:
        _stop_shell(proc)
        _kill_sandbox_serves(sandbox)
    second_server.close()
