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
