# 执行计划:YAML 编辑器缺陷修复(滚动裁剪 + ESC 误关 + 补全开关)

> 三处改动全部在 `desktop/ui-src` 前端,互不依赖,可一笔提交;grill 决议见 prd.md。
> 规模:约 0.5 小时(代码 3 处 + 测试断言 + 门禁 + 无头复验 + 重打包换装)。

## 前置

- [ ] 工作树干净(除本任务文件);分支按仓库惯例直接 main 或短期分支。
- [ ] 复现 harness 可用:按 `evidence/shim.js` 头注与 Notes 起 bridge + vite(修复后复验用;探针 `evidence/probe.py` 直接复用)。

## 改动清单(有序)

1. [ ] **滚动主修** `editor-pane.tsx`:`<CodeMirror … className="h-full">`(@uiw 渲染 `class="cm-theme h-full"`,父级定高链打通;不改外框、不加 CSS)。
2. [ ] **补全开关** 同文件:basicSetup 删 `autocompletion: true` 一项(其余项原样;决议 Q1)。
3. [ ] **ESC 守卫** `yaml-editor-dialog.tsx` window keydown 回调首行加 `if (event.defaultPrevented) return;`。
   - 实现时核实:CM 搜索面板关闭时确实调用 preventDefault(若无则改用「面板在场检测」:`document.querySelector(".cm-panel")` 非空时跳过关闭)。
4. [ ] **回归断言** `editor-pane.test.tsx`:断言 CodeMirror 组件收到含 `h-full` 的 className(防高度链再丢);`yaml-editor-dialog.test.tsx` 若存在则补 ESC 用例(defaultPrevented 的合成事件不触发 onClose)。

## 验证(有序,全绿才算完)

1. [ ] `cd desktop/ui-src && npx tsc -b && npx vitest run`(门禁:类型+单测全绿)。
2. [ ] `npm run build`(vite 产物可建)。
3. [ ] **无头复验**(harness):重跑 `evidence/probe.py` 口径量测——弹窗与双栏屏 `.cm-scroller` scrollH > clientH、编程 scrollTop 生效、⌘F 面板开着按 ESC 弹窗仍在;截图存 evidence/。
4. [ ] **门禁全量**:仓库根 `uv run --no-sync python -m pytest -q`(防意外波及)+ `cargo check`(如 CI 口径,可选)。

## 收尾

1. [ ] 提交(单笔或按缺陷分笔,遵循仓库提交风格);AC 勾选回填 prd.md。
2. [ ] **装机包刷新**:重打包 + 静默换装(纪律:完成=入库+门禁绿+装机包已刷新)。
3. [ ] 交主人目验:开弹窗滚到 330 行文件尾 / 敲一段中文(IME)/ ⌘F 开面板按 ESC 弹窗不关。

## 回滚

- 三处改动独立,任一出问题单独 revert 对应 hunk;无数据迁移、无协议变更,回滚零残留。
