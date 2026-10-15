# 剩余清单扫尾(解密件/视觉引导/nit/备份清理)

## 背景

主人令(10-15 /workflow):做完剩余清单四件,流程=探索→计划→grill→执行→技能深化→**云端大模型深度 review(代码 diff+云端视觉双通道)**→打包覆盖安装。

## 流程(dwfrun-98316ce5,含一次限额熔断前科另批)

探索员→(规划师⇄挑问员)+独立复审→实施员(唯一写手)→门禁(world.run:vitest 全量/tsc/桥+推送域 pytest 全绿)→快筛→云端双通道评审(两轮回炉:首评两 blocker 经重验证识破=旧快照伪影+冒烟补 settle 400ms 根治)→打包→安装员→提交 bb9d858c,装机 088a0f0d167a。

## 四件落点

1. **解密件**:`scripts/wechat-bridge-mediadecrypt.py` 骨架(协议壳完整自测 T1-T7 过;两算法位显式留空,命中回法定指路文案;B1 永不入桥目录/B2 env 钥匙边界,头注+文档双载)+ docs §9 指路 + 沙箱接线闭环(exit 22/23 逐字命中)。**算法面生态结论:mac 4.x .dat 无任何 MIT/Apache 可借实现**(chatlog 空仓/WeFlow CC BY-NC-SA 禁/wechat-dump-rs DMCA/余无 LICENSE)——主人三选项入档:自写/指路 WeFlow 外置件自担/imldy fork 取钥件自组。
2. **feed-site**:列宽 820→900 + 侧栏分界 /60→全强度(与铬层分界惯例对齐)。
3. **详情弹窗**:动作簇 border-t 全强度;tg-account 复查零改动。
4. **备份清理**:删 .old-1014-l3,恰留 .old-sweep 一个回退位。〔10-15 晚勘定:两标的已被装机备份清理波带走(/Applications 已无 .old-1014-*/.old-sweep);现存回滚包两枚——`.old-1015-ui`(ui 线已全推+图标亲验过,理论可清)与 `.old-cloud5`(等 ui-cloud5 目验,须留)。通知图标终验同日主人再认「图标是对的」,归档档 10-14-notify-app-icon AC1 已记;删留待主人一并裁〕

## 云端评审通道(主人点名的升级,全程实录入档)

云端 glm-5.3-flash 实弹(fuhuagoogle.top 中转 /v1/chat/completions,relay 名 z-ai/glm-5.3-flash;钥匙串取钥内存管道零落盘;官方端点无钥→中转裸名 503→PAAS 429 余额→中转查 62 型接通)。5 屏 8 调用;**代码通道两轮 findings 空**;视觉通道留 5 条非门禁 finding(l1/l2/l3/tg-card 6.5-7 分:卡片下半留白/图标三种风格/l2 垂直失衡/绿色提示句悬浮)= 下批 UI 现成清单。

## 验收

- [x] 四件全落地(解密件=骨架+三选项,算法面如实不伪造)。
- [x] 门禁全绿+云端双通道(代码净)。
- [x] 覆盖安装 088a0f0d167a(哈希复验+setup done+冒烟过;构建模式=前端内嵌二进制,Resources/ui 不再拷贝属正常)。
- [x] 真机微信真图终验(2026-10-15 实施员批:算法位已按实测填入——V2/V1 三段容器+legacy XOR+Isaac64 参考C KAT 对齐,26 单测+196 相关子集全绿;**整图解密未达成,如实记**:V2 每用户 AES 钥在本机 4.1.15 静态内存不可得——主进程/聊天渲染器/AppEx 主进程共 ~22GB dump(含执行区/页完美补灌)×AES-128/192/256/SM4×魔数/成对差分(IV 无关)/轮钥 schedule 七族 oracle 全零,钥形态为运行期驻留/受保护(Windows ZedeX 静态扫法不迁移);尾部单字节 XOR(0xE9)已解并验证,全图需主人自供钥走件内自理通道)。

## 遗留

- 云端视觉 5 条 finding 留主人另立批;git push 待令。
