# 羊毛质量治理:提问帖过滤+同主体合成+TapNow入源

## Goal

主人令2026-10-19「按照你的建议做完」——按前一轮三建议全量落地:
①羊毛提问/广告帖 drop 规则;②源级 aggregate 同主体合成(规则档);③TapNow
活动源接入。AI 档(enrich 开启做语义判重/合成)留 v0.2,不入本档。

案发背景(2026-10-19 主人报障,证据在装机库 ~/Library/Application Support/MYIA/myssia.db):

- items.id=8547「甲骨文账号升级后…可以再免费开一台 2c12g100g 的实例吗」
  (sb.sb 提问帖)因标题含「免费」被 FREE_KW 判 freebie;同型 7616(免费域名
  提问帖)、8060(B2Proxy 促销广告)。根因链:源只抓标题+URL → watchlist
  关键词过 → 免费信号压倒一切 → enrich 关闭(v0.1 设计如此,无解析环节)。
- TapNow(app.tapnow.ai)活动列表整页 8+ 行同主体(主人截图「这种情况要
  合成1个才行」),逐条进情报流=刷屏。

## Requirements

1. **drop 否决(①)**:classify.rules 规则支持 `drop: true`——命中即
   category=None 丢弃,先于内置关键词裁决;分类器
   `ClassifyResult.dropped_by` 留观测;管线 classify 阶段丢弃计数分离
   (`classify_rule_drop` ≠ `classify_unmatched`)。wool.yaml 落三条否决
   规则:提问帖(吗/呢?/请问/想问/问一下/请教/求助/求教/什么时候)、
   怎么/如何带问号、促销广告(超值/大促/秒杀/特惠/低价/元起/刀起)。
2. **源级合成(②)**:SourceConfig 新增 `aggregate: {subject}`(仅
   extract.type=list 可配,装载期交叉校验);fetch 尾声整页合成单条——
   标题=「{subject} · N 条(最高 M)」(M 仅当行标题解析出数字)、
   url=页面 URL(稳定身份)、明细进 content、原始行进
   metadata.aggregated_from。与 v0.4 顶层 aggregate(LLM 跨源)正交。
3. **TapNow 入源(③)**:实测登录墙(JS 壳 + firecrawl 云渲染点掉 cookie
   弹墙后 "Log in or sign up",无免登录 API,bundle 挖掘零收获)——按
   linux.do 先例落注释占位源,aggregate 形态已配好,解堵差主人侧登录态
   (env:TAPNOW_COOKIE 或等价通道)。
4. 顺手修预存红:74d822c4(10-18)加 g4f-endpoints 第 10 源漏更新
   test_wool_declares_nine_source_slots——补 10 源断言(git 归因:该红在
   无本任务改动的树上同样复现)。

## Acceptance Criteria

- [x] AC1 分类器:drop 规则先于免费信号否决案发标题;非命中正常放行;
      rules_from_config 接受/拒绝 drop 字段;与打标规则共存(myssia-classifier
      tests/test_classify.py 8 新测)
- [x] AC2 管线:classify_rule_drop 独立计数;整份 wool.yaml 过 load_category
      且 drop 规则名单断言(tests/pipeline/test_wool_quality_gate.py 8 测)
- [x] AC3 合成:整页 8 行→1 条契约(标题/URL/content/aggregated_from);
      空页零合成;非 list 源配 aggregate 装载即拒(同文件)
- [x] AC4 真实 wool.yaml 规则对真实案发标题(8547/7616/8060)否决、真羊毛
      (腾讯地图/京东plus/免费送NAS券)放行(同文件)
- [x] AC5 回归:全量 pytest 6001 passed 0 failed(desktop 套件 1 预存红
      test_logs_tail_run_id_merges_disk_rows,stash 归因非本任务引入,
      系并行会话在途债)
- [x] AC6 文档:skill/SKILL.md 字段表双向锁定补 drop/aggregate 两字段
      (test_skill_doc 2 红修绿)
- [x] AC7 schema:SourceAggregateConfig + ClassifyRuleConfig.drop +
      invalid_source_aggregate 装载期校验
- [ ] AC8 装机链:classifier 0.0.6 轮子装入 app 环境(0.0.1 旧轮不支持
      drop,不升则 wool 装载即炸)、wool.yaml 同步装机 config(带备份)、
      app 重打包换装、真网 dry-run 验证 drop 生效

## Notes

- 装机库 id=8547 等存量脏数据不删(用户数据面,过滤是向前生效;90d 保留
  期自然滚出)。
- TapNow 截图读图三级链(Vision/Paddle/本机VL)+ web 检索实证 Tapies 为
  TapNow 平台积分;活动列表登录墙为 firecrawl 两轮实弹结论。
- AI 档(v0.2):wool enrich.enabled 开启 + glm-5.3-flash 判「真羊毛(实测/
  操作/资源)」+ 同主体语义聚类——配置槽位(scores/batch/budget/route
  score>=8)均已预留,届时只翻开关接端点。
