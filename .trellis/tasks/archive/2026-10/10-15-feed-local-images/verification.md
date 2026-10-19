# 2026-10-16 验收与装机

交付：卡片展开与详情弹窗共用 FeedLocalImages；缩略图随窄容器收缩，键盘可切换同屏原尺寸，加载/拒绝/失败保留路径。后端先 canonicalize 并检查数据根 images/、后缀与图片头，再逐文件授权 asset protocol。拒绝相对路径、父目录段、越界/软链逃逸和伪图；不更改 persist 默认值。

## 当前证据

- `frontend-full.log/exit`：48 文件，942 tests passed，exit0。
- `rust-tests.log/exit`：3 tests passed，涵盖路径与软链边界，exit0。
- `build.log/exit`：tsc + Vite + Tauri release app 成功。为遵守禁批量删除，临时 build-config 仅绕过源码缓存清理步骤，未改变主 beforeBuildCommand。
- `browser-result.json/browser.log/browser.exit`：从已安装 Mach-O 提取的前端，在 Chromium 夹具 IPC 下，PNG 真解码640×360、缩略/键盘原图开关、越界零转换、404降级、四种视宽、零pageerror，exit0。
- `feed-regression.log/exit`：同一安装件前端的既有三级 Feed 流程无头回归，exit0。截图直接固化在 regression-screenshots，未只留 /tmp。
- `installed-ui-result.json`：安装件内嵌6资源，JS/CSS/SVG与本次构建SHA256一致；index.html经Tauri序列化改变空白/布尔属性写法，HTML语义tokens一致。
- `installed-python-result.json`：146个核心Python文件及入口双件与源码逐字节一致。
- `installation-result.json`：已换装 /Applications/世事.app；旧包保留于 /Applications/世事.backup-20261016-005608.app。新包本地ad-hoc签名并通过codesign --verify --deep --strict。安装前后MYIA进程均为空，未启动GUI。
- 装机RPC结果见兄弟任务 10-16-task-board-managed-smoke/managed-installed-result.json。

## 边界

没有在系统 WebView 中运行真实图片，没有用用户已有持久化素材目验，没有运行Windows程序；Windows路径形状有单测。浏览器IPC是夹具，Rust授权是独立测试，不能称为真实微信媒体链或完整GUI系统验收。

状态review，未归档、未提交。实现与验收均由主线程完成（指定降级子代理模型不可用）。
