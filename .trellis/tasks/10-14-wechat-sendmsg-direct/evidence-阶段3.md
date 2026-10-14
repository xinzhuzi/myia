# evidence-阶段3:白名单验证矩阵(直发通道)——验证员执行档

> 执行者=真机验证员(阶段 3 验证矩阵);执行窗=2026-10-15 03:25-03:30 +0800;
> 证据根=`/tmp/wxsend-e2e/`(本档逐条引路径)。微信活体 pid 40379 全程未断
> (pgrep 三次复核);**零 attach、零出站、零状态占用**——矩阵四项中三项为
> 只读/演练,一项(M1 真实发送尝试)被通道自身 fail-closed 前置门确定性拒绝。

## 前置态核验(矩阵执行前,03:25:19 采)

| # | 项 | 实测 | 证据 |
|---|---|---|---|
| P-a | 配置门 `send_direct_enabled` | **未置**(数据根 wechat-bridge/config.json 仅 `{"mem_search_enabled": true}`)→ 缺省 false=关 | `/tmp/wxsend-e2e/run-context.txt` |
| P-b | 锚定表 `send-direct-anchors.json` | **全机缺位**(全 home `find` 零命中)→ r4 钉入轮(P-1)从未产出锚定表 | 同上(find rc=1) |
| P-c | 装机桥(数据根 python3.14 site-packages) | **0.8.4,无 senddirect 模块**(repo 工作树=0.9.0 含之;本矩阵用 repo runner,PYTHONPATH 指向 repo 源) | `run-context.txt` + ls site-packages |
| P-d | send_state.json | last_send_epoch=1791985769(=10-14 21:49:29,动态轮 r3 桥自动发),fingerprints={} 空 | 同上 |
| P-e | WeChat/lldb | pid 40379 在跑;lldb=/usr/bin/lldb 在位 | 同上 |

**前提证伪**:任务假定「实现员已验过 filehelper」。实测否——localdb 窗口内
filehelper 最新行=**10-14 21:49:39「嘻嘻嘻嘻」(动态轮 r3)**,其后至 10-15 03:27
**零新行**(`m3-post-filehelper.rows.txt`);且锚定表全机缺位=直发真实出站
在物理上不可能发生(senddirect.py:683-698 fail-closed 拒 24)。send_state
指纹空。结论:**实现员未执行过任何直发真实发送,预算 0 消耗。**

## 矩阵执行(四项,均留证)

| # | 项 | 命令 | 结果 | 判定 |
|---|---|---|---|---|
| M1 | 直发 嘻嘻 → jiangliushi666 | `printf '嘻嘻' \| ./plugins/wechat-bridge/bin/wechat-bridge send_direct jiangliushi666 --file -` | **exit 1 `send_direct_disabled`**(配置门,cli.py:852-860;位于 G6/防重占位与 lldb spawn 之前→零 attach 零出站零占用)。目标解析成功(未报 send_target_not_found) | ❌ **真实发送未发生**——通道按设计 fail-closed:门=主人显式开启(design-阶段3 §3.2),验证员无权代开 |
| M2 | localdb 落库回执(username 定向查) | `… localdb query jiangliushi666 --since 1d` | exit 0;**messages=0**(尝试前后各查一次同结果) | ✅ 如实:零落库(与零出站一致) |
| M3 | 防重:同参立即重发应拒 | 同 M1 全参重跑一次 | **exit 1 `send_direct_disabled`**(确定性再拒);**全库零新行**:jl666 全窗 0 行、filehelper 最新行仍=10-14 21:49:39;send_state fingerprints={} 恒空、last_send_epoch 未动 | ⚠️ 等价拒绝成立(更早的 fail-closed 门,连占位都未发生);**但防重路径本体未被演练**(无成功发送可撞 120s 窗)——如实记「未按设计形态运行」 |
| M4 | OCR 链共存:send_text 常规通道 dry-run | `printf '嘻嘻' \| … send_text filehelper --file - --dry-run` | **exit 0 绿**:channel=cgevent_ocr,navigated/pasted=true,readback=clipboard_copy,title_verify=ocr,dry_run=true,sent=false,elapsed 28445ms;send_state 零写入 | ✅ 两通道并存无扰动 |

补充(非矩阵项,仅佐证"码在、门逻辑单测绿"):离线定向单测
`uv run --no-sync python -m pytest tests/wechat-bridge/test_send_direct.py -q`
= **40 passed**(0.22s;`/tmp/wxsend-e2e/supplementary-offline-test.txt`)。
此为离线桩测试,**不替代** M1/M3 的真机判定。

## 阻塞定性(为何直发无法真发;三级门全数在挡)

1. **P-0 主人裁决门未过**(design-阶段3 §4:预算终裁+串构造判例翻案;
   「任何验证发送前未得裁决=不发」)。
2. **配置门关**:`send_direct_enabled` 缺省 false,design-阶段3 §3.2 明定
   「主人显式开启才生效」——验证员开启=越权,不做。
3. **锚定表缺位**:r4 钉入轮(P-1,主人手发触发)从未执行,send_entry/
   服务对象活性锚全套无产物——伪造锚定表=伪造验证,绝不为之。

## 预算账(本矩阵)

验证员真实出站 **0 条**(M1/M3 均于配置门确定性拒绝,未达 armed/expr/
attach 任何阶段);白名单预算 2 条分毫未耗。全库零新行、send_state 零写入。

## AC 对账(白名单双发条=prd.md AC3)

**不予勾选**。AC3(白名单双发真验证)的达成前提=直发通道可真实出站,
而三级门(P-0 裁决/配置门/锚定表)全数未过——直发 0 条、双发 0/2、回执
双通道未演练。按「失败如实、绝不伪造」纪律,AC3 维持未勾,待 P-0 裁决
→ r4 钉入轮产出锚定表 → 主人开配置门后重跑本矩阵。

## 证据清单(/tmp/wxsend-e2e/)

`run-context.txt`(前置态)、`m2-baseline-jl666.{json,summary.txt}`、
`baseline-filehelper.{json,summary.txt}`、`m1-send-direct-jl666.{json,stderr}`、
`m3-resend-jl666.{json,stderr}`、`m2-post-jl666.json`、`m2-m3-run.txt`、
`m3-post-filehelper.json`、`m3-post-filehelper.rows.txt`、
`m4-send-text-dryrun.{json,stderr}`、`supplementary-offline-test.txt`
