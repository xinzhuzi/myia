import { useCallback, useEffect, useRef, useState } from "react";

import { api, onSidecarEvent } from "@/lib/api";
import type { SidecarRequestError, TestCompletedEvent } from "@/lib/api";

import { asSidecarError, listYamlFiles, saveYaml, validateYaml } from "../../yaml-editor/api";
import type { YamlFinding } from "../../yaml-editor/api";
import { buildTestOutcome } from "../api";
import type { TestOutcomeView } from "../api";
import {
  buildCategoryYaml,
  initialWizardForm,
  isPristineForm,
  wizardStepErrors,
} from "./build-category-yaml";
import type { WizardFieldRow, WizardForm } from "./build-category-yaml";

/**
 * 建源向导状态机(五步:基本信息 → 源信息 → 提取规则 → 预览保存 → 试采验证)。
 *
 * 与 use-yaml-file-editor 的形态差异(为什么不在它里面改):编辑器是
 * 「read 取 mtime → 改 → save」单向流;向导是「save 新建(expected_mtime=null)
 * → 记住应答 mtime → 返回改表单 → 重存(带 mtime)→ 再试采」的 mtime 链编排,
 * 外加分步导航/同名预检/试采 job 对账(PRD R4)。底层 yaml.validate/yaml.save
 * 走既有封装(screens/yaml-editor/api.ts,跨屏 import 先例 first-run-guide.tsx:9),
 * 零新 sidecar 协议方法。
 *
 * 保存钉序(PRD R2 第 4 步):validateYaml(content, null) 干跑(error 级 =
 * 停在第 4 步)→ saveYaml(首存 mtime=null 新建;重存带记住的 mtime 乐观锁,
 * .bak 由后端自动留底)→ 成功记住 {file, mtime} → 进第 5 步自动发起试采
 * (api.sourcesTest timeout 60)→ 等 test.completed(job_id 对账)→
 * buildTestOutcome 内嵌摘要。
 */

export type WizardStep = 1 | 2 | 3 | 4 | 5;

/** 已保存态:mtime 链基线(首存应答记住,重存带它) */
export interface WizardSaved {
  file: string;
  mtime: number;
}

/** 第 4 步保存链视图(findings = 干跑 error 级;error = 保存结构化错误) */
export interface WizardSaveState {
  running: boolean;
  findings: YamlFinding[];
  error: SidecarRequestError | null;
  /** 保存成功带回的 warning 级 findings(生成器产物通常为空;如实带回) */
  warnings: YamlFinding[];
}

/** 试采态:idle → launching → running(job_id 对账)→ done / launch_error */
export type WizardTestState =
  | { status: "idle" }
  | { status: "launching" }
  | { status: "running"; jobId: number }
  | { status: "launch_error"; error: SidecarRequestError }
  | { status: "done"; outcome: TestOutcomeView };

/** 第 1 步同名预检的文件清单视图(yaml.list 一次调用同时供 configDir) */
interface ListingState {
  status: "loading" | "ready" | "error";
  configDir: string | null;
  /** 文件名集合(如 gpu-prices.yaml;与 <id>.yaml 对比) */
  names: Set<string>;
  error: SidecarRequestError | null;
}

const INITIAL_SAVE: WizardSaveState = { running: false, findings: [], error: null, warnings: [] };

/** 与 use-yaml-file-editor/first-run-guide 同款拼路径(configDir 缺省回退 config) */
function joinPath(dir: string, name: string): string {
  return dir.endsWith("/") || dir.endsWith("\\") ? `${dir}${name}` : `${dir}/${name}`;
}

/**
 * 保存/干跑结构化错误 → 人话解释行(R4 错误码族;后端 code 原样保留展示,
 * 此处补一句人话)。锚点:desktop/entry.py `_m_yaml_save` 围栏
 * (invalid_file_stem/file_not_found/mtime_conflict/category_invalid/
 * duplicate_category_id)+ schema.py:1859-1866(invalid_cron)。
 */
export function explainSaveError(error: SidecarRequestError): string {
  switch (error.code) {
    case "invalid_file_stem":
      return "文件名不合规:换个品类 id(小写字母/数字/-/_,1-64 字符)。";
    case "mtime_conflict":
      return "文件已被其他窗口改动。可关闭向导去「YAML配置」对照,或换个 id 重来。";
    case "duplicate_category_id":
      return "这个品类 id 已被别的品类文件用掉了,换一个 id 再保存。";
    case "category_invalid":
      return "配置没过校验,文件没有写入;回上一步改完再保存。";
    case "invalid_cron":
      return "自定义抓取频率不是合法的 5 段 cron;可以先换回预设频率。";
    case "file_not_found":
      return "目标文件不存在(可能刚被别处删除);换个 id 重新保存。";
    default:
      return "保存失败;稍后重试,或关闭向导到「YAML配置」处理。";
  }
}

export interface UseSourceWizardResult {
  step: WizardStep;
  form: WizardForm;
  /** 表单有任何用户输入(与初始预填态对照) */
  formDirty: boolean;
  /** 关闭守卫:未动过任何字段直接关;有输入或已保存未完成先 confirm */
  confirmClose: () => boolean;
  /** 分步校验(纯函数;1-3 有门,4/5 恒空——第 4 步走真实干跑) */
  stepErrors: (step: WizardStep) => string[];
  /** 步导航(1-4 向前由对话框校验门控;回退自由;5 只经保存进入;越界钳到 1-5) */
  goToStep: (next: number) => void;
  /** 单字段 patch(表单变更即清过期的保存 findings/错误;saved 链保留) */
  patchForm: (patch: Partial<WizardForm>) => void;
  patchField: (index: number, patch: Partial<WizardFieldRow>) => void;
  addField: () => void;
  removeField: (index: number) => void;
  /** 同名预检:<id>.yaml 已在 config 目录 → 提示文案;预检不可用/不存在 → null */
  idExistsWarning: string | null;
  listingStatus: ListingState["status"];
  saved: WizardSaved | null;
  save: WizardSaveState;
  /** 第 4 步「保存」:干跑 → 落盘 → 记 mtime → 进第 5 步并自动发起试采 */
  saveAndAdvance: () => Promise<void>;
  test: WizardTestState;
  /** 试采发起(保存成功自动调;发起失败后的「重试」也走它) */
  launchTest: () => Promise<void>;
  /** 第 5 步「返回修改」:回第 3 步(表单态全保留,saved 链保留) */
  backToEdit: () => void;
}

export function useSourceWizard(): UseSourceWizardResult {
  const [step, setStep] = useState<WizardStep>(1);
  const [form, setForm] = useState<WizardForm>(initialWizardForm);
  const [listing, setListing] = useState<ListingState>({
    status: "loading",
    configDir: null,
    names: new Set(),
    error: null,
  });
  const [saved, setSaved] = useState<WizardSaved | null>(null);
  const [save, setSave] = useState<WizardSaveState>(INITIAL_SAVE);
  const [test, setTest] = useState<WizardTestState>({ status: "idle" });

  /** 事件对账/默认参数读取用 ref(不吃闭包陈旧) */
  const savedRef = useRef<WizardSaved | null>(null);
  savedRef.current = saved;
  const testRef = useRef<WizardTestState>({ status: "idle" });
  testRef.current = test;
  const sourceNameRef = useRef(form.sourceName.trim());
  sourceNameRef.current = form.sourceName.trim();
  /** 保存/试采在途应答丢弃序号(快速连续操作防串台) */
  const seqRef = useRef(0);

  const stepErrors = useCallback((target: WizardStep) => wizardStepErrors(form, target), [form]);

  /** 步导航(值域钉死 1-5;向前门控在对话框,4→5 只能走保存成功) */
  const goToStep = useCallback((next: number) => {
    const clamped = Math.min(5, Math.max(1, Math.trunc(next)));
    setStep(clamped as WizardStep);
  }, []);

  // 第 1 步加载:yaml.list 一次拿 configDir + 文件清单(同名预检;失败不拦,
  // 后端 mtime 围栏是终门)
  useEffect(() => {
    let disposed = false;
    listYamlFiles()
      .then((result) => {
        if (disposed) return;
        setListing({
          status: "ready",
          configDir: result.config_dir,
          names: new Set(result.files.map((entry) => entry.name)),
          error: null,
        });
      })
      .catch((error) => {
        if (disposed) return;
        setListing({ status: "error", configDir: null, names: new Set(), error: asSidecarError(error) });
      });
    return () => {
      disposed = true;
    };
  }, []);

  // test.completed 事件回屏(与 sources-screen 同款订阅;按 job_id 对账防串台)
  useEffect(() => {
    let unlisten: (() => void) | null = null;
    let disposed = false;
    void onSidecarEvent((event) => {
      if (event.type !== "test.completed") return;
      const testEvent = event as TestCompletedEvent;
      const current = testRef.current;
      if (current.status !== "running" || testEvent.job_id !== current.jobId) return;
      setTest({ status: "done", outcome: buildTestOutcome(testEvent, sourceNameRef.current) });
    })
      .then((fn) => {
        if (disposed) fn();
        else unlisten = fn;
      })
      .catch(() => {
        // 浏览器直开无事件通道:发起错误已如实呈现,零行为变化(先例同款)
      });
    return () => {
      disposed = true;
      unlisten?.();
    };
  }, []);

  /** 表单变更公共外壳:应用变更 + 清过期的保存 findings/错误(saved 链保留) */
  const mutateForm = useCallback((mutate: (prev: WizardForm) => WizardForm) => {
    setForm(mutate);
    setSave((prev) =>
      prev.findings.length > 0 || prev.error !== null ? { ...prev, findings: [], error: null } : prev,
    );
  }, []);

  const patchForm = useCallback(
    (patch: Partial<WizardForm>) => {
      mutateForm((prev) => ({ ...prev, ...patch }));
    },
    [mutateForm],
  );

  const patchField = useCallback(
    (index: number, patch: Partial<WizardFieldRow>) => {
      mutateForm((prev) => ({
        ...prev,
        fields: prev.fields.map((row, rowIndex) => (rowIndex === index ? { ...row, ...patch } : row)),
      }));
    },
    [mutateForm],
  );

  const addField = useCallback(() => {
    mutateForm((prev) => ({
      ...prev,
      fields: [...prev.fields, { name: "", selector: "", useHref: false }],
    }));
  }, [mutateForm]);

  const removeField = useCallback(
    (index: number) => {
      mutateForm((prev) => ({ ...prev, fields: prev.fields.filter((_, rowIndex) => rowIndex !== index) }));
    },
    [mutateForm],
  );

  const formDirty = !isPristineForm(form);

  /** 关闭守卫(PRD R4):未动过任何字段直接关;有输入或已保存未完成先确认 */
  const confirmClose = useCallback((): boolean => {
    if (!formDirty && saved === null) return true;
    return window.confirm("向导内容还没走完(已保存的文件会保留),确定关闭?");
  }, [formDirty, saved]);

  const idExistsWarning =
    listing.status === "ready" && form.categoryId.trim() !== ""
      ? listing.names.has(`${form.categoryId.trim()}.yaml`)
        ? `已有同名文件 ${form.categoryId.trim()}.yaml,保存会被拦;换一个 id,或去「YAML配置」编辑它`
        : null
      : null;

  /** 试采发起:api.sourcesTest({file, source, timeout: 60});失败结构化展示可重试 */
  const launchTest = useCallback(async (fileOverride?: string) => {
    const file = fileOverride ?? savedRef.current?.file;
    if (file === undefined) return;
    const seq = ++seqRef.current;
    setTest({ status: "launching" });
    try {
      const started = await api.sourcesTest({ file, source: sourceNameRef.current, timeout: 60 });
      if (seq !== seqRef.current) return;
      setTest({ status: "running", jobId: started.job_id });
    } catch (error) {
      if (seq !== seqRef.current) return;
      setTest({ status: "launch_error", error: asSidecarError(error) });
    }
  }, []);

  /** 第 4 步「保存」钉序:干跑(error 停)→ 落盘(mtime 链)→ 第 5 步 + 自动试采 */
  const saveAndAdvance = useCallback(async () => {
    if (save.running) return;
    const content = buildCategoryYaml(form);
    const seq = ++seqRef.current;
    setSave({ ...INITIAL_SAVE, running: true });
    try {
      const check = await validateYaml(content, null);
      if (seq !== seqRef.current) return;
      const blocking = check.findings.filter((finding) => finding.level === "error");
      if (!check.valid || blocking.length > 0) {
        // 停在第 4 步原样展示 error 级 findings,不发保存
        setSave({ ...INITIAL_SAVE, findings: blocking.length > 0 ? blocking : check.findings });
        return;
      }
      const dir = listing.configDir ?? "config";
      const file = joinPath(dir, `${form.categoryId.trim()}.yaml`);
      const result = await saveYaml(file, content, savedRef.current === null ? null : savedRef.current.mtime);
      if (seq !== seqRef.current) return;
      setSaved({ file: result.file, mtime: result.mtime });
      setSave({ ...INITIAL_SAVE, warnings: result.warnings });
      setStep(5);
      void launchTest(result.file);
    } catch (error) {
      if (seq !== seqRef.current) return;
      setSave({ ...INITIAL_SAVE, error: asSidecarError(error) });
    }
  }, [form, launchTest, listing.configDir, save.running]);

  /** 第 5 步「返回修改」:回第 3 步;表单与 saved 链全保留,试采态清零 */
  const backToEdit = useCallback(() => {
    setTest({ status: "idle" });
    setStep(3);
  }, []);

  return {
    step,
    form,
    formDirty,
    confirmClose,
    stepErrors,
    goToStep,
    patchForm,
    patchField,
    addField,
    removeField,
    idExistsWarning,
    listingStatus: listing.status,
    saved,
    save,
    saveAndAdvance,
    test,
    launchTest,
    backToEdit,
  };
}
