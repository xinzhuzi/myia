# tests 按模块分组+分类器测试迁包

## Goal

主人指令(2026-10-05):「按照你的逻辑去做,并且每个模块不应该混杂在一起」。主包 `tests/` 94 文件全平铺,与 `src/myssia` 子包结构脱节;独立发布的 `myssia-classifier` 无自己的测试目录。重组为镜像源码结构的模块子目录,并让分类器测试随包走。

## Requirements

1. **主包 tests/ 分组**(git mv,不改测试逻辑):
   - `alerts/ cli/ classify/ cron/ credhunter/ desktop/ engines/ enrich/ feedback/ pipeline/ plugins/ push/ store/ vision/` 子目录,归属按「被测对象」判定:
     - alerts=规则引擎;cli=CLI 命令族(含 skill_install/sources_write_surgery);classify=shim 与独立包契约(test_classifier_package);cron=定时;credhunter=凭据猎手插件;desktop=sidecar 协议+yaml 编辑协议(二者互 import 必须同目录);engines=引擎矩阵(fetch_base/direct_api/crawl4ai/scrapling/firecrawl/llm_browser/static_html/stealth/registry/proxy_*);enrich=enrich+aggregate;feedback;pipeline=pipeline+baseline(横切特性测试);plugins=插件系统;push=push+全部 messaging_*+feishu_*;store=read_state/storage_hardening/store_dedup;vision
   - `tests/` 根仅留跨切面:conftest.py、fixtures/(共享)、regen_push_targets_golden.py、test_docs/test_schema/test_secrets/test_skill_doc/test_smoke/test_trellis_finish_guard
2. **分类器测试迁包**:`test_classify.py`+`fixtures/classify_gold.json` → `myssia-classifier/tests/`(fixture 随行,`Path(__file__).parent/"fixtures"` 天然成立);import 从 `myssia.classify`(shim)改写为 `myssia_classifier` 直引——独立包的测试不得依赖主包
3. **门禁入口**:根 `pyproject.toml` `testpaths = ["tests", "myssia-classifier/tests"]`;`ci.yml` 零改动
4. **路径逻辑修正**:迁移文件中 `parents[1]`(仓库根)→ `parents[2]`;`parent / "fixtures"` → `parents[1] / "fixtures"`;根留文件不动
5. **活文档路径同步**:源码注释/文档中引用被移动测试的路径改新址(如 `src/myssia/push/__init__.py` 的 `tests/test_messaging_<平台>.py`);`.trellis/tasks/archive/` 历史档与 CHANGELOG 不改写

## Acceptance Criteria

- [ ] AC1 `tests/` 根零模块专属 test_*.py;子目录测试与被测模块一一对应;映射脚本断言 94 文件全覆盖无遗漏无重复
- [ ] AC2 `myssia-classifier/tests/test_classify.py` + `tests/fixtures/classify_gold.json` 存在,且其 import 全部指向 `myssia_classifier`(零 `myssia.` 依赖)
- [ ] AC3 全量绿:`uv run --no-sync python -m pytest -q` 收集 ≥3290(基线 3297)零失败;`uvx ruff@0.16.10 check .` 零错
- [ ] AC4 `ci.yml` 零编辑,靠根 testpaths 生效
- [ ] AC5 活文件中 `tests/test_` 引用与实际路径零漂移(test_docs/test_skill_doc 自身一致性测试过)
- [ ] AC6 单文件定向跑也绿(抽验 `pytest tests/engines/test_registry.py` 与 `pytest myssia-classifier/tests/`),证明 conftest 链与跨文件 import 在子目录下成立
- [ ] AC7 提交只含本任务文件,不混并行会话在途件;gitnexus detect-changes 核验过

## 非目标

- 不改产品代码逻辑(仅注释中的测试路径引用);不动 desktop/ui-src 前端测试;不给子目录加 `__init__.py`(文件名全局唯一,rootdir prepend 模式无冲突,已验证 conftest `from conftest import` 链依赖 tests/ 入 sys.path,由 pytest 装载根 conftest 保证)
