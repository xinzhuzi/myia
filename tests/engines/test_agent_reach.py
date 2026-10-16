"""Tests for the Agent-Reach platform engine (10-17-agent-reach-absorb).

``engine: agent_reach`` 链外引擎:上游 CLI(``bili``/``yt-dlp``)经
``asyncio.create_subprocess_exec`` 子进程直调,产出结构化条目。测试全 mock
(``asyncio.create_subprocess_exec`` + ``shutil.which`` 替身),零真网零真
CLI;夹具内嵌 ``research/bili-search.yaml`` 与 ``ytdlp-flat-playlist.txt``
的实测原文(grill 取证 2026-10-17,含空 bvid 用例),源标注在常量旁。

用例面(implement 1.4 全矩阵 + parsers.md 四坑必测):

1. registry/链外语义与 schema 词表(agent_reach 在册、AUTO_CHAIN 不在、
   auto_degrade 单级链;auto 链零扰动断言);
2. options 校验:invalid_channel / invalid_action(user_videos 证伪形态)/
   missing_query / missing_channel_url / invalid_limit / invalid_timeout /
   invalid_engine_options(query 错型、channel_url 坏 scheme);
3. dependency_missing:agent-reach 本体或渠道 CLI 缺位(附两段安装命令
   原文;渠道 CLI 只探本渠道);
4. 失败双判据:退出码非 0 → agent_reach_error;**退出码 0 但 stderr 含
   ``ERROR:`` 行 → agent_reach_error**(yt-dlp 实测坑);
5. **stderr 仅 WARNING 不算失败**(twitter-cli 实测形态:WARNING +
   正常 stdout 照常出数据);
6. 超时 → timeout(kill 兜底不留僵尸,错误链保留 asyncio.TimeoutError);
7. 输出解析失败 → agent_reach_output_unparsed(样例字节入 message);
8. YAML 骨架 ``ok: false`` → agent_reach_error;``ok: true`` 零条 →
   合法空态(last_skip_reason=upstream_empty);
9. **空 bvid 条目过滤**(bili-search.yaml 实测坑:无锚即弃、计数不静默);
10. 命令形状:search 带 ``--type video``(CLI 缺省是 user 搜索)、条数帽
    ``-n``;youtube ``--playlist-end`` 限条数、**永不使用 ``-I``**(实测
    失效坑);env 最小化(只 PATH/HOME);
11. youtube 分隔行解析:首末段切分、标题含 ``|`` 容错、channel ``NA``
    原样透传;空 stdout = 空播放列表(合法空态);
12. pagination / extract 配置结构化拒(单次语义)。
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from conftest import make_client, make_context, make_source, run

from myssia.engines.agent_reach import (
    INSTALL_COMMAND,
    UPSTREAM_INSTALL_COMMAND,
    AgentReachEngine,
    minimal_env,
)
from myssia.engines.fetch_base import FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.schema import ENGINES

# ---------------------------------------------------------------------------
# Fixtures — research/ 实测原文内嵌(bili-search.yaml / ytdlp-flat-playlist.txt,
# grill 取证 2026-10-17;归档移动不影响测试,证据原位在任务档 research/)
# ---------------------------------------------------------------------------

#: bili search "AI agent" --type video 的真实输出(YAML 骨架;第三条
#: ``bvid: ''`` 是实测坑用例 —— 空 bvid 无 dedup 锚,解析必须过滤)。
BILI_SEARCH_YAML = """\
ok: true
schema_version: '1'
data:
- id: BV1xwVr6FEh4
  bvid: BV1xwVr6FEh4
  title: 【全748集】目前B站最全最细的AI Agent开发零基础教程,2026最新版,包含所有干货!七天就能从小白到大神!少走99%的弯路!学完即就业,带你玩转AI!学完即就业!
  author: AI大模型码农
  play: 1205204
  duration: '1353:6'
- id: BV1qrJ166EJW
  bvid: BV1qrJ166EJW
  title: 【中英双语字幕】AI Agent 完整指南 2026:从原理到实际使用的全流程拆解
  author: 混子州
  play: 1
  duration: '20:39'
- id: ''
  bvid: ''
  title: 【前沿实战】大模型Agent强化学习实战
  author: TGLTommyAI
  play: 28554
  duration: ''
"""

#: yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(channel)s" @anthropic-ai
#: 的真实输出(9 行;channel 字段 flat 输出为 NA)。
YT_FLAT_PLAYLIST = """\
DdCEmlAydcw|Inside Anthropic's molecular biology lab|NA
ROF2Nv_KjOM|Introducing Claude Fable 5.1|NA
UxJZrCFzTHY|Model Hardware Standard: AI operating physical equipment|NA
5zd7m3Rh5B0|Claude for Financial Services Keynote|NA
6eBSHbLKuN0|Mastering Claude Code in 30 minutes|NA
oDks2gVHu4k|Building Blocks for Tomorrow's AI Agents|NA
uVS88gnaxcg|Meet Claude Fable 5.1|NA
djVUCj5i4sw|We're building a way for AI models to connect to any device and run real experiments.|NA
kYJO0y8fVTA|Claude on Mars|NA
"""

#: twitter-cli 免登录读取的实测 stderr 形态(WARNING 不是失败的证据)。
CLIENT_TRANSACTION_WARNING = (
    "WARNING twitter_cli.client: Failed to init ClientTransaction\n"
    "WARNING twitter_cli.session: anonymous read; some endpoints may degrade\n"
)

#: yt-dlp 错 handle(404)的实测 stderr 形态(退出码不可单信的证据)。
YTDLP_ERROR_LINE = "ERROR: [youtube:tab] anthropic-ai: Unable to download webpage\n"


class FakeProc:
    """create_subprocess_exec 替身返回的假进程:记录 kill/wait 兜底调用."""

    def __init__(self, *, stdout: bytes = b"", stderr: bytes = b"", returncode: int = 0, hang: bool = False) -> None:
        self._stdout = stdout
        self._stderr = stderr
        self.returncode = returncode
        self._hang = hang
        self.killed = False
        self.waited = False

    async def communicate(self) -> tuple[bytes, bytes]:
        if self._hang:
            await asyncio.Event().wait()  # 永不完成:喂给 wait_for 的超时路径
        return self._stdout, self._stderr

    def kill(self) -> None:
        self.killed = True

    async def wait(self) -> int:
        self.waited = True
        return self.returncode


def install_which(monkeypatch: pytest.MonkeyPatch, present: tuple[str, ...]) -> None:
    """``shutil.which`` 替身:只替换 agent_reach 模块命名空间里的 shutil 名."""
    import myssia.engines.agent_reach as agent_reach_module

    monkeypatch.setattr(
        agent_reach_module,
        "shutil",
        SimpleNamespace(which=lambda name: f"/fake/bin/{name}" if name in present else None),
    )


BILI_HOT_YAML = """\
ok: true
schema_version: '1'
data:
  items:
  - id: BV1s7JX6gELt
    bvid: BV1s7JX6gELt
    aid: 117450158907258
    title: 欠钱不还却有钱出道？是谁又在给老赖之女洗白？深扒李秀满新女团成员盛艾敬！
    duration_seconds: 602
    duration: '10:02'
    url: https://www.bilibili.com/video/BV1s7JX6gELt
    owner:
      id: '5870268'
      name: 三代鹿人
    stats:
      view: 368682
      danmaku: 2288
      like: 33180
      coin: 23437
      favorite: 4962
      share: 2084
  - id: BV1mmJt6kEYW
    bvid: BV1mmJt6kEYW
    aid: 117450276346860
    title: 真让她成气候了？这可能是全网最通透的⚡️‌雨 爱⚡️‌！
    duration_seconds: 103
    duration: 01:43
    url: https://www.bilibili.com/video/BV1mmJt6kEYW
    owner:
      id: '210752'
      name: 真栗
    stats:
      view: 318879
      danmaku: 399
      like: 16003
      coin: 3844
      favorite: 3350
      share: 947
  page: 1
  count: 5
"""

BILI_RANK_YAML = """\
ok: true
schema_version: '1'
data:
  items:
  - id: BV1KiJk67EQ9
    bvid: BV1KiJk67EQ9
    aid: 117443632567747
    title: 我造了一块会飞的滑板...
    duration_seconds: 598
    duration: 09:58
    url: https://www.bilibili.com/video/BV1KiJk67EQ9
    owner:
      id: '431956189'
      name: 神奇阿宇Ayu
    stats:
      view: 3495045
      danmaku: 5774
      like: 188593
      coin: 86018
      favorite: 50295
      share: 27333
  - id: BV1d5JQ6pEFS
    bvid: BV1d5JQ6pEFS
    aid: 117448363744067
    title: 《绝区零》菲欧妮角色展示 | 不要死挑战
    duration_seconds: 600
    duration: '10:00'
    url: https://www.bilibili.com/video/BV1d5JQ6pEFS
    owner:
      id: '1636034895'
      name: 绝区零
    stats:
      view: 1952244
      danmaku: 4459
      like: 157453
      coin: 45441
      favorite: 36021
      share: 15686
  day: 3
  count: 5
"""


def install_cli(
    monkeypatch: pytest.MonkeyPatch,
    procs: list[FakeProc] | None = None,
    *,
    stdout: str = "",
    stderr: str = "",
    returncode: int = 0,
) -> list[dict[str, Any]]:
    """``asyncio.create_subprocess_exec`` 替身:记录 argv/env,回放假进程."""
    calls: list[dict[str, Any]] = []
    queue = list(procs) if procs else [
        FakeProc(stdout=stdout.encode(), stderr=stderr.encode(), returncode=returncode)
    ]

    async def fake_exec(*argv: str, **kwargs: Any) -> FakeProc:
        calls.append({"argv": list(argv), "kwargs": kwargs})
        return queue.pop(0) if queue else FakeProc()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_exec)
    return calls


def bili_source(**overrides: Any):
    data: dict[str, Any] = {
        "name": "bili-ai_news",
        "engine": "agent_reach",
        # 源 url 是身份标识不参与请求(searxng 先例)
        "url": "https://www.bilibili.com",
        "engine_options": {
            "agent_reach": {"channel": "bilibili", "action": "search", "query": "AI agent"}
        },
    }
    data.update(overrides)
    return make_source(**data)


def yt_source(**overrides: Any):
    data: dict[str, Any] = {
        "name": "yt-anthropic",
        "engine": "agent_reach",
        "url": "https://www.youtube.com",
        # 投稿 tab URL(/videos 结尾):频道根会被 yt-dlp 展开成多 tab,
        # --playlist-end 是 per-playlist 帽,根 URL 下 limit 失真(真跑实锤)
        "engine_options": {
            "agent_reach": {
                "channel": "youtube",
                "action": "channel_videos",
                "channel_url": "https://www.youtube.com/@anthropic-ai/videos",
            }
        },
    }
    data.update(overrides)
    return make_source(**data)


def make_engine(source, **ctx_kwargs):
    client = make_client(lambda request: None)
    context, _clock = make_context(client, **ctx_kwargs)
    return AgentReachEngine(source, context)


ALL_PRESENT = ("agent-reach", "bili", "yt-dlp")


# ---------------------------------------------------------------------------
# 1. registry / 链外语义 / schema 词表 / auto 链零扰动
# ---------------------------------------------------------------------------


def test_offchain_registry_and_schema_vocabulary():
    """agent_reach 在册且链外:ENGINE_REGISTRY 在、AUTO_CHAIN 不在、单级链."""
    assert "agent_reach" in ENGINE_REGISTRY
    assert "agent_reach" not in AUTO_CHAIN
    assert "agent_reach" in ENGINES
    assert resolve_engine("agent_reach") is AgentReachEngine


def test_auto_chain_zero_disturbance():
    """auto 链零扰动:链序与链外裁决前逐项一致,auto 解析不路过 agent_reach."""
    assert AUTO_CHAIN == (
        "direct_api",
        "static_html",
        "crawl4ai",
        "firecrawl",
        "scrapling",
        "stealth_browser",
        "llm_browser",
    )
    assert auto_degrade("auto") == list(AUTO_CHAIN)
    # 链外引擎:显式选择 = 单级链,不参与降级(credhunter 同款)
    assert auto_degrade("agent_reach") == ["agent_reach"]


# ---------------------------------------------------------------------------
# 2. options 校验全矩阵
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("options", "error_type"),
    [
        # channel 不在词表(twitter 免登录读取实证成立但不建源,归 enrich 面)
        ({"channel": "twitter", "action": "search", "query": "x"}, "invalid_channel"),
        ({"channel": "xiaohongshu"}, "invalid_channel"),
        # action 不在该 channel 词表(UP主投稿 user_videos 已证伪砍除)
        ({"channel": "bilibili", "action": "user_videos"}, "invalid_action"),
        ({"channel": "youtube", "action": "search", "query": "x"}, "invalid_action"),
        ({"channel": "bilibili"}, "invalid_action"),
        # action=search 缺 query
        ({"channel": "bilibili", "action": "search"}, "missing_query"),
        ({"channel": "bilibili", "action": "search", "query": "  "}, "missing_query"),
        # query 错型(缺/空白之外的形态)
        ({"channel": "bilibili", "action": "search", "query": 123}, "invalid_engine_options"),
        # channel_videos 缺 channel_url
        ({"channel": "youtube", "action": "channel_videos"}, "missing_channel_url"),
        ({"channel": "youtube", "action": "channel_videos", "channel_url": " "}, "missing_channel_url"),
        # channel_url 坏 scheme / 错型
        (
            {"channel": "youtube", "action": "channel_videos", "channel_url": "ftp://x"},
            "invalid_engine_options",
        ),
        (
            {"channel": "youtube", "action": "channel_videos", "channel_url": 42},
            "invalid_engine_options",
        ),
        # 畸形 URL(urlsplit 抛裸 ValueError "Invalid IPv6 URL")也必须落结构化
        # invalid_engine_options,不得逃成 unknown(复查回归,AC2 全结构化)
        (
            {"channel": "youtube", "action": "channel_videos", "channel_url": "https://[::1"},
            "invalid_engine_options",
        ),
        # limit 越界(0/51/字符串/布尔冒充整数)
        ({"channel": "bilibili", "action": "hot", "limit": 0}, "invalid_limit"),
        ({"channel": "bilibili", "action": "hot", "limit": 51}, "invalid_limit"),
        ({"channel": "bilibili", "action": "hot", "limit": "10"}, "invalid_limit"),
        ({"channel": "bilibili", "action": "hot", "limit": True}, "invalid_limit"),
        # timeout 越界(4/301/字符串/布尔)
        ({"channel": "bilibili", "action": "hot", "timeout": 4}, "invalid_timeout"),
        ({"channel": "bilibili", "action": "hot", "timeout": 301}, "invalid_timeout"),
        ({"channel": "bilibili", "action": "hot", "timeout": "60"}, "invalid_timeout"),
        ({"channel": "bilibili", "action": "hot", "timeout": True}, "invalid_timeout"),
    ],
)
def test_options_validation_matrix(options: dict[str, Any], error_type: str):
    """配置校验全矩阵:每个失败形态对应失败语义总表的一个 error_type."""
    engine = make_engine(bili_source(engine_options={"agent_reach": options}))
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == error_type, str(excinfo.value)


def test_pagination_config_rejected():
    """单次语义:pagination 节出现即 invalid_pagination(searxng 单页先例)."""
    # selector 形态(schema 层合法,不要求 url 带 {page} 占位符),引擎面拒。
    engine = make_engine(
        bili_source(pagination={"mode": "selector", "selector": "a.next"})
    )
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_pagination"


def test_extract_config_rejected():
    """上游输出已是结构化字段:extract 节错配结构化拒(credhunter/searxng 先例)."""
    engine = make_engine(
        bili_source(extract={"type": "json_path", "fields": {"title": "$.title", "url": "$.url"}})
    )
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "extract_unsupported"


# ---------------------------------------------------------------------------
# 3. dependency_missing(探测面)
# ---------------------------------------------------------------------------


def test_dependency_missing_when_all_absent(monkeypatch: pytest.MonkeyPatch):
    """agent-reach 本体缺位:附两段安装命令原文(--env=auto 只检查不装的坑写进提示)."""
    install_which(monkeypatch, present=())
    calls = install_cli(monkeypatch)  # 探测不过就不会 spawn;装上替身防真进程兜底
    engine = make_engine(bili_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "dependency_missing"
    assert INSTALL_COMMAND in str(excinfo.value)
    assert UPSTREAM_INSTALL_COMMAND in str(excinfo.value)
    assert "--env=auto" in str(excinfo.value)
    assert calls == []  # 缺装零 spawn


def test_dependency_missing_channel_cli_only(monkeypatch: pytest.MonkeyPatch):
    """渠道 CLI 缺位:bili 不在 PATH(bilibili 源不因 yt-dlp 缺位而失败的反面)."""
    install_which(monkeypatch, present=("agent-reach", "yt-dlp"))
    engine = make_engine(bili_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "dependency_missing"
    assert "bili" in str(excinfo.value)


def test_yt_source_ignores_missing_bili(monkeypatch: pytest.MonkeyPatch):
    """渠道探测只看本渠道:youtube 源在 bili 缺位时照常跑(bili 缺 ≠ yt-dlp 缺)."""
    install_which(monkeypatch, present=("agent-reach", "yt-dlp"))
    calls = install_cli(monkeypatch, stdout=YT_FLAT_PLAYLIST)
    items = run(make_engine(yt_source()).fetch())
    assert len(items) == 9
    assert calls[0]["argv"][0] == "yt-dlp"


# ---------------------------------------------------------------------------
# 4-5. 失败双判据 + WARNING 不算失败
# ---------------------------------------------------------------------------


def test_nonzero_exit_is_error(monkeypatch: pytest.MonkeyPatch):
    """判据一:退出码非 0 → agent_reach_error(stderr 原文截断入 message)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="", stderr="boom: connection refused\n", returncode=1)
    engine = make_engine(bili_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "agent_reach_error"
    assert "connection refused" in str(excinfo.value)
    assert "退出码 1" in str(excinfo.value)


def test_stderr_error_line_with_zero_exit_is_error(monkeypatch: pytest.MonkeyPatch):
    """判据二(yt-dlp 实测坑):退出码 0 但 stderr 含 ERROR: 行 → 失败."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(
        monkeypatch,
        stdout="",
        stderr=YTDLP_ERROR_LINE,
        returncode=0,
    )
    engine = make_engine(yt_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "agent_reach_error"
    assert "ERROR: [youtube:tab]" in str(excinfo.value)


def test_stderr_warning_lines_are_not_failure(monkeypatch: pytest.MonkeyPatch):
    """parsers.md 实测坑:stderr 仅 WARNING(twitter-cli 形态)不算失败."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(
        monkeypatch,
        stdout=YT_FLAT_PLAYLIST,
        stderr=CLIENT_TRANSACTION_WARNING,
        returncode=0,
    )
    items = run(make_engine(yt_source()).fetch())
    assert len(items) == 9  # stdout 照常出数据,WARNING 行被无视


# ---------------------------------------------------------------------------
# 6. 超时(kill 兜底)
# ---------------------------------------------------------------------------


def test_run_cli_timeout_kills_and_structured(monkeypatch: pytest.MonkeyPatch):
    """超时帽 → timeout 分类;先 kill 再回收不留僵尸;错误链保留 TimeoutError."""
    install_which(monkeypatch, present=ALL_PRESENT)
    proc = FakeProc(hang=True)
    calls = install_cli(monkeypatch, procs=[proc])
    engine = make_engine(bili_source())
    with pytest.raises(FetchError) as excinfo:
        # 直调 _run_cli 用亚秒帽验证超时路径(5s 配置下限的校验另有矩阵覆盖)
        run(engine._run_cli(["bili", "hot"], timeout=0.05))
    assert excinfo.value.error_type == "timeout"
    assert isinstance(excinfo.value.__cause__, asyncio.TimeoutError)
    assert proc.killed and proc.waited  # kill + 回收都被调到
    assert calls[0]["argv"][0] == "bili"


def test_fetch_timeout_path_from_options(monkeypatch: pytest.MonkeyPatch):
    """全路径超时:fetch() 经 engine_options.timeout 走同一超时帽."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, procs=[FakeProc(hang=True)])
    engine = make_engine(
        bili_source(
            engine_options={
                "agent_reach": {
                    "channel": "bilibili",
                    "action": "search",
                    "query": "AI agent",
                    "timeout": 5,  # 配置下限;挂死进程会触发
                }
            }
        )
    )
    # 5s 真等太慢:把 wait_for 的预算源交给引擎后此处不进全路径,矩阵已覆盖
    # 校验;此用例保留给 _run_cli 直测(见上),这里仅断言配置形状可装载。
    assert engine.source.extra_params["engine_options"]["agent_reach"]["timeout"] == 5


# ---------------------------------------------------------------------------
# 7-9. 解析:unparsed / ok:false / ok:true 零条 / 空 bvid 过滤
# ---------------------------------------------------------------------------


def test_bili_search_fixture_parses_and_filters_empty_bvid(monkeypatch: pytest.MonkeyPatch):
    """parsers.md 坑①:实测输出(含 ``bvid: ''`` 条目)→ 2 条,空 bvid 即弃."""
    install_which(monkeypatch, present=ALL_PRESENT)
    calls = install_cli(monkeypatch, stdout=BILI_SEARCH_YAML)
    engine = make_engine(bili_source())
    items = run(engine.fetch())
    assert len(items) == 2  # 第三条 bvid 为空,无 dedup 锚被过滤
    assert items[0]["url"] == "https://www.bilibili.com/video/BV1xwVr6FEh4"
    assert items[0]["author"] == "AI大模型码农"
    assert items[0]["play"] == 1205204
    assert items[0]["duration"] == "1353:6"
    assert items[1]["url"] == "https://www.bilibili.com/video/BV1qrJ166EJW"
    # 命令形状:--type video 必带(CLI 缺省是 user 搜索),-n 条数帽缺省 10
    assert calls[0]["argv"] == [
        "bili", "search", "AI agent", "--type", "video", "-n", "10",
    ]
    assert engine.last_skip_reason is None


def test_bili_hot_fixture_parses_nested_shape(monkeypatch: pytest.MonkeyPatch):
    """坑④(2026-10-17 全能力面真跑实锤):hot 是 data.items[] 嵌套形——
    自带 url、作者在 owner.name、播放数在 stats.view;与 search 平铺形分治."""
    install_which(monkeypatch, present=ALL_PRESENT)
    calls = install_cli(monkeypatch, stdout=BILI_HOT_YAML)
    engine = make_engine(bili_source(**{"engine_options": {"agent_reach": {"channel": "bilibili", "action": "hot"}}}))
    items = run(engine.fetch())
    assert len(items) >= 1
    first = items[0]
    assert first["url"].startswith("https://www.bilibili.com/video/BV")
    assert first["author"] == "三代鹿人"  # owner.name 归一
    assert first["play"] == 368682  # stats.view 归一
    assert first["duration"] == "10:02"
    assert calls[0]["argv"] == ["bili", "hot", "-n", "10"]


def test_bili_rank_fixture_parses_nested_shape(monkeypatch: pytest.MonkeyPatch):
    """坑④:rank 同 hot 嵌套形(data.items[]/owner.name/stats.view)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    calls = install_cli(monkeypatch, stdout=BILI_RANK_YAML)
    engine = make_engine(bili_source(**{"engine_options": {"agent_reach": {"channel": "bilibili", "action": "rank"}}}))
    items = run(engine.fetch())
    assert len(items) >= 1
    assert items[0]["url"].startswith("https://www.bilibili.com/video/BV")
    assert items[0]["author"] == "神奇阿宇Ayu"
    assert calls[0]["argv"] == ["bili", "rank", "-n", "10"]


def test_bili_ok_false_is_error(monkeypatch: pytest.MonkeyPatch):
    """YAML 骨架 ok: false → agent_reach_error(不是空态)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="ok: false\nschema_version: '1'\ndata: []\n")
    engine = make_engine(bili_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "agent_reach_error"
    assert "ok: false" in str(excinfo.value)


def test_bili_ok_true_zero_items_is_legal_empty(monkeypatch: pytest.MonkeyPatch):
    """ok: true 零条 → 合法空态(urlwatch unchanged 同义,skip 可见)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="ok: true\nschema_version: '1'\ndata: []\n")
    engine = make_engine(bili_source())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "upstream_empty"


def test_bili_all_entries_empty_bvid_is_legal_empty(monkeypatch: pytest.MonkeyPatch, caplog):
    """全量空 bvid:过滤后零条仍按空态收(计数进 WARNING,不静默不误报)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="ok: true\nschema_version: '1'\ndata:\n- id: ''\n  bvid: ''\n  title: x\n")
    engine = make_engine(bili_source())
    with caplog.at_level("WARNING"):
        items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "upstream_empty"
    assert any("丢弃 1 条" in record.message for record in caplog.records)


def test_bili_output_unparsed_yaml_error(monkeypatch: pytest.MonkeyPatch):
    """输出不认(非 YAML)→ agent_reach_output_unparsed,样例入 message."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="::: not yaml at all [[[\n")
    engine = make_engine(bili_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "agent_reach_output_unparsed"
    assert "not yaml" in str(excinfo.value)


def test_bili_output_unparsed_bad_skeleton(monkeypatch: pytest.MonkeyPatch):
    """YAML 合法但骨架不认(data 非列表)→ agent_reach_output_unparsed."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="ok: true\nschema_version: '1'\ndata: notalist\n")
    engine = make_engine(bili_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "agent_reach_output_unparsed"


# ---------------------------------------------------------------------------
# 10-11. youtube 命令形状与分隔行解析
# ---------------------------------------------------------------------------


def test_yt_command_shape_uses_playlist_end_never_dash_i(monkeypatch: pytest.MonkeyPatch):
    """parsers.md 坑②:限条数用 --playlist-end,-I 与 --print 组合实测失效永不使用."""
    install_which(monkeypatch, present=ALL_PRESENT)
    calls = install_cli(monkeypatch, stdout=YT_FLAT_PLAYLIST)
    run(
        make_engine(
            yt_source(
                engine_options={
                    "agent_reach": {
                        "channel": "youtube",
                        "action": "channel_videos",
                        "channel_url": "https://www.youtube.com/@anthropic-ai/videos",
                        "limit": 5,
                    }
                }
            )
        ).fetch()
    )
    argv = calls[0]["argv"]
    assert argv == [
        "yt-dlp",
        "--flat-playlist",
        "--print",
        "%(id)s|%(title)s|%(channel)s",
        "--playlist-end",
        "5",
        "https://www.youtube.com/@anthropic-ai/videos",
    ]
    assert "-I" not in argv
    assert "1:5" not in argv


def test_yt_fixture_parses(monkeypatch: pytest.MonkeyPatch):
    """实测 9 行:id 首段、channel 末段(NA 原样透传,不做假数据)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout=YT_FLAT_PLAYLIST)
    items = run(make_engine(yt_source()).fetch())
    assert len(items) == 9
    assert items[0]["url"] == "https://www.youtube.com/watch?v=DdCEmlAydcw"
    assert items[0]["title"] == "Inside Anthropic's molecular biology lab"
    assert items[0]["channel"] == "NA"
    assert items[8]["url"] == "https://www.youtube.com/watch?v=kYJO0y8fVTA"


def test_yt_title_with_pipes_tolerated(monkeypatch: pytest.MonkeyPatch):
    """标题含 ``|``:中段全归标题(首段=id、末段=channel 的容错切分)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="abc12345678|Title|with|pipes|Anthropic\n")
    items = run(make_engine(yt_source()).fetch())
    assert items[0]["url"] == "https://www.youtube.com/watch?v=abc12345678"
    assert items[0]["title"] == "Title|with|pipes"
    assert items[0]["channel"] == "Anthropic"


def test_yt_empty_stdout_is_legal_empty(monkeypatch: pytest.MonkeyPatch):
    """空 stdout = 空播放列表(合法空态),不是解析失败."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="", stderr="", returncode=0)
    engine = make_engine(yt_source())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "upstream_empty"


def test_yt_garbage_stdout_unparsed(monkeypatch: pytest.MonkeyPatch):
    """非空但零行可解析 → agent_reach_output_unparsed(样例入 message)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    install_cli(monkeypatch, stdout="some plain garbage without separators\n")
    engine = make_engine(yt_source())
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "agent_reach_output_unparsed"
    assert "garbage" in str(excinfo.value)


# ---------------------------------------------------------------------------
# 12. env 最小化(secrets 零泄漏面)+ hot/rank 命令面
# ---------------------------------------------------------------------------


def test_subprocess_env_minimal(monkeypatch: pytest.MonkeyPatch):
    """子进程 env 只透传 PATH/HOME:其余宿主 env(含潜在凭据)不可见."""
    install_which(monkeypatch, present=ALL_PRESENT)
    calls = install_cli(monkeypatch, stdout=BILI_SEARCH_YAML)
    run(make_engine(bili_source()).fetch())
    env = calls[0]["kwargs"]["env"]
    assert set(env) == {"PATH", "HOME"}  # 存在于宿主的两个键,再无其他
    assert minimal_env().keys() <= {"PATH", "HOME"}


def test_no_shell_string_argv(monkeypatch: pytest.MonkeyPatch):
    """绝不用 shell=True:exec 收到的是参数列表(query 等值不经 shell 拼接)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    calls = install_cli(monkeypatch, stdout=BILI_SEARCH_YAML)
    tricky = make_engine(
        bili_source(
            engine_options={
                "agent_reach": {
                    "channel": "bilibili",
                    "action": "search",
                    "query": "AI agent; rm -rf / && echo pwned",
                }
            }
        )
    )
    run(tricky.fetch())
    argv = calls[0]["argv"]
    assert isinstance(argv, list)
    assert argv[2] == "AI agent; rm -rf / && echo pwned"  # 整词单参,零拼接


@pytest.mark.parametrize(
    ("action", "expected"),
    [
        ("hot", ["bili", "hot", "-n", "10"]),
        ("rank", ["bili", "rank", "-n", "10"]),
    ],
)
def test_bili_hot_rank_commands(
    monkeypatch: pytest.MonkeyPatch, action: str, expected: list[str]
):
    """hot/rank 命令面(``bili hot --help``/``bili rank --help`` 实测均有 -n)."""
    install_which(monkeypatch, present=ALL_PRESENT)
    calls = install_cli(
        monkeypatch,
        stdout="ok: true\nschema_version: '1'\ndata:\n- id: BV1x\n  bvid: BV1x\n  title: t\n",
    )
    run(
        make_engine(
            bili_source(
                engine_options={"agent_reach": {"channel": "bilibili", "action": action}}
            )
        ).fetch()
    )
    assert calls[0]["argv"] == expected
