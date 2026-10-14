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

- [ ] 两模块删除后全仓零活引用(头注/版本注记的历史性提及除外)
- [ ] pyproject extras `huggingface-hub` 依赖处置:models.py 删除后 vision extras
      内零消费者 → 从 vision/all extras 移除并 `uv lock` 校验(本机 sync 带
      `--all-extras`)
- [ ] 真机 vision.yaml 落位 + 真图冒烟通过
- [ ] 双测面 + build 绿;detect-changes 影响面 = 预期符号
