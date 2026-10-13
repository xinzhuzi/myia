"""CLI 契约单测(design §6/§8):exit 码表、错误载荷形状、golden 基件。

golden 惯例(对齐插件 golden):改契约必同步基件;显式再生成通道 =
``MYIA_WECHAT_BRIDGE_REGEN_GOLDEN=1`` 重跑本文件(基件只经此路径刷新,
绝不静默跟随)。

全部走 mock(托盘态/全绿态注入点),CI 无微信全绿;真实客户端测试在
``test_e2e_gated.py``,``MYIA_WECHAT_E2E=1`` 才跑。
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

import wechat_bridge.codes as codes_mod
from wechat_bridge.send_state import SendRateState
from wechat_bridge.sendtarget import SendTarget

from bridge_testkit import CheckMocks, run_cli, tray_mocks

FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOLDEN = FIXTURES / "golden_cli_payloads.json"
REGEN_ENV = "MYIA_WECHAT_BRIDGE_REGEN_GOLDEN"

#: send_text 分支的确定性目标桩(DB 侧解析全 mock;filehelper 白名单形态)。
FAKE_TARGET = SendTarget(
    username="filehelper", alias=None, display_name="文件传输助手", search_term="filehelper"
)


def _send_db_mocks(monkeypatch: pytest.MonkeyPatch, target: SendTarget | None = FAKE_TARGET) -> None:
    """send_text 分支的 localdb 链 + 目标解析全 mock(CI 无微信/无本地库)。

    localdb.locate/resolve 单次解析注入(design §J-19);sendtarget.
    resolve_target 返回固定 SendTarget(真身三路解析在 test_send_target.py
    受测)。
    """
    import wechat_bridge.localdb as localdb
    import wechat_bridge.sendtarget as sendtarget

    monkeypatch.setattr(localdb, "locate_db_storage", lambda: Path("/fake-db-storage"))
    monkeypatch.setattr(
        localdb, "resolve_keys", lambda storage, *, config=None: {"k": "v"}
    )
    monkeypatch.setattr(
        sendtarget,
        "resolve_target",
        lambda config, chat_id, **kwargs: target,
    )


def _scrub(value: object, volatile: Path) -> object:
    """golden 脱挥发物:消息里的绝对路径(错误定位用)替换为 <TMP>,基件
    才能跨机器/CI 逐字节可比(运行时载荷本身不脱——人读诊断要真路径)。"""
    if isinstance(value, dict):
        return {k: _scrub(v, volatile) for k, v in value.items()}
    if isinstance(value, list):
        return [_scrub(item, volatile) for item in value]
    if isinstance(value, str):
        return value.replace(str(volatile), "<TMP>")
    return value


def _collect_golden_payloads(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """确定性场景的应答全集(golden 基件的唯一事实源)。"""
    payloads: dict[str, dict] = {}
    import wechat_bridge.localdb as _localdb

    _real_resolve_keys = _localdb.resolve_keys  # ⑤⑥⑦⑧ 用真身(mock 前保存)
    _real_locate = _localdb.locate_db_storage

    # ① 托盘态 --probe(2026-10-11 实况形状:进程在/AX 在/窗口关/库在/密钥缺)
    tray_mocks(monkeypatch)
    exit_code, payload = run_cli(["--probe"], monkeypatch, tmp_path)
    assert exit_code == 0
    payloads["probe_tray"] = payload

    # ② 托盘态 sessions list → exit 12 window_closed(UI 通道专属)
    exit_code, payload = run_cli(["sessions", "list", "--json"], monkeypatch, tmp_path)
    assert exit_code == 12
    payloads["err_window_closed"] = payload

    # ③ 频控拒发(前置全绿 + 10s 内已有发送记录)→ exit 14
    #    (适配:localdb/目标解析 mock——频控门在 sendui 之前)
    green = tray_mocks(monkeypatch, CheckMocks(window=True))
    assert green.window is True
    _send_db_mocks(monkeypatch)
    rate_home = tmp_path / "rate-home"
    SendRateState(rate_home / "wechat-localdb" / "send_state.json").record_send(now=1000.0)
    monkeypatch.setattr(
        "wechat_bridge.cli._now", lambda: 1003.0  # 10s 内(注入时钟,不真等)
    )
    exit_code, payload = run_cli(
        ["send_text", "filehelper", "--file", "-"],
        monkeypatch,
        rate_home,
        stdin_text="你好",
    )
    assert exit_code == 14
    payloads["err_send_rate_limited"] = payload

    # ④ 前置全绿 + 频控放行(独立数据根,无发送记录)→ send_text D1 已落
    # (0.8.0 三源合体;golden 注入确定性桩,真身全链在 test_send_ui.py 受测)
    _send_db_mocks(monkeypatch)
    monkeypatch.setattr(
        "wechat_bridge.sendui.send_text",
        lambda config, target, body, *, dry_run=False, on_armed=None,
        on_receipt_green=None, receipt_query=None: {
            "send": {
                "target": {"username": target.username, "display_name": target.display_name},
                "channel": "ax",
                "sent": True,
                "attempts": 1,
                "readback": "ax_value",
                "title_verify": "ax_label",
                "composer_cleared": True,
                "localdb_receipt": True,
                "post_send_verified": True,
                "post_send_note": None,
                "fingerprint_note": None,
                "elapsed_ms": 1,
            }
        },
    )
    exit_code, payload = run_cli(
        ["send_text", "filehelper", "--file", "-"],
        monkeypatch,
        tmp_path / "clean-home",
        stdin_text="你好",
    )
    assert exit_code == 0
    payloads["ok_send_text"] = payload

    # ④b 断言失败族(driver 桩抛 exit 15)→ 结构化 error 载荷
    def _focus_fail(config, target, body, *, dry_run=False, on_armed=None,
                    on_receipt_green=None, receipt_query=None):
        raise codes_mod.BridgeError(
            codes_mod.SEND_AX_FOCUS_REQUIRED,
            "发送未执行:3 次尝试均未通过断言;末次失败 发送断言超时(阶段=readback,4s 内未达成)",
            fix_hint="确认微信前台可见、目标会话存在且输入区可聚焦;辅助功能/输入监控授权给桥宿主后重试",
        )

    monkeypatch.setattr("wechat_bridge.sendui.send_text", _focus_fail)
    exit_code, payload = run_cli(
        ["send_text", "filehelper", "--file", "-"],
        monkeypatch,
        tmp_path / "clean-home-2",
        stdin_text="你好",
    )
    assert exit_code == 15
    payloads["err_send_focus_required"] = payload

    # ⑤ 本地库:定位成功 + 密钥不可得(D4)→ exit 21
    #    (恢复真 resolve_keys——③④④b 的 send 分支 mock 不污染 localdb 族)
    monkeypatch.setattr(_localdb, "resolve_keys", _real_resolve_keys)
    monkeypatch.setattr(_localdb, "locate_db_storage", _real_locate)
    fake_root = tmp_path / "xwechat_files"
    account = fake_root / "wxid_demo_8253"
    (account / "db_storage" / "message").mkdir(parents=True)
    monkeypatch.setattr("wechat_bridge.localdb.WECHAT_FILES_ROOT", fake_root)
    exit_code, payload = run_cli(
        ["localdb", "query", "filehelper", "--since", "7d", "--json"],
        monkeypatch,
        tmp_path,
    )
    assert exit_code == 21
    payloads["err_localdb_key_unavailable"] = payload

    # ⑥ 本地库:数据根缺位 → exit 20
    monkeypatch.setattr(
        "wechat_bridge.localdb.WECHAT_FILES_ROOT", tmp_path / "no-such-root"
    )
    exit_code, payload = run_cli(
        ["localdb", "query", "filehelper", "--since", "7d", "--json"],
        monkeypatch,
        tmp_path,
    )
    assert exit_code == 20
    payloads["err_localdb_db_not_found"] = payload

    # ⑦ 内存密钥扫描(D4 豁免件):配置门缺省关 → exit 21(默认关语义)
    monkeypatch.setattr("wechat_bridge.localdb.WECHAT_FILES_ROOT", fake_root)
    exit_code, payload = run_cli(
        ["localdb", "key-scan", "--json"], monkeypatch, tmp_path
    )
    assert exit_code == 21
    payloads["err_memsearch_default_off"] = payload

    # ⑧ 朋友圈查询缺钥(10-13-wechat-sns-feed;⑤ 同族——sns 命令族走同一
    # 密钥链,缺位 = exit 21 如实。feed/notices 错误载荷同形,单锚定形)
    exit_code, payload = run_cli(
        ["localdb", "sns", "feed", "--since", "3d", "--json"],
        monkeypatch, tmp_path,
    )
    assert exit_code == 21
    payloads["err_localdb_sns_key_unavailable"] = payload

    return payloads


class TestGolden:
    def test_cli_payloads_match_golden(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        payloads = _scrub(_collect_golden_payloads(monkeypatch, tmp_path), tmp_path)
        if os.environ.get(REGEN_ENV) == "1":
            GOLDEN.write_text(
                json.dumps(payloads, ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8",
            )
        golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
        assert payloads == golden, (
            "CLI 应答与 golden 基件漂移:改契约必同步基件"
            f"(显式再生成:{REGEN_ENV}=1 重跑本测试)"
        )


class TestExitCodeContract:
    """§6 十二项错误码:码值、码名、载荷形状全对账。"""

    def test_code_table_is_closed_and_named(self) -> None:
        assert codes_mod.CODE_NAMES == {
            2: "usage",
            10: "wechat_not_running",
            11: "ax_permission_denied",
            16: "screen_recording_denied",
            12: "window_closed",
            13: "ax_tree_empty",
            14: "send_rate_limited",
            15: "send_ax_focus_required",
            17: "send_uncertain_dedup",  # §6 修订 2026-10-14(design §E-4)
            20: "db_not_found",
            21: "key_unavailable",
            22: "decrypt_failed",
            23: "media_unavailable",  # §6 修订 2026-10-14(10-14-wechat-media-sns)
            30: "timeout",
        }
        assert (codes_mod.EXIT_OK, codes_mod.EXIT_GENERIC_FAILURE, codes_mod.EXIT_USAGE) == (0, 1, 2)

    def test_error_payload_shape(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """失败载荷 = {"error": {code, message[, fix_hint][, retry_after_seconds]}}。"""
        tray_mocks(monkeypatch)
        exit_code, payload = run_cli(["sessions", "list"], monkeypatch, tmp_path)
        err = payload["error"]
        assert exit_code == 12
        assert err["code"] == "window_closed"
        assert isinstance(err["message"], str) and err["message"]
        assert isinstance(err["fix_hint"], str) and err["fix_hint"]
        assert "retry_after_seconds" not in err  # 非频控族不携带该键

    def test_rate_limited_payload_has_retry_after(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch)
        SendRateState(tmp_path / "wechat-localdb" / "send_state.json").record_send(now=100.0)
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 101.0)
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch,
            tmp_path,
            stdin_text="x",
        )
        assert exit_code == 14
        assert payload["error"]["retry_after_seconds"] == pytest.approx(9.0)

    def test_timeout_code_exists_for_subprocess_guard(self) -> None:
        """exit 30 的原料:_run_command 超时 kill 兜底(用真 sleep 进程验证)。"""
        import wechat_bridge.system_checks as sc

        with pytest.raises(codes_mod.BridgeError) as excinfo:
            sc._run_command(["sleep", "5"], timeout=0.2)
        assert excinfo.value.exit_code == 30
        assert excinfo.value.name == "timeout"


class TestUsageErrors:
    """exit 2 族:参数/用法错(argparse 用法错同样 JSON 化)。"""

    def test_no_command_is_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        with pytest.raises(SystemExit) as excinfo:
            run_cli([], monkeypatch, tmp_path)
        assert excinfo.value.code == 2

    def test_probe_with_subcommand_is_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        with pytest.raises(SystemExit) as excinfo:
            run_cli(["--probe", "sessions", "list"], monkeypatch, tmp_path)
        assert excinfo.value.code == 2

    def test_bad_since_shape_is_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        exit_code, payload = run_cli(
            ["localdb", "query", "chat", "--since", "7"], monkeypatch, tmp_path
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"

    def test_zero_since_is_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        exit_code, payload = run_cli(
            ["localdb", "query", "chat", "--since", "0d"], monkeypatch, tmp_path
        )
        assert exit_code == 2

    def test_file_path_rejected_only_stdin(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """--file 仅收 '-';路径形态拒(D0:argv 不携带正文)。"""
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "/tmp/body.txt"],
            monkeypatch,
            tmp_path,
            stdin_text="x",
        )
        assert exit_code == 2
        assert "stdin" in payload["error"]["message"]

    def test_empty_body_is_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        tray_mocks(monkeypatch, CheckMocks(window=True))
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch,
            tmp_path,
            stdin_text="",
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"

    def test_negative_limit_is_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        tray_mocks(monkeypatch, CheckMocks(window=True))
        exit_code, payload = run_cli(
            ["sessions", "list", "-n", "0"], monkeypatch, tmp_path
        )
        assert exit_code == 2

    def test_broken_config_file_is_usage(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        config_path = tmp_path / "custom.json"
        config_path.write_text("{bad", encoding="utf-8")
        exit_code, payload = run_cli(
            ["--config", str(config_path), "--probe"], monkeypatch, tmp_path
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"


def _fake_files_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """合成微信文件根(账号目录带 db_storage/):过 localdb 存储门。

    真因注记:exit 20 = db_not_found 而非平台拒——ubuntu 上真实微信数据
    根不存在,注入的 resolve/query/acquire 永远轮不到,须先把门喂过。
    """
    root = tmp_path / "wechat-files"
    (root / "wxid_demo" / "db_storage").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("wechat_bridge.localdb.WECHAT_FILES_ROOT", root)


class TestLocaldbWiring:
    """localdb query 的 E1→E2→E3 装配(monkeypatch 隔离;全链机器对账在
    gated 真机测试)。"""

    def test_success_payload_emitted_and_exit_zero(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        fake_payload = {
            "chat_id": "filehelper",
            "since_days": 7,
            "messages": [],
            "copy": {"dir": "<private>", "built": [], "kept": [], "skipped": [], "total_bytes": 0},
        }
        seen: dict = {}
        _fake_files_root(monkeypatch, tmp_path)

        def fake_query_history(config, storage, keys, chat_id, days, **kwargs):
            seen["chat_id"], seen["days"], seen["domains"] = chat_id, days, config.domains
            return fake_payload

        monkeypatch.setattr(
            "wechat_bridge.localdb.resolve_keys", lambda storage, *, config=None: {"k": "v"}
        )
        monkeypatch.setattr("wechat_bridge.localdb.query_history", fake_query_history)
        exit_code, payload = run_cli(
            ["localdb", "query", "filehelper", "--since", "7d", "--json"],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 0
        assert payload == fake_payload
        assert seen == {"chat_id": "filehelper", "days": 7, "domains": ["message", "session", "contact"]}

    def test_resolve_error_maps_to_its_exit_code(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError

        _fake_files_root(monkeypatch, tmp_path)

        def fake_resolve(storage, *, config=None):
            raise BridgeError(KEY_UNAVAILABLE, "本地库密钥不可得(注入)", fix_hint="D4")

        monkeypatch.setattr("wechat_bridge.localdb.resolve_keys", fake_resolve)
        exit_code, payload = run_cli(
            ["localdb", "query", "filehelper", "--since", "7d", "--json"],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 21
        assert payload["error"]["code"] == "key_unavailable"


class TestKeyScanCommand:
    """localdb key-scan(D4 豁免执行件)CLI 装配:门语义 + 形状契约。"""

    def _write_config(self, tmp_path: Path, enabled: bool) -> None:
        config_dir = tmp_path / "wechat-bridge"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "config.json").write_text(
            json.dumps({"mem_search_enabled": enabled}), encoding="utf-8"
        )

    def test_scan_payload_emitted_and_exit_zero(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        self._write_config(tmp_path, enabled=True)
        fake_payload = {
            "matched": {"count": 1, "total": 1},
            "scan": {"pids": [4242], "regions_scanned": 1, "bytes_scanned": 4096,
                     "regions_skipped_cap": 0, "regions_filtered": 0,
                     "windows": 4065, "verifies": 4065, "interrupted": False},
            "cache": str(tmp_path / "wechat-localdb" / "keys.json"),
        }

        _fake_files_root(monkeypatch, tmp_path)

        def fake_scan(storage, *, config):
            assert config.mem_search_enabled is True
            return fake_payload

        monkeypatch.setattr("wechat_bridge.memsearch.acquire_key_from_memory", fake_scan)
        exit_code, payload = run_cli(["localdb", "key-scan", "--json"], monkeypatch, tmp_path)
        assert exit_code == 0
        assert payload == fake_payload

    def test_scan_gate_error_maps_to_its_exit_code(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        from wechat_bridge.codes import WECHAT_NOT_RUNNING, BridgeError

        self._write_config(tmp_path, enabled=True)

        _fake_files_root(monkeypatch, tmp_path)

        def fake_scan(storage, *, config):
            raise BridgeError(WECHAT_NOT_RUNNING, "微信进程不在场(注入)")

        monkeypatch.setattr("wechat_bridge.memsearch.acquire_key_from_memory", fake_scan)
        exit_code, payload = run_cli(["localdb", "key-scan", "--json"], monkeypatch, tmp_path)
        assert exit_code == 10
        assert payload["error"]["code"] == "wechat_not_running"

    def test_scan_storage_missing_maps_to_db_not_found(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        self._write_config(tmp_path, enabled=True)
        monkeypatch.setattr(
            "wechat_bridge.localdb.WECHAT_FILES_ROOT", tmp_path / "no-such-root"
        )
        exit_code, payload = run_cli(["localdb", "key-scan", "--json"], monkeypatch, tmp_path)
        assert exit_code == 20
        assert payload["error"]["code"] == "db_not_found"


class TestProbeCli:
    def test_probe_exit_zero_even_when_degraded(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """探针本体跑成 = exit 0;三态在载荷(消费方按 state 映射 UI)。"""
        tray_mocks(monkeypatch)
        exit_code, payload = run_cli(["--probe"], monkeypatch, tmp_path)
        assert exit_code == 0
        assert payload["state"] == "degraded"
        assert payload["ok"] is False

    def test_probe_respects_config_override(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        config_path = tmp_path / "custom.json"
        config_path.write_text(json.dumps({"domains": ["message"]}), encoding="utf-8")
        tray_mocks(monkeypatch)
        exit_code, payload = run_cli(
            ["--config", str(config_path), "--probe"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["config"]["domains"] == ["message"]
        assert payload["config"]["source"] == str(config_path)


class TestSendContract:
    """send_text 三源合体契约(task 10-14-wechat-send-text design §E/§G)。"""

    def _stub_sendui(self, monkeypatch: pytest.MonkeyPatch, result=None) -> dict:
        """sendui 桩(新签名全参记录;默认成功全绿形态)。"""
        seen: dict = {}

        def stub(config, target, body, *, dry_run=False, on_armed=None,
                 on_receipt_green=None, receipt_query=None):
            seen["target"] = target
            seen["dry_run"] = dry_run
            seen["on_armed"] = on_armed
            seen["receipt_query"] = receipt_query
            if callable(result):
                return result(seen)
            return {
                "send": {
                    "target": {"username": target.username, "display_name": target.display_name},
                    "channel": "ax",
                    "sent": True,
                    "attempts": 1,
                    "readback": "ax_value",
                    "title_verify": "ax_label",
                    "composer_cleared": True,
                    "localdb_receipt": True,
                    "post_send_verified": True,
                    "post_send_note": None,
                    "fingerprint_note": None,
                    "elapsed_ms": 1,
                }
            }

        monkeypatch.setattr("wechat_bridge.sendui.send_text", stub)
        return seen

    def test_target_not_found_exit_1_named_code(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """查无 → exit 1 send_target_not_found;零 UI 扰动(ensure 未及)。"""
        import wechat_bridge.sendtarget as sendtarget

        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch, target=None)
        exit_code, payload = run_cli(
            ["send_text", "no_such_zzz123", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_target_not_found"
        assert "localdb query" in payload["error"]["fix_hint"]

    def test_target_ambiguous_exit_1_named_code(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.sendtarget as sendtarget

        def raise_ambiguous(config, chat_id, **kwargs):
            raise codes_mod.BridgeError(
                1, f"命中多个联系人(chat_id={chat_id},共 2 个)",
                code="send_target_ambiguous", fix_hint="改用 alias 或 username(wxid)消歧",
            )

        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch)
        monkeypatch.setattr(sendtarget, "resolve_target", raise_ambiguous)
        exit_code, payload = run_cli(
            ["send_text", "同名", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit_code == 1
        assert payload["error"]["code"] == "send_target_ambiguous"

    def test_single_resolution_of_keys(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """单次解析断言:resolve_keys 调用次数 == 1(§J-19)。"""
        import wechat_bridge.localdb as localdb

        tray_mocks(monkeypatch, CheckMocks(window=True))
        calls = {"n": 0}

        def counting_resolve(storage, *, config=None):
            calls["n"] += 1
            return {"k": "v"}

        monkeypatch.setattr(localdb, "locate_db_storage", lambda: Path("/fake"))
        monkeypatch.setattr(localdb, "resolve_keys", counting_resolve)
        monkeypatch.setattr(
            localdb, "query_history",
            lambda config, storage, keys, chat_id, days: {"messages": []},
        )
        import wechat_bridge.sendtarget as sendtarget

        monkeypatch.setattr(
            sendtarget, "resolve_target", lambda config, chat_id, **kw: FAKE_TARGET
        )
        self._stub_sendui(monkeypatch)
        exit_code, _payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit_code == 0
        assert calls["n"] == 1  # resolve_target 与 receipt 闭包共用一次解析

    def test_fingerprint_idempotent_exit_0_including_immediate_repeat(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """指纹幂等 exit 0(sent:false + deduped:true);**立即重复(<10s)
        得幂等而非 exit 14**——指纹门先于间隔门(§J-5)。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch)
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1000.0)
        self._stub_sendui(monkeypatch)
        exit1, payload1 = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit1 == 0 and payload1["send"]["sent"] is True
        # 模拟回执全绿落 sent(桩的 on_armed/on_receipt_green 由 CLI 闭包接)
        state = SendRateState(tmp_path / "wechat-localdb" / "send_state.json")
        from wechat_bridge.sendtarget import fingerprint

        state.mark_fingerprint_pending(fingerprint(FAKE_TARGET, "你好"), now=1000.5)
        state.mark_fingerprint_sent(fingerprint(FAKE_TARGET, "你好"), now=1001.0)
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1003.0)  # +2s <10s
        exit2, payload2 = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit2 == 0
        send2 = payload2["send"]
        assert send2["sent"] is False and send2["deduped"] is True
        assert send2["dedup_status"] == "sent_recently"

    def test_uncertain_dedup_exit_17(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """指纹 pending 命中 → exit 17 send_uncertain_dedup(绝不自动重试)。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch)
        from wechat_bridge.sendtarget import fingerprint

        state = SendRateState(tmp_path / "wechat-localdb" / "send_state.json")
        state.mark_fingerprint_pending(fingerprint(FAKE_TARGET, "你好"), now=1000.0)
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1030.0)
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit_code == 17
        assert payload["error"]["code"] == "send_uncertain_dedup"
        assert "绝不自动重试" in payload["error"]["message"]

    def test_dry_run_zero_rate_control_side_effects(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """--dry-run 契约:零频控副作用——dry-run 后立即可真发不被 14 拦。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch)
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1000.0)
        self._stub_sendui(monkeypatch)
        exit1, payload1 = run_cli(
            ["send_text", "filehelper", "--file", "-", "--dry-run"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit1 == 0
        assert payload1["send"]["chat"] == "filehelper"  # CLI 补原样入参
        assert SendRateState(
            tmp_path / "wechat-localdb" / "send_state.json"
        ).load_last_send_epoch() is None  # 零占位
        # 立即真发(间隔≈0)不被 14 拦 = dry-run 没占时间戳
        exit2, payload2 = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit2 == 0 and payload2["send"]["sent"] is True

    def test_receipt_query_rejects_stale_history_false_green(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """receipt_query 假绿反例:同正文历史消息 ts ≤ since-2 → False;
        新消息 → True(§J-8 防假绿)。"""
        import wechat_bridge.localdb as localdb
        import wechat_bridge.sendtarget as sendtarget

        tray_mocks(monkeypatch, CheckMocks(window=True))
        monkeypatch.setattr(localdb, "locate_db_storage", lambda: Path("/fake"))
        monkeypatch.setattr(
            localdb, "resolve_keys", lambda storage, *, config=None: {"k": "v"}
        )
        monkeypatch.setattr(
            sendtarget, "resolve_target", lambda config, chat_id, **kw: FAKE_TARGET
        )
        queries: list = []

        def fake_history(config, storage, keys, chat_id, days):
            # 同正文历史消息(旧 ts)+ 本次新消息由调用方控制
            messages = [{"ts": 1700000000 - 500, "sender": "me", "type": "text", "text": "你好"}]
            if queries:
                queries.append("late")
                messages.append({"ts": 1700000100, "sender": "me", "type": "text", "text": "你好"})
            else:
                queries.append("early")
            return {"chat_id": chat_id, "since_days": days, "messages": messages}

        monkeypatch.setattr(localdb, "query_history", fake_history)
        seen = self._stub_sendui(monkeypatch)
        monkeypatch.setattr("wechat_bridge.sendui.wall_clock", lambda: 1700000000.0)
        exit_code, _ = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit_code == 0
        receipt = seen["receipt_query"]
        assert callable(receipt)
        # 假绿反例:历史消息 ts=1700000000-500 << since-2 → False
        assert receipt("filehelper", "你好", 1700000005.0) is False
        # 新消息 ts=1700000100 > since-2 → True
        assert receipt("filehelper", "你好", 1700000090.0) is True

    def test_focus_terminal_failure_error_payload_no_rollback(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """stage=focus 终败 → exit 15 error 载荷 + 不 rollback(armed 后;
        §J-20)。on_armed 闭包已被调用 = armed 标志置位。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch)
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1000.0)
        armed_seen = {"n": 0}

        def stub(config, target, body, *, dry_run=False, on_armed=None,
                 on_receipt_green=None, receipt_query=None):
            if on_armed is not None:
                on_armed()  # armed 置位(落 pending)
                armed_seen["n"] += 1
            raise codes_mod.BridgeError(
                15,
                "发送前聚焦断言未过(未回车;指纹已 pending,120s 内同指纹重发将 exit 17):3 次尝试均未通过",
                fix_hint="重试须换正文或等 120s",
            )

        monkeypatch.setattr("wechat_bridge.sendui.send_text", stub)
        exit_code, payload = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit_code == 15
        assert payload["error"]["code"] == "send_ax_focus_required"
        assert "pending" in payload["error"]["message"]
        # 不 rollback:占位时间戳保留(armed 闭包标志生效)
        assert SendRateState(
            tmp_path / "wechat-localdb" / "send_state.json"
        ).load_last_send_epoch() == 1000.0
        assert armed_seen["n"] == 1

    def test_pre_armed_failure_rolls_back(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """on_armed 前失败 → rollback(既有语义保留,§C-4 第 2 行)。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))
        _send_db_mocks(monkeypatch)
        monkeypatch.setattr("wechat_bridge.cli._now", lambda: 1000.0)

        def failing(config, target, body, *, dry_run=False, on_armed=None,
                    on_receipt_green=None, receipt_query=None):
            raise codes_mod.BridgeError(15, "发送未执行:3 次尝试均未通过断言")

        monkeypatch.setattr("wechat_bridge.sendui.send_text", failing)
        exit_code, _ = run_cli(
            ["send_text", "filehelper", "--file", "-"],
            monkeypatch, tmp_path, stdin_text="你好",
        )
        assert exit_code == 15
        assert SendRateState(
            tmp_path / "wechat-localdb" / "send_state.json"
        ).load_last_send_epoch() is None  # 已还原


class TestDoctorCommand:
    """doctor 子命令(design §E-2:--probe 超集 + AX 门态;恒 exit 0)。"""

    def test_doctor_payload_shape_and_exit_zero(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        tray_mocks(monkeypatch)
        import wechat_bridge.system_checks as sc

        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: 122)
        import wechat_bridge.axui as axui

        monkeypatch.setattr(axui, "read_input_value", lambda: "")
        exit_code, payload = run_cli(["doctor"], monkeypatch, tmp_path)
        assert exit_code == 0
        doctor = payload["doctor"]
        assert doctor["probe"]["state"] == "degraded"
        gate = doctor["ax_gate"]
        assert gate["nodes"] == 122 and gate["state"] == "open"
        assert gate["input_field"] == "ok"
        assert gate["note"] is None and gate["fix_hint"] is None
        assert doctor["cgevent_channel"]["post_key"] == "unverified"

    def test_doctor_closed_gate_carries_lldb_fix_hint(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        tray_mocks(monkeypatch)
        import wechat_bridge.system_checks as sc

        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: 3)
        import wechat_bridge.axui as axui

        monkeypatch.setattr(axui, "read_input_value", lambda: None)
        exit_code, payload = run_cli(["doctor"], monkeypatch, tmp_path)
        assert exit_code == 0
        gate = payload["doctor"]["ax_gate"]
        assert gate["state"] == "closed" and gate["input_field"] == "missing"
        assert "LLDB" in gate["fix_hint"] and "深度枚举" in gate["note"]

    def test_doctor_unknown_node_count(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        tray_mocks(monkeypatch)
        import wechat_bridge.system_checks as sc

        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: None)
        exit_code, payload = run_cli(["doctor"], monkeypatch, tmp_path)
        assert exit_code == 0
        assert payload["doctor"]["ax_gate"]["state"] == "unknown"


def _localdb_chain_mocks(monkeypatch: pytest.MonkeyPatch) -> None:
    """C1 族密钥链 mock(locate/resolve 单点注入;查询本体各用例自桩)。"""
    import wechat_bridge.localdb as localdb

    monkeypatch.setattr(localdb, "locate_db_storage", lambda: Path("/fake-db-storage"))
    monkeypatch.setattr(
        localdb, "resolve_keys", lambda storage, *, config=None: {"k": "v"}
    )


PAGE_PAYLOAD: dict = {
    "page": {
        "chat_id": "filehelper",
        "display_name": "文件传输助手",
        "messages": [
            {
                "seq": 7,
                "ts": 1760000000,
                "sender": "wxid_a",
                "sender_id": "wxid_a",
                "type": "text",
                "local_type": 1,
                "text": "你好",
            }
        ],
        "next_cursor": "Y3Vyc29y",
        "has_more": True,
        "filter": {
            "from_ts": 1759913600,
            "to_ts": None,
            "types": ["text"],
            "sender": None,
            "order": "desc",
        },
        "page_size": 500,
    }
}

CONVERSATIONS_PAYLOAD: dict = {
    "conversations": [
        {
            "chat_id": "filehelper",
            "display_name": "文件传输助手",
            "is_group": False,
            "msg_count": 12,
            "first_ts": 1750000000,
            "last_ts": 1760000000,
        }
    ],
    "total": 1,
    "unresolved_tables": 0,
}


class TestPageConversationsExport:
    """C1 三子命令(task 10-14-wechat-chat-export;设计 §8 全 mock)。

    page/conversations 查询本体与 invalid_types/has_more 语义在
    test_localdb_page.py 受测;此处只钉 CLI 接线面:参数解析→编排器透传、
    应答键序、exit 码映射、export 的 NDJSON 流形态。
    """

    def test_page_args_parsed_and_forwarded(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.localdb as localdb

        calls: dict = {}
        _localdb_chain_mocks(monkeypatch)

        def _page_history(config, storage, keys, chat_id, **kwargs):
            calls.update(kwargs, chat_id=chat_id)
            return PAGE_PAYLOAD

        monkeypatch.setattr(localdb, "page_history", _page_history)
        exit_code, payload = run_cli(
            [
                "localdb", "page", "filehelper",
                "--limit", "500", "--asc",
                "--from-ts", "1759913600000",  # 毫秒 → 归一秒
                "--types", "text, file",  # 逗号分隔 + 宽空白
                "--sender", "wxid_a",
                "--cursor", "Y3Vyc29y",
            ],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 0
        assert payload == PAGE_PAYLOAD
        assert calls["chat_id"] == "filehelper"
        assert calls["limit"] == 500
        assert calls["asc"] is True
        assert calls["from_ts"] == 1759913600
        assert calls["types"] == ["text", "file"]
        assert calls["sender"] == "wxid_a"
        assert calls["cursor"] == "Y3Vyc29y"

    def test_page_response_key_order(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.localdb as localdb

        _localdb_chain_mocks(monkeypatch)
        monkeypatch.setattr(
            localdb, "page_history", lambda *a, **k: PAGE_PAYLOAD
        )
        exit_code, payload = run_cli(
            ["localdb", "page", "filehelper"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert list(payload) == ["page"]
        assert list(payload["page"]) == [
            "chat_id", "display_name", "messages", "next_cursor",
            "has_more", "filter", "page_size",
        ]

    def test_page_invalid_cursor_exit_two(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.localdb as localdb

        _localdb_chain_mocks(monkeypatch)

        def _raise(*a, **k):
            raise codes_mod.BridgeError(
                codes_mod.EXIT_USAGE, "游标 scope 不匹配", code="invalid_cursor"
            )

        monkeypatch.setattr(localdb, "page_history", _raise)
        exit_code, payload = run_cli(
            ["localdb", "page", "filehelper", "--cursor", "bogus"],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "invalid_cursor"

    def test_conversations_shape_and_exit_zero(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.localdb as localdb

        _localdb_chain_mocks(monkeypatch)
        monkeypatch.setattr(
            localdb,
            "conversations_census",
            lambda config, storage, keys, *, limit=None: CONVERSATIONS_PAYLOAD,
        )
        exit_code, payload = run_cli(
            ["localdb", "conversations", "--limit", "500"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert list(payload) == ["conversations", "total", "unresolved_tables"]
        assert payload["conversations"][0]["chat_id"] == "filehelper"

    def test_export_usage_reject_bad_format(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        import wechat_bridge.localdb as localdb

        _localdb_chain_mocks(monkeypatch)

        def _raise_usage(config, storage, keys, chat_id, *, fmt, out_dir, **kwargs):
            raise codes_mod.BridgeError(
                codes_mod.EXIT_USAGE,
                f"--format 须为 json|txt|csv|md|html|xlsx 之一,当前为 {fmt!r}",
                code="usage",
            )

        monkeypatch.setattr(localdb, "export_history", _raise_usage)
        exit_code, payload = run_cli(
            [
                "localdb", "export", "filehelper",
                "--format", "xml", "--out", str(tmp_path / "exports"),
            ],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"
        assert "xml" in payload["error"]["message"]

    def test_export_ndjson_stream_final_line(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """export 分支 stdout = NDJSON:progress 行经单行打印器转印,
        终态单行收尾(判例 key-acquire;断 _emit_ndjson_line 双调用形态)。"""
        import wechat_bridge.cli as cli
        import wechat_bridge.localdb as localdb

        _localdb_chain_mocks(monkeypatch)
        progress_lines: list[dict] = []

        def _export_history(config, storage, keys, chat_id, *, fmt, out_dir, **kwargs):
            progress = kwargs.get("progress")
            assert callable(progress)
            progress({"progress": {"phase": "scan", "rows": 3}})
            progress_lines.append({"phase": "scan", "rows": 3})
            return {
                "export": {
                    "chat_id": chat_id,
                    "display_name": None,
                    "format": fmt,
                    "files": [{"name": "a.json", "path": "/tmp/a.json", "rows": 3, "sha256": "0" * 64}],
                    "manifest_path": "/tmp/manifest.json",
                    "total_rows": 3,
                    "time_range": None,
                    "elapsed_ms": 5,
                }
            }

        monkeypatch.setattr(localdb, "export_history", _export_history)
        emitted: list[dict] = []
        monkeypatch.setattr(
            cli, "_emit_ndjson_line", lambda payload: emitted.append(payload)
        )
        # NDJSON 流不经 run_cli 的整段 JSON 解析(多行流),进程内原生跑。
        import io
        import sys as _sys

        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        stdout = io.StringIO()
        real_stdout = _sys.stdout
        monkeypatch.setattr(_sys, "stdout", stdout)
        try:
            exit_code = cli.main(
                [
                    "localdb", "export", "filehelper",
                    "--format", "json", "--out", str(tmp_path / "exports"),
                    "--since", "7d",
                ]
            )
        finally:
            monkeypatch.setattr(_sys, "stdout", real_stdout)
        assert exit_code == 0
        # progress 行(转印)+ 终态行(收尾)各一;终态 = export 回执原样。
        assert emitted[0] == {"progress": {"phase": "scan", "rows": 3}}
        assert emitted[-1]["export"]["total_rows"] == 3
        assert emitted[-1]["export"]["format"] == "json"
