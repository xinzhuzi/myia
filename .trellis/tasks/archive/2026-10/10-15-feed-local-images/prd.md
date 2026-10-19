# 情报流持久化图片安全实显

## Goal

让已由视觉管线显式持久化到应用数据根 `images/` 的 `image_files` 在情报流详情展开态可预览，同时保持最小 Tauri 资源协议白名单与现有文本降级。

## Evidence

- `desktop/ui-src/src/screens/feed/feed-screen.tsx:1118` 只显示图片路径，并留下 v2.2 待办。
- `src/myssia/pipeline.py:2081` 将持久化目录固定为数据库父目录下的 `images/`；`desktop/entry.py:584` 将应用数据根解析为 `MYIA_HOME` 或平台默认根。
- `desktop/src-tauri/tauri.conf.json:26` 已启用 asset protocol，但 scope 仅覆盖微信媒体缓存。
- `desktop/ui-src/src/screens/messaging/wechat/wechat-media.tsx:84` 已有同类 `convertFileSrc` 实显范式及测试。

## Requirements

1. 仅允许应用数据根 `images/**` 进入 asset protocol，不扩大为任意文件系统路径；保持既有微信媒体缓存 scope。
2. `image_files` 必须继续由既有协议白名单投影；前端只渲染其允许路径，异常、空路径或加载失败保留人话降级和路径信息。
3. 展开态展示可访问的缩略预览和原尺寸查看入口，避免影响无图、OCR/caption-only、微信媒体槽等既有路径。
4. 补足单元测试、无头冒烟及配置边界检查；不改变图片持久化默认值、不新增读取任意路径的 IPC、不触碰活进程调试或微信直发链。

## Acceptance Criteria

- [x] 正确的持久化图片在 feed 详情中可见，图像 `alt` 与加载失败状态可核验（安装件前端 + 夹具 IPC）。
- [x] `images/**` 之外的伪造路径不会被转换为可加载资产（Rust 路径测试 + 前端拒绝分支）。
- [x] 无图、坏数据、加载失败与原 OCR/caption 展示回归通过。
- [x] 相关 TypeScript 测试、feed 无头冒烟与 Tauri 配置核验通过。

## Owner decision

2026-10-16 用户批准实施；缩略图自适应（上限256px），同屏原尺寸滚动查看。数据根通过既有 Rust data_root 解析，逐文件动态授权替代跨平台静态路径猜测。已打包换装，待人审；真实系统 WebView 和用户已有持久化图片尚未目验，不宣称微信媒体链闭环。
