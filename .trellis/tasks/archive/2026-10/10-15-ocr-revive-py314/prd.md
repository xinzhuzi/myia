# OCR 供件换代 revive(rapidocr-onnxruntime→rapidocr 3.x,py314 复活)

## Goal

py314 升级连坐:旧 rapidocr-onnxruntime 1.4.x 冻结且声明 <3.13、3.14 无轮,OCR/表格还原链换血 rapidocr 3.x 新主包+onnxruntime>=1.31 显式同列(cp314 轮在位);extras/组件闭包/引擎适配/测试/文档五面同步;装机换装(swap 不重打包)

## Requirements

- (补档注:任务期 PRD 未曾存在,不事后捏造;实际要求面以提交 ee020958 文件面与下方终局回执为准)

## Acceptance Criteria

- [ ] (补档注:同上,不事后捏造 AC 清单)

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.

## 终局回执(簿记归档员落笔,2026-10-15;材料=编排回执逐字+提交证据重建)

### 补档溯源(先读)

本档为**归档时补建**:该线执行/评审/装机完成时任务档从未建过——`.trellis/tasks/` 活跃区与 `archive/` 均无此目录,`git log --all -- ".trellis/tasks/10-15-ocr-revive-py314*"` 零命中,journal 亦无轨迹;存证仅两处:①代码内标签注释(`pyproject.toml:41`/`pyproject.toml:47`/`tests/desktop/test_pyenv_resources.py:140` 的 `10-15-ocr-revive-py314` 字样,随 ee020958 落库);②编排递给簿记员的回执材料(执行 true/门禁 绿/评审 过/装机见下)。脚手架由 `task.py create --slug ocr-revive-py314 --no-start` 补生成,Requirements/AC 两节留注不补写(未发生过任务期 PRD,不事后捏造),task.json 由簿记员直改(仓库既有惯例)。

### 选型(ee020958 证据重建)

- **死因**:rapidocr-onnxruntime 1.4.x 上游冻结且声明 `Python<3.13`,cp314 无轮——py3.14 升级(10-14-leftover-sweep-install T3/D3-v2)连坐炸点(`src/myssia/vision/ocr.py:13-15` 模块头注:「旧 rapidocr-onnxruntime 1.4.x 冻结且声明 <3.13,3.14 无轮故换血」)。
- **新选**:rapidocr **3.x 新主包**(Apache-2.0;内置 PP-OCRv6 small det/rec/cls 三模型零下载);主包不带推理后端 → **onnxruntime `>=1.31,<2` 显式同列**(cp314 轮在位);体积影响 ~48MB 下载(rapidocr 27.3MB + onnxruntime 20.9MB)——`pyproject.toml:41-46`。
- **opencv 双株共存裁定**:opencv-python(rapid-table 3.0.2 requires_dist 硬含)+ opencv-python-headless(rapidocr 3.10 新增)同版(5.0.0.93)文件集相同=良性;异版分叉即停交付——`pyproject.toml:47-49`。

### 替换面(提交 ee020958,18 件 263+/131-,其中本线 15 件)

- `pyproject.toml`:vision/table 两组 extras 双改(`rapidocr-onnxruntime>=1.3` → `rapidocr>=3,<4`+`onnxruntime>=1.31,<2`);rapid-table 自身 requires_dist 硬含 `onnxruntime>1.17.0` 与显式 `>=1.31,<2` 合流落 1.31.x 无冲突。
- `src/myssia/vision/ocr.py`:`_run_rapidocr` 适配套新 API——单返回 `RapidOCROutput`(旧为 `(result, elapse)` 元组)、txts/scores 逐行平行数组(旧为 `[box,text,score]` 行组)、无文字图 `output.txts is None`/`output is None` 双条件合法空结果。
- `src/myssia/vision/{table,collect,__init__}.py`+`src/myssia/cli.py`:同步换供件名与喂入形态。
- `desktop/resources/components.json`+`desktop/src-tauri/src/pyenv_components.rs`:table 组件闭包三件→四件(`rapid-table==3.0.2 rapidocr>=3,<4 onnxruntime>=1.31,<2 tqdm>=4`),`tests/desktop/test_pyenv_resources.py` 交叉对齐把守两侧不漂移。
- 测试四面:`tests/vision/test_vision.py`、`tests/vision/test_vision_table.py`、`tests/cli/test_cli_full.py`、`tests/desktop/test_pyenv_resources.py`。
- `docs/{zh,en}/getting-started.md`+`uv.lock`(94 行再生)。

### 门禁 / 深度评审(编排回执逐字;簿记员未重跑)

- **门禁**:绿。
- **深度评审**:过。

### 装机(编排回执逐字 + 簿记员旁证亲验)

- 回执:`{"rebuilt":false,"swapped":true}`——不重打包、装机包资源直换。
- 旁证(簿记员 2026-10-15 亲验):装机包 `desktop/src-tauri/target/release/bundle/macos/世事.app/Contents/Resources/` 下 `myssia-src/myssia/vision/ocr.py:1` 已是「rapidocr 新主包」版;`components.json` table `pip_spec` 已是新四件闭包;`myssia/vision/__pycache__/` pyc 戳 Oct 15 04:48-04:49(提交 ee020958 时戳 04:19 之后的换装窗),`table.cpython-314.pyc` 在位;ocr 仅见 `cpython-312.pyc` 一株,如实记不代判。

### 簿记事实

- **代码提交 = ee020958**(已在 origin/main, ancestor of e75732ec)。**裹挟注记**:该提交消息面为 sendmsg research(r6/r7 ctx 定案),但文件面 18 件中 15 件属本线 OCR 换代(另 3 件为 sendmsg r4 research 存档)——并行 sendmsg 线的提交把本线工作裹挟落库,消息未提 OCR 一字;已推送历史不重写(仓库惯例),本档即该笔工作的对账锚点。
- 归档移动:`task.py archive --no-commit`(branch 元数据缺失时加 `--skip-branch-validation`,任务从未 PR-backed);外科提交 = 本档 archive 移动 + CHANGELOG [Unreleased] 补 OCR 供件换代一笔(同批)。
- 并行在途件未碰:工作树 M/?? 六件全在排除清单(notify-app-icon prd / wechat-bridge cli·senddirect·senddirect_probe·test_send_direct / desktop/ui-src/e2e/package_smoke.py / feed-l3·native-system-dialog 两 review-note)。
