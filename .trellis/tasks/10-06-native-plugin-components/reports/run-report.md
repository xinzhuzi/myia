# 交付报告:插件全量受管——管控面原生组件化收编(本机零 Docker)

> 任务档:`.trellis/tasks/10-06-native-plugin-components/` · 收尾轮:2026-10-06 晚 · HEAD=5345efe
> 执行流:动态工作流四阶段实施 → 全量门禁 → 四视角复审+修复 → 多流程实测 → 装机包验证 → 收尾对账(本报告)。
> 纪律口径:本报告区分「收尾轮亲跑」与「阶段轮回执」;凡未亲跑的均标注来源,不冒认。

## 0. 地面对账(收尾轮亲跑)

- `git log --oneline -25` 亲跑,本任务七笔全在:
  | 阶段 | commit | 摘要 |
  |---|---|---|
  | 阶段4a | `1214c79` | 插件 docker 模式全删(schema compose 侧/词表清空/docker-plugins 10 配方整删) |
  | 阶段4b | `421e039` | 插件 docker 交付口径全仓清零(10 处 manifest 注释/12 件 README 改写,firecrawl 配方改一句话外链) |
  | 阶段1 | `762b55c` | crawl4ai 进壳组件轨(轨A:注册表+playwright-chromium 钩子+G-Q6 体积披露) |
  | 阶段2 | `1b9c5c3` | searxng 壳服务组件轨(轨B:kind:service+三 IPC+granian 服务端+进程组托管+G-Q5 手动启停) |
  | 阶段3 | `7e20e28` | firecrawl 归面 remote 轨(轨D:市场桩+remote 配置面板+doctor 连通项) |
  | 复审修复 | `c1eccc9` | 四视角复审 14 条发现落地(高/中 4 全修+低 9);任务档 prd/design/review-fixes 随此笔首次入库 |
  | 收尾 | 本笔 | AC 勾选/spec 三处更新/本报告/任务档补提交 |
- 工作树残留:`git status` 亲查,本任务**源码/测试零未提交残留**(变更全在各阶段 commit 内);未跟踪件均为任务档自身(jsonl/evidence/implement.md/plugin-matrix.md/task.json),随本笔入库。
- 执行顺序实录:阶段4 → 阶段1 → 阶段2 → 阶段3 → 复审修复 → 装机验证(19:43-20:18)→ 收尾(编号非执行序,各阶段独立提交互不依赖)。
- 如实记:implement.jsonl / check.jsonl 为 0 字节(建档时直改 task.json 绕过 CLI start,task.json notes 已记该既成事实;同款先例 929553f telegram 档曾事后补策展)。收尾轮未获补条指示,不代跑,记此留痕。

## 1. 四阶段摘要

1. **阶段4 docker 模式全删(主人终裁②,先行)**:`PluginLocalModeConfig.compose` 字段删(install 保留)、`REQUIRES_TOKENS` 词表空(schema.py:250)、`docker/plugins/` 10 配方整删、10 处 manifest 注释改「任意已部署实例按 remote 接入」、searxng.yaml 头部 docker 三步退役、zero-cost §4 改一句话外链上游 SELF_HOST、tests 三件 fixtures 改形;产品自身 server 形态(根 `Dockerfile` + `docker/docker-compose.yml` + env.example)保留未动。
2. **阶段1 轨A crawl4ai 组件化(裁决③)**:components.json 钉窗行(>=0.9,<0.10)+post_install playwright-chromium 钩子(浏览器落数据根 playwright-browsers/,卸载即整目录消)+G-Q6 体积披露(下载 300MB 级/落盘 557MB 实测)+失败=组件戳 error 可见;sidecar 运行时按目录在场注入 PLAYWRIGHT_BROWSERS_PATH。门禁:Rust 14/14+全套 64/64、pytest 26/26、ruff、vitest 10/10、tsc;真网冒烟全链(venv→pip→chromium→quotes.toscrape.com/js 真渲染 exit0,沙箱 1.2G 已整目录回收)。
3. **阶段2 轨B searxng 服务组件(裁决④+G-Q5/G-Q6)**:components.json 扩 kind:service + service_start/stop/status 三 IPC + 状态戳记忆 + settings.yml 生成器(use_default_settings+formats json+随机 secret);服务端=granian(上游实测 searx.webserver 已移除)+进程组托管(SIGTERM 组→宽限→SIGKILL,孙进程树整组零残留,跨壳重启孤儿三锚点身份复核);装好默认停、启停只走设置卡、引擎 /healthz 就绪探测未启动=结构化提示不隐式拉起;searxng 真身不在 PyPI,两段装(git 钉 commit d48c4b555 + --no-build-isolation);门禁:Rust 29/29+全套 79/79、引擎域 20/20+desktop 契约 29/29、vitest 541/541、tsc/build;真网真跑(healthz 200→json 真查询 67 条→组停 exit0→端口释放+ps 零残留)。
4. **阶段3 轨D firecrawl 归面(裁决①+G-Q1+R7)**:`plugins/myssia-firecrawl` 市场桩(tier:remote,modes.remote.endpoint,零 adapter,AGPL 只声明不 vendor)+golden 基件同步;sidecar `plugins.remote.get/save` 两方法(注册表 #67-68,协议不 bump 循 bundled 族先例)+`_startup_remote_env` env 桥接(MYIA_FIRECRAWL_URL/API_KEY,显式 env 恒优先)+doctor `firecrawl` 键(未配置不红);设置页 remote 配置面板(endpoint 输入+凭据写钥匙串走 secret.set 同门+探活按钮);文档三处外链上游官方。门禁:pytest doctor 域+vitest+docs 全绿。
5. **复审修复(c1eccc9,四视角 14 条)**:见 §3。

## 2. 全量门禁结果

**收尾轮亲跑(当前 HEAD=5345efe,2026-10-06 20:23-20:31)**:

| 门禁 | 命令 | 结果 |
|---|---|---|
| pytest 全量 | `uv run --no-sync pytest tests/ -q` | **4729 passed, 40 skipped,EXIT=0**(116s;docs 测试 test_docs.py 含在内) |
| vitest | `cd desktop/ui-src && npx vitest run` | **26 文件 570 passed,EXIT=0** |
| tsc | `cd desktop/ui-src && npx tsc --noEmit` | **EXIT=0** 零错 |
| build | `npm run build`(desktop,转发 ui-src) | **EXIT=0**(✓ built in 1.71s) |
| cargo 壳组件域 | `cargo test --manifest-path desktop/src-tauri/Cargo.toml pyenv_components` | **30 passed, 0 failed, 1 ignored** |
| ruff | `uv run --no-sync ruff check .` | **All checks passed,EXIT=0** |

- 首跑教训如实记:tsc/vitest 我先在 `desktop/` 根跑错目录(UI 工程实在 `desktop/ui-src/`)得到无效结果,重跑修正;上表为有效轮。
- 工作流轮回执(/tmp/myia-gate-*.log,19:26-19:36 时点树):vitest 570p EXIT=0;pytest 首跑 **7 failed**(全为 tests/telegram/test_telegram_serve.py,时点工作树带 telegram 并行在途改动,非本任务域)→ 全量重跑两轮均 **4711 passed/40 skipped EXIT=0**。收尾轮 4729 与之差额=其后并行任务(telegram/feed)新增测试,如实说明。

## 3. 复审发现与处置(14 条,c1eccc9)

高/中 4 条全修:①HIGH PLAYWRIGHT_BROWSERS_PATH sidecar 拿不到→Python 侧自解析 `ensure_playwright_browsers_env`(crawl4ai+urlwatch 渲染通道双挂,102 passed 定向);②MEDIUM pid 复核无 Windows 实现→拆跨平台纯函数+PowerShell 取 argv(30 passed);③MEDIUM 服务启动回包 healthy=false 无对账→前端 5s 轮询上限 24 次转绿即停(20 passed);④MEDIUM zero-cost §5 docker compose 残留→照终裁口径改两条路(110 passed)。低 9 条落地(403 文案/prd 数字/SELF_HOST 外链 /blob/main/ 五处/secret.set 部分成功披露/草稿防覆写/探活收窄/反向闸注释/失管文案/RemoteConfigPanel 按件区分)。全清单与定向验证命令:`research/review-fixes.md`。**遗留 R-1~R-7 见 §6**。

## 4. 五流程结果

如实声明:工作流内部「多流程实测」段的原始回执对本收尾代理不可达(工作流 introspection 不可用;evidence/、journal、/tmp 均无五流程具名回执)。收尾轮**亲跑五条实流程**覆盖同一产品面(全部 temp MYIA_HOME + `myssia test` :memory: 试抓,零持久化零推送,静默无 GUI):

| # | 流程 | 命令要点 | 结果 |
|---|---|---|---|
| 1 | doctor 零配置流 | `MYIA_HOME=<temp> myssia doctor --json` | 结构化全键;`firecrawl` 键 = `{configured:false, endpoint_display:null, api_key_configured:false, probe:null}`,findings **零 firecrawl 红条**(未配置≠红,判例落地) |
| 2 | 真源采集流 | `myssia test plugins/myssia-demo.yaml` | GitHub API 真抓 **30 条,状态 success,exit 0** |
| 3 | searxng 引擎流 | `myssia test plugins/searxng.yaml --source searxng-watch` | 结构化失败 `http_502`(环境注:本机 clash TUN 对死回环端口回 502 空应答——httpx 直探实证,环境属性非代码缺陷;引擎「任何 HTTP 应答=实例在」语义正确放行);**loopback 拒连分支由单测钉死**(tests/engines/test_searxng_engine.py:389-404 断言 searxng_service_not_running,20 passed 亲跑);跑后 pgrep 零 granian/searxng 残留(不隐式拉起实证) |
| 4 | firecrawl remote 降级流 | `MYIA_FIRECRAWL_URL=http://127.0.0.1:9 myssia test <temp yaml>` | 引擎消费 `endpoint=env:MYIA_FIRECRAWL_URL`(api_key=未配置)→结构化 `http_502` + 四引擎 attempts 账本逐条在案 + 降级链干净收场 exit 2 不崩(死服务优雅降级契约) |
| 5 | crawl4ai 渲染流 | `myssia test <temp yaml>`(quotes.toscrape.com/js) | `采集成功 engine=crawl4ai items=1`,真渲染内容在案("The world as we have created it…"),状态 success,exit 0(约 9s) |

## 5. 装机证据清单(evidence/,装机验证轮 19:43-20:18 产出 + 收尾轮亲验)

| 件 | 内容 |
|---|---|
| `ac8-grep.txt` | AC8 终验:净室(git archive HEAD@b7a45e8)与装机件(/Applications/世事.app,本日换装 sha f7328027…)双验;八节 grep + 判读结论(插件面零命中/词表空/docker-plugins 不存在/白名单=产品 server 形态+任务历史档) |
| `pkg-pyenv-components.png` + `-vl.txt` | 物理窗截图+local-ocr 转录:设置→Python 运行环境 组件卡(table 已装,开关开;无重叠/溢出,一行底部截断如实记) |
| `pkg-pyenv-components-shim.png` + `-vl.txt` | 装机包自身 UI dist+真侧车无头全卡(物理 1050pt 装不下四行,pyenv_get_status 为 shim 伪造、组件态镜像生产根实况,**如实标注**;bundled 面零伪造):四组件行全可见(表格还原 已装/正文抽取兜底 未装/JS 渲染抓取 crawl4ai 未装/关键词日报 SearXNG 未装),无重叠/溢出/截断 |
| `pkg-bundled-firecrawl.png` + `-vl.txt` | 物理窗截图+转录:随包官方插件件卡 firecrawl 条目(tier remote 未装)+**轨D remote 配置面板全要素**(端点输入+API 键入钥匙串+保存配置+探活+keychain 零明文注记),真 sidecar 数据 |
| `pkg-smoke-newpkg-sandbox.png` | 新包 MYIA_SMOKE_GEOMETRY 小窗无焦点冒烟(静默铁律) |

时间线重构(收尾轮对 /tmp 工件):build12.log 19:43-19:50 重打包 → 19:52 净室导出 → 19:55-19:57 新包沙箱冒烟 → 19:59-20:07 物理窗截图链(shot-chain.sh)→ 20:11-20:16 shim 无头全卡 → 20:17-20:18 local-ocr 转录落 evidence。
**收尾轮装机件亲验**(直接读 /Applications/世事.app):Resources/components.json 四行齐(crawl4ai 带 playwright-chromium 钩子与体积披露;searxng kind:service/granian/healthz/G-Q6 披露);plugins/myssia-firecrawl 桩在(AGPL 只声明注记);myssia-src/myssia/schema.py:250 `REQUIRES_TOKENS = ()`;plugins/ `compose:` 零命中;pgrep firecrawl/granian 零进程(AC4 零残留亲验)。
小勘误:ac8-grep.txt [6] 节行文写「docker/Dockerfile」,实际 Dockerfile 在**仓库根**(docker/ 下仅 README/docker-compose.yml/env.example——该节自身 ls 输出即如此),收尾轮亲验,不遮不掩。

## 6. 遗留与留主人事项

**review-fixes 遗留(R-1~R-7,处置与理由全文见 research/review-fixes.md §遗留)**:
- R-1 探活真修未做(sidecar 轻量 `plugins.remote.probe` 单项探活;过渡版 probe_timeout=5+如实 title 已落地;entry.py 彼时为并行任务在途,绕行铁律未动)
- R-2 桥接表双份硬编码(UI `REMOTE_ENV_BRIDGE_IDS` ↔ entry.py `_REMOTE_ENGINE_BRIDGE`,同步规约在注释,增删件必须双改)
- R-3 服务运行中装组件反向闸未加真闸(触发面窄,留独立小档)
- R-4 失管孤儿兜底发现未做(端口探测/回包上传字段,涉 IPC 回包 schema)
- R-5 CLI 直跑(MYIA_HOME 未设)不注入浏览器 env(刻意防三处同源逻辑漂移;开发者显式设 env 即可)
- R-6 Windows 实机验证缺位(跨平台判定纯函数已测,需 Windows 实机验收)
- R-7 pyenv-card 初拉镜像草稿覆写窗口未动(既有 syncMirrors 事件路径已护)

**收尾轮新增**:
- 五流程原始回执不可达(§4 已声明;收尾轮五条替代覆盖同一产品面,后续工作流宜把具名回执落 evidence/)
- searxng 生产部署复验留主人服务器(源级 searxng_base_url 指过去即接,配方见上游官方文档;10-05-source-searxng research §9-5 同款口径)
- implement.jsonl/check.jsonl 0 字节既成事实(§0;是否补策展循 929553f 先例由主人定)
- 装机件 20:19 起 telegram 并行任务又做过装机外科(/tmp/myssia-b3desktop-backup-20261006-201905 在案),不属本档,未动未验

**spec 更新(本笔)**:
- `.trellis/spec/domain/connector-selection.md`:硬规则新增「插件一律本机原生运行,零 docker 模式」(判例 2026-10-06,四轨模型+产品 server 形态边界)
- `.trellis/spec/domain/security-baseline.md`:Plugin 节 compose 条款随 docker 模式删除归档,补 remote 面板凭据零明文一句
- `.trellis/spec/desktop/sidecar-protocol.md`:注册表计数纠偏 66→68(阶段3 已加 #67-68 行与批注但头部计数漏更;AST 亲验 `_HANDLERS`=68)

## 7. AC 勾选对照

AC1-AC9 全勾(prd.md),逐条依据:AC1=plugin-matrix.md(20+14+12 行零游离,收尾轮通读);AC2=1b9c5c3 真跑回执+单测 20 例+装机行(shim)+flow3;AC3=762b55c 真渲染回执+flow5 真跑+装机 components.json;AC4=装机桩+doctor 键(flow1)+文档三处+pgrep 零进程;AC5=收尾轮 grep(净树+装机件 compose: 零命中/docker-plugins 不存在/词表空/产品形态保留);AC6=§2 六路亲跑;AC7=§5 证据链+装机件亲验;AC8=收尾轮 grep(产品交付面 14 命中全数白名单类+装机件唯一命中=删除说明 docstring)+evidence/ac8-grep.txt;AC9=轨A 物理窗(table 装开关已装态)+轨B vitest 启停/绿点契约(20 例,程序化判例 e11d726「写程序测试,不是控制电脑」)+装机行+轨C bundled 卡真侧车渲染+vitest 30 例+轨D 物理窗面板全要素+vitest——桌面路径零 CLI 依赖。
