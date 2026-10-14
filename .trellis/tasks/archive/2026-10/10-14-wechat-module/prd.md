# 微信渠道模块化:对齐 TG 形态的解耦整理

## Goal(主人令 2026-10-14 晚)

微信渠道做成**稳定性的代码解耦模块**(主人:「类似 TG 渠道,都需要有各自自身的模块,否则乱成一锅粥,重构费劲」)。

**形态定位(grill R1-F2 勘误,如实)**:TG 现状=核心包 telegram/ + engine/push 平铺顶层——本任务采用**超越 TG 的彻底收拢**(微信七件全入包,engines/push 微信件清空),依据主人「各自自身模块」意图;TG 侧未来同病可循此例。备选=严格 TG 同形(仅收 sidecar),主人可翻案。

## 审计实证(现状病灶)

| 位置 | 现状 | 判定 |
|---|---|---|
| plugins/wechat-bridge/(桥组件 19 文件) | 自包含、独立发版、装机件 | ✅ 形态良好,不动 |
| src/myssia/wechat_local_sidecar.py、wechat_stats_sidecar.py | **顶层散件**两个 | ❌ 收进包 |
| src/myssia/push/weixin.py、weixin_local.py、wecom.py | 推送三分支散在 push/,与 telegram 包形态不对称 | ❌ 归位(留薄壳兼容) |
| desktop .../screens/messaging/wechat-*.tsx ×8+ | 微信屏族混在 messaging 大杂烩 | ❌ 归子域 messaging/wechat/ |
| `src/myssia/engines/wechat_local.py`(**1125 行,最大件**) | 本机会话引擎,顶层 engines/ 平铺;注册=registry.py:171 lambda+:180 `_load` 路径派生(**迁移断裂点,改法已入 design §2**) | ❌ 归位为 wechat/engine.py |
| `src/myssia/engines/wechat_local_notify.py`(**540 行,grill R1-F3 补册第七件**) | 引擎 notify 通道件,:59 引 push.weixin_local | ❌ 归位为 wechat/notify.py |
| desktop/src-tauri/keyprovider.rs 五处**注释**引用 | 勘察定级:纯文档注释,无运行时模块名串 | ➖ 注释同步项 |
| proxy_panel.py → stats_sidecar 意外耦合 | 语义存疑 | ➖ 迁移时核实,不夹带重构 |
| src/myssia/schema.py 等公共件微信字段 | 挂点,暂不动(与 telegram 同款挂点) | ➖ 评估 |

desktop 屏族(R1-F4 勘误 22 件;R2-F8 分域修订:**仅 messaging 14 件迁**,其余 8 件已同域共置不动,边界判据=「文件名或其直接依赖 api 件专属于微信域」):messaging 内 14(含 wx-stats-panel×2)+feed 内 4(wechat-groupinfo/export-api、wx-groupinfo-panel×2)+settings 内 3(wechat-keyprovider-api、weixin-account-card×2)+weixin-account-screen;完整清单与 TS 父引用面见 design §1(P0.5.2 实测对账后为准)。

**打包面定论(grill R1-F7)**:tauri 整目录拷贝+PyInstaller collect_submodules 动态收集,包内移动**免疫**,装机无需同步。**测试兼容定论(R1-F1)**:薄壳只保仓外;仓内测试(4 文件 46+ monkeypatch)必须迁新径,壳上打补丁不生效。

## 目标形态(R2 修订:七件全录+desktop 分域)

```
src/myssia/wechat/            # 与 telegram/ 平级;超越 TG 的收拢形态
├── __init__.py               # 门面(显式白名单,不做 import* 合并)
├── sidecar.py                # ← wechat_local_sidecar.py
├── stats_sidecar.py          # ← wechat_stats_sidecar.py
├── push_weixin.py            # ← push/weixin.py
├── push_local.py             # ← push/weixin_local.py
├── push_wecom.py             # ← push/wecom.py
├── engine.py                 # ← engines/wechat_local.py
└── notify.py                 # ← engines/wechat_local_notify.py
```

- python 旧路径留薄壳(兼容面=仓外);**仓内(含 9 个测试文件/85 行 monkeypatch)一律迁新径**——壳上打补丁不生效,测试迁真模块是硬步骤。
- desktop **分域方案**(R2-F8 修订):只有 messaging/ 14 件真平铺混乱→迁 `messaging/wechat/`;feed 4/settings 3/weixin-account 1 已同域共置**零迁移零变更**。

## Requirements

- 兼容纪律:旧导入路径(`myssia.push.weixin_local` 等)留 re-export 薄壳,零破坏消费方;golden/契约测试全绿。
- 迁移=纯移动+薄壳,不顺手改逻辑(解耦归解耦,行为零变)。
- 桥组件(plugins/wechat-bridge)零改动。
- desktop 屏族移动须同步组件引用路径与测试导入,vitest 全绿。

## Acceptance Criteria

- [x] AC1:src/myssia/wechat/ 包成立,**七件归位**,包内聚(包外零新微信散件;薄壳七件为兼容面豁免)。
- [x] AC2:旧导入路径全部兼容(re-export),全量 pytest+vitest 绿零回退。
- [x] AC3:messaging 14 件归 messaging/wechat/ 子域,引用与测试同步;feed/settings/weixin-account 分域豁免(零变更)。
- [x] AC4(v2 判据,R1-F11):**移动件** diff 仅 import/docstring 行;**外部件改动=白名单封闭集**(registry lambda/push __init__×3/entry.py×2/Rust 注释×5/desktop 父引用/测试 monkeypatch 目标,清单 implement),白名单外零改。
- [x] AC5:文档落位(README/相关 spec 的模块地图更新)+ 提交入库。


## 交付实录(10-14 晚,P0-P3 五笔提交)

- P1:C1 push 三件/C2 sidecar 双件(+回环破除:wechat/__init__ 暖导入,环迁移前即潜伏)/C3 notify+engine+registry 直载;零残留断言抓漏三处清零;全量 6208 绿。
- P2:14 件归 messaging/wechat/(+6 件同目录 ./api 断裂修复——T3-13 的「一行实改面」判断对父引用成立,同目录引用是移动固有修复);vitest 942 绿+build 绿。
- P3:门面十符号+Rust 注释五处(cargo check 绿)+README 模块地图。
- 终验:pytest 6207 绿+1 红=并行线 macos_notify 在途波动(非本迁移范围,src 干净归属核实);四关中三关绿,该红留并行线自愈。
- 打包:just build-desktop(tauri 全链)随后执行。
