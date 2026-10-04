"""Tests for gates — 门槛件知情启用配置(task 10-05-plugin-market-batch 批二 R5/D4-D7).

覆盖 AC6 地基面(执行卡第 10 步;先例 tests/test_secrets.py —— 根模块映根文件):

- :class:`GatesConfig` 构造即校验:未知字段拒 / keychain 引用形态(明文与
  ``env:`` 拒)/ 逐件键名词表 / 版本号 / 非布尔拒;
- :func:`load_gates_config`:缺失与空文件 = 全关(合法未配置态)、坏文件 =
  :class:`LoadError` 结构化;:func:`load_gates_fail_closed` = 全关态继续 +
  结构化错误带回(fail-closed,不是静默吞掉);
- :func:`gate_open` 唯一查询口:总开关 ∧ 逐件开关、未知键 = 关、未知 kind =
  编程错误当场抛;每开关(config 层 + CLI 层)往返;
- ``myssia gates show/set`` CLI:show-set 往返、非法 target 结构化拒、坏文件
  零写入;saas/platforms 逐件 on 缺钥匙串键 = 结构化拒(``gate_key_missing``,
  零写入;后端不可用 = ``gate_key_unverifiable``);
- manifest ``gate`` 字段(D5 独立字段):四词表值收 / 非法拒 / 缺省 None /
  与 tier 正交组合;plugin list 门槛件分组与 ``enabled`` 徽标(gates.yaml
  状态派生;坏文件全关 + 顶层 error);
- doctor:未启用门槛件 = **info** 级 finding(非 warning,用户没开是正常态)、
  启用后不再产 finding、坏 gates.yaml = warning;
- desktop/entry.py ``_gates_yaml_path``:与 vision.yaml 同位(home 模式落数据根,
  dev 回退 cwd 相对);sidecar ``gates.get``/``gates.save``(design §6.7 契约):
  get 坏文件 fail-closed=全关+error 带回(设置屏是修复入口不炸)、save 同门
  校验失败 ``gates_config_invalid`` 零写入、往返原样回显 keychain 引用。

测试纪律(与全仓一致):零真实钥匙串(InMemoryKeychainBackend 注入)、
零真实网络(本面无网络路径)、零共享状态(每测独立 tmp_path)。
"""

from __future__ import annotations

import importlib.util
import json
from dataclasses import replace as dataclass_replace
from pathlib import Path
from typing import Any

import pytest
import yaml

from myssia import secrets as secrets_store
from myssia.cli import EXIT_CONFIG_ERROR, EXIT_OK, main
import myssia.cli as cli_module
from myssia.gates import (
    GATES_FILE_NAME,
    GatesConfig,
    PlatformGate,
    SaaSGate,
    default_gates_path,
    gate_open,
    load_gates_config,
    load_gates_fail_closed,
    plugin_gate_key,
    plugin_gate_open,
    replace_analysis_switch,
    replace_platform_gate,
    replace_saas_gate,
    save_gates_config,
)
from myssia.plugins.manifest import load_manifest
from myssia.schema import LoadError
from myssia.secrets import (
    SECRET_SERVICE,
    InMemoryKeychainBackend,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

#: design.md §6.1 的示例文档形状(装载往返的黄金样本)。
FULL_GATES_YAML = """
version: 1
paid_engines: false
third_party_trace: false
saas:
  zenrows:
    enabled: false
    api_key: keychain:myia/saas/zenrows-key
  scraperapi:
    enabled: false
    api_key: keychain:myia/saas/scraperapi-key
platforms:
  crawlab:
    enabled: false
    endpoint: https://crawlab.example.com
    token: keychain:myia/platforms/crawlab-token
  worldmonitor:
    enabled: false
    endpoint: https://worldmonitor.example.com
analysis:
  snownlp_sentiment: false
"""

#: 带门槛声明 + 正交组合(tier: remote + gate: platform)的市场插件 manifest。
GATED_MANIFEST_YAML = """
id: myssia-crawlab
name: Crawlab(自有实例门槛)
version: 1.0.0
compatible: ">=0.0.1,<0.1"
tier: remote
gate: platform
provides: [crawlab]
modes:
  remote:
    endpoint: https://crawlab.example.com
install:
  source: https://github.com/myssia-official/myssia-crawlab.git
"""

#: 不声明 gate 的对照件(缺省 = 无门槛件)。
PLAIN_MANIFEST_YAML = """
id: myssia-plain
name: 普通件
version: 1.0.0
compatible: ">=0.0.1,<0.1"
tier: desktop
provides: [plain]
modes:
  local:
    install: echo ok
install:
  source: https://github.com/myssia-official/myssia-plain.git
"""


@pytest.fixture()
def backend() -> InMemoryKeychainBackend:
    """注入 mock 钥匙串(零真实触碰);测后复位不泄漏。"""
    injected = InMemoryKeychainBackend()
    secrets_store.set_backend(injected)
    yield injected
    secrets_store.reset_backend()


def write_gates(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def run_cli(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, dict[str, Any] | None]:
    """跑一条 CLI 命令,回(退出码, stdout 单份 JSON 或 None)。"""
    code = main(list(argv))
    out = capsys.readouterr().out
    return code, json.loads(out) if out.strip() else None


def make_market(tmp_path: Path, *manifests: str) -> Path:
    """建一个市场安装根,逐个写插件目录(plugin.yaml = manifest 文本)。"""
    market = tmp_path / "market"
    for manifest_text in manifests:
        data = yaml.safe_load(manifest_text)
        plugin_dir = market / str(data["id"])
        plugin_dir.mkdir(parents=True, exist_ok=True)
        (plugin_dir / "plugin.yaml").write_text(manifest_text, encoding="utf-8")
    return market


# ---------------------------------------------------------------------------
# 装载:缺失/空文件 = 全关;完整文档往返
# ---------------------------------------------------------------------------


class TestGatesLoad:
    def test_missing_file_loads_all_closed(self, tmp_path):
        config = load_gates_config(tmp_path / "gates.yaml")
        assert config == GatesConfig()
        assert config.to_payload() == {
            "version": 1,
            "paid_engines": False,
            "third_party_trace": False,
            "saas": {},
            "platforms": {},
            "analysis": {},
        }

    def test_empty_file_is_unconfigured(self, tmp_path):
        write_gates(tmp_path / "gates.yaml", "")
        assert load_gates_config(tmp_path / "gates.yaml") == GatesConfig()

    def test_full_document_round_trips(self, tmp_path):
        path = write_gates(tmp_path / "gates.yaml", FULL_GATES_YAML)
        config = load_gates_config(path)
        assert config.paid_engines is False
        assert config.third_party_trace is False
        assert config.saas == {
            "zenrows": SaaSGate(enabled=False, api_key_ref="keychain:myia/saas/zenrows-key"),
            "scraperapi": SaaSGate(enabled=False, api_key_ref="keychain:myia/saas/scraperapi-key"),
        }
        assert config.platforms == {
            "crawlab": PlatformGate(
                enabled=False,
                endpoint="https://crawlab.example.com",
                token_ref="keychain:myia/platforms/crawlab-token",
            ),
            "worldmonitor": PlatformGate(enabled=False, endpoint="https://worldmonitor.example.com"),
        }
        assert config.analysis == {"snownlp_sentiment": False}
        # to_payload → 再装载 = 同一配置(保存/显示共用同一视图)
        assert load_gates_config_from_payload(config.to_payload()) == config

    def test_default_gates_path_env_overrides(self, tmp_path, monkeypatch):
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        assert default_gates_path() == tmp_path / GATES_FILE_NAME
        monkeypatch.delenv("MYIA_HOME")
        assert default_gates_path() == Path.home() / ".myia" / GATES_FILE_NAME


def load_gates_config_from_payload(payload: dict[str, Any]) -> GatesConfig:
    """帮助器:payload → 临时文件 → load(测落盘视图往返,不走内存捷径)。"""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "gates.yaml"
        path.write_text(yaml.safe_dump(payload, allow_unicode=True), encoding="utf-8")
        return load_gates_config(path)


# ---------------------------------------------------------------------------
# 坏文件 = LoadError;fail-closed 装载 = 全关 + 结构化错误
# ---------------------------------------------------------------------------


class TestFailClosed:
    def test_broken_yaml_raises_load_error(self, tmp_path):
        path = write_gates(tmp_path / "gates.yaml", "saas: [unclosed\n")
        with pytest.raises(LoadError) as excinfo:
            load_gates_config(path)
        assert excinfo.value.errors[0].error_type == "gates_unreadable"

    def test_non_mapping_document_rejected(self, tmp_path):
        path = write_gates(tmp_path / "gates.yaml", "- a\n- b\n")
        with pytest.raises(LoadError):
            load_gates_config(path)

    def test_bad_field_file_fail_closed_all_off_with_error(self, tmp_path):
        """坏文件(未知字段)消费侧 = 全关 + 结构化错误带回,不静默。"""
        path = write_gates(tmp_path / "gates.yaml", "version: 1\npaid_engines: true\noops: 1\n")
        config, error = load_gates_fail_closed(path)
        assert config == GatesConfig()  # 全关 —— fail-closed,不半载
        assert error is not None
        assert error["errors"][0]["error_type"] == "unknown_field"

    def test_broken_yaml_fail_closed_all_off(self, tmp_path):
        path = write_gates(tmp_path / "gates.yaml", "}}not yaml{{\n")
        config, error = load_gates_fail_closed(path)
        assert config == GatesConfig()
        assert error is not None
        assert error["errors"][0]["error_type"] == "gates_unreadable"

    def test_good_file_fail_closed_returns_no_error(self, tmp_path):
        path = write_gates(tmp_path / "gates.yaml", FULL_GATES_YAML)
        config, error = load_gates_fail_closed(path)
        assert error is None
        assert config == load_gates_config(path)


# ---------------------------------------------------------------------------
# 构造即校验:未知字段拒 / keychain 引用形态 / 键名 / 版本 / 类型
# ---------------------------------------------------------------------------


class TestValidation:
    @pytest.mark.parametrize(
        ("text", "error_type"),
        [
            ("version: 1\nunknown_top: true\n", "unknown_field"),
            ("version: 2\n", "unsupported_version"),
            ("version: 1\npaid_engines: 'yes'\n", "invalid_field"),
            ("version: 1\nthird_party_trace: 1\n", "invalid_field"),
            ("version: 1\nsaas: zenrows\n", "invalid_field"),
            ("version: 1\nsaas:\n  zenrows: false\n", "invalid_field"),
            ("version: 1\nsaas:\n  zenrows:\n    enabled: false\n    oops: 1\n", "unknown_field"),
            ("version: 1\nsaas:\n  zenrows:\n    enabled: 'on'\n", "invalid_field"),
            ("version: 1\nplatforms:\n  crawlab:\n    oops: 1\n", "unknown_field"),
            ("version: 1\nplatforms:\n  crawlab:\n    endpoint: ftp://x.example.com\n", "invalid_endpoint"),
            ("version: 1\nanalysis: [1, 2]\n", "invalid_field"),
            ("version: 1\nanalysis:\n  snownlp: 'on'\n", "invalid_field"),
        ],
    )
    def test_structural_rejections(self, tmp_path, text, error_type):
        path = write_gates(tmp_path / "gates.yaml", text)
        with pytest.raises(LoadError) as excinfo:
            load_gates_config(path)
        assert excinfo.value.errors[0].error_type == error_type

    def test_plaintext_api_key_rejected(self, tmp_path):
        path = write_gates(
            tmp_path / "gates.yaml",
            "version: 1\nsaas:\n  zenrows:\n    api_key: sk-plain-value\n",
        )
        with pytest.raises(LoadError) as excinfo:
            load_gates_config(path)
        assert excinfo.value.errors[0].error_type == "credential_plaintext"
        assert "saas.zenrows.api_key" in excinfo.value.errors[0].path

    def test_env_ref_api_key_rejected_keychain_only(self, tmp_path):
        """env: 引用语法合法但门槛件只收钥匙串(§6.1「key 走钥匙串,零明文」)。"""
        path = write_gates(
            tmp_path / "gates.yaml",
            "version: 1\nsaas:\n  zenrows:\n    api_key: env:ZENROWS_KEY\n",
        )
        with pytest.raises(LoadError) as excinfo:
            load_gates_config(path)
        assert excinfo.value.errors[0].error_type == "invalid_credential_ref"

    def test_platform_plaintext_token_rejected(self, tmp_path):
        path = write_gates(
            tmp_path / "gates.yaml",
            "version: 1\nplatforms:\n  crawlab:\n    token: crawlab-plain-token\n",
        )
        with pytest.raises(LoadError) as excinfo:
            load_gates_config(path)
        assert excinfo.value.errors[0].error_type == "credential_plaintext"

    @pytest.mark.parametrize("bad_key", ["Bad-Name", "with space", "1x" + "y" * 100, ""])
    def test_bad_gate_key_rejected(self, tmp_path, bad_key):
        path = write_gates(
            tmp_path / "gates.yaml",
            "version: 1\nsaas:\n  {}: {{enabled: false}}\n".format(json.dumps(bad_key)),
        )
        with pytest.raises(LoadError) as excinfo:
            load_gates_config(path)
        assert excinfo.value.errors[0].error_type == "invalid_gate_key"

    def test_direct_construction_validates_too(self):
        """构造即校验:绕过 from_payload 直接构造也拒(与 VisionConfig 同门)。"""
        with pytest.raises(LoadError) as excinfo:
            GatesConfig(saas={"zenrows": "not-a-gate"})  # type: ignore[dict-item]
        assert excinfo.value.errors[0].error_type == "invalid_field"

    def test_direct_construction_bad_platform_endpoint(self):
        with pytest.raises(LoadError) as excinfo:
            GatesConfig(platforms={"crawlab": PlatformGate(enabled=True, endpoint="not-a-url")})
        assert excinfo.value.errors[0].error_type == "invalid_endpoint"

    def test_direct_construction_plaintext_api_key_rejected(self):
        """复审补:直接构造的明文 saas 引用同门拒 —— save 永写不出 load 拒收的文件。"""
        with pytest.raises(LoadError) as excinfo:
            GatesConfig(saas={"zenrows": SaaSGate(enabled=True, api_key_ref="PLAINTEXT-KEY-123")})
        assert excinfo.value.errors[0].error_type == "credential_plaintext"
        assert excinfo.value.errors[0].path == "saas.zenrows.api_key"

    def test_direct_construction_env_ref_rejected_both_kinds(self):
        """复审补:env: 引用在 saas.api_key 与 platforms.token 两侧都拒。"""
        with pytest.raises(LoadError) as excinfo:
            GatesConfig(saas={"zenrows": SaaSGate(enabled=True, api_key_ref="env:ZENROWS_KEY")})
        assert excinfo.value.errors[0].error_type == "invalid_credential_ref"
        with pytest.raises(LoadError) as excinfo:
            GatesConfig(
                platforms={
                    "crawlab": PlatformGate(
                        enabled=True, endpoint="https://crawlab.example.com", token_ref="env:CRAWLAB_TOKEN"
                    )
                }
            )
        assert excinfo.value.errors[0].error_type == "invalid_credential_ref"
        assert excinfo.value.errors[0].path == "platforms.crawlab.token"

    def test_direct_construction_keychain_refs_and_none_accepted_round_trip(self, tmp_path):
        """复审补:合法形态(None / keychain: 引用)直接构造可通过,save→load 同门往返。"""
        config = GatesConfig(
            saas={"zenrows": SaaSGate(enabled=True, api_key_ref="keychain:myia/saas/zenrows-key")},
            platforms={
                "crawlab": PlatformGate(
                    enabled=True,
                    endpoint="https://crawlab.example.com",
                    token_ref="keychain:myia/platforms/crawlab-token",
                ),
                "worldmonitor": PlatformGate(enabled=False, endpoint="", token_ref=None),
            },
        )
        path = save_gates_config(tmp_path / "gates.yaml", config)
        assert load_gates_config(path) == config  # 写读同门:往返逐字段等价

    def test_replace_gate_with_plaintext_ref_rejected(self):
        """复审补:replace_saas_gate/replace_platform_gate 携裸明文引用也过不了构造门。"""
        base = GatesConfig()
        with pytest.raises(LoadError) as excinfo:
            replace_saas_gate(base, "zenrows", SaaSGate(enabled=True, api_key_ref="plaintext"))
        assert excinfo.value.errors[0].error_type == "credential_plaintext"
        with pytest.raises(LoadError):
            replace_platform_gate(
                base, "crawlab", PlatformGate(enabled=True, endpoint="https://x.example.com", token_ref="plaintext")
            )


# ---------------------------------------------------------------------------
# gate_open 唯一查询口 + 每开关往返
# ---------------------------------------------------------------------------


class TestGateOpen:
    def _rich_config(self) -> GatesConfig:
        return GatesConfig(
            paid_engines=True,
            third_party_trace=True,
            saas={"zenrows": SaaSGate(enabled=True, api_key_ref="keychain:myia/saas/zenrows-key")},
            platforms={"crawlab": PlatformGate(enabled=True, endpoint="https://crawlab.example.com")},
            analysis={"snownlp_sentiment": True},
        )

    def test_gate_open_matrix(self):
        config = self._rich_config()
        assert gate_open(config, "paid_engines") is True
        assert gate_open(config, "third_party_trace") is True
        assert gate_open(config, "saas", "zenrows") is True
        assert gate_open(config, "platforms", "crawlab") is True
        assert gate_open(config, "analysis", "snownlp_sentiment") is True

    def test_unknown_item_key_is_closed(self):
        config = self._rich_config()
        assert gate_open(config, "saas", "scraperapi") is False
        assert gate_open(config, "platforms", "worldmonitor") is False
        assert gate_open(config, "analysis", "recon-ng") is False

    def test_saas_item_requires_total_switch(self):
        """§6.3:总开关或件开关未开即 gate_closed —— 件开而总关 = 关。"""
        config = dataclass_replace(self._rich_config(), paid_engines=False)
        assert gate_open(config, "saas", "zenrows") is False

    def test_unknown_kind_is_programming_error(self):
        config = self._rich_config()
        with pytest.raises(ValueError):
            gate_open(config, "bogus")
        with pytest.raises(ValueError):
            gate_open(config, "saas")  # 逐件 kind 缺名 = 编程错误,不静默全关

    def test_every_switch_round_trips_on_then_off(self, tmp_path):
        """每开关往返:五个 kind 逐一开 → 存取等价 → 逐一关 → 存取等价、全关。"""
        path = tmp_path / "gates.yaml"
        config = GatesConfig()
        config = dataclass_replace(config, paid_engines=True)
        config = dataclass_replace(config, third_party_trace=True)
        config = replace_saas_gate(
            config, "zenrows", SaaSGate(enabled=True, api_key_ref="keychain:myia/saas/zenrows-key")
        )
        config = replace_platform_gate(
            config,
            "crawlab",
            PlatformGate(
                enabled=True,
                endpoint="https://crawlab.example.com",
                token_ref="keychain:myia/platforms/crawlab-token",
            ),
        )
        config = replace_analysis_switch(config, "snownlp_sentiment", True)
        save_gates_config(path, config)
        assert load_gates_config(path) == config
        assert gate_open(load_gates_config(path), "saas", "zenrows") is True
        # 关向往返
        config = dataclass_replace(config, paid_engines=False)
        config = dataclass_replace(config, third_party_trace=False)
        config = replace_saas_gate(config, "zenrows", SaaSGate(enabled=False))
        config = replace_platform_gate(
            config, "crawlab", PlatformGate(enabled=False, endpoint="https://crawlab.example.com")
        )
        config = replace_analysis_switch(config, "snownlp_sentiment", False)
        save_gates_config(path, config)
        reloaded = load_gates_config(path)
        assert reloaded == config
        assert gate_open(reloaded, "saas", "zenrows") is False
        assert gate_open(reloaded, "platforms", "crawlab") is False
        assert gate_open(reloaded, "analysis", "snownlp_sentiment") is False


class TestPluginGateDerivation:
    def test_manifest_gate_to_gates_state(self):
        config = GatesConfig(
            paid_engines=True,
            third_party_trace=True,
            saas={"zenrows": SaaSGate(enabled=True)},
            platforms={"crawlab": PlatformGate(enabled=True, endpoint="https://crawlab.example.com")},
            analysis={"snownlp": True},
        )
        # 官方件惯例:myssia- 前缀剥掉后即 gates.yaml 逐件键
        assert plugin_gate_key("myssia-crawlab") == "crawlab"
        assert plugin_gate_key("community-tool") == "community-tool"  # 无前缀原样
        assert plugin_gate_open(config, "paid", "myssia-zenrows") is True
        assert plugin_gate_open(config, "trace", "myssia-rsshub") is True
        assert plugin_gate_open(config, "platform", "myssia-crawlab") is True
        assert plugin_gate_open(config, "stale", "myssia-snownlp") is True
        assert plugin_gate_open(config, "platform", "myssia-worldmonitor") is False

    def test_paid_plugin_requires_total_switch_too(self):
        config = GatesConfig(saas={"zenrows": SaaSGate(enabled=True)})  # 总开关关
        assert plugin_gate_open(config, "paid", "myssia-zenrows") is False

    def test_unknown_manifest_gate_is_programming_error(self):
        with pytest.raises(ValueError):
            plugin_gate_open(GatesConfig(), "bogus", "myssia-x")


# ---------------------------------------------------------------------------
# manifest gate 字段(D5:独立字段,与 TIER_TOKENS 正交)
# ---------------------------------------------------------------------------


def manifest_data(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": "myssia-crawlab",
        "name": "Crawlab(自有实例门槛)",
        "version": "1.0.0",
        "compatible": ">=0.0.1,<0.1",
        "tier": "remote",
        "provides": ["crawlab"],
        "modes": {"remote": {"endpoint": "https://crawlab.example.com"}},
        "install": {"source": "https://github.com/myssia-official/myssia-crawlab.git"},
    }
    data.update(overrides)
    return data


class TestManifestGateField:
    @pytest.mark.parametrize("token", ["paid", "trace", "platform", "stale"])
    def test_gate_tokens_accepted(self, token):
        assert load_manifest(manifest_data(gate=token)).gate == token

    def test_gate_defaults_to_none(self):
        assert load_manifest(manifest_data()).gate is None

    def test_gate_orthogonal_to_tier(self):
        """D5:crawlab = tier: remote + gate: platform 正交组合,tier 词表不动。"""
        manifest = load_manifest(manifest_data(gate="platform"))
        assert manifest.tier == "remote"
        assert manifest.gate == "platform"

    def test_invalid_gate_rejected(self):
        with pytest.raises(LoadError) as excinfo:
            load_manifest(manifest_data(gate="gated"))
        assert excinfo.value.errors[0].error_type == "invalid_gate"


# ---------------------------------------------------------------------------
# CLI:myssia gates show / set(D7,照 secret 命令族)
# ---------------------------------------------------------------------------


class TestGatesCliShowSet:
    def test_show_missing_file_all_closed_exit_ok(self, tmp_path, capsys):
        gates_file = tmp_path / "gates.yaml"
        code, payload = run_cli(
            capsys, "gates", "show", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        assert payload["exists"] is False
        assert payload["config"]["paid_engines"] is False
        assert payload["config"]["saas"] == {}

    def test_show_broken_file_structured_error(self, tmp_path, capsys):
        gates_file = write_gates(tmp_path / "gates.yaml", "oops: [\n")
        code, payload = run_cli(
            capsys, "gates", "show", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_CONFIG_ERROR
        assert payload["error"] == "gates"
        assert payload["code"] == "gates_invalid"
        assert payload["errors"]

    def test_set_show_round_trip_total_switches(self, tmp_path, capsys):
        gates_file = tmp_path / "gates.yaml"
        code, _ = run_cli(
            capsys, "gates", "set", "paid_engines", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        code, payload = run_cli(capsys, "gates", "show", "--file", str(gates_file), "--json")
        assert payload["config"]["paid_engines"] is True
        code, _ = run_cli(
            capsys, "gates", "set", "third_party_trace", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        _, payload = run_cli(capsys, "gates", "show", "--file", str(gates_file), "--json")
        assert payload["config"]["third_party_trace"] is True
        # off 往返
        code, _ = run_cli(
            capsys, "gates", "set", "paid_engines", "off", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        _, payload = run_cli(capsys, "gates", "show", "--file", str(gates_file), "--json")
        assert payload["config"]["paid_engines"] is False

    def test_set_analysis_switch_round_trip_no_key_needed(self, tmp_path, capsys, backend):
        """analysis 纯布尔开关:无凭据,直接往返(D8:批三才落分析件)。"""
        gates_file = tmp_path / "gates.yaml"
        code, payload = run_cli(
            capsys,
            "gates", "set", "analysis.snownlp_sentiment", "on",
            "--file", str(gates_file), "--json",
        )
        assert code == EXIT_OK
        assert payload["config"]["analysis"] == {"snownlp_sentiment": True}
        code, _ = run_cli(
            capsys,
            "gates", "set", "analysis.snownlp_sentiment", "off",
            "--file", str(gates_file), "--json",
        )
        assert code == EXIT_OK
        _, payload = run_cli(capsys, "gates", "show", "--file", str(gates_file), "--json")
        assert payload["config"]["analysis"] == {"snownlp_sentiment": False}

    def test_set_saas_with_key_round_trip(self, tmp_path, capsys, backend):
        """键在位 → on 成功且规范引用物化进配置;off 不查键。"""
        gates_file = tmp_path / "gates.yaml"
        backend.set_password(SECRET_SERVICE, "myia/saas/zenrows-key", "sk-test")
        code, payload = run_cli(
            capsys, "gates", "set", "saas.zenrows", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        assert payload["config"]["saas"]["zenrows"] == {
            "enabled": True,
            "api_key": "keychain:myia/saas/zenrows-key",
        }
        # CLI 层钉 §6.3:件开而总开关关 = gate_closed 语义
        _, shown = run_cli(capsys, "gates", "show", "--file", str(gates_file), "--json")
        assert shown["config"]["paid_engines"] is False
        assert shown["config"]["saas"]["zenrows"]["enabled"] is True
        # 开总开关后组合生效(gate_open 口径)
        config = load_gates_config(gates_file)
        assert gate_open(config, "saas", "zenrows") is False
        run_cli(capsys, "gates", "set", "paid_engines", "on", "--file", str(gates_file), "--json")
        assert gate_open(load_gates_config(gates_file), "saas", "zenrows") is True
        # off 往返(无需键)
        code, _ = run_cli(
            capsys, "gates", "set", "saas.zenrows", "off", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        assert load_gates_config(gates_file).saas["zenrows"].enabled is False

    def test_set_platform_with_token_round_trip(self, tmp_path, capsys, backend):
        gates_file = write_gates(
            tmp_path / "gates.yaml",
            (
                "version: 1\n"
                "platforms:\n"
                "  crawlab:\n"
                "    enabled: false\n"
                "    endpoint: https://crawlab.example.com\n"
                "    token: keychain:myia/platforms/crawlab-token\n"
            ),
        )
        backend.set_password(SECRET_SERVICE, "myia/platforms/crawlab-token", "tok")
        code, payload = run_cli(
            capsys, "gates", "set", "platforms.crawlab", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        # endpoint/token 原样保留,enabled 翻转
        assert payload["config"]["platforms"]["crawlab"]["endpoint"] == "https://crawlab.example.com"
        assert payload["config"]["platforms"]["crawlab"]["token"] == "keychain:myia/platforms/crawlab-token"
        assert payload["config"]["platforms"]["crawlab"]["enabled"] is True

    def test_set_platform_without_token_needs_no_key(self, tmp_path, capsys, backend):
        """platform 无 token 声明(worldmonitor 形态)无键可查 → 直接开(D6 不执法)。"""
        gates_file = write_gates(
            tmp_path / "gates.yaml",
            (
                "version: 1\n"
                "platforms:\n"
                "  worldmonitor:\n"
                "    enabled: false\n"
                "    endpoint: https://worldmonitor.example.com\n"
            ),
        )
        code, _ = run_cli(
            capsys, "gates", "set", "platforms.worldmonitor", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        assert load_gates_config(gates_file).platforms["worldmonitor"].enabled is True

    @pytest.mark.parametrize(
        ("target", "value"),
        [
            ("bogus.zenrows", "on"),  # 未知 kind
            ("paid_engines.zenrows", "on"),  # 总开关带逐件名
            ("saas", "on"),  # 逐件 kind 缺名
            ("saas.Bad-Name", "on"),  # 逐件名非法
        ],
    )
    def test_set_invalid_target_structured_reject(self, tmp_path, capsys, target, value):
        gates_file = tmp_path / "gates.yaml"
        code, payload = run_cli(
            capsys, "gates", "set", target, value, "--file", str(gates_file), "--json"
        )
        assert code == EXIT_CONFIG_ERROR
        assert payload["code"] == "invalid_target"
        assert not gates_file.exists()  # 零写入

    def test_set_broken_file_zero_write(self, tmp_path, capsys):
        original = "oops: [\n"
        gates_file = write_gates(tmp_path / "gates.yaml", original)
        code, payload = run_cli(
            capsys, "gates", "set", "paid_engines", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_CONFIG_ERROR
        assert payload["code"] == "gates_invalid"
        assert gates_file.read_text(encoding="utf-8") == original  # 零写入


# ---------------------------------------------------------------------------
# 逐件 on 缺钥匙串键 = 结构化拒(fail-closed,零写入)
# ---------------------------------------------------------------------------


class TestGateKeyEnforcement:
    def test_set_saas_on_missing_key_rejected_zero_write(self, tmp_path, capsys, backend):
        """键不在位(空 mock 钥匙串)→ gate_key_missing,退出码 1,零写入。"""
        gates_file = tmp_path / "gates.yaml"
        code, payload = run_cli(
            capsys, "gates", "set", "saas.zenrows", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_CONFIG_ERROR
        assert payload["code"] == "gate_key_missing"
        assert "myssia secret set myia/saas/zenrows-key" in payload["message"]
        assert not gates_file.exists()  # 拒绝开启 = 零写入

    def test_set_platform_on_missing_token_rejected_zero_write(self, tmp_path, capsys, backend):
        gates_file = write_gates(
            tmp_path / "gates.yaml",
            (
                "version: 1\n"
                "platforms:\n"
                "  crawlab:\n"
                "    enabled: false\n"
                "    endpoint: https://crawlab.example.com\n"
                "    token: keychain:myia/platforms/crawlab-token\n"
            ),
        )
        code, payload = run_cli(
            capsys, "gates", "set", "platforms.crawlab", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_CONFIG_ERROR
        assert payload["code"] == "gate_key_missing"
        assert "enabled: false" in gates_file.read_text(encoding="utf-8")  # 零写入

    def test_set_saas_on_backend_unavailable_rejected(self, tmp_path, capsys, monkeypatch):
        """钥匙链后端不可用 = 无法确认键在位,fail-closed 拒绝开启(不静默放行)。"""
        monkeypatch.setattr(cli_module, "_safe_keychain_backend", lambda: None)
        gates_file = tmp_path / "gates.yaml"
        code, payload = run_cli(
            capsys, "gates", "set", "saas.zenrows", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_CONFIG_ERROR
        assert payload["code"] == "gate_key_unverifiable"
        assert not gates_file.exists()

    def test_set_custom_api_key_ref_checks_that_name(self, tmp_path, capsys, backend):
        """显式配置的自定义引用优先于规范缺省名:查自定义名,不查缺省名。"""
        gates_file = write_gates(
            tmp_path / "gates.yaml",
            (
                "version: 1\n"
                "saas:\n"
                "  zenrows:\n"
                "    enabled: false\n"
                "    api_key: keychain:myia/saas/custom-zenrows\n"
            ),
        )
        backend.set_password(SECRET_SERVICE, "myia/saas/zenrows-key", "wrong-name-key")
        code, payload = run_cli(
            capsys, "gates", "set", "saas.zenrows", "on", "--file", str(gates_file), "--json"
        )
        assert code == EXIT_CONFIG_ERROR
        assert payload["code"] == "gate_key_missing"
        assert "myia/saas/custom-zenrows" in payload["message"]


# ---------------------------------------------------------------------------
# plugin list:门槛件分组 + enabled 徽标(gates.yaml 状态派生)
# ---------------------------------------------------------------------------


class TestPluginListGates:
    def test_gated_group_and_badges_derived_from_gates(self, tmp_path, capsys):
        market = make_market(tmp_path, GATED_MANIFEST_YAML, PLAIN_MANIFEST_YAML)
        gates_file = write_gates(
            tmp_path / "gates.yaml",
            (
                "version: 1\n"
                "platforms:\n"
                "  crawlab:\n"
                "    enabled: true\n"
                "    endpoint: https://crawlab.example.com\n"
            ),
        )
        code, payload = run_cli(
            capsys, "plugin", "list", "--dir", str(market), "--gates-file", str(gates_file), "--json"
        )
        assert code == EXIT_OK
        gated = payload["gates"]["gated"]
        assert [item["id"] for item in gated] == ["myssia-crawlab"]
        assert gated[0]["gate"] == "platform"
        assert gated[0]["key"] == "crawlab"  # 派生查询键 = id 去 myssia- 前缀
        assert gated[0]["enabled"] is True
        by_id = {plugin["id"]: plugin for plugin in payload["plugins"]}
        assert by_id["myssia-crawlab"]["gate"] == "platform"
        assert by_id["myssia-crawlab"]["gate_enabled"] is True
        assert by_id["myssia-plain"]["gate"] is None
        assert by_id["myssia-plain"]["gate_enabled"] is None
        assert payload["summary"]["gated_total"] == 1
        assert payload["summary"]["gated_enabled"] == 1

    def test_disabled_badge_when_gate_closed(self, tmp_path, capsys):
        market = make_market(tmp_path, GATED_MANIFEST_YAML)
        gates_file = write_gates(
            tmp_path / "gates.yaml",
            (
                "version: 1\n"
                "platforms:\n"
                "  crawlab:\n"
                "    enabled: false\n"
                "    endpoint: https://crawlab.example.com\n"
            ),
        )
        _, payload = run_cli(
            capsys, "plugin", "list", "--dir", str(market), "--gates-file", str(gates_file), "--json"
        )
        assert payload["gates"]["gated"][0]["enabled"] is False
        assert payload["plugins"][0]["gate_enabled"] is False
        assert payload["summary"]["gated_enabled"] == 0

    def test_broken_gates_file_all_closed_with_error(self, tmp_path, capsys):
        """坏 gates.yaml → 徽标全关 + 顶层 gates.error 结构化(fail-closed 不静默)。"""
        market = make_market(tmp_path, GATED_MANIFEST_YAML)
        gates_file = write_gates(tmp_path / "gates.yaml", "oops: [\n")
        code, payload = run_cli(
            capsys, "plugin", "list", "--dir", str(market), "--gates-file", str(gates_file), "--json"
        )
        assert code == EXIT_OK  # 信息性命令:门槛全关不拦 list
        assert payload["plugins"][0]["gate_enabled"] is False
        assert payload["gates"]["error"] is not None
        assert payload["summary"]["gated_enabled"] == 0


# ---------------------------------------------------------------------------
# doctor:未启用门槛件 = info(非 warning);坏 gates.yaml = warning
# ---------------------------------------------------------------------------


def run_doctor(capsys: pytest.CaptureFixture[str], tmp_path: Path, market: Path, gates_file: Path):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir(exist_ok=True)
    return run_cli(
        capsys,
        "doctor",
        "--plugins-dir", str(plugins_dir),
        "--db", str(tmp_path / "myssia.db"),
        "--dir", str(market),
        "--gates-file", str(gates_file),
        "--json",
    )


class TestDoctorGates:
    def test_disabled_gate_is_info_not_warning(self, tmp_path, capsys, backend):
        market = make_market(tmp_path, GATED_MANIFEST_YAML)
        gates_file = tmp_path / "gates.yaml"  # 不存在 = 全关
        code, payload = run_doctor(capsys, tmp_path, market, gates_file)
        assert code == EXIT_OK
        disabled = [f for f in payload["findings"] if f["code"] == "gate_disabled"]
        assert len(disabled) == 1
        # 词表纪律(§6.2):用户没开是正常态,info 与 warning 分开
        assert disabled[0]["severity"] == "info"
        assert disabled[0]["scope"] == "plugin:myssia-crawlab"
        assert payload["summary"]["warnings"] == 0
        assert payload["healthy"] is True
        assert payload["gates"]["gated"] == [
            {"id": "myssia-crawlab", "gate": "platform", "enabled": False}
        ]

    def test_enabled_gate_no_finding(self, tmp_path, capsys, backend):
        market = make_market(tmp_path, GATED_MANIFEST_YAML)
        gates_file = write_gates(
            tmp_path / "gates.yaml",
            (
                "version: 1\n"
                "platforms:\n"
                "  crawlab:\n"
                "    enabled: true\n"
                "    endpoint: https://crawlab.example.com\n"
            ),
        )
        code, payload = run_doctor(capsys, tmp_path, market, gates_file)
        assert code == EXIT_OK
        assert not [f for f in payload["findings"] if f["code"] == "gate_disabled"]
        assert payload["gates"]["gated"][0]["enabled"] is True

    def test_broken_gates_is_warning_and_gates_stay_closed(self, tmp_path, capsys, backend):
        market = make_market(tmp_path, GATED_MANIFEST_YAML)
        gates_file = write_gates(tmp_path / "gates.yaml", "oops: [\n")
        code, payload = run_doctor(capsys, tmp_path, market, gates_file)
        assert code == EXIT_OK
        invalid = [f for f in payload["findings"] if f["code"] == "gates_invalid"]
        assert len(invalid) == 1
        assert invalid[0]["severity"] == "warning"
        # fail-closed:坏文件按全关处理 → 门槛件仍出 info(未启用)
        disabled = [f for f in payload["findings"] if f["code"] == "gate_disabled"]
        assert len(disabled) == 1 and disabled[0]["severity"] == "info"
        assert payload["gates"]["error"] is not None

    def test_plain_market_plugin_no_gate_findings(self, tmp_path, capsys, backend):
        market = make_market(tmp_path, PLAIN_MANIFEST_YAML)
        code, payload = run_doctor(capsys, tmp_path, market, tmp_path / "gates.yaml")
        assert code == EXIT_OK
        assert payload["gates"]["gated"] == []
        assert not [f for f in payload["findings"] if f["scope"].startswith("plugin:myssia-plain")]


# ---------------------------------------------------------------------------
# desktop/entry.py:gates.yaml 路径解析挂 _serve_context 优先级链
# ---------------------------------------------------------------------------


def _load_entry_module():
    spec = importlib.util.spec_from_file_location(
        "desktop_entry_gates", REPO_ROOT / "desktop" / "entry.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TestDesktopGatesPath:
    def test_home_mode_same_position_as_vision(self, tmp_path, monkeypatch):
        module = _load_entry_module()
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        ctx = module._serve_context()
        assert ctx.home == tmp_path
        assert module._gates_yaml_path(ctx) == tmp_path / "gates.yaml"
        assert module._vision_yaml_path(ctx) == tmp_path / "vision.yaml"
        # 与 vision.yaml 同位(同一数据根、同一文件名约定)
        assert module._gates_yaml_path(ctx).parent == module._vision_yaml_path(ctx).parent

    def test_dev_fallback_cwd_relative_like_vision(self, monkeypatch):
        module = _load_entry_module()
        monkeypatch.delenv("MYIA_HOME", raising=False)
        ctx = module._serve_context()
        assert ctx.home is None
        assert module._gates_yaml_path(ctx) == Path("gates.yaml")
        assert module._vision_yaml_path(ctx) == Path("vision.yaml")


class TestDesktopGatesHandlers:
    """sidecar ``gates.get``/``gates.save``(design §6.7 契约;设置屏修复入口)。"""

    def test_handlers_registered(self):
        module = _load_entry_module()
        assert module._HANDLERS["gates.get"] is module._m_gates_get
        assert module._HANDLERS["gates.save"] is module._m_gates_save

    def test_get_missing_file_all_closed(self, tmp_path, monkeypatch):
        module = _load_entry_module()
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        payload = module._m_gates_get({})
        assert payload["path"] == str(tmp_path / "gates.yaml")
        assert payload["exists"] is False
        assert payload["error"] is None
        assert payload["config"] == GatesConfig().to_payload()

    def test_get_broken_file_fail_closed_with_error(self, tmp_path, monkeypatch):
        module = _load_entry_module()
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        write_gates(tmp_path / "gates.yaml", "{ not yaml")
        payload = module._m_gates_get({})
        # fail-closed:设置屏不炸,全关态 + 结构化 error 带回(修复入口还在)
        assert payload["exists"] is True
        assert payload["config"] == GatesConfig().to_payload()
        assert payload["error"]["errors"][0]["error_type"] == "gates_unreadable"

    def test_save_then_get_round_trip(self, tmp_path, monkeypatch):
        module = _load_entry_module()
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        document = yaml.safe_load(FULL_GATES_YAML)
        document["paid_engines"] = True
        result = module._m_gates_save({"config": document})
        assert result["ok"] is True
        assert result["path"] == str(tmp_path / "gates.yaml")
        assert (tmp_path / "gates.yaml").exists()
        # get 往返:keychain 引用原样回显,永不携带解析值
        payload = module._m_gates_get({})
        assert payload["exists"] is True
        assert payload["error"] is None
        assert payload["config"]["paid_engines"] is True
        assert payload["config"]["saas"]["zenrows"]["api_key"] == "keychain:myia/saas/zenrows-key"

    def test_save_invalid_config_structured_error_zero_write(self, tmp_path, monkeypatch):
        module = _load_entry_module()
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        document = yaml.safe_load(FULL_GATES_YAML)
        document["unknown_switch"] = True  # 未知字段 → 同门拒收
        with pytest.raises(module.ProtocolError) as excinfo:
            module._m_gates_save({"config": document})
        assert excinfo.value.code == "gates_config_invalid"
        assert excinfo.value.data["errors"][0]["error_type"] == "unknown_field"
        assert not (tmp_path / "gates.yaml").exists()  # 零写入

    def test_save_missing_config_param_rejected(self, tmp_path, monkeypatch):
        module = _load_entry_module()
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        with pytest.raises(module.ProtocolError) as excinfo:
            module._m_gates_save({})
        assert excinfo.value.code == "invalid_params"
        assert not (tmp_path / "gates.yaml").exists()
