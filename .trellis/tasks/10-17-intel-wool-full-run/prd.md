# PRD — 信息羊毛全量跑通:国外源+停摆面复活+真跑私发验证

> 主人令(2026-10-17 晚):「都要跑起来,国外的必须跑起来,一定要给我测试,先私发,
> 你看看现在的华为云都跑出来好多,你能正常跑出来吗?」

## 背景

- 装机 app(世事)自 2026-10-15 16:28 起停摆(进程不在,runs 表末条=10-15 08:28 UTC),
  全部 cron 槽位静默错过两天。
- wool(羊毛情报)/gpu-prices(显卡行情)在装机 config 里装载但从未挂 cron。
- ai-news 国外源 10-15 前直连大多通(openai/deepmind/hf 有产出),残留问题:
  meta 源 `render_helper_missing`(装机 python 缺 crawl4ai)、mistral/qwen 产出 0。
- 对标物:华为云服务器(124.71.115.174)wf_crawl.py,7 论坛源(linux.sb/bbs.bt.sb/
  sb.sb/nodeloc/cocoloop/**dalao/74站**)+ V2EX API 三节点,每日 fresh=48/errors=0,
  发飞书群+主人私聊。MYIA wool 现有 5 源,缺 dalao / 74站 / V2EX 三源。
- 本机代理:Clash Verge 常驻,混合口 127.0.0.1:7897 实测通(google 302);
  MYIA schema 代理词表 = direct / pool:<名> / residential:<区域>。
- 推送凭据全在钥匙串(myia/push/FEISHU_{APP_ID,APP_SECRET,CHAT_ID} + FEISHU2_*),
  channel_directory 现仅知群「AI中转站合伙人群」,主人私聊 chat_id 待枚举。

## 需求

1. **复活**:装机 app 常驻回来(sidecar+cron serve),后续槽位不再静默错过。
2. **都要跑起来**:wool、gpu-prices 挂上 cron;wool 补齐 dalao/74站/V2EX 达到
   华为云同源面;ai-news 残留问题源修复或如实定档。
3. **国外的必须跑起来**:全部国外源逐个真试验证;被墙/被 CF 拦的走本机代理
   或 firecrawl 云兜底(钥匙串凭据已配)。
4. **一定要测试**:每源 `myssia test` 单源试抓(不入库不推送)+ 至少一次品类真跑。
5. **先私发**:所有测试期推送发主人飞书私聊,不发群;私发链路真实验证。

## 验收标准

- [ ] AC1 装机 app 进程在跑、cron serve 活(jobs.json 9+ 任务可 tick)。
- [ ] AC2 wool 挂 cron(0 8,20)、gpu-prices 挂 cron(0 10),tick 记录可见。
- [ ] AC3 wool 源面 ≥ 8(linux.sb/bbs.bt.sb/sb.sb/nodeloc/cocoloop + dalao/74站/V2EX),
      试抓有产出(被墙源允许走代理/firecrawl 兜底,须留试抓证据)。
- [ ] AC4 ai-news 国外源逐源试抓有结论:通(有产出)/ 走兜底通 / 如实定档+原因;
      meta/mistral/qwen 三问题源必须有处置结果。
- [ ] AC5 games 国外源(epic/gog/cheapshark/steam)试抓有结论。
- [ ] AC6 拿到主人私聊 chat_id,真跑 ≥ 1 品类,推送实际发到私聊(API 回执为证)。
- [ ] AC7 仓库 config/ 与装机 config/ 同步一致,改动已提交。

## 边界与红线

- 静默铁律:不起前台焦点(open -g / 后台),不禁屏,不中途打扰。
- 测试推送一律私聊,不向任何群发测试消息。
- 不动主人侧前置件:Reddit 凭据(10-31)、X/RSSHub 实例——如实报告即可。
- live config 直改属常规操作模式(先例在案),但仓库源码同步落地必须做。
