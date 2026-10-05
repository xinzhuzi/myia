===== robots.txt of aihot.news (single fetch, curl -s) =====
# sitemap 声明(2026-06-21 SEO Phase 0):bot 据此发现可索引页;每天 ~297 次读 robots
Sitemap: https://aihot.news/sitemap.xml

# 商业 SEO 爬虫 / 数据采集器:不允许抓任何路径(2026-05-05 起)
# 配合 nginx UA 黑名单双保险:守法的看这里、不守法的被 nginx 403
User-agent: SemrushBot
User-agent: AhrefsBot
User-agent: MJ12bot
User-agent: DotBot
User-agent: BLEXBot
User-agent: DataForSeoBot
User-agent: MegaIndex
User-agent: serpstatbot
User-agent: MauiBot
User-agent: ZoominfoBot
User-agent: Mail.RU_Bot
User-agent: SeekportBot
Disallow: /

# AI 检索/引用 bot 专属组(2026-07-02 审计;决策 D2「AI 爬虫全放行」的落地补丁):
# robots 协议里 bot 只遵循「最匹配的一组」,所以这组必须自带全部想保留的 Disallow。
# 与 * 组的两点差异:
#   ① 放行 /api/public/、稳定 /api/v1/ 与 /api/mcp（llms.txt/openapi/ai-plugin 主推的机读入口，原 * 组 Disallow /api/
#     在协议层把守规 AI bot 挡在自家 API 门外,与 Agent 战略自相矛盾)
#   ② 不设 /*?*(公开 API 靠 query 传参,如 ?category=;页面 query 归并交给 canonical)
# Allow 优先级按最长路径匹配：/api/public/、/api/v1/、/api/mcp 长于 /api/，放行生效。
User-agent: GPTBot
User-agent: ChatGPT-User
User-agent: OAI-SearchBot
User-agent: ClaudeBot
User-agent: Claude-User
User-agent: Claude-SearchBot
User-agent: anthropic-ai
User-agent: PerplexityBot
User-agent: Perplexity-User
Allow: /api/public/
Allow: /api/v1/
Allow: /api/mcp
Disallow: /api/
Disallow: /admin/
[exit=0 bytes=3733]
===== robots.txt of www.airbnb.com (single fetch, curl -s) =====
#
#              ///////
#             //     //
#            //       //
#           //         //                           ///             ///                      ///
#          //           //                                          ///                      ///
#         //     ///     //               //// ///  ///  /// ////   /// ////     /// ////    /// ////
#        //   ///   ///   //            //////////  ///  ////////// ///////////  //////////  ///////////
#       //   //       //   //          ///     ///  ///  ///        ///      /// ///     /// ///      ///
#      //    //       //    //        ///      ///  ///  ///        ///      /// ///     /// ///      ///
#     //      //     //      //        ///     ///  ///  ///        ///     ///  ///     /// ///     ///
#    //        //   //        //        //////////  ///  ///        //////////   ///     /// //////////
#    //         /////         //
#    //         /////         //
#     //      ///   ///      //
#       //////         //////
#
#
#    Hello bot, engineer, or very lost layperson! Welcome to your stay on the Airbnb site, we're happy to have you as a guest.
#    If you're a human who likes solving interesting challenges with other humans, check out our careers page: https://careers.airbnb.com/positions/?_departments=engineering
#    If you're a bot who likes crawling webpages, please mind the house rules and avoid accessing any disallowed subfolders to earn a 5-star review from us.
#    Either way, thanks for stopping by! There's no need to collect your garbage at the end of your stay - we use Javascript for that.
#    See you on the next crawl!

User-agent: Googlebot
Allow: /calendar/ical/
Allow: /.well-known/amphtml/apikey.pub
Disallow: /.well-known/assetlinks.json
Disallow: /*/skeleton
Disallow: /*/sw_skeleton
Disallow: /500
Disallow: /account
Disallow: /alumni
Disallow: /api/v1/trebuchet
Disallow: /associates/click
Disallow: /book/
Disallow: /calendar/
Disallow: /contact_host
Disallow: /disaster/lookup
Disallow: /email/unsubscribe
[exit=0 bytes=20930]
===== robots.txt of www.reddit.com (single fetch, curl -s) =====
# Welcome to Reddit's robots.txt
# Reddit believes in an open internet, but not the misuse of public content.
# See https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy Reddit's Public Content Policy for access and use restrictions to Reddit content.
# See https://www.reddit.com/r/reddit4researchers/ for details on how Reddit continues to support research and non-commercial use.
# policy: https://support.reddithelp.com/hc/en-us/articles/26410290525844-Public-Content-Policy

User-agent: *
Disallow: /
[exit=0 bytes=538]
===== robots.txt of nowsecure.nl (single fetch, curl -s) =====
# As a condition of accessing this website, you agree to abide by the following
# content signals:

# (a)  If a content-signal = yes, you may collect content for the corresponding
#      use.
# (b)  If a content-signal = no, you may not collect content for the
#      corresponding use.
# (c)  If the website operator does not include a content signal for a
#      corresponding use, the website operator neither grants nor restricts
#      permission via content signal with respect to the corresponding use.

# The content signals and their meanings are:

# search:   building a search index and providing search results (e.g., returning
#           hyperlinks and short excerpts from your website's contents). Search does not
#           include providing AI-generated search summaries.
# ai-input: inputting content into one or more AI models (e.g., retrieval
#           augmented generation, grounding, or other real-time taking of content for
#           generative AI search answers).
# ai-train: training or fine-tuning AI models.

# ANY RESTRICTIONS EXPRESSED VIA CONTENT SIGNALS ARE EXPRESS RESERVATIONS OF
# RIGHTS UNDER ARTICLE 4 OF THE EUROPEAN UNION DIRECTIVE 2019/790 ON COPYRIGHT
# AND RELATED RIGHTS IN THE DIGITAL SINGLE MARKET.
[exit=0 bytes=1248]
===== robots.txt of scrapingcourse.com (single fetch, curl -s) =====
<html>
<head><title>301 Moved Permanently</title></head>
<body>
<center><h1>301 Moved Permanently</h1></center>
</body>
</html>
