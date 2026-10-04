# 技术设计:插件市场批量收录(Phase 2 盘点 → Phase 3 分批落地)

> 前提:D1-D3 已批(prd.md 决议表)。铁律:装不上不拦核心;裁决前不开收录工的闸门已过。
> 本设计只定方法与结构,不预填候选结论(盘点表逐行核实是 Phase 2 的活)。

## 1. Phase 2 盘点方法论

**产出物**:`research/inventory.md`(盘点表,照 supplier-map 惯例:○=待核实/●=已核实)。

每行字段:工具名 | 上游 repo | license | 免费路径 | 形态(库/CLI/服务/平台) | 桌面分级可行性(零 docker?) | 建议归位(a-e) | 一句话理由 | 核实标记。

**核实纪律**(避免静态罗列翻车,教训在册「选池档任务前先对归档验前提」):

- license 以上游 LICENSE 文件原文为准(AGPL=只桩不抄;GPL=submodule 样板照 Photon;BSD/MIT 可直借);
- 免费路径按 connector-selection 硬规则四问(免费层是什么/限多少/自托管可否/留痕在哪),SaaS 型直接走 e 路记档;
- 活跃度看最近提交/发布(>1 年停滞记档,不自动出局但标注);
- 每行结论必须给「归位理由」引用判定框字母,不允许无字母入表。

**归位判定框执行细则**(D1 定案):

- **a 路(进引擎链新档)**必须回答两问:比 scrapling/crawl4ai 强在哪(成本/成功率/反检测维度);降级序插哪一档(答不出=不入链,落 b 或记档);
- **b 路(插件+链外引擎)**照 credhunter 先例:`engine: <name>` 注册 `ENGINE_REGISTRY` 不进 `AUTO_CHAIN`,实现=进程内加载 `plugins/<name>/adapter.py`;显式选用、失败=源级 `dependency_missing` 结构化失败;
- **c 路(remote/server-only 桩)**照 maxun/monitor 先例:manifest 分级+compose 文件+README 自部署指引,核心零依赖;
- **d 路(同物种不收)** Crawlab 型——除非接用户既有部署(仍走 c);
- **e 路(不过关不立项)**仅记档一行,不进市场目录。

**D2 硬规则执行点**:盘点表新增「本地可跑?」列——厂商 SaaS/仅云 API 的候选此列必为 ✗,归位自动落 e(或「文档级可选后端」注记,永不进插件 lane 缺省)。

## 2. Phase 3 收录物结构(每件)

- `plugins/<name>/`:plugin.yaml(manifest:分级/版本/许可摘要)+ README.md(上游署名+装法+限制)+ adapter.py(b/c 路)或桩(c 路);
- 服务端件:`docker/` 增 compose 片段(c 路);
- doctor 集成:`dependency_missing` 降级 warning 验证用例;
- `OFFICIAL_PLUGINS` 清单 + `tests/test_plugins.py` 参数化 + golden 快照同步(教训:改官方插件声明面必同步 golden 基件);
- README「6 official categories」口径修正(AC4,与 tests 权威清单 7 个对齐,顺手在首批批内做)。

## 3. 批次划分原则

- 每批 2-4 件、独立可验、独立提交(禁大爆炸,R4);
- 首批选 **零 docker、BSD/MIT、adapter 形态**的最小风险件(打样收录流水线);平台型(c 路)与引擎链候选(a 路,须降级链设计)靠后,各自单独成批;
- a 路候选单独拆任务(涉引擎链与降级序,复杂度高于收录)。

## 4. 风险与回滚

- 收录件全部 additive(plugins/ 目录新增+清单/golden 同步),单件回滚=删目录+还原清单与 golden;
- 引擎链不动(a 路另拆任务),本任务主线零核心改动;
- 并行会话在场:状态走 task.json 直改,不用 start/finish。

## 5. 首批收录设计(2026-10-05 主人批「按照你的建议去做,尽量都弄上」)

> §1-§4 的首批具体化。盘点表=本档 `research.md`(与 §1 所称 inventory.md 同物,文件名从简);§3 首批选件原则(零 docker/MIT·公域/adapter 打样)在本批兑现,§3 尾句「a 路单独拆任务」兑现为 curl_cffi 留独立任务不动。

### 收录清单与形态裁定

| # | 插件 | 上游/license | tier | 形态 | CLI |
|---|---|---|---|---|---|
| 1 | myssia-media | yt-dlp(Unlicense 公域) | desktop | adapter subprocess(`uv run --with yt-dlp yt-dlp --dump-single-json --flat-playlist`) | `myssia media <url> --json` |
| 2 | myssia-maigret | maigret(MIT) | desktop | adapter subprocess(`uv run --with maigret maigret <user> -J simple --folderoutput <tmp>`;v0.6.6 实测) | `myssia maigret <user> --json` |
| 3 | myssia-theharvester | theHarvester(GPL-2,**submodule**) | desktop | vendor submodule + adapter subprocess(照 Photon;pip 包为空壳不可用,2026-10-05 实测) | `myssia harvester <domain> --json` |
| 4 | myssia-rsshub | RSSHub(AGPL,**只桩不抄**) | remote | manifest remote 桩 + compose + README(自部署优先;公共实例=第三方留痕,P0 注记) | — |
| 5 | myssia-spiderfoot | SpiderFoot(MIT) | remote | **改判 b→c**:不在 PyPI(2026-10-05 实测 no solution)+Web 服务优先形态,进程内故事不成立;官方镜像自部署+REST | — |

### 关键裁定(Ruling)

- **R-1 版本策略**:yt-dlp/maigret 走 uv `--with` 不钉版(yt-dlp 抽取器时效即生命、maigret 站点库自更新;uv 缓存隔离零污染根依赖;测试全 mock 可复现);theHarvester 因 GPL 纪律 submodule 钉 commit。
- **R-2 CLI 接线**:只加 media/maigret/harvester 三个子命令(rsshub/spiderfoot 桩无 CLI);命令名直白用上游名;每命令 `_add_*_parser`+失败码→退出码照 osint 先例。
- **R-3 错误契约**:每 adapter 结构化异常(code+message+details.to_dict()),code 词表照 osint(`uv_missing`/`*_failed`/`*_timeout`/`*_output_invalid`);失败绝不拦核心。
- **R-4 引擎面**:首批零新引擎(不动 schema EngineName/registry/AUTO_CHAIN)——链外引擎化进情报流是后续批次按需另立;本批交付=市场包+一键 CLI。
- **R-5 测试**:adapter 单测照 test_osint_plugin(mock subprocess 零网络);包契约并入 test_plugin_packages.py(OFFICIAL_PACKAGES+EXPECTED_TIERS);新测试落 tests/plugins/。
- **R-6 compose**:rsshub/spiderfoot 部署件落 docker/plugins/<id>/compose.yml(插件目录零 compose)。

### 各件数据面

- **media**:items={title,url,channel,uploader,duration,view_count,upload_date,item_count(频道/列表)};url_invalid/media_failed/media_timeout/output_invalid。
- **maigret**(`-J simple`):items={site,username,url,status};top_sites/timeout 可调;无命中=空态成功。
- **harvester**(`-f json`):emails/hosts/ips 按 lane 聚合;vendor_missing 码照 osint。
- **rsshub**:endpoint 占位 example.com;README 教 RSS 路由→品类 `extract.type: rss`(news.yaml 同通路)。

### 改动面

新增 5 个 `plugins/myssia-*/`(plugin.yaml+README[+adapter.py][+vendor]);`src/myssia/cli.py` 加 3 组 parser/handler;`.gitmodules` +1;`tests/plugins/test_plugin_packages.py` 清单+3 个新测试文件;`docker/plugins/myssia-{rsshub,spiderfoot}/compose.yml`;README zh/en 品类数 6→7(AC4,顺批做)。

