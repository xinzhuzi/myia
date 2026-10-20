# 设置屏分析件卡解锁(D8 占位→真开关)

## Goal

设置屏「门槛件」分区的分析件卡从 D8 只读占位升级为 `gates.analysis` 真开关:
两件官方分析件(SnowNLP 情感 / YAKE 关键词)逐件 Switch + 上游/pin 知情警示,
经既有 `gates.save` 整份原子落盘,保存后下一轮 run 生效;未知键透传不丢。

## Background(实证)

- **后端早已真执法,只差 UI**:
  - `src/myssia/analysis_lane.py:70-73` `ANALYSIS_LANE_MEMBERS = {"snownlp": "myssia-snownlp", "yake": "myssia-yake"}`;
  - `src/myssia/pipeline.py:2508` 每轮按 `gate_open(gates_config, "analysis", key)` 逐件判定;
  - `src/myssia/gates.py:199-210` 校验 `analysis.<key>` 键名/布尔;`:495` `gate_open` 读 `analysis.get(name, False)`;
  - `desktop/entry.py:4140` `_m_gates_save` 整份校验 + tmp+rename 原子落盘,协议方法 #55/#56 已在册(见 `.trellis/spec/desktop/sidecar-protocol.md`),**无协议缺口**。
- **UI 仍是 D8 禁用占位**:`desktop/ui-src/src/screens/settings/settings-screen.tsx:801-831`
  卡三只读渲染「批三解锁」Badge;`:617` `analysisEntries = Object.entries(draft.analysis)`;
  保存通道 `saveCard`(`:522-565`)目前只接受 `"paid" | "platforms"`。
- **类型注释仍写「零分析件」**:`desktop/ui-src/src/lib/api/types.ts:1262`
  `停更知情分析件逐件开关(D8:批二仅 schema+设置面占位,零分析件)` —— 与实况不符。
- **归档档明确挂账**:`.trellis/tasks/archive/2026-10/10-05-plugin-market-batch/prd.md:143`
  「①桌面设置屏分析件卡仍为 D8 禁用占位(UI 面不在本批清单;激活通道=CLI
  `myssia gates set analysis.<key> on`,设置面卡待后续批)」—— 本档即该遗留的收口。
- **现有测试钉的是占位态**:`desktop/ui-src/src/screens/settings/settings.test.tsx:1041-1098`
  断言卡内文本含「批三解锁」,且保存付费卡后 `gatesSaved?.analysis` 为 `{}`(本档须保留后一条不变量)。

## Requirements

### R1 卡面:真开关 + 知情警示(替换占位)

- 删掉「批三解锁」Badge、D8 占位文案与空态分支。
- 新增策展清单(UI 常量,镜像后端 `ANALYSIS_LANE_MEMBERS`):
  - `snownlp` — SnowNLP 情感;警示须含「上游冻结」+「pin 版自担维护」+ 钉版 `0.12.3` 隔离子进程(事实见 `plugins/myssia-snownlp/README.md`);
  - `yake` — YAKE 关键词;上游活跃,不得写「上游冻结」(docstring `analysis_lane.py:22-25` 明确此点),文案为「第三方上游,pin 版自担维护」。
- 每行:`SettingRow` + `Switch`,`aria-label` = `分析件开关 ${name}`(与付费卡 `付费引擎开关 ${name}` 同形),`data-testid` = `gates-analysis-row-${name}`。
- 卡描述须讲清真实语义(取自 `analysis_lane.py:10-25`):
  - 与 LLM 精评平行(dedup 后、push 前),装饰 `item.metadata`,不做过滤;
  - 开 = 下一轮 run 生效,关 = 字面零开销(不加载插件码/不 spawn);
  - 失败只进 `report.warnings` + skip 计数,绝不进 `report.failures`、不拦核心品类;
  - 开关只落全局 `gates.yaml` 的 `analysis.<key>`。
- 未知键(CLI/社区件写入的 `analysis.*`):照常显示为行(非官方标记 + 状态透传),
  可切换、可保存,不得在保存时丢弃。

### R2 保存:第三条保存通道(无凭据)

- `saveCard` 的类型扩为 `"paid" | "platforms" | "analysis"`;analysis 分支**不触碰**
  `secret.set`(分析件无凭据),只调 `api.gatesSave({ config: draft })`。
- 新增 `analysisSave` 状态 + `CardSaveBar`,按钮文案「保存分析件」;`dirty === false`
  或保存中禁用;成功回显写入路径(与另两卡同款 note/saved 反馈)。
- 保存失败走既有 `asSidecarError` 结构化错误面,零部分写入由后端契约保证。

### R3 编辑态:只物化已触达键,不写 false 噪声

- 装载时**不**把策展件塞进 `draft.analysis`(与 SaaS 的 `materializeGates` 不同):
  显示用 `draft.analysis[name] ?? false`。
- 切换才写入显式布尔(关 = 写 `false`,与 Switch 语义一致;`gates.py` 接受布尔)。
- 保持现有不变量:保存付费卡/平台卡时,`gates.save` 载荷里的 `analysis` 原样透传;
  未触达的官方件不得因别卡保存被写入 `analysis.snownlp: false`。

### R4 文案与类型注释同步

- `settings-screen.tsx:396-397` 文件头注释更新(D8/批三措辞退场)。
- `types.ts:1262` 注释改为实况(两件官方分析件已可经设置屏开关)。

## Acceptance Criteria

- [x] A1 设置→门槛件→分析件卡:两行官方件 + Switch,页面不再出现「批三解锁」
      与 D8 占位文案;每行含「自担维护」警示,snownlp 行含「上游冻结」,yake 行
      不含「上游冻结」。
- [x] A2 打开 snownlp 开关 →「保存分析件」→ `gates.save` 载荷含
      `analysis.snownlp === true`;无 `secret.set` 调用;保存状态显示写入路径;
      重新装载后开关保持开启。
- [x] A3 不触碰分析件、仅保存付费卡时,`gates.save` 载荷 `analysis` 与装载值逐键
      相等(官方未触达键零注入;既有测试 `analysis === {}` 不变)。
- [x] A4 `gates.get` 返回未知键(如 `analysis: {"custom-x": true}`)时:行可见、
      有非官方标记;任一卡保存后该键仍在载荷中且值不变。
- [x] A5 dirty 门:未改动保存按钮禁用;切换后启用;保存成功后回到禁用。
- [x] A6 门禁:vitest settings 套件 + `tsc --noEmit` 全绿;Python 全量测试不受影响
      (无后端改动)。
- [x] A7 桌面实跑冒烟:设置屏分析件卡可见、可切换、保存后重进分区状态保持
      (实现阶段按项目 UI 验证纪律在 dev/沙箱实例完成,并留证)。

## 边界

- **不做**后端/协议改动:不加 sidecar 方法、不 bump 协议版本、不改 `gates.py`
  与 `analysis_lane.py`;若实现中发现契约缺口,停下报主人另立档。
- **不做**分析件总开关(语义上不存在;只逐件)。
- **不扩**策展清单:新增分析件 = 后端 `ANALYSIS_LANE_MEMBERS` 核心改动,本档只镜像
  现有两件;UI 常量旁留一行注释指向上表,防静默漂移。
- **不碰** `third_party_trace`(D9 无执法点,维持 UI 不提供假开关)与付费/平台卡行为。
- 测试零真实插件加载/spawn/网络;仅协议桩。

## Notes

- 本档为纯前端小件(预计 1 个文件 + 测试),按 lightweight 任务执行,PRD-only 有效。
- 主人决议:本档无需额外拍板 —— D8/D10 已定案,本档只是执行归档档在册的「设置面卡待后续批」。

## 执行记录(2026-10-20)

- 实现:`settings-screen.tsx` 分析件卡占位换真开关(官方两行 + 未知键透传、
  逐件 note、非官方 Badge);`saveCard` 增 `"analysis"` 第三通道,无
  `secret.set`;装载不物化官方键,切换才写显式布尔;付费/平台卡保存原样
  透传 `analysis`。`types.ts` 与文件头 D8 措辞同步。
- 测试:`settings.test.tsx` 覆盖 A1-A5(官方两行/警示文案/开关保存载荷/
  零 secret.set/重新装载保持/付费卡零注入/未知键透传与可切换/dirty 门);
  `npx vitest run src/screens/settings/settings.test.tsx` → **48 passed**;
  `npx tsc -b --pretty false` → **exit 0**。
- A7 沙箱实跑:临时构建 `npx vite build --outDir /tmp/myia-settings-ui`
  (跳过 tsc,仅取证),`/tmp/settings-analysis-smoke.py` 以 sidecar IPC 桩
  驱动真实设置屏(静态服务 + headless Chromium):
  - 门槛件分区渲染两行;页面无「批三解锁」;snownlp 行含「上游冻结/0.12.3/
    自担维护」,yake 行含「自担维护」不含「上游冻结」;
  - snownlp 开关初始 `aria-checked=false`,保存按钮初始 disabled;
  - 切换 → true、按钮启用 → 点「保存分析件」→ `gates.save` 载荷
    `analysis={"snownlp":true}`,`secret.set` 调用数 0,保存条回显
    「门槛配置已写入 /tmp/home/gates.yaml」,按钮回 disabled;
  - 切到 general 分区再回 gates → `aria-checked=true`(重进保持)。
  - 结果串:`{"status":"passed","saved_analysis":{"snownlp":true},
    "secret_set_calls":0,"remount_checked":"true"}`;
    截图 `/tmp/myia-settings-smoke/settings-gates-analysis.png`(保存后)、
    `/tmp/myia-settings-smoke/settings-gates-analysis-remount.png`(重进后)。
  - 未覆盖方法仅 `pyenv_get_status` / `pyenv_migration_banner` /
    `plugin:log|log` / `plugin:event|emit`(与本卡无关)。
