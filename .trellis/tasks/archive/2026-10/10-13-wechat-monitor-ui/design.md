# Design:微信监控 UI(取钥-解密-情报流全链界面)

## 0. 总形(三个面,零新画布)

```
┌ 设置·配置·微信(WeixinAccountCard 扩展)──────────────┐
│ 桥三态灯(既有)                                        │
│ 密钥状态行:● 已就绪 20 库 · 10-13 11:22 [获取密钥]    │
│ 取钥器路径配置(B5 既有)                               │
└───────────────────────────────────────────────────────┘
        │ 点击「获取密钥」
        ▼
┌ 获取密钥流(卡内三步面板,非独立屏)───────────────────┐
│ ① 确认:将弹出系统密码框;请在微信里退出登录再扫码一次  │
│ ② 进行:等待密码 → 正在挂载 → 等待重新登录 → 验证 N 库 │
│    (progress 事件实时;取消钮随时可用)                │
│ ③ 结果:20 库解密就绪 / 失败人话+重试                  │
└───────────────────────────────────────────────────────┘

┌ feed·微信 3 级监控台(既有骨架内容化)────────────────┐
│ 右栏·监控群列表:                                      │
│   ● TMS 中转站交流    监控中 · 最新消息预览 · 5 分钟前 │
│   ● AI中转站-♾️AI Token 监控中 · …                    │
│   ○ 某群              密钥缺失 [去获取密钥]           │
│   [去配置监控群 →]  (跳既有 YAML 编辑屏;grill 决议④   │
│    一期零写面,不与数据源侧会话双写 weixin.yaml)       │
│ 左栏·选中群消息时间线(**只读**,复用 TG 三级版式,微信绿;│
│  无发送面——发送走推送屏的官方通道,grill 决议⑨)        │
└───────────────────────────────────────────────────────┘
```

## 1. 数据契约(三新增,全部只读/形状级)

### 1.1 密钥状态(桥侧新只读命令 `localdb key-status --json`;grill 决议①三态化)

```json
{"state": "ready" | "stale" | "missing",
 "db_count": 20, "acquired_at": "2026-10-13T11:22:00+08:00",
 "wechat_version": "4.1.15",
 "verdict_note": "抽样 3 库页1 HMAC 重验通过" }
```
- 三态真源:missing=keys.json 缺位;**stale=文件在场但抽样页1 HMAC 重验失败**(微信版本变化后失配——probe 的零成本判据只看文件在场会撒谎,故本命令自带抽样重验,1-3 把/次秒级);ready=在场+抽样过。UI 词:已就绪/已失效/未获取。
- `acquired_at`=keys.json **文件 mtime**(零格式变更;cache 不加元数据键,「键=库相对路径」消费方零破坏)。
- **钥内容永不出现**(db_count/时间戳=形状级证据,判例同攻坚档)。

### 1.2 取钥进度事件(Rust 壳→前端,Tauri event)

- 事件名 `wechat-key-acquire`(payload 见 §3.3);阶段枚举 `password → attach → wait_relogin → derive → done | failed | cancelled`。
- 真源=取钥器 provider 的 stdout progress 行(协议既有),桥透传给壳(§2),壳转 event——**应用零取钥实现,只转译进度**(AC-B3 零取钥守卫延续)。

### 1.3 监控群列表(零新后端:前端从既有面拼装;grill 决议⑤废拍脑袋阈值)

- 群列表=weixin 品类源清单(源名 `weixin-<群显示名>` 前缀律)+ 每源 feed 最新一条(items 查询 source 精确等值,既有 list_items 面)。
- 每群状态=**源级最近 run 的 skip_reason 映射 + 源健康度既有判据域**(feed 源健康度 ok/degraded/unk 词表复用,不新造「24h 安静」规则):无 skip=监控中;`key_unavailable`=密钥缺失;健康度域承载其余降级态。

## 2. 取钥编排链(协议 v1.1:交互式取钥器超时放宽;grill 决议②③⑥⑪)

现状缺口:协议 v1 超时 120s 硬帽,重登是分钟级人操作。

- **协议 v1.1**(向后兼容):请求新增可选字段 `"timeout_hint_seconds": <int>`;桥取 `clamp(timeout_hint, 120, 1800)` 为该次硬帽(**上限帽 1800s 防取钥器乱报**)。取钥器可据此自整等待窗。文档 docs/wechat-keyprovider.md 同步 §。
- 编排路径:UI「获取密钥」→ Rust 命令 `wechat_key_acquire`(desktop/src-tauri/src/wechat_keyprovider.rs 扩展,与 B5 同文件同风格)→ spawn 安装态桥 `localdb key-acquire --json --force --timeout-hint 600`(**--force 旗标:默认走缓存短路返回 ready;force=跳过缓存直走 provider——「重新获取」场景钥匙失效但缓存文件在场,不 force 永远空转**)→ Rust 把 progress 行转 Tauri event → 前端三步面板。壳侧兜底帽 900s(>hint,防桥自身超时后壳挂死)。
- **取消=哨兵文件机制(grill 决议③,root 段杀不动是硬事实)**:取消时 Rust ①kill 用户态链(桥/provider 用户态段)②落 `<数据根>/wechat-localdb/cancel.keyacquire` 哨兵;部署件主循环每 2s 轮询哨兵,见即自杀+内建孤儿清理(pkill lldb,攻坚档既有)+删哨兵。最迟自清窗=其 timeout(600s)。AC2 按此验收。
- **取钥器(交互式 LLDB 件)=外部部署件**:源码=攻坚档 tools/(lldb-shot.sh/lldb-run.sh 已固化),部署到 `<数据根>/wechat-localdb/bin/keyprovider-lldb.sh`(一次性安装,不进 git 仓不进组件——D1「新扫描能力不进仓」判例延续);设置页取钥器路径指向它。蓝图 wcdb_key_tool_macos.py(TANGandXUE)随部署件携带,归属注释保留。
  - 适配:v1.1 化(吃 stdin 协议请求→弹密码(osascript)→通知重登→**哨兵轮询**→命中→派生→stdout NDJSON:progress 各阶段+result keys map)。现 lldb-shot.sh 是裸编排,包装层 ~80 行 python。

## 3. 改动面

| 层 | 件 | 改动 |
|---|---|---|
| 桥(python) | localdb.py / cli.py | `key-status` 三态只读命令(抽样重验+mtime);`key-acquire` 编排命令(--force/timeout_hint/哨兵轮询透传);progress 透传 |
| 协议文档 | docs/wechat-keyprovider.md | v1.1 节(timeout_hint clamp 120..1800 语义+交互式取钥器指引+哨兵约定) |
| Rust 壳 | wechat_keyprovider.rs | `wechat_key_acquire`(--force/--timeout-hint 透传,壳帽 900s)+`wechat_key_status`;事件发射;取消=杀用户态链+落哨兵文件 |
| 前端·设置 | weixin-account-card.tsx | 密钥状态行+三步获取面板(卡内,非新屏) |
| 前端·feed | feed-screen.tsx(3级监控台段) | 群列表右栏内容化(只读)+「去配置监控群」跳 YAML 编辑屏+密钥缺失引导跳转 |
| 前端·api | settings/wechat-keyprovider-api.ts | acquire/status client+事件订阅 |
| 数据根部署件 | wechat-localdb/bin/keyprovider-lldb.sh | 外部取钥器(源在攻坚档 tools/,安装=一次性 cp+chmod;内含哨兵轮询+孤儿自清) |

## 4. 文案表(判例:人话上屏,协议词只留 code/hint)

| 位置 | 文案 |
|---|---|
| 密钥状态行 | 「数据库密钥:已就绪(20 个数据库)/ 未获取 / 已失效」 |
| 获取按钮 | 缺失/失效=「获取密钥」;已就绪=「重新获取」(二次确认);未配取钥器置灰提示「先配置取钥器」 |
| 确认页 | 「接下来会弹出系统密码框;请在微信里退出登录并重新扫码一次。全程只读,微信数据不会被修改。」(重新获取变体:追加「当前密钥将在新密钥验证通过后覆盖」) |
| 进行页阶段 | 「等待输入密码 / 正在连接微信 / 等待重新登录 / 正在验证 20 个数据库」(grill 决议⑦:「挂载」是行话,永不上屏) |
| 结果页 | 「密钥就绪,20 个数据库已可解密」/ 失败人话+「重试」 |
| 监控群状态 | 「监控中 / 密钥缺失 / 降级」(降级=源健康度域词) |

## 5. 决策点(可翻案)

- **D1·获取流放卡内面板 vs 独立向导弹窗**:推荐**卡内三步面板**(弹窗判例=详情类用模态;向导类流程卡内展开更贴既有版面;模态互斥守卫少一层面)。
- **D2·key-acquire 走桥命令 vs Rust 直 spawn 取钥器**:推荐**走桥**(密钥验真/落缓存/exit 21 语义全在桥内,壳零取钥逻辑;AC-B3 守卫面不扩大)。
- **D3·部署件安装时机**:推荐装机后首用引导(设置卡检测取钥器未配+部署件在场→「一键安装取钥器」cp 按钮);不放安装包(D1 冻结线)。

## 6. 并行避让(硬纪律)

- 数据源侧会话在途(桥 README/config/localdb.py + 根 pyproject 活跃改动 17:15+)。本任务桥侧三个件(cli/localdb/docs)**动手前必探活**(status+mtime 双探,活跃则先做前端/Rust 面,桥面排队);取钥器部署件与数据根配置面无冲突。
- 提交纪律:pathspec 分域;不收编对方面。

## 7. 风险与回滚(grill 决议⑩补权限回退)

- **osascript 提权弹窗从 Tauri app 上下文 spawn 的权限面**:SecurityAgent 对话框理论上任意父进程可弹(攻坚档从无头 bash 已实证);若装机态被自动化权限/Gatekeeper 拦,**回退=进行页降级为终端指引文案**(给出等价终端命令),不阻断流。
- 协议 v1.1 向后兼容(旧 provider 不发 timeout_hint 字段照跑,120s 帽不变)。
- 获取流失败不污染既有 keys.json(全量验真才落,桥语义既有;--force 亦不改「先全量验真后覆盖」)。
- 哨兵文件残留(取消后部署件未及轮询即崩):下轮获取流启动时先清哨兵;残留不影响功能(只在获取进行中生效)。
- 前端三面各自独立提交,可单独 revert。

## 8. grill 拷问轮记录(2026-10-13;11 决议全回写,可翻案标记★)

①三态化 key-status(抽样重验,probe 判据会说谎)②--force 旗标(失效场景短路洞)③哨兵取消(root 段杀不动)④R4 一期只读跳 YAML 屏(双写切断)★⑤群状态复用源健康度(废 24h 拍脑袋)⑥超时三处统一(600/1800 帽/900 壳)⑦「挂载」=行话禁上屏⑧AC5 机制/真实拆分(数据侧依赖挂账)★⑨左栏只读显式化⑩osascript 权限回退路径⑪timeout_hint 上限帽防乱报。★=主人可翻案;④涉及范围收缩需主人知情默认。

---

# 契约规格册(零歧义执行层;2026-10-13 grill 后深化轮)

> 与上文 §1-§8 的关系:§1-§8=设计意图与决议;本册=逐字节契约。冲突时以本册为准(本册后写且更细)。

## §A 桥 CLI 新命令契约

### §A.1 `wechat-bridge localdb key-status --json`

注册锚:`plugins/wechat-bridge/wechat_bridge/cli.py` localdb_sub 家族(query/key-scan/key-provider 之后,~L135 前);实现锚 `localdb.py` 新 `key_status()`。

**应答(恒 exit 0;三态查询不判错,缺文件=missing 也是正常态):**

```json
{"key_status": {
  "state": "ready | stale | missing",
  "db_count": 20,
  "acquired_at": "2026-10-13T11:22:00+08:00",
  "wechat_version": "4.1.15",
  "verdict_note": "抽样 3 库验真通过" }}
```

| 态 | 判据 | verdict_note 例 |
|---|---|---|
| missing | keys.json 不存在/空 dict/解析失败 | 「密钥缓存缺位」 |
| stale | 在场,抽样 1-3 把(取 mapping 前中后各 1)页1 HMAC 有一把不过 | 「抽样验真失败:N/M」 |
| ready | 在场+抽样全过 | 「抽样 3 库验真通过」 |

- `db_count` = mapping 键数(missing=0);`acquired_at` = keys.json **mtime** ISO 本地时(missing=null);`wechat_version` = probe 同源(system_checks.wechat_version,拿不到=null)。
- 抽样验真复用 `localdb.py` 既有 `_verify_enc_key` 族(与 write_key_cache 消费前重验同函数,不另写一份);验真需读库文件页 1——db 根解析复用 `auto_detect_db_dir` 同源逻辑。

### §A.2 `wechat-bridge localdb key-acquire --json [--force] [--timeout-hint N]`

- 缺省行为:keys.json 在场且抽样过 → 直接返回 `{"key_acquire": {"result": "already_ready", ...}}`(短路);`--force` = 跳过短路直走取钥器。
- `--timeout-hint N`(缺省 600):透传进 provider 请求 `timeout_hint_seconds`;桥内实际硬帽 = `clamp(N, 120, 1800)`。
- 未配取钥器:`{"error": {"code": "key_unavailable", "message": "未配置外部取钥器,请在设置中指定可执行文件路径", ...}}` + **exit 21**(与 query 缺钥同族同码,引擎/壳侧归一路径不变)。
- progress 透传形态:桥把 provider stdout 的每行 progress 原样**转印到桥自身 stdout**(NDJSON 行,与桥既有 --json 输出同流;result 前的 progress 行是协议既有合法行序,query 等既有命令不产 progress,零混流风险);同时 stderr 记一行摘要计数(诊断用,不进 stdout)。
- 启动先清残留哨兵文件(见 §C),再 spawn provider。
- 取消联动:桥收到 SIGTERM(壳 kill)→ kill provider 进程组(用户态段)+ 自身退出码 143;**root 段清理由部署件哨兵轮询自理**。

## §B 壳侧 Tauri 命令与事件契约

注册锚:`desktop/src-tauri/src/main.rs` L902 `wechat_keyprovider::wechat_key_provider` 同列表追加;实现同 `wechat_keyprovider.rs` 文件(与 B5 同风格:spawn 安装态桥 `~/.myia/plugins/wechat-bridge/bin/wechat-bridge`,MYIA_HOME 注入同源,30s→本命令不适用,见各帽)。

### §B.1 `wechat_key_status` → 应答 = §A.1 `key_status` 对象直转(wire snake_case)

### §B.2 `wechat_key_acquire {force?: bool}` → **异步命令 + 事件流**

- spawn `localdb key-acquire --json [--force] --timeout-hint 600`,stdout 逐行读;每行 progress/result 转 event;命令返回值 = 终态:`{result: "ok"|"failed"|"cancelled", db_count?: number, error?: string}`。
- 壳侧兜底帽 **900s**(读行超时或总时长超帽 → kill 用户态链 + 判 failed「超时」)。
- 取消命令 `wechat_key_acquire_cancel {token: string}`(token=B.2 返回的流标识;或简化用单飞锁:同会话只允许一个 acquire 在途,cancel 无参)。**简化定案:单飞锁无参 cancel**(实现小,多窗并发取钥本就不该发生;第二 acquire 直接报「已有获取在进行」)。
- 取消动作:①kill 用户态进程树(桥+provider 用户态段,进程组 killpg)②落哨兵 `<数据根>/wechat-localdb/cancel.keyacquire` ③终态 event `cancelled`。

### §B.3 事件 `wechat-key-acquire`(模式照抄 pyenv-api.ts 的 PYENV_STATUS_EVENT 范本)

```
载荷:{seq: number, phase: string, detail: string | null}
phase ∈ "password"|"attach"|"wait_relogin"|"derive"|"done"|"failed"|"cancelled"
```
- `seq` 单调递增(前端丢弃乱序旧包);phase 词面**只作机器枚举**,上屏词走前端词表(§D.3);detail = provider progress 的 message 原文(已是人话)。
- 前端常量名 `KEY_ACQUIRE_EVENT_NAME = "wechat-key-acquire"`(与壳侧 const 同值成对,注释互指)。

## §C 部署件规格 `keyprovider-lldb.sh`(+包装 python)

部署位:`<数据根>/wechat-localdb/bin/keyprovider-lldb.sh`(700);源=攻坚档 tools/ 三件(lldb-shot/lldb-run/蓝本 py)打包适配,安装=设置卡「一键安装取钥器」按钮(cp+chmod,检测源在场=攻坚档路径或随设置指引手放)。

**行为序列(协议 v1.1 交互式取钥器):**
1. 读 stdin 单行请求;解析 `timeout_hint_seconds`(缺省 600,自帽 ≤1800)。
2. stdout 发 `{"type":"progress","message":"等待输入管理员密码","level":0}`;osascript `do shell script ... with administrator privileges` 提权跑内层(蓝本四级链)。
3. 提权段启动前起**哨兵轮询**(后台子进程,每 2s 查 `<数据根>/wechat-localdb/cancel.keyacquire`;见即 pkill 自家 lldb 孤儿+删哨兵+exit 42=取消语义)。
4. 断点就位后 `{"type":"progress","message":"请在微信中退出登录并重新扫码","level":0}` + `osascript display notification`(Glass 音,攻坚档 lldb-shot 既有形态)。
5. 命中:内层完成派生+逐库验真(蓝本逻辑)→ 把 keys map 写**临时文件**(600,数据根私有区 tmp)→ 外层(用户态)读临时件 → stdout `{"type":"result","success":true,"keys":{...}}` → 删临时件。
6. 任一失败:`{"type":"result","success":false,"error":"人话原因","logs":[...]}`;取消哨兵触发时 error=「已取消」。
7. 全程 root/用户态分段:root 段=蓝本执行+哨兵自杀;用户态段=协议 IO(osascript 弹窗由用户态直接发起,无需 root)。

## §D 前端规格

### §D.1 设置卡扩展(weixin-account-card.tsx)

- 插入锚:取钥器配置行区块**上方**(密钥状态先于取钥器——因果序:状态→行动→工具配置)。
- 状态行:`数据库密钥:` + Badge 三态(ok=「已就绪 N 库」/warning=「已失效」/outline=「未获取」)+ `· 今天 11:22`(相对时间组件既有)+ 按钮(§D.2)。data-testid:`weixin-keystatus-{badge|refresh|time}`。
- api 扩展进 `wechat-keyprovider-api.ts`(同文件,~85 行既有):`wechatKeyStatus()`(invoke wechat_key_status + parse 守门,configured 布林严校模式照抄 parseKeyProviderState)+ `KEY_ACQUIRE_EVENT_NAME` + `subscribeKeyAcquire(cb): UnlistenFn` + `startKeyAcquire(force)`/`cancelKeyAcquire()`。

### §D.2 三步面板(卡内,状态机)

```
idle → confirm →(开始)running →(done event)result
                     ↑(取消)     ↘(failed event)result(失败形)
```
- confirm 态:两行文案(§4 表)+ 主按钮「开始」+次按钮「取消」;ready 态入口=「重新获取」时 confirm 追加覆盖语义行。
- running 态:四阶段步进条(当前 phase 高亮,已完成打勾——阶段名=词表§D.3)+ detail 行(事件 detail 原文,mono 小字)+「取消」按钮(调 cancel 命令,人话「正在取消…」直到 cancelled event)。
- result 态:成功形=「密钥就绪,N 个数据库已可解密」+重拉 status;失败形=error 人话+「重试」(回 confirm)。
- data-testid:`weixin-keyacquire-{confirm|start|running|cancel|result|retry}`。

### §D.3 阶段词表(phase→上屏)

| phase | 上屏 |
|---|---|
| password | 等待输入密码 |
| attach | 正在连接微信 |
| wait_relogin | 等待重新登录 |
| derive | 正在验证数据库 |
| done/failed/cancelled | 结果页形态(非步进条) |

### §D.4 feed 三级监控台群列表(feed-screen.tsx)

- 锚:三级双栏右栏(渠道行组件 ~L1163 家族,微信行复用 CHANNEL_ROW_AVATAR_TONE.wx 官方绿 10% tint 既有档)。
- 数据拼装:源清单(既有渠道分组数据流按 `weixin-` 前缀过滤)+ 每源最新一条(既有 list_items source 等值,渠道行 cardDigest 既有函数复用)。
- 状态映射:源最近 run skip_reason(`key_unavailable`→「密钥缺失」灰行+「去获取密钥」按钮,点击=导航设置 /weixin 屏并滚到密钥行;其余→源健康度域词「监控中/降级」)。
- 「去配置监控群 →」按钮:右栏底,跳既有 YAML 编辑屏(yaml-editor 深链携 weixin.yaml 预选,若该屏无深链参数则跳屏+文档注记手选)。
- data-testid:`wx-monitor-{row|status|latest|goto-config}`。

## §E 文件级改动锚表(执行者对照)

| 文件 | 改动 | 参照形态 |
|---|---|---|
| plugins/wechat-bridge/wechat_bridge/cli.py | localdb_sub 增 key-status/key-acquire 两 parser(~L135) | keyprov 家族同款 argparse+--json 重注册循环 |
| plugins/wechat-bridge/wechat_bridge/localdb.py | key_status()/key_acquire(进程编排+progress 转印+哨兵清理) | acquire_keys_from_provider 既有 spawn 骨架复用 |
| docs/wechat-keyprovider.md | §v1.1(timeout_hint/哨兵约定/交互式取钥器指引) | 既有 §5-§8 体例 |
| desktop/src-tauri/src/wechat_keyprovider.rs | wechat_key_status/wechat_key_acquire(_cancel)+事件发射 | 同文件 B5 spawn 骨架;事件=pyenv.rs PYENV_STATUS_EVENT 范本 |
| desktop/src-tauri/src/main.rs | L902 列表追加两命令 | 同行式 |
| desktop/ui-src/src/screens/settings/wechat-keyprovider-api.ts | status/acquire/cancel/事件订阅(~85→~180 行) | pyenv-api.ts listen+UnlistenFn 范本 |
| desktop/ui-src/src/screens/settings/weixin-account-card.tsx | 密钥状态行+三步面板(~301→~450 行) | 同卡取钥器行 ErrorBox/FieldInput 既有件 |
| desktop/ui-src/src/screens/feed/feed-screen.tsx | 三级右栏微信群列表+缺失引导+跳配置(~L1163 区) | 渠道行组件+wx tint 既有档 |
| <数据根>/wechat-localdb/bin/keyprovider-lldb.sh | 部署件(源=攻坚档 tools/) | lldb-shot.sh 骨架+§C 序列 |

## §F 错误码族汇总(新增面全表)

| 面 | code | exit/形态 | 人话 |
|---|---|---|---|
| 桥 key-acquire 未配取钥器 | key_unavailable | exit 21 | 未配置外部取钥器,请在设置中指定可执行文件路径 |
| 桥 key-acquire 取钥器失败 | key_unavailable | exit 21+error.message 透传 | 取钥失败:<provider 人话> |
| 壳 acquire 单飞锁 | acquire_in_progress | 命令错误信封 | 已有一次密钥获取在进行中 |
| 壳 acquire 超帽 | timeout | 终态 failed | 获取超时(15 分钟),可重试 |
| 部署件取消哨兵 | (内部 exit 42) | result success:false | 已取消 |
| 桥 key-status | 恒 exit 0 | 三态即正常 | —— |
