/**
 * Python 运行环境 IPC 封装(10-05-desktop-managed-py-env 第 4 步建、第 6 步扩:
 * 消费方 = 设置屏 Python 环境分区 + 全局存量迁移横幅 components/layout/
 * migration-banner.tsx;invoke 直连 + 错误归一化走 ./api 的 asSidecarError,
 * 共享客户端 @/lib/api 只读不动)。
 *
 * 契约(波次钉死,与壳侧 src-tauri/src/pyenv*.rs 逐字段对齐):
 * - command `pyenv_get_status` → `{state, install_path, python_path,
 *   mirror_runtime, mirror_pypi, steps:[{phase,status,error}],
 *   components:[{id,installed}]}`(components = 10-05-table-restore R4 扩展,
 *   注册表缺位回空表)
 *   state = not_configured|installing|ready|error|deps_stale(IPC 五态)
 * - command `pyenv_start_setup(mirror_runtime?, mirror_pypi?)` —— 前端参数键
 *   按 tauri 默认映射传 camelCase(mirrorRuntime/mirrorPypi,pyenv.rs 命令注释
 *   同口径);整体替换式落盘,空串归一为缺省(= 清回默认源)
 * - command `pyenv_sync_deps()`(D4 依赖漂移时的一键幂等重跑)
 * - command `pyenv_verify()`(10-05 主人判例,就绪态「检查状态」:三查=python
 *   可执行/依赖指纹/sidecar 握手,只读零副作用 → `{ok, checks:[{id,ok,detail}]}`)
 * - command `pyenv_install_component(id)`(10-05-table-restore R4:装可选组件
 *   进自管环境;壳侧 pyenv_components.rs)
 * - command `pyenv_migration_banner()`(第 6 步 D5/design §6:存量迁移一次性
 *   引导,查询即消费 —— {show:true} 每数据根至多一次,壳侧标记落盘;
 *   pyenv_migration.rs 为对齐源)
 * - event `pyenv-status-changed`(载荷同 status 形态;前端初始化仍以拉取
 *   `pyenv_get_status` 为准,事件只作变更通知)
 */
import { invoke } from "@tauri-apps/api/core";
import { listen, type UnlistenFn } from "@tauri-apps/api/event";

/** 状态变更事件名(与壳侧 pyenv.rs `PYENV_STATUS_EVENT` 常量一致)。 */
export const PYENV_STATUS_EVENT_NAME = "pyenv-status-changed";

/** 环境五态(IPC 契约:`not_configured|installing|ready|error|deps_stale`) */
const PYENV_STATES = ["not_configured", "installing", "ready", "error", "deps_stale"] as const;
export type PyenvState = (typeof PYENV_STATES)[number];

/** 安装链阶段(design §3 状态机;steps[].phase,固定五阶段) */
const PYENV_PHASES = ["downloading", "verifying", "extracting", "installing_deps", "selfcheck"] as const;
export type PyenvPhase = (typeof PYENV_PHASES)[number];

/** 单阶段状态(steps[].status;skipped = 幂等重试时已装步跳过) */
const PYENV_STEP_STATUSES = ["pending", "running", "done", "skipped", "failed"] as const;
export type PyenvStepStatus = (typeof PYENV_STEP_STATUSES)[number];

/** 安装链单阶段(IPC 契约:`{phase, status, error}`;error 恒在场,无错为 null)。 */
export interface PyenvStep {
  phase: PyenvPhase;
  status: PyenvStepStatus;
  error: string | null;
}

/**
 * `pyenv_get_status` 结果 / `pyenv-status-changed` 事件共用载荷
 * (IPC 契约波次钉死;属性名保持 wire 形 snake_case,惯例同 types.ts)。
 */
export interface PyenvStatus {
  state: PyenvState;
  /** 安装路径:`<数据根>/python`(install_only 解压即得) */
  install_path: string;
  /** Python 使用路径:mac `<数据根>/python/bin/python3`(win 为 python.exe) */
  python_path: string;
  /** 运行时下载源覆盖(当前生效值;null = 默认 manifest 钉版源) */
  mirror_runtime: string | null;
  /** PyPI index 覆盖(当前生效值;null = 默认 PyPI) */
  mirror_pypi: string | null;
  steps: PyenvStep[];
  /**
   * 可选组件实况(10-05-table-restore R4 扩展;注册表缺位回空表)。
   * 两键形态契约钉死:{id, installed}——展示文案(label/description)是
   * 前端展示层的事(注册表本体只在壳侧消费)。
   */
  components: PyenvComponent[];
}

/** 可选组件(自管环境按需 pip 装;壳侧 pyenv_components.rs 对齐源)。 */
export interface PyenvComponent {
  id: string;
  installed: boolean;
}

/** 安装链全阶段有序表(安装明细逐项渲染的骨架;steps 只补状态)。 */
export const PYENV_PHASE_ORDER: readonly PyenvPhase[] = PYENV_PHASES;

function asStringOrNone(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

/**
 * wire 载荷 → PyenvStatus(IPC 契约的 TS 侧守门):
 * state 非契约值即抛(壳侧 serde 已钉死,出现即对齐破了,大声失败);
 * steps/components 附加字段宽容忽略、未知 phase 丢弃、未知 status 按 pending
 * 处理(与壳侧读 python-env.json 的宽容口径一致,坏行不拦状态展示;
 * components 缺键回空表 = 旧壳兼容,条目非 {id:string, installed:boolean}
 * 形即丢弃)。
 */
export function parsePyenvStatus(raw: unknown): PyenvStatus {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`pyenv status 载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (!PYENV_STATES.includes(record.state as PyenvState)) {
    throw new TypeError(`pyenv status.state 非契约值: ${String(record.state)}`);
  }
  const steps = Array.isArray(record.steps)
    ? record.steps.flatMap((entry): PyenvStep[] => {
        if (typeof entry !== "object" || entry === null) return [];
        const step = entry as Record<string, unknown>;
        if (!PYENV_PHASES.includes(step.phase as PyenvPhase)) return [];
        return [
          {
            phase: step.phase as PyenvPhase,
            status: PYENV_STEP_STATUSES.includes(step.status as PyenvStepStatus)
              ? (step.status as PyenvStepStatus)
              : "pending",
            error: asStringOrNone(step.error),
          },
        ];
      })
    : [];
  const components = Array.isArray(record.components)
    ? record.components.flatMap((entry): PyenvComponent[] => {
        if (typeof entry !== "object" || entry === null) return [];
        const component = entry as Record<string, unknown>;
        if (typeof component.id !== "string" || typeof component.installed !== "boolean") return [];
        return [{ id: component.id, installed: component.installed }];
      })
    : [];
  return {
    state: record.state as PyenvState,
    install_path: typeof record.install_path === "string" ? record.install_path : "",
    python_path: typeof record.python_path === "string" ? record.python_path : "",
    mirror_runtime: asStringOrNone(record.mirror_runtime),
    mirror_pypi: asStringOrNone(record.mirror_pypi),
    steps,
    components,
  };
}

/**
 * 镜像覆盖归一(与壳侧 normalize_mirror 同口径):trim;空串 = 缺省
 * (= 清回默认源,不传该键;tauri Option<String> 参数缺省即 None)。
 */
function normalizeMirror(value: string | undefined): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

/** 环境状态查询(前端初始化以此为准,事件只作变更通知)。 */
export async function pyenvGetStatus(): Promise<PyenvStatus> {
  return parsePyenvStatus(await invoke("pyenv_get_status"));
}

/** 开始配置(D2:显式动作;镜像覆盖随本次动作整体替换式保存)。 */
export async function pyenvStartSetup(
  params: { mirrorRuntime?: string; mirrorPypi?: string } = {},
): Promise<PyenvStatus> {
  const mirrorRuntime = normalizeMirror(params.mirrorRuntime);
  const mirrorPypi = normalizeMirror(params.mirrorPypi);
  return parsePyenvStatus(
    await invoke("pyenv_start_setup", {
      ...(mirrorRuntime !== undefined ? { mirrorRuntime } : {}),
      ...(mirrorPypi !== undefined ? { mirrorPypi } : {}),
    }),
  );
}

/** 同步依赖(D4:依赖漂移时的一键幂等重跑安装链)。 */
export async function pyenvSyncDeps(): Promise<PyenvStatus> {
  return parsePyenvStatus(await invoke("pyenv_sync_deps"));
}

/**
 * `pyenv_install_component` 结果(10-05-table-restore R4;壳侧
 * pyenv_components.rs 对齐源)。error 恒在场,无错为 null——安装失败也走
 * Ok 回包(installed=false + error 明细如实),仅传输/护栏层拒绝走 Err。
 */
export interface ComponentInstallOutcome {
  id: string;
  installed: boolean;
  error: string | null;
}

/**
 * wire 载荷 → ComponentInstallOutcome(TS 侧守门):id/installed 非契约类型
 * 即抛(壳侧 serde 已钉死,出现即对齐破了,大声失败,同 parsePyenvStatus 口径)。
 */
export function parseComponentInstallOutcome(raw: unknown): ComponentInstallOutcome {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`组件安装结果载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.id !== "string" || typeof record.installed !== "boolean") {
    throw new TypeError(
      `组件安装结果非契约形态({id, installed, error}): ${String(raw)}`,
    );
  }
  return { id: record.id, installed: record.installed, error: asStringOrNone(record.error) };
}

/** 装组件进自管环境(设置屏组件开关消费;PyPI 镜像覆盖继承 pyenv-settings)。 */
export async function pyenvInstallComponent(id: string): Promise<ComponentInstallOutcome> {
  return parseComponentInstallOutcome(await invoke("pyenv_install_component", { id }));
}

/**
 * `pyenv_migration_banner` 结果(D5/design §6:存量迁移一次性引导)。
 * 查询即消费:壳侧命中「旧数据根 && 无 python-env.json && 未引导过」即落
 * 标记并回 show=true —— 同一数据根上此后恒 false(含重启),AC5「出现且
 * 仅出现一次」由壳侧钉死,前端只如实渲染。
 */
export interface MigrationBannerDecision {
  show: boolean;
}

/**
 * wire 载荷 → MigrationBannerDecision(TS 侧守门):show 非布尔即抛
 * (壳侧 serde 已钉死,出现即对齐破了,大声失败,同 parsePyenvStatus 口径)。
 */
export function parseMigrationBannerDecision(raw: unknown): MigrationBannerDecision {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`migration banner 载荷不是对象: ${String(raw)}`);
  }
  const show = (raw as Record<string, unknown>).show;
  if (typeof show !== "boolean") {
    throw new TypeError(`migration banner.show 非布尔: ${String(show)}`);
  }
  return { show };
}

/** 存量迁移一次性引导查询(第 6 步;AppLayout 挂载时调用一次)。 */
export async function pyenvMigrationBanner(): Promise<MigrationBannerDecision> {
  return parseMigrationBannerDecision(await invoke("pyenv_migration_banner"));
}

/**
 * 订阅 `pyenv-status-changed`(载荷同 status 形态,经 parsePyenvStatus 守门);
 * 返回取消订阅函数。载荷不合契约时不静默:交 onMalformed 上屏(默认忽略,
 * 事件态保留上一次已知的好值,拉取仍是唯一真相源)。
 */
export function onPyenvStatusChanged(
  onStatus: (status: PyenvStatus) => void,
  onMalformed: (error: unknown) => void = () => undefined,
): Promise<UnlistenFn> {
  return listen<unknown>(PYENV_STATUS_EVENT_NAME, (event) => {
    try {
      onStatus(parsePyenvStatus(event.payload));
    } catch (error) {
      onMalformed(error);
    }
  });
}

export type { UnlistenFn };

// ---------------------------------------------------------------------------
// 环境体检(10-05 主人判例:就绪态主按钮=「检查状态」,查出错引导重装)
// ---------------------------------------------------------------------------

/** 体检单项(id = python_binary | deps_fingerprint | sidecar_handshake)。 */
export interface PyenvVerifyCheck {
  id: string;
  ok: boolean;
  detail: string;
}

/** `pyenv_verify` 结果(IPC 契约:`{ok, checks:[…]}`;ok = 全部单项通过)。 */
export interface PyenvVerifyResult {
  ok: boolean;
  checks: PyenvVerifyCheck[];
}

/** wire 载荷 → PyenvVerifyResult(TS 侧守门,同 parsePyenvStatus 口径)。 */
export function parsePyenvVerifyResult(raw: unknown): PyenvVerifyResult {
  if (typeof raw !== "object" || raw === null) {
    throw new Error("pyenv_verify 应答非对象");
  }
  const result = raw as { ok?: unknown; checks?: unknown };
  if (typeof result.ok !== "boolean" || !Array.isArray(result.checks)) {
    throw new Error("pyenv_verify 应答形态不符(ok/checks)");
  }
  return {
    ok: result.ok,
    checks: result.checks.map((item) => {
      const check = (item ?? {}) as Record<string, unknown>;
      return {
        id: typeof check.id === "string" ? check.id : "",
        ok: check.ok === true,
        detail: typeof check.detail === "string" ? check.detail : "",
      };
    }),
  };
}

/**
 * 环境体检(就绪态「检查状态」按钮):三查=python 可执行/依赖指纹/
 * sidecar 握手。壳侧只读零副作用(不落戳不翻状态不碰网络);查出错后
 * 的重装入口 = pyenvStartSetup 幂等链。
 */
export async function pyenvVerify(): Promise<PyenvVerifyResult> {
  return parsePyenvVerifyResult(await invoke("pyenv_verify"));
}
