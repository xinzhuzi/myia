#!/usr/bin/env python3
"""采集日志屏无头冒烟(10-12;两级界面重做后的布局哨兵 + 动线验证)。

面板与注入(同 feed-card-smoke.py 骨架):
- 静态服务 ``desktop/ui`` 构建产物(与装机件同一构建链产物,HashRouter);
- Playwright chromium 无头直达 ``#/logs``,视口 1685×1057(主人实机档);
- IPC 注入 ``__TAURI_INTERNALS__.invoke``:version(protocol 13 读态门)/
  run.status(50 轮 DB 历史行夹具:35 成功/10 部分配置/5 失败,对齐实机
  状态分布;history=true + log_run_id 会话号)/ logs.tail(环形缓冲尾巴)。

夹具修正(10-12 R2,如实向 wire 真形对齐):
- 历史行 ``exit_code`` 保持 null(entry.py ``_history_run_rows`` 的 wire 真形
  恒 None;0/1/2/3 CLI 映射只适用注册表行——exit 语义词断言随此修正移出
  冒烟、落组件测试 logs-screen.test.tsx);
- 全部夹具行 record.stats 补 ``sources`` 数组(pipeline.py:592 形状
  source/failed/error;success 行全健康,partial/failed 行内各造一例
  failed:true 成员——stats 来自 _run_record_dict 落库 record,wire 真,
  喂 L1 摘要源段/失败段);
- failed 行(i=45..49,run_id 855..851)record.error 置真句 + logs.tail 对
  这些 run_id 恰回一行 stderr ``ERROR …``(喂失败合成第二/三源;夹具行
  log_run_id 在场,第三源可达);
- logs.tail 全部 run_id 回 TAIL_LINES=80 行(failed 行 ERROR 行埋 seq=40
  中段)——design §7 明文「冒烟双哨兵:两容器各自 scrollHeight > clientHeight」,
  L2 日志体内滚容器(run-log-{domId})要真溢出才可断言,2 行尾巴永远撑不出
  第二哨兵;80 行 × text-xs/leading-relaxed ≈ 1.5k px 对 L2 可用高 ≈ 800 px
  必然溢出,且更贴 52s 真实采集轮的日志量级(wire 真,不造假)。

断言面(design §9 编号顺序 + §6 testid 锚;布局哨兵性质保留):
- L1 直出:run-list 在场,50 摘要行;accordion 退役哨兵(run-group-header-*
  零命中 + run 行按钮无 aria-expanded);行高 ≥ 40px(min-h-11=44px 档,
  塌缩回归一票否决);容器内容溢出可滚(scrollHeight > clientHeight);
  默认不自动跳级(run-detail 不在场)+ 摘要可读(run-summary-h900 含
  「保留」「源」;run-summary-h855 含「失败 1 源」与 record.error 句);
- 两级动线:置 scrollTop=400 → 点 run-row-h855(failed 历史行,domIdOf
  规则带 h 前缀)进 L2 → 元信息头(run-detail-meta-h855 含 exit=— 与
  logs.tail run_id=855)→ 失败原因区(含 record.error 句与 exit=—,不含
  「无据」文案,stderr 摘行 run-failure-line-h855-0)→ ERROR 行高亮
  (data-error)→ L2 日志体第二塌缩哨兵(run-log-h855 溢出可滚)→ 返回钮
  回 L1(detail 卸载)→ 滚动位置保持(§4.2:写 400 → 进 → 返回 → ≥300)
  → 过滤态穿越保持(tech-rss 计数 10/50)→ 成功轮无失败区(h897 在 L2 中
  run-failure-* 零命中,AC2 渲染门槛)→ 无号遗留行降级(h851)→ 错误态满高
  算术(10-12-logs-line-low-polish G2/G5:置 run.status 故障 localStorage +
  重载 → 横幅上屏「sidecar 错误码 sidecar_not_running」+ 横幅自然高(<300px)
  + 满高算术(run-list clientHeight 缩量 ≈ 横幅高,±4px——编排层 flex 根下
  横幅+分支总高恒 = 容器高)。
  注:滚动保持断言(§9 步骤 9)骑全量列表往返——§4.2 明文钉「scrollTop 写
  400 → 进 → 返回 → ≥300」正是该循环;若骑过滤后往返,品类过滤只剩 10 行
  (≈550px)撑不满视口,scrollTop 物理钳到 0,断言必假红。

截图落 /tmp(L1/L2 各一)。退出码 0 = 冒烟通过。

背景(10-11 报障):瀑布流容器 = flex 列 + overflow-y-auto,子行无
shrink-0 —— 行数超过视口高时 flex 把每行均匀压扁(44px → ~14px),
内容被 overflow-hidden 裁没、滚动条永不出现。10-12 新 IA 下两内滚容器
(L1 run-list / L2 日志体)直接 flex 子项显式 shrink-0,本冒烟即双哨兵。

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
L1_SCREENSHOT = "/tmp/myssia-logs-screen-smoke-l1.png"
L2_SCREENSHOT = "/tmp/myssia-logs-screen-smoke-l2.png"

INJECT_SCRIPT = r"""
(() => {
  const iso = (ms) => new Date(ms).toISOString();
  // 50 轮历史行:35 success / 10 partial / 5 failed(对齐 10-11 实机分布;
  // failed 段 i=45..49 → run_id 855..851)
  const statuses = [
    ...Array(35).fill("success"),
    ...Array(10).fill("partial"),
    ...Array(5).fill("failed"),
  ];
  const categories = ["ai-news", "games-deals", "proxy-watch", "tech-rss", "urlwatch"];
  const FAILED_IDS = new Set([851, 852, 853, 854, 855]);
  const runs = statuses.map((status, i) => {
    const runId = 900 - i;
    const started = Date.now() - (i + 1) * 37 * 60_000;
    // record.stats.sources(pipeline.py:592 形状):success 全健康,
    // partial/failed 各造一例 failed:true 成员(摘要失败段真源)
    // 源行 = stats_dict 真形子集(10-12-run-detail-outcome 成果卡消费键齐备)
    const sources = [
      { source: "src-alpha", engine: "static_html", item_count: 8, duration_seconds: 1.9, skipped: false, skip_reason: null, failed: false, error: null },
      { source: "src-beta", engine: "direct_api", item_count: 7, duration_seconds: 0.4, skipped: false, skip_reason: null, failed: false, error: null },
      { source: "src-gamma", engine: "rss", item_count: 5, duration_seconds: 0.8, skipped: true, skip_reason: "engine_hint 首遇探测中", failed: false, error: null },
    ];
    if (status !== "success") {
      sources.push({ source: "src-delta", engine: "tg_web", item_count: 0, duration_seconds: 3.2, skipped: false, skip_reason: null, failed: true, error: "engine chain exhausted: timeout" });
    }
    const record = {
      run_id: runId,
      category: categories[i % categories.length],
      stats: { items_retained: 20 + (i % 7), sources },
    };
    if (status === "failed") {
      record.error = "RuntimeError: source fetch failed: timeout after 3 attempts";
    }
    return {
      run_id: runId,
      yaml: null,
      db: "/home/myssia.db",
      dry: false,
      state: "done",
      // 历史行 wire 真形恒 null(entry.py _history_run_rows);不假造 0/1/2/3
      exit_code: null,
      status,
      started_at: iso(started),
      finished_at: iso(started + 52_300),
      duration_ms: 52_300,
      record,
      history: true,
      // 最老一行(10-12-cron-run-log-alignment D5)置无号:真遗留行形态,
      // 2 级降级句断言用
      log_run_id: i === 49 ? null : runId,  // 49 = RUN_COUNT-1(JS 侧无 Python 常量)
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
        if (window.localStorage.getItem("smoke:run-status-fail") === "1") {
          // G2 错误态夹具(10-12-logs-line-low-polish):以 JSON 串拒答,
          // client.ts toSidecarError 解析为结构化 SidecarRequestError(code 走
          // 横幅「sidecar 错误码」槽)——冒烟尾段置 localStorage + 重载触发
          // (window 旗标扛不住 reload,localStorage 才是跨导航载具;屏内已无
          // 刷新钮——PageHeader 2026-10-04「无头」指令起渲染 null)
          throw JSON.stringify({ code: "sidecar_not_running", path: "$", message: "smoke 注入:sidecar 未运行" });
        }
        return { runs };
      }
      if (method === "store.items") {
        // 成果区条目预览(10-12-run-detail-outcome):窗内一条 + 窗外一条
        // (h855 = i 45 → ai-news,started ≈ 28h 前,finished = started+52s)
        const h855Started = Date.now() - 46 * 37 * 60_000;
        const mk = (id, title, seenMs) => ({
          id, url: "https://example.com/" + id, dedup_key: "dk-" + id, title,
          source: "src-alpha", content: null, pushed_at: null, push_slot: null,
          first_seen: iso(seenMs), read: false, starred: false, later: false,
        });
        const items = [
          mk(1, "窗内条目:新一轮采集成果预览甲", h855Started + 10_000),
          mk(2, "窗外条目:后继轮不应混入", Date.now() - 60_000),
        ];
        const filtered = params?.since
          ? items.filter((it) => it.first_seen >= params.since)
          : items;
        return { db: "smoke.db", count: filtered.length, items: filtered };
      }
      if (method === "logs.tail") {
        const runId = params?.run_id ?? 0;
        const total = 80;
        const lines = [];
        for (let seq = 1; seq <= total; seq += 1) {
          if (FAILED_IDS.has(runId) && seq === 40) {
            // 恰一行 stderr 错误行:喂失败合成第三源(isRowError 双信号)+
            // L2 data-error 高亮 + run-failure-line-* 摘条目
            lines.push({ seq, ts: iso(Date.now() - 60_000), run_id: runId, stream: "stderr", line: "ERROR source fetch failed: timeout after 3 attempts" });
          } else {
            lines.push({ seq, ts: iso(Date.now() - 60_000 + seq * 600), run_id: runId, stream: "stdout", line: "[run " + runId + "] step " + seq + ": fetch ok, retained " + (10 + (seq % 9)) + " items" });
          }
        }
        return { lines, total, truncated: false };
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

            # ── 1. L1 直出:50 摘要行(accordion 折叠退役,run-waterfall 改名 run-list)
            await page.wait_for_selector('[data-testid="run-list"]', timeout=10_000)
            await page.wait_for_selector('[data-testid="run-row-h900"]', timeout=10_000)
            expect(
                "50 摘要行直出(accordion 折叠退役)",
                (await page.locator('[data-testid^="run-row-"]').count()) == RUN_COUNT,
            )

            # ── 2. accordion 退役哨兵:旧折叠组头 testid 零命中 + 行按钮无
            #       aria-expanded(design §6:run-row-* 取代 run-group-header-*)
            leftover_headers = await page.locator('[data-testid^="run-group-header-"]').count()
            aria_expanded = await page.evaluate(
                """() => Array.from(
                    document.querySelectorAll('[data-testid^="run-row-"]'),
                    (el) => el.hasAttribute("aria-expanded"),
                ).filter(Boolean).length"""
            )
            expect(
                f"accordion 退役(run-group-header-* = {leftover_headers},aria-expanded 行数 = {aria_expanded})",
                leftover_headers == 0 and aria_expanded == 0,
            )

            # ── 3. 行高哨兵:逐行 min ≥ 40px(min-h-11 = 44px;塌缩回归一票否决)
            heights = await page.evaluate(
                """() => Array.from(
                    document.querySelectorAll('[data-testid^="run-row-"]'),
                    (el) => el.getBoundingClientRect().height,
                )"""
            )
            print(f"metrics - 摘要行高 min={min(heights):.1f}px max={max(heights):.1f}px n={len(heights)}")
            expect(f"行高 ≥ 40px(实测 min={min(heights):.1f}px)", min(heights) >= 40)

            # ── 4. 可滚哨兵:run-list 内容溢出必须可滚(压扁回归 = scrollHeight==clientHeight)
            scroll = await page.evaluate(
                """() => {
                    const el = document.querySelector('[data-testid="run-list"]');
                    return { sh: el.scrollHeight, ch: el.clientHeight };
                }"""
            )
            print(f"metrics - run-list scrollHeight={scroll['sh']} clientHeight={scroll['ch']}")
            expect(
                f"run-list 内容溢出可滚(scrollHeight {scroll['sh']} > clientHeight {scroll['ch']})",
                scroll["sh"] > scroll["ch"] + 100,
            )

            # ── 5. 不自动跳级哨兵 + 摘要可读(AC1:成功轮成果段+源段;失败行
            #       摘要带「失败 K 源」dead 段与 record.error 句,design §2.2)
            expect(
                "默认不自动跳级(run-detail 不在场)",
                (await page.locator('[data-testid="run-detail"]').count()) == 0,
            )
            summary_h900 = await page.locator('[data-testid="run-summary-h900"]').inner_text()
            print(f"metrics - run-summary-h900 = {summary_h900!r}")
            expect("h900 摘要非空且含「保留」与「源」", bool(summary_h900.strip()) and "保留" in summary_h900 and "源" in summary_h900)
            summary_h855 = await page.locator('[data-testid="run-summary-h855"]').inner_text()
            print(f"metrics - run-summary-h855 = {summary_h855!r}")
            expect(
                "h855 摘要含失败源段与 error 句(失败语义片段)",
                "失败 1 源" in summary_h855 and "RuntimeError: source fetch failed: timeout after 3 attempts" in summary_h855,
            )

            # ── 6. 截图 L1(AC4 双图之一)
            await page.screenshot(path=L1_SCREENSHOT, full_page=False)
            print(f"screenshot: {L1_SCREENSHOT}")

            # ── 7. 进 2 级:置滚动位(为滚动保持断言铺垫)→ 点 failed 历史行
            #       (夹具全 history:true,domIdOf 规则带 h 前缀,裸号必空匹配)
            await page.evaluate("() => { document.querySelector('[data-testid=\"run-list\"]').scrollTop = 400; }")
            await page.click('[data-testid="run-row-h855"]')
            await page.wait_for_selector('[data-testid="run-detail"]', timeout=10_000)
            expect("点行进 2 级(run-detail 在场)", True)

            # ── 7a. 元信息头事实簇(design §3.1/§6):exit=—(历史行 wire 真形
            #        恒 null)+ logs.tail 会话对齐号如实报
            meta_h855 = await page.locator('[data-testid="run-detail-meta-h855"]').inner_text()
            print(f"metrics - run-detail-meta-h855 = {meta_h855!r}")
            expect(
                "元信息头含 exit=— 与 logs.tail run_id=855",
                "exit=—" in meta_h855 and "logs.tail run_id=855" in meta_h855,
            )

            failure_panel = page.locator('[data-testid="run-failure-h855"]')
            await failure_panel.wait_for(timeout=10_000)
            panel_text = await failure_panel.inner_text()
            print(f"metrics - run-failure-h855 = {panel_text!r}")
            expect(
                "失败区含 record.error 句与 exit=—(历史行 wire 真形)",
                "RuntimeError: source fetch failed: timeout after 3 attempts" in panel_text and "exit=—" in panel_text,
            )
            expect("失败区不含「无据」文案(此轮有据)", "暂无结构化失败记录" not in panel_text)
            stderr_excerpt = page.locator('[data-testid="run-failure-line-h855-0"]')
            expect(
                "失败区 stderr 错误行摘第 1 条在场",
                (await stderr_excerpt.count()) == 1
                and "ERROR source fetch failed" in (await stderr_excerpt.inner_text()),
            )
            await page.wait_for_selector('[data-testid="log-row"]', timeout=10_000)
            expect(
                "日志行 ERROR 行 data-error 高亮",
                (await page.locator('[data-testid="log-row"][data-error="true"]').count()) >= 1,
            )

            # ── 7a. 采集成果区(10-12-run-detail-outcome):「本轮采集到了什么」──
            outcome_h855 = await page.locator('[data-testid="run-outcome-h855"]').inner_text()
            expect(
                "L2 成果区:保留 N 条 + 源行(引擎/条数)+ 跳过与失败如实",
                "保留" in outcome_h855
                and "src-alpha" in outcome_h855
                and "8 条" in outcome_h855
                and "跳过" in outcome_h855
                and "src-delta" in outcome_h855
                and "失败" in outcome_h855,
            )
            preview_h855 = await (await page.wait_for_selector('[data-testid="run-outcome-preview-h855"]', timeout=10_000)).inner_text()
            expect(
                "L2 条目预览:窗内标题在场,窗外条目被 finishedAt 截窗剔除",
                "窗内条目" in preview_h855 and "窗外条目" not in preview_h855,
            )

            # ── 7b. L2 日志体第二塌缩哨兵(design §7 双哨兵后半):内滚容器
            #        内容溢出必须可滚(80 行夹具真溢出;压扁/内滚帽回归在此暴露)
            try:
                await page.wait_for_function(
                    """() => {
                        const el = document.querySelector('[data-testid="run-log-h855"]');
                        return el !== null && el.scrollHeight > el.clientHeight + 100;
                    }""",
                    timeout=10_000,
                )
                log_scroll = await page.evaluate(
                    """() => {
                        const el = document.querySelector('[data-testid="run-log-h855"]');
                        return { sh: el.scrollHeight, ch: el.clientHeight };
                    }"""
                )
                expect(
                    f"run-log-h855 内容溢出可滚(scrollHeight {log_scroll['sh']} > clientHeight {log_scroll['ch']})",
                    True,
                )
            except Exception:
                log_scroll = await page.evaluate(
                    """() => {
                        const el = document.querySelector('[data-testid="run-log-h855"]');
                        return el ? { sh: el.scrollHeight, ch: el.clientHeight } : null;
                    }"""
                )
                expect(f"run-log-h855 内容溢出可滚(实测 {log_scroll!r})", False)

            # 截图 L2(AC4 双图之二)
            await page.screenshot(path=L2_SCREENSHOT, full_page=False)
            print(f"screenshot: {L2_SCREENSHOT}")

            # ── 8+10. 返回钮回 1 级 + 滚动位置保持(§4.2 钉死循环:写 400 → 进
            #        → 返回 → ≥300;Playwright 点行会自动滚到 h855 行,捕存值
            #        只会更大,≥300 判据稳)
            await page.click('[data-testid="run-back"]')
            await page.wait_for_selector('[data-testid="run-detail"]', state="detached", timeout=10_000)
            expect("返回钮回 1 级(run-detail 卸载)", True)
            try:
                await page.wait_for_function(
                    """() => {
                        const el = document.querySelector('[data-testid="run-list"]');
                        return el !== null && el.scrollTop >= 300;
                    }""",
                    timeout=5_000,
                )
                restored = await page.evaluate(
                    "() => document.querySelector('[data-testid=\"run-list\"]').scrollTop"
                )
                expect(f"滚动位置保持(返回后 scrollTop={restored} ≥ 300)", True)
            except Exception:
                restored = await page.evaluate(
                    "() => document.querySelector('[data-testid=\"run-list\"]')?.scrollTop ?? -1"
                )
                expect(f"滚动位置保持(返回后 scrollTop={restored} ≥ 300)", False)

            # ── 9. 过滤态保持 + 成功轮无失败区(AC2 渲染门槛 + AC3 过滤穿越):
            #       开品类过滤(Radix select 无头可点,feed/源管理既有用例同法)
            #       → 选 tech-rss → 计数读数 → 点过滤集首行 run-row-h897(最新
            #       tech-rss 轮:i%5==3 → i=3 → run_id 897,status success,一石
            #       二鸟验「成功轮 run-failure-* 零命中」)→ Esc 回 → 计数同读数
            await page.click('[data-testid="filter-category"]')
            await page.wait_for_selector('[role="option"]', timeout=10_000)
            await page.get_by_role("option", name="tech-rss").click()
            count_text = await page.locator('[data-testid="logs-filter-count"]').inner_text()
            print(f"metrics - 过滤后计数 = {count_text!r}")
            expect(f"品类过滤计数 = {count_text!r}(tech-rss 10 轮)", count_text.strip() == "10 / 50 轮")

            await page.click('[data-testid="run-row-h897"]')
            await page.wait_for_selector('[data-testid="run-detail"]', timeout=10_000)
            expect(
                "成功轮无失败区(h897 success → run-failure-* 零命中)",
                (await page.locator('[data-testid^="run-failure-"]').count()) == 0,
            )
            await page.keyboard.press("Escape")
            await page.wait_for_selector('[data-testid="run-detail"]', state="detached", timeout=10_000)
            expect("Esc 回 1 级(过滤态穿越)", True)
            count_after = await page.locator('[data-testid="logs-filter-count"]').inner_text()
            expect(
                f"返回后过滤计数保持({count_after!r} == {count_text!r})",
                count_after.strip() == count_text.strip(),
            )

            # ═══ 无号遗留行(D5):2 级如实降级,不拉 logs.tail ═══
            # (先清过滤:上段 tech-rss 过滤态保持是被测特性,h851=urlwatch 会被滤掉)
            await page.get_by_role("button", name="清除过滤").click()
            await page.wait_for_selector('[data-testid="run-row-h851"]', timeout=10_000)
            null_row = page.locator('[data-testid="run-row-h851"]')
            await null_row.scroll_into_view_if_needed()
            await null_row.click()
            await page.wait_for_selector('[data-testid="run-detail-meta-h851"]', timeout=10_000)
            detail_text = await page.locator('[data-testid="run-log-h851"]').text_content()
            expect(
                "无号行降级句(D5 文案,去时间断言)",
                "未记录日志会话号" in (detail_text or "") and "早于" not in (detail_text or ""),
            )
            expect("无号行零日志行", (await page.locator('[data-testid="run-log-h851"] [data-testid="log-row"]').count()) == 0)
            await page.locator('[data-testid="run-back"]').click()
            await page.wait_for_selector('[data-testid="run-list"]', timeout=10_000)

            # ═══ 错误态满高算术(10-12-logs-line-low-polish G2/G5):置故障
            #      localStorage → 重载 → 首载 run.status 结构化拒答 → 横幅上屏
            #      (run 集为空,L1 空态卡;flex 链高度与内容无关,算术可断);
            #      断言 ① 结构化错误码如实上屏 ② 横幅自然高(<300px)
            #      ③ 满高算术:run-list clientHeight 缩量 ≈ 横幅高(旧 fragment
            #      根下 h-full 分支与横幅成兄弟会溢出容器 100%+横幅高,新 flex
            #      根恒 = 容器高)═══
            list_before = await page.evaluate(
                "() => document.querySelector('[data-testid=\"run-list\"]').clientHeight"
            )
            await page.evaluate("() => localStorage.setItem('smoke:run-status-fail', '1')")
            await page.reload(wait_until="networkidle")
            banner = page.locator('[data-testid="logs-error"]')
            await banner.wait_for(timeout=10_000)
            await page.wait_for_selector('[data-testid="run-list"]', timeout=10_000)
            banner_text = await banner.inner_text()
            print(f"metrics - logs-error = {banner_text!r}")
            expect(
                "错误横幅上屏(结构化错误码 sidecar_not_running 如实报)",
                "采集日志不可用" in banner_text and "sidecar_not_running" in banner_text,
            )
            err_metrics = await page.evaluate(
                """() => {
                    const banner = document.querySelector('[data-testid="logs-error"]');
                    const list = document.querySelector('[data-testid="run-list"]');
                    return {
                        bh: banner.getBoundingClientRect().height,
                        ch: list.clientHeight,
                    };
                }"""
            )
            print(
                "metrics - 错误态 banner="
                f"{err_metrics['bh']:.1f}px run-list clientHeight={err_metrics['ch']}(无横幅时 {list_before})"
            )
            expect(
                f"横幅自然高(banner {err_metrics['bh']:.1f}px < 300px,不吞列表区)",
                0 < err_metrics["bh"] < 300,
            )
            shrink = list_before - err_metrics["ch"]
            expect(
                f"满高算术(run-list 缩量 {shrink}px ≈ 横幅高 {err_metrics['bh']:.1f}px,容差 4px)",
                abs(shrink - err_metrics["bh"]) <= 4,
            )
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
