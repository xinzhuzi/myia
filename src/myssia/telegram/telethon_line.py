"""Telethon 用户线(userbot)—— session 首登/消息面适配/事件宿主(10-06 B4).

bot 线(B1-B3,Bot API)覆盖 bot 所在群;本线用**账号 session**(MTProto,
Telethon ~11k★,MIT;extras ``myssia[telethon]`` 组件轨,**不改其源码**——
链接者铁律)读任意已加入群(bot 进不去的群),PRD 阶段二。

三件套(本模块):

1. **session 首登 CLI 流**(:class:`TelethonLoginFlow`,``myssia telegram
   login`` 消费):api_id/api_hash 钥匙串 → 手机号 → 验证码 →(2FA 密码)
   → session 文件落数据根 ``telegram/telethon.session``(0600);已有
   session = 直接复用提示(``--force`` 删旧重登)。一次性交互,session
   持久后引擎/宿主零交互复用。**小号建议**(风控隔离,research §2)如实
   披露在 login 指引里。api_id/api_hash 未配钥匙串 = 结构化失败
   (``api_credentials_missing``)带人话指引(my.telegram.org 恢复/换出口
   再取自有对;2026-10-08 实证:文档公开示例对 2040 已被服务端
   ApiIdInvalidError 拒,不可用,兜底路径已移除)。
2. **消息面适配**(:func:`telethon_message_to_update`):Telethon Message
   → Bot API update 形状 dict —— 分拣/聚合/锚(``updates_to_items``)/过滤
   管线/出口/幂等锚全复用 bot 线同一份语义(design D1「两档共用」),本线
   零独立消息语义。
3. **事件宿主**(:class:`TelethonUserHost`,serve 档 telethon 线):事件
   监听(``events.NewMessage``)→ 逐事件过 :class:`TelegramServeHost` 的
   ``dispatch_once``(F13 媒体组记忆/F14 出口语义/账本口径全同 bot 线);
   FloodWait 服从退避(服务器指定秒数);断线指数退避(serve 同款 1s→300s)。

凭据纪律(AC5):

- api_id/api_hash 入钥匙串(``myia/telegram/api-id`` / ``api-hash``,
  ``myssia secret set``);session 是登录态持久文件,落数据根 0600,不进
  钥匙串(路径确定性派生,PRD「session 文件」以文件形态落地);
- 手机号/验证码/2FA 密码零落日志(登录流 print 只回显提示词,值不回显;
  电话不整串外显);
- **只读边界**(design D4):本线只 iter/监听,零写接口 —— 引擎面只
  ``connect``/``is_user_authorized``/``iter_messages``/``disconnect``,
  宿主面只 ``add_event_handler``;发送/回复是另档的事(永不在本模块出现)。
  登录流例外仅限 ``send_code_request``/``sign_in``(认证面,CLI 交互独占)。

依赖门:telethon 惰性 import(:func:`require_telethon`),缺装 = 结构化
``dependency_missing`` 带安装命令(simplex/ocr 判例)—— 不进核心依赖,
未装不影响 bot 线与其余流水线。

offsets 语义:telethon 的更新游标由 **session 文件内部状态**自持(pts/seq,
MTProto 协议面),本线不写 :class:`~myssia.telegram.offsets.OffsetStore`
(bot 线的 getUpdates offset 是 Bot API 独有语义);重启断点由 session 自带,
重复消息面由 ``#tg-`` 锚去重兜底。账本(events)**按线分键**(F8 判例):
装配方传 ``bot_token="telethon-user:<api_id>"`` 形态指纹 → ``events-<sha8>.db``
与任何 bot 的账本互不可见,counts 不混计。
"""

from __future__ import annotations

import asyncio
import importlib
import logging
import os
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping

from myssia.engines.telegram import DEFAULT_API_HASH_REF, DEFAULT_API_ID_REF
from myssia.telegram.serve import (
    BACKOFF_BASE_SECONDS,
    BACKOFF_MAX_SECONDS,
    TelegramServeHost,
    TelegramSourceBinding,
)

logger = logging.getLogger(__name__)

#: MTProto 客户端库(extras ``myssia[telethon]``;缺装 → dependency_missing)。
TELETHON_PACKAGE = "telethon"

#: 安装命令(dependency_missing 错误消息附带;simplex 判例)。
INSTALL_COMMAND = "pip install 'myssia[telethon]'  # 或 uv add 'myssia[telethon]'"

#: 数据根下 session 目录名(bot 线 offsets/events 同目录,文件名分键)。
SESSION_DIR_NAME = "telegram"

#: session 文件名(数据根 ``telegram/telethon.session``;telethon 会在同
#: 名加 ``-journal`` 伴生 SQLite 文件,权限同收紧)。
SESSION_FILE_NAME = "telethon.session"

#: session 文件权限(登录态 = 凭据面,主人/属组外零读写)。
SESSION_FILE_MODE = 0o600

#: 用户线宿主空闲心跳秒(事件由 handler 异步推,循环只看停止位)。
IDLE_TICK_SECONDS = 1.0

#: 媒体组跨事件记忆帽(相册 ≤10 媒体;键 = ``chat:grouped_id`` 唯一,
#: 滞留无害,FIFO 裁剪只防长跑增长)。
MEDIA_GROUP_MEMORY_CAP = 1000

#: session 失效类异常名(telethon errors;鸭子名匹配 —— 不硬 import,
#: 缺装 telethon 的宿主也能构造本模块)。
SESSION_DEAD_EXCEPTION_NAMES = frozenset(
    {
        "AuthKeyUnregistered",
        "AuthKeyError",
        "AuthKeyInvalid",
        "AuthKeyDuplicated",
        "UnauthorizedError",
    }
)

__all__ = [
    "DEFAULT_API_HASH_REF",
    "DEFAULT_API_ID_REF",
    "IDLE_TICK_SECONDS",
    "INSTALL_COMMAND",
    "MEDIA_GROUP_MEMORY_CAP",
    "SESSION_DEAD_EXCEPTION_NAMES",
    "SESSION_DIR_NAME",
    "SESSION_FILE_MODE",
    "SESSION_FILE_NAME",
    "TELETHON_PACKAGE",
    "TelethonLineError",
    "TelethonLoginFlow",
    "TelethonUserHost",
    "assemble_user_host",
    "default_data_root",
    "flood_wait_seconds",
    "require_telethon",
    "resolve_api_credentials",
    "session_path",
    "telethon_message_to_update",
]


class TelethonLineError(RuntimeError):
    """telethon 用户线的结构化失败(reason 词表见各构造点).

    Attributes:
        reason: ``dependency_missing`` / ``api_credentials_missing`` /
            ``api_credentials_invalid`` / ``session_missing`` /
            ``session_expired`` / ``phone_invalid`` / ``code_invalid`` /
            ``code_expired`` / ``flood_wait`` / ``login_failed``。
        fatal: True = 配置态/凭据态错误,重试无意义(宿主上抛、CLI 退码 1)。
    """

    def __init__(self, message: str, *, reason: str, fatal: bool = False) -> None:
        super().__init__(message)
        self.reason = reason
        self.fatal = fatal


def require_telethon() -> Any:
    """惰性 import telethon;缺装 → 结构化 ``dependency_missing``(simplex 判例).

    Returns:
        telethon 模块对象(``TelegramClient`` / ``events`` 等消费面由此取)。
    """
    try:
        return importlib.import_module(TELETHON_PACKAGE)
    except ImportError as exc:
        raise TelethonLineError(
            f"telethon 用户线依赖 {TELETHON_PACKAGE} 未安装:"
            f"请先执行 {INSTALL_COMMAND}(链接者组件轨,不影响 bot 线)",
            reason="dependency_missing",
            fatal=True,
        ) from exc


def flood_wait_seconds(exc: BaseException) -> float | None:
    """异常是否携带 FloodWait 等待秒(``.seconds`` 鸭子面);非限频 = None."""
    seconds = getattr(exc, "seconds", None)
    if (
        isinstance(seconds, (int, float))
        and not isinstance(seconds, bool)
        and seconds >= 0
    ):
        return float(seconds)
    return None


def default_data_root() -> Path:
    """引擎/登录流的数据根缺省(``$MYIA_HOME`` 或 cwd;CLI ``_cron_default_db``
    同口径 —— serve 装配的数据根 = ``--db`` 父目录,两口径在桌面/沙箱一致)。"""
    home = os.environ.get("MYIA_HOME")
    return Path(home) if home else Path.cwd()


def session_path(data_root: str | Path) -> Path:
    """session 文件路径(数据根 ``telegram/telethon.session``;确定性派生,
    不入 YAML —— 「session」是 schema 凭据后缀词,路径明文会被凭据扫描拒)。"""
    return Path(data_root) / SESSION_DIR_NAME / SESSION_FILE_NAME


def resolve_api_credentials(
    api_id_ref: str = DEFAULT_API_ID_REF,
    api_hash_ref: str = DEFAULT_API_HASH_REF,
    *,
    backend: Any | None = None,
) -> tuple[int, str]:
    """解析 api_id/api_hash 钥匙串引用 → ``(int, str)``。

    Raises:
        TelethonLineError: ``api_credentials_missing``(引用解析失败,附
            my.telegram.org 取值 + ``myssia secret set`` 指引)或
            ``api_credentials_invalid``(api_id 非数字)。
    """
    from myssia.schema import CredentialResolveError, resolve_credential

    guidance = (
        "取值:my.telegram.org 登录 → API development tools → Create new "
        "application → App api_id/api_hash;写入:"
        "myssia secret set myia/telegram/api-id 与 "
        "myssia secret set myia/telegram/api-hash;"
        "站点不可达(裸 ERROR/限流)时等恢复或换出口网络后重取自有对 —— "
        "勿用网上流传的文档示例对(2026-10-08 实证已被服务端拒)"
    )
    try:
        api_id_raw = resolve_credential(api_id_ref, backend=backend)
        api_hash = resolve_credential(api_hash_ref, backend=backend)
    except CredentialResolveError as exc:
        raise TelethonLineError(
            f"telethon api_id/api_hash 未配或解析失败({api_id_ref} / "
            f"{api_hash_ref}):{exc}\n{guidance}",
            reason="api_credentials_missing",
            fatal=True,
        ) from exc
    api_id_raw = api_id_raw.strip()
    if not api_id_raw.isdigit():
        raise TelethonLineError(
            f"telethon api_id 应为数字(my.telegram.org 的 App api_id),"
            f"当前解析值形状不符(值不落日志;ref={api_id_ref})\n{guidance}",
            reason="api_credentials_invalid",
            fatal=True,
        )
    return int(api_id_raw), api_hash.strip()


def _message_timestamp(message: Any) -> float | None:
    """telethon 消息时间(datetime)→ epoch 秒;缺失/异型 = None."""
    date = getattr(message, "date", None)
    if isinstance(date, datetime):
        return date.timestamp()
    if isinstance(date, (int, float)) and not isinstance(date, bool):
        return float(date)
    return None


def _chat_title(message: Any) -> str | None:
    """telethon 消息所属会话标题(best-effort;实体未缓存 = None)。"""
    chat = getattr(message, "chat", None)
    title = getattr(chat, "title", None) if chat is not None else None
    if isinstance(title, str) and title.strip():
        return title.strip()
    return None


def _sender_from(message: Any) -> dict[str, Any] | None:
    """发送者 → Bot API ``from`` 形状(best-effort,零额外请求:只看已缓存实体)。"""
    sender = getattr(message, "sender", None)
    if sender is None:
        return None
    username = getattr(sender, "username", None)
    if isinstance(username, str) and username.strip():
        return {"username": username.strip()}
    first = getattr(sender, "first_name", None)
    last = getattr(sender, "last_name", None)
    parts = [part for part in (first, last) if isinstance(part, str) and part.strip()]
    if not parts:
        return None
    from_info: dict[str, Any] = {"first_name": parts[0]}
    if len(parts) > 1:
        from_info["last_name"] = parts[1]
    return from_info


def telethon_message_to_update(message: Any) -> dict[str, Any]:
    """Telethon Message → Bot API update 形状 dict(消息面复用的唯一接缝).

    产出与 Bot API ``getUpdates`` 同形(``update_id``/``message`` 嵌套:
    message_id/date/chat.id/chat.title/from/text/media_group_id),下游
    :func:`~myssia.engines.telegram.updates_to_items` / 过滤管线 / ``#tg-``
    锚零改动复用。映射口径:

    - ``update_id`` = 消息 id(**本线账本命名空间内**的观测键 —— 文件按线
      分键,与任何 bot 的 update_id 序列互不可见;跨 chat 可撞号,账本行
      另有 chat_id/message_id 列锚定,观测面够用);
    - ``text`` = ``raw_text``(Telethon 对媒体 caption 也走该属性,与 Bot
      API 的 text/caption 双字段收拢为单面,聚合判例同语义);
    - ``media_group_id`` = ``grouped_id``(相册聚合键,转 str 对齐 Bot API);
    - ``from`` 缺席 = 无缓存实体(不为此发请求 —— 只读边界)。
    """
    chat_id = getattr(message, "chat_id", None)
    inner: dict[str, Any] = {
        "message_id": getattr(message, "id", None),
        "chat": {"id": chat_id, "title": _chat_title(message)},
    }
    timestamp = _message_timestamp(message)
    if timestamp is not None:
        inner["date"] = timestamp
    text = getattr(message, "raw_text", None)
    if isinstance(text, str) and text.strip():
        inner["text"] = text
    grouped_id = getattr(message, "grouped_id", None)
    if grouped_id is not None:
        inner["media_group_id"] = str(grouped_id)
    from_info = _sender_from(message)
    if from_info is not None:
        inner["from"] = from_info
    message_id = inner.get("message_id")
    update_id = message_id if isinstance(message_id, int) else -1
    return {"update_id": update_id, "message": inner}


def _harden_session_file(path: Path) -> None:
    """收紧 session 文件权限 0600(含 SQLite ``-journal`` 伴生件;best-effort)。"""
    for candidate in (path, path.with_name(path.name + "-journal")):
        try:
            if candidate.exists():
                candidate.chmod(SESSION_FILE_MODE)
        except OSError as exc:
            logger.warning(
                "telethon session 文件权限收紧失败 path=%s: %s", candidate, exc
            )


def assemble_user_host(
    telegram_dir: str | Path,
    bindings: Mapping[str, TelegramSourceBinding],
    backend: Any,
    store_item: Callable[[dict[str, Any]], bool],
    push_high_value: Callable[[dict[str, Any]], Awaitable[bool]],
    *,
    data_root: str | Path | None = None,
) -> tuple[Any, Any, str | None]:
    """用户线装配工厂(CLI serve 与桌面 entry 同门消费,B4).

    返回 ``(host, ledger, note)``:host 为 None 时 note 说明未起原因(结构化
    留痕,不抛 —— 用户线是增强线,绝不动摇 bot 线)。装配三态:

    - session 文件缺(未首登)→ note(常态,指引 ``myssia telegram login``);
    - api_id/api_hash 缺或 telethon 缺装 → note(附指引/安装命令);
    - 全在 → 建宿主;账本按 ``telethon-user:<api_id>`` 指纹分键(F8 判例,
      与任何 bot 的 events 文件互不可见,counts 不混计)。

    Args:
        telegram_dir: 数据根 ``telegram/`` 目录(offsets/events 的既有落点)。
        bindings: chat_id → 绑定(与 bot 线同品类同形)。
        backend: 钥匙串后端(装配方解析持有)。
        store_item / push_high_value: 出口 sink(与 bot 线装配同源同语义)。
        data_root: session 所在数据根(缺省 = ``telegram_dir`` 父目录)。
    """
    from myssia.telegram.events import TelegramEventLedger

    root = Path(data_root) if data_root is not None else Path(telegram_dir).parent
    session = session_path(root)
    if not session.exists():
        return None, None, (
            f"session 未首登({session};一次性前置:myssia secret set "
            "myia/telegram/api-id 与 myssia secret set myia/telegram/api-hash"
            "(my.telegram.org 取自有对;站点不可达时等恢复或换出口网络再取,"
            "勿用网上流传的文档示例对——已被服务端拒)后 myssia telegram login,"
            "建议挂小号)"
        )
    try:
        telethon = require_telethon()
        api_id, _api_hash = resolve_api_credentials(backend=backend)
    except TelethonLineError as exc:
        return None, None, str(exc)
    ledger = TelegramEventLedger(
        Path(telegram_dir) / "events.db", bot_token=f"telethon-user:{api_id}"
    )
    client = telethon.TelegramClient(str(session), api_id, _api_hash)
    host = TelethonUserHost(
        client=client,
        bindings=bindings,
        ledger=ledger,
        push_high_value=push_high_value,
        store_item=store_item,
    )
    return host, ledger, None


class TelethonLoginFlow:
    """session 首登 CLI 交互流(``myssia telegram login``;一次性).

    全输入面注入(``input_fn``/``password_fn``/``print_fn``/``client_factory``)
    —— 测试零交互零网络零真 telethon。交互序列:

    1. api_id/api_hash 钥匙串解析:缺 = 结构化失败(``api_credentials_missing``
       ,带 my.telegram.org 恢复/换出口再取自有对的人话指引;文档示例对已被
       服务端拒,兜底已移除);引用解析坏(非「缺」)同样结构化失败;
    2. 依赖门(require_telethon);
    3. session 已在(且未 ``--force``)→ 复用提示退出 0;``--force`` 删旧重登;
    4. connect → 已授权(竞态下 session 已活)→ 复用;
    5. 手机号 → ``send_code_request`` → 验证码 → ``sign_in``;
       2FA(``SessionPasswordNeededError``)→ 密码(不回显)→ ``sign_in``;
    6. session 落盘 0600,提示下一步。

    错误面全结构化(``TelethonLineError``;手机号/验证码/密码零落日志)。
    """

    def __init__(
        self,
        *,
        input_fn: Callable[[str], str] = input,
        password_fn: Callable[[str], str] | None = None,
        print_fn: Callable[[str], None] = print,
        client_factory: Callable[[str, int, str], Any] | None = None,
        backend: Any | None = None,
    ) -> None:
        if password_fn is None:
            import getpass

            password_fn = getpass.getpass
        self._input = input_fn
        self._password = password_fn
        self._print = print_fn
        self._client_factory = client_factory
        self._backend = backend

    # ------------------------------------------------------------------ run

    async def run(self, data_root: str | Path, *, force: bool = False) -> Path:
        """执行登录;成功返回 session 文件路径(已 0600)。

        Raises:
            TelethonLineError: 依赖/凭据/交互各面结构化失败(reason 词表
                见类文档;交互取消(inputempty)按 ``login_failed`` 收)。
        """
        # 凭据缺/坏 = 结构化失败上抛(api_credentials_missing 带 my.telegram.org
        # 恢复/换出口再取自有对指引;文档示例对已被服务端拒,无兜底 —— G1 移除)。
        api_id, api_hash = resolve_api_credentials(backend=self._backend)
        target = session_path(data_root)
        if target.exists() and not force:
            # 复用检查零依赖:session 在 = 已登录态,提示即出(未装 telethon
            # 也能答「你已经登录了」;真要用时引擎/宿主的依赖门会给出指引)。
            self._print(
                f"已有 telethon session({target}),直接复用;"
                "失效重登:myssia telegram login --force"
            )
            return target
        if target.exists():
            target.unlink()
            self._print(f"已删除旧 session(--force):{target}")
        # 依赖门只在真需要 telethon 时触发(注入 factory = 测试缝,零依赖)。
        if self._client_factory is not None:
            factory = self._client_factory
        else:
            factory = self._default_factory(require_telethon())
        client = factory(str(target), api_id, api_hash)
        try:
            await client.connect()
            if await client.is_user_authorized():
                self._print(f"session 已是登录态,直接复用:{target}")
                _harden_session_file(target)
                return target
            await self._sign_in_interactive(client)
        finally:
            disconnect = getattr(client, "disconnect", None)
            if callable(disconnect):
                result = disconnect()
                if hasattr(result, "__await__"):  # noqa: PT018 - telethon 双形态
                    await result
        _harden_session_file(target)
        if not target.exists():  # pragma: no cover - telethon 异型保存路径
            raise TelethonLineError(
                f"登录完成但 session 文件未落盘(预期 {target};"
                "请检查数据根可写性后重试)",
                reason="login_failed",
                fatal=True,
            )
        self._print(
            f"telethon session 已落盘(0600):{target}\n"
            "下一步:myssia telegram serve(bot+user 双线常驻;user 线读任意"
            "已加入群),或品类源 engine_options.telegram.mode: user 批量采集"
        )
        return target

    @staticmethod
    def _default_factory(telethon: Any) -> Callable[[str, int, str], Any]:
        def _make(session: str, api_id: int, api_hash: str) -> Any:
            return telethon.TelegramClient(session, api_id, api_hash)

        return _make

    async def _sign_in_interactive(self, client: Any) -> None:
        """手机号 → 验证码 →(2FA 密码)交互段;值零回显零落日志。"""
        phone = self._input("手机号(国际格式,如 +8613800138000):").strip()
        if not phone:
            raise TelethonLineError(
                "手机号为空,登录中止", reason="login_failed", fatal=True
            )
        try:
            await client.send_code_request(phone)
        except Exception as exc:  # noqa: BLE001 - telethon errors 家族统一收
            raise self._map_telethon_error(exc, stage="发送验证码") from exc
        self._print("验证码已发送(Telegram App 内信或短信)。")
        code = self._input("验证码:").strip()
        if not code:
            raise TelethonLineError(
                "验证码为空,登录中止", reason="login_failed", fatal=True
            )
        try:
            try:
                await client.sign_in(phone=phone, code=code)
            except Exception as exc:  # noqa: BLE001
                if type(exc).__name__ != "SessionPasswordNeededError":
                    raise
                password = self._password("两步验证密码(输入不回显):")
                await client.sign_in(phone=phone, password=password)
        except Exception as exc:  # noqa: BLE001
            raise self._map_telethon_error(exc, stage="登录") from exc
        self._print("登录成功。")

    @staticmethod
    def _map_telethon_error(exc: BaseException, *, stage: str) -> TelethonLineError:
        """telethon 异常 → 结构化错误(手机号/验证码值不进消息)。"""
        name = type(exc).__name__
        seconds = flood_wait_seconds(exc)
        if seconds is not None:
            return TelethonLineError(
                f"Telegram 限频(FloodWait):{stage}被要求等待 {seconds:.0f} 秒;"
                "服从退避 —— 请稍后重新执行 myssia telegram login",
                reason="flood_wait",
                fatal=True,
            )
        if name == "PhoneNumberInvalidError":
            return TelethonLineError(
                f"{stage}失败:手机号无效(应为国际格式,含国家码)",
                reason="phone_invalid",
                fatal=True,
            )
        if name in {"PhoneCodeInvalidError", "PhoneCodeEmptyError"}:
            return TelethonLineError(
                f"{stage}失败:验证码无效(重新执行 myssia telegram login 重取)",
                reason="code_invalid",
                fatal=True,
            )
        if name == "PhoneCodeExpiredError":
            return TelethonLineError(
                f"{stage}失败:验证码已过期(重新执行 myssia telegram login 重取)",
                reason="code_expired",
                fatal=True,
            )
        if name == "PasswordHashInvalidError":
            return TelethonLineError(
                f"{stage}失败:两步验证密码错误(重新执行 myssia telegram login)",
                reason="code_invalid",
                fatal=True,
            )
        return TelethonLineError(
            f"{stage}失败({name}):{exc}",
            reason="login_failed",
            fatal=True,
        )


class _NeverPoller:
    """用户宿主内嵌 bot 分派器的占位 poller(永不调用 —— run_forever 由
    用户宿主自己跑,分派器只借 ``dispatch_once`` 的消息面语义)。"""

    async def poll(self, offset: int) -> list[dict]:  # pragma: no cover - 防御
        raise AssertionError("telethon 用户线不得触发 bot 长轮询")


class TelethonUserHost:
    """serve 档 telethon 用户线:事件监听 → bot 线同款分派(出口/账本全复用).

    骨架(B3 宿主 + urlwatch 线程桥接判例):宿主本体是 asyncio 协程
    (``run_forever``),由装配方在**独立线程**以 ``asyncio.run`` 拉起
    (CLI serve / desktop entry 与 bot 线同款判例)—— telethon 客户端的
    事件循环即宿主循环,handler 与主循环同 loop 零跨线程桥。

    Args:
        client: telethon 客户端(已构造,session/api 凭据在装配方解析;
            测试注 fake)。
        bindings: chat_id → 绑定(与 bot 线同品类同形;两线共用品类时
            chat 语义一致)。
        ledger: 本线专属事件账本(装配方按 ``telethon-user:<api_id>``
            指纹分键,F8 判例)。
        push_high_value / store_item: 出口 sink(与 bot 线装配同源同语义,
            F14 bool 契约)。
        sleep: 异步 sleep 注入(测试 fake 记录退避/心跳)。
        should_stop: 停止判定(装配方注入线程 Event;None = 只靠取消)。
        new_message_filter: 事件过滤器构造(缺省 ``telethon.events.
            NewMessage()``;测试注 fake)。

    只读边界:客户端只被调 ``connect``/``is_user_authorized``/
    ``add_event_handler``/``disconnect`` —— 零写接口(design D4)。
    """

    def __init__(
        self,
        *,
        client: Any,
        bindings: Mapping[str, TelegramSourceBinding],
        ledger: Any,
        push_high_value: Callable[[dict[str, Any]], Awaitable[bool]],
        store_item: Callable[[dict[str, Any]], bool],
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        should_stop: Callable[[], bool] | None = None,
        new_message_filter: Callable[[], Any] | None = None,
        offsets: Any | None = None,
    ) -> None:
        self._client = client
        self._bindings = dict(bindings)
        self._sleep = sleep
        self._should_stop = should_stop
        self._new_message_filter = new_message_filter
        from myssia.telegram.offsets import OffsetStore

        self._dispatcher = TelegramServeHost(
            poller=_NeverPoller(),
            bindings=self._bindings,
            # 占位游标:用户线的更新断点由 telethon session 内部状态自持
            #(见模块文档),分派路径(dispatch_once)零 offset 面 —— 构造
            # 签名要求的这个 store 构造零 I/O 且永不被读写。
            offsets=offsets
            or OffsetStore(Path(SESSION_DIR_NAME) / "offsets-user.json"),
            ledger=ledger,
            push_high_value=push_high_value,
            store_item=store_item,
            sleep=sleep,
            should_stop=should_stop,
        )
        #: 媒体组跨事件记忆(``chat:grouped_id``;F13 语义在事件面 = 永久
        #: 记忆锚定组 + FIFO 裁剪 —— 相册成员逐事件到达,滚动一轮记忆会在
        #: 「无锚定事件的成员」处丢记忆,见 :meth:`_on_event`)。
        self._anchored_groups: OrderedDict[str, None] = OrderedDict()
        #: 生命周期观测(CLI 横幅/doctor 消费)。
        self.events = 0

    # ------------------------------------------------------------------ loop

    def _stopped(self) -> bool:
        return self._should_stop is not None and self._should_stop()

    async def run_forever(self) -> None:
        """主循环:连接(退避)→ 授权校验 → 事件监听 → 停止位退出。

        Raises:
            TelethonLineError: ``session_expired``/``session_missing``
                (fatal —— session 失效是凭据态,重试无意义;结构化上抛
                给装配方留痕,重登指引在错误消息里)。
        """
        logger.info(
            "telegram telethon 用户线启动 chats=%s(事件级监听,只读)",
            sorted(self._bindings),
        )
        try:
            connected = await self._connect_with_backoff()
            if connected:
                authorized = await self._client.is_user_authorized()
                if not authorized:
                    raise TelethonLineError(
                        "telethon session 未授权/已失效(session 文件在但登录态"
                        "不在 —— 常见于 session 被 Telegram 侧吊销或账号在别处"
                        "登出);重登:myssia telegram login --force",
                        reason="session_expired",
                        fatal=True,
                    )
                builder = self._new_message_filter or self._default_filter
                self._client.add_event_handler(self._on_event, builder())
                while not self._stopped():
                    await self._sleep(IDLE_TICK_SECONDS)
        except asyncio.CancelledError:
            logger.info("telegram telethon 用户线收到取消,正在退出")
            raise
        finally:
            disconnect = getattr(self._client, "disconnect", None)
            if callable(disconnect):
                try:
                    result = disconnect()
                    if hasattr(result, "__await__"):
                        await result
                except Exception:  # noqa: BLE001
                    logger.warning(
                        "telethon 用户线客户端断开失败(忽略)", exc_info=True
                    )
        logger.info("telegram telethon 用户线已退出 events=%s", self.events)

    def _default_filter(self) -> Any:
        """缺省事件过滤器(``telethon.events.NewMessage()``;依赖门在此触发)。"""
        telethon = require_telethon()
        return telethon.events.NewMessage()

    async def _connect_with_backoff(self) -> bool:
        """连接段:FloodWait 服从服务器指定秒数;其余异常指数退避 1s→300s。

        返回 False = 停止位在退避窗口内置位(干净退出,不硬连)。
        """
        backoff = BACKOFF_BASE_SECONDS
        while not self._stopped():
            try:
                await self._client.connect()
                return True
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 - 连接段全谱容错重试
                seconds = flood_wait_seconds(exc)
                if seconds is not None:
                    logger.warning(
                        "telethon 连接被限频(FloodWait),服从退避 %.0fs 后重试",
                        seconds,
                    )
                    await self._sleep(seconds + 1.0)
                    continue  # 服务器说了算,不计指数退避
                logger.warning(
                    "telethon 连接失败,%.1fs 后重试(帽 %.0fs): %s",
                    backoff,
                    BACKOFF_MAX_SECONDS,
                    exc,
                )
                await self._sleep(backoff)
                backoff = min(backoff * 2, BACKOFF_MAX_SECONDS)
        return False

    # ---------------------------------------------------------------- events

    async def _on_event(self, event: Any) -> None:
        """一条新消息事件 → Bot API 形状 → bot 线同款分派(单条一批)。

        媒体组(相册)成员逐事件到达:分派器的滚动记忆只保「上一批」,
        单条批会把记忆在无锚定成员处清空 —— 本宿主持**永久记忆**(锚定过
        的 ``chat:grouped_id`` 全量带入 skip,后到成员按并入吞掉,FIFO 帽
        :data:`MEDIA_GROUP_MEMORY_CAP` 防长跑增长)。
        """
        self.events += 1
        message = getattr(event, "message", None)
        if message is None:  # 非消息类 NewMessage 载荷(防御)
            return
        update = telethon_message_to_update(message)
        anchored = await self._dispatcher.dispatch_once(
            [update], skip_groups=set(self._anchored_groups)
        )
        for key in anchored:
            self._anchored_groups[key] = None
        while len(self._anchored_groups) > MEDIA_GROUP_MEMORY_CAP:
            self._anchored_groups.popitem(last=False)
