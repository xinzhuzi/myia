# 直发回执精确正文修复（2026-10-18）

问题：CLI 共用回执闭包通过 _compact_body 删除正文全部空白，导致“今天 真好”和“今天真好”等不同正文匹配。

修复：_receipt_query_closure 新增 keyword-only exact_text=False；send_direct 明确传 True，逐字符比较；send_text 保留默认语义。时间判断和未知结果不变。未改变驱动拒绝门，未部署。

影响分析：GitNexus 对 _receipt_query_closure 返回 LOW，直接调用者 cli.main，传递影响 __main__.py，1 个执行流；对限定文件的 main 返回 LOW，直接调用者 __main__.py。

验证：新合成测试修复前 13 failed / 1 passed，其中 6 个 CLI 集成用例明确复现空白不同仍返回 True。修复后相关测试 91 passed / 1 skipped；桥接模块全套 856 passed / 14 skipped（9.45s）；修改的 Python 文件 Ruff 通过。新测试共 14 项，覆盖空白变体、精确命中、旧消息、不同正文、默认 UI 兼容及不可用查询。发送/数据库/进程边界使用替身，没有真实微信、调试器、数据库或账号操作。

边界：正文精确匹配不能证明出站方向、新消息唯一性或服务端送达；原有 2 秒容差仍可能命中窗口内同正文历史消息。完整业务保持、原生调度/取消最终释放、完整适配、真正发送及独立回执仍未完成。A7、L3 和原开放项维持不变，账号安全停止约束保持，不启用驱动、不装机、不归档、不执行 Git。
