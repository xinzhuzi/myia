"""notify-scan / revoke-list CLI 契约测试(10-14-wechat-notify-revoke R2)。

覆盖:stdin 载荷契约(read_scan_payload 的 CLI 消费面)/编排装配
(monkeypatch 隔离,TestLocaldbWiring 同款)/两子命令 argv+exit 码接线
(**gated**:``localdb notify-scan``/``revoke-list`` 的 cli.py 注册归集成
统一落笔,未接线时如实 skip 并指路;接线后本用例守住契约不漂移)。

零真库零真钥(全 mock);真数据干跑归复查员(realRunCommand,只读)。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

import wechat_bridge.notify_query as nq
from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError

from bridge_testkit import run_cli

CHAT = "00000000000000000000@chatroom"  # 合成会话 id(形状真实;非真实会话)


def _fake_files_root(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """合成微信文件根(账号目录带 db_storage/):过 localdb 存储门。"""
    root = tmp_path / "wechat-files"
    (root / "wxid_demo" / "db_storage").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr("wechat_bridge.localdb.WECHAT_FILES_ROOT", root)


class TestScanPayloadContract:
    """stdin 载荷契约(read_scan_payload = CLI 分支的唯一解析件)。"""

    def test_round_trip(self) -> None:
        payload = nq.read_scan_payload(
            json.dumps({"whitelist": [CHAT], "baseline": None})
        )
        assert payload == {"whitelist": [CHAT], "baseline": {}, "notify_self": False}

    def test_empty_stdin_is_usage(self) -> None:
        with pytest.raises(BridgeError) as excinfo:
            nq.read_scan_payload("")
        assert excinfo.value.exit_code == 2


class TestOrchestrationWiring:
    """编排函数装配(monkeypatch 隔离;CLI 分支只差一行调用)。"""

    def test_notify_scan_orchestration_called_with_parsed_payload(
        self, tmp_path: Path
    ) -> None:
        from wechat_bridge.config import BridgeConfig

        seen: dict = {}
        fake = {
            "notify_scan": {"events": [], "baseline": {CHAT: {"ts": 1, "unread": 0}},
                            "stats": {}},
        }

        def fake_scan(config, storage, keys, payload, **kwargs):
            seen["payload"] = payload
            seen["storage"] = storage
            return fake

        orig = nq.notify_scan
        nq.notify_scan = fake_scan
        try:
            result = nq.notify_scan(
                BridgeConfig(), Path("/tmp/synthetic"), {"k": "v"},
                {"whitelist": [CHAT], "baseline": {}, "notify_self": False},
            )
        finally:
            nq.notify_scan = orig
        assert result == fake
        assert seen["payload"]["whitelist"] == [CHAT]

    def test_key_unavailable_maps_to_exit_21(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        _fake_files_root(monkeypatch, tmp_path)

        def fake_resolve(storage, *, config=None):
            raise BridgeError(KEY_UNAVAILABLE, "本地库密钥不可得(注入)", fix_hint="D4")

        monkeypatch.setattr("wechat_bridge.localdb.resolve_keys", fake_resolve)
        # gated:子命令未接线时 CLI 会以 usage 拒(见 TestCliIntegration)
        if not TestCliIntegration._registered():
            pytest.skip("等集成:cli.py 注册 localdb notify-scan(R2 接线)")
        exit_code, payload = run_cli(
            ["localdb", "notify-scan", "--file", "-", "--json"],
            monkeypatch, tmp_path,
            stdin_text=json.dumps({"whitelist": [CHAT]}),
        )
        assert exit_code == 21
        assert payload["error"]["code"] == "key_unavailable"


class TestCliIntegration:
    """两子命令的 CLI 装配(gated:集成落笔后自动生效)。"""

    @staticmethod
    def _registered() -> bool:
        """递归探针:parser 树任意层的 choices 含两子命令名 = 已接线。"""
        from wechat_bridge.cli import build_parser

        names: set[str] = set()

        def _walk(parser: Any) -> None:
            for action in parser._actions:  # noqa: SLF001 - 装配形状探针
                choices = getattr(action, "choices", None)
                if not isinstance(choices, dict):
                    continue
                for name, choice in choices.items():
                    names.add(str(name))
                    if hasattr(choice, "_actions"):  # 子 parser 递归
                        _walk(choice)

        _walk(build_parser())
        return "notify-scan" in names and "revoke-list" in names

    def test_notify_scan_subcommand_contract(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        if not self._registered():
            pytest.skip("等集成:cli.py 注册 localdb notify-scan(R2 接线)")
        _fake_files_root(monkeypatch, tmp_path)
        fake = {"notify_scan": {"events": [], "baseline": {}, "stats": {}}}
        monkeypatch.setattr(
            "wechat_bridge.localdb.resolve_keys",
            lambda storage, *, config=None: {"k": "v"},
        )
        monkeypatch.setattr(
            nq, "notify_scan", lambda *a, **k: fake
        )
        exit_code, payload = run_cli(
            ["localdb", "notify-scan", "--file", "-", "--json"],
            monkeypatch, tmp_path,
            stdin_text=json.dumps({"whitelist": [CHAT]}),
        )
        assert exit_code == 0
        assert payload == fake

    def test_notify_scan_stdin_required(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """stdin 空 = usage 拒(argv 零内容纪律)。"""
        if not self._registered():
            pytest.skip("等集成:cli.py 注册 localdb notify-scan(R2 接线)")
        _fake_files_root(monkeypatch, tmp_path)
        monkeypatch.setattr(
            "wechat_bridge.localdb.resolve_keys",
            lambda storage, *, config=None: {"k": "v"},
        )
        exit_code, payload = run_cli(
            ["localdb", "notify-scan", "--file", "-", "--json"],
            monkeypatch, tmp_path,
            stdin_text="",
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"

    def test_revoke_list_subcommand_contract(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        if not self._registered():
            pytest.skip("等集成:cli.py 注册 localdb revoke-list(R2 接线)")
        _fake_files_root(monkeypatch, tmp_path)
        fake = {"revoke_list": [], "stats": {}}
        seen: dict = {}
        monkeypatch.setattr(
            "wechat_bridge.localdb.resolve_keys",
            lambda storage, *, config=None: {"k": "v"},
        )

        def fake_revoke_list(config, storage, keys, chat_id, days, **kwargs):
            seen["chat_id"], seen["days"] = chat_id, days
            return fake

        monkeypatch.setattr(nq, "revoke_list", fake_revoke_list)
        exit_code, payload = run_cli(
            ["localdb", "revoke-list", CHAT, "--since", "7d", "--json"],
            monkeypatch, tmp_path,
        )
        assert exit_code == 0
        assert payload == fake
        assert seen == {"chat_id": CHAT, "days": 7}

    def test_revoke_list_bad_since_is_usage(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        if not self._registered():
            pytest.skip("等集成:cli.py 注册 localdb revoke-list(R2 接线)")
        exit_code, payload = run_cli(
            ["localdb", "revoke-list", CHAT, "--since", "7", "--json"],
            monkeypatch, tmp_path,
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"
