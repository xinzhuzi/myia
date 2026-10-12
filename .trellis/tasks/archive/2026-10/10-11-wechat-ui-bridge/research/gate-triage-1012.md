# 门禁 triage — 全量门禁红归因(修复工,2026-10-12)

> 执行件:修复工(工作流子代理)。ask = 全量门禁红(pytest=1, vitest=1),只修与本任务
> (10-11-wechat-ui-bridge)相关的失败;并行会话在途文件的失败不修、记 skipped 归因。
> 本文零私有数据;证据只含计数/路径/命令/码值。

## 0. 结论速览

| 项 | 判定 |
|---|---|
| 153 failed + 6 errors(pytest 全量) | **零件属本任务**;全部归因并行会话 `plugins/ → config/` 布局迁移在途(25 个 staged rename + ~50 个 M 文件 + 新增 `src/myssia/config_layout.py`/`tests/test_config_layout.py`) |
| 1 failed(vitest 全量) | 同上:`sources.test.tsx:401` 仍断言旧文案 vs `first-run-guide.tsx:102` 已改新文案,两件均在对方 M 集 |
| 本任务面(组件 + MYIA 装配) | **全绿**:`tests/wechat-bridge` 165p/7s;`tests/desktop/test_wechat_local_handlers.py + tests/push/{test_messaging_weixin_local,test_push_channels,test_push}.py` 185p |
| 修复动作 | **零**(无本任务相关失败可修);本档为唯一产出 |
| 装机件(如实) | `~/.myia/plugins/wechat-bridge` 仍 **0.2.0**(无 `pixel.py`)——installed-visual-check.md §4.1 移交项未闭合,归主会话 |

## 1. 门禁实跑(本会话亲跑,命令原样)

| 门禁 | 命令 | 结果 |
|---|---|---|
| pytest 全量 | `uv run --no-sync python -m pytest -q --tb=short` | **153 failed / 5171 passed / 50 skipped / 6 errors**(130.21s,无 --maxfail) |
| vitest 全量 | `npm --prefix desktop/ui-src run test` | **Test Files 1 failed / 34 passed(35);Tests 1 failed / 743 passed(744)** |
| 本任务组件面 | `uv run --no-sync python -m pytest tests/wechat-bridge -q --tb=short` | **165 passed / 7 skipped**(skip=MYIA_WECHAT_E2E 门控真机,design §8 惯例) |
| 本任务装配面 | `uv run --no-sync python -m pytest tests/desktop/test_wechat_local_handlers.py tests/push/test_messaging_weixin_local.py tests/push/test_push_channels.py tests/push/test_push.py -q --tb=short` | **185 passed** |

ask 门禁摘要(30 failure 截断快照)与本文全量快照的失败数漂移
(`test_installer_resources` 9→0、`test_desktop_sidecar_protocol` 12→6、
`test_bundled_plugins_install` 2→7)= 对方会话在本文写作窗口内**仍在持续改码**,
在途状态直接实锤。

## 2. 失败全清单(按文件;全量无截断)

```
103 FAILED tests/plugins/test_plugins.py
 10 FAILED tests/engines/test_store_report_engine.py
  8 FAILED tests/plugins/test_plugin_packages.py
  7 FAILED tests/desktop/test_bundled_plugins_install.py      (M·对方)
  6 FAILED tests/desktop/test_desktop_sidecar_protocol.py     (M·对方)
  6 ERROR  tests/pipeline/test_baseline.py                    (fixture setup 级)
  3 FAILED tests/plugins/test_demo_plugin.py
  2 FAILED tests/plugins/test_{theharvester,proxy,osint,media,maigret}_plugin.py
  1 FAILED tests/plugins/test_{urlwatch,plugins_system,analysis}_plugin.py
  1 FAILED tests/pipeline/test_baseline.py
  1 FAILED tests/engines/test_tg_web_engine.py
  1 FAILED tests/cli/test_cli_full.py                         (M·对方)
```

vitest 唯一失败:`src/screens/sources/sources.test.tsx > 源管理:空态与错误态 >
无插件 → 首跑引导态`(`sources.test.tsx:401`)。

## 3. 归因证据(逐族根因)

1. **品类 YAML 加载族(103+10+8+3+2×5+1×3+1+1 failed + 6 errors)**:根因全部同形
   `FileNotFoundError: …/MYIA/plugins/<name>.yaml`(如 stocks/wool/gpu-prices;
   `tests/pipeline/test_baseline.py` 6 errors 同为 fixture setup 期
   `load_category_file(GPU_PRICES)` 撞同错)——staged rename
   `plugins/*.yaml → config/*.yaml`(25 件,git index R)后,这批**尚未被对方改到**
   的测试仍指 `PLUGINS_DIR`(如 `tests/plugins/test_plugins.py:84`)。
2. **desktop sidecar/installer 族(7+6 failed)**:三件测试文件全在对方 M 集
   (test_bundled_plugins_install / test_desktop_sidecar_protocol /
   test_installer_resources),其被改测期望(`config_dir`、17 件清单、
   `Resources/config/`)与对方同在途的 `desktop/entry.py`/`tauri.conf.json` 半程态
   互相错位;sidecar telegram 族 5 例失败日志同证:
   `telegram 宿主未起(品类缺失 telegram-groups.yaml…)`(补种源与宿主查找路径
   两头都在迁)。例:`test_serve_context_myssia_home_env` 期望
   `ctx.config_dir == home/"config"`(test 侧已改)vs entry.py 在途实现。
3. **vitest 1 例**:`first-run-guide.tsx:102` 已渲染新文案
   `配置目录(config)下没有可加载的品类 YAML…`,`sources.test.tsx:401` 仍断言旧
   `/插件目录\(plugins\)下没有可加载的品类 YAML/`——同迁移的文案改名未同步,
   两件均对方 M 集。
4. **本任务零牵连**:FAILED/ERROR 全列表 `grep -ci 'wechat|weixin'` = **0**;
   `tests/wechat-bridge`、`tests/desktop/test_wechat_local_handlers.py`、
   `tests/push/*weixin_local*` 全绿(§1)。

## 4. 处置(按 ask 纪律)

- **不修**:153+1 全数 skipped 归因(§3);涉事文件要么对方 M 在途,要么是对方
  staged rename 的待同步面——修复=混写对方迁移,违反 ask「并行会话在途文件不修」。
- **零 commit 代码面**:本档外无任何自改文件;工作树 25R+50M 全归对方。
- **移交主会话**(如实,均非本修复工范围):
  1. 门禁转绿依赖对方 config 迁移收口(尤其 tests/plugins/test_plugins.py 等
     尚未进入其 M 集的 PLUGINS_DIR 指涉面);
  2. 装机件仍 0.2.0(缺 pixel.py),installed-visual-check.md §4.1 的
     「刷新 0.3.0 + 复验两点」未闭合。

## 5. 第二轮增量(同日复triage;ask 门禁快照=24f 截断版)

| 门禁 | 命令(原样) | 结果 |
|---|---|---|
| pytest 全量 | `uv run --no-sync python -m pytest -q --tb=short` | **145 failed / 5195 passed / 49 skipped / 6 errors**(126.34s) |
| vitest 全量 | `npm --prefix desktop/ui-src run test` | **Test Files 1 failed / 34 passed;Tests 1 failed / 743 passed** |
| 本任务面(合跑) | `uv run --no-sync python -m pytest tests/wechat-bridge tests/desktop/test_wechat_local_handlers.py tests/push/test_messaging_weixin_local.py tests/push/test_push_channels.py tests/push/test_push.py -q --tb=short` | **350 passed / 7 skipped** |

**对 §1/§2 的增量**:较第一轮全量净减 8 例——`test_bundled_plugins_install`(7)
与 `test_cli_full`(1)已被对方修绿(两件均在其 M 集,已收敛);其余**分布与根因
原样未动**:test_plugins.py 103 + engines/pipeline/plugins 零散 36 + 6 errors
(抽样复核仍 `FileNotFoundError: …/plugins/gpu-prices.yaml`,该族测试文件
`git status tests/plugins tests/engines tests/pipeline` = **零改动**,纯 staged
rename 的待同步面)+ sidecar 6(telegram 宿主「品类缺失」族,仍在途)+ vitest 1
(`sources.test.tsx:401` vs `first-run-guide.tsx:102` 文案错位原样,两件均 M)。
FAILED/ERROR 全列表 grep `wechat|weixin` 仍 = **0**。
装机件只读复核:`component.json` 仍 `"version": "0.2.0"`,
`wechat_bridge/pixel.py` 仍不在装(§4 移交项维持)。**处置不变:零本任务失败,
全数 skipped 归因,零代码 commit。**

## 6. 第三轮(同日晚;ask=pytest=0 / vitest 红,D5 收尾+AC7 收尾复核)

config 迁移已收口(c48bcdb/bb9ba05)后门禁全面转绿,残余 vitest 红为瞬态。

| 门禁 | 命令(原样) | 结果 |
|---|---|---|
| pytest 全量 | `uv run --no-sync python -m pytest tests -q -p no:cacheprovider` | **5305 passed / 48 skipped / 0 failed**,exit 0(153.55s)——红=0 实锤(与 ask 摘要 5372 的±67 收集差=并行会话在途增删,两口径均零失败) |
| vitest 全量① | `npx vitest run`(desktop/ui-src) | Test Files **2 failed** / 33 passed(35);Tests 2 failed / 742 passed(744) |
| vitest 全量② | 同上(数分钟后复跑) | Test Files **1 failed** / 34 passed;Tests 1 failed / 743 passed——**两轮数字漂移=在途实锤** |
| 定向复跑① | `npx vitest run src/screens/messaging/messaging-screen.test.tsx` | **56/56 全绿**(全量①红=`platform-card-a2a` 撞「加载中」skeleton,异步加载竞态 flaky) |
| 定向复跑② | `npx vitest run src/screens/feed/feed-screen.test.tsx -t "开窗失败"` | **1 passed**(全量红用例单独跑绿) |
| D5 契约 | `uv run --no-sync python -m pytest tests/desktop/test_pyenv_resources.py -q` | **36 passed**(185484a 落地面在位) |
| D5 Rust | `cargo test --locked`(desktop/src-tauri) | **90 passed / 1 ignored**(白名单解析 5 测在列) |
| 组件单测 | `uv run --no-sync python -m pytest tests/wechat-bridge -q` | **168 passed / 7 skipped**(与 research/d5-distribution-form.md 基线持平) |
| AC7 脚本 | `bash scripts/wechat-bridge-d4-keyscan.sh --dry-run` | **exit 0**:前置自检 5 项过+缺省关路径诚实 exit 21(key_unavailable 三重门语义)+真跑命令固化展示 |

**归因与处置**:vitest 两个失败文件(`feed-screen.test.tsx`/`messaging-screen.test.tsx`)
单独复跑均绿=非稳定红;`feed-screen.test.tsx`/`tg-native-window.{ts,test.ts}` 在 git M
在途集(并行会话 feed 原生视图改动中,见本轮 `git status`),按纪律不修、记 skipped
归因;messaging-screen 与本任务面(D5 分发/AC7)零交集。**零代码改动可修**。
D5 在位眼见:`components.json` wechat-bridge 行(pip_spec/pip_src/post_install 齐)+
`tauri.conf.json:86` 随包映射+`pyenv_install.rs` resolve_pip_src_spec/is_safe_relative/
COMPONENTS_SRC_RESOURCE_DIR;随包树清理链(`desktop/package.json:10` clean:pycache→
`scripts/clean-pycache.mjs` 缺省根含 plugins/wechat-bridge,b9c5054)闭合。
AC7 唯一剩余=主人 sudo 真跑(prd.md AC7,不在修复工范围);task.json 勾选归主会话。

## 7. 第四轮(同日 13:13 后;ask 快照=pytest 5372p/0f + vitest 1f)

并行会话已推进(10-12 TG 原生窗返回钮 bf988dc 提交;新在途集=10-12-tg-session-read:
`desktop/entry.py`/`desktop/ui-src/src/lib/api/types.ts`/`feed-screen.tsx`/
`feed-screen.test.tsx`/`src/myssia/store/sqlite.py` 全 M)。

| 门禁 | 命令(原样) | 结果 |
|---|---|---|
| pytest 全量 | `uv run --no-sync python -m pytest tests -q -p no:cacheprovider` | **5305 passed / 48 skipped / 0 failed**,exit 0(149.10s)——红=0 与 ask 摘要口径一致(±67 收集差=对方在途增删) |
| vitest 全量 | `npx vitest run`(desktop/ui-src) | Test Files **1 failed** / 34 passed;Tests 1 failed / 743 passed(744)——唯一红=`feed-screen.test.tsx > tg-category-entry 监控台 > 监控台历史入口(深检 F1 后语义)` |
| 定向复跑①(单用例) | `npx vitest run src/screens/feed/feed-screen.test.tsx -t "监控台历史入口"` | **1 passed** |
| 定向复跑②(整文件) | `npx vitest run src/screens/feed/feed-screen.test.tsx` | **180/180 全绿** |
| 任务面定向 | `uv run --no-sync python -m pytest tests/desktop/test_pyenv_resources.py tests/wechat-bridge -q` | **204 passed / 7 skipped** |
| Rust | `cargo test --locked`(desktop/src-tauri) | **90 passed / 0 failed / 1 ignored** |

**归因与处置**:唯一 vitest 红文件 `feed-screen.test.tsx` 在对方 M 在途集
(10-12-tg-session-read 正改 feed-screen.tsx/test.tsx),单用例与整文件复跑均绿
=多文件并发执行竞态+在途 tsx 半程态叠加的瞬态,非稳定红;与本任务面
(D5 分发/AC7)零交集(任务面 204p+Rust 90p 全绿)。按纪律**不修、skipped 归因,
零代码改动**。D5/AC7 状态与 §6 结论不变(D5 已落地在位;AC7 唯一剩余=主人
sudo 真跑)。本档第四轮增补为唯一产出。
