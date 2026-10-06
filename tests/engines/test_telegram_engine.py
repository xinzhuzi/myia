"""Tests for the Telegram Bot API window engine (10-06-telegram-telethon B1).

四态矩阵(照 reddit 判例;design D5 引擎面):

- **凭据缺失**:钥匙串无 ``myia/telegram/bot-token`` → ``credential_missing``
  显式空态(items=[]、last_skip_reason 置位、**零请求**、四步人话指引留痕);
- **配置错误**:chat_id/lookback_limit 类型错、源 URL 不符契约、payload 形状
  坏、pagination 配置 → 结构化 FetchError;
- **开启态**:MockTransport 往返(getUpdates 窗口拉取 → 确认请求)→ items
  形状:#tg- 锚 / title 截断 / content 全文 / published=ISO UTC / 群分拣 /
  媒体组聚合 / 无文本跳过 / 确认请求 offset=max+1;**凭据零外显**(任何
  异常消息不含 token 原文);
- **注册表**:ENGINE_REGISTRY 在册、AUTO_CHAIN 七层原样、auto_degrade 单级
  链、schema ENGINES/EngineName 词表收录。

零真实网络(MockTransport)、零真实钥匙串(InMemoryKeychainBackend)、
零 robots 拉取(授权 Bot API 通道,reddit 同口径 —— 测试钉死请求序列里无
/robots.txt)。
"""

from __future__ import annotations

import httpx
import pytest

from myssia import schema
from myssia.engines.fetch_base import FetchContext, FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.engines.telegram import (
    DEFAULT_LOOKBACK_LIMIT,
    TelegramEngine,
    mask_bot_url,
)
from myssia.schema import SourceConfig
from myssia.secrets import SECRET_SERVICE, InMemoryKeychainBackend

from conftest import make_client, make_context, make_source, run

SOURCE_URL = "https://api.telegram.org"
BOT_TOKEN = "8000000001:AA_test-token-do-not-leak"

CHAT_ID = -1001234567890
OTHER_CHAT_ID = -1009999999999


def updates_payload(*updates: dict) -> dict:
    return {"ok": True, "result": list(updates)}


def message_update(
    update_id: int,
    message_id: int,
    text: str | None,
    *,
    chat_id: int = CHAT_ID,
    caption: str | None = None,
    media_group_id: str | None = None,
    date: float = 1761000000.0,
    username: str | None = "alice",
) -> dict:
    message: dict = {
        "message_id": message_id,
        "date": date,
        "chat": {"id": chat_id, "type": "supergroup", "title": "mihomo_party_group"},
    }
    if text is not None:
        message["text"] = text
    if caption is not None:
        message["caption"] = caption
    if media_group_id is not None:
        message["media_group_id"] = media_group_id
    if username is not None:
        message["from"] = {"id": 42, "username": username}
    return {"update_id": update_id, "message": message}


def telegram_client(
    captured: list,
    *,
    window_response: httpx.Response | None = None,
    confirm_status: int = 200,
) -> httpx.AsyncClient:
    """单宿主 mock:api.telegram.org 应答窗口;确认请求(带 offset)可单独设码."""

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if request.url.host != "api.telegram.org" or request.url.path.endswith("/robots.txt"):
            pytest.fail(f"意外请求(非官方端点或 robots):{request.url}")
        if "offset=" in str(request.url):
            return httpx.Response(confirm_status, json=updates_payload())
        if window_response is not None:
            return window_response
        return httpx.Response(200, json=updates_payload())

    return make_client(handler)


def telegram_context(
    client: httpx.AsyncClient, *, with_token: bool = True
) -> FetchContext:
    context, _ = make_context(client)
    if with_token:
        backend = InMemoryKeychainBackend()
        backend.set_password(SECRET_SERVICE, "myia/telegram/bot-token", BOT_TOKEN)
        context.keychain_backend = backend
    return context


def make_telegram_source(**overrides: object) -> SourceConfig:
    data: dict = {
        "name": "telegram-mihomo_party_group",
        "engine": "telegram",
        "url": SOURCE_URL,
        "engine_options": {
            "telegram": {"chat_id": str(CHAT_ID), "bot_token": "keychain:myia/telegram/bot-token"}
        },
    }
    data.update(overrides)
    return SourceConfig.model_validate(data)


# ---------------------------------------------------------------------------
# 状态一:凭据缺失 = 显式空态(零请求)
# ---------------------------------------------------------------------------


def test_no_credentials_is_explicit_empty_state_zero_requests(caplog):
    """钥匙串无 token → credential_missing 空态:零请求 + 四步指引留痕."""
    captured: list = []
    client = telegram_client(captured)
    context = telegram_context(client, with_token=False)
    source = make_telegram_source()

    engine = TelegramEngine(source, context)
    with caplog.at_level("INFO", logger="myssia.engines.telegram"):
        items = run(engine.fetch())

    assert items == []
    assert engine.last_skip_reason == "credential_missing"
    assert captured == []  # 零请求
    assert "setprivacy" in caplog.text  # 隐私模式坑的人话指引
    assert "myia/telegram/bot-token" in caplog.text


def test_unresolvable_token_ref_is_empty_state_with_warning(caplog):
    """引用在而钥匙串未写 → 同空态 + warning 留痕(reddit 同口径)."""
    captured: list = []
    client = telegram_client(captured)
    context, _ = make_context(client)  # 无 keychain 后端注入 = 解析失败路径
    context.keychain_backend = InMemoryKeychainBackend()  # 空后端:键未写
    source = make_telegram_source()

    engine = TelegramEngine(source, context)
    with caplog.at_level("WARNING", logger="myssia.engines.telegram"):
        items = run(engine.fetch())

    assert items == []
    assert engine.last_skip_reason == "credential_missing"
    assert captured == []
    assert "解析失败" in caplog.text


# ---------------------------------------------------------------------------
# 状态二:配置错误 = 结构化 FetchError
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("options", "fragment"),
    [
        ({"chat_id": True}, "chat_id"),
        ({"chat_id": None}, "chat_id"),
        ({"lookback_limit": 0}, "lookback_limit"),
        ({"lookback_limit": 101}, "lookback_limit"),
        ({"lookback_limit": "50"}, "lookback_limit"),
    ],
)
def test_invalid_engine_options_structural_rejection(options, fragment):
    context, _ = make_context(make_client(lambda request: httpx.Response(500)))
    source = make_telegram_source(
        engine_options={"telegram": {"chat_id": str(CHAT_ID), **options}}
    )
    engine = TelegramEngine(source, context)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert fragment in str(excinfo.value)


def test_plaintext_bot_token_rejected_by_schema():
    """bot_token 明文/非引用:schema 凭据子串扫描(token)装载期即拒."""
    import pytest as _pytest

    with _pytest.raises(Exception) as excinfo:
        make_telegram_source(
            engine_options={
                "telegram": {"chat_id": str(CHAT_ID), "bot_token": 123}
            }
        )
    assert "凭据" in str(excinfo.value)


@pytest.mark.parametrize(
    "url",
    [
        "http://api.telegram.org",
        "https://t.me/s/durov",
        "https://api.telegram.org/bot123/getUpdates",
        "https://evil.example.com",
    ],
)
def test_source_url_contract_rejection(url):
    context, _ = make_context(make_client(lambda request: httpx.Response(500)))
    source = make_telegram_source(url=url)
    engine = TelegramEngine(source, context)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_telegram_source_url"


def test_pagination_unsupported():
    """pagination 配置结构化拒(schema 要求 template 带 {page},故配合法形态)."""
    context, _ = make_context(make_client(lambda request: httpx.Response(500)))
    source = make_telegram_source(
        url="https://api.telegram.org{page}",
        pagination={"mode": "template", "max_pages": 2},
    )
    engine = TelegramEngine(source, context)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "pagination_unsupported"


def test_malformed_payload_rejection():
    captured: list = []
    client = telegram_client(
        captured, window_response=httpx.Response(200, text="<html>not json</html>")
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "json_decode"


def test_payload_without_result_array_rejection():
    captured: list = []
    client = telegram_client(
        captured, window_response=httpx.Response(200, json={"ok": True})
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "telegram_payload_malformed"


def test_api_error_answer_structural_rejection():
    """"ok": false 应答(401 家族)→ 结构化错误,error_code 进错误类."""
    captured: list = []
    client = telegram_client(
        captured,
        window_response=httpx.Response(
            200, json={"ok": False, "error_code": 401, "description": "Unauthorized"}
        ),
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "telegram_api_401"


# ---------------------------------------------------------------------------
# 状态三:开启态 —— 窗口拉取 / 分拣 / 聚合 / 锚点 / 确认
# ---------------------------------------------------------------------------


def test_window_pull_builds_items_with_tg_anchor():
    captured: list = []
    client = telegram_client(
        captured,
        window_response=httpx.Response(
            200,
            json=updates_payload(
                message_update(11, 101, "mihomo 新版本发布了"),
                message_update(12, 102, "闲聊灌水" * 60),
            ),
        ),
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    items = run(engine.fetch())

    assert engine.last_skip_reason is None
    assert len(items) == 2
    first = items[0]
    assert first["url"] == f"{SOURCE_URL}#tg-{CHAT_ID}-101"
    assert first["title"] == "mihomo 新版本发布了"
    assert first["content"] == "mihomo 新版本发布了"
    assert first["published"] == "2025-10-20T22:40:00+00:00"
    assert first["author"] == "@alice"
    assert first["chat_title"] == "mihomo_party_group"
    # 超长文本:title 截断至 100,content 全文
    assert len(items[1]["title"]) == 100
    assert len(items[1]["content"]) == 240
    # 请求序列:窗口拉取 + 确认(offset=max+1);token 在 path,请求不落日志
    assert len(captured) == 2
    assert "/bot" in str(captured[0].url)
    assert "offset=13" in str(captured[1].url)


def test_chat_filtering_keeps_only_configured_chat():
    captured: list = []
    client = telegram_client(
        captured,
        window_response=httpx.Response(
            200,
            json=updates_payload(
                message_update(11, 101, "本群消息", chat_id=CHAT_ID),
                message_update(12, 201, "别群消息", chat_id=OTHER_CHAT_ID),
            ),
        ),
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    items = run(engine.fetch())

    assert len(items) == 1
    assert items[0]["url"] == f"{SOURCE_URL}#tg-{CHAT_ID}-101"


def test_textless_messages_skipped():
    """无 text 无 caption 的消息(贴纸/纯图)零可筛面 → 跳过不炸源."""
    captured: list = []
    client = telegram_client(
        captured,
        window_response=httpx.Response(
            200,
            json=updates_payload(
                message_update(11, 101, None, username=None),
                message_update(12, 102, "有文本"),
            ),
        ),
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    items = run(engine.fetch())

    assert [item["url"] for item in items] == [f"{SOURCE_URL}#tg-{CHAT_ID}-102"]


def test_media_group_aggregates_to_single_item():
    """同 media_group_id 相册聚一条:首条带 caption 的铸锚,后续并入."""
    captured: list = []
    client = telegram_client(
        captured,
        window_response=httpx.Response(
            200,
            json=updates_payload(
                message_update(11, 101, None, media_group_id="mg-1"),
                message_update(12, 102, "相册说明:免费节点截图", media_group_id="mg-1"),
                message_update(13, 103, None, media_group_id="mg-1"),
                message_update(14, 104, "独立消息"),
            ),
        ),
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    items = run(engine.fetch())

    assert [item["url"] for item in items] == [
        f"{SOURCE_URL}#tg-{CHAT_ID}-102",  # 组内首条有文本的(102)铸锚
        f"{SOURCE_URL}#tg-{CHAT_ID}-104",
    ]
    assert items[0]["media_group_id"] == "mg-1"
    assert items[0]["content"] == "相册说明:免费节点截图"


def test_edited_message_updates_consumed_with_same_anchor():
    """edited_message 更新照常消费(同 message_id = 同锚,编辑重投天然幂等)."""
    captured: list = []
    edited = {
        "update_id": 21,
        "edited_message": message_update(0, 301, "编辑后的文本")["message"],
    }
    client = telegram_client(
        captured, window_response=httpx.Response(200, json=updates_payload(edited))
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    items = run(engine.fetch())

    assert [item["url"] for item in items] == [f"{SOURCE_URL}#tg-{CHAT_ID}-301"]


def test_non_message_updates_ignored():
    """callback_query 等非消息更新跳过(无 message 面)."""
    captured: list = []
    client = telegram_client(
        captured,
        window_response=httpx.Response(
            200, json=updates_payload({"update_id": 31, "callback_query": {"id": "1"}})
        ),
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    items = run(engine.fetch())

    assert items == []
    assert len(captured) == 1  # 零确认请求(无消息可确认)


def test_http_401_structured_with_guidance_no_token_leak():
    captured: list = []
    client = telegram_client(
        captured, window_response=httpx.Response(401, text="Unauthorized")
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "http_401"
    assert BOT_TOKEN not in str(excinfo.value)
    assert "token" in str(excinfo.value)  # 指引在,凭据不在


def test_http_409_conflict_guidance():
    captured: list = []
    client = telegram_client(
        captured, window_response=httpx.Response(409, text="Conflict")
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "http_409"
    assert "serve" in str(excinfo.value)


def test_transport_error_sanitized_no_token_leak():
    """网络失败:FetchError 消息净化(httpx 异常 str 带完整 URL 含 token)."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(
            f"[Errno 8] Connection failed: {request.url}", request=request
        )

    client = make_client(handler)
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert BOT_TOKEN not in str(excinfo.value)
    assert "/bot***/" in str(excinfo.value)


def test_confirm_failure_is_warning_not_source_failure(caplog):
    """确认请求失败只告警:窗口 items 照常出仓(锚点去重兜底正确性)."""
    captured: list = []
    client = telegram_client(
        captured,
        window_response=httpx.Response(
            200, json=updates_payload(message_update(11, 101, "文本"))
        ),
        confirm_status=500,
    )
    context = telegram_context(client)
    engine = TelegramEngine(make_telegram_source(), context)

    with caplog.at_level("WARNING", logger="myssia.engines.telegram"):
        items = run(engine.fetch())

    assert len(items) == 1
    assert "确认失败" in caplog.text
    assert BOT_TOKEN not in caplog.text


def test_default_lookback_limit_is_hundred():
    """lookback_limit 缺省 = 100(getUpdates 硬顶;窗口宁可多拉靠锚点去重)."""
    captured: list = []
    client = telegram_client(captured)
    context = telegram_context(client)
    source = make_telegram_source(
        engine_options={"telegram": {"chat_id": str(CHAT_ID)}}
    )
    engine = TelegramEngine(source, context)

    run(engine.fetch())

    assert "limit=100" in str(captured[0].url)
    assert DEFAULT_LOOKBACK_LIMIT == 100


def test_default_token_key_is_keychain_reference():
    """bot_token 缺省 = keychain:myia/telegram/bot-token(示范件可省略该键)."""
    captured: list = []
    client = telegram_client(captured)
    context = telegram_context(client)  # 已写缺省键
    source = make_telegram_source(
        engine_options={"telegram": {"chat_id": str(CHAT_ID)}}
    )
    engine = TelegramEngine(source, context)

    items = run(engine.fetch())

    assert engine.last_skip_reason is None  # 缺省键解析成功 → 正常路径
    assert len(captured) >= 1


# ---------------------------------------------------------------------------
# 状态四:注册表 / schema 词表 / 凭据零外显工具
# ---------------------------------------------------------------------------


def test_registry_and_schema_vocabulary():
    assert "telegram" in ENGINE_REGISTRY
    assert resolve_engine("telegram") is TelegramEngine
    assert "telegram" not in AUTO_CHAIN  # 链外:七层降级链原样
    assert auto_degrade("telegram") == ["telegram"]  # 显式选择 = 单级链
    assert "telegram" in schema.ENGINES
    source = make_source(engine="telegram", url=SOURCE_URL)  # schema Literal 收录
    assert source.engine == "telegram"


def test_mask_bot_url():
    assert (
        mask_bot_url(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?limit=100")
        == "https://api.telegram.org/bot***/getUpdates?limit=100"
    )
    assert mask_bot_url("https://api.telegram.org/robots.txt") == "https://api.telegram.org/robots.txt"


def test_category_plugin_yaml_loads():
    """示范件 plugins/telegram-groups.yaml 可装载(schema 全节校验)."""
    import pathlib

    from myssia.schema import load_category_file

    path = pathlib.Path(__file__).resolve().parent.parent.parent / "plugins" / "telegram-groups.yaml"
    if not path.exists():  # pragma: no cover - 仓库布局守卫
        pytest.skip("plugins/telegram-groups.yaml 不在本测试布局内")
    config = load_category_file(path)
    assert config.id == "telegram-groups"
    assert [source.name for source in config.sources] == ["telegram-mihomo_party_group"]
    assert all(source.engine == "telegram" for source in config.sources)
