# Design:试抓结果详情弹窗

## 边界

- 只动 `desktop/ui-src/src/screens/sources/` 四件:`api.ts`(视图构造)、`sources-screen.tsx`(状态/装配/撤横幅)、新增 `test-result-dialog.tsx`(展示)、`sources-table.tsx`(仅试抓钮补 title/testid);外加 `sources.test.tsx` 断言同步。
- 协议零改动:`types.ts` 的 `TestCompletedEvent` 原样消费;后端(`src/myssia/cli.py`)零改动——载荷已含全部明细。

## 数据流

不变段:`sources.test` 发起(job 单飞)→ `test.completed` 事件按 job_id 对账回屏。

变化段:

```
test.completed ──buildTestOutcome(原 summarizeTestCompleted,改产结构化视图)──▶ TestOutcomeView
sources.test 发起失败 catch ──launch_error 形────────────────────────────▶ TestOutcomeView
testOutcome ≠ null ──▶ <TestResultDialog> 自动弹出;onClose → setTestOutcome(null)
handleTest 起手 setTestOutcome(null)(新发起即关旧弹窗,既有行为保留)
```

## TestOutcomeView(结构化,api.ts 导出)

```ts
{
  sourceName: string;
  ok: boolean;   // report 形随源级 report.ok(引擎链耗尽如实判失败,kind 仍 report 并携 report.error)
  kind: "report" | "event_error" | "launch_error";
  // kind="report"(事件 ok 且报文里有本源报告;报告缺源 → event_error 形「报告里没有该源的结果」)
  engine?: string;            // 命中引擎(report.engine)
  engineConfigured?: string;  // 配置引擎(report.engine_configured)
  itemCount?: number;
  fingerprint?: { verdict: string; meaning: string; skipReason: string | null };
  failures?: { engine: string; errorType: string; message: string }[];
  items?: { dedupKey: string | null; dedupKeyError: string | null; fields: Record<string, string> }[];  // dedupKeyError = 模板求值失败,如实呈现不静默
  itemsTruncated?: boolean;
  // kind="event_error"(事件 ok=false):error + data.errors[] {path, message}
  // kind="report" 且链耗尽前的整体超时(report.error)也入 error 字段,弹窗失败明细节呈现
  error?: string; errors?: { path: string; message: string }[];
  // kind="launch_error"(sources.test invoke 被拒):code + message
  code?: string; message?: string;
}
```

## 弹窗组件(手写 overlay,零新依赖;`YamlEditorDialog` 同范式)

- 容器:`fixed inset-0 z-50 bg-black/60 animate-overlay-in` 遮罩 + 居中面板 `w-[min(760px,88vw)] max-h-[80vh] flex flex-col rounded-lg border border-border bg-card shadow-drawer animate-dialog-in`(全 token,零 arbitrary 值)。
- 标题区:`试抓结果 · {sourceName}` + 状态徽章(成功=ok 色/失败=destructive 色,`test-result-status`)+ X 关闭钮。
- 正文(overflow-y-auto)分节,有则渲染:
  1. 概要:引擎命中 `{engine}`(配置 `{engineConfigured}`)· 条目 `{itemCount}` 条(链耗尽时命中回落配置引擎,再缺位如实「—」)
  2. 指纹判定:`fingerprint.meaning` 全文
  3. 引擎退化({n} 次):逐条 `{engine} [{errorType}] {message}`
  4. 条目预览(`test-result-items`):逐条 dedup_key(mono 2xs)+ fields「k = v」行;`itemsTruncated` → 「仅预览前 N 条」
  5. 失败明细:event_error 逐条 `{path}:{message}`;launch_error `{code}:{message}`
- 底部动作条:「查看采集日志」链接(`#/logs`,同 runOnce 横幅的链接样式)+ 关闭钮。
- 交互:ESC / 遮罩点击 / X 三径同关(只读无 dirty 守卫);面板挂载即聚焦(`tabIndex={-1}` + focus,ESC 免先点进);`event.defaultPrevented` 不关(YamlEditorDialog 缺陷 2 判例)。
- testid:根 `test-result-dialog`;状态徽章 `test-result-status`;条目区 `test-result-items`。

## 进行中态

顶部「进行中」横幅撤除;行内试抓钮 spinner 既有,`testing` 态补 `title="试抓进行中,实时输出见日志屏"` + `data-testid="test-running"`(测试锚点迁移至此)。

## 兼容 / 回滚

- 浏览器直开无事件通道:行为不变(发起错误照走失败弹窗,零事件依赖)。
- 回滚 = revert 单笔提交(无协议/存储/依赖面)。

## 已知边界与互斥(复查 M/L 修法,2026-10-05)

- **模态互斥**:结果弹窗渲染条件 `testOutcome && editingFile === null`——编辑模态在途时结果不叠双模态(同 z-50 叠底 + 两个 window keydown 监听 ESC 双关,会静默丢结果),只驻 state,编辑弹窗关闭后自然浮现;新发起试抓起手 `setTestOutcome(null)` 旧弹窗随关(既有行为)。
- 概要括注仅 `engineConfigured !== engineHit` 时示(引擎缺位回落时防「命中 X(配置 X)」重复);失败明细 path 空不带冒号;正文滚动容器 `tabIndex={0}`(键盘可滚)。
- testing 卡死(事件永不到达)无超时,与横幅时代一致(预存行为,如实认定);无 focus trap 系继承 YamlEditorDialog 范式局限(全仓弹窗共性,另行统一)。

## 权衡记录

- 自动弹出 vs 手动点开:试抓由用户行内发起,等结果是其直接意图 → 完成即弹,少一次点击(Kestra Trigger→Execution 详情同向)。
- 「跑一次」/「启停」横幅不同改:见 prd 留观节,防 scope 蔓延。
