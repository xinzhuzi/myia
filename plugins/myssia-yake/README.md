# myssia-yake — 关键词装饰(yake)

官方场景件(desktop 分级,无门槛声明)。上游
[yake](https://github.com/LIAAD/yake)(AGPL-3.0 免费档+商业双轨,2026-02
仍活跃)是无监督关键词抽取库:不依赖词典与语料,对任意文本直接抽关键词。
收录为分析 lane 装饰件:对本轮条目(title+content)抽取关键词,落条目
`metadata` 的 `keywords`(列表),供 route 规则与推送模板消费。
AGPL 纪律:只声明依赖零复制——本目录只有 MYIA 自写 adapter.py,上游
以 pip 依赖形态由用户运行时自装(pip 运行时装包不构成分发)。

## 桌面路径(desktop 分级,零 docker)

纯本地分析件,无 remote endpoint、无服务形态、零网络零凭据。进程内形态
(惰性 import):启用前先把上游装进宿主环境——

```
uv pip install yake     # 2026-10-05 PyPI 末版 0.7.3
```

未装 = `dependency_missing` 条目级降级 warning(条目照常投递,绝不拦核心)。
中文说明:YAKE 的分词器面向空格分隔文本,adapter 已做 CJK 逐字切分前置
(连续汉字间插空格);启发式抽取,关键词是辅助信号不是分类依据。

## 为什么无门槛声明,但仍需开关

上游活跃(非 stale)、许可核验已过(AGPL 免费档可用,设置面无关)——
manifest 不声明 gate。但批三分析 lane 的纪律是:**lane 件一律显式开启才跑**
(缺省关闭来自 D2「永不缺省」,不依赖 manifest 徽标)。启用:

```
myssia gates set analysis.yake on
```

(或桌面 设置→门槛件→分析件 分区。)`myssia plugin list` 的 lane 成员
启用徽标派生自 `analysis.yake` 开关。

## 运行时语义(批三分析 lane,真执法)

- 挂点:管线的 analyze 阶段(dedup 之后、push 之前),与 LLM 精评同位互补;
  **装饰不过滤**——关键词不改变任何条目的存活,LLM 精评关闭时 lane 照常可用;
- 开关关闭(缺省)= 字面零开销:不 import 插件码、不触碰条目;gates.yaml
  缺失/损坏 = 全关 = lane 不跑(fail-closed,装不上不拦核心);
- 分析件失败(未装 yake/抽取失败)= 降级注记(report.warnings +
  `analysis_lane_degraded_*` 计数),条目照常投递,**绝不翻 partial 退出码**。
