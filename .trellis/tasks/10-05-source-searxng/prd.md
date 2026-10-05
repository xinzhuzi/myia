# SearXNG 搜索式情报源(自托管元搜索 → 关键词日报)

## Goal

接入 SearXNG(自托管元搜索聚合)为新型情报源:**搜索式情报**——关键词
日报/舆情面(「竞品名+发布」「事件词+进展」),与现有订阅式源(RSS/
静态页/直连 API)互补。走现有引擎层抽象,零新引擎框架。

## 背景与现状(锚点)

- 引擎层实况:engines/ 有 static_html/direct_api/rss(via static_html
  extract)/crawl4ai/…,**无搜索型引擎**;registry.py 注册表+降级链先例。
- grill Q5 决议:**硬前提=主人愿意多跑一个自托管 docker 服务**(本机/
  自有服务器);json 接口默认关闭——需在实例 settings.yml 显式开
  `formats: [html, json]`(自托管可控,非上游恩赐)。
- 许可:AGPL-3.0(searxng/searxng)——同 RSSHub/Firecrawl 判例:**只作
  自托管 HTTP 服务消费,零代码复用**,合规。
- 既有相似件:RSSHub 场景件(plugins/myssia-rsshub,manifest 声明依赖+
  文档指路,不 vendor 代码)——SearXNG 同款形态。

## Requirements(两段式:探查先行,实现后行)

1. **探查段(先行,产出 research.md)**:
   - docker compose 起本机 searxng(官方镜像);settings.yml 开 json
     format+limiter 配置核对;
   - 探接口形状:`GET /search?q=<关键词>&format=json&language=zh-CN
     &safesearch=1&p=<页>`;results[] 字段(title/url/engines/publisheddates
     可空);分页 pageno 语义;空结果/坏参数形态;
   - robots:自托管实例 robots 自控——**记录自家实例策略=允许自家采集**,
     尊重上游搜索源由 SearXNG 自身聚合策略负责(不绕过其设计);
   - 产出:接口快照(date 戳)+查询词示例集+限流口径(limiter/机器人
     检测默认态)。
2. **实现段(探查过了再动)**:
   - engines/searxng.py(BaseEngine):源配置 `queries: [关键词列表]`,
     逐词一页(research.md 定页数),逐 result 出条 {url,title,
     content=result.abstract 若有};去重走 feed 层既有 url metric 键
     (零新机制);**礼貌间隔**:interval 建议 ≥1800s+逐词串行+页间延时
     (自托管也设——上游元搜索的礼貌由 searxng 聚合层承担,MYIA 不放大)。
   - schema:SourceConfig 支持 engine="searxng"+`queries` 字段+
     `searxng_base_url`(缺省 http://127.0.0.1:8888,env MYIA_SEARXNG_URL
     同 FIRECRAWL 先例 firecrawl.py:46-48)。
   - 品类 YAML 示例:plugins/searxng.yaml(关键词日报骨架,**缺省不启用**,
     注释含部署一句话指引);随包 resources 映射核对(test_installer_
     resources 守卫常量若涉随包需同步——**优先不进随包**,池档件定位)。
3. **UI 美化**:
   - 源管理屏:引擎徽章 searxng(与 rss/static_html 徽章同款样式);
   - feed 卡:来源标注正常走既有通道零新面;
   - yaml-editor:模板列表增「SearXNG 关键词日报」骨架;queries 数组
     编辑复用既有数组字段控件(零新组件);
   - 文案人话:「自己跑的聚合搜索,按关键词天天给你一页结果差集」。

## 测试

- engines 用例(fixture json,research.md 快照对齐):①正常多词多结果
  ②空结果→零条不炸 ③坏行跳过(缺 url/title)④分页拼接 ⑤base_url
  env 覆盖两态 ⑥schema queries 必填校验(engine=searxng 时)。
- 限流/礼貌:间隔与串行断言(沿既有引擎礼貌用例形态)。
- vitest:源管理徽章+yaml-editor 模板项(若编辑器动了模板列表)。

## 验证

- 真跑(探查段即真跑):本机 docker 实例 20 条入库截图+evidence 落档;
  主人服务器部署后复验一条(AC 门控:无 docker 环境则 fixture 充分+真跑
  留部署后)。
- 装机件:源管理屏 searxng 徽章像素(装机包随下批)。

## Acceptance Criteria

- [x] AC1 探查:research.md 含接口快照+json 开启步骤+限流口径(真跑)。
      (勾选依据见尾部「探查段收口注记」——research §1/§2.3/§5/§8 全真跑)
- [ ] AC2 引擎:六用例绿;去重走既有 metric;礼貌间隔在位。
- [ ] AC3 schema/YAML:queries 校验;示例骨架缺省不启用。
- [ ] AC4 UI:徽章+模板+文案像素回执。
- [ ] AC5 门禁:pytest/vitest/ruff 全绿;协议对账零漂移(零 sidecar 面)。
- [ ] AC6 部署指引:README/zero-cost 一节一句话+compose 模板(服务消费
      零代码复用,AGPL 边界声明同 RSSHub 先例)。

## 边界与红线

- 不做:代理公共 SearXNG 实例(公共实例明禁 API 滥用,只走自托管);
  搜索结果正文抓取(条目即情报,深抓走既有引擎手动配置)。
- 红线:AGPL 零代码复用;queries 明文非凭据可落 YAML(无密)。

## 放行回执(2026-10-05 深夜,主人令「都按建议去做」)

- 问题:自托管 docker 前提。做法:主人整体放行,排队第 4;探查段用本机 docker compose 先行验证(不依赖主人服务器),部署上生产才需主人侧 docker;AGPL 服务消费判例在档。
- 执行顺序(全五档):cron-heartbeat(先做,零前置)→ push-bark → push-apprise(点名即启)→ source-searxng → firecrawl-selfhost-verify。

## 探查段收口注记(2026-10-06,「余量全清」归档会话)

- **AC1 勾选成立**(探查段达成):research.md 已实测结案——§1 json
  开启 compose 步骤(官方口径+实测通过)、§2.3 接口实快照(categories=web
  55 条,evidence 蓝本)、§5 限流两态实测定案(常发 Accept-Language+
  template=default.html 过滤),§8 清单全项真跑 evidence 六件在档。
- **AC2-AC6 全部为实现段门控**(§9 挂点定案:engines/searxng.py+
  ENGINE_REGISTRY/queries 校验/示例骨架缺省不启用/UI 徽章/部署指引),
  实现段续本档不立新档(research §9-1 定案),届时逐项回填,本段不预勾。
- 统一批门禁亲跑绿(pytest 4461/40/0+vitest 523+tsc/vite build+cargo
  check/test 56+ruff)+CI 绿(run 37352272165,success,headSha
  ff3e4a9)与探查段零代码面无涉,如实记;本机实例留跑(json 开+
  limiter 关+bing 启用)供实现批复用。
- 本档不归档(in_progress 续实现段);探查段提交 ad19a9a+edecfd0。
