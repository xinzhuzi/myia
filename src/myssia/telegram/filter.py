"""Telegram 过滤管线 —— 粗筛词表 + LLM 精筛 + 高价值合并单条(10-06 B2).

形态(design D2「过滤管线」,grill Q5 决议):

1. **关键词粗筛**(零成本):消息文本命中词表才进入后续面 —— 群消息以闲聊
   为主,粗筛把 LLM 成本压到命中子集;未命中的消息**不产出条目**(不占库
   不占日报,零痕迹跳过)。词表三层:源级 ``engine_options.telegram.keywords``
   > 内置缺省 :data:`DEFAULT_COARSE_KEYWORDS`(免费/token/额度/优惠/白嫖
   等)—— 配置化即「口味」(grill Q5:口味配置化)。
2. **LLM 精筛**(挂点,enrich 客户端复用)::class:`~myssia.enrich.client.
   OpenAICompatClient` 直连 OpenAI 兼容端点(缺省 ``glm-4-flash``,enrich
   同款缺省),凭据 ``llm_base_url``/``llm_api_key`` 走 ``env:``/
   ``keychain:`` 引用(prompt 引擎同契约,明文拒);一轮批量打分 0-10。
   **端点未配 = 降级纯粗筛**(粗筛命中全部按普通出仓,零 token;宁慢推
   不误推)—— 精筛是增强件,不是硬前置。
3. **出口**(组合铁律):score ≥ :data:`DEFAULT_SCORE_THRESHOLD`(8,可配
   ``score_threshold``)= 高价值 → 同轮多条**合并单条**出仓(一轮至多一条
   即时推送;批量档 route ``score >= 8 → immediate``,serve 档直推);
   其余 = 普通逐条出仓带 score(route archive 入库,合并日报「Telegram
   群」分区承载)。

合并锚点:高价值合并条目 URL = 组内按 url 字典序首条的原 url 加
``-hv<组内条数>-<尾 message_id>`` 后缀 —— 措辞修正(深审 F12):后缀只含
**一个**尾 id,不是 ``<chat_id>-<min>-<max>`` 区间对;组内消息 id 的数值序
min/max 全量记录在 ``merged_message_ids`` metadata(观测与账本面)。同
窗口重拉同批消息 → 排序确定 → 同锚 → 管线 dedup 拦截,批量档重跑幂等。

降级语义(保守方向永远是不推):

- ``llm_not_configured``:端点引用缺 → 全部普通出仓(score 缺),INFO 留痕;
- ``llm_failed``:引用解析失败 / 端点调用失败 / 输出解析失败 → 同上,
  WARNING 留痕(条目仍入库可见,漏推可从日报找回);
- 条目级缺分(模型漏答个别 id)→ 该条普通出仓,不废整轮。

凭据零外显:解析后的 base_url/api_key 不落日志;异常消息不带 api_key
(OpenAICompatClient 异常 str 不含 key;引用形态原样可记)。

 Raises 面向上层(引擎/serve)统一吞为降级 —— 本模块**不抛**,一切失败
 都以 :class:`TelegramFilterOutcome` 的 ``degraded``/``degrade_reason``
 观测(调用方决定日志级别);唯一例外是构造期配置形状错(
 :class:`ValueError`,非法词表/阈值型)—— 配置错误当场暴露优于静默吞。
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from myssia.enrich.client import OpenAICompatClient
from myssia.enrich.scoring import extract_json_entries
from myssia.schema import DEFAULT_ENRICH_MODEL

logger = logging.getLogger(__name__)

#: 内置缺省粗筛词表(免费情报口味;源级 keywords 覆盖 = 口味配置化)。
#: ASCII 词大小写不敏感命中(coarse_hit);中文词精确子串。
DEFAULT_COARSE_KEYWORDS: tuple[str, ...] = (
    "免费",
    "白嫖",
    "羊毛",
    "token",
    "额度",
    "优惠",
    "折扣",
    "赠送",
    "福利",
    "激活码",
    "兑换码",
    "促销",
    "coupon",
    "free",
    "giveaway",
)

#: 高价值阈值缺省(grill Q5:≥8 分即时;源级 score_threshold 可配)。
DEFAULT_SCORE_THRESHOLD = 8

#: 精筛单轮 LLM 超时秒(enrich 缺省同量级;群消息批量小、60s 足)。
DEFAULT_LLM_TIMEOUT_SECONDS = 60.0

#: 精筛条目进 prompt 的文本截断(群消息可 4096 字;评分只要要点)。
MESSAGE_SNIPPET_CHARS = 600

#: 精筛 system 指令:打分口径与输出形态(grill Q5 口径的机器可执行版)。
SYSTEM_PROMPT = (
    "你是 MYIA 的 Telegram 群消息情报评估员。对每条消息按羊毛/优惠情报价值"
    "打 0-10 整数分:8-10 = 立刻值得推送主人的高价值(限时免费额度/白嫖渠道/"
    "重大折扣/稀缺 token 或激活码/马上过期的福利);5-7 = 有点意思但可等日报"
    "(常规优惠、间接线索);0-4 = 闲聊灌水、广告、与羊毛无关。"
    "只输出 JSON 数组,每个元素形如 "
    '{"id": <消息编号>, "score": <0-10 整数>, "reason": "<一句话理由>"},'
    "覆盖输入的每一条,不要寒暄、不要输出 JSON 以外的内容。"
)

#: 合并条目 content 逐条文本截断(合并卡可读性;全文在库)。
MERGED_LINE_CHARS = 200

__all__ = [
    "DEFAULT_COARSE_KEYWORDS",
    "DEFAULT_LLM_TIMEOUT_SECONDS",
    "DEFAULT_SCORE_THRESHOLD",
    "MERGED_LINE_CHARS",
    "MESSAGE_SNIPPET_CHARS",
    "SYSTEM_PROMPT",
    "TelegramFilterConfig",
    "TelegramFilterOutcome",
    "TelegramFilterPipeline",
    "coarse_hit",
    "merge_high_value",
]


def coarse_hit(text: str, keywords: Sequence[str]) -> str | None:
    """粗筛:文本命中词表任一词 → 返回该词;未命中 → None.

    ASCII 词大小写不敏感(``free`` 命中 ``FREE``/``Free``),中文词精确
    子串;词表为空 = 全部未命中(显式配 ``keywords: []`` 即整体静默——
    有意的关闭语义,与缺省词表区分)。
    """
    haystack = text.lower()
    for keyword in keywords:
        needle = keyword.strip().lower()
        if needle and needle in haystack:
            return keyword
    return None


@dataclass(frozen=True)
class TelegramFilterConfig:
    """过滤管线配置(engine_options.telegram 子集,引擎侧装配).

    Attributes:
        keywords: 粗筛词表(空元组 = 用缺省;空列表经引擎归一为空元组后再
            区分——见 :func:`coarse_hit`,空词表=全未命中=关闭)。
        score_threshold: 高价值阈值(1-10,缺省 8)。
        model: 精筛模型(缺省 ``glm-4-flash``,enrich 同款)。
        llm_base_url / llm_api_key: OpenAI 兼容端点引用(None = 降级纯粗筛;
            成对配置,半配是配置错误由引擎结构化拒)。
        timeout: 单轮精筛超时秒。
    """

    keywords: tuple[str, ...] = DEFAULT_COARSE_KEYWORDS
    score_threshold: int = DEFAULT_SCORE_THRESHOLD
    model: str = DEFAULT_ENRICH_MODEL
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    timeout: float = DEFAULT_LLM_TIMEOUT_SECONDS


@dataclass
class TelegramFilterOutcome:
    """一轮过滤的可观测结果(引擎/serve/doctor 消费)."""

    #: 高价值条目(score ≥ 阈值,已带 score metadata;由调用方合并或直推)。
    high_value: list[dict[str, Any]] = field(default_factory=list)
    #: 普通条目(粗筛命中但分低于阈值/无分;入库进日报)。
    normal: list[dict[str, Any]] = field(default_factory=list)
    #: 粗筛命中数(进入精筛面的消息)。
    coarse_hits: int = 0
    #: 粗筛未命中数(零痕迹跳过)。
    coarse_misses: int = 0
    #: LLM 实际打分条数(降级时 0)。
    scored: int = 0
    #: 降级标记与原因(llm_not_configured / llm_failed / None)。
    degraded: bool = False
    degrade_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "high_value": len(self.high_value),
            "normal": len(self.normal),
            "coarse_hits": self.coarse_hits,
            "coarse_misses": self.coarse_misses,
            "scored": self.scored,
            "degraded": self.degraded,
            "degrade_reason": self.degrade_reason,
        }


class TelegramFilterPipeline:
    """粗筛 → 精筛 → 分级(两档共用;批量引擎与 serve 宿主各持一份).

    Args:
        config: 过滤配置(词表/阈值/端点引用)。
        completer: LLM 完成层注入口(测试 fake;缺省每轮一建
            :class:`OpenAICompatClient` 并在轮末关闭 —— prompt 引擎资源
            卫生判例)。签名同 ``OpenAICompatClient.complete(model=…,
            system=…, user=…)``。
        keychain_backend: 凭据解析后端(引擎的 ``context.keychain_backend``
            直传;测试传 InMemoryKeychainBackend)。
    """

    def __init__(
        self,
        config: TelegramFilterConfig,
        *,
        completer: Any | None = None,
        keychain_backend: Any | None = None,
    ) -> None:
        self.config = config
        self._completer = completer
        self._keychain_backend = keychain_backend

    # ------------------------------------------------------------- filtering

    async def process(self, items: list[dict[str, Any]]) -> TelegramFilterOutcome:
        """一轮过滤:items(引擎条目)→ 高价值/普通两组(不抛)."""
        outcome = TelegramFilterOutcome()
        if not items:
            return outcome
        hits: list[dict[str, Any]] = []
        for item in items:
            text = self._screen_text(item)
            if coarse_hit(text, self.config.keywords) is not None:
                hits.append(item)
            else:
                outcome.coarse_misses += 1
        outcome.coarse_hits = len(hits)
        if not hits:
            return outcome

        scores = await self._fine_scores(hits, outcome)
        for item in hits:
            score = scores.get(self._item_key(item))
            if score is not None and score >= self.config.score_threshold:
                item["score"] = score
                outcome.high_value.append(item)
            else:
                if score is not None:
                    item["score"] = score
                outcome.normal.append(item)
        logger.info(
            "telegram 过滤完成 hits=%s misses=%s scored=%s high=%s normal=%s"
            " degraded=%s(%s)",
            outcome.coarse_hits,
            outcome.coarse_misses,
            outcome.scored,
            len(outcome.high_value),
            len(outcome.normal),
            outcome.degraded,
            outcome.degrade_reason or "-",
        )
        return outcome

    @staticmethod
    def _screen_text(item: Mapping[str, Any]) -> str:
        """粗筛面:title + content(引擎把全文放这两键)."""
        parts = [
            value
            for value in (item.get("title"), item.get("content"))
            if isinstance(value, str)
        ]
        return "\n".join(parts)

    @staticmethod
    def _item_key(item: Mapping[str, Any]) -> str:
        """条目在打分应答里的匹配键(url 全期唯一锚)."""
        return str(item.get("url") or "")

    # ------------------------------------------------------------ LLM scoring

    async def _fine_scores(
        self, hits: list[dict[str, Any]], outcome: TelegramFilterOutcome
    ) -> dict[str, int]:
        """LLM 批量打分:命中条目 → {url: score}(降级 = 空 dict,不抛)."""
        config = self.config
        if config.llm_base_url is None or config.llm_api_key is None:
            outcome.degraded = True
            outcome.degrade_reason = "llm_not_configured"
            logger.info(
                "telegram 精筛端点未配(llm_base_url/llm_api_key),降级纯粗筛:"
                "%s 条命中全部按普通出仓(入库日报可见)",
                len(hits),
            )
            return {}
        endpoint: tuple[str, str] | None = None
        own_client: OpenAICompatClient | None = None
        ids = {index + 1: self._item_key(item) for index, item in enumerate(hits)}
        sections = []
        for index, item in enumerate(hits):
            text = (self._screen_text(item) or "")[:MESSAGE_SNIPPET_CHARS]
            author = item.get("author") if isinstance(item.get("author"), str) else ""
            sections.append(f"[id {index + 1}] {author}: {text}".strip())
        user_message = "群消息清单(编号对应输出 id):\n" + "\n".join(sections)

        try:
            if self._completer is not None:
                # 测试缝:注入的完成层自带端点,凭据解析整段跳过(fake 不
                # 需要真引用可解析 —— prompt 引擎 completer 注入同语义)。
                completer = self._completer
            else:
                endpoint = self._resolve_endpoint()
                if endpoint is None:
                    outcome.degraded = True
                    outcome.degrade_reason = "llm_failed"
                    return {}
                base_url, api_key = endpoint
                own_client = OpenAICompatClient(
                    base_url, api_key, timeout_seconds=config.timeout
                )
                completer = own_client.complete
            completion = await asyncio.wait_for(
                completer(model=config.model, system=SYSTEM_PROMPT, user=user_message),
                timeout=config.timeout,
            )
            text = str(getattr(completion, "text", "") or "")
            scores = self._parse_scores(text, ids)
            outcome.scored = len(scores)
            if not scores:
                outcome.degraded = True
                outcome.degrade_reason = "llm_failed"
                logger.warning(
                    "telegram 精筛输出无可解析条目(降级纯粗筛,条目照常入库)"
                    " model=%s",
                    config.model,
                )
            return scores
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - 端点/超时/解析:降级不抛
            outcome.degraded = True
            outcome.degrade_reason = "llm_failed"
            logger.warning(
                "telegram 精筛调用失败(降级纯粗筛,条目照常入库) model=%s: %s",
                config.model,
                exc,
            )
            return {}
        finally:
            if own_client is not None:
                try:
                    await own_client.aclose()
                except Exception:  # noqa: BLE001 - 清理失败不污染结果
                    logger.warning("telegram 精筛客户端关闭失败(忽略)", exc_info=True)

    def _resolve_endpoint(self) -> tuple[str, str] | None:
        """解析端点引用(值不落日志;失败 = None 由调用方降级)."""
        from myssia.schema import CredentialResolveError, resolve_credential

        try:
            base_url = resolve_credential(
                self.config.llm_base_url or "", backend=self._keychain_backend
            )
            api_key = resolve_credential(
                self.config.llm_api_key or "", backend=self._keychain_backend
            )
        except CredentialResolveError as exc:
            logger.warning(
                "telegram 精筛端点引用解析失败(降级纯粗筛) ref=%s: %s",
                self.config.llm_base_url,
                exc,
            )
            return None
        if not base_url.startswith(("http://", "https://")):
            logger.warning(
                "telegram 精筛 base_url 解析结果不是 http(s) 地址(降级纯粗筛)"
            )
            return None
        return base_url, api_key

    def _parse_scores(self, text: str, ids: Mapping[int, str]) -> dict[str, int]:
        """LLM 应答 → {url: 0-10 分}(宽容:坏条目跳过,不废整轮)."""
        from myssia.enrich.scoring import ScoreParseError

        try:
            entries = extract_json_entries(text)
        except (ScoreParseError, ValueError):
            return {}
        scores: dict[str, int] = {}
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            entry_id = entry.get("id")
            score = entry.get("score")
            if (
                isinstance(entry_id, bool)
                or not isinstance(entry_id, int)
                or isinstance(score, bool)
                or not isinstance(score, (int, float))
            ):
                continue
            url = ids.get(entry_id)
            if url is None:
                continue
            scores[url] = max(0, min(10, int(round(score))))
        return scores


# ---------------------------------------------------------------------------
# 高价值合并(组合铁律:同轮多条 → 单条)
# ---------------------------------------------------------------------------


def merge_high_value(
    items: Sequence[Mapping[str, Any]], *, threshold: int = DEFAULT_SCORE_THRESHOLD
) -> dict[str, Any] | None:
    """同轮高价值条目合并单条(空组 = None;批量引擎与 serve 共用).

    合并条目:

    - ``url`` = 首条 url 加 ``-hv<n>-<尾 message_id>`` 后缀(首/尾取组内
      按 url 字典序排序的首末条 → 同窗口重拉同批同序 → 同锚 → dedup
      幂等;锚不改变落点;数值序 id 全量在 ``merged_message_ids``);
    - ``title`` = 「Telegram 高价值 N 条(score≥8)」;
    - ``content`` = 逐条 markdown 列表(分数/作者/文本截断);
    - ``score`` = 组内最高分(route ``score >= 8 → immediate`` 直接过);
    - metadata:`merged_count` / `merged_message_ids`(观测与账本面)。
    """
    if not items:
        return None
    ordered = sorted(items, key=lambda item: str(item.get("url") or ""))
    first = ordered[0]
    last_id = ""
    message_ids: list[Any] = []
    for item in ordered:
        mid = item.get("message_id")
        if isinstance(mid, int):
            message_ids.append(mid)
            last_id = str(mid)
    lines: list[str] = []
    top_score: int | None = None
    for item in ordered:
        score = item.get("score")
        score_label = f"{round(score)}分" if isinstance(score, (int, float)) else "?分"
        if isinstance(score, (int, float)) and (
            top_score is None or score > top_score
        ):
            top_score = int(round(score))
        author = item.get("author") if isinstance(item.get("author"), str) else ""
        text = (item.get("content") or item.get("title") or "").strip()
        prefix = f"{author}: " if author else ""
        lines.append(f"- [{score_label}] {prefix}{text[:MERGED_LINE_CHARS]}")
    merged: dict[str, Any] = {
        "url": f"{first.get('url')}-hv{len(ordered)}-{last_id}",
        "title": f"Telegram 高价值 {len(ordered)} 条(score≥{threshold})",
        "content": "\n".join(lines),
        "merged_count": len(ordered),
    }
    if message_ids:
        merged["merged_message_ids"] = message_ids
    if top_score is not None:
        merged["score"] = top_score
    chat_title = first.get("chat_title")
    if isinstance(chat_title, str) and chat_title:
        merged["chat_title"] = chat_title
    return merged
