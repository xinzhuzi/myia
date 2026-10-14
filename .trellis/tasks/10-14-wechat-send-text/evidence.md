# 真机测试证据(10-14 r3,主会话直跑;工作流 dwfrun-44b197a8 因 provider 故障由主会话按主人判例接手)

环境:微信 4.1.15(pid 91831,曾重启→AX 门复位→LLDB 配方重开,vptr 自检 0x13CB1FE68 精确命中);装机桥 0.8.3(热修);桥测试 730 passed / 12 skipped。

## 测试矩阵(全过)

| # | 项 | 结果 | 证据 |
|---|---|---|---|
| 1 | dry-run filehelper | ✅ 29.8s,navigate(title ocr)/粘贴/AX 回读/零回车 | JSON 载荷 pick_rule=text_match terms_hit=文件传输助手;chat=filehelper |
| 2 | dry-run jiangliushi666 | ✅ 36.9s,emoji 目标走间接证据链(title_verify=indirect) | JSON 载荷 terms_hit=jiangliushi666;chat=jiangliushi666 |
| 3 | dry-run 不存在联系人 | ✅ exit send_target_not_found,DB 侧干净拒发零 UI 扰动 | JSON 载荷(三路均无) |
| 4 | **真发 #1 filehelper** | ✅ sent+composer 清空+post_send_verified | **localdb 落库:04:03:59 修正为 04:03:50,嘻嘻,local_type=1**(直查 decrypted/message_0.db) |
| 5 | **真发 #2 jiangliushi666** | ✅ 同上(title_verify=indirect) | **localdb 落库:04:06:53,嘻嘻** |
| 6 | 防重(同参重发) | ✅ exit 17 send_uncertain_dedup「pending 120s 窗,绝不自动重试」 | 随后 115s 全库零新行=零双发 |
| 7 | 真实发送总数 | **2**(红线 ≤2) | 上述两行,无第三行 |

附:send#1 后主窗截图 OCR 见「嘻嘻」气泡(/tmp/wxsend-e2e/r3/after-send1.png;OCR 报两行为切行伪影,DB 单行是真值)。

## r3 深挖修掉的缺陷(grill 实证,全修+回归测试)

- **门关态降级=挂死**:AX 直写在门关时 osascript 挂 10s 上抛,降级链三连烧死 → 修:ax 通道+降级链内原语 BridgeError 降格为能力缺失走剪贴板路(真机验证:门关 dry-run 从 timeout 挂死变干净拒发)。
- **浮窗定位三连错**:裸 min(面积) 命中 100×30 不可见工具窗(黑图 luma 0)→ 差分法失效(浮窗=预建隐藏窗,id 不变,kCGWindowIsOnscreen 才是判据)→ **layer 过滤错(浮窗是 layer 3 非 0)**。终判据:属主+layer∈{0,3}+在屏+尺寸带 200-800+非主窗;真机窗表实证(wid 96721 368×370@layer3)。
- **BFS 全窗遍历搜索态 >10s 挂死**(浮窗动态树膨胀,press_session_item 恒超时)→ 修:主窗选择=最大面积窗(命名元素全在主窗,浮窗内是空 id virtual_cell);单原语 3.1s→2.5s,搜索态不再挂。
- **doctor ax_gate 假阴性**:枚举探针被挂起污染报 closed 而 AX 树实可读(独立工具 /tmp/ax_chat_test 交叉证实)→ 留档:doctor 门态以独立读为信。
- 回归测试:tests/wechat-bridge/test_send_ui.py TestSearchWindowDiff0_8_3(真机窗表快照入夹具)+ test_axui 形状断言更新(最大窗选择);730 passed 不回退。

## 留档未修(诚实)

- **桥 localdb query 对 filehelper 解析为空**(实际消息在 Msg_0e1945d6…,md5('filehelper')≠表名;jl666 的 wxid 路径正常)——回执直查 sqlite 兜底;修法待查桥表名映射规则,followup。
- 重复发送的第二次尝试在聚焦断言干净失败(粘贴未吃上,未回车零新发)——低频鲁棒性,留 P9 观察。
- 老档「唤窗全手段皆败」翻案:本机托盘态 `open -a WeChat` 唤窗成功(0→1 窗)。
- AX 门关闭态(S2)演练已做(门关 dry-run→挂死→修后行为),但「门关态完整降级发送成功」未演练(门开后未再关)。

## followups 三件终局(10-14 午,主人令续做)

- **S1 golden AX 快照夹具 ✅**:tests/wechat-bridge/fixtures/ax_tree_snapshot.json(真机 System Events BFS 全量转储,主窗 126 节点/33 命名 + 浮窗 15 节点)+ test_ax_snapshot.py 5 测(承重件锚定/树量级漂移守卫/主窗专属证/浮窗命名行证/采集前提留档)。**重大事实修正:搜索浮窗结果行有命名 id(search_item_function_<名字>),旧档「搜索面板全空 id」只对聊天记录区(virtual_cell)成立。**
- **S3 频控并发 ✅**:test_send_state_concurrency.py 3 测(multiprocessing 真子进程):异指纹同刻并发恰一占位/他方 exit 14;pending 指纹 exit 17;占位后跨进程间隔门可见。flock 语义封闭实证,零微信交互。
- **S2 门关态演练 ✅(含惊群发现)**:重启后新进程 AX 树**不暴露**——LLDB 门字节可写可验(read-back=1)但 AppKit 不接线:System Events 零窗/原生 API 空树/-25208 拒增强位与 hit-test/P3 NSApp 位无效/门关-开翻转广播无效/真实点击无效/窗重建无效(8 路实验,证据 /tmp/wxsend-e2e/r3/)。**旧档「重启失效可重开」在全新进程上不成立**(r2 时代开门成功的进程是长期运行实例)。**降级链兜底打通**:中文搜索词落框(焦点时序敏感,先点后粘非必需)+浮窗(368×570 layer3 在屏)分区过滤 OCR → 门关态 dry-run 7.8s 全绿(attempts=1)。
- **WeChat-MCP(277⭐)通道采纳验证**:原生 AXUIElement(ApplicationServices)读树快而稳、不挂起,已验证可用于门开态(python 依赖 pyobjc-framework-ApplicationServices 待正式入桥);其 AX 增强位写法同样被 4.1.15 拒——**门是微信生态共同天花板,非我方独有**。
- **主人判例落地:搜索用中文**——pick_search_term 中文名优先(纯 emoji 名落 alias 档),四档测试重写;真机复验 terms_hit=文件传输助手。

## 网络区抓障修复(10-14 午后,主人报障「每次都搜索网络结果」)

- **取证**(位置化 OCR /tmp/wxsend-e2e/r3/float-evidence.png):4.1.15 浮窗真布局=网络区置顶(搜索网络结果+Q 联想行)→功能(本地头)→带内目标行→聊天记录(深区,同名行再现)。旧 navfilter 三重错:①假设垃圾在底(实际在顶);②「功能」被误标 JUNK;③无分区头时全行候选(网络行可中)。旧实现点对过=OCR 漏读头+y 最大平局的运气。
- **navfilter 重写**:本地分区带内选行(带=网络区下首个本地头→下一分区头);无本地头→None 绝不猜;并列取带内最上(勘误旧 y 最大规则会点深区同名行);网络行 containment 锚(「大 搜索网络结果」带图标前缀也拦);真机布局回归测试锁死。
- **侧栏优先导航**(0.8.4):在册目标侧栏直选(AX:sidebar_ax 零键;OCR:sidebar_ocr 零搜索面板)——搜索面板根本不打开=网络区不出现。热列表防御:目标行位置稳定锁(0.3s 重扫 y±0.02)+点后即时标题确认(不符不烧尝试落搜索)。真机实证主人列表极热(12:3x 新消息连续重排)三连跑均安全落搜索路;安静时段(如深夜排程)侧栏路接管。
- **locate 失败补清理**(Q搜索浮层残留修)。
- 742 passed 全绿;真机三连 dry-run 全绿(title_verify=ocr)。

## 三刀加固终局(10-14 午后,主人令「微信保持最新+干你能做的」)

- **主人定调入档**:微信版本保持最新(版本锚定线正式出局);SendMsgFtouser 直调仍待红线裁决。
- **刀1(词落框恢复)**:浮窗过半窗未弹=词大概率没进框(真机实证 Cmd+V 静默丢)→ OCR 定位常驻搜索框点击+重粘一次;
- **刀2(备用打字引擎)**:整窗零候选 → 清态重开搜索,System Events keystroke 直打搜索词再给一完整窗口(剪贴板粘贴兜底);
- **刀3(行位稳定性双读)**:命中行隔 0.3s 重读,y 漂移 ≤0.03 才点击(以第二读为准)——建议区异步渲染顶动行位时拒点,防点错行。
- 测试:743 passed(新增漂移拒点专项+float-missing 三刀语义重写+测试安全铁律:keystroke 引擎在单测中强制打桩,永不真调 osascript——曾暴露真打字副作用,已堵死);装机 0.8.4;真机三连 dry-run 全绿(10.5-11.5s,text_match+title ocr,零发送)。
