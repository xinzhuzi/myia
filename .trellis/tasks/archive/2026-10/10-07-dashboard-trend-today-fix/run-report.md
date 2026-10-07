# run-report — 10-07-dashboard-trend-today-fix

执行载体:动态工作流 dwfrun-8fad3264(批0-批3+返修循环+复查门;20:20 起跑,20:40 会话中断一次,恢复后续跑至全绿终态)。

## 提交对账

| 批次 | 提交 | 内容 | scoped 门禁(代理亲跑) |
|---|---|---|---|
| 建档 | 5802161 | 三件套+jsonl+task.json 六件(evidence/ 不入) | —(docs 提交 detect-changes=No changes) |
| 批1 提交点① | cfc3c9a | api.ts:CHART_WINDOW_MIN_DAYS=7+chartWindowDays+buildOverviewStats 概览窗切片+注释;纯函数断言(基线 71+2) | vitest 73 passed + tsc EXIT=0;impact buildOverviewStats=LOW(屏内) |
| 批2 提交点② | d88c306 | screen:两调用点切 chartWindowDays+标签两分法+D6/D8 守卫+注释;断言翻新七行+新增 2 例 | vitest 75 passed + tsc EXIT=0;impact DashboardScreen=LOW;detect-changes=屏内(d4bb295 为并行任务,零混淆) |
| 批3 提交点③ | (验证步零代码) | 全量门禁+像素验收+复查门,回执见下 | — |
| 收尾 | 本提交 | 勾选回填+task.json→review | — |

## 门禁回执(脚本 world.run 统一实跑)

- 全量 vitest(`npm --prefix desktop/ui-src run test`):exit 0(28 files passed)
- tsc -b + vite build(`npm run build`):exit 0
- 批0 基线:scoped 71 passed(1 file)

## 像素验收(grill Q6:devUrl 为准)

- 链路:像素代理自建 harness(evidence/harness/pixel_verify.py,devUrl + 受控 mock store.trend/runs.trend/doctor/runs.list/run.status),三场景 27/27 断言过,截图三张:evidence/像素验收-今日档.png、像素验收-全零窗.png、像素验收-14天回归.png
- 主会话 local-ocr 补验(180d707 教训:无图像输入代理的像素主张须补位)两张关键图逐字核过:今日档=「近7天共22条·峰值5条/日」+轴行 2026-09-30/2026-10-06 两端不同+verdict「今日采集5条」;全零窗=无 y 刻度列(0/0/0 不再)+「近7天共0条 ·峰值0条/日」

## 复查门(独立代理,零实现参与)

pass——AC1-AC5 全过;§4 翻新清单七行 diff 逐行核;verdict 段零 hunk;D6 不闪机制亲核;协议零变更;反 AI 审美不触发。唯一 low(evidence/harness/__pycache__ 留档)已清。

## 遗留与如实注记

- cargo test/check 未跑:零 Rust 改面(detect-changes 波及核对)
- 真机装机包目验:grill Q6 决议归 tag 驱动发布流,不绑本档(装机包刷新未做,主人升级时随发布流刷新)
- 未推送:待主人令
