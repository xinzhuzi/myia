# weixin-macos 社区方案 4.1.15 适配状态(10-15 深夜快照)

## 已实锤(Ghidra+实弹三重验证)
- sendFuncAddr = 0x597eda0(MMStartTask manager 两参;lldb 窗口1命中3次+onebot sendFunc hook 实时捕获同值)
- req2bufEnter = 0x5980a6c(FUN_05980a6c,唯一非桥 "Req2Buf" 字符串引用者;内含序列化虚调用)
- blrX8 = 0x5980c44(enter 函数内唯一序列化虚调用:构造对象→vtable+0x10→blr→cmp 长度)
- req2bufExit = 0x5980d6c(enter 函数 ret 位)
- buf2Resp = 0x5980dec(字符串锚;"Buf2Resp" 引用者,待实弹校)

## 待定(需窗口4实弹)
- autoBufferWriteFunc:0x597e100=日志函数已排除;CAND_A 内 bl 0x5a6c868/0x5ab3f98 待验;或改自实现(mars AutoBuffer 结构公开)
- 门寄存器:4.1.12 的 x20/x1==taskId 在 4.1.15 漂移(桥位点 x20=param7);blr 位点 x1≠AutoBuffer(静态判)
- X24+0x60 语义=task+0x60 消息指针槽(4.1.12);4.1.15 的 task 在 enter 哪个参数待定

## 窗口3 实测结论(onebot+json)
- 服务跑通/9 hook 全装/trigger 直调发生(result="1"=未抛异常)/微信零崩
- 失败因:blrX8 门(x20)与 req2bufEnter 门(x1)寄存器漂移→注入未发生;首连超时=frida 大进程首 attach 慢(预热后秒连)
- 改 script.js 门=trigger 活跃窗门或 task 指针门(不依赖寄存器语义)是适配方向

## 关键文件
- ~/Downloads/微信反编译/weixin-macos/(clone)
- /tmp/wxsend3/onebot-4115/(onebot 二进制+json+script;tmp 易失,json 已固化)
- 桥函数链:0x5daad24(stn_callback_bridge,vtable+0x30 转发)→…→0x5980a6c(mmext 实现)
