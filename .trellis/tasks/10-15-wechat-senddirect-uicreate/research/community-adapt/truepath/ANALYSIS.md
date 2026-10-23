# truepath 勘察分析(4.1.15 文本序列化现场定位)2026-10-16 00:45–01:30

> 2026-10-16 接续复核勘误：下文为历史判读。0x5981cd4 实际为标志/长度访问器，不能称为已定位文本序列化器；样本未建立正文与任务关联，不能证明文本永不经过某路径。第三次崩溃与调试的因果关系未定，“机制上无关”“SIGTERM 无副作用”不成立。五份 drive_wf*.sh 均已入口封禁，禁止照本档复跑。新证据及接续门禁见 `.trellis/tasks/10-16-wechat-senddirect-offline-recovery/research/recovery-review.md`；原始日志保留。

## 结论速览
1. **命题否证**:mars 桥 0x5daad24(hunt_r29 所称 stn_callback_bridge)在两窗真实文本发送
   (wf101/wf102,均 sent:true+post_send_verified:true)中 **0 命中**(run1/run2,断点 locs=1、
   首指字节 ff4306d1=`sub sp,sp,#0x190` 与 hunt_r29 逐字节吻合;同窗阳性对照 0x5980a6c 命中 37 次、
   0x597d26c 命中 29 次)。它对 "Req2Buf" 字符串的引用只是 delegate 为空时的报错日志路径
   (hunt_r25 xref + hunt_r29 反汇编),**不是文本序列化链的一环** → 其 vtable+0x30 目标对文本路径
   不可捕获。旧 frida 探针(probe.log/probe2.log,pid 91292)同样 0 命中,互证。
2. **真实序列化分发链(实弹+静态双证)**:
   - 分发桥 0x5971c24(10 参形态,似 0x5daad24 同族 trampoline):this=0x78cab43c0(稳定单例);
     主路 `*(this+0x18)`(=0x78d51cd38,对象+8 处带 "ZTUM" 标记)→ 0x5980a6c;
     主路返回 0(null-getter 早退)→ 兜底 `*(this+0x10)`(**可变槽**,曾见 0x78c95ba70"default"实现
     与 0x78cc26180 mmnet 管理器——即 onebot 日志里 MMStartTask 的 X0)→ 0x597d26c。
   - 主路 0x5980a6c 内部(hunt_r33 全函数反汇编 + 37 次命中):getter 0x5980d74 取任务对象 →
     37 次中 36 次 null 早退;唯一深段执行(hit2_blrA_1,t=148.5,tid=21):
     **序列化虚调用 = 任务对象 vtable+0x10,调用位 0x5980c44,实测目标 rva 0x5981cd4**
     (对象 0x78cb26868,vtable 0x148266770=数据段 rva 0x9f2e770;
     槽位 +0x0=0x5981c6c/+0x8=0x5981ca0/+0x10=0x5981cd4/+0x18=0x5981cec/+0x20=0x5981fa8/
      +0x50=0x59820d0/+0x58=0x59820e4/+0x60=0x5982108/+0x70=0x5982114)。
     随后 0x5980ca4 阶段(hit2_blrB_1,lr=0x5980c48 证明是 blr 返回后的落点,即 json 里
     blrX8Addr=0x5980ca4 的真实身份):局部 AutoBuffer(x29-0xb8)→ 0x5a6c868 取长 →
     0x5ded378 扩容 **x21=第4参 out AutoBuffer** → 0x5ab3f98 memcpy。
   - 兜底 0x597d26c 热点 ~0.5–1Hz(背景流量),29 命中样本 x0=0x78cc26180,
     其 vtable 0x1482663e8(数据段 rva 0x9f2e3e8),关键槽 +0x48=0x59442cc/+0x50=0x597f418/
     +0x58=0x597f45c/+0x60=0x597f480/+0x68=0x597f484/+0x70=0x597f488/+0x78=0x597f4a4。
3. **文本 needle 定位未竟**:全部 67 个命中(dispatcher31+fallback29+enter37-重叠计)浅层对象图
   (x0/x1/x3 起 2–5 层,含一层指针槽 deref)均未见 嘻嘻~wf* 字面 → 文本任务类在采样窗内未走
   上述任何位点,或文本在更深的对象层。MMStartTask 0x597eda0 在 run3(wf103,sent:true)亦 0 命中
   ——ADAPT-STATUS 所称"发送必中3次"未复现(当时窗含 onebot 注入流,场景不同)。
   堆扫+读观察点方案(capwf5)因 lldb 区域 API 兼容问题两轮未出数;且第五窗尾部 WeChat 崩溃
   (见 §异常),按铁律停手。

## 参数形态判读(实弹)
- 分发桥 0x5971c24 入参:x0=this(0x78cab43c0);x1=taskid(u32,如 0x668/0x687,逐任务递增);
  x2=0;x3=**out AutoBuffer 指针**(全程贯穿,序列化输出容器);x4–x6=栈上小结构指针(0x17132cxx
  同线程栈邻域);x7=1/2(小整数);另有栈参(x29+0x10 u64 / +0x18 u16,转发出参形态);
  x9=cmdid 样值(0xe4dd/0xa625);lr 常见 0x5db0e58(上层另一 stn 桥 0x5db0db8 的兜底 blr 位)。
- 主路 0x5980a6c:x0=0x78d51cd38 固定单例(+8="ZTUM" 标记);x1=taskid(0x498/0x4a4…);
  x3=out AutoBuffer;x20=cmdid 样值;返回 w0=(getter 命中?1:0)。
- 深段 0x5980c44(blr 前一刻):x0=任务对象(getter 结果);x8=*(*(x0)+0x10)=序列化函数;
  x20=0x78d51cd38(主路 this);x21=out AutoBuffer;lr=0x5980bd0(深段入口侧)。
- 兜底 0x597d26c:x0=*(dispatcher+0x10)(可变实现,0x78cc26180);x1=taskid;x3=out AutoBuffer;
  x27=dispatcher this;lr=0x5971d14。
- 桥 0x5daad24:**文本场景无参数现场**(未命中),其静态形态见 hunt_r29:
  x0=this;x1–x7=参1–7;[sp]=栈参0(u64,尾段 x28 转发);[sp+8]=栈参1(u16,尾段 w27 strh 转发);
  delegate=*(x0+8);调 *( *delegate +0x30 )(delegate, 参1..7, 栈参0, 栈参1)。

## 六窗实录(全部 pre/post 锚点复验 PASS:L3@0x433C5F0=fc6fbca9f65701a9、BL@0x435E070=6079ff97)
| 窗 | needle | 断点 | 命中 | 发送 | 锚点 |
|---|---|---|---|---|---|
| run1 | wf101 | 0x5daad24 | 0 | sent:true | PASS/PASS(SIGTERM 兜底) |
| run2 | wf102 | 0x5daad24+0x5980a6c+0x5980c44+0x5980ca4 | 桥0 / enter37 / blrA1 / blrB1 | sent:true | PASS/PASS |
| run3 | wf103 | 0x597eda0(MMStartTask) | 0 | sent:true | PASS/PASS |
| run4 | wf104 | 0x5971c24+0x597d26c | 31+29(全背景) | sent:true | PASS/PASS |
| run5a | wf105 | 0x597d26c+堆扫 | 0(API 异常) | sent:true | PASS/PASS |
| run5b | wf106 | 同上(修复中) | 0 | rc=30(osascript 超时,未发) | PASS/**崩**→重启复验 PASS |

## 异常与收尾(铁律执行)
- 01:22:35 WeChat(56383)崩溃:WeChat-2026-10-16-012235.ips = EXC_BAD_ACCESS/SIGSEGV,
  faultingThread 57 webview_io_thread,栈全在 WeChatAppEx Framework(内嵌 webview UAF 样毒指针
  0xbf80000000000019)——**非** wechat.dylib、非 SIGTRAP、非断点地址,机制上与断点/纯读无关
  (本会话零写入;mach vm_read 只拷贝)。当晚 23:43/00:17 已有两次 onebot 时代崩溃在案。
- 处置:立即停手 → `open -a WeChat` 重启(新 pid 33589,slide 0x13be04000)→ 锚点复验
  **PASS**(verify_post.txt:post_reboot)。
- 附:lldb 收尾四窗均 Detach 卡死→SIGTERM 兜底(编排器 260/300s 看门狗),与 main-r4 时代一致;
  四次 SIGTERM 均无副作用(微信存活+锚点 PASS)。

## 关键文件
- hit2_blrA_1.txt / hit2_blrB_1.txt:序列化虚调用唯一实弹捕获(目标 rva 0x5981cd4)
- hit4_dispatcher_*.txt / hit4_fallback_*.txt:分发桥参数与实现 vtable
- hit2_req2buf_enter_*.txt(37):主路参数形态与 taskid 序列
- disdiag.txt:分发桥 0x5971c24 与 getter 0x5980d74 现场反汇编(纯读)
- capwf*.py / drivewf*.py / drive_wf*.sh:六窗可复现脚本;ARMED*:装断点与字节校验
- orchestrate*.log / verify_*.txt / *_run.log:全链锚点与收尾记录
- 崩溃报告:~/Library/Logs/DiagnosticReports/WeChat-2026-10-16-012235.ips
