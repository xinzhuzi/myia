# 执行记录——tests 按模块分组 + 分类器测试迁包

补建说明:本任务按轻量任务走 PRD-only,主人在两轮 grill 深化后令补全执行侧文档——94 文件→14 组的**权威映射**与**归组规则**原先只存在于已清理的临时迁移脚本,本档将其固化为档案(映射从迁移后磁盘逐组重取,非转抄)。

## 归组规则(判定顺序)

1. **按被测对象,不按 import 形态**:import 了 `myssia.pipeline` 但测的是告警规则的 `test_alert_rules` 归 `alerts/`;import 了 `myssia.dedup` 但测推送矩阵的 `test_push_channels` 归 `push/`。
2. **跨测试文件 import 必须同目录**:`test_yaml_editor_protocol_gaps` 依赖 `test_desktop_sidecar_protocol` 的 `EDITOR_YAML/_editor_plugins/rpc`,双双落 `desktop/`。
3. **特性横切测试**(串多模块的端到端特性)归 `pipeline/`(如 trend baseline 串 schema+store+push 模板)。
4. **CLI 命令族归 cli/**:skill_install/sources_write_surgery 测的是 `myssia` 子命令。
5. **独立包的语义测试随包走**:`test_classify.py` → `myssia-classifier/tests/`,且零 `myssia.` 依赖(直引 `myssia_classifier`,含 caplog logger 名);主包 `classify/test_classifier_package.py` 只测 shim 同一性与独立发行契约(镜像 `src/myssia/classify` shim 的存在)。
6. **分不清被测对象 = 横切**,才许落根(docs/schema/secrets/skill_doc/smoke/trellis 守卫)。

## 权威映射(94 文件,迁移后磁盘逐组重取)

- **tests/alerts/**(1): test_alert_rules
- **tests/classify/**(1): test_classifier_package
- **tests/cli/**(5): test_cli, test_cli_channels, test_cli_full, test_skill_install, test_sources_write_surgery
- **tests/cron/**(7): test_cron_executions, test_cron_jobs, test_cron_occurrences, test_cron_runner, test_cron_schedule, test_cron_store, test_cron_tick
- **tests/credhunter/**(6): test_credhunter_credcheck, test_credhunter_exposure, test_credhunter_fingerprints, test_credhunter_ghhunt, test_credhunter_keystore, test_credhunter_wiring
- **tests/desktop/**(2): test_desktop_sidecar_protocol, test_yaml_editor_protocol_gaps
- **tests/engines/**(11): test_crawl4ai, test_direct_api, test_fetch_base, test_firecrawl, test_llm_browser, test_proxy_pool, test_proxy_transport, test_registry, test_scrapling, test_static_html, test_stealth
- **tests/enrich/**(2): test_aggregate, test_enrich
- **tests/feedback/**(1): test_feedback
- **tests/pipeline/**(2): test_baseline, test_pipeline
- **tests/plugins/**(6): test_demo_plugin, test_osint_plugin, test_plugin_packages, test_plugins, test_plugins_system, test_proxy_plugin
- **tests/push/**(37): feishu_discovery, feishu_targeting + messaging_{a2a,bluebubbles,buzz,dingtalk,discord,email,google_chat,homeassistant,irc,line,matrix,mattermost,msgraph_webhook,ntfy,photon,pipeline,qqbot,raft,signal,simplex,slack,sms,teams,telegram,wecom,weixin_bridge,whatsapp_cloud,yuanbao}(28) + push, push_channels, push_delivery, push_directory, push_images, push_schema_targets, push_targets(7)
- **tests/store/**(3): test_read_state, test_storage_hardening, test_store_dedup
- **tests/vision/**(3): test_vision, test_vision_collect, test_vision_models_server
- **根留(6,跨切面)**: test_docs, test_schema, test_secrets, test_skill_doc, test_smoke, test_trellis_finish_guard
- **迁出(1+fixture)**: test_classify + fixtures/classify_gold.json → `myssia-classifier/tests/`
- 合计:87 分组 + 6 根留 + 1 迁出 = 94 ✓(迁移脚本 Counter 查重 + 双向差集断言)

## 执行步骤(实录)

1. 显式映射脚本(`/tmp/migrate_tests.py`,已清理)+ 全覆盖断言 → `git mv` 87 文件入组 + 2 项迁出
2. 路径修正(28 文件):`parents[1]`→`parents[2]`(仓库根)、`.resolve().parent / "fixtures"`→`parents[1] / "fixtures"`(共享 fixtures)、desktop 的 `parent.parent`→`parents[2]`、漏网 `cli/test_sources_write_surgery` 补修
3. `test_classify.py` import 改写 5 处:顶层 import/局部 import×2/logger 名×2/docstring
4. 根 `pyproject.toml` testpaths 双目录;活引用同步 5 处(push/__init__·desktop/entry·PR 模板·spec×2)
5. 门禁:定向冒烟 218 绿 → 全量 3585 passed 19 skipped → ruff 绿 → detect-changes 净

## 回滚

- 代码层零行为变化,revert `8d2e8a8`(纯重命名)+ `b864d2b`(内容增量)即整体还原;无数据迁移、无配置兼容问题
- 注意:revert 后 pyproject testpaths 与文档引用需随同回退(均在上述两笔内)

## 事故与教训

- **共享暂存区竞态**:git mv 暂存的 89 重命名被并行提交 8d2e8a8 收编(裁决 G1:不拆)。教训:长事务批量 git mv 期间,暂存区对并行会话是裸露的;下次大迁移应在 mv 后立即 commit 空档最短化,或迁前与并行线打招呼锁定提交窗口
- **证据链教训**:AC3 初版用「全量数 ≥ 基线」论证零丢失,被 grill 推翻(并行线持续加测试,数量涨不反证无丢失),补 collect-only 归一 diff 才闭环
