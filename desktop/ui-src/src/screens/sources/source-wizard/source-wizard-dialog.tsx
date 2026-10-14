import { Check, ExternalLink, Loader2, Plus, Save, Trash2, X } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import type { ReactNode } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import { TestResultDialog } from "../test-result-dialog";
import type { TestOutcomeView } from "../api";
import {
  DEFAULT_USER_AGENT,
  SCHEDULE_CUSTOM,
  SCHEDULE_PRESETS,
  buildCategoryYaml,
  resolveScheduleCron,
} from "./build-category-yaml";
import type { WizardPagination } from "./build-category-yaml";
import { explainSaveError, useSourceWizard } from "./use-source-wizard";

/**
 * 建源向导对话框(PRD:.trellis/tasks/10-14-visual-source-builder,R1/R2)。
 *
 * 形态:源管理屏内多步向导(不新路由/不新侧栏行/零新 sidecar 协议方法)。
 * 弹窗范式沿本屏 YamlEditorDialog:fixed 遮罩 + 居中面板 role=dialog
 * aria-modal,ESC / 遮罩 / 关闭钮三径同关(有输入或已保存先 confirm);
 * 头部次入口「直接编辑 YAML」深链保留。步骤条五步置顶,底部「上一步/下一步」。
 * 状态机 = use-source-wizard(五步/表单态/保存 mtime 链/试采 job);
 * 试采详情二次打开既有 TestResultDialog(零改动复用)。
 *
 * 文案纪律(R5):人话——「抓取频率」不是 schedule、「翻页」不是 pagination;
 * 「试一试(抓 1 次看看)」首现后续「试一试」;错误保留后端 code + 一句人话。
 */

const STEP_LABELS = ["基本信息", "源信息", "提取规则", "预览保存", "试一试"] as const;

/** 翻页下拉的三值(与 WizardPagination.mode 一一对应) */
const PAGINATION_OPTIONS: ReadonlyArray<{ value: WizardPagination["mode"]; label: string }> = [
  { value: "none", label: "不翻页(只抓第一页)" },
  { value: "template", label: "网址带页码(地址里有 {page})" },
  { value: "selector", label: "点「下一页」链接" },
];

interface SourceWizardDialogProps {
  /** 关闭向导(守卫在组件内:有输入或已保存先 confirm;确认放弃才回调) */
  onClose: () => void;
}

export function SourceWizardDialog({ onClose }: SourceWizardDialogProps) {
  const {
    step,
    form,
    confirmClose,
    stepErrors,
    goToStep,
    patchForm,
    patchField,
    addField,
    removeField,
    idExistsWarning,
    saved,
    save,
    saveAndAdvance,
    test,
    launchTest,
    backToEdit,
  } = useSourceWizard();

  /** 「查看详情」二次弹窗(既有 TestResultDialog,零改动复用) */
  const [detailOutcome, setDetailOutcome] = useState<TestOutcomeView | null>(null);
  const detailOpenRef = useRef(false);
  detailOpenRef.current = detailOutcome !== null;
  const panelRef = useRef<HTMLDivElement>(null);
  /** 当前步错误是否上屏(点「下一步」被拦后才显示,避免空表单开场即满屏红字) */
  const [showStepErrors, setShowStepErrors] = useState(false);

  const attemptClose = useCallback(() => {
    if (!confirmClose()) return;
    onClose();
  }, [confirmClose, onClose]);

  // 键盘:ESC 关闭(已消费的事件不关;详情弹窗打开时让给它,防双关丢结果)
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.defaultPrevented) return;
      if (event.key === "Escape" && !detailOpenRef.current) attemptClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [attemptClose]);

  // 模态基础焦点:面板挂载即聚焦(ESC 无需先点进表单;轮廓不抢视觉)
  useEffect(() => {
    panelRef.current?.focus();
  }, []);

  // 换步即收起上一步的拦截错误(新步从干净态开始)
  useEffect(() => {
    setShowStepErrors(false);
  }, [step]);

  const currentErrors = stepErrors(step);

  /** 下一步:本步有门错误 = 原地展示并拦下(AC2/AC3);通过才前进 */
  const handleNext = useCallback(() => {
    if (step >= 4) return;
    if (stepErrors(step).length > 0) {
      setShowStepErrors(true);
      return;
    }
    goToStep(step + 1);
  }, [goToStep, step, stepErrors]);

  /** 翻页模式切换:none 不带参数;两种翻页 max_pages 缺省 5(修正③) */
  const patchPaginationMode = useCallback(
    (mode: WizardPagination["mode"]) => {
      patchForm({
        pagination:
          mode === "none"
            ? { mode: "none" }
            : mode === "template"
              ? { mode: "template", maxPages: 5 }
              : { mode: "selector", selector: "", maxPages: 5 },
      });
    },
    [patchForm],
  );

  /** max_pages 数字输入(Number 解析;NaN 归 0 让校验拦,不静默吞) */
  const patchMaxPages = useCallback(
    (raw: string) => {
      const parsed = Math.trunc(Number(raw));
      if (form.pagination.mode === "template") {
        patchForm({ pagination: { mode: "template", maxPages: Number.isFinite(parsed) ? parsed : 0 } });
      } else if (form.pagination.mode === "selector") {
        patchForm({
          pagination: {
            mode: "selector",
            selector: form.pagination.selector,
            maxPages: Number.isFinite(parsed) ? parsed : 0,
          },
        });
      }
    },
    [form.pagination, patchForm],
  );

  const paginationLabel =
    form.pagination.mode === "none"
      ? "不翻页"
      : form.pagination.mode === "template"
        ? `网址带页码(最多 ${form.pagination.maxPages} 页)`
        : `「下一页」链接(最多 ${form.pagination.maxPages} 页)`;

  const outcome = test.status === "done" ? test.outcome : null;
  const doneOutcome = outcome !== null && outcome.ok ? outcome : null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6 animate-overlay-in"
      onClick={attemptClose}
      data-testid="source-wizard-overlay"
    >
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-label="新建品类向导"
        tabIndex={-1}
        data-testid="source-wizard-dialog"
        className="flex max-h-[85vh] w-[min(880px,92vw)] flex-col gap-3 rounded-lg border border-border bg-card p-4 shadow-drawer animate-dialog-in outline-none"
        onClick={(event) => event.stopPropagation()}
      >
        {/* 标题区:标题 + 次入口深链(R1.3)+ 关闭 */}
        <div className="flex shrink-0 items-center justify-between gap-2">
          <div className="flex min-w-0 flex-col gap-0.5">
            <span className="truncate text-sm font-semibold text-foreground">新建品类(向导)</span>
            <span className="text-2xs text-muted-foreground">
              填一填、试一试,落成一份品类 YAML;关键词过滤、分类、推送等进「YAML配置」补全
            </span>
          </div>
          <div className="flex shrink-0 items-center gap-2">
            <a
              href="#/yaml-editor"
              title="不走向导,直接到「YAML配置」手写品类 YAML"
              className="inline-flex items-center gap-1 text-2xs font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
            >
              <ExternalLink className="size-3" />
              直接编辑 YAML
            </a>
            <Button size="sm" variant="ghost" aria-label="关闭对话框" onClick={attemptClose}>
              <X className="size-4" />
            </Button>
          </div>
        </div>

        {/* 步骤条(五步名置顶;当前步 aria-current) */}
        <ol
          aria-label="向导步骤"
          className="flex shrink-0 items-center gap-1 overflow-x-auto border-y border-border px-1 py-2"
        >
          {STEP_LABELS.map((label, index) => {
            const number = index + 1;
            const isDone = number < step;
            const isCurrent = number === step;
            return (
              <li
                key={label}
                aria-current={isCurrent ? "step" : undefined}
                data-testid={`wizard-step-${number}`}
                className={`flex shrink-0 items-center gap-1.5 rounded-sm px-2 py-1 ${
                  isCurrent
                    ? "bg-primary/10 text-foreground"
                    : isDone
                      ? "text-muted-foreground"
                      : "text-muted-foreground/60"
                }`}
              >
                <span
                  aria-hidden
                  className={`flex size-5 items-center justify-center rounded-full border text-2xs ${
                    isCurrent ? "border-primary text-foreground" : "border-border"
                  }`}
                >
                  {isDone ? <Check className="size-3" /> : number}
                </span>
                <span className="text-xs">{label}</span>
              </li>
            );
          })}
        </ol>

        {/* 正文:分步表单滚动区 */}
        <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto px-1 py-1">
          {/* 拦截错误区(点「下一步」被拦后上屏;换步即收起) */}
          {showStepErrors && currentErrors.length > 0 ? (
            <ul
              role="alert"
              data-testid="wizard-step-errors"
              className="flex flex-col gap-1 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2.5"
            >
              {currentErrors.map((line) => (
                <li key={line} className="text-xs text-destructive">
                  {line}
                </li>
              ))}
            </ul>
          ) : null}

          {step === 1 ? (
            <StepBlock title="基本信息" description="这一份 YAML 叫什么、多久自动抓一次">
              <FormField label="品类 id(也是文件名)" htmlFor="wizard-id" help="小写字母/数字/-/_,1-64 字符;保存后文件名就是它">
                <Input
                  id="wizard-id"
                  value={form.categoryId}
                  disabled={saved !== null}
                  placeholder="如 gpu-prices"
                  onChange={(event) => patchForm({ categoryId: event.target.value })}
                />
              </FormField>
              {saved !== null ? (
                <p className="text-2xs text-muted-foreground">已保存,文件名不再改;要换 id 请关闭向导重来。</p>
              ) : null}
              <FormField label="品类名" htmlFor="wizard-name" help="中文随意,列表里显示用">
                <Input
                  id="wizard-name"
                  value={form.categoryName}
                  placeholder="如 显卡行情"
                  onChange={(event) => patchForm({ categoryName: event.target.value })}
                />
              </FormField>
              <FormField label="抓取频率" htmlFor="wizard-schedule" help="多久自动抓一次;预设不够用可选自定义">
                <select
                  id="wizard-schedule"
                  value={form.schedulePreset}
                  onChange={(event) => patchForm({ schedulePreset: event.target.value })}
                  className="h-8 w-full min-w-0 rounded-md border border-input bg-background px-2 text-sm text-foreground"
                >
                  <option value="">先选一个…</option>
                  {SCHEDULE_PRESETS.map((preset) => (
                    <option key={preset.value} value={preset.value}>
                      {preset.label}
                    </option>
                  ))}
                  <option value={SCHEDULE_CUSTOM}>自定义…</option>
                </select>
              </FormField>
              {form.schedulePreset === SCHEDULE_CUSTOM ? (
                <FormField
                  label="自定义频率(5 段 cron)"
                  htmlFor="wizard-schedule-custom"
                  help="5 段从左到右是:分 时 日 月 周(空格隔开),如 0 9 * * * = 每天 9 点"
                >
                  <Input
                    id="wizard-schedule-custom"
                    value={form.scheduleCustom}
                    placeholder="0 9 * * *"
                    onChange={(event) => patchForm({ scheduleCustom: event.target.value })}
                  />
                </FormField>
              ) : null}
              {idExistsWarning !== null ? (
                <p role="alert" data-testid="wizard-id-exists" className="text-xs text-warning">
                  {idExistsWarning}
                </p>
              ) : null}
            </StepBlock>
          ) : null}

          {step === 2 ? (
            <StepBlock title="源信息" description="去哪个网页、抓哪些页">
              <FormField label="源名" htmlFor="wizard-source-name" help="一个品类可以有几个源;第一个叫 main 就行">
                <Input
                  id="wizard-source-name"
                  value={form.sourceName}
                  placeholder="main"
                  onChange={(event) => patchForm({ sourceName: event.target.value })}
                />
              </FormField>
              <FormField label="页面地址" htmlFor="wizard-url" help="要 http:// 或 https:// 开头的完整网址">
                <Input
                  id="wizard-url"
                  value={form.url}
                  placeholder="https://example.com/list"
                  onChange={(event) => patchForm({ url: event.target.value })}
                />
              </FormField>
              {form.pagination.mode === "template" && form.url !== "" && !form.url.includes("{page}") ? (
                <p role="alert" data-testid="wizard-page-placeholder" className="text-xs text-destructive">
                  选了「网址带页码」翻页,页面地址里要有 {"{page}"} 占位(抓的时候会依次换成页码)
                </p>
              ) : null}
              <FormField label="抓取方式" help={undefined}>
                <p className="rounded-md border border-border/60 bg-muted/30 px-2.5 py-2 text-xs text-muted-foreground">
                  读取网页源代码 —— 适合服务器渲染的普通网页列表(浏览器里右键 → 查看网页源代码,能看到内容的页面)。
                  要登录、要滚动加载或 JSON 接口的源,完成后去「YAML配置」手写。
                </p>
              </FormField>
              <FormField label="翻页" htmlFor="wizard-pagination" help="列表不止一页时才需要">
                <select
                  id="wizard-pagination"
                  value={form.pagination.mode}
                  onChange={(event) => patchPaginationMode(event.target.value as WizardPagination["mode"])}
                  className="h-8 w-full min-w-0 rounded-md border border-input bg-background px-2 text-sm text-foreground"
                >
                  {PAGINATION_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </FormField>
              {form.pagination.mode === "selector" ? (
                <FormField
                  label="「下一页」按钮的 CSS 选择器"
                  htmlFor="wizard-next-selector"
                  help="和第 3 步一样:右键该元素 → 检查 → Copy selector"
                >
                  <Input
                    id="wizard-next-selector"
                    value={form.pagination.mode === "selector" ? form.pagination.selector : ""}
                    placeholder="如 a.next"
                    onChange={(event) =>
                      form.pagination.mode === "selector" &&
                      patchForm({
                        pagination: { ...form.pagination, selector: event.target.value },
                      })
                    }
                  />
                </FormField>
              ) : null}
              {form.pagination.mode !== "none" ? (
                <FormField label="最多翻几页" htmlFor="wizard-max-pages" help="1-10000;翻到头会提前停">
                  <Input
                    id="wizard-max-pages"
                    type="number"
                    min={1}
                    max={10000}
                    value={String(form.pagination.maxPages)}
                    onChange={(event) => patchMaxPages(event.target.value)}
                    className="w-32"
                  />
                </FormField>
              ) : null}
              <FormField label="浏览器标识(可选)" htmlFor="wizard-ua" help="已预填常见浏览器标识;清空 = 不带">
                <Input
                  id="wizard-ua"
                  value={form.userAgent}
                  placeholder={DEFAULT_USER_AGENT}
                  onChange={(event) => patchForm({ userAgent: event.target.value })}
                />
              </FormField>
            </StepBlock>
          ) : null}

          {step === 3 ? (
            <StepBlock title="提取规则" description="先框住页面上重复的整条(比如一行商品),再告诉每条里哪个部分是标题、哪个是链接">
              <FormField
                label="列表整条的选择器(item)"
                htmlFor="wizard-item"
                help="浏览器里右键该元素 → 检查 → 右键高亮节点 → Copy → Copy selector,粘过来"
              >
                <Input
                  id="wizard-item"
                  value={form.itemSelector}
                  placeholder="如 div.list-item"
                  onChange={(event) => patchForm({ itemSelector: event.target.value })}
                />
              </FormField>
              <div className="flex flex-col gap-2">
                <span className="text-xs font-medium text-foreground">字段(每条里取什么)</span>
                {form.fields.map((row, index) => (
                  <div key={index} data-testid="wizard-field-row" className="flex flex-wrap items-center gap-2">
                    <Input
                      aria-label={`字段 ${index + 1} 名字`}
                      value={row.name}
                      placeholder="字段名,如 price"
                      className="w-36"
                      onChange={(event) => patchField(index, { name: event.target.value })}
                    />
                    <Input
                      aria-label={`字段 ${index + 1} 选择器`}
                      value={row.selector}
                      placeholder="CSS 选择器,如 span.price"
                      className="min-w-48 flex-1"
                      onChange={(event) => patchField(index, { selector: event.target.value })}
                    />
                    {row.name.trim() === "url" ? (
                      <label className="flex shrink-0 items-center gap-1.5 text-2xs text-muted-foreground">
                        <input
                          type="checkbox"
                          aria-label="取链接地址(@href)"
                          checked={row.useHref}
                          onChange={(event) => patchField(index, { useHref: event.target.checked })}
                        />
                        取链接地址
                      </label>
                    ) : null}
                    <Button
                      size="sm"
                      variant="ghost"
                      aria-label={`删除字段 ${index + 1}`}
                      title="删掉这行字段"
                      onClick={() => removeField(index)}
                    >
                      <Trash2 className="size-3.5" />
                    </Button>
                  </div>
                ))}
                <div>
                  <Button size="sm" variant="outline" onClick={addField}>
                    <Plus className="size-3.5" />
                    添加字段
                  </Button>
                </div>
                <p className="text-2xs text-muted-foreground">
                  预置的 url 字段是必须的(每条内容的链接);url 行勾「取链接地址」= 抓链接地址而不是文字。
                </p>
              </div>
            </StepBlock>
          ) : null}

          {step === 4 ? (
            <StepBlock title="预览与保存" description="这就是将落盘的 YAML;保存前会先校验一遍">
              <pre
                data-testid="wizard-yaml-preview"
                className="max-h-72 overflow-auto whitespace-pre rounded-md border border-border bg-muted/30 p-3 font-mono text-xs text-foreground"
              >
                {buildCategoryYaml(form)}
              </pre>
              <div data-testid="wizard-summary" className="flex flex-col gap-1 rounded-md border border-border/60 px-3 py-2.5">
                <SummaryLine label="品类" value={`${form.categoryName.trim() || "(未填)"}(${form.categoryId.trim() || "(未填)"})`} />
                <SummaryLine label="抓取频率" value={resolveScheduleCron(form) || "(未选)"} />
                <SummaryLine label="页面地址" value={form.url.trim() || "(未填)"} />
                <SummaryLine label="翻页" value={paginationLabel} />
                <SummaryLine
                  label="字段"
                  value={`${form.fields.filter((row) => row.name.trim() !== "").length} 个:${form.fields
                    .filter((row) => row.name.trim() !== "")
                    .map((row) => row.name.trim())
                    .join("、") || "(无)"}`}
                />
              </div>
              {save.findings.length > 0 ? (
                <ul
                  role="alert"
                  data-testid="wizard-validate-findings"
                  className="flex flex-col gap-1 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2.5"
                >
                  <li className="text-xs font-medium text-destructive">校验没过,还没保存:</li>
                  {save.findings.map((finding) => (
                    <li key={`${finding.path}:${finding.code}`} className="break-all text-xs text-destructive">
                      {finding.path}:{finding.message}(code={finding.code})
                    </li>
                  ))}
                </ul>
              ) : null}
              {save.error !== null ? (
                <div
                  role="alert"
                  data-testid="wizard-save-error"
                  className="flex flex-col gap-1 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2.5"
                >
                  <p className="text-xs text-destructive">{explainSaveError(save.error)}</p>
                  <p className="break-all font-mono text-2xs text-destructive/80">
                    code={save.error.code}:{save.error.message}
                  </p>
                </div>
              ) : null}
              {save.warnings.length > 0 ? (
                <ul data-testid="wizard-save-warnings" className="flex flex-col gap-1 px-1">
                  {save.warnings.map((finding) => (
                    <li key={`${finding.path}:${finding.code}`} className="break-all text-2xs text-warning">
                      保存时的提醒:{finding.path}:{finding.message}
                    </li>
                  ))}
                </ul>
              ) : null}
            </StepBlock>
          ) : null}

          {step === 5 ? (
            <StepBlock title="试一试(抓 1 次看看)" description="保存成功了;现在真抓一次,看看能取回什么">
              {test.status === "launching" || test.status === "running" ? (
                <p role="status" data-testid="wizard-test-running" className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Loader2 className="size-4 animate-spin" />
                  试一试进行中;实时输出见「采集日志」
                </p>
              ) : null}
              {test.status === "launch_error" ? (
                <div
                  role="alert"
                  data-testid="wizard-test-launch-error"
                  className="flex flex-col gap-2 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2.5"
                >
                  <p className="break-all text-xs text-destructive">
                    发起失败:{test.error.message}(code={test.error.code})
                  </p>
                  <div>
                    <Button size="sm" variant="outline" onClick={() => void launchTest()}>
                      重试
                    </Button>
                  </div>
                </div>
              ) : null}
              {outcome !== null ? (
                <WizardTestSummary outcome={outcome} onOpenDetail={() => setDetailOutcome(outcome)} />
              ) : null}
              {doneOutcome !== null && saved !== null ? (
                <div
                  data-testid="wizard-done"
                  className="flex flex-col gap-2 rounded-md border border-ok/30 bg-ok/10 px-3 py-2.5"
                >
                  <p className="text-sm text-ok">配置建好了,已开始按频率自动抓取。</p>
                  <p className="break-all font-mono text-2xs text-muted-foreground" title={saved.file}>
                    {saved.file}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    这份 YAML 只配了采集;关键词过滤、分类、推送等下游配置,去「YAML配置」继续补。
                  </p>
                  <div className="flex flex-wrap items-center gap-2">
                    <a
                      href={`#/yaml-editor?file=${encodeURIComponent(saved.file)}`}
                      className="inline-flex items-center gap-1.5 text-sm font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
                    >
                      <ExternalLink className="size-3.5" />
                      去补全推送等配置
                    </a>
                  </div>
                </div>
              ) : null}
            </StepBlock>
          ) : null}
        </div>

        {/* 底部导航:上一步/下一步(1-3)/保存(4)/返回修改·完成(5) */}
        <div className="flex shrink-0 items-center gap-2 border-t border-border pt-3">
          {step > 1 && step < 5 ? (
            <Button size="sm" variant="outline" onClick={() => goToStep(step - 1)}>
              上一步
            </Button>
          ) : null}
          {step < 4 ? (
            <Button size="sm" onClick={handleNext}>
              下一步
            </Button>
          ) : null}
          {step === 4 ? (
            <Button size="sm" disabled={save.running} onClick={() => void saveAndAdvance()}>
              <Save className="size-3.5" />
              {save.running ? "保存中…" : "保存"}
            </Button>
          ) : null}
          {step === 5 && doneOutcome === null ? (
            /* 在途/发起失败/试采失败都可回改(在途返回后若旧 job 未收,
               下次自动试采撞 test_busy 会如实展示可重试,不静默) */
            <Button size="sm" variant="outline" onClick={backToEdit}>
              返回修改
            </Button>
          ) : null}
          <span className="flex-1" />
          {step === 5 && doneOutcome !== null ? (
            <Button size="sm" onClick={onClose}>
              完成
            </Button>
          ) : (
            <Button size="sm" variant="outline" onClick={attemptClose}>
              关闭
            </Button>
          )}
        </div>
      </div>

      {/* 「查看详情」二次弹窗:既有 TestResultDialog,零改动复用 */}
      {detailOutcome !== null ? (
        <TestResultDialog outcome={detailOutcome} onClose={() => setDetailOutcome(null)} />
      ) : null}
    </div>
  );
}

/** 试采内嵌摘要(AC6):成功与否/命中引擎/条数 + 前 5 条样例的字段值表 + 查看详情 */
function WizardTestSummary({
  outcome,
  onOpenDetail,
}: {
  outcome: TestOutcomeView;
  onOpenDetail: () => void;
}) {
  const engineHit = outcome.engine ?? outcome.engineConfigured ?? "—";
  const samples = (outcome.items ?? []).slice(0, 5);
  const columns: string[] = [];
  for (const item of samples) {
    for (const key of Object.keys(item.fields)) {
      if (!columns.includes(key)) columns.push(key);
    }
  }
  const failureLines: string[] = [];
  if (outcome.kind === "event_error") failureLines.push(`试一试失败(${outcome.error ?? "error"})`);
  else if (outcome.error !== undefined) failureLines.push(`试一试失败:${outcome.error}`);
  for (const entry of outcome.kind === "event_error" ? outcome.errors ?? [] : []) {
    failureLines.push(`${entry.path ? `${entry.path}:` : ""}${entry.message}`);
  }

  return (
    <div data-testid="wizard-test-summary" className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center gap-2">
        <Badge variant={outcome.ok ? "ok" : "destructive"}>{outcome.ok ? "抓到了" : "没抓到"}</Badge>
        <span className="text-sm text-foreground">
          实际使用引擎 <span className="font-mono text-xs">{engineHit}</span> · 共{" "}
          <span className="font-semibold">{outcome.itemCount ?? 0}</span> 条
        </span>
        <span className="flex-1" />
        <Button size="sm" variant="outline" onClick={onOpenDetail}>
          查看详情
        </Button>
      </div>
      {samples.length > 0 ? (
        <div className="overflow-x-auto rounded-md border border-border/60">
          <table className="w-full text-left text-2xs">
            <thead className="bg-muted/40 text-muted-foreground">
              <tr>
                {columns.map((column) => (
                  <th key={column} scope="col" className="whitespace-nowrap px-2.5 py-1.5 font-medium">
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="font-mono">
              {samples.map((item, index) => (
                <tr key={index} className="border-t border-border/60">
                  {columns.map((column) => (
                    <td key={column} className="max-w-64 truncate px-2.5 py-1.5" title={item.fields[column] ?? ""}>
                      {item.fields[column] ?? "—"}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-xs text-muted-foreground">一条也没抓到;多半是选择器不对,返回修改再试。</p>
      )}
      {failureLines.length > 0 ? (
        <ul role="alert" className="flex flex-col gap-1 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2.5">
          {failureLines.map((line, index) => (
            <li key={index} className="break-all text-xs text-destructive">
              {line}
            </li>
          ))}
        </ul>
      ) : null}
      {(outcome.itemsTruncated ?? false) && samples.length > 0 ? (
        <p className="text-2xs text-muted-foreground">上面只列前 {samples.length} 条,全部明细点「查看详情」。</p>
      ) : null}
    </div>
  );
}

/** 分步块:标题 + 一句人话说明 + 表单列 */
function StepBlock({ title, description, children }: { title: string; description: string; children: ReactNode }) {
  return (
    <section className="flex min-h-0 flex-col gap-4" aria-label={title}>
      <div className="flex flex-col gap-0.5">
        <h2 className="text-sm font-semibold text-foreground">{title}</h2>
        <p className="text-xs text-muted-foreground">{description}</p>
      </div>
      <div className="flex flex-col gap-4">{children}</div>
    </section>
  );
}

/** 表单字段外壳:label + 控件 + 帮助小字 */
function FormField({
  label,
  htmlFor,
  help,
  children,
}: {
  label: string;
  htmlFor?: string;
  help?: string;
  children: ReactNode;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <label htmlFor={htmlFor} className="text-xs font-medium text-foreground">
        {label}
      </label>
      {children}
      {help !== undefined && help !== null ? <span className="text-2xs text-muted-foreground">{help}</span> : null}
    </div>
  );
}

function SummaryLine({ label, value }: { label: string; value: string }) {
  return (
    <p className="flex min-w-0 items-baseline gap-2 text-xs">
      <span className="shrink-0 text-muted-foreground">{label}</span>
      <span className="min-w-0 break-all font-medium text-foreground">{value}</span>
    </p>
  );
}
