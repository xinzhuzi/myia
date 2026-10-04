"""收尾探针:替换/折叠/补全 + ESC 误关弹窗专项(T7b)。

probe3 已证:撤销/重做 ✓、⌘F 开面板 ✓、搜索面板 ESC 会误关整个弹窗(T7a 实锤)。
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
SHIM = (HERE / "shim.js").read_text()
CHROME = (
    "/Users/zhengbingjin/Library/Caches/ms-playwright/chromium-1243/"
    "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
)


def check(name, ok, detail=None):
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  | {detail}" if detail else ""), file=sys.stderr)


def open_dialog(page):
    page.goto("http://localhost:5176/#/sources")
    page.wait_for_selector("button[title^='弹出编辑对话框'][title*='ai-news.yaml']", timeout=20000)
    page.wait_for_timeout(500)
    page.locator("button[title^='弹出编辑对话框'][title*='ai-news.yaml']").first.click()
    page.wait_for_selector(".cm-content", timeout=10000)
    page.wait_for_timeout(700)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=CHROME)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.add_init_script(SHIM)
        page.on("pageerror", lambda e: print(f"[pageerror] {e}", file=sys.stderr))

        # ---- 替换(不经 ESC,面板用 ✕ 关) ----
        open_dialog(page)
        page.locator(".cm-line").first.click()
        page.keyboard.press("End")
        page.keyboard.type(" probe-xyz probe-xyz")
        page.wait_for_timeout(200)
        page.keyboard.press("Meta+f")
        page.wait_for_timeout(300)
        pn = page.locator(".cm-panel.cm-search")
        inputs = pn.locator("input")
        inputs.first.fill("probe-xyz")
        rep = pn.locator("input[name=replace]")
        if rep.count() == 0:
            rep = inputs.nth(1)
        rep.fill("probe-abc")
        btn_all = pn.locator("button[name=replaceAll]")
        if btn_all.count() == 0:
            btn_all = pn.get_by_role("button").filter(has_text="all")
        clicked = False
        if btn_all.count():
            btn_all.first.click()
            clicked = True
        page.wait_for_timeout(400)
        body = page.locator(".cm-content").inner_text()
        check("T4 全部替换生效", clicked and "probe-abc" in body and "probe-xyz" not in body,
              f"btnAll={btn_all.count()} abc={'probe-abc' in body} xyz={'probe-xyz' in body}")
        close_btn = pn.locator("button[name=close]")
        if close_btn.count():
            close_btn.first.click()
        page.keyboard.press("Meta+z")  # 撤销替换
        page.wait_for_timeout(200)

        # ---- 搜索选中可见性(T3b 复测) ----
        page.keyboard.press("Meta+f")
        page.wait_for_timeout(300)
        pn = page.locator(".cm-panel.cm-search")
        pn.locator("input").first.fill("sources")
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        sel = page.evaluate("() => window.getSelection()?.toString() || null")
        selbg = page.locator(".cm-selectionBackground").count()
        check("T3b 搜索命中产生选区", (sel == "sources") or selbg > 0, f"sel={sel!r} selBg={selbg}")
        cb = pn.locator("button[name=close]")
        if cb.count():
            cb.first.click()

        # ---- 折叠 ----
        before = page.evaluate("() => document.querySelectorAll('.cm-line').length")
        page.locator(".cm-line").nth(3).click()
        page.keyboard.press("Meta+Alt+BracketLeft")
        page.wait_for_timeout(400)
        after = page.evaluate("() => document.querySelectorAll('.cm-line').length")
        ph = page.locator(".cm-foldPlaceholder").count()
        check("T5 折叠生效", after < before or ph > 0, f"lines {before}->{after} placeholder={ph}")
        if ph > 0:
            page.keyboard.press("Meta+Alt+BracketRight")
            page.wait_for_timeout(200)

        # ---- 补全 + T7b:补全弹窗开着按 ESC ----
        page.locator(".cm-line").first.click()
        page.keyboard.press("End")
        page.keyboard.type(" sou")
        page.wait_for_timeout(800)
        tooltip = page.locator(".cm-tooltip-autocomplete").count()
        detail6 = page.locator(".cm-tooltip-autocomplete").inner_text().replace("\n", "/")[:60] if tooltip else "(无弹窗)"
        check("T6 词级补全弹窗", tooltip >= 1, detail6)
        if tooltip:
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            dlg = page.locator("[data-testid='yaml-editor-dialog']").count()
            tip_left = page.locator(".cm-tooltip-autocomplete").count()
            check("T7b ESC 只关补全、不关编辑弹窗", dlg == 1, f"dialog_left={dlg} tooltip_left={tip_left}")
        browser.close()
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
