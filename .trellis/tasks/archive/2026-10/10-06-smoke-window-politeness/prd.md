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

- [x] AC1 壳层:ui-ready 门控+5s 兜底+焦点分档三路落码,Reopen/二实例零行为变化(cargo test 绿,纯函数面有测)
- [x] AC2 前端:App mount emit myia:ui-ready(浏览器态静默容错)
- [x] AC3 几何:parse_smoke_geometry 纯函数+clamp+单测;env 未设零行为
- [x] AC4 装机真机:小窗+无焦点+「出现即已渲染」(出现当帧截图 OCR 有内容非纯白;frontmost 不变)
- [x] AC5 验证配方更新入记忆,后续验证流不再糊脸

## 回标(2026-10-06)

- AC1-3:a04dfb5 落码(UI_READY/PENDING_SHOW 门控+5s 兜底+焦点分档+几何纯函数),cargo 59 passed(+3)/tsc 0/vitest 532;Reopen/二实例回调路径零改动亲读。
- AC4 装机真机三轴:小窗 Width=900 生效(grep 'Width.: 900' 命中)/frontmost 前后均 clash-verge(零抢焦)/出现当帧截图 OCR 直读出情报流成品(世事/未读/星标/50/50条)非白屏;backgroundColor 暗底随包。
- AC5:配方已入记忆(packaged-app-verify-and-swap-race);CI 绿(run 见 gh list a04dfb5 success);装机包已换装备份 /tmp。
- 根因注:白窗=渲染前 show(仅验证路径中招);弹脸=全尺寸+set_focus 配方;现行 SHOW_ON_START 残留实例已清(报障源头之一)。
