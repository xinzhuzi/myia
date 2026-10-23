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
