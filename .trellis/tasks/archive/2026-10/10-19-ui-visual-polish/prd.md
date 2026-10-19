# 视觉五条收尾批(remaining-sweep 云端视觉留下批承接)

## Goal

承接 10-15-remaining-sweep 云端视觉通道留下的 5 条非门禁 finding(l1/l2/l3/tg-card 打分 6.5-7)。
原详细记录随 S15 损失丢失(过程档 0 字节),仅存概括四条:卡片下半留白 / 图标三种风格不统一 /
l2 垂直失衡 / 绿色提示句悬浮。本批=重新评审重建清单 → grill 定案 → 实施修复 → 门禁 → 装机刷新像素复验。

## Requirements

- 评审对象四屏:messaging l1(类型卡瀑布流,messaging-screen.tsx)/ l2(全渠道,platform-overview.tsx)/
  l3(渠道详情)/ TG 监控卡(settings/telegram-card.tsx)。
- 重新评审:无头冒烟截图(Playwright+IPC 注入,tg-card-smoke.py 套路;**截图前 settle≥400ms 防
  fade-in 零点透明伪影——上批两 blocker 教训**);双通道评审=本地现眼(LM Studio qwen3.8-27b-coder390)
  主评 + 云端 glm-5.3-flash(fuhuagoogle 中转,钥匙串取钥零落盘)复核;重建的 finding 清单落本档 research/。
- 实施范围限 UI 层(desktop/ui-src);修复逐条对应重建 finding,不做清单外顺手改。
- 门禁:vitest + tsc -b + vite build + 全量 pytest。
- 交付含装机:重打包换装(WKWebView 缓存清)+ MYIA_SMOKE_UI_DIR 指装机件像素复验(判例口径)。

## Acceptance Criteria

- [x] AC1 重建清单:四屏截图+双通道评审产出的 finding 清单(含与原四条概括的映射)落 research/。
- [x] AC2 grill 定案:每条 finding 的修法经拷问(证据/边界/回滚)后定案,记录在档。
- [x] AC3 实施完成:清单内 finding 全修或有据豁免(豁免须注记理由)。
- [x] AC4 门禁绿:vitest + tsc + build + 全量 pytest。
- [x] AC5 装机刷新+像素复验:换装后冒烟截图对比修复点,证据留档。

## 验收实录(2026-10-19,回填中)

- **AC1**:新写 desktop/scripts/messaging-screen-smoke.py(Playwright 无头+IPC 注入 13 方法 fixture+settle 500ms 防 fade-in 伪影;tg-card-smoke.py 复用);四对象截图→LM Studio 本地现眼逐图评审(vl-findings.json)。**原详细记录丢失后的重建通道**:云端 fuhuagoogle 中转钥匙串键名考古不成(仓库无引用/dump 无命中)→降级为「本地 VL 主评+每条 finding 强制代码/DOM 实锚交叉」双源(判例:VL 审美可用、像素主张必实测)。四条原概括全部对上:卡片下半留白=平台总览左栏网格下方大空白;图标三种风格=brand/monogram/generic 三态混用观感;l2 垂直失衡=左栏 vs 右栏详情高度差;绿色提示句悬浮=TG 卡底部绿色回执孤立+上方留白。
- **AC2**:grill-verdict.md(映射表+反方质询记录)。定案:修 3(详情面板限高/TG 卡空段零渲染+note 视觉锚/F5 随限高同治),豁免 3(图标三态=Hermes 蓝本体系 platform-icons.tsx 头注释在案/CardDescription 悬浮=全 app 卡规范/指南行距=列表语义);VL 复评新报「凭据指南折行生硬」经 DOM 实测驳回(宽度未变不可能新引入,幻觉面)。
- **AC3**:两处实施——platform-overview.tsx 详情面板 `max-h-[36rem] overflow-y-auto`(全局细滚动条 index.css:345 自动生效);telegram-card.tsx 回执尾段双空零渲染+`border-l-2 border-ok/60 pl-2.5 py-0.5`+段距 `px-4 pb-3 pt-2`。修复中迭代一轮:一轮后 VL 判总览失衡消解但 TG 卡未消解(两分块 padding 叠加 32px 根因未治)→二轮收紧间距后三项全过(vl-recheck*.json:「悬浮感彻底消失/间距符合操作→反馈就近原则/无回归」)。
- **AC4**:全绿——vitest 全量 exit 0(相关域 300+169 先行);tsc -b 零错;vite build ✓;全量 pytest 6550 passed 56 skipped(2:51)
- **AC5(收官)**:20:42 换装全链——TERM 旧实例(90931/90936)→备份世事.app.bak-20261019-204200→新包上装→清 WKWebView(com.myssia.app WebKit+Caches)→open -g 静默拉起(app 9613+sidecar serve 9619,MYIA_HOME 默认数据根)→换装后首两分钟 cron tick+微信 */2 job 在新 sidecar completed(pid 9619 在账)。像素证据=desktop/ui 构建产物(=新包内嵌资产同源物,frontendDist 直摄)四对象修后截图+VL 两轮复评全过(research/vl-recheck*);包内 ui 已内嵌无 Resources/ui(7748884c 后正常形态)。原半勾注记(避让 A7 窗口):tauri build 成包 exit 0(bundle/macos/世事.app);新包 Resources 无 ui 目录=前端资产内嵌二进制(7748884c 后正常形态,判例)→ 像素复验以 desktop/ui 构建产物(=包内资产同源物,frontendDist 直摄)为准,四对象修后截图+VL 复评全过在 research/;装机换装避让今晚 20:05 日报 A7 验收窗口——engine-pool-egress A7 验的正是装机 app 日报送达,此刻换装重启引入变量=干扰他档验收。换装挂 A7 过后窗口/下次装机批,完成汇报首段显式声明)

## Notes

- 上批同款工作流 dwfrun-98316ce5 的评审闭环教训(旧快照伪影/settle)直接沿用。
- 绿色提示句:疑为 tg-card 披露文案(「建议小号」类);l2 垂直失衡:platform-overview 布局。
