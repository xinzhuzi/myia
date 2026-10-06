# PRD:AI 优惠守望——prompt 精筛羊毛社区三站 AI token/模型优惠(补档)

> 立档:2026-10-06(补档) · 来历:三段纪律巡检发现本件已交付未立档(先档后行形态缺口,如实补记,未新造内容)
> 状态:交付在案(plugins/ai-token-deals.yaml 提交 2d69613 + 日报分区提交 4ad1fe0 + cron 挂点 job 99c31ad4a152);本档为事后回填,非开工档

## 开始段:需求与挂点(补记交付时的需求面)

**主人令(2026-10-06,原文)**:「找一些有价值的,免费白嫖 token,AI token 模型优惠」(录于 plugins/ai-token-deals.yaml 头注 L3)。

**需求形态**(配置件即需求载体,指针如下):

- **prompt 精筛羊毛社区三站**:linux.sb / bbs.bt.sb/latest / www.nodeloc.com/latest(plugins/ai-token-deals.yaml L35-37,羊毛件已验证通路复用);LLM 只挑「AI token 白嫖/免费额度/新用户送额度/API 优惠/模型折扣/低价 API 中转」类目(L27-33)。
- **价值排序**:免费大额>长期白嫖>限时折扣>小额(L30)。
- **风险标注**:骗子/倒卖高风险标「⚠️谨慎」、看不出可信度如实标「未验证」(L31);全部站点无相关帖时如实说「今日无 AI 优惠线索」不编造(L32)。
- **配置文件指针**:`plugins/ai-token-deals.yaml`(交付提交 2d69613,2026-10-06 18:02,+66 行单文件);engine: prompt(链外引擎,schema.py ENGINES 词表在册)+ 同 GLM 凭据(keychain:myia/llm/base_url + myia/image/api_key,L39-40);push=archive 仅入库归合并日报(L54-59)。
- **cron 挂点**:每日 08:00(`0 8 * * *`,Asia/Shanghai,与羊毛件同槽,合并日报 08:05 承载,L14);cron job id **99c31ad4a152**(数据根 cron/jobs.json 实录,建于 2026-10-06T18:02:46+08:00)。

## 过程段(交付流水,git/数据根实录回填)

- [x] 2026-10-06 18:02 提交 **2d69613**(2d69613e4cabda9e16bd25c3f991b8afe93fe88e):plugins/ai-token-deals.yaml 落地(+66 行仅本件一路径);提交信息实录「dry-run success 亲验」——交付者回执在案。
- [x] 18:02:46 cron 挂点建档:job **99c31ad4a152** 写入数据根 cron/jobs.json(origin=cli,插件 yaml 解析建档成功即装载回执);数据根部署副本 `~/Library/Application Support/MYIA/plugins/ai-token-deals.yaml` 与仓内件逐字节一致(本档补录时 diff 亲验)。
- [x] 18:23 提交 **4ad1fe0**(4ad1fe0481e93e55a8e9a0aa3aac0bd7177d83a1):plugins/daily-digest.yaml 新增分区四「AI 白嫖与优惠」(L94-96,sources: [ai-token-deals],max_entries: 10;+11 行仅本件一路径)——合并日报承载面配齐。

## 结果段(验收回执:AC 装载/调度/分区逐项对照现状)

- [x] **AC1 装载**:仓内 `plugins/ai-token-deals.yaml` 在库(提交 2d69613);数据根部署副本与仓内件 diff 逐字节一致(本会话亲验);engine: prompt 在 `src/myssia/schema.py` ENGINES 词表在册(本会话亲读,10-06-hermes-align 批次3 4a5b980 引入);cron 注册器自该 yaml 成功解析建档(job created_at=2026-10-06T18:02:46)= 系统侧装载实绩。
- [x] **AC2 调度**:job 99c31ad4a152 实录 enabled=true、state=scheduled、`0 8 * * *` Asia/Shanghai、next_run_at=2026-10-07T08:00:00+08:00(数据根 cron/jobs.json 本会话亲读)。如实注:last_run_at=null——挂点建于 10-06 18:02,首跑窗口 10-07 08:00,补档时点未到,**首跑实绩回执尚未产生**(留位)。
- [x] **AC3 分区**:plugins/daily-digest.yaml:94-96 分区四「AI 白嫖与优惠」sources [ai-token-deals](本会话亲读;交付提交 4ad1fe0)。
- [ ] **(留位)dry-run 复验**:交付提交 2d69613 信息记录「dry-run success 亲验」为交付者回执;本补档会话**未重跑**(涉真实 LLM 调用消费凭据额度,补档范围=对照现状不重复涉网)——如需现时回执,`myssia run plugins/ai-token-deals.yaml --dry-run` 一条可复。

## 验收标准(AC)

- [x] AC1 装载:插件 yaml 入库+数据根部署一致+引擎词表在册+cron 解析建档(见结果段)
- [x] AC2 调度:cron job 99c31ad4a152 每日 08:00 已挂已启用(见结果段;首跑回执留位)
- [x] AC3 分区:合并日报「AI 白嫖与优惠」分区已配(见结果段)
- [ ] dry-run 现时复验(交付回执在案,补档未重跑;见结果段留位)
