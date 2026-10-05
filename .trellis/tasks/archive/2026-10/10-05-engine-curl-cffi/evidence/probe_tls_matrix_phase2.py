#!/usr/bin/env python
"""TLS 归因矩阵第二轮(10-05-engine-curl-cffi Q1):首轮 5 站未现 TLS 归因
形态,补两座文献在案的 TLS 指纹墙站(Amazon 503-captcha 墙 / Zillow CF 墙)。

robots:Amazon * 组放行首页(02d 记档);Zillow 明文 Allow /homes/for_sale/
(02d 记档)。纪律同首轮:每 URL 每路单次,20s 超时,失败不重试,1s 间隔。
B 路 UA = 首轮 echo 回读的 chrome150 UA(03-tls-matrix-run.log Phase 0),
与 C 路实发 UA 逐字节一致。

用法:/tmp/curl-eval/bin/python probe_tls_matrix_phase2.py 2>&1 | tee 04-tls-matrix-phase2.log
"""

from __future__ import annotations

import importlib.util
import json
import time
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "probe_tls_matrix", Path(__file__).with_name("probe_tls_matrix.py"))
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)

CHROME_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36")

TARGETS = [
    ("amazon-home", "https://www.amazon.com/",
     "TLS 指纹墙经典例(python TLS 常 503 captcha;robots * 放行首页)"),
    ("zillow-homes", "https://www.zillow.com/homes/for_sale/",
     "Cloudflare 硬墙站(robots * 明文 Allow 该路径)"),
]


def main() -> int:
    results = {}
    for tag, url, note in TARGETS:
        print(f"== {tag}: {url}  ({note}) ==")
        row_a = mod.probe_httpx(url, mod.MYIA_UA)
        print(f"  A(httpx+MYIA UA): {row_a}")
        time.sleep(1)
        row_b = mod.probe_httpx(url, CHROME_UA)
        print(f"  B(httpx+Chrome UA): {row_b}")
        time.sleep(1)
        row_c = mod.probe_curlcffi(url)
        print(f"  C(curl_cffi chrome): {row_c}")
        results[tag] = {"url": url, "note": note, "A": row_a, "B": row_b, "C": row_c}
    print("\n== JSON ==")
    print(json.dumps(results, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
