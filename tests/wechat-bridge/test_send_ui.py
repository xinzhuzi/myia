"""send_text 三源合体单测(task 10-14-wechat-send-text design §G;全 mock,
零真实系统调用——平台原语/AX/OCR/时钟全部是 sendui 与 axui 的注入点,
:class:`FakeHarness` 整组替换)。

受测面(design §G test_send_ui 行 ①~⑫ + 既有三支柱行为断言语义保留):

① AX 主链全绿;② 降级链全绿(键序无 KEY_DOWN_ARROW);③ 盲回车禁止
(KEY_RETURN 仅发送点一次);④ 哨兵空断言链;⑤ 清空轮询超时 → uncertain
(不抛错);⑥ dry-run(无回车无 on_armed/KEY_ESCAPE/nav_debug);⑦
title_verify 三枚举;⑧ emoji(乱码单行 → unique-row → indirect;零候选 →
exit 15 拒发=设计内行为);⑨ CGEvent 事件源;⑩ on_armed fail-closed +
armed 后 on_receipt_green 抛 → 吞;⑪ 聚焦断言两通道对称;⑫ 回执轮询
按 RECEIPT_POLL_SCHEDULE 退避(假钟推进)。

既有行为断言(0.7.0 语义,新序列下保留):激活失败/窗口缺 → exit 15;
回读失败 → exit 15 且无回车;剪贴板复原;载荷永不载正文(红线 6);
text_confirmed 纯函数。
"""

from __future__ import annotations

import dataclasses
import itertools
import json
import sys
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))

import wechat_bridge.axui as axui  # noqa: E402
import wechat_bridge.sendui as sendui  # noqa: E402
from wechat_bridge.codes import (  # noqa: E402
    EXIT_OK,
    SEND_AX_FOCUS_REQUIRED,
    TIMEOUT,
    BridgeError,
)
from wechat_bridge.config import BridgeConfig  # noqa: E402
from wechat_bridge.pixel import OcrLine  # noqa: E402
from wechat_bridge.sendtarget import SendTarget  # noqa: E402

CHAT = "文件传输助手"
BODY = "桥发冒烟正文 hello 42"
TARGET = SendTarget(
    username="filehelper", alias=None, display_name=CHAT, search_term="filehelper"
)


@dataclasses.dataclass
class FakeWindow:
    window_id: int = 42
    onscreen: bool = True
    width: float = 800.0
    height: float = 600.0
    pid: int = 100
    x: float = 100.0
    y: float = 200.0


def _sline(text: str, y: float) -> OcrLine:
    """搜索面板行(裁剪系坐标;分区头默认在最下做锚)。"""
    return OcrLine(text=text, conf=0.9, x=0.10, y=y, w=0.20, h=0.04)


class FakeHarness:
    """sendui/axui 平台原语的进程内替身(键序/点击/剪贴板/composer 全程留痕)。

    状态机:focus ∈ {"composer", "other"};composer = 输入框内容;clip =
    剪贴板。Cmd+V(焦点在 composer)→ composer=clip;Cmd+C → clip=
    composer;Cmd+A+Delete → composer 清空;Return(焦点 composer)→
    发送:composer 清空并记 sent_returns。
    """

    def __init__(
        self,
        *,
        channel: str = "cgevent_ocr",
        frontmost: bool = True,
        window: object | None = FakeWindow(),
        ocr_texts: dict[str, str] | None = None,
        search_lines: list[OcrLine] | None = None,
        pre_nav_title: str | None = None,
        activate_raises: BridgeError | None = None,
        ax_search_write: bool | None = None,
    ) -> None:
        self.keys: list[tuple[int, int]] = []
        self.clicks: list[tuple[int, int]] = []
        self.clip_sets: list[str] = []
        self.sleeps: list[float] = []
        self.ocr_calls: list[str] = None or []  # type: ignore[assignment]
        self.ocr_texts = {
            "title": CHAT,
            "input": BODY,
            "sent": BODY,
            **(ocr_texts or {}),
        }
        self.search_lines = search_lines if search_lines is not None else [
            _sline("联系人", 0.80),  # 分区头(锚)
            _sline(CHAT, 0.40),  # 目标行
        ]
        self.pre_nav_title = pre_nav_title if pre_nav_title is not None else CHAT
        self.channel_want = channel
        # write_search_value 可用性(0.8.1 起降级链也先试 AXFocusedUIElement
        # 直写;None = 随通道——ax True / cgevent False=走剪贴板兜底)。
        self.ax_search_write = (
            ax_search_write if ax_search_write is not None else channel == "ax"
        )
        self.frontmost = frontmost
        self.window = window
        self.activate_raises = activate_raises
        # 状态机
        self.focus = "other"
        self.composer = ""
        self.clip: str | None = None
        self.sent_returns = 0
        self.armed_calls = 0
        self.receipt_calls: list[float] = []
        self.green_calls = 0
        self._clock = itertools.count(1)
        self._wall = itertools.count(1700000000)
        self.title_ocr_count = 0

    # ------------------------------------------------------------ 装配 ----
    def install(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sendui, "monotonic", lambda: float(next(self._clock)))
        monkeypatch.setattr(sendui, "wall_clock", lambda: float(next(self._wall)))
        monkeypatch.setattr(sendui, "sleep", self._sleep)
        monkeypatch.setattr(sendui, "activate_wechat", self._activate)
        # keystroke 引擎恒失败 → 双引擎回落 CGEvent mock(键序断言面不变;
        # 独立单测锁 post_key_stevents 自身)。
        monkeypatch.setattr(sendui, "post_key_stevents", lambda k, f=0: False)
        monkeypatch.setattr(sendui, "frontmost_is_wechat", lambda: self.frontmost)
        monkeypatch.setattr(sendui, "post_key", self._post_key)
        monkeypatch.setattr(sendui, "click_at", self._click_at)
        monkeypatch.setattr(sendui, "set_clipboard_text", self._set_clip)
        monkeypatch.setattr(sendui, "clipboard_text", lambda: self.clip)
        monkeypatch.setattr(sendui, "_ocr_region", self._ocr_region)
        monkeypatch.setattr(sendui, "_ocr_region_lines", self._ocr_region_lines)
        monkeypatch.setattr(sendui, "_find_window", lambda: self.window)
        monkeypatch.setattr(sendui, "_post_send_verify", self._post_send_verify)
        # axui 原语(通道相关)
        monkeypatch.setattr(axui, "probe_wechat_ax", lambda: self.channel_want == "ax")
        monkeypatch.setattr(axui, "write_search_value", self._ax_write_search)
        monkeypatch.setattr(axui, "press_session_item", self._ax_press_item)
        monkeypatch.setattr(axui, "read_current_chat_name", lambda: self._ax_label())
        monkeypatch.setattr(axui, "read_input_value", lambda: self._ax_input_value())
        monkeypatch.setattr(axui, "write_input_value", self._ax_write_input)
        monkeypatch.setattr(axui, "focus_input", self._ax_focus_input)
        monkeypatch.setattr(axui, "focused_is_input", lambda: self._ax_focused())

    # ------------------------------------------------------------ 原语 ----
    def _activate(self) -> None:
        if self.activate_raises is not None:
            raise self.activate_raises

    def _sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)

    def _post_key(self, key_code: int, flags: int = 0) -> None:
        self.keys.append((key_code, flags))
        if key_code == sendui.KEY_V and flags == sendui.FLAG_COMMAND and self.focus == "composer":
            self.composer = self.clip or ""
        elif key_code == sendui.KEY_C and flags == sendui.FLAG_COMMAND and self.focus == "composer":
            if self.composer:  # 空框 Cmd+C 无效果(剪贴板保持哨兵 → 探得 None)
                self.clip = self.composer
        elif key_code == sendui.KEY_DELETE:
            self.composer = ""
        elif key_code == sendui.KEY_RETURN and flags == 0 and self.focus == "composer":
            self.sent_returns += 1
            self.composer = ""  # 发出 → 清空(降级链哨兵读/AX 读均见空)

    def _click_at(self, x: int, y: int) -> None:
        self.clicks.append((x, y))
        self.focus = "composer"  # 点击范围收窄:行点击(切会话)/composer 点

    def _set_clip(self, text: str) -> None:
        self.clip_sets.append(text)
        self.clip = text

    def _ocr_region(self, _window, _box, _workdir, tag: str) -> str:
        self.ocr_calls.append(tag)
        if tag == "title":
            self.title_ocr_count += 1
            if self.title_ocr_count == 1 and self.pre_nav_title is not None:
                return self.pre_nav_title
        return self.ocr_texts.get(tag, "")

    def _ocr_region_lines(self, _window, _box, _workdir, tag: str) -> list[OcrLine]:
        self.ocr_calls.append(tag)
        return list(self.search_lines)

    def _post_send_verify(self, _body, _workdir) -> dict:
        return {"post_send_verified": True, "post_send_note": None}

    # ------------------------------------------------------- axui 替身 ----
    def _ax_write_search(self, term: str) -> bool:
        return self.ax_search_write

    def _ax_press_item(self, name: str) -> bool:
        return self.channel_want == "ax"

    def _ax_label(self) -> str | None:
        return CHAT if self.channel_want == "ax" else None

    def _ax_input_value(self) -> str | None:
        return self.composer if self.channel_want == "ax" else None

    def _ax_write_input(self, text: str) -> bool:
        if self.channel_want != "ax":
            return False
        self.composer = text
        return True

    def _ax_focus_input(self) -> bool:
        if self.channel_want != "ax":
            return False
        self.focus = "composer"
        return True

    def _ax_focused(self) -> bool | None:
        return self.focus == "composer" if self.channel_want == "ax" else None

    # -------------------------------------------------------- 回调替身 ----
    def on_armed(self) -> None:
        self.armed_calls += 1

    def on_receipt_green(self) -> None:
        self.green_calls += 1

    def receipt_query(self, username: str, body: str, since_epoch: float) -> bool:
        self.receipt_calls.append(since_epoch)
        return True

    # ------------------------------------------------------------ 断言面 ----
    def return_keys(self) -> list[tuple[int, int]]:
        return [key for key in self.keys if key[0] == sendui.KEY_RETURN]

    def body_pasted(self) -> bool:
        return BODY in self.clip_sets


def _run(harness: FakeHarness, *, dry_run: bool = False, on_armed=None, on_receipt_green=None, receipt_query=None):
    return sendui.send_text(
        BridgeConfig(),
        TARGET,
        BODY,
        dry_run=dry_run,
        on_armed=on_armed,
        on_receipt_green=on_receipt_green,
        receipt_query=receipt_query,
    )


@pytest.fixture()
def harness(monkeypatch: pytest.MonkeyPatch) -> FakeHarness:
    fake = FakeHarness()
    fake.install(monkeypatch)
    return fake


@pytest.fixture()
def ax_harness(monkeypatch: pytest.MonkeyPatch) -> FakeHarness:
    fake = FakeHarness(channel="ax")
    fake.install(monkeypatch)
    return fake


class TestHappyPaths:
    """① AX 主链全绿;② 降级链全绿(键序无 KEY_DOWN_ARROW)。"""

    def test_ax_channel_happy_path(self, ax_harness: FakeHarness) -> None:
        payload = _run(
            ax_harness, on_armed=ax_harness.on_armed,
            on_receipt_green=ax_harness.on_receipt_green,
            receipt_query=ax_harness.receipt_query,
        )
        send = payload["send"]
        assert send["sent"] is True and send["attempts"] == 1
        assert send["channel"] == "ax"
        assert send["readback"] == "ax_value"
        assert send["title_verify"] == "ax_label"
        assert send["composer_cleared"] is True
        assert send["localdb_receipt"] is True
        assert send["post_send_verified"] is True
        assert send["target"] == {"username": "filehelper", "display_name": CHAT}
        assert ax_harness.armed_calls == 1 and ax_harness.green_calls == 1
        assert len(ax_harness.receipt_calls) == 1
        assert ax_harness.return_keys() == [(sendui.KEY_RETURN, 0)]  # ③ 唯一一次回车

    def test_cgevent_fallback_happy_path(self, harness: FakeHarness) -> None:
        payload = _run(
            harness, on_armed=harness.on_armed,
            on_receipt_green=harness.on_receipt_green,
            receipt_query=harness.receipt_query,
        )
        send = payload["send"]
        assert send["sent"] is True and send["channel"] == "cgevent_ocr"
        assert send["readback"] == "clipboard_copy"  # 四路:剪贴板对账→(ax 关)→全量复制→(未达 OCR)
        assert send["title_verify"] == "ocr"
        assert harness.return_keys() == [(sendui.KEY_RETURN, 0)]
        # 键序:无 KEY_DOWN_ARROW(盲回车键序已删除,design §B-5)
        assert all(key[0] != getattr(sendui, "KEY_DOWN_ARROW", 0x7D) for key in harness.keys)
        # 导航 = 分区过滤点击(非回车)
        assert len(harness.clicks) >= 2  # 结果行 + composer
        assert harness.sent_returns == 1

    def test_payload_never_carries_body(self, harness: FakeHarness) -> None:
        payload = _run(harness, on_armed=harness.on_armed)
        assert BODY not in json.dumps(payload, ensure_ascii=False)

    def test_clipboard_restored(self, harness: FakeHarness) -> None:
        harness.clip = "主人原来的剪贴板"
        _run(harness, on_armed=harness.on_armed)
        assert harness.clip_sets[-1] == "主人原来的剪贴板"

    def test_clipboard_cleared_when_originally_empty(self, harness: FakeHarness) -> None:
        _run(harness, on_armed=harness.on_armed)
        assert harness.clip_sets[-1] == ""


class TestBlindReturnBan:
    """③ 盲回车禁止:KEY_RETURN 仅发送点一次;失败路径零回车。"""

    def test_readback_failure_never_returns(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """回读全败 → exit 15;全键序零 KEY_RETURN。"""
        harness = FakeHarness(ocr_texts={"input": ""})
        harness.install(monkeypatch)
        # 全量复制回读路:Cmd+C 复制回空(输入带模拟空,回读必败)
        monkeypatch.setattr(sendui, "_copy_all_readback", lambda *a, **k: False)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness)
        assert excinfo.value.exit_code == SEND_AX_FOCUS_REQUIRED == 15
        assert "readback" in excinfo.value.message
        assert harness.return_keys() == []  # 零回车
        assert harness.sent_returns == 0

    def test_activate_timeout_raises_15_stage_activate(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness(frontmost=False)
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness)
        assert excinfo.value.exit_code == 15
        assert "activate" in excinfo.value.message
        assert harness.keys == []

    def test_window_missing_raises_15(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness(window=None)
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness)
        assert excinfo.value.exit_code == 15
        assert "window" in excinfo.value.message

    def test_subprocess_timeout_propagates_30(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness(
            activate_raises=BridgeError(TIMEOUT, "平台子进程超时(osascript…)", fix_hint="重试")
        )
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness)
        assert excinfo.value.exit_code == TIMEOUT == 30


class TestNavigateZeroCandidates:
    """⑧ 后半:搜索面板零候选 → exit 15 拒发(设计内行为,绝不盲点)。"""

    def test_zero_candidates_refuses_to_send(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness(search_lines=[_sline("联系人", 0.80)])  # 只有分区头,零候选
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness)
        assert excinfo.value.exit_code == 15
        assert "navigate" in excinfo.value.message
        assert harness.return_keys() == []
        assert harness.clicks == []  # 零候选 → 零点击


class TestSentinelAndClear:
    """④ 哨兵空断言链;⑤ 清空轮询超时 → uncertain(不抛错)。"""

    def test_dirty_composer_cleared_then_proceeds(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """空断言:composer 有残留 → Cmd+A+Delete 清 → 复探空 → 放行。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        harness.composer = "残留草稿"

        def sentinel_read(window) -> str | None:
            return harness.composer or None

        monkeypatch.setattr(sendui, "read_composer_via_clipboard", sentinel_read)
        payload = _run(harness, on_armed=harness.on_armed)
        assert payload["send"]["sent"] is True
        assert (sendui.KEY_DELETE, 0) in harness.keys  # 清残留发生过

    def test_ax_dirty_composer_cleared_without_keyboard(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ax 路空断言零键盘(质询修正):残留经 ``write_input_value("")``
        AXValue 直写清空——**无 Cmd+A/Delete 键序**(焦点未断言不合成
        Delete,焦点落在会话列表时是 IM 破坏性键)。"""
        harness = FakeHarness(channel="ax")
        harness.install(monkeypatch)
        harness.composer = "残留草稿"
        writes: list[str] = []
        real_write = harness._ax_write_input

        def spy_write(text: str) -> bool:
            writes.append(text)
            return real_write(text)

        monkeypatch.setattr(axui, "write_input_value", spy_write)
        payload = _run(harness, on_armed=harness.on_armed)
        assert payload["send"]["sent"] is True
        assert "" in writes  # AXValue 直写空串清残留
        assert (sendui.KEY_DELETE, 0) not in harness.keys  # 零 Delete 键
        assert (sendui.KEY_A, sendui.FLAG_COMMAND) not in harness.keys  # 零 Cmd+A(空断言/清残留段)

    def test_ax_dry_run_cleanup_without_keyboard(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """ax 路 dry-run 收尾零键盘:草稿经 write_input_value("") 清,
        无 Cmd+A/Delete/Esc 键序。"""
        harness = FakeHarness(channel="ax")
        harness.install(monkeypatch)
        writes: list[str] = []
        real_write = harness._ax_write_input

        def spy_write(text: str) -> bool:
            writes.append(text)
            return real_write(text)

        monkeypatch.setattr(axui, "write_input_value", spy_write)
        payload = _run(harness, dry_run=True)
        assert payload["send"]["dry_run"] is True
        assert writes[-1] == ""  # 收尾清草稿 = AXValue 空串
        assert (sendui.KEY_DELETE, 0) not in harness.keys
        assert (sendui.KEY_ESCAPE, 0) not in harness.keys  # ax 路不进搜索态

    def test_cgevent_dry_run_cleanup_clicks_composer_first(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """cgevent 路 dry-run 清草稿键序前先 click composer(焦点断言
        等价保障,键序才允许)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        payload = _run(harness, dry_run=True)
        assert payload["send"]["dry_run"] is True
        keys = harness.keys
        delete_index = next(i for i, k in enumerate(keys) if k == (sendui.KEY_DELETE, 0))
        # Delete 前必有一个 composer 点击(clicks 单调递增于键序之前,
        # 以最后两次点击的 y 坐标均在 composer 带内近似)
        assert harness.clicks, "清草稿键序前必须有点击(焦点保障)"
        assert (sendui.KEY_ESCAPE, 0) in keys

    def test_dirty_composer_uncleanable_refuses(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """清不掉(复探仍非空)→ exit 15(composer_not_empty)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)

        def always_dirty(window) -> str | None:
            return "怎么都清不掉"

        monkeypatch.setattr(sendui, "read_composer_via_clipboard", always_dirty)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness)
        assert excinfo.value.exit_code == 15
        assert "composer_not_empty" in excinfo.value.message
        assert harness.return_keys() == []

    def test_clear_poll_timeout_reports_uncertain(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """清空轮询 12×80ms 超时 → 不抛错,载荷如实 composer_cleared=False
        (指纹不升 sent:全绿才升级,design §C-4)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        reads = {"n": 0}

        def staged_read(window) -> str | None:
            reads["n"] += 1
            if reads["n"] == 1:
                return None  # 空断言首探:空(放行)
            if reads["n"] == 2:
                return harness.composer or None  # 聚焦探:正文在框(聚焦成立)
            return BODY  # 发送后清空轮询:恒见正文(未清空 → uncertain)

        monkeypatch.setattr(sendui, "read_composer_via_clipboard", staged_read)
        payload = _run(
            harness, on_armed=harness.on_armed,
            on_receipt_green=harness.on_receipt_green,
            receipt_query=harness.receipt_query,
        )
        send = payload["send"]
        assert send["sent"] is True
        assert send["composer_cleared"] is False
        assert harness.green_calls == 0  # 非全绿不升级 sent
        assert harness.return_keys() == [(sendui.KEY_RETURN, 0)]


class TestDryRun:
    """⑥ dry-run:无回车无 on_armed、降级链 KEY_ESCAPE 退出搜索态、nav_debug。"""

    def test_dry_run_no_return_no_armed(self, harness: FakeHarness) -> None:
        payload = _run(harness, dry_run=True, on_armed=harness.on_armed)
        send = payload["send"]
        assert send["sent"] is False and send["dry_run"] is True
        assert send["navigated"] is True and send["pasted"] is True
        assert harness.return_keys() == []
        assert harness.armed_calls == 0
        assert harness.sent_returns == 0
        assert (sendui.KEY_ESCAPE, 0) in harness.keys  # 降级链退出搜索态
        assert (sendui.KEY_DELETE, 0) in harness.keys  # 清草稿
        nav = send["nav_debug"]
        assert nav["pick_rule"] == "text_match" and nav["terms_hit"] == CHAT
        assert isinstance(nav["pick_cx"], float) and isinstance(nav["pick_cy"], float)

    def test_dry_run_ax_channel_keeps_search_state(self, ax_harness: FakeHarness) -> None:
        """AX 通道 dry-run 不按 Esc(AXPress 导航不进搜索态)。"""
        payload = _run(ax_harness, dry_run=True)
        assert payload["send"]["nav_debug"]["pick_rule"] == "ax_session_item"
        assert (sendui.KEY_ESCAPE, 0) not in ax_harness.keys


class TestTitleVerifyModes:
    """⑦ title_verify 三枚举:ax_label / ocr / indirect。"""

    def test_ax_label_exact(self, ax_harness: FakeHarness) -> None:
        payload = _run(ax_harness)
        assert payload["send"]["title_verify"] == "ax_label"

    def test_ocr_band(self, harness: FakeHarness) -> None:
        payload = _run(harness)
        assert payload["send"]["title_verify"] == "ocr"

    def test_emoji_indirect_via_unique_row(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """⑧ 前:emoji 目标(乱码单行 → unique-row 采纳)→ 标题 OCR 读不
        出 → 间接证据链(标题带已变)放行,title_verify=indirect(真发路径;
        nav_debug 只在 dry-run 载荷,unique-row 采纳由下个 dry-run 用例直锁)。"""
        emoji_target = SendTarget(
            username="wxid_m90epbt5ojml22",
            alias="jiangliushi666",
            display_name="🐳",
            search_term="jiangliushi666",
        )
        harness = FakeHarness(
            ocr_texts={"title": "🦭读不出的新标题"},  # ≠ baseline → 会话已切换
            pre_nav_title="旧的会话标题",
            search_lines=[_sline("联系人", 0.80), _sline(".cert.=:)", 0.42)],  # 乱码单行
        )
        harness.install(monkeypatch)
        payload = sendui.send_text(
            BridgeConfig(), emoji_target, BODY,
            on_armed=harness.on_armed, receipt_query=harness.receipt_query,
        )
        send = payload["send"]
        assert send["title_verify"] == "indirect"
        assert send["sent"] is True and "dry_run" not in send  # 真发载荷不带 dry_run 键
        assert "nav_debug" not in send  # nav_debug 仅 dry-run 载(质询条1形态核实)
        assert harness.return_keys() == [(sendui.KEY_RETURN, 0)]

    def test_emoji_unique_row_rule_in_dry_run_nav_debug(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """dry-run 载荷直锁 unique-row 采纳(nav_debug.pick_rule;E-1 形状)。"""
        emoji_target = SendTarget(
            username="wxid_m90epbt5ojml22",
            alias="jiangliushi666",
            display_name="🐳",
            search_term="jiangliushi666",
        )
        harness = FakeHarness(
            ocr_texts={"title": "🦭读不出的新标题"},
            pre_nav_title="旧的会话标题",
            search_lines=[_sline("联系人", 0.80), _sline(".cert.=:)", 0.42)],
        )
        harness.install(monkeypatch)
        payload = sendui.send_text(BridgeConfig(), emoji_target, BODY, dry_run=True)
        nav = payload["send"]["nav_debug"]
        assert nav["pick_rule"] == "unique_row"
        assert nav["terms_hit"] == ""

    def test_ax_label_mismatch_refuses(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """AX label 可读但非目标 → exit 15(locate)。"""
        harness = FakeHarness(channel="ax")
        harness.install(monkeypatch)
        monkeypatch.setattr(axui, "read_current_chat_name", lambda: "别的会话")
        with pytest.raises(BridgeError) as excinfo:
            _run(harness)
        assert excinfo.value.exit_code == 15
        assert "locate" in excinfo.value.message


class TestArmedIsolation:
    """⑩ on_armed fail-closed;armed 后异常吞(fingerprint_note 如实)。"""

    def test_on_armed_failure_is_fail_closed(self, harness: FakeHarness) -> None:
        """on_armed 抛 OSError → 上抛包装 exit 15 族;无回车;armed 未置位
        (CLI 可 rollback);指纹未落。"""

        def broken_armed() -> None:
            raise OSError("disk full")

        with pytest.raises(BridgeError) as excinfo:
            _run(harness, on_armed=broken_armed)
        assert excinfo.value.exit_code == 15
        assert "on_armed" in excinfo.value.message
        assert harness.return_keys() == []  # 未回车
        assert harness.sent_returns == 0

    def test_armed_then_on_receipt_green_raises_is_swallowed(
        self, harness: FakeHarness
    ) -> None:
        """armed 后 on_receipt_green 抛 → 吞 + fingerprint_note 如实
        (防重窗仍以 pending 有效)。"""
        harness.install_monkey = None

        def broken_green() -> None:
            raise OSError("state file gone")

        payload = _run(
            harness, on_armed=harness.on_armed,
            on_receipt_green=broken_green, receipt_query=harness.receipt_query,
        )
        send = payload["send"]
        assert send["sent"] is True  # 发出不抛
        assert send["fingerprint_note"] is not None
        assert "pending" in send["fingerprint_note"]

    def test_armed_then_internal_exception_swallowed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """armed 后内部异常(清空轮询原语炸)→ 兜底吞 + post_send_note。"""
        harness = FakeHarness()
        harness.install(monkeypatch)

        def boom(window, channel) -> bool:
            raise RuntimeError("unexpected")

        monkeypatch.setattr(sendui, "_wait_composer_cleared", boom)
        payload = _run(harness, on_armed=harness.on_armed)
        send = payload["send"]
        assert send["sent"] is True
        assert send["post_send_verified"] is False
        assert "内部异常" in send["post_send_note"]

    def test_mixed_attempts_armed_ever_carries_pending_note(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """条5 回归锁:尝试1 armed 后聚焦败 + 尝试2 导航前(activate)败的
        混合场景——终败 message 仍带 pending 注记(armed_ever 在循环内
        并集,不再只反映末次尝试)。"""
        harness = FakeHarness(channel="ax")
        harness.install(monkeypatch)
        attempts = {"n": 0}
        real_activate = harness._activate

        def staged_activate() -> None:
            attempts["n"] += 1
            if attempts["n"] >= 2:
                raise BridgeError(15, "发送断言超时(阶段=activate,6s 内未达成)")
            real_activate()

        def lose_body_focus() -> bool:
            harness.composer = ""  # 聚焦动作把正文搞丢
            return True

        monkeypatch.setattr(sendui, "activate_wechat", staged_activate)
        monkeypatch.setattr(axui, "focus_input", lose_body_focus)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness, on_armed=harness.on_armed)
        assert excinfo.value.exit_code == 15
        assert "pending" in excinfo.value.message  # 尝试1 armed 过 → 注记必须在
        assert harness.armed_calls == 1  # 仅尝试1 到达 on_armed
        assert harness.return_keys() == []


class TestFocusAssertion:
    """⑪ 聚焦断言两通道对称(§D-2/§J-17)。"""

    def test_ax_focus_input_false_signals_capability_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """AX 路 focus_input 返回 False = AX 能力缺失信号(§D-1)——下一
        尝试 forced_fallback(整链行为见 TestCrossAttemptFallback);本用例
        锁单元语义:抛 _AxCapabilityMissing,不抛 BridgeError、无回车。"""
        harness = FakeHarness(channel="ax")
        harness.install(monkeypatch)
        monkeypatch.setattr(axui, "focus_input", lambda: False)
        with pytest.raises(sendui._AxCapabilityMissing) as excinfo:
            sendui._assert_focused(BODY, harness.window, "ax")
        assert excinfo.value.primitive == "focus_input"
        assert harness.return_keys() == []

    def test_ax_focus_lost_body_terminal_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """AX 聚焦后复读正文丢失(非能力缺失)→ 重试耗尽 → **exit 15 error
        载荷**:stage=focus + 「未回车;指纹已 pending,120s 内同指纹重发
        将 exit 17」注记(§J-20,不破 exit 0 ⇒ sent:true)。"""
        harness = FakeHarness(channel="ax")
        harness.install(monkeypatch)

        def bad_focus() -> bool:
            harness.focus = "other"  # 聚焦动作把正文搞丢的形态
            harness.composer = ""
            return True

        monkeypatch.setattr(axui, "focus_input", bad_focus)
        with pytest.raises(BridgeError) as excinfo:
            _run(harness, on_armed=harness.on_armed)
        assert excinfo.value.exit_code == 15
        assert "focus" in excinfo.value.message
        assert "pending" in excinfo.value.message  # §J-20 注记
        assert harness.return_keys() == []
        assert harness.armed_calls >= 1  # armed 过(每尝试落 pending)

    def test_fallback_sentinel_mismatch_is_focus_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """降级链:composer 点击后哨兵读回异值 → focus 失败(焦点落别处,
        §J-17:哨兵读协议本身即聚焦断言,不是裸点击)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        monkeypatch.setattr(
            sendui, "read_composer_via_clipboard", lambda window: "别处的内容"
        )
        with pytest.raises(sendui._FocusFail):
            sendui._assert_focused(BODY, harness.window, "cgevent_ocr")

    def test_fallback_sentinel_body_passes_empty_is_focus_failure(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """降级链聚焦判据(质询修正后):哨兵读 ==body → 聚焦成立;**回 None/
        空 = 正文已丢失 → _FocusFail**(发送前空 ≠ 聚焦成立,与 ax 路对称,
        绝不在空 composer 上回车)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        got = {"value": harness.composer or None}
        monkeypatch.setattr(
            sendui, "read_composer_via_clipboard", lambda window: got["value"]
        )
        # ==body 形态:聚焦成立(默认全绿路径也覆盖此形态,此处直锁判据)
        got["value"] = BODY
        sendui._assert_focused(BODY, harness.window, "cgevent_ocr")  # 不抛
        # None 形态:正文丢失 → focus 失败
        got["value"] = None
        with pytest.raises(sendui._FocusFail):
            sendui._assert_focused(BODY, harness.window, "cgevent_ocr")
        # 空串形态:同 None
        got["value"] = ""
        with pytest.raises(sendui._FocusFail):
            sendui._assert_focused(BODY, harness.window, "cgevent_ocr")

    def test_fallback_empty_composer_never_reaches_return(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """全链形态:发送前哨兵读回空(正文丢失)→ 重试耗尽 exit 15,
        **零回车**(质询实证场景的回归锁)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        monkeypatch.setattr(
            sendui, "read_composer_via_clipboard", lambda window: None
        )
        with pytest.raises(BridgeError) as excinfo:
            _run(harness, on_armed=harness.on_armed)
        assert excinfo.value.exit_code == 15
        assert "focus" in excinfo.value.message
        assert harness.return_keys() == []  # 空 composer 上绝不回车
        assert harness.sent_returns == 0


class TestSearchTermDirectWrite:
    """0.8.1:降级链搜索词 AXFocusedUIElement 直写优先(REF 对齐,
    /tmp/wxsend-e2e/ 实证 CGEvent Cmd+V 可能静默丢)。"""

    def test_fallback_search_term_direct_write_skips_clipboard(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """write_search_value 可用 → 搜索词零剪贴板、无 Cmd+V(键序少一路,
        搜索词经系统级焦点查询直写)。"""
        harness = FakeHarness(ax_search_write=True)
        harness.install(monkeypatch)
        payload = _run(harness, on_armed=harness.on_armed)
        assert payload["send"]["sent"] is True
        assert "filehelper" not in harness.clip_sets  # 搜索词未走剪贴板
        assert (sendui.KEY_F, sendui.FLAG_COMMAND) in harness.keys  # Cmd+F 仍在
        # 搜索段无 Cmd+V(正文粘贴的 Cmd+V 仍在——那是写正文)
        assert harness.clip_sets.count(BODY) >= 1

    def test_fallback_search_term_falls_back_to_clipboard(
        self, harness: FakeHarness
    ) -> None:
        """write_search_value 不可用(默认)→ 剪贴板 + Cmd+V 兜底(旧行为)。"""
        payload = _run(harness, on_armed=harness.on_armed)
        assert payload["send"]["sent"] is True
        assert "filehelper" in harness.clip_sets
        assert (sendui.KEY_V, sendui.FLAG_COMMAND) in harness.keys


class TestKeystrokeDualEngine:
    """0.8.1:非发送键 = System Events keystroke 优先(失败可检测)/
    CGEvent 兜底;发送回车恒 CGEvent 单路。"""

    def test_stevents_script_shape_and_flags(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """keystroke 脚本形状:key code N [using command down];其它旗标
        组合 False(回落 CGEvent 由调用方处理)。"""
        import subprocess as sp

        seen: dict = {}

        def fake_run(argv: list[str]) -> sp.CompletedProcess:
            seen["argv"] = argv
            return sp.CompletedProcess(args=[], returncode=0, stdout=b"", stderr=b"")

        monkeypatch.setattr(sendui, "_run", fake_run)
        assert sendui.post_key_stevents(sendui.KEY_F, sendui.FLAG_COMMAND) is True
        assert seen["argv"][1:3] == ["-e", 'tell application "System Events" to key code 3 using command down']
        assert sendui.post_key_stevents(sendui.KEY_RETURN) is True
        assert "using" not in seen["argv"][2]
        assert sendui.post_key_stevents(sendui.KEY_F, flags=0x0200) is False  # 非支持旗标

        def failing_run(argv: list[str]) -> sp.CompletedProcess:
            return sp.CompletedProcess(args=[], returncode=1, stdout=b"", stderr=b"not allowed")

        monkeypatch.setattr(sendui, "_run", failing_run)
        assert sendui.post_key_stevents(sendui.KEY_A, sendui.FLAG_COMMAND) is False

    def test_dual_engine_falls_back_to_cgevent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """keystroke False → post_key(CGEvent)兜底;True → post_key 不被调。"""
        calls: list[tuple] = []
        monkeypatch.setattr(sendui, "post_key_stevents", lambda k, f=0: False)
        monkeypatch.setattr(sendui, "post_key", lambda k, f=0: calls.append((k, f)))
        sendui._post_key_dual(sendui.KEY_F, sendui.FLAG_COMMAND)
        assert calls == [(sendui.KEY_F, sendui.FLAG_COMMAND)]
        calls.clear()
        monkeypatch.setattr(sendui, "post_key_stevents", lambda k, f=0: True)
        sendui._post_key_dual(sendui.KEY_A, sendui.FLAG_COMMAND)
        assert calls == []  # keystroke 已注入,CGEvent 不重复


class TestCrossAttemptFallback:
    """跨尝试降级(§D-1):AX 能力缺失 → 下一尝试 forced_fallback。"""

    def test_ax_primitive_missing_falls_back_next_attempt(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness(channel="ax")
        harness.install(monkeypatch)
        attempts = {"n": 0}
        real_write = harness._ax_write_search

        def flaky_write(term: str) -> bool:
            attempts["n"] += 1
            if attempts["n"] <= 1:
                return False  # 首试 AX 写失败 → 能力缺失
            return real_write(term)

        monkeypatch.setattr(axui, "write_search_value", flaky_write)
        payload = _run(harness, on_armed=harness.on_armed)
        send = payload["send"]
        assert send["attempts"] == 2
        # 第二尝试不再 probe,直接降级链(channel 如实)
        assert send["channel"] == "cgevent_ocr"


class TestReceiptPolling:
    """⑫ 回执轮询按 RECEIPT_POLL_SCHEDULE 退避(假钟推进断言时序)。"""

    def test_poll_backoff_shape_and_since_epoch(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """首查未见 → 按 (5,10,15)s 退避重查;since_epoch = on_armed 时刻
        (wall_clock 注入)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        wall_values: list[float] = []

        def fake_wall() -> float:
            return 1700000000.0

        monkeypatch.setattr(sendui, "wall_clock", fake_wall)
        verdicts = iter([False, False, True])  # 第 3 次查询才见
        since_seen: list[float] = []

        def receipt(username: str, body: str, since_epoch: float) -> bool:
            since_seen.append(since_epoch)
            return next(verdicts)

        payload = _run(harness, on_armed=harness.on_armed, receipt_query=receipt)
        assert payload["send"]["localdb_receipt"] is True
        assert since_seen == [1700000000.0] * 3  # since_epoch 恒为 armed 时刻
        # 退避形态:sleeps 里恰出现 (5.0, 10.0) 两个 gap(第 3 次命中,15 不等)
        gaps = [s for s in harness.sleeps if s in sendui.RECEIPT_POLL_SCHEDULE]
        assert gaps == [5.0, 10.0]

    def test_poll_all_miss_returns_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness()
        harness.install(monkeypatch)
        calls = {"n": 0}

        def receipt(username, body, since_epoch):
            calls["n"] += 1
            return False

        payload = _run(harness, on_armed=harness.on_armed, receipt_query=receipt)
        assert payload["send"]["localdb_receipt"] is False
        assert calls["n"] == 4  # 首 + 3 退避
        gaps = [s for s in harness.sleeps if s in sendui.RECEIPT_POLL_SCHEDULE]
        assert gaps == [5.0, 10.0, 15.0]

    def test_poll_chain_error_returns_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """链挂(BridgeError)→ None 如实(不算失败也不算成功)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)

        def broken(username, body, since_epoch):
            raise BridgeError(20, "db_not_found(注入)")
            return False  # pragma: no cover

        payload = _run(harness, on_armed=harness.on_armed, receipt_query=broken)
        assert payload["send"]["localdb_receipt"] is None
        assert harness.green_calls == 0

    def test_no_receipt_query_returns_none(self, harness: FakeHarness) -> None:
        payload = _run(harness, on_armed=harness.on_armed)
        assert payload["send"]["localdb_receipt"] is None


class TestCGEventSource:
    """⑨ CGEvent 事件源:键盘/鼠标事件均带 combinedSessionState 句柄。"""

    def test_post_key_and_click_use_cached_source(self, monkeypatch: pytest.MonkeyPatch) -> None:
        class FakeLib:
            def __init__(self) -> None:
                self.calls: list[tuple] = []

            def CGEventSourceCreate(self, state: int) -> int:
                self.calls.append(("source", state))
                return 999

            def CGEventCreateKeyboardEvent(self, src, key, down):
                self.calls.append(("key", src, key, down))
                return 1

            def CGEventCreateMouseEvent(self, src, event_type, point, button):
                self.calls.append(("mouse", src, event_type, point.x, point.y))
                return 1

            def CGEventSetFlags(self, event, flags):
                pass

            def CGEventPost(self, tap, event):
                pass

        fake = FakeLib()
        monkeypatch.setattr(sendui, "_coregraphics", lambda: fake)
        monkeypatch.setattr(sendui, "_EVENT_SOURCE", None)
        monkeypatch.setattr(sendui, "_event_source_tried", False)
        monkeypatch.setattr(sendui, "sleep", lambda _s: None)
        monkeypatch.setattr(sendui, "_release", lambda _e: None)
        sendui.post_key(sendui.KEY_A, sendui.FLAG_COMMAND)
        sendui.click_at(300, 400)
        kinds = {(c[0], c[1]) for c in fake.calls}
        assert ("source", sendui.EVENT_SOURCE_COMBINED) in fake.calls
        assert ("key", 999) in kinds  # 键盘事件带源句柄
        assert ("mouse", 999) in kinds  # 鼠标事件同源
        mouse = [c for c in fake.calls if c[0] == "mouse"]
        assert mouse[-1][3:] == (300.0, 400.0)  # moved→down→up 三事件同点


class TestTextConfirmed:
    """回读对账纯函数(空白不敏感;长正文首尾段)——0.7.0 用例原样保留。"""

    def test_exact_after_whitespace_squash(self) -> None:
        assert sendui.text_confirmed("hello 世 界\n", "hello 世界") is True

    def test_missing_body_is_false(self) -> None:
        assert sendui.text_confirmed("完全无关", BODY) is False

    def test_empty_body_never_confirms(self) -> None:
        assert sendui.text_confirmed("任意", "") is False

    def test_long_body_head_tail_rule(self) -> None:
        long_body = "头" * 100 + "中段可能滚出可视区" + "尾" * 100
        visible = "头" * 100 + "尾" * 100  # 中段不可见
        assert sendui.text_confirmed(visible, long_body) is True
        assert sendui.text_confirmed("头" * 100, long_body) is False  # 缺尾段

    def test_short_body_requires_full(self) -> None:
        assert sendui.text_confirmed("正文片段", "正文") is True
        assert sendui.text_confirmed("正", "正文") is False
