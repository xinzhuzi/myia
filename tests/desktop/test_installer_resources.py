"""装机包 resources 面守卫(10-05-plugin-market-batch AC5,批三)。

钉两件事(全部离线,零外网、零构建):

1. **官方品类全量捆绑**:tauri.conf.json resources 必须含全部 7 个官方
   品类 YAML(README「7 official categories」口径:ai-news/wool/stocks/
   gpu-prices/games/news/exposure)+ demo 件——AC5 挂账根因即「只捆 4/7
   (games/news/exposure 缺)」,补齐后本文件把 7/7 钉死,回退即红。
2. **desktop tier 插件包源码面随包**(AC5 市场面包裁决):desktop 分级
   全件(EXPECTED_TIERS 口径,与 tests/plugins/test_plugin_packages.py
   同源;跨目录不 import,清单漂移由两侧参数化对不上时人工对账)逐件捆
   manifest+README+adapter.py 三件套;myssia-credhunter 额外捆自有
   ``credhunter/`` 子包(adapter compile+exec 自举依赖,漏捆即交付坏件)。
   **刻意不捆**:vendor/ 外来 submodule(GPL Photon / theHarvester,随包
   分发越许可红线;装机上 vendor 缺失走 adapter 既有结构化
   ``vendor_missing`` 指引,tests/plugins/test_osint_plugin.py 等已钉)、
   docker/(服务端件面)、__pycache__(逐文件映射天然排除,断言兜底)。

与 tests/desktop/test_pyenv_resources.py 的分工:彼管自管 Python 环境
五映射 + 种子映射「不被挤掉」;此管 AC5 补齐面(品类 7/7 + 桌面件源码面
+ 排除断言)。两文件都只断「在」,不断「仅有」,互不牵连。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_TAURI = REPO_ROOT / "desktop" / "src-tauri"
TAURI_CONF = SRC_TAURI / "tauri.conf.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

#: 官方 7 品类(README zh/en「7 official categories」口径)+ demo 件;
#: AC5 前 resources 只捆前 4,games/news/exposure 为本批补齐件。
OFFICIAL_CATEGORY_YAMLS = (
    "ai-news.yaml",
    "wool.yaml",
    "stocks.yaml",
    "gpu-prices.yaml",
    "games.yaml",
    "news.yaml",
    "exposure.yaml",
    # demo 件非官方品类,但 v1.1 起随包(既有面,不动)。
    "myssia-demo.yaml",
)

#: desktop tier 插件包全件(EXPECTED_TIERS 同源清单;市场面 AC5 裁决:
#: desktop 件零 docker、进程内/子进程形态,源码面可随包分发)。
DESKTOP_TIER_PACKAGES = (
    "myssia-proxy",
    "myssia-osint",
    "myssia-credhunter",
    "myssia-media",
    "myssia-maigret",
    "myssia-theharvester",
    "myssia-urlwatch",
)

#: 每个桌面件必备的三件套源码面(manifest 规范 + 上游署名文档 + 适配器)。
PACKAGE_SOURCE_FILES = ("plugin.yaml", "README.md", "adapter.py")

#: myssia-credhunter 自有子包(adapter.py compile+exec 自举加载
#: credhunter/*.py 与 data/ 数据文件;零上游复制,可随包)。
CREDHUNTER_SUBPACKAGE = "credhunter"


def _conf_resources() -> dict[str, str]:
    conf = json.loads(TAURI_CONF.read_text(encoding="utf-8"))
    resources = conf["bundle"]["resources"]
    assert isinstance(resources, dict), "resources 段须为 map 形"
    return resources


# ---------------------------------------------------------------------------
# 1. 官方品类 7/7 + demo 全捆
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "yaml_name", [name for name in OFFICIAL_CATEGORY_YAMLS if name != "myssia-demo.yaml"]
)
def test_official_category_yaml_bundled(yaml_name: str) -> None:
    """7 个官方品类逐一:resources 有映射,且映射源在仓库 plugins/ 实况存在。"""
    source = f"../../plugins/{yaml_name}"
    dest = f"plugins/{yaml_name}"
    resources = _conf_resources()
    assert resources.get(source) == dest, (
        f"官方品类未随包捆绑: {source!r} -> {dest!r}(实得 {resources.get(source)!r})"
    )
    assert (SRC_TAURI / source).is_file(), f"映射源不存在: {source}"


def test_demo_yaml_still_bundled() -> None:
    """demo 件维持随包(既有面;官方 7 之外的教程件)。"""
    assert _conf_resources().get("../../plugins/myssia-demo.yaml") == "plugins/myssia-demo.yaml"


# ---------------------------------------------------------------------------
# 2. desktop tier 插件包源码面(三件套 + credhunter 子包)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("package", DESKTOP_TIER_PACKAGES)
@pytest.mark.parametrize("filename", PACKAGE_SOURCE_FILES)
def test_desktop_package_source_file_bundled(package: str, filename: str) -> None:
    """每桌面件 × 三件套:映射在 + 源在盘(manifest 校验由包契约测试另行钉)。"""
    source = f"../../plugins/{package}/{filename}"
    dest = f"plugins/{package}/{filename}"
    resources = _conf_resources()
    assert resources.get(source) == dest, (
        f"desktop 件源码面未随包: {source!r} -> {dest!r}(实得 {resources.get(source)!r})"
    )
    assert (SRC_TAURI / source).is_file(), f"映射源不存在: {source}"


def test_credhunter_subpackage_bundled() -> None:
    """credhunter/ 自有子包随包(adapter 自举依赖;整目录映射)。"""
    source = f"../../plugins/myssia-credhunter/{CREDHUNTER_SUBPACKAGE}"
    dest = f"plugins/myssia-credhunter/{CREDHUNTER_SUBPACKAGE}"
    assert _conf_resources().get(source) == dest
    assert (SRC_TAURI / source).is_dir(), f"映射源目录不存在: {source}"
    # 自举依赖的最小实况:入口模块与数据目录在(缺一则装机件必坏)。
    assert (SRC_TAURI / source / "findings.py").is_file()
    assert (SRC_TAURI / source / "data").is_dir()


# ---------------------------------------------------------------------------
# 3. 排除断言:vendor / docker / __pycache__ 绝不入包
# ---------------------------------------------------------------------------


def test_no_vendor_submodule_bundled() -> None:
    """vendor/ 外来 submodule(GPL Photon / theHarvester)不随包:许可红线。

    装机上 vendor 缺失走 adapter 既有结构化 ``vendor_missing`` 指引
    (tests/plugins/test_osint_plugin.py、test_theharvester_plugin.py 已钉),
    不在 resources 面补。
    """
    resources = _conf_resources()
    vendor_sources = [src for src in resources if "/vendor" in src or src.endswith("/vendor")]
    assert not vendor_sources, f"vendor/ 不得随包分发(许可红线): {vendor_sources}"


def test_no_docker_or_pycache_bundled() -> None:
    """docker/(服务端件面)与 __pycache__ 不得出现在任何映射键里。"""
    resources = _conf_resources()
    offenders = [
        src for src in resources if "docker" in src.split("/") or "__pycache__" in src.split("/")
    ]
    assert not offenders, f"docker/__pycache__ 不得入 resources: {offenders}"
