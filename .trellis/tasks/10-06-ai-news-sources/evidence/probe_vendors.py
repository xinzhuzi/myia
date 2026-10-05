#!/usr/bin/env python3
"""S1 厂商官方源探查(10-06-ai-news-sources AC1)——robots 先行 + 每候选 URL 单次零压力.

纪律(档内 prd「涉网纪律」):每 URL 只探一次不重试、先 robots 后内容、
honest UA、证据全落本目录。直连失败(网络层/403/451)且本机代理活着时
对同一 URL 补一次代理路探查(独立 egress,单次,记为 proxy 路证据)。

产物:probe-log.md(人读总表)+ probe-results.json(机读全量)。
"""

from __future__ import annotations

import json
import socket
import time
from contextlib import nullcontext
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

import httpx

HERE = Path(__file__).resolve().parent
UA = "MYIA-source-probe/0.1 (+https://github.com/xinzhuzi/myia; feed reachability check)"
TIMEOUT = 20.0

# 候选清单:每厂商 1-3 个官方 feed 猜测位(单次探测,宁多候选不多请求次数
# ——每个 URL 仍只探一次;robots 每宿主只探一次)。
CANDIDATES: dict[str, list[str]] = {
    "openai": [
        "https://openai.com/news/rss.xml",
        "https://openai.com/blog/rss.xml",
    ],
    "anthropic": [
        "https://www.anthropic.com/news/rss.xml",
        "https://www.anthropic.com/rss.xml",
    ],
    "deepmind": [
        "https://deepmind.google/blog/rss.xml",
    ],
    "google-research": [
        "https://research.google/blog/rss/",
    ],
    "meta-ai": [
        "https://ai.meta.com/blog/rss/",
        "https://ai.meta.com/feed/",
    ],
    "microsoft-research": [
        "https://www.microsoft.com/en-us/research/feed/",
    ],
    "xai": [
        "https://x.ai/news/rss.xml",
        "https://x.ai/rss.xml",
    ],
    "mistral": [
        "https://mistral.ai/news/rss.xml",
        "https://mistral.ai/rss.xml",
    ],
    "cohere": [
        "https://cohere.com/blog/rss.xml",
        "https://cohere.com/rss.xml",
    ],
    "hf-blog": [
        "https://huggingface.co/blog/feed.xml",
    ],
    "qwen": [
        "https://qwenlm.github.io/blog/feed.xml",
        "https://qwenlm.github.io/index.xml",
    ],
    "deepseek": [
        "https://api-docs.deepseek.com/rss.xml",
        "https://www.deepseek.com/rss.xml",
    ],
    "zhipu": [
        "https://www.zhipuai.cn/rss.xml",
        "https://bigmodel.cn/rss.xml",
    ],
    "moonshot": [
        "https://www.moonshot.cn/rss.xml",
    ],
    "minimax": [
        "https://www.minimaxi.com/rss.xml",
    ],
    "seed": [
        "https://seed.bytedance.com/rss.xml",
        "https://seed.bytedance.com/feed.xml",
    ],
}

PROXY_PORTS = (7897, 7890, 1087, 8118)


def detect_local_proxy() -> str | None:
    for port in PROXY_PORTS:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.4)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                return f"http://127.0.0.1:{port}"
    return None


def sniff(body: bytes, content_type: str) -> str:
    head = body[:600].lstrip().lower()
    if head.startswith(b"<?xml") or "xml" in (content_type or ""):
        if b"<rss" in body[:1200] or b"<channel" in body[:1500]:
            return "rss"
        if b"<feed" in body[:1200]:
            return "atom"
        return "xml"
    if "<html" in head[:300] or "html" in (content_type or ""):
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
            "shape": sniff(body, response.headers.get("content-type", "")) if response.status_code == 200 else "",
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
    proxy = detect_local_proxy()
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results: dict[str, dict] = {
        "meta": {"utc": stamp, "ua": UA, "local_proxy": proxy, "candidates": CANDIDATES},
        "robots": {},
        "feeds": {},
    }
    hosts_seen: set[str] = set()
    feed_rows: list[dict] = []
    robots_rows: list[dict] = []

    with httpx.Client(headers={"User-Agent": UA}) as direct, (
        httpx.Client(headers={"User-Agent": UA}, proxy=proxy) if proxy else nullcontext(None)
    ) as proxied:
        for vendor, urls in CANDIDATES.items():
            # robots 先行:每宿主一次(direct 路)
            for url in urls:
                host = urlsplit(url).netloc
                if host in hosts_seen:
                    continue
                hosts_seen.add(host)
                robots_url = f"{urlsplit(url).scheme}://{host}/robots.txt"
                row = probe_one(direct, robots_url)
                row["kind"] = "robots"
                row["host"] = host
                robots_rows.append(row)
                time.sleep(0.5)
            for url in urls:
                row = probe_one(direct, url)
                row["kind"] = "feed"
                row["vendor"] = vendor
                row["path"] = "direct"
                feed_rows.append(row)
                # 直连失败(网络层/403/451/5xx)且代理活着 → 同 URL 补一次代理路
                failed = row["status"] is None or row["status"] in (403, 405, 451) or (row["status"] or 0) >= 500
                if failed and proxied is not None:
                    prow = probe_one(proxied, url)
                    prow.update({"kind": "feed", "vendor": vendor, "path": "proxy"})
                    feed_rows.append(prow)
                time.sleep(0.7)  # 零压力:同宿主候选间隔

    results["robots"] = robots_rows
    results["feeds"] = feed_rows
    (HERE / "probe-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    lines = [
        "# S1 厂商官方源探查回执",
        "",
        f"- UTC: {stamp} · honest UA: `{UA}`",
        f"- 本机代理探测(端口 {list(PROXY_PORTS)}): {proxy or '全部不通,仅直连'}",
        f"- 候选 {sum(len(v) for v in CANDIDATES.values())} URL / {len(CANDIDATES)} 厂商;纪律=每 URL 单次 + robots 每宿主先行",
        "",
        "## robots(直连,每宿主一次)",
        "",
        "| host | status | bytes | 判读 |",
        "|---|---|---|---|",
    ]
    for row in robots_rows:
        verdict = "允许/无 robots" if (row["status"] in (200, 404, None) and "disallow" not in row["head"].lower()) else (
            "有 Disallow 行,入 YAML 前需对照 feed 路径" if row["status"] == 200 else "网络失败"
        )
        lines.append(f"| {row['host']} | {row['status']} | {row['bytes']} | {verdict} |")
    lines += ["", "## feed 探查", "", "| vendor | path | status | shape | bytes | 落点 |", "|---|---|---|---|---|---|"]
    for row in feed_rows:
        note = row["final_url"] if row["final_url"] != row["url"] else ""
        if row["status"] == 200 and row["shape"] in ("rss", "atom"):
            verdict = "✅ 可用 feed"
        elif row["status"] == 200 and row["shape"] in ("html", "other"):
            verdict = "⚠️ 200 但非 feed 形状(可能是 HTML 404 页)"
        elif row["status"] is None:
            verdict = "❌ 网络失败"
        else:
            verdict = f"❌ HTTP {row['status']}"
        lines.append(
            f"| {row['vendor']} | {row['path']} | {row['status']} | {row['shape'] or '-'} | {row['bytes']} | {verdict} {note} |"
        )
    (HERE / "probe-log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"probe done: {len(feed_rows)} feed probes, {len(robots_rows)} robots probes; log -> probe-log.md")


if __name__ == "__main__":
    main()
