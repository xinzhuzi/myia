# 错题集:微信自动化会话失败路径(主人令 2026-10-13 固化)

> 来源:会话 #微信自动化(sess_d73e1a43)。该会话是微信桥双轨制(pixel/localdb)与 AX/iLink 排错的诞生地。
> 每条 = 【尝试】→【失败实况】→【根因】→【守则】。供后续微信线一切任务引用;同类坑不再二踩。

## 一、方向层错题

### M1. 需求约束漂移未钉死就开工
- 【尝试】约束从「不封号不破解」→「要 UI 自动化」→ 双线并行(macOS AX 先行+Windows wxauto 备胎)→ UI 读+官方 iLink 写。
- 【失败实况】每翻一次方向,前面的排错资产作废一批。
- 【守则】微信线开工前先钉「读还是写、本人身份还是 bot 身份、UI 还是数据面」三问;翻方向必须显式宣告并盘点资产存活面。

### M2. 调研浅查下负向结论
- 【尝试】单查 "wechat" 关键词搜生态。
- 【失败实况】漏掉整个 MCP server 生态,负向结论被主人纠偏;按 find-skills 方法论多查询形状(10+ 形态)深查后补获 BiboyQG 275★ 等。
- 【守则】负向结论须 ≥3 种搜索形状(仓搜/代码搜/平台 API)才许落档;单形状零命中=没查,不是不存在。

## 二、macOS AX 死路(方向性错题,勿再入场)

### M3. AX 自动化对微信 4.x 判死
- 【尝试】osascript/AX API 读微信 UI 树做自动化。
- 【失败实况】`osascript` 报「无效的索引 (-1719)」、AX 零窗口暴露;定因=微信 4.x 是 Chromium 多进程架构(WeChatAppEx+Renderer helpers),AX 树默认关闭。**4.1.15 输入框/AX 零暴露,本人身份 UI 自动发送定论做不了。**
- 【守则】macOS 微信 4.x 的一切 AX 路线(读控件/写输入框)不再入场;UI 面只剩像素链(只读、当前打开会话)。

### M4. CGWindowList 零窗口误判权限
- 【尝试】窗口数=0 → 怀疑屏幕录制权限问题。
- 【失败实况】实为主窗口未开(微信在托盘后台),非权限问题。
- 【守则】窗口零命中先分诊「进程在不在/主窗开没开/权限有没有」三层,别跳层归因。

## 三、读通道语义错题

### M5. 结构化 skip 误读为引擎失败
- 【尝试】像素链真拉 0 条 → 二轮零新增。
- 【失败实况】成因是 `skip_reason=chat_title_unreadable`(微信没开声明会话的聊天窗)= 合法结构化 skip;二轮零新增的账要记在 skip 头上,不是 dedep/引擎。
- 【守则】产出为零时先看 skip_reason 分布再谈缺陷;skip≠fail,验收口径分开记。

### M6. 会话寻址裸 id 与显示名割裂
- 【实况(本任务 10-13 延伸)】localdb query 按显示名查零命中:sessions 列表只回裸 id(如 50438708676@chatroom),显示名在 contact 库。
- 【守则】会话寻址统一先经 contact/contact.db 解析显示名→username 再查消息;显示名直查是二等公民。

## 四、官方侧(iLink)不可抗错题

### M7. iLink bot 读群三重死
- 【尝试】QR 登录 @im.bot 想拉群消息。
- 【失败实况】①`@im.bot` 身份拉不进普通微信群(腾讯不给);②即使进群,iLink 不投递普通群消息事件;③个人客户端无「读群 API」概念。
- 【守则】读普通微信群永远不走官方 bot 线;官方通道(Hermes 桥 src/myssia/push/weixin.py,ClawBot 合规位)只做写出站。

## 五、工程层错题(可泛化)

### M8. 频控状态放内存,桥是一次性子进程
- 【失败实况】桥进程退出→内存频控丢→频控形同虚设。
- 【守则】一次性子进程的跨次状态必须落盘(send_state.json+flock 是正解);间隔不足拒发并回剩余秒数。

### M9. AC 互斥未提前对撞
- 【实况】「发送必须持焦」vs「不抢焦点」静默铁律互斥,做到一半才暴露,降级案提裁决。
- 【守则】PRD 阶段把 AC 两两对撞一遍,互斥项开工前裁决,不带病进 implement。

### M10. weixin.yaml 两层 enabled 陷阱
- 【失败实况】74 行 `enabled: false` 是 enrich LLM 红线开关,不是品类开关;品类真开启=cron job 注册(*/30 微信监控 job);schema extra=forbid 无品类顶层 enabled。
- 【守则】改 weixin.yaml 前先重读该档注释;同名键多层语义必须看行号定归属。

### M11. errored workflow 不可 resume
- 【实况】换 key 后 `workflow_run_not_resumable`。
- 【守则】errored 工作流复活法=脚本顶部加注释造字节差+AmendWorkflow。

### M12. 文档 Edit 锚点事故连环
- 【实况】Edit 锚点不匹配/「File modified since read」多次;design.md §6 插入顶掉 §5.3 bullets;中文逗号形态不一致致替换失败。
- 【守则】Edit 前重读目标段;插入点用唯一定界符;改完 rg 复核邻段完整性。

### M13. cd 后 cwd 漂移致 git pathspec 失效
- 【实况】git exit 128,cd 进任务目录后 pathspec 不匹配。
- 【守则】长会话中 git/任务脚本一律绝对路径或先回仓库根。

### M14. flaky 测试误归因
- 【实况】`pytest -q --lf` 一次 9 passed 被归因 flaky,非真实回归。
- 【守则】--lf 通过≠全绿;收尾门禁跑全量。

## 六、与本文档互指

- 密钥线错题(九路排除史):`.trellis/tasks/10-13-wechat-key-crack/research/crack-roadmap.md`
- 本任务(取钥外置化):`../prd.md` `../design.md`
- 10-13 战报:LLDB 路已破 4.1.15(20/20 全库验真),见攻坚档终局节。
