# 复审修复执行记录(2026-10-06,复审发现 14 条)

> 修复工程师档:medium/high 4 条全修;low 10 条中 6 条落地、4 条部分落地(其余
> 面记下方遗留)。全部定向测试亲跑绿(命令与结果见各条);一笔提交。

## 已修(定向验证亲跑)

1. **HIGH PLAYWRIGHT_BROWSERS_PATH sidecar 拿不到** → Python 侧自解析:
   `src/myssia/engines/crawl4ai.py` 新增 `ensure_playwright_browsers_env()`
   (谓词=用户已设原样尊重 > MYIA_HOME 在场且 `<MYIA_HOME>/playwright-browsers`
   目录在才 setdefault 注入),`_fetch_impl` fetch 前调用(L3 进程内);
   `src/myssia/engines/urlwatch.py` 渲染通道构 job 前调用(ShellJob shell=True
   继承,覆盖 render_crawl4ai 子进程);`_browser_failure` 误导 hint 改桌面态
   优先指引。验证:`uv run --no-sync pytest tests/engines/test_crawl4ai.py
   tests/engines/test_urlwatch_engine.py -q` → 102 passed, 2 skipped(新增
   TestEnsurePlaywrightBrowsersEnv 5 例 + 渲染通道 env 对齐 1 例)。
2. **MEDIUM pid_command_matches_service 无 Windows 实现** → 拆平台无关纯函数
   `command_line_matches_service`(三锚点判定)+ unix ps / windows
   PowerShell `Get-CimInstance Win32_Process` 双平台取 argv(powershell
   不可用/非零退出=复核不过,与 unix 同语义)。验证:`cargo test
   --manifest-path desktop/src-tauri/Cargo.toml pyenv_components` →
   30 passed; 0 failed(含新增跨平台纯函数测试)。
3. **MEDIUM 服务启动回包 healthy=false 无自动对账** → pyenv-card 前端轮询:
   回包 running+healthy=false 起 `SERVICE_HEALTH_POLL_INTERVAL_MS=5s` 轮询,
   上限 24 次(≈2 分钟)绿即停;回执文案同步如实(「本页每 5s 自动对账一次」)。
   验证:`npx vitest run src/screens/settings/pyenv-components.test.tsx` →
   20 passed(新增 fake-timers 轮询转绿即停 1 例)。
4. **MEDIUM zero-cost §5 docker compose 残留** → zh/en §5 照 §4 终裁口径改写:
   删 curl/docker compose up 命令块、colima 实测句、docker-in-VM 注记;改两条路
   (路①本机原生服务组件=设置→Python 运行环境→「关键词日报(SearXNG)」行;
   路②外部已部署实例,配方外链 docs.searxng.org 我方不复刻);末行交叉引用
   改指头注两条路说明。验证:`uv run --no-sync pytest tests/test_docs.py -q`
   → 110 passed。
5. **LOW searxng 403 文案** → 删「docker compose restart core」,改部署形态
   中立表述。验证:`uv run --no-sync pytest tests/engines/test_searxng_engine.py -q`
   → 20 passed;`grep -rn 'docker compose restart' src plugins` 零命中。
6. **LOW prd/design 数字与轨D行** → R4/决议②「8 件/8 处」回填「10 件/10 处」;
   design §1 轨 D 行改「上游部署配方 = 外链上游官方文档,仓库零携带(终裁②)」;
   design §4「8 件全删」→「10 件全删」。
7. **LOW firecrawl SELF_HOST 外链** → 五处 /blob/master/ → /blob/main/
   (README.md ×2、docs/zh+en zero-cost、plugins/myssia-firecrawl/README.md)。
   历史证据存档 .trellis/tasks/10-05-firecrawl-selfhost-verify/evidence/ 一处
   **刻意不改**(历史记录,改写有篡改档之嫌)。
8. **LOW secret.set 部分成功不披露** → 前端校验对齐后端(`^https?://\S+$`,
   「https://」空余部形态先拒零 IPC);secret.set 成功而 remote.save 被拒时
   note 披露「API 键已先行写入系统钥匙串(凭据面可见,secret 可删)」;
   dev 形态(remote_config_unavailable)保存预判禁用,部分成功在 dev 不发生。
9. **LOW setEndpoint 覆写草稿** → endpointDirty 标记(ref 读防回调换引用),
   载入应答不再覆写已改草稿;保存成功后回读回填刚保存值。
10. **LOW 探活过渡收窄** → `remoteDoctorProbe` 显式传 `probe_timeout: 5`
    (单次 GET 上限 10s→5s);按钮 title 如实「跑一次完整 doctor 取 firecrawl
    连通项(全量诊断…)」。
11. **LOW 反向闸注释** → service_start 前置注释改为「**单向前置**…反向暂未
    拦截,勿读作双向闭合护栏」。
12. **LOW 失管错误文案** → 「服务进程启动后即退出」补撞端口/失管孤儿提示与
    手工处理指引(端口值来自 svc.port)。
13. **LOW RemoteConfigPanel 按件区分** → 新增 `REMOTE_ENV_BRIDGE_IDS`(=1 的
    UI 镜像),回执/标题按件区分:非桥接件如实写「经品类 YAML 消费,暂无
    引擎 env 通道」。

前端三项验证:`npx tsc --noEmit` 零错;`npx vitest run
src/screens/settings/bundled-plugins-card.test.tsx` → 30 passed(新增部分
成功披露/dev 禁存/草稿防覆写 3 例 + 校验列表加「https://」)。
Python lint:`uv run --no-sync ruff check .` 与 CI 同命令绿
(CI 门禁=check 最小集,`ruff format --check` 非本仓门禁,存量格式差异不入)。

## 遗留(risks,未修部分如实记)

- **R-1 探活真修未做**(sidecar 轻量 `plugins.remote.probe {id}` 单项探活):
  `desktop/entry.py` 为并行任务(10-06-feed-channel-groups)未提交在途改动,
  按并行会话绕行铁律不动;过渡版(probe_timeout+如实 title)已落地。后续
  entry.py 空闲时补轻量方法即可替换。
- **R-2 桥接表双份硬编码**:`REMOTE_ENV_BRIDGE_IDS`(UI)与
  `_REMOTE_ENGINE_BRIDGE`(entry.py)两处,暂未经 bundled.list 面向 UI 暴露
  (同 R-1 原因绕行 entry.py);同步规约已写在常量注释,entry.py 增删件时必须
  双改。
- **R-3 服务运行中装组件的反向闸未加真闸**:仅注释如实化;真闸
  (ServiceManager.children 非空/跨会话孤儿戳 pid 复核 → 结构化拒)涉及
  生命周期语义与 UI 文案联动,触发面窄(UI 两开关不同行),留独立小档。
- **R-4 失管孤儿兜底发现未做**:start 撞端口/reconcile 无戳分支的端口探测
  (TcpStream::connect/lsof)与 write_service_stamp 失败上传回包字段均未做
  (涉及 IPC 回包 schema 变更);本轮仅错误文案补撞端口指引。
- **R-5 CLI 直跑(MYIA_HOME 未设)不注入浏览器 env**:刻意不复刻平台数据根
  解析进 src/myssia(防 entry.py/壳/引擎三处同源逻辑漂移);CLI 直跑开发者
  可显式设 MYIA_HOME 或 PLAYWRIGHT_BROWSERS_PATH。
- **R-6 Windows 实机验证缺位**:`pid_command_matches_service` windows 版
  (PowerShell Get-CimInstance)按语义实现且判定纯函数跨平台测试绿,但
  本机 darwin 无法亲跑 Windows 路径,需 Windows 实机验收。
- **R-7 pyenv-card 初拉镜像草稿的同款覆写窗口**(mount→IPC 应答)未动:
  本轮 pyenv-card 已带轮询改动,镜像草稿保护不扩面(既有 syncMirrors 机制
  的事件路径已护,初拉窗口极窄)。
