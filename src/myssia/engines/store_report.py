"""store 报表引擎 —— 跨品类合并日报(Hermes 版式),链外.

``engine: store_report`` 显式选择才生效(链外注册,prompt/urlwatch 先例):
``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式选择 =
单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

语义(10-06-hermes-align 批次4,主人截图 OCR 版式):一个源 = 一份跨品类
合并日报——从 store 查**本槽位窗**内各品类新条目(AM = 本地 00:00 起、
PM = 本地 12:00 起,``SLOT_BOUNDARY_HOUR`` 同一边界),按 ``sections``
配置分区渲染 Hermes 布局的 markdown:

::

    <总标题> · <日期> · <AM|PM>
    <分区一标题>
    1. <一句话条目>(可带来源前缀,链接附句尾)
    2. …
    --
    <分区二标题>
    1. <子标题>
       <缩进明细行们>
    2. …
    <HH:MM> 实时爬取生成 · 全条目指纹去重 · 无新内容自动静默

要点(与既有 digest 路由的分工):本引擎是「日报层」——既用品类的
``digest`` 路由已降噪为 ``archive``(仅入库),immediate(score≥9/喜加一)
保留即时推送;本报表把窗口内全部新条目(含 immediate 已推的)合并成
**一条**飞书 markdown 文本消息发送,成为唯一日报出口。

布局纪律(主人令,照抄 Hermes 产线原文):

- **条目 = 编号 + 一句话**,不是链接列表——链接以 ``[原文](url)`` 附在
  句尾;``labels`` 可给条目带来源前缀(如 ``[OpenAI]``);
- **detail 分区** = 编号子标题 + 缩进明细行(``style: detail``;LLM 摘要
  条目的 content 逐行归一后缩进,markdown 结构符 ``#``/``-``/``**`` 剥除,
  防飞书 md 把缩进行渲染成标题/列表破坏版式);
- **空分区整段跳过**(分隔线 ``--`` 只落在已渲染分区之间);**全部分区
  无新条目 = 零条目 = 整条静默不发**(urlwatch「合法空态」判例 +
  ``last_skip_reason`` 留痕);
- 长度护栏交给通道层:feishu ``msg_form: text`` 的 post md rows 按
  :data:`~myssia.push.feishu_card.POST_SPLIT_THRESHOLD`(4000)行边界拆段,
  多段头尾 ``(i/N)``(组合铁律在案,不在本层重做)。

去重键适配(urlwatch ``#watch-`` / prompt ``#prompt-`` 判例):品类级
``dedup.key: {url}`` 会把「明天的日报」全期吞掉,引擎给条目 URL 铸
**日期+槽位锚点** ``<源url>#report-<YYYYMMDD>-<am|pm>``——每槽一个新
URL = 新去重键,同槽重跑幂等,跨槽必新。

配置形状(``engine_options.store_report``):

- ``sections``(必填):分区清单,每项 ``{title, sources, labels?, style?,
  suffix_fields?, max_entries?, max_lines?}``;
  - ``title``(必填):分区标题;
  - ``sources``(必填):纳入该分区的**源名**清单(store items.source 的
    匹配键——分类器 category 对 builtin 关闭的品类恒 None,games/
    ai-vendor-watch 无从按 category 查,源名是稳定锚);
  - ``labels``(可选):源名 → 条目前缀映射(如 ``openai-news: OpenAI``);
  - ``style``(可选,缺省 ``list``):``list`` = 编号一句话;``detail`` =
    编号子标题 + 缩进明细行;
  - ``suffix_fields``(可选):raw metadata 键清单,第一个非空值作句尾
  附注(如游戏的 ``price_text``/``sale_price``);
  - ``max_entries``(可选,缺省 :data:`DEFAULT_MAX_ENTRIES`):分区条目
  帽,超出以「另有 N 条省略」行留痕;
  - ``max_lines``(可选,缺省 :data:`DEFAULT_MAX_DETAIL_LINES`):detail
  分区每条目的明细行帽;
- ``title``(可选):总标题(缺省 = 源名);
- ``timezone``(可选):槽位边界时区(IANA;缺省本地)——品类 YAML 的
  ``timezone`` 键引擎读不到(FetchContext 不带品类配置),报表窗口语义
  需要时区就得在这里显式声明;
- ``max_chars_per_title``(可选,缺省 :data:`DEFAULT_TITLE_CHARS`):
  一句话条目的标题截断。

零 HTTP、零凭据(读的是本 run 注入的 store);``context.store`` 缺席 =
结构化 ``store_not_available``(引擎无降级面,如实说破)。

Raises:
    FetchError: 见各校验;``pagination``/``extract`` 配置结构化拒
        (单报表语义,urlwatch 同款)。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Mapping
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from myssia.dedup import SLOT_BOUNDARY_HOUR
from myssia.engines.fetch_base import BaseEngine, FetchContext, FetchError
from myssia.schema import SourceConfig
from myssia.store import SLOT_AM, SLOT_PM

logger = logging.getLogger(__name__)

#: 引擎层标签(schema 引擎词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "STORE_REPORT"

#: 分区词表:``list`` = 编号一句话;``detail`` = 编号子标题 + 缩进明细行。
SECTION_STYLES = ("list", "detail")

#: 分区条目帽缺省(超长日报截断护栏;超出以「另有 N 条省略」留痕)。
DEFAULT_MAX_ENTRIES = 12

#: detail 分区每条目明细行帽缺省。
DEFAULT_MAX_DETAIL_LINES = 10

#: 一句话条目标题截断(字符;标题精炼是版式纪律,超长条目截断保可读)。
DEFAULT_TITLE_CHARS = 80

#: 明细单行截断(字符;LLM 摘要行可长,缩进行超长会撑破版式)。
DEFAULT_DETAIL_LINE_CHARS = 120

#: 条目句尾附注(链接)的展示文案——「不是链接列表」纪律:链接是附注,
#: 不是条目本体。
LINK_LABEL = "原文"

#: 尾戳声明行(主人截图产线原文;时间占位在渲染时填)。
FOOTER_TEMPLATE = "{time} 实时爬取生成 · 全条目指纹去重 · 无新内容自动静默"

#: 空窗静默的 skip 哨兵(urlwatch ``watch_unchanged`` 判例:doctor 把
#: 「零条目但指纹未跳过」判 degraded,零产出是合法语义就得留痕)。
SKIP_WINDOW_EMPTY = "store_report_window_empty"

__all__ = [
    "DEFAULT_MAX_DETAIL_LINES",
    "DEFAULT_MAX_ENTRIES",
    "DEFAULT_TITLE_CHARS",
    "DEFAULT_DETAIL_LINE_CHARS",
    "FOOTER_TEMPLATE",
    "LAYER",
    "LINK_LABEL",
    "SECTION_STYLES",
    "SKIP_WINDOW_EMPTY",
    "DigestEntry",
    "DigestSection",
    "ReportSpec",
    "StoreReportEngine",
    "clip_title",
    "normalize_detail_line",
    "render_report",
    "slot_window",
]


def clip_title(text: str, limit: int) -> str:
    """标题截断为单行一句话(压空白;超长截断加省略号,不截断链接)。"""
    line = " ".join(str(text or "").split())
    if len(line) <= limit:
        return line
    return line[: max(limit - 1, 1)] + "…"


def normalize_detail_line(line: str, limit: int = DEFAULT_DETAIL_LINE_CHARS) -> str | None:
    """明细行归一:剥 markdown 结构符,空白行/纯符号行返回 None.

    版式纪律:缩进明细行不能带 ``#``/列表符/加粗——飞书 md 会把 ``#`` 行
    渲染成标题、``- `` 行渲染成列表,破坏「缩进明细」的视觉;归一成纯
    文本行(``· `` 前缀由渲染层加)。
    """
    text = line.strip()
    if not text:
        return None
    while text.startswith("#"):
        text = text.lstrip("#").strip()
    if text.startswith(("- ", "* ", "+ ")):
        text = text[2:].strip()
    text = text.replace("**", "").replace("__", "")
    text = clip_title(text, limit)
    return text or None


def slot_window(
    now: datetime, tz: ZoneInfo | None = None
) -> tuple[str, datetime, str]:
    """本地槽位窗口:``(slot, window_start, date_str)``.

    AM = 本地 ``00:00`` 起,PM = 本地 ``12:00`` 起(:data:`SLOT_BOUNDARY_HOUR`
    与 dedup/digest 同一边界);``date_str`` = 窗口日的 ``YYYY-MM-DD``
    (本地)。返回的 ``window_start`` 是 aware 本地时刻(调用方自行转
    store 的 UTC ISO 口径)。
    """
    local = now.astimezone(tz) if tz is not None else now.astimezone()
    day_start = local.replace(hour=0, minute=0, second=0, microsecond=0)
    window_start = day_start if local.hour < SLOT_BOUNDARY_HOUR else day_start.replace(
        hour=SLOT_BOUNDARY_HOUR
    )
    slot = SLOT_AM if local.hour < SLOT_BOUNDARY_HOUR else SLOT_PM
    return slot, window_start, window_start.strftime("%Y-%m-%d")


@dataclass
class DigestEntry:
    """分区内的一个条目(渲染输入的一手形状)."""

    head: str
    url: str | None = None
    label: str | None = None
    suffix: str | None = None
    details: list[str] = field(default_factory=list)


@dataclass
class DigestSection:
    """一个分区(条目已按展示序排定)."""

    title: str
    style: str = "list"
    entries: list[DigestEntry] = field(default_factory=list)
    omitted: int = 0  # 超过 max_entries 被省略的条数(渲染层留痕)


def render_report(
    sections: list[DigestSection],
    *,
    title: str,
    date: str,
    slot: str,
    generated_at: datetime,
) -> str:
    """Hermes 版式渲染(纯函数,快照测试锚).

    布局契约(主人截图 OCR):首行 = ``总标题 · 日期 · AM|PM``;分区标题行
    + 编号条目;分区之间 ``--`` 分隔线(只落在**已渲染**分区之间,空分区
    整段跳过);末行尾戳 = ``HH:MM 实时爬取生成 · 全条目指纹去重 ·
    无新内容自动静默``。全部分区空 → 空串(调用方静默不发)。
    """
    lines: list[str] = [f"{title} · {date} · {slot.upper()}"]
    rendered_any = False
    for section in sections:
        if not section.entries:
            continue
        if rendered_any:
            lines.append("--")
        lines.append(section.title)
        for index, entry in enumerate(section.entries, start=1):
            head = entry.head
            if entry.label:
                head = f"[{entry.label}] {head}"
            if entry.suffix:
                head = f"{head} · {entry.suffix}"
            if entry.details:
                lines.append(f"{index}. {head}")
                lines.extend(f"   · {detail}" for detail in entry.details)
            else:
                if entry.url:
                    head = f"{head} [{LINK_LABEL}]({entry.url})"
                lines.append(f"{index}. {head}")
        if section.omitted:
            lines.append(f"   ……(另有 {section.omitted} 条省略)")
        rendered_any = True
    if not rendered_any:
        return ""
    lines.append(FOOTER_TEMPLATE.format(time=generated_at.strftime("%H:%M")))
    return "\n".join(lines)


@dataclass
class ReportSpec:
    """一份报表的配置侧形状(``_options`` 校验产物)."""

    title: str
    sections: list[dict[str, Any]]
    tz: ZoneInfo | None
    max_chars_per_title: int


class StoreReportEngine(BaseEngine):
    """跨品类合并日报源(显式 ``engine: store_report``;store 查询 → 版式渲染).

    items 出口对齐 ``Item.from_extracted`` 契约:整份报表 = **一条**条目
    (url = 日期+槽位锚点,title = 总标题,content = 版式 markdown 入 items
    表档案),``report_markdown``(同一 markdown)与其余观测键进 metadata
    ——push 模板经 item_view 的 metadata 合并直接可渲染
    (``{{ item.report_markdown }}``),零 push 层改动(prompt 引擎同款)。
    """

    LAYER = "STORE_REPORT"
    ENGINE_NAME = "store_report"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    def __init__(
        self,
        source: SourceConfig,
        context: FetchContext,
        *,
        now_fn: Any | None = None,
    ) -> None:
        super().__init__(source, context)
        #: 墙钟注入口(测试控时;缺省本地真实时钟)。FetchContext.clock 是
        #: monotonic(测速用),报表的日期/槽位语义需要墙钟。
        self._now_fn = now_fn or (lambda: datetime.now().astimezone())

    # -------------------------------------------------------------- options

    def _options(self) -> ReportSpec:
        """engine_options.store_report 校验与缺省化(错型即结构化拒)."""
        options = self.engine_options()
        raw_sections = options.get("sections")
        if not isinstance(raw_sections, list) or not raw_sections:
            raise FetchError(
                "engine_options.store_report.sections 应为非空分区清单"
                "(每项 {title, sources, …}),当前为 "
                f"{raw_sections!r}",
                error_type="invalid_engine_options",
            )
        sections: list[dict[str, Any]] = []
        for index, raw in enumerate(raw_sections):
            path = f"sections[{index}]"
            if not isinstance(raw, dict):
                raise FetchError(
                    f"engine_options.store_report.{path} 应为键值映射,当前为 {raw!r}",
                    error_type="invalid_engine_options",
                )
            unknown = set(raw) - {
                "title", "sources", "labels", "style", "suffix_fields",
                "max_entries", "max_lines",
            }
            if unknown:
                raise FetchError(
                    f"engine_options.store_report.{path} 未知字段 {sorted(unknown)}",
                    error_type="invalid_engine_options",
                )
            title = raw.get("title")
            if not isinstance(title, str) or not title.strip():
                raise FetchError(
                    f"engine_options.store_report.{path}.title 应为非空字符串(分区标题)",
                    error_type="invalid_engine_options",
                )
            sources = raw.get("sources")
            if not isinstance(sources, list) or not sources or not all(
                isinstance(item, str) and item.strip() for item in sources
            ):
                raise FetchError(
                    f"engine_options.store_report.{path}.sources 应为非空源名清单"
                    "(store items.source 的匹配键)",
                    error_type="invalid_engine_options",
                )
            labels = raw.get("labels", {})
            if not isinstance(labels, dict) or not all(
                isinstance(key, str) and isinstance(value, str) for key, value in labels.items()
            ):
                raise FetchError(
                    f"engine_options.store_report.{path}.labels 应为 源名→前缀 字符串映射",
                    error_type="invalid_engine_options",
                )
            style = raw.get("style", "list")
            if style not in SECTION_STYLES:
                raise FetchError(
                    f"engine_options.store_report.{path}.style 必须是 "
                    f"{list(SECTION_STYLES)} 之一,当前为 {style!r}",
                    error_type="invalid_engine_options",
                )
            suffix_fields = raw.get("suffix_fields", [])
            if not isinstance(suffix_fields, list) or not all(
                isinstance(item, str) and item.strip() for item in suffix_fields
            ):
                raise FetchError(
                    f"engine_options.store_report.{path}.suffix_fields 应为"
                    " metadata 键字符串清单",
                    error_type="invalid_engine_options",
                )
            max_entries = raw.get("max_entries", DEFAULT_MAX_ENTRIES)
            if (
                isinstance(max_entries, bool)
                or not isinstance(max_entries, int)
                or not 1 <= max_entries <= 100
            ):
                raise FetchError(
                    f"engine_options.store_report.{path}.max_entries 应为 1-100 整数,"
                    f"当前为 {max_entries!r}",
                    error_type="invalid_engine_options",
                )
            max_lines = raw.get("max_lines", DEFAULT_MAX_DETAIL_LINES)
            if (
                isinstance(max_lines, bool)
                or not isinstance(max_lines, int)
                or not 1 <= max_lines <= 200
            ):
                raise FetchError(
                    f"engine_options.store_report.{path}.max_lines 应为 1-200 整数,"
                    f"当前为 {max_lines!r}",
                    error_type="invalid_engine_options",
                )
            sections.append(
                {
                    "title": title.strip(),
                    "sources": [item.strip() for item in sources],
                    "labels": labels,
                    "style": style,
                    "suffix_fields": suffix_fields,
                    "max_entries": max_entries,
                    "max_lines": max_lines,
                }
            )
        title = options.get("title", self.source.name)
        if not isinstance(title, str) or not title.strip():
            raise FetchError(
                f"engine_options.store_report.title 应为非空字符串,当前为 {title!r}",
                error_type="invalid_engine_options",
            )
        tz_name = options.get("timezone")
        tz: ZoneInfo | None = None
        if tz_name is not None:
            if not isinstance(tz_name, str) or not tz_name.strip():
                raise FetchError(
                    f"engine_options.store_report.timezone 应为 IANA 时区名,"
                    f"当前为 {tz_name!r}",
                    error_type="invalid_engine_options",
                )
            try:
                tz = ZoneInfo(tz_name.strip())
            except (ZoneInfoNotFoundError, ValueError) as exc:
                raise FetchError(
                    f"engine_options.store_report.timezone 不是有效 IANA 时区名:"
                    f"{tz_name!r}",
                    error_type="invalid_engine_options",
                ) from exc
        max_chars = options.get("max_chars_per_title", DEFAULT_TITLE_CHARS)
        if (
            isinstance(max_chars, bool)
            or not isinstance(max_chars, int)
            or not 10 <= max_chars <= 400
        ):
            raise FetchError(
                "engine_options.store_report.max_chars_per_title 应为 10-400 整数,"
                f"当前为 {max_chars!r}",
                error_type="invalid_engine_options",
            )
        return ReportSpec(
            title=title.strip(), sections=sections, tz=tz, max_chars_per_title=max_chars
        )

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        spec = self._options()
        store = self.context.store
        if store is None:
            raise FetchError(
                "store_report 引擎需要 store 注入(FetchContext.store),当前运行"
                "上下文未携带——报表无数据面,无降级路径",
                error_type="store_not_available",
            )
        now: datetime = self._now_fn()
        slot, window_start, date_str = slot_window(now, spec.tz)
        # 窗口 = 单槽位(≤12h),量级小;但 items 表混着**不在任何分区**的源
        # (wool 等),newest-first 的单页 limit 会被无关新条目挤占——走
        # before/before_id 复合游标拉全窗口,页 500、保底帽 4000 条防病态膨胀。
        source_names = {name for section in spec.sections for name in section["sources"]}
        records = self._list_window(store, window_start)
        by_source: dict[str, list[Mapping[str, Any]]] = {}
        for record in records:
            raw_source = getattr(record, "source", None) or ""
            if raw_source in source_names:
                by_source.setdefault(raw_source, []).append(record)
        sections = [
            self._build_section(section, by_source, spec.max_chars_per_title)
            for section in spec.sections
        ]
        total = sum(len(section.entries) for section in sections)
        if total == 0:
            # 全分区无新内容 = 整条静默(urlwatch 合法空态判例):零条目 +
            # skip 哨兵留痕(doctor 不误诊 degraded),绝不发「无内容」占位。
            self.last_skip_reason = SKIP_WINDOW_EMPTY
            logger.info(
                "store 报表窗口内无新条目,静默: date=%s slot=%s sources=%s",
                date_str,
                slot,
                sorted(source_names),
            )
            return []
        generated_at = now.astimezone(spec.tz) if spec.tz is not None else now.astimezone()
        markdown = render_report(
            sections,
            title=spec.title,
            date=date_str,
            slot=slot,
            generated_at=generated_at,
        )
        stamp = window_start.strftime("%Y%m%d")
        item: dict[str, Any] = {
            "url": f"{self.source.url}#report-{stamp}-{slot}",
            "title": spec.title,
            "content": markdown,
            "report_markdown": markdown,
            "report_date": date_str,
            "report_slot": slot,
            "report_entries": total,
            "report_window_start": window_start.isoformat(),
            "report_sections": [
                {"title": section.title, "entries": len(section.entries)}
                for section in sections
                if section.entries
            ],
        }
        logger.info(
            "store 报表完成: date=%s slot=%s sections=%d entries=%d chars=%d",
            date_str,
            slot,
            len(sections),
            total,
            len(markdown),
        )
        return [item]

    #: 窗口拉取页大小与保底帽(复合游标逐页;帽 = 防病态膨胀的护栏)。
    WINDOW_PAGE_SIZE = 500
    WINDOW_MAX_RECORDS = 4000

    def _list_window(self, store: Any, window_start: datetime) -> list[Any]:
        """拉全窗口条目(newest-first 复合游标翻页,不足一页即止)."""
        records: list[Any] = list(
            store.list_items(since=window_start, limit=self.WINDOW_PAGE_SIZE)
        )
        while (
            len(records) < self.WINDOW_MAX_RECORDS
            and len(records) % self.WINDOW_PAGE_SIZE == 0
            and records
        ):
            last = records[-1]
            page = store.list_items(
                since=window_start,
                before=getattr(last, "first_seen", None),
                before_id=getattr(last, "id", None),
                limit=self.WINDOW_PAGE_SIZE,
            )
            if not page:
                break
            records.extend(page)
        return records

    def _build_section(
        self,
        section: Mapping[str, Any],
        by_source: Mapping[str, list[Mapping[str, Any]]],
        max_chars: int,
    ) -> DigestSection:
        """一个分区:按源声明序收条目(store 已 newest-first),编号帽截断."""
        entries: list[DigestEntry] = []
        for source_name in section["sources"]:
            labels = section["labels"]
            for record in by_source.get(source_name, ()):
                entries.append(
                    self._entry_from_record(record, source_name, labels, section, max_chars)
                )
        max_entries = section["max_entries"]
        omitted = max(len(entries) - max_entries, 0)
        return DigestSection(
            title=section["title"],
            style=section["style"],
            entries=entries[:max_entries],
            omitted=omitted,
        )

    def _entry_from_record(
        self,
        record: Mapping[str, Any],
        source_name: str,
        labels: Mapping[str, str],
        section: Mapping[str, Any],
        max_chars: int,
    ) -> DigestEntry:
        """store 条目 → 渲染条目(list 一句话 / detail 子标题+缩进明细)."""
        title = str(getattr(record, "title", None) or "(无标题)")
        url_value = getattr(record, "url", None)
        url = url_value if isinstance(url_value, str) and url_value.strip() else None
        entry = DigestEntry(
            head=clip_title(title, max_chars),
            url=url,
            label=labels.get(source_name),
        )
        raw = getattr(record, "raw", None)
        raw_map = raw if isinstance(raw, Mapping) else {}
        if section["style"] == "detail":
            content = str(getattr(record, "content", None) or "")
            details: list[str] = []
            for line in content.splitlines():
                if len(details) >= section["max_lines"]:
                    details.append("……(明细超长省略)")
                    break
                normalized = normalize_detail_line(line)
                if normalized is not None:
                    details.append(normalized)
            entry.details = details
        else:
            for key in section["suffix_fields"]:
                value = raw_map.get(key)
                if isinstance(value, (str, int, float)) and not isinstance(value, bool):
                    text = str(value).strip()
                    if text:
                        entry.suffix = text
                        break
        return entry

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单报表语义:任何 pagination 配置都结构化拒(urlwatch 判例).

        报表对象是「store 窗口查询」,翻页游走会让报表的对象漂移。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "store_report 引擎是单报表语义(sections 即报表对象,每槽一份),"
                "不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
