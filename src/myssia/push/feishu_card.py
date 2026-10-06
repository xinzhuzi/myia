"""Feishu interactive-card channel (open.feishu.cn, im/v1/messages).

蓝本归属(10-03-messaging-feishu):定向寻址语义移植自 Hermes
``plugins/platforms/feishu/``(NousResearch/Hermes-Agent,MIT;发送路由见
其 ``adapter.py`` 的 receive_id 选择,直达 id 前缀见 Hermes
``tools/send_message_targets.py`` 的 ``_FEISHU_TARGET_RE``)。MYIA 重写为
自有通道内的两个钩子(:meth:`FeishuCardChannel.parse_direct_ref` /
:meth:`FeishuCardChannel.discover_directory`),绝不整块复制上游。【偏离
注记(grill 事实轮):Hermes feishu 不调任何列表 API,目录纯靠入站会话
回填;MYIA 出站-only 无入站可回填,``im/v1/chats`` 列表发现是 MYIA 侧
新增设计,字段契约以官方文档为准】。

``target`` uses ``env:FEISHU_CHAT_ID`` style references. Card layout mirrors
the production wf-crawl card.json (local-only reference, never committed):
``config.wide_screen_mode`` + blue header + ``lark_md`` divs separated by
``hr`` + a trailing ``note``. With a user template the rendered text becomes
a single ``lark_md`` div inside the same shell. No in-card feedback buttons
yet: the valuable/not-valuable loop is CLI-first today (``myssia feedback
mark``) and the Telegram/Feishu callback *receivers* already speak the
button contract — the buttons themselves land with the desktop UI
(deliberate v0.3 scoping, PRD 10-01-v03-feedback-loop Notes).

immediate 带图(看图 v2,PRD 10-03-vision-v2):``kind="immediate"`` 单条目
且 ``metadata.image_files`` 有本机存在文件时,先经 ``im/v1/images``
multipart 上传首图换 ``image_key``(同一 tenant token,应用需开
``im:resource`` 权限),卡片条目 div 后插 ``img`` 元素;上传失败/文件缺失
降级「图析摘要卡」文本形态(lark_md 图析摘要行 + 配图 N 张注记),只告警
不阻投递。digest 批量不带图;路由/when 逻辑零改动,仅组装层增强。

话题定向(10-04-feishu-thread-send):``context.target.thread_id`` 在场即
改投**话题回复端点** ``POST im/v1/messages/{thread_id}/reply``(root_id
锚定 = 话题根消息 id;三段 spec ``feishu:<名或id>:<thread_id>`` 的解析在
:mod:`myssia.push.targets`,本类 ``supports_threads = True`` 声明 opt-in)。
蓝本锚:Hermes ``adapter.py`` ``_send_raw_message`` 的话题分支(上游
3747-3772 行,``im.v1.message.reply``)。【偏离注记 1:Hermes 的话题回复
是被动回信(入站消息自带 reply_to/root 元数据);MYIA 出站-only 无入站
可依附,是以存量 thread_id 为锚的**主动**话题投递。偏离注记 2:Hermes
在回复目标失效时回退 ``receive_id_type="thread_id"`` 直发(上游 3759-
3760 行)——MYIA 持续不采纳:该 receive_id_type 不在官方成文枚举。话题
根失效的处置随 10-05-push-reliability-batch R2 演进:从「按
``feishu_api_error`` 进死信」升级为**锚失效降级**(见下方「发送护栏」
节——蓝本 ``_feishu_send_with_retry`` 的 create 兜底分支,与被否决的
thread_id 直发是两条不同机制)】。回复端点不收 ``receive_id``/
``receive_id_type``(路径参数即锚),与 create 路径共用同一卡片组装。

发送护栏(10-05-push-reliability-batch R2,缺口②):蓝本 Hermes
``FeishuAdapter._feishu_send_with_retry``(``plugins/platforms/feishu/
adapter.py:3925-3970``,NousResearch/Hermes-Agent,MIT)与
``MAX_MESSAGE_LENGTH=8000``/``_SPLIT_THRESHOLD=4000`` 常量对(上游
1293-1295 行)。三件落地(:meth:`FeishuCardChannel._send_with_retry` /
:func:`_split_item_cards` / :func:`_split_markdown_cards`):

- **瞬态重试**:网络错(``http_error``)/ 5xx·429 状态 / 飞书限流类业务
  码(:data:`TRANSIENT_API_CODES`)→ 指数退避 ``2**attempt`` 秒,总尝试
  :data:`SEND_ATTEMPTS` 次;sleeper 构造注入(默认 :func:`asyncio.sleep`,
  测试钉零等待)。MYIA 刻意收窄:蓝本对**一切**异常重试,MYIA 只认瞬态
  类——配置错(如 99991663 token 失效)立即失败,交死信/重试账本分类。
- **话题锚失效降级**:reply 端点应答码 ∈
  :data:`FEISHU_REPLY_FALLBACK_CODES`(230011/231003,消息被撤回/不存在,
  蓝本同名常量)→ 丢弃话题锚,改投 create 端点向 chat_id 发新消息;多卡
  场景降级只做一次(锚已判死,后续卡直发 create,免在话题群里连环开新话
  题)。【上游护栏「话题内不降级」(metadata.thread_id 在场即跳过降级,
  上游 3943-3949 行,防 create 开新话题)在 MYIA 无从移植:MYIA 唯一的
  reply 路径就是话题路径,且协议面无法辨别话题群,护栏直译会使降级在
  本仓永不可达——PRD R2 括注「话题内不降级,对齐上游」与同句的「reply
  失效码降级新消息」+AC2「降级路径」测试要求在此互斥,本实现**偏离
  括注字面口径**、按投递保真优先裁量:锚失效一律降级并以 warning 留痕
  (不静默);话题群内降级会开出新话题是已记档的已知代价。该裁定系
  实现期裁量而非档面批复(PRD 未载此取舍),留换眼复审/主人追认】
- **卡片长度护栏**:估算载荷(序列化 JSON 字符数)超
  :data:`CARD_SPLIT_THRESHOLD`(对齐上游 ``_SPLIT_THRESHOLD=4000`` 的预拆
  口径:贴近飞书客户端 ~4096 字符分片线)→ 拆多卡发送。拆分不破坏条目
  完整性:内置布局按**条目**贪心装箱,模板输出按**行**边界切;单条目/
  单行自身超阈值时独占一卡(不截断——截断会吃条目、硬切会断 lark_md 链
  接语法;蓝本 8000 硬截断仅适用上游纯文本,卡片版刻意不取)。

组合优先铁律(10-06-hermes-align,主人 10-06 令,最高优先):一轮运行
产出的多条目必须**组合成一条消息**发,绝不逐条单发——① immediate 路由
同轮多条命中的合并发生在派发层(:func:`myssia.push.digest.send_immediate`
按定向 specs 分组、每组一条),消息头=类目+条数由本层兑现:
:func:`card_title` 的 immediate 支带「N 条」后缀,正文=逐条标题+链接
(:func:`_item_markdown` 行);② 文本日报单条消息承载全部条目,仅真超
:data:`POST_SPLIT_THRESHOLD` 才按序续条并头尾标注 ``(i/N)``(拆条是
不得已,不是默认)。

文本消息形态(10-06-hermes-align 批次1,``msg_form: text``):日报照
Hermes 形态发 **markdown 文本**而非交互卡片——``msg_type="post"`` 的
``md`` tag rows 经 ``im/v1/messages`` 发群。蓝本锚(NousResearch/
Hermes-Agent,MIT):

- rows 构建 = 上游 ``_build_markdown_post_rows``(``plugins/platforms/
  feishu/adapter.py:449-481``)直译:无 code fence → 整段单 row;有 fence
  → 每个 fenced code block 独占一 row,fence 前后的 prose 各自成 row
  (上游注释:大元素内混 fence 会被飞书 md 渲染器吞尾部内容);载荷 =
  ``{"zh_cn": {"content": rows}}``(上游 ``_build_markdown_post_payload``,
  443-446 行)。
- 4000 字拆分 = 上游 ``_SPLIT_THRESHOLD = 4000`` 预拆口径(上游 1295 行:
  贴近飞书 ~4096 字符客户端分片线;MYIA 侧 :data:`POST_SPLIT_THRESHOLD`
  与卡片阈值同值同论证),按**行边界**贪心装箱(:func:`_split_post_markdown`
  ——行完整性是卡片版行切分纪律的文本对应物;单行超线独占一段,不截断)。
  多段时每段头尾加 ``(i/N)`` 段指示——组合优先铁律(主人 10-06 令「要
  组合到一起再发送,而不是一条一条的发送」):单条消息承载全部条目是
  默认,拆条是不得已的续条,头尾标注让读者知道这是同一条日报的第几段;
  蓝本同款 = 上游 ``truncate_message`` 的 ``(1/3)`` 段指示
  (``gateway/platforms/base.py:4874``,NousResearch/Hermes-Agent,MIT)。
  【上游对 post 载荷被拒时回退纯文本(``_POST_CONTENT_INVALID_RE``,
  adapter.py:1683-1691)不移植:MYIA 把 ``feishu_api_error`` 交死信/
  重试账本如实可见,不做静默降级】
- markdown 来源:用户 ``template`` 渲染,或内置文本版式(标题行 +
  :func:`_item_markdown` 条目行——lark_md 的 ``**bold**``/``[t](u)``
  与标准 markdown 同形);footer 注记随末段。text 形态不带图
  (:meth:`_attach_card_image` 的 img/图析摘要能力属卡片组装层;
  immediate 带图与 text 形态组合如实不带图,克制取舍)。

双机器人(10-06-hermes-align 批次2,``bot: analyst``):同一通道类支持
第二套飞书应用凭据——蓝本 = Hermes multiplex 双 profile(主 agent
``~/.hermes/.env`` + ``ai-analyst`` profile 独立 ``FEISHU_APP_ID``,
research.md §1 实证);MYIA 落法 = push 条目 ``bot`` 字段选凭据档案
(:data:`BOT_APP_CREDENTIAL_KEYS`,二号 = env/钥匙链规范名
``FEISHU2_APP_ID``/``FEISHU2_APP_SECRET``),tenant token 缓存按 app_id
分键天然隔离;chat id 沿用本条目 ``target`` 解析(缺省主群,不随 bot
切换——蓝本双 profile 同投 FEISHU_HOME_CHANNEL 主群的分工形态)。

Credentials stay references until send time (security baseline: 凭据零明文):
the bot token comes from ``env:FEISHU_BOT_TOKEN`` (or an injected value for
tests). Errors carry reference names only, never resolved values.

All HTTP I/O goes through an injectable ``httpx.AsyncClient`` — tests use
``httpx.MockTransport`` and never touch the real API.
"""

from __future__ import annotations

import asyncio
import json
import logging
import mimetypes
import re
import time
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping, Sequence
from urllib.parse import quote

import httpx

from myssia.push.base import (
    DEFAULT_SEND_TIMEOUT_SECONDS,
    PushSendError,
    SendContext,
    TrendAwareChannel,
    also_seen_list,
    clip_text,
    item_images,
    item_view,
    resolve_channel_credential,
)
from myssia.push.directory import ChannelEntry
from myssia.push.targets import ChannelTarget
from myssia.push.templates import TemplateRenderError, TemplateRenderer
from myssia.schema import CredentialResolveError

__all__ = [
    "API_URL",
    "BOT_APP_CREDENTIAL_KEYS",
    "CAPTION_EXCERPT_CHARS",
    "CARD_SPLIT_THRESHOLD",
    "CHATS_API_URL",
    "CHATS_MAX_PAGES",
    "CHATS_PAGE_SIZE",
    "DEFAULT_TOKEN_ENV_REF",
    "DIRECT_REF_RE",
    "FEISHU_REPLY_FALLBACK_CODES",
    "FeishuCardChannel",
    "IMAGES_API_URL",
    "MARKDOWN_FENCE_CLOSE_RE",
    "MARKDOWN_FENCE_OPEN_RE",
    "MSG_FORMS",
    "POST_SPLIT_THRESHOLD",
    "SEND_ATTEMPTS",
    "TENANT_TOKEN_CACHE",
    "THREAD_ID_RE",
    "TOKEN_API_URL",
    "TOKEN_REFRESH_LEAD_SECONDS",
    "TRANSIENT_API_CODES",
    "TRANSIENT_STATUS_CODES",
    "build_card",
    "build_markdown_card",
    "build_post_payload",
    "build_post_rows",
    "card_title",
    "escape_lark_md",
    "thread_reply_url",
]

logger = logging.getLogger(__name__)

#: Feishu open-platform message endpoint (chat-id receive mode).
API_URL = "https://open.feishu.cn/open-apis/im/v1/messages"
#: Feishu open-platform chat-list endpoint(目录发现;官方字段:items[].chat_id/
#: name/chat_status,翻页 has_more/page_token,page_size 上限 100)。
CHATS_API_URL = "https://open.feishu.cn/open-apis/im/v1/chats"
#: Feishu open-platform image-upload endpoint(immediate 带图,看图 v2):卡片
#: ``img`` 元素的前置步骤——multipart 上传本地图换 ``image_key``。同一
#: tenant access token(Bearer);应用需具 ``im:resource``(上传图片)权限,
#: 部署侧未开通时上传返回非零 code,通道降级图析摘要卡(见 _attach_card_image)。
IMAGES_API_URL = "https://open.feishu.cn/open-apis/im/v1/images"
#: 图析摘要在卡片 lark_md 行 / img alt 内的截断长度(保持卡片可读)。
CAPTION_EXCERPT_CHARS = 240
#: 翻页 page_size(官方默认 20,上限 100;取上限减少往返)。
CHATS_PAGE_SIZE = 100
#: 翻页保底上限(design D2:防服务端 has_more 死循环;20 页 × 100 = 2000 群)。
CHATS_MAX_PAGES = 20
#: Bot credential reference; the value is a tenant access token.
DEFAULT_TOKEN_ENV_REF = "env:FEISHU_BOT_TOKEN"
#: Tenant-token mint endpoint(10-05-push-credential-journey:app_id+app_secret
#: 自换 token,消灭「curl 手工换 + 每 2 小时续命」;凭据位 = 设置→推送
#: 表单存入的钥匙链规范名 ``myia/push/FEISHU_APP_ID``/``FEISHU_APP_SECRET``
#: 与 ``env:`` 同键回退解析)。
#: 蓝本锚:app_id/secret 自换 tenant token 的机制语义对位 Hermes
#: (``FEISHU_APP_ID``/``FEISHU_APP_SECRET`` 凭据位同名;onboarding 探针直调
#: 同一端点,``plugins/platforms/feishu/adapter.py:4245``,NousResearch/
#: Hermes-Agent,MIT);载体刻意偏离——上游运行期由 lark-oapi SDK 托管
#: token 生命周期,MYIA 裸 httpx 故手写 mint+缓存;存储亦偏离——Hermes 存
#: profile ``.env``/config extra,MYIA 按 security-baseline 铁律存系统钥匙链
#: (env: 兼容优先)。(2026-10-05 深度对拍定稿表述)
TOKEN_API_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
#: 缓存失效提前量(秒):expire 减去本值即本地过期线,避免临界命中已失效 token。
TOKEN_REFRESH_LEAD_SECONDS = 120.0
#: 进程内 tenant token 缓存:{app_id: (token, expires_at_monotonic)}。
#: sidecar 常驻进程 2 小时一 mint 足够;重启重 mint 一次可接受(无落盘泄面)。
TENANT_TOKEN_CACHE: dict[str, tuple[str, float]] = {}
DEFAULT_HEADER_COLOR = "blue"
CARD_FOOTER = "MYIA 自动聚合推送 · 条目来自公开论坛分享,注意甄别风险。"

#: 直达对象形态(Hermes ``send_message_targets.py`` 的 ``_FEISHU_TARGET_RE``
#: 同款:oc_ 群/私聊、ou_ open_id、on_ union_id、chat_/open_ 原生 id;可选
#: ``:thread`` 部分自 10-04-feishu-thread-send 起由发送侧兑现——见
#: :meth:`FeishuCardChannel.send` 的话题回复路径)。
DIRECT_REF_RE = re.compile(
    r"^((?:oc|ou|on|chat|open)_[-A-Za-z0-9]+)(?::([-A-Za-z0-9_]+))?$"
)

#: 话题根消息 id 形态(发送侧校验):ASCII 字母/数字/下划线/连字符——与
#: :data:`myssia.push.targets.THREAD_REF_RE` 同款保守集(官方消息 id 形如
#: ``om_xxx``/``mt_xxx``,均在其内);不匹配即结构化报错,解析值不回显
#: (discord 话题同款纪律,10-03-messaging-w3-longtail D1)。
THREAD_ID_RE = re.compile(r"^[-A-Za-z0-9_]+$")

# --------------------------------------------------------------- 发送护栏(R2)

#: 发送包瞬态重试总尝试次数(10-05-push-reliability-batch R2):网络错 /
#: 5xx·429 / 飞书限流类应答按 ``2**attempt`` 秒指数退避重试,总尝试本数。
#: 蓝本锚:Hermes ``_FEISHU_SEND_ATTEMPTS = 3``(``plugins/platforms/feishu/
#: adapter.py:145``,NousResearch/Hermes-Agent,MIT;重试体见其
#: ``_feishu_send_with_retry``,上游 3925-3970 行)。
SEND_ATTEMPTS = 3
#: reply 端点「锚消息被撤回/不存在」类错误码 → 丢弃话题锚,降级为群内
#: create 新消息(多卡只降级一次,见 :meth:`FeishuCardChannel._send_with_retry`)。
#: 蓝本锚:Hermes ``_FEISHU_REPLY_FALLBACK_CODES = frozenset({230011, 231003})``
#: (上游 adapter.py:188,降级分支 3939-3956;MIT 出处同上)。
FEISHU_REPLY_FALLBACK_CODES = frozenset({230011, 231003})
#: 瞬态 HTTP 状态(429 限频 / 5xx 网关抖动;含非 JSON 应答体):退避重试。
#: MYIA 收窄注记:蓝本对一切异常重试,MYIA 只认瞬态类(配置错快速失败)。
TRANSIENT_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
#: 飞书限流类业务码:99991400 = too many request(应用级 QPS 频率限制,
#: 官方错误码);退避后重试通常可自愈。
TRANSIENT_API_CODES = frozenset({99991400})
#: 卡片估算载荷拆分阈值(字符数):超线拆多卡,条目完整(见模块 docstring
#: 「发送护栏」节)。蓝本锚:上游纯文本对 ``MAX_MESSAGE_LENGTH=8000`` 硬截
#: 断 + ``_SPLIT_THRESHOLD = 4000`` 预拆(上游 adapter.py:1293-1295,注释
#: 明言 4000 贴近飞书客户端 ~4096 字符分片线使续拆几乎必然);MYIA 卡片
#: 版不截断只拆分,故单取 4000 预拆线。
CARD_SPLIT_THRESHOLD = 4000

# ------------------------------------------------- 文本消息形态(批次1)

#: 文本形态消息可选值:``card``(缺省,交互卡片)/ ``text``(markdown 文本,
#: post md rows)。构造期校验(schema Literal 是第一道门,这里是直构路径
#: 的纵深防御——cron summary 直构先例)。
MSG_FORMS = ("card", "text")
#: 文本形态拆分阈值(字符数):markdown 按行边界贪心装箱,单段 ≤ 本值。
#: 蓝本锚:上游 ``_SPLIT_THRESHOLD = 4000``(``plugins/platforms/feishu/
#: adapter.py:1295``,NousResearch/Hermes-Agent,MIT——贴近飞书 ~4096 字符
#: 客户端分片线);与 :data:`CARD_SPLIT_THRESHOLD` 同值同论证。
POST_SPLIT_THRESHOLD = 4000
#: code fence 开栏形态(上游 ``_MARKDOWN_FENCE_OPEN_RE`` 同款,adapter.py:110):
#: 行首三反引号 + 语言名(可空),行尾允余空白。
MARKDOWN_FENCE_OPEN_RE = re.compile(r"^```([^\n`]*)\s*$")
#: code fence 闭栏形态(上游 ``_MARKDOWN_FENCE_CLOSE_RE`` 同款,adapter.py:111):
#: 行首三反引号、无语言名(闭栏行带语言名不合法)。
MARKDOWN_FENCE_CLOSE_RE = re.compile(r"^```\s*$")

# ------------------------------------------------- 双机器人凭据档案(批次2)

#: bot 名 → (app_id env 键, app_secret env 键)。缺省(无 bot 字段)= 主
#: 机器人 ``FEISHU_APP_ID``/``FEISHU_APP_SECRET``;``analyst`` = 二号机器人
#: (Hermes ai-analyst profile 的独立飞书应用),凭据位 env/钥匙链规范名
#: ``myia/push/FEISHU2_APP_ID``/``myia/push/FEISHU2_APP_SECRET``
#: (:func:`myssia.push.base.resolve_channel_credential` 的 env→钥匙链回退
#: 同链)。词表与 schema ``push[].bot`` Literal 人工同步(schema 不反依赖
#: push 层)。蓝本锚:Hermes multiplex 双 profile 各持独立 FEISHU_APP_ID
#: (research.md §1 实证);chat id 不随 bot 切换(蓝本双 profile 同投
#: 主群 FEISHU_HOME_CHANNEL 的分工形态)。
BOT_APP_CREDENTIAL_KEYS: dict[str, tuple[str, str]] = {
    "analyst": ("FEISHU2_APP_ID", "FEISHU2_APP_SECRET"),
}


def thread_reply_url(thread_id: str) -> str:
    """话题回复端点 ``im/v1/messages/{root_id}/reply``(root_id = 话题根消息 id)。

    thread_id 经 :func:`urllib.parse.quote` 字面化入路径(防御:path 注入;
    合法形态本就全在 unreserved 集内,quote 是纵深一层)。
    """
    return f"{API_URL}/{quote(thread_id, safe='')}/reply"


def escape_lark_md(text: str) -> str:
    """lark_md 特殊字符字面化:``[`` ``]`` ``<`` 前加反斜杠。

    图析摘要(caption)是模型产物,可能携带 ``[链接式](文本)`` / ``<标签>``
    形态的字符序列 —— 不转义会被飞书解析成残缺链接/标签,摘要被吃掉。
    只处理这三个字符(lark_md 链接与标签语法的最小封闭集),纯装饰性的
    ``[配图 N 张未附]`` 注记是本通道自产文本,不经此函数。
    """
    return text.replace("[", "\\[").replace("]", "\\]").replace("<", "\\<")


def card_title(context: SendContext, *, count: int | None = None) -> str:
    """Production-style card title: 📡 聚合日报 / 🔔 立即推送 / ⏱ 定时摘要.

    ``count``(组合铁律,10-06-hermes-align):immediate 支带「N 条」后缀
    ——同轮合并一条后,消息头=类目+条数是主人令「组合到一起再发送」的
    头部形态;缺省 None 全形态逐字节不变(telegram ``build_message`` 等
    既有调用方零感知)。
    """
    subject = context.category or "情报"
    day = context.date[5:] if len(context.date) >= 10 else context.date
    if context.kind == "immediate":
        title = f"🔔 {subject} · {day}"
        if count is not None:
            title += f" · {count}条"
        return title
    if context.kind == "cron_summary":
        # 定时任务运行摘要卡(10-04-hermes-cron grill Q3 受控扩值):一次性
        # 运行报告,无槽位聚合概念,不挂 slot_label。
        return f"⏱ {subject}定时摘要 {day}"
    return f"📡 {subject}日报 {day} · {context.slot_label}摘要"


def _item_markdown(view: Mapping[str, Any]) -> str:
    """One item as a lark_md line: bold title linked to the source URL.

    合并单卡(v0.4 事件聚合):条目携带 ``also_seen`` 时在主行下追加
    「另见 N 源」列表(每源一个链接,无 url 的源退回纯标题)。
    """
    title = str(view.get("title") or "(无标题)")
    url = view.get("url")
    line = f"**[{title}]({url})**" if url else f"**{title}**"
    category = view.get("category")
    if category:
        line += f" · {category}"
    also = also_seen_list(view)
    if also:
        refs = "、".join(
            f"[{entry['title']}]({entry['url']})" if entry["url"] else entry["title"]
            for entry in also
        )
        line += f"\n　└ 另见 {len(also)} 源: {refs}"
    return line


def build_card(
    items: Sequence[Any],
    *,
    title: str,
    footer: str | None = CARD_FOOTER,
    header_color: str = DEFAULT_HEADER_COLOR,
) -> dict[str, Any]:
    """Build an interactive card with one lark_md div per item (hr between)."""
    elements: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if index:
            elements.append({"tag": "hr"})
        elements.append(
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": _item_markdown(item_view(item))},
            }
        )
    if not elements:
        elements.append(
            {
                "tag": "div",
                "text": {"tag": "lark_md", "content": "本槽位没有待推送条目"},
            }
        )
    if footer:
        elements.append(
            {"tag": "note", "elements": [{"tag": "plain_text", "content": footer}]}
        )
    return _card_shell(title, elements, header_color)


def build_markdown_card(
    markdown: str,
    *,
    title: str,
    footer: str | None = CARD_FOOTER,
    header_color: str = DEFAULT_HEADER_COLOR,
) -> dict[str, Any]:
    """Build an interactive card wrapping one rendered-markdown div."""
    elements: list[dict[str, Any]] = [
        {"tag": "div", "text": {"tag": "lark_md", "content": markdown}}
    ]
    if footer:
        elements.append(
            {"tag": "note", "elements": [{"tag": "plain_text", "content": footer}]}
        )
    return _card_shell(title, elements, header_color)


def _card_shell(
    title: str, elements: list[dict[str, Any]], header_color: str
) -> dict[str, Any]:
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": header_color,
            "title": {"tag": "plain_text", "content": title},
        },
        "elements": elements,
    }


def _card_payload_chars(card: Mapping[str, Any]) -> int:
    """估算载荷 = 序列化 JSON 字符数(``ensure_ascii=False``,中文按 1 字符计,
    与上游字符口径一致)。阈值判定用,宁保守不精确——真实载荷是 HTTP body
    字节数(UTF-8 中文 3 字节),字符数低估字节但高估飞书客户端按字符的
    分片口径,取字符数对齐蓝本语义。
    """
    return len(json.dumps(card, ensure_ascii=False))


def _split_item_cards(
    items: Sequence[Any], *, title: str, threshold: int
) -> list[dict[str, Any]]:
    """长度护栏(内置布局):条目贪心装箱成多卡,估算载荷 ≤ threshold。

    条目完整性是硬约束:单条目自身超阈值时独占一卡(不截断、不切行,
    如实超线发送)。装箱估算按「含 footer」的完整卡计算(footer 实际
    只挂末卡,末卡因此恒在线内,前段卡更小)。
    """
    chunks: list[list[Any]] = []
    current: list[Any] = []
    for item in items:
        if (
            current
            and _card_payload_chars(
                build_card([*current, item], title=title)  # footer 缺省即 CARD_FOOTER
            )
            > threshold
        ):
            chunks.append(current)
            current = [item]
        else:
            current.append(item)
    if current:
        chunks.append(current)
    if not chunks:  # 空批次保住占位卡(「本槽位没有待推送条目」,行为不变)
        chunks = [[]]
    return [
        build_card(
            chunk,
            title=title,
            footer=(CARD_FOOTER if index == len(chunks) - 1 else None),
        )
        for index, chunk in enumerate(chunks)
    ]


def _split_markdown_cards(
    markdown: str, *, title: str, threshold: int
) -> list[dict[str, Any]]:
    """长度护栏(用户模板输出):按行边界切多卡,估算载荷 ≤ threshold。

    行完整性是条目完整性的模板对应物——模板渲染产物无条目结构,行是其
    最近似的完整单元;单行自身超阈值时独占一卡——lark_md 链接语法可横跨
    硬切口,绝不硬切(与 telegram 通道的 plain-text 硬切论证不同:那边
    无 parse_mode)。
    """
    lines = markdown.split("\n")
    chunks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if (
            current
            and _card_payload_chars(
                build_markdown_card("\n".join([*current, line]), title=title)
            )
            > threshold
        ):
            chunks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append(current)
    return [
        build_markdown_card(
            "\n".join(chunk),
            title=title,
            footer=(CARD_FOOTER if index == len(chunks) - 1 else None),
        )
        for index, chunk in enumerate(chunks)
    ]


# ------------------------------------------------ 文本消息形态(批次1)


def build_post_rows(markdown: str) -> list[list[dict[str, str]]]:
    """markdown → post ``md`` tag rows(蓝本 ``_build_markdown_post_rows`` 直译)。

    上游锚:``plugins/platforms/feishu/adapter.py:449-481``
    (NousResearch/Hermes-Agent,MIT)。形状:每个 row 是元素列表,本函数
    恒产单元素 ``[{"tag": "md", "text": segment}]`` row(上游同款——row 的
    多元素位留给富文本 image/a 混排,MYIA 文本形态不涉)。分行为**code
    fence 边界**:大 md 元素内混 fence 会被飞书 md 渲染器吞掉 fence 之后的
    尾部内容,故 fence 前的 prose、fence 自身(整块代码)、fence 后的
    prose 各自成 row;空段(纯空白)跳过。无 fence / 空内容 → 单 row 整段。
    """
    if not markdown:
        return [[{"tag": "md", "text": ""}]]
    if "```" not in markdown:
        return [[{"tag": "md", "text": markdown}]]

    rows: list[list[dict[str, str]]] = []
    current: list[str] = []

    def _flush_current() -> None:
        nonlocal current
        segment = "\n".join(current)
        if segment.strip():
            rows.append([{"tag": "md", "text": segment}])
        current = []

    in_code_block = False
    for raw_line in markdown.splitlines():
        fence_re = MARKDOWN_FENCE_CLOSE_RE if in_code_block else MARKDOWN_FENCE_OPEN_RE
        is_fence = bool(fence_re.match(raw_line.strip()))
        if is_fence and not in_code_block:
            # 开栏:fence 之前的 prose 自成一 row。
            _flush_current()
        current.append(raw_line)
        if is_fence:
            in_code_block = not in_code_block
            if not in_code_block:
                # 闭栏:整个 code block 自成一 row。
                _flush_current()
    _flush_current()
    return rows or [[{"tag": "md", "text": markdown}]]


def build_post_payload(markdown: str) -> str:
    """markdown → post 消息 ``content`` JSON 串(蓝本同构)。

    上游锚:``_build_markdown_post_payload``(adapter.py:443-446)——
    ``{"zh_cn": {"content": rows}}``,``ensure_ascii=False``(中文按字面
    入串,与卡片 content 同口径)。经 ``im/v1/messages`` 以
    ``msg_type="post"`` 发送。
    """
    return json.dumps(
        {"zh_cn": {"content": build_post_rows(markdown)}}, ensure_ascii=False
    )


def _split_post_markdown(markdown: str, *, threshold: int) -> list[str]:
    """文本形态长度护栏:markdown 按**行边界**贪心装箱,单段 ≤ threshold 字符。

    行完整性是卡片版行切分(:func:`_split_markdown_cards`)纪律的文本对应
    物——行是模板产物最近似的完整单元,硬切会断 markdown 链接/列表语法;
    单行自身超阈值时独占一段(不截断,如实超线发送)。蓝本锚:上游
    ``_SPLIT_THRESHOLD = 4000`` 预拆口径(adapter.py:1295);拆分实现取
    MYIA 行边界贪心(上游 ``truncate_message`` 是 8000 字符预算硬拆,偏离
    注记见模块 docstring「文本消息形态」节)。
    """
    lines = markdown.split("\n")
    chunks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if current and len("\n".join([*current, line])) > threshold:
            chunks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        chunks.append(current)
    return ["\n".join(chunk) for chunk in chunks] or [""]


def _is_transient_send_error(error: PushSendError) -> bool:
    """发送失败是否瞬态类(可退避重试):网络错 / 5xx·429 状态 / 限流类业务码。

    蓝本对一切异常重试(上游 3958-3969);MYIA 收窄为瞬态类——配置错
    (99991663 token 失效等)立即失败,交死信/重试账本(R1)按 code 分类。
    """
    if error.code == "http_error":
        return True
    if getattr(error, "http_status", None) in TRANSIENT_STATUS_CODES:
        return True
    return getattr(error, "feishu_code", None) in TRANSIENT_API_CODES


def _is_reply_anchor_lost(error: PushSendError) -> bool:
    """失败是否 reply 端点「锚消息被撤回/不存在」类码(蓝本 fallback codes)。"""
    return error.code == "feishu_api_error" and (
        getattr(error, "feishu_code", None) in FEISHU_REPLY_FALLBACK_CODES
    )


class FeishuCardChannel(TrendAwareChannel):
    """``feishu_card`` channel: one POST per message to open.feishu.cn.

    目录寻址(10-03-messaging-feishu):``supports_targeting=True``,
    ``context.target.chat_id`` 优先、退回 legacy ``target`` 引用(schema
    侧 targets 在场时 target 可省,故构造参数同样可选);``ou_`` 前缀按
    ``receive_id_type=open_id`` 投递(Hermes 发送路由同款),其余维持
    ``chat_id``。话题寻址(10-04-feishu-thread-send):``supports_threads=
    True`` + ``context.target.thread_id`` 在场改投 ``{thread_id}/reply``
    话题回复端点(蓝本锚/偏离注记见模块 docstring「话题定向」节)。

    Args:
        target: credential reference for the receiving chat id
            (``env:FEISHU_CHAT_ID`` style, resolved at send time);与
            ``targets`` 定向配置互斥可省——两条寻址路径至少一条在场,
            否则发送期报 ``missing_target`` 结构化错误。
        template: optional user template (Jinja2); omitted → built-in layout.
        token: pre-resolved bot token (constructor injection for tests);
            resolved from :data:`DEFAULT_TOKEN_ENV_REF` when omitted.
        renderer: template renderer; defaults to a shared sandboxed one.
        client: injectable ``httpx.AsyncClient`` (tests mock here); when
            omitted a per-send client is created with ``timeout``.
        timeout: per-send timeout in seconds for the self-managed client.
        sleep: awaitable backoff sleeper(10-05 R2 发送护栏,构造注入);
            defaults to :func:`asyncio.sleep`,测试钉零等待。
        msg_form: 消息形态(批次1,缺省 ``"card"`` 交互卡片):``"text"`` =
            markdown 文本消息(post md rows 经 ``im/v1/messages``,蓝本
            Hermes 日报形态,见模块 docstring「文本消息形态」节)。
        bot: 出站机器人凭据档案(批次2,缺省 None = 主机器人):
            ``"analyst"`` = 二号机器人(`:data:`BOT_APP_CREDENTIAL_KEYS``
            的 FEISHU2_* 凭据位);chat id 不随 bot 切换。

    Raises:
        ValueError: ``msg_form``/``bot`` 不在词表内(直构路径的纵深防御;
            YAML 路径第一道门在 schema Literal)。
        PushSendError: credential resolution failed, HTTP transport failed
            after the :data:`SEND_ATTEMPTS` transient-retry budget,
            non-JSON response, or Feishu answered a non-zero ``code``
            (配置类码立即失败,不重试)。
    """

    name = "feishu_card"
    #: 目录寻址已开(10-03-messaging-feishu):context.target 优先,legacy
    #: target 兜底;协议判定见 base.Channel docstring。
    supports_targeting = True
    #: 话题寻址已开(10-04-feishu-thread-send):core targets 解析器据此启用
    #: ``feishu:<名或id>:<thread_id>`` 三段回退(targets._split_thread_ref),
    #: 发送侧兑现见 :meth:`send` 的话题回复路径。
    supports_threads = True
    #: 目录发现 429 退避秒数(design D2:退避一次再试;测试可钉 0)。
    discover_backoff_seconds = 1.0

    def __init__(
        self,
        *,
        target: str | None = None,
        template: str | None = None,
        token: str | None = None,
        renderer: TemplateRenderer | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = DEFAULT_SEND_TIMEOUT_SECONDS,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        msg_form: str = "card",
        bot: str | None = None,
    ) -> None:
        if msg_form not in MSG_FORMS:
            raise ValueError(
                f"msg_form 必须是 {MSG_FORMS} 之一(消息形态),当前为 {msg_form!r}"
            )
        if bot is not None and bot not in BOT_APP_CREDENTIAL_KEYS:
            raise ValueError(
                f"bot 必须是 {sorted(BOT_APP_CREDENTIAL_KEYS)} 之一(出站机器人"
                f"凭据档案),当前为 {bot!r}"
            )
        self._target = target
        self._template = template
        self._token = token
        self._renderer = renderer or TemplateRenderer()
        self._client = client
        self._timeout = timeout
        self._sleep = sleep
        self._msg_form = msg_form
        self._bot = bot

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """Render and POST one or more interactive cards carrying ``items``.

        定向优先(``context.target.chat_id`` > legacy ``target`` 引用);
        两条路径都缺席时报 ``missing_target`` 结构化错误(fail-fast,
        绝不猜默认群)。``context.target.thread_id`` 在场即改投话题回复端点
        (root_id 锚定,蓝本锚/偏离注记见模块 docstring「话题定向」节);
        legacy 路径无话题概念,thread_id 恒 None(行为不变)。R2 发送护栏:
        估算载荷超 :data:`CARD_SPLIT_THRESHOLD` 拆多卡(:meth:`_build_cards`),
        每卡经 :meth:`_send_with_retry` 发送包(瞬态退避 + 话题锚失效降级,
        降级后后续卡直发 create)。

        ``msg_form="text"``(批次1)改走文本消息形态:markdown → post
        ``md`` rows 按 :data:`POST_SPLIT_THRESHOLD` 行边界拆段,逐段
        ``msg_type="post"`` 经同一 :meth:`_send_with_retry` 发送包(护栏
        复用;蓝本锚见模块 docstring「文本消息形态」节)。

        Raises:
            PushSendError: on any credential/transport/API failure (callers
                isolate per channel; nothing is raised on success).
        """
        token = await self._obtain_token()
        chat_id = (
            context.target.chat_id
            if context.target is not None
            else self._resolve_target()
        )
        thread_id = (
            (context.target.thread_id or "").strip() or None
            if context.target is not None
            else None
        )
        if self._msg_form == "text":
            # 文本消息形态(批次1):markdown → post md rows,逐段经同一
            # 发送包(瞬态退避 + 话题锚失效降级,R2 护栏零变化);footer
            # 注记随末段(卡片版「footer 只挂末卡」的同款纪律)。多段时
            # 每段头尾加 ``(i/N)`` 段指示(组合铁律:拆条是不得已,标注
            # 让读者知道这是同一条日报的续段;上游 truncate_message 的
            # ``(1/3)`` 指示同款,base.py:4874——头尾各一处,群内折叠
            # 展示时任一端可见)。text 形态不带图(img/图析摘要能力属卡片
            # 组装层,见模块 docstring)。
            segments = self._build_post_segments(items, context)
            total = len(segments)
            for index, segment in enumerate(segments):
                if total > 1:
                    marker = f"({index + 1}/{total})"
                    segment = f"{marker}\n{segment}\n{marker}"
                if index == total - 1 and CARD_FOOTER:
                    segment = f"{segment}\n\n{CARD_FOOTER}"
                body = {
                    "receive_id": chat_id,
                    "msg_type": "post",
                    "content": build_post_payload(segment),
                }
                thread_id = await self._send_with_retry(
                    token, body, thread_id=thread_id
                )
            logger.debug(
                "飞书文本消息已提交: segments=%d slot=%s kind=%s count=%d target=%s",
                len(segments),
                context.slot,
                context.kind,
                len(items),
                context.target,
            )
            return
        cards = self._build_cards(items, context)
        for index, card in enumerate(cards):
            # immediate 带图(看图 v2):先建卡(模板渲染错误在 _build_cards
            # 抛出,零请求发出),再尝试附图——上传/降级均在组装层内闭环,
            # 不阻投递;多卡时图只随首卡(单条目带图与拆卡不同时发生,防御
            # 性保序)。
            if index == 0:
                card = await self._attach_card_image(token, card, items, context)
            body = {
                "receive_id": chat_id,
                "msg_type": "interactive",
                "content": json.dumps(card, ensure_ascii=False),
            }
            thread_id = await self._send_with_retry(token, body, thread_id=thread_id)
        logger.debug(
            "飞书卡片已提交: cards=%d slot=%s kind=%s count=%d target=%s",
            len(cards),
            context.slot,
            context.kind,
            len(items),
            context.target,
        )

    def _build_cards(
        self, items: Sequence[Any], context: SendContext
    ) -> list[dict[str, Any]]:
        """组装发送卡(R2 长度护栏):估算载荷超阈值 → 拆多卡。

        内置布局按条目贪心装箱(:func:`_split_item_cards`),用户模板输出按
        行边界切(:func:`_split_markdown_cards`);不超阈值时单卡,产物与
        历史单卡逐字节同形(含 footer)。
        """
        title = card_title(context, count=len(items))
        if self._template is not None:
            # 契约:send 只抛 PushSendError —— 模板渲染失败(未定义变量/沙箱
            # 拦截等运行期错误;语法错误已在加载期被 schema 拒绝)包装为
            # 结构化的 template_render_error,由调用方按通道隔离。
            try:
                markdown = self._renderer.render(
                    self._template, items, context, **self.trend_render_kwargs()
                )
            except TemplateRenderError as exc:
                raise PushSendError(
                    "template_render_error", f"push[].template 渲染失败: {exc}"
                ) from exc
            return _split_markdown_cards(
                markdown, title=title, threshold=CARD_SPLIT_THRESHOLD
            )
        return _split_item_cards(items, title=title, threshold=CARD_SPLIT_THRESHOLD)

    # ------------------------------------------------ 文本消息形态(批次1)

    def _build_post_segments(
        self, items: Sequence[Any], context: SendContext
    ) -> list[str]:
        """组装文本形态发送段:markdown → 行边界拆段(:data:`POST_SPLIT_THRESHOLD`)。

        markdown 来源两条(与卡片路径同构):用户 ``template`` 渲染(渲染
        失败包 ``template_render_error``,同一契约)或内置文本版式——标题行
        (:func:`card_title`,与卡片同源)+ :func:`_item_markdown` 条目行
        (lark_md 的 ``**bold**``/``[t](u)`` 与标准 markdown 同形,直用);
        空批次保「本槽位没有待推送条目」占位行(卡片版同款)。footer 注记
        由 :meth:`send` 随末段追加,不在此处。
        """
        if self._template is not None:
            try:
                markdown = self._renderer.render(
                    self._template, items, context, **self.trend_render_kwargs()
                )
            except TemplateRenderError as exc:
                raise PushSendError(
                    "template_render_error", f"push[].template 渲染失败: {exc}"
                ) from exc
        else:
            lines = [f"**{card_title(context, count=len(items))}**"]
            lines.extend(_item_markdown(item_view(item)) for item in items)
            if not items:
                lines.append("本槽位没有待推送条目")
            markdown = "\n".join(lines)
        return _split_post_markdown(markdown, threshold=POST_SPLIT_THRESHOLD)

    # ------------------------------------------------- immediate 带图(看图 v2)

    async def _attach_card_image(
        self,
        token: str,
        card: dict[str, Any],
        items: Sequence[Any],
        context: SendContext,
    ) -> dict[str, Any]:
        """Immediate 单条目带图组装:img 元素(上传成功)或图析摘要行(降级)。

        仅 ``kind="immediate"`` 且恰一条目生效(digest 批量不带图,PRD
        10-03-vision-v2 定案);``metadata.image_files`` 缺席 → 卡片原样返回,
        零行为变化。两条路径:

        - 上传成功:条目 div 之后插入 ``img`` 元素(``img_key`` + alt=图析
          摘要截断,无摘要退回标题),内文布局不动;
        - 上传失败 / 文件缺失:降级「图析摘要卡」文本形态——lark_md 附
          「图析: …」摘要行 + 「配图 N 张未附」注记,只告警不阻投递。

        多图只上 ``paths[0]``;alt/摘要行均截断到
        :data:`CAPTION_EXCERPT_CHARS`;摘要行入 lark_md 前经
        :func:`escape_lark_md` 字面化(``[``/``]``/``<``),alt 回退 title 时
        同样截断。
        """
        if context.kind != "immediate" or len(items) != 1:
            return card
        info = item_images(items[0])
        if info is None:
            return card
        elements = card.get("elements")
        if not isinstance(elements, list) or not elements:
            return card  # 防御:非预期卡片形态不动(elements 恒非空,见 build_card)
        image_key: str | None = None
        if info.paths:
            try:
                image_key = await self._upload_image(token, info.paths[0])
            except (PushSendError, OSError) as exc:
                logger.warning("飞书图片上传失败,降级图析摘要卡(不阻推送): %s", exc)
        excerpt = clip_text(info.caption, CAPTION_EXCERPT_CHARS) if info.caption else ""
        if image_key is not None:
            # alt 是 plain_text(零解析),但回退 title 时同样截断到 CAPTION 上限
            # —— 超长标题会让 alt 失去「一眼可读」的辅助语义。
            alt = excerpt or clip_text(
                str(item_view(items[0]).get("title") or ""), CAPTION_EXCERPT_CHARS
            )
            elements.insert(
                1,
                {
                    "tag": "img",
                    "img_key": image_key,
                    "alt": {"tag": "plain_text", "content": alt},
                },
            )
            return card
        # lark_md 行:caption 是模型产物,[]< 序列先字面化再插入(防飞书
        # 误解析成链接/标签把摘要吃掉);「配图 N 张未附」是自产注记,原样。
        lines = [f"　└ 图析: {escape_lark_md(excerpt)}"] if excerpt else []
        lines.append(f"　└ [配图 {info.declared} 张未附]")
        elements.insert(
            1, {"tag": "div", "text": {"tag": "lark_md", "content": "\n".join(lines)}}
        )
        logger.info(
            "飞书卡片采用图析摘要文本形态: 声明 %d 图,本机存在 %d",
            info.declared,
            len(info.paths),
        )
        return card

    async def _upload_image(self, token: str, image_path: str) -> str:
        """Upload one local image → ``image_key`` (``im/v1/images``, multipart).

        官方卡片 ``img`` 元素的前置步骤:multipart 携带 ``image_type=message``
        与图片文件,同一 tenant access token(Bearer)授权;应用需开
        ``im:resource`` 权限,未开通时返回非零 code(调用方降级,不硬造)。

        Raises:
            PushSendError: 文件读取失败、HTTP 传输失败、非 JSON 响应、飞书
                非零 code,或响应缺 ``data.image_key``。
        """
        path = Path(image_path)
        try:
            payload = path.read_bytes()
        except OSError as exc:
            raise PushSendError(
                "image_read_error",
                f"飞书图片读取失败({path.name}): {type(exc).__name__}: {exc}",
            ) from exc
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"image_type": "message"}
        files = {"image": (path.name, payload, content_type)}
        try:
            if self._client is not None:
                response = await self._client.post(
                    IMAGES_API_URL, data=data, files=files, headers=headers
                )
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(
                        IMAGES_API_URL, data=data, files=files, headers=headers
                    )
        except httpx.HTTPError as exc:
            raise PushSendError(
                "http_error", f"飞书图片上传请求失败: {type(exc).__name__}: {exc}"
            ) from exc
        envelope = self._parse_response(response)
        payload_json = envelope.get("data")
        image_key = (
            payload_json.get("image_key") if isinstance(payload_json, Mapping) else None
        )
        if not isinstance(image_key, str) or not image_key.strip():
            raise PushSendError(
                "invalid_response",
                f"飞书图片上传响应缺 data.image_key: {str(envelope)[:200]!r}",
            )
        return image_key

    async def _obtain_token(self) -> str:
        """取 tenant access token:注入 → BOT_TOKEN(env→kc 回退)→ app 凭据 mint。

        10-05-push-credential-journey:三级解析——①构造 ``token=`` 注入
        (测试/显式);②``FEISHU_BOT_TOKEN`` 走
        :func:`~myssia.push.base.resolve_channel_credential`(显式引用优先,
        env 缺失回退钥匙链规范名 ``myia/push/FEISHU_BOT_TOKEN``,手工 token
        用户路径保留);③``FEISHU_APP_ID``+``FEISHU_APP_SECRET``(同一回退)
        在场则自 mint + 进程缓存(过期前 ``TOKEN_REFRESH_LEAD_SECONDS`` 重
        mint)。三级全缺 → ``env_var_missing`` 指引设置→推送。

        双机器人(批次2):``bot=`` 档案在场时**不走**主机器人三级链,直接
        按 :data:`BOT_APP_CREDENTIAL_KEYS` 的 env/钥匙链键位解析二号应用
        凭据 mint(二号无 BOT_TOKEN 手工路径;缓存按 app_id 分键天然隔离);
        缺任一键 → ``env_var_missing`` 指引对应键位。chat id 解析不受影响
        (沿用 ``target``/``targets``,缺省主群)。

        Raises:
            PushSendError: 三级全缺(``env_var_missing``)或 mint 失败
            (``feishu_token_mint_failed``);bot 档案凭据缺
            (``env_var_missing``,文案带二号键位指引)。
        """
        if self._token is not None:
            return self._token
        if self._bot is not None:
            app_id_env, app_secret_env = BOT_APP_CREDENTIAL_KEYS[self._bot]
            app_id = self._resolve_app_credential(app_id_env)
            app_secret = self._resolve_app_credential(app_secret_env)
            if app_id is None or app_secret is None:
                raise PushSendError(
                    "env_var_missing",
                    f"飞书 bot={self._bot} 凭据未录入:需要 {app_id_env} 与 "
                    f"{app_secret_env}(环境变量,或钥匙链规范名 "
                    f"myia/push/{app_id_env} / myia/push/{app_secret_env})",
                )
            return await self._mint_tenant_token(app_id, app_secret)
        try:
            return resolve_channel_credential(
                DEFAULT_TOKEN_ENV_REF,
                env_key="FEISHU_BOT_TOKEN",
                label="飞书 tenant token",
            )
        except CredentialResolveError as bot_token_miss:
            app_id = self._resolve_app_credential("FEISHU_APP_ID")
            app_secret = self._resolve_app_credential("FEISHU_APP_SECRET")
            if app_id is None or app_secret is None:
                raise PushSendError(
                    bot_token_miss.code,
                    f"飞书 bot 凭据解析失败: {bot_token_miss}"
                    "(或录入 FEISHU_APP_ID+FEISHU_APP_SECRET 走自动续期)",
                ) from bot_token_miss
        return await self._mint_tenant_token(app_id, app_secret)

    def _resolve_app_credential(self, env_key: str) -> str | None:
        """App 凭据位解析(env → 钥匙链规范名);缺任一返回 None(交由调用方指引)。"""
        try:
            return resolve_channel_credential(
                f"env:{env_key}", env_key=env_key, label="飞书应用凭据"
            )
        except CredentialResolveError:
            return None

    async def _mint_tenant_token(self, app_id: str, app_secret: str) -> str:
        """Mint + 缓存 tenant token(模块级缓存按 app_id 分键;提前量失效)。"""
        cached = TENANT_TOKEN_CACHE.get(app_id)
        if cached is not None and cached[1] > time.monotonic():
            return cached[0]
        body = {"app_id": app_id, "app_secret": app_secret}
        try:
            if self._client is not None:
                response = await self._client.post(TOKEN_API_URL, json=body)
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(TOKEN_API_URL, json=body)
            envelope = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise PushSendError(
                "feishu_token_mint_failed",
                f"飞书 tenant token 换取请求失败: {type(exc).__name__}: {exc}",
            ) from exc
        token = envelope.get("tenant_access_token")
        expire = envelope.get("expire")
        if envelope.get("code") != 0 or not isinstance(token, str) or not token:
            raise PushSendError(
                "feishu_token_mint_failed",
                f"飞书 tenant token 换取应答非零 code 或缺 token: {str(envelope)[:200]!r}"
                "(核对 app_id/app_secret 与应用发布状态)",
            )
        lifetime = expire if isinstance(expire, (int, float)) else 0
        TENANT_TOKEN_CACHE[app_id] = (
            token,
            time.monotonic() + max(lifetime - TOKEN_REFRESH_LEAD_SECONDS, 0.0),
        )
        return token

    def _resolve_target(self) -> str:
        if self._target is None:
            raise PushSendError(
                "missing_target",
                "feishu_card 未配置 legacy target(env:/keychain: 引用),"
                "本次发送也未携带 context.target——两条寻址路径至少一条在场",
            )
        try:
            return resolve_channel_credential(
                self._target, env_key="FEISHU_CHAT_ID", label="飞书推送群 chat_id"
            )
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"飞书 target 解析失败: {exc}") from exc

    async def _send_with_retry(
        self, token: str, body: dict[str, Any], *, thread_id: str | None
    ) -> str | None:
        """发送包(单卡):瞬态退避重试 + 话题锚失效降级(10-05 R2)。

        蓝本锚:Hermes ``FeishuAdapter._feishu_send_with_retry``
        (``plugins/platforms/feishu/adapter.py:3925-3970``,NousResearch/
        Hermes-Agent,MIT)——指数退避 ``2**attempt`` 秒,总尝试
        :data:`SEND_ATTEMPTS`;reply 应答码命中
        :data:`FEISHU_REPLY_FALLBACK_CODES`(锚消息被撤回/不存在)即置空
        锚、改投 create 新消息(蓝本 ``active_reply_to = None`` 后 ``_raw(
        None)``,降级发送同在本循环的瞬态重试保护内)。**降级不消耗尝试
        槽位**——蓝本的 create 兜底与失败的 reply 同属一个 attempt(上游
        内联执行),MYIA 以「仅瞬态退避递增计数」的 while 循环对齐:末次
        尝试上才降级也能完成改投,不会耗尽预算坠入不可达路径。MYIA 适配
        注记见模块 docstring「发送护栏」节。

        Returns:
            实际生效的话题锚(降级后为 None)——多卡场景后续卡直发
            create:锚已判死,逐卡再探死锚只会在话题群里连环开新话题。
        """
        attempt = 0
        while attempt < SEND_ATTEMPTS:
            try:
                await self._post(token, body, thread_id=thread_id)
            except PushSendError as exc:
                if thread_id is not None and _is_reply_anchor_lost(exc):
                    logger.warning(
                        "飞书话题锚失效(code=%s,消息被撤回/不存在),降级为"
                        "群内新消息(话题群内会开出新话题,以此留痕不静默): %s",
                        getattr(exc, "feishu_code", None),
                        exc,
                    )
                    thread_id = None
                    # 降级不消耗尝试槽位:蓝本的 create 兜底与 reply 同属一个
                    # attempt(上游 ``response = await _raw(None)`` 内联执行,
                    # 上游 3949-3956 行);若以 for 槽位计,末次尝试上的降级会
                    # 耗尽循环坠入不可达断言——修复实录见 10-05 R2 收尾笔。
                    continue
                if attempt >= SEND_ATTEMPTS - 1 or not _is_transient_send_error(exc):
                    raise
                delay = float(2**attempt)
                logger.warning(
                    "飞书发送失败(第 %d/%d 次尝试),%.1fs 后退避重试: %s",
                    attempt + 1,
                    SEND_ATTEMPTS,
                    delay,
                    exc,
                )
                await self._sleep(delay)
                attempt += 1
            else:
                return thread_id
        raise AssertionError(
            "unreachable: retry loop must return or raise"
        )  # pragma: no cover

    async def _post(
        self, token: str, body: dict[str, Any], *, thread_id: str | None = None
    ) -> dict[str, Any]:
        """POST one message:话题回复端点(thread_id 在场)或 create 端点。

        话题路径(10-04-feishu-thread-send):``POST im/v1/messages/{thread_id}/
        reply``,root_id 锚定 = 话题根消息 id(官方契约:话题群内定位既有
        话题必须走回复端点,直发 create 会开新话题);回复体只携带
        ``msg_type``/``content``——不收 ``receive_id``/``receive_id_type``
        (路径参数即锚)。蓝本 Hermes ``_send_raw_message`` 的话题分支;
        偏离注记见模块 docstring。单次往返不重试——重试/降级由
        :meth:`_send_with_retry` 发送包统一持有(R2)。

        Raises:
            PushSendError: 话题 id 形态非法(结构化报错,解析值不回显)、
                HTTP 传输失败、非 JSON 响应或飞书非零 code(携带结构化
                ``feishu_code``/``http_status`` 属性,供重试/降级判定)。
        """
        url = API_URL
        params: dict[str, str] | None = None
        payload: dict[str, Any] = body
        if thread_id is not None:
            if THREAD_ID_RE.fullmatch(thread_id) is None:
                raise PushSendError(
                    "invalid_thread_ref",
                    f"飞书话题 id 形态非法(须为 ASCII 字母/数字/下划线/连字符):"
                    f"得到 {len(thread_id)} 字符的值,不匹配该形态(解析值不回显)",
                )
            url = thread_reply_url(thread_id)
            params = None  # 回复端点无 receive_id_type 查询参
            payload = {"msg_type": body.get("msg_type"), "content": body.get("content")}
        else:
            receive_id = str(body.get("receive_id") or "")
            # ou_ 前缀是用户 open_id,须按 open_id 路由;其余(oc_/chat_/……)
            # 一律 chat_id(Hermes feishu adapter 发送路由同款形态)。
            params = {
                "receive_id_type": "open_id"
                if receive_id.startswith("ou_")
                else "chat_id"
            }
        headers = {"Authorization": f"Bearer {token}"}
        try:
            if self._client is not None:
                response = await self._client.post(
                    url, params=params, headers=headers, json=payload
                )
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(
                        url, params=params, headers=headers, json=payload
                    )
        except httpx.HTTPError as exc:
            raise PushSendError(
                "http_error", f"飞书卡片请求失败: {type(exc).__name__}: {exc}"
            ) from exc
        return self._parse_response(response)

    @staticmethod
    def _parse_response(response: httpx.Response) -> dict[str, Any]:
        try:
            data = response.json()
        except ValueError as exc:
            error = PushSendError(
                "invalid_response",
                f"飞书响应不是 JSON(HTTP {response.status_code}): {response.text[:200]!r}",
            )
            # R2:结构化 HTTP 状态(5xx/429 的非 JSON 应答按瞬态退避重试)。
            error.http_status = response.status_code  # type: ignore[attr-defined]
            raise error from exc
        if not isinstance(data, Mapping) or data.get("code") != 0:
            code = data.get("code") if isinstance(data, Mapping) else None
            message = (
                data.get("msg") if isinstance(data, Mapping) else response.text[:200]
            )
            error = PushSendError(
                "feishu_api_error", f"飞书 API 返回错误: code={code} msg={message}"
            )
            # R2:结构化数值码 + HTTP 状态,供 :func:`_is_transient_send_error`
            # (限流退避)与 :func:`_is_reply_anchor_lost`(锚失效降级)判定。
            error.feishu_code = code if isinstance(code, int) else None  # type: ignore[attr-defined]
            error.http_status = response.status_code  # type: ignore[attr-defined]
            raise error
        logger.debug("飞书 API 调用成功")
        return dict(data)

    # ------------------------------------------------- 目录发现(design D1/D2)

    async def discover_directory(self) -> list[ChannelEntry]:
        """List every group chat the bot belongs to(目录发现,MYIA 新增设计)。

        ``GET im/v1/chats`` 官方契约(实现期已对照文档逐字段核对):items[]
        取 ``chat_id``/``name``,``chat_status`` 非 normal(已解散)跳过;
        ``has_more``/``page_token`` 翻页,保底 :data:`CHATS_MAX_PAGES` 页;
        429 退避一次再试。私聊不在该 API 返回内(官方明示排除 p2p)——
        私聊/话题靠别名文件手工补录(prd Q5 定案)。

        Raises:
            PushSendError: 凭据缺失/失效、HTTP 传输失败、非 JSON 响应或
                飞书返回非零 code(如 401 对应的 token 失效)。调用方
                (:meth:`myssia.push.directory.ChannelDirectory.refresh`)按
                发现失败隔离:告警 + 保留旧桶,不触碰投递死信账本。
        """
        token = await self._obtain_token()
        entries: list[ChannelEntry] = []
        page_token: str | None = None
        for page_index in range(CHATS_MAX_PAGES):
            data = await self._fetch_chats_page(token, page_token)
            entries.extend(
                entry
                for raw in (data.get("items") or [])
                if (entry := self._entry_from_chat(raw)) is not None
            )
            if not data.get("has_more"):
                return entries
            page_token = str(data.get("page_token") or "").strip()
            if not page_token:
                # has_more 却不给游标:防御性止步(不依赖服务端守约)。
                logger.warning("飞书群列表 has_more 但缺 page_token,目录发现提前止步")
                return entries
        logger.warning(
            "飞书群列表翻页达保底上限 %d 页,目录可能不完整(服务端 has_more 未收敛)",
            CHATS_MAX_PAGES,
        )
        return entries

    @staticmethod
    def _entry_from_chat(raw: Any) -> ChannelEntry | None:
        """One ``items[]`` → :class:`ChannelEntry`;形态坏/已解散 → None。

        群列表条目恒为 ``type="group"``、无话题(``thread_id=None``);
        ``name`` 缺失时退回 chat_id 占位(条目仍可按 id 寻址)。
        """
        if not isinstance(raw, Mapping):
            return None
        chat_id = str(raw.get("chat_id") or "").strip()
        if not chat_id:
            return None
        status = str(raw.get("chat_status") or "normal").strip()
        if status and status != "normal":
            logger.debug("跳过非 normal 状态群: chat_id=%s status=%s", chat_id, status)
            return None
        name = str(raw.get("name") or "").strip() or chat_id
        return ChannelEntry(platform="feishu", chat_id=chat_id, name=name, type="group")

    async def _fetch_chats_page(
        self, token: str, page_token: str | None
    ) -> dict[str, Any]:
        """One ``GET im/v1/chats`` page(429 退避一次再试,design D2)。"""
        params: dict[str, Any] = {
            "user_id_type": "open_id",
            "page_size": CHATS_PAGE_SIZE,
        }
        if page_token:
            params["page_token"] = page_token
        headers = {"Authorization": f"Bearer {token}"}
        response: httpx.Response | None = None
        for attempt in (1, 2):
            try:
                if self._client is not None:
                    response = await self._client.get(
                        CHATS_API_URL, params=params, headers=headers
                    )
                else:
                    async with httpx.AsyncClient(timeout=self._timeout) as client:
                        response = await client.get(
                            CHATS_API_URL, params=params, headers=headers
                        )
            except httpx.HTTPError as exc:
                raise PushSendError(
                    "http_error", f"飞书群列表请求失败: {type(exc).__name__}: {exc}"
                ) from exc
            if response.status_code != 429 or attempt == 2:
                break
            logger.warning(
                "飞书群列表 429 限频,退避 %.1fs 重试一次", self.discover_backoff_seconds
            )
            await asyncio.sleep(self.discover_backoff_seconds)
        assert response is not None  # 循环体至少执行一次
        envelope = self._parse_response(response)
        data = envelope.get("data")
        if not isinstance(data, Mapping):
            raise PushSendError(
                "invalid_response",
                f"飞书群列表响应缺 data 对象: {str(envelope)[:200]!r}",
            )
        return dict(data)

    # ------------------------------------------------- 直达解析(design D4)

    @classmethod
    def parse_direct_ref(cls, ref: str) -> ChannelTarget | None:
        """显式 id 直达:``oc_/ou_/on_/chat_/open_`` 前缀不经目录。

        Hermes ``_FEISHU_TARGET_RE`` 同款形态;``oc_x:mt_x`` 的 ``:mt_x``
        部分解析进 ``thread_id``,自 10-04-feishu-thread-send 起由发送侧
        兑现(:meth:`send` 的话题回复路径)。非 id 形态返回 None(调用方
        回落目录四路径解析)。
        """
        match = DIRECT_REF_RE.fullmatch(ref.strip())
        if match is None:
            return None
        chat_id, thread_id = match.group(1), match.group(2)
        return ChannelTarget(
            platform="feishu",
            chat_id=chat_id,
            thread_id=thread_id,
            resolved_from="direct",
        )
