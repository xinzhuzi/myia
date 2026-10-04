// b234-smoke-drive.cjs — 10-04-desktop-b234 无头 GUI 冒烟(法 = 10-03-detail-images
// evidence/app-headless/di-smoke-drive.cjs 先例:vite dev + 真源码 sidecar bridge +
// Playwright headless chromium + __TAURI_INTERNALS__ shim)。
//
// 覆盖(对应 prd AC):
//   P0 协议往返(真 sidecar spawn):runs.trend 聚合/钳制/过滤 + store.trend +
//      feedback.stats 基线 + 方法注册面(runs.trend 在 allowed);
//   B2  feed 卡片 👍(aria-pressed+置灰)→ feedback.list/stats 往返(channel=desktop)
//      + 仪表盘反馈统计卡计数;
//   B3  settings EnrichFeedbackCard 开关 → yaml.save 写回 → 磁盘 enrich.enabled 往返
//      + .bak 留底 + 回拨复原;
//   B4/G6 仪表盘双折线:trend-total 文案 + SVG polyline points 与种子真数据逐点对算
//      (公式 = sparkline.tsx sparkPoints,width 260/height 48/pad 3)+ 7 天窗切换双查
//      + 成功率累计摘要(57% 4/7)与「近期 run 成功率」卡(40%,内存合并口径)差异实录。
// 数据通路全真:零 mock、零 route 拦截;夹具库经 MYIA_HOME=/tmp/myia-b234-e2e/home
// 由 serve 上下文缺省解析(比 shim 注 params.db 更贴真壳)。
const { chromium } = require("/Users/zhengbingjin/.npm/_npx/705bc6b22212b352/node_modules/playwright");
const fs = require("fs");
const path = require("path");

const BASE = "http://localhost:5222";
const BRIDGE = "http://127.0.0.1:54119";
const FIXTURE_YAML = "/tmp/myia-b234-e2e/home/plugins/ai-news.yaml";
const OUT = "/Users/zhengbingjin/Project/Github/MYIA/.trellis/tasks/10-04-desktop-b234/evidence/headless";

const steps = [];
const consoleErrors = [];
function record(name, ok, evidence, screenshot) {
  steps.push({ name, ok, evidence, screenshot: screenshot ?? null });
  console.log(`[${ok ? "PASS" : "FAIL"}] ${name} :: ${String(evidence).slice(0, 600)}`);
}

async function rpc(method, params) {
  const res = await fetch(`${BRIDGE}/rpc`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ method, params: params ?? {} }),
  });
  if (!res.ok) throw new Error(`bridge HTTP ${res.status}`);
  return res.json();
}

// sparkline.tsx sparkPoints(:50-57)的文档公式复刻——期望几何由种子真数据算出
function expectedPoints(values, width = 260, height = 48, pad = 3, domainMax) {
  const max = domainMax !== undefined && domainMax > 0 ? domainMax : Math.max(...values, 0);
  const spanX = width - pad * 2;
  const spanY = height - pad * 2;
  return values
    .map((value, index) => ({
      x: values.length === 1 ? width / 2 : pad + (spanX * index) / (values.length - 1),
      y: max === 0 ? height / 2 : pad + spanY * (1 - value / max),
    }))
    .map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`)
    .join(" ");
}

const SEED = {
  trendCounts14: [0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 3, 0, 0, 5],
  trendCounts7: [0, 0, 0, 3, 0, 0, 5],
  rates: [0.0, 1.0, 0.75],
};

const SHIM = `
(() => {
  const BRIDGE = ${JSON.stringify(BRIDGE)};
  let cbSeq = 0;
  const invoke = async (cmd, args = {}, options) => {
    if (cmd === "sidecar_request") {
      const method = args && args.method;
      const params = Object.assign({}, (args && args.params) || {});
      let res;
      try {
        res = await fetch(BRIDGE + "/rpc", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ method, params }),
        });
      } catch (e) {
        throw JSON.stringify({ code: "transport_error", path: "$", message: "smoke bridge 不可达: " + e });
      }
      if (res.status === 503) throw JSON.stringify({ code: "sidecar_not_running", path: "$", message: "bridge 503" });
      if (!res.ok) throw JSON.stringify({ code: "transport_error", path: "$", message: "bridge HTTP " + res.status });
      const msg = await res.json();
      if (msg && msg.error) throw JSON.stringify(msg.error);
      return msg.result;
    }
    if (cmd === "plugin:event|listen" || cmd === "plugin:event|unlisten") return 0;
    if (cmd === "plugin:app|version") return "0.0.1-smoke";
    throw JSON.stringify({ code: "unsupported_command", path: "$", message: "smoke shim 未实现命令: " + cmd });
  };
  window.__TAURI_INTERNALS__ = {
    invoke,
    transformCallback: (cb, once) => ++cbSeq,
    unregisterCallback: () => {},
    metadata: { currentWindow: { label: "main" }, currentWebview: { label: "main" } },
  };
  // @tauri-apps/api/event.js:100 _unlisten 走此对象(缺则路由切换清理时 pageerror)
  window.__TAURI_EVENT_PLUGIN_INTERNALS__ = { unregisterListener: () => {} };
})();
`;

function yamlEnrichEnabled(text) {
  const idx = text.indexOf("\nenrich:");
  if (idx < 0) return null;
  const chunk = text.slice(idx, idx + 600);
  const m = chunk.match(/enabled:\s*(true|false)/);
  return m ? m[1] : null;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1680, height: 1050 } });
  page.on("console", (m) => { if (m.type() === "error") consoleErrors.push(m.text().slice(0, 300)); });
  page.on("pageerror", (e) => consoleErrors.push("pageerror: " + String(e).slice(0, 300)));
  await page.addInitScript(SHIM);

  // ---------------- P0 协议往返(真 sidecar spawn) ----------------
  const alive = await rpc("run.status", {});
  record(
    "P0:真 sidecar spawn(run.status 空注册表应答)",
    alive?.result?.runs !== undefined && Array.isArray(alive.result.runs),
    JSON.stringify(alive).slice(0, 200),
  );

  const unknown = await rpc("definitely.not.a.method", {});
  const allowed = unknown?.error?.data?.allowed ?? [];
  record(
    "P0:方法注册面 runs.trend 在 method_not_found.allowed(共 " + allowed.length + " 方法)",
    unknown?.error?.code === "method_not_found" && allowed.includes("runs.trend")
      && allowed.includes("feedback.mark") && allowed.includes("store.trend"),
    `code=${unknown?.error?.code};allowed=${allowed.length};含 runs.trend=${allowed.includes("runs.trend")}`,
  );

  const trend = await rpc("runs.trend", { days: 14 });
  const days14 = trend.result?.days ?? [];
  const byDate = Object.fromEntries(days14.map((d) => [d.date, d]));
  const todayIso = new Date().toISOString().slice(0, 10);
  const ydayIso = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const d3Iso = new Date(Date.now() - 3 * 86400000).toISOString().slice(0, 10);
  const d40Iso = new Date(Date.now() - 40 * 86400000).toISOString().slice(0, 10);
  const datesSorted = JSON.stringify(days14.map((d) => d.date)) === JSON.stringify([...days14.map((d) => d.date)].sort());
  const stOk = (d, want) => {
    if (!d) return false;
    const s = d.statuses ?? {};
    return Object.keys(s).length === Object.keys(want).length
      && Object.entries(want).every(([k, v]) => s[k] === v);
  };
  record(
    "P0:runs.trend days=14 聚合(今天 3s+1f+1r / 昨天 1s+1r / 3 天前 2f;旧→新)",
    datesSorted
      && byDate[todayIso]?.total === 5
      && stOk(byDate[todayIso], { success: 3, failed: 1, running: 1 })
      && byDate[ydayIso]?.total === 2
      && stOk(byDate[ydayIso], { success: 1, running: 1 })
      && byDate[d3Iso]?.total === 2
      && stOk(byDate[d3Iso], { failed: 2 })
      && byDate[d40Iso] === undefined,
    `dates=${JSON.stringify(days14.map((d) => d.date + ":" + JSON.stringify(d.statuses)))}`,
  );

  const clamp0 = await rpc("runs.trend", { days: 0 });
  const clamp91 = await rpc("runs.trend", { days: 91 });
  const catDemo = await rpc("runs.trend", { days: 14, category: "ai-news" });
  const catNone = await rpc("runs.trend", { days: 14, category: "no-such-category" });
  const badDays = await rpc("runs.trend", { days: "7" });
  record(
    "P0:runs.trend 钳制/过滤/形状(days0→仅今天、91→含 40 天前 partial、category 过滤、非 int 拒)",
    JSON.stringify(clamp0.result?.days?.map((d) => d.date)) === JSON.stringify([todayIso])
      && (clamp91.result?.days ?? []).some((d) => d.date === d40Iso && d.statuses.partial === 1)
      && catDemo.result?.days?.length === days14.length
      && catNone.result?.days?.length === 0
      && badDays?.error?.code === "invalid_params",
    `days0=${JSON.stringify(clamp0.result?.days?.map((d) => d.date))};91 含 d40 partial=${(clamp91.result?.days ?? []).some((d) => d.date === d40Iso)};cat none=${catNone.result?.days?.length};days"7" err=${badDays?.error?.code}`,
  );

  const storeTrend = await rpc("store.trend", { days: 14 });
  const sDays = storeTrend.result?.days ?? [];
  const sBy = Object.fromEntries(sDays.map((d) => [d.date, d.count]));
  record(
    "P0:store.trend days=14(10 天前 7 / 3 天前 3 / 今天 5,旧→新)",
    sBy[new Date(Date.now() - 10 * 86400000).toISOString().slice(0, 10)] === 7
      && sBy[d3Iso] === 3 && sBy[todayIso] === 5 && sDays.length === 3,
    JSON.stringify(sDays),
  );

  const statsBefore = await rpc("feedback.stats", { window_days: 14 });
  record(
    "P0:feedback.stats 基线(既有 CLI good×1)",
    statsBefore.result?.stats?.total === 1 && statsBefore.result?.stats?.good === 1
      && JSON.stringify(statsBefore.result?.stats?.by_channel) === JSON.stringify({ cli: 1 }),
    JSON.stringify(statsBefore.result?.stats).slice(0, 200),
  );

  // ---------------- B2:feed 卡片 👍 + feedback 往返 ----------------
  await page.goto(`${BASE}/#/feed`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid^="feed-item-"]', { timeout: 45000 });
  await page.waitForTimeout(1200);
  // 目标行 = 含种子标题的 feed-item 行(Playwright hasText 过滤,不再手写 closest)
  const row = page.locator('[data-testid^="feed-item-"]', { hasText: "B234 冒烟反馈条目" }).first();
  const rowVisible = await row.isVisible().catch(() => false);
  const fbSpan = row.locator('[data-testid^="feed-feedback-"]').first();
  const upBtn = fbSpan.getByRole("button", { name: "好评" });
  const upBefore = await upBtn.getAttribute("aria-pressed");
  const enabledBefore = await upBtn.isEnabled();
  await upBtn.click();
  let pressedNow = false;
  let disabledNow = false;
  for (let i = 0; i < 40; i += 1) {
    pressedNow = (await upBtn.getAttribute("aria-pressed")) === "true";
    disabledNow = await upBtn.isDisabled();
    if (pressedNow && disabledNow) break;
    await page.waitForTimeout(500);
  }
  const fbSpanText = await fbSpan.innerText().catch(() => "");
  await page.screenshot({ path: path.join(OUT, "b2-feed-marked.png"), fullPage: true });
  record(
    "B2:feed 卡片 👍 标记(aria-pressed=true + 置灰防重)",
    rowVisible && upBefore === "false" && enabledBefore === true && pressedNow && disabledNow,
    `目标行可见=${rowVisible};点击前 pressed=${upBefore}/enabled=${enabledBefore};点击后 pressed=${pressedNow}+disabled=${disabledNow};span 文本="${fbSpanText.trim().slice(0, 80)}"`,
    "b2-feed-marked.png",
  );

  const fbList = await rpc("feedback.list", {});
  const newest = fbList.result?.items?.[0];
  record(
    "B2:feedback.mark→list 往返(channel=desktop,dedup_key=b234-smoke-key-1)",
    fbList.result?.count === 2 && newest?.channel === "desktop"
      && newest?.dedup_key === "b234-smoke-key-1" && newest?.verdict === "good"
      && fbList.result.items[1]?.channel === "cli",
    JSON.stringify(fbList.result?.items),
  );
  const statsAfter = await rpc("feedback.stats", { window_days: 14 });
  const sa = statsAfter.result?.stats ?? {};
  record(
    "B2:feedback.stats 标记后(cli1+desktop1 → good=2)",
    sa.total === 2 && sa.good === 2 && sa.by_channel?.cli === 1 && sa.by_channel?.desktop === 1
      && Object.keys(sa.by_channel ?? {}).length === 2,
    JSON.stringify(sa).slice(0, 200),
  );

  // ---------------- B3:settings EnrichFeedbackCard 开关往返 ----------------
  const yaml0 = fs.readFileSync(FIXTURE_YAML, "utf8");
  const enabled0 = yamlEnrichEnabled(yaml0);
  await page.goto(`${BASE}/#/settings`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="enrich-feedback-card"]', { timeout: 60000 });
  await page.waitForSelector('[data-testid^="enrich-row-"]', { timeout: 60000 });
  await page.waitForTimeout(800);
  const enrichSwitch = page.getByRole("switch", { name: /ai-news\.yaml/ });
  await enrichSwitch.waitFor({ timeout: 20000 });
  const checked0 = await enrichSwitch.getAttribute("aria-checked");
  await page.screenshot({ path: path.join(OUT, "b3-enrich-before.png"), fullPage: true });
  await enrichSwitch.click();
  await page.waitForFunction(
    () => {
      const status = document.querySelector('[data-testid="enrich-save-status"]');
      const sw = document.querySelector('[role="switch"][aria-label*="ai-news.yaml"]');
      return status && (status.textContent || "").includes("停用") && sw && sw.getAttribute("aria-checked") === "false";
    },
    { timeout: 30000 },
  );
  await page.screenshot({ path: path.join(OUT, "b3-enrich-disabled.png"), fullPage: true });
  const yaml1 = fs.readFileSync(FIXTURE_YAML, "utf8");
  const enabled1 = yamlEnrichEnabled(yaml1);
  const bakExists = fs.existsSync(FIXTURE_YAML + ".bak");
  const statusText1 = await page.locator('[data-testid="enrich-save-status"]').textContent();
  record(
    "B3:enrich.enabled 开关 → yaml.save 写回磁盘 false + doctor 复核回显 + .bak 留底",
    checked0 === "true" && enabled0 === "true" && enabled1 === "false" && bakExists,
    `开关 ${checked0}→false;磁盘 enrich.enabled ${enabled0}→${enabled1};.bak=${bakExists};状态行="${(statusText1 || "").trim().slice(0, 120)}"`,
    "b3-enrich-disabled.png",
  );

  await page.getByRole("switch", { name: /ai-news\.yaml/ }).click();
  await page.waitForFunction(
    () => {
      const status = document.querySelector('[data-testid="enrich-save-status"]');
      const sw = document.querySelector('[role="switch"][aria-label*="ai-news.yaml"]');
      return status && (status.textContent || "").includes("启用") && sw && sw.getAttribute("aria-checked") === "true";
    },
    { timeout: 30000 },
  );
  const enabled2 = yamlEnrichEnabled(fs.readFileSync(FIXTURE_YAML, "utf8"));
  record(
    "B3:回拨复原(enrich.enabled → true)",
    enabled2 === "true",
    `磁盘 enrich.enabled=${enabled2};开关 aria-checked=true`,
  );

  // ---------------- B4/G6:仪表盘双折线(数据源 = 种子真数据) ----------------
  await page.goto(`${BASE}/#/`, { waitUntil: "domcontentloaded" });
  await page.waitForSelector('[data-testid="dashboard-rate-sparkline"] polyline', { timeout: 60000 });
  await page.waitForSelector('[data-testid="dashboard-sparkline"] polyline', { timeout: 30000 });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: path.join(OUT, "b4-g6-dashboard-14d.png"), fullPage: true });

  const trendTotal14 = (await page.locator('[data-testid="trend-total"]').textContent())?.trim();
  record(
    "B4:采集量趋势摘要(近 14 天共 15 条 · 峰值 7 条/日;种子 7+3+5)",
    trendTotal14 === "近 14 天共 15 条 · 峰值 7 条/日",
    `trend-total="${trendTotal14}"`,
    "b4-g6-dashboard-14d.png",
  );

  const countsPoints14 = await page.locator('[data-testid="dashboard-sparkline"] polyline').getAttribute("points");
  const expectCounts14 = expectedPoints(SEED.trendCounts14);
  record(
    "B4:采集量 sparkline SVG polyline 与种子真数据逐点对算(14 点,max=7 归一)",
    countsPoints14 === expectCounts14,
    `rendered="${countsPoints14}"\nexpected="${expectCounts14}"`,
  );

  const ratePoints14 = await page.locator('[data-testid="dashboard-rate-sparkline"] polyline').getAttribute("points");
  const expectRates = expectedPoints(SEED.rates, 260, 48, 3, 1);
  const rateSvgArea = await page.locator('[data-testid="dashboard-rate-sparkline"] polygon').count();
  record(
    "G6:成功率 sparkline 固定 [0,1] 刻度逐点对算(3 点 [0,1,0.75],max=1,area=false)",
    ratePoints14 === expectRates && rateSvgArea === 0,
    `rendered="${ratePoints14}"\nexpected="${expectRates}";polygon(渐变填充)=${rateSvgArea}`,
  );

  const rateSummary = (await page.locator('[data-testid="rate-summary"]').textContent())?.replace(/\s+/g, " ").trim();
  record(
    "G6:累计成功率摘要(57% = 4/7;零完结日不入线)",
    rateSummary === "近 14 天累计成功率 57%(4/7 次成功)",
    `rate-summary="${rateSummary}"`,
  );

  const rateAria = await page.locator('[data-testid="dashboard-rate-sparkline"]').getAttribute("aria-label");
  record(
    "G6:成功率 sparkline aria 累计口径 + 「不含进行中」口径注记在卡面",
    (rateAria || "").includes("近 14 天累计成功率 57%(4/7 次成功)") && (rateAria || "").includes("无完结 run 的日子不入线")
      && (await page.locator('[data-testid="dashboard-rate-section"]').innerText()).includes("不含进行中"),
    `aria-label="${rateAria}"`,
  );

  const errCount = await page.locator('[data-testid="dashboard-trend-error"], [data-testid="dashboard-rate-error"], [data-testid="dashboard-rate-empty"]').count();
  record(
    "B4/G6:趋势区零错误零空态(双序列都画出来了)",
    errCount === 0,
    `trend-error/rate-error/rate-empty 命中数=${errCount}`,
  );

  const cardRate = (await page.locator('[data-testid="run-success-rate"]').textContent())?.trim();
  record(
    "G6 口径差异实录:「近期 run 成功率」卡(runs.list 内存合并)=40% ≠ 趋势 57%(表内 status 口径)",
    cardRate === "40%",
    `run-success-rate 卡="${cardRate}"(10 行含 2 行僵尸 running 全算完结 → 4/10);趋势卡 57%(4/7,running 不入分母)——两口径卡面各自如实,不冒充同源`,
  );

  const fbGood = (await page.locator('[data-testid="feedback-good"]').textContent())?.trim();
  const fbBad = (await page.locator('[data-testid="feedback-bad"]').textContent())?.trim();
  record(
    "B2:仪表盘反馈统计卡计数(good=2 cli+desktop / bad=0)",
    fbGood === "2" && fbBad === "0",
    `feedback-good="${fbGood}";feedback-bad="${fbBad}"`,
  );

  // 窗口切换 7 天:两序列同窗重查
  await page.locator('[aria-label="趋势时间范围"]').click();
  await page.getByRole("option", { name: "7 天" }).click();
  await page.waitForFunction(
    () => (document.querySelector('[data-testid="trend-total"]')?.textContent || "").includes("近 7 天"),
    { timeout: 30000 },
  );
  await page.waitForTimeout(600);
  await page.screenshot({ path: path.join(OUT, "b4-g6-dashboard-7d.png"), fullPage: true });
  const trendTotal7 = (await page.locator('[data-testid="trend-total"]').textContent())?.trim();
  const countsPoints7 = await page.locator('[data-testid="dashboard-sparkline"] polyline').getAttribute("points");
  const expectCounts7 = expectedPoints(SEED.trendCounts7);
  record(
    "B4:窗口切换 7 天双查询重画(共 8 条 · 峰值 5;7 点对算)",
    trendTotal7 === "近 7 天共 8 条 · 峰值 5 条/日" && countsPoints7 === expectCounts7,
    `trend-total="${trendTotal7}";points 对算 ${countsPoints7 === expectCounts7 ? "一致" : "失配"}\nrendered="${countsPoints7}"\nexpected="${expectCounts7}"`,
    "b4-g6-dashboard-7d.png",
  );
  const ratePoints7 = await page.locator('[data-testid="dashboard-rate-sparkline"] polyline').getAttribute("points");
  const rateSummary7 = (await page.locator('[data-testid="rate-summary"]').textContent())?.replace(/\s+/g, " ").trim();
  record(
    "G6:窗口切换后成功率序列不变(3 个完结日全在 7 天窗内;57% 4/7)",
    ratePoints7 === expectRates && rateSummary7 === "近 7 天累计成功率 57%(4/7 次成功)",
    `points="${ratePoints7}";summary="${rateSummary7}"`,
  );

  fs.writeFileSync(
    path.join(OUT, "b234-smoke-transcript.json"),
    JSON.stringify({ steps, consoleErrors: consoleErrors.slice(0, 30) }, null, 2),
  );
  console.log("\n==== SUMMARY ====");
  for (const s of steps) console.log(`${s.ok ? "PASS" : "FAIL"}  ${s.name}`);
  await browser.close();
  process.exit(steps.every((s) => s.ok) ? 0 : 2);
})().catch((e) => {
  console.error("DRIVER CRASH:", e);
  fs.writeFileSync(
    path.join(OUT, "b234-smoke-transcript.json"),
    JSON.stringify({ steps, crash: String(e), consoleErrors }, null, 2),
  );
  process.exit(1);
});
