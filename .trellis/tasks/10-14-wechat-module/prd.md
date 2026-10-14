# 微信渠道模块化:对齐 TG 形态的解耦整理

## Goal(主人令 2026-10-14 晚)

微信渠道对标 TG 渠道,做成**稳定性的代码解耦模块**——TG 有 `src/myssia/telegram/` 自包含包,微信没有对等物,散乱现状重构费劲。

## 审计实证(现状病灶)

| 位置 | 现状 | 判定 |
|---|---|---|
| plugins/wechat-bridge/(桥组件 19 文件) | 自包含、独立发版、装机件 | ✅ 形态良好,不动 |
| src/myssia/wechat_local_sidecar.py、wechat_stats_sidecar.py | **顶层散件**两个 | ❌ 收进包 |
| src/myssia/push/weixin.py、weixin_local.py、wecom.py | 推送三分支散在 push/,与 telegram 包形态不对称 | ❌ 归位(留薄壳兼容) |
| desktop .../screens/messaging/wechat-*.tsx ×8+ | 微信屏族混在 messaging 大杂烩 | ❌ 归子域 messaging/wechat/ |
| src/myssia/schema.py 等公共件微信字段 | 挂点,暂不动(与 telegram 同款挂点) | ➖ 评估 |

## 目标形态

```
src/myssia/wechat/            # 与 telegram/ 平级
├── __init__.py               # 统一门面(消费方唯一入口)
├── sidecar.py                # ← wechat_local_sidecar.py
├── stats_sidecar.py          # ← wechat_stats_sidecar.py
├── push_local.py             # ← push/weixin_local.py(桥推送适配)
├── push_weixin.py            # ← push/weixin.py(保留薄壳 re-export 兼容)
└── push_wecom.py             # ← push/wecom.py(同)
desktop/.../messaging/wechat/ # 微信屏族子域(8+ 文件+测试)
```

## Requirements

- 兼容纪律:旧导入路径(`myssia.push.weixin_local` 等)留 re-export 薄壳,零破坏消费方;golden/契约测试全绿。
- 迁移=纯移动+薄壳,不顺手改逻辑(解耦归解耦,行为零变)。
- 桥组件(plugins/wechat-bridge)零改动。
- desktop 屏族移动须同步组件引用路径与测试导入,vitest 全绿。

## Acceptance Criteria

- [ ] AC1:src/myssia/wechat/ 包成立,五件归位,包内聚(包外零新散件)。
- [ ] AC2:旧导入路径全部兼容(re-export),全量 pytest+vitest 绿零回退。
- [ ] AC3:desktop 微信屏族归 messaging/wechat/ 子域,引用与测试同步。
- [ ] AC4:行为零变(纯移动判据:diff 仅路径与 import,逻辑行零改)。
- [ ] AC5:文档落位(README/相关 spec 的模块地图更新)+ 提交入库。
