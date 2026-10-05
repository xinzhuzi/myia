#!/usr/bin/env python
"""TLS 指纹归因矩阵探针(10-05-engine-curl-cffi Q1 实证材料)。

设计(计划指令定案):
- 三路:A = httpx + MYIA static_html 缺省 UA(与 src/myssia/engines/
  fetch_base.py:135 DEFAULT_USER_AGENT 逐字节一致);B = httpx + Chrome UA
  控制组(UA 取自 C 路对 echo 端点实发 UA 的回读——B/C 的 UA 逐字节同,
  差异收窄到 TLS+HTTP/2 指纹与底层栈);C = curl_cffi requests
  impersonate="chrome"(0.16.3 DEFAULT_CHROME=chrome150,macOS Tahoe)。
- 归因矩阵:A 拒+B 拒+C 过 = TLS/HTTP2 指纹归因(curl_cffi 独有增量);
  A 拒+B 过 = UA 归因(headers 配置即可解,curl_cffi 增量存疑);
  全拒 = 硬墙(JS 挑战类,curl_cffi 不够);全过 = 无墙。
- 涉网纪律:每 URL 每路单次请求,超时 20s,失败不重试不轰炸;同站相邻
  请求间 1s 礼貌间隔;robots 记录见 02-*.md(探询清单已经 robots 核对)。

不 import myssia(评估期零核心依赖,亦免疫 selectolax 解析墙)。

用法:/tmp/curl-eval/bin/python probe_tls_matrix.py 2>&1 | tee 03-tls-matrix-run.log
"""

from __future__ import annotations

import json
import re
import sys
import time

import httpx
from curl_cffi import requests as creq

# 与 src/myssia/engines/fetch_base.py:135 DEFAULT_USER_AGENT 逐字节一致
MYIA_UA = "MYIA/0.1 (config-driven intelligence hub)"

# C 路回读失败时的兜底 UA(echo 端点不可达时 B 路仍可跑,残余差异如实记)
CHROME_UA_FALLBACK = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")

ECHO_URL = "https://tls.browserleaks.com/json"  # JA3/JA4/UA 回显(robots 404=无限制,已记档)

CONTENT_URLS = [
    # (标签, URL, 说明)
    ("aihot-item", "https://aihot.news/items/bzodztryi4kvwm4kz9mrwb6nn",
     "archive/10-04-crawl4ai-l3 基线 URL,crawl4ai 真跑 PASS(markdown_len=3949)"),
    ("airbnb-home", "https://www.airbnb.com/",
     "curl_cffi README 经典 TLS 指纹墙例(* 组放行首页,robots 已记档)"),
    ("nowsecure-nl", "https://nowsecure.nl/",
     "Cloudflare 挑战测试页(robots 无 Disallow)"),
    ("scrapingcourse-cf", "https://scrapingcourse.com/cloudflare-challenge",
     "Cloudflare managed challenge 测试页(robots * 仅禁 /ecommerce/*)"),
    ("hn-home", "https://news.ycombinator.com/",
     "无墙对照站(robots 放行首页,Crawl-delay 30 远高于单次探询)"),
]

TIMEOUT_S = 20.0
TITLE_RE = re.compile(rb"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)

ECHO_KEYS = ("user_agent", "ja3_hash", "ja4", "ja4_r", "akamai_fp_hash",
             "http2_fingerprint", "tls_version", "cipher_suite")


def classify(status: int | None, body: bytes, title: str) -> str:
    """成功判据:2xx 且载荷非空且非挑战页标题。"""
    if status is None or not (200 <= status < 300):
        return "blocked"
    if len(body) < 200:
        return "blocked(thin-body)"
    low = title.lower()
    if "just a moment" in low or "attention required" in low or "verifying you are human" in low:
        return "blocked(challenge-page)"
    return "ok"


def _meta(r, body: bytes) -> dict:
    title_m = TITLE_RE.search(body[:200_000])
    title = title_m.group(1).decode("utf-8", "replace").strip()[:90] if title_m else ""
    hdr = getattr(r, "headers", {})
    out = {
        "status": getattr(r, "status_code", None),
        "http_version": getattr(r, "http_version", "") or "",
        "bytes": len(body),
        "server": hdr.get("server", ""),
        "cf_mitigated": hdr.get("cf-mitigated", ""),
        "title": title,
        "verdict": classify(getattr(r, "status_code", None), body, title),
    }
    # echo 端点:附带指纹回显字段(在则记)
    try:
        j = r.json()
        if isinstance(j, dict):
            for k in ECHO_KEYS:
                if k in j:
                    out[k] = str(j[k])[:120]
    except Exception:
        pass
    return out


def probe_httpx(url: str, ua: str) -> dict:
    headers = {
        "User-Agent": ua,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    t0 = time.perf_counter()
    try:
        with httpx.Client(timeout=TIMEOUT_S, follow_redirects=True) as client:
            r = client.get(url, headers=headers)
        out = _meta(r, r.content)
    except Exception as exc:  # noqa: BLE001 - 失败形态本身是实验数据
        out = {"status": None, "http_version": "", "bytes": 0, "server": "",
               "cf_mitigated": "", "title": "", "verdict": f"error:{type(exc).__name__}",
               "error": str(exc)[:160]}
    out["elapsed_s"] = round(time.perf_counter() - t0, 2)
    return out


def probe_curlcffi(url: str) -> dict:
    t0 = time.perf_counter()
    try:
        r = creq.get(url, impersonate="chrome", timeout=TIMEOUT_S)
        out = _meta(r, r.content or b"")
    except Exception as exc:  # noqa: BLE001
        out = {"status": None, "http_version": "", "bytes": 0, "server": "",
               "cf_mitigated": "", "title": "", "verdict": f"error:{type(exc).__name__}",
               "error": str(exc)[:160]}
    out["elapsed_s"] = round(time.perf_counter() - t0, 2)
    return out


def main() -> int:
    results: dict = {"echo": {}, "matrix": {}}

    # ── Phase 0:echo 端点(C 先行回读 UA → A/B 用同 UA 各打一次;每路单次)──
    print(f"== Phase 0: echo {ECHO_URL} (每路单次) ==")
    c_echo = probe_curlcffi(ECHO_URL)
    chrome_ua = c_echo.get("user_agent") or CHROME_UA_FALLBACK
    print(f"  C(curl_cffi chrome): ja3={c_echo.get('ja3_hash','?')} ja4={c_echo.get('ja4','?')} "
          f"ua={chrome_ua!r} verdict={c_echo['verdict']}")
    time.sleep(1)
    a_echo = probe_httpx(ECHO_URL, MYIA_UA)
    print(f"  A(httpx+MYIA UA): ja3={a_echo.get('ja3_hash','?')} ja4={a_echo.get('ja4','?')} "
          f"verdict={a_echo['verdict']}")
    time.sleep(1)
    b_echo = probe_httpx(ECHO_URL, chrome_ua)
    print(f"  B(httpx+Chrome UA): ja3={b_echo.get('ja3_hash','?')} ja4={b_echo.get('ja4','?')} "
          f"verdict={b_echo['verdict']}")
    results["echo"] = {"A": a_echo, "B": b_echo, "C": c_echo,
                       "chrome_ua_echoed": c_echo.get("user_agent", ""),
                       "chrome_ua_source": "echo" if c_echo.get("user_agent") else "fallback"}
    time.sleep(1)

    # ── Phase 1:内容站矩阵 ──
    for tag, url, note in CONTENT_URLS:
        print(f"\n== {tag}: {url}  ({note}) ==")
        row_a = probe_httpx(url, MYIA_UA)
        print(f"  A(httpx+MYIA UA): {row_a}")
        time.sleep(1)
        row_b = probe_httpx(url, chrome_ua)
        print(f"  B(httpx+Chrome UA): {row_b}")
        time.sleep(1)
        row_c = probe_curlcffi(url)
        print(f"  C(curl_cffi chrome): {row_c}")
        results["matrix"][tag] = {"url": url, "note": note,
                                  "A": row_a, "B": row_b, "C": row_c}

    print("\n== JSON ==")
    print(json.dumps(results, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
