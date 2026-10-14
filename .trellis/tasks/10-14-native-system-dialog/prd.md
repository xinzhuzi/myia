# macOS 系统级原生确认弹窗(window.confirm → Tauri 原生)

## 背景

主人令(10-14):「项目的这个弹窗,就是在 MacOS 上面的弹窗要做的精美一些,从系统层面的弹窗」。

现状:全 App 8 处「确定要…?」类确认走 `window.confirm`——WKWebView 的原生 JS 弹窗,
macOS 上无标题、无图标、按钮是英文 OK/Cancel,与桌面 app 质感严重不符。
`tauri-plugin-dialog` 已注册(main.rs:887),但只用于看图屏文件选择。

## Goal

把 8 处确认弹窗统一换成系统级原生弹窗:macOS = NSAlert(标题 + 警示图标 + 动词化中文按钮),
Windows = 原生 MessageBox,同一条代码路径双平台受益。

## Requirements

1. **新助手 `desktop/ui-src/src/lib/system-confirm.ts`**:`systemConfirm({ title, message, okLabel, cancelLabel, destructive })`
   → Tauri 环境调 `@tauri-apps/plugin-dialog` 的 `confirm(message, { title, kind, okLabel, cancelLabel })`;
   非 Tauri 环境(jsdom 测试/浏览器直开)回退 `window.confirm(message)`,既有 window.confirm spy 测试零改动保持绿。
   Tauri 判定 = `__TAURI_INTERNALS__` in window(仓内冒烟 shim 同款事实源)。
2. **capabilities 补权限**:`dialog:default` 仅含 message/save/open(实证 permissions/default.toml),
   必须显式加 `dialog:allow-confirm`(仅此一条,不开 ask)。
3. **8 处调用点替换**(破坏性操作一律 `kind: "warning"` + 动词化按钮,Apple HIG 惯例;正文文案逐字保留):
   - cron-screen.tsx removeJob(删定时任务)
   - use-yaml-file-editor.ts confirmDiscardIfDirty(放弃未保存修改,屏与弹窗共用)
   - yaml-editor-screen.tsx handleDelete(删品类文件)+ useBlocker 路由守卫
   - yaml-editor-dialog.tsx attemptClose(ESC/遮罩/关闭钮同守卫)
   - use-source-wizard.ts confirmClose(向导未完成关闭)+ source-wizard-dialog.tsx attemptClose
   - bundled-plugins-card.tsx handleUninstall / handleCategoryInstall(卸载/覆盖)
   - feishu-account-card.tsx handleDelete(删账号)
   守卫从同步 boolean 变 Promise<boolean>:调用方 await;attemptClose 类同步回调改
   fire-and-forget + 在飞守卫防 ESC 双触发;useBlocker effect 加 cancelled 标记防卸载后 proceed。

## Acceptance Criteria

- [x] AC1 8 处确认在 Tauri 桌面态走 `dialog.confirm`(title/kind/okLabel/cancelLabel 齐备),非 Tauri 态回退 window.confirm;system-confirm 有专测覆盖两分支。
- [x] AC2 `dialog:allow-confirm` 进 capabilities/default.json,描述同步;无其他权限面变化。
- [x] AC3 既有测试(cron-screen / feishu-account-card / yaml-editor / source-wizard)scoped vitest 全绿零改动或最小改动;`npx tsc --noEmit -p tsconfig.app.json` 过。(实测:119/119 scoped + 941/941 全量,既有测试零改动)
- [x] AC4 全仓 `window.confirm` 调用仅剩 system-confirm.ts 回退分支一处(生产代码零残留)。
- [ ] AC5 装机包真机弹窗像素验证(NSAlert 实貌)留主人,汇报中显式声明(判例:完成=入库+门禁绿+装机包已刷新)。

## 非目标

- 详情弹窗/图片查看器等富内容模态保持 web 实现(判例:动作详情做模态弹窗不贴屏顶横幅;NSAlert 只承载文本+按钮)。
- 不动 `beforeunload` 应用级守卫(浏览器原生 sheet,异步插件弹窗无法替代)。
- 不引入 ask/message 新弹窗;不改 sidecar 协议。
