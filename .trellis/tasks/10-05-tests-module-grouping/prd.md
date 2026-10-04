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

- [x] AC1 `tests/` 根零模块专属 test_*.py;子目录测试与被测模块一一对应;映射脚本断言 94 文件全覆盖无遗漏无重复
  — evidence: 迁移脚本(全显式映射+Counter 查重+双向差集断言)通过:94 = 87 分组 + 6 根留 + 1 迁出;根残留仅 test_docs/schema/secrets/skill_doc/smoke/trellis_finish_guard。
- [x] AC2 `myssia-classifier/tests/test_classify.py` + `tests/fixtures/classify_gold.json` 存在,且其 import 全部指向 `myssia_classifier`(零 `myssia.` 依赖)
  — evidence: 文件+fixture 均在新位;`grep "myssia\." myssia-classifier/tests/test_classify.py` 零命中(顶层 import/局部 import×2/caplog logger 名×2/首行 docstring 全改直引)。
- [x] AC3 全量绿:`uv run --no-sync python -m pytest -q` 收集 ≥3290(基线 3297)零失败;`uvx ruff@0.16.10 check .` 零错
  — evidence: `3585 passed, 19 skipped in 93.15s`(高于基线,并行线新增测试全数收进);ruff `All checks passed!`。
- [x] AC4 `ci.yml` 零编辑,靠根 testpaths 生效
  — evidence: b864d2b 触碰清单不含 `.github/workflows/`(仅 PR 模板示例行路径改新形态);根 pyproject testpaths=["tests","myssia-classifier/tests"]。
- [x] AC5 活文件中 `tests/test_` 引用与实际路径零漂移(test_docs/test_skill_doc 自身一致性测试也须过)
  — evidence: 同步 5 处(push/__init__.py:150、desktop/entry.py:1183、PR 模板:14、spec python/index.md:52、spec desktop/sidecar-protocol.md:289);tests/fixtures 未动故 templates.py/yaml-schema.md 引用天然成立;test_docs/test_skill_doc 随全量 3585 绿。
- [x] AC6 单文件定向跑也绿(抽验 `pytest tests/engines/test_registry.py` 与 `pytest myssia-classifier/tests/`),证明 conftest 链与跨文件 import 在子目录下成立
  — evidence: `pytest tests/engines/test_registry.py myssia-classifier/tests/test_classify.py tests/desktop -q` → `218 passed in 7.17s`(conftest 助手链/独立 import/desktop 跨文件 import 三风险点全覆盖)。
- [x] AC7 提交只含本任务文件,不混并行会话在途件;gitnexus detect-changes 核验过
  — evidence: b864d2b 34 文件全任务域(逐 hunk 核过共享热文件);`gitnexus detect-changes -r shishi --scope staged` → No changes detected。**事故注记**:89 个 git mv 纯重命名(零内容变更)被并行提交 8d2e8a8 经共享暂存区意外收编,内容增量全部由 b864d2b 承载;两笔均未推送,是否拆分 8d2e8a8 历史归位留主人裁决。

## 验证记录(2026-10-05)

- 定向冒烟:`uv run --no-sync python -m pytest tests/engines/test_registry.py myssia-classifier/tests/test_classify.py tests/desktop -q --tb=short` → 218 passed in 7.17s
- 全量:`uv run --no-sync python -m pytest -q --tb=short` → 3585 passed, 19 skipped in 93.15s(0:01:33)
- Lint:`uvx ruff@0.16.10 check .` → All checks passed!
- GitNexus:`gitnexus detect-changes -r shishi --scope staged` → No changes detected(测试移动不触符号图)
- 提交:纯重命名部分随 8d2e8a8(事故收编,零内容变更);内容增量+任务档 = b864d2b;本回标 = 追加一笔

## 非目标

- 不改产品代码逻辑(仅注释中的测试路径引用);不动 desktop/ui-src 前端测试;不给子目录加 `__init__.py`(文件名全局唯一,rootdir prepend 模式无冲突,已验证 conftest `from conftest import` 链依赖 tests/ 入 sys.path,由 pytest 装载根 conftest 保证)
