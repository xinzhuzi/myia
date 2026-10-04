"""飞书/TG 发送护栏测试 — 10-05-push-reliability-batch R2(缺口②③)。

覆盖(蓝本锚:Hermes ``plugins/platforms/feishu/adapter.py:3925-3970``
``_feishu_send_with_retry`` + ``MAX_MESSAGE_LENGTH=8000``/``_SPLIT_THRESHOLD=
4000``;``tools/send_message_senders.py:70-96`` ``_telegram_retry_delay``,
NousResearch/Hermes-Agent,MIT——本文件测 MYIA 侧重写,不测上游):

- 飞书瞬态重试:网络错 / 5xx 非 JSON / 限流类业务码 → 指数退避
  ``2**attempt``,总尝试 ``SEND_ATTEMPTS=3``;配置类码(99991663)立即
  失败零重试;
- 飞书话题锚失效降级:reply 端点应答 230011/231003 → 丢弃话题锚改投
  create 新消息;多卡降级只做一次(后续卡直发 create);瞬态错不触发
  降级(退避后仍走 reply 端点);降级后的失败如实抛出不循环;
- 卡片长度护栏:估算载荷(序列化 JSON 字符数)超 ``CARD_SPLIT_THRESHOLD``
  → 拆多卡;条目/行完整性(单条目独占一卡不截断);footer 只挂末卡;
- telegram sendMessage 包退避:429 携 ``parameters.retry_after`` 优先;
  超时永不重试;5xx/传输错指数退避 ≤3 次;永久码(400)单次失败。

全部 ``httpx.MockTransport`` 逐错应答序列断言,零外网零真发;退避 sleeper
注入 ``SleepRecorder``(零真实等待);凭据一律构造注入(token="t")+
``context.target`` 显式寻址,零钥匙串触碰。
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import Any

import httpx
import pytest

from myssia.push import FeishuCardChannel, PushSendError, SendContext, TelegramChannel
from myssia.push.feishu_card import (
    API_URL,
    CARD_SPLIT_THRESHOLD,
)
from myssia.push.targets import ChannelTarget


class SleepRecorder:
    """退避 sleeper 替身:记录每次等待时长,绝不真等。"""

    def __init__(self) -> None:
        self.sleeps: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.sleeps.append(seconds)


def _feishu_ok() -> httpx.Response:
    return httpx.Response(200, json={"code": 0, "msg": "success", "data": {}})


def _feishu_code(code: int, msg: str = "err") -> httpx.Response:
    return httpx.Response(200, json={"code": code, "msg": msg})


def _tg_ok() -> httpx.Response:
    return httpx.Response(200, json={"ok": True, "result": {"message_id": 1}})


def _tg_error(error_code: int, description: str, **extra: Any) -> httpx.Response:
    return httpx.Response(200, json={"ok": False, "error_code": error_code,
                                     "description": description, **extra})


def _sequence_client(
    calls: list[dict],
    *,
    responses: list[httpx.Response] | None = None,
    raises: list[Exception | None] | None = None,
    ok: httpx.Response | None = None,
) -> httpx.AsyncClient:
    """逐调用应答序列:第 i 调用先看 ``raises[i]``(传输层异常)再看
    ``responses[i]``;两列表越界沿用末元素/缺省成功应答。"""

    index = {"i": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        i = index["i"]
        index["i"] += 1
        calls.append({"url": str(request.url), "body": json.loads(request.content)})
        if raises is not None and i < len(raises) and raises[i] is not None:
            raise raises[i]
        if responses is not None:
            return responses[min(i, len(responses) - 1)]
        return ok or _feishu_ok()

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def _ctx(target: ChannelTarget | None = None) -> SendContext:
    return replace(
        SendContext(slot="am", date="2026-10-05", category="羊毛", kind="digest"),
        target=target,
    )


def _feishu_target(
    *, thread_id: str | None = None, chat_id: str = "oc_g"
) -> ChannelTarget:
    return ChannelTarget(platform="feishu", chat_id=chat_id, thread_id=thread_id)


def _feishu_channel(calls: list[dict], sleeper: SleepRecorder, **kwargs: Any):
    kwargs.setdefault("token", "t")
    return FeishuCardChannel(
        client=_sequence_client(calls, **kwargs.pop("client_kwargs", {})),
        sleep=sleeper,
        **kwargs,
    )


def _tg_channel(calls: list[dict], sleeper: SleepRecorder, **kwargs: Any):
    kwargs.setdefault("token", "t")
    return TelegramChannel(
        client=_sequence_client(calls, ok=_tg_ok(), **kwargs.pop("client_kwargs", {})),
        sleep=sleeper,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# 飞书:瞬态重试(逐错序列)
# ---------------------------------------------------------------------------


class TestFeishuTransientRetry:
    def test_network_error_retries_then_succeeds(self):
        """传输错(连接拒绝)→ 退避 1s 重试 → 成功;共 2 次调用。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={"raises": [httpx.ConnectError("connection refused"), None]},
        )
        asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert len(calls) == 2
        assert sleeper.sleeps == [1.0]  # 2**0

    def test_gateway_503_non_json_retries_then_succeeds(self):
        """5xx 非 JSON 应答(invalid_response 携结构化状态)→ 瞬态退避。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [httpx.Response(503, text="Bad Gateway"), _feishu_ok()]},
        )
        asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert len(calls) == 2
        assert sleeper.sleeps == [1.0]

    def test_rate_limit_api_code_retries_then_succeeds(self):
        """飞书限流类业务码 99991400(too many request)→ 退避重试。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [_feishu_code(99991400, "too many request"), _feishu_ok()]},
        )
        asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert len(calls) == 2
        assert sleeper.sleeps == [1.0]

    def test_transient_sequence_backoff_is_exponential(self):
        """连败两次(503×2)第三次成功:退避序列 [1.0, 2.0](2**attempt)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={
                "responses": [
                    httpx.Response(503, text="Bad Gateway"),
                    httpx.Response(503, text="Bad Gateway"),
                    _feishu_ok(),
                ]
            },
        )
        asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert len(calls) == 3
        assert sleeper.sleeps == [1.0, 2.0]

    def test_transient_exhaustion_raises_after_send_attempts(self):
        """持续 503:总尝试 SEND_ATTEMPTS=3 后如实抛错(1 首发加 2 重试)。"""
        from myssia.push.feishu_card import SEND_ATTEMPTS

        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls, sleeper, client_kwargs={"responses": [httpx.Response(503, text="x")]}
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert excinfo.value.code == "invalid_response"
        assert len(calls) == SEND_ATTEMPTS
        assert sleeper.sleeps == [1.0, 2.0]

    def test_permanent_api_error_fails_without_retry(self):
        """配置类码(99991663 token 失效)非瞬态:单次失败,零退避。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [_feishu_code(99991663, "invalid access token")]},
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert excinfo.value.code == "feishu_api_error"
        assert len(calls) == 1
        assert sleeper.sleeps == []

    def test_client_error_400_never_retries(self):
        """HTTP 400(JSON 体)非瞬态状态:单次失败。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [httpx.Response(400, json={"code": 400, "msg": "bad"})]},
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert excinfo.value.code == "feishu_api_error"
        assert len(calls) == 1
        assert sleeper.sleeps == []


# ---------------------------------------------------------------------------
# 飞书:话题锚失效降级(蓝本 _FEISHU_REPLY_FALLBACK_CODES)
# ---------------------------------------------------------------------------


class TestFeishuReplyFallback:
    def test_thread_anchor_withdrawn_downgrades_to_create(self):
        """reply 端点 230011(锚被撤回)→ 丢锚改投 create 新消息(零退避)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [_feishu_code(230011, "reply message not found"), _feishu_ok()]},
        )
        asyncio.run(
            channel.send([{"title": "条目"}], _ctx(_feishu_target(thread_id="om_root1")))
        )
        assert len(calls) == 2
        assert calls[0]["url"] == f"{API_URL}/om_root1/reply"
        assert calls[1]["url"].split("?")[0] == API_URL  # create 端点
        assert "receive_id_type=chat_id" in calls[1]["url"]
        assert calls[1]["body"]["receive_id"] == "oc_g"  # 降级目标 = 群
        assert sleeper.sleeps == []  # 降级不是瞬态重试,无退避

    def test_second_fallback_code_after_downgrade_fails_honestly(self):
        """降级后的 create 再报 fallback 类码:不再降级、非瞬态,如实抛。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={
                "responses": [_feishu_code(230011, "x"), _feishu_code(231003, "y")]
            },
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(
                channel.send([{"title": "条目"}], _ctx(_feishu_target(thread_id="om_root1")))
            )
        assert excinfo.value.code == "feishu_api_error"
        assert len(calls) == 2
        assert sleeper.sleeps == []

    def test_thread_transient_error_keeps_reply_endpoint(self):
        """话题路径瞬态错(503)不触发降级:退避后仍走 reply 端点。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [httpx.Response(503, text="x"), _feishu_ok()]},
        )
        asyncio.run(
            channel.send([{"title": "条目"}], _ctx(_feishu_target(thread_id="om_root2")))
        )
        assert [call["url"] for call in calls] == [
            f"{API_URL}/om_root2/reply",
            f"{API_URL}/om_root2/reply",
        ]
        assert sleeper.sleeps == [1.0]

    def test_multi_card_downgrades_only_once(self):
        """多卡 + 锚失效:仅首卡探死锚,后续卡直发 create(免连环开话题)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        items = [
            {"title": f"条目{i} " + "x" * 700, "url": f"https://e/{i}"} for i in range(8)
        ]
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={
                "responses": [_feishu_code(230011, "x"), _feishu_ok(), _feishu_ok()]
            },
        )
        asyncio.run(channel.send(items, _ctx(_feishu_target(thread_id="om_root3"))))
        assert len(calls) == 3  # 2 卡,锚只被探 1 次
        assert calls[0]["url"] == f"{API_URL}/om_root3/reply"
        assert calls[1]["url"].split("?")[0] == API_URL
        assert calls[2]["url"].split("?")[0] == API_URL
        assert sleeper.sleeps == []

    def test_fallback_on_last_attempt_still_downgrades(self):
        """末次尝试槽上的降级不烧预算:503×2 退避耗掉 2 次尝试后,第 3 次
        (末次)reply 报 230011 → 仍完成降级改投 create(回归:早期 for 槽
        位计数的实现在此坠入「不可达」AssertionError,降级 create 根本不发)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls,
            sleeper,
            client_kwargs={
                "responses": [
                    httpx.Response(503, text="x"),
                    httpx.Response(503, text="x"),
                    _feishu_code(230011, "reply message not found"),
                    _feishu_ok(),
                ]
            },
        )
        asyncio.run(
            channel.send([{"title": "条目"}], _ctx(_feishu_target(thread_id="om_root4")))
        )
        assert len(calls) == 4  # 2 瞬态 + 1 死锚探测 + 1 降级 create
        assert calls[2]["url"] == f"{API_URL}/om_root4/reply"
        assert calls[3]["url"].split("?")[0] == API_URL  # 降级 create 在末次槽内完成
        assert sleeper.sleeps == [1.0, 2.0]  # 降级零退避(蓝本内联兜底,不额外等)

    def test_create_path_fallback_code_fails_without_downgrade(self):
        """create 路径收到 fallback 类码:无锚可丢,立即失败(防自降级环)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(
            calls, sleeper, client_kwargs={"responses": [_feishu_code(230011, "x")]}
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], _ctx(_feishu_target())))
        assert excinfo.value.code == "feishu_api_error"
        assert len(calls) == 1

    def test_fallback_codes_constant_matches_blueprint(self):
        """蓝本口径钉死:``_FEISHU_REPLY_FALLBACK_CODES = {230011, 231003}``。"""
        from myssia.push.feishu_card import FEISHU_REPLY_FALLBACK_CODES

        assert FEISHU_REPLY_FALLBACK_CODES == frozenset({230011, 231003})


# ---------------------------------------------------------------------------
# 飞书:卡片长度护栏(拆多卡)
# ---------------------------------------------------------------------------


class TestFeishuCardSplit:
    def test_small_batch_stays_single_card(self):
        """小批量(估算 ≤ 阈值):单卡单 POST,行为与拆卡前一致。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(calls, sleeper)
        asyncio.run(
            channel.send(
                [{"title": "条目一", "url": "https://e/1"}, {"title": "条目二"}],
                _ctx(_feishu_target()),
            )
        )
        assert len(calls) == 1

    def test_large_digest_splits_into_multiple_cards(self):
        """大 digest(估算超 4000)拆多卡:每卡载荷 ≤ 阈值、条目整全、
        footer 只挂末卡、标题每卡在场。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        items = [
            {"title": f"条目{i} " + "x" * 700, "url": f"https://e/{i}"} for i in range(12)
        ]
        channel = _feishu_channel(calls, sleeper)
        asyncio.run(channel.send(items, _ctx(_feishu_target())))
        assert len(calls) >= 2
        seen_titles: list[str] = []
        for index, call in enumerate(calls):
            card = json.loads(call["body"]["content"])
            assert len(json.dumps(card, ensure_ascii=False)) <= CARD_SPLIT_THRESHOLD
            assert card["header"]["title"]["content"]  # 每卡有标题
            if index == len(calls) - 1:
                assert card["elements"][-1]["tag"] == "note"  # footer 只挂末卡
            else:
                assert card["elements"][-1]["tag"] != "note"
            seen_titles.extend(
                str(element)
                for element in card["elements"]
                if isinstance(element, dict)
            )
        # 条目完整性:12 个条目标题各出现且仅出现一次
        for i in range(12):
            marker = f"条目{i} "
            assert sum(1 for t in seen_titles if marker in t) == 1

    def test_single_oversized_item_kept_intact(self):
        """单条目自身超阈值:独占一卡不截断(条目完整优先于阈值)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        monster = "巨" + "长" * 5000
        channel = _feishu_channel(calls, sleeper)
        asyncio.run(
            channel.send([{"title": monster, "url": "https://e/big"}], _ctx(_feishu_target()))
        )
        assert len(calls) == 1
        card = json.loads(calls[0]["body"]["content"])
        assert monster in json.dumps(card, ensure_ascii=False)  # 全文在场
        assert len(json.dumps(card, ensure_ascii=False)) > CARD_SPLIT_THRESHOLD  # 如实超线

    def test_template_output_splits_at_line_boundaries(self):
        """模板输出(单 markdown 体)按行边界拆:行不切断、每卡 ≤ 阈值。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        template = "\n".join(f"第{i}行 " + "y" * 300 for i in range(30))
        channel = _feishu_channel(calls, sleeper, template=template)
        asyncio.run(channel.send([{"title": "t"}], _ctx(_feishu_target())))
        assert len(calls) >= 2
        contents: list[str] = []
        for call in calls:
            card = json.loads(call["body"]["content"])
            assert len(json.dumps(card, ensure_ascii=False)) <= CARD_SPLIT_THRESHOLD
            contents.append(
                "".join(
                    str(element.get("text", {}).get("content", ""))
                    for element in card["elements"]
                    if isinstance(element, dict)
                )
            )
        joined = "\n".join(contents)
        for i in range(30):  # 每行整全落进某一卡
            assert f"第{i}行 " + "y" * 300 in joined

    def test_threshold_constant_aligns_blueprint(self):
        """蓝本口径钉死:``_SPLIT_THRESHOLD = 4000``(上游 1293-1295 行)。"""
        assert CARD_SPLIT_THRESHOLD == 4000

    def test_empty_items_placeholder_card_unchanged(self):
        """空批次:占位卡(「本槽位没有待推送条目」)单卡,行为不变。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _feishu_channel(calls, sleeper)
        asyncio.run(channel.send([], _ctx(_feishu_target())))
        assert len(calls) == 1
        card = json.loads(calls[0]["body"]["content"])
        assert "本槽位没有待推送条目" in json.dumps(card, ensure_ascii=False)


# ---------------------------------------------------------------------------
# telegram:sendMessage 包退避(蓝本 _telegram_retry_delay)
# ---------------------------------------------------------------------------


TG_CONTEXT = _ctx(ChannelTarget(platform="telegram", chat_id="424242"))


class TestTelegramRetryBackoff:
    def test_429_uses_retry_after_with_priority(self):
        """429 携 parameters.retry_after=7 → 退避 7.0s(优先于指数基数)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _tg_channel(
            calls,
            sleeper,
            client_kwargs={
                "responses": [
                    _tg_error(429, "Too Many Requests: retry after 7",
                              parameters={"retry_after": 7}),
                    _tg_ok(),
                ]
            },
        )
        asyncio.run(channel.send([{"title": "条目"}], TG_CONTEXT))
        assert len(calls) == 2
        assert sleeper.sleeps == [7.0]

    def test_429_without_retry_after_backs_off_exponentially(self):
        """429 缺 retry_after → 指数退避 2**0 = 1.0s。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _tg_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [_tg_error(429, "Too Many Requests"), _tg_ok()]},
        )
        asyncio.run(channel.send([{"title": "条目"}], TG_CONTEXT))
        assert len(calls) == 2
        assert sleeper.sleeps == [1.0]

    def test_5xx_exhausts_at_three_attempts(self):
        """持续 503:3 次封顶(1 首发加 2 重试),退避 [1.0, 2.0],如实抛。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _tg_channel(
            calls, sleeper, client_kwargs={"responses": [_tg_error(503, "Service Unavailable")]}
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], TG_CONTEXT))
        assert excinfo.value.code == "telegram_api_error"
        assert "503" in str(excinfo.value)
        assert len(calls) == 3
        assert sleeper.sleeps == [1.0, 2.0]

    def test_timeout_never_retried(self):
        """超时(ReadTimeout)永不重试:单次失败零退避(防重复消息)。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _tg_channel(
            calls, sleeper, client_kwargs={"raises": [httpx.ReadTimeout("timed out")]}
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], TG_CONTEXT))
        assert excinfo.value.code == "http_error"
        assert isinstance(excinfo.value.__cause__, httpx.ReadTimeout)
        assert len(calls) == 1
        assert sleeper.sleeps == []

    def test_transport_error_retries_then_succeeds(self):
        """非超时传输错(连接拒绝)→ 指数退避重试 → 成功。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _tg_channel(
            calls,
            sleeper,
            client_kwargs={"raises": [httpx.ConnectError("connection refused"), None]},
        )
        asyncio.run(channel.send([{"title": "条目"}], TG_CONTEXT))
        assert len(calls) == 2
        assert sleeper.sleeps == [1.0]

    def test_permanent_400_fails_without_retry(self):
        """永久码 400(chat not found):单次失败零退避。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _tg_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [_tg_error(400, "Bad Request: chat not found")]},
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], TG_CONTEXT))
        assert excinfo.value.code == "telegram_api_error"
        assert len(calls) == 1
        assert sleeper.sleeps == []

    def test_non_json_502_retries_then_succeeds(self):
        """非 JSON 502(invalid_response 携结构化状态)→ 瞬态退避。"""
        calls: list[dict] = []
        sleeper = SleepRecorder()
        channel = _tg_channel(
            calls,
            sleeper,
            client_kwargs={"responses": [httpx.Response(502, text="Bad Gateway"), _tg_ok()]},
        )
        asyncio.run(channel.send([{"title": "条目"}], TG_CONTEXT))
        assert len(calls) == 2
        assert sleeper.sleeps == [1.0]
