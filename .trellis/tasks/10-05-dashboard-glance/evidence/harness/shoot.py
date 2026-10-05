"""S7 无头冒烟视觉取证驱动(10-05-dashboard-glance)。

前置:vite(5173,desktop/ui-src)+ mock 桥(8790,harness/mock-bridge.py)。
用法(任意目录):/opt/homebrew/opt/python@3.14/bin/python3.14 shoot.py

产物(../ 即 evidence/):
  01-verdict-ok.png           verdict ok 态行(最关键,领衔)
  02-verdict-dead.png         verdict dead 态行(可点链接态)
  03-overview-four-cells.png  概览四格(ok 态)
  04-overview-tooltip.png     概览四格 + ⓘ tooltip 展开(活跃源说明)
  05-alert-list-dead.png      告警清单(dead 态:3 行 + 溢出口)
  06-category-note-dead.png   品类节(节注「1 品类异常」+ 品类卡)
  07-success-rate-card-ok.png 最近采集成功率卡(ok 态 80%)
  08-fullpage-ok.png          ok 态整屏
  09-fullpage-dead.png        dead 态整屏
  probe.json                  DOM 断言 + 文字重叠/溢出机械探针(OCR 的互补证据)
"""

from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent
SHIM = (HERE / "shim.js").read_text(encoding="utf-8")
BASE = "http://localhost:5173"
BRIDGE = "http://127.0.0.1:8790"

results: list[dict] = []  # 每张截屏:路径 + 断言 + 探针


def set_scenario(name: str) -> str:
    with urllib.request.urlopen(f"{BRIDGE}/scenario?set={name}", timeout=5) as r:
        return json.loads(r.read())["scenario"]


def shoot(page, name: str, locator=None, full_page: bool = False, clip=None) -> dict:
    path = EVIDENCE / f"{name}.png"
    if locator is not None:
        locator.screenshot(path=str(path))
    else:
        page.screenshot(path=str(path), full_page=full_page, clip=clip)
    entry = {"shot": f"{name}.png", "bytes": path.stat().st_size}
    results.append(entry)
    print(f"[shot] {name}.png {entry['bytes']}B")
    return entry


# DOM 机械探针:目标根内任意两个「都不互为祖先」的文字叶子矩形相交 = 重叠;
# 溢出 = 非 truncate 元素 scrollWidth > clientWidth + 1(截断类是设计内截断)。
PROBE_JS = """
(selector) => {
  const root = document.querySelector(selector);
  if (!root) return { error: "root-not-found:" + selector };
  const leaves = [];
  const walk = (el) => {
    for (const child of el.childNodes) {
      if (child.nodeType === Node.TEXT_NODE && child.textContent.trim()) {
        leaves.push(el);
        break;
      }
    }
    for (const kid of el.children) walk(kid);
  };
  walk(root);
  const rects = leaves.map((el) => ({ el, r: el.getBoundingClientRect() }));
  const overlaps = [];
  const TOL = 1.5; // 亚像素容差
  for (let i = 0; i < rects.length; i += 1) {
    for (let j = i + 1; j < rects.length; j += 1) {
      const a = rects[i], b = rects[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      const ox = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
      const oy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
      if (ox > TOL && oy > TOL) {
        overlaps.push({
          a: (a.el.textContent || "").trim().slice(0, 40),
          b: (b.el.textContent || "").trim().slice(0, 40),
          ox: Math.round(ox * 10) / 10,
          oy: Math.round(oy * 10) / 10,
        });
      }
    }
  }
  const overflows = [];
  for (const { el } of rects) {
    const cls = el.getAttribute("class") || "";
    if (cls.includes("truncate")) continue;
    if (el.scrollWidth > el.clientWidth + 1) {
      overflows.push({
        text: (el.textContent || "").trim().slice(0, 40),
        scrollWidth: el.scrollWidth,
        clientWidth: el.clientWidth,
      });
    }
  }
  return {
    textLeaves: rects.length,
    overlaps,
    overflows,
    docHorizontalOverflow:
      document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  };
}
"""


def probe(page, selector: str, label: str) -> dict:
    data = page.evaluate(PROBE_JS, selector)
    print(f"[probe:{label}] {json.dumps(data, ensure_ascii=False)}")
    return {"target": label, "selector": selector, **data}


def wait_dashboard(page, force=False):
    if force:
        # 同 URL 的 #/ goto 是 same-document 导航不重载(切场景后零 rpc 已证),
        # 先跳 about:blank 强制丢文档,shim+夹具才随新文档重跑
        page.goto("about:blank")
    page.goto(f"{BASE}/#/", wait_until="domcontentloaded")
    page.wait_for_selector('[data-testid="dashboard-screen-root"]', timeout=20000)
    page.wait_for_selector('[data-testid="dashboard-verdict"]', timeout=20000)
    page.wait_for_selector('[data-testid^="category-"]', timeout=20000)
    time.sleep(0.8)  # sparkline/反馈卡等次波渲染


def main() -> int:
    failures: list[str] = []
    # python playwright 自带浏览器构建(1223)未下载;复用本机缓存里 node 版
    # chromium-1243 的 Chrome for Testing 二进制(版本近邻,能力一致)。
    executable = (
        "/Users/zhengbingjin/Library/Caches/ms-playwright/chromium-1243/"
        "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=executable)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
            color_scheme="dark",
        )
        page = context.new_page()
        page.add_init_script(SHIM)
        page.set_default_timeout(30000)

        # ---------------- 场景 ok ----------------
        assert set_scenario("ok") == "ok"
        wait_dashboard(page)

        verdict = page.locator('[data-testid="dashboard-verdict"]')
        ok_text = verdict.inner_text()
        ok_asserts = {
            "text": ok_text,
            "一切正常": "一切正常" in ok_text,
            "今日采集 128 条": "今日采集 128 条" in ok_text,
            "5/5 源在线": "5/5 源在线" in ok_text,
            "推送成功 5": "推送成功 5" in ok_text,
        }
        print(f"[assert:verdict-ok] {json.dumps(ok_asserts, ensure_ascii=False)}")
        for k, v in ok_asserts.items():
            if k != "text" and not v:
                failures.append(f"verdict-ok 缺 {k}")
        shoot(page, "01-verdict-ok", locator=verdict)
        results[-1]["asserts"] = ok_asserts
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-verdict"]', "verdict-ok")

        # 概览四格(元素截屏,含节头)
        overview = page.locator('[data-testid="dashboard-overview"]')
        ov_text = overview.inner_text()
        cells = page.evaluate(
            "() => Array.from(document.querySelectorAll('[data-testid^=\"stat-\"]')).map((el) => el.getAttribute('data-testid') + '=' + (el.textContent || '').trim())"
        )
        print(f"[assert:overview-cells] {json.dumps(cells, ensure_ascii=False)}")
        shoot(page, "03-overview-four-cells", locator=overview)
        results[-1]["cells"] = cells
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-overview"]', "overview")

        # ⓘ tooltip 展开:悬停「活跃源说明」HintButton(Radix openDelay 300ms)
        page.locator('[data-testid="dashboard-overview"]').scroll_into_view_if_needed()
        page.locator('[aria-label="活跃源说明"]').hover()
        page.wait_for_selector('[data-slot="tooltip-content"][data-state="open"]', timeout=5000)
        time.sleep(0.5)  # fade-in 动画落定
        tip_text = page.locator('[data-slot="tooltip-content"]').inner_text()
        print(f"[assert:tooltip] {tip_text!r}")
        if "ok+degraded" not in tip_text:
            failures.append(f"tooltip 文案异常: {tip_text!r}")
        clip = page.evaluate(
            """() => {
              const grid = document.querySelector('[data-testid="dashboard-overview"]');
              const tip = document.querySelector('[data-slot="tooltip-content"]');
              const a = grid.getBoundingClientRect(), b = tip.getBoundingClientRect();
              const x = Math.min(a.left, b.left), y = Math.min(a.top, b.top);
              const r = Math.max(a.right, b.right), bo = Math.max(a.bottom, b.bottom);
              return { x, y, width: r - x, height: bo - y };
            }"""
        )
        shoot(page, "04-overview-tooltip", clip=clip)
        results[-1]["tooltipText"] = tip_text
        results[-1]["clip"] = clip
        page.mouse.move(0, 0)  # 收 tooltip

        # 最近采集成功率卡(含卡头的整张 Card)
        rate_card = page.locator('[data-testid="run-success-rate"]').locator(
            "xpath=ancestor::div[contains(@class,\"card\")][1]"
        )
        rate_text = rate_card.inner_text()
        print(f"[assert:success-rate-card] {rate_text.splitlines()[:8]}")
        shoot(page, "07-success-rate-card-ok", locator=rate_card)
        results[-1]["cardTextHead"] = rate_text.splitlines()[:8]
        results[-1]["probe"] = probe(page, '[data-testid="run-success-rate"]', "success-rate")

        # ok 态整屏
        shoot(page, "08-fullpage-ok", full_page=True)
        rpc_ok = page.evaluate("() => window.__rpc")
        methods_ok = sorted({r["method"] for r in rpc_ok})
        print(f"[rpc-ok] {methods_ok}")
        results.append({"shot": "08-fullpage-ok.png", "rpcMethods": methods_ok})

        # ---------------- 场景 dead(切夹具后整页强制重载) ----------------
        assert set_scenario("dead") == "dead"
        wait_dashboard(page, force=True)

        verdict_d = page.locator('[data-testid="dashboard-verdict"]')
        dead_text = verdict_d.inner_text()
        dead_asserts = {
            "text": dead_text,
            "2 个源失效": "2 个源失效" in dead_text,
            "3/6 源在线": "3/6 源在线" in dead_text,
            "tagName=A(可点)": verdict_d.evaluate("(el) => el.tagName") == "A",
        }
        print(f"[assert:verdict-dead] {json.dumps(dead_asserts, ensure_ascii=False)}")
        for k, v in dead_asserts.items():
            if k != "text" and k != "tagName=A(可点)" and not v:
                failures.append(f"verdict-dead 缺 {k}")
        if not dead_asserts["tagName=A(可点)"]:
            failures.append("verdict-dead 不是可点链接")
        shoot(page, "02-verdict-dead", locator=verdict_d)
        results[-1]["asserts"] = dead_asserts
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-verdict"]', "verdict-dead")

        # 告警清单
        alert = page.locator('[data-testid="dashboard-alert-list"]')
        page.wait_for_selector('[data-testid="dashboard-alert-list"]', timeout=5000)
        alert_text = alert.inner_text()
        rows = page.evaluate("() => Array.from(document.querySelectorAll('[data-testid^=\"alert-row-\"]')).map((el) => (el.textContent || '').trim())")
        overflow_text = page.locator('[data-testid="dashboard-alert-overflow"]').inner_text() if page.locator('[data-testid="dashboard-alert-overflow"]').count() else ""
        print(f"[assert:alert] rows={json.dumps(rows, ensure_ascii=False)} overflow={overflow_text!r}")
        if len(rows) != 3:
            failures.append(f"告警行数 {len(rows)} ≠ 3")
        if "还有 2 个异常" not in overflow_text:
            failures.append(f"溢出口文案异常: {overflow_text!r}")
        shoot(page, "05-alert-list-dead", locator=alert)
        results[-1]["rows"] = rows
        results[-1]["overflow"] = overflow_text
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-alert-list"]', "alert-list")

        # 品类节(节注 + 品类卡)
        cat_section = page.locator('section[aria-label="品类状态"]')
        cat_text = cat_section.inner_text()
        print(f"[assert:category-note] {cat_text.splitlines()[:6]}")
        if "1 品类异常" not in cat_text:
            failures.append(f"品类节注缺「1 品类异常」: {cat_text[:80]!r}")
        shoot(page, "06-category-note-dead", locator=cat_section)
        results[-1]["sectionHead"] = cat_text.splitlines()[:6]
        results[-1]["probe"] = probe(page, 'section[aria-label="品类状态"]', "category-section")

        shoot(page, "09-fullpage-dead", full_page=True)
        rpc_dead = page.evaluate("() => window.__rpc")
        results.append({"shot": "09-fullpage-dead.png", "rpcMethods": sorted({r["method"] for r in rpc_dead})})

        browser.close()

    (EVIDENCE / "probe.json").write_text(
        json.dumps({"results": results, "failures": failures}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"== S7 冒烟取证:shots={len(results)} failures={len(failures)} ==")
    for f in failures:
        print(f"  FAIL: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
