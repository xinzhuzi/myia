#!/usr/bin/env python3
"""TG 监控总卡无头冒烟(10-08-tg-web-line W4;程序化验证,禁屏控;
10-08-browser-module 接线:登录动作 mock 面改 browser.open)。

面板与注入:
- 静态服务 ``desktop/ui`` 构建产物(``npm run build``,HashRouter 免服务端);
- Playwright chromium 无头(浏览器二进制 = playwright 缺省缓存,与
  crawl4ai 组件轨同源;CLI 直跑仓 ``.venv``);
- IPC 注入:``add_init_script`` 定义 ``__TAURI_INTERNALS__.invoke``,按
  ``sidecar_request`` 的 method 应答 telegram.status / telegram.web.delete /
  browser.open(登录动作经浏览器模块统一入口,单入口铁律)/
  telegram.web.check(账号体检,10-11-tg-manage-absorb)四方法夹具
  —— 卡片三段 + 账号行 + 添加/删除/检测动作全链路渲染冒烟(零真实壳零
  真实网络零屏控)。

断言面:总卡渲染 / bot·session·web 三段 / 账号行 / 披露文案(建议小号/
扫码提示)/ 添加账号动作链(新行 + busy 态)/ 体检动作链(上次体检小字)/
删除动作链(行消失);截图落 /tmp 备查。
退出码 0 = 冒烟通过。

用法(仓库根):``.venv/bin/python desktop/scripts/tg-card-smoke.py``
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
# UI 目录可注入(装机件冒烟:MYIA_SMOKE_UI_DIR=/Applications/世事.app/
# Contents/Resources/ui 时验的就是装机包像素,判例=装机像素证据走无头冒烟)
import os as _os

UI_DIR = pathlib.Path(
    _os.environ.get("MYIA_SMOKE_UI_DIR", str(REPO_ROOT / "desktop" / "ui"))
)
PORT = 4517
PLAYWRIGHT_CACHE = pathlib.Path.home() / "Library" / "Caches" / "ms-playwright"

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
  const statusFixture = {
    bot: { configured: true, error: null },
    session: { exists: false },
    web: {
      accounts: [
        {
          account: "telegram-alt1",
          logged_in: true,
          logged_in_at: "2026-10-08T02:30:00+00:00",
          label: "小号·尾号93105",
          user_id: "8012674093",
          login_in_progress: false,
          login_note: null,
          last_verified_at: null,
          alive: null,
          check_in_progress: false,
          check_note: null,
        },
      ],
    },
  };
  let current = statusFixture;
  window.__TAURI_INTERNALS__ = {
    invoke: async (command, args) => {
      if (command !== "sidecar_request") {
        throw new Error("smoke 只应答 sidecar_request,收到: " + command);
      }
      const { method, params } = args ?? {};
      if (method === "telegram.status") return current;
      if (method === "browser.open") {
        const account = String(params?.session_key ?? "");
        const accounts = current.web.accounts.map((row) =>
          row.account === account ? { ...row, login_in_progress: true } : row,
        );
        if (!accounts.some((row) => row.account === account)) {
          accounts.push({
            account,
            logged_in: false,
            logged_in_at: null,
            login_in_progress: true,
            login_note: null,
          });
        }
        current = { ...current, web: { accounts } };
        return { started: true, op_id: account, kind: params?.kind };
      }
      if (method === "telegram.web.delete") {
        const account = String(params?.account ?? "");
        current = {
          ...current,
          web: {
            accounts: current.web.accounts.filter((row) => row.account !== account),
          },
        };
        return { deleted: true, account };
      }
      if (method === "telegram.web.check") {
        // 体检夹具(10-11-tg-manage-absorb):发起即翻完成态 —— 卡面立即
        // 回读渲染「上次体检 · 活」小字(真实路径 = 台账收尾 + 5s 轮询回读)
        const account = String(params?.account ?? "");
        const accounts = current.web.accounts.map((row) =>
          row.account === account
            ? {
                ...row,
                check_in_progress: false,
                last_verified_at: new Date().toISOString(),
                alive: true,
                check_note: "体检通过:登录态活(冒烟夹具)",
              }
            : row,
        );
        current = { ...current, web: { accounts } };
        return { started: true, account, note: "体检完成(冒烟夹具)" };
      }
      if (method === "telegram.web.rename") {
        // 改名夹具(2026-10-17 主人令「以后不记得是什么名字」):merge 改
        // label 后卡面回读新名(mock 侧即时生效,真实路径 = 标记 merge 写)
        const account = String(params?.account ?? "");
        const label = String(params?.label ?? "");
        const accounts = current.web.accounts.map((row) =>
          row.account === account ? { ...row, label } : row,
        );
        current = { ...current, web: { accounts } };
        return { renamed: true, account, label };
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


def cached_chromium() -> str | None:
    """Return the newest locally cached Chrome for Testing binary, if present."""
    matches = sorted(PLAYWRIGHT_CACHE.glob(
        "chromium-*/chrome-mac*/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    ))
    return str(matches[-1]) if matches else None


async def main() -> int:
    if not (UI_DIR / "index.html").exists():
        print(f"FAIL - 构建产物缺位({UI_DIR}/index.html);先 npm run build", file=sys.stderr)
        return 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        port_free = probe.connect_ex(("127.0.0.1", PORT)) != 0
    port = PORT if port_free else 4518
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
            executable_path = cached_chromium()
            browser = await p.chromium.launch(headless=True, executable_path=executable_path)
            page = await browser.new_page()
            await page.add_init_script(INJECT_SCRIPT)
            await page.goto(
                f"http://127.0.0.1:{port}/#/tg-account",
                wait_until="networkidle",
            )
            await page.wait_for_selector('[data-testid="telegram-card"]', timeout=10_000)
            expect("总卡渲染", True)
            expect("bot 段在册", await page.get_by_text("bot 线(Bot API)").count() == 1)
            expect(
                "session 段在册",
                await page.get_by_text("用户 session(Telethon)").count() == 1,
            )
            expect(
                "web 段在册",
                await page.get_by_text("网页登录(tg_web)").count() == 1,
            )
            expect(
                "账号行渲染",
                await page.locator(
                    '[data-testid="telegram-web-account-telegram-alt1"]'
                ).count()
                == 1,
            )
            expect(
                "身份面:备注名主显示(2026-10-11 主人令)",
                await page.get_by_text("小号·尾号93105").count() == 1,
            )
            expect(
                "身份面:键名+TG id 退小字",
                await page.get_by_text("telegram-alt1 · id 8012674093").count()
                == 1,
            )
            expect(
                "披露文案可见(建议小号)",
                await page.get_by_text("建议各键专用小号").count() >= 1,
            )
            expect(
                "扫码提示文案可见(AC2)",
                await page.get_by_text("免等验证码").count() >= 1,
            )
            # 添加账号动作链:填键名 → 点添加 → 新行 + busy 态(mock 置 in_progress)
            await page.get_by_label("新账号键名").fill("telegram-alt2")
            await page.locator('[data-testid="telegram-web-add"]').click()
            await page.wait_for_selector(
                '[data-testid="telegram-web-account-telegram-alt2"]', timeout=5_000
            )
            expect("添加账号后新行渲染", True)
            await page.wait_for_selector(
                '[data-testid="telegram-web-telegram-alt2-busy"]', timeout=5_000
            )
            expect("新行登录中 busy 态", True)
            # 体检动作链(10-11-tg-manage-absorb):点检测 → 立即回读翻完成态
            # → 「上次体检 · 活」小字出现(mock telegram.web.check)
            await page.locator(
                '[data-testid="telegram-web-telegram-alt1-check"]'
            ).click()
            await page.wait_for_selector(
                '[data-testid="telegram-web-telegram-alt1-verified"]', timeout=5_000
            )
            expect("体检后上次检查小字出现", True)
            expect(
                "体检小字判活",
                await page.get_by_text("上次检查").count() >= 1,
            )
            # 改名动作链(2026-10-17):点改名 → 行内输入框 → 填新名 → 保存
            # → 卡面主显示翻新名(mock telegram.web.rename merge label)
            await page.locator(
                '[data-testid="telegram-web-telegram-alt1-rename"]'
            ).click()
            await page.wait_for_selector(
                '[data-testid="telegram-web-telegram-alt1-rename-input"]',
                timeout=5_000,
            )
            expect("改名行内输入框出现", True)
            await page.get_by_label("账号 telegram-alt1 新备注名").fill(
                "羊毛专用小号"
            )
            await page.locator(
                '[data-testid="telegram-web-telegram-alt1-rename-confirm"]'
            ).click()
            await page.wait_for_selector(
                'text=羊毛专用小号', timeout=5_000
            )
            expect("改名后卡面主显示新备注名", True)
            expect(
                "改名成功 note 出现",
                await page.get_by_text("备注名已改为").count() >= 1,
            )
            await page.screenshot(
                path="/tmp/myssia-tg-card-smoke-rename.png", full_page=False
            )
            # 删除动作链:alt1 删除后行消失
            await page.locator(
                '[data-testid="telegram-web-telegram-alt1-delete"]'
            ).click()
            await page.wait_for_function(
                """() => document.querySelectorAll(
                    '[data-testid="telegram-web-account-telegram-alt1"]'
                ).length === 0""",
                timeout=5_000,
            )
            expect("删除后行消失", True)
            await page.screenshot(path="/tmp/myssia-tg-card-smoke.png", full_page=True)
            print("screenshot: /tmp/myssia-tg-card-smoke.png")
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
    print("TG 监控总卡无头冒烟:全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
