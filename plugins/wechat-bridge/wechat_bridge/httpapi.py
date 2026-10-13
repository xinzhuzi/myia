"""本地库只读 HTTP API 服务核心(task 10-14-wechat-http-api;R1-R5/R7/R9/R10)。

``wechat-bridge localdb serve`` 的本体(独立受管组件进程内常驻;桌面 app 是
宿主之一而非本体,PRD R1 进程归属裁决)。**纯只读对外面**:一切端点读解密
副本,零微信进程干预、零写微信侧数据;MYIA 内部消费不走本面(维持一次性
CLI 子进程通道)。

接口形态锚 WeFlow ``docs/HTTP-API.md`` 的**语义**(127.0.0.1 绑定/token 三
通道+常时比较/未配置即全拒/GET+POST 统一/SSE 心跳+重放+Last-Event-ID 续传/
ChatLab Pull 水位协议),代码与文案**零拷贝**(其许可 CC BY-NC-SA 4.0,比
GPL 更不可沾——只借设计思想)。chatlog 血统的反面坑(默认全网卡绑定/零
token/CORS 全开带凭据)固化为守卫测试,不进实现。

核心结构(transport 无关,单测零 socket):

- :class:`HttpApiService.handle` —— (method, path, headers, body) →
  :class:`ApiResponse`;鉴权/路由/参数校验/错误映射全在这层。
- :class:`_ApiRequestHandler` —— stdlib ``ThreadingHTTPServer`` 薄适配
  (do_GET/do_POST/do_OPTIONS 三个方法处理器,别无其他;501→405 映射)。
- :func:`run_serve` —— R1 启动序:读配置 → 回环校验(R3)→ bind → stdout
  单行就绪 JSON → serve_forever;SIGTERM/Ctrl-C 干净退 exit 0。

服务内部消费同一套桥编排函数(:func:`wechat_bridge.localdb.query_history` /
``sns_history`` / ``group_info`` 等)——HTTP 应答与 CLI 应答**逐字段同源**,
不造第二套查询实现;唯二新数据面函数已按 PRD 终位平移并经 import 消费:

- :func:`wechat_bridge.localdb_query.query_messages_range`(R5 ChatLab Pull);
- :func:`wechat_bridge.localdb.sessions_list`(R4 会话编排,与 query_history
  同构自愈钩子)。

私有数据红线(prd 红线 6):访问日志只载形状(method/path 去 query——SSE 的
access_token 在 query 里,绝不落日志/status/耗时),零聊天内容零密钥;错误
消息只承载形状与指引。
"""

from __future__ import annotations

import hmac
import json
import mimetypes
import os
import re
import secrets
import signal
import socket
import sys
import threading
import time
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qs, unquote, urlsplit

from . import __version__, localdb, watermark
from .codes import (
    DB_NOT_FOUND,
    DECRYPT_FAILED,
    EXIT_GENERIC_FAILURE,
    EXIT_OK,
    KEY_UNAVAILABLE,
    BridgeError,
)
from .config import (
    BridgeConfig,
    default_config_path,
    load_config,
    save_config_key,
)
from .localdb import _ensure_copies_with_self_heal, sessions_list
from .localdb_query import (
    _apply_sender_display,
    _contact_pick_names,
    _open_copy,
    query_messages_range,
)

__all__ = [
    "HTTP_API_ENABLED_DEFAULT",
    "HTTP_API_HOST_DEFAULT",
    "HTTP_API_PORT_DEFAULT",
    "HTTP_API_TOKEN_DEFAULT",
    "LOOPBACK_HOSTS",
    "MEDIA_DIR_NAME",
    "ApiResponse",
    "HttpApiService",
    "effective_settings",
    "http_token_clear",
    "http_token_generate",
    "http_token_show",
    "media_dir_path",
    "query_messages_range",
    "read_http_api_token",
    "resolve_media_file",
    "run_serve",
    "sessions_list",
    "validate_loopback_host",
]

_BRIDGE_VERSION = __version__

# —— R10 配置缺省(封闭清单 4 键的唯一缺省出处;config.py 侧落键与
#    component.json config_defaults 由集成员同步,见任务 integrationSpec)——
#: ``http_api_enabled`` 缺省(仅桌面托管消费;显式 CLI 起服不读该键,R1)。
HTTP_API_ENABLED_DEFAULT = False
#: ``http_api_host`` 缺省(R3 回环强制;装载期不拒非回环,serve 面拒)。
HTTP_API_HOST_DEFAULT = "127.0.0.1"
#: ``http_api_port`` 缺省(刻意避开 5030/5031 chatlog 族端口,防同机相撞)。
HTTP_API_PORT_DEFAULT = 5032
#: ``http_api_token`` 缺省(空 = 未配置 = 非 health 全拒,R2)。
HTTP_API_TOKEN_DEFAULT = ""

#: R3 回环白名单(serve 面强制;``0.0.0.0``/公网地址 → exit 2)。
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})
#: 媒体下发白名单目录名(R7:只服务 <数据根>/wechat-localdb/http-media/ 内)。
MEDIA_DIR_NAME = "http-media"

_API_PREFIX = "/api/v1"
#: Pull 端点路径(session/<chat_id>/messages;chat_id 经 unquote 后匹配)。
_PULL_ROUTE_RE = re.compile(r"^/api/v1/sessions/([^/]+)/messages$")
#: CORS 回环 Origin 判定用的 host 集(任意端口;R2)。
_CORS_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
_MEDIA_PREFIX = f"{_API_PREFIX}/media/"
_SSE_PATH = f"{_API_PREFIX}/push/messages"


# =====================================================================
# 设置/回环守卫/token(R1/R2/R3/R9)
# =====================================================================


def effective_settings(
    config: BridgeConfig | Any,
    *,
    host_override: str | None = None,
    port_override: int | None = None,
) -> dict[str, Any]:
    """生效 host/port:CLI flags > 配置键(集成期经 getattr 兼容取键)> 缺省。

    集成前 ``BridgeConfig`` 尚无 ``http_api_*`` 字段(config.py 加法在
    integrationSpec),``getattr`` 缺省回落本模块常量——前后行为一致。
    """
    host = (host_override or "").strip() or getattr(
        config, "http_api_host", HTTP_API_HOST_DEFAULT
    ) or HTTP_API_HOST_DEFAULT
    port = port_override if port_override is not None else getattr(
        config, "http_api_port", HTTP_API_PORT_DEFAULT
    )
    try:
        port_value = int(port)
    except (TypeError, ValueError) as exc:
        raise BridgeError(
            2,
            f"http_api_port 须为 1..65535 正整数,当前为 {port!r}",
            code="usage",
        ) from exc
    if not 1 <= port_value <= 65535:
        raise BridgeError(
            2,
            f"http_api_port 须为 1..65535 正整数,当前为 {port_value}",
            code="usage",
        )
    return {"host": str(host), "port": port_value}


def validate_loopback_host(host: str) -> None:
    """R3 回环绑定强制(红线级):host ∉ 回环白名单 → BridgeError exit 2。

    文案注明对外暴露解密聊天数据是红线 + chatlog 族判例;配置装载期不拒
    非回环字符串(坏值不许炸无关命令,判例同 key_provider_path),只在
    serve 面拒绝。
    """
    value = (host or "").strip()
    if value in LOOPBACK_HOSTS:
        return
    raise BridgeError(
        2,
        f"http_api_host 须为本机回环地址({sorted(LOOPBACK_HOSTS)}),当前为 {value!r}:"
        "对外暴露解密聊天数据是红线(chatlog 族收函/下架判例在案,prd Constraints)",
        code="usage",
        fix_hint="仅本机回环可用;外部系统经反向代理/SSH 隧道自担其责地转发 127.0.0.1",
    )


def media_dir_path(data_root: Path | None = None) -> Path:
    """媒体下发白名单目录(R7:<数据根>/wechat-localdb/http-media/,700)。"""
    return watermark.watermark_path(data_root).parent / MEDIA_DIR_NAME


def read_http_api_token(
    config_path: Path | None = None, *, data_root: Path | None = None
) -> tuple[str | None, str | None]:
    """热读 ``http_api_token``(每请求重读配置文件,R2 token 热生效)。

    Returns:
        ``(token, config_error)``:token = ``""`` 表未配置(合法态);``None``
        表配置文件不可读/形状异常——调用方沿 last-good token 继续服务并把
        ``config_error`` 注记进 /health(不炸服务不静默)。**不经
        :func:`load_config`**(它对未知键 fail-fast,且冷启动后配置损坏不应
        拖垮已在跑的鉴权)。
    """
    path = config_path if config_path is not None else default_config_path(data_root)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return HTTP_API_TOKEN_DEFAULT, None  # 缺文件 = 未配置(非错误)
    except (OSError, ValueError) as exc:
        return None, f"配置文件不可读({type(exc).__name__});鉴权沿上次有效 token"
    if not isinstance(raw, dict):
        return None, "配置文件顶层形状异常;鉴权沿上次有效 token"
    value = raw.get("http_api_token")
    if value is None or value == "":
        return HTTP_API_TOKEN_DEFAULT, None
    if isinstance(value, str):
        return value, None
    return None, "http_api_token 形状异常(须为字符串);鉴权沿上次有效 token"


# =====================================================================
# 应答核心(transport 无关)
# =====================================================================


@dataclass(frozen=True)
class ApiResponse:
    """服务核心应答(status/headers/body;SSE 以 ``is_sse`` 标记交适配层泵流)。"""

    status: int
    body: bytes = b""
    headers: tuple[tuple[str, str], ...] = ()
    content_type: str = "application/json; charset=utf-8"
    is_sse: bool = False
    sse_last_event_id: int | None = None


def _json_response(payload: Any, status: int = 200) -> ApiResponse:
    body = json.dumps(payload, ensure_ascii=False, indent=1) + "\n"
    return ApiResponse(status=status, body=body.encode("utf-8"))


def _error_response(
    code: str, message: str, fix_hint: str | None = None, status: int = 400
) -> ApiResponse:
    error: dict[str, str] = {"code": code, "message": message}
    if fix_hint:
        error["fix_hint"] = fix_hint
    return _json_response({"error": error}, status=status)


class HttpApiService:
    """R2-R7 服务核心:鉴权/路由/参数/错误映射 + 端点编排(同源直调桥件)。"""

    def __init__(
        self,
        *,
        config: Any,
        host: str,
        port: int,
        config_path: Path | None = None,
        data_root: Path | None = None,
        files_root: Path | None = None,
        hub: watermark.EventHub | None = None,
        now_fn: Any = time.time,
        version: str = _BRIDGE_VERSION,
    ) -> None:
        self.config = config
        self.host = host
        self.port = port
        self.config_path = config_path
        self.data_root = data_root
        self.files_root = files_root
        self.hub = hub if hub is not None else watermark.EventHub()
        self.now_fn = now_fn
        self.version = version
        self.started_at = now_fn()
        self.shutdown_event = threading.Event()
        self._token_lock = threading.Lock()
        self._last_good_token = ""
        self._config_error: str | None = None
        media_dir = media_dir_path(data_root)
        media_dir.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(media_dir, 0o700)  # R7:服务自有缓存目录 700
        except OSError:  # pragma: no cover - 非 POSIX 文件系统
            pass

    # —— R2 token 热生效(每请求重读;坏配置沿 last-good,/health 注记)——
    def _current_token(self) -> str:
        token, config_error = read_http_api_token(
            self.config_path, data_root=self.data_root
        )
        with self._token_lock:
            if token is not None:
                self._last_good_token = token
                self._config_error = None
            if config_error:
                self._config_error = config_error
            return self._last_good_token

    def _config_error_snapshot(self) -> str | None:
        with self._token_lock:
            return self._config_error

    def _authorized(
        self,
        headers: Mapping[str, str],
        query: dict[str, Any],
        body_params: dict[str, Any],
        *,
        is_sse: bool,
    ) -> bool:
        """R2 三通道:Bearer 头(全端点)/ POST body ``token``(全端点)/
        URL ``access_token``(**仅 SSE**——EventSource 不能设头);常时比较
        :func:`hmac.compare_digest`(对位 WeFlow timingSafeEqual,stdlib)。"""
        expected = self._current_token()
        if not expected:
            return False  # 未配置 = 全拒(防裸奔),错误体由调用方给 fix_hint
        candidates: list[str] = []
        auth_value = headers.get("authorization") or ""
        if auth_value.startswith("Bearer "):
            candidates.append(auth_value[len("Bearer "):].strip())
        body_token = body_params.get("token")
        if isinstance(body_token, str) and body_token:
            candidates.append(body_token)
        if is_sse:
            query_token = query.get("access_token")
            if isinstance(query_token, str) and query_token:
                candidates.append(query_token)
        expected_bytes = expected.encode("utf-8")
        return any(
            hmac.compare_digest(candidate.encode("utf-8"), expected_bytes)
            for candidate in candidates
        )

    def _unauthorized_response(self) -> ApiResponse:
        if not self._current_token():
            return _error_response(
                "unauthorized",
                "未配置访问 token:本机接口默认全拒(防裸奔)",
                fix_hint="wechat-bridge localdb http-token generate --json 生成 token"
                "后重试(热生效,无须重启服务);文档 docs/wechat-http-api.md",
                status=401,
            )
        return _error_response(
            "unauthorized",
            "token 不符(Bearer 头 / POST body token;SSE 端点另收 URL access_token)",
            fix_hint="核对 token:wechat-bridge localdb http-token show --json 本机查看",
            status=401,
        )

    # —— 定位/取钥(缺省 = 桥既有编排;单测经 monkeypatch localdb 模块注入)——
    def _locate(self) -> Path:
        return localdb.locate_db_storage(files_root=self.files_root)

    def _resolve(self, storage: Path) -> dict[str, str]:
        return localdb.resolve_keys(
            storage, config=self.config, data_root=self.data_root
        )

    # —— R4 端点编排(同源直调;错误族由 handle 统一映射)——
    def _payload_sessions(self, params: dict[str, Any]) -> ApiResponse:
        limit = _int_param(params, "limit", 20, 1, 200)
        storage = self._locate()
        keys = self._resolve(storage)
        return _json_response(
            sessions_list(
                self.config, storage, keys, limit, data_root=self.data_root
            )
        )

    def _payload_messages(self, params: dict[str, Any]) -> ApiResponse:
        chat_id = _str_param(params, "chat_id")
        days = _int_param(params, "since_days", 30, 1, 3650)
        limit = _int_param(
            params, "limit", int(getattr(self.config, "messages", 50)), 1, 1000
        )
        storage = self._locate()
        keys = self._resolve(storage)
        payload = localdb.query_history(
            self.config, storage, keys, chat_id, days, data_root=self.data_root
        )
        return _json_response(payload)

    def pull_messages(
        self,
        chat_id: str,
        since: int,
        end: int | None,
        limit: int,
        offset: int,
    ) -> dict[str, Any]:
        """ChatLab Pull 编排(R4/R5):[message,contact] 副本 → 升序增量 +
        sync 块;发送者上屏名与 run_query 同款(contact 域批量解析)。"""
        storage = self._locate()
        keys = self._resolve(storage)
        copy_info, _keys = _ensure_copies_with_self_heal(
            self.config, storage, keys, ["message", "contact"], data_root=self.data_root
        )
        copy_dir = Path(str(copy_info["dir"]))
        con = None
        for rel in ("message/message_0.db", "message/biz_message_0.db"):
            con = _open_copy(copy_dir, rel)
            if con is not None:
                break
        if con is None:
            raise BridgeError(
                DECRYPT_FAILED,
                "message 域解密副本不可用(副本缺失或损坏;G5 重建流程未产出可用库)",
                fix_hint="重试触发副本重建;持续失败先核密钥与 sqlcipher(design §5.1)",
            )
        try:
            messages, sync = query_messages_range(
                con, chat_id, since, end, limit=limit, offset=offset
            )
        finally:
            con.close()
        contact_con = _open_copy(copy_dir, "contact/contact.db")
        if contact_con is not None:
            try:
                senders = [
                    m.get("sender")
                    for m in messages
                    if isinstance(m.get("sender"), str)
                ]
                _apply_sender_display(messages, _contact_pick_names(contact_con, senders))
            finally:
                contact_con.close()
        return {"chat_id": chat_id, "since": int(since), "messages": messages, "sync": sync}

    def _payload_pull(self, chat_id: str, params: dict[str, Any]) -> ApiResponse:
        since = _int_param(params, "since", None, 0, None)
        end = _optional_int_param(params, "end", 0)
        limit = _int_param(params, "limit", 500, 1, 5000)
        offset = _int_param(params, "offset", 0, 0, None)
        return _json_response(self.pull_messages(chat_id, since, end, limit, offset))

    def _payload_group_info(self, params: dict[str, Any]) -> ApiResponse:
        chat_id = _str_param(params, "chat_id")
        storage = self._locate()
        keys = self._resolve(storage)
        return _json_response(
            localdb.group_info(
                self.config, storage, keys, chat_id, data_root=self.data_root
            )
        )

    def _payload_sns(self, params: dict[str, Any]) -> ApiResponse:
        mode = params.get("mode", "feed")
        if mode not in ("feed", "notices"):
            raise BridgeError(
                2, f"mode 须为 feed|notices,当前为 {mode!r}", code="usage"
            )
        days = _int_param(params, "since_days", 3, 1, 3650)
        storage = self._locate()
        keys = self._resolve(storage)
        return _json_response(
            localdb.sns_history(
                self.config, storage, keys, mode, days, data_root=self.data_root
            )
        )

    def _health(self) -> ApiResponse:
        """/health(token 豁免,恒 200;chatlog DB 状态中间件语义:健康面
        如实暴露后端生命周期)。"""
        state = "ok"
        try:
            self._locate()
        except BridgeError:
            state = "db_missing"
        key_status_payload = localdb.key_status(
            data_root=self.data_root, files_root=self.files_root
        )
        inner = key_status_payload.get("key_status", {})
        if state != "db_missing":
            state = {
                "ready": "ok",
                "missing": "key_missing",
                "stale": "key_stale",
            }.get(str(inner.get("state")), "ok")
        health: dict[str, Any] = {
            "state": state,
            "key_status": inner,
            "bridge_version": self.version,
            "uptime_seconds": max(0, int(self.now_fn() - self.started_at)),
        }
        config_error = self._config_error_snapshot()
        if config_error:
            health["config_error"] = config_error
        return _json_response({"health": health})

    # —— R7 媒体白名单(路径穿越守卫,红线级)——
    def resolve_media_file(self, rel: str) -> Path | None:
        """``rel`` → 白名单目录内文件绝对路径;任何越界形状 → None(404)。

        判序(unquote **之后**校验——``%2e%2e%2f`` 先还原再判,不留编码盲区):
        拒绝对路径/反斜杠/空段/``..`` 段 → ``realpath`` 双重校验(realpath
        解析符号链接,出根即拒)→ 必须是常规文件。目录外(含 ``decrypted/``
        ``keys.json`` 配置文件)结构性不可达。
        """
        if not rel:
            return None
        if rel.startswith("/") or rel.startswith("\\") or "\\" in rel or "\x00" in rel:
            return None
        parts = rel.split("/")
        if any(part in ("", "..", ".") for part in parts):
            return None
        media_dir = media_dir_path(self.data_root)
        root_real = os.path.realpath(media_dir)
        candidate_real = os.path.realpath(media_dir.joinpath(*parts))
        if candidate_real == root_real or not candidate_real.startswith(
            root_real + os.sep
        ):
            return None
        if not os.path.isfile(candidate_real):
            return None
        return Path(candidate_real)

    def _media_response(self, rel: str) -> ApiResponse:
        resolved = self.resolve_media_file(rel)
        if resolved is None:
            return _error_response(
                "not_found",
                "媒体文件不存在或不在服务目录内(http-media/ 白名单)",
                status=404,
            )
        try:
            data = resolved.read_bytes()
        except OSError:
            return _error_response("not_found", "媒体文件不可读", status=404)
        guessed = mimetypes.guess_type(resolved.name)[0] or "application/octet-stream"
        return ApiResponse(
            status=200, body=data, content_type=guessed
        )

    # —— R2 CORS(仅回环 Origin 回头;其余 Origin 不回任何 CORS 头)——
    @staticmethod
    def cors_headers(headers: Mapping[str, str]) -> tuple[tuple[str, str], ...]:
        lowered = {str(k).lower(): str(v) for k, v in headers.items()}
        origin = (lowered.get("origin") or "").strip()
        if not origin:
            return ()
        host = urlsplit(origin).hostname or ""
        if host.lower() not in _CORS_HOSTS:
            return ()
        return (
            ("Access-Control-Allow-Origin", origin),
            ("Vary", "Origin"),
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
            ("Access-Control-Allow-Headers", "Authorization, Content-Type"),
        )

    # —— 路由总入口 ——
    def handle(
        self,
        method: str,
        raw_path: str,
        headers: Mapping[str, str],
        body: bytes = b"",
    ) -> ApiResponse:
        """(method, path, headers, body) → 应答;零 socket,单测直驱。"""
        normalized = {str(k).lower(): str(v) for k, v in headers.items()}
        try:
            return self._route(method, raw_path, normalized, body)
        except BridgeError as exc:
            if exc.exit_code in (DB_NOT_FOUND, KEY_UNAVAILABLE, DECRYPT_FAILED):
                return _json_response({"error": exc.to_payload()}, status=503)
            return _json_response({"error": exc.to_payload()}, status=400)
        except Exception as exc:  # noqa: BLE001 - 未预期异常:500 + 形状日志
            _diag(f"httpapi: 未预期异常({type(exc).__name__})")
            return _error_response(
                "internal", "服务内部错误(未预期异常;日志只载形状)", status=500
            )

    def _route(
        self,
        method: str,
        raw_path: str,
        headers: Mapping[str, str],
        body: bytes,
    ) -> ApiResponse:
        split = urlsplit(raw_path)
        path = unquote(split.path)
        query = {
            key: values[-1]
            for key, values in parse_qs(split.query, keep_blank_values=True).items()
        }
        body_params: dict[str, Any] = {}
        if method == "POST" and body:
            try:
                parsed_body = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, ValueError) as exc:
                raise BridgeError(
                    2, f"POST body 须为合法 JSON 对象({type(exc).__name__})", code="usage"
                ) from exc
            if not isinstance(parsed_body, dict):
                raise BridgeError(2, "POST body 须为 JSON 对象", code="usage")
            body_params = parsed_body
        params: dict[str, Any] = {**query, **body_params}  # POST body 参数并入(同名覆盖)

        if method == "OPTIONS":
            # CORS 头由适配层统一补(此处零头;204 预检应答)。
            return ApiResponse(status=204, body=b"")
        if method not in ("GET", "POST"):
            return _error_response(
                "method_not_allowed",
                f"方法 {method} 不在允许集(GET/POST/OPTIONS)",
                status=405,
            )

        if path == f"{_API_PREFIX}/health":
            return self._health()

        is_sse = path == _SSE_PATH
        if not self._authorized(headers, query, body_params, is_sse=is_sse):
            denied = self._unauthorized_response()
            return ApiResponse(
                status=denied.status,
                body=denied.body,
                headers=self.cors_headers(headers) + denied.headers,
                content_type=denied.content_type,
            )

        pull_match = _PULL_ROUTE_RE.fullmatch(path)
        if path == f"{_API_PREFIX}/sessions":
            return self._payload_sessions(params)
        if path == f"{_API_PREFIX}/messages":
            return self._payload_messages(params)
        if pull_match:
            return self._payload_pull(unquote(pull_match.group(1)), params)
        if path == f"{_API_PREFIX}/group-info":
            return self._payload_group_info(params)
        if path == f"{_API_PREFIX}/sns":
            return self._payload_sns(params)
        if path.startswith(_MEDIA_PREFIX):
            if method != "GET":
                return _error_response(
                    "method_not_allowed", "媒体下发仅收 GET", status=405
                )
            return self._media_response(path[len(_MEDIA_PREFIX):])
        if is_sse:
            last_event_id = _parse_last_event_id(headers.get("last-event-id"))
            return ApiResponse(
                status=200,
                is_sse=True,
                sse_last_event_id=last_event_id,
                headers=(
                    ("Content-Type", "text/event-stream; charset=utf-8"),
                    ("Cache-Control", "no-store"),
                ),
            )
        return _error_response(
            "not_found", f"未知路由: {path}(端点族谱见 docs/wechat-http-api.md)", status=404
        )


def _parse_last_event_id(raw: str | None) -> int | None:
    if raw is None or not str(raw).strip():
        return None
    try:
        return int(str(raw).strip())
    except ValueError:
        return None


def _int_param(
    params: dict[str, Any],
    name: str,
    default: int | None,
    lo: int | None,
    hi: int | None,
) -> int:
    """整型参数校验(缺省/区间;形状错 = usage → HTTP 400,PRD R4)。"""
    raw = params.get(name, default)
    if raw is None:
        raise BridgeError(2, f"缺少必填参数: {name}", code="usage")
    if isinstance(raw, bool):
        raise BridgeError(2, f"参数 {name} 须为整数,当前为布尔", code="usage")
    try:
        value = int(raw)
    except (TypeError, ValueError) as exc:
        raise BridgeError(
            2, f"参数 {name} 须为整数,当前为 {raw!r}", code="usage"
        ) from exc
    if lo is not None and value < lo:
        raise BridgeError(2, f"参数 {name} 须 ≥ {lo},当前为 {value}", code="usage")
    if hi is not None and value > hi:
        raise BridgeError(2, f"参数 {name} 须 ≤ {hi},当前为 {value}", code="usage")
    return value


def _optional_int_param(
    params: dict[str, Any], name: str, lo: int | None = None
) -> int | None:
    if name not in params or params[name] in (None, ""):
        return None
    return _int_param(params, name, None, lo, None)


def _str_param(params: dict[str, Any], name: str) -> str:
    value = params.get(name)
    if not isinstance(value, str) or not value.strip():
        raise BridgeError(2, f"缺少必填参数: {name}(非空字符串)", code="usage")
    return value.strip()


def _diag(message: str) -> None:
    """stderr 摘要行(形状级;零聊天内容零密钥,红线 6)。"""
    try:
        sys.stderr.write(message + "\n")
    except OSError:  # pragma: no cover - stderr 关闭的极端形态
        pass


# =====================================================================
# stdlib HTTP 适配层(ThreadingHTTPServer;方法处理器仅三个)
# =====================================================================


class _ApiRequestHandler(BaseHTTPRequestHandler):
    """薄适配:核心 :meth:`HttpApiService.handle` ↔ socket。

    方法处理器**只有** do_GET/do_POST/do_OPTIONS(AC9 grep 守卫);其余方法
    走 BaseHTTPRequestHandler 的 501 路径,经 :meth:`send_error` 覆写映射
    405(R4)。访问日志 :meth:`log_request` 只载形状(method/path 去 query
    ——SSE 的 access_token 在 query 里绝不落日志/status/耗时)。
    """

    service: HttpApiService  # 由 build_server 绑定(每服务一个子类实例)
    protocol_version = "HTTP/1.0"  # SSE 无 Content-Length,连接级关闭语义

    def do_GET(self) -> None:  # noqa: N802 - http.server 命名约定
        self._dispatch("GET")

    def do_POST(self) -> None:  # noqa: N802
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        body = self.rfile.read(length) if length > 0 else b""
        self._dispatch("POST", body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._dispatch("OPTIONS")

    def _dispatch(self, method: str, body: bytes = b"") -> None:
        self._request_started = time.time()
        response = self.service.handle(method, self.path, dict(self.headers), body)
        try:
            if response.is_sse:
                self._send_sse(response)
            else:
                self._send(response)
        except (BrokenPipeError, ConnectionResetError):
            self.close_connection = True

    def _send(self, response: ApiResponse) -> None:
        self.send_response(response.status)
        for key, value in self.service.cors_headers(dict(self.headers)):
            self.send_header(key, value)
        for key, value in response.headers:
            self.send_header(key, value)
        self.send_header("Content-Type", response.content_type)
        self.send_header("Content-Length", str(len(response.body)))
        if response.status == 401:
            self.send_header("WWW-Authenticate", 'Bearer realm="wechat-bridge"')
        if response.status == 405:
            self.send_header("Allow", "GET, POST, OPTIONS")
        self.end_headers()
        if response.body:
            self.wfile.write(response.body)

    def _send_sse(self, response: ApiResponse) -> None:
        self.send_response(response.status)
        for key, value in self.service.cors_headers(dict(self.headers)):
            self.send_header(key, value)
        for key, value in response.headers:
            self.send_header(key, value)
        self.end_headers()
        for frame in watermark.sse_stream(
            self.service.hub,
            response.sse_last_event_id,
            stop_event=self.service.shutdown_event,
        ):
            self.wfile.write(frame.encode("utf-8"))
            self.wfile.flush()

    def send_error(  # noqa: D401 - http.server 签名
        self, code: int, message: str | None = None, explain: str | None = None
    ) -> None:
        """协议层错误统一 JSON 错误体;501(未实现方法)→ 405(R4)。"""
        status = 405 if code == 501 else code
        error_code = "method_not_allowed" if code == 501 else "bad_request"
        payload = json.dumps(
            {"error": {"code": error_code, "message": message or ""}},
            ensure_ascii=False,
        ).encode("utf-8")
        try:
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            if code == 501:
                self.send_header("Allow", "GET, POST, OPTIONS")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):  # pragma: no cover
            self.close_connection = True

    def log_request(self, code: int | str = "-", size: int | str = "-") -> None:
        """访问日志(R1:stderr,只载形状;path 去 query,零内容零密钥)。"""
        path_only = self.path.split("?", 1)[0]
        elapsed_ms = int((time.time() - getattr(self, "_request_started", time.time())) * 1000)
        _diag(f"httpapi {self.command} {path_only} {code} {elapsed_ms}ms")

    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: D401
        pass  # 默认访问行已由 log_request 形状化接管;别无他话

    def log_error(self, fmt: str, *args: Any) -> None:  # noqa: D401
        pass  # 协议层错误细节不落日志(send_error 已结构化应答)


class _HttpApiServer(ThreadingHTTPServer):
    """ThreadingHTTPServer(daemon_threads;``::1`` 绑定切 AF_INET6)。"""

    daemon_threads = True

    def __init__(
        self, address: tuple[str, int], handler: type[BaseHTTPRequestHandler]
    ) -> None:
        if ":" in address[0]:
            self.address_family = socket.AF_INET6
        super().__init__(address, handler)


def build_server(service: HttpApiService, settings: Mapping[str, Any]) -> _HttpApiServer:
    """bind(失败抛 OSError,由 run_serve 转 exit 1 结构化错误)。"""
    handler = type("_BoundApiHandler", (_ApiRequestHandler,), {"service": service})
    return _HttpApiServer((settings["host"], int(settings["port"])), handler)


# =====================================================================
# R1 serve 入口(CLI 子命令体;argparse 装配在 cli.py,集成员接线)
# =====================================================================


def run_serve(
    *,
    config_path: Path | None = None,
    host: str | None = None,
    port: int | None = None,
    data_root: Path | None = None,
    files_root: Path | None = None,
) -> int:
    """``localdb serve`` 全链:读配置 → 回环校验 → bind → 就绪 JSON → 常驻。

    前台常驻(daemonize 属集成点,PRD R1);SIGTERM/Ctrl-C 干净退 exit 0;
    bind 失败 = exit 1 结构化错误(端口占用指引);非回环 host = exit 2。
    """
    resolved_config_path = (
        config_path if config_path is not None else default_config_path(data_root)
    )
    try:
        config = load_config(config_path)
        settings = effective_settings(config, host_override=host, port_override=port)
        validate_loopback_host(settings["host"])
    except BridgeError as exc:
        sys.stdout.write(
            json.dumps({"error": exc.to_payload()}, ensure_ascii=False) + "\n"
        )
        sys.stdout.flush()
        return exc.exit_code
    service = HttpApiService(
        config=config,
        host=settings["host"],
        port=settings["port"],
        config_path=resolved_config_path,
        data_root=data_root,
        files_root=files_root,
    )
    try:
        server = build_server(service, settings)
    except OSError as exc:
        hint = "端口被占用:--port 换端口,或 lsof -nP -iTCP:%s 查占用方" % settings["port"]
        if getattr(exc, "errno", None) == 13:  # EACCES(特权端口等)
            hint = "端口无权限绑定:换 1024 以上端口(缺省 5032)"
        sys.stdout.write(
            json.dumps(
                {
                    "error": {
                        "code": "bind_failed",
                        "message": f"HTTP 服务绑定失败({type(exc).__name__}: {exc}): "
                        f"{settings['host']}:{settings['port']}",
                        "fix_hint": hint,
                    }
                },
                ensure_ascii=False,
            )
            + "\n"
        )
        sys.stdout.flush()
        return EXIT_GENERIC_FAILURE
    # 就绪单行 JSON(stdout;此后访问日志走 stderr,PRD R1)。
    ready = {
        "http_api": {
            "host": settings["host"],
            "port": settings["port"],
            "token_configured": bool(service._current_token()),
            "version": _BRIDGE_VERSION,
        }
    }
    sys.stdout.write(json.dumps(ready, ensure_ascii=False) + "\n")
    sys.stdout.flush()

    scanner = watermark.WatermarkScanner(
        hub=service.hub,
        config=config,
        data_root=service.data_root,
        files_root=files_root,
    )

    def _on_sigterm(_signum: int, _frame: Any) -> None:  # noqa: ANN001
        raise SystemExit(EXIT_OK)  # SIGTERM 干净退 exit 0(PRD R1)

    handler_installed = False
    previous_handler: Any = None
    try:
        previous_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, _on_sigterm)
        handler_installed = True
    except ValueError:
        pass  # 非主线程(库态调用):取消面交还调用方
    scanner.start()
    try:
        server.serve_forever(poll_interval=0.5)
    except (KeyboardInterrupt, SystemExit):
        pass  # Ctrl-C / SIGTERM:干净退,exit 0
    finally:
        service.shutdown_event.set()
        scanner.stop()
        server.server_close()
    return EXIT_OK


# =====================================================================
# R9 token 管理 CLI(localdb http-token;argparse 装配在 cli.py,集成员接线)
# =====================================================================


def http_token_generate(
    *, config_path: Path | None = None, data_root: Path | None = None
) -> dict[str, Any]:
    """generate:``secrets.token_urlsafe(32)`` → ``save_config_key`` 代写。

    再生成=轮换(旧 token 即刻失效——R2 每请求热重读,无须重启);应答
    明文 token **仅本次显示**(落盘的是配置文件,600 私有区)。
    """
    token = secrets.token_urlsafe(32)
    save_config_key("http_api_token", token, path=config_path, data_root=data_root)
    return {
        "http_token": {"result": "generated", "token": token, "length": len(token)}
    }


def http_token_show(
    *, config_path: Path | None = None, data_root: Path | None = None
) -> dict[str, Any]:
    """show:本机主人面(配置 600 私有区;未配置如实 false)。"""
    token, config_error = read_http_api_token(config_path, data_root=data_root)
    configured = bool(token)
    payload: dict[str, Any] = {
        "configured": configured,
        "token": token if configured else None,
        "length": len(token) if configured else 0,
    }
    if config_error:
        payload["config_error"] = config_error
    return {"http_token": payload}


def http_token_clear(
    *, config_path: Path | None = None, data_root: Path | None = None
) -> dict[str, Any]:
    """clear:吊销(=未配置态,一切非 health 401;热生效无须重启)。"""
    save_config_key("http_api_token", None, path=config_path, data_root=data_root)
    return {"http_token": {"result": "cleared"}}
