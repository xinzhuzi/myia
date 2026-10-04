# myssia-maigret — 用户名跨站侦察(maigret)

官方场景件(desktop 分级):对一个用户名跨站查占用/命中(maigret 官方站点库,
rank 前 N 站)。上游 [maigret](https://github.com/soxoj/maigret)(MIT)以
`uv run --no-project --with maigret` 隔离子进程调用,不 vendor、不复制源码,
依赖不进根依赖;版本不钉(站点库随上游自更新)。

## 桌面路径(默认)

```bash
myssia maigret torvalds --json                  # top-100 站,分钟级
myssia maigret someone --top-sites 300 --timeout 900   # 范围/预算可调
```

- `--top-sites N` 按站点 rank 前置预算(全库数千站可达数小时,慎用 `--top-sites 0` 之外的全量);
- `--timeout S` 是整个子进程 wall-clock 预算;逐站请求超时缺省 15s;
- 上游是 CLI 库,**无 remote endpoint**(无服务形态,亦无 token)。

## 输出形状(`--json`)

`hits[]` 字段:`site/url/status(恒 Claimed 族)/rank/is_similar/tags/ids`
(ids 仅保留标量,如 uid/follower_count)。**零命中=合法空态**(success 且
hit_count 0),不是错误。

## 失败语义(绝不拦核心)

`username_invalid`/`uv_missing`(配置类,退 1);`maigret_failed`/
`maigret_timeout`/`maigret_report_missing`/`maigret_report_invalid`(采集类,
退 2)。任何失败只影响本命令,核心品类流水线照常(`myssia doctor` 零影响)。

## 采集边界与留痕

逐站点直连查询(本机出口 IP 对各目标站点可见——采集固有);**零第三方聚合
服务器**,查询不经任何厂商 SaaS(P0 本地执行硬规则)。仅用于已授权侦察
目标;零凭据注入。
