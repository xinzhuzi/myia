"""Tests for store-report ``first_run``(首跑条目折叠,10-18 批次).

首轮建档条目(新源第一次入库,``raw.fetch_change_reason == first_fetch``,
分类层 F5 写键)在日报层的处理:分区配 ``first_run: fold`` 时不占编号
席位、分区尾折叠一行人话留痕;缺省 ``show`` 照常编号(现状不变)。
折叠在场 = 窗口不空(``low_value`` 同判:折叠行是诚实信号,静默才是
说谎)。测试全 mock(内存 SQLiteStore 种子数据 + now_fn 控时),零真网。

用例面:

1. ``fold``:首跑条目折进折叠行、不占编号席位(正文编号只数非首跑)、
   文案逐字断言;折叠判在 ``min_score`` 之先(首跑条目无 enrich 分,
   价值门无分不拦、不误伤——首跑计数与低价值计数不混账);
2. ``show`` 缺省(分区不配键)与显式 ``show``:首跑条目照常编号进正文,
   零折叠行(现状不变);
3. 非法值拒载:非 ``fold``/``show`` 一律 ``invalid_engine_options``
   结构化拒(照 min_score/max_entries 同门);
4. 全分区仅剩首跑折叠条目时**不静默**:报表照发、skip 哨兵不落
   (折叠行即内容,静默才是说谎);
5. 渲染纯函数与判定谓词:DigestSection.first_run 折叠行/分区不算空/
   折叠行缀分区尾(省略、低价值之后);record_is_first_fetch 口径。
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

import httpx
import pytest

from conftest import make_client, make_context, make_source, run

from myssia.engines.fetch_base import FetchError
from myssia.engines.store_report import (
    FOOTER_TEMPLATE,
    FIRST_RUN_MODES,
    SKIP_WINDOW_EMPTY,
    DigestEntry,
    DigestSection,
    StoreReportEngine,
    record_is_first_fetch,
    render_report,
)
from myssia.store import SQLiteStore
from myssia.store.models import ItemRecord

TZ_SHANGHAI = ZoneInfo("Asia/Shanghai")
NOW_PM = datetime(2026, 10, 18, 20, 30, tzinfo=TZ_SHANGHAI)  # PM 槽,窗口起 12:00
IN_WINDOW_PM = datetime(2026, 10, 18, 6, 0, tzinfo=timezone.utc)  # 14:00 +08 = PM 窗内
EARLIER_PM = IN_WINDOW_PM - timedelta(minutes=10)  # 13:50 +08 = PM 窗内(次新)

#: 首跑折叠行的逐字文案(渲染层单源;N = 收进本分区的首跑子集计数)。
FOLD_LINE = "   ……(另有 {count} 条首轮建档条目(新源第一次入库,未打扰))"


def report_options(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "title": "情报日报",
        "timezone": "Asia/Shanghai",
        "sections": [{"title": "AI 资讯", "sources": ["aihot"]}],
    }
    base.update(overrides)
    return base


def make_engine(
    store: SQLiteStore | None,
    *,
    now: datetime = NOW_PM,
    options: dict[str, Any] | None = None,
) -> StoreReportEngine:
    """直构引擎(store 注入 + 墙钟钉死;零 HTTP——MockTransport 兜 robots 缺省)."""
    data: dict[str, Any] = {
        "name": "daily-digest",
        "engine": "store_report",
        "url": "https://myia.local/daily-digest",
    }
    if options is None:
        options = report_options()
    data["engine_options"] = {"store_report": options}
    source = make_source(**data)
    context, _clock = make_context(make_client(lambda request: httpx.Response(404)), store=store)
    return StoreReportEngine(source, context, now_fn=lambda: now)


def seed(
    store: SQLiteStore,
    *,
    source: str,
    title: str,
    url: str,
    first_seen: datetime,
    content: str | None = None,
    raw: dict[str, Any] | None = None,
    scores: dict[str, Any] | None = None,
) -> None:
    store.save_item(
        ItemRecord(
            url=url,
            dedup_key=f"{url}#k",
            title=title,
            source=source,
            content=content,
            raw=raw or {},
            scores=scores,
            first_seen=first_seen,
        )
    )


def seed_first_fetch(store: SQLiteStore, *, title: str, url: str) -> None:
    """种一条首轮建档条目(F5 写键口径:raw.fetch_change_reason=first_fetch)."""
    seed(
        store,
        source="aihot",
        title=title,
        url=url,
        first_seen=IN_WINDOW_PM,
        raw={"fetch_change_reason": "first_fetch"},
    )


def numbered(markdown: str) -> list[str]:
    return [
        line for line in markdown.splitlines() if line[:3] in {f"{i}. " for i in range(1, 10)}
    ]


@pytest.fixture()
def store(tmp_path):
    return SQLiteStore(tmp_path / "report.db")


# ------------------------------------------------------- ① fold:折叠与文案


def test_fetch_first_run_fold_folds_and_traces(store):
    """fold:首跑条目不占编号席位(正文编号只数非首跑),分区尾折叠一行
    人话留痕;报表条目数只数正文."""
    seed(
        store,
        source="aihot",
        title="存量要闻甲",
        url="https://aihot/keep/1",
        first_seen=IN_WINDOW_PM,  # 最新 → 编号 1
    )
    seed(
        store,
        source="aihot",
        title="存量要闻乙",
        url="https://aihot/keep/2",
        first_seen=EARLIER_PM,  # 次新 → 编号 2(时间戳错开钉顺序,store
        # newest-first + id DESC 同刻并列不赌)
    )
    seed_first_fetch(store, title="新源首跑甲", url="https://aihot/first/1")
    seed_first_fetch(store, title="新源首跑乙", url="https://aihot/first/2")
    engine = make_engine(
        store,
        options=report_options(
            sections=[{"title": "AI 资讯", "sources": ["aihot"], "first_run": "fold"}]
        ),
    )
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    markdown = item["report_markdown"]
    # 首跑条目不占编号席位:编号行只数两条存量要闻,编号 1、2 连续。
    heads = numbered(markdown)
    assert len(heads) == 2
    assert heads[0].startswith("1. 存量要闻甲")
    assert heads[1].startswith("2. 存量要闻乙")
    # 首跑标题不进正文,逐字折叠行留痕(N=2)。
    assert "新源首跑甲" not in markdown
    assert "新源首跑乙" not in markdown
    assert FOLD_LINE.format(count=2) in markdown
    assert item["report_entries"] == 2
    assert engine.last_skip_reason is None
    assert FOOTER_TEMPLATE.format(time="20:30") in markdown


def test_fetch_first_run_fold_before_min_score(store):
    """折叠判在 min_score 之先:首跑条目无 enrich 分,价值门无分不拦、
    不误伤——首跑计数与低价值计数不混账(各数各的)."""
    seed_first_fetch(store, title="新源首跑甲", url="https://aihot/first/1")
    seed(
        store,
        source="aihot",
        title="低分闲闻",
        url="https://aihot/lo",
        first_seen=IN_WINDOW_PM,
        scores={"value": 1},
    )
    seed(
        store,
        source="aihot",
        title="高分要闻",
        url="https://aihot/hi",
        first_seen=IN_WINDOW_PM,
        scores={"value": 8},
    )
    engine = make_engine(
        store,
        options=report_options(
            sections=[
                {
                    "title": "AI 资讯",
                    "sources": ["aihot"],
                    "min_score": 3,
                    "first_run": "fold",
                }
            ]
        ),
    )
    items = run(engine.fetch())
    markdown = items[0]["report_markdown"]
    assert len(numbered(markdown)) == 1  # 只有高分要闻占席位
    assert "高分要闻" in markdown
    # 首跑走折叠通道(1 条),低分走价值门通道(1 条):两行各在,不混账。
    assert FOLD_LINE.format(count=1) in markdown
    assert "   ……(另有 1 条低价值条目,价值分<3)" in markdown
    # 折叠行缀分区尾:低价值折叠行之后。
    assert markdown.index("低价值条目") < markdown.index("首轮建档条目")


# --------------------------------------------------- ② show 缺省:现状不变


@pytest.mark.parametrize("explicit", [None, "show"])
def test_fetch_first_run_show_default_keeps_current(store, explicit):
    """缺省(不配键)与显式 show 同貌:首跑条目照常编号进正文,零折叠行
    (现状不变——不配 first_run 的存量配置行为一分不动)."""
    seed_first_fetch(store, title="新源首跑甲", url="https://aihot/first/1")
    seed(
        store,
        source="aihot",
        title="存量要闻",
        url="https://aihot/keep/1",
        first_seen=EARLIER_PM,  # 次新 → 编号 2(时间戳错开钉顺序)
    )
    section: dict[str, Any] = {"title": "AI 资讯", "sources": ["aihot"]}
    if explicit is not None:
        section["first_run"] = explicit
    engine = make_engine(store, options=report_options(sections=[section]))
    items = run(engine.fetch())
    assert len(items) == 1
    markdown = items[0]["report_markdown"]
    heads = numbered(markdown)
    assert len(heads) == 2  # 首跑照常占编号席位(store newest-first 既有判例)
    assert heads[0].startswith("1. 新源首跑甲")  # 最新(IN_WINDOW_PM)→ 编号 1
    assert heads[1].startswith("2. 存量要闻")
    assert "首轮建档条目" not in markdown
    assert items[0]["report_entries"] == 2


# ------------------------------------------------- ③ 非法值:结构化拒载


@pytest.mark.parametrize(
    "bad",
    [
        "hide",
        "FOLD",  # 大小写敏感
        True,
        1,
        ["fold"],
    ],
)
def test_options_reject_invalid_first_run(store, bad):
    """first_run 仅接受 fold|show:非法值 invalid_engine_options 结构化拒
    (照 min_score/max_entries 同门;白名单放行 first_run 键本身)."""
    engine = make_engine(
        store,
        options=report_options(
            sections=[{"title": "AI 资讯", "sources": ["aihot"], "first_run": bad}]
        ),
    )
    with pytest.raises(FetchError, match="first_run") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert "fold" in str(excinfo.value)


def test_first_run_modes_vocab():
    """词表锚:fold|show 二值,fold 在册(show 缺省语义在 _options)."""
    assert FIRST_RUN_MODES == ("fold", "show")


# ------------------------- ④ 全分区仅剩首跑折叠条目:不静默、发折叠行


def test_fetch_first_run_only_not_silent(store):
    """全分区仅剩首跑折叠条目:报表照发、skip 哨兵不落——折叠行是诚实
    信号,静默才是说谎(low_value 同判)."""
    seed_first_fetch(store, title="新源首跑甲", url="https://aihot/first/1")
    seed_first_fetch(store, title="新源首跑乙", url="https://aihot/first/2")
    engine = make_engine(
        store,
        options=report_options(
            sections=[{"title": "AI 资讯", "sources": ["aihot"], "first_run": "fold"}]
        ),
    )
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    markdown = item["report_markdown"]
    assert engine.last_skip_reason is None  # 窗口不空:不落 SKIP_WINDOW_EMPTY
    assert numbered(markdown) == []
    assert "AI 资讯" in markdown  # 分区不算空:标题 + 折叠行即内容
    assert FOLD_LINE.format(count=2) in markdown
    assert item["report_entries"] == 0
    assert FOOTER_TEMPLATE.format(time="20:30") in markdown


def test_fetch_silent_only_when_truly_empty_with_first_run_fold(store):
    """对照面:窗口真空(零条目)照旧静默——first_run 只放行「首跑折叠
    在场」,不扩大不静默豁免."""
    engine = make_engine(
        store,
        options=report_options(
            sections=[{"title": "AI 资讯", "sources": ["aihot"], "first_run": "fold"}]
        ),
    )
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == SKIP_WINDOW_EMPTY


# --------------------------------------------- 渲染纯函数与判定谓词(先例)


def test_render_report_first_run_fold_line():
    """DigestSection.first_run:折叠行缀分区尾(省略、低价值之后);
    首跑-only 分区不算空(标题 + 折叠行照渲染),空分区照跳过."""
    sections = [
        DigestSection(
            title="AI 资讯",
            entries=[DigestEntry(head="要闻", url="https://x/1")],
            omitted=1,
            low_value=2,
            min_score=3,
            first_run=4,
        ),
        DigestSection(title="游戏", entries=[], first_run=5),
        DigestSection(title="空分区", entries=[]),
    ]
    rendered = render_report(
        sections, title="情报日报", date="2026-10-18", slot="pm", generated_at=NOW_PM
    )
    assert "1. 要闻" in rendered
    assert "   ……(另有 1 条省略)" in rendered
    assert "   ……(另有 2 条低价值条目,价值分<3)" in rendered
    assert FOLD_LINE.format(count=4) in rendered
    # 折叠行缀分区尾:省略 → 低价值 → 首跑。
    assert rendered.index("另有 1 条省略") < rendered.index("另有 2 条低价值条目")
    assert rendered.index("另有 2 条低价值条目") < rendered.index("首轮建档条目")
    # 首跑-only 分区:标题 + 折叠行照渲染;空分区照跳过。
    assert "游戏" in rendered
    assert FOLD_LINE.format(count=5) in rendered
    assert "空分区" not in rendered


def test_record_is_first_fetch_precedent():
    """判定口径:raw 缺席/非映射/值不符都算非首跑(照常编号,不误伤)."""

    def record(raw: Any) -> ItemRecord:
        return ItemRecord(url="u", dedup_key="k", title="t", raw=raw)

    assert record_is_first_fetch(record(None)) is False
    assert record_is_first_fetch(record({})) is False
    assert record_is_first_fetch(record({"fetch_change_reason": "hash_differ"})) is False
    assert record_is_first_fetch(record({"fetch_change_reason": "first_fetch"})) is True
