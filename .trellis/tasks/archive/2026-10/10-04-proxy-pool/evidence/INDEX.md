# 10-04-proxy-pool 冒烟证据(2026-10-04,proxy+win 冒烟员)

零外网口径:全部 I/O 骑 mock 传输层/FakeClock;CI 真跑项如实标 manual。

| 文件 | 内容 | 对应 AC |
|---|---|---|
| `e2e_matrix_smoke.py/.log` | 多上游池 fixture 端到端矩阵:M1 轮换 / M2 摘除 / M3 未到期跳过 / M4 半开恢复 / M5 池熔断(零网络,传输层计数为证)/ M6 熔断解除 + E1 引擎级(YAML 真加载器 → DirectAPIEngine,A 死 B 活)+ C1 pool 未声明零影响对照 + C2 v0.2 字符串兼容 → **38 PASS,exit 0** | AC2/AC3/AC1(兼容面) |
| `pytest-proxy-suites.log` | `pytest tests/test_proxy_pool.py tests/test_proxy_transport.py -q` → **71 passed**;AC 关键具名测试逐项 PASS(未声明零影响 / doctor 逐上游×2 / registry 短路不清 hint / 熔断零网络) | AC2/AC3/AC4 |
| `ac1-migration-and-spec.log` | 既有套件 44 passed(33 基线 + 加载器新增);implement.md B6 列名迁移 4 项逐名 PASS | AC1 |
| `full-pytest.log` | 全量 `uv run --no-sync python -m pytest -q` → **3495 passed, 19 skipped, 0 failed(exit 0,66.74s)**;无预存红需豁免 | AC5 |

AC7(文档)与 AC6(真机)证据不在本目录:AC7 = docs/zh/schema.md:114-133、docs/en/schema.md:126-157(双语 pools 节 + 行为变化披露)、.trellis/spec/python/index.md:53-60 + `pytest tests/test_docs.py -q` → 92 passed(本会话跑);AC6 = [manual] 主人侧真机双上游,未跑。
