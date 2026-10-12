# Design:组件安装状态进按钮 + 排队自动装

对齐源:`desktop/src-tauri/src/pyenv_components.rs`(组件域)、`pyenv.rs`(status 组装/事件)、`desktop/ui-src/src/screens/settings/pyenv-card.tsx`(组件行 UI)、`pyenv-api.ts`(IPC 契约 TS 守门)。

## 1. 壳侧(Rust)

### 1.1 ComponentManager 队列化(pyenv_components.rs)

```rust
pub struct ComponentManager {
    pub installing: Mutex<Option<String>>,     // 既有:单飞槽
    pub queued: Mutex<VecDeque<String>>,       // 新增:FIFO 排队(id 去重)
}
```

单飞护栏不变(同刻一个 pip);排队是槽外的等待区。

### 1.2 pyenv_install_component 改造(同文件 ~1303)

现流程:注册表对 id → 环境在位护栏 → 主链护栏 → **槽被占 → Err(弹错)** → 占槽 spawn_blocking → await → 清槽 → emit。

新流程:

```
注册表对 id → 环境在位护栏 → 主链护栏
→ 尝试占槽:
    槽空 → 占槽 → emit_current ←(新增:开装即广播,前端即时见 installing)
              → spawn_blocking(install_component) → await → 清槽
              → 队列非空 → 取队首 → 占槽 → emit_current → spawn 续装(递归同构)
              → emit_current(终态,既有)
    槽被占(装的或队的含本 id)→ 入队(去重:已在装/已在队 = 幂等回执)
              → emit_current → Ok({id, installed:false, queued:true})
```

实现要点:

- **落地形态(复审后定案)**:续装逻辑为 `spawn_component_install_chain(app, first_id)`——命令只 spawn 这条链,链内 loop 自续(初稿的「命令入口与续装共用占槽函数」未采用:受理三态判断在命令锁段内联,链体每轮重解析注册表)。**终态转移原子化**:`ComponentRuntime::release_and_claim_next`(一次锁内释放当前槽+占队首)——分两次锁的间隙会被命令入口插队占槽,接力随后的占槽即双 pip 并发(复审 grill 抓出的竞态);链中止走 `abort_all`(槽+队列全清,排队件不滞留假排队)。
- **命令回包不再等待安装完成**:占槽/入队后立即回,完成态全靠事件+拉取。`ComponentInstallOutcome` 加 `queued: bool`(serde 恒在场,TS 守门同步);`installed` 在回包时点恒 false(真相源=戳/状态),语义改为"已受理"。
- 既有 `installing.await` 的 Err(join 失败)分支保留落 error 戳路径(install_component 内部 fail 闭包写戳;join panic 在链内补写戳)。
- 锁纪律不变:锁只在占槽/查队/终态转移瞬间 held,pip 在 spawn_blocking,emit 在锁外。

### 1.3 状态组装带 install_state(pyenv_components.rs ~1126 / pyenv.rs status_at)

```rust
pub struct ComponentStatus {
    pub id: String,
    pub installed: bool,
    pub kind: Option<String>,              // 既有
    pub install_state: Option<String>,     // 新:"installing"|"queued"|"error"|None
    pub install_error: Option<String>,     // 新:仅 error 态非空(戳 error 原文)
}
```

- 内存态优先:installing/queued 来自 `ComponentManager`;否则读戳 `state==Some("error")` → `install_state=Some("error")` + 原文。ready/无戳 → None。
- **爆炸半径对策(impact 实测 CRITICAL 后定案)**:`status_at`/`component_statuses` 签名**不动**(status_at 上游 15 符号/6 执行流零触碰);install_state 改在 `pyenv::current_status` 里后置拼装——纯函数 `apply_components_runtime(&mut [ComponentStatus], Option<&ComponentsRuntime>, &Path)`:内存态(installing/queued)优先,否则戳 `state==Some("error")` → `install_state=Some("error")` + `install_error`=戳原文。ready/无戳 → None。`ComponentsRuntime { installing: Option<String>, queued: Vec<String> }` 从 `app.state::<ComponentManager>()` 快照。
- `main.rs spawn_sidecar` 不动(不消费 components 内容);`emit_current` 走 `current_status` 自动带新键。
- 契约兼容:附加键向后兼容(轨B `kind` 先例);老壳(无新键)→ TS 守门宽容回 null。

### 1.4 广播时点

| 时点 | 既有/新增 |
|------|----------|
| 占槽开装 | **新增** emit_current |
| 入队/幂等回执 | **新增** emit_current |
| 出队续装 | **新增** emit_current |
| 装完/失败终态 | 既有(pyenv_components.rs:1366) |

## 2. 前端(TS/TSX)

### 2.1 契约(pyenv-api.ts)

- `PyenvComponent` 加 `install_state?: "installing" | "queued" | "error"`、`install_error?: string | null`;`parsePyenvStatus` 守门:非契约值丢弃回 undefined/null(宽容口径同既有)。
- `ComponentInstallOutcome` 加 `queued: boolean`(守门:number/string 形即抛,同 id/installed 口径)。

### 2.2 组件行按钮化(pyenv-card.tsx ~611-745)

删除:`Badge`(已装/未装)、`Switch`、旁挂 `busy` spinner 行(`installingComponent` 本地态退防双击过渡,不再驱动渲染主体)。

新增 `<ComponentInstallButton>`(屏内组件,不入共享层):状态机按 `component.install_state` + `component.installed` + `envBlocked`:

| 判据(优先序) | 渲染 |
|------|------|
| `install_state==="installing"` | 禁用 + spinner + 「安装中…」,title「下载依赖+按需拉浏览器,可能耗时数分钟」 |
| `install_state==="queued"` | 禁用 + 「排队中…」,title「等前面的组件装完自动开装」 |
| `installed` | 禁用 + outline ok + 「已装」,title「卸载将在后续版本提供;停用请调整品类/源配置不再引用」 |
| `install_state==="error"` | 警告态可点 + 「重试安装」;行下方失败原因小字(`install_error`) |
| 其余(未装) | 主按钮可点 + 「安装」 |
| `envBlocked`(not_configured/installing) | 以上各态一律禁用,title 前缀「先完成 Python 环境配置」 |

- 点击 → `pyenvInstallComponent(id)` → 回执后 `applyStatus(await pyenvGetStatus())` 拉真值(既有惯例);点击间隙本地 `pendingId` 防双击。
- `handleToggleComponent` 的 off 分支(卸载提示 note)随 Switch 删除而消亡;`componentNote` 保留成功/失败回执小字(error 态常驻来自 status,非 note)。
- 已装服务组件行(启停按钮+健康点)不动;未装服务组件走同一 `ComponentInstallButton`。

### 2.3 事件消费

既有 `onPyenvStatusChanged` 订阅(pyenv-card.tsx:262)已把事件载荷 `applyStatus`——install_state 随载荷自动进组件行,零新增通道。

## 3. 兼容与风险

- **wire 兼容**:components[] 只增可选键;`ComponentInstallOutcome` 加 `queued` 后,老前端(不识)忽略、新前端对老壳缺键 → 守门宽容。回包语义变化(不等装完)只影响本仓前端,同版本发布。
- **壳重启**:内存队列丢;在装组件若戳未落 → 显示未装/可重试,重试幂等(pip 已装跳过、chromium 续装)——既有幂等链兜底,PRD 边界在案。
- **多窗口竞态**:入队去重 + 槽单点,无 TOCTOU 面(锁内查+改)。
- **测试面**:`pyenv-components.test.tsx` 的 Switch 断言全量重写为按钮断言;`pyenv-card.test.tsx` 事件通道复用加 install_state 用例;Rust 侧 `status_at` 新参数的单测调用点补 None 占位。

## 4. 回滚

单 commit 面(Rust 壳 + 前端 + 测试),revert 即回旧交互;无数据迁移、无 schema 变更,戳格式不变。
