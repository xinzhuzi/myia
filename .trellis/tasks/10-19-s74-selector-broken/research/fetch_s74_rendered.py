"""s74 云渲染 DOM 抓取(侦察脚本,2026-10-19)。

凭据经 MYIA 钥匙串通道解析(myssia.secrets.get_secret;失败回落 security CLI
子进程),密钥值只存在于进程内存,不打印、不落盘。请求体与
src/myssia/engines/firecrawl.py:_scrape 同构(formats=[markdown,html])。
只输出安全信息:HTTP 状态、负载字节数、页面 metadata。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import httpx

OUT_DIR = Path(__file__).resolve().parent
TARGET = "https://tkkgv8.gicp.fun/"
STAMP = "2026-10-19"


def _read_secret(name: str) -> str:
    try:
        from myssia.secrets import get_secret

        value = get_secret(name)
        if value:
            return value
    except Exception as exc:  # noqa: BLE001 —— 回落 security CLI
        print(f"keyring 通道失败({type(exc).__name__}),回落 security CLI", file=sys.stderr)
    proc = subprocess.run(
        ["security", "find-generic-password", "-s", "myia", "-a", name, "-w"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise SystemExit(f"secret 读取失败 name={name} rc={proc.returncode}")
    return proc.stdout.strip()


def main() -> int:
    endpoint = _read_secret("myia/firecrawl/url").rstrip("/")
    api_key = _read_secret("myia/firecrawl/api-key")

    resp = httpx.post(
        endpoint + "/v1/scrape",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        json={"url": TARGET, "formats": ["markdown", "html"], "timeout": 60000},
        timeout=90.0,
    )
    print("http_status:", resp.status_code)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("success") is False:
        print("firecrawl_error:", payload.get("error"))
        return 2
    data = payload.get("data") or {}
    html = data.get("html") or ""
    markdown = data.get("markdown") or ""
    meta = data.get("metadata") or {}

    (OUT_DIR / f"s74-rendered-{STAMP}.html").write_text(html, encoding="utf-8")
    (OUT_DIR / f"s74-rendered-{STAMP}.md").write_text(markdown, encoding="utf-8")
    (OUT_DIR / f"s74-rendered-{STAMP}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("html_bytes:", len(html.encode("utf-8")))
    print("markdown_bytes:", len(markdown.encode("utf-8")))
    print("page_title:", meta.get("title"))
    print("page_url:", meta.get("sourceURL") or meta.get("url") or TARGET)
    print("saved_to:", OUT_DIR / f"s74-rendered-{STAMP}.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
