# myssia-maxun — 无代码爬虫平台(Maxun)

官方场景件,v1.1 分级 **server-only(桌面默认集移出)**:浏览器录制式
无代码爬虫(recorder 机器人 → 结构化数据/REST API/定时任务)。封装上游
[getmaxun/maxun](https://github.com/getmaxun/maxun)(约 17.6k stars,
**AGPL-3.0 License**)。

> 许可边界:AGPL 上游只以 **manifest 声明依赖 + 文档引用**接入;本仓库
> 不复制、不修改、不分发 Maxun 的任何源码。
>
> 为什么移出桌面默认集:上游是 Electron 应用 + 多容器栈(postgres +
> minio + backend + frontend + browser),不可进程化 —— 桌面路径(源码/
> 进程内优先)不携带它。可用形态只有一种:**任意已部署实例按 remote
> 模式接入**;插件不提供 docker 模式,部署配方归上游官方文档
> (见下文「实例从哪来」)。

## 桌面路径(remote 接入,零 Docker)

已有部署(自托管实例或上游托管版)时,品类 YAML 填:

```yaml
plugin:
  id: myssia-maxun
  modes:
    remote:
      endpoint: https://maxun.example.com   # 换成你的实例地址
```

- `provides: [maxun]`:把任意站点录制成机器人,产出结构化数据;myia 侧
  经 L1 `direct_api` 消费其导出接口/REST 端点。
- 装不上/不可达 → 结构化 warning,不拦核心流水线(铁律)。

上游鉴权为控制台会话(浏览器登录),没有稳定的 API token 契约,故本插件
不声明 token;若你在实例前加了带 token 的网关,把 token 写入钥匙链
(`myssia secret set myia/maxun/<name>`)后在品类侧按
`keychain:myia/maxun/<name>` 引用。

## 实例从哪来(部署属主人运维面,我方不复刻配方)

MYIA 不携带任何插件部署配方(终裁 2026-10-06:插件 docker 模式全删)。
Maxun 是多容器栈(postgres + minio + backend + frontend + browser),
自备实例按上游仓库官方部署文档操作(`.env` 从上游 `.env.example`
复制变量清单逐项填值,口令自生成、零明文入库;部署默认只绑回环,
控制台注册首个账号即管理员)。部署好后,把实例地址按上一节 remote
接入填给 MYIA。

## 凭据红线

- 本插件全部文件零明文凭据;部署侧口令在上游部署面自行注入,`.env`
  不入库、不进本仓库。
- 仓库即公开:实例地址只用 `example.com` 占位。

## 安装 / 移除

```bash
myssia plugin install plugins/myssia-maxun
myssia plugin list --json
myssia plugin remove myssia-maxun
```
