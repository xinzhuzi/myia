"""HTTP API 门控真库测试(task 10-14-wechat-http-api R12/R13;MYIA_WECHAT_E2E=1)。

对**真解密副本**(数据资产已就位:20 钥 keys.json 已验真、346MB 消息库)跑:

- Pull 两轮拉取与 ``sqlite3 COUNT(*) WHERE create_time>since`` 交叉核对(AC5);
- 深分页基准(R13/AC6):limit=1000 × offset ∈ {0, 50000, 200000, 库内最大},
  p50/p95 落档,**任一点 p95 > 5s = 未过**(依赖声明:C1 R1 副本索引自举未落
  时,无索引 ORDER BY 全排序在 20 万级 offset 上可能超阈——见任务设计拷问①);
- /api/v1/messages 与 CLI 编排(localdb.query_history 直调)同库同参耗时对拍;
- 真 revoke 行(local_type=10002)事件合成(R8);
- SSE 一轮真扫描端到端(水位写在临时数据根,真库副本只读)。

红线:全程零微信进程干预、零写微信侧数据;副本重建只落数据根私有区。
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
import statistics
import time
from pathlib import Path

import pytest

import wechat_bridge.httpapi as httpapi
import wechat_bridge.localdb as localdb
import wechat_bridge.watermark as watermark
from wechat_bridge.config import load_config
from wechat_bridge.watermark import EventHub, WatermarkScanner, parse_revoke_events

pytestmark = pytest.mark.skipif(
    os.environ.get("MYIA_WECHAT_E2E") != "1",
    reason="真库门控默认跳过(design §8:MYIA_WECHAT_E2E=1 才跑)",
)

#: 对拍群(TMS 群,解密副本实测锚;env 可覆写)。
CHAT = os.environ.get("MYIA_WECHAT_E2E_CHAT", "50438708676@chatroom")
CHAT_TABLE = "Msg_" + hashlib.md5(CHAT.encode()).hexdigest()

DEEP_PAGING_OFFSETS = (0, 50_000, 200_000)
DEEP_PAGING_LIMIT = 1000
DEEP_PAGING_SAMPLES = 5
P95_GATE_SECONDS = 5.0


def _message_copy_path() -> Path:
    from wechat_bridge.config import myssia_home

    return (
        myssia_home()
        / "wechat-localdb"
        / "decrypted"
        / "message"
        / "message_0.db"
    )


def _require_assets() -> sqlite3.Connection:
    """真解密副本在场(先经端点链触发 ensure);不在场 = 明确失败。"""
    path = _message_copy_path()
    if not path.is_file():
        pytest.fail(
            f"真解密副本缺位: {path}(先跑一次 localdb query 触发 E2,或核对 MYIA_HOME)"
        )
    return sqlite3.connect(f"file:{path}?mode=ro", uri=True)


@pytest.fixture(scope="module")
def service():
    config = load_config()
    svc = httpapi.HttpApiService(
        config=config,
        host="127.0.0.1",
        port=0,
        config_path=None,
        data_root=None,  # 真数据根
    )
    svc._current_token()  # token 状态预热(不设 token 则端点调用走注入路径)
    return svc


def _pull(service: httpapi.HttpApiService, **params) -> dict:
    """绕鉴权直调编排(门控面:数据正确性,不走 socket;鉴权面归 CI 件)。"""
    return service.pull_messages(
        CHAT,
        int(params["since"]),
        params.get("end"),
        int(params.get("limit", 500)),
        int(params.get("offset", 0)),
    )


class TestPullCrossCheck:
    def test_two_round_pull_matches_sqlite_count(self, service) -> None:
        con = _require_assets()
        try:
            (row_max,) = con.execute(
                f'SELECT MAX(create_time) FROM "{CHAT_TABLE}"'
            ).fetchone()
        finally:
            con.close()
        since = int(row_max) - 7 * 86400  # 近 7 天窗口
        first = _pull(service, since=since, limit=500)
        con = _require_assets()
        try:
            (count,) = con.execute(
                f'SELECT COUNT(*) FROM "{CHAT_TABLE}" WHERE create_time > ?', (since,)
            ).fetchone()
        finally:
            con.close()
        if count <= 500:
            assert len(first["messages"]) == count
            assert first["sync"]["hasMore"] is False
            assert first["sync"]["nextOffset"] == 0
            assert first["sync"]["nextSince"] == first["sync"]["watermark"]
            return
        assert len(first["messages"]) == 500  # 取满 → hasMore 翻页语义
        assert first["sync"]["hasMore"] is True
        assert first["sync"]["nextOffset"] == 500
        assert first["sync"]["nextSince"] == since  # 翻页期 since 不动
        second = _pull(service, since=since, limit=500, offset=500)
        assert [m["ts"] for m in second["messages"]] == sorted(
            m["ts"] for m in second["messages"]
        )
        assert second["messages"][0]["ts"] >= first["messages"][-1]["ts"]  # 升序续页不回退
        # 拉毕(取到不满页)→ 跳水位。
        pages = [first, second]
        offset = 1000
        for _ in range(20):  # 上限 20 页防失控
            page = _pull(service, since=since, limit=500, offset=offset)
            pages.append(page)
            offset += 500
            if not page["sync"]["hasMore"]:
                break
        last = pages[-1]
        assert last["sync"]["hasMore"] is False
        assert last["sync"]["nextSince"] == last["sync"]["watermark"] >= int(row_max)
        total = sum(len(p["messages"]) for p in pages)
        print(f"\n[pull 交叉核对] sqlite COUNT={count} 端点合计={total} 页数={len(pages)}")
        assert total == count  # 不丢不重(两轮翻页全程)


class TestDeepPagingBenchmark:
    def test_deep_paging_p95_gate(self, service) -> None:
        """R13:各 offset 点 p50/p95 落档;任一点 p95 > 5s = 未过。"""
        con = _require_assets()
        try:
            (row_max_ts,) = con.execute(
                f'SELECT MAX(create_time) FROM "{CHAT_TABLE}"'
            ).fetchone()
            (row_min_ts,) = con.execute(
                f'SELECT MIN(create_time) FROM "{CHAT_TABLE}"'
            ).fetchone()
            (total_rows,) = con.execute(
                f'SELECT COUNT(*) FROM "{CHAT_TABLE}" WHERE create_time > ?',
                (int(row_min_ts) - 1,),
            ).fetchone()
        finally:
            con.close()
        since = int(row_min_ts) - 1  # 全量窗口:深分页压力面
        offsets = list(DEEP_PAGING_OFFSETS) + [max(0, int(total_rows) - DEEP_PAGING_LIMIT)]
        report_lines = [
            f"\n[深分页基准] chat={CHAT} 表行数={total_rows} since={since}"
            f"(门 p95<{P95_GATE_SECONDS}s;C1 副本索引未落时大 offset 可能超阈——设计拷问①)"
        ]
        for offset in offsets:
            durations = []
            for _ in range(DEEP_PAGING_SAMPLES):
                started = time.perf_counter()
                page = _pull(
                    service, since=since, limit=DEEP_PAGING_LIMIT, offset=offset
                )
                durations.append(time.perf_counter() - started)
            ordered = sorted(durations)
            p50 = statistics.median(durations)
            p95 = ordered[max(0, min(len(ordered) - 1, int(0.95 * len(ordered))))]
            report_lines.append(
                f"  offset={offset:>8} rows={len(page['messages']):>5} "
                f"p50={p50*1000:8.1f}ms p95={p95*1000:8.1f}ms"
            )
            assert p95 < P95_GATE_SECONDS, (
                f"深分页未过门槛: offset={offset} p95={p95:.2f}s ≥ {P95_GATE_SECONDS}s"
                "(R13:design 换策略——副本索引/键集分页——后重测)"
            )
        print("\n".join(report_lines))

    def test_messages_endpoint_vs_cli_orchestration_timing(
        self, service, monkeypatch
    ) -> None:
        """/api/v1/messages 与 CLI 编排同库同参耗时对拍(AC6;差值≈HTTP 开销)。

        token 走注入(门控机不写真配置文件):handle() 全链 = 鉴权 + 编排,
        与 localdb.query_history 直调对拍。
        """
        config = load_config()
        monkeypatch.setattr(service, "_current_token", lambda: "bench-token")
        durations_direct = []
        durations_api = []
        for _ in range(3):
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            started = time.perf_counter()
            localdb.query_history(config, storage, keys, CHAT, 7)
            durations_direct.append(time.perf_counter() - started)
            started = time.perf_counter()
            response = service.handle(
                "GET",
                f"/api/v1/messages?chat_id={CHAT}&since_days=7",
                {"Authorization": "Bearer bench-token"},
            )
            durations_api.append(time.perf_counter() - started)
            assert response.status == 200
        print(
            f"\n[对拍] CLI 编排 p50={statistics.median(durations_direct)*1000:.1f}ms"
            f" HTTP 核心 p50={statistics.median(durations_api)*1000:.1f}ms(差值≈HTTP 开销)"
        )


class TestRealRevoke:
    def test_real_revoke_row_synthesis(self) -> None:
        """真 revoke 行事件合成(R8):全表族找 10002 行 + newmsgid 配对
        (能配上最好,配不上=仅撤回事实,不臆造)。"""
        from wechat_bridge.localdb_query import (
            _decode_text_content,
            find_message_tables,
            name2id_maps,
        )

        con = _require_assets()
        try:
            located = None
            for table, colmap in find_message_tables(con):
                if not colmap.get("chat"):
                    continue
                row = con.execute(
                    f'SELECT create_time, real_sender_id, message_content FROM "{table}" '
                    "WHERE local_type = 10002 ORDER BY create_time DESC LIMIT 1"
                ).fetchone()
                if row is not None:
                    located = (table, colmap, row)
                    break
        finally:
            con.close()
        if located is None:
            pytest.skip("真库所有会话表均无 10002 行(无撤回记录可合成)")
        table, colmap, (ts, sender_id, content) = located
        chat_id = str(colmap["chat"])
        text, _placeholder = _decode_text_content(content, None, None)
        rows = [{"ts": int(ts), "sender": f"sender_{sender_id}", "local_type": 10002,
                 "text": text, "server_id": None, "rowid": 0}]
        newmsgid = watermark._REVOKE_NEWMSGID_RE.search(text or "")
        if newmsgid:
            con = _require_assets()
            try:
                original = con.execute(
                    f'SELECT create_time, message_content FROM "{table}" '
                    "WHERE server_id = ? LIMIT 1",
                    (int(newmsgid.group(1)),),
                ).fetchone()
            finally:
                con.close()
            if original:
                orig_text, _p = _decode_text_content(original[1], None, None)
                rows.append({"ts": int(original[0]), "sender": "orig", "local_type": 1,
                             "text": orig_text, "server_id": int(newmsgid.group(1)),
                             "rowid": 1})
        events = parse_revoke_events(rows, chat_id)
        assert events, "真 10002 行必须合成出 revoke 事件"
        event = events[0]
        assert event["type"] == "message.revoke" and event["chat_id"] == chat_id
        if "orig_preview" in event:
            assert len(event["orig_preview"]) <= 30
        print(f"\n[真 revoke] chat={chat_id[:16]}… ts={event['ts']} "
              f"sender_shape={bool(event['sender'])} "
              f"orig_preview={'orig_preview' in event}")


class TestSseRealRound:
    def test_one_real_scan_round_end_to_end(self, tmp_path: Path) -> None:
        """SSE 一轮真扫描端到端:真定位/取钥/副本链 + 临时水位根(不碰真水位文件)。"""
        config = load_config()
        hub = EventHub()
        scanner = WatermarkScanner(
            hub=hub,
            config=config,
            data_root=tmp_path,  # 水位文件隔离在 tmp:不写真实 http-watermark.json
            resolve=lambda storage: localdb.resolve_keys(storage, config=config),
            ensure=lambda storage, keys: localdb.ensure_decrypted_copies(
                storage,
                keys,
                domains=["session", "message"],
                ttl_hours=config.copy_ttl_hours,
                capacity_mb=config.copy_capacity_mb,
                data_root=None,  # 副本走真数据根(已在场则 kept)
            ),
        )
        watermark.write_watermark(tmp_path, time.time() - 600)  # 断档 10 分钟:首轮补发
        started = time.perf_counter()
        value = scanner.scan_once()
        elapsed = time.perf_counter() - started
        events = [payload for _eid, payload in hub.events_after(0)]
        assert value > 0
        print(
            f"\n[SSE 真扫描] 一轮耗时={elapsed*1000:.0f}ms 事件数={len(events)} "
            f"水位推进至={value:.0f}(门 p95<5s;50 会话上限)"
        )
        assert elapsed < 5.0, f"单轮扫描 {elapsed:.2f}s ≥ 5s 红线(R13)"
        for payload in events[:5]:
            assert payload["type"] in ("message.new", "message.revoke")
            assert payload["chat_id"] and isinstance(payload["ts"], int)
