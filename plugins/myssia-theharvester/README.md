# myssia-theharvester — 域名侦察(theHarvester)

官方场景件(desktop 分级):对域名/组织做一次开源情报聚合侦察(邮箱、子域、
IP、ASN 等)。上游 [theHarvester](https://github.com/laramies/theHarvester)
(GPL-2.0)以 git submodule 钉在 `vendor/theHarvester`(照 myssia-osint/Photon
样板:零复制、零修改、零分发),适配器经 uv 临时环境(`--no-config
--no-project --with <钉版依赖>`,与上游 pyproject 同源)隔离子进程调用;
依赖不进根依赖。上游 pip 包为空壳不可用(2026-10-05 实测),故走源码形态。

## 桌面路径(默认)

```bash
git submodule update --init plugins/myssia-theharvester/vendor/theHarvester  # 首次
myssia harvester example.com --json                     # 缺省凭据免费源 crtsh+dnsdumpster
myssia harvester example.com --sources crtsh,dnsdumpster,hackertarget --json
```

- `-f <临时目录>/harvest` 让上游同时落 harvest.json/.xml/.jsonl,适配器读
  JSON 装配结构化条目;
- 源清单可调(上游 `--source-list` 可见全量;带 key 的源如 shodan 未配
  凭据会被上游跳过);范围/页数经上游 `-l` 限;
- 上游是 CLI 库,**无 remote endpoint**(无服务形态,亦无 token)。

## 输出形状(`--json`)

emails/hosts/ips/asn 等按上游 JSON 分桶装进 `results`;`source_list` 为
实际执行的源清单。零命中=合法空态(success 且各桶空)。

## 失败语义(绝不拦核心)

`domain_invalid`/`vendor_missing`/`uv_missing`(配置类,退 1);`harvester_failed`/
`harvester_timeout`/`harvester_report_missing`/`harvester_report_invalid`
(采集类,退 2)。任何失败只影响本命令,核心品类流水线照常。

## 许可与边界

GPL-2.0 上游只以 submodule 引用;仅用于已授权安全研究与自有/已授权资产
的侦察;本机直连零第三方聚合服务器(P0 本地执行硬规则)。
