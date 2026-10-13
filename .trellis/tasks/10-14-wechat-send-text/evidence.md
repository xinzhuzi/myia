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
