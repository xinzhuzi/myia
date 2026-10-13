# AC1/AC2 真库实证留档(2026-10-14,实现员会话)

## AC1 keyset 等价(真库,只读)

命令:`.venv/bin/python .trellis/tasks/10-14-wechat-chat-export/research/real_check.py`
(脚本即留档;输出副本 = `real_check_output_20261014.txt`)

```
shard=message/message_0.db::Msg_3aec884d788fe4e43dfb44afa6725f7f rows=9821 pages=20 elapsed=245ms
keyset_sequence_equal=True
explain_plan(no index yet)=SCAN Msg_3aec884d788fe4e43dfb44afa6725f7f | USE TEMP B-TREE FOR ORDER BY
census_mapping_consistent=True (mismatches=[])
RESULT: PASS
```

- keyset 逐页拼接(desc,批 500)vs 单次 `ORDER BY create_time,rowid` 全量:序列与总条数一致(9821 条)。
- 未建索引时计划 = `SCAN + USE TEMP B-TREE FOR ORDER BY`(索引自举动机实证);
  建索引后 `SEARCH … USING COVERING INDEX` 断言 = 合成夹具单测
  `tests/wechat-bridge/test_localdb_page.py::test_index_bootstrap_creates_marker_and_explain_search`。
- 真库端到端 AC1(带索引翻页 p95 ≤ 2s)与 AC5 留 CLI 集成后复查员跑
  (本会话保持副本零写:未调 ensure_page_index/scan_conversations 落缓存)。

## AC2 类型普查(零内容)

- 基件:`tests/wechat-bridge/fixtures/local_type_census.json`
  (message_0.db 249 表 609,915 条 + biz_message_0.db 195 表 8,041 条;
  逐 local_type 形状计数 + 映射证据)。
- 大数变体解码规律(逐变体抽样 XML 验证):`localType = (appmsg_subtype << 32) | 49`,
  hi32 与 `<appmsg><type>` 子节点同值;群消息 XML 带 `wxid:\n` 前缀(人话化前剥离)。
- 抽样实证:5→链接卡(url)、57→引用(refermsg)、6→文件(totallen)、
  19→合并转发(title=群聊的聊天记录,recordinfo 缺席 → 如实降级)、
  50→voipmsg(通话)、42→名片、47→emoji description。
- 映射覆盖:已知名 617,872/618,000 行;未知回落 `type_<N>` 占 0.96%
  (长尾 top:266287972401 拍一拍族 2,034 / 8594229559345 红包 1,210 /
  219043332145 1,016 …… 详见基件 `coverage` 节;不臆造)。

## 设计拷问修正落实记录(实现员侧)

- ①R2 普查缓存:按副本指纹(两库 mtime_ns+size)落 `decrypted/conversations-census.json`
  (0600),失配重扫;普查原语 `localdb_page.scan_conversations` 供 C2 复用(集成员接线)。
- ②索引自举:标记键取值时点 = CREATE INDEX **之后**(`ensure_page_index` 内
  fresh_fp);建索引走 `.rebuild.lock` 类式排他锁(刻意不用 @contextmanager:
  其退出路径的 Python 级 `exc.__traceback__` 赋值会炸 frozen BridgeError,实测)。
  C2 mtime+size 指纹被建索引刷新失效一次 = 已知一次性成本(注释注记)。
- ③C2 边界注记失实:集成侧修 prd.md:103(C2 自建 stats 聚合,不走逐页通道;
  真实耦合 = R3 映射先定型)。
- ④版本 0.8.0 五档撞号:集成侧统一裁决(本档 integrationSpec 标注)。
