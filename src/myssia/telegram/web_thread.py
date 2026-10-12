"""TG 网页线评论线程导航面(10-12-tg-comments-reach V1)—— 开/关线程流与状态验证.

频道帖的评论线程是 Web K 的**多 tab 页片**形态:点评论钮 = 新开一个
``.chat.tabs-tab`` 页片,频道页片留在 DOM 非 active(r3_02 取证);本模块
持有线程档的导航知识与真点时序,DOM 抽取面在 :mod:`myssia.telegram.web_dom`
(线程 collect 变体)。引擎批量档(``tg_web comments_max_threads > 0``)按
帖消费:点开 → 读(active tab 作用域)→ 关 → 下一帖;线程页片不关会堆积
(``open_chat_flow`` 只保证频道页片 active,不替线程收尾)。

Web K 线程交互标定(2026-10-12 活页取证,r4-r7 轮;选择器表同
:data:`web_dom.SELECTOR_REVISION` ``2026-10-12.v3``):

- **进线程**:评论钮 = 自定义元素 ``replies-element.replies.replies-footer``
  (频道帖泡内,可见态整块可点);时序铁律 = scrollIntoView 后等 ~2s
  (懒加载挪位窗)→ 取**新鲜** rect 立即 ``page.mouse.click``(第 1 轮按
  4s 前旧坐标点击 0 效果实测在案)→ hash 变化轮询 ≤20s 为开成标志
  (URL hash 无线程参数,变化即线程页片接管)。合成 ``el.click()`` 无效
  (web_line 真点铁律①同源)。
- **返回**:**只有**线程顶栏 ``.btn-icon.sidebar-close-button``(子含
  ``.back-unread-badge``)真点有效(r6 实测:定位 504,40,
  elementFromPoint 验证命中本体);``history.back()``/``page.go_back()``
  不返回(r5_7:hash 不动);侧栏 ``sidebar-back-button`` 点击无效(r5_5)。
- **状态验证(must_fix4,状态基非时间基)**:回频道 = hash 回频道 hash
  **且** 频道 tab 重新 active 双条件;频道页片识别 = 含频道帖
  ``.bubble[data-mid=<帖 mid>]`` 的页片(线程头帖是转发副本,mid 在讨论
  群 2^32 序,不撞频道帖 mid —— 锚面成对判据同源)。关闭败则由引擎侧
  ``open_chat_flow`` 侧栏重开频道兜底(最坏 ≈20+4+20s,独立预算)。
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Awaitable, Callable

logger = logging.getLogger(__name__)

#: 评论钮就绪轮询帽(秒;频道页片懒渲染,footer 可能迟到)。
THREAD_FOOTER_READY_TIMEOUT_SECONDS = 10.0

#: 就绪轮询步长(秒)。
THREAD_FOOTER_POLL_SECONDS = 1.0

#: scrollIntoView 后的懒加载挪位稳态窗(秒;第 1 轮旧坐标点击 0 效果实测)。
THREAD_PREP_SETTLE_SECONDS = 2.0

#: 开成标志(hash 变化)轮询帽(秒)。
THREAD_OPEN_HASH_TIMEOUT_SECONDS = 20.0

#: hash 轮询步长(秒)。
THREAD_HASH_POLL_SECONDS = 1.0

#: 线程打开后回复渲染稳态窗(秒;服务端历史拉取后才出回泡,r5 实测 ~3s)。
THREAD_READ_SETTLE_SECONDS = 2.0

#: 关闭验证轮询帽(秒;流内帽须 < 引擎段级 CLOSE_RESERVE,留点击余量)。
THREAD_CLOSE_VERIFY_TIMEOUT_SECONDS = 4.0

#: 关闭验证轮询步长(秒)。
THREAD_STATE_POLL_SECONDS = 1.0

#: 每段关闭储备(秒;引擎预算面消费:每段 = wait_for(开+读, remaining−
#: 本值) + wait_for(关, 本值);兜底 open_chat_flow 走独立预算不挤这里)。
CLOSE_RESERVE_SECONDS = 5.0

__all__ = [
    "CLOSE_RESERVE_SECONDS",
    "HASH_PROBE_JS",
    "LOCATE_CLOSE_BTN_JS",
    "LOCATE_REPLY_FOOTER_JS",
    "THREAD_CLOSE_VERIFY_TIMEOUT_SECONDS",
    "THREAD_FOOTER_POLL_SECONDS",
    "THREAD_FOOTER_READY_TIMEOUT_SECONDS",
    "THREAD_HASH_POLL_SECONDS",
    "THREAD_OPEN_HASH_TIMEOUT_SECONDS",
    "THREAD_PREP_SETTLE_SECONDS",
    "THREAD_READ_SETTLE_SECONDS",
    "THREAD_STATE_JS",
    "THREAD_STATE_POLL_SECONDS",
    "close_thread_flow",
    "open_thread_flow",
    "read_page_hash",
    "read_thread_state",
]


#: hash 探针(线程开/关的状态基判据面;单表达式,evaluate 直跑)。
HASH_PROBE_JS = "() => location.hash"


async def read_page_hash(page: Any) -> str:
    """当前页 hash(线程开/关的状态基判据;异常容错空串,验证自然失败走兜底)."""
    try:
        value = await page.evaluate(HASH_PROBE_JS)
    except Exception:  # noqa: BLE001 - 导航间隙异常按空串,不掩盖主流程
        return ""
    return str(value) if value is not None else ""


#: 评论钮定位件(泡内 footer;``scroll=true`` 顺带 scrollIntoView,幂等)。
#: 只定位不点击 —— 真点时序(新鲜 rect 即点)在 :func:`open_thread_flow`。
LOCATE_REPLY_FOOTER_JS = """
(args) => {
    const scope = document.querySelector('.chat.tabs-tab.active') || document;
    const bubble = scope.querySelector('.bubble[data-mid="' + args.mid + '"]');
    if (!bubble) return {ok: false, reason: 'post_missing'};
    const footer = bubble.querySelector(
        'replies-element.replies, .replies-footer');
    if (!footer) return {ok: false, reason: 'no_footer'};
    if (args.scroll) {
        footer.scrollIntoView({block: 'center'});
        return {ok: true, reason: 'scrolled'};
    }
    const rect = footer.getBoundingClientRect();
    if (!(rect.width > 0 && rect.height > 0)) {
        return {ok: false, reason: 'invisible'};
    }
    return {ok: true, reason: 'located',
            x: rect.x + rect.width / 2, y: rect.y + rect.height / 2};
}
"""


#: 线程页片状态件(频道页片识别 = 含频道帖 mid 的页片;must_fix4 状态基)。
THREAD_STATE_JS = """
(args) => {
    const tabs = Array.from(document.querySelectorAll('.chat.tabs-tab'));
    let chanTab = null;
    if (args && args.postMid != null) {
        chanTab = tabs.find((t) =>
            t.querySelector('.bubble[data-mid="' + args.postMid + '"]')) || null;
    }
    return {
        hash: location.hash || '',
        tabCount: tabs.length,
        chanTabActive: chanTab
            ? String(chanTab.className).indexOf('active') !== -1 : null,
    };
"""


async def read_thread_state(page: Any, post_mid: str) -> dict[str, Any]:
    """线程开/关状态快照(异常容错空 dict,调用方按失败面处理)."""
    try:
        state = await page.evaluate(THREAD_STATE_JS, {"postMid": post_mid})
    except Exception:  # noqa: BLE001 - 导航间隙异常按空快照
        return {}
    return state if isinstance(state, dict) else {}


def _state_back(state: Any, expected_hash: str) -> bool:
    """状态基双条件:hash 回频道 hash 且频道页片 active(must_fix4)."""
    return bool(
        isinstance(state, dict)
        and state.get("chanTabActive") is True
        and str(state.get("hash")) == str(expected_hash)
    )


#: 线程顶栏关闭钮定位件(r6 实测唯一有效返回路径;elementFromPoint 验命中)。
LOCATE_CLOSE_BTN_JS = """
() => {
    const active = document.querySelector('.chat.tabs-tab.active');
    if (!active) return {ok: false, reason: 'no_active_tab'};
    const btn = active.querySelector(
        '.topbar .sidebar-close-button, .sidebar-close-button');
    if (!btn) return {ok: false, reason: 'close_btn_missing'};
    const rect = btn.getBoundingClientRect();
    if (!(rect.width > 0 && rect.height > 0)) {
        return {ok: false, reason: 'invisible'};
    }
    const x = rect.x + rect.width / 2, y = rect.y + rect.height / 2;
    const hit = document.elementFromPoint(x, y);
    return {ok: true, x: x, y: y,
            hit: hit ? String(hit.className).slice(0, 60) : null,
            badge: btn.querySelector('.back-unread-badge') !== null};
}
"""


async def open_thread_flow(
    page: Any,
    post_mid: str,
    *,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> dict[str, Any]:
    """点开频道帖的评论线程(真点时序;引擎线程段消费).

    流程(导航时序标定,模块 docstring):评论钮就绪轮询(scrollIntoView
    幂等伴随)→ ~2s 懒加载挪位稳态 → **新鲜** rect 立即 ``page.mouse.click``
    → hash 变化轮询 ≤20s。

    Returns:
        ``{ok, reason, ...}``;成功 reason=``thread_open`` 带 ``hash``;
        失败词表 = ``post_missing``/``no_footer``/``invisible``(钮面)、
        ``thread_open_timeout``(点击后 hash 未变 —— 坐标失效或 DOM 改版)。
    """
    import time as _time

    # 1) 评论钮就绪轮询(懒渲染迟到容忍;每次尝试顺带 scrollIntoView)
    deadline = _time.monotonic() + THREAD_FOOTER_READY_TIMEOUT_SECONDS
    while True:
        try:
            found = await page.evaluate(
                LOCATE_REPLY_FOOTER_JS, {"mid": post_mid, "scroll": True}
            )
        except Exception:  # noqa: BLE001 - 页面重渲染间隙异常重试
            found = None
        if isinstance(found, dict) and found.get("ok"):
            break
        reason = (
            found.get("reason")
            if isinstance(found, dict)
            else "footer_locate_failed"
        )
        if _time.monotonic() >= deadline:
            return {"ok": False, "reason": reason or "footer_locate_failed"}
        await sleep(THREAD_FOOTER_POLL_SECONDS)
    # 2) 懒加载挪位稳态窗(scrollIntoView 挪位后旧坐标即失效,实测在案)
    await sleep(THREAD_PREP_SETTLE_SECONDS)
    # 3) 新鲜 rect 即点(定位与点击之间零额外等待)
    try:
        fresh = await page.evaluate(
            LOCATE_REPLY_FOOTER_JS, {"mid": post_mid, "scroll": False}
        )
    except Exception:  # noqa: BLE001 - 真跑面异常如实报失败面
        fresh = None
    if not (isinstance(fresh, dict) and fresh.get("ok")):
        reason = fresh.get("reason") if isinstance(fresh, dict) else "locate_failed"
        return {"ok": False, "reason": reason or "locate_failed"}
    pre_hash = await read_page_hash(page)
    await page.mouse.click(fresh["x"], fresh["y"])
    # 4) 开成标志 = hash 变化(≤20s;URL hash 无线程参数,变化即接管)
    deadline = _time.monotonic() + THREAD_OPEN_HASH_TIMEOUT_SECONDS
    while True:
        current = await read_page_hash(page)
        if current != pre_hash:
            return {"ok": True, "reason": "thread_open", "hash": current}
        if _time.monotonic() >= deadline:
            return {"ok": False, "reason": "thread_open_timeout", "hash": current}
        await sleep(THREAD_HASH_POLL_SECONDS)


async def close_thread_flow(
    page: Any,
    post_mid: str,
    expected_hash: str,
    *,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
) -> dict[str, Any]:
    """收评论线程页片(close-btn 真点 + 状态基双条件验证).

    幂等短路:已回频道(hash + 频道页片 active 双条件)→ 免点 —— 防对频道
    页片误点 close 把频道本身关掉(开线程失败面天然走到这里)。

    Returns:
        ``{ok, reason}``;成功 reason=``already_closed``/``closed``;失败
        词表 = ``close_btn_missing``/``no_active_tab``/``invisible``/
        ``close_verify_timeout``(败则调用方走 open_chat_flow 兜底)。
    """
    import time as _time

    state = await read_thread_state(page, post_mid)
    if _state_back(state, expected_hash):
        return {"ok": True, "reason": "already_closed"}
    try:
        btn = await page.evaluate(LOCATE_CLOSE_BTN_JS)
    except Exception:  # noqa: BLE001 - 重渲染间隙异常如实报失败面
        btn = None
    if not (isinstance(btn, dict) and btn.get("ok")):
        reason = btn.get("reason") if isinstance(btn, dict) else "close_btn_missing"
        return {"ok": False, "reason": reason or "close_btn_missing"}
    await page.mouse.click(btn["x"], btn["y"])
    deadline = _time.monotonic() + THREAD_CLOSE_VERIFY_TIMEOUT_SECONDS
    while True:
        state = await read_thread_state(page, post_mid)
        if _state_back(state, expected_hash):
            return {"ok": True, "reason": "closed"}
        if _time.monotonic() >= deadline:
            return {"ok": False, "reason": "close_verify_timeout", "state": state}
        await sleep(THREAD_STATE_POLL_SECONDS)
