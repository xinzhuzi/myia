# 渠道卡缺凭据角标——看似正常但永远 0 条一眼可见

## Goal

TG 渠道 2 级卡片对凭据缺失的源(如 mihomo_party_group 指向 bot-token-disabled 占位)显示缺凭据角标,监控每 30 分钟空转但用户看到今日 0 条无从得知原因。

## Requirements

- 数据面不新增 RPC:健康度快照(sourceHealthBySource,与 engineBySource 同一次 health() 装配)已携带 `latest.skip_reason`;credential_missing = 引擎显式空态(健康度判 ok 但永远 0 新),把它抬到卡视图模型(`FeedChannelCardData.credentialMissing`)。
- UI:2 级渠道行行 1 渠道名右侧亮「未配凭据」角标(warning 色档,借 wx 群状态点范式),title 人话给因与去向,行话不上屏;健康渠道零角标。
- 纯函数 `feedChannelCards` 加可选 healthBySource 参数,缺席 = 行为不变(向后兼容)。

## Acceptance Criteria

- [x] credential_missing 显式空态源的 2 级渠道行亮「未配凭据」角标,title 人话;健康/指纹跳过源零角标(渲染级+纯函数双测)
- [x] 角标旗走既有 health() 快照,零新 RPC、零协议变更
- [x] 门禁全绿(scoped feed-screen 223 + 全量 vitest 961 + tsc/vite build + 全量 pytest 6493)

## 执行记录

- 触发:10-20 主人真机目验后问「这个 UI 一直是 0 条吗」——诊断为非缺陷
  (mihomo bot 凭据未配,引擎显式空态),但「看似正常却永远 0 条」的可见性
  缺口成立,主人批「立,然后做」。
- 实现:api.ts `FeedChannelCardData.credentialMissing?` + `feedChannelCards`
  第 6 可选参 healthBySource;feed-screen.tsx channelCards useMemo 传入
  sourceHealthBySource,ChannelRow 行 1 挂角标(border-warning/50 text-warning,
  testid `feed-channel-cred-<key>`)。foldSnsMomentCards 展开继承天然保旗。
- 工程课(实测在案):测试文件里 `fixtureItem()` 只许在 `it` 体内调 ——
  模块级 `nextItemId` 自增,describe 收集期调用会把前序用例的条目 id 顶掉
  (`feed-item-1` 假失踪 5s 超时),二分定位到测试文件后修法=夹具调用下移。
- 门禁实绩:vitest 全量 961/961(此前偶发单红 updater-card 复跑两遍未再现,
  判抖动);pytest 6493 过 56 跳。
