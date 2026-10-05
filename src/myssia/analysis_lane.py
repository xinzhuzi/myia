"""分析 lane(analysis lane)—— ``_stage_analyze`` 阶段内的本地装饰件通道.

批三 D10 定案(task 10-05-plugin-market-batch,2026-10-05 主人令按建议执行):
情感/关键词等零 token 分析件挂在 **enrich 平行**位(dedup 之后、push 之前,
与 LLM 精评同位互补),不是 classify 后处理——classify 是过滤器(未命中即丢),
analyze 是装饰器(scoring decorates, it does not filter)。挂过滤器阶段会诱使
分析结果参与丢弃决策 → 分类结果依赖插件在位性 → 击穿「装不上不拦核心」铁律。

**lane ↔ gates.analysis 执法关系(D10-2:真执法,dispatch 级)**:

- 唯一激活路径 = 全局 ``<home>/gates.yaml`` 的 ``analysis.<key>`` 开关
  (:func:`myssia.gates.gate_open`;键名按 ``plugin_gate_key`` 官方惯例 =
  插件 id 去 ``myssia-`` 前缀);**gate 关 = 字面零开销**:不 import 插件码、
  不 spawn 子进程、条目零触碰,仅一次字典查找;
- **lane 关 = 正常未启用态**(doctor info + debug 日志),刻意不是 SaaS 引擎
  ``gate_closed`` 结构化失败——那是「被品类请求后被拒」的语义
  (engines/saas.py),lane 无此调用方;
- fail-closed:gates.yaml 缺失/损坏 = 全关 = lane 不跑(D2 永不缺省存活);
- 每轮 run 在 lane 入口重新装载(照 vision ring 每轮装载先例),设置面开关
  下一轮即生效。

**成员注册表**::data:`ANALYSIS_LANE_MEMBERS` 由核心维护(官方件谱系);
yake 不声明 manifest gate(上游活跃,stale 徽标失实),lane 成员资格一律按
本表判定,激活一律走 ``analysis.<key>``——缺省关闭来自 D2,不依赖 manifest
徽标(D10-2 实况修正)。

**adapter 契约**(插件 ``adapter.py`` 必须暴露的函数):

.. code-block:: python

    decorate(texts: list[dict[str, str]]) -> dict
    # 入参:[{"url": <去重键根基>, "text": <title+content 拼接>}, ...]
    # 返回:{"decorations": {<url>: {<metadata 字段名>: 值, ...}}, ...}

失败抛结构化异常(``.code`` 属性,词表照 urlwatch:``uv_missing`` /
``dependency_missing`` / ``*_failed`` / ``*_timeout`` / ``*_output_invalid``),
由 lane 统一转成 ``analysis_lane_degraded_<code>`` skip 计数 + report.warnings
降级注记——**绝不进 report.failures**(不翻 partial;enrich 条目级降级先例)。

装饰落 ``item.metadata``(route 规则/push 模板经 ``Item.view()`` 消费);
items 表回填 best-effort(store.merge_item_metadata,照 enricher
``update_item_scores`` 先例)。lane 装饰是 run 级重算,不进 checkpoint 载荷
(续跑条目 content 缺失时输入退化为 title-only)。
"""

from __future__ import annotations

import logging
import re
import types
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

__all__ = [
    "ANALYSIS_LANE_MEMBERS",
    "AnalysisLaneError",
    "decorate_items",
    "default_plugins_roots",
    "import_analysis_adapter",
    "lane_degrade_token",
    "locate_adapter_file",
]

logger = logging.getLogger(__name__)

#: 官方分析 lane 成员注册表:``gates.yaml analysis.<key>`` 键 → 插件包名。
#: 核心维护的封闭清单(新增成员 = 核心改动,非市场件自注册)——lane 成员
#: 资格是市场面(plugin list/doctor 启用徽标)与管线 dispatch 的共同依据。
ANALYSIS_LANE_MEMBERS: dict[str, str] = {
    "snownlp": "myssia-snownlp",
    "yake": "myssia-yake",
}

#: adapter 文件在插件包内的固定位置(manifest ``adapter.entry`` 同名约定)。
_ADAPTER_ENTRY = "adapter.py"

#: degrade 计数键的安全词形(``[a-z0-9_]+``;适配器自报 code 形态不可信时归一)。
_DEGRADE_TOKEN_RE = re.compile(r"[^a-z0-9_]+")


class AnalysisLaneError(Exception):
    """lane 件级/条目级失败的结构化形态(code + message + details)。

    适配器异常可以不是本类(lane 会取 ``exc.code`` 属性,缺省归
    ``adapter_error``);本类用于 lane 自身的装载/输出形状错误。
    """

    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, **self.details}


def lane_degrade_token(code: Any) -> str:
    """适配器错误码 → skip 计数键的安全词形(``analysis_lane_degraded_<token>``)。"""
    text = _DEGRADE_TOKEN_RE.sub("_", str(code or "adapter_error").strip().lower())
    return text.strip("_") or "adapter_error"


def default_plugins_roots(data_root: Path | str | None = None) -> list[Path]:
    """adapter 发现的候选根(先后有序):CLI cwd ``plugins`` > 数据根 ``plugins``。

    与 credhunter 引擎的 cwd 相对约定及桌面 ``<home>/plugins`` 安装根
    (InstalledPluginStore)各占一半——零新配置面,两个发行形态都天然可达。
    """
    roots = [Path.cwd() / "plugins"]
    if data_root is not None:
        roots.append(Path(data_root) / "plugins")
    # 去重(cwd == 数据根时同一目录扫两遍没有意义)
    seen: set[Path] = set()
    unique: list[Path] = []
    for root in roots:
        resolved = root.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(root)
    return unique


def locate_adapter_file(plugins_roots: Sequence[Path], package_id: str) -> Path | None:
    """按候选根顺序定位 ``<root>/<package_id>/adapter.py``;找不到 = None。"""
    for root in plugins_roots:
        candidate = Path(root) / package_id / _ADAPTER_ENTRY
        if candidate.is_file():
            return candidate
    return None


def import_analysis_adapter(adapter_file: Path | str) -> types.ModuleType:
    """compile+exec 加载一个分析 lane 插件 adapter(credhunter 同手法)。

    插件目录不是 Python 包,不走 SourceFileLoader(会在插件目录写
    ``__pycache__`` 垃圾);核心仓库与插件零静态耦合。加载失败抛
    OSError/SyntaxError,由调用方统一转 lane 降级注记。
    """
    path = Path(adapter_file)
    module = types.ModuleType(f"myssia_analysis_lane_{path.parent.name}")
    module.__file__ = str(path)
    executable = compile(path.read_text(encoding="utf-8"), str(path), "exec")
    exec(executable, module.__dict__)  # noqa: S102 - 仓库内受控插件代码,非任意输入
    return module


def decorate_items(adapter: Any, texts: list[dict[str, str]]) -> dict[str, dict[str, Any]]:
    """调用一个 adapter 的 ``decorate(texts)`` 并校验输出形状。

    Returns:
        ``decorations`` 映射:{url: {metadata 字段: 值}}(只保留可 JSON 化的
        字典型条目;单个 url 的装饰形状不对则跳过该条并 debug 记录——件内
        个别坏输出不废整件)。

    Raises:
        AnalysisLaneError: ``analysis_output_invalid``——适配器抛错(带原始
            code 透传为 details)或整体输出形状不对。
    """
    try:
        payload = adapter.decorate(texts)
    except AnalysisLaneError:
        raise
    except Exception as exc:  # noqa: BLE001 - 适配器任何异常 = 件级降级,不拦管线
        code = getattr(exc, "code", None)
        raise AnalysisLaneError(
            lane_degrade_token(code) if code else "adapter_error",
            f"分析 lane 适配器执行失败:{exc}",
            adapter_code=code,
        ) from exc
    if not isinstance(payload, Mapping):
        raise AnalysisLaneError(
            "output_invalid",
            f"分析 lane 适配器输出必须是含 decorations 的映射,当前为 {type(payload).__name__}",
        )
    raw = payload.get("decorations")
    if not isinstance(raw, Mapping):
        raise AnalysisLaneError(
            "output_invalid",
            "分析 lane 适配器输出缺少 decorations 映射(契约:{{'decorations': {{url: {{字段: 值}}}}}})",
        )
    decorations: dict[str, dict[str, Any]] = {}
    for url, fields in raw.items():
        if not isinstance(url, str) or not isinstance(fields, Mapping):
            logger.debug("分析 lane 装饰形状不对,跳过该条 url=%r", url)
            continue
        decorations[url] = dict(fields)
    return decorations
