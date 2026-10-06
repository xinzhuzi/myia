# probe6 — Meta 博客重接探查与渲染通道实证(2026-10-06 §12)

> 承 §10/§11 口子⑤「Meta 重接需 JS 通道(另立档)」。本轮三证:crawl4ai
> 渲染可达、urlwatch 上游 shell 型 job 契约、离线端到端管线。涉网仅一次
> (ai.meta.com/blog 单页单加载,零压力;robots 复用 probe3 在案证据
> `User-agent: *` 段允许 `/blog`,不重复打)。UA 不伪装——playwright
> headless Chromium 真实身份即生产足迹。

## 1. crawl4ai 渲染探针(真网单次)

- 脚本/结果:`probe6-meta-crawl4ai.py` / `probe6-meta-crawl4ai.json` /
  正文摘录 `probe6-meta-crawl4ai.markdown.txt`(40KB 截断)。
- 命令:`.venv/bin/python .trellis/tasks/10-06-ai-news-sources/evidence/probe6-meta-crawl4ai.py`
- 结果:**success=true,7.3s,html 209KB,markdown 17345 字**;markdown 里
  `/blog/<slug>` 链接 **5 条**(静态通道实证为 0):introducing-muse-spark
  -meta-model-api(7/9)、assistive-robotics-university-of-pittsburgh-sam
  -dino(7/27)、genesis-mission-…-segment-anything-dino(7/21)、
  introducing-muse-image-muse-video-msl(7/7)、brain2qwerty-…(6/29)。
  标题+日期+分类全可读(「The latest AI news from Meta」列表完整)。
- 噪声源实证:markdown 内 fbcdn 图片 URL 带 `oe=`/`_nc_oc=` 轮换签名
  参数(如 `oe=6ACA3439` vs `oe=6ADECAFE` 同页不同图)——保留即逐次
  快照漂移。处置:helper 归一化剥图片/链接 URL 只留文本
  (`strip_markdown_noise`,单测钉死「仅签名不同两份 markdown 归一相等」)。
- 出口注记:本轮 env 无代理变量(env_proxy 全 null),直连可达。

## 2. urlwatch 2.29 shell 型 job 契约(本地零目标网)

- 命令:`printf` 写 jobs 文件(1×shell 型 `{name, command,
  user_visible_url}` + 1×url 型)→ `uv run --no-project --with urlwatch
  python -c "UrlsYaml(...).load()"`。
- 结果(zread thp/urlwatch master `lib/urlwatch/jobs.py` 亲核 + 2.29 装包
  实测一致):**ShellJob 装载成功,`get_location()` 返回 user_visible_url
  (页面 URL,非命令串),`pretty_name()`=name,guid=sha1(location)**——
  引擎的事件匹配(`event.location == url`)零改动即适配 shell 型。
- ShellJob 执行面:`subprocess.Popen(command, shell=True)` → 命令串必须
  三段引号隔离(引擎 `build_render_command`:POSIX shlex / win32
  list2cmdline,单测钉死)。
- 上游另有 BrowserJob(kind: browser, playwright)但跑在 uv 临时环境,
  playwright 浏览器二进制不在彼处——shell 型 + 宿主解释器跑 crawl4ai 才通。

## 3. 离线端到端(真 uv 子进程 × 3 跑,零目标网)

- adapter 真链(normalize → jobs YAML → uv+shim → 上游 worker.run_jobs →
  ShellJob → JSON 事件),command=`printf blog-A...`(echo 形,不打目标站):
  - run1:**new**(location=`https://ai.meta.com/blog`);
  - run2(同输出):**unchanged**(快照对比在命令 stdout 上成立);
  - run3(输出加行):**changed**,diff 为标准 unified diff。
- 结论:shell 型 job 全语义(new/unchanged/changed/diff)在上游原样成立,
  渲染通道只是把「命令」换成 helper。

## 4. RSSHub meta 路由(S3 邻近选项记档)

- `gh search code --repo DIYgod/RSSHub 'ai.meta.com'` 命中
  `lib/routes/meta/ai-blog.ts`(zread 亲读):路由 `/meta/ai/blog`,
  maintainer TonyRL;机理=静态抓页取 DTSGInitialData→LSD token→POST
  `ai.meta.com/api/graphql/`(doc_id 9516719638450392,
  MetaAIBlogRecentPostSearchQuery)。
- 定性:**存在但非捷径**——同受 S3 前置一(本机 Docker 已卸载)阻塞,
  且依赖 Meta 私有 GraphQL doc_id(漂移脆弱性与 RSSHub twitter 路由同款,
  §3 在案)。自部署 crawl4ai 渲染通道不依赖该私有 API 面。

## 5. 实现面回执(同轮落地)

- 引擎 `src/myssia/engines/urlwatch.py`:`engine_options.urlwatch.render:
  crawl4ai`(词表 `RENDER_BACKENDS`;与 selector 互斥结构化拒)+ shell job
  构造(`user_visible_url` 锚事件定位)+ `_render_helper` 前置
  (helper 件缺失=`render_helper_missing`、后端未装=`dependency_missing`)。
- 场景件:`render_crawl4ai.py`(自包含 stdlib+crawl4ai 惰性 import;退出码
  0/1/3);adapter `normalize_urls` 双轨(url 型/shell 型,后者
  user_visible_url 必填+command 形状校验+按 location 去重)。
- 测试:引擎件 +8(render 构形/互斥/两缺失态/命令引号两平台/锚点路径)、
  插件件 +8(shell job 接受/拒形/去重/名字派生/过滤透传)、helper 件新
  6(归一化×3+CLI 退出码×3)、插件包守卫豁免清单 +render_crawl4ai.py。
- 门禁:ruff check 绿+format 落定;定向三件 96/96;插件包守卫 262/262;
  **全量 pytest 4527 passed / 0 failed / 0 errors**(首轮 1 失败=插件包守卫
  豁免缺项当场修、1 失败+2 ERROR=并行会话在途编辑中间态,复跑两连清)。
- gitnexus impact:`normalize_urls` 实跑 LOW(1 调用方 adapter.run);
  引擎符号因索引 WAL 态读路径失效,以 rg 全树普查替代(UrlwatchEngine 仅
  registry.py:130 惰性注册+自有模块+引擎测试引用,接口面零变)。
