"""随包交付物清单一致性(10-05-desktop-managed-py-env implement.md 第 1 条门)。

覆盖四件事(全部离线,零外网):

1. ``tauri.conf.json`` resources 段:自管环境五映射已声明且源路径磁盘实况
   存在;既有官方插件种子映射(首跑种子依赖)不被挤掉。
   1b. 组件注册表 ``components.json`` 随包映射 + 契约形态(10-05-table-restore
   R4;首件 table 钉版在册)。
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
    assert resources.get(source) == dest, (
        f"resources 缺映射 {source!r} -> {dest!r}(实得 {resources.get(source)!r})"
    )
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
# 1b. 组件注册表 components.json(10-05-table-restore 桌面侧 R4):随包映射
#     + 契约形态(壳侧 pyenv_components.rs 读同文件宽容解析;此处钉「形」
#     与首件钉版,防注册表被无声挤掉或改坏——壳侧宽容读取会把坏文件吞成
#     空表,组件开关整面静默消失,故须仓测钉死)。
# ---------------------------------------------------------------------------

#: 表格还原组件闭包与钉版(pip_spec 可含空格分隔多条 spec,逐条作 pip install
#: 位置参数)。**跟引擎 API 走**(质检高危修正:组件消费者是
#: src/myssia/vision/table.py,按 rapid_table 3.x API 写——裸 RapidTable()/
#: ocr_results= 复数/pred_htmls 复数;1.0.3 虽模型随轮但 __init__ 必传
#: RapidTableInput、ocr_result/pred_html 单数,三处调用面全断)。主件钉
#: ==3.0.2 落在 extras >=3.0.2,<4 内;rapidocr-onnxruntime 供单元格文字
#: (引擎显式喂 ocr_results 绕开其内置新版 rapidocr 通道)、tqdm 是 3.0.2
#: 轮隐性 import(extras 显式补)——裸装主件会让引擎 dependency_missing,
#: 故闭包必须与 extras myssia[table] 三件同源(交叉对齐测试把守)。
TABLE_COMPONENT_PIP_SPEC = "rapid-table==3.0.2 rapidocr-onnxruntime>=1.3 tqdm>=4"

#: 正文抽取兜底组件闭包(10-05-bundled-plugins-batch2 R1):与 pyproject
#: extras ``myssia[trafilatura]`` 逐字符同字串——主件也用 extras 原窗
#: ``>=2.3,<3`` 不钉版(与 table 主件钉 ==3.0.2 不同:trafilatura extras
#: 本身是双约束窗,组件侧钉版会造出第三种口径;selectolax<1 钉版不可省,
#: 防 1.0.0 撞 Modest 解析器移除墙,保护 MYIA extract_html 面)。
TRAFILATURA_COMPONENT_PIP_SPEC = "trafilatura>=2.3,<3 selectolax<1"

#: JS 渲染抓取组件闭包(10-06-native-plugin-components 轨A,裁决③):主件窗
#: ``>=0.9,<0.10``——本仓 uv.lock/dev 实测 0.9.4,引擎(crawl4ai.py 的
#: MarkdownGenerationResult 鸭子兼容)与 render_crawl4ai 场景件均按 0.9.x
#: 探测写作;0.10+ 未验不冒进。闭包单件与 extras ``myssia[crawl4ai]``
#: 同源(crawl4ai 自带 playwright 依赖,不另钉第三口径);浏览器二进制
#: 不走 pip(安装链 post_install 钩子拉 chromium,壳侧
#: pyenv_components.rs 把守)。
CRAWL4AI_COMPONENT_PIP_SPEC = "crawl4ai>=0.9,<0.10"

#: post_install 钩子已知值词表(壳侧 install_component 对未知值结构化拒;
#: 此处钉上游不产未知值——壳侧拒绝发生在用户点安装之后,仓测先拦拼写漂移)。
KNOWN_POST_INSTALL_HOOKS = {"playwright-chromium", "pip-src-no-build-isolation"}

#: pre_start 钩子已知值词表(壳侧 start_service_process 对未知值结构化拒;
#: 钩子配套字段缺失同样安装期先拦——此处钉上游注册表不产漂移形态)。
KNOWN_PRE_START_HOOKS = {"searxng-settings"}

#: 组件 kind 已知值词表(缺省 = 轨A 库组件;"service" = 轨B 壳服务组件,
#: 须伴随 service 节且节点键齐全——壳侧动作期校验,这里上游先拦形态漂移)。
KNOWN_COMPONENT_KINDS = {None, "service"}

#: SearXNG 上游钉 commit(=引擎探查实例 2026.10.4+d48c4b555 的同 commit;
#: searxng 真身不在 PyPI,git 钉 commit 是唯一可复现安装锚点)。
SEARXNG_SOURCE_COMMIT = "d48c4b555421e824342c51d68482dd0898e54d0f"


def test_components_resource_declared_and_present() -> None:
    """components.json 随包映射已声明且源文件在盘。"""
    source, dest = "../resources/components.json", "components.json"
    resources = _conf_resources()
    assert resources.get(source) == dest, (
        f"resources 缺映射 {source!r} -> {dest!r}(实得 {resources.get(source)!r})"
    )
    assert (SRC_TAURI / source).is_file(), f"映射源不存在: {source}"


def test_components_registry_shape() -> None:
    """注册表契约形态:{components:[{id,pip_spec,label,description}]},首件
    table 钉版在册(id/pip_spec/label/description 非空;壳侧过滤半截条目,
    这里钉上游不产半截)。

    形状正则的约束段是 ``[^\s]+`` 整段——天然容忍逗号多约束 token(如
    ``trafilatura>=2.3,<3``),无需为多约束单列语法;此处遍历**全部条目**
    (不止 table)做形状检查,后续加件自动纳管。10-06 阶段2 起扩充两类
    词形(10-06-native-plugin-components 轨B):① ``-r <requirements URL>``
    (一段闭包经 pip -r 装上游钉版清单;URL 必须 commit 钉版——浮 tag/ref
    形态即安装不可复现,红);② ``name@git+https://…@<40 位 hex>``(PEP508
    直引 git commit 钉,无空格形态——组件 spec 按空格分词,带空格的
    ``name @ url`` 会被拆成两条废 spec)。"""
    registry = json.loads(
        (RESOURCES_DIR / "components.json").read_text(encoding="utf-8")
    )
    assert isinstance(registry.get("components"), list), "components 须为数组"
    ids = [entry.get("id") for entry in registry["components"]]
    assert "table" in ids, f"首件 table 必须在册(实得 {ids})"
    for entry in registry["components"]:
        assert isinstance(entry, dict), f"条目须为对象: {entry!r}"
        for key in ("id", "pip_spec", "label", "description"):
            assert isinstance(entry.get(key), str) and entry[key], (
                f"条目缺非空 {key}: {entry!r}"
            )
        # post_install 钩子(可选字段):在场必须是壳已知值——壳侧对未知值
        # 在用户点安装后才拒,此处上游先拦(壳已知值见 pyenv_components.rs)。
        if "post_install" in entry:
            assert entry["post_install"] in KNOWN_POST_INSTALL_HOOKS, (
                f"post_install 未知值(壳侧会拒装): {entry['post_install']!r}"
            )
        # pre_start 钩子(可选字段;轨B 服务启动前件生成,同 post_install 惯例)
        if "pre_start" in entry:
            assert entry["pre_start"] in KNOWN_PRE_START_HOOKS, (
                f"pre_start 未知值(壳侧启动期会拒): {entry['pre_start']!r}"
            )
        # kind(可选字段):缺省 = 轨A 库组件;"service" = 轨B 壳服务组件,
        # 须伴随 service 节且节点键齐全(壳侧动作期校验——这里上游先把
        # 形态漂移拦掉)。
        assert entry.get("kind") in KNOWN_COMPONENT_KINDS, (
            f"组件 kind 未知值: {entry.get('kind')!r}(壳已知值: {sorted(map(str, KNOWN_COMPONENT_KINDS))})"
        )
        if entry.get("kind") == "service":
            service = entry.get("service")
            assert isinstance(service, dict), (
                f"kind=service 条目缺 service 节: {entry!r}"
            )
            assert (
                isinstance(service.get("start_cmd"), list) and service["start_cmd"]
            ), f"service.start_cmd 须非空 argv 数组: {service!r}"
            assert all(
                isinstance(token, str) and token for token in service["start_cmd"]
            ), f"service.start_cmd 须非空串数组: {service!r}"
            assert isinstance(service.get("health_url"), str) and service[
                "health_url"
            ].startswith("http"), f"service.health_url 须 http URL: {service!r}"
            assert isinstance(service.get("port"), int), (
                f"service.port 须整数: {service!r}"
            )
            if "pip_src" in entry:
                assert isinstance(entry["pip_src"], str) and entry["pip_src"], (
                    f"pip_src 须非空串: {entry!r}"
                )
        # pip spec 形状:闭包逐条钉版/约束词形,或 -r URL、git 直引两类轨B 词形。
        for token in entry["pip_spec"].split():
            is_pinned = re.match(
                r"^[A-Za-z0-9][A-Za-z0-9._-]*(==[^\s]+|>=?[^\s]+|<=?[^\s]+|!=+[^\s]+|~=+[^\s]+)$",
                token,
            )
            is_requirements_url = re.match(
                rf"^(-r|https://raw\.githubusercontent\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/[0-9a-f]{{40}}/[^\s]+)$",
                token,
            )
            is_git_direct_ref = re.match(
                rf"^[A-Za-z0-9][A-Za-z0-9._-]*@git\+https://[^\s]+@[0-9a-f]{{40}}$",
                token,
            )
            assert is_pinned or is_requirements_url or is_git_direct_ref, (
                f"spec 形状不符(钉版/约束/-r URL/git 直引四类词形外): {token!r}"
            )
    table = next(entry for entry in registry["components"] if entry["id"] == "table")
    assert table["pip_spec"] == TABLE_COMPONENT_PIP_SPEC, (
        f"table 闭包漂移: {table['pip_spec']!r}"
    )


def test_table_component_matches_pyproject_extras() -> None:
    """桌面组件闭包 ↔ pyproject extras ``myssia[table]`` 交叉对齐(红线)。

    质检高危「桌面钉 1.0.3 / 引擎按 3.x API 写」的根因是两侧并行未对齐;
    本测试把「组件消费者是引擎」钉成仓测:闭包逐件与 extras 同名、主件钉版
    满足 extras 约束、伴生件字串与 extras 逐字符一致——任一侧漂移即红。
    """
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    extras_raw = pyproject["project"]["optional-dependencies"]["table"]
    extras = {
        _pep503(str(Requirement(raw).name)): str(Requirement(raw)) for raw in extras_raw
    }
    desktop = {
        _pep503(str(Requirement(token).name)): token
        for token in TABLE_COMPONENT_PIP_SPEC.split()
    }
    assert set(desktop) == set(extras), (
        f"闭包件集与 extras 不一致: 桌面 {sorted(desktop)} vs extras {sorted(extras)}"
        "(裸装主件会让引擎 dependency_missing 于伴生件)"
    )
    for name, desktop_raw in desktop.items():
        extras_req = Requirement(extras[name])
        desktop_req = Requirement(desktop_raw)
        if str(desktop_req.specifier) == str(extras_req.specifier):
            continue  # 伴生件:与 extras 完全同字串
        # 主件允许更严(钉版),但钉的版本必须落在 extras 约束内
        pinned = list(desktop_req.specifier)
        assert len(pinned) == 1 and pinned[0].operator == "==", (
            f"{name} 桌面侧须钉版(==)或与 extras 同字串: {desktop_raw!r}"
        )
        assert extras_req.specifier.contains(pinned[0].version, prereleases=True), (
            f"{name} 桌面钉版 {pinned[0].version} 不满足 extras 约束 "
            f"{extras_req.specifier}(代差即引擎三处调用面全断)"
        )


def test_trafilatura_component_matches_pyproject_extras() -> None:
    """桌面组件闭包 ↔ pyproject extras ``myssia[trafilatura]`` 交叉对齐
    (10-05-bundled-plugins-batch2 R1)。

    与 table 的三方锁(tests/cli/test_cli_full.py
    test_table_component_closure_three_way)对照,本件**如实降为两方**:
    doctor 探测面不存在——trafilatura 是 env 开关件(``MYIA_EXTRACT_FALLBACK``,
    static_html.py 惰性 import + 缺装结构化降级),不是 images.table 式品类
    声明件,cli.py 无探测清单可锁;pyenv 侧(pyenv_components.rs
    ``load_registry``)全动态零 id 锁(实测无注册表 id 硬编码,测试常量
    TABLE_PIP_SPEC 只是测试基准)——两侧锁面 = extras 字串与注册表 pip_spec
    **逐字符一致**(主件用 extras 原窗 ``>=2.3,<3``,不引入第三种钉版口径;
    sorted 对比避免 Requirement 归一化重排 ``<3,>=2.3`` 造成假阴/假阳)。
    """
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    extras_raw = list(pyproject["project"]["optional-dependencies"]["trafilatura"])
    registry = json.loads(
        (RESOURCES_DIR / "components.json").read_text(encoding="utf-8")
    )
    entry = next(e for e in registry["components"] if e["id"] == "trafilatura")
    assert entry["pip_spec"] == TRAFILATURA_COMPONENT_PIP_SPEC, (
        f"trafilatura 闭包漂移: {entry['pip_spec']!r}"
    )
    # 逐字符同字串:token 原文排序后与 extras 原文排序后相等(不经 Requirement
    # 归一化——它会把 >=2.3,<3 重排成 <3,>=2.3,比不出「同字串」)。
    assert sorted(entry["pip_spec"].split()) == sorted(extras_raw), (
        f"闭包与 extras 不逐字符同字串: 桌面 {sorted(entry['pip_spec'].split())} "
        f"vs extras {sorted(extras_raw)}(任一侧漂移即红)"
    )
    # label/description 人话在册(R1:开关与缺省态必须写进描述)
    assert entry["label"] == "正文抽取兜底"
    assert "MYIA_EXTRACT_FALLBACK" in entry["description"], "描述须写明开关环境变量"


# ---------------------------------------------------------------------------
# 1c. crawl4ai 组件行(10-06-native-plugin-components 轨A,裁决③ + G-Q6):
#     钉窗闭包 + post_install 浏览器钩子声明 + 体积/落点/卸载三披露。
# ---------------------------------------------------------------------------


def test_crawl4ai_component_row_contract() -> None:
    """crawl4ai 组件行:pip_spec 钉窗在册 + post_install 钩子声明 +
    G-Q6 三披露(体积 300MB 级 / 落点数据根 playwright-browsers +
    PLAYWRIGHT_BROWSERS_PATH / 卸载即整目录消)——主人磁盘敏感,本轮任务
    起因,披露缺失即红。"""
    registry = json.loads(
        (RESOURCES_DIR / "components.json").read_text(encoding="utf-8")
    )
    entry = next(e for e in registry["components"] if e["id"] == "crawl4ai")
    assert entry["pip_spec"] == CRAWL4AI_COMPONENT_PIP_SPEC, (
        f"crawl4ai 闭包漂移: {entry['pip_spec']!r}"
    )
    assert entry["post_install"] == "playwright-chromium", (
        "浏览器钩子必须声明(否则装完缺 chromium 二进制,render 链起不来)"
    )
    description = entry["description"]
    assert "300MB" in description, "须明示 chromium 下载体积(G-Q6)"
    assert "playwright-browsers" in description, "须明示落点数据根浏览器目录(G-Q6)"
    assert "PLAYWRIGHT_BROWSERS_PATH" in description, "须写明注入变量名(落点机制)"
    assert "卸载" in description and "整目录" in description, (
        "须明示卸载组件即整目录回收(G-Q6)"
    )


def test_crawl4ai_component_window_within_extras() -> None:
    """桌面钉窗 ↔ extras ``myssia[crawl4ai]`` 交叉对齐(红线,table 同款)。

    extras 本身无约束(纯 ``crawl4ai``)——组件侧窗是收窄不是第三口径:
    件集与 extras 同源(单件),窗覆盖本仓实测 0.9.4、排除 0.10+/0.8.x
    未验线;壳侧指纹随 pip_spec 整串,两侧漂移即 installed=false 引导重装。
    """
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    extras_raw = pyproject["project"]["optional-dependencies"]["crawl4ai"]
    extras = {
        _pep503(str(Requirement(raw).name)): Requirement(raw) for raw in extras_raw
    }
    desktop = {
        _pep503(str(Requirement(token).name)): Requirement(token)
        for token in CRAWL4AI_COMPONENT_PIP_SPEC.split()
    }
    assert set(desktop) == set(extras), (
        f"闭包件集与 extras 不一致: 桌面 {sorted(desktop)} vs extras {sorted(extras)}"
    )
    window = desktop["crawl4ai"].specifier
    assert window.contains("0.9.4") and window.contains("0.9.99"), (
        f"窗应覆盖 0.9.x 实测线: {window}"
    )
    assert not window.contains("0.10.0") and not window.contains("0.8.9"), (
        f"窗应排除未验线(0.10+ 与 0.8.x): {window}"
    )


# ---------------------------------------------------------------------------
# 1d. searxng 服务组件行(10-06-native-plugin-components 阶段2 轨B,design §2
#     + G-Q5/G-Q6):两段装闭包 + granian 服务端 + 声明/健康端点/启动前件钩子
#     三披露锚点。上游现实(2026-10-06 实测):searxng 真身不在 PyPI(同名包
#     是无关 MCP 包装器),git 钉 commit d48c4b555(=引擎探查实例
#     2026.10.4+d48c4b555)是唯一可复现安装锚点。
# ---------------------------------------------------------------------------


def _searxng_entry() -> dict:
    registry = json.loads(
        (RESOURCES_DIR / "components.json").read_text(encoding="utf-8")
    )
    return next(e for e in registry["components"] if e["id"] == "searxng")


def test_searxng_component_row_closure_pinned_to_probe_instance_commit() -> None:
    """两段装闭包逐 token 对账:

    - 一段(依赖闭包):``-r <该 commit 的 requirements.txt 原文 URL>`` +
      ``granian==2.8.3``(上游当前 master 服务端;arm64 轮在场,沙箱实测
      起服务/healthz/json 全通)+ ``setuptools wheel``(二段装的构建后端
      ——上游 setup.py 构建期 import searx,缺它们 --no-build-isolation
      必败);
    - 二段(源码包,pip_src 字段):``searxng@git+…@<commit>`` 直引钉版。

    commit 与引擎探查实例同 commit——注册表漂移即红(引擎行为基准与组件
    安装锚点必须同线)。
    """
    entry = _searxng_entry()
    assert entry["kind"] == "service", (
        f"searxng 必须是 kind=service 服务组件: {entry!r}"
    )
    assert entry["post_install"] == "pip-src-no-build-isolation", (
        "两段装钩子必须声明(缺它只装了依赖闭包,searx 源码包不在场)"
    )
    closure = entry["pip_spec"].split()
    assert closure[0] == "-r", f"一段闭包必须以 -r 打头(上游钉版清单): {closure!r}"
    assert closure[1] == (
        f"https://raw.githubusercontent.com/searxng/searxng/{SEARXNG_SOURCE_COMMIT}"
        "/requirements.txt"
    ), f"-r URL 必须 commit 钉版: {closure[1]!r}"
    assert "granian==2.8.3" in closure, f"granian 服务端须在一段闭包(钉版): {closure!r}"
    assert "setuptools>=75" in closure and "wheel>=0.45" in closure, (
        f"二段装的构建后端(钉下限的约束形态)必须在一段闭包(--no-build-isolation 的前提): {closure!r}"
    )
    assert entry["pip_src"] == (
        f"searxng@git+https://github.com/searxng/searxng.git@{SEARXNG_SOURCE_COMMIT}"
    ), f"pip_src 必须 commit 钉版直引(与引擎探查实例同线): {entry['pip_src']!r}"


def test_searxng_service_spec_matches_upstream_serving_shape() -> None:
    """服务声明与上游服务形态对账(2026-10-06 master 实测:``searx.webserver``
    已被上游移除,现役服务端是 granian 的 WSGI 接口;entrypoint.sh 的 exec
    形态 = ``granian searx.webapp:app``):

    - start_cmd = ``-m granian --interface wsgi --host 127.0.0.1 --port 8888
      searx.webapp:app``(本机回环绑定——桌面服务组件不给外部网络面);
    - health_url 与 port 声明一致(127.0.0.1:8888;/healthz 上游是纯文本
      200,零上游搜索成本);
    - env 注入 SEARXNG_SETTINGS_PATH 指向 ``{service_dir}/settings.yml``
      (壳侧生成器落点;占位符形态——注册表保持数据根无关)。
    """
    entry = _searxng_entry()
    service = entry["service"]
    assert service["start_cmd"] == [
        "-m",
        "granian",
        "--interface",
        "wsgi",
        "--host",
        "127.0.0.1",
        "--port",
        "8888",
        "searx.webapp:app",
    ], f"start_cmd 必须与上游 granian WSGI 形态同源(本机回环): {service['start_cmd']!r}"
    assert service["health_url"] == "http://127.0.0.1:8888/healthz"
    assert service["port"] == 8888, "port 声明须与 health_url/start_cmd 的 8888 一致"
    assert service["env"] == {"SEARXNG_SETTINGS_PATH": "{service_dir}/settings.yml"}, (
        f"env 必须恰好注入 settings 路径(占位符形态): {service['env']!r}"
    )
    assert entry["pre_start"] == "searxng-settings", (
        "启动前件生成钩子必须声明(缺它服务起不来——json format 默认不开)"
    )


def test_searxng_component_row_gq6_disclosures() -> None:
    """G-Q6 三披露(主人磁盘敏感,本轮任务起因;披露缺失即红):

    - 体积:闭包约 100MB 级实测数字入文案(无浏览器/chromium 量级下载——
      与 crawl4ai 的 300MB/600MB 级对比是用户决策面);
    - 落点:数据根 services/searxng/(服务数据)+ site-packages(闭包,
      数据根 python/ 下)——不散落系统缓存区;
    - 卸载/回收:清数据根即整目录回收;+ G-Q5 手动启停语义(装好默认停,
      引擎不隐式拉起)与 git 源(需可及 github.com,不走 PyPI 镜像)如实
      披露。
    """
    description = _searxng_entry()["description"]
    assert "100MB" in description, f"须明示闭包实测体积(G-Q6): {description!r}"
    assert "services/searxng" in description, (
        f"须明示服务数据落点(G-Q6): {description!r}"
    )
    assert "数据根" in description and "整目录" in description, (
        f"须明示清数据根即整目录回收(G-Q6): {description!r}"
    )
    assert "默认停" in description or "装好默认停" in description, (
        f"须披露 G-Q5 手动启停语义(装好默认停): {description!r}"
    )
    assert "不隐式拉起" in description, f"须披露引擎不隐式拉起(G-Q5): {description!r}"
    assert "github.com" in description, f"须如实披露 git 源(网络前提;不走 PyPI 镜像)"


# ---------------------------------------------------------------------------
# 2. runtime-manifest.json:钉版 URL + 实算 sha256 + 解压布局
# ---------------------------------------------------------------------------


def _manifest() -> dict:
    data = json.loads(
        (RESOURCES_DIR / "runtime-manifest.json").read_text(encoding="utf-8")
    )
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
        assert entry["extract_root_dir"] == "python", (
            f"{key}: install_only 应解压出 python/ 根目录"
        )
        assert entry["python_bin"] == expected_bins[key]
        assert entry["python_bin"].startswith(entry["extract_root_dir"] + "/")


# ---------------------------------------------------------------------------
# 3. requirements-lock.txt ↔ pyproject dependencies 一致性
# ---------------------------------------------------------------------------


def _lock_pins() -> dict[str, str]:
    """解析锁版清单:仅取 ``name==version`` 顶格行(注释/续行/标记剥掉)。"""
    pins: dict[str, str] = {}
    for raw in (
        (RESOURCES_DIR / "requirements-lock.txt")
        .read_text(encoding="utf-8")
        .splitlines()
    ):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        assert (
            not line.startswith("-e") and "file:" not in line and "://" not in line
        ), f"桌面锁版清单不得含 editable/路径/URL 依赖: {raw!r}"
        pinned = line.split(";", 1)[0].strip()
        name, sep, version = pinned.partition("==")
        assert sep, f"非钉版行(须 name==version): {raw!r}"
        pins[_pep503(name.strip())] = version.strip()
    return pins


def test_requirements_lock_covers_pyproject_dependencies() -> None:
    """pyproject 每条直接依赖:锁版清单有钉版行,且版本满足约束(锁=约束的冻结)。"""
    pyproject = tomllib.loads(
        (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
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
        "myssia_desktop_entry",
        pkg_dir / "__init__.py",
        submodule_search_locations=[str(pkg_dir)],
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("myssia_desktop_entry", module)
    spec.loader.exec_module(module)
    return module


def _load_entry_direct():
    """与 tests/desktop/test_desktop_sidecar_protocol.py 同手法直载 entry.py。"""
    spec = importlib.util.spec_from_file_location(
        "pyenv_parity_entry", DESKTOP / "entry.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_entry_package_reuses_entry_protocol_surface() -> None:
    """协议面零漂移:装载目标就是 desktop/entry.py,方法集/协议版本与直载一致。"""
    pkg = _load_entry_package()
    assert pkg.ENTRY_PY == DESKTOP / "entry.py", (
        "开发树布局:入口包应定位同目录的 entry.py"
    )
    reused = pkg.load_entry_module()
    direct = _load_entry_direct()
    assert reused.PROTOCOL_VERSION == direct.PROTOCOL_VERSION
    assert sorted(reused._HANDLERS) == sorted(direct._HANDLERS), (
        "方法集漂移:装载目标不是同一 entry.py?"
    )
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
    assert proc.returncode == 0, (
        f"serve 退出码 {proc.returncode};stderr={proc.stderr[-2000:]}"
    )
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
    assert proc.returncode == 0, (
        f"--version 退出码 {proc.returncode};stderr={proc.stderr[-2000:]}"
    )
    assert proc.stdout.strip().startswith("myssia "), proc.stdout
