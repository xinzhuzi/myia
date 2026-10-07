# 日志屏历史跨重启可见:运行历史 DB 合流 + cron/feishu 入口统一收尾

## Goal

主人 2026-10-07 令「按照你的建议去做」——承接 10-07-unified-logging 归档勘误(run-report §8)的全部建议:让重启后的日志屏真正翻得到上一程(把回填的价值在 UI 落地),顺手修独立复查遗留两 low。前置勘误 commit 已入归档档。

## 现状与根因(勘误已核,勿重查)

- 运行历史数据源=sidecar **会话级**内存注册表(`run.status`→`_m_run_status`),重启即空;空态(`logs-screen.tsx:812` EmptyState)盖整卡,`logs.tail` 按运行行展开才惰性拉取——列表空则回填(协议层已生效,测试钉死)永不可见。
- DB `runs` 表已有跑次落库(f299432:stats_dict 含推送失败明细)——读史的基础在,未被 run.status 消费。
- 独立 `myssia cron serve` 走 cli.py 入口 `proc="cli"` 硬编码(cli.py `_configure_logging`);design 曾承诺 proc="cron"。
- `python -m myssia.push.feishu_callback` 独立进程入口仍是 ad-hoc `basicConfig`(feishu_callback.py:449)零持久化。

## Requirements

- **R1 运行历史跨重启可见(核心)**:`run.status` 改为「会话注册表(进行中/最新,现有语义)合流 DB runs 表历史」——重启后日志屏显示上一程跑次行(新→旧排序不变),历史行带徽标(如「上一程」)与同款状态/耗时/条目数;展开历史行→`logs.tail?run_id=N`→回填行(已生效能力,零新协议)。历史行数上限 50(防长列表)。**runs 表字段不足以支撑行展示时最小补字段落库(不动旧数据)**;注册表行与 DB 行去重(同跑次不双列)。无任何历史(全新装机)时空态现状不变。
- **R2 cron proc 细分**:独立 `myssia cron serve` 进程 proc="cron"(cli 入口传递);普通 CLI 仍 proc="cli"。测试双向钉死。
- **R3 feishu_callback 统一入口**:`logging.basicConfig` 退役,改经 `myssia.log.configure(mode="serve", data_root=<MYIA_HOME 感知解析>, ring=False, proc="feishu_callback")`;终端裸跑=stderr-only 沿决议②口径。测试:配置后 handler 集形状+MYIA_HOME 沙箱落盘。
- **R4 spec 同步**:sidecar-protocol.md `run.status` 行为补「DB 历史合流」语义(形状兼容声明);python/logging.md proc 枚举补 cron/feishu_callback。

### 非目标

- 不做「UI 日志进日志屏」(决议④可选项,不随本任务解禁)。
- 不动并行任务 dashboard-trend-today-fix 的域文件(dashboard/feed 趋势面)。
- 不引入 runs 表 schema 大改或数据迁移(最小补字段即可,若必需)。

## Acceptance Criteria

- [x] AC1 重启后历史可见(协议):`run.status` 在新 serve 实例返回 DB 历史跑次行(含徽标字段/去重/上限 50),注册表进行中行合流在前;空库时空态形状与现状全同(零回归)。——tests/desktop/test_desktop_sidecar_protocol.py:511(合流形状/徽标/新→旧/僵尸滤除/log_run_id 透传)、:537(注册表在前+record.run_id 去重+键集不混新键)、:568(上限 50:60 行种库取 60..11)、:584(空库 `{"runs":[]}` 零回归)、:592(真 run 端到端:runs 行回填 log_run_id+全量视图同跑次不双列);实现=desktop/entry.py `_history_run_rows`(上限 `_RUN_HISTORY_LIMIT=50`@entry.py:3296,拉取=limit+排除数@entry.py:3594)。独立复查者亲跑复验过同批用例全绿。
- [x] AC2 像素级装机验证:换装后真机跑一次采集→重启 App→日志屏**显示上一程跑次行**,展开该行**可见日志行(回填)**——截图 PaddleOCR 复核文字实据(收尾代理无图像输入时必须走 local-ocr 车道,不留主人)。——装机验证者按车道直调 PaddleOCR,实读文字(evidence/ocr-13-logs-screen-final.txt):「运行历史30/30轮新→旧」+#30 myia-demo「上一程」(conf 0.9998)+#29 ai-news「上一程」(0.9998)+展开体日志行两条(「2026-10-07 05:34:49,633 INFO myssia.pipeline: 去重跳过(已见过) key=https://github.com/CopilotKit/openmuse|OpenDots」)+「总耗时 3.1s /94行/1ogs.tail run_id=1」;07 初始帧同读(ocr-07-initial.png.txt)。链路回执=evidence/install-receipt.txt(run 30 落库 log_run_id=1、schema v9→v10 迁移、换装+清 WKWebView 缓存、复原核 env 旗均空)。注:收尾者模型无图像输入,像素主张以 OCR 车道产物为据+独立复查者交叉读档复核(其复查档原文明记「AC2 装机证据本身真实充分」)。
- [x] AC3 cron/feishu proc:测试钉死 cron serve=proc:"cron"、普通 CLI="cli"、feishu_callback 配置后 handler 集与落盘形状。——tests/test_log.py:496(cron serve 入口 proc="cron")、:513(普通 cron 子命令仍 "cli")、:522(`_configure_logging` 缺省 "cli")、:531(feishu MYIA_HOME 落盘形状:JsonlFileHandler+StreamHandler 两件/ring 无/行 proc=feishu_callback)、:558(裸跑 stderr-only 不建 logs/);实现=cli.py:1312(proc 关键字参)/cli.py:2278(serve→"cron" 其余→"cli")/feishu_callback.py:457-461(configure proc="feishu_callback")。
- [x] AC4 spec 两档同步入档。——.trellis/spec/desktop/sidecar-protocol.md:28(run.status 行为补 DB 历史合流:history:true 徽标+log_run_id 对齐键+record.run_id 去重+上限 50+僵尸行不进+空库全同+**形状兼容声明**——加法可选字段,旧前端忽略照跑,PROTOCOL_VERSION 不 bump=10(entry.py:503 亲核));.trellis/spec/python/logging.md:20(入口路由 proc 词表 `cli`/`cron`/`sidecar`/`vision`/`feishu_callback`,R2/R3 语义入档)。commit 8f6f33b。
- [x] AC5 门禁全绿:定向 pytest+ruff / `just test-ui` / 收尾 `just test`+`just check`;gitnexus impact 前置(run.status 触及面)+ detect-changes。——定向(各批提交回执):d4bb295 pytest 76+162+593 passed、ruff 全绿;902509d vitest 28 files/598 tests 全绿+tsc 双绿。gitnexus:impact 前置 `_m_run_status`=LOW/`_configure_logging`=MEDIUM(加默认参 12 调用点零改动)/`_row_to_run`=HIGH(纯增量可空+防御读已核);detect-changes 各批回执(8 files 32 symbols 零 dashboard 泄漏→3 files 9 symbols low→3 files 5 symbols low);902509d 索引用面缺口(logs 屏符号不在索引)如实记档+rg 全树核验兜底。收尾全量(本批收尾者亲跑,2026-10-07 05:57-05:59):`just test`=pytest **4922 passed, 40 skipped**(112.94s)+vitest **598 passed(28 files)** exit=0;`just check`=ruff **All checks passed!**+`tsc -b && vite build` ✓ built+cargo check --locked Finished,exit=0(回执详见 run-report.md §门禁)。
- [x] AC6 并行安全:全程未触碰 dashboard 域文件与并行任务档;提交外科 pathspec;task.json 状态直改(不用 task.py start/finish/archive)。——五提交文件面亲核(git show --stat):d4bb295(8 文件:entry.py/cli.py/feishu_callback.py/store 两档+测试三档)、66a22f7(测试三件)、902509d(logs 屏三件)、8f6f33b(spec 两档+本任务档四件)、d02812d(测试三件)——零 dashboard/feed 趋势域文件、零 .trellis dashboard 任务档;各批 git add 外科 pathspec;task.json 全程直改(本批置 review);evidence/ 按例不入 git。独立复查越界核对同结论。

## 过程(执行流水,回填位)

- 前置:180d707 归档档勘误补记(任务出生证明,根因与建议=10-07-unified-logging run-report §8,勿重查)。
- 事实核谱(只读侦察员):runs 表 schema 与读取 helper、run.status 形状与「会话计数器 vs DB AUTOINCREMENT 两编号空间不同源」结论(去重键定案)、前端 run 行消费字段与徽标体系、cron dispatch 点、feishu 入口结构;产出实现风险清单。
- 后端批 d4bb295(05:46 提交,04:46):R1 run.status 合流(`_history_run_rows`:注册表在前新→旧形状逐字节不变+DB 历史接续/去重键=注册表行 record.run_id(同 DB 空间)/上限 50/僵尸行不进历史/库故障降级仅注册表视图)+ store 最小补字段(runs 表 v10 加 log_run_id:SCHEMA_VERSION 9→10 幂等迁移+防御式读+set_run_log_run_id 回填 helper+_run_worker 尽力回填会话号)+ R2 cron serve proc="cron"+ R3 feishu_callback 统一入口;测试三档落位(AC1 五例/AC3 五例/store 三例);定向门禁亲跑全绿(pytest 76+162+593、ruff);gitnexus impact 前置+detect-changes staged(8 files 32 symbols,零 dashboard 泄漏)。
- 门禁收口 66a22f7(05:02):schema 版本钉死断言随 v10 符号化六处(tests/alerts 三+tests/store 三)+ 两例 dev 腿 CWD 敏感用例 hermetic 化;复验 906+258 passed。
- 前端批 902509d(05:16):logs 屏「上一程」历史行(徽标同 variant=outline/logs.tail 按 log_run_id 对齐拉取/旧行 null 如实降级「该跑次早于日志对齐落库」/rowKey 全链防撞号/历史行无重跑钮/空态守 runRows.length===0 合并模型)+ logs-screen.test.tsx 五例(渲染/按对齐号拉取/旧行降级/撞号防混/空态零回归);vitest 598 全绿+tsc 双绿;gitnexus 索引用面缺口如实记(索引自查无此屏)——rg 全树核验爆炸半径兜底+SOP 全量重建恢复 WAL。
- spec 批 8f6f33b(05:19):R4 两档同步+任务档建档入库(prd/task.json/jsonl 六件随本批入 git)。
- 门禁收口二 d02812d(05:24):全量 just test 五红修复——engines 四红=MYIA_EXTRACT_FALLBACK 环境泄漏 hermetic 化(monkeypatch.delenv,存量欠账非本任务回归,双态双绿闭环)+ test_baseline.py:463 版本金丝雀 "9"→"10" 随 v10 迁。
- 装机像素级验证(装机验证者,05:31-05:5x):just build-desktop 重打包(HEAD=d02812d,产物含 R1 合流码+前端「上一程」)→ 备份换装+清 WKWebView 缓存 → 会话一直跑二进制(无焦点纪律)跑一次采集(run 30 落库,log_run_id=1,schema v9→v10 实迁)→ quit 退净 → 会话二重启进日志屏 → 截图七帧+PaddleOCR 实读两帧 → 复原核(env 旗均空/工作树零源码改动);过程帧 WKWebView 欠栅格化现象如实注记(合成器行为非产品缺陷,大 resize 后像素层齐)。
- 独立复查(独立复查者,冷审):五提交 diff 全读+定向测试亲跑复验(AC1 六例/store 三例/AC3 五例/金丝雀 136 例/前端 logs 21 例全绿);核心正确性八项成立(去重键同编号空间/上限与排序/空库零回归/proc 双向/spec 逐条对齐/run_id 闭环到 ring_snapshot/越界零触碰/前端防撞号);**零 medium+ 发现**,两 low 见 run-report §复查处置。
- 收尾(本批):全量 `just test`+`just check` 亲跑双绿(回执 run-report §门禁)→ 回填本档 → run-report.md → task.json 直改 review → docs(task) 收尾 commit(外科 pathspec,只提交不推送)。

## 结果(验收回执,完工填)

- AC1-AC6 全勾(证据逐条见上);R1-R4 全落地,四需求各有实现锚点+测试钉死+spec 入档。
- 门禁终态:定向各批全绿(见过程);收尾全量 `just test`=pytest 4922 passed, 40 skipped+vitest 598 passed(28 files)、`just check`=ruff+tsc/vite build+cargo check 全绿,均 exit=0。
- 装机终态:重启后日志屏「上一程」行+展开回填日志行均经 PaddleOCR 实读(OCR 文字与置信度存 evidence/)。
- 复查终态:零 medium+;两 low——①僵尸行占拉取余量窗(entry.py:3594/3603,合格历史行可能少列不超限)遗留观察项;②AC5 全量门禁无回执+收尾批未落——**本批已偿**(全量双绿+本回填+task.json 置 review)。
- 状态:review(休止,不 archive——归档留 wrap);未推送(待主人令)。
