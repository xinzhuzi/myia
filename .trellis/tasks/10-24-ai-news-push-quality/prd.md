# PRD — AI 资讯推送质量三修:条数帽/重点过滤/中文翻译

## Goal

主人 10-24 判例(截屏 07:00:10):「AI 资讯」一条推 8 段 235 条英文标题——太多、无重点过滤、无中文。三修让任何出口的推送单条有界、有门槛、人话(中文)。

## 背景与根因

- 事故放大器=s5 误推(first_run 积压 235 条 route 预演 immediate 合并一条,8 段续发);但**产品缺口普适**:品类自身 push 模板直渲染 `for items` 无条帽(daily-digest 分区有 max_entries/min_score,品类卡裸奔);enrich 分只用于路由,digest 出口无价值折叠;全链零翻译面,英文标题原样上屏。

## Requirements

- R1 条数帽:所有直渲染 items 的品类 push 模板(ai-news/wool/games 等存量)加统一帽——正文最多 20 条,超出尾行「另有 N 条省略」;模板层实现(Jinja 切片),不改管线。
- R2 重点过滤:同一批模板加价值折叠——`item.scores.value` 有分且 <3 的不进正文,尾行「另有 N 条低价值」;无分条目不拦(既有语义)。
- R3 中文翻译:enrich 增 `translate` 开关——title 非中文条目批量产中文译名(≤40 字,专有名词保留)写 `metadata.title_zh`;ai-news 先开(modelscope 免费推理,既有 batch/cache 框架);出口模板(ai-news/wool/daily-digest)优先渲染 `title_zh`,无则回退原题。
- 防御注记:s5 形态(开发库存量轰爆)真库由 value_gate.first_run_quiet 兜住,本档修普适面。

## Acceptance Criteria

- [x] AC1 模板帽:构造 30 条 items 渲染,正文=20 条+「另有 10 条省略」行;≤20 条时无省略行(快照测试)。
- [x] AC2 折叠:构造 scores.value=2/5/无分三态,正文含 5 分与无分、低分进折叠行(快照测试)。
- [x] AC3 翻译:enrich translate 开启后英文标题条目 metadata.title_zh 非空且中文(mock LLM 单测+真跑冒烟一条);中文标题零调用。
- [x] AC4 模板优先级:有 title_zh 渲染译名,无则原题;daily-digest 分区一同生效。
- [x] AC5 全量门禁:pytest 全量零新红 + ruff。


## 真跑验收实录(2026-10-24 07:40-09:10,主人问「测试了吗」后补)

- 单测 6668 绿先行;真跑(stdout 通道沙箱变体,零飞书打扰)挖出并修掉三连:
  1. **魔搭免费推理整线下线**(DeepSeek-V4-Pro/V3.1/Qwen3-235B 三候选全拒)→ 按 10-17 本机优先判例切 LM Studio qwen3.8-27b;
  2. **60s 超时缺省**是云轨旧值 → 240s;
  3. **思考态双病症**(JSON 截断未闭合+拖满超时)→ max_output_tokens 8192 + disable_thinking 参数级接线(schema 两字段全链);提示级 /no_think 对 LM Studio 无效判例重演。
- **终验实证**:真 LLM 中文译名落库 9 条(「Uber与OpenAI为全员引入ChatGPT Work」「AT&T如何用OpenAI重塑内部法律工作」…);34 条构造经真 renderer 卡面=20 条正文+「另有 14 条省略」尾行+原生中文(aihot)正常混排——三修全链真实生效。本地 27b 实测约 2 分钟/5 条批(全量 862 条靠预算 50k 封顶+缓存跨 run 增量,首轮慢后续秒)。
- 插件测试内存钥匙链补种 local 键对+批宽断言同步(5)。

## 主人版式裁决落地(2026-10-24 09:30-10:00,主人看板「这个方式就是对的」)

- 主人示图=华为云 8:30 老线 AM 日报(服务器未关仍在跑);**MYIA 同槽 08:05 日报 failed**——根因:生产数据根 daily-digest.yaml 旧副本带 labels,装机新代码 options 校验拒载(补种幂等不覆盖判例的阴暗面首次实害);7 件漂移配置 repo→生产同步核验一致。
- 版式对齐主人拍板格式:头行「AI信息 {date}-{AM/PM}」(替「情报日报 · date · AM」),分区名 AI 日报/AI 厂商日报;快照+断言面 8 处同步(9e3de5fd)。
- **补发实证**:09:51:59 真发一条「AI信息 2026-10-24-AM」(AI 日报/AI 厂商日报/AI 白嫖与优惠 三分区+15 条+尾戳;日志 run 10904 immediate=1 唯一一次,二次诊断跑被 dedup 拦截零重发)。
- 遗留:羊毛并进单卡第四区块(现独立速报卡)=可翻案开放点;华为云关停待主人执行。

## 装机面收口(2026-10-24 10:00,主人问「做完了?」后补)

- 诚实欠账承认:四轮代码落地后装机包未刷——旧包 schema 不识 translate/disable_thinking,明早 08:00 ai-news cron 会被新配置打红(主会话自查抓出)。
- **并行会话活跃中**(10-24-paid-sub2api-tencent-migration 10-24 09:5x 在途建档+desktop/ui-src 有未提交改动)→ 全树 tauri build 会打包他人半成品,按判例改走**外科**:git archive HEAD 干净源(内容=已推提交,完整性等价)→ /Applications/世事.app Resources/myssia-src/{myssia,myssia_classifier,entry.py}+config 19 件 rsync 刷新(旧 schema 备份 /tmp/schema-before.bak)→ codesign 重签 satisfies DR。
- **装机态五验全过**:①EnrichConfig translate/disable_thinking/max_output_tokens 8192 可载;②ai-news/baily-digest/wool/watch-deals/ai-vendor-daily 五品类新配置装载;③urlwatch MYIA_HOME 锚定;④模板帽 20/折叠线 3.0;⑤cron 执行体可导入——明早 08:00 采集→08:05「AI信息 2026-10-24-AM」全链由新代码跑。
- 完整重打包(tauri build)留待并行会话落定后补做(外科源=HEAD 已推内容,风险窗口为零,记档)。