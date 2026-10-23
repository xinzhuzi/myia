"""Tests for the vendor-market engine(10-24-huawei-ai-news-absorb D4).

厂商行情速览(生产 ai_daily_report.py:30-109 的 MYIA 承载):三路抓取
(Yahoo/腾讯股价双源 + ZOL 经 firecrawl 云渲染 + B站合集 API)→ 确定性
计算 → 单条目出仓(#vendor-<日期> 锚)。测试全 mock(httpx.MockTransport
四端点路由 + FakeClock),零真网;firecrawl 端点走 env 注入
(MYIA_FIRECRAWL_URL,引擎 env 回退路径)。

用例面:

1. registry/链外语义与 schema 词表(vendor_market 在册、AUTO_CHAIN 不在、
   auto_degrade 单级链、EngineName 词表收词、SourceConfig 可显式选用);
2. options 校验:未知字段/词表外 provider/msrp 空表与非正数/凭据引用
   明文拒/数值越界;
3. 纯函数:normalize_zol_prices(变体拼写归一 + 首见即钉 + 三族外丢弃)、
   build_gpu_rows(便宜/贵/持平三分支 + 停产行 + 行帽)、
   format_stock_line(生产格式串逐字,含/无 数据时间);
4. 全活形态:三路全活 → 一条目,报告版式逐行断言(生产行文案)、
   metadata 观测键(vendor_report/vendor_stock/vendor_gpu/vendor_video_*/
   vendor_degraded 空清单)、Item.from_extracted 键落位;
5. 股价双源:Yahoo 死 → 腾讯 gbk 兜底(provider=tencent);双死 →
   「股价源暂不可用」降级行,整条照出;
6. ZOL 死:firecrawl 后端死 / 端点未配 → 「GPU 价格源暂不可用」降级行;
7. B站死:视频行缺位 + degraded 留痕;
8. msrp 未配 → GPU 比价区整段跳过(无行无降级);
9. 锚点幂等:#vendor-<YYYYMMDD> 纯日期函数,同日两跑同 URL;
10. pagination/extract 配置结构化拒(单报表语义);
11. 真实配置面:config/ai-vendor-daily.yaml 装载(engine/builtin/dedup/
    archive 路由/msrp 原表)、daily-digest.yaml「AI 厂商行情」分区
    (sources/style)与 4.4 改造同步。
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import pytest

from conftest import make_client, make_context, make_source, run

from myssia.engines.fetch_base import FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.engines.vendor_market import (
    GPU_DEGRADED_LINE,
    GPU_STOPPED_SUFFIX,
    STOCK_DEGRADED_LINE,
    VendorMarketEngine,
    build_gpu_rows,
    format_stock_line,
    normalize_zol_prices,
)
from myssia.pipeline import Item
from myssia.push.route import resolve_route, routes_from_config
from myssia.schema import ENGINES, load_category_file

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"

#: 生产 MSRP 原表(整数——行文案 $8,500 不带 .0)+ 一张三族外型号
#: (5080:ZOL 抽价归一丢弃 → 恒停产行)。
MSRP_TABLE: dict[str, int] = {
    "RTX PRO 6000": 8500,
    "RTX 5090": 1999,
    "RTX 4090": 1599,
    "RTX 5080": 999,
}

#: ZOL 云渲染页合成形状(正则命中最小形状;含 5080 诱饵条 —— 归一丢弃)。
ZOL_HTML = (
    '<ul id="J_PicMode">'
    '<li data-follow-id="1"><h3><a title="七彩虹 RTX PRO 6000 X 24G"'
    ' href="//detail.zol.com.cn/vga/a1.html">卡一</a></h3>'
    '<b class="price-type">62000</b></li>'
    '<li data-follow-id="2"><h3><a title="影驰 RTX 5090 魔刃 32G"'
    ' href="//detail.zol.com.cn/vga/a2.html">卡二</a></h3>'
    '<b class="price-type">16499</b></li>'
    '<li data-follow-id="3"><h3><a title="耕升 RTX 4090 追风 24G"'
    ' href="//detail.zol.com.cn/vga/a3.html">卡三</a></h3>'
    '<b class="price-type">9999</b></li>'
    '<li data-follow-id="4"><h3><a title="索泰 RTX 5080 16G"'
    ' href="//detail.zol.com.cn/vga/a4.html">诱饵</a></h3>'
    '<b class="price-type">8299</b></li>'
    "</ul>"
)

#: Yahoo chart 应答(meta 直取价与涨跌幅;regularMarketTime = 2026-10-23
#: 04:00 UTC,UTC 与东八区同日 —— 期望串按测试机时区动态渲染防漂)。
YAHOO_MARKET_TIME = 1792728000
EXPECTED_STOCK_WHEN = datetime.fromtimestamp(YAHOO_MARKET_TIME).strftime(
    "%Y-%m-%d"
)
YAHOO_PAYLOAD = {
    "chart": {
        "result": [
            {
                "meta": {
                    "longName": "NVIDIA Corporation",
                    "symbol": "NVDA",
                    "regularMarketPrice": 210.96,
                    "regularMarketChangePercent": -0.59,
                    "regularMarketTime": YAHOO_MARKET_TIME,
                    "currency": "USD",
                }
            }
        ]
    }
}

#: B站合集 API 应答(最新一期标题含「显卡日报」,生产 2026-10-24 实测形态)。
BILI_PAYLOAD = {
    "code": 0,
    "message": "OK",
    "data": {
        "archives": [
            {
                "aid": 117490793517234,
                "bvid": "BV1Tcn86mEnN",
                "title": "RTX50系中端显卡价格翻倍｜显卡日报10月24日",
            }
        ]
    },
}


def tencent_body(
    *,
    price: str = "210.96",
    prev: str = "212.21",
    when: str = "2026-10-23 16:00:01",
    pct: str = "-0.59",
) -> bytes:
    """腾讯行情 gbk 应答(生产字段序:parts[3]=现价 [4]=昨收 [30]=时间 [32]=涨%).

    尾部补两段占位让 ``";` 收尾落在 parts[34](真实 payload 远超 33 段,
    parts[32] 中段干净可 float —— 生产同构)。
    """
    parts = ['v_usNVDA="200', "英伟达", "NVDA.OQ", price, prev]
    parts += ["0"] * 25  # 占位 5..29
    parts += [when, "", pct]  # 30 时间 / 31 空段 / 32 涨%
    parts += ["尾段", "收尾"]  # 33..:引号收尾落最后一段,不污染 [32]
    return ("~".join(parts) + '";').encode("gbk")


def vendor_handler(
    *,
    yahoo: str = "ok",
    tencent: str = "ok",
    firecrawl: str = "ok",
    bilibili: str = "ok",
):
    """四端点路由 mock(yahoo/tencent/firecrawl/bilibili 各可控生死)."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        host = request.url.host
        if host == "query1.finance.yahoo.com":
            if yahoo != "ok":
                return httpx.Response(500, text="yahoo down")
            return httpx.Response(200, json=YAHOO_PAYLOAD)
        if host == "qt.gtimg.cn":
            if tencent != "ok":
                return httpx.Response(500, text="qt down")
            return httpx.Response(200, content=tencent_body())
        if host == "fc.test":
            if firecrawl != "ok":
                return httpx.Response(500, text="fc down")
            return httpx.Response(
                200, json={"success": True, "data": {"html": ZOL_HTML}}
            )
        if host == "api.bilibili.com":
            if bilibili != "ok":
                return httpx.Response(500, text="bili down")
            return httpx.Response(200, json=BILI_PAYLOAD)
        return httpx.Response(404, text=f"unexpected {request.url}")

    return handler


def vendor_options(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "title": "AI 厂商行情 · NVIDIA",
        "stock": {"symbol": "NVDA"},
        "msrp": dict(MSRP_TABLE),
        "fx": 7.25,
    }
    base.update(overrides)
    return base


def make_engine(
    *,
    handler=None,
    options: dict[str, Any] | None = None,
    **source_overrides: Any,
) -> VendorMarketEngine:
    """直构引擎(MockTransport + 静音限速;firecrawl 端点默认走 env 注入)."""
    data: dict[str, Any] = {
        "name": "ai-vendor-daily",
        "engine": "vendor_market",
        "url": "https://myia.local/ai-vendor-daily",
        "engine_options": {
            "vendor_market": vendor_options() if options is None else options
        },
    }
    data.update(source_overrides)
    source = make_source(**data)
    if handler is None:
        handler = vendor_handler()
    context, _clock = make_context(make_client(handler), silent_limiter=True)
    return VendorMarketEngine(source, context)


@pytest.fixture(autouse=True)
def _firecrawl_env(monkeypatch: pytest.MonkeyPatch):
    """firecrawl 端点 env 注入(引擎 env 回退路径;测试零钥匙串)."""
    monkeypatch.setenv("MYIA_FIRECRAWL_URL", "https://fc.test")
    monkeypatch.setenv("MYIA_FIRECRAWL_API_KEY", "fc-test-key")


# --------------------------------------------------------------- 词表与链外


def test_registered_off_chain_and_schema_vocab():
    """vendor_market 在册、AUTO_CHAIN 不在、auto 单级链、schema 词表收词."""
    assert "vendor_market" in ENGINE_REGISTRY
    assert "vendor_market" not in AUTO_CHAIN
    assert auto_degrade("vendor_market") == ["vendor_market"]
    assert resolve_engine("vendor_market") is VendorMarketEngine
    assert "vendor_market" in ENGINES
    make_engine()  # schema 接受显式 engine: vendor_market


# -------------------------------------------------------------- options 校验


@pytest.mark.parametrize(
    ("overrides", "fragment"),
    [
        ({"bogus": 1}, "未知字段"),
        ({"stock": {"provider": "sina"}}, "provider"),
        ({"msrp": {}}, "msrp"),
        ({"msrp": {"RTX 5090": -1}}, "正数"),
        ({"msrp": {"RTX 5090": True}}, "正数"),
        ({"fx": 0}, "fx"),
        ({"fx": "seven"}, "fx"),
        ({"bilibili": {"mid": 0}}, "mid"),
        ({"bilibili": {"keyword": " "}}, "keyword"),
        ({"extra_zol_pages": ["not-a-url"]}, "extra_zol_pages"),
        ({"firecrawl": {"endpoint": "https://plaintext.example"}}, "明文拒绝"),
        ({"firecrawl": {"oops": 1}}, "未知字段"),
        ({"title": ""}, "title"),
    ],
)
def test_invalid_options_structurally_rejected(overrides, fragment):
    """配置形状错 = 结构化 invalid_engine_options(整源拒,不是降级)."""
    engine = make_engine(options=vendor_options(**overrides))
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert fragment in str(excinfo.value)


def test_pagination_and_extract_structurally_rejected():
    """单报表语义:pagination/extract 配置结构化拒(urlwatch 判例).

    schema 交叉校验要求 template 模式 url 带 {page} 占位符 —— 先给合法
    形状过装载,引擎在 fetch 前结构化拒(零 I/O)。
    """
    engine = make_engine(
        url="https://myia.local/vendor?page={page}",
        pagination={"mode": "template", "max_pages": 2},
    )
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "pagination_unsupported"
    engine = make_engine(extract={"type": "json_path", "fields": {"url": "$.x"}})
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "extract_unsupported"


# ------------------------------------------------------------------ 纯函数


def test_normalize_zol_prices_variants_and_first_wins():
    """变体拼写归一(Pro6000D/5090 D)+ 三族外丢弃 + 首见即钉."""
    html = (
        '<a title="NVIDIA RTX PRO 6000D工作站版" href="x">a</a>'
        '<b class="price-type">65000</b>'
        '<a title="微星 RTX Pro6000 D 24G" href="y">b</a>'
        '<b class="price-type">61000</b>'
        '<a title="华硕 RTX 5090 D 32G" href="z">c</a>'
        '<b class="price-type">16999</b>'
        '<a title="索泰 RTX 5080" href="w">d</a>'
        '<b class="price-type">8299</b>'
    )
    assert normalize_zol_prices(html) == {
        "RTX PRO 6000": 65000,  # 首见即钉:第二张 61000 不覆盖
        "RTX 5090": 16999,
    }


def test_build_gpu_rows_three_branches_and_stopped():
    """比价三分支(持平 <3% / 贵 / 便宜)+ 停产行 + 行帽(fx=7.25 账)."""
    msrp = dict(MSRP_TABLE)
    cn = {"RTX PRO 6000": 62000, "RTX 5090": 16499, "RTX 4090": 9999}
    rows = build_gpu_rows(msrp, cn)
    assert rows == [
        # 8500*7.25=61625 → +0.61% 持平;1999*7.25→14493 → +13.8% 贵 14%;
        # 1599*7.25→11593 → -13.7% 便宜 14%;5080 无国行价 → 停产。
        "　RTX PRO 6000: 美价 $8,500(≈¥61,625) ｜ 国行 ¥62,000 ｜ 持平",
        "　RTX 5090: 美价 $1,999(≈¥14,493) ｜ 国行 ¥16,499 ｜ 贵 14%",
        "　RTX 4090: 美价 $1,599(≈¥11,593) ｜ 国行 ¥9,999 ｜ 便宜 14%",
        f"　RTX 5080: 美价 $999(≈¥7,243) ｜ {GPU_STOPPED_SUFFIX}",
    ]


def test_build_gpu_rows_cap():
    """行帽 = 生产 rows[:5]."""
    wide = {f"M{i}": 100 + i for i in range(8)}
    cn = {f"M{i}": 100 for i in range(8)}
    assert len(build_gpu_rows(wide, cn)) == 5


def test_format_stock_line_production_format():
    """股价行格式串逐字(生产 ai_daily_report.py:44-48):箭头/数据时间."""
    assert format_stock_line(210.96, -0.59, "2026-10-23") == (
        "股价 $210.96(-0.6%↓ 今日 · 数据时间2026-10-23)"
    )
    assert format_stock_line(212.5, 1.23) == "股价 $212.50(+1.2%↑ 今日)"


# ---------------------------------------------------------------- 全活形态


def test_full_alive_single_item_and_report_layout():
    """三路全活 → 一条目;报告版式逐行断言(生产行文案);metadata 观测键."""
    engine = make_engine()
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    assert re.search(r"#vendor-\d{8}$", item["url"])
    assert item["title"] == "AI 厂商行情 · NVIDIA"
    assert item["vendor_degraded"] == []
    assert item["vendor_stock"]["provider"] == "yahoo"
    assert item["vendor_stock"]["price"] == 210.96
    assert item["vendor_gpu"] == {
        "RTX PRO 6000": 62000,
        "RTX 5090": 16499,
        "RTX 4090": 9999,
        "RTX 5080": None,
    }
    assert item["vendor_video_title"] == "RTX50系中端显卡价格翻倍｜显卡日报10月24日"
    assert item["vendor_video_url"] == "https://www.bilibili.com/video/BV1Tcn86mEnN"
    assert item["vendor_report"] == item["content"]
    assert item["content"].splitlines() == [
        "**NVIDIA 🌍**",
        f"　股价 $210.96(-0.6%↓ 今日 · 数据时间{EXPECTED_STOCK_WHEN})",
        "　RTX PRO 6000: 美价 $8,500(≈¥61,625) ｜ 国行 ¥62,000 ｜ 持平",
        "　RTX 5090: 美价 $1,999(≈¥14,493) ｜ 国行 ¥16,499 ｜ 贵 14%",
        "　RTX 4090: 美价 $1,599(≈¥11,593) ｜ 国行 ¥9,999 ｜ 便宜 14%",
        f"　RTX 5080: 美价 $999(≈¥7,243) ｜ {GPU_STOPPED_SUFFIX}",
        "　📺 [每日显卡行情视频｜RTX50系中端显卡价格翻倍｜显卡日报10月24日]"
        "(https://www.bilibili.com/video/BV1Tcn86mEnN)",
    ]
    # Item.from_extracted 键落位:url/title/content 管线键,观测键进 metadata。
    entry = Item.from_extracted(item, source="ai-vendor-daily")
    assert entry.metadata["vendor_report"] == item["vendor_report"]
    assert entry.metadata["vendor_stock"]["provider"] == "yahoo"


# ---------------------------------------------------------------- 股价双源


def test_stock_tencent_fallback_when_yahoo_dead():
    """Yahoo 主源死 → 腾讯备源 gbk 兜底(provider=tencent,行格式同款)."""
    engine = make_engine(handler=vendor_handler(yahoo="dead"))
    items = run(engine.fetch())
    assert items[0]["vendor_stock"]["provider"] == "tencent"
    assert items[0]["vendor_degraded"] == []
    assert "　股价 $210.96(-0.6%↓ 今日 · 数据时间2026-10-23)" in items[0]["content"]


def test_stock_tencent_primary_order(monkeypatch: pytest.MonkeyPatch):
    """provider: tencent = 腾讯主源(Yahoo 死活不影响,首取即中)."""
    options = vendor_options(stock={"symbol": "NVDA", "provider": "tencent"})
    engine = make_engine(
        handler=vendor_handler(yahoo="dead"), options=options
    )
    items = run(engine.fetch())
    assert items[0]["vendor_stock"]["provider"] == "tencent"


def test_stock_both_dead_degrades_line_not_block():
    """股价形态:双源死 → 「股价源暂不可用」降级行,GPU/视频照出,整条在."""
    engine = make_engine(handler=vendor_handler(yahoo="dead", tencent="dead"))
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    assert item["vendor_stock"] is None
    assert item["vendor_degraded"] == ["stock"]
    lines = item["content"].splitlines()
    assert lines[1] == STOCK_DEGRADED_LINE
    assert any("RTX 5090" in line and "贵 14%" in line for line in lines)
    assert any("📺" in line for line in lines)


def test_stock_tencent_garbage_payload_falls_through():
    """腾讯应答缺字段(<33 段)= 该源无效 → 双源语义下整路降级."""
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "query1.finance.yahoo.com":
            return httpx.Response(500, text="yahoo down")
        if request.url.host == "qt.gtimg.cn":
            return httpx.Response(200, content=b"v_usNVDA=short")
        if request.url.host == "fc.test":
            return httpx.Response(
                200, json={"success": True, "data": {"html": ZOL_HTML}}
            )
        if request.url.host == "api.bilibili.com":
            return httpx.Response(200, json=BILI_PAYLOAD)
        return httpx.Response(404, text="robots")

    engine = make_engine(handler=handler)
    items = run(engine.fetch())
    assert items[0]["vendor_degraded"] == ["stock"]
    assert STOCK_DEGRADED_LINE in items[0]["content"]


# ------------------------------------------------------------------- ZOL 路


def test_zol_dead_degrades_line_not_block():
    """ZOL 形态:firecrawl 后端死 → GPU 降级行,股价/视频照出,整条在."""
    engine = make_engine(handler=vendor_handler(firecrawl="dead"))
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    assert item["vendor_degraded"] == ["gpu"]
    assert item["vendor_gpu"] == {model: None for model in MSRP_TABLE}
    lines = item["content"].splitlines()
    assert GPU_DEGRADED_LINE in lines
    assert not any("RTX 5090" in line for line in lines)
    assert "　股价 $210.96" in lines[1]
    assert any("📺" in line for line in lines)


def test_zol_unconfigured_degrades_without_raising(monkeypatch: pytest.MonkeyPatch):
    """firecrawl 端点未配(无 options 引用无 env)= ZOL 路降级,不抛."""
    monkeypatch.delenv("MYIA_FIRECRAWL_URL")
    monkeypatch.delenv("MYIA_FIRECRAWL_API_KEY")
    options = vendor_options()
    options.pop("firecrawl", None)  # 本测试 options 本就未配 firecrawl
    engine = make_engine(options=options)
    items = run(engine.fetch())
    assert items[0]["vendor_degraded"] == ["gpu"]
    assert GPU_DEGRADED_LINE in items[0]["content"]


def test_zol_one_page_dead_keeps_other_page_prices():
    """单页死不抹全区(生产 except: continue 同款):首页死,次页价照出."""
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "fc.test":
            # 首页(引擎页序第一)死,系列页(s11096)活出全部三族价。
            body = json.loads(request.content)
            if str(body.get("url", "")).rstrip("/").endswith("vga"):
                return httpx.Response(500, text="first page down")
            return httpx.Response(
                200, json={"success": True, "data": {"html": ZOL_HTML}}
            )
        return vendor_handler()(request)

    engine = make_engine(handler=handler)
    items = run(engine.fetch())
    assert items[0]["vendor_degraded"] == []
    assert items[0]["vendor_gpu"]["RTX 5090"] == 16499


def test_zol_firecrawl_success_false_continues():
    """firecrawl success:false 应答 = 单页无产出(降级继续,不炸)."""
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "fc.test":
            return httpx.Response(
                200, json={"success": False, "error": "ZOL blocked"}
            )
        return vendor_handler(firecrawl="unused")(request)

    engine = make_engine(handler=handler)
    items = run(engine.fetch())
    assert items[0]["vendor_degraded"] == ["gpu"]
    assert GPU_DEGRADED_LINE in items[0]["content"]


def test_msrp_absent_skips_gpu_section_entirely():
    """msrp 未配 = GPU 比价区整段跳过(无行、无降级、metadata vendor_gpu=None)."""
    options = vendor_options()
    options.pop("msrp")
    engine = make_engine(options=options)
    items = run(engine.fetch())
    item = items[0]
    assert item["vendor_gpu"] is None
    assert item["vendor_degraded"] == []
    lines = item["content"].splitlines()
    assert not any("美价 $" in line for line in lines), "GPU 比价行不应出现"
    assert len(lines) == 3  # 厂商头 + 股价行 + 视频行


# ------------------------------------------------------------------ B站路


def test_bilibili_dead_drops_video_line():
    """B站形态:API 死 → 视频行缺位 + degraded 留痕,股价/GPU 照出."""
    engine = make_engine(handler=vendor_handler(bilibili="dead"))
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    assert item["vendor_degraded"] == ["video"]
    assert item["vendor_video_title"] is None
    assert item["vendor_video_url"] is None
    lines = item["content"].splitlines()
    assert not any("📺" in line for line in lines)
    assert any("RTX 5090" in line for line in lines)


def test_bilibili_no_keyword_match_drops_video_line():
    """应答活但无期名命中 = 视频行缺位(生产:无视频 = 行不出现)."""
    payload = {"code": 0, "data": {"archives": [
        {"title": "装机模拟器2026EP7", "bvid": "BV1Other"}
    ]}}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "api.bilibili.com":
            return httpx.Response(200, json=payload)
        return vendor_handler(bilibili="unused")(request)

    engine = make_engine(handler=handler)
    items = run(engine.fetch())
    assert items[0]["vendor_video_title"] is None
    assert "📺" not in items[0]["content"]


# ---------------------------------------------------------------- 锚点幂等


def test_anchor_same_day_idempotent():
    """#vendor-<YYYYMMDD> 纯日期函数:同日两跑(两引擎实例)同 URL."""
    first = run(make_engine().fetch())[0]["url"]
    second = run(make_engine().fetch())[0]["url"]
    assert first == second
    assert re.fullmatch(r"https://myia\.local/ai-vendor-daily#vendor-\d{8}", first)


# ------------------------------------------------------------- 真实配置面


def test_category_config_loads_with_vendor_market():
    """config/ai-vendor-daily.yaml:engine/builtin/dedup/archive 路由/msrp 原表."""
    config = load_category_file(CONFIG_DIR / "ai-vendor-daily.yaml")
    assert config.id == "ai-vendor-daily"
    (source,) = config.sources
    assert source.engine == "vendor_market"
    assert config.classify.builtin is False, "报表条目无标题可筛,builtin 只会误杀"
    assert config.dedup.key == "{url}", "锚点已铸日期,同日幂等跨日必新"
    assert config.enrich.enabled is False, "纯确定性计算,零 token"
    assert config.push, "品类必须至少保留一个推送条目"
    for push in config.push:
        modes = [rule.mode for rule in routes_from_config(push.route)]
        assert modes == ["archive"], "发送由 daily-digest 分区承担,仅入库"
        assert resolve_route(
            {"url": "https://myia.local/ai-vendor-daily#vendor-20261024", "title": "t"},
            routes_from_config(push.route),
        ).mode == "archive"
    options = source.extra_params["engine_options"]["vendor_market"]
    assert options["msrp"] == {
        "RTX PRO 6000": 8500,
        "RTX 5090": 1999,
        "RTX 4090": 1599,
    }, "生产 GPU_MSRP_USD 原表"
    assert options["fx"] == 7.25
    assert options["bilibili"] == {
        "mid": 22697887,
        "season_id": 2565297,
        "keyword": "显卡日报",
    }
    firecrawl = options["firecrawl"]
    assert firecrawl["endpoint"] == "keychain:myia/firecrawl/url"
    assert firecrawl["api_key"] == "keychain:myia/firecrawl/api-key"


def test_daily_digest_vendor_section_retargeted():
    """daily-digest「AI 厂商行情」分区:sources 指向 ai-vendor-daily(4.4 改造)."""
    config = load_category_file(CONFIG_DIR / "daily-digest.yaml")
    options = config.sources[0].extra_params["engine_options"]["store_report"]
    by_title = {section["title"]: section for section in options["sections"]}
    assert "AI 厂商行情" in by_title, "分区二应已改造为「AI 厂商行情」"
    section = by_title["AI 厂商行情"]
    assert section["sources"] == ["ai-vendor-daily"]
    assert section["style"] == "detail"
    assert "AI 厂商官网" not in by_title, "旧 prompt 版分区名应已退役"
