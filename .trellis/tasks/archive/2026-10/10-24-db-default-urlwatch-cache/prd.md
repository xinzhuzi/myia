# PRD — cli --db 缺省与 urlwatch 缓存路径两坑修复

## Goal

收编执行(10-24-huawei-ai-news-absorb)踩出的两个同型「沙箱失锚」坑修掉:MYIA_HOME 在场时数据面必须锚定到 env 指的数据根,终端无 env 行为不变。

## Requirements

- R1 顶层 `myssia run --db` 缺省复用 `_cron_default_db()` 语义(MYIA_HOME 设→`$MYIA_HOME/myssia.db`,不设→`./myssia.db` 不变)——s5 误推事故根子(沙箱跑漏进仓库根开发库);其余子命令(listing/doctor/feed 等读侧面)不动,留档。
- R2 urlwatch 快照缓存缺省解析上收引擎侧:cache_file 选项缺省时引擎显式传入解析值(MYIA_HOME 设→`$MYIA_HOME/urlwatch/cache.db` 并建父目录,不设→遗留 `~/.myia/urlwatch/cache.db` 不变)——s3 误删真根事故根子;adapter 自身遗留兜底不动(独立运行面),模块注释改为如实。
- 纯行为修:零 schema 变更、零新依赖;cron 组与显式 `--db`/`cache_file` 路径恒优先不变。

## Acceptance Criteria

- [x] AC1 run 缺省锚定:MYIA_HOME+cwd≠home 跑 `myssia run` store 落 `$MYIA_HOME/myssia.db` 且 cwd 零落盘;无 env 时 cwd 行为逐字节不变(测试钉住)。
- [x] AC2 引擎传参:fake adapter 捕获 cache_file=解析值(MYIA_HOME 形/遗留形两测);MYIA_HOME 形父目录自动创建。
- [x] AC3 全量门禁:pytest 全量零新红 + ruff 过。
