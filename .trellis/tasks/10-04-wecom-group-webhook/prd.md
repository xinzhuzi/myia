# 消息平台增量:企微群机器人 webhook

## 需求源 / Goal

主人 2026-10-04「按建议继续做完」点头两项增量候选之一(企微群机器人 webhook);血缘:消息平台树(父档 10-03-messaging-w2-platforms 已归档),伞档登记在案。W2 PRD R3 曾将本能力明确列为「群聊/markdown 为蓝本外能力,不做(群机器人 webhook 列为 MYIA 增量候选,默认不做,主人点头才加)」——本档即该点头的落地。

## 【偏离注记】蓝本外增量(全档生效)

蓝本 Hermes ``plugins/platforms/wecom/callback_adapter.py``(NousResearch/Hermes-Agent,MIT)**没有群机器人 webhook 形态**——W2 事实表(10-03-messaging-w2-platforms prd):「仅 msgtype:"text",2048B 分块,收件人只有 touser(私聊);无群、无 markdown、无卡片」。本任务全部新增能力为 **MYIA increment**,与蓝本无对应段;``src/myia/push/wecom.py`` 既有蓝本标注(token 生命周期/text 私聊/2048B 分块)原样保留,新增段落一律标 ``MYIA increment · 10-04-wecom-group-webhook``。上游无对应实现,不存在「照抄形态」;官方事实全部核订自腾讯开发者文档「群机器人配置说明」(developer.work.weixin.qq.com/document/path/91770,2026-10-04 拉取)。

## 官方事实核订(群机器人 webhook,doc 91770)

- 端点 ``POST https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=<key>``;key 为 webhook URL 的 query 参数,官方示例形态 ``key=693a91f6-7xxx-4bc4-97a0-0ec2sifa5aaa``(UUID 段式,示例含掩码字符;实装按标准 hex UUID 8-4-4-4-12 判形,见设计 D1)。
- msgtype 族:text / markdown(markdown_v2)/ image / news / file / voice / template_card;本增量只做 **markdown**。
- 长度:text content 最长 **2048 字节**、markdown content 最长 **4096 字节**(原文「markdown内容,最长不超过4096个字节」),均 utf8。
- 频率:每机器人 **20 条/分钟**(原文);超限错误码本页未列(社区核订 45009)。
- 文档明示 webhook URL 是凭据(「一定要保护好消息推送的webhook地址,避免泄漏」)→ 沿用 ``env:``/``keychain:`` 引用基线。
- 群 webhook **免 access_token**(无 corpid/secret/gettoken 环节),也就无 40001/42001 重试环。

## 设计定案

- **D1 target 双形态,发送期按解析值形态分流**(主人建议定案):wecom 通道的 target(``push[].target`` 或 ``context.target.chat_id``)解析值二义——
  - **私聊形态(现状,蓝本)**:corpid+corpsecret+agentid 三凭据 → ``gettoken`` → ``message/send`` ``msgtype=text``、touser 寻址、2048B 分块——一行不动;
  - **群形态(MYIA increment)**:解析值为群机器人 webhook key——**裸 UUID**(8-4-4-4-12 hex)或**完整官方 webhook URL**(host 锚定 ``https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=…``,从中提取 key)——即 ``POST /cgi-bin/webhook/send?key=…``,body ``{"msgtype": "markdown", "markdown": {"content": …}}``,**4096 字节**分块(复用 :func:`split_utf8_chunks` 的 ``limit`` 参数,行边界优先语义同款)。
  - 判形严格全串匹配(剥首尾空白),不子串嗅探;**判形先于 ``corpid:userid`` 拆分**(完整 URL 含 ``://`` 会被既有拆分破坏)。
- **D2 schema 零改(核订结论)**:群形态 target 仍是纯 ``env:``/``keychain:`` 引用(``_check_target_ref`` 不动),wecom 通道「target 或 targets 至少其一」的必填约束对群形态同样成立(target=key 引用在场)——**无任何校验需要放宽,schema/pipeline 零改动**;测试钉住该结论(PushConfig 直接收口 + golden 零回归)。
- **D3 死信分类沿用不新译**:群形态错误文案同款带 ``errcode=<n>``,走既有 :data:`_FORBIDDEN_MARKERS`/:data:`_CHAT_LEVEL_NOT_FOUND_MARKERS` 码表(40001/42001/60020/60021/81013 → forbidden;40003/60111/46004 → not_found;45009/``-1``/超时无 marker = 瞬态)。webhook 形态语义与应用消息同表,不新增码、不改 delivery.py。
- **D4 直达/别名天然兼容**:UUID 命中既有 :data:`USERID_RE`(字母/数字/``-``/``_``,36 ≤ 64),``wecom:<uuid>`` 直达即群形态;别名登记 chat_id=key 同理(dingtalk 别名登记完整 webhook URL 同款先例)。**已知限制(登记)**:UUID 形态的合法 userid 会被判群形态 → webhook 端点报 key 无效,结构化失败不误投;规避 = 别名登记该 userid。
- **D5 频率不做客户端限速**:20 条/分钟超限落 45009(瞬态),与全通道「不做客户端 pacing」同款取舍,由摘要留池/重试语义吸收。

## Requirements

1. **R1 双形态分流**(:meth:`WecomChannel.send`):target 解析值为 key 形态 → 群路径(零 gettoken、零 access_token、无重试环);否则原私聊路径逐字节不变。
2. **R2 群发送**:`POST /cgi-bin/webhook/send?key=…`,`msgtype=markdown`,4096 字节分块逐块顺序发送;errcode≠0 → ``wecom_api_error`` 带 ``errcode=<n>``;非 JSON → ``invalid_response``;传输失败 → ``http_error``(全部结构化,文案不带 key 值)。
3. **R3 常量与判形函数落 ``wecom.py``**(`WEBHOOK_SEND_URL`/`WEBHOOK_KEY_RE`/`WEBHOOK_URL_RE`/`WEBHOOK_MARKDOWN_MAX_BYTES`/``parse_webhook_key``),模块/成员 docstring 增量段全标 MYIA increment,蓝本归属块原样。
4. **R4 schema/pipeline 零改**(D2 核订),测试钉住。
5. **R5 测试**(tests/test_messaging_wecom.py 增群形态用例,httpx mock):裸 key / 完整 URL / context.target(UUID)三路、4096 分块、errcode 结构化+瞬态分类、UUID 歧义钉板、schema 零改钉板;私聊形态既有用例零回归。

## Acceptance Criteria

- [x] 群形态:target 解析为裸 key 或完整官方 URL → POST ``webhook/send?key=…``、``msgtype=markdown``、零 gettoken 调用。
- [x] ``context.target.chat_id`` 为 UUID 时同走群形态(定向/别名路)。
- [x] 超长内容按 4096 字节分块,块序即发送序,每块 ≤4096B。
- [x] errcode≠0 → ``wecom_api_error`` 文案带 ``errcode=<n>``;45009 分类瞬态(None)。
- [x] 私聊形态零回归:既有 33 用例全绿 + 新增用例绿(``uv run --no-sync python -m pytest tests/ -q -k wecom``)。
- [x] schema 零改钉板:群形态配置 ``PushConfig(channel="wecom", target="env:WECOM_WEBHOOK_KEY")`` 直接收口;「无 target 且无 targets 仍拒」不变。
- [x] 零新依赖;蓝本标注保留、增量段标 MYIA increment;task.json/git 未动(并行脏改只追加)。

## 非目标

- 群 webhook 其余 msgtype(image/news/file/voice/template_card/markdown_v2)——单形态 markdown 即通知场景所需。
- 客户端限速/配额(D5)。
- 桌面 UI 凭据指南文案与 docs/{zh,en}/schema.md 的群形态说明——随消息文档线另行走档(本档实现零依赖)。
- 企微应用消息的 markdown/卡片(蓝本外且非本增量对象;应用侧维持 text)。

## Notes

- 执行环境注记:本任务进行中遇到并行 ``src/shishi → src/myia`` 全仓改名(会话中途落盘);实装按新路径 ``src/myia/push/wecom.py`` 落档,自测在新包名下通过。影响面核订:GitNexus ``impact WecomChannel upstream`` = LOW(2 个直接 import:pipeline.py、push/__init__.py;0 process),构造签名与公开面零变化。
- 官方文档依据:developer.work.weixin.qq.com/document/path/91770(群机器人配置说明,2026-10-04);key UUID 形态以官方 URL 示例 + 社区一致实践核订,判形不命中即结构化报错(fail-fast,不静默回落)。
