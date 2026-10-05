# 表格还原:自管环境首件可选组件(rapid_table)

## Goal(主人定向,2026-10-05 两轮讨论定案)

截图里的表格(行情/比价/参数对比/榜单)还原成结构化 Markdown 进条目 metadata,推送卡片可直接嵌表。作为 desktop-managed-py-env(D6)立好后的第一件可选重件,验证「组件装进自管环境、零重打包」路线。

## 决议

- **R1 引擎**:rapid_table(RapidAI 家族 onnx 版,模型随轮内置几十 MB,复用自管环境 python/onnxruntime;**不引 Paddle 全家**)。
- **R2 品类开关**:品类 YAML `images:` 节 sidecar 加 `table: true`(默认关;与既有 images sidecar 字段同模式,$. 前缀错误路径)。
- **R3 CLI 通道**:extras `myssia[table]`(缺装结构化报错带安装命令,管线红线同 vision)。
- **R4 桌面通道**:设置页「表格还原」组件开关 → pyenv 组件机制往自管环境 pip 装(镜像索引继承既有覆盖;组件注册表条目形态:id=table, pip spec 钉版)。
- **R5 分工边界**:表格结构化 = rapid_table;整图语义描述 = 既有 VL 环;互不替代。
- **R6 产出契约**:`metadata.tables = [{markdown: "管道表", rows, cols}]`;失败只写 `metadata.table_status`(`table_provider_error` 等),绝不阻管线(与 images 环同款红线)。

## Acceptance Criteria

- [x] AC1 引擎惰性 import + 缺装结构化报错(`table_provider_error` 类,文案带 `pip install "myssia[table]"`);装后真图(含管道表夹具)还原逐格正确
  - 回标 2026-10-05(QC「表格还原·Python 引擎与管线」pass,门禁 uv 绿):惰性 import 实证——table.py 模块级仅核心依赖(selectolax),rapid_table/rapidocr 全部 importlib 函数内惰性(`_get_table_engine` table.py:122);dev 环境真缺 rapid_table,亲跑得 code=dependency_missing、message 与 details.install 均含 `pip install "myssia[table]"`(table.py:53/131,当前树实读);装后真图逐格正确:/tmp 隔离 venv(rapid-table==3.0.2 + rapidocr-onnxruntime + selectolax<1.0 对齐锁面)真跑仓内管道表夹具 tests/vision/fixtures/table_sample.png,输出与期望逐字节 EXACT MATCH:True,rows/cols=(4,3);仓内 TestRealEngineFixture 按设计 SKIP 留 AC6 沙箱(dev 缺装,探针环境已清理)。
- [x] AC2 `table: true` 品类端到端:图片环产出 metadata.tables;`table` 缺省/false 时零行为变化(既有 golden 全绿)
  - 回标 2026-10-05(同上 QC):collect.py:1021 `if effective.table:` 守卫 + `asyncio.gather(..., return_exceptions=True)`,成功表落 metadata.tables(契约恰三键 {markdown, rows, cols},table.py:92-94 to_dict 当前树实读),失败只写 `table_status="table_provider_error"`(collect.py:1040)、OCR/VL 无条件继续;table 过 _merge_overrides 存活(collect.py:818 model_dump)、覆写键表无 images_table(不开放源级覆写);定向跑 `uv run --no-sync pytest tests/vision/ -q` = 165 passed/1 skipped(1 skip 即 AC1 注的真引擎例)、`uv run --no-sync pytest tests/test_schema.py -q` = 76 passed(12 节契约面 golden 全绿);缺省/false 零行为变化各有 golden 测试随套件绿。
- [ ] AC3 CLI:extras 装通;doctor 对 table 组件的缺装披露
  - 未勾(2026-10-05):extras 行已落 pyproject.toml:57 `table = ["rapid-table>=3.0.2,<4", "rapidocr-onnxruntime>=1.3", "tqdm>=4"]`(当前树实读,tqdm 为 3.0.2 轮隐性 import 的真实修复);doctor 缺装披露未做、docs zh/en + skill/SKILL.md 四处同步未做(执行清单③剩余);uv.lock 未动(--no-sync 铁律),门禁侧 uv sync 时按新 extras 解锁属门禁域。
- [ ] AC4 桌面:设置页开关 → 自管环境装组件 → 状态回读;卸载/缺装如实呈现;镜像覆盖生效
  - 未勾(2026-10-05):实现面+门禁全绿——QC「表格还原·桌面组件开关」门禁 npm 绿:cargo test 53、`./.venv/bin/python -m pytest tests/desktop/test_pyenv_resources.py` 23、vitest(pyenv-components + pyenv-card)23、tsc -b 退出 0;跨域高危「注册表钉 rapid-table==1.0.3 vs 引擎仅支持 3.x」已闭合:components.json pip_spec(当前树实读 desktop/resources/components.json:5)= `rapid-table==3.0.2 rapidocr-onnxruntime>=1.3 tqdm>=4`,与 extras 同源闭包且 ==3.0.2 落在 `>=3.0.2,<4` 内;3.0.2 API 正面匹配(裸 `RapidTable()` 构造/`ocr_results` 复数参数/`pred_htmls` 输出,对 GitHub v3.0.2 源码实核);run_pip_spec 多 spec 逐条位置参数语义(pyenv_install.rs:642-647)+ 空白串防御各有新测;钉版常量三侧同步(tests/desktop/test_pyenv_resources.py:135 / desktop/src-tauri/src/pyenv_components.rs:69 / pyenv-card.tsx:210,均当前树实读)。但「开关→真装 3.0.2→状态回读」真机全链路(含 modelscope 首用下载 6.8MB)未实跑,归沙箱验收(同 AC6)。残留:中危主链反向护栏(pyenv_install.rs:1068 start_install_thread 不查 ComponentManager.installing,组件与主链 pip 可并发写同一自管环境)、low tauri.conf.json staged 版缺 components.json 随包映射(按 staged 内容分批提交会丢映射→组件面静默消失,提交时需一并入册)。
- [ ] AC5 docs zh/en(schema.md images 节 + getting-started 组件说明)+ skill/SKILL.md 词表同步(四处同步纪律)
  - 未勾(2026-10-05):四处同步未做(执行清单③剩余,非本步域)。
- [ ] AC6 门禁:pytest/vitest/tsc/cargo 全绿;沙箱端到端(装组件→跑品类→表进 metadata)
  - 未勾(2026-10-05):定向门禁绿——uv 侧 tests/vision 165 passed/1 skipped + test_schema 76 passed;npm 侧 cargo test 53 + tests/desktop 23 + vitest 23 + tsc -b 退出 0(数字较修复前各 +1,系多 spec/空白串新测)。但全量 pytest 未跑(遵嘱只跑定向面),沙箱端到端(装组件→跑品类→表进 metadata,含 TestRealEngineFixture 真引擎例)未实跑,归脚本统一门禁/沙箱验收。

## 非目标

- 手写体/公式/版面全档结构化(Paddle 域);不改 12 节公开契约(table 是 sidecar);不动核心依赖红线。

## 执行清单

1. [x] Python 侧:vision/table.py 引擎 + schema sidecar + collect 环分支 + 测试(tests/vision)
   - 回标 2026-10-05(QC「表格还原·Python 引擎与管线」pass,门禁 uv 绿):引擎封装(table.py,惰性 import + dependency_missing 结构化报错带安装命令)、schema sidecar(ImagesConfig.table 默认 False,$.images.table 错误路径)、collect 环分支(collect.py:1021-1040,失败不阻管线只写 table_status)、测试全落地(tests/vision 165 passed/1 skipped);R6 契约三键恰 {markdown, rows, cols};不自动装(D2 语义,table.py/collect.py 零 subprocess/pip 调用);关键实况经 PyPI 轮直接解包双轮独立复核(3.0.2 契约/tqdm 隐性 import/3.x 不内置模型首用 modelscope 下载 6.8MB/R1 不引 Paddle),extras 已按实轮契约写好(pyproject.toml:57)。
2. [x] 桌面侧:pyenv 组件注册表 + IPC + 设置屏开关 + vitest/cargo 测试
   - 回标 2026-10-05(QC「表格还原·桌面组件开关」高危闭合,门禁 npm 绿):注册表 components.json(table 条目 pip_spec 钉 `rapid-table==3.0.2 rapidocr-onnxruntime>=1.3 tqdm>=4`,与 extras 同源闭包)+ run_pip_spec 多 spec 语义与空白串防御(pyenv_install.rs:642-647)+ 设置屏开关文案(pyenv-card.tsx:210,modelscope 首用下载/镜像生效均已写明)+ 测试落地并复跑全绿:cargo test 53、tests/desktop/test_pyenv_resources.py 23、vitest 23、tsc -b 退出 0;钉版常量三侧同步无「模型随轮」旧说法残留。残留(不阻勾,已记 AC4 注):中危主链反向护栏、tauri.conf.json staged 映射提交时需并入;真装全链路归沙箱。
3. [ ] CLI extras + doctor 披露 + docs/skill 四处同步
   - 未勾(2026-10-05):extras 行已落(pyproject.toml:57);CLI doctor 对 table 组件缺装披露、docs zh/en 与 skill/SKILL.md 四处同步未做(实现员披露的剩余项,非 Python/桌面两步域)。
