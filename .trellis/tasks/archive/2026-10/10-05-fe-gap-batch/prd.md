# 前端三小件:fe-gap 批次(侧栏折叠销号/源管理点簇筛选/设置 tooltip 裁撤)

## Goal

基线盘点(2026-10-05 傍晚收口后)定案的 fe-gap 三件,按计划定案处置:
①②a 侧栏分组级折叠——**裁(销号)**,已在库非余量,池档销号+口径更正;
②②b 源管理多选点簇筛选——**实做**(sources-table.tsx);
③②c 设置 tooltip——**裁撤记档**,翻案极小方案留池档。

## Requirements

### ②a 侧栏分组级折叠(销号,零代码改动)

- 已在库:7853d96(2026-10-04)落 GroupSection 全链路
  (`sidebar.tsx:198-243`;ChevronDown size-3.5 折叠旋 -rotate-90、
  `duration-(--duration-fast)`=120ms;条目区 grid-rows 0fr↔1fr 250ms
  Kestra 缓动 cubic-bezier(0.22,1,0.36,1);inert 防键盘焦点;
  独立存储键 `myssia.sidebar-groups.v1` 于 :86/:135/:155)。
- 池档(v12-backlog prd.md §8)两条过期口径更正:「~150ms」→ 实际
  120/250ms;「`rg ChevronDown sidebar.tsx` 零命中」→ 已命中。
- 整栏折叠(拖拽右缘/`[` 快捷键)语义不动——分组折叠与之独立共存。

### ②b 源管理多选点簇筛选(实做,desktop/ui-src/src/screens/sources/sources-table.tsx)

- state 增 `clusterFilter: Set<string>`(簇键=行 pluginFile),与既有
  globalFilter/healthFilter 并列。
- 簇清单 useMemo 从 rows 派生:簇键=pluginFile、标签=pluginLabel
  (name ?? id ?? file)、逐簇源数;localeCompare 稳定排序。
- UI:健康度按钮组(aria-pressed button 先例)同工具栏区加簇 chips 条
  (独立一行防挤爆 32px 控件行):点击 toggle 进/出 Set;chip 徽章带该簇
  源数;Set 非空时显「清除」文字钮。
- 过滤接线:data 前置派生(空 Set=全量零筛选;`rows.filter(r=>
  Set.has(簇键))`)传入 useReactTable——与 globalFilter/columnFilters
  正交叠加,零自定义 filterFn;防御:刷新后失效簇键不再过滤(防空屏)。
- n/m 徽章:chips 行尾显「{filtered}/{rows.length}」+ aria-live。
- vitest 四用例(追加 sources.test.tsx):单簇过滤 / 多选与健康度叠加 /
  n·m 计数 / 清空复位。

### ②c 设置 tooltip(裁撤记档)

- 依据:基线自标弱需求 + 全 UI 零 Tooltip 业务消费(tooltip.tsx 基件在库,
  唯一消费 = 基件自测 ui-base.test.tsx;settings-screen.tsx 零命中)+
  本轮已排 ②b/⑥ 两 UI 件避免面铺宽。
- 翻案极小方案留池档:ui/tooltip.tsx 直接消费,设置屏 3-5 个高困惑字段
  (enrich 模型/探测路径/gates 凭据引用)挂 Radix Tooltip + vitest a11y
  断言,半小时量。

## Acceptance Criteria

- [x] AC1 侧栏折叠销号:池档 §8「侧栏分组级折叠」条目追加已消号注记
  (7853d96 落库证据 + 120/250ms 口径更正),零代码改动。
  证据:v12-backlog prd.md §8 该条尾追加「已消号(2026-10-05)」段——
  GroupSection `sidebar.tsx:198-243`(亲读核对:ChevronDown -rotate-90
  :219-225、grid-rows 0fr↔1fr 250ms :227-231、inert :233)、存储键
  :86/:135/:155、`--duration-fast: 120ms` 定义 `index.css:112` 亲证
  (原「~150ms」池档口径不准,已更正);本流对该文件零代码改动。
- [x] AC2 点簇筛选实现:clusterFilter Set + 簇 chips(aria-pressed+源数
  徽章+清除钮)+ data 前置派生正交叠加 + n/m 徽章 aria-live;空 Set 全量。
  证据:`sources-table.tsx` —— state(:283 clusterFilter Set)、簇清单
  useMemo(:294-307 pluginFile 键+pluginLabel 标签+逐簇数+localeCompare
  排序)、visibleRows 前置派生(:309-314,空 Set=rows;失效簇键剔除防
  空屏)、useReactTable data=visibleRows(:317)、chips 条(:395-457,
  独立行 role=group、aria-pressed、chip aria-label=「标签(n 个源)」、
  「清除」钮(:437-)、n/m 徽章 data-testid=sources-row-count(:447)+
  aria-live=polite,单簇不渲染);底部「共 X 行(全部 Y 行)」计数语义
  自动正确(data 派生后 filtered=三重筛选交集、rows.length=原 props 全量)。
- [x] AC3 vitest 四用例绿:单簇过滤 / 多选×健康度叠加 / n·m 计数 / 清空复位
  (追加 sources.test.tsx,mock sidecar 屏级渲染,零外网零真 IPC)。
  证据:`sources.test.tsx` 追加 describe「源管理:品类点簇筛选」四用例
  (三品类五源夹具:ai-news 2 源含 dead / dev-tools 1 / games 2 含
  degraded);`npx vitest run src/screens/sources/sources.test.tsx` →
  20 passed(16 既有 + 4 新增,2026-10-05 18:51 亲跑)。
- [x] AC4 门禁全绿:`npx vitest run` 全量 + `npm run build`(tsc -b +
  vite build)亲跑通过。
  证据:`npm test` → Test Files 25 passed / **Tests 463 passed**(基线
  459 + 新增 4,对账吻合);`npm run build` → tsc -b 零错 + vite build
  成功(1.59s;>500kB chunk 警告为既有基线状况,非本流引入)。
- [x] AC5 池档收尾:②b 消号注记指向本档;②c 裁撤+翻案方案记档;
  task.json 置 review(归档归收口)。
  证据:v12-backlog prd.md §8 三条各自尾注(侧栏已消号/点簇已消号指向
  本档/tooltip 裁撤+翻案极小方案留池);task.json status=review。

## AC 外核验(GitNexus,编辑后补跑)

- `gitnexus impact -r shishi SourcesTable --direction upstream
  --summary-only`:risk **LOW**,impactedCount 2(直接上游 1 =
  sources-screen.tsx;受影响流程 2 条渲染链)。本流未改 SourcesTable
  对外 props 契约(纯内部 state+派生+UI),上游零适配需求。
- `gitnexus detect-changes -r shishi --scope unstaged`:本流符号 =
  SourcesTable/columns/columnFilters/headers/target(全在
  sources-table.tsx);同报文另见 entry.py×3 + settings-screen×2 符号,
  属并行流 10-05-g10-proxy-probe 的工作树改动,不在本流提交内
  (git status 亲证归属,commit --only 隔离)。

## Notes

- 池档基线锚点 sources-table.tsx:287-291 已漂至 :327-351(健康度按钮组),
  本档以 grep 现码为准,勿硬编码行号。
- git 提交 `git commit --only` 明确路径;不推远端不打 tag。

## 收口回执(2026-10-05 归档轮)

- 收口门禁(收口准备轮亲跑,回执落 3470b59 journal 段;本流 c26f681 已在其树内):desktop/ui-src `npx vitest run` 全量 → **26 files / 474 passed**(=基线 459 + 本流 4 + g10 2 + bundled 9,对账吻合);`npm run build`(tsc -b + vite build)exit 0;全量 pytest **4284 / 0 failed** 与 ruff 全绿(本流零 py 改动,面不受染)。
- CI:run 37304222631(main @ 3470b59,含本流 c26f681)→ **success**;归档轮 `gh run view` 亲验 + `merge-base --is-ancestor` 亲证 c26f681 ∈ 3470b59。
- 收口处置:归档至 archive/2026-10/;消号项已逐条回标池档(②a 销号/②b 实现/②c 裁撤+翻案方案留池);无受阻项。
