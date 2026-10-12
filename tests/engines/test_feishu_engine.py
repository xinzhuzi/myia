"""feishu 引擎单测(10-12-feishu-ingest-engine;telegram 引擎测试同款骨架).

MockTransport 注入零真实出网;凭据走 env(monkeypatch)与钥匙链规范名
兜底(InMemoryKeychainBackend)两路;异步经 conftest.run(asyncio.run).
"""

import httpx
import pytest

from conftest import make_client, make_context, make_source, run
from myssia.engines.feishu import FeishuEngine
from myssia.engines.fetch_base import FetchError
from myssia.secrets import InMemoryKeychainBackend

CHAT = "oc_f38a491eae5baf19898de28107087f05"


def feishu_source(**overrides: object):
    data: dict[str, object] = {
        "name": "feishu-ai-relay-group",
        "url": "https://open.feishu.cn",
        "engine": "feishu",
        "engine_options": {"feishu": {"chat_id": CHAT, "lookback_limit": 50}},
    }
    data.update(overrides)
    return make_source(**data)


def feishu_handler(*, token_code: int = 0, msg_code: int = 0, items: list | None = None,
                   token_missing: bool = False):
    """Mock handler:token mint + 群消息两端点;载荷可编程。"""
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/tenant_access_token/internal"):
            if token_missing:
                return httpx.Response(200, json={"code": 0, "data": {}})
            return httpx.Response(
                200 if token_code == 0 else 400,
                json=({"code": token_code, "msg": "app secret 错"}
                      if token_code else {"code": 0, "tenant_access_token": "t-1"}),
            )
        if request.url.path.endswith("/im/v1/messages"):
            assert request.headers.get("Authorization") == "Bearer t-1"
            assert request.url.params["container_id"] == CHAT
            assert request.url.params["container_id_type"] == "chat"
            return httpx.Response(
                200 if msg_code == 0 else 400,
                json=({"code": msg_code, "msg": "权限不足"}
                      if msg_code else {"code": 0, "data": {"items": items or []}}),
            )
        return httpx.Response(404, json={"code": 404, "msg": "not found"})
    return handler


def text_msg(mid: str, text: str) -> dict:
    import json
    return {
        "message_id": mid, "msg_type": "text",
        "body": {"content": json.dumps({"text": text})},
        "create_time": "1700000000000",
        "sender": {"id": "ou_sender1", "sender_type": "user"},
    }


# --------------------------------------------------------------------- 空态


def test_no_credentials_is_explicit_empty_state(caplog, monkeypatch):
    """凭据双路全缺(env 未设 + 钥匙链空)→ credential_missing 显式空态零请求."""
    monkeypatch.delenv("FEISHU_APP_ID", raising=False)
    monkeypatch.delenv("FEISHU_APP_SECRET", raising=False)
    requests: list[httpx.Request] = []
    client = make_client(lambda r: (requests.append(r), httpx.Response(500))[1])
    context, _ = make_context(client)
    context.keychain_backend = InMemoryKeychainBackend()
    engine = FeishuEngine(feishu_source(), context)
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "credential_missing"
    assert requests == []  # 零请求


# ------------------------------------------------------------------- 兜底链


def test_keychain_fallback_credentials(monkeypatch):
    """env 缺失 → 钥匙链规范名 keychain:myia/push/<ENV_KEY> 兜底(GUI 推送
    表单落点;backend=context.keychain_backend —— 生产 None=系统钥匙串)."""
    monkeypatch.delenv("FEISHU_APP_ID", raising=False)
    monkeypatch.delenv("FEISHU_APP_SECRET", raising=False)
    backend = InMemoryKeychainBackend()
    backend.set_password("myia", "myia/push/FEISHU_APP_ID", "cli_app")
    backend.set_password("myia", "myia/push/FEISHU_APP_SECRET", "sec")
    seen: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/tenant_access_token/internal"):
            import json
            seen.append(json.loads(request.content))
            return httpx.Response(200, json={"code": 0, "tenant_access_token": "t-1"})
        return httpx.Response(200, json={"code": 0, "data": {"items": []}})

    context, _ = make_context(make_client(handler))
    context.keychain_backend = backend
    items = run(FeishuEngine(feishu_source(), context).fetch())
    assert items == []
    assert seen == [{"app_id": "cli_app", "app_secret": "sec"}]


# ------------------------------------------------------------------ 出条目


def test_text_messages_become_items_with_fs_anchors(monkeypatch):
    """text 出条目(#fs-<chat>-<mid> 锚);非 text/空文本静默跳过."""
    monkeypatch.setenv("FEISHU_APP_ID", "cli_app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "sec")
    items_payload = [
        text_msg("om_a", "群消息一条:https://example.com/x"),
        {"message_id": "om_b", "msg_type": "image", "body": {"content": "{}"},
         "sender": {"id": "ou_1"}},
        text_msg("om_c", ""),
        text_msg("om_d", "第二条"),
        {"message_id": "om_e", "msg_type": "text", "body": {"content": "{\"text\": \"机器人回声\"}"},
         "sender": {"id": "cli_app", "sender_type": "app"}},
    ]
    context, _ = make_context(make_client(feishu_handler(items=items_payload)))
    engine = FeishuEngine(feishu_source(), context)
    items = run(engine.fetch())
    assert [item["url"] for item in items] == [
        f"https://open.feishu.cn#fs-{CHAT}-om_a",
        f"https://open.feishu.cn#fs-{CHAT}-om_d",
    ]
    assert items[0]["content"] == "群消息一条:https://example.com/x"
    assert items[0]["title"] == "群消息一条:https://example.com/x"
    assert items[0]["chat_id"] == CHAT


# ------------------------------------------------------------------ 错误面


def test_permission_denied_is_structured(monkeypatch):
    """权限 code(99991672)→ feishu_permission_denied(指引加权限+拉机器人)."""
    monkeypatch.setenv("FEISHU_APP_ID", "cli_app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "sec")
    context, _ = make_context(make_client(feishu_handler(msg_code=99991672)))
    with pytest.raises(FetchError) as exc:
        run(FeishuEngine(feishu_source(), context).fetch())
    assert exc.value.error_type == "feishu_permission_denied"
    assert "im:message" in str(exc.value)


def test_token_mint_failure_is_structured(monkeypatch):
    """token mint 被拒 → feishu_token_mint_failed(凭据坏不伪装空态)."""
    monkeypatch.setenv("FEISHU_APP_ID", "cli_app")
    monkeypatch.setenv("FEISHU_APP_SECRET", "bad")
    context, _ = make_context(make_client(feishu_handler(token_code=10003)))
    with pytest.raises(FetchError) as exc:
        run(FeishuEngine(feishu_source(), context).fetch())
    assert exc.value.error_type == "feishu_token_mint_failed"


# ------------------------------------------------------------------ options


def test_invalid_engine_options_structural_rejection():
    """chat_id 缺失/错型 → invalid_engine_options(零 I/O 结构化拒)."""
    context, _ = make_context(make_client(lambda r: httpx.Response(500)))
    for options in ({}, {"feishu": {"chat_id": ""}}, {"feishu": {"chat_id": 123}}):
        source = feishu_source(engine_options={"feishu": dict(options.get("feishu", {}))})
        with pytest.raises(FetchError) as exc:
            run(FeishuEngine(source, context).fetch())
        assert exc.value.error_type == "invalid_engine_options"
