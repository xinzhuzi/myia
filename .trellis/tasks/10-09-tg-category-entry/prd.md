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

- [ ] AC6 **Telegram 归一大分类**:三个插件品类文件(telegram-groups/channels/web.yaml)统一 `id: telegram`、`name: Telegram 监控`(文件仍各自持源,L1/品类层只出一条);存量数据回填(telegram-groups/channels/web → telegram);盖戳映射随 config.id 自动归一;前端 `startsWith("telegram")` 判定与文案随动;设置·源管理的三文件展示如实(文件名区分)。
- [x] AC7 监控台上到**品类渠道页顶部**(用户实际点击落点):未登录=扫码登录钮(browser.open 单入口);已登录=●监控中+账号+管理跳转;【看全部历史消息】直达历史态。
- [x] AC8 历史态:绕过当日窗看该品类全部入库条目,知会词「含历史 · 不限当日窗」;TG 品类空态改「监控在线,窗内暂无新消息」,不再甩「先跑一轮采集」死胡同。
- [ ] AC9 测试修复:当日窗 03:00 翻面暴露的时间炸弹(硬编码日期夹具出窗致一批墙层用例齐红)全部改相对刻度;监控台/折叠用例齐;门禁全绿。
- [ ] AC10 打包覆盖安装 + 换装双实锤 + app 还原常驻;入库 pathspec 提交。

### 在途交接(工作流起点)

工作树未提交改动 = 品类盖戳(entry.py _telegram_source_categories/_store_item + 存量已回填 telegram-groups)、监控台/历史态(feed-screen.tsx drill.history + L2 控制台 + TG 空态)、测试(盖戳 3 例 + 折叠/状态条/监控台用例)。已知红:4+ 用例(监控台两例种子/断言待调、审计批 F5/F5补充 疑似仍有时间炸弹或墙层回归待诊)。

## v3 追加(2026-10-09 凌晨,主人令「自己判断结果是否正常合理,是否加载了内置浏览器界面,展示 tg 内容」)

- [ ] AC11 **内置浏览器预览**:监控台提供应用内浏览器界面展示 TG 内容——取最新条目 url 推导频道公开镜像 `t.me/s/<频道名>`,以 Tauri WebviewWindow 应用内窗口打开(免二次登录;数据入库仍由后台 watcher 登录会话负责,职责分离如实标注);私有频道/预览不可达 = 窗内给出说明不装死。验收 = 单测(推导/开窗调用)+ 验收员动线 + 主人点亮终验。
