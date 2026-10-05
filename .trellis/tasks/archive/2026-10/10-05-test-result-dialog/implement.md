# Implement:试抓结果详情弹窗

## 顺序清单

1. `api.ts`:`summarizeTestCompleted` → `buildTestOutcome`(结构化 `TestOutcomeView`,三 kind;纯函数,防御式取值与现状同款)。删除一行 summary 逻辑。
2. 新增 `test-result-dialog.tsx`(design 全节落地;零新依赖;ESC/遮罩/X 三径同关)。
3. `sources-screen.tsx`:撤两处顶部横幅块(试抓进行中 + 试抓结果,现 331-353 行);`testOutcome` 非 null 渲染 `<TestResultDialog onClose=…>`;事件订阅处换 `buildTestOutcome`;`handleTest` 的发起失败 catch 换 launch_error 视图。头部注释同步(C13 段描述)。
4. `sources-table.tsx`:试抓钮 `testing` 态补 title + `data-testid="test-running"`。
5. `sources.test.tsx` C13 段同步:
   - 成功形:弹窗弹出 + 概要(引擎/条数)/指纹判定文案断言;载荷加 `failures` + `items`(含 dedup_key/fields/截断)断言退化链与条目预览。
   - 失败形:error 族 + `data.errors` 逐条在弹窗内。
   - 发起失败(test_busy):弹窗失败形。
   - ESC 关闭弹窗断言;`test-running` 锚点迁行内钮后仍可查。

## 验证命令

```bash
cd desktop/ui-src && npx vitest run src/screens/sources
cd desktop/ui-src && npx tsc --noEmit -p tsconfig.app.json
git diff --stat   # 不得越出 desktop/ui-src/src/screens/sources/(与并行会话混线,提交走 pathspec)
```

vite build 归统一门禁,不在任务内跑(spec frontend-ui 第 5 条)。

## 回滚点

单笔提交整体回滚(无迁移/无协议面)。
