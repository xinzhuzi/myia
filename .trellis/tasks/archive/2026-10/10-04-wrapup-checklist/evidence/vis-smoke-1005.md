# 主人目验替身:最新 UI 视觉把关(2026-10-05 01:0x,主人令「你替我做」)

方法:无头 GUI 冒烟法(vite 真前端 5199 + fork 桥 cwd 沙箱 + 非打包 sidecar target/release/myssia-core + __TAURI_INTERNALS__ shim + playwright 截屏)——沙箱数据=3 条 feed 条目+1 次成功 run+两 job(1 scheduled/1 paused);截图入库 docs/screenshots/vis-smoke-1005/(01-dashboard/02-feed/03-cron);本机 VL(qwen3-vl-8b,8080,model=本地路径)三屏宏观把关。

## VL 结论(逐屏)
- **01-dashboard:无异常**——概览四卡/趋势图/源健康度/品类状态布局完整,零覆盖错位截断。
- **02-feed:无异常**——工具行全控件在场(品类下拉/分段/搜索/JSONL/CSV/**导出当前视图**——CI 回绿批迁入的导出组视觉实证落位),与列表零重叠。
- **03-cron:布局无异常**——活性条+表格两行 job(运行/暂停态)清晰;活性条黄条「调度器未存活」=**dev 回退环境伪象**(entry.py:327 设计明示 dev 不起 ticker 用 CLI serve;真 app ticker 已由首燃+急停 E2E 双实证活)——黄条文案反被验证正确。

## 像素级目验
宏观把关已尽(VL 校准=宏观可用);主人翻图 30 秒即终验(截图在 docs/screenshots/vis-smoke-1005/)。
