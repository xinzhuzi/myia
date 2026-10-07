"""Telegram Bot API 窗口引擎 —— getUpdates 批量拉取,链外,凭据可选(10-06).

``engine: telegram`` 显式选择才生效(链外注册,reddit/urlwatch/prompt 判例):
``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式选择 =
单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

通道形态(design D2 双模式):

**bot 模式**(缺省,阶段一 bot 线;PRD 10-06-telegram-telethon;httpx 直调
零依赖,**不引 PTB/aiogram** —— 调研 §1:python-telegram-bot 29.5k★ 只借其
分层思想,MYIA 手搓同 Hermes 网关手法):

1. GET ``https://api.telegram.org/bot<token>/getUpdates?limit=N&timeout=0``
   (不带 offset = 未确认窗口从头拉;批量档不做长轮询 —— 25s 挂起属 serve
   档(``myssia telegram serve``,另文件)的常驻语义);
2. 客户端按 ``engine_options.telegram.chat_id`` 过滤(serve 级单 bot 多群
   各配一源,更新流按群分拣),消息文本 = 条目,锚点幂等见下;
3. 成功解析后跟一发**确认请求**(``offset=<max_update_id>+1``,best-effort):
   服务器据此丢弃 ≤ max 的已处理更新,窗口不随时间滚雪球;确认失败只告警
   —— 锚点去重兜底正确性,下一轮重拉被管线拦掉。⚠ 多群共用同一 bot 时
   确认是**全 bot 语义**(A 群源的确认会把 B 群未处理更新一并丢弃)——
   单 bot 单群(Grill Q2:首批仅 mihomo_party_group)或全部走 serve 档
   (offset 持久 + 逐条分拣)即可规避,扩群时再议。

**锚点幂等**(prompt ``#prompt-`` 判例):条目 URL = ``<源url>#tg-<chat_id>-
<message_id>`` —— 消息 id 群内单调递增,锚全期唯一,品类 ``dedup.key:
{url}`` 同条消息只进一次(编辑消息重投同 id → 同锚 → 天然吞掉;锚不改变
落点)。**媒体组聚合**:同 ``media_group_id`` 的多条消息(相册/多图)聚合
为一条 —— 取组内首条有 text/caption 的消息铸锚,纯媒体无文本整组跳过
(零文本无可筛面)。跨轮/跨窗口切组的残余重复面:serve 档由调用方传
``skip_groups``(上一轮铸锚组前缀保留一轮,深审 F13);批量档窗口重拉
自带未确认重叠,残余概率面由锚点去重兜底(如实注记,不引跨轮状态)。

**user 模式**(B4,``engine_options.telegram.mode: user``):Telethon 账号
session(MTProto)拉同一群的窗口消息 —— bot 进不去的群由已加入的账号读
(PRD 阶段二)。语义与 bot 模式同一份:同一 ``#tg-`` 锚(同群两模式消息 id
同命名空间)、同一媒体组聚合、同一过滤挂点;差别只在取数通道 ——
``iter_messages`` 单轮窗口(``lookback_limit`` 同帽),**无确认请求**
(offset 确认是 Bot API 独有语义)。凭据三态(bot 判例 + 两件):

- telethon 缺装 → 结构化 ``dependency_missing``(extras ``myssia[telethon]``
  组件轨,crawl4ai 判例);
- api_id/api_hash 引用缺/解析失败 → ``credential_missing`` 显式空态零请求
  (指引 my.telegram.org + ``myssia secret set``);
- session 文件缺(未首登)→ ``session_missing`` 显式空态零请求(指引
  ``myssia telegram login``;主人小号+验证码的一次性前置);
- session 在而登录态失效 → 结构化 ``session_expired``(重登指引
  ``myssia telegram login --force`` —— 不静默,design D4)。

只读边界(user 模式):引擎只 ``connect``/``is_user_authorized``/
``iter_messages``/``disconnect``,零写接口;限频走 telethon 内建 FloodWait
服从(引擎面捕获后结构化 ``telegram_flood_wait`` 带服务器指定秒数)。
session 路径确定性派生(``$MYIA_HOME`` 或 cwd 下 ``telegram/telethon.session``,
``myssia telegram login`` 的落点)—— 不入 YAML(「session」是 schema 凭据
后缀词,路径明文会被凭据扫描拒)。

**凭据三态**(reddit 判例,核心决议:凭据可选,绝不拦核心):

- **未配置**(``bot_token`` 引用缺)→ 结构化 ``credential_missing`` 显式
  空态:零请求、:attr:`last_skip_reason` 置位、日志人话指引(主人四步:
  BotFather 建 bot → ``/setprivacy`` 关隐私模式 → ``myssia secret set
  myia/telegram/bot-token`` → 拉进目标群);
- **引用在而解析失败**(钥匙串键未写等)→ 同空态 + warning 留痕;
- **解析成功** → 正常拉取。token 坏(401)→ 结构化 ``http_401``(不重试
  无意义值,提示 token 失效/被 revoke)。

**凭据零外显**(saas/reddit 同款纪律):token 走 URL path
(``/bot<token>/getUpdates``)—— 一切落日志/错误消息的 URL 一律过
:func:`mask_bot_url`(``/bot***/``);httpx 异常 str 自带完整 URL,包装
FetchError 前先净化(错误分类不净化,消息净化)。

robots 论证(reddit 同口径):api.telegram.org 的 robots 面对授权 Bot API
通道无意义 —— 合规面在 Bot API 条款(bot token 即授权凭证),引擎只保留
通用礼貌(限速 + 重试退避),不经 ``_ensure_robots_allowed``;该豁免只属
本模块钉死的官方端点常量。

其余边界:单轮窗口语义(``lookback_limit`` 1-100 缺省 100,getUpdates 硬
顶;无翻页 —— 长轮询/offset 持久是 serve 档的形态);409 冲突(serve 档
同 bot 在线长轮询互斥)→ 结构化 ``telegram_conflict`` 带指引;代理骑共
享 HTTP 栈(direct/pool 语义原样)。

Raises:
    FetchError: engine_options 形状错 / 源 URL 不符契约、getUpdates HTTP
        失败(消息净化)、响应形状不符、pagination 配置(单轮窗口语义拒)。
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timezone
from typing import Any, Mapping
from urllib.parse import urlencode, urlsplit

import httpx

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchContext,
    FetchError,
    classify_exception,
)
from myssia.schema import CredentialResolveError, SourceConfig, resolve_credential
from myssia.telegram.filter import (
    DEFAULT_COARSE_KEYWORDS,
    DEFAULT_LLM_TIMEOUT_SECONDS,
    DEFAULT_SCORE_THRESHOLD,
    TelegramFilterConfig,
    TelegramFilterPipeline,
    merge_high_value,
)

logger = logging.getLogger(__name__)

#: 引擎名(schema ``EngineName`` 词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "OFFICIAL_BOT_API"

#: Bot API 宿主(源 URL 必须精确匹配;端点由引擎构造,token 在 path)。
API_HOST = "api.telegram.org"

#: Bot API 端点 scheme(源 URL 契约与请求构造共用)。
API_ORIGIN = "https://api.telegram.org"

#: 钥匙串缺省键(与 PRD/示范件一致;``myssia secret set`` 的落点)。
DEFAULT_TOKEN_KEY = "keychain:myia/telegram/bot-token"

#: user 模式 api_id/api_hash 缺省引用(B4;``myssia telegram login`` 的
#: 指引与 ``telethon_line`` 同源 —— 常量定义在本模块,telethon_line 反向
#: 复用(serve→engine 依赖方向已定,反引会成环)。
DEFAULT_API_ID_REF = "keychain:myia/telegram/api-id"
DEFAULT_API_HASH_REF = "keychain:myia/telegram/api-hash"

#: 单轮窗口帽(getUpdates limit 硬顶 100;缺省即顶 —— 群消息窗口宁可多拉
#: 靠锚点去重,不可漏)。
DEFAULT_LOOKBACK_LIMIT = 100
MAX_LOOKBACK_LIMIT = 100

#: 条目标题截断(消息文本可 4096 字,标题面给列表/日报用,全文在 content)。
TITLE_SNIPPET_CHARS = 100

#: token path 段的净化形态(URL 日志/错误消息统一过这个)。
_MASKED_TOKEN_PATH = "/bot***/"

#: ``/bot<token>/`` 路径段的捕获(净化用;token 形如 ``<数字>:<字母数字_-]>``,
#: 含冒号 —— 官方 token 语法,非 URL scheme 段)。
_TOKEN_PATH_RE = re.compile(r"/bot[A-Za-z0-9:_-]+/")

#: 纯文本消息之外可作 content 的字段(媒体组判例:文本缺失取 caption)。
_TEXT_FIELDS = ("text", "caption")

__all__ = [
    "API_HOST",
    "API_ORIGIN",
    "DEFAULT_API_HASH_REF",
    "DEFAULT_API_ID_REF",
    "DEFAULT_LOOKBACK_LIMIT",
    "DEFAULT_TOKEN_KEY",
    "LAYER",
    "MAX_LOOKBACK_LIMIT",
    "TITLE_SNIPPET_CHARS",
    "TelegramEngine",
    "mask_bot_url",
    "mask_token_text",
]


def mask_bot_url(url: str) -> str:
    """把 URL 里的 ``/bot<token>/`` 段净化为 ``/bot***/``(凭据零外显)."""
    return _TOKEN_PATH_RE.sub("/bot***/", url)


def mask_token_text(value: Any) -> str:
    """异常/消息文本净化:字符串里的 bot token path 段一律打码.

    公开导出(深审 F10):serve 档 poller 与本引擎共用同一净化纪律 ——
    httpx 异常 str 自带完整 URL(含 token path),拼进错误消息前必须过
    本门(引擎/serve 两档同款,不再是引擎私有件)。
    """
    if not isinstance(value, str):
        return str(value)
    return _TOKEN_PATH_RE.sub("/bot***/", value)


#: 引擎内部旧名(mask_token_text 的私有别名;既有调用面零扰动)。
_mask_text = mask_token_text


def message_text(message: dict[str, Any]) -> str | None:
    """消息可筛文本:text 优先、caption 兜底(媒体组判例),双缺 = None."""
    for field in _TEXT_FIELDS:
        value = message.get(field)
        if isinstance(value, str) and value.strip():
            return value
    return None


class TelegramEngine(BaseEngine):
    """Telegram Bot API 群消息窗口源(显式 ``engine: telegram``;凭据可选).

    内置 Telegram updates 形状解析,``extract`` 节必是错配(配置即结构化
    拒);单轮窗口语义,``pagination`` 节同理拒;items 出口对齐
    ``Item.from_extracted`` 契约:url(#tg- 锚,管线去重键)/title(文本截
    断)/content(全文),其余观测键(published/author/chat_id/…)进
    metadata。
    """

    LAYER = "OFFICIAL_BOT_API"
    ENGINE_NAME = "telegram"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    def __init__(
        self,
        source: SourceConfig,
        context: FetchContext,
        *,
        completer: Any | None = None,
    ) -> None:
        super().__init__(source, context)
        #: LLM 精筛完成层注入口(测试 fake;缺省过滤管线自建
        #: OpenAICompatClient,每轮一建一关 —— prompt 引擎资源卫生判例)。
        self._completer = completer

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """engine_options.telegram 校验与缺省化(错型即结构化拒)."""
        options = self.engine_options()
        mode = options.get("mode", "bot")
        if mode not in ("bot", "user"):
            raise FetchError(
                "engine_options.telegram.mode 应为 bot(Bot API,getUpdates)"
                f"或 user(Telethon 账号 session,MTProto),当前为 {mode!r}",
                error_type="invalid_engine_options",
            )
        chat_id = options.get("chat_id")
        if isinstance(chat_id, bool) or not isinstance(chat_id, (str, int)):
            raise FetchError(
                "engine_options.telegram.chat_id 应为群/频道数字 id(字符串或"
                f"整数,超级群形如 -100xxxx),当前为 {chat_id!r}",
                error_type="invalid_engine_options",
            )
        lookback = options.get("lookback_limit", DEFAULT_LOOKBACK_LIMIT)
        if (
            isinstance(lookback, bool)
            or not isinstance(lookback, int)
            or not 1 <= lookback <= MAX_LOOKBACK_LIMIT
        ):
            raise FetchError(
                f"engine_options.telegram.lookback_limit 应为 "
                f"1-{MAX_LOOKBACK_LIMIT} 整数(getUpdates 硬顶),当前为 {lookback!r}",
                error_type="invalid_engine_options",
            )
        result: dict[str, Any] = {
            "mode": mode,
            "chat_id": str(chat_id).strip(),
            "lookback_limit": lookback,
        }
        if mode == "bot":
            bot_token = options.get("bot_token", DEFAULT_TOKEN_KEY)
            if not isinstance(bot_token, str) or not bot_token.strip():
                raise FetchError(
                    "engine_options.telegram.bot_token 应为 env:/keychain: 凭据引用"
                    f"(缺省 {DEFAULT_TOKEN_KEY}),当前为 {bot_token!r}",
                    error_type="invalid_engine_options",
                )
            result["bot_token"] = bot_token.strip()
        else:
            # user 模式凭据引用(api_id/api_hash;bot_token 不参与)。
            for key, default_ref in (
                ("api_id", DEFAULT_API_ID_REF),
                ("api_hash", DEFAULT_API_HASH_REF),
            ):
                ref = options.get(key, default_ref)
                if not isinstance(ref, str) or not ref.strip():
                    raise FetchError(
                        f"engine_options.telegram.{key} 应为 env:/keychain: 凭据引用"
                        f"(缺省 {default_ref}),当前为 {ref!r}",
                        error_type="invalid_engine_options",
                    )
                result[key] = ref.strip()
        return result

    def _filter_options(self) -> TelegramFilterConfig:
        """过滤面配置(engine_options.telegram 过滤键;错型即结构化拒)."""
        return filter_config_from_options(self.engine_options())

    # ------------------------------------------------------- url & credentials

    def _parse_source_url(self) -> None:
        """源 URL 契约校验(零 I/O):``https://api.telegram.org`` 锚形态.

        源 URL 只是引擎锚(铸 #tg- 去重键 + 排障定位);请求端点由引擎全权
        构造,host 必须精确匹配 —— 把引擎指到别站只会换来误导性错误。
        """
        parsed = urlsplit(self.source.url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host != API_HOST or parsed.path not in ("", "/"):
            raise FetchError(
                f"telegram 引擎源 url 应为 https://{API_HOST} 锚形态"
                f"(路径留空;chat 配置在 engine_options.telegram.chat_id),"
                f"当前为 {self.source.url!r}",
                error_type="invalid_telegram_source_url",
            )

    def _bot_token(self) -> str | None:
        """解析 bot token 三态(见模块文档;None = 显式空态,由调用方落 skip)."""
        options = self._options()
        ref = options["bot_token"]
        try:
            token = resolve_credential(ref, backend=self.context.keychain_backend)
        except CredentialResolveError as exc:
            # 引用在而钥匙串未写/解析坏:空态 + warning 留痕(reddit 同口径)。
            logger.warning(
                "telegram 凭据引用解析失败,源降级为显式空态 source=%s ref=%s: %s",
                self.source.name,
                ref,
                exc,
            )
            return None
        if not token.strip() or token.strip() in {"token", "changeme"}:
            # 占位值视同未配置:零请求显式空态,不拿坏 token 去撞端点。
            logger.warning(
                "telegram bot token 引用 %s 解析为占位值,源降级为显式空态 source=%s",
                ref,
                self.source.name,
            )
            return None
        return token.strip()

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        self._parse_source_url()
        options = self._options()
        # 深审 F9:过滤面配置校验前移到任何 I/O 之前 —— 尤其必须早于
        # _confirm_updates(确认是全 bot 不可逆语义:服务器丢弃 ≤offset 的
        # 已处理更新;校验迟到一步 = 消息已被确认丢弃后才抛配置错,静默
        # 丢单。零 I/O 纯校验,提前到取数前还顺带省一轮无谓请求)。
        filter_config = self._filter_options()
        if options["mode"] == "user":
            return await self._fetch_impl_user(options, filter_config)
        token = self._bot_token()
        if token is None:
            self.last_skip_reason = "credential_missing"
            logger.info(
                "telegram 引擎未配凭据,显式空态 source=%s(本轮零请求;"
                "主人四步:BotFather 建 bot → /setprivacy 关闭隐私模式(否则看不到"
                "普通消息)→ myssia secret set myia/telegram/bot-token → 拉进目标群;"
                "chat_id=%s)",
                self.source.name,
                options["chat_id"],
            )
            return []
        payload = await self._fetch_updates(token, options["lookback_limit"])
        updates = self._extract_updates(payload)
        items = self._updates_to_items(updates, options["chat_id"])
        await self._confirm_updates(token, updates)
        final_items = await self._apply_filter(items, filter_config)
        logger.info(
            "telegram 窗口取得 source=%s chat_id=%s updates=%s items=%s"
            " (粗筛后出仓 %s)",
            self.source.name,
            options["chat_id"],
            len(updates),
            len(items),
            len(final_items),
        )
        return final_items

    async def _apply_filter(
        self, items: list[dict], filter_config: TelegramFilterConfig | None = None
    ) -> list[dict]:
        """过滤管线挂点(B2):粗筛 → LLM 精筛 → 高价值合并单条(组合铁律).

        零命中 / 降级纯粗筛均不拦出仓路径;高价值组经 :func:`merge_high_value`
        合并为**单条**(score=组内最高,route ``score >= 8 → immediate``
        一轮至多推一条),普通条目带 score 逐条出仓(archive 入库,合并日报
        「Telegram 群」分区承载)。精筛端点未配 = 降级纯粗筛(INFO 留痕,
        条目照常入库)—— 过滤是增强件,不是硬前置。

        ``filter_config``:_fetch_impl 已在确认请求前校验过的配置直传
        (深审 F9 时序);None = 此处再取(独立调用面兼容)。
        """
        if not items:
            return []
        pipeline = TelegramFilterPipeline(
            filter_config if filter_config is not None else self._filter_options(),
            completer=self._completer,
            keychain_backend=self.context.keychain_backend,
        )
        outcome = await pipeline.process(items)
        merged = merge_high_value(
            outcome.high_value, threshold=pipeline.config.score_threshold
        )
        return ([merged] if merged is not None else []) + outcome.normal

    async def _fetch_impl_user(
        self, options: dict[str, Any], filter_config: TelegramFilterConfig
    ) -> list[dict]:
        """user 模式窗口:Telethon ``iter_messages`` → 共用消息面(模块文档).

        凭据三态与错误面见模块文档(user 模式段);只读边界 = connect/
        is_user_authorized/iter_messages/disconnect 四面。session 路径 =
        ``$MYIA_HOME``(或 cwd)下 ``telegram/telethon.session``,与
        ``myssia telegram login`` 落点同口径。
        """
        from myssia.telegram.telethon_line import (
            TelethonLineError,
            default_data_root,
            flood_wait_seconds,
            require_telethon,
            resolve_api_credentials,
            session_path,
            telethon_message_to_update,
        )

        # 三态序:凭据/首登的显式空态(零请求,常设前置)先于依赖门 ——
        # 未配置用户拿到的是人话指引而不是安装命令;依赖门只拦「想用而未装」。
        try:
            api_id, api_hash = resolve_api_credentials(
                options["api_id"], options["api_hash"],
                backend=self.context.keychain_backend,
            )
        except TelethonLineError as exc:
            if exc.reason != "api_credentials_missing":
                raise FetchError(str(exc), error_type="invalid_engine_options") from exc
            self.last_skip_reason = "credential_missing"
            logger.info(
                "telegram user 模式 api_id/api_hash 未配,显式空态 source=%s"
                "(本轮零请求;取值:my.telegram.org → API development tools →"
                " myssia secret set myia/telegram/api-id 与"
                " myssia secret set myia/telegram/api-hash;"
                "站点不可达时等恢复或换出口网络再取,"
                "勿用网上流传的文档示例对(已被服务端拒)",
                self.source.name,
            )
            return []
        session = session_path(default_data_root())
        if not session.exists():
            self.last_skip_reason = "session_missing"
            logger.info(
                "telegram user 模式 session 未首登,显式空态 source=%s"
                "(零请求;一次性前置:myssia telegram login 交互输入手机号+"
                "验证码,建议挂小号风控隔离)",
                self.source.name,
            )
            return []
        try:
            telethon = require_telethon()
        except TelethonLineError as exc:
            raise FetchError(str(exc), error_type="dependency_missing") from exc
        client = telethon.TelegramClient(str(session), api_id, api_hash)
        updates: list[dict[str, Any]] = []
        try:
            await client.connect()
            if not await client.is_user_authorized():
                raise FetchError(
                    "telethon session 未授权/已失效(session 文件在但登录态不在,"
                    "常见于被 Telegram 侧吊销或账号在别处登出);"
                    "重登:myssia telegram login --force",
                    error_type="session_expired",
                )
            # iter_messages 新→旧吐;倒序归一到 Bot API 的时间序(锚与聚合
            # 对序不敏感,排序只为与 bot 线同观感)。
            async for message in client.iter_messages(
                int(options["chat_id"]), limit=options["lookback_limit"]
            ):
                updates.append(telethon_message_to_update(message))
            updates.reverse()
        except FetchError:
            raise
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - telethon errors 家族统一收
            raise self._map_user_fetch_error(exc) from exc
        finally:
            disconnect = getattr(client, "disconnect", None)
            if callable(disconnect):
                try:
                    result = disconnect()
                    if hasattr(result, "__await__"):
                        await result
                except Exception:  # noqa: BLE001 - 收尾失败不污染主结果
                    logger.warning("telethon 客户端断开失败(忽略)", exc_info=True)
        items = self._updates_to_items(updates, options["chat_id"])
        final_items = await self._apply_filter(items, filter_config)
        logger.info(
            "telegram user 窗口取得 source=%s chat_id=%s messages=%s items=%s"
            " (粗筛后出仓 %s)",
            self.source.name,
            options["chat_id"],
            len(updates),
            len(items),
            len(final_items),
        )
        return final_items

    @staticmethod
    def _map_user_fetch_error(exc: BaseException) -> FetchError:
        """user 模式取数异常 → 结构化 FetchError(FloodWait/失效/其余)."""
        from myssia.telegram.telethon_line import (
            SESSION_DEAD_EXCEPTION_NAMES,
            flood_wait_seconds,
        )

        seconds = flood_wait_seconds(exc)
        if seconds is not None:
            return FetchError(
                f"telethon FloodWait:服务器要求等待 {seconds:.0f} 秒"
                "(服从退避;批量档下轮排程自然重试,锚点去重兜底)",
                error_type="telegram_flood_wait",
            )
        name = type(exc).__name__
        if name in SESSION_DEAD_EXCEPTION_NAMES:
            return FetchError(
                f"telethon session 失效({name});"
                "重登:myssia telegram login --force",
                error_type="session_expired",
            )
        # MTProto 面:异常文本不含 token/api_hash(协议层凭据不在消息面),
        # 实体解析类失败(如账号未打开过该会话)如实透出便于排障。
        return FetchError(
            f"telethon user 模式拉取失败({name}): {exc}",
            error_type="telegram_user_failed",
        )

    async def _fetch_updates(self, token: str, lookback_limit: int) -> dict[str, Any]:
        """GET getUpdates(未确认窗口,零长轮询;限速 + 重试 + 消息净化).

        Raises:
            FetchError: ``http_4xx``(401 = token 失效 / 409 = serve 档冲突)、
                网络类(transport 净化)、``telegram_payload_malformed``。
        """
        query = urlencode(
            {
                "limit": lookback_limit,
                "timeout": 0,
                "allowed_updates": '["message"]',
            }
        )
        url = f"{API_ORIGIN}/bot{token}/getUpdates?{query}"
        await self._acquire_rate_limit(API_ORIGIN)
        try:
            response = await self._send_with_retry(
                "GET", url, headers={**self._headers}, log_url=mask_bot_url(url)
            )
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status == 401:
                hint = "(bot token 被拒:常见于 token 失效/revoke,重新找 BotFather 取)"
            elif status == 409:
                hint = (
                    "(getUpdates 冲突:同 token 的常驻宿主(myssia telegram serve"
                    "/webhook)在跑,批量档与其互斥 —— 常驻开着就不必排程采集)"
                )
            else:
                hint = ""
            raise FetchError(
                f"telegram getUpdates HTTP {status} endpoint={mask_bot_url(url)}"
                f": {exc.response.reason_phrase}{hint}",
                error_type=f"http_{status}",
            ) from exc
        except httpx.TransportError as exc:
            raise FetchError(
                f"telegram getUpdates 网络失败 endpoint={_MASKED_TOKEN_PATH}getUpdates: "
                f"{_mask_text(str(exc))}",
                error_type=classify_exception(exc),
            ) from self._wrap_proxy_transport_failure(exc)
        try:
            payload = response.json()
        except ValueError as exc:
            raise FetchError(
                f"telegram getUpdates 响应不是有效 JSON endpoint="
                f"{_MASKED_TOKEN_PATH}getUpdates: {exc}",
                error_type="json_decode",
            ) from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("ok"), bool):
            raise FetchError(
                "telegram getUpdates 响应缺 ok 字段或形状不符(端点应答非 Bot API "
                "契约形态)",
                error_type="telegram_payload_malformed",
            )
        if not payload["ok"]:
            # Bot API 错误应答:{"ok": false, "error_code": …, "description": …}
            error_code = payload.get("error_code")
            description = _mask_text(payload.get("description"))
            raise FetchError(
                f"telegram getUpdates 应答错误 error_code={error_code}: {description}"
                "(401 = token 失效;409 = 常驻宿主冲突)",
                error_type=f"telegram_api_{error_code if isinstance(error_code, int) else 'error'}",
            )
        if not isinstance(payload.get("result"), list):
            raise FetchError(
                "telegram getUpdates 响应缺 result 数组",
                error_type="telegram_payload_malformed",
            )
        return payload

    def _extract_updates(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        """result 数组 → message/edited_message 更新(其余类型跳过)."""
        updates: list[dict[str, Any]] = []
        for update in payload["result"]:
            if not isinstance(update, dict):
                continue
            for kind in ("message", "edited_message"):
                message = update.get(kind)
                if isinstance(message, dict):
                    updates.append(update)
                    break
        return updates

    async def _confirm_updates(
        self, token: str, updates: list[dict[str, Any]]
    ) -> None:
        """确认请求(offset=max+1;best-effort:失败只告警,锚点去重兜底)."""
        if not updates:
            return
        max_update_id = max(
            update.get("update_id", 0) for update in updates if isinstance(update, dict)
        )
        if not isinstance(max_update_id, int) or max_update_id <= 0:
            return
        url = (
            f"{API_ORIGIN}/bot{token}/getUpdates"
            f"?{urlencode({'offset': max_update_id + 1, 'limit': 1, 'timeout': 0})}"
        )
        await self._acquire_rate_limit(API_ORIGIN)
        try:
            await self._send_with_retry(
                "GET", url, headers={**self._headers}, log_url=mask_bot_url(url)
            )
        except Exception as exc:  # noqa: BLE001 - 确认是窗口卫生动作,失败不废源
            logger.warning(
                "telegram 窗口确认失败(忽略;锚点去重兜底正确性) source=%s: %s",
                self.source.name,
                _mask_text(str(exc)),
            )

    # --------------------------------------------------------------- mapping

    def _updates_to_items(
        self, updates: list[dict[str, Any]], chat_id: str
    ) -> list[dict]:
        """更新流 → 管线 items(群分拣/媒体组聚合/#tg- 锚;逐条目宽容)."""
        return updates_to_items(updates, chat_id, source_url=self.source.url)

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单轮窗口语义:任何 pagination 配置都结构化拒(urlwatch 判例).

        窗口即 lookback_limit 帽;长轮询/offset 游标是 serve 档的常驻形态,
        翻页模板/滚动对本引擎无意义。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "telegram 引擎是单轮窗口语义(lookback_limit 即窗口帽,"
                "常驻长轮询走 myssia telegram serve),不支持 pagination 配置",
                error_type="pagination_unsupported",
            )


def filter_config_from_options(
    options: Mapping[str, Any],
) -> TelegramFilterConfig:
    """engine_options.telegram 过滤键 → 过滤配置(引擎与 serve 装配共用).

    键面:keywords(缺省内置词表;空列表=关闭粗筛)/score_threshold(1-10,
    缺省 8,grill Q5)/model(缺省 glm-4-flash,enrich 同款)/llm_base_url+
    llm_api_key(成对 env:/keychain: 引用,明文拒;全缺=降级纯粗筛)/
    timeout(正数秒)。

    Raises:
        FetchError: ``invalid_engine_options``(类型/半配/引用形态)。
    """
    from myssia.schema import parse_secret_value

    keywords_option = options.get("keywords")
    if keywords_option is None:
        keywords = DEFAULT_COARSE_KEYWORDS
    elif isinstance(keywords_option, (list, tuple)):
        keywords_list: list[str] = []
        for word in keywords_option:
            if not isinstance(word, str) or not word.strip():
                raise FetchError(
                    f"engine_options.telegram.keywords 元素应为非空字符串,"
                    f"当前为 {word!r}",
                    error_type="invalid_engine_options",
                )
            keywords_list.append(word.strip())
        keywords = tuple(keywords_list)
    else:
        raise FetchError(
            f"engine_options.telegram.keywords 应为字符串列表(缺省内置"
            f"免费情报词表;空列表 = 关闭粗筛),当前为 {keywords_option!r}",
            error_type="invalid_engine_options",
        )
    threshold = options.get("score_threshold", DEFAULT_SCORE_THRESHOLD)
    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, int)
        or not 1 <= threshold <= 10
    ):
        raise FetchError(
            f"engine_options.telegram.score_threshold 应为 1-10 整数"
            f"(缺省 {DEFAULT_SCORE_THRESHOLD},grill Q5),当前为 {threshold!r}",
            error_type="invalid_engine_options",
        )
    model = options.get("model")
    if model is None:
        model_str = None
    elif isinstance(model, str) and model.strip():
        model_str = model.strip()
    else:
        raise FetchError(
            f"engine_options.telegram.model 应为非空模型名,当前为 {model!r}",
            error_type="invalid_engine_options",
        )
    timeout = options.get("timeout")
    if timeout is not None and (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise FetchError(
            f"engine_options.telegram.timeout 应为正数秒,当前为 {timeout!r}",
            error_type="invalid_engine_options",
        )
    base_ref = options.get("llm_base_url")
    key_ref = options.get("llm_api_key")
    if (base_ref is None) != (key_ref is None):
        raise FetchError(
            "engine_options.telegram.llm_base_url 与 llm_api_key 须成对配置"
            "(env:/keychain: 引用;全缺 = 降级纯粗筛的合法形态):当前 "
            f"llm_base_url={'已配' if base_ref is not None else '缺'} / "
            f"llm_api_key={'已配' if key_ref is not None else '缺'}",
            error_type="invalid_engine_options",
        )
    for label, ref in (("llm_base_url", base_ref), ("llm_api_key", key_ref)):
        if ref is None:
            continue
        if not isinstance(ref, str) or not ref.strip():
            raise FetchError(
                f"engine_options.telegram.{label} 应为 env:/keychain: 凭据引用"
                "字符串(prompt 引擎/enrich 同契约,明文拒)",
                error_type="invalid_engine_options",
            )
        try:
            parse_secret_value(ref, label=f"engine_options.telegram.{label}")
        except Exception as exc:
            raise FetchError(
                f"engine_options.telegram.{label} 必须是纯 env:/keychain:"
                f" 凭据引用(明文拒绝):{exc}",
                error_type="invalid_engine_options",
            ) from exc
    return TelegramFilterConfig(
        keywords=keywords,
        score_threshold=threshold,
        model=model_str or TelegramFilterConfig.model,  # 缺省 = glm-4-flash
        llm_base_url=base_ref.strip() if isinstance(base_ref, str) else None,
        llm_api_key=key_ref.strip() if isinstance(key_ref, str) else None,
        timeout=float(timeout)
        if timeout is not None
        else DEFAULT_LLM_TIMEOUT_SECONDS,
    )


    # --------------------------------------------------------------- mapping

def updates_to_items(
    updates: list[dict[str, Any]],
    chat_id: str,
    *,
    source_url: str,
    skip_groups: set[str] | None = None,
) -> list[dict]:
    """更新流 → 管线 items(群分拣/媒体组聚合/#tg- 锚;引擎与 serve 共用).

    B3 抽出为模块级函数:批量引擎(``engine: telegram``)与常驻宿主
    (``myssia telegram serve``)共用同一分拣/聚合/锚语义 —— 两档只差
    取数形态(窗口拉取 vs 长轮询),消息面语义一份(design D1)。

    ``skip_groups``(深审 F13):调用方持有的「已铸锚媒体组」前缀。长轮询
    分批边界会把同一 media_group_id(相册/多图)切到两轮 —— 轮内缓存对
    跨轮后到成员失效,后到的带 caption 成员会再出一条重复条目;serve 宿主
    把上一轮铸锚的组传入,后到成员按「并入首条」吞掉。批量档窗口重拉
    自带未确认重叠,无需传入(跨窗口重复面由锚点去重兜底,如实注记)。
    """
    # 群分拣:只留目标 chat 的消息(单 bot 多群 = 每群一源,各配 chat_id)。
    messages: list[dict[str, Any]] = []
    for update in updates:
        message = update.get("message") or update.get("edited_message")
        if not isinstance(message, dict):
            continue
        chat = message.get("chat")
        if not isinstance(chat, dict) or str(chat.get("id", "")) != chat_id:
            continue
        messages.append(message)
    # 媒体组聚合:同 media_group_id 取首条有文本的铸锚,整组出一条。
    seen_groups: set[str] = set(skip_groups or ())
    items: list[dict] = []
    for message in messages:
        media_group_id = message.get("media_group_id")
        text = message_text(message)
        if isinstance(media_group_id, str) and media_group_id:
            if media_group_id in seen_groups:
                continue  # 组内后续消息(纯图/重复 caption)并入首条
            if text is None:
                continue  # 组首无文本:不锁组,组内后续带文本的仍有机会
            seen_groups.add(media_group_id)
        if text is None:
            continue  # 无文本无 caption 的单发消息(贴纸/纯图):零可筛面,跳过
        items.append(message_to_item(message, text, source_url=source_url))
    return items



def message_to_item(
    message: dict[str, Any], text: str, *, source_url: str
) -> dict[str, Any]:
    """一条消息 → 管线条目(#tg- 锚 + 观测键;Item.from_extracted 契约)."""
    chat = message.get("chat") if isinstance(message.get("chat"), dict) else {}
    message_id = message.get("message_id")
    item: dict[str, Any] = {
        "url": f"{source_url}#tg-{chat.get('id')}-{message_id}",
        "title": text[:TITLE_SNIPPET_CHARS],
        "content": text,
    }
    date = message.get("date")
    if isinstance(date, (int, float)) and not isinstance(date, bool):
        item["published"] = datetime.fromtimestamp(date, tz=timezone.utc).isoformat()
    author = _author_label(message.get("from"))
    if author:
        item["author"] = author
    chat_title = chat.get("title")
    if isinstance(chat_title, str) and chat_title.strip():
        item["chat_title"] = chat_title.strip()
    if isinstance(message.get("media_group_id"), str):
        item["media_group_id"] = message["media_group_id"]
    # 观测键(B2/B3 消费):高价值合并锚区间与事件账本按消息 id 记账。
    item["chat_id"] = chat.get("id")
    item["message_id"] = message_id
    return item



def _author_label(sender: Any) -> str | None:
    """发送者可读标识:@username 优先,实名拼接兜底,双缺 = None."""
    if not isinstance(sender, dict):
        return None
    username = sender.get("username")
    if isinstance(username, str) and username.strip():
        return f"@{username.strip()}"
    parts = [
        part
        for part in (sender.get("first_name"), sender.get("last_name"))
        if isinstance(part, str) and part.strip()
    ]
    if parts:
        return " ".join(parts)
    return None
