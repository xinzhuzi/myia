"""随包交付物清单一致性(10-05-desktop-managed-py-env implement.md 第 1 条门)。

覆盖四件事(全部离线,零外网):

1. ``tauri.conf.json`` resources 段:自管环境五映射已声明且源路径磁盘实况
   存在;既有官方插件种子映射(首跑种子依赖)不被挤掉。
2. ``desktop/resources/runtime-manifest.json``:钉版=主人 D3 原文 URL(mac)+
   同 release Windows 等效件;sha256 为实算入盘的 64 位小写 hex;解压布局
   (install_only 根目录 ``python/`` 与平台 python_bin)自洽。
3. ``desktop/resources/requirements-lock.txt`` 与 pyproject dependencies 一致:
   每个直接依赖都有 ``name==version`` 钉版行且满足 pyproject 约束;无
   editable/路径依赖(桌面环境 pip 一律走 PyPI);classifier 的 PyPI 钉版
   (唯一手改行)单独把守。
4. 入口包 ``desktop/myssia_desktop_entry``:importlib 复用 ``entry.py`` 协议面
   (方法集/serve/直通零漂移),真进程冒烟 ``python -m myssia_desktop_entry``
   serve version 往返与 ``--version`` 直通退出码。
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

REPO_ROOT = Path(__file__).resolve().parents[2]
DESKTOP = REPO_ROOT / "desktop"
SRC_TAURI = DESKTOP / "src-tauri"
RESOURCES_DIR = DESKTOP / "resources"
TAURI_CONF = SRC_TAURI / "tauri.conf.json"

#: D3 主人钉定原文(PRD 决议 2026-10-05;一字不改)。
D3_MAC_URL = (
    "https://github.com/indygreg/python-build-standalone/releases/download/20241016/"
    "cpython-3.12.7+20241016-aarch64-apple-darwin-install_only.tar.gz"
)
#: 同 release Windows 等效件(D3:取 20241016 的 x86_64-pc-windows-msvc)。
WIN_URL = (
    "https://github.com/indygreg/python-build-standalone/releases/download/20241016/"
    "cpython-3.12.7+20241016-x86_64-pc-windows-msvc-install_only.tar.gz"
)

#: 自管环境随包映射(tauri.conf.json resources 源 → 目标;源路径相对 src-tauri/)。
PYENV_RESOURCE_MAP = {
    "../../src/myssia": "myssia-src/myssia",
    "../entry.py": "myssia-src/entry.py",
    "../myssia_desktop_entry": "myssia-src/myssia_desktop_entry",
    "../resources/runtime-manifest.json": "runtime-manifest.json",
    "../resources/requirements-lock.txt": "requirements-lock.txt",
}

#: 既有官方插件种子映射(首跑种子依赖,design.md §2 之前的既定面)。
SEED_RESOURCE_MAP = {
    "../fixture/plugin.yaml": "plugin.yaml",
    "../../plugins/ai-news.yaml": "plugins/ai-news.yaml",
    "../../plugins/wool.yaml": "plugins/wool.yaml",
    "../../plugins/stocks.yaml": "plugins/stocks.yaml",
    "../../plugins/gpu-prices.yaml": "plugins/gpu-prices.yaml",
    "../../plugins/myssia-demo.yaml": "plugins/myssia-demo.yaml",
}

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _pep503(name: str) -> str:
    """PEP 503 规范名(大小写与 ``-``/``_``/``.`` 分隔归一)。"""
    return re.sub(r"[-_.]+", "-", name).lower()


# ---------------------------------------------------------------------------
# 1. tauri.conf.json resources 段:声明 + 磁盘实况
# ---------------------------------------------------------------------------


def _conf_resources() -> dict[str, str]:
    conf = json.loads(TAURI_CONF.read_text(encoding="utf-8"))
    resources = conf["bundle"]["resources"]
    assert isinstance(resources, dict), "resources 段须为 map 形(目录映射需要 map 语义)"
    return resources


@pytest.mark.parametrize("source,dest", sorted(PYENV_RESOURCE_MAP.items()))
def test_pyenv_resources_declared_and_present(source: str, dest: str) -> None:
    """五映射逐条:已按预期目标声明,且源路径在磁盘实况存在(目录/文件形态对)。"""
    resources = _conf_resources()
    assert resources.get(source) == dest, f"resources 缺映射 {source!r} -> {dest!r}(实得 {resources.get(source)!r})"
    path = (SRC_TAURI / source).resolve()
    assert path.exists(), f"映射源不存在: {source} -> {path}"
    if path.is_dir():
        assert (path / "__init__.py").is_file(), f"映射源目录不是包: {path}"


def test_myssia_resource_tree_shape() -> None:
    """随包源码树核心件:myssia 包可 -m 起(CLI 入口在)+ 入口包双件齐全。"""
    assert (REPO_ROOT / "src" / "myssia" / "__init__.py").is_file()
    assert (REPO_ROOT / "src" / "myssia" / "cli.py").is_file()
    entry_pkg = DESKTOP / "myssia_desktop_entry"
    assert (entry_pkg / "__init__.py").is_file()
    assert (entry_pkg / "__main__.py").is_file()
    assert (DESKTOP / "entry.py").is_file()


@pytest.mark.parametrize("source,dest", sorted(SEED_RESOURCE_MAP.items()))
def test_seed_resources_untouched(source: str, dest: str) -> None:
    """官方插件种子映射保持(首跑种子 _bundle_plugins_dir 依赖;不被重排挤掉)。"""
    assert _conf_resources().get(source) == dest


# ---------------------------------------------------------------------------
# 2. runtime-manifest.json:钉版 URL + 实算 sha256 + 解压布局
# ---------------------------------------------------------------------------


def _manifest() -> dict:
    data = json.loads((RESOURCES_DIR / "runtime-manifest.json").read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def test_runtime_manifest_shape_and_pins() -> None:
    """manifest 骨架 + 双平台钉版:URL 与 D3 原文逐字节一致,release 全局一致。"""
    data = _manifest()
    assert data["manifest_version"] == 1
    runtime = data["runtime"]
    assert runtime["name"] == "cpython"
    assert runtime["version"] == "3.12.7"
    assert runtime["release_tag"] == "20241016"
    assert runtime["distribution"] == "indygreg/python-build-standalone"
    assert runtime["install_kind"] == "install_only"
    platforms = data["platforms"]
    # D3:mac 当前只发 aarch64(与现行 dmg 单架构一致);win 取 x86_64 等效件。
    assert set(platforms) == {"aarch64-apple-darwin", "x86_64-pc-windows-msvc"}
    assert platforms["aarch64-apple-darwin"]["url"] == D3_MAC_URL
    assert platforms["x86_64-pc-windows-msvc"]["url"] == WIN_URL
    for key, entry in platforms.items():
        # URL 文件名与平台键/release 元数据三方自洽(镜像覆盖只换 URL,不换钉版语义)。
        expected_file = f"cpython-3.12.7+20241016-{key}-install_only.tar.gz"
        assert entry["url"].rsplit("/", 1)[-1] == expected_file
        assert f"/download/20241016/{expected_file}" in entry["url"]


def test_runtime_manifest_sha256_format() -> None:
    """sha256 = 实算入盘的 64 位小写 hex;两平台指纹互异(非复制粘贴产物)。"""
    entries = _manifest()["platforms"]
    digests = set()
    for key, entry in entries.items():
        digest = entry["sha256"]
        assert _SHA256_RE.match(digest), f"{key}.sha256 非小写 64 位 hex: {digest!r}"
        digests.add(digest)
    assert len(digests) == len(entries), "两平台 sha256 相同:疑似未实算"


def test_runtime_manifest_extract_layout() -> None:
    """解压布局自洽:install_only 根目录 python/;python_bin 落其下且平台正确。"""
    entries = _manifest()["platforms"]
    expected_bins = {
        "aarch64-apple-darwin": "python/bin/python3",
        "x86_64-pc-windows-msvc": "python/python.exe",
    }
    for key, entry in entries.items():
        assert entry["archive"] == "tar.gz"
        assert entry["extract_root_dir"] == "python", f"{key}: install_only 应解压出 python/ 根目录"
        assert entry["python_bin"] == expected_bins[key]
        assert entry["python_bin"].startswith(entry["extract_root_dir"] + "/")


# ---------------------------------------------------------------------------
# 3. requirements-lock.txt ↔ pyproject dependencies 一致性
# ---------------------------------------------------------------------------


def _lock_pins() -> dict[str, str]:
    """解析锁版清单:仅取 ``name==version`` 顶格行(注释/续行/标记剥掉)。"""
    pins: dict[str, str] = {}
    for raw in (RESOURCES_DIR / "requirements-lock.txt").read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        assert not line.startswith("-e") and "file:" not in line and "://" not in line, (
            f"桌面锁版清单不得含 editable/路径/URL 依赖: {raw!r}"
        )
        pinned = line.split(";", 1)[0].strip()
        name, sep, version = pinned.partition("==")
        assert sep, f"非钉版行(须 name==version): {raw!r}"
        pins[_pep503(name.strip())] = version.strip()
    return pins


def test_requirements_lock_covers_pyproject_dependencies() -> None:
    """pyproject 每条直接依赖:锁版清单有钉版行,且版本满足约束(锁=约束的冻结)。"""
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    deps = pyproject["project"]["dependencies"]
    pins = _lock_pins()
    missing = []
    for dep in deps:
        req = Requirement(dep)  # 解析 extras/markers/约束(httpx[socks]>=0.27 等)
        pinned = pins.get(_pep503(req.name))
        if pinned is None:
            missing.append(req.name)
            continue
        assert SpecifierSet(str(req.specifier)).contains(pinned), (
            f"{req.name} 钉版 {pinned} 不满足 pyproject 约束 {req.specifier}"
        )
    assert not missing, f"锁版清单缺直接依赖: {sorted(missing)}"
    # 自管环境装的是随包源码,清单不钉 myssia 自身(也不该有 dev 工具)。
    assert "myssia" not in pins
    assert "pytest" not in pins


def test_requirements_lock_classifier_pypi_pin() -> None:
    """唯一手改行把守:workspace 成员 myssia-classifier 必须钉 PyPI 版(可解析)。"""
    pins = _lock_pins()
    assert pins.get("myssia-classifier") == "0.0.1", (
        "myssia-classifier 应钉 PyPI 版 0.0.1(uv.lock 解析版本;editable 行会令桌面 pip 装不上)"
    )


# ---------------------------------------------------------------------------
# 4. 入口包:复用 entry.py 协议面 + 真进程冒烟
# ---------------------------------------------------------------------------


def _load_entry_package():
    """以包语义直载 desktop/myssia_desktop_entry(不经 sys.path 全局污染)。"""
    pkg_dir = DESKTOP / "myssia_desktop_entry"
    spec = importlib.util.spec_from_file_location(
        "myssia_desktop_entry", pkg_dir / "__init__.py", submodule_search_locations=[str(pkg_dir)]
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("myssia_desktop_entry", module)
    spec.loader.exec_module(module)
    return module


def _load_entry_direct():
    """与 tests/desktop/test_desktop_sidecar_protocol.py 同手法直载 entry.py。"""
    spec = importlib.util.spec_from_file_location("pyenv_parity_entry", DESKTOP / "entry.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_entry_package_reuses_entry_protocol_surface() -> None:
    """协议面零漂移:装载目标就是 desktop/entry.py,方法集/协议版本与直载一致。"""
    pkg = _load_entry_package()
    assert pkg.ENTRY_PY == DESKTOP / "entry.py", "开发树布局:入口包应定位同目录的 entry.py"
    reused = pkg.load_entry_module()
    direct = _load_entry_direct()
    assert reused.PROTOCOL_VERSION == direct.PROTOCOL_VERSION
    assert sorted(reused._HANDLERS) == sorted(direct._HANDLERS), "方法集漂移:装载目标不是同一 entry.py?"
    assert callable(reused.serve) and callable(reused.cli_main)


def _spawn_env(tmp_path: Path) -> dict[str, str]:
    """真进程环境:PYTHONPATH=入口包+核心源(模拟 Resources/myssia-src)+ 沙箱数据根。"""
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join([str(DESKTOP), str(REPO_ROOT / "src")])
    env["MYIA_HOME"] = str(tmp_path / "home")
    return env


def test_entry_module_serve_version_roundtrip(tmp_path: Path) -> None:
    """真进程冒烟:``python -m myssia_desktop_entry serve`` version 往返,EOF 退出 0。"""
    request = '{"id": 1, "method": "version", "params": {}}\n'
    proc = subprocess.run(
        [sys.executable, "-m", "myssia_desktop_entry", "serve"],
        input=request,
        capture_output=True,
        text=True,
        env=_spawn_env(tmp_path),
        timeout=120,
    )
    assert proc.returncode == 0, f"serve 退出码 {proc.returncode};stderr={proc.stderr[-2000:]}"
    lines = [line for line in proc.stdout.splitlines() if line.strip()]
    assert lines, f"协议流无应答;stderr={proc.stderr[-2000:]}"
    answer = json.loads(lines[0])
    direct = _load_entry_direct()
    assert answer["id"] == 1
    assert answer["result"]["name"] == "myssia"
    assert answer["result"]["protocol"] == direct.PROTOCOL_VERSION


def test_entry_module_cli_passthrough_version(tmp_path: Path) -> None:
    """直通模式契约:``python -m myssia_desktop_entry --version`` = CLI 原样(exit 0)。"""
    proc = subprocess.run(
        [sys.executable, "-m", "myssia_desktop_entry", "--version"],
        capture_output=True,
        text=True,
        env=_spawn_env(tmp_path),
        timeout=120,
    )
    assert proc.returncode == 0, f"--version 退出码 {proc.returncode};stderr={proc.stderr[-2000:]}"
    assert proc.stdout.strip().startswith("myssia "), proc.stdout
