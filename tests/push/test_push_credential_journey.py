"""推送凭据用户旅程(10-05-push-credential-journey)。

行为面:``env:`` 缺失 → 钥匙链规范名 ``myia/push/<ENV_KEY>`` 回退(设置→推送
表单存入位,GUI 桌面不读 shell 环境的接通路)+ 飞书 app_id/secret 自动 mint
tenant token(含缓存与失败结构化)。钥匙链一律 ``InMemoryKeychainBackend``
注入(:func:`myssia.secrets.set_backend`,零真实触碰);HTTP 一律
``httpx.MockTransport``,零外网(同 ``test_push_channels`` 约定)。
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
import pytest

from myssia import secrets as secrets_store
from myssia.push import CHANNELS, PushSendError, SendContext
from myssia.push.base import resolve_channel_credential
from myssia.push.feishu_card import (
    TENANT_TOKEN_CACHE,
    TOKEN_API_URL,
    FeishuCardChannel,
)
from myssia.schema import CredentialResolveError

_PUSH_ENV_KEYS = (
    "FEISHU_BOT_TOKEN",
    "FEISHU_CHAT_ID",
    "FEISHU_APP_ID",
    "FEISHU_APP_SECRET",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_CHAT_ID",
    "MYIA_WEBHOOK_URL",
)


@pytest.fixture(autouse=True)
def _in_memory_keychain(monkeypatch):
    """每用例独立 InMemory 钥匙链 + 推送 env 清零 + mint 缓存清零;用毕复位。"""
    secrets_store.set_backend(secrets_store.InMemoryKeychainBackend())
    for var in _PUSH_ENV_KEYS:
        monkeypatch.delenv(var, raising=False)
    TENANT_TOKEN_CACHE.clear()
    yield
    secrets_store.reset_backend()


def _immediate_context() -> SendContext:
    return SendContext(slot="am", date="2026-10-05", category=None, kind="immediate")


def _capture(request: httpx.Request) -> dict[str, Any]:
    return {
        "url": str(request.url),
        "auth": request.headers.get("authorization", ""),
        "body": json.loads(request.content.decode("utf-8")) if request.content else {},
    }


class TestResolveChannelCredential:
    """helper 三态:env 优先 / kc 回退 / 双缺指引;显式引用语义零变化。"""

    def test_env_hit_takes_priority(self, monkeypatch):
        secrets_store.set_secret("myia/push/FEISHU_BOT_TOKEN", "kc-value")
        monkeypatch.setenv("FEISHU_BOT_TOKEN", "env-value")
        assert (
            resolve_channel_credential(
                "env:FEISHU_BOT_TOKEN", env_key="FEISHU_BOT_TOKEN", label="测试位"
            )
            == "env-value"
        )

    def test_env_missing_falls_back_to_keychain(self):
        secrets_store.set_secret("myia/push/FEISHU_BOT_TOKEN", "kc-value")
        assert (
            resolve_channel_credential(
                "env:FEISHU_BOT_TOKEN", env_key="FEISHU_BOT_TOKEN", label="测试位"
            )
            == "kc-value"
        )

    def test_both_missing_guides_to_settings(self):
        with pytest.raises(CredentialResolveError) as excinfo:
            resolve_channel_credential(
                "env:FEISHU_BOT_TOKEN", env_key="FEISHU_BOT_TOKEN", label="测试位"
            )
        assert excinfo.value.code == "env_var_missing"
        assert "设置→推送" in str(excinfo.value)

    def test_explicit_keychain_ref_passes_through(self):
        secrets_store.set_secret("myia/stocks/my_chat", "oc_x")
        assert (
            resolve_channel_credential(
                "keychain:myia/stocks/my_chat", env_key="FEISHU_CHAT_ID", label="测试位"
            )
            == "oc_x"
        )

    def test_non_env_failure_reraised_unchanged(self):
        # 显式 keychain 引用缺项:secret_not_found 原样上抛,不被吞成 env_var_missing
        with pytest.raises(CredentialResolveError) as excinfo:
            resolve_channel_credential(
                "keychain:myia/stocks/absent", env_key="FEISHU_CHAT_ID", label="测试位"
            )
        assert excinfo.value.code == "secret_not_found"


class TestTelegramKeychainFallback:
    def test_token_and_chat_resolved_from_keychain(self, monkeypatch):
        secrets_store.set_secret("myia/push/TELEGRAM_BOT_TOKEN", "111:AAA")
        secrets_store.set_secret("myia/push/TELEGRAM_CHAT_ID", "424242")
        calls: list[dict[str, Any]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(_capture(request))
            return httpx.Response(200, json={"ok": True, "result": {"message_id": 1}})

        channel = CHANNELS["telegram"](
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler))
        )
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "424242")  # legacy target 缺省 env 引用
        asyncio.run(
            channel.send([{"title": "t", "url": "https://example.com/a"}], _immediate_context())
        )
        assert len(calls) == 1
        assert "bot111:AAA/sendMessage" in calls[0]["url"]
        assert calls[0]["body"]["chat_id"] == "424242"

    def test_both_missing_structured_error_with_guidance(self):
        channel = CHANNELS["telegram"]()
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "t"}], _immediate_context()))
        assert excinfo.value.code == "env_var_missing"
        assert "设置→推送" in str(excinfo.value)


class TestWebhookKeychainFallback:
    def test_endpoint_resolved_from_keychain(self):
        secrets_store.set_secret("myia/push/MYIA_WEBHOOK_URL", "http://127.0.0.1:9/hook")
        calls: list[dict[str, Any]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(_capture(request))
            return httpx.Response(200, json={"ok": True})

        channel = CHANNELS["webhook"](client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
        asyncio.run(
            channel.send([{"title": "t", "url": "https://example.com/a"}], _immediate_context())
        )
        assert len(calls) == 1
        assert calls[0]["url"].startswith("http://127.0.0.1:9/hook")


class TestFeishuAutoMint:
    """app_id/secret 在场自动 mint;手工 token 优先;mint 失败结构化。"""

    @staticmethod
    def _channel(handler) -> FeishuCardChannel:
        return FeishuCardChannel(
            target="env:FEISHU_CHAT_ID",
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

    def test_mint_then_send_with_process_cache(self, monkeypatch):
        secrets_store.set_secret("myia/push/FEISHU_APP_ID", "cli_app")
        secrets_store.set_secret("myia/push/FEISHU_APP_SECRET", "app_sec")
        monkeypatch.setenv("FEISHU_CHAT_ID", "oc_room")
        mints: list[dict[str, Any]] = []
        posts: list[dict[str, Any]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            captured = _capture(request)
            if captured["url"] == TOKEN_API_URL:
                mints.append(captured["body"])
                return httpx.Response(
                    200, json={"code": 0, "tenant_access_token": "t-abc", "expire": 7200}
                )
            posts.append(captured)
            return httpx.Response(200, json={"code": 0, "data": {"message_id": "om_1"}})

        channel = self._channel(handler)
        asyncio.run(channel.send([{"title": "t", "url": "https://example.com/a"}], _immediate_context()))
        asyncio.run(channel.send([{"title": "t2", "url": "https://example.com/b"}], _immediate_context()))
        assert len(mints) == 1  # 第二次发送走进程缓存,不再 mint
        assert mints[0] == {"app_id": "cli_app", "app_secret": "app_sec"}
        assert len(posts) == 2
        assert all(post["auth"] == "Bearer t-abc" for post in posts)

    def test_manual_bot_token_preferred_over_mint(self, monkeypatch):
        secrets_store.set_secret("myia/push/FEISHU_BOT_TOKEN", "t-manual")
        secrets_store.set_secret("myia/push/FEISHU_APP_ID", "cli_app")
        secrets_store.set_secret("myia/push/FEISHU_APP_SECRET", "app_sec")
        monkeypatch.setenv("FEISHU_CHAT_ID", "oc_room")
        mints: list[dict[str, Any]] = []
        posts: list[dict[str, Any]] = []

        def handler(request: httpx.Request) -> httpx.Response:
            captured = _capture(request)
            if captured["url"] == TOKEN_API_URL:
                mints.append(captured["body"])
                return httpx.Response(
                    200, json={"code": 0, "tenant_access_token": "t-minted", "expire": 7200}
                )
            posts.append(captured)
            return httpx.Response(200, json={"code": 0, "data": {"message_id": "om_1"}})

        asyncio.run(self._channel(handler).send([{"title": "t"}], _immediate_context()))
        assert mints == []  # 手工 token 在场:直用,mint 路零触发
        assert posts and posts[0]["auth"] == "Bearer t-manual"

    def test_mint_api_rejection_structured(self, monkeypatch):
        secrets_store.set_secret("myia/push/FEISHU_APP_ID", "cli_app")
        secrets_store.set_secret("myia/push/FEISHU_APP_SECRET", "wrong_sec")
        monkeypatch.setenv("FEISHU_CHAT_ID", "oc_room")

        def handler(request: httpx.Request) -> httpx.Response:
            if str(request.url) == TOKEN_API_URL:
                return httpx.Response(200, json={"code": 99991663, "msg": "app secret invalid"})
            raise AssertionError("mint 失败不应发出消息请求")

        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(self._channel(handler).send([{"title": "t"}], _immediate_context()))
        assert excinfo.value.code == "feishu_token_mint_failed"
        assert "app_id/app_secret" in str(excinfo.value)

    def test_all_credential_slots_missing_guides_to_settings(self, monkeypatch):
        monkeypatch.setenv("FEISHU_CHAT_ID", "oc_room")
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(self._channel(lambda request: httpx.Response(500)).send([{"title": "t"}], _immediate_context()))
        assert excinfo.value.code == "env_var_missing"
        assert "设置→推送" in str(excinfo.value)
