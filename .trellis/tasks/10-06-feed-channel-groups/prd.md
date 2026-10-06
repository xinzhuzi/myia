# 情报流渠道级分组

## Goal

主人三令合一(2026-10-06):
1. 「情报流也要分渠道呀」+「不同渠道表现的方式不一样」——渠道(源名全称规约 telegram-<频道> 等)细分 + 按渠道类型差异化呈现;
2. 「情报流要不停地过信息日志,每天凌晨 3 点清零,继续过滤」——实时滚动 + 每日 03:00 视图清零;
3. 「二级界面分类,一层一层点击进去」——导航形态从平铺分组改为**三级下钻**(L1 品类 → L2 渠道 → L3 消息流)。

验证纪律(主人 10-06 追令):**UI 验证一律程序化(vitest + 无头 GUI 冒烟 Playwright 判例),禁控制电脑**;装机件同步照旧(备份/ditto/sha 对拍);像素确认走无头截图证据文件。

## Requirements

### R1 渠道分型呈现(卡面,所有层级生效)
- telegram-*/tg-* 源名前缀 → 消息卡:气泡(正文在泡内)+ 频道名(去平台前缀)+ 相对时间;
- engine=urlwatch(health 源名→engine 映射)或条目带 watch_event → 变更事件:「有更新」徽标 + 时间 + 目标页链接(watch_page 真链;条目 url 是 #watch-<sha> 锚);
- engine=prompt/store_report → 日报 markdown 文档视图(可折叠正文;MarkdownLite 零依赖渲染);
- 品类 games/wool 或价格键在场 → 价格/优惠行:现价突出(等宽)+ 原价划线 + 折扣/限免徽标(dealPriceView 镜像 games.yaml push 模板 elif 链与 classify 限免析取);
- 其余 → 新闻列表卡(现状原样,回归安全)。

### R2 三级下钻导航
- L1 = 品类列表(health().plugins 词汇源 ∪ 已加载条目品类):置顶「全部条目 · 滚动流」全局行 + 品类行(色点 + 今日/未读/渠道计数);
- L2 = 品类内渠道列表:渠道行带类型基因(图标+类型词)+ 窗内计数;头部「本品类全部已读」(mark_all 带 category 精确等值,豁免二次确认);
- L3 = 渠道消息流(分型呈现主场):store.items 带 category+source 精确等值 + 游标分页;工具条(读态分段/计数/搜索/刷新/显示选项/导出);渠道作用域下批量与导出不出钮(协议无 source 粒度的 mark_all/export,范围不实);
- 面包屑:情报流 / 品类 / 渠道,逐级可退;j/k/U/Mod+F 热键只属 L3;品类分组显示选项退役(品类维度 = L1/L2 层级本体,历史存储值就地映射回时间四桶)。

### R3 实时滚动 + 03:00 当日窗
- 实时滚动:completed / cron.completed 事件即时刷新 + 30s 可见性感知轮询兜底(隐藏暂停;mergeFreshItems 前插新键,已加载行与游标零扰动);
- 当日窗:每日 03:00 清零 = **视图层**当日窗滚动(03:00 → 次日 03:00,窗口锚写死 DAY_WINDOW_ANCHOR_HOUR=3,配置位预留);滚动流(未读/全部)过窗离场、视图从零累计;store 数据不动(retention 照旧);星标/稍后读与 later 到期重现条目 = 显式留存,跨窗可见;工具条/概览窗锚知会。

### R4 协议最小面扩展(entry.py)
- `_item_dict` 白名单补价格/优惠七键(price_text/sale_price/normal_price/final_price/original_price/discount_pct/savings_pct;final_price 兼收人民币分 int 与 CS·GOG 美元串)+ urlwatch 事件两键(watch_event/watch_page);
- `store.items` 增 `source` 精确等值参数(与 category 同门;空串/非字符串 invalid_params)—— L3 渠道流查询面;
- spec 同步:.trellis/spec/desktop/sidecar-protocol.md。

## Acceptance Criteria

- [x] AC1 五档渠道分型卡面可见(vitest 组件测 + 无头冒烟截图:telegram 气泡/watch 徽标+目标链/document markdown/deal 价格行/news 现状);
- [x] AC2 L1→L2→L3 三级点击路径可用,面包屑回退可用;L3 查询带 category+source 精确等值(桥请求日志为证);
- [x] AC3 实时刷新可见新条目(事件 + 轮询;无头冒烟:沙箱直插新行 + visibilitychange → 新行前插);
- [x] AC4 03:00 当日窗滚动后视图从零(纯函数边界 + 屏测:窗外条目未读/全部离场、星标跨窗、窗锚知会在场);
- [x] AC5 门禁:vitest 全绿 + tsc 0 错 + vite/tauri build 通过;pytest 协议面投影/过滤测试通过;
- [x] AC6 gitnexus detect-changes 核验(影响流全在情报流域);
- [x] AC7 装机件同步:重打包 + 备份 + ditto 换装 + 主二进制 sha 对拍;无头冒烟对**装机包内源**跑通(sidecar = 装机 myssia-src + 仓库 venv);
- [x] AC8 验证程序化:零 cliclick/零屏控;证据 = 冒烟断言输出 + e2e/artifacts/feed-channels/ 截图文件。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

---

## 执行追踪(子代理工作面,主人令「子代理做的事/将做的事落实到档」)

**在途执行**(2026-10-06 派工,后台工程师代理进行中):

| # | 事项 | 状态 |
|---|------|------|
| 1 | 情报流品类下按**渠道分组**(源名全称规约 telegram-<原名> 等) | ✅(形态升级为三级下钻,见 R2) |
| 2 | **分型呈现**五种:telegram-* 消息卡(气泡+时间+频道名)/RSS 标题链接列表/urlwatch 官网监控=变更事件徽标/prompt 日报=markdown 文档可折叠/游戏羊毛=价格行 | ✅ |
| 3 | **实时滚动**(当日不停过日志:自动刷新节奏,新条目持续进流;刷新机制按前端既有模式选型,防高频打爆 sidecar) | ✅(主人追加;事件驱动+30s 可见性轮询) |
| 4 | **每日 03:00 视图清零**(当日窗 03:00-次日 03:00;只清视图不动 store,retention 照旧;窗口锚缺省 03:00) | ✅(主人追加) |
| 5 | 数据面:走 sidecar 协议既有 items 查询(带 source);不足则最小面扩展 | ✅(store.items 增 source 精确等值 + _item_dict 价格/watch 白名单) |
| 6 | 门禁:vitest 全绿+tsc 0 错 | ✅(570/570 + tsc 0) |
| 7 | 装机:重打包+换装(sha 对拍)+ 无头程序化验证(判例改写:禁控制电脑) | ✅(无头冒烟 feed_channels_smoke) |
| 8 | AC 补两条:实时刷新可见新条目;跨 03:00 窗口滚动后视图从零 | ✅(AC3/AC4) |
| 9 | (主人三令)**二级界面分类一层层点击进去**:L1 品类 → L2 渠道 → L3 消息流 | ✅ |

**关联前置**:telegram 持续监控线(10-06-telegram-telethon,planning)落地后,群消息实时进流=本屏「不停过日志」的信源;本任务先行把窗口与分型做好等流进来。

## 过程(执行流水,完工逐项回填)
- [x] 渠道分组落地 → 三级下钻(文件:desktop/ui-src/src/screens/feed/{feed-screen.tsx,api.ts,markdown-lite.tsx};提交:见结果节)
- [x] 五型呈现落地(FeedCard kind 分派 + dealPriceView + MarkdownLite)
- [x] 实时滚动机制选型与落地(completed/cron.completed 事件 + 30s 可见性轮询 + mergeFreshItems 前插)
- [x] 03:00 当日窗+视图清零落地(dayWindowStart/inDayWindow + visible 管线过滤)
- [x] vitest/tsc 门禁(570/570;tsc 0)
- [x] 装机重打包+换装+无头程序化验证(冒烟 PASS 计数与截图清单见结果节)

## 结果(验收回执,完工填)
- [x] AC 全勾记录+无头证据(见下「装机与冒烟回执」)

## 装机与冒烟回执

- **构建+换装**(2026-10-06 19:19,零屏控):`npx tauri build` exit 0;主二进制 sha256
  `4af5d62b0bed9f88d6dc4e276bb07af921343ca34120f44d3927cfc3286dead3`(构建产物与
  /Applications 装机件双验一致);备份 `/tmp/myssia-app-backup-20261006-191944-drill`
  (前版另存 `/tmp/myssia-app-backup-20261006-185125`);WKWebView+Caches 清理;包内
  Resources/myssia-src/entry.py 亲核含 source 参数与价格/watch 白名单(17 处命中)。
- **无头程序化冒烟**:`desktop/ui-src/e2e/feed_channels_smoke.py`(复用 package_smoke
  判例:同源 HTTP 桥 + __TAURI_INTERNALS__ shim + Playwright headless;sidecar =
  **装机包内** myssia-src + 仓库 .venv;沙箱 MYIA_HOME 五类九行种子)——
  **21/21 PASS**:L1 当日窗知会/全局滚动流行/五品类行;L2 渠道行类型词(新闻/监控/
  频道/日报)+ 品类批量入口;L3 store.items 带 category+source 精确等值(桥 RPC
  日志为证);分型五档(watch「有更新」徽标+目标页主机名 / telegram 气泡+频道名
  durov / document markdown 展开 / deal ¥0.00+限免+¥39.00 划线);面包屑 L3→L2→L1;
  实时滚动(沙箱直插新行 + visibilitychange → 新行前插)。
- **截图证据**(headless chromium 截图文件,非屏控;OCR 交叉核对文字可见):
  `desktop/ui-src/e2e/artifacts/feed-channels/`:01-l1-categories(L1 品类+当日窗知会)/
  02-l2-channels / 03-l3-watch-channel / 04-l3-telegram-bubble(气泡+durov) /
  05-l3-document-markdown / 06-l3-deal-price(¥0.00+限免+¥39.00)/ 07-live-refresh。
  local-ocr 抽检:01 图命中「当日窗 03:00起·实时滚动·今日9条/未读9」「全部条目·滚动流」;
  04 图命中「情报流 > Telegram频道监控」「durov」「Telegram 消息甲…」;06 图命中
  「Epic 演示限免游戏」「¥0.00 ¥39.00」。
- **门禁**:vitest 570/570(26 文件;feed 屏 105 例含三级下钻/分型/实时滚动/当日窗);
  tsc -b 0 错;pytest tests/desktop 288/288(新增 source 精确等值 + 价格/watch 投影两测);
  vite build + tauri build 通过;gitnexus detect-changes:改动面 = feed 屏 + entry.py
  投影/查询面,影响执行流全在情报流域(FeedScreen 中心度高致评级 high,实测无域外破环)。
- **说明**:①UI 验证全程程序化(主人 10-06 追令),先前 cliclick 判例作废,未再触
  前台;②并行会话(10-06-native-plugin-components)提交的 bundled-plugins-card.test.tsx
  有 tsc 类型错(CFA 不追踪闭包赋值)阻塞全仓 build,本批一行 cast 修复(运行时语义
  不变,`resolveGet as ((value: unknown) => void) | null)?.({})`);③同会话工作树另有
  telegram/crawl4ai/urlwatch 等在途脏文件,本提交经 `git commit --only` 定向,未触碰。

## 追加回执:合并日报价值门槛 min_score(2026-10-06 20:20,出口线收尾)

主人判例「有价值才进,不裸塞」的最后一块(与 341c4cb TG 频道价值筛同线):
`store_report` 的 `sections` 增可选 `min_score`(缺省 `None`=不过滤,现状语义零变化)。

- **语义**:低于线(enrich `value` 0-10 制,严格小于)条目不进分区正文,分区尾折一行
  `   ……(另有 N 条低价值条目,价值分<X)` 留痕;**无分条目不拦**(`scores.value`
  缺席/bool/非数值=无分,取分口径=push/digest `_digest_order_key` 判例,精评未覆盖
  ≠低价值);排序维持 store newest-first 既有判例(不加值排序);门槛拦在
  `max_entries` 帽之先(低价值不占正文席位);**整区低于线时折叠行即内容**——分区
  照渲染、报表照发,`store_report_window_empty` 哨兵只留给真空窗(窗不空,静默才是
  说谎);`report_sections` metadata 增 `low_value` 计数(加法,不动旧键)。
- **配置**:`plugins/daily-digest.yaml` AI 资讯分区配 `min_score: 3`(口味可调),
  其余分区缺省不动。
- **提交**:`9859911`(3 文件 +341/−15;`--only` 定向,并行脏文件 desktop/entry.py、
  telegram/serve.py、desktop 测试未碰,未推远端)。
- **门禁**:本文件测试 38→48 例全 mock(+10:阈值拦截/折叠行/无分不拦/贴线分==线
  不拦/bool 口径/门槛先于帽/整区低价值留痕不发静默/缺省 None 现状/yaml 装载校验
  端到端);全量 4722 passed / 40 skipped;`uvx ruff` 过;gitnexus impact(render_report
  LOW,私法 0 上游)+ detect-changes(staged)= 3 文件 39 符号 0 执行流,风险 LOW。
- **装机外科**(2026-10-06 20:13):备份 `/tmp/myssia-minscore-backup-20261006-201301`
  (bundle store_report.py + 数据根 daily-digest.yaml 前版);同步两件——bundle
  `世事.app/Contents/Resources/myssia-src/myssia/engines/store_report.py`(换前 sha
  =HEAD~1 亲核无并行漂移)与数据根 `~/Library/Application Support/MYIA/plugins/
  daily-digest.yaml`;sha256 对拍双验一致(`c4b330c8…` / `314aef59…`);engines 陈旧
  `__pycache__` 清除;`codesign --force --deep -s -` 重签,`codesign -vv` = valid on
  disk / satisfies its Designated Requirement。
- **装机态装载校验**(仓库 venv + PYTHONPATH=bundle myssia-src,零真网内存库):
  ①store_report 装载自装机包路径;②registry 解析 store_report;③数据根 yaml 装载
  AI 资讯 min_score=3、其余分区缺省;④装机代码端到端:高分进正文/低分折叠行
  (价值分<3)——4/4 过。cron 挂点 fb85edaf94ac(每日合并日报,数据根 yaml 路径)
  未动,下次 2026-10-07 08:05 自动带门槛跑。
- **统一收尾批复核**(终局收尾员,2026-10-06 20:19-20:31):9859911 两件(bundle
  `store_report.py` `c4b330c8…`/数据根 `daily-digest.yaml` `314aef59…`)sha256 复核
  与仓库 HEAD(5345efe 静置)一致零漂移——本收尾批外科对象为桌面接线批 5345efe
  两件(entry.py/telegram serve.py),装机包同窗 adhoc 重签+`codesign -vv` 双过、
  `open -g` 静默拉起+ticker 心跳双验在案(明细见 telegram-telethon 档过程段
  「统一装机收尾」),装机实例保持常驻;全量门禁亲跑:pytest 4810 passed/40 skipped
  exit 0(**=HEAD(5345efe)+20:33 时点并行在途件的工作树**,并行会话 20:28-20:35
  持续写入中间态致首轮 4 failed、复跑全绿,19:23 先例同型;纯 HEAD 基线无法在本
  窗口重跑如实分界)+ vitest 570/570(跑窗干净)+ tsc -b 0 错。

## 追加回执:独立深审修复批(2026-10-06 20:52,F1/F2/F3/F4/F5/F6/F7)

- **修复面七发现**(提交 `eef5ff1`,5 文件 +546/−104;store 层 F6 另批 `4acfc42`、
  桌面 `_m_store_items` 协议级 category 强校验随 telegram 批 `bced6c5`):
  - **F1 L1/L2 只吃全局首页 50 条→假空态**:L1 行计数/全局行统计/L2 渠道列表改按
    品类查询(store.items 带 category 游标,每品类一页 50 勿全量拉;词表=health 选项
    ∪全局页品类,join 串依赖防身份抖动);L2 进层定向补查;liveRefresh 在 L1/L2 顺带
    刷概览。长尾品类假空态/假零回归测试(品类查询确实发出+端到端下钻可见)。
  - **F2 liveRefresh/refresh 竞态**:请求序号守卫(每发包取新票,应答落地前对票,
    旧应答丢弃)——refresh 慢应答不覆盖 liveRefresh 已并入新行;切作用域后旧域包
    不把全局行混进 scoped 流;loadMore 同门;概览独立对票;两竞态场景测试。
  - **F3 mark_all(category) 全库作用域错配**:L2 豁免钮作用域收窄到当日窗——逐键
    置位(store.state.mark keys=窗内已加载品类页行),UI 所见=实际作用域;补「窗内
    未读」反向出口;title 如实不再宣称全库;R1 两测重写(keys 精确集钉死,窗外旧键
    不入)。
  - **F4 markdown-lite 死链**:裸链接走 openInBrowser 受控门(plugin-shell open,
    capabilities 与「打开原文」同门);点击行为测试(shell.open 收到 URL)。
  - **F5 dealPriceView 字符串价格降级**:Number() 宽容解析三键(final_price/
    original_price/discount_pct,types.ts 同批放宽);布尔/空串/NaN 不猜;形态测试。
  - **F6 热键守卫补 <select>**:feed 屏 u/j/k 与 Esc 两处本地守卫补 SELECT(use-hotkeys
    底座本有,屏内漏);select 聚焦敲 j 不巡游+对照测试。
  - **F7 分组桶口径**:groupFeedItems 桶边界与当日窗对齐(03:00 锚)——00:00-03:00
    条目组头如实标「昨天(上一窗口)」;凌晨视角昨日下午条目=「今天」(窗口对齐另一
    面);DST 注记(Shanghai 无 DST 零影响);边界测试重写+凌晨视角测试。
- **门禁**:vitest 全量 **577 passed**(feed 屏 112 例,深审批新增 6 例+重写 3 例);
  `tsc -b` 0 错;pytest/ruff 见 telegram 批回执(同窗全量 4810 passed)。
- **装机外科**:与 telegram 深审批同窗一次 `npx tauri build` 重打包换装(UI+Python
  同包),明细见 telegram-telethon 档「追加回执:独立深审修复批」(备份/sha 对拍/
  重签/open -g 拉起/ticker 心跳双验);WKWebView+Caches 清理在换装时一并做。
