"""评论线程档测试(10-12-tg-comments-reach)—— 零网络零真浏览器.

覆盖:

- **fixture 钉死面**(must_fix1/must_fix5):``tests/fixtures/
  tg_web_thread_bubbles.html``(r7_2 真实回泡 HTML + r5_3 头帖/服务泡
  attrs)经 html.parser 极简抽取器镜像 ``collect_thread_messages_js``
  的结构契约 → :func:`collect_thread_updates` → 产出**仅回泡**锚
  (``#tg-<-4373866046>-<回mid>``,讨论群独立命名空间),头帖/服务泡
  零出现;文本 = ``.translatable-message`` 叶(不粘时间)。
- **半失配哨兵**(must_fix5):text 命中率 <0.8 如实入 stats(调用方按
  ``tg_web_dom_stale`` 词表留痕,引擎测试面另钉)。
- **导航流**(web_thread):open_thread_flow 真点时序(scroll→稳态→
  新鲜 rect 即点→hash 变化)、footer 缺失/开不成结构化失败;
  close_thread_flow 幂等短路(防误关频道页片)、close-btn 真点双条件
  验证、验证超时结构化失败。
- **JS 形状把守**:结构过滤/文本序/作用域选择器烙进 JS 体(改版跟修面)。
"""

from __future__ import annotations

import asyncio
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pytest

from myssia.telegram import web_thread
from myssia.telegram.web_dom import (
    ACTIVE_TAB_SELECTOR,
    REPLY_MARKER_ATTR,
    THREAD_MESSAGE_TEXT_SELECTORS,
    collect_channel_posts,
    collect_channel_posts_js,
    collect_thread_messages_js,
    collect_thread_updates,
)
from myssia.telegram.web_thread import (
    HASH_PROBE_JS,
    LOCATE_CLOSE_BTN_JS,
    LOCATE_REPLY_FOOTER_JS,
    THREAD_STATE_JS,
    close_thread_flow,
    open_thread_flow,
    read_page_hash,
)

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "tg_web_thread_bubbles.html"

#: 频道/线程 hash(r6 活页取证:clashv8 频道 ↔ xoxo8868 讨论群)。
CHANNEL_HASH = "#@clashv8"
THREAD_HASH = "#@xoxo8868"


def run(coro: Any) -> Any:
    return asyncio.run(coro)


@pytest.fixture(autouse=True)
def _fast_thread_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """轮询帽/步长全归零(失败路径单测零等待;真跑标定值在 web_thread)."""
    monkeypatch.setattr(web_thread, "THREAD_FOOTER_READY_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_FOOTER_POLL_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_OPEN_HASH_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_HASH_POLL_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_CLOSE_VERIFY_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_STATE_POLL_SECONDS", 0.0)


# --------------------------------------------------------------------- fakes


class _SleepRecorder:
    """零等待 sleep 替身:记录时长序列(时序断言面)."""

    def __init__(self) -> None:
        self.calls: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)


class _FlowMouse:
    """受信点击 fake:记录坐标并驱动页片状态翻转(真点语义)."""

    def __init__(self, page: "_FlowPage") -> None:
        self.clicks: list[tuple[float, float]] = []
        self._page = page

    async def click(self, x: float, y: float, **_: Any) -> None:
        self.clicks.append((x, y))
        self._page.apply_click(x, y)


class _FlowPage:
    """线程导航流 fake:evaluate 按 JS 体分发,真点坐标翻转页片状态.

    坐标判例:r6 实测 close-btn 位于 (504, 40);footer 坐标任取常量。
    """

    FOOTER_XY = (10.0, 20.0)
    CLOSE_XY = (504.0, 40.0)

    def __init__(
        self,
        *,
        footer_ok: bool = True,
        footer_opens: bool = True,
        close_works: bool = True,
    ) -> None:
        self.in_thread = False
        self.footer_ok = footer_ok
        self.footer_opens = footer_opens
        self.close_works = close_works
        self.footer_calls: list[tuple[str, bool]] = []
        self.close_locates = 0
        self.state_calls = 0
        self.mouse = _FlowMouse(self)

    def apply_click(self, x: float, y: float) -> None:
        if (x, y) == self.FOOTER_XY and self.footer_opens:
            self.in_thread = True
        elif (x, y) == self.CLOSE_XY and self.close_works:
            self.in_thread = False

    async def evaluate(self, script: Any, arg: Any = None) -> Any:
        js = script if isinstance(script, str) else ""
        if "replies-element" in js:  # LOCATE_REPLY_FOOTER_JS
            self.footer_calls.append((str(arg.get("mid")), bool(arg.get("scroll"))))
            if not self.footer_ok or self.in_thread:
                return {"ok": False, "reason": "no_footer"}
            if arg.get("scroll"):
                return {"ok": True, "reason": "scrolled"}
            return {"ok": True, "reason": "located", "x": 10.0, "y": 20.0}
        if "sidebar-close-button" in js:  # LOCATE_CLOSE_BTN_JS
            self.close_locates += 1
            return {
                "ok": True,
                "x": 504.0,
                "y": 40.0,
                "hit": "btn-icon",
                "badge": True,
            }
        if "tabs-tab" in js:  # THREAD_STATE_JS
            self.state_calls += 1
            return {
                "hash": THREAD_HASH if self.in_thread else CHANNEL_HASH,
                "tabCount": 2 if self.in_thread else 1,
                "chanTabActive": not self.in_thread,
            }
        if js.strip() == HASH_PROBE_JS:
            return THREAD_HASH if self.in_thread else CHANNEL_HASH
        raise AssertionError(f"意外 evaluate 面:{js[:80]}")


class _PayloadPage:
    """collect 面 fake:evaluate 恒返固定载荷(记录调用)."""

    def __init__(self, payload: Any) -> None:
        self._payload = payload
        self.calls: list[str] = []

    async def evaluate(self, script: Any, arg: Any = None) -> Any:
        self.calls.append(script if isinstance(script, str) else "")
        return self._payload


# --------------------------------------------------------- fixture 钉死面


class _BubbleExtractor(HTMLParser):
    """极简泡抽取器(测试面):镜像 collect_thread_messages_js 的结构契约.

    只认 ``div.bubble[data-mid]`` 泡属性 + 后代文本按 class 命中
    (``translatable-message`` → text、``peer-title`` → sender、任何
    非空文本 → has_inner_text)—— 不做通用 CSS 选择器,fixture 结构
    钉死后逐字段对齐。
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.entries: list[dict[str, Any]] = []
        self._stack: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrd = {k: v for k, v in attrs if v is not None}
        classes = set((attrd.get("class") or "").split())
        node: dict[str, Any] = {"classes": classes, "entry": None}
        if "bubble" in classes and attrd.get("data-mid"):
            entry = {
                "mid": attrd["data-mid"],
                "peerId": attrd.get("data-peer-id"),
                "replyTo": attrd.get("data-reply-to-mid"),
                "text": None,
                "sender": None,
                "timestamp": (
                    float(attrd["data-timestamp"])
                    if attrd.get("data-timestamp")
                    else None
                ),
                "has_inner_text": False,
            }
            self.entries.append(entry)
            node["entry"] = entry
        elif self._stack:
            node["entry"] = self._stack[-1]["entry"]
        self._stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        if self._stack:
            self._stack.pop()

    def handle_data(self, data: str) -> None:
        if not self._stack or not data.strip():
            return
        node = self._stack[-1]
        entry = node.get("entry")
        if entry is None:
            return
        entry["has_inner_text"] = True
        if "translatable-message" in node["classes"] and entry["text"] is None:
            entry["text"] = data.strip()
        elif "peer-title" in node["classes"] and entry["sender"] is None:
            entry["sender"] = data.strip()


def _fixture_entries() -> list[dict[str, Any]]:
    extractor = _BubbleExtractor()
    extractor.feed(FIXTURE.read_text(encoding="utf-8"))
    return extractor.entries


def test_fixture_pins_thread_bubble_shapes() -> None:
    """fixture 自身钉死:三段形态在档(头帖带 data-saved-from、服务泡小数
    mid、回泡带 data-reply-to-mid + 讨论群 peer)。"""
    entries = {e["mid"]: e for e in _fixture_entries()}
    assert set(entries) == {"4295090508", "4295090508.0001", "4295090517", "4295090521"}
    head = entries["4295090508"]
    assert head["peerId"] == "-4373866046"
    assert head["replyTo"] is None  # 头帖无回泡判据属性(双注入防线)
    assert entries["4295090508.0001"]["replyTo"] is None  # 服务泡同
    for mid in ("4295090517", "4295090521"):
        reply = entries[mid]
        assert reply["replyTo"] == "4295090508"
        assert reply["peerId"] == "-4373866046"
        assert reply["text"] == "订阅"
    # r7_2 钉死值(时间戳/发送者)
    assert entries["4295090517"]["timestamp"] == 1791724777.0
    assert entries["4295090517"]["sender"] == "李某人 ."
    assert entries["4295090521"]["sender"] == "OO OO"


def test_collect_thread_updates_fixture_only_reply_anchors() -> None:
    """must_fix1/must_fix5 端到端(fixture→collect→分拣→锚):

    产出仅回泡 update(头帖/服务泡被 replyTo 二道守丢弃),锚 =
    ``#tg-<-4373866046>-<回mid>``(讨论群独立命名空间),头帖锚零出现;
    文本 = translatable-message 叶(『订阅』,不粘时间);stats 携带讨论群
    peer id(引擎第二次 updates_to_items 的 chat_id 实参)。
    """
    from myssia.engines.telegram import updates_to_items

    page = _PayloadPage(_fixture_entries())
    updates, stats = run(collect_thread_updates(page, limit=50))
    assert "data-reply-to-mid" in page.calls[0]  # JS 面就是线程读取件
    assert stats["thread_chat_id"] == "-4373866046"
    assert stats["text_hit_rate"] == 1.0
    assert stats["reply_bubbles"] == 2
    message_ids = [u["message"]["message_id"] for u in updates]
    assert message_ids == [4295090517, 4295090521]  # 头帖/服务泡零出现
    first = updates[0]["message"]
    assert first["text"] == "订阅"
    assert first["from"] == {"first_name": "李某人 ."}
    assert first["chat"]["id"] == "-4373866046"
    items = updates_to_items(
        updates, stats["thread_chat_id"], source_url="https://web.telegram.org"
    )
    urls = [item["url"] for item in items]
    # 锚全形 = <源url>#tg-<讨论群peer>-<回mid>(负 peer 与 #tg- 连写双横线,
    # bot 线判例同形)
    assert urls == [
        "https://web.telegram.org#tg--4373866046-4295090517",
        "https://web.telegram.org#tg--4373866046-4295090521",
    ]
    assert not any("4295090508" in url for url in urls)  # 头帖锚零出现


def test_collect_thread_updates_half_mismatch_stats() -> None:
    """半失配哨兵统计(must_fix5):text 命中率如实入 stats(调用方留痕)."""
    entries = [
        {
            "mid": str(100 + i),
            "peerId": "-4373866046",
            "replyTo": "4295090508",
            "text": "订阅" if i < 2 else None,
            "sender": f"用户{i}",
            "timestamp": 1791724777.0,
            "has_inner_text": True,
        }
        for i in range(10)
    ]
    updates, stats = run(collect_thread_updates(_PayloadPage(entries), limit=50))
    assert stats["reply_bubbles"] == 10
    assert stats["text_hits"] == 2
    assert stats["text_hit_rate"] == pytest.approx(0.2)
    assert len(updates) == 2  # 失配不拦已读到的条目


def test_collect_thread_updates_non_list_and_no_peer() -> None:
    """非列表(DOM 改版面)与零 peer id(锚不可铸)= 零 update 如实回报."""
    updates, stats = run(collect_thread_updates(_PayloadPage("oops"), limit=50))
    assert updates == [] and stats["thread_chat_id"] is None
    entries = [{"mid": "1", "peerId": None, "replyTo": "9", "text": "hi",
                "has_inner_text": True}]
    updates, stats = run(collect_thread_updates(_PayloadPage(entries), limit=50))
    assert updates == [] and stats["thread_chat_id"] is None


# --------------------------------------------------------------- JS 形状


def test_thread_collect_js_shapes() -> None:
    """结构过滤/文本序/作用域烙进 JS 体(改版跟修面钉死)."""
    js = collect_thread_messages_js(7)
    assert js.startswith("const LIMIT = 7;")
    assert f"[{REPLY_MARKER_ATTR.replace('data-', 'data-')}]" in js.replace(
        "'.bubble[data-mid][data-reply-to-mid]'", ""
    ) or "[data-reply-to-mid]" in js  # 结构过滤(must_fix1)
    assert ACTIVE_TAB_SELECTOR in js  # active tab 作用域(双 tab 并存)
    # must_fix5:.translatable-message 首位、.message 不进线程档
    assert THREAD_MESSAGE_TEXT_SELECTORS[0] == ".translatable-message"
    assert ".message" not in THREAD_MESSAGE_TEXT_SELECTORS
    assert ".translatable-message" in js
    assert "has_inner_text" in js  # 半失配哨兵统计面
    posts_js = collect_channel_posts_js()
    assert "replies-footer-text" in posts_js
    assert "mid === '-1'" in posts_js  # 广告泡滤除
    assert "is-unread" in posts_js


def test_navigation_js_shapes() -> None:
    """导航件形状:footer 只定位不点击;close-btn elementFromPoint 验命中."""
    assert "scrollIntoView" in LOCATE_REPLY_FOOTER_JS
    assert "no_footer" in LOCATE_REPLY_FOOTER_JS
    assert "post_missing" in LOCATE_REPLY_FOOTER_JS
    assert "elementFromPoint" in LOCATE_CLOSE_BTN_JS
    assert "back-unread-badge" in LOCATE_CLOSE_BTN_JS
    assert "close_btn_missing" in LOCATE_CLOSE_BTN_JS
    assert "chanTabActive" in THREAD_STATE_JS


# ------------------------------------------------------------- collect 帖


def test_collect_channel_posts_normalizes_and_filters() -> None:
    page = _PayloadPage(
        [
            {"mid": "4294967708", "peerId": "-3770098404",
             "commentsCount": 1128, "isUnread": True},
            {"mid": "4294967633", "peerId": "-3770098404",
             "commentsCount": 0, "isUnread": False},  # 无评论钮帖
            {"mid": "4294967702", "peerId": "-3770098404",
             "commentsCount": -3, "isUnread": False},  # 异型计数归零
            "junk",  # 非字典跳过
        ]
    )
    posts = run(collect_channel_posts(page))
    assert posts == [
        {"mid": "4294967708", "peer_id": "-3770098404",
         "comments_count": 1128, "is_unread": True},
        {"mid": "4294967633", "peer_id": "-3770098404",
         "comments_count": 0, "is_unread": False},
        {"mid": "4294967702", "peer_id": "-3770098404",
         "comments_count": 0, "is_unread": False},
    ]
    assert run(collect_channel_posts(_PayloadPage(None))) == []  # 非列表容错


# ------------------------------------------------------------ 导航流


def test_open_thread_flow_real_click_timing() -> None:
    """真点时序:scroll→稳态窗→新鲜 rect 立即点击→hash 变化开成."""
    page = _FlowPage()
    recorder = _SleepRecorder()
    result = run(open_thread_flow(page, "4294967708", sleep=recorder))
    assert result["ok"] and result["reason"] == "thread_open"
    assert result["hash"] == THREAD_HASH
    # 定位序:scroll=True(就绪轮询)→ 稳态 → scroll=False(新鲜 rect)
    assert page.footer_calls == [("4294967708", True), ("4294967708", False)]
    assert recorder.calls == [web_thread.THREAD_PREP_SETTLE_SECONDS]
    assert page.mouse.clicks == [_FlowPage.FOOTER_XY]


def test_open_thread_flow_footer_missing_structured() -> None:
    page = _FlowPage(footer_ok=False)
    result = run(open_thread_flow(page, "4294967633", sleep=_SleepRecorder()))
    assert result["ok"] is False
    assert result["reason"] == "no_footer"
    assert page.mouse.clicks == []


def test_open_thread_flow_hash_never_changes_structured() -> None:
    """点击后 hash 不动(坐标失效/DOM 改版)= thread_open_timeout."""
    page = _FlowPage(footer_opens=False)
    result = run(open_thread_flow(page, "4294967708", sleep=_SleepRecorder()))
    assert result["ok"] is False
    assert result["reason"] == "thread_open_timeout"
    assert page.mouse.clicks == [_FlowPage.FOOTER_XY]  # 点击发生了,页面没接管


def test_close_thread_flow_already_closed_short_circuits() -> None:
    """幂等短路:已回频道(双条件过)免点 —— 防误关频道页片本身."""
    page = _FlowPage()  # in_thread=False
    result = run(
        close_thread_flow(page, "4294967708", CHANNEL_HASH, sleep=_SleepRecorder())
    )
    assert result == {"ok": True, "reason": "already_closed"}
    assert page.close_locates == 0
    assert page.mouse.clicks == []


def test_close_thread_flow_click_and_verify() -> None:
    page = _FlowPage()
    page.apply_click(*_FlowPage.FOOTER_XY)  # 预置在线程页片
    result = run(
        close_thread_flow(page, "4294967708", CHANNEL_HASH, sleep=_SleepRecorder())
    )
    assert result["ok"] is True and result["reason"] == "closed"
    assert page.mouse.clicks == [_FlowPage.CLOSE_XY]
    assert page.in_thread is False


def test_close_thread_flow_verify_timeout_structured() -> None:
    """点击后双条件不过(hash 或频道页片未复原)= 结构化失败走兜底."""
    page = _FlowPage(close_works=False)
    page.apply_click(*_FlowPage.FOOTER_XY)
    result = run(
        close_thread_flow(page, "4294967708", CHANNEL_HASH, sleep=_SleepRecorder())
    )
    assert result["ok"] is False
    assert result["reason"] == "close_verify_timeout"
    assert page.mouse.clicks == [_FlowPage.CLOSE_XY]


def test_close_thread_flow_missing_btn_structured() -> None:
    class _NoBtnPage(_FlowPage):
        async def evaluate(self, script: Any, arg: Any = None) -> Any:
            js = script if isinstance(script, str) else ""
            if "sidebar-close-button" in js:
                return {"ok": False, "reason": "close_btn_missing"}
            return await super().evaluate(script, arg)

    page = _NoBtnPage()
    page.apply_click(*_FlowPage.FOOTER_XY)  # 预置在线程页片
    result = run(
        close_thread_flow(page, "4294967708", CHANNEL_HASH,
                          sleep=_SleepRecorder())
    )
    assert result == {"ok": False, "reason": "close_btn_missing"}


def test_read_page_hash_tolerates_evaluate_failure() -> None:
    class _Boom:
        async def evaluate(self, script: Any, arg: Any = None) -> Any:
            raise RuntimeError("navigation in flight")

    assert run(read_page_hash(_Boom())) == ""
    assert run(read_page_hash(_PayloadPage("#@clashv8"))) == "#@clashv8"
