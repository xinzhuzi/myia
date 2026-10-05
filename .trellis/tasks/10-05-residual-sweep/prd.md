# 残扫收尾:文档 trafilatura 源级覆写口径补齐 + CI runner ubuntu 钉版(10-05-residual-sweep)

## Goal

两件既定建议的执行收尾,零代码符号改动:

1. **文档差口**:d11a7ef 定案的源级覆写(`engine_options.static_html.extract_fallback`,
   优先级 = 源级 > 全局 env > 缺省关)已同步 docs/zh|en/schema.md + SKILL.md,但
   README zh/en 段与 docs/zh|en/getting-started 四处口径仍只写全局 env
   `MYIA_EXTRACT_FALLBACK` 双态(装+开)——补源级覆写两行口径,中英成对,引
   schema.md 详表;守 tests/test_docs.py 双语结构对齐(页集/标题骨架/fence 剖面/
   YAML 示例结构,补写走纯散文行,零 fence 增删)。
2. **runner 钉版**:GitHub 公告 ubuntu-latest 标签 2026-10-19 起渐进迁 Ubuntu 26.04
   (窗口至 11-19,同标签新旧混跑;公告 2026-09-17 changelog),为免到期行为漂移,
   把 .github/workflows/ci.yml(5 处)+ desktop-release.yml(1 处,行内注释保留)的
   ubuntu-latest 显式钉 ubuntu-24.04——当前 latest 即 24.04,零行为变化;macos 侧
   仅 desktop-release.yml:54 且已显式 macos-14(销号,零改动)。

## 探查结论(动工前侦察已核实)

- 缺口坐实:`grep extract_fallback README.md docs/zh/getting-started.md
  docs/en/getting-started.md` 零命中;范本 = docs/zh/schema.md:91 与
  docs/en/schema.md:103 三态口径。
- runner 全清单:ubuntu-latest 全仓 10 处——ci.yml:11,29,55,80,94;
  desktop-release.yml:274;docker-publish.yml:22;pypi-publish.yml:79,254,345。
  本任务点名口径 = ci.yml+desktop-release.yml 两件;docker-publish/pypi-publish
  4 处不在点名清单,如实留报不扩面。
- README doctest 面不存在:pyproject.toml/pytest.ini/setup.cfg/tox.ini/Makefile
  零 doctest 配置(该门禁件销号)。

## Requirements

### R1 文档补写(README.md + docs/zh/getting-started.md + docs/en/getting-started.md)

- 四处落点(README zh/en 段 + getting-started zh/en 开关节)各补两行内散文:
  源级 `engine_options.static_html.extract_fallback: true/false` 可覆写全局,
  源级 > 全局 `MYIA_EXTRACT_FALLBACK` > 缺省关(源级未设时与全局口径逐字节
  一致),详表引 schema.md;中英成对。
- 零 fence 增删、零标题改动(getting-started 相对链接 `schema.md` 落同目录,
  test_docs 相对链接门可解析)。

### R2 runner 钉版(.github/workflows/ci.yml + desktop-release.yml)

- ubuntu-latest → ubuntu-24.04 共 6 处(ci 5 + desktop-release 1);
  desktop-release.yml:274 行内注释「jq 预装(grill R2-D6a)」保留;macos-14
  不动;docker-publish/pypi-publish 不碰。

### R3 门禁(亲跑,数字回执)

- `uv run --no-sync pytest tests/test_docs.py -q`(双语结构对齐+yaml 块真加载)。
- 两 workflow `python3 -c yaml.safe_load` 解析自检。
- README doctest 面:不存在,销号(证据见上)。

## Acceptance Criteria

- [x] **AC1(口径补齐)**:四处落点各含源级覆写口径,与 schema.md 三态口径一致;
  中英成对;test_docs.py 全绿。
- [x] **AC2(runner 钉版)**:ci.yml+desktop-release.yml 的 ubuntu-latest 清零、
  显式 ubuntu-24.04 落位;macos-14 原样;两 yaml 可解析。
- [x] **AC3(门禁)**:R3 命令亲跑全过,数字回执本档;commit 全部 `--only`
  明确路径。

## AC 证据回填(2026-10-05,本流亲跑)

- **AC1**:grep extract_fallback 四文件全命中——README.md:174(zh 段)/553(en
  段)、docs/zh/getting-started.md:102、docs/en/getting-started.md:128,口径与
  schema.md zh:91/en:103 三态一致(源级 > 全局 env > 缺省关+未设逐字节一致),
  中英成对;纯散文行,fence/标题零增删。交付 commit **4acc191**。
- **AC2**:grep 亲验 ci.yml ubuntu-latest 清零、ubuntu-24.04 落位 5 处
  (行 13,31,57,82,96,首处带迁移公告注释);desktop-release.yml:274 落位
  (jq 注释保留);desktop-release.yml:54 macos-14 原样;docker-publish/
  pypi-publish 4 处 ubuntu-latest 未碰(不在点名清单,留报)。yaml 解析:ci 5
  jobs 全 ubuntu-24.04,desktop-release 3 jobs(release-finalize 已钉),ok。
  交付 commit **612c427**。
- **AC3**:`uv run --no-sync pytest tests/test_docs.py -q` → **110 passed in
  0.16s**;`python3 -c yaml.safe_load` 两 workflow → jobs 剖面如上,ok;README
  doctest 面 = 不存在(pyproject.toml/pytest.ini/setup.cfg/tox.ini/Makefile 零
  doctest 配置,grep 亲验)——销号。`gitnexus detect-changes -r shishi --scope
  staged`(本流五文件 stage 后):5 files 10 symbols 全文档锚点,**Affected
  processes 0,Risk low**,零代码符号。commit 两笔均 `--only` 明确路径
  (3 文件+2 文件),外来脏面与 index 中外部 label-hint 重命名零触碰。

## 约束(红线)

- 并行会话在途域(desktop ui-src/desktop entry/sidecar 协议/alerts/pipeline/
  test_heartbeat/test_desktop_sidecar_protocol/.trellis/tasks/10-05-dashboard-glance,
  及 index 中已 stage 的 label-hint 重命名)一律不碰不代修;工作树外来脏面不动
  不提交,如实上报。
- `git commit --only` 明确路径,绝不 `git add -A`;不推远端不打 tag;遇
  index.lock 稍候重试;uv 裸 sync 禁用;涉网单次(本轮探查已用罄,后续全本地)。

## 收口轮注记(2026-10-05 夜,尾部纯增量,原文不改)

- **标记 B「正文抽取兜底」装机像素补验 = 已完成(seen=true),leftover ②销号**:
  标记流按配方 `MYIA_SHOW_ON_START=1 MYIA_SMOKE_ROUTE='settings?section=python-env'`
  直跑 /Applications/世事.app 三轮滚动取证——R1 End 键零位移(根因=滚动容器是
  内层 main.overflow-y-auto `app-layout.tsx:27`,body 焦点下 End 滚的是外层
  overflow-hidden 文档,两帧 OCR 框坐标逐字一致证零位移);R2 PageDown×5 重做轮
  命中:中性点击内容区空白带(配方授权的唯一合成输入)后实滚约 285pt,
  「正文抽取兜底」label OCR 置信度 **1.00 @1306,1692**,描述三行逐字对上源码
  `pyenv-card.tsx:222-226`(trafilatura 兜底/MYIA_EXTRACT_FALLBACK 开关/
  selectolax<1),右侧「未装」chip @2801,1748 同帧;R3 小步滚轮(Swift
  CGEvent scrollWheelEvent2Source)down/up 各 8×80px 双向实证(命中卡仍在帧/
  回滚至顶部版位)。事故如实记:R2 首试期间窗被外部并行会话切至「源管理」屏,
  该轮作废,干净重启重做命中。清场三步完成(pkill 烟测实例→launchctl unsetenv
  两烟测 env、getenv 双空核验→open -g 复启,ps eww 无 MYIA_* 烟测 env)。
  佐证引用(既有,未重跑):包内 Resources/components.json 第二件
  id=trafilatura/label=正文抽取兜底/pip_spec 钉版;vitest
  `pyenv-components.test.tsx:165,170`。证据 34 件存 /tmp/myia-sweep/
  (命中帧 b-round2-pagedown-redo.png 626KB 3840x2100)。收口员亲验:命中帧
  png 与 box.txt 行 42「1.00 1306,1692,161x28 正文抽取兜底」实存。取证主体
  归标记流回执,本段为并档注记。
- **索引刷新回执**:gitnexus analyze(不带 -r 形态)退出 0,输出
  「Preserving 22700 existing embeddings」——索引已刷新,既有嵌入保留。
- **CI 实况**:绿(run 37326012359;引自收口回执材料)。
- 本轮收口提交:本档 prd/task.json 收口注记 + workspace journal 清扫段,
  `--only` 三路径;档维持 review(归档循「review 等收口」惯例留主人批次)。
