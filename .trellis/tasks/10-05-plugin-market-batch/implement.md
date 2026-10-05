# 执行计划:插件市场批量收录(Phase 2 盘点 → Phase 3 分批)

> 决议:D1-D3(prd.md);方法与结构:design.md。Phase 1 已毕(AC1 ✓)。

## Phase 2:全量盘点(R2/AC2)

1. [x] 盘点表落 `research.md`(27 行/6 形态类;§1 所称 inventory.md 同物,文件名从简);
2. [x] 逐行核实(gh api license/星数/活跃度快照 2026-10-05;○ 项=实施时核,记「未核项」节);
3. [x] 覆盖 6 形态类 27 工具(AC2 口径超额);
4. [x] 主人过目并批「按照你的建议去做,尽量都弄上」= 首批 5 件定稿(design §5)。

## Phase 3+:分批收录(R3/R4/AC3,每批循环)

5. [x] **首批 5 件**(design §5:media/maigret/theharvester 桌面 adapter 件+rsshub/spiderfoot remote 桩),单件单提交:
   - [x] 5a myssia-media(yt-dlp 公域,不钉版 R-1):adapter+`myssia media` CLI+测试 396 绿+真网 E2E(Big Buck Bunny 8.3s);提交见 git log;
   - [x] 5b myssia-maigret(MIT):adapter(报告契约 v0.6.6 实测:命中在条目 status 键下)+`myssia maigret` CLI+测试 427 绿+真网 E2E(torvalds 6 站 18s);
   - [x] 5c myssia-theharvester(GPL-2 submodule 钉 4.9.2:master 49a38f8d 含 Py2 语法残留不可运行,退稳定 tag 记档;uv --no-config 隔离+-c 唤上游入口)+`myssia harvester` CLI+钉版依赖同源校验+真网 E2E(example.com crtsh+dnsdumpster exit 0);**提交事故记档:全套曾入并行 b26af14,对方 amend 退回工作树,重提交净版**;
   - [x] 5d+5e myssia-rsshub(AGPL 只桩,自部署优先/公共实例留痕注记)+myssia-spiderfoot(MIT,不在 PyPI+Web 形态 b→c 改判):compose 集齐七件,测试 518 绿;合并一笔(孪生桩);
   - 并行会话同批加 myssia-urlwatch(BSD-3 上游,desktop),非本批清单但同任务语境,互不阻塞;
6. [x] 门禁:tests/plugins 组 518 绿;`myssia plugin install+list` 沙箱冒烟过(myssia-media desktop 可见);装不上场景 doctor 降级 warning=包契约测试既有钉(test_plugin_packages 契约三);批末全量门禁跑毕勾回(见 AC3 注);
7. [x] README「6 official categories」→7 口径修正(AC4):并行会话顺手完成(265b7a9,双语两处);
8. [ ] 主人过目首批 → 后续批次按同循环推进(TikTokDownloader 备选/○ 项核实在册);
9. [ ] a 路候选(curl_cffi/trafilatura)不在本任务做:单独拆任务(引擎链+降级序设计)。

## 收尾

- [x] AC 回填(批二 AC6-AC9:批二回标+2026-10-05 批二收口审计复核一行回标,见 prd 收口段;AC5 之 [x] 系并行批三会话在途回标 commit pending,本步未核验、留批三收口);e 路记档汇总=research.md 第四波(e 路门槛化重标注)/第五波(核验终态:weibo-search/SpiderKeeper 无 LICENSE、EasySpider 形态不可接,均维持不收;文件在档根 research.md,design §1「文件名从简」同款);
- [x] 每批独立提交;跨批不共享半成品(批一 6 笔/批二 7 笔单件单提交;golden 未随件提交事故与教训=evidence/batch-2-report.md §四,aa89aa5 收编闭环)。

## 回滚

- 单件:删 `plugins/<name>/` + 还原 OFFICIAL_PLUGINS/golden;
- 整批:revert 批次提交;零核心改动,无数据迁移。

## 批二:D4 门槛机制+门槛件+分析件(2026-10-05 晚立,按依赖序)

10. [x] **门槛机制先行**(R5,其余件的地基):`src/myssia/gates.py`(gates.yaml fail-closed 装载,照 vision/settings.py)+ manifest `TIER_TOKENS`+`gated`+plugin list 分组+doctor info finding+测试。**(2026-10-05 批二回填:按 D5 落地=gate 独立字段、TIER_TOKENS 不动;主体 gates.py/manifest.py/cli.py(gates 命令族+plugin list 分组+doctor gate_disabled=info)/SKILL.md 先随并行收编 d613310 入库,本批补 sidecar gates.get/save(entry.py,坏文件 fail-closed 全关+error 带回/同门校验失败零写入)与 tests/test_gates.py,落账 fa10443;门禁实跑见 evidence/batch-2-report.md)**;
11. [x] **设置面门槛件分区**(R5 尾):桌面 SECTIONS 第 5 分区+sidecar `gates.get/save` 两方法(main.rs 白名单)+三卡表单+知情文案+UI 测试。**(批二回填:84533ee——main.rs 实无方法级白名单、rust 零改动,gates.yaml 拒载=fail-closed 警示卡+保存即覆写修复,分析件卡 D8 禁用占位;协议版本**定案不随批 bump**(维持 v10,两方法在 v10 内交付,测试 docstring 记因 tests/desktop/test_desktop_sidecar_protocol.py:2308);执行中报过的 v11 契约红已随定案消解)**;
12. [x] **付费 SaaS gated 引擎**(R6):zenrows/scraperapi 引擎模块(词表+注册表不进 AUTO_CHAIN+gate_closed 失败类+keychain 键解析)+MockTransport 测试(关闭态/开启态往返)。**(批二回填:60e2f52——共用骨架 engines/saas.py,关闭态零上游请求,apikey mask 不落日志;执行中报过的 SKILL.md 枚举表连锁红已闭(SKILL.md:57 含两 token,test_skill_doc 24 绿);遗留低危两条见 evidence/batch-2-report.md 复审处置表)**;
13. [x] **同物种门槛桩**(R7):myssia-crawlab+myssia-worldmonitor(remote,gated tier,compose+README 门槛说明)+EasySpider 形态核验结案记档。**(批二回填:7df322b(crawlab,BSD-3 官方镜像 compose)/0195806(worldmonitor,AGPL 只桩,compose 构建上下文钉上游 tag v2.10.0)——D5 落地=`tier: remote`+`gate: platform`,README 指设置面「自有实例」表单+规范键名 myia/platforms/<name>-token;compose 集**实为 10 件**(卡面 7→9 系本步单步语言,webcheck 同批也配 compose,与卡面文件清单自洽的总数=10,桩件路已如实报;golden 断言同步未随 4a/4b 提交=复审 high,aa89aa5 收编闭环);EasySpider 终态不收(第五波)**;
14. [x] **分析件二批**(AC9):myssia-webcheck+myssia-socialanalyzer(remote 桩)+trafilatura extract 增评估结案(独立任务或并入,答增量问)。**(批二回填:66ace59(webcheck,MIT 官方镜像 compose)/cd29e0f(socialanalyzer,AGPL 只桩不携 compose,与 cd29e0f 同笔附 research.md 第六波 trafilatura 结案=零配置正文抽取补手写规则两盲区,另立引擎任务);D8 裁剪照办——gates.analysis 仅 schema+设置面占位「批三解锁」,零分析件;D9 backlog 照记)**;
15. [x] 许可核验批(gh api LICENSE 原文一手,结论 research.md 第五波):MediaCrawler=非商业学习许可(警示型批三裁)/yake=AGPL 双许可(门槛可清,批三候选)/weibo-search+SpiderKeeper=无 LICENSE(维持不收终态);EasySpider 形态核验同批结案=Electron GUI 无 API,维持不收(终态);
16. [x] 门禁与提交纪律同首批(单件单提交✓;tests/plugins 组绿=批二落账前后两跑 1144 passed/30 skipped(evidence §三)+批二回填任务书门禁 1182 passed/30 skipped+批二收口步 G1(tests/plugins+tests/test_gates.py)退出码 0;批末全量=aa89aa5 收编回执全量 4074 过;快照外科=批二落账纪律,evidence §一)。

## 批一终局快照(2026-10-05 深夜回填;「之前做好的」全量对账)

**实际落地 6 件**(两路会话合奏,单件单提交):

| 件 | 提交 | 形态 | 验证 |
|---|---|---|---|
| myssia-media | `0f491fb` | desktop adapter+`myssia media` | 真网 E2E 8.3s |
| myssia-maigret | `09abb67` | desktop adapter+`myssia maigret` | 真网 E2E 6 站 18s |
| myssia-theharvester | `6ba242e` | desktop submodule 钉 4.9.2+`myssia harvester` | 真网 E2E exit 0;提交收编事故(b26af14→amend 退回→净版重提交)已记 |
| myssia-rsshub+myssia-spiderfoot | `85bfdab` | remote 桩对+compose 集齐 7 | manifest 契约+compose 验证 |
| myssia-urlwatch(并行线) | `f2d08dc` | desktop adapter(上游 Python API 面非 CLI,2.29 源码亲核) | file:// 零网络双跑+25 例契约 |
| README 品类数 6→7(AC4) | `265b7a9` | 双语两处 | — |

**终态数字**:官方场景件 **13**(desktop 7:proxy/osint/credhunter/media/maigret/theharvester/urlwatch;remote 4:credentials/monitor/rsshub/spiderfoot;server-only 2:douyin/maxun);CLI 侦察/采集面新增 media/maigret/harvester 三命令;tests/plugins 组 518 绿,全量 3766 passed/0 failed(88s);docker/plugins compose 7 件;submodule 2 个(Photon+theHarvester)。

**任务状态**:批一交付、task.json 曾置 review(ce9878d);D4 裁决+批二立档后回 in_progress。

## 批二执行卡(2026-10-05 深夜深化:精确文件/命令/期望输出)

### 10. 门槛机制地基(R5)

- 新建 `src/myssia/gates.py`:照 `src/myssia/vision/settings.py` 同款(GATES_FILE_NAME="gates.yaml";`GatesConfig` 构造即校验非法拒构造;`load_gates_config(path)`;坏文件=LoadError 结构化+调用侧全关);路径解析挂 `desktop/entry.py` `_serve_context()` 优先级链(显式 params>MYIA_HOME env>bundle 探测>dev cwd,与 vision.yaml 同位)
- `src/myssia/plugins/manifest.py`:新增可选字段 `gate: paid|trace|platform|stale`(D5:独立字段,TIER_TOKENS 不动;校验=词表+未知字段拒);`src/myssia/cli.py` `_plugin_list` payload 加门槛件分组与 `enabled` 徽标(gates.yaml 状态派生);doctor:未启用门槛件=info finding(词表区分 warning/info)
- `src/myssia/cli.py` 新命令族 `myssia gates show --json` / `gates set <kind>.<name> <on|off>`(D7;saas/platforms 逐件 on 缺 keychain 键=结构化拒);`skill/SKILL.md` 清单同步一行
- 测试:`tests/test_gates.py`(根级,`test_secrets.py` 先例——根模块映根文件):装载/坏文件全关/未知字段拒/每开关往返/gates CLI show-set 往返/逐件 on 缺键拒
- 命令:`uv run --no-sync python -m pytest tests/test_gates.py tests/plugins -q` 期望全绿

### 11. 设置屏门槛件分区(R5 尾)

- `desktop/entry.py` `_HANDLERS` 注册 `gates.get`/`gates.save`(**main.rs 无方法级白名单,rust 侧零改动**——协议权威在 entry.py,通用路由);gates.save 走 tmp+rename 原子写
- `desktop/ui-src/src/screens/settings/settings-screen.tsx`:`SECTIONS` +`{id:"gates", label:"门槛件"}`;三卡表单(付费/自有实例/分析件)每开关挂知情警示;`desktop/ui-src/src/lib/api/types.ts`+`client.ts` 加 GatesView/gatesGet/gatesSave
- 文档同步:`.trellis/spec/desktop/sidecar-protocol.md` 方法表 +2 行(zh/en docs 若提及设置分区同步)
- 测试:`desktop/ui-src` settings 测试扩展 + `tests/desktop/test_desktop_sidecar_protocol.py` gates 两方法用例;命令 `npm --prefix desktop/ui-src test -- settings` + `uv run --no-sync python -m pytest tests/desktop -q`

### 12. 付费 SaaS gated 引擎(R6)

- `src/myssia/schema.py` EngineName 词表(~L153)+=`zenrows`/`scraperapi`(显式选用语义,AUTO_CHAIN 不动);`src/myssia/engines/zenrows.py`+`scraperapi.py`:fetch 前置查 gates(总开关+件开关),关闭→`FetchError(class="gate_closed")`(新失败类,doctor 文案与 dependency_missing 分开);开启→keychain 解 api_key→httpx 调上游 REST(Zenrows/ScraperAPI 均为 GET ?url=…&apikey=… 形态**已核 ●**:Zenrows `GET api.zenrows.com/v1/?apikey=&url=&js_render=true`(可选 premium_proxy/css_extractor);ScraperAPI `GET api.scraperapi.com/?api_key=&url=`(可选 country/render);同薄形态→共用一个 SaaS fetch 骨架,research 第五波)
- `src/myssia/engines/registry.py` ENGINE_REGISTRY +2(链外,credhunter 先例位)
- 测试:`tests/engines/test_saas_gated_engines.py`:三态=关闭态 gate_closed/开启态 MockTransport 往返/注册表断言不在 AUTO_CHAIN
- 品类示例:`plugins/` 不加新品类 yaml(gated 引擎属用户显式 engine 选择,README 文档指路)

### 13. 同物种门槛桩(R7)

- 新建 `plugins/myssia-crawlab/`+`plugins/myssia-worldmonitor/`(plugin.yaml **`tier: remote`+`gate: platform`**(D5 组合)+modes.remote.endpoint 占位+README 门槛说明「自有实例例外通道,组织性不执法」);`docker/plugins/<id>/compose.yml` ×2(compose 集合断言 7→9)
- `tests/plugins/test_plugin_packages.py`:OFFICIAL_PACKAGES+EXPECTED_TIERS(gated 档)+compose 期望集;EasySpider 形态核验**已毕(第五波)**:Electron GUI 无 API→门槛条件不成立维持不收(终态);桩件仅 crawlab+worldmonitor 两件

### 14. 分析件二批(AC9)

- `plugins/myssia-webcheck/`+`plugins/myssia-socialanalyzer/`(remote 普通桩,无门槛;web-check MIT 自部署 compose;social-analyzer AGPL 只桩)
- trafilatura extract 增强结案:research.md 写评估结论(回答「比手写 extract 规则强在哪:零配置正文自动抽取 vs 逐源手写 json_path/css」;若立项→独立引擎任务引用本档)
- **D8 裁剪**:gates.analysis 仅 schema+设置面占位(禁用态「批三解锁」),零分析件;批三前置质询题记档:「分析 lane 挂点=classify 后处理还是 enrich 平行?」
- **D9 backlog**:公共实例 endpoint 检测(rsshub.app 清单→doctor info)留批三随 analysis lane 一起议

### 15. 许可核验批(AC8 尾)

- **已毕(2026-10-05 深夜)**:结论在 research.md 第五波——MediaCrawler=非商业学习许可(警示型收录留批三)/yake=AGPL-3.0 双许可(门槛可清,批三分析件候选)/weibo-search+SpiderKeeper=无 LICENSE 文件(维持不收,终态);EasySpider=Electron GUI 无 API(门槛条件不成立,维持不收终态)

### 16. 纪律(同批一)

单件单提交;tests/plugins 组绿+批末全量;并行会话在场→快照外科暂存+状态直改 task.json;提交前 gitnexus detect-changes(索引已刷新,`-r shishi`)。
