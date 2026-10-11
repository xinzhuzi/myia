"""像素读层单测(Phase C1/C2;全 mock/合成,零真实系统调用,CI 全绿)。

真机链(Vision/截窗/VL)一律 ``MYIA_WECHAT_E2E=1`` 门控,见本文件末尾
TestRealPixelChain(design §8 纪律:严禁真客户端测试裸进 pytest 全量)。
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import bridge_testkit
from bridge_testkit import run_cli
from pixel_fixture import SESSIONS, render
from wechat_bridge import pixel
from wechat_bridge.codes import BridgeError
from wechat_bridge.config import BridgeConfig

FIXTURE_PNG = Path(__file__).resolve().parent / "fixtures" / "synthetic_wechat_panel.png"


def _line(text: str, conf: float, x: float, y: float, w: float = 0.05, h: float = 0.013):
    return pixel.OcrLine(text=text, conf=conf, x=x, y=y, w=w, h=h)


def _synthetic_session_lines() -> list:
    """按 fixture 真值几何直接构造 OCR 行(不依赖 PNG 与 Vision;纯函数面)。

    8 行会话:3 行带时间锚(其一含数字徽标、其一 999+),2 行时间被「漏读」
    (趟 2 对组恢复目标),外加聊天区噪声行(居中时间/左气泡/发送者/右气泡,
    不得污染会话解析)。
    """
    lines: list = []
    y0, pitch = 0.086, 0.059
    for index, (name, when, unread, preview) in enumerate(SESSIONS):
        y = y0 + index * pitch
        lines.append(_line(name, 1.0, 0.060, y))
        lines.append(_line(preview, 1.0, 0.060, y + 0.018))
        if when:
            lines.append(_line(when, 1.0, 0.229 - 0.045, y, w=0.045))
        if unread is not None:
            lines.append(_line(str(unread), 0.9, 0.215, y + 0.020, w=0.014))
    # 聊天区噪声(标题带 + 居中时间 + 左气泡 + 发送者 + 右气泡)
    lines.append(_line("合成会话甲", 1.0, 0.44, 0.041))  # 聊天标题
    lines.append(_line("14:20", 1.0, 0.58, 0.16))  # 居中时间(非会话时间列)
    lines.append(_line("合成同事", 1.0, 0.243, 0.244))  # 发送者
    lines.append(_line("合成消息:气泡文本", 1.0, 0.243, 0.271))  # 左气泡
    lines.append(_line("自己发送的合成消息", 1.0, 0.80, 0.31))  # 右气泡
    return lines


class TestFindMainWindow:
    def _reader(self, rows: list[dict]):
        return lambda: rows

    def test_prefers_onscreen_then_largest(self) -> None:
        rows = [
            {"kCGWindowOwnerName": "微信", "kCGWindowLayer": 0, "kCGWindowNumber": 1,
             "kCGWindowIsOnscreen": False, "kCGWindowBounds": {"Width": 1920, "Height": 1050},
             "kCGWindowOwnerPID": 100},
            {"kCGWindowOwnerName": "微信", "kCGWindowLayer": 0, "kCGWindowNumber": 2,
             "kCGWindowIsOnscreen": False, "kCGWindowBounds": {"Width": 700, "Height": 640}},
            {"kCGWindowOwnerName": "微信", "kCGWindowLayer": 3, "kCGWindowNumber": 3,
             "kCGWindowIsOnscreen": True, "kCGWindowBounds": {"Width": 1920, "Height": 1050}},
        ]
        info = pixel.find_main_window(window_list_reader=self._reader(rows))
        assert info is not None and info.window_id == 1  # layer 3 被滤;剩余面积最大者

    def test_accepts_english_owner_name(self) -> None:
        rows = [
            {"kCGWindowOwnerName": "WeChat", "kCGWindowLayer": 0, "kCGWindowNumber": 9,
             "kCGWindowIsOnscreen": True, "kCGWindowBounds": {"Width": 800, "Height": 600}},
        ]
        info = pixel.find_main_window(window_list_reader=self._reader(rows))
        assert info is not None and info.window_id == 9 and info.onscreen is True

    def test_no_window_returns_none(self) -> None:
        assert pixel.find_main_window(window_list_reader=self._reader([])) is None


class TestCaptureWindow:
    def test_failure_exit_nonzero_raises(self, tmp_path: Path) -> None:
        def runner(*args, **kwargs):
            return subprocess.CompletedProcess(args, returncode=7, stdout=b"", stderr=b"err")

        with pytest.raises(BridgeError) as excinfo:
            pixel.capture_window(
                pixel.WindowInfo(1, True, 100, 100), tmp_path / "w.png", runner=runner
            )
        assert excinfo.value.name == "screen_capture_failed"

    def test_black_image_raises_black(self, tmp_path: Path) -> None:
        from PIL import Image

        out = tmp_path / "w.png"
        Image.new("RGB", (200, 100), (2, 2, 2)).save(out)

        def runner(*args, **kwargs):
            return subprocess.CompletedProcess(args, returncode=0, stdout=b"", stderr=b"")

        with pytest.raises(BridgeError) as excinfo:
            pixel.capture_window(
                pixel.WindowInfo(1, True, 100, 100), out, runner=runner
            )
        assert excinfo.value.name == "screen_capture_black"
        assert "屏幕录制" in (excinfo.value.fix_hint or "")

    def test_timeout_maps_to_exit_30(self, tmp_path: Path) -> None:
        def runner(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd="screencapture", timeout=15)

        with pytest.raises(BridgeError) as excinfo:
            pixel.capture_window(
                pixel.WindowInfo(1, True, 100, 100), tmp_path / "w.png", runner=runner
            )
        assert excinfo.value.exit_code == 30

    def test_real_content_image_reports_ok(self, tmp_path: Path) -> None:
        out = tmp_path / "w.png"
        render(out)

        def runner(*args, **kwargs):
            return subprocess.CompletedProcess(args, returncode=0, stdout=b"", stderr=b"")

        result = pixel.capture_window(
            pixel.WindowInfo(1, True, 1920, 1050), out, runner=runner
        )
        assert result["state"] == "ok"
        assert result["mean_luma"] > pixel.BLACK_MEAN_MAX


class TestParseSessions:
    def test_two_pass_assembly_matches_ground_truth(self) -> None:
        rows, meta = pixel.parse_sessions(_synthetic_session_lines(), limit=20)
        truth_names = [s[0] for s in SESSIONS]
        assert [row.name for row in rows] == truth_names  # 8/8,顺序=窗口自上而下
        assert meta["rows"] == len(SESSIONS)
        assert meta["with_time"] == sum(1 for s in SESSIONS if s[1])
        # 聊天区噪声不得成行
        assert all(row.name not in ("合成消息:气泡文本", "自己发送的合成消息") for row in rows)

    def test_unread_badges_parsed(self) -> None:
        rows, _ = pixel.parse_sessions(_synthetic_session_lines(), limit=20)
        truth = {s[0]: s[2] for s in SESSIONS}
        got = {row.name: row.unread for row in rows}
        assert got["合成会话丙-项目群"] == 999  # "999+" 语义
        assert got["Epsilon群"] == 12
        assert got["SyntheticBeta"] is None

    def test_limit_truncates(self) -> None:
        rows, _ = pixel.parse_sessions(_synthetic_session_lines(), limit=3)
        assert len(rows) == 3

    def test_empty_lines(self) -> None:
        rows, meta = pixel.parse_sessions([], limit=20)
        assert rows == [] and meta["rows"] == 0


class TestParseMessages:
    def _message_lines(self) -> list:
        return [
            _line("合成会话甲", 1.0, 0.44, 0.041),  # 标题带
            _line("14:20", 1.0, 0.47, 0.16),  # 居中时间标记
            _line("合成同事", 1.0, 0.005, 0.20),  # 发送者(短,上方)
            _line("合成消息正文第一行", 1.0, 0.005, 0.23),  # 气泡(dy=0.03)
            _line("续行文本", 1.0, 0.005, 0.26),  # 换行(dy=0.03,同 x → 合并)
            _line("自己发送的合成消息", 1.0, 0.70, 0.33),  # 右侧(自己)
            _line("下一条对方消息", 1.0, 0.005, 0.42),  # 与上行 dy=0.09 → 独立一条
        ]

    def test_markers_senders_wrap_and_sides(self) -> None:
        title, rows, meta = pixel.parse_messages(self._message_lines(), k=10)
        assert title == "合成会话甲"
        assert [row.side for row in rows] == ["left", "right", "left"]
        assert rows[0].sender == "合成同事"
        assert rows[0].ts == "14:20"
        # 换行合并:「…第一行」+「续行文本」
        assert rows[0].text.endswith("续行文本")
        assert rows[2].text == "下一条对方消息"
        assert meta["markers"] == 1

    def test_k_cut_returns_most_recent(self) -> None:
        _, rows, _ = pixel.parse_messages(self._message_lines(), k=2)
        assert len(rows) == 2
        assert rows[-1].text == "下一条对方消息"

    def test_chat_match_normalization(self) -> None:
        assert pixel._chat_match("甲", "合成会话甲") is True
        assert pixel._chat_match("不存在", "合成会话甲") is False
        assert pixel._chat_match("任意", None) is None


class TestVlCorrection:
    def test_correction_applied_line_count_preserved(self) -> None:
        lines = [_line("初稿甲", 0.4, 0.1, 0.1), _line("初稿乙", 0.9, 0.1, 0.2)]
        answer = json.dumps({"choices": [{"message": {"content": json.dumps(
            [{"i": 0, "text": "校正甲"}, {"i": 1, "text": "校正乙"}]
        )}}]})

        def fake_opener(request):
            assert request.full_url.startswith("http://127.0.0.1:8080/v1/chat/completions")
            return json.loads(answer)

        out, meta = pixel.vl_correct_lines(
            FIXTURE_PNG, lines, Path("/tmp"), model_id="m", opener=fake_opener
        )
        assert meta["parsed"] is True
        assert [line.text for line in out] == ["校正甲", "校正乙"]  # 行数/顺序保持
        assert out[0].conf == 0.4  # 置信度/几何不动

    def test_unparsable_answer_keeps_draft(self) -> None:
        lines = [_line("初稿甲", 0.4, 0.1, 0.1)]

        def fake_opener(request):
            return {"choices": [{"message": {"content": "抱歉我不会"}}]}

        out, meta = pixel.vl_correct_lines(
            FIXTURE_PNG, lines, Path("/tmp"), model_id="m", opener=fake_opener
        )
        assert meta["parsed"] is False
        assert out == lines

    def test_vl_unavailable_returns_draft(self) -> None:
        lines = [_line("初稿甲", 0.4, 0.1, 0.1)]

        def failing_opener(request):
            raise ConnectionError("vl service down(注入)")

        out, meta = pixel.vl_correct_lines(
            FIXTURE_PNG, lines, Path("/tmp"), model_id=None, opener=failing_opener
        )
        assert out == lines
        assert meta["parsed"] is False
        assert meta["error"] == "vl_unavailable"


class TestOrchestration:
    def _window(self) -> pixel.WindowInfo:
        return pixel.WindowInfo(window_id=42, onscreen=False, width=1920, height=1050, pid=100)

    def _capture_ok(self, window, out_path):
        from PIL import Image

        Image.new("RGB", (64, 32), (30, 30, 30)).save(out_path)
        return {"state": "ok", "path": str(out_path), "width": 64, "height": 32, "mean_luma": 30.0}

    def _vision_fake(self, lines_by_call: list):
        calls: list[Path] = []

        def vision(image_path: Path):
            calls.append(image_path)
            return "vision", lines_by_call[min(len(calls), len(lines_by_call)) - 1], 0.01

        return vision, calls

    def test_list_sessions_payload_shape_and_cleanup(self, tmp_path: Path) -> None:
        vision, calls = self._vision_fake([_synthetic_session_lines()])
        created: list[Path] = []

        def capturer(window, out_path):
            created.append(out_path.parent)
            return self._capture_ok(window, out_path)

        payload = pixel.list_sessions(
            BridgeConfig(), None,
            window_finder=lambda: self._window(),
            capturer=capturer,
            vision_fn=vision,
            vl_fn=lambda *a, **k: (a[1], {"parsed": False}),
        )
        assert set(payload) >= {"sessions", "count", "window", "capture", "ocr"}
        assert payload["count"] == len(SESSIONS)
        assert payload["window"]["onscreen"] is False
        assert "note" in payload["window"]
        for row in payload["sessions"]:
            assert {"id", "name", "unread", "time", "preview", "conf"} <= set(row)
        assert all(not path.exists() for path in created)  # 私有工作目录用后即清(红线 6)

    def test_list_sessions_without_window_raises(self) -> None:
        with pytest.raises(BridgeError) as excinfo:
            pixel.list_sessions(
                BridgeConfig(), None, window_finder=lambda: None,
                capturer=lambda w, p: {}, vision_fn=lambda p: ("vision", [], 0.0),
            )
        assert excinfo.value.name == "screen_capture_failed"

    def test_read_messages_reports_chat_match(self, tmp_path: Path) -> None:
        lines = _synthetic_session_lines()
        vision, _ = self._vision_fake([lines, lines])
        payload = pixel.read_messages(
            BridgeConfig(), "合成会话甲", 10,
            window_finder=lambda: self._window(),
            capturer=self._capture_ok,
            vision_fn=vision,
            vl_fn=lambda *a, **k: (a[1], {"parsed": False}),
        )
        assert set(payload) >= {"messages", "count", "chat", "window", "capture", "ocr"}
        assert payload["chat"]["match"] is True
        assert payload["chat"]["requested_id"] == "合成会话甲"
        assert payload["messages"], "消息行不得为空"

    def test_read_messages_mismatch_flagged(self) -> None:
        lines = _synthetic_session_lines()
        vision, _ = self._vision_fake([lines, lines])
        payload = pixel.read_messages(
            BridgeConfig(), "完全另一个会话", 10,
            window_finder=lambda: self._window(),
            capturer=self._capture_ok,
            vision_fn=vision,
            vl_fn=lambda *a, **k: (a[1], {"parsed": False}),
        )
        assert payload["chat"]["match"] is False
        assert payload["chat"]["note"]  # 不匹配必须如实声明,不静默张冠李戴


class TestCliWiring:
    def test_sessions_list_emits_contract_payload(self, monkeypatch, tmp_path) -> None:
        bridge_testkit.tray_mocks(monkeypatch, bridge_testkit.CheckMocks(window=True))
        import wechat_bridge.pixel as pixel_mod

        monkeypatch.setattr(
            pixel_mod,
            "list_sessions",
            lambda config, limit: {
                "sessions": [{"id": "合成会话", "name": "合成会话", "unread": None,
                              "time": None, "preview": None, "conf": 1.0}],
                "count": 1,
                "window": {"window_id": 1, "onscreen": True, "width": 1, "height": 1, "note": None},
                "capture": {"state": "ok", "width": 1, "height": 1, "mean_luma": 30.0},
                "ocr": {},
            },
        )
        exit_code, payload = run_cli(["sessions", "list", "--json"], monkeypatch, tmp_path)
        assert exit_code == 0
        assert payload["count"] == 1
        assert payload["sessions"][0]["id"] == "合成会话"

    def test_messages_read_emits_contract_payload(self, monkeypatch, tmp_path) -> None:
        bridge_testkit.tray_mocks(monkeypatch, bridge_testkit.CheckMocks(window=True))
        import wechat_bridge.pixel as pixel_mod

        monkeypatch.setattr(
            pixel_mod,
            "read_messages",
            lambda config, chat_id, k: {
                "messages": [{"ts": None, "sender": None, "type": "text", "text": "合成",
                              "side": "left", "conf": 1.0}],
                "count": 1,
                "chat": {"requested_id": chat_id, "visible_title": chat_id,
                         "match": True, "note": None},
                "window": {"window_id": 1, "onscreen": True, "width": 1, "height": 1, "note": None},
                "capture": {"state": "ok", "width": 1, "height": 1, "mean_luma": 30.0},
                "ocr": {},
            },
        )
        exit_code, payload = run_cli(["messages", "read", "合成会话", "-k", "5", "--json"],
                                     monkeypatch, tmp_path)
        assert exit_code == 0
        assert payload["chat"]["match"] is True
        assert payload["messages"][0]["type"] == "text"

    def test_window_closed_still_gates_at_exit_12(self, monkeypatch, tmp_path) -> None:
        bridge_testkit.tray_mocks(monkeypatch, bridge_testkit.CheckMocks(window=False))
        exit_code, payload = run_cli(["sessions", "list", "--json"], monkeypatch, tmp_path)
        assert exit_code == 12
        assert payload["error"]["code"] == "window_closed"


class TestPostParseVl:
    """解析后 VL 修字(几何以一级 Vision 为准;校对只回填低置信行文本)。"""

    def test_low_conf_rows_get_corrected(self, tmp_path: Path) -> None:
        lines = list(_synthetic_session_lines())
        # 把第一行会话名压成低置信 → 触发 VL 送检
        lines[0] = _line(lines[0].text, 0.4, lines[0].x, lines[0].y)

        def fake_vl(image_path, draft_lines, workdir, model_id=None):
            assert len(draft_lines) >= 1  # 只送低置信行,不是全量
            corrected = [
                pixel.OcrLine(f"校正{i}", 0.4, line.x, line.y, line.w, line.h)
                for i, line in enumerate(draft_lines)
            ]
            return corrected, {"parsed": True, "model": "m", "downsampled": True}

        window = pixel.WindowInfo(window_id=1, onscreen=False, width=1920, height=1050)
        payload = pixel.list_sessions(
            BridgeConfig(), None,
            window_finder=lambda: window,
            capturer=lambda w, p: (render(p), {"state": "ok", "path": str(p),
                                               "width": 3840, "height": 2100,
                                               "mean_luma": 40.0})[1],
            vision_fn=lambda p: ("vision", lines, 0.01),
            vl_fn=fake_vl,
        )
        vl_meta = payload["ocr"]["vl"]
        assert vl_meta["used"] is True and vl_meta["corrected_lines"] >= 1
        # 被校对的行名已替换;其余行名保持原几何解析结果
        assert any(row["name"].startswith("校正") for row in payload["sessions"])
        assert payload["sessions"][1]["name"] != "校正1"


class TestOwnerNameGuard:
    """system_checks 窗口属主名对账(zh-CN「微信」恒判 False 的实测回归)。"""

    def test_owner_names_constant_shared(self) -> None:
        from wechat_bridge import system_checks as sc

        assert "微信" in sc.WECHAT_OWNER_NAMES
        assert "WeChat" in sc.WECHAT_OWNER_NAMES
        assert set(pixel.WECHAT_OWNER_NAMES) == set(sc.WECHAT_OWNER_NAMES)

    def test_window_open_accepts_chinese_owner(self, monkeypatch) -> None:
        import wechat_bridge.system_checks as sc

        class FakeQuartz:
            kCGWindowListOptionAll = 1
            kCGNullWindowID = 0
            kCGWindowOwnerName = "kCGWindowOwnerName"

            @staticmethod
            def CGWindowListCopyWindowInfo(option, target):
                return [{"kCGWindowOwnerName": "微信", "kCGWindowIsOnscreen": False}]

        monkeypatch.setattr(sc, "sys_darwin", lambda: True)
        import sys as _sys

        monkeypatch.setitem(_sys.modules, "Quartz", FakeQuartz)
        assert sc.wechat_main_window_open() is True


# —— 真机链(gated;design §8:MYIA_WECHAT_E2E=1 才跑,CI 缺省跳过)——

pytestmark_e2e = pytest.mark.skipif(
    __import__("os").environ.get("MYIA_WECHAT_E2E") != "1",
    reason="真机像素链默认跳过(MYIA_WECHAT_E2E=1 才跑;CI 无微信/无授权)",
)


@pytest.mark.skipif(
    __import__("os").environ.get("MYIA_WECHAT_E2E") != "1",
    reason="真机像素链默认跳过(MYIA_WECHAT_E2E=1 才跑)",
)
class TestRealPixelChain:
    def test_fixture_vision_parse_hit_rate(self) -> None:
        """合成面板真 Vision OCR → 解析命中(名字 ≥7/8;徽标部分命中如实)。"""
        engine, lines, _ = pixel.vision_ocr(FIXTURE_PNG)
        assert engine == "vision" and len(lines) > 20
        rows, meta = pixel.parse_sessions(lines, limit=20)
        truth_names = {s[0] for s in SESSIONS}
        hit = sum(1 for row in rows if row.name in truth_names)
        assert hit >= 7, f"合成面板名字命中率过低:{hit}/8(meta={meta})"

    def test_real_window_capture_and_parse(self) -> None:
        """真窗截窗(三态)→ Vision → 会话解析:零激活零抢焦,只验形状。"""
        import wechat_bridge.system_checks as sc

        if not sc.wechat_process_running():
            pytest.skip("微信进程不在(实况如实跳过)")
        window = pixel.find_main_window()
        if window is None:
            pytest.skip("微信主窗不在册(实况如实跳过)")
        import tempfile

        workdir = Path(tempfile.mkdtemp(prefix="wx-e2e-"))
        try:
            capture = pixel.capture_window(window, workdir / "w.png")
            assert capture["state"] == "ok"
            _, lines, _ = pixel.vision_ocr(workdir / "w.png")
            rows, meta = pixel.parse_sessions(lines, limit=20)
            assert isinstance(meta["rows"], int)  # 行数随实况,只验形状自洽
        finally:
            import shutil

            shutil.rmtree(workdir, ignore_errors=True)

    def test_real_vl_correction_roundtrip(self) -> None:
        """VL 服务在场时:合成面板真校对回路(行数保持,解析成功)。"""
        model = pixel.vl_available()
        if model is None:
            pytest.skip("VL 服务未起(127.0.0.1:8080;实况如实跳过)")
        _, lines, _ = pixel.vision_ocr(FIXTURE_PNG)
        import tempfile

        workdir = Path(tempfile.mkdtemp(prefix="wx-vl-"))
        try:
            corrected, meta = pixel.vl_correct_lines(FIXTURE_PNG, lines, workdir, model_id=model)
            assert meta["parsed"] is True
            assert len(corrected) == len(lines)
        finally:
            import shutil

            shutil.rmtree(workdir, ignore_errors=True)
