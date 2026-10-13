"""``localdb stats`` CLI 接缝单测(task 10-14-wechat-stats-reports R2)。

被测对象 = stats_query.register_cli / dispatch_cli(cli.py 集成分支的
唯一调用点,接线清单在任务档 integrationSpec——本文件不依赖 cli.py 改动,
先行绿)。exit 码契约:查询层降级恒 0;密钥链 20/21/22 结构化 error 非 0;
用法错(窗口互斥/缺省/形态)exit 2。
"""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

import pytest

from bridge_testkit import COMPONENT_SRC

if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))

from wechat_bridge import stats_query  # noqa: E402
from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError  # noqa: E402

# 与 test_stats_query 同:时区钉 UTC(本文件在其后导入,桥族无更后继者)
import os
import time

os.environ.setdefault("TZ", "UTC")
time.tzset()


def _dispatch(argv: list[str], monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """进程内跑 dispatch_cli:隔离 MYIA_HOME,回 (exit, stdout JSON)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    root = argparse.ArgumentParser()
    sub = root.add_subparsers(dest="localdb_cmd")
    stats_query.register_cli(sub)
    ns = root.parse_args(argv)
    ns.config = None
    stdout = io.StringIO()
    real = sys.stdout
    monkeypatch.setattr(sys, "stdout", stdout)
    try:
        exit_code = stats_query.dispatch_cli(ns, None)
    finally:
        monkeypatch.setattr(sys, "stdout", real)
    payload = json.loads(stdout.getvalue()) if stdout.getvalue().strip() else None
    return exit_code, payload


@pytest.fixture()
def fake_chain(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict:
    """密钥链 mock:存储门 + resolve_keys + stats_history 全注入。"""
    import wechat_bridge.localdb as localdb_mod
    import wechat_bridge.stats_query as sq

    root = tmp_path / "wechat-files"
    (root / "wxid_x" / "db_storage").mkdir(parents=True)
    monkeypatch.setattr(localdb_mod, "WECHAT_FILES_ROOT", root)
    seen: dict = {}
    monkeypatch.setattr(
        localdb_mod, "resolve_keys", lambda storage, *, config=None: {"k": "v"}
    )

    def fake_history(config, storage, keys, mode, **kwargs):
        seen["mode"] = mode
        seen.update({k: v for k, v in kwargs.items() if v is not None and v is not False})
        return {f"stats_{mode}": {"stub": True}}

    monkeypatch.setattr(sq, "stats_history", fake_history)
    return seen


class TestUsageErrors:
    def test_chat_window_missing_is_usage(self, monkeypatch, tmp_path):
        exit_code, payload = _dispatch(["stats", "chat", "wxid_x"], monkeypatch, tmp_path)
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"

    def test_chat_window_both_given_is_usage(self, monkeypatch, tmp_path):
        exit_code, payload = _dispatch(
            ["stats", "chat", "wxid_x", "--since", "7d", "--all"],
            monkeypatch, tmp_path,
        )
        assert exit_code == 2

    def test_bad_since_shape_is_usage(self, monkeypatch, tmp_path):
        exit_code, payload = _dispatch(
            ["stats", "chat", "wxid_x", "--since", "7"], monkeypatch, tmp_path
        )
        assert exit_code == 2
        assert "形态" in payload["error"]["message"]

    def test_annual_neither_is_usage(self, monkeypatch, tmp_path):
        exit_code, _ = _dispatch(["stats", "annual"], monkeypatch, tmp_path)
        assert exit_code == 2

    def test_annual_both_is_usage(self, monkeypatch, tmp_path):
        exit_code, _ = _dispatch(
            ["stats", "annual", "--year", "2025", "--all"], monkeypatch, tmp_path
        )
        assert exit_code == 2

    def test_annual_year_out_of_range(self, monkeypatch, tmp_path):
        exit_code, _ = _dispatch(
            ["stats", "annual", "--year", "10000"], monkeypatch, tmp_path
        )
        assert exit_code == 2

    def test_blank_chat_id_is_usage(self, monkeypatch, tmp_path):
        exit_code, _ = _dispatch(
            ["stats", "chat", "  ", "--since", "7d"], monkeypatch, tmp_path
        )
        assert exit_code == 2

    def test_stats_subcommand_required(self, monkeypatch, tmp_path):
        with pytest.raises(SystemExit) as excinfo:
            _dispatch(["stats"], monkeypatch, tmp_path)
        assert excinfo.value.code == 2


class TestDispatch:
    def test_chats_emits_payload_exit_zero(self, monkeypatch, tmp_path, fake_chain):
        exit_code, payload = _dispatch(["stats", "chats"], monkeypatch, tmp_path)
        assert exit_code == 0
        assert payload == {"stats_chats": {"stub": True}}
        assert fake_chain["mode"] == "chats"

    def test_chat_forwards_since_and_chat_id(self, monkeypatch, tmp_path, fake_chain):
        exit_code, payload = _dispatch(
            ["stats", "chat", "wxid_x", "--since", "30d"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert fake_chain["mode"] == "chat"
        assert fake_chain["chat_id"] == "wxid_x"
        assert fake_chain["since_days"] == 30

    def test_dual_all_time_flag(self, monkeypatch, tmp_path, fake_chain):
        exit_code, payload = _dispatch(
            ["stats", "dual", "wxid_x", "--all"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert fake_chain["mode"] == "dual"
        assert fake_chain.get("all_time") is True

    def test_annual_year_forwarded(self, monkeypatch, tmp_path, fake_chain):
        exit_code, _ = _dispatch(
            ["stats", "annual", "--year", "2025"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert fake_chain["mode"] == "annual"
        assert fake_chain["year"] == 2025

    def test_refresh_forwarded(self, monkeypatch, tmp_path, fake_chain):
        exit_code, _ = _dispatch(
            ["stats", "chats", "--refresh"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert fake_chain.get("refresh") is True

    def test_key_unavailable_maps_to_21(
        self, monkeypatch, tmp_path, fake_chain
    ):
        import wechat_bridge.stats_query as sq

        def raise_key(config, storage, keys, mode, **kwargs):
            raise BridgeError(
                KEY_UNAVAILABLE, "本地库密钥不可得(注入)", fix_hint="D4"
            )

        monkeypatch.setattr(sq, "stats_history", raise_key)
        exit_code, payload = _dispatch(
            ["stats", "chat", "wxid_x", "--since", "7d"], monkeypatch, tmp_path
        )
        assert exit_code == 21
        assert payload["error"]["code"] == "key_unavailable"

    def test_storage_missing_maps_to_20(self, monkeypatch, tmp_path):
        import wechat_bridge.localdb as localdb_mod

        monkeypatch.setattr(
            localdb_mod, "WECHAT_FILES_ROOT", tmp_path / "no-such-root"
        )
        exit_code, payload = _dispatch(
            ["stats", "chats"], monkeypatch, tmp_path
        )
        assert exit_code == 20
        assert payload["error"]["code"] == "db_not_found"


class TestRegisterCli:
    def test_returns_nodes_for_json_reregistration(self, monkeypatch, tmp_path):
        root = argparse.ArgumentParser()
        sub = root.add_subparsers(dest="localdb_cmd")
        nodes = stats_query.register_cli(sub)
        assert len(nodes) == 5  # stats + 四子命令(chats/chat/annual/dual)
        # --json 兼容旗标可逐层重注册(集成员接线位)
        for node in nodes:
            node.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
        ns = root.parse_args(
            ["stats", "chat", "wxid_x", "--since", "7d", "--json"]
        )
        assert ns.stats_cmd == "chat"
        assert ns.chat_id == "wxid_x"
