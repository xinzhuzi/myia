/**
 * 「TG 账号」独立屏(10-11-tg-multi-account-groups v10:侧栏新增「配置」组,
 * Telegram 监控分区自设置屏抽为独立屏,路由 /tg-account;feed 3 级监控台
 * 「管理」钮同批改指本屏)。
 *
 * 内容 = TelegramCard 整卡(10-08-tg-web-line W4:bot/session/web 三线状态头
 * + 网页线账号列表「添加 / 重登 / 删除」,登录动作经浏览器模块统一入口)。
 * 组件与 IPC 契约仍在 settings/telegram-card.tsx(跨屏 import 有先例:
 * feed-screen 本就消费同目录 telegram-api;搬家会牵连 error-box/field-input/
 * browser-api 依赖簇,渐进改造原则下不迁)。
 *
 * PageHeader 沿无头令渲染 null(与消息/定时任务屏同口径),title 保留
 * 「TG 账号」作语义锚,后续流整删时防编译红。
 */
import { PageHeader } from "@/components/layout/page-header";
import { TelegramCard } from "@/screens/settings/telegram-card";

export function TgAccountScreen() {
  return (
    <div className="flex flex-col gap-block pb-block">
      <PageHeader
        title="TG 账号"
        description="Telegram 三线状态(bot / session / 网页线)与账号生命周期:添加 / 重登 / 删除(登录经浏览器模块统一入口)"
      />
      <div className="px-6">
        <TelegramCard />
      </div>
    </div>
  );
}
