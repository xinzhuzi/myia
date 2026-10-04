# 发布与收尾待办清单(主人门禁+装机验收+待确认处置)

## Goal

2026-10-04 按 trellis 做完全部任务工作流(12/12 闭环)后的剩余问题清单落档:主人门禁/装机验收/在途知悉/待确认处置,待办不悬对话。

本档为收尾清单档:口径如实记录,不新增判断;各项处置动作按节内标注的责任方(主人/AI/并行会话)走,不在本档内展开实现。

## Requirements

### 一、主人门禁(只有主人能做)

1. PyPI 双包 pending publisher:pypi.org 注册时包名以**定名终局为准 = `myssia`/`myssia-classifier`**(2026-10-04 定名,dc064d3/1be66b0 已入库;本条原写 myia/myia-classifier 系改名前口径,如 pypi.org 侧此前已按旧名建过 pending publisher 需删旧建新)、Repository 填 `myia`(GitHub 仓 = xinzhuzi/myia);完成后回话,由 AI 代跑 Re-run + 发布线终勾。
2. GHCR 包页清理。

### 二、装机/真机验收(代码已就绪,留装机)

1. 桌面端重装 /Applications 目视冒烟(12 任务闭环后的新构建,工作流止于 `tauri build`)。
2. 消息平台 W2 换装冒烟。
3. keychain `-25244` 修复的跨进程验收(修复已入库 `9652cf3`)。

### 三、长期挂账

- 真机飞书/TG 收卡。
- 活 GLM key 的 enrich 真跑。

### 四、待主人确认的处置

1. ~~疑死工作流处置(确认后停,防双跑):`dwfrun-202c9176` / `dwfrun-f1a9a0b9` / `dwfrun-c72abec5` / `dwfrun-2f494cf4` / `dwfrun-39d071be` / `dwfrun-2dc0d9a3`~~。

   **✅ 已销项(2026-10-04 实核,收官流)**:`39d071be` completed / `2dc0d9a3`
   superseded 链终态;`202c9176` / `f1a9a0b9` / `c72aebec5` / `2f494cf4` 已随
   10-03 午后 Amend 置终态;全项目唯一活跃 run=收官双流(fe-gap-census +
   wrapup-checklist),无需停任何东西。
2. ~~归档会话收走 10 个 review 态任务档(grill 决议:独立会话)~~。**✅ 已完成(2026-10-04,主人令「归档」当场收走)**:messaging-w3-longtail / shishi-everywhere / alert-rules / crawl4ai-l3 / desktop-b234 / feishu-thread-send / hermes-cron / proxy-pool / wecom-group-webhook / windows-build 十档入 archive/2026-10/,每档独立 pathspec 提交,review 态清零,活目录余 5(v12-backlog 池 2/2 / fe-gap-census / wrapup-checklist 两 planning + interaction-batch / read-state-server 两 in_progress 在途)。

### 五、在途知悉(并行会话自收,勿重复立项)

- ~~`messaging-w3-longtail`(残余红测 `test_join_403` 归它)——已归档,红测若仍在树=移交 read-state-server 收口批或独立小修~~。**✅ 处置完结(2026-10-04 收口核)**:实跑 `.venv/bin/python -m pytest tests/test_messaging_irc.py` = 29 passed 0.13s(含 `test_join_403_is_not_found_dead`,tests/test_messaging_irc.py:252)——`test_join_403` 已不在当前红测清单,系被在途线修掉;零代码修复故零 fix(test) 提交,亦无需移交 read-state-server。
- ~~`shishi-everywhere`~~(已归档;PyPI 注册动作仍在第一节挂账,注意发行名已漂移 myssia)。
- ~~`10-04-alert-rules`~~(已归档)。
- `v12-backlog` 池。

## 六、路由执行记录(fe-gap-census 处置路由 10 条终态,2026-10-04)

> 主人令「全部做完」后收官流逐条处置完毕。出处=`.trellis/tasks/10-04-fe-gap-census/
> research/matrix.md` §处置路由汇总(R1-R9)+§3.2 真机手验一行;执行细目见该档文首
> 「路由执行记录」节。10 条全部终态,无一悬置。另:10-04 收官归档波再归
> 档三线(590c4ea interaction-batch / e0ece43 read-state-server / 108b46b
> fe-gap-census),活目录余 v12-backlog 池与本档。

- **直接小修 4 条(R1-R4)→ 3 落地 + 1 核毕销项**:R1 feed Mod+F 聚焦内联搜索框
  +Esc 即时清空(落地:`feed-screen.tsx`,+2 用例)/ R2 AlertsFiredEvent 入
  SidecarEvent 联合+logs 穷尽守卫适配+消息屏去 cast 直窄化(落地:`types.ts`+
  `logs/api.ts`+`messaging-screen.tsx`,+3 用例)/ R4 v12-backlog 池 prd 回标
  (落地:G5 主体/G7/G8/G12 消号+R6/R7 增补入池第 8 项);**R3 版本号=已对齐
  (核毕销项,零改动)**——10-03-tag-release 决议 9 已把版本纪元归零 0.0.1
  (commit 9810139:tauri.conf.json/Cargo.toml/classifier 双处同落,根 pyproject
  随后同落),现树 `tauri.conf.json:5`=0.0.1 与发布线本已一致;matrix R3 原判据
  「对齐 package.json 0.1.0」系普查未计归零决议的误读——desktop/ui-src 两
  package.json 的 0.1.0 为 v1.0 期 npm 脚手架占位,从来不在版本对齐面(v1.1.1
  期对齐叙事即仅四处:pyproject/classifier/Cargo.toml/tauri.conf.json,workspace
  journal 在案),维持不动。
- **G9 立档(R5)→ 立档后同日撤并(终审收口 commit 2237bf9)**:全库批量已读
  store/协议本体由 `10-04-read-state-server` 交付(已归档;afa7339
  `store.state.mark_all` 全库语义三端+能力门+按钮真话),快捷键/右键批量件随
  `10-04-interaction-batch`(已归档);余量曾立档 `.trellis/tasks/10-04-g9-read-all/`
  (按品类批量入口+全库确认交互,grill 未批不开工),终审裁定**撤并不另立项**——
  档自工作树移除(未跟踪件,零 git 痕迹),G9 终态=`10-03-v12-backlog/prd.md`
  第 5 项已消号标注(在库)。
- **入池 2 条(R6/R7)→ 已入池**:G10 代理池连通性测试按钮(后端依赖解锁)
  +七件小件(侧栏分组折叠/源管理多选点簇/设置 tooltip/snooze 到期重现/设置搜索/
  suppressed 词表 v2/P3 标题跳级),增补回执 `10-03-v12-backlog/prd.md` 第 5 项
  G10 行+第 8 项新增块——其中**设置搜索(#7)后由终审收口先行落地**
  (settings-screen.tsx+settings.test.tsx,commit 2237bf9),余六件仍留池。
- **关闭 3 条(R8/R9/§3.2)→ 维持关闭,不再立项**:R8 语义不匹配/过度 4 项、
  R9 在途归 interaction-batch+已实装 24 项(#7 设置搜索 census 定稿时悬置
  留池、matrix 定稿注记在案,后由终审收口落地见 R7 行注)、§3.2 真机手验归
  本档第二节。

## Acceptance Criteria

- [ ] 档已建:prd 四+一节齐全(一~五节按上口径落档)。
- [ ] `implement.jsonl` / `check.jsonl` 各一条指向本 prd。
- [ ] `task.py validate` 通过。
