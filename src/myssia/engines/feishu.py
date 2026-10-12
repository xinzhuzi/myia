"""飞书群消息引擎(显式 ``engine: feishu``;10-12-feishu-ingest-engine).

官方 Open API 直读群消息:tenant_access_token 自 mint(凭据 = 推送区同一
自建应用,``FEISHU_APP_ID``/``FEISHU_APP_SECRET`` env 缺失回退钥匙链规范名
``myia/push/<键>`` —— 账号/机器人两线共凭据的裁定语义,10-11-platform-
account-config),群消息窗口拉取( ``GET /im/v1/chats/{chat_id}/messages``,
sort_type=ByCreateTimeDesc 最新一页),锚 ``#fs-<chat_id>-<message_id>``
全期幂等(管线 url 去重键,#tg- 同款)。

诚实边界(v1):
- 仅 ``msg_type=text`` 出条目(post/富媒体/合并转发等静默跳过 —— 群情报
  主体是文本;扩展面留 v2);
- 无粗筛/LLM 过滤(群量小,条目全进 feed,靠 watchlist 面收口);
- 应用缺 ``im:message`` 群消息只读权限、或机器人不在群内 → 结构化
  ``feishu_permission_denied``(主人侧动作:开放平台加权限 + 拉机器人进群),
  不伪装空态。
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from myssia.engines.fetch_base import BaseEngine, FetchError
from myssia.schema import resolve_credential, CredentialResolveError

logger = logging.getLogger(__name__)

API_HOST = "open.feishu.cn"
API_BASE = f"https://{API_HOST}/open-apis"
DEFAULT_LOOKBACK_LIMIT = 50
MAX_LOOKBACK_LIMIT = 100
#: 群消息只读权限缺失的典型 code(99991672=权限不足;230002=机器人不在群/
#: 无可见性)。其余 code 原样 feishu_api_error,不猜。
_PERMISSION_CODES = {99991672, 230002}


class FeishuEngine(BaseEngine):
    """飞书 Open API 群消息窗口源(显式 ``engine: feishu``;凭据复用推送区)."""

    LAYER = "OFFICIAL_OPEN_API"
    ENGINE_NAME = "feishu"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """engine_options.feishu 校验与缺省化(错型即结构化拒)."""
        options = self.engine_options()
        chat_id = options.get("chat_id")
        if (
            isinstance(chat_id, bool)
            or not isinstance(chat_id, str)
            or not chat_id.strip()
        ):
            raise FetchError(
                "engine_options.feishu.chat_id 应为群 chat_id(oc_ 前缀字符串,"
                f"消息屏目录或群设置可查),当前为 {chat_id!r}",
                error_type="invalid_engine_options",
            )
        lookback = options.get("lookback_limit", DEFAULT_LOOKBACK_LIMIT)
        if (
            isinstance(lookback, bool)
            or not isinstance(lookback, int)
            or not 1 <= lookback <= MAX_LOOKBACK_LIMIT
        ):
            raise FetchError(
                f"engine_options.feishu.lookback_limit 应为 "
                f"1-{MAX_LOOKBACK_LIMIT} 整数(单页窗口帽),当前为 {lookback!r}",
                error_type="invalid_engine_options",
            )
        result: dict[str, Any] = {
            "chat_id": chat_id.strip(),
            "lookback_limit": lookback,
            "app_id_ref": options.get("app_id_ref", "env:FEISHU_APP_ID"),
            "app_secret_ref": options.get("app_secret_ref", "env:FEISHU_APP_SECRET"),
        }
        return result

    def _parse_source_url(self) -> None:
        """源 URL 契约校验(零 I/O):``https://open.feishu.cn`` 锚形态."""
        from urllib.parse import urlsplit

        parsed = urlsplit(self.source.url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host != API_HOST or parsed.path not in ("", "/"):
            raise FetchError(
                f"feishu 引擎源 url 应为 https://{API_HOST} 锚形态"
                f"(路径留空;chat 配置在 engine_options.feishu.chat_id),"
                f"当前为 {self.source.url!r}",
                error_type="invalid_feishu_source_url",
            )

    def _app_credentials(self) -> tuple[str, str] | None:
        """解析应用凭据三态(None = 显式空态,由调用方落 skip).

        两级:env 优先(``env:FEISHU_APP_ID/SECRET``)→ 钥匙链规范名兜底
        ``keychain:myia/push/<ENV_KEY>``(推送区 GUI 表单落点;backend 用
        ``context.keychain_backend`` —— 生产管线不注入(None)= 系统钥匙串
        懒发现,telegram 的 keychain 引用同款机制;账号线复用机器人凭据
        的裁定语义)。
        """
        options = self._options()
        values: list[str] = []
        for env_key, fallback_ref in (
            ("FEISHU_APP_ID", "keychain:myia/push/FEISHU_APP_ID"),
            ("FEISHU_APP_SECRET", "keychain:myia/push/FEISHU_APP_SECRET"),
        ):
            value: str | None = None
            try:
                value = resolve_credential(f"env:{env_key}")
            except CredentialResolveError:
                pass  # env 缺失常态:转钥匙链兜底
            if not value or not value.strip():
                try:
                    value = resolve_credential(fallback_ref, backend=self.context.keychain_backend)
                except CredentialResolveError as exc:
                    logger.warning(
                        "feishu 凭据两路全缺 env=%s keychain=%s: %s",
                        env_key, fallback_ref, exc,
                    )
                    value = None
            if not value or not value.strip():
                return None
            values.append(value.strip())
        return values[0], values[1]

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        self._parse_source_url()
        options = self._options()
        credentials = self._app_credentials()
        if credentials is None:
            logger.warning(
                "feishu 应用凭据未配置,源降级为显式空态 source=%s"
                "(设置→推送录 feishu_card 凭据即通,账号线复用同一应用)",
                self.source.name,
            )
            self.last_skip_reason = "credential_missing"
            return []
        app_id, app_secret = credentials

        token = await self._mint_token(app_id, app_secret)
        return await self._read_messages(options["chat_id"], options["lookback_limit"], token)

    async def _mint_token(self, app_id: str, app_secret: str) -> str:
        """tenant_access_token 自 mint(与推送区同端点;进程内不缓存 ——
        引擎每轮一建一关,prompt 引擎资源卫生判例)."""
        response = await self._active_client.post(
            f"{API_BASE}/auth/v3/tenant_access_token/internal",
            json={"app_id": app_id, "app_secret": app_secret},
        )
        try:
            payload = response.json()
        except ValueError as exc:
            raise FetchError(
                f"飞书凭据返回的不是 JSON:HTTP {response.status_code}",
                error_type="feishu_token_mint_failed",
            ) from exc
        if response.status_code != 200 or payload.get("code") != 0:
            raise FetchError(
                f"获取飞书访问凭据被拒(code={payload.get('code')}):"
                f"{payload.get('msg') or f'HTTP {response.status_code}'};请核对 app_id/app_secret",
                error_type="feishu_token_mint_failed",
            )
        token = payload.get("tenant_access_token")
        if not token:
            raise FetchError(
                "飞书凭据返回的结果缺 tenant_access_token",
                error_type="feishu_token_mint_failed",
            )
        return str(token)

    async def _read_messages(self, chat_id: str, lookback: int, token: str) -> list[dict]:
        """群消息窗口拉取 + 条目映射(text 出条目,其余类型静默跳过)."""
        response = await self._active_client.get(
            f"{API_BASE}/im/v1/messages",
            params={
                "container_id_type": "chat",
                "container_id": chat_id,
                "sort_type": "ByCreateTimeDesc",
                "page_size": str(lookback),
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        try:
            payload = response.json()
        except ValueError as exc:
            raise FetchError(
                f"飞书消息返回的不是 JSON:HTTP {response.status_code}",
                error_type="feishu_api_error",
            ) from exc
        code = payload.get("code")
        if response.status_code != 200 or code != 0:
            if code in _PERMISSION_CODES:
                raise FetchError(
                    f"飞书群消息读取被拒(code={code}):{payload.get('msg')} —— "
                    "请到飞书开放平台为该应用开通 im:message 群消息只读权限,"
                    "并把机器人加入这个群(凭据与推送使用同一应用)",
                    error_type="feishu_permission_denied",
                )
            raise FetchError(
                f"飞书消息拉取被拒(code={code}):{payload.get('msg') or f'HTTP {response.status_code}'}",
                error_type="feishu_api_error",
            )
        messages = (payload.get("data") or {}).get("items") or []
        items: list[dict] = []
        for message in messages:
            if (message.get("sender") or {}).get("sender_type") == "app":
                continue  # 机器人自身消息(含 MYIA 推送回声)不回采
            item = self._message_to_item(chat_id, message)
            if item is not None:
                items.append(item)
        return items

    def _message_to_item(self, chat_id: str, message: dict[str, Any]) -> dict[str, Any] | None:
        """一条消息 → 管线条目(#fs- 锚;Item.from_extracted 契约)。非 text
        类型 v1 静默跳过(模块文档诚实边界)."""
        if message.get("msg_type") != "text":
            return None
        try:
            body = json.loads(message.get("body", {}).get("content") or "{}")
            text = str(body.get("text") or "").strip()
        except ValueError:
            return None
        if not text:
            return None
        message_id = str(message.get("message_id") or "").strip()
        if not message_id:
            return None
        sender = message.get("sender") or {}
        return {
            # 锚:#fs-<chat_id>-<message_id>(全期幂等,管线 url 去重键)
            "url": f"https://{API_HOST}#fs-{chat_id}-{message_id}",
            "title": text[:80],
            "content": text,
            "published": message.get("create_time"),
            "author": str(sender.get("id") or ""),
            "chat_id": chat_id,
            "sender_type": sender.get("sender_type"),
            "feishu_message_id": message_id,
        }
