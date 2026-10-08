#!/usr/bin/env python3
"""浏览器模块页无头冒烟(10-08-browser-module 案甲;程序化验证,禁屏控零弹窗).

面板与注入(判例 = tg-card-smoke.py):
- 静态服务 ``desktop/ui`` 构建产物(``npm run build``,HashRouter 免服务端);
- Playwright chromium 无头(浏览器二进制 = playwright 缺省缓存,与
  crawl4ai 组件轨同源;CLI 直跑仓 ``.venv``)—— 冒烟全程无头,零真实壳
  零真实网络零屏控(禁屏控令豁免面 = 用户点击触发的登录窗,不在冒烟面);
- IPC 注入:``add_init_script`` 定义 ``__TAURI_INTERNALS__.invoke``,按
  ``sidecar_request`` 的 method 应答 browser.* 四方法夹具。

断言面(PRD AC4:模块独立分区 + 操作列表/窗口管理,全程序化):
设置树「浏览器」一级分区在册 / 模块页渲染 / 操作台账三态行(登录中·
完成·失败)/ 失败行人话错误+修复指引+重试 / 聚焦·关闭窗口管理动作链 /
日志尾巴可见;截图落 /tmp 备查。退出码 0 = 冒烟通过。

用法(仓库根):``.venv/bin/python desktop/scripts/browser-module-smoke.py``
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
  const now = "2026-10-08T06:00:00+00:00";
  const ops = {
    "telegram-alt1": {
      op_id: "telegram-alt1",
      kind: "tg_web_login",
      session_key: "telegram-alt1",
      url: "https://web.telegram.org",
      phase: "done",
      note: "登录完成(登录态已落配置档,0700/0600)",
      fix_hint: null,
      started_at: now,
      finished_at: now,
      log_tail: [now + " 操作登记:tg_web_login 会话 telegram-alt1(force=false)",
                 now + " 登录窗口已打开(账号 telegram-alt1)。"],
    },
    "telegram-alt2": {
      op_id: "telegram-alt2",
      kind: "tg_web_login",
      session_key: "telegram-alt2",
      url: "https://web.telegram.org",
      phase: "failed",
      note: "浏览器二进制缺失(Chromium 未下载):Executable doesn't exist at …",
      fix_hint: "设置 →「Python 环境」→ 安装「JS 渲染抓取(crawl4ai)」组件(含 Chromium 下载)",
      started_at: now,
      finished_at: now,
      log_tail: [now + " 操作登记:tg_web_login 会话 telegram-alt2(force=false)"],
    },
    "telegram-alt3": {
      op_id: "telegram-alt3",
      kind: "tg_web_login",
      session_key: "telegram-alt3",
      url: "https://web.telegram.org",
      phase: "running",
      note: "登录窗拉起中(浏览器窗口即将弹出)",
      fix_hint: null,
      started_at: now,
      finished_at: null,
      log_tail: [now + " 操作登记:tg_web_login 会话 telegram-alt3(force=false)"],
    },
  };
  const calls = { open: [], focus: [], close: [] };
  window.__myiaBrowserSmokeCalls = calls;
  const ledger = () => ({
    operations: Object.values(ops).sort((a, b) => (a.started_at < b.started_at ? 1 : -1)),
    kinds: { tg_web_login: "TG 网页线登录(web.telegram.org;复用 web_line 登录器)" },
  });
  window.__TAURI_INTERNALS__ = {
    invoke: async (command, args) => {
      if (command !== "sidecar_request") {
        throw new Error("smoke 只应答 sidecar_request,收到: " + command);
      }
      const { method, params } = args ?? {};
      if (method === "browser.list") return ledger();
      if (method === "browser.open") {
        calls.open.push(params);
        const key = String(params?.session_key ?? "");
        ops[key] = {
          ...(ops[key] ?? {}),
          op_id: key,
          kind: String(params?.kind ?? "tg_web_login"),
          session_key: key,
          url: "https://web.telegram.org",
          phase: "running",
          note: "登录窗拉起中(浏览器窗口即将弹出)",
          fix_hint: null,
          started_at: now,
          finished_at: null,
          log_tail: (ops[key]?.log_tail ?? []).concat([now + " 重试拉起(force=" + (params?.force ?? false) + ")"]),
        };
        return { started: true, op_id: key, kind: params?.kind };
      }
      if (method === "browser.focus") {
        calls.focus.push(params);
        return { focused: true, op_id: params?.op_id };
      }
      if (method === "browser.close") {
        calls.close.push(params);
        const key = String(params?.op_id ?? "");
        if (ops[key]) ops[key] = { ...ops[key], phase: "closed", note: "窗口已关闭:用户关闭" };
        return { closed: true, op_id: key, note: "已请求关闭" };
      }
      if (method === "version") return { version: "smoke" };
      if (method === "health") return { ok: true };
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
            await page.goto(
                f"http://127.0.0.1:{port}/#/settings?section=browser",
                wait_until="networkidle",
            )
            # 分区在册:设置树「浏览器」一级分区导航 + 模块页挂载
            await page.wait_for_selector(
                '[data-testid="settings-nav-browser"]', timeout=10_000
            )
            expect("设置树「浏览器」一级分区在册", True)
            await page.wait_for_selector(
                '[data-testid="browser-module-card"]', timeout=10_000
            )
            expect("模块页渲染(浏览器分区)", True)
            expect(
                "单入口文案在卡面",
                await page.get_by_text("统一入口与台账").count() >= 1,
            )
            # 操作台账三态行
            expect(
                "完成态行 + 徽标",
                (await page.locator('[data-testid="browser-op-telegram-alt1-phase"]').count() == 1)
                and ("完成" in (await page.locator('[data-testid="browser-op-telegram-alt1-phase"]').inner_text())),
            )
            expect(
                "登录中行:聚焦/关闭按钮在",
                (await page.locator('[data-testid="browser-op-telegram-alt3-focus"]').count() == 1)
                and (await page.locator('[data-testid="browser-op-telegram-alt3-close"]').count() == 1),
            )
            failed_note = await page.locator(
                '[data-testid="browser-op-telegram-alt2-note"]'
            ).inner_text()
            expect(
                "失败行:人话错误上浮",
                "浏览器二进制缺失" in failed_note,
            )
            expect(
                "失败行:修复指引可见",
                await page.locator('[data-testid="browser-op-telegram-alt2-fix"]').count() == 1,
            )
            expect(
                "失败行:重试按钮在",
                await page.locator('[data-testid="browser-op-telegram-alt2-retry"]').count() == 1,
            )
            expect(
                "日志尾巴可见(完成行)",
                await page.locator('[data-testid="browser-op-telegram-alt1-log"]').count() == 1,
            )
            # 窗口管理动作链:进行中行 → 关闭 → 台账转「已关闭」
            await page.locator('[data-testid="browser-op-telegram-alt3-close"]').click()
            await page.wait_for_function(
                """() => document.querySelector(
                    '[data-testid="browser-op-telegram-alt3-phase"]'
                )?.textContent?.includes('已关闭')""",
                timeout=5_000,
            )
            expect("关闭动作链:台账行转「已关闭」", True)
            # 重试动作链:失败行 → 重试(force)→ 行转「登录中」
            await page.locator('[data-testid="browser-op-telegram-alt2-retry"]').click()
            await page.wait_for_function(
                """() => document.querySelector(
                    '[data-testid="browser-op-telegram-alt2-phase"]'
                )?.textContent?.includes('登录中')""",
                timeout=5_000,
            )
            expect("重试动作链:失败行转「登录中」", True)
            calls = await page.evaluate("window.__myiaBrowserSmokeCalls")
            expect(
                "重试走 browser.open force:true(单入口)",
                len(calls["open"]) == 1
                and calls["open"][0]["kind"] == "tg_web_login"
                and calls["open"][0]["session_key"] == "telegram-alt2"
                and calls["open"][0]["force"] is True,
            )
            expect(
                "关闭走 browser.close {op_id}",
                len(calls["close"]) == 1 and calls["close"][0]["op_id"] == "telegram-alt3",
            )
            await page.screenshot(path="/tmp/myssia-browser-module-smoke.png", full_page=True)
            print("screenshot: /tmp/myssia-browser-module-smoke.png")
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
    print("浏览器模块页无头冒烟:全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
