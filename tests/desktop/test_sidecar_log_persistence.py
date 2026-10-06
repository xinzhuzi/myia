"""统一日志 sidecar 集成测试(10-07-unified-logging 批1;implement.md 1.6)。

锚点按任务档测试矩阵:AC0 ``test_entrypoints_same_handlers``(四入口
handler 集形状一致)/ AC1 落盘保真(serve 集成路径)/ AC2
``test_run_logs_survive_restart``(run_id 落盘 + 新 serve 实例回填可读)/
AC3 ``test_cli_embedded_single_copy`` · ``test_bare_print_still_streamed`` ·
``test_handlers_after_cli_call``(内嵌 CLI 窗口三向)/ AC6
``test_backfill_budget_and_seq`` · ``test_backfill_no_files_noop``(serve
启动回填)/ 决议② ``test_cli_bare_repo_stderr_only`` ·
``test_cli_home_env_writes_file``。

隔离纪律沿批0 tests/test_log.py(design §1.2):root handlers +
LogRecordFactory 快照恢复;数据根一律 tmp_path + MYIA_HOME 沙箱,零真实
数据根触碰。vision 子进程泵(proc=vision 行落盘)在
tests/vision/test_vision_models_server.py 的 spawn 桩用例覆盖,此处不重。
"""

from __future__ import annotations

import importlib.util
import io
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from myssia import log as myssia_log
from myssia.cli import _configure_logging as cli_configure_logging

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRY_PATH = REPO_ROOT / "desktop" / "entry.py"

_spec = importlib.util.spec_from_file_location("desktop_entry_logtest", ENTRY_PATH)
entry = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(entry)


@pytest.fixture(autouse=True)
def _isolated_unified_logging(monkeypatch):
    """统一日志模块态隔离(root handlers + 工厂快照;批0 同款纪律)。"""
    saved_handlers = logging.getLogger().handlers[:]
    saved_factory = logging.getLogRecordFactory()
    myssia_log._reset_module_state()
    monkeypatch.delenv("MYIA_HOME", raising=False)
    yield
    myssia_log._reset_module_state()
    logging.getLogger().handlers[:] = saved_handlers
    logging.setLogRecordFactory(saved_factory)


def _handler_shapes() -> list[tuple[str, int | None, str | None]]:
    """本模块 handler 形状(类名/级别/格式串)——AC0 形状断言面。

    只看统一模块挂的(tagged;pytest 的 logging 插件自有 handler 不入面)。"""
    return [
        (
            type(h).__name__,
            getattr(h, "level", None),
            h.formatter._fmt if h.formatter is not None else None,
        )
        for h in logging.getLogger().handlers
        if getattr(h, "_myssia_unified_log", False)
    ]


def _file_handler_logs_dir() -> Path | None:
    for h in logging.getLogger().handlers:
        if getattr(h, "_myssia_unified_log", False) and type(h).__name__ == "JsonlFileHandler":
            return Path(h._logs_dir)
    return None


def rpc(*requests: dict) -> tuple[int, list[dict]]:
    """一轮 serve:写请求 → 读应答(事件面本文件不用,拆掉)。"""
    stdin = io.StringIO("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in requests))
    out = io.StringIO()
    code = entry.serve(stdin=stdin, stdout=out)
    responses = [json.loads(line) for line in out.getvalue().splitlines() if "id" in json.loads(line)]
    return code, responses


def _today_log_file(home: Path) -> Path:
    return home / "logs" / f"myssia-{datetime.now():%Y%m%d}.jsonl"


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


# ---------------------------------------------------------------------------
# AC0:四入口 handler 集形状一致
# ---------------------------------------------------------------------------


class TestEntrypointsSameHandlers:
    def test_entrypoints_same_handlers(self, tmp_path, monkeypatch):
        """cli(=cron 独立进程入口,批1 零代码同函数)/ sidecar serve / vision
        三入口经统一模块配置后:handler 形状序列一致(cli 与 serve 全等,
        vision 为去 RingHandler 的子序列——design §2 ring 只挂 serve);
        文件 handler 的落盘目录同为 ``<home>/logs``。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))

        cli_configure_logging(as_json=True)
        cli_shapes = _handler_shapes()
        cli_logs_dir = _file_handler_logs_dir()
        assert cli_shapes == [
            ("JsonlFileHandler", 0, None),
            ("RingHandler", 0, None),
            ("StreamHandler", logging.WARNING, "%(asctime)s %(levelname)s %(name)s: %(message)s"),
        ]
        assert cli_logs_dir == home / "logs"

        myssia_log._reset_module_state()
        entry._configure_serve_logging()  # sidecar serve 启动路径(serve() 内同参)
        serve_shapes = _handler_shapes()
        assert serve_shapes == cli_shapes  # 形状一致(AC0);级别按 mode 分级在设计内
        assert _file_handler_logs_dir() == home / "logs"

        myssia_log._reset_module_state()
        # vision 独立形态:vserver._ensure_unified_logging 的自举参数原样
        # (自举行为本身由 tests/vision 的 spawn 桩用例验证)
        myssia_log.configure(mode="serve", data_root=home, ring=False, proc="vision")
        vision_shapes = _handler_shapes()
        assert vision_shapes == [s for s in serve_shapes if s[0] != "RingHandler"]
        assert _file_handler_logs_dir() == home / "logs"

    def test_cli_bare_repo_stderr_only(self, tmp_path, monkeypatch):
        """决议②:MYIA_HOME 未设 → data_root=None 仅 stderr,零文件 handler,
        裸 repo 终端跑不建 logs/(games jobs.json 同源坑防线)。"""
        monkeypatch.chdir(tmp_path)
        cli_configure_logging(as_json=False)
        assert myssia_log._STATE.data_root is None
        assert _file_handler_logs_dir() is None
        # human 模式 stderr 门 = INFO(行为对齐旧 basicConfig)
        stream = [h for h in logging.getLogger().handlers if type(h).__name__ == "StreamHandler"]
        assert len(stream) == 1 and stream[0].level == logging.INFO
        logging.getLogger("myssia.demo").info("terminal-visible")
        assert not (tmp_path / "logs").exists()

    def test_cli_home_env_writes_file(self, tmp_path, monkeypatch):
        """决议②正路:MYIA_HOME 设 → <MYIA_HOME>/logs 落盘。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))
        cli_configure_logging(as_json=True)
        logging.getLogger("myssia.demo").warning("cli-home-line")
        log_file = _today_log_file(home)
        assert log_file.exists()
        rows = _read_jsonl(log_file)
        assert any(r["line"] == "cli-home-line" and r["proc"] == "cli" for r in rows)
        assert all("seq" not in r for r in rows)  # 文件行不落 seq(grill 勘误)


# ---------------------------------------------------------------------------
# AC1 / AC2:落盘保真 + run 日志跨重启
# ---------------------------------------------------------------------------


class TestRunLogsPersistence:
    def test_run_logs_survive_restart(self, tmp_path, monkeypatch):
        """AC2:run 跑次行(run_id 保留)落 ``<home>/logs/myssia-*.jsonl``,
        全新 serve 实例启动回填后 ``logs.tail?run_id=`` 仍可读。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))
        code, responses = rpc({"id": 1, "method": "version"})
        assert code == 0 and responses[0]["result"]["name"]
        # run 子进程行(pump 的核心通路;proc=sidecar 为本进程缺省)
        entry_a = myssia_log.stream_line(7, "stdout", "采集开始 demo")
        entry_b = myssia_log.stream_line(7, "stderr", "运行结束 status=success")
        assert entry_a["run_id"] == 7 and entry_a["proc"] == "sidecar"

        log_file = _today_log_file(home)
        rows = _read_jsonl(log_file)
        persisted = [r for r in rows if r.get("run_id") == 7]
        assert {r["line"] for r in persisted} == {"采集开始 demo", "运行结束 status=success"}
        for r in persisted:  # AC1 字段保真:ts/run_id/stream/line/proc 与条目一致
            assert set(r) == {"ts", "run_id", "stream", "line", "proc"}
        # AC2 后半:全新 serve 实例(backfill 从盘尾拉回)+ 协议过滤零变化
        code2, responses2 = rpc(
            {"id": 2, "method": "logs.tail", "params": {"run_id": 7, "lines": 50}}
        )
        result = responses2[0]["result"]
        assert set(result) == {"lines", "total", "truncated"}
        assert result["total"] == 2 and result["truncated"] is False
        assert [e["line"] for e in result["lines"]] == ["采集开始 demo", "运行结束 status=success"]
        assert [e["seq"] for e in result["lines"]] == sorted(e["seq"] for e in result["lines"])


# ---------------------------------------------------------------------------
# AC3:内嵌 CLI 窗口三向(恰一份 / 裸 print 仍入流 / 窗口后 handler 完整)
# ---------------------------------------------------------------------------


class TestCliEmbeddedWindow:
    def _fake_cli_main(self, monkeypatch, *, emit_logging: bool) -> None:
        """假 cli_main:logging 行(CLI 诊断)+ 可选裸 print;返回 0 退出码。"""
        import sys

        def fake_cli_main(argv):
            if emit_logging:
                logging.getLogger("myssia.demo").warning("cli-log-line")
            print("bare-diagnostic", file=sys.stderr)
            return 0

        monkeypatch.setattr(entry, "cli_main", fake_cli_main)

    def test_cli_embedded_single_copy(self, tmp_path, monkeypatch):
        """AC3 ①:同一 CLI logging 行 ring 中恰一份(ring handler 直入 +
        窗口 suspend 防被捕获 err 二次入流)。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))
        entry._configure_serve_logging()
        self._fake_cli_main(monkeypatch, emit_logging=True)
        code, _payload = entry._cli_json(["list", "--json"])
        assert code == 0
        ring = myssia_log.ring_snapshot()
        assert sum(1 for e in ring if e["line"] == "cli-log-line") == 1

    def test_bare_print_still_streamed(self, tmp_path, monkeypatch):
        """AC3 ②:裸 print(非 logging 输出)仍沿旧路入流(ring+盘),
        「CLI 诊断可见」语义不丢。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))
        entry._configure_serve_logging()
        self._fake_cli_main(monkeypatch, emit_logging=False)
        code, _payload = entry._cli_json(["list", "--json"])
        assert code == 0
        ring = myssia_log.ring_snapshot()
        bare = [e for e in ring if e["line"] == "bare-diagnostic"]
        assert len(bare) == 1 and bare[0]["proc"] == "sidecar"
        rows = _read_jsonl(_today_log_file(home))
        assert any(r["line"] == "bare-diagnostic" for r in rows)

    def test_handlers_after_cli_call(self, tmp_path, monkeypatch):
        """AC3 ③:窗口后 handler 集完整——serve 形态(file+ring+stderr
        WARNING)原样恢复,proc 回 sidecar(force 互踩不再可能,R4)。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))
        entry._configure_serve_logging()
        before = _handler_shapes()
        self._fake_cli_main(monkeypatch, emit_logging=True)
        entry._cli_json(["list", "--json"])
        assert _handler_shapes() == before
        assert myssia_log._STATE.proc == "sidecar"
        # serve 门收回 WARNING:窗口后的模块 INFO 行不上进程 stderr
        stream = [h for h in logging.getLogger().handlers if type(h).__name__ == "StreamHandler"]
        assert len(stream) == 1 and stream[0].level == logging.WARNING
        # 后续 sidecar 行 proc 标注回正(不残留 cli)
        entry_c = myssia_log.stream_line(None, "stderr", "after-window-sidecar")
        assert entry_c["proc"] == "sidecar"


# ---------------------------------------------------------------------------
# AC6:serve 启动冷回填(集成路径;模块级细节批0 已钉)
# ---------------------------------------------------------------------------


class TestServeBackfill:
    def test_backfill_budget_and_seq(self, tmp_path, monkeypatch):
        """预算内回填:2500 行存量 → prev-* 恰回预算 2000 条(头 500 截掉)、
        盘尾对齐、seq 按读入顺序重发单调;回填后新行 seq 续接;ring 帽不破。

        serve 启动路径自身的留痕行(cron ticker/telegram,旧形态同入 ring)
        追加在回填行之后——总数 = 预算 + 启动留痕,断言面用 prev-* 行钉。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))
        log_file = _today_log_file(home)
        log_file.parent.mkdir(parents=True)
        total = myssia_log.BACKFILL_BUDGET + 500
        with log_file.open("w", encoding="utf-8") as fh:
            for i in range(total):
                fh.write(json.dumps({
                    "ts": f"2026-10-07T00:00:00.{i:03d}+00:00",
                    "run_id": None,
                    "stream": "stderr",
                    "line": f"prev-{i}",
                    "proc": "sidecar",
                }, ensure_ascii=False) + "\n")
        code, _ = rpc({"id": 1, "method": "version"})
        assert code == 0
        ring = myssia_log.ring_snapshot()
        prev_lines = [e["line"] for e in ring if e["line"].startswith("prev-")]
        assert len(prev_lines) == myssia_log.BACKFILL_BUDGET  # 头 500 被预算截掉
        assert prev_lines[0] == f"prev-{total - myssia_log.BACKFILL_BUDGET}"
        assert prev_lines[-1] == f"prev-{total - 1}"  # 盘尾对齐
        assert myssia_log.BACKFILL_BUDGET < len(ring) <= myssia_log.CAPACITY  # 帽不破
        seqs = [e["seq"] for e in ring]
        assert seqs == sorted(seqs) and len(set(seqs)) == len(seqs)  # 重发单调且唯一
        fresh = myssia_log.stream_line(None, "stderr", "fresh-after-backfill")
        assert fresh["seq"] > max(seqs)  # 当期流 seq 续接
        assert any(e["line"] == "fresh-after-backfill" for e in myssia_log.ring_snapshot())

    def test_backfill_no_files_noop(self, tmp_path, monkeypatch):
        """无文件/无目录:serve 照常起、logs.tail 协议形状自洽、ring 里只有
        本程启动留痕(cron/telegram,旧行为同入)——无回填行,零回归。"""
        home = tmp_path / "home"
        monkeypatch.setenv("MYIA_HOME", str(home))
        code, responses = rpc(
            {"id": 1, "method": "logs.tail", "params": {"lines": 10}}
        )
        assert code == 0
        result = responses[0]["result"]
        assert set(result) == {"lines", "total", "truncated"}
        assert result["total"] == len(result["lines"]) and result["truncated"] is False
        assert all(
            e["proc"] == "sidecar" and not e["line"].startswith("prev-")
            for e in result["lines"]
        )
