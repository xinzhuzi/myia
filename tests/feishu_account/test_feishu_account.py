"""feishu_account 领域层单测(10-11-platform-account-config)。

No pytest-asyncio in dev deps: async calls run through ``asyncio.run``
(test_bark 同款惯例);keychain 用 InMemoryKeychainBackend;HTTP 用
httpx.MockTransport 注入,零真实出网。
"""

import asyncio
import json

import httpx
import pytest

from myssia import feishu_account as fa
from myssia.secrets import InMemoryKeychainBackend, get_secret, reset_backend, set_backend


@pytest.fixture(autouse=True)
def _keychain():
    set_backend(InMemoryKeychainBackend())
    yield
    reset_backend()


def _run(coro):
    return asyncio.run(coro)


def _oauth_response(payload: dict, status: int = 200) -> httpx.Response:
    return httpx.Response(status, json=payload, request=httpx.Request("POST", "https://open.feishu.cn/x"))


# ---------------------------------------------------------------------------
# 键规约与 URL 构造
# ---------------------------------------------------------------------------


def test_account_key_rules():
    assert fa.validate_account_key("feishu-alt1") == "feishu-alt1"
    assert fa.validate_account_key("feishu-zh_2-x") == "feishu-zh_2-x"
    for bad in ["bad", "feishu-", "feishu-大写", "feishu-../escape", "telegram-alt1", ""]:
        with pytest.raises(fa.FeishuAccountError) as exc:
            fa.validate_account_key(bad)
        assert exc.value.code == "account_key_invalid"


def test_authorize_url_pure_function():
    url = fa.authorize_url("cli_a", "http://127.0.0.1:8731/callback", "st8")
    assert url.startswith("https://accounts.feishu.cn/open-apis/authen/v1/authorize?")
    assert "app_id=cli_a" in url
    assert "state=st8" in url
    # redirect_uri 被整体编码(冒号/斜杠不裸奔)
    assert "redirect_uri=http%3A%2F%2F127.0.0.1%3A8731%2Fcallback" in url


# ---------------------------------------------------------------------------
# 换 token / 刷新(应答解析同族)
# ---------------------------------------------------------------------------


def test_exchange_code_ok():
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["grant_type"] == "authorization_code"
        assert body["code"] == "abc"
        assert body["app_id"] == "cli_a"
        return _oauth_response(
            {"code": 0, "data": {"access_token": "u-1", "refresh_token": "r-1"}}
        )

    tokens = _run(
        fa.exchange_code("cli_a", "sec", "abc", "http://127.0.0.1:8731/callback",
                         transport=httpx.MockTransport(handler))
    )
    assert tokens == {"access_token": "u-1", "refresh_token": "r-1"}


def test_exchange_code_business_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return _oauth_response({"code": 99991663, "msg": "code 已使用"})

    with pytest.raises(fa.FeishuAccountError) as exc:
        _run(
            fa.exchange_code("cli_a", "sec", "abc", "http://x/callback",
                             transport=httpx.MockTransport(handler))
        )
    assert exc.value.code == "feishu_oauth_exchange_failed"
    assert "code 已使用" in str(exc.value)


def test_exchange_code_http_error_and_missing_token():
    def handler_500(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="boom", request=httpx.Request("POST", "https://x"))

    with pytest.raises(fa.FeishuAccountError) as exc:
        _run(fa.exchange_code("a", "s", "c", "http://x/callback",
                              transport=httpx.MockTransport(handler_500)))
    assert exc.value.code == "feishu_oauth_exchange_failed"

    def handler_missing(request: httpx.Request) -> httpx.Response:
        return _oauth_response({"code": 0, "data": {"access_token": "u-1"}})

    with pytest.raises(fa.FeishuAccountError) as exc:
        _run(fa.exchange_code("a", "s", "c", "http://x/callback",
                              transport=httpx.MockTransport(handler_missing)))
    assert exc.value.code == "feishu_oauth_exchange_failed"


def test_refresh_tokens_ok():
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        assert body["grant_type"] == "refresh_token"
        assert body["refresh_token"] == "r-old"
        return _oauth_response(
            {"code": 0, "data": {"access_token": "u-2", "refresh_token": "r-2"}}
        )

    tokens = _run(fa.refresh_tokens("cli_a", "sec", "r-old",
                                    transport=httpx.MockTransport(handler)))
    assert tokens == {"access_token": "u-2", "refresh_token": "r-2"}


# ---------------------------------------------------------------------------
# 存储:marker / 账号枚举 / 删除
# ---------------------------------------------------------------------------


def test_marker_roundtrip_and_corruption(tmp_path):
    directory = tmp_path / "feishu-accounts" / "feishu-a"
    payload = fa.write_login_marker(directory, label="工作号", refresh_ok=True)
    assert payload["label"] == "工作号"
    assert payload["refresh_ok"] is True
    assert payload["authorized_at"]
    marker = fa.read_login_marker(directory)
    assert marker is not None and marker["label"] == "工作号"
    # 复写保留 authorized_at 与 label(探针只动状态位)
    fa.write_login_marker(directory, label="", refresh_ok=False)
    marker = fa.read_login_marker(directory)
    assert marker is not None
    assert marker["label"] == "工作号" and marker["authorized_at"] == payload["authorized_at"]
    assert marker["refresh_ok"] is False
    # 坏标记宽容回 None
    (directory / fa.LOGIN_MARKER_NAME).write_text("::: 不是 json", encoding="utf-8")
    assert fa.read_login_marker(directory) is None


def test_list_accounts_sorted_and_skips_bad_dirs(tmp_path):
    root = tmp_path / "feishu-accounts"
    (root / "feishu-b").mkdir(parents=True)
    (root / "feishu-a").mkdir(parents=True)
    (root / "not-a-key").mkdir(parents=True)
    fa.write_login_marker(root / "feishu-a", label="A", refresh_ok=None)
    accounts = fa.list_accounts(tmp_path)
    assert [a["account"] for a in accounts] == ["feishu-a", "feishu-b"]
    assert accounts[0]["label"] == "A"
    assert accounts[1]["label"] is None  # 无标记目录也入列,标记位留 None
    assert fa.list_accounts(tmp_path / "无此目录") == []


def test_store_and_delete_account(tmp_path):
    fa.store_account_tokens("feishu-a", "u-1", "r-1")
    assert get_secret("myia/feishu-a/user_access_token") == "u-1"
    assert get_secret("myia/feishu-a/refresh_token") == "r-1"
    directory = fa.account_dir(tmp_path, "feishu-a")
    directory.mkdir(parents=True)
    result = fa.delete_account(tmp_path, "feishu-a")
    assert result == {"deleted": True, "account": "feishu-a"}
    assert not directory.exists()
    with pytest.raises(Exception):
        get_secret("myia/feishu-a/user_access_token")
    with pytest.raises(Exception):
        get_secret("myia/feishu-a/refresh_token")


def test_delete_tolerates_dir_without_tokens(tmp_path):
    directory = fa.account_dir(tmp_path, "feishu-b")
    directory.mkdir(parents=True)
    result = fa.delete_account(tmp_path, "feishu-b")  # 未授权成功 = 只有目录
    assert result["deleted"] is True


# ---------------------------------------------------------------------------
# 探针闭环(refresh 可成功 = 绿;失败 = 灰;无 token = 结构化错)
# ---------------------------------------------------------------------------


def _seed_account(tmp_path, key="feishu-a", refresh="r-old"):
    fa.store_account_tokens(key, "u-old", refresh)
    fa.write_login_marker(fa.account_dir(tmp_path, key), label="工作号", refresh_ok=None)


def test_probe_success_rewrites_tokens_and_marker(tmp_path):
    _seed_account(tmp_path)

    def handler(request: httpx.Request) -> httpx.Response:
        return _oauth_response(
            {"code": 0, "data": {"access_token": "u-new", "refresh_token": "r-new"}}
        )

    result = _run(
        fa.probe_account(tmp_path, "feishu-a", "cli_a", "sec",
                         transport=httpx.MockTransport(handler))
    )
    assert result["refresh_ok"] is True
    assert get_secret("myia/feishu-a/user_access_token") == "u-new"  # 续期回写
    assert get_secret("myia/feishu-a/refresh_token") == "r-new"
    marker = fa.read_login_marker(fa.account_dir(tmp_path, "feishu-a"))
    assert marker is not None
    assert marker["refresh_ok"] is True and marker["label"] == "工作号"


def test_probe_failure_sets_grey_and_raises(tmp_path):
    _seed_account(tmp_path)

    def handler(request: httpx.Request) -> httpx.Response:
        return _oauth_response({"code": 99991668, "msg": "refresh_token 已失效"})

    with pytest.raises(fa.FeishuAccountError) as exc:
        _run(fa.probe_account(tmp_path, "feishu-a", "cli_a", "sec",
                              transport=httpx.MockTransport(handler)))
    assert exc.value.code == "feishu_refresh_failed"
    marker = fa.read_login_marker(fa.account_dir(tmp_path, "feishu-a"))
    assert marker is not None and marker["refresh_ok"] is False


def test_probe_without_refresh_token_is_structured(tmp_path):
    directory = fa.account_dir(tmp_path, "feishu-c")
    directory.mkdir(parents=True)
    with pytest.raises(fa.FeishuAccountError) as exc:
        _run(fa.probe_account(tmp_path, "feishu-c", "cli_a", "sec"))
    assert exc.value.code == "feishu_refresh_token_missing"
    marker = fa.read_login_marker(directory)
    assert marker is not None and marker["refresh_ok"] is False
