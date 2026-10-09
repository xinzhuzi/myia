#!/usr/bin/env python3
"""TG 渠道卡无头冒烟(10-08-tg-channel-card;程序化验证,禁屏控)。

面板与注入(同 tg-card-smoke.py 骨架):
- 静态服务 ``desktop/ui`` 构建产物(与装机件同一构建链产物,HashRouter);
- Playwright chromium 无头直达 ``#/feed``(v5:落地即瀑布流首屏,无导航中转);
- IPC 注入 ``add_init_script`` 定义 ``__TAURI_INTERNALS__.invoke``,按
  ``sidecar_request`` 的 method 应答 version(protocol 13 过服务端读态 + 计数
  口径门)/ health(telegram + tech 双品类)/ store.items(按 category+source
  精确等值过滤夹具,with_total 回带)/ telegram.status(已登录)/
  store.state.import·mark·mark_all。

断言面(装机无头证据;vitest jsdom 之外的真实 Chromium 一层;v5 瀑布流
信息架构):首屏 = 瀑布流卡片墙(内容卡直出,TG = 聊天气泡卡;旧导航面
feed-drill-*/feed-kind-wall/feed-tg-channels/面包屑退场)/ 筛选 chips(全部 +
telegram + tech,零计数不出;渠道 chips 选定品类后出现)/ TG 品类激活 =
监控台钉墙顶 + TG 频道 chip = 聊天视图(日期胶囊 + 气泡)/ 全部渠道/tech
品类/渠道 chips 作用域切换 / 搜索框改 query 结果即瀑布流 / 点击卡片 = 详情
弹窗(Esc 关);截图落 /tmp 备查。退出码 0 = 冒烟通过。

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
      tags: ["proxy"], category: "telegram", scores: null, pushed_at: null, push_slot: null,
      first_seen: iso(now - 10 * 60_000), read: false, starred: false, later: false,
    },
    {
      id: 2, url: "https://t.me/s/mihomo_party/1200", dedup_key: "dk-2",
      title: "🎉 Clash Party Dev Build 1.9.4",
      source: "telegram-mihomo_party_group",
      content: "基于版本: 1.9.4-d0426.9ea9da7",
      tags: ["proxy"], category: "telegram", scores: null, pushed_at: null, push_slot: null,
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
        return { name: "myssia", version: "smoke", protocol: 13, app_version: null };
      }
      if (method === "health") {
        return {
          command: "list", plugins_dir: "/home/plugins", db: "/home/myssia.db",
          store_error: null,
          plugins: [
            {
              file: "/home/plugins/telegram.yaml", id: "telegram", name: "Telegram 监控",
              schedule: null, timezone: null, push_channels: [], loaded: true,
              load_errors: null, sources: [],
            },
            {
              file: "/home/plugins/tech.yaml", id: "tech", name: "科技",
              schedule: null, timezone: null, push_channels: [], loaded: true,
              load_errors: null, sources: [],
            },
          ],
          summary: { plugins: 2, sources: 0, ok: 0, degraded: 0, dead: 0, unknown: 0 },
          healthy: true, first_run: false, exit_code: 0,
        };
      }
      if (method === "store.items") {
        const filtered = items.filter((item) => {
          if (params?.category && item.category !== params.category) return false;
          if (params?.source && item.source !== params.source) return false;
          return true;
        });
        // v13 同门:with_total 请求回带同 WHERE 全量计数
        return {
          db: "smoke.db", count: filtered.length, items: filtered,
          ...(params?.with_total ? { total: filtered.length } : {}),
        };
      }
      if (method === "telegram.status") {
        return {
          bot: { configured: false, error: null },
          session: { exists: false },
          web: {
            accounts: [
              { account: "telegram-alt1", logged_in: true, logged_in_at: "2026-10-09T01:00:00+00:00", login_in_progress: false, login_note: null },
            ],
          },
        };
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

            # ═══ 首屏 = 瀑布流卡片墙(v5 AC13:落地即内容卡,无导航中转)═══
            await page.wait_for_selector('[data-testid="feed-waterfall"]', timeout=10_000)
            expect("瀑布流容器在场", True)
            expect(
                "瀑布流多列 class(columns-1 起档)",
                "columns-1" in (await page.locator('[data-testid="feed-waterfall"]').get_attribute("class") or ""),
            )
            news_card = page.locator('[data-testid="feed-item-3"]')
            expect("网页新闻卡直出", (await news_card.count()) == 1)
            expect("新闻卡 data-kind=news", (await news_card.get_attribute("data-kind")) == "news")
            expect(
                "TG 气泡卡直出(数据 id=1)",
                (await page.locator('[data-testid="feed-tg-bubble-1"]').count()) == 1,
            )
            # 旧信息架构面随 AC17 撤销
            for gone in ("feed-kind-wall", "feed-drill-all", "feed-tg-channels", "feed-breadcrumb", "feed-l1", "feed-l2"):
                expect(f"旧面退场:{gone}", (await page.locator(f'[data-testid="{gone}"]').count()) == 0)

            # ═══ 筛选 chips 替代导航(AC15):全部 + telegram + tech ═══
            await page.wait_for_selector('[data-testid="feed-chip-cat-telegram"]', timeout=10_000)
            expect("品类 chip:全部", (await page.locator('[data-testid="feed-chip-cat-all"]').count()) == 1)
            tg_chip = page.locator('[data-testid="feed-chip-cat-telegram"]')
            expect("TG chip 计数 2", "2" in ((await tg_chip.text_content()) or ""))
            expect("tech chip 在场", (await page.locator('[data-testid="feed-chip-cat-tech"]').count()) == 1)
            # 未选品类:渠道 chips 不出现
            expect("渠道 chips 未选品类不出", (await page.locator('[data-testid="feed-chip-src-all"]').count()) == 0)

            # ═══ TG 品类激活:监控台钉墙顶 + 渠道 chip 进聊天视图(AC16)═══
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-wall.png", full_page=True)
            print("screenshot: /tmp/myssia-feed-card-smoke-wall.png")
            await tg_chip.click()
            console_card = page.locator('[data-testid="feed-tg-console"]')
            await console_card.wait_for(timeout=10_000)
            expect("监控台钉墙顶", (await console_card.count()) == 1)
            expect(
                "监控台显监控中",
                "监控中" in ((await page.locator('[data-testid="feed-tg-console-live"]').text_content()) or ""),
            )
            src_chip = page.locator('[data-testid="feed-chip-src-telegram-mihomo_party_group"]')
            await src_chip.wait_for(timeout=10_000)
            await src_chip.click()
            await page.wait_for_selector('[data-testid="feed-chat-timeline"]', timeout=10_000)
            expect("TG 频道 chip = 聊天视图", True)
            expect(
                "日期胶囊在场",
                (await page.locator('[data-testid="feed-group-今天"]').count()) == 1,
            )
            expect(
                "聊天视图气泡 1",
                (await page.locator('[data-testid="feed-tg-bubble-1"]').count()) == 1,
            )
            expect("网页条目不混入", (await page.locator('[data-testid="feed-item-3"]').count()) == 0)
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-chat.png", full_page=True)

            # ═══ 全部渠道 chip 回品类瀑布流;tech 品类 + 渠道 chips ═══
            await page.locator('[data-testid="feed-chip-src-all"]').click()
            await page.wait_for_selector('[data-testid="feed-item-1"]', timeout=10_000)
            expect("全部渠道回品类瀑布流", True)
            await page.locator('[data-testid="feed-chip-cat-tech"]').click()
            news_in_scope = page.locator('[data-testid="feed-item-3"]')
            await news_in_scope.wait_for(timeout=10_000)
            expect("tech 品类作用域:新闻卡在", (await news_in_scope.count()) == 1)
            expect("TG 气泡不混入", (await page.locator('[data-testid="feed-tg-bubble-1"]').count()) == 0)
            await page.locator('[data-testid="feed-chip-src-openai-news"]').wait_for(timeout=10_000)
            expect("tech 渠道 chip 在场", True)

            # ═══ 搜索(AC14):首屏搜索框即改 query,结果即瀑布流 ═══
            await page.get_by_label("搜索条目").fill("OpenAI")
            await page.get_by_label("搜索条目").press("Enter")
            await page.wait_for_selector('[data-testid="feed-search-scope"]', timeout=10_000)
            expect("搜索作用域词在", True)
            # 计数词面随动(F2):tech 作用域首页取尽(total=同 WHERE 行数)
            # →「1 / 1 条」全量词面;截断时升「已加载 X · 共 T 条」
            await page.wait_for_selector('[data-testid="feed-count"]', timeout=10_000)
            count_text = (await page.locator('[data-testid="feed-count"]').text_content()) or ""
            expect("F2 计数词面随动(1 / 1 条)", "1 / 1 条" in count_text)
            await page.get_by_label("搜索条目").press("Escape")
            await page.wait_for_selector('[data-testid="feed-item-3"]', timeout=10_000)
            expect("清空搜索恢复", True)

            # ═══ 点击卡片 = 详情弹窗(AC13;弹开即记已读)═══
            # 走键盘动线(j 巡游落首卡 + Enter 开详情;与点击同门)—— 真实
            # 浏览器里标题钮居中点击会被右上悬停操作簇(opacity-0 仍拦截指针)
            # 截走;先 blur 搜索框(Esc 清空后焦点仍在框内,j/Enter 守卫会让位)
            await page.get_by_label("搜索条目").blur()
            await page.keyboard.press("j")
            await page.keyboard.press("Enter")
            await page.wait_for_selector('[data-testid="feed-detail-dialog"]', timeout=10_000)
            expect(
                "详情弹窗标题",
                "OpenAI" in ((await page.locator('[data-testid="feed-detail-title"]').text_content()) or ""),
            )
            # Esc 走 dialog 元素本尊(locator.press 先聚焦再派发):dialog 基件的
            # 关闭线挂 overlay onKeyDown(事件冒泡),初始聚焦是 rAF 异步落——
            # 若打给 body 级 keyboard.press,无头下 rAF 节流时事件路径不过
            # overlay,弹窗永不关(深测实锤的竞态)。与 vitest closeDetailDialog
            # 对 dialog 元素直接 keyDown 同一契约。
            await page.get_by_role("dialog").press("Escape")
            await page.wait_for_selector('[data-testid="feed-detail-dialog"]', state="detached", timeout=10_000)
            expect("Esc 关详情弹窗", True)

            await page.screenshot(path="/tmp/myssia-feed-card-smoke.png", full_page=True)
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
