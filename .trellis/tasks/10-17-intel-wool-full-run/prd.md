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

- [x] AC1 装机 app 进程在跑、cron serve 活(jobs.json 9+ 任务可 tick)。
- [x] AC2 wool 挂 cron(0 8,20)、gpu-prices 挂 cron(0 10),tick 记录可见。
- [x] AC3 wool 源面 ≥ 8(linux.sb/bbs.bt.sb/sb.sb/nodeloc/cocoloop + dalao/74站/V2EX),
      试抓有产出(被墙源允许走代理/firecrawl 兜底,须留试抓证据)。
- [x] AC4 ai-news 国外源逐源试抓有结论:通(有产出)/ 走兜底通 / 如实定档+原因;
      meta/mistral/qwen 三问题源必须有处置结果。
- [x] AC5 games 国外源(epic/gog/cheapshark/steam)试抓有结论。
- [x] AC6 拿到主人私聊 chat_id,真跑 ≥ 1 品类,推送实际发到私聊(API 回执为证)。
- [x] AC7 仓库 config/ 与装机 config/ 同步一致,改动已提交。

## 完成记(2026-10-17 晚)

- AC1:open -g 复活(app+sidecar serve+补跑 ai-news 20:00 错过槽位);根因=app 10-15 16:28 起停摆。
- AC2:cron job wool=057a70998714(0 8,20,next 10-18 08:00)、gpu=38c4e21a4e37(0 10,next 10-18 10:00)。
- AC3:wool 9 源 359 条真跑(linuxsb52/dalao26/v2ex-free20/deals18/share20/s74·58/nodeloc60/cocoloop60/sbsb45);
  btsb 判死=域名迁 bt.sb+长亭 WAF(直连/Clash/FC 云三通道全堵,记档 yaml 注释)。
- AC4:17 源 0 故障;meta 修通(crawl4ai 装入管理 python,8 条);anthropic14/cohere22(列表化同步生效);
  6 个 RSS 零产出=条件请求合法跳过(not_modified/validators_match/hash_match,服务器确认无新内容)。
- AC5:epic13/cheapshark20/steam10 通;gog 0=API 200 合法空(当前无 0 元游戏)。
- AC6:FEISHU_CHAT_ID 实锤=主人 p2p(ou_efa4…郑冰津);真跑三连全送达:wool 52 immediate+56 digest
  (push ok×2)、gpu 8 immediate+88 digest(ok)、ai-news 6 immediate(ok)。
- AC7:9 件 config repo→live 同步(先整包备份 config-bak-20261017-woolrun.tgz);提交含 wool/gpu/任务档。
- 附注:bilibili-watch/youtube-watch 仅在仓库(10-17 agent-reach-absorb 线在途件,归该线发布);
  X/RSSHub、Reddit 凭据两前置仍属主人侧(10-31 前配 reddit 凭据即活)。

## 追加:Reddit 源当日点亮(主人令「你自己试试」+否决 opencli 路线)

- 建应用网页表单 reCAPTCHA 死锁(绿勾+服务端恒拒「Incorrect response」,主人手点同败,
  疑出口 IP 被 Reddit 风控标记)→ 弃该路线;agent-reach 的 OpenCLI 浏览器会话方案被主人
  否决(不装第三方扩展)→ 终路=**官方公开 RSS 直连**(json 403/.rss 200 实测定分)。
- 落地:config/proxy-pools.yaml(clash 池=127.0.0.1:7897)+ ai-news 新源 reddit-ml
  (proxy: pool:clash;respect_robots=false 沿 10-05 API 路判例);试抓 25 条实证×2。
- 装机:live 同步;ai-news cron 重建带 --config(ef86ce95d1fd→3445da5eec81)。
- 边界:匿名 RSS 有速率窗,密集测试会 429(冷却后复验通过);每日 2 槽礼貌面在额度内。
- X 观察:agent-reach doctor 实测 twitter-cli 已完整可用(搜索/时间线/读推)——引擎层
  接入留后续档,比 RSSHub 路线优先。

## 边界与红线

- 静默铁律:不起前台焦点(open -g / 后台),不禁屏,不中途打扰。
- 测试推送一律私聊,不向任何群发测试消息。
- 不动主人侧前置件:Reddit 凭据(10-31)、X/RSSHub 实例——如实报告即可。
- live config 直改属常规操作模式(先例在案),但仓库源码同步落地必须做。
