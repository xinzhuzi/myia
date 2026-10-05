#!/usr/bin/env python3
"""S1 探查第二轮(10-06-ai-news-sources)——修复 round1 sniff 的 bytes/str bug 后重取证.

round1 工具故障(在档):probe_vendors.py 的 sniff() 用 `"<html" in head`(str
in bytes)→ **一切 200 响应在判形时崩**,被 except 记成「网络失败」。受害者=
全部 robots 探查 + 8 条 feed 探查(智谱/月暗/MiniMax/Seed/DeepSeek/cohere 的
200 证据被毁)。本轮对被毁证据重取证(每 URL 仍单次),并补 watch 候选页。

产物:probe2-log.md + probe2-results.json。
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

HERE = Path(__file__).resolve().parent
UA = "MYIA-source-probe/0.1 (+https://github.com/xinzhuzi/myia; feed reachability check)"
TIMEOUT = 20.0

# 被毁证据重取证:robots(进入 YAML 判定面的宿主)
ROBOTS_HOSTS = [
    "https://openai.com",
    "https://www.anthropic.com",
    "https://deepmind.google",
    "https://research.google",
    "https://ai.meta.com",
    "https://www.microsoft.com",
    "https://mistral.ai",
    "https://huggingface.co",
    "https://qwenlm.github.io",
    "https://www.zhipuai.cn",
    "https://bigmodel.cn",
    "https://www.moonshot.cn",
    "https://www.minimaxi.com",
    "https://seed.bytedance.com",
]

# 被毁证据重取证:feed(round1 里 200→崩→误记网络失败的 URL)+ 新候选 qwen feed.xml
FEEDS = {
    "zhipu": "https://www.zhipuai.cn/rss.xml",
    "bigmodel": "https://bigmodel.cn/rss.xml",
    "moonshot": "https://www.moonshot.cn/rss.xml",
    "minimax": "https://www.minimaxi.com/rss.xml",
    "seed-rss": "https://seed.bytedance.com/rss.xml",
    "seed-feed": "https://seed.bytedance.com/feed.xml",
    "deepseek-www": "https://www.deepseek.com/rss.xml",
    "cohere-blog": "https://cohere.com/blog/rss.xml",
    "qwen-feed": "https://qwenlm.github.io/feed.xml",
}

# watch 候选页(S2:urlwatch 引擎目标;判 200+html+直连可达)
PAGES = {
    "anthropic-news": "https://www.anthropic.com/news",
    "meta-ai-blog": "https://ai.meta.com/blog",
    "xai-news": "https://x.ai/news",
    "cohere-blog-page": "https://cohere.com/blog",
    "qwen-blog-page": "https://qwenlm.github.io/blog/",
    "zhipu-news": "https://www.zhipuai.cn/news",
    "deepseek-home": "https://www.deepseek.com",
}


def sniff(body: bytes, content_type: str) -> str:
    head = body[:600].lstrip().lower()
    ctype = (content_type or "").lower()
    if head.startswith(b"<?xml") or "xml" in ctype:
        if b"<rss" in body[:1200] or b"<channel" in body[:1500]:
            return "rss"
        if b"<feed" in body[:1200]:
            return "atom"
        return "xml"
    if b"<html" in head[:400] or b"<!doctype html" in head[:40] or "html" in ctype:
        return "html"
    return "other"


def probe_one(client: httpx.Client, url: str) -> dict:
    started = time.monotonic()
    try:
        response = client.get(url, follow_redirects=True, timeout=TIMEOUT)
        elapsed = time.monotonic() - started
        body = response.content or b""
        return {
            "url": url,
            "status": response.status_code,
            "final_url": str(response.url),
            "content_type": response.headers.get("content-type", ""),
            "bytes": len(body),
            "elapsed_s": round(elapsed, 2),
            "shape": sniff(body, response.headers.get("content-type", "")),
            "head": body[:220].decode("utf-8", "replace").replace("\n", " "),
            "error": "",
        }
    except Exception as exc:  # noqa: BLE001 - 探查脚本:一切失败都是证据
        return {
            "url": url,
            "status": None,
            "final_url": "",
            "content_type": "",
            "bytes": 0,
            "elapsed_s": round(time.monotonic() - started, 2),
            "shape": "",
            "head": "",
            "error": f"{type(exc).__name__}: {exc}"[:260],
        }


def main() -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    robots_rows: list[dict] = []
    feed_rows: list[dict] = []
    page_rows: list[dict] = []

    with httpx.Client(headers={"User-Agent": UA}) as direct:
        for origin in ROBOTS_HOSTS:
            row = probe_one(direct, f"{origin}/robots.txt")
            row["kind"] = "robots"
            row["host"] = origin.split("//", 1)[1]
            robots_rows.append(row)
            time.sleep(0.5)
        for vendor, url in FEEDS.items():
            row = probe_one(direct, url)
            row.update({"kind": "feed", "vendor": vendor, "path": "direct"})
            feed_rows.append(row)
            time.sleep(0.7)
        for vendor, url in PAGES.items():
            row = probe_one(direct, url)
            row.update({"kind": "page", "vendor": vendor, "path": "direct"})
            page_rows.append(row)
            time.sleep(0.7)

    payload = {
        "meta": {"utc": stamp, "ua": UA, "round": 2, "note": "sniff bytes/str bug fixed; re-probe of destroyed evidence + watch pages"},
        "robots": robots_rows,
        "feeds": feed_rows,
        "pages": page_rows,
    }
    (HERE / "probe2-results.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = [
        "# S1 探查第二轮回执(sniff bug 修复后重取证)",
        "",
        f"- UTC: {stamp}",
        "- round1 工具故障在档:200 响应被 sniff 崩成「网络失败」,本轮对被毁证据逐 URL 重探(仍单次)",
        "",
        "## robots 重取证(直连)",
        "",
        "| host | status | bytes | head 片段 |",
        "|---|---|---|---|",
    ]
    for row in robots_rows:
        lines.append(f"| {row['host']} | {row['status']} | {row['bytes']} | {row['head'][:90] or row['error'][:90]} |")
    lines += ["", "## feed 重取证", "", "| vendor | status | shape | bytes | head 片段 |", "|---|---|---|---|---|"]
    for row in feed_rows:
        lines.append(f"| {row['vendor']} | {row['status']} | {row['shape'] or '-'} | {row['bytes']} | {row['head'][:80] or row['error'][:80]} |")
    lines += ["", "## watch 候选页(S2)", "", "| vendor | status | shape | bytes | 落点 |", "|---|---|---|---|---|"]
    for row in page_rows:
        if row["status"] == 200 and row["shape"] == "html":
            verdict = "✅ watch 候选(200 html)"
        elif row["status"] == 200:
            verdict = f"⚠️ 200 但形状 {row['shape']}"
        else:
            verdict = f"❌ {row['status'] if row['status'] else '网络失败:' + row['error'][:60]}"
        lines.append(f"| {row['vendor']} | {row['status']} | {row['shape'] or '-'} | {row['bytes']} | {verdict} |")
    (HERE / "probe2-log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"probe2 done: {len(robots_rows)} robots, {len(feed_rows)} feeds, {len(page_rows)} pages -> probe2-log.md")


if __name__ == "__main__":
    main()
