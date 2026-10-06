"""Tests for 统一日志模块 myssia.log(10-07-unified-logging 批0)。

锚点按 implement.md 测试矩阵:AC0 ``test_configure_idempotent`` / AC1
``test_jsonl_fidelity``・``test_daily_rollover``・``test_multiprocess_append``
/ AC5 ``test_purge_stale``・``test_purge_neighbors_untouched`` / AC6
``test_backfill_budget_and_seq``・``test_backfill_no_files_noop`` / AC7
``test_degraded_readonly_root``,另覆盖 0.2 清单的 seq 单调/环形帽/凭据
负断言与 suspend/resume、超长截断。

测试隔离守 design §1.2 纪律(:func:`isolated` 夹具):保存/恢复 root
handlers、loggerDict、LogRecordFactory;日期函数经 monkeypatch 注入跨天;
数据根一律 ``tmp_path``,零真实数据根触碰。
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import pytest

from myssia import log as myssia_log
from myssia.log import (
    BACKFILL_BUDGET,
    CAPACITY,
    backfill,
    configure,
    resume_stderr,
    ring_snapshot,
    stream_line,
    suspend_stderr,
)

SRC = Path(__file__).resolve().parents[1] / "src"

#: 降级提示的过滤锚(比「降级」更精确,不误中含「降级」字样的数据行)。
NOTICE_MARK = "日志落盘已降级"


# ---------------------------------------------------------------------------
# 夹具:design §1.2 测试隔离
# ---------------------------------------------------------------------------


@pytest.fixture()
def isolated():
    """保存/恢复 root handlers+级别、loggerDict 增量、LogRecordFactory。

    进出各做一次模块态复位(:func:`myssia_log._reset_module_state` 摘本模块
    handler、卸工厂、清环形),保证用例间零共享状态。
    """
    root = logging.getLogger()
    saved_handlers = root.handlers[:]
    saved_level = root.level
    saved_factory = logging.getLogRecordFactory()
    saved_loggerdict = dict(logging.Logger.manager.loggerDict)
    myssia_log._reset_module_state()
    yield
    myssia_log._reset_module_state()
    root.handlers[:] = saved_handlers
    root.setLevel(saved_level)
    logging.setLogRecordFactory(saved_factory)
    for name in list(logging.Logger.manager.loggerDict):
        if name not in saved_loggerdict:
            del logging.Logger.manager.loggerDict[name]


def _tagged() -> list[logging.Handler]:
    """本模块挂的 handler(configure 打的标记为锚)。"""
    return [
        h
        for h in logging.getLogger().handlers
        if getattr(h, myssia_log._HANDLER_TAG, False)
    ]


def _tagged_shapes() -> list[tuple[str, int]]:
    return [(type(h).__name__, h.level) for h in _tagged()]


def _today_file(tmp_path: Path) -> Path:
    return tmp_path / "logs" / f"myssia-{myssia_log._today():%Y%m%d}.jsonl"


# ---------------------------------------------------------------------------
# AC0:configure 幂等(批0 半;四入口形状一致面在批1 tests/desktop/)
# ---------------------------------------------------------------------------


class TestConfigureIdempotent:
    def test_configure_idempotent(self, isolated, tmp_path):
        """双 configure:handler 集不翻倍、形状逐件相同(force 语义模块自持)。"""
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        first = _tagged_shapes()
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        second = _tagged_shapes()
        assert first == second
        assert len(second) == 3  # file + ring + stderr 恰三件
        assert sorted(second) == sorted(
            [("JsonlFileHandler", 0), ("RingHandler", 0), ("StreamHandler", logging.WARNING)]
        )

    def test_configure_reconfigure_keeps_ring(self, isolated, tmp_path):
        """进程内重配不清环形(R4 互踩根治的模块语义:CLI 窗口后行仍在)。"""
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        stream_line(7, "stdout", "before-reconfigure")
        configure(mode="human", data_root=tmp_path, ring=False, proc="cli")
        assert [e["line"] for e in ring_snapshot()] == ["before-reconfigure"]

    @pytest.mark.parametrize(
        ("mode", "expected"),
        [("human", logging.INFO), ("json", logging.WARNING), ("serve", logging.WARNING)],
    )
    def test_configure_stderr_mode_levels(self, isolated, tmp_path, mode, expected):
        """stderr 分级:human=INFO / json·serve=WARNING(design §1)。"""
        configure(mode=mode, data_root=tmp_path)
        stderr = [h for h in _tagged() if isinstance(h, logging.StreamHandler)]
        assert len(stderr) == 1
        assert stderr[0].level == expected

    def test_configure_without_data_root_is_stderr_only(self, isolated, tmp_path):
        """决议②:data_root=None 仅 stderr,不建 logs/ 目录。"""
        configure(mode="human", data_root=None)
        assert [t for t, _ in _tagged_shapes()] == ["StreamHandler"]
        assert not (tmp_path / "logs").exists()
        stream_line(None, "stdout", "stderr-only")
        assert not _today_file(tmp_path).exists()


# ---------------------------------------------------------------------------
# seq 单调 / 环形帽
# ---------------------------------------------------------------------------


class TestSeqAndRing:
    def test_seq_monotonic_across_stream_and_module_logs(self, isolated, tmp_path):
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        stream_line(1, "stdout", "stream-a")
        logging.getLogger("myssia.demo").warning("module-w1")
        stream_line(1, "stdout", "stream-b")
        entries = ring_snapshot()
        seqs = [e["seq"] for e in entries]
        assert len(entries) == 3
        assert all(later > earlier for earlier, later in zip(seqs, seqs[1:]))  # 严格单调
        assert all(e["seq"] >= 1 for e in entries)
        # 模块自身日志缺省口径:run_id=None / stream=stderr / proc=本进程
        module_entry = entries[1]
        assert module_entry["run_id"] is None
        assert module_entry["stream"] == "stderr"
        assert module_entry["proc"] == "sidecar"
        assert module_entry["line"] == "module-w1"

    def test_ring_capacity_cap(self, isolated, tmp_path):
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        total = CAPACITY + 25
        for i in range(total):
            stream_line(None, "stdout", f"line-{i}")
        entries = ring_snapshot()
        assert len(entries) == CAPACITY  # 帽不破
        assert entries[0]["line"] == "line-25"  # 最旧逐出
        assert entries[-1]["line"] == f"line-{total - 1}"

    def test_ring_snapshot_run_id_filter_and_lines(self, isolated, tmp_path):
        """快照语义沿 _m_logs_tail:run_id 过滤 + 尾部截取。"""
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        stream_line(1, "stdout", "run-1-a")
        stream_line(2, "stdout", "run-2-a")
        stream_line(1, "stdout", "run-1-b")
        assert [e["line"] for e in ring_snapshot(run_id=1)] == ["run-1-a", "run-1-b"]
        assert [e["line"] for e in ring_snapshot(lines=2)] == ["run-2-a", "run-1-b"]
        assert ring_snapshot(lines=0) == []


# ---------------------------------------------------------------------------
# AC1:JSONL 保真 / 跨天轮转 / 多进程并发 append
# ---------------------------------------------------------------------------


class TestJsonlPersistence:
    def test_jsonl_fidelity(self, isolated, tmp_path):
        """文件行字段保真(ts/run_id/stream/line/proc)且**不含 seq**;
        ring 条目 = 文件行 + seq(同 ts/line,逐条对齐)。"""
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        stream_line(42, "stdout", "子进程输出一行")
        stream_line(None, "stderr", "CLI WARNING 行")
        logging.getLogger("myssia.pipeline").warning("模块告警 %s", "demo")
        path = _today_file(tmp_path)
        assert path.exists()
        rows = [json.loads(r) for r in path.read_text(encoding="utf-8").splitlines()]
        assert len(rows) == 3
        for row in rows:
            assert set(row) == {"ts", "run_id", "stream", "line", "proc"}  # 无 seq
            assert row["proc"] == "sidecar"
        assert (rows[0]["run_id"], rows[0]["stream"], rows[0]["line"]) == (
            42,
            "stdout",
            "子进程输出一行",
        )
        assert (rows[1]["run_id"], rows[1]["stream"]) == (None, "stderr")
        assert rows[2]["line"] == "模块告警 demo"
        entries = ring_snapshot()
        assert len(entries) == 3
        for entry, row in zip(entries, rows):
            assert entry["seq"] >= 1
            assert {k: v for k, v in entry.items() if k != "seq"} == row

    def test_daily_rollover(self, isolated, tmp_path, monkeypatch):
        """本地日切换换文件(注入日期;无 rename 的轮转形态)。"""
        monkeypatch.setattr(myssia_log, "_today", lambda: date(2026, 10, 6))
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        stream_line(1, "stdout", "day-one-line")
        monkeypatch.setattr(myssia_log, "_today", lambda: date(2026, 10, 7))
        stream_line(1, "stdout", "day-two-line")
        logs = tmp_path / "logs"
        assert sorted(p.name for p in logs.glob("*.jsonl")) == [
            "myssia-20261006.jsonl",
            "myssia-20261007.jsonl",
        ]
        first = [json.loads(r) for r in (logs / "myssia-20261006.jsonl").read_text().splitlines()]
        second = [json.loads(r) for r in (logs / "myssia-20261007.jsonl").read_text().splitlines()]
        assert [r["line"] for r in first] == ["day-one-line"]
        assert [r["line"] for r in second] == ["day-two-line"]

    def test_multiprocess_append(self, isolated, tmp_path):
        """多进程并发 append 同一当日文件:零丢行、零坏行(互踢场景模拟)。

        每子进程独立 configure(独立 seq 计数器,故文件行本就不落 seq)。
        """
        script = "\n".join(
            [
                "import sys",
                "from pathlib import Path",
                "from myssia.log import configure, stream_line",
                "data_root, worker, count = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])",
                'configure(mode="serve", data_root=data_root, ring=False, proc=f"cli-{worker}")',
                'for i in range(count):',
                '    stream_line(None, "stdout", f"{worker}-{i}")',
            ]
        )
        env = {**os.environ, "PYTHONPATH": str(SRC)}
        workers, per_worker = 4, 40
        procs = [
            subprocess.Popen(
                [sys.executable, "-c", script, str(tmp_path), f"w{k}", str(per_worker)],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for k in range(workers)
        ]
        for proc in procs:
            out, err = proc.communicate(timeout=60)
            assert proc.returncode == 0, f"子进程失败:{err or out}"
        rows = [json.loads(r) for r in _today_file(tmp_path).read_text(encoding="utf-8").splitlines()]
        assert len(rows) == workers * per_worker  # 零丢行
        counts = Counter(row["proc"] for row in rows)
        assert set(counts.values()) == {per_worker}
        assert counts.keys() == {f"cli-w{k}" for k in range(workers)}
        for row in rows:  # 零坏行:逐行可解析已在 read 时保证
            assert set(row) == {"ts", "run_id", "stream", "line", "proc"}

    def test_long_line_truncated_to_cap(self, isolated, tmp_path):
        """超 64KB 行按字节截断保单次 write 原子上限;ring 与文件同款。"""
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        entry = stream_line(None, "stdout", "长" * 40000)  # 120KB utf-8
        assert len(entry["line"].encode("utf-8")) <= myssia_log._MAX_LINE_BYTES + 64
        assert entry["line"].endswith("…[超长截断]")
        row = json.loads(_today_file(tmp_path).read_text(encoding="utf-8").splitlines()[-1])
        assert row["line"] == entry["line"]

    def test_no_credential_values_in_outputs(self, isolated, tmp_path, monkeypatch):
        """凭据红线负断言:env 值样张不出现(引用名可留,展开值禁止)。"""
        secret_name = "MYIA_LOG_TEST_SECRET"
        secret_value = "super-secret-value-do-not-log"
        monkeypatch.setenv(secret_name, secret_value)
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        stream_line(1, "stdout", f"使用凭据 env:{secret_name}(引用不展开)")
        logging.getLogger("myssia.push").warning("push target=env:%s", secret_name)
        file_text = _today_file(tmp_path).read_text(encoding="utf-8")
        assert secret_value not in file_text
        assert secret_value not in json.dumps(ring_snapshot(), ensure_ascii=False)
        assert f"env:{secret_name}" in file_text  # 名字可见(引用不算凭据值)


# ---------------------------------------------------------------------------
# AC5:保留清理 + 邻居负断言
# ---------------------------------------------------------------------------


class TestRetentionPurge:
    def test_purge_stale(self, isolated, tmp_path, monkeypatch):
        """cutoff=今天−7 天:此前删除、此后(含边界)保留。"""
        monkeypatch.setattr(myssia_log, "_today", lambda: date(2026, 10, 7))
        logs = tmp_path / "logs"
        logs.mkdir(parents=True)
        stale = logs / "myssia-20260929.jsonl"
        boundary = logs / "myssia-20260930.jsonl"  # == cutoff:保留
        fresh1 = logs / "myssia-20261001.jsonl"
        fresh2 = logs / "myssia-20261007.jsonl"
        for path in (stale, boundary, fresh1, fresh2):
            path.write_text("{}\n", encoding="utf-8")
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        assert not stale.exists()
        assert boundary.exists()
        assert fresh1.exists()
        assert fresh2.exists()

    def test_purge_neighbors_untouched(self, isolated, tmp_path, monkeypatch):
        """红线:前缀 glob 钉死,名形不合/壳归档/cron 产物/旧 vision-server.log
        一律不碰(升级场景旧文件留存不删)。"""
        monkeypatch.setattr(myssia_log, "_today", lambda: date(2026, 10, 7))
        logs = tmp_path / "logs"
        logs.mkdir(parents=True)
        stale = logs / "myssia-20260901.jsonl"  # 正门:超期删除
        garbage = logs / "myssia-notadate.jsonl"  # 前缀合、日期形不合
        fake_date = logs / "myssia-99999999.jsonl"  # 日期形合、值非法
        shell_archive = logs / "shell_2026-09-01_00-00-00.log"  # 壳归档(自清属壳)
        shell_live = logs / "shell.log"
        old_vision = tmp_path / "vision-server.log"  # 升级场景旧文件(B1:home 顶层)
        cron_output = tmp_path / "cron" / "output" / "demo-job" / "run-1.log"
        cron_output.parent.mkdir(parents=True)
        for path in (stale, garbage, fake_date, shell_archive, shell_live, old_vision, cron_output):
            path.write_text("keep\n", encoding="utf-8")
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        assert not stale.exists()
        for survivor in (garbage, fake_date, shell_archive, shell_live, old_vision, cron_output):
            assert survivor.exists(), f"邻居被误删:{survivor}"
            assert survivor.read_text(encoding="utf-8") == "keep\n"


# ---------------------------------------------------------------------------
# AC6:冷启动回填
# ---------------------------------------------------------------------------


class TestBackfill:
    def test_backfill_budget_and_seq(self, isolated, tmp_path, monkeypatch):
        """预算帽/坏行跳过/时间序/proc 保留/seq 重发单调且续接。"""
        monkeypatch.setattr(myssia_log, "_today", lambda: date(2026, 10, 7))
        logs = tmp_path / "logs"
        logs.mkdir(parents=True)
        rows_yesterday = [
            {
                "ts": "2026-10-06T00:00:00.000+00:00",
                "run_id": None,
                "stream": "stdout",
                "line": f"old-{i}",
                "proc": "cli",
            }
            for i in range(2500)
        ]
        yesterday_lines = [json.dumps(r, ensure_ascii=False) for r in rows_yesterday]
        yesterday_lines.insert(1000, "{broken-mid-line")
        yesterday_lines.append("{broken-crash-tail")  # 崩溃截尾:末行无换行
        (logs / "myssia-20261006.jsonl").write_text(
            "\n".join(yesterday_lines) + "\n", encoding="utf-8"
        )
        rows_today = [
            {
                "ts": "2026-10-07T00:00:00.000+00:00",
                "run_id": 3,
                "stream": "stdout",
                "line": f"today-{i}",
                "proc": "sidecar",
            }
            for i in range(100)
        ]
        (logs / "myssia-20261007.jsonl").write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in rows_today) + "\n",
            encoding="utf-8",
        )
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        seeded = backfill(tmp_path)
        # 预算帽:昨日尾 1900 + 今日 100 = 2000(坏行不占预算)
        assert len(seeded) == BACKFILL_BUDGET
        expected = [r["line"] for r in rows_yesterday[-1900:]] + [
            r["line"] for r in rows_today
        ]
        assert [e["line"] for e in seeded] == expected
        assert seeded[0]["proc"] == "cli"  # proc 保留可辨上一程
        assert seeded[-1]["proc"] == "sidecar"
        # seq 重发单调(文件行无 seq,按读入顺序新发)
        seqs = [e["seq"] for e in seeded]
        assert all(later > earlier for earlier, later in zip(seqs, seqs[1:]))
        assert ring_snapshot() == seeded  # seed 即环形
        # 后续新行 seq 续接单调、帽不破
        entry = stream_line(9, "stdout", "after-backfill")
        assert entry["seq"] > seqs[-1]
        assert len(ring_snapshot()) <= CAPACITY

    def test_backfill_no_files_noop(self, isolated, tmp_path):
        """无文件/无目录/全坏行:零行为、零异常(与现状全同)。"""
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        stream_line(1, "stdout", "live-line")
        before = ring_snapshot()
        empty_root = tmp_path / "empty-root"
        empty_root.mkdir()
        assert backfill(empty_root) == []  # 有根无 logs 目录
        assert backfill(tmp_path / "does-not-exist") == []  # 目录本身不存在
        bad_root = tmp_path / "bad-root"
        (bad_root / "logs").mkdir(parents=True)
        (bad_root / "logs" / "myssia-20261007.jsonl").write_text(
            "{broken\nnot json at all\n", encoding="utf-8"
        )
        assert backfill(bad_root) == []  # 全坏行
        assert ring_snapshot() == before


# ---------------------------------------------------------------------------
# AC7:降级
# ---------------------------------------------------------------------------


class TestDegraded:
    def test_degraded_readonly_root(self, isolated, tmp_path, capfd):
        """数据根不可写(logs 被占位为普通文件):主链不破 + 恰一条提示 + 永久静默。"""
        (tmp_path / "logs").write_text("占位:logs 是普通文件,目录创建必失败", encoding="utf-8")
        configure(mode="serve", data_root=tmp_path, ring=True, proc="sidecar")
        entry = stream_line(5, "stdout", "降级前一行")  # 主链不破:首行不抛
        assert entry["line"] == "降级前一行"

        def notices() -> list[dict]:
            return [e for e in ring_snapshot() if NOTICE_MARK in e["line"]]

        first = notices()
        assert len(first) == 1  # 恰一条提示
        assert first[0]["run_id"] is None
        assert first[0]["stream"] == "stderr"
        assert first[0]["proc"] == "sidecar"
        for i in range(5):  # 永久静默:后续行不再提示、不再抛
            stream_line(5, "stdout", f"后续行-{i}")
        assert len(notices()) == 1
        assert len(ring_snapshot()) == 7  # 1 提示 + 6 数据行,环形照常
        # 文件路确未触碰占位件
        assert (tmp_path / "logs").read_text(encoding="utf-8").startswith("占位")
        # stderr 主链仍在(协议进程可见)
        logging.getLogger("myssia.demo").warning("terminal-visible")
        _, err = capfd.readouterr()
        assert "terminal-visible" in err
        assert NOTICE_MARK not in err  # 提示只进 ring,不刷 stderr


# ---------------------------------------------------------------------------
# suspend / resume stderr(design §3;AC3 窗口三向钉死在批1)
# ---------------------------------------------------------------------------


class TestSuspendResumeStderr:
    def test_suspend_and_resume_stderr(self, isolated, tmp_path, capfd):
        configure(mode="human", data_root=tmp_path, ring=True, proc="sidecar")
        logging.getLogger("myssia.demo").info("before-window")
        _, err = capfd.readouterr()
        assert "before-window" in err
        suspend_stderr()
        logging.getLogger("myssia.demo").info("in-window")
        _, err = capfd.readouterr()
        assert "in-window" not in err
        assert any(e["line"] == "in-window" for e in ring_snapshot())  # ring 仍必得
        resume_stderr()
        logging.getLogger("myssia.demo").info("after-window")
        _, err = capfd.readouterr()
        assert "after-window" in err
        stderr_handlers = [
            h for h in _tagged() if isinstance(h, logging.StreamHandler)
        ]
        assert len(stderr_handlers) == 1  # 窗口后 handler 集完整

    def test_suspend_resume_without_state_are_noops(self, isolated, tmp_path):
        """未挂起时 resume / 已挂起时重复 suspend:幂等 no-op。"""
        configure(mode="serve", data_root=tmp_path)
        resume_stderr()  # 未挂起
        suspend_stderr()
        suspend_stderr()  # 重复挂起
        resume_stderr()
        stderr_handlers = [
            h for h in _tagged() if isinstance(h, logging.StreamHandler)
        ]
        assert len(stderr_handlers) == 1


# ---------------------------------------------------------------------------
# 入口 proc 细分(10-07-logs-restart-visibility R2/R3;AC3 双向钉死)
# ---------------------------------------------------------------------------


class TestEntryProcCronAndFeishu:
    """cron serve="cron" / 普通 CLI="cli" / feishu_callback 统一配置三面。"""

    def test_cron_serve_entry_proc_is_cron(self, isolated, tmp_path, monkeypatch):
        """独立 cron serve 宿主:dispatch 点分流 proc="cron"(serve handler
        入口处捕获——不真起 serve_forever,零阻塞零网络)。"""
        from myssia import cli as myssia_cli

        captured: dict[str, object] = {}

        def fake_serve(args: object) -> int:
            captured["proc"] = myssia_log._STATE.proc
            return 0

        monkeypatch.setattr(myssia_cli, "_cmd_cron_serve", fake_serve)
        code = myssia_cli.main(["cron", "serve", "--db", str(tmp_path / "cron.db")])
        assert code == 0
        assert captured["proc"] == "cron"
        assert myssia_log._STATE.proc == "cron"

    def test_cron_plain_subcommand_proc_stays_cli(self, isolated, tmp_path, monkeypatch):
        """普通 cron 子命令(非 serve):proc 仍 "cli",十个兄弟命令不误标。"""
        from myssia import cli as myssia_cli

        monkeypatch.delenv("MYIA_HOME", raising=False)
        code = myssia_cli.main(["cron", "list", "--db", str(tmp_path / "plain.db")])
        assert code == 0
        assert myssia_log._STATE.proc == "cli"

    def test_configure_logging_default_proc_cli(self, isolated, monkeypatch):
        """_configure_logging 缺省 proc="cli":十二个既有调用点零改动的根据。"""
        from myssia import cli as myssia_cli

        monkeypatch.delenv("MYIA_HOME", raising=False)
        myssia_cli._configure_logging(False)
        assert myssia_log._STATE.proc == "cli"
        assert myssia_log._STATE.mode == "human"

    def test_feishu_callback_configures_unified_logging(self, isolated, tmp_path, monkeypatch):
        """MYIA_HOME 在场:file+stderr 两 handler(ring=False 无 RingHandler)、
        stderr 门 WARNING、INFO 行落盘且 proc="feishu_callback"。

        走公网绑定拒绝(--enable + --host 8.8.8.8)的非阻塞错路:
        构造期 _validate_bind_host 在 main 的 try 内抛、结构化 return 1,
        不起 serve_forever、零网络。
        """
        import myssia.push.feishu_callback as feishu_callback

        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        code = feishu_callback.main(
            ["--enable", "--host", "8.8.8.8", "--db", str(tmp_path / "feishu.db")]
        )
        assert code == 1
        assert sorted(_tagged_shapes()) == sorted(
            [("JsonlFileHandler", 0), ("StreamHandler", logging.WARNING)]
        )
        assert myssia_log._STATE.proc == "feishu_callback"
        logging.getLogger("myssia.feishu.demo").info("feishu 落盘一行")
        path = _today_file(tmp_path)
        assert path.exists()
        rows = [json.loads(r) for r in path.read_text(encoding="utf-8").splitlines()]
        assert rows and all(r["proc"] == "feishu_callback" for r in rows)
        assert any(r["line"] == "feishu 落盘一行" for r in rows)
        assert ring_snapshot() == []  # ring=False:独立服务进程无 UI 数据面

    def test_feishu_callback_bare_run_stderr_only(self, isolated, tmp_path, monkeypatch):
        """裸跑(无 MYIA_HOME):决议②——仅 stderr handler,不在 CWD 建 logs/。"""
        import myssia.push.feishu_callback as feishu_callback

        monkeypatch.delenv("MYIA_HOME", raising=False)
        code = feishu_callback.main(
            ["--enable", "--host", "8.8.8.8", "--db", str(tmp_path / "bare.db")]
        )
        assert code == 1
        assert [t for t, _ in _tagged_shapes()] == ["StreamHandler"]
        assert not (tmp_path / "logs").exists()
        assert myssia_log._STATE.proc == "feishu_callback"
