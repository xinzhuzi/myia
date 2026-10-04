# Design:定时任务管理屏(照 Hermes CronPage 抄)

> 蓝本:`~/.hermes/hermes-agent/web/src/pages/CronPage.tsx`(1294 行)+ `web/src/lib/cron-job.ts`(198 行,前端镜像后端常量/表单模型)。事实依据:sidecar 九方法语义(entry.py `_m_cron_*` docstring 实读)、MYIA UI 惯例(HashRouter 七屏 App.tsx:30-37、侧栏分组 sidebar.tsx:37-56、基件 14 件)。

## 1. 蓝本对照表(Hermes → MYIA)

| CronPage 结构(H 行号段) | MYIA 对位 | 说明 |
|---|---|---|
| 侧栏项 `/cron` label "Cron" icon Clock(App.tsx:210) | sidebar 主群 `to:"/cron"` label「定时任务」icon Clock,排「源管理」后 | grill Q1 |
| `schedulerStaleAgeS`(lib/cron-job.ts:172 镜像 STALE_AFTER ~3×60s+slack) | 屏首活性条:`cron.status` 的 **writer_alive/heartbeat_age**;僵死判据 `!writer_alive \|\| heartbeat_age>180s` 黄条;estopped 红条+**双向**:`cron.pause all`(红钮+确认 Dialog)/`cron.resume all`(grill Q6) | 判据常量注明出处 |
| Jobs 视图 job 行:name/schedule 人话/next_run+逾期红标(`cronNextRunOverdueMs` 镜像 _OVERDUE_GRACE_SECONDS)/state 色/last_run/repeat/mode/model/profile | table 行:name/schedule_display(直读)/next_run_at+逾期红标(**grace=15min 照抄 H cron.py:630**)/last_status 四态 badge/deliver/repeat | 四态=ok|failed|delivery_failed/skipped_busy|paused;blueprints Tabs 不抄 |
| 创建/编辑双 Modal(emptyCronJobForm/editorFormFromJob/buildPayload,143-175) | 双 Dialog 同款状态机:emptyForm/fromJob/buildPayload 三函数;字段裁成 §2 表单 | 蓝本字段族裁剪见偏离表 |
| (MYIA 增量,无蓝本对位) | **category 下拉选择器**:现成 `yaml.list` 列品类 YAML,坏文件行禁选带标;「手输路径」兜底(grill Q4) | 零协议变更 |
| (MYIA 增量,无蓝本对位) | **schedule 模板 chips**:五种常用排程点击填入仍可改(grill Q5) | 纯前端 |
| NameCheckboxPicker(82,skills 多选) | 不抄 | 无 skill 概念 |
| profile 选择(516-524) | 不抄 | 单数据根 |
| delivery-targets 选择器(GET /api/cron/delivery-targets) | 不抄;deliver 手输 spec+格式说明一行 | |
| 手动触发 trigger + triggerControllerRef spinner(534-553) | cron.run + 行键 Set 进行态;完成由 cron.completed 事件落地即清 | |
| 运行历史 GET runs + 输出预览(routers `_cron_output_run_preview` 截 180 字) | cron.runs 行内展开:status/finished_at/run_summary_json 摘要 | grill Q3 |
| i18n scheduleDescriber(554-576) | 不抄;schedule_display 直读 | 后端已生成人话 |

## 2. 文件与形状

```
desktop/ui-src/src/screens/cron/
  cron-screen.tsx        # 屏本体(活性条+列表+动作+双 Dialog+历史展开;组件 docstring 标蓝本行号段)
  api.ts                 # 本屏 invoke 封装(经 client 共享门面)
  cron-form.ts           # emptyCronJobForm/fromJob/buildPayload 三函数(蓝本 143-175 对位)+ 常量镜像
  cron-screen.test.tsx   # vitest(mock bridge)
desktop/ui-src/src/lib/api/types.ts   # 九方法签名入 SidecarProtocol mirror(纯前端,协议不动)
desktop/ui-src/src/components/layout/sidebar.tsx  # 主群加一项
desktop/ui-src/src/App.tsx            # <Route path="cron" element={<CronScreen/>}/>
```

表单字段(F4,grill Q4/Q5 落定):schedule(必填,**五种模板 chips**点击填入仍可改)+category(必填,**yaml.list 下拉选择器**,坏文件行禁选带标+「手输路径」兜底)/deliver(缺省 local,附格式说明)/failure_deliver/repeat(空=永久)/timezone/run_timeout/dry_run(Switch)。create→cron.create(早失败错误原样回显:parse 文案/category 校验);edit→cron.edit 部分更新(schedule 变更后端自重算 next_run_at)。

刷新(F7,grill Q2 修正案):进屏 Promise.all(list+status)→ SidecarEvent 流订阅 cron.completed/cron.skipped→toast(直读事件载荷 name/status)+立即重拉→手动刷新按钮;**不做 interval 轮询**(全仓 UI 零先例);逾期红标走时=本地 1min 时钟重渲染(纯前端 tick,不重取)。

## 2.5 Grill 决议(2026-10-04 六问全按推荐)

Q1 主群源管理后 / Q2 事件驱动+手动刷新+本地时钟 / Q3 历史行内展开 / Q4 category=yaml.list 选择器+手输兜底 / Q5 schedule 模板 chips / Q6 急停双向(红钮+确认 Dialog/红条恢复全部)。事实裁决五条见 prd「Grill 决议」节(协议形状五件/**grace=15min 照抄 H cron.py:630**/僵死判据 `!writer_alive||heartbeat_age>180s`/toast·confirm 先例在/screens 零 setInterval)。

## 3. 偏离表(蓝本 → MYIA,逐条理由)

| # | 偏离 | 理由 |
|---|------|------|
| B1 | 不抄 Blueprints 视图/Tabs | MYIA 无任务模板概念 |
| B2 | 不抄 profile 选择/多路 jobKey | 单数据根(jobKey=job id) |
| B3 | 不抄 skills/model/provider/toolsets/prompt/monitor 表单族 | job 载荷=品类 YAML(hermes-cron D2 对位) |
| B4 | 排程人话直读 schedule_display,不做前端翻译器/i18n | 后端 parse_schedule 已生成 display;UI 全中文 |
| B5 | deliver 手输 spec,不做 delivery-targets API | 协议零变更红线;格式说明一行足够 |
| B6 | REST fetch → sidecar invoke(client 门面) | 桌面架构差,蓝本数据流形态保留(加载/错误/空态三态) |
| B7 | 输出预览不进屏 | cron.runs 已带 run_summary_json 摘要;原文留 CLI/文件 |

## 4. 风险

- 并行线 ui-reskin-r2 在途:动工前 git status 核 sidebar.tsx/App.tsx 占用,被占走等待环(4min×20 轮,先例 hermes-cron B3);
- toast/confirm 先例已核(messaging/feed 的 toast、yaml-editor 的 window.confirm spy)——复用既有模式,不自绘、不引新依赖;
- 逾期/僵死判定与后端常量漂移:注释双向标出处(前端常量 ↔ H cron.py:630(_OVERDUE_GRACE_SECONDS=15min)/ 我们的 status 字段 writer_alive)。
