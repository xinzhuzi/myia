import { useSidecarStatus } from "@/hooks/use-sidecar-status";
import {
  Activity,
  ShieldAlert,
  Cpu,
  Eye,
  KeyRound,
  Layers,
  Lightbulb,
  Lock,
  RefreshCw,
  Save,
  Send,
  SlidersHorizontal,
  Stethoscope,
  Trash2,
  Globe,
} from "lucide-react";
import { useCallback, useEffect, useState, type ReactNode } from "react";
import { useSearchParams } from "react-router-dom";

import { LabelHint } from "@/components/label-hint";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import type { DoctorParams, GatesLoadErrorView, GatesView, SidecarRequestError } from "@/lib/api";
import { api } from "@/lib/api";
import { cn } from "@/lib/utils";

import {
  asSidecarError,
  CategoryNodeError,
  deleteSecretByName,
  isSecretRef,
  listSecretNames,
  mutateEnrichField,
  proxySecretName,
  pushSecretName,
  saveCategoryNode,
  saveSecret,
  SECRET_NAME_LLM_API_KEY,
  SECRET_NAME_LLM_BASE_URL,
  validateLlmForm,
  validateProxyForm,
  validatePushForm,
  verifyWithDoctor,
} from "./api";
import type { DoctorVerify, EnrichView, SecretSaveRecord } from "./api";
import { BundledPluginsCard } from "./bundled-plugins-card";
import { DoctorVerifyPanel } from "./doctor-verify";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
import { PyenvCard } from "./pyenv-card";
import { SettingRow } from "./settings-row";
import { UpdaterCard } from "./updater-card";
import { VisionForm } from "./vision-form";

// ---------------------------------------------------------------------------
// D4 结构重做(10-03-ui-deep-imitation,对照 research/teardown-linear-settings
// 第 1/2/5/6 条):左列分区导航(当前项高亮左竖条,URL ?section= 驱动,对应
// 拆解表「路由 settings/:section」——App.tsx 路由面冻结,以查询参数在同一路由
// 内实现同等深链/回退语义)+ 右列每子区一屏(区标题+描述,下堆叠多个 Card,
// 每 Card 一个设置主题)+ 开关行自动保存无按钮、输入类配卡片底部保存条
// (拆解表标注「自创」项,按仓内卡片底栏实现)+ 危险操作单独 Destructive
// Card 置于区页底部二次确认。vision/updater 已有件整卡融入,不重写。
//
// 10-04-ui-kestra-anchor:行式对齐 Kestra settings(结构借自 Apache-2.0
// kestra/ui/src/components/settings/BasicSettings.vue + components/
// {Wrapper,block/Block,block/SettingRow}.vue,借结构改语义):行 =
// SettingRow 横排(label+hint 左/控件右 w-64)、卡内行间 divide-y 细线。
// 不抄:单页无分区导航(我们的分区 ?section= 深链是既有功能面,R5 零改动保留)。
//
// 10-05 版面重排:内容列弃旧版 Wrapper 的 600px 固定窄列,跟 Kestra 现行
// Wrapper.vue 栅格(el-col sm 20/md 18/lg 16/xl 14,offset 居中)——按断点
// 比例流式居中(md 75%/lg 67%/xl 58%),1920 下 ≈950px 居中、两侧留白对称,
// 不再左钉右空;区标题行挂 actions(Kestra Block.vue heading 的 actions 槽),
// 承接无头化后 PageHeader 渲染 null 而丢失的「重新验证」入口。
// ---------------------------------------------------------------------------

/** 通道 → 规范凭据名缺省(target 语义:feishu 卡的 chat_id / tg 的 bot token / webhook 地址 / bark 的 device key / apprise 的目标串) */
const PUSH_SECRET_NAME_BY_CHANNEL: Record<string, string> = {
  feishu_card: "chat_id",
  telegram: "token",
  webhook: "url",
  // bark(10-05-push-bark):target = device key(在 iPhone Bark App 里复制)
  bark: "device_key",
  // apprise(10-05-push-apprise):target = Apprise 目标串(bark://… 等多目标)
  apprise: "targets",
};
type PushChannel = keyof typeof PUSH_SECRET_NAME_BY_CHANNEL;

/**
 * 通道 → 预设凭据位(10-05-push-credential-journey:填一次即可真收推送)。
 * 键 = 环境变量名(钥匙链规范名 myia/push/<键> 与运行时 env: 回退同口径);
 * password 位只写不回显;optional 位留空不保存(不覆盖已录值)。
 */
const PUSH_FIELDS_BY_CHANNEL: Record<
  PushChannel,
  { key: string; label: string; password?: boolean; optional?: boolean; hint: string }[]
> = {
  feishu_card: [
    { key: "FEISHU_APP_ID", label: "App ID", hint: "飞书开放平台 → 开发者后台 → 应用详情" },
    { key: "FEISHU_APP_SECRET", label: "App Secret", password: true, hint: "同应用详情页;保存后 token 自动续期,无需手工换" },
    { key: "FEISHU_CHAT_ID", label: "群 chat_id", optional: true, hint: "可选;消息屏「刷新」列群目录可查;不填则按规则的推送对象" },
  ],
  telegram: [
    { key: "TELEGRAM_BOT_TOKEN", label: "Bot Token", password: true, hint: "@BotFather 建 bot 后回复的令牌" },
    { key: "TELEGRAM_CHAT_ID", label: "chat_id", optional: true, hint: "可选;给 bot 发条消息后消息屏目录自动记下会话" },
  ],
  webhook: [{ key: "MYIA_WEBHOOK_URL", label: "接收端点 URL", hint: "POST JSON 的接收端(自建服务 / n8n 等)" }],
  // bark(10-05-push-bark):iOS 即时推送;唯一凭据位 = device key
  bark: [
    { key: "BARK_DEVICE_KEY", label: "Device Key", password: true, hint: "在 iPhone 的 Bark App 里复制;凭据走 env:/keychain: 引用(保存即入钥匙链)" },
  ],
  // apprise(10-05-push-apprise):统一推送;唯一凭据位 = Apprise 目标串
  apprise: [
    { key: "APPRISE_URL", label: "Apprise 目标串", password: true, hint: "Apprise 原生目标串,如 bark://… 或 pushover://…,逗号或换行分隔多个;凭据走 env:/keychain: 引用(保存即入钥匙链)" },
  ],
};

/** 通道 → 「发送测试」的目标凭据键(push.test target = keychain:myia/push/<键>) */
const PUSH_TEST_TARGET_KEY: Record<PushChannel, string> = {
  feishu_card: "FEISHU_CHAT_ID",
  telegram: "TELEGRAM_CHAT_ID",
  webhook: "MYIA_WEBHOOK_URL",
  bark: "BARK_DEVICE_KEY",
  apprise: "APPRISE_URL",
};
/** 通道 → 下拉显示名(既有通道 = 原名零漂移;bark/apprise 带人话标注) */
const PUSH_CHANNEL_LABELS: Record<PushChannel, string> = {
  feishu_card: "feishu_card",
  telegram: "telegram",
  webhook: "webhook",
  bark: "Bark(iOS 推送)",
  apprise: "Apprise(统一推送)",
};
const PUSH_CHANNELS = Object.keys(PUSH_SECRET_NAME_BY_CHANNEL) as PushChannel[];

/** 分区定义(拆解表第 1 条:通用/视觉/推送/更新/高级) */
interface SettingsSection {
  id: string;
  label: string;
  icon: typeof SlidersHorizontal;
  title: string;
  description: string;
}

const SECTIONS: SettingsSection[] = [
  { id: "general", label: "通用", icon: SlidersHorizontal, title: "通用", description: "LLM 精评与代理池凭据 + doctor 诊断" },
  { id: "push", label: "推送", icon: Send, title: "推送", description: "通道凭据;发送测试验证连通" },
  { id: "vision", label: "视觉", icon: Eye, title: "视觉", description: "看图通道与 OCR + MLX 视觉模型" },
  { id: "gates", label: "门槛件", icon: Lock, title: "门槛件", description: "付费 SaaS / 自有实例 / 分析件:知情启用(fail-closed,缺省全关)" },
  // 10-05-bundled-plugins-install:装机组件分区(随包官方插件件发现/一键装;
  // sidecar plugins.bundled.list/install,契约见 bundled-plugins-api.ts)。
  // 批二(10-05-bundled-plugins-batch2):+卸载(uninstall)与品类 YAML
  // 平铺装(category_install/categories)。
  { id: "installer-plugins", label: "装机组件", icon: Layers, title: "装机组件", description: "随包官方插件件:发现 / 安装 / 重装 / 卸载 + 品类配置平铺装(manifest 校验;品类与补种同落点)" },
  // 10-05-desktop-managed-py-env 第 4 步(D1/D2):Python 运行环境自管区块,
  // 也是 D2 引导空态「一键跳设置」的深链落点(#/settings?section=python-env)
  { id: "python-env", label: "Python 环境", icon: Cpu, title: "Python 运行环境", description: "运行时与依赖按需下载:开始配置 / 双镜像覆盖 / 安装明细 / 同步依赖" },
  { id: "system", label: "系统", icon: Activity, title: "系统", description: "sidecar 连接 + 软件更新 + 凭据管理" },
];
const DEFAULT_SECTION = "general";

interface LlmForm {
  baseUrl: string;
  model: string;
  key: string;
}
interface ProxyForm {
  pool: string;
  value: string;
}
interface PushForm {
  channel: PushChannel;
  scope: string;
  secretName: string;
  value: string;
}

/** 单品类 enrich 行的本地编辑态(model 输入框与 doctor 回显分离) */
interface EnrichRowState {
  modelDraft: string;
  saving: boolean;
}

/**
 * 每卡保存态(D4「每区保存态反馈」):saving / saved(凭据名清单,值不回程)/
 * note(引导入 YAML 类提示)/ error(结构化错误)。状态渲染在卡片底栏保存条内。
 */
type CardSaveState =
  | { kind: "saving" }
  | { kind: "saved"; names: string[]; note: string | null }
  | { kind: "note"; note: string }
  | { kind: "error"; error: SidecarRequestError };

/** 卡片底部保存条:状态反馈在左、保存动作在右(拆解表第 5 条输入类的显式保存) */
function CardSaveBar({
  state,
  savingLabel,
  action,
}: {
  state: CardSaveState | null;
  savingLabel: string;
  action: ReactNode;
}) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-2 border-t border-border/60 pt-3">
      <div className="min-w-0 flex-1">
        {state?.kind === "saving" ? (
          <span role="status" className="text-xs text-muted-foreground">
            {savingLabel}
          </span>
        ) : null}
        {state?.kind === "saved" ? (
          <div role="status" data-testid="save-status" className="text-xs text-ok">
            已写入钥匙链:{state.names.join("、")}(值不回显)
            {state.note ? <span className="mt-0.5 block text-2xs text-muted-foreground">{state.note}</span> : null}
          </div>
        ) : null}
        {state?.kind === "note" ? (
          <p role="note" data-testid="save-note" className="text-xs text-muted-foreground">
            {state.note}
          </p>
        ) : null}
        {state?.kind === "error" ? <ErrorBox error={state.error} /> : null}
      </div>
      {action}
    </div>
  );
}

/**
 * 「评分与反馈」卡片(B3+C11,10-03-v112-desktop-parity;D4 起属「通用」分区)。
 *
 * 品类 schema 无独立 feedback 节 —— 唯一真实存在、带预算护栏、可经 yaml.save
 * 写回品类节的反馈回路开关 = ``enrich.enabled`` + ``enrich.budget_per_run``
 * (LLM 精评/评分回路;design §6 拍板解释)。逐品类:enabled 开关行即时写回
 * (拆解表第 5 条:开关类自动保存无按钮,Linear docs 实证模式)+ model 显式
 * 保存 + budget 只读护栏;push 通道声明指引在「推送」分区; pools 全局配置
 * 写回顺延(yaml-editor 待拍板 3 未定,维持只展示 + 探测)。
 */
function EnrichFeedbackCard({
  enrichSections,
  onSaved,
}: {
  enrichSections: EnrichView[];
  /** 写回成功后回抛 doctor 复核结果(驱动父级回显整体刷新) */
  onSaved: (doctor: DoctorVerify) => void;
}) {
  const [drafts, setDrafts] = useState<Record<string, EnrichRowState>>({});
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const [nodeError, setNodeError] = useState<string | null>(null);
  /** 最近一次写回成功的行内回执(本卡自持,不再走全局横幅) */
  const [status, setStatus] = useState<string | null>(null);

  const rowState = (file: string): EnrichRowState =>
    drafts[file] ?? { modelDraft: "", saving: false };
  const setRowState = (file: string, next: Partial<EnrichRowState>) =>
    setDrafts((prev) => ({
      ...prev,
      [file]: { ...(prev[file] ?? { modelDraft: "", saving: false }), ...next },
    }));

  /** 四步写回:yaml.read → 文本手术 → yaml.save(mtime 锁)→ doctor 复核 */
  const writeNode = useCallback(
    async (file: string, field: "enabled" | "model", value: string, note: string) => {
      setError(null);
      setNodeError(null);
      setStatus(null);
      setRowState(file, { saving: true });
      try {
        const outcome = await saveCategoryNode(file, (content) =>
          mutateEnrichField(content, field, value),
        );
        onSaved(outcome.doctor);
        setStatus(note);
        setDrafts((prev) => {
          const next = { ...prev };
          delete next[file]; // 写回成功:草稿回归 doctor 回显现值
          return next;
        });
      } catch (err) {
        if (err instanceof CategoryNodeError) setNodeError(`${file}:${err.message}`);
        else setError(asSidecarError(err));
      } finally {
        setRowState(file, { saving: false });
      }
    },
    [onSaved],
  );

  return (
    <Card data-testid="enrich-feedback-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Lightbulb className="size-4 text-muted-foreground" />
          评分与反馈
        </CardTitle>
        <CardDescription>
          逐品类 LLM 精评开关(enrich.enabled,切换即写回)+ 预算护栏 + model 写回;反馈的 👍/👎 标记在情报流卡片,统计在仪表盘
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {error ? <ErrorBox error={error} /> : null}
        {nodeError ? (
          <p role="alert" className="text-xs text-destructive" data-testid="enrich-node-error">
            {nodeError}
          </p>
        ) : null}
        {status ? (
          <p role="status" data-testid="enrich-save-status" className="text-xs text-ok">
            {status}
          </p>
        ) : null}
        {enrichSections.length === 0 ? (
          <span className="text-xs text-muted-foreground">
            暂无带 enrich 节的品类(doctor 回显为准);到「配置编辑」为品类补 enrich 节。
          </span>
        ) : (
          /* Kestra SettingRow 扁平化:逐品类 = 开关行 + model 行,行间细线,
             控件右缘与全卡行对齐同一轨(不再嵌套内缩盒) */
          <div className="divide-y divide-border/60">
            {enrichSections.map(({ pluginFile, enrich }) => {
              const row = rowState(pluginFile);
              const modelValue = row.modelDraft || enrich.model;
              const modelDirty = row.modelDraft !== "" && row.modelDraft !== enrich.model;
              return (
                <div key={pluginFile} data-testid={`enrich-row-${pluginFile}`} className="flex flex-col">
                  <SettingRow
                    label={
                      <LabelHint
                        label={pluginFile.split("/").pop() ?? pluginFile}
                        tip="开 = 每条情报交给 AI 打个分再入库。预算护栏限制一轮采集最多花多少钱,超了就停;这里是只读回显,想改数额到「配置编辑」改品类文件里的 budget_per_run。"
                      />
                    }
                    description={`预算护栏 budget_per_run = ${enrich.budget_per_run}(只读,改值走「配置编辑」)`}
                  >
                    <span className="text-2xs text-muted-foreground">
                      {row.saving ? "写回中…" : enrich.enabled ? "精评已启用" : "精评已停用"}
                    </span>
                    {/* 开关行:自动保存无按钮(拆解表第 5 条;Linear 开关即时生效模式) */}
                    <Switch
                      checked={enrich.enabled}
                      disabled={row.saving}
                      aria-label={`精评开关 ${pluginFile}`}
                      title="切换即写回品类 YAML enrich.enabled(yaml.save,注释保真)"
                      onCheckedChange={() =>
                        void writeNode(
                          pluginFile,
                          "enabled",
                          enrich.enabled ? "false" : "true",
                          `${pluginFile} 精评已${enrich.enabled ? "停用" : "启用"}(enrich.enabled 写回,doctor 已复核)。`,
                        )
                      }
                    />
                  </SettingRow>
                  <FieldInput
                    label="enrich.model"
                    aria-label={`精评模型 ${pluginFile}`}
                    placeholder={enrich.model}
                    value={modelValue}
                    hint="写回品类 YAML enrich.model(yaml.save;doctor 回显为现值)"
                    onChange={(event) => setRowState(pluginFile, { modelDraft: event.target.value })}
                    action={
                      <Button
                        size="sm"
                        disabled={!modelDirty || row.saving}
                        title={modelDirty ? "写回 enrich.model" : "与现值一致,无需保存"}
                        onClick={() =>
                          void writeNode(
                            pluginFile,
                            "model",
                            modelValue.trim(),
                            `${pluginFile} enrich.model 已写回(${modelValue.trim()}),doctor 已复核。`,
                          )
                        }
                      >
                        <Save className="size-3.5" />
                        保存 model
                      </Button>
                    }
                  />
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

/**
 * 门槛件分区(10-05-plugin-market-batch 批二第 11 步,R5 尾/D4):gates.yaml
 * 知情启用配置的读写面(sidecar gates.get/save,契约 design.md §6.7)。
 *
 * 三卡:付费通道(paid_engines 总开关 + saas 逐件开关 + 钥匙串键录入——
 * 值只经 secret.set 入钥匙链,配置只存 keychain: 引用,与 vision 云端 key
 * 同门)/ 自有实例(platforms 逐件 endpoint+token 表单)/ 分析件(D8:批二
 * 仅占位,「批三解锁」禁用态,零分析件落地,不是空面)。
 *
 * 文案铁律(design §6.4):每开关挂知情警示(按页计费/目标清单经对方服务
 * 器/组织性不执法);fail-closed:gates.yaml 缺失 = 全关默认态,拒载 =
 * 全关态 + 警示卡(设置屏是修复入口,保存任一卡即合法覆写,entry.py
 * `_m_gates_get` 刻意不 fail fast);传输层失败才整屏 ErrorBox。整份配置
 * 经 gates.save 原子落盘,未知逐件键(community 件)与 third_party_trace
 * (D9:现阶段无执法点,UI 不提供假开关)载荷保真透传,不在保存时丢失。
 */

/** 官方付费 SaaS 件(R6 zenrows/scraperapi;键名与 gates.yaml `saas.<name>`、
 *  引擎词表同口径;知情文案按件挂) */
const GATES_SAAS_ITEMS: { name: string; label: string; note: string }[] = [
  { name: "zenrows", label: "Zenrows", note: "按页计费;开启后目标 URL 经 Zenrows 服务器抓取(永不进自动降级链,仅显式 engine 选用)" },
  { name: "scraperapi", label: "ScraperAPI", note: "按页计费;开启后目标 URL 经 ScraperAPI 服务器抓取(永不进自动降级链,仅显式 engine 选用)" },
];

/** 官方自有实例件(R7 crawlab/worldmonitor remote 桩;token 位按件有无) */
const GATES_PLATFORM_ITEMS: { name: string; label: string; hasToken: boolean }[] = [
  { name: "crawlab", label: "Crawlab", hasToken: true },
  { name: "worldmonitor", label: "worldmonitor", hasToken: false },
];

/** 钥匙串引用规范名(gates.py `canonical_saas_key_ref` / platforms 模板同口径) */
const saasKeyRef = (name: string) => `keychain:myia/saas/${name}-key`;
const platformTokenRef = (name: string) => `keychain:myia/platforms/${name}-token`;

/** 引用 → 钥匙串名(自定义引用跟随;无引用/非引用回落规范名) */
function secretNameFromRef(ref: string | null, fallback: string): string {
  return ref && ref.startsWith("keychain:") ? ref.slice("keychain:".length) : fallback;
}

/** 未配置的官方件物化进编辑态(design §6.1 样例形状:enabled:false + 规范引用;
 *  显式优于隐式,与 gates.py 「创建新件时物化」同口径) */
function materializeGates(view: GatesView): GatesView {
  const saas = { ...view.saas };
  for (const item of GATES_SAAS_ITEMS) {
    if (!saas[item.name]) saas[item.name] = { enabled: false, api_key: saasKeyRef(item.name) };
  }
  const platforms = { ...view.platforms };
  for (const item of GATES_PLATFORM_ITEMS) {
    if (!platforms[item.name]) {
      platforms[item.name] = { enabled: false, endpoint: "", token: item.hasToken ? platformTokenRef(item.name) : null };
    }
  }
  return { ...view, saas, platforms };
}

function GatesForm({
  secretNames,
  onSecretsChanged,
}: {
  /** 设置屏已加载的钥匙链名清单(判逐件 key 是否已存;值永不可读) */
  secretNames: string[] | null;
  /** 凭据写入后回抛刷新(存在性徽标随动) */
  onSecretsChanged: () => void;
}) {
  const [draft, setDraft] = useState<GatesView | null>(null);
  const [path, setPath] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestError | null>(null);
  /** gates.yaml 拒载明细(fail-closed:config 恒为全关态,设置屏是修复入口) */
  const [configError, setConfigError] = useState<GatesLoadErrorView | null>(null);
  const [dirty, setDirty] = useState(false);
  /** 逐卡保存态(与 LLM/推送卡同款 CardSaveBar 反馈) */
  const [paidSave, setPaidSave] = useState<CardSaveState | null>(null);
  const [platformsSave, setPlatformsSave] = useState<CardSaveState | null>(null);
  /** 付费 key / 平台 token 的值输入(只经 secret.set 入钥匙链,保存即清) */
  const [paidValues, setPaidValues] = useState<Record<string, string>>({});
  const [tokenValues, setTokenValues] = useState<Record<string, string>>({});
  /** 平台 endpoint 前端校验(gates.py 同门:http(s) 或空;省一轮协议往返) */
  const [endpointErrors, setEndpointErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const result = await api.gatesGet();
        if (cancelled) return;
        setPath(result.path);
        setConfigError(result.error);
        setDraft(materializeGates(result.config));
      } catch (error) {
        if (!cancelled) setLoadError(asSidecarError(error));
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const patchConfig = useCallback((patch: (prev: GatesView) => GatesView) => {
    setDirty(true);
    setDraft((prev) => (prev === null ? prev : patch(prev)));
  }, []);

  const toggleSaas = useCallback(
    (name: string) =>
      patchConfig((prev) => ({
        ...prev,
        saas: { ...prev.saas, [name]: { ...prev.saas[name], enabled: !prev.saas[name].enabled } },
      })),
    [patchConfig],
  );

  const togglePlatform = useCallback(
    (name: string) =>
      patchConfig((prev) => ({
        ...prev,
        platforms: { ...prev.platforms, [name]: { ...prev.platforms[name], enabled: !prev.platforms[name].enabled } },
      })),
    [patchConfig],
  );

  const setPlatformEndpoint = useCallback(
    (name: string, endpoint: string) => {
      setEndpointErrors((prev) => ({ ...prev, [name]: "" }));
      patchConfig((prev) => ({
        ...prev,
        platforms: { ...prev.platforms, [name]: { ...prev.platforms[name], endpoint } },
      }));
    },
    [patchConfig],
  );

  const hasValueInput = (values: Record<string, string>) =>
    Object.values(values).some((value) => value.trim() !== "");

  /** 整份配置原子保存(gates.save)+ 本卡填了值的凭据先入钥匙链(secret.set)。
   *  失败零写入是后端契约;前端只再拦一道 endpoint 形状(gates.py 同门)。 */
  const saveCard = useCallback(
    async (card: "paid" | "platforms") => {
      if (draft === null) return;
      const setSave = card === "paid" ? setPaidSave : setPlatformsSave;
      if (card === "platforms") {
        const errors: Record<string, string> = {};
        for (const [name, gate] of Object.entries(draft.platforms)) {
          const endpoint = gate.endpoint.trim();
          if (endpoint && !endpoint.startsWith("http://") && !endpoint.startsWith("https://")) {
            errors[name] = "endpoint 须为 http(s) 地址(自有实例占位)";
          }
        }
        setEndpointErrors(errors);
        if (Object.keys(errors).length > 0) return; // 前端拦下,零协议调用
      }
      setSave({ kind: "saving" });
      try {
        const names: string[] = [];
        const valueEntries =
          card === "paid"
            ? Object.entries(paidValues)
            : Object.entries(tokenValues);
        for (const [name, value] of valueEntries) {
          const trimmed = value.trim();
          if (!trimmed) continue; // 留空不覆盖已录值
          const ref =
            card === "paid"
              ? (draft.saas[name]?.api_key ?? null)
              : (draft.platforms[name]?.token ?? null);
          const fallback =
            card === "paid" ? `myia/saas/${name}-key` : `myia/platforms/${name}-token`;
          const record = await saveSecret(secretNameFromRef(ref, fallback), trimmed);
          names.push(record.name);
        }
        if (card === "paid") setPaidValues({});
        else setTokenValues({});
        const result = await api.gatesSave({ config: draft });
        setPath(result.path);
        setConfigError(null); // 合法覆写即修复(设置屏 = fail-closed 的修复入口)
        setDirty(false);
        setSave(
          names.length > 0
            ? { kind: "saved", names, note: `门槛配置已写入 ${result.path}(值不回显)` }
            : { kind: "note", note: `门槛配置已写入 ${result.path}` },
        );
        if (names.length > 0) onSecretsChanged();
      } catch (error) {
        setSave({ kind: "error", error: asSidecarError(error) });
      }
    },
    [draft, paidValues, tokenValues, onSecretsChanged],
  );

  if (loadError !== null) {
    // 传输/协议层失败(method 不达、壳不可用等)如实上屏;gates.yaml 拒载
    // 不走此分支 —— 那是结构化 error 载荷(上方 configError 警示卡)
    return (
      <Card data-testid="gates-load-error">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lock className="size-4 text-muted-foreground" />
            门槛件配置读取失败
          </CardTitle>
          <CardDescription>
            gates.get 未达(sidecar 不可用或协议错误);重进本分区重试,详见下方结构化错误
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ErrorBox error={loadError} />
        </CardContent>
      </Card>
    );
  }
  if (draft === null) {
    return (
      <Card data-testid="gates-loading">
        <CardContent className="pt-6">
          <span className="text-xs text-muted-foreground">门槛配置装载中…</span>
        </CardContent>
      </Card>
    );
  }

  const saasEntries = [
    ...GATES_SAAS_ITEMS.map((item) => item.name),
    ...Object.keys(draft.saas).filter((name) => !GATES_SAAS_ITEMS.some((item) => item.name === name)),
  ];
  const platformEntries = [
    ...GATES_PLATFORM_ITEMS.map((item) => item.name),
    ...Object.keys(draft.platforms).filter((name) => !GATES_PLATFORM_ITEMS.some((item) => item.name === name)),
  ];
  const analysisEntries = Object.entries(draft.analysis);

  return (
    <>
      {/* gates.yaml 拒载警示(fail-closed):config 已按全关处理,但设置屏仍是
          修复入口 —— 保存任一卡 = 用合法配置覆写坏文件(entry.py 刻意不 fail fast) */}
      {configError !== null ? (
        <Card
          data-testid="gates-corrupt-warning"
          className="border-warning/40 bg-warning/[0.04]"
        >
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-warning">
              <ShieldAlert className="size-4" />
              gates.yaml 拒载(fail-closed,已按全关处理)
            </CardTitle>
            <CardDescription>
              门槛件全关继续运行,核心品类不受影响;下方表单以全关默认态渲染,
              保存任一卡将用合法配置覆写修复该文件
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-1 text-2xs text-muted-foreground">
            {configError.errors.map((detail) => (
              <p key={`${detail.path}:${detail.error_type}`}>
                <span className="font-mono">[{detail.error_type}]</span> {detail.path} — {detail.message}
              </p>
            ))}
          </CardContent>
        </Card>
      ) : null}

      {/* 卡一:付费通道(paid_engines 总开关 + saas 逐件 + 钥匙串键录入) */}
      <Card data-testid="gates-paid-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <KeyRound className="size-4 text-muted-foreground" />
            付费通道(付费 SaaS 采集引擎)
          </CardTitle>
          <CardDescription>
            知情启用:按页计费,你的采集目标清单将经对方服务器并与账号绑定;永不缺省、永不进自动降级链(仅显式 engine 选用)
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-1">
          <div className="divide-y divide-border/60">
            <SettingRow
              label="付费通道总开关"
              description="按页计费,你的采集目标清单将经对方服务器(gates.yaml paid_engines;逐件还需各自开启)"
            >
              <Switch
                checked={draft.paid_engines}
                onCheckedChange={() => patchConfig((prev) => ({ ...prev, paid_engines: !prev.paid_engines }))}
                aria-label="付费通道总开关"
                title="知情确认后开启;文件缺失/损坏时 fail-closed 全关"
              />
            </SettingRow>
            {saasEntries.map((name) => {
              const gate = draft.saas[name];
              const official = GATES_SAAS_ITEMS.find((item) => item.name === name);
              const secretName = secretNameFromRef(gate.api_key, `myia/saas/${name}-key`);
              const keyPresent = secretNames?.includes(secretName) ?? false;
              return (
                <div key={name} data-testid={`gates-saas-row-${name}`} className="flex flex-col">
                  <SettingRow label={official?.label ?? name} description={official?.note ?? "付费 SaaS 逐件开关(community 件;按页计费知情)"}>
                    {gate.enabled && secretNames !== null && !keyPresent ? (
                      <Badge variant="destructive" title={`钥匙链缺 ${secretName};开启态调用会因凭据缺失失败`}>
                        钥匙链缺键
                      </Badge>
                    ) : null}
                    <Switch
                      checked={gate.enabled}
                      onCheckedChange={() => toggleSaas(name)}
                      aria-label={`付费引擎开关 ${name}`}
                    />
                  </SettingRow>
                  <FieldInput
                    label="API Key 值"
                    aria-label={`${name} API Key 值`}
                    type="password"
                    autoComplete="new-password"
                    placeholder={`写入 ${secretName};留空不覆盖`}
                    value={paidValues[name] ?? ""}
                    onChange={(event) => setPaidValues((prev) => ({ ...prev, [name]: event.target.value }))}
                    labelHint="密钥只存进系统钥匙串,配置文件里只存一个指名道姓的引用、不存明文。留空保存不会动已录过的旧密钥。"
                    hint={`值只入钥匙链,配置侧存 ${gate.api_key ?? saasKeyRef(name)} 引用(明文引用会被拒载)`}
                  />
                </div>
              );
            })}
          </div>
          <CardSaveBar
            state={paidSave}
            savingLabel="保存中…"
            action={
              <Button
                size="sm"
                onClick={() => void saveCard("paid")}
                disabled={(!dirty && !hasValueInput(paidValues)) || paidSave?.kind === "saving"}
                title={dirty || hasValueInput(paidValues) ? "整份门槛配置原子落盘(gates.save)" : "无改动可保存"}
              >
                <Save className="size-3.5" />
                保存付费通道
              </Button>
            }
          />
          <p className="border-t border-border/60 pt-2 text-2xs text-muted-foreground">
            第三方留痕通道(third_party_trace)= {draft.third_party_trace ? "开" : "关"}:公共 RSSHub
            实例等;现阶段无执法点(D9,保护 = 插件 README 知情文案),经 myssia gates set 配置,保存时原样透传
          </p>
        </CardContent>
      </Card>

      {/* 卡二:自有实例(platforms 逐件 endpoint + token 表单;D6 组织性不执法) */}
      <Card data-testid="gates-platforms-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Globe className="size-4 text-muted-foreground" />
            自有实例(同物种例外通道)
          </CardTitle>
          <CardDescription>
            门槛 = 你自部署的实例 endpoint(Crawlab/worldmonitor 等 remote 桩);MYIA 组织性不执法,不拦你的 direct_api 源(D6)
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-1">
          <div className="divide-y divide-border/60">
            {platformEntries.map((name) => {
              const gate = draft.platforms[name];
              const official = GATES_PLATFORM_ITEMS.find((item) => item.name === name);
              const officialHasToken = official?.hasToken ?? gate.token !== null;
              const tokenName = secretNameFromRef(gate.token, `myia/platforms/${name}-token`);
              return (
                <div key={name} data-testid={`gates-platform-row-${name}`} className="flex flex-col">
                  <SettingRow
                    label={official?.label ?? name}
                    description="接入即知情确认:该实例将收到你的采集目标清单与账号 token(组织性确认,不执法)"
                  >
                    <Switch
                      checked={gate.enabled}
                      onCheckedChange={() => togglePlatform(name)}
                      aria-label={`自有实例开关 ${name}`}
                    />
                  </SettingRow>
                  <FieldInput
                    label="endpoint"
                    aria-label={`${name} endpoint`}
                    placeholder="https://crawlab.example.com"
                    value={gate.endpoint}
                    error={endpointErrors[name] || null}
                    onChange={(event) => setPlatformEndpoint(name, event.target.value)}
                    hint="自部署实例地址(http(s));留空 = 未配置,开关保持知情确认态"
                  />
                  {officialHasToken ? (
                    <FieldInput
                      label="Token 值"
                      aria-label={`${name} Token 值`}
                      type="password"
                      autoComplete="new-password"
                      placeholder={`写入 ${tokenName};留空不覆盖`}
                      value={tokenValues[name] ?? ""}
                      onChange={(event) => setTokenValues((prev) => ({ ...prev, [name]: event.target.value }))}
                      hint={`值只入钥匙链,配置侧存 ${gate.token ?? platformTokenRef(name)} 引用`}
                    />
                  ) : null}
                </div>
              );
            })}
          </div>
          <CardSaveBar
            state={platformsSave}
            savingLabel="保存中…"
            action={
              <Button
                size="sm"
                onClick={() => void saveCard("platforms")}
                disabled={(!dirty && !hasValueInput(tokenValues)) || platformsSave?.kind === "saving"}
                title={dirty || hasValueInput(tokenValues) ? "整份门槛配置原子落盘(gates.save)" : "无改动可保存"}
              >
                <Save className="size-3.5" />
                保存自有实例
              </Button>
            }
          />
        </CardContent>
      </Card>

      {/* 卡三:分析件(D8:批二仅 schema+占位,「批三解锁」禁用态,不是空面) */}
      <Card data-testid="gates-analysis-card">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Lightbulb className="size-4 text-muted-foreground" />
            分析件(停更知情)
          </CardTitle>
          <CardDescription>
            批二零分析件落地(D8):批三解锁时每开关将挂「上游冻结,pin 版自担维护」知情警示;分析 lane 挂点(classify 后处理还是 enrich 平行)随批三质询定案
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="divide-y divide-border/60">
            {analysisEntries.length === 0 ? (
              <SettingRow
                label="分析件"
                description="停更知情型分析件(snownlp 情感等)批三解锁;gates.analysis schema 已就位,配置经 myssia gates set 可达"
              >
                <Badge variant="outline">批三解锁</Badge>
              </SettingRow>
            ) : (
              analysisEntries.map(([name, on]) => (
                <SettingRow key={name} label={name} description="批三解锁前只读(D8:仅 schema+设置面占位,不提供开关)">
                  <span className="text-2xs text-muted-foreground">{on ? "已启用" : "已停用"}</span>
                  <Badge variant="outline">批三解锁</Badge>
                </SettingRow>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      <p className="text-2xs text-muted-foreground">
        门槛铁律:开关只落全局 {path ?? "gates.yaml"}(不进品类 YAML,AI 生成配置不可能无意开启付费通道);
        文件缺失/损坏 = 全关 + doctor 提示;门槛件任何失败(含引擎 gate_closed)不拦核心品类。
      </p>
    </>
  );
}

/**
 * 设置(D4 结构重做后):左分区导航(通用/视觉/推送/更新/高级)+ 右侧当前分区
 * 表单卡片列。LLM(base_url/model/key)/ 代理池 / 推送通道三个凭据表单 +
 * doctor 验证回显;vision/updater 已有件按分区融入。
 *
 * 铁律落地:key 类输入只经 sidecar secret.set 写入系统钥匙链 —— 值不进组件
 * 持久状态(保存即清)、不经任何 DOM/日志回显;「保存成功」的唯一证据是
 * doctor 回显面板里凭据存在性核验(✓ 已在钥匙链)。model / 池 URL 结构 /
 * 通道声明属品类或全局 YAML(非凭据),其写回是 sidecar 协议缺口(与源管理
 * sources.write 同一缺口),界面如实标注,不伪造保存成功。
 */
export function SettingsScreen() {
  /** 分区态走 URL 查询参数(?section=vision):深链/回退语义对齐拆解表第 1 条 */
  const [searchParams, setSearchParams] = useSearchParams();
  const rawSection = searchParams.get("section");
  const sectionId = SECTIONS.some((section) => section.id === rawSection)
    ? (rawSection as string)
    : DEFAULT_SECTION;
  const activeSection = SECTIONS.find((section) => section.id === sectionId) ?? SECTIONS[0];

  /** 分区过滤(10-04-interaction-batch 补做,census 缺口 #7「设置搜索设置项」:
   *  Linear settings 口径——分区导航上方过滤框实时过滤分区名,纯前端零 RPC)。
   *  匹配 label/id 不分大小写(拉丁输入可按 id 命中,如 vision→视觉);
   *  只影响导航可见性:不改当前分区,URL ?section= 深链语义不动。 */
  const [sectionFilter, setSectionFilter] = useState("");
  const sectionQuery = sectionFilter.trim().toLowerCase();
  const visibleSections = sectionQuery
    ? SECTIONS.filter(({ id, label }) => label.toLowerCase().includes(sectionQuery) || id.includes(sectionQuery))
    : SECTIONS;

  const [llm, setLlm] = useState<LlmForm>({ baseUrl: "", model: "", key: "" });
  const [llmErrors, setLlmErrors] = useState<Partial<Record<"baseUrl", string>>>({});
  const [proxy, setProxy] = useState<ProxyForm>({ pool: "", value: "" });
  const [proxyErrors, setProxyErrors] = useState<Partial<Record<"pool" | "value", string>>>({});
  const [probePath, setProbePath] = useState("");
  const [push, setPush] = useState<PushForm>({ channel: "feishu_card", scope: "", secretName: "chat_id", value: "" });
  const [pushErrors, setPushErrors] = useState<Partial<Record<"scope" | "secretName" | "value", string>>>({});
  /** 预设凭据位值(10-05-push-credential-journey):{ENV_KEY: 值},按通道字段集读写 */
  const [pushValues, setPushValues] = useState<Record<string, string>>({});

  /** 每卡独立保存态(D4:每区保存态反馈;替代旧全局横幅) */
  const [llmSave, setLlmSave] = useState<CardSaveState | null>(null);
  const [proxySave, setProxySave] = useState<CardSaveState | null>(null);
  const [pushSave, setPushSave] = useState<CardSaveState | null>(null);

  const [verify, setVerify] = useState<DoctorVerify | null>(null);
  const [verifying, setVerifying] = useState(false);
  const [verifyError, setVerifyError] = useState<SidecarRequestError | null>(null);
  const [secretNames, setSecretNames] = useState<string[] | null>(null);
  /** C5:已点击删除、待二次确认的凭据名(inline confirm,同看图模型卡惯例) */
  const [deletingSecret, setDeletingSecret] = useState<string | null>(null);
  const [deleteError, setDeleteError] = useState<SidecarRequestError | null>(null);

  const refreshSecretNames = useCallback(async () => {
    try {
      setSecretNames(await listSecretNames());
    } catch {
      setSecretNames(null); // 名清单失败不拦主流程(doctor 回显仍在)
    }
  }, []);

  const runDoctor = useCallback(async (params?: DoctorParams) => {
    setVerifying(true);
    setVerifyError(null);
    try {
      setVerify(await verifyWithDoctor(params));
    } catch (error) {
      setVerifyError(asSidecarError(error));
    } finally {
      setVerifying(false);
    }
  }, []);

  /** C5:删除凭据 → 刷新名清单 + doctor 复核(secret_not_found 等结构化上屏)。 */
  const handleDeleteSecret = useCallback(
    async (name: string) => {
      setDeleteError(null);
      try {
        await deleteSecretByName(name);
        setDeletingSecret(null);
        await refreshSecretNames();
        await runDoctor();
      } catch (error) {
        setDeleteError(asSidecarError(error));
      }
    },
    [refreshSecretNames, runDoctor],
  );

  useEffect(() => {
    void runDoctor();
    void refreshSecretNames();
  }, [runDoctor, refreshSecretNames]);

  const handleLlmSave = useCallback(async () => {
    const formError = validateLlmForm(llm);
    if (formError === "base_url_invalid") {
      setLlmErrors({ baseUrl: "base_url 须为 http(s) 地址或 env:/keychain: 引用" });
      return;
    }
    setLlmErrors({});
    setLlmSave({ kind: "saving" });
    try {
      const saved: SecretSaveRecord[] = [];
      let note: string | null = null;
      const base = llm.baseUrl.trim();
      if (base && isSecretRef(base)) {
        // 引用本身只该出现在 YAML/env;界面不代写、也不把它当值入钥匙链
        note = "base_url 是 env:/keychain: 引用:请把该引用直接写入品类 YAML enrich.base_url(品类 YAML 写回属协议缺口,见 openIssues)。";
      } else if (base) {
        saved.push(await saveSecret(SECRET_NAME_LLM_BASE_URL, base));
        note = "base_url 值已入钥匙链;品类 YAML 侧以 keychain:myia/llm/base_url 引用(schema 只收引用,端点值不落盘)。";
      }
      if (llm.key) {
        saved.push(await saveSecret(SECRET_NAME_LLM_API_KEY, llm.key));
      }
      // 有写入 → 凭据名回执;纯引用提示 → note(与旧全局横幅两种形态同口径)
      setLlmSave(
        saved.length > 0
          ? { kind: "saved", names: saved.map((record) => record.name), note }
          : { kind: "note", note: note ?? "未填写可保存的凭据值。" },
      );
      setLlm((prev) => ({ ...prev, key: "" })); // key 保存即清:不留存、不回显
      await runDoctor();
      await refreshSecretNames();
    } catch (error) {
      setLlmSave({ kind: "error", error: asSidecarError(error) });
    }
  }, [llm, refreshSecretNames, runDoctor]);

  const handleProxySave = useCallback(async () => {
    const formError = validateProxyForm(proxy);
    if (formError === "pool_invalid") {
      setProxyErrors({ pool: "池名须为字母/数字/连字符/下划线(与 pool:<名称> 语法同口径)" });
      return;
    }
    if (formError === "value_empty") {
      setProxyErrors({ value: "凭据值必填" });
      return;
    }
    setProxyErrors({});
    setProxySave({ kind: "saving" });
    try {
      const record = await saveSecret(proxySecretName(proxy.pool.trim()), proxy.value);
      setProxySave({
        kind: "saved",
        names: [record.name],
        note: "池凭据已入钥匙链;全局 pools YAML 侧以 keychain:myia/proxy/<pool> 引用(池 URL 结构写回属协议缺口)。",
      });
      setProxy((prev) => ({ ...prev, value: "" }));
      await runDoctor();
      await refreshSecretNames();
    } catch (error) {
      setProxySave({ kind: "error", error: asSidecarError(error) });
    }
  }, [proxy, refreshSecretNames, runDoctor]);

  /** G10(10-05-g10-proxy-probe):探测两态——路径非空走显式 config(现状),
   *  留空走 config_auto 由 sidecar 发现 <数据根>/pools.yaml;autoMiss 记住
   *  「最近一次探测是自动态」,doctor 应答无新键,未命中提示行靠它 gating
   *  (挂载初始/保存后刷新不发 config_auto,不冒「未找到」)。 */
  const [probeAutoMiss, setProbeAutoMiss] = useState(false);
  const handleProbe = useCallback(async () => {
    const path = probePath.trim();
    setProbeAutoMiss(!path);
    await runDoctor(path ? { config: path } : { config_auto: true });
  }, [probePath, runDoctor]);

  const handlePushSave = useCallback(async () => {
    const formError = validatePushForm(push);
    if (formError === "scope_invalid") {
      setPushErrors({ scope: "scope 须为品类 id 规则:小写字母/数字开头,可含连字符" });
      return;
    }
    if (formError === "name_invalid") {
      setPushErrors({ secretName: "凭据名段须为字母/数字开头,可含点/连字符/下划线" });
      return;
    }
    if (formError === "value_empty") {
      setPushErrors({ value: "凭据值必填" });
      return;
    }
    setPushErrors({});
    setPushSave({ kind: "saving" });
    try {
      const record = await saveSecret(pushSecretName(push.scope.trim(), push.secretName.trim()), push.value);
      setPushSave({
        kind: "saved",
        names: [record.name],
        note: "通道凭据已入钥匙链;品类 YAML push[].target 侧以 keychain:myia/<scope>/<name> 引用(通道声明写回属协议缺口)。",
      });
      setPush((prev) => ({ ...prev, value: "" }));
      await runDoctor();
      await refreshSecretNames();
    } catch (error) {
      setPushSave({ kind: "error", error: asSidecarError(error) });
    }
  }, [push, refreshSecretNames, runDoctor]);

  /** G5 前半(10-03-feed-ux):push.test 真发一条测试消息(channel 取表单当前
   *  选中;scope 已填则 target 引用 keychain:myia/<scope>/<secretName>,缺省
   *  走通道默认 env 引用链)。结果行内回显:成功 ok 徽标 / 结构化错误。 */
  const [pushTesting, setPushTesting] = useState(false);
  const [pushTestNote, setPushTestNote] = useState<string | null>(null);
  const [pushTestOk, setPushTestOk] = useState<boolean | null>(null);

  const handlePushTest = useCallback(async (explicitTarget?: string) => {
    setPushTesting(true);
    setPushTestNote(null);
    setPushTestOk(null);
    // target 引用:显式传入(预设位)优先;否则自定义位 scope/凭据名齐全才组;
    // 都无则让通道走默认 env 链(env 缺失时运行时自动回退钥匙链规范名)
    let target = explicitTarget;
    if (!target) {
      const scope = push.scope.trim();
      const name = push.secretName.trim() || PUSH_SECRET_NAME_BY_CHANNEL[push.channel] || "";
      target = scope && name ? `keychain:myia/${scope}/${name}` : undefined;
    }
    try {
      const result = await api.pushTest({ channel: push.channel, ...(target ? { target } : {}) });
      setPushTestOk(true);
      setPushTestNote(
        result.preview
          ? `测试消息已发(stdout 通道预览):${result.preview.slice(0, 200)}`
          : `测试消息已发(${result.channel})——请到对应客户端查收。`,
      );
    } catch (error) {
      const failure = asSidecarError(error);
      setPushTestOk(false);
      setPushTestNote(`发送失败(${failure.code}):${failure.message}`);
    } finally {
      setPushTesting(false);
    }
  }, [push.channel, push.scope, push.secretName]);

  /** 预设凭据位保存(10-05-push-credential-journey):逐非空字段写
   *  myia/push/<ENV_KEY>;空字段跳过不覆盖(清除走危险区 secret.delete)。 */
  const handlePresetSave = useCallback(async () => {
    const fields = PUSH_FIELDS_BY_CHANNEL[push.channel];
    const entries = fields
      .map((field) => ({ field, value: (pushValues[field.key] ?? "").trim() }))
      .filter((entry) => entry.value !== "");
    if (entries.length === 0) {
      setPushSave({ kind: "note", note: "至少填一个字段再保存;留空的字段不会覆盖已录入的值。" });
      return;
    }
    setPushSave({ kind: "saving" });
    try {
      const names: string[] = [];
      for (const entry of entries) {
        const record = await saveSecret(`myia/push/${entry.field.key}`, entry.value);
        names.push(record.name);
      }
      setPushSave({
        kind: "saved",
        names,
        note: "已入钥匙链;运行时 env 缺失会自动用这些值(发送测试与真实推送同源)。",
      });
      setPushValues({});
      await runDoctor();
      await refreshSecretNames();
    } catch (error) {
      setPushSave({ kind: "error", error: asSidecarError(error) });
    }
  }, [push.channel, pushValues, refreshSecretNames, runDoctor]);

  return (
    /* R2 重排:区块节奏消费具名令牌 gap-block(24px)+ pb-block;
       屏级标题行已随无头化移除(PageHeader 渲染 null),「重新验证」
       动作迁入区标题行 actions 槽(见下方 header) */
    <div className="flex flex-col gap-block pb-block">
      {verifyError ? (
        <div className="px-6">
          <ErrorBox error={verifyError} onRetry={() => void runDoctor()} retrying={verifying} />
        </div>
      ) : null}

      {/* 左列 = 分区过滤框(导航上方,census #7)+ 分区导航;右列 = 分区内容
          (拆解表第 1/2 条:当前项高亮左竖条,每子区一屏)。
          R2 重排:双列间距消费 gap-block(24px);右列卡堆叠走 gap-grid(12px)。
          10-05 主人再裁(python-settings-unify):python-env 曾按 bac3ce4
          判例隐藏本列独占画布,现撤特殊化——导航对全部分区常驻 */}
      <div className="flex flex-col gap-card px-6 md:flex-row md:gap-block">
        <div className="flex shrink-0 flex-col gap-2 md:w-44">
          {/* 终审修整:过滤框转共享 Input 基件(带 data-slot=input,与全屏输入
              同享微填充+低可见描边+统一圆角;原裸 input 描边/填充自成一家,
              VL 指认「输入框描边粗细不一」) */}
          <Input
            type="search"
            value={sectionFilter}
            aria-label="过滤分区"
            placeholder="过滤分区"
            data-testid="settings-section-filter"
            onChange={(event) => setSectionFilter(event.target.value)}
          />
          <nav
            aria-label="设置分区"
            data-testid="settings-nav"
            className="flex flex-row gap-1 overflow-x-auto md:flex-col md:gap-0.5 md:overflow-visible"
          >
            {visibleSections.map(({ id, label, icon: Icon }) => {
              const active = id === sectionId;
              return (
                <button
                  key={id}
                  type="button"
                  data-testid={`settings-nav-${id}`}
                  aria-current={active ? "true" : undefined}
                  onClick={() => setSearchParams(id === DEFAULT_SECTION ? {} : { section: id })}
                  className={cn(
                    "relative flex h-8 shrink-0 items-center gap-2.5 rounded-md px-2.5 text-sm",
                    "transition-colors duration-(--duration-fast) ease-out-expo",
                    active
                      ? "bg-accent font-medium text-foreground"
                      : "text-muted-foreground hover:bg-accent/60 hover:text-foreground",
                  )}
                >
                  {active ? (
                    <span
                      aria-hidden
                      className="absolute left-0 top-1/2 h-4 w-0.5 -translate-y-1/2 rounded-full bg-primary"
                    />
                  ) : null}
                  <Icon className="size-4 shrink-0" />
                  {label}
                </button>
              );
            })}
          </nav>
          {visibleSections.length === 0 ? (
            <span data-testid="settings-section-filter-empty" className="px-2.5 text-2xs text-muted-foreground">
              无匹配分区(通用/推送/视觉/门槛件/装机组件/Python 环境/系统)
            </span>
          ) : null}
        </div>

        {/* 右列:区标题行(标题+描述左 / actions 右,Block.vue heading 范式),
            下堆叠多个 Card(每 Card 一个设置主题)。
            10-05 版面重排:内容列宽跟 Kestra 现行 Wrapper.vue 栅格——
            按断点比例流式居中(el-col md 18/lg 16/xl 14 offset 居中同构),
            不再 600px 固定窄列左钉;python-env 撤特殊化后同此列宽
            (10-05-pyenv-settings-unify,不再 max-w-4xl 独占) */}
        <section
          key={activeSection.id}
          aria-labelledby={`settings-section-title-${activeSection.id}`}
          data-testid={`settings-section-${activeSection.id}`}
          className="mx-auto flex min-w-0 w-full animate-fade-in flex-col gap-4 md:max-w-[75%] lg:max-w-[67%] xl:max-w-[58%]"
        >
          {/* 区标题行 = Kestra Block.vue heading 范式:content(标题+描述)左 /
              actions 右;「重新验证」自无头化的 PageHeader 迁入(否则不可见) */}
          <header className="flex items-start justify-between gap-4 pb-1">
            <div className="flex flex-col gap-1">
              <h2 id={`settings-section-title-${activeSection.id}`} className="text-lg font-semibold text-foreground">
                {activeSection.title}
              </h2>
              <p className="text-xs text-muted-foreground">{activeSection.description}</p>
            </div>
            <Button size="sm" variant="outline" className="shrink-0" onClick={() => void runDoctor()} disabled={verifying}>
              <RefreshCw className={verifying ? "size-3.5 animate-spin" : "size-3.5"} />
              重新验证
            </Button>
          </header>

          {activeSection.id === "system" ? (
            <>
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="size-4 text-muted-foreground" />
                  sidecar 核心进程
                </CardTitle>
                <CardDescription>实时连接状态(从侧栏底部迁移至此;侧栏不再展示)</CardDescription>
              </CardHeader>
              <CardContent>
                <SidecarStatusPanel />
              </CardContent>
            </Card>
            <UpdaterCard />

            {/* 危险区(拆解表第 6 条):单独 Destructive Card 置于区页底部;
                inline 二次确认沿用仓内惯例(同看图模型卡删除)。
                10-05 归位:79f7f7b 分区 6→4 收编时「高级」区被移除,此卡曾在
                守卫 id==="advanced" 的死分支里 UI 不可达;系统分区描述与终态
                合同本就写着「凭据管理」——钥匙链清单/删除的唯一入口在此落地 */}
            <Card
              data-testid="settings-danger-zone"
              className="border-destructive/40 bg-destructive/[0.04]"
            >
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-destructive">
                  <ShieldAlert className="size-4" />
                  危险区 · 钥匙链凭据(secret.list)
                </CardTitle>
                <CardDescription>
                  只有名字,值永不可读(secrets.py 契约);删除需二次确认,删除后引用该凭据的源将采集失败
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-col gap-2">
                {deleteError ? <ErrorBox error={deleteError} /> : null}
                {secretNames === null ? (
                  <span className="text-xs text-muted-foreground">无法获取(secret.list 失败或环境不可用)</span>
                ) : secretNames.length === 0 ? (
                  <span className="text-xs text-muted-foreground">暂无凭据</span>
                ) : (
                  <div className="flex flex-wrap items-center gap-1.5">
                    {secretNames.map((name) => (
                      <span key={name} className="flex items-center gap-0.5">
                        <Badge variant="outline" className="font-mono">
                          {name}
                        </Badge>
                        {deletingSecret === name ? (
                          <>
                            <Button
                              size="sm"
                              variant="destructive"
                              data-testid={`confirm-delete-${name}`}
                              onClick={() => void handleDeleteSecret(name)}
                            >
                              确认删除
                            </Button>
                            <Button size="sm" variant="ghost" onClick={() => setDeletingSecret(null)}>
                              取消
                            </Button>
                          </>
                        ) : (
                          <Button
                            variant="ghost"
                            size="icon"
                            className="size-6 hover:text-destructive"
                            aria-label={`删除凭据 ${name}`}
                            title={`删除 ${name}:删除后引用该凭据的源将采集失败`}
                            onClick={() => {
                              setDeleteError(null);
                              setDeletingSecret(name);
                            }}
                          >
                            <Trash2 className="size-3" />
                          </Button>
                        )}
                      </span>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>

            <p className="text-2xs text-muted-foreground">
              安全底线:任何凭据输入只经协议 secret.set 写入系统钥匙链(macOS Keychain /
              Windows DPAPI);配置文件出现明文凭据 = 启动即报错拒跑。model /
              enrich.enabled 经「通用 → 评分与反馈」写回品类 YAML(yaml.save,注释保真);
              池 URL 结构写回顺延(待拍板落点),push 通道声明去「配置编辑」。
            </p>
            </>
          ) : activeSection.id === "general" ? (
            <>
              {/* LLM */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <KeyRound className="size-4 text-muted-foreground" />
                    LLM 精评
                  </CardTitle>
                  <CardDescription>
                    base_url / key 属凭据类,只经 secret.set 入钥匙链;model 经下方「评分与反馈」写回品类 YAML(yaml.save)
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex flex-col gap-1">
                  <div className="divide-y divide-border/60">
                    <FieldInput
                      label="base_url"
                      aria-label="base_url"
                      placeholder="https://open.bigmodel.cn/api/paas/v4 或 env:MYIA_LLM_BASE_URL"
                      value={llm.baseUrl}
                      onChange={(event) => setLlm((prev) => ({ ...prev, baseUrl: event.target.value }))}
                      error={llmErrors.baseUrl}
                      hint="http(s) 地址 → 值入钥匙链(myia/llm/base_url);env:/keychain: 引用 → 直接写 YAML,不经界面"
                    />
                    <FieldInput
                      label="model"
                      aria-label="model"
                      placeholder="glm-4-flash(doctor 回显为现值)"
                      value={llm.model}
                      onChange={(event) => setLlm((prev) => ({ ...prev, model: event.target.value }))}
                      hint="非凭据:存于品类 YAML enrich.model;写回走下方「评分与反馈」分区(yaml.save,mtime 乐观锁)"
                    />
                    <FieldInput
                      label="LLM API Key"
                      aria-label="LLM API Key"
                      type="password"
                      autoComplete="new-password"
                      placeholder="输入后才写入;保存即清,永不回显"
                      value={llm.key}
                      onChange={(event) => setLlm((prev) => ({ ...prev, key: event.target.value }))}
                      hint="写入 myia/llm/api_key;YAML 侧引用 keychain:myia/llm/api_key"
                    />
                  </div>
                  <CardSaveBar
                    state={llmSave}
                    savingLabel="保存中…"
                    action={
                      <Button size="sm" onClick={() => void handleLlmSave()} disabled={llmSave?.kind === "saving"}>
                        <Save className="size-3.5" />
                        保存 LLM 凭据
                      </Button>
                    }
                  />
                </CardContent>
              </Card>

              {/* 评分与反馈(B3+C11:enrich.enabled 开关行自动保存 + model 写回 + budget 护栏) */}
              <EnrichFeedbackCard
                enrichSections={verify?.enrichSections ?? []}
                onSaved={(doctor) => setVerify(doctor)}
              />

              {/* 代理池 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Globe className="size-4 text-muted-foreground" />
                    代理池
                  </CardTitle>
                  <CardDescription>池凭据入钥匙链;池 URL 结构在全局 pools YAML(探测走 doctor --config)</CardDescription>
                </CardHeader>
                <CardContent className="flex flex-col gap-1">
                  <div className="divide-y divide-border/60">
                    <FieldInput
                      label="池名"
                      aria-label="代理池名"
                      placeholder="main"
                      value={proxy.pool}
                      onChange={(event) => setProxy((prev) => ({ ...prev, pool: event.target.value }))}
                      error={proxyErrors.pool}
                      labelHint="池名会拼进凭据保存的名字里(myia/proxy/池名)。同一个池名再存新值就是换密码;字母或数字开头,可以带点、连字符、下划线。"
                      hint="写入 myia/proxy/<池名>;YAML 侧以 keychain: 引用"
                    />
                    <FieldInput
                      label="凭据值"
                      aria-label="代理凭据值"
                      type="password"
                      autoComplete="new-password"
                      placeholder="写入 myia/proxy/<池名>;永不回显"
                      value={proxy.value}
                      onChange={(event) => setProxy((prev) => ({ ...prev, value: event.target.value }))}
                      error={proxyErrors.value}
                    />
                    <FieldInput
                      label="全局 pools YAML 路径"
                      aria-label="pools YAML 路径"
                      placeholder="留空=自动探测 <数据根>/pools.yaml"
                      value={probePath}
                      onChange={(event) => setProbePath(event.target.value)}
                      hint="留空自动探测数据根缺省文件;填写则用该路径探测"
                      action={
                        <Button size="sm" variant="secondary" onClick={() => void handleProbe()} disabled={verifying}>
                          探测
                        </Button>
                      }
                    />
                  </div>
                  <CardSaveBar
                    state={proxySave}
                    savingLabel="保存中…"
                    action={
                      <Button size="sm" variant="outline" onClick={() => void handleProxySave()} disabled={proxySave?.kind === "saving"}>
                        <Save className="size-3.5" />
                        保存代理凭据
                      </Button>
                    }
                  />
                </CardContent>
              </Card>

              {/* 诊断:保存后验证(doctor 回显;与代理池探测同区联动) */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Stethoscope className="size-4 text-muted-foreground" />
                    保存后验证(doctor 回显)
                  </CardTitle>
                  <CardDescription>
                    一切回显来自 doctor 应答:凭据存在性核验 + enrich 现值 + 池探测 + 结构化发现
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <DoctorVerifyPanel verify={verify} loading={verifying} proxyAutoMiss={probeAutoMiss} />
                </CardContent>
              </Card>
            </>
          ) : null}

          {/* 看图配置(10-03-vision-pipeline 拆屏后看图在桌面的唯一保留面:
              通道/引擎结构配置 + 云端 key 入钥匙链 + 模型管理;已有件整卡融入不重写) */}
          {activeSection.id === "vision" ? <VisionForm secretNames={secretNames} /> : null}

          {/* 门槛件(10-05-plugin-market-batch 批二第 11 步:付费 SaaS / 自有实例 /
              分析件知情启用,gates.get/save 读写 <MYIA_HOME>/gates.yaml) */}
          {activeSection.id === "gates" ? (
            <GatesForm secretNames={secretNames} onSecretsChanged={() => void refreshSecretNames()} />
          ) : null}

          {/* 装机组件(10-05-bundled-plugins-install:随包官方插件件发现/一键装,
              plugins.bundled.list/install;装卸门与 CLI myssia plugin install 同门) */}
          {activeSection.id === "installer-plugins" ? <BundledPluginsCard /> : null}

          {/* Python 运行环境(10-05-desktop-managed-py-env 第 4 步,D1/D2:
              开始配置/路径/双镜像覆盖/安装明细/同步依赖;IPC 契约见 pyenv-api.ts) */}
          {activeSection.id === "python-env" ? <PyenvCard /> : null}

          {activeSection.id === "push" ? (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Send className="size-4 text-muted-foreground" />
                  推送通道
                </CardTitle>
                <CardDescription>
                  按通道填一次凭据(入钥匙链 myia/push/*),运行时自动解析;「发送测试」与真实推送同源;
                  通道启停与阈值路由在品类 YAML push: 节
                </CardDescription>
              </CardHeader>
                <CardContent className="flex flex-col gap-1">
                  <div className="divide-y divide-border/60">
                    <SettingRow label="通道" description="feishu_card / telegram / webhook / bark / apprise;通道启停与阈值路由在品类 YAML push: 节">
                      <Select
                        value={push.channel}
                        onValueChange={(channel) =>
                          setPush((prev) => ({
                            ...prev,
                            channel: channel as PushChannel,
                            secretName: PUSH_SECRET_NAME_BY_CHANNEL[channel] ?? prev.secretName,
                          }))
                        }
                      >
                        <SelectTrigger aria-label="推送通道" className="w-64 min-w-0 flex-1 sm:flex-none">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {PUSH_CHANNELS.map((channel) => (
                            <SelectItem key={channel} value={channel}>
                              {PUSH_CHANNEL_LABELS[channel]}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </SettingRow>
                    {PUSH_FIELDS_BY_CHANNEL[push.channel].map((field) => (
                      <FieldInput
                        key={field.key}
                        label={field.label}
                        aria-label={`${push.channel} ${field.label}`}
                        type={field.password ? "password" : "text"}
                        autoComplete="new-password"
                        placeholder={`写入 myia/push/${field.key};永不回显`}
                        value={pushValues[field.key] ?? ""}
                        onChange={(event) =>
                          setPushValues((prev) => ({ ...prev, [field.key]: event.target.value }))
                        }
                        hint={field.hint}
                      />
                    ))}
                    {push.channel === "bark" ? (
                      // bark 端点非凭据(不进钥匙链),引导写在品类 YAML;10-05-push-bark
                      <p data-testid="bark-endpoint-hint" className="px-1 pb-1 text-2xs text-muted-foreground">
                        推送端点 bark_endpoint:留空 = 官方服务(api.day.app);自建 bark-server
                        填主机地址(如 http://192.168.1.10:8080)——写在品类 YAML push: 节
                      </p>
                    ) : null}
                    {push.channel === "apprise" ? (
                      // apprise 目标走凭据引用,值为目标串;10-05-push-apprise
                      <p data-testid="apprise-target-hint" className="px-1 pb-1 text-2xs text-muted-foreground">
                        目标走 env:/keychain: 引用,值为 Apprise 目标串(bark://…、pushover://…
                        可逗号分隔多个);需装可选依赖(pip install "myssia[apprise]" 或
                        uv sync --extra apprise),未装时发送会明确报错、不影响其他通道
                      </p>
                    ) : null}
                  </div>
                <CardSaveBar
                  state={pushSave}
                  savingLabel="保存中…"
                  action={
                    <div className="flex flex-wrap items-center gap-2">
                      <Button
                        size="sm"
                        onClick={() => void handlePresetSave()}
                        disabled={pushSave?.kind === "saving" || pushTesting}
                      >
                        <Save className="size-3.5" />
                        保存推送凭据
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() =>
                          void handlePushTest(`keychain:myia/push/${PUSH_TEST_TARGET_KEY[push.channel]}`)
                        }
                        disabled={pushTesting}
                        title="真发一条测试消息(push.test):目标=该通道预设凭据位,与真实推送同源解析"
                      >
                        <Send className={pushTesting ? "size-3.5 animate-pulse" : "size-3.5"} />
                        {pushTesting ? "发送中…" : "发送测试"}
                      </Button>
                      {pushTestOk === true ? <Badge variant="ok">通道连通</Badge> : null}
                      {pushTestOk === false ? <Badge variant="destructive">通道失败</Badge> : null}
                    </div>
                  }
                />
                {pushTestNote ? (
                  <p
                    role={pushTestOk === false ? "alert" : "status"}
                    data-testid="push-test-result"
                    className={pushTestOk === false ? "text-xs text-destructive" : "text-xs text-muted-foreground"}
                  >
                    {pushTestNote}
                  </p>
                ) : null}
                <details className="border-t border-border/60 pt-2 text-2xs text-muted-foreground">
                  <summary className="cursor-pointer select-none">
                    自定义凭据位(品类 YAML 手写 keychain: 引用用;日常接入用上方预设位即可)
                  </summary>
                  <div className="mt-2 flex flex-col gap-2">
                    <FieldInput
                      label="品类 scope"
                      aria-label="品类 scope"
                      placeholder="stocks"
                      value={push.scope}
                      onChange={(event) => setPush((prev) => ({ ...prev, scope: event.target.value }))}
                      error={pushErrors.scope}
                      hint="凭据引用键段:myia/<scope>/<凭据名>"
                    />
                    <FieldInput
                      label="凭据名段"
                      aria-label="推送凭据名"
                      placeholder={PUSH_SECRET_NAME_BY_CHANNEL[push.channel]}
                      value={push.secretName}
                      onChange={(event) => setPush((prev) => ({ ...prev, secretName: event.target.value }))}
                      error={pushErrors.secretName}
                      hint="通道目标凭据名(feishu 卡 chat_id / tg token / webhook url / bark device_key / apprise targets)"
                    />
                    <FieldInput
                      label="凭据值"
                      aria-label="推送凭据值"
                      type="password"
                      autoComplete="new-password"
                      placeholder="写入 myia/<scope>/<name>;永不回显"
                      value={push.value}
                      onChange={(event) => setPush((prev) => ({ ...prev, value: event.target.value }))}
                      error={pushErrors.value}
                    />
                    <div>
                      <Button size="sm" variant="outline" onClick={() => void handlePushSave()}>
                        <Save className="size-3.5" />
                        保存自定义凭据位
                      </Button>
                    </div>
                  </div>
                </details>
                <div className="flex flex-wrap items-center gap-1.5 border-t border-border/60 pt-2 text-2xs text-muted-foreground">
                  <span>推送通道声明(push: 节)与阈值路由在品类 YAML:</span>
                  {/* HashRouter 路由:普通锚点即可跳配置编辑屏,不引 Router context 依赖 */}
                  <a href="#/yaml-editor" className="underline underline-offset-2 hover:text-foreground">
                    去配置编辑改 push 声明
                  </a>
                </div>
              </CardContent>
            </Card>
          ) : null}
        </section>
      </div>
    </div>
  );
}

/** 设置-连接分区:sidecar 状态面板(主人 2026-10-04 指令从侧栏底部挪入) */
function SidecarStatusPanel() {
  const { status, info, error, reprobe } = useSidecarStatus();
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const stateMap: Record<string, { label: string; cls: string; dot: string }> = {
    online: { label: "已连接", cls: "text-ok", dot: "bg-ok" },
    connecting: { label: "连接中…", cls: "text-muted-foreground", dot: "bg-muted-foreground" },
    respawning: { label: "自动重拉中", cls: "text-warning", dot: "bg-warning" },
    dead: { label: "已退出", cls: "text-dead", dot: "bg-dead" },
    offline: { label: "未连接", cls: "text-muted-foreground", dot: "bg-muted-foreground" },
  };
  const st = stateMap[status] ?? stateMap.offline;

  return (
    <div data-testid="sidecar-status-panel" className="flex flex-col gap-3">
      <div className="flex items-center gap-3">
        <span className={`relative flex size-3 shrink-0`}>
          <span className={`absolute inline-flex h-full w-full animate-ping rounded-full ${st.dot} opacity-60`} />
          <span className={`relative inline-flex size-3 rounded-full ${st.dot}`} />
        </span>
        <span className={`text-sm font-medium ${st.cls}`} data-testid="sidecar-status-label">{st.label}</span>
        <span className="text-2xs text-muted-foreground">检测于 {now.toLocaleTimeString("zh-CN")}</span>
      </div>
      {status === "online" && info ? (
        <div className="grid grid-cols-2 gap-2 text-2xs text-muted-foreground md:grid-cols-4">
          <div><span className="text-foreground font-medium">核心版本</span><br />v{info.version}</div>
          <div><span className="text-foreground font-medium">协议版本</span><br />v{info.protocol}</div>
          <div><span className="text-foreground font-medium">应用版本</span><br />{info.app_version ? `v${info.app_version}` : "—"}</div>
          <div><span className="text-foreground font-medium">名称</span><br />{info.name}</div>
        </div>
      ) : null}
      {error ? (
        <div className="text-2xs text-dead">
          错误:[{error.code}] {error.message}
        </div>
      ) : null}
      <div className="flex gap-2">
        <Button variant="outline" size="sm" onClick={() => reprobe()} data-testid="sidecar-status-reprobe">
          <RefreshCw className="mr-1 size-3" />
          重新检测
        </Button>
      </div>
    </div>
  );
}
