"""微信本机会话引擎(显式 ``engine: wechat_local``;10-12-weixin-feed-channel).

主人令翻案 G3(10-11 档「仅展示不入管线」):微信消息经 wechat-bridge 桥
读回后**入 store/dedup/feed**,与 telegram 同为情报流一等渠道。

通道形态:零 HTTP 零凭据 —— 数据面 = 管线进程内起**本机桥子进程**
(``wechat-bridge messages read <chat> -k N --json``,受管组件,
``myssia.push.weixin_local`` 的 ``bin_path``/``run_bridge_command_sync``/
``parse_bridge_payload`` 同组 helper,与 :mod:`myssia.wechat_local_sidecar`
的 ``_run_bridge`` 同款封装)。**不经 sidecar**:``wechat_local.*`` sidecar
方法保持纯 UI 探针/浏览面,数据面从不绕道桌面 IPC —— 引擎跑在 cron/CLI
进程里,sidecar 可能根本不在场(tg_web 自持 Playwright 传输同构论证)。

源 YAML 形态(design §2.1):

.. code-block:: yaml

    - name: weixin-<会话名>              # 源名全称律(G7 对称纪律)
      engine: wechat_local
      url: "https://weixin.qq.com"       # 锚(schema http(s) 形状要求;引擎零 HTTP)
      empty_ok: true                     # 会话不匹配/零消息 = 合法空
      engine_options:
        wechat_local:
          chat: "<会话名>"               # 与像素链可见标题匹配(桥 messages read 的 id)
          count: 50                      # 最近 K 条,1-200(sidecar 协议上界同值)
          sides: [left]                  # 采集侧:缺省 left=对方;right=自己/center=系统行
          read_timeout_seconds: 60       # 单次桥读上界(截图+OCR)

**像素链硬边界(绝不张冠李戴)**:桥不能点击切换会话(静默铁律,合成点击
被禁),每轮只读微信主窗**当前打开会话**的消息区。源声明 ``chat`` 与桥回报
的 ``chat.match`` 核对:``false`` = 结构化空态 ``chat_not_open``(skip 理由
人话含当前标题 vs 声明,主人可对齐);``null``(标题不可读)= 空态
``chat_title_unreadable``。载荷绝不归到不匹配源名下。

**锚 = 内容哈希,非平台消息 id**(design §2.3,如实弱幂等):像素链的
MessageRow 只有 ts(最近居中时间标记原文,无绝对日期)/side/text,没有
消息 id,锚只能内容铸:

    hash = sha1( chat | ts_marker | side | normalize(text) )[:16]
    url  = wechat-local://chat/<urlencoded(chat)>#wx-<hash>

同窗重读同消息 → 同锚 → dedup 沉默;OCR 修字/置信度波动使文本微变 → 新锚
(重复条目风险,残留靠 feed 读态消化);ts 锚缺失段(时间标记间歇出现)内
同文本同侧消息会并锚。与 ``#tg-<chat>-<mid>`` 的全期强幂等不可比,如实。
``wechat-local://`` 自定义 scheme(非 http(s))是**有意**:私聊消息没有
公开 URL,「打开原文/复制链接」如实缺席(前端 ``isOpenableUrl`` 判 false);
正文内粘贴的 http(s) 链接不受影响。

**错误码表**(桥具名错误族原样透传,与 tg_web 的
session_missing/logged_out/dom_stale 哨兵同纪律,绝不装死):

===========  ==========================  ====================================
error_type   面                          语义
===========  ==========================  ====================================
component_missing  桥组件缺席             bin 不存在/不可执行(fix_hint 指安装)
bridge_timeout     子进程超时              MYIA 侧 kill 兜底;桥内码 ``timeout`` 同归
wechat_not_running / screen_recording_denied /  window_closed / ax_permission_denied /
ax_tree_empty      桥具名族               码名原样作 error_type(§6 码表)
chat_not_open      结构化空态(skip)      当前打开会话与声明不符
chat_title_unreadable  结构化空态(skip)  可见标题不可读,无法核对归属
bridge_error       应答不可解析            stdout 非契约 JSON(重装/升级桥)
===========  ==========================  ====================================

robots 论证(tg_web 同口径):本引擎驱动的是**已授权本机微信客户端**的
像素读回,不对任何站点发请求,robots.txt 语义不适用;``respect_robots``
配置零消费(引擎不走 :meth:`BaseEngine.request` 的 robots/限速面 —— 唯一
的「端点」是本机桥子进程)。

其余边界:单轮窗口语义(pagination 配置即结构化拒,urlwatch/tg_web 判例);
静默铁律全程(桥只读命令,不新增任何写通道/点击/激活);私有数据红线
(消息内容只活在桥 stdout → 管线内存 → store;本模块日志只留形状 —— 计数/
会话名/码名,永不打 text/sender 原文);多源并发成本如实(每源一次桥读 =
一次截图+OCR,同轮多源重复读同一窗口,v1 接受)。

Raises:
    FetchError: engine_options 形状错 / 源 URL 不符契约 / 桥组件缺席 /
        桥超时 / 桥具名错误族 / 应答不可解析 / pagination 配置。
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import os
import re
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

#: 引擎名(schema ``EngineName`` 词表一员;链外源引擎,不进 AUTO_CHAIN)。
ENGINE_NAME = "wechat_local"
LAYER = "LOCAL_BRIDGE"

#: 官方域锚(schema ``SourceConfig.url`` 强制 http(s) 的形状落点;引擎零 HTTP,
#: 请求「端点」是本机桥子进程 —— telegram-web.yaml 锚判例同构)。
WEB_HOST = "weixin.qq.com"

#: 最近 K 条缺省(单轮窗口帽;桥像素链现存消息,不滚动翻历史)。
DEFAULT_COUNT = 50
#: count 域上界(sidecar 协议 ``_LIMIT_MESSAGES_MAX`` 同值,桥内另有配置兜底)。
MAX_COUNT = 200

#: 采集侧词表(桥 MessageRow.side:left=对方 / right=自己 / center=系统行)。
SIDES = ("left", "right", "center")
#: 缺省只采对方消息(left)—— 情报源语义;right/center 显式声明才收。
DEFAULT_SIDES = ("left",)

#: 单次桥读(截图+OCR)超时缺省(秒;= ``DEFAULT_BRIDGE_TIMEOUT_SECONDS``
#: 同值口径,本地单命令上界,超时 kill 兜底)。
DEFAULT_READ_TIMEOUT_SECONDS = 60.0

#: 标题截断(TG 同律:标题 = 首行/全文截断;feishu ``text[:80]`` 判例)。
TITLE_MAX_CHARS = 80

#: 锚前缀与 scheme(design §2.3;#wx- 与 #tg-/#fs- 同族命名)。
ANCHOR_SCHEME = "wechat-local://"
ANCHOR_PREFIX = "#wx-"

#: 内容哈希的文本规整(压空白):OCR 行间空格抖动不另立新锚的缓解面。
_WS_RE = re.compile(r"\s+")

__all__ = [
    "ANCHOR_PREFIX",
    "ANCHOR_SCHEME",
    "DEFAULT_COUNT",
    "DEFAULT_READ_TIMEOUT_SECONDS",
    "DEFAULT_SIDES",
    "ENGINE_NAME",
    "LAYER",
    "MAX_COUNT",
    "SIDES",
    "TITLE_MAX_CHARS",
    "WEB_HOST",
    "WechatLocalEngine",
    "anchor_url",
]


def _normalize_text(text: str) -> str:
    """压空白(空格/换行/制表 → 单空格 + 去首尾):OCR 微抖动的锚稳定面."""
    return _WS_RE.sub(" ", text).strip()


def anchor_url(chat: str, ts: str | None, side: str, text: str) -> str:
    """铸内容哈希锚:``wechat-local://chat/<urlencoded(chat)>#wx-<sha1[:16]>``.

    盐 = ``chat | ts标记 | side | 压空白文本``(design §2.3):ts/side 入盐
    缓解「ts 缺失段内同文本并锚」面;同窗重读同消息 → 同锚(dedup 幂等),
    文本微变(OCR 修字)→ 新锚(如实弱幂等,见模块文档)。
    """
    digest = hashlib.sha1(
        f"{chat}|{ts if ts is not None else ''}|{side}|{_normalize_text(text)}".encode(
            "utf-8"
        )
    ).hexdigest()[:16]
    return f"{ANCHOR_SCHEME}chat/{quote(chat, safe='')}{ANCHOR_PREFIX}{digest}"


class WechatLocalEngine(BaseEngine):
    """微信本机会话窗口源(显式 ``engine: wechat_local``;本机桥直调,零 HTTP).

    items 出口对齐 ``Item.from_extracted`` 契约:url(``#wx-`` 内容哈希锚)/
    title(首行截断)/content(全文);观测键(``sender``/``side``/``ts``/
    ``conf``/``chat``)留 raw 面(metadata,feed v1 不投影 —— 设计定案,
    投影须 bump PROTOCOL_VERSION 三处同步)。
    """

    LAYER = LAYER
    ENGINE_NAME = ENGINE_NAME
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """engine_options.wechat_local 校验与缺省化(错型即结构化拒)."""
        options = self.engine_options()
        chat = options.get("chat")
        if isinstance(chat, bool) or not isinstance(chat, str) or not chat.strip():
            raise FetchError(
                "engine_options.wechat_local.chat 应为会话名字符串(与像素链"
                "可见标题匹配,同桥 messages read 的 id),当前为 "
                f"{chat!r}",
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
                "显式声明才收),当前为 "
                f"{raw_sides!r}",
                error_type="invalid_engine_options",
            )
        timeout = options.get("read_timeout_seconds", DEFAULT_READ_TIMEOUT_SECONDS)
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise FetchError(
                "engine_options.wechat_local.read_timeout_seconds 应为正数秒"
                "(单次桥读=截图+OCR 的上界),当前为 "
                f"{timeout!r}",
                error_type="invalid_engine_options",
            )
        return {
            "chat": chat.strip(),
            "count": count,
            "sides": tuple(raw_sides),
            "read_timeout_seconds": float(timeout),
        }

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
        try:
            exit_code, stdout, _stderr = await asyncio.to_thread(
                run_bridge_command_sync,
                argv,
                "",
                options["read_timeout_seconds"],
            )
        except LocalBridgeTimeoutError as exc:
            raise FetchError(
                f"wechat_local 桥读超时:{exc}(截图+OCR 单命令上界 "
                f"{options['read_timeout_seconds']:.0f}s;瞬态可重试)",
                error_type="bridge_timeout",
            ) from exc
        payload = self._check_bridge_result(exit_code, stdout)
        return self._items_from_payload(options, payload)

    def _check_bridge_result(self, exit_code: int, stdout: str) -> dict[str, Any]:
        """(exit_code, stdout) → 成功载荷;失败映射结构化 FetchError.

        桥 stdout 恒单 JSON:成功 = 命令契约载荷;失败 = ``{"error": {code,
        message, fix_hint?}}``。具名错误族码名**原样**作 error_type
        (wechat_not_running/screen_recording_denied/window_closed/…);
        桥内码 ``timeout`` 归 ``bridge_timeout``(与 MYIA 侧 runner 超时同一
        词面,doctor/UI 单一词汇);无码名/不可解析 = ``bridge_error``。
        """
        payload = parse_bridge_payload(stdout)
        if exit_code == 0 and isinstance(payload, dict) and not payload.get("error"):
            return payload
        error = payload.get("error") if isinstance(payload, dict) else None
        if isinstance(error, dict) and error.get("code"):
            code = str(error["code"])
            error_type = "bridge_timeout" if code == "timeout" else code
            message = str(error.get("message") or f"桥 exit={exit_code}")
            fix_hint = error.get("fix_hint")
            suffix = f"。修复指引:{fix_hint}" if fix_hint else ""
            raise FetchError(
                f"wechat_local 桥读失败({code}):{message}{suffix}",
                error_type=error_type,
            )
        raise FetchError(
            f"wechat_local 桥应答不是契约 JSON(exit={exit_code});"
            "重装或升级 wechat-bridge 组件",
            error_type="bridge_error",
        )

    def _items_from_payload(
        self, options: dict[str, Any], payload: dict[str, Any]
    ) -> list[dict]:
        """成功载荷 → 条目(``chat.match`` 三态核对在先,绝不张冠李戴)."""
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
                "wechat_local 桥应答缺 messages 列表(契约漂移;重装或升级"
                " wechat-bridge 组件)",
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
                "wechat_local 引擎是单轮窗口语义(count 即最近 K 条帽,"
                "深历史是微信客户端滚动加载面),不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
