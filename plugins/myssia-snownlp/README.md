# myssia-snownlp — 中文情感装饰(snownlp)

官方场景件(desktop 分级,**门槛件:停更知情**)。上游
[snownlp](https://github.com/isnowfy/snownlp)(MIT)是中文情感分析经典库,
最后推送 2020-01-19 —— 上游已冻结,收录为分析 lane 装饰件:对本轮条目
(title+content)算一个贝叶斯正面概率,落条目 `metadata` 的
`sentiment_score`(0..1,越高越正面)与 `sentiment_label`(正面/负面),
供 route 规则与推送模板消费。零复制:MYIA 侧只有本目录的 adapter.py
(MYIA 自写),上游以 pip 依赖形态经 uv 临时环境注入。

## 桌面路径(desktop 分级,零 docker)

纯本地分析件,无 remote endpoint、无服务形态、零网络零凭据。上游依赖由
adapter 以 `uv run --no-project --with snownlp==0.12.3` 隔离子进程注入
(pin 号 = 2026-10-05 收录时 PyPI 末版;宿主需有
[uv](https://docs.astral.sh/uv/));每轮单次 spawn 批处理(snownlp import
即载训练模型,不逐条 spawn)。

## 为什么有门槛(stale,停更知情)

上游 2020 年起冻结:不会再有修复版,pin 版 = 你自担维护(安全/兼容问题
无人上游兜底)。知情后开启:

```
myssia gates set analysis.snownlp on
```

(或桌面 设置→门槛件→分析件 分区。)开启后 `myssia plugin list` 门槛件分组
显示「已启用」徽标,doctor 由 info 转 ok;未启用是正常态(info,不是故障)。

## 运行时语义(批三分析 lane,真执法)

- 挂点:管线的 analyze 阶段(dedup 之后、push 之前),与 LLM 精评同位互补;
  **装饰不过滤**——情感结果不改变任何条目的存活,LLM 精评关闭时 lane 照常可用;
- 开关关闭(缺省)= 字面零开销:不 import 插件码、不 spawn 子进程、条目零触碰;
  gates.yaml 缺失/损坏 = 全关 = lane 不跑(fail-closed,装不上不拦核心);
- 分析件失败(uv 缺失/子进程失败/超时/输出坏)= 降级注记(report.warnings +
  `analysis_lane_degraded_*` 计数),条目照常投递,**绝不翻 partial 退出码**。
