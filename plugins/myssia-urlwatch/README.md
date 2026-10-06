# myssia-urlwatch — 轻量变更监控(urlwatch)

官方场景件(desktop 分级):对一组 URL 做快照对比监控——每跑一次,产出
`new`/`changed`/`unchanged`/`error` 事件与统一 diff。上游
[urlwatch](https://github.com/thp/urlwatch)(BSD-3-Clause,2026-10-05 对
2.29 装包源码 license 头亲核)以 `uv run --no-project --with urlwatch`
隔离子进程调用,不 vendor、不复制源码,依赖不进根依赖;版本不钉。

与 `myssia-monitor`(changedetection.io,remote 桩)互补:本件是**本地零
docker** 形态的轻量监控,适合桌面侧小批量 URL 的快照对比。

## 桌面路径(默认)

本批交付程序面(adapter,进程内可调;CLI 子命令/引擎面归后续批次)。适配器
经 `myssia.cli._import_plugin_adapter(plugins_dir, "myssia-urlwatch")` 装载
(compile+exec,插件目录不是 Python 包),或任何等价的进程内加载:

```python
from myssia.cli import _import_plugin_adapter
adapter = _import_plugin_adapter("plugins", "myssia-urlwatch")
adapter.run(["https://example.com/a", {"name": "示例", "url": "https://example.com/b"}])
```

- 快照缓存落 `~/.myia/urlwatch/cache.db`(minidb,跨 run 持久)——**首次跑
  全部 `new`**,之后才有 `changed`/`unchanged` 判定;可用 `cache_file=`
  换路径(测试/多租户隔离);
- `timeout` 是整个子进程 wall-clock 预算(缺省 300s);上游逐 job 请求
  超时缺省 60s;
- 输入收 `http://`/`https://` URL(≤64 条/次,重复自动去重保序),以及
  10-06 §12 起的 shell 型 job(`{name, command, user_visible_url}`;
  `user_visible_url` 必填且锚住事件 location/guid)。

## 渲染通道(纯客户端渲染页,10-06 §12)

`render_crawl4ai.py`(本目录)是 JS 渲染页的取正文体:urlwatch 引擎配
`engine_options.urlwatch.render: crawl4ai` 时,job 换上游 ShellJob 形态,
命令 stdout 即快照对象——helper 用 crawl4ai 无头渲染目标页,把正文归一成
纯文本(图片/链接 URL 剔除,CDN 签名轮换噪声出局)打印 stdout。适用面:
静态通道 CSS 选择器取不到正文的纯客户端渲染页(ai.meta.com/blog 实证,
六选择器全零);与 `selector` 互斥。前置:运行 myssia 的解释器环境需装
crawl4ai(缺=引擎结构化 `dependency_missing`)。

## 输出形状(`run()` 返回)

`counts{new,changed,unchanged,error,deferred}` + `events[]`(每条
`event/name/location/diff`(changed 带,尾部截断 4000 字)/`error`(error
带))。**零变更=合法空态**(status success 且 changed 0),不是错误;
`deferred` 是上游 max_tries 重试未到报错阈值、本轮不判定的 job 数。

## 失败语义(绝不拦核心)

`url_invalid`/`uv_missing`(配置类);`urlwatch_failed`/
`urlwatch_timeout`/`urlwatch_output_invalid`(采集类)。任何失败只影响
本次调用,核心品类流水线照常(`myssia doctor` 零影响)。上游依赖缺失时
结构化报 `uv_missing`(依赖只进 uv 临时环境,永不进根依赖)。

## 采集边界与留痕

逐 URL 直连抓取(本机出口 IP 对目标站点可见——采集固有);**零第三方聚合
服务器**,不经任何厂商 SaaS(P0 本地执行硬规则)。上游 2.29 无 JSON
reporter,子进程内由 MYIA 自写薄 shim 借其 Python API
(`worker.run_jobs` + 事件 collector)产出结构化 JSON,上游代码零入库;
零凭据注入(无需 token;上游是 CLI 库,无 remote endpoint)。
