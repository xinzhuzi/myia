# wechat-bridge 密钥子系统固化(C 收集器+验证管道+setuid 自愈)

## Goal

密钥获取全链固化进桥组件:三模式 C 收集器(字符串/裸hex/salt邻域)+sqlcipher 验证管道(熵筛+并行+参数变体)替换天文数字的 Python 滑窗实现+setuid 自愈件(密钥失效零人工重取)+一键脚本 v2;主人令 2026-10-13「全部固化成代码落实到项目中」

## Requirements

- 密钥获取全链固化进桥组件(三模式 C 收集器+sqlcipher 验证管道替换 Python 滑窗+setuid 自愈+一键脚本 v2),使 passphrase 失效时零人工重取。

## Acceptance Criteria

- [x] AC1 C 收集器三模式固化(46a4fac,0.4.0):plugins/wechat-bridge/native/collector.c(字符串/裸hex/salt邻域三模式)+memsearch.py 重写+install-keyscanner.sh+scripts/wechat-bridge-d4-keyscan.sh 脚本 v2,产物在树亲证。
- [x] AC2 自愈件(289d96f,0.4.1):失效退避/冷却门,密钥失效零人工重取路径在库。
- [x] AC3 复审修收编(e07a81d)+ Ghidra 技能与研究档入库(80fb1a2:.zcode/.agents 双技能+ghidra-static-keyhunt.md,含 32B XOR 掩码 FUN_058ba638 实锚)。

## 收口注记(2026-10-14 收编批)

档件(本 prd+task.json+两 jsonl)建档后未随代码提交(10-13 07:23 后该线停更 17h+,判活=会话已离场,按收编判例代为关档)。遗留:low⑤「C 合成镜像测试台」(e07a81d 复审注记)留档后续,不阻塞收口。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
