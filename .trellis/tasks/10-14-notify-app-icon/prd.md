# macos_notify 换壳代发:通知带 app 图标归组世事

## 背景

主人报障(10-14 截图实锤):微信/TG 新消息的系统通知横幅「不好看,这个图标不是本项目的图标」。
根因:`src/myssia/push/macos_notify.py`(10-14-wechat-notify-revoke R3)用
`/usr/bin/osascript display notification` 直弹——**osascript 发的通知图标恒为脚本编辑器、
归组显示 osascript**(模块注释自己记了这条「已知形态限制」)。

## Goal

通知由**桌面壳(app 本体)代发**:Rust 壳挂 tauri-plugin-notification(desktop = notify-rust,
macOS `set_application(bundle_id)`),sidecar 经协议事件 `notify.banner` 送壳 → 壳以
`com.myssia.app` 身份发——图标/归组/通知中心归属/点击唤起全部是世事 app。CLI 无壳跑保留
osascript 兜底;壳代发故障逐条回退 osascript,横幅不丢。

## Requirements

1. **Python(`src/myssia/push/macos_notify.py`)**:新增 `set_banner_emitter()` 注入点;
   `send()` 里发射器在位 → 每条 plan 调发射器(不 spawn);发射器异常 → warn + 回退该条
   osascript;合并纪律/文案帽/日志零正文全部不动。
2. **宿主注册(`desktop/entry.py` serve)**:`_OUT` 捕获后注册
   `lambda plan: _write_line({"type": "notify.banner", **plan})`;顶层 import 不 lazy。
3. **壳(`desktop/src-tauri`)**:Cargo + `tauri-plugin-notification = "2"`;泵
   `handle_stdout_line` 对 `type == "notify.banner"` 分支代发(title/body;subtitle 折叠进
   正文 `"{subtitle} · {body}"`,桌面 builder 无 subtitle 面),失败 warn 不转发 UI;
   其余 type 照旧转发。
4. **权限**:Rust 侧代发不经 webview ACL,capabilities 零改动;macOS 首发时系统一次性
   征询「世事发送通知」(master 授权一次)。
5. **测试**:python 专测补发射器三分支(注入→事件形状/零 osascript;异常→回退;
   复位→osascript 照旧);Rust cargo check+build 门禁。

## Acceptance Criteria

- [x] AC1 机制全落地并实弹到系统层:沙箱注入验证横幅触发 macOS 对「世事」的一次性通知授权征询(截图 evidence-auth-prompt 入档);图标终验=主人点「允许」后第一条自然横幅(一眼之验,无法代点)。
- [x] AC2 CLI 无壳零差(ENXIO/无注入回退 osascript 专测在案)。
- [x] AC3 中继三形态专测(真 FIFO 端到端/ENXIO 回退/CLI 形态)23/23 全绿,既有用例零改动;cargo check+build 绿。
- [x] AC4 全量 6275 passed / 53 skipped;UI 零涉。
- [x] AC5 三次换装哈希验毕(aa1fc397);沙箱 FIFO 中继实跑+注入横幅实弹至系统授权层(像素证据入档);回退包 .old-1014-b 在位。

## 非目标

- 不动合并纪律/文案(每会话一条、撤回独立、200 字帽)。
- 不引入 terminal-notifier 等外部二进制(链接者红线)。
- Windows/Linux 通知形态顺带受益(插件自带),不做专项。
