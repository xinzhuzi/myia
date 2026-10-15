# 微信 Mac 保证级发送:发送链路 LLDB 直调通道

## Goal

已批红线裁决(10-14 主人令,10-14 晚按实证修正):**旧前提作废**(归档「SendMsgFtouser 主流程」系 NewSync 误标、ObjC selector 路无 send 族)。现行目标:按 design.md「运行时明文猎捕协议」定位 (用户,内容) 明文 API → 推导调用签名 → LLDB attach 直调零 UI 发送 → 白名单双发验证(文件传输助手+jiangliushi666,嘻嘻,≤2 条)→ 固化为桥的保证级通道,与 OCR 链(0.8.4 主力)分级并存。

## Requirements

- 从 corrected-path 架构(UI 逻辑层→协程任务系统 task_service→mars::stn 传输)定位 (用户,内容) 明文入口——**执行协议=design.md「运行时明文猎捕协议」;历史错误全谱系=research/错题集.md;已证死路=design.md 死路表**(2026-10-14 晚交接态)
- LLDB 直调零 UI 发送,白名单双发验证,固化为桥保证级通道与 OCR 链分级并存
- 纪律继承:任何轮次 detach 干净微信零伤;uncertain-never-retry;连续 3 次同域失败停手升维(错题集 D2)
- 红线裁决(10-14 晚主人批「都按推荐落实」):**发送预算总帽 10**(勘察已耗 6+1,余 3 每条先报后发);**猎捕触发=主人手发**(标准形态,流程=主人说「发」→3s 窗口使能→主人发送);**Phase 0 离线整备随时开工,Phase 1 等主人手发窗口**,不抢并行会话微信时段〔10-15 凌晨簿记括注:「余 3」为 r1 前旧值——阶段 3 动态轮桥发 3 条在案,账本 9~10/10 余 0~1,P-2 需 2→P-0 裁决门先行(design-阶段3.md §4)〕〔10-15 归档补笔:P-0 已裁 (c)——主人令原文「C,自动化情况下,可以发无数条信息的」(design-阶段3.md §4 P-0 裁决块 :405-409):自动化发送总量不限,G6 节奏护栏(单条/≥10s,防封)保留;本行「总帽 10」预算帽据此作废,终局出站总账=勘察 6+动态轮 3+终轮触发 2=11 条(r1 零出站已耗授权另计 1)〕〔10-15 晚勘正(主会话亲跑复核):11 为流程账——微信本地 DB 同窗出站(local_type=1)实测 **28 条**(sqlite3 message_0.db / Msg_9e20f478…/ create_time≥1791952800,行数链 62→73→75→82 对账闭合);差额 17=r4 钉入轮 6+cap5 1+§2.8-§2.11 研究轮触发 7+10-14 20:58 无主行 1+勘察窗「6+1」口径与 DB 差 1;(c) 裁决下无越权,纯记载勘正〕

## Acceptance Criteria

✅ AC1(达成,形态修订):明文消费点定位=F_exec(0x83e394)+msgctx 三槽布局逐字节实证(r4/cap5);全函数反编译在档(research/r4/fexec_decompile.c)
⛔ AC2(未达成,结构性):签名推导完成但直调三形态全阴性(裸调/嵌套调/TLS 追踪;F_exec 含协程挂起点,普通函数调用不成立,§2.9);配方封存(§2.11)
⛔ AC3(未达成,依赖 AC2):直调 0 送达(三轮实证);触发链 15+ 条全落库绿,回执双通道本身验证通过
◐ AC4(半成):基础设施全落地(锚定表/门/错误码/防重/827 测试绿;失败=干净拒绝零误发);配方未通→分级调度暂以 send_text 兜底,实际发送由 OCR 链承担

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.


## 终局裁定(2026-10-15,主人令「review 后归档」)

直调配方线五轮攻坚(r4→r10)后按 D2 纪律封存:知识库(38 帧架构图/三槽布局/三阴性/ TLS 排除)全量入库;OCR 链(全天 15+ 条落库零误发)承担实际发送;send_direct 通道保留(失败=干净拒绝)。重开前置=先验 resume 存储形态(§2.11)。
