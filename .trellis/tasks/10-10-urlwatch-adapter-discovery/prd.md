# urlwatch 场景件适配器装机态发现链断裂

## Goal

桌面装机形态下,urlwatch 引擎定位场景件 `adapter.py` 的三条候选路径全部落空,而真实组件所在的
`~/.myia/plugins` 组件根不在候选清单里。表现为 ai-news 品类 `anthropic-news-watch` 源自
2026-10-08 起每轮调度必败(`urlwatch_adapter_missing`),UI 显示「失效 · run#58 失败」。
修复 = 发现链补组件根候选(或壳层回落注入),并核查同手法的 maigret 等场景件引擎。

## 症状

- 监控台源行:`anthropic-news-w… / AI资讯 / urlwatch / 失效 / 8 次 · run#58 失败`。
- 日志(`~/Library/Application Support/MYIA/logs/myssia-2026*.jsonl`)每轮:
  `urlwatch 适配器不存在:plugins/myssia-urlwatch/adapter.py(场景件应随仓库 plugins/ 分发;
  桌面端=myssia plugin install plugins/myssia-urlwatch)` → 引擎链耗尽 → 采集最终失败。
- 采集**从未发起网络请求**——不是 anthropic.com 不可达、不是代理/反爬问题。

## 证据矩阵(2026-10-10 实测)

| # | 证据 | 结果 |
|---|------|------|
| E1 | 失效起点 | 10-07 20:04(本地)最后一次成功(items=1)→ 10-08 20:00 起连败;与 10-08 晚换装(TG 线 sidecar 并入装配构建)时间吻合 |
| E2 | 调度节奏 | cron `AI资讯` = `0 8,20 * * *`(jobs.json ef86ce95d1fd),每天 08:00/20:00 各一轮,失败即 UI「失效」态 |
| E3 | 候选① cwd 相对 `plugins/` | sidecar PID 17174 实际 cwd = `/`(`lsop cwd` 实测)→ `/plugins/...` 不存在;数据根 `plugins/` 只放管线 YAML 配置,非组件 |
| E4 | 候选② `MYIA_BUNDLED_PLUGINS` | 当前 sidecar env 已注入(`/Applications/世事.app/Contents/Resources/plugins`),但该目录按 10-06「装机包只带声明」规范只有 `README.md + plugin.yaml`,**无 adapter.py**(10-10 19:00 新包实测) |
| E5 | 候选③ 源码树兜底 | 托管 Python 形态(`<数据根>/python`),非源码树布局,兜底不命中 |
| E6 | 真件位置 | `~/.myia/plugins/myssia-urlwatch/adapter.py` 存在(10-05 设置页组件安装;另有 `myssia-maigret/adapter.py` 同布局)——**不在任何候选路径上** |
| E7 | 旧装对照 | `~/Applications/MYIA.app`(10-03)二进制无 `MYIA_BUNDLED_PLUGINS` 字符串;10-06/10-07 的成功 runs 出自旧形态(cwd/内嵌件与今不同,具体通道已不可考,进程已不在) |

## 根因

`src/myssia/engines/urlwatch.py` 的 `import_urlwatch_adapter()` / `render_helper_path()`
候选顺序 = ① `plugins_dir`(cwd 相对)→ ② `MYIA_BUNDLED_PLUGINS` → ③ 源码树。
10-06「插件源码不随包」规范落地后,装机态三个候选天然全空(声明件包 × cwd=/ × 托管 Python),
发现链与组件管控面(`~/.myia/plugins` + pyenv_components 戳)之间**断链**。

## Requirements

- R1 装机态下 `engine: urlwatch` 源必须能发现已安装的组件 adapter(组件根
  `~/.myia/plugins`,darwin;win/lin 按组件管控面实际根)。
- R2 发现链收口为一处权威实现(两函数同序,勿再各写一份候选表);候选扩充不破坏
  dev/CLI(cwd 相对)与源码树布局的既有行为。
- R3 maigret 及一切复用「场景件动态装载」手法的引擎(credhunter 先例)同病排查:
  装机态发现路径逐一验证,同样断链的一并修。
- R4 修后 UI 侧该源无需人工干预即自愈:下一轮调度(或手动「立即跑」)恢复 items 采集,
  「失效」态按既有失败清零语义回落。
- R5 回归:打包件(声明件规范)内不可依赖仓库路径;测试覆盖「组件根命中/三候选全空结构化报错」两态。

## Acceptance Criteria

- [ ] AC1 本机装机态实测:`anthropic-news-watch` 手动触发一轮,日志出现采集成功/合法空态
      (watch_unchanged),不再出现 `urlwatch_adapter_missing`。
- [ ] AC2 候选顺序含组件根且两函数(import/render helper)一致;单测覆盖三候选+组件根四态。
- [ ] AC3 maigret 同手法引擎核验结论入档(同修或明确无病)。
- [ ] AC4 门禁全绿(pytest + vitest + tsc);装机包刷新并换装后复查一轮真跑。
- [ ] AC5 UI 监控台该源「失效」态解除(下一轮调度后像素/截图证据)。

## Notes

- 修复方向候选(实现时定,倾向 A):
  - A. 引擎候选表补组件根(与 pyenv_components 管控面同源,最小改、单点收口);
  - B. 壳层注入:bundled 目录缺件时把 `MYIA_BUNDLED_PLUGINS` 回落指到组件根;
  - C. 设置页组件安装落点改到引擎已扫描目录(动管控面,影响面大,不倾向)。
- 时序判断:本轮(10-10 19:01 新 sidecar)env 已注入但候选②为声明件目录,**当晚 20:00
  调度预计继续失败**——修复落前该源持续「失效」属预期,不是新病。

## Design(2026-10-10 实施定案)

按 A 落地,收口形式:候选表上移为**一处权威实现**。

- `src/myssia/plugins/installed.py` 新增 `scenario_file_candidates(plugin_id, filename,
  plugins_dir="plugins")`:候选序 = cwd 相对 `plugins_dir` → `MYIA_BUNDLED_PLUGINS`
  锚点 → `default_install_root()`(`MYIA_PLUGIN_DIR` 可覆盖,缺省 `~/.myia/plugins`)。
  与组件管控面(设置页安装落点 / `myssia plugin install`)同源,零新概念。
- 三个装载点改消费该 helper,装载手法(compile+exec)与报错文案仍归各自:
  - `engines/urlwatch.py::import_urlwatch_adapter`(保留源码树兜底为末位);
  - `engines/urlwatch.py::render_helper_path`(同上);
  - `engines/credhunter.py::import_credhunter_adapter`(补齐锚点+安装根两候选)。
- R3 核验结论:**maigret/proxy/media 等 CLI 侧装载无病**——CLI 参数缺省即
  `default_install_root()`(cli.py listing `--dir`),只有引擎侧是 cwd 相对单/三候选。
- 影响面(GitNexus impact 实测):三符号上游仅各自引擎 fetch 链
  (`_adapter`/`_fetch_impl`、`_fetch_exposure`),无跨进程上游,风险低。
- 测试:urlwatch 三态(安装根命中/锚点优先序/锚点失效落安装根与源码树)+
  credhunter 安根命中 + helper 直测二态;`test_bundled_plugins_env_ignored_when_not_a_dir`
  补 `MYIA_PLUGIN_DIR` 指空目录,保本机装有真组件时测试仍确定性走兜底。
- 门禁:改动文件 ruff 0.16.10 绿;全量 pytest(CI 同款 `python -m pytest`)绿。
  纯 Python 改动,UI 门禁(vitest/tsc)不受影响,随 CI 兜跑。
- 预存红归因(非本档引入):`uv run pytest`(裸 pytest,无 cwd 入 sys.path)会在
  `tests/desktop/test_telegram_category_stamp.py` 收集期报 `from desktop import entry`
  ImportError;`PYTHONPATH=.` 或 CI 同款 `python -m pytest` 即绿(3 passed)。CI 口径
  本就带 cwd,故不修码。

## 交付记录

- 2026-10-10:代码+测试落地;装机包重打包换装与真跑验证见 AC1/AC4/AC5 勾选态。
