"""myssia.telegram —— Telegram 消息面(10-06-telegram-telethon).

包布局(按批次落地):

- :mod:`myssia.telegram.filter`(B2)—— 过滤管线:关键词粗筛(零成本)
  → LLM 精筛打分(glm-4-flash,grill Q5:≥8 分即时)→ 高价值同轮合并
  单条(组合铁律)/ 普通入库。批量引擎(``myssia.engines.telegram``)与
  常驻宿主(serve,B3)两档共用(design D1「两档共用」决议)。
- :mod:`myssia.telegram.serve` + :mod:`myssia.telegram.offsets` +
  :mod:`myssia.telegram.events`(B3)—— 常驻宿主:getUpdates 长轮询
  (25s 挂起)/ offset 持久断点续拉 / 断线指数退避 / 消息级事件账本
  (executions 形态新表 telegram_events);``myssia telegram serve`` CLI +
  桌面 sidecar 接线位(TelegramServeHost 可嵌入,详 serve 模块文档)。

命名边界:本包是**消息获取面**(收);Telegram 作为推送出口的通道适配器
在 :mod:`myssia.push.telegram`(发),二者分属引擎/通道两词表,互不相干。
"""
