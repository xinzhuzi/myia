# Phase B 桥骨架验证记录(2026-10-11)

> 执行件:骨架工(10-11-wechat-ui-bridge Phase B)。本文只记形状级证据(红线 6:零内容、零密钥材料)。

## B1 组件目录落点

- 落点:`plugins/wechat-bridge/`(组件源码 + 组件戳 `component.json` + README)。
- 惯例对账:
  - 运行位 = design §1/§7 钉的 `~/.myia/plugins/wechat-bridge/`,即插件安装根(`src/myssia/plugins/installed.py` `DEFAULT_INSTALL_ROOT` = `~/.myia/plugins`);仓内 `plugins/<id>/` 目录即装机源(随包/`myssia plugin install` 链的同源)。
  - **不带 `plugin.yaml`**:市场插件 manifest(schema 需 modes/install)是场景插件的面;wechat-bridge 是受管桥组件,消费形态 = push 层子进程调用(`wechat_bridge_bin`,Phase F 接线)。桌面随包发现对无 manifest 目录自动跳过(`desktop/entry.py` `_bundled_plugin_views`),零市场 UI 干扰。
  - `pyenv_components` 链 = pip 闭包组件(壳写戳 state/fingerprint);wechat-bridge 是原生运行件(sqlcipher 系统依赖),故组件戳落在组件目录内(`component.json`:版本 + 适用微信版本范围 + §6 码表 + §7 配置缺省),design §4「版本锁」由 `tests/wechat-bridge/test_component_stamp.py` 与代码互钉。
- 命名(G7):组件 `wechat-bridge`,包 `wechat_bridge`,push 通道 `weixin-local`(Phase F);`src/myssia/push/weixin.py`(官方 Hermes 桥蓝本)零改动。

## B2 CLI 契约

- design §6 四子命令 + `--probe` 全按文样(`--json` 逐层可放,契约旗标缺省即开);§6 十二项错误码封闭表在 `wechat_bridge/codes.py`,戳/测试双向对账。
- §7 配置面:`<数据根>/wechat-bridge/config.json`(缺文件可用;domains/limits/copy_ttl_hours/copy_capacity_mb;**无频控键**,配置里写频控键 = usage 拒载);频控状态 `数据根/wechat-localdb/send_state.json`(flock + 原子写,时间注入)。
- 骨架态如实应答纪律:前置检查真跑(§6 码序 10→11→12;localdb 20),实现层未落地 = exit 1 + `not_implemented` 过渡码(不谎报 §6 具名族),密钥途径 D4 未裁决 = exit 21 `key_unavailable`。

## --probe 实跑(微信托盘态,2026-10-11,共 3 次一致)

命令(装机同形):

```console
cd plugins/wechat-bridge && python -m wechat_bridge --probe
```

- exit 0;`state=degraded`;`wechat_version=4.1.15`;checks:进程 ok / AX 权限 ok / 主窗口 fail(托盘)/ localdb 落盘 ok / 密钥 unavailable / AX 树 unknown(Phase C 判据);reasons = `window_closed` + `key_unavailable`。
- 全程只读零前台扰动:pgrep 进程表、plistlib 直读 Info.plist、`AXIsProcessTrusted`(无弹框语义)、CGWindowList 快照、目录计数。原始输出存档:`tests/wechat-bridge/fixtures/probe_tray_state_20261011.json`(fixture 录制惯例,形状级)。
- 不装可用:CLI 对配置缺文件(全缺省)、pyobjc 缺位(检查如实 unknown)、非 darwin(同)均可用不炸。

## B3 测试与 CI

- `tests/wechat-bridge/`:74 测试(3 条 `MYIA_WECHAT_E2E=1` 门控真机探针,CI 缺省跳过;AX/localdb 层全 mock;golden 基件 `fixtures/golden_cli_payloads.json`,再生成 = `MYIA_WECHAT_BRIDGE_REGEN_GOLDEN=1` 重跑 TestGolden)。
- 组件单测:`uv run --no-sync python -m pytest tests/wechat-bridge -q` → **71 passed, 3 skipped**;门控跑(`MYIA_WECHAT_E2E=1`)→ **74 passed**。
- 全量门禁:`uv run --no-sync python -m pytest -q` → **5160 passed, 43 skipped**(连跑两次全绿);`uvx ruff@0.16.10 check .` → All checks passed。
- 测试目录名用连字符 `tests/wechat-bridge`(镜像组件目录),**勿改回下划线**:`tests/wechat_bridge` 会被 pytest prepend 导入模式当 PEP 420 命名空间包,抢注组件包名 `wechat_bridge` 致全量导入错乱(实测);组件导入走 `pyproject.toml` `[tool.pytest.ini_options] pythonpath`,不走 conftest(conftest 文件名会顶掉仓库通用裸 `from conftest import` 共享夹具,实测踩全量)。

## 移交注记(Phase C/D/E/F)

- Phase C/D 在 `wechat_bridge/ax.py` 原地扩 AX 层(前置门 `ensure_ui_preconditions` 已可复用);Phase E 在 `wechat_bridge/localdb.py` 原地扩密钥/副本(E1 落地时同步替换 `system_checks.localdb_key_available` 判据);`send_state.record_send` 仅在回执确认后调用。
- 新测试文件放 `tests/wechat-bridge/`,共享件进 `bridge_testkit.py`(勿新建 conftest.py,原因见上)。
