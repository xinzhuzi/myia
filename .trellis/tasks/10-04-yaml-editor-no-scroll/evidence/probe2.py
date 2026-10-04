"""yaml 编辑链全面体检:输入/脏标记/校验/保存回路/切文件/findings 滚动/双栏屏。

环境:vite(5174)+ bridge(8798 → 真 sidecar,沙箱 home)。只写沙箱文件。
用法:/opt/homebrew/bin/python3 probe2.py
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
HOME = HERE / "home"
RESULTS = {"checks": []}


def check(name, ok, detail=None):
    RESULTS["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  | {detail}" if detail else ""), file=sys.stderr)


def pick_row_titles(page):
    page.goto("http://localhost:5174/#/sources")
    page.wait_for_selector("button[title^='弹出编辑对话框']", timeout=20000)
    page.wait_for_timeout(800)
    btns = page.locator("button[title^='弹出编辑对话框']")
    return [btns.nth(i).get_attribute("title") for i in range(btns.count())]


def open_dialog(page, yaml_stem):
    page.goto("http://localhost:5174/#/sources")
    page.wait_for_selector(f"button[title^='弹出编辑对话框'][title*='/{yaml_stem}.yaml']", timeout=20000)
    page.wait_for_timeout(600)
    page.locator(f"button[title^='弹出编辑对话框'][title*='/{yaml_stem}.yaml']").first.click()
    page.wait_for_selector("[data-testid='yaml-editor-dialog']", timeout=10000)
    page.wait_for_selector(".cm-content", timeout=10000)
    page.wait_for_timeout(700)


def stem_of(title):
    # title 形如「弹出编辑对话框:/abs/path/<stem>.yaml」
    return title.rsplit("/", 1)[-1].removesuffix(".yaml")


def first_line(page):
    return page.evaluate("() => document.querySelector('.cm-line')?.innerText ?? null")


def dialog_title(page):
    return page.locator("[data-testid='editor-title'] span").first.inner_text()


def save_button_state(page):
    btns = page.locator("[data-testid='yaml-editor-dialog'] button", has_text="保存")
    return None if btns.count() == 0 else btns.first.is_disabled()


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=CHROME)
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.add_init_script(SHIM)
        page.on("pageerror", lambda e: print(f"[pageerror] {e}", file=sys.stderr))

        # ============ A. 弹窗内输入编辑(ai-news.yaml,169 行,首屏有行) ============
        titles = pick_row_titles(page)
        primary = "ai-news" if any("ai-news.yaml" in t for t in titles) else stem_of(titles[0])
        other_titles = [t for t in titles if stem_of(t) != primary]
        check("A0 首屏可选行就绪", len(titles) > 0 and len(other_titles) > 0, f"visible={sorted({stem_of(t) for t in titles})}")
        open_dialog(page, primary)
        news_disk = (HOME / "plugins" / f"{primary}.yaml").read_text().split("\n")
        check("A1 打开即载入 news.yaml 头行", first_line(page) == news_disk[0], first_line(page)[:50])

        page.locator(".cm-line").first.click()
        page.keyboard.press("End")
        page.keyboard.type("  # probe-edit")
        page.wait_for_timeout(400)
        edited_first = first_line(page)
        check("A2 键盘输入生效(行尾追加)", edited_first == news_disk[0] + "  # probe-edit", edited_first[-40:])
        check("A3 脏标记出现(标题带 *)", "*" in dialog_title(page), dialog_title(page))
        check("A4 保存按钮随 dirty 解禁", save_button_state(page) is False)

        # ============ B. 校验互动:改成坏 yaml ============
        page.keyboard.press("Home")
        page.keyboard.press("Shift+End")
        page.keyboard.type("broken: [unclosed")
        page.wait_for_timeout(300)
        page.get_by_role("button", name="校验").click()
        page.wait_for_timeout(1500)
        panel = page.locator("[data-testid='findings-panel']").count()
        errs = page.locator("[data-testid='findings-panel'] li[data-level='error']").count()
        first_msg = page.locator("[data-testid='findings-panel'] li").first.inner_text() if panel else ""
        check("B1 坏 yaml 校验出 error findings", panel >= 1 and errs >= 1, first_msg[:80].replace("\n", " | "))
        # findings 面板滚动:构造多 findings(8 源缺 url)
        page.keyboard.press("Home")
        page.keyboard.press("Shift+End")
        page.keyboard.type("id: probe-broken")
        page.locator(".cm-content").click()
        page.keyboard.press("Meta+a")
        synthetic = "\n".join(
            ["id: probe-broken", "name: probe", "sources:"] +
            [f"  - name: s{i}\n    enable: true" for i in range(8)]
        )
        page.keyboard.insert_text(synthetic)
        page.wait_for_timeout(300)
        page.get_by_role("button", name="校验").click()
        page.wait_for_timeout(1500)
        area = page.evaluate(
            """() => {
              const dlg = document.querySelector("[data-testid='yaml-editor-dialog']");
              // 结果区 = 带 overflow-y-auto 的 flex 容器
              const els = [...dlg.querySelectorAll('div')].filter(e => getComputedStyle(e).overflowY === 'auto');
              return els.map(e => ({cls: e.className.slice(0,40), scrollH: e.scrollHeight, clientH: e.clientHeight}));
            }"""
        )
        results_area = next((a for a in area if "border-t" in a["cls"] or a["scrollH"] > 0), None)
        if results_area:
            check("B2 多 findings 结果区可滚或未溢出",
                  results_area["clientH"] >= min(results_area["scrollH"], 160),
                  json.dumps(results_area))
        else:
            check("B2 结果区(overflow-y:auto)存在", False, json.dumps(area))

        # ============ C. 放弃改动 → 干净弹窗 → 小编辑 → 保存回路 ============
        page.once("dialog", lambda d: d.accept())
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)
        check("C1 dirty 守卫后弹窗可关", page.locator("[data-testid='yaml-editor-dialog']").count() == 0)

        open_dialog(page, primary)
        check("C2 重开后内容回磁盘原样", first_line(page) == news_disk[0])
        page.locator(".cm-line").first.click()
        page.keyboard.press("End")
        page.keyboard.type("  # probe-save")
        page.wait_for_timeout(300)
        page.keyboard.press("Meta+s")  # Cmd+S 路径保存
        page.wait_for_timeout(2500)
        save_ok = page.locator("[data-testid='save-ok']").count()
        doctor = page.locator("[data-testid='doctor-check']").count()
        disk_now = (HOME / "plugins" / f"{primary}.yaml").read_text().split("\n")
        bak_exists = (HOME / "plugins" / f"{primary}.yaml.bak").exists()
        check("C3 Cmd+S 保存成功提示", save_ok == 1)
        check("C4 doctor 复核提示出现", doctor == 1, page.locator("[data-testid='doctor-check']").inner_text() if doctor else None)
        check("C5 落盘含编辑", any("probe-save" in ln for ln in disk_now))
        check("C6 .bak 留底生成", bak_exists)
        check("C7 保存后标题去 *", "*" not in dialog_title(page), dialog_title(page))

        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

        # ============ D. 切文件:同屏关一个开另一个 ============
        secondary = stem_of(other_titles[0])
        open_dialog(page, secondary)
        stocks_disk = (HOME / "plugins" / f"{secondary}.yaml").read_text().split("\n")
        path_shown = page.locator("[data-testid='editor-path']").inner_text()
        check("D1 切到另一文件路径正确", path_shown.endswith(f"{secondary}.yaml"), path_shown)
        check("D2 内容随文件切换", first_line(page) == stocks_disk[0], first_line(page)[:50])
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

        # ============ E. 双栏配置编辑屏基本面 ============
        page.goto("http://localhost:5174/#/yaml-editor")
        page.wait_for_selector("text=games.yaml", timeout=15000)
        page.wait_for_timeout(800)
        listed = page.locator("text=wool.yaml").count()
        check("E1 双栏屏左栏列出插件 yaml", listed >= 1)
        page.locator("text=wool.yaml").first.click()
        page.wait_for_selector(".cm-content", timeout=10000)
        page.wait_for_timeout(700)
        wool_disk = (HOME / "plugins" / "wool.yaml").read_text().split("\n")
        check("E2 双栏屏载入 wool.yaml", first_line(page) == wool_disk[0], first_line(page)[:50])
        page.locator(".cm-line").first.click()
        page.keyboard.press("End")
        page.keyboard.type("  # probe-screen")
        page.wait_for_timeout(400)
        check("E3 双栏屏输入生效", first_line(page) == wool_disk[0] + "  # probe-screen")
        page.screenshot(path=str(HERE / "sweep-screen.png"))

        browser.close()

    print(json.dumps(RESULTS, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
