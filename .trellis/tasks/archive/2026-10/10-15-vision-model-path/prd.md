# PRD:看图改 LM Studio 客户端制——MYIA 不自跑视觉大模型

## Goal

看图本地通道改为**纯客户端**:配置 LM Studio 等 OpenAI 兼容本地服务的
base_url / 模型名 / 可选 api_key;拆除 MYIA 自跑视觉大模型的全部设施
(应用内 HF 下载、模型目录扫描、mlx_vlm.server 自起代管)。

## 背景(主人指令,2026-10-15 三连)

> 1.「要给路径,myia 使用路径下的大模型,而不是自己下载大模型,这是错误的设计」
> 2.「要用 /Users/zhengbingjin/Project/IP/漫影工作室/comfyui/models/ 这个下面的」
> 3.「这个看图大模型不能使用本地模型,你要配置成为 lmstudio 的apikey,url等等,
>    而不是直接自己本地看图,这样太奇怪了,并且要使用目前lmstudio下载的那个
>    qwen27B 大模型」
> 4.「就用 qwen3.8-27b-coder390 这个进行识图吧」

指令演化:1+2 定调「不自下载」;3+4 终局定调「不自跑模型」——本地看图走
LM Studio 已在跑的服务,MYIA 只当 OpenAI 兼容客户端(同云端 GLM 的形态,
端点换成本地)。

本机实况(2026-10-15 探测):LM Studio `http://127.0.0.1:1234` 在跑,唯一
模型 `qwen3.8-27b-coder390`(GGUF + mmproj 视觉投影);**真图验证通过**
(1×1 红像素图,模型答「红」);当前未开 API 鉴权(无 key 可访问)。

## Requirements

- **R1 本地通道三件套**:vision.yaml `local` = `base_url` + `model`(模型名,
  非路径)+ `api_key`(可选 `keychain:` 引用,`myia/image/local_api_key`);
  缺省 base_url 改 LM Studio 标准口 `http://127.0.0.1:1234/v1`。
- **R2 拆自跑链**:`myssia.vision.models`(下载/扫描/激活)与
  `myssia.vision.server`(mlx_vlm 自起代管)两模块删除;管线 vl:local 前
  的 ensure 环删除;协议 `image.models.*` 四方法、`image.server.*` 两方法、
  `image.models.progress/completed` + `image.server.completed` 三事件全下线。
- **R3 设置屏**:「看图模型管理」卡整体删除;看图配置卡本地区 =
  base_url / 模型名 / 本地 API Key(可选,入钥匙串)三字段。
- **R4 本机配置落位**:真机 vision.yaml `local` 指向 LM Studio + 
  `qwen3.8-27b-coder390`(api_key 不设——LM Studio 未开鉴权,字段已备好,
  主人日后开鉴权即录)。
- **R5 云端通道/OCR/table 不动**。

## 非目标

- 不做 LM Studio 模型发现/下拉(模型在 LM Studio 应用里管,MYIA 只填名字)。
- 不动 comfyui/models 目录(指令 2 的路径制方案已被指令 3 取代)。

## Acceptance Criteria

- [x] AC1 代码面:`src/myssia/vision/{models,server}.py` 不存在;全仓
      `rg 'ensure_vision_server|image\.models|image\.server' src/ desktop/` 零活引用
      (entry.py/spec/types 内仅历史注记;docs/build 脚本/pyproject 的
      huggingface-hub 同批摘除)。
- [x] AC2 设置屏无模型管理卡、无下载/删除/启动服务任何入口;本地三字段在
      (vision-form.tsx 单卡;vision-models.test.tsx 删除,form 薄测补)。
- [x] AC3 真机 vision.yaml:local.base_url=1234、model=qwen3.8-27b-coder390
      (主人晨间已手改到位,新代码装载验证);以该配置跑 VisionClient 真图冒烟,
      返回「红」(LM Studio :1234 实跑,mmproj 视觉链真出话;api_key 未设 =
      端点未开鉴权,字段已备好)。
- [x] AC4 门禁:pytest 全量 6316 passed / 56 skipped;vitest 932 passed;
      tsc + vite build 绿;ruff 改动域零告警。
- [x] AC5 旧 vision.yaml(无 local.api_key、base_url 是 8080)照常装载
      (test_vision.py 用例;显式旧值不迁移,行为 = 按显式值连)。

## 追记(交付后主人令两笔,同屏追加)

1. 云端缺省模型改 `glm-5.3-flash`(实证:ui-cloud5 视觉通道 z-ai/glm-5.3-flash
   5 屏 8 调用吃图;官方端点现有钥 1113 无余额,云端真通待 funded 钥)。
2. 云端三件套补齐:`云端 base_url` 入表单成可编辑字段(原先只读保留),
   云端 base_url/API Key/模型一组;中转端点可直接指。
两笔均已换装装机件;本机 vision.yaml cloud.model=glm-5.3-flash。

## 终验(10-15 晚,主人过目)

设置·看图分区四处核对**「与上述一致→过」**:无模型管理卡、本地三字段(1234/qwen3.8-27b-coder390)、云端三件套(地址可编辑+API Key+缺省 glm-5.3-flash)。本档全闭归档;云端真调通待 funded 钥(追记 1 所注,非本档欠账)。
