/**
 * 「微信」独立屏(10-11-platform-account-config;2026-10-11 主人令渠道本名制:
 * 自「平台账号」总屏拆解,路由 /weixin)。
 *
 * 内容 = WeixinAccountCard 整卡(受限形态:桥接状态灯 + 登录指引,
 * 登录态在 Hermes 侧,MYIA 红线不读不写其私有目录)。组件与 IPC 契约在
 * settings/weixin-account-card.tsx。
 *
 * PageHeader 沿无头令渲染 null,title 保留「微信账号」作语义锚。
 */
import { PageHeader } from "@/components/layout/page-header";
import { WeixinAccountCard } from "@/screens/settings/weixin-account-card";

export function WeixinAccountScreen() {
  return (
    <div className="flex flex-col gap-block pb-block">
      <PageHeader
        title="微信账号"
        description="微信个人账号(经 Hermes 桥)状态与登录指引:扫码登录在 Hermes 终端向导内完成(机器人凭据归 配置 → 机器人凭据)"
      />
      <div className="px-6">
        <WeixinAccountCard />
      </div>
    </div>
  );
}
