#!/usr/bin/env python3
"""probe5b:五家过滤后正文可读性摘录落档(可读性判定的证据面).

probe5 的 log 只有 160 字预览,「可读正文」判定需要更长摘录落档。对五家
(zhipu/moonshot/minimax/seed + 已记死的 deepseek 对照)各单次抓页,用与
生产同链的 LxmlParser(utf-8-first decode,probe5 修正轮同款)过滤出最优
选择器的纯文本,全文(截 4000 字)写 probe5b-readable-excerpt.txt。

运行:uv run --no-project --with urlwatch --with cssselect python probe5b_readable.py
"""

from __future__ import annotations

import re
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from urlwatch.filters import LxmlParser

HERE = Path(__file__).resolve().parent
UA = (
    "MYIA-source-probe/0.1 (+https://github.com/xinzhuzi/myia; spa css-filter re-probe)"
)
TIMEOUT = 30.0
EXCLUDE = "script, style, noscript, template, svg"

# probe5 修正轮选出的每家最优选择器(deepseek 为记死对照)
TARGETS = [
    ("zhipu", "https://www.zhipuai.cn/news", "main"),
    ("moonshot", "https://www.moonshot.cn/", "#root"),
    ("minimax", "https://www.minimaxi.com/", "main"),
    ("seed", "https://seed.bytedance.com/", "main"),
    ("deepseek", "https://www.deepseek.com/", "main"),
]


def decode_like_urlwatch(response: requests.Response) -> str:
    """照抄上游 UrlJob.retrieve 的 decode(probe5 修正轮同款)."""
    content_type = response.headers.get("Content-Type", "")
    if re.match(r"text/(?:html|plain); charset=", content_type):
        return response.text
    raw = response.content or b""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin1")


def main() -> None:
    import lxml.html

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# probe5b:五家过滤后正文可读性摘录(probe5 修正轮同链,2026-" + stamp + ")",
        "",
        f"- UA: {UA};过滤链与生产同:css{{selector, exclude='{EXCLUDE}', method:html}}",
        "- 每家单次抓取;摘录截 4000 字;总字数=归一化空白后的全文长度",
        "",
    ]
    for vendor, url, selector in TARGETS:
        try:
            response = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
            html_text = decode_like_urlwatch(response)
            parser = LxmlParser(
                "css",
                {"selector": selector, "exclude": EXCLUDE, "method": "html"},
                "selector",
            )
            parser.feed(html_text)
            filtered = parser.get_filtered_data()
            text = (
                re.sub(
                    r"\s+", " ", lxml.html.fromstring(filtered).text_content()
                ).strip()
                if filtered
                else ""
            )
            excerpt = text[:4000]
            lines += [
                f"## {vendor} — `{selector}`(总 {len(text)} 字,filtered html "
                f"{len(filtered)} 字符)",
                "",
                excerpt or "(空)",
                "",
            ]
        except Exception as exc:  # noqa: BLE001 - 探查脚本:一切失败都是证据
            lines += [
                f"## {vendor} — `{selector}` 失败:{type(exc).__name__}: {exc}",
                "",
            ]
        time.sleep(1.0)
    (HERE / "probe5b-readable-excerpt.txt").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print(f"probe5b done -> probe5b-readable-excerpt.txt")


if __name__ == "__main__":
    main()
