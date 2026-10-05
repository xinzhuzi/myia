"""Telegram ``getUpdates`` feedback polling (桌面形态接收, grill Q7 定案).

The desktop form has no public endpoint for card callbacks, so the receiving
side polls the Bot API instead: every ``callback_query`` update whose
``data`` carries our feedback contract is turned into a callback record for
:func:`myssia.feedback.ingest_callbacks`. Long-polling (``getUpdates``
``timeout``) keeps this cheap; the pipeline's resident mode runs the loop in
the background whenever a ``telegram`` push channel is configured.

被动目录积累(10-03-messaging-telegram D2):Telegram Bot API 无「列出
会话」能力(蓝本事实轮核,Hermes 同款约束),目录条目唯一来源是入站
回填——轮询看到的每个 update 的 effective chat 归一为
:class:`~myssia.push.directory.ChannelEntry` 后经 ``on_chat`` sink 交回调方
(管线注入 ``ChannelDirectory.merge_entries("telegram", …)``)。sink 是
**旁路观察者**:解析/去重/错误路径零改动,sink 抛错只记日志不中断轮询;
不注入时行为与不带 sink 逐字节一致。

**一个 bot token 只允许一个轮询方**(素材 12 → 10-05-telegram-token-dedupe
由库内保证):bot token 固定解析自 ``env:TELEGRAM_BOT_TOKEN``,Telegram 对
同一 token 的并发 ``getUpdates`` long-poll 回 **409 Conflict** 互踢。多品类
共享同一 token 因此是受支持形态而非配置错误::func:`acquire_poll_lease`
以**进程内注册表 + 跨进程 flock** 双层去重——先到的常驻进程独占轮询
(反馈回调与会话目录观测只入它的库),后到者(同进程或他进程)**禁动**
(推送不受影响,只是不接收反馈);``myssia doctor`` 的
``telegram_token_poll_conflict`` finding 披露该单接收方语义。

Callback-data contract (buttons belong to the desktop 正式版; the receiver
already speaks it): ``fb:<good|bad>:<dedup_key>`` — the dedup key may be a
URL and therefore contain colons, so the prefix splits at most twice. Note
the Bot API caps ``callback_data`` at 64 bytes; keys longer than that need a
short-reference scheme at *send* time (tracked gap, see the task's open
issues) — the receiver stays compatible with both.

Credentials stay references until send time (security baseline: 凭据零明文);
all HTTP I/O goes through an injectable ``httpx.AsyncClient`` — tests use
``httpx.MockTransport`` and never touch the real API.
"""

from __future__ import annotations

import contextlib
import errno
import hashlib
import logging
import os
import tempfile
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, Any, Callable, Mapping

import httpx

from myssia.push.base import DEFAULT_SEND_TIMEOUT_SECONDS
from myssia.push.directory import ChannelEntry
from myssia.push.telegram import DEFAULT_TOKEN_ENV_REF
from myssia.schema import CredentialResolveError, resolve_credential

try:  # 跨平台文件锁:Unix fcntl / Windows msvcrt(cron/tick.py 同款守卫导入)
    import fcntl  # noqa: F401  (可能缺,保名字存在)
except ImportError:  # pragma: no cover - Windows
    fcntl = None  # type: ignore[assignment]
try:
    import msvcrt  # type: ignore[import-not-found]  # noqa: F401
except ImportError:  # pragma: no cover - POSIX
    msvcrt = None  # type: ignore[assignment]

__all__ = [
    "CALLBACK_PREFIX",
    "DEFAULT_POLL_INTERVAL_SECONDS",
    "PollResult",
    "TelegramCallback",
    "TelegramFeedbackError",
    "TelegramFeedbackPoller",
    "TelegramPollLease",
    "acquire_poll_lease",
    "chat_entry_from_update",
    "default_poll_lock_dir",
    "entry_from_chat",
    "parse_callback_data",
]

logger = logging.getLogger(__name__)

#: Feedback callback-data prefix: ``fb:<verdict>:<dedup_key>``.
CALLBACK_PREFIX = "fb:"
#: Legal verdicts inside callback data (normalized again at ingestion).
_CALLBACK_VERDICTS = ("good", "bad")
#: Background-loop sleep between getUpdates calls (pipeline resident mode).
DEFAULT_POLL_INTERVAL_SECONDS = 30.0
#: update 顶层携带 chat 的载荷键(首个命中即取;一条 update 只有一种载荷)。
_CHAT_BEARER_KEYS = (
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "my_chat_member",
    "chat_member",
)
#: callback_query 的 chat 藏在 ``.message.chat`` 下(按钮回调的消息宿主)。
_CALLBACK_QUERY_KEY = "callback_query"


class TelegramFeedbackError(RuntimeError):
    """One feedback-poll failed (structured code; never a bare string).

    Attributes:
        code: ``http_error`` / ``invalid_response`` / ``telegram_api_error``
            / credential codes re-exported from
            :class:`myssia.schema.CredentialResolveError`.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def parse_callback_data(data: Any) -> tuple[str, str] | None:
    """Parse ``fb:<verdict>:<dedup_key>``; None when not our feedback data.

    The dedup key keeps everything after the second colon (URLs contain
    colons themselves); verdicts are matched exactly against good/bad —
    anything else (foreign bots' callbacks, malformed data) returns None and
    the update is counted as skipped by the caller.
    """
    if not isinstance(data, str) or not data.startswith(CALLBACK_PREFIX):
        return None
    parts = data[len(CALLBACK_PREFIX) :].split(":", 1)  # maxsplit=1:URL 键自带冒号
    if len(parts) != 2:
        return None
    verdict, dedup_key = parts
    if verdict not in _CALLBACK_VERDICTS or not dedup_key.strip():
        return None
    return verdict, dedup_key


def entry_from_chat(chat: Any) -> ChannelEntry | None:
    """One Bot API ``chat`` object → :class:`ChannelEntry`(design D2 归一).

    归一规则(蓝本:Hermes telegram adapter ``_normalize_chat_type`` 的
    private→dm / supergroup→group 语汇,NousResearch/Hermes-Agent,MIT):

    - ``group``/``supergroup``:``title`` 为名,type=group;
    - ``channel``:``title`` 为名,type=channel;
    - ``private``(及未知形态按私聊兜底):``first_name [+ last_name]`` 为名,
      type=dm;有 username 拼进 name 尾注(``名 (@user)``)——不扩
      ChannelEntry schema,实现取简(design D2 定案)。

    名字缺失退回 username / chat_id 占位(条目仍可按 id 寻址);``id``
    缺失或载荷非 dict → None(静默丢弃,不毒化目录)。
    """
    if not isinstance(chat, Mapping):
        return None
    chat_id = str(chat.get("id") or "").strip()
    if not chat_id:
        return None
    chat_type = str(chat.get("type") or "").strip().lower()
    if chat_type in ("group", "supergroup", "channel"):
        # supergroup 归一为 group(design D2:两者都按群记,ENTRY_TYPES 无
        # supergroup 形态;Hermes 的 forum 话题形态属非目标)。
        name = str(chat.get("title") or "").strip() or chat_id
        return ChannelEntry(
            platform="telegram",
            chat_id=chat_id,
            name=name,
            type="group" if chat_type != "channel" else "channel",
        )
    first = str(chat.get("first_name") or "").strip()
    last = str(chat.get("last_name") or "").strip()
    username = str(chat.get("username") or "").strip()
    name = " ".join(part for part in (first, last) if part) or username or chat_id
    if username and username not in name:
        name = f"{name} (@{username})"
    return ChannelEntry(platform="telegram", chat_id=chat_id, name=name, type="dm")


def chat_entry_from_update(update: Any) -> ChannelEntry | None:
    """One getUpdates update → its effective chat as :class:`ChannelEntry`.

    消息类载荷(``message``/``edited_message``/``channel_post``/
    ``edited_channel_post``)与成员事件(``my_chat_member``/``chat_member``)
    的 chat 在 ``.chat``;``callback_query`` 在 ``.message.chat``。一条
    update 只有一种载荷,首个命中即取;无 chat / 载荷坏 → None。
    """
    if not isinstance(update, Mapping):
        return None
    for key in _CHAT_BEARER_KEYS:
        payload = update.get(key)
        if isinstance(payload, Mapping):
            return entry_from_chat(payload.get("chat"))
    query = update.get(_CALLBACK_QUERY_KEY)
    if isinstance(query, Mapping):
        message = query.get("message")
        if isinstance(message, Mapping):
            return entry_from_chat(message.get("chat"))
    return None


@dataclass(frozen=True)
class TelegramCallback:
    """One parsed feedback callback (ingestion input, 见 myssia.feedback)."""

    update_id: int
    verdict: str
    dedup_key: str
    channel: str = "telegram"

    @property
    def external_id(self) -> str:
        """幂等身份:同一 update 双击/重试/重启重放只入库一次(见 myssia.feedback)."""
        return str(self.update_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            "update_id": self.update_id,
            "channel": self.channel,
            "verdict": self.verdict,
            "dedup_key": self.dedup_key,
            "external_id": self.external_id,
        }


@dataclass
class PollResult:
    """One ``getUpdates`` round: parsed callbacks + the offset bookmark."""

    callbacks: list[TelegramCallback] = field(default_factory=list)
    update_count: int = 0
    skipped: int = 0
    next_offset: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "callbacks": [callback.to_dict() for callback in self.callbacks],
            "update_count": self.update_count,
            "skipped": self.skipped,
            "next_offset": self.next_offset,
        }


# ---------------------------------------------------------------------------
# 同 token 单轮询器租约(10-05-telegram-token-dedupe)
# ---------------------------------------------------------------------------

#: 进程内租约注册表:token sha256 摘要 → 持有中的租约。同进程第二个轮询
#: 循环在此被拦下(不落到文件锁层);桌面/服务形态未来把多品类管线收进
#: 单进程时,这一层就是去重点。
_POLL_LEASES: dict[str, TelegramPollLease] = {}
_POLL_LEASES_LOCK = threading.Lock()


def default_poll_lock_dir() -> Path:
    """跨进程轮询锁目录(每用户一目录;多用户 Linux 共享 /tmp 下互不踩踏)。

    品类常驻进程各有 db/cwd,数据根不是共享锚点,故落系统临时目录;macOS/
    Windows 的 tempdir 本就按用户隔离,POSIX 再以 uid 分目录。
    """
    uid = os.getuid() if hasattr(os, "getuid") else None
    stem = f"myssia-tg-poll-{uid}" if uid is not None else "myssia-tg-poll"
    return Path(tempfile.gettempdir()) / stem


def _is_lock_contention_errno(err: OSError) -> bool:
    """*err* 是否意味着「另一持有方在锁」而非真故障(errno 族与
    ``cron/tick.py`` 的 ``_is_lock_contention_errno`` 同源;本域对两者的
    处置都是禁动,但日志口径分开——竞争是 INFO,真故障是 WARNING)。"""
    if err.errno is None:
        return False
    if fcntl is not None:
        return err.errno in (errno.EWOULDBLOCK, errno.EAGAIN, errno.EACCES)
    if msvcrt is not None:  # pragma: no cover - Windows
        return err.errno in (errno.EACCES, errno.EDEADLK)
    return False


class TelegramPollLease:
    """一个 bot token 的 getUpdates 轮询租约(持有方独占,后到者禁动)。

    由 :func:`acquire_poll_lease` 创建;``release()`` 幂等——归还进程内
    注册表并解锁/关闭锁文件。锁文件名只含 token 摘要、内容只写属主 pid
    (security baseline:凭据零明文)。
    """

    def __init__(
        self, digest: str, lock_path: Path | None, lock_fd: IO[str] | None
    ) -> None:
        self._digest = digest
        self._lock_path = lock_path
        self._lock_fd = lock_fd

    @property
    def digest(self) -> str:
        """token 的 sha256 摘要(诊断安全口径;绝不暴露 token 本体)。"""
        return self._digest

    def release(self) -> None:
        """释放租约(幂等):注册表出清 → 解锁 → 关 fd。"""
        if self._lock_fd is None:
            return
        with _POLL_LEASES_LOCK:
            if _POLL_LEASES.get(self._digest) is self:
                del _POLL_LEASES[self._digest]
        if fcntl is not None:
            with contextlib.suppress(OSError):
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
        elif msvcrt is not None:  # pragma: no cover - Windows
            with contextlib.suppress(OSError):
                msvcrt.locking(self._lock_fd.fileno(), msvcrt.LK_UNLCK, 1)
        with contextlib.suppress(OSError):
            self._lock_fd.close()
        self._lock_fd = None


def acquire_poll_lease(
    token: str, *, lock_dir: Path | None = None
) -> TelegramPollLease | None:
    """获取该 bot token 的轮询租约;``None`` = 已有轮询方,后到者禁动。

    双层去重(10-05-telegram-token-dedupe 决议):

    1. **进程内注册表**:同进程已有该 token 的持有方 → None;
    2. **跨进程 flock**:``<lock_dir>/tg-poll-<sha256[:16]>.lock`` 非阻塞
       独占锁(蓝本 = ``cron/tick.py`` 的 tick.lock);竞争 errno → None。

    锁基础设施真故障(目录建不了等)**fail closed** 也返回 None 并大声
    记日志:409 互踢伤及的是对方健康轮询方,宁可本方禁动。锁文件开 ``a``
    模式——竞争输家开文件不截断持有方刚写的 pid 行;拿到锁后才
    truncate+重写。返回的租约由调用方在轮询循环退出/取消时 ``release()``。
    """
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with _POLL_LEASES_LOCK:
        if digest in _POLL_LEASES:
            logger.debug(
                "TG 轮询租约进程内命中(禁动): digest=%s", digest[:16]
            )
            return None
    directory = lock_dir if lock_dir is not None else default_poll_lock_dir()
    try:
        directory.mkdir(parents=True, exist_ok=True)
        with contextlib.suppress(OSError):
            os.chmod(directory, 0o700)
        lock_path = directory / f"tg-poll-{digest[:16]}.lock"
        lock_fd = open(lock_path, "a", encoding="utf-8")
    except OSError as exc:
        logger.warning(
            "TG 轮询租约目录不可用,反馈轮询禁动(fail closed): %s", exc
        )
        return None
    try:
        if fcntl is not None:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        elif msvcrt is not None:  # pragma: no cover - Windows
            msvcrt.locking(lock_fd.fileno(), msvcrt.LK_NBLCK, 1)
        with contextlib.suppress(OSError):
            os.chmod(lock_path, 0o600)
        lock_fd.seek(0)
        lock_fd.truncate()
        lock_fd.write(f"pid={os.getpid()}\n")  # 只写属主 pid,凭据零明文
        lock_fd.flush()
    except OSError as exc:
        with contextlib.suppress(OSError):
            lock_fd.close()
        if _is_lock_contention_errno(exc):
            logger.info(
                "TG 轮询租约被他方持有(禁动): digest=%s", digest[:16]
            )
            return None
        logger.warning(
            "TG 轮询租约获取失败,反馈轮询禁动(fail closed): %s", exc
        )
        return None
    lease = TelegramPollLease(digest, lock_path, lock_fd)
    with _POLL_LEASES_LOCK:
        incumbent = _POLL_LEASES.get(digest)
        if incumbent is not None:  # 同进程双开竞态(理论不可达,防御)
            lease.release()
            return None
        _POLL_LEASES[digest] = lease
    return lease


class TelegramFeedbackPoller:
    """Polls Bot API ``getUpdates`` for feedback callbacks (桌面形态).

    Args:
        token: pre-resolved bot token (constructor injection for tests);
            resolved from ``token_ref`` when omitted — resolution happens
            here (fail fast), so an unusable credential disables the poller
            at construction, never mid-run.
        token_ref: bot-token credential reference; defaults to the same
            ``env:TELEGRAM_BOT_TOKEN`` the send channel uses.
        on_chat: 被动目录 sink(10-03-messaging-telegram D2,可选):每条
            update 的 effective chat 归一为 :class:`ChannelEntry` 后回调;
            缺省 None = 行为与不带 sink 完全一致。sink 抛错只记日志,
            绝不中断轮询(旁路观察者契约)。
        client: injectable ``httpx.AsyncClient`` (tests mock here); when
            omitted a per-poll client is created with ``timeout``.
        timeout: per-request timeout for the self-managed client.
        poll_timeout: Bot API long-poll seconds (0 = short poll; the client
            timeout grows accordingly so a long poll is never cut locally).

    Raises:
        TelegramFeedbackError: the bot-token reference cannot be resolved
            (structured, reference name only — never the value).
    """

    name = "telegram_feedback"

    def __init__(
        self,
        *,
        token: str | None = None,
        token_ref: str | None = None,
        on_chat: Callable[[ChannelEntry], None] | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = DEFAULT_SEND_TIMEOUT_SECONDS,
        poll_timeout: int = 0,
    ) -> None:
        self._token = token
        self._token_ref = token_ref or DEFAULT_TOKEN_ENV_REF
        self._on_chat = on_chat
        self._client = client
        self._timeout = timeout
        self._poll_timeout = max(0, int(poll_timeout))
        if self._token is None:
            self._token = self._resolve_token()

    def _resolve_token(self) -> str:
        try:
            return resolve_credential(self._token_ref)
        except CredentialResolveError as exc:
            raise TelegramFeedbackError(exc.code, f"telegram bot 凭据解析失败: {exc}") from exc

    def acquire_poll_lease(
        self, *, lock_dir: Path | None = None
    ) -> TelegramPollLease | None:
        """本 poller 的 token 的轮询租约(模块级 :func:`acquire_poll_lease`
        的便捷入口;``run_forever`` 的反馈循环启动前调用,抢不到即禁动)。"""
        return acquire_poll_lease(self._token, lock_dir=lock_dir)

    async def poll(self, *, offset: int | None = None) -> PollResult:
        """Run one ``getUpdates`` round; return parsed feedback callbacks.

        Args:
            offset: the ``next_offset`` bookmark from the previous round
                (Telegram re-delivers unconfirmed updates without it).

        Returns:
            :class:`PollResult` — callbacks in arrival order plus the next
            bookmark (``max(update_id) + 1``; None when the round saw no
            updates).注入了 ``on_chat`` 时,本轮每个 update 的 effective
            chat 另经 sink 回调(旁路;不影响本返回值,sink 失败只记日志)。

        Raises:
            TelegramFeedbackError: transport failure, non-JSON response, or
                the API answered ``ok != true`` (structured codes; callers
                log-and-continue — 轮询失败不拖垮常驻调度).
        """
        params: dict[str, Any] = {"timeout": self._poll_timeout}
        if offset is not None:
            params["offset"] = offset
        url = f"https://api.telegram.org/bot{self._token}/getUpdates"
        try:
            if self._client is not None:
                response = await self._client.get(url, params=params)
            else:
                async with httpx.AsyncClient(
                    timeout=self._timeout + self._poll_timeout + 1.0
                ) as client:
                    response = await client.get(url, params=params)
        except httpx.HTTPError as exc:
            raise TelegramFeedbackError(
                "http_error", f"telegram getUpdates 请求失败: {type(exc).__name__}: {exc}"
            ) from exc
        result = self._parse_response(response)
        self._observe_chats(response)
        return result

    def _observe_chats(self, response: httpx.Response) -> None:
        """被动目录积累(设计 D2):sink 旁路,绝不影响轮询本体。

        响应体已由 :meth:`_parse_response` 校验(ok=true,非 JSON/坏包在
        那里已抛);这里重读同一份 JSON(httpx 缓存响应内容,无二次网络
        I/O)提取每条 update 的 effective chat,归一后交 ``on_chat``。
        任何异常——含 sink 抛错——只记日志(轮询契约零改动)。
        """
        if self._on_chat is None:
            return
        try:
            data = response.json()
        except ValueError:
            return  # 理论不可达(_parse_response 已校验);防御性静默
        updates = data.get("result") if isinstance(data, Mapping) else None
        if not isinstance(updates, list):
            return
        for update in updates:
            entry = chat_entry_from_update(update)
            if entry is None:
                continue
            try:
                self._on_chat(entry)
            except Exception as exc:  # noqa: BLE001 - sink 抛错不中断轮询(设计 D2)
                logger.warning(
                    "TG 目录 sink 回调失败(轮询继续): chat_id=%s error=%s",
                    entry.chat_id,
                    exc,
                )

    @staticmethod
    def _parse_response(response: httpx.Response) -> PollResult:
        try:
            data = response.json()
        except ValueError as exc:
            raise TelegramFeedbackError(
                "invalid_response",
                f"telegram 响应不是 JSON(HTTP {response.status_code}): {response.text[:200]!r}",
            ) from exc
        if not isinstance(data, Mapping) or data.get("ok") is not True:
            error_code = data.get("error_code") if isinstance(data, Mapping) else None
            description = (
                data.get("description") if isinstance(data, Mapping) else response.text[:200]
            )
            raise TelegramFeedbackError(
                "telegram_api_error",
                f"telegram API 返回错误: error_code={error_code} description={description}",
            )
        result = PollResult()
        updates = data.get("result")
        if not isinstance(updates, list):
            return result
        max_update_id: int | None = None
        for update in updates:
            if not isinstance(update, Mapping):
                result.skipped += 1
                continue
            update_id = update.get("update_id")
            if isinstance(update_id, bool) or not isinstance(update_id, int):
                result.skipped += 1
                continue
            max_update_id = update_id if max_update_id is None else max(max_update_id, update_id)
            result.update_count += 1
            query = update.get("callback_query")
            if not isinstance(query, Mapping):
                continue  # 普通消息等更新:非反馈回调,计入但不跳过(offset 仍前进)
            parsed = parse_callback_data(query.get("data"))
            if parsed is None:
                result.skipped += 1
                logger.debug("跳过非反馈 callback_query update_id=%s", update_id)
                continue
            verdict, dedup_key = parsed
            result.callbacks.append(
                TelegramCallback(update_id=update_id, verdict=verdict, dedup_key=dedup_key)
            )
        if max_update_id is not None:
            result.next_offset = max_update_id + 1
        logger.debug(
            "getUpdates 完成 updates=%s callbacks=%s skipped=%s next_offset=%s",
            result.update_count, len(result.callbacks), result.skipped, result.next_offset,
        )
        return result
