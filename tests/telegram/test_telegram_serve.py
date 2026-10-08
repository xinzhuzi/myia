"""Tests for the Telegram serve resident host (10-06-telegram-telethon B3).

覆盖面(design D5 serve 面):

- **offsets**:roundtrip/缺文件=0/坏 JSON=0/非法值拒写(重放由锚点去重兜底);
- **events**:outcome 词表记账/词表外拒写/counts/tail;
- **poller**:长轮询 URL 形状(offset/timeout=25/limit)、result 解析、
  401/409 = fatal(不退避,上抛)、transport = 非致命、token 零外显;
- **host**:一轮更新 → 过滤(fake completer)→ 普通入库/高价值恰 1 次推送
  (组合铁律)、offset 持久 = max+1、账本 outcome 分布、未配置 chat/
  无文本/非消息三类丢弃记账、断线指数退避(1→2s,成功归零)、致命错误
  上抛、should_stop 干净停、入库失败不带走循环。

零真实网络(poller 注 fake 或 MockTransport)、零真实钥匙串。
"""

from __future__ import annotations

import json

import httpx
import pytest

from myssia.telegram.events import OUTCOMES, TelegramEventLedger
from myssia.telegram.filter import TelegramFilterConfig, TelegramFilterPipeline
from myssia.telegram.offsets import OffsetStore
from myssia.telegram.serve import (
    BACKOFF_BASE_SECONDS,
    LONG_POLL_SECONDS,
    POLL_LIMIT,
    TelegramPollError,
    TelegramPoller,
    TelegramServeHost,
    TelegramSourceBinding,
)

from conftest import make_client, run

CHAT_ID = -1001234567890
OTHER_CHAT = -1009999999999
SOURCE_URL = "https://api.telegram.org"
SOURCE_NAME = "telegram-mihomo_party_group"
BOT_TOKEN = "8000000001:AA_test-token-do-not-leak"


# ---------------------------------------------------------------------------
# fakes
# ---------------------------------------------------------------------------


class FakeCompletion:
    def __init__(self, text: str) -> None:
        self.text = text
        self.total_tokens = 50


class FakeCompleter:
    def __init__(self, mapping: dict[int, int]) -> None:
        self.mapping = mapping
        self.calls = 0

    async def __call__(self, *, model: str, system: str, user: str) -> FakeCompletion:
        self.calls += 1
        payload = [
            {"id": item_id, "score": score, "reason": "fake"}
            for item_id, score in self.mapping.items()
        ]
        return FakeCompletion(json.dumps(payload, ensure_ascii=False))


class FakeSleeper:
    """记录退避等待,永不真睡."""

    def __init__(self) -> None:
        self.sleeps: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.sleeps.append(seconds)


def message_update(
    update_id: int,
    message_id: int,
    text: str | None,
    *,
    chat_id: int = CHAT_ID,
    media_group_id: str | None = None,
) -> dict:
    message: dict = {
        "message_id": message_id,
        "date": 1761000000.0,
        "chat": {"id": chat_id, "type": "supergroup", "title": "g"},
    }
    if text is not None:
        message["text"] = text
    if media_group_id is not None:
        message["media_group_id"] = media_group_id
    return {"update_id": update_id, "message": message}


def make_binding(completer: FakeCompleter | None = None) -> TelegramSourceBinding:
    return TelegramSourceBinding(
        chat_id=str(CHAT_ID),
        source_name=SOURCE_NAME,
        source_url=SOURCE_URL,
        pipeline=TelegramFilterPipeline(
            TelegramFilterConfig(llm_base_url="env:X", llm_api_key="env:Y"),
            completer=completer,
        ),
    )


class FakePoller:
    """脚本化轮询:按序吐轮次,支持错误与停表."""

    def __init__(self, rounds: list) -> None:
        self.rounds = list(rounds)  # 每项:list[updates] 或 TelegramPollError
        self.calls: list[int] = []

    async def poll(self, offset: int) -> list[dict]:
        self.calls.append(offset)
        item = self.rounds.pop(0) if self.rounds else []
        if isinstance(item, TelegramPollError):
            raise item
        return item


class Recorder:
    """出仓 sink 双面记录;push 返回 bool(F14:True = 真实送达)."""

    def __init__(self, *, push_result: bool = True) -> None:
        self.stored: list[dict] = []
        self.pushed: list[dict] = []
        self._push_result = push_result

    def store(self, item: dict) -> bool:
        seen = any(old["url"] == item["url"] for old in self.stored)
        if seen:
            return False
        self.stored.append(item)
        return True

    async def push(self, item: dict) -> bool:
        self.pushed.append(item)
        return self._push_result


def build_host(*args, **kwargs):  # pragma: no cover - 兼容占位(见 _wire)
    return _wire(*args, **kwargs)


async def _noop() -> None:
    return None


def test_offset_store_roundtrip(tmp_path):
    store = OffsetStore(tmp_path / "telegram" / "offsets.json")
    assert store.load() == 0  # 缺文件
    store.save(42)
    assert store.load() == 42
    store.save(43)
    assert store.load() == 43
    assert not store.path.with_suffix(".json.tmp").exists()  # 原子写不留临时件


def test_offset_store_corrupt_file_falls_back_to_zero(tmp_path, caplog):
    path = tmp_path / "offsets.json"
    path.write_text("{not json", encoding="utf-8")
    with caplog.at_level("WARNING", logger="myssia.telegram.offsets"):
        assert OffsetStore(path).load() == 0
    assert "按 0" in caplog.text


def test_offset_store_rejects_invalid_values(tmp_path):
    path = tmp_path / "offsets.json"
    OffsetStore(path).save(-5)
    OffsetStore(path).save(True)
    assert not path.exists()


# ---------------------------------------------------------------------------
# events ledger
# ---------------------------------------------------------------------------


def test_event_ledger_records_and_counts(tmp_path):
    ledger = TelegramEventLedger(tmp_path / "events.db")
    assert ledger.record(update_id=1, outcome="stored", score=6)
    assert ledger.record(update_id=2, outcome="pushed", chat_id=str(CHAT_ID), message_id=9, score=10)
    assert ledger.record(update_id=3, outcome="dropped_coarse")
    assert not ledger.record(update_id=4, outcome="nonsense")
    counts = ledger.counts()
    assert counts == {"stored": 1, "pushed": 1, "dropped_coarse": 1}
    tail = ledger.tail()
    assert tail[0]["update_id"] == 3  # 新→旧
    assert set(OUTCOMES) >= {"stored", "pushed", "dropped_coarse", "error"}


# ---------------------------------------------------------------------------
# poller
# ---------------------------------------------------------------------------


def test_poller_long_poll_url_shape_and_result():
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(
            200, json={"ok": True, "result": [message_update(7, 70, "免费")]}
        )

    poller = TelegramPoller(make_client(handler), BOT_TOKEN)
    updates = run(poller.poll(6))
    assert updates and updates[0]["update_id"] == 7
    url = str(captured[0].url)
    assert "offset=6" in url
    assert f"timeout={int(LONG_POLL_SECONDS)}" in url
    assert f"limit={POLL_LIMIT}" in url
    assert "/bot" in url  # token 在请求里
    assert BOT_TOKEN not in str(updates)  # 响应面不带凭据


@pytest.mark.parametrize(
    ("status", "reason", "fatal"),
    [(401, "http_401", True), (409, "http_409", True), (500, "http_500", False)],
)
def test_poller_status_errors(status, reason, fatal):
    poller = TelegramPoller(
        make_client(lambda request: httpx.Response(status, text="x")), BOT_TOKEN
    )
    with pytest.raises(TelegramPollError) as excinfo:
        run(poller.poll(0))
    assert excinfo.value.reason == reason
    assert excinfo.value.fatal is fatal
    assert BOT_TOKEN not in str(excinfo.value)  # 错误消息净化


def test_poller_transport_error_non_fatal():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("boom", request=request)

    poller = TelegramPoller(make_client(handler), BOT_TOKEN)
    with pytest.raises(TelegramPollError) as excinfo:
        run(poller.poll(0))
    assert excinfo.value.reason == "transport"
    assert not excinfo.value.fatal


def test_poller_malformed_payload():
    poller = TelegramPoller(
        make_client(lambda request: httpx.Response(200, json={"nope": 1})), BOT_TOKEN
    )
    with pytest.raises(TelegramPollError) as excinfo:
        run(poller.poll(0))
    assert excinfo.value.reason == "malformed"


# ---------------------------------------------------------------------------
# host:分派/出口/账本/offset
# ---------------------------------------------------------------------------


def test_host_round_pushes_exactly_once_and_persists_offset(tmp_path):
    """一轮:2 高价值 + 1 普通 + 1 未命中 → 推送恰 1 次,入库 4 条(含合并),
    offset=max+1,账本 pushed=1/stored=3/dropped_coarse=1."""
    completer = FakeCompleter({1: 9, 2: 10, 3: 6})
    recorder = Recorder()
    host, recorder = _wire(
        tmp_path,
        rounds=[
            [
                message_update(11, 101, "免费 token 翻倍"),
                message_update(12, 102, "白嫖 Claude 一年"),
                message_update(13, 103, "常规优惠推送"),
                message_update(14, 104, "纯闲聊"),
            ]
        ],
        completer=completer,
        recorder=recorder,
    )
    run(host.run_forever())
    # 出口:高价值恰 1 条合并(组合铁律),带组内最高分与 source 锚
    assert len(recorder.pushed) == 1
    merged = recorder.pushed[0]
    assert merged["score"] == 10
    assert merged["merged_count"] == 2
    assert merged["source"] == SOURCE_NAME
    assert merged["url"] == f"{SOURCE_URL}#tg-{CHAT_ID}-101-hv2-102"
    # 入库:合并条目 + 2 普通(6 分/未命中丢弃不进库)
    urls = [item["url"] for item in recorder.stored]
    assert merged["url"] in urls
    assert f"{SOURCE_URL}#tg-{CHAT_ID}-103" in urls
    assert f"{SOURCE_URL}#tg-{CHAT_ID}-104" not in urls  # 粗筛未命中零痕迹
    # offset 持久 = max_update_id + 1
    assert host._offsets.load() == 15
    # 账本分布
    counts = host._ledger.counts()
    assert counts.get("pushed") == 1
    assert counts.get("stored") == 2
    assert counts.get("dropped_coarse") == 1


def _wire(tmp_path, *, rounds, completer=None, recorder=None, should_stop=None, sleeper=None):
    poller = FakePoller(rounds)
    binding = make_binding(completer)
    recorder = recorder or Recorder()
    host = TelegramServeHost(
        poller=poller,
        bindings={str(CHAT_ID): binding},
        offsets=OffsetStore(tmp_path / "telegram" / "offsets.json"),
        ledger=TelegramEventLedger(tmp_path / "telegram" / "events.db"),
        push_high_value=recorder.push,
        store_item=recorder.store,
        sleep=sleeper or _RecordingSleep(),
        # 缺省:脚本轮次耗尽即停(单轮测试跑完一轮干净退出)
        should_stop=should_stop or (lambda: not poller.rounds),
    )
    return host, recorder


class _RecordingSleep:
    async def __call__(self, seconds: float) -> None:
        return None


def test_host_dropped_outcomes_ledgered(tmp_path):
    """未配置 chat / 无文本 / 非消息更新 → 账本三类丢弃,零出仓."""
    host, recorder = _wire(
        tmp_path,
        rounds=[
            [
                message_update(21, 201, "别群免费消息", chat_id=OTHER_CHAT),
                message_update(22, 202, None),
                {"update_id": 23, "callback_query": {"id": "x"}},
            ]
        ],
    )
    run(host.run_forever())
    assert recorder.stored == []
    assert recorder.pushed == []
    counts = host._ledger.counts()
    assert counts.get("dropped_chat") == 1
    assert counts.get("dropped_textless") == 1
    assert counts.get("dropped_other") == 1


def test_host_offset_resumes_from_persisted(tmp_path):
    """重启续拉:offset 文件在 → 第二宿主从 max+1 起(不重放)."""
    rounds = [[message_update(31, 301, "免费 a")]]
    host1, _ = _wire(tmp_path, rounds=rounds)
    run(host1.run_forever())
    assert host1._offsets.load() == 32
    host2, recorder2 = _wire(tmp_path, rounds=[[message_update(32, 302, "白嫖 b")]])
    run(host2.run_forever())
    assert host2._poller.calls == [32]  # 从持久 offset 起
    assert any(item["url"].endswith("#tg-%d-302" % CHAT_ID) for item in recorder2.stored)


def test_host_backoff_doubles_then_resets(tmp_path):
    """断线退避:1s→2s 翻倍,成功后归零(再失败回 1s 起步)."""
    sleeper = FakeSleeper()
    rounds = [
        TelegramPollError("net down", reason="transport"),
        TelegramPollError("net down", reason="transport"),
        [message_update(41, 401, "免费 a")],
        TelegramPollError("net down", reason="transport"),
    ]
    host, _ = _wire(tmp_path, rounds=rounds, sleeper=sleeper)
    # 计退避次数:第 3 次退避睡完即停(第 4 轮失败后)
    state = {"backoffs": 0}
    real_backoff = host._backoff

    async def counting_backoff(exc):
        state["backoffs"] += 1
        return await real_backoff(exc)

    host._backoff = counting_backoff
    host._should_stop = lambda: state["backoffs"] >= 3
    run(host.run_forever())
    assert sleeper.sleeps == [1.0, 2.0, 1.0]  # 翻倍→成功归零→重新起步
    assert host.backoff_seconds == 2.0


def test_host_fatal_poll_error_raises(tmp_path):
    """401/409 致命:不退避,结构化上抛(宿主退出给人看)."""
    host, _ = _wire(
        tmp_path,
        rounds=[TelegramPollError("401: token 失效", reason="http_401", fatal=True)],
    )
    with pytest.raises(TelegramPollError):
        run(host.run_forever())


def test_host_store_failure_does_not_kill_loop(tmp_path):
    """入库 sink 炸:账本记 error,循环活着,推送照走(高价值不因库炸丢推)."""
    completer = FakeCompleter({1: 10})
    recorder = Recorder()

    def exploding_store(item):
        raise RuntimeError("disk full")

    poller = FakePoller([[message_update(51, 501, "免费大羊毛")]])
    host = TelegramServeHost(
        poller=poller,
        bindings={str(CHAT_ID): make_binding(completer)},
        offsets=OffsetStore(tmp_path / "telegram" / "offsets.json"),
        ledger=TelegramEventLedger(tmp_path / "telegram" / "events.db"),
        push_high_value=recorder.push,
        store_item=exploding_store,
        sleep=_RecordingSleep(),
        should_stop=lambda: not poller.rounds,
    )
    run(host.run_forever())
    assert len(recorder.pushed) == 1  # 推送不受入库失败连坐
    assert host._ledger.counts().get("pushed") == 1


def test_host_filter_pipeline_failure_degrades_to_store(tmp_path):
    """过滤管线炸:全量入库降级 + 账本 error,循环不死."""

    class ExplodingPipeline:
        config = TelegramFilterConfig()

        async def process(self, items):
            raise RuntimeError("llm stack blew")

    poller = FakePoller([[message_update(61, 601, "免费 a")]])
    recorder = Recorder()
    host = TelegramServeHost(
        poller=poller,
        bindings={
            str(CHAT_ID): TelegramSourceBinding(
                chat_id=str(CHAT_ID),
                source_name=SOURCE_NAME,
                source_url=SOURCE_URL,
                pipeline=ExplodingPipeline(),
            )
        },
        offsets=OffsetStore(tmp_path / "telegram" / "offsets.json"),
        ledger=TelegramEventLedger(tmp_path / "telegram" / "events.db"),
        push_high_value=recorder.push,
        store_item=recorder.store,
        sleep=_RecordingSleep(),
        should_stop=lambda: not poller.rounds,
    )
    run(host.run_forever())
    assert len(recorder.stored) == 1  # 降级入库
    assert host._ledger.counts().get("error") == 1


def test_host_no_llm_config_stores_all(tmp_path):
    """LLM 未配 = 降级纯粗筛:命中全部入库,零推送(批量档同语义)."""
    host, recorder = _wire(
        tmp_path, rounds=[[message_update(71, 701, "免费 a")]]
    )  # make_binding 默认带 env: refs + 无 completer → 端点解析失败降级
    run(host.run_forever())
    assert len(recorder.stored) == 1
    assert recorder.pushed == []


# ---------------------------------------------------------------------------
# 深审修复批(F8 指纹分键 / F10 transport 净化 / F11 保留帽 / F13 跨轮媒体组 /
# F14 no_channel 虚账 + 资源收尾)
# ---------------------------------------------------------------------------

BOT_TOKEN_B = "8000000002:AA_another-bot-token"


def test_offset_store_bot_fingerprint_isolation(tmp_path):
    """F8:同目录双 bot 各指纹文件各游标 —— 交叉污染(静默丢单)不再可能."""
    from myssia.telegram.offsets import bot_fingerprint

    base = tmp_path / "telegram" / "offsets.json"
    store_a = OffsetStore(base, bot_token=BOT_TOKEN)
    store_b = OffsetStore(base, bot_token=BOT_TOKEN_B)
    assert store_a.path != store_b.path
    assert store_a.path.name == f"offsets-{bot_fingerprint(BOT_TOKEN)}.json"
    # 并发交替写:各存各读,互不覆盖不串台
    store_a.save(101)
    store_b.save(7)
    assert store_a.load() == 101
    assert store_b.load() == 7
    store_a.save(102)
    assert store_b.load() == 7  # B 的游标不被 A 的推进顶掉
    assert store_a.load() == 102
    assert not base.exists()  # 旧单键路径全程未被触碰


def test_offset_store_migrates_legacy_once_then_deletes(tmp_path):
    """F8 迁移:旧单键文件被首个指纹宿主采纳一次即删;后来 bot 从 0 续拉."""
    base = tmp_path / "telegram" / "offsets.json"
    base.parent.mkdir(parents=True)
    base.write_text(json.dumps({"offset": 42}), encoding="utf-8")
    store_a = OffsetStore(base, bot_token=BOT_TOKEN)
    assert store_a.load() == 42  # 采纳旧值(单 bot 升级不断点)
    assert store_a.path.exists()
    assert not base.exists()  # 删除旧键:后来 bot 不会误采他人游标
    assert store_a.load() == 42  # 此后读自己的指纹文件
    store_b = OffsetStore(base, bot_token=BOT_TOKEN_B)
    assert store_b.load() == 0  # 第二 bot:无旧键可采,从 0(重放安全)


def test_event_ledger_bot_dimension(tmp_path):
    """F8:账本同指纹分键 —— 双 bot counts 不混计;no_channel 在词表."""
    base = tmp_path / "telegram" / "events.db"
    ledger_a = TelegramEventLedger(base, bot_token=BOT_TOKEN)
    ledger_b = TelegramEventLedger(base, bot_token=BOT_TOKEN_B)
    assert ledger_a._path != ledger_b._path
    assert ledger_a.record(update_id=1, outcome="stored")
    assert ledger_a.record(update_id=2, outcome="no_channel")  # F14 新词
    assert ledger_b.record(update_id=1, outcome="pushed")
    assert ledger_a.counts() == {"stored": 1, "no_channel": 1}
    assert ledger_b.counts() == {"pushed": 1}
    assert not base.exists()  # 旧单库路径未建
    ledger_a.close()
    ledger_b.close()


def test_event_ledger_prunes_to_cap(tmp_path):
    """F11:每写一裁到 1000 行帽(最旧出列);帽内显式 prune 零删."""
    from myssia.telegram.events import MAX_EVENTS

    ledger = TelegramEventLedger(tmp_path / "events.db")
    for index in range(MAX_EVENTS + 5):
        assert ledger.record(update_id=index, outcome="stored")
    counts = ledger.counts()
    assert counts["stored"] == MAX_EVENTS
    tail_ids = [row["update_id"] for row in ledger.tail(limit=500)]
    assert max(tail_ids) == MAX_EVENTS + 4  # 最新在
    assert min(tail_ids) == 505  # 可见窗最旧 = 505:0-4 已裁(帽 1000,窗 500)
    assert ledger.prune() == 0  # 帽内显式裁剪零删
    ledger.close()


def test_poller_transport_error_masks_token():
    """F10:transport 异常 str 带完整 URL(含 token)—— 净化后零外显."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(
            f"[Errno 8] Connection failed: {request.url}", request=request
        )

    poller = TelegramPoller(make_client(handler), BOT_TOKEN)
    with pytest.raises(TelegramPollError) as excinfo:
        run(poller.poll(0))
    assert excinfo.value.reason == "transport"
    assert BOT_TOKEN not in str(excinfo.value)  # token path 段打码
    assert "/bot***/" in str(excinfo.value)


def test_host_media_group_cross_round_absorbed(tmp_path):
    """F13:相册切两轮 —— 第二轮后到的同组带 caption 成员并入首轮锚,不重复出条."""
    host, recorder = _wire(
        tmp_path,
        rounds=[
            [message_update(11, 101, "相册说明:免费节点截图", media_group_id="mg-x")],
            [message_update(12, 102, "相册第二段 caption", media_group_id="mg-x")],
            [message_update(13, 103, "第三轮免费独立消息")],
        ],
    )
    run(host.run_forever())
    urls = [item["url"] for item in recorder.stored]
    assert urls == [
        f"{SOURCE_URL}#tg-{CHAT_ID}-101",  # 首轮组锚
        f"{SOURCE_URL}#tg-{CHAT_ID}-103",  # 第三轮独立条目
    ]  # 第二轮 102 被跨轮记忆吞掉(并入 mg-x,不重复出条)
    counts = host._ledger.counts()
    assert counts.get("stored") == 2
    assert counts.get("dropped_textless") == 1  # 并入成员按口径记 dropped_textless


def test_host_no_push_channel_no_virtual_accounting(tmp_path):
    """F14:推送 sink 返 False(通道未配)—— 账本记 no_channel,pushed 不虚增."""
    completer = FakeCompleter({1: 10})
    recorder = Recorder(push_result=False)
    host, recorder = _wire(
        tmp_path,
        rounds=[[message_update(21, 201, "免费大羊毛")]],
        completer=completer,
        recorder=recorder,
    )
    run(host.run_forever())
    assert len(recorder.stored) == 1  # 条目已入库(日报兜底)
    assert len(recorder.pushed) == 1  # sink 被调用过(留痕在 sink 侧)
    counts = host._ledger.counts()
    assert counts.get("no_channel") == 1  # 如实记通道未配
    assert "pushed" not in counts  # 不虚记 pushed
    assert "stored" not in counts  # 首条走 no_channel,不重复记 stored


def test_host_shutdown_closes_poller_client_and_keeps_ledger_readable(tmp_path):
    """F14:宿主退出路径收尾 —— poller 客户端 aclose(fake 无 aclose 软探兼容);
    账本连接归装配方关闭(宿主退出后观测面 counts/tail 仍可读)。"""

    class ClosablePoller(FakePoller):
        def __init__(self, rounds):
            super().__init__(rounds)
            self.closed = False

        async def aclose(self) -> None:
            self.closed = True

    poller = ClosablePoller([[message_update(31, 301, "免费 a")]])
    ledger = TelegramEventLedger(tmp_path / "events.db")
    host = TelegramServeHost(
        poller=poller,
        bindings={str(CHAT_ID): make_binding()},
        offsets=OffsetStore(tmp_path / "telegram" / "offsets.json"),
        ledger=ledger,
        push_high_value=Recorder().push,
        store_item=Recorder().store,
        sleep=_RecordingSleep(),
        should_stop=lambda: not poller.rounds,
    )
    run(host.run_forever())
    assert poller.closed is True
    assert ledger.counts().get("stored") == 1  # 退出后观测面仍可读(装配方再关)
    ledger.close()  # 装配方(CLI finally / desktop bundle close)的收尾动作


# ---------------------------------------------------------------------------
# CLI 装配面(myssia telegram serve;零网络零钥匙串)
# ---------------------------------------------------------------------------


def _write_category(tmp_path, *, chat_id="-1001234567890"):
    path = tmp_path / "tg-groups.yaml"
    path.write_text(
        f"""
id: telegram-groups
name: Telegram群消息监控
schedule: "*/30 * * * *"
timezone: Asia/Shanghai
sources:
  - name: telegram-mihomo_party_group
    engine: telegram
    url: "https://api.telegram.org"
    engine_options:
      telegram:
        chat_id: "{chat_id}"
dedup:
  key: "{{url}}"
push:
  - channel: stdout
storage:
  retention: 90d
""",
        encoding="utf-8",
    )
    return path


def test_cli_telegram_serve_missing_token_guidance(tmp_path, monkeypatch, capsys):
    """钥匙串无 token → 结构化退出 1 + 四步指引(serve 无空态:没 token 没意义)."""
    from myssia.cli import EXIT_CONFIG_ERROR, main
    from myssia.secrets import InMemoryKeychainBackend

    backend = InMemoryKeychainBackend()  # 空:未写 myia/telegram/bot-token
    monkeypatch.setattr("myssia.secrets.get_backend", lambda: backend)
    path = _write_category(tmp_path)
    code = main(
        ["telegram", "serve", "--category", str(path), "--db", str(tmp_path / "myssia.db")]
    )
    assert code == EXIT_CONFIG_ERROR
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    assert "四步" in combined or "setprivacy" in combined


def test_cli_telegram_serve_rejects_non_telegram_sources(tmp_path, capsys):
    """品类含非 telegram 源 → 结构化拒(批量采集是 myssia run 的事)."""
    from myssia.cli import EXIT_CONFIG_ERROR, main

    path = tmp_path / "mixed.yaml"
    path.write_text(
        """
id: mixed
name: 混装
schedule: "0 8 * * *"
sources:
  - name: web
    engine: static_html
    url: "https://example.com"
    extract:
      type: list
      item: ".post"
      fields:
        title: ".title"
        url: "a@href"
dedup:
  key: "{url}"
storage:
  retention: 90d
""",
        encoding="utf-8",
    )
    code = main(
        ["telegram", "serve", "--category", str(path), "--db", str(tmp_path / "myssia.db")]
    )
    assert code == EXIT_CONFIG_ERROR
    captured = capsys.readouterr()
    assert "engine: telegram" in captured.out + captured.err


def test_cli_telegram_serve_help_registered():
    """``myssia telegram serve`` 在册(subparser 装配烟测)."""
    from myssia.cli import build_parser

    parser = build_parser()
    ns = parser.parse_args(["telegram", "serve"])
    assert ns.telegram_command == "serve"


def test_ledger_cross_thread_write(tmp_path):
    """账本跨线程写回归(2026-10-08 装机实跑暴露):sidecar 装配线程建、
    serve 线程写 —— check_same_thread=False(store/sqlite.py 同款)守装机面;
    CLI serve 单线程不受影响。"""
    import threading

    ledger = TelegramEventLedger(tmp_path / "events.db")
    outcome: dict[str, object] = {}

    def _write() -> None:
        outcome["ok"] = ledger.record(update_id=1, outcome="stored")

    worker = threading.Thread(target=_write)
    worker.start()
    worker.join()
    assert outcome["ok"] is True
    assert ledger.counts().get("stored") == 1
