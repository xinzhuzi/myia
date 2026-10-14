# 微信 Mac 保证级发送:发送链路 LLDB 直调通道

## Goal

已批红线裁决(10-14 主人令,10-14 晚按实证修正):**旧前提作废**(归档「SendMsgFtouser 主流程」系 NewSync 误标、ObjC selector 路无 send 族)。现行目标:按 design.md「运行时明文猎捕协议」定位 (用户,内容) 明文 API → 推导调用签名 → LLDB attach 直调零 UI 发送 → 白名单双发验证(文件传输助手+jiangliushi666,嘻嘻,≤2 条)→ 固化为桥的保证级通道,与 OCR 链(0.8.4 主力)分级并存。

## Requirements

- 从 corrected-path 架构(UI 逻辑层→协程任务系统 task_service→mars::stn 传输)定位 (用户,内容) 明文入口——**执行协议=design.md「运行时明文猎捕协议」;历史错误全谱系=research/错题集.md;已证死路=design.md 死路表**(2026-10-14 晚交接态)
- LLDB 直调零 UI 发送,白名单双发验证,固化为桥保证级通道与 OCR 链分级并存
- 纪律继承:任何轮次 detach 干净微信零伤;uncertain-never-retry;连续 3 次同域失败停手升维(错题集 D2)
- 红线裁决(10-14 晚主人批「都按推荐落实」):**发送预算总帽 10**(勘察已耗 6+1,余 3 每条先报后发);**猎捕触发=主人手发**(标准形态,流程=主人说「发」→3s 窗口使能→主人发送);**Phase 0 离线整备随时开工,Phase 1 等主人手发窗口**,不抢并行会话微信时段

## Acceptance Criteria

- [ ] AC1:明文入口定位(运行时猎捕协议 Step 1-2;产物=入口函数 VA+全函数反编译)
- [ ] AC2:调用签名推导(LLDB 只读方法验证机制通过 + 直调发送一次成功,白名单内,协议见 design.md Step 3)
- [ ] AC3:白名单双发真验证(filehelper+jiangliushi666,嘻嘻,≤2 条,≥10s;**回执双通道**:filehelper=sqlite 直查 decrypted/message_0.db,jl666=桥 localdb query——桥对 filehelper 表名映射有已知缺陷)
- [ ] AC4:桥保证级通道落地+与 OCR 链分级调度+单测绿(打字路径打桩;直调通道同过 G6 频控)

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
