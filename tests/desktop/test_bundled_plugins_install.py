"""随包插件组件包发现/一键安装/卸载 + 品类 YAML 平铺安装(plugins.bundled.*,
10-05-bundled-plugins-install + 10-05-bundled-plugins-batch2 + 10-06 远取批)。

sidecar 方法族的协议单测(mock stdin/stdout 往返,同
test_desktop_sidecar_protocol.py 的 rpc 手法;rpc helper 本文件独立一份,
与彼处同源零共享 import)。全部离线零外网零构建。

发现面(mounted-plugin-market 安装语义:随包 Resources/plugins/<pkg> 作
安装来源)的核心口径:

- **装机态目录树从 tauri.conf.json resources 映射逐键重建**(Tauri resources
  展开后 Resources/plugins/ 的忠实模拟——resources 是随包面的单一事实源,
  本测试不经「手写件清单」二手复述:list 断言数从映射动态派生,与
  test_installer_resources.py 的守卫常量(DESKTOP_TIER_PACKAGES 9 +
  STUB_ONLY_PACKAGES 1 + REMOTE_STUB_PACKAGES 1 = 11 组件包,10-06 阶段3
  起含 remote 桩 myssia-firecrawl;10-08 查漏批③后品类 14 件)对账,映射漂移
  即红);
- env 未设/目录不存在 = 合法空表(dev 稳定契约);
- install 三岔编排(10-06 分发规范:声明随包、源码远取):锁在+条目在 →
  远取链(mock transport 全程真管线:拉资产→sha256→剥壳解包→同门落位);
  锁缺/无条目但包内目录携带源码件(旧包形态,夹具 ``with_source=True``)→
  包内直拷回退;声明件-only 且锁无条目 → ``plugin_lock_missing`` 结构化拒。
  装卸殊途同归 InstalledPluginStore 同门(CLI ``myssia plugin install/remove``
  零差异):manifest 校验→版本矩阵→整目录拷贝/删绝不半装半卸;
  PluginStoreError code 原文透传(远取链失败 data 带定位信息);已装未
  force 拒且**零网络**;已装旧件逐字节零扰动(INV-6);
- category_install(批二 R3):品类 YAML 单文件平铺拷到数据根 plugins/
  (与 _seed_first_run 补种同落点);已存在未 force 拒、force 才覆盖。
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import shutil
import sys
import tarfile
from pathlib import Path

import httpx
import pytest

from myssia.plugins import remote as remote_module

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRY_PATH = REPO_ROOT / "desktop" / "entry.py"
SRC_TAURI = REPO_ROOT / "desktop" / "src-tauri"
TAURI_CONF = SRC_TAURI / "tauri.conf.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

_spec = importlib.util.spec_from_file_location("desktop_entry_bundled", ENTRY_PATH)
entry = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(entry)

# 与 test_installer_resources.py 同源守卫常量(随包组件包 11 件 + 品类 14 件
# 单一事实源;跨文件 import 常量——两侧清单漂移时参数化对不上即红,人工对账
# 口径同彼处)。
from test_installer_resources import (  # noqa: E402
    DESKTOP_TIER_PACKAGES,
    OFFICIAL_CATEGORY_YAMLS,
    REMOTE_STUB_PACKAGES,
    STUB_ONLY_PACKAGES,
)

#: 随包组件包全集(恰 11 件;恰对 tauri.conf resources 组件包目录映射;
#: 10-06 阶段3 起含 remote 桩件 myssia-firecrawl——随包为装机「随包官方
#: 插件件」卡的轨D remote 配置面板挂点,零 adapter 零运行时)。
BUNDLED_PACKAGES = DESKTOP_TIER_PACKAGES + STUB_ONLY_PACKAGES + REMOTE_STUB_PACKAGES

#: 随包品类 YAML 全集(恰 14 件;= OFFICIAL_CATEGORY_YAMLS 同源,7 官方 +
#: demo + monitor/credentials 两场景件 + telegram 三件与 daily-digest,
#: 10-08 查漏批③ G5/G9 入种子)。
BUNDLED_CATEGORY_IDS = tuple(name.removesuffix(".yaml") for name in OFFICIAL_CATEGORY_YAMLS)


@pytest.fixture(autouse=True)
def _reset_sidecar_state(monkeypatch, tmp_path):
    """每例独立的 sidecar 内存态 + env 隔离(MYIA_HOME/MYIA_BUNDLED_PLUGINS 均
    从干净态起;MYIA_PLUGIN_DIR 统一指到本例空沙箱——dev 回退根
    ~/.myia/plugins 是本机实况(可能真装着件),发现面已装态断言不得渗入)。"""
    monkeypatch.delenv("MYIA_HOME", raising=False)
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "isolated-install-root"))
    monkeypatch.delenv(entry.BUNDLED_PLUGINS_ENV, raising=False)
    entry._stop_cron_ticker()
    yield
    entry._stop_cron_ticker()


def rpc(*requests: dict) -> tuple[int, list[dict], list[dict]]:
    """整轮 RPC(与 test_desktop_sidecar_protocol.py 同款;独立实现零跨文件共享)。"""
    lines = [json.dumps(req, ensure_ascii=False) for req in requests]
    stdin = io.StringIO("".join(line + "\n" for line in lines))
    out = io.StringIO()
    code = entry.serve(stdin=stdin, stdout=out)
    responses: list[dict] = []
    events: list[dict] = []
    for line in out.getvalue().splitlines():
        obj = json.loads(line)
        (responses if "id" in obj else events).append(obj)
    return code, responses, events


def _conf_resources() -> dict[str, str]:
    import json as _json

    conf = _json.loads(TAURI_CONF.read_text(encoding="utf-8"))
    return conf["bundle"]["resources"]


def rebuild_bundled_tree(base: Path) -> Path:
    """按 tauri.conf resources 的 plugins/ 映射逐键重建目录树(Tauri resources
    展开后 Resources/plugins/ 的忠实模拟:源在仓库 plugins/<...>,目标
    <base>/plugins/<...>;credhunter 子包映射亦照搬)。批二起平铺品类 YAML
    (plugins/<name>.yaml 两段目标)一并照搬——装机 plugins 面 = 组件包子目录
    + 品类平铺文件,与真包 Resources/plugins 布局一致。"""
    resources = _conf_resources()
    copied = 0
    for source, dest in resources.items():
        if not dest.startswith("plugins/") or not dest.endswith((".yaml", ".yml", ".py", ".md", "credhunter")):
            continue
        parts = dest.split("/")
        if len(parts) < 2:  # 防御:plugins/ 下至少还有一段文件/目录名
            continue
        target = base / Path(*parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        source_path = SRC_TAURI / source
        assert source_path.exists(), f"映射源不存在(构建装机树失败): {source}"
        if source_path.is_dir():
            shutil.copytree(source_path, target)
        else:
            shutil.copy2(source_path, target)
        copied += 1
    assert copied > 0, "resources 映射里没有组件包文件——重建树空了(守卫常量对不上)"
    return base / "plugins"


#: 最小合法 manifest(版本兼容当前 myssia:>=0.0.1 全开下界)。
MINIMAL_MANIFEST = """id: {id}
name: {name}
version: 1.0.0
compatible: ">=0.0.1,<999"
tier: desktop
requires: []
provides: [demo_cap]
modes:
  local:
    install: myssia plugin install plugins/{id}
install:
  source: https://github.com/xinzhuzi/myia.git
"""


def make_bundled_package(base: Path, plugin_id: str, manifest_text: str, *, with_source: bool = True) -> Path:
    """往随包目录树放一件组件包(manifest 文本原样写)。

    ``with_source=True``(缺省)再放一个 ``adapter.py``——**旧包形态**(源码
    随包,10-06 分发规范前的包;锁缺席时走包内直拷回退,D3)。新规范包
    (声明随包、源码远取)只有 plugin.yaml+README,远取路径测试显式
    ``with_source=False`` 造形。
    """
    pkg = base / plugin_id
    pkg.mkdir(parents=True, exist_ok=True)
    (pkg / "plugin.yaml").write_text(manifest_text, encoding="utf-8")
    if with_source:
        (pkg / "adapter.py").write_text(f"# 旧包源码件(回退直拷夹具)\n", encoding="utf-8")
    return pkg


# ---------------------------------------------------------------------------
# list:发现面 / 空态 / 坏 manifest 条目 / 装机态对账(11 组件包 + 14 品类)
# ---------------------------------------------------------------------------


def test_list_empty_env_is_legal_empty_state():
    """env 未设 = 合法空表(dev 稳定契约):dir=null 如实,不虚构
    (批二起 categories 同空态)。"""
    code, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    assert code == 0
    assert responses[0] == {
        "id": 1,
        "result": {"dir": None, "count": 0, "plugins": [], "categories": []},
    }


def test_list_env_points_to_missing_dir_is_also_empty(monkeypatch, tmp_path):
    """env 设了但目录不存在(旧包/自动化半注入)= 同款合法空表。"""
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(tmp_path / "nope"))
    code, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    assert code == 0
    assert responses[0]["result"] == {
        "dir": None, "count": 0, "plugins": [], "categories": [],
    }


def test_list_rebuilt_installer_tree_yields_exactly_eleven_packages(monkeypatch, tmp_path):
    """装机态对账:resources 映射重建目录树 → 组件包恰 11 件(10 desktop +
    myssia-firecrawl remote 桩)、品类恰 14 件(与 test_installer_resources
    守卫常量同源;映射漂移即红,不硬编码孤数)。"""
    root = rebuild_bundled_tree(tmp_path / "Resources")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    # home 沙箱:categories 的 exists 检查 plugins_dir 干净(dev 回退根是仓库
    # cwd/plugins 实况,官方品类同名件在盘会把 exists 污成 True)
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    code, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    assert code == 0
    result = responses[0]["result"]
    assert result["dir"] == str(root)
    assert result["count"] == len(BUNDLED_PACKAGES) == 11
    assert {plugin["id"] for plugin in result["plugins"]} == set(BUNDLED_PACKAGES)
    # 逐件摘要键集恰为契约面(id/name/version/tier/gate/requires/provides +
    # 兼容判定 + 已装态 + findings;manifest schema 无 description,如实不带)
    for plugin in result["plugins"]:
        assert set(plugin) == {
            "id", "dir_name", "path", "name", "version", "tier", "gate",
            "compatible", "compatible_current", "requires", "provides",
            "installed", "installed_version", "findings",
        }, f"{plugin['id']} 摘要键集漂移"
        # 10-06 阶段3:随包面 = 10 件 desktop + remote 桩件(tier 如实,轨D
        # 面板据此渲染 remote 配置区)
        expected_tier = "remote" if plugin["id"] in REMOTE_STUB_PACKAGES else "desktop"
        assert plugin["tier"] == expected_tier
        assert plugin["compatible_current"] is True  # 官方件 compatible 全兼容当前
        assert plugin["installed"] is False  # 全新安装根零预装
        assert plugin["findings"] == []  # 官方件 manifest 全部可读
    # credhunter 件 credhunter/ 子包(整目录映射)不单独成条目——按 manifest 计
    ids = sorted(plugin["id"] for plugin in result["plugins"])
    assert ids == sorted(BUNDLED_PACKAGES)
    # 品类发现面(批二 R3;批③后 14 件):重建树平铺 YAML,id 集与守卫常量同源;
    # exists 对齐数据根实况(隔离空沙箱 → 全 False);官方件全可读零 finding。
    assert len(result["categories"]) == len(BUNDLED_CATEGORY_IDS) == 14
    assert {cat["id"] for cat in result["categories"]} == set(BUNDLED_CATEGORY_IDS)
    for cat in result["categories"]:
        assert set(cat) == {"file", "path", "id", "name", "schedule", "exists", "findings"}, (
            f"{cat['file']} 品类视图键集漂移"
        )
        assert cat["exists"] is False
        assert cat["findings"] == []
        assert cat["schedule"]  # 品类必有合法 cron(schema 校验门)


def test_bundled_declaration_files_are_mapped_in_tauri_resources():
    """反向对账(§12.1 复核轮补钉;10-06 分发规范翻案):仓库组件包**声明件**
    ⊆ tauri resources 映射.

    正向(rebuild_bundled_tree / test_installer_resources)只验「映射→磁盘」
    方向——从映射删行不红;本钉反向「磁盘→映射」:随包组件包目录里的**声明
    件**(plugin.yaml/README.md,新规范唯一随包分发面,INV-1)漏登记
    bundle.resources 时,任何按清单的打包/刷新都会静默丢件(10-06 §12.1
    HIGH 实录同款)。源码件(adapter.py 等)10-06 起设计上**不随包**(INV-2,
    源码远取——负断言在 test_installer_resources.py 键空间门),不再 demand
    映射;__pycache__/loot/vendor 运行时与上游件永不随包(同上不在面)。
    """
    dests = set(_conf_resources().values())  # 映射键=源路径(../../…),值=目标(plugins/…)
    bundled_pkgs = {
        dest.split("/")[1]
        for dest in dests
        if dest.startswith("plugins/") and len(dest.split("/")) >= 3
    }  # plugins/<pkg>/<file|dir> 形;平铺品类 plugins/<name>.yaml 不在列
    assert bundled_pkgs == set(BUNDLED_PACKAGES), "映射组件包集与守卫常量漂移"
    dir_mappings = {
        dest
        for dest in dests
        if dest.startswith("plugins/") and not dest.endswith((".yaml", ".yml", ".py", ".md"))
    }  # 整目录映射(如过渡期的 plugins/myssia-credhunter/credhunter)
    for pkg in sorted(bundled_pkgs):
        pkg_dir = PLUGINS_DIR / pkg
        assert pkg_dir.is_dir(), f"映射指向不存在的组件包目录: {pkg_dir}"
        for declaration in ("plugin.yaml", "README.md"):
            declaration_file = pkg_dir / declaration
            if not declaration_file.is_file():
                continue  # 个别件无 README 属实况,不 demand 存在,只 demand「在则必映射」
            dest_rel = f"plugins/{pkg}/{declaration}"
            covered = dest_rel in dests or any(dest_rel.startswith(dir_dest + "/") for dir_dest in dir_mappings)
            assert covered, (
                f"{pkg}/{declaration}: 组件包声明件未登记 tauri resources 映射——官方重打包"
                "会静默丢件(10-06 §12.1 HIGH 同款;补 bundle.resources 该文件行)"
            )


def test_list_bad_manifest_is_entry_level_finding_not_table_failure(monkeypatch, tmp_path):
    """坏 manifest 条目级 finding(manifest_invalid)不整表炸(yaml.list 先例):
    坏件 id=None/摘要空 + findings 带首行原因;好件照常在列。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-good", MINIMAL_MANIFEST.format(id="myssia-good", name="好件"))
    bad = root / "myssia-bad"
    bad.mkdir(parents=True)
    (bad / "plugin.yaml").write_text("id: 123\ninvalid_field: 1\n", encoding="utf-8")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    code, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    assert code == 0
    result = responses[0]["result"]
    assert result["count"] == 2
    by_dir = {plugin["dir_name"]: plugin for plugin in result["plugins"]}
    assert by_dir["myssia-good"]["id"] == "myssia-good"
    assert by_dir["myssia-good"]["findings"] == []
    assert by_dir["myssia-bad"]["id"] is None  # manifest 坏:无从取 id,如实 None
    codes = [finding["code"] for finding in by_dir["myssia-bad"]["findings"]]
    assert "manifest_invalid" in codes
    # 平铺品类 YAML 不是组件包(补种面已覆盖品类),不进组件包清单
    (root / "ai-news.yaml").write_text("id: ai-news\n", encoding="utf-8")
    code, responses, _ = rpc({"id": 2, "method": "plugins.bundled.list", "params": {}})
    assert responses[0]["result"]["count"] == 2
    # 但进品类发现面(批二 R3):坏 YAML 条目级 finding(id=None 如实)
    cats = {cat["file"]: cat for cat in responses[0]["result"]["categories"]}
    assert cats["ai-news.yaml"]["id"] is None
    assert "category_invalid" in [f["code"] for f in cats["ai-news.yaml"]["findings"]]


def test_list_dir_name_manifest_id_mismatch_surfaces_warning(monkeypatch, tmp_path):
    """目录名与 manifest id 不一致 → id_mismatch warning 如实透出(按 manifest id 为准)。"""
    root = tmp_path / "bundled"
    pkg = make_bundled_package(root, "wrong-dir-name", MINIMAL_MANIFEST.format(id="myssia-real", name="错名件"))
    assert pkg.is_dir()
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    code, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    assert code == 0
    plugin = responses[0]["result"]["plugins"][0]
    assert plugin["id"] == "myssia-real"
    assert [finding["code"] for finding in plugin["findings"]] == ["id_mismatch"]


def test_list_installed_state_aligns_with_install_root(monkeypatch, tmp_path):
    """已装态对齐:安装根预装一件 → installed=true + installed_version=已装 manifest
    版本;版本不同的重装可见(已装 0.9 / 随包 1.0)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-demo-cap", MINIMAL_MANIFEST.format(id="myssia-demo-cap", name="演示件"))
    # 安装根预装 0.9.0(旧版本)
    install_root = tmp_path / "plugins"
    installed_dir = install_root / "myssia-demo-cap"
    installed_dir.mkdir(parents=True)
    (installed_dir / "plugin.yaml").write_text(
        MINIMAL_MANIFEST.format(id="myssia-demo-cap", name="演示件").replace("version: 1.0.0", "version: 0.9.0"),
        encoding="utf-8",
    )
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    code, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    assert code == 0
    plugin = responses[0]["result"]["plugins"][0]
    assert plugin["installed"] is True
    assert plugin["installed_version"] == "0.9.0"
    assert plugin["version"] == "1.0.0"  # 随包版本(UI 据此提示「可重装更新」)


# ---------------------------------------------------------------------------
# install:一键装 / 结构化拒 / 同门透传
# ---------------------------------------------------------------------------


def test_install_copies_directory_into_install_root(monkeypatch, tmp_path):
    """一键装真拷贝:整目录拷贝(manifest+README+adapter 逐字节一致),应答
    {ok, dir, version};目录恰落在安装根 <install_root>/<id>。"""
    root = tmp_path / "bundled"
    pkg = make_bundled_package(root, "myssia-copyable", MINIMAL_MANIFEST.format(id="myssia-copyable", name="拷贝件"))
    (pkg / "README.md").write_text("# 拷贝件 README\n", encoding="utf-8")
    (pkg / "adapter.py").write_text("print('copyable adapter')\n", encoding="utf-8")
    (pkg / "sub").mkdir()
    (pkg / "sub" / "data.txt").write_text("data\n", encoding="utf-8")
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    code, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                               "params": {"id": "myssia-copyable"}})
    assert code == 0
    assert responses[0]["result"]["ok"] is True
    assert responses[0]["result"]["version"] == "1.0.0"
    installed = install_root / "myssia-copyable"
    assert responses[0]["result"]["dir"] == str(installed)
    assert (installed / "plugin.yaml").read_text(encoding="utf-8") == (pkg / "plugin.yaml").read_text(encoding="utf-8")
    assert (installed / "README.md").read_text(encoding="utf-8") == (pkg / "README.md").read_text(encoding="utf-8")
    assert (installed / "adapter.py").read_text(encoding="utf-8") == (pkg / "adapter.py").read_text(encoding="utf-8")
    assert (installed / "sub" / "data.txt").read_text(encoding="utf-8") == "data\n"
    # 随包原件只读永不删(卸载语义 = 删安装根拷贝可重装)
    assert (pkg / "plugin.yaml").exists()


def test_install_already_installed_without_force_is_structured_reject(monkeypatch, tmp_path):
    """已装未 force → already_installed 结构化拒(PluginStoreError code 原文透传);
    force=true → 重装成功(先清后拷,不残留旧文件)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-forceable", MINIMAL_MANIFEST.format(id="myssia-forceable", name="重装件"))
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-forceable"}})
    assert responses[0]["result"]["ok"] is True
    # 二装未 force:already_installed(安装门零新增,与 CLI 同门)
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-forceable"}})
    assert responses[0]["error"]["code"] == "already_installed"
    assert responses[0]["error"]["path"] == "params.id"
    # force=true:重装成功;先清后拷(旧残留文件不存活)
    stale = install_root / "myssia-forceable" / "stale.txt"
    stale.write_text("stale\n", encoding="utf-8")
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-forceable", "force": True}})
    assert responses[0]["result"]["ok"] is True
    assert not stale.exists()
    # 重装后 list 已装态翻真
    _, responses, _ = rpc({"id": 4, "method": "plugins.bundled.list", "params": {}})
    plugin = responses[0]["result"]["plugins"][0]
    assert plugin["installed"] is True
    assert plugin["installed_version"] == "1.0.0"


def test_install_incompatible_version_rejected_and_force_overrides(monkeypatch, tmp_path):
    """版本矩阵同门:随包件 compatible 要求不存在的 myssia 版本 → 未 force
    incompatible_version 拒;force 强装(compatible_current 如实 false,UI 据此警示)。"""
    root = tmp_path / "bundled"
    make_bundled_package(
        root, "myssia-future",
        MINIMAL_MANIFEST.format(id="myssia-future", name="未来件").replace('">=0.0.1,<999"', '">=999.0.0"'),
    )
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-future"}})
    assert responses[0]["error"]["code"] == "incompatible_version"
    assert "999.0.0" in responses[0]["error"]["message"]
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-future", "force": True}})
    assert responses[0]["result"]["ok"] is True
    # 强装后发现面如实带不兼容警示(compatible_current=false + finding)
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.list", "params": {}})
    plugin = responses[0]["result"]["plugins"][0]
    assert plugin["installed"] is True
    assert plugin["compatible_current"] is False  # 随包件本身仍不兼容(如实)
    assert "incompatible_version" in [finding["code"] for finding in plugin["findings"]]


def test_install_traversal_ids_are_rejected_before_any_lookup(monkeypatch, tmp_path):
    """穿越 id 防线:../foo、a/b、斜杠/点点形态与大写/过短形状 → invalid_params
    (path=params.id),正则门先于目录映射(_PLUGIN_ID_RE 与 manifest.py/
    installed.py 同源——数字开头如 123 是合法形状,归 not_found 组另断)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-target", MINIMAL_MANIFEST.format(id="myssia-target", name="目标件"))
    (tmp_path / "escape-marker.txt").write_text("escape!\n", encoding="utf-8")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "install-root"))
    for bad_id in ("../escape-marker", "a/b", "../../etc", "..", "FOO", "x", "-leading-dash"):
        _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                                "params": {"id": bad_id}})
        assert responses[0]["error"]["code"] == "invalid_params", f"{bad_id!r} 应被正则门拒"
        assert responses[0]["error"]["path"] == "params.id"
    # 正则允许但目录里没有(数字开头合法形状):归 bundled_plugin_not_found
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install", "params": {"id": "123"}})
    assert responses[0]["error"]["code"] == "bundled_plugin_not_found"
    assert (tmp_path / "escape-marker.txt").read_text(encoding="utf-8") == "escape!\n"  # 原件未被动


def test_install_without_env_is_unavailable_structured_reject(monkeypatch, tmp_path):
    """env 未设(dev 形态/旧包)→ bundled_plugins_unavailable 结构化拒,如实。"""
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "install-root"))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-anywhere"}})
    assert responses[0]["error"]["code"] == "bundled_plugins_unavailable"
    assert responses[0]["error"]["path"] == "params.id"


def test_install_unknown_id_in_bundled_tree_is_not_found(monkeypatch, tmp_path):
    """id 合法但随包目录内无此件 → bundled_plugin_not_found(可用件见 list)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-known", MINIMAL_MANIFEST.format(id="myssia-known", name="在列件"))
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "install-root"))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-unknown"}})
    assert responses[0]["error"]["code"] == "bundled_plugin_not_found"
    assert responses[0]["error"]["path"] == "params.id"


def test_install_params_shape_is_validated(monkeypatch, tmp_path):
    """参数形状:缺 id/非字符串、force 非布尔 → invalid_params(path 精确到键)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-shape", MINIMAL_MANIFEST.format(id="myssia-shape", name="形状件"))
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "install-root"))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.id"
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.install", "params": {"id": 123}})
    assert responses[0]["error"]["path"] == "params.id"
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-shape", "force": "yes"}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.force"


def test_install_bad_manifest_source_is_rejected_not_half_installed(monkeypatch, tmp_path):
    """随包件 manifest 坏 → manifest_invalid 结构化拒(绝不半装:校验发生在
    安装根 mkdir 之前,安装根零目录零副作用)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-broken", "id: 123\ninvalid_field: 1\n")
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-broken", "force": True}})
    assert responses[0]["error"]["code"] == "manifest_invalid"
    assert not install_root.exists(), "manifest 校验失败绝不半装(安装根都不该被建)"


def test_install_locates_by_manifest_id_when_dir_name_differs(monkeypatch, tmp_path):
    """id→目录映射:目录名直配 > manifest id 匹配兜底(坏 manifest 目录跳过)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "wrong-dir", MINIMAL_MANIFEST.format(id="myssia-real-id", name="错名件"))
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                            "params": {"id": "myssia-real-id"}})
    assert responses[0]["result"]["ok"] is True
    assert (install_root / "myssia-real-id" / "plugin.yaml").exists()  # 按 manifest id 落目录
    assert responses[0]["result"]["dir"] == str(install_root / "myssia-real-id")


def test_bundled_methods_on_rebuilt_installer_tree_roundtrip(monkeypatch, tmp_path):
    """装机树端到端(10-06 翻案为远取路径,真官方 manifest 零手写夹具):
    resources 映射重建装机树 + 锁(资产字节 = 仓库 plugins/myssia-proxy 真件
    打包)→ install 走远取链落位逐字节对账;再二装未 force already_installed
    拒且零网络;list 已装态对齐。锁条目优先于包内目录形态——收窄前后
    (包内有无源码)行为一致,不依赖打包线在途状态。
    """
    root = rebuild_bundled_tree(tmp_path / "Resources")
    # 资产 = 仓库真件(含 adapter.py 源码——远取面不分声明/源码,整包走)
    repo_pkg = PLUGINS_DIR / "myssia-proxy"
    repo_files = {
        str(item.relative_to(repo_pkg)): item.read_bytes()
        for item in sorted(repo_pkg.rglob("*"))
        if item.is_file() and "__pycache__" not in item.parts
    }
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for rel, data in sorted(repo_files.items()):
            info = tarfile.TarInfo(f"plugins/myssia-proxy/{rel}")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    tarball = buffer.getvalue()
    write_plugins_lock(root, {"myssia-proxy": lock_entry_for(tarball, "myssia-proxy")})
    patch_remote_transport(monkeypatch, serve(tarball))
    install_root = tmp_path / "install"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-proxy"}})
    assert responses[0].get("result", {}).get("ok") is True, f"官方件装机失败: {responses[0]}"
    installed = install_root / "myssia-proxy"
    for rel, data in repo_files.items():
        assert (installed / rel).read_bytes() == data, f"远取落位逐字节不符: {rel}"
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.list", "params": {}})
    by_id = {plugin["id"]: plugin for plugin in responses[0]["result"]["plugins"]}
    assert by_id["myssia-proxy"]["installed"] is True
    assert by_id["myssia-media"]["installed"] is False
    # 二装未 force:already_installed 且零网络(换一碰就炸的 transport 证不触发远取)
    patch_remote_transport(monkeypatch, refuse_network())
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-proxy"}})
    assert responses[0]["error"]["code"] == "already_installed"


# ---------------------------------------------------------------------------
# 远取主路径(10-06 分发规范:声明随包、源码远取)——全 mock 零真网
# ---------------------------------------------------------------------------

#: 远取测试锁的固定上下文(与真锁同形:repo=现远端 shishi)。
LOCK_REPO = "https://github.com/xinzhuzi/shishi"
LOCK_TAG = "v0.0.2"


def build_remote_tarball(plugin_id: str, manifest_text: str, extra: dict[str, bytes] | None = None) -> bytes:
    """打包 ``plugins/<id>/`` 前缀 tar.gz(远取资产形态;发布脚本同前缀)。"""
    files = {
        "plugin.yaml": manifest_text.encode("utf-8"),
        "README.md": "# 远取件 README\n".encode("utf-8"),
        "adapter.py": b"print('remote adapter')\n",
    }
    files.update(extra or {})
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        for name, data in sorted(files.items()):
            info = tarfile.TarInfo(f"plugins/{plugin_id}/{name}")
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def write_plugins_lock(root: Path, assets: dict[str, dict]) -> None:
    """往随包根写 plugins.lock.json(缺省自洽:url 按资产名规则拼)。"""
    payload = {
        "manifest_version": 1,
        "repo": LOCK_REPO,
        "tag": LOCK_TAG,
        "generated_at": "2026-10-06T00:00:00+08:00",
        "assets": assets,
    }
    (Path(root) / remote_module.LOCK_FILENAME).write_text(json.dumps(payload), encoding="utf-8")


def lock_entry_for(tarball: bytes, plugin_id: str, *, sha256: str | None = None) -> dict:
    """单件锁条目(缺省钉真 sha256/size)。"""
    return {
        "url": f"{LOCK_REPO}/releases/download/{LOCK_TAG}/plugin-{plugin_id}.tar.gz",
        "sha256": sha256 or hashlib.sha256(tarball).hexdigest(),
        "size": len(tarball),
        "version": "1.0.0",
    }


def patch_remote_transport(monkeypatch, handler) -> None:
    """把 entry.install_remote 包一层真实现 + 注入 MockTransport(端到端走真
    远取管线:锁→拉取→校验→解包→store.install;零真网)。"""
    real_install_remote = remote_module.install_remote

    def fake(lock, plugin_id, store, *, force=False, **kwargs):
        kwargs.setdefault("client_factory", lambda **ck: httpx.Client(transport=httpx.MockTransport(handler), **ck))
        return real_install_remote(lock, plugin_id, store, force=force, **kwargs)

    monkeypatch.setattr(entry, "install_remote", fake)


def serve(payload: bytes, *, status: int = 200):
    """固定应答 handler(2xx 恒回资产字节 / 非 2xx 回状态)。"""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, content=payload)
    return handler


def refuse_network(message: str = "远取不该被触发"):
    """一碰就炸 handler:断言「零网络」用。"""
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(message)
    return handler


def make_declaration_package(base: Path, plugin_id: str, manifest_text: str) -> Path:
    """新规范包形态:只有声明件 plugin.yaml+README(源码远取,INV-1)。"""
    pkg = make_bundled_package(base, plugin_id, manifest_text, with_source=False)
    (pkg / "README.md").write_text("# 声明件 README\n", encoding="utf-8")
    return pkg


def test_install_remote_path_via_lock_entry_end_to_end(monkeypatch, tmp_path):
    """远取主路径端到端(锁在+条目在):拉资产→sha256 校验→剥壳解包→
    InstalledPluginStore 同门落位;应答 {ok,dir,version} 契约不变;装后 list
    installed=true 版本对;.staging 清残;随包声明件只读不动。"""
    root = tmp_path / "bundled"
    make_declaration_package(root, "myssia-remote", MINIMAL_MANIFEST.format(id="myssia-remote", name="远取件"))
    tarball = build_remote_tarball("myssia-remote", MINIMAL_MANIFEST.format(id="myssia-remote", name="远取件"))
    write_plugins_lock(root, {"myssia-remote": lock_entry_for(tarball, "myssia-remote")})
    patch_remote_transport(monkeypatch, serve(tarball))
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-remote"}})
    assert responses[0]["result"] == {
        "ok": True,
        "dir": str(install_root / "myssia-remote"),
        "version": "1.0.0",
    }, responses[0]
    installed = install_root / "myssia-remote"
    assert (installed / "plugin.yaml").read_text(encoding="utf-8") == MINIMAL_MANIFEST.format(id="myssia-remote", name="远取件")
    assert (installed / "adapter.py").read_text(encoding="utf-8") == "print('remote adapter')\n"  # 源码经远取落位
    staging = install_root / ".staging"
    assert not staging.is_dir() or not any(staging.iterdir()), "暂存清残"
    # 随包声明件只读不动(源码不来自包内)
    assert sorted(p.name for p in (root / "myssia-remote").iterdir()) == ["README.md", "plugin.yaml"]
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.list", "params": {}})
    plugin = responses[0]["result"]["plugins"][0]
    assert plugin["installed"] is True
    assert plugin["installed_version"] == "1.0.0"
    # 已装未 force 二装:already_installed 结构化拒(同门,装后语义零漂移)
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-remote"}})
    assert responses[0]["error"]["code"] == "already_installed"


def test_install_declaration_only_without_lock_is_structured_refuse(monkeypatch, tmp_path):
    """新包形态但锁缺席 → plugin_lock_missing 结构化拒(不静默不虚构;直拷
    声明件会装出不能跑的空壳);零半装零残。"""
    root = tmp_path / "bundled"
    make_declaration_package(root, "myssia-nolock", MINIMAL_MANIFEST.format(id="myssia-nolock", name="无锁件"))
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-nolock"}})
    error = responses[0]["error"]
    assert error["code"] == "plugin_lock_missing"
    assert error["path"] == "params.id"
    assert error["data"]["lock_present"] is False
    assert not (install_root / "myssia-nolock").exists()


def test_install_declaration_dir_polluted_with_pycache_still_refuses(monkeypatch, tmp_path):
    """回退门收紧:纯声明件目录混入 __pycache__(含 .pyc、无任何 .py)不再
    按「非隐藏子目录」误判旧包直拷——照走 plugin_lock_missing 结构化拒,
    不装出缺 adapter 的空壳「已装」件(暴露面:手动/自定义
    MYIA_BUNDLED_PLUGINS 指向被污染目录)。"""
    root = tmp_path / "bundled"
    pkg = make_declaration_package(root, "myssia-dirty", MINIMAL_MANIFEST.format(id="myssia-dirty", name="污染件"))
    cache = pkg / "__pycache__"
    cache.mkdir()
    (cache / "adapter.cpython-312.pyc").write_bytes(b"\x00pyc")
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-dirty"}})
    error = responses[0]["error"]
    assert error["code"] == "plugin_lock_missing"
    assert error["data"]["lock_present"] is False
    assert not (install_root / "myssia-dirty").exists(), "不得装出缺 adapter 的空壳件"


def test_install_lock_entry_missing_for_id_is_structured_refuse(monkeypatch, tmp_path):
    """锁在但无该件条目 → plugin_lock_missing(data lock_present=True);
    声明件照常在 list 可见(发现面不依赖锁)。"""
    root = tmp_path / "bundled"
    make_declaration_package(root, "myssia-orphan", MINIMAL_MANIFEST.format(id="myssia-orphan", name="锁外件"))
    other_tarball = build_remote_tarball("myssia-other", MINIMAL_MANIFEST.format(id="myssia-other", name="他件"))
    write_plugins_lock(root, {"myssia-other": lock_entry_for(other_tarball, "myssia-other")})
    patch_remote_transport(monkeypatch, refuse_network())
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-orphan"}})
    error = responses[0]["error"]
    assert error["code"] == "plugin_lock_missing"
    assert error["data"]["lock_present"] is True
    assert not (install_root / "myssia-orphan").exists()
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.list", "params": {}})
    assert responses[0]["result"]["plugins"][0]["id"] == "myssia-orphan"  # 发现面照常


def test_install_remote_bad_hash_structured_with_digests(monkeypatch, tmp_path):
    """坏 hash 拒:integrity_mismatch + data 带期望/实得与 url;零半装、
    .staging 零残件(AC3)。夹具与锁 size 同长度、内容漂移——先过 size
    前置对账,专测摘要面。"""
    root = tmp_path / "bundled"
    make_declaration_package(root, "myssia-badhash", MINIMAL_MANIFEST.format(id="myssia-badhash", name="坏钉件"))
    tarball = build_remote_tarball("myssia-badhash", MINIMAL_MANIFEST.format(id="myssia-badhash", name="坏钉件"))
    write_plugins_lock(root, {"myssia-badhash": lock_entry_for(tarball, "myssia-badhash", sha256="0" * 64)})
    tampered = b"t" * len(tarball)
    patch_remote_transport(monkeypatch, serve(tampered))
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-badhash"}})
    error = responses[0]["error"]
    assert error["code"] == "integrity_mismatch"
    assert error["data"]["expected"] == "0" * 64
    assert error["data"]["actual"] == hashlib.sha256(tampered).hexdigest()
    assert error["data"]["url"].endswith("/plugin-myssia-badhash.tar.gz")
    assert not (install_root / "myssia-badhash").exists()
    staging = install_root / ".staging"
    assert not staging.is_dir() or not any(staging.iterdir())


def test_install_remote_http_failure_structured_with_status(monkeypatch, tmp_path):
    """网络失败拒:plugin_fetch_failed + data 带 HTTP 状态与 url;零半装。"""
    root = tmp_path / "bundled"
    make_declaration_package(root, "myssia-down", MINIMAL_MANIFEST.format(id="myssia-down", name="断网件"))
    tarball = build_remote_tarball("myssia-down", MINIMAL_MANIFEST.format(id="myssia-down", name="断网件"))
    write_plugins_lock(root, {"myssia-down": lock_entry_for(tarball, "myssia-down")})
    patch_remote_transport(monkeypatch, serve(b"server boom", status=503))
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-down"}})
    error = responses[0]["error"]
    assert error["code"] == "plugin_fetch_failed"
    assert error["data"]["status"] == 503
    assert error["data"]["url"].endswith("/plugin-myssia-down.tar.gz")
    assert not (install_root / "myssia-down").exists()


def test_install_corrupt_lock_is_structured_invalid(monkeypatch, tmp_path):
    """锁文件坏(非合法 JSON)→ plugin_lock_invalid 结构化拒(不静默走直拷
    绕过内容寻址)。"""
    root = tmp_path / "bundled"
    root.mkdir()
    (root / remote_module.LOCK_FILENAME).write_text("{corrupt lock", encoding="utf-8")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "install-root"))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-any"}})
    assert responses[0]["error"]["code"] == "plugin_lock_invalid"


def test_install_remote_already_installed_never_fetches(monkeypatch, tmp_path):
    """已装未 force → already_installed 且零网络(已装件不触发远取;装卸
    网络代价不花在注定拒绝的请求上)。"""
    root = tmp_path / "bundled"
    make_declaration_package(root, "myssia-prefetched", MINIMAL_MANIFEST.format(id="myssia-prefetched", name="预装件"))
    tarball = build_remote_tarball("myssia-prefetched", MINIMAL_MANIFEST.format(id="myssia-prefetched", name="预装件"))
    write_plugins_lock(root, {"myssia-prefetched": lock_entry_for(tarball, "myssia-prefetched")})
    patch_remote_transport(monkeypatch, refuse_network())
    install_root = tmp_path / "install-root"
    preinstalled = install_root / "myssia-prefetched"
    preinstalled.mkdir(parents=True)
    (preinstalled / "plugin.yaml").write_text(
        MINIMAL_MANIFEST.format(id="myssia-prefetched", name="预装件").replace("version: 1.0.0", "version: 0.9.0"),
        encoding="utf-8",
    )
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-prefetched"}})
    assert responses[0]["error"]["code"] == "already_installed"
    assert (preinstalled / "plugin.yaml").read_text(encoding="utf-8").count("0.9.0") >= 1  # 已装件零扰动


def test_install_legacy_installed_plugin_zero_disturbance_across_remote_ops(monkeypatch, tmp_path):
    """INV-6 端到端:已装旧件在远取链任何操作(成功装他件/失败装他件/列表/
    卸载他件)后逐字节不变;其卸载语义原样可用。"""

    def tree_digest(target: Path) -> dict[str, bytes]:
        return {str(p.relative_to(target)): p.read_bytes() for p in sorted(target.rglob("*")) if p.is_file()}

    root = tmp_path / "bundled"
    make_declaration_package(root, "myssia-newwave", MINIMAL_MANIFEST.format(id="myssia-newwave", name="新规件"))
    tarball = build_remote_tarball("myssia-newwave", MINIMAL_MANIFEST.format(id="myssia-newwave", name="新规件"))
    write_plugins_lock(root, {"myssia-newwave": lock_entry_for(tarball, "myssia-newwave")})
    patch_remote_transport(monkeypatch, serve(tarball))
    install_root = tmp_path / "install-root"
    legacy = install_root / "myssia-legacy"
    legacy.mkdir(parents=True)
    (legacy / "plugin.yaml").write_text(
        MINIMAL_MANIFEST.format(id="myssia-legacy", name="旧装件").replace("version: 1.0.0", "version: 0.8.0"),
        encoding="utf-8",
    )
    (legacy / "adapter.py").write_text("# legacy adapter untouched\n", encoding="utf-8")
    (legacy / "notes").mkdir()
    (legacy / "notes" / "local.txt").write_text("user data\n", encoding="utf-8")
    before = tree_digest(legacy)
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    # 成功远取他件
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-newwave"}})
    assert responses[0]["result"]["ok"] is True
    # 失败远取他件(坏钉)
    write_plugins_lock(root, {"myssia-newwave": lock_entry_for(tarball, "myssia-newwave", sha256="1" * 64)})
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-newwave", "force": True}})
    assert responses[0]["error"]["code"] == "integrity_mismatch"
    # 列表/卸载他件
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.list", "params": {}})
    _, responses, _ = rpc({"id": 4, "method": "plugins.bundled.uninstall",
                           "params": {"id": "myssia-newwave"}})
    assert responses[0]["result"]["ok"] is True
    assert tree_digest(legacy) == before, "已装旧件必须逐字节零扰动"
    # 旧件自身卸载照旧(安装根操作,语义零变化)
    _, responses, _ = rpc({"id": 5, "method": "plugins.bundled.uninstall",
                           "params": {"id": "myssia-legacy"}})
    assert responses[0]["result"]["ok"] is True
    assert not legacy.exists()


def test_install_lock_present_source_carrying_dir_falls_back_to_direct_copy(monkeypatch, tmp_path):
    """锁在场但该件无条目、而包内目录携带源码(过渡/旧包混锁形态)→ 直拷
    回退自愈(D3 第二分支),不因锁缺席硬拒。"""
    root = tmp_path / "bundled"
    pkg = make_bundled_package(root, "myssia-transition", MINIMAL_MANIFEST.format(id="myssia-transition", name="过渡件"))
    other_tarball = build_remote_tarball("myssia-other", MINIMAL_MANIFEST.format(id="myssia-other", name="他件"))
    write_plugins_lock(root, {"myssia-other": lock_entry_for(other_tarball, "myssia-other")})
    patch_remote_transport(monkeypatch, refuse_network())
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-transition"}})
    assert responses[0]["result"]["ok"] is True
    assert (install_root / "myssia-transition" / "adapter.py").exists()
    assert (pkg / "adapter.py").exists()  # 包内原件只读


# ---------------------------------------------------------------------------
# uninstall(批二 R2):删安装根拷贝 / dev 形态可卸 / 结构化拒
# ---------------------------------------------------------------------------


def _minimal_category_yaml(category_id: str) -> str:
    """最小合法品类 YAML(过 load_category 校验:sources 必非空)。"""
    return f"""id: {category_id}
name: 品类夹具 {category_id}
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:9/list"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.data[*].title"
        url: "$.data[*].url"
push:
  - channel: stdout
"""


def test_uninstall_removes_install_root_copy_only(monkeypatch, tmp_path):
    """卸载真删:安装根 <install_root>/<id> 整目录删除;应答 {ok,id,path};
    **随包原件只读永不删**(卸载语义=删安装根拷贝,可重装)。"""
    root = tmp_path / "bundled"
    pkg = make_bundled_package(root, "myssia-removable", MINIMAL_MANIFEST.format(id="myssia-removable", name="可卸件"))
    install_root = tmp_path / "install-root"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-removable"}})
    assert responses[0]["result"]["ok"] is True
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.uninstall",
                           "params": {"id": "myssia-removable"}})
    assert "result" in responses[0], f"卸载应答应为 result: {responses[0]}"
    assert responses[0]["result"] == {
        "ok": True, "id": "myssia-removable", "path": str(install_root / "myssia-removable"),
    }
    assert not (install_root / "myssia-removable").exists()  # 安装根拷贝已删
    assert (pkg / "plugin.yaml").exists()  # 随包原件未动
    # 卸载后 list installed 翻假
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.list", "params": {}})
    assert responses[0]["result"]["plugins"][0]["installed"] is False
    # 卸载后可重装(随包原件是重装来源)
    _, responses, _ = rpc({"id": 4, "method": "plugins.bundled.install",
                           "params": {"id": "myssia-removable"}})
    assert responses[0]["result"]["ok"] is True


def test_uninstall_not_installed_is_structured_reject(monkeypatch, tmp_path):
    """未装件卸载 → not_installed 结构化拒(PluginStoreError code 原文透传)。"""
    root = tmp_path / "bundled"
    make_bundled_package(root, "myssia-absent", MINIMAL_MANIFEST.format(id="myssia-absent", name="不在件"))
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "install-root"))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.uninstall",
                           "params": {"id": "myssia-absent"}})
    assert responses[0]["error"]["code"] == "not_installed"
    assert responses[0]["error"]["path"] == "params.id"


def test_uninstall_does_not_require_bundled_env(monkeypatch, tmp_path):
    """卸载不依赖随包目录(dev 形态/旧包 MYIA_BUNDLED_PLUGINS 未设同样可卸)——
    卸载是安装根操作,与发现来源无关(批二 R2 档记语义)。"""
    monkeypatch.delenv(entry.BUNDLED_PLUGINS_ENV, raising=False)
    install_root = tmp_path / "install-root"
    preinstalled = install_root / "myssia-orphan"
    preinstalled.mkdir(parents=True)
    (preinstalled / "plugin.yaml").write_text(
        MINIMAL_MANIFEST.format(id="myssia-orphan", name="孤儿件"), encoding="utf-8",
    )
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.uninstall",
                           "params": {"id": "myssia-orphan"}})
    assert responses[0]["result"]["ok"] is True
    assert not preinstalled.exists()


def test_uninstall_traversal_and_shape_are_rejected(monkeypatch, tmp_path):
    """穿越 id 先于任何查找拒(invalid_params);缺 id/非字符串同拒;
    路径精确到 params.id(与 install 同门)。"""
    install_root = tmp_path / "install-root"
    marker = tmp_path / "escape-marker.txt"
    marker.write_text("escape!\n", encoding="utf-8")
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(install_root))
    for bad_id in ("../escape-marker", "a/b", "..", "FOO", "x", "-leading-dash"):
        _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.uninstall",
                               "params": {"id": bad_id}})
        assert responses[0]["error"]["code"] == "invalid_params", f"{bad_id!r} 应被正则门拒"
        assert responses[0]["error"]["path"] == "params.id"
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.uninstall", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.id"
    assert marker.read_text(encoding="utf-8") == "escape!\n"  # 原件未被动


# ---------------------------------------------------------------------------
# categories 发现面 + category_install(批二 R3):平铺拷贝 / 已存在拒 /
# 与补种语义对齐
# ---------------------------------------------------------------------------


def _home_sandbox(monkeypatch, tmp_path) -> Path:
    """品类组沙箱:MYIA_HOME 指一次性根(plugins_dir=<home>/plugins 干净,
   品类安装落点 = 补种落点同款;dev 回退根是本机实况不净)。"""
    home = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(home))
    return home


def test_categories_bad_yaml_is_entry_level_finding(monkeypatch, tmp_path):
    """坏品类 YAML 条目级 finding(category_invalid)不整表炸:id=None 如实;
    好件照常在列(沿 yaml.list 先例)。"""
    root = tmp_path / "bundled"
    root.mkdir()
    (root / "good.yaml").write_text(_minimal_category_yaml("good"), encoding="utf-8")
    (root / "broken.yaml").write_text("id: 123\nschedule: not-a-cron\n", encoding="utf-8")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    _home_sandbox(monkeypatch, tmp_path)
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    result = responses[0]["result"]
    assert result["count"] == 0  # 组件包面零件(品类不是组件包)
    by_file = {cat["file"]: cat for cat in result["categories"]}
    assert by_file["good.yaml"]["id"] == "good"
    assert by_file["good.yaml"]["findings"] == []
    assert by_file["broken.yaml"]["id"] is None
    assert "category_invalid" in [f["code"] for f in by_file["broken.yaml"]["findings"]]
    # 组件包与品类两视图互不渗入:坏 manifest 目录不进 categories、坏 YAML 不进 plugins
    make_bundled_package(root, "myssia-pkg", MINIMAL_MANIFEST.format(id="myssia-pkg", name="包件"))
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.list", "params": {}})
    result = responses[0]["result"]
    assert result["count"] == 1
    assert {cat["file"] for cat in result["categories"]} == {"good.yaml", "broken.yaml"}


def test_category_install_copies_flat_file_into_plugins_dir(monkeypatch, tmp_path):
    """品类安装=单文件平铺拷贝:落 <home>/plugins/<源文件名>,内容逐字节一致,
    应答 {ok,file,path};tmp 中转不残留(原子替换不留 .tmp 残件)。"""
    root = tmp_path / "bundled"
    root.mkdir()
    (root / "flat-cat.yaml").write_text(_minimal_category_yaml("flat-cat"), encoding="utf-8")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    home = _home_sandbox(monkeypatch, tmp_path)
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.category_install",
                           "params": {"id": "flat-cat"}})
    assert responses[0]["result"] == {
        "ok": True, "file": "flat-cat.yaml", "path": str(home / "plugins" / "flat-cat.yaml"),
    }
    target = home / "plugins" / "flat-cat.yaml"
    assert target.read_text(encoding="utf-8") == (root / "flat-cat.yaml").read_text(encoding="utf-8")
    assert not (home / "plugins" / ".flat-cat.yaml.tmp").exists()
    # 随包原件未动 + list categories exists 翻真
    assert (root / "flat-cat.yaml").exists()
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.list", "params": {}})
    cat = responses[0]["result"]["categories"][0]
    assert cat["exists"] is True


def test_category_install_existing_without_force_rejected_force_overrides(monkeypatch, tmp_path):
    """已存在未 force → category_exists 结构化拒(如实「已存在」不覆盖);
    force=true → 覆盖内容翻新(用户手改件被随包版覆盖,知情操作)。"""
    root = tmp_path / "bundled"
    root.mkdir()
    (root / "dup-cat.yaml").write_text(_minimal_category_yaml("dup-cat"), encoding="utf-8")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    home = _home_sandbox(monkeypatch, tmp_path)
    plugins = home / "plugins"
    plugins.mkdir(parents=True)
    (plugins / "dup-cat.yaml").write_text("# 用户自建同名文件\n", encoding="utf-8")
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.category_install",
                           "params": {"id": "dup-cat"}})
    assert responses[0]["error"]["code"] == "category_exists"
    assert responses[0]["error"]["path"] == "params.id"
    assert (plugins / "dup-cat.yaml").read_text(encoding="utf-8") == "# 用户自建同名文件\n"  # 未覆盖
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.category_install",
                           "params": {"id": "dup-cat", "force": True}})
    assert responses[0]["result"]["ok"] is True
    assert (plugins / "dup-cat.yaml").read_text(encoding="utf-8") == _minimal_category_yaml("dup-cat")


def test_category_install_guards(monkeypatch, tmp_path):
    """防线矩阵:env 未设 → bundled_plugins_unavailable;穿越 id → invalid_params;
    id 合形不在目录 → bundled_category_not_found;坏 YAML 源 → category_invalid
    拒且数据根零文件;force 非布尔 → invalid_params。"""
    root = tmp_path / "bundled"
    root.mkdir()
    (root / "valid-cat.yaml").write_text(_minimal_category_yaml("valid-cat"), encoding="utf-8")
    (root / "bad-cat.yaml").write_text("id: bad-cat\nschedule: not-a-cron\n", encoding="utf-8")
    _home_sandbox(monkeypatch, tmp_path)
    # env 未设(dev 形态/旧包)
    monkeypatch.delenv(entry.BUNDLED_PLUGINS_ENV, raising=False)
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.category_install",
                           "params": {"id": "valid-cat"}})
    assert responses[0]["error"]["code"] == "bundled_plugins_unavailable"
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    # 穿越形(../x、大写、斜杠、前导连字符)与缺 id(CATEGORY_ID_RE 与
    # _PLUGIN_ID_RE 差异如实:品类门 1-64 字符,单字符 'x' 是合法形状归
    # not_found 组另断)
    for bad in ("../escape", "a/b", "FOO", "-dash"):
        _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.category_install",
                               "params": {"id": bad}})
        assert responses[0]["error"]["code"] == "invalid_params", f"{bad!r} 应被 CATEGORY_ID_RE 拒"
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.category_install", "params": {}})
    assert responses[0]["error"]["path"] == "params.id"
    # id 合形但目录内无此件(数字开头/单字符都是合法形状,归 not_found)
    for absent in ("123abc", "x"):
        _, responses, _ = rpc({"id": 4, "method": "plugins.bundled.category_install",
                               "params": {"id": absent}})
        assert responses[0]["error"]["code"] == "bundled_category_not_found"
    # 坏 YAML 源:拒装零拷贝
    _, responses, _ = rpc({"id": 5, "method": "plugins.bundled.category_install",
                           "params": {"id": "bad-cat"}})
    assert responses[0]["error"]["code"] == "category_invalid"
    assert not (tmp_path / "home" / "plugins" / "bad-cat.yaml").exists()
    # force 非布尔
    _, responses, _ = rpc({"id": 6, "method": "plugins.bundled.category_install",
                           "params": {"id": "valid-cat", "force": "yes"}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.force"


def test_category_install_locates_by_yaml_id_when_file_name_differs(monkeypatch, tmp_path):
    """id→文件定位双路:文件名 stem 直配 > YAML id 字段兜底(id_mismatch 件
    可达;安装按**源文件名**落平铺,保持文件名形状)。"""
    root = tmp_path / "bundled"
    root.mkdir()
    (root / "renamed-file.yaml").write_text(_minimal_category_yaml("real-cat-id"), encoding="utf-8")
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    home = _home_sandbox(monkeypatch, tmp_path)
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.category_install",
                           "params": {"id": "real-cat-id"}})
    assert responses[0]["result"]["file"] == "renamed-file.yaml"  # 按源文件名落
    assert (home / "plugins" / "renamed-file.yaml").exists()
    # 发现面对该件如实透 id_mismatch warning
    _, responses, _ = rpc({"id": 2, "method": "plugins.bundled.list", "params": {}})
    cat = responses[0]["result"]["categories"][0]
    assert cat["id"] == "real-cat-id"
    assert [f["code"] for f in cat["findings"]] == ["id_mismatch"]


def test_category_install_and_seed_semantics_aligned(monkeypatch, tmp_path):
    """与 _seed_first_run 幂等补缺对齐不打架(批二 R3 红线):

    - serve 启动补种自动补缺:14 件随包品类全落数据根(list exists 全翻真);
    - 补种绝不覆盖已存在文件:手改件逐字节保留(再跑一轮补种不动它);
    - 安装面对已存在件(补种拷的)未 force → category_exists 拒——两通道
      语义同向:自动面永不覆盖,显式面知情 force 才覆盖。
    """
    root = rebuild_bundled_tree(tmp_path / "Resources")
    home = _home_sandbox(monkeypatch, tmp_path)
    monkeypatch.setenv(entry.BUNDLED_PLUGINS_ENV, str(root))
    # 补种源锚点指同一树(测试态 _bundle_plugins_dir 布局探测恒 None,如实替换)
    monkeypatch.setattr(entry, "_bundle_plugins_dir", lambda: root)
    _, responses, _ = rpc({"id": 1, "method": "plugins.bundled.list", "params": {}})
    categories = responses[0]["result"]["categories"]
    assert len(categories) == 14
    assert all(cat["exists"] for cat in categories), "serve 启动补种应已把 14 件补齐"
    seeded = home / "plugins" / "ai-news.yaml"
    assert seeded.exists()
    # 手改件不被补种覆盖(幂等补缺,逐字节保留)
    seeded.write_text(seeded.read_text(encoding="utf-8") + "# local edit\n", encoding="utf-8")
    rpc({"id": 2, "method": "version", "params": {}})  # 再触发一轮 serve 启动补种
    assert seeded.read_text(encoding="utf-8").endswith("# local edit\n")
    # 安装面:补种已拷的件未 force 拒(如实「已存在」)
    _, responses, _ = rpc({"id": 3, "method": "plugins.bundled.category_install",
                           "params": {"id": "ai-news"}})
    assert responses[0]["error"]["code"] == "category_exists"
