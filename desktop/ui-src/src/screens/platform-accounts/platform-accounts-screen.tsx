/**
 * 「平台账号」独立屏(10-11-platform-account-config:侧栏「配置」组新增,
 * 路由 /platform-accounts)。
 *
 * 内容 = PlatformAccountsCard 整卡(飞书 user_access_token 账号线 +
 * 微信桥受限状态段)。裁定语义:本身账号(个人授权态)≠ 推送机器人
 * (App 凭据/bot token)——机器人配置归 设置→推送,本屏只做账号。
 * 组件与 IPC 契约在 settings/platform-accounts-card.tsx(跨屏 import
 * 有 /tg-account 先例,依赖簇不迁)。
 *
 * PageHeader 沿无头令渲染 null(与消息/定时任务屏同口径),title 保留
 * 「平台账号」作语义锚。
 */
import { PageHeader } from "@/components/layout/page-header";
import { PlatformAccountsCard } from "@/screens/settings/platform-accounts-card";

export function PlatformAccountsScreen() {
  return (
    <div className="flex flex-col gap-block pb-block">
      <PageHeader
        title="平台账号"
        description="微信 / 飞书等平台的本身账号(个人授权态)管理:添加授权 / 状态检查 / 删除(机器人凭据归 设置→推送)"
      />
      <div className="px-6">
        <PlatformAccountsCard />
      </div>
    </div>
  );
}
