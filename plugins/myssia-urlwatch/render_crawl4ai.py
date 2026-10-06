"""myssia-urlwatch 渲染 helper:crawl4ai 取纯文本正文,喂 urlwatch shell job.

背景(10-06-ai-news-sources §10/§12):ai.meta.com/blog 是纯客户端渲染页,
静态通道六种 CSS 选择器全零判死;urlwatch 上游的 ShellJob(kind: shell,
``command`` 必填)以**命令 stdout 为监控对象**,本 helper 就是那个命令——
用 crawl4ai 无头渲染一页,把博文列表归一成纯文本打印到 stdout,快照对比
与 diff 语义全部复用上游(urlwatch 侧零改动)。

调用形状(由引擎 :func:`myssia.engines.urlwatch.build_render_command` 装配):

``<python> render_crawl4ai.py <url>``

- ``<python>`` = 运行 myssia 的解释器(``sys.executable``;crawl4ai 装在哪个
  环境就由哪个环境跑,uv 临时 urlwatch 环境不背浏览器重依赖);
- stdout = 归一化正文(**只**打印监控对象;诊断一律走 stderr);
- 退出码:``0`` 成功 / ``1`` 渲染失败 / ``3`` 渲染后端未安装(区分于抓取
  失败,装机 doctor 面可辨)。

归一化(:func:`strip_markdown_noise`):markdown 里的图片与链接 URL 剔除
(fbcdn CDN 图片带 ``oe=``/``_nc_oc=`` 轮换签名参数,保留即逐次快照漂移=
每 run 假阳性,probe6 实证),标题/日期等正文文字保留——快照只随真实
内容变化。单页单加载(零压力);UA 不伪装(headless Chromium 真实身份,
robots 面由引擎在抓取前照查)。

本件是场景件(MYIA 创作,非上游代码),自包含:仅标准库 + crawl4ai,
不 import myssia(插件目录不是包,也不绑核心版本)。
"""

from __future__ import annotations

import argparse
import asyncio
import re
import sys
from typing import Iterable

#: 渲染页预算秒(crawl4ai page_timeout 毫秒制;probe6 实测整页 ~7-8s)。
PAGE_TIMEOUT_SECONDS = 60

#: 退出码词表:0 成功 / 1 渲染失败 / 3 渲染后端缺失。
EXIT_OK = 0
EXIT_FETCH_FAILED = 1
EXIT_BACKEND_MISSING = 3

#: 图片 markdown(``![alt](url)``)整段剔除——url 带轮换签名,纯噪声。
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")

#: 链接 markdown(``[text](url)``)只留 text。
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")

#: 3+ 连续空行归一双空行。
_BLANK_RUN_RE = re.compile(r"\n{3,}")

__all__ = [
    "EXIT_BACKEND_MISSING",
    "EXIT_FETCH_FAILED",
    "EXIT_OK",
    "PAGE_TIMEOUT_SECONDS",
    "main",
    "strip_markdown_noise",
]


def strip_markdown_noise(markdown: str) -> str:
    """渲染 markdown → 稳定纯文本快照(图片/链接 URL 出局,正文文字保留).

    CDN 签名轮换(``oe=``/``_nc_oc=`` 等)只存在于图片/链接 URL 里,剔除后
    快照漂移面收敛到真实内容变化;标题、日期、分类等文字原样保留。链接
    文字尾随空白(如 ``[标题 ](url)`` 剥 URL 后的悬空空格)逐行 rstrip 归一
    ——不可见字符漂移不进快照(复核轮:精确形状由等值断言钉死)。
    """
    text = _IMAGE_RE.sub("", markdown)
    text = _LINK_RE.sub(r"\1", text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    text = _BLANK_RUN_RE.sub("\n\n", text)
    return text.strip() + "\n"


async def _crawl_markdown(url: str) -> str:
    """crawl4ai 渲染一页,返回原始 markdown(惰性 import,失败让 caller 分类)."""
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode="BYPASS",  # 快照语义要真拉,crawl4ai 自带缓存一律旁路
        page_timeout=PAGE_TIMEOUT_SECONDS * 1000,
        verbose=False,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
    if not getattr(result, "success", False):
        raise RuntimeError(
            f"crawl4ai 渲染失败: {getattr(result, 'error_message', '') or '未知错误'}"
        )
    # 0.9.x 的 result.markdown 是 MarkdownGenerationResult(raw_markdown 属性),
    # 旧版是 str——鸭子兼容,与核心 L3 引擎同款手法。
    markdown = getattr(result, "markdown", None)
    raw = getattr(markdown, "raw_markdown", None)
    if isinstance(raw, str) and raw:
        return raw
    return markdown if isinstance(markdown, str) else ""


def main(argv: Iterable[str] | None = None) -> int:
    """CLI 入口:归一化正文打印 stdout;失败走 stderr + 非零退出码."""
    parser = argparse.ArgumentParser(
        description="crawl4ai 渲染一页并打印归一化纯文本(urlwatch shell job 体)"
    )
    parser.add_argument("url", help="要渲染的目标页地址(http/https)")
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        markdown = asyncio.run(_crawl_markdown(args.url))
    except ImportError as exc:  # crawl4ai 未装:依赖缺失,与抓取失败分形
        print(f"渲染后端 crawl4ai 不可用: {exc}", file=sys.stderr)
        return EXIT_BACKEND_MISSING
    except Exception as exc:  # noqa: BLE001 - 渲染失败统一退出 1(诊断进 stderr)
        print(f"crawl4ai 渲染失败 url={args.url}: {exc}", file=sys.stderr)
        return EXIT_FETCH_FAILED
    sys.stdout.write(strip_markdown_noise(markdown))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
