"""yaml 编辑弹窗报障探针:内容对照 + 滚动实测 + 截图存证。

环境:vite(5173) + bridge(8797 → 真 sidecar,沙箱 home)。
用法:python3 probe.py
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
SHIM = (HERE / "shim.js").read_text()
GAMES_YAML = pathlib.Path("/tmp/myia-yaml-repro/home/plugins/games.yaml")

SCROLL_METRICS = """
() => {
  const info = (el) => el && ({
    cls: (el.className && el.className.toString ? el.className.toString() : '').slice(0, 70),
    scrollH: el.scrollHeight, clientH: el.clientHeight, offsetH: el.offsetHeight,
    overflowY: getComputedStyle(el).overflowY, overflowX: getComputedStyle(el).overflowX,
    height: getComputedStyle(el).height, rectH: Math.round(el.getBoundingClientRect().height),
  });
  const scroller = document.querySelector('.cm-scroller');
  const wrap = document.querySelector('[data-testid="yaml-editor"]');
  const editorEl = document.querySelector('.cm-editor');
  const content = document.querySelector('.cm-content');
  return {
    scroller: info(scroller), wrap: info(wrap), editor: info(editorEl), content: info(content),
    scrollOffsets: scroller ? { top: scroller.scrollTop, left: scroller.scrollLeft } : null,
  };
}
"""


def collect_editor_state(page, label):
    state = {}
    state["metrics"] = page.evaluate(SCROLL_METRICS)
    content_text = page.evaluate("() => document.querySelector('.cm-content')?.innerText ?? null")
    if content_text is None:
        state["content_lines"] = None
    else:
        lines = content_text.split("\n")
        state["content_lines"] = {
            "count": len(lines),
            "head": lines[:3],
            "tail": lines[-3:],
        }
    return state


def try_scroll(page, label):
    """三种滚动途径各试一次:程序置 scrollTop / 鼠标滚轮 / 键盘 PageDown。"""
    out = {}
    out["programmatic"] = page.evaluate(
        """() => {
          const s = document.querySelector('.cm-scroller');
          if (!s) return { found: false };
          s.scrollTop = 400;
          return { found: true, after: s.scrollTop, scrollable: s.scrollHeight > s.clientHeight };
        }"""
    )
    box = page.evaluate(
        """() => {
          const s = document.querySelector('.cm-scroller');
          if (!s) return null;
          const r = s.getBoundingClientRect();
          return { x: r.x + r.width / 2, y: r.y + Math.min(r.height / 2, 200) };
        }"""
    )
    if box:
        page.mouse.move(box["x"], box["y"])
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(300)
        out["wheel_top_after"] = page.evaluate(
            "() => document.querySelector('.cm-scroller')?.scrollTop"
        )
    page.keyboard.press("PageDown")
    page.wait_for_timeout(300)
    out["pagedown_top_after"] = page.evaluate(
        "() => document.querySelector('.cm-scroller')?.scrollTop"
    )
    return out


def main():
    results = {"dialog": {}, "screen": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=(
                "/Users/zhengbingjin/Library/Caches/ms-playwright/chromium-1243/"
                "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
            ),
        )
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.add_init_script(SHIM)
        page.on("console", lambda m: print(f"[console.{m.type}] {m.text[:200]}", file=sys.stderr))
        page.on("pageerror", lambda e: print(f"[pageerror] {e}", file=sys.stderr))

        # ---- 场景 A:源管理屏 → 行编辑弹窗(games.yaml,330 行) ----
        page.goto("http://localhost:5173/#/sources")
        page.wait_for_selector("button[title^='弹出编辑对话框'][title*='games.yaml']", timeout=20000)
        page.wait_for_timeout(800)
        edit_btn = page.locator("button[title^='弹出编辑对话框'][title*='games.yaml']").first
        edit_btn.click()
        page.wait_for_selector("[data-testid='yaml-editor-dialog']", timeout=10000)
        page.wait_for_selector(".cm-content", timeout=10000)
        page.wait_for_timeout(1000)

        results["dialog"]["path"] = page.locator("[data-testid='editor-path']").inner_text()
        results["dialog"]["state"] = collect_editor_state(page, "dialog")
        results["dialog"]["scroll"] = try_scroll(page, "dialog")
        page.locator("[data-testid='yaml-editor-dialog']").screenshot(path=str(HERE / "dialog-after-wheel.png"))

        # 磁盘真值对照
        disk = GAMES_YAML.read_text()
        shown = page.evaluate("() => document.querySelector('.cm-content')?.innerText ?? ''")
        disk_lines = disk.rstrip("\n").split("\n")
        shown_lines = shown.rstrip("\n").split("\n")
        results["dialog"]["content_match"] = {
            "disk_lines": len(disk_lines),
            "shown_lines": len(shown_lines),
            "head_equal": shown_lines[:3] == disk_lines[:3],
            "tail_equal": shown_lines[-3:] == disk_lines[-3:],
            "tail_shown": shown_lines[-3:],
            "tail_disk": disk_lines[-3:],
        }
        page.screenshot(path=str(HERE / "sources-dialog-full.png"))

        # 关弹窗(可能 confirm,自动接受)
        page.once("dialog", lambda d: d.accept())
        page.keyboard.press("Escape")
        page.wait_for_timeout(600)

        # ---- 场景 B:配置编辑屏(双栏)同一文件 ----
        page.goto("http://localhost:5173/#/yaml-editor")
        page.wait_for_selector("text=games.yaml", timeout=15000)
        page.wait_for_timeout(500)
        page.locator("text=games.yaml").first.click()
        page.wait_for_selector(".cm-content", timeout=10000)
        page.wait_for_timeout(800)
        results["screen"]["state"] = collect_editor_state(page, "screen")
        results["screen"]["scroll"] = try_scroll(page, "screen")
        page.screenshot(path=str(HERE / "yaml-editor-screen.png"))

        browser.close()

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
