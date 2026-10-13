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
        # D4 豁免开关缺省关(design §4:默认关,主人显式开启才生效)。
        assert config.mem_search_enabled is False

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

    def test_copy_ttl_zero_means_never_expire(self, tmp_path: Path) -> None:
        """copy_ttl_hours=0 合法且语义=永不过期(2026-10-13 审计修复:
        用户直觉「0=永不过期」,旧实现拒载致全桥不可用);负数仍拒。"""
        path = tmp_path / "config.json"
        path.write_text(json.dumps({"copy_ttl_hours": 0}), encoding="utf-8")
        config = load_config(path)
        assert config.copy_ttl_hours == 0
        # 容量键不受连带:仍须正整数(0 容量无合法语义)。
        path.write_text(json.dumps({"copy_capacity_mb": 0}), encoding="utf-8")
        with pytest.raises(BridgeError) as excinfo:
            load_config(path)
        assert excinfo.value.exit_code == EXIT_USAGE
        assert "copy_capacity_mb 须为正整数" in excinfo.value.message

    def test_mem_search_enabled_accepts_bool_only(self, tmp_path: Path) -> None:
        """D4 豁免开关:布尔收下(true/false),其余形态 usage 拒。"""
        path = tmp_path / "config.json"
        path.write_text(json.dumps({"mem_search_enabled": True}), encoding="utf-8")
        assert load_config(path).mem_search_enabled is True
        path.write_text(json.dumps({"mem_search_enabled": False}), encoding="utf-8")
        assert load_config(path).mem_search_enabled is False

    @pytest.mark.parametrize(
        "raw",
        [
            '{"mem_search_enabled": 1}',
            '{"mem_search_enabled": 0}',
            '{"mem_search_enabled": "true"}',
        ],
    )
    def test_mem_search_non_bool_rejected(self, tmp_path: Path, raw: str) -> None:
        path = tmp_path / "config.json"
        path.write_text(raw, encoding="utf-8")
        with pytest.raises(BridgeError) as excinfo:
            load_config(path)
        assert excinfo.value.exit_code == EXIT_USAGE
        assert "布尔" in excinfo.value.message

    def test_mem_search_null_is_absent(self, tmp_path: Path) -> None:
        """JSON null 与未声明同语义(本配置族 get-None 口径)→ 缺省关。"""
        path = tmp_path / "config.json"
        path.write_text('{"mem_search_enabled": null}', encoding="utf-8")
        assert load_config(path).mem_search_enabled is False

    def test_to_payload_exposes_switch_shape(self, tmp_path: Path) -> None:
        """诊断面暴露开关形状(纯布尔,非敏感)。"""
        path = tmp_path / "config.json"
        path.write_text(json.dumps({"mem_search_enabled": True}), encoding="utf-8")
        assert load_config(path).to_payload()["mem_search_enabled"] is True
        assert BridgeConfig().to_payload()["mem_search_enabled"] is False


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
            # TTL 负数仍拒(0 = 永不过期已合法,见 TestLoadCustom 正例);
            # 布尔/非整数同拒(锚「非负整数」新话术)。
            ('{"copy_ttl_hours": -1}', "非负整数"),
            ('{"copy_ttl_hours": true}', "非负整数"),
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
