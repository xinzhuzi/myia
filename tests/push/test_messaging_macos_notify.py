"""Tests for 10-14-wechat-notify-revoke R3 — macos_notify 通道(本机弹窗)。

覆盖(AC3):osascript argv 构造断言/AppleScript 转义/每会话合并一条/
撤回文案三态/非 darwin 结构化拒/发送日志零正文(grep 断言)/targets 拒
(通道属性面;schema PUSH_CHANNELS 收录归集成接线,gated 用例等集成)。

零真通知:runner 注入点捕获 argv,不 spawn 真子进程(AC7 端到端弹窗归
主人实测,截图证据)。No pytest-asyncio in dev deps:async 走 asyncio.run
(test_bark.py 同约定)。
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from typing import Any

import pytest

from myssia.push.base import PushSendError
from myssia.push.macos_notify import (
    BODY_MAX_CHARS,
    NOTIFY_FIFO_ENV,
    OSASCRIPT_BIN,
    MacosNotifyChannel,
    applescript_escape,
    build_notification_script,
    plan_notifications,
    start_notify_relay,
)
from myssia.push import SendContext

CONTEXT = SendContext(slot="am", date="2026-10-14", category="微信通知", kind="immediate")


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def _new_msg(
    session: str = "合成群聊",
    sender: str = "合成张三",
    preview: str = "合成新消息预览",
    ts: int = 100,
) -> dict[str, Any]:
    """一条 message.new 条目(引擎 items_from_events 契约形;全合成)。"""
    return {
        "url": f"wechat-local://notify/{session}#wxn-{ts}",
        "title": f"{session} · {sender}",
        "content": preview,
        "sender": sender,
        "session_display": session,
        "sender_display": sender,
        "event": "message.new",
        "ts": ts,
        "revoke": False,
    }


def _revoke(
    session: str = "合成群聊",
    revoker: str = "合成李四",
    body_state: str = '原内容:"被撤回的合成原文"',
    ts: int = 200,
) -> dict[str, Any]:
    """一条 message.revoke 条目(content = 引擎组装好的三态文案)。"""
    return {
        "url": f"wechat-local://notify/{session}#wxnr-{ts}",
        "title": f"{session} · {revoker} 撤回了一条消息",
        "content": f"{revoker}撤回了一条消息:{body_state}",
        "sender": revoker,
        "session_display": session,
        "sender_display": revoker,
        "event": "message.revoke",
        "ts": ts,
        "revoke": True,
    }


class FakeRunner:
    """runner 注入点:捕获 argv,可注入 exit 码/超时。"""

    def __init__(self, *, exit_code: int = 0, raise_timeout: bool = False) -> None:
        self.calls: list[list[str]] = []
        self.exit_code = exit_code
        self.raise_timeout = raise_timeout

    def __call__(self, argv: Any, timeout: float) -> tuple[int, str, str]:
        import subprocess

        self.calls.append(list(argv))
        if self.raise_timeout:
            raise subprocess.TimeoutExpired(cmd="osascript", timeout=timeout)
        return self.exit_code, "", ""


def _channel(runner: FakeRunner, *, platform: str = "darwin") -> MacosNotifyChannel:
    return MacosNotifyChannel(runner=runner, platform=platform)


# ---------------------------------------------------------------------------
# argv 构造与转义
# ---------------------------------------------------------------------------


class TestArgvAndEscape:
    def test_argv_shape_is_literal_osascript(self) -> None:
        runner = FakeRunner()
        _run(_channel(runner).send([_new_msg()], CONTEXT))
        assert len(runner.calls) == 1
        argv = runner.calls[0]
        assert argv[0] == OSASCRIPT_BIN == "/usr/bin/osascript"
        assert argv[1] == "-e"
        script = argv[2]
        assert script.startswith('display notification "')
        assert 'with title "合成群聊"' in script
        assert 'subtitle "1 条新消息"' in script

    def test_escape_quotes_backslash_newline(self) -> None:
        assert applescript_escape('a"b\\c') == 'a\\"b\\\\c'
        assert applescript_escape("行1\n行2") == "行1\\n行2"
        assert applescript_escape("tab\there") == "tab\\there"

    def test_script_escapes_body_with_quotes(self) -> None:
        runner = FakeRunner()
        _run(
            _channel(runner).send(
                [_new_msg(preview='说"你好"\n第二行')], CONTEXT
            )
        )
        script = runner.calls[0][2]
        assert '\\"你好\\"' in script
        assert "\\n" in script
        assert "\n" not in script  # 裸换行绝不进 AppleScript 串

    def test_build_notification_script_without_subtitle(self) -> None:
        script = build_notification_script(title="t", subtitle=None, body="b")
        assert script == 'display notification "b" with title "t"'


# ---------------------------------------------------------------------------
# 每会话合并 + 撤回独立成条 + 三态文案
# ---------------------------------------------------------------------------


class TestMergeDiscipline:
    def test_same_session_merges_into_one_with_count(self) -> None:
        runner = FakeRunner()
        items = [
            _new_msg(preview="第一条", ts=100),
            _new_msg(preview="第二条", ts=200),
            _new_msg(session="另一会话", preview="别的会话", ts=150),
        ]
        _run(_channel(runner).send(items, CONTEXT))
        assert len(runner.calls) == 2  # 两会话各一条
        scripts = [call[2] for call in runner.calls]
        assert any('subtitle "2 条新消息"' in s for s in scripts)
        assert any('subtitle "1 条新消息"' in s for s in scripts)
        # body = 最新一条(ts 最大)的「发送者: 预览」
        two = next(s for s in scripts if "2 条新消息" in s)
        assert "合成张三: 第二条" in two
        assert "第一条" not in two

    def test_body_clipped_to_200(self) -> None:
        runner = FakeRunner()
        _run(_channel(runner).send([_new_msg(preview="长" * 500)], CONTEXT))
        script = runner.calls[0][2]
        # 转义后正文长度受 200 帽约束(截断加省略号)
        body = script.split('display notification "')[1].split('" with title')[0]
        assert len(body) <= BODY_MAX_CHARS + 2  # 省略号+发送者前缀裕量内

    def test_revoke_is_separate_notification(self) -> None:
        runner = FakeRunner()
        items = [_new_msg(ts=100), _revoke(ts=200)]
        _run(_channel(runner).send(items, CONTEXT))
        assert len(runner.calls) == 2
        revoke_script = next(
            call[2] for call in runner.calls if "撤回了一条消息" in call[2]
        )
        assert "合成李四撤回了一条消息" in revoke_script
        # 引号按 AppleScript 形态转义入脚本(转义断言另见 TestArgvAndEscape)
        assert '原内容:\\"被撤回的合成原文\\"' in revoke_script
        assert "条新消息" not in revoke_script  # 撤回条不带 N 条新消息 subtitle

    @pytest.mark.parametrize(
        ("state", "fragment"),
        [
            ('原内容:"恢复的原文预览"', "恢复的原文预览"),  # 有恢复
            ('"合成王五"撤回了一条消息', "合成王五"),      # replacemsg 兜底
            ("原内容未能恢复", "原内容未能恢复"),          # none
        ],
    )
    def test_revoke_three_states(self, state: str, fragment: str) -> None:
        plans = plan_notifications([_revoke(body_state=state)])
        assert len(plans) == 1
        assert fragment in plans[0]["body"]
        assert plans[0]["title"] == "合成群聊"
        assert plans[0]["subtitle"] is None

    def test_revoke_without_content_gets_fallback(self) -> None:
        item = _revoke()
        item["content"] = "   "
        plans = plan_notifications([item])
        assert "原内容未能恢复" in plans[0]["body"]

    def test_generic_items_without_event_metadata_merge(self) -> None:
        plans = plan_notifications(
            [{"title": "羊毛线报A", "source": "羊毛", "ts": 1},
             {"title": "羊毛线报B", "source": "羊毛", "ts": 2}]
        )
        assert len(plans) == 1
        assert plans[0]["subtitle"] == "2 条更新"
        assert "羊毛线报B" in plans[0]["body"]  # 最新

    def test_item_key_carries_anchor_dedup_key(self) -> None:
        """10-15 粒度细化:计划携 item_key = 锚定条目 dedup_key(合并通知锚
        = 最新一条);缺 dedup_key = None(深链退会话级),不虚构。"""
        old = _new_msg(ts=100)
        old["dedup_key"] = "dk-old"
        latest = _new_msg(ts=200)
        latest["dedup_key"] = "dk-latest"
        plans = plan_notifications([old, latest])
        assert plans[0]["item_key"] == "dk-latest"  # 最新锚,非首条

        no_key = _new_msg()  # 异常条目缺 dedup_key
        plans = plan_notifications([no_key])
        assert plans[0]["item_key"] is None

        revoke = _revoke()
        revoke["dedup_key"] = "dk-revoke"
        plans = plan_notifications([revoke])
        assert plans[0]["item_key"] == "dk-revoke"  # 撤回独立条也锚定


# ---------------------------------------------------------------------------
# 平台门 + 失败面 + 日志零正文
# ---------------------------------------------------------------------------


def test_start_notify_relay_missing_mkfifo_degrades_to_none(monkeypatch, tmp_path):
    """平台能力缺失纵深兜底(10-18-v0.0.5 Windows 装测实锤):os.mkfifo
    不存在(Windows)时优雅回退 None,不把 serve() 调用方拖崩——serve 层
    的 darwin 守卫是第一道,这里是任何未来新调用点的零伤兜底。"""
    monkeypatch.delattr(os, "mkfifo", raising=False)
    assert start_notify_relay(tmp_path, lambda plan: None) is None


class TestGuards:
    def test_non_darwin_is_structured_platform_unsupported(self) -> None:
        runner = FakeRunner()
        with pytest.raises(PushSendError) as excinfo:
            _run(_channel(runner, platform="linux").send([_new_msg()], CONTEXT))
        assert excinfo.value.code == "platform_unsupported"
        assert runner.calls == []  # 零子进程

    def test_osascript_nonzero_exit_is_structured(self) -> None:
        runner = FakeRunner(exit_code=1)
        with pytest.raises(PushSendError) as excinfo:
            _run(_channel(runner).send([_new_msg()], CONTEXT))
        assert excinfo.value.code == "osascript_failed"
        assert "exit=1" in str(excinfo.value)
        # 失败消息零正文零 stderr 回显(私有数据红线)
        assert "合成" not in str(excinfo.value)

    def test_timeout_is_structured(self) -> None:
        runner = FakeRunner(raise_timeout=True)
        with pytest.raises(PushSendError) as excinfo:
            _run(_channel(runner).send([_new_msg()], CONTEXT))
        assert excinfo.value.code == "notify_timeout"

    def test_supports_targeting_false(self) -> None:
        """targets 配置即拒的通道属性面(stdout 同款;schema 分支归集成)。"""
        assert MacosNotifyChannel.supports_targeting is False
        assert MacosNotifyChannel.name == "macos_notify"

    def test_send_log_has_no_content(self, caplog: pytest.LogCaptureFixture) -> None:
        """AC3:发送日志只记形状,grep 断言零正文(预览/发送者/会话名均不入)。"""
        runner = FakeRunner()
        with caplog.at_level(logging.INFO, logger="myssia.push.macos_notify"):
            _run(
                _channel(runner).send(
                    [_new_msg(preview="机密预览不应入日志"), _revoke()],
                    CONTEXT,
                )
            )
        joined = "\n".join(record.getMessage() for record in caplog.records)
        assert joined, "应有一条形状级日志"
        for forbidden in ("机密预览", "合成张三", "合成李四", "被撤回的合成原文"):
            assert forbidden not in joined
        assert "notifications=2" in joined

    def test_empty_items_send_nothing(self) -> None:
        runner = FakeRunner()
        _run(_channel(runner).send([], CONTEXT))
        assert runner.calls == []


# ---------------------------------------------------------------------------
# schema 收录(gated:集成把 macos_notify 补进 PUSH_CHANNELS 后本用例生效)
# ---------------------------------------------------------------------------


class TestSchemaIntegration:
    def test_push_channels_literal_includes_macos_notify(self) -> None:
        """集成接线后:macos_notify 入 PUSH_CHANNELS 字面表(target/targets 拒)。

        未接线时(本文件先落)如实 skip——接线清单见任务档 integrationSpec;
        接线后本用例守住「字面表收录」不再漂移。
        """
        from myssia import schema

        if "macos_notify" not in schema.PUSH_CHANNELS:
            pytest.skip("等集成:schema PUSH_CHANNELS 收录 macos_notify(R6 接线)")
        assert "macos_notify" in schema.PUSH_CHANNELS

    def test_push_channels_registry_registered(self) -> None:
        from myssia.push import CHANNELS

        if "macos_notify" not in CHANNELS:
            pytest.skip("等集成:push/__init__.py 注册 MacosNotifyChannel(R6 接线)")
        assert CHANNELS["macos_notify"] is MacosNotifyChannel


# ---------------------------------------------------------------------------
# 壳代发(MYIA_NOTIFY_FIFO 中继;10-14-notify-app-icon)
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_notify_fifo_env(monkeypatch: pytest.MonkeyPatch):
    """中继环境隔离:每测前后摘除,防泄漏污染既有 osascript 用例。"""
    monkeypatch.delenv(NOTIFY_FIFO_ENV, raising=False)
    yield
    monkeypatch.delenv(NOTIFY_FIFO_ENV, raising=False)


class TestNotifyRelayFifo:
    """中继端到端(真 FIFO+读者线程)→ 零 osascript+形状不变;无读者/无管道 → 回退。"""

    def test_relay_end_to_end_zero_osascript(self, tmp_path) -> None:
        received: list[dict[str, str | None]] = []
        fifo = start_notify_relay(tmp_path, received.append)
        try:
            assert fifo is not None and fifo.exists()
            assert os.environ[NOTIFY_FIFO_ENV] == str(fifo)  # 注入 = 子进程继承面
            runner = FakeRunner()
            _run(_channel(runner).send([_new_msg(), _revoke()], CONTEXT))
            deadline = time.monotonic() + 2.0  # 读者线程异步转发,轮询等待
            while len(received) < 2 and time.monotonic() < deadline:
                time.sleep(0.02)
            assert runner.calls == []  # 零 osascript(中继在位 = 不 spawn)
            assert len(received) == 2  # 合并纪律不变:撤回独立在前 + 每会话一条
            assert received[0]["subtitle"] is None  # 撤回条无 subtitle
            assert received[0]["title"] == "合成群聊"
            assert received[1]["subtitle"] == "1 条新消息"
            assert received[1]["body"].startswith("合成张三: ")
        finally:
            os.environ.pop(NOTIFY_FIFO_ENV, None)

    def test_fifo_no_reader_falls_back_osascript(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setenv(NOTIFY_FIFO_ENV, str(tmp_path / "missing.fifo"))
        runner = FakeRunner()
        _run(_channel(runner).send([_new_msg()], CONTEXT))
        assert len(runner.calls) == 1  # 无读者(ENXIO)回退直弹,横幅不丢
        assert runner.calls[0][0] == OSASCRIPT_BIN

    def test_env_unset_osascript_as_before(self, monkeypatch) -> None:
        monkeypatch.delenv(NOTIFY_FIFO_ENV, raising=False)  # CLI 单跑形态
        runner = FakeRunner()
        _run(_channel(runner).send([_new_msg()], CONTEXT))
        assert len(runner.calls) == 1
