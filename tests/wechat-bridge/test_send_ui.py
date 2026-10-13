"""send_text 热激活 UI 驱动单测(wxauto 三支柱;全 mock,零真实系统调用)。

设计纪律(design §8 同款):sendui 平台原语(激活/前台/键盘/剪贴板/AX/
截窗 OCR)全部是模块级注入点,本文件以 :class:`FakeHarness` 整组替换;
时钟(:data:`sendui.monotonic`)换计数器(每次 +1s)——等待环有界可终止,
单测不真等。真机冒烟走 ``MYIA_WECHAT_E2E=1`` 门控(下一阶段)。

三支柱的受测面:

① 焦点/状态断言 —— 前台断言失败/定位超时/窗口缺位 → exit 15;
② 粘后回读确认 —— 剪贴板对账 + AX value 精确路 + OCR 输入带兜底路;
③ 超时报错绝不假成功 —— 断言失败重试上限 3 后 exit 15/30,**回车只在
   回读确认后按下**(键序断言:全败路径的末键必是粘贴,绝不是回车)。

G6 接线(CLI 级):成功 → 占位生效(10s 内二发 exit 14);失败 →
rollback(10s 内重试不被 14 拦——失败不吞重试窗口)。
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import pytest

import wechat_bridge.sendui as sendui
from wechat_bridge.codes import (
    EXIT_OK,
    SEND_AX_FOCUS_REQUIRED,
    TIMEOUT,
    BridgeError,
)
from wechat_bridge.config import BridgeConfig

from bridge_testkit import CheckMocks, run_cli, tray_mocks

CHAT = "文件传输助手"
BODY = "桥发冒烟正文 hello 42"


class FakeHarness:
    """sendui 平台原语的进程内替身(键序/剪贴板全程留痕)。"""

    def __init__(
        self,
        *,
        frontmost: bool = True,
        window: object | None = object(),
        ax_value: str | None = None,
        ocr_texts: dict[str, str] | None = None,
        clipboard_corrupt: bool = False,
        activate_raises: BridgeError | None = None,
        ocr_raises: dict[str, BridgeError] | None = None,
    ) -> None:
        self.keys: list[tuple[int, int]] = []
        self.clip_sets: list[str] = []
        self.clip: str | None = None
        self.ocr_calls: list[str] = []
        self.ocr_texts = {
            "title": CHAT,
            "input": BODY,
            "sent": BODY,
            **(ocr_texts or {}),
        }
        self.frontmost = frontmost
        self.window = window
        self.ax_value = ax_value
        self.clipboard_corrupt = clipboard_corrupt
        self.activate_raises = activate_raises
        self.ocr_raises = ocr_raises or {}
        self._clock = itertools.count(1)

    # ------------------------------------------------------------ 装配 ----
    def install(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sendui, "monotonic", lambda: float(next(self._clock)))
        monkeypatch.setattr(sendui, "sleep", lambda _s: None)
        monkeypatch.setattr(sendui, "activate_wechat", self._activate)
        monkeypatch.setattr(sendui, "frontmost_is_wechat", lambda: self.frontmost)
        monkeypatch.setattr(sendui, "post_key", self._post_key)
        monkeypatch.setattr(sendui, "set_clipboard_text", self._set_clip)
        monkeypatch.setattr(sendui, "clipboard_text", self._get_clip)
        monkeypatch.setattr(sendui, "ax_focused_value", lambda: self.ax_value)
        monkeypatch.setattr(sendui, "_ocr_region", self._ocr_region)
        monkeypatch.setattr(sendui, "_find_window", lambda: self.window)

    # ------------------------------------------------------------ 原语 ----
    def _activate(self) -> None:
        if self.activate_raises is not None:
            raise self.activate_raises

    def _post_key(self, key_code: int, flags: int = 0) -> None:
        self.keys.append((key_code, flags))

    def _set_clip(self, text: str) -> None:
        self.clip_sets.append(text)
        self.clip = text

    def _get_clip(self) -> str | None:
        if self.clipboard_corrupt and self.clip == BODY:
            return "别的进程改了剪贴板"
        return self.clip

    def _ocr_region(self, _window, _box, _workdir, tag: str) -> str:
        self.ocr_calls.append(tag)
        if tag in self.ocr_raises:
            raise self.ocr_raises[tag]
        return self.ocr_texts.get(tag, "")

    # ------------------------------------------------------------ 断言面 ----
    def send_returns(self) -> list[tuple[int, int]]:
        """全部回车键事件(搜索回车 + 发送回车同码,按位置区分)。"""
        return [key for key in self.keys if key[0] == sendui.KEY_RETURN]

    def body_pasted(self) -> bool:
        return BODY in self.clip_sets


@pytest.fixture()
def harness(monkeypatch: pytest.MonkeyPatch) -> FakeHarness:
    fake = FakeHarness()
    fake.install(monkeypatch)
    return fake


class TestThreePillars:
    """wxauto 三支柱:断言、回读、绝不假成功。"""

    def test_happy_path_ocr_readback(self, harness: FakeHarness) -> None:
        """AX 不可用 → OCR 输入带回读;成功载荷形状 + 末键=回车 flags=0。"""
        payload = sendui.send_text(BridgeConfig(), CHAT, BODY)
        send = payload["send"]
        assert send["sent"] is True
        assert send["attempts"] == 1
        assert send["readback"] == "ocr_strip"
        assert send["post_send_verified"] is True
        assert send["post_send_note"] is None
        assert send["chat"] == CHAT
        assert isinstance(send["elapsed_ms"], int)
        assert harness.keys[-1] == (sendui.KEY_RETURN, 0)  # 确认后才回车,flags=0
        assert BODY in harness.clip_sets  # 正文走过剪贴板
        assert harness.clip_sets[-1] == ""  # 原剪贴板为空 → 复原=清空,不留正文
        assert "input" in harness.ocr_calls and "title" in harness.ocr_calls

    def test_happy_path_ax_value_exact_readback(self, harness: FakeHarness) -> None:
        """AX 焦点 value 可用 → 精确路;OCR 输入带不启用。"""
        harness.ax_value = BODY
        payload = sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert payload["send"]["readback"] == "ax_value"
        assert "input" not in harness.ocr_calls

    def test_payload_never_carries_body(self, harness: FakeHarness) -> None:
        """红线 6:载荷只载形状与通路,永不载正文。"""
        payload = sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert BODY not in json.dumps(payload, ensure_ascii=False)

    def test_transient_readback_miss_absorbed_by_poll(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """瞬态 OCR 漏读由回读轮询环吸收(同尝试内恢复)→ attempts=1。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        original = harness._ocr_region
        calls = {"input": 0}

        def flaky(_window, _box, _workdir, tag):
            if tag == "input":
                calls["input"] += 1
                if calls["input"] == 1:
                    return ""  # 首次漏读 → 轮询环内恢复
            return original(_window, _box, _workdir, tag)

        monkeypatch.setattr(sendui, "_ocr_region", flaky)
        payload = sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert calls["input"] >= 2
        assert payload["send"]["attempts"] == 1
        assert payload["send"]["sent"] is True
        assert harness.keys[-1] == (sendui.KEY_RETURN, 0)

    def test_attempt_level_retry_after_locate_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """整尝试级重试:首试定位超时(标题带全败)→ 退避后二试成功 →
        attempts=2(重试由 RETRY_BACKOFF_S 睡眠分隔,睡眠桩兼作尝试边界哨兵)。"""
        harness = FakeHarness()
        harness.install(monkeypatch)
        original = harness._ocr_region
        failed_attempts = {"n": 0}

        def spy_sleep(seconds: float) -> None:
            if seconds == sendui.RETRY_BACKOFF_S:
                failed_attempts["n"] += 1  # 尝试边界:退避=一次整尝试失败

        def title_stuck(_window, _box, _workdir, tag):
            if tag == "title" and failed_attempts["n"] == 0:
                return "别的会话"  # 首试整个定位窗口内都不匹配
            return original(_window, _box, _workdir, tag)

        monkeypatch.setattr(sendui, "sleep", spy_sleep)
        monkeypatch.setattr(sendui, "_ocr_region", title_stuck)
        payload = sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert payload["send"]["attempts"] == 2
        assert payload["send"]["sent"] is True
        assert harness.keys[-1] == (sendui.KEY_RETURN, 0)

    def test_all_attempts_fail_raises_15_and_never_enters(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """支柱③:3 次尝试回读全败 → exit 15;**发送回车绝不发出**。

        键序判据:每尝试恰一个搜索回车(3 尝试=3 个 Return),末键=正文
        粘贴(Cmd+V)——粘贴之后无任何键,回车未按下。
        """
        harness = FakeHarness(ocr_texts={"input": "", "sent": BODY})
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert excinfo.value.exit_code == SEND_AX_FOCUS_REQUIRED == 15
        assert "readback" in excinfo.value.message
        assert "3" in excinfo.value.message
        assert len(harness.send_returns()) == 3  # 全部是搜索回车
        assert harness.keys[-1] == (sendui.KEY_V, sendui.FLAG_COMMAND)  # 末键=粘贴,非回车
        assert harness.body_pasted()

    def test_activate_timeout_raises_15_stage_activate(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """支柱①:前台断言永不成立 → 超时 exit 15(阶段=activate),零键入。"""
        harness = FakeHarness(frontmost=False)
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert excinfo.value.exit_code == 15
        assert "activate" in excinfo.value.message
        assert harness.keys == []

    def test_locate_mismatch_raises_15(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """支柱①:标题带与请求会话不符(定位未达)→ exit 15(阶段=locate)。

        键序判据:末键=搜索回车(定位流最后一步),粘贴(及发送回车)未达。
        """
        harness = FakeHarness(ocr_texts={"title": "别的会话", "input": BODY})
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert excinfo.value.exit_code == 15
        assert "locate" in excinfo.value.message
        assert harness.keys[-1] == (sendui.KEY_RETURN, 0)  # 搜索回车是末键=未进入粘贴
        assert BODY not in harness.clip_sets  # 正文从未进剪贴板

    def test_window_missing_raises_15(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """前置门放行后窗口消失 → exit 15(阶段=window)。"""
        harness = FakeHarness(window=None)
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert excinfo.value.exit_code == 15
        assert "window" in excinfo.value.message

    def test_clipboard_corruption_raises_15(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """支柱②第一腿:粘贴后剪贴板读回与正文不符 → exit 15(阶段=clipboard)。"""
        harness = FakeHarness(clipboard_corrupt=True)
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert excinfo.value.exit_code == 15
        assert "clipboard" in excinfo.value.message
        assert harness.keys[-1] == (sendui.KEY_V, sendui.FLAG_COMMAND)  # 未回车

    def test_subprocess_timeout_propagates_30(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """子进程挂起族:激活原语抛 exit 30 → 3 次尝试后原码透传(不吞成 15)。"""
        harness = FakeHarness(
            activate_raises=BridgeError(TIMEOUT, "平台子进程超时(osascript…)", fix_hint="重试")
        )
        harness.install(monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert excinfo.value.exit_code == TIMEOUT == 30


class TestPostSendVerdict:
    """发送后回读:绝不抛错(ax.py 契约/G6 方向),结果如实入载荷。"""

    def test_message_area_unseen_reports_honestly(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness(ocr_texts={"sent": ""})
        harness.install(monkeypatch)
        payload = sendui.send_text(BridgeConfig(), CHAT, BODY)  # 不抛
        send = payload["send"]
        assert send["sent"] is True
        assert send["post_send_verified"] is False
        assert isinstance(send["post_send_note"], str) and send["post_send_note"]
        assert harness.keys[-1] == (sendui.KEY_RETURN, 0)

    def test_message_area_ocr_failure_swallowed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        capture_error = BridgeError(1, "截窗失败", code="screen_capture_failed")
        harness = FakeHarness(ocr_raises={"sent": capture_error})
        harness.install(monkeypatch)
        payload = sendui.send_text(BridgeConfig(), CHAT, BODY)  # 不抛
        assert payload["send"]["post_send_verified"] is False
        assert "screen_capture_failed" in payload["send"]["post_send_note"]

    def test_clipboard_restored_when_original_present(self, monkeypatch: pytest.MonkeyPatch) -> None:
        harness = FakeHarness()
        harness.install(monkeypatch)
        harness.clip = "主人原来的剪贴板"  # 发送前已有内容
        sendui.send_text(BridgeConfig(), CHAT, BODY)
        assert harness.clip_sets[-1] == "主人原来的剪贴板"


class TestTextConfirmed:
    """回读对账纯函数(空白不敏感;长正文首尾段)。"""

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


class TestG6WiringAtCli:
    """G6 频控与占位还原的 CLI 级接线(driver 整体 mock,时间注入)。"""

    def test_success_stamps_rate_window(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """成功发送后 10s 内二发 → exit 14(占位生效,G6 硬间隔;时钟注入)。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))
        monkeypatch.setattr(
            "wechat_bridge.sendui.send_text",
            lambda config, chat_id, body: {
                "send": {"chat": chat_id, "sent": True, "attempts": 1,
                         "readback": "ocr_strip", "post_send_verified": True,
                         "post_send_note": None, "elapsed_ms": 1}
            },
        )
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1000.0)
        exit_code, payload = run_cli(
            ["send_text", CHAT, "--file", "-"], monkeypatch, tmp_path, stdin_text=BODY
        )
        assert exit_code == EXIT_OK == 0
        assert payload["send"]["sent"] is True
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1007.0)  # +7s:<10s
        exit2, payload2 = run_cli(
            ["send_text", CHAT, "--file", "-"], monkeypatch, tmp_path, stdin_text=BODY
        )
        assert exit2 == 14
        assert payload2["error"]["retry_after_seconds"] == pytest.approx(3.0)

    def test_failure_rolls_back_rate_window(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """失败(未发出)→ rollback:10s 内重试不被 14 拦(不吞重试窗口)。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))
        calls = {"n": 0}

        def failing_send(config, chat_id, body):
            calls["n"] += 1
            raise BridgeError(
                SEND_AX_FOCUS_REQUIRED, "发送断言失败(阶段=readback)", fix_hint="重试"
            )

        monkeypatch.setattr("wechat_bridge.sendui.send_text", failing_send)
        exit_code, payload = run_cli(
            ["send_text", CHAT, "--file", "-"], monkeypatch, tmp_path, stdin_text=BODY
        )
        assert exit_code == 15
        assert payload["error"]["code"] == "send_ax_focus_required"
        # 立即重试(间隔≈0):未发出 → 占位已还原 → 放行(再败同码,而非 14)
        exit2, payload2 = run_cli(
            ["send_text", CHAT, "--file", "-"], monkeypatch, tmp_path, stdin_text=BODY
        )
        assert calls["n"] == 2
        assert exit2 == 15
