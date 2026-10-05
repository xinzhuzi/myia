"""desktop/entry.py sidecar 协议单测(mock stdin/stdout,全方法往返)。

覆盖:10 个方法的请求→应答往返、流式事件(log/progress/completed 以 type
区分)、错误结构化透传(code/path/message)、退出码语义(serve EOF=0;run
子进程 0/1/2 原样透传;直通模式 0/1)。零外网:成功 run 走 127.0.0.1 本地
http.server(安全底线明示例外);凭据方法 monkeypatch,不触碰真实钥匙链。
"""

from __future__ import annotations

import http.server
import importlib.util
import io
import json
import shutil
import socketserver
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path
from typing import Any

import pytest

from myssia.secrets import InMemoryKeychainBackend
from myssia.store import SQLiteStore

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRY_PATH = REPO_ROOT / "desktop" / "entry.py"

_spec = importlib.util.spec_from_file_location("desktop_entry", ENTRY_PATH)
entry = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(entry)


VALID_YAML = """
id: proto-demo
name: 协议夹具品类
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:{port}/list"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.data[*].title"
        url: "$.data[*].url"
classify:
  builtin: false   # 夹具条目不属于七大类,直通(同 desktop/fixture 惯例)
push:
  - channel: stdout
"""

BAD_CRON_YAML = """
id: proto-bad
name: 非法 cron
schedule: "not-a-cron"
sources:
  - name: api
    engine: direct_api
    url: "http://127.0.0.1:9/x"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.a"
        url: "$.b"
"""

API_JSON = {"data": [{"title": "协议条目一", "url": "https://example.com/p1"},
                     {"title": "协议条目二", "url": "https://example.com/p2"}]}


# ---------------------------------------------------------------------------
# 夹具与助手
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_sidecar_state(monkeypatch):
    """每个测试独立的 sidecar 内存态(run 注册表/日志环/钥匙链后端)。"""
    monkeypatch.setattr(entry, "_RUNS", {})
    monkeypatch.setattr(entry, "_ACTIVE_RUN_ID", None)
    monkeypatch.setattr(entry, "_NEXT_RUN_ID", 0)
    monkeypatch.setattr(entry, "_RUN_PROCS", {})
    monkeypatch.setattr(entry, "_CANCEL_TIMERS", [])
    monkeypatch.setattr(entry, "_TEST_ACTIVE_JOB", None)
    monkeypatch.setattr(entry, "_TEST_NEXT_JOB_ID", 0)
    monkeypatch.setattr(entry, "_MODELS_DL_ACTIVE_JOB", None)
    monkeypatch.setattr(entry, "_MODELS_DL_NEXT_JOB_ID", 0)
    monkeypatch.setattr(entry, "_LOG_RING", deque(maxlen=entry.LOG_RING_CAPACITY))
    monkeypatch.setattr(entry, "_LOG_SEQ", 0)
    # v1.1.1 上下文隔离:ambient MYIA_HOME 不得影响任何用例(dev 模式是默认前提)
    monkeypatch.delenv("MYIA_HOME", raising=False)
    monkeypatch.delenv("MYIA_PLUGIN_DIR", raising=False)
    backend = InMemoryKeychainBackend()

    def fake_delete_secret(name: str) -> None:
        # 与 myssia.secrets.delete_secret 同门:名字校验 → 存在性 → 删除
        from myssia.secrets import SecretError, validate_secret_name

        validate_secret_name(name)
        if backend.get_password("myia", name) is None:
            raise SecretError("secret_not_found", f"系统钥匙链中未找到凭据 {name!r},无法删除")
        backend.delete_password("myia", name)

    monkeypatch.setattr(entry, "set_secret", _capture_secret(backend))
    monkeypatch.setattr(entry, "list_secrets", lambda: sorted(name for _, name in backend._items))
    monkeypatch.setattr(entry, "delete_secret", fake_delete_secret)
    yield
    # hermes-cron 批(10-04-hermes-cron B3):serve 内置 cron ticker 拆线——
    # 置 stop + 有界 join + 模块级句柄复位(ground-truth B12 ⚠️ 防测试线程
    # 泄漏;dev 用例此调用是幂等 no-op,home 模式用例才真正起过线程)。
    entry._stop_cron_ticker()


class _SecretCapture:
    def __init__(self, backend: InMemoryKeychainBackend) -> None:
        self.backend = backend
        self.calls: list[tuple[str, str]] = []


def _capture_secret(backend: InMemoryKeychainBackend):
    capture = _SecretCapture(backend)

    def fake_set_secret(name: str, value: str) -> None:
        capture.calls.append((name, value))
        capture.backend.set_password(entry.SECRET_SERVICE if hasattr(entry, "SECRET_SERVICE") else "myia",
                                     name, value)

    fake_set_secret.capture = capture  # type: ignore[attr-defined]
    return fake_set_secret


def rpc(*requests: dict, raw_lines: list[str] | None = None) -> tuple[int, list[dict], list[dict]]:
    """整轮 RPC:写请求 → serve → 按有无 id 拆应答/事件。"""
    lines = [json.dumps(req, ensure_ascii=False) for req in requests]
    lines += raw_lines or []
    stdin = io.StringIO("".join(line + "\n" for line in lines))
    out = io.StringIO()
    code = entry.serve(stdin=stdin, stdout=out)
    responses: list[dict] = []
    events: list[dict] = []
    for line in out.getvalue().splitlines():
        obj = json.loads(line)
        (responses if "id" in obj else events).append(obj)
    return code, responses, events


def write_yaml(tmp_path: Path, text: str, name: str = "demo.yaml") -> str:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


class _ApiHandler(http.server.BaseHTTPRequestHandler):
    """任意路径回固定 JSON 直 API 夹具(仅 127.0.0.1,零外网)。"""

    def do_GET(self):  # noqa: N802
        body = json.dumps(API_JSON, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # 静默
        pass


@pytest.fixture()
def local_api():
    """临时本地直 API 服务(线程内,ephemeral 端口,测毕关闭)。"""
    with socketserver.TCPServer(("127.0.0.1", 0), _ApiHandler) as srv:
        port = srv.server_address[1]
        thread = threading.Thread(target=srv.serve_forever, daemon=True)
        thread.start()
        yield port
        srv.shutdown()


def split_stream(out: io.StringIO) -> tuple[list[dict], list[dict]]:
    """协议流拆分:有 id = 应答,有 type = 事件(与 spec 的单写锁同步快照)。"""
    with entry._WRITE_LOCK:
        text = out.getvalue()
    responses: list[dict] = []
    events: list[dict] = []
    for line in text.splitlines():
        obj = json.loads(line)
        (responses if "id" in obj else events).append(obj)
    return responses, events


def wait_completed(out: io.StringIO, run_id: int, timeout: float = 60.0) -> dict:
    """等 completed 事件(工作线程异步写 stdout;EOF 后仍在写)。"""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        for obj in split_stream(out)[1]:
            if obj.get("type") == "completed" and obj.get("run_id") == run_id:
                return obj
        time.sleep(0.05)
    raise AssertionError(f"run {run_id} 未在 {timeout}s 内完成")


# ---------------------------------------------------------------------------
# 基础往返:version / health / plugins.list / doctor
# ---------------------------------------------------------------------------


def test_version_roundtrip():
    """version:与 myssia.__version__ 一致,携带协议版本。"""
    import myssia

    code, responses, events = rpc({"id": 1, "method": "version", "params": {}})
    assert code == 0
    assert events == []
    assert responses == [{"id": 1, "result": {"name": "myssia", "version": myssia.__version__,
                                              "protocol": entry.PROTOCOL_VERSION,
                                              "app_version": None}}]


def test_health_roundtrip_with_summary(tmp_path):
    """health:CLI list 同源数据 + 状态计数聚合 + healthy。"""
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    (plugins_dir / "demo.yaml").write_text(
        VALID_YAML.replace("{port}", "9"), encoding="utf-8"
    )
    db = tmp_path / "myssia.db"
    code, responses, _ = rpc({"id": 7, "method": "health",
                              "params": {"plugins_dir": str(plugins_dir), "db": str(db)}})
    assert code == 0
    result = responses[0]["result"]
    assert "error" not in responses[0]
    assert result["exit_code"] == 0
    assert result["healthy"] is True
    assert result["summary"]["plugins"] == 1
    assert result["summary"]["unknown"] == 1  # 无运行记录 → unknown(非 dead)
    plugin = result["plugins"][0]
    assert plugin["loaded"] is True
    assert plugin["sources"][0]["health"]["state"] == "unknown"


def test_health_missing_dir_structured_error(tmp_path):
    """health:目录不存在 → CLI 错误结构化透传(code=path/message 落位)。"""
    code, responses, _ = rpc({"id": 1, "method": "health",
                              "params": {"plugins_dir": str(tmp_path / "nope")}})
    assert code == 0  # serve 进程不因单请求错误退出
    error = responses[0]["error"]
    assert error["code"] == "plugins_dir"
    assert "message" in error and error["path"] == "$"
    assert error["data"]["error"] == "plugins_dir"


def test_plugins_list_roundtrip(tmp_path):
    """plugins.list:缺失安装根 = 空清单正常态(exit_code 0,与 CLI 语义一致)。"""
    code, responses, _ = rpc({"id": 2, "method": "plugins.list",
                              "params": {"dir": str(tmp_path / "no-root")}})
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    assert result["plugins"] == []
    assert result["summary"]["installed"] == 0


def test_doctor_roundtrip(tmp_path):
    """doctor:完成即 0,findings 全量随行,healthy 视角与 CLI 一致。"""
    yaml_path = write_yaml(tmp_path, VALID_YAML.replace("{port}", "9"))
    db = tmp_path / "myssia.db"
    code, responses, _ = rpc({"id": 3, "method": "doctor",
                              "params": {"yamls": [yaml_path], "db": str(db)}})
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    assert result["healthy"] is True
    assert result["plugins"][0]["id"] == "proto-demo"
    assert isinstance(result["findings"], list)


# ---------------------------------------------------------------------------
# doctor config_auto(G10 10-05-g10-proxy-probe:免手填一键化;零外网——命中例
# 用 env 缺失凭据上游,解析在探测前失败隔离成行,同 test_proxy_pool.py 手法)
# ---------------------------------------------------------------------------

POOLS_YAML_UNRESOLVED = """
pools:
  main:
    upstreams:
      - "http://env:MYIA_PROBE_TEST_MISSING@127.0.0.1:9"
"""


def test_doctor_config_auto_discovers_home_pools_yaml(tmp_path, monkeypatch):
    """config_auto 命中:MYIA_HOME 置 pools.yaml → 自动拼 --config,路径经既有
    proxy.config 键回显(零新应答键),逐池行真跑(缺凭据 → 解析失败行)。"""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("MYIA_HOME", str(home))
    (home / "pools.yaml").write_text(POOLS_YAML_UNRESOLVED, encoding="utf-8")
    code, responses, _ = rpc({"id": 1, "method": "doctor", "params": {"config_auto": True}})
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    proxy = result["proxy"]
    assert proxy["config"] == str(home / "pools.yaml")
    assert len(proxy["pools"]) == 1
    row = proxy["pools"][0]
    assert row["pool"] == "main" and row["ok"] is False
    assert "无法解析" in row["message"]
    # 解析失败(credential_unresolved)= error 级 finding,doctor 仍完成即 0
    assert any(item["scope"] == "proxy:main" for item in result["findings"])


def test_doctor_config_auto_miss_and_dev_fallback(tmp_path, monkeypatch):
    """config_auto 未命中:home 模式零 pools.yaml → 不带 --config(只看现状,
    proxy.config=null、pools=[]);dev 回退(home=None)同款不炸。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    code, responses, _ = rpc({"id": 1, "method": "doctor", "params": {"config_auto": True}})
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    assert result["proxy"]["config"] is None and result["proxy"]["pools"] == []

    monkeypatch.delenv("MYIA_HOME")
    code, responses, _ = rpc({"id": 2, "method": "doctor", "params": {"config_auto": True}})
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    assert result["proxy"]["config"] is None and result["proxy"]["pools"] == []


def test_doctor_config_explicit_wins_over_config_auto(tmp_path, monkeypatch):
    """优先级之首:显式 config 与 config_auto 并存 → 手填赢(路径原样回显)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    (tmp_path / "home").mkdir()
    (tmp_path / "home" / "pools.yaml").write_text(POOLS_YAML_UNRESOLVED, encoding="utf-8")
    explicit = str(tmp_path / "elsewhere.yaml")
    code, responses, _ = rpc({"id": 1, "method": "doctor",
                              "params": {"config": explicit, "config_auto": True}})
    result = responses[0]["result"]
    assert result["exit_code"] == 0
    # 显式路径(不存在)→ 拒载明细进 proxy.error,config 仍回显手填值
    assert result["proxy"]["config"] == explicit
    assert result["proxy"]["pools"] == []
    assert result["proxy"].get("error")


def test_doctor_config_auto_non_bool_rejected():
    """config_auto 形状门:非布尔 invalid_params(path=params.config_auto)。"""
    code, responses, _ = rpc({"id": 1, "method": "doctor", "params": {"config_auto": "yes"}})
    error = responses[0]["error"]
    assert error["code"] == "invalid_params"
    assert error["path"] == "params.config_auto"


# ---------------------------------------------------------------------------
# run.start / run.status / logs.tail(子进程 + 流式事件 + 退出码透传)
# ---------------------------------------------------------------------------


def test_run_start_success_full_roundtrip(tmp_path, local_api):
    """成功 run:立即返回 running → log/progress 流 → completed(0/success)
    → run.status done → logs.tail → store.items(数据面贯通)。"""
    yaml_path = write_yaml(tmp_path, VALID_YAML.replace("{port}", str(local_api)))
    db = tmp_path / "myssia.db"
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 1, "method": "run.start",
                                    "params": {"yaml": yaml_path, "db": str(db)}}) + "\n")
    assert entry.serve(stdin=stdin, stdout=out) == 0  # EOF 即回,不等 run
    responses, _ = split_stream(out)
    started = responses[0]["result"]
    run_id = started["run_id"]
    assert started["state"] == "running" and started["dry"] is False

    completed = wait_completed(out, run_id)
    assert completed["exit_code"] == 0
    assert completed["status"] == "success"
    assert completed["record"] is not None
    assert completed["record"]["status"] == "success"

    _, events = split_stream(out)
    types = {event["type"] for event in events}
    assert {"log", "progress", "completed"} <= types  # 三类事件以 type 区分
    phases = [event["phase"] for event in events if event["type"] == "progress"]
    assert "run_start" in phases and "run_end" in phases
    assert any(event["type"] == "progress" and event.get("phase") == "source_done"
               and event.get("items") == "2" for event in events)

    code, status_resp, _ = rpc({"id": 2, "method": "run.status", "params": {"run_id": run_id}})
    entry_record = status_resp[0]["result"]["runs"][0]
    assert entry_record["state"] == "done"
    assert entry_record["exit_code"] == 0 and entry_record["status"] == "success"

    code, logs_resp, _ = rpc({"id": 3, "method": "logs.tail",
                              "params": {"run_id": run_id, "lines": 200}})
    log_lines = logs_resp[0]["result"]["lines"]
    assert log_lines and any("运行结束" in entry["line"] for entry in log_lines)

    code, items_resp, _ = rpc({"id": 4, "method": "store.items", "params": {"db": str(db)}})
    items = items_resp[0]["result"]
    assert items["count"] == 2
    assert {item["title"] for item in items["items"]} == {"协议条目一", "协议条目二"}


def test_run_start_dry_leaves_store_untouched(tmp_path, local_api):
    """dry run:全链执行、completed 0/success,但 store 零持久化副作用。"""
    yaml_path = write_yaml(tmp_path, VALID_YAML.replace("{port}", str(local_api)), "dry.yaml")
    db = tmp_path / "dry.db"
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 1, "method": "run.start",
                                    "params": {"yaml": yaml_path, "dry": True, "db": str(db)}}) + "\n")
    entry.serve(stdin=stdin, stdout=out)
    run_id = json.loads(out.getvalue().splitlines()[0])["result"]["run_id"]
    completed = wait_completed(out, run_id)
    assert completed["exit_code"] == 0 and completed["status"] == "success"
    assert completed["dry"] is True
    assert completed["record"] is None  # dry 走内存存储,无 runs 记录
    code, items_resp, _ = rpc({"id": 2, "method": "store.items", "params": {"db": str(db)}})
    assert items_resp[0]["result"]["count"] == 0


def test_run_start_config_error_exit_code_one(tmp_path):
    """坏 YAML:completed 透传 CLI 退出码 1(config_error),无 store 记录。"""
    yaml_path = write_yaml(tmp_path, BAD_CRON_YAML, "bad.yaml")
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 1, "method": "run.start",
                                    "params": {"yaml": yaml_path, "db": str(tmp_path / "x.db")}}) + "\n")
    entry.serve(stdin=stdin, stdout=out)
    run_id = json.loads(out.getvalue().splitlines()[0])["result"]["run_id"]
    completed = wait_completed(out, run_id)
    assert completed["exit_code"] == 1
    assert completed["status"] == "config_error"
    assert completed["record"] is None


def test_run_busy_single_flight():
    """已有 run 在执行:第二个 run.start 结构化拒绝(run_busy)。"""
    entry._RUNS[99] = {"run_id": 99, "state": "running"}
    entry._ACTIVE_RUN_ID = 99
    try:
        code, responses, _ = rpc({"id": 1, "method": "run.start",
                                  "params": {"yaml": "whatever.yaml"}})
        error = responses[0]["error"]
        assert error["code"] == "run_busy"
        assert error["data"]["active_run_id"] == 99
    finally:
        entry._ACTIVE_RUN_ID = None


def test_run_status_unknown_id():
    """未知 run_id:结构化 404(run_not_found)。"""
    code, responses, _ = rpc({"id": 5, "method": "run.status", "params": {"run_id": 424242}})
    assert responses[0]["error"]["code"] == "run_not_found"
    assert responses[0]["error"]["path"] == "params.run_id"


# ---------------------------------------------------------------------------
# store.items / secret.set / secret.list
# ---------------------------------------------------------------------------


def test_store_items_seeded_db_with_filters(tmp_path):
    """store.items:直读 SQLiteStore,支持 category 过滤与 limit(新→旧)。"""
    db = tmp_path / "seed.db"
    store = SQLiteStore(str(db))
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord
    for index in range(3):
        store.save_item(ItemRecord(
            url=f"https://example.com/{index}", dedup_key=f"k{index}", title=f"条目{index}",
            category="proto-demo" if index < 2 else "other",
            first_seen=datetime(2026, 10, 1, tzinfo=timezone.utc),
        ))
    store.close()
    code, responses, _ = rpc({"id": 1, "method": "store.items", "params": {"db": str(db)}})
    result = responses[0]["result"]
    assert result["count"] == 3 and result["items"][0]["title"] == "条目2"  # 新→旧
    code, responses, _ = rpc({"id": 2, "method": "store.items",
                              "params": {"db": str(db), "category": "proto-demo", "limit": 1}})
    result = responses[0]["result"]
    assert result["count"] == 1 and result["items"][0]["category"] == "proto-demo"


def test_store_items_projects_image_ocr_scalar(tmp_path):
    """store.items 图析投影:vision 环四键白名单出面,raw 整包不出面。

    feed 屏图析行渲染 item.image_ocr(feed-screen.tsx),详情展开吃
    image_caption / image_files / image_ocr_lines(10-03-vision-v2 起随
    ``images.persist`` 产生);数据链 = vision 环挂 metadata → pipeline 以
    raw=item.metadata 入库 → 本投影;无图条目置 None(契约同 types.ts)。
    """
    db = tmp_path / "ocr.db"
    store = SQLiteStore(str(db))
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord
    store.save_item(ItemRecord(
        url="https://example.com/vision", dedup_key="ocr1", title="带图条目",
        first_seen=datetime(2026, 10, 2, tzinfo=timezone.utc),
        raw={
            "image_ocr": "促销 广告语",
            "image_caption": "图表解读全文",
            "image_files": ["/data/images/abc123.png", "/data/images/def456.jpg"],
            "image_ocr_lines": [
                {"text": "促销", "conf": 0.98},
                {"text": "广告语", "conf": 0.91},
            ],
            "image_status": "ok",
            "watch": "raw 其余键",
        },
    ))
    store.save_item(ItemRecord(
        url="https://example.com/plain", dedup_key="ocr2", title="无图条目",
        first_seen=datetime(2026, 10, 1, tzinfo=timezone.utc),
    ))
    store.save_item(ItemRecord(
        url="https://example.com/badshape", dedup_key="ocr3", title="形态坏条目",
        first_seen=datetime(2026, 10, 3, tzinfo=timezone.utc),
        # 坏形态:caption 空白 / files 混杂坏值 / ocr_lines 夹杂坏行 → 全置 None
        raw={"image_ocr": "x", "image_caption": "  ", "image_files": ["ok.png", 42],
             "image_ocr_lines": [{"text": "好", "conf": 0.9}, {"text": "坏行"}]},
    ))
    store.close()
    code, responses, _ = rpc({"id": 1, "method": "store.items", "params": {"db": str(db)}})
    result = responses[0]["result"]
    by_key = {item["dedup_key"]: item for item in result["items"]}
    assert by_key["ocr1"]["image_ocr"] == "促销 广告语"
    assert by_key["ocr1"]["image_caption"] == "图表解读全文"
    assert by_key["ocr1"]["image_files"] == ["/data/images/abc123.png", "/data/images/def456.jpg"]
    assert by_key["ocr1"]["image_ocr_lines"] == [{"text": "促销", "conf": 0.98},
                                                 {"text": "广告语", "conf": 0.91}]
    assert by_key["ocr2"]["image_ocr"] is None
    assert by_key["ocr2"]["image_caption"] is None
    assert by_key["ocr2"]["image_files"] is None
    assert by_key["ocr2"]["image_ocr_lines"] is None
    # 坏形态:三新键整体置 None(image_ocr 标量照常投影,不受牵连)
    assert by_key["ocr3"]["image_caption"] is None
    assert by_key["ocr3"]["image_files"] is None
    assert by_key["ocr3"]["image_ocr_lines"] is None
    assert by_key["ocr3"]["image_ocr"] == "x"
    # raw 整包仍不出协议面:仅白名单投影,其余 metadata 键不外泄
    # (read/starred/later = v10 起随行读态三键,G9)
    assert set(by_key["ocr1"]) == {
        "id", "url", "dedup_key", "title", "source", "content", "image_ocr",
        "image_caption", "image_files", "image_ocr_lines",
        "tags", "category", "scores", "pushed_at", "push_slot", "first_seen",
        "read", "starred", "later",
    }


def test_store_items_corrupt_db_structured_error(tmp_path):
    """库损坏:结构化透传 store_corrupt(码/路径/消息)。"""
    db = tmp_path / "corrupt.db"
    db.write_bytes(b"this is not sqlite" * 10)
    code, responses, _ = rpc({"id": 1, "method": "store.items", "params": {"db": str(db)}})
    error = responses[0]["error"]
    assert error["code"] == "store_corrupt"
    assert error["path"] == "params.db"


def test_secret_set_roundtrip_value_never_echoed():
    """secret.set:写入走 myssia.secrets(钥匙链),应答零回显值。"""
    fake = entry.set_secret
    code, responses, events = rpc({"id": 9, "method": "secret.set",
                                   "params": {"name": "myia/proto/token", "value": "super-secret-value"}})
    assert code == 0
    assert responses == [{"id": 9, "result": {"name": "myia/proto/token", "stored": True}}]
    assert fake.capture.calls == [("myia/proto/token", "super-secret-value")]
    assert "super-secret-value" not in json.dumps(responses)  # 值零回显
    code, responses, _ = rpc({"id": 10, "method": "secret.list"})
    assert responses[0]["result"]["names"] == ["myia/proto/token"]  # 只有名字


def test_secret_set_missing_params():
    """secret.set 缺参:invalid_params 带字段路径。"""
    code, responses, _ = rpc({"id": 1, "method": "secret.set", "params": {"name": "myia/a/b"}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.value"


# ---------------------------------------------------------------------------
# 协议层:错误结构化 / 通知 / EOF 退出码 / 直通模式
# ---------------------------------------------------------------------------


def test_protocol_errors_are_structured():
    """parse_error(id=null)/ invalid_request / invalid_params / method_not_found。"""
    code, responses, _ = rpc(raw_lines=["{not json"])
    assert responses[0] == {"id": None, "error": {"code": "parse_error", "path": "$",
                                                  "message": responses[0]["error"]["message"]}}
    code, responses, _ = rpc({"id": 1, "params": {}})  # 缺 method
    assert responses[0]["error"]["code"] == "invalid_request"
    code, responses, _ = rpc({"id": 2, "method": "version", "params": [1]})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params"
    code, responses, _ = rpc({"id": 3, "method": "does.not.exist"})
    assert responses[0]["error"]["code"] == "method_not_found"
    assert "version" in responses[0]["error"]["data"]["allowed"]


def test_method_registry_full_reconciliation():
    """全量对账(质询补死,归属 G10 流):method_not_found 的 data.allowed ==
    sorted(_HANDLERS) == sidecar-protocol.md 注册表逐行方法名——两侧动态比对,
    代码或文档任一侧漂移即红(原用例只断成员包含;行数随批自然涨,不硬编码)。"""
    code, responses, _ = rpc({"id": 1, "method": "does.not.exist"})
    allowed = responses[0]["error"]["data"]["allowed"]
    assert allowed == sorted(entry._HANDLERS)
    spec_text = (REPO_ROOT / ".trellis" / "spec" / "desktop" / "sidecar-protocol.md").read_text(
        encoding="utf-8"
    )
    table = spec_text.split("## 方法注册表", 1)[1].split("\n分组:", 1)[0]
    documented: list[str] = []
    for line in table.splitlines():
        if not line.startswith("| ") or line.startswith("| #") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and cells[0].isdigit():
            documented.append(cells[1].strip("`"))
    assert sorted(documented) == allowed, (
        f"注册表({len(documented)} 行)与 _HANDLERS({len(allowed)}) 漂移:"
        f" 文档多={sorted(set(documented) - set(allowed))},"
        f" 代码多={sorted(set(allowed) - set(documented))}"
    )


def test_notification_yields_no_response():
    """无 id = 通知:执行但不应答(零输出行)。"""
    code, responses, events = rpc({"method": "version"})
    assert code == 0
    assert responses == [] and events == []


def test_serve_exit_code_zero_on_eof():
    """stdin EOF = 干净退出 0(壳关闭管道即正常关停)。"""
    code, _, _ = rpc()
    assert code == 0


def test_oneshot_passthrough_preserves_cli_contract(tmp_path):
    """直通模式:退出码契约原样(--version=0;run 坏 YAML=1)。"""
    env = {"PATH": "/usr/bin:/bin", "PYTHONPATH": str(REPO_ROOT / "src"), "HOME": str(tmp_path)}
    version = subprocess.run(
        [sys.executable, str(ENTRY_PATH), "--version"], capture_output=True, text=True, env=env,
        check=False,
    )
    assert version.returncode == 0
    assert version.stdout.startswith("myssia ")
    bad = write_yaml(tmp_path, BAD_CRON_YAML, "passthrough-bad.yaml")
    run = subprocess.run(
        [sys.executable, str(ENTRY_PATH), "run", bad, "--db", str(tmp_path / "p.db")],
        capture_output=True, text=True, env=env, check=False,
    )
    assert run.returncode == 1  # 配置错误 = 1(spec python/error-handling)


# ---------------------------------------------------------------------------
# sources.write:源启停写回(往返一致 = load_category_file 同门复核)
# ---------------------------------------------------------------------------

SOURCES_WRITE_YAML = """
id: sources-demo
name: 源启停夹具
schedule: "0 9 * * *"
sources:
  - name: keep-me
    engine: static_html
    url: "http://127.0.0.1:9/pages"
    rate_limit:
      respect_robots: false
    extract:
      type: list
      item: "li"
      fields:
        title: "h3"
        url: "a@href"
  - name: drop-me
    engine: static_html
    url: "http://127.0.0.1:9/other"
    rate_limit:
      respect_robots: false
    extract:
      type: list
      item: "li"
      fields:
        title: "h3"
        url: "a@href"
classify:
  builtin: false
dedup:
  key: "{url}"
push:
  - channel: stdout
plugin:
  id: myssia-demo
  modes:
    local:
      compose: docker-compose.yml
"""


def test_sources_write_disable_enable_roundtrip(tmp_path):
    """disable 摘出(enable 移回):myssia 装载器同门复核 + sidecar 节保留 +
    暂存文件 lossless 往返 —— PRD「写回品类 YAML 并被 myssia run 识别」。"""
    from myssia.schema import load_category_file

    yaml_path = Path(write_yaml(tmp_path, SOURCES_WRITE_YAML, "sources-demo.yaml"))

    code, responses, _ = rpc(
        {"id": 1, "method": "sources.write",
         "params": {"file": str(yaml_path), "disable": ["drop-me"]}},
    )
    assert code == 0
    assert responses[0]["result"] == {
        "file": str(yaml_path),
        "written": True,
        "enabled": ["keep-me"],
        "disabled": ["drop-me"],
    }
    # myssia run 同门:写回文件可装载,名单只剩 keep-me;plugin: 节原样保留
    config = load_category_file(yaml_path)
    assert [source.name for source in config.sources] == ["keep-me"]
    assert config.plugin is not None and config.plugin.id == "myssia-demo"
    raw_text = yaml_path.read_text(encoding="utf-8")
    assert "plugin:" in raw_text and "drop-me" not in raw_text
    # lossless 暂存:被摘出的源完整落在 <yaml>.disabled.json
    stash = json.loads((tmp_path / "sources-demo.yaml.disabled.json").read_text("utf-8"))
    assert [item["name"] for item in stash] == ["drop-me"]
    assert stash[0]["url"] == "http://127.0.0.1:9/other"

    # enable 移回:名单复原,暂存文件清空删除
    code, responses, _ = rpc(
        {"id": 2, "method": "sources.write",
         "params": {"file": str(yaml_path), "enable": ["drop-me"]}},
    )
    assert code == 0
    assert responses[0]["result"]["enabled"] == ["keep-me", "drop-me"]
    assert responses[0]["result"]["disabled"] == []
    config = load_category_file(yaml_path)
    assert [source.name for source in config.sources] == ["keep-me", "drop-me"]
    assert not (tmp_path / "sources-demo.yaml.disabled.json").exists()


def test_sources_write_structured_refusals(tmp_path):
    """结构化拒绝:未知源名 / 停用最后一个启用源,失败零写入。"""
    yaml_path = Path(write_yaml(tmp_path, SOURCES_WRITE_YAML, "refusal.yaml"))
    before = yaml_path.read_text(encoding="utf-8")

    code, responses, _ = rpc(
        {"id": 1, "method": "sources.write",
         "params": {"file": str(yaml_path), "disable": ["nope"]}},
    )
    assert code == 0  # 协议流不因业务错误中断;错误在应答对象里
    error = responses[0]["error"]
    assert error["code"] == "source_unknown"
    assert error["data"]["enabled"] == ["keep-me", "drop-me"]

    code, responses, _ = rpc(
        {"id": 2, "method": "sources.write",
         "params": {"file": str(yaml_path).replace("refusal.yaml", "missing.yaml"),
                    "disable": ["keep-me"]}},
    )
    error = responses[0]["error"]
    assert error["code"] == "source_file_unreadable"
    assert error["path"] == "params.file"

    # 逐个停到只剩一个,再停即拒(schema sources min_length=1 的可装载底线)
    code, responses, _ = rpc(
        {"id": 3, "method": "sources.write",
         "params": {"file": str(yaml_path), "disable": ["drop-me"]}},
    )
    assert responses[0]["result"]["written"] is True
    code, responses, _ = rpc(
        {"id": 4, "method": "sources.write",
         "params": {"file": str(yaml_path), "disable": ["keep-me"]}},
    )
    assert responses[0]["error"]["code"] == "last_source"
    # 拒绝 = 零写入(文件仍是「只剩 keep-me」的成功态,不是半态)
    from myssia.schema import load_category_file

    assert [source.name for source in load_category_file(yaml_path).sources] == ["keep-me"]
    assert yaml_path.read_text(encoding="utf-8") != before


# ---------------------------------------------------------------------------
# v1.1.1 应用数据根:上下文解析优先级 / .app bundle 探测 / 首跑种子 / first_run
# (task 10-03-v111-desktop-paths,design.md D1-D3/D8)
# ---------------------------------------------------------------------------

OFFICIAL_TEMPLATE = """
id: {pid}
name: 官方夹具 {pid}
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:9/x"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.a"
        url: "$.b"
classify:
  builtin: false
"""


def _fake_bundle(tmp_path: Path, *plugin_ids: str) -> Path:
    bundle = tmp_path / "bundle" / "plugins"
    bundle.mkdir(parents=True, exist_ok=True)
    for pid in plugin_ids:
        (bundle / f"{pid}.yaml").write_text(OFFICIAL_TEMPLATE.format(pid=pid), encoding="utf-8")
    return bundle


def test_serve_context_myssia_home_env(tmp_path, monkeypatch):
    """MYIA_HOME env → home 模式:db/plugins 默认全落数据根(并即时建目录)。"""
    home = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(home))
    ctx = entry._serve_context()
    assert ctx.home == home
    assert ctx.db == str(home / "myssia.db")
    assert ctx.plugins_dir == str(home / "plugins")
    assert ctx.install_root == str(home / "plugins")
    assert home.is_dir()


def test_serve_context_plugin_dir_env_respected(tmp_path, monkeypatch):
    """既有 MYIA_PLUGIN_DIR 约定不被夺权:安装根显式 env 优先于 <home>/plugins。"""
    market = tmp_path / "market"
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("MYIA_PLUGIN_DIR", str(market))
    assert entry._serve_context().install_root == str(market)


def test_serve_context_dev_fallback_unchanged(monkeypatch):
    """dev 回退:三项默认与 v1.1 CLI 常量逐字节一致(仓库内行为不回退)。"""
    from myssia.cli import DEFAULT_DB_PATH, DEFAULT_PLUGINS_DIR
    from myssia.plugins.installed import default_install_root

    monkeypatch.delattr(sys, "frozen", raising=False)
    ctx = entry._serve_context()
    assert ctx.home is None
    assert ctx.db == DEFAULT_DB_PATH
    assert ctx.plugins_dir == DEFAULT_PLUGINS_DIR
    assert ctx.install_root == str(default_install_root())


def test_bundle_detection_dot_app(tmp_path, monkeypatch):
    """冻结 exe 位于 .app 内 → 平台数据根(bundle 探测,Rust 注入丢失时的兜底)。"""
    exe = tmp_path / "MYIA.app" / "Contents" / "MacOS" / "myia"
    exe.parent.mkdir(parents=True)
    exe.write_text("#!/bin/sh\n", encoding="utf-8")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(exe))
    platform_root = tmp_path / "platform-root"
    monkeypatch.setattr(entry, "myssia_home", lambda: platform_root)
    assert entry._inside_app_bundle() is True
    assert entry._serve_context().home == platform_root


def test_bundle_detection_requires_dot_app(tmp_path, monkeypatch):
    """冻结但不在 .app 内(裸 CLI 分发形态)→ 仍 dev 回退,不偷偷进家目录。"""
    exe = tmp_path / "bin" / "myia"
    exe.parent.mkdir(parents=True)
    exe.write_text("#!/bin/sh\n", encoding="utf-8")
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "executable", str(exe))
    assert entry._inside_app_bundle() is False
    assert entry._serve_context().home is None


def test_bundle_plugins_dir_managed_python_resource_tree(tmp_path, monkeypatch):
    """托管 Python 形态(非冻结,10-05-desktop-managed-py-env):资源树布局
    Resources/myssia-src/entry.py → 按本文件相对定位旁级 Resources/plugins。

    装机实测回归钉(2026-10-05 换装):冻结时代 ``sys.frozen`` 门 + exe 相对
    候选在 ``python -m myssia_desktop_entry`` 形态下恒 None,品类补种静默
    no-op —— games/news/exposure 永不落数据根,此测试钉死该形态的解析。"""
    resources = tmp_path / "Resources"
    src_tree = resources / "myssia-src"
    src_tree.mkdir(parents=True)
    shutil.copyfile(ENTRY_PATH, src_tree / "entry.py")
    bundle = resources / "plugins"
    bundle.mkdir()
    (bundle / "games.yaml").write_text(OFFICIAL_TEMPLATE.format(pid="games"), encoding="utf-8")
    monkeypatch.delattr(sys, "frozen", raising=False)
    spec = importlib.util.spec_from_file_location("managed_entry_probe", src_tree / "entry.py")
    managed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(managed)
    assert managed._bundle_plugins_dir() == bundle


def test_bundle_plugins_dir_dev_tree_stays_none(monkeypatch):
    """开发树(desktop/entry.py,父目录名非 myssia-src)且非冻结 → None,dev 行为零变化。"""
    monkeypatch.delattr(sys, "frozen", raising=False)
    assert entry._bundle_plugins_dir() is None


def test_seed_copies_official_plugins_and_marks(tmp_path, monkeypatch):
    """首跑补种:空 plugins → 拷官方四件套 + 写 .seeded;删件后重启补缺回。"""
    home = tmp_path / "home"
    bundle = _fake_bundle(tmp_path, "ai-news", "wool", "stocks", "gpu-prices")
    monkeypatch.setattr(entry, "_bundle_plugins_dir", lambda: bundle)
    ctx = entry.ServeContext(
        home=home, db=str(home / "myssia.db"),
        plugins_dir=str(home / "plugins"), install_root=str(home / "plugins"),
    )
    assert entry._seed_first_run(ctx) is True
    seeded = sorted(path.name for path in (home / "plugins").glob("*.yaml"))
    assert seeded == ["ai-news.yaml", "gpu-prices.yaml", "stocks.yaml", "wool.yaml"]
    marker = home / entry.SEED_MARKER
    assert marker.exists()

    # 幂等补缺(AC5 语义):删一个插件后重启 → 该件补回,标志不重写。
    (home / "plugins" / "wool.yaml").unlink()
    mtime_before = marker.stat().st_mtime_ns
    assert entry._seed_first_run(ctx) is True
    assert (home / "plugins" / "wool.yaml").exists()
    assert marker.stat().st_mtime_ns == mtime_before  # 首次补种时刻定格


def test_seed_skips_when_user_has_plugins(tmp_path, monkeypatch):
    """用户自建品类在场:原样保留零覆盖,bundle 缺件(官方位)照补。"""
    home = tmp_path / "home"
    bundle = _fake_bundle(tmp_path, "ai-news")
    plugins = home / "plugins"
    plugins.mkdir(parents=True)
    mine = OFFICIAL_TEMPLATE.format(pid="mine")
    (plugins / "mine.yaml").write_text(mine, encoding="utf-8")
    monkeypatch.setattr(entry, "_bundle_plugins_dir", lambda: bundle)
    ctx = entry.ServeContext(
        home=home, db=str(home / "myssia.db"),
        plugins_dir=str(plugins), install_root=str(plugins),
    )
    assert entry._seed_first_run(ctx) is True  # 官方 ai-news 缺 → 补
    assert (plugins / "mine.yaml").read_text(encoding="utf-8") == mine  # 用户件不动
    assert sorted(path.name for path in plugins.glob("*.yaml")) == ["ai-news.yaml", "mine.yaml"]
    assert (home / entry.SEED_MARKER).exists()


def test_seed_does_not_overwrite_existing_games_yaml(tmp_path, monkeypatch):
    """AC5 补种:已存在 games.yaml(手改/旧版)→ 逐字节原样,绝不被 bundle 覆盖。"""
    home = tmp_path / "home"
    bundle = _fake_bundle(tmp_path, "games", "news")
    plugins = home / "plugins"
    plugins.mkdir(parents=True)
    custom = OFFICIAL_TEMPLATE.format(pid="games-user-edited")
    (plugins / "games.yaml").write_text(custom, encoding="utf-8")
    monkeypatch.setattr(entry, "_bundle_plugins_dir", lambda: bundle)
    ctx = entry.ServeContext(
        home=home, db=str(home / "myssia.db"),
        plugins_dir=str(plugins), install_root=str(plugins),
    )
    assert entry._seed_first_run(ctx) is True  # news 缺,补了一件
    assert (plugins / "games.yaml").read_text(encoding="utf-8") == custom
    assert sorted(path.name for path in plugins.glob("*.yaml")) == ["games.yaml", "news.yaml"]

    # 零缺件再跑:幂等零动作(全量在位)。
    assert entry._seed_first_run(ctx) is False
    assert (plugins / "games.yaml").read_text(encoding="utf-8") == custom


def test_seed_fills_missing_news_yaml_only(tmp_path, monkeypatch):
    """AC5 补种:缺 news.yaml 时只补 news.yaml;全量在位的首次启动零标志。"""
    home = tmp_path / "home"
    bundle = _fake_bundle(tmp_path, "ai-news", "news")
    plugins = home / "plugins"
    plugins.mkdir(parents=True)
    for pid in ("ai-news", "news"):
        (plugins / f"{pid}.yaml").write_text(OFFICIAL_TEMPLATE.format(pid=pid), encoding="utf-8")
    monkeypatch.setattr(entry, "_bundle_plugins_dir", lambda: bundle)
    ctx = entry.ServeContext(
        home=home, db=str(home / "myssia.db"),
        plugins_dir=str(plugins), install_root=str(plugins),
    )
    # 从未缺件:零拷贝、零标志(「已做过一次补种」的记录无从谈起)。
    assert entry._seed_first_run(ctx) is False
    assert not (home / entry.SEED_MARKER).exists()

    # 缺 news.yaml → 只补 news.yaml,标志随之落盘。
    (plugins / "news.yaml").unlink()
    assert entry._seed_first_run(ctx) is True
    assert (plugins / "news.yaml").exists()
    assert (home / entry.SEED_MARKER).exists()


def test_serve_startup_seeds_in_home_mode(tmp_path, monkeypatch):
    """serve 启动即种子(home 模式);dev 模式连 bundle 探测都不碰。"""
    home = tmp_path / "home"
    bundle = _fake_bundle(tmp_path, "ai-news")
    monkeypatch.setenv("MYIA_HOME", str(home))
    monkeypatch.setattr(entry, "_bundle_plugins_dir", lambda: bundle)
    code, responses, _ = rpc({"id": 1, "method": "version", "params": {}})
    assert code == 0 and responses[0]["result"]["version"]
    assert (home / "plugins" / "ai-news.yaml").exists()

    monkeypatch.delenv("MYIA_HOME")
    monkeypatch.setattr(
        entry, "_bundle_plugins_dir",
        lambda: (_ for _ in ()).throw(AssertionError("dev 模式不得触发 bundle 探测")),
    )
    code, responses, _ = rpc({"id": 2, "method": "version", "params": {}})
    assert code == 0 and responses[0]["result"]["version"]


def test_health_first_run_flag_and_home_defaults(tmp_path, monkeypatch):
    """health:home 模式 db/plugins 落数据根;零 yaml → first_run=true,种上即 false。"""
    home = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(home))
    code, responses, _ = rpc({"id": 1, "method": "health", "params": {}})
    result = responses[0]["result"]
    assert code == 0
    assert result["plugins_dir"] == str(home / "plugins")
    assert result["db"] == str(home / "myssia.db")
    assert result["first_run"] is True
    assert result["healthy"] is True  # 空态是合法态,不是错误

    (home / "plugins").mkdir(parents=True, exist_ok=True)
    (home / "plugins" / "ai-news.yaml").write_text(
        OFFICIAL_TEMPLATE.format(pid="ai-news"), encoding="utf-8"
    )
    code, responses, _ = rpc({"id": 2, "method": "health", "params": {}})
    result = responses[0]["result"]
    assert result["first_run"] is False
    assert [plugin["id"] for plugin in result["plugins"]] == ["ai-news"]


def test_health_explicit_params_win_over_env(tmp_path, monkeypatch):
    """优先级之首:显式 params 永远赢过 MYIA_HOME(env 只供缺省)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    plugins_dir = tmp_path / "elsewhere"
    plugins_dir.mkdir()
    code, responses, _ = rpc(
        {"id": 1, "method": "health", "params": {"plugins_dir": str(plugins_dir)}},
    )
    assert code == 0
    assert responses[0]["result"]["plugins_dir"] == str(plugins_dir)


def test_store_items_and_run_default_db_follow_home(tmp_path, monkeypatch):
    """store.items / run.start 的 db 缺省同收口:一条数据通路一个库。"""
    home = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(home))
    code, responses, _ = rpc({"id": 1, "method": "store.items", "params": {"limit": 5}})
    assert code == 0
    assert responses[0]["result"]["db"] == str(home / "myssia.db")
    assert responses[0]["result"]["items"] == []


def test_myssia_home_three_platforms(tmp_path, monkeypatch):
    """myssia_home 三平台规则(design.md D1):darwin=~/Library/Application
    Support/MYIA、win32=%APPDATA%\\MYIA、linux=~/.myia(本机外分支注入
    sys.platform 验证;Path.home 按 tarHeel 平台语义 monkeypatch)。"""
    # darwin(HOME 重定向,避免触碰真实用户目录)
    monkeypatch.setattr(sys, "platform", "darwin")
    monkeypatch.setenv("HOME", str(tmp_path))
    assert entry.myssia_home() == tmp_path / "Library" / "Application Support" / "MYIA"
    # win32(APPDATA 优先,缺失回退 ~/AppData/Roaming)
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setenv("APPDATA", str(tmp_path / "Roaming"))
    assert entry.myssia_home() == tmp_path / "Roaming" / "MYIA"
    monkeypatch.delenv("APPDATA")
    monkeypatch.setattr(Path, "home", lambda: tmp_path)  # Windows 语义:家目录即 %USERPROFILE%
    assert entry.myssia_home() == tmp_path / "AppData" / "Roaming" / "MYIA"
    # linux/其余(POSIX 家目录策略,收编旧 ~/.myia 约定)
    monkeypatch.setattr(sys, "platform", "linux")
    assert entry.myssia_home() == tmp_path / ".myia"


def test_run_start_default_db_follows_home(tmp_path, monkeypatch):
    """run.start 的 db 缺省收口到数据根(工作线程 monkeypatch 成 no-op,
    只验参数装配形态,不真跑子进程;参数形态=UI types.ts RunStartParams)。"""
    home = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(home))
    yaml_path = write_yaml(tmp_path, VALID_YAML.replace("{port}", "9"))
    monkeypatch.setattr(entry, "_run_worker", lambda *args, **kwargs: None)
    code, responses, _ = rpc({"id": 1, "method": "run.start", "params": {"yaml": yaml_path}})
    assert code == 0
    started = responses[0]["result"]
    assert started["db"] == str(home / "myssia.db")
    assert started["state"] == "running" and started["dry"] is False
    assert entry._ACTIVE_RUN_ID == 1
    entry._ACTIVE_RUN_ID = None  # no-op worker 不会走 finally 清理,此处手工复位


# ---------------------------------------------------------------------------
# yaml.*:配置编辑器协议(task 10-03-yaml-editor;契约钉死于任务档 design.md §1,
# 坏文件入列可修、围栏四违例、save 零写入守门、乐观锁、启停止血、两写路径互斥)
# ---------------------------------------------------------------------------

EDITOR_YAML = """
# 头部注释:编辑器往返保真夹具(逐字节原样,注释不丢)
id: editor-demo
name: 编辑器夹具
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:9/x"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.a"
        url: "$.b"
classify:
  builtin: false
push:
  - channel: stdout
"""

#: 启停止血/写路径互斥夹具:两源 + 顶部注释(sources.write 的 safe_dump 会抹注释)。
COMMENTED_TOGGLE_YAML = """
# 顶部注释:启停止血夹具(safe_dump 重写会抹掉,.bak 留底可找回)
id: toggle-demo
name: 启停止血
schedule: "0 9 * * *"
sources:
  - name: keep-me
    engine: static_html
    url: "http://127.0.0.1:9/pages"
    rate_limit:
      respect_robots: false
    extract:
      type: list
      item: "li"
      fields:
        title: "h3"
        url: "a@href"
  - name: drop-me
    engine: static_html
    url: "http://127.0.0.1:9/other"
    rate_limit:
      respect_robots: false
    extract:
      type: list
      item: "li"
      fields:
        title: "h3"
        url: "a@href"
"""

#: 凭据分级夹具:env: 引用只验格式(不对照名单),keychain: 未录入出 warning。
SECRET_REF_YAML = """
id: secret-demo
name: 凭据夹具
schedule: "0 9 * * *"
sources:
  - name: api
    engine: direct_api
    url: "http://127.0.0.1:9/x"
    headers:
      Authorization: "env:NOT_SET_ANYWHERE"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.a"
        url: "$.b"
push:
  - channel: webhook
    target: "keychain:myia/push/demo"
"""


def _editor_plugins(tmp_path: Path, monkeypatch, *files: tuple[str, str]) -> Path:
    """home 模式下的可控 plugins 目录:yaml.list 零参数,目录由 serve 上下文定。"""
    plugins = tmp_path / "home" / "plugins"
    plugins.mkdir(parents=True, exist_ok=True)
    for name, text in files:
        (plugins / name).write_text(text, encoding="utf-8")
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    return plugins


def test_yaml_fence_four_violations_and_stem(tmp_path, monkeypatch):
    """路径围栏:../ 穿越 / 目录外绝对路径 / 非 yaml 后缀 / 符号链接逃逸 →
    结构化拒绝;新建 stem 违例(大写+空格)在 save 路径同样被拦。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", EDITOR_YAML))
    outside = tmp_path / "outside.yaml"
    outside.write_text(EDITOR_YAML, encoding="utf-8")
    link = plugins / "link.yaml"
    link.symlink_to(outside)
    cases = [
        (str(plugins / ".." / ".." / "evil.yaml"), "path_outside_root"),  # ../ 穿越
        (str(outside), "path_outside_root"),  # 目录外绝对路径
        (str(plugins / "notes.txt"), "not_yaml_suffix"),  # 非 yaml 后缀
        (str(link), "path_outside_root"),  # 符号链接逃逸(resolve 消解后越界)
    ]
    for index, (file, code) in enumerate(cases, start=1):
        _, responses, _ = rpc({"id": index, "method": "yaml.read", "params": {"file": file}})
        assert responses[0]["error"]["code"] == code
    # 新建 stem 违例:围栏第三道门(file 不存在时 stem 过品类 id 同款正则)
    bad_stem = plugins / "My Category.yaml"
    _, responses, _ = rpc({"id": 9, "method": "yaml.save",
                           "params": {"file": str(bad_stem), "content": EDITOR_YAML,
                                      "expected_mtime": None}})
    assert responses[0]["error"]["code"] == "invalid_file_stem"
    assert not bad_stem.exists()  # 拒绝 = 零写入


def test_yaml_list_broken_file_readable_and_fixable(tmp_path, monkeypatch):
    """坏 YAML 也入列(parse_ok=false + error)且可读可修 —— 编辑器核心用例:
    修好 health 加载不了的文件;修好 save 后 list 恢复 parse_ok。"""
    plugins = _editor_plugins(
        tmp_path, monkeypatch,
        ("demo.yaml", EDITOR_YAML),
        ("broken.yaml", EDITOR_YAML.replace("editor-demo", "broken-demo")
                                   .replace('schedule: "0 9 * * *"', 'schedule: "not-a-cron"')),
    )
    code, responses, _ = rpc({"id": 1, "method": "yaml.list"})
    result = responses[0]["result"]
    assert code == 0
    assert result["plugins_dir"] == str(plugins)
    assert [item["name"] for item in result["files"]] == ["broken.yaml", "demo.yaml"]  # 按文件名排序
    good = result["files"][1]
    assert good["parse_ok"] is True and good["category_id"] == "editor-demo"
    assert good["category_name"] == "编辑器夹具" and good["sources"] == 1
    assert good["error"] is None
    bad = result["files"][0]
    assert bad["parse_ok"] is False and bad["category_id"] is None and bad["sources"] is None
    assert bad["error"]["code"] == "invalid_cron" and bad["error"]["path"] == "$.schedule"

    # 坏文件可读:原文字节直读,注释原样
    _, responses, _ = rpc({"id": 2, "method": "yaml.read",
                           "params": {"file": str(plugins / "broken.yaml")}})
    read = responses[0]["result"]
    assert "头部注释" in read["content"]
    assert read["size"] == len(read["content"].encode("utf-8"))
    # 可修:带读回的 mtime 保存修好的内容 → list 恢复 parse_ok
    fixed = read["content"].replace("not-a-cron", "0 9 * * *")
    _, responses, _ = rpc({"id": 3, "method": "yaml.save",
                           "params": {"file": str(plugins / "broken.yaml"),
                                      "content": fixed, "expected_mtime": read["mtime"]}})
    assert responses[0]["result"]["created"] is False
    _, responses, _ = rpc({"id": 4, "method": "yaml.list"})
    entry = [item for item in responses[0]["result"]["files"]
             if item["name"] == "broken.yaml"][0]
    assert entry["parse_ok"] is True and entry["category_id"] == "broken-demo"


def test_yaml_validate_dry_run_zero_write(tmp_path, monkeypatch):
    """validate 干跑:findings 结构化(未知字段 error 级 + 字段路径),正例带
    category 摘要;干跑后文件内容与 mtime 逐项不变(零写入)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", EDITOR_YAML))
    path = plugins / "demo.yaml"
    before = path.read_text(encoding="utf-8")
    mtime_before = path.stat().st_mtime
    _, responses, _ = rpc({"id": 1, "method": "yaml.validate",
                           "params": {"content": EDITOR_YAML + "bogus_field: 1\n",
                                      "file": str(path)}})
    result = responses[0]["result"]
    assert result["valid"] is False and result["category"] is None
    finding = result["findings"][0]
    assert finding == {"path": "$.bogus_field", "code": "unknown_field",
                       "message": finding["message"], "level": "error"}
    assert path.read_text(encoding="utf-8") == before  # 零写入
    assert path.stat().st_mtime == mtime_before  # 连 mtime 都不动
    # 正例:不带 file 也可干跑,category 摘要随行
    _, responses, _ = rpc({"id": 2, "method": "yaml.validate", "params": {"content": EDITOR_YAML}})
    result = responses[0]["result"]
    assert result["valid"] is True and result["findings"] == []
    assert result["category"] == {"id": "editor-demo", "name": "编辑器夹具", "sources": 1}


def test_yaml_save_invalid_zero_write_bak_untouched(tmp_path, monkeypatch):
    """save 校验失败:语法错/停到 0 源(schema 同门)→ category_invalid 结构化
    明细;目标文件零变更,既有 .bak 不动(拒绝路径不碰备份)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", EDITOR_YAML))
    path = plugins / "demo.yaml"
    bak = plugins / "demo.yaml.bak"
    bak.write_text("SENTINEL-BAK", encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    _, responses, _ = rpc({"id": 1, "method": "yaml.save",
                           "params": {"file": str(path), "content": "id: broken\nsources: [",
                                      "expected_mtime": path.stat().st_mtime}})
    error = responses[0]["error"]
    assert error["code"] == "category_invalid" and error["path"] == "params.content"
    assert error["data"]["errors"][0]["code"] == "yaml_parse_error"  # 明细同构透传
    # 停到 0 源:schema sources min_length=1 的编辑保存同门生效
    no_sources = """
id: editor-demo
name: 编辑器夹具
schedule: "0 9 * * *"
sources: []
"""
    _, responses, _ = rpc({"id": 2, "method": "yaml.save",
                           "params": {"file": str(path), "content": no_sources,
                                      "expected_mtime": path.stat().st_mtime}})
    error = responses[0]["error"]
    assert error["code"] == "category_invalid"
    assert error["data"]["errors"][0]["code"] == "too_short"
    assert path.read_text(encoding="utf-8") == before  # 零写入
    assert bak.read_text(encoding="utf-8") == "SENTINEL-BAK"  # .bak 不动


def test_yaml_save_new_file_roundtrip_and_not_found_fork(tmp_path, monkeypatch):
    """新建往返:null mtime + 不存在 = 创建(created=true、无 .bak)→ doctor/
    list 识别新品类,既有文件 .bak 不误伤;非 null mtime + 不存在 = file_not_found。"""
    from myssia.schema import load_category_file

    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", EDITOR_YAML))
    new_path = plugins / "fresh-pick.yaml"
    content = EDITOR_YAML.replace("editor-demo", "fresh-pick")
    code, responses, _ = rpc({"id": 1, "method": "yaml.save",
                              "params": {"file": str(new_path), "content": content,
                                         "expected_mtime": None}})
    result = responses[0]["result"]
    assert code == 0
    assert result["file"] == str(new_path)
    assert result["written"] is True and result["created"] is True
    assert result["backed_up"] is None and result["warnings"] == []
    assert isinstance(result["mtime"], float) and result["mtime"] > 0
    # myssia run 同门:新文件可装载,id 即用户命名
    assert load_category_file(new_path).id == "fresh-pick"
    # doctor 识别(保存闭环的证据面)
    _, responses, _ = rpc({"id": 2, "method": "doctor", "params": {"yamls": [str(new_path)]}})
    assert responses[0]["result"]["plugins"][0]["id"] == "fresh-pick"
    # list 识别;既有 demo.yaml 不被误伤(无 .bak)
    _, responses, _ = rpc({"id": 3, "method": "yaml.list"})
    names = [item["name"] for item in responses[0]["result"]["files"]]
    assert names == ["demo.yaml", "fresh-pick.yaml"]
    assert not (plugins / "demo.yaml.bak").exists()
    # file_not_found 分叉:「想改却不存在」≠「想建」,防路径手误建出影子文件
    ghost = plugins / "ghost.yaml"
    _, responses, _ = rpc({"id": 4, "method": "yaml.save",
                           "params": {"file": str(ghost), "content": content,
                                      "expected_mtime": 1.0}})
    assert responses[0]["error"]["code"] == "file_not_found"
    assert not ghost.exists()


def test_yaml_save_overwrite_backs_up_previous_content(tmp_path, monkeypatch):
    """save 成功覆盖已有文件:.bak = 保存前旧原文(含注释,逐字节),应答
    backed_up 指向它;单份滚动 —— 二次保存后 .bak 前移为上一次内容
    (design §7 测试清单「save 的 .bak 内容 = 旧原文」的锁定项)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", EDITOR_YAML))
    path = plugins / "demo.yaml"
    bak = plugins / "demo.yaml.bak"
    assert not bak.exists()  # 起点:无备份(只有真覆盖才产生)
    edited = EDITOR_YAML.replace('schedule: "0 9 * * *"', 'schedule: "*/15 * * * *"')
    code, responses, _ = rpc({"id": 1, "method": "yaml.save",
                              "params": {"file": str(path), "content": edited,
                                         "expected_mtime": path.stat().st_mtime}})
    result = responses[0]["result"]
    assert code == 0
    assert result["created"] is False
    assert result["backed_up"] == str(bak)
    assert path.read_text(encoding="utf-8") == edited  # 新内容落盘
    assert bak.read_text(encoding="utf-8") == EDITOR_YAML  # .bak = 旧原文(头注释在内)
    # 单份滚动:再保存一次,.bak 换成上一次内容(永远只有最近一份留底)
    twice = edited.replace("name: 编辑器夹具", "name: 编辑器夹具二")
    _, responses, _ = rpc({"id": 2, "method": "yaml.save",
                           "params": {"file": str(path), "content": twice,
                                      "expected_mtime": result["mtime"]}})
    assert responses[0]["result"]["created"] is False
    assert path.read_text(encoding="utf-8") == twice
    assert bak.read_text(encoding="utf-8") == edited  # .bak 前移为上一次内容


def test_yaml_save_duplicate_category_id_rejected(tmp_path, monkeypatch):
    """跨文件品类 id 查重:新建内容撞既有 id → duplicate_category_id(data 带
    冲突文件),零写入(静默混品类地雷在写盘门收口)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", EDITOR_YAML))
    dup_path = plugins / "shadow.yaml"
    _, responses, _ = rpc({"id": 1, "method": "yaml.save",
                           "params": {"file": str(dup_path), "content": EDITOR_YAML,
                                      "expected_mtime": None}})
    error = responses[0]["error"]
    assert error["code"] == "duplicate_category_id"
    assert [Path(item).name for item in error["data"]["conflicts"]] == ["demo.yaml"]
    assert not dup_path.exists()
    # 改 id 后同一保存即放行(id 空间归位)
    _, responses, _ = rpc({"id": 2, "method": "yaml.save",
                           "params": {"file": str(dup_path),
                                      "content": EDITOR_YAML.replace("editor-demo", "shadow"),
                                      "expected_mtime": None}})
    assert responses[0]["result"]["created"] is True


def test_yaml_delete_roundtrip_cleans_stash(tmp_path, monkeypatch):
    """delete 往返:.bak 留底删除前原文 → 主文件删 → 连带 .disabled.json 清;
    .bak 不入列;再删 = file_not_found。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("doomed.yaml", EDITOR_YAML))
    path = plugins / "doomed.yaml"
    stash = plugins / "doomed.yaml.disabled.json"
    stash.write_text(json.dumps([{"name": "stashed", "url": "http://127.0.0.1:9/y"}],
                                ensure_ascii=False), encoding="utf-8")
    code, responses, _ = rpc({"id": 1, "method": "yaml.delete", "params": {"file": str(path)}})
    result = responses[0]["result"]
    assert code == 0
    assert result == {"file": str(path), "deleted": True,
                      "backed_up": str(plugins / "doomed.yaml.bak")}
    assert Path(result["backed_up"]).read_text(encoding="utf-8") == EDITOR_YAML  # .bak = 删除前原文
    assert not path.exists() and not stash.exists()  # 主文件 + 连带暂存清理
    # 合法空态:.bak 不入列(编辑对象只剩备份痕迹)
    _, responses, _ = rpc({"id": 2, "method": "yaml.list"})
    assert responses[0]["result"]["files"] == []
    _, responses, _ = rpc({"id": 3, "method": "yaml.delete", "params": {"file": str(path)}})
    assert responses[0]["error"]["code"] == "file_not_found"


def test_yaml_template_passes_load_category():
    """模板必过 load_category(schema 演进防腐锁);头注释指向 stocks.yaml。"""
    import yaml as yaml_module

    from myssia.schema import load_category

    code, responses, _ = rpc({"id": 1, "method": "yaml.template"})
    content = responses[0]["result"]["content"]
    assert code == 0 and "stocks.yaml" in content
    config = load_category(yaml_module.safe_load(content))
    assert config.id == "my-category" and config.name == "我的品类"
    assert len(config.sources) == 1 and config.sources[0].name == "example"


def test_yaml_secret_warning_level_and_save_not_blocked(tmp_path, monkeypatch):
    """findings 分级:secret_unknown 是 warning(valid 不翻假、保存放行且应答
    带回);env: 引用只验格式不做存在性对照;补录凭据后 warning 消失。"""
    plugins = _editor_plugins(tmp_path, monkeypatch)
    _, responses, _ = rpc({"id": 1, "method": "yaml.validate", "params": {"content": SECRET_REF_YAML}})
    result = responses[0]["result"]
    assert result["valid"] is True  # warning 不翻假
    assert result["category"] == {"id": "secret-demo", "name": "凭据夹具", "sources": 1}
    assert result["findings"] == [{
        "path": "$.push[0].target", "code": "secret_unknown", "level": "warning",
        "message": result["findings"][0]["message"],
    }]
    assert "myia/push/demo" in result["findings"][0]["message"]  # message 含凭据名
    assert "myssia secret set" in result["findings"][0]["message"]  # 与录入命令
    assert "NOT_SET_ANYWHERE" not in json.dumps(result)  # env: 不对照名单(决议 8)
    # warning 不拦保存,且应答原样带回(UI 展示)
    _, responses, _ = rpc({"id": 2, "method": "yaml.save",
                           "params": {"file": str(plugins / "secret-demo.yaml"),
                                      "content": SECRET_REF_YAML, "expected_mtime": None}})
    saved = responses[0]["result"]
    assert saved["written"] is True
    assert [finding["code"] for finding in saved["warnings"]] == ["secret_unknown"]
    # 补录凭据(先写 YAML 后补凭据是合法流)→ validate 干净
    rpc({"id": 3, "method": "secret.set",
         "params": {"name": "myia/push/demo", "value": "hook-token"}})
    _, responses, _ = rpc({"id": 4, "method": "yaml.validate", "params": {"content": SECRET_REF_YAML}})
    assert responses[0]["result"]["findings"] == []


def test_yaml_save_mtime_conflict(tmp_path, monkeypatch):
    """mtime 乐观锁:读后文件被外部(CLI/别的窗口)改过 → mtime_conflict 且
    不覆盖外部改动;重读携带新 mtime 后保存成功(UI 恢复路径)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", EDITOR_YAML))
    path = plugins / "demo.yaml"
    _, responses, _ = rpc({"id": 1, "method": "yaml.read", "params": {"file": str(path)}})
    stale = responses[0]["result"]["mtime"]
    external = EDITOR_YAML.replace("0 9 * * *", "0 10 * * *")
    path.write_text(external, encoding="utf-8")  # 读后外部改动
    _, responses, _ = rpc({"id": 2, "method": "yaml.save",
                           "params": {"file": str(path), "content": EDITOR_YAML,
                                      "expected_mtime": stale}})
    error = responses[0]["error"]
    assert error["code"] == "mtime_conflict" and error["path"] == "params.expected_mtime"
    assert error["data"]["expected_mtime"] == stale
    assert error["data"]["current_mtime"] != stale
    assert path.read_text(encoding="utf-8") == external  # 不覆盖外部改动
    _, responses, _ = rpc({"id": 3, "method": "yaml.read", "params": {"file": str(path)}})
    _, responses, _ = rpc({"id": 4, "method": "yaml.save",
                           "params": {"file": str(path), "content": EDITOR_YAML,
                                      "expected_mtime": responses[0]["result"]["mtime"]}})
    assert responses[0]["result"]["written"] is True


def test_yaml_read_limits_and_encoding(tmp_path, monkeypatch):
    """read 错误面补全:>1 MiB → file_too_large;非 UTF-8 → invalid_encoding;
    不存在 → file_not_found。"""
    plugins = _editor_plugins(tmp_path, monkeypatch)
    big = plugins / "big.yaml"
    big.write_text("x" * (entry.YAML_MAX_BYTES + 1), encoding="utf-8")
    _, responses, _ = rpc({"id": 1, "method": "yaml.read", "params": {"file": str(big)}})
    error = responses[0]["error"]
    assert error["code"] == "file_too_large"
    assert error["data"] == {"size": entry.YAML_MAX_BYTES + 1, "limit": entry.YAML_MAX_BYTES}
    garbled = plugins / "gbk.yaml"
    garbled.write_bytes(b"\xd6\xd0\xce\xc4 not-utf8")  # GBK 字节,非 UTF-8
    _, responses, _ = rpc({"id": 2, "method": "yaml.read", "params": {"file": str(garbled)}})
    assert responses[0]["error"]["code"] == "invalid_encoding"
    _, responses, _ = rpc({"id": 3, "method": "yaml.read",
                           "params": {"file": str(plugins / "ghost.yaml")}})
    assert responses[0]["error"]["code"] == "file_not_found"


def test_sources_write_backup_stops_comment_loss(tmp_path):
    """启停止血(决议 2)+ 根治(10-03-yaml-toggle-comments 已落地):点一次
    启停,.bak 保有操作前的带注释原文(第二条保险带);主文件不再被 safe_dump
    整份重写抹注释 —— 文本手术逐字节保真,只摘目标条目整段。"""
    path = Path(write_yaml(tmp_path, COMMENTED_TOGGLE_YAML, "toggle.yaml"))
    original = path.read_text(encoding="utf-8")
    code, responses, _ = rpc({"id": 1, "method": "sources.write",
                              "params": {"file": str(path), "disable": ["drop-me"]}})
    assert code == 0 and responses[0]["result"]["written"] is True
    bak = tmp_path / "toggle.yaml.bak"
    assert bak.read_text(encoding="utf-8") == original  # .bak = 带注释原文
    after = path.read_text(encoding="utf-8")
    assert "顶部注释" in after  # 根治:文本手术保注释,不再 safe_dump 重写
    assert "drop-me" not in after  # 摘除的只有目标条目(暂存入独立 stash 文件)


def test_sources_write_then_yaml_save_mutex_by_mtime(tmp_path, monkeypatch):
    """两写路径互斥:编辑器读到的 mtime 被 sources.write 顶掉 → yaml.save 撞
    mtime_conflict(靠乐观锁互斥,不靠运气);重读后保存恢复。"""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("toggle.yaml", COMMENTED_TOGGLE_YAML))
    path = plugins / "toggle.yaml"
    _, responses, _ = rpc({"id": 1, "method": "yaml.read", "params": {"file": str(path)}})
    stale = responses[0]["result"]["mtime"]
    _, responses, _ = rpc({"id": 2, "method": "sources.write",
                           "params": {"file": str(path), "disable": ["drop-me"]}})
    assert responses[0]["result"]["written"] is True
    _, responses, _ = rpc({"id": 3, "method": "yaml.save",
                           "params": {"file": str(path), "content": COMMENTED_TOGGLE_YAML,
                                      "expected_mtime": stale}})
    assert responses[0]["error"]["code"] == "mtime_conflict"
    # 重读 → 携带启停后的新 mtime → 编辑保存放行(注释随原文写回)
    _, responses, _ = rpc({"id": 4, "method": "yaml.read", "params": {"file": str(path)}})
    fresh = responses[0]["result"]["mtime"]
    _, responses, _ = rpc({"id": 5, "method": "yaml.save",
                           "params": {"file": str(path), "content": COMMENTED_TOGGLE_YAML,
                                      "expected_mtime": fresh}})
    assert responses[0]["result"]["written"] is True
    assert "顶部注释" in path.read_text(encoding="utf-8")  # 编辑链路注释保真


# ---------------------------------------------------------------------------
# image.config.*:看图配置两方法往返(10-03-vision-pipeline 拆四留二:
# image.import/ocr/analyze/status 四方法与两事件用例已删,保留设置屏
# VisionForm 依赖的 config.read/save;零外网零真实钥匙链;MYIA_HOME 指向
# tmp 数据根)
# ---------------------------------------------------------------------------

#: 完整合法看图配置(云端 key 引用在用例里按需注入)。
VISION_CONFIG_OK = {
    "channel_default": "local",
    "local": {"base_url": "http://127.0.0.1:8080/v1", "model": "/models/qwen3-vl-8b-mlx"},
    "cloud": {"base_url": "https://open.bigmodel.cn/api/paas/v4", "model": "glm-4.6v",
              "api_key": None},
    "ocr": {"enabled": True, "engine_default": "vision"},
}


def test_image_config_read_defaults_without_file(tmp_path, monkeypatch):
    """config.read:文件不存在 = 全缺省(exists=false,合法未配置态)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    code, responses, _ = rpc({"id": 1, "method": "image.config.read", "params": {}})
    result = responses[0]["result"]
    assert result["exists"] is False
    assert result["file"] == str(tmp_path / "home" / "vision.yaml")
    assert result["config"]["channel_default"] == "local"
    assert result["config"]["cloud"]["model"] == "glm-4.6v"
    assert result["config"]["cloud"]["api_key"] is None
    assert result["config"]["ocr"]["engine_default"] == "vision"


def test_image_config_save_and_read_roundtrip(tmp_path, monkeypatch):
    """config.save→read 往返:引用原样落盘,keychain 引用不回明文(值无从谈起)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    config = dict(VISION_CONFIG_OK)
    config["cloud"] = {"base_url": "https://open.bigmodel.cn/api/paas/v4",
                       "model": "glm-4.6v", "api_key": "keychain:myia/image/api_key"}
    config["ocr"] = {"enabled": True, "engine_default": "rapidocr"}
    code, responses, _ = rpc({"id": 1, "method": "image.config.save",
                              "params": {"config": config}})
    assert responses[0]["result"]["ok"] is True
    text = (tmp_path / "home" / "vision.yaml").read_text(encoding="utf-8")
    assert "keychain:myia/image/api_key" in text

    code, responses, _ = rpc({"id": 2, "method": "image.config.read", "params": {}})
    result = responses[0]["result"]
    assert result["exists"] is True
    assert result["config"]["ocr"]["engine_default"] == "rapidocr"
    assert result["config"]["cloud"]["api_key"] == "keychain:myia/image/api_key"


def test_image_config_save_plaintext_rejected_zero_write(tmp_path, monkeypatch):
    """config.save:明文 key / 非法引擎 → image_config_invalid 且零写入。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    bad = dict(VISION_CONFIG_OK)
    bad["cloud"] = {**bad["cloud"], "api_key": "sk-plaintext"}
    code, responses, _ = rpc({"id": 1, "method": "image.config.save",
                              "params": {"config": bad}})
    error = responses[0]["error"]
    assert error["code"] == "image_config_invalid"
    assert error["data"]["error_type"] == "credential_plaintext"
    assert not (tmp_path / "home" / "vision.yaml").exists()  # 拒载 = 零写入

    bad_engine = dict(VISION_CONFIG_OK)
    bad_engine["ocr"] = {"enabled": True, "engine_default": "paddle"}
    code, responses, _ = rpc({"id": 2, "method": "image.config.save",
                              "params": {"config": bad_engine}})
    assert responses[0]["error"]["code"] == "image_config_invalid"
    assert responses[0]["error"]["data"]["error_type"] == "invalid_engine"


# ---------------------------------------------------------------------------
# channels.list / channels.refresh / channels.alias / push.write
# (消息屏协议,task 10-03-messaging-ui;追加式新增,契约钉死于任务档 design.md §D2)
# ---------------------------------------------------------------------------

#: 消息屏品类夹具:feishu push 条目带 targets(同平台约束正例形态)。
MESSAGING_YAML = """
id: messaging-demo
name: 消息屏夹具
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:9/list"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.data[*].title"
        url: "$.data[*].url"
classify:
  builtin: false
push:
  - channel: feishu_card
    targets:
      - feishu:AI中转站合伙人群
      - feishu:羊毛反馈群
    route:
      - when: "category == 'freebie'"
        mode: immediate
"""


def _messaging_home(tmp_path: Path, monkeypatch, yaml_text: str | None = MESSAGING_YAML) -> Path:
    """home 模式夹具:MYIA_HOME 指向 tmp home,plugins 内放消息屏品类 YAML。"""
    home = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(home))
    plugins = home / "plugins"
    plugins.mkdir(parents=True, exist_ok=True)
    if yaml_text is not None:
        (plugins / "messaging-demo.yaml").write_text(yaml_text, encoding="utf-8")
    return home


def _write_directory(home: Path, platforms: dict, updated_at: str | None = None) -> None:
    """直编 channel_directory.json(夹具数据源;格式=directory.py 持久形态)。"""
    import json as _json

    payload = {"updated_at": updated_at, "platforms": platforms}
    (home / "channel_directory.json").write_text(
        _json.dumps(payload, ensure_ascii=False), encoding="utf-8"
    )


def test_channels_list_four_views(tmp_path, monkeypatch):
    """channels.list 正例:目录+别名+死信+规则四视图,条目名已套别名覆盖。"""
    home = _messaging_home(tmp_path, monkeypatch)
    _write_directory(
        home,
        {
            "feishu": [
                {"platform": "feishu", "chat_id": "oc_1", "name": "AI中转站合伙人群",
                 "type": "group", "thread_id": None, "last_seen": 1760000000.0},
                {"platform": "feishu", "chat_id": "oc_2", "name": "羊毛反馈群",
                 "type": "group", "thread_id": None, "last_seen": None},
            ]
        },
        updated_at="2026-10-03T00:00:00",
    )
    (home / "channel_aliases.json").write_text(
        json.dumps({"feishu": {"oc_2": "手动别名群"}}, ensure_ascii=False), encoding="utf-8"
    )
    (home / "delivery_ledger.json").write_text(
        json.dumps({"feishu:oc_2": {"reason": "forbidden: bot was blocked",
                                    "marked_at": 1760000001.0}}, ensure_ascii=False),
        encoding="utf-8",
    )

    code, responses, _ = rpc({"id": 1, "method": "channels.list", "params": {}})
    assert code == 0
    result = responses[0]["result"]
    assert result["data_root"] == str(home)
    assert result["updated_at"] == "2026-10-03T00:00:00"
    # 目录条目名已套别名覆盖(oc_2 显示手动别名),chat_id/type/last_seen 原样
    entries = result["platforms"]["feishu"]
    assert [e["chat_id"] for e in entries] == ["oc_1", "oc_2"]
    assert entries[1]["name"] == "手动别名群"
    assert entries[0]["last_seen"] == 1760000000.0
    # 别名原始覆盖层 + 死信键快照
    assert result["aliases"] == {"feishu": {"oc_2": "手动别名群"}}
    assert result["dead"] == ["feishu:oc_2"]
    # 规则视图:push 条目带 platform 映射与 targets 回显 + raw 最小无损写回 base
    rule = next(r for r in result["rules"] if r["parse_ok"])
    assert rule["category_id"] == "messaging-demo"
    assert rule["entries"] == [
        {"index": 0, "channel": "feishu_card", "platform": "feishu",
         "targets": ["feishu:AI中转站合伙人群", "feishu:羊毛反馈群"],
         "has_template": False, "route_count": 1,
         "raw": {
             "channel": "feishu_card",
             "targets": ["feishu:AI中转站合伙人群", "feishu:羊毛反馈群"],
             "route": [{"when": "category == 'freebie'", "mode": "immediate"}],
         }},
    ]
    # raw 原样回传能过 push.write 同门(往返闭环:UI 拿 raw 改 targets 提交)
    code, responses, _ = rpc(
        {"id": 2, "method": "push.write",
         "params": {"file": rule["file"], "push": [rule["entries"][0]["raw"]]}},
    )
    assert responses[0]["result"]["written"] is True


def test_channels_list_empty_state_is_legal(tmp_path, monkeypatch):
    """零平台零规则 = 合法空态(UI 给「先配平台凭据」指引,不报错)。"""
    _messaging_home(tmp_path, monkeypatch, yaml_text=None)
    code, responses, _ = rpc({"id": 1, "method": "channels.list", "params": {}})
    assert code == 0
    result = responses[0]["result"]
    assert result["platforms"] == {}
    assert result["aliases"] == {}
    assert result["dead"] == []
    assert result["rules"] == []


def test_channels_refresh_unknown_platform_structured(tmp_path, monkeypatch):
    """refresh 未知平台:unknown_platform + allowed 名单,旧目录不动。

    样例平台名用 icq(从未注册);原用 slack,但 W3 长尾接线
    (10-03-messaging-w3-longtail)后 slack 已注册进 PLATFORMS——注册平台
    走 discover_not_supported 族,不再是 unknown_platform。
    """
    home = _messaging_home(tmp_path, monkeypatch, yaml_text=None)
    _write_directory(home, {"feishu": []})
    code, responses, _ = rpc(
        {"id": 1, "method": "channels.refresh", "params": {"platform": "icq"}},
    )
    assert code == 0
    error = responses[0]["error"]
    assert error["code"] == "unknown_platform"
    assert "icq" in error["message"]
    assert "feishu" in error["data"]["allowed"]
    # 旧目录文件未被触碰
    assert json.loads((home / "channel_directory.json").read_text("utf-8"))["platforms"] == {"feishu": []}


def test_channels_refresh_discover_failure_keeps_old_bucket(tmp_path, monkeypatch):
    """refresh 发现失败(凭据缺失族):结构化 channel_refresh_failed,旧桶不动。"""
    from myssia.push.base import PushSendError

    home = _messaging_home(tmp_path, monkeypatch, yaml_text=None)
    _write_directory(home, {"feishu": [
        {"platform": "feishu", "chat_id": "oc_old", "name": "旧桶群", "type": "group",
         "thread_id": None, "last_seen": None}]})

    class _BrokenAdapter:
        def discover_directory(self):
            raise PushSendError("credential_not_found", "飞书 bot 凭据未配置")

    monkeypatch.setattr("myssia.push.PLATFORMS", {"feishu": _BrokenAdapter})
    code, responses, _ = rpc(
        {"id": 1, "method": "channels.refresh", "params": {"platform": "feishu"}},
    )
    error = responses[0]["error"]
    assert error["code"] == "channel_refresh_failed"
    assert error["data"]["code"] == "credential_not_found"
    # 旧桶逐字节未动
    assert json.loads((home / "channel_directory.json").read_text("utf-8"))["platforms"]["feishu"][0][
        "chat_id"
    ] == "oc_old"


def test_channels_refresh_merges_and_persists(tmp_path, monkeypatch):
    """refresh 正例:发现条目桶替换落盘,应答 merged=n + entries;updated_at 前移。"""
    from myssia.push.directory import ChannelEntry

    home = _messaging_home(tmp_path, monkeypatch, yaml_text=None)

    class _FakeAdapter:
        async def discover_directory(self):
            return [
                ChannelEntry(platform="feishu", chat_id="oc_1", name="AI中转站合伙人群", type="group"),
                ChannelEntry(platform="feishu", chat_id="oc_2", name="羊毛反馈群", type="group"),
            ]

    monkeypatch.setattr("myssia.push.PLATFORMS", {"feishu": _FakeAdapter})
    code, responses, _ = rpc(
        {"id": 1, "method": "channels.refresh", "params": {"platform": "feishu"}},
    )
    assert code == 0
    result = responses[0]["result"]
    assert result["platform"] == "feishu"
    assert result["merged"] == 2
    assert [e["name"] for e in result["entries"]] == ["AI中转站合伙人群", "羊毛反馈群"]
    # 落盘可复核:重开目录读到同一桶 + updated_at 已写(供 list 视图)
    persisted = json.loads((home / "channel_directory.json").read_text("utf-8"))
    assert len(persisted["platforms"]["feishu"]) == 2
    assert persisted["updated_at"] is not None
    code, responses, _ = rpc({"id": 2, "method": "channels.list", "params": {}})
    assert responses[0]["result"]["updated_at"] == persisted["updated_at"]


def test_channels_refresh_no_discovery_platform_structured(tmp_path, monkeypatch):
    """W2 平台(ntfy/dingtalk/wecom)refresh:无自动发现 = discover_not_supported
    结构化说明(与 telegram 被动积累同族),不是 channel_refresh_failed;旧桶不动。"""
    from myssia.push import NtfyChannel

    home = _messaging_home(tmp_path, monkeypatch, yaml_text=None)
    _write_directory(home, {"ntfy": [
        {"platform": "ntfy", "chat_id": "games", "name": "游戏台", "type": "channel",
         "thread_id": None, "last_seen": None}]})

    monkeypatch.setattr("myssia.push.PLATFORMS", {"ntfy": NtfyChannel})
    code, responses, _ = rpc(
        {"id": 1, "method": "channels.refresh", "params": {"platform": "ntfy"}},
    )
    assert code == 0
    error = responses[0]["error"]
    assert error["code"] == "discover_not_supported"
    assert "无自动发现" in error["message"]
    assert error["data"]["platform"] == "ntfy"
    # 旧桶逐字节未动(别名登记的条目不被「刷新」清掉)
    assert json.loads((home / "channel_directory.json").read_text("utf-8"))["platforms"][
        "ntfy"
    ][0]["chat_id"] == "games"


def test_channels_alias_set_delete_roundtrip(tmp_path, monkeypatch):
    """alias 正例:set 落别名文件且立即生效;delete 摘除,未发现占位条目随之消失。"""
    home = _messaging_home(tmp_path, monkeypatch, yaml_text=None)
    _write_directory(home, {"feishu": [
        {"platform": "feishu", "chat_id": "oc_1", "name": "原名", "type": "group",
         "thread_id": None, "last_seen": None}]})

    code, responses, _ = rpc(
        {"id": 1, "method": "channels.alias",
         "params": {"platform": "feishu", "chat_id": "oc_1", "name": "新别名"}},
    )
    assert code == 0
    assert responses[0]["result"] == {
        "platform": "feishu", "chat_id": "oc_1", "deleted": False, "name": "新别名",
    }
    # 别名文件持久形态 + list 视图条目名已覆盖
    assert json.loads((home / "channel_aliases.json").read_text("utf-8")) == {
        "feishu": {"oc_1": "新别名"}}
    code, responses, _ = rpc({"id": 2, "method": "channels.list", "params": {}})
    assert responses[0]["result"]["platforms"]["feishu"][0]["name"] == "新别名"

    # delete:name=null 摘除别名;目录回退发现名
    code, responses, _ = rpc(
        {"id": 3, "method": "channels.alias",
         "params": {"platform": "feishu", "chat_id": "oc_1", "name": None}},
    )
    assert responses[0]["result"]["deleted"] is True
    assert json.loads((home / "channel_aliases.json").read_text("utf-8")) == {}
    code, responses, _ = rpc({"id": 4, "method": "channels.list", "params": {}})
    assert responses[0]["result"]["platforms"]["feishu"][0]["name"] == "原名"

    # set 未知 chat_id = 合法占位别名(新群可先命名后首聊,directory 语义)
    code, responses, _ = rpc(
        {"id": 5, "method": "channels.alias",
         "params": {"platform": "feishu", "chat_id": "oc_new", "name": "占位群"}},
    )
    assert responses[0]["result"]["name"] == "占位群"
    code, responses, _ = rpc({"id": 6, "method": "channels.list", "params": {}})
    assert {e["chat_id"] for e in responses[0]["result"]["platforms"]["feishu"]} == {
        "oc_1", "oc_new"}


def test_channels_alias_param_validation(tmp_path, monkeypatch):
    """alias 参数形状:缺 platform/chat_id、name 类型错 → invalid_params 定位。"""
    _messaging_home(tmp_path, monkeypatch, yaml_text=None)
    code, responses, _ = rpc(
        {"id": 1, "method": "channels.alias", "params": {"chat_id": "oc_1", "name": "x"}},
    )
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.platform"
    code, responses, _ = rpc(
        {"id": 2, "method": "channels.alias",
         "params": {"platform": "feishu", "chat_id": "oc_1", "name": 42}},
    )
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.name"


def test_push_write_full_replacement_roundtrip(tmp_path, monkeypatch):
    """push.write 正例:targets 全量替换落盘;注释/其他节逐字节保留;.bak 留底。"""
    from myssia.schema import load_category_file

    home = _messaging_home(tmp_path, monkeypatch)
    yaml_path = home / "plugins" / "messaging-demo.yaml"
    before = yaml_path.read_text(encoding="utf-8")

    new_push = [
        {
            "channel": "feishu_card",
            "targets": ["feishu:AI中转站合伙人群"],
            "route": [{"when": "category == 'freebie'", "mode": "immediate"}],
        },
        {"channel": "stdout"},
    ]
    code, responses, _ = rpc(
        {"id": 1, "method": "push.write",
         "params": {"file": str(yaml_path), "push": new_push}},
    )
    assert code == 0
    result = responses[0]["result"]
    assert result["written"] is True
    assert result["changed"] is True
    # myssia run 同门:写回文件可装载,push 逐条对上
    config = load_category_file(yaml_path)
    assert [push.channel for push in config.push] == ["feishu_card", "stdout"]
    assert config.push[0].targets == ["feishu:AI中转站合伙人群"]
    # push 之外逐字节不动(sources/classify/头部原文仍在;push 块本身被重写)
    after = yaml_path.read_text(encoding="utf-8")
    assert "title: \"$.data[*].title\"" in after
    assert "builtin: false" in after
    assert after[: after.index("push:")] == before[: before.index("push:")]
    # .bak 留底 = 手术前原文
    assert (home / "plugins" / "messaging-demo.yaml.bak").read_text(encoding="utf-8") == before


def test_push_write_bad_targets_rejected_zero_write(tmp_path, monkeypatch):
    """push.write 拒写:坏 targets(跨平台前缀)→ category_invalid 且文件未变。"""
    from myssia.schema import load_category_file  # noqa: F401 — 门禁语义锚点

    home = _messaging_home(tmp_path, monkeypatch)
    yaml_path = home / "plugins" / "messaging-demo.yaml"
    before = yaml_path.read_text(encoding="utf-8")

    bad_push = [
        {"channel": "feishu_card", "targets": ["telegram:别的平台群"]},
    ]
    code, responses, _ = rpc(
        {"id": 1, "method": "push.write",
         "params": {"file": str(yaml_path), "push": bad_push}},
    )
    assert code == 0  # 业务错误在应答对象里,协议流不断
    error = responses[0]["error"]
    assert error["code"] == "category_invalid"
    assert error["path"] == "params.push"
    details = error["data"]["errors"]
    assert details and details[0]["code"] == "platform_mismatch"
    # 拒写 = 零写入:文件与 .bak 均未变
    assert yaml_path.read_text(encoding="utf-8") == before
    assert not (home / "plugins" / "messaging-demo.yaml.bak").exists()


def test_push_write_empty_array_removes_section(tmp_path, monkeypatch):
    """push.write 空数组 = 摘除 push 节(品类允许无 push);再写回可复原。"""
    from myssia.schema import load_category_file

    home = _messaging_home(tmp_path, monkeypatch)
    yaml_path = home / "plugins" / "messaging-demo.yaml"

    code, responses, _ = rpc(
        {"id": 1, "method": "push.write",
         "params": {"file": str(yaml_path), "push": []}},
    )
    assert responses[0]["result"]["changed"] is True
    config = load_category_file(yaml_path)
    assert config.push == []
    text = yaml_path.read_text(encoding="utf-8")
    assert "push:" not in text

    # 无 push 节 + 空数组 = 无操作(changed=false,不落盘)
    mtime_before = yaml_path.stat().st_mtime_ns
    code, responses, _ = rpc(
        {"id": 2, "method": "push.write",
         "params": {"file": str(yaml_path), "push": []}},
    )
    assert responses[0]["result"] == {
        "file": str(yaml_path), "written": True, "changed": False, "push": []}
    assert yaml_path.stat().st_mtime_ns == mtime_before

    # 无 push 节 + 非空数组 = EOF 追加(push 节重建,可装载)
    code, responses, _ = rpc(
        {"id": 3, "method": "push.write",
         "params": {"file": str(yaml_path),
                    "push": [{"channel": "stdout"}]}},
    )
    assert responses[0]["result"]["changed"] is True
    assert [push.channel for push in load_category_file(yaml_path).push] == ["stdout"]


def test_push_write_fence_and_param_refusals(tmp_path, monkeypatch):
    """push.write 围栏与参数:越出 plugins 目录 / 缺 push 数组 / 文件不存在。"""
    home = _messaging_home(tmp_path, monkeypatch)
    yaml_path = home / "plugins" / "messaging-demo.yaml"

    code, responses, _ = rpc(
        {"id": 1, "method": "push.write",
         "params": {"file": "/tmp/elsewhere.yaml", "push": [{"channel": "stdout"}]}},
    )
    assert responses[0]["error"]["code"] == "path_outside_root"

    code, responses, _ = rpc(
        {"id": 2, "method": "push.write",
         "params": {"file": str(yaml_path), "push": "not-a-list"}},
    )
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.push"

    code, responses, _ = rpc(
        {"id": 3, "method": "push.write",
         "params": {"file": str(home / "plugins" / "nope.yaml"),
                    "push": [{"channel": "stdout"}]}},
    )
    assert responses[0]["error"]["code"] == "file_not_found"


def test_push_write_mid_file_block_and_template_roundtrip(tmp_path, monkeypatch):
    """push 块夹在文件中部(plugin: 节在后)同样可换;多行模板 literal 往返保真。"""
    from myssia.schema import load_category_file

    home = _messaging_home(
        tmp_path,
        monkeypatch,
        yaml_text=(
            'id: messaging-mid\n'
            'name: 中部夹具\n'
            'schedule: "0 9 * * *"\n'
            'sources:\n'
            '  - name: local-api\n'
            '    engine: direct_api\n'
            '    url: "http://127.0.0.1:9/list"\n'
            '    rate_limit:\n'
            '      qps: 1000.0\n'
            '      respect_robots: false\n'
            '    retry: 0\n'
            '    extract:\n'
            '      type: json_path\n'
            '      fields:\n'
            '        title: "$.a"\n'
            '        url: "$.b"\n'
            '# 头部注释:push 之前的内容逐字节不动\n'
            'push:\n'
            '  - channel: stdout\n'
            'plugin:\n'
            '  id: myssia-mid\n'
            '  modes:\n'
            '    local:\n'
            '      compose: docker-compose.yml\n'
        ),
    )
    yaml_path = home / "plugins" / "messaging-demo.yaml"
    template = "**速报 · {{ date }}**\n{% for item in items %}\n- {{ item.title }}\n{% endfor %}\n"
    new_push = [
        {
            "channel": "feishu_card",
            "targets": ["feishu:中部群"],
            "template": template,
        }
    ]
    code, responses, _ = rpc(
        {"id": 1, "method": "push.write",
         "params": {"file": str(yaml_path), "push": new_push}},
    )
    assert code == 0
    assert responses[0]["result"]["changed"] is True
    config = load_category_file(yaml_path)
    assert config.push[0].template == template  # 多行模板逐字节往返
    assert config.plugin is not None and config.plugin.id == "myssia-mid"  # 后节未动
    text = yaml_path.read_text(encoding="utf-8")
    assert "# 头部注释:push 之前的内容逐字节不动" in text
    assert text.index("plugin:") > text.index("push:")  # push 仍在 plugin 之前


# ---------------------------------------------------------------------------
# v1.1.2 桌面对齐批(10-03-v112-desktop-parity):run.cancel / runs.list /
# secret.delete / sources.test / store.items 游标与搜索(C2/C3/C5/C13/C1)
# ---------------------------------------------------------------------------


class _SlowApiHandler(http.server.BaseHTTPRequestHandler):
    """拖延 API(run.cancel 夹具):响应前睡 30s,保证取消窗口足够长。"""

    def do_GET(self):  # noqa: N802
        try:
            time.sleep(30)
            body = json.dumps(API_JSON, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception:  # noqa: BLE001 — 客户端被杀后写管道失败:静默收场
            self.close_connection = True

    def log_message(self, *args):  # 静默
        pass


@pytest.fixture()
def slow_api():
    """临时本地慢直 API(线程化:每连接独立,客户端被杀不阻塞后续)。"""
    with socketserver.ThreadingTCPServer(("127.0.0.1", 0), _SlowApiHandler) as srv:
        port = srv.server_address[1]
        thread = threading.Thread(target=srv.serve_forever, daemon=True)
        thread.start()
        yield port
        srv.shutdown()


def test_run_cancel_full_roundtrip(tmp_path, slow_api):
    """C2 run.cancel 全往返:慢源 run 进行中 → killpg 取消 → completed 信号终局
    status=cancelled → run.status 终态 → 子进程收尸(poll is not None)。

    dev 测试边界如实注记:此形态只见单进程(无 bootloader);onefile 双进程
    「孙进程不残留」的最终证据在装机冒烟,此处绿不冒充该验收。
    """
    yaml_path = write_yaml(tmp_path, VALID_YAML.replace("{port}", str(slow_api)), "slow.yaml")
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 1, "method": "run.start",
                                    "params": {"yaml": yaml_path, "db": str(tmp_path / "c.db")}}) + "\n")
    assert entry.serve(stdin=stdin, stdout=out) == 0
    responses, _ = split_stream(out)
    run_id = responses[0]["result"]["run_id"]

    deadline = time.monotonic() + 30
    proc = None
    while time.monotonic() < deadline:
        proc = entry._RUN_PROCS.get(run_id)
        if proc is not None and proc.poll() is None:
            break
        time.sleep(0.05)
    assert proc is not None and proc.poll() is None, "run 子进程未在期限内起跑"

    result = entry._m_run_cancel({})
    assert result == {"run_id": run_id, "cancelled": True, "state": "running"}

    completed = wait_completed(out, run_id)
    assert completed["exit_code"] is not None and completed["exit_code"] < 0  # 信号终局
    assert completed["status"] == "cancelled"
    assert proc.poll() is not None  # 子进程已收尸(run.cancel 的直接物证)

    code, status_resp, _ = rpc({"id": 2, "method": "run.status", "params": {"run_id": run_id}})
    record = status_resp[0]["result"]["runs"][0]
    assert record["state"] == "done" and record["status"] == "cancelled"
    assert entry._ACTIVE_RUN_ID is None  # 单飞位已释放


def test_run_cancel_refusals():
    """C2 错误矩阵:未知 id / 无活跃 run = run_not_found;已终态 = run_not_active。"""
    code, responses, _ = rpc({"id": 1, "method": "run.cancel", "params": {"run_id": 424242}})
    assert responses[0]["error"]["code"] == "run_not_found"
    code, responses, _ = rpc({"id": 2, "method": "run.cancel", "params": {}})
    assert responses[0]["error"]["code"] == "run_not_found"  # 无进行中 run
    entry._RUNS[7] = {"run_id": 7, "state": "done", "status": "success"}
    code, responses, _ = rpc({"id": 3, "method": "run.cancel", "params": {"run_id": 7}})
    error = responses[0]["error"]
    assert error["code"] == "run_not_active" and error["data"]["state"] == "done"


def test_runs_list_reads_table_newest_first(tmp_path):
    """C3 runs.list:直读 runs 表(新→旧)—— 内存注册表为空(= sidecar 重启后)
    历史仍可达;category 过滤 + limit 钳制;非整数 limit 拒。"""
    db = tmp_path / "runs.db"
    store = SQLiteStore(str(db))
    for category in ("proto-demo", "proto-demo", "other"):
        run_id = store.start_run(category)
        store.finish_run(run_id, status="success", stats={"items_retained": 1})
    store.close()
    code, responses, _ = rpc({"id": 1, "method": "runs.list", "params": {"db": str(db)}})
    result = responses[0]["result"]
    assert result["count"] == 3
    ids = [row["run_id"] for row in result["runs"]]
    assert ids == sorted(ids, reverse=True)  # 新→旧
    assert set(result["runs"][0]) == {
        "run_id", "category", "status", "started_at", "finished_at", "stats", "steps", "error",
    }
    code, responses, _ = rpc({"id": 2, "method": "runs.list",
                              "params": {"db": str(db), "category": "proto-demo", "limit": 1}})
    assert responses[0]["result"]["count"] == 1
    assert responses[0]["result"]["runs"][0]["category"] == "proto-demo"
    code, responses, _ = rpc({"id": 3, "method": "runs.list", "params": {"db": str(db), "limit": 500}})
    assert responses[0]["result"]["count"] == 3  # 钳制 [1,200] 不报错
    code, responses, _ = rpc({"id": 4, "method": "runs.list", "params": {"db": str(db), "limit": "x"}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_runs_trend_daily_outcomes_utc(tmp_path):
    """G6 runs.trend:runs 表逐日×status 聚合(旧→新)—— statuses.running 如实
    计数(分母剔除是前端装配行为,归 vitest);category 过滤 + 钳制 + 空态。"""
    from datetime import datetime, timedelta, timezone

    db = tmp_path / "runs-trend.db"
    store = SQLiteStore(str(db))
    now = datetime.now(timezone.utc)

    def backdate(run_id: int, started_at: datetime) -> None:
        store.conn.execute(
            "UPDATE runs SET started_at = ? WHERE id = ?",
            (started_at.isoformat(), run_id),
        )
        store.conn.commit()

    # 今天:demo success×2 + failed×1;昨天:demo 只 start 不 finish(running×1);
    # 40 天前:partial×1(days=14 窗口外)
    for _ in range(2):
        run_id = store.start_run("demo")
        backdate(run_id, now)
        store.finish_run(run_id, status="success")
    run_id = store.start_run("demo")
    backdate(run_id, now)
    store.finish_run(run_id, status="failed")
    run_id = store.start_run("demo")
    backdate(run_id, now - timedelta(days=1))  # running:不 finish
    run_id = store.start_run("demo")
    backdate(run_id, now - timedelta(days=40))
    store.finish_run(run_id, status="partial")
    # 今天:另一品类 other success×1(category 过滤用)
    run_id = store.start_run("other")
    backdate(run_id, now)
    store.finish_run(run_id, status="success")
    store.close()

    code, responses, _ = rpc(
        {"id": 1, "method": "runs.trend", "params": {"db": str(db), "days": 14}},
    )
    days = responses[0]["result"]["days"]
    assert [row["date"] for row in days] == sorted({row["date"] for row in days})  # 旧→新
    by_date = {row["date"]: row for row in days}
    today = by_date[now.date().isoformat()]
    assert today["total"] == 4  # demo 3 + other 1(窗口右端含今天)
    assert today["statuses"] == {"success": 3, "failed": 1}
    yesterday = by_date[(now - timedelta(days=1)).date().isoformat()]
    assert yesterday["total"] == 1
    assert yesterday["statuses"] == {"running": 1}  # running 如实计数(不在此剔除)
    assert (now - timedelta(days=40)).date().isoformat() not in by_date  # 窗外不入

    # category 过滤:demo 窗口 = 今天 3 + 昨天 running 1
    code, responses, _ = rpc(
        {"id": 2, "method": "runs.trend",
         "params": {"db": str(db), "days": 14, "category": "demo"}},
    )
    demo = {row["date"]: row for row in responses[0]["result"]["days"]}
    assert demo[now.date().isoformat()]["total"] == 3
    assert (now - timedelta(days=1)).date().isoformat() in demo
    # days 钳制:0 → 1(只剩今天)、91 → 90 不报错
    code, responses, _ = rpc(
        {"id": 3, "method": "runs.trend", "params": {"db": str(db), "days": 0}},
    )
    zero = responses[0]["result"]["days"]
    assert [row["date"] for row in zero] == [now.date().isoformat()]
    code, responses, _ = rpc(
        {"id": 4, "method": "runs.trend", "params": {"db": str(db), "days": 91}},
    )
    # 91 → 90 不报错;90 天窗含 40 天前的 partial 行(14 天窗不含,两响应由此可分)
    wide = {row["date"]: row for row in responses[0]["result"]["days"]}
    assert wide[(now - timedelta(days=40)).date().isoformat()]["statuses"] == {"partial": 1}
    # 参数形状:days 非整数/bool、category 空串 = invalid_params
    for bad_params in ({"days": "7"}, {"days": True}, {"category": ""}):
        code, responses, _ = rpc(
            {"id": 5, "method": "runs.trend", "params": {"db": str(db), **bad_params}},
        )
        assert responses[0]["error"]["code"] == "invalid_params"

    # 空态:零 run 库 → {"days": []}(合法空态,非错误)
    empty_db = tmp_path / "empty.db"
    SQLiteStore(str(empty_db)).close()
    code, responses, _ = rpc(
        {"id": 6, "method": "runs.trend", "params": {"db": str(empty_db)}},
    )
    assert responses[0]["result"] == {"days": []}


def test_secret_delete_roundtrip():
    """C5 secret.delete:删除后 secret.list 不再列出;二次删除 secret_not_found。"""
    code, responses, _ = rpc({"id": 1, "method": "secret.set",
                              "params": {"name": "myia/llm/api_key", "value": "v"}})
    assert responses[0]["result"]["stored"] is True
    code, responses, _ = rpc({"id": 2, "method": "secret.list", "params": {}})
    assert "myia/llm/api_key" in responses[0]["result"]["names"]
    code, responses, _ = rpc({"id": 3, "method": "secret.delete",
                              "params": {"name": "myia/llm/api_key"}})
    assert responses[0]["result"] == {"name": "myia/llm/api_key", "deleted": True}
    code, responses, _ = rpc({"id": 4, "method": "secret.list", "params": {}})
    assert "myia/llm/api_key" not in responses[0]["result"]["names"]
    code, responses, _ = rpc({"id": 5, "method": "secret.delete",
                              "params": {"name": "myia/llm/api_key"}})
    assert responses[0]["error"]["code"] == "secret_not_found"
    code, responses, _ = rpc({"id": 6, "method": "secret.delete", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_store_items_same_timestamp_pagination_to_exhaustion(tmp_path):
    """C1 复合游标:同刻 first_seen 条目(7)> 单页 limit(3),before+before_id
    翻页推进直至取尽(sum == 7 且零重复);单 before 会整批跳过同刻条目(对照)。"""
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord
    db = tmp_path / "same.db"
    store = SQLiteStore(str(db))
    moment = datetime(2026, 10, 2, 8, 0, tzinfo=timezone.utc)
    for index in range(7):
        store.save_item(ItemRecord(
            url=f"https://example.com/s{index}", dedup_key=f"s{index}",
            title=f"同刻条目{index}", first_seen=moment,
        ))
    store.close()
    seen: list[str] = []
    before, before_id, limit = None, None, 3
    pages = 0
    while True:
        params: dict = {"db": str(db), "limit": limit}
        if before is not None:
            params["before"] = before
            params["before_id"] = before_id
        code, responses, _ = rpc({"id": pages + 1, "method": "store.items", "params": params})
        items = responses[0]["result"]["items"]
        seen += [item["dedup_key"] for item in items]
        pages += 1
        if len(items) < limit:
            break
        oldest = items[-1]
        before, before_id = oldest["first_seen"], oldest["id"]
        assert pages <= 10, "游标未推进,疑似死循环"
    assert pages == 3 and len(seen) == 7 and len(set(seen)) == 7  # 取尽且零重复

    # 对照:严格 before 单键把同刻更旧条目整批跳过 —— before_id 的升级理由。
    code, responses, _ = rpc({"id": 90, "method": "store.items",
                              "params": {"db": str(db), "limit": 3, "before": moment.isoformat()}})
    assert responses[0]["result"]["count"] == 0
    # before_id 单传(缺 before)= invalid_params(复合游标成对出现)
    code, responses, _ = rpc({"id": 91, "method": "store.items",
                              "params": {"db": str(db), "before_id": 5}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_store_items_query_like_nocase(tmp_path):
    """C1×G1 query:title/content/source 三列 NOCASE LIKE;% 通配按字面匹配。"""
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord
    db = tmp_path / "query.db"
    store = SQLiteStore(str(db))
    base = datetime(2026, 10, 2, tzinfo=timezone.utc)

    def seed(index: int, title: str, content: str | None, source: str | None) -> None:
        store.save_item(ItemRecord(
            url=f"https://example.com/q{index}", dedup_key=f"q{index}", title=title,
            content=content, source=source,
            first_seen=datetime(2026, 10, 2, index + 1, tzinfo=timezone.utc),
        ))

    seed(0, "RSS 周报第 1 期", None, "hackernews")
    seed(1, "评分纪要", "GLM 精评 4.6 分", "blog")
    seed(2, "增长 100%", None, "blog")
    seed(3, "增长 100x", None, "blog")
    store.close()
    del base

    def titles_of(query: str) -> list[str]:
        code, responses, _ = rpc({"id": 1, "method": "store.items",
                                  "params": {"db": str(db), "query": query}})
        return [item["title"] for item in responses[0]["result"]["items"]]

    assert titles_of("rss") == ["RSS 周报第 1 期"]  # title 命中(NOCASE)
    assert titles_of("glm") == ["评分纪要"]  # content 命中
    assert titles_of("HackerNews") == ["RSS 周报第 1 期"]  # source 命中(大小写不敏感)
    assert titles_of("100%") == ["增长 100%"]  # % 按字面,不吞 100x


def _wait_test_completed(out: io.StringIO, timeout: float = 60.0) -> dict:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        for obj in split_stream(out)[1]:
            if obj.get("type") == "test.completed":
                return obj
        time.sleep(0.05)
    raise AssertionError(f"试抓未在 {timeout}s 内完成")


def test_sources_test_async_job_roundtrip(tmp_path, local_api, monkeypatch):
    """C13 sources.test:围栏内品类 → 提交即返 job_id → test.completed 事件回载
    CLI --json 结果(真跑 127.0.0.1 本地夹具,exit 0)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch,
                              ("demo.yaml", VALID_YAML.replace("{port}", str(local_api))))
    yaml_path = plugins / "demo.yaml"
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 1, "method": "sources.test",
                                    "params": {"file": str(yaml_path), "source": "local-api"}}) + "\n")
    assert entry.serve(stdin=stdin, stdout=out) == 0
    responses, _ = split_stream(out)
    result = responses[0]["result"]
    assert result["state"] == "running" and result["source"] == "local-api"
    assert isinstance(result["job_id"], int) and result["job_id"] >= 1
    event = _wait_test_completed(out)
    assert event["ok"] is True and event["exit_code"] == 0
    assert event["result"]["command"] == "test"
    assert event["result"]["sources"][0]["ok"] is True
    assert entry._TEST_ACTIVE_JOB is None  # 单飞位已释放


def test_sources_test_unknown_source_completes_with_error(tmp_path, local_api, monkeypatch):
    """C13 源不存在:预检放行(品类可载)→ CLI config 错经事件透传(ok=false)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch,
                              ("demo.yaml", VALID_YAML.replace("{port}", str(local_api))))
    yaml_path = plugins / "demo.yaml"
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 1, "method": "sources.test",
                                    "params": {"file": str(yaml_path), "source": "no-such-source"}}) + "\n")
    assert entry.serve(stdin=stdin, stdout=out) == 0
    event = _wait_test_completed(out)
    assert event["ok"] is False
    assert event["error"] == "config"  # CLI config 错透传(source_not_found 细节在 data)
    assert any(err.get("error_type") == "source_not_found"
               for err in event["data"]["errors"])


def test_sources_test_single_flight_and_refusals(tmp_path, monkeypatch):
    """C13 错误矩阵:test_busy 单飞 / file 缺失 invalid_params / 围栏外
    not_yaml_suffix / 装不上品类 source_file_unreadable / timeout>120 拒。"""
    plugins = _editor_plugins(tmp_path, monkeypatch,
                              ("demo.yaml", VALID_YAML.replace("{port}", "1")),
                              ("bad.yaml", BAD_CRON_YAML))
    good = str(plugins / "demo.yaml")
    entry._TEST_ACTIVE_JOB = 88
    code, responses, _ = rpc({"id": 1, "method": "sources.test", "params": {"file": good}})
    error = responses[0]["error"]
    assert error["code"] == "test_busy" and error["data"]["active_job_id"] == 88
    entry._TEST_ACTIVE_JOB = None
    code, responses, _ = rpc({"id": 2, "method": "sources.test", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"
    code, responses, _ = rpc({"id": 3, "method": "sources.test", "params": {"file": "/etc/hosts"}})
    assert responses[0]["error"]["code"] == "not_yaml_suffix"
    code, responses, _ = rpc({"id": 4, "method": "sources.test",
                              "params": {"file": str(plugins / "bad.yaml")}})
    assert responses[0]["error"]["code"] == "source_file_unreadable"
    code, responses, _ = rpc({"id": 5, "method": "sources.test",
                              "params": {"file": str(plugins / "bad.yaml"), "timeout": 121}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_method_registry_allowed_matches_handlers():
    """对账(spec 变更纪律第 2 条):data.allowed 与 _HANDLERS 键集一致;
    v1.1.2 桌面对齐批(run.cancel/runs.list/secret.delete/sources.test)+
    feed-ux 批(feed.export/push.test/schedule.preview)+
    weixin-bridge 批(bridge.status)+
    vision-v2 批(image.models.*×4 + image.server.*×2 + image.files.purge)+
    v1.1.2 批第二切片(feedback.mark/list/stats + store.trend)+
    fe-small-batch 批(feed.enrich)+ alert-rules 批(alerts.* 四方法,
    10-04-alert-rules)+ desktop-b234 批(runs.trend,10-04-desktop-b234)+
    hermes-cron 批(cron.* 九方法,10-04-hermes-cron B3)+
    read-state-server 批(store.state.* 三方法,10-04-read-state-server)+
    plugin-market-b2 批(gates.get/gates.save 两方法,10-05-plugin-market-batch
    批二第 10 步 D4/D7;设置面分区 UI = 同批第 11 步)
    后 = 62。"""
    code, responses, _ = rpc({"id": 1, "method": "no.such.method", "params": {}})
    allowed = responses[0]["error"]["data"]["allowed"]
    assert allowed == sorted(entry._HANDLERS)
    assert len(allowed) == 62
    for method in ("run.cancel", "runs.list", "runs.trend", "secret.delete",
                   "sources.test", "feed.export", "push.test", "schedule.preview",
                   "bridge.status", "image.models.list", "image.models.download",
                   "image.models.delete", "image.models.activate",
                   "image.server.status", "image.server.ensure",
                   "image.files.purge", "feed.enrich",
                   "alerts.list", "alerts.save", "alerts.delete", "alerts.test",
                   "cron.list", "cron.create", "cron.edit", "cron.pause",
                   "cron.resume", "cron.run", "cron.remove", "cron.status",
                   "cron.runs", "store.state.mark", "store.state.mark_all",
                   "store.state.import", "gates.get", "gates.save"):
        assert method in allowed


def test_protocol_version_bumped_for_feed_ux():
    """feed-ux 批新增三方法 → PROTOCOL_VERSION 3;weixin-bridge 批
    (bridge.status,10-03-messaging-weixin-bridge)→ v4;vision-v2 批
    (image.models.*/image.server.* + store.items 三新投影键)→ v5;
    fe-small-batch 批(feed.enrich,10-03-fe-small-batch G8)→ v6;
    alert-rules 批(alerts.* 四方法 + alerts.fired 事件,10-04-alert-rules)→ v7;
    desktop-b234 批(runs.trend,10-04-desktop-b234)→ v8;
    hermes-cron 批(cron.* 九方法 + cron.skipped/cron.completed 两事件 +
    serve 内置 cron ticker,10-04-hermes-cron B3)→ v9;
    read-state-server 批(store.state.* 三方法 + store.items 投影补
    read/starred/later 三键,10-04-read-state-server)→ v10(开工实读 v9 后
    +1:hermes-cron 已先合入,竞速顺延);
    plugin-market-batch 批二(gates.get/gates.save 两方法,
    10-05-plugin-market-batch 第 11 步)**未随批 bump**——地基路定案维持
    v10(两方法在 v10 内交付,注册表 62 行;gates UI 无 protocol 版本能力门,
    旧壳+新 UI 组合经 method_not_found 结构化降级不白屏)。若后续补 bump,
    本断言随迁。"""
    code, responses, _ = rpc({"id": 1, "method": "version", "params": {}})
    assert responses[0]["result"]["protocol"] == 10


# ---------------------------------------------------------------------------
# read-state-server 批(10-04-read-state-server,协议件):store.state.* 三方法
# + store.items/feed.export 投影补 read/starred/later 三键(G9)
# ---------------------------------------------------------------------------

#: v7 期 items 表形状(无 read/starred/later 三列;直造旧表而非从 v8 降级——
#: SQLite DROP COLUMN 会因建表 DDL 中的行注释重建出非法语句,真实旧库本就是
#: 这种带列旧形状,直造更忠实;store 层 tests/test_read_state.py 同款)。
_V7_ITEMS_DDL = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    dedup_key TEXT NOT NULL,
    source TEXT,
    title TEXT NOT NULL,
    content TEXT,
    content_hash TEXT,
    tags TEXT,
    category TEXT,
    scores TEXT,
    pushed_at TEXT,
    push_slot TEXT,
    first_seen TEXT NOT NULL,
    raw TEXT
);
"""


def _make_v7_database(path, rows: list[tuple[str, str, str]]) -> None:
    """手造 v7 库:旧形状 items 表 + 版本戳 7(模拟升级前的库文件)。"""
    import sqlite3

    raw = sqlite3.connect(path)
    raw.executescript(
        _V7_ITEMS_DDL
        + "CREATE TABLE IF NOT EXISTS store_meta"
        + " (key TEXT PRIMARY KEY, value TEXT NOT NULL);"
    )
    raw.execute("INSERT INTO store_meta (key, value) VALUES ('schema_version', '7')")
    raw.executemany(
        "INSERT INTO items (url, dedup_key, title, first_seen)"
        " VALUES (?, ?, ?, '2026-10-01T00:00:00+00:00')",
        rows,
    )
    raw.commit()
    raw.close()


def test_store_state_v7_database_migrates_on_protocol_open(tmp_path):
    """AC1 迁移:v7 旧库被任一协议方法打开即迁 v8——行保留、三列 +
    idx_items_dedup_key 在位、schema_version=8、存量行读态不猜测(全 False)。
    fresh 库直建 v8 两路径同形由 store 层 tests/test_read_state.py 盖;
    此处验协议面触发(handler 每请求独立 SQLiteStore 开库)。"""
    import sqlite3

    db = tmp_path / "legacy-v7.db"
    _make_v7_database(db, [
        ("https://old/1", "https://old/1", "旧条目一"),
        ("https://old/2", "https://old/2", "旧条目二"),
    ])

    code, responses, _ = rpc({"id": 1, "method": "store.items", "params": {"db": str(db)}})
    result = responses[0]["result"]
    assert result["count"] == 2  # 行保留
    by_key = {item["dedup_key"]: item for item in result["items"]}
    assert (by_key["https://old/1"]["read"],
            by_key["https://old/1"]["starred"],
            by_key["https://old/1"]["later"]) == (False, False, False)  # 迁移不猜读态

    raw = sqlite3.connect(db)
    version = raw.execute(
        "SELECT value FROM store_meta WHERE key = 'schema_version'"
    ).fetchone()[0]
    columns = {row[1] for row in raw.execute("PRAGMA table_info(items)").fetchall()}
    indexes = {row[1] for row in raw.execute("PRAGMA index_list(items)").fetchall()}
    raw.close()
    assert version == "8"
    assert {"read", "starred", "later"} <= columns
    assert "idx_items_dedup_key" in indexes


def test_store_state_mark_roundtrip_and_projection(tmp_path):
    """§6.1-3:mark 单键置位 → store.items 应答 read=true(投影联通);
    未列出键不动;rowcount 口径 = 匹配行数如实回传。"""
    db = tmp_path / "mark.db"
    _seed_items_for_export(db, [("条目甲", "news", "a"), ("条目乙", "news", "b")])

    code, responses, _ = rpc({"id": 1, "method": "store.state.mark", "params": {
        "db": str(db), "keys": ["e0"], "marker": "read", "value": True}})
    assert responses[0]["result"] == {"updated": 1}

    code, responses, _ = rpc({"id": 2, "method": "store.items", "params": {"db": str(db)}})
    by_key = {item["dedup_key"]: item for item in responses[0]["result"]["items"]}
    assert (by_key["e0"]["read"], by_key["e0"]["starred"], by_key["e0"]["later"]) == (True, False, False)
    assert by_key["e1"]["read"] is False  # 未列出键不动

    # 幂等重放:显式置同值,rowcount 仍如实计匹配行(不二次核算)
    code, responses, _ = rpc({"id": 3, "method": "store.state.mark", "params": {
        "db": str(db), "keys": ["e0"], "marker": "read", "value": True}})
    assert responses[0]["result"] == {"updated": 1}
    # 未知键:匹配 0 行,如实回传 0
    code, responses, _ = rpc({"id": 4, "method": "store.state.mark", "params": {
        "db": str(db), "keys": ["no-such-key"], "marker": "later", "value": True}})
    assert responses[0]["result"] == {"updated": 0}


def test_store_state_mark_same_dedup_key_multi_row_all_marked(tmp_path):
    """§6.1-4 / AC2 红线:dated-key 旋转下同键多行(dedup_registry 滚键)
    同置——与 localStorage itemKey 语义一致。"""
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord

    db = tmp_path / "dated.db"
    store = SQLiteStore(str(db))
    base = datetime(2026, 10, 3, tzinfo=timezone.utc)
    store.save_item(ItemRecord(url="https://d/old", dedup_key="dated:2026-10-01",
                               title="旧轮", first_seen=base))
    store.save_item(ItemRecord(url="https://d/new", dedup_key="dated:2026-10-01",
                               title="新轮", first_seen=base.replace(hour=2)))
    store.close()

    code, responses, _ = rpc({"id": 1, "method": "store.state.mark", "params": {
        "db": str(db), "keys": ["dated:2026-10-01"], "marker": "read", "value": True}})
    assert responses[0]["result"] == {"updated": 2}  # 同键两行同置

    code, responses, _ = rpc({"id": 2, "method": "store.items", "params": {"db": str(db)}})
    items = responses[0]["result"]["items"]
    assert len(items) == 2 and all(item["read"] for item in items)


def test_store_state_mark_invalid_params_matrix(tmp_path):
    """§6.1-5:非法 marker / 非 bool value / 空 keys / 含空串 / 超 2000 上限
    → invalid_params;恰 2000 边界放行(上限是误用防线不是容量声明)。"""
    db = tmp_path / "matrix.db"
    SQLiteStore(str(db)).close()
    cases = [
        ({"keys": ["k"], "marker": "deleted", "value": True}, "params.marker"),
        ({"keys": ["k"], "marker": "read", "value": "yes"}, "params.value"),
        ({"keys": [], "marker": "read", "value": True}, "params.keys"),
        ({"keys": ["ok", ""], "marker": "read", "value": True}, "params.keys"),
        ({"keys": ["ok", 5], "marker": "read", "value": True}, "params.keys"),
        ({"keys": [f"k{i}" for i in range(2001)], "marker": "read", "value": True},
         "params.keys"),
    ]
    for index, (extra, path) in enumerate(cases):
        code, responses, _ = rpc({"id": index, "method": "store.state.mark",
                                  "params": {"db": str(db), **extra}})
        error = responses[0]["error"]
        assert error["code"] == "invalid_params" and error["path"] == path, extra

    code, responses, _ = rpc({"id": 90, "method": "store.state.mark", "params": {
        "db": str(db), "keys": [f"k{i}" for i in range(2000)],
        "marker": "read", "value": True}})
    assert responses[0]["result"] == {"updated": 0}  # 边界放行:空库匹配 0 行


def test_store_state_mark_all_whole_library_and_category(tmp_path):
    """§6.1-6:mark_all 全库置位(计数=全库行数,含未翻页语义)+ category
    精确等值过滤(只置该类;无 query 参数——Q3.2 钉死)。"""
    db = tmp_path / "markall.db"
    _seed_items_for_export(db, [
        ("甲", "news", "a"), ("乙", "news", "b"), ("丙", "stocks", "api"),
    ])

    code, responses, _ = rpc({"id": 1, "method": "store.state.mark_all", "params": {
        "db": str(db), "marker": "read", "value": True}})
    assert responses[0]["result"] == {"updated": 3}  # 全库 = 3 行全置

    code, responses, _ = rpc({"id": 2, "method": "store.state.mark_all", "params": {
        "db": str(db), "marker": "starred", "value": True, "category": "news"}})
    assert responses[0]["result"] == {"updated": 2}  # 只置 news 类

    code, responses, _ = rpc({"id": 3, "method": "store.items", "params": {"db": str(db)}})
    by_category = {item["category"]: item for item in responses[0]["result"]["items"]}
    assert by_category["news"]["read"] is True and by_category["news"]["starred"] is True
    assert by_category["stocks"]["read"] is True and by_category["stocks"]["starred"] is False

    code, responses, _ = rpc({"id": 4, "method": "store.state.mark_all", "params": {
        "db": str(db), "marker": "read", "value": False, "category": ""}})
    assert responses[0]["error"]["code"] == "invalid_params"  # category 空串拒绝
    # 无 query 参数是契约钉死(Q3.2):方法签名不含它,handler 对多余键
    # 不主动拒(与全协议风格一致,未知键静默忽略),不另设拒绝用例。


def test_store_state_import_three_key_forms(tmp_path):
    """§6.1-7 / AC4:import 三形态——dedup_key 直配置上 / id:<n> 映射置上 /
    id:<url> 计 skipped;快照只覆盖出现的标记键。"""
    db = tmp_path / "import.db"
    _seed_items_for_export(db, [("甲", "news", "a"), ("乙", "stocks", "b")])
    store = SQLiteStore(str(db))
    numeric_id = store.list_items()[0].id  # 取一行真实 id(id:<n> 引用)
    store.close()

    states = {
        "e0": {"read": True},                      # dedup_key 直配
        f"id:{numeric_id}": {"starred": True},     # id:<n> → 解析到 dedup_key
        "id:https://example.com/missed": {"read": True},  # id:<url> 无从解析
    }
    code, responses, _ = rpc({"id": 1, "method": "store.state.import", "params": {
        "db": str(db), "states": states}})
    assert responses[0]["result"] == {"imported": 2, "skipped": 1}

    code, responses, _ = rpc({"id": 2, "method": "store.items", "params": {"db": str(db)}})
    by_key = {item["dedup_key"]: item for item in responses[0]["result"]["items"]}
    assert by_key["e0"]["read"] is True and by_key["e0"]["starred"] is False  # 只覆盖出现键
    starred_keys = [key for key, item in by_key.items() if item["starred"]]
    assert len(starred_keys) == 1  # id:<n> 解析目标已置(恰一行)


def test_store_state_import_second_call_is_noop_with_server_flag(tmp_path):
    """§6.1-8:import 二次调用 no-op(imported=0,不触库);幂等旗标 =
    store_meta feed_state_imported_at(服务端是唯一真相,Q2.2)可直查。"""
    db = tmp_path / "flag.db"
    _seed_items_for_export(db, [("甲", "news", "a")])

    code, responses, _ = rpc({"id": 1, "method": "store.state.import", "params": {
        "db": str(db), "states": {"e0": {"read": True}}}})
    assert responses[0]["result"] == {"imported": 1, "skipped": 0}

    # 旗标已落在 store_meta(与库同寿命,webview 清数据击不穿)
    store = SQLiteStore(str(db))
    try:
        assert store.get_meta("feed_state_imported_at") is not None
    finally:
        store.close()

    # 二次调用:即使载荷不同也 no-op 应答,值不再被覆盖(重放不可能)
    code, responses, _ = rpc({"id": 2, "method": "store.state.import", "params": {
        "db": str(db), "states": {"e0": {"starred": True}}}})
    assert responses[0]["result"] == {"imported": 0, "skipped": 0}
    code, responses, _ = rpc({"id": 3, "method": "store.items", "params": {"db": str(db)}})
    item = responses[0]["result"]["items"][0]
    assert item["read"] is True and item["starred"] is False  # 第二发未触库


def test_store_items_and_feed_export_carry_state_keys_csv_unchanged(tmp_path):
    """§6.1-9 / AC5:feed.export JSONL 多三键(共用 _item_dict 投影,加法变化);
    CSV 固定列集不变。"""
    db = tmp_path / "export-state.db"
    _seed_items_for_export(db, [("甲", "news", "a"), ("乙", "news", "b")])
    code, responses, _ = rpc({"id": 1, "method": "store.state.mark", "params": {
        "db": str(db), "keys": ["e0"], "marker": "read", "value": True}})
    assert responses[0]["result"] == {"updated": 1}

    jsonl_path = tmp_path / "state.jsonl"
    code, responses, _ = rpc({"id": 2, "method": "feed.export", "params": {
        "format": "jsonl", "path": str(jsonl_path), "db": str(db)}})
    assert responses[0]["result"]["count"] == 2
    rows = {obj["dedup_key"]: obj for obj in (
        json.loads(line) for line in jsonl_path.read_text(encoding="utf-8").splitlines()
    )}
    assert rows["e0"]["read"] is True and rows["e0"]["starred"] is False and rows["e0"]["later"] is False
    assert rows["e1"]["read"] is False  # JSONL 三键随行

    csv_path = tmp_path / "state.csv"
    code, responses, _ = rpc({"id": 3, "method": "feed.export", "params": {
        "format": "csv", "path": str(csv_path), "db": str(db)}})
    assert csv_path.read_text(encoding="utf-8").splitlines()[0] == (
        "id,first_seen,category,source,title,url,content")  # CSV 列集不变


# ---------------------------------------------------------------------------
# hermes-cron 批(10-04-hermes-cron B3):cron.* 九方法 + serve 内置 ticker
# ---------------------------------------------------------------------------


def _write_cron_category(tmp_path: Path, name: str = "news.yaml") -> str:
    """能过 load_category_file 的品类 YAML(Q6 早失败门的正样本)。"""
    return write_yaml(tmp_path, VALID_YAML.replace("{port}", "1"), name)


def test_cron_family_roundtrip(tmp_path):
    """cron.* 九方法行为(AC7 与 CLI 同一 API 层):create(Q5 绝对路径/
    origin=desktop)→ list → edit(schedule 变更重算)→ pause(reason)→
    resume → run(trigger 复活+manual_run_at)→ status → runs(run_summary
    解析)→ estop all → remove。"""
    db = str(tmp_path / "cron.db")
    category = _write_cron_category(tmp_path)

    code, responses, _ = rpc({"id": 1, "method": "cron.create", "params": {
        "schedule": "every 45m", "category": category, "name": "早晚情报流",
        "deliver": "local", "db": db}})
    assert code == 0
    job = responses[0]["result"]["job"]
    assert job["name"] == "早晚情报流"
    assert job["schedule"]["kind"] == "interval"
    assert job["next_run_at"]  # scheduled:立即有下次射点
    assert job["origin"] == {"source": "desktop"}
    assert job["category"] == str(Path(category))  # Q5:绝对路径存储

    code, responses, _ = rpc({"id": 2, "method": "cron.list", "params": {"db": db}})
    listed = responses[0]["result"]
    assert listed["count"] == 1 and listed["jobs"][0]["id"] == job["id"]
    assert listed["data_root"] == str(tmp_path)  # 数据根 = db 父目录

    code, responses, _ = rpc({"id": 3, "method": "cron.edit", "params": {
        "job": job["id"], "schedule": "every 2h", "name": "改名", "db": db}})
    updated = responses[0]["result"]["job"]
    assert updated["name"] == "改名"
    assert updated["schedule"]["minutes"] == 120  # schedule 变更重算生效

    code, responses, _ = rpc({"id": 4, "method": "cron.pause", "params": {
        "job": "改名", "reason": "主人暂停", "db": db}})
    paused = responses[0]["result"]["job"]
    assert paused["state"] == "paused"
    assert paused["paused_reason"] == "主人暂停"

    code, responses, _ = rpc({"id": 5, "method": "cron.resume", "params": {
        "job": job["id"], "db": db}})
    resumed = responses[0]["result"]["job"]
    assert resumed["state"] == "scheduled"
    assert resumed["paused_reason"] is None

    code, responses, _ = rpc({"id": 6, "method": "cron.run", "params": {
        "job": job["id"], "db": db}})
    triggered = responses[0]["result"]["job"]
    assert triggered["manual_run_at"] == triggered["next_run_at"]  # 下次 tick 立即跑

    code, responses, _ = rpc({"id": 7, "method": "cron.status", "params": {"db": db}})
    status = responses[0]["result"]
    assert status["jobs_total"] == 1 and status["jobs_enabled"] == 1
    assert status["ticker_alive"] is False  # 本测试无 ticker,心跳从未落盘
    assert status["next_due_at"] == triggered["next_run_at"]
    assert status["estopped"] is False

    # runs:空账本 → 注入一行带摘要(run_summary_json)→ 随行解析
    code, responses, _ = rpc({"id": 8, "method": "cron.runs", "params": {"db": db}})
    assert responses[0]["result"]["count"] == 0
    from myssia.cron.jobs import CronJobs

    cron = CronJobs.for_db(db)
    row = cron.ledger.create_execution(job["id"], source="manual")
    cron.ledger.finish_execution(
        row["id"], success=True, error=None,
        run_summary={"job": {"id": job["id"]}, "run": {"status": "ok"}},
    )
    code, responses, _ = rpc({"id": 9, "method": "cron.runs", "params": {
        "job": job["id"], "db": db}})
    result = responses[0]["result"]
    assert result["count"] == 1
    record = result["executions"][0]
    assert record["status"] == "completed"
    assert record["run_summary"]["run"]["status"] == "ok"
    assert "run_summary_json" not in record  # 原始串已被解析替换

    # estop(Q4):pause all → status 可见 → resume all 解除
    code, responses, _ = rpc({"id": 10, "method": "cron.pause", "params": {
        "all": True, "db": db}})
    assert responses[0]["result"]["estopped"] is True
    code, responses, _ = rpc({"id": 11, "method": "cron.status", "params": {"db": db}})
    assert responses[0]["result"]["estopped"] is True
    code, responses, _ = rpc({"id": 12, "method": "cron.resume", "params": {
        "all": True, "db": db}})
    cleared = responses[0]["result"]
    assert cleared["cleared"] is True and cleared["estopped"] is False

    code, responses, _ = rpc({"id": 13, "method": "cron.remove", "params": {
        "job": job["id"], "db": db}})
    assert responses[0]["result"] == {
        "removed": True, "job_id": job["id"], "name": "改名"}
    code, responses, _ = rpc({"id": 14, "method": "cron.list", "params": {
        "db": db, "all": True}})
    assert responses[0]["result"]["count"] == 0


def test_cron_family_error_matrix(tmp_path):
    """cron.* 错误码(与 CLI 同门):schedule 解析失败 / 品类装不上(Q6)/
    参数形状 / 空更新集 / 未知 job / 重名引用 / all 与 job 互斥。"""
    db = str(tmp_path / "cron.db")
    category = _write_cron_category(tmp_path)
    broken = write_yaml(tmp_path, "id: broken\n", "broken.yaml")

    code, responses, _ = rpc({"id": 1, "method": "cron.create", "params": {
        "schedule": "not-a-cron", "category": category, "db": db}})
    assert responses[0]["error"]["code"] == "cron_create_failed"
    code, responses, _ = rpc({"id": 2, "method": "cron.create", "params": {
        "schedule": "every 45m", "category": broken, "db": db}})
    error = responses[0]["error"]
    assert error["code"] == "cron_category_invalid"
    assert error["path"] == "params.category"
    assert error["data"]["errors"]  # LoadError.to_dict 结构化细节
    code, responses, _ = rpc({"id": 3, "method": "cron.create", "params": {
        "category": category, "db": db}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.schedule"
    code, responses, _ = rpc({"id": 4, "method": "cron.create", "params": {
        "schedule": "every 45m", "category": category, "repeat": "3", "db": db}})
    assert responses[0]["error"]["code"] == "invalid_params"

    code, responses, _ = rpc({"id": 5, "method": "cron.create", "params": {
        "schedule": "every 45m", "category": category, "name": "重名", "db": db}})
    first = responses[0]["result"]["job"]
    code, responses, _ = rpc({"id": 6, "method": "cron.create", "params": {
        "schedule": "every 46m", "category": category, "name": "重名", "db": db}})
    second = responses[0]["result"]["job"]
    assert first["id"] != second["id"]

    code, responses, _ = rpc({"id": 7, "method": "cron.pause", "params": {
        "job": "重名", "db": db}})
    error = responses[0]["error"]
    assert error["code"] == "cron_ambiguous_job"
    assert sorted(error["data"]["candidates"]) == sorted([first["id"], second["id"]])
    code, responses, _ = rpc({"id": 8, "method": "cron.run", "params": {
        "job": "查无此 job", "db": db}})
    assert responses[0]["error"]["code"] == "cron_job_not_found"
    code, responses, _ = rpc({"id": 9, "method": "cron.edit", "params": {
        "job": first["id"], "db": db}})
    assert responses[0]["error"]["code"] == "cron_edit_no_changes"
    code, responses, _ = rpc({"id": 10, "method": "cron.pause", "params": {
        "all": True, "job": first["id"], "db": db}})
    assert responses[0]["error"]["code"] == "invalid_params"
    code, responses, _ = rpc({"id": 11, "method": "cron.list", "params": {
        "db": db, "all": "yes"}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_cron_dispatch_gate_skips_when_run_busy(monkeypatch):
    """Q2 冲突路径:cron fire 撞桌面 run 单飞锁 = 跳过本 fire + ``cron.skipped``
    事件(reason=run_busy、active_run_id 透传);空闲时放行且零事件。"""
    out = io.StringIO()
    monkeypatch.setattr(entry, "_OUT", out)
    entry._ACTIVE_RUN_ID = 7
    try:
        assert entry._cron_dispatch_gate({"id": "j1", "name": "早晚情报流"}) is False
    finally:
        entry._ACTIVE_RUN_ID = None
    assert entry._cron_dispatch_gate({"id": "j1", "name": "早晚情报流"}) is True
    lines = [json.loads(line) for line in out.getvalue().splitlines()]
    assert len(lines) == 1  # 空闲放行不发事件
    event = lines[0]
    assert event["type"] == "cron.skipped"
    assert event["job_id"] == "j1" and event["name"] == "早晚情报流"
    assert event["reason"] == "run_busy" and event["active_run_id"] == 7
    assert event["ts"]


def test_cron_execute_job_emits_completed_event(monkeypatch):
    """``cron.completed`` 事件:执行体跑完即发;摘要取账本 ``run_summary_json``
    (D10 零二次解析),status 从摘要 run 块取;账本无行时 summary=null 如实。"""
    from types import SimpleNamespace

    out = io.StringIO()
    monkeypatch.setattr(entry, "_OUT", out)

    class _StubRunner:
        def __init__(self, cron):
            self.cron = cron

        def execute(self, job):
            return True, None, "feishu:群 投递失败"

    monkeypatch.setattr(entry, "CronRunner", _StubRunner)
    summary = {"job": {"id": "j1"}, "run": {"status": "partial"}}
    fake_cron = SimpleNamespace(
        ledger=SimpleNamespace(
            get_execution=lambda execution_id: {"run_summary_json": json.dumps(summary)},
        )
    )
    ok, error, delivery_error = entry._cron_execute_job(
        fake_cron, {"id": "j1", "name": "早晚情报流", "execution_id": "e1"}
    )
    assert (ok, error, delivery_error) == (True, None, "feishu:群 投递失败")
    event = json.loads(out.getvalue().splitlines()[0])
    assert event["type"] == "cron.completed"
    assert event["job_id"] == "j1" and event["ok"] is True
    assert event["status"] == "partial"  # 摘要 run 块优先于成功布尔
    assert event["delivery_error"] == "feishu:群 投递失败"
    assert event["summary"] == summary
    assert event["ts"]

    # 账本无行(写失败兜底):事件照发,summary=null 如实、status 回落布尔
    out.truncate(0)
    out.seek(0)
    fake_cron.ledger.get_execution = lambda execution_id: None
    ok, error, delivery_error = entry._cron_execute_job(
        fake_cron, {"id": "j2", "name": "无账本", "execution_id": "e2"}
    )
    event = json.loads(out.getvalue().splitlines()[0])
    assert event["type"] == "cron.completed"
    assert event["summary"] is None and event["status"] == "ok"


def test_cron_ticker_lifecycle_home_mode(tmp_path, monkeypatch):
    """ticker 起停干净(home 模式):supervisor + SupervisedTickerThread 双
    daemon 起、心跳真落盘(启动即首个心跳)、stop 后线程退出 + 句柄复位。"""
    from myssia.cron.jobs import CronJobs

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    monkeypatch.setattr(entry, "CRON_TICK_INTERVAL_SECONDS", 0.05)
    entry._start_cron_ticker()
    supervisor, ticker = entry._CRON_SUPERVISOR, entry._CRON_TICKER
    assert supervisor is not None and supervisor.is_alive()
    assert ticker is not None and ticker.is_alive()
    assert entry._CRON_STOP is not None

    cron = CronJobs.for_db(tmp_path / "myssia.db")
    deadline = time.time() + 5.0
    while time.time() < deadline and cron.get_ticker_heartbeat_age() is None:
        time.sleep(0.02)
    assert cron.get_ticker_heartbeat_age() is not None  # ticker 真跑过

    entry._stop_cron_ticker(join_timeout=2.0)
    assert entry._CRON_SUPERVISOR is None and entry._CRON_TICKER is None
    assert entry._CRON_STOP is None
    supervisor.join(2.0)
    ticker.join(2.0)
    assert not supervisor.is_alive() and not ticker.is_alive()

    # 幂等:重复 stop 与重复 start(已停后重起)都干净
    entry._stop_cron_ticker()
    entry._start_cron_ticker()
    assert entry._CRON_SUPERVISOR is not None and entry._CRON_SUPERVISOR.is_alive()
    entry._start_cron_ticker()  # 已在跑:幂等 no-op,不叠线程
    entry._stop_cron_ticker(join_timeout=2.0)
    assert entry._CRON_SUPERVISOR is None


def test_cron_ticker_dev_mode_not_started():
    """dev 回退(home=None)不起 ticker:数据根落 cwd,起真 ticker 会污染
    仓库目录;dev 常宿形态 = ``myssia cron serve``(design §4.2 注记)。"""
    entry._start_cron_ticker()
    assert entry._CRON_SUPERVISOR is None
    assert entry._CRON_TICKER is None
    assert entry._CRON_STOP is None


def test_serve_starts_and_stops_cron_ticker(tmp_path, monkeypatch):
    """serve() 接线:home 模式请求处理期 ticker 在跑(不占 serve 线程,
    B10);serve EOF 关停 + 句柄复位(lifetime = serve)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    monkeypatch.setattr(entry, "CRON_TICK_INTERVAL_SECONDS", 0.05)
    seen: dict[str, Any] = {}
    original = entry._handle_line

    def spy(line: str) -> None:
        # 捕获"请求处理那一刻"的活性(serve EOF 会关停,事后验对象必是死的)
        seen["supervisor_alive"] = (
            entry._CRON_SUPERVISOR is not None and entry._CRON_SUPERVISOR.is_alive()
        )
        seen["ticker_alive"] = (
            entry._CRON_TICKER is not None and entry._CRON_TICKER.is_alive()
        )
        original(line)

    monkeypatch.setattr(entry, "_handle_line", spy)
    code, responses, _ = rpc({"id": 1, "method": "version", "params": {}})
    assert code == 0
    # v9 = hermes-cron 批;v10 = read-state-server 批(版本实读 +1 顺延)
    assert responses[0]["result"]["protocol"] == 10
    assert seen["supervisor_alive"] and seen["ticker_alive"]
    # EOF:serve 返回前已关停(idle ticker 即醒即退,interval 已注入 0.05s)
    assert entry._CRON_SUPERVISOR is None and entry._CRON_TICKER is None


# ---------------------------------------------------------------------------
# feed-ux 批(10-03-feed-ux):feed.export / schedule.preview / push.test
# ---------------------------------------------------------------------------


def _seed_items_for_export(db, titles):
    """三个标题 + 类目/来源各异的可查询条目(新→旧入库)。"""
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord
    store = SQLiteStore(str(db))
    base = datetime(2026, 10, 3, tzinfo=timezone.utc)
    for index, (title, category, source) in enumerate(titles):
        store.save_item(ItemRecord(
            url=f"https://example.com/e{index}", dedup_key=f"e{index}", title=title,
            content=f"{title} 正文", source=source, category=category,
            first_seen=base.replace(hour=index + 1),
        ))
    store.close()


def test_feed_export_jsonl_csv_roundtrip(tmp_path):
    """G3 feed.export:JSONL/CSV 双格式落盘可查,query/category 过滤生效,
    应答带 path/count/bytes。"""
    db = tmp_path / "export.db"
    _seed_items_for_export(db, [
        ("RSS 甲", "news", "blog"),
        ("RSS 乙", "news", "hackernews"),
        ("股票丙", "stocks", "api"),
    ])
    jsonl_path = tmp_path / "feed.jsonl"
    code, responses, _ = rpc(
        {"id": 1, "method": "feed.export",
         "params": {"format": "jsonl", "path": str(jsonl_path), "db": str(db)}},
    )
    result = responses[0]["result"]
    assert result["path"] == str(jsonl_path) and result["count"] == 3
    assert result["bytes"] == jsonl_path.stat().st_size
    lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    first = json.loads(lines[0])  # 新→旧:股票丙最新
    assert first["title"] == "股票丙" and first["source"] == "api"

    csv_path = tmp_path / "feed.csv"
    code, responses, _ = rpc(
        {"id": 2, "method": "feed.export",
         "params": {"format": "csv", "path": str(csv_path), "db": str(db),
                    "category": "news", "query": "rss"}},
    )
    result = responses[0]["result"]
    assert result["count"] == 2  # category × query 组合过滤
    rows = csv_path.read_text(encoding="utf-8").splitlines()
    assert rows[0] == "id,first_seen,category,source,title,url,content"  # 表头
    assert len(rows) == 3  # 表头 + 2 条(新→旧:乙小时=2 晚于甲=1)
    assert "RSS 乙" in rows[1] and "RSS 甲" in rows[2]


def test_feed_export_path_refusals(tmp_path):
    """G3 err 矩阵:format 外值 / path 空 / 相对路径 / 父目录不存在。"""
    db = tmp_path / "export.db"
    SQLiteStore(str(db)).close()
    cases = [
        ({"format": "xml", "path": str(tmp_path / "f.xml")}, "invalid_params"),
        ({"format": "jsonl", "path": ""}, "export_path_invalid"),
        ({"format": "jsonl", "path": "relative.jsonl"}, "export_path_invalid"),
        ({"format": "jsonl", "path": str(tmp_path / "no-such-dir" / "f.jsonl")}, "export_path_invalid"),
    ]
    for index, (extra, expected) in enumerate(cases):
        code, responses, _ = rpc({"id": index, "method": "feed.export",
                                  "params": {"db": str(db), **extra}})
        assert responses[0]["error"]["code"] == expected, extra


def test_schedule_preview_next_runs_and_clamp(tmp_path, monkeypatch):
    """G4 schedule.preview:Next runs 数量 = count(钳制 ≤20)、严格递增、
    时刻可解析;schedule/timezone 原文回显。"""
    from datetime import datetime

    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", VALID_YAML))
    code, responses, _ = rpc({"id": 1, "method": "schedule.preview",
                              "params": {"file": str(plugins / "demo.yaml"), "count": 3}})
    result = responses[0]["result"]
    assert result["schedule"] == "0 9 * * *" and result["timezone"] is None
    assert len(result["runs"]) == 3
    times = [datetime.fromisoformat(value) for value in result["runs"]]
    assert times == sorted(times) and len(set(times)) == 3  # 严格递增无重复
    # 钳制:count=99 → 20;count=0 → invalid_params
    code, responses, _ = rpc({"id": 2, "method": "schedule.preview",
                              "params": {"file": str(plugins / "demo.yaml"), "count": 99}})
    assert len(responses[0]["result"]["runs"]) == 20
    code, responses, _ = rpc({"id": 3, "method": "schedule.preview",
                              "params": {"file": str(plugins / "demo.yaml"), "count": 0}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_schedule_preview_refusals(tmp_path, monkeypatch):
    """G4 err 矩阵:file 缺失 / 围栏外 / 装不上品类(source_file_unreadable)。"""
    plugins = _editor_plugins(tmp_path, monkeypatch,
                              ("demo.yaml", VALID_YAML), ("bad.yaml", BAD_CRON_YAML))
    code, responses, _ = rpc({"id": 1, "method": "schedule.preview", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"
    code, responses, _ = rpc({"id": 2, "method": "schedule.preview",
                              "params": {"file": "/etc/hosts"}})
    assert responses[0]["error"]["code"] == "not_yaml_suffix"
    code, responses, _ = rpc({"id": 3, "method": "schedule.preview",
                              "params": {"file": str(plugins / "bad.yaml")}})
    assert responses[0]["error"]["code"] == "source_file_unreadable"


def test_push_test_stdout_preview_and_refusals():
    """G5 push.test:stdout 通道真跑(卡片入应答 preview,协议流零污染);
    channel 未知名拒;凭据缺失走通道结构化错误原文(feishu 默认 env 链)。"""
    code, responses, events = rpc({"id": 1, "method": "push.test",
                                   "params": {"channel": "stdout"}})
    result = responses[0]["result"]
    assert result["ok"] is True and result["channel"] == "stdout"
    assert "MYIA 推送测试" in result["preview"]
    assert events == []  # stdout 卡片绝不落协议流

    code, responses, _ = rpc({"id": 2, "method": "push.test", "params": {"channel": "nope"}})
    assert responses[0]["error"]["code"] == "invalid_params"

    # 凭据缺失 = 通道既有错误分类直传(feishu 未配 target → 默认 env 引用链
    # 先在 bot token 处断:env_var_missing)
    code, responses, _ = rpc({"id": 3, "method": "push.test", "params": {"channel": "feishu_card"}})
    assert responses[0]["error"]["code"] == "env_var_missing"


def test_push_test_sends_via_channel_with_target(monkeypatch):
    """G5 push.test:target 引用下传通道构造;send 收到合成条目(标题带
    「MYIA 推送测试」)与 immediate 上下文 —— monkeypatch 假 send,不真发。"""
    sent: dict = {}

    class FakeChannel:
        def __init__(self, *, target=None, template=None, **kwargs):
            sent["target"] = target
            sent["template"] = template
            sent["extra"] = kwargs

        async def send(self, items, context):
            sent["items"] = list(items)
            sent["context"] = context

    monkeypatch.setitem(entry.myssia_push.CHANNELS, "feishu_card", FakeChannel)
    code, responses, _ = rpc(
        {"id": 1, "method": "push.test",
         "params": {"channel": "feishu_card", "target": "keychain:myia/feishu/chat_id"}},
    )
    result = responses[0]["result"]
    assert result == {"ok": True, "channel": "feishu_card"}  # 非 stdout 无 preview
    assert sent["target"] == "keychain:myia/feishu/chat_id"
    assert "MYIA 推送测试" in sent["items"][0]["title"]
    assert sent["context"].kind == "immediate"


# ---------------------------------------------------------------------------
# feed.enrich(10-03-fe-small-batch G8,协议 v6 #43):单条情报卡 AI 摘要,
# 骑 myssia.enrich.LLMEnricher 同门管线(端点 env: 引用 + enrich_cache 复用)
# ---------------------------------------------------------------------------


ENRICH_YAML = """
id: feed-enrich-demo
name: 精评夹具品类
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:9/list"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.data[*].title"
        url: "$.data[*].url"
classify:
  builtin: false
watchlist:
  keywords: ["模型"]
enrich:
  enabled: true
  model: fake-model-x
  scores: [value, relevance]
  base_url: "env:MYIA_TEST_ENRICH_BASE"
  api_key: "env:MYIA_TEST_ENRICH_KEY"
push:
  - channel: stdout
"""

ENRICH_URL = "https://example.com/enrich-1"
ENRICH_KEY = "enrich-key-1"


class _FakeCompletion:
    """Scripted completion client(tests/test_enrich.py FakeCompletionClient
    同款);零外网,fake 注入走 entry.LLMEnricher 的 client= 关键字。"""

    def __init__(self, responses: list[str] | None = None, *, fail: bool = False):
        self.responses = list(responses or [])
        self.fail = fail
        self.calls: list[str] = []

    async def complete(self, *, model: str, system: str, user: str):
        from myssia.enrich.client import CompletionResult

        self.calls.append(user)
        if self.fail:
            raise RuntimeError("模拟端点故障")
        text = self.responses.pop(0) if self.responses else "[]"
        return CompletionResult(text=text, total_tokens=88)


def _inject_enrich_client(monkeypatch, client: _FakeCompletion) -> None:
    """handler 侧 LLMEnricher(config, settings) → 真类 + 注入 fake client。"""
    real = entry.LLMEnricher
    monkeypatch.setattr(
        entry, "LLMEnricher",
        lambda config, settings: real(config, settings, client=client),
    )


def _enrich_home(tmp_path: Path, monkeypatch, yaml_text: str = ENRICH_YAML) -> Path:
    """MYIA_HOME 模式夹具:<home>/plugins 放品类 YAML(端点 env: 引用密闭)。"""
    home = tmp_path / "enrich-home"
    (home / "plugins").mkdir(parents=True, exist_ok=True)  # 同测多次换 YAML 复用
    (home / "plugins" / "demo.yaml").write_text(yaml_text, encoding="utf-8")
    monkeypatch.setenv("MYIA_HOME", str(home))
    return home


def _seed_enrich_db(tmp_path: Path, *, category: str = "feed-enrich-demo") -> str:
    """一条带 content 的种子条目(category 可指向不存在的品类测拒配)。"""
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord

    db = tmp_path / "enrich.db"
    store = SQLiteStore(str(db))
    store.save_item(ItemRecord(
        url=ENRICH_URL, dedup_key=ENRICH_KEY, title="精评条目:模型发布了",
        category=category, content="正文摘要一段",
        first_seen=datetime(2026, 10, 3, tzinfo=timezone.utc),
    ))
    store.close()
    return str(db)


def test_feed_enrich_fresh_then_cache_roundtrip(tmp_path, monkeypatch):
    """G8 往返:首评 LLM(shape 同 fake 端点)→ 二评 enrich_cache 命中零
    token;分数回填 items 表(缓存命中路径同回填,管线契约)。"""
    import json as _json

    _enrich_home(tmp_path, monkeypatch)
    monkeypatch.setenv("MYIA_TEST_ENRICH_BASE", "https://llm.test.local/v1")
    monkeypatch.setenv("MYIA_TEST_ENRICH_KEY", "test-key-not-real")
    db = _seed_enrich_db(tmp_path)
    reply = _json.dumps(
        [{"url": ENRICH_URL, "value": 8, "relevance": 9, "reason": "干货"}],
        ensure_ascii=False,
    )
    client = _FakeCompletion([reply])
    _inject_enrich_client(monkeypatch, client)

    code, responses, _ = rpc(
        {"id": 1, "method": "feed.enrich", "params": {"db": db, "item": ENRICH_KEY}},
    )
    assert code == 0
    result = responses[0]["result"]
    assert set(result.keys()) == {"item_id", "model", "scores", "score", "cached"}
    assert isinstance(result["item_id"], int)
    assert result["model"] == "fake-model-x"  # 品类 enrich 节模型透传
    assert result["scores"] == {"value": 8, "relevance": 9}
    assert result["score"] == 8.5  # composite = 配置两维均值 1 位小数
    assert result["cached"] is False
    assert len(client.calls) == 1
    assert ENRICH_URL in client.calls[0] and "精评条目" in client.calls[0]

    # 二评:enrich_cache 命中 —— 零新调用,cached=true,分数同形
    code, responses, _ = rpc(
        {"id": 2, "method": "feed.enrich",
         "params": {"db": db, "item": str(responses[0]["result"]["item_id"])}},
    )
    cached_result = responses[0]["result"]
    assert cached_result["cached"] is True
    assert cached_result["scores"] == result["scores"] and cached_result["score"] == 8.5
    assert len(client.calls) == 1

    # items 行回填复核:扁平维度 + score 标量(_persist_scores 契约)
    store = SQLiteStore(db)
    try:
        row = store.get_item_by_dedup_key(ENRICH_KEY)
        assert row.scores == {"value": 8, "relevance": 9, "score": 8.5}
    finally:
        store.close()


def test_feed_enrich_not_configured_three_reasons(tmp_path, monkeypatch):
    """graceful 拒配三分:enrich_disabled / endpoint_missing /
    category_yaml_not_found;另 item_not_found / invalid_params 拒绝面。"""
    # ① enabled=false → enrich_disabled
    _enrich_home(tmp_path, monkeypatch, yaml_text=ENRICH_YAML.replace("enabled: true", "enabled: false"))
    db = _seed_enrich_db(tmp_path)
    code, responses, _ = rpc(
        {"id": 1, "method": "feed.enrich", "params": {"db": db, "item": ENRICH_KEY}},
    )
    error = responses[0]["error"]
    assert error["code"] == "enrich_not_configured"
    assert error["data"]["reason"] == "enrich_disabled"

    # ② 启用但缺端点引用(api_key 留空)→ endpoint_missing
    _enrich_home(tmp_path, monkeypatch,
                 yaml_text=ENRICH_YAML.replace('  api_key: "env:MYIA_TEST_ENRICH_KEY"\n', ""))
    code, responses, _ = rpc(
        {"id": 2, "method": "feed.enrich", "params": {"db": db, "item": ENRICH_KEY}},
    )
    error = responses[0]["error"]
    assert error["code"] == "enrich_not_configured"
    assert error["data"]["reason"] == "endpoint_missing"

    # ③ 条目品类无 YAML(已删品类的历史条目)→ category_yaml_not_found
    _enrich_home(tmp_path, monkeypatch)
    db_ghost = _seed_enrich_db(tmp_path, category="ghost-category")
    code, responses, _ = rpc(
        {"id": 3, "method": "feed.enrich", "params": {"db": db_ghost, "item": ENRICH_KEY}},
    )
    error = responses[0]["error"]
    assert error["code"] == "enrich_not_configured"
    assert error["data"]["reason"] == "category_yaml_not_found"

    # 拒绝面:条目不存在 = item_not_found(同 feedback.mark 口径);缺 item = invalid_params
    code, responses, _ = rpc(
        {"id": 4, "method": "feed.enrich", "params": {"db": db, "item": "no-such"}},
    )
    assert responses[0]["error"]["code"] == "item_not_found"
    code, responses, _ = rpc(
        {"id": 5, "method": "feed.enrich", "params": {"db": db}},
    )
    assert responses[0]["error"]["code"] == "invalid_params"


def test_feed_enrich_endpoint_error_passthrough_and_unscored(tmp_path, monkeypatch):
    """EnrichConfigError code 原文透传(env 未设 = credential_unresolved);
    端点故障批次失败条目未获分 = enrich_failed(degrade_reason 入 data)。"""
    # ① 端点 env: 引用配置了但环境变量未设 → 构造期 credential_unresolved
    _enrich_home(tmp_path, monkeypatch)  # 不 setenv 两个 MYIA_TEST_ENRICH_* 变量
    db = _seed_enrich_db(tmp_path)
    code, responses, _ = rpc(
        {"id": 1, "method": "feed.enrich", "params": {"db": db, "item": ENRICH_KEY}},
    )
    assert responses[0]["error"]["code"] == "credential_unresolved"

    # ② 端点整批失败(LLMEnricher 降级不中断 → 条目无分 → handler 结构化收口)
    monkeypatch.setenv("MYIA_TEST_ENRICH_BASE", "https://llm.test.local/v1")
    monkeypatch.setenv("MYIA_TEST_ENRICH_KEY", "test-key-not-real")
    _inject_enrich_client(monkeypatch, _FakeCompletion(fail=True))
    code, responses, _ = rpc(
        {"id": 2, "method": "feed.enrich", "params": {"db": db, "item": ENRICH_KEY}},
    )
    error = responses[0]["error"]
    assert error["code"] == "enrich_failed"
    assert error["data"]["degrade_reason"] == "llm_batch_failed"
    assert error["data"]["failures"][0]["url"] == ENRICH_URL


# ---------------------------------------------------------------------------
# bridge.status(10-03-messaging-weixin-bridge,协议 v4 #31):微信桥接探测
# ---------------------------------------------------------------------------


def _weixin_bridge_fixture(tmp_path, monkeypatch, *, bin_=True, accounts=True, with_yaml=True):
    """桥接探测夹具:HERMES_HOME 指向 tmp(MYIA home 复用),YAML 带 weixin
    条目的 ``weixin_hermes_bin`` 覆写 → 探测完全密闭(不触真机 ~/.hermes)。"""
    script = tmp_path / "hermes-bin"
    yaml_text = None
    if with_yaml:
        yaml_text = WEIXIN_BRIDGE_YAML.format(bin_path=str(script))
    home = _messaging_home(tmp_path, monkeypatch, yaml_text=yaml_text)
    monkeypatch.setenv("HERMES_HOME", str(home))
    if bin_:
        script.write_text("#!/bin/sh\n:", encoding="utf-8")
        script.chmod(0o755)
    if accounts:
        acc = home / "weixin" / "accounts"
        acc.mkdir(parents=True, exist_ok=True)
        (acc / "bot@im.bot.json").write_text("{}", encoding="utf-8")
    return home, script


#: 桥接品类夹具:weixin push 条目带 targets + bin 路径覆写(占位符运行期代入)。
WEIXIN_BRIDGE_YAML = """
id: weixin-bridge-demo
name: 桥接夹具
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:9/list"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.data[*].title"
        url: "$.data[*].url"
push:
  - channel: weixin
    targets:
      - weixin:peer123@im.wechat
    weixin_hermes_bin: "{bin_path}"
"""


def test_bridge_status_all_present_available(tmp_path, monkeypatch):
    """正例:bin + accounts 在场 → available=True、reason=None,七键齐全,
    bin 路径取 YAML ``weixin_hermes_bin`` 覆写(design D2/D4)。"""
    _home, script = _weixin_bridge_fixture(tmp_path, monkeypatch)

    code, responses, _ = rpc({"id": 1, "method": "bridge.status", "params": {}})

    assert code == 0
    result = responses[0]["result"]
    assert set(result) == {
        "available",
        "reason",
        "fix_hint",
        "bin_found",
        "weixin_configured",
        "gateway_alive",
        "bin_path",
    }
    assert result["available"] is True
    assert (result["reason"], result["fix_hint"]) == (None, None)
    assert result["bin_found"] is True and result["weixin_configured"] is True
    assert result["gateway_alive"] is False  # 咨询信号:无 sock 不影响 available
    assert result["bin_path"] == str(script)


def test_bridge_status_bin_missing_structured(tmp_path, monkeypatch):
    """bin 缺失形态:hermes_missing + 修复指引含 weixin_hermes_bin(R2)。"""
    _home, _script = _weixin_bridge_fixture(tmp_path, monkeypatch, bin_=False)

    code, responses, _ = rpc({"id": 1, "method": "bridge.status", "params": {}})

    result = responses[0]["result"]
    assert result["available"] is False
    assert result["reason"] == "hermes_missing"
    assert "weixin_hermes_bin" in result["fix_hint"]
    assert result["bin_found"] is False and result["weixin_configured"] is True


def test_bridge_status_weixin_not_configured_structured(tmp_path, monkeypatch):
    """accounts 缺失形态:weixin_not_configured + 扫码指引(available=False)。"""
    _home, _script = _weixin_bridge_fixture(tmp_path, monkeypatch, accounts=False)

    code, responses, _ = rpc({"id": 1, "method": "bridge.status", "params": {}})

    result = responses[0]["result"]
    assert result["available"] is False
    assert result["reason"] == "weixin_not_configured"
    assert "gateway setup" in result["fix_hint"]
    assert result["bin_found"] is True and result["weixin_configured"] is False


def test_bridge_status_without_yaml_uses_default_bin_path(tmp_path, monkeypatch):
    """无 weixin 条目:探测缺省 bin 路径(只断言路径键,存在性随真机)。"""
    home, _script = _weixin_bridge_fixture(
        tmp_path, monkeypatch, bin_=False, accounts=False, with_yaml=False
    )

    code, responses, _ = rpc({"id": 1, "method": "bridge.status", "params": {}})

    result = responses[0]["result"]
    assert result["bin_path"].endswith(".hermes/bin/hermes")
    # 缺省路径(真机形态未知)但应答本身永不报错:探测是纯展示信息
    assert isinstance(result["available"], bool)


def test_bridge_status_bad_yaml_does_not_block_probe(tmp_path, monkeypatch):
    """坏品类 YAML:跳过不阻塞探测(yaml.list 自会如实展示其错误)。"""
    home = _messaging_home(tmp_path, monkeypatch, yaml_text=None)
    (home / "plugins" / "broken.yaml").write_text("id: [broken", encoding="utf-8")
    monkeypatch.setenv("HERMES_HOME", str(home))

    code, responses, _ = rpc({"id": 1, "method": "bridge.status", "params": {}})

    assert code == 0
    assert "available" in responses[0]["result"]


# ---------------------------------------------------------------------------
# image.models.* / image.server.*(10-03-vision-v2;契约与前端 TS 侧同形状冻结:
# list→{models:[{name,path,bytes,active}]};download→{job_id}+progress/completed
# 两事件;delete/activate→{ok};status→{running,base_url,model,healthy};
# ensure→status+{started})
# ---------------------------------------------------------------------------


def _vision_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """MYIA_HOME 指到 tmp;建 models 目录,返回 home。"""
    home = tmp_path / "home"
    monkeypatch.setenv("MYIA_HOME", str(home))
    (home / "models").mkdir(parents=True)
    return home


def _seed_model(home: Path, name: str, size: int = 64, *, incomplete: bool = False) -> Path:
    """种一个模型目录;incomplete=True 只落半截权重(无 config.json)。"""
    model_dir = home / "models" / name
    model_dir.mkdir(parents=True, exist_ok=True)
    (model_dir / "w.safetensors").write_bytes(b"x" * size)
    if not incomplete:
        (model_dir / "config.json").write_text("{}", encoding="utf-8")
    return model_dir


def test_image_models_list_roundtrip(tmp_path, monkeypatch):
    """models.list:扫描 + active/incomplete 标;空目录空表。"""
    home = _vision_home(tmp_path, monkeypatch)
    _seed_model(home, "qwen-4bit", 100)
    _seed_model(home, "smol-250m", 10)
    (home / "models" / "README.md").write_text("杂文件不算")
    code, responses, _ = rpc({"id": 1, "method": "image.models.list", "params": {}})
    result = responses[0]["result"]
    assert [m["name"] for m in result["models"]] == ["qwen-4bit", "smol-250m"]
    by_name = {m["name"]: m for m in result["models"]}
    config_bytes = (home / "models" / "qwen-4bit" / "config.json").stat().st_size
    assert by_name["qwen-4bit"]["bytes"] == 100 + config_bytes
    assert by_name["smol-250m"]["active"] is False  # vision.yaml 未配 → 全部非激活
    assert by_name["qwen-4bit"]["incomplete"] is False  # 完整(config+权重齐)

    # 激活一个(vision.yaml local.model)后 active 标翻转
    (home / "vision.yaml").write_text(
        "local:\n  model: " + str((home / "models" / "qwen-4bit").resolve()) + "\n",
        encoding="utf-8",
    )
    code, responses, _ = rpc({"id": 2, "method": "image.models.list", "params": {}})
    by_name = {m["name"]: m for m in responses[0]["result"]["models"]}
    assert by_name["qwen-4bit"]["active"] is True
    assert by_name["smol-250m"]["active"] is False


def test_image_models_list_marks_incomplete(tmp_path, monkeypatch):
    """半成品目录(缺 config.json / 缺 *.safetensors)标 incomplete=true。"""
    home = _vision_home(tmp_path, monkeypatch)
    _seed_model(home, "half-weights", 50, incomplete=True)  # 有权重无 config
    no_weights = home / "models" / "no-weights"
    no_weights.mkdir()
    (no_weights / "config.json").write_text("{}", encoding="utf-8")  # 有 config 无权重
    code, responses, _ = rpc({"id": 1, "method": "image.models.list", "params": {}})
    by_name = {m["name"]: m for m in responses[0]["result"]["models"]}
    assert by_name["half-weights"]["incomplete"] is True
    assert by_name["no-weights"]["incomplete"] is True


def test_image_models_list_empty_home_is_legal(tmp_path, monkeypatch):
    """零模型 = 合法空表(下载引导态,不报错)。"""
    _vision_home(tmp_path, monkeypatch)
    code, responses, _ = rpc({"id": 1, "method": "image.models.list", "params": {}})
    assert responses[0]["result"] == {"models": []}


def test_image_models_download_job_and_events(tmp_path, monkeypatch):
    """download:提交即返 job_id;progress/completed 两事件形状冻结。"""
    home = _vision_home(tmp_path, monkeypatch)
    calls: dict[str, Any] = {}

    def fake_download(repo, models_root, *, name=None, on_progress=None):
        calls["repo"] = repo
        calls["name"] = name
        calls["root"] = str(models_root)
        calls["dir"] = (home / "models" / "qwen-4bit").mkdir()
        if on_progress is not None:
            on_progress(100, 200)
            on_progress(200, 200)
        return home / "models" / "qwen-4bit"

    monkeypatch.setattr(entry, "vision_download_model", fake_download)
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({
        "id": 1, "method": "image.models.download",
        "params": {"repo": "mlx-community/qwen-4bit"},
    }) + "\n")
    assert entry.serve(stdin=stdin, stdout=out) == 0
    responses, _ = split_stream(out)
    job_id = responses[0]["result"]["job_id"]
    assert isinstance(job_id, int)

    deadline = time.monotonic() + 10
    events: list[dict] = []
    while time.monotonic() < deadline:
        _, events = split_stream(out)
        if any(e["type"] == "image.models.completed" for e in events):
            break
        time.sleep(0.05)
    progress = [e for e in events if e["type"] == "image.models.progress"]
    completed = [e for e in events if e["type"] == "image.models.completed"]
    assert progress, "进度事件必须发生"
    assert progress[0]["job_id"] == job_id
    assert progress[0]["repo"] == "mlx-community/qwen-4bit"
    assert progress[0]["done_bytes"] == 100 and progress[0]["total_bytes"] == 200
    assert progress[-1]["done_bytes"] == 200
    assert completed and completed[0]["ok"] is True
    assert completed[0]["job_id"] == job_id
    assert "error" not in completed[0]
    assert calls["repo"] == "mlx-community/qwen-4bit"
    assert calls["name"] is None  # 缺省 = repo 名段
    assert calls["root"] == str(home / "models")


def test_image_models_download_failure_event_and_busy(tmp_path, monkeypatch):
    """下载失败:completed{ok:false, error=code};并发第二单 download_busy。"""
    _vision_home(tmp_path, monkeypatch)
    release = threading.Event()

    def failing_download(repo, models_root, *, name=None, on_progress=None):
        release.wait(timeout=10)  # 钉住第一单,确保第二单撞单飞窗口
        raise entry.VisionModelError("disk_insufficient", "磁盘不足")

    monkeypatch.setattr(entry, "vision_download_model", failing_download)
    out = io.StringIO()
    stdin = io.StringIO("".join(line + "\n" for line in [
        json.dumps({"id": 1, "method": "image.models.download",
                    "params": {"repo": "mlx-community/qwen-4bit"}}),
        json.dumps({"id": 2, "method": "image.models.download",
                    "params": {"repo": "mlx-community/other"}}),
    ]))
    entry.serve(stdin=stdin, stdout=out)
    responses, _ = split_stream(out)
    # 第二单撞第一单(单飞):结构化 download_busy(不是 500)
    assert responses[1]["error"]["code"] == "download_busy"
    release.set()
    deadline = time.monotonic() + 10
    completed: list[dict] = []
    while time.monotonic() < deadline:
        _, events = split_stream(out)
        completed = [e for e in events if e["type"] == "image.models.completed"]
        if completed:
            break
        time.sleep(0.05)
    assert completed[0]["ok"] is False
    assert completed[0]["error"] == "disk_insufficient"


def test_image_models_download_invalid_params(tmp_path, monkeypatch):
    """缺 repo / 非 mlx-community 前缀:invalid_params/invalid_repo 结构化拒。"""
    _vision_home(tmp_path, monkeypatch)
    code, responses, _ = rpc({"id": 1, "method": "image.models.download", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert responses[0]["error"]["path"] == "params.repo"
    # 非 mlx-community repo:同步快速失败(校验在 download_model 内,job 事件收口)
    monkeypatch.setattr(entry, "vision_download_model",
                        lambda *a, **k: (_ for _ in ()).throw(
                            entry.VisionModelError("invalid_repo", "只收 mlx-community")))
    out = io.StringIO()
    stdin = io.StringIO(json.dumps({
        "id": 2, "method": "image.models.download",
        "params": {"repo": "Qwen/Qwen2-VL"}}) + "\n")
    entry.serve(stdin=stdin, stdout=out)
    responses, _ = split_stream(out)
    assert responses[0]["result"]["job_id"] == 1  # 提交照常,失败走事件


def test_image_models_delete_and_activate_roundtrip(tmp_path, monkeypatch):
    """delete/activate → {ok};active 拒删 model_active_refused;激活写 vision.yaml;
    半成品拒激活 model_incomplete(零写入)。"""
    home = _vision_home(tmp_path, monkeypatch)
    _seed_model(home, "qwen-4bit")
    _seed_model(home, "smol-250m")
    _seed_model(home, "half-done", incomplete=True)
    # 激活 qwen-4bit
    code, responses, _ = rpc({"id": 1, "method": "image.models.activate",
                              "params": {"name": "qwen-4bit"}})
    assert responses[0]["result"] == {"ok": True}
    vision_text = (home / "vision.yaml").read_text(encoding="utf-8")
    assert str((home / "models" / "qwen-4bit").resolve()) in vision_text
    # 半成品拒激活:vision.yaml 零改写(local.model 仍指 qwen-4bit)
    code, responses, _ = rpc({"id": 2, "method": "image.models.activate",
                              "params": {"name": "half-done"}})
    assert responses[0]["error"]["code"] == "model_incomplete"
    assert (home / "vision.yaml").read_text(encoding="utf-8") == vision_text
    # active 拒删
    code, responses, _ = rpc({"id": 3, "method": "image.models.delete",
                              "params": {"name": "qwen-4bit"}})
    assert responses[0]["error"]["code"] == "model_active_refused"
    assert (home / "models" / "qwen-4bit").exists()  # 拒删 = 目录原样
    # 非激活模型正常删(半成品也可删 = 放弃续传)
    code, responses, _ = rpc({"id": 4, "method": "image.models.delete",
                              "params": {"name": "smol-250m"}})
    assert responses[0]["result"] == {"ok": True}
    assert not (home / "models" / "smol-250m").exists()
    # 未知模型结构化 404 族
    code, responses, _ = rpc({"id": 5, "method": "image.models.delete",
                              "params": {"name": "ghost"}})
    assert responses[0]["error"]["code"] == "model_not_found"
    code, responses, _ = rpc({"id": 6, "method": "image.models.delete", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_image_server_status_roundtrip_local_http(tmp_path, monkeypatch, local_api):
    """server.status:对本地 /models 端点 running/healthy;死端口全 False。"""
    home = _vision_home(tmp_path, monkeypatch)
    port = local_api  # 复用直 API 夹具服务器(任意路径回 200 JSON)
    (home / "vision.yaml").write_text(
        f"local:\n  base_url: http://127.0.0.1:{port}/v1\n  model: /m/qwen\n",
        encoding="utf-8",
    )
    code, responses, _ = rpc({"id": 1, "method": "image.server.status", "params": {}})
    assert responses[0]["result"] == {
        "running": True,
        "base_url": f"http://127.0.0.1:{port}/v1",
        "model": "/m/qwen",
        "healthy": True,
    }
    # 死端口:vision.yaml 指向无人听的 127.0.0.1:9
    (home / "vision.yaml").write_text(
        "local:\n  base_url: http://127.0.0.1:9/v1\n  model: /m/qwen\n",
        encoding="utf-8",
    )
    code, responses, _ = rpc({"id": 2, "method": "image.server.status", "params": {}})
    result = responses[0]["result"]
    assert result["running"] is False and result["healthy"] is False


def _wait_for_event(out: io.StringIO, event_type: str, timeout: float = 10.0) -> dict:
    """轮询协议流直到指定事件出现(后台线程写,serve 主线程已 EOF)。"""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        _, events = split_stream(out)
        found = [e for e in events if e.get("type") == event_type]
        if found:
            return found[-1]
        time.sleep(0.05)
    raise AssertionError(f"{event_type} 事件在 {timeout}s 内未出现")


def _reset_ensure_job() -> None:
    """清 ensure 单飞位(防上例失败残留串扰;同 sources.test 的 _TEST_ACTIVE_JOB)。"""
    entry._SERVER_ENSURE_ACTIVE_JOB = None


def test_image_server_ensure_paths(tmp_path, monkeypatch):
    """ensure 新契约:快路径已健康 = status+{started} 即返零事件;慢路径应答
    立即返快照超集 + {ensuring, job_id},终态走 image.server.completed 事件
    (ok 时带 status;错误族以 error code 收口)—— serve 循环不再被 120s
    健康窗冻住。

    探测统一桩死(dev 主机 8080 可能真跑着 mlx_vlm.server,测试绝不碰真网);
    ①走真 ensure 实现,②③走 entry 能力桩。
    """
    import myssia.vision.server as vision_server_module
    monkeypatch.setattr(vision_server_module, "_probe",
                        lambda url, timeout=2.0: (False, False))
    home = _vision_home(tmp_path, monkeypatch)
    _reset_ensure_job()

    # ① vision.yaml 未配 local.model 且探测未跑:应答立即返(ensuring) +
    #    completed{ok:false, error:no_local_model} 事件收口
    out = io.StringIO()
    stdin = io.StringIO(json.dumps(
        {"id": 1, "method": "image.server.ensure", "params": {}}) + "\n")
    entry.serve(stdin=stdin, stdout=out)
    responses, _ = split_stream(out)
    result = responses[0]["result"]
    assert result["ensuring"] is True and isinstance(result["job_id"], int)
    assert result["healthy"] is False and result["started"] is False  # 快照原样
    completed = _wait_for_event(out, "image.server.completed")
    assert completed["ok"] is False
    assert completed["error"] == "no_local_model"
    assert "status" not in completed

    # ② 已健康:快路径,应答即终态(status+started)零事件
    monkeypatch.setattr(vision_server_module, "_probe",
                        lambda url, timeout=2.0: (True, True))
    _seed_model(home, "qwen-4bit")
    (home / "vision.yaml").write_text(
        "local:\n  model: " + str((home / "models" / "qwen-4bit").resolve()) + "\n",
        encoding="utf-8",
    )
    code, responses, events = rpc({"id": 2, "method": "image.server.ensure", "params": {}})
    assert responses[0]["result"] == {
        "running": True,
        "base_url": "http://127.0.0.1:8080/v1",
        "model": str((home / "models" / "qwen-4bit").resolve()),
        "healthy": True,
        "started": False,
    }
    assert "ensuring" not in responses[0]["result"]
    assert [e for e in events if e["type"] == "image.server.completed"] == []

    # ③ 慢路径真自起:能力桩回 started=true → completed{ok:true, status}
    monkeypatch.setattr(vision_server_module, "_probe",
                        lambda url, timeout=2.0: (False, False))

    def _spawning(cfg, **kwargs):
        return {"running": True, "base_url": cfg.local_base_url,
                "model": cfg.local_model, "healthy": True, "started": True}

    monkeypatch.setattr(entry, "ensure_vision_server", _spawning)
    out = io.StringIO()
    stdin = io.StringIO(json.dumps(
        {"id": 3, "method": "image.server.ensure", "params": {}}) + "\n")
    entry.serve(stdin=stdin, stdout=out)
    responses, _ = split_stream(out)
    assert responses[0]["result"]["ensuring"] is True
    completed = _wait_for_event(out, "image.server.completed")
    assert completed["ok"] is True
    assert completed["status"]["started"] is True
    assert completed["status"]["healthy"] is True

    # ④ 代管层失败(如 uvx 缺装):completed{ok:false, error:spawn_failed}
    def _failing(cfg, **kwargs):
        raise entry.VisionServerError("spawn_failed", "uvx 不可用")

    monkeypatch.setattr(entry, "ensure_vision_server", _failing)
    out = io.StringIO()
    stdin = io.StringIO(json.dumps(
        {"id": 4, "method": "image.server.ensure", "params": {}}) + "\n")
    entry.serve(stdin=stdin, stdout=out)
    responses, _ = split_stream(out)
    assert responses[0]["result"]["ensuring"] is True
    completed = _wait_for_event(out, "image.server.completed")
    assert completed["ok"] is False and completed["error"] == "spawn_failed"


def test_image_server_ensure_single_flight_busy(tmp_path, monkeypatch):
    """ensure 单飞:慢路径进行中第二单结构化 ensure_busy(不排队不双起)。"""
    import myssia.vision.server as vision_server_module
    monkeypatch.setattr(vision_server_module, "_probe",
                        lambda url, timeout=2.0: (False, False))
    _vision_home(tmp_path, monkeypatch)
    _reset_ensure_job()
    release = threading.Event()

    def _pinned(cfg, **kwargs):
        release.wait(timeout=10)  # 钉住第一单,确保第二单撞单飞窗口
        return {"running": True, "base_url": cfg.local_base_url,
                "model": cfg.local_model, "healthy": True, "started": True}

    monkeypatch.setattr(entry, "ensure_vision_server", _pinned)
    out = io.StringIO()
    stdin = io.StringIO("".join(line + "\n" for line in [
        json.dumps({"id": 1, "method": "image.server.ensure", "params": {}}),
        json.dumps({"id": 2, "method": "image.server.ensure", "params": {}}),
    ]))
    entry.serve(stdin=stdin, stdout=out)
    responses, _ = split_stream(out)
    # 第二单撞第一单(单飞):结构化 ensure_busy(不是 500);第一单已受理
    assert responses[0]["result"]["ensuring"] is True
    assert responses[1]["error"]["code"] == "ensure_busy"
    assert responses[1]["error"]["data"]["active_job_id"] == responses[0]["result"]["job_id"]
    release.set()
    completed = _wait_for_event(out, "image.server.completed")
    assert completed["ok"] is True


# ---------------------------------------------------------------------------
# image.files.purge(10-03-vision-v2 复查:落图零回收的 CLI 面清除口)
# ---------------------------------------------------------------------------


def test_image_files_purge_by_mtime(tmp_path, monkeypatch):
    """purge:按文件 mtime 清 <数据根>/images 超龄文件 → {deleted, bytes_freed};
    新文件保留;目录不存在 = 合法零删。"""
    import os

    home = _vision_home(tmp_path, monkeypatch)
    images = home / "images"
    images.mkdir()
    old_a = images / "aaaa1111bbbb2222.png"
    old_b = images / "cccc3333dddd4444.jpg"
    fresh = images / "eeee5555ffff6666.png"
    old_a.write_bytes(b"x" * 100)
    old_b.write_bytes(b"y" * 40)
    fresh.write_bytes(b"z" * 10)
    week_ago = time.time() - 7 * 86400
    os.utime(old_a, (week_ago, week_ago))
    os.utime(old_b, (week_ago - 86400, week_ago - 86400))

    code, responses, _ = rpc({"id": 1, "method": "image.files.purge", "params": {"days": 7}})
    assert responses[0]["result"] == {"deleted": 2, "bytes_freed": 140}
    assert not old_a.exists() and not old_b.exists()
    assert fresh.exists()  # 新文件不动

    # 再跑一次:已清空 → 零删幂等
    code, responses, _ = rpc({"id": 2, "method": "image.files.purge", "params": {"days": 7}})
    assert responses[0]["result"] == {"deleted": 0, "bytes_freed": 0}

    # 目录不存在 = 合法零删(不报错)
    shutil.rmtree(images)
    code, responses, _ = rpc({"id": 3, "method": "image.files.purge", "params": {"days": 1}})
    assert responses[0]["result"] == {"deleted": 0, "bytes_freed": 0}


def test_image_files_purge_rejects_bad_days(tmp_path, monkeypatch):
    """days 非 int / <1 / 布尔( isinstance(bool,int) 的坑)/ 缺失 → invalid_params。"""
    _vision_home(tmp_path, monkeypatch)
    for bad in (0, -3, "7", 1.5, True, None):
        params = {} if bad is None else {"days": bad}
        code, responses, _ = rpc({"id": 1, "method": "image.files.purge", "params": params})
        assert responses[0]["error"]["code"] == "invalid_params", bad
        assert responses[0]["error"]["path"] == "params.days"


# ---------------------------------------------------------------------------
# feedback.mark / feedback.list / feedback.stats + store.trend + version.app_version
# (B2/B4/C10,10-03-v112-desktop-parity 第二切片;CLI 往返一致 = channel=desktop
# 落 feedback 表,CLI `myssia feedback list` 无过滤即见同一条目)
# ---------------------------------------------------------------------------


def _seed_feedback_db(tmp_path: Path) -> str:
    """带一条目 + 一条既有 CLI 反馈的种子库(mark 往返的对照面)。"""
    from datetime import datetime, timezone

    from myssia.store.models import FEEDBACK_CHANNEL_CLI, FeedbackRecord, ItemRecord

    db = tmp_path / "feedback.db"
    store = SQLiteStore(str(db))
    store.save_item(ItemRecord(
        url="https://example.com/fb", dedup_key="fb-key-1", title="反馈条目",
        category="proto-demo", first_seen=datetime(2026, 10, 3, tzinfo=timezone.utc),
    ))
    store.save_feedback(FeedbackRecord(
        dedup_key="fb-key-0", verdict="good", channel=FEEDBACK_CHANNEL_CLI,
        item_id=None, title="旧条", category=None,
        created_at=datetime(2026, 10, 2, tzinfo=timezone.utc),
    ))
    store.close()
    return str(db)


def test_feedback_mark_list_roundtrip(tmp_path):
    """mark(dedup_key 身份,channel=desktop)→ list 可见同条;item_not_found 拒。"""
    db = _seed_feedback_db(tmp_path)
    code, responses, _ = rpc(
        {"id": 1, "method": "feedback.mark",
         "params": {"db": db, "item": "fb-key-1", "verdict": "good"}},
    )
    assert code == 0
    result = responses[0]["result"]
    assert result["channel"] == "desktop"
    assert result["dedup_key"] == "fb-key-1"
    assert result["verdict"] == "good"
    assert isinstance(result["feedback_id"], int)

    # list:CLI 旧行 + 桌面新行都可见(往返一致;CLI feedback list 同表无过滤)
    code, responses, _ = rpc(
        {"id": 2, "method": "feedback.list", "params": {"db": db}},
    )
    listing = responses[0]["result"]
    assert listing["count"] == 2
    newest = listing["items"][0]  # 新→旧
    assert newest["channel"] == "desktop" and newest["dedup_key"] == "fb-key-1"
    assert set(newest.keys()) == {
        "id", "item_id", "dedup_key", "verdict", "channel", "title", "category", "created_at",
    }
    # 过滤:channel=desktop 只剩桌面行;verdict 过滤同理
    code, responses, _ = rpc(
        {"id": 3, "method": "feedback.list",
         "params": {"db": db, "channel": "desktop"}},
    )
    assert responses[0]["result"]["count"] == 1

    # 拒绝面:条目不存在 = item_not_found;verdict 非法 = feedback
    code, responses, _ = rpc(
        {"id": 4, "method": "feedback.mark",
         "params": {"db": db, "item": "no-such-key", "verdict": "good"}},
    )
    assert responses[0]["error"]["code"] == "item_not_found"
    code, responses, _ = rpc(
        {"id": 5, "method": "feedback.mark",
         "params": {"db": db, "item": "fb-key-1", "verdict": "meh"}},
    )
    assert responses[0]["error"]["code"] == "feedback"


def test_feedback_stats_window_and_tuning_shape(tmp_path):
    """stats:窗口计数 + active_tuning/tuning_history 键对齐 CLI stats 载荷。"""
    db = _seed_feedback_db(tmp_path)
    code, responses, _ = rpc(
        {"id": 1, "method": "feedback.stats", "params": {"db": db, "window_days": 14}},
    )
    result = responses[0]["result"]
    assert result["window_days"] == 14
    assert result["stats"]["total"] == 1 and result["stats"]["good"] == 1
    assert result["stats"]["by_channel"] == {"cli": 1}
    assert "top_bad_categories" in result["stats"] and "top_bad_words" in result["stats"]
    assert "active_tuning" in result and isinstance(result["tuning_history"], list)
    # 参数形状拒绝:window_days 非法 = invalid_params
    code, responses, _ = rpc(
        {"id": 2, "method": "feedback.stats", "params": {"db": db, "window_days": 0}},
    )
    assert responses[0]["error"]["code"] == "invalid_params"


def test_store_trend_daily_counts_utc(tmp_path):
    """store.trend:items 按 first_seen UTC 逐日计数(旧→新);category 过滤 + 钳制。"""
    from datetime import datetime, timedelta, timezone

    from myssia.store.models import ItemRecord

    db = tmp_path / "trend.db"
    store = SQLiteStore(str(db))
    now = datetime.now(timezone.utc)
    plan = [
        (now, "tech", 2),                    # 今天:tech 2 条
        (now, "stocks", 1),                  # 今天:stocks 1 条
        (now - timedelta(days=1), "tech", 1),  # 昨天:tech 1 条
        (now - timedelta(days=40), "tech", 5),  # 40 天前:窗口(7 天)外
    ]
    for first_seen, category, count in plan:
        for index in range(count):
            store.save_item(ItemRecord(
                url=f"https://example.com/{category}-{first_seen.date()}-{index}",
                dedup_key=f"t-{category}-{first_seen.date()}-{index}", title="t",
                category=category, first_seen=first_seen,
            ))
    store.close()

    code, responses, _ = rpc(
        {"id": 1, "method": "store.trend", "params": {"db": str(db), "days": 7}},
    )
    days = responses[0]["result"]["days"]
    assert [row["date"] for row in days] == sorted({row["date"] for row in days})
    counts = {row["date"]: row["count"] for row in days}
    assert counts.get(now.date().isoformat()) == 3
    assert counts.get((now - timedelta(days=1)).date().isoformat()) == 1
    assert sum(counts.values()) == 4  # 40 天前不入窗

    # category 过滤 + days 钳制(0 → 1:只剩今天)
    code, responses, _ = rpc(
        {"id": 2, "method": "store.trend",
         "params": {"db": str(db), "days": 7, "category": "tech"}},
    )
    counts = {row["date"]: row["count"] for row in responses[0]["result"]["days"]}
    assert counts.get(now.date().isoformat()) == 2
    code, responses, _ = rpc(
        {"id": 3, "method": "store.trend", "params": {"db": str(db), "days": 0}},
    )
    assert sum(row["count"] for row in responses[0]["result"]["days"]) == 3
    # 参数形状:days 非整数 = invalid_params
    code, responses, _ = rpc(
        {"id": 4, "method": "store.trend", "params": {"db": str(db), "days": "7"}},
    )
    assert responses[0]["error"]["code"] == "invalid_params"


def test_version_app_version_passthrough(monkeypatch):
    """version.app_version:透传 MYIA_APP_VERSION;未注入 = null(dev/CLI 如实)。"""
    monkeypatch.delenv("MYIA_APP_VERSION", raising=False)
    code, responses, _ = rpc({"id": 1, "method": "version", "params": {}})
    assert responses[0]["result"]["app_version"] is None
    monkeypatch.setenv("MYIA_APP_VERSION", "1.1.2")
    code, responses, _ = rpc({"id": 2, "method": "version", "params": {}})
    assert responses[0]["result"]["app_version"] == "1.1.2"


# ---------------------------------------------------------------------------
# alert-rules 批(10-04-alert-rules Stage D,协议 v7 #44-47):alerts.list /
# save / delete / test 四方法 + alerts.fired 回放事件。契约钉死于任务档
# design.md §4:save 全量替换两道门 + diff 保 id;test dry 求值不真发不落
# fired;错误码 alert_rule_invalid / alert_not_found / item_not_found /
# alert_test_no_item。
# ---------------------------------------------------------------------------


def _alert_rule_payload(name="融资告警", when="'融资' in title", action="tag", **extra):
    """AlertRuleInput 载荷(tag 动作缺省;push 传 action_config)."""
    payload = {"name": name, "when": when, "action": action}
    if action == "tag":
        payload["action_config"] = {"tags": ["重要"]}
    else:
        payload["action_config"] = {"channel": "stdout"}
    payload.update(extra)
    return payload


def test_alerts_list_empty_is_legal_state(tmp_path):
    """零惊扰默认:不配规则 = 空表合法态,alerts.list 返回空数组。"""
    db = tmp_path / "alerts.db"
    SQLiteStore(str(db)).close()
    code, responses, _ = rpc({"id": 1, "method": "alerts.list", "params": {"db": str(db)}})
    result = responses[0]["result"]
    assert result["count"] == 0 and result["rules"] == []


def test_alerts_save_full_replacement_keeps_ids(tmp_path):
    """save 全量替换(diff 保 id):建两条 → 改一条(保 id 翻启停)+ 删一条 +
    新增一条;fired_count/last_fired_at 自 alert_fired 派生(计数不落规则行)."""
    from myssia.store.models import AlertFired

    db = tmp_path / "alerts.db"
    code, responses, _ = rpc({"id": 1, "method": "alerts.save", "params": {"db": str(db), "rules": [
        _alert_rule_payload(name="规则甲"),
        _alert_rule_payload(name="规则乙", when="'gpu' in title"),
    ]}})
    saved = responses[0]["result"]["rules"]
    assert responses[0]["result"]["ok"] is True
    assert [rule["id"] for rule in saved] == [1, 2]  # id 升序分配
    assert all(rule["fired_count"] == 0 and rule["last_fired_at"] is None for rule in saved)

    # 全量替换:只提交 id=2(停用)+ 新规则;id=1 被删,新规则拿新 id
    code, responses, _ = rpc({"id": 2, "method": "alerts.save", "params": {"db": str(db), "rules": [
        _alert_rule_payload(name="规则乙改", when="'gpu' in title", id=2, enabled=False),
        _alert_rule_payload(name="规则丙", when="'涨价' in title"),
    ]}})
    saved = responses[0]["result"]["rules"]
    assert [rule["id"] for rule in saved] == [2, 3]  # 保 id;删除的 id 不复用
    by_id = {rule["id"]: rule for rule in saved}
    assert by_id[2]["enabled"] is False and by_id[2]["name"] == "规则乙改"

    # 命中计数派生:直接落一条 fired 历史(协议层不造命中,store 直种)
    store = SQLiteStore(str(db))
    store.record_fired(AlertFired(rule_id=2, rule_name="规则乙改", dedup_key="dk-1",
                                  title="gpu 涨价", action="tag", action_status="tagged"))
    store.close()
    code, responses, _ = rpc({"id": 3, "method": "alerts.list", "params": {"db": str(db)}})
    by_id = {rule["id"]: rule for rule in responses[0]["result"]["rules"]}
    assert by_id[2]["fired_count"] == 1 and by_id[2]["last_fired_at"] is not None
    assert by_id[3]["fired_count"] == 0 and by_id[3]["last_fired_at"] is None

    # 空数组 = 清空规则表(回到零惊扰默认)
    code, responses, _ = rpc({"id": 4, "method": "alerts.save",
                              "params": {"db": str(db), "rules": []}})
    assert responses[0]["result"]["rules"] == []
    code, responses, _ = rpc({"id": 5, "method": "alerts.list", "params": {"db": str(db)}})
    assert responses[0]["result"]["count"] == 0


def test_alerts_save_invalid_rule_zero_write(tmp_path):
    """构造期拒整批零写入:坏 when / 坏 action / 未知键 / 坏 push 通道 /
    非对象元素 → alert_rule_invalid(data 三键 index/field/reason),库不动。"""
    db = tmp_path / "alerts.db"
    code, responses, _ = rpc({"id": 1, "method": "alerts.save",
                              "params": {"db": str(db), "rules": [_alert_rule_payload()]}})
    assert responses[0]["result"]["ok"] is True  # 先立一条好规则
    cases = [
        (_alert_rule_payload(when='__import__("os")'), "alert_rules.when_expr"),
        (_alert_rule_payload(action="email"), "alert_rules.action"),
        (_alert_rule_payload(when="'a' in title", foo="bar"), "foo"),
        (_alert_rule_payload(action="push", action_config={"channel": "pigeon"}), "push 动作的 channel"),
        ("不是对象", "rule"),
        (_alert_rule_payload(name="  "), "name"),
    ]
    for index, (bad_rule, field) in enumerate(cases):
        code, responses, _ = rpc({"id": 10 + index, "method": "alerts.save",
                                  "params": {"db": str(db), "rules": [bad_rule]}})
        error = responses[0]["error"]
        assert error["code"] == "alert_rule_invalid", bad_rule
        assert error["data"]["index"] == 0 and error["data"]["field"] == field
        assert error["data"]["reason"]
    # 第 2 条坏 → index=1,且第 1 条(好)也不落(整批零写入)
    code, responses, _ = rpc({"id": 20, "method": "alerts.save", "params": {"db": str(db), "rules": [
        _alert_rule_payload(name="好的"),
        _alert_rule_payload(when="scores['x'] > 1"),  # 白名单禁下标
    ]}})
    error = responses[0]["error"]
    assert error["code"] == "alert_rule_invalid" and error["data"]["index"] == 1
    code, responses, _ = rpc({"id": 21, "method": "alerts.list", "params": {"db": str(db)}})
    assert responses[0]["result"]["count"] == 1  # 仍是最初那一条
    # rules 非数组 = invalid_params(载荷形状,非构造期拒)
    code, responses, _ = rpc({"id": 22, "method": "alerts.save",
                              "params": {"db": str(db), "rules": "全部"}})
    assert responses[0]["error"]["code"] == "invalid_params"
    # 载荷带未知 id 更新 → alert_not_found(store 值错结构化)
    code, responses, _ = rpc({"id": 23, "method": "alerts.save", "params": {"db": str(db), "rules": [
        _alert_rule_payload(id=99),
    ]}})
    assert responses[0]["error"]["code"] == "alert_not_found"
    assert responses[0]["error"]["data"]["id"] == 99


def test_alerts_delete_keeps_fired_history(tmp_path):
    """delete:删定义行 fired 历史照留(命中历史是事实);未知 id 结构化拒。"""
    from myssia.store.models import AlertFired

    db = tmp_path / "alerts.db"
    code, responses, _ = rpc({"id": 1, "method": "alerts.save",
                              "params": {"db": str(db), "rules": [_alert_rule_payload()]}})
    rule_id = responses[0]["result"]["rules"][0]["id"]
    store = SQLiteStore(str(db))
    store.record_fired(AlertFired(rule_id=rule_id, rule_name="融资告警", dedup_key="dk",
                                  title="融资", action="tag", action_status="tagged"))
    store.close()

    code, responses, _ = rpc({"id": 2, "method": "alerts.delete",
                              "params": {"db": str(db), "id": rule_id}})
    assert responses[0]["result"] == {"ok": True, "id": rule_id}
    code, responses, _ = rpc({"id": 3, "method": "alerts.delete",
                              "params": {"db": str(db), "id": rule_id}})
    error = responses[0]["error"]
    assert error["code"] == "alert_not_found" and error["data"]["id"] == rule_id
    store = SQLiteStore(str(db))  # fired 行仍在(悬挂 rule_id 即历史事实)
    assert len(store.list_fired(rule_id=rule_id)) == 1
    store.close()
    code, responses, _ = rpc({"id": 4, "method": "alerts.delete",
                              "params": {"db": str(db), "id": "1"}})
    assert responses[0]["error"]["code"] == "invalid_params"


def _seed_alert_items(db, rows):
    """种库内条目(新→旧依序入库;返回 None,行 id 由调用方再查)."""
    from datetime import datetime, timezone

    from myssia.store.models import ItemRecord

    store = SQLiteStore(str(db))
    base = datetime(2026, 10, 4, tzinfo=timezone.utc)
    for index, (title, category) in enumerate(rows):
        store.save_item(ItemRecord(
            url=f"https://example.com/a{index}", dedup_key=f"ak-{index}", title=title,
            content=f"{title} 正文", source="api", category=category,
            first_seen=base.replace(hour=index + 1),
        ))
    store.close()


def test_alerts_test_synthetic_item_and_content_patch(tmp_path):
    """test 草稿形态:合成 item 任意子集(url 缺省合成);content 补丁
    ('融资' in content 原生 view 写不了,alert_view 补上);tag 动作展开。"""
    db = tmp_path / "alerts.db"
    SQLiteStore(str(db)).close()
    code, responses, _ = rpc({"id": 1, "method": "alerts.test", "params": {"db": str(db), "rule": _alert_rule_payload(
        when="'融资' in content",
    ), "item": {"title": "某公司公告", "content": "宣布完成新一轮融资"}}})
    result = responses[0]["result"]
    assert result["matched"] is True and result["muted"] is False
    assert result["actions"] == [{"action": "tag", "tags": ["重要"]}]
    assert "already_fired" not in result  # 仅 rule_id 形态携带
    # 不匹配路径 + metadata 平铺(metadata 子 dict 并进求值上下文)
    code, responses, _ = rpc({"id": 2, "method": "alerts.test", "params": {"db": str(db), "rule": _alert_rule_payload(
        when="'gpu' in title",
    ), "item": {"title": "无关条目", "metadata": {"author": "张三"}}}})
    assert responses[0]["result"]["matched"] is False


def test_alerts_test_stored_rule_and_item_forms(tmp_path):
    """test 取材形态:rule_id+item_id(库内条目)/ 缺省最近一条 / already_fired
    预查;错误码 alert_not_found / item_not_found / alert_test_no_item /
    invalid_params(互斥门)."""
    from myssia.store.models import AlertFired

    db = tmp_path / "alerts.db"
    code, responses, _ = rpc({"id": 1, "method": "alerts.save", "params": {"db": str(db), "rules": [
        _alert_rule_payload(name="标题匹配", when="'融资' in title")]}}
    )
    rule_id = responses[0]["result"]["rules"][0]["id"]
    _seed_alert_items(db, [("旧条目无关", "news"), ("新条目谈融资", "news")])
    store = SQLiteStore(str(db))
    item_ids = [row.id for row in store.list_items(limit=2)]  # 新→旧
    newest_id, older_id = item_ids[0], item_ids[1]
    # 种一条 fired:新条目(ak-1,index=1 是最新行)已触发过 → already_fired 预查为真
    store.record_fired(AlertFired(rule_id=rule_id, rule_name="标题匹配",
                                  dedup_key="ak-1", title="新条目谈融资",
                                  action="tag", action_status="tagged"))
    store.close()

    # rule_id + item_id:库内条目求值上下文(content 列还原,category 顶层)
    code, responses, _ = rpc({"id": 2, "method": "alerts.test",
                              "params": {"db": str(db), "rule_id": rule_id, "item_id": newest_id}})
    result = responses[0]["result"]
    assert result["matched"] is True and result["already_fired"] is True
    # rule_id + 无 item:缺省取最近一条(新→旧首行)
    code, responses, _ = rpc({"id": 3, "method": "alerts.test",
                              "params": {"db": str(db), "rule_id": rule_id}})
    assert responses[0]["result"]["matched"] is True  # 最近一条 = 谈融资的新条目
    # 旧条目(item_id 显式):不匹配
    code, responses, _ = rpc({"id": 4, "method": "alerts.test",
                              "params": {"db": str(db), "rule_id": rule_id, "item_id": older_id}})
    assert responses[0]["result"]["matched"] is False
    # 错误码矩阵
    code, responses, _ = rpc({"id": 5, "method": "alerts.test",
                              "params": {"db": str(db), "rule_id": 99, "item_id": newest_id}})
    assert responses[0]["error"]["code"] == "alert_not_found"
    code, responses, _ = rpc({"id": 6, "method": "alerts.test",
                              "params": {"db": str(db), "rule_id": rule_id, "item_id": 999}})
    assert responses[0]["error"]["code"] == "item_not_found"
    empty_db = tmp_path / "empty.db"
    SQLiteStore(str(empty_db)).close()
    code, responses, _ = rpc({"id": 7, "method": "alerts.test",
                              "params": {"db": str(empty_db), "rule": _alert_rule_payload()}})
    assert responses[0]["error"]["code"] == "alert_test_no_item"
    code, responses, _ = rpc({"id": 8, "method": "alerts.test",
                              "params": {"db": str(db), "rule": _alert_rule_payload(),
                                       "rule_id": rule_id}})
    assert responses[0]["error"]["code"] == "invalid_params"


def test_alerts_test_mute_and_eval_error(tmp_path):
    """test 语义:mute 压制(effective mute = 反馈 0.0 权重词,命中即未命中
    不评估)与 eval_error 如实上报(引擎运行期 WARNING+未命中的同款事实)."""
    from myssia.store.models import TuningRecord

    db = tmp_path / "alerts.db"
    _seed_alert_items(db, [("某公司完成融资", "news")])
    store = SQLiteStore(str(db))
    store.save_tuning(TuningRecord(kind="mute_weight",
                                   payload={"word": "融资", "weight": 0.0}))
    store.close()
    # mute 命中:matched False(跳过评估,引擎硬规则),muted True
    code, responses, _ = rpc({"id": 1, "method": "alerts.test", "params": {"db": str(db), "rule": _alert_rule_payload(
        when="'融资' in title",
    ), "item": {"title": "某公司完成融资", "url": "https://example.com/m"}}})
    result = responses[0]["result"]
    assert result["muted"] is True and result["matched"] is False
    # eval_error:score 缺失(enrich 未回填)时阈值比较 TypeError → RuleEvalError
    code, responses, _ = rpc({"id": 2, "method": "alerts.test", "params": {"db": str(db), "rule": _alert_rule_payload(
        when="score >= 4",
    ), "item": {"title": "无分数条目", "url": "https://example.com/n"}}})
    result = responses[0]["result"]
    assert result["matched"] is False and result["muted"] is False
    assert result["eval_error"]


def test_alerts_test_push_channel_resolution(tmp_path, monkeypatch):
    """test push 动作展开:通道解析 = 当前品类 push[] 内该类型第一条
    (resolved + resolved_target);品类未配该类型 / 条目无品类 → 降级原因."""
    plugins = _editor_plugins(tmp_path, monkeypatch, ("demo.yaml", VALID_YAML))
    db = tmp_path / "push-resolve.db"
    SQLiteStore(str(db)).close()
    # 品类 proto-demo 的 YAML 配了 stdout 通道 → resolved
    code, responses, _ = rpc({"id": 1, "method": "alerts.test", "params": {"db": str(db), "rule": _alert_rule_payload(
        action="push", when="'a' in title",
    ), "item": {"title": "abc", "category": "proto-demo"}}})
    action = responses[0]["result"]["actions"][0]
    assert action["action"] == "push" and action["channel"] == "stdout"
    assert action["resolved"] is True
    # 品类配了 push 但无该类型(telegram)→ category_push_missing
    code, responses, _ = rpc({"id": 2, "method": "alerts.test", "params": {"db": str(db), "rule": _alert_rule_payload(
        action="push", when="'a' in title",
        action_config={"channel": "telegram"},
    ), "item": {"title": "abc", "category": "proto-demo"}}})
    action = responses[0]["result"]["actions"][0]
    assert action["resolved"] is False and action["degrade_reason"] == "category_push_missing"
    # 条目无品类 → item_no_category
    code, responses, _ = rpc({"id": 3, "method": "alerts.test", "params": {"db": str(db), "rule": _alert_rule_payload(
        action="push", when="'a' in title",
    ), "item": {"title": "abc"}}})
    action = responses[0]["result"]["actions"][0]
    assert action["resolved"] is False and action["degrade_reason"] == "item_no_category"


def test_alerts_fired_replayed_after_run_completed(tmp_path, local_api):
    """alerts.fired 事件流(design §4.3 主路线):真 run 子进程落 alert_fired,
    父进程终态收口 list_fired(since=run.started_at) 逐条回放(completed 之前);
    dry run 零落库零回放。"""
    yaml_path = write_yaml(tmp_path, VALID_YAML.replace("{port}", str(local_api)))
    db = tmp_path / "fired.db"
    # 预存规则:tag 动作(零通道依赖),标题含「协议」即命中(两条夹具条目都命中)
    code, responses, _ = rpc({"id": 1, "method": "alerts.save", "params": {"db": str(db), "rules": [
        _alert_rule_payload(name="协议 watcher", when="'协议' in title")]}}
    )
    rule_id = responses[0]["result"]["rules"][0]["id"]

    out = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 2, "method": "run.start",
                                    "params": {"yaml": yaml_path, "db": str(db)}}) + "\n")
    entry.serve(stdin=stdin, stdout=out)
    run_id = json.loads(out.getvalue().splitlines()[0])["result"]["run_id"]
    completed = wait_completed(out, run_id)
    assert completed["exit_code"] == 0 and completed["status"] == "success"

    _, events = split_stream(out)
    fired_events = [event for event in events if event["type"] == "alerts.fired"]
    assert len(fired_events) == 2  # 协议条目一 / 协议条目二
    for event in fired_events:
        assert set(event) == {"type", "rule_id", "rule_name", "item_id", "dedup_key",
                              "title", "action", "action_status", "ts"}
        assert event["rule_id"] == rule_id and event["rule_name"] == "协议 watcher"
        assert event["action"] == "tag" and event["action_status"] == "tagged"
        assert event["item_id"] is not None and event["dedup_key"]
    assert {event["title"] for event in fired_events} == {"协议条目一", "协议条目二"}
    # 回放先于 completed(UI 角标先到,completed 触发的刷新带上新计数)
    completed_index = events.index(completed)
    assert all(events.index(event) < completed_index for event in fired_events)

    # dry run:管线侧零落库(design §6.1-0 最强零告警),终态零回放
    dry_db = tmp_path / "dry.db"
    rpc({"id": 3, "method": "alerts.save",
         "params": {"db": str(dry_db), "rules": [_alert_rule_payload(name="协议 watcher")]}})
    out_dry = io.StringIO()
    stdin = io.StringIO(json.dumps({"id": 4, "method": "run.start",
                                    "params": {"yaml": yaml_path, "dry": True, "db": str(dry_db)}}) + "\n")
    entry.serve(stdin=stdin, stdout=out_dry)
    dry_run_id = json.loads(out_dry.getvalue().splitlines()[0])["result"]["run_id"]
    wait_completed(out_dry, dry_run_id)
    _, dry_events = split_stream(out_dry)
    assert not [event for event in dry_events if event["type"] == "alerts.fired"]
    store = SQLiteStore(str(dry_db))
    assert store.list_fired() == []  # dry 零落库
    store.close()


def test_alerts_fired_replay_only_new_hits_in_window(tmp_path):
    """回放窗口:since=run.started_at 只回放本 run 新命中,历史命中零重放
    (崩窗/重跑防线是 UNIQUE 占坑,事件面不重复消费)."""
    from datetime import datetime, timedelta, timezone

    from myssia.store.models import AlertFired

    db = tmp_path / "window.db"
    store = SQLiteStore(str(db))
    started = datetime.now(timezone.utc)
    store.record_fired(AlertFired(rule_id=1, rule_name="新命中", dedup_key="new",
                                  title="t", action="tag", action_status="tagged"))
    store.record_fired(AlertFired(rule_id=1, rule_name="历史命中", dedup_key="old",
                                  title="t", action="tag", action_status="tagged",
                                  created_at=started - timedelta(hours=1)))
    store.close()
    out = io.StringIO()
    entry._OUT = out
    try:
        count = entry._replay_alerts_fired(7, str(db), started.isoformat())
    finally:
        entry._OUT = io.StringIO()
    assert count == 1
    event = json.loads(out.getvalue().splitlines()[0])
    assert event["type"] == "alerts.fired" and event["dedup_key"] == "new"


# ---------------------------------------------------------------------------
# gates.get / gates.save(10-05-plugin-market-batch 批二第 11 步;能力实现
# src/myssia/gates.py `GatesConfig`,处理器 entry.py `_m_gates_get`/
# `_m_gates_save`;契约 = 任务档 design.md §6.7 + 处理器实况——get 应答
# {config, path, exists, error}:坏文件 fail-closed 不 fail fast,全关态 +
# 拒载明细带回,一次合法 save 覆写修复;save 同门校验失败
# `gates_config_invalid` 零落盘,tmp+rename 原子写)
# ---------------------------------------------------------------------------

GATES_CONFIG_OK = {
    "version": 1,
    "paid_engines": True,
    "third_party_trace": False,
    "saas": {
        "zenrows": {"enabled": True, "api_key": "keychain:myia/saas/zenrows-key"},
        "scraperapi": {"enabled": False, "api_key": "keychain:myia/saas/scraperapi-key"},
    },
    "platforms": {
        "crawlab": {"enabled": False, "endpoint": "https://crawlab.example.com",
                    "token": "keychain:myia/platforms/crawlab-token"},
        "worldmonitor": {"enabled": False, "endpoint": "", "token": None},
    },
    "analysis": {},
}


def test_gates_get_missing_file_is_all_off(tmp_path, monkeypatch):
    """get:文件不存在 = 全关默认态(fail-closed 合法未配置),exists=False 零 error。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    code, responses, _ = rpc({"id": 1, "method": "gates.get", "params": {}})
    assert code == 0
    result = responses[0]["result"]
    assert result["path"] == str(tmp_path / "home" / "gates.yaml")
    assert result["exists"] is False
    assert result["error"] is None
    assert result["config"] == {
        "version": 1, "paid_engines": False, "third_party_trace": False,
        "saas": {}, "platforms": {}, "analysis": {},
    }


def test_gates_save_and_get_roundtrip(tmp_path, monkeypatch):
    """save→get 往返:keychain 引用原样落盘/回显,凭据永不回值。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    code, responses, _ = rpc({"id": 1, "method": "gates.save",
                              "params": {"config": GATES_CONFIG_OK}})
    assert responses[0]["result"] == {"ok": True, "path": str(tmp_path / "home" / "gates.yaml")}
    text = (tmp_path / "home" / "gates.yaml").read_text(encoding="utf-8")
    assert "keychain:myia/saas/zenrows-key" in text
    assert "keychain:myia/platforms/crawlab-token" in text

    code, responses, _ = rpc({"id": 2, "method": "gates.get", "params": {}})
    result = responses[0]["result"]
    assert result["exists"] is True
    assert result["error"] is None
    assert result["config"]["paid_engines"] is True
    assert result["config"]["saas"]["zenrows"] == {"enabled": True, "api_key": "keychain:myia/saas/zenrows-key"}
    assert result["config"]["platforms"]["crawlab"]["endpoint"] == "https://crawlab.example.com"
    assert result["config"]["platforms"]["worldmonitor"]["token"] is None


def test_gates_save_plaintext_and_unknown_field_rejected_zero_write(tmp_path, monkeypatch):
    """save:明文凭据/未知顶层字段 = gates_config_invalid(结构化明细)零落盘。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    plaintext = {
        **GATES_CONFIG_OK,
        "saas": {"zenrows": {"enabled": True, "api_key": "sk-plaintext"},
                 "scraperapi": GATES_CONFIG_OK["saas"]["scraperapi"]},
    }
    code, responses, _ = rpc({"id": 1, "method": "gates.save", "params": {"config": plaintext}})
    error = responses[0]["error"]
    assert error["code"] == "gates_config_invalid"
    assert error["data"]["errors"][0]["error_type"] == "credential_plaintext"
    assert not (tmp_path / "home" / "gates.yaml").exists()  # 拒载 = 零写入

    unknown = {**GATES_CONFIG_OK, "paid_engine": True}  # 手滑字段名不会静默失效
    code, responses, _ = rpc({"id": 2, "method": "gates.save", "params": {"config": unknown}})
    error = responses[0]["error"]
    assert error["code"] == "gates_config_invalid"
    assert error["data"]["errors"][0]["error_type"] == "unknown_field"
    assert not (tmp_path / "home" / "gates.yaml").exists()


def test_gates_save_missing_config_invalid_params(tmp_path, monkeypatch):
    """save:缺 config 对象 = invalid_params(参数形状,非业务校验)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    code, responses, _ = rpc({"id": 1, "method": "gates.save", "params": {}})
    assert responses[0]["error"]["code"] == "invalid_params"
    assert not (tmp_path / "home" / "gates.yaml").exists()


def test_gates_get_broken_file_fail_closed_then_save_repairs(tmp_path, monkeypatch):
    """get:坏文件不 fail fast——全关态 + exists=True + 拒载明细;合法 save 覆写修复。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    home = tmp_path / "home"
    home.mkdir(parents=True)
    (home / "gates.yaml").write_text(
        "version: 1\npaid_engines: true\noops_field: 1\n", encoding="utf-8")

    code, responses, _ = rpc({"id": 1, "method": "gates.get", "params": {}})
    result = responses[0]["result"]
    assert result["exists"] is True
    assert result["error"] is not None
    assert result["error"]["errors"][0]["error_type"] == "unknown_field"
    # fail-closed:拒载 = 全关默认态(paid_engines 不透传内存里的 true)
    assert result["config"]["paid_engines"] is False
    assert result["config"]["saas"] == {}

    # 一次合法 save 覆写修复(设置屏 = 修复入口)
    code, responses, _ = rpc({"id": 2, "method": "gates.save", "params": {"config": GATES_CONFIG_OK}})
    assert responses[0]["result"]["ok"] is True
    code, responses, _ = rpc({"id": 3, "method": "gates.get", "params": {}})
    result = responses[0]["result"]
    assert result["error"] is None
    assert result["config"]["saas"]["zenrows"]["enabled"] is True
