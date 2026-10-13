"""HTTP API 服务核心单测(task 10-14-wechat-http-api R12;CI 全 mock)。

覆盖面(PRD R12「test_httpapi.py」):鉴权红队、CORS 双向、回环守卫、
四端点与编排同源逐字段对拍、错误映射、路径穿越变体族、SSE(注入免真等)、
grep 守卫(写/装类端点词零混入 + 方法处理器仅三个 + 文档无「实时」)。

数据面 = **临时数据根 + 假副本**(4.1.15 分表形状全合成,零真实语料):
预置新鲜解密副本(源 mtime 拨旧,ensure_decrypted_copies 全程 kept,假 keys
永不进解密链);定位/取钥经 monkeypatch localdb 模块注入(服务与同源对拍
的期望值走**同一**编排函数——HTTP 应答与 CLI 载荷逐字段一致是断言本身)。

配置键扩展(R10 四键)经 monkeypatch ``config._ALLOWED_TOP_KEYS`` 模拟
集成后态(config.py 落键属 integrationSpec;token 读写/热生效路径在此
全真跑:save_config_key 代写 + 每请求热重读)。
"""

from __future__ import annotations

import hashlib
import http.client
import json
import os
import re
import signal
import socket
import sqlite3
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

import wechat_bridge.config as config_module
import wechat_bridge.httpapi as httpapi
import wechat_bridge.localdb as localdb
import wechat_bridge.watermark as watermark
from wechat_bridge.codes import BridgeError
from wechat_bridge.config import load_config

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
DOCS_FILE = Path(__file__).resolve().parents[2] / "docs" / "wechat-http-api.md"

NOW = int(time.time())
CHAT = "filehelper"
CHAT_TABLE = "Msg_" + hashlib.md5(CHAT.encode()).hexdigest()
GROUP_CHAT = "12345678@chatroom"
REVOKE_ORIGINAL_SERVER_ID = 99001

#: 集成后配置封闭清单(config.py 加法 = R10 四键;测试先模拟之)。
_PATCHED_ALLOWED_KEYS = frozenset(
    set(config_module._ALLOWED_TOP_KEYS)
    | {"http_api_enabled", "http_api_host", "http_api_port", "http_api_token"}
)


def _msg_ddl(table: str) -> str:
    return (
        f'CREATE TABLE "{table}" (local_id INTEGER PRIMARY KEY, server_id INTEGER, '
        "local_type INTEGER, sort_seq INTEGER, real_sender_id INTEGER, "
        "create_time INTEGER, status INTEGER, upload_status INTEGER, "
        "download_status INTEGER, server_seq INTEGER, origin_source TEXT, "
        "source TEXT, message_content TEXT, compress_content BLOB, "
        "packed_info_data BLOB, WCDB_CT_message_content INTEGER, WCDB_CT_source INTEGER)"
    )


REVOKE_XML = (
    '<sysmsg type="revokemsg"><revokemsg><session>filehelper</session>'
    f"<msgid>1</msgid><newmsgid>{REVOKE_ORIGINAL_SERVER_ID}</newmsgid>"
    '<replacemsg><![CDATA["文件传输助手" 撤回了一条消息]]></replacemsg>'
    "</revokemsg></sysmsg>"
)


def _build_message_db(path: Path, *, rows_offset: int = 0) -> dict[str, int]:
    """4.1.15 分表形状合成库(Name2Id 反解 + real_sender_id + 撤回对)。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE Name2Id (user_name TEXT PRIMARY KEY, is_session INTEGER)")
    con.execute(_msg_ddl(CHAT_TABLE))
    group_table = "Msg_" + hashlib.md5(GROUP_CHAT.encode()).hexdigest()
    con.execute(_msg_ddl(group_table))
    rowids: dict[str, int] = {}
    for username in (CHAT, "wxid_friend_1", GROUP_CHAT):
        cur = con.execute(
            "INSERT INTO Name2Id (user_name, is_session) VALUES (?, 1)", (username,)
        )
        rowids[username] = int(cur.lastrowid)
    me = rowids[CHAT]
    friend = rowids["wxid_friend_1"]
    # 6 条窗口内行(Pull 分页用:limit=3 两页恰好取完)+ 1 条 40 天前窗口外行。
    base = NOW - 600
    rows = [
        (1, 10001, 1, 1, me, base + 10, 0, 0, "合成文本-第一条"),
        (2, 10002, 1, 2, friend, base + 20, 0, 0, "合成文本-第二条"),
        (3, 10003, 3, 3, friend, base + 30, 0, 0, "img_合成立名"),
        (4, REVOKE_ORIGINAL_SERVER_ID, 1, 4, me, base + 40, 0, 0, "被撤回的原文消息内容"),
        (5, 10005, 10002, 5, me, base + 50, 0, 0, REVOKE_XML),
        (6, 10006, 1, 6, friend, base + 60, 0, 0, "合成文本-末条"),
        (7, 10007, 1, 7, friend, NOW - 40 * 86400, 0, 0, "合成文本-40天前应被窗口滤掉"),
    ]
    for local_id, server_id, local_type, sort_seq, sender, ts, ct, _extra, content in rows:
        con.execute(
            f'INSERT INTO "{CHAT_TABLE}" (local_id, server_id, local_type, sort_seq, '
            "real_sender_id, create_time, status, upload_status, download_status, "
            "server_seq, message_content, WCDB_CT_message_content) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (local_id + rows_offset, server_id, local_type, sort_seq, sender, ts, 0, 0, 0, 0, content, ct),
        )
    con.commit()
    con.close()
    return rowids


def _build_session_db(path: Path, chats: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE SessionTable (strTalker TEXT PRIMARY KEY, nickName TEXT, unreadCount INTEGER)"
    )
    for index, chat in enumerate(chats):
        con.execute(
            "INSERT INTO SessionTable VALUES (?,?,?)", (chat, f"会话-{index}", index)
        )
    con.commit()
    con.close()


def _build_contact_db(path: Path, usernames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE contact (username TEXT PRIMARY KEY, alias TEXT, nickname TEXT, remark TEXT, localType INTEGER)"
    )
    for username in usernames:
        con.execute(
            "INSERT INTO contact VALUES (?,?,?,?,1)",
            (username, None, f"昵称-{username}", None),
        )
    con.commit()
    con.close()


class FakeEnv:
    """临时数据根 + 假副本 + 注入式定位/取钥(同源对拍的两侧共用)。"""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.data_root = root / "home"
        self.storage = root / "wxid_x_1" / "db_storage"
        decrypted = self.data_root / "wechat-localdb" / "decrypted"
        self.copies_dir = decrypted
        self.keys = {
            "message/message_0.db": "ab" * 32,
            "session/session.db": "cd" * 32,
            "contact/contact.db": "ef" * 32,
            "sns/sns.db": "01" * 32,
        }
        # 假副本(明文 sqlite,内容全合成)。
        self.name2id = _build_message_db(decrypted / "message" / "message_0.db")
        _build_session_db(decrypted / "session" / "session.db", [CHAT, GROUP_CHAT])
        _build_contact_db(
            decrypted / "contact" / "contact.db", [CHAT, "wxid_friend_1", GROUP_CHAT]
        )
        (decrypted / "sns").mkdir(parents=True, exist_ok=True)
        sns_con = sqlite3.connect(decrypted / "sns" / "sns.db")
        sns_con.execute(  # 空动态表(feed 面 200 空列表;notices 面缺表如实降级)
            "CREATE TABLE SnsTimeLine (user_name TEXT, content TEXT)"
        )
        sns_con.commit()
        sns_con.close()
        # 假 db_storage 源文件(内容不进解密链:副本恒新鲜 kept;源拨旧防重建)。
        for rel in self.keys:
            source = self.storage / rel
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_bytes(b"fake-source-not-read")
            os.utime(source, (1000, 1000))
        self.config = load_config()

    def patch_chain(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """定位/取钥注入(服务与同源对拍期望值走同一批假件)。"""
        storage = self.storage
        keys = self.keys

        def fake_locate(**_kwargs):
            return storage

        def fake_resolve(db_storage, **_kwargs):
            assert db_storage is storage
            return dict(keys)

        monkeypatch.setattr(localdb, "locate_db_storage", fake_locate)
        monkeypatch.setattr(localdb, "resolve_keys", fake_resolve)

    def service(self, **overrides) -> httpapi.HttpApiService:
        params = dict(
            config=self.config,
            host="127.0.0.1",
            port=0,
            config_path=self.data_root / "wechat-bridge" / "config.json",
            data_root=self.data_root,
        )
        params.update(overrides)
        return httpapi.HttpApiService(**params)


@pytest.fixture()
def env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> FakeEnv:
    fake = FakeEnv(tmp_path)
    monkeypatch.setenv("MYIA_HOME", str(fake.data_root))
    fake.patch_chain(monkeypatch)
    monkeypatch.setattr(
        config_module, "_ALLOWED_TOP_KEYS", _PATCHED_ALLOWED_KEYS
    )
    return fake


class LiveServer:
    """真 socket 服务(127.0.0.1 + 临时端口;后台线程泵)。"""

    def __init__(self, service: httpapi.HttpApiService) -> None:
        self.server = httpapi.build_server(service, {"host": "127.0.0.1", "port": 0})
        self.port = self.server.server_address[1]
        assert self.server.server_address[0] == "127.0.0.1"  # AC2 CI 面:缺省回环
        self.thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True
        )
        self.thread.start()

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        body: bytes | None = None,
        raw: bool = False,
    ) -> http.client.HTTPResponse:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        try:
            if raw:  # 不让客户端规范化路径(路径穿越变体要原样送达)
                conn.putrequest(method, path)
                for key, value in (headers or {}).items():
                    conn.putheader(key, value)
                conn.endheaders()
                if body:
                    conn.send(body)
            else:
                conn.request(method, path, body=body, headers=headers or {})
            return conn.getresponse()
        except Exception:
            conn.close()
            raise

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)


@pytest.fixture()
def live(env: FakeEnv) -> LiveServer:
    server = LiveServer(env.service())
    yield server
    server.stop()


def _write_token(env: FakeEnv, token: str) -> None:
    path = env.data_root / "wechat-bridge" / "config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    raw: dict = {}
    if path.is_file():
        raw = json.loads(path.read_text(encoding="utf-8"))
    if token:
        raw["http_api_token"] = token
    else:
        raw.pop("http_api_token", None)
    path.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# =====================================================================
# R2 鉴权红队
# =====================================================================


class TestAuthRedTeam:
    def test_unconfigured_token_rejects_everything_but_health(self, live: LiveServer) -> None:
        """/health 恒 200;其余全部 401(未配置=防裸奔,AC1)。"""
        response = live.request("GET", "/api/v1/health")
        assert response.status == 200
        for path in (
            "/api/v1/sessions",
            "/api/v1/messages?chat_id=x",
            "/api/v1/group-info?chat_id=x",
            "/api/v1/sns",
            "/api/v1/sessions/x/messages?since=1",
            "/api/v1/push/messages",
            "/api/v1/nope",
        ):
            denied = live.request("GET", path)
            assert denied.status == 401, path
            payload = json.loads(denied.read())
            assert payload["error"]["code"] == "unauthorized"
            assert "http-token generate" in payload["error"]["fix_hint"]

    def test_wrong_bearer_is_401(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "correct-token-42")
        wrong = live.request(
            "GET", "/api/v1/sessions", headers={"Authorization": "Bearer wrong"}
        )
        assert wrong.status == 401
        right = live.request(
            "GET", "/api/v1/sessions", headers={"Authorization": "Bearer correct-token-42"}
        )
        assert right.status == 200

    def test_post_body_token_channel(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "body-token-1")
        ok = live.request(
            "POST",
            "/api/v1/sessions",
            body=json.dumps({"token": "body-token-1"}).encode(),
            headers={"Content-Type": "application/json"},
        )
        assert ok.status == 200
        bad = live.request(
            "POST",
            "/api/v1/sessions",
            body=json.dumps({"token": "nope"}).encode(),
            headers={"Content-Type": "application/json"},
        )
        assert bad.status == 401

    def test_query_token_only_for_sse(self, env: FakeEnv, live: LiveServer) -> None:
        """URL access_token 仅 SSE 端点放行;其余端点 query 通道=401(AC1)。"""
        _write_token(env, "q-token")
        non_sse = live.request("GET", "/api/v1/sessions?access_token=q-token")
        assert non_sse.status == 401
        sse = live.request("GET", "/api/v1/push/messages?access_token=q-token")
        assert sse.status == 200
        assert sse.getheader("Content-Type", "").startswith("text/event-stream")

    def test_hot_reload_rotate_and_revoke(self, env: FakeEnv, live: LiveServer) -> None:
        """token 轮换/吊销热生效:无须重启(AC10 CI 面)。"""
        _write_token(env, "first-token")
        assert (
            live.request(
                "GET", "/api/v1/sessions", headers={"Authorization": "Bearer first-token"}
            ).status
            == 200
        )
        _write_token(env, "second-token")  # 轮换:旧 token 即刻 401
        assert (
            live.request(
                "GET", "/api/v1/sessions", headers={"Authorization": "Bearer first-token"}
            ).status
            == 401
        )
        assert (
            live.request(
                "GET", "/api/v1/sessions", headers={"Authorization": "Bearer second-token"}
            ).status
            == 200
        )
        _write_token(env, "")  # 吊销:全拒
        assert (
            live.request(
                "GET", "/api/v1/sessions", headers={"Authorization": "Bearer second-token"}
            ).status
            == 401
        )

    def test_broken_config_keeps_last_good_token(self, env: FakeEnv, live: LiveServer) -> None:
        """/health 如实加 config_error,不炸服务(AC/R2)。"""
        _write_token(env, "last-good")
        warm = live.request(
            "GET", "/api/v1/sessions", headers={"Authorization": "Bearer last-good"}
        )
        assert warm.status == 200  # 先让服务读到一次有效 token(落 last-good)
        config_path = env.data_root / "wechat-bridge" / "config.json"
        config_path.write_text("{broken json", encoding="utf-8")
        still = live.request(
            "GET", "/api/v1/sessions", headers={"Authorization": "Bearer last-good"}
        )
        assert still.status == 200  # 沿 last-good 继续服务
        health = json.loads(live.request("GET", "/api/v1/health").read())
        assert "config_error" in health["health"]

    def test_compare_digest_is_used_at_source_level(self) -> None:
        """源级守卫:常时比较必须在码(AC1)。"""
        source = Path(httpapi.__file__).read_text(encoding="utf-8")
        assert "hmac.compare_digest" in source


# =====================================================================
# CORS
# =====================================================================


class TestCors:
    def test_loopback_origin_gets_echo_headers(self, live: LiveServer) -> None:
        response = live.request(
            "GET", "/api/v1/health", headers={"Origin": "http://localhost:3000"}
        )
        assert response.status == 200
        assert response.getheader("Access-Control-Allow-Origin") == "http://localhost:3000"
        assert response.getheader("Vary") == "Origin"

    def test_foreign_origin_gets_no_cors_headers(self, live: LiveServer) -> None:
        response = live.request(
            "GET", "/api/v1/health", headers={"Origin": "https://evil.com"}
        )
        assert response.status == 200
        assert response.getheader("Access-Control-Allow-Origin") is None

    def test_preflight_same_rule(self, live: LiveServer) -> None:
        ok = live.request(
            "OPTIONS", "/api/v1/messages", headers={"Origin": "http://127.0.0.1:5173"}
        )
        assert ok.status == 204
        assert ok.getheader("Access-Control-Allow-Origin") == "http://127.0.0.1:5173"
        assert "OPTIONS" in (ok.getheader("Access-Control-Allow-Methods") or "")
        foreign = live.request(
            "OPTIONS", "/api/v1/messages", headers={"Origin": "https://evil.com"}
        )
        assert foreign.getheader("Access-Control-Allow-Origin") is None


# =====================================================================
# R3 回环守卫
# =====================================================================


class TestLoopbackGuard:
    @pytest.mark.parametrize("host", ["0.0.0.0", "192.168.1.5", "example.com", "::"])
    def test_non_loopback_rejected_exit_2(self, host: str) -> None:
        with pytest.raises(BridgeError) as excinfo:
            httpapi.validate_loopback_host(host)
        assert excinfo.value.exit_code == 2
        assert "红线" in excinfo.value.message

    @pytest.mark.parametrize("host", ["127.0.0.1", "localhost", "::1"])
    def test_loopback_allowed(self, host: str) -> None:
        httpapi.validate_loopback_host(host)

    def test_default_settings_bind_loopback(self, env: FakeEnv) -> None:
        settings = httpapi.effective_settings(env.config)
        assert settings == {"host": "127.0.0.1", "port": 5032}

    def test_run_serve_refuses_public_host_before_bind(
        self, env: FakeEnv, capsys: pytest.CaptureFixture[str]
    ) -> None:
        exit_code = httpapi.run_serve(host="0.0.0.0", data_root=env.data_root)
        assert exit_code == 2
        payload = json.loads(capsys.readouterr().out)
        assert payload["error"]["code"] == "usage"


# =====================================================================
# R4 端点同源(临时数据根 + 假副本;HTTP 应答 == CLI 编排载荷)
# =====================================================================


class TestEndpointsSameSource:
    def test_sessions_endpoint_matches_orchestration(
        self, env: FakeEnv, live: LiveServer
    ) -> None:
        _write_token(env, "t")
        expected = httpapi.sessions_list(
            env.config, env.storage, env.keys, 20, data_root=env.data_root
        )
        response = live.request(
            "GET", "/api/v1/sessions", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 200
        assert json.loads(response.read()) == expected

    def test_messages_endpoint_matches_query_history(
        self, env: FakeEnv, live: LiveServer
    ) -> None:
        _write_token(env, "t")
        expected = localdb.query_history(
            env.config, env.storage, env.keys, CHAT, 30, data_root=env.data_root
        )
        response = live.request(
            "GET",
            f"/api/v1/messages?chat_id={CHAT}",
            headers={"Authorization": "Bearer t"},
        )
        assert response.status == 200
        assert json.loads(response.read()) == expected

    def test_messages_endpoint_post_body_params(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "t")
        response = live.request(
            "POST",
            "/api/v1/messages",
            body=json.dumps({"token": "t", "chat_id": CHAT, "since_days": 1}).encode(),
            headers={"Content-Type": "application/json"},
        )
        assert response.status == 200
        payload = json.loads(response.read())
        assert payload["chat_id"] == CHAT
        assert payload["since_days"] == 1

    def test_group_info_endpoint_matches_orchestration(
        self, env: FakeEnv, live: LiveServer
    ) -> None:
        _write_token(env, "t")
        expected = localdb.group_info(
            env.config, env.storage, env.keys, CHAT, data_root=env.data_root
        )
        response = live.request(
            "GET", "/api/v1/group-info?chat_id=filehelper",
            headers={"Authorization": "Bearer t"},
        )
        assert response.status == 200
        assert json.loads(response.read()) == expected

    def test_sns_endpoint_matches_orchestration(
        self, env: FakeEnv, live: LiveServer
    ) -> None:
        _write_token(env, "t")
        expected = localdb.sns_history(
            env.config, env.storage, env.keys, "feed", 3, data_root=env.data_root
        )
        response = live.request(
            "GET", "/api/v1/sns?mode=feed&since_days=3",
            headers={"Authorization": "Bearer t"},
        )
        assert response.status == 200
        assert json.loads(response.read()) == expected


class TestPullEndpoint:
    def test_two_page_pull_with_sync_block(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "t")
        since = NOW - 700
        headers = {"Authorization": "Bearer t"}
        first = json.loads(
            live.request(
                "GET",
                f"/api/v1/sessions/{CHAT}/messages?since={since}&limit=3",
                headers=headers,
            ).read()
        )
        assert first["chat_id"] == CHAT and first["since"] == since
        assert [m["ts"] for m in first["messages"]] == sorted(
            m["ts"] for m in first["messages"]
        )  # 升序
        assert len(first["messages"]) == 3
        assert first["sync"]["hasMore"] is True
        assert first["sync"]["nextOffset"] == 3
        assert first["sync"]["nextSince"] == since  # 翻页期 since 不动
        second = json.loads(
            live.request(
                "GET",
                f"/api/v1/sessions/{CHAT}/messages?since={since}&limit=3&offset=3",
                headers=headers,
            ).read()
        )
        assert len(second["messages"]) == 3  # 窗口内恰 6 行(40 天前被滤)
        # 取满 limit(3/3)→ hasMore 仍 true(是否还有下一页须再翻一页才知;
        # ChatLab 语义:取满=可能有更多)。第三页空 → 拉毕跳水位。
        assert second["sync"]["hasMore"] is True
        assert second["sync"]["nextOffset"] == 6
        third = json.loads(
            live.request(
                "GET",
                f"/api/v1/sessions/{CHAT}/messages?since={since}&limit=3&offset=6",
                headers=headers,
            ).read()
        )
        assert third["messages"] == []
        assert third["sync"]["hasMore"] is False
        assert third["sync"]["nextOffset"] == 0
        assert third["sync"]["nextSince"] == third["sync"]["watermark"]
        assert third["sync"]["watermark"] == max(
            m["ts"] for m in first["messages"] + second["messages"]
        )
        # 拉毕跳水位:nextSince 处再拉 = 空窗。
        fourth = json.loads(
            live.request(
                "GET",
                f"/api/v1/sessions/{CHAT}/messages?since={third['sync']['watermark']}&limit=3",
                headers=headers,
            ).read()
        )
        assert fourth["messages"] == [] and fourth["sync"]["hasMore"] is False

    def test_cross_check_with_direct_sqlite(self, env: FakeEnv, live: LiveServer) -> None:
        """行数与 sqlite3 直查 COUNT 交叉核对(AC5 的 CI 假库版)。"""
        _write_token(env, "t")
        since = NOW - 700
        payload = json.loads(
            live.request(
                "GET",
                f"/api/v1/sessions/{CHAT}/messages?since={since}&limit=5000",
                headers={"Authorization": "Bearer t"},
            ).read()
        )
        con = sqlite3.connect(
            f"file:{env.copies_dir / 'message' / 'message_0.db'}?mode=ro", uri=True
        )
        (count,) = con.execute(
            f'SELECT COUNT(*) FROM "{CHAT_TABLE}" WHERE create_time > ?', (since,)
        ).fetchone()
        con.close()
        assert len(payload["messages"]) == count == 6
        assert payload["sync"]["watermark"] == NOW - 600 + 60


class TestParamAndRouteErrors:
    def test_missing_chat_id_is_400_usage(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "t")
        response = live.request(
            "GET", "/api/v1/messages", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 400
        assert json.loads(response.read())["error"]["code"] == "usage"

    @pytest.mark.parametrize(
        "path",
        [
            "/api/v1/messages?chat_id=x&limit=0",
            "/api/v1/messages?chat_id=x&limit=1001",
            "/api/v1/messages?chat_id=x&since_days=0",
            "/api/v1/sessions?limit=201",
            "/api/v1/sns?mode=bogus",
            "/api/v1/sessions/x/messages?since=abc",
            "/api/v1/sessions/x/messages?since=1&limit=5001",
            "/api/v1/sessions/x/messages?since=1&offset=-1",
        ],
    )
    def test_shape_errors_are_400(self, env: FakeEnv, live: LiveServer, path: str) -> None:
        _write_token(env, "t")
        response = live.request(
            "GET", path, headers={"Authorization": "Bearer t"}
        )
        assert response.status == 400, path

    def test_bad_json_body_is_400(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "t")
        response = live.request(
            "POST",
            "/api/v1/messages",
            body=b"{not-json",
            headers={"Authorization": "Bearer t", "Content-Type": "application/json"},
        )
        assert response.status == 400

    def test_unknown_route_is_404(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "t")
        response = live.request(
            "GET", "/api/v1/unknown", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 404
        assert json.loads(response.read())["error"]["code"] == "not_found"

    def test_disallowed_methods_are_405(self, env: FakeEnv, live: LiveServer) -> None:
        _write_token(env, "t")
        head = live.request("HEAD", "/api/v1/health")
        assert head.status == 405  # do_HEAD 不存在 → 501 路径 → send_error 映射 405
        head.read()
        media = live.request(
            "POST", "/api/v1/media/ok.png", headers={"Authorization": "Bearer t"}
        )
        assert media.status == 405  # 媒体下发仅收 GET(R4 表)
        media.read()


# =====================================================================
# 错误映射(20/21/22 → 503 码名透传)
# =====================================================================


class TestErrorMapping:
    def test_key_unavailable_maps_503(self, env: FakeEnv, monkeypatch, live: LiveServer) -> None:
        _write_token(env, "t")
        monkeypatch.setattr(
            localdb,
            "resolve_keys",
            lambda *a, **k: (_ for _ in ()).throw(
                BridgeError(21, "密钥缺位(合成)", code=None)
            ),
        )
        response = live.request(
            "GET", "/api/v1/messages?chat_id=x", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 503
        payload = json.loads(response.read())
        assert payload["error"]["code"] == "key_unavailable"

    def test_db_not_found_maps_503(self, env: FakeEnv, monkeypatch, live: LiveServer) -> None:
        _write_token(env, "t")
        monkeypatch.setattr(
            localdb,
            "locate_db_storage",
            lambda **k: (_ for _ in ()).throw(BridgeError(20, "库根缺位(合成)")),
        )
        response = live.request(
            "GET", "/api/v1/sessions", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 503
        assert json.loads(response.read())["error"]["code"] == "db_not_found"

    def test_decrypt_failed_maps_503(self, env: FakeEnv, live: LiveServer) -> None:
        """删掉 message 副本 → 重建链(sqlcipher 缺席/假源不可解)→ 22 → 503。"""
        _write_token(env, "t")
        (env.copies_dir / "message" / "message_0.db").unlink()
        response = live.request(
            "GET", f"/api/v1/messages?chat_id={CHAT}", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 503
        assert json.loads(response.read())["error"]["code"] == "decrypt_failed"


# =====================================================================
# R7 路径穿越守卫(红线级)
# =====================================================================


class TestPathTraversal:
    @pytest.fixture()
    def media_env(self, env: FakeEnv, live: LiveServer) -> LiveServer:
        _write_token(env, "t")
        media_dir = httpapi.media_dir_path(env.data_root)
        media_dir.mkdir(parents=True, exist_ok=True)
        (media_dir / "ok.png").write_bytes(b"fake-png-bytes")
        # 数据根内造假密钥件:必须结构性不可达(AC8)。
        (env.data_root / "wechat-localdb" / "keys.json").write_text("{}")
        return live

    @pytest.mark.parametrize(
        "rel",
        [
            "../keys.json",
            "../../keys.json",
            "%2e%2e%2fkeys.json",
            "..%2fkeys.json",
            "%2e%2e/keys.json",
            "a/../../keys.json",
            "/etc/passwd",
            "%2fetc%2fpasswd",
            "ok.png/../../../keys.json",
            "sub/../ok.png",
            "",
        ],
    )
    def test_variants_unreachable_core(self, env: FakeEnv, rel: str) -> None:
        service = env.service()
        assert service.resolve_media_file(rel) is None

    def test_allowed_file_served(self, env: FakeEnv, media_env: LiveServer) -> None:
        response = media_env.request(
            "GET", "/api/v1/media/ok.png", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 200
        assert response.read() == b"fake-png-bytes"

    @pytest.mark.parametrize(
        "path",
        [
            "/api/v1/media/../../keys.json",
            "/api/v1/media/%2e%2e%2fkeys.json",
            "/api/v1/media/..%2f..%2fkeys.json",
            "/api/v1/media/%2e%2e%2f%2e%2e%2fwechat-bridge%2fconfig.json",
        ],
    )
    def test_variants_unreachable_over_socket(
        self, env: FakeEnv, media_env: LiveServer, path: str
    ) -> None:
        response = media_env.request(
            "GET", path, headers={"Authorization": "Bearer t"}, raw=True
        )
        assert response.status == 404, path
        response.read()

    def test_symlink_out_of_root_rejected(self, env: FakeEnv, media_env: LiveServer) -> None:
        media_dir = httpapi.media_dir_path(env.data_root)
        outside = env.root / "outside-secret.txt"
        outside.write_text("secret", encoding="utf-8")
        (media_dir / "link.png").symlink_to(outside)
        service = env.service()
        assert service.resolve_media_file("link.png") is None
        response = media_env.request(
            "GET", "/api/v1/media/link.png", headers={"Authorization": "Bearer t"}
        )
        assert response.status == 404
        response.read()

    def test_fake_keys_json_never_reachable(
        self, env: FakeEnv, media_env: LiveServer
    ) -> None:
        for path in (
            "/api/v1/media/keys.json",
            "/api/v1/media/../keys.json",
            "/api/v1/media/%2e%2e/decrypted/message/message_0.db",
        ):
            response = media_env.request(
                "GET", path, headers={"Authorization": "Bearer t"}, raw=True
            )
            assert response.status in (401, 404), path
            response.read()


# =====================================================================
# SSE(核心注入;免真等)
# =====================================================================


class TestSseCore:
    def test_sse_route_requires_token_with_query_channel(self, env: FakeEnv) -> None:
        service = env.service()
        response = service.handle("GET", "/api/v1/push/messages?access_token=nope", {}, b"")
        assert response.status == 401
        _write_token(env, "right")
        ok = service.handle("GET", "/api/v1/push/messages?access_token=right", {}, b"")
        assert ok.is_sse and ok.status == 200

    def test_replay_and_resume(self) -> None:
        hub = watermark.EventHub(now_fn=lambda: 1.0)
        hub.publish_all([{"type": "message.new", "ts": i} for i in range(5)])
        frames = list(
            watermark.sse_stream(hub, 2, poll_timeout=0.01, max_frames=4)
        )
        # Last-Event-ID=2 → 补发 3、4、5(不丢不重);重放毕无新事件 → 心跳注释帧。
        assert frames[0].startswith("id: 3\nevent: message\ndata: ")
        assert json.loads(frames[0].split("data: ", 1)[1])["ts"] == 2
        assert frames[1].startswith("id: 4\n")
        assert frames[2].startswith("id: 5\n")
        assert frames[3] == ": ping\n\n"

    def test_heartbeat_frames(self) -> None:
        hub = watermark.EventHub(now_fn=lambda: 1.0)
        frames = list(watermark.sse_stream(hub, None, poll_timeout=0.01, max_frames=2))
        assert frames == [": ping\n\n", ": ping\n\n"]

    def test_live_events_stream_after_replay(self) -> None:
        hub = watermark.EventHub(now_fn=lambda: 1.0)
        hub.publish({"ts": 1})
        seen: list[str] = []

        def pump() -> None:
            for frame in watermark.sse_stream(hub, None, poll_timeout=0.5, max_frames=2):
                seen.append(frame)

        thread = threading.Thread(target=pump, daemon=True)
        thread.start()
        time.sleep(0.05)
        hub.publish({"ts": 2})  # 活流事件经订阅队列到达(0.5s 等待窗内)
        thread.join(timeout=3)
        assert any('"ts": 2' in frame for frame in seen)

    def test_replay_buffer_evicts_by_count(self) -> None:
        hub = watermark.EventHub(max_events=10, ttl_seconds=600, now_fn=lambda: 1.0)
        hub.publish_all([{"ts": i} for i in range(15)])
        assert len(hub.events_after(0)) == 10  # 环形上限
        assert [eid for eid, _payload in hub.events_after(0)] == list(range(6, 16))

    def test_replay_buffer_evicts_by_ttl(self) -> None:
        clock = {"now": 1.0}
        hub = watermark.EventHub(max_events=100, ttl_seconds=60, now_fn=lambda: clock["now"])
        hub.publish({"ts": 1})
        clock["now"] = 120.0
        assert hub.events_after(0) == []  # 超期淘汰如实(重连过晚 → Pull 补)


# =====================================================================
# R1 就绪行 / serve 进程(真进程,临时端口)
# =====================================================================


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class TestServeProcess:
    def test_ready_line_then_sigterm_exit_zero(self, env: FakeEnv, tmp_path: Path) -> None:
        port = _free_port()
        proc = subprocess.Popen(
            [
                sys.executable,
                "-c",
                "import sys; from wechat_bridge.httpapi import run_serve;"
                f"sys.exit(run_serve(host='127.0.0.1', port={port}))",
            ],
            cwd=COMPONENT_SRC,
            env={**os.environ, "MYIA_HOME": str(env.data_root)},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            ready_line = proc.stdout.readline().strip()
            ready = json.loads(ready_line)
            assert ready["http_api"]["host"] == "127.0.0.1"
            assert ready["http_api"]["port"] == port
            assert ready["http_api"]["token_configured"] is False
            assert ready["http_api"]["version"]
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
            conn.request("GET", "/api/v1/health")
            response = conn.getresponse()
            assert response.status == 200
            response.read()
            conn.close()
        finally:
            proc.send_signal(signal.SIGTERM)
            proc.wait(timeout=15)
        assert proc.returncode == 0  # SIGTERM 干净退 exit 0(R1/AC)

    def test_bind_failure_is_exit_1_with_hint(
        self, env: FakeEnv, capsys: pytest.CaptureFixture[str]
    ) -> None:
        port = _free_port()
        with socket.socket() as blocker:  # 占住端口
            blocker.bind(("127.0.0.1", port))
            blocker.listen(1)
            exit_code = httpapi.run_serve(
                host="127.0.0.1", port=port, data_root=env.data_root
            )
        captured = capsys.readouterr().out
        assert exit_code == 1
        payload = json.loads(captured.strip())
        assert payload["error"]["code"] == "bind_failed"
        assert "端口" in payload["error"]["fix_hint"]


# =====================================================================
# R9 token 管理 CLI
# =====================================================================


class TestHttpTokenCommands:
    def test_generate_show_clear_lifecycle(self, env: FakeEnv) -> None:
        generated = httpapi.http_token_generate(data_root=env.data_root)
        assert generated["http_token"]["result"] == "generated"
        token = generated["http_token"]["token"]
        assert len(token) == generated["http_token"]["length"] == 43
        config_path = env.data_root / "wechat-bridge" / "config.json"
        assert config_path.is_file()
        assert (config_path.stat().st_mode & 0o777) == 0o600
        shown = httpapi.http_token_show(data_root=env.data_root)
        assert shown["http_token"]["configured"] is True
        assert shown["http_token"]["token"] == token
        cleared = httpapi.http_token_clear(data_root=env.data_root)
        assert cleared["http_token"]["result"] == "cleared"
        after = httpapi.http_token_show(data_root=env.data_root)
        assert after["http_token"]["configured"] is False
        assert after["http_token"]["token"] is None
        assert shown["http_token"]["token"] == token
        cleared = httpapi.http_token_clear(data_root=env.data_root)
        assert cleared["http_token"]["result"] == "cleared"
        after = httpapi.http_token_show(data_root=env.data_root)
        assert after["http_token"]["configured"] is False
        assert after["http_token"]["token"] is None

    def test_generate_rotates_hot(self, env: FakeEnv, live: LiveServer) -> None:
        first = httpapi.http_token_generate(data_root=env.data_root)["http_token"]["token"]
        assert (
            live.request(
                "GET", "/api/v1/sessions", headers={"Authorization": f"Bearer {first}"}
            ).status
            == 200
        )
        second = httpapi.http_token_generate(data_root=env.data_root)["http_token"]["token"]
        assert second != first
        assert (
            live.request(
                "GET", "/api/v1/sessions", headers={"Authorization": f"Bearer {first}"}
            ).status
            == 401
        )
        assert (
            live.request(
                "GET", "/api/v1/sessions", headers={"Authorization": f"Bearer {second}"}
            ).status
            == 200
        )


# =====================================================================
# /health 载荷
# =====================================================================


class TestHealth:
    def test_health_payload_shape(self, env: FakeEnv, live: LiveServer) -> None:
        payload = json.loads(live.request("GET", "/api/v1/health").read())
        health = payload["health"]
        assert health["state"] in {"ok", "key_missing", "key_stale", "db_missing"}
        assert health["state"] == "key_missing"  # 假数据根无 keys.json
        assert health["key_status"]["state"] == "missing"
        assert health["bridge_version"]
        assert isinstance(health["uptime_seconds"], int)

    def test_health_reports_db_missing(self, env: FakeEnv, monkeypatch, live: LiveServer) -> None:
        monkeypatch.setattr(
            localdb,
            "locate_db_storage",
            lambda **k: (_ for _ in ()).throw(BridgeError(20, "库根缺位(合成)")),
        )
        payload = json.loads(live.request("GET", "/api/v1/health").read())
        assert payload["health"]["state"] == "db_missing"


# =====================================================================
# AC9 grep 守卫(写/hook 端点词零混入 + 方法处理器仅三个 + 文档措辞)
# =====================================================================


class TestGrepGuards:
    BANNED_RE = re.compile(
        r"\b(DELETE|PUT|PATCH|block-delete|block_delete|install|uninstall)\b"
    )

    def test_httpapi_has_no_write_or_hook_endpoint_words(self) -> None:
        source = Path(httpapi.__file__).read_text(encoding="utf-8")
        hits = self.BANNED_RE.findall(source)
        assert not hits, f"写/hook 端点词混入 httpapi.py: {hits}(AC9)"

    def test_method_handlers_are_exactly_three(self) -> None:
        handlers = sorted(
            name
            for name in dir(httpapi._ApiRequestHandler)
            if name.startswith("do_")
        )
        assert handlers == ["do_GET", "do_OPTIONS", "do_POST"]

    def test_docs_have_no_realtime_wording(self) -> None:
        text = DOCS_FILE.read_text(encoding="utf-8")
        assert "实时" not in text, "文档禁「实时」字样(延迟口径=分钟级,AC7)"
        assert "分钟级" in text

    def test_access_log_carries_shape_only(
        self, env: FakeEnv, live: LiveServer, capsys: pytest.CaptureFixture
    ) -> None:
        _write_token(env, "shhh-token-secret")
        live.request("GET", "/api/v1/push/messages?access_token=shhh-token-secret")
        live.request("GET", "/api/v1/health")
        # 日志在服务线程写 stderr;给一点调度时间后收割。
        time.sleep(0.2)
        captured = capsys.readouterr().err
        assert "shhh-token-secret" not in captured, "访问日志不得携带 query 内 token"
        assert "/api/v1/push/messages" in captured  # method/path/status/耗时 形状在场
