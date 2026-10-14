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
| `engines/wechat_local.py` | 1125 | registry.py:171 lambda+:180 `_load` 派生(**断裂点**);**函数内 lazy:331/:514 → engines.wechat_local_notify(validate_options/fetch_notify)**;tests/engines/test_wechat_local_engine.py(85 行 setattr 全部打在 wx_engine,T3-10 勘误) |
| `engines/wechat_local_notify.py` | 540 | **engines/wechat_local:331/:514(lazy,双向环)**;**函数内 :99/:109 反向 lazy → engines.wechat_local(TITLE_MAX_CHARS/watermark_key)**;tests/engines/test_wechat_local_notify.py |

挂点不动:schema/store。cron/、docker/ 零引用(实测)。**同包引用规范:一律绝对径**(`from myssia.wechat.notify import ...`,与仓库现行绝对 import 惯例一致,不用相对径)。

### 测试面账实(R2-F1,完整清单)

7 个文件含旧径 import/monkeypatch:`tests/desktop/test_wechat_local_handlers.py`、`test_wechat_local_media_handlers.py`、`test_wechat_stats_sidecar.py`、`tests/engines/test_wechat_local_engine.py(85 行 setattr 全部打在 wx_engine,T3-10 勘误)`(**85 行 setattr,其中 58 处打在 wx_engine 模块**)、`tests/engines/test_wechat_local_notify.py`(14 处 setattr)、`tests/push/test_messaging_weixin_local.py`、`test_messaging_weixin_bridge.py`、`test_messaging_wecom.py`、`test_messaging_pipeline.py`(9 文件,以 P0.6 实测贴档为最终账)。

### Desktop(R2-F8 修订:**分域方案**,只治真乱处)

- **迁**:`screens/messaging/` 内微信件 14 件(`wechat-{local,contacts,media,sns}.tsx+test`、`wechat-{chat-export,contacts}-api.ts+export.test`、`wechat-stats-api.ts`、`wx-stats-panel.tsx+test`)→ `messaging/wechat/` 子域;
- **不动**:feed/ 4 件(wechat-groupinfo/export-api、wx-groupinfo-panel×2,本就与 feed 同域共置)、settings/ 3 件、weixin-account/ 1 件——**零迁移零引用变更**,避免跨域反向 import(AC 判据同步收窄);
- TS 父引用面(**T3-13 实测正资产:仓外 importer 实仅 messaging-screen.tsx:62 一行**;platform-icons/platform-overview/types.ts 等皆字符串提及零 import,wx-stats-panel×2 属迁移主体自身)——仍以 0.5.2 三探针并集复核为准,预期改动面=一行+子域内相对路径。

### 跨语言与打包

- Rust keyprovider.rs 五处注释(5/26/66/200/397)同步改名;零运行时引用。
- 打包免疫定论:tauri.conf.json:86 的 `"../../src/myssia": "myssia-src/myssia"` 整目录拷贝(T3-11 注:myssia-core.spec 已退役勿引;PyInstaller 链同理 collect_submodules 动态收集免疫)→ 包内移动免疫,装机无需同步。
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

**注册面与外部件改动(白名单封闭集,R3 修订)**:
- registry.py:171(**裁决 T3-4:lambda 直载**——lambda 内 import_module("myssia.wechat.engine") 后取类属性,顶部补 import;**零触 `_load`**,其他引擎零影响);
- push/__init__.py:114(wecom)/115(weixin)/119(weixin_local)三 import;
- desktop/entry.py **三处**(433/434-436/**4815**,T3-9 行号勘误);
- `src/myssia/proxy_panel.py:5` docstring 的 :mod: 旧点径(T3-2,注释一处);
- desktop/src-tauri/src/**wechat_keyprovider.rs**(T3-8 文件名勘误)五处注释;
- desktop 父引用(**实测面=T3-13:messaging-screen.tsx:62 一行**,以 0.5.2 并集复核为准);测试 monkeypatch 目标(0.6 实测账)。

## 3. 迁移纪律(铁律,R2-F2 修订判据)

1. **移动件 diff 判据**(T3-1 修订,三类可变行封闭集):①模块 docstring 首行;②**一切 import 语句**(顶层+函数内 lazy:engine:331/:514、notify:99/:109、stats_sidecar:151 恰五处;notify:59 为顶层单列);③**移动件内部 docstring/注释中的旧点径字符串**(8 处已点名:engine:12/:13/:162、notify:3、push_local(原 weixin_local):3/:153、stats_sidecar:8、sidecar(原 local_sidecar):14——残留断言要求清零,判据须放行此改)。其余逻辑行零改;同包互引一律绝对新径。
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
# 仓内零残留(P1 终验;T3-3/5/6/12 修订:补 build-pyi 排除、补 from-import 形态、豁免=七薄壳本体、退出码语义摆正):
! rg -n "myssia\.push\.weixin_local|myssia\.push\.weixin\b|myssia\.push\.wecom\b|myssia\.engines\.wechat_local|myssia\.wechat_local_sidecar|myssia\.wechat_stats_sidecar|from myssia import wechat_local_sidecar|from myssia import wechat_stats_sidecar" \
    src desktop/src desktop/ui-src/src tests \
    --glob '!__pycache__' --glob '!build-pyi' \
    | rg -v "^src/myssia/(push/weixin(_local)?\.py|push/wecom\.py|wechat_local_sidecar\.py|wechat_stats_sidecar\.py|engines/wechat_local(_notify)?\.py):"
# 语义:管道有输出(残留)则整条非零=失败;干净则成功(前置 ! 摆正 T3-6)。豁免=七薄壳本体行号前缀,精确到文件,无误豁免(T3-12 修正)。
```
