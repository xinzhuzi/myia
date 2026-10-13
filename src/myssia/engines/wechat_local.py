"""微信本机会话引擎(显式 ``engine: wechat_local``;10-12-weixin-feed-channel).

主人令翻案 G3(10-11 档「仅展示不入管线」):微信消息经 wechat-bridge 桥
读回后**入 store/dedup/feed**,与 telegram 同为情报流一等渠道。

三通道(``engine_options.wechat_local.channel``,缺省 ``pixel`` 向后兼容;
主人令 2026-10-13 换轨:像素链 OCR 逻辑性/准确性判例成立 → TMS 源切
``localdb`` 本地库直读;同日 sns 批加朋友圈):

- **pixel(缺省)**:数据面 = 管线进程内起本机桥子进程
  (``wechat-bridge messages read <chat> -k N --json``,受管组件,
  ``myssia.push.weixin_local`` 的 ``bin_path``/``run_bridge_command_sync``/
  ``parse_bridge_payload`` 同组 helper,与 :mod:`myssia.wechat_local_sidecar`
  的 ``_run_bridge`` 同款封装)。**不经 sidecar**:``wechat_local.*`` sidecar
  方法保持纯 UI 探针/浏览面,数据面从不绕道桌面 IPC —— 引擎跑在 cron/CLI
  进程里,sidecar 可能根本不在场(tg_web 自持 Playwright 传输同构论证)。
- **localdb**:数据面 = 同一桥子进程的 ``localdb query <chat> --since Nd
  --json``(桥 0.3.2 Phase E;E1 密钥 → E2 解密副本 → E3 message/session/
  contact 三域只读 SQL)。**只读语义**:查询走解密副本,对微信进程**零
  交互零截窗零 AX** —— 本分支绝不触碰任何截窗/AX 面(与 pixel 分支完全
  隔离;桥侧同纪律:localdb 命令族不跑 UI 前置检查)。增量窗口 = 源级
  水位(见下)。
- **sns**(10-13-wechat-sns-feed):数据面 = 同一桥子进程的
  ``localdb sns feed|notices --since Nd --json``(桥 0.6.0;朋友圈域
  SnsTimeLine XML / SnsMessage_tmp3 互动通知)。朋友圈无会话概念:
  不消费 ``chat``/``sides``/``count``(声明即拒),专属键 ``feed_kind``
  (feed=动态缺省/notices=互动通知)。**强幂等锚**:动态用微信侧全局 id
  (``#wxsns-<id>``)、通知用表主键(``#wxsnsn-<local_id>``)—— 比消息通道
  的内容哈希锚强(TG 同级),重读/重装恒同锚。**可疑空水位防御**:feed
  零条目且桥报 parse_errors>0(XML 坏行吞噬整窗的形状)= 不推进水位
  (下轮重开同窗,微信 XML 格式变化不丢中间窗口);正常安静窗照常推进。

源 YAML 形态(design §2.1 + 换轨批):

.. code-block:: yaml

    - name: weixin-<会话名>              # 源名全称律(G7 对称纪律)
      engine: wechat_local
      url: "https://weixin.qq.com"       # 锚(schema http(s) 形状要求;引擎零 HTTP)
      empty_ok: true                     # 空态/密钥缺位 = 合法空
      engine_options:
        wechat_local:
          channel: localdb               # pixel(缺省)| localdb(本地库直读)
          chat: "<会话名或会话 id>"       # 见「chat 寻址」节
          since_days: 3                  # localdb:首拉/无水位窗口(缺省 3 天)
          sides: [left]                  # 采集侧:缺省 left=对方;right=自己
          read_timeout_seconds: 600      # localdb 缺省 600;pixel 缺省 60

**pixel 硬边界(绝不张冠李戴)**:桥不能点击切换会话(静默铁律,合成点击
被禁),每轮只读微信主窗**当前打开会话**的消息区。源声明 ``chat`` 与桥回报
的 ``chat.match`` 核对:``false`` = 结构化空态 ``chat_not_open``(skip 理由
人话含当前标题 vs 声明,主人可对齐);``null``(标题不可读)= 空态
``chat_title_unreadable``。载荷绝不归到不匹配源名下。**该三态核对族仅
pixel 通道适用**(localdb 无窗口概念,另有自己的空态族,见码表)。

**localdb chat 寻址**:桥按库内 ``strTalker`` 精确匹配查消息,即 ``chat``
理想形态是微信会话 id(``wxid_xxx`` / ``xxx@chatroom``)。兼容声明**会话
显示名**(与 pixel 同形,如「TMS 中转站交流」):首查零消息且 contact 域
解析不出展示名时,拿应答 ``sessions`` 列表按名精确匹配解析出会话 id 再查
一次(至多两查;``sessions`` 是桥 best-effort 前 20 行,不在列表 = 解析
不到,如实零产出不猜)。想免去二查,直接声明会话 id 即可。

**锚 = 内容哈希,非平台消息 id**(design §2.3,如实弱幂等):

    hash = sha1( chat | ts | side | normalize(text) )[:16]
    url  = wechat-local://chat/<urlencoded(chat)>#wx-<hash>

- pixel:MessageRow 只有 ts(最近居中时间标记原文,无绝对日期)/side/
  text,没有消息 id —— OCR 修字/置信度波动使文本微变 → 新锚(重复条目
  风险,残留靠 feed 读态消化);ts 锚缺失段内同文本同侧消息会并锚。
- localdb:**桥应答消息行无 id 字段**(实探桥 ``localdb_query.query_messages``
  只选 时间/内容/类型/发送者 四列,ts=epoch 秒、sender="me"|会话id、
  文本原样)—— 强幂等锚 ``#wxdb-<chat>-<msgid>``(TG ``#tg-`` 形态同款)
  **无从铸,不谎报**;退同一内容锚:ts 是精确 epoch、文本无 OCR 噪声,
  重读同消息恒同锚(幂等性远强于 pixel),残留并锚面 = 同秒同侧同文本
  (如实)。桥应答未来加 id 字段时可升级(档注明:2026-10-13 探明无)。
- 同窗重读同消息 → 同锚 → dedup 沉默。``wechat-local://`` 自定义 scheme
  (非 http(s))是**有意**:私聊消息没有公开 URL,「打开原文/复制链接」
  如实缺席(前端 ``isOpenableUrl`` 判 false);正文内粘贴的 http(s) 链接
  不受影响。

**localdb 水位(源级增量窗口)**:上次成功拉取时刻记在 store 的
``change_baseline`` 表(键 ``wechat-local://watermark/<源名>``,``etag``
存 epoch 秒)—— 通用 kv 面零 schema 改动;pipeline 清理从不传
``active_urls``(共享库安全缺省,sqlite.py cleanup 契约),水位行不会被
误剪。``--since`` 天数 = ``max(1, ceil(现在-水位)/86400)``(桥按天开窗,
天粒度向上取整 → 相邻轮次天然小幅重叠,dedup 消化);无水位(首拉/试抓
无 store)= ``since_days`` 源配置(缺省 3 天)。**仅成功拉取推进水位**;
key_unavailable 跳过/超时/失败都不推进(下轮重开同窗,不丢消息)。

**错误码表**(桥具名错误族原样透传,与 tg_web 的
session_missing/logged_out/dom_stale 哨兵同纪律,绝不装死;★ = 仅该通道):

===========  ==========================  ====================================
error_type   面                          语义
===========  ==========================  ====================================
component_missing  桥组件缺席             bin 不存在/不可执行(fix_hint 指安装)
bridge_timeout     子进程超时              MYIA 侧 kill 兜底;桥内码 ``timeout`` 同归
wechat_not_running / screen_recording_denied / window_closed / ax_permission_denied /
ax_tree_empty      桥具名族(pixel)       码名原样作 error_type(§6 码表)★
chat_not_open      结构化空态(skip)      pixel:当前打开会话与声明不符 ★
chat_title_unreadable  结构化空态(skip)  pixel:可见标题不可读,无法核对归属 ★
key_unavailable    结构化空态(skip)      localdb:解密密钥未就绪(exit 21,
                                          D4 合法预期态——不算 failure 免告警;
                                          指引:跑 scripts/wechat-bridge-d4-keyscan.sh)★
db_not_found / decrypt_failed  桥具名族(localdb)  码名原样作 error_type ★
bridge_error       应答不可解析            stdout 非契约 JSON(重装/升级桥)
===========  ==========================  ====================================

robots 论证(tg_web 同口径):本引擎驱动的是**已授权本机微信客户端**
(pixel 像素读回或 localdb 解密副本查询),不对任何站点发请求,robots.txt
语义不适用;``respect_robots`` 配置零消费(引擎不走 :meth:`BaseEngine.request`
的 robots/限速面 —— 唯一的「端点」是本机桥子进程)。

其余边界:单轮窗口语义(pagination 配置即结构化拒,urlwatch/tg_web 判例);
静默铁律全程(桥只读命令,不新增任何写通道/点击/激活;localdb 对微信进程
零交互);私有数据红线(消息内容只活在桥 stdout → 管线内存 → store;本模块
日志只留形状 —— 计数/会话名/码名,永不打 text/sender 原文);pixel 多源
并发成本如实(每源一次桥读 = 一次截图+OCR,同轮多源重复读同一窗口,v1
接受;localdb 无此面 —— 按库查询,与会话窗口无关)。

Raises:
    FetchError: engine_options 形状错 / 源 URL 不符契约 / 桥组件缺席 /
        桥超时 / 桥具名错误族(除 key_unavailable = 结构化 skip)/
        应答不可解析 / pagination 配置。
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import math
import os
import re
import time
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

from myssia.engines.fetch_base import BaseEngine, FetchError
from myssia.push.weixin_local import (
    LocalBridgeTimeoutError,
    bin_path,
    parse_bridge_payload,
    run_bridge_command_sync,
)

logger = logging.getLogger(__name__)

#: 引擎名(schema ``EngineName`` 词表一员;链外源,不进 AUTO_CHAIN)。
ENGINE_NAME = "wechat_local"
LAYER = "LOCAL_BRIDGE"

#: 官方域锚(schema ``SourceConfig.url`` 强制 http(s) 的形状落点;引擎零 HTTP,
#: 请求「端点」是本机桥子进程 —— telegram-web.yaml 锚判例同构)。
WEB_HOST = "weixin.qq.com"

#: 通道词表(换轨批+sns 批):pixel = 像素链截窗 OCR(缺省,向后兼容);
#: localdb = 本地库解密副本直读(只读,零截窗零 AX);sns = 朋友圈域
#: (动态/互动通知,零截窗零 AX,强 id 锚)。
CHANNELS = ("pixel", "localdb", "sns")
DEFAULT_CHANNEL = "pixel"

#: sns 模式词表:feed = 朋友圈动态(SnsTimeLine)/notices = 互动通知
#: (SnsMessage_tmp3 赞/评)。
SNS_KINDS = ("feed", "notices")
DEFAULT_SNS_KIND = "feed"

#: 最近 K 条缺省(pixel 单轮窗口帽;桥像素链现存消息,不滚动翻历史)。
DEFAULT_COUNT = 50
#: count 域上界(sidecar 协议 ``_LIMIT_MESSAGES_MAX`` 同值,桥内另有配置兜底)。
MAX_COUNT = 200

#: localdb 首拉/无水位历史窗口缺省(天;换轨批合理缺省 3d)。
DEFAULT_SINCE_DAYS = 3
#: since_days 上界(sidecar 协议 ``_SINCE_DAYS_MAX`` 同值:防一把梭全量拉取,
#: 桥内另有 limits 兜底;不是业务约束)。
MAX_SINCE_DAYS = 3650

#: localdb 查询超时缺省(秒;sidecar ``_QUERY_TIMEOUT_SECONDS`` 同款判例:
#: 桥侧 sqlcipher 单库解密上界 300s,密钥就绪后首查大概率触发多域副本首建,
#: 累计可超 60s —— 取 2×单库上界盖住;副本 kept 语义让超时重试只补缺库)。
DEFAULT_LOCALDB_TIMEOUT_SECONDS = 600.0

#: 采集侧词表(桥消息行 side:left=对方 / right=自己 / center=系统行;
#: localdb 由 sender 派生:"me" → right,其余(会话 id)→ left)。
SIDES = ("left", "right", "center")
#: 缺省只采对方消息(left)—— 情报源语义;right/center 显式声明才收。
DEFAULT_SIDES = ("left",)

#: pixel 单次桥读(截图+OCR)超时缺省(秒;= ``DEFAULT_BRIDGE_TIMEOUT_SECONDS``
#: 同值口径,本地单命令上界,超时 kill 兜底)。
DEFAULT_READ_TIMEOUT_SECONDS = 60.0

#: 标题截断(TG 同律:标题 = 首行/全文截断;feishu ``text[:80]`` 判例)。
TITLE_MAX_CHARS = 80

#: 锚前缀与 scheme(design §2.3;#wx- 与 #tg-/#fs- 同族命名;sns 批加
#: #wxsns-/#wxsnsn- 强 id 锚族)。
ANCHOR_SCHEME = "wechat-local://"
ANCHOR_PREFIX = "#wx-"
SNS_ANCHOR_PREFIX = "#wxsns-"
SNS_NOTICE_ANCHOR_PREFIX = "#wxsnsn-"

#: localdb 水位键前缀(store ``change_baseline`` 表的引擎自有命名空间;
#: 与条目锚同 scheme 家族,不与任何 http(s) 源 URL 相撞)。
WATERMARK_PREFIX = "wechat-local://watermark/"

#: localdb 密钥缺位 skip 的指引面(D4 一键脚本;主人 sudo 执)。
KEYSCAN_SCRIPT = "scripts/wechat-bridge-d4-keyscan.sh"

#: 内容哈希的文本规整(压空白):OCR 行间空格抖动不另立新锚的缓解面。
_WS_RE = re.compile(r"\s+")

__all__ = [
    "ANCHOR_PREFIX",
    "ANCHOR_SCHEME",
    "CHANNELS",
    "DEFAULT_CHANNEL",
    "DEFAULT_COUNT",
    "DEFAULT_LOCALDB_TIMEOUT_SECONDS",
    "DEFAULT_READ_TIMEOUT_SECONDS",
    "DEFAULT_SIDES",
    "DEFAULT_SINCE_DAYS",
    "DEFAULT_SNS_KIND",
    "ENGINE_NAME",
    "KEYSCAN_SCRIPT",
    "LAYER",
    "MAX_COUNT",
    "MAX_SINCE_DAYS",
    "SIDES",
    "SNS_ANCHOR_PREFIX",
    "SNS_KINDS",
    "SNS_NOTICE_ANCHOR_PREFIX",
    "TITLE_MAX_CHARS",
    "WATERMARK_PREFIX",
    "WEB_HOST",
    "WechatLocalEngine",
    "anchor_url",
    "sns_anchor",
    "sns_notice_anchor",
    "watermark_key",
]


def _normalize_text(text: str) -> str:
    """压空白(空格/换行/制表 → 单空格 + 去首尾):OCR 微抖动的锚稳定面."""
    return _WS_RE.sub(" ", text).strip()


def anchor_url(chat: str, ts: str | None, side: str, text: str) -> str:
    """铸内容哈希锚:``wechat-local://chat/<urlencoded(chat)>#wx-<sha1[:16]>``.

    盐 = ``chat | ts标记 | side | 压空白文本``(design §2.3):ts/side 入盐
    缓解「ts 缺失段内同文本并锚」面;同窗重读同消息 → 同锚(dedup 幂等),
    文本微变(OCR 修字)→ 新锚(如实弱幂等,见模块文档)。localdb 通道
    ts 传 str(epoch 秒)—— 精确时间入盐,同会话同文本不同时刻不并锚。
    """
    digest = hashlib.sha1(
        f"{chat}|{ts if ts is not None else ''}|{side}|{_normalize_text(text)}".encode(
            "utf-8"
        )
    ).hexdigest()[:16]
    return f"{ANCHOR_SCHEME}chat/{quote(chat, safe='')}{ANCHOR_PREFIX}{digest}"


def sns_anchor(entry_id: str) -> str:
    """朋友圈动态强锚:``wechat-local://sns/<id>#wxsns-<id>``.

    id = 微信侧全局 id(桥 XML 解析;全期稳定)—— 与消息通道的内容哈希锚
    不同,**重读恒同锚**(TG ``#tg-`` 同级幂等),OCR/解析噪声零并锚面。
    """
    return f"{ANCHOR_SCHEME}sns/{quote(entry_id, safe='')}{SNS_ANCHOR_PREFIX}{entry_id}"


def sns_notice_anchor(local_id: object) -> str:
    """互动通知强锚:``wechat-local://sns/notice/<id>#wxsnsn-<id>``(表主键)."""
    return (
        f"{ANCHOR_SCHEME}sns/notice/{local_id}"
        f"{SNS_NOTICE_ANCHOR_PREFIX}{local_id}"
    )


def watermark_key(source_name: str) -> str:
    """源级水位键(store ``change_baseline`` 命名空间;源名 = 条目盖戳键)."""
    return f"{WATERMARK_PREFIX}{quote(source_name, safe='')}"


class WechatLocalEngine(BaseEngine):
    """微信本机会话源(显式 ``engine: wechat_local``;本机桥直调,零 HTTP).

    items 出口对齐 ``Item.from_extracted`` 契约:url(``#wx-`` 内容哈希锚)/
    title(首行截断)/content(全文);观测键(``sender``/``side``/``ts``/
    ``conf``(pixel)/``chat``)留 raw 面(metadata,feed v1 不投影 —— 设计
    定案,投影须 bump PROTOCOL_VERSION 三处同步)。
    """

    LAYER = LAYER
    ENGINE_NAME = ENGINE_NAME
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """engine_options.wechat_local 校验与缺省化(错型即结构化拒).

        通道词表 ``channel``:缺省 pixel(向后兼容);pixel/localdb 共享
        chat/sides,专属键交叉声明即拒(count 属 pixel,since_days 属
        localdb);sns 通道无会话概念(chat/sides/count 全不消费,专属键
        feed_kind)—— 消费面不同,静默忽略会谎报配置生效。
        """
        options = self.engine_options()
        channel = options.get("channel", DEFAULT_CHANNEL)
        if isinstance(channel, bool) or channel not in CHANNELS:
            raise FetchError(
                f"engine_options.wechat_local.channel 应为 {'/'.join(CHANNELS)} "
                "(pixel=像素链截窗 OCR 缺省;localdb=本地库解密副本直读;"
                f"sns=朋友圈动态/互动通知),当前为 {channel!r}",
                error_type="invalid_engine_options",
            )
        result: dict[str, Any] = {"channel": channel}
        if channel == "sns":
            for chat_key in ("chat", "sides", "count"):
                if chat_key in options:
                    raise FetchError(
                        f"engine_options.wechat_local.{chat_key} 是会话通道"
                        "(pixel/localdb)的配置,朋友圈无会话概念,sns 通道不"
                        "消费(全量收朋友圈动态;窗口用 since_days)",
                        error_type="invalid_engine_options",
                    )
            feed_kind = options.get("feed_kind", DEFAULT_SNS_KIND)
            if (
                isinstance(feed_kind, bool)
                or feed_kind not in SNS_KINDS
            ):
                raise FetchError(
                    f"engine_options.wechat_local.feed_kind 应为 "
                    f"{'/'.join(SNS_KINDS)}(feed=朋友圈动态缺省;"
                    "notices=互动通知赞/评),当前为 "
                    f"{feed_kind!r}",
                    error_type="invalid_engine_options",
                )
            since_days = options.get("since_days", DEFAULT_SINCE_DAYS)
            if (
                isinstance(since_days, bool)
                or not isinstance(since_days, int)
                or not 1 <= since_days <= MAX_SINCE_DAYS
            ):
                raise FetchError(
                    f"engine_options.wechat_local.since_days 应为 1-{MAX_SINCE_DAYS}"
                    " 整数(sns 首拉/无水位历史窗口天数,缺省 "
                    f"{DEFAULT_SINCE_DAYS};有水位后自动按增量开窗),当前为 "
                    f"{since_days!r}",
                    error_type="invalid_engine_options",
                )
            result["feed_kind"] = feed_kind
            result["since_days"] = since_days
            default_timeout = DEFAULT_LOCALDB_TIMEOUT_SECONDS
            timeout = options.get("read_timeout_seconds", default_timeout)
            if (
                isinstance(timeout, bool)
                or not isinstance(timeout, (int, float))
                or timeout <= 0
            ):
                raise FetchError(
                    "engine_options.wechat_local.read_timeout_seconds 应为正数秒"
                    f"(单次桥读上界;sns 缺省 {DEFAULT_LOCALDB_TIMEOUT_SECONDS:.0f}"
                    " 副本首建),当前为 "
                    f"{timeout!r}",
                    error_type="invalid_engine_options",
                )
            result["read_timeout_seconds"] = float(timeout)
            return result
        chat = options.get("chat")
        if isinstance(chat, bool) or not isinstance(chat, str) or not chat.strip():
            raise FetchError(
                "engine_options.wechat_local.chat 应为会话名字符串(pixel 与"
                "像素链可见标题匹配;localdb 理想形态是会话 id wxid_xxx/"
                "xxx@chatroom,声明显示名则按 sessions 名解析),当前为 "
                f"{chat!r}",
                error_type="invalid_engine_options",
            )
        if "feed_kind" in options:
            raise FetchError(
                "engine_options.wechat_local.feed_kind 是 sns 通道(朋友圈)的"
                "模式配置,会话通道(pixel/localdb)不消费;朋友圈源请声明"
                " channel: sns",
                error_type="invalid_engine_options",
            )
        raw_sides = options.get("sides", list(DEFAULT_SIDES))
        if (
            not isinstance(raw_sides, list)
            or not raw_sides
            or any(
                isinstance(side, bool)
                or not isinstance(side, str)
                or side not in SIDES
                for side in raw_sides
            )
        ):
            raise FetchError(
                f"engine_options.wechat_local.sides 应为 {'/'.join(SIDES)} 的"
                "非空列表(缺省 [left]=只采对方消息;right=自己/center=系统行"
                "显式声明才收;localdb 由 sender 派生 me→right 其余→left),"
                f"当前为 {raw_sides!r}",
                error_type="invalid_engine_options",
            )
        result: dict[str, Any] = {
            "channel": channel,
            "chat": chat.strip(),
            "sides": tuple(raw_sides),
        }
        if channel == "localdb":
            if "count" in options:
                raise FetchError(
                    "engine_options.wechat_local.count 是 pixel 通道的最近 K 条"
                    "窗口帽,localdb 通道不消费(窗口=--since 水位增量,条数"
                    "上限走桥配置 limits.messages);如需深历史用 since_days",
                    error_type="invalid_engine_options",
                )
            since_days = options.get("since_days", DEFAULT_SINCE_DAYS)
            if (
                isinstance(since_days, bool)
                or not isinstance(since_days, int)
                or not 1 <= since_days <= MAX_SINCE_DAYS
            ):
                raise FetchError(
                    f"engine_options.wechat_local.since_days 应为 1-{MAX_SINCE_DAYS}"
                    " 整数(localdb 首拉/无水位历史窗口天数,缺省 "
                    f"{DEFAULT_SINCE_DAYS};有水位后自动按增量开窗),当前为 "
                    f"{since_days!r}",
                    error_type="invalid_engine_options",
                )
            result["since_days"] = since_days
            default_timeout = DEFAULT_LOCALDB_TIMEOUT_SECONDS
        else:
            if "since_days" in options:
                raise FetchError(
                    "engine_options.wechat_local.since_days 是 localdb 通道的"
                    "历史窗口配置,pixel 通道不消费(pixel 是最近 K 条窗口帽"
                    "count);深历史请切 channel: localdb",
                    error_type="invalid_engine_options",
                )
            count = options.get("count", DEFAULT_COUNT)
            if (
                isinstance(count, bool)
                or not isinstance(count, int)
                or not 1 <= count <= MAX_COUNT
            ):
                raise FetchError(
                    f"engine_options.wechat_local.count 应为 1-{MAX_COUNT} 整数"
                    "(单轮最近 K 条窗口帽;深历史是微信客户端滚动加载面),"
                    f"当前为 {count!r}",
                    error_type="invalid_engine_options",
                )
            result["count"] = count
            default_timeout = DEFAULT_READ_TIMEOUT_SECONDS
        timeout = options.get("read_timeout_seconds", default_timeout)
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise FetchError(
                "engine_options.wechat_local.read_timeout_seconds 应为正数秒"
                f"(单次桥读上界;{CHANNELS[0]} 缺省 {DEFAULT_READ_TIMEOUT_SECONDS:.0f}"
                f" 截图+OCR / {CHANNELS[1]} 缺省 {DEFAULT_LOCALDB_TIMEOUT_SECONDS:.0f}"
                " 副本首建),当前为 "
                f"{timeout!r}",
                error_type="invalid_engine_options",
            )
        result["read_timeout_seconds"] = float(timeout)
        return result

    # ------------------------------------------------------- url contract

    def _parse_source_url(self) -> None:
        """源 URL 契约校验(零 I/O):``https://weixin.qq.com`` 锚形态."""
        from urllib.parse import urlsplit

        parsed = urlsplit(self.source.url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host != WEB_HOST or parsed.path not in ("", "/"):
            raise FetchError(
                f"wechat_local 引擎源 url 应为 https://{WEB_HOST} 锚形态"
                "(路径留空;会话配置在 engine_options.wechat_local.chat),"
                f"当前为 {self.source.url!r}",
                error_type="invalid_wechat_local_source_url",
            )

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        self._parse_source_url()
        options = self._options()
        if options["channel"] == "sns":
            return await self._fetch_sns(options)
        if options["channel"] == "localdb":
            return await self._fetch_localdb(options)
        return await self._fetch_pixel(options)

    async def _run_bridge(
        self, argv: list[str], timeout: float, *, label: str
    ) -> tuple[int, str]:
        """桥子进程往返(to_thread 不堵事件循环;同轮多源并发不被卡)."""
        try:
            exit_code, stdout, _stderr = await asyncio.to_thread(
                run_bridge_command_sync,
                argv,
                "",
                timeout,
            )
        except LocalBridgeTimeoutError as exc:
            raise FetchError(
                f"{label}超时:{exc}(上限 {timeout:.0f} 秒;"
                "多为暂时现象,稍后重试即可)",
                error_type="bridge_timeout",
            ) from exc
        return exit_code, stdout

    async def _fetch_pixel(self, options: dict[str, Any]) -> list[dict]:
        """pixel 通道:``messages read`` 截窗 OCR(原路径,行为不变)."""
        resolved = bin_path(None)
        if not (resolved.is_file() and os.access(resolved, os.X_OK)):
            raise FetchError(
                "微信本机桥组件 bin 不存在或不可执行: "
                f"{resolved}。修复指引:到设置安装 wechat-bridge 组件"
                "(前置 brew install sqlcipher)",
                error_type="component_missing",
            )
        argv = [
            str(resolved),
            "messages",
            "read",
            options["chat"],
            "-k",
            str(options["count"]),
            "--json",
        ]
        # 桥是同步子进程(subprocess.run);包 to_thread 不堵事件循环 ——
        # 同轮多源并发时其余源/阶段不被一次截图+OCR 卡住。
        exit_code, stdout = await self._run_bridge(
            argv, options["read_timeout_seconds"], label="读取微信消息"
        )
        payload = self._check_bridge_result(exit_code, stdout)
        return self._items_from_payload(options, payload)

    async def _fetch_localdb(self, options: dict[str, Any]) -> list[dict]:
        """localdb 通道:``localdb query`` 解密副本只读查询(零截窗零 AX).

        增量窗口 = 源级水位(首拉/无水位用 since_days);声明显示名时按
        sessions 名解析会话 id 至多二查;key_unavailable = 结构化 skip
        (密钥缺位合法预期态,不推进水位)。
        """
        resolved = bin_path(None)
        if not (resolved.is_file() and os.access(resolved, os.X_OK)):
            raise FetchError(
                "微信本机桥组件 bin 不存在或不可执行: "
                f"{resolved}。修复指引:到设置安装 wechat-bridge 组件"
                "(前置 brew install sqlcipher)",
                error_type="component_missing",
            )
        chat = options["chat"]
        days = self._localdb_since_days(options)
        payload = await self._run_localdb_query(
            str(resolved), chat, days, options["read_timeout_seconds"]
        )
        if payload is None:  # key_unavailable:结构化 skip,零条目不算失败
            return []
        items, declared_chat_live = self._localdb_items_from_payload(options, payload)
        if not items and not declared_chat_live:
            # 声明值没当会话 id 命中(零消息且 contact 解析不出展示名):
            # 尝试按 sessions 会话名精确解析 → 命中则按会话 id 再查一次。
            session_id = self._resolve_session_id(chat, payload)
            if session_id is not None:
                logger.info(
                    "wechat_local localdb 声明 chat 按会话名解析出会话 id 再查"
                    " source=%s(形状级:二查,不记内容)",
                    self.source.name,
                )
                payload = await self._run_localdb_query(
                    str(resolved), session_id, days, options["read_timeout_seconds"]
                )
                if payload is None:  # 二查撞 key_unavailable:同 skip 语义
                    return []
                items, _ = self._localdb_items_from_payload(options, payload)
        self._advance_watermark()
        return items

    async def _run_localdb_query(
        self, bridge_bin: str, chat_id: str, days: int, timeout: float
    ) -> dict[str, Any] | None:
        """一次 ``localdb query`` 往返;key_unavailable → None(skip 语义).

        其余失败族(db_not_found/decrypt_failed/timeout/不可解析)与 pixel
        同纪律结构化冒泡 —— 密钥缺位是 D4 合法预期态(一键脚本待主人
        sudo),唯独它不算 failure 免告警。
        """
        argv = [bridge_bin, "localdb", "query", chat_id, "--since", f"{days}d", "--json"]
        exit_code, stdout = await self._run_bridge(
            argv, timeout, label="查询微信本地库"
        )
        payload = self._check_bridge_result(
            exit_code, stdout, skip_codes=frozenset({"key_unavailable"})
        )
        if payload is None:
            # _check_bridge_result 对 skip 码族返回 None;localdb 面 = 密钥缺位
            self.last_skip_reason = "key_unavailable"
            logger.info(
                "wechat_local localdb 显式空态:解密密钥未就绪(key_unavailable),"
                "本轮跳过不算失败 source=%s。指引:跑仓库 %s(主人 sudo 一键"
                "内存密钥扫描,命中自动落 keys.json,下一轮即通)",
                self.source.name,
                KEYSCAN_SCRIPT,
            )
        return payload

    # ------------------------------------------------------ localdb helpers

    async def _fetch_sns(self, options: dict[str, Any]) -> list[dict]:
        """sns 通道:``localdb sns feed|notices`` 朋友圈域只读(零截窗零 AX).

        增量窗口 = 源级水位(同 localdb 机制);key_unavailable = 结构化
        skip;**可疑空水位防御**(grill 决议):feed 零条目且桥报
        parse_errors>0(XML 坏行吞噬整窗的形状)= 不推进水位——微信 XML
        格式变化时中间窗口不丢,修好后的下一轮重开同窗补齐。
        """
        resolved = bin_path(None)
        if not (resolved.is_file() and os.access(resolved, os.X_OK)):
            raise FetchError(
                "微信本机桥组件 bin 不存在或不可执行: "
                f"{resolved}。修复指引:到设置安装 wechat-bridge 组件"
                "(前置 brew install sqlcipher)",
                error_type="component_missing",
            )
        mode = options["feed_kind"]
        days = self._localdb_since_days(options)
        argv = [
            str(resolved), "localdb", "sns", mode,
            "--since", f"{days}d", "--json",
        ]
        exit_code, stdout = await self._run_bridge(
            argv, options["read_timeout_seconds"], label="查询朋友圈"
        )
        payload = self._check_bridge_result(
            exit_code, stdout, skip_codes=frozenset({"key_unavailable"})
        )
        if payload is None:
            self.last_skip_reason = "key_unavailable"
            logger.info(
                "wechat_local sns 显式空态:解密密钥未就绪(key_unavailable),"
                "本轮跳过不算失败 source=%s。指引:跑仓库 %s(主人 sudo 一键"
                "内存密钥扫描,命中自动落 keys.json,下一轮即通)",
                self.source.name,
                KEYSCAN_SCRIPT,
            )
            return []
        items = self._sns_items_from_payload(payload)
        sns = payload.get("sns") if isinstance(payload.get("sns"), dict) else {}
        suspicious_empty = (
            not items
            and mode == "feed"
            and isinstance(sns, dict)
            and int(sns.get("parse_errors") or 0) > 0
        )
        if suspicious_empty:
            logger.warning(
                "wechat_local sns feed 可疑空窗:零条目且 parse_errors=%s"
                "(XML 坏行形状),水位不推进 source=%s(下轮重开同窗)",
                sns.get("parse_errors"),
                self.source.name,
            )
            return items
        self._advance_watermark()
        return items

    def _sns_items_from_payload(self, payload: dict[str, Any]) -> list[dict]:
        """sns 成功载荷 → 条目(feed 强 id 锚 / notices 主键锚;§3.2).

        标题回退链(design grill 决议:media type 数字语义不臆造,视频型
        判别不做):text → [图片×N] → [朋友圈动态]。通知词面中性不假设
        归属(is_relative_me 语义未实证)。``kind``/``username``/``ts`` 等
        留 raw 面(metadata;feed v1 不投影)。
        """
        sns = payload.get("sns")
        if not isinstance(sns, dict):
            raise FetchError(
                "wechat-bridge 组件返回的结果缺 sns 节;请重装或升级该组件"
                "(需要 0.6.0+)",
                error_type="bridge_error",
            )
        mode = sns.get("mode")
        rows = sns.get("feed") if mode == "feed" else sns.get("notices")
        if not isinstance(rows, list):
            raise FetchError(
                "wechat-bridge 组件返回的结果缺 feed/notices 列表;"
                "请重装或升级该组件(需要 0.6.0+)",
                error_type="bridge_error",
            )
        items: list[dict] = []
        for row in rows:
            if not isinstance(row, dict):
                continue
            if mode == "feed":
                item = self._sns_feed_row_to_item(row)
            else:
                item = self._sns_notice_row_to_item(row)
            if item is not None:
                items.append(item)
        logger.info(
            "wechat_local sns 窗口取得 source=%s mode=%s rows=%s items=%s"
            " parse_errors=%s(形状级,不记内容)",
            self.source.name,
            mode,
            len(rows),
            len(items),
            sns.get("parse_errors"),
        )
        return items

    def _sns_feed_row_to_item(self, row: dict[str, Any]) -> dict[str, Any] | None:
        """一条朋友圈动态 → 管线条目(#wxsns-<id> 强锚).

        标题回退链(grill 深化批,type 语义已实证:2=图/6=视频,真库
        videoDuration 交叉验证——「视频显示成图片」的词面瑕疵据此修复):
        text → 媒体词面([图片×N]/[视频×K]/混合)→ [朋友圈动态]。
        """
        entry_id = row.get("id")
        if not isinstance(entry_id, str) or not entry_id:
            return None  # 桥侧已过滤,防御形状
        text = row.get("text")
        text = text if isinstance(text, str) and text.strip() else ""
        media_types = row.get("media_types")
        media_types = (
            [str(t) for t in media_types]
            if isinstance(media_types, list)
            else []
        )
        video_count = sum(1 for t in media_types if t == "6")
        image_count = len(media_types) - video_count
        media_count = row.get("media_count")
        media_count = media_count if isinstance(media_count, int) else 0
        if text:
            display = text
        elif video_count and image_count:
            display = f"[图片×{image_count}·视频×{video_count}]"
        elif video_count:
            display = f"[视频×{video_count}]"
        elif image_count:
            display = f"[图片×{image_count}]"
        else:
            display = "[朋友圈动态]"
        title = display.splitlines()[0][:TITLE_MAX_CHARS]
        return {
            "url": sns_anchor(entry_id),
            "title": title,
            "content": display,
            "sender": row.get("nickname") or row.get("username"),
            "side": "left",  # 朋友圈 feed 全收(v1 不筛自己;design §3.1)
            "ts": row.get("create_time"),
            "kind": "sns",
            "sns_kind": "feed",
            "username": row.get("username"),
            "nickname": row.get("nickname"),
            "media_count": media_count,
            "ref_nickname": row.get("ref_nickname"),
        }

    def _sns_notice_row_to_item(self, row: dict[str, Any]) -> dict[str, Any] | None:
        """一条互动通知 → 管线条目(#wxsnsn-<local_id> 主键锚;中性词面)."""
        local_id = row.get("local_id")
        if local_id is None:
            return None
        who = row.get("from_nickname") or row.get("from_username") or "微信好友"
        content = row.get("content")
        content = content if isinstance(content, str) and content.strip() else ""
        if row.get("type") == "comment" and content:
            title = f"{who} 评论了朋友圈动态:{content[:40]}"
        elif row.get("type") == "comment":
            title = f"{who} 评论了朋友圈动态"
        else:  # like / 未知型:赞词面兜底(未知型如实入 title,不臆造分类)
            kind_label = "赞了" if row.get("type") == "like" else f"互动({row.get('type')})"
            title = f"{who} {kind_label}朋友圈动态"
        if len(title) > TITLE_MAX_CHARS:
            title = title[:TITLE_MAX_CHARS]
        return {
            "url": sns_notice_anchor(local_id),
            "title": title,
            "content": content or title,
            "sender": who,
            "side": "left",
            "ts": row.get("create_time"),
            "kind": "sns",
            "sns_kind": "notices",
            "notice_type": row.get("type"),
            "is_relative_me": row.get("is_relative_me"),
            "from_username": row.get("from_username"),
            "feed_id": row.get("feed_id"),
        }

    def _localdb_since_days(self, options: dict[str, Any]) -> int:
        """水位 → ``--since`` 天数(天粒度向上取整;无水位 = since_days 缺省)."""
        last_pull = self._read_watermark()
        if last_pull is None:
            return options["since_days"]
        elapsed_days = (time.time() - last_pull) / 86400.0
        return max(1, math.ceil(elapsed_days))

    def _watermark_key(self) -> str:
        return watermark_key(self.source.name)

    def _read_watermark(self) -> float | None:
        """读源级水位(上次成功拉取 epoch 秒);无 store/无水位/坏值 = None.

        水位落 store ``change_baseline`` 表(通用 kv 面,键 = 引擎自有
        ``wechat-local://watermark/`` 命名空间);试抓/干跑无 store 时如实
        降级缺省窗口(重叠重读,dedup 消化)。
        """
        store = self.context.store
        if store is None:
            return None
        baseline = store.get_baseline(self._watermark_key())
        if baseline is None or not baseline.etag:
            return None
        try:
            return float(baseline.etag)
        except ValueError:
            logger.warning(
                "wechat_local localdb 水位值不可解析,按无水位处理"
                " source=%s(形状级:etag 非数值)",
                self.source.name,
            )
            return None

    def _advance_watermark(self) -> None:
        """成功拉取后推进水位(仅成功面调用;skip/失败不推进,下轮重开同窗)."""
        store = self.context.store
        if store is None:
            return
        store.set_baseline(
            self._watermark_key(),
            etag=str(int(time.time())),
            last_changed=datetime.now(timezone.utc),
        )

    def _resolve_session_id(self, declared: str, payload: dict[str, Any]) -> str | None:
        """sessions 列表按会话名精确匹配 → 会话 id(声明值本身就是 id 时 None).

        ``sessions`` 是桥 best-effort 前 20 行(会话域);不在列表 = 解析
        不到,如实返回 None(零产出不猜 —— 会话可能只是不在前 20)。
        """
        sessions = payload.get("sessions")
        if not isinstance(sessions, list):
            return None
        for session in sessions:
            if not isinstance(session, dict):
                continue
            session_id = session.get("id")
            if (
                isinstance(session_id, str)
                and session_id
                and session_id != declared
                and session.get("name") == declared
            ):
                return session_id
        return None

    def _localdb_items_from_payload(
        self, options: dict[str, Any], payload: dict[str, Any]
    ) -> tuple[list[dict], bool]:
        """localdb 成功载荷 → (条目列表, 声明 chat 是否当会话 id 命中).

        命中判据 = 有消息,或 contact 域解析出展示名(``display_name`` 非
        None)—— 两者都空说明声明值可能不是会话 id(显示名形态),交给
        上层做 sessions 名解析二查。sender 派生 side:"me" → right,
        其余(会话 id)→ left;非 text 行/侧过滤/空白文本与 pixel 同律。
        """
        messages = payload.get("messages")
        if not isinstance(messages, list):
            raise FetchError(
                "wechat-bridge 组件返回的结果缺 messages 列表;"
                "请重装或升级该组件",
                error_type="bridge_error",
            )
        chat = options["chat"]
        items: list[dict] = []
        skipped_side = 0
        skipped_type = 0
        for message in messages:
            if not isinstance(message, dict):
                continue
            if message.get("type") != "text":
                skipped_type += 1  # v1 全文本;媒体行是类型占位(media_placeholder)
                continue
            sender = message.get("sender")
            sender_str = sender if isinstance(sender, str) else ""
            side = "right" if sender_str == "me" else "left"
            if side not in options["sides"]:
                skipped_side += 1
                continue
            text = message.get("text")
            text = text if isinstance(text, str) else ""
            if not text.strip():
                continue
            ts = message.get("ts")
            ts = ts if isinstance(ts, int) else None
            item = self._localdb_message_to_item(chat, sender_str, side, ts, text)
            if item is not None:
                items.append(item)
        declared_chat_live = bool(items) or payload.get("display_name") is not None
        if not items:
            logger.info(
                "wechat_local localdb 窗口零产出 source=%s chat=%s messages=%s"
                " sides=%s 过滤跳过(侧=%s 非 text=%s)(安静会话或全被侧过滤)",
                self.source.name,
                chat,
                len(messages),
                list(options["sides"]),
                skipped_side,
                skipped_type,
            )
        else:
            logger.info(
                "wechat_local localdb 窗口取得 source=%s chat=%s messages=%s"
                " items=%s sides=%s 过滤跳过(侧=%s 非 text=%s)",
                self.source.name,
                chat,
                len(messages),
                len(items),
                list(options["sides"]),
                skipped_side,
                skipped_type,
            )
        return items, declared_chat_live

    def _localdb_message_to_item(
        self, chat: str, sender: str, side: str, ts: int | None, text: str
    ) -> dict[str, Any] | None:
        """一条 localdb 消息 → 管线条目(#wx- 内容锚,ts=epoch 入盐;如实弱幂等).

        ``sender``/``side``/``ts``(epoch 秒)/``chat`` 留 raw 面(metadata;
        feed v1 不投影)。localdb 文本原样(无 OCR 噪声),重读恒同锚。
        """
        title = text.splitlines()[0][:TITLE_MAX_CHARS]
        return {
            "url": anchor_url(chat, str(ts) if ts is not None else None, side, text),
            "title": title,
            "content": text,
            "sender": sender or None,
            "side": side,
            "ts": ts,
            "chat": chat,
        }

    # ------------------------------------------------------- pixel payload

    def _check_bridge_result(
        self, exit_code: int, stdout: str, *, skip_codes: frozenset[str] = frozenset()
    ) -> dict[str, Any] | None:
        """(exit_code, stdout) → 成功载荷;失败映射结构化 FetchError.

        桥 stdout 恒单 JSON:成功 = 命令契约载荷;失败 = ``{"error": {code,
        message, fix_hint?}}``。具名错误族码名**原样**作 error_type
        (wechat_not_running/screen_recording_denied/window_closed/…);
        桥内码 ``timeout`` 归 ``bridge_timeout``(与 MYIA 侧 runner 超时同一
        词面,doctor/UI 单一词汇);无码名/不可解析 = ``bridge_error``。
        码名命中 ``skip_codes`` → 返回 None(调用方置结构化空态不算失败
        —— localdb 面的 key_unavailable 判例;pixel 面不传,行为不变)。
        """
        payload = parse_bridge_payload(stdout)
        if exit_code == 0 and isinstance(payload, dict) and not payload.get("error"):
            return payload
        error = payload.get("error") if isinstance(payload, dict) else None
        if isinstance(error, dict) and error.get("code"):
            code = str(error["code"])
            if code in skip_codes:
                return None
            error_type = "bridge_timeout" if code == "timeout" else code
            message = str(error.get("message") or f"桥 exit={exit_code}")
            fix_hint = error.get("fix_hint")
            suffix = f"。修复指引:{fix_hint}" if fix_hint else ""
            raise FetchError(
                f"wechat_local 桥读失败({code}):{message}{suffix}",
                error_type=error_type,
            )
        raise FetchError(
            f"wechat-bridge 组件返回了无法识别的结果(exit={exit_code});"
            "请重装或升级该组件",
            error_type="bridge_error",
        )

    def _items_from_payload(
        self, options: dict[str, Any], payload: dict[str, Any]
    ) -> list[dict]:
        """pixel 成功载荷 → 条目(``chat.match`` 三态核对在先,绝不张冠李戴)."""
        chat_info = payload.get("chat")
        match = chat_info.get("match") if isinstance(chat_info, dict) else None
        chat = options["chat"]
        if match is False:
            visible = ""
            if isinstance(chat_info, dict):
                visible = str(chat_info.get("visible_title") or "")
            self.last_skip_reason = "chat_not_open"
            logger.info(
                "wechat_local 显式空态:当前打开会话『%s』与声明『%s』不匹配,"
                "本轮载荷弃用不张冠李戴 source=%s(对齐 = 在微信里打开该会话)",
                visible,
                chat,
                self.source.name,
            )
            return []
        if match is None:
            self.last_skip_reason = "chat_title_unreadable"
            logger.info(
                "wechat_local 显式空态:可见标题不可读,无法核对会话归属,"
                "本轮载荷弃用 source=%s chat=%s(主窗标题带被遮挡/截窗异常)",
                self.source.name,
                chat,
            )
            return []
        messages = payload.get("messages")
        if not isinstance(messages, list):
            raise FetchError(
                "wechat-bridge 组件返回的结果缺 messages 列表;"
                "请重装或升级该组件",
                error_type="bridge_error",
            )
        items: list[dict] = []
        skipped_side = 0
        skipped_type = 0
        for message in messages:
            if not isinstance(message, dict):
                continue
            if message.get("type") != "text":
                skipped_type += 1  # 像素链 v1 全文本;防御非 text 形态
                continue
            side = str(message.get("side") or "")
            if side not in options["sides"]:
                skipped_side += 1
                continue
            item = self._message_to_item(chat, message)
            if item is not None:
                items.append(item)
        if not items:
            logger.info(
                "wechat_local 窗口零产出 source=%s chat=%s messages=%s"
                " sides=%s 过滤跳过(侧=%s 非 text=%s)(安静会话或全被侧过滤)",
                self.source.name,
                chat,
                len(messages),
                list(options["sides"]),
                skipped_side,
                skipped_type,
            )
            return []
        logger.info(
            "wechat_local 窗口取得 source=%s chat=%s messages=%s items=%s"
            " sides=%s 过滤跳过(侧=%s 非 text=%s)",
            self.source.name,
            chat,
            len(messages),
            len(items),
            list(options["sides"]),
            skipped_side,
            skipped_type,
        )
        return items

    def _message_to_item(
        self, chat: str, message: dict[str, Any]
    ) -> dict[str, Any] | None:
        """一条消息 → 管线条目(#wx- 内容哈希锚;Item.from_extracted 契约).

        空白文本跳过(OCR 噪声行);``sender``/``side``/``ts``/``conf``/
        ``chat`` 留 raw 面(metadata;feed v1 不投影)。
        """
        text = message.get("text")
        text = text if isinstance(text, str) else ""
        if not text.strip():
            return None
        ts = message.get("ts")
        ts = ts.strip() if isinstance(ts, str) and ts.strip() else None
        side = str(message.get("side") or "")
        title = text.splitlines()[0][:TITLE_MAX_CHARS]
        return {
            "url": anchor_url(chat, ts, side, text),
            "title": title,
            "content": text,
            "sender": message.get("sender"),
            "side": side,
            "ts": ts,
            "conf": message.get("conf"),
            "chat": chat,
        }

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单轮窗口语义:任何 pagination 配置都结构化拒(urlwatch/tg_web 判例)."""
        if self.source.pagination is not None:
            raise FetchError(
                "wechat_local 引擎是单轮窗口语义(pixel count 即最近 K 条帽,"
                "localdb since 即水位增量窗;深历史是微信客户端滚动加载面),"
                "不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
