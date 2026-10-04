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

- [ ] AC 回填;e 路记档汇总(不立项清单)入 research/;
- [ ] 每批独立提交;跨批不共享半成品。

## 回滚

- 单件:删 `plugins/<name>/` + 还原 OFFICIAL_PLUGINS/golden;
- 整批:revert 批次提交;零核心改动,无数据迁移。

## 批二:D4 门槛机制+门槛件+分析件(2026-10-05 晚立,按依赖序)

10. [ ] **门槛机制先行**(R5,其余件的地基):`src/myssia/gates.py`(gates.yaml fail-closed 装载,照 vision/settings.py)+ manifest `TIER_TOKENS`+`gated`+plugin list 分组+doctor info finding+测试;
11. [ ] **设置面门槛件分区**(R5 尾):桌面 SECTIONS 第 5 分区+sidecar `gates.get/save` 两方法(main.rs 白名单)+三卡表单+知情文案+UI 测试;
12. [ ] **付费 SaaS gated 引擎**(R6):zenrows/scraperapi 引擎模块(词表+注册表不进 AUTO_CHAIN+gate_closed 失败类+keychain 键解析)+MockTransport 测试(关闭态/开启态往返);
13. [ ] **同物种门槛桩**(R7):myssia-crawlab+myssia-worldmonitor(remote,gated tier,compose+README 门槛说明)+EasySpider 形态核验结案记档;
14. [ ] **分析件二批**(AC9):myssia-webcheck+myssia-socialanalyzer(remote 桩)+trafilatura extract 增评估结案(独立任务或并入,答增量问);
15. [ ] 许可核验批:MediaCrawler/yake/weibo-search/SpiderKeeper 许可原文核验(仓库 LICENSE 一手),可进则进、不可进如实挂起;
16. [ ] 门禁与提交纪律同首批(单件单提交、tests/plugins 组绿+批末全量、快照外科防并行混线)。
