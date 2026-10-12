# TG频道消息评论(讨论线程)采集

## Goal

主人令(2026-10-12):群消息里还有 > 再进一步的信息(comments/讨论线程),如何获取——先详细探索再执行。V1 目标:tg_web 批量档在读频道窗口时,对带评论的帖子展开线程读回复进管线(锚命名空间=讨论群 chat id,与频道帖独立)。探索先行:clashv8 帖子是否带评论钮/线程 DOM 形态/导航与返回机制,活标定后才动手。

## Requirements

- TBD

## Acceptance Criteria

- [x] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 终局回执(2026-10-12 午后,主会话收口)

- 探索(工作流 dwfrun-fed6d55d,活页实测):clashv8 帖带评论(1128/697 条);评论钮=replies-footer;讨论群 @xoxo8866(peer -4373866046)锚独立;锚必 (data-peer-id,data-mid) 成对;导航真点+close-button 返回;定级 v1-batch。
- 方案:两轮评审否决(预算账漏 LLM 过滤段)→修正案(预算动态推导≤80+过滤储备 60+5s)过审;限流中断一次后续跑;实现段因 provider 故障死于汇报前,产物完整(主会话验收)。
- 实现:web_thread.py+引擎评论档+schema/CLI/配置面;门禁 pytest 5347/0+vitest 762/762+build+ruff 全绿。
- 真跑回执:clashv8 64 采集/45 入库(纯频道 19→+44 条评论锚 #tg--4373866046-* 独立命名空间;本轮评论全为「订阅」占楼短消息,带链接评论出现时链接化渲染自动生效);降级守卫实证(弃2帖保基线)。
- 装机:5 py 件+config 外科换装+重签 strict;装机态真跑 success(app 内 web 线 5 进程常驻)。
- **配置事故与恢复(如实记)**:主会话误以仓库版覆盖数据根生产件(仓库版仅旧 mihomo 源,clashv8 只在数据根)——按 10-11 v3 实测形态重建(clashv8 上位带评论档+mihomo 注释回切),装载验证+装机态生产跑 success;教训=外科同步配置先 diff 数据根与仓库,数据根是生产真相源。
