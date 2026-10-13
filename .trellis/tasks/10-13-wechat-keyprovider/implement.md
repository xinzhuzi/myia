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
