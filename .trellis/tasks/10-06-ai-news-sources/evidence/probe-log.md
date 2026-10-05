# S1 厂商官方源探查回执

- UTC: 2026-10-05T16:32:13+00:00 · honest UA: `MYIA-source-probe/0.1 (+https://github.com/xinzhuzi/myia; feed reachability check)`
- 本机代理探测(端口 [7897, 7890, 1087, 8118]): http://127.0.0.1:7897
- 候选 26 URL / 16 厂商;纪律=每 URL 单次 + robots 每宿主先行

## robots(直连,每宿主一次)

| host | status | bytes | 判读 |
|---|---|---|---|
| openai.com | None | 0 | 允许/无 robots |
| www.anthropic.com | None | 0 | 允许/无 robots |
| deepmind.google | None | 0 | 允许/无 robots |
| research.google | None | 0 | 允许/无 robots |
| ai.meta.com | None | 0 | 允许/无 robots |
| www.microsoft.com | None | 0 | 允许/无 robots |
| x.ai | None | 0 | 允许/无 robots |
| mistral.ai | None | 0 | 允许/无 robots |
| cohere.com | None | 0 | 允许/无 robots |
| huggingface.co | None | 0 | 允许/无 robots |
| qwenlm.github.io | None | 0 | 允许/无 robots |
| api-docs.deepseek.com | None | 0 | 允许/无 robots |
| www.deepseek.com | None | 0 | 允许/无 robots |
| www.zhipuai.cn | None | 0 | 允许/无 robots |
| bigmodel.cn | None | 0 | 允许/无 robots |
| www.moonshot.cn | 404 | 153 | 允许/无 robots |
| www.minimaxi.com | None | 0 | 允许/无 robots |
| seed.bytedance.com | None | 0 | 允许/无 robots |

## feed 探查

| vendor | path | status | shape | bytes | 落点 |
|---|---|---|---|---|---|
| openai | direct | 200 | rss | 760851 | ✅ 可用 feed  |
| openai | direct | 200 | rss | 760851 | ✅ 可用 feed https://openai.com/news/rss.xml |
| anthropic | direct | 404 | - | 21048 | ❌ HTTP 404  |
| anthropic | direct | 404 | - | 20529 | ❌ HTTP 404  |
| deepmind | direct | 200 | rss | 69955 | ✅ 可用 feed  |
| google-research | direct | 200 | rss | 78568 | ✅ 可用 feed  |
| meta-ai | direct | 404 | - | 155534 | ❌ HTTP 404  |
| meta-ai | direct | 404 | - | 155203 | ❌ HTTP 404  |
| microsoft-research | direct | 200 | rss | 243744 | ✅ 可用 feed  |
| xai | direct | 404 | - | 80629 | ❌ HTTP 404  |
| xai | direct | 403 | - | 5475 | ❌ HTTP 403  |
| xai | proxy | 403 | - | 5475 | ❌ HTTP 403  |
| mistral | direct | 404 | - | 243732 | ❌ HTTP 404  |
| mistral | direct | 200 | rss | 25474 | ✅ 可用 feed https://mistral.ai/news/rss |
| cohere | direct | None | - | 0 | ❌ 网络失败  |
| cohere | proxy | None | - | 0 | ❌ 网络失败  |
| cohere | direct | 404 | - | 14294 | ❌ HTTP 404  |
| hf-blog | direct | 200 | rss | 258034 | ✅ 可用 feed  |
| qwen | direct | 404 | - | 7582 | ❌ HTTP 404  |
| qwen | direct | 404 | - | 7582 | ❌ HTTP 404  |
| deepseek | direct | None | - | 0 | ❌ 网络失败  |
| deepseek | proxy | None | - | 0 | ❌ 网络失败  |
| deepseek | direct | 404 | - | 45549 | ❌ HTTP 404  |
| zhipu | direct | None | - | 0 | ❌ 网络失败  |
| zhipu | proxy | None | - | 0 | ❌ 网络失败  |
| zhipu | direct | None | - | 0 | ❌ 网络失败  |
| zhipu | proxy | None | - | 0 | ❌ 网络失败  |
| moonshot | direct | None | - | 0 | ❌ 网络失败  |
| moonshot | proxy | None | - | 0 | ❌ 网络失败  |
| minimax | direct | None | - | 0 | ❌ 网络失败  |
| minimax | proxy | None | - | 0 | ❌ 网络失败  |
| seed | direct | None | - | 0 | ❌ 网络失败  |
| seed | proxy | None | - | 0 | ❌ 网络失败  |
| seed | direct | None | - | 0 | ❌ 网络失败  |
| seed | proxy | None | - | 0 | ❌ 网络失败  |
