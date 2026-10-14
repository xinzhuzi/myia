# 点选式可视化建源

## Goal

八爪鱼点选式任务配置,YAML 编辑器远期形态;对标八爪鱼/EasySpider(AGPL 只看不抄)/Maxun;V1 形态由设计拷问定案。

**V1 定案(本 PRD):表单向导生成 YAML**——多步表单填一填、试一采,落成一份合法品类 YAML。不做自由画布、不做页面内点选注入(八爪鱼全形态留远期;EasySpider 式「内嵌预览 + 点选」的 Tauri 技术路径未定,是 V2 设计拷问的第一议题)。

## 一句话形态

源管理屏顶栏「新建品类」按钮打开**屏内多步向导对话框**(不新路由、不新侧栏行、零新 sidecar 协议方法):基本信息 → 源信息 → 提取规则 → 预览保存 → 试采验证,五步走完产出 `config/<id>.yaml`,完成页深链去「YAML配置」补全下游。

## 调研锚点(结论存档;设计拷问与 design.md 详引)

- **结构主锚 = EasySpider**(AGPL-3.0,**只借交互思想,禁止参考其源码实现**;design.md 须留「未参考其源码实现」注记)。可借:设计时/运行时分离(builder 只产出/校验 YAML,运行时零改动走既有引擎管线)、设计期样例值回显(试采先看抓到什么再定稿)、单步试运行闭环(填了选择器→立刻试→看结果→再改)。
- **UX 北极星 = 八爪鱼 Octoparse**(闭源商业,无码可借)。借「Auto-detect 起步 + 精修」分层入口思想:V1 的「表单+试采」= 低门槛起步层;AI 入口(说需求自动建源)是 MYIA 远期(顺接 README.md 头部「说需求,AI 做其余」定位)。
- **次参照 = Maxun**(AGPL-3.0,形态映射最重:全栈 Web + 浏览器池 + PostgreSQL,**架构一律不借**)。只借「录制产物 = 声明式可版本化定义」原则——MYIA 产物是 YAML 本身,可 diff/可 git/可手改,与 YAML 编辑器两形态共用同一份真相。
- **表达力边界**:MYIA 源 YAML 是声明式单源(extract list + pagination,`config/gpu-prices.yaml:11-34` 实读),不是有环有分支的命令图。V1 向导只覆盖**列表页 + 字段 + 翻页三件套**;超出者引导走 YAML 编辑器手写,不可静默丢弃。
- **源 ≠ 整个 YAML**:一个品类 YAML 还有 watchlist/classify/push/baseline 等下游段(`config/gpu-prices.yaml:36-85`)。向导只管 `sources[].extract` 段,完成页必须引导去 YAML 编辑器补下游,防「点几下=完整配置」的误解。

## 用户故事

- 我看到一个网站想监控它的列表页,不会写 YAML、不会开浏览器开发者工具到能抄选择器的深度以外的东西。我在源管理点「新建品类」,按向导填网址、粘贴两条选择器(页面上教我去哪抄),点「试一试」,看到抓回来的真实条目,确认没问题点完成——一个每天自动跑的源就有了。
- 我已经会用 YAML 编辑器。向导对我只是快速打底:生成骨架后一键跳过去补 watchlist 和 push。

## Requirements(V1)

### R1 入口与形态(并入屏族,不新造画布)

- R1.1 入口 = 源管理屏顶栏既有「新建品类」主操作(`desktop/ui-src/src/screens/sources/sources-screen.tsx:239-244`,现为 `<a href="#/yaml-editor">`)改绑为打开向导对话框;图标(Plus)与按钮文案不变。
- R1.2 形态 = 源管理屏内多步向导对话框,视觉与交互范式沿本屏既有弹窗(YamlEditorDialog 的 fixed 遮罩 + 居中面板 + ESC/遮罩/关闭钮三径同关;宽度取宽档,给表单与结果留位)。步骤条(五步名)置顶,底部「上一步/下一步」导航。
- R1.3 向导头部提供次入口链接「直接编辑 YAML」→ `#/yaml-editor`(既有深链,零改动保留)。
- R1.4 不新增路由、不改 `App.tsx`、不动侧栏 `NAV_GROUPS`、不动 command-palette `SCREENS`。

### R2 向导五步

**第 1 步 基本信息**

- 品类 id:单行输入。约束 = 品类 id 同款正则(前端预检镜像 `CATEGORY_ID_PATTERN`,权威 `src/myssia/schema.py:368` `^[a-z0-9][a-z0-9_-]{0,63}$`);placeholder 与帮助文案说明「小写字母/数字/-/_,也是文件名」。id 同时用作 YAML `id:` 与文件 stem(`<configDir>/<id>.yaml>`,一处输入两处用途,与 `yaml.save` 新建围栏一致,`desktop/entry.py:3141-3149`)。
- 品类名 name:单行输入,中文自由填(落 YAML `name:`)。
- 抓取频率 schedule:下拉预设四选 + 自定义。预设:「每天一次(上午 10 点)」= `"0 10 * * *`、`「每小时一次」= `"0 * * * *`、`「每 6 小时」= `"0 */6 * * *`、`「每周一上午 9 点」= `"0 9 * * 1`;自定义 = cron 五段表达式输入框(帮助文案一句话解释五段是什么)。schema 必填无缺省(`src/myssia/schema.py:1794`),故本步不选完不进下一步。
- 同名预检:本步加载时用既有 `yaml.list`(`desktop/ui-src/src/screens/yaml-editor/api.ts:164-166`)的文件清单对比 `<id>.yaml` 是否已存在;已存在 = 输入框下即时提示「已有同名文件,保存会被拦;换一个 id 或去 YAML配置 编辑它」(预检不拦输入,后端 `mtime_conflict` 是终门)。

**第 2 步 源信息**

- 源名 name:单行(默认预填 `main`;落 `sources[0].name`)。
- 页面地址 url:单行,前端预检 http(s)(后端终门 `invalid_url`,`src/myssia/schema.py:850-856`)。
- 引擎:**V1 锁定 `static_html` 不暴露选择**,表单显示为固定说明行「适合服务器渲染的普通网页列表(浏览器里右键→查看网页源代码能看到内容的页面)」。其他引擎/rss/详情页进钻的源,完成页与帮助文案引导走 YAML 编辑器。
- 翻页(可折叠,默认「不翻页」):三选一——不翻页(不生成 pagination 节)/ 网址带页码(url 需含 `{page}` 占位,输入框即时校验占位符在场,生成 `mode: template` + max_pages 数字输入,默认 5,范围 1-10000)/ 点「下一页」链接(填下一页按钮的 CSS 选择器,生成 `mode: selector` + 该选择器,`src/myssia/schema.py:655-675` 同构)。`scroll` 模式不提供(L4+ 引擎语义,V1 锁 static_html 不适用)。
- 浏览器标识 User-Agent(可选):默认预填 gpu-prices 同款 Chrome UA 串(`config/gpu-prices.yaml:17`);留空 = 不生成 headers 节。

**第 3 步 提取规则**

- 结构说明一句话(人话):「先框住页面上重复的整条(比如一行商品),再告诉每条里哪个部分是标题、哪个是链接」。
- 列表整条的选择器 item:单行 CSS 选择器输入(帮助文案:浏览器里右键该元素 → 检查 → 右键高亮节点 → Copy → Copy selector)。
- 字段表 fields:动态行(字段名 + CSS 选择器),可增删行、行内排序不需要。预置两行:`title`(提示「标题」)与 `url`(提示「链接」);url 行选择器旁附快捷开关「取链接地址」= 自动给选择器追加 `@href` 后缀(生成 `h3 a@href` 形态,`config/gpu-prices.yaml:25-27` 同构)。
- 校验:fields 至少 1 行且必含 `url` 字段名(否则 schema `missing_url_field` 拒载,`src/myssia/schema.py:789-795`);字段名重复即拦;item 为空不进下一步(`missing_extract_item`)。
- V1 不做:页面预览、元素点选、选择器自动猜测(全部留 V2 设计拷问;「备选选择器回退」思想走 Scrapling/L4 已有能力,不在向导层实现)。

**第 4 步 预览与保存**

- 顶部生成 YAML 原文(等宽字体只读预览,生成规则见 R3),侧栏/下方给逐项中文摘要(id/频率/网址/翻页/字段数)。
- 「保存」按钮钉序:① `validateYaml(content, null)` 干跑(`desktop/ui-src/src/screens/yaml-editor/api.ts:177-179`),有 error 级 finding = 停在本步原样展示 findings,不发保存;② 通过则 `saveYaml(file, content, expected_mtime)`(`api.ts:191-193`)——首次保存 expected_mtime=null(新建);保存成功记住应答 `mtime` 与 `file`,后续重存带它(乐观锁)。
- 结构化错误如实展示、留在本步可改:`invalid_file_stem` / `mtime_conflict` / `duplicate_category_id` / `category_invalid` 等既有错误码族(`desktop/entry.py:3100-3224`),每条给人话解释行。
- `mtime_conflict`(外部改过/撞同名)文案指路:「文件已被其他窗口改动。可关闭向导去 YAML配置 对照,或换个 id 重来」——V1 不做冲突覆盖/三方合并。

**第 5 步 试采验证**

- 保存成功后本步自动发起:`api.sourcesTest({ file, source: 源名, timeout: 60 })`(既有共享门面方法,`desktop/ui-src/src/screens/sources/api.ts:21-24` 注记、协议 `desktop/entry.py:3377-3429`);发起失败(`test_busy` 等)如实展示并给「重试」。
- 结果 = 既有 `test.completed` 事件回屏 → `buildTestOutcome`(`sources/api.ts:357-401`)→ **向导内嵌摘要**(成功与否、命中引擎、抓到条数、前 5 条样例的字段值表)+「查看详情」按钮打开既有 `TestResultDialog`(零改动复用,`desktop/ui-src/src/screens/sources/test-result-dialog.tsx:10-15` props 形态)。样例值回显是本向导核心体验(EasySpider exampleValues 思想的映射):用户看见抓回来的真实标题和链接,才信这份配置是对的。
- 试采不满意 =「返回修改」回第 3 步(表单态全保留),改完重走保存(第 4 步持上次 mtime 重存,.bak 自动留底)再试采。
- 试采通过 = 完成态:显示落盘路径 + 两个出口按钮:「去补全推送等配置」→ `#/yaml-editor?file=<file>`(既有深链预选,`desktop/ui-src/src/screens/yaml-editor/yaml-editor-screen.tsx:103-111`);「完成」关闭向导并刷新源管理列表(reload 既有 health 链路)。

### R3 YAML 生成器(纯函数,产物钉死)

- 新建 `build-category-yaml.ts`:表单态 → YAML 文本,纯函数、无 IO、可直接单测。
- 产物 = 最小合法模板(`desktop/entry.py:2839-2849`)的严格超集,字段顺序与节注释钉死如下(全中文注释、人话):

```yaml
# 由建源向导生成:普通网页列表采集(每天到点抓一页/几页,提取列表字段)。
# 只配了采集;关键词过滤、分类、推送等下游配置请到「YAML配置」补全。
id: <id>
name: <品类名>
schedule: "<cron>"
sources:
  - name: <源名>
    engine: static_html
    url: "<url>"
    method: GET
    headers:            # 仅当用户填写 UA 时生成;空则整节不出现
      User-Agent: "<UA>"
    pagination:         # 仅当选了翻页时生成;不翻页则整节不出现
      mode: template    # 或 selector(带 selector: "<下一页选择器>" 行)
      max_pages: <N>
    extract:
      type: list
      item: "<item>"
      fields:
        title: "<选择器>"
        url: "<选择器>@href"
        <自定义字段>: "<选择器>"
```

- timezone 不生成(缺省走本地);watchlist/classify/dedup/enrich/push/storage 全不生成(schema 有 default_factory,`src/myssia/schema.py:1797-1802`,模板即先例)。
- 缩进、引号风格与 `config/gpu-prices.yaml` 对齐(字符串值带双引号);产物唯一性由生成器单测锁定(给定表单态 → 逐字节断言文本)。

### R4 状态机与守卫

- 新建 `use-source-wizard.ts`:五步状态机(当前步/表单态/保存态{file, mtime, saved}/试采态),供对话框消费。
- 关闭守卫:表单有任何输入或已保存未完成时,ESC/遮罩/关闭钮三径先弹确认「向导内容还没走完(已保存的文件会保留),确定关闭?」;未动过任何字段则直接关(沿 YamlEditorDialog dirty 守卫先例)。
- 已保存文件在关闭后不回收(那是用户的成果;不想要去 YAML 编辑器删,那里有 .bak)。

### R5 文案纪律

- 全人话零生造词:「抓取频率」不是「schedule」、「翻页」不是「pagination」、「试一试」或「试采」统一用「试一试(抓 1 次看看)」首现、后续「试一试」;错误消息里保留后端 code(排障用)但必须跟一句人话解释。
- 不上屏的词:「engine 链」「退化链」详情归 TestResultDialog(它已有既定文案);向导摘要里引擎名如实显示。

## 非目标(V1 明确不做)

- 页面预览与点选注入(Tauri 单 webview 无扩展机制,技术路径未定——V2 设计拷问第一议题:子窗口 webview / 本地代理改写注入 / CDP 挂真实浏览器)。
- 选择器自动检测/猜测、备选选择器生成与回退(回退是引擎层 L4/Scrapling 的事,不在向导层)。
- 引擎选择暴露(锁 static_html)、extract.type 其他值(item/json_path/rss)、多源品类、POST/自定义 headers/代理/限速等高级源参数——统统引导 YAML 编辑器。
- 下游段配置(watchlist/classify/push/baseline…)与「向导反向导入既有 YAML 再编辑」。
- AI 建源入口、模板市场、云协同(八爪鱼商业形态,与 MYIA 本地单机定位冲突,防被带偏)。

## Acceptance Criteria

- [x] AC1 源管理顶栏「新建品类」打开五步向导对话框;App.tsx/侧栏/command-palette/`desktop/entry.py` `_HANDLERS` 零改动(diff 可证零新路由零新协议)。
- [x] AC2 第 1 步:id 不合正则即拦(前端预检,不发请求);schedule 未选不进下一步;同名文件即时提示。
- [x] AC3 第 3 步:fields 缺 `url` 字段名或 item 为空即拦,提示人话;字段行可增删。
- [x] AC4 生成器单测:至少 3 组表单态(不翻页/template 翻页/selector 翻页 × 有无 UA)逐字节断言产物文本,且产物过 `yaml.validate` valid=true(测试内真实调用 mock invoke 或用生成器快照+validate 契约桩分离断言)。
- [x] AC5 保存链:干跑有 error 停第 4 步不发保存;保存成功记住 mtime;`mtime_conflict`/`duplicate_category_id` 人话展示可改重试。
- [x] AC6 试采链:保存后自动发起 sources.test(timeout 60);`test.completed` 后内嵌摘要(条数+前 5 条样例值);「查看详情」打开既有 TestResultDialog 且其组件零改动。
- [x] AC7 闭环:试采失败 → 返回修改 → 重存(带 mtime)→ 再试采全链可用;完成页「去补全推送等配置」深链 `#/yaml-editor?file=` 生效(编辑屏预选该文件)。
- [x] AC8 关闭守卫:有输入时三径关闭均先确认;关闭后已保存文件保留;源管理列表在完成/关闭后刷新。
- [x] AC9 `source-wizard-dialog.test.tsx` + 生成器测试全绿;既有 `sources.test.tsx` 零回归(顶栏按钮改绑后其断言同步更新)。
- [x] AC10 UI 全 token 化(spec frontend-ui 反 AI 审美红线过检);文案全人话,无「job/engine 链/指纹」词裸上屏(详情弹窗既有文案除外)。

## 红线与纪律

- **AGPL 双红线**:EasySpider/Maxun 均 AGPL-3.0,只借交互/数据形态思想,**不参考其源码实现、不搬任何文件**;EasySpider 另有「定制提取流程服务封装系统」发明专利主张(2022),不得 1:1 复刻其流程细节。design.md 留「未参考其源码实现」注记。干净先例线:Playwright codegen / Chrome DevTools Recorder(Apache-2.0/BSD 系)+ MYIA 已依赖的 Scrapling(L4 自适应,README.md:379)。
- 零新 sidecar 协议方法、零 Python 侧改动(全部编排走既有 yaml.*/sources.test/health);若实现中发现「必须加后端方法才能做」,停下回 PRD 而不是顺手扩协议。
- 产物是 YAML 文本本身(Maxun「录制存声明式定义」原则):不引入第二份「向导工程文件」;向导关闭即丢表单态,真相只有 config/ 下的 YAML。

## 既有件复用清单(避免重做)

| 既有件 | 位置 | 向导用法 |
|---|---|---|
| yaml 六方法封装 | `screens/yaml-editor/api.ts:164-198` | 直接 import(先例:first-run-guide.tsx:9 跨屏 import) |
| 品类 id 正则镜像 | `screens/yaml-editor/api.ts:117-122` | 直接 import 同一常量 |
| 试采发起 + 事件 | `api.sourcesTest` 共享门面 + `test.completed` | 原样调用 |
| 试采结果视图 | `buildTestOutcome`(`screens/sources/api.ts:357-401`) | 原样调用 |
| 试采详情弹窗 | `screens/sources/test-result-dialog.tsx` | 零改动复用 |
| 保存/校验/乐观锁 | `entry.py` `_m_yaml_save/_m_yaml_validate` | 原样依赖 |
| 试采 job | `entry.py` `_m_sources_test` | 原样依赖(timeout 60) |
| 模板与最小合法形 | `entry.py:2839-2849` | 生成器超集基准 |
| 顶栏按钮位 | `sources-screen.tsx:239-244` | 改绑 onClick |
| 弹窗范式 | `yaml-editor-dialog.tsx`(dirty 守卫/三径关闭) | 借结构 |

## 远期路线(V2+,本 PRD 不承诺)

1. 页面预览 + 点选注入(技术路径设计拷问定案:Tauri 子窗口 webview / 代理改写 / CDP)——点选语法对标 EasySpider「右键→相似元素→列表四选一」,产物仍是同一份 YAML 的 extract 段。
2. 自动检测起步(Octoparse Auto-detect 层:抓首页 HTML 猜 item+fields+翻页,人确认)。
3. AI 入口(「说需求,AI 建源」;与 enrich/LLM 凭据链衔接)。
4. 向导反向导入(既有 YAML 载入表单迭代)。
