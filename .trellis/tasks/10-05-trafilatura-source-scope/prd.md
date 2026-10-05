# PRD:trafilatura 兜底源级开关(10-05-trafilatura-source-scope)

## Goal

母任务 `archive/2026-10/10-05-trafilatura-impl`(ba8af60)落地的全局 opt-in 开关
`MYIA_EXTRACT_FALLBACK=1`(缺省关)扩出**源级覆写**:品类 YAML 单源可开/关兜底;
优先级 = **源级 > 全局 env > 缺省关**;全局 env 语义不变(源级未设时取值链与
现状逐字节一致)。主人令翻案落地母任务留池件「源级开关粒度」。

## 背景

- 母任务 design.md「开关定档」节当年否决源级开关的第 1/2 条理由 = 动
  `ExtractConfig` 伤 `schema.py` + `tests/test_schema.py` golden 守军面;第 4 条
  明写「源级粒度需求留池档(另立批次须先 gitnexus impact ExtractConfig 报爆炸
  半径)」。本档即该池件的翻案批次,首步纪律照单执行(见下节)。
- 翻案不推翻母任务结论,而是换形态绕开:开关不进 `ExtractConfig`,走
  **引擎旋钮命名空间** `engine_options`(源级开放参数,`SourceConfig` 的
  `extra="allow"` 直通,PRD「源级扩展参数」既有设计)。

## 首步纪律:impact + golden 受染评估(动工前亲跑,2026-10-05)

### gitnexus impact(CLI,-r shishi)

| 符号 | 风险 | 半径 | 解读 |
|---|---|---|---|
| `ExtractConfig` | **CRITICAL** | impactedCount=84(直接 47 / depth2=30 / depth3=7),processes=0 | 主因 = `schema.py` 类符号的 IMPORTS 边(pipeline/gates/engines 全导 schema)。结论:**不碰 ExtractConfig 类面**——这也是形态定案的直接输入(见下)。 |
| `SourceConfig` | **CRITICAL** | impactedCount=84(同 schema.py 类符号 IMPORTS 面) | 同因。结论:不增 SourceConfig 闭字段,源级开关走 `extra="allow"` 开放命名空间,两类面零触碰。 |
| `_fallback_enabled` | 未入索引(`Target not found`) | — | 索引滞后于 ba8af60 私有函数;按任务口径 grep 兜底:`rg -n '_fallback_enabled'` 全仓仅 `src/myssia/engines/static_html.py` 定义 + 同文件两调用点(`_check_extract_support` / `_fetch_page`),零外部消费,纯模块内私有半径。 |

按 AGENTS 纪律如实记:两符号 CRITICAL 警告在案。本批次的动法 = **对这两个
CRITICAL 类零编辑**(schema.py 零改动),实际编辑面 = static_html.py 模块私有
函数升实例方法(grep 证零外部调用者)+ 测试 + 文档。爆炸半径实际收窄为 LOW。

### tests/test_schema.py golden 面受染评估

- 76 个测试;`rg 'golden|model_dump|model_fields|snapshot'` 零命中——本仓
  schema 测试无序列化快照面,断言全是行为级(错误码/path/校验语义)。
- 源级开关走 `engine_options` 开放键 = `schema.py` 零字段增 = **test_schema.py
  零受染**(门禁跑它纯粹是守军回归确认,不存在「同步再生 golden」事由)。

## 开关形态定案(主人令:两候选取最合身,定案记档)

**定案:`engine_options.static_html.extract_fallback: true/false`(布尔,缺省未设)。**

```yaml
sources:
  - name: demo
    url: https://example.com/news/story
    engine_options:
      static_html:
        extract_fallback: true   # 单源开;false=单源关;未设=跟随全局 env
```

候选评估:

1. **`extract.fallback`(ExtractConfig 内字段)——弃**。结构性缺陷:三分触发的
   ①场景 = `extract=None`(规则缺失),extract 键整个不存在,`extract.fallback`
   无处挂——而①恰是源级粒度最有价值的场景(想让个别无规则源吃 L2 正文兜底,
   其余源不吃)。要救①就得给 `ExtractConfig.type`/`fields` 必填开洞,破坏
   fail-fast,且正撞 impact CRITICAL/84 的类面。
2. **`engine_options.static_html.extract_fallback`——取**。合身性四条:
   - `engine_options.<引擎名>` 是 docs 明文的「引擎旋钮命名空间」
     (firecrawl.endpoint / scrapling.backend / stealth_browser.max_pages /
     crawl4ai.timeout / zenrows.timeout / credhunter 凭据先例);兜底开关是
     static_html 引擎行为参数,同族归位,①②两场景(extract 有无)均可达。
   - **schema.py 零改动**:`SourceConfig extra="allow"` 直通,凭据扫描 +
     已知字段 typo 守卫(`_check_extra_params`)已覆盖此命名空间——母任务
     否决理由 1/2(schema 伤害 + golden 受染)就此消解,CRITICAL 类面零触碰。
   - 校验落引擎层循 saas `_bool_option` 先例(saas.py:180「布尔选项(类型错即
     结构化拒;SaaS 参数面容不下含糊值)」):值非布尔 → `FetchError
     error_type="invalid_engine_options"` 结构化拒,不开不关的含糊值(字符串
     "yes"/1)装载后静默失效才是坑。
   - 布尔三态天然:`true`(开)/`false`(关)/ 未设(跟随全局 env)。

关于任务指令中「schema.py 词表/校验」:engine_options 形态下 schema.py 零新
词表/校验需求(开放命名空间由既有 `_check_extra_params` 把守;类型校验按先例
落在引擎层 `invalid_engine_options` 既有错误码)。这是「取最合身形态」的直接
推论,如实记档。

## Requirements

### R1 取值链(static_html.py)

`_fallback_enabled()` 由模块函数升为引擎实例方法(带源上下文):

```
engine_options.static_html.extract_fallback(布尔,类型错结构化拒)
  → 未设时 MYIA_EXTRACT_FALLBACK == "1"(现状语义逐字节不变)
  → 缺省关
```

- ①放行判定(`_check_extract_support`)与 ②跑空兜底(`_fetch_page`)两触发点
  同一实例方法,取值链单点。
- `engine_options()` 形状校验免费继承 BaseEngine property(非映射 → 既有
  `invalid_engine_options` 拒)。
- rss/json_path 结构性不挂、规则命中永不触达、质量门、缺装降级——母任务
  全部语义零改动。

### R2 测试(tests/engines/test_static_html.py,既有断言零改动)

- 开关矩阵:源级开/关/未设 × 全局 env 开/关 = 6 格(参数化,①场景断言出条/
  拒载 + fake.calls 触达性),MockTransport 离线。
- 类型错例:`extract_fallback: "yes"` → `invalid_engine_options` 结构化拒。
- ②场景代表性例:源级开 + env 关 → 规则跑空兜底出条(证②同一取值链)。

### R3 文档同步

- `docs/zh/schema.md` + `docs/en/schema.md`:sources 表 `extract` 行补源级覆写
  口径;`engine_options` 旋钮清单补 `static_html.extract_fallback`。
- `skill/SKILL.md`:sources 表 `extract` 行 + `engine_options` 命名空间行同款
  同步(母任务未覆盖 SKILL.md 的开关口径,本批补上)。

## Acceptance Criteria

- [x] **AC1(矩阵六格)**:参数化矩阵全绿——源级开(两 env 态均开)/ 源级关
  (两 env 态均关,含全局开被单源压掉)/ 未设(跟随 env,与现状逐字节一致)。
- [x] **AC2(类型错)**:非布尔值 → `FetchError error_type="invalid_engine_options"`。
- [x] **AC3(守军零回归)**:`uv run --no-sync pytest tests/test_schema.py tests/engines -q`
  全绿;`tests/test_schema.py` 与 `schema.py` 本流零触碰(git status 证)。
- [x] **AC4(docs/SKILL 同步)**:docs zh/en schema.md 双侧 + skill/SKILL.md 同步,
  优先级口径(源级 > 全局 env > 缺省关)三处一致。
- [x] **AC5(门禁)**:定向 pytest(AC3 命令)+ `uvx ruff@0.16.10 check .` 全过;
  数字回执本档。

## AC 证据回填(2026-10-05,本流亲跑)

- **AC1**:`tests/engines/test_static_html.py` 参数化
  `test_fallback_source_scoped_switch_matrix` 六格
  (`src-on-env-on` / `src-on-env-off` / `src-off-env-on` / `src-off-env-off` /
  `src-unset-env-on` / `src-unset-env-off`)全绿;开态断言出条+provenance+
  `fake.calls` 触达,关态断言 `extract_required`+零触达;未设两格与母任务
  既有例(`test_fallback_missing_rules_produces_single_item` /
  `..._disabled_by_default`)口径逐字节一致。
- **AC2**:`test_fallback_source_scoped_type_error`——`extract_fallback: "yes"`
  → `error_type="invalid_engine_options"` + `fake.calls == []`(校验在兜底
  分流前,fetch 生命周期 `_check_extract_support` 即拒)。
- **AC2.5(②同链)**:`test_fallback_source_scoped_covers_rules_empty`——
  源级开+env 关,规则跑空(list 型零命中)兜底出条,证②触发点同一取值链。
- **AC3**:`uv run --no-sync pytest tests/test_schema.py tests/engines -q` →
  **473 passed, 8 skipped**;`schema.py` 与 `tests/test_schema.py` 零触碰
  (git status 亲证,不在本流改动清单);test_static_html.py 单件
  26 passed(18 既有零改动 + 8 新)。
- **AC4**:docs/zh/schema.md + docs/en/schema.md(sources 表 `extract` 行优先级
  口径 + engine_options 旋钮清单各加 `static_html.extract_fallback` 条目)+
  skill/SKILL.md(sources 表 `extract` 行 + 源级扩展参数段)三处同步,
  口径一致(源级 > 全局 env > 缺省关;非布尔 fetch 期结构化拒)。
- **AC5**:全仓 `uvx ruff@0.16.10 check .` → All checks passed!;
  `gitnexus detect-changes -r shishi --scope staged`(本流路径 stage 后)结果
  见 task.json notes。
- 并行流注记:本流工作期间工作树新出现 `tests/desktop/test_desktop_sidecar_protocol.py`
  与 `tests/pipeline/test_baseline.py` 脏件(首次 git status 无,属并行会话
  在途件),本流零触碰零关联,commit 严格 `--only` 六路径。

## 约束(红线)

- `schema.py` / `tests/test_schema.py` 零触碰(形态定案的直接红利,亦是守军红线)。
- 全局 env `MYIA_EXTRACT_FALLBACK` 语义不变;源级未设时行为与 ba8af60 现状
  逐字节一致(既有 8 个兜底用例零改动全绿即证)。
- 并行会话脏面域(alerts/store(sqlite.py/models)/cron/messaging)一律不碰;
  `git commit --only` 明确路径,绝不 `git add -A`;不推远端;uv 裸 sync 禁用。
- 兜底非首选不变:源级开关只裁「该源是否允许兜底」,不改变三分触发/质量门/
  零新键契约。
