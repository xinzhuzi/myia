# design v2:微信渠道模块化(10-14-wechat-module;grill R1 13 findings 全吸收)

**形态定位(勘误 R1-F2,诚实叙事)**:telegram 渠道现状=核心包 `src/myssia/telegram/` + **顶层** `engines/telegram.py`/`tg_web.py` + **顶层** `push/telegram*.py`(registry.py:169-180 注册的正是顶层件)——TG 的 engine/push 本也平铺。本任务采用**超越 TG 的彻底收拢形态**:微信七件全入 `src/myssia/wechat/`,engines/ 与 push/ 里的微信件清空。理由=主人令「各自自身的模块,否则乱成一锅粥」;TG 侧未来若同病可循此例。严格 TG 同形(仅收 sidecar 双件)为备选,主人可翻案。

## 1. 现状精确地图(R1 修正版;行数与引用 rg 实测)

### Python 侧(**七件**)

| 文件 | 行数 | 职责 | 被引用方(全量,实测) |
|---|---|---|---|
| `src/myssia/wechat_local_sidecar.py` | 479 | 本机桥 sidecar 协议面 | stats_sidecar、engines/wechat_local.py:142、**desktop/entry.py:434-436**、Rust keyprovider.rs(仅注释×5)、tests/desktop×3(local_handlers/local_media_handlers/stats_sidecar) |
| `src/myssia/wechat_stats_sidecar.py` | 399 | 统计报告 sidecar | desktop/entry.py、proxy_panel.py:**仅 docstring 注释引用,R1-F10 勘误(零运行时耦合,无需核实步)** |
| `src/myssia/push/weixin.py` | 476 | Hermes-Agent CLI 桥接通道 | **push/__init__.py:114(直 import+注册)**、**desktop/entry.py:433(probe_bridge)** |
| `src/myssia/push/weixin_local.py` | 489 | 本机通道(桥消费) | local_sidecar、engines/wechat_local.py、**engines/wechat_local_notify.py:59**、**push/__init__.py:115**、Rust(注释)、tests |
| `src/myssia/push/wecom.py` | 587 | 企业微信通道 | pipeline.py、**push/__init__.py:119** |
| `src/myssia/engines/wechat_local.py` | 1125 | 本机会话引擎 | **engines/registry.py:171(`"wechat_local": lambda: _load("wechat_local", "WechatLocalEngine")`;:180 `_load` 按 `myssia.engines.{name}` 派生路径——迁移断裂点,R1-F6)**、tests/engines/test_wechat_local_engine.py(46 处 monkeypatch setattr) |
| `src/myssia/engines/wechat_local_notify.py` | **540**(R1-F3 新入册) | 引擎 notify 通道件 | 引擎内部+push.weixin_local |

挂点(不动):`schema.py`、`store/`(与 telegram 同款)。cron/、docker/ 对七件**零引用**(实测)。

### Desktop 侧(R1-F4 勘误:**22 件**,含边界判据)

判据:**文件名或其直接依赖的 api 件专属于微信域**者迁;跨渠道共享件(platform-icons/messaging-screen/api.ts/types.ts)不迁、只改 import。

- messaging/:`wechat-{local,contacts,media,sns}.tsx(+各 .test.tsx)`、`wechat-{chat-export,contacts}-api.ts`、`wechat-chat-export-api.test.ts`、`wechat-stats-api.ts`、`wx-stats-panel.tsx(+.test.tsx)`
- feed/:`wechat-groupinfo-api.ts`、`wechat-group-export-api.ts`、`wx-groupinfo-panel.tsx(+.test.tsx)`
- settings/:`wechat-keyprovider-api.ts`、`weixin-account-card.tsx(+.test.tsx)`
- weixin-account/:`weixin-account-screen.tsx`

**TS 引用面(改 import 的完整对象,R1-F5)**:messaging-screen.tsx、messaging/api.ts、platform-icons(.test).tsx、platform-overview.tsx、wx-stats-panel×2、feed/api.ts、feed-screen(.test).tsx、lib/api/types.ts——P0.5.2 探针重生成核对后才动。

### 跨语言与打包(R1-F7 定论)

- Rust keyprovider.rs 五处引用(行 5/26/66/200/397)=纯注释,同步改名即可。
- **装机/发行免疫定论**(勘察实证):tauri.conf.json:86 为 `"../../src/myssia": "myssia-src/myssia"` **整目录拷贝**;PyInstaller 走 `collect_submodules('myssia')` 动态收集(myssia-core.spec:17)。**包内移动对二者免疫,装机包无需同步动作**;薄壳随树入包。

### `__file__` 依赖(R1-F8,唯一一处)

`wechat_stats_sidecar.py:193` `Path(__file__).resolve()` 向上找 `config/wechat-stats.yaml`——移入 `wechat/` 子目录后 parents 仍含仓库根,**行为不变**;P1 加显式探针验证(见 implement 1.4)。`push_local` 的 `DEFAULT_BRIDGE_BIN`=家目录串(非 __file__,安全)。

## 2. 目标架构与薄壳协议(R1-F1/F13 修正)

```
src/myssia/wechat/
├── __init__.py      # 门面:显式符号白名单 re-export(手工 __all__,不做 import* 合并——
│                    #   weixin/weixin_local 引入同名对象虽同体无害,F13 遮蔽取舍无判据,白名单免争)
├── sidecar.py       # ← wechat_local_sidecar.py
├── stats_sidecar.py # ← wechat_stats_sidecar.py
├── push_weixin.py   # ← push/weixin.py
├── push_local.py    # ← push/weixin_local.py
├── push_wecom.py    # ← push/wecom.py
├── engine.py        # ← engines/wechat_local.py
└── notify.py        # ← engines/wechat_local_notify.py
```

**薄壳协议(收窄语义)**:原路径留 `from myssia.wechat.xxx import *(# 兼容壳)`+显式透传公共名。**兼容面=仓外消费者**(脚本/未来外部);**仓内(含全部测试)一律改指新径**——monkeypatch 私有名(`wls._BASE`/`wx_engine` 46 处 setattr)打在壳上不生效(壳无下划线名、setattr 落壳副本),测试必须迁真模块,此为 P1 硬步骤非可选。

**注册面改动(白名单,非移动件)**:
1. `engines/registry.py:171` lambda → 指向 `myssia.wechat.engine`(:180 `_load` 的路径派生不适用于新位置,给 `_load` 加全路径变体或 lambda 直 import);
2. `push/__init__.py:114-119` 三通道 import 改新径(注册键名 `weixin-local` 等**不变**——外部配置面零影响);
3. `desktop/entry.py:433-436` 两处 import 改新径。

## 3. 迁移纪律(铁律,R1-F11 重述判据)

1. **移动件 diff 判据**:仅 import 行与模块 docstring 首行可变,逻辑行零改;
2. **外部件改动=白名单封闭集**:registry lambda、push/__init__ 三行、entry.py 两行、Rust 注释五处、desktop 父引用与测试 monkeypatch 目标(清单见 implement)——白名单外任何逻辑改动=返工;
3. 取证先行/修一处扫类照旧(错题集纪律)。

## 4. 风险与回滚

| 风险 | 缓解 |
|---|---|
| 测试 monkeypatch 迁移漏点→假绿 | P0.5 底账含测试全清单;迁移后对 4 个测试文件 grep 旧路径断言零残留 |
| registry `_load` 路径派生失配 | design §2 已点名改法;P1.6 单步验证(import myssia.wechat.engine 直载) |
| desktop 打包路径别名 | vitest+build 双关;tsconfig paths 如涉同步 |
| 并行会话在途(10-14-wechat-sendmsg-direct 桥件已脏) | 0.1 真跑 git status;脏文件与七件不相交方可进(桥件在 plugins/,不相交) |

回滚:五笔切分提交,单笔 revert;薄壳保证中途态可用。

## 5. 验证命令(每阶段全绿才进;R1 实测形态)

```bash
uv run --no-sync python -m pytest tests/ -q --tb=short
npm --prefix desktop/ui-src run test        # = vitest run(package.json 实测)
npm --prefix desktop/ui-src run build       # = tsc -b && vite build(实测)
cargo check --manifest-path desktop/src-tauri/Cargo.toml
uv run --no-sync python -c "from myssia.push.weixin_local import DEFAULT_BRIDGE_BIN; from myssia.engines.wechat_local import WechatLocalEngine; print('兼容壳 OK')"   # 壳+真径双通
uv run --no-sync python -c "from myssia.wechat.stats_sidecar import _resolve_config; print(_resolve_config())"   # __file__ 探针(F8,函数名以实码为准,P1 核对)
```
