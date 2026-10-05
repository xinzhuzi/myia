"""S7 补批 11- 视觉取证驱动(10-05-dashboard-glance)。

前置:vite(5173,desktop/ui-src)+ mock 桥(8790,harness/mock-bridge.py,
场景 ok|dead|cred|doctorfail)。
用法(任意目录):/opt/homebrew/opt/python@3.14/bin/python3.14 shoot11.py

产物(../ 即 evidence/):
  11-unified-window-7d-ok.png      统一时间窗全景(领衔):概览头唯一 Select 切
                                   「7 天」→ 概览四格/采集量趋势/成功率三面同
                                   窗(趋势卡无自有 Select);含 ok 态 verdict 行
  12-unified-window-today-ok.png   切回「今日(UTC)」:趋势 = 单点居中如实画
  13-verdict-dead.png              verdict dead 态行(2 个源失效,可点 A)
  14-source-collapse-default.png   dead 态源健康度:坏源铺开 + 「N 个源正常」
                                   折叠组默认收起(aria-expanded=false)
  15-source-collapse-expanded.png  点开折叠组 → 正常源网格出现
  16-verdict-warning-cred.png      cred 态 verdict(2 项告警,warning 可点)
  17-alert-cred-credentials.png    cred 态概览:告警格 2 + 清单「凭据」行型
                                   (scope=credentials 人话映射,异常/提醒双行)
  18-verdict-unknown-doctorfail.png doctor 分区失败:verdict unknown「部分数据
                                   不可达」+ 降级卡 + 四格 — 态
  11-probe.json                     DOM 断言 + rpc 调用痕 + 文字重叠/溢出机械探针
"""

from __future__ import annotations

import json
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent
SHIM = (HERE / "shim.js").read_text(encoding="utf-8")
BASE = "http://localhost:5173"
BRIDGE = "http://127.0.0.1:8790"

UTC = timezone.utc
TODAY = datetime.now(UTC).strftime("%Y-%m-%d")
DAY6 = (datetime.now(UTC) - timedelta(days=6)).strftime("%Y-%m-%d")

results: list[dict] = []
failures: list[str] = []


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


def check(label: str, value, ok: bool):
    print(f"[assert:{label}] {json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value!r} -> {'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(f"{label}: {value!r}")


# 机械探针(与 shoot.py 同款):文字叶子矩形相交 = 重叠;非 truncate 元素
# scrollWidth > clientWidth + 1 = 溢出。
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
  const TOL = 1.5;
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


def wait_dashboard(page, force=False, categories=True):
    if force:
        page.goto("about:blank")
    page.goto(f"{BASE}/#/", wait_until="domcontentloaded")
    page.wait_for_selector('[data-testid="dashboard-screen-root"]', timeout=20000)
    page.wait_for_selector('[data-testid="dashboard-verdict"]', timeout=20000)
    if categories:
        page.wait_for_selector('[data-testid^="category-"]', timeout=20000)
    time.sleep(0.8)  # sparkline/反馈卡等次波渲染


def pick_window(page, option_label: str):
    """概览头 Select(全屏唯一)选档;Radix 真浏览器 mouse 点击即可开合。"""
    page.locator('[data-slot="select-trigger"][aria-label="概览时间范围"]').click()
    page.get_by_role("option", name=option_label, exact=True).click()


def rpc_log(page) -> list[dict]:
    return page.evaluate("() => window.__rpc")


def trend_days_calls(page) -> dict[str, list]:
    out: dict[str, list] = {"store.trend": [], "runs.trend": []}
    for entry in rpc_log(page):
        if entry.get("method") in out:
            out[entry["method"]].append((entry.get("params") or {}).get("days"))
    return out


# TrendChart 数据点层:每值一枚圆点(今日档 = 1 枚居中;7 天档 = 7 枚)
DOTS_JS = """
() => {
  const out = {};
  for (const tid of ["dashboard-sparkline", "dashboard-rate-sparkline"]) {
    const el = document.querySelector(`[data-testid="${tid}"]`);
    if (!el) { out[tid] = { count: null }; continue; }
    const wrap = el.parentElement;
    const dots = wrap ? wrap.lastElementChild.querySelectorAll("span") : [];
    const styles = Array.from(dots).map((d) => d.getAttribute("style") || "");
    out[tid] = { count: dots.length, styles: styles.slice(0, 8) };
  }
  return out;
}
"""

# 多元素包围盒(全景 clip 用)
CLIP_UNION_JS = """
(selectors) => {
  let x = Infinity, y = Infinity, r = -Infinity, b = -Infinity;
  for (const s of selectors) {
    const el = document.querySelector(s);
    if (!el) return { error: "missing:" + s };
    const rect = el.getBoundingClientRect();
    x = Math.min(x, rect.left); y = Math.min(y, rect.top);
    r = Math.max(r, rect.right); b = Math.max(b, rect.bottom);
  }
  return { x, y, width: r - x, height: b - y };
}
"""


def panorama_clip(page):
    clip = page.evaluate(CLIP_UNION_JS, ['[data-testid="dashboard-verdict"]', 'section[aria-label="采集量趋势"]'])
    assert "error" not in clip, clip
    return clip


def main() -> int:
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

        # ================= 场景 ok:统一时间窗交互 =================
        assert set_scenario("ok") == "ok"
        wait_dashboard(page)

        trigger = page.locator('[data-slot="select-trigger"][aria-label="概览时间范围"]')
        check("初始窗=今日(UTC)", trigger.inner_text(), trigger.inner_text() == "今日(UTC)")
        dots0 = page.evaluate(DOTS_JS)
        check("初始单点(默认今日窗)", dots0, dots0["dashboard-sparkline"]["count"] == 1)

        # ---- ① 切「7 天」:概览/趋势/成功率三面同窗,趋势卡无自有 Select ----
        pick_window(page, "7 天")
        # 切窗即弃旧数据(组件内 setTrend(null) 先卸载轴/合计行再补新),谓词须判空
        page.wait_for_function(
            "() => { const el = document.querySelector('[data-testid=\"trend-total\"]'); return !!el && el.textContent.includes('近 7 天共 164 条'); }",
            timeout=15000,
        )
        header7 = page.locator('[data-testid="dashboard-overview"] h2').inner_text()
        check("概览头标题 7 天", header7, header7 == "近 7 天概览(UTC)")
        trigger7 = trigger.inner_text()
        check("Select 值 7 天", trigger7, trigger7 == "7 天")
        items7 = page.locator('[data-testid="stat-window-items"]').inner_text()
        check("采集格 7 天窗口和 164", items7.splitlines(), "近 7 天采集" in items7 and "164" in items7)
        axis = page.evaluate(
            "() => Array.from(document.querySelectorAll('[data-testid=\"trend-axis\"] span')).map((el) => el.textContent)"
        )
        check("趋势轴 7 天跨度", axis, len(axis) == 3 and axis[0] == DAY6 and axis[2] == TODAY)
        total7 = page.locator('[data-testid="trend-total"]').inner_text()
        check("趋势合计 7 天", total7, total7 == "近 7 天共 164 条 · 峰值 128 条/日")
        rate7 = page.locator('[data-testid="rate-summary"]').inner_text()
        check("成功率摘要 7 天", rate7, rate7 == "近 7 天累计成功率 84%(38/45 次成功)")
        dots7 = page.evaluate(DOTS_JS)
        check("两线数据点 7+5", dots7, dots7["dashboard-sparkline"]["count"] == 7 and dots7["dashboard-rate-sparkline"]["count"] == 5)
        days_calls = trend_days_calls(page)
        check("双趋势同窗重查 days=7", days_calls, days_calls["store.trend"][-1] == 7 and days_calls["runs.trend"][-1] == 7)
        selects = page.evaluate(
            "() => Array.from(document.querySelectorAll('[data-slot=\"select-trigger\"]')).map((el) => el.getAttribute('aria-label'))"
        )
        trend_selects = page.evaluate(
            "() => document.querySelectorAll('section[aria-label=\"采集量趋势\"] [data-slot=\"select-trigger\"]').length"
        )
        check("全屏唯一 Select(趋势卡 0 自有)", {"selects": selects, "trendCardSelects": trend_selects}, selects == ["概览时间范围"] and trend_selects == 0)

        clip = panorama_clip(page)
        shoot(page, "11-unified-window-7d-ok", clip=clip)
        results[-1].update(
            {
                "clip": clip,
                "header": header7,
                "trigger": trigger7,
                "statWindowItems": items7,
                "axis": axis,
                "trendTotal": total7,
                "rateSummary": rate7,
                "dots": dots7,
                "trendDaysCalls": days_calls,
                "selects": selects,
                "trendCardSelects": trend_selects,
            }
        )
        results[-1]["probe"] = probe(page, 'section[aria-label="采集量趋势"]', "trend-7d")
        results[-1]["probeOverview"] = probe(page, '[data-testid="dashboard-overview"]', "overview-7d")

        # ---- ② 切回「今日(UTC)」:趋势 = 单点如实画 ----
        pick_window(page, "今日(UTC)")
        page.wait_for_function(
            "() => { const el = document.querySelector('[data-testid=\"trend-total\"]'); return !!el && el.textContent.includes('今日共 128 条'); }",
            timeout=15000,
        )
        header1 = page.locator('[data-testid="dashboard-overview"] h2').inner_text()
        check("概览头标题今日", header1, header1 == "今日概览(UTC)")
        trigger1 = trigger.inner_text()
        check("Select 值今日", trigger1, trigger1 == "今日(UTC)")
        axis1 = page.evaluate(
            "() => Array.from(document.querySelectorAll('[data-testid=\"trend-axis\"] span')).map((el) => el.textContent)"
        )
        check("趋势轴单日(起=止=今日)", axis1, len(axis1) == 3 and axis1[0] == TODAY and axis1[2] == TODAY)
        total1 = page.locator('[data-testid="trend-total"]').inner_text()
        check("趋势合计今日", total1, total1 == "今日共 128 条 · 峰值 128 条/日")
        rate1 = page.locator('[data-testid="rate-summary"]').inner_text()
        check("成功率摘要今日", rate1, rate1 == "今日累计成功率 90%(9/10 次成功)")
        dots1 = page.evaluate(DOTS_JS)
        single_left = dots1["dashboard-sparkline"]["styles"][0] if dots1["dashboard-sparkline"]["styles"] else ""
        check(
            "单点居中(left=50%)",
            {"trendDots": dots1["dashboard-sparkline"]["count"], "rateDots": dots1["dashboard-rate-sparkline"]["count"], "left": single_left},
            dots1["dashboard-sparkline"]["count"] == 1 and dots1["dashboard-rate-sparkline"]["count"] == 1 and "left: 50%" in single_left,
        )
        days_calls1 = trend_days_calls(page)
        check("双趋势同窗重查 days=1", days_calls1, days_calls1["store.trend"][-1] == 1 and days_calls1["runs.trend"][-1] == 1)

        clip1 = panorama_clip(page)
        shoot(page, "12-unified-window-today-ok", clip=clip1)
        results[-1].update(
            {
                "clip": clip1,
                "header": header1,
                "trigger": trigger1,
                "axis": axis1,
                "trendTotal": total1,
                "rateSummary": rate1,
                "dots": dots1,
                "trendDaysCalls": days_calls1,
            }
        )
        results[-1]["probe"] = probe(page, 'section[aria-label="采集量趋势"]', "trend-today")

        # ================= 场景 dead:verdict dead + 源折叠组 =================
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
            if k not in ("text", "tagName=A(可点)") and not v:
                failures.append(f"verdict-dead 缺 {k}")
        if not dead_asserts["tagName=A(可点)"]:
            failures.append("verdict-dead 不是可点链接")
        shoot(page, "13-verdict-dead", locator=verdict_d)
        results[-1]["asserts"] = dead_asserts
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-verdict"]', "verdict-dead")

        # ---- ③ 源健康度:坏源铺开 + 正常源折叠组默认收起 → 点开 ----
        src_section = page.locator('section[aria-label="源健康度"]')
        bad_grid = {
            "present": page.locator('[data-testid="source-health-grid"]').count(),
            "cards": page.evaluate(
                "() => Array.from(document.querySelectorAll('[data-testid=\"source-health-grid\"] [data-testid^=\"source-card-\"]')).map((el) => el.getAttribute('data-testid'))"
            ),
        }
        toggle = page.locator('[data-testid="source-ok-toggle"]')
        collapsed = {
            "text": toggle.inner_text(),
            "ariaExpanded": toggle.get_attribute("aria-expanded"),
            "groupPresent": page.locator('[data-testid="source-ok-group"]').count(),
        }
        check(
            "dead 态坏源铺开",
            bad_grid,
            bad_grid["present"] == 1 and len(bad_grid["cards"]) == 4 and bad_grid["cards"][0].endswith("#deadone"),
        )
        check(
            "正常源折叠组默认收起",
            collapsed,
            collapsed["ariaExpanded"] == "false" and collapsed["groupPresent"] == 0 and "2 个源正常" in collapsed["text"],
        )
        shoot(page, "14-source-collapse-default", locator=src_section)
        results[-1].update({"badGrid": bad_grid, "collapsed": collapsed})
        results[-1]["probe"] = probe(page, 'section[aria-label="源健康度"]', "source-collapsed")

        toggle.click()
        page.wait_for_selector('[data-testid="source-ok-group"]', timeout=5000)
        expanded = {
            "text": toggle.inner_text(),
            "ariaExpanded": toggle.get_attribute("aria-expanded"),
            "groupCards": page.evaluate(
                "() => Array.from(document.querySelectorAll('[data-testid=\"source-ok-group\"] [data-testid^=\"source-card-\"]')).map((el) => el.getAttribute('data-testid'))"
            ),
        }
        check(
            "点开折叠组 → 正常源网格出现",
            expanded,
            expanded["ariaExpanded"] == "true" and sorted(c.split("#")[1] for c in expanded["groupCards"]) == ["a", "b"],
        )
        shoot(page, "15-source-collapse-expanded", locator=src_section)
        results[-1]["expanded"] = expanded
        results[-1]["probe"] = probe(page, 'section[aria-label="源健康度"]', "source-expanded")

        # ================= 场景 cred:credentials-only finding =================
        assert set_scenario("cred") == "cred"
        wait_dashboard(page, force=True)

        verdict_c = page.locator('[data-testid="dashboard-verdict"]')
        cred_text = verdict_c.inner_text()
        cred_asserts = {
            "text": cred_text,
            "2 项告警": "2 项告警" in cred_text,
            "5/5 源在线": "5/5 源在线" in cred_text,
            "tagName=A(warning 可点)": verdict_c.evaluate("(el) => el.tagName") == "A",
        }
        print(f"[assert:verdict-cred] {json.dumps(cred_asserts, ensure_ascii=False)}")
        for k, v in cred_asserts.items():
            if k not in ("text", "tagName=A(warning 可点)") and not v:
                failures.append(f"verdict-cred 缺 {k}")
        if not cred_asserts["tagName=A(warning 可点)"]:
            failures.append("verdict-cred(warning 态)不可点")
        shoot(page, "16-verdict-warning-cred", locator=verdict_c)
        results[-1]["asserts"] = cred_asserts
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-verdict"]', "verdict-cred")

        overview_c = page.locator('[data-testid="dashboard-overview"]')
        alerts_cell = page.locator('[data-testid="stat-alerts"]').inner_text()
        rows_c = page.evaluate(
            "() => Array.from(document.querySelectorAll('[data-testid^=\"alert-row-\"]')).map((el) => ({ id: el.getAttribute('data-testid'), text: (el.textContent || '').trim() }))"
        )
        overflow_c = page.locator('[data-testid="dashboard-alert-overflow"]').count()
        check("告警格=2", alerts_cell, "告警" in alerts_cell and "2" in alerts_cell)
        check(
            "凭据行型(error→异常 + warning→提醒)",
            rows_c,
            len(rows_c) == 2
            and "凭据" in rows_c[0]["text"] and "异常" in rows_c[0]["text"] and "缺少 TG_TOKEN 凭据" in rows_c[0]["text"]
            and "凭据" in rows_c[1]["text"] and "提醒" in rows_c[1]["text"] and "mail 凭据 30 天内到期" in rows_c[1]["text"],
        )
        check("2 行不溢出(≤3 无溢出口)", overflow_c, overflow_c == 0)
        shoot(page, "17-alert-cred-credentials", locator=overview_c)
        results[-1].update({"alertsCell": alerts_cell, "rows": rows_c, "overflowCount": overflow_c})
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-overview"]', "overview-cred")

        # ================= 场景 doctorfail:verdict unknown + 分区降级 =================
        assert set_scenario("doctorfail") == "doctorfail"
        wait_dashboard(page, force=True, categories=False)
        page.wait_for_selector('[data-testid="dashboard-section-errors"]', timeout=10000)

        verdict_u = page.locator('[data-testid="dashboard-verdict"]')
        unknown_text = verdict_u.inner_text()
        unknown_asserts = {
            "text": unknown_text,
            "部分数据不可达,状态未知": "部分数据不可达,状态未知" in unknown_text,
            "其余分区已降级显示": "其余分区已降级显示" in unknown_text,
            "tagName=DIV(unknown 不可点)": verdict_u.evaluate("(el) => el.tagName") == "DIV",
        }
        print(f"[assert:verdict-unknown] {json.dumps(unknown_asserts, ensure_ascii=False)}")
        for k, v in unknown_asserts.items():
            if k not in ("text", "tagName=DIV(unknown 不可点)") and not v:
                failures.append(f"verdict-unknown 缺 {k}")
        if not unknown_asserts["tagName=DIV(unknown 不可点)"]:
            failures.append("verdict-unknown(unknown 态)不应可点却可点")
        section_errors = page.locator('[data-testid="dashboard-section-errors"]').inner_text()
        check(
            "分区降级卡明文",
            section_errors.splitlines(),
            "部分数据不可用,已降级显示其余分区" in section_errors and "诊断/源健康度" in section_errors and "internal_error" in section_errors,
        )
        active_cell = page.locator('[data-testid="stat-active-sources"]').inner_text()
        check("活跃源格 — + 诊断不可达明文", active_cell.splitlines(), "—" in active_cell and "诊断不可达 · doctor 分区失败" in active_cell)
        alerts_cell_u = page.locator('[data-testid="stat-alerts"]').inner_text()
        check("告警格 —", alerts_cell_u.splitlines(), "—" in alerts_cell_u and "2" not in alerts_cell_u)
        doctor_rpc = [e for e in rpc_log(page) if e.get("method") == "doctor"]
        # StrictMode(main.tsx:14)dev 双跑 effect → doctor 调用两次,每次都应
        # 是 internal_error 拒绝值(分区降级的驱动事实,次数非事实)
        check(
            "doctor 分区错误回传",
            doctor_rpc,
            len(doctor_rpc) >= 1 and all(e.get("err") == "internal_error" for e in doctor_rpc),
        )

        clip_u = page.evaluate(
            CLIP_UNION_JS,
            ['[data-testid="dashboard-verdict"]', '[data-testid="dashboard-overview"]'],
        )
        assert "error" not in clip_u, clip_u
        shoot(page, "18-verdict-unknown-doctorfail", clip=clip_u)
        results[-1].update(
            {
                "asserts": unknown_asserts,
                "sectionErrors": section_errors.splitlines(),
                "activeCell": active_cell.splitlines(),
                "alertsCell": alerts_cell_u.splitlines(),
                "doctorRpc": doctor_rpc,
                "clip": clip_u,
            }
        )
        results[-1]["probe"] = probe(page, '[data-testid="dashboard-overview"]', "overview-doctorfail")
        results[-1]["probeVerdict"] = probe(page, '[data-testid="dashboard-verdict"]', "verdict-unknown")

        rpc_u = rpc_log(page)
        results.append({"shot": "(doctorfail rpc)", "rpcMethods": sorted({e["method"] for e in rpc_u})})

        browser.close()

    (EVIDENCE / "11-probe.json").write_text(
        json.dumps({"results": results, "failures": failures, "today": TODAY, "day6": DAY6}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"== S7 补批 11- 取证:shots=8 failures={len(failures)} ==")
    for f in failures:
        print(f"  FAIL: {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
