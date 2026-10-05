#!/usr/bin/env python3
"""S1 探查第三轮(10-06-ai-news-sources)——round2 头片截断(220B)不足以判
robots 全文与 RSS autodiscovery;本轮全量记 robots(微软/Meta)+ 在 watch
候选页全文搜 <link rel=alternate type=application/rss+xml>。每 URL 单次。"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
UA = "MYIA-source-probe/0.1 (+https://github.com/xinzhuzi/myia; feed reachability check)"
TIMEOUT = 20.0

FULL_ROBOTS = [
    "https://www.microsoft.com/robots.txt",
    "https://ai.meta.com/robots.txt",
]

AUTODISCOVERY_PAGES = {
    "anthropic-news": "https://www.anthropic.com/news",
    "meta-ai-blog": "https://ai.meta.com/blog",
    "cohere-blog": "https://cohere.com/blog",
    "qwen-blog": "https://qwenlm.github.io/blog/",
    "moonshot-home": "https://www.moonshot.cn",
    "minimax-home": "https://www.minimaxi.com",
    "seed-home": "https://seed.bytedance.com",
    "zhipu-news": "https://www.zhipuai.cn/news",
}


def fetch(client: httpx.Client, url: str) -> httpx.Response:
    return client.get(url, follow_redirects=True, timeout=TIMEOUT)


def main() -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out: dict = {"meta": {"utc": stamp, "round": 3}, "robots_full": {}, "autodiscovery": {}}
    lines = [f"# S1 探查第三轮回执(robots 全文 + autodiscovery 全文搜)\n", f"- UTC: {stamp}\n"]

    with httpx.Client(headers={"User-Agent": UA}) as client:
        for url in FULL_ROBOTS:
            try:
                r = fetch(client, url)
                body = r.text
                out["robots_full"][url] = {"status": r.status_code, "body": body}
                disallows = [ln.strip() for ln in body.splitlines() if "disallow" in ln.lower()]
                lines.append(f"## robots {url} → {r.status_code},共 {len(disallows)} 行 Disallow")
                for ln in disallows:
                    lines.append(f"- {ln}")
                lines.append("")
            except Exception as exc:  # noqa: BLE001
                out["robots_full"][url] = {"error": str(exc)[:200]}
                lines.append(f"## robots {url} → 失败 {exc}\n")
            time.sleep(0.7)
        for name, url in AUTODISCOVERY_PAGES.items():
            try:
                r = fetch(client, url)
                body = r.text
                links = re.findall(r"<link[^>]+rel=[\"']?alternate[\"']?[^>]*>", body, re.I)
                feeds = [ln for ln in links if "rss" in ln.lower() or "atom" in ln.lower()]
                title = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
                out["autodiscovery"][name] = {
                    "url": url,
                    "status": r.status_code,
                    "bytes": len(r.content),
                    "title": (title.group(1).strip()[:80] if title else ""),
                    "feed_links": feeds[:5],
                }
                verdict = "有 feed 声明:" + "; ".join(feeds[:3]) if feeds else "无 RSS autodiscovery"
                lines.append(
                    f"- **{name}**({url})→ {r.status_code},title=「{title.group(1).strip()[:60] if title else '?'}」:{verdict}"
                )
            except Exception as exc:  # noqa: BLE001
                out["autodiscovery"][name] = {"url": url, "error": str(exc)[:200]}
                lines.append(f"- **{name}**({url})→ 失败 {str(exc)[:120]}")
            time.sleep(0.7)

    (HERE / "probe3-results.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (HERE / "probe3-log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"probe3 done -> probe3-log.md")


if __name__ == "__main__":
    main()
