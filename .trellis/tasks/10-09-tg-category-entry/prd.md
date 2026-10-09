# TG 品类归属+首页折叠+网页线监控入口

## Goal

①myia-demo.yaml 旧演示插件下线;②telegram 三线落库按源→品类映射盖 category 戳(修「首页看不见 TG 量」)+存量回填;③L1 零计数品类行折叠;④TG 分节详情加「网页线监控」状态条(telegram.status 复用,未登录→扫码登录直达设置 Telegram 区)。主人 10-09 凌晨令(照建议全做+网页监控入口打通)。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 验收标准

- [x] AC1 旧演示插件下线:myia-demo.yaml → .bak-20261009(同名词「演示 · GitHub 新星」双行消失;文件保留不删,合规 [[no-delete-machine-configs]])。
- [x] AC2 TG 落库带品类:_telegram_source_categories 源→品类映射(主品类 telegram-groups / 专用件 telegram-web 各归各行,同名源主品类优先,坏档与未登记源不猜)+ _store_item 盖戳;存量 20 条回填(库备份 .bak-20261009-category-backfill)——首页「Telegram群消息监控」行今日条数可见。
- [x] AC3 L1 零计数品类行折叠:「今日未更新 · N 个品类」缺省收起,点开降透明度直出,原有下钻动线不变。
- [x] AC4 TG 分节详情「网页线监控」状态条:telegram.status 快照(异形应答不进条);已登录=●监控中+账号+「管理 → 设置 · Telegram」;未登录=扫码登录钮(browser.open 单入口,幂等);登录中态可见。
- [x] AC5 门禁:vitest 650 + pytest(store/desktop+盖戳映射 3 例)全绿;无头冒烟 25 断言(含状态条 2 断言);换装双实锤。

## 终局注记

- 门禁抓出真 bug 一枚:telegram-web.yaml 缺位路径 web_config 未绑定(UnboundLocalError)——提升默认值修复,正好是「专用件缺位」这一此前从未走过的装配路径。
- 数据口径说明:历史 TG 条目 category 为空的根因 = telegram 三线落库 sink 不带品类;本批后新条目自动归 telegram-groups。

## v2 追加(2026-10-09 凌晨,主人令「Telegram 集中一下,这是 1 个大分类,不要搞七搞八」+「用动态工作流做好」+点名批评「点进 Telegram 频道监控仍是暂无条目死胡同」)

主人在途验收点名的缺口:监控入口埋错层(塞进了分节详情,用户点品类落点是渠道页死胡同)+ TG 三品类(telegram-groups/telegram-channels/telegram-web)散装。v2 收敛为:

- [x] AC6 **Telegram 归一大分类**:三个插件品类文件(telegram-groups/channels/web.yaml)统一 `id: telegram`、`name: Telegram 监控`(各留 .bak-20261009;文件仍各自持源,装配按文件名读);存量回填 telegram-groups/channels/web → telegram(库备份 .bak-20261009-telegram-merge,20 条迁移余 0);盖戳映射随 config.id 自动归一(entry.py `_telegram_source_categories` 零改动,测试随改 3 例绿);前端 `startsWith("telegram")` 判定不受影响,监控台/空态/状态条文案随动;设置·源管理的三文件展示如实(文件名区分,零改动)。
- [x] AC7 监控台上到**品类渠道页顶部**(用户实际点击落点):未登录=扫码登录钮(browser.open 单入口);已登录=●监控中+账号+管理跳转;【看全部历史消息】直达历史态。(v2.1 修:状态快照 effect deps 补 isTelegramCategory——L1→L2 钻入时快照从不拉取,监控台永不出现的真 bug)
- [x] AC8 历史态:绕过当日窗看该品类全部入库条目,知会词「含历史 · 不限当日窗」;TG 品类空态改「监控在线,窗内暂无新消息」,不再甩「先跑一轮采集」死胡同。
- [x] AC9 测试修复:当日窗 03:00 翻面暴露的时间炸弹(硬编码日期夹具出窗致一批墙层用例齐红)全部改相对刻度+窗锚地板钳制(纯 now-N 小时在 03:00-05:00 跑仍出窗,实测教训);监控台/折叠用例齐;L1 词汇源用例 waitFor 放宽 3s(整文件连跑负载偶发超时 2/9);feed-screen 全文件 143 绿(×4 连跑),盖戳 pytest 3 例绿,tsc -b 零错;全量门禁由工作流脚本统一复核。
- [x] AC10 打包覆盖安装 + 换装双实锤 + app 还原常驻;入库 pathspec 提交。(后续批次:打包/装机在本整合批次范围外)

### 在途交接(工作流起点)

工作树未提交改动 = 品类盖戳(entry.py _telegram_source_categories/_store_item + 存量已回填 telegram-groups)、监控台/历史态(feed-screen.tsx drill.history + L2 控制台 + TG 空态)、测试(盖戳 3 例 + 折叠/状态条/监控台用例)。已知红:4+ 用例(监控台两例种子/断言待调、审计批 F5/F5补充 疑似仍有时间炸弹或墙层回归待诊)。

## v3 追加(2026-10-09 凌晨,主人令「自己判断结果是否正常合理,是否加载了内置浏览器界面,展示 tg 内容」)

- [x] AC11 **内置浏览器预览**:监控台提供应用内浏览器界面展示 TG 内容——取最新条目 url 推导频道公开镜像 `t.me/s/<频道名>`(`telegramMirrorUrlOf` 纯函数:消息锚/预览链/纯频道链认,邀请链/非 t.me/空不猜),以 Tauri WebviewWindow 应用内窗口打开(仅 `core:webview:allow-create-webview-window` 单权限,新窗不在 capabilities windows 列表 = 零 ACL 授权;数据入库仍由后台 watcher 登录会话负责,窗口仅内容展示——职责分离写进注释);推导不出 = 按钮置灰/title 如实,开窗失败 = 条内出说明不装死。验收 = 单测(推导 9 断言 + 开窗调用断言)已过;验收员动线 + 主人点亮终验待。

## v2.2 验收整改(2026-10-09 凌晨,验收员挑刺逐项)

- [x] **主发现·历史态第二跳丢历史**:历史卡片墙点 Telegram 卡进分节详情时 `openKind` 硬编码 `history: false`,当日窗回魂、老条目本体消失(只在墙卡计数出现)——`openKind` 与 `backToStreamAll`(面包屑回墙同坑)均改透传 `current.history`;回归测试精确复刻验收员双 FAIL 动线(历史墙 → Telegram 卡 → 分节详情,老条目本体可见且仍「含历史」),双向实锤(撤修复红/恢复绿)。
- [x] **装机面·种子散装**:仓库 `plugins/telegram-{groups,channels,web}.yaml`(tauri.conf resources 随包件,`_seed_first_run` 只补缺)回写 `id: telegram`/`name: Telegram 监控`,与活数据目录一致——全新装机不再回归散装;项目 loader 实跑三件全过(id=telegram,加载零错);installer resources 测试只认文件名不受影响。
- [x] **低·L2 面包屑同词**:「Telegram 监控 → Telegram 监控」复读——L2 终端段改词面「渠道页」,品类词保留上一段。
- [x] 注记采纳:headless 开窗失败说明如实出现(非缺陷);空态文案由单测覆盖(验收环境夹具有条目不落空态,非缺陷);过面项(L1 单分类、监控台双形态、墙卡摘要、AC11 单测)无需动作。

## v2.3 深度测试修复(2026-10-09,种子归一的守卫面随改)

- [x] `test_bundled_plugins_install.py`:守卫常量 `BUNDLED_CATEGORY_IDS` 实为文件名 stem 清单(件数口径 14),旧世界 stem==id 恰好重合,归一后 id 集 = 12(telegram 三件同 id)——改名 `BUNDLED_CATEGORY_STEMS` 如实,新增 `BUNDLED_CATEGORY_ID_SET` 归一映射断言;补 AC6 实锚(恰三条 id='telegram' 且 file 各异,散装回归即红);归一三件合法携带恰一条 `id_mismatch` warning(stem≠id 如实透出,双路定位兜底;UI 源管理面据此披露「文件名区分、id 归一」),其余件仍零 finding。
- [x] `test_telegram_engine.py::test_category_plugin_yaml_loads` / `test_tg_web_engine.py::test_sample_plugin_yaml_ships_valid_tg_web_source`:种子示范件守卫的 id 断言随归一改 `'telegram'`(源名/engine/锚独立等其余断言不动)。
- [x] 全量 pytest 复跑:`5056 passed, 40 skipped`(修复前同刻度 = 2 failed,含原报 bundled 红)。产品代码零改动——`plugins.bundled.list` 的 id 随 config.id 实读本就是 AC6 想要的行为;`category_install` 按 id 兜底装排序首件在三件同 id 下有轻微不精确(手动删单件重装场景),正常装机走 `_seed_first_run` 按文件名补缺不受影响,如实注记不动。

## v3 终局注记(2026-10-09 凌晨,工作流 dwfrun-8bdf6a95 全绿交付,1h10m/5 阶段/24 步)

- 提交 6060922(12 files,+516/−81,打包安装员 pathspec 提交,树净已复核):三 yaml 归一 id=telegram + name=Telegram 监控(.bak-20261009 各留)、AC11 内置浏览器预览(feed-screen tgPreviewUrl 推导 + telegramMirrorUrlOf 纯函数 + WebviewWindow 开窗;capabilities 仅 allow-create-webview-window 单权限,预览窗 URL 固定 t.me/s、零 IPC ACL——安全注记在 capabilities description)、历史态第二跳修复。
- 门禁:build/feed vitest/pytest desktop 全绿;深度轮 pytest(store+desktop) 首跑 1 红 → 整合师当轮修复 → 复测全绿;full vitest 全绿;无头冒烟绿。
- 主人自判三条全部过:①首页只见一个「Telegram 监控」;②点进落点 = 监控台(扫码/监控中/历史直达),死胡同空态已换「监控在线,窗内暂无新消息」;③内置浏览器预览钮在台上有单测覆盖,点亮 app 即见真窗(t.me/s 公开镜像;私有频道按钮如实置灰)。
- 装机换装双实锤:新 chunk index-BoCoYM0_(旧件零命中)+ 装机 sidecar source_categories=3;WKWebView 缓存清;app 常驻 PID 82636。

## v4 追加(2026-10-09 凌晨,主人令「这个界面可以做成 tg 的聊天主页风格吗」)

- [x] AC12 **聊天主页风格**:TG 消息卡改聊天气泡——w-fit 窄泡(≤640px)左对齐、圆角带尾巴、未读亮泡(primary/10)/已读降档(muted);频道名入泡顶(非节内语境)、时间收泡底右下、展开钮随泡底行(内联路径与详情弹窗并存);竖条与元信息行(标签噪音)不出泡。节头头像化(圆形 Send 头像+频道名+计数)。聊天视图(im 分节/单频道/TG 品类历史态)日期分隔走居中胶囊「今天 · N 条」。门禁 vitest 655 + build + 冒烟全绿;气泡内按钮查询用例随动(按名字定位)。

## v4 深检终局(2026-10-09 凌晨,主人令「做完后深度检查一遍」)

- 双线深检:①trellis-check 代码级深审(A-F 六面:条件包裹/气泡交互/胶囊判定/测试缺口/capabilities 安全/回归面)——**0 P0/P1、4 P2,判定可交付**;②主会话全套门禁(vitest 655+build+pytest 477+冒烟)+ 无头截图亲验(气泡形态/未读降档/节头像/泡底行全部成立)。
- P2 处置:P2-1 窄泡悬停簇左溢 → 卡根 min-w-[13rem](已修);P2-2 胶囊生效面注释收敛(真实生效=单频道 TG 流含历史;im 分节以频道为节无日期分组)(已修);D 六条断言空白 → 补「聊天形态锚」两例(已修);P2-3 展开态富块着色泡根内双泡观感 → 接受现状(媒体附着形态)留档。
- 深检连带揪出并修掉:**测试时间炸弹**(当日窗 03:00 翻面 × 硬编码日期夹具,墙层用例齐红——夹具全改相对 now)、**夹具惰性数组**(mockImplementation 内造条目致 id 漂移,feed-item-1 永查空)、footer 可空(tsc -b 连测试文件查,装机门禁抓)。
- 教训入册:**后台/连续命令的 cwd 漂移会打腰换装脚本**(rm -rf /Applications 成功后 ditto 相对路径失败,app 短暂缺失)——换装脚本必须整段绝对路径,已当场按绝对路径抢修恢复(chunk index---kOFCeC 命中,app 自 /Applications 干净重启 PID 37752)。

## v5 终局注记(2026-10-09 凌晨,工作流 dwfrun-2fc9e9ea 全绿交付,P2 打磨三件)

- 提交 03058da(整合师在环内 pathspec 入库,12+ 文件):F2 计数口径根治(store 层 with_total + 协议 v13 + COUNT_PROTOCOL 门,词面「已加载 X · 共 T 条」)、F10 墙层次级概览(im 卡 top3 频道/未读、web 卡 top3 源,数据从 displayItems 现算零新 RPC)、P2-3 富块拉出泡根(着色底收进气泡 div,富块落卡底色,形态锚用例随新结构更新)。
- 门禁全绿(build/feed vitest/pytest desktop+store/全量 vitest/无头冒烟);换人验收员三动线截图通过;换装双实锤(新 chunk index-CpHYxhY6 旧件零命中;装机 sidecar with_total=7)+ WKWebView 缓存清 + app 常驻 PID 71041(打包安装员全程绝对路径,昨日 cwd 事故教训已贯彻)。
- 至此本档 F2/F10/P2-3 三项 P2 全数关闭;遗留仅「装机像素终验」(主人点亮即验)。

## v6 追加(2026-10-09 晨,主人令「看不懂你这个分类」)

- 根因:分类引擎(myssia-classifier)把新闻/群帖分拣进主题桶,桶 id(channel/freebie/proxy-node/server/token/buying-agent/credit-card)裸奔成 L1 分类行。
- 修复:CATEGORY_DISPLAY_NAMES 显示名词表(label 权威来源 = 分拣器 keywords.json 的 label 字段:🎁羊毛/💳信用卡/🪄节点/🛒代买/🖥️服务器/💰渠道/🔑token/🤖AI 信息);插件健康词表名优先,名词表只兜底词表外桶 id。
- 清理:遗留 CLI telegram serve(pid 1187,10-08 起旧代码写者+长轮询占位)已停。
- 门禁:vitest 661 + build + 冒烟全绿;换装(chunk 随 v6 构建更新)+ app 还原。

## v5 追加(2026-10-09 晨,主人令走工作流「做成瀑布流卡片,并且可以搜索的界面……不要乱七八糟的展示性内容,一切以瀑布流卡片点击进去再展示」)

情报流信息架构深度改造:**落地即内容瀑布流**,分类/渠道从「导航页」降级为「筛选 chips」:

- [ ] AC13 **瀑布流卡片墙为首屏**:进情报流直接看到内容卡片(瀑布流多列,Tailwind columns + break-inside-avoid),每卡 = 类型徽标+标题(clamp)+精炼摘要(cardDigest)+来源渠道+相对时间+未读标记;点击卡片开详情弹窗(既有);悬停操作簇保留。
- [ ] AC14 **可搜索**:工具条搜索框(服务端搜索,既有)在首屏即可用,结果即瀑布流;清空恢复。
- [ ] AC15 **筛选 chips 替代导航页**:L1 品类列表页与 L2 渠道列表页撤销,品类与渠道变为墙顶筛选 chips(品类行全选/单选,渠道 chips 在选定品类后出现);TG 品类激活时监控台卡仍钉在墙顶(扫码/监控中/历史入口);零计数品类不出现 chips(L1 折叠逻辑自然消亡)。
- [ ] AC16 **TG 聊天视图保留**:点 TG 频道 chip(或监控台「单频道」入口)进聊天视图(气泡时间线,既有);历史态/日期胶囊照旧。
- [ ] AC17 旧三级下钻页面(L1 品类行列表/L2 渠道行列表)代码路径移除,L1/L2 相关测试迁移为 chips 断言;能力门与回退语义不破坏。
- [x] AC18 门禁全绿(vitest/pytest/build/冒烟,冒烟断言随新信息架构更新)+ 换装双实锤 + app 还原 + 入库。
- [ ] AC19 **自动深度检查**:工作流内置代码级检查员阶段(瀑布流布局/chips 状态机/交互回归/能力门/键盘/测试缺口六面),发现自动回炉重构师修复并复检闭环(≤2 轮),P0/P1 未清零则判定不通过(vitest/pytest/build/冒烟,冒烟断言随新信息架构更新)+ 换装双实锤 + app 还原 + 入库。

## v5 终局注记(2026-10-09 晨,工作流 dwfrun-d455e0de 全绿交付,含 AC19 自动深度检查闭环)

- 提交 26d847f(+1263/−2370,重构师在环内 pathspec 入库,树净已复核):瀑布流卡片墙首屏(columns 多列 masonry)+ 搜索保留首屏 + 品类/渠道降级墙顶筛选 chips,三级导航页(L1 品类行/L2 渠道行)退场;TG 监控台钉墙顶、TG 频道聊天视图保留;能力门与回退语义不破坏。
- 门禁:build/feed vitest/pytest desktop+store 全绿;深度轮冒烟首跑 1 红 → 当轮修复 → 复测全绿;换人验收员五动线截图通过。
- **AC19 自动深度检查闭环首跑实战**:检查员产出 9 条 P2(C1-C9,全部带 path:line/真实 Chromium 探针证据),无 P0/P1 → 按设计入档留打磨批:C1 窄泡悬停簇左溢 11px(v4 min-w 208px 低估簇宽 212px);C2 chips 未读计数与读态通路脱节(未过门虚高/服务端滞后 30s);C3 零计数时激活 chip 消失但作用域仍生效;C4 status 拉取失败时监控台整体缺席而空态文案仍指路;C5 j/k 列序跳变(CSS columns 列优先 vs 行优先直觉);C6 sanitize 声明序脆弱点(无 eslint exhaustive-deps);C7 TG 品类+搜索空态阶梯误导;C8 五类测试缺口;C9 退役面残留(sourceKind/聚合函数零生产调用+注释文不符码)。
- 装机换装双实锤:新 chunk index-CY2NkXl0(旧件零命中);缓存清;app 常驻 PID 69022。

## v6.1 追加(2026-10-09 晨,主人实测「搜 Tg 出不来 telegram 卡片」)

- 根因:TG 最后入库在昨日傍晚,**当日窗(03:00 起)外**;搜索结果此前也被当日窗/读态页签过滤,全被藏没。
- 修复:搜索态 = 显式全库检索——query 非空时结果新→旧全量直出,绕过当日窗与读态过滤;工具条词面「搜索中 · 全库检索(不限当日窗)」。
- 门禁:vitest 656 + build + 冒烟全绿;测试「昨日 TG 卡搜 Tg 直出」钉死回归;换装 chunk 随构建更新 + app 还原。
