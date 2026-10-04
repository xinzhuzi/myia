"""打包链退役守卫(10-05-desktop-managed-py-env implement.md 第 7 条)。

第 1 步已把随包交付物铺进 tauri resources(externalBin 当时未动,退役归本步);
本文件钉死退役态,防打包链回退/复活死链(全部离线,零外网、零构建):

1. ``tauri.conf.json``:``bundle.externalBin`` 已移除;``beforeBuildCommand``
   不再拉 sidecar 构建,且先清随包源码树 ``__pycache__`` 再 vite 构建
   (第 1 步遗留裁量:resources map 形目录映射无排除语义,gitignored 字节码
   缓存会被原样打进包体)。
2. ``desktop/package.json``:``sidecar`` 脚本已退役,``clean:pycache`` 在位。
3. CI 面:``ci.yml`` / ``desktop-release.yml`` 无 build-sidecar / MYIA_SIDECAR_SKIP
   / externalBin 占位步骤(发版流水线与 rust-check 门不再依赖死链)。
4. ``desktop/build-sidecar.sh``:档注保留 + 执行即拒(退出非 0 且带退役说明,
   误用者得到的是指引不是 118MiB 冻结二进制)。
5. ``desktop/scripts/clean-pycache.mjs``:真跑——临时树内嵌套 ``__pycache__``
   与 ``.DS_Store`` 全清、正常文件原样(跨平台 node 实现,不依赖 ``find``)。
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
DESKTOP = REPO_ROOT / "desktop"
SRC_TAURI = DESKTOP / "src-tauri"
TAURI_CONF = SRC_TAURI / "tauri.conf.json"
PACKAGE_JSON = DESKTOP / "package.json"
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"
BUILD_SIDECAR = DESKTOP / "build-sidecar.sh"
CLEAN_PYCACHE = DESKTOP / "scripts" / "clean-pycache.mjs"


def _conf() -> dict:
    return json.loads(TAURI_CONF.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# 1. tauri.conf.json:externalBin 退役 + beforeBuildCommand 去 sidecar
# ---------------------------------------------------------------------------


def test_externalbin_retired() -> None:
    """bundle.externalBin 已移除:壳不再消费冻结 sidecar 二进制(tauri-build
    对 gitignored binaries/ 的存在性校验随之消失,ci.yml 占位步已同步退役)。"""
    bundle = _conf()["bundle"]
    assert "externalBin" not in bundle, (
        "bundle.externalBin 应已移除(10-05 第 7 步):Python 面随 resources 交付,"
        "冻结 sidecar 二进制不再进包"
    )


def test_before_build_command_no_sidecar_and_cleans_pycache() -> None:
    """beforeBuildCommand:无 sidecar 段;先 clean:pycache(resources 无排除语义,
    第 1 步遗留裁量落地)再 npm run build(vite)。"""
    cmd = _conf()["build"]["beforeBuildCommand"]
    assert "sidecar" not in cmd, f"beforeBuildCommand 仍引用 sidecar 链: {cmd!r}"
    assert cmd == "npm run clean:pycache && npm run build", (
        f"beforeBuildCommand 应为清理+前端构建链,实得: {cmd!r}"
    )


def test_pyenv_resources_still_mapped() -> None:
    """externalBin 退役不挤掉自管环境五映射(第 1 步交付面原样)。"""
    resources = _conf()["bundle"]["resources"]
    for source, dest in {
        "../../src/myssia": "myssia-src/myssia",
        "../entry.py": "myssia-src/entry.py",
        "../myssia_desktop_entry": "myssia-src/myssia_desktop_entry",
        "../resources/runtime-manifest.json": "runtime-manifest.json",
        "../resources/requirements-lock.txt": "requirements-lock.txt",
    }.items():
        assert resources.get(source) == dest, f"resources 缺映射 {source!r} -> {dest!r}"


# ---------------------------------------------------------------------------
# 2. desktop/package.json:sidecar 脚本退役 + clean:pycache 在位
# ---------------------------------------------------------------------------


def test_package_json_scripts() -> None:
    scripts = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))["scripts"]
    assert "sidecar" not in scripts, "npm run sidecar 已退役(死链入口应移除)"
    assert scripts.get("clean:pycache") == "node scripts/clean-pycache.mjs"


# ---------------------------------------------------------------------------
# 3. CI 面: workflows 无 sidecar 链
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "workflow",
    ["ci.yml", "desktop-release.yml"],
)
def test_workflows_sidecar_chain_retired(workflow: str) -> None:
    """发版流水线与 rust-check 门零 sidecar 链执行引用(死链复活会在此红,
    而不是在发版日)。注:头注里的「desktop/build-sidecar.sh 档注」是退役说明,
    不是执行——needle 取执行形(``bash build-sidecar.sh``)而非裸文件名。"""
    text = (WORKFLOWS_DIR / workflow).read_text(encoding="utf-8")
    for needle in ("bash build-sidecar.sh", "MYIA_SIDECAR_SKIP", "placeholder externalBin"):
        assert needle not in text, f"{workflow} 仍引用已退役打包链: {needle!r}"


# ---------------------------------------------------------------------------
# 4. build-sidecar.sh:档注保留 + 执行即拒
# ---------------------------------------------------------------------------


def test_build_sidecar_script_retired_marker() -> None:
    """档注保留(design §2):退役说明指向自管环境替代链与回滚口径。"""
    text = BUILD_SIDECAR.read_text(encoding="utf-8")
    assert "已退役" in text and "10-05-desktop-managed-py-env" in text


def test_build_sidecar_script_refuses_to_run() -> None:
    """执行即拒:退出非 0 且 stderr 带退役说明(防误产出无消费方的冻结二进制)。"""
    proc = subprocess.run(
        ["bash", str(BUILD_SIDECAR)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert proc.returncode != 0, "退役脚本执行应失败,不得静默产出 sidecar"
    assert "已退役" in proc.stderr


# ---------------------------------------------------------------------------
# 5. clean-pycache.mjs:真跑(嵌套缓存 + macOS 元数据垃圾全清,正常文件不动)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(shutil.which("node") is None, reason="本机无 node(tauri CLI 本身依赖 node,正常构建面恒在)")
def test_clean_pycache_script(tmp_path: Path) -> None:
    tree = tmp_path / "tree"
    (tree / "pkg" / "__pycache__").mkdir(parents=True)
    (tree / "pkg" / "__pycache__" / "mod.cpython-312.pyc").write_text("junk", encoding="utf-8")
    (tree / "pkg" / "sub" / "__pycache__").mkdir(parents=True)
    (tree / "pkg" / "sub" / "__pycache__" / "deep.cpython-312.pyc").write_text("junk", encoding="utf-8")
    (tree / "pkg" / ".DS_Store").write_text("junk", encoding="utf-8")
    (tree / "pkg" / "sub" / "keep.py").write_text("print('keep')\n", encoding="utf-8")

    proc = subprocess.run(
        ["node", str(CLEAN_PYCACHE), str(tree)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"clean-pycache 失败: {proc.stderr[-1000:]}"
    # 垃圾全清(嵌套两处 __pycache__ + .DS_Store = 3 条)。
    assert not list(tree.rglob("__pycache__")), "__pycache__ 残留"
    assert not list(tree.rglob(".DS_Store")), ".DS_Store 残留"
    # 正常文件原样。
    assert (tree / "pkg" / "sub" / "keep.py").read_text(encoding="utf-8") == "print('keep')\n"
    assert "3" in proc.stdout, f"清理计数应=3: {proc.stdout!r}"


@pytest.mark.skipif(shutil.which("node") is None, reason="本机无 node(tauri CLI 本身依赖 node,正常构建面恒在)")
def test_clean_pycache_script_idempotent_on_missing_root(tmp_path: Path) -> None:
    """幂等 + 容错:目标目录不存在时静默通过(CI 干净检出台面即此态)。"""
    proc = subprocess.run(
        ["node", str(CLEAN_PYCACHE), str(tmp_path / "nope")],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, f"缺省根不存在应静默通过: {proc.stderr[-1000:]}"
    assert "0" in proc.stdout


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-q"]))
