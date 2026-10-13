# Design:微信取钥外置化(真数据先行)

## 0. 现状盘点(2026-10-13 实锚)

| 件 | 位置 | 现状 |
|---|---|---|
| MYIA 引擎 | `src/myssia/engines/wechat_local.py`(823 行) | 子进程调桥;桥 exit 21 key_unavailable → 结构化 skip |
| 桥组件源码 | `plugins/wechat-bridge/`(component.json+pyproject+native/collector.c) | 装于 `~/.myia/plugins/wechat-bridge`;`localdb query`/`localdb key-scan`(内置三模式扫描+sqlcipher 试开+页1 HMAC 验证)/config.json(含 mem_search_enabled) |
| 仓内编排脚本 | `scripts/wechat-bridge-d4-keyscan.sh`(310 行) | sudo 一键:setuid 自愈件安装+扫描编排 |
| 攻坚工具链 | `.trellis/tasks/10-13-wechat-key-crack/research/tools/` | collector5/verify3/run5(研究件);蓝本 `/tmp/wcdb_key_tool_macos.py` 在位 |
| 配置 | `config/weixin.yaml`(localdb 块)+ 桥自有 config.json | 引擎零取钥逻辑,取钥全在桥侧 |

**与 WeFlow 模式的差距**:WeFlow=取钥器是用户自备外部可执行件,协议通用(stdin JSON/stdout NDJSON),应用对实现零知识;MYIA 现状=取钥锁死在桥内置 key-scan(三模式扫描)+ 仓内 sudo 编排脚本,**不可换、协议不通用**。

## 1. 目标形态

```
┌─ MYIA 设置页 ──────────────┐
│ 微信分区 →「取钥器」路径配置 │──┐
└────────────────────────────┘  │ 写入(经桥管理命令)
                                 ▼
┌─ wechat-bridge(外部组件)──────────────────────────┐
│ config.json: key_provider_path                      │
│ localdb query → keys.json 缺/失效?                  │
│   ├─ key_provider_path 已配 → spawn 取钥器子进程    │
│   │    stdin: {"action":"get_db_key",...}          │
│   │    stdout: NDJSON progress…+result(keys map)   │
│   │    → 页1 HMAC 验证 → 落 keys.json → 继续查询    │
│   └─ 未配/失败 → exit 21 key_unavailable(现状语义)  │
└─────────────────────────────────────────────────────┘
```

取钥器本体=任意可执行文件(LLDB 版/内存扫描版/读缓存版/未来的 chatlog 包装),桥不校验来源签名,不内置降级。

## 2. 取钥器协议 v1(照 WeFlow keyProviderService 适配 4.1 多钥现实)

**请求**(桥→取钥器 stdin,单行 JSON,写后关 stdin):
```json
{"action":"get_db_key","db_path":"/abs/path/to/db_dir","account_id":"wxid_xxx"}
```

**响应**(取钥器→桥 stdout,NDJSON 按行):
```json
{"type":"progress","message":"人类可读进度","level":0}
{"type":"result","success":true,"keys":{"<salt_hex>":"<key_hex>",...},"account_id":"wxid_xxx","logs":["..."]}
{"type":"result","success":false,"error":"人话错误","logs":["..."]}
```

- `progress` 0..N 次;`result` **恰一次**,即终态。
- `keys` = `{salt_hex: key_hex}` map(**与 WeFlow 单 key 的关键偏离**:微信 4.1+ 每库独立密钥,攻坚档实锚;单 key 形态的旧取钥器可用 `"*": "<key_hex>"` 通配键表达「全域同钥」,桥侧兼容两形态)。
- 退出语义:退出码非 0=失败;**退出码 0 但无 result=失败(「未返回结果」)**;超时 120s 桥 kill=失败。stderr 收尾 500 字符附错误信息。
- 所有权:取钥器**不写 keys.json**(桥独占写,验真后才落);取钥器无状态、可任意实现。
- 校验:桥对返回的每个 key 跑页 1 HMAC 离线验证(复用桥内既有验证器),验不过=该 key 弃用,如实计入 result 日志。

## 3. 挂点与改动面

| 面 | 改动 | 文件锚 |
|---|---|---|
| 桥·配置 | config.json 新键 `key_provider_path`(缺省空=现状行为) | `plugins/wechat-bridge/wechat_bridge/config.py` |
| 桥·管理命令 | `wechat-bridge localdb key-provider set <path>|get|clear`(set 校验文件存在+可执行) | `cli.py` |
| 桥·调用点 | keys 缺失时按 §2 协议 spawn;成功验真落 keys.json,失败 exit 21 | `localdb.py` |
| 设置页 | 微信/桥分区新增「取钥器」行:路径输入+状态(已配/未配/文件缺失);未配置引导文案指协议文档 | 前端设置屏 + Rust 配置面(经桥管理命令,不直写桥 config.json) |
| 协议文档 | `docs/` 新件,第三方照写零歧义(请求/响应/退出码/超时/多钥/通配/示例) | `docs/` |
| 参考取钥器 | 读 keys 缓存+协议包装的示例实现(无扫描逻辑,可入仓作 example) | `plugins/wechat-bridge/examples/` |
| 引擎 | **零改动**(取钥闭环在桥内;exit 21 语义不变) | `wechat_local.py` 不动 |

## 4. 决策点(主人过目)

- **D1·扫描件留仓与否**:桥内 memsearch.py+native/collector.c 已在公开仓。全 WeFlow 纯度=外迁出仓(只留协议)。**推荐:本任务不动**(已公开、单用户工具、迁移收益<搅动成本),立冻结线:新的扫描能力不再进仓,后续取钥器开发在仓外。可翻案。
- **D2·编排脚本去留**:`scripts/wechat-bridge-d4-keyscan.sh` 在 provider 就位后降级为「桥内置扫描的旧入口」,保留不动(零风险),README 指向 provider 为正解。

## 5. 红线与风险

- Phase A LLDB=瞬时断点干预,仅限主人配合窗口(30 秒重登);会话日志与钥匙只落数据根私有区。
- 桥写 keys.json 前必过页 1 HMAC 验真(防取钥器返回垃圾钥污染缓存)。
- 回滚:桥组件版本化管理,config.json 新键缺省空=完全回退现状行为;设置页新行可独立隐藏(配置面灰度)。
- UI 文案守判例:「取钥器」上屏,协议 JSON 字段保留英文;错误文案人话(「未配置外部取钥器,请在设置中指定可执行文件路径」)。
