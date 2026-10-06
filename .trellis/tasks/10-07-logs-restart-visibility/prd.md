# 日志屏历史跨重启可见:运行历史 DB 合流 + cron/feishu 入口统一收尾

## Goal

主人 2026-10-07 令「按照你的建议去做」——承接 10-07-unified-logging 归档勘误(run-report §8)的全部建议:让重启后的日志屏真正翻得到上一程(把回填的价值在 UI 落地),顺手修独立复查遗留两 low。前置勘误 commit 已入归档档。

## 现状与根因(勘误已核,勿重查)

- 运行历史数据源=sidecar **会话级**内存注册表(`run.status`→`_m_run_status`),重启即空;空态(`logs-screen.tsx:812` EmptyState)盖整卡,`logs.tail` 按运行行展开才惰性拉取——列表空则回填(协议层已生效,测试钉死)永不可见。
- DB `runs` 表已有跑次落库(f299432:stats_dict 含推送失败明细)——读史的基础在,未被 run.status 消费。
- 独立 `myssia cron serve` 走 cli.py 入口 `proc="cli"` 硬编码(cli.py `_configure_logging`);design 曾承诺 proc="cron"。
- `python -m myssia.push.feishu_callback` 独立进程入口仍是 ad-hoc `basicConfig`(feishu_callback.py:449)零持久化。

## Requirements

- **R1 运行历史跨重启可见(核心)**:`run.status` 改为「会话注册表(进行中/最新,现有语义)合流 DB runs 表历史」——重启后日志屏显示上一程跑次行(新→旧排序不变),历史行带徽标(如「上一程」)与同款状态/耗时/条目数;展开历史行→`logs.tail?run_id=N`→回填行(已生效能力,零新协议)。历史行数上限 50(防长列表)。**runs 表字段不足以支撑行展示时最小补字段落库(不动旧数据)**;注册表行与 DB 行去重(同跑次不双列)。无任何历史(全新装机)时空态现状不变。
- **R2 cron proc 细分**:独立 `myssia cron serve` 进程 proc="cron"(cli 入口传递);普通 CLI 仍 proc="cli"。测试双向钉死。
- **R3 feishu_callback 统一入口**:`logging.basicConfig` 退役,改经 `myssia.log.configure(mode="serve", data_root=<MYIA_HOME 感知解析>, ring=False, proc="feishu_callback")`;终端裸跑=stderr-only 沿决议②口径。测试:配置后 handler 集形状+MYIA_HOME 沙箱落盘。
- **R4 spec 同步**:sidecar-protocol.md `run.status` 行为补「DB 历史合流」语义(形状兼容声明);python/logging.md proc 枚举补 cron/feishu_callback。

### 非目标

- 不做「UI 日志进日志屏」(决议④可选项,不随本任务解禁)。
- 不动并行任务 dashboard-trend-today-fix 的域文件(dashboard/feed 趋势面)。
- 不引入 runs 表 schema 大改或数据迁移(最小补字段即可,若必需)。

## Acceptance Criteria

- [ ] AC1 重启后历史可见(协议):`run.status` 在新 serve 实例返回 DB 历史跑次行(含徽标字段/去重/上限 50),注册表进行中行合流在前;空库时空态形状与现状全同(零回归)。
- [ ] AC2 像素级装机验证:换装后真机跑一次采集→重启 App→日志屏**显示上一程跑次行**,展开该行**可见日志行(回填)**——截图 PaddleOCR 复核文字实据(收尾代理无图像输入时必须走 local-ocr 车道,不留主人)。
- [ ] AC3 cron/feishu proc:测试钉死 cron serve=proc:"cron"、普通 CLI="cli"、feishu_callback 配置后 handler 集与落盘形状。
- [ ] AC4 spec 两档同步入档。
- [ ] AC5 门禁全绿:定向 pytest+ruff / `just test-ui` / 收尾 `just test`+`just check`;gitnexus impact 前置(run.status 触及面)+ detect-changes。
- [ ] AC6 并行安全:全程未触碰 dashboard 域文件与并行任务档;提交外科 pathspec;task.json 状态直改(不用 task.py start/finish/archive)。

## 过程(执行流水,回填位)

- (空位;执行由此续填)

## 结果(验收回执,完工填)

- (空位)
