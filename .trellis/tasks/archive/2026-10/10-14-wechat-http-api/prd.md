# 微信本地库 HTTP API(C6)

## Goal

把桥 localdb 只读能力映射为**本机 HTTP API 常驻服务**(`wechat-bridge localdb serve`),供外部系统/自动化脚本/LLM 工具对接。鉴权=本机回环+token(父档已钉死);接口形态锚 WeFlow `docs/HTTP-API.md` 的**语义**(端点族谱/SSE 契约/ChatLab 水位协议/GET+POST 统一),代码与文案零拷贝(其许可 CC BY-NC-SA 4.0,比 GPL 更不可沾)。服务内部消费同一套桥编排函数——HTTP 应答与 CLI 应答逐字段同源,不造第二套查询实现。

## 来源与依赖

- 父档:10-13-wechat-features C6 行(`localdb 能力 HTTP 化(常驻服务模式),鉴权=本机回环+token`)。
- 开源调研结论(2026-10-14,立档输入):
  - **锚 WeFlow**(hicccc77/WeFlow,15052★,活跃,CC BY-NC-SA 4.0):127.0.0.1 绑定、token 三通道+timingSafeEqual、未配置 token 即全拒、/health 豁免、GET/POST 统一、SSE 25s 心跳+重放缓冲 1000 条/10min TTL+Last-Event-ID 续传、ChatLab Pull 增量水位协议(since/end/limit/offset + sync 块 hasMore/nextSince/nextOffset/watermark)。全部**借语义零抄码**;其 7.6/7.7 章写/hook 端点(sns/block-delete、DELETE /api/v1/sns/post、install/uninstall)整族排除并进 grep 守卫词表。
  - **反面教材** chatlog 血统(myysophia/wechat-log,Apache-2.0):默认 `0.0.0.0:5030`+零 token+CORS `*` 带凭据——MYIA 要避开的全部坑,固化为守卫测试;其 DB 状态中间件语义(后端未就绪→503+明确 error 文案)如实借。
  - **法律判例**:sjzar/chatlog 收微信官方函件清库(2025-10-20)、0xlane/wechat-dump-rs 被 GitHub DMCA(2026-01-08 Tencent 申诉)、MemoTrace(42092★)清库、PyWxDump 删库——见「Constraints·公开分发风险知情决策」。
- 既有数据面全复用(不重做):桥 E2 解密副本管道+E3 查询层+localdb 命令族(见下节);20 钥 keys.json 已验真、346MB 消息库已解密(父档「数据资产已就位」)。
- 姊妹档:**无硬依赖**(C6 自含水位扫描件);C3 媒体导出、C4 联系人查询层落位后经媒体/联系人端点扩量(集成点接线,C6 不等待)。
- MYIA 内部消费**不经 HTTP**:管线引擎/桌面 sidecar 维持既有一次性 CLI 子进程通道(`src/myssia/engines/wechat_local.py` 既有形态);HTTP API 是**对外**面。

## 既有交付盘点(不重做,全部直接复用)

| 交付 | 证据锚 |
|---|---|
| 密钥解析全链(keys.json 重验→取钥器→自愈→E1)+ 三态 key_status | `plugins/wechat-bridge/wechat_bridge/localdb.py:1187`(resolve_keys)、`localdb.py:979`(key_status) |
| E2 解密副本生命周期(TTL/容量/失败重建/源新即重建/并发单飞锁) | `localdb.py:1406`(ensure_decrypted_copies)、`localdb.py:1386`(_source_newer) |
| 查询编排:query_history / sns_history / group_info(供 HTTP 端点同源调用) | `localdb.py:1547`、`localdb.py:1601`、`localdb.py:1656` |
| E3 查询层:query_messages(4.1.15 分表/Name2Id 反解/zstd)、list_sessions、contact 批量名解析、group_info | `wechat_bridge/localdb_query.py:277`、`:754`、`:368`、`:676` |
| CLI 命令族+stdout 单 JSON 契约+exit 码族(20/21/22) | `wechat_bridge/cli.py:108-194`、`wechat_bridge/codes.py` |
| 配置面:封闭键清单+缺省+save_config_key 管理代写(600/700) | `wechat_bridge/config.py:95`(键清单)、`config.py:288`(save_config_key) |
| 回环 HTTP 服务先例(stdlib ThreadingHTTPServer,仅 127.0.0.1) | `src/myssia/push/feishu_callback.py:38,407`、`desktop/entry.py:6766-6879`(OAuth 回调) |
| 组件打包/版本三方同步(0.7.0)/测试台 tests/wechat-bridge/ + MYIA_WECHAT_E2E 门控 | `wechat_bridge/__init__.py:22`、`pyproject.toml`、`component.json:4`、`tests/wechat-bridge/test_e2e_gated.py:26` |
| 桌面微信设置卡(取钥器/密钥状态行族,HTTP 分区的落点) | `desktop/ui-src/src/screens/settings/weixin-account-card.tsx` |
| 引擎级水位先例(源级水位+内容锚) | `src/myssia/engines/wechat_local.py`(「源级水位」节) |

## Requirements

### R1 常驻服务命令 `localdb serve`

- 新 CLI 子命令:`wechat-bridge localdb serve --json [--host H] [--port P]`(flags 覆写配置;缺省取配置键)。
- **前台常驻**:stdlib `ThreadingHTTPServer`(`daemon_threads=True`),Ctrl-C/SIGTERM 干净退出 exit 0;**不做 daemonize**(桌面托管/launchd 属集成点与后续)。
- 启动序:读配置 → **回环校验**(R3)→ bind(bind 失败=exit 1 结构化错误带「端口占用」指引)→ stdout 打**单行就绪 JSON** `{"http_api":{"host","port","token_configured":bool,"version"}}` → 进入服务循环;此后访问日志走 stderr 且**只载形状**(method/path/status/耗时,零聊天内容零密钥,红线 6)。
- `http_api_enabled` 配置键**只供桌面托管消费**(集成点);显式 CLI 起服=意图明确,不读该键。
- 进程归属裁决(PRD 钉死,design 只落细节):常驻服务本体=桥组件自身(独立受管组件,与 WeFlow 内嵌 Electron 主进程不同构;CLI 直起保证无桌面/服务器场景可用),桌面 app 是它的宿主之一而非本体。

### R2 鉴权(WeFlow 语义全套,PRD 已钉死)

- token 三通道:`Authorization: Bearer <token>` 头(全端点)/ POST JSON body `token` 字段(全端点)/ URL `access_token` 查询参数(**仅限 SSE 端点 `/api/v1/push/*`**——EventSource 不能设头;其余端点 query 通道=401。文档主推 Bearer,防 token 进 shell history/进程列表——WeFlow 没有的收紧)。
- token 未配置(空串/键缺):一切非 `/api/v1/health` 请求 **401**(防裸奔),错误体带 fix_hint 指向 `localdb http-token generate`。
- 比较用 `hmac.compare_digest`(常时,stdlib;对位 WeFlow timingSafeEqual)。
- **token 热生效**:每请求重读配置文件验证 token(小文件本机读,代价可忽略)→ `http-token generate/clear` 后无须重启服务即轮换/吊销;配置文件坏=沿 last-good token 继续服务,`/health` 如实加 `config_error` 注记(不炸服务不静默)。
- CORS:仅当 `Origin` 头的 host 属 `localhost|127.0.0.1|[::1]`(任意端口)时回 `Access-Control-Allow-Origin: <origin>` + `Vary: Origin`(+ Methods GET,POST,OPTIONS / Headers Authorization,Content-Type);其余 Origin **不回任何 CORS 头**。OPTIONS 预检同规。

### R3 回环绑定强制(红线级)

- 缺省 `http_api_host="127.0.0.1"`;`serve` 启动时校验 host ∈ {`127.0.0.1`,`localhost`,`::1`},非回环值(含 `0.0.0.0`)→ **BridgeError exit 2** 结构化报错(文案注明:对外暴露解密聊天数据是红线,chatlog 判例)。
- 配置装载期不拒非回环 host 字符串(坏值不许炸 `sessions list` 等无关命令,判例同 key_provider_path);只在 serve 面拒绝。

### R4 端点族谱(全只读;GET/POST 统一,POST JSON body 参数并入查询参数)

| 端点 | 参数 | 行为 |
|---|---|---|
| `GET/POST /api/v1/health` | — | **token 豁免**;恒 200。应答 `{"health":{"state","key_status":{…三态载荷…},"bridge_version","uptime_seconds"}}`;state ∈ `ok\|key_missing\|key_stale\|db_missing`(复用 `localdb.key_status` + db_storage 定位;chatlog DB 状态中间件语义:健康面如实暴露后端生命周期) |
| `GET/POST /api/v1/sessions` | `limit?`(1..200,缺省 20) | 会话列表;新编排 `localdb.sessions_list`(确保 [session,contact] 域副本→`list_sessions`);应答同 CLI 载荷 |
| `GET/POST /api/v1/messages` | `chat_id`(必)、`since_days?`(1..3650,缺省 30)、`limit?`(1..1000,缺省=配置 limits.messages) | **与 `localdb query` 同源**:直调 `localdb.query_history`,应答=CLI 载荷原样(messages/sessions/display_name/copy/…) |
| `GET/POST /api/v1/sessions/{chat_id}/messages` | `since`(epoch 秒,必)、`end?`(epoch 秒,不含)、`limit?`(1..5000,缺省 500)、`offset?`(≥0,缺省 0) | **ChatLab Pull 水位协议**:新查询函数(见 R5);应答 `{"chat_id","since","messages":[…升序…],"sync":{"hasMore","nextSince","nextOffset","watermark"}}`;消息行=既有行形状(`ts/sender/type/text?/media_placeholder?`) |
| `GET/POST /api/v1/group-info` | `chat_id`(必) | 直调 `localdb.group_info`,应答同 CLI(缺表降级空结构恒 200) |
| `GET/POST /api/v1/sns` | `mode=feed\|notices`(缺省 feed)、`since_days?`(1..3650) | 直调 `localdb.sns_history`,应答同 CLI |
| `GET /api/v1/media/<rel>` | — | **两段式媒体下发(形状先立,内容随 C3 集成注入)**:只允许服务 `http-media/` 缓存目录内文件(见 R7 路径穿越);目录外/不存在=404;C3 导出未接线前目录为空=如实 404 |
| `GET /api/v1/push/messages` | `access_token`(SSE 专用 token 通道) | SSE 事件流(见 R6) |

- 参数形状错→400 `{"error":{"code":"usage",…}}`;未知路由→404;非 GET/POST/OPTIONS 方法→405。
- 桥错误族映射:`BridgeError`(db_not_found=20/key_unavailable=21/decrypt_failed=22)→ **503** `{"error":{"code","message","fix_hint"}}`(码名/文案与 CLI 错误载荷同源);未预期异常→500(日志只载形状)。

### R5 ChatLab Pull 水位协议(查询层新增,`localdb_query.py` 加法)

- 新函数 `query_messages_range(con, chat_id, since_ts, end_ts, limit, offset)`:
  - 按 `find_message_tables` 同一自适应机制选表,`create_time > since`(且 `≤ end` 若给)升序 + `LIMIT limit OFFSET offset`;
  - `watermark` = 该会话表当前 `max(create_time)`(单会话表内聚合,代价=单会话规模,不扫全库);
  - sync 块语义:取满 `limit` 条 → `hasMore=true, nextOffset=offset+limit, nextSince=since`(翻页期 since 不动);未取满 → `hasMore=false, nextOffset=0, nextSince=watermark`(一轮拉毕跳水位)。
- 既有 `query_messages` 零改动(纯加法;CLI 契约不动)。

### R6 SSE 事件流(`/api/v1/push/messages`)

- **事件载荷**(协议字段英文):`event: message` + `id: <单调整数序号>` + `data: {"type":"message.new"|"message.revoke","chat_id","ts","sender",…}`;`message.new` 载 `text?`(文本)或 `media_placeholder`;`message.revoke` 由 local_type=10002 记录+残留原消息合成(携 `orig_preview` ≤30 字,解析件见 R8)。
- **心跳**:每 25s 注释帧 `: ping`(常量注入点,单测不真等)。
- **重放缓冲**:环形 ≤1000 事件 / TTL 10min;断线带 `Last-Event-ID` 重连→补发该 id 之后事件;超量/超期淘汰如实(消费端契约:按 id 去重;重连过晚=从头经 Pull 端点补)。
- **水位扫描线程**(serve 进程内,独立模块):
  - 扫描间隔 60s(模块常量);水位持久化 `<数据根>/wechat-localdb/http-watermark.json`(600;内容仅 `{"watermark":<epoch 秒>,"updated_at":…}`,零内容零密钥);
  - 冷启动无水位文件 → watermark=now(**不倒灌历史**;历史走 Pull 端点);有文件 → 断档间隙首轮扫描如实补发(消费端按 (chat_id, ts, sender, sha1(text)[:16]) 内容锚去重——与 `engines/wechat_local.py` 锚形态同族);
  - 单轮扫描范围=session 表前 50 会话(库内自然序)逐会话 since 水位增量查询;覆盖面如实文档化(近活跃会话;全量历史=Pull 端点);
  - **性能红线**:单轮扫描不得触发全库逐行扫描;实现机制(副本建索引/私有区台账/定点查询)留 design 裁决,约束=索引/台账只落解密副本或数据根私有区,永不出私有区、永不写微信侧。
- **延迟量级如实钉死**:事件延迟=扫描间隔量级(分钟级),文档与应答描述**禁用「实时」字样**(WeFlow 靠 FFI 表变更通知 500ms 去抖做到秒级,MYIA 只读链无此件——如实,不虚标)。

### R7 路径穿越守卫(红线级)

- 媒体路由**只**服务 `<数据根>/wechat-localdb/http-media/` 目录(服务自有导出缓存目录,700;C3 集成时导出物落此);`decrypted/`、`keys.json`、配置文件**结构性不可达**:
  - 解析后绝对路径必须 `path.resolve` 后以 `http-media/` 前缀开头,否则 404;
  - 拒绝绝对路径入参、符号链接出根(构件以 `os.path.realpath` 二次校验);
  - `../`、`%2e%2e%2f`、`..%2f`、混合编码变体一律 404——用例照 verificationIdeas 红线级清单打。

### R8 撤回事件解析件(与 C5 共用)

- 桥侧新解析函数:输入会话增量行,识别 `local_type=10002` revoke 记录并关联残留原消息(同会话、撤回系统消息可解析的原文引用或时间邻域内被撤类型行),输出 revoke 事件载荷(原消息缺失=仅撤回事实,不臆造内容)。
- **归属**:C6 先落则归 C6(供 SSE),C5 浏览面撤回标记消费同一函数;C5 先落则 C6 消费其件(集成员统一,见 overlapNotes)——两头不得各写一份解析。

### R9 token 管理 CLI(`localdb http-token`)

- `generate --json`: `secrets.token_urlsafe(32)` → `save_config_key("http_api_token", …)`;应答 `{"http_token":{"result":"generated","token":"<明文仅本次应答显示>","length":43}}`(再生成=轮换,旧 token 即刻失效,热生效见 R2)。
- `show --json`: `{"http_token":{"configured":bool,"token":"…","length":…}}`(本机主人面;配置 600 私有区)。
- `clear --json`: 吊销(=token 未配置态,一切非 health 401),应答 `{"http_token":{"result":"cleared"}}`。
- v1 单活 token(无 token 清单/多活);轮换路径=generate 覆写。

### R10 配置面扩展(封闭清单加 4 键,`config.py`)

| 键 | 类型 | 缺省 | 校验 |
|---|---|---|---|
| `http_api_enabled` | bool | `false` | 布尔;仅桌面托管消费(R1) |
| `http_api_host` | str | `"127.0.0.1"` | 字符串;非回环值在 serve 面拒(R3),装载期不拒 |
| `http_api_port` | int | `5032` | 1..65535 正整数(**刻意避开 5030/5031**:chatlog/WeFlow 族端口,防同机并用相撞) |
| `http_api_token` | str | `""` | 字符串;空=未配置=全拒(R2);由 http-token 命令代写,不进 limits |

- `component.json` config_defaults 同步;未知键 fail-fast 纪律不变。

### R11 版本与文档

- 组件版本 0.7.0 → **0.8.0**(`__init__.py`/`pyproject.toml`/`component.json` 三方同步,真锁惯例;component.json cli_contract 追加 serve/http-token 两行、private_paths 追加 http-watermark.json/http-media/、config_defaults 追加 4 键)。
- 新文档 `docs/wechat-http-api.md`(协议文档惯例对齐 `docs/wechat-keyprovider.md`):端点全表+参数/应答示例、鉴权三通道与推荐用法、错误码映射表、SSE 事件契约(心跳/重放/续传/去重锚/延迟量级如实)、安全边界(回环强制/token/媒体 allowlist/路径穿越)、`curl` 快上手、公开分发风险注记(见 Constraints)。
- `plugins/wechat-bridge/README.md` 运行形态节补 serve/http-token 两行。

### R12 测试(全 mock 进 CI;真库件走 MYIA_WECHAT_E2E=1 门控)

- `tests/wechat-bridge/test_httpapi.py`:鉴权红队(未配置全 401/错 token 401/三通道正例/query 通道限 SSE/health 豁免/compare_digest 源级断言)、CORS(localhost 回/外源不回)、回环守卫(0.0.0.0 拒启 exit 2/缺省绑 127.0.0.1)、路由契约(临时数据根+假副本:各端点应答与 CLI 编排同源逐字段、参数 400/路由 404/PUT 405)、错误映射(20/21/22→503)、路径穿越变体族(造假 keys.json 证不可达)、SSE(注入假 ticker:心跳帧/Last-Event-ID 补发/缓冲淘汰与 TTL)。
- `tests/wechat-bridge/test_watermark.py`:水位持久化/冷启动=now/断档补发/扫描上限 50/撤回解析(fixture 行:10002+残留原文)。
- `tests/wechat-bridge/test_httpapi_gated.py`(门控,对真解密副本):Pull 两轮拉取与 `sqlite3 COUNT(*) create_time>since` 交叉核对、深分页基准(R13)、真 revoke 行事件合成、SSE 一轮真扫描端到端。
- grep 守卫(进 test 或 CI 脚本):`httpapi.py` 全文无 `DELETE|PUT|block-delete|install|uninstall` 端点词表;方法处理器仅 do_GET/do_POST/do_OPTIONS。

### R13 性能验收(346MB 真库)

- Pull 端点 `limit=1000&offset ∈ {0, 50000, 200000, 库内最大行数}` 打点:各点 p50/p95 落档;**任一 offset 点 p95 > 5s = 未过**,design 换策略(副本索引/键集分页)后重测。
- SSE 单轮扫描(50 会话上限)真库实测耗时落档,p95 < 5s 同门槛。
- `/api/v1/messages` 与 CLI `localdb query` 同库同参耗时对拍(同源验证,差值≈HTTP 开销)。

## Constraints

- **只读红线**:一切端点读解密副本;零微信进程干预、零写微信侧数据;密钥材料与聊天内容不入 git/日志/报告(服务访问日志只载形状)。
- **许可纪律**:WeFlow=CC BY-NC-SA 4.0,代码/JSON 结构/文案**零拷贝**,只借 API 形态与工程参数(设计思想);chatlog 族代码不可得且 Go→Python 无复用面,同样只借语义;实现全部自写。
- **写/hook 端点整族排除**:WeFlow 的 sns/block-delete、install/uninstall、DELETE 类端点永不进端点族谱(grep 守卫钉死);MYIA HTTP 面=纯只读。
- **公开分发风险知情决策(记录在案)**:本能力面(解密聊天数据→可编程 HTTP)与 chatlog(2025-10-20 收微信官方函件清库)、wechat-dump-rs(2026-01-08 DMCA)、MemoTrace/PyWxDump(清库/删库)被打击件同面。缓解=只读解密副本+密钥不出数据根私有区+本机回环+token+不对外分发密钥获取能力;**若 MYIA 公开仓库发布,收函/DMCA 风险只能降低不能归零**——主人 2026-10-13 已圈定 HTTP API 功能令(WeFlow 功能清单原文第 12 行),本档记录风险后按令推进,风险知悉。
- 文案:文档/UI 词全人话(「聊天记录」「本机接口」),协议字段/端点路径保留标准英文(AC-P5 同源)。

## Acceptance Criteria

- [x] AC1 鉴权红队(真进程+curl):token 未配置→非 health 全 401;错 token(Bearer/body)401;`access_token` query 在非 SSE 端点 401、在 SSE 端点放行;Bearer/body 正例放行;/health 无 token 恒 200;`hmac.compare_digest` 在码(源级守卫断言)。
- [x] AC2 回环守卫:缺省起服后 `lsof -nP -iTCP:5032` 确认仅 127.0.0.1 LISTEN;`--host 0.0.0.0` 起服 exit 2 结构化报错;localhost/::1 放行。
- [x] AC3 CORS:Origin `http://localhost:3000` 回 ACAO+Vary;Origin `https://evil.com` 无任何 CORS 头(curl -i 断言)。
- [x] AC4 端点同源:sessions/messages/group-info/sns 四端点对真解密副本(TMS 群)应答与对应 CLI 命令载荷逐字段一致(同一编排函数,对拍脚本断言)。
- [x] AC5 水位交叉核对(门控):Pull 端点两轮拉取,`sqlite3` 直查 `COUNT(*) WHERE create_time>since` 交叉核对行数与 `sync.hasMore/nextSince/nextOffset/watermark` 一致;翻页期 nextSince 不动、拉毕跳 watermark。
- [x] AC6 深分页基准(门控):R13 基准全点通过(p95<5s)且分布落档;`/api/v1/messages` 与 CLI 耗时对拍落档。
- [x] AC7 SSE 续传:注入事件→断开→带 Last-Event-ID 重连→补发不丢不重(内容锚去重可用);25s 心跳注释帧在场;重放缓冲 1000/10min 淘汰如实在测;延迟口径=分钟级且文档无「实时」字样(grep 守卫)。
- [x] AC8 路径穿越(红线级):`/api/v1/media/../../keys.json` 及 `%2e%2e%2f`/`..%2f`/绝对路径/符号链接变体全 404;数据根内造假 keys.json 全程不可达。
- [x] AC9 写/hook 零混入(grep 守卫):httpapi.py 无 DELETE/PUT 处理器与 `block-delete|install|uninstall` 端点词;端点族谱与 R4 表逐行对得上。
- [x] AC10 token 生命周期:generate 后明文仅本次应答显示;轮换后旧 token 立即 401(热生效,不重启);clear 后非 health 全 401。
- [x] AC11 红线复审:全程零微信进程干预、零写微信侧数据;服务日志抽查只载形状;红线三项(改消息/防撤回拦截/朋友圈拦截)未以任何形态混入。
- [x] AC12 文档+版本:docs/wechat-http-api.md 全端点+鉴权+错误码+SSE 契约+安全边界+风险注记;三方版本同步 0.8.0;`uv run --no-sync python -m pytest tests/wechat-bridge -q` 全绿零回归,门控件在 `MYIA_WECHAT_E2E=1` 下通过。

> **复查回执(2026-10-14 复查员实跑,判定 PASS/needsFix=false)**:① MYIA_WECHAT_E2E=1 pytest tests/wechat-bridge/test_httpapi_gated.py → 4 passed+1 skipped(撤回合成件 skip 如实,真库 10002 行数=0);深分页 offset∈{0,50000,200000,8821} p95≤45.3ms≪5s 门;CLI 编排 p50=35.3ms vs HTTP 核心 37.1ms;SSE 真扫描 25ms 水位推进;② 红线 grep httpapi.py:DELETE|PUT|PATCH|block-delete|uninstall|install 全零;do_ 处理器恰三个(httpapi.py:730/733/741);docs/wechat-http-api.md「实时」零命中、「分钟级」2 处;③ 安全锚点在码:hmac.compare_digest(httpapi.py:330)、validate_loopback_host(:165)、realpath 双重出根校验(:495);④ pytest test_httpapi+test_watermark 99 passed;⑤ 全量 tests/wechat-bridge 730 passed 12 skipped 0 failed(六域桥件集成态全绿)。装机像素验证(HTTP API 面)归父档 AC-P4 blocked 注记(UI 未落,AC 全 CLI/curl/文档级)。
>
> **留档发现**:[info] 前回执披露的两项集成裁决仍在案待集成员定夺:撤回解析器产权(C5 notify_query 阶梯 vs watermark.parse_revoke_events 双实现)、serve 进程内双扫描器(C5 白名单基线 vs C6 尾窗)是否合流——非缺陷,是仲裁项。

## Notes(留 design 的口,不属 PRD 义务)

- SSE 扫描的免全库扫机制(副本索引 vs 私有区台账 vs 定点查询)——约束已钉(私有区内、单轮 p95<5s),机制 design 裁决。
- 桌面托管细节(子进程监管/有界重启/就绪行握手)与设置卡「本机接口」分区版式——集成点,集成员接线。
- 媒体导出缓存写入方(C3 集成)与 http-media/ 目录内容管理(TTL/清理)——C6 只立目录与守卫。
