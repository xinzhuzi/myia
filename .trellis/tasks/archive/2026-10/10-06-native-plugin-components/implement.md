# Implement:分阶段执行计划

> 前置:grill 五问定裁(prd §待裁决)回写后 start;每阶段独立提交,门禁绿才进下一阶段。

## 阶段 0 定裁与总表(research 产物)

- [x] grill 定裁:主人终裁已回写 prd §决议(②全删 docker 模式;①⑤随之定案;③④依概念定稿可翻案)
- [x] R1 归面总表:`research/plugin-matrix.md`——20 插件包+12 品类 YAML+14 引擎逐行,零游离项(2026-10-06 grill 轮,脚本抽取非手抄)
- [x] grill 第二轮 G-Q1~Q6 定裁回写(主人令「按照你的推荐」:firecrawl 市场桩/server-only 保留/snownlp 维持/scrapling 维持 extras/searxng 手动启停+状态记忆/体积披露——prd §决议 6-11)
- 回滚点:纯文档,无

## 阶段 1 轨 A:crawl4ai 组件化(裁决③)

- [x] `desktop/resources/components.json` 加 crawl4ai 行;安装链带 playwright 浏览器钩子(PLAYWRIGHT_BROWSERS_PATH 落数据根);**description 明示体积/落点/卸载即消(G-Q6)**
- [x] 壳侧测试:组件注册/安装戳/失败态(Rust 单测 + 既有组件测试同款)
- [x] 装机态真跑:render_crawl4ai 场景件走一遍 JS 站(判例站 quotes.toscrape.com/js)
- [x] 门禁:定向 pytest(desktop 组件域)+ cargo test pyenv_components + ruff
- 回滚点:删 components.json 新行即回旧态

## 阶段 2 轨 B:searxng 服务组件(裁决④=A 时)

- [x] `pyenv_components.rs` 扩 kind:service + service_start/stop/status IPC + 状态文件;settings.yml 生成器(两行关键覆盖机器化+随机 secret)
- [x] 设置卡:服务组件行(启停按钮+健康绿点,照 python-env 卡语义)
- [x] 引擎侧:searxng.py ensure 探测+未启动结构化降级(不隐式拉起)
- [x] 装机态真跑:searxng 组件起服务→ ai-news 或专用 searxng 源 json 查询真跑→ 停服务零残留进程
- [x] 门禁:cargo test + vitest(设置卡)+ pytest(引擎域)+ tsc/build
- 回滚点:IPC 加法+UI 不渲染即零行为差;组件行删除即回旧态

## 阶段 3 轨 D:firecrawl 市场桩 + remote 归面 + remote 配置面板(裁决① + G-Q1 + R7)

- [x] **firecrawl 市场桩**:`plugins/myssia-firecrawl/plugin.yaml`(tier: remote,零 adapter)+ golden 基件同步(games v2 判例)+ bundled 卡出现该条目验证
- [x] doctor 连通项(未配置≠红;配置了探活);市场/注释态源声明统一 remote 面板来源
- [x] **轨D remote 配置面板**:bundled-plugins-card 条目详情区(endpoint 输入 + 凭据写钥匙串走 sidecar `myssia secret set` 同门 + doctor 探活按钮);vitest 覆盖(含 keychain-only 校验联动)
- [x] sidecar 数据面:remote 配置读写(数据根插件配置),firecrawl 桌面态由面板供端点(env 留开发后门)
- [x] 文档:README/zero-cost 引用上游官方文档外链(10-05 档产物改口径)
- [x] 门禁:pytest doctor 域 + vitest + docs 测试
- 回滚点:doctor 项/面板均为加法,零破

## 阶段 4 docker 模式全删 + 文档清扫(主人终裁②⑤)

- [x] schema:`PluginLocalModeConfig.compose` 删、docstring 改、`REQUIRES_TOKENS` → 空词表(:25/:236/:1537 同步)
- [x] `docker/plugins/` 10 件 compose 配方整目录删除(实数,见 plugin-matrix);`docker/README.md` 拆节(产品 server 形态节保留)
- [x] 10 处 plugin.yaml 注释「服务端部署 compose 在仓库 docker/plugins/…」改「任意已部署实例按 remote 接入」(清单见 plugin-matrix)
- [x] searxng.yaml 头部本机 docker 三步段退役;zero-cost §4 复刻的 compose 步骤改一句话外链(上游官方文档)
- [x] tests 三件 compose fixtures 改形/删(test_media_plugin / test_plugins_system / test_plugin_packages)
- [x] zh/en 文档全扫:插件 docker 交付口径零残留;AC5 grep 三验(compose:/docker-plugins 目录/插件面 docker 字样)
- [x] 门禁:全量 pytest + vitest + tsc + build
- 回滚点:schema+配方删除各自独立提交,git revert 单提交可回

## 阶段 5 收官(交付判例)

- [x] 全量门禁亲跑绿(pytest/vitest/tsc/build/docs)
- [x] 装机包重打包 → 静默换装(MYIA_SMOKE_GEOMETRY 小窗铁律)→ 像素级验证:设置卡组件行/searxng 启停/doctor 三截图过 local-ocr 链
- [x] AC8 零 Docker 终验 grep(全仓+装机件;服务器配方白名单)
- [x] 勾 AC、spec 更新(trellis-update-spec:connector-selection 加「插件不跑 Docker」硬规则)、收尾提交

## 验证命令速查

```bash
uv run --no-sync pytest tests/ -q            # 全量(python)
cd desktop && npx tsc --noEmit && npm run build && npx vitest run   # 桌面
cargo test --manifest-path desktop/src-tauri/Cargo.toml pyenv_components   # 壳组件域
grep -rn -E 'docker (compose|run)|colima' --include='*.md' --include='*.yaml' --include='*.rs' src plugins desktop docs README*   # AC8
```
