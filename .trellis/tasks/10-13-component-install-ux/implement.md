# Implement:组件安装状态进按钮 + 排队自动装

依赖图:壳侧(1→2)→ 契约(3)→ 前端(4)→ 测试(5)→ 门禁(6)。每步验证命令在条目内;全量门禁在步骤 6。

## 1. 壳侧队列化(pyenv_components.rs)

- [x] `ComponentManager` 加 `queued: Mutex<VecDeque<String>>`
- [x] 抽 `spawn_component_install(app, id)` 续装接力(占槽→emit→spawn_blocking→清槽→取队首续装→终态 emit);`pyenv_install_component` 改为:护栏检查 → 占槽即回 / 入队即回(`queued:true`);`ComponentInstallOutcome` 加 `queued: bool`
- [x] 广播时点补齐:占槽/入队/出队 emit_current(design §1.4 表)
- 验证:`cargo test --manifest-path desktop/src-tauri/Cargo.toml`(既有件零红)

## 2. 状态组装 install_state(pyenv_components.rs / pyenv.rs / main.rs)

- [x] `ComponentStatus` 加 `install_state`/`install_error`;`component_statuses` 加 `runtime: Option<&ComponentsRuntime>` 参(内存态优先,否则戳 error 态)
- [x] `pyenv::status_at` 加第 5 参;`current_status` 组 runtime 传入;`main.rs spawn_sidecar` 传 None;既有单测调用点补 None
- 验证:`cargo test`(新增单测:installing/queued/error 三态组装 + 旧形 None 路不破)

## 3. TS 契约(pyenv-api.ts)

- [x] `PyenvComponent` 加 `install_state?`/`install_error?`;`parsePyenvStatus` 守门(非契约值宽容丢弃)
- [x] `ComponentInstallOutcome` 加 `queued: boolean`;`parseComponentInstallOutcome` 守门
- 验证:`npm --prefix desktop/ui-src run typecheck`(或既有等价脚本,先 `npm run` 看脚本名)

## 4. 前端按钮化(pyenv-card.tsx)

- [x] 新增 `ComponentInstallButton`(design §2.2 状态机表);删 Badge/Switch/旁挂 spinner
- [x] `handleToggleComponent` 重构:off 分支删除;点击 → invoke → 回执 → `applyStatus(await pyenvGetStatus())`;本地 `pendingId` 防双击
- [x] `componentNote` 保留;error 态失败原因小字来自 `install_error`
- 验证:`npm --prefix desktop/ui-src run build` 零错

## 5. 测试重写/新增

- [x] `pyenv-components.test.tsx`:Switch 断言 → 按钮断言;新增用例:安装中禁用转圈/排队中/已装禁用/失败重试可点+原因/envBlocked 禁用
- [x] `pyenv-card.test.tsx`:事件载荷带 `install_state` → 按钮态随新;回包 `queued:true` 后拉取
- [x] Rust 单测:入队去重(同 id 双点)、槽清空续装接力、回包 queued 形状
- 验证:同步骤 6

## 6. 全量门禁 + 冒烟

- [x] `cargo test --manifest-path desktop/src-tauri/Cargo.toml` 全绿
- [x] 前端门禁(vitest 全量 + tsc + build)零新红
- [ ] 真壳沙箱冒烟(MYIA_HOME 临时根 GUI 实跑):不可 CI 化,并入 AC7 装机验证一并做(等效覆盖已落:vitest 23 用例含受理/排队/事件全链/error 重试,cargo 纯函数测含 install_state 组装与原子转移)
- [x] review gate:提交前 `gitnexus detect-changes -r shishi --scope staged`(WAL 恢复态空输出先 `gitnexus analyze --index-only`)

## 回滚点

单 commit 面;任一步骤红 → 停在当步修复,不跨步续写。
