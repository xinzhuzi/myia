# Implement:看图 LM Studio 客户端制

## 批次

1. **Python 能力层**:settings.py(local.api_key/新缺省/resolve_local_api_key;
   回退早前误加的 models_dir)→ 删 models.py/server.py → client.py docstring
   → collect.py `_VlChannel` local 分支。
2. **Python 协议/管线**:entry.py(整段删除 image.models/server 方法+事件+状态
   +imports+注册表+头注+v16)、pipeline.py 删 ensure 环。
3. **TS 层**:types.ts → logs/api.ts → vision-api.ts → vision-form.tsx
   (删卡+本地三字段)。
4. **测试**:删 tests/vision/test_vision_models_server.py;改 test_vision.py
   (8080 缺省断言→1234、local api_key 用例);改 test_desktop_sidecar_protocol.py
   (image.models/server 段删);删 vision-models.test.tsx,增 vision-form.test.tsx。
5. **spec + 真机**:.trellis/spec/desktop/sidecar-protocol.md 同步;真机
   vision.yaml 落位;VisionClient 真图冒烟(答「红」)。

## 验证命令

```bash
rg -n 'ensure_vision_server|vision\.models|vision\.server|image\.models|image\.server' src/ desktop/ --glob '!*.md'
uv run pytest tests/vision tests/desktop -q
npm --prefix desktop/ui-src run test -- --run src/screens/settings
npm --prefix desktop/ui-src run build
gitnexus detect-changes -r shishi --scope staged
```

## 检查单

- [x] models.py/server.py 删除后全仓零活引用(头注/版本注记的历史性提及除外;
      docs zh/en、build-sidecar.sh、pyproject 的 huggingface-hub 同批摘净)
- [x] pyproject extras `huggingface-hub` 已从 vision/all 移除,uv.lock 刷新
      (锁内残留为其余 extras 的传递依赖,非直接要求)
- [x] 真机 vision.yaml 落位(主人晨间已手改 LM Studio + qwen3.8-27b-coder390,
      新装载器验证)+ VisionClient 真图冒烟答「红」
- [x] 双测面 + build 绿(pytest 6316 / vitest 932 / tsc+vite / ruff);
      detect-changes 影响面 = VisionForm/saveImageConfig 流,符合预期
- [x] 装机:净树 UI(git archive HEAD 导出构建,零裹挟并行 WIP)→ tauri
      build → 外科净化 Resources(macos_notify 回 HEAD 版 + 清 __pycache__)→
      换装 /Applications/世事.app → 清 WKWebView 缓存;在跑实例下次重启生效
