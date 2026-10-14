# evidence-阶段3-final(capture_call 真机证明轮;2026-10-15 05:30-05:51 CST)

> 执行者:真机验证员(动态工作流子代理)。产物根 `/tmp/wxsend6/`(本档所有 stdout/stderr/哨兵副本/截图/复现脚本在位)。预算红线:直调真发 ≤2 + 触发 ≤2、目标仅 filehelper、微信异常即停、不确定绝不重试。**P-0 已裁 (c)+主人令「继续做完」为本轮发送授权依据**(原文载体=design-阶段3.md §4 P-0 裁决块 :405-409;「继续做完」另见 design-阶段3.md §2.9 标题 :601、research/r4/cap8.py:1 头注。〔10-15 补笔改锚:原括注引「evidence.md 预算账 10-15 更新节」,该节当时不含任何 (c)/「继续做完」记载,锚点失准;该节已于同日归档补笔回填 P-0 裁决,现可作次级载体〕)。

## 0. 环境与基线(05:29-05:31)

| 项 | 值 | 证据 |
|---|---|---|
| 微信 | pid **40379**(4.1.15),全程未变 | `pgrep -x WeChat`;doctor state=ok |
| lldb | /usr/bin/lldb,零残留 attach | `which lldb`;`ps aux│grep lldb│debugserver` 空 |
| 锚定表 | schema 3,send_entry=0x83e394,observe_bp,svc_vtable_off=0x9c516b8,**svc_invariants_hex=null(待 capture 回填)**,callable_for_send=True | 数据根 `wechat-bridge/send-direct-anchors.json` |
| 配置门 | **缺省关**(config.json 仅 `{"mem_search_enabled": true}`)→ **代开 `send_direct_enabled: true`**(P-0 已裁 (c)+主人令;验后保持开启,见 §7) | `/tmp/wxsend6/config.json.before` |
| 桥形态 | 装机桌面 python(3.14.8)+ 工作树 0.9.0(send_direct 仅存在于工作树;site-packages 0.8.4 无此命令) | `python -m wechat_bridge` 自插件目录 |
| DB 基线 | filehelper 表 `Msg_9e20f478899dc29eb19741386f9343c8`(md5(filehelper))**73 行**,max create_time=1792008585(04:09:45 嘻嘻~cap5),近 30 分钟 0 行 | sqlite3 直查 decrypted 副本 |
| 崩溃基线 | 最新 WeChat 崩溃报告=昨日 20:46(E10 事故) | DiagnosticReports 列表 |

dry-run 前置验证(零预算):`send_direct filehelper --file - --dry-run` → exit 0,`preflight: "ok"`,anchor_build 4.1.15,elapsed 4122ms(`/tmp/wxsend6/dryrun.stdout`)——版本门链(模块锁定+16B 锚字节+165MiB 切片 sha256+attach)真机全绿。

## 1. 五轮发送实跑账(全 record 如下)

| 轮 | 时刻 | 命令形态 | 结果 | 出站 | 证据 |
|---|---|---|---|---|---|
| send#1 | 05:30:47 | CLI capture_call(嘻嘻) | ❌ exit 30「lldb 批超时(armed 前 45s)」 | **0**(触发未放、DB 零新行、指纹回滚) | send1.{stdout,exit};DB 73 行复核 05:31 |
| send#2 | 05:36:56 | 同上(修复①后) | ❌ exit 30「capture 段观察窗超时(needle 未中)」 | **0**(触发放出但 navigate 3 连败,线程被弃,DB 零新行) | send2.{stdout,exit} |
| send#3 | 05:41:01 | 插桩 driver(触发 trace+哨兵盗录+2s 截屏) | ❌ 同 send#2;trace 实证触发 T+3.61s 放出、T+34s 进程退出时 ax.send_text 仍未返回 | **0** | trigger3.log;run3_shots 16 帧 OCR |
| send#4 | 05:46:43 | 同 send#3(修复②后) | ⚠️ **capture 全链绿**;expr 直调抛 C++ 异常 → exit 1 `send_direct_call_failed` | **触发 1**(row 88 嘻嘻~cap 05:47:00);直调 **0** | send4.*;run3_sentinels/* |
| send#5(误) | 05:49 | 本意为防重探针,但距 send#4 armed **>120s 窗已过** → 整轮 capture_call 又跑了一遍 | ❌ 同 send#4(expr 再抛,-4) | **触发 1**(row 89 嘻嘻~cap 05:49:18);直调 **0** | dedup.stdout;DB row 89 |
| dedup2 | 05:50:10 | 同参立即重发(窗内 52s) | ✅ **exit 17 `send_uncertain_dedup`「pending,120s 窗内,剩 64s:绝不自动重试」;DB 零新行** | 0 | dedup2.{stdout,exit} |

**预算终账:触发出站 2/2(触顶,不再有任何 capture_call);直调真发 0/2(两次 expr 均异常,零送达)。**send#5 为执行时序失误(防重探针落窗外的客观后果),如实入账;其价值=直调异常的第二次独立实证(-5/-4 内部异常断点各一次,非偶发)。

## 2. 两个真机首发 bug:根因+修复(本轮代码改动,全部留工作树未提交)

### bug①(sync Continue 自死锁;send#1 根因)

- 现象:45s 批超时、零哨兵、触发未放、零出站;dry-run 却绿(dry-run 不经 Continue)。
- 根因实证(零风险实验,目标=/bin/sleep 非微信):lldb 命令文件批(`-b -s`)SBDebugger **缺省 async=False**,`proc.Continue()` 阻塞至进程再停;而 `CAPTURE_ARMED` 在 Continue 返回后才写(`senddirect_probe.py` _capture_template),桥侧见哨兵才放触发 → **触发被一个需要触发才能出现的前置所门死**。`PHASE1 async_default=False` 且 PHASE3 永不打印(SIGINT 无效,SIGKILL 收,rc=137):`/tmp/wxsend6/async_test.{py,cmd,log}`。
- 修复:`_capture_template` 段首 `lldb.debugger.SetAsync(True)`(Continue 立即返,轮询循环按设计跑),finally 恢复 `SetAsync(False)`(`plugins/wechat-bridge/wechat_bridge/senddirect_probe.py`)。

### bug②(触发目标合成形态 navigate 必败;send#2/#3 根因)

- 现象:触发线程 30s+ 不归、零出站;插桩截图(16 帧 OCR)实证 UI 链**卡在搜索-选行循环**:搜索开、词入框、结果浮窗渲染,但始终点不进会话,3 次尝试耗尽。
- 根因实证(零预算 repro):`ax.send_text(合成目标 display_name=""/search_term="filehelper", dry_run=True)` → 54.1s 后 exit 15「搜索结果浮窗无可定位行(分区过滤零候选)」;同链 CLI 解析态目标(display_name=文件传输助手)dry-run **8.9s 绿**(navigated/pasted 全真)。机理:4.1.15 对 "filehelper" 的搜索浮窗无本地分区锚(联系人/群聊头),`navfilter.select_result_row` 「无本地头 → None 绝不猜」→ 零候选。
- 修复:CLI 触发闭包改用**解析态**目标——同目标直发(filehelper 发 filehelper)复用主目标;异目标再 `resolve_target("filehelper")`(异常/形态不符回落旧合成形态,语义同旧)(`plugins/wechat-bridge/wechat_bridge/cli.py` send_direct 分支)。
- 回归测试:test fake lldb debugger 增 SetAsync 记录;`test_full_run_hit_disable_construct_call_sequence` 增 async_on→continue→…→async_off<expr_eval 序断言;`test_happy_path_payload_shape` 触发桩增 `display_name=="文件传输助手"`(旧合成形态必红)。**全套 `pytest tests/wechat-bridge/` = 827 passed, 14 skipped**(两处修复后各跑一遍)。

## 3. ask 逐项结论

| # | 项 | 结论 | 证据 |
|---|---|---|---|
| 1 | capture_call 流程(触发 send_text 一次+断点捕获 ctx/模板+直调一次) | **流程机架全绿,直调模型红**:send#4 实序=T+4.5s CAPTURE_ARMED(bp=0x12b926394=slide+0x83e394)→T+4.25s 触发放出(嘻嘻~cap)→主线程断点命中→needle 中→读 x0=ctx(37103942680)/dump x1 起 0x230B 模板(sha dc5b305c…)/vptr−S=0x9c516b8 与锚定全等→不变量采集→PREFLIGHT_OK→ARMED(T+11.4s)→**expr EvaluateExpression 执行中被内部 C++ 异常断点打断(-5)「The process has been returned to the state before expression evaluation」**→ERROR stage=call→回执红→exit 1 `send_direct_call_failed`(never-retry 族,按设计 fail-closed)。微信全程存活、状态复原、干净 detach | run3_sentinels/{CAPTURE_ARMED,ARMED,PREFLIGHT_OK,ERROR}.json+lldb-batch.log;trigger3.log TRIGGER_DONE sent:true |
| 2 | localdb 落库回执(sqlite 直查) | **触发消息落库实证**:row 88(local_id=88,local_type=1,create_time=1792014420=05:47:00,嘻嘻~cap)+row 89(1792014558=05:49:18,同文);直调消息(嘻嘻)**未落库**——与 expr 异常自洽(回执红判断正确拒绿) | sqlite3 直查 `Msg_9e20f478899dc29eb19741386f9343c8`;时间窗+内容+local_type=1 齐 |
| 3 | 微信存活断言 | ✅ pid 40379 全程不变(基线 05:30:28 → 终检 05:51);零新崩溃报告(最新仍为昨日 20:46 E10 件);零 lldb/debugserver 残留;终检 doctor state=ok/main_window=ok;五轮全部干净 detach | 本档 §0/§4;DiagnosticReports 复核 |
| 4 | 第二条直调验缓存路径(ctx 复用) | **跳过(未实现,如实)**:`execute_send` 每次 invocation 都是全新 lldb 批+全新触发捕获,无跨进程 ctx/模板会话缓存(senddirect.py 全文无缓存机制;锚定表仅回填不变量)。经验旁证:send#5 重新走了完整 capture 段 | senddirect.py 代码面;send#5 行为 |
| 5 | 防重:同参立即重发 deduped/17+零新行 | ✅ **exit 17** `send_uncertain_dedup`(pending,120s 窗内剩 64s,绝不自动重试);DB 75→75 **零新行**。注:防重态=armed 后 pending(直调异常所留),非 sent_recently 的 deduped/0 形态——两形态都属 ask 认可的「deduped/17」口径 | dedup2.{stdout,exit}+DB 计数 |
| 附 | 锚定表不变量回填 | ✅ svc_invariants_hex 由 null → `009647a3080000002800000000000000183c91a308000000`(§2.7 回填路径真机首证) | 数据根锚定表(05:47 后) |

## 4. 直调 C++ 异常——如实定性(未解,交下轮)

两次独立实跑(send#4 -5 / send#5 -4,内部异常断点编号异、现象同)=**确定性模型缺陷非偶发**。expr 形态=栈上 560B 模板拷贝+三槽补丁(inline23)+0x228 置 0+`F_exec(ctx, msgctx)` 于**停在 F_exec 入口的主线程**上再入调用。异常在调用内同步抛出(__cxa_throw 命中 lldb 内部断点),UnwindOnError 完整回滚(微信零伤)。候选机理(按既有证据权重):①E14 已证 x0+0x8=043f88e4 自指=「函数指针入协程」——F_exec 疑为**协程过程体**而非可自由直调的入队 API,脱离协程框架上下文同步调用即抛;②msgctx 位于 lldb 求值栈(异步消费需堆存活)——但异常发生在 expr 期间而非返回后,非首嫌。**本轮不再消耗预算试错**(触发已 2/2 触顶,且无假设驱动的第三方案);模型修订(改走上层提交者或框架内调度)属下轮逆向面。

## 5. 零伤核验(逐轮)

send#1-#5+dedup2 每轮后均复核:pid 40379 在、DB 行数与预期一致、`ps`零 lldb/debugserver 残留;全程零崩溃报告新增;lldb-batch.log 尾=干净 detach+quit。触发线程两次被弃(join 超时)后进程自然退出,无孤儿进程(终检空)。

## 6. 工件清单(/tmp/wxsend6/)

config.json.before;baseline/{pid,crash_reports_before,filehelper_count,send_state.before}.{\txt,json};dryrun.{stdout,stderr};async_test.{py,cmd,log}(bug① 零风险实证);send{1,2,4}.{start_epoch,start_time,stdout,stderr,exit};trigger3.log(send#3/#4 触发 trace);run3_sentinels/(send#4 哨兵盗录 7 件);run3_shots/shot_01-16.png(+本轮 OCR 转写);send3_driver.py(插桩 driver);dedup.{stdout,exit}(send#5 误轮);dedup2.{stdout,exit}(真防重);textdry.{stdout,stderr}(解析态 dry-run 绿);合成目标 repro 命令与 54.1s exit 15 输出(见 §2 bug②)。

## 7. 遗留与交代

1. **配置门保持开启**(`send_direct_enabled: true` 留在数据根 config.json)——遵主人令(P-0 裁 (c)+「继续做完」),特此注明;关闭方法=删该键或置 false。
2. 工作树三件(senddirect_probe.py / cli.py / test_send_direct.py)含本轮修复,叠加在原 M 态上,**未提交**(非本验证员职责面)。
3. send#5 误轮(防重探针落窗外)=执行时序失误,如实入账;其触发出站与 send#4 同文(嘻嘻~cap)但为两条独立消息(row 88/89)。
4. 直调模型缺陷(§4)为最终未竟项;capture 机架/回执/防重/存活面全数有结论。

## 8. 打包换装回执(打包安装员,2026-10-15 05:53-06:03)

§7.2 交代的工作树三件(实为四件:另含 senddirect.py 阶段3终版模型)本轮已走完门禁+打包+装机+提交链:

- **全量测试**:`uv run --no-sync python -m pytest tests/ -q` = **1 failed, 6289 passed, 56 skipped(165.62s)**。单红 `tests/push/test_messaging_macos_notify.py::TestNotifyRelayFifo::test_relay_end_to_end_zero_osascript` = 在册 FIFO 竞态(10-14-notify-app-icon prd.md「转交注记」:第 2 条通知泄漏一次 osascript 直弹,同签名);与本批 wechat-bridge 改动零交集;单验该文件 23 passed(0.27s)。按档内门禁处置口径记条件绿。
- **构建**:`just build-desktop` exit 0 → `世事.app`(20.47MiB)+`世事_0.0.3_aarch64.dmg`(9.13MiB)。MYIA 二进制 sha256 `088a0f0d167a0cad…`;dmg sha256 `64180d2aa1b1dfbd…`。
- **验源**:装包内 `Resources/components/wechat-bridge/wechat_bridge/{cli,senddirect,senddirect_probe}.py` 与工作树 `cmp` 逐字节一致(三件全)。
- **换装**(判例全流程):osascript 温和退出在跑实例(旧 pid 56444;sidecar 随 stdin EOF 自清)→ 旧装备份 `/tmp/世事.app.bak-1015-sendmsg` → cp -R 新包入 `/Applications/世事.app` → 装后二进制与构建产物 cmp 一致+插件三件一致 → `rm -rf ~/Library/WebKit/com.myssia.app ~/Library/Caches/com.myssia.app`。
- **像素冒烟**:`MYIA_SHOW_ON_START=1` 直跑装机二进制(pid 10950)→ 主窗(窗主名=世事,id 1045696→104564 族)亮窗渲染 → `screencapture -l 104564 -x` 截图(922,141B,3976×2236,**禁全屏,定窗**)→ Vision OCR 一级实证全 UI 在屏:侧栏「仪表盘/情报流/采集/定时任务/采集日志/配置/源管理/YAML配置/Telegram/飞书/微信/机器人凭据/代理池/凭证猎手」+顶栏「3个源失效 今日采集 550条•32/48 源在线•推送成功16」+「今日概览(UTC) 活跃源 32/48 今日采集 550」。截图/日志本地档 `evidence/smoke-1015-sendmsg-swap.{png,log}`(`.gitignore:123` 忽略 evidence/ 子目录,仓策,故实物留本地+本节文字回执入 git)。
- **收尾**:冒烟实例退出干净 → `open -g` 复原常驻(pid 18494,零焦点)→ env 旗核:常驻实例冒烟旗(MYIA_SHOW_ON_START/SMOKE_*)=0;`MYIA_EXTRACT_FALLBACK=1` 为主人 launchctl 全局预置(会话起始 zcode 进程即带,`launchctl getenv` 实证),非冒烟泄漏。
- 注:新包 `codesign --verify --strict` 报「code has no resources…」= 10-11 在册构建固有告警(源包同报判例);冒烟启动全链即权威闸,已过。

**〔10-15 归档补笔(代审复核两笔回填)〕**

1. **装机/提交时序如实补记**:换装窗 05:53-06:03(装机件 mtime=05:58:45)先于提交 bd395888(2026-10-15T06:04:35+08:00)约 90 秒——装机时装的是**工作树态**,非「已提交态」,时序上两者不能画等号。内容等价已当代复核(补笔轮实跑):装机三件 `/Applications/世事.app/Contents/Resources/components/wechat-bridge/wechat_bridge/{cli,senddirect,senddirect_probe}.py` 与 HEAD 逐字节一致(`git show HEAD:<path> | cmp - 装机件` IDENTICAL ×3),且 `git log bd395888..HEAD --` 四代码件=零后续触碰 → 装机内容 ≡ bd395888 后来提交态(字节级)。
2. **提交回执数字勘正**:bd395888 提交消息「test_send_direct.py +26 用例」与实测不吻合——`git diff bd395888~1 bd395888` 计 def test_ 新增 **27**/删除 **4**/净增 **23**(全文 38→61;parametrize 前后均 1 处);collect-only 实测当前 **63 tests collected**(提交前 40 系代审轮实测)。数字账不齐但非红绿问题:套件 `pytest tests/wechat-bridge/` = 827 passed/14 skipped 与 §2 bug② 节回执精确吻合。
