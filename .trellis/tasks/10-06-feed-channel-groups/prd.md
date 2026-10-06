# 情报流渠道级分组

## Goal

主人令「情报流也要分渠道呀」:桌面 app 情报流屏在品类分组下再按渠道(源名,规约 telegram-<频道> 等全称)细分——分组展示或筛选器形态按既有 feed 屏风格定;vitest+装机重打包换装像素验证。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

---

## 执行追踪(子代理工作面,主人令「子代理做的事/将做的事落实到档」)

**在途执行**(2026-10-06 派工,后台工程师代理进行中):

| # | 事项 | 状态 |
|---|------|------|
| 1 | 情报流品类下按**渠道分组**(源名全称规约 telegram-<原名> 等) | 在途 |
| 2 | **分型呈现**五种:telegram-* 消息卡(气泡+时间+频道名)/RSS 标题链接列表/urlwatch 官网监控=变更事件徽标/prompt 日报=markdown 文档可折叠/游戏羊毛=价格行 | 在途 |
| 3 | **实时滚动**(当日不停过日志:自动刷新节奏,新条目持续进流;刷新机制按前端既有模式选型,防高频打爆 sidecar) | 在途(主人追加) |
| 4 | **每日 03:00 视图清零**(当日窗 03:00-次日 03:00;只清视图不动 store,retention 照旧;窗口锚缺省 03:00) | 在途(主人追加) |
| 5 | 数据面:走 sidecar 协议既有 items 查询(带 source);不足则最小面扩展 | 在途 |
| 6 | 门禁:vitest 全绿+tsc 0 错 | 待办 |
| 7 | 装机:重打包+换装五步判例+MYIA_SHOW_ON_START=1 亮窗+截屏 local-ocr 验证渠道分组与五型样式可见 | 待办 |
| 8 | AC 补两条:实时刷新可见新条目;跨 03:00 窗口滚动后视图从零 | 待办 |

**关联前置**:telegram 持续监控线(10-06-telegram-telethon,planning)落地后,群消息实时进流=本屏「不停过日志」的信源;本任务先行把窗口与分型做好等流进来。
