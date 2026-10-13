# 界面文案全面审计:词不达意清查与统一修正

## Goal

主人令(2026-10-12):「关键词粗筛,就写成关键词粗筛的英文单词,这个词不达意的问题你犯了好多次了,全部过一遍,确定哪些词不达意,要修改」。全屏文案审计(生造词/行话/中英混杂/名实不符/同物多名),产出改词表,统一修正+测试同步+门禁+打包换装。旗舰嫌疑:粗筛/精筛/精评一族

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 结果(交付回执,2026-10-12/13)

- **工作流 dwfrun-e4038766**:7 审计员并行盘点(95 条发现)→ 汇总员定改词表(46 项改/含旗舰族)→ 独立复审员对抗性复审 → 4 改词员按文件分片应用(8 笔提交,回炉多轮)→ 门禁(构建+全量前端测试)→ 打包换装(备份 /tmp/myssia-wording-backup-*)→ 冒烟全 PASS。
- **旗舰定稿**:「粗筛/精筛」→「消息过滤」;「精评/AI 摘要/LLM 精评」→「AI 评分」(三生造词两概念+与 UI 卡名对不上,全 App 一词);字段名 score/model/API Key/base_url 保留标准英文。
- **功能性修复(审计意外收获)**:10 处「设置→推送」指引指向已不存在的入口(推送分区已抽到 配置→机器人凭据)——全部改指新入口。
- **主会话地面核验(收官纪律)**:8 笔提交在库;亲跑构建绿 + vitest 780/780;装机件内嵌文案「AI 评分/首次运行/部分成功」在、「LLM 精评/B 派通道」零残留;全库高危词抽查——用户可见面清零,残留 18 处全为代码注释(审计范围外,合规)。
- **如实说明**:工作流报「41 文件跳过(并行在途)」——终态核验可见面零残留,该计数系改词员多轮重复计入/测试与注释文件也计入 skip,以终态为准。
- **未覆盖(建议另档)**:后端 Python 错误文案(ErrorBox 显示面,动 pytest 面);实机 yaml 注释;README。审计报告 artifact 存全量逐处 old→new(46 项)与保留判定,主人可逐项翻案。
