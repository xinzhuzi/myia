# myssia-media — 视频情报(yt-dlp)

官方场景件(desktop 分级):对视频/频道/播放列表 URL 做一次「扁平快扫」,
产出标题/链接/频道/时长/观看数等结构化条目。上游 [yt-dlp](https://github.com/yt-dlp/yt-dlp)
为 Unlicense(公域),以 `uv run --no-project --with yt-dlp` 隔离子进程调用,
不 vendor、不复制源码,依赖不进根依赖。

## 桌面路径(默认)

```bash
myssia media "https://www.youtube.com/watch?v=…" --json          # 单视频元数据
myssia media "https://www.youtube.com/@channel" --json            # 频道扁平快扫(≤50 条)
myssia media "…" --max-items 100 --timeout 300                    # 条目/预算可调
```

- `--flat-playlist` 扁平快扫:频道/列表不逐条解析媒体流,轻量出清单;
  `--max-items N` 经上游 `--playlist-end` 前置预算。
- 版本不钉:每次运行取 uv 缓存里最新的 yt-dlp(抽取器时效即生命)。
- 上游是 CLI 库,**无 remote endpoint**(无服务形态,亦无 token)。

## 输出形状(`--json`)

`entries[]` 字段白名单:`id/url/title/uploader/channel/duration/view_count/upload_date`;
`entry_total` 为上游总条数(截断前),`meta` 为单视频/频道头部信息。

## 失败语义(绝不拦核心)

`url_invalid`/`uv_missing`(配置类,退 1);`media_failed`/`media_timeout`/
`media_output_invalid`(采集类,退 2)。任何失败只影响本命令,核心品类
流水线照常(`myssia doctor` 零影响)。

## 采集边界

目标由使用者指定,须遵守目标站点服务条款与当地法律;本件不做任何凭据
注入,仅公开可访问内容。零成本:本机直连,无第三方服务器。
