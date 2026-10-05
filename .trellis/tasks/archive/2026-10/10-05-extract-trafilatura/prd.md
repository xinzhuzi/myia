# 引擎链评估:trafilatura 零配置正文抽取(extract 面增强)

## Goal

评估 trafilatura 为 extract 面增强:**零配置正文自动抽取**——不写规则也能从任意文章页剥掉导航/广告/排版噪音,拿到干净正文+标题+时间+作者(`.trellis/tasks/10-05-plugin-market-batch/research.md` 第六波结案原文)。定位=补手写 extract 规则的结构性盲区、**兜底而非首选,互补不是替代**;须答与手写规则的共存边界才准动手。

## 背景与证据(全部引自 10-05-plugin-market-batch 既有档)

- **结案依据(第六波,AC9 批二步骤 14 已毕)**:L2 `static_html` 的结构化靠**逐源手写 extract**(品类 YAML 的 json_path/css 选择器)——字段精确但只覆盖写过规则的源;trafilatura(Apache-2.0,6.9k 星,活跃)补的正是两个结构性盲区:**「无规则长尾源」**与**「改版后规则失效时的兜底」**;成本=核心依赖 +1(纯 Python 无浏览器,重量可接受);风险=启发式在列表页/非文章页退化为噪声,须挂正确档位而非全量接管;**结案建议=另立引擎任务,判定框 a 路两问必须先答**(research.md 第六波)。
- **归位轨迹**:第二波「观察(核心 extract 能力增强候选):语义属『URL→结构化内容』核心侧而非插件,与 L2 手写 extract 规则互补」;第三波「a/b 候选(引擎侧另立任务)」;第四波 D4 回写「extract 增强另立任务(AC9),无门槛,须答『比手写 extract 强在哪』」——三波归位一致,件已随母任务 AC9 结案拆到本档。
- **宪法约束**:Apache-2.0 可直借、本地纯 Python、零成本(D2 硬规则过);「URL→结构化内容」语义属引擎侧非插件层(D1 两层分工)。

## 定案问题(planning 期必答,答完才开设计)

1. **与手写 json_path/css 规则的共存边界**(本任务核心问):候选模型=「手写规则命中→用规则(精确字段映射优先);规则缺失/失败→trafilatura 兜底(正文形态最优)」——但边界细节须定:兜底触发条件(规则缺失?规则跑出空/异常?改版后字段级失败?)、输出契约(兜底路径的字段面与手写路径如何对齐 items schema)、以及兜底结果是否标注 provenance(可区分「规则产出」与「启发式产出」)。
2. **挂点档位**:候选=「static_html extract 缺失/失败时的回退」或 enrich 平行(research.md 第六波原列两候选,属引擎链设计)——须回答挂在哪一层、对降级链/`engine_hints`/失败记账有无影响;启发式噪声风险(列表页/非文章页退化)如何被挂点选择天然约束。

## Requirements(骨架,planning 期细化)

- R1:共存边界与挂点定案(上两问)入 `research.md`,含逐源行为矩阵(有规则源/无规则源/改版失效源三列)。
- R2:依赖面:trafilatura 进可选依赖纪律(`dependency_missing` 不拦链)的路径;核心 6 依赖红线合规(`.trellis/spec/python/index.md`)。
- R3:抽取质量无硬断言的现实接受:定位=兜底,验收以「手写规则路径零回归」+「无规则源拿到可用正文」为准,不给启发式设硬性质量门。
- R4:若定案动引擎链:改动清单+爆炸半径(GitNexus impact);若定案不动链(enrich 侧):挂点模块与失败语义同样记档。

## Acceptance Criteria(骨架)

- [x] AC1:共存边界定案(触发条件/输出契约/provenance)记档,逐源行为矩阵在档。
  ——回填(2026-10-05):research.md §2(三分触发:①规则缺失→兜底主路/②规则跑空→质量门后兜底/③字段级失败→不兜底;输出契约=`{url,title,content[,published,author]}` 零新键对齐 items schema;provenance=`metadata["extract_provenance"]="trafilatura"` 仅兜底条目,规则路径零新键)+§2.4 三列行为矩阵(离线夹具真跑,evidence/matrix-output.json)。
- [x] AC2:挂点档位定案(回退 vs enrich 平行)记档,与降级链的交互面说清。
  ——回填(2026-10-05):research.md §3 定案=static_html 引擎内回退;降级链/engine_hints/失败记账逐项推演(§3.1),enrich 平行三重架构性否决理由(§3.2),启发式噪声=触达面天然窄+产出质量后验门(§3.3,pagetype 判据实证不可用)。
- [x] AC3:手写规则路径零回归=硬门;trafilatura 路径=可用性验收(AC 定案时细化)。
  ——回填(2026-10-05):research.md §5 守军清单(处理域文件面 7 件行号级+测试面 9 件逐名)为硬门勾选依据;§6 验收口径定案(可用性判据=「无规则源拿到可用正文」A2/C2 形态;噪声如实记档不设质量分门)。
- [x] AC4:本任务止于评估定案+设计;planning 期零核心文件改动。
  ——自查声明(2026-10-05):全程仅写本档目录内文件(research.md/evidence/ 五件/prd.md/task.json),`git status --porcelain` 每步核对,核心文件(src/tests/pyproject)零改动零暂存;依赖实证走 /tmp/traf-eval venv,不碰仓库环境。

## Constraints

- 装不上不拦核心铁律:trafilatura 缺失=手写规则路径照常,兜底能力结构化降级。
- 启发式永不全量接管:定位「兜底」不是「首选」(research.md 第六波风险条原文)。
- 核心管线改动先报爆炸半径(AGENTS.md GitNexus 纪律)。

## Notes

- 2026-10-05 建档(「两引擎任务建档」路,与母任务批三并行会话互不阻塞)。母任务:`.trellis/tasks/10-05-plugin-market-batch/`(research 第六波结案/第二三四波归位/AC9 回标)。
