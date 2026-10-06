# 实现段真跑记录(2026-10-06,prd §8-⑦ / AC 门控:20 条入库)

实例:本机探查栈 http://127.0.0.1:8888(colima docker,searxng-core +
valkey,json 开 + limiter 关,~/.searxng-probe;探查段留跑件复用,零新栈)。
冒烟前置:`/healthz` → OK;`categories=web` 一发 → 25 条(实时波动)。

## 命令(临时品类 + 临时库,不碰生产 myssia.db)

```sh
uv run --no-sync myssia run /tmp/myia-searxng-ac.yaml --once \
    --db /tmp/myia-searxng-ac.db --json
```

临时品类(evidence/2026-10-06-impl-realrun-category.yaml 原样):3 个
查询词(探查实测词集:舆情×2 + 事件×1),engine: searxng,push stdout,
dedup {url},classify builtin 关。涉网只对本机 8888 栈。

## 结果

| 轮 | status | engine | item_count | duration | 入库总数(items 表) |
|---|---|---|---|---|---|
| 1 | success | searxng | **127** | 13.5s | **127**(≥20 AC 门过) |
| 2(去重验证) | success | searxng | 122 | 16.5s | 135(净增 8) |

- 轮 1 failures:[] 零失败;runs 表记 engine=searxng、attempts=1。
- 轮 2 fetch 122 条(实时波动)而库只净增 8 —— 其余全被 `{url}` dedup
  短路:「去重走 feed 层既有 url metric 键」实证成立(同 URL 不同标题
  的重复结果不再入库)。
- 样例条目(zh.wikipedia / baike.baidu / dream.kotra.or.kr 系,与探查
  快照同源分布;title/content/query 字段齐全)。
- 完整机器输出:`…-realrun-1.json`(78KB 含全部条目)/ `…-realrun-2-dedup.json`。

## 截图口径

UI 零新面(源管理徽章=引擎字符串动态渲染,searxng 自动显示,无枚举面
可同步——见 prd AC4 注记),本 AC 以 --json 机器输出 + items 表计数落档
替代像素截图(桌面端装机徽章随下批,同 prd「装机件:装机包随下批」口径)。

## 清场

真跑后临时件(/tmp/myia-searxng-ac.yaml / -ac.db / run*.json)已拷贝
evidence 后删除;仓库根零临时残留;探查栈按探查段口径留跑不收。
