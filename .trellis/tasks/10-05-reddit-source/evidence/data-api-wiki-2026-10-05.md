# Reddit Data API Wiki 一手摘录(2026-10-05 webReader 全文读取)

> URL: https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki
> 页面 publishedTime: 2026-05-11T16:00:03Z;robots 前置=A5 ✅
> 页首免责:"Some of the information in our legacy API documentation ... may be out of date. Always consult our Developer Terms and Data API Terms."

## 关键原文(摘)

- **OAuth 强制**:"Reddit **requires** OAuth for authentication";"Clients must authenticate with a registered OAuth token. We can and will freely throttle or block unidentified Data API users.";**"Traffic not using OAuth or login credentials will be blocked, and the default rate limit will not apply."**
- **免费层额度(一手明文)**:"We enforce rate limits for those eligible for free access usage of our Data API. The limit is: **100 queries per minute (QPM) per OAuth client id**. QPM limits will be an average over a time window (currently 10 minutes) to support bursting requests."
- 聊天另册:2,000 msg/天/接收者、3,000 msg/天/计、300 房/天(bot)。
- 限速响应头:X-Ratelimit-Used / X-Ratelimit-Remaining / X-Ratelimit-Reset。
- UA 硬要求:格式 `<platform>:<app ID>:<version string> (by /u/<reddit username>)`;默认 UA(Python/urllib 等)被大幅限速;**"NEVER lie about your User-Agent"**。
- **robots 边界(决定性)**:**"Our robots.txt is for search engines, not Data API users."**
- 删除义务:Reddit 侧删除的内容必须同步删除(含标题/正文/URL/作者标识);"strongly recommend routinely deleting any stored user data and content within **48 hours**";留存已删内容(即使去标识)= 违反条款。
- 申请:"To request, please contact us here."(联系审批)
