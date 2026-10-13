# 微信取钥外置化:真数据先行,后代码落地

## Goal

照 WeFlow 模式(hicccc77/WeFlow,15023★,`docs/third-party-components.md` + `keyProviderService.ts`)把微信桥的取钥面外置为可插拔件:设置页配取钥器可执行文件路径,桥按子进程协议调用;MYIA 本体(src/ 产品代码)**零取钥实现**。

**硬门禁(主人 2026-10-13 令,最高优先约束):必须先获取微信真数据,再用代码落实到项目中。** Phase A(真数据)验收不过,Phase B(代码落地)不准开工。

## 背景与动机

- 微信 4.1.13+ 内存密钥字面量撤除,社区全部现成工具同版本全灭(攻坚档 crack-roadmap.md 已固化);取钥唯一活路=LLDB 符号断点(GATE 候选③,主人已口头允+今日「先拿数据」指令构成实施授权)。
- WeFlow 的生存架构:应用本体干净,风险件(内存扫描取钥器)用户自备、仓外分发——ylytdeng/wechat-decrypt 被 DMCA 而 WeFlow 活着,是可复制判例。
- MYIA 开源仓(xinzhuzi/myia)同理:产品代码不进货取钥扫描实现。

## Requirements

### Phase A:真数据到手(先做,硬门禁)

- A-R1 用 LLDB 路(蓝本 TANGandXUE `/tmp/wcdb_key_tool_macos.py`,符号 `CCKeyDerivationPBKDF`,条件 `$x2==32`,`preload-symbols false`)捕获 4.1.15 的账号级 passphrase。
- A-R2 passphrase → PBKDF2 派生全库 enc_key(keys map)→ `verify3.py` 逐库验真。
- A-R3 `localdb query` 真跑,message_0.db 至少一库返回真实消息记录。
- A-R4 过程红线:只读、瞬时断点(读寄存器即拆)、密钥材料只落数据根私有区;LLDB 窗口需要主人 30 秒配合(微信内退出登录重扫码)。

### Phase B:取钥器外置化(过门后才做)

- B-R1 协议契约:外部可执行文件,stdin 写一行 JSON 请求 / stdout 按行 NDJSON 响应;动作 `get_db_key`(本期唯一必选);未配置/找不到可执行文件=人话报错,**无降级实现、不校验来源签名**(WeFlow 原样)。
- B-R2 设置页:微信/桥配置区新增「取钥器路径」配置;未配置态给引导文案。
- B-R3 桥调用面:localdb 引擎在钥匙缓存缺失时经 provider 子进程取钥;已有 keys.json 缓存路径保留(不强制走 provider)。
- B-R4 协议文档落 docs/,写到第三方照着能实现的粒度(CLI 契约/错误码/超时语义/JSON 字段)。
- B-R5 我方参考实现=组件内 example 件(`plugins/wechat-bridge/examples/keyprovider_ref.py`,零扫描逻辑,只读钥匙文件+协议包装)。~~不进 src/、不进装机包~~(10-13 收官修正:组件=整目录装机形态,example 随装;件本身零扫描零 DMCA 实质风险,design §3「可入仓作 example」在案)。**内存扫描版取钥器永不入仓不变。**

## Acceptance Criteria

### Phase A(硬门禁验收点)

- [x] AC-A1:passphrase 捕获到手,LLDB 会话日志留档(断点命中+寄存器读值)。(10-13 11:22,蓝本四级链+osascript 提权一键件,日志 /tmp/wxkey-c/lldb-extract.log 600;passphrase 落 ~/.wcdb-key-tool/wechat-passphrase.json 600 属主已归还)
- [x] AC-A2:keys map 逐库验真全绿。(**20/20 salts 全中**:message_0(346.6MB)/message_fts(126.5MB)/contact/session/sns/favorite/emoticon 等 20 库,蓝本派生循环内逐库页 1 HMAC 验证,与 verify3 同协议)
- [x] AC-A3:真数据到手。桥 E2 解密副本产出 404MB(message/session/contact/biz 四库,domains 全 ok),probe 全绿(localdb_key: ok);直查明文副本:TMS 群(50438708676@chatroom)Msg 表 9745 条,当日 32 条实时在流,文本消息可读。**注:桥 `localdb query` E3 适配层对 4.1.15 返回 0 条——表签名识别要求会话列而 4.1.15 分表无此列(会话=表名 md5)+内容列名 message_content 不在候选族;根因已明,修复=B0(Phase B 首项)。**
- [x] **AC-A0(总门禁):A1-A3 全勾 → Phase B 解锁(10-13)。**

### Phase B

- [x] AC-B1:设置页可配置取钥器路径,保存/读取/校验存在性。(WeixinAccountCard 三态徽标+路径输入;拷问揪出 Rust 载荷形状断裂已修,真实形状对账用例 provider_state_bridge_real_get_output 在案)
- [x] AC-B2:未配置时——设置页显示引导文案;桥取钥调用返回人话错误(含「未配置外部取钥器」字样),无静默降级。(23 例桥测试含四负例)
- [x] AC-B3:src/ 零取钥实现:grep 守卫绿(工作流 world.run 实跑,src/ 零命中)。
- [x] AC-B4:参考 provider 按协议跑通 `get_db_key`。(假取钥器对夹具库正例+四负例全绿;真钥端到端随 AC-B7 装机验)
- [x] AC-B5:协议文档 docs/wechat-keyprovider.md 落地(全量验真门槛/行序硬约束/实现注/管理命令/walkthrough;收官补:多条 result 取首条实现注+progress 不透传披露+绝对路径要求)。
- [x] AC-B6:门禁全绿(pytest/vitest/tsc+ruff/cargo 五门禁二轮全绿,工作流 world.run 实跑)+ detect-changes 主会话收官跑。
- [ ] AC-B7:装机包刷新+像素级验证(设置页新配置项+未配置报错态,截屏+OCR 证据)。

**已知限制(如实)**:zstd 压缩消息真解码需 Python ≥3.14(PEP 784);装机态数据根自管 python=3.12.7 → 压缩行落占位并如实计数(zstd_module_missing);escape hatch=$MYIA_WECHAT_BRIDGE_PYTHON 指 3.14 即全解码(开发态 .venv 3.14 实测 28/28 解码)。自管 python 升 3.14=主人架构裁决域,本任务不擅动。

## Constraints

- 红线不变:零微信进程干预(LLDB 瞬时断点=唯一例外,仅限 Phase A 窗口);密钥材料只落数据根私有区。
- DMCA 洁净:产品代码/装机包不包含内存扫描取钥实现;攻坚档 research/tools/ 既有研究件维持现状不再扩散进产品路径。
- 词汇守 UI 文案判例:配置项名用「取钥器」或「密钥获取工具」,协议名/JSON 字段保留标准英文术语。

## Out of Scope

- 媒体解密插件、批量导出引擎两个 WeFlow 缝(对 MYIA 无场景)。
- WCDB 读取库外置(localdb 开库=标准 sqlcipher 用法,留仓内)。
- 自动内存扫描版取钥器(攻坚档另线;本任务参考实现只做「缓存钥匙+协议包装」)。
