"""mock sidecar 桥(S7 无头冒烟;六方法 doctor/runs.list/run.status/store.trend/runs.trend/feedback.stats)。

不 spawn 真 sidecar——POST /rpc 按当前场景回夹具(形状严格仿
desktop/ui-src/src/screens/dashboard/dashboard-screen.test.tsx 的 fixture* 家族;
日期用 UTC 今天动态生成,verdict「今日采集」永远落窗)。场景切换:
GET /scenario?set=ok|dead(驱动脚本在两态截屏之间切换,页面重载即生效)。

应答形与 .zcode/smoke/bridge.mjs 对页面 shim 的契约一致:
{"result": ...} 或 {"error": {code, path, message}}。

用法:python3 mock-bridge.py [端口=8790]
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

UTC = timezone.utc


def utc_today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def iso_now() -> str:
    return datetime.now(UTC).isoformat()


def iso_at(minutes_ago: int) -> str:
    return (datetime.now(UTC) - timedelta(minutes=minutes_ago)).isoformat()


# ---------------------------------------------------------------------------
# 夹具(镜像 dashboard-screen.test.tsx fixtureSource/fixturePlugin/fixtureDoctor)
# ---------------------------------------------------------------------------


def fixture_source(name, state, reason="", latest=None):
    return {
        "name": name,
        "url": f"https://example.com/{name}",
        "engine": "static_html",
        "engine_hint": None,
        "health": {
            "state": state,
            "reason": reason if reason else ("连续无产出" if state == "dead" else ""),
            "observed": 5,
            "latest": latest,
            "baseline": 2,
        },
        "fingerprint_skips": {"observed": 0, "skipped": 0},
    }


def fixture_plugin(overrides=None):
    plugin = {
        "file": "tech.yaml",
        "id": "tech",
        "name": "科技资讯",
        "schedule": "0 9 * * *",
        "timezone": "Asia/Shanghai",
        "push_channels": [],
        "loaded": True,
        "load_errors": None,
        "sources": [],
        "next_fire_at": "2026-10-06T09:00:00+08:00",
        "enrich": None,
    }
    if overrides:
        plugin.update(overrides)
    return plugin


def doctor_ok():
    """ok 态:两品类全 ok 源、零 findings。"""
    return {
        "command": "doctor",
        "generated_at": iso_now(),
        "db": "myssia.db",
        "healthy": True,
        "plugins": [
            fixture_plugin(
                {
                    "sources": [
                        fixture_source(
                            "hn",
                            "ok",
                            latest={"run_id": 1002, "run_status": "success", "item_count": 5, "skip_reason": None, "failed": False},
                        ),
                        fixture_source(
                            "gh",
                            "ok",
                            latest={"run_id": 1002, "run_status": "success", "item_count": 3, "skip_reason": None, "failed": False},
                        ),
                        fixture_source("blog", "ok"),
                    ]
                }
            ),
            fixture_plugin(
                {
                    "file": "life.yaml",
                    "id": "life",
                    "name": "生活方式",
                    "schedule": "30 10 * * *",
                    "sources": [fixture_source("weekly", "ok"), fixture_source("zine", "ok")],
                }
            ),
        ],
        "credentials": {"backend_available": True, "backend_error": None, "entries": []},
        "proxy": {"config": None, "pools": []},
        "findings": [],
        "summary": {"plugins": 2, "sources": 5, "errors": 0, "warnings": 0},
    }


def doctor_dead():
    """dead 态:tech 六源(2 dead/1 degraded/1 unknown/2 ok)+ broken.yaml 拒载品类。

    覆盖:verdict「2 个源失效」、告警清单 3 行 + 溢出、品类节注「1 品类异常」、
    源健康度四态计数 2/1/2/1。
    """
    return {
        "command": "doctor",
        "generated_at": iso_now(),
        "db": "myssia.db",
        "healthy": False,
        "plugins": [
            fixture_plugin(
                {
                    "sources": [
                        fixture_source(
                            "a",
                            "ok",
                            latest={"run_id": 2002, "run_status": "success", "item_count": 4, "skip_reason": None, "failed": False},
                        ),
                        fixture_source("b", "ok"),
                        fixture_source("deadone", "dead", reason="连续无产出"),
                        fixture_source("deadtwo", "dead", reason="连续无产出"),
                        fixture_source("degradedone", "degraded", reason="最近一轮零产出"),
                        fixture_source("unknownone", "unknown"),
                    ]
                }
            ),
            fixture_plugin(
                {
                    "file": "broken.yaml",
                    "id": "broken",
                    "name": "坏品类",
                    "loaded": False,
                    "load_errors": [{"error_type": "config_error", "path": "$", "message": "schema 拒载"}],
                    "next_fire_at": None,
                }
            ),
        ],
        "credentials": {"backend_available": True, "backend_error": None, "entries": []},
        "proxy": {"config": None, "pools": []},
        "findings": [
            {"severity": "error", "scope": "plugin:broken.yaml", "code": "config_error", "message": "schema 拒载"},
        ],
        "summary": {"plugins": 2, "sources": 6, "errors": 1, "warnings": 0},
    }


def history_runs(success, partial, failed, push_ok_today, base_run_id):
    """runs.list 历史行(新→旧,全部落今日 UTC;success 行带 push 数组喂推送格)。"""
    plan = [("success",)] * success + [("partial",)] * partial + [("failed",)] * failed
    runs = []
    for i, (status,) in enumerate(plan):
        run_id = base_run_id + i
        stats = {"items_retained": 3 + (i % 4)}
        if status == "success" and i < push_ok_today:
            stats["push"] = [
                {"channel": "tg", "ok": True},
                {"channel": "mail", "ok": i % 2 == 0},
            ]
        elif status == "failed":
            stats = {"items_retained": 0, "push": [{"channel": "tg", "ok": False}]}
        runs.append(
            {
                "run_id": run_id,
                "category": "tech",
                "status": status,
                "started_at": iso_at(9 * (i + 1)),
                "finished_at": iso_at(9 * (i + 1) - 1),
                "stats": stats,
                "steps": None,
                "error": None if status != "failed" else "源 gh 抓取超时",
            }
        )
    # i=0 最新(9 分钟前)→ 列表本身即新→旧,与 entry.py _m_runs_list 契约一致
    return runs


def store_trend(days, today_count):
    """store.trend:days 窗口逐日 count,今天=今天数,往日给形状(总条数好看)。"""
    today = datetime.now(UTC).date()
    shape = [3, 7, 0, 12, 5, 9, 14, 6, 0, 11, 8, 4, 10]  # 13 个往日
    days_list = []
    for i in range(days - 1, 0, -1):
        d = today - timedelta(days=i)
        days_list.append({"date": d.strftime("%Y-%m-%d"), "count": shape[(i - 1) % len(shape)]})
    days_list.append({"date": today.strftime("%Y-%m-%d"), "count": today_count})
    return {"days": days_list}


def runs_trend(days):
    """runs.trend:窗口内若干天的 total×statuses(成功率折线 + 累计摘要)。"""
    today = datetime.now(UTC).date()
    rows = [
        (2, {"success": 6, "failed": 2, "running": 1}),
        (3, {"success": 9, "partial": 1}),
        (5, {"success": 4, "partial": 2, "failed": 1}),
        (6, {"success": 10}),
        (9, {"success": 7, "failed": 3}),
    ]
    out = []
    for offset, statuses in rows:
        if offset >= days:
            continue
        d = today - timedelta(days=offset)
        out.append({"date": d.strftime("%Y-%m-%d"), "total": sum(statuses.values()), "statuses": statuses})
    out.append({"date": today.strftime("%Y-%m-%d"), "total": 11, "statuses": {"success": 9, "partial": 1, "running": 1}})
    return {"days": out}


def feedback_stats():
    return {
        "window_days": 14,
        "stats": {
            "total": 12,
            "good": 10,
            "bad": 2,
            "bad_ratio": 0.1667,
            "by_channel": {"desktop": 12},
            "top_bad_categories": [{"key": "tech", "bad": 2}],
            "top_bad_words": [{"key": "旧闻", "bad": 1}, {"key": "误报", "bad": 1}],
        },
        "active_tuning": {},
        "tuning_history": [],
    }


# ---------------------------------------------------------------------------
# 场景表:method + params → result
# ---------------------------------------------------------------------------

SCENARIOS = {}


def build_scenario(name):
    if name == "ok":
        doctor = doctor_ok()
        runs = history_runs(success=8, partial=1, failed=1, push_ok_today=3, base_run_id=1001)
        today_count = 128
    else:
        doctor = doctor_dead()
        runs = history_runs(success=6, partial=2, failed=2, push_ok_today=2, base_run_id=2001)
        today_count = 36

    def handler(method, params):
        params = params or {}
        if method == "doctor":
            return doctor
        if method == "runs.list":
            limit = params.get("limit", 20)
            return {"db": "myssia.db", "count": len(runs), "runs": runs[:limit]}
        if method == "run.status":
            return {"runs": []}
        if method == "store.trend":
            days = int(params.get("days") or 14)
            return store_trend(days, today_count)
        if method == "runs.trend":
            days = int(params.get("days") or 14)
            return runs_trend(days)
        if method == "feedback.stats":
            return feedback_stats()
        return None  # method_not_found

    return handler


SCENARIOS["ok"] = build_scenario("ok")
SCENARIOS["dead"] = build_scenario("dead")
current = {"name": "ok"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # 控制台留痕(场景切换 + 方法调用)
        sys.stderr.write("[mock-bridge] " + (fmt % args) + "\n")

    def _json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("access-control-allow-origin", "*")
        self.send_header("access-control-allow-methods", "POST, GET, OPTIONS")
        self.send_header("access-control-allow-headers", "content-type")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._json(204, {})

    def do_GET(self):
        if self.path.startswith("/healthz"):
            self._json(200, {"scenario": current["name"]})
            return
        if self.path.startswith("/scenario"):
            from urllib.parse import parse_qs, urlparse

            qs = parse_qs(urlparse(self.path).query)
            set_to = (qs.get("set") or [current["name"]])[0]
            if set_to in SCENARIOS:
                current["name"] = set_to
            self._json(200, {"scenario": current["name"]})
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self):
        if self.path != "/rpc":
            self._json(404, {"error": "not_found"})
            return
        length = int(self.headers.get("content-length") or 0)
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json(400, {"error": {"code": "bad_request", "path": "$", "message": "请求体不是 JSON"}})
            return
        method = payload.get("method")
        params = payload.get("params") or {}
        sys.stderr.write(f"[mock-bridge] rpc {method} params={json.dumps(params, ensure_ascii=False)}\n")
        result = SCENARIOS[current["name"]](method, params)
        if result is None:
            self._json(200, {"error": {"code": "method_not_found", "path": "$", "message": f"mock 未实现方法 {method}"}})
            return
        self._json(200, {"result": result})


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8790
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"MOCK_BRIDGE_READY http://127.0.0.1:{server.server_address[1]} scenario=ok", flush=True)
    server.serve_forever()
