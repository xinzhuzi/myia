import { KeyRound, Save } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { SidecarRequestError } from "@/lib/api";
import type { OcrEngine, VisionChannel, VisionConfig } from "@/lib/api";

import {
  DEFAULT_VISION_CONFIG,
  readImageConfig,
  saveImageConfig,
} from "./vision-api";

import { saveSecret } from "./api";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
import { SettingRow } from "./settings-row";

/** 云端 api_key 的钥匙链规范名(与 sidecar vision.yaml 引用同口径) */
const SECRET_NAME_IMAGE_API_KEY = "myia/image/api_key";
/** 本地端点(LM Studio 等)可选 api_key 的钥匙链规范名(10-15 客户端制) */
const SECRET_NAME_IMAGE_LOCAL_API_KEY = "myia/image/local_api_key";

interface VisionFormProps {
  /** 设置屏已加载的钥匙链名清单(判 api_key 是否已存;值永不可读) */
  secretNames: string[] | null;
}

interface VisionFormState {
  channelDefault: VisionChannel;
  ocrEngine: OcrEngine;
  localBaseUrl: string;
  localModel: string;
  cloudModel: string;
}

function stateFromConfig(config: VisionConfig): VisionFormState {
  return {
    channelDefault: config.channel_default,
    ocrEngine: config.ocr.engine_default,
    localBaseUrl: config.local.base_url,
    localModel: config.local.model,
    cloudModel: config.cloud.model,
  };
}

/** 应答形状防御:mock/异常环境下 invoke 可能回 undefined,不构造即崩。 */
function isVisionConfigLike(value: unknown): value is VisionConfig {
  return (
    typeof value === "object" &&
    value !== null &&
    typeof (value as VisionConfig).channel_default === "string" &&
    typeof (value as VisionConfig).local?.base_url === "string"
  );
}

/**
 * 设置 → 看图分区(单卡,10-15-vision-model-path 客户端制):二级看图通道
 * 与 OCR 引擎结构配置(经 image.config.save 落 MYIA_HOME/vision.yaml)。
 * 本地通道 = LM Studio 等 OpenAI 兼容端点的纯客户端 —— base_url / 模型名 /
 * 可选 api_key 三件套,MYIA 不下载/不自跑大模型(模型在 LM Studio 应用里
 * 管理);云端 = GLM 等。凭据铁律照旧:两个 api_key 都只经 secret.set 入
 * 钥匙串,配置里只落 keychain: 引用 —— 明文拒载,值不回显不落盘。
 */
export function VisionForm({ secretNames }: VisionFormProps) {
  const [form, setForm] = useState<VisionFormState>(stateFromConfig(DEFAULT_VISION_CONFIG));
  /** 原样保存 read 应答:save 时保留未入表单的字段(cloud.base_url/ocr.enabled 等) */
  const [loaded, setLoaded] = useState<VisionConfig>(DEFAULT_VISION_CONFIG);
  const [loadedError, setLoadedError] = useState<SidecarRequestError | null>(null);
  const [apiKey, setApiKey] = useState("");
  const [localApiKey, setLocalApiKey] = useState("");
  const [errors, setErrors] = useState<Partial<Record<"localBaseUrl", string>>>({});
  const [saving, setSaving] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [saveError, setSaveError] = useState<SidecarRequestError | null>(null);

  useEffect(() => {
    let cancelled = false;
    readImageConfig()
      .then((value) => {
        if (cancelled) return;
        if (!isVisionConfigLike(value)) {
          throw new SidecarRequestError({ code: "transport_error", path: "$", message: "image.config.read 应答形状异常" });
        }
        setLoaded(value);
        setForm(stateFromConfig(value));
      })
      .catch((raw) => {
        if (!cancelled) setLoadedError(raw instanceof SidecarRequestError ? raw : new SidecarRequestError({ code: "transport_error", path: "$", message: String(raw) }));
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const handleSave = useCallback(async () => {
    const localBase = form.localBaseUrl.trim() || DEFAULT_VISION_CONFIG.local.base_url;
    if (!/^https?:\/\//.test(localBase)) {
      setErrors({ localBaseUrl: "本地 base_url 须为 http(s) 地址(留空用默认 http://127.0.0.1:1234/v1)" });
      return;
    }
    setErrors({});
    setSaving(true);
    setSaveError(null);
    setStatus(null);
    try {
      // 1) 凭据(如有输入)只入钥匙链;配置里仅落引用
      let apiKeyRef = loaded.cloud.api_key ?? null;
      if (apiKey) {
        await saveSecret(SECRET_NAME_IMAGE_API_KEY, apiKey);
        apiKeyRef = `keychain:${SECRET_NAME_IMAGE_API_KEY}`;
      }
      let localApiKeyRef = loaded.local.api_key ?? null;
      if (localApiKey) {
        await saveSecret(SECRET_NAME_IMAGE_LOCAL_API_KEY, localApiKey);
        localApiKeyRef = `keychain:${SECRET_NAME_IMAGE_LOCAL_API_KEY}`;
      }
      // 2) 结构配置整份写回(未入表单字段按 read 原样保留)
      const config: VisionConfig = {
        channel_default: form.channelDefault,
        local: { base_url: localBase, model: form.localModel.trim(), api_key: localApiKeyRef },
        cloud: { base_url: loaded.cloud.base_url, model: form.cloudModel.trim() || loaded.cloud.model, api_key: apiKeyRef },
        ocr: { enabled: loaded.ocr.enabled, engine_default: form.ocrEngine },
      };
      await saveImageConfig(config);
      setApiKey(""); // key 保存即清:不留存、不回显
      setLocalApiKey("");
      // 3) 复核往返:重读配置与所写一致才算数
      const rereadValue = await readImageConfig();
      const consistent =
        isVisionConfigLike(rereadValue) &&
        rereadValue.channel_default === config.channel_default &&
        rereadValue.local.base_url === config.local.base_url &&
        rereadValue.local.model === config.local.model &&
        rereadValue.local.api_key === config.local.api_key &&
        rereadValue.cloud.model === config.cloud.model &&
        rereadValue.ocr.engine_default === config.ocr.engine_default;
      setStatus(
        consistent
          ? "看图配置已保存(vision.yaml),重读复核一致"
          : "已保存,但重读复核未确认 —— 请检查本地服务日志(配置可能在校验时被改写)",
      );
      if (consistent && isVisionConfigLike(rereadValue)) {
        setLoaded(rereadValue);
        setForm(stateFromConfig(rereadValue));
      }
    } catch (raw) {
      setSaveError(raw instanceof SidecarRequestError ? raw : new SidecarRequestError({ code: "transport_error", path: "$", message: String(raw) }));
    } finally {
      setSaving(false);
    }
  }, [apiKey, localApiKey, form, loaded]);

  const keyInKeychain = secretNames?.includes(SECRET_NAME_IMAGE_API_KEY) ?? false;
  const localKeyInKeychain = secretNames?.includes(SECRET_NAME_IMAGE_LOCAL_API_KEY) ?? false;

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <KeyRound className="size-4 text-muted-foreground" />
          看图
        </CardTitle>
        <CardDescription>
          本地通道 = LM Studio 等 OpenAI 兼容端点(模型在 LM Studio 里管理);云端 = GLM;配置落 MYIA_HOME/vision.yaml
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {loadedError ? (
          // 加载失败是注记不是告警(不占 role=alert:设置屏既有用例对 alert
          // 单匹配断言);协议未收编(Python 侧未落地)时如实提示,保存可试
          <div
            role="note"
            className="rounded-md border border-border bg-muted/30 px-3 py-2 text-xs text-muted-foreground"
            data-testid="vision-config-note"
          >
            现值读取失败(code={loadedError.code}:{loadedError.message});表单按缺省展示。保存将尝试写回
            image.config.save —— 协议未收编(Python 侧未落地)时会得到结构化 method_not_found,如实呈现。
          </div>
        ) : null}
        <SettingRow label="默认通道" description="本地端点优先;云端出网(按云端 key)">
          <Select
            value={form.channelDefault}
            onValueChange={(value) => setForm((prev) => ({ ...prev, channelDefault: value as VisionChannel }))}
          >
            <SelectTrigger aria-label="看图默认通道" className="w-64 min-w-0 flex-1 sm:flex-none">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="local">本地端点</SelectItem>
              <SelectItem value="cloud">云端(出网)</SelectItem>
            </SelectContent>
          </Select>
        </SettingRow>
        <SettingRow label="OCR 默认引擎" description="Vision(macOS 原生)或 RapidOCR">
          <Select
            value={form.ocrEngine}
            onValueChange={(value) => setForm((prev) => ({ ...prev, ocrEngine: value as OcrEngine }))}
          >
            <SelectTrigger aria-label="OCR 默认引擎" className="w-64 min-w-0 flex-1 sm:flex-none">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="vision">Vision(macOS)</SelectItem>
              <SelectItem value="rapidocr">RapidOCR</SelectItem>
            </SelectContent>
          </Select>
        </SettingRow>
        <FieldInput
          label="本地 base_url"
          aria-label="本地 base_url"
          placeholder="http://127.0.0.1:1234/v1(LM Studio;留空用默认)"
          value={form.localBaseUrl}
          onChange={(event) => setForm((prev) => ({ ...prev, localBaseUrl: event.target.value }))}
          error={errors.localBaseUrl}
          hint="OpenAI 兼容端点(含 /v1 路径);默认 LM Studio 标准口 http://127.0.0.1:1234/v1"
        />
        <FieldInput
          label="本地模型"
          aria-label="本地模型"
          placeholder="LM Studio 模型列表里的模型名"
          value={form.localModel}
          onChange={(event) => setForm((prev) => ({ ...prev, localModel: event.target.value }))}
          hint="端点上的模型名(本地服务模型列表 id);本地看图走它在 LM Studio 里加载的模型"
        />
        <FieldInput
          label="本地 API Key"
          aria-label="本地 API Key"
          type="password"
          autoComplete="new-password"
          placeholder="本地服务开了 API 鉴权才需要;留空 = 不带鉴权"
          value={localApiKey}
          onChange={(event) => setLocalApiKey(event.target.value)}
          hint={`LM Studio 未开鉴权可留空;输入则写入钥匙串 ${SECRET_NAME_IMAGE_LOCAL_API_KEY},保存即清,永不回显`}
          action={
            secretNames !== null ? (
              localKeyInKeychain ? (
                <Badge variant="ok">本地 key 已在钥匙串</Badge>
              ) : (
                <Badge variant="outline">本地无鉴权</Badge>
              )
            ) : null
          }
        />
        <FieldInput
          label="云端模型"
          aria-label="云端模型"
          placeholder="glm-5.3-flash"
          value={form.cloudModel}
          onChange={(event) => setForm((prev) => ({ ...prev, cloudModel: event.target.value }))}
          hint="默认 glm-5.3-flash(云端评审视觉通道实证);留空按已保存值"
        />
        <FieldInput
          label="云端 API Key"
          aria-label="云端 API Key"
          type="password"
          autoComplete="new-password"
          placeholder="输入后才写入;保存即清,永不回显"
          value={apiKey}
          onChange={(event) => setApiKey(event.target.value)}
          hint={`写入钥匙串 ${SECRET_NAME_IMAGE_API_KEY};未录时云端回落既有 LLM key(myia/llm/api_key)`}
          action={
            secretNames !== null ? (
              keyInKeychain ? (
                <Badge variant="ok">key 已在钥匙串</Badge>
              ) : (
                <Badge variant="outline">key 未录(云端回落 LLM key)</Badge>
              )
            ) : null
          }
        />
        <div className="flex items-center gap-2">
          <Button size="sm" onClick={() => void handleSave()} disabled={saving}>
            <Save className="size-3.5" />
            保存看图配置
          </Button>
          {status ? (
            <span role="status" className="text-xs text-ok" data-testid="vision-save-status">
              {status}
            </span>
          ) : null}
        </div>
        {saveError ? <ErrorBox error={saveError} /> : null}
      </CardContent>
    </Card>
  );
}
