"""编辑器内核功能实机验证:撤销/重做、搜索替换、折叠、补全、ESC 冲突。

上一轮只做了代码级核实(basicSetup 合并语义),本轮逐项实敲。
环境:vite(5176)+ bridge(8799 → 真 sidecar,沙箱)。
"""
import json
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


def first_line(page):
    return page.evaluate("() => document.querySelector('.cm-line')?.innerText ?? ''")


def line_count(page):
    return page.evaluate("() => document.querySelectorAll('.cm-line').length")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=CHROME)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.add_init_script(SHIM)
        page.on("pageerror", lambda e: print(f"[pageerror] {e}", file=sys.stderr))

        page.goto("http://localhost:5176/#/sources")
        page.wait_for_selector("button[title^='弹出编辑对话框'][title*='ai-news.yaml']", timeout=20000)
        page.wait_for_timeout(600)
        page.locator("button[title^='弹出编辑对话框'][title*='ai-news.yaml']").first.click()
        page.wait_for_selector(".cm-content", timeout=10000)
        page.wait_for_timeout(800)
        base_line = first_line(page)

        # ---- T1/T2 撤销/重做(⌘Z / ⇧⌘Z) ----
        page.locator(".cm-line").first.click()
        page.keyboard.press("End")
        page.keyboard.type(" TYPED")
        page.wait_for_timeout(200)
        typed = first_line(page)
        page.keyboard.press("Meta+z")
        page.wait_for_timeout(300)
        undone = first_line(page)
        page.keyboard.press("Meta+Shift+z")
        page.wait_for_timeout(300)
        redone = first_line(page)
        page.keyboard.press("Meta+z")  # 打扫现场
        page.wait_for_timeout(200)
        check("T1 ⌘Z 撤销输入", typed.endswith("TYPED") and undone == base_line, f"typed…{typed[-12:]!r} -> {undone[-12:]!r}")
        check("T2 ⇧⌘Z 重做", redone.endswith("TYPED"), f"redone…{redone[-12:]!r}")

        # ---- T3 搜索(⌘F 面板 + 跳转) ----
        page.keyboard.press("Meta+f")
        page.wait_for_timeout(400)
        panel = page.locator(".cm-panel.cm-search")
        check("T3a ⌘F 打开搜索面板", panel.count() == 1)
        if panel.count():
            search_input = panel.locator("input").first
            search_input.fill("sources")
            page.keyboard.press("Enter")
            page.wait_for_timeout(300)
            sel = page.evaluate(
                "() => { const s = window.getSelection(); return s && s.toString() ? s.toString() : null; }"
            )
            check("T3b 搜索命中并选中", sel == "sources", f"selection={sel!r}")

        # ---- T4 替换(面板 replace) ----
        if panel.count():
            # 先造一个唯一目标词
            page.keyboard.press("Escape")  # 先关面板(下一项专门测 ESC 冲突,这里先观察)
            page.wait_for_timeout(400)
            dialog_after_esc = page.locator("[data-testid='yaml-editor-dialog']").count()
            print(f"[note] 搜索面板开着按 ESC:弹窗仍在={dialog_after_esc == 1}", file=sys.stderr)
            if dialog_after_esc == 1:
                page.locator(".cm-line").first.click()
                page.keyboard.press("End")
                page.keyboard.type(" probe-xyz probe-xyz")
                page.wait_for_timeout(200)
                page.keyboard.press("Meta+f")
                page.wait_for_timeout(300)
                pn = page.locator(".cm-panel.cm-search")
                pn.locator("input").first.fill("probe-xyz")
                inputs = pn.locator("input")
                # CM 搜索面板:第 3 个 input 是替换框(1 搜索词 2 替换词,顺序因版本而异;找 placeholder 或 name)
                rep = pn.locator("input[name=replace], input[placeholder*=eplace]")
                if rep.count() == 0:
                    rep = inputs.nth(1)
                rep.fill("probe-abc")
                # 「全部替换」按钮:文案因版本为 Replace all / 全部替换,取面板按钮兜底最后一个
                btns = pn.locator("button")
                replaced = False
                for i in range(btns.count()):
                    t = btns.nth(i).inner_text().strip().lower()
                    if "all" in t or "全部" in t:
                        btns.nth(i).click()
                        page.wait_for_timeout(400)
                        replaced = True
                        break
                body = page.locator(".cm-content").inner_text()
                check("T4 全部替换生效", replaced and "probe-abc" in body and "probe-xyz" not in body,
                      f"replaced={replaced}, abc-in={'probe-abc' in body}, xyz-in={'probe-xyz' in body}")
                # 撤销打扫
                page.keyboard.press("Escape")
                page.keyboard.press("Meta+z")
                page.wait_for_timeout(200)
            else:
                check("T4 全部替换生效(弹窗被 ESC 关闭,无法继续)", False, "见 T7 ESC 冲突")

        # ---- T5 折叠(⌥⌘[ / gutter 箭头) ----
        before = line_count(page)
        # 点进正文一个块首行(第 4 行左右),按折叠键
        page.locator(".cm-line").nth(3).click()
        page.keyboard.press("Meta+Alt+BracketLeft")
        page.wait_for_timeout(400)
        after = line_count(page)
        placeholder = page.locator(".cm-foldPlaceholder").count()
        check("T5 代码折叠生效", after < before or placeholder > 0, f"lines {before}->{after}, placeholder={placeholder}")
        if placeholder > 0 or after < before:  # 展开恢复
            page.keyboard.press("Meta+Alt+BracketRight")
            page.wait_for_timeout(200)

        # ---- T6 词级自动补全 ----
        page.locator(".cm-line").first.click()
        page.keyboard.press("End")
        page.keyboard.type(" sou")
        page.wait_for_timeout(700)
        tooltip = page.locator(".cm-tooltip-autocomplete")
        opts = page.locator(".cm-tooltip-autocomplete li, .cm-completionLabel")
        ok6 = tooltip.count() >= 1 and opts.count() >= 1
        detail6 = page.locator(".cm-tooltip-autocomplete").inner_text().replace("\n", "/")[:60] if tooltip.count() else "(无弹窗)"
        check("T6 输入触发补全弹窗(含 sources 候选)", ok6, detail6)

        # ---- T7 ESC 冲突专项:补全弹窗开着按 ESC,弹窗会不会整个被关? ----
        dialog_before = page.locator("[data-testid='yaml-editor-dialog']").count()
        if page.locator(".cm-tooltip-autocomplete").count():
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            dialog_after = page.locator("[data-testid='yaml-editor-dialog']").count()
            tooltip_after = page.locator(".cm-tooltip-autocomplete").count()
            check("T7 ESC 只关补全弹窗、不关编辑弹窗", dialog_after == 1, f"dialog {dialog_before}->{dialog_after}, tooltip left={tooltip_after}")
        else:
            check("T7 ESC 冲突(前置:补全弹窗在场)", False, "T6 未出弹窗,无从测")

        page.screenshot(path=str(HERE / "kernel-test-final.png"))
        browser.close()
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
