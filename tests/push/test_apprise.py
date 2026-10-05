"""Tests for 10-05-push-apprise — apprise 适配器(统一推送,extras 可选依赖)。

覆盖(prd 验收 2 的六用例;apprise 库经 sys.modules 注入假模块——
crawl4ai/trafilatura 先例,零真外发):

①URL 串多目标解析:逗号/换行混合分隔 → add 逐目标调用 + 一次 notify 广播;
②明文 target 拒:发送期零 apprise 触碰零外发(schema 加载期另有拒载用例);
③env/keychain 引用解析:env 命中 / env 缺失回退钥匙链规范名 myia/push/APPRISE_URL;
④未装 → 结构化 apprise_unavailable 带安装命令 + doctor finding
  apprise_not_installed 带安装命令(配了才披露,未配置用户零打扰);
⑤notify 失败透传不吞:notify 返回 False / add 拒目标(错误只报序号不报内容);
⑥标题/正文映射:title=card_title 跨通道一致,body=bark 同款「▸ 标题 · URL」。

另附 schema 面:literal 增员且不进 CHANNEL_PLATFORMS、配 targets 即拒、
明文 target 加载期拒、最小条目加载;管线下传接线(_build_channel 把 target
送达构造——apprise 无通道专属可选字段,kwargs 走 target/template 通用路);
parse_targets 单元(混合分隔/全空)。

No pytest-asyncio in dev deps: async calls run through ``asyncio.run``
(同 test_bark.py 约定)。
"""

from __future__ import annotations

import asyncio
import sys
import types
from typing import Any

import pytest

from myssia import secrets as secrets_store
from myssia.push import AppriseChannel, SendContext
from myssia.push.apprise import (
    INSTALL_COMMAND,
    parse_targets,
)
from myssia.push.base import PushSendError
from myssia.push.feishu_card import card_title
from myssia.schema import LoadError, load_category

CONTEXT = SendContext(slot="am", date="2026-10-05", category="羊毛", kind="digest")


# ---------------------------------------------------------------------------
# Fake apprise(sys.modules 注入;通道对包的全部消费面 = Apprise().add/notify)
# ---------------------------------------------------------------------------


def install_fake_apprise(
    monkeypatch: pytest.MonkeyPatch,
    *,
    reject_at: int | None = None,
    notify_result: bool = True,
    notify_raises: Exception | None = None,
) -> list[Any]:
    """注入假 ``apprise`` 模块;返回 Apprise 实例记录器(逐 send 单例)。

    ``reject_at``:第 N 个 add 调用返回 False(Apprise 拒收该目标)。
    """
    instances: list[Any] = []

    class FakeApprise:
        def __init__(self) -> None:
            self.added: list[str] = []
            self.notify_calls: list[dict[str, str]] = []
            instances.append(self)

        def add(self, url: str) -> bool:
            self.added.append(url)
            return len(self.added) != reject_at

        def notify(self, *, title: str, body: str) -> bool:
            self.notify_calls.append({"title": title, "body": body})
            if notify_raises is not None:
                raise notify_raises
            return notify_result

    module = types.ModuleType("apprise")
    module.Apprise = FakeApprise
    monkeypatch.setitem(sys.modules, "apprise", module)
    return instances


@pytest.fixture(autouse=True)
def _memory_keychain():
    """每用例独立 InMemory 钥匙链(env 缺失回退路径可测);用毕复位。"""
    secrets_store.set_backend(secrets_store.InMemoryKeychainBackend())
    yield
    secrets_store.reset_backend()


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def _data(**overrides: Any) -> dict:
    base = {
        "id": "demo",
        "name": "Demo",
        "schedule": "0 9 * * *",
        "sources": [{"name": "example", "url": "https://example.com/list?page={page}"}],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# 六用例:发送路径(mock apprise;prd 验收 2)
# ---------------------------------------------------------------------------


class TestAppriseSend:
    def test_multi_target_string_parsed_and_notified_once(self, monkeypatch):
        """①逗号/换行混合目标串:add 逐目标 3 次调用,一次 notify 广播。"""
        instances = install_fake_apprise(monkeypatch)
        monkeypatch.setenv(
            "APPRISE_URL",
            "json://sink.local/a, pushover://u:t\n\nbark://key/DEFAULT",
        )
        channel = AppriseChannel(target="env:APPRISE_URL")

        _run(channel.send([{"title": "羊毛", "url": "https://x/1"}], CONTEXT))

        assert len(instances) == 1  # 每次 send 一个 Apprise 单例
        assert instances[0].added == [
            "json://sink.local/a",
            "pushover://u:t",
            "bark://key/DEFAULT",
        ]
        assert len(instances[0].notify_calls) == 1  # 一次广播到全部目标

    def test_plaintext_target_refused_without_touching_apprise(self, monkeypatch):
        """②明文目标串拒(invalid_credential_ref),零 apprise 实例零外发。"""
        instances = install_fake_apprise(monkeypatch)
        channel = AppriseChannel(target="json://sink.local/secret-token")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "invalid_credential_ref"
        # 铁律:凭据问题零外发,错误文案不带目标串值
        assert "secret-token" not in str(excinfo.value)
        assert instances == []  # 未触碰 apprise

    def test_keychain_fallback_resolves_targets(self, monkeypatch):
        """③env 缺失回退钥匙链规范名 myia/push/APPRISE_URL(设置表单存入位)。"""
        instances = install_fake_apprise(monkeypatch)
        monkeypatch.delenv("APPRISE_URL", raising=False)
        secrets_store.set_secret("myia/push/APPRISE_URL", "json://sink.local/kc")
        channel = AppriseChannel()  # 缺省引用 env:APPRISE_URL(可省 target)

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert instances[0].added == ["json://sink.local/kc"]

    def test_not_installed_is_structured_unavailable_and_doctor_finding(
        self, monkeypatch, tmp_path, capsys
    ):
        """④未装:发送期 apprise_unavailable 带安装命令;doctor finding
        apprise_not_installed 带安装命令,且未配置品类零 finding(不惊扰)。"""
        # 发送面:sys.modules 置 None 强制真实 ImportError 分支(crawl4ai 先例)
        monkeypatch.setitem(sys.modules, "apprise", None)
        monkeypatch.setenv("APPRISE_URL", "json://sink.local/a")
        with pytest.raises(PushSendError) as excinfo:
            _run(AppriseChannel(target="env:APPRISE_URL").send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "apprise_unavailable"
        assert INSTALL_COMMAND in str(excinfo.value)  # pip install "myssia[apprise]"

        # doctor 面:配了 apprise 通道的品类 + 未装 → warning finding 带安装命令
        import json

        import myssia.cli as cli_module
        from myssia.cli import EXIT_OK, main
        from myssia.store import SQLiteStore

        monkeypatch.setattr(cli_module, "_package_available", lambda module: False)
        db = tmp_path / "myssia.db"
        SQLiteStore(str(db)).close()
        directory = tmp_path / "plugins"
        directory.mkdir()
        (directory / "apprise-demo.yaml").write_text(
            "id: apprise-demo\nname: Apprise\nschedule: '0 9 * * *'\n"
            "sources:\n  - name: example\n    url: https://example.com/list?page={page}\n"
            "push:\n  - channel: apprise\n    target: env:APPRISE_URL\n",
            encoding="utf-8",
        )
        (directory / "plain.yaml").write_text(
            "id: plain\nname: Plain\nschedule: '0 9 * * *'\n"
            "sources:\n  - name: example\n    url: https://example.com/list?page={page}\n",
            encoding="utf-8",
        )
        assert main(["doctor", "--plugins-dir", str(directory), "--db", str(db), "--json"]) == EXIT_OK
        payload = json.loads(capsys.readouterr().out)
        codes = [f["code"] for f in payload["findings"]]
        assert "apprise_not_installed" in codes
        finding = next(f for f in payload["findings"] if f["code"] == "apprise_not_installed")
        assert finding["severity"] == "warning"  # 缺装不是配置错,不翻 healthy
        assert payload["healthy"] is True
        assert "apprise-demo" in finding["message"]
        assert INSTALL_COMMAND in finding["message"]
        assert 'uv sync --extra apprise' in finding["message"]

        # 不惊扰:未配置 apprise 的品类零 finding(没配该通道 = 正常态)。
        assert main(["doctor", str(directory / "plain.yaml"), "--db", str(db), "--json"]) == EXIT_OK
        payload = json.loads(capsys.readouterr().out)
        assert not any(f["code"] == "apprise_not_installed" for f in payload["findings"])

    def test_notify_failure_passthrough_not_swallowed(self, monkeypatch):
        """⑤notify 返回 False / add 拒目标:结构化透传;错误只报序号不报内容。"""
        # 5a:notify 返回 False(Apprise 某目标拒绝/不可达)
        instances = install_fake_apprise(monkeypatch, notify_result=False)
        monkeypatch.setenv("APPRISE_URL", "json://sink.local/a")
        with pytest.raises(PushSendError) as excinfo:
            _run(AppriseChannel(target="env:APPRISE_URL").send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "apprise_notify_failed"

        # 5b:第 2 个目标不被 Apprise 接受 → 序号文案,目标串值不进文案
        instances = install_fake_apprise(monkeypatch, reject_at=2)
        monkeypatch.setenv("APPRISE_URL", "json://sink.local/a,json://bad/形态")
        with pytest.raises(PushSendError) as excinfo:
            _run(AppriseChannel(target="env:APPRISE_URL").send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "apprise_target_invalid"
        assert "2/2" in str(excinfo.value)  # 序号可定位
        assert "json://bad" not in str(excinfo.value)  # 目标串含凭据,永不进文案
        assert instances[-1].notify_calls == []  # fail-fast:不半推

    def test_title_body_mapping(self, monkeypatch):
        """⑥title=card_title 跨通道一致;body=bark 同款「▸ 标题 · URL」行。"""
        instances = install_fake_apprise(monkeypatch)
        monkeypatch.setenv("APPRISE_URL", "json://sink.local/a")
        context = SendContext(slot="pm", date="2026-10-06", category="羊毛", kind="digest")
        items = [
            {"title": "A 标题", "url": "https://x/1"},
            {"title": "B 标题"},  # 无 URL 条目:不带链接尾缀
        ]

        _run(AppriseChannel(target="env:APPRISE_URL").send(items, context))

        call = instances[0].notify_calls[0]
        assert call["title"] == card_title(context)
        assert "A 标题 · https://x/1" in call["body"]
        assert "B 标题" in call["body"]


# ---------------------------------------------------------------------------
# schema 两用例 + 加载期门(prd 验收 1)
# ---------------------------------------------------------------------------


class TestAppriseSchema:
    def test_apprise_in_vocabulary_but_not_targeting(self):
        """literal 增员:apprise ∈ PUSH_CHANNELS;∉ CHANNEL_PLATFORMS(同 webhook/bark)。"""
        from myssia.schema import CHANNEL_PLATFORMS, PUSH_CHANNELS

        assert "apprise" in PUSH_CHANNELS
        assert "apprise" not in CHANNEL_PLATFORMS  # 配 targets 即拒的表驱动来源

    def test_apprise_targets_rejected_at_load(self):
        """apprise 配 targets 即拒(目标=URL 串无目录语义;fail-fast 于配置)。"""
        with pytest.raises(LoadError) as excinfo:
            load_category(_data(push=[{
                "channel": "apprise",
                "target": "env:APPRISE_URL",
                "targets": ["apprise:phone"],
            }]))
        assert any(d.error_type == "targeting_not_supported" for d in excinfo.value.errors)

    def test_plaintext_target_rejected_at_load(self):
        """明文目标串(URL 含 token)加载期即拒——全通道凭据红线。"""
        with pytest.raises(LoadError) as excinfo:
            load_category(_data(push=[{
                "channel": "apprise",
                "target": "json://sink.local/secret",
            }]))
        assert any(d.error_type == "credential_plaintext" for d in excinfo.value.errors)

    def test_minimal_entry_loads_and_target_lands(self):
        """最小条目加载;target 引用原样落位(解析在发送期)。"""
        cfg = load_category(_data(push=[{"channel": "apprise", "target": "env:APPRISE_URL"}]))
        assert cfg.push[0].channel == "apprise"
        assert cfg.push[0].target == "env:APPRISE_URL"


# ---------------------------------------------------------------------------
# 管线下传接线:target 经真实 _build_channel 到达通道构造参数(kwargs 通用路)
# ---------------------------------------------------------------------------


def test_build_channel_wires_target(tmp_path):
    """apprise 无通道专属可选字段:target 走 _build_channel 通用下传路。"""
    import httpx

    from myssia.pipeline import Pipeline
    from myssia.store import SQLiteStore

    cfg = load_category(_data(push=[{"channel": "apprise", "target": "env:APPRISE_URL"}]))
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
        assert isinstance(channel, AppriseChannel)
        assert channel._target == "env:APPRISE_URL"
    finally:
        pipeline.close()


# ---------------------------------------------------------------------------
# parse_targets 单元:混合分隔 / 全空(发送期拒空串的判据)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("json://a", ["json://a"]),
        ("a,b", ["a", "b"]),
        ("a\nb", ["a", "b"]),
        ("a,\nb\r\nc, ,d", ["a", "b", "c", "d"]),
        ("  ", []),
        ("", []),
    ],
)
def test_parse_targets_separator_matrix(raw, expected):
    assert parse_targets(raw) == expected
