"""Thin async client over any OpenAI-compatible ``chat.completions`` endpoint.

The ``openai`` package is an *optional* dependency (extras ``myssia[llm]``) and
is imported lazily at first use — never at module import — so the core
pipeline stays zero-heavy-dependency (same pattern as
``myssia.engines.crawl4ai.load_crawl4ai``). Tests inject a fake object with the
same ``complete()`` coroutine; no test ever touches the network.

Token accounting: the response's ``usage.total_tokens`` travels back with the
text — it is what :class:`myssia.enrich.scoring.BudgetTracker` spends against
``budget_per_run``. A response without usage information reports 0 tokens
(the shortfall is visible in the run's outcome stats, not silently assumed).
"""

from __future__ import annotations

import asyncio
import importlib
import logging
from dataclasses import dataclass
from typing import Any

import httpx

from myssia.enrich.errors import EnrichConfigError

__all__ = ["INSTALL_COMMAND", "CompletionResult", "OpenAICompatClient"]

logger = logging.getLogger(__name__)

INSTALL_COMMAND = "pip install 'myssia[llm]'  # 或 uv add 'myssia[llm]'"


@dataclass(frozen=True)
class CompletionResult:
    """One completion: message text plus observed token usage."""

    text: str
    total_tokens: int


class OpenAICompatClient:
    """Minimal async wrapper: one ``chat.completions.create`` per call.

    Construction never touches the optional dependency: ``openai`` is
    imported lazily at the first completion (:meth:`_ensure_async_client`),
    so building this client (or an enricher/aggregator holding one) succeeds
    without the extra installed.

    Args:
        base_url: resolved endpoint base URL (http(s), already credential-
            resolved by the enricher — this class never sees references).
        api_key: resolved key (never logged).
        timeout_seconds: hard cap per completion (asyncio.wait_for).
        max_output_tokens: completion cap sent to the endpoint.

    Raises:
        EnrichConfigError: on the first :meth:`complete` call —
            ``dependency_missing`` when the ``openai`` package is not
            installed (structured, carries :data:`INSTALL_COMMAND`).
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        *,
        timeout_seconds: float = 60.0,
        max_output_tokens: int = 2048,
        extra_body: dict[str, Any] | None = None,
    ) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds
        self._max_output_tokens = max_output_tokens
        self._extra_body = dict(extra_body) if extra_body else None
        self._async_client: Any | None = None
        # Anthropic 兼容通道(10-25 主人裁定 glm-5.3 走 /api/anthropic):
        # base_url 含 "anthropic" 时走原生 messages 协议(httpx 直调,
        # 零 openai SDK 依赖);否则走既有 OpenAI chat.completions 路径。
        self._anthropic = "anthropic" in base_url

    def _ensure_async_client(self) -> Any:
        """Build (once) the lazily-imported ``openai.AsyncOpenAI``."""
        if self._async_client is None:
            openai = self._import_openai()
            self._async_client = openai.AsyncOpenAI(
                base_url=self._base_url,
                api_key=self._api_key,
                timeout=self._timeout_seconds,
            )
        return self._async_client

    @staticmethod
    def _import_openai() -> Any:
        try:
            return importlib.import_module("openai")
        except ImportError as exc:
            raise EnrichConfigError(
                "dependency_missing",
                f"enrich 依赖 openai 未安装:请先执行 {INSTALL_COMMAND}"
                "(openai 为可选 extras,核心流水线零重依赖)",
                details={"package": "openai", "install": INSTALL_COMMAND},
            ) from exc

    async def _complete_anthropic(
        self, *, model: str, system: str, user: str
    ) -> CompletionResult:
        """Anthropic messages 协议适配(智谱 /api/anthropic 官方通道).

        glm-5.3 等思考型主力模型仅在此通道畅付(PAAS v4 撞 1113 计费墙,
        且该通道支持 thinking disabled);httpx 为核心依赖,零 openai SDK。
        extra_body.chat_template_kwargs.enable_thinking(既有 disable_thinking
        接线)在此映射为 Anthropic ``thinking.type``。
        """
        payload: dict[str, Any] = {
            "model": model,
            "max_tokens": self._max_output_tokens,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        extra = self._extra_body or {}
        ctw = extra.get("chat_template_kwargs")
        if isinstance(ctw, dict) and ctw.get("enable_thinking") is False:
            payload["thinking"] = {"type": "disabled"}
        url = self._base_url.rstrip("/") + "/v1/messages"
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            data = resp.json()
        text = "".join(
            block.get("text", "")
            for block in data.get("content", [])
            if isinstance(block, dict) and block.get("type") == "text"
        )
        usage = data.get("usage", {})
        total = int(usage.get("input_tokens", 0)) + int(usage.get("output_tokens", 0))
        return CompletionResult(text=text, total_tokens=total)

    async def complete(self, *, model: str, system: str, user: str) -> CompletionResult:
        """One scored-batch completion (system+user messages, temperature 0).

        Anthropic 兼容 base_url(含 "anthropic")走 :meth:`_complete_anthropic`
        原生协议;其余走 OpenAI ``chat.completions``。

        Raises:
            TimeoutError: the completion exceeded ``timeout_seconds``.
            Exception: endpoint/API errors propagate to the enricher, which
                isolates them per batch (调用方按单批失败处理).
        """
        if self._anthropic:
            return await self._complete_anthropic(model=model, system=system, user=user)
        client = self._ensure_async_client()
        create_kwargs: dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0,
            "max_tokens": self._max_output_tokens,
        }
        if self._extra_body:
            # OpenAI 兼容端点的非标扩展体(openai SDK extra_body 直通)。
            # 当前唯一消费场景 = 本地思考型模型关思考(LM Studio 的
            # chat_template_kwargs.enable_thinking,2026-10-17 实测生效)。
            create_kwargs["extra_body"] = self._extra_body
        response = await asyncio.wait_for(
            client.chat.completions.create(**create_kwargs),
            timeout=self._timeout_seconds,
        )
        return CompletionResult(
            text=_message_text(response),
            total_tokens=_usage_tokens(response),
        )

    async def aclose(self) -> None:
        """Release the underlying httpx-backed client, when built."""
        if self._async_client is not None:
            close = getattr(self._async_client, "close", None)
            if close is not None:
                result = close()
                if asyncio.iscoroutine(result):
                    await result
            self._async_client = None


def _message_text(response: Any) -> str:
    """Extract the first choice's message content (missing → empty string)."""
    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError, TypeError):
        return ""
    return content if isinstance(content, str) else ""


def _usage_tokens(response: Any) -> int:
    """Observed total token usage, 0 when the endpoint omits usage."""
    usage = getattr(response, "usage", None)
    tokens = getattr(usage, "total_tokens", None)
    if isinstance(tokens, (int, float)) and tokens > 0:
        return int(tokens)
    logger.debug("LLM 响应未携带 usage,按 0 token 计入预算(预算护栏可能低估)")
    return 0
