# 通知点击深链:横幅点开直达消息详情

## 背景

主人令(10-15):「弹窗弹出哪个内容,我希望点击后,可以进入到具体的详情界面」——通知横幅点击不再只唤前台,要落到该会话的 feed 3 级聊天工作台。

## 方案(实证选型)

mac-notification-sys 0.6.15 原生 `wait_for_click(true)`(cargo registry 实读:阻塞返回 NotificationResponse::Click);tauri-plugin-notification(notify-rust 链)不透传点击响应 → macOS 绕开插件直用底层件。

- **Python**:`plan_notifications` 三路(撤回/按会话分组/通用)计划各带 `source`(最新条目的条目源键;微信本机 = 会话名 = feed 渠道键);缺位 None 壳侧只唤不链。
- **壳(macOS)**:`notify.banner` 泵分支直发(set_application 每发必调);专属线程 `wait_for_click` → `NotificationResponse::Click` → `emit notify:navigate {source}`;关闭钮不链;非 macOS 保留插件面(载荷保形)。
- **前端**:`lib/notify-route.ts`(挂起槽 + main.tsx 安装器 + 窗口信号);feed 屏 openChannel 声明后消费 effect(挂载消费 + 即时信号两形态;openChannel 幂等)。

## 验收

- [x] AC1 全链门禁:feed 220/220 + 全量 vitest 934/934 + tsc + push 域 pytest 1234 绿;detect-changes medium(泵分支波及)。
- [x] AC2 cargo check 绿(既有 sanitize_file_name 死码警告非本批)。
- [ ] AC3 装机覆盖安装 + 真横幅点击深链终验(主人一眼:点 TMS 群横幅 → 直达该群 3 级)。

## 局限(如实)

- 冷启动点击(壳线程随旧进程亡)只唤不链。
- 深链目标 = 会话的 3 级渠道视图(不滚到具体某条;最新消息本就在顶部区)。

## 工程教训

并行会话同时在写 feed-screen.tsx(另 4 个 dwfrun 在跑):写入被周期性回打——守波(90 秒静默)+ git HEAD 干净底一次成型 + Edit 工具落点 + 即时门禁 + 立即提交锁果。

## 增量(10-15 晚,主人令「小件都做完」):粒度细化到具体消息(4a355082)

原局限「落到会话 3 级,不定位到具体消息」已消除:

- 载荷全链新增 `item_key`(python plan → 横幅 → 壳事件):= 锚定条目
  `dedup_key`(feed 屏 `data-item-key`);合并通知锚 = 最新一条;撤回
  独立条也锚定;缺 = 会话级如实退化。
- feed 屏消费:开 3 级 → 有限重试(12×250ms 等挂载/数据)→
  `scrollIntoView(center)` + `ring-1 ring-primary/60` 短暂高亮 1.6s
  (类名取键盘巡游现成组合,保 Tailwind 构建产物在位)。
- notify-route 挂起槽升级 `{source, itemKey}` 两元组(新增单测 4 条)。
- 门禁:pytest 24 / vitest 937 / tsc / cargo check 全绿。
