"""Tests for the WeChat local-session engine (10-12-weixin-feed-channel 数据面).

四态矩阵(照 tg_web/feishu 引擎判例;design §2.2/§4):

- **配置错误**:chat/count/sides/read_timeout_seconds/channel/since_days 形状错、
  通道专属键交叉(count+localdb / since_days+pixel)、源 URL 不符锚契约、
  pagination 配置 → 结构化 FetchError(invalid_engine_options /
  invalid_wechat_local_source_url / pagination_unsupported);
- **桥缺席/失败面**:bin 缺失 = ``component_missing``(零子进程);桥超时 =
  ``bridge_timeout``;桥具名错误族码名原样透传
  (wechat_not_running/screen_recording_denied/window_closed);应答不可解析
  = ``bridge_error``;
- **结构化空态**(绝不张冠李戴):pixel ``chat.match=False`` →
  ``chat_not_open``;``chat.match=None`` → ``chat_title_unreadable``;localdb
  密钥缺位(桥 exit 21)→ ``key_unavailable``(D4 合法预期态,不算 failure,
  水位不推进);
- **开启态**:mock 桥子进程往返 → items 形状(#wx- 内容哈希锚/标题截断/
  全文 content/sides 过滤/type 过滤/空白文本跳过);锚稳定性(同窗同锚、
  OCR 微变另锚、side 入盐);
- **localdb 电池(2026-10-13 换轨批)**:argv 契约(--since 水位增量窗)、
  sender→side 派生、ts=epoch 入盐锚、sessions 名解析二查、水位推进/不推进、
  db_not_found/decrypt_failed 透传、无 store 降级;
- **词表/注册表**:schema ENGINES/EngineName 收录、ENGINE_REGISTRY 在册、
  AUTO_CHAIN 原样、auto_degrade 单级链、词表↔注册表双向同步;
- **配置装载+入库盖戳**:config/weixin.yaml 真件装载(双通道样例源:id=weixin、
  engine=wechat_local、dedup {url}、push 空、enrich 关);Pipeline 全链跑
  (桥面 mock)→ 条目 source=weixin-<会话名>、category=weixin、
  dedup_key=url 全串;同载荷二跑零新增(锚幂等)。

零真机零真桥零真实微信(bin_path/run_bridge_command_sync 全 monkeypatch;
fixture 消息全合成样本,不碰真实数据 —— 私有数据红线)。
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import httpx
import pytest

import myssia.wechat.engine as wx_engine
from myssia import schema
from myssia.engines.fetch_base import FetchContext, FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.wechat.engine import WechatLocalEngine, anchor_url
from myssia.schema import load_category_file

from conftest import make_client, make_context, make_source, run

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_URL = "https://weixin.qq.com"
CHAT = "文件传输助手"
CHAT_URL_ENCODED = "%E6%96%87%E4%BB%B6%E4%BC%A0%E8%BE%93%E5%8A%A9%E6%89%8B"
ANCHOR_RE = re.compile(rf"^wechat-local://chat/{CHAT_URL_ENCODED}#wx-[0-9a-f]{{16}}$")


def ANCHOR_RE_WITH(*, chat: str) -> re.Pattern[str]:
    """任意会话名的 #wx- 锚形状(多源断言用)."""
    return re.compile(
        rf"^wechat-local://chat/{quote(chat, safe='')}#wx-[0-9a-f]{{16}}$"
    )


# ---------------------------------------------------------------------------
# Helpers(桥面 mock:bin 存在性 + 子进程往返;fixture 全合成样本)
# ---------------------------------------------------------------------------


def make_bridge_bin(tmp_path: Path) -> Path:
    """假桥 bin(存在 + 可执行位;内容永不被执行 —— runner 已 mock)."""
    fake_bin = tmp_path / "wechat-bridge"
    fake_bin.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_bin.chmod(0o755)
    return fake_bin


def fake_runner(
    payload: dict[str, Any] | None = None,
    *,
    exit_code: int = 0,
    stdout: str | None = None,
    raise_timeout: bool = False,
    calls: list[list[str]] | None = None,
):
    """桥子进程 fake:固定应答/异常;记录 argv 供命令形态断言."""

    def _runner(argv: Any, input_text: str, timeout: float) -> tuple[int, str, str]:
        if calls is not None:
            calls.append(list(argv))
        if raise_timeout:
            raise wx_engine.LocalBridgeTimeoutError(
                f"wechat-bridge 超过 {timeout:.0f}s 未退出,子进程已终止"
            )
        if stdout is not None:
            return exit_code, stdout, ""
        return exit_code, json.dumps(payload, ensure_ascii=False), ""

    return _runner


def msg(
    text: str,
    *,
    side: str = "left",
    ts: str | None = "22:30",
    sender: str | None = "合成样本发送者",
    conf: float = 0.97,
    type_: str = "text",
) -> dict[str, Any]:
    """一条合成消息行(桥 MessageRow.to_payload 契约形;非真实数据)."""
    return {
        "ts": ts,
        "sender": sender,
        "type": type_,
        "text": text,
        "side": side,
        "conf": conf,
    }


def bridge_payload(
    messages: list[dict[str, Any]],
    *,
    match: bool | None = True,
    visible_title: str | None = CHAT,
) -> dict[str, Any]:
    """桥 messages read 成功载荷(契约形;chat.match 三态注入口)."""
    return {
        "messages": messages,
        "count": len(messages),
        "chat": {
            "requested_id": CHAT,
            "visible_title": visible_title,
            "match": match,
            "note": None if match is True else "像素链静默硬边界(合成)",
        },
        "window": {"window_id": 1, "onscreen": True, "width": 1200, "height": 800, "note": None},
        "capture": {"state": "ok", "width": 1200, "height": 800, "mean_luma": 0.5},
        "ocr": {"vl": {"used": False}},
    }


#: localdb 合成会话 id(形状真实:chatroom 形态;非任何真实会话)。
DB_CHAT_ID = "00000000000000000000@chatroom"


def db_msg(
    text: str,
    *,
    sender: str = DB_CHAT_ID,
    ts: int = 1760000000,
    type_: str = "text",
) -> dict[str, Any]:
    """一条 localdb 合成消息行(桥 localdb_query.query_messages 契约形).

    契约事实(2026-10-13 实探桥 localdb_query.py):行只有 ts(epoch 秒)/
    sender("me"|会话 id)/type/text? 或 media_placeholder?—— **没有消息
    id 字段**,锚退内容铸(引擎文档同记)。
    """
    row: dict[str, Any] = {"ts": ts, "sender": sender, "type": type_}
    if type_ == "text":
        row["text"] = text
    else:
        row["media_placeholder"] = "非文本消息,内容未导出(占位)"
    return row


def db_payload(
    messages: list[dict[str, Any]],
    *,
    chat_id: str = CHAT,
    display_name: str | None = None,
    sessions: list[dict[str, Any]] | None = None,
    since_days: int = 3,
) -> dict[str, Any]:
    """桥 localdb query 成功载荷(契约形;chat_id/display_name/sessions 注入口)."""
    return {
        "chat_id": chat_id,
        "since_days": since_days,
        "messages": messages,
        "display_name": display_name,
        "sessions": sessions if sessions is not None else [],
        "domains": {"message": "ok", "contact": "ok", "session": "ok"},
        "copy": {
            "dir": "/synthetic/wechat-localdb/decrypted",
            "built": ["message/message_0.db"],
            "kept": [],
            "skipped": [],
            "total_bytes": 0,
        },
    }


def make_engine(
    *,
    chat: Any = CHAT,
    count: Any = 50,
    sides: Any = None,
    read_timeout: Any = 60,
    url: str = SOURCE_URL,
    channel: Any = None,
    since_days: Any = None,
    store: Any = None,
    extra: dict[str, Any] | None = None,
) -> tuple[WechatLocalEngine, FetchContext]:
    """构造引擎 + 上下文(engine_options 形状注入口,Any 故意 —— 校验面).

    ``channel=None`` = 不声明(缺省 pixel);其余 None 键同理不进 options,
    使各测试精确控制「声明了什么」。
    """
    options: dict[str, Any] = {}
    if channel is not None:
        options["channel"] = channel
    options["chat"] = chat
    if channel == "localdb":
        if since_days is not None:
            options["since_days"] = since_days
    else:
        options["count"] = count
    if sides is not None:
        options["sides"] = sides
    if read_timeout is not None:
        options["read_timeout_seconds"] = read_timeout
    source_kwargs: dict[str, Any] = {
        "name": f"weixin-{CHAT}",
        "engine": "wechat_local",
        "url": url,
        "engine_options": {"wechat_local": options},
    }
    source_kwargs.update(extra or {})
    source = make_source(**source_kwargs)
    context, _clock = make_context(
        make_client(lambda request: httpx.Response(404)), store=store
    )
    return WechatLocalEngine(source, context), context


def make_engine_raw(
    options: dict[str, Any], *, store: Any = None
) -> tuple[WechatLocalEngine, FetchContext]:
    """直接喂 engine_options.wechat_local 原始 dict(交叉键/畸形面注入口)."""
    source = make_source(
        name=f"weixin-{CHAT}",
        engine="wechat_local",
        url=SOURCE_URL,
        engine_options={"wechat_local": options},
    )
    context, _clock = make_context(
        make_client(lambda request: httpx.Response(404)), store=store
    )
    return WechatLocalEngine(source, context), context


def fetch_items(engine: WechatLocalEngine) -> list[dict[str, Any]]:
    return run(engine.fetch())


# ---------------------------------------------------------------------------
# 1. 配置错误面(结构化 FetchError;零子进程)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("overrides", "fragment"),
    [
        ({"chat": None}, "chat"),
        ({"chat": "  "}, "chat"),
        ({"chat": True}, "chat"),
        ({"count": 0}, "count"),
        ({"count": 201}, "count"),
        ({"count": True}, "count"),
        ({"count": "50"}, "count"),
        ({"sides": []}, "sides"),
        ({"sides": ["left", "up"]}, "sides"),
        ({"sides": "left"}, "sides"),
        ({"sides": [True]}, "sides"),
        ({"read_timeout": 0}, "read_timeout_seconds"),
        ({"read_timeout": -1}, "read_timeout_seconds"),
        ({"read_timeout": "60"}, "read_timeout_seconds"),
    ],
)
def test_engine_options_shape_errors(overrides: dict[str, Any], fragment: str):
    engine, _ = make_engine(**overrides)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert fragment in str(excinfo.value)


@pytest.mark.parametrize(
    "url",
    [
        "http://weixin.qq.com",  # 非 https
        "https://wx.qq.com",  # 非锚域
        "https://weixin.qq.com/chat/foo",  # 路径非空
    ],
)
def test_source_url_anchor_contract(url: str):
    engine, _ = make_engine(url=url)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_wechat_local_source_url"
    assert "https://weixin.qq.com" in str(excinfo.value)


def test_pagination_unsupported():
    engine, _ = make_engine(
        extra={"pagination": {"mode": "selector", "selector": "a.next", "max_pages": 2}}
    )
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "pagination_unsupported"


# ---------------------------------------------------------------------------
# 2. 桥缺席/失败面(component_missing / bridge_timeout / 具名族透传)
# ---------------------------------------------------------------------------


def test_bridge_bin_missing_is_component_missing(tmp_path, monkeypatch):
    missing = tmp_path / "no-such-bridge"
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: missing)
    calls: list[list[str]] = []
    monkeypatch.setattr(wx_engine, "run_bridge_command_sync", fake_runner(calls=calls))
    engine, _ = make_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "component_missing"
    assert "wechat-bridge" in str(excinfo.value)
    assert calls == []  # bin 缺失先于子进程:零执行


def test_bridge_timeout_is_structured(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine, "run_bridge_command_sync", fake_runner(raise_timeout=True)
    )
    engine, _ = make_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "bridge_timeout"


@pytest.mark.parametrize(
    ("exit_code", "code"),
    [
        (10, "wechat_not_running"),
        (11, "screen_recording_denied"),
        (11, "ax_permission_denied"),
        (12, "window_closed"),
        (13, "ax_tree_empty"),
        (30, "timeout"),
    ],
)
def test_bridge_named_error_family_passes_through(
    tmp_path, monkeypatch, exit_code: int, code: str
):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    payload = {
        "error": {
            "code": code,
            "message": f"合成 {code} 错误",
            "fix_hint": "合成修复指引",
        }
    }
    monkeypatch.setattr(
        wx_engine, "run_bridge_command_sync", fake_runner(payload, exit_code=exit_code)
    )
    engine, _ = make_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    expected = "bridge_timeout" if code == "timeout" else code
    assert excinfo.value.error_type == expected
    assert "合成修复指引" in str(excinfo.value)


def test_bridge_unparseable_answer_is_bridge_error(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(exit_code=1, stdout="not-json"),
    )
    engine, _ = make_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "bridge_error"


def test_bridge_success_with_error_payload_is_rejected(tmp_path, monkeypatch):
    """exit 0 却带 error 载荷 = 契约漂移,按具名族拒(不装死)."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    payload = {"error": {"code": "window_closed", "message": "窗口未开"}}
    monkeypatch.setattr(
        wx_engine, "run_bridge_command_sync", fake_runner(payload, exit_code=0)
    )
    engine, _ = make_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "window_closed"


def test_bridge_payload_without_messages_list_is_bridge_error(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine, "run_bridge_command_sync", fake_runner({"count": 0, "chat": {"match": True}})
    )
    engine, _ = make_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "bridge_error"


# ---------------------------------------------------------------------------
# 3. 结构化空态(chat.match 三态;绝不张冠李戴)
# ---------------------------------------------------------------------------


def test_chat_not_open_is_explicit_empty_state(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(bridge_payload([msg("合成样本")], match=False, visible_title="别的事")),
    )
    engine, _ = make_engine()
    assert fetch_items(engine) == []
    assert engine.last_skip_reason == "chat_not_open"


def test_chat_title_unreadable_is_explicit_empty_state(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(bridge_payload([msg("合成样本")], match=None, visible_title=None)),
    )
    engine, _ = make_engine()
    assert fetch_items(engine) == []
    assert engine.last_skip_reason == "chat_title_unreadable"


# ---------------------------------------------------------------------------
# 4. 开启态(items 形状 / 过滤 / 命令形态)
# ---------------------------------------------------------------------------


def test_bridge_argv_contract(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(bridge_payload([msg("合成样本")]), calls=calls),
    )
    engine, _ = make_engine(chat=CHAT, count=7)
    fetch_items(engine)
    assert len(calls) == 1
    argv = calls[0]
    assert argv[1:] == ["messages", "read", CHAT, "-k", "7", "--json"]
    assert argv[0].endswith("wechat-bridge")


def test_items_shape_and_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    text = "合成样本正文第一行\n合成样本正文第二行"
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(bridge_payload([msg(text, ts="22:30", conf=0.91)])),
    )
    engine, _ = make_engine()
    items = fetch_items(engine)
    assert len(items) == 1
    item = items[0]
    assert ANCHOR_RE.match(item["url"])
    assert item["title"] == "合成样本正文第一行"
    assert item["content"] == text
    # 观测键留 raw 面(metadata;Item.from_extracted 把非契约键收进 metadata)
    assert item["sender"] == "合成样本发送者"
    assert item["side"] == "left"
    assert item["ts"] == "22:30"
    assert item["conf"] == 0.91
    assert item["chat"] == CHAT


def test_title_truncation_long_text(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    long_text = "长" * 200
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(bridge_payload([msg(long_text)])),
    )
    engine, _ = make_engine()
    items = fetch_items(engine)
    assert len(items[0]["title"]) == wx_engine.TITLE_MAX_CHARS
    assert items[0]["content"] == long_text


def test_sides_filter(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            bridge_payload(
                [
                    msg("对方消息", side="left"),
                    msg("自己的消息", side="right"),
                    msg("系统行", side="center"),
                ]
            )
        ),
    )
    # 缺省 sides=[left]:只出对方消息
    engine, _ = make_engine(sides=None)  # 不配 → 缺省 [left]
    assert [i["content"] for i in fetch_items(engine)] == ["对方消息"]
    # 显式 [left, right]:对方+自己
    engine2, _ = make_engine(sides=["left", "right"])
    assert [i["content"] for i in fetch_items(engine2)] == ["对方消息", "自己的消息"]


def test_non_text_and_blank_messages_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            bridge_payload(
                [
                    msg("正常消息"),
                    msg("图片行", type_="image"),
                    msg("   "),  # 空白文本(OCR 噪声)
                    "not-a-dict",  # 防御:非 dict 行
                ]
            )
        ),
    )
    engine, _ = make_engine()
    assert [i["content"] for i in fetch_items(engine)] == ["正常消息"]


def test_zero_items_after_filter_is_legitimate_empty(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(bridge_payload([msg("自己的消息", side="right")])),
    )
    engine, _ = make_engine()  # 缺省 [left] → 全被侧过滤
    assert fetch_items(engine) == []
    assert engine.last_skip_reason is None  # 窗口零产出 ≠ 结构化空态码


# ---------------------------------------------------------------------------
# 5. 锚稳定性(#wx- 内容哈希;同窗同锚 / OCR 微变另锚 / side·ts 入盐)
# ---------------------------------------------------------------------------


def test_anchor_stable_same_window_same_anchor():
    first = anchor_url(CHAT, "22:30", "left", "同一条合成消息")
    second = anchor_url(CHAT, "22:30", "left", "同一条合成消息")
    assert first == second


def test_anchor_whitespace_variation_collapses():
    """空白规整:OCR 行间空格抖动不另立新锚(缓解面,如实非全幂等)."""
    plain = anchor_url(CHAT, "22:30", "left", "合成 消息 文本")
    spaced = anchor_url(CHAT, "22:30", "left", "合成\n  消息\t文本 ")
    assert plain == spaced


def test_anchor_ocr_text_change_is_new_anchor():
    """文本真变(OCR 修字)= 新锚(弱幂等如实:重复条目风险面)."""
    first = anchor_url(CHAT, "22:30", "left", "合成消息甲")
    second = anchor_url(CHAT, "22:30", "left", "合成消息乙")
    assert first != second


def test_anchor_side_and_ts_are_salt():
    base = anchor_url(CHAT, "22:30", "left", "同一条合成消息")
    other_side = anchor_url(CHAT, "22:30", "right", "同一条合成消息")
    other_ts = anchor_url(CHAT, None, "left", "同一条合成消息")
    other_chat = anchor_url("别的会话", "22:30", "left", "同一条合成消息")
    assert len({base, other_side, other_ts, other_chat}) == 4


def test_anchor_shape():
    url = anchor_url(CHAT, "22:30", "left", "合成样本")
    assert url.startswith(f"wechat-local://chat/{CHAT_URL_ENCODED}#wx-")
    assert re.fullmatch(r"[0-9a-f]{16}", url.rsplit("#wx-", 1)[1])


# ---------------------------------------------------------------------------
# 5b. localdb 通道电池(2026-10-13 换轨批:全 mock,fixture 全合成样本)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("overrides", "fragment"),
    [
        ({"channel": "LocalDB"}, "channel"),
        ({"channel": True}, "channel"),
        ({"channel": "sqlite"}, "channel"),
        ({"since_days": 0}, "since_days"),
        ({"since_days": 3651}, "since_days"),
        ({"since_days": True}, "since_days"),
        ({"since_days": "3"}, "since_days"),
    ],
)
def test_localdb_options_shape_errors(overrides: dict[str, Any], fragment: str):
    """channel/since_days 形状错 = 结构化拒(零子进程)."""
    engine, _ = make_engine_raw({"chat": CHAT, "channel": "localdb", **overrides})
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert fragment in str(excinfo.value)


def test_localdb_rejects_pixel_only_count():
    """count 是 pixel 窗口帽,localdb 声明即拒(静默忽略 = 谎报配置生效)."""
    engine, _ = make_engine_raw(
        {"channel": "localdb", "chat": CHAT, "count": 50}
    )
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert "count" in str(excinfo.value)
    assert "localdb" in str(excinfo.value)


def test_pixel_rejects_localdb_only_since_days():
    engine, _ = make_engine_raw({"chat": CHAT, "since_days": 3})
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert "since_days" in str(excinfo.value)


def test_localdb_default_channel_is_pixel_for_legacy_options():
    """缺省通道回归:不声明 channel 的既有源走 pixel(messages read 形态)."""
    engine, _ = make_engine()  # 无 channel 声明
    assert engine._options()["channel"] == "pixel"


def test_localdb_argv_contract_first_pull(tmp_path, monkeypatch):
    """首拉无水位 → --since <since_days>d(缺省 3);命令形态 localdb query."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(db_payload([db_msg("合成样本")]), calls=calls),
    )
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    fetch_items(engine)
    assert len(calls) == 1
    argv = calls[0]
    assert argv[1:] == ["localdb", "query", CHAT, "--since", "3d", "--json"]
    assert argv[0].endswith("wechat-bridge")


def test_localdb_timeout_default_600(tmp_path, monkeypatch):
    """localdb 读超时缺省 600s(sidecar _QUERY_TIMEOUT_SECONDS 同款判例)."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    seen: dict[str, float] = {}

    def _runner(argv, input_text, timeout):
        seen["timeout"] = timeout
        return 0, json.dumps(db_payload([]), ensure_ascii=False), ""

    monkeypatch.setattr(wx_engine, "run_bridge_command_sync", _runner)
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    fetch_items(engine)
    assert seen["timeout"] == wx_engine.DEFAULT_LOCALDB_TIMEOUT_SECONDS == 600.0


def test_localdb_items_shape_and_side_derivation(tmp_path, monkeypatch):
    """sender 派生 side("me"→right/其余→left);ts=epoch 入盐锚;raw 键保留."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            db_payload(
                [
                    db_msg("对方合成消息", sender=DB_CHAT_ID, ts=1760000100),
                    db_msg("自己的合成消息", sender="me", ts=1760000200),
                    db_msg("图片行", type_="image"),
                    {"ts": 1760000300, "sender": DB_CHAT_ID, "type": "text"},  # 无 text 键
                    "not-a-dict",
                ],
                chat_id=CHAT,
            )
        ),
    )
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    items = fetch_items(engine)
    # 缺省 sides=[left]:只出对方消息;me 行被侧过滤;无 text/非 dict 跳过;
    # 图片行不再丢弃(10-16-feed-wx-images)——出「[图片]」占位条目
    assert [i["content"] for i in items] == ["对方合成消息", "[图片]"]
    item = items[0]
    assert ANCHOR_RE.match(item["url"])
    assert item["title"] == "对方合成消息"
    assert item["sender"] == DB_CHAT_ID
    assert item["side"] == "left"
    assert item["ts"] == 1760000100  # epoch 秒原样(raw 面)
    assert item["chat"] == CHAT
    assert "conf" not in item  # localdb 无 OCR 置信度,不谎报
    # sides=[left,right] 时自己消息也出,side=right
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            db_payload(
                [
                    db_msg("对方合成消息", sender=DB_CHAT_ID, ts=1760000100),
                    db_msg("自己的合成消息", sender="me", ts=1760000200),
                ],
                chat_id=CHAT,
            )
        ),
    )
    engine2, _ = make_engine(channel="localdb", sides=["left", "right"], read_timeout=None)
    items2 = fetch_items(engine2)
    assert [i["side"] for i in items2] == ["left", "right"]


def test_localdb_anchor_epoch_salt_and_stability():
    """localdb 锚:ts=epoch 入盐,同消息恒同锚;不同秒不并锚(内容锚如实弱幂等,
    桥应答无消息 id 不谎报强幂等 —— 引擎/档同记)."""
    first = anchor_url(CHAT, "1760000100", "left", "同一条 合成消息")
    second = anchor_url(CHAT, "1760000100", "left", " 同一条\t合成消息\n")
    other_second = anchor_url(CHAT, "1760000200", "left", "同一条 合成消息")
    assert first == second  # 压空白规整 + 精确 ts:重读恒同锚
    assert first != other_second  # 同文本不同秒:不并锚
    assert first.startswith(f"wechat-local://chat/{CHAT_URL_ENCODED}#wx-")


def _media_dispatch_runner(
    query_payload: dict[str, Any],
    media_payload: dict[str, Any] | None = None,
    *,
    calls: list[list[str]] | None = None,
    timeouts: list[float] | None = None,
    media_error: Exception | None = None,
):
    """按 argv 分发的桥 fake:query → 查询载荷;media scan → 媒体载荷/异常."""

    def _runner(argv: Any, input_text: str, timeout: float) -> tuple[int, str, str]:
        argv_list = [str(part) for part in argv]
        if calls is not None:
            calls.append(argv_list)
        if timeouts is not None:
            timeouts.append(float(timeout))
        if "media" in argv_list:
            if media_error is not None:
                raise media_error
            return 0, json.dumps(media_payload), ""
        return 0, json.dumps(query_payload), ""

    return _runner


def test_localdb_image_rows_attach_decrypted_paths(tmp_path, monkeypatch):
    """10-16-feed-wx-images:图片行出占位条目 + media scan --decrypt 按 ts
    回填 image_files(仅「已解密」;实况/失败/缺 ts 如实不挂)。"""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    img_ts = 1760000500
    calls: list[list[str]] = []
    media_payload = {
        "media": {
            "chat_id": CHAT,
            "items": [
                {
                    "message_ref": {"ts": img_ts, "sender": DB_CHAT_ID, "local_type": 3},
                    "type": "image",
                    "status": "已解密",
                    "cached_path": "/cache/abc123.jpg",
                },
                {
                    "message_ref": {"ts": img_ts + 1, "sender": DB_CHAT_ID, "local_type": 3},
                    "type": "image",
                    "status": "实况格式,暂不支持预览",
                    "cached_path": "/cache/def.wxgf",
                },
                {
                    "message_ref": {"ts": img_ts + 2, "sender": DB_CHAT_ID, "local_type": 3},
                    "type": "image",
                    "status": "解密失败",
                },
            ],
            "stats": {},
        }
    }
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        _media_dispatch_runner(
            db_payload(
                [
                    db_msg("文本消息", ts=1760000100),
                    db_msg("图片", type_="image", ts=img_ts),
                ],
                chat_id=CHAT,
            ),
            media_payload,
            calls=calls,
        ),
    )
    engine, _ = make_engine(channel="localdb")
    items = fetch_items(engine)
    assert [i["content"] for i in items] == ["文本消息", "[图片]"]
    assert items[0].get("image_files") is None  # 文本条目零媒体键
    assert items[1]["image_files"] == ["/cache/abc123.jpg"]  # 仅已解密挂载
    # 媒体扫描 argv 契约:scan + since + decrypt + json
    media_argv = next(c for c in calls if "media" in c)
    assert media_argv[1:4] == ["localdb", "media", "scan"]
    assert "--decrypt" in media_argv and "--json" in media_argv
    assert "--since" in media_argv


def test_localdb_image_media_failure_degrades_to_placeholder(tmp_path, monkeypatch):
    """媒体面任何失败(超时/非零)只降级:占位条目仍在、无 image_files、
    不拦文本条目流(私有数据红线:日志形状级)。"""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        _media_dispatch_runner(
            db_payload(
                [db_msg("文本消息", ts=1760000100), db_msg("图", type_="image", ts=1760000200)],
                chat_id=CHAT,
            ),
            media_error=wx_engine.LocalBridgeTimeoutError(
                "wechat-bridge 超过 300s 未退出,子进程已终止"
            ),
        ),
    )
    engine, _ = make_engine(channel="localdb")
    items = fetch_items(engine)
    assert [i["content"] for i in items] == ["文本消息", "[图片]"]
    assert all(i.get("image_files") is None for i in items)


def test_localdb_image_media_timeout_floor(tmp_path, monkeypatch):
    """媒体面超时地板 ≥300s:首轮解密逐张 spawn 解密件可到分钟级,沿用
    读取超时会中途超时(水位已进 → 老图永失)。"""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    timeouts: list[float] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        _media_dispatch_runner(
            db_payload([db_msg("图", type_="image", ts=1760000100)], chat_id=CHAT),
            media_payload={"media": {"items": [], "stats": {}}},
            timeouts=timeouts,
        ),
    )
    engine, _ = make_engine(channel="localdb", read_timeout=60)
    fetch_items(engine)
    assert len(timeouts) >= 2
    query_to, media_to = timeouts[0], timeouts[1]
    assert query_to == 60  # 查询沿用读取超时
    assert media_to >= 300  # 媒体扫描吃地板帽


def test_localdb_session_name_resolution_second_query(tmp_path, monkeypatch):
    """声明显示名:首查零消息且 contact 解析不出 → sessions 名解析 → 二查用会话 id."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    payloads = [
        db_payload([], chat_id=CHAT, display_name=None,
                   sessions=[{"id": DB_CHAT_ID, "name": CHAT, "unread": 0}]),
        db_payload([db_msg("解析后合成消息", sender=DB_CHAT_ID)], chat_id=DB_CHAT_ID,
                   display_name=CHAT),
    ]
    state = {"i": 0}

    def _runner(argv, input_text, timeout):
        calls.append(list(argv))
        payload = payloads[state["i"]]
        state["i"] += 1
        return 0, json.dumps(payload, ensure_ascii=False), ""

    monkeypatch.setattr(wx_engine, "run_bridge_command_sync", _runner)
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    items = fetch_items(engine)
    assert [i["content"] for i in items] == ["解析后合成消息"]
    assert len(calls) == 2
    assert calls[0][3] == CHAT  # 首查 = 声明显示名
    assert calls[1][3] == DB_CHAT_ID  # 二查 = 解析出的会话 id
    assert calls[0][4:] == calls[1][4:] == ["--since", "3d", "--json"]


def test_localdb_chat_id_direct_hit_single_query(tmp_path, monkeypatch):
    """声明会话 id 直接命中(有消息)→ 一查即中,不做 sessions 解析."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            db_payload([db_msg("直接命中合成消息")], chat_id=DB_CHAT_ID, display_name=CHAT),
            calls=calls,
        ),
    )
    engine, _ = make_engine(channel="localdb", chat=DB_CHAT_ID, read_timeout=None)
    assert [i["content"] for i in fetch_items(engine)] == ["直接命中合成消息"]
    assert len(calls) == 1


def test_localdb_quiet_chat_id_no_resolution_single_query(tmp_path, monkeypatch):
    """声明 id 但窗口零消息且 contact 有展示名(display_name 非 None)= 安静
    合法空,一查即止(display_name 在 = id 是活会话,不做名解析)."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(db_payload([], chat_id=DB_CHAT_ID, display_name=CHAT), calls=calls),
    )
    engine, _ = make_engine(channel="localdb", chat=DB_CHAT_ID, read_timeout=None)
    assert fetch_items(engine) == []
    assert engine.last_skip_reason is None  # 安静会话 ≠ 结构化空态码
    assert len(calls) == 1


def test_localdb_name_unresolvable_is_legitimate_empty(tmp_path, monkeypatch):
    """显示名不在 sessions(前 20 best-effort)= 解析不到,如实零产出不猜."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            db_payload([], chat_id=CHAT, display_name=None,
                       sessions=[{"id": "other@chatroom", "name": "别的合成会话", "unread": 0}]),
            calls=calls,
        ),
    )
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    assert fetch_items(engine) == []
    assert engine.last_skip_reason is None
    assert len(calls) == 1  # 不猜第二次


def test_localdb_key_unavailable_is_structured_skip_no_watermark(
    tmp_path, monkeypatch, engine_store
):
    """桥 exit 21 key_unavailable = D4 合法预期态:零条目 + skip 码 + 不算
    failure;水位不推进(下轮仍首拉窗口,不丢消息)."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    payload = {
        "error": {
            "code": "key_unavailable",
            "message": "合成:解密密钥未就绪(零内存途径不可推导)",
            "fix_hint": "合成指引:跑 keyscan 脚本",
        }
    }
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(payload, exit_code=21, calls=calls),
    )
    engine, _ = make_engine(channel="localdb", read_timeout=None, store=engine_store)
    assert fetch_items(engine) == []
    assert engine.last_skip_reason == "key_unavailable"
    assert len(calls) == 1
    # 水位未推进:同 store 二拉仍用首拉窗口(since_days 缺省 3)
    engine2, _ = make_engine(channel="localdb", read_timeout=None, store=engine_store)
    fetch_items(engine2)
    assert calls[1][4:] == ["--since", "3d", "--json"]


@pytest.mark.parametrize(
    ("exit_code", "code"),
    [
        (20, "db_not_found"),
        (22, "decrypt_failed"),
    ],
)
def test_localdb_other_named_family_passes_through(
    tmp_path, monkeypatch, exit_code: int, code: str
):
    """db_not_found/decrypt_failed 是真失败(非合法预期态)→ 结构化 FetchError."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    payload = {
        "error": {"code": code, "message": f"合成 {code} 错误", "fix_hint": "合成修复指引"}
    }
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(payload, exit_code=exit_code),
    )
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == code
    assert "合成修复指引" in str(excinfo.value)
    assert engine.last_skip_reason is None


def test_localdb_bridge_timeout_and_unparseable(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    monkeypatch.setattr(
        wx_engine, "run_bridge_command_sync", fake_runner(raise_timeout=True)
    )
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "bridge_timeout"
    # 应答不可解析 = bridge_error(与 pixel 同纪律)
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(exit_code=1, stdout="not-json"),
    )
    with pytest.raises(FetchError) as excinfo2:
        run(engine.fetch())
    assert excinfo2.value.error_type == "bridge_error"


def test_localdb_payload_without_messages_is_bridge_error(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner({"chat_id": CHAT, "since_days": 3}),
    )
    engine, _ = make_engine(channel="localdb", read_timeout=None)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "bridge_error"


def test_localdb_watermark_advances_and_shrinks_window(tmp_path, monkeypatch, engine_store):
    """成功拉取推进水位 → 下轮 --since 1d(增量窗);隔 25h → 2d."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            db_payload([db_msg("水位合成消息")], chat_id=DB_CHAT_ID, display_name=CHAT),
            calls=calls,
        ),
    )
    engine, _ = make_engine(
        channel="localdb", chat=DB_CHAT_ID, read_timeout=None, store=engine_store
    )
    assert len(fetch_items(engine)) == 1
    assert calls[0][4:] == ["--since", "3d", "--json"]  # 首拉 = since_days
    # 水位已落 store(change_baseline 键空间;etag = epoch 秒)
    baseline = engine_store.get_baseline(wx_engine.watermark_key(f"weixin-{CHAT}"))
    assert baseline is not None and baseline.etag is not None
    assert abs(float(baseline.etag) - time.time()) < 60
    # 二拉(同 store 新引擎实例):水位在 → 增量窗 1d
    engine2, _ = make_engine(
        channel="localdb", chat=DB_CHAT_ID, read_timeout=None, store=engine_store
    )
    fetch_items(engine2)
    assert calls[1][4:] == ["--since", "1d", "--json"]
    # 手拨水位回 25h → 2d(天粒度向上取整,相邻轮次小幅重叠由 dedup 消化)
    engine_store.set_baseline(
        wx_engine.watermark_key(f"weixin-{CHAT}"),
        etag=str(int(time.time()) - 90000),
    )
    engine3, _ = make_engine(
        channel="localdb", chat=DB_CHAT_ID, read_timeout=None, store=engine_store
    )
    fetch_items(engine3)
    assert calls[2][4:] == ["--since", "2d", "--json"]


def test_localdb_without_store_degrades_to_default_window(tmp_path, monkeypatch):
    """无 store(试抓/干跑面):水位不持久,每轮缺省窗口,不炸不谎."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            db_payload([db_msg("无库合成消息")], chat_id=DB_CHAT_ID, display_name=CHAT),
            calls=calls,
        ),
    )
    for _ in range(2):
        engine, _ = make_engine(channel="localdb", chat=DB_CHAT_ID, read_timeout=None)
        fetch_items(engine)
    assert [c[5] for c in calls] == ["3d", "3d"]  # 无水位可读,恒缺省窗


def test_localdb_corrupt_watermark_falls_back(tmp_path, monkeypatch, engine_store):
    """水位值坏(非数值 etag)→ 当无水位处理(缺省窗),不炸."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    engine_store.set_baseline(
        wx_engine.watermark_key(f"weixin-{CHAT}"), etag="not-a-number"
    )
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            db_payload([db_msg("坏水位合成消息")], chat_id=DB_CHAT_ID, display_name=CHAT),
            calls=calls,
        ),
    )
    engine, _ = make_engine(
        channel="localdb", chat=DB_CHAT_ID, read_timeout=None, store=engine_store
    )
    fetch_items(engine)
    assert calls[0][5] == "3d"


def test_localdb_second_query_key_unavailable_skips(tmp_path, monkeypatch, engine_store):
    """二查(名解析后)撞 key_unavailable:同 skip 语义,水位不推进."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    payloads = [
        db_payload([], chat_id=CHAT, display_name=None,
                   sessions=[{"id": DB_CHAT_ID, "name": CHAT, "unread": 0}]),
        {
            "error": {
                "code": "key_unavailable",
                "message": "合成:二查时密钥不可用",
                "fix_hint": "合成指引",
            }
        },
    ]
    state = {"i": 0}

    def _runner(argv, input_text, timeout):
        idx = state["i"]
        state["i"] += 1
        code = 0 if idx == 0 else 21
        return code, json.dumps(payloads[idx], ensure_ascii=False), ""

    monkeypatch.setattr(wx_engine, "run_bridge_command_sync", _runner)
    engine, _ = make_engine(channel="localdb", read_timeout=None, store=engine_store)
    assert fetch_items(engine) == []
    assert engine.last_skip_reason == "key_unavailable"
    # 水位未推进:二拉仍首拉窗口
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(db_payload([db_msg("后续合成消息")], chat_id=CHAT, display_name=CHAT)),
    )
    engine2, _ = make_engine(channel="localdb", read_timeout=None, store=engine_store)
    items = fetch_items(engine2)
    assert len(items) == 1


# ---------------------------------------------------------------------------
# 6. 词表/注册表(链外注册;AUTO_CHAIN 原样;词表↔注册表双向同步)
# ---------------------------------------------------------------------------


def test_schema_vocabulary_includes_wechat_local():
    assert "wechat_local" in schema.ENGINES
    engine_names = schema.EngineName.__args__  # type: ignore[attr-defined]
    assert "wechat_local" in engine_names


def test_registry_off_chain_registration():
    assert "wechat_local" in ENGINE_REGISTRY
    assert resolve_engine("wechat_local") is WechatLocalEngine
    assert "wechat_local" not in AUTO_CHAIN  # 链外:auto 永不路过
    assert auto_degrade("wechat_local") == ["wechat_local"]  # 单级链零降级


def test_schema_vocabulary_and_registry_are_in_sync():
    """词表(除 auto)↔注册表双向一致:新引擎两处齐改,漏一处即红."""
    assert set(schema.ENGINES) - {"auto"} == set(ENGINE_REGISTRY)


def test_source_config_accepts_wechat_local_engine():
    source = make_source(
        name="weixin-demo", engine="wechat_local", url=SOURCE_URL
    )
    assert source.engine == "wechat_local"


# ---------------------------------------------------------------------------
# 7. 配置装载 + 入库盖戳(config/weixin.yaml 真件;Pipeline 全链 mock)
# ---------------------------------------------------------------------------


def test_weixin_yaml_loads_and_carries_red_lines():
    """双通道样例(2026-10-13 换轨批):pixel 首源 + localdb 二源."""
    config = load_category_file(REPO_ROOT / "config" / "weixin.yaml")
    assert config.id == "weixin"
    assert config.name == "微信监控"
    assert len(config.sources) == 2
    # 首源(pixel 缺省显式):文件传输助手
    pixel = config.sources[0]
    assert pixel.name == f"weixin-{CHAT}"
    assert pixel.engine == "wechat_local"
    assert pixel.url == SOURCE_URL
    assert pixel.empty_ok is True
    pixel_options = pixel.extra_params["engine_options"]["wechat_local"]
    assert pixel_options["chat"] == CHAT
    assert pixel_options["channel"] == "pixel"
    assert pixel_options["count"] == 50
    # 二源(localdb 换轨样例):合成会话
    localdb = config.sources[1]
    assert localdb.name == "weixin-localdb样例会话"
    localdb_options = localdb.extra_params["engine_options"]["wechat_local"]
    assert localdb_options["channel"] == "localdb"
    assert localdb_options["since_days"] == 3
    assert "count" not in localdb_options  # 通道专属键不交叉
    assert localdb.empty_ok is True
    assert config.dedup.key == "{url}"  # #wx- 锚全串模板
    assert config.enrich.enabled is False  # 红线:私有内容不出本机
    assert config.push == []  # 红线:不外发任何通道
    assert config.storage.retention == "30d"  # 隐私谨慎缺省(TG 90d)


def test_weixin_yaml_localdb_comments_carry_keyscan_guidance():
    """密钥缺位指引面文件级注记(keyscan 一键脚本;skip 人话同源)."""
    text = (REPO_ROOT / "config" / "weixin.yaml").read_text(encoding="utf-8")
    assert "key_unavailable" in text
    assert "scripts/wechat-bridge-d4-keyscan.sh" in text


def test_pipeline_stamps_source_category_and_dedups(tmp_path, monkeypatch):
    """入库盖戳全链(双通道):引擎条目 → Item(source=yaml 源名/category=
    weixin)→ dedup {url} → store;同载荷二跑零新增(锚幂等)."""
    from myssia.pipeline import Pipeline
    from myssia.store import SQLiteStore

    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    pixel_payload = bridge_payload(
        [msg("合成样本消息甲", ts="22:30"), msg("合成样本消息乙", ts=None)]
    )
    localdb_payload = db_payload(
        [db_msg("localdb 合成样本消息", sender=DB_CHAT_ID, ts=1760000100)],
        chat_id=DB_CHAT_ID,
        display_name="localdb样例会话",
    )

    def dispatch_runner(argv: Any, input_text: str, timeout: float) -> tuple[int, str, str]:
        """按 argv 命令族分发(pixel=messages read / localdb=localdb query)."""
        if "localdb" in argv:
            return 0, json.dumps(localdb_payload, ensure_ascii=False), ""
        return 0, json.dumps(pixel_payload, ensure_ascii=False), ""

    monkeypatch.setattr(wx_engine, "run_bridge_command_sync", dispatch_runner)
    config = load_category_file(REPO_ROOT / "config" / "weixin.yaml")
    client = httpx.AsyncClient(
        transport=httpx.MockTransport(lambda request: httpx.Response(404))
    )
    store = SQLiteStore(tmp_path / "wx-feed.db")
    pipeline = Pipeline(config, store=store, client=client)

    first = run(pipeline.run())
    assert first.status == "success"
    assert first.category == "weixin"  # run 级盖戳(RunResult.category=config.id)
    records = store.list_items(source=f"weixin-{CHAT}")
    assert len(records) == 2
    assert {record.source for record in records} == {f"weixin-{CHAT}"}
    for record in records:
        # 条目级 category 不盖章:classify.builtin=false 下 store category=None
        # —— telegram-web.yaml 同构(TG 线判例);feed 渠道判定走源名前缀
        # (WEIXIN_SOURCE_RE)+ health() 词表,零依赖 items.category。
        assert record.category is None
        assert ANCHOR_RE.match(record.url)
        assert record.dedup_key == record.url  # {url} 模板渲染锚全串
    # localdb 二源条目(source 盖戳 = 源名全称;锚同 #wx- 家族)
    db_records = store.list_items(source="weixin-localdb样例会话")
    assert len(db_records) == 1
    assert ANCHOR_RE_WITH(chat="localdb样例会话").match(db_records[0].url)

    # 同窗重读(同载荷)= 同锚 → dedup 沉默(dedup 表全期在册),零新增
    second = run(pipeline.run())
    assert second.status == "success"
    assert len(store.list_items(source=f"weixin-{CHAT}")) == 2
    assert len(store.list_items(source="weixin-localdb样例会话")) == 1
    store.close()


def test_weixin_yaml_disabled_by_default_no_cron_job():
    """缺省关纪律(telegram-web.yaml 判例):品类在场 ≠ 在跑 —— cron jobs
    是显式注册面;本测试钉死 config/weixin.yaml 不自带任何自动激活钩子
    (该断言面的真源是 cron 侧显式 create_job,这里锁文件语义注释在场)."""
    text = (REPO_ROOT / "config" / "weixin.yaml").read_text(encoding="utf-8")
    assert "缺省关" in text  # 隐私面显式开启纪律的文件级注记


# ---------------------------------------------------------------------------
# sns 通道电池(10-13-wechat-sns-feed;feed 强 id 锚 / notices 主键锚 /
# 水位增量 / 可疑空防御 / 交叉键拒;零真桥零真实数据)
# ---------------------------------------------------------------------------

SNS_ENTRY_ID = "15031476623630930533"


def sns_feed_row(
    *,
    entry_id: str = SNS_ENTRY_ID,
    username: str = "wxid_synthetic00",
    nickname: str | None = "合成昵称",
    create_time: int = 1760000000,
    text: str | None = "合成朋友圈正文",
    media_count: int = 0,
    media_types: list[str] | None = None,
    ref_nickname: str | None = None,
) -> dict[str, Any]:
    """一条桥 sns feed 契约行(合成;桥 sns_query.parse_feed_row 形)."""
    return {
        "id": entry_id,
        "username": username,
        "nickname": nickname,
        "create_time": create_time,
        "text": text,
        "media_count": media_count,
        "media_types": media_types or [],
        "ref_username": None,
        "ref_nickname": ref_nickname,
    }


def sns_notice_row(
    *,
    local_id: int = 247,
    create_time: int = 1760000000,
    type_: str = "like",
    from_nickname: str | None = "合成赞者",
    content: str | None = None,
    is_relative_me: int = 0,
    feed_id: str | None = "-3417398247010987346",
) -> dict[str, Any]:
    """一条桥 sns notices 契约行(合成;feed_id 已是 str——桥侧转好)."""
    return {
        "local_id": local_id,
        "create_time": create_time,
        "type": type_,
        "from_username": "wxid_synthetic_from",
        "from_nickname": from_nickname,
        "feed_id": feed_id,
        "content": content,
        "is_relative_me": is_relative_me,
    }


def sns_payload(mode: str, rows: list[dict[str, Any]], *, parse_errors: int = 0) -> dict[str, Any]:
    """桥 localdb sns 成功载荷(契约形;§2.4)."""
    return {
        "sns": {
            "mode": mode,
            "since_days": 3,
            mode: rows,
            "rows_total": len(rows),
            "parse_errors": parse_errors,
            "domains": {"sns": "ok", "contact": "ok"},
            "copy": {"dir": "/synthetic", "built": [], "kept": []},
        }
    }


def make_sns_engine(
    *,
    feed_kind: Any = None,
    since_days: Any = None,
    store: Any = None,
    name: str = "weixin-朋友圈",
) -> tuple[WechatLocalEngine, FetchContext]:
    """sns 通道引擎构造器(源名默认朋友圈形态;None 键不进 options)."""
    options: dict[str, Any] = {"channel": "sns"}
    if feed_kind is not None:
        options["feed_kind"] = feed_kind
    if since_days is not None:
        options["since_days"] = since_days
    source = make_source(
        name=name,
        engine="wechat_local",
        url=SOURCE_URL,
        engine_options={"wechat_local": options},
    )
    context, _clock = make_context(
        make_client(lambda request: httpx.Response(404)), store=store
    )
    return WechatLocalEngine(source, context), context


def test_sns_options_reject_session_keys():
    """sns 无会话概念:chat/sides/count 声明即拒(静默忽略=谎报配置生效)."""
    for key, value in (("chat", CHAT), ("sides", ["left"]), ("count", 50)):
        engine, _ = make_engine_raw({"channel": "sns", key: value})
        with pytest.raises(FetchError) as excinfo:
            run(engine.fetch())
        assert excinfo.value.error_type == "invalid_engine_options"
        assert key in str(excinfo.value)


def test_sns_rejects_bad_feed_kind_and_since_days():
    engine, _ = make_engine_raw({"channel": "sns", "feed_kind": "bogus"})
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert "feed_kind" in str(excinfo.value)
    engine, _ = make_engine_raw({"channel": "sns", "since_days": 0})
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert "since_days" in str(excinfo.value)


def test_session_channels_reject_feed_kind():
    """反向交叉:pixel/localdb 声明 feed_kind 同拒(sns 专属键)."""
    engine, _ = make_engine_raw({"chat": CHAT, "feed_kind": "feed"})
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert "feed_kind" in str(excinfo.value)


def test_sns_argv_contract_and_watermark(tmp_path, monkeypatch, engine_store):
    """argv 契约:localdb sns feed --since 3d(首拉)→ 水位推进 → 1d(增量)."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            sns_payload("feed", [sns_feed_row()]), calls=calls
        ),
    )
    engine, _ = make_sns_engine(store=engine_store)
    assert len(fetch_items(engine)) == 1
    assert calls[0][1:] == ["localdb", "sns", "feed", "--since", "3d", "--json"]
    baseline = engine_store.get_baseline(wx_engine.watermark_key("weixin-朋友圈"))
    assert baseline is not None and baseline.etag is not None
    engine2, _ = make_sns_engine(store=engine_store)
    fetch_items(engine2)
    assert calls[1][1:] == ["localdb", "sns", "feed", "--since", "1d", "--json"]


def test_sns_notices_argv(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    calls: list[list[str]] = []
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(sns_payload("notices", [sns_notice_row()]), calls=calls),
    )
    engine, _ = make_sns_engine(feed_kind="notices")
    assert len(fetch_items(engine)) == 1
    assert calls[0][1:] == ["localdb", "sns", "notices", "--since", "3d", "--json"]


def test_sns_feed_items_and_strong_anchor(tmp_path, monkeypatch):
    """feed 条目:#wxsns-<id> 强锚(重读恒同);标题回退链;text 空 → 图片占位."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    rows = [
        sns_feed_row(),
        sns_feed_row(entry_id="9002", text=None, media_count=2, media_types=["2", "2"]),
        sns_feed_row(entry_id="9003", text=None, media_count=0),
        sns_feed_row(entry_id="9004", nickname=None),
        "not-a-dict",
    ]
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(sns_payload("feed", rows)),
    )
    engine, _ = make_sns_engine()
    items = fetch_items(engine)
    assert len(items) == 4
    by_id = {item["url"].split("#wxsns-")[1]: item for item in items}
    assert set(by_id) == {SNS_ENTRY_ID, "9002", "9003", "9004"}
    first = by_id[SNS_ENTRY_ID]
    assert first["url"] == f"wechat-local://sns/{SNS_ENTRY_ID}#wxsns-{SNS_ENTRY_ID}"
    assert first["title"] == "合成朋友圈正文"
    assert first["sender"] == "合成昵称"  # nickname 优先,username 回落
    assert first["kind"] == "sns" and first["sns_kind"] == "feed"
    assert first["ts"] == 1760000000
    assert by_id["9002"]["title"] == "[图片×2]"  # 无文本 → 媒体占位
    assert by_id["9003"]["title"] == "[朋友圈动态]"  # 无文本无媒体 → 兜底
    assert by_id["9004"]["sender"] == "wxid_synthetic00"  # nickname 缺 → username
    # 强幂等:同 id 重铸同锚(内容变了锚也不变 —— id 锚非内容锚)
    assert wx_engine.sns_anchor(SNS_ENTRY_ID) == first["url"]


def test_sns_notice_items_neutral_wording(tmp_path, monkeypatch):
    """notices 条目:中性词面(不假设归属);like/comment/未知型三档."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    rows = [
        sns_notice_row(local_id=1, type_="like", from_nickname="赞者"),
        sns_notice_row(local_id=2, type_="comment", content="合成评论内容", from_nickname="评者"),
        sns_notice_row(local_id=3, type_="99", from_nickname=None),
    ]
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(sns_payload("notices", rows)),
    )
    engine, _ = make_sns_engine(feed_kind="notices")
    items = fetch_items(engine)
    assert [i["title"] for i in items] == [
        "赞者 赞了朋友圈动态",
        "评者 评论了朋友圈动态:合成评论内容",
        "wxid_synthetic_from 互动(99)朋友圈动态",
    ]
    assert items[0]["url"] == "wechat-local://sns/notice/1#wxsnsn-1"
    assert items[0]["content"] == "赞者 赞了朋友圈动态"  # 赞无内容 → 词面句
    assert items[1]["content"] == "合成评论内容"
    assert items[2]["notice_type"] == "99"
    assert items[0]["is_relative_me"] == 0


def test_sns_key_unavailable_skip_no_watermark(tmp_path, monkeypatch, engine_store):
    """密钥缺位 = 结构化 skip(零条目不算失败),水位不推进(localdb 同判例)."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            {"error": {"code": "key_unavailable", "message": "合成缺钥"}},
            exit_code=21,
        ),
    )
    engine, _ = make_sns_engine(store=engine_store)
    assert fetch_items(engine) == []
    assert engine.last_skip_reason == "key_unavailable"
    assert engine_store.get_baseline(wx_engine.watermark_key("weixin-朋友圈")) is None


def test_sns_suspicious_empty_holds_watermark(tmp_path, monkeypatch, engine_store):
    """可疑空防御(grill 决议):feed 零条目 + parse_errors>0 → 水位不推进."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(sns_payload("feed", [], parse_errors=37)),
    )
    engine, _ = make_sns_engine(store=engine_store)
    assert fetch_items(engine) == []
    assert engine_store.get_baseline(wx_engine.watermark_key("weixin-朋友圈")) is None
    # 对照:安静空窗(parse_errors=0)照常推进
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(sns_payload("feed", [], parse_errors=0)),
    )
    engine2, _ = make_sns_engine(store=engine_store)
    fetch_items(engine2)
    assert engine_store.get_baseline(wx_engine.watermark_key("weixin-朋友圈")) is not None


def test_sns_error_family_passthrough(tmp_path, monkeypatch):
    """桥具名错误族透传(decrypt_failed 同 localdb 纪律)."""
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(
            {"error": {"code": "decrypt_failed", "message": "合成解密失败"}},
            exit_code=22,
        ),
    )
    engine, _ = make_sns_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "decrypt_failed"


def test_sns_timeout_and_missing_payload_shape(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(raise_timeout=True),
    )
    engine, _ = make_sns_engine()
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "bridge_timeout"
    # 旧桥(0.5.x)应答无 sns 节 → bridge_error + 升级指引
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner({"messages": []}),
    )
    engine2, _ = make_sns_engine()
    with pytest.raises(FetchError) as excinfo2:
        run(engine2.fetch())
    assert excinfo2.value.error_type == "bridge_error"
    assert "0.6.0" in str(excinfo2.value)


def test_sns_timeout_default_600(tmp_path, monkeypatch):
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    seen: dict[str, float] = {}

    def _runner(argv, input_text, timeout):
        seen["timeout"] = timeout
        return 0, json.dumps(sns_payload("feed", []), ensure_ascii=False), ""

    monkeypatch.setattr(wx_engine, "run_bridge_command_sync", _runner)
    engine, _ = make_sns_engine()
    fetch_items(engine)
    assert seen["timeout"] == wx_engine.DEFAULT_LOCALDB_TIMEOUT_SECONDS == 600.0


def test_sns_feed_media_wording_by_evidenced_types(tmp_path, monkeypatch):
    """grill 深化批:media type 语义实证(2=图/6=视频)后的词面回退链.

    纯视频动态不再误标「图片」;混合形态双计;无媒体兜底不变。
    """
    monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
    rows = [
        sns_feed_row(entry_id="v1", text=None, media_count=2, media_types=["6", "6"]),
        sns_feed_row(entry_id="m1", text=None, media_count=3, media_types=["2", "6", "2"]),
        sns_feed_row(entry_id="i1", text=None, media_count=1, media_types=["2"]),
        sns_feed_row(entry_id="n1", text=None, media_count=0, media_types=[]),
    ]
    monkeypatch.setattr(
        wx_engine,
        "run_bridge_command_sync",
        fake_runner(sns_payload("feed", rows)),
    )
    engine, _ = make_sns_engine()
    items = fetch_items(engine)
    titles = {i["url"].split("#wxsns-")[1]: i["title"] for i in items}
    assert titles["v1"] == "[视频×2]"
    assert titles["m1"] == "[图片×2·视频×1]"
    assert titles["i1"] == "[图片×1]"
    assert titles["n1"] == "[朋友圈动态]"
