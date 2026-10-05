# 涉网探查日志(全程:每目标 URL 单次、先 robots、零压力、全部记档)

时区:本地 2026-10-05 傍晚。工具:curl 8.x(web 直探)/webReader MCP(页面读取)/WebSearch+web_search_prime(搜索引擎定位)。凡失败不重试同 URL;redirect 跟随属同一次请求链。

## A. robots.txt 探查(每宿主单次)

| # | 宿主 | 命令 | 结果 | 存档 |
|---|------|------|------|------|
| A1 | www.reddit.com | `curl -s -m 15 https://www.reddit.com/robots.txt` | exit 0,538B | reddit-robots-2026-10-05.txt |
| A2 | www.reddit.com | `curl -o /dev/null -w '%{http_code}' -m 15` 同 URL | **200** | (本行) |
| A3 | oauth.reddit.com | `curl -s -m 15 https://oauth.reddit.com/robots.txt` | exit 0,26B,`User-Agent: * Disallow: /` | reddit-robots-oauth-host-2026-10-05.txt |
| A4 | developers.reddit.com | `curl -s -m 15 .../robots.txt` | 483B:`*` 段 Allow /$、/apps、/docs、/docs/;Disallow /(其余)+ /docs/*.md$ + llms.txt | robots-developers-reddit-com.txt |
| A5 | support.reddithelp.com | 同上 | 2448B:Zendesk 版;`*` 段**未禁** /hc/*/articles(仅禁 signin/search/requests 等) | robots-support-reddithelp-com.txt |
| A6 | techcrunch.com | 同上 | 710B:`*` 段仅禁 wp-admin/search;**文章页放行**(AI 专用 UA 另册全禁) | robots-techcrunch-com.txt |
| A7 | news.google.com | 同上 | 484B:`*` 段 `Disallow: /` + Allow 清单(/$、/home、/topics/、/stories/ 等)——**/rss/ 不在 Allow 清单=禁** | robots-news-google-com.txt |
| A8 | www.bing.com | 同上 | 302→cn.bing.com(地区跳) | robots-www-bing-com.txt |
| A9 | cn.bing.com | 同上(随 A8 redirect) | 2676B:`*` 段禁 /search 等 90+ 路径,**未禁 /news/search** | robots-cn-bing-com.txt |
| A10 | pushshift.io | 同上 | 200,1248B,内容信号模板(无 UA/Disallow 指令) | robots-pushshift-io.txt |

**A1/A2 与 10-03 库档对照**:`diff -u` exit 0 + SHA-256 同值 `41aea421…781857` → **字节级一致**,两快照(10-03 库档+10-05 现探)+10-05 转述注口径成立。

## B. 页面读取(每 URL 单次,webReader;目标域 robots 已先探)

| # | URL | 结果 | 存档 |
|---|-----|------|------|
| B1 | developers.reddit.com/docs | Devvit v0.9 文档(Docusaurus),非 Data API 口径页;有链接汇总 | (未落全文,结论入 research) |
| B2 | developers.reddit.com/docs/api | Devvit RedditAPI 插件页(v0.9 旧档),非配额页 | 同上 |
| B3 | support.reddithelp.com/.../26410290525844-Public-Content-Policy | 全文到手(页面 publishedTime 2025-05-29) | public-content-policy-2026-10-05.md |
| B4 | support.reddithelp.com/.../49381918834964-Reddit-for-Researchers-Program | 全文到手(publishedTime 2026-06-02) | reddit-for-researchers-2026-10-05.md |
| B5 | support.reddithelp.com/.../14945211791892-Developer-Platform-Accessing-Reddit-Data | 全文到手(publishedTime 2026-05-28) | dev-platform-accessing-data-2026-10-05.md |
| B6 | support.reddithelp.com/.../16160319875092-Reddit-Data-API-Wiki | 全文到手(publishedTime 2026-05-11) | data-api-wiki-2026-10-05.md |
| B7 | support.reddithelp.com/.../47822311698452-App-Migration-Program-2026-Terms | 全文到手(publishedTime 2026-04-09) | app-migration-terms-2026-10-05.md |
| B8 | support.reddithelp.com/hc/sitemap.xml | 450B sitemapindex(4 子图);未追子图(本轮无需要) | sitemap-reddithelp.xml |
| B9 | techcrunch.com/2026/09/30/reddit-is-killing-rss-feeds...(URL 系搜索结果推断) | webReader 500(服务端错,未达目标);WebFetch 备选=404(URL 推断错,**未再猜**) | (如实记未取得) |

## C. PoC(零凭据合规通道候选;单次每 URL)

| # | URL | 结果 |
|---|-----|------|
| C1 | `https://www.bing.com/news/search?q=site%3Areddit.com&format=rss`(-L) | 200 但 final=cn.bing.com/(**302 吞路径**),15KB 首页 HTML 非 RSS,`<item>`=0 → poc-bing-news-rss.xml |
| C2 | `https://cn.bing.com/news/search?q=site%3Areddit.com&format=rss` | **302→/**(118B 跳转页),0 items → poc-bing-news-rss-cn.xml |
| C3 | C2 + `&ensearch=1`(强制国际版惯用参数) | **302→/** 同墙,0 items → poc-bing-news-rss-ensearch.xml |
| C4 | `https://api.pushshift.io/`(根,状态探) | **307**(0 字节体)——服务残壳应答,无 API 载荷 → api-pushshift-root.html |
| C5 | news.google.com/rss/search PoC | **未执行**:A7 robots 已判 /rss/ 对通用 UA 禁,按纪律不探 |

## D. 搜索引擎定位(WebSearch/web_search_prime,≥3 形状交叉;非目标域直探)

- Data API 免费层 100 QPM:多源(crawlfeed/techloy/HN/GitHub Infinity for Reddit 等)一致 → 后由 B6 一手坐实。
- 2026-09-30 Reddit 公告(RSS 2026-11-13 退役;新 API 申请 2026-10-31 截止;未注册 app 2027-01-12 起移除;公 Data API 2027-03 分阶段终结;迁移向 Devvit):TechCrunch/TechRepublic/Mashable/unite.ai/crawlfeed 多源一致 + r/help 官方周报(2026-10-01)引用 r/redditdev 公告佐证 + B7 一手迁移计划侧证(2026-03-31~12-31)。**一手原文在 r/redditdev(www.reddit.com robots 全站禁抓,按纪律未取)。**
- Pushshift:2023-05-02 被 Reddit 撤销访问,mod-only 部分恢复,无新数据摄入(think-pol/redditapis 多源)→ 与 C4 直探互证。
