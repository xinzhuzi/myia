# L2 详情采集成果区(stats 成果卡+条目预览)

## Goal

主人报障(10-12 晚,截图 #88 详情页):L2 没展示「本轮最终采集到了什么」——
元信息+日志体之间缺成果答案位。补采集成果卡 + 条目标题预览,门禁+换装。

## Requirements(已交付)

1. **采集成果卡**(OutcomePanel,失败原因区的对偶):保留 N 条
   (items_retained)+ 每源行(源名 · 引擎 · N 条 · 耗时 · 跳过原因/失败
   如实)+ 推送概要(渠道 ✓/✗ · 直发/日报/归档数)+ 入库失败计数;数据 =
   record.stats(run.status 行随身,零新协议)。渲染门槛:running/无记录/
   空 stats 一行不出。
2. **条目标题预览**:store.items?category+since=started_at(零新协议)
   惰性拉,客户端按 first_seen ≤ finished_at 截窗(后继轮不混入);前 8 条
   标题+相对时间,超出报「另 N 条(情报流可看全)」;拉取失败如实一行。
3. 布局:面板 shrink-0(塌缩律 67546cd 同门),源行/预览各自 max-h 内滚。

## Acceptance Criteria

- [x] AC1 L2 终态轮直出成果卡:保留 N 条 + 每源行 + 推送概要(vitest 39 绿
      + 冒烟「成果区」断言:保留/src-alpha/8 条/跳过/src-delta/失败全中)。
- [x] AC2 条目预览:窗内标题在场、窗外条目被 finishedAt 截窗剔除(冒烟
      「条目预览」断言 + vitest not.toContain 截窗用例;running 行零请求)。
- [x] AC3 门禁:build/vitest 764/pytest 定向 547/冒烟全绿;tauri 重打包
      静默换装(见终局回执)。

## 边界

- 条目「全量列表」不在此做(情报流是全量视图,预览只是答案位;点开条目
  详情属 feed 域已有能力)。
- 旧库行 stats 缺 push 键 → pushes 空数组如实无推送行。
