# 建议执行批:TG归档自动化+百度源关键词+后端错误文案审计

## Goal

主人令(/workflow 按建议都做完):①TG 手游源码群自动取消归档(Playwright UI 自动化,先退 app 释放配置档,完成复原);②百度网盘源配关键词(百度/网盘/pan.baidu.com/短剧等,yaml.save 实机+仓库种子同步);③后端 Python 错误文案审计(前端文案审计姊妹篇:entry.py+引擎+管线错误消息,衔接已定词表 粗筛→消息过滤/精评→AI 评分 等,pytest 同步+全量门禁+打包换装)

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 结果(交付回执,2026-10-13)

- **工作流 dwfrun-b666b03d(限额中断)→dwfrun-55b8266c(Amend 升级含拷问,已完成步骤缓存导入)**:三关 Grill 拷问(拷问官先读 grilling/grill-me 技能)——①配套动作 12 质疑全解;②改词表打回修正后收口;③落地 diff 放行(带 4 项低危记录)。
- **TG 手游群**:实测已在主列表(targetInMain=True,归档列表空,截图 /tmp/tg-unarchive-proof.png);app 复原;重启后 watcher 无新告警。
- **百度源关键词**:yaml.save 校验+.bak+读回复核;仓库种子 cmp 逐字节一致+试载过(提交 d657be9)。
- **后端错误文案**:125 处改(英文报错族整族中文化/写回→保存/零写入→文件未做任何改动/拉起→打开/job→定时任务/裸方法名与裸异常类名撤下屏);pytest 5487 绿+vitest 780 绿。
- **主会话地面核验纠偏(收官纪律抓到拷问③失手)**:同族 9 条变体消息(锚点/push 节形态等)漏改,亲手补修统一「无法保存:…;文件未做任何改动」句式(提交在案),ruff+桌面协议 405 绿+全量 pytest 5487 绿,重打包换装(strict verify+冒烟全 PASS+包内抽验 12 处新句式在)。
- **留案**:①CLI argparse help 残留「粗筛/LLM 精评」(cli.py:473/2745/2770)——下次 CLI 文案档收口;②两处测试断言轻度弱化+jobs.py 按钮名「立即运行」vs GUI「运行」不齐(低危);③安全观察:TG 页面有陌生设备登录横幅(Tokyo, Redmi K80 Pro),请主人确认是否己方设备/代理出口。
- **主人侧待办(不可代做)**:LLM API Key 录入/飞书重定向 URL 登记/打开位置目验/review 档裁决。
