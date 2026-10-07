"""TG 网页线 DOM 面 —— 选择器表/JS 注入件/消息映射(10-08-tg-web-line W2).

web.telegram.org 是客户端渲染 SPA(GramJS 前端,``/k/`` 与 ``/a/`` 两版
并存);本模块是网页线对 DOM 的**唯一**知识面:选择器常量、注入 JS
(MutationObserver / 消息抽取)、DOM 消息 → Bot API update 同形映射。
引擎(批量档)与常驻 Watcher 共用同一份(``web_line`` 登录器只共用登录
标志选择器)。

诚实披露的落点(PRD「DOM 改版跟修」):选择器表是**标定件** —— 前端
改版即失配;失配不装死:全表不中 → 结构化告警 ``tg_web_dom_stale``
(哨兵在 :mod:`myssia.telegram.web_host`),源级失败带「跟修指引」
(重新标定 = 无头开页 dump 候选选择器)。选择器表带版本注记,改版跟修
只动本模块。

映射口径(``dom_message_to_update`` → :func:`engines.telegram.
updates_to_items` 全语义复用):

- ``message_id`` = ``data-mid``(Web K/A 两版的消息 DOM 节点均带;数字
  形态,与 Bot API 消息 id 同命名空间 —— 同群同锚,网页线与 bot 线消息
  不重复进库);
- ``text`` = 消息文本节点(纯文本拼接,媒体 caption 同面);
- ``from`` = 发送者名(显示名,@username 网页 DOM 拿不到就不给 —— 观测
  键 best-effort,不为此加请求);
- ``date`` = ``data-timestamp``(epoch 秒;缺 = None,锚与聚合不依赖);
- ``media_group_id``:网页 DOM 无相册分组键,**不虚构** —— 相册成员各自
  出条,纯媒体无文本成员照 bot 线「零可筛面」口径跳过,残余重复面由
  ``#tg-`` 锚去重兜底(如实注记);
- ``chat.id`` 由调用方注入(Watcher/引擎按源配置的 chat 标识);
- 纯媒体消息(有媒体标记无文本)→ 不产 update(与 bot 线贴纸/纯图
  口径一致)。
"""

from __future__ import annotations

import logging
from typing import Any, Mapping

logger = logging.getLogger(__name__)

#: 选择器表标定版本(改版跟修只动本模块 + 升本注记)。
SELECTOR_REVISION = "2026-10-08.v1"

#: 登录成功标志(左栏会话列表;命中任一 = 已登录)。Web K:聊天列表容器
#: ``.chatlist-container``;Web A:``.chat-list`` 一族。多候选兜底。
CHAT_LIST_SELECTORS: tuple[str, ...] = (
    ".chatlist-container",  # Web K
    ".chat-list",  # Web A
    "ul.chatlist",
)

#: 登出态标志(登录表单在场)。Web K 手机号输入 ``.login-form`` 一族;
#: Web A ``input[name='phone']``(部分版本 ``#phone-number``)。
LOGGED_OUT_SELECTORS: tuple[str, ...] = (
    ".login-form",  # Web K 登录卡片
    "input[name='phone']",  # Web A 手机号输入
    "#phone-number",
)

#: 聊天打开态标志(消息容器在场;Watcher 判「群页开成功」用)。
CHAT_OPEN_SELECTORS: tuple[str, ...] = (
    ".bubbles",  # Web K 消息列
    ".messages-container",  # Web A 消息列
)

#: 消息节点选择器(批量档窗口读取;新节点判定同面)。Web K 气泡带
#: ``data-mid``;Web A 同。只认带 ``data-mid`` 的节点(锚面必需)。
MESSAGE_SELECTORS: tuple[str, ...] = (
    ".bubble[data-mid]",  # Web K
    ".message[data-mid]",  # Web A
)

#: 消息节点内文本子选择器(候选序 = 优先级;首个非空命中)。
MESSAGE_TEXT_SELECTORS: tuple[str, ...] = (
    ".message",
    ".translatable-message",
    ".text-content",
)

#: 消息发送者显示名子选择器(best-effort 观测键)。
MESSAGE_SENDER_SELECTORS: tuple[str, ...] = (
    ".peer-title",
    ".sender-title",
    ".message-title-name",
)

#: 消息时间属性(``data-timestamp`` = epoch 秒,两版同)。
MESSAGE_TIMESTAMP_ATTR = "data-timestamp"

#: 媒体在巢标记(命中 = 该消息带媒体;文本缺失 + 媒体在 = 纯媒体跳过)。
MESSAGE_MEDIA_SELECTORS: tuple[str, ...] = (
    ".document-wrapper, .media-container, .photo, .video, .sticker",
)

#: 单页消息读取帽(批量档 lookback 窗;DOM 现存即读,不滚动翻历史 ——
#: 批量档是「读当前窗口」,深历史是 TG 客户端滚动加载面,不属本线)。
MAX_DOM_MESSAGES = 100

__all__ = [
    "CHAT_LIST_SELECTORS",
    "CHAT_OPEN_SELECTORS",
    "LOGGED_OUT_SELECTORS",
    "MAX_DOM_MESSAGES",
    "MESSAGE_MEDIA_SELECTORS",
    "MESSAGE_SELECTORS",
    "MESSAGE_SENDER_SELECTORS",
    "MESSAGE_TEXT_SELECTORS",
    "MESSAGE_TIMESTAMP_ATTR",
    "SELECTOR_REVISION",
    "chat_url",
    "collect_messages_js",
    "collect_window_updates",
    "combined_selectors",
    "dom_message_to_update",
    "drain_observer_js",
    "extract_message_js",
    "install_observer_js",
    "open_chat_js",
]


def combined_selectors(chat_list: str, logged_out: str) -> dict[str, list[str]]:
    """登录轮询页用的选择器载荷(evaluate 参数面).

    逗号联合串按 CSS 组合拆回列表 —— 注入侧逐候选探测,命中即返回。
    """
    return {
        "chat_list": [s.strip() for s in chat_list.split(",") if s.strip()],
        "logged_out": [s.strip() for s in logged_out.split(",") if s.strip()],
    }


def chat_url(chat: str) -> str:
    """群定位 URL(v1 口径):统一开 ``/k/`` 主页,群命中交给搜索交互
    (:func:`open_chat_js` 的注入件完成 —— 搜索框输入 + 点首条结果)。

    URL 只开应用;数字 id(``-100…``)与用户名同走此面。深链形态
    (``#?tgAddr=`` 一族)稳定性未标定,升级只动本函数。
    """
    return "https://web.telegram.org/k/"


#: 打开目标群的注入 JS(搜索框 → 输入 → 点首条结果;标定件 v1)。
#: 参数:``{chat, chatOpenSelectors, pollStepMs}``;返回
#: ``{ok, reason, title?}``。
OPEN_CHAT_JS = """
async (args) => {
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const alreadyOpen = args.chatOpenSelectors.find(
        (s) => document.querySelector(s) !== null);
    if (alreadyOpen) return {ok: true, reason: 'already_open'};
    const input = document.querySelector(
        'input.search-input, input[type="search"], .search .input-search');
    if (!input) return {ok: false, reason: 'search_box_missing'};
    input.focus();
    input.value = args.chat;
    input.dispatchEvent(new Event('input', {bubbles: true}));
    await sleep(args.pollStepMs * 10);
    const result = document.querySelector(
        '.chatlist-chat .dialog-title, .search-results .chat-item, ' +
        '.found-chats .chatlist-chat, ul.chatlist a');
    if (!result) return {ok: false, reason: 'chat_not_found'};
    result.click();
    for (let i = 0; i < 40; i += 1) {
        await sleep(args.pollStepMs);
        const opened = args.chatOpenSelectors.find(
            (s) => document.querySelector(s) !== null);
        if (opened) {
            const titleEl = document.querySelector('.topbar .peer-title, .chat-info .peer-title');
            return {ok: true, reason: 'opened',
                    title: titleEl ? titleEl.textContent.trim() : null};
        }
    }
    return {ok: false, reason: 'open_timeout'};
}
"""


def open_chat_js() -> str:
    """群打开注入件(搜索交互;标定 v1,失配走 tg_web_dom_stale 哨兵)."""
    return OPEN_CHAT_JS


#: MutationObserver 安装件(常驻 Watcher 用):新消息节点 → 事件队列。
#: 参数:``{messageSelectors, containerSelectors}``;返回 ``{ok, reason}``。
INSTALL_OBSERVER_JS = """
(args) => {
    if (window.__myssiaTgWebObserver) {
        return {ok: true, reason: 'already_installed'};
    }
    const container = args.containerSelectors
        .map((s) => document.querySelector(s))
        .find((el) => el !== null);
    if (!container) {
        return {ok: false, reason: 'container_missing'};
    }
    window.__myssiaTgWebEvents = window.__myssiaTgWebEvents || [];
    const matches = (node) => args.messageSelectors.some(
        (s) => node.matches(s) || node.querySelector(s) !== null);
    const observer = new MutationObserver((mutations) => {
        for (const m of mutations) {
            for (const node of m.addedNodes) {
                if (node.nodeType !== 1) continue;
                const hits = matches(node)
                    ? (node.matches(args.messageSelectors.join(',')) ? [node]
                        : Array.from(node.querySelectorAll(args.messageSelectors.join(','))))
                    : [];
                for (const hit of hits) {
                    const mid = hit.getAttribute('data-mid');
                    if (!mid) continue;
                    window.__myssiaTgWebEvents.push({mid});
                }
            }
        }
    });
    observer.observe(container, {childList: true, subtree: true});
    window.__myssiaTgWebObserver = observer;
    return {ok: true, reason: 'installed'};
}
"""


def install_observer_js() -> str:
    """Watcher 注入件(page.evaluate 执行;polyfill 经 evaluate 自带)."""
    return INSTALL_OBSERVER_JS


#: 事件队列清空件:取走积压 mid 列表(splice 原子取)。
DRAIN_OBSERVER_JS = """
() => (window.__myssiaTgWebEvents || []).splice(0)
"""


def drain_observer_js() -> str:
    return DRAIN_OBSERVER_JS


#: 单条消息按 mid 抽取件(工厂形态,选择器表烙进 JS 体;mid 走入参)。


def extract_message_js(
    *,
    text_selectors: tuple[str, ...] = MESSAGE_TEXT_SELECTORS,
    sender_selectors: tuple[str, ...] = MESSAGE_SENDER_SELECTORS,
    media_selectors: tuple[str, ...] = MESSAGE_MEDIA_SELECTORS,
) -> str:
    """单条抽取件工厂(选择器表烙进 JS;调用方只传 mid)."""
    body = """
(mid) => {
    const node = document.querySelector(`[data-mid="${mid}"]`);
    if (!node) return null;
    const firstText = (selectors) => {
        for (const s of selectors) {
            for (const el of node.querySelectorAll(s)) {
                const t = el.textContent && el.textContent.trim();
                if (t) return t;
            }
        }
        return null;
    };
    const text = firstText(TEXT_SELECTORS);
    if (!text) return {mid, text: null, sender: firstText(SENDER_SELECTORS),
        timestamp: null, has_media: MEDIA_SELECTORS.some(
            (s) => node.querySelector(s) !== null),
        raw_timestamp: node.getAttribute('data-timestamp')};
    return {
        mid,
        text,
        sender: firstText(SENDER_SELECTORS),
        timestamp: (() => {
            const ts = node.getAttribute('data-timestamp');
            return ts ? Number(ts) : null;
        })(),
        has_media: MEDIA_SELECTORS.some(
            (s) => node.querySelector(s) !== null),
    };
}
"""
    import json

    return (
        f"const TEXT_SELECTORS = {json.dumps(list(text_selectors))};\n"
        f"const SENDER_SELECTORS = {json.dumps(list(sender_selectors))};\n"
        f"const MEDIA_SELECTORS = {json.dumps(list(media_selectors))};\n"
        + body
    )


#: 批量档窗口读取件:现存消息一次抽全(逆序 DOM → 时间序返回)。


def collect_messages_js(limit: int = MAX_DOM_MESSAGES) -> str:
    """窗口读取件工厂(全量 querySelectorAll + 单节点抽取,帽 limit)."""
    import json

    return (
        f"const LIMIT = {int(limit)};\n"
        f"const TEXT_SELECTORS = {json.dumps(list(MESSAGE_TEXT_SELECTORS))};\n"
        f"const SENDER_SELECTORS = {json.dumps(list(MESSAGE_SENDER_SELECTORS))};\n"
        f"const MEDIA_SELECTORS = {json.dumps(list(MESSAGE_MEDIA_SELECTORS))};\n"
        + """
() => {
    const nodes = Array.from(
        document.querySelectorAll('.bubble[data-mid], .message[data-mid]'));
    const out = [];
    for (const node of nodes.slice(-LIMIT)) {
        const firstText = (selectors) => {
            for (const s of selectors) {
                for (const el of node.querySelectorAll(s)) {
                    const t = el.textContent && el.textContent.trim();
                    if (t) return t;
                }
            }
            return null;
        };
        const ts = node.getAttribute('data-timestamp');
        out.push({
            mid: node.getAttribute('data-mid'),
            text: firstText(TEXT_SELECTORS),
            sender: firstText(SENDER_SELECTORS),
            timestamp: ts ? Number(ts) : null,
            has_media: MEDIA_SELECTORS.some(
                (s) => node.querySelector(s) !== null),
        });
    }
    return out;
}
"""
    )


def dom_message_to_update(
    dom: Mapping[str, Any],
    *,
    chat_id: str,
    chat_title: str | None = None,
) -> dict[str, Any] | None:
    """DOM 消息 → Bot API update 同形 dict(消息面复用的唯一接缝).

    产出与 :func:`telegram.telethon_line.telethon_message_to_update` 同构
    (``update_id``/``message`` 嵌套),下游 :func:`engines.telegram.
    updates_to_items` / 过滤管线 / ``#tg-`` 锚零改动复用。纯媒体(无文本)
    → None(零可筛面,bot 线贴纸/纯图同口径);``mid`` 非数字 → None
    (锚面必需,异型防御)。
    """
    text = dom.get("text")
    if not isinstance(text, str) or not text.strip():
        return None
    mid = dom.get("mid")
    try:
        message_id = int(str(mid))
    except (TypeError, ValueError):
        return None
    inner: dict[str, Any] = {
        "message_id": message_id,
        "chat": {"id": chat_id, "title": chat_title},
        "text": text.strip(),
    }
    timestamp = dom.get("timestamp")
    if isinstance(timestamp, (int, float)) and not isinstance(timestamp, bool):
        inner["date"] = float(timestamp)
    sender = dom.get("sender")
    if isinstance(sender, str) and sender.strip():
        # 显示名 → first_name 面(@username 网页 DOM 拿不到,不虚构)。
        inner["from"] = {"first_name": sender.strip()[:64]}
    return {"update_id": message_id, "message": inner}


async def collect_window_updates(
    page: Any,
    *,
    chat_id: str,
    chat_title: str | None = None,
    limit: int = MAX_DOM_MESSAGES,
) -> list[dict[str, Any]]:
    """批量档窗口读取:现存 DOM 消息 → update 同形列表(时间序).

    DOM 失配(全选择器零节点)如实返回空表并留痕 —— 调用方(引擎)按
    ``tg_web_dom_stale`` 结构化失败上报(此函数只管读,哨兵归调用方)。
    """
    raw = await page.evaluate(collect_messages_js(limit))
    updates: list[dict[str, Any]] = []
    if not isinstance(raw, list):
        logger.warning(
            "TG 网页线窗口读取返回非列表(DOM 改版面):%r",
            type(raw).__name__,
        )
        return []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        update = dom_message_to_update(
            entry, chat_id=chat_id, chat_title=chat_title
        )
        if update is not None:
            updates.append(update)
    return updates
