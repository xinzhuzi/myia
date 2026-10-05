# Design:trafilatura extract 兜底实现(10-05-trafilatura-impl)

> 蓝本:research.md(母任务档)。本档是实现期定档,与 research 冲突处以 research 为准。

## 首步 impact(gitnexus CLI,-r shishi,2026-10-05 本流亲跑)

- `gitnexus impact -r shishi _fetch_page` → **LOW**:impactedCount=3(直接 2 =
  `_walk_template`/`_walk_selector`,均 static_html 模块内;depth2=1)。
- `gitnexus impact -r shishi extract_html` → **MEDIUM**:impactedCount=14(直接 5,含
  crawl4ai/firecrawl 的 `_extract_target`;跨模块消费面)。
- 结论:均未达 HIGH/CRITICAL,可动;据此定档——**兜底逻辑全部落在 static_html.py 模块内,
  `extract_html` 本体零触碰**(MEDIUM 消费面不染,crawl4ai/firecrawl 零波及)。

## 开关定档(动工门,先落档后动码)

**定案:全局环境变量 `MYIA_EXTRACT_FALLBACK=1`。**

- 读点 = 引擎内兜底函数 `os.environ.get("MYIA_EXTRACT_FALLBACK") == "1"`;CLI 与 sidecar
  同一 Python 代码路径自然同读(desktop/entry.py 起的 sidecar 进程继承环境)。
- 测试形态 = `monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")` 逐例注入——同
  desktop/entry.py:563-567「env 可被测试逐例注入」先例形态(`_serve_context` 每请求
  `os.environ.get`,无缓存)。
- 缺省未设/值非 "1" = 零兜底,既有源零行为差。
- AC 可用性验收(A2/C2)= 测试内 setenv 打开后离线夹具真跑出条,开关可达性成立。

**否决源级开关的理由**(计划指令要求落档):

1. 源级 = `ExtractConfig` +1 可选字段 = 动 `schema.py`(research §5 守军文件 5),而
   research §7 原文明写目标「不动 ExtractConfig」。
2. `tests/test_schema.py` golden 契约面必受染(字段增 = 序列化面变),守军面扩大,违背
   「手写规则路径零回归」硬门的实现路径。
3. 本流红线:schema.py 与 tests/test_schema.py 零触碰(AGENTS 纪律 + 计划指令)。
4. 源级粒度需求留池档(另立批次须先 `gitnexus impact -r shishi ExtractConfig` 报爆炸半径)。

## 改动清单(research §7 对齐,共 4 文件 + docs)

### 1. `pyproject.toml`(research §4)

`[project.optional-dependencies]` 增组(先例 vision/crawl4ai/simplex 注释风格):

```toml
trafilatura = ["trafilatura>=2.3,<3", "selectolax<1"]
```

- `trafilatura>=2.3,<3`:2.3.0 为 research 实测版;`extract(output_format="json",
  with_metadata=True)` 为钉版稳定面;<3 防上游大版本漂移。
- `selectolax<1` 钉版不可省(research §4):自由解析装 selectolax 1.0.0 撞 Modest 解析器
  移除墙;trafilatura 对 selectolax 无硬依赖(走 lxml 路径),钉版保护的是 MYIA 自身
  extract_html 面。核心 dependencies 的 `selectolax>=0.3.21` 不动(核心依赖零改动)。
- 不进 `all` 组(all 现语义=重引擎全家桶,vision/table 亦不在内;保守不扩)。
- 随后 `uv lock` + `uv sync --all-extras` 刷新本机环境(纪律许可路径)。

### 2. `src/myssia/engines/static_html.py`(核心,LOW 半径)

模块级新增(全在本文件,不碰 fetch_base):

```python
FALLBACK_ENV = "MYIA_EXTRACT_FALLBACK"
FALLBACK_MIN_TEXT_CHARS = 120  # 质量门缺省,夹具标定见下

def _fallback_enabled() -> bool          # 读 env,缺省 False
def _load_trafilatura():                 # 惰性 import;ImportError → WARNING(带安装
                                          # 命令 pip install 'myssia[trafilatura]')→ None
def _trafilatura_fallback(html, url)     # 兜底主体,返回 list[dict] | None
```

`_trafilatura_fallback` 流程:

1. `_load_trafilatura()` None → 返回 None(装不上不拦核心:①已由覆写回落拒载,②维持零条)。
2. `trafilatura.extract(html, url=url, output_format="json", with_metadata=True)`:
   异常 catch → WARNING → None(启发式崩溃不外溢);返回 None/空 → None(启发式判定无正文)。
3. `json.loads` → dict;`text` 缺时退 `raw_text`;正文 `strip()` 后 `< FALLBACK_MIN_TEXT_CHARS`
   → INFO → None(质量门:不过门=视同启发式失败=零条保真)。
4. 过门 → 单条 `{url, title: doc.title or "", content, [published: doc.date], [author:
   doc.author], extract_provenance: "trafilatura"}`;其余 JSON 键不映射直接丢(research §2.2)。

**质量门阈值标定**:缺省 120。夹具实证(research §2.4 矩阵):文章页 203(过)vs 列表退化
78/51(拦)vs 纯导航 6(拦)——120 居中且留有中英正文密度余量;pagetype 判据弃用(四夹具
恒 None,research §3.3-2)。

`StaticHTMLEngine` 两处:

- **覆写 `_check_extract_support`(①的 REQUIRES_EXTRACT 面)**:
  ```python
  def _check_extract_support(self) -> None:
      if (self.source.extract is None and _fallback_enabled()
              and _load_trafilatura() is not None):
          return  # ①兜底放行:开关开+trafilatura 可用,分流进 _fetch_page
      super()._check_extract_support()  # 其余一切分支逐字节走父类现状
  ```
  开关关/未装 → super() 照抛 `extract_required`(现状零行为差);开关开+已装 → 放行。
  覆写而非分流前移:`fetch()` 生命周期(fetch_base.py:2140)零改动,改动面最小。
- **`_fetch_page` 出口分流**(与 rss 分流 :104-115 同构):
  ```python
  extract = self.source.extract
  if extract is None:                     # ① 规则缺失(覆写已保证开关+依赖可用)
      page_items = _trafilatura_fallback(text, url)
      if page_items:
          return page_items, self._next_page_url(text, url), False
      return [], None, True               # 兜底失败=零条,L3 探测信号保真
  ...(rss/list/item 原路径不动)...
  if not page_items:
      if extract.type != "rss" and _fallback_enabled():   # ② rss 结构性不挂
          page_items = _trafilatura_fallback(text, url)
          if page_items:
              logger.info("规则跑空,trafilatura 兜底出条 url=%s", url)
              return page_items, self._next_page_url(text, url), False
      logger.debug("本页提取 0 条,提前收尾 url=%s", url)
      return [], None, True               # 不过门/兜底失败=维持零条语义
  ```
  ③字段级失败零新代码(extract_html 内部语义,本流不碰)。①兜底出条走
  `_next_page_url(text, url)` 与规则出条同构(selector 翻页照常跟,template 翻页照常走)。

### 3. `src/myssia/pipeline.py`(②软信号,research §7-4)

`_stage_fetch` 汇拢循环(pipeline.py:1512)扩 zip 对齐源配置(asyncio.gather 保序),
对「源配了非 rss extract + 条目含 provenance=trafilatura + 选中引擎 static_html」的源挂
一条降级注记:

```python
report.warnings.append({
    "source": ..., "engine": "static_html",
    "error_type": "extract_rules_empty_fallback",
    "message": "规则跑空(整页 0 条),trafilatura 兜底出条;规则选择器疑已失效",
    "fallback_items": n,
})
```

- 走 `StageReport.warnings`(pipeline.py:334-336 既有降级注记通道,enrich 条目级失败先例
  :1924):自动恢复、不翻 run 状态、`resolve_status` 不计 partial。
- ①(无规则)不挂——源没配 extract 就无所谓「规则已烂」;doctor 由源配置即可分辨①②。
- registry/schema 零改动达成(FetchOutcome 不加字段)。

### 4. `tests/engines/test_static_html.py`(新增用例,既有断言零改动)

mock 先例 = tests/vision/test_vision_table.py:216(`monkeypatch.setitem(sys.modules,
"rapid_table", SimpleNamespace(...))`)+ 引擎单例逐例重置(test_registry.py:190 纪律:
sys.modules 假模块注入后缓存须清防串台)。fake trafilatura 形态:

```python
_FAKE_TRAF = SimpleNamespace(extract=lambda html, url, output_format, with_metadata: json.dumps({...}))
monkeypatch.setitem(sys.modules, "trafilatura", _FAKE_TRAF)
```

用例清单(全走 httpx.MockTransport 离线):
1. ①开关开+mock 在 → 出条+键面断言+provenance;翻页正常收尾。
2. ①开关关 → `extract_required` 照旧(零行为差)。
3. ①开关开+trafilatura ImportError(注入假 import 抛错形态:sys.modules 塞 None 即
   import 失败)→ 照旧 `extract_required`。
4. ②规则跑空(list 型)+开关开+正文过门 → 兜底条+`Item.from_extracted` 契约测试
   (published/author/provenance 落 metadata,content 落 Item.content)。
5. ②正文不过门(text 50 字符)→ 零条(质量门)。
6. ② rss 型跑空 → 不兜底,零条(feedparser 路径负向边界)。
7. ③字段级:部分字段 miss 的既有语义用例已覆盖(extract_html 面零改动),不新增。
8. 管线级:`StageReport.warnings` 出 `extract_rules_empty_fallback`(②软信号)+
   ①不挂注记——挂 tests/pipeline/(消费面)或本文件(轻量直调 _stage_fetch 不便,改为
   pipeline 件内新增;守军件既有断言零改动)。

### 5. docs 四处 + README(AC5)

- `docs/zh/getting-started.md` + `docs/en/getting-started.md`:extras 命令区补
  `uv sync --extra trafilatura`,「可选依赖共 8 个」→ 9 个,补**开关双态口径**:
  - CLI/直跑二进制:`MYIA_EXTRACT_FALLBACK=1 myssia run ...`(命令行 env 前缀);
  - 已装 app:`launchctl setenv MYIA_EXTRACT_FALLBACK 1` 后重启 app(open 不透传 shell
    env,main.rs 侧由父进程环境继承;不写全桌面态开法,验收者按 shell export 试必误判
    「开关无效」,给 env 路线埋错翻案证据——计划指令质询补全原文)。
- `docs/zh/schema.md` + `docs/en/schema.md`:sources 表 `extract` 行缺省语义补 L2 opt-in
  兜底一句(「留空时 L3+ 引擎自动结构化兜底」+「L2 static_html 在 MYIA_EXTRACT_FALLBACK=1
  且装 trafilatura extras 时正文兜底」)。
- `README.md` zh/en 两区 extras 命令列表顺带补一行(既有 table 先例同位)。

## 交互面推演(research §3.1 逐项落地的代码面证据)

- **降级链**:兜底成功=static_html 出条 → registry.py:338-351 照常回写 hint、链停 L2;
  兜底失败=零条 → 「static_html 真零结果」L3 探测信号(registry.py:312-337)保真触发。零改动。
- **engine_hints**:与零条也回写同语义(research §3.1-2),provenance 标注消解胜者歧义。
- **失败记账**:①兜底放行后 `extract_required` 失败消失(换来出条,正向);②软信号走
  warnings 不走 failures。

## 环境与实验纪律

- 主环境变更:`uv lock` → `uv sync --all-extras`(纪律许可;绝不裸 sync)。
- 真跑验证:/tmp venv(`uv venv /tmp/traf-impl && uv pip install --python /tmp/traf-impl
  -e . --extra trafilatura 'selectolax<1' trafilatura==2.3.0` 同 research §4 先例),
  离线夹具(复用母任务 evidence/matrix-script.py 的 ARTICLE/LISTING/REVAMPED 同款 HTML),
  零外网零 robots 负担;输出记本档 evidence/。
- 主套件测试不依赖真 trafilatura(全 mock;已装/未装环境都绿——mock 注入 sys.modules
  覆盖真包,import 探测形态两态各有用例)。

## 风险与回退

- 风险面 = static_html 引擎新分支(LOW 半径)+ pipeline 一条注记;缺省开关关 = 行为
  逐字节不变,回退 = 关开关即回现状;代码回退 = revert 4 文件,无 schema/lock 语义耦合
  (uv.lock 仅增 extras 解析条目)。
- 启发式噪声(B2/C3 列表页退化)如实记档不设质量分——质量门只裁出不出条(research §6)。
