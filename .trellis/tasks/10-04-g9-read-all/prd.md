# G9 全库批量已读:服务端批量标记(store+协议扩展)

> **2026-10-04 重开(终局后翻案)**:本档同日曾被终审撤并(wrapup-checklist prd:64-70 / 2237bf9 消号);主人令『按照你的建议继续做完』,余量两小件经拍板重开补做,范围即 R1/R2/R4+AC6;Grill 五问按推荐定稿(主人令授权),协议零新增零 bump 铁律不变。

## Goal

fe-gap-census 路由件(matrix.md R5:「G9 全库批量已读(store/协议扩展)|立档(架构级,先 grill)」):feed「全部标已读」从已加载作用域升级为服务端真批量。**立档时依赖核实发现:在途批 10-04-read-state-server 已把 store/协议扩展本体整体吃下**(见下节),故本档定位收窄为——**依赖收口之后的作用域入口与确认交互增量**,不重复造任何已落地面。

## 依赖核实结论(2026-10-04 立档时实读在途档+工作树;依赖前置=10-04-read-state-server)

census 路由时不知情项:matrix 在途声明(`.trellis/tasks/10-04-fe-gap-census/research/matrix.md:5`)只列 interaction-batch 六件,未计 read-state-server——而后者 prd 标题即「G9 服务端已读态**+全库批量已读**」(`.trellis/tasks/10-04-read-state-server/prd.md:1`),其 grill 决议 Q3.2 明写 `store.state.mark_all` 是「全库批量语义的核心件」、R4 含「『全部标已读/未读』按钮语义升级为全库(title 换真话)」、AC3/AC7 为验收口径;task.json `status: in_progress`。

立档时工作树实况(未提交,read-state-server 在途 diff):

- store 层:`src/myssia/store/sqlite.py:914` `set_all_item_states(marker, value, category=None)` 已落——全库单 UPDATE,category 精确等值与 `list_items` 同参、不收 query(决议 Q3.2 钉死);`set_item_states` :885 / `import_item_states` :939;SCHEMA_VERSION=8(:88)。**注意包名漂移**:read-state-server 的 implement.jsonl 仍引 `src/myia/store/sqlite.py` 旧径,现树为 `src/myssia/`。
- 协议层:`desktop/entry.py:978` `_m_store_state_mark_all` 已实装,`:4800` _HANDLERS 注册(`store.state.mark`/`mark_all`/`import` 三行 :4799-4801);PROTOCOL_VERSION=10(:456;v10 注记=read-state-server 批,hermes-cron 先合 v9 的竞速条款已落地 `sidecar-protocol.md:112`)。
- 协议档 mirror:`.trellis/spec/desktop/sidecar-protocol.md:80-82` 注册行 #58-60 已加,`:109-112` 版本注记已记。
- 测试:`tests/test_read_state.py`(未跟踪新文件):310-334 已含 mark_all 全库置位 / category 精确等值(:318-324)/ 空串 category ValueError(:333-334)用例。
- UI:`desktop/ui-src/src/screens/feed/feed-screen.tsx:994-1018` `markAllRead` 双路已落——过门走 `storeStateMarkAll`(乐观翻转已加载行+调用前快照回滚),未过门走 `setMarkerBulk` 本地批量;过滤区两按钮 `:1246-1279` title 双路真话(过门=「全库所有条目(含未翻页)…服务端持久」/未过门=「已加载的 N 条…本地态」)。`client.ts:193-199` 三方法封装、`types.ts:960-962` 方法表齐。

**裁定**:census R5 所指「store/协议扩展」本体已在途实现,本档**不得重复立项实现**;本档全部增量骑在 read-state-server 收口之上,开工第一门=核实其收口实况(见 R0/AC1)。

## 现状缺口(本档真正的余量;行号按立档时工作树,在途 diff 中,开工实读重取)

1. **按品类批量:协议+store 已留门,UI 零消费**。`mark_all` 的 `category` 参数三端齐(store :914 / entry :978 / types+client),但 feed 屏唯一调用点 `feed-screen.tsx:1000` 只传 `{marker:"read", value}`,全屏无品类级批量入口(rg 实况:仅过滤区全库两按钮)。census 需求面点名「按品类」作用域,这是本档主增量。
2. **确认交互:无**。「全部标已读/未读」按钮 onClick 直发(`:1260`/`:1275`),全库置位无二次确认;全库单 UPDATE 影响全部条目(含未加载),误触代价大。
3. **按当前筛选作用域:未做且被钉死**。read-state-server 决议 Q3.2「不收 query(LIKE 语义进 UPDATE 是范围蠕变)」;census 需求面提「按当前筛选」,若要=翻案重 grill(见 Grill Q1)。
4. **未过门旧通路**:`setMarkerBulk` 已加载作用域(`api.ts:214-230`),依赖档钉死保留,本档不动。
5. 同族余量(提及不扩 scope):未读 FILTERS 过滤=已加载作用域(`feed-screen.tsx:1024` applyFeedFilter 作用于页内条目)——read-state-server AC10 钉死「未读过滤全库化另立」,本档非目标。

## Grill 5 问(全带推荐;主人/B 设计师回写前不开工)

2026-10-04 定稿:五问照推荐(重开时主人令授权)。

### Q1 作用域形态:全库 / 按品类 / 按当前筛选,本档收哪些?

**推荐**:全库=维持已落地形态不动;本档补「**按品类**」UI 入口(协议零新增,category 参数现成);「**按当前筛选**」维持否掉——搜索词圈定批量范围易误伤(搜索命中 title+content,用户对范围心智弱),且依赖档决议已钉死不收 query,翻案需主人明示理由。若翻案收 query:协议扩参数+PROTOCOL_VERSION 实读+1+mirror 同步,量级升 medium+。

### Q2 协议方法形状:要不要另立 `feed.read.mark-all` 之类新方法?

**推荐**:**否**。复用已落地的 `store.state.mark_all`(依赖档 Q3.2 已决挂 `store.` 数据面家族,v10 已注册已测);读态是 store 投影状态,再造 `feed.` 家族=同义方法双轨。本档**协议零新增、零版本 bump**;唯一翻案口=Q1 若收「按当前筛选」需在 mark_all 上扩参数(而非新方法)。

### Q3 幂等与二次确认:全库批量要不要确认步?要不要 Undo?

**推荐**:幂等已落地(mark/mark_all 显式置值,无读-改-写,依赖档 Q3.1),无需再设计;**补 inline 二次确认**——仓内有意惯例=AlertDialog→inline 确认(settings 先例,matrix 1.3#6),「全部标已读/未读」两按钮同门(一次点击进入确认态,再点执行,Esc/失焦取消);**Undo toast 不推荐**——全库改前快照不可行(未加载条目无客户端真值),且「全部恢复未读」不是无损对冲(会把本就已读的条目一并翻回未读)。

### Q4 桌面 UI 入口:品类级批量放哪?

**推荐**:品类分组组头入口——`display.groupMode === "category"` 时组头行尾小按钮(「本组全部已读」),`group.key` 即 `item.category`(`api.ts:519-522`),与 mark_all category 精确等值同词直配;**红线:未分类组 key=null 不可传**(mark_all 的 category 缺省=全库,null 直传会全库置位),未分类组不设入口(title 如实说明或干脆不出钮);时间分组/不分组模式不出组头入口。过滤区既有全库两按钮保留。不开右键菜单/⌘K 新面(interaction-batch 在途占面,勿重叠)。

### Q5 与 feedback mute 等既有批量语义的关系?

**推荐**:**语义分立,不共用通道**。三通道各司其职:feedback mute=词级压制(品类 watchlist+反馈 0.0 权重词,`entry.py:4264-4271`,作用于评分/推送判定,非条目状态);`setMarkerBulk`=未过门旧通路的已加载批量(`api.ts:219`);`store.state.mark_all`=服务端全库/品类状态置位(可逆双值)。本档不引入「批量 mute」(词级语义归 feedback/调参面),不动未过门通路,不与 mute 合并入口。

## Requirements(按推荐口径展开;grill 翻案则对应改写)

- R0 依赖门(开工第一步):实读 read-state-server 收口实况——task.json status=completed(或至少协议 v10+mark_all 三端已合主干)、`tests/test_read_state.py` 绿;实况回写本档 Notes。未收口不开工。
- R1 按品类批量入口:品类分组组头动作触发 `storeStateMarkAll({marker:"read", value:true, category:<group.key>})`;乐观翻转该组已加载行+失败按调用前快照回滚(同 `markAllRead` 惯例);未分类组(key=null)处置按 grill 决议(推荐:不出钮)。
- R2 确认交互:全库「全部标已读/未读」两按钮 inline 二次确认(确认态→执行;Esc/失焦/再点取消);品类入口按 grill 决议(推荐:豁免——作用域小一级,组头钮即时执行+title 如实;若主人要同门则同门)。
- R3 协议纪律:本档零新增方法、零版本 bump、mirror 零加行;收口时如实核验记录(AC4)。
- R4 文案如实:品类入口 title/aria-label 注明「该品类全库(含未翻页)」;过门通路文案不出现「已加载」字样。

## Acceptance Criteria

- [x] AC1 依赖门兑现:本档 Notes 记录 read-state-server 收口实况(task.json 状态/协议 v10 在主干/test_read_state.py 实测绿,含命令与输出)。
- [x] AC2 品类入口:分组=品类模式下组头动作以该组 category 调 `store.state.mark_all`;乐观+失败快照回滚可见(feed-mark-error 行同门);未分类组(null)无入口或禁用且 title 如实;时间/不分组模式无组头入口。
- [x] AC3 确认交互:全库两按钮不直发——确认步后执行,Esc/失焦取消可验;品类入口按决议口径可验。
- [x] AC4 协议对账:收口时 `_HANDLERS` 无本档新增行、PROTOCOL_VERSION 与 read-state-server 收口值一致(本档不 bump)、协议档 mirror 无本档加行;核验记录回填。
- [x] AC5 文案:入口 title/aria-label 作用域真话(品类级=该品类全库含未翻页);过门通路无「已加载/本地态」字样残留。
- [x] AC6 测试:vitest 用例覆盖 AC2/AC3(组头入口参数/确认流/失败回滚),实测命令与输出回填;python 侧无新协议面不新增用例(复核 test_read_state.py:318-334 category 用例在主干即复用)。

## 非目标

- 按当前筛选(query)批量作用域——除非 grill Q1 翻案明示。
- 未读过滤全库化(store.items read 查询参数)——read-state-server AC10 钉死另立。
- 未过门旧通路(setMarkerBulk/localStorage `myia.feed.states.v1`)任何改动。
- retention 剪枝豁免(starred/later 过期语义)——read-state-server Q4.2 另立。
- CSV 导出列集、feed.export JSONL 投影——依赖档已定,本档不碰。
- 批量 mute / feedback 语义合并。

## Notes

- 立档员:G9 立档员(census R5 路由),2026-10-04;只立档未动 desktop/ 与 src/ 任何文件,未 commit。
- 行号口径:立档时工作树(read-state-server + interaction-batch 双在途未提交),开工须实读重取;包名 myia→myssia 已漂移,以现树为准。
- 必读:`.trellis/tasks/10-04-read-state-server/prd.md`(裁决基准+依赖实况)+ `.trellis/tasks/10-04-fe-gap-census/research/matrix.md`(G9 条目 :73 / R5 路由 :115)。**重开时路径已漂移**:read-state-server 已归档,现路径 `.trellis/tasks/archive/2026-10/10-04-read-state-server/prd.md`(本档 implement.jsonl 依赖行已按归档路径写);fe-gap-census 同已归档至 `.trellis/tasks/archive/2026-10/10-04-fe-gap-census/`。
- **R0 依赖门兑现记录(2026-10-04 重开时立档恢复员实跑)**:
  - `.venv/bin/python -m pytest tests/test_read_state.py -q` → **26 passed in 0.36s**(全绿);
  - `desktop/entry.py:456` `PROTOCOL_VERSION = 10`;`_m_store_state_mark_all` 定义 `desktop/entry.py:978`、`_HANDLERS` 注册 `desktop/entry.py:4800`(三端在册);
  - `git log --format='%h %s' -1 afa7339` → `afa7339 feat(desktop): G9 读态迁服务端——store.state.* 三方法(协议 v10)+UI 能力门+一次性 localStorage 搬迁`(提交在库);
  - read-state-server `task.json` `status: completed`(已归档 `archive/2026-10/10-04-read-state-server/`)。R0 判定:**过门**。
- **档务实况(重开时如实记)**:本档 prd 曾两度被并行会话按撤并口径删除(17:1x 首次落盘→19:05 核实在盘→发布帖收尾清扫再删),本次由主会话二次落盘(逐字原文);立档恢复员据此完成头部重开注记+Grill 定稿行+本 Notes 回写。
- **收口勾验记录(2026-10-04 晚,收口员会话;feat 提交 fe9f1ed)**:AC1=R0 记录在案(上上条,:86-90)。AC2/AC3=`feed-screen.tsx` 实读核验——品类组头钮只在 `useServerState && groupCategory !== null` 出场,onClick=`markAllRead(true, groupCategory)` 以该组 category 精确等值调 `store.state.mark_all`;乐观翻转与失败快照回滚均按 `inScope` 谓词只落作用域内行(域外组不动),失败走 `setMarkError`(feed-mark-error 同门);未分类组(null)不出钮、时间分组 category 恒 null 零入口、未过门组头零入口;全库两钮走 `confirmAllMark` inline 确认(一次点击只进确认态零 RPC,「确认」才执行;Esc 全局监听(输入框内不抢)/失焦(relatedTarget 出「确认/取消」簇)/「取消」三路退出);品类入口按 Q3 推荐豁免确认(即时执行+title 如实)可验。AC5=品类钮 aria-label/title 含「该品类『X』全库条目(含未翻页)」真话;过门全库两钮 title 文案无「已加载/本地态」字样(diff 实读)。AC6=`feed-screen.test.tsx` 新增 describe「g9-read-all」5 用例(R1 参数精确等值+就地翻转只落该组/R1 失败快照回滚域外不动+feed-mark-error/仅品类分组模式有钮/R2 三路退出零执行/未过门零入口)+既有 G9 用例改写为二次确认口径;**收口实跑 `cd desktop/ui-src && npx vitest run src/screens/feed/feed-screen.test.tsx` = 1 file / 76 tests passed(19:50:48)**;本轮工作流脚本统一门禁=vitest 全量 22 文件/374 用例+tsc+vite 构建绿(尾输出转录于收口令与 journal,非收口会话自跑);python 侧零新协议面不新增用例,`tests/test_read_state.py` category 用例已在主干(R0 复跑 26 passed 为证)。
- **AC4 协议对账记录(2026-10-04 晚收口实跑)**:`git diff --stat -- desktop/entry.py .trellis/spec/desktop/sidecar-protocol.md` = **空**(协议面零触碰);`PROTOCOL_VERSION = 10`(`desktop/entry.py:456`,与 read-state-server 收口值一致,本档不 bump);`store.state.mark_all` 注册在册 `desktop/entry.py:4800`(afa7339 既有,`_HANDLERS` 无本档新增行);协议档 mirror 既有行 `sidecar-protocol.md:81`(注册表 #59)+ `:277`(错误码读态行),无本档加行。**判定:过(零新增方法/零 bump/mirror 零加行)**。
- **质检两低危处置(2026-10-04,mustFix=false 维持不改)**:①确认态触发钮卸载后焦点回落 body,确认钮簇无 autoFocus 补位(键盘/读屏需重 Tab 定位「确认」;AC3 字面已满足且无错误行为,可访问性改进点备案);②品类组头入口随 `displayItems`(过滤后集合)渲染——默认「未读」过滤下某品类已加载行全已读时该组不出场、组头入口暂不可达,切「过滤:全部」恢复(该品类仍可被全库两钮覆盖,语义无错,边界知会在案)。(**2026-10-04 晚补遗轮已修**:①②均奉主人令补修——①确认主钮 `autoFocus` 已落/②「过滤:未读」title 知会已落、行为级事实不变;见「质检两低危补修」条与「补遗」行。)
- **实现自报偏差(收口如实转录)**:确认态为「常规两钮整体让位给确认/取消一对」(循 settings inline 先例;若设计要求确认期间另一颗常规钮保持在场需再调一处 JSX 条件);品类组头钮无禁用条件(已加载视图口径无法如实代表品类全库作用域,幂等显式置值重复点击无害,PRD 未钉死禁用口径按最小面);首跑 1 例时序抖动(「j/k+U 联动」用例,本 diff 未触碰路径)——复跑 3 次+HEAD 基线 2 次均全绿,判负载下 waitFor 超时非本批引入。
- **质检两低危补修(2026-10-04 补遗轮,主人令修;白名单 feed-screen.tsx / feed-screen.test.tsx)**:①件一键盘焦点——确认主钮(`feed-screen.tsx` 确认簇 destructive 钮)补 `autoFocus`:进入确认态时焦点落确认主钮,触发钮卸载不再致焦点回落 body(键盘/读屏无需重 Tab);既有簇级 onBlur 经实读本就是「焦点离开整个确认/取消簇才取消」口径(`relatedTarget` containment 判定,程序化初始焦点在簇内不构成簇级退出),零改动即兼容,取消逻辑未动。react-dom `commitHostMount` 对 `button` 标签 autoFocus 时调 `focus()`(node_modules react-dom-client.production.js 实读核验)。②件二可达性知会——按质检原判落最小面:「过滤:未读」钮加 title「未读过滤会隐藏已加载行全已读的分组(含其批量入口);切『全部』可恢复」;默认未读过滤下某品类已加载行全已读时该组不出场、组头批量入口暂不可达的**行为级事实不变**(组头随 displayItems 过滤后集合渲染,客户端拿不到未翻页计数,行为级修复必破协议零新增铁律故不为),过滤/分组渲染语义零改。测试补两条:件一断言进确认态后 `document.activeElement` 为确认主钮+Esc 仍取消零执行;件二 title 静态断言(含其余页签零附加文案)。协议零新增零 bump、setMarkerBulk 未动、未 commit。
- **补遗(2026-10-04 晚,收口员)**:两条 low 登记已修——件一 autoFocus(测试 1 条)/件二 title 知会(测试 1 条);过滤/分组语义与协议面零改动。feat 提交 dcaa2d9(feed-screen 两件纯增量 60 行零删,autoFocus=`feed-screen.tsx:1395`/title=`:1333`,测试=`feed-screen.test.tsx:1766`/`:1794`);门禁=本轮工作流脚本统一实跑 vitest 全量 22 文件/376 用例(上轮 374→376 恰合 +2)+tsc+vite 绿(尾输出转录,收口会话未自跑);复验发现与处置=[];提交前实跑 `gitnexus detect-changes -r shishi --scope staged`="No changes detected"(纯属性/用例增量,零符号级行为变更,与上轮 feat 批 4 symbols/6 流程对照如实记)。档维持 review 不动,归档+终勾留主人。
