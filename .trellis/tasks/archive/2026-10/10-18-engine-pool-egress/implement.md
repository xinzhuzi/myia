# Implementation — 引擎侧 IP 伪装:按源挂池与池配置装机送达链路

> 执行序:步骤 1-5 为仓库内改动+测试,6 为打包换装,7 为装机侧手改+验收,8 为收尾。每步带验证命令;提交切分与回滚点见文末。改动前先读 `prd.md` / `design.md` / `research/` 两件。

## 仓库内改动

### 步骤 1:品类 yaml 挂池(仓库蓝本)

- [x] 1.1 `config/telegram-channels.yaml:38`:telegram-durov 的 `proxy: direct` → `proxy: pool:clash`,行尾注释「被墙域:本机 Clash 混合口(池声明见 proxy-pools.yaml)」(照 ai-news.yaml:299 reddit-ml 同款风格);同源上方注释若提 direct 语义一并校正。
- [x] 1.2 `config/telegram-groups.yaml:59`:telegram-mihomo_party_group 的 `proxy: direct # api.telegram.org 出海按需改 pool:<名称>` → `proxy: pool:clash`(空态预挂注释:bot_token 激活即走池)。
- [x] 1.3 `config/ai-news.yaml`:deepmind-blog(:127)/ google-research(:138)/ qwen-blog(:182)/ **openai-news(:116)/ hf-blog(:160,定稿升挂)** 五处 `proxy: direct` → `proxy: pool:clash`(被墙域注释同款;openai/hf 两处注释记「CF 风控强站防拉黑升挂——观察判据抓不住 403/质询,定稿 2026-10-18」)。
- [x] 1.4 (定稿取消)原「openai-news/hf-blog 行尾补观察位注释」方案取消——二源升挂池(见 1.3),本批无观察位;观察位注释模板(修正版判据:transport 失败**或 403/质询类应用层拒绝**实录即挂)留档 design §2 供未来 stay-direct 候选用。
- [x] 1.5 核对零越界:`git diff --stat` 只见上述 3 件;stay-direct 清单文件零改动。

验证:
```bash
uv run --no-sync python -m pytest tests/cli/test_sources_write_surgery.py tests/plugins/ -q   # 装载/roundtrip/插件铁律
uv run --no-sync python -c "from myssia.schema import load_category_file; [load_category_file(p) for p in ('config/ai-news.yaml','config/telegram-channels.yaml','config/telegram-groups.yaml')]"   # 逐件装载(schema.py:2313,golden 测试同款入口)
```
(装载入口已定稿写死:`myssia.schema.load_category_file`——拷问 F10,不再是占位符;门禁结论见 research/source-inventory.md §2 ①。)

### 步骤 2:proxy-pools.yaml 随包

- [x] 2.1 `desktop/src-tauri/tauri.conf.json` resources 映射(45-63 区)增一行:`"../../config/proxy-pools.yaml": "config/proxy-pools.yaml"`(按字母序插在 news.yaml 之后、stocks.yaml 之前,与清单排序一致)。
- [x] 2.2 确认 `config/proxy-pools.yaml` 内容即装机期望蓝本(clash 单上游 127.0.0.1:7897;池化形态零改动)。

验证:
```bash
python3 -c "import json; r=json.load(open('desktop/src-tauri/tauri.conf.json'))['bundle']['resources']; assert 'config/proxy-pools.yaml' in r.values(), r"
```

### 步骤 3:doctor config_auto 查找顺序(entry.py)

- [x] 3.1 `desktop/entry.py` doctor 分支(1515-1518 区):`default_pools = ctx.home / "pools.yaml"` 改为按序探测 `[ctx.home / CONFIG_DIR_NAME / "proxy-pools.yaml", ctx.home / "pools.yaml"]`,第一个存在者拼 `--config`(都不在维持不拼;新位路径同走 `CONFIG_DIR_NAME`,与 4.1/5.1 同源——拷问 F8);注释记双位回落理由(新位=resources 补种落点,旧位=历史装机兼容)。
- [x] 3.2 `tests/desktop/test_proxy_pool_panel.py`:既有 `<home>/pools.yaml` 用例(:102,:289-333)应因回落兼容继续绿;新增用例:仅 `config/proxy-pools.yaml` 在场 → config_auto 用它;双在场 → config/ 优先。

验证:
```bash
uv run --no-sync python -m pytest tests/desktop/test_proxy_pool_panel.py -q
```

### 步骤 4:run.start 自动拼 --config(entry.py)

- [x] 4.1 `_m_run_start`(3641-3677 区):`_serve_context()` 收口单次调用复用;`if params.get("config")` 分支后加 `elif ctx.home is not None and (ctx.home / CONFIG_DIR_NAME / "proxy-pools.yaml").exists(): argv_tail += ["--config", str(...)]`——路径走 `CONFIG_DIR_NAME`(entry.py:353 已自 myssia.config_layout 导入),**禁写 `"config"` 字面量**(拷问 F8:常量改名即静默漂移)。
- [x] 4.2 新增 tests/desktop 用例(落 test_desktop_sidecar_protocol.py 或同目录 run 相关文件,按被测对象归组):显式 params.config 优先;home 模式池文件在场自动拼;池文件缺失不拼;dev(ctx.home None)不拼;dry-run 同路径。

验证:
```bash
uv run --no-sync python -m pytest tests/desktop/ -q
```

### 步骤 5:cron job_command 自动拼 --config(runner.py)

- [x] 5.1 `src/myssia/cron/runner.py` `job_command`(175-193 区):顶部 import 区新增 `from myssia.config_layout import CONFIG_DIR_NAME`(config_layout.py:25,同包真源,与 entry.py 同一常量——拷问 F8);config_path 缺省分支后加 `elif`——`os.environ.get("MYIA_HOME")` 在场且 `Path(home) / CONFIG_DIR_NAME / "proxy-pools.yaml"` 存在 → 拼 `--config`;docstring 补自动发现语义(显式优先/home 门/文件在场门)。
- [x] 5.2 `tests/cron/test_cron_runner.py` 扩测(job_command 组装区 :300 邻域):monkeypatch MYIA_HOME + tmp 池文件 → 自动拼;显式 config_path 赢;无 MYIA_HOME(dev)不拼;MYIA_HOME 在场但文件缺失不拼。

验证:
```bash
uv run --no-sync python -m pytest tests/cron/ -q
```

### 步骤 6:全量门禁

- [x] 6.1 全量 pytest(CI 同款):
```bash
uv run --no-sync python -m pytest -q
```
- [x] 6.2 golden 预期零触碰,跑了确认:
```bash
uv run --no-sync python -m pytest tests/push/ -q          # push golden 家族(test_push_schema_targets.py 实测在 tests/push/,拷问 F10 定稿写死)
uv run --no-sync python tests/regen_push_targets_golden.py  # 同源自检(不带 --refreeze)
```
- [x] 6.3 桌面相关组全绿后进入打包。

## 打包与装机

### 步骤 7:打包

- [x] 7.1 `just build-desktop`(产物 desktop/src-tauri/target/release/bundle/macos/myssia.app;时长超 30 分钟属正常,后台任务 + exit 文件监控,禁 sleep 轮询——工程纪律)。
- [x] 7.2 冒烟:`python3 desktop/ui-src/e2e/package_smoke.py`(brotli 内嵌 dist 验源;按其参数面指向新 bundle)。

### 步骤 8:换装 + 装机侧手改 + 验收

- [x] 8.0 换装跨度披露与跨面冒烟(拷问 F4 定稿新增):本次覆盖安装 = 0.0.3→main **全量跨越**,非本任务单一逻辑安装;v0.0.3..HEAD 运行时行为关键笔至少——abe51b9c(日报出站切「AI信息分析师」bot)、b1684dfc(日报 AI 白嫖分区三新源)、9880aa0a(思考层切魔搭)、a99f6174(games 羊毛面)、29e7bb37/1b147007(微信图片入 feed)、e33612ff/8d42a63d(agent_reach)。装机后必做冒烟(A7):日报下一期仍送达预期 bot 且 AI 白嫖分区含三新源(覆盖前两笔);其余跨度面在任务档记录「已跨越、未逐面冒烟」。
- [x] 8.1 进程清场:`ps aux | rg -i "世事|MYIA|myssia_desktop_entry"` 为空才动(不为空则等本轮结束,不静默杀)。
- [x] 8.2 备份旧包:`mv /Applications/世事.app /Applications/世事.backup-$(date +%Y%m%d%H%M%S).app`;新包入位;ad-hoc 签名;`codesign --verify --deep --strict /Applications/世事.app` 通过。
- [x] 8.3 装机包含本任务逻辑(A5):安装件 `Resources/config/` 含 proxy-pools.yaml;安装件 Python 文件与源码逐字节比对(package_smoke 判例形态,10-15-feed-local-images/verification.md:12-13)。
- [x] 8.4 数据根手改(每件先 `cp x.yaml x.yaml.bak-<ts>`):`~/Library/Application Support/MYIA/config/` 下 telegram-channels.yaml / telegram-groups.yaml / ai-news.yaml 的同款 **7 处** `direct → pool:clash`(以装机件实际行号为准,先 grep 定位;装机件与蓝本已漂移,勿整文件覆盖)。三条设防(拷问 F3/F5 定稿):
  - **顺序硬约束**:8.2 换装完成且新 sidecar 在跑之前,**禁止手改数据根 proxy 值**——反序则旧包无自动发现,「TG频道监控」「TG群监控」(装机 jobs.json 实测 config_path=None)下一 fire 即报 proxy_pools_not_configured;
  - **并行编辑设防**:手改前三件各记快照(`shasum -a 256 <file>` + `stat -f '%m %N' <file>`);写完立即复核 diff——除目标 7 处 proxy 行外零变化,不一致先停手排查再续;数据根今晨(10-18 01:20-02:49)有并行会话编辑实录(ai-news.yaml / ai-token-deals.yaml / daily-digest.yaml),执行前与并行会话约定数据根独占操作窗口;
  - **只改 proxy 行**:与手改前快照逐行 diff 佐证,不整文件替换。
- [x] 8.5 启动装机 app(数据根补种不覆盖既有件;jobs.json 零手改——自动发现兜底)。
- [x] 8.6 验收 A3(出口 IP 分流):
```bash
curl -s http://members.3322.org/dyndns/getip            # 本地 ISP IP 直连基线
# 装机 app:设置→代理池 探测(proxy.probe config_auto)→ 记录 exit_ip
# 判据:exit_ip ≠ 本地 ISP IP(探索员基线 198.2.214.3 vs 139.227.235.178;节点可漂移,以不等为准)
```
- [x] 8.7 验收 A4(池源取回,**必须走 R3 自动发现路径**):装机 app 对「TG频道监控」品类发起一次采集——该 job 实测 config_path=None,恰走 job_command 自动拼 `--config` 路径;判据:telegram-durov 条目取回、direct 源正常、日志无 proxy_pools_not_configured;mihomo/Clash 面板连接记录佐证 7897 有该域流量(可选加强)。**「等既有 AI资讯 cron fire」已定稿删去**(拷问 F7:AI资讯 是 16 job 中唯一显式 config_path,fire 成功只证明旧显式路径仍在工作,不构成 R3 验证;R3 验收 = 本项 + 8.3/A5 的 argv 佐证叠加)。
- [x] 8.8 验收 A7(换装跨度冒烟,拷问 F4):日报下一期送达预期 bot(AI信息分析师)+ AI 白嫖分区含三新源;其余跨度面记录「已跨越、未逐面冒烟」入任务档。
- [x] 8.9 UI 未刷新才清 WKWebView 缓存(~/Library/WebKit/com.myssia.app、~/Library/Caches/MYIA/)——口传套路,如实记录是否执行。

## 提交切分(pathspec 纪律;每笔 git add 逐文件列名,禁目录通配)

1. `feat(config): 引擎侧按源挂池——telegram-durov/mihomo_party_group/deepmind/google-research/qwen-blog/openai-news/hf-blog 七源挂 pool:clash(后二 CF 风控强站定稿升挂)`
   - config/telegram-channels.yaml、config/telegram-groups.yaml、config/ai-news.yaml
2. `feat(desktop): 池配置装机送达收口——proxy-pools.yaml 随包 + doctor config_auto 双位回落 + run/cron home 模式自动发现`
   - desktop/src-tauri/tauri.conf.json、desktop/entry.py、src/myssia/cron/runner.py、tests/desktop/test_proxy_pool_panel.py、tests/desktop/test_desktop_sidecar_protocol.py(或新增 run 用例所在件)、tests/cron/test_cron_runner.py
3. 收尾:任务档归档提交(trellis bookkeeping,单独一笔;按仓库三段式惯例工作提交在前)。

注:提交信息风格照 `git log --oneline -5` 现行中文长句式;提交前跑 `gitnexus detect-changes -r shishi --scope staged`(文档/配置类可豁免,本笔含 py 代码不可豁免);禁 push。

## 回滚点

| 点位 | 回滚动作 |
|---|---|
| 提交 1(挂池 yaml) | `git revert <c1>`——池源回 direct,CLI dev 不再需要 --config |
| 提交 2(送达链) | `git revert <c2>`——回显式-only;装机侧自动发现随旧包恢复(换回备份包) |
| 装机回滚(**原子联动,拷问 F6 定稿**) | 换回 /Applications/世事.backup-<ts>.app + codesign 校验,**同批**逐件 `mv x.yaml.bak-<ts> x.yaml` 还原 7 处——缺一即留中间态(旧包无自动发现,TG频道/TG群 job 每 fire 报 proxy_pools_not_configured);两步须在同一 cron fire 间隔内完成 |
| 打包中途 | bundle 产物目录可整弃,无状态残留;换装未动旧包前零风险 |

## golden 重生成预案(预期不需要)

- 依据:golden 回归只比 push 子树(tests/push/test_push_schema_targets.py:244-297 承诺边界 :255-258),proxy 值不参与;JSON 内 32 处 proxy 快照值非比对面(research/source-inventory.md §2 ⑤)。
- 若 6.2 意外红:**先查 diff 根因**(是否误触 push 子树/是否夹带无关改动),禁止盲重置基线;确认属合法演化且评审点头后才:
```bash
uv run --no-sync python tests/regen_push_targets_golden.py --refreeze
```
- refreeze 后必须全量 pytest 复跑并在任务档记录重置理由与新 MANIFEST 摘要。

## 风险提示(执行者必读)

- 数据根手改前先 `diff` 装机件与蓝本(已漂移:装机多 searxng/weixin-sns/feishu-groups 等 + .bak 族),**只改 proxy 行,勿整文件替换**。
- 数据根手改窗口存在并行会话在途编辑(10-18 凌晨实录:ai-news.yaml 01:20、ai-token-deals.yaml 02:26、daily-digest.yaml 02:49,均实测 mtime)——执行 8.4 前与并行会话约定独占窗口,快照/diff 双复核(拷问 F3)。
- cron/runner.py 属 Hermes 蓝本偏离表管辖模块(spec python/index.md 定时任务底座节):改动仅限 job_command 缺省分支(含顶部新增 CONFIG_DIR_NAME import 一行),不动 D1-D14 偏离面;SQLiteStore SCHEMA_VERSION 零触碰。
- entry.py 改动须同步 sidecar 协议测试口径(spec python/index.md 桌面发行数据根节:「改路径行为必须同步 tests/desktop/test_desktop_sidecar_protocol.py」)。
- 验收 A3/A4 依赖本机 Clash 在线(7897);探测失败先 `nc -z 127.0.0.1 7897` 再查 mihomo 服务,勿把 Clash 挂误判为本任务回归。

## 第二批:海外站一律藏(主人裁决追加,2026-10-18 执行)

裁决:主人「按照你的建议去做」→ prd 残余风险升级路径触发,第二批 14 处 `direct → pool:clash`(蓝本 config/ + 装机数据根双侧;数据根逐行验内容后手术改 + `.bak-20261018-batch2` 先行,勿整文件覆盖——凌晨并行编辑窗口纪律照旧,实测 14/14 命中)。

- [x] B1 蓝本 14 处:ai-news.yaml 五厂商源(:149/:171/:219/:250/:272)、games.yaml 四源(:59/:86/:148/:204)、stocks.yaml(:74,顺手退役 v0.1「仅 direct 生效」过时注释)、credentials.yaml aipocket(:70)、myssia-demo.yaml(:32)、ai-token-deals.yaml 两 releases 源(:84/:95)。
- [x] B2 维持 direct 裁定:aihot(DoH 实测 aihot.news→eo.dnse2.com→112.84.131.78 腾讯 EdgeOne CN 边缘,判国内)、credhunter-native(消费路径未核验)、urlwatch 四源/agent_reach/tg_web/firecrawl 云渲染/零 HTTP/自建端点(既定)。
- [x] B3 测试配套:_single_source_config 代理压回 direct;scoped(tests/cli/test_sources_write_surgery.py + tests/plugins/)803 passed + 全量 **6486 passed/56 skipped** 实跑绿。
- [x] B4 数据根同步:终态 pool:clash 计数 ai-news 12(含一批 7)/games 4/stocks 1/credentials 1/myssia-demo 1/ai-token-deals 2。
- [x] B5 装机实跑:装机 python(PYTHONPATH=app Resources/myssia-src)+ 显式 --config 跑 stocks——yahoo-chart 经池取回 5 条行情(NVDA 214.13/AAPL 343.46/TSLA 354.72/0700.HK 417.8/600519.SS 1329),全链 success,fetch 8.5s(run_id 4124,2026-10-17T20:21:46Z)。
- [x] B6 提交:外科式只收本批 hunks(同文件并存并行会话在途改动,`git diff -U0` 过滤「第二批」标记行 `git apply --cached`,他人 hunks 原样留工作树);tests/plugins/test_plugins.py 改动全属本任务(改前核该件零脏)。
- 回滚(比第一批宽松):蓝本 revert 本批提交 + 数据根 6 件 `mv x.yaml.bak-20261018-batch2 x.yaml`——direct 是安全态(无 pools 注入依赖),反序无中间态报错风险。

## 收官实录(2026-10-19,主人令「没有解决的要继续解决」)

- **实施归属披露**:步骤 1(两批挂池)=bbc95de7+批2 提交;步骤 2-5(送达三缺口)=并行会话 4ec13773(早于 v0.0.5 发版,旧装机包即含);本日主会话做的是**验收+收口**非实施。
- A5:装机包(2026-10-19 晨 0.0.6 换装)Resources/config/proxy-pools.yaml 在位;entry.py/runner.py 与源码字节级一致(diff 亲验)。
- A3:装机 CLI doctor 探测——直连 139.227.235.178(上海联通)vs 经池 exit_ip=198.2.214.3(US 圣何塞),latency 1.2s ok=true,分流成立。
- A4(生产实证):run 6471 今晨 00:03 telegram-durov 经池取回 20 条 attempts=1 failures=0;当日零 proxy_pools_not_configured;TG群监控每 30min 空态 success(预挂正确)。
- A1:全量 pytest 6550 passed/56 skipped/0 failed(146s)——顺带修复 test_logs_tail_run_id_merges_disk_rows 日期腐烂夹具(写死 20261011 出 7 天保留窗,改随墙钟当日;今晨基线 2 红全愈)。
- A6:4ec13773 三入口测试(cron/desktop 双件)scoped 241→修后 242 全绿。
- A7:20:05 新包首期日报待验(一次性自动化 20:21 已挂,结果回写本档)。
- 8.4 数据根手改:批1+批2 已于 10-18 完成(B4 终态计数在档),本日零触碰。

## A7 收官实录(2026-10-19 20:36,主会话亲验代跑——原挂 20:21 一次性检查落在别会话工作区未触发)

- 20:05 PM 日报(run 8060):completed,push feishu_card ok=true(immediate=1),零失败;装机 config `bot: analyst` 出站(20:14 botswitch 备份链在证)=送达「AI信息分析师」✓。
- 三新源(b1684dfc):装机分区清单含三源名;今早 8:00 采集 run 6465 三源全活(edumails-nav 231/freellmapi 10/gpt4free 10);8:05 AM 日报(6474)分区实render 三源条目 ✓;PM 期分区空=三源 job 仅 0 8 排程的设计行为(窗口空哨兵注释 daily-digest.yaml:136)。明早 8:05 AM 为新包直接目验兜底。
- A1-A7 至此全过,档转收官态待主人归档。
