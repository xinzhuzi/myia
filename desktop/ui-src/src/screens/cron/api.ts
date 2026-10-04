/**
 * 定时任务数据装配(本屏私有 api 模块;cron.* 九方法走共享门面
 * `@/lib/api`——10-04-cron-ui 封装政策,屏私名单不扩)。
 *
 * 数据面 = sidecar 协议(契约权威 desktop/entry.py `_m_cron_*`,协议 v9
 * hermes-cron 批):
 *   cron.list   → job 清单(缺省仅活跃;all:true 含暂停/终态);
 *   cron.status → ticker 活性快照(活性条三态数据源,Stage 2 消费);
 *   cron.runs   → 执行账本(行内展开,Stage 4 消费);
 *   sidecar://event → cron.completed / cron.skipped(事件驱动重拉,Stage 4)。
 * Stage 1 骨架:屏首挂载即 list+status 双拉(空/载/错三态打底)。
 */
import { api } from "@/lib/api";
import type { CronListResult, CronStatusResult } from "@/lib/api";

/** 屏首快照:job 清单 + ticker 活性(单屏一次拉齐;错误整体走 ErrorBox) */
export interface CronOverview {
  list: CronListResult;
  status: CronStatusResult;
}

/** 拉取屏首数据(list+status 并行);all 透传 cron.list(「显示暂停/终态」开关) */
export async function loadCronOverview(all = false): Promise<CronOverview> {
  const [list, status] = await Promise.all([api.cronList({ all }), api.cronStatus()]);
  return { list, status };
}
