"""Built-in seven-category classifier: the zero-token first funnel.

Faithful port of the production crawler's keyword classifier (Huawei-cloud
``wf_crawl.py`` v3.1, keyword tables at their 2026-10-20 revision), semantics
verified by running the production ``cat_of`` over the real corpus (gold set
re-measured 2026-10-24). Keyword tables live in ``data/keywords.json`` so the
owner or an AI can tune them without code changes; this module loads the
tables and runs the adjudication. The adjudication *order* itself is code
(production semantics), with the charity/cloud/lure inline regexes ported
verbatim from ``wf_crawl.py``:

1. dead -> noise -> fake filters -> discard (category ``None``)
   (fake = 2026-10-20 假信号: 听说/盘点/合集… even when the title says 免费)
2. registration lure: title contains 注册 without any direct-give signal
   -> discard (blocks "register xxx" bait posts)
3. free signal (freebie hard-threshold table union direct-give) branch:
   a. 公益/倍率0 hit -> ``freebie`` (charity exempts the paid signal)
   b. cloud-server family hit and not paid -> ``freebie`` (2026-10-17
      cloud-first ruling, takes precedence over the token context)
   c. token-context hit -> ``token``
   d. not paid -> ``freebie``; otherwise the branch yields nothing and the
      title falls through to the primary scan below
4. no free signal (or free branch fell through): primary categories scanned
   in priority order (credit-card -> proxy-node -> buying-agent -> server ->
   token — 2026-10-24: token joins the loop, apikey/额度 titles reach
   ``token`` without any free signal, matching production v3.1)
5. paid/lure cut (2026-10-03 五刀, owner ruling 2026-10-24 Q1): paid hit or
   lure words (中转/relay/逆向/号池/接入了/api站/聚合/车队/纳新/低价/优惠)
   -> discard; ``channel`` is no longer a destination (the category row
   stays in the table as a retired legacy label only)
6. fallback scan -> the configured ``fallback_target`` (ai-news)
7. otherwise ``None`` -- the caller decides whether to drop the item

Known divergence from production v3.1 (deliberate, design §2 ruling):
production's no-free loop checks 🤖AI信息 *before* the paid/lure cut, so
titles like 「v0.4.2 发布」 land in ai-news; MYIA cuts paid/lure first —
the five-knife intent (付费广告整体砍) wins over the loop-order artifact.
The four affected gold cases record the divergence in their descriptions.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "ALL_CATEGORIES",
    "BuiltinResult",
    "CATEGORY_CHANNEL",
    "ClassifyDataError",
    "ClassifyTable",
    "DEFAULT_TABLE_PATH",
    "MatchEvidence",
    "SEVEN_CATEGORIES",
    "category_label",
    "classify_title",
    "load_table",
]

logger = logging.getLogger(__name__)

#: The seven MYIA categories (kept stable, pinned by tests/test_smoke.py).
SEVEN_CATEGORIES: list[str] = [
    "credit-card",
    "proxy-node",
    "buying-agent",
    "server",
    "token",
    "ai-news",
    "freebie",
]

#: Eighth production label — RETIRED as a destination (owner ruling
#: 2026-10-24 Q1: paid/lure titles are discarded, ``channel`` is never
#: assigned). The id stays in the category universe for legacy-label
#: compatibility (label lookup, main-package route mapping).
CATEGORY_CHANNEL = "channel"

ALL_CATEGORIES: list[str] = [*SEVEN_CATEGORIES, CATEGORY_CHANNEL]

DEFAULT_TABLE_PATH = Path(__file__).resolve().with_name("data") / "keywords.json"

_STAGE_FREE_TARGET = "free_target"
_STAGE_PRIMARY = "primary"
_STAGE_PAID_TARGET = "paid_target"
_STAGE_FALLBACK = "fallback"
_KNOWN_STAGES = frozenset(
    {_STAGE_FREE_TARGET, _STAGE_PRIMARY, _STAGE_PAID_TARGET, _STAGE_FALLBACK}
)

_TABLE_TOP_KEYS = frozenset({"version", "description", "categories", "signals", "filters", "adjudication"})
_SECTION_KEYS = frozenset({"keywords", "patterns", "case_insensitive", "target_category", "description"})

#: keywords.json table version this loader accepts (v2 ships with the
#: 2026-10-20 production keyword revision; older tables live in git history).
_TABLE_VERSION = 2

# ── 裁决序内联正则(逐字移植自生产 wf_crawl.py,裁决序属代码不属数据)──
#: 2026-10-20 公益豁免:公益站/倍率0 标题免付费信号直归羊毛(wf_crawl.py cat_of)。
_CHARITY_EXEMPT_RE = re.compile(r"公益|倍率\s?0|0\s?倍率", re.UNICODE)
#: 2026-10-17 云服务器优先:免费+云服务器族且非付费 → 羊毛(先于 token 判定)。
_CLOUD_SERVER_RE = re.compile(r"云服务器|云虚拟机|云主机|ECS|轻量服务器|VPS", re.UNICODE | re.I)
#: 2026-10-03 五刀+2026-10-24 Q1:付费/拉客帖整体砍,渠道不再作归宿。
_PAID_LURE_RE = re.compile(r"中转|relay|逆向|号池|接入了|api站|聚合|车队|纳新|低价|优惠", re.UNICODE | re.I)

#: Evidence table names for the inline adjudication regexes (hit trace).
_CHARITY_TABLE = "adjudication.charity_exempt"
_CLOUD_TABLE = "adjudication.cloud_server_first"
_LURE_TABLE = "adjudication.paid_lure"


class ClassifyDataError(ValueError):
    """Raised when the keyword table is missing, malformed or invalid.

    The message is structured: ``字段路径: 原因`` so AI/user edits can be
    fixed without reading the loader.
    """


@dataclass(frozen=True)
class MatchEvidence:
    """One keyword/pattern hit, kept for traceability and rule tuning."""

    table: str  # dotted data-file section, e.g. "category:token" / "signals.paid"
    kind: str  # "keyword" | "pattern"
    value: str  # the keyword or pattern exactly as written in the data file
    start: int  # match span within the normalized title
    end: int

    def describe(self) -> str:
        return f"{self.table}:{self.kind}={self.value}"


@dataclass(frozen=True)
class _Entry:
    """A compiled matcher plus its raw source for evidence output."""

    kind: str  # "keyword" | "pattern"
    value: str
    regex: re.Pattern[str]


@dataclass(frozen=True)
class Section:
    """One named table section: compiled keywords/patterns (+ optional target)."""

    name: str  # dotted path in the data file, e.g. "signals.paid"
    entries: tuple[_Entry, ...] = ()
    target_category: str | None = None


@dataclass(frozen=True)
class Category:
    """One category with its keyword section and adjudication stage."""

    id: str
    label: str
    stage: str
    priority: int
    section: Section


@dataclass(frozen=True)
class BuiltinResult:
    """Classification outcome for one title, with hit trace."""

    category: str | None
    matched: tuple[MatchEvidence, ...]
    normalized_title: str


@dataclass(frozen=True)
class ClassifyTable:
    """Compiled keyword table; build via :func:`load_table`."""

    version: int
    source: str
    categories: tuple[Category, ...]  # sorted by (priority, file order)
    free_target: Category
    paid_target: Category
    primary_categories: tuple[Category, ...]
    fallback_categories: tuple[Category, ...]
    direct_give: Section
    paid_signal: Section
    token_context: Section
    dead_filter: Section
    noise_filter: Section
    fake_filter: Section
    registration_lure: Section
    fallback_target: str

    def label_of(self, category_id: str) -> str | None:
        """Return the human label (e.g. "🎁羊毛") for a category id."""
        for category in self.categories:
            if category.id == category_id:
                return category.label
        return None


def _compile_entry(kind: str, value: str, flags: int, path: str) -> _Entry:
    source = re.escape(value) if kind == "keyword" else value
    try:
        return _Entry(kind=kind, value=value, regex=re.compile(source, flags))
    except re.error as exc:
        raise ClassifyDataError(f"分类关键词表字段错误: {path}: 正则编译失败: {exc}") from exc


def _build_section(name: str, raw: Any, base_path: str) -> Section:
    if not isinstance(raw, Mapping):
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}: 必须是对象, got {type(raw).__name__}")
    unknown = set(raw) - _SECTION_KEYS
    if unknown:
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}: 未知字段 {sorted(unknown)}")
    case_insensitive = raw.get("case_insensitive", False)
    if not isinstance(case_insensitive, bool):
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.case_insensitive: 必须是布尔值")
    flags = re.UNICODE | (re.IGNORECASE if case_insensitive else 0)
    entries: list[_Entry] = []
    for kind, key in (("keyword", "keywords"), ("pattern", "patterns")):
        raw_items = raw.get(key, [])
        if not isinstance(raw_items, list) or not all(isinstance(item, str) for item in raw_items):
            raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.{key}: 必须是字符串列表")
        for index, item in enumerate(raw_items):
            if not item:
                raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.{key}[{index}]: 不能为空字符串")
            entries.append(_compile_entry(kind, item, flags, f"{base_path}.{key}[{index}]"))
    target = raw.get("target_category")
    if target is not None and not isinstance(target, str):
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.target_category: 必须是字符串")
    return Section(name=name, entries=tuple(entries), target_category=target)


def _build_category(raw: Any, index: int) -> Category:
    base_path = f"categories[{index}]"
    if not isinstance(raw, Mapping):
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}: 必须是对象")
    unknown = set(raw) - (_SECTION_KEYS | {"id", "label", "stage", "priority"})
    if unknown:
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}: 未知字段 {sorted(unknown)}")
    category_id = raw.get("id")
    if not isinstance(category_id, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", category_id):
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.id: 必须是 snake_case 字符串, got {category_id!r}")
    label = raw.get("label")
    if not isinstance(label, str) or not label:
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.label: 必须是非空字符串")
    stage = raw.get("stage")
    if stage not in _KNOWN_STAGES:
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.stage: 必须是 {_KNOWN_STAGES} 之一, got {stage!r}")
    priority = raw.get("priority")
    if isinstance(priority, bool) or not isinstance(priority, int):
        raise ClassifyDataError(f"分类关键词表字段错误: {base_path}.priority: 必须是整数, got {priority!r}")
    # categories carry both adjudication metadata and a keyword section;
    # the section builder must only see the section keys
    section_raw = {key: raw[key] for key in _SECTION_KEYS if key in raw}
    section = _build_section(f"category:{category_id}", section_raw, base_path)
    return Category(id=category_id, label=label, stage=stage, priority=priority, section=section)


def _validate_references(categories: tuple[Category, ...], token_context: Section, fallback_target: Any) -> None:
    ids = [category.id for category in categories]
    duplicated = {category_id for category_id in ids if ids.count(category_id) > 1}
    if duplicated:
        raise ClassifyDataError(f"分类关键词表字段错误: categories: 类目 id 重复: {sorted(duplicated)}")
    free_targets = [category for category in categories if category.stage == _STAGE_FREE_TARGET]
    if len(free_targets) != 1:
        raise ClassifyDataError(
            f"分类关键词表字段错误: categories: 必须有且只有一个 stage=free_target 类目, 当前 {len(free_targets)} 个"
        )
    paid_targets = [category for category in categories if category.stage == _STAGE_PAID_TARGET]
    if len(paid_targets) != 1:
        raise ClassifyDataError(
            f"分类关键词表字段错误: categories: 必须有且只有一个 stage=paid_target 类目, 当前 {len(paid_targets)} 个"
        )
    if token_context.target_category is None or token_context.target_category not in ids:
        raise ClassifyDataError(
            f"分类关键词表字段错误: signals.token_context.target_category: "
            f"必须指向存在的类目 id, got {token_context.target_category!r}"
        )
    if not isinstance(fallback_target, str) or fallback_target not in ids:
        raise ClassifyDataError(
            f"分类关键词表字段错误: adjudication.fallback_target: 必须指向存在的类目 id, got {fallback_target!r}"
        )


def load_table(path: str | Path = DEFAULT_TABLE_PATH) -> ClassifyTable:
    """Load and validate a keyword table JSON file.

    Raises:
        ClassifyDataError: file missing, JSON invalid, unknown fields or
            broken references -- fail fast with 字段路径 + 原因.
    """
    table_path = Path(path)
    if not table_path.is_file():
        raise ClassifyDataError(f"分类关键词表加载失败: 文件不存在: {table_path}")
    try:
        data = json.loads(table_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise ClassifyDataError(f"分类关键词表加载失败: {table_path}: JSON 解析错误: {exc}") from exc
    if not isinstance(data, Mapping):
        raise ClassifyDataError(f"分类关键词表加载失败: {table_path}: 顶层必须是对象")
    unknown = set(data) - _TABLE_TOP_KEYS
    if unknown:
        raise ClassifyDataError(f"分类关键词表字段错误: 顶层未知字段 {sorted(unknown)}")
    version = data.get("version")
    if version != _TABLE_VERSION or isinstance(version, bool):
        raise ClassifyDataError(f"分类关键词表字段错误: version: 仅支持 {_TABLE_VERSION}, got {version!r}")

    raw_categories = data.get("categories")
    if not isinstance(raw_categories, list) or not raw_categories:
        raise ClassifyDataError("分类关键词表字段错误: categories: 必须是非空列表")
    categories = tuple(_build_category(raw, index) for index, raw in enumerate(raw_categories))

    raw_signals = data.get("signals")
    if not isinstance(raw_signals, Mapping) or set(raw_signals) != {"direct_give", "paid", "token_context"}:
        raise ClassifyDataError(
            "分类关键词表字段错误: signals: 必须包含且仅包含 direct_give/paid/token_context"
        )
    direct_give = _build_section("signals.direct_give", raw_signals["direct_give"], "signals.direct_give")
    paid_signal = _build_section("signals.paid", raw_signals["paid"], "signals.paid")
    token_context = _build_section("signals.token_context", raw_signals["token_context"], "signals.token_context")

    raw_filters = data.get("filters")
    if not isinstance(raw_filters, Mapping) or set(raw_filters) != {"dead", "noise", "fake", "registration_lure"}:
        raise ClassifyDataError("分类关键词表字段错误: filters: 必须包含且仅包含 dead/noise/fake/registration_lure")
    dead_filter = _build_section("filters.dead", raw_filters["dead"], "filters.dead")
    noise_filter = _build_section("filters.noise", raw_filters["noise"], "filters.noise")
    fake_filter = _build_section("filters.fake", raw_filters["fake"], "filters.fake")
    registration_lure = _build_section(
        "filters.registration_lure", raw_filters["registration_lure"], "filters.registration_lure"
    )

    raw_adjudication = data.get("adjudication", {})
    if not isinstance(raw_adjudication, Mapping):
        raise ClassifyDataError("分类关键词表字段错误: adjudication: 必须是对象")
    unknown_adjudication = set(raw_adjudication) - {"fallback_target", "description"}
    if unknown_adjudication:
        raise ClassifyDataError(f"分类关键词表字段错误: adjudication: 未知字段 {sorted(unknown_adjudication)}")
    fallback_target = raw_adjudication.get("fallback_target")

    _validate_references(categories, token_context, fallback_target)

    ordered = tuple(sorted(categories, key=lambda category: category.priority))
    return ClassifyTable(
        version=_TABLE_VERSION,
        source=str(table_path),
        categories=ordered,
        free_target=next(c for c in ordered if c.stage == _STAGE_FREE_TARGET),
        paid_target=next(c for c in ordered if c.stage == _STAGE_PAID_TARGET),
        primary_categories=tuple(c for c in ordered if c.stage == _STAGE_PRIMARY),
        fallback_categories=tuple(c for c in ordered if c.stage == _STAGE_FALLBACK),
        direct_give=direct_give,
        paid_signal=paid_signal,
        token_context=token_context,
        dead_filter=dead_filter,
        noise_filter=noise_filter,
        fake_filter=fake_filter,
        registration_lure=registration_lure,
        fallback_target=fallback_target,
    )


@lru_cache(maxsize=1)
def _default_table() -> ClassifyTable:
    return load_table()


def _scan(section: Section, title: str, evidence: list[MatchEvidence]) -> bool:
    """Record every keyword/pattern hit of ``section``; return True on any hit."""
    hit = False
    for entry in section.entries:
        match = entry.regex.search(title)
        if match is not None:
            hit = True
            evidence.append(
                MatchEvidence(
                    table=section.name,
                    kind=entry.kind,
                    value=entry.value,
                    start=match.start(),
                    end=match.end(),
                )
            )
    return hit


def _scan_inline(
    table: str, regex: re.Pattern[str], title: str, evidence: list[MatchEvidence]
) -> bool:
    """Record a hit of one adjudication-order inline regex (production port).

    The charity/cloud/lure regexes live in code (production ``cat_of``
    semantics), not in the data table; hits still land in the evidence trace
    so rule tuning stays observable.
    """
    match = regex.search(title)
    if match is None:
        return False
    evidence.append(
        MatchEvidence(
            table=table,
            kind="pattern",
            value=regex.pattern,
            start=match.start(),
            end=match.end(),
        )
    )
    return True


def classify_title(title: str, table: ClassifyTable | None = None) -> BuiltinResult:
    """Classify one title with the dual-signal adjudication.

    Args:
        title: raw title; whitespace is normalized exactly like production
            (``re.sub(r"\\s+", " ", ...).strip()``) before matching.
        table: preloaded table; defaults to the packaged ``data/keywords.json``.

    Returns:
        BuiltinResult with ``category`` (id or ``None`` for discarded titles)
        and the hit trace (which table/keyword/pattern matched where).

    Raises:
        TypeError: ``title`` is not a string.
        ClassifyDataError: the default table is malformed (propagated from
            first use; use :func:`load_table` to fail fast at startup).
    """
    if table is None:
        table = _default_table()
    if not isinstance(title, str):
        raise TypeError(f"分类标题必须是字符串, got {type(title).__name__}")
    normalized = re.sub(r"\s+", " ", title).strip()

    evidence: list[MatchEvidence] = []
    if _scan(table.dead_filter, normalized, evidence):
        logger.debug("分类丢弃: reason=dead title=%r evidence=%s", normalized, [e.describe() for e in evidence])
        return BuiltinResult(category=None, matched=tuple(evidence), normalized_title=normalized)
    if _scan(table.noise_filter, normalized, evidence):
        logger.debug("分类丢弃: reason=noise title=%r evidence=%s", normalized, [e.describe() for e in evidence])
        return BuiltinResult(category=None, matched=tuple(evidence), normalized_title=normalized)
    if _scan(table.fake_filter, normalized, evidence):
        logger.debug("分类丢弃: reason=fake title=%r evidence=%s", normalized, [e.describe() for e in evidence])
        return BuiltinResult(category=None, matched=tuple(evidence), normalized_title=normalized)

    reg_hit = _scan(table.registration_lure, normalized, evidence)
    give_hit = _scan(table.direct_give, normalized, evidence)
    if reg_hit and not give_hit:
        logger.debug("分类丢弃: reason=registration_lure title=%r evidence=%s", normalized, [e.describe() for e in evidence])
        return BuiltinResult(category=None, matched=tuple(evidence), normalized_title=normalized)

    # 两个信号表都全量扫描: 命中明细要完整(主人调规则要看所有命中的关键词)
    free_hit = _scan(table.free_target.section, normalized, evidence) or give_hit
    paid_hit = _scan(table.paid_signal, normalized, evidence)

    category: str | None = None
    if free_hit:
        # 免费分支(生产 v3.1 cat_of 裁决序,正则逐字移植):
        if _scan_inline(_CHARITY_TABLE, _CHARITY_EXEMPT_RE, normalized, evidence):
            # 2026-10-20 公益豁免: 公益站/倍率0 免付费直归羊毛
            category = table.free_target.id
        elif _scan_inline(_CLOUD_TABLE, _CLOUD_SERVER_RE, normalized, evidence) and not paid_hit:
            # 2026-10-17 云服务器优先: 云服务器族且非付费 → 羊毛(先于 token 判定)
            category = table.free_target.id
        elif _scan(table.token_context, normalized, evidence):
            category = table.token_context.target_category
        elif not paid_hit:
            category = table.free_target.id
        # 四级全落空(免费+付费且无豁免) → 落入下方主循环(生产同构)

    if category is None:
        # 无免费信号(或免费分支落空): 主循环 v2 起含 token(免免费可达,生产 v3.1 同款)
        for candidate in table.primary_categories:
            if _scan(candidate.section, normalized, evidence):
                category = candidate.id
                break

    if category is None:
        if paid_hit or _scan_inline(_LURE_TABLE, _PAID_LURE_RE, normalized, evidence):
            # 2026-10-03 五刀 + 2026-10-24 主人 Q1: 付费/拉客帖整体砍,
            # 渠道(paid_target)不再作归宿 —— 直接丢弃,不进兜底扫描。
            logger.debug(
                "分类丢弃: reason=paid_lure title=%r evidence=%s",
                normalized, [e.describe() for e in evidence],
            )
        else:
            for candidate in table.fallback_categories:
                if _scan(candidate.section, normalized, evidence):
                    category = table.fallback_target
                    break

    logger.debug(
        "分类完成: category=%s title=%r evidence=%s",
        category,
        normalized,
        [e.describe() for e in evidence],
    )
    return BuiltinResult(category=category, matched=tuple(evidence), normalized_title=normalized)


def category_label(category_id: str, table: ClassifyTable | None = None) -> str | None:
    """Return the human-readable label (e.g. "🎁羊毛") for a category id."""
    if table is None:
        table = _default_table()
    return table.label_of(category_id)
