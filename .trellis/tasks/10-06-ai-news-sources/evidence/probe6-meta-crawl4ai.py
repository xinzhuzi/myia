"""probe5: crawl4ai 渲染 ai.meta.com/blog 能否取到博文列表文本.

纪律:单次零压力(一页一加载,cache_mode=BYASS 强制真拉);UA 不伪装
(playwright headless Chromium 真实 UA,即生产通道的真实足迹);robots
面复用 probe3 在案证据(User-agent: * 段允许 /blog,不重复打)。
输出:probe5-meta-crawl4ai.json(结构化结果)+ .markdown.txt(正文摘录)。
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import time
from pathlib import Path

URL = "https://ai.meta.com/blog"
HERE = Path(__file__).resolve().parent
OUT_JSON = HERE / "probe5-meta-crawl4ai.json"
OUT_MD = HERE / "probe5-meta-crawl4ai.markdown.txt"

MAX_MD_DUMP = 40_000


def _markdown_text(result) -> str:  # noqa: ANN001 - crawl4ai 结果对象鸭子类型
    md = getattr(result, "markdown", None)
    if md is None:
        return ""
    raw = getattr(md, "raw_markdown", None)
    if isinstance(raw, str) and raw:
        return raw
    fit = getattr(md, "fit_markdown", None)
    if isinstance(fit, str) and fit:
        return fit
    return md if isinstance(md, str) else ""


async def main() -> None:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig

    t0 = time.monotonic()
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode="BYPASS",
        page_timeout=60_000,
        verbose=False,
    )
    outcome: dict = {
        "probe": "crawl4ai-render-ai-meta-blog",
        "url": URL,
        "crawl4ai_version": None,
        "env_proxy": {
            k: os.environ.get(k)
            for k in ("http_proxy", "https_proxy", "all_proxy", "no_proxy")
        },
    }
    try:
        import importlib.metadata as metadata

        outcome["crawl4ai_version"] = metadata.version("crawl4ai")
    except Exception:  # noqa: BLE001 - 版本取不到不毁探针
        pass

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=URL, config=run_config)
        elapsed = round(time.monotonic() - t0, 1)
        outcome.update(
            {
                "success": bool(result.success),
                "status_code": getattr(result, "status_code", None),
                "elapsed_seconds": elapsed,
                "error_message": (
                    str(result.error_message) if not result.success else None
                ),
            }
        )
        html = getattr(result, "html", "") or ""
        markdown = _markdown_text(result)
        outcome["html_chars"] = len(html)
        outcome["markdown_chars"] = len(markdown)
        # 博文列表判定信号:/blog/<slug> 链接出现次数(静态通道实证为 0)
        blog_links = sorted(set(re.findall(r"/blog/[A-Za-z0-9_-]{3,}", markdown)))
        outcome["blog_slug_links_in_markdown"] = blog_links[:40]
        outcome["blog_slug_link_count"] = len(blog_links)
        # 已知近期博文标题词(meta blog 常见词形,人核用)
        markers = ["Llama", "AI at Meta", "Meta AI", "model", "research"]
        outcome["marker_hits"] = {m: markdown.count(m) for m in markers}
        OUT_MD.write_text(markdown[:MAX_MD_DUMP], encoding="utf-8")
    except Exception as exc:  # noqa: BLE001 - 探针失败也是证据
        outcome.update(
            {
                "success": False,
                "error": f"{type(exc).__name__}: {exc}",
                "elapsed_seconds": round(time.monotonic() - t0, 1),
            }
        )
    OUT_JSON.write_text(
        json.dumps(outcome, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(outcome, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
