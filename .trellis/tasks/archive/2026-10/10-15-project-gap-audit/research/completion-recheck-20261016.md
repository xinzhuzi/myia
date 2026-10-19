# 相关任务完成性复核（2026-10-16）

结论：没有全部完成。复核范围为上轮审计涉及的五个执行/计划任务、审计本身、待办池，以及看板和装机验证缺口；没有把 review、测试通过或研究资产齐全等同于产品交付。

最后运行态检查：2026-10-16 00:11:10 +08:00。本轮没有附加调试器、触发微信发送、启动/关闭装机应用、执行 Git/worktree、修改生产代码或任务状态。

## 逐任务核验

| 任务 | 当前状态 | 实际完成情况 | 未完成/证据 |
|---|---|---|---|
| 10-15-media-key-hunt | in_progress | 静态坐标与离线工具切片已交付；父任务未完成 | PRD:62-65 四项仍未勾；本轮用既有钥通道对5份真实样本复验，exit2、blocked_missing_key、verified0。缺真实钥、三图解密、供钥、装机 |
| 10-15-wechat-senddirect-uicreate | review | 自研旧路线研究已记录；社区适配真实直发未验成 | PRD:109 传导未验收；:121-125 最新终验记录为最后注入前失败，并记载一次微信 crash。当前脚本后续修改尚无本轮成功发送证据 |
| 10-15-wechat-senddirect-spawner | review | spawn 路线阴性研究阶段有交付，不能说实现了任意正文直发 | PRD:119-124 四项阶段AC完成；阴性分支明确不做桥0.10.0；顶部:9/:13仍TBD，须和阶段结论统一 |
| 10-15-feed-local-images | planning | 仅计划，功能尚未实现 | feed-screen.tsx:1118-1131仍只输出路径与v2.2 TODO；tauri.conf.json:26-30 scope仍只有微信媒体缓存；四项AC全未勾 |
| 10-15-trellis-no-git-task-create | planning | 仅计划，修复尚未实现 | task_store.py:473仍无条件run_git；无须实际调用Git即可确认与项目禁令冲突；四项AC全未勾 |
| 10-15-project-gap-audit | planning | 上轮报告已交付；本轮完成相关任务复核 | 审计报告不是产品问题已修复的证据；上轮核心/插件逐模块审计未完成的限制仍成立 |
| 10-03-v12-backlog | planning | 待办池，不能按planning推断所有条目未做 | 开头三项含明确“已消号”回标；保留历史/用户侧验证边界，不重复算成新任务 |

## 新确认的完成口径问题

### 1. 直发档的零崩溃验收与后续真实记录冲突

uicreate/prd.md:110 的“全程存活零崩溃”仍打勾，而:125记载23:43发生一次SIGSEGV。保存的 community-adapt/crash-234325.ips 由本地JSON解析确认：WeChat、EXC_BAD_ACCESS、SIGSEGV、捕获时间2026-10-15 23:43:22 +0800。报告仅提取这些诊断字段，未外发崩溃全文。

正确结论是：此前研究切片的存活结果与后续社区适配窗必须分开；后续发生过崩溃，因此不能把整个任务概括成零崩溃或已终验成功。

### 2. 旧风险说明已不能覆盖当前适配脚本

uicreate/prd.md:95-97旧说明称不patch代码段；当前community-adapt/script-4115.js:792-802已对微信模块偏移0x5980c30做Memory.patchCode/NOP，:851-859在onLeave恢复。脚本mtime为2026-10-16 00:08:48，晚于PRD最后更新。

同一脚本:362为INJECT_MODE=false，但模式检查在:680；Req2Buf入口:798已执行代码补丁，随后:810等分支改写消息指针，二者没有被这个观察模式开关保护。因此“观察模式”不能被当成不修改目标状态的保证。代码补丁当前看到的是onLeave恢复；取消、失败或提前终止时的恢复尚无本轮验证证据。下次动态窗口必须重新评估当前版本与限时清理，不能沿用旧风险结论或历史授权。

静态链也确认生产桥仍是既有LLDB路线：GitNexus query/context追到senddirect.execute_send，源码:802起调用load_anchor_table、require_lldb、run_lldb_batch；该文件未出现onebot接线。研究脚本/地址表在位不代表生产桥已完成社区方案集成。

### 3. 看板及装机验证缺口仍在

- fd定点检查.trellis/scripts，open_task_board.py仍未找到，不能按规定入口生成标准十列表；本轮没有伪造该看板。
- 当前装机包为com.myssia.app、版本0.0.3，无Contents/MacOS/myssia-core，使用自管Python。package_smoke.py:1017-1031会在该架构下跳过Part B；:689-691同时跳过sidecar断言。即使该脚本汇总PASS，也不能替代真实sidecar/编辑保存链验证。
- 该脚本:636-657会先退出并必要时TERM既有应用；本轮未调用该入口，以免中断共享运行中的应用。保留“装机真实链路尚未在本轮验证”的边界，没有宣称无头冒烟等于装机通过。
- 主线程只读对账：装机myssia-src/entry.py、myssia_desktop_entry/__main__.py及全部146个核心Python文件与源码一致；这不证明前端嵌入资源、插件、运行时配置或完整发行物都一致。

## 本轮新鲜验证

1. `.venv/bin/python -m pytest .trellis/tasks/10-15-media-key-hunt/research/test_verify_media_samples.py .trellis/tasks/10-15-media-key-hunt/research/test_media_window.py tests/scripts/test_wechat_bridge_mediadecrypt.py tests/wechat-bridge/test_media.py tests/wechat-bridge/test_send_direct.py -q --tb=short`
   - 158 passed、1 skipped、3.51s，exit0。跳过的是真LLDB表达式自有进程E2E，须MYIA_LLDB_EXPR_E2E=1才启用；本轮未开启。通过项使用离线桩/合成材料，不附加微信。
2. 前端Vitest：47文件、937 tests passed，12.79s，exit0。cron/tg-account用例仍有migration-banner缺mock的stderr，未导致测试失败。
3. TypeScript `--noEmit --incremental false -p tsconfig.app.json`：exit0。
4. browser-module、feed-card、logs-screen、tg-card四项无头冒烟均exit0；使用已有desktop/ui和夹具IPC，截图重定向到本次recheck目录，未重建或启动装机应用。
5. 真实样本离线验收：5份输入、要求至少3、verified0、blocked_missing_key、exit2、stderr为空。只保存脱敏计数，无钥、私有路径、摘要、明文图像入报告。

测试和截图产物位于research/recheck-20261016/。本轮没有执行Python全库测试，没有真实发送、真实点图或系统IME目验，不用历史CI绿色替代这些缺口。

## 微信与并行执行现状

复查微信PID29809、PPID1、state S、P_TRACED=false；未看到同名LLDB/debugserver进程。两份旧sentinel/launch.sh均仍在执行体之前exit78，未恢复旧循环。

本轮后段出现onebot进程PID48885，最后检查仍在运行。P_TRACED=false不能排除Frida注入或hook存留，不能据此宣称微信完全无注入。该进程是否已成功完成新一轮发送不在本轮证据中；本轮不接管、不重启、不触发、不终止其他会话。适配工作存在在途状态，以上动态结论仅为检查时点快照。

已对本轮关键源码/PRD保存sha256并在收尾复查，无期间变化；后续并行会话更新应以新的终验与产物重新判断，不能把本次快照永久当成终局。

## 建议的后续顺序

先让在途onebot窗口按其授权和清理机制收口，核验真实回执及崩溃/恢复证据；任何下一次活附加均需新的明确单次授权。媒体链要等真实钥后三图验真再供钥/装机。可独立实施的仍是no-git建任务与Feed预览；看板补齐和自管Python装机验证应单独形成可验证切片。不要先改任务状态、勾满AC或归档来替代这些交付。
