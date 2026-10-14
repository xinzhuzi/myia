# Design:看图 LM Studio 客户端制

## 1. 配置面(vision.yaml)

```yaml
local:
  base_url: http://127.0.0.1:1234/v1   # LM Studio 标准口(新缺省)
  model: qwen3.8-27b-coder390           # 模型名(OpenAI model 参,非路径)
  api_key: keychain:myia/image/local_api_key   # 可选;null/缺省 = 不带鉴权
```

- `settings.py`:`_LOCAL_KEYS = ("base_url", "model", "api_key")`;
  `VisionConfig.local_api_key_ref: str | None = None`(校验复用
  `_require_keychain_ref`,泛化出 field/keychain 参);`DEFAULT_LOCAL_BASE_URL`
  改 `http://127.0.0.1:1234/v1`;新增 `KEYCHAIN_LOCAL_API_KEY =
  "myia/image/local_api_key"` 与 `resolve_local_api_key`(显式引用解析,
  失败原样上抛;未配 = None,无回落链)。
- 兼容:老 yaml 的 8080 显式值照载照连(不迁移);无 api_key 键 = None。

## 2. 能力层

- **删** `myssia/vision/models.py`(下载/清单/激活——整模块)与
  `myssia/vision/server.py`(mlx_vlm 自起/健康等待/日志泵——整模块)。
  `vision/__init__.py` 不引这两件,零改动。
- `client.py`:构造语义已通(`api_key=None` = 剥鉴权头;给 key = Bearer)——
  仅 docstring 措辞更新(model=端点模型名;本地示例 LM Studio)。
- `collect.py` `_VlChannel` local 分支:补 `resolve_local_api_key`(解析失败
  = `credential_resolve_failed` 降级,同云端门风);`no_local_model` 语义改为
  「本地模型名未配」。

## 3. 管线(pipeline.py)

- 删 vl 前的 ensure 环(import + `asyncio.to_thread(ensure_vision_server…)`
  块)。LM Studio 由用户自己跑;不在跑 = VL 按既有 `vl_skipped_error` 降级。

## 4. 协议面(desktop/entry.py)

- 删方法:`image.models.list/download/delete/activate`(四)、
  `image.server.status/ensure`(两);删事件:`image.models.progress/completed`
  (已无生产者)与 `image.server.completed`;删 `_SERVER_ENSURE_*` 单飞态与
  ensure worker、`_vision_models_dir`/`_active_model_path` 助手、models/server
  两模块 import。
- `image.config.read/save`、`image.files.purge` 原样。
- 版本:`PROTOCOL_VERSION` 15→16,v16 注记 = 本批收窄(方法/事件移除清单)。
- 头注两段(方法表 + 详述段)与事件样例同步。

## 5. UI 面(desktop/ui-src)

- `types.ts`:删 `IMAGE_MODELS_*` 两正则、`ImageModelEntry`、`ImageModels*`
  全家、`ImageServer*` 两型;MethodMap/事件联合摘对应项;
  `VisionConfig.local` = `{base_url, model, api_key: string | null}`。
- `logs/api.ts`:事件名映射删三支(models.progress/completed、server.completed)。
- `vision-api.ts`:只剩 readImageConfig/saveImageConfig;头注重写;
  `DEFAULT_VISION_CONFIG.local` 带三键(api_key: null)。
- `vision-form.tsx`:删 `VisionModelsCard` 整组件与其 imports/state/事件订阅;
  配置卡本地区三字段(base_url/模型名/本地 API Key,keychain
  `myia/image/local_api_key`,「输入后才写入;LM Studio 未开鉴权可留空」);
  卡描述改为「本地 = LM Studio 等 OpenAI 兼容端点;云端 = GLM」。
- 测试:`vision-models.test.tsx` 删除(被测组件已亡);新增
  `vision-form.test.tsx` 薄测(字段渲染 + 保存往返含 local.api_key 引用拼装)。

## 6. 真机落位

- `~/Library/Application Support/MYIA/vision.yaml` local 节改
  base_url=1234 / model=qwen3.8-27b-coder390(不动 cloud;`.bak-*` 一律不碰)。
- 冒烟:以真配置构造 `VisionClient` 发 1×1 红像素图,断言回「红」。

## 7. 风险

- LM Studio 不在跑时本地 VL 降级(`vl_skipped_error`)——与旧形态「server
  没起」等价,无新增风险;不自起反而消除双 server 抢 8080 的历史隐患。
- 收窄批必 bump 协议版本(旧 UI 调删方法得 method_not_found 结构化降级);
  sidecar 与 UI 同包同发,无错配窗口。
