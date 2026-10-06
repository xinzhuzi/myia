# 冒烟/验证窗口礼貌化:白窗修复+不抢焦点+小窗几何

## 背景(主人报障 2026-10-06:「沙箱启动的总是弹出白色,并且占住我的工作弹脸上」)

根因双源:
1. **白窗**=验证启动(MYIA_SHOW_ON_START/SMOKE_ROUTE)在 WKWebView 渲染完成前就 show——正常产品路径(visible:false 藏窗等 Dock Reopen)永远不见白,故只有自动化验证/沙箱实例中招。
2. **弹脸**=验证配方用 1920x1080 全尺寸窗+set_focus 抢前台(历轮验证与开关点击尝试)。

## 决议

- R1 白窗修复:前端 App mount 完成 emit `myia:ui-ready`;壳层验证性亮窗(SMOKE_ROUTE/SHOW_ON_START)改为「等就绪才 show」,5s 兜底防卡死藏窗;Reopen/Windows 二实例回调保持立即 show+focus(内容早已加载)。
- R2 焦点礼貌:MYIA_SHOW_ON_START 亮窗默认不 set_focus;焦点仅 dev 构建或显式 MYIA_SMOKE_FOCUS=1(需点击的验证才开)。
- R3 小窗几何:MYIA_SMOKE_GEOMETRY="WxH+X+Y"(或 WxH)setup 期应用,验证窗不再全屏糊脸。
- R4 窗口底色:tauri.conf 主窗 backgroundColor 设应用暗色,残余首帧白闪也变暗底(若 schema 不支持则裁)。

## AC

- [ ] AC1 壳层:ui-ready 门控+5s 兜底+焦点分档三路落码,Reopen/二实例零行为变化(cargo test 绿,纯函数面有测)
- [ ] AC2 前端:App mount emit myia:ui-ready(浏览器态静默容错)
- [ ] AC3 几何:parse_smoke_geometry 纯函数+clamp+单测;env 未设零行为
- [ ] AC4 装机真机:小窗+无焦点+「出现即已渲染」(出现当帧截图 OCR 有内容非纯白;frontmost 不变)
- [ ] AC5 验证配方更新入记忆,后续验证流不再糊脸
