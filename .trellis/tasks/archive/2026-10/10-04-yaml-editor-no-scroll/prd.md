# YAML 编辑器缺陷修复:滚动裁剪(主)+ ESC 误关弹窗 + 补全开关误导

## Goal

源管理行内编辑弹窗与配置编辑屏共用 EditorPane:@uiw 的 .cm-theme 容器无定高,cm-editor height:100% 对不定高父级退化为内容高,外框 overflow-hidden 裁剪→330 行文件只见头 ~39 行、滚轮/键盘全无效。实测根因+修复方向已验证(给 CodeMirror 传 className=h-full 或 .cm-theme{height:100%})。

- **报障**:主人 2026-10-04 晚,「yaml 好像弹出的内容不对,也不能上下滑动」(源管理屏行内编辑弹窗)。
- **性质**:功能性缺陷(非 reskin 回归;d359a3e 10-03 交付即坏,无头冒烟未覆盖滚动;4fdda1a 行点击也开弹窗后暴露面变大)。
- **优先级**:P1——两处配置编辑入口对超过一屏的品类文件事实上不可用(看不见也改不到头屏之后的内容)。

## Requirements

### 1. 症状与实测证据(无头复现,HEAD=当前工作树)

复现环境:沙箱 MYIA_HOME + 真 sidecar(`desktop/entry.py serve`,bridge.mjs)+ vite(5173)+ Playwright。
harness 与证据:`evidence/probe.py`、`evidence/probe-result.json`、截图 ×4、补丁版 `evidence/shim.js`;沙箱插件含 330 行的 games.yaml。

**症状 A「不能上下滑动」——两处编辑入口全中招:**

| 量测项 | 弹窗(源管理行编辑) | 双栏配置编辑屏 |
| --- | --- | --- |
| 外框(EditorPane 根 div)实高 | 618px(有定高 ✓) | 889px(有定高 ✓) |
| `.cm-theme`(@uiw 内部容器)实高 | **7419px(auto,随内容撑开)** | **7419px(同)** |
| `.cm-editor` 实高 | **7419px**(height:100% 失效) | **7419px**(同)** |
| `.cm-scroller` scrollH/clientH | 7419/7419 → 无滚动 | 7419/7419 → 无滚动 |
| 滚轮 800px 后 scrollTop | **0** | **0** |
| 编程置 scrollTop=400 | **0** | **0** |
| PageDown 后 scrollTop | **0** | **0** |

**症状 B「弹出的内容不对」——与 A 同根因的表现,内容本体没错:**

- 磁盘 games.yaml 330 行;弹窗 DOM 里 `.cm-content` 只物化 **39 行**(CM6 视口虚拟渲染,scrollTop 恒 0 只渲染头屏)。
- 头 3 行与磁盘逐字一致(`head_equal: true`);`.cm-content` 总高 7419px ≈ 330 行 × 行高(heightmap 完整)——文档本体完整,用户「永远翻不过第一屏」所以看着不对。
- 内容链路无嫌疑:`pluginFile`(health PluginReport.file)→ `yaml.read`(逐字节原读)同源同根,前端未改写。

### 2. 根因(代码级)

`desktop/ui-src/src/screens/yaml-editor/editor-pane.tsx` 结构:

```
EditorPane 根 div(min-h-0 overflow-hidden …;弹窗/屏都给了定高 h-full ✓)
  └─ <CodeMirror height="100%">   ← @uiw v4.25.12 渲染出 div.cm-theme(无任何高度类)
        └─ .cm-editor             ← height:100% 主题规则(KESTRA_CHROME & + @uiw dimensionTheme)全打这层
```

- 两发 `& {height: 100%}` 命中的都是 `.cm-editor`(实测规则命中 `.ͼ17`/`.ͼ18`),但父级 `.cm-theme` height 是 auto(不定高);CSS 百分比高对不定高包含块解析为 auto → 退化成内容高 7419px。
- 外框 618px + `overflow-hidden` → 裁掉 ~7100px:无滚动条,滚轮落在不可滚的 scroller(scrollH==clientH)上全部无效。
- `@codemirror/view` baseTheme 的 `.cm-scroller` 只有 `overflowX: auto`,竖向滚动依赖编辑器有定高——定高失效是链头。

### 3. 修复方向(已在复现现场注入验证,未动仓库代码)

往活页面注入 `.cm-theme {height: 100%}`(等价给 `<CodeMirror>` 传 `className="h-full"`)后实测:`.cm-theme`/`.cm-editor` 616px、`.cm-scroller` clientH 616 / **scrollH 7347 → scrollable=true**,编程置 scrollTop=2000 生效,CM6 虚拟渲染随滚动正常换行(`evidence/dialog-fix-sim.png`)。

**推荐改法**(一行,仓库 tailwind 惯例):`editor-pane.tsx` 的 `<CodeMirror … className="h-full">` —— @uiw 渲染 `class="cm-theme h-full"`(`node_modules/@uiw/react-codemirror/esm/index.js:84-88`),`.cm-editor` 的 height:100% 随父级定高生效。备选:在 `KESTRA_CHROME` 或全局 CSS 加 `.cm-theme {height: 100%}`。

## 2026-10-05 grill 决议(主人按推荐全批,3 项)

| 决议点 | 定案 |
| --- | --- |
| 补全开关(Q1) | **本档关闭 `autocompletion`**——lang-yaml 无补全源,开关开着永远无候选属误导;词级补全源 / schema 感知补全若要做**另立档**,不混入缺陷修复 |
| ESC 修复口径(Q2) | **`event.defaultPrevented` 前置守卫**(实现时核实 CM 面板确实调用 preventDefault);不做焦点语义重设计(过度工程) |
| 开工顺序(Q3) | **本档先行**(P1、用户可见、改动小);10-04-unified-dev-entry 随后 |

## Acceptance Criteria

- [x] **弹窗滚动**:源管理屏点任意行「编辑」,330 行 games.yaml 在弹窗内可用滚轮/触控板/键盘滚动至文件尾(无头断言:`.cm-scroller` scrollH > clientH 且编程置 scrollTop 生效)。(回标 2026-10-05:`editor-pane.tsx:55` `<CodeMirror className="h-full">` 落到 `.cm-theme` 打通定高链;§3 复现现场注入等价 CSS 已实测 clientH 616 / scrollH 7347→scrollable=true、编程 scrollTop 生效;单测锁链见回归防护条;门禁绿)
- [x] **双栏屏滚动**:配置编辑屏(`#/yaml-editor`)同文件同样可滚。(回标 2026-10-05:双栏屏与弹窗共用同一 EditorPane 组件,弹窗侧外框 h-full(`yaml-editor-dialog.tsx:129`)链路同修,一处改动两入口同覆盖)
- [x] **内容完整**:滚动到文件尾可见磁盘最后一行(`storage:` 段);头尾与磁盘逐字一致。(回标 2026-10-05:§1B 已证内容链路无改写(330 行=heightmap 7419px、头 3 行逐字一致),所见「不对」= 裁剪表现;定高链打通后全文档随滚动可至尾行,内容零改动)
- [x] **回归防护**:`editor-pane.test.tsx` 加断言(CodeMirror 收到 h-full/等价类),防高度链再丢。(回标 2026-10-05:`editor-pane.test.tsx` 新增「高度链」用例,真渲染断言 `.cm-theme` classList 含 `h-full`;本会话局部自检 2 文件 12 用例全过)
- [x] **ESC 不误关**:CodeMirror 子面板(⌘F 搜索面板)开着按 ESC 只关子面板,编辑弹窗保留、dirty 状态不变(缺陷 2,`defaultPrevented` 守卫,见补二)。(回标 2026-10-05:`yaml-editor-dialog.tsx:67` keydown 首行守卫;前提已核实 `@codemirror/search` dist:1055 Escape 绑 search-panel scope + dist:1145-1148 面板命中即 preventDefault;`yaml-editor-dialog.test.tsx` 新用例:已 preventDefault 的合成 ESC 不触发 onClose/confirm,弹窗仍在)
- [x] **补全开关关闭**:`editor-pane.tsx` basicSetup 移除 `autocompletion`;`closeBrackets`/折叠/括号匹配等其余项保留(grill 决议 Q1)。(回标 2026-10-05:`editor-pane.tsx:62` 已删该行,lineNumbers/foldGutter/highlightActiveLine/bracketMatching/closeBrackets 五项原样)
- [ ] **中文输入(IME)**:修复后人工在编辑器敲一段中文确认组合输入正常(无头测不了 IME,CodeMirror 6 理论支持,主人日常中文场景须实证)。**(2026-10-05 03:00 自测回标:文本插入已自动 PASS(B4);真实 IME 组字自动化实测已尽力——搜狗拼音在位+辅助功能已授权,但 osascript 合成键盘不达 WKWebView、面板经顶栏清理(7152ff9)后无按钮入口纯 ⌘K(设计态,自测代理误判陈旧构建已由主会话更正)、且启动即弹钥匙串授权框需主人亲自「始终允许」——此条终态=主人亲手敲一段,自动化通道已探明边界)**
- [x] **门禁**:vitest + tsc + build 全绿。(回标 2026-10-05:工作流脚本统一执行前端构建/前端单测/全量 pytest 全绿;实现会话局部自检 `npx tsc -b` 0 错 + vitest 两改动文件 12 用例过)
- [x] **装机包刷新**:入库后重打包静默换装(「完成=入库+门禁绿+装机包已刷新」纪律),主人只做目验:开弹窗滚到文件尾 / 敲一段中文 / ⌘F 开面板按 ESC 弹窗仍在。(回标 2026-10-05:三段链终包 ce9878d 换装留痕 `evidence/install-log-final.md`(01:33,含与旧产物尺寸差异证新码进包);其后并行线 02:09 再换装更新尖;**装机包自动冒烟对当前 /Applications 包全 PASS(A 六项+B 全组,含滚动/ESC/中文插入/保存回路),实跑日志与截图 `desktop/ui-src/e2e/artifacts/`;目验三步已被冒烟代码覆盖,主人仅需真实 IME 组合输入手感一条)**

## 2026-10-05 补(一):编辑链全面体检(17/17 PASS,零新功能缺陷)

主人问「还有其他 yaml 问题吗 / 有办法编辑输入吗」——同 harness(evidence/probe2.py + sweep-checks.log)对编辑链全量体检,**除已录的裁剪/滚动缺陷外未发现新功能缺陷**:

- 输入与脏跟踪:键盘输入生效、标题 `*` 脏标记、保存按钮随 dirty 解禁 ✓
- 校验:坏 yaml 出结构化 error findings(「未知字段 'broken',schema 不允许 fail-fast」)✓
- 保存回路:Cmd+S 保存成功提示、doctor 复核(识别品类+源数)、落盘含编辑、`.bak` 留底、保存后脏标记清除 ✓
- 守卫与切换:dirty confirm 放弃后重开回磁盘原样;切另一文件内容正确切换 ✓
- 双栏屏:左栏列文件、载入、输入 ✓
- 已知限制(本缺陷的直接后果,**随滚动修复自然解除**):裁剪 bug 期间编辑被实际限制在头一屏——光标移到 39 行以下时看不到正在输入的位置。
- findings 结果区滚动:`max-h-40 overflow-y-auto` 代码级保障(体检时量测未精确隔离该元素,不构成缺陷记录,修复验收时顺带目验)。


## 2026-10-05 补(二):编辑器内核功能实机核验(含 1 项更正 + 1 个新缺陷)

主人质询「实际深度探查了吗」后,对内核功能逐项实敲(evidence/probe3.py、probe4.py、k6/k7 日志):

| 功能 | 实测结果 | 证据 |
| --- | --- | --- |
| 撤销/重做(⌘Z / ⇧⌘Z) | ✓ 正常 | probe3 T1/T2 |
| ⌘F 搜索面板 + 跳转命中行 | ✓ 正常(需编辑器先有焦点,属正常行为) | k7:activeLine 跳至 `sources:` 命中行 |
| 全部替换 | ✓ 正常 | probe4 T4:probe-xyz→probe-abc 落文 |
| 代码折叠 | ✓ 正常(fold gutter 7 个标记;折叠 `sources:` 块出 placeholder) | k7(首次测在注释行上属探针选行不当) |
| **词级自动补全** | ✗ **实际不可用——更正**:产品代码 `autocompletion: true` 只是开关,`basicSetup` 空参调用 `autocompletion()` 且 @codemirror/lang-yaml **不带任何补全源**(dist 无 completionSource),任何输入都不会出候选 | k6 T6 无弹窗 + 静态核实双包 |

### 缺陷 2(新):ESC 冒泡误关整个编辑弹窗

- **现象**:CodeMirror 子面板(如 ⌘F 搜索面板)开着时按 ESC,本意只关子面板,实际**整个编辑弹窗被关**(probe3:`搜索面板开着按 ESC:弹窗仍在=False`;非 dirty 时静默关,dirty 时突然弹放弃确认)。
- **根因方向**:`yaml-editor-dialog.tsx` 的 window 级 keydown 监听不检查 `event.defaultPrevented`(CodeMirror 面板已消费该键并 preventDefault,但事件仍冒泡到 window)。
- **修复方向**:`if (event.defaultPrevented) return;` 前置守卫(实现时核实 CM 面板确实调用了 preventDefault)。
- **验收补条**:搜索面板开着按 ESC → 只关面板、编辑弹窗保留、dirty 状态不变。

### 可选增强(2026-10-05 grill 已决:本档只关开关;以下若做另立档)

- 词级补全源(文档已出现的词)约 +30 行;进阶品类 schema 感知补全(需 py 侧 schema → JSON Schema)。两者均为**独立立项候选**,本档不做。

## Notes

- 附带发现(不入本档修复范围,复用 harness 时注意):
  - 归档 shim(`10-03-fe-small-batch/evidence/touch-harness/shim.js`)缺 `window.__TAURI_EVENT_PLUGIN_INTERNALS__`(新版 @tauri-apps/api event.js:100 unlisten 会读),浏览器直开时组件卸载即抛 pageerror;本档 `evidence/shim.js` 已补 no-op,后续复用以此为准。
  - 归档 seed.py 仍 import 旧包名 `myia`(已改名 myssia),复用时绕过(本次直接 touch 空 myia.db + 拷插件 yaml 即可起 sidecar)。
