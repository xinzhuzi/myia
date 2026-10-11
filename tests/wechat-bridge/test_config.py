"""§7 配置面单测:缺文件可用(设计原文)、键封闭、未知键/频控键拒载。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from wechat_bridge.codes import EXIT_USAGE, BridgeError
from wechat_bridge.config import (
    DEFAULT_DOMAINS,
    BridgeConfig,
    default_config_path,
    load_config,
    myssia_home,
)


class TestDataRoot:
    def test_myia_home_env_wins(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        """MYIA_HOME env 优先(壳 spawn 注入;main.rs data_root 同序)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        assert myssia_home() == tmp_path

    def test_myia_home_blank_falls_through(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """空串 env 视作未设(与 entry.py 的 strip+or 同口径)。"""
        monkeypatch.setenv("MYIA_HOME", "   ")
        assert myssia_home() != Path("")


class TestMissingFileUsable:
    def test_missing_file_yields_defaults(self, tmp_path: Path) -> None:
        """缺文件可用:全缺省 + source=None 如实。"""
        config = load_config(tmp_path / "nope" / "config.json")
        assert config == BridgeConfig()
        assert config.source is None
        assert config.domains == DEFAULT_DOMAINS
        assert (config.sessions, config.messages, config.history_days) == (20, 50, 30)
        assert (config.copy_ttl_hours, config.copy_capacity_mb) == (24, 512)

    def test_default_path_under_data_root(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """缺省路径 = <数据根>/wechat-bridge/config.json(design §7 原文)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        assert default_config_path() == tmp_path / "wechat-bridge" / "config.json"


class TestLoadCustom:
    def test_full_custom_file(self, tmp_path: Path) -> None:
        path = tmp_path / "config.json"
        path.write_text(
            json.dumps(
                {
                    "domains": ["message"],
                    "limits": {"sessions": 5, "messages": 7, "history_days": 3},
                    "copy_ttl_hours": 6,
                    "copy_capacity_mb": 64,
                }
            ),
            encoding="utf-8",
        )
        config = load_config(path)
        assert config.domains == ["message"]
        assert config.sessions == 5 and config.messages == 7 and config.history_days == 3
        assert config.copy_ttl_hours == 6 and config.copy_capacity_mb == 64
        assert config.source == str(path)

    def test_partial_custom_file_merges_defaults(self, tmp_path: Path) -> None:
        path = tmp_path / "config.json"
        path.write_text(json.dumps({"limits": {"messages": 9}}), encoding="utf-8")
        config = load_config(path)
        assert config.messages == 9
        assert config.sessions == 20  # 未声明键回落缺省


class TestFailFast:
    @pytest.mark.parametrize(
        ("raw", "fragment"),
        [
            ('{"domains": ["message"], "bogus": 1}', "未知键"),
            ('{"limits": {"nope": 1}}', "limits 含未知键"),
            ("[]", "键值映射"),
            ('{"domains": []}', "非空字符串列表"),
            ('{"domains": "message"}', "非空字符串列表"),
            ('{"limits": {"messages": 0}}', "正整数"),
            ('{"limits": {"messages": -3}}', "正整数"),
            ('{"limits": {"messages": true}}', "正整数"),
            ('{"copy_ttl_hours": 0}', "正整数"),
            ('{"copy_capacity_mb": "512"}', "正整数"),
            # G6:频控类键写进来 = 契约漂移,拒载(设计 §7「无频控键」)。
            ('{"send_interval_seconds": 5}', "未知键"),
            ('{"rate_limit": {"interval": 5}}', "未知键"),
        ],
    )
    def test_invalid_shapes_rejected_as_usage(
        self, tmp_path: Path, raw: str, fragment: str
    ) -> None:
        path = tmp_path / "config.json"
        path.write_text(raw, encoding="utf-8")
        with pytest.raises(BridgeError) as excinfo:
            load_config(path)
        assert excinfo.value.exit_code == EXIT_USAGE
        assert fragment in excinfo.value.message

    def test_broken_json_rejected_as_usage(self, tmp_path: Path) -> None:
        path = tmp_path / "config.json"
        path.write_text("{not json", encoding="utf-8")
        with pytest.raises(BridgeError) as excinfo:
            load_config(path)
        assert excinfo.value.exit_code == EXIT_USAGE
        assert excinfo.value.fix_hint is not None
