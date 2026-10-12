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

## 分发形态(D5 裁决:随包源码 + pip_src 相对路径,2026-10-12)

- **路线**:MYIA 仓私有,git 直引需凭据不可行、发 PyPI 加发布纪律 → 组件源码随壳包走:tauri.conf resources 把本目录整份映射进 `Resources/components/wechat-bridge`,桌面组件注册表(`desktop/resources/components.json`)的 `pip_src: "wechat-bridge"` 相对路径由壳白名单解析到该落点(拒绝对路径/`..` 穿越),零 PyPI 依赖、零凭据墙、零发布纪律。
- **两段装**(searxng 先例):一段装构建后端闭包(`setuptools>=75 wheel>=0.45`),二段 `--no-build-isolation` 装随包源码——本目录 `pyproject.toml` 即 pip 装元数据(name `wechat-bridge`,版本与 component.json/`__init__.__version__` 三方同步),主依赖带像素链 pyobjc(Quartz/Vision,darwin 环境标记)与 pillow;装成后自管环境内有 console script `wechat-bridge`。
- **编译依赖不入主链**:sqlcipher Python 绑定(`sqlcipher3`/`pysqlcipher3`)是编译型依赖,放 optional extra `wechat-bridge[sqlcipher]`;**本地库前置是 `brew install sqlcipher`**(design §5.1)——现行解密实现走 sqlcipher CLI,缺装时结构化指引不静默半装;绑定 extras 仅嵌入式路线备用,需要时显式安装。
- **就绪前置**(components.json 描述同口径):`brew install sqlcipher`(本地库通道)+ 辅助功能授权(授给 MYIA app 本体);内存密钥扫描(D4)默认关,显式开启 + root 提权 + 主人裁决在案三重门齐才生效,密钥不可得如实 exit 21。

## 落点与配置

- 组件源码(本目录)经受管链路落在 `~/.myia/plugins/wechat-bridge/`(design §1);MYIA 侧 `wechat_bridge_bin` 可覆写路径(Phase F)。
- 桥配置:`<数据根>/wechat-bridge/config.json`(全部有缺省、**缺文件可用**,design §7):`domains`(G4 三域)、`limits`(AC2 参数化)、`copy_ttl_hours`/`copy_capacity_mb`(G5)、`mem_search_enabled`(D4 豁免开关,**缺省关**;显式开启 + 提权才生效)。**无频控键**(G6 硬编码:单条、间隔 ≥10s、无批量、不可配置)。
- 频控状态:`<数据根>/wechat-localdb/send_state.json`(flock 防并发,design §2)。
- 外部密钥(D4 裁决②):`<数据根>/wechat-localdb/keys.json`(600 权限;键 = 相对 `db_storage` 的库路径,值 = 该库 64-hex SQLCipher 密钥)。与组件密钥缓存**同位同权**:`localdb query` 消费前逐条 page1 HMAC 重验(`resolve_keys`),全量命中即一步闭合;密钥与库不匹配(如登录态轮换)如实 exit 21 并指明 keys.json 未命中。

## 能力边界(Phase C1/C2 像素链已落;Phase E 已落,E1 实测负结论如实)

- `--probe` 真实现:三态判据矩阵(design §2)照跑——进程/版本/AX 权限/主窗口/本地库落盘/密钥缓存,全只读零前台扰动;微信托盘态如实 `degraded(window_closed)`,进程不在如实 `bridge_unavailable`。
- **UI 读通道 = 像素链(Phase C1/C2 已落地;D2 定论改写)**:A1 实测微信 4.1.15 聊天内容层对 AX 完全零暴露(证据 `research/ax-probe-4.1.15.md`)→ 读 = `screencapture -x -o -l`(静默零交互,ordered-off 托盘窗实测可出完整合成帧,证据 `research/pixel-chain-e2e.md`)→ VisionOCR(pyobjc/Vision 一级,毫秒级+逐行置信度)→ 结构化解析(几何全部数据驱动:会话行=时间锚/名字+预览对组两趟组装;零本机像素硬编码)→ VL 修字(127.0.0.1:8080 qwen3-vl-8b-mlx 二级,任一行 conf≤0.5 触发,**解析后只回填低置信行文本,几何永以一级 Vision 为准**;显式降采样路径:长边 >2048 先 LANCZOS)。C1 会话名+未读徽标(徽标不可见/漏读时 `unread: null` 如实)、C2 最近 K 条文本(ts=最近居中时间标记原文,side=左右气泡,发送者名为启发式)。
  - **硬边界(静默铁律派生)**:桥不能点击切换会话(合成点击被禁)→ `messages read` 读的是**当前打开会话**,载荷 `chat.match` 如实回报请求 id 与可见标题匹配,`false` 时消费方自行取舍。
  - **误差如实**:载荷 `ocr` 节带 engine/低置信行数/VL 是否参与/解析命中率;单个小徽标数字 Vision 常漏读、`999+` 可能读成 `999`(2026-10-11 实测形状)。像素层专属故障不谎报 §6 具名族:`screen_capture_failed`/`screen_capture_black`(后者典型=宿主缺「屏幕录制」TCC 授权)/`ocr_unavailable`(exit 1 过渡码,扩 §6 码表须先改 design)。
  - 截图/裁剪件含聊天内容:全程 0700 私有临时目录、用后即清(红线 3)。
- UI 写通道(send_text):Phase D 按 A1 第三案收口(官方 iLink 桥独任);前置检查门真跑(§6 码序 fail-fast),未落地实现层结构化应答 `not_implemented`(exit 1 过渡码,不谎报 §6 具名族)。
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
