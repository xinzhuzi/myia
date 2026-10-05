# Reddit for Researchers(RFR)Program 一手摘录(2026-10-05 webReader 全文读取)

> URL: https://support.reddithelp.com/hc/en-us/articles/49381918834964-Reddit-for-Researchers-Program
> 页面 publishedTime: 2026-06-02T08:11:46Z(页面标注 "Updated 1 month ago");robots 前置=A5 ✅

## 关键原文(摘)

- 定位:"gives academics a secure, privacy-first way to access Reddit public content"。
- 资格:**认证高校**附属研究员/PI + **机构邮箱**申请;须交:详细 proposal(含目标 subreddit)、**IRB/伦理审查证明**、机构赞助人证明、既往研究成果(加分);"limited to sponsored academic researchers affiliated with higher education institutions conducting non-commercial research"(偶批非营利/政府)。
- **免费**:"Access to the RFR dataset is provided free of charge for approved, non-commercial academic projects."
- **访问形态:不是 REST API,是 BigQuery Analytics Hub(BQAH)**——Google Cloud 控制台 SQL 查询;@redditresearchers.com 账号 + 2FA。
- 数据面:**5 年历史 + 6 个月延迟**,月度更新;含 hashed user id/subreddit/posts/comments;排除私信/已删/私密/隔离/NSFW/spam。
- 期限:**单项目 ≤1 年**,到期重申请;查询全量审计日志;禁止再分发/共享凭据/去匿名化;发表前交 preprint 存档。
- 官方定位互证(dev-platform 文章):"The only official and authorized avenue for performing research using Reddit data is through the Reddit For Researchers (RFR) program."

## 判读(给 research.md)

- RFR = 学术批文制 + BigQuery 历史数据集(6 月延迟),**不是实时采集 API**;
- 对 MYIA(个人情报实时收集)结构性不适用:无高校/IRB 门槛即够不着,够着了也拿不到实时流;
- 「robots.txt 自指 r/reddit4researchers 为研究/非商业通道」的池档口径须修正:该通道实际=RFR(BQAH),与个人非商业 API 使用是两回事。
