"""Tests for myssia.cli — exit-code contract, --json/--dry-run/--loop, stubs.

Covers PRD 10-01-v01-cli-basic acceptance criteria:

- ``myssia run <yaml> --dry-run --json`` 输出单份可被 json/jq 解析的结果;
- 配置错误退出码 1,错误信息含字段路径(与 schema 层打通);
- 退出码语义 0/1/2/3 全覆盖(供 agent 与 CI 判断);
- ``--help`` 输出清晰;``list``/``test``/``init`` 等留位子命令结构化提示;
- ``alerts list`` 告警命中历史只读(10-04-alert-rules design §8:
  ``--rule``/``--limit``/``--json``;v1 无写子命令);
- ``cron`` 十一子命令族(10-04-hermes-cron design §4.1,B2):create 的
  Q6 装载校验早失败 / Q5 绝对路径存储 / ``--json`` 单份契约 / list 过滤 /
  estop 急停 / tick 派发(执行体与 serve 同款 CronRunner,离线原则由
  spawn 替身承担——真子进程从不 spawn,零网络) /
  退出码只用 0/1。

Pipeline is replaced by a fake (constructor + run/run_forever recorded) —
the CLI layer is tested in isolation; the real pipeline contract is covered
by tests/test_pipeline.py and the real-process e2e in the task log.
"""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime, timezone
from typing import Any

import pytest

import myssia
import myssia.cli as cli_module
from myssia.cli import EXIT_CONFIG_ERROR, EXIT_OK, EXIT_PARTIAL, build_parser, main
from myssia.pipeline import ChannelPushReport, RunResult, StageReport
from myssia.schema import load_category
from myssia.store import AlertFired, SQLiteStore

VALID_YAML = """
id: demo
name: 演示品类
schedule: "0 9 * * *"
timezone: Asia/Shanghai
sources:
  - name: api
    engine: direct_api
    url: "https://api.demo.local/list"
    extract:
      type: json_path
      fields:
        title: "$[*].title"
        url: "$[*].url"
push:
  - channel: stdout
"""

PLAINTEXT_YAML = """
id: demo
name: 演示品类
schedule: "0 9 * * *"
timezone: Asia/Shanghai
sources:
  - name: api
    engine: direct_api
    url: "https://api.demo.local/list"
    headers:
      Cookie: "sid=123456"
    extract:
      type: json_path
      fields:
        title: "$[*].title"
        url: "$[*].url"
push:
  - channel: stdout
"""


# ---------------------------------------------------------------------------
# Fakes: the CLI layer sees a canned RunResult, no I/O
# ---------------------------------------------------------------------------


def make_result(status: str = "success", **overrides: Any) -> RunResult:
    """A real RunResult dataclass with minimal canned content."""
    fields: dict[str, Any] = {
        "category": "demo",
        "category_name": "演示品类",
        "run_id": 1,
        "started_at": datetime.now(timezone.utc),
        "finished_at": datetime.now(timezone.utc),
        "status": status,
        "stages": [
            StageReport(name=name, status="ok")
            for name in ("fetch", "classify", "dedup", "analyze", "push")
        ],
        "sources": [],
        "items": [],
        "pushes": [ChannelPushReport(channel="stdout")],
    }
    fields.update(overrides)
    return RunResult(**fields)


class FakePipeline:
    """Records constructor/run/run_forever calls; returns a canned result."""

    last_instance: "FakePipeline | None" = None

    def __init__(self, config: Any, **kwargs: Any) -> None:
        self.config = config
        self.kwargs = kwargs
        self.run_calls: list[dict[str, Any]] = []
        self.forever_calls: list[dict[str, Any]] = []
        self.closed = False
        self.result: RunResult = make_result()
        FakePipeline.last_instance = self

    async def run(self, *, dry_run: bool = False) -> RunResult:
        self.run_calls.append({"dry_run": dry_run})
        return replace(self.result, dry_run=dry_run)  # CLI 的开关如实反映到输出

    async def run_forever(self, *, dry_run: bool = False) -> int:
        self.forever_calls.append({"dry_run": dry_run})
        return 3

    def close(self) -> None:
        self.closed = True


@pytest.fixture()
def fake_pipeline(monkeypatch: pytest.MonkeyPatch) -> type[FakePipeline]:
    """Swap the CLI's Pipeline for the fake and hand the config loader a win."""
    config = load_category(
        {
            "id": "demo",
            "name": "演示品类",
            "schedule": "0 9 * * *",
            "timezone": "Asia/Shanghai",
            "sources": [
                {
                    "name": "api",
                    "engine": "direct_api",
                    "url": "https://api.demo.local/list",
                    "extract": {
                        "type": "json_path",
                        "fields": {"title": "$[*]", "url": "$[*]"},
                    },
                }
            ],
            "push": [{"channel": "stdout"}],
        }
    )
    monkeypatch.setattr(cli_module, "load_category_file", lambda path: config)
    monkeypatch.setattr(cli_module, "Pipeline", FakePipeline)
    return FakePipeline


# ---------------------------------------------------------------------------
# Exit code 0: success / dry-run / loop
# ---------------------------------------------------------------------------


def test_run_success_exit_zero_and_json_parseable(fake_pipeline, capsys):
    """--json:单份 JSON,可被 json/jq 解析;成功退出码 0。"""
    code = main(["run", "demo.yaml", "--json"])

    assert code == EXIT_OK
    out = capsys.readouterr().out
    payload = json.loads(out)  # jq 等价:单份 JSON 文档
    assert payload["status"] == "success"
    assert payload["category"] == "demo"
    assert [stage["name"] for stage in payload["stages"]] == [
        "fetch",
        "classify",
        "dedup",
        "analyze",
        "push",
    ]
    instance = fake_pipeline.last_instance
    assert instance is not None and instance.run_calls == [{"dry_run": False}]
    assert instance.closed is True  # 资源已释放


def test_run_human_output_exit_zero(fake_pipeline, capsys):
    """默认人类可读输出;与 --json 同一信息另一种皮。"""
    code = main(["run", "demo.yaml"])

    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "世事 run:" in out
    assert "状态:success" in out
    assert "fetch:ok" in out


def test_run_dry_run_flag_forwarded(fake_pipeline, capsys):
    """--dry-run 透传给 pipeline(全链执行但不推送)。"""
    code = main(["run", "demo.yaml", "--dry-run", "--json"])

    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["dry_run"] is True
    instance = fake_pipeline.last_instance
    assert instance is not None and instance.run_calls == [{"dry_run": True}]


def test_run_loop_calls_run_forever(fake_pipeline, capsys):
    """--loop:常驻调度(run_forever),干净退出码 0。"""
    code = main(["run", "demo.yaml", "--loop"])

    assert code == EXIT_OK
    instance = fake_pipeline.last_instance
    assert instance is not None
    assert instance.forever_calls == [{"dry_run": False}]
    assert instance.run_calls == []


def test_run_keyboard_interrupt_exits_zero(fake_pipeline, capsys):
    """常驻模式 Ctrl-C:干净退出,退出码 0。"""
    instance = fake_pipeline.last_instance

    async def interrupted(*, dry_run: bool = False):
        raise KeyboardInterrupt

    assert instance is not None
    instance.run_forever = interrupted  # type: ignore[method-assign]
    assert main(["run", "demo.yaml", "--loop"]) == EXIT_OK


# ---------------------------------------------------------------------------
# Exit codes 2 / 3: fetch-all-failed / partial
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("status", "expected"),
    [("failed", 2), ("partial", 3)],
)
def test_run_maps_status_to_exit_code(fake_pipeline, capsys, status, expected):
    """failed→2(采集全部失败)、partial→3(部分失败)。"""
    fake_pipeline.last_instance = None
    original = FakePipeline.__init__

    def init_with_status(self, config, **kwargs):
        original(self, config, **kwargs)
        self.result = make_result(status=status)

    fake_pipeline.__init__ = init_with_status  # type: ignore[method-assign]
    try:
        code = main(["run", "demo.yaml", "--json"])
    finally:
        fake_pipeline.__init__ = original  # type: ignore[method-assign]
    assert code == expected
    assert json.loads(capsys.readouterr().out)["status"] == status


def test_exit_code_constants_are_pinned():
    """退出码常量即 CLI 契约,不可漂移。"""
    from myssia.cli import EXIT_FETCH_ALL_FAILED

    assert (EXIT_OK, EXIT_CONFIG_ERROR, EXIT_FETCH_ALL_FAILED, EXIT_PARTIAL) == (
        0,
        1,
        2,
        3,
    )


# ---------------------------------------------------------------------------
# Exit code 1: config errors carry field paths
# ---------------------------------------------------------------------------


def test_config_error_missing_file_exit_one(capsys):
    """文件不存在:退出码 1,结构化 file_not_found。"""
    code = main(["run", "no-such-plugin.yaml", "--json"])

    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"] == "config"
    assert payload["errors"][0]["error_type"] == "file_not_found"


def test_config_error_unknown_field_carries_field_path(tmp_path, capsys):
    """未知字段 fail-fast:错误含字段路径(与 schema 层打通)。"""
    bad = tmp_path / "bad.yaml"
    bad.write_text(VALID_YAML + "\nnope: 未知字段\n", encoding="utf-8")
    code = main(["run", str(bad), "--json"])

    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["errors"][0]["path"] == "$.nope"
    assert payload["errors"][0]["error_type"] == "unknown_field"


def test_config_error_plaintext_credential_exit_one(tmp_path, capsys):
    """明文凭据:退出码 1,字段路径指向具体 header(schema 拒载,零网络)。"""
    bad = tmp_path / "plaintext.yaml"
    bad.write_text(PLAINTEXT_YAML, encoding="utf-8")
    assert "Cookie" in bad.read_text(encoding="utf-8")  # 夹具本身先自检
    code = main(["run", str(bad), "--json"])

    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["errors"][0]["error_type"] == "credential_plaintext"
    assert payload["errors"][0]["path"] == "$.sources[0].headers.Cookie"


def test_config_error_human_output_goes_to_stderr(tmp_path, capsys):
    """人类可读模式:配置错误走 stderr,含字段路径。"""
    bad = tmp_path / "bad.yaml"
    bad.write_text(VALID_YAML + "\nnope: 未知字段\n", encoding="utf-8")
    code = main(["run", str(bad)])

    assert code == EXIT_CONFIG_ERROR
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "$.nope" in captured.err


def test_pipeline_config_error_exit_one(fake_pipeline, capsys, monkeypatch):
    """Pipeline 构造期的配置错误(route 规则等)也归退出码 1。"""
    real_config = load_category(
        {
            "id": "demo",
            "name": "演示品类",
            "schedule": "0 9 * * *",
            "timezone": "Asia/Shanghai",
            "sources": [{"name": "api", "url": "https://api.demo.local/list"}],
        }
    )
    monkeypatch.setattr(cli_module, "load_category_file", lambda path: real_config)

    class BrokenPipeline:
        def __init__(self, config, **kwargs):
            raise ValueError("push[].route 配置非法")

    monkeypatch.setattr(cli_module, "Pipeline", BrokenPipeline)
    code = main(["run", "demo.yaml", "--json"])

    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["errors"][0]["error_type"] == "config_error"
    assert "push[].route" in payload["errors"][0]["message"]


# ---------------------------------------------------------------------------
# Usage errors & help & version
# ---------------------------------------------------------------------------


def test_unknown_command_exits_one(capsys):
    """未知子命令:用法错误归退出码 1(不用 argparse 的 2,避免撞码)。"""
    assert main(["bogus"]) == EXIT_CONFIG_ERROR
    assert "usage" in capsys.readouterr().err


def test_once_and_loop_mutually_exclusive(capsys):
    """--once 与 --loop 互斥:用法错误退出码 1。"""
    assert main(["run", "demo.yaml", "--once", "--loop"]) == EXIT_CONFIG_ERROR


def test_no_command_prints_help_exit_zero(capsys):
    """无子命令:打印帮助,退出码 0。"""
    assert main([]) == EXIT_OK
    assert "usage" in capsys.readouterr().out


def test_version_flag(capsys):
    """--version:打印版本号,退出码 0(SystemExit 传播)。"""
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    # 与 cli.py --version 同源断言(版本序列归零 10-03-tag-release 决议 9 后
    # 不再硬编码版本号,升版免改本测)
    assert f"myssia {myssia.__version__}" in capsys.readouterr().out


def test_help_documents_run_and_exit_codes(capsys):
    """--help 输出清晰:run 子命令与退出码契约可见(文档也是 AI 的输入)。"""
    parser = build_parser()
    help_text = parser.format_help()
    assert "run" in help_text
    assert "--dry-run" in help_text
    assert "--loop" in help_text
    assert "退出码" in help_text


def test_run_help_mentions_flags(capsys):
    """run 子命令的 --help 列出全部开关。"""
    parser = build_parser()
    run_parser = next(
        action
        for action in parser._subparsers._group_actions[0].choices.values()  # type: ignore[union-attr]
        if action.prog.endswith("run")
    )
    help_text = run_parser.format_help()
    for flag in ("--once", "--loop", "--dry-run", "--json", "--db"):
        assert flag in help_text


# ---------------------------------------------------------------------------
# Stub commands(仍留位的子命令;list/test/init/doctor 已在 v0.2 实装,
# 见 test_cli_full.py)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("command", ["add-source", "dashboard"])
def test_stub_commands_not_implemented(command, capsys):
    """留位子命令:结构化 not_implemented 提示,退出码 1。"""
    code = main([command])

    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"] == "not_implemented"
    assert payload["command"] == command
    assert payload["scheduled_version"] == "v0.2"


# ---------------------------------------------------------------------------
# alerts list:告警命中历史只读(v1;design §8 --rule/--limit/--json,无写子命令)
# ---------------------------------------------------------------------------


def _seed_fired_history(db_path) -> None:
    """两条命中历史:rule 1(push,send_failed)先落、rule 2(tag,tagged)后落。

    ``record_fired`` 不要求规则行存在(fired 是事实快照,规则删除后历史照留),
    种子直接按 rule_id 落行,聚焦 CLI 层。
    """
    store = SQLiteStore(str(db_path))
    try:
        store.record_fired(
            AlertFired(
                rule_id=1,
                rule_name="竞对融资",
                dedup_key="https://a.example/1",
                action="push",
                action_status="send_failed",
                item_id=11,
                title="A 公司完成 B 轮融资",
                category="finance",
            )
        )
        store.record_fired(
            AlertFired(
                rule_id=2,
                rule_name="AI 打标",
                dedup_key="https://b.example/2",
                action="tag",
                action_status="tagged",
                item_id=12,
                title="AI 进展",
                category="tech",
            )
        )
    finally:
        store.close()


def test_alerts_list_json_readonly(tmp_path, capsys):
    """--json:单份可解析 JSON,新→旧,快照字段(rule_name/title/action_status)齐全。"""
    db = tmp_path / "alerts.db"
    _seed_fired_history(db)
    code = main(["alerts", "list", "--db", str(db), "--json"])

    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)  # jq 等价:单份 JSON 文档
    assert payload["command"] == "alerts" and payload["action"] == "list"
    assert payload["count"] == 2
    first, second = payload["items"]  # 新→旧:后落的 rule 2 在前
    assert first["rule_id"] == 2 and first["rule_name"] == "AI 打标"
    assert first["action"] == "tag" and first["action_status"] == "tagged"
    assert second["rule_id"] == 1 and second["rule_name"] == "竞对融资"
    assert second["action"] == "push" and second["action_status"] == "send_failed"
    assert second["title"] == "A 公司完成 B 轮融资"
    for item in payload["items"]:
        datetime.fromisoformat(item["created_at"])  # 时间字段 ISO-8601 可解析


def test_alerts_list_rule_filter_and_limit(tmp_path, capsys):
    """--rule 按规则 id 过滤;--limit 截新→旧前 N(钳制 [1,200] 在 store 层)。"""
    db = tmp_path / "alerts.db"
    _seed_fired_history(db)
    code = main(["alerts", "list", "--db", str(db), "--rule", "1", "--json"])

    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["count"] == 1
    assert all(item["rule_id"] == 1 for item in payload["items"])

    code = main(["alerts", "list", "--db", str(db), "--limit", "1", "--json"])
    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["count"] == 1 and payload["items"][0]["rule_id"] == 2  # 取最新


def test_alerts_list_human_output(tmp_path, capsys):
    """人类可读:输出行 = 时间/动作:状态/规则名(快照)/条目标题(design §8)。"""
    db = tmp_path / "alerts.db"
    _seed_fired_history(db)
    code = main(["alerts", "list", "--db", str(db)])

    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "世事 alerts list:共 2 条命中(新→旧)" in out
    assert "[tag:tagged] AI 打标 — AI 进展" in out
    assert "[push:send_failed] 竞对融资 — A 公司完成 B 轮融资" in out


def test_alerts_list_empty_history_is_legal(tmp_path, capsys):
    """零命中(不配规则的零惊扰默认)是合法态:count=0,人类可读如实报 0。"""
    db = tmp_path / "empty.db"
    code = main(["alerts", "list", "--db", str(db), "--json"])

    assert code == EXIT_OK
    assert json.loads(capsys.readouterr().out)["count"] == 0

    code = main(["alerts", "list", "--db", str(db)])
    assert code == EXIT_OK
    assert "共 0 条命中" in capsys.readouterr().out


def test_alerts_cli_is_readonly_v1(capsys):
    """v1 无写子命令:save/delete 等用法错误归退出码 1;子命令集恰为 {list}。"""
    assert main(["alerts", "save"]) == EXIT_CONFIG_ERROR
    assert "usage" in capsys.readouterr().err

    parser = build_parser()
    alerts_parser = parser._subparsers._group_actions[0].choices["alerts"]  # type: ignore[union-attr]
    sub_choices = alerts_parser._subparsers._group_actions[0].choices  # type: ignore[union-attr]
    assert set(sub_choices) == {"list"}


# ---------------------------------------------------------------------------
# cron:定时任务族(10-04-hermes-cron design §4.1 / implement.md B2)。
# 离线原则:CLI 手动 tick 与 serve 同款注入真执行体(CronRunner.execute,
# spawn ``myssia run --json``);本文件在 spawn 层断掉真子进程(替身直携
# RunResult payload)——品类管线从不被构造,零网络;此处只测 CLI 面
# (参数、--json 契约、退出码、过滤、派发接线)。
# ---------------------------------------------------------------------------


def _offline_cron_runner(monkeypatch: pytest.MonkeyPatch) -> None:
    """CLI 层 CronRunner → 离线替身(spawn 层直携 payload,零子进程)。

    复查修(10-04):手动 ``cron tick`` 不再走底座 no-op stub(F2.3「外接
    cron 用」口径下会记假成功),与 serve 同款注入 ``CronRunner.execute``。
    CLI 面测试的离线原则改由此替身承担:exit 0 + RunResult payload →
    派发路径完整走执行体/账本/记账,只是不 spawn 真进程。
    """
    from myssia.cron.runner import CronRunner, SubprocessResult

    payload = {
        "status": "success",
        "run_id": 1,
        "dry_run": False,
        "duration_seconds": 0.0,
        "sources": [],
        "items": [],
        "push": [],
        "failures": [],
    }

    def _fake_spawn(cmd, env, *, timeout, inflight=None):
        return SubprocessResult(exit_code=0, payload=payload)

    monkeypatch.setattr(
        cli_module, "CronRunner", lambda cron: CronRunner(cron, spawn=_fake_spawn)
    )


def _write_category(tmp_path) -> Any:
    """品类 YAML 夹具(带 timezone: Asia/Shanghai,供 Q6 时区链断言)。"""
    yaml_path = tmp_path / "cat.yaml"
    yaml_path.write_text(VALID_YAML, encoding="utf-8")
    return yaml_path


def test_cron_create_json_absolute_category_and_category_timezone(tmp_path, capsys):
    """create --json:单份 JSON;Q5 category 存绝对路径;Q6 时区顺势取品类
    YAML 的 timezone(未给 --timezone 时);next_run_at 回显。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"

    code = main(
        [
            "cron",
            "create",
            "every 5m",
            "--category",
            str(yaml_path),
            "--db",
            str(db),
            "--json",
        ]
    )

    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)  # stdout 恰一份可解析 JSON
    job = payload["job"]
    assert payload["command"] == "cron" and payload["action"] == "create"
    assert job["category"] == str(yaml_path.resolve())  # Q5:绝对路径存储
    assert job["timezone"] == "Asia/Shanghai"  # Q6:顺势取品类 YAML timezone
    assert job["schedule"] == {"kind": "interval", "minutes": 5, "display": "every 5m"}
    assert job["next_run_at"]  # 回显下次运行
    assert job["origin"] == {"source": "cli"}
    # 落盘:<数据根>/cron/jobs.json(数据根 = db 父目录)
    stored = json.loads((tmp_path / "cron" / "jobs.json").read_text(encoding="utf-8"))
    assert [j["id"] for j in stored["jobs"]] == [job["id"]]


def test_cron_create_timezone_flag_overrides_category(tmp_path, capsys):
    """--timezone 显式实参优先于品类 YAML 的 timezone。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"

    code = main(
        [
            "cron",
            "create",
            "0 9 * * 1",
            "--category",
            str(yaml_path),
            "--timezone",
            "UTC",
            "--db",
            str(db),
            "--json",
        ]
    )

    assert code == EXIT_OK
    job = json.loads(capsys.readouterr().out)["job"]
    assert job["timezone"] == "UTC"
    assert job["schedule"]["kind"] == "cron"


def test_cron_create_invalid_category_exits_one_no_job_persisted(tmp_path, capsys):
    """Q6:品类 YAML 坏(未知字段)→ 完整装载校验早失败,exit 1,错误带字段
    路径;jobs.json 不落任何 job。"""
    bad = tmp_path / "bad.yaml"
    bad.write_text(VALID_YAML + "\nnope: 未知字段\n", encoding="utf-8")
    db = tmp_path / "myssia.db"

    code = main(
        [
            "cron",
            "create",
            "every 5m",
            "--category",
            str(bad),
            "--db",
            str(db),
            "--json",
        ]
    )

    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"] == "config"
    assert payload["errors"][0]["path"] == "$.nope"
    jobs_file = tmp_path / "cron" / "jobs.json"
    assert not jobs_file.exists()  # 早失败:注册表零残留


def test_cron_create_missing_category_file_exits_one(tmp_path, capsys):
    """Q6:品类文件不存在 → exit 1 结构化 file_not_found。"""
    db = tmp_path / "myssia.db"
    code = main(
        [
            "cron",
            "create",
            "every 5m",
            "--category",
            str(tmp_path / "nope.yaml"),
            "--db",
            str(db),
            "--json",
        ]
    )
    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["errors"][0]["error_type"] == "file_not_found"


def test_cron_create_bad_schedule_exits_one(tmp_path, capsys):
    """schedule 解析失败 → exit 1,消息带五形态用法清单(底座 parse_schedule
    文案照抄 H);不落 job。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"

    code = main(
        [
            "cron",
            "create",
            "nonsense ###",
            "--category",
            str(yaml_path),
            "--db",
            str(db),
            "--json",
        ]
    )

    assert code == EXIT_CONFIG_ERROR
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"] == "cron_create_failed"
    assert "Invalid schedule 'nonsense ###'" in payload["message"]
    assert not (tmp_path / "cron" / "jobs.json").exists()


def test_cron_create_paused_reason_requires_paused(tmp_path, capsys):
    """--paused-reason 不带 --paused:底座自相矛盾守卫 → exit 1。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"

    code = main(
        [
            "cron",
            "create",
            "every 5m",
            "--category",
            str(yaml_path),
            "--paused-reason",
            "等主人放行",
            "--db",
            str(db),
            "--json",
        ]
    )

    assert code == EXIT_CONFIG_ERROR
    assert json.loads(capsys.readouterr().out)["error"] == "cron_create_failed"


def test_cron_create_paused_job_has_no_next_run(tmp_path, capsys):
    """--paused:生而暂停(state=paused、next_run_at=None),list 默认不可见。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"

    code = main(
        [
            "cron",
            "create",
            "every 5m",
            "--category",
            str(yaml_path),
            "--paused",
            "--db",
            str(db),
            "--json",
        ]
    )

    assert code == EXIT_OK
    job = json.loads(capsys.readouterr().out)["job"]
    assert job["state"] == "paused" and job["next_run_at"] is None
    assert job["paused_reason"]  # 缺省审计文案


def test_cron_list_filters_paused_and_all_includes(tmp_path, capsys):
    """list 默认只看启用;--all 含 paused;人类输出带 name/schedule/deliver。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    assert (
        main(
            [
                "cron",
                "create",
                "every 5m",
                "--category",
                str(yaml_path),
                "--db",
                str(db),
            ]
        )
        == EXIT_OK
    )
    assert (
        main(
            [
                "cron",
                "create",
                "0 9 * * 1",
                "--category",
                str(yaml_path),
                "--name",
                "morning",
                "--paused",
                "--db",
                str(db),
            ]
        )
        == EXIT_OK
    )
    capsys.readouterr()

    code = main(["cron", "list", "--db", str(db), "--json"])
    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["count"] == 1  # 默认过滤 paused
    assert payload["jobs"][0]["schedule_display"] == "every 5m"
    assert payload["data_root"] == str(tmp_path)

    code = main(["cron", "list", "--db", str(db), "--all", "--json"])
    assert code == EXIT_OK
    assert json.loads(capsys.readouterr().out)["count"] == 2

    code = main(["cron", "list", "--db", str(db), "--all"])
    assert code == EXIT_OK
    out = capsys.readouterr().out
    assert "cat.yaml [scheduled]" in out and "morning [paused]" in out
    assert "schedule: 0 9 * * 1" in out and "deliver: local" in out


def test_cron_lifecycle_run_pause_resume_remove_json(tmp_path, capsys):
    """run(trigger)/pause/resume/remove 的 --json 契约与退出码;重删 → 1。"""
    from myssia.cron.jobs import CronJobs

    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    assert (
        main(
            [
                "cron",
                "create",
                "every 5m",
                "--category",
                str(yaml_path),
                "--db",
                str(db),
                "--json",
            ]
        )
        == EXIT_OK
    )
    job_id = json.loads(capsys.readouterr().out)["job"]["id"]

    # run:下次 tick 立即跑(manual 标记)
    code = main(["cron", "run", job_id, "--db", str(db), "--json"])
    assert code == EXIT_OK
    triggered = json.loads(capsys.readouterr().out)["job"]
    assert triggered["manual_run_at"] == triggered["next_run_at"]

    # pause → state=paused;resume → state=scheduled 且 next_run_at 重算
    assert main(["cron", "pause", job_id, "--db", str(db), "--json"]) == EXIT_OK
    paused = json.loads(capsys.readouterr().out)["job"]
    assert paused["state"] == "paused"
    assert main(["cron", "resume", job_id, "--db", str(db), "--json"]) == EXIT_OK
    resumed = json.loads(capsys.readouterr().out)["job"]
    assert resumed["state"] == "scheduled" and resumed["next_run_at"]

    # 名字也能寻址(resolve_job_ref;CLI 同一解析面)
    assert main(["cron", "pause", "cat.yaml", "--db", str(db), "--json"]) == EXIT_OK
    assert CronJobs.for_db(db).get_job(job_id)["state"] == "paused"
    capsys.readouterr()

    # remove:记录删,再删 → 1
    assert main(["cron", "remove", job_id, "--db", str(db), "--json"]) == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["removed"] is True and payload["job_id"] == job_id
    assert (
        main(["cron", "remove", job_id, "--db", str(db), "--json"]) == EXIT_CONFIG_ERROR
    )
    assert json.loads(capsys.readouterr().out)["error"] == "cron_job_not_found"


def test_cron_unknown_and_missing_job_exit_one(tmp_path, capsys):
    """未知 job 引用与未知子命令都归 exit 1(不撞 2/3 的采集语义)。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    assert (
        main(["cron", "pause", "ghost", "--db", str(db), "--json"]) == EXIT_CONFIG_ERROR
    )
    assert json.loads(capsys.readouterr().out)["error"] == "cron_job_not_found"
    assert main(["cron", "bogus"]) == EXIT_CONFIG_ERROR
    assert "usage" in capsys.readouterr().err


def test_cron_pause_all_estop_blocks_tick_resume_all_fires(
    tmp_path, capsys, monkeypatch
):
    """Q4:pause --all 踩 estop 标记 → 到期 job 不派发;resume --all 解除 →
    同一 tick 派发(离线替身记 ok)。"""
    from myssia.cron.jobs import CronJobs

    _offline_cron_runner(monkeypatch)
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    assert (
        main(
            [
                "cron",
                "create",
                "every 5m",
                "--category",
                str(yaml_path),
                "--db",
                str(db),
                "--json",
            ]
        )
        == EXIT_OK
    )
    job_id = json.loads(capsys.readouterr().out)["job"]["id"]
    cron = CronJobs.for_db(db)
    cron.update_job(job_id, {"next_run_at": "2026-10-04T08:00:00+08:00"})  # 强制到期

    # 急停:tick 静默 0,job 原样到期未被派发
    assert main(["cron", "pause", "--all", "--db", str(db), "--json"]) == EXIT_OK
    assert json.loads(capsys.readouterr().out)["estopped"] is True
    assert main(["cron", "tick", "--db", str(db)]) == EXIT_OK
    capsys.readouterr()
    assert CronJobs.for_db(db).get_job(job_id)["last_status"] is None

    # status 报告急停态
    assert main(["cron", "status", "--db", str(db), "--json"]) == EXIT_OK
    assert json.loads(capsys.readouterr().out)["estopped"] is True

    # 解除:同一 tick 派发一发(离线替身 → ok),next_run_at 重锚
    assert main(["cron", "resume", "--all", "--db", str(db), "--json"]) == EXIT_OK
    assert json.loads(capsys.readouterr().out)["cleared"] is True
    assert main(["cron", "tick", "--db", str(db)]) == EXIT_OK
    fired = CronJobs.for_db(db).get_job(job_id)
    assert fired["last_status"] == "ok"
    assert fired["next_run_at"] != "2026-10-04T08:00:00+08:00"


def test_cron_tick_dispatch_records_execution_and_runs_lists_it(
    tmp_path, capsys, monkeypatch
):
    """到期 tick(离线替身执行体)→ 执行账本落行;runs --json 出账、--limit 钳制。"""
    from myssia.cron.jobs import CronJobs

    _offline_cron_runner(monkeypatch)
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    assert (
        main(
            [
                "cron",
                "create",
                "every 5m",
                "--category",
                str(yaml_path),
                "--db",
                str(db),
                "--json",
            ]
        )
        == EXIT_OK
    )
    job_id = json.loads(capsys.readouterr().out)["job"]["id"]
    CronJobs.for_db(db).update_job(job_id, {"next_run_at": "2026-10-04T08:00:00+08:00"})

    assert main(["cron", "tick", "--db", str(db)]) == EXIT_OK
    capsys.readouterr()

    code = main(["cron", "runs", "--db", str(db), "--json"])
    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["count"] == 1
    record = payload["executions"][0]
    assert record["job_id"] == job_id and record["source"] == "tick"
    assert record["status"] == "completed"  # 离线替身执行体记成功

    # 按 job 过滤 + limit;未知 job 过滤 → 1
    assert (
        main(["cron", "runs", job_id, "--db", str(db), "--limit", "1", "--json"])
        == EXIT_OK
    )
    assert json.loads(capsys.readouterr().out)["count"] == 1
    assert (
        main(["cron", "runs", "ghost", "--db", str(db), "--json"]) == EXIT_CONFIG_ERROR
    )

    # 人类可读:状态行 + 账本条目
    assert main(["cron", "runs", "--db", str(db)]) == EXIT_OK
    out = capsys.readouterr().out
    assert "[completed]" in out and f"job={job_id}" in out


def test_cron_edit_reschedules_and_updates_payload(tmp_path, capsys):
    """edit --schedule 重算 next_run_at(schedule_display 跟随);裸 edit 无
    字段 → 1。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    assert (
        main(
            [
                "cron",
                "create",
                "every 5m",
                "--category",
                str(yaml_path),
                "--db",
                str(db),
                "--json",
            ]
        )
        == EXIT_OK
    )
    job_id = json.loads(capsys.readouterr().out)["job"]["id"]

    code = main(
        [
            "cron",
            "edit",
            job_id,
            "--schedule",
            "0 9 * * 1-5",
            "--deliver",
            "feishu:测试群",
            "--db",
            str(db),
            "--json",
        ]
    )
    assert code == EXIT_OK
    edited = json.loads(capsys.readouterr().out)["job"]
    assert edited["schedule"]["kind"] == "cron"
    assert edited["schedule_display"] == "0 9 * * 1-5"
    assert edited["deliver"] == "feishu:测试群"
    assert edited["next_run_at"]  # 重算出的下次运行

    assert (
        main(["cron", "edit", job_id, "--db", str(db), "--json"]) == EXIT_CONFIG_ERROR
    )
    assert json.loads(capsys.readouterr().out)["error"] == "cron_edit_no_changes"

    # edit --category 同样走 Q6 早失败
    assert (
        main(
            [
                "cron",
                "edit",
                job_id,
                "--category",
                str(tmp_path / "nope.yaml"),
                "--db",
                str(db),
                "--json",
            ]
        )
        == EXIT_CONFIG_ERROR
    )
    assert json.loads(capsys.readouterr().out)["error"] == "config"


def test_cron_status_json_contract_and_empty_state(tmp_path, capsys):
    """status --json:单份契约载荷;空数据根 = 合法态(0 job,ticker 未跑)。"""
    db = tmp_path / "myssia.db"
    code = main(["cron", "status", "--db", str(db), "--json"])
    assert code == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["command"] == "cron" and payload["action"] == "status"
    assert payload["ticker_alive"] is False  # 从未 serve:心跳缺位如实报告
    assert payload["heartbeat_age_seconds"] is None
    assert payload["estopped"] is False
    assert payload["jobs_total"] == 0 and payload["next_due_at"] is None

    # 空转 tick 写心跳(status 端立即可见;同进程 pid 存活 → 判活)
    assert main(["cron", "tick", "--db", str(db)]) == EXIT_OK
    capsys.readouterr()
    assert main(["cron", "status", "--db", str(db), "--json"]) == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["heartbeat_age_seconds"] is not None
    assert payload["ticker_alive"] is True


def test_cron_resume_at_rearms_completed_oneshot(tmp_path, capsys):
    """resume --at:一次性 job 完成后重挂新时刻(recurring 拒收 → 1)。"""
    from myssia.cron.jobs import CronJobs

    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    assert (
        main(
            [
                "cron",
                "create",
                "in 1m",
                "--category",
                str(yaml_path),
                "--db",
                str(db),
                "--json",
            ]
        )
        == EXIT_OK
    )
    payload = json.loads(capsys.readouterr().out)
    job_id = payload["job"]["id"]
    assert payload["job"]["schedule"]["kind"] == "once"
    assert payload["job"]["repeat"] == {"times": 1, "completed": 0}  # once 自动 times=1

    # 直接推到终态:模拟一次完成(repeat 计数到限 → state=completed)
    cron = CronJobs.for_db(db)
    job = cron.get_job(job_id)
    assert (
        cron.update_job(
            job_id,
            {
                "repeat": {"times": 1, "completed": 1},
                "state": "completed",
                "enabled": False,
                "next_run_at": None,
            },
        )
        is not None
    )

    code = main(
        [
            "cron",
            "resume",
            job_id,
            "--at",
            "2030-01-01T09:00:00+08:00",
            "--db",
            str(db),
            "--json",
        ]
    )
    assert code == EXIT_OK
    rearmed = json.loads(capsys.readouterr().out)["job"]
    assert rearmed["next_run_at"].startswith("2030-01-01T09:00")
    assert rearmed["state"] == "scheduled"

    # recurring job 拒收 --at(底座照抄文案 → 结构化 1)
    assert (
        main(
            [
                "cron",
                "create",
                "every 5m",
                "--category",
                str(yaml_path),
                "--db",
                str(db),
                "--json",
            ]
        )
        == EXIT_OK
    )
    recurring_id = json.loads(capsys.readouterr().out)["job"]["id"]
    code = main(
        [
            "cron",
            "resume",
            recurring_id,
            "--at",
            "2030-01-01T09:00:00+08:00",
            "--db",
            str(db),
            "--json",
        ]
    )
    assert code == EXIT_CONFIG_ERROR
    assert json.loads(capsys.readouterr().out)["error"] == "cron_resume_failed"


def test_cron_add_alias_maps_to_create(tmp_path, capsys):
    """别名 add(→create)与 rm(→remove)经规范化分发,行为同规范名。"""
    yaml_path = _write_category(tmp_path)
    db = tmp_path / "myssia.db"
    code = main(
        [
            "cron",
            "add",
            "every 5m",
            "--category",
            str(yaml_path),
            "--db",
            str(db),
            "--json",
        ]
    )
    assert code == EXIT_OK
    job_id = json.loads(capsys.readouterr().out)["job"]["id"]
    code = main(["cron", "rm", job_id, "--db", str(db), "--json"])
    assert code == EXIT_OK
    assert json.loads(capsys.readouterr().out)["removed"] is True


def test_cron_subcommand_surface_is_frozen():
    """十一子命令面冻结(design §4.1;别名 add/rm/delete/history 另计)。"""
    parser = build_parser()
    cron_parser = parser._subparsers._group_actions[0].choices["cron"]  # type: ignore[union-attr]
    sub_choices = set(cron_parser._subparsers._group_actions[0].choices)  # type: ignore[union-attr]
    canonical = {
        "list",
        "create",
        "edit",
        "pause",
        "resume",
        "run",
        "remove",
        "status",
        "runs",
        "serve",
        "tick",
    }
    assert canonical <= sub_choices
    assert sub_choices - canonical == {"add", "rm", "delete", "history"}
