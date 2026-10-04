# Implement:10-04-alert-rules

> 契约权威 = 本档 design.md(决议展开);开工前重读 PRD「Grill 决议(2026-10-04)」节。
> 查改分家:每 Stage 动手前先 Read 对应白名单文件现状(行号以当日实读为准,design 行号为 2026-10-04 口径)。

## Stage 0:基线与占位定案

- [ ] 0.1 `uv run pytest -q` 记录基线(预存红以 stash 归因 HEAD 树);`git status` 快照留档
- [ ] 0.2 **协议版本占位定案**(design §4.4):实读 `desktop/entry.py` `PROTOCOL_VERSION` 当前值与 `.trellis/spec/desktop/sidecar-protocol.md` 对账行数——仍为 6/43 则本批 v7(43→47);hermes-cron 已占 v7 则本批 v8(镜像表注明顺延)。以下按 v7 书写,v8 同形
- [ ] 0.3 并行流再核:`git status` 下 messaging 屏在途改动面(design §9 已核 2026-10-04 仅注释更名)

## Stage A:存储层(自底向上,每步独立可测)

- [ ] A1 `src/shishi/store/models.py`:`AlertRule` / `AlertFired` dataclass(design §2.3;FeedbackRecord slots 先例)
- [ ] A2 `src/shishi/store/sqlite.py`:`SCHEMA_VERSION` 6→7;`_SCHEMA` 基线增两表两索引(design §2.1);`_migrate_v7_add_alerts` 入 `_MIGRATIONS` 链(CREATE TABLE IF NOT EXISTS 幂等,`_migrate_v4_add_feedback` 同构)
- [ ] A3 `src/shishi/store/base.py`:Protocol 扩九方法族(design §3 表:save/list/delete_alert_rule、record_fired、mark_alert_fired_status、has_fired、list_fired、fired_counts、update_item_tags),契约 docstring 逐方法同步
- [ ] A4 `src/shishi/store/sqlite.py`:九方法 SQLiteStore 实装(record_fired = INSERT + UNIQUE 冲突捕获返 None;list_fired 的 since 过滤 + limit 钳制 [1,200])
- [ ] A5 `tests/test_store_alerts.py`(新):design §11 store 行全用例
- [ ] **门禁 G1(存储成形)**:`uv run pytest -q tests/test_store_alerts.py` 全绿;旧 v6 库打开自动升级且幂等重放零数据迁移用例过;全量回归零新红

## Stage B:规则引擎

- [ ] B1 `src/shishi/alerts/rule.py`:`AlertRule` + `AlertConfigError` 构造期拒(design §5.1;RouteRule.__post_init__ 同构:Rule 试建捕 RuleSyntaxError)
- [ ] B2 `src/shishi/alerts/engine.py`:`alert_view`(view() + `ctx['content']` 补丁,不改 `Item.view()`)+ `AlertEngine`(求值循环;动作执行器接收 channel 工厂与 registry 注入,不 import Pipeline)
- [ ] B3 `src/shishi/alerts/__init__.py` 再导出;`tests/test_alert_engine.py`(新):design §11 引擎行全用例(构造期拒全形态/资源护栏/content 补丁/mute 硬定律/score=None 隔离)
- [ ] **门禁 G2(引擎成形)**:`uv run pytest -q tests/test_alert_engine.py` 全绿 + 全量零新红;`Item.view()` 零波及(route 求值用例原样绿)

## Stage C:管线挂点

- [ ] C1 `src/shishi/pipeline.py`:`_alert_pass` 附加步(design §6.1 时序:dry 短路→空规则短路→tuning/mute 词表→逐条 mute 预筛→逐规则求值→占坑→动作→回填状态);挂 `run()` 阶段循环后、maintenance 前;输入 = `result.items`(broken 空集跳过);不进 STAGE_OPTION_NAMES/RESUME_CHECKPOINT_STAGES/EXECUTED_STAGES、不写 runs.steps
- [ ] C2 动作接线(design §7):push = 当前品类 `push[]` 同类型第一条 `_build_channel` + `send_immediate`(共享 run registry);降级 WARNING + `degraded_no_channel`;tag = `add_tags` + `update_item_tags` 两步回写
- [ ] C3 `tests/test_alert_pipeline.py`(新):design §11 管线行全用例——**零惊扰(不配规则全量回归零新红)为第一用例**;双向压制两方向;至多一次(占坑冲突/重跑);dry-run 零落库零发送
- [ ] **门禁 G3(挂点成形)**:`uv run pytest -q tests/test_alert_pipeline.py` 全绿;全量 `uv run pytest -q` 零新红(既有 route/digest 测试全绿)

## Stage D:协议 + CLI

- [ ] D1 `desktop/entry.py`:`_m_alerts_list/save/delete/test` 四处理器(design §4.1;save 全量替换两道门 + diff 保 id;test 三取材 + dry 不落不发)+ `_HANDLERS` 注册 4 行 + `PROTOCOL_VERSION` → v7;run 终态收口处 `alerts.fired` 回放(design §4.3 主路线:list_fired(since=run.started_at) 逐条 _write_line)
- [ ] D2 `tests/test_desktop_sidecar_protocol.py` 增:四方法契约/错误码(alert_rule_invalid/alert_not_found/item_not_found/alert_test_no_item)/版本断言/fired 回放事件用例(design §11 协议行)
- [ ] D3 `src/shishi/cli.py`:`shishi alerts list` 只读子命令(design §8;feedback parser 先例);`tests/test_cli.py` 增用例
- [ ] D4 `.trellis/spec/desktop/sidecar-protocol.md`:方法表增 alerts 段 4 行(43→47;v8 则注明顺延)+ 事件族补 `alerts.fired` + 错误码入表;与 `_HANDLERS` 机器对账(method_not_found 的 data.allowed)
- [ ] **门禁 G4(协议成形)**:`uv run pytest -q tests/test_desktop_sidecar_protocol.py tests/test_cli.py` 全绿;spec 对账一致(方法数 = 镜像表行数)

## Stage E:消息屏子面板

- [ ] E1 `desktop/ui-src/src/lib/api/types.ts` + `screens/messaging/api.ts`:AlertRuleView 输入/视图类型 + `alertsList/alertsSave/alertsDelete/alertsTest` 四调用
- [ ] E2 `screens/messaging/messaging-screen.tsx`:推送规则面板后追加「告警规则」Card(design §9 布局:列表行/启停 Switch=全量提交/表单/测试结果面板/空态/删除二次确认;channel 下拉 + 降级提示文案)
- [ ] E3 webview `alerts.fired` 事件消费:toast + 命中数刷新
- [ ] E4 `screens/messaging/messaging-screen.test.tsx` 增 vitest 用例(design §11 UI 行);`npm run build`/`tsc` 过
- [ ] **门禁 G5(UI 成形)**:vitest 全绿 + tsc 零错;dev 实机手验:建规则→启停→测试(dry)→真发借 push.test→run 触发→fired 事件 toast→命中数刷新

## 收尾

- [ ] C1 全量 `uv run pytest -q` 零新红;UI 侧 `npm test` + `npm run build` 过
- [ ] C2 `gitnexus detect-changes -r shishi --scope staged` 核验改动面(预期:store/alerts/pipeline/entry/cli + ui messaging 屏;核心依赖零动)
- [ ] C3 spec 对账终核:sidecar-protocol.md 行数与方法注册表一致;PRD AC 逐条勾验
- [ ] C4 提交分批:A 存储 / B+C 引擎+挂点 / D 协议+CLI / E UI,逐批 detect-changes
- [ ] C5 回滚验证:删除 `src/shishi/alerts/` + 还原 pipeline/entry/cli/store 改动 = 净回滚;alert_rules/alert_fired 表无害残留(空表)

## 回滚点

- G1 前:纯 store 改动,`git checkout` 即净
- G3 后:删 `src/shishi/alerts/` + pipeline 挂点还原;两表残留无害(空表不参与任何现有查询)
- G5 后:同上 + UI 子面板还原;messaging 屏其余功能零牵连(并行流已核,design §9)

## 验证命令速查

```bash
uv run pytest -q tests/test_store_alerts.py tests/test_alert_engine.py tests/test_alert_pipeline.py
uv run pytest -q tests/test_desktop_sidecar_protocol.py tests/test_cli.py
uv run pytest -q                                   # 全量回归(零惊扰门禁)
uv run shishi alerts list                          # CLI 只读历史
gitnexus detect-changes -r shishi --scope staged
cd desktop/ui-src && npm test -- messaging-screen  # vitest
```
