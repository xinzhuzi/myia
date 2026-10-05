# S1 探查第二轮回执(sniff bug 修复后重取证)

- UTC: 2026-10-05T16:35:45+00:00
- round1 工具故障在档:200 响应被 sniff 崩成「网络失败」,本轮对被毁证据逐 URL 重探(仍单次)

## robots 重取证(直连)

| host | status | bytes | head 片段 |
|---|---|---|---|
| openai.com | 200 | 98 | User-agent: * Allow: / Disallow: /microsoft-for-startups/  Sitemap: https://openai.com/sit |
| www.anthropic.com | 200 | 71 | User-Agent: * Allow: /  Sitemap: https://www.anthropic.com/sitemap.xml  |
| deepmind.google | 200 | 69 | User-agent: * Allow: /  Sitemap: https://deepmind.google/sitemap.xml  |
| research.google | 200 | 68 | User-Agent: * Allow: /  Sitemap: https://research.google/sitemap.xml |
| ai.meta.com | 200 | 859 | # Notice: Collection of data on Facebook through automated means is # prohibited unless yo |
| www.microsoft.com | 200 | 9126 | # Robots.txt file for www.microsoft.com v2.11  User-agent: * Disallow: /*?*ep_* Disall |
| mistral.ai | 200 | 70 | User-agent: * Allow: /  Sitemap: https://mistral.ai/sitemap-index.xml  |
| huggingface.co | 200 | 68 | User-agent: * Allow: /  Sitemap: https://huggingface.co/sitemap.xml  |
| qwenlm.github.io | 200 | 70 | User-agent: * Disallow: Sitemap: https://qwenlm.github.io/sitemap.xml  |
| www.zhipuai.cn | 200 | 64 | User-Agent: * Allow: /  Sitemap: https://zhipuai.cn/sitemap.xml  |
| bigmodel.cn | 200 | 115 | User-agent: * Disallow: /agent Disallow: /flow-landing Disallow: /demo Disallow: /dev/ Dis |
| www.moonshot.cn | 404 | 153 | <html> <head><title>404 Not Found</title></head> <body> <center><h1>404 Not Found</h1>< |
| www.minimaxi.com | 200 | 131 | User-Agent: * Allow: / Disallow: /api/ Disallow: /_next/  Host: https://www.minimax.cn Sit |
| seed.bytedance.com | 200 | 70 | User-Agent: * Allow: / Sitemap: https://seed.bytedance.com/sitemap.xml |

## feed 重取证

| vendor | status | shape | bytes | head 片段 |
|---|---|---|---|---|
| zhipu | 200 | html | 899271 | <!DOCTYPE html><html lang="rss.xml"><head><meta charSet="utf-8"/><meta name="vie |
| bigmodel | 200 | html | 4297 | <!DOCTYPE html><html lang="zh-cn"><head><meta charset="utf-8"><meta name="author |
| moonshot | 200 | html | 98191 | <!DOCTYPE html>     <html dir="ltr" lang="zh-Hans">       <head>         <link r |
| minimax | 200 | html | 339921 | <!DOCTYPE html><html lang="zh-CN"><head><meta charSet="utf-8"/><meta name="viewp |
| seed-rss | 200 | html | 11054 | <!doctype html><html lang="zh-CN"><head><script>window.gfdatav1={"env":"prod","e |
| seed-feed | 200 | html | 11058 | <!doctype html><html lang="zh-CN"><head><script>window.gfdatav1={"env":"prod","e |
| deepseek-www | 404 | html | 45549 | <!DOCTYPE html><html id="__next_error__"><head><meta charSet="utf-8"/><meta name |
| cohere-blog | 200 | html | 1012830 | <!DOCTYPE html><html lang="en-US" dir="ltr"><head><meta charSet="utf-8"/><meta n |
| qwen-feed | 404 | html | 7582 | <!doctype html><html lang=en dir=auto><head><meta charset=utf-8><meta http-equiv |

## watch 候选页(S2)

| vendor | status | shape | bytes | 落点 |
|---|---|---|---|---|
| anthropic-news | 200 | html | 425195 | ✅ watch 候选(200 html) |
| meta-ai-blog | 200 | html | 202750 | ✅ watch 候选(200 html) |
| xai-news | 403 | html | 5475 | ❌ 403 |
| cohere-blog-page | 200 | html | 1012830 | ✅ watch 候选(200 html) |
| qwen-blog-page | 200 | html | 13828 | ✅ watch 候选(200 html) |
| zhipu-news | 200 | html | 899213 | ✅ watch 候选(200 html) |
| deepseek-home | 200 | html | 115583 | ✅ watch 候选(200 html) |
