# 命令面板缺「定时任务」屏条目(SCREENS 七屏清单漏 cron)

## Goal

全链自测实证(dwf‌run-a25f5cbc 视觉验收):command-palette.tsx:47-55 SCREENS 仅七屏、注释自称路由表七屏,但 App.tsx:38 与 sidebar 均有 cron 屏——⌘K 面板无法导航到定时任务,只能走侧栏。修法=SCREENS 加一行+命令面板测试同步;轻量档 PRD-only。

## Requirements

- R1(条目):SCREENS 在源管理(/sources)后插第八屏 `{ to: "/cron", label: "定时任务", icon: Clock, keywords: "cron schedule timer jobs" }`——to/label/icon 对齐 App.tsx:38 路由与 sidebar.tsx:46;keywords 含任务示例 cron/schedule/timer,纯英文小写贴其余七屏风格(label「定时」本就走中文匹配,无需入 keywords;主体 303f57b 初版误入,529af11 修正补 jobs)。
- R2(注释):command-palette.tsx:36 与 :47「七屏」注释改「八屏」(App.tsx 路由表口径)。
- R3(测试同步):command-palette.test.tsx 全清单断言按渲染序插「定时任务」(源管理后,其余旧断言不动)+ 新增「cron」keywords 过滤例与「定时」→Enter 导航 /cron+关闭例;文件头注释「导航七屏」→「八屏」同改。

## Acceptance Criteria

- [x] SCREENS 补行:command-palette.tsx:52 增 `/cron`「定时任务」(Clock=sidebar.tsx:46 同款;位次=源管理后,与 App.tsx:38/sidebar 一致;keywords「cron schedule timer jobs」;落 303f57b+529af11;2026-10-05 回标复核:实读 :52 终态逐字一致、Clock 静态 import 自 lucide-react(:4),git show 两提交合计仅动 tsx/test/task.json 三文件零越界,git diff HEAD 组件+任务域为空)
- [x] 注释口径::36/:47(及测试文件头)「七屏」→「八屏」——落 303f57b;2026-10-05 回标复核:实读 tsx:36/:47 与测试文件头三处均「八屏」,无「七屏」残留
- [x] 测试同步:command-palette.test.tsx 八屏期望+「定时任务」条目,新增 cron 关键词过滤/Enter 导航 2 例;vitest 单文件 21/21 绿(2026-10-05 实跑;收口会话复跑同绿;回标轮再复跑 `npx vitest run src/components/layout/command-palette.test.tsx` → Test Files 1 passed / Tests 21 passed,实读 :184-204 渲染序插「定时任务」旧断言未动、:220-224 cron 过滤例、:279-285 「定时」Enter→/cron+关闭例)
- [x] 门禁全绿(脚本统一执行,2026-10-05 收尾档确认;2026-10-05 回标轮遵 ask「可跑定向不跑全量」豁免未复跑全量,本轮以定向单文件 21/21 绿为证,task.json status=review 实读)

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
