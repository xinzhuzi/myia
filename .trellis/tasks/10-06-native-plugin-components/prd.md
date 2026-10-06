# PRD:插件全量受管——MYIA 管控面原生组件化收编(本机零 Docker)

> 立档:2026-10-06 · 来源:主人两道判例令(对话链:沙箱/磁盘排查 → Docker 栈清理回收 20G → firecrawl 归属对齐 →「MYIA 控制**所有**插件,你不理解这个概念吗?」「立项做,使用 trellis,包括其他几个插件」)
> 类型:架构收编 + 组件工程,单档多 scope(逐件独立可验) · 状态:planning,待 grill 定裁后 start

## 概念不变量(主人判例,本档宪法,一切设计服从)

1. **MYIA 控制所有插件**:一个插件/引擎要么在 MYIA 管控面内(声明 → 安装/启停/健康/卸载全走 app),要么不存在。游离在外的手工资产 = 违例(判例:firecrawl Docker 栈无主白占 21G,2026-10-06 已清)。
2. **本机零 Docker**:所有插件在本机原生运行;插件不提供 docker 模式(终裁见 §决议②)。
3. **管控面的唯一入口 = 设置页 UI**(主人追加令 2026-10-06「设置里面下载这些插件,给UI配置才对」):下载/安装/卸载、启停(服务)、remote 端点与凭据配置、健康状态,全部在设置屏操作;不开 CLI/手工 YAML 后门给桌面用户。
4. 与桌面自管 py 环境判例同源(2026-10-05):组件按需装,包体不冻结运行时。

## 证据矩阵:管控面现状(2026-10-06 亲核,引用即已核勿重探)

| 层 | 现状 | 证据 |
|---|---|---|
| 壳组件面 | **机制就绪、存量仅 2**:`components.json` `{id,pip_spec,label,description}` ×2(table/trafilatura)+ 安装戳 `pyenv-components/<id>.json` + `pyenv_install_component` IPC + 设置页组件卡 | `desktop/resources/components.json`;`desktop/src-tauri/src/pyenv_components.rs`(宽容读取,扩 id 不破老装) |
| desktop 插件包轨 | 已受管先例:myssia-urlwatch、myssia-maigret(adapter.py+plugin.yaml,装 `~/.myia/plugins/`) | `ls ~/.myia/plugins/` |
| 引擎适配器 | 17 个,全为客户端(纯 httpx/进程内),本身合规;缺的是**服务端/运行时归面** | `src/myssia/engines/` |
| 官方件 | `plugins/` 32 件,tier 三态(desktop/remote/docker 型桩),待逐一归面 | `plugins/`、`plugins/myssia-*/plugin.yaml` |
| Docker 栈 | **已拆**:colima delete + 孤儿盘清除,回收 20G(926G 盘 86%→84%);10-05-firecrawl-selfhost-verify 的「复验留存镜像 5.2GB」随主人清理令同灭 | 本机 df 实测;该档 task.json 回执三 |
| 违例存量 | ①`plugins/searxng.yaml` 头部「本机 docker 起栈三步」指引(与新令冲突)②crawl4ai 装机态 `dependency_missing`(desktop lock extras 裁定悬置,llm 先例)③schema v1.7 plugin 双模式的 local docker compose 侧 | searxng.yaml:1-25;ai-news-sources 档 bc6dece;schema.py:1540-1600 |

**相邻任务关系**:`10-05-firecrawl-selfhost-verify`(review 态,不动)=本机 docker 真跑验证已毕+服务器部署指引已交付;其**本机路径被本档取代**(禁 Docker 令),其 remote/服务器配方被本档 R3 吸收复用。

## Requirements

- **R1 全清单归面**:**已完成(grill 轮)**——20 插件包 + 12 品类 YAML + 14 引擎适配器逐一落表 `research/plugin-matrix.md`,零「游离」项。grill 新发现:①`server-only` 第三种 tier 存在(douyin/maxun)②gate 词汇含 platform/stale(snownlp 挂 stale)③**firecrawl 引擎无市场条目,轨D 配置面板无挂点**(G-Q1)④注释 recipe 引用 10 处、docker/plugins/ 配方 10 件(一一对应)。
- **R2 原生组件实做**:searxng、crawl4ai 两件落地(载体与形态遵裁决①③④),装机态真跑真源;安装戳/设置卡/doctor 全走既有面,不新造第二套机制。
- **R3 firecrawl 归面(remote 轨)**:本机不装 Node 服务端;市场声明 + doctor 连通项 + 文档三处一致指向 cloud env / 主人服务器 URL;缺省未配 = 降级链既有行为不变(firecrawl.py 契约:dead service degrades cleanly)。
- **R4 插件 docker 模式全删(主人终裁)**:schema compose 侧删除(install 原生安装保留)+ docker 词表退役 + `docker/plugins/*` 10 件配方删除 + manifest 注释改写 + searxng.yaml 头部本机 docker 指引退役 + `docker/README.md` 拆节;产品自身 server 形态(Dockerfile/docker-compose.yml)不属插件面,保留。
- **R5 零 Docker 终验**:装机包/数据根/启动链全 grep 无本机 docker 拉起路径;zh/en 文档口径同步。
- **R6 交付判例**:门禁全绿 + 装机包刷新 + 静默换装 + 像素级装机验证(交付含装机包判例 + 静默铁律)。
- **R7 设置页统一操控面(主人追加令)**:四轨全部在设置 UI 可操——轨A 组件行装/卸(pyenv 组件卡,既有面)、轨B 服务行启停+健康点(本档新增)、轨C 随包件装/卸(bundled-plugins 卡,批二既有面)、**轨D remote 配置面板(新增:每 remote 插件详情区 = endpoint 输入 + 凭据写钥匙串(走 sidecar `myssia secret set` 同门)+ doctor 探活按钮)**;桌面用户零 CLI、零手工 YAML。

## Acceptance Criteria

- [ ] AC1 归面总表在档:全插件 ×(旧形态/新形态/动作/验证法),零游离项
- [ ] AC2 searxng 原生通路:装机态真源 json 查询真跑通,状态在设置卡/doctor 可见
- [ ] AC3 crawl4ai 收编:装机态 render 链真跑,`dependency_missing` 消除
- [ ] AC4 firecrawl remote 归面:市场/doctor/文档三处一致,本机零 Node 服务端、零进程残留
- [ ] AC5 插件 docker 模式全删落地:schema compose 侧/词表/配方/注释/文档五处一致,`grep -r 'compose:' plugins/` 零命中、`docker/plugins/` 目录不存在;产品 server 形态保留未动
- [ ] AC6 门禁:pytest / vitest / tsc / build / docs 全绿
- [ ] AC7 装机包刷新 + 静默换装 + 像素级验证(doctor/组件卡截图证据,local-ocr 链)
- [ ] AC8 零 Docker 终验:全仓 + 装机件 grep 无本机 docker 启动路径(服务器配方除外,语义已改)
- [ ] AC9 设置页四轨可操:轨A/B/C/D 各至少一件在装机 UI 亲验(装/卸/启停/remote 配置+探活),像素证据并入 AC7;桌面路径零 CLI 依赖

## 决议(2026-10-06 主人终裁,原 grill 五问)

1. **firecrawl 本机形态 → remote-only 定案**(由决议②推定:docker 模式全删后自托管只剩官方云 env / 主人自有服务器 URL,引擎零改动消费,10-05 已证)。
2. **插件 docker 模式 → 全删(主人原话「插件都不要docker模式」,比原推荐更彻底)**:schema `PluginLocalModeConfig.compose` 字段删除(`install` 原生安装命令保留——credhunter 在用,是合规原生形态);`REQUIRES_TOKENS` 的 docker 词退役(词表空);`docker/plugins/*` 10 件 compose 配方删除;10 处 plugin.yaml 注释里「服务端部署 compose 在仓库 docker/plugins/…」改写为「任意已部署实例按 remote 接入」;`docker/README.md` 拆节(**产品自身 server 形态 `docker/docker-compose.yml`+`Dockerfile` 不属插件面,保留**)。删除面已核干净:`compose:` 字段与 `requires: docker` 今天零 manifest 在用(grep 实证)= 零迁移。
3. **crawl4ai 载体 → components.json 组件轨**(依概念定稿,可翻案;备选 lock extras)。
4. **searxng 服务形态 → 壳服务轨 A**(依概念定稿,可翻案;真·MYIA 控制,唯一新机制)。
5. **文档清扫 → 全翻**:zh/en 里插件 docker 交付口径零残留;zero-cost §4 的 firecrawl 自托管 compose 步骤**改为一句话外链上游官方 SELF_HOST.md**(上游自身文档不属我方插件模式;我方不复刻配方)。

### grill 第二轮决议(2026-10-06 主人令「按照你的推荐」,逐件过一遍产物见 research/plugin-matrix.md)

6. **G-Q1 → firecrawl 市场桩化**:新建 `plugins/myssia-firecrawl` 桩(tier: remote,`modes.remote.endpoint` 声明,无 adapter,零运行时)——轨D 设置页配置面板的挂点;RSSHub 桩同款先例;官方插件声明面新增必同步 golden 基件(games v2 判例)。
7. **G-Q2 → server-only tier 词汇保留**(douyin/maxun 如实反映上游形态,零迁移,消费面同轨D)。
8. **G-Q3 → snownlp stale 闸维持现状**(市场 UI 已示警;退役属独立产品决策不混本档)。
9. **G-Q4 → scrapling 维持 extras+doctor 提示**(装机真实使用发生再平移组件轨;一档不摊大饼)。
10. **G-Q5 → searxng 服务手动启停+状态记忆**(装好默认停;引擎跑源未启动=结构化提示,不隐式拉起;管控面透明判例)。
11. **G-Q6 → 组件体积披露**:crawl4ai/searxng 组件 description 明示下载体积(chromium ~300MB 级)+落点(数据根)+卸载即整目录消(主人磁盘敏感,本轮任务起因)。

## 既有事实(引用即已核)

- urlwatch/maigret = desktop 插件包先例;table/trafilatura = 壳组件先例;RSSHub = remote 桩先例(AGPL 只桩不抄判例,firecrawl 同判例)
- 公共 searxng 实例 robots 明禁 API(searxng.yaml:5-6),只走自托管
- firecrawl 引擎契约:cloud/self-host drop-in,endpoint 三级解析,服务死=优雅降级(firecrawl.py docstring)
- Docker Desktop 本就卸载(10-05 探针在案);colima 已删(2026-10-06)
