# 国产五家 SPA watch 重探(css 内容过滤轮,research §7 兑现)

- UTC: 2026-10-06T04:18:18+00:00
- UA: MYIA-source-probe/0.1 (+https://github.com/xinzhuzi/myia; spa css-filter re-probe)
- urlwatch: 2.29
- 链路:与生产同(上游 LxmlParser,css{selector, exclude='script, style, noscript, template, svg', method:html);判定线=纯文本 >500 字且双跑 R2=unchanged

## Phase 0 robots(单次先行;四家复验 + deepseek 补档)

| vendor | status | allowed | 判据 |
|---|---|---|---|
| zhipu | 200 | ✅ | star-rules=[('allow', '/')] -> allow |
| moonshot | 404 | ✅ | robots 404 (default allow) |
| minimax | 200 | ✅ | star-rules=[('allow', '/'), ('disallow', '/api/'), ('disallow', '/_next/')] -> allow |
| seed | 200 | ✅ | star-rules=[('allow', '/')] -> allow |
| deepseek | 200 | ✅ | star-rules=[('allow', '/')] -> allow |

## Phase 1 页面 + 选择器初筛(每家单次抓取,本地过滤)

| vendor | page status | page bytes | selector | filtered html | 纯文本字数 | 预览 |
|---|---|---|---|---|---|---|
| zhipu | 200 | 899299 | `main` | 176904 | 2138 | 你好 我是 ZCode 头脑风暴 逻辑推理 信息问答 内容创作 创意开发 ZCode 简单、迅捷、氛围十足！ GLM模型 新一代大模型全栈技术体系 GLM-5. |
| zhipu | 200 | 899299 | `#app` | 0 | 0 |  |
| zhipu | 200 | 899299 | `#__next` | 0 | 0 |  |
| zhipu | 200 | 899299 | `#root` | 0 | 0 |  |
| zhipu | 200 | 899299 | `[role=main]` | 0 | 0 |  |
| zhipu | 200 | 899299 | `article` | 0 | 0 |  |
| zhipu | 200 | 899299 | `body` | 190813 | 2508 | GLM MaaS 产品 研究 关于我们 EN中 合作咨询 你好 我是 ZCode 头脑风暴 逻辑推理 信息问答 内容创作 创意开发 ZCode 简单、迅捷、氛围 |
| moonshot | 200 | 98191 | `main` | 0 | 0 |  |
| moonshot | 200 | 98191 | `#app` | 0 | 0 |  |
| moonshot | 200 | 98191 | `#__next` | 0 | 0 |  |
| moonshot | 200 | 98191 | `#root` | 35363 | 848 | Kimi企业服务API研究下载加入我们关于我们 Kimi企业服务API研究下载加入我们关于我们 寻求将能源转化为智能的最优解 体验 Kimi体验 API 最新研 |
| moonshot | 200 | 98191 | `[role=main]` | 0 | 0 |  |
| moonshot | 200 | 98191 | `article` | 0 | 0 |  |
| moonshot | 200 | 98191 | `body` | 36282 | 848 | Kimi企业服务API研究下载加入我们关于我们 Kimi企业服务API研究下载加入我们关于我们 寻求将能源转化为智能的最优解 体验 Kimi体验 API 最新研 |
| minimax | 200 | 339921 | `main` | 47648 | 1348 | 前沿 Coding /Agent 能力 真实工程级，不止生成代码，更懂协作 MSA · 1M 上下文 全新稀疏注意力，让 context 真正可 scale 原 |
| minimax | 200 | 339921 | `#app` | 0 | 0 |  |
| minimax | 200 | 339921 | `#__next` | 0 | 0 |  |
| minimax | 200 | 339921 | `#root` | 0 | 0 |  |
| minimax | 200 | 339921 | `[role=main]` | 0 | 0 |  |
| minimax | 200 | 339921 | `article` | 17859 | 376 | MiniMax M3 Coding 顶尖 · 1M 上下文 · 原生多模态 MiniMax H3 视频生成 MiniMax Speech 2.8 语音 Mini |
| minimax | 200 | 339921 | `body` | 72830 | 1727 | 模型 语言模型 MiniMax M3MiniMax M2.7MiniMax M2.5 视频生成 MiniMax H3 语音&音乐 MiniMax Speech  |
| seed | 200 | 128636 | `main` | 132488 | 2171 | Seed2.1 面向真实生产力场景的全新智能体 了解更多 技术博客立即体验 最新动态 SeedRealtime 音视频全双工大模型发布：走向全模态自然交互 20 |
| seed | 200 | 128636 | `#app` | 0 | 0 |  |
| seed | 200 | 128636 | `#__next` | 0 | 0 |  |
| seed | 200 | 128636 | `#root` | 82938 | 1694 | 首页模型博客&论文Seed Edge加入我们 首页模型博客&论文Seed Edge加入我们 开始体验 EN 首页模型博客&论文Seed Edge加入我们 开始体 |
| seed | 200 | 128636 | `[role=main]` | 0 | 0 |  |
| seed | 200 | 128636 | `article` | 2643 | 0 |  |
| seed | 200 | 128636 | `body` | 82953 | 1694 | 首页模型博客&论文Seed Edge加入我们 首页模型博客&论文Seed Edge加入我们 开始体验 EN 首页模型博客&论文Seed Edge加入我们 开始体 |
| deepseek | 200 | 115583 | `main` | 10870 | 395 | DeepSeek-V4.1-Flash 发布，文本与 Agent 性能全面提升、兼具原生多模态视觉理解能力，能力更强、速度更快、且成本更低，欢迎测试和反馈探索未 |
| deepseek | 200 | 115583 | `#app` | 0 | 0 |  |
| deepseek | 200 | 115583 | `#__next` | 0 | 0 |  |
| deepseek | 200 | 115583 | `#root` | 0 | 0 |  |
| deepseek | 200 | 115583 | `[role=main]` | 0 | 0 |  |
| deepseek | 200 | 115583 | `article` | 0 | 0 |  |
| deepseek | 200 | 115583 | `body` | 13272 | 490 | 获取 APP 扫码下载 DeepSeek App 中文EN DeepSeek 网页版DeepSeek HarnessAPI 开放平台API 文档DeepSeek |

## Phase 2 背靠背双跑(初筛 >500 字且 robots 允许者;R2=unchanged 才可接)

| vendor | selector | 纯文本 | R1 | R2 | 判定 |
|---|---|---|---|---|---|
| zhipu | `main` | 2138 | new | unchanged | ✅ 可接 |
| moonshot | `#root` | 848 | new | unchanged | ✅ 可接 |
| minimax | `main` | 1348 | new | unchanged | ✅ 可接 |
| seed | `main` | 2171 | new | unchanged | ✅ 可接 |
