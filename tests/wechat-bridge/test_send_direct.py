"""send_direct 直发通道单测(task 10-14-wechat-sendmsg-direct design-阶段3
§6 + §2.7 终版模型)。

全桩离线(§6 门禁纪律):lldb 全桩 = monkeypatch ``senddirect.run_lldb_batch``
回放哨兵协议;探针 capture 段经 ``sys.modules["lldb"]`` 假模块桩测(命中-
禁用-构造-调用序);localdb/目标解析照 test_bridge_cli 判例 mock;时钟/
sleep 注入(回执退避不真等)。真实 lldb/微信路径在 e2e 门控件之外,本文件
零微信零 attach 零发送。

§6 对账:1 门关/未知键/形状;2 版本门夹具→24+未调用+rollback;3 cmd 工件
golden(唯一碰微信内存的产物;§2.7 模板直调模型三槽补丁);4 快乐路载荷+
dry-run 零状态写入;5 17/30/dedup/14/目标/空正文/双长度门;6 跨通道互锁;
7 codes 24+doctor 三态;8 冻结分支(§5 预案);另附 S15 事故回归测。
§2.7 对账:capture_call 接线(request 面/触发序/哨兵面/锚定回填/失败族
observe_timeout=30·进程退出=10·expr 失败=call_failed)。
"""

from __future__ import annotations

import json
import sys
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

#: 阶段3 §2.7 终版锚定表夹具(observe_bp 形态,镜像装机真表:send_entry=
#: F_exec 0x83e394、queue_delta=0、svc_invariants 待 capture 轮回填)。
ANCHOR_FIXTURE: dict = {
    "schema": 3,
    "wechat_version": "4.1.15",
    "dylib_arm64_slice_sha256": "aa" * 32,
    "anchor_offset": "0x490fb20",
    "anchor_bytes_hex": "ffc305d1fc6f14a9f44f15a9fd7b16a9",
    "offsets": {
        "pump_resume": None,
        "enqueue_a": "0x83e394",
        "enqueue_b": "0xa5ed0",
        "send_entry": "0x83e394",
        "arg_abi": {
            "peer_slot": "msgctx+0x08",
            "body_slot": "msgctx+0x48",
            "display_slot": "msgctx+0x130",
            "string_form": "inline23_rawlen",
            "by_value": False,
            "buffer_mode": "template_capture_same_session",
        },
        "service_ptr_mode": "observe_bp",
        "service_global_off": None,
        "queue_selector": "enqueue_a",
        "queue_delta": "0x0",
        "svc_vtable_off": "0x9c516b8",
        "svc_invariants_hex": None,
    },
}

#: §2.7 事实输入的模板夹具参数(与装机锚定表同源:cap5 直捕形态)。
SLIDE = 0x12B0E8000
CTX_ADDR = 0x8A3913C18
CTX_VTABLE_OFF = 0x9C516B8


def _template_fixture(
    *,
    flag: int = 1,
    peer: bytes = b"filehelper",
    body: bytes = "嘻嘻~cap".encode("utf-8"),
    display: bytes = "文件传输助手".encode("utf-8"),
) -> bytes:
    """§2.7 模板夹具:0x230B,flag@+0,三 inline23 槽(peer/body/display)。"""

    def _inline23_slot(encoded: bytes) -> bytes:
        return bytes(encoded) + b"\x00" * (23 - len(encoded)) + bytes([len(encoded)])

    template = bytearray(senddirect.TEMPLATE_BYTES)
    template[0] = flag
    template[0x08 : 0x08 + 24] = _inline23_slot(peer)
    template[0x48 : 0x48 + 24] = _inline23_slot(body)
    template[0x130 : 0x130 + 24] = _inline23_slot(display)
    return bytes(template)


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

    script 键:preflight_ok(bool)/preflight_fail(reason)/capture_armed(bool)/
    armed(bool)/done(call_rc)/error({stage,detail})/timed_out/killed/rc/
    trigger_error(异常)/trigger_fails(bool)。
    """
    recorded: dict = {"runs": [], "on_armed_called": 0, "triggers": []}

    def fake_run(
        lldb_path, cmd_path, run_dir, request_path, *, timeout_s, grace_s,
        on_armed=None, poll_s=0.2, sleep=None, monotonic=None, trigger=None,
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
            preflight = {"slide": SLIDE, "svc": CTX_ADDR, "attach_ms": 5}
            if script.get("capture_invariants_hex"):
                preflight["svc_invariants_hex"] = script["capture_invariants_hex"]
            (run / "PREFLIGHT_OK.json").write_text(
                json.dumps(preflight), encoding="utf-8"
            )
        if script.get("capture_armed") and trigger is not None:
            # 真驱动序回放:探针布防哨兵 → 桥侧放触发(§2.7 时序)。
            (run / "CAPTURE_ARMED.json").write_text(json.dumps({"t": 0}), encoding="utf-8")
            try:
                recorded["triggers"].append(trigger())
            except BaseException as exc:  # noqa: BLE001 - 同真驱动捕获面
                recorded["trigger_error"] = exc
        armed = bool(script.get("armed", False))
        if armed:
            (run / "ARMED.json").write_text(json.dumps({"t": 0}), encoding="utf-8")
            if on_armed is not None:
                recorded["on_armed_called"] += 1
                on_armed()
        if "done" in script:
            (run / "DONE.json").write_text(
                json.dumps({"call_rc": script["done"], "alive": True}), encoding="utf-8"
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
            trigger_error=recorded.get("trigger_error"),
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
        assert run["request"]["mode"] == "capture_call"  # 请求面在,probe 拒调
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
    """§6-3 + §2.7:cmd 工件 golden(唯一碰微信内存的产物;纯函数直测)。"""

    def test_call_expr_template_literal_three_slots_and_refcount_zero(self) -> None:
        template = _template_fixture()
        expr = senddirect.build_call_expr(
            0x83E394, SLIDE, CTX_ADDR,
            template,
            b"filehelper", "嘻嘻".encode("utf-8"), "文件传输助手".encode("utf-8"),
        )
        assert expr.startswith("(int)({\n")
        # 模板 560B 十进制字面量逐字节对账(§2.7:dump x1 起 0x230B 原样进 expr;
        # 行尾闭**单**括号 `};`——质询轮 P0 判例:`}};` 是 f-string 转义惯例
        # 泄漏进普通串拼接段,真 lldb 解析必败于列 1152)。
        assert (
            f"  unsigned char msgctx[560] = {{"
            + ",".join(str(v) for v in template) + "};" in expr
        )
        # 三槽补丁(inline23:memset 清槽 → memcpy 装值 → 末字节裸长度;
        # len=**UTF-8 字节数**非字符数——嘻嘻=2 字符 6 字节)。
        # memset/memcpy 一律 (void) cast(质询轮 F1→F2 实弹:lldb 表达式语境
        # 无 libc 声明,裸调用拒析 "unknown return type; cast the call")。
        assert (
            "  (void)memset(msgctx+8,0,24); (void)memcpy(msgctx+8,"
            "(unsigned char[]){102,105,108,101,104,101,108,112,101,114},10); "
            "msgctx[8+23]=10;" in expr
        )
        assert (
            "  (void)memset(msgctx+0x48,0,24); (void)memcpy(msgctx+0x48,"
            "(unsigned char[]){229,152,187,229,152,187},6); "
            "msgctx[0x48+23]=6;" in expr
        )
        assert (
            "  (void)memset(msgctx+0x130,0,24); (void)memcpy(msgctx+0x130,"
            "(unsigned char[]){230,150,135,228,187,182,228,188,160,232,190,147,"
            "229,138,169,230,137,139},18); msgctx[0x130+23]=18;" in expr
        )
        # +0x228 置 0 跳 retain(§2.7:双 null 守卫实证安全)。
        assert "  *(long*)(msgctx+0x228) = 0;" in expr
        # 调用形态 = F_exec(ctx, msgctx):地址=slide+send_entry 代入算术。
        call_addr = SLIDE + 0x83E394
        assert f"((int(*)(void*,void*))0x{call_addr:x})" in expr
        assert f"((void*)0x{CTX_ADDR:x}, (void*)msgctx);" in expr

    def test_call_expr_statement_shape_balanced(self) -> None:
        # 结构性守门(P0「golden 与实现同期手写」盲区的补面):括号配平、
        # 无 `}}` 残迹、每语句行以 `;` 收尾——对非法 C 的整类形态设防。
        expr = senddirect.build_call_expr(
            0x83E394, SLIDE, CTX_ADDR, _template_fixture(),
            b"filehelper", "嘻嘻".encode("utf-8"), "文件传输助手".encode("utf-8"),
        )
        assert expr.count("{") == expr.count("}")
        assert "}}" not in expr
        for line in expr.splitlines():
            stripped = line.strip()
            if stripped and stripped not in ("(int)({", "})"):
                assert stripped.endswith(";"), line

    def test_call_expr_rejects_bad_template(self) -> None:
        template = _template_fixture()
        with pytest.raises(ValueError, match="560"):
            senddirect.build_call_expr(
                0x83E394, SLIDE, CTX_ADDR, template[:-1],
                b"filehelper", b"x", b"y",
            )
        with pytest.raises(ValueError, match="标志字节"):
            senddirect.build_call_expr(
                0x83E394, SLIDE, CTX_ADDR, _template_fixture(flag=0),
                b"filehelper", b"x", b"y",
            )

    def test_call_expr_inline23_gates_are_utf8_byte_counts(self) -> None:
        template = _template_fixture()
        # peer 24B(8 汉字 username 夹具)→ 拒;display 24B → 拒;
        # body 24B → 拒(长度=字节数非字符数,§2.0 定则)。
        with pytest.raises(ValueError, match="peer"):
            senddirect.build_call_expr(
                0x83E394, SLIDE, CTX_ADDR, template,
                "嘻嘻嘻嘻嘻嘻嘻嘻".encode("utf-8"), b"x", b"y",
            )
        with pytest.raises(ValueError, match="body"):
            senddirect.build_call_expr(
                0x83E394, SLIDE, CTX_ADDR, template,
                b"filehelper", "嘻嘻嘻嘻嘻嘻嘻嘻".encode("utf-8"), b"y",
            )
        with pytest.raises(ValueError, match="display"):
            senddirect.build_call_expr(
                0x83E394, SLIDE, CTX_ADDR, template,
                b"filehelper", b"x", "嘻嘻嘻嘻嘻嘻嘻嘻".encode("utf-8"),
            )

    def test_trigger_body_variant_must_differ_from_direct_body(self) -> None:
        # 回执对账按 (username, squash(body)) 匹配——触发变体与直发正文
        # squash 同形=假绿面(质询轮 P1 实证:stdin 尾随 \n 形态)。
        assert senddirect.trigger_body_for("嘻嘻") == "嘻嘻~cap"
        assert senddirect.trigger_body_for("嘻嘻~cap") == "嘻嘻~cap2"
        assert senddirect.trigger_body_for("嘻嘻~cap2") == "嘻嘻~cap"
        # squash 互斥:去全部空白后同形者也必须避开。
        from wechat_bridge.sendui import squash

        assert senddirect.trigger_body_for("嘻嘻~cap\n") == "嘻嘻~cap2"
        assert senddirect.trigger_body_for(" 嘻嘻~cap2 ") == "嘻嘻~cap"
        assert senddirect.trigger_body_for("嘻 嘻 ~ c a p\n\n") == "嘻嘻~cap2"
        for variant in senddirect.TRIGGER_BODY_VARIANTS:
            assert len(variant.encode("utf-8")) <= senddirect.MAX_INLINE_STRING_BYTES
        # 终局自证:所选变体与直发正文的 squash 形态必互异。
        for body in ("嘻嘻", "嘻嘻~cap\n", " 嘻嘻~cap2 ", "嘻嘻~cap3", "哈"):
            assert squash(senddirect.trigger_body_for(body)) != squash(body)

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
        import wechat_bridge.sendui as sendui

        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(
            monkeypatch, {"capture_armed": True, "armed": True, "done": 0}
        )
        trigger_calls: list[dict] = []

        def _trigger_stub(config, target, body, **kwargs):
            # CLI 触发闭包终点 = ax.send_text → sendui.send_text(既有链)。
            trigger_calls.append(
                {
                    "username": target.username,
                    "display_name": target.display_name,
                    "search_term": target.search_term,
                    "body": body,
                    "receipt_query": kwargs.get("receipt_query"),
                    "on_armed": kwargs.get("on_armed"),
                }
            )
            return {"send": {"sent": True, "channel": "ax"}}

        monkeypatch.setattr(sendui, "send_text", _trigger_stub)
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
        # 触发序(§2.7):CAPTURE_ARMED 哨兵后才放触发;触发经既有 send 链
        # 到 filehelper;变体与直发正文 squash 互斥(回执对账防假绿)。
        # 触发不挂回执轮询(质询轮 P3:缩触发线程寿命,失败路径 join 能
        # 覆盖 sendui finally 的剪贴板复原)。
        assert len(trigger_calls) == 1
        assert trigger_calls[0]["username"] == "filehelper"
        # 触发目标=解析态(2026-10-15 装机实证 bug 回归面:合成
        # display_name=""/search_term="filehelper" 形态搜索浮窗无本地
        # 分区锚 → navigate 零候选 3 连败,触发零出站 → observe_timeout)。
        assert trigger_calls[0]["display_name"] == "文件传输助手"
        assert trigger_calls[0]["body"] == "嘻嘻~cap"
        assert trigger_calls[0]["receipt_query"] is None
        assert trigger_calls[0]["on_armed"] is None
        # 调用载荷面:peer/body/display 三槽 + capture needle 逐字节进 request。
        request = recorded["runs"][0]["request"]
        assert request["mode"] == "capture_call"
        assert request["call"]["peer"] == [102, 105, 108, 101, 104, 101, 108, 112, 101, 114]
        assert request["call"]["body"] == [229, 152, 187, 229, 152, 187]
        assert request["call"]["display"] == list("文件传输助手".encode("utf-8"))
        assert request["call"]["send_entry"] == "0x83e394"
        assert request["capture"]["needle"] == list("嘻嘻~cap".encode("utf-8"))
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

    def test_display_name_over_23_bytes_rejected(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        # §2.7 display 槽(+0x130)同为 inline23:12 汉字=36B → 宁拒不裁
        # (错裁展示名不如整条走 send_text)。
        target = SendTarget(
            username="wxid_ok123", alias=None, display_name="名" * 12, search_term="x"
        )
        home = _direct_env(monkeypatch, tmp_path)
        _db_mocks(monkeypatch, target=target)
        recorded = _fake_lldb(monkeypatch, {})
        exit_code, payload = run_cli(
            ["send_direct", "wxid_ok123", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_direct_target_too_long"
        assert "展示名" in payload["error"]["message"]
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
        # §2.7 终版:send_entry + observe_bp + svc_vtable_off 即就绪
        # (svc_invariants 可缺 = capture 轮回填)。
        assert table.callable_for_send() is True
        assert table.send_entry == 0x83E394
        assert table.queue_delta == 0x0
        assert table.svc_invariants is None
        # 缺 send_entry → 不就绪。
        no_entry = json.loads(json.dumps(ANCHOR_FIXTURE))
        no_entry["offsets"]["send_entry"] = None
        home2 = tmp_path / "h2"
        _write_anchor(home2, no_entry)
        assert senddirect.load_anchor_table(home2).callable_for_send() is False
        # 旧模型 global 作废(§2.7:svc 全局槽不存在)→ 不就绪。
        legacy = json.loads(json.dumps(ANCHOR_FIXTURE))
        legacy["offsets"]["service_ptr_mode"] = "global"
        legacy["offsets"]["service_global_off"] = "0x9c61f58"
        home3 = tmp_path / "h3"
        _write_anchor(home3, legacy)
        assert senddirect.load_anchor_table(home3).callable_for_send() is False


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
        assert anchor["queue_delta"] == "0x0"
        call = recorded["runs"][0]["request"]["call"]
        assert call["send_entry"] == "0x83e394"

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


# ============================================================================
# §2.7 capture_call:探针 capture 段桩测(命中-禁用-构造-调用序)+ 失败族
# ============================================================================


def _capture_harness(
    tmp_path: Path,
    *,
    template: bytes | None = None,
    needle: bytes = "嘻嘻~cap".encode("utf-8"),
    stray: bool = True,
    ctx_vtable_off: int = CTX_VTABLE_OFF,
    exit_after_expr: bool = False,
    expr_ok: bool = True,
):
    """假 lldb 会话装配:sys.modules 注入 + 内存图 + 动作序记录。

    内存图:slide+anchor_offset(锚字节)/ctx(vtable+不变量)/x1(模板)/
    stray_x1(无 needle 杂散块)。命中序: stray(可选)→ hit。
    """
    import hashlib
    import types

    if template is None:
        template = _template_fixture()
    slide = SLIDE
    ctx = CTX_ADDR
    x1 = 0x16D768288
    stray_x1 = 0x16D7678D8
    anchor_bytes = bytes.fromhex(ANCHOR_FIXTURE["anchor_bytes_hex"])
    invariants = bytes(range(24))
    memory: dict[int, bytes] = {
        slide + 0x490FB20: anchor_bytes,
        ctx: (slide + ctx_vtable_off).to_bytes(8, "little"),
        ctx + 8: invariants,
        x1: template,
        stray_x1: b"\x00" * 128 + b"filehelper" + b"\x00" * 64,  # 无 needle
    }
    actions: list[str] = []
    stops: list[int] = ([stray_x1] if stray else []) + [x1]
    holder: dict = {}

    class _BP:
        def __init__(self, addr: int) -> None:
            self.addr = addr
            self.enabled = True

        def SetEnabled(self, on: bool) -> None:
            self.enabled = on
            actions.append("bp_disable" if not on else "bp_enable")

        def GetID(self) -> int:
            return 77

    class _Frame:
        def __init__(self, regs: dict | None = None) -> None:
            self.regs = regs or {}

        def FindRegister(self, name: str):
            if name not in self.regs:
                return None
            return types.SimpleNamespace(
                IsValid=lambda: True, GetValueAsUnsigned=lambda v=self.regs[name]: v
            )

        def EvaluateExpression(self, expr_text, options):
            actions.append("expr_eval")
            harness["expr"] = expr_text
            if exit_after_expr and "proc" in holder:
                holder["proc"].exited = True  # postflight 存活断言面(§2.7)
            if not expr_ok:
                return types.SimpleNamespace(IsValid=lambda: False)
            return types.SimpleNamespace(
                IsValid=lambda: True,
                GetError=lambda: types.SimpleNamespace(Success=lambda: True),
                GetValueAsSigned=lambda: 0,
            )

    class _Thread:
        def __init__(self, frame: _Frame | None) -> None:
            self.frame = frame

        def GetStopReason(self):
            return fake_lldb.eStopReasonBreakpoint if self.frame else 0

        def GetFrameAtIndex(self, _i: int):
            return self.frame

        def GetSelectedFrame(self):
            return self.frame

    class _Proc:
        def __init__(self) -> None:
            self.stopped = True
            self.current: _Thread | None = _Thread(_Frame({"x0": ctx, "x1": x1}))
            self.exited = False

        def IsValid(self):
            return True

        def GetState(self):
            if self.exited:
                return fake_lldb.eStateExited
            return fake_lldb.eStateStopped if self.stopped else fake_lldb.eStateRunning

        def Continue(self):
            actions.append("continue")
            if stops:
                addr = stops.pop(0)
                self.current = _Thread(_Frame({"x0": ctx, "x1": addr}))
                self.stopped = True
            else:
                self.current = None
                self.stopped = False
            return True

        def ReadMemory(self, addr, size, _err):
            data = memory.get(addr)
            return data[:size] if data is not None else None

        def GetSelectedThread(self):
            return _Thread(_Frame({}))  # expr 段选中线程(无寄存器面)

        def __iter__(self):
            return iter([self.current] if self.current else [])

    class _Section:
        def IsValid(self):
            return True

        def GetByteSize(self):
            return 0x9000000

        def GetLoadAddress(self, _target):
            return slide

    class _Module:
        file = None  # 由 harness 外注入(thin dylib 磁盘件)

        def FindSection(self, name):
            return _Section() if name == "__TEXT" else types.SimpleNamespace(IsValid=lambda: False)

        def GetObjectFileHeaderAddress(self):
            return types.SimpleNamespace(GetLoadAddress=lambda _t: slide)

    _Module.file = types.SimpleNamespace(basename="wechat.dylib", fullpath="")
    bps: dict[int, _BP] = {}

    class _Target:
        def module_iter(self):
            return [_Module()]

        def GetProcess(self):
            return holder["proc"]

        def BreakpointCreateByAddress(self, addr):
            actions.append(f"bp_create@{addr:#x}")
            bp = _BP(addr)
            bps[bp.GetID()] = bp
            return bp

        def BreakpointDelete(self, bp_id):
            actions.append("bp_delete")

    proc = _Proc()
    holder["proc"] = proc

    class _SBError:
        def Success(self):
            return True

    class _SBExpressionOptions:
        def SetTimeoutInMicroSeconds(self, _us):
            return None

        def SetUnwindOnError(self, _v):
            return None

        def SetIgnoreBreakpoints(self, _v):
            return None

    fake_lldb = types.SimpleNamespace(
        debugger=types.SimpleNamespace(
            GetSelectedTarget=lambda: _Target(),
            # async 转换记入 actions(2026-10-15 装机实证 bug 回归面:sync
            # 缺省下 Continue 阻塞 → CAPTURE_ARMED 永不落 → 触发自死锁)。
            SetAsync=lambda on: actions.append("async_on" if on else "async_off"),
        ),
        eStateStopped=5,
        eStateRunning=6,
        eStateExited=10,
        eStateInvalid=0,
        eStopReasonBreakpoint=1,
        SBError=_SBError,
        SBExpressionOptions=_SBExpressionOptions,
    )
    thin = b"\xcf\xfa\xed\xfe" + b"\x11" * 2048
    thin_path = tmp_path / "wechat.dylib"
    thin_path.write_bytes(thin)
    _Module.file.fullpath = str(thin_path)
    harness = {
        "fake_lldb": fake_lldb,
        "actions": actions,
        "proc": proc,
        "memory": memory,
        "expr": None,
        "slide": slide,
        "ctx": ctx,
        "x1": x1,
        "template": template,
        "needle": needle,
        "slice_sha256": hashlib.sha256(thin).hexdigest(),
        "invariants_hex": invariants.hex(),
    }
    return harness


def _capture_request(harness) -> dict:
    """capture_call request 夹具(与桥侧 execute_send 出口同形)。"""
    return {
        "mode": "capture_call",
        "anchor": {
            "slice_sha256": harness["slice_sha256"],
            "anchor_offset": "0x490fb20",
            "anchor_bytes_hex": ANCHOR_FIXTURE["anchor_bytes_hex"],
            "enqueue_a": "0x83e394",
            "enqueue_b": "0xa5ed0",
            "send_entry": "0x83e394",
            "service_ptr_mode": "observe_bp",
            "service_global_off": None,
            "queue_selector": "enqueue_a",
            "queue_delta": "0x0",
            "svc_vtable_off": f"0x{CTX_VTABLE_OFF:x}",
            "svc_invariants_hex": None,
        },
        "capture": {"needle": list(harness["needle"])},
        "call": {
            "send_entry": "0x83e394",
            "peer": list(b"filehelper"),
            "body": list("嘻嘻".encode("utf-8")),
            "display": list("文件传输助手".encode("utf-8")),
        },
    }


class TestProbeCaptureSegment:
    """探针 capture 段桩测(§2.7:命中-禁用-构造-调用序 + 判别门)。"""

    def test_dry_run_gates_only_zero_breakpoint_infinite_rerunnable(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """dry_run 真探针路径(质询轮 P1:旧径在 observe_bp 锚定表下等自然
        任务 10s → 空闲微信必败 observe_timeout → 恒 30,「可无限重跑」
        契约破)。新径=门即止:零断点零等待零触发(本测试不桩
        run_lldb_batch,直接驱动真 probe.run + 假 lldb)。"""
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path)
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        request = _capture_request(harness)
        request["mode"] = "dry_run"
        request.pop("capture")
        request.pop("call")
        request_path = run_dir / "request.json"
        request_path.write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
        monkeypatch.setattr(probe, "RUN_DIR", str(run_dir))
        monkeypatch.setattr(probe, "REQUEST_PATH", str(request_path))
        monkeypatch.setitem(sys.modules, "lldb", harness["fake_lldb"])
        probe.run()
        # 门即止:门哨兵在,零断点动作,无 capture/call 哨兵。
        preflight = json.loads((run_dir / "PREFLIGHT_OK.json").read_text(encoding="utf-8"))
        assert set(preflight) == {"slide", "attach_ms", "slice_sha256"}
        assert harness["actions"] == []  # 零 bp_create/continue(§2.0 零断点)
        assert not (run_dir / "CAPTURE_ARMED.json").exists()
        assert not (run_dir / "ARMED.json").exists()
        assert not (run_dir / "PREFLIGHT_FAIL.json").exists()

    def test_full_run_hit_disable_construct_call_sequence(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path)
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        request_path = run_dir / "request.json"
        request_path.write_text(
            json.dumps(_capture_request(harness), ensure_ascii=False), encoding="utf-8"
        )
        monkeypatch.setattr(probe, "RUN_DIR", str(run_dir))
        monkeypatch.setattr(probe, "REQUEST_PATH", str(request_path))
        monkeypatch.setitem(sys.modules, "lldb", harness["fake_lldb"])

        probe.run()

        # 命中-禁用-构造-调用序(§2.7 收兵序:命中即禁断点→删除,直调零断点)。
        actions = harness["actions"]
        assert actions[0] == f"bp_create@{SLIDE + 0x83E394:#x}"
        # async 纪律(2026-10-15 装机实证 bug 回归面):首个 continue 前
        # 必切 async(命令文件批缺省 sync → Continue 阻塞至停 →
        # CAPTURE_ARMED 永不落 → 触发自死锁);capture 收兵恢复 sync。
        assert actions[1] == "async_on"
        assert actions[2] == "continue"
        assert "async_off" in actions
        assert actions.index("async_off") > len(actions) - 1 - actions[::-1].index("continue")
        assert actions.index("async_off") < actions.index("expr_eval")
        assert "bp_disable" in actions and "bp_delete" in actions
        assert actions.index("bp_disable") < actions.index("expr_eval")
        assert actions.index("bp_delete") < actions.index("expr_eval")
        # 杂散命中(needle 未中)被继续等待:两次 continue 在 expr 之前。
        assert actions.count("continue") >= 2
        assert actions[-1] == "expr_eval"
        # CAPTURE_ARMED 哨兵(桥侧放触发的时序锚)。
        assert (run_dir / "CAPTURE_ARMED.json").is_file()
        # PREFLIGHT_OK:svc=ctx(x0)、vtable 相对量、不变量采集、模板只记
        # 指纹(键集钉死——哨兵零内容材料,§5 隐私)。
        preflight = json.loads((run_dir / "PREFLIGHT_OK.json").read_text(encoding="utf-8"))
        import hashlib as _hashlib

        assert set(preflight) == {
            "slide", "svc", "attach_ms", "slice_sha256",
            "svc_vtable_off", "svc_invariants_hex",
            "template_sha256", "template_len",
        }
        assert preflight["svc"] == harness["ctx"]
        assert preflight["svc_vtable_off"] == CTX_VTABLE_OFF
        assert preflight["svc_invariants_hex"] == harness["invariants_hex"]
        assert preflight["template_len"] == 560
        assert preflight["template_sha256"] == _hashlib.sha256(harness["template"]).hexdigest()
        # ARMED 先于 expr;DONE 带返回值+存活。
        assert (run_dir / "ARMED.json").is_file()
        done = json.loads((run_dir / "DONE.json").read_text(encoding="utf-8"))
        assert done["call_rc"] == 0 and done["alive"] is True
        # expr 工件=桥侧 build_call_expr 同一函数产物(单一出处):三槽补丁+
        # +0x228 置零+模板 560B 字面量+F_exec(ctx,msgctx) 形态。
        expr = harness["expr"]
        assert expr.startswith("(int)({\n")
        assert f"unsigned char msgctx[560] = {{" in expr
        assert "msgctx[8+23]=10;" in expr
        assert "msgctx[0x48+23]=6;" in expr
        assert "msgctx[0x130+23]=18;" in expr
        assert "*(long*)(msgctx+0x228) = 0;" in expr
        call_addr = SLIDE + 0x83E394
        assert f"((void*)0x{harness['ctx']:x}, (void*)msgctx);" in expr
        assert f"0x{call_addr:x}" in expr
        # 无 PREFLIGHT_FAIL / ERROR。
        assert not (run_dir / "PREFLIGHT_FAIL.json").exists()
        assert not (run_dir / "ERROR.json").exists()

    def test_stray_hits_without_needle_are_skipped(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        # 判别门:杂散块(含 filehelper 无 needle)绝不取首击(cap5 纪律)。
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path, stray=True)
        _inject_fake_lldb(monkeypatch, harness)
        ctx, template, vtable_off, invariants = probe._capture_template(
            _harness_target(harness), harness["proc"], _capture_request(harness), SLIDE
        )
        assert ctx == harness["ctx"]
        assert template == harness["template"]
        assert vtable_off == CTX_VTABLE_OFF
        assert invariants.hex() == harness["invariants_hex"]
        assert harness["actions"].count("continue") == 2  # 初次 continue + 杂散后续等

    def test_observe_timeout_when_no_hit(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path, stray=False)
        _inject_fake_lldb(monkeypatch, harness)
        # 掏空停止脚本:Continue 后永不停止 → 观察窗超时(窗宽钉小防真等)。
        harness["proc"].Continue = lambda: (  # type: ignore[method-assign]
            harness["actions"].append("continue"),
            setattr(harness["proc"], "stopped", False),
            setattr(harness["proc"], "current", None),
        )
        monkeypatch.setattr(probe, "CAPTURE_WAIT_S", 0.15)
        with pytest.raises(probe.PreflightFail) as excinfo:
            probe._capture_template(
                _harness_target(harness), harness["proc"], _capture_request(harness), SLIDE
            )
        assert excinfo.value.reason == "observe_timeout"
        # 断点仍被禁用+删除(finally 收兵序不因失败省略)。
        assert "bp_disable" in harness["actions"] and "bp_delete" in harness["actions"]

    def test_process_exit_during_capture(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path, stray=False)
        harness["proc"].exited = True
        _inject_fake_lldb(monkeypatch, harness)
        with pytest.raises(probe.PreflightFail) as excinfo:
            probe._capture_template(
                _harness_target(harness), harness["proc"], _capture_request(harness), SLIDE
            )
        assert excinfo.value.reason == "observe_process_state"

    def test_bad_template_flag_rejected(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path, template=_template_fixture(flag=0))
        _inject_fake_lldb(monkeypatch, harness)
        with pytest.raises(probe.PreflightFail) as excinfo:
            probe._capture_template(
                _harness_target(harness), harness["proc"], _capture_request(harness), SLIDE
            )
        assert excinfo.value.reason == "capture_template_flag"

    def test_vtable_mismatch_rejected(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path, ctx_vtable_off=0x1111111)
        _inject_fake_lldb(monkeypatch, harness)
        with pytest.raises(probe.PreflightFail) as excinfo:
            probe._capture_template(
                _harness_target(harness), harness["proc"], _capture_request(harness), SLIDE
            )
        assert excinfo.value.reason == "svc_vtable_mismatch"

    def test_missing_needle_payload_rejected(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path)
        _inject_fake_lldb(monkeypatch, harness)
        request = _capture_request(harness)
        request["capture"] = {}
        with pytest.raises(probe.PreflightFail) as excinfo:
            probe._capture_template(
                _harness_target(harness), harness["proc"], request, SLIDE
            )
        assert excinfo.value.reason == "capture_needle"

    def test_expr_failure_writes_call_error(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.senddirect_probe as probe

        harness = _capture_harness(tmp_path, expr_ok=False)
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        request_path = run_dir / "request.json"
        request_path.write_text(
            json.dumps(_capture_request(harness), ensure_ascii=False), encoding="utf-8"
        )
        monkeypatch.setattr(probe, "RUN_DIR", str(run_dir))
        monkeypatch.setattr(probe, "REQUEST_PATH", str(request_path))
        monkeypatch.setitem(sys.modules, "lldb", harness["fake_lldb"])
        probe.run()
        assert (run_dir / "ARMED.json").is_file()  # armed 时点=expr 提交前
        error = json.loads((run_dir / "ERROR.json").read_text(encoding="utf-8"))
        assert error["stage"] == "call"
        assert not (run_dir / "DONE.json").exists()

    def test_process_death_after_call_writes_call_error(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import wechat_bridge.senddirect_probe as probe

        # expr 求值后进程退出(harness 的 exit_after_expr 钩)→ postflight
        # 存活断言拦下:ERROR stage=call,DONE 不落(§2.7 postflight 形态)。
        harness = _capture_harness(tmp_path, exit_after_expr=True)
        run_dir = tmp_path / "run"
        run_dir.mkdir()
        request_path = run_dir / "request.json"
        request_path.write_text(
            json.dumps(_capture_request(harness), ensure_ascii=False), encoding="utf-8"
        )
        monkeypatch.setattr(probe, "RUN_DIR", str(run_dir))
        monkeypatch.setattr(probe, "REQUEST_PATH", str(request_path))
        monkeypatch.setitem(sys.modules, "lldb", harness["fake_lldb"])
        probe.run()
        assert "expr_eval" in harness["actions"]
        error = json.loads((run_dir / "ERROR.json").read_text(encoding="utf-8"))
        assert error["stage"] == "call"
        assert "退出" in error["detail"]
        assert not (run_dir / "DONE.json").exists()


def _harness_target(harness):
    """假 lldb target(直调 _capture_template 的轻量入口)。"""
    return harness["fake_lldb"].debugger.GetSelectedTarget()


def _inject_fake_lldb(monkeypatch: pytest.MonkeyPatch, harness) -> None:
    """探针函数内 ``import lldb`` 的桩注入(sys.modules 顶层)。"""
    monkeypatch.setitem(sys.modules, "lldb", harness["fake_lldb"])


class TestTriggerOrchestration:
    """run_lldb_batch 触发编排桩测(§2.7:CAPTURE_ARMED 哨兵后才放触发)。"""

    @staticmethod
    def _batch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, events: list):
        """假 Popen 驱动 run_lldb_batch;events 交错记录时序。"""
        import wechat_bridge.senddirect as sd

        run_dir = tmp_path / "run"
        run_dir.mkdir(exist_ok=True)
        (run_dir / "request.json").write_text("{}", encoding="utf-8")

        class _FakeProc:
            def __init__(self) -> None:
                self.rc: int | None = None

            def poll(self):
                return self.rc

            def send_signal(self, _sig):
                self.rc = -2

            def kill(self):
                self.rc = -9

            def wait(self, timeout=None):
                return self.rc

        fake = _FakeProc()
        monkeypatch.setattr(
            sd.subprocess, "Popen", lambda *a, **kw: (events.append("spawn"), fake)[1]
        )
        return sd, run_dir, fake

    def test_trigger_fires_only_after_capture_armed_sentinel(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        events: list = []
        sd, run_dir, fake = self._batch(tmp_path, monkeypatch, events=events)
        clock = {"t": 0.0}

        def _sleep(seconds: float) -> None:
            clock["t"] += seconds
            events.append("poll")
            if clock["t"] >= 0.4:
                # 探针布防哨兵在数个轮询后出现(真序:attach+门+bp+Continue)。
                # 事件标记当场落(质询轮 P2 判例:事后回读 clock 终值=空转断言)。
                if "cap_armed" not in events:
                    (run_dir / sd.CAPTURE_ARMED_NAME).write_text("{}", encoding="utf-8")
                    events.append("cap_armed")
            if clock["t"] >= 1.0:
                fake.rc = 0  # 批收兵

        def _trigger():
            events.append("trigger")

        outcome = sd.run_lldb_batch(
            "/fake/lldb", run_dir / "lldb.cmd", run_dir, run_dir / "request.json",
            sleep=_sleep, monotonic=lambda: clock["t"], trigger=_trigger,
            timeout_s=30.0,
        )
        assert outcome.returncode == 0 and outcome.trigger_error is None
        assert events[0] == "spawn"
        # 时序铁律(标记序断言):trigger 严格晚于 CAPTURE_ARMED 落盘标记
        # (若驱动序坏为「先 trigger 后哨兵」,events 序即倒置 → 此断言红)。
        assert "cap_armed" in events and "trigger" in events
        assert events.index("trigger") > events.index("cap_armed")

    def test_trigger_never_fires_without_sentinel(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        events: list = []
        sd, run_dir, fake = self._batch(tmp_path, monkeypatch, events=events)
        clock = {"t": 0.0}

        def _sleep(seconds: float) -> None:
            clock["t"] += seconds
            if clock["t"] >= 1.0:
                fake.rc = 0

        def _trigger():
            events.append("trigger")

        outcome = sd.run_lldb_batch(
            "/fake/lldb", run_dir / "lldb.cmd", run_dir, run_dir / "request.json",
            sleep=_sleep, monotonic=lambda: clock["t"], trigger=_trigger,
            timeout_s=30.0,
        )
        assert outcome.returncode == 0
        assert "trigger" not in events  # 哨兵缺失 → 触发绝不放行

    def test_trigger_error_captured_not_raised(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        events: list = []
        sd, run_dir, fake = self._batch(tmp_path, monkeypatch, events=events)
        (run_dir / sd.CAPTURE_ARMED_NAME).write_text("{}", encoding="utf-8")
        clock = {"t": 0.0}

        def _sleep(seconds: float) -> None:
            clock["t"] += seconds
            if clock["t"] >= 0.5:
                fake.rc = 0

        def _trigger():
            raise BridgeError(15, "ax 断言失败(触发链夹具)")

        outcome = sd.run_lldb_batch(
            "/fake/lldb", run_dir / "lldb.cmd", run_dir, run_dir / "request.json",
            sleep=_sleep, monotonic=lambda: clock["t"], trigger=_trigger,
            timeout_s=30.0,
        )
        # 触发链异常进 outcome.trigger_error(后台线程捕获面),守护不炸。
        assert isinstance(outcome.trigger_error, BridgeError)
        assert outcome.trigger_error.exit_code == 15


class TestCaptureCallBridge:
    """execute_send capture_call 失败族接线(§2.7 + §3.3 矩阵)。"""

    def test_capture_observe_timeout_exit_30_rollback(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(
            monkeypatch, {"preflight_fail": "observe_timeout", "detail": "25s 观察窗内未见"}
        )
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 30
        assert payload["error"]["code"] == "timeout"
        assert "观察窗" in payload["error"]["message"]
        assert recorded["on_armed_called"] == 0
        state = SendRateState(home / "wechat-localdb" / "send_state.json")
        assert state.load_last_send_epoch() is None  # armed 前 → rollback

    def test_capture_process_exit_exit_10(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        home = _direct_env(monkeypatch, tmp_path)
        _fake_lldb(
            monkeypatch, {"preflight_fail": "observe_process_state", "detail": "state=10"}
        )
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 10
        assert "capture" in payload["error"]["message"]

    def test_trigger_bridge_error_reraised_with_rollback(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import wechat_bridge.sendui as sendui

        home = _direct_env(monkeypatch, tmp_path)
        _fake_lldb(monkeypatch, {"capture_armed": True, "preflight_ok": False})

        def _trigger_boom(config, target, body, **kwargs):
            raise BridgeError(15, "触发链夹具终败")

        monkeypatch.setattr(sendui, "send_text", _trigger_boom)
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        # 触发链 BridgeError 原样透传族语义(armed 前 → rollback,无指纹)。
        assert exit_code == 15
        assert "触发链夹具终败" in payload["error"]["message"]
        state = SendRateState(home / "wechat-localdb" / "send_state.json")
        assert state.load_last_send_epoch() is None
        assert not _fingerprints(home)

    def test_trigger_succeeded_but_capture_missed_is_timeout(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        # 触发成功而 needle 未中(假绿防御面):探针 observe_timeout 收兵,
        # 桥侧 30(不是触发误报——触发 payload 不参与判定)。
        import wechat_bridge.sendui as sendui

        home = _direct_env(monkeypatch, tmp_path)
        _fake_lldb(
            monkeypatch,
            {"capture_armed": True, "preflight_fail": "observe_timeout"},
        )
        monkeypatch.setattr(
            sendui, "send_text",
            lambda config, target, body, **kw: {"send": {"sent": True}},
        )
        exit_code, payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 30
        state = SendRateState(home / "wechat-localdb" / "send_state.json")
        assert state.load_last_send_epoch() is None

    def test_invariants_backfilled_into_anchor_file(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        import wechat_bridge.sendui as sendui

        home = _direct_env(monkeypatch, tmp_path)
        monkeypatch.setattr(
            sendui, "send_text",
            lambda config, target, body, **kw: {"send": {"sent": True}},
        )
        clock = {"t": 3000.0}
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: clock["t"])
        captured = "00" * 24
        recorded = _fake_lldb(
            monkeypatch,
            {"capture_armed": True, "armed": True, "done": 0,
             "capture_invariants_hex": captured},
        )
        exit_code, _payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        anchor_path = home / "wechat-bridge" / "send-direct-anchors.json"
        anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
        assert anchor["offsets"]["svc_invariants_hex"] == captured  # §2.7 回填
        # 已锚定值不被覆盖(第二次 capture 采集值漂移 → 原值保留)。
        recorded2 = _fake_lldb(
            monkeypatch,
            {"capture_armed": True, "armed": True, "done": 0,
             "capture_invariants_hex": "ff" * 24},
        )
        assert recorded2 is not None
        import wechat_bridge.localdb as localdb

        monkeypatch.setattr(
            localdb, "query_history",
            lambda *a, **kw: {"messages": [{"text": "哈", "ts": 9999999999}]},
        )
        clock["t"] += 20.0  # 让出 G6 间隔窗(异指纹二次直发)
        exit_code, _payload = run_cli(
            ["send_direct", "filehelper", "--file", "-"],
            monkeypatch, home, stdin_text="哈",
        )
        assert exit_code == 0
        anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
        assert anchor["offsets"]["svc_invariants_hex"] == captured

    def test_default_trigger_targets_filehelper_via_ax_chain(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        # execute_send 直调面(不经 CLI):缺省触发件=合成 filehelper 目标
        # 经 ax.send_text(既有链),零 trigger_send 注入也可 mock 桩测。
        import wechat_bridge.ax as ax
        from wechat_bridge.config import BridgeConfig

        calls: list[dict] = []
        monkeypatch.setattr(
            ax, "send_text",
            lambda config, target, body, **kw: (
                calls.append({"username": target.username, "body": body}) or
                {"send": {"sent": True}},
            ),
        )
        home = tmp_path / "direct-home"
        home.mkdir(parents=True, exist_ok=True)
        _write_anchor(home)
        monkeypatch.setattr(senddirect, "wechat_pid", lambda: 4242)
        monkeypatch.setattr(senddirect, "lldb_executable", lambda: "/fake/lldb")
        monkeypatch.setattr(senddirect, "_sleep", lambda s: None)
        recorded = _fake_lldb(
            monkeypatch, {"capture_armed": True, "armed": True, "done": 0}
        )
        payload = senddirect.execute_send(
            BridgeConfig(send_direct_enabled=True), FAKE_TARGET, "嘻嘻",
            data_root=home,
            receipt_query=lambda username, body, since: True,
        )
        assert payload["send"]["sent"] is True
        assert calls == [{"username": "filehelper", "body": "嘻嘻~cap"}]
        assert recorded["runs"][0]["request"]["capture"]["needle"] == list(
            "嘻嘻~cap".encode("utf-8")
        )

    def test_dry_run_never_triggers(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.sendui as sendui

        home = _direct_env(monkeypatch, tmp_path)
        recorded = _fake_lldb(monkeypatch, {"preflight_ok": True})
        boom = lambda *a, **kw: (_ for _ in ()).throw(AssertionError("dry-run 触发了发送"))
        monkeypatch.setattr(sendui, "send_text", boom)
        exit_code, _payload = run_cli(
            ["send_direct", "filehelper", "--file", "-", "--dry-run"],
            monkeypatch, home, stdin_text="嘻嘻",
        )
        assert exit_code == 0
        assert recorded["triggers"] == []


class TestExprRealLLDBParseGate:
    """P0 回归锁(质询轮判例):expr 必须过**真 lldb 解析**——`}};` 双括号
    与未 cast 的 memset/memcpy 都是「golden 与实现同期手写」的盲区,结构
    断言只能防整类,防不了「clang 语境才暴露的」具体形态。

    门控:默认跳过(套件离线纪律,§6);显式 ``MYIA_LLDB_EXPR_E2E=1``
    时对自有 sleep 进程实弹(attach 自有进程=零微信零发送,LLDB 红线内)。
    尾调用摘除(函数指针行 → 槽长读回),真跑三槽补丁并验证 memset/memcpy
    已执行(body 槽 len 字节=6)。
    """

    def test_expr_parses_and_patches_in_real_lldb(self, tmp_path: Path) -> None:
        import os
        import shutil
        import subprocess
        import time

        if os.environ.get("MYIA_LLDB_EXPR_E2E") != "1":
            pytest.skip("真 lldb 解析门:MYIA_LLDB_EXPR_E2E=1 显式开启(自有进程,零微信)")
        lldb_path = shutil.which("lldb")
        if lldb_path is None:
            pytest.skip("lldb 不在 PATH")

        expr = senddirect.build_call_expr(
            0x83E394, SLIDE, CTX_ADDR, _template_fixture(),
            b"filehelper", "嘻嘻".encode("utf-8"), "文件传输助手".encode("utf-8"),
        )
        lines = expr.splitlines()
        call_idx = max(
            i for i, line in enumerate(lines) if "((int(*)(void*,void*))" in line
        )
        # 尾调用摘除 → 槽长读回:语句块尾表达式 = body 槽 len 字节(证明
        # memset 清槽 + memcpy 装值 + 裸长度赋值三步真执行)。
        lines[call_idx] = "  msgctx[0x48+23];"
        expr_path = tmp_path / "expr.txt"
        expr_path.write_text("\n".join(lines), encoding="utf-8")
        out_path = tmp_path / "result.json"

        driver = tmp_path / "driver.py"
        driver.write_text(
            "import json, os\n"
            "import lldb\n"
            "def run():\n"
            "    text = open(os.environ['EXPR_PATH']).read()\n"
            "    target = lldb.debugger.GetSelectedTarget()\n"
            "    proc = target.GetProcess()\n"
            "    frame = proc.GetSelectedThread().GetSelectedFrame()\n"
            "    opts = lldb.SBExpressionOptions()\n"
            "    opts.SetTimeoutInMicroSeconds(15_000_000)\n"
            "    opts.SetUnwindOnError(True)\n"
            "    opts.SetIgnoreBreakpoints(True)\n"
            "    value = frame.EvaluateExpression(text, opts)\n"
            "    ok = value.IsValid() and value.GetError().Success()\n"
            "    json.dump({'ok': ok,\n"
            "               'val': value.GetValueAsSigned() if ok else None,\n"
            "               'err': str(value.GetError()) if value.IsValid() else 'invalid'},\n"
            "              open(os.environ['EXPR_OUT'], 'w'))\n",
            encoding="utf-8",
        )
        victim = subprocess.Popen(["sleep", "60"])
        try:
            env = dict(os.environ)
            env["EXPR_PATH"] = str(expr_path)
            env["EXPR_OUT"] = str(out_path)
            cmd = tmp_path / "lldb.cmd"
            cmd.write_text(
                f"attach -p {victim.pid}\n"
                f'command script import "{driver}"\n'
                "script driver.run()\n"
                "detach\n"
                "quit\n",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [lldb_path, "-b", "-s", str(cmd)],
                capture_output=True, text=True, env=env, timeout=60,
            )
            assert out_path.is_file(), (
                f"驱动未落结果:rc={completed.returncode} "
                f"stderr={completed.stderr[-400:]}"
            )
            result = json.loads(out_path.read_text(encoding="utf-8"))
            # 解析过 + 三槽补丁真执行(body 槽 len 字节=6)。
            assert result["ok"] is True, result["err"]
            assert result["val"] == 6
        finally:
            victim.kill()
            victim.wait()
