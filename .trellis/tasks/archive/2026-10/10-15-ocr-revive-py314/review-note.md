# review-note(代审留档)

## proxy-review-py314-anchor 代审结论:过(对账锚点核对口径——四锚当代实证全部在位且与档述一致)

- 代审员:proxy-review-py314-anchor;时间:2026-10-15 06:59–07:03 +0800;审查基点:HEAD=0ade6d59。
- 代审面(「改钉」形态):本档为归档时补建的对账锚点档(prd:23「本档即该笔工作的对账锚点」见 prd:52),代审只核**代码锚在位与档述一致**,不补写任何 Requirements/AC 文本(prd:9/:13 留注维持原样,本步未动 prd 任何字节)。
- 模板:feed-l3 版头。注:ask 给的模板路径 `.trellis/tasks/10-14-feed-l3-beautify/review-note.md` 已漂移(该任务已归档),实际模板在 `.trellis/tasks/archive/2026-10/10-14-feed-l3-beautify/review-note.md:1`(fd -H 实测定位)。

## 三次探活(动手前/落笔前/提交前;纪律=静默 ≥30min 才可动手)

| 轮 | 时点 | 档内 newest mtime | 静默 | ps 作业进程 |
|---|---|---|---|---|
| 1(动手前) | 06:59:35 | 05:10:23(task.json,ls -laT 实测) | ~1h49m>30min ✓ | 零(`ps aux \| grep -iE 'lldb\|senddirect\|wechat-bridge\|rapidocr\|onnxruntime\|ocr\|py314'` 命中全为 GUI 噪声:ZCode/VSCode/LM Studio flag 串含 "ocr"、微信本体自带 wxocr helper(pid 21387,WeChat 内部件非作业进程)) |
| 2(落笔前) | 07:01:44 | 05:10:23(stat -f 实测,未变) | ~1h51m ✓ | 零(`grep -iE 'lldb\|senddirect\|rapidocr\|onnxruntime'` wc -l = 0) |
| 3(提交前) | 07:02:25 | 05:10:23(task.json,未变;档内唯一新 mtime=本文件 07:02:18) | ~1h52m ✓ | 零(grep 同轮 wc -l = 0) |

档目录 git 唯一触碰 = `7cb79c3e`(2026-10-15 05:11:18 归档提交,git log -5 实测仅此一笔);并行线活跃(sendmsg 档 06:57:30 被 fdc1e278 归档、ui-cloud5 M 件在树)但均不在本步写面——本步唯一写入=本文件(档内新建)。

## 代码锚核验(全部本步实读;命令与输出原文引行号)

### 锚一 pyproject.toml 依赖段(ask 指名 :41-47;Read 工具整文件实读)

```
pyproject.toml:41  # 看图(10-03-image-input;OCR 供件换代 10-15-ocr-revive-py314):双引擎
pyproject.toml:42  # OCR = ocrmac(macOS Vision,MIT)+ rapidocr(Apache-2.0 新主包,内置
pyproject.toml:43  # PP-OCRv6 small det/rec/cls 三模型零下载);显式含 llm 的 openai
pyproject.toml:44  # (VisionClient 复用 AsyncOpenAI 模式)。rapidocr 主包不带推理后端,
pyproject.toml:45  # onnxruntime 显式同列(>=1.31,<2:cp314 轮在位);体积影响 ~48MB 下载
pyproject.toml:46  # (rapidocr 27.3MB + onnxruntime 20.9MB),见任务档 design 依赖节。
pyproject.toml:47  # opencv 双株共存注记(10-15-ocr-revive-py314):opencv-python 经
```

- :41 与 :47 双标签 `10-15-ocr-revive-py314` 在位 ✓(prd:23 档述「pyproject.toml:41/pyproject.toml:47 的字样」);:41-46 vision 注记段与 prd:28「pyproject.toml:41-46」吻合 ✓;:47-49 opencv 双株注记与 prd:29「pyproject.toml:47-49」吻合 ✓。
- extras 落点(实读):`pyproject.toml:55` vision=`…,"rapidocr>=3,<4", "onnxruntime>=1.31,<2",…`;`pyproject.toml:64` table=`…,"rapidocr>=3,<4", "onnxruntime>=1.31,<2", "tqdm>=4"` ✓(prd:33 档述双组 extras 双改形态)。

### 锚二 OCR 模块头注(`src/myssia/vision/ocr.py`,Read 实读 :1-24 docstring)

```
ocr.py:1   """双引擎 OCR 统一接口:macOS Vision(ocrmac)+ RapidOCR(rapidocr 新主包)。
…
ocr.py:13    Vision 不可直接互比,UI 注记来源引擎,阈值统一)。供件换代见
ocr.py:14    10-15-ocr-revive-py314(旧 rapidocr-onnxruntime 1.4.x 冻结且声明
ocr.py:15    <3.13,3.14 无轮故换血)。
```

:13-15 与 prd:27 档述引文(「`src/myssia/vision/ocr.py:13-15` 模块头注:『旧 rapidocr-onnxruntime 1.4.x 冻结且声明 <3.13,3.14 无轮故换血』」)逐字一致 ✓;:1「rapidocr 新主包」与 prd:48 装机旁证口径同形 ✓。

### 锚三 档述第三处代码标签(`tests/desktop/test_pyenv_resources.py`;sed -n '135,145p' 实读)

`:140` = `#: (交叉对齐测试把守;供件换代 10-15-ocr-revive-py314)。`;`:141` = `TABLE_COMPONENT_PIP_SPEC = "rapid-table==3.0.2 rapidocr>=3,<4 onnxruntime>=1.31,<2 tqdm>=4"` —— 与 prd:23 档述(test_pyenv_resources.py:140 标签)、prd:36(table 四件闭包)吻合 ✓。

### 锚四 裹挟提交 ee020958(补档性质注记的实据;git show 实测)

`git show --stat --format='%H%n%an %ad%n%s%n%b' ee020958 | head -40`:

- 全哈希 `ee02095825060b6fca9a9448c859c3e6b737dc82`;作者 cnb;2026-10-15 04:19:29 +0800。
- 消息面:`research(sendmsg): r6/r7 ctx 来源定案——无全局槽(堆链所有,双法活扫零命中);务实路线=ctx 会话内缓存(observe_bp 形态,首条 2 发后续 1 发);spawner/外层七件 DAT 清单入档` —— **零提 OCR 一字**,与 prd:52「消息未提 OCR 一字」吻合 ✓。
- 文件面:18 件 263+/131-;逐件清点=15 件 OCR 换代(desktop/resources/components.json、desktop/src-tauri/src/pyenv_components.rs、docs/{en,zh}/getting-started.md、pyproject.toml、src/myssia/cli.py、src/myssia/vision/{__init__,collect,ocr,table}.py、tests/{cli/test_cli_full,desktop/test_pyenv_resources,vision/test_vision,vision/test_vision_table}.py、uv.lock)+3 件 sendmsg r4 research 存档(research/r4/{FINDINGS-r4.md,global_scan.txt,scan_globals.py})——与 prd:31/:52「18 件 263+/131-,其中本线 15 件」逐项吻合 ✓;uv.lock 变更行数=94,与 prd:38「uv.lock(94 行再生)」吻合 ✓。
- 祖先关系:`git merge-base --is-ancestor` 实测——ee020958 是 HEAD 祖先 YES、是 e75732ec 祖先 YES,与 prd:52「已在 origin/main, ancestor of e75732ec」吻合 ✓。

### 旁证(归档提交 7cb79c3e,git show --stat 实测)

文件面=档内 4 件(check.jsonl 0B/implement.jsonl 0B/prd.md +54/task.json +26)+`CHANGELOG.md` +9——与 prd:53「archive 移动 + CHANGELOG [Unreleased] 补 OCR 供件换代一笔(同批)」吻合 ✓。

## 补档性质注记(如实)

- 本档为归档时补建:任务期 PRD 从未存在,Requirements/AC 两节留注不补写(prd:9/:13)——本代审同律,**未改动 prd 任何字节**(自检:本步提交 `git show --stat HEAD` 仅含本文件;`git diff HEAD~1 -- <prd>` 为空)。
- 该笔工作经裹挟提交 ee020958 落库:消息面为 sendmsg research(r6/r7 ctx 定案),文件面 18 件中 15 件属本线 OCR 供件换代;已推送历史不重写(仓库惯例),本档即该笔工作的对账锚点(prd:52 原文)。本次代审=钉住这枚锚:四项代码锚全部当代实证在位且与档述一致。
- **未当代复验项(如实)**:①门禁/深度评审=编排回执逐字「绿/过」(prd:40-43 明载簿记员未重跑),代审员亦未重跑——代审面为锚点核对,非门禁重演;②装机旁证(bundle 侧 ocr.py 新主包版、pyc 戳 04:48-04:49)为簿记员亲验记录(prd:45-48),本代审未触装机面(红线:装机只装已提交态;装机侧另有并行线作业窗口);③prd:54 所列并行在途件现态未复核(非本步锚面)。

## 哨兵

- 步初 porcelain(v1)=7 条(6 M:frontend-ui.md/feed api.ts/feed-screen.test.tsx/feed-screen.tsx/telegram-card.tsx/macos_notify.py + 1 ??:.trellis/tasks/10-15-ui-cloud5/),全部并行线件,本步未碰;步末复测见下。
- 本 review-note 为本步唯一写入(新增 ?? 一条);状态指针(task.json)未动。
- 提交=scoped:`git add` + `git commit --` 双显式路径(仅本文件);文档类提交,detect-changes 按仓库豁免(AGENTS.md MYIA 实况段:文档/配置类提交可豁免)。

## 结论

**过(锚点核对口径)**:pyproject.toml 依赖段(:41/:47 双标签+注记段+extras 落点)、ocr.py 模块头注(:13-15 逐字)、test_pyenv_resources.py:140 标签+四件闭包、ee020958 裹挟事实(消息面/文件面 15+3/祖先关系/uv.lock 94 行)四锚当代实证全部与档述一致;归档提交 7cb79c3e 文件面亦吻合。prd Requirements/AC 留注原样未动。门禁/装机面不在本次代审重演面,如上如实记。
