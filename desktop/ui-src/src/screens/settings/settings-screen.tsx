import { useSidecarStatus } from "@/hooks/use-sidecar-status";
import {
  Activity,
  ShieldAlert,
  Eye,
  KeyRound,
  Lightbulb,
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

import { PageHeader } from "@/components/layout/page-header";
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
import type { DoctorParams, SidecarRequestError } from "@/lib/api";
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
import { DoctorVerifyPanel } from "./doctor-verify";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
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
// {Wrapper,block/Block,block/SettingRow}.vue,借结构改语义):内容列
// 600px 居中单列(Wrapper 范式)、行 = SettingRow 横排(label+hint 左/
// 控件右 w-64)、卡内行间 divide-y 细线。不抄:单页无分区导航(我们的
// 五分区 ?section= 深链是既有功能面,R5 零改动保留)。
// ---------------------------------------------------------------------------

/** 通道 → 规范凭据名缺省(target 语义:feishu 卡的 chat_id / tg 的 bot token / webhook 地址) */
const PUSH_SECRET_NAME_BY_CHANNEL: Record<string, string> = {
  feishu_card: "chat_id",
  telegram: "token",
  webhook: "url",
};
type PushChannel = keyof typeof PUSH_SECRET_NAME_BY_CHANNEL;
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
                    label={pluginFile.split("/").pop() ?? pluginFile}
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

  const handleProbe = useCallback(async () => {
    await runDoctor(probePath.trim() ? { config: probePath.trim() } : undefined);
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

  const handlePushTest = useCallback(async () => {
    setPushTesting(true);
    setPushTestNote(null);
    setPushTestOk(null);
    // target 引用:表单 scope/凭据名齐全才组;否则让通道走默认 env 链(如实测)
    const scope = push.scope.trim();
    const name = push.secretName.trim() || PUSH_SECRET_NAME_BY_CHANNEL[push.channel] || "";
    const target = scope && name ? `keychain:myia/${scope}/${name}` : undefined;
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

  return (
    /* R2 重排:区块节奏消费具名令牌 gap-block(24px)+ pb-block */
    <div className="flex flex-col gap-block pb-block">
      <PageHeader
        title="设置"
        description="通用 / 视觉 / 推送 / 更新 / 高级 五分区 —— 凭据只入系统钥匙链,doctor 验证回显,软件更新检查"
        actions={
          <Button size="sm" variant="outline" onClick={() => void runDoctor()} disabled={verifying}>
            <RefreshCw className={verifying ? "size-3.5 animate-spin" : "size-3.5"} />
            重新验证
          </Button>
        }
      />

      {verifyError ? (
        <div className="px-6">
          <ErrorBox error={verifyError} onRetry={() => void runDoctor()} retrying={verifying} />
        </div>
      ) : null}

      {/* 左列 = 分区过滤框(导航上方,census #7)+ 分区导航;右列 = 分区内容
          (拆解表第 1/2 条:当前项高亮左竖条,每子区一屏)。
          R2 重排:双列间距消费 gap-block(24px);右列卡堆叠走 gap-grid(12px) */}
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
              无匹配分区(通用/视觉/推送/更新/高级)
            </span>
          ) : null}
        </div>

        {/* 右列:区标题+描述,下堆叠多个 Card(每 Card 一个设置主题)。
            10-04-ui-kestra-anchor:内容列宽对齐 Kestra settings Wrapper
            (min(600px, 100%-48px) 居中单列);行 = SettingRow 横排范式 */}
        <section
          key={activeSection.id}
          aria-labelledby={`settings-section-title-${activeSection.id}`}
          data-testid={`settings-section-${activeSection.id}`}
          className="flex w-full min-w-0 max-w-[600px] animate-fade-in flex-col gap-4"
        >
          <header className="flex flex-col gap-1 pb-1">
            <h2 id={`settings-section-title-${activeSection.id}`} className="text-lg font-semibold text-foreground">
              {activeSection.title}
            </h2>
            <p className="text-xs text-muted-foreground">{activeSection.description}</p>
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
                      placeholder="config/pools.yaml(--config;缺省=只看现状)"
                      value={probePath}
                      onChange={(event) => setProbePath(event.target.value)}
                      hint="doctor --config 探测全局池结构"
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
                  <DoctorVerifyPanel verify={verify} loading={verifying} />
                </CardContent>
              </Card>
            </>
          ) : null}

          {/* 看图配置(10-03-vision-pipeline 拆屏后看图在桌面的唯一保留面:
              通道/引擎结构配置 + 云端 key 入钥匙链 + 模型管理;已有件整卡融入不重写) */}
          {activeSection.id === "vision" ? <VisionForm secretNames={secretNames} /> : null}

          {activeSection.id === "push" ? (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Send className="size-4 text-muted-foreground" />
                  推送通道
                </CardTitle>
                <CardDescription>
                  通道凭据(chat_id / bot token / webhook)入钥匙链;「发送测试」真发一条验证通道连通(push.test);
                  通道启停与阈值路由在品类 YAML push: 节
                </CardDescription>
              </CardHeader>
                <CardContent className="flex flex-col gap-1">
                  <div className="divide-y divide-border/60">
                    <SettingRow label="通道" description="feishu_card / telegram / webhook;通道启停与阈值路由在品类 YAML push: 节">
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
                              {channel}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </SettingRow>
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
                      hint="通道目标凭据名(feishu 卡 chat_id / tg token / webhook url)"
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
                  </div>
                <CardSaveBar
                  state={pushSave}
                  savingLabel="保存中…"
                  action={
                    <div className="flex flex-wrap items-center gap-2">
                      <Button
                        size="sm"
                        onClick={() => void handlePushSave()}
                        disabled={pushSave?.kind === "saving" || pushTesting}
                      >
                        <Save className="size-3.5" />
                        保存推送凭据
                      </Button>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => void handlePushTest()}
                        disabled={pushTesting}
                        title="真发一条测试消息(push.test):验证所选通道连通性"
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

          {/* 软件更新(官方签名更新通道,updater-card.tsx;已有件融入不重写) */}
          {activeSection.id === "update" ? <UpdaterCard /> : null}

          {activeSection.id === "advanced" ? (
            <>
              {/* 危险区(拆解表第 6 条):单独 Destructive Card 置于区页底部;
                  inline 二次确认沿用仓内惯例(同看图模型卡删除) */}
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
