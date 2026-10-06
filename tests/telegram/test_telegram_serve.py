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
) -> dict:
    message: dict = {
        "message_id": message_id,
        "date": 1761000000.0,
        "chat": {"id": chat_id, "type": "supergroup", "title": "g"},
    }
    if text is not None:
        message["text"] = text
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
    def __init__(self) -> None:
        self.stored: list[dict] = []
        self.pushed: list[dict] = []

    def store(self, item: dict) -> bool:
        seen = any(old["url"] == item["url"] for old in self.stored)
        if seen:
            return False
        self.stored.append(item)
        return True

    async def push(self, item: dict) -> None:
        self.pushed.append(item)


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
