"""轨D remote 声明配置(plugins.remote.*,10-06-native-plugin-components 阶段3
G-Q1/R7):tier=remote 插件件的端点/凭据引用读写 + env 桥接。

sidecar 方法族的协议单测(mock stdin/stdout 往返,与
test_bundled_plugins_install.py 同款 rpc 手法;独立实现零跨文件共享)。

核心口径(设计 §6 轨D 数据面):

- **配置落数据根** ``<home>/remote-plugins.json``(endpoint 具体值 + token
  keychain 引用);dev 形态无数据根 → ``remote_config_unavailable`` 结构化拒
  (env = 开发后门);
- **keychain-only 判例同规**:token 只收 ``keychain:`` 规范引用(明文凭据经
  secret.set 入钥匙串,永不落本配置);endpoint 只收 http(s) 具体地址;
- **env 桥接零引擎改动**:save 后即时桥接 + serve 启动桥接
  (``MYIA_FIRECRAWL_URL``/``MYIA_FIRECRAWL_API_KEY``,引擎 firecrawl.py 既有
  env 通道);显式 env(开发后门)恒优先不被覆写。

测试纪律:零真实网络(本文件不探活——doctor 连通项归 tests/cli 域)、
InMemoryKeychainBackend、每测独立 tmp_path。
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRY_PATH = REPO_ROOT / "desktop" / "entry.py"

_spec = importlib.util.spec_from_file_location("desktop_entry_remote", ENTRY_PATH)
entry = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(entry)

from myssia.secrets import InMemoryKeychainBackend  # noqa: E402
from myssia.secrets import reset_backend as reset_keychain_backend  # noqa: E402
from myssia.secrets import set_backend as set_keychain_backend  # noqa: E402
from myssia.secrets import set_secret  # noqa: E402

#: firecrawl 桥接的 env 对(_REMOTE_ENGINE_BRIDGE 同源;测试直取名,防漂移
#: 断言写死字符串)。
FC_URL_ENV = "MYIA_FIRECRAWL_URL"
FC_KEY_ENV = "MYIA_FIRECRAWL_API_KEY"
FC_TOKEN_NAME = "myia/firecrawl/api-key"


@pytest.fixture(autouse=True)
def _reset_sidecar_state(monkeypatch, tmp_path):
    """每例干净态:MYIA_HOME/MYIA_PLUGIN_DIR/firecrawl env 隔离 + 桥接记账清空
    + 钥匙串内存后端(_BRIDGED_ENV 是模块级,跨例残留会把「我方写值」误当
    显式 env,桥接语义断言必炸)。

    收尾**强制 pop** 桥接 env:桥接是 ``os.environ`` 直写(非 monkeypatch
    通道),monkeypatch 拆卸不知情——不 pop 则泄漏整个 pytest 进程,后续
    doctor 域测试会「已配置 firecrawl」触发真实网络探测(顺序依赖红)。
    """
    monkeypatch.delenv("MYIA_HOME", raising=False)
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(tmp_path / "isolated-install-root"))
    monkeypatch.delenv(entry.BUNDLED_PLUGINS_ENV, raising=False)
    monkeypatch.delenv(FC_URL_ENV, raising=False)
    monkeypatch.delenv(FC_KEY_ENV, raising=False)
    entry._BRIDGED_ENV.clear()
    entry._stop_cron_ticker()
    set_keychain_backend(InMemoryKeychainBackend())
    yield
    entry._BRIDGED_ENV.clear()
    os.environ.pop(FC_URL_ENV, None)
    os.environ.pop(FC_KEY_ENV, None)
    entry._stop_cron_ticker()
    reset_keychain_backend()


@pytest.fixture()
def home(monkeypatch, tmp_path) -> Path:
    """home 沙箱:MYIA_HOME 指一次性数据根(remote 配置落点)。"""
    path = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(path))
    return path


def rpc(*requests: dict) -> tuple[int, list[dict], list[dict]]:
    """整轮 RPC(与 test_bundled_plugins_install.py 同款;独立实现零共享)。"""
    lines = [json.dumps(req, ensure_ascii=False) for req in requests]
    stdin = io.StringIO("".join(line + "\n" for line in lines))
    out = io.StringIO()
    code = entry.serve(stdin=stdin, stdout=out)
    responses: list[dict] = []
    events: list[dict] = []
    for line in out.getvalue().splitlines():
        obj = json.loads(line)
        (responses if "id" in obj else events).append(obj)
    return code, responses, events


def _get(plugin_id: str = "myssia-firecrawl") -> dict:
    _, responses, _ = rpc(
        {"id": 1, "method": "plugins.remote.get", "params": {"id": plugin_id}}
    )
    assert "result" in responses[0], f"get 应答应为 result: {responses[0]}"
    return responses[0]["result"]


def _save(params: dict) -> dict:
    _, responses, _ = rpc({"id": 2, "method": "plugins.remote.save", "params": params})
    return responses[0]


# ---------------------------------------------------------------------------
# get:未配置如实 / roundtrip / dev 形态结构化拒
# ---------------------------------------------------------------------------


def test_get_unknown_plugin_is_unconfigured_truthful(home):
    """未配置件:endpoint/token null + known=false 如实(不虚构不报错)。"""
    result = _get()
    assert result == {
        "id": "myssia-firecrawl",
        "endpoint": None,
        "token": None,
        "known": False,
    }


def test_get_and_save_roundtrip_persists_in_data_root(home):
    """save → 落数据根 remote-plugins.json;get 回读一致(token 只存引用)。"""
    outcome = _save(
        {
            "id": "myssia-firecrawl",
            "endpoint": "https://fc.mine.example.org",
            "token": f"keychain:{FC_TOKEN_NAME}",
        }
    )
    assert outcome["result"] == {
        "ok": True,
        "id": "myssia-firecrawl",
        "path": str(home / entry.REMOTE_PLUGINS_CONFIG),
        "endpoint": "https://fc.mine.example.org",
    }
    raw = json.loads((home / entry.REMOTE_PLUGINS_CONFIG).read_text(encoding="utf-8"))
    assert raw["myssia-firecrawl"] == {
        "endpoint": "https://fc.mine.example.org",
        "token": f"keychain:{FC_TOKEN_NAME}",
    }
    assert _get() == {
        "id": "myssia-firecrawl",
        "endpoint": "https://fc.mine.example.org",
        "token": f"keychain:{FC_TOKEN_NAME}",
        "known": True,
    }


def test_save_without_token_keeps_existing_reference(home):
    """token 不传 = 保持现值(只改端点不清凭据引用)。"""
    _save(
        {
            "id": "myssia-firecrawl",
            "endpoint": "https://a.example.org",
            "token": f"keychain:{FC_TOKEN_NAME}",
        }
    )
    _save({"id": "myssia-firecrawl", "endpoint": "https://b.example.org"})
    result = _get()
    assert result["endpoint"] == "https://b.example.org"
    assert result["token"] == f"keychain:{FC_TOKEN_NAME}"


def test_dev_mode_without_home_is_structured_reject(monkeypatch):
    """dev 形态(无 MYIA_HOME)= remote_config_unavailable(开发后门=env)。"""
    monkeypatch.delenv("MYIA_HOME", raising=False)
    _, responses, _ = rpc(
        {"id": 1, "method": "plugins.remote.get", "params": {"id": "myssia-firecrawl"}}
    )
    assert responses[0]["error"]["code"] == "remote_config_unavailable"
    _, responses, _ = rpc(
        {
            "id": 2,
            "method": "plugins.remote.save",
            "params": {"id": "myssia-firecrawl", "endpoint": "https://x.example.org"},
        }
    )
    assert responses[0]["error"]["code"] == "remote_config_unavailable"


def test_corrupt_config_file_is_structured_reject(home):
    """坏 JSON 配置 → remote_config_invalid(不静默吞手改坏件)。"""
    home.mkdir(parents=True, exist_ok=True)
    (home / entry.REMOTE_PLUGINS_CONFIG).write_text("{not json", encoding="utf-8")
    _, responses, _ = rpc(
        {"id": 1, "method": "plugins.remote.get", "params": {"id": "myssia-firecrawl"}}
    )
    assert responses[0]["error"]["code"] == "remote_config_invalid"


# ---------------------------------------------------------------------------
# 校验:keychain-only 判例同规(端点具体地址 / token 只收引用)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_endpoint",
    [
        "",
        "not-a-url",
        "ftp://fc.example.org",
        "env:MYIA_FIRECRAWL_URL",  # 引用不是端点:引用属品类 YAML/env 通道
        f"keychain:{FC_TOKEN_NAME}",
    ],
)
def test_save_rejects_non_http_endpoint(home, bad_endpoint):
    """endpoint 只收 http(s) 具体地址;引用形态一律 invalid_params。"""
    response = _save({"id": "myssia-firecrawl", "endpoint": bad_endpoint})
    assert response["error"]["code"] == "invalid_params"
    assert response["error"]["path"] == "params.endpoint"
    assert not (home / entry.REMOTE_PLUGINS_CONFIG).exists(), "拒收零落盘"


@pytest.mark.parametrize(
    ("bad_token", "expected_code"),
    [
        (
            "sk-plaintext-secret",
            "invalid_params",
        ),  # 明文凭据:永不落配置(keychain-only 判例)
        ("env:MYIA_FIRECRAWL_API_KEY", "invalid_params"),
        ("", "invalid_params"),
        # keychain: 前缀但名字不合规范:secrets 名门 code 透传(与 secret.set 同门)
        ("keychain:not-canonical", "invalid_secret_name"),
    ],
)
def test_save_rejects_non_keychain_token(home, bad_token, expected_code):
    """token 只收 keychain: 规范引用(明文经 secret.set 入钥匙串,另门)。"""
    response = _save(
        {
            "id": "myssia-firecrawl",
            "endpoint": "https://fc.example.org",
            "token": bad_token,
        }
    )
    assert response["error"]["code"] == expected_code
    assert response["error"]["path"] == "params.token"


def test_save_rejects_traversal_and_shape(home):
    """id 门与 bundled 族同源:穿越/大写/缺 id → invalid_params(path=params.id)。"""
    for bad_id in ("../escape", "a/b", "FOO", "x", 123, None):
        response = _save({"id": bad_id, "endpoint": "https://fc.example.org"})
        assert response["error"]["code"] == "invalid_params", f"{bad_id!r} 应被拒"
        assert response["error"]["path"] == "params.id"


# ---------------------------------------------------------------------------
# env 桥接:save 即时 / serve 启动 / 开发后门优先 / 钥匙串缺件降级
# ---------------------------------------------------------------------------


def test_save_bridges_endpoint_and_key_into_env_immediately(home):
    """save 即时桥接:端点直入 env URL;token 引用经钥匙串解析成值入 env KEY
    (引擎零改动的通道;同进程 run/doctor 即刻可见)。"""
    set_secret(FC_TOKEN_NAME, "fc-api-key-value")
    _save(
        {
            "id": "myssia-firecrawl",
            "endpoint": "https://fc.example.org",
            "token": f"keychain:{FC_TOKEN_NAME}",
        }
    )
    assert os.environ[FC_URL_ENV] == "https://fc.example.org"
    assert os.environ[FC_KEY_ENV] == "fc-api-key-value"


def test_save_token_without_keychain_entry_skips_key_bridge(home):
    """钥匙串缺件:端点仍桥接,键跳过(引擎按「未配键」降级,不炸 save)。"""
    _save(
        {
            "id": "myssia-firecrawl",
            "endpoint": "https://fc.example.org",
            "token": f"keychain:{FC_TOKEN_NAME}",
        }
    )
    assert os.environ[FC_URL_ENV] == "https://fc.example.org"
    assert FC_KEY_ENV not in os.environ


def test_explicit_env_dev_backdoor_wins_over_config(home, monkeypatch):
    """显式 env(开发后门)恒优先:启动桥接与 save 再桥接都不覆写。"""
    monkeypatch.setenv(FC_URL_ENV, "https://dev-explicit.example.org")
    # serve 启动桥接(配置已写)不覆写显式 env
    home.mkdir(parents=True, exist_ok=True)
    (home / entry.REMOTE_PLUGINS_CONFIG).write_text(
        json.dumps({"myssia-firecrawl": {"endpoint": "https://panel.example.org"}}),
        encoding="utf-8",
    )
    rpc({"id": 1, "method": "version", "params": {}})
    assert os.environ[FC_URL_ENV] == "https://dev-explicit.example.org"
    # save 再桥接同样不覆写(_BRIDGED_ENV 记账:该值非我方写值)
    _save({"id": "myssia-firecrawl", "endpoint": "https://panel2.example.org"})
    assert os.environ[FC_URL_ENV] == "https://dev-explicit.example.org"


def test_startup_bridge_reads_config_into_env(home):
    """serve 启动桥接:数据根配置(先写盘)→ env,同进程引擎/doctor 可见。"""
    set_secret(FC_TOKEN_NAME, "fc-key")
    home.mkdir(parents=True, exist_ok=True)
    (home / entry.REMOTE_PLUGINS_CONFIG).write_text(
        json.dumps(
            {
                "myssia-firecrawl": {
                    "endpoint": "https://panel.example.org",
                    "token": f"keychain:{FC_TOKEN_NAME}",
                },
                # 非引擎桥接件(rsshub 类):配置在,零 env 动作不炸
                "myssia-rsshub": {"endpoint": "https://rsshub.mine.example.org"},
            }
        ),
        encoding="utf-8",
    )
    rpc({"id": 1, "method": "version", "params": {}})
    assert os.environ[FC_URL_ENV] == "https://panel.example.org"
    assert os.environ[FC_KEY_ENV] == "fc-key"


def test_save_twice_updates_bridged_value(home):
    """面板改端点再存:我方上次桥接值可更新(未被显式 env 接管时)。"""
    _save({"id": "myssia-firecrawl", "endpoint": "https://first.example.org"})
    assert os.environ[FC_URL_ENV] == "https://first.example.org"
    _save({"id": "myssia-firecrawl", "endpoint": "https://second.example.org"})
    assert os.environ[FC_URL_ENV] == "https://second.example.org"


def test_no_config_no_env_bridge(home):
    """零配置启动:env 桥接零动作(缺省未配 = 降级链既有行为不变)。"""
    rpc({"id": 1, "method": "version", "params": {}})
    assert FC_URL_ENV not in os.environ and FC_KEY_ENV not in os.environ
