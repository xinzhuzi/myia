/**
 * 「飞书」独立屏(10-11-platform-account-config;2026-10-11 主人令渠道本名制:
 * 原「平台账号」总屏拆解——飞书就是飞书,渠道入口以本名呈现,侧栏「配置」组
 * 与 Telegram 平级,路由 /feishu)。
 *
 * 内容 = FeishuAccountCard 整卡(user_access_token 账号线:添加授权/状态
 * 检查/删除)。组件与 IPC 契约在 settings/feishu-account-card.tsx(跨屏
 * import 有 /tg-account 先例)。
 *
 * PageHeader 沿无头令渲染 null,title 保留「飞书账号」作语义锚。
 */
import { PageHeader } from "@/components/layout/page-header";
import { FeishuAccountCard } from "@/screens/settings/feishu-account-card";

export function FeishuAccountScreen() {
  return (
    <div className="flex flex-col gap-block pb-block">
      <PageHeader
        title="飞书账号"
        description="飞书本身账号(user_access_token 授权态)管理:添加授权 / 状态检查 / 删除(机器人凭据归 设置→推送)"
      />
      <div className="px-6">
        <FeishuAccountCard />
      </div>
    </div>
  );
}
