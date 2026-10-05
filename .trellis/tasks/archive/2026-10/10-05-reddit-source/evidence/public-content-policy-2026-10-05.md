# Reddit Public Content Policy 原文摘录(2026-10-05 webReader 全文读取)

> URL: https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy
> robots 前置:robots-support-reddithelp-com.txt(User-agent: * 允许 /hc/*/articles 页面,仅禁 signin/search 等)✅
> 页面元数据 publishedTime: 2025-05-29T15:00:01Z(快照日期以此+本轮读取日 2026-10-05 双标)

## 与本任务直接相关的关键段落(原文抄录)

1. **非商业可用、商业须谈**(Introduction 之后的 "Reddit believes in an open internet" 节):
   > "One of Reddit's values is Default Open. We believe that the free flow of ideas and conversation is the lifeblood of a healthy internet. Our terms have always aligned with our Default Open value — **you can use Reddit content for non-commercial uses, such as learning and community, but talk to us if you have commercial purposes in mind.**"

2. **抓取=未授权访问**(同节):
   > "Unfortunately, we see more and more entities using **unauthorized access (for example, by scraping or using data brokers)** or misusing authorized access to collect public data in bulk, especially with the rise of use cases like generative AI. These entities amass public data, including Reddit content, for their own commercial gain..."

3. **三类被许可方**(data licensees):
   > "Companies that help brands monitor trends associated with their brands; Large language model makers ...; **Researchers trying to better humanity and the open internet, to whom we continue to provide access to Reddit public content for research.**"

4. **被许可方限制清单**(摘):不得继续使用已删除内容;不得访问/展示色情内容;不得按敏感属性画像;不得与三方数据合并投放/建客群;不得骚扰;不得监控敏感事件/组织;不得背景调查/极端审查/信用风险/人脸识别;不得向政府/三方提供监控执法用途;不得非法欺骗用途。

5. 隐私面:私有数据(私信/私密社区/已删除/非公开账户信息)永不许可。

## 口径判读(给 research.md 用)

- **非商业使用被条款正面允许**("Our terms have always aligned ... non-commercial uses")——但通道必须是**授权访问**:政策把「抓取 scraping」点名为未授权访问形态。
- 研究通道存在且被正面表述("continue to provide access ... for research"),与 robots.txt 注释自指 r/reddit4researchers 一致。
- 对 MYIA(个人非商业情报收集)的含义:走官方授权通道(Data API OAuth)落在「非商业可用」口径内;绕 robots 直抓站内(含 .rss/new.json)与政策「未授权访问」表述冲突,10-03 respect_robots 判例维持。
