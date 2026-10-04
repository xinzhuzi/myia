# B234 无头 GUI 冒烟证据(10-04-desktop-b234)

**结论:21/21 断言全绿(DRIVER_EXIT=0),零 console 错误。** B2/B3/B4 三件 + G6 成功率折线
在无头真链路(GUI ← shim ← bridge ← 真 sidecar spawn ← 夹具 SQLite)上全部实测通过;
趋势折线数据源为种子真数据(SVG polyline 逐点对算),非 mock。

## 法(先例:10-03-detail-images evidence/app-headless)

零 GUI 启动:不跑 Tauri 壳。四件套:

1. **真 sidecar spawn**:`bridge-b234.mjs` 用 `desktop/.venv-build/bin/python` spawn
   当前源码 `desktop/entry.py serve`(stdin/stdout 行 JSON 协议),HTTP `/rpc` 转发(带 CORS)。
2. **夹具隔离**:`MYIA_HOME=/tmp/myia-b234-e2e/home`(bridge 内注入)→ serve 上下文
   缺省 db=`<home>/myia.db`、plugins=`<home>/plugins`;比先例的 shim 注 `params.db`
   更贴真壳数据通路(不注入任何参数,缺省解析全真)。`seed_fixture.py` 用真
   SQLiteStore 写种子(items 7/3/5 三日 + runs 四日五态 + CLI 反馈 1 条),
   种子法镜像 tests/test_desktop_sidecar_protocol.py:2016/:3219/:3304。
3. **vite dev**(5222)+ **Playwright headless chromium**:`__TAURI_INTERNALS__` shim
   把 `sidecar_request` 转发 bridge(全真协议往返,零 mock 零 route 拦截);
   另补 `__TAURI_EVENT_PLUGIN_INTERNALS__`(@tauri-apps/api/event.js:100 的
   unlisten 通路,缺则路由清理 pageerror)。
4. **对算断言**:期望几何由 sparkline.tsx sparkPoints(:50-57)文档公式在驱动侧
   独立复刻,喂种子真值算出,与渲染出的 `polyline points` 逐字符比对。

## 断言清单(21 项,全 PASS;transcript 见 b234-smoke-transcript.json)

| 区 | 断言 | 实测 |
|---|---|---|
| P0 协议 | 真 spawn 应答 / 注册面 | run.status 空表;method_not_found.allowed=48 且含 runs.trend/feedback.mark/store.trend |
| P0 协议 | runs.trend days=14 聚合 | 今天{success3,failed1,running1}/昨天{success1,running1}/3天前{failed2} 旧→新,40 天前不入窗 |
| P0 协议 | 钳制/过滤/形状 | days0→仅今天;91→含 40 天前 partial;category 过滤;非 int 拒 invalid_params |
| P0 协议 | store.trend | d-10:7 / d-3:3 / 今天:5 |
| P0 协议 | feedback.stats 基线 | CLI good×1 |
| B2 GUI | feed 👍 | aria-pressed false→true + 置灰防重(b2-feed-marked.png) |
| B2 往返 | mark→list | channel=desktop, dedup_key=b234-smoke-key-1, title 快照正确 |
| B2 往返 | stats | total2/good2/by_channel cli1+desktop1 |
| B2 GUI | 仪表盘反馈统计卡 | feedback-good=2 / feedback-bad=0 |
| B3 GUI | enrich 开关→写回 | aria-checked true→false;磁盘 enrich.enabled true→false;.bak 留底;状态行「doctor 已复核」(b3-enrich-disabled.png) |
| B3 GUI | 回拨复原 | 磁盘恢复 true |
| B4 GUI | 采集量摘要 | 「近 14 天共 15 条 · 峰值 7 条/日」(种子 7+3+5) |
| B4 GUI | sparkline 逐点对算 | 14 点 === 期望(max=7 归一) |
| G6 GUI | 成功率 sparkline | 3 点 [0,1,0.75] max=1 固定刻度逐点一致;area=false(polygon=0) |
| G6 GUI | 累计摘要 | 「近 14 天累计成功率 57%(4/7 次成功)」 |
| G6 GUI | 口径注记 | aria 累计口径 + 「不含进行中」/「无完结 run 的日子不入线」在卡面 |
| B4/G6 | 零错误零空态 | trend-error/rate-error/rate-empty 命中 0 |
| G6 实录 | 两口径差异 | 「近期 run 成功率」卡 40%(4/10,内存合并含僵尸 running)≠ 趋势 57%(4/7,表内口径)——如实并存 |
| B4 GUI | 窗口切换 7 天 | 双查询重画:「近 7 天共 8 条 · 峰值 5」;7 点对算一致(b4-g6-dashboard-7d.png) |
| G6 GUI | 切换后成功率 | 3 完结日全在 7 天窗,序列/摘要不变 |

截图:b2-feed-marked.png / b3-enrich-before.png / b3-enrich-disabled.png /
b4-g6-dashboard-14d.png / b4-g6-dashboard-7d.png。

## 复跑(runbook)

```bash
# 0) 夹具(幂等:先清)
rm -rf /tmp/myia-b234-e2e/home && mkdir -p /tmp/myia-b234-e2e/home/plugins
cp plugins/ai-news.yaml /tmp/myia-b234-e2e/home/plugins/
desktop/.venv-build/bin/python <本目录>/seed_fixture.py > <本目录>/seed-out.txt
# 1) bridge(后台)  2) vite(后台)
node <本目录>/bridge-b234.mjs &
(cd desktop/ui-src && npm run dev -- --port 5222 --strictPort &)
# 3) driver
node <本目录>/b234-smoke-drive.cjs   # exit 0 = 全绿
```

## 附带自跑门禁(本会话,2026-10-04)

- `uv run --no-sync python -m pytest tests/test_desktop_sidecar_protocol.py -q`
  → **116 passed in 5.99s**(全绿)
- `npm --prefix desktop/ui-src run test` → 337 passed / **1 failed**(338);
  失败 = `top-bar.test.tsx`「全局命令位留白」——**非 B234 范围**:并行
  interaction-batch 波已把留白换成真命令面板触发器(top-bar.tsx:99 注释自证
  「D4 留位 → interaction-batch A-cmd」),旧测试待该批收口同步;B234 范围套件
  全绿(dashboard-screen 36 / settings 30 / feed-card-feedback 6 / client 6 / feed 60)
- `npm --prefix desktop/ui-src run build` → **✓ built in 1.50s**(chunk 体积警告为存量)

## 锚点核对(本会话实读)

- `desktop/entry.py:379` `PROTOCOL_VERSION = 8`;`entry.py:4083-4092` 注册表
  (doctor/runs.list/runs.trend/feedback.*/store.trend);`_m_runs_trend` 实读参数校验同 store.trend 门
- `.trellis/spec/desktop/sidecar-protocol.md` 注册表 **48 行**(`^| [0-9]` 计数),
  :69 = 第 48 行 runs.trend;:88 分组注记;:111 版本段 v8 —— 与实测 allowed=48 对账一致
- `CHANGELOG.md:14` Unreleased/Added 英文条目(runs.trend)
- R3:`grep -rn "trend-card\|TrendCard" desktop/ui-src/src` **零命中**(exit 1)
- README.md:290/:301 宣称「卡片内反馈按钮、设置反馈开关、采集量趋势已随桌面对齐批次
  落地」——与本冒烟 GUI+协议实测一致,宣称属实
