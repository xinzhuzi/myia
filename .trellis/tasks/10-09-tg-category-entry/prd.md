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
- [ ] AC10 打包覆盖安装 + 换装双实锤 + app 还原常驻;入库 pathspec 提交。(后续批次:打包/装机在本整合批次范围外)

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
