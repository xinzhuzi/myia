"""Tests for 10-14-wechat-stats-reports R5 — 微信统计 sidecar 协议面。

覆盖:stats 中继的 argv 构造/参数校验/桥错误透传;stats_report 的配置
状态机(ai_disabled/dependency_missing/成功)、隐私缺省(载荷剥离
messages)、LLM 全 fake 零网络。桥子进程与 LLM 客户端全注入。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from myssia.wechat import sidecar as wls  # noqa: E402
from myssia.wechat import stats_sidecar as wss  # noqa: E402
from myssia.enrich.errors import EnrichConfigError  # noqa: E402
from myssia.wechat.sidecar import WechatLocalSidecarError  # noqa: E402

STATS_PAYLOAD = {
    "stats_chat": {
        "chat_id": "wxid_x",
        "total": 100,
        "sent": 40,
        "received": 58,
        "human_total": 98,
        "type_counts": {"text": 80},
        "hourly": [0] * 24,
        "top_phrases": [{"phrase": "好的", "count": 9}],
    }
}


@pytest.fixture()
def fake_bridge(tmp_path, monkeypatch):
    """fake bridge:可执行占位(过 bin 存在性门)+ 换 _BASE + 捕获 argv。"""
    calls: list[dict[str, Any]] = []
    responses: dict[str, tuple[int, str]] = {}

    bridge_bin = tmp_path / "fake-wechat-bridge"
    bridge_bin.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    bridge_bin.chmod(0o755)

    def fake_run(argv, input_text, timeout):
        calls.append({"argv": list(argv), "timeout": timeout})
        key = " ".join(argv[1:4]) if len(argv) >= 4 else " ".join(argv[1:])
        exit_code, stdout = responses.get(key, (0, json.dumps(STATS_PAYLOAD)))
        return exit_code, stdout, ""

    monkeypatch.setattr(wls, "_BASE", str(bridge_bin))
    monkeypatch.setattr(wls, "run_bridge_command_sync", fake_run)
    return calls, responses


# =====================================================================
# stats 中继
# =====================================================================


class TestStatsRelay:
    def test_chats_argv(self, fake_bridge):
        calls, _ = fake_bridge
        result = wss.handle_wechat_stats("stats", {"mode": "chats"})
        assert result == STATS_PAYLOAD
        assert calls[0]["argv"][1:] == ["localdb", "stats", "chats", "--json"]

    def test_chat_since_argv(self, fake_bridge):
        calls, _ = fake_bridge
        wss.handle_wechat_stats(
            "stats", {"mode": "chat", "chat_id": "wxid_x", "since_days": 30}
        )
        assert calls[0]["argv"][1:] == [
            "localdb", "stats", "chat", "wxid_x", "--since", "30d", "--json",
        ]

    def test_dual_all_and_refresh_argv(self, fake_bridge):
        calls, _ = fake_bridge
        wss.handle_wechat_stats(
            "stats",
            {"mode": "dual", "chat_id": "wxid_x", "all": True, "refresh": True},
        )
        assert calls[0]["argv"][1:] == [
            "localdb", "stats", "dual", "wxid_x", "--all", "--refresh", "--json",
        ]

    def test_annual_year_argv(self, fake_bridge):
        calls, _ = fake_bridge
        wss.handle_wechat_stats("stats", {"mode": "annual", "year": 2025})
        assert calls[0]["argv"][1:] == [
            "localdb", "stats", "annual", "--year", "2025", "--json",
        ]

    def test_query_timeout_bound(self, fake_bridge):
        calls, _ = fake_bridge
        wss.handle_wechat_stats("stats", {"mode": "annual", "all": True})
        assert calls[0]["timeout"] == wls._QUERY_TIMEOUT_SECONDS

    @pytest.mark.parametrize(
        "params",
        [
            {"mode": "nope"},
            {"mode": "chat"},  # 缺 chat_id
            {"mode": "chat", "chat_id": "x"},  # 缺窗口
            {"mode": "chat", "chat_id": "x", "since_days": 7, "all": True},
            {"mode": "annual"},  # 缺 year/all
            {"mode": "annual", "year": 2025, "all": True},
            {"mode": "chat", "chat_id": "x", "since_days": True},  # bool 非整
        ],
    )
    def test_invalid_params_structured(self, fake_bridge, params):
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            wss.handle_wechat_stats("stats", params)
        assert excinfo.value.code == "invalid_params"

    def test_unknown_action_closed_vocabulary(self, fake_bridge):
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            wss.handle_wechat_stats("bogus", {})
        assert excinfo.value.code == "invalid_params"
        assert "stats" in excinfo.value.message

    def test_bridge_named_error_passthrough(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb stats chats"] = (
            21,
            json.dumps(
                {
                    "error": {
                        "code": "key_unavailable",
                        "message": "本地库密钥不可得",
                        "fix_hint": "D4",
                    }
                }
            ),
        )
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            wss.handle_wechat_stats("stats", {"mode": "chats"})
        assert excinfo.value.code == "key_unavailable"
        assert excinfo.value.data == {"fix_hint": "D4"}


# =====================================================================
# stats_report(AI)
# =====================================================================


class _FakeClient:
    """零网络 fake:记录 prompt 断言面,回固定 CompletionResult。"""

    def __init__(self, *, text="# 总览\n好的。", tokens=123):
        self._text = text
        self._tokens = tokens
        self.calls: list[dict[str, str]] = []
        self.raised: Exception | None = None

    async def complete(self, *, model: str, system: str, user: str):
        self.calls.append({"model": model, "system": system, "user": user})
        if self.raised is not None:
            raise self.raised
        from myssia.enrich.client import CompletionResult

        return CompletionResult(text=self._text, total_tokens=self._tokens)

    async def aclose(self):
        return None


@pytest.fixture()
def enabled_config(tmp_path, monkeypatch):
    """数据根内启用态配置(端点引用齐备;凭据解析注入成事)。"""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "wechat-stats.yaml").write_text(
        "stats_report:\n"
        "  enabled: true\n"
        "  model: glm-5.3-flash\n"
        "  base_url: env:MYIA_TEST_BASE_URL\n"
        "  api_key: env:MYIA_TEST_KEY\n"
        "  timeout_seconds: 5\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("MYIA_HOME", raising=False)
    return tmp_path


@pytest.fixture()
def fake_endpoint(monkeypatch):
    monkeypatch.setenv("MYIA_TEST_BASE_URL", "https://llm.example/v1")
    monkeypatch.setenv("MYIA_TEST_KEY", "test-key")


@pytest.fixture()
def fake_llm(monkeypatch):
    holder: dict[str, _FakeClient] = {}

    def build(base_url, api_key, **kwargs):
        client = holder.get("client") or _FakeClient()
        holder["client"] = client
        return client

    monkeypatch.setattr(wss, "OpenAICompatClient", build)
    return holder


class TestStatsReport:
    def _run(self, data_root, **overrides):
        params = {
            "mode": "chat",
            "stats_payload": json.loads(json.dumps(STATS_PAYLOAD)),
        }
        params.update(overrides)
        return wss.handle_wechat_stats(
            "stats_report", params, data_root=data_root
        )

    def test_disabled_by_default(self, tmp_path, monkeypatch):
        monkeypatch.delenv("MYIA_HOME", raising=False)
        # 数据根无配置 → 全缺省(enabled false)
        empty = tmp_path / "home"
        empty.mkdir()
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            self._run(empty)
        assert excinfo.value.code == "ai_disabled"
        assert excinfo.value.data and "fix_hint" in excinfo.value.data

    def test_enabled_but_endpoint_missing(
        self, enabled_config, fake_endpoint, monkeypatch
    ):
        # 只留 base_url(缺 api_key)→ ai_disabled 如实报缺哪件
        cfg = enabled_config / "config" / "wechat-stats.yaml"
        cfg.write_text(
            "stats_report:\n  enabled: true\n  base_url: env:MYIA_TEST_BASE_URL\n",
            encoding="utf-8",
        )
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            self._run(enabled_config)
        assert excinfo.value.code == "ai_disabled"
        assert "api_key" in excinfo.value.message

    def test_success_returns_report_contract(
        self, enabled_config, fake_endpoint, fake_llm
    ):
        result = self._run(enabled_config, tone="轻松")
        assert set(result) == {"report_markdown", "model", "total_tokens"}
        assert result["model"] == "glm-5.3-flash"
        assert result["total_tokens"] == 123
        assert result["report_markdown"].startswith("# 总览")

    def test_prompt_carries_aggregates_but_no_messages(
        self, enabled_config, fake_endpoint, fake_llm
    ):
        payload = json.loads(json.dumps(STATS_PAYLOAD))
        payload["stats_chat"]["messages"] = [
            {"ts": 1, "text": "不该被喂给模型的原文"}
        ]
        wss.handle_wechat_stats(
            "stats_report",
            {"mode": "chat", "stats_payload": payload},
            data_root=enabled_config,
        )
        user = fake_llm["client"].calls[0]["user"]
        assert '"total": 100' in user  # 聚合数字在场
        assert "不该被喂给模型的原文" not in user  # 逐条原文零泄漏(隐私缺省)
        assert "messages" not in user
        system = fake_llm["client"].calls[0]["system"]
        assert "总览" in system and "结语" in system  # 四章钉死

    def test_tone_forwarded_to_user_prompt(
        self, enabled_config, fake_endpoint, fake_llm
    ):
        self._run(enabled_config, tone="幽默")
        assert "幽默" in fake_llm["client"].calls[0]["user"]

    def test_bad_tone_rejected(self, enabled_config):
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            self._run(enabled_config, tone="x" * 60)
        assert excinfo.value.code == "invalid_params"

    def test_dependency_missing_structured(
        self, enabled_config, fake_endpoint, fake_llm, monkeypatch
    ):
        client = _FakeClient()
        client.raised = EnrichConfigError(
            "dependency_missing",
            "enrich 依赖 openai 未安装:请先执行 pip install 'myssia[llm]'",
            details={"package": "openai"},
        )
        fake_llm["client"] = client
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            self._run(enabled_config)
        assert excinfo.value.code == "dependency_missing"
        assert excinfo.value.data and "install" in str(excinfo.value.data.get("fix_hint"))

    def test_unresolvable_env_ref_is_ai_disabled(
        self, enabled_config, monkeypatch
    ):
        # 引用在但 env 未设 → credential_unresolved → ai_disabled(结构化)
        monkeypatch.delenv("MYIA_TEST_BASE_URL", raising=False)
        monkeypatch.delenv("MYIA_TEST_KEY", raising=False)
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            self._run(enabled_config)
        assert excinfo.value.code == "ai_disabled"

    def test_bad_params(self, enabled_config):
        for params in (
            {"mode": "chat"},  # 缺 stats_payload
            {"mode": "bogus", "stats_payload": {}},
            {"stats_payload": {}},  # 缺 mode
        ):
            with pytest.raises(WechatLocalSidecarError) as excinfo:
                wss.handle_wechat_stats("stats_report", params, data_root=enabled_config)
            assert excinfo.value.code == "invalid_params"


class TestConfigLoading:
    def test_repo_default_config_disabled(self):
        # 仓库无随包种子(config/ 只收品类文件,样例 = *.yaml.example):
        # dev 回落全缺省 enabled:false(与种子内容等价,sidecar 零依赖仓库件)。
        cfg = wss.load_stats_report_config()
        assert cfg.enabled is False
        assert cfg.model == "glm-5.3-flash"

    def test_missing_file_all_defaults(self, tmp_path):
        cfg = wss.load_stats_report_config(tmp_path / "nope")
        assert cfg.enabled is False and cfg.base_url_ref is None

    def test_corrupt_file_falls_back_to_defaults(self, tmp_path):
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "wechat-stats.yaml").write_text("{bad yaml: [", encoding="utf-8")
        cfg = wss.load_stats_report_config(tmp_path)
        assert cfg.enabled is False

    def test_data_root_env_resolution(self, tmp_path, monkeypatch):
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "wechat-stats.yaml").write_text(
            "stats_report:\n  enabled: true\n", encoding="utf-8"
        )
        monkeypatch.delenv("MYIA_HOME", raising=False)
        assert wss.config_path(tmp_path) == config_dir / "wechat-stats.yaml"
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        cfg = wss.load_stats_report_config()
        assert cfg.enabled is True

    def test_plaintext_endpoint_refused_by_enrich_settings(
        self, tmp_path, monkeypatch
    ):
        # 明文端点:EnrichSettings 构造即拒(构造门在调用侧,这里验证
        # 装载层不静默吞——配置原样带出,拒绝发生在 resolve 链)
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "wechat-stats.yaml").write_text(
            "stats_report:\n  enabled: true\n"
            "  base_url: https://plain.example\n  api_key: sk-plain\n",
            encoding="utf-8",
        )
        monkeypatch.delenv("MYIA_HOME", raising=False)
        cfg = wss.load_stats_report_config(tmp_path)
        assert cfg.base_url_ref == "https://plain.example"
        with pytest.raises(WechatLocalSidecarError) as excinfo:
            wss.handle_wechat_stats(
                "stats_report",
                {"mode": "chat", "stats_payload": {}},
                data_root=tmp_path,
            )
        assert excinfo.value.code == "ai_disabled"  # 拒绝且结构化
