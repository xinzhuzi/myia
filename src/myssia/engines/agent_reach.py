"""Agent-Reach 平台情报引擎 —— 上游 CLI 子进程直调,链外,零 import 本体.

Contract(PRD/design 10-17-agent-reach-absorb;解析器事实唯一依据
``.trellis/tasks/10-17-agent-reach-absorb/research/parsers.md``,grill 实测
2026-10-17 固化):

- **链外引擎**:``engine: agent_reach`` 显式选择才生效(``ENGINE_REGISTRY``
  在册、``AUTO_CHAIN`` 不在,credhunter/reddit/searxng 先例);显式选择 =
  单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。
  平台语义读取(搜索/投稿列表的结构化输出)与「URL→HTML」的降级链不同构,
  auto 永不路过(设计 §5 否决记录)。
- **零 import 本体**:Agent-Reach(Panniantong/Agent-Reach,MIT,98k★)是
  「安装器+多后端路由器+健康检查器」,真正干活的是它装好的上游 CLI
  (``bili`` / ``yt-dlp`` / ``twitter``)。本引擎经
  :func:`asyncio.create_subprocess_exec` 直调上游 CLI(参数列表显式构造,
  query 等值不经 shell 拼接,**绝不用 shell=True**),MYIA 核心不 import
  agent-reach 任何符号 —— 比 scrapling 的惰性 import 更进一步(连惰性
  import 都不需要);extras(钉 tag 直装 GitHub archive)只影响「装不装得
  上上游 CLI」,不影响核心装载。上游源码一行不改(链接者铁律)。
- **探测面(fetch 前零网络)**:``shutil.which("agent-reach")`` +
  渠道 CLI(``bili``/``yt-dlp``)任一缺位 → ``dependency_missing``,message
  附两段安装命令原文(``pip install 'myssia[agent-reach]'`` +
  ``agent-reach install --env local --channels bilibili``;v1.5.0 实测无
  ``--system`` 旗标)。落盘位置因安装方式而异(venv bin /
  ``~/.local/bin``,grill 实测),故 ``shutil.which`` 是唯一探测面,不硬编码
  路径;注意 ``install --env=auto`` 与 ``--safe`` 均只做安全检查**不真装**
  (输出原文 "No changes were made"),真装是 ``--env local`` 显式指定。全平台健康检查
  直接消费 ``agent-reach doctor --json``(每平台 status/backends/
  active_backend 一次拿齐),引擎不做逐 CLI 散测。
- **环境最小化(secrets 零泄漏面)**:子进程 env 只透传 ``PATH``/``HOME``
  (上游 CLI 需要定位 ``~/.agent-reach/``),其余 env 一律不传 —— 第一期
  零凭据,也不给未来凭据留泄漏面(设计 §3.2)。
- **失败双判据(yt-dlp 实测坑)**:退出码非 0 **或** stderr 含 ``ERROR:`` 行
  → ``agent_reach_error``(stderr 原文截断入 message)。yt-dlp 各版本失败
  退出码行为不可单信(错 handle 404 时 stderr 出现
  ``ERROR: [youtube:tab] ...`` 行而退出码可能正常);反之 **stderr 的
  ``WARNING`` 行不是失败**(twitter-cli 实测:免登录读取必带
  ClientTransaction WARNING 但 ``ok: true`` 照常出数据)。stdout 是判据,
  stderr 只认 ``ERROR:`` 前缀行。
- **YAML 骨架族**(bili-cli):输出 ``ok / schema_version / data[]`` 骨架,
  ``yaml.safe_load`` 直读;``ok: false`` → ``agent_reach_error``;``ok: true``
  零条 → **合法空态**零条目(源没更新不是故障,urlwatch unchanged 同义;
  置 ``last_skip_reason=upstream_empty`` 让 doctor 按健康跳过口径看待)。
  **必过坑:bili search 实测存在 ``bvid: ''`` 空条目,无锚即弃** —— 计数
  进日志 WARNING(不静默),其余条目照常。
- **分隔行族**(yt-dlp):``--flat-playlist --print "%(id)s|%(title)s|
  %(channel)s"`` 逐行 split;**限条数用 ``--playlist-end <N>**(``-I 1:3``
  与 ``--print`` 组合实测失效,打出 9 条,故引擎永不使用 ``-I``);标题含
  ``|`` 的行按「首段=id、末段=channel、中段全归标题」容错切分。空 stdout =
  空播放列表(合法空态);非空但一行都不认 → ``agent_reach_output_unparsed``
  (样例前 200 字节入 message,留上游格式升级的余地)。
- **单次语义**:``pagination`` 节出现即 ``invalid_pagination``(searxng
  单页先例);``extract`` 节错配结构化拒(上游输出已是结构化字段,归一
  映射按 parsers.md 白名单固化在 parser 内:title/url/author/published,
  published 两平台 flat 输出均无,不做假数据)。
- **条目锚**:bilibili ``https://www.bilibili.com/video/<bvid>``;youtube
  ``https://www.youtube.com/watch?v=<id>`` —— dedup 以条目 url 为锚全期
  生效(品类级 ``dedup.key: "{url}"``)。归一字段:bilibili
  title/author/play/duration;youtube title/channel(flat 输出 channel 为
  ``NA`` 原样透传);额外字段经 ``Item.from_extracted`` 落 metadata,模板
  经 item_view 可渲染。
- **礼貌**:上游 CLI 已做重试链,MYIA 不再叠加重试(PRD 约束 5);引擎在
  spawn 前按渠道目标 host 过一次既有 per-host 限速器(同域多源合并取最严
  qps,配额敏感平台源级 ``qps ≤ 0.2`` 必配);robots 面不适用平台官方
  API/CLI 通道(reddit「授权通道,robots.txt 不适用于钉死的官方端点」同款
  论证)。B站禁用 yt-dlp 抓取(上游明令),渠道→CLI 映射在常量表钉死。
- **超时帽**:整个子进程调用包 :func:`asyncio.wait_for`,预算
  ``engine_options.agent_reach.timeout``(缺省 60s,5-300)→ ``timeout``,
  超时先 ``kill()`` 再回收,不留僵尸进程。

源配置面(``engine_options.agent_reach``;源 url 是身份标识不参与请求,
searxng 先例):

- ``channel``(必填):``bilibili | youtube``;
- ``action``(必填):bilibili ``search | hot | rank``(免登录命令面全集,
  UP主投稿已证伪砍除)/ youtube ``channel_videos``;
- ``query``(action=search 必填):搜索词;
- ``channel_url``(action=channel_videos 必填):投稿 tab URL(以
  ``/videos`` 结尾);**频道根 URL 会被 yt-dlp 展开成多 tab**(Videos/
  Shorts/Live 各算一个 playlist,``--playlist-end`` 是 per-playlist 帽,
  真跑实锤根 URL 下 limit 10 出 25 条),投稿监控必须指到 tab;handle 先
  核对(如 Anthropic 官方是 ``@anthropic-ai``,错 handle 报 404);
- ``limit``(可选):单次条数帽,缺省 10,1-50;
- ``timeout``(可选):子进程超时秒,缺省 60,5-300。

失败语义总表(设计 §3.4,全部结构化 :class:`FetchError`,源级隔离):

===============================  =========================================
error_type                       触发
===============================  =========================================
``dependency_missing``           agent-reach / 渠道 CLI 缺位(附安装命令原文)
``invalid_channel``              channel 不在词表
``invalid_action``               action 不在该 channel 词表
``invalid_limit``                limit 越界(1-50)
``invalid_timeout``              timeout 越界(5-300)
``missing_query``                action=search 缺 query
``missing_channel_url``          channel_videos 缺 channel_url
``invalid_pagination``           pagination 节出现(单次语义)
``agent_reach_error``            CLI 退出非 0 或 stderr 含 ``ERROR:`` 行;
                                 YAML 骨架 ``ok: false``
``agent_reach_output_unparsed``  输出不认(样例字节截断入 message)
``timeout``                      超时帽(命令与帽值入 message)
===============================  =========================================

Raises:
    FetchError: 见上表;``engine_options`` 形状错为
        ``invalid_engine_options``(credhunter/先例同款兜底类)。
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import shlex
import shutil
from typing import Any
from urllib.parse import urlsplit

import yaml

from myssia.engines.fetch_base import BaseEngine, FetchError

logger = logging.getLogger(__name__)

#: 引擎层标签(schema 引擎词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "PLATFORM_ROUTER"

#: extras 安装命令原文(dependency_missing 错误消息逐字携带,doctor 消费)。
INSTALL_COMMAND = "pip install 'myssia[agent-reach]'"

#: 上游工具安装命令原文(v1.5.0 实测参数面:无 --system 旗标,可选渠道
#: 枚举 twitter,xiaoyuzhou,xueqiu,xiaohongshu,reddit,bilibili,linkedin,all
#: ——不含 youtube,yt-dlp 随 pip 依赖直装;``--env=auto``/``--safe`` 均只
#: 检查不真装,grill 实测输出原文 "No changes were made")。
UPSTREAM_INSTALL_COMMAND = "agent-reach install --env local --channels bilibili"

#: 渠道词表与渠道→CLI 映射(B站禁用 yt-dlp 抓取,上游明令;twitter 免登录
#: 单条读取已实证但监控源形态价值弱,归 enrich 面后续档,不进词表)。
CHANNELS = ("bilibili", "youtube")
BILI_ACTIONS = ("search", "hot", "rank")
YT_ACTIONS = ("channel_videos",)
CHANNEL_CLIS: dict[str, str] = {"bilibili": "bili", "youtube": "yt-dlp"}

#: 渠道目标 host(限速器注册面;条目 URL 前缀同源)。
BILI_HOST_URL = "https://www.bilibili.com/"
BILI_VIDEO_URL_PREFIX = "https://www.bilibili.com/video/"
YT_HOST_URL = "https://www.youtube.com/"
YT_VIDEO_URL_PREFIX = "https://www.youtube.com/watch?v="

#: yt-dlp flat-playlist 的分隔行模板(parsers.md 实测固化;标题含 ``|`` 由
#: parser 首末段切分容错,不在模板面解决)。
YT_PRINT_TEMPLATE = "%(id)s|%(title)s|%(channel)s"

#: 单次条数帽缺省与边界(设计 §3.1)。
DEFAULT_LIMIT = 10
MIN_LIMIT = 1
MAX_LIMIT = 50

#: 子进程超时帽缺省与边界(秒,设计 §3.2):上游 CLI 自带重试链,预算宽于
#: 管线 HTTP 默认 30s 一档,5s 下限防误配 0 值秒杀。
DEFAULT_TIMEOUT_SECONDS = 60.0
MIN_TIMEOUT_SECONDS = 5.0
MAX_TIMEOUT_SECONDS = 300.0

#: stderr 原文入 message 的截断长度(排障够用,刷屏免了)。
STDERR_EXCERPT_CHARS = 400

#: 输出不认时样例字节入 message 的截断长度(设计 §3.3:前 200 字节)。
OUTPUT_SAMPLE_BYTES = 200

__all__ = [
    "BILI_ACTIONS",
    "BILI_HOST_URL",
    "BILI_VIDEO_URL_PREFIX",
    "CHANNELS",
    "CHANNEL_CLIS",
    "DEFAULT_LIMIT",
    "DEFAULT_TIMEOUT_SECONDS",
    "INSTALL_COMMAND",
    "LAYER",
    "MAX_LIMIT",
    "MAX_TIMEOUT_SECONDS",
    "MIN_LIMIT",
    "MIN_TIMEOUT_SECONDS",
    "OUTPUT_SAMPLE_BYTES",
    "STDERR_EXCERPT_CHARS",
    "UPSTREAM_INSTALL_COMMAND",
    "YT_ACTIONS",
    "YT_HOST_URL",
    "YT_PRINT_TEMPLATE",
    "YT_VIDEO_URL_PREFIX",
    "AgentReachEngine",
    "minimal_env",
]


def minimal_env() -> dict[str, str]:
    """子进程环境最小化:只透传 ``PATH``/``HOME``,其余 env 一律不传。

    PATH 让 ``create_subprocess_exec`` 按探测面同源解析 CLI 路径,HOME 供
    上游 CLI 定位 ``~/.agent-reach/`` 配置;环境里的其余变量(含任何潜在
    凭据)对子进程不可见 —— 第一期零凭据,也不给未来凭据留泄漏面(设计
    §3.2,secrets 零泄漏判例)。键缺席于宿主环境时静默略过。
    """
    env: dict[str, str] = {}
    for key in ("PATH", "HOME"):
        value = os.environ.get(key)
        if value is not None:
            env[key] = value
    return env


class AgentReachEngine(BaseEngine):
    """平台情报源(显式 ``engine: agent_reach``;上游 CLI 子进程直调).

    items 出口对齐 ``Item.from_extracted`` 契约:url/title 管线键 + 渠道
    特有字段(author/play/duration/channel)落 metadata;url 是 dedup 锚
    根基(品类级 ``dedup.key: "{url}"``)。
    """

    LAYER = "PLATFORM_ROUTER"
    ENGINE_NAME = "agent_reach"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """``engine_options.agent_reach`` 校验与缺省化(错型即结构化拒).

        校验位置选 fetch 期(credhunter/prompt 先例)而非 schema 装载期
        (searxng queries 先例):渠道/action 组合约束是引擎私有词表,收在
        引擎内让 schema 保持引擎无关,错误仍结构化带字段路径语义。
        """
        options = self.engine_options()
        channel = options.get("channel")
        if channel not in CHANNELS:
            raise FetchError(
                f"engine_options.agent_reach.channel 应为 {'/'.join(CHANNELS)} 之一,"
                f"当前为 {channel!r}",
                error_type="invalid_channel",
            )
        allowed_actions = BILI_ACTIONS if channel == "bilibili" else YT_ACTIONS
        action = options.get("action")
        if action not in allowed_actions:
            raise FetchError(
                f"engine_options.agent_reach.action 在 channel={channel} 下应为"
                f" {'/'.join(allowed_actions)} 之一,当前为 {action!r}"
                "(bili 命令面无 UP主投稿命令,grill 实证;写操作不碰,链接者铁律)",
                error_type="invalid_action",
            )
        query: str | None = None
        if action == "search":
            raw_query = options.get("query")
            if raw_query is None or (isinstance(raw_query, str) and not raw_query.strip()):
                raise FetchError(
                    "action=search 必须提供 engine_options.agent_reach.query"
                    "(非空搜索词)",
                    error_type="missing_query",
                )
            if not isinstance(raw_query, str):
                raise FetchError(
                    f"engine_options.agent_reach.query 应为非空字符串,当前为 {raw_query!r}",
                    error_type="invalid_engine_options",
                )
            query = raw_query.strip()
        channel_url: str | None = None
        if action == "channel_videos":
            raw_url = options.get("channel_url")
            if raw_url is None or (isinstance(raw_url, str) and not raw_url.strip()):
                raise FetchError(
                    "action=channel_videos 必须提供 engine_options.agent_reach."
                    "channel_url(投稿 tab URL,以 /videos 结尾 —— 频道根会被"
                    " yt-dlp 展开成多 tab,--playlist-end 按 playlist 生效,"
                    "limit 帽会失真;handle 先核对,错 handle 报 404,"
                    "如 Anthropic 官方是 @anthropic-ai 不是 @AnthropicAI)",
                    error_type="missing_channel_url",
                )
            if not isinstance(raw_url, str):
                raise FetchError(
                    f"engine_options.agent_reach.channel_url 应为 http(s) URL 字符串,"
                    f"当前为 {raw_url!r}",
                    error_type="invalid_engine_options",
                )
            channel_url = raw_url.strip()
            try:
                parts = urlsplit(channel_url)
            except ValueError as exc:
                # urlsplit 对畸形 URL(如 https://[::1 的裸 IPv6 括号)抛裸
                # ValueError("Invalid IPv6 URL")—— 必须接住结构化,否则
                # classify_exception 归 "unknown" 逃出失败语义总表(AC2)。
                raise FetchError(
                    f"engine_options.agent_reach.channel_url 无法解析为 URL"
                    f"(畸形形态,如未闭合的 IPv6 括号):{exc};当前为 {channel_url!r}",
                    error_type="invalid_engine_options",
                ) from exc
            if parts.scheme not in ("http", "https") or not parts.netloc:
                raise FetchError(
                    f"engine_options.agent_reach.channel_url 应为 http(s) 地址,"
                    f"当前为 {channel_url!r}",
                    error_type="invalid_engine_options",
                )
        limit = options.get("limit", DEFAULT_LIMIT)
        if isinstance(limit, bool) or not isinstance(limit, int) or not MIN_LIMIT <= limit <= MAX_LIMIT:
            raise FetchError(
                f"engine_options.agent_reach.limit 应为 {MIN_LIMIT}-{MAX_LIMIT} 整数,"
                f"当前为 {limit!r}",
                error_type="invalid_limit",
            )
        timeout = options.get("timeout", DEFAULT_TIMEOUT_SECONDS)
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or not MIN_TIMEOUT_SECONDS <= timeout <= MAX_TIMEOUT_SECONDS
        ):
            raise FetchError(
                f"engine_options.agent_reach.timeout 应为 {MIN_TIMEOUT_SECONDS:.0f}-"
                f"{MAX_TIMEOUT_SECONDS:.0f} 的数值秒,当前为 {timeout!r}",
                error_type="invalid_timeout",
            )
        return {
            "channel": str(channel),
            "action": str(action),
            "query": query,
            "channel_url": channel_url,
            "limit": limit,
            "timeout": float(timeout),
        }

    # ---------------------------------------------------------- dependency

    def _probe_binaries(self, channel: str) -> None:
        """fetch 前零网络探测:agent-reach 本体 + 渠道 CLI 任一缺位即拒。

        落盘位置因安装方式而异(venv bin / ``~/.local/bin``,grill 实测),
        ``shutil.which`` 是唯一探测面。渠道 CLI 只探本渠道的(bilibili 源
        不因 yt-dlp 缺位而失败)。
        """
        cli = CHANNEL_CLIS[channel]
        missing = [name for name in ("agent-reach", cli) if shutil.which(name) is None]
        if missing:
            raise FetchError(
                f"agent-reach 上游组件缺位:{'/'.join(missing)} 不在 PATH;"
                f"请先执行 {INSTALL_COMMAND},再执行 {UPSTREAM_INSTALL_COMMAND}"
                "(--env=auto 只做安全检查不真装,必须 --system 显式授权;"
                "装完可用 agent-reach doctor --json 体检各平台状态)",
                error_type="dependency_missing",
            )

    # ---------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        options = self._options()
        self._probe_binaries(options["channel"])
        argv = self._build_argv(options)
        # 同域多源合并限速(配额敏感平台):spawn 前过一次既有 per-host
        # 限速器,qps 语义由源配置承担(≤0.2 礼貌档);上游 CLI 自带重试链,
        # MYIA 不再叠加重试。
        host_url = BILI_HOST_URL if options["channel"] == "bilibili" else YT_HOST_URL
        await self._acquire_rate_limit(host_url)
        returncode, stdout, stderr = await self._run_cli(argv, options["timeout"])
        failure = self._cli_failure(argv, returncode, stderr)
        if failure is not None:
            raise failure
        if options["channel"] == "bilibili":
            return self._parse_bilibili(stdout, argv)
        return self._parse_youtube(stdout, argv)

    def _build_argv(self, options: dict[str, Any]) -> list[str]:
        """渠道适配器:options → 上游命令(实测固化,设计 §4 命令表)。

        bilibili hot/rank 的 ``-n <limit>`` 按 ``bili hot --help`` /
        ``bili rank --help`` 实测(两命令均有 ``-n, --max``);search 的
        ``--type video`` 必带(CLI 缺省是 user 搜索)。youtube 限条数用
        ``--playlist-end``(``-I`` 与 ``--print`` 组合实测失效,永不使用)。
        """
        limit = str(options["limit"])
        if options["channel"] == "bilibili":
            if options["action"] == "search":
                assert options["query"] is not None  # _options() 已校验
                return ["bili", "search", options["query"], "--type", "video", "-n", limit]
            if options["action"] == "hot":
                return ["bili", "hot", "-n", limit]
            return ["bili", "rank", "-n", limit]
        assert options["channel_url"] is not None  # _options() 已校验
        return [
            "yt-dlp",
            "--flat-playlist",
            "--print",
            YT_PRINT_TEMPLATE,
            "--playlist-end",
            limit,
            options["channel_url"],
        ]

    async def _run_cli(self, argv: list[str], timeout: float) -> tuple[int, str, str]:
        """spawn 上游 CLI → ``(returncode, stdout, stderr)``(文本解码容错)。

        env 最小化(只 PATH/HOME);整个调用包 :func:`asyncio.wait_for`,
        超时先 kill 再回收(不留僵尸);探测与执行之间 CLI 消失
        (FileNotFoundError)按 ``dependency_missing`` 语义归类,其余启动
        失败归 ``agent_reach_error``。
        """
        try:
            proc = await asyncio.create_subprocess_exec(
                *argv,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=minimal_env(),
            )
        except FileNotFoundError as exc:
            raise FetchError(
                f"上游 CLI {argv[0]!r} 探测后在执行位消失(可能刚被卸载):{exc};"
                f"请重装:{INSTALL_COMMAND} 后 {UPSTREAM_INSTALL_COMMAND}",
                error_type="dependency_missing",
            ) from exc
        except OSError as exc:
            raise FetchError(
                f"上游 CLI {argv[0]!r} 启动失败:{exc};命令:{shlex.join(argv)}",
                error_type="agent_reach_error",
            ) from exc
        try:
            stdout_bytes, stderr_bytes = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError as exc:
            with contextlib.suppress(OSError):
                proc.kill()
            with contextlib.suppress(Exception):  # 回收失败不遮蔽超时主因
                await proc.wait()
            raise FetchError(
                f"agent-reach 上游命令超时(>{timeout:.0f}s 帽):{shlex.join(argv)}"
                "(上游 CLI 自带重试链,超帽即放弃本 run,下一 run 自然重试)",
                error_type="timeout",
            ) from exc
        returncode = proc.returncode if proc.returncode is not None else -1
        return (
            returncode,
            stdout_bytes.decode("utf-8", errors="replace"),
            stderr_bytes.decode("utf-8", errors="replace"),
        )

    def _cli_failure(self, argv: list[str], returncode: int, stderr: str) -> FetchError | None:
        """失败双判据:退出码非 0 **或** stderr 含 ``ERROR:`` 行 → 结构化失败。

        stderr 的 ``WARNING`` 行不是失败(twitter-cli 实测:免登录读取必带
        ClientTransaction WARNING 但 ``ok: true`` 照常出数据)—— stdout 才是
        数据判据,stderr 只认行首 ``ERROR:`` 前缀(yt-dlp 404 形态
        ``ERROR: [youtube:tab] ...``)。
        """
        error_lines = [line.strip() for line in stderr.splitlines() if line.strip().startswith("ERROR:")]
        if returncode == 0 and not error_lines:
            return None
        excerpt = stderr.strip()
        if len(excerpt) > STDERR_EXCERPT_CHARS:
            excerpt = f"{excerpt[:STDERR_EXCERPT_CHARS]}…(截断)"
        if not excerpt:
            excerpt = "(stderr 为空)"
        first_error = error_lines[0] if error_lines else ""
        return FetchError(
            f"agent-reach 上游命令失败(退出码 {returncode}"
            f"{'/stderr ERROR 行' if error_lines else ''}):{shlex.join(argv)}"
            f"{';首行:' + first_error if first_error else ''};stderr:{excerpt}",
            error_type="agent_reach_error",
        )

    # --------------------------------------------------------------- parsing

    def _parse_bilibili(self, stdout: str, argv: list[str]) -> list[dict]:
        """YAML 骨架族解析(search/hot/rank 三 action 全实测,2026-10-17
        全能力面真跑取证;坑④见 parsers.md):``ok/schema_version`` 同族,
        但 ``data`` 两形——search 是 **data[] 平铺**(author/play 平铺,
        无 url 需 bvid 拼);hot/rank 是 **data.items[] 嵌套**(自带 url,
        作者在 ``owner.name``、播放数在 ``stats.view``)。

        ``ok: false`` → ``agent_reach_error``;``ok: true`` 零条 → 合法空态
        (源没更新不是故障,urlwatch unchanged 同义);**空 bvid 条目过滤**
        (实测坑:无锚即弃,计数进 WARNING 不静默);形状不认 →
        ``agent_reach_output_unparsed``。
        """
        try:
            payload = yaml.safe_load(stdout)
        except yaml.YAMLError as exc:
            raise self._unparsed(stdout, f"YAML 解析失败:{exc}") from exc
        if not isinstance(payload, dict) or "ok" not in payload or "data" not in payload:
            raise self._unparsed(stdout, "缺 ok/data 骨架键")
        data = payload["data"]
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            entries: list[Any] = data["items"]  # 坑④:hot/rank 嵌套形
        elif isinstance(data, list):
            entries = data  # search 平铺形
        else:
            raise self._unparsed(stdout, f"data 非两形之一(列表/items 嵌套),实际 {type(data).__name__}")
        if payload["ok"] is not True:
            raise FetchError(
                f"agent-reach 上游骨架报 ok: false:{shlex.join(argv)};"
                f"stdout 样例:{self._sample(stdout)}",
                error_type="agent_reach_error",
            )
        items: list[dict] = []
        dropped = 0
        for entry in entries:
            if not isinstance(entry, dict):
                dropped += 1
                continue
            # 坑④:hot/rank 自带完整 url;search 需 bvid 拼(两形都要求 bvid
            # 兜底——url 缺失且 bvid 空即无 dedup 锚,弃)。
            url = entry.get("url")
            bvid = entry.get("bvid")
            if isinstance(url, str) and url.strip():
                item_url = url.strip()
            elif isinstance(bvid, str) and bvid.strip():
                item_url = f"{BILI_VIDEO_URL_PREFIX}{bvid.strip()}"
            else:
                # 实测坑:bili search 会混入 bvid 为空的条目 —— 无 dedup 锚
                # 即弃,计数不静默。
                dropped += 1
                continue
            item: dict[str, Any] = {"url": item_url}
            title = entry.get("title")
            if isinstance(title, str) and title.strip():
                item["title"] = title
            owner = entry.get("owner")
            author = entry.get("author") if not isinstance(owner, dict) else owner.get("name")
            if isinstance(author, str) and author.strip():
                item["author"] = author
            stats = entry.get("stats")
            play = entry.get("play") if not isinstance(stats, dict) else stats.get("view")
            if isinstance(play, int) and not isinstance(play, bool):
                item["play"] = play
            duration = entry.get("duration")
            if isinstance(duration, str) and duration.strip():
                item["duration"] = duration
            items.append(item)
        if dropped:
            logger.warning(
                "agent-reach bili 输出丢弃 %s 条(空 bvid/坏行,无 dedup 锚)"
                " source=%s items=%s",
                dropped,
                self.source.name,
                len(items),
            )
        if not items:
            self.last_skip_reason = "upstream_empty"
        return items

    def _parse_youtube(self, stdout: str, argv: list[str]) -> list[dict]:
        """分隔行族解析(yt-dlp ``--print`` 逐行,parsers.md)。

        首段=视频 id、末段=channel、中段全归标题(标题含 ``|`` 容错);
        空 stdout = 空播放列表(合法空态);非空但零行可解析 →
        ``agent_reach_output_unparsed``。channel 字段 flat 输出常为 ``NA``
        (原样透传,不做假数据)。
        """
        items: list[dict] = []
        bad = 0
        for line in stdout.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            parts = stripped.split("|")
            video_id = parts[0].strip()
            if len(parts) < 3 or not video_id:
                bad += 1
                continue
            channel = parts[-1].strip()
            title = "|".join(parts[1:-1]).strip()
            item: dict[str, Any] = {"url": f"{YT_VIDEO_URL_PREFIX}{video_id}", "channel": channel}
            if title:
                item["title"] = title
            items.append(item)
        if bad:
            logger.warning(
                "agent-reach youtube 输出 %s 行不认(已跳过,计数不静默)"
                " source=%s items=%s",
                bad,
                self.source.name,
                len(items),
            )
        if not items:
            if stdout.strip():
                raise self._unparsed(stdout, "分隔行零行可解析")
            self.last_skip_reason = "upstream_empty"
        return items

    @staticmethod
    def _sample(stdout: str) -> str:
        """输出样例前 200 字节形态(message 内展示,容错引号包裹)。"""
        text = stdout.strip()
        if len(text) > OUTPUT_SAMPLE_BYTES:
            text = f"{text[:OUTPUT_SAMPLE_BYTES]}…(截断)"
        return text if text else "(stdout 为空)"

    def _unparsed(self, stdout: str, reason: str) -> FetchError:
        """``agent_reach_output_unparsed`` 构造器(样例字节截断入 message)。"""
        return FetchError(
            f"agent-reach 上游输出无法解析({reason});样例:{self._sample(stdout)!r}"
            "(上游格式升级时留此余地:以实测重跑回填 research/parsers.md)",
            error_type="agent_reach_output_unparsed",
        )

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单次语义:任何 pagination 配置都结构化拒(不是只拒 scroll)。

        上游 CLI 一次一页(条数帽 ``-n`` / ``--playlist-end`` 内建),翻页
        属上游命令面的事,不在本引擎的游走面(searxng 单页先例)。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "agent_reach 引擎是单次语义(条数帽经 limit 内建,"
                "上游 CLI 自带分页参数面),不支持 pagination 配置",
                error_type="invalid_pagination",
            )
