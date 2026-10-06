"""装机包 resources 面守卫(10-06-plugin-src-remote-fetch 批3,规范反转)。

分发规范(主人原话 2026-10-06:**「是这些源码不能随包,但是这些配置可以」**;
档 .trellis/tasks/10-06-plugin-src-remote-fetch/prd.md §1)不变量:

1. **INV-1 声明随包**:11 个随包组件包目录**只准携带** ``plugin.yaml`` +
   ``README.md`` 两件——Resources/plugins/<id>/ 下出现其余任何文件即违例。
2. **INV-2 源码不进包**:adapter.py、场景件(如 render_crawl4ai.py)一律
   不得出现在 resources 映射——源码经发布链 per-plugin release 资产
   (tar.gz + plugins.lock.json 内容寻址)远取安装,装机侧
   tests/desktop/test_bundled_plugins_install.py + src/myssia/plugins/remote.py。
3. **INV-3 数据件不进包**:vendor/(submodule 上游 GPL 源码,零分发红线
   沿既有裁定)、__pycache__ 缓存、自有子包(credhunter/)整目录。

**规范反转留痕**:本文件曾钉「desktop tier 源码面随包(三件套)」
(10-05-plugin-market-batch AC5 → 10-06-native-plugin-components §12.1
反向对账),10-06-plugin-src-remote-fetch 批3 按新规范全面翻案——断言从
「manifest+README+adapter 三件套必须在」反转为「两声明必须在 + 其余
必须在键空间不存在」。随包源码的历史理由(装机直拷安装链)由远取链
接管;仓库 plugins/ 源树不动(远取资产的打包源),仅装机包映射收窄。

**锁件注**:远取锁 plugins.lock.json 随发布链(批4 release-plugins)
产真锁后落包,其门禁(11 件全覆盖 + sha256/url 自洽)随批4 落,本文件
不锁锁件。

品类面(官方 7 + demo + 场景 monitor/credentials)属「配置可随包」,
维持随包不变,断言原样保留。与 tests/desktop/test_pyenv_resources.py
的分工:彼管 Python 运行时五映射「不被挤掉」;此管随包插件面
(品类在 + 组件包两声明在且**仅有** + 源码/数据件不在)。
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_TAURI = REPO_ROOT / "desktop" / "src-tauri"
TAURI_CONF = SRC_TAURI / "tauri.conf.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

#: 官方 7 品类(README zh/en「7 official categories」口径)+ demo 件;
#: monitor/credentials(10-05-bundled-plugins-batch2 R4):场景品类随包
#: (安全裁定=纯 keychain:/env: 引用模板 + example.com 占位,零明文凭据,
#: 亲读全文物证;物证钉死见本文件 §4)。品类是「配置」,新规范下照旧随包。
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
    # 场景品类件(monitor=changedetection.io 远端集成;credentials=凭证猎手),
    # 2026-10-05 批二进包:随包 plugins 面自此 10 组件包 + 10 品类 = 20 件。
    "monitor.yaml",
    "credentials.yaml",
)

#: desktop tier 源码件全件(EXPECTED_TIERS 同源清单;新规范下这些件的
#: adapter.py/场景件**不再随包**——源码远取,本清单只剩「哪些目录存在」
#: 的发现面口径)。与 STUB_ONLY_PACKAGES/REMOTE_STUB_PACKAGES 合计 11 组件包。
DESKTOP_TIER_PACKAGES = (
    "myssia-proxy",
    "myssia-osint",
    "myssia-credhunter",
    "myssia-media",
    "myssia-maigret",
    "myssia-theharvester",
    "myssia-urlwatch",
    "myssia-snownlp",
    "myssia-yake",
)

#: desktop tier 警示型文档桩件(design §7.3 D10-3:tier: desktop 但零
#: adapter/零程序面,收录=市场知识面)——桩形状本就只有两声明件。
STUB_ONLY_PACKAGES = ("myssia-mediacrawler",)

#: remote tier 桩件(10-06-native-plugin-components 阶段3 G-Q1):
#: tier: remote、零 adapter 零运行时——随包的唯一目的是让装机「随包官方
#: 插件件」卡出现该条目,作轨D remote 配置面板的挂点;桩形状同 mediacrawler。
REMOTE_STUB_PACKAGES = ("myssia-firecrawl",)

#: 随包组件包全集(恰 11 件 = DESKTOP_TIER 9 + 桩 1 + remote 桩 1;与
#: tests/desktop/test_bundled_plugins_install.py 的 BUNDLED_PACKAGES 同源
#: 合成式——该文件跨目录 import 上述三清单常量,清单漂移两侧参数化对不上
#: 即红)。
ALL_BUNDLED_PACKAGES = DESKTOP_TIER_PACKAGES + STUB_ONLY_PACKAGES + REMOTE_STUB_PACKAGES

#: INV-1 口径:每个随包组件包目录**只准**携带的两件声明(发现面靠
#: plugin.yaml,署名/警示文档靠 README.md;manifest schema 见
#: src/myssia/plugins/manifest.py)。
DECLARATION_FILES = ("plugin.yaml", "README.md")

#: myssia-credhunter 自有子包(INV-3:adapter compile+exec 自举加载
#: credhunter/*.py 与 data/ 数据文件)——源码子包不再随包,远取资产整树
#: 打包(发布链 git archive,批4),装机按锁拉回。
CREDHUNTER_SUBPACKAGE = "credhunter"


def _conf_resources() -> dict[str, str]:
    conf = json.loads(TAURI_CONF.read_text(encoding="utf-8"))
    resources = conf["bundle"]["resources"]
    assert isinstance(resources, dict), "resources 段须为 map 形"
    return resources


# ---------------------------------------------------------------------------
# 1. 官方品类 7/7 + demo 全捆(「配置可随包」,新规范不变)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "yaml_name", [name for name in OFFICIAL_CATEGORY_YAMLS if name != "myssia-demo.yaml"]
)
def test_official_category_yaml_bundled(yaml_name: str) -> None:
    """品类 YAML 逐一(官方 7 + 场景 2,monitor/credentials 见常量注):
    resources 有映射,且映射源在仓库 plugins/ 实况存在。"""
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
# 2. 组件包两声明必须在(INV-1 正面)+ 目录内「仅有」两件(INV-1 反面)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("package", ALL_BUNDLED_PACKAGES)
@pytest.mark.parametrize("filename", DECLARATION_FILES)
def test_bundled_package_declaration_file_mapped(package: str, filename: str) -> None:
    """每组件包 × 两声明件:映射在 + 源在盘(远取安装后以实拉 manifest
    校验为准,但发现面/署名面必须随包离线可见)。"""
    source = f"../../plugins/{package}/{filename}"
    dest = f"plugins/{package}/{filename}"
    resources = _conf_resources()
    assert resources.get(source) == dest, (
        f"组件包声明件未随包: {source!r} -> {dest!r}(实得 {resources.get(source)!r})"
    )
    assert (SRC_TAURI / source).is_file(), f"映射源不存在: {source}"


@pytest.mark.parametrize("package", ALL_BUNDLED_PACKAGES)
def test_bundled_package_dir_maps_declarations_only(package: str) -> None:
    """INV-1 键空间精确断言:该组件包前缀下的映射**恰为**两声明件——
    多出任何一件(adapter.py/场景件/子目录/缓存)即红,少一件也红
    (与 §2 正面参数化互为正反,本断言额外拦「未清单化的多余件」)。"""
    resources = _conf_resources()
    prefix = f"../../plugins/{package}/"
    actual = {src: dest for src, dest in resources.items() if src.startswith(prefix)}
    expected = {
        f"{prefix}{filename}": f"plugins/{package}/{filename}" for filename in DECLARATION_FILES
    }
    assert actual == expected, (
        f"{package} 随包面违 INV-1(只准 {list(DECLARATION_FILES)},"
        f"实得映射 {sorted(actual)});源码/数据件应走远取,声明件补映射"
    )


# ---------------------------------------------------------------------------
# 3. 排除断言:源码 / vendor / 子包 / docker / __pycache__ 绝不入包
#    (INV-2/INV-3,负断言遍历全 map 键空间)
# ---------------------------------------------------------------------------


def test_no_plugin_python_source_mapped() -> None:
    """INV-2:plugins/ 键空间下零 ``*.py`` 映射——adapter.py、场景件
    (render_crawl4ai.py 等)源码一律远取,不随包分发。

    注意口径:只拦 ``../../plugins/`` 前缀(myssia-src/ 产品本体 Python
    源码随包是 INV-4 既有面,不在本守卫列)。"""
    resources = _conf_resources()
    offenders = [
        src for src in resources if src.startswith("../../plugins/") and src.endswith(".py")
    ]
    assert not offenders, f"插件源码不得随包(INV-2,远取链接管): {offenders}"


def test_credhunter_subpackage_not_bundled() -> None:
    """INV-3:credhunter/ 自有子包(adapter compile+exec 自举依赖)不再
    整目录随包——远取资产整树打包,装机按锁拉回后子包随安装根落位。

    源树仍在仓库(远取资产的打包源,发布链 git archive HEAD plugins/<id>
    取的就是这棵树):自举最小实况(入口模块 + 数据目录)在盘断言,
    源树被误删时此处红,远取资产即断供。"""
    subpackage = f"myssia-credhunter/{CREDHUNTER_SUBPACKAGE}"
    resources = _conf_resources()
    offenders = [
        src for src in resources if f"/{CREDHUNTER_SUBPACKAGE}" in src or src.endswith(
            f"/{subpackage}"
        )
    ]
    assert not offenders, f"credhunter/ 子包不得随包(INV-3,远取资产接管): {offenders}"
    repo_subpkg = PLUGINS_DIR / subpackage
    assert repo_subpkg.is_dir(), f"仓库源树子包缺失(远取资产断供): {repo_subpkg}"
    assert (repo_subpkg / "findings.py").is_file()
    assert (repo_subpkg / "data").is_dir()


def test_no_vendor_submodule_bundled() -> None:
    """INV-3:vendor/ 外来 submodule(GPL Photon / theHarvester)不随包:
    许可红线沿既有裁定(新规范下组件包源码本就整体远取,vendor 亦不进
    远取资产——design D5)。装机上 vendor 缺失走 adapter 既有结构化
    ``vendor_missing`` 指引(tests/plugins/test_osint_plugin.py 等已钉)。"""
    resources = _conf_resources()
    vendor_sources = [src for src in resources if "/vendor" in src or src.endswith("/vendor")]
    assert not vendor_sources, f"vendor/ 不得随包分发(许可红线): {vendor_sources}"


def test_no_docker_or_pycache_bundled() -> None:
    """INV-3:docker/(服务端件面)与 __pycache__ 不得出现在任何映射键里
    (逐文件映射天然排除,beforeBuildCommand clean:pycache 纵深防御,
    本断言兜底)。"""
    resources = _conf_resources()
    offenders = [
        src for src in resources if "docker" in src.split("/") or "__pycache__" in src.split("/")
    ]
    assert not offenders, f"docker/__pycache__ 不得入 resources: {offenders}"


# ---------------------------------------------------------------------------
# 4. 场景品类件安全裁定守卫(10-05-bundled-plugins-batch2 R4,原样保留)
# ---------------------------------------------------------------------------

#: 承载凭据的键(R4 物证核对面):这些键的值只允许 keychain:/env: 引用
#: 模板、Bearer 前缀引用或占位 URL,出现其余形态即疑似明文凭据。
_CREDENTIAL_BEARING_RE = re.compile(
    r"^\s*(?:-\s*)?(token|target|Authorization|X-Api-Key|github_tokens)\s*:\s*(.+?)\s*$",
    re.MULTILINE,
)


@pytest.mark.parametrize("yaml_name", ["monitor.yaml", "credentials.yaml"])
def test_scenario_category_yaml_is_credential_template_only(yaml_name: str) -> None:
    """R4 安全裁定物证钉死:monitor/credentials 只含凭据**引用模板**
    (``keychain:``/``env:`` + example.com 占位 endpoint),零明文凭据——
    两件入包(resources 映射)即成随包分发面,未来任何往里加明文密钥的
    改动在本测试即红(安全红线:入包即泄漏面)。"""
    text = (PLUGINS_DIR / yaml_name).read_text(encoding="utf-8")
    for match in _CREDENTIAL_BEARING_RE.finditer(text):
        raw = match.group(2)
        if raw.startswith("#"):
            continue  # 行内注释(如「# myssia secret set …」指引)不是值
        value = raw.strip("\"'").strip()
        # 块列表形(`github_tokens:\n  - keychain:…` 的 `\s*` 会吃掉换行把
        # 列表前缀带进值):剥列表记号后仍是引用才放行
        value = value.removeprefix("- ").strip()
        value = value.removeprefix("Bearer ").strip()  # Authorization 惯例前缀
        assert value.startswith(("keychain:", "env:")), (
            f"{yaml_name} 疑似明文凭据值(只允许 keychain:/env: 引用模板): "
            f"{match.group(0).strip()!r}"
        )
    # endpoint 是占位符不是真实部署地址(第一道防线:入包前就不该有真实地址)
    assert "example.com" in text, f"{yaml_name} 缺 example.com 占位锚点(物证核对面变化,人工复核)"
