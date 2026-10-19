#!/usr/bin/env python3
"""消息屏无头冒烟·视觉评审取证(10-19-ui-visual-polish;程序化,禁屏控)。

复用 tg-card-smoke.py 套路:静态服务 desktop/ui 构建产物(HashRouter)+
Playwright chromium 无头 + add_init_script 注入 __TAURI_INTERNALS__.invoke
按 sidecar_request 应答(channels.list 四视图/alerts 族/secret.list/health/
bridge.status/wechat_local.probe+sessions)。

与断言型冒烟的差异:本脚本主产物=截图(视觉评审取证),断言只保留
「屏可达 + platform-overview 渲染」两道护栏;截图前 settle 500ms
(remaining-sweep 教训:fade-in 零点透明摄入伪影,两 blocker 教训在册)。

截图落 /tmp/myia-messaging-smoke/:fullpage / viewport 首屏 / 总览区元素。
退出码 0 = 取证完成。

用法(仓库根):``.venv/bin/python desktop/scripts/messaging-screen-smoke.py``
MYIA_SMOKE_UI_DIR 指装机件 Resources/ui 时验的就是装机包像素(判例)。
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
import os as _os

UI_DIR = pathlib.Path(
    _os.environ.get("MYIA_SMOKE_UI_DIR", str(REPO_ROOT / "desktop" / "ui"))
)
PORT = 4519
PLAYWRIGHT_CACHE = pathlib.Path.home() / "Library" / "Caches" / "ms-playwright"
OUT_DIR = pathlib.Path("/tmp/myia-messaging-smoke")

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
  // channels.list 四视图(形状逐字段对照 messaging-screen.test.tsx 夹具;
  // telegram 桶给足 8 条,让通道目录瀑布流形态真实可评)
  const ch = (platform, chatId, name, extra = {}) => ({
    platform, chat_id: chatId, name,
    type: extra.type ?? "group", thread_id: null,
    last_seen: extra.last_seen ?? 1760000000,
  });
  const view = {
    data_root: "/tmp/home",
    updated_at: "2026-10-19T12:00:00",
    platforms: {
      feishu: [
        ch("feishu", "oc_1", "AI中转站合伙人群"),
        ch("feishu", "oc_2", "羊毛反馈群", { type: "dm" }),
      ],
      telegram: [
        ch("telegram", "-1002090123456", "AI 快讯频道"),
        ch("telegram", "-1002080111222", "羊毛线报站"),
        ch("telegram", "-1002070222333", "VPS 交流群"),
        ch("telegram", "-1002060333444", "白嫖研究所"),
        ch("telegram", "12345", "测试私聊", { type: "dm" }),
        ch("telegram", "-1002050444555", "开发内参"),
        ch("telegram", "-1002040555666", "苹果软件园"),
        ch("telegram", "-1002030666777", "好价线报"),
      ],
    },
    aliases: { telegram: { "-1002090123456": "AI 快讯(别名)" } },
    dead: ["feishu:oc_2"],
    rules: [
      {
        file: "/tmp/home/config/messaging-demo.yaml",
        category_id: "messaging-demo",
        category_name: "消息屏夹具",
        parse_ok: true,
        error: null,
        entries: [
          {
            index: 0, channel: "feishu_card", platform: "feishu",
            targets: ["feishu:AI中转站合伙人群"], has_template: false,
            route_count: 1,
            raw: {
              channel: "feishu_card", targets: ["feishu:AI中转站合伙人群"],
              route: [{ when: "category == 'freebie'", mode: "immediate" }],
            },
          },
          {
            index: 1, channel: "stdout", platform: null, targets: [],
            has_template: false, route_count: 0, raw: { channel: "stdout" },
          },
        ],
      },
    ],
  };
  const alertRules = {
    rules: [{
      id: 1, name: "竞对融资", enabled: true, scope: "global",
      when: "'融资' in title", action: "push",
      action_config: { channel: "feishu_card" },
      created_at: "2026-10-04T00:00:00", updated_at: "2026-10-04T00:00:00",
      fired_count: 2, last_fired_at: "2026-10-04T01:23:45",
    }],
  };
  const wechatSessions = {
    sessions: [
      { chat_id: "wx_001", name: "文件传输助手", kind: "dm",
        last_time: 1760950000, last_text: "[图片]" },
      { chat_id: "wx_002", name: "产品交流群", kind: "group",
        last_time: 1760949000, last_text: "今晚发布会看吗" },
      { chat_id: "wx_003", name: "妈妈", kind: "dm",
        last_time: 1760930000, last_text: "周末回家吃饭" },
    ],
  };
  window.__smoke_unknown_methods = [];
  window.__TAURI_INTERNALS__ = {
    invoke: async (command, args) => {
      if (command !== "sidecar_request") {
        throw new Error("smoke 只应答 sidecar_request,收到: " + command);
      }
      const { method } = args ?? {};
      switch (method) {
        case "channels.list": return view;
        case "channels.refresh": {
          const { platform } = args.params ?? {};
          const bucket = view.platforms[platform] ?? [];
          return { platform, merged: bucket.length, entries: bucket };
        }
        case "channels.alias": {
          const { platform, chat_id, name } = args.params ?? {};
          return { platform, chat_id, deleted: name === null, name };
        }
        case "push.write": {
          const { file, push } = args.params ?? {};
          return { file, written: true, changed: true, push };
        }
        case "secret.list":
          return { names: ["myia/telegram/bot-token", "myia/feishu/app-secret"] };
        case "health": return { healthy: true };
        case "alerts.list": return alertRules;
        case "alerts.save": return { ok: true, rules: alertRules.rules };
        case "alerts.delete": return { ok: true };
        case "alerts.test": return { ok: true };
        case "bridge.status":
          return {
            available: true, reason: null, fix_hint: null,
            bin_found: true, weixin_configured: true, gateway_alive: true,
            bin_path: "/Users/smoke/.local/bin/wechat-bridge",
          };
        case "wechat_local.probe":
          return {
            ok: true, state: "ok",
            checks: { binary: "ok", keychain: "ok", db: "ok" },
            wechat_version: "4.1.15", bridge_version: "0.4.3",
            reasons: [],
          };
        case "wechat_local.sessions": return wechatSessions;
        default:
          window.__smoke_unknown_methods.push(String(method));
          return {};
      }
    },
  };
})();
"""


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def log_message(self, *args) -> None:
        return

    def translate_path(self, path: str) -> str:
        parsed = urllib.parse.urlsplit(path)
        rel = urllib.parse.unquote(parsed.path)
        if rel in ("", "/"):
            rel = "/index.html"
        return super().translate_path(rel)


def cached_chromium() -> str | None:
    matches = sorted(PLAYWRIGHT_CACHE.glob(
        "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    ))
    return str(matches[-1]) if matches else None


async def main() -> int:
    if not (UI_DIR / "index.html").exists():
        print(f"FAIL - 构建产物缺位({UI_DIR}/index.html);先 npm run build", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        port_free = probe.connect_ex(("127.0.0.1", PORT)) != 0
    port = PORT if port_free else 4520
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    from playwright.async_api import async_playwright

    browser = None
    try:
        async with async_playwright() as p:
            executable_path = cached_chromium()
            browser = await p.chromium.launch(headless=True, executable_path=executable_path)
            page = await browser.new_page(viewport={"width": 1440, "height": 900})
            await page.add_init_script(INJECT_SCRIPT)
            await page.goto(
                f"http://127.0.0.1:{port}/#/messaging",
                wait_until="networkidle",
            )
            # settle 500ms:fade-in 零点透明摄入伪影教训(remaining-sweep)
            await page.wait_for_timeout(500)
            await page.wait_for_selector('[data-testid="platform-overview"]', timeout=10_000)
            print("ok - 消息屏可达,platform-overview 渲染")

            await page.screenshot(path=str(OUT_DIR / "messaging-fullpage.png"), full_page=True)
            await page.screenshot(path=str(OUT_DIR / "messaging-viewport.png"))
            overview = page.locator('[data-testid="platform-overview"]')
            if await overview.count() == 1:
                await overview.screenshot(path=str(OUT_DIR / "platform-overview.png"))

            unknown = await page.evaluate("window.__smoke_unknown_methods ?? []")
            if unknown:
                print(f"note - 未覆盖方法(fallback 空): {unknown}")
        print(f"done - 截图落 {OUT_DIR}/")
        return 0
    finally:
        if browser is not None:
            await browser.close()
        server.shutdown()


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
