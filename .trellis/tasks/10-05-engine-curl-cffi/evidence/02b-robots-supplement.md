===== robots.txt of news.ycombinator.com (single fetch) =====
User-Agent: *
Crawl-delay: 30
Disallow: /collapse?
Disallow: /context?
Disallow: /fave?
Disallow: /flag?
Disallow: /hide?
Disallow: /login
Disallow: /logout
Disallow: /r?
Disallow: /reply?
Disallow: /submitlink?
Disallow: /vote?
Disallow: /x?

===== aihot.news robots.txt FULL (second doc fetch: first record truncated at 40 lines, * group needed) =====
Disallow: /admin/
Disallow: /mp
Disallow: /noise
Disallow: /sources
Disallow: /starred
Disallow: /events/
Disallow: /feedback

# 通用爬虫 / 搜索引擎 / 大厂 LLM bot:默认全放行,只禁后台和私有页
# 「可索引哪些页」交给 sitemap.xml 表达;robots 只做 Disallow(2026-06-21 SEO 审计 #12:
# 删掉原 Allow /mp /selected /x 等冗余行——User-agent:* 本就默认全放行,逐条 Allow 是
# no-op,且这些非索引入口与 sitemap 故意排除策略自相矛盾)。
User-agent: *
# 注:不再 Disallow /items/。详情页靠页内 meta robots noindex 排除收录;robots 屏蔽
# 反而让 bot 拿不到 noindex 标记(可能"被屏蔽仍索引 URL"),且挡掉 AI bot 读全文(决策 D2)。
# /mp、/noise、/events 已退役；/sources 只保留到后台的书签跳转。继续 Disallow
# 避免守规 bot 消耗这些非内容路径；实际 404/302 由 nginx 决定，robots 不作为权限闸。
# /hot 已于 2026-08-02 正式开放，事件详情使用 /story/*；两者允许抓取并由 sitemap 发现。
Allow: /api/v1/
Allow: /api/mcp
Disallow: /api/
Disallow: /admin/
Disallow: /mp
Disallow: /noise
Disallow: /sources
Disallow: /starred
Disallow: /events/
Disallow: /feedback
# 2026-07-15 参数页索引治理:不再用 `/*?*` 阻止 query URL。
# 原规则让 Google 看不到页内 canonical，却仍可从外链发现并收录裸 URL，GSC 因而积累
# “被 robots.txt 屏蔽但仍收录”；公开参数页现在允许抓取并读取 canonical，sitemap 仍只提交
# 主 URL。无限参数的成本边界由 nginx cache-key 白名单、分页深度上限和 limit_req 负责，
# 不再拿 robots.txt 兼任 canonical / noindex。OG 图自带的 hash query 也自然恢复可抓，无需 Allow 特判。
# 不设 Crawl-delay(2026-06-21 SEO 审计 #12):它会把想拉拢的 Bingbot/GPTBot/ClaudeBot/
# PerplexityBot 一并限速(软违决策 D2「AI 爬虫全放行、最大化曝光」);Googlebot 本就忽略它。
# 滥用防护由 nginx UA 黑名单 + 分层 limit_req 兜底：公开页 `aihot_public_rl`，公开 API 另有
# `aihot_api_ip_rl=60r/m`，RSS 另有专用低频桶；robots 只是守规爬虫软约束。
