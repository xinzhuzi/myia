"""send_direct 直发通道单测(task 10-14-wechat-sendmsg-direct design-阶段3 §6)。

全桩离线(§6 门禁纪律):lldb 全桩 = monkeypatch ``senddirect.run_lldb_batch``
回放哨兵协议(SENTINEL 协议回放);localdb/目标解析照 test_bridge_cli 判例
mock;时钟/sleep 注入(回执退避不真等)。真实 lldb/微信路径在 e2e 门控件
之外,本文件零微信零 attach 零发送。

§6 对账:1 门关/未知键/形状;2 版本门夹具→24+未调用+rollback;3 cmd 工件
golden(唯一碰微信内存的产物);4 快乐路载荷+dry-run 零状态写入;5 17/30/
dedup/14/目标/空正文/双长度门;6 跨通道互锁;7 codes 24+doctor 三态;
8 冻结分支(§5 预案);另附 S15 事故回归测(早失败路径绝不触碰 cwd)。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import wechat_bridge.codes as codes_mod
import wechat_bridge.senddirect as senddirect
from wechat_bridge.codes import BridgeError
from wechat_bridge.send_state import SendRateState
from wechat_bridge.sendtarget import SendTarget

from bridge_testkit import CheckMocks, run_cli, tray_mocks

FAKE_TARGET = SendTarget(
    username="filehelper", alias=None, display_name="文件传输助手", search_term="filehelper"
)

#: 阶段3 §2.6 schema 3 锚定表夹具(全部 slide 相对量;哈希为占位值,
#: 真值来自 r4 钉入轮——单测只锁形态与链路)。
ANCHOR_FIXTURE: dict = {
    "schema": 3,
    "wechat_version": "4.1.15",
    "dylib_arm64_slice_sha256": "aa" * 32,
    "anchor_offset": "0x490fb20",
    "anchor_bytes_hex": "ffc305d1fc6f14a9f44f15a9fd7b16a9",
    "offsets": {
        "pump_resume": "0x43f88e4",
        "enqueue_a": "0xa6060",
        "enqueue_b": "0xa5ed0",
        "send_entry": "0x1234567",
        "arg_abi": {
            "peer_slot": "x1",
            "body_slot": "x2",
            "string_form": "inline23_rawlen",
            "by_value": False,
            "buffer_mode": "expr_local",
        },
        "service_ptr_mode": "global",
        "service_global_off": "0x9c61f58",
        "queue_selector": "same",
        "svc_vtable_off": "0x8765432",
        "svc_invariants_hex": "00112233445566778899aabbccddeeff00112233",
    },
}


def _write_anchor(home: Path, anchor: dict | None = ANCHOR_FIXTURE) -> None:
    """锚定表落 tmp 数据根(私有路径族 wechat-bridge/)。"""
    directory = home / "wechat-bridge"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "send-direct-anchors.json").write_text(
        json.dumps(anchor, ensure_ascii=False, indent=1), encoding="utf-8"
    )


def _write_config(home: Path, payload: dict) -> None:
    directory = home / "wechat-bridge"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "config.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8"
    )


def _db_mocks(
    monkeypatch: pytest.MonkeyPatch, target: SendTarget | None = FAKE_TARGET
) -> None:
    """localdb 链 + 目标解析 mock(test_bridge_cli._send_db_mocks 同款)。"""
    import wechat_bridge.localdb as localdb
    import wechat_bridge.sendtarget as sendtarget

    monkeypatch.setattr(localdb, "locate_db_storage", lambda: Path("/fake-db-storage"))
    monkeypatch.setattr(
        localdb, "resolve_keys", lambda storage, *, config=None: {"k": "v"}
    )
    monkeypatch.setattr(sendtarget, "resolve_target", lambda config, chat_id, **kw: target)


def _receipt_mocks(monkeypatch: pytest.MonkeyPatch, *, green: bool = True) -> None:
    """回执闭包的 query_history mock:绿=新 ts 同文;红=空消息表。"""
    import wechat_bridge.localdb as localdb

    def _query(config, storage, keys, username, days):
        if green:
            return {"messages": [{"text": "嘻嘻", "ts": 9999999999}]}
        return {"messages": []}

    monkeypatch.setattr(localdb, "query_history", _query)


def _direct_env(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *,
    enabled: bool = True,
    anchor: dict | None = ANCHOR_FIXTURE,
    receipt_green: bool = True,
    window: bool = True,
) -> Path:
    """send_direct 全前置绿装:配置门/锚定表/lldb/微信 pid/回执/免睡。"""
    home = tmp_path / "direct-home"
    home.mkdir(parents=True, exist_ok=True)
    if enabled:
        _write_config(home, {"send_direct_enabled": True})
    if anchor is not None:
        _write_anchor(home, anchor)
    tray_mocks(monkeypatch, CheckMocks(window=window))
    _db_mocks(monkeypatch)
    _receipt_mocks(monkeypatch, green=receipt_green)
    monkeypatch.setattr(senddirect, "wechat_pid", lambda: 4242)
    monkeypatch.setattr(senddirect, "lldb_executable", lambda: "/fake/bin/lldb")
    monkeypatch.setattr(senddirect, "_sleep", lambda seconds: None)
    return home


def _fake_lldb(monkeypatch: pytest.MonkeyPatch, script: dict) -> dict:
    """lldb 批全桩:按 script 回放哨兵协议,记录工件面供断言。

    script 键:preflight_ok(bool)/preflight_fail(reason)/armed(bool)/
    done(call_rc)/error({stage,detail})/timed_out/killed/rc。
    """
    recorded: dict = {"runs": [], "on_armed_called": 0}

    def fake_run(
        lldb_path, cmd_path, run_dir, request_path, *, timeout_s, grace_s,
        on_armed=None, poll_s=0.2, sleep=None, monotonic=None,
    ):
        recorded["runs"].append(
            {
                "lldb_path": lldb_path,
                "cmd_text": Path(cmd_path).read_text(encoding="utf-8"),
                "request": json.loads(Path(request_path).read_text(encoding="utf-8")),
            }
        )
        run = Path(run_dir)
        if "preflight_fail" in script:
            (run / "PREFLIGHT_FAIL.json").write_text(
                json.dumps(
                    {"reason": script["preflight_fail"], "detail": script.get("detail", "")}
                ),
                encoding="utf-8",
            )
        elif script.get("preflight_ok", True):
            (run / "PREFLIGHT_OK.json").write_text(
                json.dumps({"slide": 0x12B0E8000, "svc": 0x89AE3E168, "attach_ms": 5}),
                encoding="utf-8",
            )
        armed = bool(script.get("armed", False))
        if armed:
            (run / "ARMED.json").write_text(json.dumps({"t": 0}), encoding="utf-8")
            if on_armed is not None:
                recorded["on_armed_called"] += 1
                on_armed()
        if "done" in script:
            (run / "DONE.json").write_text(
                json.dumps({"call_rc": script["done"]}), encoding="utf-8"
            )
        if "error" in script:
            (run / "ERROR.json").write_text(
                json.dumps(script["error"]), encoding="utf-8"
            )
        return senddirect.BatchOutcome(
            returncode=script.get("rc", 0),
            timed_out=bool(script.get("timed_out", False)),
            killed=bool(script.get("killed", False)),
            armed_seen=armed,
            log_path=run / "lldb-batch.log",
        )

    monkeypatch.setattr(senddirect, "run_lldb_batch", fake_run)
    return recorded


def _fingerprints(home: Path) -> dict:
    state = SendRateState(home / "wechat-localdb" / "send_state.json")
    return state._locked(lambda _: state._fingerprints_unlocked(state._read_full_unlocked()))


class TestConfigGate:
    """§6-1:门关/未知键/形状校验。"""

    def test_disabled_by_default_exit_1_named_code(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path, enabled=False)
        recorded = _fake_lldb(monkeypatch, {"preflight_ok": True})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_direct_disabled"
        assert recorded["runs"] == []  # 未 spawn(lldb 批零调用)

    def test_unknown_config_key_still_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = tmp_path / "bad-home"
        home.mkdir()
        _write_config(home, {"send_direct_enabled": True, "send_directt_enabled": True})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"

    def test_send_direct_enabled_shape_must_be_bool(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = tmp_path / "shape-home"
        home.mkdir()
        _write_config(home, {"send_direct_enabled": "yes"})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 2
        assert "send_direct_enabled" in payload["error"]["message"]


class TestVersionGates:
    """§6-2:版本门夹具 → 24 + 未进调用段 + rollback(send_text 不被 14 拦)。"""

    @pytest.mark.parametrize("reason", ["slice_sha256", "anchor_bytes", "module_lock"])
    def test_gate_failure_exit_24_no_call_and_rollback(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, reason: str
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(
            monkeypatch, {"preflight_fail": reason, "detail": "fixture"}
        )
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 24
        assert payload["error"]["code"] == "send_direct_unanchored"
        run = recorded["runs"][0]
        # 未生成 expr 调用段:批内无 ARMED(armed_seen False = probe 未进调用)。
        assert recorded["on_armed_called"] == 0
        assert "senddirect_probe.run()" in run["cmd_text"]
        assert run["request"]["mode"] == "call"  # 请求面在,probe 拒调
        # rollback:占位还原(状态无 last_send)→ OCR 回退不撞 G6 14。
        state = SendRateState(home / "wechat-localdb" / "send_state.json")
        assert state.load_last_send_epoch() is None
        monkeypatch.setattr(
            "wechat_bridge.sendui.send_text",
            lambda *a, **kw: {"send": {"sent": True}},
        )
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0  # 未被 14 拦(rollback 生效)

    def test_missing_anchor_file_exit_24(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path, anchor=None)
        recorded = _fake_lldb(monkeypatch, {})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 24
        assert "锚定表缺位" in payload["error"]["message"]
        assert recorded["runs"] == []

    def test_incomplete_anchor_send_entry_missing_exit_24(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        anchor = json.loads(json.dumps(ANCHOR_FIXTURE))
        anchor["offsets"]["send_entry"] = None
        home = _direct_env(monkeypatch, tmp_path, anchor=anchor)
        recorded = _fake_lldb(monkeypatch, {})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 24
        assert "send_entry" in payload["error"]["message"]
        assert recorded["runs"] == []

    def test_attach_failure_maps_to_lldb_attach_failed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        _fake_lldb(monkeypatch, {"preflight_fail": "attach", "detail": "busy"})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "lldb_attach_failed"
        state = SendRateState(home / "wechat-localdb" / "send_state.json")
        assert state.load_last_send_epoch() is None  # rollback


class TestCmdArtifacts:
    """§6-3:cmd 工件 golden(唯一碰微信内存的产物;纯函数直测)。"""

    def test_inline23_filehelper(self) -> None:
        assert senddirect.inline23_bytes(b"filehelper") == [
            102, 105, 108, 101, 104, 101, 108, 112, 101, 114,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10,
        ]

    def test_inline23_len_is_utf8_byte_count_not_chars(self) -> None:
        # 「嘻嘻」= 2 字符 = 6 UTF-8 字节 → len 字节 = 6(§2.0 定则)。
        assert senddirect.inline23_bytes("嘻嘻".encode("utf-8")) == [
            229, 152, 187, 229, 152, 187,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6,
        ]

    def test_inline23_rejects_24_bytes(self) -> None:
        with pytest.raises(ValueError):
            senddirect.inline23_bytes("嘻嘻嘻嘻嘻嘻嘻嘻".encode("utf-8"))  # 8 汉字=24B

    def test_call_expr_template_and_address_arithmetic(self) -> None:
        expr = senddirect.build_call_expr(
            0x0A6060, 0x12B0E8000, 0x89AE3E168,
            b"filehelper", "嘻嘻".encode("utf-8"),
        )
        assert expr.startswith("(int)({\n")
        assert "unsigned char peer[24] = {102,105,108,101,104,101,108,112,101,114,0,0,0,0,0,0,0,0,0,0,0,0,0,10};" in expr
        assert "unsigned char body[24] = {229,152,187,229,152,187,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6};" in expr
        # 0x<S+F_send_off> 代入算术:slide+send_entry = 0x12b0e8000+0xa6060
        assert f"0x{0x12B0E8000 + 0xA6060:x}" in expr
        assert f"(void*)0x{0x89AE3E168:x}, (void*)peer, (void*)body" in expr
        assert "((int(*)(void*,void*,void*))" in expr

    def test_cmd_text_shape(self, tmp_path: Path) -> None:
        cmd = senddirect.build_cmd_text(4242, Path("/x/senddirect_probe.py"))
        assert cmd == (
            "attach -p 4242\n"
            'command script import "/x/senddirect_probe.py"\n'
            "script senddirect_probe.run()\n"
            "detach\n"
            "quit\n"
        )


class TestHappyPathAndDryRun:
    """§6-4:快乐路载荷形状 + dry-run 零状态写入。"""

    def test_happy_path_payload_shape(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(monkeypatch, {"armed": True, "done": 0})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        send = payload["send"]
        assert send["chat"] == "filehelper"
        assert send["target"] == {"username": "filehelper", "display_name": "文件传输助手"}
        assert send["sent"] is True and send["channel"] == "direct"
        assert send["anchor_build"] == "4.1.15"
        assert send["lldb"]["call_rc"] == 0 and send["lldb"]["receipt"] == "green"
        assert isinstance(send["lldb"]["attach_ms"], int)
        assert isinstance(send["elapsed_ms"], int)
        # 调用载荷面:peer/body 逐字节进 request(探针侧构造 expr)。
        request = recorded["runs"][0]["request"]
        assert request["call"]["peer"] == [102, 105, 108, 101, 104, 101, 108, 112, 101, 114]
        assert request["call"]["body"] == [229, 152, 187, 229, 152, 187]
        assert request["call"]["send_entry"] == "0x1234567"
        # 指纹落 sent(回执绿升级)。
        entries = _fingerprints(home)
        assert entries and all(v["status"] == "sent" for v in entries.values())

    def test_dry_run_zero_state_writes(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(monkeypatch, {"preflight_ok": True})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-", "--dry-run"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        send = payload["send"]
        assert send["sent"] is False and send["dry_run"] is True
        assert send["channel"] == "direct" and send["preflight"] == "ok"
        assert recorded["on_armed_called"] == 0
        assert not (home / "wechat-localdb" / "send_state.json").exists()
        # 可无限重跑:同一 dry-run 再次 exit 0。
        exit_code, _ = run_cli(
            ["send_direct", "filehelper", "--file", "-", "--dry-run"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0


class TestFailureFamilies:
    """§6-5:17/30/dedup/14/目标/空正文/双长度门。"""

    def test_armed_receipt_not_green_exit_17_pending_kept(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path, receipt_green=False)
        _fake_lldb(monkeypatch, {"armed": True, "done": 0})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 17
        assert payload["error"]["code"] == "send_uncertain_dedup"
        entries = _fingerprints(home)
        assert entries and all(v["status"] == "pending" for v in entries.values())
        # uncertain-never-retry:同指纹重试 → 17(指纹门先于间隔门)。
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 17

    def test_call_error_receipt_red_is_call_failed(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path, receipt_green=False)
        _fake_lldb(
            monkeypatch, {"armed": True, "error": {"stage": "call", "detail": "EXC_BAD_ACCESS"}}
        )
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_direct_call_failed"

    def test_pre_armed_timeout_exit_30_rollback(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(
            monkeypatch, {"preflight_ok": False, "timed_out": True, "killed": True, "rc": None}
        )
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 30
        assert payload["error"]["code"] == "timeout"
        assert recorded["on_armed_called"] == 0
        state = SendRateState(home / "wechat-localdb" / "send_state.json")
        assert state.load_last_send_epoch() is None  # rollback

    def test_armed_timeout_exit_17_no_rollback(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        _fake_lldb(
            monkeypatch, {"armed": True, "timed_out": True, "killed": True, "rc": None}
        )
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 17
        entries = _fingerprints(home)
        assert entries and all(v["status"] == "pending" for v in entries.values())

    def test_dedup_idempotent_exit_0(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(monkeypatch, {"armed": True, "done": 0})
        exit_code, _ = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        send = payload["send"]
        assert send["sent"] is False and send["deduped"] is True
        assert len(recorded["runs"]) == 1  # 第二次未进 lldb 批

    def test_interval_gate_exit_14(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        _fake_lldb(monkeypatch, {"armed": True, "done": 0})
        clock = {"t": 1000.0}
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: clock["t"])
        exit_code, _ = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        clock["t"] = 1003.0  # 10s 内异指纹
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="哈",
        )
        assert exit_code == 14
        assert payload["error"]["code"] == "send_rate_limited"

    def test_target_not_found(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        _db_mocks(monkeypatch, target=None)
        recorded = _fake_lldb(monkeypatch, {})
        exit_code, payload = run_cli(
            ["send_direct", "no_such_zzz123", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_target_not_found"
        assert recorded["runs"] == []

    def test_empty_body_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="  \n",
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"

    def test_body_24_bytes_rejected(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(monkeypatch, {})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻嘻嘻嘻嘻嘻嘻",  # 8 汉字 = 24B
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_direct_body_too_long"
        assert recorded["runs"] == []

    def test_target_41_byte_chatroom_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        long_room = "@chatroom-" + "1" * 32  # 41B(F9:长 id 真实存在)
        target = SendTarget(
            username=long_room, alias=None, display_name="群", search_term=long_room
        )
        home = _direct_env(monkeypatch, tmp_path)
        _db_mocks(monkeypatch, target=target)
        recorded = _fake_lldb(monkeypatch, {})
        exit_code, payload = run_cli(
            ["send_direct", long_room, "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_direct_target_too_long"
        assert recorded["runs"] == []


class TestCrossChannelInterlock:
    """§6-6:跨通道互锁(direct ↔ text 共用 SendRateState 同 flock 同键)。"""

    def test_direct_then_text_interlock(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        _fake_lldb(monkeypatch, {"armed": True, "done": 0})
        text_calls: list[dict] = []

        def _text_stub(config, target, body, *, dry_run=False, on_armed=None,
                       on_receipt_green=None, receipt_query=None):
            text_calls.append({"body": body})
            if on_armed is not None:
                on_armed()
            if on_receipt_green is not None:
                on_receipt_green()
            return {"send": {"target": {"username": target.username,
                                        "display_name": target.display_name},
                             "channel": "ax", "sent": True}}

        monkeypatch.setattr("wechat_bridge.sendui.send_text", _text_stub)
        clock = {"t": 2000.0}
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: clock["t"])
        exit_code, _ = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        # 异指纹(异正文)10s 内 → 14(间隔门;非 dedup——互斥断言)。
        clock["t"] = 2005.0
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="哈",
        )
        assert exit_code == 14
        # 同指纹跨通道(direct 后立即 text 同正文同目标)→ deduped 幂等
        # exit 0 零出站(text 桩未被调用)。
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        send = payload["send"]
        assert send["sent"] is False and send["deduped"] is True
        assert text_calls == []  # 零出站


class TestCodesAndDoctor:
    """§6-7:codes 24 名映射 + doctor direct_channel 三态。"""

    def test_code_24_named(self) -> None:
        assert codes_mod.CODE_NAMES[24] == "send_direct_unanchored"
        assert codes_mod.SEND_DIRECT_UNANCHORED == 24
        assert BridgeError(24, "x").name == "send_direct_unanchored"

    def test_doctor_carries_direct_channel_disabled(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        tray_mocks(monkeypatch)
        import wechat_bridge.system_checks as sc
        import wechat_bridge.axui as axui

        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: 122)
        monkeypatch.setattr(axui, "read_input_value", lambda: "")
        exit_code, payload = run_cli(["doctor"], monkeypatch, tmp_path)
        assert exit_code == 0
        node = payload["doctor"]["direct_channel"]
        assert node["enabled"] is False
        assert node["anchored"] == "no_anchor_file"  # tmp 数据根无锚定表

    def test_doctor_direct_channel_states(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        from wechat_bridge.config import BridgeConfig

        # 缺锚定表 → no_anchor_file。(BridgeConfig() 显式缺省态——无参
        # load_config() 会读真实数据根,真机开门后此测试即被环境穿透,
        # 2026-10-15 收尾验收实测。)
        node = senddirect.doctor_direct_channel(
            BridgeConfig(), data_root=tmp_path, lldb_check=lambda: "/fake/lldb"
        )
        assert node["anchored"] == "no_anchor_file"
        assert node["last_anchor_build"] is None
        # 有锚定表 + 门关 → unknown(不 attach)。
        _write_anchor(tmp_path)
        node = senddirect.doctor_direct_channel(
            BridgeConfig(), data_root=tmp_path, lldb_check=lambda: "/fake/lldb"
        )
        assert node == {
            "enabled": False,
            "anchored": "unknown",
            "lldb": "ok",
            "last_anchor_build": "4.1.15",
            "slice_sha256_matched": None,
        }
        # 门开 + 验证器三态注入。
        enabled_cfg = BridgeConfig(send_direct_enabled=True)
        for verdict in ("ok", "mismatch", "unknown"):
            node = senddirect.doctor_direct_channel(
                enabled_cfg,
                data_root=tmp_path,
                validator=lambda verdict=verdict: {
                    "anchored": verdict,
                    "slice_sha256_matched": verdict == "ok",
                },
                lldb_check=lambda: "/fake/lldb",
            )
            assert node["anchored"] == verdict
            assert node["enabled"] is True

    def test_doctor_disabled_never_attaches(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        from wechat_bridge.config import BridgeConfig

        _write_anchor(tmp_path)
        probed: list[int] = []

        def _validator():  # 不应被调(门关不 attach)
            probed.append(1)
            return {"anchored": "ok", "slice_sha256_matched": True}

        senddirect.doctor_direct_channel(
            BridgeConfig(), data_root=tmp_path,
            validator=_validator, lldb_check=lambda: "/fake/lldb",
        )
        assert probed == []


class TestFrozenBranch:
    """§6-8:SIGKILL 收兵桩(哨兵缺失)→ 存活探测被调 → wechat_frozen。"""

    def test_killed_no_sentinels_reports_frozen(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import wechat_bridge.system_checks as sc

        home = _direct_env(monkeypatch, tmp_path)
        probes = {"n": 0}

        def _counting_alive():
            probes["n"] += 1
            return True  # 进程在(窗口探针挂 False → 冻结判别形态)

        monkeypatch.setattr(sc, "wechat_process_running", _counting_alive)
        monkeypatch.setattr(sc, "wechat_main_window_open", lambda: False)
        _fake_lldb(monkeypatch, {"preflight_ok": False, "killed": True, "rc": None})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "wechat_frozen"
        assert "冻结" in payload["error"]["message"]
        assert "绝不自动 kill" in payload["error"]["fix_hint"]
        assert probes["n"] >= 1  # 存活探测被调(§5-ii)

    def test_killed_wechat_dead_reports_honestly(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import wechat_bridge.system_checks as sc

        home = _direct_env(monkeypatch, tmp_path)
        monkeypatch.setattr(sc, "wechat_process_running", lambda: False)
        monkeypatch.setattr(sc, "wechat_main_window_open", lambda: None)
        _fake_lldb(monkeypatch, {"preflight_ok": False, "killed": True, "rc": None})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "wechat_frozen"
        assert "进程不在" in payload["error"]["message"]


class TestAnchorTable:
    """锚定表装载面(§2.6 形态门;malformed → 发送 24 / doctor unknown)。"""

    def test_malformed_anchor_rejected_as_unanchored(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path, anchor={"schema": 2})
        recorded = _fake_lldb(monkeypatch, {})
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 24
        assert "schema" in payload["error"]["message"]
        assert recorded["runs"] == []
        assert senddirect.anchor_file_state(home) == "malformed"

    def test_slice_hash_fat_and_thin(self, tmp_path: Path) -> None:
        """F10 切片哈希算法:FAT 取 arm64 区间,thin 整文件。"""
        import hashlib
        import struct

        payload = b"\xab" * 64
        # FAT:2 arch(x86_64@0x4000 + arm64@0x8000);fat_arch 每项 20B 五字段
        # (cputype/cpusubtype/offset/size/align,皆大端);文件区间与表严格对齐。
        fat = struct.pack(">II", 0xCAFEBA_BE, 2)
        fat += struct.pack(">IIIII", 0x01000007, 0, 0x4000, 0x40, 0x1000)  # x86_64
        fat += struct.pack(">IIIII", 0x0100000C, 0, 0x8000, len(payload), 0x4000)  # arm64
        body = bytearray(b"\x00" * 0x8000)
        body[0:len(fat)] = fat
        fat_path = tmp_path / "fat.dylib"
        fat_path.write_bytes(bytes(body) + payload + b"\x00" * 0x100)
        assert senddirect.slice_arm64_sha256(fat_path) == hashlib.sha256(payload).hexdigest()
        thin = struct.pack("<I", 0xFEEDFACF) + payload[4:]
        thin_path = tmp_path / "thin.dylib"
        thin_path.write_bytes(thin)
        assert senddirect.slice_arm64_sha256(thin_path) == hashlib.sha256(thin).hexdigest()
        other = tmp_path / "other.bin"
        other.write_bytes(b"NOTMACHO" * 8)
        assert senddirect.slice_arm64_sha256(other) is None

    def test_callable_for_send_requires_full_recipe(self, tmp_path: Path) -> None:
        _write_anchor(tmp_path)
        table = senddirect.load_anchor_table(tmp_path)
        assert table.callable_for_send() is True
        assert table.queue_delta == 0x1C0
        assert table.send_entry == 0x1234567
        base = json.loads(json.dumps(ANCHOR_FIXTURE))
        base["offsets"]["service_ptr_mode"] = None
        home2 = tmp_path / "h2"
        _write_anchor(home2, base)
        assert senddirect.load_anchor_table(home2).callable_for_send() is False


class TestCleanupSafety:
    """S15 事故回归测:早失败路径的 finally 绝不触碰 cwd(2026-10-15 判例:
    ``Path()``→``.`` 的 rmtree 曾整删仓库;run_dir 现 None 起步+临时目录门)。"""

    def test_early_failure_leaves_cwd_untouched(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import os

        workdir = tmp_path / "cwd-sentinel"
        workdir.mkdir()
        (workdir / "keep.txt").write_text("must-survive", encoding="utf-8")
        previous_cwd = os.getcwd()
        os.chdir(workdir)
        try:
            home = _direct_env(monkeypatch, tmp_path, anchor=None)  # 锚定表缺位=早失败
            _fake_lldb(monkeypatch, {})
            exit_code, payload = run_cli(
                ["send_direct", "filehelper", "--file", "-"],
                monkeypatch, home, stdin_text="嘻嘻",
            )
            assert exit_code == 24
        finally:
            os.chdir(previous_cwd)
        assert (workdir / "keep.txt").read_text(encoding="utf-8") == "must-survive"
        # 缺省清理原语:None/相对路径/仓库路径都不进 rmtree。
        senddirect._cleanup_run_dir(None)
        senddirect._cleanup_run_dir(Path("relative-dir"))
        senddirect._cleanup_run_dir(Path("/Users/definitely/not/tmp"))
        assert (workdir / "keep.txt").exists()

    def test_cleanup_removes_owned_tempdir(self, tmp_path: Path) -> None:
        import tempfile

        owned = Path(tempfile.mkdtemp(prefix="wechat-bridge-send-direct-test-"))
        (owned / "x").write_text("1", encoding="utf-8")
        senddirect._cleanup_run_dir(owned)
        assert not owned.exists()


class TestRequestOffsetEncoding:
    """装机实证 bug 回归锁(2026-10-15 收尾验收发现):

    桥侧 request 的 ``anchor_offset`` 曾以裸 int 直传,而 lldb 内探针按
    ``int(str(x), 16)`` 二次十六进制解析——0x490fb20(=76631072)被误读为
    0x76610336,装机 dry-run 实证踩中 anchor_region 假拒(单测桩回放
    哨兵不跑真探针,故原 36 测未拦)。双侧修复:桥侧统一 ``0x`` 串形态,
    探针侧 :func:`_hex_int` 宽容解析(int 直收)。
    """

    def test_request_anchor_offsets_are_0x_strings(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(
            monkeypatch, {"preflight_ok": True, "armed": True, "done": 0}
        )
        exit_code, _payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        anchor = recorded["runs"][0]["request"]["anchor"]
        # 全偏移字段一律 0x 串形态(探针 _hex_int 兼容,但桥侧出口钉死串)。
        assert anchor["anchor_offset"] == "0x490fb20"
        assert anchor["queue_delta"] == "0x1c0"
        call = recorded["runs"][0]["request"]["call"]
        assert call["send_entry"] == "0x1234567"

    def test_probe_hex_int_tolerates_int_and_0x_string(self) -> None:
        # 探针顶层零 lldb 依赖,可直接导入(装载路径 = lldb 进程内,此处单测纯解析)。
        import wechat_bridge.senddirect_probe as probe

        # int 直收:76631072 绝不被按 16 再解析成 0x76610336(装机 bug 原形态)。
        assert probe._hex_int(76631072, "anchor_offset") == 76631072
        assert probe._hex_int(0x490FB20, "anchor_offset") == 0x490FB20
        # 0x 串与裸 hex 串同值;0x 前缀大小写不敏感。
        assert probe._hex_int("0x490fb20", "anchor_offset") == 0x490FB20
        assert probe._hex_int("0X490FB20", "anchor_offset") == 0x490FB20
        assert probe._hex_int("490fb20", "anchor_offset") == 0x490FB20
        # 非法形态 → PreflightFail(reason=request_shape),fail-closed。
        with pytest.raises(probe.PreflightFail) as excinfo:
            probe._hex_int("not-hex!", "anchor_offset")
        assert excinfo.value.reason == "request_shape"
        with pytest.raises(probe.PreflightFail):
            probe._hex_int(True, "anchor_offset")
