#!/usr/bin/env python3
"""TG 渠道卡无头冒烟(10-08-tg-channel-card;程序化验证,禁屏控)。

面板与注入(同 tg-card-smoke.py 骨架):
- 静态服务 ``desktop/ui`` 构建产物(与装机件同一构建链产物,HashRouter);
- Playwright chromium 无头直达 ``#/feed`` → L1 下钻「全部条目 · 滚动流」;
- IPC 注入 ``add_init_script`` 定义 ``__TAURI_INTERNALS__.invoke``,按
  ``sidecar_request`` 的 method 应答 version(protocol 10 过服务端读态门)/
  health / store.items(按 category+source 精确等值过滤夹具)/
  store.state.import·mark·mark_all。

断言面(装机无头证据;vitest jsdom 之外的真实 Chromium 一层):
渠道卡区置顶 / 渠道卡三行(频道名去前缀+最新一条预览+条数·未读)/
未读 accent 竖条 / TG 消息卡离场+news 卡照旧 / 时间组头只计列表本体 /
点卡进渠道详情(气泡逐条+news 不混入)→ 面包屑「全部条目」一键回流;
截图落 /tmp 备查。退出码 0 = 冒烟通过。

用法(仓库根):``.venv/bin/python desktop/scripts/feed-card-smoke.py``
"""

from __future__ import annotations

import asyncio
import http.server
import pathlib
import socket
import sys
import threading
import urllib.parse

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
UI_DIR = REPO_ROOT / "desktop" / "ui"
PORT = 4519

MIME = {
    ".html": "text/html",
    ".js": "text/javascript",
    ".css": "text/css",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".json": "application/json",
}

INJECT_SCRIPT = r"""
(() => {
  const now = Date.now();
  const iso = (ms) => new Date(ms).toISOString();
  const items = [
    {
      id: 1, url: "https://t.me/s/mihomo_party/1201", dedup_key: "dk-1",
      title: "🎉 Clash Party Dev Build 开发版本发布",
      source: "telegram-mihomo_party_group",
      content: "基于版本: 1.9.5-d0510.92f21d0 提交哈希: 92f21d0 更新日志: # 1.9.5",
      tags: ["proxy"], category: "tech", scores: null, pushed_at: null, push_slot: null,
      first_seen: iso(now - 10 * 60_000), read: false, starred: false, later: false,
    },
    {
      id: 2, url: "https://t.me/s/mihomo_party/1200", dedup_key: "dk-2",
      title: "🎉 Clash Party Dev Build 1.9.4",
      source: "telegram-mihomo_party_group",
      content: "基于版本: 1.9.4-d0426.9ea9da7",
      tags: ["proxy"], category: "tech", scores: null, pushed_at: null, push_slot: null,
      first_seen: iso(now - 70 * 60_000), read: false, starred: false, later: false,
    },
    {
      id: 3, url: "https://openai.com/blog/x", dedup_key: "dk-3",
      title: "新闻标题丙:OpenAI 发布新模型",
      source: "openai-news",
      content: "摘要内容丙",
      tags: ["ai"], category: "tech", scores: null, pushed_at: null, push_slot: null,
      first_seen: iso(now - 20 * 60_000), read: false, starred: false, later: false,
    },
  ];
  window.__TAURI_INTERNALS__ = {
    invoke: async (command, args) => {
      if (command !== "sidecar_request") {
        throw new Error("smoke 只应答 sidecar_request,收到: " + command);
      }
      const { method, params } = args ?? {};
      if (method === "version") {
        return { name: "myssia", version: "smoke", protocol: 10, app_version: null };
      }
      if (method === "health") {
        return {
          command: "list", plugins_dir: "/home/plugins", db: "/home/myssia.db",
          store_error: null,
          plugins: [{
            file: "/home/plugins/ai-news.yaml", id: "ai-news", name: "AI资讯",
            schedule: null, timezone: null, push_channels: [], loaded: true,
            load_errors: null, sources: [],
          }],
          summary: { plugins: 1, sources: 0, ok: 0, degraded: 0, dead: 0, unknown: 0 },
          healthy: true, first_run: false, exit_code: 0,
        };
      }
      if (method === "store.items") {
        const filtered = items.filter((item) =>
          (!params?.category || item.category === params.category) &&
          (!params?.source || item.source === params.source));
        return { db: "smoke.db", count: filtered.length, items: filtered };
      }
      if (method === "store.state.import") return { imported: 0, skipped: 0 };
      if (method === "store.state.mark") return { updated: params?.keys?.length ?? 0 };
      if (method === "store.state.mark_all") return { updated: 0 };
      return {};
    },
    metadata: {
      currentWindow: { label: "smoke" },
      currentWebview: { label: "smoke" },
    },
    plugins: {},
  };
})();
"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def log_message(self, *args) -> None:  # 静态服务零噪声
        return

    def translate_path(self, path: str) -> str:
        parsed = urllib.parse.urlsplit(path)
        rel = urllib.parse.unquote(parsed.path)
        if rel in ("", "/"):
            rel = "/index.html"
        return super().translate_path(rel)


async def main() -> int:
    if not (UI_DIR / "index.html").exists():
        print(f"FAIL - 构建产物缺位({UI_DIR}/index.html);先 npm run build", file=sys.stderr)
        return 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        port_free = probe.connect_ex(("127.0.0.1", PORT)) != 0
    port = PORT if port_free else 4520
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    from playwright.async_api import async_playwright

    failures: list[str] = []

    def expect(label: str, ok: bool) -> None:
        if ok:
            print(f"ok - {label}")
        else:
            failures.append(label)
            print(f"FAIL - {label}", file=sys.stderr)

    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.add_init_script(INJECT_SCRIPT)
            await page.goto(f"http://127.0.0.1:{port}/#/feed", wait_until="networkidle")
            # L1 挂载 → 下钻「全部条目 · 滚动流」
            await page.wait_for_selector('[data-testid="feed-drill-all"]', timeout=10_000)
            await page.locator('[data-testid="feed-drill-all"]').click()

            # 渠道卡区置顶;渠道卡三行(频道名/最新预览/条数·未读)+ 未读竖条
            await page.wait_for_selector('[data-testid="feed-tg-channels"]', timeout=10_000)
            expect("渠道卡区置顶", True)
            card = page.locator('[data-testid="feed-tg-channel-card-telegram-mihomo_party_group"]')
            expect("渠道卡在场", (await card.count()) == 1)
            text = await card.text_content()
            expect("频道名去前缀", "mihomo_party_group" in (text or ""))
            expect("最新一条预览", "Clash Party Dev Build 开发版本发布" in (text or ""))
            expect("条数计数 2 条", "2 条" in (text or ""))
            expect("未读计数 未读 2", "未读 2" in (text or ""))
            expect(
                "未读 accent 竖条",
                (await page.locator('[data-testid="feed-tg-channel-unread-telegram-mihomo_party_group"]').count()) == 1,
            )
            # TG 消息卡离场,news 卡照旧;无假空态;组头只计列表本体
            expect("TG 消息卡 1 离场", (await page.locator('[data-testid="feed-item-1"]').count()) == 0)
            expect("TG 消息卡 2 离场", (await page.locator('[data-testid="feed-item-2"]').count()) == 0)
            expect("news 卡照旧", (await page.locator('[data-testid="feed-item-3"]').count()) == 1)
            expect("无假空态", (await page.get_by_text("没有未读条目").count()) == 0)
            group = await page.locator('[data-testid="feed-group-今天"]').text_content()
            expect("时间组头只计列表本体 1 条", "1 条" in (group or ""))

            await page.screenshot(path="/tmp/myssia-feed-card-smoke.png", full_page=True)

            # 点卡进渠道详情(气泡逐条),面包屑「全部条目」一键回流
            await card.click()
            await page.wait_for_selector('[data-testid="feed-tg-bubble-1"]', timeout=10_000)
            expect("渠道详情:气泡 1 渲染", True)
            expect("渠道详情:气泡 2 渲染", (await page.locator('[data-testid="feed-tg-bubble-2"]').count()) == 1)
            expect("渠道详情:news 卡不混入", (await page.locator('[data-testid="feed-item-3"]').count()) == 0)
            crumb = page.locator('[data-testid="feed-crumb-all-stream"]')
            expect("面包屑「全部条目」中间层", (await crumb.count()) == 1)
            await crumb.click()
            await page.wait_for_selector(
                '[data-testid="feed-tg-channel-card-telegram-mihomo_party_group"]', timeout=10_000
            )
            expect("一键回流:渠道卡区复现", True)
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-detail.png", full_page=True)
            print("screenshot: /tmp/myssia-feed-card-smoke.png")
    except Exception as exc:  # noqa: BLE001 - 冒烟异常如实报
        failures.append(f"异常: {exc}")
        print(f"SMOKE ERROR: {exc}", file=sys.stderr)
    finally:
        if browser is not None:
            await browser.close()
        server.shutdown()

    if failures:
        print(f"冒烟失败 {len(failures)} 项", file=sys.stderr)
        return 1
    print("TG 渠道卡无头冒烟:全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
