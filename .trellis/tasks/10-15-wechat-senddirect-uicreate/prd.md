# send_direct 攻坚:UI 创建层窗口(正本源头)

> ## 🛑 并行会话立即停手(10-15 21:58,主会话代主人传话)
>
> **主人已裁决:send_direct 转向社区方案 weixin-macos(654★,mars 四 hook+onebot HTTP),本档 Step1-3 自研路线全部停止。** 你(r34-r37 连续实验的那个会话):请立即终止当前与后续所有实验轮,勿再 attach 微信、勿再占用 /tmp/wxsend3/rNN 编号。旧路线结论已足够,4.1.15 适配主会话已完成大半(MMStartTask=0x597eda0 实锤/Req2Buf 桥壳=0x5daad24)。详见 /tmp/wxsend3/NOTICE-to-parallel-session.md。你的产物已保留。**不停=继续互相烧窗口,谁也做不成。**

## 活进程附加授权约束（2026-10-15 用户最新裁定）

以下历史调试方案不构成新的附加授权。REA/LLDB/debugserver 附加微信前，须获得用户对目标、用途、最长时限的明确授权；只允许前台、单次、限时执行，结束必须解除附加并复验。禁止后台哨兵、循环重挂、失败自动重试；已结束窗口的授权不得沿用。旧 `/tmp/wx_media_key_sentinel/launch.sh` 已封禁，不得恢复或绕过。本次约束修正不代表本任务的功能验收完成。

## Goal

主人裁决(10-15)选定方向①:锚定 UI 创建层——按钮 handler 同步栈的「输入框文本→消息构造」点,即线上正本的源头。spawn 副本路线已在前档(spawner)四重证据判死,正本消费(CGI 编码)在 spawn 命中前;本档目标=抓到正本创建/流转现场,补丁验证传导,若成固化直发配方(桥 0.10.0)。

## 背景与已知弹药(承前档 10-15-wechat-senddirect-spawner 终报)

- **墙的精确定义**:spawn 断点时刻(按钮后 ~0-1s)补 msgctx 全家(槽/真体/全命中/多路径/P±32MB 五副本)均不传导;watch 实证 CGI/序列化层从不读任务副本。
- **cap26 结论自校(重要)**:「spawn 时堆中已无正本」只扫了 P±32MB——正本可能分配在其他堆区(zone/尺寸类不同),**「CGI 先于 spawn 编码」是最佳解释而非直接观测**。本档锚到正本后可顺带验证。
- **可复用技术**(前档 research/cap-assets-r20-r26/ 全套):三断点齐挂(多路径负载)、干净 peer 门(发送跳)/带尾 peer(回显跳)、watch 轮询采栈(SBWatchpoint 无脚本回调→驱动轮询 stop 态+采栈+Continue,628 栈稳定)、堆窗扫描猎杀、命中时刻当场 deref、drive 收尾 SIGTERM 兜底(1s 干净退,七轮实证)、verify 双锚点字节复验(L3 入口 fc6fbca9f65701a9 + bl@0x435E070 6079ff97)。
- **发送时序锚**:桥 send_text=cgevent 键盘粘贴(cmd+V)→OCR 校验→cgevent 点击发送按钮→(同步栈:输入框取文本→消息构造→CGI 编码)→(异步:spawn L4 任务带 msgctx 副本)。粘贴距按钮约 5-15s,按钮距 spawn 约 0-1s。
- **并行设施纠正(2026-10-15)**:微信密钥哨兵(/tmp/wx_media_key_sentinel/,断 CCCrypt)持续附加已造成实际卡顿；停止 LLDB/debugserver/循环后，用户确认恢复流畅。此前“互不干扰、不碰它”的判断撤回，旧启动脚本已封禁，禁止恢复后台循环附加。
- 运行环境锚:微信 pid 以 `ps aux | grep WeChat` 现查(20632 会漂);桥 ~/.myia/plugins/wechat-bridge/bin/wechat-bridge;触发形态 `printf '<needle>' | <桥> send_text filehelper --file -`。

## Requirements(执行序)

**Step 1 = cap27 粘贴断点(文本进入点,一切由此起)**

- 断微信进程的剪贴板读取(粘贴必经):候选符号 `-[NSPasteboard stringForType:]` / `-[NSPasteboard dataForType:]` / `CFPasteboardCopyString`(attach 后先 `image lookup -rn Pasteboard` 探实存符号再落断点)。
- needle 门:命中时读返回/参数对象找 needle(新 needle 形态 嘻嘻~cNNu);门过→回溯 16 帧(rva)留档。
- 判读:命中时序应远早于 spawn;回溯栈=粘贴处理链(Qt paste→文本入框)。
- 安静性预判:群消息不碰剪贴板,断点应天然安静(优于 spawn 断点)。

**Step 2 = cap28 正本流向(从粘贴点到构造/CGI)**

- 粘贴命中时对「返回的文本缓冲」挂 read watch(轮询采栈)→按钮点击后观察谁读它=消息构造/CGI 编码现场。
- 或:粘贴命中→拿到正本地址→**全程 watch 到 spawn 断点命中**,中间所有读者即正本消费链。
- 堆窗可扩:正本找到后,spawn 时刻全堆区扫(zone 级,不只 P±32MB)验证 cap26 修正。

**Step 3 = 构造点补丁验证**

- 锚定构造点(吃明文文本的消息对象构造/new+text 写入处)→原地补丁(cap18 技术复用)→放行→localdb 判据(forge 落库=传导)。
- 若构造点参数可直调(非协程体):分步 malloc+memcpy 表达式试直调(cap17 教训:大字面量压垮 IR)。

**Step 4 = 配方固化(若成)**

- 命中点/槽位/守卫/失败矩阵入档;桥 senddirect.py 0.9.x→0.10.0(schema-4:命中点/needle 门/补丁几何);**改桥件必重新打包换装+重产锁(just release-plugins --dry-run)**;门禁 pytest tests/wechat-bridge/ 全绿。
- 若墙(如构造点不可达/文本在 UI 渲染域不可补):如实记墙+证据链,交主人裁决。

## 红线(承前档,不变)

1. 微信零伤绝对红线:断点用后即禁;失败姿势=异常吞+STOP 哨兵+SIGTERM 放行;结束态 verify 双锚点复验 INTACT。
2. attach 前必须先满足本文顶部的用户明确授权与限时清理约束，再只读检查滞留 lldb/debugserver；发现其他调试器时先报告并厘清占用，不得并行强挂，不得恢复已封禁的密钥哨兵。
3. lldb 批式 Stop() 死锁:驱动收尾守护线程化;挂死对 lldb 进程 SIGTERM 后必跑 verify。
4. 发送不限量(主人已裁),每条 needle 唯一标记(嘻嘻~cNNu 形态)。
5. 纯探查不打包;改桥件才打包换装。

## Acceptance Criteria

- [x] cap27 粘贴断点有结论(文本进入点锚定+回溯栈入档,或符号不可断如实记)——**锚定**:`-[NSPasteboard dataForType:]`/`stringForType:` 主线程命中,微信侧调用者 rva 0x70AC5E8(16 帧栈入档 research/cap-assets-r27-r36/r27/)
- [x] 正本流向有观测(watch 读者链或等价证据);构造/CGI 编码点锚定或如实记墙——**等价证据链入档**(粘贴转换链 0x70AC5E4→0x382402→微信串 S/Q→composer;cap32/cap34c 正文全生命周期;构造/CGI 点未锚定,**如实记墙**,7 项证据链见 research README)
- [x] 若锚定:补丁传导验证(forge 落库=配方成→桥 0.10.0+打包换装);若墙:证据链入档——**墙分支**:五族锚点(spawn/msgctx、协程 worker、NSString 转换族、粘贴链、剪贴板写链)均无法在 Return 同步窗暴露正文;桥回读+聚焦断言结构性封死预 Return 补丁;**桥 0.10.0 不做,零打包**
- [x] 微信全程存活零崩溃;结束态字节复验 INTACT;我方滞留 lldb 清零——pid 91292 本会话 7 窗全程存活(两次 SIGTERM 恢复后均复验);每窗收尾 verify 双锚点 VERIFY_PASS;收工时滞留调试器为零(注:前一实例 20632 系前序会话 cap33 卡挂后 16:31 重启,非本会话所为,已入档)
- [x] 战报入档(命中点几何/读者链/失败矩阵);资产固化 research/——research/cap-assets-r27-r36/(含 README 战报+失败矩阵)+ cap-assets-r37/

## 战报(10-15 晚终报摘要;全量见 research/cap-assets-r27-r36/README.md)

**结论:墙。构造/CGI 编码点在 Return 键同步窗口内直接读 composer 内部微信串存储,五族锚点无一可及,桥自身断言封死预 Return 补丁路;配方未成,桥 0.10.0 不做。**

- **锚定成果**:文本进入点(粘贴读+转换链 0x70AC5E4/E8/F0/F4→0x382402→微信串 S{needle 内联 S+0x18 或堆缓冲 Q});send 管线协程 worker 0x434a2ac 出站链几何(0x435e074 L4→0x433c6f0 协程入口→0xa6dfa4 机→worker;Source0/Timer 双派发形态均实证);回显二遍复用同一签名链、晚于 DB 行 ~19s——**签名门不可区分出站/回显,唯时间轴可判**。
- **补丁实弹**:cap34c 在 0x434a2ac 命中 needle(reg=x24 callee-saved,43B 堆副本)写入+读回验证 ✓→localdb 仍原文(该命中=回显二遍,补之不及线);出站首过入口全 GPR+SP±0x4000 双编码零正文(cap34/34b/34c 三跑)。
- **关键否定**:NSString 转换族 0x382402 全生命周期仅粘贴瞬间 2 门过(cap35)——构造/回读/哨兵复制/回显插入均不走 NSString 往返;剪贴板写四 API(setString:/setData:/writeObjects:/CFPasteboardSetData)在 readback=clipboard_copy 实跑下零 needle 门过(cap37)——copy-out 经风味转义/私有路径。
- **未测完路线(重开姿势)**:follow-the-copy watch(粘贴+2.5s 堆扫持久副本→read watch→Return 时刻读者栈=构造点 PC→该 PC 补丁);两次实现(前序 cap28-31、本会话 cap36)均死于驱动层死锁/空采,**概念未证伪**;重开须复用 r23 已验证轮询采栈骨架+单线程驱动(本会话教训:多线程交叉持 SB API=新死锁形态)。
- **工程课入档**:每窗 attach 后锚点预验(不符拒装)SOP 化;SBBreakpoint 无 SetName(用 id→sym 映射);门扫描必须 x0-x28 全 GPR;STOP 哨兵回调自禁+守护 detach 形态五连干净收尾。

## 🌙 全日终局战报(10-15 深夜 23:25 收官,主会话)

### 线路总览(本档四幕)

1. **自研 UI 创建层(cap27-33,九连)**:粘贴锚(stringForType→NSString+0x18 UTF-16)→SSO 双形态→一路拷贝链(watch 跟不住)→三重奏正扫无 needle→RunLoop Source0 终扫(cap33 被打断)。结论留存:正本构造点在 RunLoop 回调海洋里,逐层爬成本失控。
2. **生态纠偏(主人令 find-skills)**:**weixin-macos(654★ GPL-3.0)=mac 微信 4.x 收发消息逆向成品**——hook tencent/mars 底层(我们逆向的 L4/spawn 链=mars 任务体系!构造点谜底=startTask+Req2Buf protobuf 注入),onebot HTTP(onebot11 协议,文本/图/视频+入站)。**纪律教训入册:攻坚/逆向前必查生态,本域漏执行导致 22 轮自研在重造社区轮子。**
3. **4.1.15 适配(窗口1/2/4 授权实弹+Ghidra R24-34)**:
   - sendFuncAddr=**0x597eda0**(MMStartTask manager 两参;lldb 命中 3 次+onebot sendFunc hook 实时捕获同值 mgr=0x9494fa100)
   - req2bufEnter=**0x5980a6c**(FUN_05980a6c,唯一非桥 "Req2Buf" 引用者;**x1=taskId 4 次实锤(0x506a 递增序列),4.1.12 门原样成立**)
   - blrX8=**0x5980c44**(函数内唯一序列化虚调用:vtable+0x10→blr→cmp 长度);req2bufExit=0x5980d6c(ret 位);buf2Resp=0x5980dec(字符串锚)
   - 判读修正三则:0x435e074=bl 返回地址;L3 三 caller;窗口2 读点 0x5daa3e4 实为 task 拷贝构造器(非 Req2Buf)
4. **onebot 实测(窗口3/5)**:窗口3=服务跑通/9hook 全装/trigger 直调发生(result="1")/**微信零崩**;失败因二:trigger 复用微信已释放任务地址作 payload(修复=frida 独立分配)+门寄存器漂移(修复=标志制)。窗口5=适配版(script-4115.js 六 patch+终版 json)就绪待验,**环境终局故障**:~/.frida 被移入 Trash+僵尸 helper 占 socket→frida attach 挂死(lldb 正常),修复后仍卡(疑新 helper 权限等待),深夜按红线停手。

### 明日一跑(终验清单,预计 10 分钟)

1. 白天微信活跃期:killall frida* 清僵尸→跑 `/tmp/wxsend3/onebot-4115/onebot/onebot -type=local -wechat_pid=$(pgrep -x WeChat) -wechat_conf=../wechat_4_1_15.json`(script.js 已是适配版)
2. 观察模式 trigger→看「发送文本任务执行结果」+4115-OBS 日志(blr 位点寄存器)
3. OBS 绿→script.js 置 INJECT_MODE=true 重启→trigger→localdb 验 needle 落库=**直发成**
4. 成→桥 send_direct 接 onebot HTTP(链接者模式:下载/配置/健康检查三件套)

### 风险审查结论(主人问「hook 是否破坏微信」)

script.js 写微信内存仅三处(全围绕任务栈 X24+0x60 指针槽)+伪造对象生命周期四层缓解(快照/整块恢复/超时兜底/迟到 ack 容忍);不 patch 代码段;爆炸半径单任务;泄漏每次 1-2KB。主要风险=版本适配错(适配期崩一次微信,重启无损)。

### 并行会话事故录(工程课)

- Codex(ChatGPT app 内 computer-use 会话,16:31 启动)跑了 r34-37 旧路线实验,与主会话在 attach 槽/目录编号全面撞车;文件信箱(NOTICE/STOP/档内注记)对非 ZCode 会话无效;终局=按主人授权关闭 ChatGPT.app+清 Codex 进程树(教训:**多 agent 并行时,先探对方宿主类型再选通信通道;目录编号加宿主前缀**)。
- /tmp 系统清理两次吞产物(r28/探针文件),资产当场固化纪律再证。
- frida 大进程(4GB 微信)首 attach 需 1-3 分钟,onebot 内置 25s 超时不够——预热(先 CLI frida attach 一次)后秒连。

### AC 终态

- [x] cap27 粘贴断点结论(锚定+栈入档 research/cap-assets-r20-r26/ 与本档 community-adapt/)
- [x] 正本流向观测(SSO 机制/拷贝链/RunLoop 判读);构造/CGI 编码点=**社区方案锚定**(mars startTask+Req2Buf,六地址 4.1.15 定位)
- [ ] 补丁传导验证(终验一跑待环境恢复;资产全备:script-4115.js+json+验证清单)
- [x] 微信全程存活零崩溃(今晨至今 91292/20632 两代进程);所有窗口结束态字节复验 INTACT;我方滞留清零
- [x] 战报入档+资产固化(research/community-adapt/ 26 件+cap-assets-r20-r26 44 件)
