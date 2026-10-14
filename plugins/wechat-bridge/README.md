# wechat-bridge — 微信本机桥(UI 自动化 + 本地库只读)

受管组件(task 10-11-wechat-ui-bridge,G7 命名):管「当下收发」的 **UI 自动化桥**(macOS AX 先行,Windows wxauto 备胎另启)+ 管「历史与全量」的**本地库只读通道**。不破解协议;微信进程内存仅在 D4 豁免的密钥扫描里**只读**接触(默认关,三重门;0.4.0 固化为 C 收集器管道),外部件走受管组件链路。

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
python -m wechat_bridge send_text <id> --file - [--dry-run]  # 正文经 stdin(G6 硬频控;0.8.0 三源合体:分区过滤导航零盲回车+验证五件套+AX 主链/CGEvent 降级+localdb 回执终验;--dry-run 走到粘贴回读不回车、零频控副作用可重跑)
python -m wechat_bridge doctor                          # send 链就绪度探针(--probe 超集 + AX 门态/输入区能力;零前台扰动;恒 exit 0;0.8.0)
python -m wechat_bridge localdb query <chat> --since 7d --json   # 本地库只读(Phase E)
python -m wechat_bridge localdb key-scan --json        # 内存密钥批处理扫描(D4 豁免;默认关+须提权(root 或 setuid 自愈件)+只读单遍)
python -m wechat_bridge localdb key-status --json      # 密钥缓存三态 ready/stale/missing(抽样页1 HMAC 重验;恒 exit 0;0.5.0)
python -m wechat_bridge localdb key-acquire --json [--force] [--timeout-hint 600]  # 交互式取钥编排(ready 短路 already_ready/--force 直走/hint clamp 120..1800/progress 原样转印 stdout NDJSON;协议 v1.1)
python -m wechat_bridge localdb sns feed --since 3d --json    # 朋友圈动态(SnsTimeLine XML 解析;窗口过滤在解析后;0.6.0)
python -m wechat_bridge localdb sns notices --since 3d --json # 朋友圈互动通知(赞/评;type 1→like/2→comment;窗口过滤在 SQL;0.6.0)
python -m wechat_bridge localdb page <chat> --limit 500 [--cursor/--from-ts/--to-ts/--types/--sender/--asc]  # keyset 分页,游标续拉(0.8.0)
python -m wechat_bridge localdb conversations [--limit 500]   # 会话清单普查(逐表 COUNT/MIN/MAX+显示名解析;0.8.0)
python -m wechat_bridge localdb export <chat> --format json|txt|csv|md|html|xlsx --out <dir> [--all/--verify]  # 六格式导出+manifest 对账;stdout NDJSON(0.8.0)
python -m wechat_bridge localdb stats chats --json            # 统计与会话枚举/单会话/年度/双人四模式(--since Nd|--all;缓存 <数据根>/wechat-bridge/stats-cache/;0.8.0)
python -m wechat_bridge localdb media status|decrypt <dat>|scan <chat> --since 30d [--decrypt]  # 媒体面(解密件协议 docs/wechat-mediadecrypt.md;未配置=exit 23;0.8.0)
python -m wechat_bridge localdb media-decrypt set <path>|get|clear  # 媒体解密件管理(set 校验绝对路径/存在/可执行;0.8.0)
python -m wechat_bridge localdb sns export --format json|html [--out DIR] --since 30d [--with-media]  # 朋友圈导出(--with-media=唯一受限 CDN GET 豁免,缺省关;0.8.0)
python -m wechat_bridge localdb contacts --type former --with-residue --json  # 联系人六桶分类+找回考古(counts 恒全量/keyset 游标/缺表降级恒 exit 0;0.8.0)
python -m wechat_bridge localdb notify-scan --file -           # 轮询水位通知扫描+撤回检测/恢复阶梯(stdin JSON 载荷,argv 零内容;0.8.0)
python -m wechat_bridge localdb revoke-list <chat> --since 7d  # 会话撤回历史(同一恢复阶梯;0.8.0)
python -m wechat_bridge localdb serve --json [--host 127.0.0.1] [--port 5032]  # 本机 HTTP API 常驻(回环强制+token;协议 docs/wechat-http-api.md;0.8.0)
python -m wechat_bridge localdb http-token generate|show|clear --json  # HTTP token 管理(轮换热生效;0.8.0)
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
- 桥配置:`<数据根>/wechat-bridge/config.json`(全部有缺省、**缺文件可用**,design §7):`domains`(G4 三域)、`limits`(AC2 参数化)、`copy_ttl_hours`(G5 缺省 24;**非负整数,0 = 永不过期**——TTL 判定 0 = 恒新鲜、跳过重建;负数拒)/ `copy_capacity_mb`(G5,须**正整数**)、`mem_search_enabled`(D4 豁免开关,**缺省关**;显式开启 + 提权才生效)。**无频控键**(G6 硬编码:单条、间隔 ≥10s、无批量、不可配置)。
- 频控状态:`<数据根>/wechat-localdb/send_state.json`(flock 防并发,design §2)。
- 外部密钥(D4 裁决②):`<数据根>/wechat-localdb/keys.json`(600 权限;键 = 相对 `db_storage` 的库路径,值 = 该库 64-hex SQLCipher 密钥)。与组件密钥缓存**同位同权**:`localdb query` 消费前逐条 page1 HMAC 重验(`resolve_keys`),全量命中即一步闭合;密钥与库不匹配(如登录态轮换)如实 exit 21 并指明 keys.json 未命中。

## 能力边界(Phase C1/C2 像素链已落;Phase E 已落,E1 实测负结论如实)

- `--probe` 真实现:三态判据矩阵(design §2)照跑——进程/版本/AX 权限/主窗口/本地库落盘/密钥缓存,全只读零前台扰动;微信托盘态如实 `degraded(window_closed)`,进程不在如实 `bridge_unavailable`。
- **UI 读通道 = 像素链(Phase C1/C2 已落地;D2 定论改写)**:A1 实测微信 4.1.15 聊天内容层对 AX 完全零暴露(证据 `research/ax-probe-4.1.15.md`)→ 读 = `screencapture -x -o -l`(静默零交互,ordered-off 托盘窗实测可出完整合成帧,证据 `research/pixel-chain-e2e.md`)→ VisionOCR(pyobjc/Vision 一级,毫秒级+逐行置信度)→ 结构化解析(几何全部数据驱动:会话行=时间锚/名字+预览对组两趟组装;零本机像素硬编码)→ VL 修字(127.0.0.1:8080 qwen3-vl-8b-mlx 二级,任一行 conf≤0.5 触发,**解析后只回填低置信行文本,几何永以一级 Vision 为准**;显式降采样路径:长边 >2048 先 LANCZOS)。C1 会话名+未读徽标(徽标不可见/漏读时 `unread: null` 如实)、C2 最近 K 条文本(ts=最近居中时间标记原文,side=左右气泡,发送者名为启发式)。
  - **硬边界(静默铁律派生)**:桥不能点击切换会话(合成点击被禁)→ `messages read` 读的是**当前打开会话**,载荷 `chat.match` 如实回报请求 id 与可见标题匹配,`false` 时消费方自行取舍。
  - **误差如实**:载荷 `ocr` 节带 engine/低置信行数/VL 是否参与/解析命中率;单个小徽标数字 Vision 常漏读、`999+` 可能读成 `999`(2026-10-11 实测形状)。像素层专属故障不谎报 §6 具名族:`screen_capture_failed`/`screen_capture_black`(后者典型=宿主缺「屏幕录制」TCC 授权)/`ocr_unavailable`(exit 1 过渡码,扩 §6 码表须先改 design)。
  - 截图/裁剪件含聊天内容:全程 0700 私有临时目录、用后即清(红线 3)。
- UI 写通道(send_text,**0.8.0 三源合体**;0.7.0 wxauto 三支柱升级,task 10-14-wechat-send-text;**0.8.1-0.8.4 进化与真机验证版全链见下文「send_text 全链工作原理」节**):①**分区过滤导航零盲回车**(tonyshield 蓝本)——旧「Cmd+F→↓→Return」键序已删除,`KEY_RETURN` 全链唯一出现点=发送;搜索结果面板 OCR 选行=本地/垃圾分区头锚定 + 评分 + unique-row 兜底(emoji 行乱码可救,零候选 exit 15 拒发绝不盲点),坐标三段换算(裁剪系→全窗→屏幕);②**验证五件套**(wechatctl 蓝本)——标题双验证(AX label 直读/OCR 标题带/emoji 间接证据链)、composer 哨兵探测(只读协议 Cmd+A 全选+哨兵+Cmd+C)、发送后清空轮询(12×80ms)、SHA256 指纹防重 120s + uncertain-never-retry(多槽指纹档,exit 17)、剪贴板 finally 复原;③**AX 主链+CGEvent+OCR 降级**——每次尝试双判据(全窗最大节点数>5 AND 输入区可读)判定通道,AX 原语 False → 下一尝试 forced_fallback;CGEvent 键盘/鼠标事件带 combinedSessionState 源句柄,点击范围收窄到导航行+composer 聚焦点;④**localdb 回执终验**(红线 4)——`receipt_query` 闭包按 username 查 1d 窗口消息,`ts > since_epoch-2` 防同正文历史假绿,退避 (5,10,15)s 累计 ~30s;⑤**fail-closed 门与 armed 段隔离**——on_armed(回车 down 前落指纹 pending)失败=上抛可 rollback;armed 后一切异常吞掉如实注记(上抛会诱发 rollback 放开 10s 第二发);**发送前聚焦断言两通道对称**(AX focus_input+复读 / 降级链哨兵读一致性),终败 exit 15 error 载荷(stage=focus,注明 pending 已落);⑥**G6+防重门序**——指纹门在前(幂等命中不占位、立即重复得幂等而非 14)、间隔门在后,同一 flock 临界区;`--dry-run` 走到粘贴回读即收尾(清草稿+Esc 退搜索态,零频控零指纹副作用可无限重跑,载荷带 nav_debug 供 P9 校准);`doctor` 子命令=--probe 超集+AX 门态(0.8.4:closed 时如实注记供给侧边界并指向 CGEvent+OCR 降级链,不再给 LLDB 配方——重开后树仍浅,见「send_text 全链工作原理」节)。**消费方迁移注记(design §E-5)**:exit 0 现有两处 `sent:false` 扩展形态——`deduped:true`(指纹幂等命中,零新发)与 `dry_run:true`(演练);未升级的消费方把 exit 0 当 sent:true 会误判上述两形态,MYIA push 层(weixin_local)按分支键判;除此之外 exit 0 恒 sent:true(聚焦终败=exit 15)。前置=桥宿主需辅助功能/输入监控授权。真机矩阵=P9/P10(dry-run 预验+≤2 真发门控)。
- `localdb query`(Phase E,已落地):定位 db_storage → E1 密钥获取(零内存途径=key_info.db 材料→候选提取→page1 离线 HMAC-SHA512 校验,机制完整可单测)→ E2 sqlcipher 解密副本至 `<数据根>/wechat-localdb/decrypted/`(600/700 权限,TTL 24h 缺省(0=永不过期)+容量上限,失败重建;源库(含 -wal)mtime 比副本新 = 重建(0.4.4,近实时:微信写库后下轮查询即见;微信活跃期重建频率上升为已知 trade-off);TTL=0 = 显式永不刷新(源新也不重建,冻结快照))→ E3 message/session/contact 三域只读查询(列签名自适应,版本漂移如实降级)。**E1 实测结论(2026-10-11 真跑):零内存密钥途径不可推导**(候选全数 HMAC 未命中,与三方独立公开实测一致)→ 如实 `key_unavailable`(exit 21)+ D4 待主人裁决;密钥可得(外部引入或 D4 豁免后)即全链闭合。
- `localdb key-scan`(D4 豁免执行件,主人 2026-10-11「全部解决」令;**0.4.0 固化**主人 2026-10-13「固化成代码」令):内存密钥批处理扫描,管道 = **C 收集器**(`native/collector.c`,三模式宽收集:`x'hex'` 包裹串 / 连续 96-hex 裸串 / 已知 salt 二进制 ±512B 邻域 1B 步进;只读 mach 四调用 `task_for_pid`/`mach_vm_region`/`mach_vm_read`/`mach_vm_deallocate`,**零写零注入零 exec**,argv 白名单=pid,候选恒走 stdout)→ 候选文件(数据根私有区临时件 600,用后即清)→ 熵预筛(≥3.5 bits/byte)→ 8 并发 sqlcipher 试开(微信 4.x 参数变体 4 组)→ page1 离线 HMAC 交叉验证 → 全量命中才落 `keys.json`(600,`localdb query` 一步闭合)。**三重门**:配置 `mem_search_enabled: true`(缺省关)+ 提权在位(root 或 setuid 自愈件)+ 主人裁决在案;旧 Python 滑窗实现退役删除;禁写内存/禁注入/禁调试器附加/禁重签名,守卫测试钉死(C 源码级)。如实预告:微信为 hardened runtime 签名,root 亦可能被内核拒(`task_for_pid` KERN_FAILURE)——该拒绝即此路在本机不可达的如实信号。
- **setuid 自愈件**(0.4.0):`native/install-keyscanner.sh`(一键脚本首段代跑,一次 root)把收集器装为 `<数据根>/wechat-localdb/bin/keyscanner`(root:staff,4750)——此后扫描/自愈零 sudo;`localdb query` 的密钥缺位/解密失败(密钥轮换)在 `mem_search_enabled: true` + 件在位时自动重取(`resolve_keys`/`query_history` 自愈钩子,全量命中才落缓存)。**失败退避**(0.4.1 复审修复):自愈未闭合落冷却戳 `<数据根>/wechat-localdb/self_heal_cooldown.json`(600,内容仅时间戳,零密钥材料),30 分钟窗内查询链不再重扫——不可闭合态(微信改版零命中/部分命中/收集器超时)不再逐次 query 重读微信全进程内存;冷却中 exit 21/22 消息如实注记(不谎称重取过);戳损坏即忘却(负缓存不卡死自愈);成功闭合(自愈或手动 `key-scan`)即清戳;`localdb key-scan` CLI 与一键脚本直连扫描入口,不受冷却门。**威胁模型(如实)**:单用户本机 = 用户读自己微信内存;多用户机器上 staff 组成员可借它做同款只读模式扫描——不接受则不装,`sudo rm` 该件即回归现状(未安装 = key_unavailable + 一键脚本指引)。
- 依赖:sqlcipher CLI(`brew install sqlcipher`,design §5.1 前置;0.4.0 起同为密钥试开验证前置)、cc(Xcode CLT,收集器首用自动编译,缺装时结构化报错带 `xcode-select --install` 指引)。
- 频控+防重落盘模块(G6)已实现并可单测(时间注入,不真等 10 秒;0.8.0 起状态文件两键:`last_send_epoch` + `send_fingerprints` 多槽指纹档——同指纹 120s 防重,pending 命中 exit 17 `send_uncertain_dedup` 绝不自动重试,sent 命中幂等 exit 0)。
- 依赖:sqlcipher CLI(`brew install sqlcipher`,design §5.1 前置;缺装时解密步骤结构化报错并给指引)。

## send_text 全链工作原理(0.8.4,2026-10-14 真机验证版)

**能力声明**:对指定微信会话发送一条文本,全链真机验证(当日 8+ 条真实消息全部送达并落库,零误发)。与微信版本解耦(最新 4.1.15 新进程可用,不依赖 AX 树)。前置:微信在跑(桥自动唤窗,`open -a` 托盘态唤窗实证有效)+ 桥宿主有辅助功能/输入监控/屏幕录制授权。

### 成功逻辑(按执行时序,零歧义粒度)

1. **目标解析**(发送前置,失败即拒,零 UI 扰动):localdb 三路解析(username/alias/展示名),唯一命中才继续;多命中 exit 1 `send_target_ambiguous`,零命中 exit 1 `send_target_not_found`。搜索词选择=**中文名优先**(主人判例 2026-10-14:display_name 非纯 emoji 即用中文名;纯 emoji 名(🐳)落 alias 档)。
2. **通道判定**:AX 探测(主窗最大面积窗 BFS 节点数>5 且输入区可读)。**常态判定结果=走 CGEvent+OCR 降级链**——微信 4.1.15 主窗为 mmui 自绘引擎,accessibleRoot 恒 nil(双线定论:门位自愈=红鲱鱼,树浅是供给侧;见归档 10-14-wechat-ax-gate-exp),AX 主链只在罕见的长命旧进程上可用。
3. **导航 = 侧栏优先,搜索兜底**(主人判例:搜索面板网络区永不为点击目标):
   - **侧栏直选**:OCR 主窗侧栏带(SIDEBAR_BOX),display_name 精确/前缀**唯一**命中→目标行 0.3s 位置稳定锁(y 漂移 ≤0.02 才点,热列表防漂移误点)→点击→即时标题确认;不符**不烧尝试**直接落搜索路。AX 通道等价物=侧栏 session_item AXPress(sidebar_ax)。
   - **搜索路**:Cmd+F→AXFocusedUIElement 直写中文词(失败回落剪贴板 Cmd+V)→等浮窗(**判据:属主微信+layer∈{0,3}+在屏 kCGWindowIsOnscreen+两边长 200-800px;浮窗是预建隐藏窗,id 不变,差分法无效;100×30 状态条/1920×30 横条/280×380 常驻面板全排除**)→OCR 分区带选行(**真机布局:网络区置顶(搜索网络结果+Q 联想行)、本地分区(功能/联系人/…)在下;只在首个本地头到下一分区头的带内选行,无本地头=拒发绝不猜;并列取带内最上**)→点击前**行位稳定性双读**(隔 0.3s,y 漂移 ≤0.03 才点)。
   - **四刀加固**(0.8.4):刀1=浮窗过半窗未弹(词没进框)→OCR 定位常驻搜索框点击+重粘;刀2=整窗零候选→清态重开换 System Events keystroke 直打再给一完整窗口;刀3=上述行位双读;刀4=正文慢落退避重读(真机实证 15:08:粘贴在慢窗上断言时框空、数秒后内容才现,读空先 0.3s×3 重读再判,恒空仍 fail-closed)。
4. **验证五层**(任一不符即拒发,exit 15):①身份(第 1 步);②导航后标题带(AX label 直读/OCR;emoji 目标走间接证据链=导航级采纳+标题带变化);③粘贴回读(AX value 或剪贴板哨兵:Cmd+A→置哨兵→Cmd+C→回读,空=哨兵本体);④发送后输入框清空轮询(12×80ms);⑤localdb 回执终验(username 查 1d 窗,ts>发送时刻-2s)。
5. **发送**:唯一回车点=验证全过后 key code 36(不点发送按钮)。
6. **护栏(G6,硬编码无配置面)**:单次调用只发一条;两次发送硬间隔 ≥10s(flock 占位原语,跨进程并发封闭实证);同指纹(username+\0+正文 SHA256)120s 防重——pending 命中 exit 17 `send_uncertain_dedup` **绝不自动重试**,sent 命中幂等 exit 0;尝试上限 3。
7. **清理**:任何失败路径清搜索态(清词+ESC 关浮窗,含 locate 阶段失败);剪贴板 finally 复原。

### 使用

```console
echo "正文" | wechat-bridge send_text --file - 文件传输助手   # 中文名直达
wechat-bridge send_text --file 正文.txt 张三
echo "测试" | wechat-bridge send_text --file - 文件传输助手 --dry-run  # 预演:零发送零频控副作用,可无限重跑
wechat-bridge doctor                                                # 体检(含通道/门态如实注记)
```

exit 0 载荷三形态:`sent:true` / `deduped:true`(幂等,零新发)/ `dry_run:true`;exit 15=断言族拒发(stage=navigate/locate/focus);exit 14=间隔不足;exit 17=指纹不确定。

### 已知边界(如实)

- 发送窗口 ~8-15s 会短暂占用前台焦点(排程场景无感);主窗关闭时桥自动唤窗。
- 单次成功率非 100%(活人界面的随机性:焦点时序/列表温度);失败=干净拒发可重试,全天实测零误发。
- 热列表(新消息持续重排)时侧栏直选安全让位搜索路;安静时段(深夜排程)侧栏路接管。
- 消费方 MYIA push 层(weixin_local)按 `sent/deduped/dry_run` 分支键判,勿裸把 exit 0 当已发送。

---



1. 静默后台(读通道):不抢前台焦点、不合成鼠标点击、不激活微信窗口。**写通道 send_text 例外**(主人 2026-10-13 热激活批令):激活+键盘 CGEvent+剪贴板驱动,+ 合成鼠标点击(**仅导航行与 composer 聚焦**;PRD 2026-10-14 翻案,task 10-14-wechat-send-text design §I-1——不点发送按钮,发送=回车)。
2. 不破解协议:禁逆向、禁 hook 注入;内存密钥搜索默认关,仅 D4 豁免后配置显式开启 + 提权在位(root 或 setuid 自愈件)才生效,且只读 vm_read 单遍零常驻、禁写内存/禁注入/禁调试器附加/禁重签名(0.4.0:mach 逻辑只在 `native/collector.c`,源码级守卫;setuid 件零 exec、argv 白名单、输出恒 stdout)。
3. 私有数据:聊天内容/密钥材料不入 git/日志/报告;证据只留形状。
4. 依赖纪律:临时依赖一律独立 venv,勿入仓库 `.venv`。

## 测试

```console
uv run --no-sync python -m pytest tests/wechat-bridge -q      # 全 mock,CI 全绿
MYIA_WECHAT_E2E=1 uv run --no-sync python -m pytest tests/wechat-bridge -q  # 加跑真机探针(design §8)
```
