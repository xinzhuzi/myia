# W2 换装冒烟(2026-10-05 00:45 尝试,受阻断档)

- 桥状态全绿:probe_bridge available=True(bin/微信已配置/gateway 活着);主人 peer 已定位(网关日志 46 次收发者)。
- 发送(smoke-20261005-weixin-001,经 WeixinChannel→hermes send)被上游拒:**「微信会话未就绪:对端尚未给 bot 发过消息(或登录态已过期),iLink 要求先有入站才持有出站 context_token」**——与 W1 决议记录的机制一致(整体桥接否决的根因;单平台桥的已知约束)。
- **修复=主人动作**:给 bot 发一条微信消息(刷新 context_token)后回话,我即重发冒烟;若 token 过期则需 Hermes 侧重新扫码配对(档内 UPDATER/桥接 runbook)。
