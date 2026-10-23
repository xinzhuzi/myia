"""厂商行情引擎 —— 股价 + GPU 跨区比价 + 显卡日报视频,聚合单条目,链外.

``engine: vendor_market`` 显式选择才生效(链外注册,prompt/store_report
先例):``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式
选择 = 单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

语义(华为云 ai-news-bot ``ai_daily_report.py:30-109`` 的 MYIA 承载,
10-24-huawei-ai-news-absorb D4;正则/格式串逐字参照生产):一个源 = 一份
厂商行情速览 —— 三路抓取 + 纯确定性计算(零 LLM),产出**一条**条目,
markdown 报告放 ``metadata.vendor_report``(prompt_summary/report_markdown
合并判例,push 模板经 item_view 直接可渲染)::

    **NVIDIA 🌍**
    　股价 $210.96(-0.6%↓ 今日 · 数据时间2026-10-23)
    　RTX PRO 6000: 美价 $8,500(≈¥61,625) ｜ 国行 ¥62,000 ｜ 持平
    　RTX 5090: 美价 $1,999(≈¥14,493) ｜ 国行 ¥16,499 ｜ 贵 14%
    　📺 [每日显卡行情视频｜RTX50系…｜显卡日报10月24日](https://www.bilibili.com/video/BV…)

三路抓取(全走引擎共享 HTTP 栈,礼貌面 prompt 引擎同款 —— 逐 URL
robots 自查 + per-host 限速 + 重试退避;proxy 源级 ``direct``/``pool:``
经 BaseEngine 统一挂载):

1. **股价**(双源任一活即出价,生产 10-20 换道判例的 MYIA 双保险):
   Yahoo chart(``query1.finance.yahoo.com/v8/finance/chart/<symbol>``,
   stocks.yaml 同端点;主源)→ 败则腾讯 ``qt.gtimg.cn/q=us<symbol>``
   (gbk 解码、``~`` 分段解析,生产 ``fetch_nvda_stock`` 逐字移植;备源)
   → 双败 = 股价行标降级,**不废整块**;
2. **ZOL 国行 GPU 价**:复用 firecrawl 云客户端(gpu-prices 判例:ZOL
   反爬门,静态直抓 152B 壳,云渲染真页)抓 ``detail.zol.com.cn/vga/``
   与 ``vga/s11096/``(5090 系列页,2026-10-20 生产修复),行内
   ``title="…"…price-type">N<`` 正则抽价,型号归一(Pro6000D/5090D
   变体映射,生产 ``fetch_gpu_prices`` 逐字移植);firecrawl 端点
   未配/失败 = GPU 区标降级,不废整块;
3. **B站显卡日报视频**:合集 API
   ``api.bilibili.com/x/polymer/web-space/seasons_archives_list``,取最新
   标题含关键词期(UA+Referer+buvid3 头,生产 ``fetch_gpu_daily_video``
   同款;mid/season_id/关键词可配);失败 = 视频行缺位 + 降级留痕,不废整块。

计算(纯确定性):美价 = ``msrp`` 常量表;``≈¥ = round(usd * fx)``;
``diff%`` → 便宜/贵/持平(``|diff| < 3%`` 判持平,生产口径)。

去重键适配(#prompt- 判例):品类级 ``dedup.key: {url}`` 会把「明天的
行情」全期吞掉,引擎给条目 URL 铸**日期锚点** ``<源url>#vendor-<YYYYMMDD>``
(本地日期,日报语义)—— 每天一个新 URL = 新去重键,同日重跑幂等。

失败模型(生产 10-20 判例「源站异常不能让 NVIDIA 整块消失」):**每路
独立降级** —— 单路异常(网络/HTTP/解析/凭据解析)只降级该路(行内标注
或行缺位 + 日志 + ``vendor_degraded`` 清单),整条照出;仅
``invalid_engine_options``(配置形状错)与 ``pagination``/``extract``
配置是结构化拒。``asyncio.CancelledError`` 属 BaseException,不进降级
分支(取消不是降级)。

配置形状(``engine_options.vendor_market``):

- ``title``(可选):条目标题(缺省 = 源名);
- ``header``(可选):报告首行厂商头(缺省 ``NVIDIA 🌍``,生产原文);
- ``stock``(可选):``{symbol?, provider?}`` —— symbol 缺省 ``NVDA``;
  provider ``yahoo``(缺省,Yahoo 主→腾讯备)| ``tencent``(腾讯主→
  Yahoo 备);
- ``msrp``(可选):型号 → USD 官价表(生产
  ``GPU_MSRP_USD = {RTX PRO 6000: 8500, RTX 5090: 1999, RTX 4090: 1599}``;
  省略/空表 = GPU 比价区整段跳过 —— 无表可比);
- ``fx``(可选):USD_CNY 汇率常量(缺省 :data:`DEFAULT_FX_USD_CNY`
  7.25,生产「每周校准」由改配置承担);
- ``bilibili``(可选):``{mid?, season_id?, keyword?}``(缺省 = 生产
  UP主芝士华莱士 mid=22697887 / season_id=2565297 / 关键词「显卡日报」);
- ``extra_zol_pages``(可选):追加 ZOL 页 URL 清单(生产改版适配位);
- ``firecrawl``(可选):``{endpoint, api_key, timeout?}`` —— 云客户端
  凭据引用(``env:``/``keychain:`` only,明文拒;gpu-prices.yaml 同款),
  缺省回退 ``MYIA_FIRECRAWL_URL``/``MYIA_FIRECRAWL_API_KEY`` env,皆无 =
  ZOL 路降级(不抛)。

型号归一词表钉 RTX PRO 6000/5090/4090 三族(生产判例):``msrp`` 表配
其他型号会恒落「国行已停产无现货报价」——ZOL 抽价只认这三族的变体拼写。

Raises:
    FetchError: ``invalid_engine_options``(配置形状错:msrp 非正数/词表
        外 provider/凭据引用明文等);``pagination``/``extract`` 配置结构化
        拒(单报表语义,urlwatch 判例)。
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchError,
    mask_endpoint_url,
)
from myssia.schema import (
    CredentialResolveError,
    parse_secret_value,
    resolve_credential,
)

logger = logging.getLogger(__name__)

#: 引擎层标签(schema 引擎词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "VENDOR_MARKET"

#: USD_CNY 汇率常量缺省(生产 ``USD_CNY = 7.25``,每周校准由配置承担)。
DEFAULT_FX_USD_CNY = 7.25

#: 股价标的缺省(生产钉 NVDA;NVIDIA 恒定第一的生产判例)。
DEFAULT_STOCK_SYMBOL = "NVDA"

#: 股价主源词表:yahoo = Yahoo 主→腾讯备;tencent = 腾讯主→Yahoo 备
#: (生产 10-20 因 Yahoo 403 华为云 IP 换道腾讯;MYIA 本机双源任一活即出价)。
STOCK_PROVIDERS = ("yahoo", "tencent")

#: Yahoo chart 端点(config/stocks.yaml 同端点,主源)。
YAHOO_CHART_URL = (
    "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    "?range=5d&interval=1d"
)

#: 腾讯美股行情端点(生产 fetch_nvda_stock 同款,gbk 应答)。
TENCENT_QUOTE_URL = "https://qt.gtimg.cn/q=us{symbol}"

#: B站合集 API 端点模板(生产 fetch_gpu_daily_video 同款,免签名档)。
BILIBILI_SEASON_URL = (
    "https://api.bilibili.com/x/polymer/web-space/seasons_archives_list"
    "?mid={mid}&season_id={season_id}&sort_reverse=true&page_num=1&page_size=3"
)

#: B站 UP主「芝士华莱士」缺省(mid/season_id 生产同值;keyword = 期名过滤词)。
DEFAULT_BILIBILI_MID = 22697887
DEFAULT_BILIBILI_SEASON_ID = 2565297
DEFAULT_BILIBILI_KEYWORD = "显卡日报"

#: ZOL 显卡页缺省两页(生产 2026-10-20 修复:5090 不在首页产品卡,增抓
#: s11096 系列页;4090 已停产系列页被 5070Ti 顶替 —— 由 msrp 表驱动输出)。
DEFAULT_ZOL_PAGES = (
    "https://detail.zol.com.cn/vga/",
    "https://detail.zol.com.cn/vga/s11096/",
)

#: ZOL 抽价正则(生产 ai_daily_report.py:87 逐字移植):
#: ``title="型号…"`` 后 600 字符内首个 ``price-type">NNNN<``。
ZOL_PRICE_RE = re.compile(
    r'title="([^"]{4,80})"[^>]*>.{0,600}?price-type">(\d{4,6})<', re.S
)

#: 型号归一规则(生产 ai_daily_report.py:89-94 逐字移植:变体拼写 →
#: msrp 表键;顺序即优先级 —— Pro 6000 先于 5090/4090)。
MODEL_RULES: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"RTX\s?Pro\s?6000", re.I), "RTX PRO 6000"),
    (re.compile(r"RTX\s?5090", re.I), "RTX 5090"),
    (re.compile(r"RTX\s?4090", re.I), "RTX 4090"),
)

#: GPU 比价行帽(生产 ``rows[:5]``)。
GPU_ROWS_CAP = 5

#: 持平判定阈(生产口径:``abs(diff) < 3`` 判持平)。
FLAT_THRESHOLD_PCT = 3.0

#: firecrawl 云端点单页抓取预算缺省(秒,firecrawl 引擎同值)。
DEFAULT_FIRECRAWL_TIMEOUT_SECONDS = 60.0

#: firecrawl 端点/key 的 env 回退名(firecrawl 引擎同款)。
ENV_FIRECRAWL_URL = "MYIA_FIRECRAWL_URL"
ENV_FIRECRAWL_API_KEY = "MYIA_FIRECRAWL_API_KEY"

#: 浏览器 UA(腾讯/B站请求头,生产同款字符串)。
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "Chrome/131.0.0.0 Safari/537.36"
)

#: 腾讯行情 Referer(生产同款)。
TENCENT_REFERER = "https://gu.qq.com/"

#: 报告行文案(生产逐字:降级标注与视频行前缀;``　`` = 全角空格缩进)。
STOCK_DEGRADED_LINE = "　股价源暂不可用"
GPU_DEGRADED_LINE = "　GPU 价格源暂不可用(ZOL 改版或网络异常)"
GPU_STOPPED_SUFFIX = "国行已停产无现货报价"
VIDEO_LINE_TEMPLATE = "　📺 [每日显卡行情视频｜{title}]({url})"

__all__ = [
    "BILIBILI_SEASON_URL",
    "BROWSER_USER_AGENT",
    "DEFAULT_BILIBILI_KEYWORD",
    "DEFAULT_BILIBILI_MID",
    "DEFAULT_BILIBILI_SEASON_ID",
    "DEFAULT_FIRECRAWL_TIMEOUT_SECONDS",
    "DEFAULT_FX_USD_CNY",
    "DEFAULT_STOCK_SYMBOL",
    "DEFAULT_ZOL_PAGES",
    "ENV_FIRECRAWL_API_KEY",
    "ENV_FIRECRAWL_URL",
    "FLAT_THRESHOLD_PCT",
    "GPU_DEGRADED_LINE",
    "GPU_ROWS_CAP",
    "GPU_STOPPED_SUFFIX",
    "LAYER",
    "MODEL_RULES",
    "STOCK_DEGRADED_LINE",
    "STOCK_PROVIDERS",
    "TENCENT_QUOTE_URL",
    "TENCENT_REFERER",
    "VIDEO_LINE_TEMPLATE",
    "YAHOO_CHART_URL",
    "VendorMarketEngine",
    "build_gpu_rows",
    "format_stock_line",
    "normalize_zol_prices",
]


# --------------------------------------------------------------------- 纯函数


def normalize_zol_prices(html: str) -> dict[str, int]:
    """ZOL 页 HTML → 型号归一后的国行价映射(首见即钉,生产逐字移植).

    生产 ``fetch_gpu_prices`` 内循环的纯函数化::data:`ZOL_PRICE_RE` 抽
    ``(型号原文, 价格字符串)``,型号经 :data:`MODEL_RULES` 归一到 msrp
    表键(不匹配三族拼写的条目丢弃),同型号首见即钉(列表页首个报价即
    参考价,生产 ``if model not in cn`` 同款)。
    """
    cn: dict[str, int] = {}
    for match in ZOL_PRICE_RE.finditer(html):
        name = match.group(1)
        model: str | None = None
        for pattern, canonical in MODEL_RULES:
            if pattern.search(name):
                model = canonical
                break
        if model is None:
            continue
        if model not in cn:
            cn[model] = int(match.group(2))
    return cn


def build_gpu_rows(
    msrp: Mapping[str, int | float],
    cn_prices: Mapping[str, int],
    *,
    fx: float = DEFAULT_FX_USD_CNY,
) -> list[str]:
    """MSRP 表 + 国行价 → GPU 比价行(生产 ai_daily_report.py:99-109 逐字).

    美价 = MSRP 常量;``≈¥ = round(usd * fx)``;``diff%`` → 便宜/贵/持平
    (``|diff| < 3`` 判持平);无国行价的型号落「国行已停产无现货报价」。
    行帽 :data:`GPU_ROWS_CAP`(生产 ``rows[:5]``)。
    """
    rows: list[str] = []
    for model, usd in msrp.items():
        cny = cn_prices.get(model)
        usd_cny = round(usd * fx)
        if not cny:
            rows.append(
                f"　{model}: 美价 ${usd:,}(≈¥{usd_cny:,}) ｜ {GPU_STOPPED_SUFFIX}"
            )
            continue
        diff = (cny - usd_cny) / usd_cny * 100
        tag = (
            "持平"
            if abs(diff) < FLAT_THRESHOLD_PCT
            else (f"贵 {diff:.0f}%" if diff > 0 else f"便宜 {abs(diff):.0f}%")
        )
        rows.append(
            f"　{model}: 美价 ${usd:,}(≈¥{usd_cny:,}) ｜ 国行 ¥{cny:,} ｜ {tag}"
        )
    return rows[:GPU_ROWS_CAP]


def format_stock_line(
    price: float, day_pct: float, when: str | None = None
) -> str:
    """股价行渲染(生产 ai_daily_report.py:44-48 格式串逐字移植).

    ``when`` = 数据时间(腾讯 ``parts[30][:10]`` / Yahoo regularMarketTime
    格式化的 ``YYYY-MM-DD``);空则省略「 · 数据时间」段。行首 ``　``
    (全角空格)由调用方在拼块时加(生产 ``\n　{stock_line}`` 同款)。
    """
    arrow = "↑" if day_pct >= 0 else "↓"
    wk = f" · 数据时间{when}" if when else ""
    return f"股价 ${price:.2f}({day_pct:+.1f}%{arrow} 今日{wk})"


# ----------------------------------------------------------------------- 引擎


@dataclass
class VendorSpec:
    """engine_options.vendor_market 校验产物(纯数据,渲染/抓取消费)."""

    title: str
    header: str
    symbol: str
    provider: str
    msrp: dict[str, int | float]
    fx: float
    bilibili_mid: int
    bilibili_season_id: int
    bilibili_keyword: str
    zol_pages: tuple[str, ...]
    firecrawl_endpoint: str | None  # 引用原样(解析值不落日志/不落 spec)
    firecrawl_api_key: str | None
    firecrawl_timeout: float


@dataclass
class StockQuote:
    """一档股价观测(渲染与 metadata 消费)."""

    provider: str
    price: float
    day_pct: float
    when: str | None = None


class VendorMarketEngine(BaseEngine):
    """厂商行情速览源(显式 ``engine: vendor_market``;三路抓取+确定性计算).

    items 出口对齐 ``Item.from_extracted`` 契约:整份行情 = **一条**条目
    (url = 日期锚点,title = 配置标题,content = 报告 markdown 入 items 表
    档案),``vendor_report``(同一 markdown)与其余观测键进 metadata ——
    push 模板经 item_view 的 metadata 合并直接可渲染,零 push 层改动
    (prompt 引擎同款)。
    """

    LAYER = "VENDOR_MARKET"
    ENGINE_NAME = "vendor_market"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    # -------------------------------------------------------------- options

    def _options(self) -> VendorSpec:
        """engine_options.vendor_market 校验与缺省化(错型即结构化拒)."""
        options = self.engine_options()
        unknown = set(options) - {
            "title", "header", "stock", "msrp", "fx", "bilibili",
            "extra_zol_pages", "firecrawl",
        }
        if unknown:
            raise FetchError(
                f"engine_options.vendor_market 未知字段 {sorted(unknown)}",
                error_type="invalid_engine_options",
            )
        title = options.get("title", self.source.name)
        if not isinstance(title, str) or not title.strip():
            raise FetchError(
                f"engine_options.vendor_market.title 应为非空字符串,当前为 {title!r}",
                error_type="invalid_engine_options",
            )
        header = options.get("header", "NVIDIA 🌍")
        if not isinstance(header, str) or not header.strip():
            raise FetchError(
                f"engine_options.vendor_market.header 应为非空字符串(报告首行"
                f"厂商头),当前为 {header!r}",
                error_type="invalid_engine_options",
            )
        stock = options.get("stock", {})
        if not isinstance(stock, Mapping):
            raise FetchError(
                f"engine_options.vendor_market.stock 应为 {{symbol?, provider?}} "
                f"映射,当前为 {stock!r}",
                error_type="invalid_engine_options",
            )
        unknown_stock = set(stock) - {"symbol", "provider"}
        if unknown_stock:
            raise FetchError(
                f"engine_options.vendor_market.stock 未知字段 {sorted(unknown_stock)}",
                error_type="invalid_engine_options",
            )
        symbol = stock.get("symbol", DEFAULT_STOCK_SYMBOL)
        if not isinstance(symbol, str) or not symbol.strip():
            raise FetchError(
                f"engine_options.vendor_market.stock.symbol 应为非空股票代码"
                f"(如 NVDA),当前为 {symbol!r}",
                error_type="invalid_engine_options",
            )
        provider = stock.get("provider", "yahoo")
        if provider not in STOCK_PROVIDERS:
            raise FetchError(
                f"engine_options.vendor_market.stock.provider 必须是 "
                f"{list(STOCK_PROVIDERS)} 之一(主源序,双源任一活即出价),"
                f"当前为 {provider!r}",
                error_type="invalid_engine_options",
            )
        msrp_raw = options.get("msrp", {})
        if "msrp" in options and (not isinstance(msrp_raw, Mapping) or not msrp_raw):
            raise FetchError(
                "engine_options.vendor_market.msrp 应为非空 型号→USD 官价映射"
                "(不配 GPU 比价区请直接省略该键 = 整段跳过),"
                f"当前为 {msrp_raw!r}",
                error_type="invalid_engine_options",
            )
        if not isinstance(msrp_raw, Mapping):
            msrp_raw = {}
        msrp: dict[str, float] = {}
        for model, usd in msrp_raw.items():
            if not isinstance(model, str) or not model.strip():
                raise FetchError(
                    f"engine_options.vendor_market.msrp 键应为型号字符串,"
                    f"当前为 {model!r}",
                    error_type="invalid_engine_options",
                )
            if (
                isinstance(usd, bool)
                or not isinstance(usd, (int, float))
                or usd <= 0
            ):
                raise FetchError(
                    f"engine_options.vendor_market.msrp[{model!r}] 应为正数"
                    f"(USD 官价),当前为 {usd!r}",
                    error_type="invalid_engine_options",
                )
            # 原样保留 int/float:渲染 ``${usd:,}`` 对 int 无小数尾巴
            # (生产 GPU_MSRP_USD 整数表,行文案 $8,500 不带 .0)。
            msrp[model.strip()] = usd
        fx = options.get("fx", DEFAULT_FX_USD_CNY)
        if isinstance(fx, bool) or not isinstance(fx, (int, float)) or fx <= 0:
            raise FetchError(
                f"engine_options.vendor_market.fx 应为正数(USD_CNY 汇率常量,"
                f"缺省 {DEFAULT_FX_USD_CNY}),当前为 {fx!r}",
                error_type="invalid_engine_options",
            )
        bilibili = options.get("bilibili", {})
        if not isinstance(bilibili, Mapping):
            raise FetchError(
                f"engine_options.vendor_market.bilibili 应为 {{mid?, season_id?, "
                f"keyword?}} 映射,当前为 {bilibili!r}",
                error_type="invalid_engine_options",
            )
        unknown_bili = set(bilibili) - {"mid", "season_id", "keyword"}
        if unknown_bili:
            raise FetchError(
                f"engine_options.vendor_market.bilibili 未知字段 {sorted(unknown_bili)}",
                error_type="invalid_engine_options",
            )
        mid = bilibili.get("mid", DEFAULT_BILIBILI_MID)
        season_id = bilibili.get("season_id", DEFAULT_BILIBILI_SEASON_ID)
        for name, value in (("mid", mid), ("season_id", season_id)):
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise FetchError(
                    f"engine_options.vendor_market.bilibili.{name} 应为正整数,"
                    f"当前为 {value!r}",
                    error_type="invalid_engine_options",
                )
        keyword = bilibili.get("keyword", DEFAULT_BILIBILI_KEYWORD)
        if not isinstance(keyword, str) or not keyword.strip():
            raise FetchError(
                f"engine_options.vendor_market.bilibili.keyword 应为非空字符串"
                f"(期名过滤词),当前为 {keyword!r}",
                error_type="invalid_engine_options",
            )
        extra_pages = options.get("extra_zol_pages", [])
        if not isinstance(extra_pages, (list, tuple)) or not all(
            isinstance(page, str) and page.startswith(("http://", "https://"))
            for page in extra_pages
        ):
            raise FetchError(
                "engine_options.vendor_market.extra_zol_pages 应为 ZOL 页 "
                f"http(s) URL 字符串清单,当前为 {extra_pages!r}",
                error_type="invalid_engine_options",
            )
        firecrawl_raw = options.get("firecrawl", {})
        if not isinstance(firecrawl_raw, Mapping):
            raise FetchError(
                f"engine_options.vendor_market.firecrawl 应为 {{endpoint, api_key, "
                f"timeout?}} 映射,当前为 {firecrawl_raw!r}",
                error_type="invalid_engine_options",
            )
        unknown_fc = set(firecrawl_raw) - {"endpoint", "api_key", "timeout"}
        if unknown_fc:
            raise FetchError(
                f"engine_options.vendor_market.firecrawl 未知字段 {sorted(unknown_fc)}",
                error_type="invalid_engine_options",
            )
        endpoint = firecrawl_raw.get("endpoint")
        if endpoint is not None:
            endpoint = self._require_ref(
                "engine_options.vendor_market.firecrawl.endpoint", endpoint
            )
        api_key = firecrawl_raw.get("api_key")
        if api_key is not None:
            api_key = self._require_ref(
                "engine_options.vendor_market.firecrawl.api_key", api_key
            )
        fc_timeout = firecrawl_raw.get("timeout", DEFAULT_FIRECRAWL_TIMEOUT_SECONDS)
        if (
            isinstance(fc_timeout, bool)
            or not isinstance(fc_timeout, (int, float))
            or fc_timeout <= 0
        ):
            raise FetchError(
                "engine_options.vendor_market.firecrawl.timeout 应为正数秒,"
                f"当前为 {fc_timeout!r}",
                error_type="invalid_engine_options",
            )
        return VendorSpec(
            title=title.strip(),
            header=header.strip(),
            symbol=symbol.strip().upper(),
            provider=provider,
            msrp=msrp,
            fx=float(fx),
            bilibili_mid=mid,
            bilibili_season_id=season_id,
            bilibili_keyword=keyword.strip(),
            zol_pages=(*DEFAULT_ZOL_PAGES, *extra_pages),
            firecrawl_endpoint=endpoint,
            firecrawl_api_key=api_key,
            firecrawl_timeout=float(fc_timeout),
        )

    @staticmethod
    def _require_ref(field: str, value: Any) -> str:
        """firecrawl 凭据引用形状校验(纯 env:/keychain:,明文拒载).

        只查形状;解析(env 缺/钥匙串未写)延后到 ZOL 路抓取时 —— 单路
        降级语义:解析失败降级该路,不废整条。
        """
        if not isinstance(value, str) or not value.strip():
            raise FetchError(
                f"{field} 应为 env:/keychain: 凭据引用字符串,当前为 {value!r}",
                error_type="invalid_engine_options",
            )
        try:
            parse_secret_value(value.strip(), label=field)
        except Exception as exc:
            raise FetchError(
                f"{field} 必须是纯 env:/keychain: 凭据引用(明文拒绝):{exc}",
                error_type="invalid_engine_options",
            ) from exc
        return value.strip()

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        spec = self._options()
        degraded: list[str] = []

        stock_quote = await self._fetch_stock(spec, degraded)
        gpu_rows, cn_prices = await self._fetch_gpu_rows(spec, degraded)
        video = await self._fetch_video(spec, degraded)

        markdown = self._render(spec, stock_quote, gpu_rows, video)
        now = datetime.now()  # 本地日期 = 日报语义(#prompt- 判例同款)
        stamp = now.strftime("%Y%m%d")
        item: dict[str, Any] = {
            "url": f"{self.source.url}#vendor-{stamp}",
            "title": spec.title,
            "content": markdown,
            "vendor_report": markdown,
            "vendor_date": now.strftime("%Y-%m-%d"),
            "vendor_stock": (
                {
                    "provider": stock_quote.provider,
                    "price": stock_quote.price,
                    "day_pct": stock_quote.day_pct,
                    "data_time": stock_quote.when,
                }
                if stock_quote is not None
                else None
            ),
            "vendor_gpu": (
                None
                if gpu_rows is None
                else {model: cn_prices.get(model) for model in spec.msrp}
            ),
            "vendor_video_title": video[0] if video else None,
            "vendor_video_url": video[1] if video else None,
            "vendor_degraded": degraded,
        }
        logger.info(
            "厂商行情完成: date=%s stock=%s gpu_rows=%s video=%s degraded=%s",
            item["vendor_date"],
            stock_quote.provider if stock_quote else "降级",
            len(gpu_rows) if gpu_rows is not None else "跳过",
            "有" if video else "无",
            ",".join(degraded) or "无",
        )
        return [item]

    # ---------------------------------------------------------- 股价(双源)

    async def _fetch_stock(
        self, spec: VendorSpec, degraded: list[str]
    ) -> StockQuote | None:
        """股价双源:主源败落备源,双败降级(生产 10-20 换道判例双保险)."""
        order = (
            ("yahoo", "tencent")
            if spec.provider == "yahoo"
            else ("tencent", "yahoo")
        )
        for provider in order:
            try:
                if provider == "yahoo":
                    quote = await self._fetch_stock_yahoo(spec)
                else:
                    quote = await self._fetch_stock_tencent(spec)
            except Exception as exc:  # noqa: BLE001 - 单路降级判例(CancelledError 是 BaseException 不进此分支)
                logger.warning(
                    "厂商行情股价源失败(降级换道) provider=%s: %s: %s",
                    provider,
                    type(exc).__name__,
                    exc,
                )
                continue
            if quote is not None:
                return quote
        degraded.append("stock")
        return None

    async def _fetch_stock_yahoo(self, spec: VendorSpec) -> StockQuote | None:
        """Yahoo chart(stocks.yaml 同端点;meta 直取价与涨跌幅).

        无效应答(缺 result/meta/价)返回 None —— 该源视为失败,调用方
        换道(与生产「异常即弃」同语义)。
        """
        url = YAHOO_CHART_URL.format(symbol=spec.symbol)
        await self._ensure_robots_allowed(url)
        await self._acquire_rate_limit(url)
        # 骑引擎基头(源级可覆写 UA;stocks.yaml 判例:诚实 MYIA UA 得 200,
        # 伪装浏览器 UA 反 429 —— 不在引擎里伪装)。
        response = await self._send_with_retry(
            "GET",
            url,
            headers={**self._headers, "Accept": "application/json"},
        )
        payload = response.json()
        result = ((payload or {}).get("chart") or {}).get("result") or []
        if not result:
            return None
        meta = result[0].get("meta") or {}
        price = meta.get("regularMarketPrice")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            return None
        day_pct = meta.get("regularMarketChangePercent")
        when = None
        raw_time = meta.get("regularMarketTime")
        if (
            isinstance(raw_time, (int, float))
            and not isinstance(raw_time, bool)
            and raw_time > 0
        ):
            when = datetime.fromtimestamp(raw_time).strftime("%Y-%m-%d")
        return StockQuote(
            provider="yahoo",
            price=float(price),
            day_pct=(
                float(day_pct)
                if isinstance(day_pct, (int, float)) and not isinstance(day_pct, bool)
                else 0.0
            ),
            when=when,
        )

    async def _fetch_stock_tencent(self, spec: VendorSpec) -> StockQuote | None:
        """腾讯美股行情(gbk 解码 + ``~`` 分段,生产 fetch_nvda_stock 逐字移植).

        字段序(生产注释):``parts[3]=现价 parts[4]=昨收 parts[30]=时间
        parts[32]=涨%``;字段不足 33 段或现价空 = 该源无效(返回 None)。
        """
        url = TENCENT_QUOTE_URL.format(symbol=spec.symbol)
        await self._ensure_robots_allowed(url)
        await self._acquire_rate_limit(url)
        response = await self._send_with_retry(
            "GET",
            url,
            headers={
                "User-Agent": BROWSER_USER_AGENT,
                "Referer": TENCENT_REFERER,
            },
        )
        text = response.content.decode("gbk", "ignore")
        parts = text.split("~")
        if len(parts) < 33 or not parts[3]:
            return None
        px, prev = float(parts[3]), float(parts[4])
        day_pct = float(parts[32]) if parts[32] else (px - prev) / prev * 100
        when = parts[30][:10] if len(parts) > 30 else ""
        return StockQuote(
            provider="tencent", price=px, day_pct=day_pct, when=when or None
        )

    # ------------------------------------------------------ ZOL(firecrawl)

    async def _fetch_gpu_rows(
        self, spec: VendorSpec, degraded: list[str]
    ) -> tuple[list[str] | None, dict[str, int]]:
        """GPU 比价区:msrp 缺省 = 整段跳过;ZOL 全败 = 降级行.

        返回 ``(渲染行清单, 型号→国行价)``;行清单 ``None`` 表示「无 GPU
        区」(未配 msrp,与降级态 ``[GPU_DEGRADED_LINE]`` 分立);单页失败
        降级继续(其余页可能出价,生产 ``except: continue`` 同款),全部页
        无产出才降级标注。
        """
        if not spec.msrp:
            return None, {}
        cn: dict[str, int] = {}
        try:
            for page_url in spec.zol_pages:
                # 单页失败降级继续(生产 ``except: continue`` 同款):其余页
                # 可能出价,一页之死不抹全区的积累。
                try:
                    html = await self._fetch_zol_page(spec, page_url)
                except Exception as exc:  # noqa: BLE001 - 单页降级判例
                    logger.warning(
                        "厂商行情 ZOL 单页失败(降级继续) page=%s: %s: %s",
                        page_url,
                        type(exc).__name__,
                        exc,
                    )
                    continue
                if html is None:
                    continue
                for model, price in normalize_zol_prices(html).items():
                    if model not in cn:
                        cn[model] = price
        except Exception as exc:  # noqa: BLE001 - 单路降级判例(防御:归一循环)
            logger.warning(
                "厂商行情 ZOL 路失败(降级标注) source=%s: %s: %s",
                self.source.name,
                type(exc).__name__,
                exc,
            )
            cn = {}
        if not cn:
            degraded.append("gpu")
            return [GPU_DEGRADED_LINE], cn
        return build_gpu_rows(spec.msrp, cn, fx=spec.fx), cn

    async def _fetch_zol_page(self, spec: VendorSpec, page_url: str) -> str | None:
        """一页 ZOL:firecrawl 云客户端渲染(单页失败降级继续,生产同款).

        礼貌面(firecrawl 引擎判例):robots/限速作用于**目标站**(ZOL),
        我们自己的后端只走重试与掩码日志;单页异常返回 None(调用方继续
        其余页)。端点未配置抛 :class:`FetchError`
        (``firecrawl_not_configured``)—— 由 :meth:`_fetch_gpu_rows` 的
        单路降级语义接住。
        """
        endpoint = self._resolve_firecrawl_endpoint(spec)
        api_key = self._resolve_firecrawl_key(spec)
        url = endpoint.rstrip("/") + "/v1/scrape"
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        body = {
            "url": page_url,
            "formats": ["html"],
            "timeout": int(spec.firecrawl_timeout * 1000),
        }
        await self._ensure_robots_allowed(page_url)
        await self._acquire_rate_limit(page_url)
        response = await self._send_with_retry(
            "POST",
            url,
            json_body=body,
            headers=headers,
            timeout=max(spec.firecrawl_timeout, self.context.timeout),
            log_url=mask_endpoint_url(url),
        )
        payload = response.json()
        if isinstance(payload, dict) and payload.get("success") is False:
            logger.warning(
                "firecrawl 抓取失败 page=%s: %s", page_url, payload.get("error")
            )
            return None
        data = payload.get("data") if isinstance(payload, dict) else None
        html = data.get("html") if isinstance(data, dict) else None
        if not isinstance(html, str) or not html:
            return None
        return html

    def _resolve_firecrawl_endpoint(self, spec: VendorSpec) -> str:
        """端点解析:options 引用 → env 回退;皆无抛(上层降级 ZOL 路).

        解析值不落日志(错误消息只带引用名/env 名;展示形态同 firecrawl
        引擎的 endpoint_display 契约)。
        """
        if spec.firecrawl_endpoint:
            try:
                return resolve_credential(
                    spec.firecrawl_endpoint,
                    backend=self.context.keychain_backend,
                )
            except CredentialResolveError as exc:
                raise FetchError(
                    "firecrawl endpoint 引用解析失败"
                    f"({spec.firecrawl_endpoint}): {exc}",
                    error_type="credential_unresolved",
                ) from exc
        from_env = os.environ.get(ENV_FIRECRAWL_URL, "").strip()
        if from_env:
            return from_env
        raise FetchError(
            "firecrawl 端点未配置(engine_options.vendor_market.firecrawl."
            f"endpoint 引用或 env {ENV_FIRECRAWL_URL}),ZOL 路无法抓取",
            error_type="firecrawl_not_configured",
        )

    def _resolve_firecrawl_key(self, spec: VendorSpec) -> str | None:
        """API key 解析(可缺省 —— env 回退/自托管端点免钥;失败如实抛)."""
        reference = spec.firecrawl_api_key
        if reference is None:
            reference = (
                os.environ.get(ENV_FIRECRAWL_API_KEY, "").strip() or None
            )
        if reference is None:
            return None
        if not reference.startswith(("env:", "keychain:")):
            return reference  # env 回退值已是具体端点钥(非引用形态)
        try:
            return resolve_credential(
                reference, backend=self.context.keychain_backend
            )
        except CredentialResolveError as exc:
            raise FetchError(
                f"firecrawl api_key 引用解析失败({reference}): {exc}",
                error_type="credential_unresolved",
            ) from exc

    # ------------------------------------------------------ B站显卡日报视频

    async def _fetch_video(
        self, spec: VendorSpec, degraded: list[str]
    ) -> tuple[str, str] | None:
        """B站合集 API:最新一期标题含关键词(UA+Referer+buvid3,生产同款).

        返回 ``(标题, 视频URL)``;失败/无命中 = None + ``video`` 降级留痕
        —— 视频行缺位,不废块(生产行为:无视频 = 行整个不出现)。
        """
        try:
            url = BILIBILI_SEASON_URL.format(
                mid=spec.bilibili_mid, season_id=spec.bilibili_season_id
            )
            await self._ensure_robots_allowed(url)
            await self._acquire_rate_limit(url)
            response = await self._send_with_retry(
                "GET",
                url,
                headers={
                    "User-Agent": BROWSER_USER_AGENT,
                    "Referer": f"https://space.bilibili.com/{spec.bilibili_mid}",
                    "Cookie": "buvid3=x",
                },
            )
            payload = response.json()
            archives = ((payload.get("data") or {}).get("archives")) or []
            for archive in archives:
                title = archive.get("title") or ""
                bvid = archive.get("bvid")
                if spec.bilibili_keyword in title and bvid:
                    return str(title), f"https://www.bilibili.com/video/{bvid}"
        except Exception as exc:  # noqa: BLE001 - 单路降级判例
            logger.warning(
                "厂商行情 B站视频路失败(视频行缺位) source=%s: %s: %s",
                self.source.name,
                type(exc).__name__,
                exc,
            )
        degraded.append("video")
        return None

    # --------------------------------------------------------------- 渲染

    def _render(
        self,
        spec: VendorSpec,
        stock_quote: StockQuote | None,
        gpu_rows: list[str] | None,
        video: tuple[str, str] | None,
    ) -> str:
        """三路观测 → 报告 markdown(生产 NVIDIA 块版式,行文案逐字).

        版式(生产 ``block = f"**{fn}. NVIDIA 🌍**\\n　{stock_line}\\n
        {gpu_block}{vd_line}"``):首行厂商头;股价行带全角空格缩进;GPU
        行自带缩进;视频行殿后;msrp 未配 = GPU 区整段不出现。
        """
        lines = [f"**{spec.header}**"]
        lines.append(
            f"　{format_stock_line(stock_quote.price, stock_quote.day_pct, stock_quote.when)}"
            if stock_quote is not None
            else STOCK_DEGRADED_LINE
        )
        if gpu_rows is not None:
            lines.extend(gpu_rows)
        if video is not None:
            lines.append(VIDEO_LINE_TEMPLATE.format(title=video[0], url=video[1]))
        return "\n".join(lines)

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单报表语义:任何 pagination 配置都结构化拒(urlwatch 判例).

        行情对象是「当日一份速览」,翻页游走会让报表的对象漂移。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "vendor_market 引擎是单报表语义(三路抓取即报表对象,每日一份),"
                "不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
