import { ChevronRight, FilePlus2, Rocket, ScrollText, Send } from "lucide-react";
import { useCallback, useState } from "react";

import { MyssiaMark } from "@/components/myssia-mark";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import type { SidecarRequestError } from "@/lib/api";
import { asSidecarError } from "./api";
import { getYamlTemplate, saveYaml } from "../yaml-editor/api";

/** demo 品类文件名(stem 过 CATEGORY_ID 预检;与官方件 myssia-demo.yaml 同名同源) */
const DEMO_STEM = "myssia-demo";

/** 一键 demo 的阶段机:idle → 创建(模板+落盘)→ 发起(run.start)→ done/failed */
type DemoPhase =
  | { kind: "idle" }
  | { kind: "busy"; step: "creating" | "starting" }
  | { kind: "done"; runId: number; file: string }
  | { kind: "failed"; error: SidecarRequestError };

interface GuideCardSpec {
  icon: typeof FilePlus2;
  title: string;
  description: string;
  href: string;
}

/** 指引卡清单(Kestra OverviewBottom 范式:图标+标题+描述+chevron 的横排行) */
const GUIDE_CARDS: GuideCardSpec[] = [
  {
    icon: FilePlus2,
    title: "从模板新建品类",
    description: "到「配置编辑」用最小模板起草品类 YAML:声明 sources、schedule 与 push",
    href: "#/yaml-editor",
  },
  {
    icon: ScrollText,
    title: "采集结果在日志屏",
    description: "run 的产出条数与错误行都在日志屏;跑完去那里核对",
    href: "#/logs",
  },
  {
    icon: Send,
    title: "精评与推送",
    description: "LLM 精评凭据、推送通道(chat_id/bot token)在「设置」录入(只入钥匙链)",
    href: "#/settings",
  },
];

/**
 * 首跑引导态(10-04-ui-kestra-anchor,R4):结构借自 Apache-2.0
 * kestra/ui/packages/design-system/.../KsEmptyState.vue(左对齐
 * artwork+标题+描述+动作行)与 kestra/ui/src/components/flows/
 * NoExecutions.vue + onboarding/execution/OverviewBottom.vue(「需要指引?」
 * 标签 + 边框堆叠指引卡列表),借结构改语义——
 * 「一键跑 demo」= 既有协议面的 UI 编排:yaml.template 取模板 → yaml.save
 * 落盘 myssia-demo.yaml → run.start 发起采集 → 引导去日志屏(零新后端功能)。
 * 品牌光晕/MyssiaMark 是自有品牌层(非 Kestra 元素)。
 */
export function FirstRunGuide({
  pluginsDir,
  onDemoCreated,
}: {
  pluginsDir: string | null;
  onDemoCreated: () => void | Promise<void>;
}) {
  const [phase, setPhase] = useState<DemoPhase>({ kind: "idle" });

  const runDemo = useCallback(async () => {
    setPhase({ kind: "busy", step: "creating" });
    try {
      const dir = pluginsDir ?? "plugins";
      const file = dir.endsWith("/") ? `${dir}${DEMO_STEM}.yaml` : `${dir}/${DEMO_STEM}.yaml`;
      const template = await getYamlTemplate();
      const content = template.content.replace("id: my-category", `id: ${DEMO_STEM}`);
      await saveYaml(file, content, null);
      setPhase({ kind: "busy", step: "starting" });
      const started = await api.runStart({ yaml: file });
      setPhase({ kind: "done", runId: started.run_id, file });
      await onDemoCreated();
    } catch (error) {
      setPhase({ kind: "failed", error: asSidecarError(error) });
    }
  }, [onDemoCreated, pluginsDir]);

  const busy = phase.kind === "busy";

  return (
    <section aria-label="首跑引导" className="flex flex-col gap-6 py-16" data-testid="first-run-guide">
      {/* Kestra KsEmptyState:左对齐 artwork+标题+描述+动作行(块间 gap≈21px) */}
      <div className="flex flex-col items-start gap-5 px-1">
        <div className="relative flex items-center justify-center">
          <div
            aria-hidden
            className="pointer-events-none absolute size-28 rounded-full bg-gradient-to-br from-brand-from/15 to-brand-to/15 blur-2xl"
          />
          <MyssiaMark className="relative size-12" />
        </div>
        <div className="flex max-w-sm flex-col gap-2">
          <h2 className="text-xl font-semibold text-foreground">还没有品类源</h2>
          <p className="text-sm leading-5 text-muted-foreground">
            插件目录{pluginsDir ? `(${pluginsDir})` : ""}下没有可加载的品类 YAML——真·首跑。
            一键用官方模板跑通第一个 demo 采集,或从指引开始手动建品类。
          </p>
        </div>
        <div className="flex flex-col gap-1.5">
          <Button size="sm" disabled={busy} title="模板落盘 myssia-demo.yaml 并发起一次采集(run.start)" onClick={() => void runDemo()}>
            <Rocket className={busy ? "size-3.5 animate-pulse" : "size-3.5"} />
            {phase.kind === "busy" && phase.step === "creating"
              ? "创建 demo 品类…"
              : phase.kind === "busy" && phase.step === "starting"
                ? "发起采集…"
                : "一键跑 demo"}
          </Button>
          {phase.kind === "done" ? (
            <span role="status" className="text-xs text-ok" data-testid="demo-started">
              demo 已发起(run #{phase.runId});
              <a href="#/logs" className="ml-0.5 text-primary underline-offset-2 hover:underline">
                去日志屏查看
              </a>
            </span>
          ) : null}
        </div>
        {phase.kind === "failed" ? (
          <p role="alert" className="max-w-sm text-xs text-destructive" data-testid="demo-failed">
            一键 demo 失败({phase.error.code}):{phase.error.message}
            <span className="mt-0.5 block text-muted-foreground">
              目录里已有 {DEMO_STEM}.yaml 时不会覆盖(mtime 锁);先到「配置编辑」处理同名文件。
            </span>
          </p>
        ) : null}
      </div>

      {/* Kestra NoExecutions/OverviewBottom:「需要指引?」标签 + 边框堆叠指引卡 */}
      <div className="max-w-xl">
        <p className="mb-3 text-left text-xs text-muted-foreground">需要指引?</p>
        <div className="overflow-hidden rounded-lg border border-border">
          {GUIDE_CARDS.map(({ icon: Icon, title, description, href }, index) => (
            <a
              key={href}
              href={href}
              className={
                "flex items-center gap-4 px-5 py-4 text-left transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent/40 " +
                (index > 0 ? "border-t border-border" : "")
              }
            >
              <Icon aria-hidden className="size-4 shrink-0 text-muted-foreground" />
              <span className="min-w-0 flex-1">
                <span className="block text-sm font-medium text-foreground">{title}</span>
                <span className="block text-2xs text-muted-foreground">{description}</span>
              </span>
              <ChevronRight aria-hidden className="size-4 shrink-0 text-muted-foreground" />
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}
