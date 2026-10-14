# design v3:微信渠道模块化(R1 13+R2 12 findings 全吸收)

**形态定位(如实)**:TG 现状=核心包 telegram/ + engine/push 平铺顶层。本任务采**超越 TG 的彻底收拢**:微信**七件**全入 `src/myssia/wechat/`,engines/ 与 push/ 的微信件清空(留薄壳)。依据=主人「各自自身的模块」意图;TG 侧未来同病可循此例。严格 TG 同形(仅收 sidecar 双件)为备选,主人可翻案。

## 1. 现状精确地图(R2 修正;引用 rg 实测,行号以 P0 底账贴档为准)

### Python 七件

| 文件 | 行数 | 被引用方(全量) |
|---|---|---|
| `wechat_local_sidecar.py` | 479 | stats_sidecar(**含函数内 :151 lazy `_BASE`**)、engines/wechat_local:142、entry.py:434-436、Rust 注释×5、tests/desktop×3 |
| `wechat_stats_sidecar.py` | 399 | entry.py(:434-436 + **:4814 函数内 lazy handle_wechat_stats,共三处**)、proxy_panel(仅 docstring,零运行时) |
| `push/weixin.py` | 476 | **push/__init__.py:115**、entry.py:433、tests/push/test_messaging_weixin_bridge.py |
| `push/weixin_local.py` | 489 | local_sidecar、engines/wechat_local、**engines/wechat_local_notify:59**、**push/__init__.py:119**、Rust 注释、tests/push/test_messaging_weixin_local.py |
| `push/wecom.py` | 587 | pipeline.py、**push/__init__.py:114**、tests/push/test_messaging_wecom.py、test_messaging_pipeline.py |
| `engines/wechat_local.py` | 1125 | registry.py:171 lambda+:180 `_load` 派生(**断裂点**);**函数内 lazy:331/:514 → engines.wechat_local_notify(validate_options/fetch_notify)**;tests/engines/test_wechat_local_engine.py |
| `engines/wechat_local_notify.py` | 540 | **engines/wechat_local:331/:514(lazy,双向环)**;**函数内 :99/:109 反向 lazy → engines.wechat_local(TITLE_MAX_CHARS/watermark_key)**;tests/engines/test_wechat_local_notify.py |

挂点不动:schema/store。cron/、docker/ 零引用(实测)。**同包引用规范:一律绝对径**(`from myssia.wechat.notify import ...`,与仓库现行绝对 import 惯例一致,不用相对径)。

### 测试面账实(R2-F1,完整清单)

7 个文件含旧径 import/monkeypatch:`tests/desktop/test_wechat_local_handlers.py`、`test_wechat_local_media_handlers.py`、`test_wechat_stats_sidecar.py`、`tests/engines/test_wechat_local_engine.py`(**85 行 setattr,其中 58 处打在 wx_engine 模块**)、`tests/engines/test_wechat_local_notify.py`(14 处 setattr)、`tests/push/test_messaging_weixin_local.py`、`test_messaging_weixin_bridge.py`、`test_messaging_wecom.py`、`test_messaging_pipeline.py`(9 文件,以 P0.6 实测贴档为最终账)。

### Desktop(R2-F8 修订:**分域方案**,只治真乱处)

- **迁**:`screens/messaging/` 内微信件 14 件(`wechat-{local,contacts,media,sns}.tsx+test`、`wechat-{chat-export,contacts}-api.ts+export.test`、`wechat-stats-api.ts`、`wx-stats-panel.tsx+test`)→ `messaging/wechat/` 子域;
- **不动**:feed/ 4 件(wechat-groupinfo/export-api、wx-groupinfo-panel×2,本就与 feed 同域共置)、settings/ 3 件、weixin-account/ 1 件——**零迁移零引用变更**,避免跨域反向 import(AC 判据同步收窄);
- TS 父引用面(messaging 14 件迁动的完整对象):messaging-screen.tsx、messaging/api.ts、platform-icons(.test).tsx、platform-overview.tsx、wx-stats-panel×2、lib/api/types.ts(**App.tsx/feed 系列因分域方案解除引用变更**)——P0.5.2 三探针并集对账后为准。

### 跨语言与打包

- Rust keyprovider.rs 五处注释(5/26/66/200/397)同步改名;零运行时引用。
- 打包免疫定论:tauri.conf.json:86 整目录拷贝 + PyInstaller collect_submodules(spec:17)→ 包内移动免疫,装机无需同步。
- `__file__` 唯一处:stats_sidecar:193 向上找 `config/wechat-stats.yaml`(仓库根无此文件,常态走数据根回落);移入 wechat/ 后 parents 仍含仓库根,行为不变;P1 探针验证。

## 2. 目标架构与薄壳协议

```
src/myssia/wechat/
├── __init__.py        # 门面:显式符号白名单+手工 __all__(不做 import* 合并)
├── sidecar.py         # ← wechat_local_sidecar.py
├── stats_sidecar.py   # ← wechat_stats_sidecar.py
├── push_weixin.py     # ← push/weixin.py
├── push_local.py      # ← push/weixin_local.py
├── push_wecom.py      # ← push/wecom.py
├── engine.py          # ← engines/wechat_local.py
└── notify.py          # ← engines/wechat_local_notify.py
```

薄壳=原路径 `from myssia.wechat.xxx import *` + 公共名显式透传;**兼容面仅仓外**;仓内(全部源码与测试)一律新径。

**注册面与外部件改动(白名单封闭集,R2 修订)**:registry.py:171 lambda 改指 `myssia.wechat.engine`;push/__init__.py:114(wecom)/115(weixin)/119(weixin_local)三 import(R2-F5 行号勘误);entry.py **三处**(433/434-436/4814);Rust 注释×5;desktop 父引用;测试 monkeypatch 目标(9 文件)。

## 3. 迁移纪律(铁律,R2-F2 修订判据)

1. **移动件 diff 判据**:可变行=模块 docstring 首行 + **一切 import 语句(含函数体内 lazy import 行,五处已点名:engine:331/:514、notify:59/:99/:109、stats_sidecar:151)**;其余逻辑行零改。同包互引改绝对新径。
2. 外部件改动=§2 白名单封闭集,白名单外零改。
3. **仓内零残留铁律**:七条旧径(`myssia.push.weixin_local`、`myssia.push.weixin\b`、`myssia.push.wecom`、`myssia.engines.wechat_local`、`myssia.engines.wechat_local_notify`、`myssia.wechat_local_sidecar`、`myssia.wechat_stats_sidecar`)在 src/desktop/tests 全树 rg 断言零命中(七个薄壳文件自身的路径串除外——其**内容** import 的是新径,不命中)。

## 4. 风险与回滚

| 风险 | 缓解 |
|---|---|
| 测试漏迁→假绿 | P0.6 账实贴档(9 文件/85 setattr);1.9 用 §3 七旧径全量断言(不是子集) |
| engine⇄notify 双向环改错 | 五处 lazy import 逐点列在 1.7/1.8 步内,逐处改逐跑该件测试 |
| registry `_load` 失配 | §2 已点名;1.8 直载验证 |
| 并行在途 | 0.1 真跑 git status(当前实况:脏件为 sendmsg-direct 任务档,与七件零相交;以当时实测为准) |

回滚:五笔切分,单笔 revert;薄壳保证中途态可用。

## 5. 验证命令(每阶段全绿才进)

```bash
uv run --no-sync python -m pytest tests/ -q --tb=short
npm --prefix desktop/ui-src run test        # vitest run
npm --prefix desktop/ui-src run build       # tsc -b && vite build
cargo check --manifest-path desktop/src-tauri/Cargo.toml
# 兼容壳+真径双通:
uv run --no-sync python -c "from myssia.push.weixin_local import DEFAULT_BRIDGE_BIN; from myssia.wechat.push_local import DEFAULT_BRIDGE_BIN as B2; assert DEFAULT_BRIDGE_BIN == B2; print('壳 OK')"
# __file__ 探针(R2-F12 勘误:实码函数 config_path,:180;仓库根无 yaml,断言回落行为不抛):
uv run --no-sync python -c "from myssia.wechat import stats_sidecar as s; p = s.config_path(); print('config_path →', p); assert p is None or 'wechat-stats' in str(p)"
# 仓内零残留(P1 终验):
rg -n "myssia\.push\.weixin_local|myssia\.push\.weixin\b|myssia\.push\.wecom|myssia\.engines\.wechat_local|myssia\.wechat_local_sidecar|myssia\.wechat_stats_sidecar" src desktop tests --glob '!__pycache__' --glob '!target' | rg -v "^src/myssia/(push/weixin(_local)?|wecom|wechat_local_sidecar|wechat_stats_sidecar|engines/wechat_local(_notify)?)\.py:" ; echo "残留=$?"
```
