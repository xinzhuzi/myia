# 消息平台增量:飞书话题定向发送

## Goal

主人 2026-10-04「按建议继续做完」点头两项增量候选之一(飞书话题定向发送);
血缘:消息平台树(父档已归档),伞档登记在案。目录侧早已记录
`ChannelEntry.thread_id`/`ChannelTarget.thread_id`(10-03-messaging-feishu
非目标节的承诺),本期补齐**发送侧**:三段 target spec 解析 + 话题内投递。

## 蓝本锚与偏离注记

- **蓝本锚**:Hermes feishu 插件(`~/.hermes/hermes-agent/plugins/platforms/
  feishu/adapter.py`,NousResearch/Hermes-Agent,MIT)的 thread 处理——
  `_send_raw_message`(上游 3747-3772 行):话题内投递走 **reply 端点**
  ``im/v1/messages/{message_id}/reply``;``send_message_targets.py`` 的
  ``_FEISHU_TARGET_RE`` 提供 ``<id>:<thread>`` 直达形态(MYIA 的
  ``DIRECT_REF_RE`` 已同款移植)。
- **偏离 1(主动投递)**:Hermes 的话题回复是**被动**的(入站消息携带
  reply_to/root 元数据,顺手回);MYIA 出站-only 无入站可依附——**主动**
  以存量 thread_id(目录条目或 spec 显式段)作话题根锚定直接投递。
- **偏离 2(不采纳 create 兜底)**:Hermes 在回复目标失效时有 create 兜底
  (上游 ``receive_id_type="thread_id"`` 直发 + 错误码 230011/231003 回退,
  adapter.py:3759-3760 / 188)。MYIA 不采纳:该 receive_id_type 不在官方
  成文枚举(open_id/user_id/union_id/email/chat_id),且回退直发在话题群
  会**开新话题**(官方行为,社区实测同症状)——静默错位投递比诚实失败
  更糟。话题根失效 → 结构化 ``feishu_api_error`` 进死信,如实上报。
- **官方契约核订**(2026-10-04 检索飞书开放平台文档):话题群内定位**既有**
  话题必须走回复端点;``im/v1/messages`` 直发 create 在话题群会创建新话题。
  回复端点路径参数即话题根消息 id(root_id),请求体不收
  ``receive_id``/``receive_id_type``。

## Requirements

- **R1 三段 spec(core targets)**:``feishu:<名或id>:<thread_id>`` 三段解析
  落 :mod:`myia.push.targets`——整体 ref 的既有四路径(直达钩子 → 目录
  精确 id → 精确名 → 唯一前缀)**全部未命中后**追加「末段拆分」回退:
  base 经同一套钩子+四路径解析,命中即返回并携带显式话题段。
  - 话题段字符集保守(``[-A-Za-z0-9_]+``,与 feishu ``DIRECT_REF_RE``
    话题组同款):中文/空格/点号不拆,含冒号的合法名称零误伤;
  - **平台 opt-in**:仅声明 ``supports_threads = True`` 的平台启用拆分
    (本期仅 feishu);其余平台三段 spec 仍按未命中报错,零行为变化;
  - 显式话题段**覆盖**目录条目存量 thread_id(spec 比目录新);
  - 无显式段时目录条目 ``thread_id`` 照旧透传(既有行为,不重述)。
- **R2 话题发送(feishu_card)**:``context.target.thread_id`` 在场 →
  ``POST im/v1/messages/{thread_id}/reply``(root_id 锚定),请求体仅
  ``msg_type``/``content``;thread_id 缺席 → 原 create 路径零变化。
  发送侧形态校验(discord 同款纪律):话题段须匹配保守 id 字符集,非法
  形态结构化报错且**不回显解析值**;thread_id 入 URL 前字面化(防注入)。
- **R3 铁律**:不碰 schema.py(``_TARGET_SPEC_RE`` 的 ``(.+)`` 本就放行
  三段,零 schema 改动);零新依赖(stdlib ``urllib.parse.quote`` 除外);
  并行脏改(src/shishi→src/myia 改名)只追加不回退。

## Acceptance Criteria

- [x] ``feishu:<名或id>:<thread_id>`` 经 ``resolve_target`` 解析:直达 id/
      目录精确 id/精确名/唯一前缀四种 base 全通,thread_id 到位;
      显式段覆盖目录存量;非 opt-in 平台不拆;含冒号名称整体匹配优先。
- [x] httpx mock 验证话题发送:URL 为 ``{API_URL}/{thread_id}/reply``,
      无 ``receive_id_type`` 查询参、体无 ``receive_id``、体携带
      ``msg_type=interactive`` + 卡片 content;无 thread 的发送路径回归不变。
- [x] ``uv run pytest -k "feishu or targets"`` 全绿(含既有回归)。

## Notes

- 死信账本键 = ``platform:chat_id``(不含话题段):同群异话题共享死信键,
  本期不改 delivery.py(任务范围外,如实记录)。
- uuid 幂等去重(回复端点支持)本期不加,与 create 路径对称。
- 蓝本对照:discord 已有 thread_id 发送侧(``/channels/{thread_id}/messages``)、
  a2a 以 thread_id 续 contextId——feishu 本期加入同语汇,supports_threads
  旗标为后续平台(telegram 论坛帖等)预留通用口。
