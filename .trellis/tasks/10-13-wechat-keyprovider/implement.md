# Implement:微信取钥外置化(真数据先行)

> 硬门禁(AC-A0):Phase A 三项验收全勾才准开 Phase B。Phase A 任一失败 → 回攻坚档(10-13-wechat-key-crack)换路线,本档 Phase B 顺延,不做「先写代码等钥匙」。

## Phase A:真数据到手(需要主人一个 30 秒窗口)——✅ 10-13 全勾,门禁已过

- [x] A1 **LLDB 取钥实战**:一键件=/tmp/wxkey-c/{lldb-run.sh,lldb-shot.sh}(osascript 提权弹密码框→蓝本四级链→断点 CCKeyDerivationPBKDF x2==32→主人重登触发→命中读 x1 32B→自动 detach)。**11:22 一击命中**。工具已固化 tools/。
- [x] A2 **派生+验真**:蓝本派生循环 20/20 salts 全中(页 1 HMAC 逐库验真,同 verify3 协议)。
- [x] A3 **通电**:keys.json 20 钥落数据根私有区(`~/Library/Application Support/MYIA/wechat-localdb/keys.json`,600/目录 700——注意 macOS 缺省数据根是 Application Support/MYIA 非 ~/.myia);桥 E2 解密副本 404MB 四库;TMS 群 9745 条真消息在库。E3 查询适配 bug 见 B0。
- [x] A4 **门禁判定**:A1-A3 全勾 → Phase B 解锁(10-13 记档)。

验证命令:`python3 .trellis/tasks/10-13-wechat-key-crack/research/tools/verify3.py <db> <key>`;`~/.myia/plugins/wechat-bridge/bin/wechat-bridge localdb query <chat> --since 3d`

## Phase B:取钥器外置化(A4 已解锁)

- [ ] **B0(新增,首项)·桥 E3 查询适配 4.1.15 修复**:localdb_query.py 表签名识别两处漂移——①`Msg_<md5>` 分表无会话列(会话=表名,md5(username),Name2Id 表在 message 库可反查+real_sender_id 由此解析);②内容列候选族缺 `message_content`。补列候选+无会话列表的表名反解;负例守卫(压缩列 WCDB_CT_* 的 zstd 内容不误读)。修后 `localdb query 50438708676@chatroom --since 3d` 必须回真消息。
- [ ] B1 协议文档 `docs/wechat-keyprovider.md`(§2 契约全量+取钥器作者视角示例+错误码表)→ AC-B5
- [ ] B2 桥·配置与管理命令:`config.py` 新键 `key_provider_path`;`cli.py` 增 `localdb key-provider set|get|clear`(set 校验存在+可执行)——pytest 桥套件
- [ ] B3 桥·provider 调用:`localdb.py` keys 缺失分支 → spawn(stdin 单行 JSON/NDJSON 解析/120s 超时 kill/退出码语义)→ 页 1 HMAC 验真 → keys.json;失败 exit 21 语义不变——含假取钥器(超时/无 result/垃圾钥)四负例测试 → AC-B4
- [ ] B4 参考取钥器 `plugins/wechat-bridge/examples/keyprovider_ref.py`(读钥匙缓存+协议包装,零扫描逻辑)→ AC-B4
- [ ] B5 设置页:微信/桥分区「取钥器」行(路径输入+三态:已配/未配/文件缺失;未配置引导文案)——vitest+tsc → AC-B1/B2
- [ ] B6 守卫与门禁:src/ grep 守卫(task_for_pid|mach_vm|vm_read|ptrace 零新增);全量 pytest/vitest/tsc/cargo;`gitnexus detect-changes --scope staged` → AC-B3/B6
- [ ] B7 装机包:重打包+静默换装+像素级验证(截屏+OCR:新配置项三态+未配置报错态)→ AC-B7
- [ ] B8 spec 更新(`.trellis/spec/` 对应层写入协议契约纪律)+ finish-work

## 回滚点

- 桥:组件版本回退+config.json 新键删即回现状(缺省空=旧行为)。
- 设置页:新行独立提交,可单独 revert。
- Phase A 产物(passphrase/keys.json)只在数据根私有区,删除即清。

## 执行方式

- Phase A=主会话亲自操刀(需要主人配合窗口+红线敏感,不派子代理)。
- Phase B=trellis-implement 子代理分步派发(dispatch 首行 `Active task: .trellis/tasks/10-13-wechat-keyprovider`),每步过 grilling 拷问,门禁红了先修再进。

## 复核发现与处置(2026-10-13 落档)

> 两轮审计 + 本轮文档侧复核的全部发现,逐条处置状态。**独立复核证据**:
> [`research/e2e-provider-verify.md`](research/e2e-provider-verify.md)
> (独立验证员真数据全链,E2E 七步全绿,verifiedCount=20——1 至 6 号步骤含
> keys 缺失态/spawn+NDJSON/HMAC 验真+缓存/真消息+zstd 独立比对/负例×2/换号语义)。

### 第一轮审计(代码侧审计→对方 phase4 修复)

| 发现 | 处置 |
|---|---|
| 1 high | **已修复**(对方工作流 phase4;修复后 E2E 复核全链绿为旁证) |
| 3 medium | **已修复**(同上;E2E 负例×2 零缓存污染+换号语义如实,与修复口径吻合) |

明细以对方(代码侧)phase4 交付为准,本档不重复展开;仓内未见独立审计明细档,
上表分类与处置结论按本任务指令如实记录。

### 本轮发现与处置(zstd/TTL/低危四件 + 换号实弹暂缓)

| # | 发现 | 处置 |
|---|---|---|
| 1 | zstd 解码装机面恒占位(自管 3.12 无 stdlib `compression.zstd`) | **已修复**(代码侧):两级 import 链 stdlib→pip `zstandard`(0.4.3 主依赖,commit f51d5ac);装机态真跑 TMS 群 50 条,zstd_available=True/zstd_decoded=28;E2E 独立比对 5/5 一致(research/e2e-provider-verify.md 步骤 4) |
| 2 | TTL=0 语义(0 是否=永不过期) | **终局=0=永不过期已四面落地**(后续同日 fix 轮翻转)。本档初记轮结论曾为「未落地、0 非法」;后续(同日 fix 轮)已改代码语义:**0=永不过期四面落地**——config 校验改非负整数(0 合法,`config.py:233-246`,报错文案「0 = 永不过期」)、localdb fresh 判定 0 短路(`localdb.py:1061`,陈旧副本恒新鲜跳过重建)、README 键说明改写(`plugins/wechat-bridge/README.md:40`「非负整数,0 = 永不过期;负数拒」)、test_config 正例(0 合法,`test_config.py:78-83`)+负例(-1 拒,`:141`)与 test_localdb_copy「拨回一年仍 kept」专测(`test_localdb_copy.py:106-115`)。`copy_capacity_mb` 维持正整数(0 容量无合法语义)。初记轮的旧行号引用(config.py:235/test_config.py:127/localdb.py:998-1001)随翻转作废,以本行现位行号为准 |
| 3 | 低危·回滚陷阱(桥回滚旧版遇未知键全桥拒载) | **已处置(文档)**:协议文档 §10 补「回滚注意事项」——回滚到不认识 `key_provider_path` 的版本(0.4.2 前)须先 `localdb key-provider clear`,否则 config.json 残留键令旧版桥 exit 2 全拒载(`config.py:190-197` 键封闭装载) |
| 4 | 低危·换号指引缺口(cache-read 形态换号后无运维指引) | **已处置(文档)**:协议文档 §7 补「换号后怎么办」——桥端行为(HMAC 全拒+exit 21+重取指引+缓存整体覆写)+ 两形态对号(cache-read=手动更新钥匙文件;passphrase-derive=passphrase 来源新鲜即天然闭环) |
| 5 | 换号实弹验证 | **主人明令暂缓**,不入本轮验收;协议语义面已有等价证据(E2E 步骤 6:错误 passphrase→HMAC 0/20 全拒+「重取后重试」+零缓存污染) |
| 6 | 源新即重建(0.4.4) | **已实装+本轮补档**——动机:10-13 实况副本 11:47 恒新鲜到次日、下午消息全盲区(TTL 内副本不重建,新消息不可见);实装 `_source_newer`(`localdb.py:960-1027`:主库+`-wal` mtime 对比副本,源消失保持既有副本不炸);测试锄4个(源新重建/`wal` 新重建/TTL=0 关闸/源消失保持,`test_localdb_copy.py:121-184`);版本 bump 五处(component.json/pyproject/`__init__.py`/test_pyenv_resources.py/golden_cli_payloads.json,0.4.3→0.4.4);trade-off 如档:微信活跃期重建频率上升、TTL 摊薄实质弱化。文档同步(整改轮补):README E2 生命周期段、design G5 语义扩展注记(10-11 归档档) |

### 附加交付(主人点名:版本基线)

- **微信版本基线档**:[`research/wechat-version-baseline.md`](research/wechat-version-baseline.md)
  ——实读 4.1.15(构建 270135);基线表(DB 路径形态/钥与 passphrase 位置/派生协议
  参数/4.1.15 表形态/未重签名 attach 实锚)+ 版本漂移对照(一条 `defaults read`
  对照命令 + 「版本变了最先失效什么」清单:passphrase→重跑 lldb-shot SOP;表结构→
  B0 适配重验;压缩形态→zstd 链重验)。
- 协议文档 §11「版本基线(SOP)」小节同步:当前验证版本 + 指到基线档 + 对照命令。
