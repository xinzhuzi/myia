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

from bridge_testkit import CheckMocks, run_cli, tray_mocks

FIXTURES = Path(__file__).resolve().parent / "fixtures"
GOLDEN = FIXTURES / "golden_cli_payloads.json"
REGEN_ENV = "MYIA_WECHAT_BRIDGE_REGEN_GOLDEN"


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
    green = tray_mocks(monkeypatch, CheckMocks(window=True))
    assert green.window is True
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

    # ④ 前置全绿 + 频控放行(独立数据根,无发送记录)→ 实现层未落地(骨架
    # 过渡码,exit 1)
    exit_code, payload = run_cli(
        ["send_text", "filehelper", "--file", "-"],
        monkeypatch,
        tmp_path / "clean-home",
        stdin_text="你好",
    )
    assert exit_code == 1
    payloads["err_not_implemented_send"] = payload

    # ⑤ 本地库:定位成功 + 密钥不可得(D4)→ exit 21
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
            20: "db_not_found",
            21: "key_unavailable",
            22: "decrypt_failed",
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
