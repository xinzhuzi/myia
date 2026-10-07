# run-report — 10-07-logs-restart-visibility

执行载体:动态工作流 dwfrun-b566e3de(事实核谱→后端 R1-R3→前端 R1→spec+全量门禁→装机像素级验证→独立复查→修复收尾;05:2x 起跑至收尾双绿终态)。承接 10-07-unified-logging 归档勘误(180d707,run-report §8 三件建议=本任务 R1-R3 需求源)。

## 提交对账

| 批次 | 提交 | 内容 | scoped 门禁(代理亲跑,提交信息回执) |
|---|---|---|---|
| 前置勘误 | 180d707 | unified-logging 归档档 §8 勘误三件(任务出生证明;仅改归档档两文件) | —(docs 提交) |
| 后端批 | d4bb295 | R1 合流:`_history_run_rows`(注册表在前/DB 历史接续/去重/上限 50/僵尸滤除/库故障降级)+ store v10 `runs.log_run_id`(SCHEMA_VERSION 9→10);R2 cli.py:2278 serve→proc="cron";R3 feishu_callback.py:457 统一 configure;测试三档(AC1 五例/AC3 五例/store 三例),8 文件 +438/-15 | pytest 76+162+593 passed、ruff 全绿;impact `_m_run_status`=LOW/`_configure_logging`=MEDIUM(默认参零改动)/`_row_to_run`=HIGH(增量可空已核);detect-changes staged=8 files 32 symbols 零 dashboard 泄漏 |
| 门禁收口 | 66a22f7 | schema 版本钉死断言随 v10 符号化六处+两例 dev 腿 CWD 敏感 hermetic 化(3 测试文件) | 906+258 passed、ruff 全绿;detect-changes=3 files 9 symbols risk low |
| 前端批 | 902509d | logs 屏「上一程」历史行:徽标/log_run_id 对齐展开/旧行 null 如实降级/rowKey 防撞号/空态守合并模型;logs-screen.test.tsx +5 例(logs 屏 3 文件 +382/-129) | vitest 28 files/598 tests 全绿+tsc 双绿;gitnexus 索引用面缺口(logs 屏符号不在索引)如实记,rg 全树核验兜底 |
| spec 批 | 8f6f33b | R4 两档(sidecar-protocol.md run.status DB 合流+形状兼容声明;python/logging.md proc 词表)+ 任务档建档六件入库 | —(docs 提交) |
| 门禁收口二 | d02812d | 全量 just test 五红修复:MYIA_EXTRACT_FALLBACK 环境泄漏四例 hermetic 化(存量欠账,归属如实记)+ baseline 金丝雀 "9"→"10"(3 测试文件) | 双态(变量在场/剥掉)各 139/106 passed、ruff 三文件全绿;detect-changes=3 files 5 symbols risk low |
| 收尾 | 本提交 | prd AC1-AC6 勾档回填+本报告+task.json 直改 review | 收尾全量双绿(见下节,收尾者亲跑) |
| 归档 | 6921c97 | 判活 idle(7f02a31 后>30min+该档零未提交改动)→ tasks→archive/2026-10 归档移动五件,task.json 置 completed+completedAt=2026-10-07 | —(档务提交;detect-changes=No changes detected) |
| low①②处置(归档后 wrap 补笔) | 843a5a6 | low① `_history_run_rows` 僵尸行余量递增扩窗(首窗=limit+排除数收不满翻倍续拉至收满/行尽,测试 test_run_status_history_cap_fifty_with_zombie_margin)+ vision-server.out/.err 纳入 `_purge_stale` mtime 清理(47b4672 遗留,测试 test_purge_vision_sink_by_mtime)+ spec logging.md sink mtime 一句(5 文件 +107/-31) | impact 两符号 LOW(_m_run_status/configure);detect-changes staged=5 files 12 symbols risk low;TZ=Asia/Shanghai 定向 190 passed+ruff 全绿(提交信息回执) |

## 门禁回执

- 收尾全量(收尾者亲跑,2026-10-07 05:57-05:59,HEAD=d02812d 工作树仅本任务档改动):
  - `just --justfile …/justfile test`:**exit 0**——pytest `4922 passed, 40 skipped in 112.94s` + vitest `Test Files 28 passed (28) / Tests 598 passed (598)`(日志 /tmp/lrv-just-test.log)。
  - `just --justfile …/justfile check`:**exit 0**——`uvx ruff@0.16.10 check .` = All checks passed!;`tsc -b && vite build` = ✓ built in 1.49s;`cargo check --locked` = Finished dev profile 0.79s(日志 /tmp/lrv-just-check.log)。
- 定向(各批代理亲跑,提交信息回执):后端 76+162+593 passed+ruff;前端 vitest 598+tsc 双绿;门禁收口二双态双绿(139/106)。
- gitnexus:impact 前置与 detect-changes 各批回执见对账表;前端批索引用面缺口(logs 屏符号不在索引,force 重建后如故,非本批引入)已如实记档并以 rg 全树核验+`git diff --cached --stat` 亲核兜底。

## 装机像素证据(指针+OCR 实读文字)

- 目录:`.trellis/tasks/10-07-logs-restart-visibility/evidence/`(按例不入 git)——截图七帧(07-13)+PaddleOCR 实读两帧(ocr-07-initial.png.txt / ocr-13-logs-screen-final.txt)+链路回执 install-receipt.txt。(归档 6921c97 后路径实况:07-13 帧与两份 ocr/install-receipt 随档移至 archive/2026-10 本档 evidence/;活动路径 evidence/ 仅余 wrap/(装机验证 01-06 帧+回执),均留盘外。)
- 链路(回执要点):just build-desktop 重打包(HEAD=d02812d,05:31)→ 包内验 R1 合流码+前端 dist 含「上一程」→ 备份旧装+清 WKWebView 缓存换装 → 会话一直跑二进制(无焦点纪律)触发一次采集:run 30 落库(id=30 myia-demo success 3.1s,**log_run_id=1 回填**,schema v9→v10 实迁)→ quit 退净 → 会话二重启进日志屏。
- **AC2 实读文字**(ocr-13-logs-screen-final.txt,avg_conf 0.9493):「运行历史30/30轮新→旧」+「#30」「myia-demo」「上一程」(conf 0.9998)+「3.1s」「成功」;展开体=「总耗时 3.1s /94行/1ogs.tail run_id=1」+日志行两条「2026-10-07 05:34:49,633 INFO myssia.pipeline: 去重跳过(已见过) key=https://github.com/CopilotKit/openmuse|OpenDots」;次行「#29」「ai-news」「上一程」(0.9998)「28条」「1m16s」「部分」。07 初始帧同读(「运行历史 30/30轮·新→旧」+#30 上一程+logs.tail run_id=1)。
- 判读口径如实注:装机验证者与独立复查者均无图像输入,像素主张以 PaddleOCR 车道产物为据(180d707 教训的既定偿法);收尾者模型亦无图像输入,本报告 OCR 文字=直读两份 ocr-*.txt 产物+复查者交叉读档(复查档原文明记「AC2 装机证据本身真实充分」)。过程帧(07-11)WKWebView 欠栅格化(仅绘首屏,AX 可读全量)为无焦点验证口径的合成器行为,12 帧大 resize 后像素层齐——非产品缺陷,如实注记。

## 复查发现处置(独立复查者,冷审零实现参与)

- 核心正确性八项全立(复查者亲跑定向测试:AC1 六例/store 三例/AC3 五例/金丝雀 136 例/前端 logs 21 例全绿):去重键同编号空间(`_run_record_dict` run_id=record.id=DB 空间↔`seen_db_ids` 同空间)、上限 50/新→旧(sqlite.py:2000 ORDER BY id DESC)、空库零回归、cron/feishu proc 双向(cli.py:2278/feishu_callback.py:461)、spec 逐条对齐+PROTOCOL_VERSION=10 不 bump(entry.py:503)、run_id 闭环(pump 会话号→log_run_id 同号回填→logs.tail 过滤 int==int 命中,log.py:403-404)、越界零触碰、前端 rowKey 防撞号。
- **零 medium+ 发现**(mustFix 空,收尾零代码修复)。两 low:
  1. low/python——僵尸行占拉取余量窗:`desktop/entry.py:3594` 拉取量=limit+排除数只补去重余量,`:3603` 僵尸行(finished_at None)跳过不占余量;DB 顶部僵尸行较多时合格历史行收不足 50(≤上限不违约,仅尾部少列;典型僵尸量 1-2 条)。**处置:遗留观察项不修**——上限语义未违、排序/去重不受影响,循环多拉属边缘场景优化,留后续(如僵尸行常态化再议)。**处置更新(2026-10-07 深夜 wrap 批 843a5a6):已修**——`_history_run_rows` 改递增扩窗:首窗=limit+排除数,收不满翻倍扩窗续拉,consumed 只走增量不重扫,直到收满 50 或行尽;上限语义/新→旧排序/去重键/行形状/尽力而为故障路径全不变;测试 test_run_status_history_cap_fifty_with_zombie_margin 钉死(顶 10 僵尸+55 收口仍收满 50,僵尸零入历史)。
  2. low/boundary——AC5 全量门禁无回执+收尾批未落(task.json in_progress/AC 未勾/evidence 未入 git)。**处置:本批已偿**——收尾全量 just test+just check 双绿回执(§门禁)、prd AC1-AC6 逐条勾档、task.json 直改 review;evidence/ 按仓库惯例不入 git(对账表「建档」行同款口径,非欠账)。

## 遗留与如实注记

- **未推送**:五实现提交+本收尾提交均只提交不推(主人门禁,待令)。
- **不 archive**:task.json 置 review 休止——并行任务 10-07-dashboard-trend-today-fix 同窗在途,归档留 wrap(其收尾 a97a52b 同款纪律);completedAt 不填。(后续实况:dashboard 并行档已自行归档 0b9ad6e;本档 6921c97 归档置 completed completedAt=2026-10-07——本行系收尾时点记录。)
- 复查 low①(僵尸行余量窗)收尾时点遗留观察项——归档后 wrap 批 843a5a6 已实修(见§复查发现处置更新),该项遗留清零。
- 收尾者无图像输入(AC2 口径见§装机像素证据);cargo test 未跑——零 Rust 改面,`cargo check --locked` 已绿于 just check。
- 工作树残留:四任务 evidence/ 未跟踪目录(按例不入 git,dashboard/本任务/plugin-src-remote-fetch/unified-logging 归档档各一)。——后续:f4a3747 起 .gitignore 增 evidence 两级模式(任务面+归档面),?? 噪音清零,留盘外口径不变;本档活动路径 evidence/wrap/ 与归档面 evidence/ 均按此留盘外。
