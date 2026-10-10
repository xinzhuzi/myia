#!/usr/bin/env python3
"""情报流三级界面无头冒烟(v8,10-10;程序化验证,禁屏控)。

面板与注入(同 tg-card-smoke.py 骨架):
- 静态服务 ``desktop/ui`` 构建产物(与装机件同一构建链产物,HashRouter);
- Playwright chromium 无头直达 ``#/feed``(v8:**三级界面** —— 1 级 = 渠道
  类型卡瀑布流(竖版卡,只有卡片+搜索)→ 2 级 = 该类型全渠道列表 → 3 级 =
  该渠道详情(TG 含监控台;消息时间线/条目;条目点击 = 详情弹窗),
  主人定调「三级界面」,design-v8.md 照稿;Esc/返回钮 3→2→1 逐级回退);
- IPC 注入 ``add_init_script`` 定义 ``__TAURI_INTERNALS__.invoke``,按
  ``sidecar_request`` 的 method 应答 version(protocol 13 过服务端读态 + 计
  数口径门;stats 门 14 未过 = catalog 口径,零 source_stats 试错)/ health
  (telegram + tech 插件,携 sources 词表:tg_web/static_html/prompt 三引擎)/
  store.items(按 source 精确等值过滤夹具,with_total 回带)/ telegram.status
  (已登录)/ store.state.import·mark·mark_all。

断言面(装机无头证据;vitest jsdom 之外的真实 Chromium 一层;v8 三级信息
架构):1 级三类型卡直出(词表序,竖版 min-h)→ 搜「Tg」TG 卡独显 → 点 TG
卡 = 2 级行列(mihomo 行在场,openai/daily 不混;脚注渠道数)→ 点行 =
3 级聊天时间线(日期胶囊 + 气泡)+ 监控台常驻条 + feed-stream-count → 裸
j + Enter = 条目详情弹窗(Esc 关;三层单环,Shift 层退役)→ 返回钮/Esc
逐级回退 3→2→1;退役 testid 零命中清单随 v7 先例更新。截图落 /tmp 备查。
退出码 0 = 冒烟通过。

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
      first_seen: iso(now - 20 * 60_000), read: false, starred: false, later: false,
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
        // protocol 13 = 过读态/计数门;stats 门(14)未过 = 1 级类型卡走
        // catalog 已加载口径 + title 如实(不发 store.source_stats 试错)
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
              load_errors: null,
              sources: [
                { name: "telegram-mihomo_party_group", url: "https://t.me/s/mihomo_party",
                  engine: "tg_web", engine_hint: null,
                  health: { state: "unknown", reason: "无观测", observed: 0, latest: null, baseline: null },
                  fingerprint_skips: { observed: 0, skipped: 0 } },
              ],
            },
            {
              file: "/home/plugins/tech.yaml", id: "tech", name: "科技",
              schedule: null, timezone: null, push_channels: [], loaded: true,
              load_errors: null,
              sources: [
                { name: "openai-news", url: "https://openai.com/blog",
                  engine: "static_html", engine_hint: null,
                  health: { state: "unknown", reason: "无观测", observed: 0, latest: null, baseline: null },
                  fingerprint_skips: { observed: 0, skipped: 0 } },
                { name: "daily-digest", url: "https://example.com/daily",
                  engine: "prompt", engine_hint: null,
                  health: { state: "unknown", reason: "无观测", observed: 0, latest: null, baseline: null },
                  fingerprint_skips: { observed: 0, skipped: 0 } },
              ],
            },
          ],
          summary: { plugins: 2, sources: 3, ok: 0, degraded: 0, dead: 0, unknown: 0 },
          healthy: true, first_run: false, exit_code: 0,
        };
      }
      if (method === "store.items") {
        const filtered = items.filter((item) => {
          if (params?.category && item.category !== params.category) return false;
          if (params?.source && item.source !== params.source) return false;
          if (params?.query) {
            const hay = `${item.title} ${item.content ?? ""} ${item.source ?? ""}`;
            if (!hay.toLowerCase().includes(String(params.query).toLowerCase())) return false;
          }
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
              { account: "telegram-alt1", logged_in: true, logged_in_at: "2026-10-10T01:00:00+00:00", login_in_progress: false, login_note: null },
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

            # ═══ 1 级 = 类型卡瀑布流(v8 AC29:只有卡片+搜索)═══
            await page.wait_for_selector('[data-testid="feed-types-wall"]', timeout=10_000)
            expect("类型卡墙容器在场", True)
            tg_card = page.locator('[data-testid="feed-type-card-tg"]')
            site_card = page.locator('[data-testid="feed-type-card-site"]')
            daily_card = page.locator('[data-testid="feed-type-card-daily"]')
            expect("TG 类型卡直出(tg_web → tg)", (await tg_card.get_attribute("data-channels")) == "1")
            expect("网站类型卡直出(static_html → site)", (await site_card.get_attribute("data-channels")) == "1")
            expect("日报类型卡直出(prompt → daily,零条目也出卡)", (await daily_card.get_attribute("data-channels")) == "1")
            expect(
                "竖版卡 min-h(卡片高度 > 宽度,主人钉死)",
                "min-h-[340px]" in ((await tg_card.get_attribute("class")) or ""),
            )
            expect(
                "卡内计数词面(今日/未读,catalog 口径)",
                "今日 2 条" in ((await tg_card.text_content()) or "")
                and "未读 2" in ((await tg_card.text_content()) or ""),
            )
            expect(
                "卡内最新预览带渠道名",
                "mihomo_party_group" in ((await tg_card.text_content()) or ""),
            )
            expect("1 级无搜索类型框外杂项(feed-channel-list 不在此级)",
                   (await page.locator('[data-testid="feed-channel-list"]').count()) == 0)
            expect("1 级类型搜索框在场", (await page.get_by_label("搜索类型").count()) == 1)
            # 旧信息架构面随三级化撤销
            for gone in ("feed-chips", "feed-kind-wall", "feed-drill-all", "feed-tg-channels",
                         "feed-breadcrumb", "feed-channel-wall", "feed-waterfall", "feed-back-to-wall",
                         "feed-overview", "feed-overview-stats", "feed-back-to-overview", "feed-search-scope"):
                expect(f"旧面退场:{gone}", (await page.locator(f'[data-testid="{gone}"]').count()) == 0)
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-l1.png", full_page=True)
            print("screenshot: /tmp/myssia-feed-card-smoke-l1.png")

            # ═══ 1 级搜索「Tg」:TG 类型卡独显(别名前缀命中)═══
            type_search = page.get_by_label("搜索类型")
            await type_search.fill("Tg")
            await page.wait_for_selector('[data-testid="feed-type-card-tg"]', timeout=10_000)
            expect("搜 Tg:TG 类型卡独显", (await site_card.count()) == 0 and (await daily_card.count()) == 0)
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-l1-search.png", full_page=True)
            await type_search.press("Escape")
            await page.wait_for_selector('[data-testid="feed-type-card-site"]', timeout=10_000)
            expect("清空搜索恢复全量", True)

            # ═══ 点 TG 卡 = 2 级该类型全渠道列表(v8 AC30)═══
            await tg_card.click()
            await page.wait_for_selector('[data-testid="feed-channel-list"]', timeout=10_000)
            expect("2 级行列表容器在场", True)
            tg_row = page.locator('[data-testid="feed-channel-row-telegram-mihomo_party_group"]')
            await tg_row.wait_for(timeout=10_000)
            expect("mihomo 行在场(engine tg_web → 类型 tg)",
                   (await tg_row.get_attribute("data-channel-kind")) == "tg")
            expect(
                "类型词面(返回钮旁)",
                "TG" in ((await page.locator('[data-testid="feed-type-title"]').text_content()) or ""),
            )
            expect(
                "脚注词面 = 渠道数(feed-count 随迁 2 级)",
                "1 个渠道" in ((await page.locator('[data-testid="feed-count"]').text_content()) or ""),
            )
            expect(
                "openai/daily 行不混(2 级作用域 = 该类型成员集)",
                (await page.locator('[data-testid="feed-channel-row-openai-news"]').count()) == 0
                and (await page.locator('[data-testid="feed-channel-row-daily-digest"]').count()) == 0,
            )
            expect(
                "行内未读徽标(未读 >0)",
                (await tg_row.get_attribute("data-unread")) == "true",
            )
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-l2.png", full_page=True)
            print("screenshot: /tmp/myssia-feed-card-smoke-l2.png")

            # ═══ 点行 = 3 级渠道详情(TG:监控台 + 聊天时间线)═══
            await tg_row.click()
            console_card = page.locator('[data-testid="feed-tg-console"]')
            await console_card.wait_for(timeout=10_000)
            expect("监控台常驻条(3 级专属,工具条下)", (await console_card.count()) == 1)
            expect(
                "监控台显监控中",
                "监控中" in ((await page.locator('[data-testid="feed-tg-console-live"]').text_content()) or ""),
            )
            await page.wait_for_selector('[data-testid="feed-chat-timeline"]', timeout=10_000)
            expect("TG 3 级 = 聊天时间线", True)
            expect(
                "日期胶囊在场",
                (await page.locator('[data-testid="feed-group-今天"]').count()) == 1,
            )
            expect(
                "聊天视图气泡 1",
                (await page.locator('[data-testid="feed-tg-bubble-1"]').count()) == 1,
            )
            expect("网页条目不混入", (await page.locator('[data-testid="feed-item-3"]').count()) == 0)
            expect(
                "作用域词 = 渠道名",
                "mihomo_party_group" in ((await page.locator('[data-testid="feed-stream-title"]').text_content()) or ""),
            )
            expect(
                "3 级条目计数(feed-stream-count)",
                (await page.locator('[data-testid="feed-stream-count"]').count()) == 1,
            )
            expect(
                "渠道内检索框在场(§4.3)",
                (await page.get_by_label("渠道内检索").count()) == 1,
            )
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-l3.png", full_page=True)

            # ═══ 裸 j + Enter = 条目详情弹窗;Esc 关(v8 三层单环,Shift 层退役)═══
            # 点击行后焦点在行根(DIV),键盘守卫放行;真浏览器标题钮居中点击会被
            # 右上悬停操作簇截走,键盘动线最稳。
            await page.keyboard.press("j")
            await page.wait_for_function(
                "document.querySelector('[data-testid=\"feed-item-1\"]')?.getAttribute('data-nav-focused') === 'true'",
                timeout=10_000,
            )
            expect("裸 j 落首条目(3 级条目环亮)", True)
            await page.keyboard.press("Enter")
            await page.wait_for_selector('[data-testid="feed-detail-dialog"]', timeout=10_000)
            expect(
                "详情弹窗标题(TG 消息)",
                "Clash Party" in ((await page.locator('[data-testid="feed-detail-title"]').text_content()) or ""),
            )
            # Esc 走 dialog 元素本尊(locator.press 先聚焦再派发):dialog 基件的
            # 关闭线挂 overlay onKeyDown(事件冒泡),初始聚焦是 rAF 异步落——
            # 若打给 body 级 keyboard.press,无头下 rAF 节流时事件路径不过
            # overlay,弹窗永不关(深测实锤的竞态)。
            await page.get_by_role("dialog").press("Escape")
            await page.wait_for_selector('[data-testid="feed-detail-dialog"]', state="detached", timeout=10_000)
            expect("Esc 关详情弹窗(层级保持)", True)
            expect(
                "弹窗 Esc 只关弹窗(3 级仍在场)",
                (await page.locator('[data-testid="feed-chat-timeline"]').count()) == 1,
            )

            # ═══ Esc 回退链:3→2→1(v8 §7,返回链完整)═══
            await page.keyboard.press("Escape")
            await page.wait_for_selector('[data-testid="feed-channel-list"]', timeout=10_000)
            expect("Esc 3→2(渠道行列表回归)", True)
            await page.keyboard.press("Escape")
            await page.wait_for_selector('[data-testid="feed-types-wall"]', timeout=10_000)
            expect("Esc 2→1(类型卡墙回归)", True)
            await page.keyboard.press("Escape")
            expect("Esc 1 级 no-op(卡墙仍在)", (await page.locator('[data-testid="feed-types-wall"]').count()) == 1)

            # ═══ 返回钮动线复验:1→2→3→返回→返回 ═══
            await site_card.click()
            await page.wait_for_selector('[data-testid="feed-channel-row-openai-news"]', timeout=10_000)
            await page.locator('[data-testid="feed-channel-row-openai-news"]').click()
            await page.wait_for_selector('[data-testid="feed-stream-list"]', timeout=10_000)
            expect("网站 3 级 = 条目单列(feed-stream-list)", True)
            expect(
                "监控台条退场(非 TG 渠道)",
                (await page.locator('[data-testid="feed-tg-console"]').count()) == 0,
            )
            expect(
                "网站条目在场(条目 3)",
                (await page.locator('[data-testid="feed-item-3"]').count()) == 1,
            )
            expect(
                "TG 气泡不混入",
                (await page.locator('[data-testid="feed-tg-bubble-1"]').count()) == 0,
            )
            await page.screenshot(path="/tmp/myssia-feed-card-smoke-site.png", full_page=True)
            await page.locator('[data-testid="feed-back-to-channels"]').click()
            await page.wait_for_selector('[data-testid="feed-channel-list"]', timeout=10_000)
            expect("返回钮 3→2(行高亮退场 = 本级无持久选中)",
                   (await page.locator('[data-testid="feed-channel-row-openai-news"]').get_attribute("data-selected")) == "false")
            await page.locator('[data-testid="feed-back-to-types"]').click()
            await page.wait_for_selector('[data-testid="feed-types-wall"]', timeout=10_000)
            expect("返回钮 2→1(类型卡墙回归)", True)

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
    print("情报流三级界面无头冒烟:全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
