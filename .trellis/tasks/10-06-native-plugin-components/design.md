# Design:四轨管控模型 + 壳服务轨扩展

## 1. 四轨模型(全插件归面的目标态)

```
MYIA 管控面(壳 = 唯一控制者)
├── 轨 A 壳库组件   components.json {id, pip_spec, ...} → 装进自管 pyenv,进程内调用
│    既有:table、trafilatura;本档新增:crawl4ai(裁决③)、(searxng 若裁决④选 B 也走此轨)
├── 轨 B 壳服务组件  components.json 扩 {kind: service, start, health, port}(本档新增机制,裁决④选 A)
│    本档新增:searxng(8888,healthz);复用 pyenv 安装链装包 + 新增生命周期 IPC
├── 轨 C desktop 插件包  ~/.myia/plugins/<id>/(adapter.py+plugin.yaml)→ 壳按需装/版本钉
│    既有:urlwatch、maigret(+credhunter 等按 R1 总表逐件归入,零新机制)
└── 轨 D remote 声明    manifest modes.remote {endpoint}(cloud API / 主人服务器)
     既有:RSSHub/Zenrows/ScraperAPI 等;本档:firecrawl 归此轨(裁决①)
     上游部署配方 = 外链上游官方文档(SELF_HOST.md 等),仓库零携带(终裁②)
```

判别式(总表逐件过):需要本机常驻进程 → 轨 B;需要本机 py 库 → 轨 A;独立工具形态 adapter → 轨 C;纯 HTTP 消费外部服务 → 轨 D。四轨外 = 游离违例,清或废。

## 2. 轨 B 服务组件(唯一新机制,最小面)

- **声明**:`components.json` 条目扩可选字段 `kind: "service"` + `service: {start_cmd, health_url, port, stop_signal}`;缺 kind = 既有库组件,老消费端(宽容读取)零感知。
- **生命周期 IPC**(`pyenv_components.rs` 同文件扩,复用指纹/戳模式):
  - `service_start(id)` / `service_stop(id)`:tauri 侧 spawn/detach 子进程,状态落 `<数据根>/pyenv-components/<id>.service.json`(running/stopped/last_exit/started_at);
  - 健康面:`service_status(id)` 轮 health_url(复用既有 reqwest 依赖),设置卡绿点/按钮(启停语义照 python-env 卡判例 f333417:就绪检查状态·异常重试)。
- **进程托管取舍(G-Q5 定裁:手动启停+状态记忆)**:装好默认停;启停只走设置卡按钮;引擎侧 `searxng.py` 加 ensure 探测,跑源时未启动=结构化提示「服务组件未启动」并降级,**不隐式拉起**(隐式拉起=状态不可见,违背管控面透明)。
- **searxng 落地形状**:pip 装 searxng 进自管 pyenv;`<数据根>/services/searxng/settings.yml` 由壳生成(`use_default_settings: true` + `formats: [html, json]` + 随机 secret_key——searxng.yaml:12-17 两行关键覆盖的机器化);start_cmd = pyenv python -m searx.webserver;health = /healthz。

## 3. 轨 A:crawl4ai 组件(裁决③推荐形态)

- `components.json` 新行 `{id: "crawl4ai", pip_spec: "crawl4ai>=…"}`;安装链复用既有 pip 段。**description 明示体积与落点(G-Q6 定裁)**:chromium ~300MB 级下载、PLAYWRIGHT_BROWSERS_PATH 落数据根、卸载组件即整目录消;searxng 组件行同理标注。
- **playwright 浏览器链**:crawl4ai 首跑需浏览器二进制——组件安装后钩子跑 `playwright install chromium`(装进自管 pyenv 的 PLAYWRIGHT_BROWSERS_PATH,数据根下,卸载组件即整目录消);失败=组件戳 error 态(既有 error 卡形态),不静默。
- 既有 `plugins/myssia-urlwatch/render_crawl4ai.py` 场景件消费路径不变(它跑在自管 pyenv 里,组件装好即 dependency_missing→ready)。

## 4. 轨 D:remote 声明(firecrawl 归面)+ docker 模式全删(主人终裁)

- **firecrawl 市场桩(G-Q1 定裁)**:新建 `plugins/myssia-firecrawl/plugin.yaml`(tier: remote,`modes.remote.endpoint`,无 adapter,零运行时)——设置页轨D 配置面板的挂点,RSSHub 桩同款先例;官方插件声明面新增必同步 golden 基件(games v2 判例)。
- 市场声明:manifest(或 ai-news.yaml 注释态源)统一 `modes.remote.endpoint`;firecrawl 端点由配置面板写入(云端或主人自有服务器,endpoint http(s) 字面或 env 引用按既有解析);doctor 加连通项(未配=「未配置」不红)。
- **仓库不再携带任何插件 compose 配方**:`docker/plugins/*` 10 件全删;上游部署属主人运维,文档只留外链(上游官方 SELF_HOST.md / RSSHub 官方 docs),我方不复刻步骤。
- 引擎零改动(10-05 已证 cloud/self-host drop-in)。

## 4b. schema 手术(docker 模式删除的精确边界)

- `PluginLocalModeConfig`:**删 `compose` 字段**,保留 `install`(原生安装命令,credhunter 先例);docstring「本机 Docker compose 交付」改「原生安装命令」;`_check_has_content` 校验只剩 install 一路。
- `REQUIRES_TOKENS = ("docker",)` → `()`(机制保留词表空,未来新 token 零阻力);schema.py:25 的 v1.7「双模式 local docker compose / remote」描述同步改写。
- 删除面已核零迁移:`compose:` 与 `requires: docker` 在 32 件 manifest 中零使用(grep 实证 2026-10-06);已发布市场 manifest 无受影响者。
- 测试面:test_media_plugin / test_plugins_system / test_plugin_packages 的 compose fixtures 改 install 形态或删;docs 测试同步。

## 5. 兼容与回滚

- components.json 扩字段:老版本壳读新文件仅多忽略字段(zod/serde 宽容读取既有);回滚=删新行。
- ~~schema local-docker 保留字段~~ **已翻案(主人终裁)**:compose 字段直接删;零 manifest 在用=已发布面零破,回滚=git revert 单提交。
- 壳 IPC 新增命令:加法不改老命令,回滚=UI 不渲染即零行为差(components 空数组先例 pyenv_components.rs:23)。
- 每轨独立提交,阶段间可停(见 implement.md 回滚点)。

## 6. 设置页统一操控面(R7;复用既有卡,不新开屏——版面判例 38acd34)

| 轨 | UI 落点 | 现状 → 动作 |
|---|---|---|
| A 库组件 | pyenv-card 组件行(table/trafilatura 先例) | 既有面,crawl4ai 进注册表即自动出行 |
| B 服务组件 | 同卡组件行扩 kind:service 形态(启停按钮+健康绿点,语义照 python-env 就绪检查判例 f333417) | 本档新增(阶段 2) |
| C desktop 插件包 | bundled-plugins-card(装/卸/品类平铺装,批二 R2/R3 交付面) | **既有,零改** |
| D remote 声明 | bundled-plugins-card 条目详情区**新增**:endpoint 输入 + 凭据写钥匙串(sidecar `myssia secret set` 同门,UI 不碰明文)+ doctor 探活按钮 | 本档新增(阶段 3) |

轨D 数据面:remote 配置落数据根插件配置(`modes.remote.endpoint` 用户值 + token 钥匙串引用),与 schema 校验(keychain-only 判例)同规;firecrawl 的 `MYIA_FIRECRAWL_URL` 桌面态改由该面板提供(写数据根配置,sidecar 读,env 仍作开发后门但桌面不依赖)。

## 7. 明确不做

- 不 vendor AGPL 服务源码(firecrawl/RSSHub 判例);不引入 Node 运行时自管(裁决① remote-only);不做市场外「手工安装」入口(那正是违例根源);不动 10-05-firecrawl-selfhost-verify 档(review 态)。
