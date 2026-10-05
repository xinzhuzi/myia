"""Tests for 10-05-push-bark — bark 适配器(iOS 即时推送,零依赖小件)。

覆盖(prd 验收 1 的六用例):one-shot POST 形态(URL 拼 endpoint/key +
JSON 体 title/body/group=MYIA)、404 坏 key 结构化错误(状态码透传)、
超时透传、明文 target 拒、自建 endpoint 拼接、配 targets 即拒(schema 面);
另附 schema 两用例(literal 增员且不进 CHANNEL_PLATFORMS;bark_endpoint
http/https 门)+ 管线下传接线(_build_channel 把 bark_endpoint 送达构造)。

No pytest-asyncio in dev deps: async calls run through ``asyncio.run``
(同 test_messaging_ntfy.py 约定)。All network I/O goes through
``httpx.MockTransport``.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import httpx
import pytest

from myssia.push import BarkChannel, SendContext
from myssia.push.base import PushSendError
from myssia.schema import LoadError, load_category

CONTEXT = SendContext(slot="am", date="2026-10-05", category="羊毛", kind="digest")


def _capture(request: httpx.Request) -> dict:
    return {
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": json.loads(request.content.decode("utf-8")),
    }


def _mock(calls: list[dict], response: httpx.Response | None = None) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(_capture(request))
        return response or httpx.Response(200, json={"code": 200, "message": "success"})

    return httpx.MockTransport(handler)


def _channel(calls: list[dict], *, response: httpx.Response | None = None, **kwargs: Any) -> BarkChannel:
    kwargs.setdefault("target", "env:MYIA_TEST_BARK_KEY")
    client = kwargs.pop("client", None) or httpx.AsyncClient(transport=_mock(calls, response=response))
    return BarkChannel(client=client, **kwargs)


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


@pytest.fixture()
def key_env(monkeypatch):
    monkeypatch.setenv("MYIA_TEST_BARK_KEY", "devkey_abc123")


# ---------------------------------------------------------------------------
# 六用例:one-shot POST 形态 + 错误面 + 寻址门(prd 验收 1)
# ---------------------------------------------------------------------------


class TestBarkSend:
    def test_success_posts_endpoint_slash_key_with_myia_group(self, key_env):
        """①200 成功:URL 拼 endpoint/key;JSON 体 title/body/group=MYIA。"""
        calls: list[dict] = []
        channel = _channel(calls)

        _run(channel.send([{"title": "羊毛", "url": "https://x/1"}], CONTEXT))

        assert calls[0]["url"] == "https://api.day.app/devkey_abc123"
        body = calls[0]["body"]
        assert body["group"] == "MYIA"  # iOS 通知分组聚合,信息流不刷屏(PRD 定案)
        assert "羊毛" in body["body"] and "https://x/1" in body["body"]
        assert body["title"]  # card_title 跨通道一致(锁屏标题行)
        assert calls[0]["headers"]["content-type"] == "application/json"

    def test_404_bad_key_is_structured_error_with_status(self, key_env):
        """②404(坏 key)→ bark_api_error,文案含 HTTP 404(死信分类可命中)。"""
        calls: list[dict] = []
        channel = _channel(
            calls, response=httpx.Response(404, text='{"code":404,"message":"device key not found"}')
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "bark_api_error"
        assert "HTTP 404" in str(excinfo.value)
        assert "device key not found" in str(excinfo.value)  # 原厂 message 透传

    def test_timeout_is_structured_http_error(self, key_env):
        """③超时 → http_error 透传(bark 无发送期重试环,PRD:重试走账本)。"""
        calls: list[dict] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(_capture(request))
            raise httpx.TimeoutException("timed out")

        channel = BarkChannel(
            target="env:MYIA_TEST_BARK_KEY",
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "http_error"
        assert "TimeoutException" in str(excinfo.value)
        assert len(calls) == 1  # 零重试:一次即透传

    def test_plaintext_target_refused_before_any_request(self, key_env):
        """④明文 device key 拒(invalid_credential_ref),零请求发出。"""
        calls: list[dict] = []
        channel = _channel(calls, target="devkey_plaintext")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "invalid_credential_ref"
        assert "devkey_plaintext" not in str(excinfo.value)  # 错误只带语义,不带值
        assert calls == []  # 铁律:凭据问题绝不触网

    def test_custom_endpoint_joins_key(self, key_env):
        """⑤自建 endpoint(http 主机:端口,尾斜杠容忍)拼 {endpoint}/{key}。"""
        calls: list[dict] = []
        channel = _channel(calls, bark_endpoint="http://192.168.1.10:8080/")

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert calls[0]["url"] == "http://192.168.1.10:8080/devkey_abc123"

    def test_targets_rejected_at_schema(self):
        """⑥bark 配 targets 即拒(无目录语义,同 webhook;fail-fast 于配置)。"""
        with pytest.raises(LoadError) as excinfo:
            load_category(_data(push=[{
                "channel": "bark",
                "target": "env:BARK_DEVICE_KEY",
                "targets": ["bark:phone"],
            }]))
        assert any(d.error_type == "targeting_not_supported" for d in excinfo.value.errors)


# ---------------------------------------------------------------------------
# schema 两用例:literal 增员;bark_endpoint 校验(http/https scheme 门)
# ---------------------------------------------------------------------------


def _data(**overrides: Any) -> dict:
    base = {
        "id": "demo",
        "name": "Demo",
        "schedule": "0 9 * * *",
        "sources": [{"name": "example", "url": "https://example.com/list?page={page}"}],
    }
    base.update(overrides)
    return base


class TestBarkSchema:
    def test_bark_in_push_channels_vocabulary_but_not_targeting(self):
        """literal 增员:bark ∈ PUSH_CHANNELS;∉ CHANNEL_PLATFORMS(同 webhook)。"""
        from myssia.schema import CHANNEL_PLATFORMS, PUSH_CHANNELS

        assert "bark" in PUSH_CHANNELS
        assert "bark" not in CHANNEL_PLATFORMS  # 配 targets 即拒的表驱动来源

    @pytest.mark.parametrize(
        "bad",
        [
            "ftp://host:8080",  # 花样新 scheme(SSRF 面,红线)
            "192.168.1.10:8080",  # 缺 scheme
            "http://",  # 缺主机
        ],
    )
    def test_bark_endpoint_scheme_gate(self, bad):
        """bark_endpoint 必须 http(s) 形态;花样新 scheme 加载期即拒。"""
        with pytest.raises(LoadError) as excinfo:
            load_category(_data(push=[{
                "channel": "bark",
                "target": "env:BARK_DEVICE_KEY",
                "bark_endpoint": bad,
            }]))
        assert any(d.error_type == "invalid_url" for d in excinfo.value.errors)

    def test_bark_endpoint_on_wrong_channel_rejected(self):
        """bark_endpoint 仅 bark 通道可配(别处出现 = unexpected_platform_field)。"""
        with pytest.raises(LoadError) as excinfo:
            load_category(_data(push=[{
                "channel": "ntfy",
                "target": "env:NTFY_TARGET",
                "bark_endpoint": "http://192.168.1.10:8080",
            }]))
        assert any(
            d.error_type == "unexpected_platform_field" for d in excinfo.value.errors
        )

    def test_bark_minimal_entry_loads_and_custom_endpoint_lands(self):
        """最小条目(留空端点=官方服务)照常加载;自建端点原样落位。"""
        cfg = load_category(_data(push=[
            {"channel": "bark", "target": "env:BARK_DEVICE_KEY"},
            {"channel": "bark", "target": "env:BARK_DEVICE_KEY", "bark_endpoint": "http://192.168.1.10:8080"},
        ]))
        bare, custom = cfg.push
        assert (bare.channel, bare.bark_endpoint) == ("bark", None)  # 留空=官方(缺省在 push 层)
        assert custom.bark_endpoint == "http://192.168.1.10:8080"


# ---------------------------------------------------------------------------
# 管线下传接线:schema 可选字段经真实 _build_channel 到达通道构造参数
# ---------------------------------------------------------------------------


def test_build_channel_wires_bark_endpoint(tmp_path, monkeypatch):
    """bark_endpoint 经 _W2_CHANNEL_FIELD_KWARGS 下传(先例:W2 凭据字段接线)。"""
    from myssia.pipeline import Pipeline
    from myssia.store import SQLiteStore

    cfg = load_category(_data(push=[{
        "channel": "bark",
        "target": "env:BARK_DEVICE_KEY",
        "bark_endpoint": "http://192.168.1.10:8080",
    }]))
    pipeline = Pipeline(
        cfg,
        db_path=tmp_path / "p.db",
        store=SQLiteStore(tmp_path / "p.db"),
        client=httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(404, text=""))
        ),
    )
    try:
        channel = pipeline._build_channel(pipeline.config.push[0])
        assert isinstance(channel, BarkChannel)
        assert channel._endpoint == "http://192.168.1.10:8080"
        assert channel._target == "env:BARK_DEVICE_KEY"
    finally:
        pipeline.close()
