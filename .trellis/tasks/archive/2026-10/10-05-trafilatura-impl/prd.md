# PRD:trafilatura extract 兜底实现(10-05-trafilatura-impl)

## Goal

static_html 引擎内 trafilatura 兜底:三分触发(规则缺失/规则跑空/字段级不兜底)+零新键输出
契约+provenance 仅兜底条目+正文量质量门+opt-in 环境变量开关(缺省关)+trafilatura 入
pyproject extras(selectolax<1 钉版);蓝本=archive/2026-10/10-05-extract-trafilatura/research.md

## 背景与蓝本

母任务 `archive/2026-10/10-05-extract-trafilatura`(已归档)完成评估定案,本档为**实现档**。
唯一蓝本 = `.trellis/tasks/archive/2026-10/10-05-extract-trafilatura/research.md`(下称 research.md),
实现逐条对齐不得另起炉灶。

一句话:static_html 引擎(L2)在「规则缺失①/规则跑空②」时,opt-in 走 trafilatura 单页正文
兜底;字段级失败③不兜底;兜底非首选,永不全量接管。

## Requirements(对齐 research §2/§3/§4/§7)

### R1 三分触发(research §2.1)

| # | 触发条件 | 行为 |
|---|---|---|
| ① | 规则缺失(`extract=None`,static_html) | 开关开+trafilatura 可用 → 兜底出条;否则现状 `extract_required` 拒载逐字节不变 |
| ② | 规则跑空(extract 在,整页 0 条;`rss` 类型除外) | 开关开 → 兜底产出过质量门才出条+降级注记;不过门/兜底失败 → 维持零条语义 |
| ③ | 字段级失败(条目缺 url→invalid_item;部分字段 miss) | **不兜底**(条目级失败=配置质量问题;单页一条形态无法重造列表条目 url) |

负向边界:`json_path` 源(direct_api/saas)与 `rss` 源结构性永不触达兜底;规则命中的源
trafilatura 永不触达(结构性「兜底非首选」)。

### R2 输出契约零新键(research §2.2/§2.3)

兜底产出 = 单页一条:

```
{url: 请求页 URL, title: trafilatura title(可退化空串), content: 正文纯文本,
 [published: date 字符串], [author: 作者], extract_provenance: "trafilatura"}
```

- 键面全部是管线/白名单既有键:`url/title/content` = `Item.from_extracted` known 四键
  (pipeline.py:465);`published/author` = RSS_ENTRY_FIELDS 既有字段名(schema.py:602);
  `extract_provenance` 落条目 metadata(不在 known 四键,from_extracted 自动归入)。
- trafilatura JSON 其余键(description/sitename/categories/tags/fingerprint/hostname/pagetype/
  source/raw_text…)不映射直接丢。
- 手写规则路径零新键零改动(不给规则产出加 provenance 之类)。
- API 钉版:`trafilatura.extract(output_format="json", with_metadata=True)`;`bare_extraction`
  2.3.0 返 Document 非 dict(v1 脚本实测 AttributeError),**禁用**。

### R3 质量门 + opt-in 开关(research §3.2/§3.3)

- 质量门 = 最低正文量门(`content.strip()` 字符数阈值,缺省 120;夹具标定:文章 203 过 /
  列表退化 78 不过,分离度好)。不过门 = 视同启发式失败 = 维持零条语义,不产伪条目。
  pagetype 判据弃用(四夹具恒 None)。
- 开关定档(动工前落死,详见 design.md「开关定档」节):**全局环境变量
  `MYIA_EXTRACT_FALLBACK=1`**,读点在引擎内兜底函数;缺省未设 = 零兜底,既有源零行为差。
  源级开关否决(理由见 design.md),粒度留池档。

### R4 依赖(research §4)

- `pyproject.toml [project.optional-dependencies]` 增 `trafilatura` 组(先例 vision/crawl4ai),
  **不进核心 dependencies**(核心依赖红线);`'selectolax<1'` 钉版入组不可省。
- 引擎内惰性 import;ImportError → 结构化降级不拦链(装不上不拦核心铁律):
  手写规则路径照常,兜底能力结构化降级(①回落 extract_required 现状;②维持零条)。

### R5 软信号(②)(research §3.1/§7-4)

②触发的 `rules_empty` 信号不丢:挂管线 fetch 阶段 `StageReport.warnings`
(pipeline.py:334 既有降级注记通道,enrich 条目级失败先例),自动恢复不翻 run 状态。

## Acceptance Criteria

- [x] **AC1(三分触发)**:mock trafilatura 注入 `sys.modules`(同 rapid_table/rapidocr 先例)
  的主套件测试覆盖:①出条(provenance=trafilatura)/ ②跑空兜底出条 / ③字段级不兜底 /
  rss 跑空不兜底 / 开关关=零行为差(①照旧 extract_required,②照旧零条)/ 质量门不过=零条 /
  trafilatura 缺装(ImportError)= ①照旧拒载。
- [x] **AC2(零新键契约)**:兜底条目键面断言 = `{url,title,content,published,author,
  extract_provenance}` 子集;`Item.from_extracted` 真跑后 published/author/extract_provenance
  落 metadata、content 落 Item.content;手写规则路径条目键面与现状一致(既有断言零改动
  全绿即证)。
- [x] **AC3(守军零回归)**:research §5 守军清单 9 测试件全绿
  (test_static_html / test_fetch_base / test_registry / test_direct_api /
  test_saas_gated_engines / test_pipeline / test_baseline / test_analysis_lane / test_schema),
  既有断言零改动;`tests/test_schema.py` 与 `schema.py` 本流**零触碰**。
- [x] **AC4(真跑可用性)**:/tmp venv(trafilatura 2.3.0 同版本)离线夹具真跑:A2(无规则
  文章页)/C2(改版文章页)出条、provenance 在档、导航/广告/页脚剥除;B2/C3(列表退化)
  被质量门拦住维持零条。证据记 evidence/。
- [x] **AC5(docs 四处+extras)**:`pyproject.toml` extras 组落地;docs/zh+en getting-started
  (extras 命令+计数)+ docs/zh+en schema.md(extract 缺省语义)同步;**开关用法双态口径**
  必须写全(CLI=env 前缀;已装 app=launchctl setenv 后重启——open 不透传 shell env)。
- [x] **AC6(门禁)**:定向 `uv run --no-sync pytest tests/engines tests/pipeline tests/test_schema.py`
  + 全量 `uvx ruff@0.16.10 check .` + `gitnexus detect-changes -r shishi --scope staged`;
  首步 impact 已跑:`_fetch_page`=LOW / `extract_html`=MEDIUM(均非 HIGH/CRITICAL,详
  design.md「首步 impact」)。

## 约束(红线)

- 兜底非首选,永不全量接管(research prd Constraints 原文重申)。
- registry/schema 层零改动是目标(env 开关路线下成立);`schema.py`/`tests/test_schema.py` 零触碰。
- 既有源缺省零行为差(开关缺省关)。
- 环境:uv sync --all-extras 或 /tmp venv;绝不裸 uv sync;真跑零外网(离线夹具)。


## AC 证据回填(2026-10-05,本流亲跑)

- **AC1**:`tests/engines/test_static_html.py` 新增 8 例(18=10 既有+8 全绿,
  `uv run --no-sync pytest tests/engines/test_static_html.py -q` → 18 passed):
  ①`test_fallback_missing_rules_produces_single_item` / ①开关关
  `test_fallback_missing_rules_disabled_by_default`(照旧 extract_required+零调用)/
  ①缺装 `test_fallback_missing_rules_without_dependency`(sys.modules 置 None)/
  ②`test_fallback_rules_empty_produces_single_item` / 规则命中永不触达+③面
  `test_fallback_rules_hit_never_touches_trafilatura` / 质量门
  `test_fallback_quality_gate_blocks_degenerate_text` / 启发式 None
  `test_fallback_heuristic_none_keeps_zero_items` / rss 负向
  `test_fallback_rss_empty_not_touched`。
- **AC2**:①用例内嵌 `Item.from_extracted` 真跑断言(metadata 三键+content 落
  Item.content);键污染探针(ARTICLE_DOC 带应被丢弃的 description/sitename/
  categories/fingerprint)断言条目面零外溢;规则路径既有断言零改动全绿。
- **AC3**:`uv run --no-sync pytest tests/engines tests/pipeline tests/test_schema.py -q`
  → **541 passed, 8 skipped**(9 守军件全含);全量 `uv run --no-sync pytest -q` →
  4267 passed, 40 skipped, **1 failed**——唯一 failed =
  `tests/desktop/test_desktop_sidecar_protocol.py::test_method_registry_allowed_matches_handlers`
  (断言 sidecar 方法数 62,实际 64):**stash 对照亲证归属并行流**
  10-05-bundled-plugins-install 的未收口中间态(`git stash push -- desktop/entry.py
  tests/desktop/test_desktop_sidecar_protocol.py` 后同例 **1 passed**,pop 后复红;
  该流加了 plugins.bundled.list/install 两方法尚未更新对账断言),本流零 desktop
  文件改动、零关联。schema.py 与 tests/test_schema.py 本流零触碰(git status 证)。
- **AC4**:`evidence/real-run-output.json`(/tmp venv trafilatura 2.3.0 真跑,
  脚本 `evidence/real-run-script.py`):A2 无规则文章页=单条 203 字符正文
  (导航/广告「全场五折」/页脚「© 2026」剥除干净)+published+provenance;
  C2 改版文章页规则跑空=兜底出条同款;B2/C1 列表退化=质量门拦维持零条;
  开关关两态=A2 照旧 extract_required、C1 照旧零条。title 拿成站名与评估档
  §2.2 注记一致(既有容错消化,如实记)。
- **AC5**:pyproject.toml extras `trafilatura = ["trafilatura>=2.3,<3",
  "selectolax<1"]`(uv.lock 随更新,`uv sync --all-extras` 亲装实证 trafilatura
  2.3.0+selectolax 0.4.13 共存);docs/zh+en getting-started(extras 命令+8→9
  计数+开关双态口径:CLI env 前缀/launchctl setenv 后重启,main.rs:452 亲核
  std::env::var 消费面)+ docs/zh+en schema.md(extract 行缺省语义)+ README
  zh/en(extras 命令区+致谢 trafilatura 条目)。
- **AC6**:定向 541 passed 8 skipped / ruff `uvx ruff@0.16.10 check .` →
  All checks passed! / `gitnexus detect-changes -r shishi --scope staged` →
  16 files, 45 symbols, Affected processes: 0, Risk level: low(CLI 尾部
  「... and 30 more」截断为工具输出形态;py 符号面经索引未见受染流程)。

## 收口回执(2026-10-05 归档轮)

- 收口门禁(收口准备轮亲跑,回执落 3470b59 journal 段;本流 ba8af60 已在其树内):全量 `uv run --no-sync pytest -q` → **4284 passed / 40 skipped / 0 failed**——本流中间态曾红的对账例(62≠64,归属并行流已 stash 铁证)终态转绿零 failed;守军九件(计划清单口径)→ **302 passed, 3 skipped**(3 skipped 为既有条件 skip);净树对账 `git archive 1e231f4` collect 增量 **+31** 与逐函数清点严丝合缝(本流 10 = engines 8 + pipeline 2);ruff 0.16.10 全绿。
- CI:run 37304222631(main @ 3470b59,含本流 ba8af60)→ **success**;归档轮 `gh run view` 亲验 + `merge-base --is-ancestor` 亲证 ba8af60 ∈ 3470b59。
- 收口处置:归档至 archive/2026-10/;leftovers 留档不动(source 级开关粒度留池/trafilatura extras 不进 all 组/装机包自管环境未装该组件,后续组件接线跟进)。
