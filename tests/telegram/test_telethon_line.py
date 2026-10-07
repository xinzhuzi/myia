"""Tests for the Telethon user line (10-06-telegram-telethon B4).

覆盖面(design D5 + B4 任务面;全 mock 零网络零真 telethon 零真钥匙串):

- **依赖门/凭据**:require_telethon 缺装 → dependency_missing;api_id/api_hash
  三态(缺 = my.telegram.org 指引 / 非数字 = invalid / 齐 = 元组);
- **消息面适配**:telethon_message_to_update 的 Bot API 同形映射(锚/媒体组
  组键/发送者/标题/时间),与 updates_to_items 的复用接缝(#tg- 锚);
- **登录流**:session 复用/--force 删旧/手机号→验证码→(2FA)→session 0600/
  验证码错/限频服从/凭据值零外显;
- **事件宿主**:连接退避(FloodWait 服从服务器秒数;transport 指数退避)/
  session 失效结构化上抛(重登指引)/事件→条目→过滤→出口(与 bot 线同
  语义:锚幂等/账本口径/高价值合并单推)/相册三成员跨事件吸收(F13 事件
  面回归)/只读边界(fake 客户端调用面记录,零写接口);
- **引擎 user 模式**:mode 词表拒/依赖缺结构化拒/api 凭据空态/session 未
  首登空态/窗口拉取端到端(锚+过滤)/未授权 session_expired/FloodWait
  结构化。
"""

from __future__ import annotations

import asyncio
import sys
import types
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from myssia.secrets import SECRET_SERVICE, InMemoryKeychainBackend
from myssia.telegram.events import TelegramEventLedger
from myssia.telegram.filter import TelegramFilterConfig, TelegramFilterPipeline
from myssia.telegram.telethon_line import (
    INSTALL_COMMAND,
    SESSION_FILE_MODE,
    TelethonLineError,
    TelethonLoginFlow,
    TelethonUserHost,
    flood_wait_seconds,
    require_telethon,
    resolve_api_credentials,
    session_path,
    telethon_message_to_update,
)

from conftest import run

CHAT_ID = -1001234567890
OTHER_CHAT = -1009999999999
SOURCE_URL = "https://api.telegram.org"
SOURCE_NAME = "telegram-mihomo_party_group"
API_ID = 1234567
API_HASH = "0123456789abcdef0123456789abcdef"


# ---------------------------------------------------------------------------
# fakes(telethon 鸭子面;异常类名与 telethon.errors 真名对齐 —— 映射按名匹配)
# ---------------------------------------------------------------------------


class FloodWaitError(Exception):
    def __init__(self, seconds: float) -> None:
        super().__init__(f"FloodWait {seconds}s")
        self.seconds = seconds


class SessionPasswordNeededError(Exception):
    pass


class PhoneCodeInvalidError(Exception):
    pass


class AuthKeyUnregistered(Exception):
    pass


@dataclass
class FakeSender:
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None


@dataclass
class FakeChat:
    title: str | None = None


@dataclass
class FakeMessage:
    """telethon Message 鸭子面(适配函数只读这些属性)。"""

    id: int
    chat_id: int
    raw_text: str | None = None
    date: datetime | None = None
    grouped_id: int | None = None
    chat: Any = None
    sender: Any = None


def message(
    mid: int,
    text: str | None,
    *,
    chat_id: int = CHAT_ID,
    grouped_id: int | None = None,
    username: str | None = "alice",
    title: str = "羊毛群",
) -> FakeMessage:
    return FakeMessage(
        id=mid,
        chat_id=chat_id,
        raw_text=text,
        date=datetime(2026, 10, 8, 12, 0, 0, tzinfo=timezone.utc),
        grouped_id=grouped_id,
        chat=FakeChat(title=title),
        sender=FakeSender(username=username),
    )


class FakeRecordingClient:
    """telethon TelegramClient 鸭子面(引擎/宿主消费);调用面全记录。"""

    def __init__(
        self,
        *,
        authorized: bool = True,
        messages: list[FakeMessage] | None = None,
        connect_errors: list[Exception] | None = None,
    ) -> None:
        self.authorized = authorized
        self.messages = list(messages or [])
        self.connect_errors = list(connect_errors or [])
        self.calls: list[str] = []
        self.handlers: list[tuple[Any, Any]] = []
        self.disconnected = False

    async def connect(self) -> None:
        self.calls.append("connect")
        if self.connect_errors:
            raise self.connect_errors.pop(0)

    async def is_user_authorized(self) -> bool:
        self.calls.append("is_user_authorized")
        return self.authorized

    async def iter_messages(self, entity: Any, limit: int | None = None):
        self.calls.append(f"iter_messages:{entity}:{limit}")
        for item in self.messages:
            yield item

    def add_event_handler(self, handler: Any, event_filter: Any = None) -> None:
        self.calls.append("add_event_handler")
        self.handlers.append((handler, event_filter))

    async def disconnect(self) -> None:
        self.calls.append("disconnect")
        self.disconnected = True


class FakeLoginClient:
    """登录流消费面(认证例外:send_code_request/sign_in 允许)。"""

    def __init__(
        self,
        session_target: Path,
        *,
        authorized: bool = False,
        needs_password: bool = False,
        code_invalid: bool = False,
        send_code_error: Exception | None = None,
        write_session: bool = True,
    ) -> None:
        self.session_target = session_target
        self.authorized = authorized
        self.needs_password = needs_password
        self.code_invalid = code_invalid
        self.send_code_error = send_code_error
        self.write_session = write_session
        self.calls: list[str] = []
        self.received: dict[str, Any] = {}

    async def connect(self) -> None:
        self.calls.append("connect")

    async def is_user_authorized(self) -> bool:
        self.calls.append("is_user_authorized")
        return self.authorized

    async def send_code_request(self, phone: str) -> None:
        self.calls.append("send_code_request")
        self.received["phone"] = phone
        if self.send_code_error is not None:
            raise self.send_code_error

    async def sign_in(
        self, phone: str | None = None, code: str | None = None, password: str | None = None
    ) -> None:
        self.calls.append("sign_in")
        if code is not None:
            self.received["code"] = code
        if code is not None and self.needs_password and password is None:
            raise SessionPasswordNeededError()
        if code is not None and self.code_invalid:
            raise PhoneCodeInvalidError()
        if password is not None:
            self.received["password"] = password
        if self.write_session:
            self.session_target.parent.mkdir(parents=True, exist_ok=True)
            self.session_target.write_bytes(b"fake-session")

    async def disconnect(self) -> None:
        self.calls.append("disconnect")


class FakeSleeper:
    """记录 sleep 秒数,永不真睡。"""

    def __init__(self) -> None:
        self.sleeps: list[float] = []

    async def __call__(self, seconds: float) -> None:
        self.sleeps.append(seconds)


class Recorder:
    """出仓 sink 双面记录(F14:push 返 bool)。"""

    def __init__(self, *, push_result: bool = True) -> None:
        self.stored: list[dict] = []
        self.pushed: list[dict] = []
        self._push_result = push_result

    def store(self, item: dict) -> bool:
        if any(old["url"] == item["url"] for old in self.stored):
            return False
        self.stored.append(item)
        return True

    async def push(self, item: dict) -> bool:
        self.pushed.append(item)
        return self._push_result


def make_binding(keywords: tuple[str, ...] = ("免费",)) -> Any:
    from myssia.telegram.serve import TelegramSourceBinding

    return TelegramSourceBinding(
        chat_id=str(CHAT_ID),
        source_name=SOURCE_NAME,
        source_url=SOURCE_URL,
        pipeline=TelegramFilterPipeline(
            TelegramFilterConfig(keywords=keywords, llm_base_url=None, llm_api_key=None)
        ),
    )


def make_user_host(
    tmp_path: Path,
    client: FakeRecordingClient,
    *,
    recorder: Recorder | None = None,
    stop_after_events: int | None = None,
    stop_after_ticks: int = 1,
) -> tuple[TelethonUserHost, TelegramEventLedger, Recorder, FakeSleeper, dict]:
    """装配用户宿主(全注入):默认首个空闲 tick 即停(lifecycle 用例有限
    退出);``stop_after_events`` = N 个事件后停(事件面用例)。"""
    recorder = recorder or Recorder()
    ledger = TelegramEventLedger(tmp_path / "events-user.db")
    stop_flag = {"stop": False}
    sleeper = FakeSleeper()
    real_sleep = sleeper.__call__
    ticks = {"n": 0}

    async def _sleep(seconds: float) -> None:
        await real_sleep(seconds)
        ticks["n"] += 1
        if ticks["n"] >= stop_after_ticks:
            stop_flag["stop"] = True

    host = TelethonUserHost(
        client=client,
        bindings={str(CHAT_ID): make_binding()},
        ledger=ledger,
        push_high_value=recorder.push,
        store_item=recorder.store,
        sleep=_sleep,
        should_stop=lambda: stop_flag["stop"],
        new_message_filter=lambda: object(),
    )
    if stop_after_events is not None:
        original = host._on_event

        async def _counting(event: Any) -> None:
            await original(event)
            if host.events >= stop_after_events:
                stop_flag["stop"] = True

        host._on_event = _counting  # type: ignore[method-assign]
    return host, ledger, recorder, sleeper, stop_flag


# ---------------------------------------------------------------------------
# 依赖门 / 凭据解析
# ---------------------------------------------------------------------------


def block_telethon_import(monkeypatch: pytest.MonkeyPatch) -> None:
    """确定性依赖缺失缝:拦 ``importlib.import_module``(require_telethon 的
    真实取数路径;拦 ``builtins.__import__`` 对 importlib 无强制力 —— 2026-
    10-08 全量套件实证:venv 意外装上 telethon 后该缝静默失效)。"""
    import importlib as _importlib

    real_import_module = _importlib.import_module

    def _blocked(name: str, *args: object, **kwargs: object):
        if name == "telethon":
            raise ImportError("No module named 'telethon'")
        return real_import_module(name, *args, **kwargs)  # type: ignore[return-value]

    monkeypatch.setattr(_importlib, "import_module", _blocked)
    monkeypatch.delitem(sys.modules, "telethon", raising=False)


def test_require_telethon_missing_is_structured(monkeypatch: pytest.MonkeyPatch) -> None:
    """缺装 → dependency_missing 带安装命令(simplex/ocr 判例)。"""
    block_telethon_import(monkeypatch)
    with pytest.raises(TelethonLineError) as excinfo:
        require_telethon()
    assert excinfo.value.reason == "dependency_missing"
    assert INSTALL_COMMAND in str(excinfo.value)
    assert excinfo.value.fatal is True


def make_backend(*, api_id: str | None = str(API_ID), api_hash: str | None = API_HASH):
    backend = InMemoryKeychainBackend()
    if api_id is not None:
        backend.set_password(SECRET_SERVICE, "myia/telegram/api-id", api_id)
    if api_hash is not None:
        backend.set_password(SECRET_SERVICE, "myia/telegram/api-hash", api_hash)
    return backend


def test_resolve_api_credentials_three_states() -> None:
    """缺 = my.telegram.org 指引;非数字 = invalid;齐 = (int, str)。"""
    with pytest.raises(TelethonLineError) as excinfo:
        resolve_api_credentials(backend=make_backend(api_id=None))
    assert excinfo.value.reason == "api_credentials_missing"
    assert "my.telegram.org" in str(excinfo.value)
    assert "myssia secret set myia/telegram/api-id" in str(excinfo.value)

    with pytest.raises(TelethonLineError) as excinfo:
        resolve_api_credentials(backend=make_backend(api_id="not-a-number"))
    assert excinfo.value.reason == "api_credentials_invalid"
    assert "not-a-number" not in str(excinfo.value)  # 值不落日志

    assert resolve_api_credentials(backend=make_backend()) == (API_ID, API_HASH)


def test_session_path_shape(tmp_path: Path) -> None:
    """session 路径确定性派生:数据根 telegram/telethon.session。"""
    assert session_path(tmp_path) == tmp_path / "telegram" / "telethon.session"
    assert SESSION_FILE_MODE == 0o600


# ---------------------------------------------------------------------------
# 消息面适配(telethon → Bot API 同形 → 既有分拣/锚复用)
# ---------------------------------------------------------------------------


def test_message_to_update_full_mapping() -> None:
    """全字段映射:id/chat_id/标题/时间/raw_text/grouped_id/发送者。"""
    update = telethon_message_to_update(message(101, "免费羊毛快来"))
    inner = update["message"]
    assert update["update_id"] == 101
    assert inner["message_id"] == 101
    assert inner["chat"]["id"] == CHAT_ID
    assert inner["chat"]["title"] == "羊毛群"
    assert inner["text"] == "免费羊毛快来"
    assert isinstance(inner["date"], float)
    assert inner["from"] == {"username": "alice"}


def test_message_to_update_minimal_and_media_group() -> None:
    """缺面宽容:无文本/无发送者/无时间;相册 grouped_id → media_group_id。"""
    bare = telethon_message_to_update(
        FakeMessage(id=7, chat_id=CHAT_ID, raw_text=None, date=None, chat=None, sender=None)
    )
    assert "text" not in bare["message"]
    assert "from" not in bare["message"]
    assert "date" not in bare["message"]
    assert bare["update_id"] == 7

    grouped = telethon_message_to_update(
        message(8, "相册说明", grouped_id=555_000_111)
    )
    assert grouped["message"]["media_group_id"] == "555000111"


def test_message_to_update_feeds_existing_item_pipeline() -> None:
    """适配输出直接喂 updates_to_items:#tg- 锚/群分拣零改动复用。"""
    from myssia.engines.telegram import updates_to_items

    updates = [
        telethon_message_to_update(message(201, "第一条")),
        telethon_message_to_update(message(202, "别群消息", chat_id=OTHER_CHAT)),
    ]
    items = updates_to_items(updates, str(CHAT_ID), source_url=SOURCE_URL)
    assert [item["url"] for item in items] == [
        f"{SOURCE_URL}#tg-{CHAT_ID}-201",
    ]
    assert items[0]["chat_id"] == CHAT_ID
    assert items[0]["message_id"] == 201


# ---------------------------------------------------------------------------
# 登录流(myssia telegram login;全注入零交互零网络)
# ---------------------------------------------------------------------------


def make_flow(tmp_path: Path, client: FakeLoginClient, backend: Any = None) -> TelethonLoginFlow:
    answers = iter(["+8613800138000", "12345"])

    def _input(prompt: str) -> str:
        return next(answers)

    def _password(prompt: str) -> str:
        return "hunter2"

    lines: list[str] = []

    def _print(text: str) -> None:
        lines.append(text)

    flow = TelethonLoginFlow(
        input_fn=_input,
        password_fn=_password,
        print_fn=_print,
        client_factory=lambda session, api_id, api_hash: client,
        backend=backend if backend is not None else make_backend(),
    )
    flow._printed = lines  # type: ignore[attr-defined]
    return flow


def test_login_existing_session_reused_without_client(tmp_path: Path) -> None:
    """已有 session = 直接复用提示,零连接零交互。"""
    target = session_path(tmp_path)
    target.parent.mkdir(parents=True)
    target.write_bytes(b"existing")
    client = FakeLoginClient(target)

    class _Boom:
        def __call__(self, *args):  # pragma: no cover - 不应触
            raise AssertionError("复用路径不得构造客户端")

    flow = TelethonLoginFlow(
        input_fn=lambda p: pytest.fail("复用路径不得读输入"),
        client_factory=_Boom(),
        backend=make_backend(),
        print_fn=lambda t: None,
    )
    path = run(flow.run(tmp_path))
    assert path == target
    assert client.calls == []


def test_login_interactive_success_and_permissions(tmp_path: Path) -> None:
    """手机号→验证码→session 落盘 0600;值零回显。"""
    target = session_path(tmp_path)
    client = FakeLoginClient(target)
    factory_args: list[tuple] = []

    def _factory(session: str, api_id: int, api_hash: str) -> FakeLoginClient:
        factory_args.append((session, api_id, api_hash))
        return client

    flow = make_flow(tmp_path, client)
    flow._client_factory = _factory  # type: ignore[attr-defined]
    path = run(flow.run(tmp_path))
    assert path == target and target.exists()
    assert (target.stat().st_mode & 0o777) == SESSION_FILE_MODE
    assert client.calls == [
        "connect", "is_user_authorized", "send_code_request", "sign_in", "disconnect",
    ]
    assert client.received["phone"] == "+8613800138000"
    assert client.received["code"] == "12345"
    assert factory_args == [(str(target), API_ID, API_HASH)]  # 配了 = 自有对主路径
    joined = "\n".join(flow._printed)
    assert "+8613800138000" not in joined  # 手机号零回显
    assert "12345" not in joined  # 验证码零回显
    assert "默认凭据" not in joined  # 自有对:无兜底披露
    assert "myssia telegram serve" in joined  # 下一步指引


def test_login_zero_credential_falls_back_to_documented_pair(tmp_path: Path) -> None:
    """零凭据兜底(2026-10-08 主人令):api_id/api_hash 未配钥匙串 → 文档
    公开示例对登录成功 + 限速风险披露;my.telegram.org 裸 ERROR 也能登。"""
    from myssia.telegram.telethon_line import (
        DEFAULT_FALLBACK_API_HASH,
        DEFAULT_FALLBACK_API_ID,
    )

    target = session_path(tmp_path)
    client = FakeLoginClient(target)
    factory_args: list[tuple] = []

    def _factory(session: str, api_id: int, api_hash: str) -> FakeLoginClient:
        factory_args.append((session, api_id, api_hash))
        return client

    flow = TelethonLoginFlow(
        input_fn=lambda p: {"手机号": "+8613800138000", "验证码": "54321"}[p[:3]],
        password_fn=lambda p: "pw",
        print_fn=lambda t: None,
        client_factory=_factory,
        backend=make_backend(api_id=None, api_hash=None),
    )
    lines: list[str] = []
    flow._print = lines.append  # type: ignore[method-assign]
    path = run(flow.run(tmp_path))
    assert path == target and target.exists()
    assert factory_args == [
        (str(target), DEFAULT_FALLBACK_API_ID, DEFAULT_FALLBACK_API_HASH)
    ]
    assert client.received["code"] == "54321"
    joined = "\n".join(lines)
    assert "默认凭据" in joined and "限速" in joined  # 风险如实披露
    assert "myssia secret set myia/telegram/api-id" in joined  # 换自有对指引
    assert "login --force" in joined  # 重登指引


def test_login_force_deletes_stale_session(tmp_path: Path) -> None:
    """--force 删旧重登(失效重登路径)。"""
    target = session_path(tmp_path)
    target.parent.mkdir(parents=True)
    target.write_bytes(b"stale")
    client = FakeLoginClient(target)
    flow = make_flow(tmp_path, client)
    run(flow.run(tmp_path, force=True))
    assert client.calls[0] == "connect"  # 真走了登录
    assert any("已删除旧 session" in line for line in flow._printed)


def test_login_two_factor_password_path(tmp_path: Path) -> None:
    """2FA:sign_in 抛 SessionPasswordNeededError → 密码注入重签。"""
    target = session_path(tmp_path)
    client = FakeLoginClient(target, needs_password=True)
    flow = make_flow(tmp_path, client)
    run(flow.run(tmp_path))
    assert client.received["password"] == "hunter2"
    assert client.received["code"] == "12345"
    joined = "\n".join(flow._printed)
    assert "hunter2" not in joined  # 密码零回显


def test_login_code_invalid_structured(tmp_path: Path) -> None:
    """验证码错 → code_invalid 结构化(重试指引)。"""
    client = FakeLoginClient(session_path(tmp_path), code_invalid=True)
    flow = make_flow(tmp_path, client)
    with pytest.raises(TelethonLineError) as excinfo:
        run(flow.run(tmp_path))
    assert excinfo.value.reason == "code_invalid"
    assert "myssia telegram login" in str(excinfo.value)


def test_login_flood_wait_disclosed(tmp_path: Path) -> None:
    """限频:服从语义如实披露等待秒数(不静默硬睡 CLI)。"""
    client = FakeLoginClient(
        session_path(tmp_path), send_code_error=FloodWaitError(300)
    )
    flow = make_flow(tmp_path, client)
    with pytest.raises(TelethonLineError) as excinfo:
        run(flow.run(tmp_path))
    assert excinfo.value.reason == "flood_wait"
    assert "300" in str(excinfo.value)


def test_login_api_credentials_invalid_still_structured(tmp_path: Path) -> None:
    """api_id 非数字(配了但坏)不属「缺」—— 结构化失败,不走兜底。"""
    flow = TelethonLoginFlow(
        input_fn=lambda p: "",
        client_factory=lambda *a: pytest.fail("坏凭据不得构造客户端"),
        backend=make_backend(api_id="not-a-number"),
        print_fn=lambda t: None,
    )
    with pytest.raises(TelethonLineError) as excinfo:
        run(flow.run(tmp_path))
    assert excinfo.value.reason == "api_credentials_invalid"


# ---------------------------------------------------------------------------
# 事件宿主(telethon 线;连接退避/session 失效/事件→出口/只读边界)
# ---------------------------------------------------------------------------


def test_host_registers_handler_and_stops_clean(tmp_path: Path) -> None:
    """连接→授权→注册事件 handler→停止位退出→断开(只读四面)。"""
    client = FakeRecordingClient()
    host, ledger, recorder, _, _ = make_user_host(tmp_path, client)
    run(host.run_forever())
    assert client.calls == [
        "connect", "is_user_authorized", "add_event_handler", "disconnect",
    ]
    assert len(client.handlers) == 1  # 一个 NewMessage handler
    assert client.disconnected is True
    assert host.events == 0 and recorder.stored == []


def test_host_unauthorized_session_is_fatal_with_relogin_guidance(tmp_path: Path) -> None:
    """session 在而未授权 → session_expired 结构化上抛 + --force 指引(D4)。"""
    client = FakeRecordingClient(authorized=False)
    host, _, _, _, _ = make_user_host(tmp_path, client)
    with pytest.raises(TelethonLineError) as excinfo:
        run(host.run_forever())
    assert excinfo.value.reason == "session_expired"
    assert excinfo.value.fatal is True
    assert "myssia telegram login --force" in str(excinfo.value)
    assert client.calls[-1] == "disconnect"  # 收尾仍执行


def test_host_connect_flood_wait_obeyed(tmp_path: Path) -> None:
    """FloodWait 服从:睡服务器指定秒(+1 余量)后重连,不走指数退避。"""
    client = FakeRecordingClient(
        connect_errors=[FloodWaitError(42)]
    )
    host, _, _, sleeper, _ = make_user_host(tmp_path, client, stop_after_ticks=10**9)

    async def _drive() -> None:
        assert await host._connect_with_backoff() is True

    run(_drive())
    assert client.calls == ["connect", "connect"]  # 首连被拒,服从后二连
    assert sleeper.sleeps == [43.0]


def test_host_connect_transport_backoff_doubles(tmp_path: Path) -> None:
    """transport 类连接失败 → 指数退避 1s→2s(serve 同款;帽 300s)。"""
    client = FakeRecordingClient(
        connect_errors=[OSError("boom"), OSError("boom")]
    )
    host, _, _, sleeper, _ = make_user_host(tmp_path, client, stop_after_ticks=10**9)

    async def _drive() -> None:
        await host._connect_with_backoff()

    run(_drive())
    assert client.calls == ["connect"] * 3
    assert sleeper.sleeps == [1.0, 2.0]


def test_host_event_to_item_stored_with_anchor(tmp_path: Path) -> None:
    """事件→条目:粗筛命中无 LLM=降级普通出仓,#tg- 锚入库+账本 stored。"""

    class _Event:
        def __init__(self, msg: FakeMessage) -> None:
            self.message = msg

    client = FakeRecordingClient()
    host, ledger, recorder, _, _ = make_user_host(tmp_path, client, stop_after_events=1)
    run(host._on_event(_Event(message(301, "免费羊毛一枚"))))
    assert [item["url"] for item in recorder.stored] == [
        f"{SOURCE_URL}#tg-{CHAT_ID}-301"
    ]
    assert recorder.pushed == []  # 降级纯粗筛:零即时推
    assert ledger.counts().get("stored") == 1


def test_host_event_outcome_ledger_vocabulary(tmp_path: Path) -> None:
    """账本口径与 bot 线同词表:dropped_chat/dropped_textless/dropped_coarse。"""

    class _Event:
        def __init__(self, msg: FakeMessage) -> None:
            self.message = msg

    client = FakeRecordingClient()
    host, ledger, recorder, _, _ = make_user_host(tmp_path, client, stop_after_events=3)
    run(host._on_event(_Event(message(401, "别群", chat_id=OTHER_CHAT))))
    run(host._on_event(_Event(message(402, None))))
    run(host._on_event(_Event(message(403, "闲聊灌水"))))
    counts = ledger.counts()
    assert counts.get("dropped_chat") == 1
    assert counts.get("dropped_textless") == 1
    assert counts.get("dropped_coarse") == 1
    assert recorder.stored == []


def test_host_album_three_members_absorbed_across_events(tmp_path: Path) -> None:
    """相册三成员逐事件:F13 事件面回归 —— 首成员锚定后,后续成员(含带
    caption 的)全部并入,不重复出条(滚动一轮记忆会在第二成员处丢记忆)。"""

    class _Event:
        def __init__(self, msg: FakeMessage) -> None:
            self.message = msg

    client = FakeRecordingClient()
    host, ledger, recorder, _, _ = make_user_host(tmp_path, client, stop_after_events=3)
    run(host._on_event(_Event(message(501, "相册说明:免费节点", grouped_id=9001))))
    run(host._on_event(_Event(message(502, None, grouped_id=9001))))
    run(host._on_event(_Event(message(503, "第三段 caption", grouped_id=9001))))
    assert [item["url"] for item in recorder.stored] == [
        f"{SOURCE_URL}#tg-{CHAT_ID}-501"
    ]
    assert ledger.counts().get("stored") == 1
    assert ledger.counts().get("dropped_textless") == 2


def test_host_read_only_client_surface(tmp_path: Path) -> None:
    """只读边界:宿主全生命周期对客户端的调用面 = connect/授权/注册/断开,
    零写接口(send_message/forward_messages/…永不出现)。"""

    class _Event:
        def __init__(self, msg: FakeMessage) -> None:
            self.message = msg

    client = FakeRecordingClient()
    host, _, _, _, _ = make_user_host(tmp_path, client, stop_after_events=1)
    run(host._on_event(_Event(message(601, "免费"))))
    client.calls.clear()
    host._should_stop = lambda: True  # type: ignore[method-assign]
    run(host.run_forever())
    allowed = {"connect", "is_user_authorized", "add_event_handler", "disconnect"}
    assert set(client.calls) <= allowed
    for call in client.calls:
        assert not call.startswith(("send_", "forward_", "delete_", "edit_"))


def test_flood_wait_seconds_duck_typing() -> None:
    """flood_wait_seconds:.seconds 鸭子面(非限频异常 = None)。"""
    assert flood_wait_seconds(FloodWaitError(9)) == 9.0
    assert flood_wait_seconds(OSError("no seconds")) is None
    assert flood_wait_seconds(ValueError()) is None


# ---------------------------------------------------------------------------
# CLI 装配面(myssia telegram login;零网络零钥匙串零交互)
# ---------------------------------------------------------------------------


def test_cli_telegram_login_parser_registered():
    """``myssia telegram login`` 在册(subparser + --force 装配烟测)。"""
    from myssia.cli import build_parser

    parser = build_parser()
    ns = parser.parse_args(["telegram", "login"])
    assert ns.telegram_command == "login"
    assert ns.force is False
    forced = parser.parse_args(["telegram", "login", "--force"])
    assert forced.force is True


def test_cli_telegram_login_structured_failure_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    """CLI 装配烟测:空钥匙串走零凭据兜底继续;未装 telethon(本仓 mock 纪律
    下的常态)→ dependency_missing 结构化退出 1;装了则空手机号 → login_failed
    退出 1 —— 两世界都收敛在结构化错误退出,零交互挂死。"""
    from myssia.cli import EXIT_CONFIG_ERROR, main
    from myssia.secrets import InMemoryKeychainBackend

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    monkeypatch.setattr("myssia.secrets.get_backend", lambda: InMemoryKeychainBackend())
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    monkeypatch.setattr("getpass.getpass", lambda prompt: "")
    # 零网纪律:钉死依赖缺失世界(venv 真装了 telethon 的开发机上,真
    # TelegramClient 连真端点,测试缝必须确定性拦)。
    block_telethon_import(monkeypatch)
    code = main(["telegram", "login", "--db", str(tmp_path / "myssia.db")])
    assert code == EXIT_CONFIG_ERROR
    captured = capsys.readouterr()
    combined = captured.out + captured.err
    assert "myssia[telethon]" in combined  # 安装指引结构化在场


# ---------------------------------------------------------------------------
# 引擎 user 模式(engine: telegram mode: user;mock telethon 模块注入)
# ---------------------------------------------------------------------------


def install_fake_telethon(
    monkeypatch: pytest.MonkeyPatch, client: FakeRecordingClient
) -> None:
    """把 fake telethon 模块塞进 sys.modules(TelegramClient 工厂返回注入件)。"""
    module = types.ModuleType("telethon")
    module.TelegramClient = lambda session, api_id, api_hash: client  # type: ignore[attr-defined]
    module.events = types.SimpleNamespace(NewMessage=lambda: object())  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "telethon", module)


def user_source(**overrides: object):
    from myssia.schema import SourceConfig

    data: dict = {
        "name": SOURCE_NAME,
        "engine": "telegram",
        "url": SOURCE_URL,
        "engine_options": {
            "telegram": {
                "mode": "user",
                "chat_id": str(CHAT_ID),
                "api_id": "keychain:myia/telegram/api-id",
                "api_hash": "keychain:myia/telegram/api-hash",
            }
        },
    }
    data.update(overrides)
    return SourceConfig.model_validate(data)


def user_context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    from myssia.engines.fetch_base import FetchContext
    from tests.conftest import make_client

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    context = FetchContext(client=make_client(lambda request: None))
    context.keychain_backend = make_backend()
    return context


def test_engine_user_mode_invalid_mode_rejected(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """mode 词表外 → invalid_engine_options(结构化拒,零 I/O)。"""
    from myssia.engines.telegram import TelegramEngine

    engine = TelegramEngine(user_source(), user_context(monkeypatch, tmp_path))
    bad = user_source()
    bad.extra_params["engine_options"]["telegram"]["mode"] = "mtproto"
    engine = TelegramEngine(bad, user_context(monkeypatch, tmp_path))
    from myssia.engines.fetch_base import FetchError

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert "mode" in str(excinfo.value)


def test_engine_user_mode_dependency_missing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """telethon 缺装 → FetchError dependency_missing 带安装命令(想用而未装:
    凭据齐 + session 在,只有依赖缺 —— 空态前置不遮蔽依赖门)。"""
    from myssia.engines.fetch_base import FetchError
    from myssia.engines.telegram import TelegramEngine

    session = session_path(tmp_path)
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_bytes(b"fake")
    block_telethon_import(monkeypatch)
    engine = TelegramEngine(user_source(), user_context(monkeypatch, tmp_path))
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "dependency_missing"
    assert INSTALL_COMMAND in str(excinfo.value)


def test_engine_user_mode_credentials_and_session_empty_states(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """api 凭据缺 = credential_missing;session 未首登 = session_missing
    (两空态均零请求零 telethon 触达)。"""
    from myssia.engines.telegram import TelegramEngine

    context = user_context(monkeypatch, tmp_path)
    context.keychain_backend = make_backend(api_id=None)
    engine = TelegramEngine(user_source(), context)
    assert run(engine.fetch()) == []
    assert engine.last_skip_reason == "credential_missing"

    context2 = user_context(monkeypatch, tmp_path)
    engine2 = TelegramEngine(user_source(), context2)
    assert run(engine2.fetch()) == []
    assert engine2.last_skip_reason == "session_missing"


def test_engine_user_mode_window_fetch_end_to_end(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """窗口拉取端到端:iter_messages → #tg- 锚 → 粗筛过滤出仓;只读调用面。"""
    from myssia.engines.telegram import TelegramEngine

    session = session_path(tmp_path)
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_bytes(b"fake")
    client = FakeRecordingClient(
        messages=[message(701, "免费羊毛"), message(702, "闲聊"), message(703, None)]
    )
    install_fake_telethon(monkeypatch, client)
    engine = TelegramEngine(user_source(), user_context(monkeypatch, tmp_path))
    items = run(engine.fetch())
    assert [item["url"] for item in items] == [
        f"{SOURCE_URL}#tg-{CHAT_ID}-701",
    ]
    # 只读调用面:连接/授权/拉取/断开;确认请求(offset=)永不出场。
    assert client.calls == [
        "connect",
        "is_user_authorized",
        f"iter_messages:{CHAT_ID}:100",
        "disconnect",
    ]


def test_engine_user_mode_unauthorized_session(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """session 在而未授权 → session_expired 结构化(重登指引)。"""
    from myssia.engines.fetch_base import FetchError
    from myssia.engines.telegram import TelegramEngine

    session = session_path(tmp_path)
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_bytes(b"stale")
    client = FakeRecordingClient(authorized=False)
    install_fake_telethon(monkeypatch, client)
    engine = TelegramEngine(user_source(), user_context(monkeypatch, tmp_path))
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "session_expired"
    assert "myssia telegram login --force" in str(excinfo.value)


def test_engine_user_mode_flood_wait_structured(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """拉取限频 → telegram_flood_wait 结构化(秒数披露,服从语义)。"""
    from myssia.engines.fetch_base import FetchError
    from myssia.engines.telegram import TelegramEngine

    session = session_path(tmp_path)
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_bytes(b"fake")

    class _FloodClient(FakeRecordingClient):
        async def iter_messages(self, entity, limit=None):
            self.calls.append(f"iter_messages:{entity}:{limit}")
            raise FloodWaitError(77)
            yield  # pragma: no cover - 生成器形态要求

    client = _FloodClient()
    install_fake_telethon(monkeypatch, client)
    engine = TelegramEngine(user_source(), user_context(monkeypatch, tmp_path))
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "telegram_flood_wait"
    assert "77" in str(excinfo.value)


def test_engine_user_mode_session_dead_exception_mapped(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """AuthKeyUnregistered → session_expired(telethon errors 鸭子名匹配)。"""
    from myssia.engines.fetch_base import FetchError
    from myssia.engines.telegram import TelegramEngine

    session = session_path(tmp_path)
    session.parent.mkdir(parents=True, exist_ok=True)
    session.write_bytes(b"dead")

    class _DeadClient(FakeRecordingClient):
        async def iter_messages(self, entity, limit=None):
            self.calls.append(f"iter_messages:{entity}:{limit}")
            raise AuthKeyUnregistered()
            yield  # pragma: no cover

    client = _DeadClient()
    install_fake_telethon(monkeypatch, client)
    engine = TelegramEngine(user_source(), user_context(monkeypatch, tmp_path))
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "session_expired"
