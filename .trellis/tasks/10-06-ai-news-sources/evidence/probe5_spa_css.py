#!/usr/bin/env python3
"""国产五家 SPA watch 重探(10-06-ai-news-sources,research §7 兑现轮).

背景:research §2 暂缓的五家(zhipu/moonshot/minimax/seed/deepseek)当时判
「SPA 软 200 无 feed,快照=巨型 JS 壳」;§10 已给 urlwatch 引擎落 CSS 内容
过滤链(engine_options.urlwatch.selector → 上游 filter: css{selector,
exclude, method:html}),anthropic/cohere 实证框架噪声出局。本轮用**同一条
链**重探五家:

- Phase 0 robots 先行(单次;四家在档复验 + deepseek 补档——probe2/3 的
  robots 清单里没有 deepseek,本轮补);
- Phase 1 初筛:每家单次抓页,honest UA,本地用上游 ``LxmlParser``(与
  生产 CssFilter 同一入口)试 main/#app/#__next/#root/[role=main]/article
  选择器,记过滤后 html 长度/纯文本长度/预览;
- Phase 2 背靠背双跑:初筛出可读正文(>500 字)的每家×最优选择器,用
  ``urlwatch.worker.run_jobs``+与生产相同的 filter 形状跑两遍(独立
  cache),R2=unchanged 才可接。

运行(任务指定形态):
  uv run --no-project --with urlwatch --with cssselect python probe5_spa_css.py

产物:probe5-log.md + probe5-results.json(+ probe5-cache/ 双跑快照留档)。
"""

from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlparse

import requests
import urlwatch
from urlwatch.filters import LxmlParser
from urlwatch.storage import CacheMiniDBStorage, UrlsYaml
from urlwatch.worker import run_jobs

HERE = Path(__file__).resolve().parent
UA = (
    "MYIA-source-probe/0.1 (+https://github.com/xinzhuzi/myia; spa css-filter re-probe)"
)
TIMEOUT = 30.0

# 五家目标页(research §2 的 URL 面;zhipu 用 /news 列表页,其余各家首页)
TARGETS = [
    ("zhipu", "https://www.zhipuai.cn/news"),
    ("moonshot", "https://www.moonshot.cn/"),
    ("minimax", "https://www.minimaxi.com/"),
    ("seed", "https://seed.bytedance.com/"),
    ("deepseek", "https://www.deepseek.com/"),
]

# 候选选择器(任务点名 main/#app/#__next/[role=main]/article 等;#root 为
# React 常见挂载点补入;body 仅作过滤基线对照,不入候选)
CANDIDATE_SELECTORS = ["main", "#app", "#__next", "#root", "[role=main]", "article"]
BASELINE_SELECTOR = "body"

# 与生产 src/myssia/engines/urlwatch.py 完全一致的过滤子参数
EXCLUDE = "script, style, noscript, template, svg"
METHOD = "html"

TEXT_MIN_CHARS = 500  # 判定线:过滤后纯文本 >500 字才算可读正文


class Collector:
    """同款 JSON collector(照抄 adapter SHIM_SOURCE;上游 Report 鸭子类型)."""

    def __init__(self) -> None:
        self.events: list[dict] = []

    def _record(self, verb: str, job_state: SimpleNamespace) -> None:
        event = {
            "event": verb,
            "name": job_state.job.pretty_name(),
            "location": job_state.job.get_location(),
            "timestamp": job_state.timestamp,
        }
        if verb == "error":
            event["error"] = str(job_state.exception)
        self.events.append(event)

    def new(self, job_state: SimpleNamespace) -> None:
        self._record("new", job_state)

    def changed(self, job_state: SimpleNamespace) -> None:
        self._record("changed", job_state)

    def unchanged(self, job_state: SimpleNamespace) -> None:
        self._record("unchanged", job_state)

    def error(self, job_state: SimpleNamespace) -> None:
        self._record("error", job_state)


def decode_like_urlwatch(response: requests.Response) -> str:
    """照抄上游 UrlJob.retrieve 的 decode(header 无 charset 先试 UTF-8).

    初轮探针直接用 ``response.text``(requests 对无 charset 的 text/html
    落 ISO-8859-1)→ moonshot/deepseek 预览 mojibake;生产 urlwatch 链是
    UTF-8-first(上游 retrieve 源码亲核),探针必须同形才不冤枉站点。
    """
    content_type = response.headers.get("Content-Type", "")
    if re.match(r"text/(?:html|plain); charset=", content_type):
        return response.text  # charset 显式,requests 已正确解码
    raw = response.content or b""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin1")


def fetch(url: str) -> dict:
    """单次抓取(requests,honest UA);一切失败都是证据不抛出."""
    started = time.monotonic()
    try:
        response = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
        return {
            "status": response.status_code,
            "bytes": len(response.content or b""),
            "text": (
                decode_like_urlwatch(response) if response.status_code == 200 else ""
            ),
            "elapsed_s": round(time.monotonic() - started, 2),
            "error": "",
        }
    except Exception as exc:  # noqa: BLE001 - 探查脚本:一切失败都是证据
        return {
            "status": None,
            "bytes": 0,
            "text": "",
            "elapsed_s": round(time.monotonic() - started, 2),
            "error": f"{type(exc).__name__}: {exc}"[:260],
        }


def robots_allows(robots_text: str, path: str) -> tuple[bool, str]:
    """粗粒度 robots 判定:只看 User-agent: * 段的 Allow/Disallow 前缀规则.

    404/空文本=无 robots(默认允许)。最长前缀匹配(robots 通配不展开,
    探针够用;精确面以 robots.txt 原文留档为准)。
    """
    if not robots_text or not robots_text.strip():
        return True, "no robots body (default allow)"
    star_rules: list[tuple[str, str]] = []
    in_star = False
    for line in robots_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"(?i)user-agent\s*:\s*(.+)", stripped)
        if match:
            in_star = match.group(1).strip() == "*"
            continue
        rule = re.match(r"(?i)(allow|disallow)\s*:\s*(\S*)", stripped)
        if rule and in_star:
            star_rules.append((rule.group(1).lower(), rule.group(2)))
    best_len, best = -1, "allow"
    for verb, prefix in star_rules:
        if not prefix or path.startswith(prefix):
            if len(prefix) >= best_len:
                best_len, best = len(prefix), verb
    return best == "allow", f"star-rules={star_rules or 'none'} -> {best}"


def css_filter_len(html_text: str, selector: str) -> dict:
    """与生产同链的 css 过滤(上游 LxmlParser),返回长度面+预览(自测过
    零命中=空串不崩;一切异常记证据)."""
    import lxml.html

    started = time.monotonic()
    try:
        parser = LxmlParser(
            "css",
            {"selector": selector, "exclude": EXCLUDE, "method": METHOD},
            "selector",
        )
        parser.feed(html_text)
        filtered = parser.get_filtered_data()
        text = lxml.html.fromstring(filtered).text_content() if filtered else ""
        text_norm = re.sub(r"\s+", " ", text).strip()
        return {
            "selector": selector,
            "filtered_html_chars": len(filtered),
            "text_chars": len(text_norm),
            "preview": text_norm[:160],
            "error": "",
            "elapsed_s": round(time.monotonic() - started, 2),
        }
    except Exception as exc:  # noqa: BLE001 - 探查脚本:一切失败都是证据
        return {
            "selector": selector,
            "filtered_html_chars": 0,
            "text_chars": 0,
            "preview": "",
            "error": f"{type(exc).__name__}: {exc}"[:200],
            "elapsed_s": round(time.monotonic() - started, 2),
        }


def run_once(jobs_path: Path, cache_path: Path) -> dict:
    """跑一遍 urlwatch worker(照抄 SHIM_SOURCE 构造;每遍独立开关 cache)."""
    jobs = UrlsYaml(str(jobs_path)).load()
    cache = CacheMiniDBStorage(str(cache_path))
    collector = Collector()
    urlwatcher = SimpleNamespace(
        urlwatch_config=SimpleNamespace(tags=None, idx_set=set(), joblist=[]),
        jobs=jobs,
        cache_storage=cache,
        config_storage=SimpleNamespace(config={"job_defaults": {}, "display": {}}),
        report=collector,
        should_run=lambda idx, job: True,
    )
    try:
        run_jobs(urlwatcher)
    finally:
        cache.close()
    return {
        "checked": len(jobs),
        "events": collector.events,
        "urlwatch_version": getattr(urlwatch, "__version__", None),
    }


def main() -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    robots_rows: list[dict] = []
    page_rows: list[dict] = []
    selector_rows: list[dict] = []

    # ── Phase 0: robots 先行(五家 host 各单次)────────────────────────
    robots_by_vendor: dict[str, dict] = {}
    for vendor, url in TARGETS:
        origin = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        row = fetch(f"{origin}/robots.txt")
        row.update({"vendor": vendor, "origin": origin})
        row["robots_text"] = row.pop("text", "")
        allowed, reason = robots_allows(
            row["robots_text"] if row["status"] == 200 else "",
            urlparse(url).path or "/",
        )
        if row["status"] == 404:
            allowed, reason = True, "robots 404 (default allow)"
        elif row["status"] != 200:
            allowed, reason = False, f"robots status {row['status']}"
        row["allowed"] = allowed
        row["reason"] = reason
        robots_by_vendor[vendor] = row
        robots_rows.append(
            {k: v for k, v in row.items() if k != "robots_text"}
            | {"robots_head": row["robots_text"][:120].replace("\n", " ")}
        )
        time.sleep(1.0)

    # ── Phase 1: 每家单次抓页 + 多选择器本地初筛(与生产同链)──────────
    pages: dict[str, str] = {}
    for vendor, url in TARGETS:
        row = fetch(url)
        row.update({"vendor": vendor, "url": url})
        page_rows.append({k: v for k, v in row.items() if k != "text"})
        if row["status"] == 200 and row["text"]:
            pages[vendor] = row["text"]
        time.sleep(1.0)

    best: dict[str, dict] = {}
    for vendor, html_text in pages.items():
        for selector in CANDIDATE_SELECTORS + [BASELINE_SELECTOR]:
            result = css_filter_len(html_text, selector)
            result["vendor"] = vendor
            selector_rows.append(result)
            if selector in CANDIDATE_SELECTORS and not result["error"]:
                if (
                    vendor not in best
                    or result["text_chars"] > best[vendor]["text_chars"]
                ):
                    best[vendor] = result
        time.sleep(0.3)

    # ── Phase 2: 初筛通过者背靠背双跑(生产同链 filter 形状)────────────
    passed = {
        vendor: result
        for vendor, result in best.items()
        if result["text_chars"] > TEXT_MIN_CHARS
        and robots_by_vendor.get(vendor, {}).get("allowed") is True
    }
    dual_rows: list[dict] = []
    if passed:
        jobs_dir = HERE / "probe5-cache"
        jobs_dir.mkdir(exist_ok=True)
        jobs_path = jobs_dir / "jobs.yaml"
        cache_path = jobs_dir / "cache.db"
        if cache_path.exists():
            cache_path.unlink()  # 探针基线从零起(不碰生产 ~/.myia/urlwatch/)
        docs = [
            {
                "name": vendor,
                "url": dict(TARGETS)[vendor],
                "filter": [
                    {
                        "css": {
                            "selector": passed[vendor]["selector"],
                            "exclude": EXCLUDE,
                            "method": METHOD,
                        }
                    }
                ],
            }
            for vendor in passed
        ]
        jobs_path.write_text(
            "\n---\n".join(json.dumps(doc, ensure_ascii=False) for doc in docs) + "\n",
            encoding="utf-8",
        )
        r1 = run_once(jobs_path, cache_path)
        time.sleep(2.0)
        r2 = run_once(jobs_path, cache_path)
        for vendor in passed:
            events1 = [e for e in r1["events"] if e["name"] == vendor]
            events2 = [e for e in r2["events"] if e["name"] == vendor]
            verbs1 = [e["event"] for e in events1]
            verbs2 = [e["event"] for e in events2]
            dual_rows.append(
                {
                    "vendor": vendor,
                    "selector": passed[vendor]["selector"],
                    "text_chars": passed[vendor]["text_chars"],
                    "r1_events": verbs1,
                    "r2_events": verbs2,
                    "r2_unchanged": verbs2 == ["unchanged"],
                    "r2_detail": [
                        e.get("error", "") for e in events2 if e["event"] == "error"
                    ],
                }
            )
        # 双跑事件全量留档(含 R1 error 面,如有)
        (jobs_dir / "dual-run-events.json").write_text(
            json.dumps({"r1": r1, "r2": r2}, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )

    # ── 落盘:JSON + 人读 log ──────────────────────────────────────────
    payload = {
        "meta": {
            "utc": stamp,
            "ua": UA,
            "round": 5,
            "urlwatch_version": getattr(urlwatch, "__version__", None),
            "text_min_chars": TEXT_MIN_CHARS,
            "exclude": EXCLUDE,
            "method": METHOD,
            "selectors": CANDIDATE_SELECTORS + [f"{BASELINE_SELECTOR} (baseline)"],
            "note": "spa css-filter re-probe (research §7): same LxmlParser chain "
            "as production engine_options.urlwatch.selector; decode fixed to "
            "urlwatch utf-8-first (initial pass used requests .text -> mojibake "
            "on moonshot/deepseek, tool-layer bug same family as probe round1)",
        },
        "robots": robots_rows,
        "pages": page_rows,
        "selectors": selector_rows,
        "dual_run": dual_rows,
    }
    (HERE / "probe5-results.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    lines = [
        "# 国产五家 SPA watch 重探(css 内容过滤轮,research §7 兑现)",
        "",
        f"- UTC: {stamp}",
        f"- UA: {UA}",
        f"- urlwatch: {payload['meta']['urlwatch_version']}",
        "- 链路:与生产同(上游 LxmlParser,css{selector, exclude="
        f"'{EXCLUDE}', method:html);判定线=纯文本 >{TEXT_MIN_CHARS} 字且双跑 R2=unchanged",
        "",
        "## Phase 0 robots(单次先行;四家复验 + deepseek 补档)",
        "",
        "| vendor | status | allowed | 判据 |",
        "|---|---|---|---|",
    ]
    for row in robots_rows:
        lines.append(
            f"| {row['vendor']} | {row['status']} | {'✅' if row['allowed'] else '❌'} "
            f"| {row['reason'][:100]} |"
        )
    lines += [
        "",
        "## Phase 1 页面 + 选择器初筛(每家单次抓取,本地过滤)",
        "",
        "| vendor | page status | page bytes | selector | filtered html | 纯文本字数 | 预览 |",
        "|---|---|---|---|---|---|---|",
    ]
    page_by_vendor = {row["vendor"]: row for row in page_rows}
    for row in selector_rows:
        page = page_by_vendor[row["vendor"]]
        lines.append(
            f"| {row['vendor']} | {page['status']} | {page['bytes']} | "
            f"`{row['selector']}` | {row['filtered_html_chars']} | {row['text_chars']} "
            f"| {row['preview'][:80] or row['error'][:60]} |"
        )
    lines += [
        "",
        "## Phase 2 背靠背双跑(初筛 >500 字且 robots 允许者;R2=unchanged 才可接)",
        "",
        "| vendor | selector | 纯文本 | R1 | R2 | 判定 |",
        "|---|---|---|---|---|---|",
    ]
    for row in dual_rows:
        verdict = "✅ 可接" if row["r2_unchanged"] else "❌ 漂移/失败"
        lines.append(
            f"| {row['vendor']} | `{row['selector']}` | {row['text_chars']} | "
            f"{','.join(row['r1_events']) or '-'} | {','.join(row['r2_events'])} | {verdict} |"
        )
    if not dual_rows:
        lines.append("| (无通过初筛者) | | | | | |")
    (HERE / "probe5-log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"probe5 done: {len(robots_rows)} robots, {len(page_rows)} pages, "
        f"{len(selector_rows)} selector rows, {len(dual_rows)} dual-run -> probe5-log.md"
    )


if __name__ == "__main__":
    main()
