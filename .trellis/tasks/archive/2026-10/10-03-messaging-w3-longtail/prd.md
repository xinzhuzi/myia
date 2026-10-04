# 消息平台 W3 伞:长尾平台登记与开工门(待续标记)

**血缘归属**:消息平台树(父档 `archive/2026-10/10-03-hermes-messaging` 波次表;因父档已归档,本任务独立成档)。主人 2026-10-03 指示:「还没有做的、需要做的要有区分,因为等别的会话做完,要继续再做」——本档就是那条「继续」的显性标记。

## 待办登记(本伞持有,不做实装)

| 待办 | 性质 | 开工门 |
|---|---|---|
| 22 家长尾平台实装(slack/discord/whatsapp_cloud/signal/line/matrix/mattermost/google_chat/teams/email/sms/irc/simplex/bluebubbles/msgraph_webhook/qqbot/yuanbao/a2a/buzz/photon/raft/homeassistant) | 分批开发 | 主人排期指令 + 并行战场安静;蓝本范式已定(有官方 HTTP 出站→照 feishu/telegram 范式;无→extras 结构化报错;仅 simplex 有 list_channels,其余全别名+直达) |
| 企微群机器人 webhook 增量候选 | 增量开发(默认不做) | 主人点头即做(W2 档 R3 登记) |
| 飞书话题(thread)定向发送 | 增量开发(目录已记 thread_id) | 真实需求出现 |
| 黄金回归治本(冻结快照) | 独立任务 `10-03-golden-frozen-snapshots`(planning,活动区) | 建议随 W3 首批一起跑 |
| 主人手工门禁(TG/企微/钉钉/ntfy 真机冒烟、消息屏视觉过目、拉 bot 入群) | manual | 见归档父档「遗留」节清单 |

> **2026-10-04 状态追记(收口会话;追加式,上表原文不动)**:第 1 行「22 家长尾平台实装」已由并行会话(大工作流「按 trellis 做完全部任务」)跨会话实装入库——22 家适配器文件与注册(`src/shishi/push/__init__.py:151` `_W3_LONGTAIL_CHANNELS`,收口会话 ls/grep 实测在册)、schema `PUSH_CHANNELS` 30 值、UI 卡转实装+凭据指南、22 家测试均在;**分批任务档未建**(实装未走本伞 Requirements 第 1 条「每批 3-5 家一任务」流程,由并行大工作流批量直做,commit 证据见下「W3 执行结果」节)。第 4 行「黄金回归治本」亦已被他会话完成归档(`archive/2026-10/10-03-golden-frozen-snapshots` task.json status=completed,收口会话 2026-10-04 复读属实),不抢占。第 2/3/5 行(企微群 webhook/飞书话题/手工门禁)不动,仍留主人。

## Requirements(开工时)

1. 每批 3-5 家平台一任务,照 W2 范式(事实探查先行→三件套→流水线:实现→本域双门禁→独立质检→提交)。
2. 事实探查模板同 W2:蓝本形态/纯 httpx 出站可否/目录发现有无/错误码→死信映射。
3. 需要外部守护进程的(signal 需 signal-cli、bluebubbles 需服务端)进 extras 并结构化报错,不进核心。

## Acceptance Criteria

- [ ] 每批平台:适配器+测试+UI 卡转实装+凭据指南落地,门禁双绿,真机冒烟清单留主人。
- [ ] 全量平台覆盖达 28/28 或明确豁免理由(决议外/需 extras)。

## W3 执行结果(2026-10-04 收口记账)

**归属(跨会话如实记档)**:22 家长尾平台实装由并行会话(大工作流「按 trellis 做完全部任务」)完成并入库——22 家适配器文件(收口会话 ls 实测在册)、`src/shishi/push/__init__.py:151` 起 `_W3_LONGTAIL_CHANNELS` 注册(横切面核验:与 `schema.py:168-191` 名单完全一致)、schema `PUSH_CHANNELS` 30 值、桌面 UI 卡转实装+凭据指南、22 家测试文件均在册;**分批任务档未建**(未走本伞 Requirements 第 1 条「每批 3-5 家一任务」流程,由并行大工作流批量直做)。本会话对上述成果做了交叉核验(六片+横切面)与修复,结论全部通过(原文转录见下)。

**涉及 commit**(收口会话 2026-10-04 实测 `git log --format='%h %ad %s' --date=short -- src/myia/push/ src/shishi/push/` 前 5 笔;单查新路径 `src/shishi/push/` 仅得 2 笔——58cb40b 改名截断历史,故并查改名前后两路径,如实记档):

1. `58cb40b` 2026-10-04 refactor!: module rename myia→shishi — src tree, CLI script, packaging chain
2. `3332fc2` 2026-10-04 docs: schema zh/en 补 L3 零结果首遇探测行为与手动重探出口(engine: crawl4ai)——复查 low#3 收口(10-04-crawl4ai-l3)
3. `0fc42a5` 2026-10-03 fix(push): W3 复核九项收敛——契约/凭据/死信分类/文档(10-03-messaging-w3-longtail)
4. `a809654` 2026-10-03 feat(vision): 看图 v2 收口——模型下载/server 代管/落图 purge/推送带图/桌面模型管理与 feed 图析详情(10-03-vision-v2,含复查修复批)
5. `3cd0441` 2026-10-03 feat(push): W3 长尾 22 家终局接线——CHANNELS 30/PLATFORMS 28 一处收口(10-03-messaging-w3-longtail)

读档辅助(收口会话 `git show --stat 3cd0441` 实测):W3 主体落地为 `3cd0441`——22 家适配器随其入库(`src/myia/push/` 下含 push/ 路径文件 23 个、`__init__.py` +127,并带改本任务 task.json/implement.jsonl)与 `0fc42a5`(W3 复核收敛);`58cb40b`(改名)/`3332fc2`(docs)/`a809654`(vision)按各自提交信息系混载或顺带触该树。**未提交批**:核验摘要所引修复改动的现状,截至记账仍在工作树未提交——`git status` 实测 M `src/shishi/push/` 11 文件(a2a/bluebubbles/delivery/discord/mattermost/photon/qqbot/simplex/slack/sms/teams)、`desktop/ui-src/src/screens/messaging/` 4 文件、`tests/` 12 文件(含 test_cli.py);提交与否留主人。

**核验结论摘要(六片+横切面;核验会话实测,以下为原文转录;收口会话未重跑测试,仅做文中「收口注」所列只读复核)**:

### 前置跳过项(黄金回归)

❌档在 .trellis/tasks/archive/2026-10/10-03-golden-frozen-snapshots/task.json 且状态 completed(他会话在途?)——不抢占,跳过。

> 收口注(2026-10-04):记账时复读该 task.json,status 仍为 completed,属实。

### 片1

✅W3 片1 核验通过:四项问题主体均已解决,判定 pass;附两处 low 残留(见 failures)。逐项核验(全部在本轮实测):

问题1(medium,已解决):desktop/ui-src/src/screens/messaging/platform-overview.tsx:493-618 slack/discord/line/mattermost 四平台全部转入 IMPLEMENTED_PLATFORMS,各带完整凭据指南(env key 用途+步骤+curl 冒烟)与 discovery 说明,行 490-492 注释点名伞任务验收项;UPCOMING_PLATFORMS 只剩 signal(867-869),四平台不再灰卡;右栏详情面板已连接时显示目录速览(1342-1352)。测试侧:messaging-screen.test.tsx:971-1023 新测试「W3 组一四平台指南各就位」正向断言四家指南(SLACK_BOT_TOKEN/chat:write/im:write/discord 开发者模式/LINE 好友约束/mattermost 双路),1107-1109 循环断言四家转实装——原「钉死 slack 灰卡」断言已不存在。docs/zh/schema.md:37 与 docs/en/schema.md:41 PUSH_CHANNELS 表已列 30 值,实测与 schema.PUSH_CHANNELS 逐值比对双向差集为空。命令与结果:npx vitest run messaging-screen.test.tsx → 52 passed;platform-icons.test.tsx → 13 passed;uv run python -m pytest tests/test_docs.py tests/test_skill_doc.py -q → 116 passed。

问题2(low,已解决):src/shishi/push/discord.py:26-30 docstring 与 :224-226 代码注释已改为「403 → forbidden、404 → not_found、429/5xx → 瞬态;401 是 token 级配置错,分类器不标死信、按瞬态透传(delivery.classify_dead_error 无 http 401 锚点)」。实测分类器与新文档一致:classify_dead_error(401)→ None、(403)→ forbidden、(429)→ None(delivery.py:78-93 _FORBIDDEN_MARKERS 确无 http 401 锚点)。homeassistant.py:23-24 同主题描述亦如实。

问题3(low,已解决):slack.py:81 定义 CHANNEL_ID_RE=^[CGDUW][A-Z0-9]{8,20}$,:193-200 _resolve_channel 对解析值 fullmatch 校验,畸形 → invalid_credential_ref(解析值不回显),与 discord.py:185-197 同款;docstring:172-181 注明与三家一致的理由。实测:malformed chat_id → invalid_credential_ref、合法 C id 发送成功、合法 U id 经 conversations.open 换 DM 后成功(mock client);tests/test_messaging_slack.py:213-233 有该校验的测试覆盖。

问题4(low,已解决):slack.py:20-23 docstring 注记「与蓝本的偏离:Hermes _resolve_slack_user_dm 按 (token,user) 缓存(_slack_dm_cache);MYIA 每次发送重开——多一次 API 往返与限频暴露面」,_open_dm docstring(217-222)内再注;mattermost.py:16-19 注记「Hermes _post_message 携 root_id 做话题回复、断根回退 _post_preserving_thread;MYIA 一律平铺发频道」。蓝本事实核实:~/.hermes/.../slack/adapter.py:6484 确有 _slack_dm_cache;mattermost/adapter.py:180 确有 _post_preserving_thread 及 root_id 逻辑(177/184-187/202)——注记内容与蓝本相符。

回归:cd repo 根 uv run python -m pytest tests/ -q → 3125 passed, 19 skipped。

### 片2

✅W3 片2 核验通过:复检三项问题全部已解决(逐项证据如下)。

【问题1·已解决】四平台 UI 卡已转实装且凭据指南已落地:desktop/ui-src/src/screens/messaging/platform-overview.tsx:371(whatsapp_cloud,WHATSAPP_CLOUD_TOKEN/PHONE_NUMBER_ID/TO 三 key + Meta 后台步骤 + curl 冒烟)、:405(google_chat,GOOGLE_CHAT_WEBHOOK_URL + 空间 webhook 步骤)、:431(teams,TEAMS_WEBHOOK_URL + Power Automate Workflows 步骤 + curl 冒烟)、:457(matrix,MATRIX_HOMESERVER/ACCESS_TOKEN/ROOM_ID 三 key + login curl)——四家均为 wave W3、完整 PlatformGuide;UPCOMING_PLATFORMS(:867-869)只剩 signal 一张灰卡,:858-866 注释明记组二四家已转实装。后端注册仍在位:src/shishi/push/__init__.py:154,157-160 四家在 _W3_LONGTAIL_CHANNELS。测试钉死新行为:messaging-screen.test.tsx:1117-1122 遍历四 id 断言 guide 非空/wave=W3/discovery=manual。跑原发现点名检查:cd desktop/ui-src && npx vitest run src/screens/messaging/messaging-screen.test.tsx → 52 passed(原发现时 48,新增即四卡用例);另跑 npx vitest run src/screens/messaging/platform-icons.test.tsx → 13 passed(platform-icons.tsx 同批新增四平台头像)。

【问题2·已解决】注释已改与分类表一致:src/shishi/push/teams.py:222-224 现为「403(未授权)→ forbidden、404(webhook 失效)→ not_found、402/429/5xx → 瞬态(分类表仅锚定 http 403,402 单独出现不标死信,漏标只会持续重试)」,与 src/shishi/push/delivery.py:78-93 的 _FORBIDDEN_MARKERS(含 "http 403" :80,无 "http 402")完全吻合;grep 全文件确认无残留旧「402/403→forbidden」表述。行为无回归:uv run pytest tests/test_messaging_teams.py -q 随下条一起 50 passed。

【问题3·已解决】404 专测已补:tests/test_messaging_whatsapp_cloud.py:289-302 test_404_classifies_not_found——模拟 graph 404 应答,断言 "HTTP 404" 进文案且 classify_dead_error(excinfo.value)=="not_found",与 whatsapp_cloud.py:248 docstring「死信分类按 403/404/429/5xx 命中」对齐,补齐了对照 matrix/google_chat/teams 的覆盖缺口。实跑:cd 仓库根 && uv run pytest tests/test_messaging_whatsapp_cloud.py tests/test_messaging_teams.py -q → 50 passed(首次因工作目录漂移至 desktop/ui-src 报 file not found,回仓库根重跑成功)。

备注:全部核验只读,未改动任何文件;跑的检查均为原发现点名或直接对应的测试套件。

### 片3

✅W3 片3 核验通过:7 条问题全部处置完毕:6 条已修复(simplex extras 声明+锁文件、UI 四平台转实装卡+凭据指南、sms 账号级 4xx 不再标死信(文案锚定形态收敛)、发信号码不回显解析值、irc 测试头措辞校正、simplex _send_frame 结构化错误包膜),1 条(irc 纯函数蓝本近逐字移植)为记录性质,原判即不判违规——复测确认事实未变(约 30-37 行同款函数仍在,逐函数「蓝本同款」注记 + 文件级 MIT 标注属实,上游 LICENSE 实测 MIT © 2025 Nous Research),维持记录供主档裁量。后端 4 套测试 121 passed,desktop UI 全套 288 passed,均在本次执行。

### 片4

✅W3 片4 核验通过:四项问题全部已解决,证据与实测如下。

【问题1 已解决】修复方式是改文案为如实口径(而非添加 extras 组)。pyproject.toml:30-48 optional-dependencies 现为 crawl4ai/scrapling/firecrawl/skyvern/simplex/llm/vision/all,`grep -rn bluebubbles pyproject.toml` 零命中(exit=1)——extras 组仍不存在,但不再被虚指:src/shishi/push/bluebubbles.py:49-57 的 INSTALL_COMMAND 改为「部署 BlueBubbles 服务端(https://bluebubbles.app…)…发送路实现随 extras 实装批次提供」,不再抛 pip 命令;docstring :12-14 与注释 :50-52 明写「pyproject 尚无 bluebubbles extras 组,不虚指 pip install 'shishi[bluebubbles]'」。测试 tests/test_messaging_bluebubbles.py:74-76 已反转为断言 "bluebubbles.app" in message 且 "shishi[bluebubbles]" not in message,不再钉死错误命令。实测 `.venv/bin/python -m pytest tests/test_messaging_bluebubbles.py -q` → 10 passed。

【问题2 已解决】delivery.py:108-116 新增 `_TOKEN_LEVEL_MARKERS = ("token 获取失败", "token 响应不是 json")`,classify_dead_error 在 forbidden/not_found 判定前先查该表并 return None(delivery.py:206-207);注释 :110-115 明确「HTTP 403/404 不再误判 forbidden/not_found,消息端点状态码语义不变」。msgraph_webhook.py:302 与 qqbot.py:313 的 token 失败文案均含「token 获取失败」,命中 marker。实测(.venv/bin/python 内联脚本,8 组用例):msgraph token 403/404/401 → None,qqbot token 403/404/400 → None;对照组消息端点 403 → 'forbidden'、404 → 'not_found' 保持不变。测试补齐 403/404:tests/test_messaging_qqbot.py:223-229、tests/test_messaging_msgraph_webhook.py:180-187 各有参数化 test_token_403_404_do_not_mark_dead。实测 `.venv/bin/python -m pytest tests/test_messaging_qqbot.py tests/test_messaging_msgraph_webhook.py tests/test_push_delivery.py -q` → 101 passed。

【问题3 已解决】desktop/ui-src/src/screens/messaging/platform-overview.tsx:qqbot(:661-691,3 keys+5 steps)、msgraph_webhook(:692-726,4 keys+5 steps)、bluebubbles(:727-746,steps 4 条;keys 为空数组且注释说明系刻意事实——壳通道当前不读任何环境变量,服务端 password 待发送路实装后补)、yuanbao(:747-766,同款如实口径)四平台全部进入 IMPLEMENTED_PLATFORMS 数组(:88-856);UPCOMING_PLATFORMS(:867-869)现仅剩 signal。EXTRAS_SHELL_PLATFORM_IDS(:953-959)对 bluebubbles/yuanbao/buzz/photon/raft 恒 needs_setup 如实披露(「绿态已连接是误导」),buildPlatformCards(:976-1003)统一渲染实装卡。push/__init__.py:156-170 的 CHANNELS 注册在侧佐证。实测 `npx vitest run src/screens/messaging`(desktop/ui-src)→ 2 文件 65 passed。备注(如实):evidence 末尾提及的 skill/SKILL.md 与 docs/write-a-plugin.md 仍是通道词表列举——经查这两处本就是 schema 词表文档,凭据指南归属地(消息屏 guide)已落地,此项不构成 UI 卡判定的失败。

【问题4 已解决】qqbot.py:189 `for chunk in split_message(content, limit=MESSAGE_LIMIT)`(复用 telegram.py:101 的 split_message,与 discord.py:134/slack.py:135/teams.py:152 同范式),MESSAGE_LIMIT 现有 4 处命中(注释 :24、__all__ :77、定义 :108、使用 :189),不再是死常量;偏离注记已补:qqbot.py:104-107「蓝本 constants.py 的 MAX_MESSAGE_LENGTH = 4000 是 guild 频道消息路径的截断上限(蓝本 guild 分支 content[:4000] 硬截不拆条);MYIA 取 2000 系主动消息路径的取值,与蓝本 guild 常量有意不同,未按其对齐」。测试补齐:tests/test_messaging_qqbot.py:130-164 两用例(超 2000 按行边界拆多条、每条 ≤ MESSAGE_LIMIT、拆条不重取 token;单行超限硬切不丢不发),含在上述 101 passed 内。

所有检查均在本轮实际运行:pytest 三批(10/101 passed)、vitest messaging 套件(65 passed)、classify_dead_error 内联实测(8 用例)、grep/grep -rn 若干(输出如上)。

### 片5

✅W3 片5 核验通过:三条问题均已解决(复检证据为本次会话实读实跑)。

问题1 已解决:desktop/ui-src/src/screens/messaging/platform-overview.tsx 中四家全部移入 IMPLEMENTED_PLATFORMS——a2a 在 771-800 行,指南含 A2A_PEER/A2A_TOKEN 两个凭据 key + SendMessage 冒烟 curl + 直达寻址说明;buzz(801-819)/photon(820-837)/raft(838-855)为 extras 壳卡,keys 留空是刻意事实(壳通道当前零环境变量可录,与既有 bluebubbles/yuanbao 728-766 行同款处理),但指南 steps 已携带 INSTALL_HINT 同款修复路径(buzz CLI+BUZZ_RELAY_URL/BUZZ_PRIVATE_KEY、photon Node sidecar+PHOTON_PROJECT_ID/PHOTON_PROJECT_SECRET、raft CLI+RAFT_PROFILE)。UPCOMING_PLATFORMS(867-869)仅剩 signal;EXTRAS_SHELL_PLATFORM_IDS(953-959)使壳卡恒 needs_setup 并在 statusExplanation(1280-1282)如实披露 dependency_missing。测试覆盖已补:messaging-screen.test.tsx:727-783(四家交互/指南断言)、1141-1177(卡派生+指南 keys 断言),platform-icons.test.tsx:51-70、133-164。实跑 `npx vitest run src/screens/messaging/messaging-screen.test.tsx src/screens/messaging/platform-icons.test.tsx`(desktop/ui-src 下)→ 2 文件 65 测试全过。

问题2 已解决:photon.py:17-23 现表述「蓝本 README 的 PHOTON_HOME_CHANNEL 只文档两形态——space id 或裸 E.164 号码(DM 由号码解析);UUID 是对 space id 的保守接受面,蓝本未给成文样例,不作蓝本归属声明;蓝本 DM 侧唯一具体 GUID 形态是入站 chat GUID any;-;+号码(adapter.py 归一为裸号码,非 UUID)」。已对照蓝本核实:~/.hermes/hermes-agent/plugins/platforms/photon/README.md 的 PHOTON_HOME_CHANNEL 行原文确为 "a space id, or a bare E.164 number (resolved to a DM)"(两形态);adapter.py 1293-1297 行 `_DM_CHAT_GUID_RE = re.compile(r"^any;-;(\+\d{6,})$")` 注释明确归一为裸号码——新 docstring 与原文逐点吻合,过头归属声明已撤。PHOTON_TARGET_RE 注释(50-52)同步改口。实跑 `uv run pytest tests/test_messaging_photon.py -q` → 8 passed。

问题3 已解决:a2a.py:66 引入 scrub_dead_markers,289-297 行对 JSON-RPC error 的 code 与 message 均先滤除 marker 子串再入 PushSendError 文案;delivery.py:147-167 的 scrub_dead_markers 对三张 marker 表(_FORBIDDEN_MARKERS/_CHAT_LEVEL_NOT_FOUND_MARKERS/_SUBCHAT_NOT_FOUND_MARKERS)全量大小写不敏感滤除(命中段→「…」),故对端文案含 forbidden/http 404 字样不再可能经 delivery.py 分类子串命中误标死信,恒瞬态;docstring a2a.py:27-30 已改写为如实描述。测试已覆盖 message 文本路径(原仅 code 路径):test_messaging_a2a.py:297-327 test_jsonrpc_error_peer_text_with_markers_stays_transient 用例构造含 "Forbidden by policy; peer said HTTP 404 and chat not found" 的 message,断言 blob 无 marker 残留且 classify_dead_error → None。实跑 `uv run pytest tests/test_messaging_a2a.py tests/test_messaging_photon.py tests/test_push_delivery.py -q` → 84 passed(分文件 31/8/45)。注:a2a HTTP 层(状态码≥300)文案有意不过 scrub(delivery.py:156-157 注明锚定分类路径不得过滤)——HTTP 状态码非自由文本,属设计内行为,非残留暴露。

### 片6

✅W3 片6 核验通过:问题已解决。复检在当前工作区逐条核验:(1) desktop/ui-src/src/screens/messaging/platform-overview.tsx:867-869 的 UPCOMING_PLATFORMS 仅剩 signal 一项,homeassistant 灰卡与 W3'尚未实装'文案已不存在;(2) platform-overview.tsx:623-656 homeassistant 已转入 IMPLEMENTED_PLATFORMS(wave W3, discovery manual),:630-655 完整 PlatformGuide 落地——keys 为 HASS_URL/HASS_TOKEN/HASS_TARGET,steps 5 步含长期访问令牌创建与 curl 冒烟命令;(3) 头像支持见 platform-icons.tsx:203-205;(4) messaging-screen.test.tsx:650-671 断言已随转——点击 homeassistant 卡详情为'需要设置'(黄)、textContent 不含'尚未实装'、platform-guide-homeassistant 含 HASS_URL/HASS_TOKEN,:814-819 归入'未启用'筛选档,:1126-1131 断言 guide 非空,原问题引用的 :660-677 灰卡断言已被替换;(5) 后端注册仍在 src/shishi/push/__init__.py:126/168/233。测试实跑:npx vitest run src/screens/messaging/messaging-screen.test.tsx src/screens/messaging/platform-icons.test.tsx → 2 文件 65 测全绿;npx vitest run 前端全套 → 20 文件 288 测全绿;uv run pytest tests/test_messaging_homeassistant.py -q → 28 passed。原问题'UI 文案与事实相悖'与伞 PRD 验收项'UI 卡转实装+凭据指南落地'的 UI 半均已落地。

### 横切面

✅横切面 核验通过:W3 横切面 5 项核验全部实跑完成,核心一致性无缺陷:(1) schema 一致——PushChannel Literal 30 值 == PUSH_CHANNELS 元组 == CHANNELS 键集(程序比对零差集);22 家 W3 名单在 schema.py:168-191 与 push/__init__.py:151-174 完全一致;21 家 parse_direct_ref 的 platform= 字面量与注册键逐一相符(grep 实证),raft 有意不设(登记处 __init__.py:215-216 已注明),唯一 name 不匹配是 feishu→feishu_card(前 W3 设计内平台/通道拆名)。(2) `import shishi.push` 通过,CHANNELS=30/PLATFORMS=28,22 家 supports_targeting 全 True;discover_directory 实探 21 家抛 DirectoryDiscoverUnsupported(带各家蓝本事实说明)、仅 simplex 实装发现(沙箱无守护进程连接拒驳=运行时事实);6 家壳通道发送恒报 PushSendError code='dependency_missing'(yuanbao/buzz/photon/raft/signal/bluebubbles 逐一实跑)。(3) CLI 实跑:refresh slack/irc/email 打印 no_discovery 说明+EXIT 0 不假装刷新;--json 显示 telegram→passive、slack/raft→no_discovery、failed:[];未知平台 EXIT 1;simplex 无守护进程→结构化 channels_refresh_failed EXIT 1 且单平台隔离。(4) 现状:全量 pytest 3108 passed/19 skipped/0 failed(58.88s);消息域 638 passed;vitest 消息屏域 2 文件 56 tests 全绿。(5) PRD 对照:行1 后端已做(22 适配器+22 测试文件+注册),但『UI 卡转实装+凭据指南』未做(platform-overview.tsx:266-289 仍全灰卡,测试 :891 锁定 22 张 coming_soon;图标却已备齐 28 家品牌标);行2 企微群 webhook 未做(与登记一致,默认不做);行3 飞书 thread 未做(feishu_card.py:106/576 注明只解析不入路由,与登记一致);行4 黄金回归实际已完成归档(2026-10-04),PRD 仍写 planning/活动区=过期;行5 主人手工门禁为 manual,仓库内无可核验证据。两个验收复选框未勾——与现状相符(后端 28/28 达成,UI/凭据指南/真机冒烟缺)。

> 收口注(2026-10-04,只读复核):横切面第(5)项 PRD 对照中「『UI 卡转实装+凭据指南』未做(platform-overview.tsx:266-289 仍全灰卡,测试 :891 锁定 22 张 coming_soon)」系其核验时点的较早读数——其 vitest 消息屏计数 56 亦早于片 4/5 复检的 65,可推断横切面跑在修复批落地之前;其后片 1/2/4/5/6 复检均为「已转实装+凭据指南落地」。收口会话 grep 实测现状与片 1-6 一致:`platform-overview.tsx:867-869` 的 UPCOMING_PLATFORMS 仅剩 signal 一项,:858-866 注释明记各组已转实装。横切面第(1)-(4)项(一致性/导入/CLI/现状)与片结论无冲突。

**门禁现状(ask 给定口径,记账会话未实跑)**:pytest 本域=绿;vitest 消息屏=绿。

**仍留主人**:企微群机器人 webhook / 飞书话题(thread)两项增量候选、手工门禁清单(TG/企微/钉钉/ntfy 真机冒烟、消息屏视觉过目、拉 bot 入群)保持不动,仍留主人;Acceptance 两个复选框不代勾(每批验收含真机冒烟半项,须主人执行);分批任务档补建与否、工作树未提交修复批的提交,由主人裁量。

## 非目标

- 本伞自身不实装任何平台(纯登记与开工门)。
- 入站/双向(定向出站决议不变)。
