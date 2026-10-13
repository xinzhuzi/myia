# TG web 线铺源:枚举会话清单并批量加源

## Goal

主人令按建议铺源:无头枚举 telegram-alt1(持久配置档)在 web.telegram.org 的会话清单,群/频道逐个写进 telegram-web.yaml(engine tg_web,chat=标题片段),经 yaml.save 校验+留底;跑一轮采集验证新源产出。DM 不采

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 结果(交付回执,2026-10-12)

- 无头枚举:telegram-alt1 会话 5 个,可铺新源 2 个(排除 DM 官方号与已采的 clashv8;Clash-Party 因 bot 线已在采、双线同群会双条入库,在册判例跳过)。
- 铺源经 yaml.save(校验+.bak):telegram-handgame-src(手游源码.技术供需)、telegram-baidu-pan(百度网盘资源分享)落盘。
- 排障实录:批跑全源 logged_out=与 app 常驻 web watcher 抢配置档的假象(重探 logged_in=True 钉死;常驻模式下批跑不需要);重启 app 后 watcher 装载新源——baidu-pan 无告警已接上;handgame 报 dialogs_missing(群在归档/静音区,引擎对话框枚举够不到),留主人在 TG 取消归档即接。
- 意外收获:yaml.save 存量 id 豁免修复(telegram 三文件此前 GUI 永久不可编辑),测试三态。
