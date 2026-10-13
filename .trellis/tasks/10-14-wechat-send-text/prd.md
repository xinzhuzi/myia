# 微信 send_text 三源合体升级(导航/验证协议/AX 链)

## Goal

把已验证的三路开源/自研资产合体进桥(`plugins/wechat-bridge`)的 `send_text` 通道,替换旧盲法导航,达到「指定联系人 → 导航 → 写入 → 发送 → 回执验证」全链可信,并以真机白名单双发完成深度测试。主人令(2026-10-14):「按照你的建议先将开源的代码借鉴之后,深度测试,使用 grill 方式进行深化与补全」。

## 三源(均已实读源码/实弹验证)

| 源 | 抄什么 | 资产位置 |
|---|---|---|
| WuZiyong/wechatctl.swift(1⭐ 283 行成品,已逐行核毕) | 验证协议:verifyTitle 标题带 OCR 模糊匹配、composer 哨兵探测(置哨兵→Cmd+A→**Cmd+C**→回读)、发送后清空轮询(12×80ms)、SHA256(收件人+消息)120s 防重 + uncertain-never-retry、旧剪贴板保存/恢复、CGEvent(combinedSessionState 源 + cghidEventTap 注入) | `/tmp/wuziyong_wechatctl.swift` |
| tonyshield/send-wechat-message | 导航:Cmd+F → AXFocusedUIElement/AXValue 写搜索词 → OCR 分区过滤(左栏 30%,分区头上方本地结果,排除搜一搜;需补「功能分类」分区头)→ CGEvent 点击目标行——**不盲回车** | `/tmp/ref_search_click.sh`(仓:tonyshield/send-wechat-message) |
| 自验 AX 链(10-13/14 晨实弹) | AX 门 LLDB 热激活配方(QCocoaAccessibility+8 bool,静态 VA 见 FINDINGS)+ `chat_input_field` AXValue 写入/回读 + activate+回车(36);元素名 `current_chat_name_label`/`session_item_<名字>` | `/tmp/wxrev/FINDINGS.md`、`/tmp/ax_chat_test` |

已排除:chairmanmiao/wechat-macos-proxy(peekaboo 依赖+硬编码坐标+无条件假成功)、wechat-use(闭源二进制+激活码审核+锁 4.1.9 副本)、tiancheng91(404)。

## 现状(勘察结论)

- 桥源码在仓库:`plugins/wechat-bridge/wechat_bridge/`;`send_text` 子命令**已存在**(cli.py:99,Phase D),`send_state.py` 已有 G6 flock 占位频控(单条、≥10s 硬间隔);另有 `ax.py`/`sendui.py`/`pixel.py`/`system_checks.py` 前置件——本任务是**升级**非新建。
- 装机活体:`~/.myia/plugins/wechat-bridge/`(bin/wechat-bridge 启动器 + wechat_bridge 包),热修=cp 源文件。
- 测试基线:`uv run --no-sync python -m pytest tests/wechat-bridge -q` = 302 passed / 7 skipped 绿。
- 微信 4.1 主进程在跑(pid 见勘察);AX 门状态须探,关则按 FINDINGS.md 配方重开。

## 硬约束(红线)

1. **白名单双发**:真机发送仅限 文件传输助手(filehelper)与 jiangliushi666(display_name 🐳),内容固定「嘻嘻」,全程真实发送 ≤2 条,间隔 ≥10s。
2. **禁止盲发**:发送前 DB 侧(alias→wxid→display_name)+ 当前会话标题(AX label 或 OCR 标题带)双验证;导航不得盲回车(分区过滤选行)。
3. **uncertain-never-retry**:发送结果不确定时不得重试,如实报告。
4. 每步证据留痕(截图/AX 读值/localdb 回执查询);回执最终以 localdb 落库为准。
5. grill 三关(设计/落地 diff/测试证据)全过才算交付。

## Acceptance Criteria

- [ ] AC1:导航升级落地——搜索→分区过滤选行→点击,零盲回车;单测覆盖分区过滤逻辑(mock)。
- [ ] AC2:验证协议五件套(标题校验/哨兵探测/清空轮询/SHA256 防重/剪贴板恢复)进桥,行为有单测。
- [ ] AC3:AX 链为主通道、CGEvent+OCR 为降级通道的形态落地;AX 门失效可按配方重开并有 doctor 探针。
- [ ] AC4:真机深度测试矩阵全过:dry-run 导航×2 目标、真发×2(每目标 1 条「嘻嘻」)、防重拒发(第 3 次尝试被拒且零新发)、不存在联系人干净拒发、localdb 回执双查。
- [ ] AC5:全量桥测试绿(基线 302 不回退)+ 装机活体热修后 smoke 过。
- [ ] AC6:grill 三关裁决 pass 留痕;发现项全修或有如实注记。
- [ ] AC7:提交入库(桥源码+测试+任务档),detect-changes 过。
