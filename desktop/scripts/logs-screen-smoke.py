#!/usr/bin/env python3
"""采集日志屏无头冒烟(10-11;run 瀑布流满高滚动布局验证)。

面板与注入(同 feed-card-smoke.py 骨架):
- 静态服务 ``desktop/ui`` 构建产物(与装机件同一构建链产物,HashRouter);
- Playwright chromium 无头直达 ``#/logs``,视口 1685×1057(主人实机档);
- IPC 注入 ``__TAURI_INTERNALS__.invoke``:version(protocol 13 读态门)/
  run.status(50 轮 DB 历史行夹具:35 成功/10 部分配置/5 失败,对齐实机
  状态分布;history=true + log_run_id 会话号)/ logs.tail(环形缓冲尾巴)。

断言面(run 瀑布流满高滚动布局):50 组行直出;每组行高 ≥ 40px
(min-h-11=44px 档,塌缩回归哨兵);瀑布流容器内容溢出可滚
(scrollHeight > clientHeight);首组自动展开(跟随策略)且日志体在场。
截图落 /tmp 备查。退出码 0 = 冒烟通过。

背景(10-11 报障):瀑布流容器 = flex 列 + overflow-y-auto,子组无
shrink-0 —— 行数超过视口高时 flex 把每行均匀压扁(44px → ~14px),
内容被 overflow-hidden 裁没、滚动条永不出现,实机表现为整屏黑条。
本冒烟即该回归的布局哨兵。

用法(仓库根):``.venv/bin/python desktop/scripts/logs-screen-smoke.py``
"""

from __future__ import annotations

import asyncio
import http.server
import json
import pathlib
import socket
import sys
import threading
import urllib.parse

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
UI_DIR = REPO_ROOT / "desktop" / "ui"
PORT = 4533

MIME = {
    ".html": "text/html",
    ".js": "text/javascript",
    ".css": "text/css",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".json": "application/json",
}

RUN_COUNT = 50

INJECT_SCRIPT = r"""
(() => {
  const iso = (ms) => new Date(ms).toISOString();
  // 50 轮历史行:35 success / 10 partial / 5 failed(对齐 10-11 实机分布)
  const statuses = [
    ...Array(35).fill("success"),
    ...Array(10).fill("partial"),
    ...Array(5).fill("failed"),
  ];
  const categories = ["ai-news", "games-deals", "proxy-watch", "tech-rss", "urlwatch"];
  const runs = statuses.map((status, i) => {
    const started = Date.now() - (i + 1) * 37 * 60_000;
    return {
      run_id: 900 - i,
      yaml: null,
      db: "/home/myssia.db",
      dry: false,
      state: "done",
      exit_code: status === "failed" ? 1 : 0,
      status,
      started_at: iso(started),
      finished_at: iso(started + 52_300),
      duration_ms: 52_300,
      record: {
        run_id: 900 - i,
        category: categories[i % categories.length],
        stats: { items_retained: 20 + (i % 7) },
      },
      history: true,
      log_run_id: 900 - i,
    };
  });
  window.__TAURI_INTERNALS__ = {
    invoke: async (command, args) => {
      if (command !== "sidecar_request") {
        throw new Error("smoke 只应答 sidecar_request,收到: " + command);
      }
      const { method, params } = args ?? {};
      if (method === "version") {
        return { name: "myssia", version: "smoke", protocol: 13, app_version: null };
      }
      if (method === "run.status") {
        return { runs };
      }
      if (method === "logs.tail") {
        const runId = params?.run_id ?? 0;
        const lines = Array.from({ length: 8 }, (_, k) => ({
          seq: k + 1,
          ts: iso(Date.now() - 60_000 + k * 1000),
          run_id: runId,
          stream: k === 6 ? "stderr" : "stdout",
          line: `[run ${runId}] step ${k + 1}: fetch ok, retained ${10 + k} items`,
        }));
        return { lines, total: lines.length, truncated: false };
      }
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
        print(f"FAIL - 构建产物缺位({UI_DIR}/index.html);先 npm --prefix desktop/ui-src run build", file=sys.stderr)
        return 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        port_free = probe.connect_ex(("127.0.0.1", PORT)) != 0
    port = PORT if port_free else PORT + 1
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
            page = await browser.new_page(viewport={"width": 1685, "height": 1057})
            await page.add_init_script(INJECT_SCRIPT)
            await page.goto(f"http://127.0.0.1:{port}/#/logs", wait_until="networkidle")

            await page.wait_for_selector('[data-testid="run-waterfall"]', timeout=10_000)
            await page.wait_for_selector('[data-testid="run-group-h900"]', timeout=10_000)
            expect(
                "50 组历史行直出",
                (await page.locator('[data-testid^="run-group-"]:not([data-testid*="-header-"])').count()) == RUN_COUNT,
            )

            # 布局哨兵:逐组行高(min-h-11 = 44px;塌缩回归 ≈ 14px 一票否决)
            heights = await page.evaluate(
                """() => Array.from(
                    document.querySelectorAll('[data-testid^="run-group-"]:not([data-testid*="-header-"])'),
                    (el) => el.getBoundingClientRect().height,
                )"""
            )
            print(f"metrics - 组行高 min={min(heights):.1f}px max={max(heights):.1f}px n={len(heights)}")
            expect(f"组行高 ≥ 40px(实测 min={min(heights):.1f}px)", min(heights) >= 40)

            # 瀑布流容器:内容溢出必须可滚(压扁回归 = scrollHeight==clientHeight)
            scroll = await page.evaluate(
                """() => {
                    const el = document.querySelector('[data-testid="run-waterfall"]');
                    return { sh: el.scrollHeight, ch: el.clientHeight };
                }"""
            )
            print(f"metrics - waterfall scrollHeight={scroll['sh']} clientHeight={scroll['ch']}")
            expect(
                f"瀑布流内容溢出可滚(scrollHeight {scroll['sh']} > clientHeight {scroll['ch']})",
                scroll["sh"] > scroll["ch"] + 100,
            )

            # 首组跟随策略自动展开,日志体在场(拉取态或行集均可,不许报错面)
            await page.wait_for_selector('[data-testid="run-log-h900"]', timeout=10_000)
            expect("首组自动展开(跟随策略)", True)
            expect(
                "展开体无加载错误",
                (await page.locator('[data-testid="run-log-h900"] .text-dead').count()) == 0,
            )

            await page.screenshot(path="/tmp/myssia-logs-screen-smoke.png", full_page=False)
            print("screenshot: /tmp/myssia-logs-screen-smoke.png")
    except Exception as exc:  # noqa: BLE001 - 冒烟异常如实报
        failures.append(f"异常: {exc}")
        print(f"SMOKE ERROR: {exc}", file=sys.stderr)
    finally:
        if browser is not None:
            await browser.close()
        server.shutdown()

    if failures:
        print(f"冒烟失败 {len(failures)} 项: {json.dumps(failures, ensure_ascii=False)}", file=sys.stderr)
        return 1
    print("采集日志屏无头冒烟:全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
