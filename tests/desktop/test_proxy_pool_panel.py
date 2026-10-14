"""代理池管理面板 sidecar 面(task 10-14-proxy-pool-panel R5)。

覆盖 ``src/myssia/proxy_panel.py``(proxy.probe / proxy.history 两方法的
实现本体;entry.py 注册接线见任务档 integrationSpec,本件先以
monkeypatch.setitem 注入同款 handler 全链路验证——集成后逐字节同径):

- 纯读面:limit 钳制/缺省、pool 过滤、坏行跳过(skipped 如实)、
  文件不存在空表、dev 无 home(home_available=false);
- 落盘面:探测后恰一行 {at,config,pools}(pools 行打码)、保留帽 200
  裁最旧、文件 0600、write_failed / no_home / no_proxy_section 降级
  (探测结果照回不 fail);
- e2e:serve 全链路经 rpc() 往返(真实 doctor,零外网——env 缺失凭据
  上游解析在探测前失败隔离成行,同 G10 AC1 手法)。
"""

from __future__ import annotations

import importlib.util
import io
import json
import logging
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from myssia import log as myssia_log
from myssia import proxy_panel

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRY_PATH = REPO_ROOT / "desktop" / "entry.py"

_spec = importlib.util.spec_from_file_location("desktop_entry_proxy_panel", ENTRY_PATH)
entry = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(entry)

#: env 缺失凭据上游(G10 AC1 同款夹具:resolve_upstreams 在探测前抛错,
#: 零外网;顶层必须带 pools: 包装——fetch_base.py:831 裸池名静默合法空表)。
POOLS_YAML_UNRESOLVED = """
pools:
  main:
    upstreams:
      - "http://env:MYIA_PROBE_TEST_MISSING@127.0.0.1:9"
"""

FIXED_NOW = datetime(2026, 10, 14, 8, 30, 0, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def _isolate_logging_and_env(monkeypatch):
    """日志模块态/env 隔离(既有 sidecar 套件同款纪律的子集)。

    doctor 经 entry._cli_json 在本进程内跑,会重配 root logging 到 serve
    形态——不隔离会泄漏到同会话邻域测试文件;MYIA_HOME 摘除保证
    dev 回退是默认前提。
    """
    monkeypatch.delenv("MYIA_HOME", raising=False)
    monkeypatch.delenv("MYIA_PLUGIN_DIR", raising=False)
    saved_handlers = logging.getLogger().handlers[:]
    saved_factory = logging.getLogRecordFactory()
    myssia_log._reset_module_state()
    yield
    myssia_log._reset_module_state()
    logging.getLogger().handlers[:] = saved_handlers
    logging.setLogRecordFactory(saved_factory)


def rpc(*requests: dict) -> tuple[int, list[dict], list[dict]]:
    """整轮 RPC(与既有 sidecar 套件同款:serve → 按有无 id 拆应答/事件)。"""
    stdin = io.StringIO("".join(json.dumps(req, ensure_ascii=False) + "\n" for req in requests))
    out = io.StringIO()
    code = entry.serve(stdin=stdin, stdout=out)
    responses: list[dict] = []
    events: list[dict] = []
    for line in out.getvalue().splitlines():
        obj = json.loads(line)
        (responses if "id" in obj else events).append(obj)
    return code, responses, events


def install_handlers(monkeypatch: pytest.MonkeyPatch, **overrides: Any) -> None:
    """把工厂产出的两 handler 注入 entry._HANDLERS(= 集成接线同径)。"""
    handlers = proxy_panel.make_proxy_panel_handlers(
        doctor=overrides.get("doctor", entry._m_doctor),
        home_resolver=overrides.get("home_resolver", lambda: entry._serve_context().home),
        protocol_error=entry.ProtocolError,
        now=overrides.get("now", lambda: FIXED_NOW),
    )
    for method, handler in handlers.items():
        monkeypatch.setitem(entry._HANDLERS, method, handler)


def history_path(home: Path) -> Path:
    return home / proxy_panel.PROBE_HISTORY_FILENAME


def make_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    (home / "pools.yaml").write_text(POOLS_YAML_UNRESOLVED, encoding="utf-8")
    return home


# ---------------------------------------------------------------------------
# 纯读面:read_history / clamp_limit(零 entry 依赖)
# ---------------------------------------------------------------------------


def test_read_history_missing_file_is_legal_empty(tmp_path):
    result = proxy_panel.read_history(tmp_path, limit=20)
    assert result == {
        "snapshots": [],
        "count": 0,
        "truncated": False,
        "home_available": True,
        "skipped": 0,
    }


def test_read_history_dev_home_is_unavailable():
    result = proxy_panel.read_history(None, limit=20)
    assert result["home_available"] is False
    assert result["snapshots"] == [] and result["count"] == 0


def test_read_history_newest_first_bad_lines_skipped(tmp_path):
    path = history_path(tmp_path)
    good_old = {"at": "2026-10-13T00:00:00+00:00", "config": "/a.yaml", "pools": [{"pool": "main", "ok": True}]}
    good_new = {"at": "2026-10-14T00:00:00+00:00", "config": None, "pools": []}
    path.write_text(
        "not json\n"
        + json.dumps(good_old)
        + "\n"
        + json.dumps({"at": 123, "config": None, "pools": []})  # at 非字符串 = 坏行
        + "\n"
        + "\n"  # 空行:静默忽略,不计坏行
        + json.dumps(good_new)
        + "\n",
        encoding="utf-8",
    )
    result = proxy_panel.read_history(tmp_path, limit=20)
    assert [snap["at"] for snap in result["snapshots"]] == [good_new["at"], good_old["at"]]
    assert result["count"] == 2 and result["truncated"] is False
    assert result["skipped"] == 2


def test_read_history_limit_window_and_pool_filter(tmp_path):
    path = history_path(tmp_path)
    rows = [
        {"at": f"2026-10-14T00:0{i}:00+00:00", "config": None,
         "pools": [{"pool": "main", "ok": i % 2 == 0}, {"pool": "backup", "ok": False}]}
        for i in range(5)
    ]
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
    windowed = proxy_panel.read_history(tmp_path, limit=3)
    assert windowed["count"] == 3 and windowed["truncated"] is True
    assert windowed["snapshots"][0]["at"] == rows[-1]["at"]  # 新→旧
    assert windowed["snapshots"][0]["pools"] == rows[-1]["pools"]  # 无 pool 过滤 = 原行整包

    only_main = proxy_panel.read_history(tmp_path, limit=20, pool="main")
    assert only_main["count"] == 5
    for snap in only_main["snapshots"]:
        assert [row["pool"] for row in snap["pools"]] == ["main"]

    absent = proxy_panel.read_history(tmp_path, limit=20, pool="nonexistent")
    assert absent["snapshots"] == [] and absent["count"] == 0


def test_clamp_limit_window():
    assert proxy_panel.clamp_limit(0) == 1
    assert proxy_panel.clamp_limit(1000) == 100
    assert proxy_panel.clamp_limit(50) == 50


# ---------------------------------------------------------------------------
# 落盘面:append_snapshot(0600 / 保留帽 200 / 打码随行)
# ---------------------------------------------------------------------------


def test_append_snapshot_creates_mode_600_and_keeps_shape(tmp_path):
    snapshot = {
        "at": "2026-10-14T08:30:00+00:00",
        "config": str(tmp_path / "pools.yaml"),
        "pools": [{"pool": "main", "ok": False, "proxy_url": "http://***@127.0.0.1:9"}],
    }
    proxy_panel.append_snapshot(tmp_path, snapshot)
    path = history_path(tmp_path)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == snapshot


def test_append_snapshot_trims_to_keep_max(tmp_path):
    for index in range(proxy_panel.HISTORY_KEEP_MAX + 5):
        proxy_panel.append_snapshot(
            tmp_path,
            {"at": f"2026-10-14T00:00:{index:02d}+00:00", "config": None, "pools": []},
        )
    lines = history_path(tmp_path).read_text(encoding="utf-8").splitlines()
    assert len(lines) == proxy_panel.HISTORY_KEEP_MAX
    # 裁的是最旧:首行 = 第 6 条(index 5)
    assert json.loads(lines[0])["at"] == "2026-10-14T00:00:05+00:00"
    assert stat.S_IMODE(history_path(tmp_path).stat().st_mode) == 0o600


# ---------------------------------------------------------------------------
# handler 直调:降级三态(探测结果照回不 fail)+ 参数门
# ---------------------------------------------------------------------------


def doctor_payload(_params: dict | None = None) -> dict[str, Any]:
    return {
        "command": "doctor",
        "exit_code": 0,
        "healthy": True,
        "proxy": {
            "config": "/x/pools.yaml",
            "pools": [{"pool": "main", "ok": True, "proxy_url": "http://***@h:1", "exit_ip": "1.2.3.4"}],
        },
    }


def direct_handlers(**overrides: Any) -> dict[str, Any]:
    return proxy_panel.make_proxy_panel_handlers(
        doctor=overrides.get("doctor", doctor_payload),
        home_resolver=overrides.get("home_resolver", lambda: None),
        protocol_error=entry.ProtocolError,
        now=lambda: FIXED_NOW,
    )


def test_probe_no_home_degrades_not_fail():
    result = direct_handlers()["proxy.probe"]({})
    assert result["exit_code"] == 0  # doctor 原形状照回
    assert result["snapshot"] == {"persisted": False, "reason": "no_home"}


def test_probe_write_failed_degrades(tmp_path, monkeypatch):
    def boom(home: Path, snapshot: dict) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(proxy_panel, "append_snapshot", boom)
    result = direct_handlers(home_resolver=lambda: tmp_path)["proxy.probe"]({})
    assert result["snapshot"]["persisted"] is False
    assert result["snapshot"]["reason"].startswith("write_failed")


def test_probe_no_proxy_section_degrades(tmp_path):
    result = direct_handlers(
        doctor=lambda params: {"exit_code": 0}, home_resolver=lambda: tmp_path
    )["proxy.probe"]({})
    assert result["snapshot"] == {"persisted": False, "reason": "no_proxy_section"}


def test_history_param_gates():
    handlers = direct_handlers()
    with pytest.raises(entry.ProtocolError) as exc:
        handlers["proxy.history"]({"limit": "5"})
    assert exc.value.code == "invalid_params" and exc.value.path == "params.limit"
    with pytest.raises(entry.ProtocolError) as exc:
        handlers["proxy.history"]({"limit": True})  # bool 不是计数
    assert exc.value.path == "params.limit"
    with pytest.raises(entry.ProtocolError) as exc:
        handlers["proxy.history"]({"pool": 123})
    assert exc.value.path == "params.pool"
    with pytest.raises(entry.ProtocolError) as exc:
        handlers["proxy.history"]({"pool": ""})
    assert exc.value.path == "params.pool"


# ---------------------------------------------------------------------------
# e2e:serve 全链路(真实 doctor,零外网;handler 注入 = 集成接线同径)
# ---------------------------------------------------------------------------


def test_probe_persists_masked_snapshot_via_serve(tmp_path, monkeypatch):
    """PRD R5.1 原方:env 缺失凭据上游 → 解析失败兜底行(零外网构造)。

    实证补充:兜底行 message 含 env **引用名**(『环境变量 MYIA_PROBE_…
    未设置』)——引用名非凭据值(该 env 根本未设置),是 doctor 既有
    语义(settings 屏今天同款显示),快照原样存档不篡改。
    """
    home = make_home(tmp_path)
    monkeypatch.setenv("MYIA_HOME", str(home))
    install_handlers(monkeypatch)
    code, responses, _ = rpc({"id": 1, "method": "proxy.probe", "params": {"config_auto": True}})
    assert code == 0
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    assert result["proxy"]["config"] == str(home / "pools.yaml")
    assert result["snapshot"] == {"persisted": True}

    path = history_path(home)
    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    snapshot = json.loads(lines[0])
    assert snapshot["at"] == FIXED_NOW.isoformat(timespec="milliseconds")
    assert snapshot["config"] == str(home / "pools.yaml")
    row = snapshot["pools"][0]
    assert row["pool"] == "main" and row["ok"] is False
    assert "无法解析" in row["message"]
    assert row["proxy_url"] == "http://***@127.0.0.1:9"  # 打码随行(红线 4)
    assert stat.S_IMODE(path.stat().st_mode) == 0o600


def test_probe_persists_no_credential_value_via_serve(tmp_path, monkeypatch):
    """红线 4 强式:凭据**值**在时(解析成功 → 探测走环回死代理,连接拒绝,
    零外网)——落盘行只见打码 URL,凭据值永不入文件。"""
    home = make_home(tmp_path)
    monkeypatch.setenv("MYIA_HOME", str(home))
    monkeypatch.setenv("MYIA_PROBE_TEST_MISSING", "s3cret-value-7f3a")
    install_handlers(monkeypatch)
    code, responses, _ = rpc(
        {"id": 1, "method": "proxy.probe", "params": {"config_auto": True, "probe_timeout": 3}}
    )
    assert code == 0
    result = responses[0]["result"]
    assert result["snapshot"] == {"persisted": True}
    row = result["proxy"]["pools"][0]
    assert row["proxy_url"] == "http://***@127.0.0.1:9"  # 值在也只回打码
    file_text = history_path(home).read_text(encoding="utf-8")
    assert "s3cret-value-7f3a" not in file_text  # 凭据值永不落盘
    assert "http://***@127.0.0.1:9" in file_text


def test_probe_config_auto_gate_inherited_from_doctor(monkeypatch):
    install_handlers(monkeypatch)
    code, responses, _ = rpc({"id": 1, "method": "proxy.probe", "params": {"config_auto": "yes"}})
    error = responses[0]["error"]
    assert error["code"] == "invalid_params" and error["path"] == "params.config_auto"


def test_probe_dev_no_home_via_serve(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config").mkdir()
    install_handlers(monkeypatch)
    code, responses, _ = rpc({"id": 1, "method": "proxy.probe", "params": {"config_auto": True}})
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    assert result["proxy"]["config"] is None and result["proxy"]["pools"] == []
    assert result["snapshot"] == {"persisted": False, "reason": "no_home"}


def test_history_roundtrip_via_serve(tmp_path, monkeypatch):
    home = make_home(tmp_path)
    monkeypatch.setenv("MYIA_HOME", str(home))
    install_handlers(monkeypatch)
    _, responses, _ = rpc({"id": 1, "method": "proxy.probe", "params": {"config_auto": True}})
    assert responses[0]["result"]["snapshot"]["persisted"] is True

    _, responses, _ = rpc({"id": 2, "method": "proxy.history", "params": {}})
    result = responses[0]["result"]
    assert result["count"] == 1 and result["truncated"] is False
    assert result["home_available"] is True
    assert result["snapshots"][0]["pools"][0]["pool"] == "main"

    _, responses, _ = rpc({"id": 3, "method": "proxy.history", "params": {"pool": "main"}})
    assert responses[0]["result"]["pool"] == "main"
    _, responses, _ = rpc({"id": 4, "method": "proxy.history", "params": {"pool": "absent"}})
    assert responses[0]["result"]["snapshots"] == []

    # 坏行跳过:skipped 如实,好行照回
    with history_path(home).open("a", encoding="utf-8") as handle:
        handle.write("garbage\n")
    _, responses, _ = rpc({"id": 5, "method": "proxy.history", "params": {}})
    result = responses[0]["result"]
    assert result["count"] == 1 and result["skipped"] == 1


def test_history_limit_clamped_via_serve(tmp_path, monkeypatch):
    home = make_home(tmp_path)
    monkeypatch.setenv("MYIA_HOME", str(home))
    for index in range(4):
        proxy_panel.append_snapshot(
            home, {"at": f"2026-10-14T00:0{index}:00+00:00", "config": None, "pools": []}
        )
    install_handlers(monkeypatch)
    _, responses, _ = rpc({"id": 1, "method": "proxy.history", "params": {"limit": 0}})
    assert responses[0]["result"]["count"] == 1 and responses[0]["result"]["truncated"] is True
    _, responses, _ = rpc({"id": 2, "method": "proxy.history", "params": {"limit": 999}})
    assert responses[0]["result"]["count"] == 4 and responses[0]["result"]["truncated"] is False


def test_history_missing_file_empty_via_serve(tmp_path, monkeypatch):
    home = make_home(tmp_path)
    monkeypatch.setenv("MYIA_HOME", str(home))
    install_handlers(monkeypatch)
    _, responses, _ = rpc({"id": 1, "method": "proxy.history", "params": {}})
    result = responses[0]["result"]
    assert result["snapshots"] == [] and result["count"] == 0 and result["truncated"] is False
    assert result["home_available"] is True


def test_handlers_install_is_isolated(monkeypatch):
    """注入不外漏:teardown 后两方法回到模块级真实接线件(对账例不被本件污染)。

    集成员接线后(10-14-proxy-pool-panel R1)``_HANDLERS`` 字面量已含
    proxy.probe/proxy.history:monkeypatch.setitem 的还原语义 = 回到模块
    装载时的 ``_PROXY_PANEL`` 产物(不再是本件注入的定轴 now 版本)。
    计数不写死 95/96(批序漂移坑:本例曾硬编码 95,cred-hunter-panel 批
    +1 后全场门禁红):安装前后取模块级基线对回,只证「本件零污染」。
    """
    before = dict(entry._HANDLERS)
    install_handlers(monkeypatch)
    assert "proxy.probe" in entry._HANDLERS and "proxy.history" in entry._HANDLERS
    injected_probe = entry._HANDLERS["proxy.probe"]
    monkeypatch.undo()
    assert "proxy.probe" in entry._HANDLERS and "proxy.history" in entry._HANDLERS
    assert entry._HANDLERS["proxy.probe"] is not injected_probe
    assert entry._HANDLERS["proxy.probe"] is entry._PROXY_PANEL["proxy.probe"]
    assert entry._HANDLERS["proxy.history"] is entry._PROXY_PANEL["proxy.history"]
    assert entry._HANDLERS == before
