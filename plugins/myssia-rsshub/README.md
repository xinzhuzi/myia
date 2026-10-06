# myssia-rsshub — RSS 源扩容(RSSHub)

官方场景件(remote 分级):接入一个已部署的 [RSSHub](https://github.com/DIYgod/RSSHub)
实例,把「没有 RSS 的站点」变成 RSS 路由,喂进 MYIA 品类的 RSS 通道
(`extract.type: rss`,与 news.yaml 同通路)。上游 AGPL-3.0,只以 manifest
+文档引用接入,零源码复制。

## 接入路径(remote:填 endpoint)

1. 自部署优先(零第三方):按上游 [RSSHub 官方部署文档](https://docs.rsshub.app/)
   起一套(官方镜像 `diygod/rsshub`;启用访问控制时注入
   `RSSHUB_ACCESS_KEY`)——部署属主人运维面,插件不提供 docker 模式,
   我方不复刻配方;
2. 把实例地址填进 endpoint(品类 YAML 的 `plugin.modes.remote.endpoint`);
   启用访问控制的部署再把键写入钥匙串:
   `myssia secret set myia/rsshub/access-key`;
3. 品类源即可引用 RSSHub 路由,如:

```yaml
sources:
  - name: rsshub-microsoft-blog
    engine: static_html            # RSS 通路与 news.yaml 同构
    url: "https://rsshub.example.com/microsoft/blog"
    extract:
      type: rss
      fields: {title: title, url: link, time: published}
```

## 留痕与成本(主人 P0 裁决)

- **自部署 = 零成本零第三方**(推荐缺省):查询只经过你自己的实例;
- 公共实例 `rsshub.app` 免费但属第三方服务器:你的订阅路由清单会经过对方
  且有限速——可临时用,不作缺省推荐;
- 上游是 Web 服务,不可进程化,故 remote 分级(桌面默认集不携带)。

## 铁律

实例不可达/路由 404 只降级为源级结构化失败,核心品类流水线照常
(装不上不拦核心;`myssia doctor` 可见)。
