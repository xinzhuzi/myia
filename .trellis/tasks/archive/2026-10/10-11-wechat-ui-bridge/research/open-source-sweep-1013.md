# 微信读数开源件补遗(2026-10-13,主人点名五仓库+Xposed 质询轮)

> 背景:主人质询「GitHub 开源的不能用吗?Xposed 你不看的吗?」,点名五仓库。逐个实测级核查(zread/GitHub 页面取证),补录本档。**本轮最大发现 = jackwener/wx-cli(调研档此前漏收)。**

## 逐个结论

| 仓库 | 平台/机制 | 裁定 |
|---|---|---|
| **jackwener/wx-cli**(Apache-2.0,Rust 单二进制,npm 装) | **macOS/Linux/Windows;微信 4.x SQLCipher 本地库解密**(mach_vm 扫 `x'<64hex><32salt>'` raw key) | **⭐ 重大候选件**:与 MYIA keyscan 同机理但已成成品——daemon 解密缓存、`new-messages` 增量、`history/search/contacts/members/stats/export`、公众号 biz_articles、朋友圈、附件解码、agent 友好 JSON wrapper。macOS 前提 = **微信 ad-hoc 重签名**(codesign --force --deep --sign - + tccutil reset + 重启;副作用 = 微信频繁弹「访问其他 App 数据」;文档称 SSH+Apple 签名组合或可免重签但 macOS 14+ 未实测)。链接者架构下 = 受管组件完美形状 |
| zjp1997720/wechat-radar(MIT) | macOS Next.js 看板,**读数全靠 wx-cli** | 壳件;价值在其上游 wx-cli(已单列)。看板形态与 MYIA 情报流重叠,无增量价值 |
| B022MC/wechat-observatory(33★,MIT) | **Android LSPosed Xposed 模块**hook 微信进程 + Go 服务端 | 安卓 Root+LSPosed 路线;hook 路径仅适配 Android 微信 8.0.75(版本死绑);风控/封号风险 README 自认。不适用:数据源=安卓微信,非 mac 本机库 |
| youkuzazazazaza/wechat-cli(15★,MIT) | Windows(WeFlow HTTP + UI 自动化发送) | Windows 专用;读靠第三方 WeFlow 服务。不适用 |
| jiangliushi666/WeKit(0★) | Android Xposed/Zygisk 微信**功能增强**模块 | 是「微信增强插件」不是数据采集管线;Root+LSPosed;不适用 |
| qinge5202024/wechat-mp-harvest(0★,109 forks,**Private 许可禁再分发**) | Windows DLL 注入(CreateRemoteThread+MinHook)采公众号文章 | 私有许可法律上不可集成;版本死绑 4.1.8.107;侵入式 watchdog。不适用 |
| **Xposed 路线总评** | Android Root+LSPosed,进程内 hook | 能力最强但:①需 Root 安卓机常驻挂微信;②hook 对微信版本死绑,升级即断;③腾讯对 Xposed 检测激进(封号风险,删库潮近因);④与「不改上游」有张力(运行时注入);⑤读的是安卓微信的数据,对 mac 本机库零帮助。**维持排除**,除非主人未来要安卓线 |

## 对 MYIA 的决策影响(待主人裁决)

- **方案甲(现状)**:自研 keyscan(已到只差 sudo 一步)——wx-cli 的存在证明机理正确(同款 mach_vm 扫描+同款 raw key 格式),但不解决「硬化运行时是否需要重签」的不确定性;d4-memscan-e2e.md 的实测结论是本方案的事实依据。
- **方案乙(新增候选)**:wx-cli 收编为受管组件——wechat_local 引擎 localdb 通道改挂 `wx new-messages --json`(按会话过滤喂既有锚/水位/白名单契约),自研 keyscan 降 fallback 或退役。代价 = **微信 ad-hoc 重签名**(改腾讯官方 app 的签名,主人级裁决;副作用=跨 App 访问弹窗频繁+TCC 重置)或赌「SSH+Apple 签名免重签」路径(macOS 14+ 未实测)。
- 两案不互斥:先跑甲(sudo 一步);甲若在硬化运行时上失败,乙是社区验证过的备胎,届时立项评估重签裁决。
