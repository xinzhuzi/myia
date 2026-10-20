# 配置蓝本漂移诊断(doctor 只读对账)

## Goal

给 `myssia doctor` 增加只读的「随包官方配置蓝本 ↔ 数据根 config」对账:
文件级比对同名 YAML 的哈希/缺件/多件,以 info findings + `config_drift` JSON
段呈现;只报不改,让漂移在造成采集故障前可见。

## Background(实证)

- **事故**:2026-10-19 20:00(local)wool run 8048 的 s74 源采集到 62 条,
  **62 条全部**因「提取条目缺少有效 url 字段」被拒
  (`myssia-20261019.jsonl` run_id=8048 逐条 62 行);同源在仓库配置修复后
  dry-run 62 条/0 失败。仓库 `config/wool.yaml` 修复时刻 20:10:46,数据根
  `~/Library/Application Support/MYIA/config/wool.yaml` 同步时刻 20:14:16 ——
  20:00 的运行读的是**旧数据根副本**。
- **种子语义是「绝不覆盖」**:`desktop/entry.py:624-657` `_seed_first_run`
  「缺哪件补哪件,绝不覆盖已存在文件」;`:658-680` 启动迁移同哲学。因此随包
  蓝本的修复**永远不会**到达已装机用户的数据根副本,双份真相是结构性存在。
- **既有挂账**:`.trellis/tasks/archive/2026-10/10-18-engine-pool-egress/prd.md:33`
  「装机品类蓝本漂移治理(双份真相问题备档,不在本任务收)」—— 本档为只读诊断
  的第一步,不做自动合并。
- **doctor 已有承载面**:`src/myssia/cli.py:4025` `_cmd_doctor` 汇总 findings 并
  产 JSON;`:3628` `_finding` 统一 finding 形状;`:4060-4080` 已有
  proxy/gates/firecrawl 分节,照此新增 `config_drift` 节即可。
- **随包目录解析逻辑已存在但只在桌面侧**:`desktop/entry.py:527-551`
  `_bundle_config_dir()`(托管 Python `Resources/myssia-src/` 布局 +
  frozen `.app/Resources/config` + exe 旁 resources/config;dev 树返回 None),
  与 `src/myssia/config_layout.py` 的 `CONFIG_DIR_NAME` 同源。CLI 侧无此能力,
  需抽共享解析器,避免两份路径规则漂移。

## Requirements

### R1 共享蓝本目录解析(只读)

- 在 `src/myssia/config_layout.py` 抽公共函数(命名实现定,语义如下):
  输入 `source_file` / `executable` / `frozen`(可注入,便于测试),按
  `desktop/entry.py:527-551` 现有候选顺序返回首个含 `*.yaml` 的目录,否则 None。
- `desktop/entry.py` 的 `_bundle_config_dir()` 改为薄委托(行为零变化,
  现有桌面种子测试须全绿);CLI doctor 调同一函数。
- doctor 新增 `--bundled-config DIR`:显式指定时优先;未指定走自动解析;
  解析不到 = 本项不检查(`checked=false` + reason),**零 finding、不报错**。
- `--config-dir` 与蓝本目录为同一目录(dev 默认 `./config`)→ `checked=false,
  reason="same_dir"`,避免自己比自己。

### R2 文件级对账

- 只比 `<dir>/*.yaml` 与 `*.yml` 平铺文件(与 `_seed_first_run` 的补种面一致);
  子目录、`.seeded` 标记、插件安装根不参与。
- 每个文件产出状态:
  - `drift` — 同名、字节不同(sha256 不同);
  - `missing_in_data_root` — 蓝本有、数据根无;
  - `extra_in_data_root` — 数据根有、蓝本无(用户自建,如 `telegram-groups.yaml`
    等;照报 info,不视为故障)。
- 每项附 `bundled_sha256` / `config_sha256`(存在侧)、mtime(ISO)、size;
  **绝不读取/输出文件内容**(配置里虽只有 `env:`/`keychain:` 引用,仍守只报
  形状不报值的红线)。

### R3 doctor 呈现与退出语义

- 每个 `drift` 文件一条 `severity="info"`, `scope="config"`,
  `code="config_blueprint_drift"`,消息含文件名与双方 mtime,并提示
  「差异可能是用户有意修改;本检查只报不改」。
- `missing_in_data_root` / `extra_in_data_root` 不逐条刷 findings,
  只在 `config_drift.counts` 中计数(避免装机常态噪声)。
- JSON payload 新增:
  ```json
  "config_drift": {
    "checked": true,
    "bundled_dir": "...", "config_dir": "...",
    "counts": {"drift": 1, "missing_in_data_root": 0, "extra_in_data_root": 2},
    "files": [{"name": "wool.yaml", "status": "drift", "bundled_sha256": "...", "config_sha256": "...", "bundled_mtime": "...", "config_mtime": "..."}]
  }
  ```
- 人读输出:有 drift 时一行汇总(`config drift: 1 件与随包蓝本不同`)并列出文件名;
  无 drift 不占行。
- doctor 退出码不变(0;问题全在 findings),对两个目录**零写入**。

### R4 测试(全合成临时目录)

- 单元:解析器三种布局候选 + 不可解析返回 None(与桌面现有测试同口径)。
- 对账纯函数:identical → 无 drift;同名异字节 → `drift` + 双方 sha256;
  缺件 → `missing_in_data_root`;多件 → `extra_in_data_root`;非 YAML 忽略;
  子目录忽略。
- CLI:`main(["doctor", ..., "--json", "--bundled-config", tmp_b, "--config-dir", tmp_d])`
  (照 `tests/cli/test_cli_full.py:409` 的 doctor 用例形态):
  - 相同目录 → `checked=false/reason=same_dir`;
  - 漂移 → JSON 含 `config_drift.files` 与 info finding,退出 0;
  - 输出字符串中不含任一 YAML 的内容(只允许哈希/mtime/文件名);
  - 运行前后两目录文件字节与 mtime 不变(只读证据)。
- `desktop/entry.py` 委托重构后:`tests/desktop` 种子相关用例全绿。

## Acceptance Criteria

- [x] A1 `myssia doctor --json --bundled-config <b> --config-dir <d>` 输出
      `config_drift` 节;两目录 YAML 完全相同时 `counts.drift=0` 且零
      `config_blueprint_drift` finding。
- [x] A2 同名异字节 → 恰一条 info finding;`files` 项含双方 sha256/mtime/size;
      全输出无文件内容。
- [x] A3 缺件/多件分类与计数正确;非 YAML 与子目录零参与。
- [x] A4 `--bundled-config` 未给时自动解析:dev 树命中仓库 `config/`(与
      `--config-dir` 同目录则 `same_dir`);托管/frozen 布局照桌面现有候选;
      解析不到 = `checked=false`,零 finding、退出 0。
- [x] A5 两目录运行前后逐文件 sha256 与 mtime 不变(零写入),凭据引用值
      未被解析或打印。
- [x] A6 `tests/cli` doctor 相关 + `tests/desktop` 种子相关全绿;`ruff check`
      通过;全量 Python 测试无新增红。

## 边界

- **只读**:不做自动合并/覆盖/同步,不改 `_seed_first_run` 与迁移语义。
- **不做 UI**:设置屏/桌面启动告警不在本档;若后续要上桌面,另立档。
- **不做语义级 YAML diff**:只到文件级哈希;逐键 diff 需脱敏与合并策略,
  属后续决策。
- **不碰**插件安装根(`plugins/`)、cron 账本、`gates.yaml`(后者已有独立
  诊断面);不 bump sidecar 协议(本档纯 CLI)。
- 差异不等于错误:任何情况下不得把用户合法手改报成 error/fatal。

## Notes

- 本档是「双份真相」治理的安全第一步:先让漂移可见,自动传播/合并的取舍
  (覆盖用户手改 vs 只提示 vs 三方合并)**待主人定夺**,不在本档拍板。
- 预计改动:`src/myssia/config_layout.py`(解析器)、`src/myssia/cli.py`
  (doctor 参数/对账/输出)、`desktop/entry.py`(薄委托)、测试 2-3 文件。

## 执行记录(2026-10-20)

- `config_layout.resolve_bundled_config_dir()` 落地:托管资源树按最近
  `myssia-src` 祖先定位(兼容装机 ``myssia-src/myssia/*.py`` 与
  ``myssia-src/entry.py`` 两形)、frozen 三候选照旧;`include_dev=True`
  仅供 CLI 诊断补 ``<repo>/config`` 候选 —— 桌面委托不开,dev 形态行为零变化。
- `desktop/entry.py::_bundle_config_dir` 改薄委托(候选/顺序/`*.yaml` 判定不变)。
- doctor 新增 `--bundled-config`、`config_drift` 段与
  `config_blueprint_drift` info finding;reasons:`same_dir` /
  `bundled_dir_missing` / `bundled_dir_unresolved` / `config_dir_missing`;
  `files` 只含非一致件,缺件/多件不刷 finding;人读有 drift 才占一行。
- 测试:`tests/test_config_layout.py` 新增 7 个解析器用例(两形托管 /
  .app 资源 / exe 旁 / 空目录 None / dev 候选开关);`tests/cli/test_cli_full.py`
  新增 `TestDoctorConfigDrift` 7 用例(一致 / 漂移+只读+无内容 / 缺多分类 /
  人读汇总行 / same_dir / 显式缺失 / 自动解析不到)。
- 门禁:`pytest tests/test_config_layout.py tests/cli/test_cli_full.py -q`
  → 72 passed;`pytest tests/desktop -k "bundle_config_dir or seed"` →
  15 passed;`pytest tests/desktop tests/cli -q` → 669 passed;
  `pytest -q` 全量 → **6565 passed, 56 skipped**;`ruff check` 五文件全过。
- 真机数据根只读实测(2026-10-20,仓库 CLI):
  `doctor --config-dir ~/Library/Application Support/MYIA/config` →
  `checked=true`,counts=`drift 7 / missing_in_data_root 2 / extra_in_data_root 18`,
  7 条 info finding(credentials/exposure/monitor/myssia-demo/
  telegram-channels/telegram-web/weixin),exit 0;人读行
  「config drift: 7 件与随包蓝本不同…;只报不改」。
  18 件 extra 中多数为 `*.backup-*.yaml`(只计数不刷 finding,符合设计)。
  这一跑即把 PRD 背景里的 wool 事故同型「双份真相」变成可见信号;本档
  仍只报不改。
