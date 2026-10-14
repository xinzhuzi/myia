/**
 * 看图分区协议封装(task 10-03-vision-pipeline 拆屏:image.* 配置面 =
 * image.config.read / image.config.save 由设置屏 VisionForm 使用)。
 * 10-15-vision-model-path 客户端制收窄:image.models.* / image.server.* 六方法
 * 与模型下载/server ensure 三事件已随协议 v16 下线 —— 本地通道 = LM Studio
 * 等 OpenAI 兼容端点的纯客户端(vision.yaml local = base_url/model/api_key
 * 三件套),MYIA 不下载/不自跑大模型。
 *
 * 数据面 = sidecar 协议:
 *   image.config.read {}       → {file, exists, config}(config 为脱敏
 *                                VisionConfig;本模块解包返 config)
 *   image.config.save {config} → {ok}(同门校验失败零写入)
 *   image.files.purge {days}   → {deleted, bytes_freed}(CLI 面能力,零 UI)
 *
 * 惯例与 sources/settings 屏一致:invoke 直连壳命令 `sidecar_request` +
 * asSidecarError 归一化(错误必得 code/path/message)。
 */
import { invoke } from "@tauri-apps/api/core";

import type {
  ImageConfigReadResult,
  VisionConfig,
} from "@/lib/api";

import { asSidecarError } from "./api";

// ---------------------------------------------------------------------------
// 协议方法封装(走壳命令 sidecar_request;方法名与 entry.py 双侧同步)
// ---------------------------------------------------------------------------

/** 读看图结构配置(vision.yaml;keychain 引用不回明文)。
 *  协议应答是 {file, exists, config} 包装(entry.py 锁定),此处解包返 config;
 *  mock/异常应答缺 config 字段时原样透传,由调用方形状防御如实呈现。 */
export async function readImageConfig(): Promise<VisionConfig> {
  try {
    const response = await invoke<ImageConfigReadResult>("sidecar_request", {
      method: "image.config.read",
      params: {},
    });
    if (response && typeof response === "object" && "config" in response) {
      return response.config;
    }
    return response as unknown as VisionConfig;
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 写看图结构配置(同门校验失败零写入);设置屏 VisionForm 复用。 */
export async function saveImageConfig(config: VisionConfig): Promise<{ ok: true }> {
  try {
    return await invoke<{ ok: true }>("sidecar_request", {
      method: "image.config.save",
      params: { config },
    });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

// ---------------------------------------------------------------------------
// 缺省配置(sidecar 未实现/未配置时的回退;形状与 vision.yaml 缺省一致)
// ---------------------------------------------------------------------------

export const DEFAULT_VISION_CONFIG: VisionConfig = {
  channel_default: "local",
  // 带 /v1 后缀,与 Python 缺省一致(settings.py DEFAULT_LOCAL_BASE_URL:SDK 按
  // {base_url}/chat/completions 发请求;客户端制缺省 = LM Studio 标准口 1234)
  local: { base_url: "http://127.0.0.1:1234/v1", model: "", api_key: null },
  cloud: { base_url: "https://open.bigmodel.cn/api/paas/v4", model: "glm-4.6v", api_key: null },
  ocr: { enabled: true, engine_default: "vision" },
};
