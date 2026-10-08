# Implement:TG 渠道卡

## 顺序清单

1. [ ] `gitnexus impact -r shishi FeedScreen`(留档爆炸半径;LOW-MEDIUM 预期)
2. [ ] api.ts:`telegramChannelCards(items, states)` 纯函数 + `TelegramChannelCard` 类型(聚合/排序/未读口径,见 design §1)
3. [ ] feed-screen.tsx:
   - [ ] tgCards / streamItems / kindByItem 派生(仅 source===null 的 L3)
   - [ ] TelegramChannelCard 组件 + 「TG 频道」区(顶部,testid 齐)
   - [ ] 时间分组/空态门/j-k 巡游/U 键切 streamItems
   - [ ] 面包屑:category===null 的 source 作用域加「全部条目」中间层
4. [ ] 测试(feed-screen.test.tsx):
   - [ ] 新增:渠道卡区呈现(名称/预览/计数/未读竖条/时间)+ 点击进渠道详情 + 回流面包屑
   - [ ] 新增:全 TG 流不误现空态;TG 卡从消息列表消失、其他类型不受影响
   - [ ] 迁移:原 L3 流内 TG 气泡断言 → 渠道详情作用域下成立
   - [ ] telegramChannelCards 纯函数直测(排序/未读/边界)
5. [ ] 门禁:`npx vitest run src/screens/feed` + `npx tsc --noEmit`(ui-src 形态按仓内惯例)+ `npm run build`
6. [ ] 复查(gitnexus detect-changes staged)+ 提交
7. [ ] 装机:重打包 + 静默换装 + WKWebView 缓存清理 + 装机件像素级验证(截图/OCR 证据;[[delivery-includes-installed-artifact]] 判例)
8. [ ] 档回填(AC 勾选)+ 汇报

## 验证命令(按仓内实际形态微调)

```bash
cd desktop/ui-src && npx vitest run src/screens/feed
cd desktop/ui-src && npx tsc --noEmit && npm run build
```

## 回滚点

- 步骤 2-4 全部在单 working tree,任一步失败 `git checkout -- desktop/ui-src` 回滚。
- 提交后回滚 = revert 单 commit(无迁移/无协议变化)。
