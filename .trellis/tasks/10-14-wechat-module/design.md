# design:微信渠道模块化(10-14-wechat-module)

参照系:`src/myssia/telegram/`(自包含包,含 serve/web_line/telethon_line/events/filter/offsets/web_backup;外界挂点仅 store/schema/cron-summary 等少数)。

## 1. 现状精确地图(2026-10-14 勘察实证)

### Python 侧(六件 + 两个挂点)

| 文件 | 行数 | 职责 | 被引用方(实测 rg) |
|---|---|---|---|
| `src/myssia/wechat_local_sidecar.py` | 479 | 本机桥 sidecar 协议面(10-11 F2) | stats_sidecar、engines/wechat_local、desktop Rust(仅注释)、tests/desktop×2 |
| `src/myssia/wechat_stats_sidecar.py` | 399 | 统计报告 sidecar(10-14 stats) | desktop/entry.py、**proxy_panel.py(意外耦合,迁移时核实)** |
| `src/myssia/push/weixin.py` | 476 | Hermes-Agent CLI 桥接通道 | push 注册面 |
| `src/myssia/push/weixin_local.py` | 489 | 本机通道(桥消费方,F1/G7) | local_sidecar、engines/wechat_local、Rust(注释)、tests |
| `src/myssia/push/wecom.py` | 587 | 企业微信通道(gettoken+webhook) | pipeline.py |
| `src/myssia/engines/wechat_local.py` | **1125** | 本机会话引擎(engine:wechat_local;10-12 feed-channel) | 引擎注册面 |

挂点(不动):`schema.py`(微信字段)、`store/`(与 telegram 同款挂点形态)。

### Desktop 侧(12 文件,全在 screens/messaging/ 平铺)

`wechat-{local,contacts,media,sns}.tsx(+.test.tsx)`、`wechat-{chat-export,contacts,stats}-api.ts(+export 的 .test.ts)`——与 messaging 大杂烩混居。

### 跨语言引用(勘察定级)

`desktop/src-tauri/src/wechat_keyprovider.rs` 对 `weixin_local`/`wechat_local_sidecar` 的引用**全部为文档注释**(行 5/26/66/200/397,对齐口径说明,无运行时 `-m` 模块名串)。→ 迁移后**注释同步改名**(文档一致性项,零功能风险);sidecar 拉起走 desktop/entry.py(python import)。

## 2. 目标架构

```
src/myssia/wechat/                 # 与 telegram/ 平级同形
├── __init__.py                    # 门面:消费方唯一入口(re-export 六件的公共符号+__all__)
├── sidecar.py                     # ← wechat_local_sidecar.py(纯移动)
├── stats_sidecar.py               # ← wechat_stats_sidecar.py
├── push_weixin.py                 # ← push/weixin.py
├── push_local.py                  # ← push/weixin_local.py
├── push_wecom.py                  # ← push/wecom.py
└── engine.py                      # ← engines/wechat_local.py
```

- **薄壳兼容层**(零破坏):原路径文件改为 `from myssia.wechat.xxx import *  # 兼容壳(10-14-wechat-module)` + 显式 `__all__` 透传;`myssia.push.weixin_local` 等**旧 import 路径永久可用的稳定 API 面**(与 telegram 演进同策略)。
- **engines/ 与 push/ 的注册面**:注册处(引擎注册/pipeline 渠道表/directory)改指新路径,薄壳保底旧引用。
- **desktop 子域**:`screens/messaging/wechat/` 目录收 12 件;组件内相对导入随之改;messaging-screen.tsx 等父级引用路径同步。
- Rust 注释同步:keyprovider.rs 五处注释的文件名口径更新。

## 3. 迁移纪律(铁律)

1. **纯移动零逻辑**:diff 判据=除 import 行/模块 docstring 首行外逻辑行零改;夹带逻辑改=返工。
2. **取证先行**(错题集纪律):每阶段动手前先跑该阶段涉及文件的基线测试,记录绿;移动后同套测试再跑,对照。
3. **修一处扫类**:改任一 import 时,rg 全库扫该符号的全部引用点一次清点(防漏 desktop 测试/cron 侧)。

## 4. 风险与回滚

| 风险 | 缓解 |
|---|---|
| push 渠道注册对**模块路径字符串**的反射/配置引用(如 channel key→module map) | P0 探针步骤:rg 渠道发现机制(directory/注册表),清单化后再动 |
| desktop 打包对屏族路径的 glob/别名引用(vite tsconfig paths) | 移动后跑 tsc+build+vitest 三关 |
| proxy_panel→stats_sidecar 意外耦合断 | 薄壳兜底;若 proxy_panel 语义上不该依赖微信,单独立档(不在本任务夹带) |
| 并行会话在途改动同文件 | 动手前 git status 核对该六件+12 件干净;脏则等波/协调 |

回滚:全部为 add+薄壳形态,`git revert` 单笔即回;薄壳层保证中途态也可用。

## 5. 验证命令(每阶段必跑,全绿才进下一阶段)

```bash
uv run --no-sync python -m pytest tests/ -q --tb=short          # 全量 python(基线对照)
npm --prefix desktop/ui-src run test 2>/dev/null || npm --prefix desktop/ui-src test -- --run   # vitest
npm --prefix desktop/ui-src run build                            # tsc+vite
cargo check --manifest-path desktop/src-tauri/Cargo.toml 2>&1 | tail -3   # Rust 注释改动零破坏
# 兼容面探针(薄壳有效性):
uv run --no-sync python -c "from myssia.push.weixin_local import DEFAULT_BRIDGE_BIN; from myssia.wechat_local_sidecar import *; print('兼容壳 OK')"
```

## 6. 依赖图(执行顺序依据)

```
P0 python 包归位(sidecar/stats/push×3 → engine,先叶后干)
P1 desktop 子域(12 件+父引用)
P2 门面 __init__ + Rust 注释 + 文档(README 模块地图/spec)
```
