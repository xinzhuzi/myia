"""cron 心跳告警(10-05-cron-heartbeat:kind=cron_stale 规则全链).

一个文件收拢本批测试面:

- store:v8→v9 迁移(旧库自动升级/既有行 kind 缺省 'item'/新库基线含两列)
  + kind/params 落库往返(INSERT/UPDATE 两路);
- 构造门:cron_stale 合法三形态(scope 钉品类/explicit/auto/job_id)与拒
  六形态(global/when≠true/params 形状/未知键/阈值二选一违例/item 带 params
  防误配/bad kind);
- 引擎 heartbeat_pass:久未成功触发 fire(文案含品类与时长)/同桶 UNIQUE
  冷却/新鲜静默/从未成功的规则年龄冷静期/恢复通知(同桶)+跨桶不重发/
  auto 阈值(2× 节奏+夹取)/auto 观测不足 WARNING 跳过/未落库规则跳过/
  push 动作按规则品类解析器(sent 与 degraded 两态,跨品类零借用)/
  item 规则不进心跳路径、cron_stale 规则不进条目路径(双向零漂移);
- job_id 精确模式(复核批,PRD 需求 1/测试清单⑦):观测按 (品类, job_id)
  取,健康同品类任务掩蔽不了被盯任务的停摆(含品类级聚合掩蔽对照组)/
  恢复通知按 job 身份去重;
- 账本只读查询:last_completed_at(有/无成功/空 job 集)与
  completed_gap_hours(中位节奏/观测不足 None);
- 管线挂点(接线批):_alert_pass 尾挂 heartbeat_pass,账本解析器注入
  (品类→job_ids 经 jobs.json→ExecutionLedger 只读两查询);零心跳规则
  零 cron 足迹;账本缺位(jobs 建好从未派发)不建库(复核批窄边守卫)。

全部零真实网络零真实等待;推送走注入假件。
"""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest
import httpx
import yaml

from myssia.alerts import AlertConfigError, AlertEngine, compile_rule
from myssia.alerts.engine import heartbeat_pass
from myssia.cron.executions import ExecutionLedger
from myssia.cron.store import CronJobStore
from myssia.pipeline import Item, Pipeline, make_cron_heartbeat_scan
from myssia.push.base import SendReport
from myssia.schema import load_category
from myssia.store import AlertRule, SQLiteStore

NOW = datetime(2026, 10, 5, 12, 0, 0, tzinfo=timezone.utc)
TIMEZONE = "Asia/Shanghai"


def make_store(tmp_path) -> SQLiteStore:
    return SQLiteStore(tmp_path / "heartbeat.db")


def make_heartbeat_rule(**overrides) -> AlertRule:
    base = dict(
        name="ai-news 心跳", when="true", action="tag", action_config={"tags": ["hb"]},
        kind="cron_stale", params={"threshold_hours": 6}, scope="ai-news",
        created_at=NOW - timedelta(hours=30),
    )
    base.update(overrides)
    return AlertRule(**base)


def run(coro):
    return asyncio.run(coro)


# ---------------------------------------------------------------------------
# store:v8 → v9 迁移 + kind/params 往返
# ---------------------------------------------------------------------------

def _make_v8_database(path) -> None:
    """手工造一个 v8 形态的旧库(无 kind/params 列,schema_version=8)."""
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE store_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    conn.execute(
        """CREATE TABLE alert_rules (
             id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
             enabled INTEGER NOT NULL DEFAULT 1, scope TEXT NOT NULL DEFAULT 'global',
             when_expr TEXT NOT NULL, action TEXT NOT NULL, action_config TEXT NOT NULL,
             created_at TEXT NOT NULL, updated_at TEXT NOT NULL)"""
    )
    conn.execute(
        "INSERT INTO store_meta (key, value) VALUES ('schema_version', '8')"
    )
    conn.execute(
        "INSERT INTO alert_rules (name, when_expr, action, action_config,"
        " created_at, updated_at) VALUES ('旧规则', 'true', 'tag', '{\"tags\": [\"x\"]}',"
        " '2026-10-01T00:00:00+00:00', '2026-10-01T00:00:00+00:00')"
    )
    conn.commit()
    conn.close()


def test_migration_v8_to_v9_upgrades_existing_rules(tmp_path):
    db = tmp_path / "old.db"
    _make_v8_database(db)
    store = SQLiteStore(db)
    rules = store.list_alert_rules()
    assert len(rules) == 1
    assert rules[0].kind == "item"  # 既有行零漂移:缺省 kind
    assert rules[0].params is None
    columns = {
        row[1] for row in store.conn.execute("PRAGMA table_info(alert_rules)")
    }
    assert {"kind", "params"} <= columns


def test_heartbeat_rule_roundtrip_insert_and_update(tmp_path):
    store = make_store(tmp_path)
    saved = store.save_alert_rule(make_heartbeat_rule())
    assert saved.kind == "cron_stale" and saved.params == {"threshold_hours": 6}
    saved.params = {"auto": True}
    saved.scope = "freebie"
    updated = store.save_alert_rule(saved)  # UPDATE 路径
    assert updated.params == {"auto": True} and updated.scope == "freebie"
    assert updated.kind == "cron_stale"


# ---------------------------------------------------------------------------
# 构造门:cron_stale 形态
# ---------------------------------------------------------------------------

def test_compile_accepts_three_legal_forms():
    compile_rule(make_heartbeat_rule())  # explicit
    compile_rule(make_heartbeat_rule(params={"auto": True}))  # auto
    compile_rule(make_heartbeat_rule(params={"threshold_hours": 4, "job_id": "j-1"}))


@pytest.mark.parametrize(
    "overrides",
    [
        dict(scope="global"),                                   # 心跳必须钉品类
        dict(when="score > 3"),                                 # when 恒占位 true
        dict(params=None),                                      # params 必须是映射
        dict(params={"threshold_hours": 6, "nope": 1}),         # 未知键
        dict(params={"threshold_hours": 6, "auto": True}),      # 阈值二选一
        dict(params={}),                                        # 阈值必须给一个
        dict(params={"threshold_hours": -1}),                   # 正数
        dict(params={"threshold_hours": True}),                 # bool 非数
        dict(params={"auto": True, "job_id": ""}),              # job_id 非空
    ],
)
def test_compile_rejects_bad_cron_stale_shapes(overrides):
    with pytest.raises(AlertConfigError):
        compile_rule(make_heartbeat_rule(**overrides))


def test_compile_rejects_item_rule_with_params_and_bad_kind():
    with pytest.raises(AlertConfigError, match="params 仅 cron_stale"):
        compile_rule(AlertRule(
            name="x", when="true", action="tag", action_config={"tags": ["t"]},
            params={"auto": True},
        ))
    with pytest.raises(AlertConfigError, match="kind"):
        compile_rule(AlertRule(
            name="x", when="true", action="tag", action_config={"tags": ["t"]},
            kind="webhook",
        ))


# ---------------------------------------------------------------------------
# heartbeat_pass 语义
# ---------------------------------------------------------------------------

def test_fires_when_never_succeeded_past_grace_period(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())  # 规则年龄 30h > 6h
    fired = run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: None, now=NOW))
    assert len(fired) == 1
    assert "ai-news" in fired[0].title and "30" in fired[0].title
    assert fired[0].action_status == "tagged"
    assert fired[0].dedup_key.startswith("cron-stale:ai-news:")


def test_cooldown_same_bucket_is_at_most_once(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())
    run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: None, now=NOW))
    fired_again = run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: None, now=NOW))
    assert fired_again == []  # UNIQUE 门闩 = 每桶一条


def test_fresh_category_stays_silent(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())
    fired = run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: NOW, now=NOW))
    assert fired == []


def test_young_rule_without_history_waitGrace(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(created_at=NOW - timedelta(hours=2)))
    fired = run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: None, now=NOW))
    assert fired == []  # 冷静期:规则年龄 2h < 阈值 6h


def test_stale_then_recovered_notifies_once_per_incident(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())
    run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: None, now=NOW))
    recovered = run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: NOW, now=NOW))
    assert len(recovered) == 1 and "恢复" in recovered[0].title
    again = run(heartbeat_pass(store, [rule], last_success_at=lambda c, j=None: NOW, now=NOW + timedelta(hours=1)))
    assert again == []  # 同事故不重发(近两桶恢复行在场即压制)


def test_auto_threshold_uses_doubled_cadence_and_skips_without_observation(tmp_path, caplog):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(params={"auto": True}, scope="server"))
    fired = run(heartbeat_pass(
        store, [rule], last_success_at=lambda c, j=None: None, now=NOW,
        cadence_hours=lambda c, j=None: 10 if c == "server" else None,
    ))
    assert len(fired) == 1  # 2×10=20h,规则年龄 30h > 20h
    with caplog.at_level("WARNING"):
        skipped = run(heartbeat_pass(
            store, [rule], last_success_at=lambda c, j=None: None, now=NOW, cadence_hours=lambda c, j=None: None,
        ))
    assert skipped == [] and any("观测不足" in r.message for r in caplog.records)


def test_unsaved_rule_is_skipped_with_warning(tmp_path):
    store = make_store(tmp_path)
    fired = run(heartbeat_pass(store, [make_heartbeat_rule()], last_success_at=lambda c, j=None: None, now=NOW))
    assert fired == []  # 无 id 无法占坑:跳过不猜


def test_push_action_resolves_channel_for_rule_category(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(
        action="push", action_config={"channel": "stdout"},
    ))
    seen: list[str] = []

    async def fake_send(items, **kwargs):
        seen.append(kwargs.get("category"))
        return [SendReport(channel="stdout", ok=True, item_count=1)]

    fired = run(heartbeat_pass(
        store, [rule], last_success_at=lambda c, j=None: None, now=NOW,
        channel_resolver_for=lambda category, channel: (
            seen.append(f"resolve:{category}:{channel}") or object()
        ),
        send=fake_send,
    ))
    assert len(fired) == 1 and fired[0].action_status == "sent"
    assert "resolve:ai-news:stdout" in seen and seen[-1] == "ai-news"  # 按规则品类+通道名解析


def test_push_action_degrades_without_channel_for_rule_category(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(
        action="push", action_config={"channel": "telegram"},
    ))
    fired = run(heartbeat_pass(
        store, [rule], last_success_at=lambda c, j=None: None, now=NOW,
        channel_resolver_for=lambda category, channel: None,
    ))
    assert fired[0].action_status == "degraded_no_channel"


def test_item_rules_ignored_by_heartbeat_and_cron_stale_ignored_by_item_pass(tmp_path):
    store = make_store(tmp_path)
    heartbeat_rule = store.save_alert_rule(make_heartbeat_rule())
    item_rule = store.save_alert_rule(AlertRule(
        name="条目规则", when="'快讯' in title", action="tag",
        action_config={"tags": ["flash"]}, scope="ai-news",
    ))
    # 心跳路径只吃 cron_stale
    fired = run(heartbeat_pass(
        store, [heartbeat_rule, item_rule], last_success_at=lambda c, j=None: NOW, now=NOW,
    ))
    assert fired == []
    # 条目路径只吃 item(run_pass 对 cron_stale 零求值)
    item = Item(url="https://example.org/a", title="快讯:某事", category="ai-news")
    item.dedup_key = "k-1"
    engine = AlertEngine(store=store)
    rows = run(engine.run_pass([item], [heartbeat_rule, item_rule]))
    assert len(rows) == 1 and rows[0].rule_name == "条目规则"


# ---------------------------------------------------------------------------
# 账本只读查询
# ---------------------------------------------------------------------------

def _seed_ledger(tmp_path, completions: list[int]) -> ExecutionLedger:
    ledger = ExecutionLedger(tmp_path / "cron-root")
    for hours_ago in completions:
        record = ledger.create_execution("job-1", source="tick")
        ledger.finish_execution(record["id"], success=True)
        # 把 finished_at 回拨到目标时刻(账本 API 不接受自定义时刻,测试直改)
        with ledger.transaction() as conn:
            conn.execute(
                "UPDATE executions SET finished_at = ? WHERE id = ?",
                ((NOW - timedelta(hours=hours_ago)).isoformat(), record["id"]),
            )
    return ledger


def test_ledger_last_completed_and_gap(tmp_path):
    ledger = _seed_ledger(tmp_path, completions=[1, 5, 9, 13])  # 等距 4h × 3 段
    assert ledger.last_completed_at(["job-1"]) is not None
    assert ledger.completed_gap_hours(["job-1"]) == pytest.approx(4.0)
    assert ledger.last_completed_at(["job-other"]) is None
    assert ledger.completed_gap_hours([]) is None


def test_ledger_gap_needs_two_completions(tmp_path):
    ledger = _seed_ledger(tmp_path, completions=[2])
    assert ledger.completed_gap_hours(["job-1"]) is None


# ---------------------------------------------------------------------------
# 管线挂点(第二批接线):_alert_pass 尾挂 heartbeat_pass,账本解析器注入
# ---------------------------------------------------------------------------

def _heartbeat_handler(payloads):
    """direct_api 源的 mock 传输(test_alert_rules.make_handler 同款)."""
    def handler(request):
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(200, json=payloads)
    return handler


def make_pipeline(config, *, handler, store: SQLiteStore, **kwargs):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return Pipeline(config, store=store, client=client, **kwargs)


def _heartbeat_data(category_id: str, **overrides) -> dict:
    """心跳接线测试的品类配置 data(直连源 + 可空 push;load_category 全字段
    合法)。落文件用它而不用 ``model_dump()``:pydantic dump 会把平台专属
    可选字段吐成显式 null/默认值(``ntfy_token: null``/``timeout: 10.0``),
    schema 的平台字段门拒显式形态——手写 YAML 的形态就是这份 data 本身。"""
    data = {
        "id": category_id,
        "name": f"{category_id} 品类",
        "schedule": "0 9 * * *",
        "timezone": TIMEZONE,
        "sources": [
            {
                "name": "api",
                "engine": "direct_api",
                "url": "https://api.demo.local/list",
                "extract": {
                    "type": "json_path",
                    "fields": {"title": "$[*].title", "url": "$[*].url"},
                },
            }
        ],
        "push": [{"channel": "stdout"}],
        "classify": {"builtin": False, "rules": []},
    }
    data.update(overrides)
    load_category(data)  # 门:形状不合法在造数时就炸,不等到落文件/建管线后
    return data


def _write_category_yaml(path, data: dict) -> None:
    """把品类 data 落成可再载入的 YAML(``load_category_file`` 同门可读)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")


def _wire_cron(tmp_path, *, yaml_path, completions: dict):
    """种 cron 侧事实:jobs.json 逐 job 一条(job.category=品类 YAML 绝对路径)
    + 执行账本逐 job 一次成功执行(完成时刻回拨——账本 API 不接受自定义
    时刻,测试直改)。completions:job_id → 距今小时数。"""
    jobs_store = CronJobStore(tmp_path)
    with jobs_store.jobs_lock():
        jobs_store.save_jobs([{
            "id": job_id, "name": f"定时采集 {job_id}", "schedule": "0 * * * *",
            "category": str(yaml_path), "enabled": True,
            "next_run_at": (NOW + timedelta(hours=1)).isoformat(),
        } for job_id in completions], replace=True)
    ledger = ExecutionLedger(tmp_path)
    for job_id, hours_ago in completions.items():
        record = ledger.create_execution(job_id, source="tick")
        ledger.finish_execution(record["id"], success=True)
        with ledger.transaction() as conn:
            conn.execute(
                "UPDATE executions SET finished_at = ? WHERE id = ?",
                ((NOW - timedelta(hours=hours_ago)).isoformat(), record["id"]),
            )


def test_pipeline_heartbeat_wires_jobs_ledger_and_channel(tmp_path):
    """端到端接线:run 尾心跳附加步——品类经 jobs.json 解析 job_ids →
    账本只读驱动 stale 判定 → fired 落库;push 通道按规则品类解析(job 自身
    YAML 路径),宿主品类(server)未配 push 也照发(禁止借宿主凭据的结构面)。"""
    db = tmp_path / "myssia.db"
    store = SQLiteStore(db)
    ai_news_yaml = tmp_path / "plugins" / "ai-news.yaml"
    _write_category_yaml(ai_news_yaml, _heartbeat_data("ai-news"))
    _wire_cron(tmp_path, yaml_path=ai_news_yaml, completions={"job-1": 30})
    store.save_alert_rule(AlertRule(
        name="ai-news 心跳", when="true", action="push",
        action_config={"channel": "stdout"}, kind="cron_stale",
        params={"threshold_hours": 6}, scope="ai-news",
    ))
    host = make_pipeline(
        load_category(_heartbeat_data("server", push=[])),  # 宿主品类零 push:借不到任何通道
        handler=_heartbeat_handler([{"title": "某服务器新闻", "url": "https://api.demo.local/a"}]),
        store=store, db_path=db, wall_clock=lambda: NOW,
    )
    result = asyncio.run(host.run())
    assert result.status == "success"  # 附加步失败也不拖垮 run;这里应全绿
    fired = store.list_fired()
    assert len(fired) == 1
    assert fired[0].dedup_key.startswith("cron-stale:ai-news:")
    assert "ai-news" in fired[0].title and "30" in fired[0].title
    assert fired[0].action_status == "sent"  # 通道自 ai-news YAML 解析成功
    store.close()


def test_pipeline_heartbeat_fresh_completion_stays_silent(tmp_path):
    """新鲜成功(1h 前 < 阈值 6h)→ 静默:接线后的判定链用的是账本真值。"""
    db = tmp_path / "myssia.db"
    store = SQLiteStore(db)
    ai_news_yaml = tmp_path / "plugins" / "ai-news.yaml"
    _write_category_yaml(ai_news_yaml, _heartbeat_data("ai-news"))
    _wire_cron(tmp_path, yaml_path=ai_news_yaml, completions={"job-1": 1})
    store.save_alert_rule(AlertRule(
        name="ai-news 心跳", when="true", action="tag",
        action_config={"tags": ["hb"]}, kind="cron_stale",
        params={"threshold_hours": 6}, scope="ai-news",
    ))
    host = make_pipeline(
        load_category(_heartbeat_data("server", push=[])),
        handler=_heartbeat_handler([{"title": "某服务器新闻", "url": "https://api.demo.local/a"}]),
        store=store, db_path=db, wall_clock=lambda: NOW,
    )
    result = asyncio.run(host.run())
    assert result.status == "success"
    assert store.list_fired() == []
    store.close()


def test_pipeline_without_heartbeat_rules_never_touches_cron(tmp_path):
    """零心跳规则零惊扰:不读 jobs.json/账本,数据根不落 cron 目录(评估只读,
    不给从未用过 cron 的部署留写入足迹)."""
    db = tmp_path / "myssia.db"
    store = SQLiteStore(db)
    store.save_alert_rule(AlertRule(
        name="条目规则", when="'快讯' in title", action="tag",
        action_config={"tags": ["flash"]},
    ))
    host = make_pipeline(
        load_category(_heartbeat_data("server", push=[])),
        handler=_heartbeat_handler([{"title": "快讯:某事", "url": "https://api.demo.local/a"}]),
        store=store, db_path=db, wall_clock=lambda: NOW,
    )
    result = asyncio.run(host.run())
    assert result.status == "success"
    assert len(store.list_fired()) == 1  # 条目规则照常
    assert not (tmp_path / "cron").exists()  # 心跳守卫:零 cron 足迹
    store.close()


# ---------------------------------------------------------------------------
# 复核处置(第三批):job_id 精确模式(PRD 需求 1 / 测试清单⑦)+ 账本缺位
# 零足迹(「评估只读账本零写入」红线的窄边)
# ---------------------------------------------------------------------------

def test_job_id_precise_mode_not_masked_by_healthy_sibling(tmp_path):
    """⑦ job_id 精确模式:观测按 (品类, job_id) 取——被盯任务停摆 30h 照报,
    同品类健康任务掩蔽不了它;新鲜目标静默;dedup 身份与文案都点名 job_id。"""
    store = make_store(tmp_path)
    stale_rule = store.save_alert_rule(make_heartbeat_rule(
        params={"threshold_hours": 6, "job_id": "job-b"},
    ))
    healthy_rule = store.save_alert_rule(make_heartbeat_rule(
        name="job-a 心跳", params={"threshold_hours": 6, "job_id": "job-a"},
    ))
    observations = {
        ("ai-news", "job-a"): NOW,                    # 健康任务:1 分钟前刚成功
        ("ai-news", "job-b"): NOW - timedelta(hours=30),  # 被盯任务:停摆 30h
    }
    fired = run(heartbeat_pass(
        store, [stale_rule, healthy_rule],
        last_success_at=lambda c, j=None: observations.get((c, j)),
        now=NOW,
    ))
    assert len(fired) == 1  # 只有 job-b 的规则 fire;job-a 新鲜静默
    assert fired[0].rule_name == "ai-news 心跳"
    assert fired[0].dedup_key.startswith("cron-stale:ai-news:job-b:")
    assert "job-b" in fired[0].title and "30" in fired[0].title


def test_job_id_category_aggregation_masks_stale_job_by_contrast(tmp_path):
    """对照组(精确模式存在的理由):品类级聚合取全体 job 的最近成功——健康
    job-a 会把停摆 job-b 掩蔽成「品类新鲜」,品类级规则静默。"""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(name="品类级心跳"))
    observations = {
        ("ai-news", "job-a"): NOW,
        ("ai-news", "job-b"): NOW - timedelta(hours=30),
    }

    def aggregating_last(category, job_id=None):
        """品类级 = 该品类全部 job 最近成功的最大值(与 pipeline.job_ids_for
        聚合 + ledger.last_completed_at(job_ids) 同语义)。"""
        if job_id is not None:
            return observations.get((category, job_id))
        values = [v for (cat, _), v in observations.items() if cat == category]
        return max(values) if values else None

    fired = run(heartbeat_pass(
        store, [rule], last_success_at=aggregating_last, now=NOW,
    ))
    assert fired == []  # 聚合视角:品类「新鲜」,job-b 的停摆被掩蔽


def test_job_id_recovery_uses_precise_identity(tmp_path):
    """精确模式的恢复通知按 job 身份去重(近两桶精确查 cron-stale:品类:job)。"""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(
        params={"threshold_hours": 6, "job_id": "job-b"},
    ))
    observations = {"job-b": None}  # 先停摆(从未成功走规则年龄 30h > 6h)

    def last(category, job_id=None):
        return observations.get(job_id or category)

    run(heartbeat_pass(store, [rule], last_success_at=last, now=NOW))
    observations["job-b"] = NOW  # 单任务恢复
    recovered = run(heartbeat_pass(store, [rule], last_success_at=last, now=NOW))
    assert len(recovered) == 1 and "job-b" in recovered[0].title and "恢复" in recovered[0].title
    assert recovered[0].dedup_key.startswith("cron-recovered:ai-news:job-b:")


def test_pipeline_heartbeat_job_id_precise_not_masked(tmp_path):
    """接线级 ⑦:jobs.json 同品类两条 job(job-1 新鲜 1h/job-2 停摆 30h)——
    规则 job_id=job-2 → fire 且点名 job-2;品类级聚合本会被 job-1 掩蔽。"""
    db = tmp_path / "myssia.db"
    store = SQLiteStore(db)
    ai_news_yaml = tmp_path / "plugins" / "ai-news.yaml"
    _write_category_yaml(ai_news_yaml, _heartbeat_data("ai-news"))
    _wire_cron(tmp_path, yaml_path=ai_news_yaml,
               completions={"job-1": 1, "job-2": 30})
    store.save_alert_rule(AlertRule(
        name="job-2 心跳", when="true", action="tag",
        action_config={"tags": ["hb"]}, kind="cron_stale",
        params={"threshold_hours": 6, "job_id": "job-2"}, scope="ai-news",
    ))
    host = make_pipeline(
        load_category(_heartbeat_data("server", push=[])),
        handler=_heartbeat_handler([{"title": "某服务器新闻", "url": "https://api.demo.local/a"}]),
        store=store, db_path=db, wall_clock=lambda: NOW,
    )
    result = asyncio.run(host.run())
    assert result.status == "success"
    fired = store.list_fired()
    assert len(fired) == 1  # 精确模式:job-2 停摆照报(job-1 的健康掩蔽不了)
    assert fired[0].dedup_key.startswith("cron-stale:ai-news:job-2:")
    assert "job-2" in fired[0].title and "30" in fired[0].title
    store.close()


def test_pipeline_heartbeat_missing_ledger_leaves_no_footprint(tmp_path):
    """复核窄边(红线的破口,已修):心跳规则在场 + jobs.json 在场 +
    executions.db 缺位(job 建好从未派发)→ 评估**不建账本库**(缺位=零执行
    记录,从未成功走规则年龄冷静期);ExecutionLedger._connect 的连接期 DDL
    曾会在此自建 executions.db,守卫后 cron/ 目录零新增。"""
    db = tmp_path / "myssia.db"
    store = SQLiteStore(db)
    ai_news_yaml = tmp_path / "plugins" / "ai-news.yaml"
    _write_category_yaml(ai_news_yaml, _heartbeat_data("ai-news"))
    jobs_store = CronJobStore(tmp_path)  # 只种 jobs.json,不进账本(不触发建库)
    with jobs_store.jobs_lock():
        jobs_store.save_jobs([{
            "id": "job-1", "name": "定时采集 job-1", "schedule": "0 * * * *",
            "category": str(ai_news_yaml), "enabled": True,
            "next_run_at": (NOW + timedelta(hours=1)).isoformat(),
        }], replace=True)
    before = sorted(path.name for path in (tmp_path / "cron").iterdir())
    assert "executions.db" not in before and "jobs.json" in before
    store.save_alert_rule(AlertRule(
        name="ai-news 心跳", when="true", action="tag",
        action_config={"tags": ["hb"]}, kind="cron_stale",
        params={"threshold_hours": 6}, scope="ai-news",
    ))
    host = make_pipeline(
        load_category(_heartbeat_data("server", push=[])),
        handler=_heartbeat_handler([{"title": "某服务器新闻", "url": "https://api.demo.local/a"}]),
        store=store, db_path=db, wall_clock=lambda: NOW,
    )
    result = asyncio.run(host.run())
    assert result.status == "success"
    after = sorted(path.name for path in (tmp_path / "cron").iterdir())
    assert after == before  # 零建库零足迹(复核亲测曾在此多出 executions.db)
    assert store.list_fired() == []  # 规则刚建(年龄 ~0 < 6h)冷静期静默
    store.close()


# ---------------------------------------------------------------------------
# 收尾件(池档 C3 边角):ticker 直挂扫描——run 阶段自身异常中断的轮次
# 不再漏评(依赖被评对象跑批成功的评估不是停摆检测)
# ---------------------------------------------------------------------------

def test_ticker_scan_fires_without_any_run(tmp_path, capsys):
    """工厂闭环:规则+账本就位,**零品类 run**(搭车路径根本不在场)→
    同步 scan() 即 fire 且走 stdout 通道(action_status=sent);同桶 UNIQUE
    冷却在直挂路径同样成立(连扫两轮不重发)。"""
    db = tmp_path / "myssia.db"
    store = SQLiteStore(db)
    ai_news_yaml = tmp_path / "plugins" / "ai-news.yaml"
    _write_category_yaml(ai_news_yaml, _heartbeat_data("ai-news"))
    _wire_cron(tmp_path, yaml_path=ai_news_yaml, completions={"job-1": 30})
    store.save_alert_rule(AlertRule(
        name="ai-news 心跳", when="true", action="push",
        action_config={"channel": "stdout"}, kind="cron_stale",
        params={"threshold_hours": 6}, scope="ai-news",
    ))
    store.close()

    scan = make_cron_heartbeat_scan(db)
    scan()  # 同步直调(ticker 线程形态)
    scan()  # 同桶重扫:UNIQUE 门闩不重发

    reopened = SQLiteStore(db)
    fired = reopened.list_fired()
    assert len(fired) == 1
    assert fired[0].dedup_key.startswith("cron-stale:ai-news:")
    # 直挂路径走真时钟(_utc_now),静默时长=实距账本回拨点(~30h+N,非定数):
    # 断言文案点名品类+量纲,不断言具体小时数。
    assert "ai-news" in fired[0].title and "小时无成功采集" in fired[0].title
    assert fired[0].action_status == "sent"  # 通道经规则品类 YAML 解析(stdout)
    out = capsys.readouterr().out
    assert "ai-news" in out  # stdout 通道真发卡片行(与管线搭车路径同门)
    reopened.close()


def test_ticker_scan_missing_db_leaves_no_footprint(tmp_path):
    """库缺位零足迹:myssia.db 不存在(告警规则无从谈起)→ scan() 直接返回,
    不从 ticker 线程建库——评估只读精神,首跑种子前的数据根零意外文件。"""
    missing = tmp_path / "none.db"
    make_cron_heartbeat_scan(missing)()
    assert not missing.exists()
    assert list(tmp_path.iterdir()) == []  # 数据根整体零足迹
