# wechat-bridge — 微信本机桥(UI 自动化 + 本地库只读)

受管组件(task 10-11-wechat-ui-bridge,G7 命名):管「当下收发」的 **UI 自动化桥**(macOS AX 先行,Windows wxauto 备胎另启)+ 管「历史与全量」的**本地库只读通道**。不破解协议、不碰微信进程内存,外部件走受管组件链路。

- 设计与契约:`.trellis/tasks/10-11-wechat-ui-bridge/design.md`(CLI §6 / 配置 §7 / 测试 §8)
- 组件戳:`component.json`(版本 + 适用微信版本范围,真锁惯例 design §4)
- MYIA 侧接入:push 通道 `weixin-local`(Phase F;`weixin` 通道名保持归官方 Hermes 桥 `src/myssia/push/weixin.py`,该文件是本桥调用形态的蓝本)

## 运行形态

一次性子进程,stdout 恒单个 JSON 对象,exit 三段语义(0 成功 / 1 通用失败 / 2 用法;失败段按 §6 细化码值):

```console
~/.myia/plugins/wechat-bridge/bin/wechat-bridge --probe          # 装机形态(下同;bin 启动器自选 Python ≥3.11)
python -m wechat_bridge --probe                        # 开发形态(组件根上直跑;三态探针 ok/degraded/bridge_unavailable)
python -m wechat_bridge sessions list --json           # 会话列表(Phase C1)
python -m wechat_bridge messages read <id> -k 50       # 最近 K 条文本(Phase C2)
python -m wechat_bridge send_text <id> --file -        # 正文经 stdin(G6 硬频控;Phase D)
python -m wechat_bridge localdb query <chat> --since 7d --json   # 本地库只读(Phase E)
python -m wechat_bridge localdb key-scan --json        # 内存密钥批处理扫描(D4 豁免;默认关+须提权+只读单遍)
```

`bin/wechat-bridge` = 装机启动器(纯转接,零业务逻辑):解析组件根 → 按
`MYIA_WECHAT_BRIDGE_PYTHON` env > `<数据根>/python/bin/python3`(MYIA 桌面
自管环境)> PATH `python3` 的序选首个 **Python ≥3.11**(component.json
requires),exec `python -m wechat_bridge`;stdout 恒单 JSON 由桥包保证,
启动器失败只写 stderr + exit 2。MYIA 侧消费点即此 bin
(`myssia.push.weixin_local.DEFAULT_BRIDGE_BIN`)。

## 落点与配置

- 组件源码(本目录)经受管链路落在 `~/.myia/plugins/wechat-bridge/`(design §1);MYIA 侧 `wechat_bridge_bin` 可覆写路径(Phase F)。
- 桥配置:`<数据根>/wechat-bridge/config.json`(全部有缺省、**缺文件可用**,design §7):`domains`(G4 三域)、`limits`(AC2 参数化)、`copy_ttl_hours`/`copy_capacity_mb`(G5)、`mem_search_enabled`(D4 豁免开关,**缺省关**;显式开启 + 提权才生效)。**无频控键**(G6 硬编码:单条、间隔 ≥10s、无批量、不可配置)。
- 频控状态:`<数据根>/wechat-localdb/send_state.json`(flock 防并发,design §2)。
- 外部密钥(D4 裁决②):`<数据根>/wechat-localdb/keys.json`(600 权限;键 = 相对 `db_storage` 的库路径,值 = 该库 64-hex SQLCipher 密钥)。与组件密钥缓存**同位同权**:`localdb query` 消费前逐条 page1 HMAC 重验(`resolve_keys`),全量命中即一步闭合;密钥与库不匹配(如登录态轮换)如实 exit 21 并指明 keys.json 未命中。

## 能力边界(Phase E 已落,E1 实测负结论如实)

- `--probe` 真实现:三态判据矩阵(design §2)照跑——进程/版本/AX 权限/主窗口/本地库落盘/密钥缓存,全只读零前台扰动;微信托盘态如实 `degraded(window_closed)`,进程不在如实 `bridge_unavailable`。
- UI 子命令(sessions/messages/send_text):前置检查门真跑(§6 码序 fail-fast),实现层落位 Phase C/D,未落地时结构化应答 `not_implemented`(exit 1 过渡码,不谎报 §6 具名族)。
- `localdb query`(Phase E,已落地):定位 db_storage → E1 密钥获取(零内存途径=key_info.db 材料→候选提取→page1 离线 HMAC-SHA512 校验,机制完整可单测)→ E2 sqlcipher 解密副本至 `<数据根>/wechat-localdb/decrypted/`(600/700 权限,TTL 24h+容量上限,失败重建)→ E3 message/session/contact 三域只读查询(列签名自适应,版本漂移如实降级)。**E1 实测结论(2026-10-11 真跑):零内存密钥途径不可推导**(候选全数 HMAC 未命中,与三方独立公开实测一致)→ 如实 `key_unavailable`(exit 21)+ D4 待主人裁决;密钥可得(外部引入或 D4 豁免后)即全链闭合。
- `localdb key-scan`(D4 豁免执行件,主人 2026-10-11「全部解决」令):内存密钥批处理扫描——只读 vm_read 类系统调用(`task_for_pid`/`mach_vm_region`/`mach_vm_read_overwrite`)单遍遍历可写私有区 → 32 字节滑窗候选 → 复用 E1 校验器对 page1 离线 HMAC 校验 → 全量命中才落 `keys.json`(600,`localdb query` 一步闭合)。**三重门**:配置 `mem_search_enabled: true`(缺省关)+ root 提权 + 主人裁决在案;预算(单区 64MB/总 256MB)为模块常量;禁写内存/禁注入/禁调试器附加/禁重签名,守卫测试钉死。如实预告:微信为 hardened runtime 签名,root 亦可能被内核拒(`task_for_pid` KERN_FAILURE)——该拒绝即此路在本机不可达的如实信号。
- 频控落盘模块(G6)已实现并可单测(时间注入,不真等 10 秒)。
- 依赖:sqlcipher CLI(`brew install sqlcipher`,design §5.1 前置;缺装时解密步骤结构化报错并给指引)。

## 红线(违者返工)

1. 静默后台:不抢前台焦点、不合成鼠标点击、不激活微信窗口;UI 侧只走 AX 通道。
2. 不破解协议:禁逆向、禁 hook 注入;内存密钥搜索默认关,仅 D4 豁免后配置显式开启 + 提权才生效,且只读 vm_read 单遍零常驻、禁写内存/禁注入/禁调试器附加/禁重签名。
3. 私有数据:聊天内容/密钥材料不入 git/日志/报告;证据只留形状。
4. 依赖纪律:临时依赖一律独立 venv,勿入仓库 `.venv`。

## 测试

```console
uv run --no-sync python -m pytest tests/wechat-bridge -q      # 全 mock,CI 全绿
MYIA_WECHAT_E2E=1 uv run --no-sync python -m pytest tests/wechat-bridge -q  # 加跑真机探针(design §8)
```
