"""Command-line entry point (stdlib argparse, no new deps).

Exit-code contract (spec python/error-handling — agent 与 CI 依赖):

=== ====== ==============================================================
码   含义   触发
=== ====== ==============================================================
0   成功   run 正常结束(含 dry-run);``--loop`` 干净退出;init/list/doctor
            完成;secret 操作成功;``--version`` / ``--help``
1   配置错误   品类 YAML 被 schema 拒载 / 明文凭据 / route 或规则配置非法 /
            用法错误(argparse)/ 插件目录不存在 / secret 结构化失败;
            错误结构化、含字段路径
2   采集全部失败   run:所有 source 采集失败;test:被试抓的源全部失败
3   部分失败   run:部分 source/条目或通道发送失败;test:部分源失败
=== ====== ==============================================================

argparse 的默认用法错误退出码是 2,与「采集全部失败」冲突 ——
``_Parser.error`` 改为抛 :class:`_UsageError`,统一归入退出码 1。
``--help`` / ``--version`` 仍按惯例以 0 退出(经 SystemExit 传播)。

输出双形态:人类可读摘要(stdout)与 ``--json`` 机器可读单份 JSON(可被
jq 解析)。日志走 logging 框架(stderr),``--json`` 模式下日志收敛到
WARNING;stdout 推送通道的卡片行在 ``--json`` 下也改写 stderr,保证
stdout 只有一份纯 JSON(AI 消费路径)。

子命令(AI-NATIVE:每条命令的 JSON 输出即 agent 的行动依据):

- ``run``       跑一次品类流水线或常驻调度(v0.1)。
- ``cron``      定时任务族(10-04-hermes-cron,蓝本 Hermes cron):job 载荷 =
                品类 YAML 管线,``list/create/edit/pause/resume/run/remove/
                status/runs`` 管理 + ``serve`` 常驻宿主(监督守护线程)+
                ``tick`` 手动单次扫描;数据根 = ``--db`` 父目录下的 ``cron/``
                (jobs.json + executions.db,不进 myssia.db)。退出码只用 0/1
                (job 的运行成败归 tick/serve 侧,不撞 2/3 的采集语义)。
- ``init``      输出生成品类 YAML 所需的**结构化信息清单**(JSON,非人机
                问答):agent 据此向用户收集信息并生成 12 节 YAML。
- ``test``      单源试抓:打印提取字段、变更指纹与去重键预览;不推送、
                不入库(存储走 ``:memory:``,退出码沿用 0/2/3 子集语义)。
- ``list``      插件清单 + 各源健康度(状态机 ok/degraded/dead/unknown、
                引擎提示、指纹跳过率;判据看源级条目数与 skip 原因,不看
                run 级成败 —— run success 不得掩盖单源静默 0 条)。
- ``doctor``    结构化诊断:源状态机、engine_hints、凭据配置检查(env:
                存在性 + keychain 引用存在性)、代理连通性(--config 提供
                pools 声明时)、调度下次触发时间、enrich 预算/缓存;
                ``--json`` 输出,agent 据 findings 自修。诊断完成即退出
                0,发现的问题全部落在 ``findings``(healthy=false)。
- ``secret``    钥匙链凭据 set/list/delete(薄包装 myssia.secrets;值永不
                回显、不落日志)。
- ``gates``     门槛件知情启用 show/set(D4/D7,10-05-plugin-market-batch
                批二):付费 SaaS/第三方留痕/自有实例/停更分析的激活开关,
                落全局 gates.yaml(fail-closed:缺失/损坏 = 全关);saas/
                platforms 逐件 on 需钥匙串键在位,缺键结构化拒(退出码 1);
                BYO-agent 无桌面时的配置通道。
- ``plugin``    市场插件装卸:list/install/remove(v0.3,薄包装
                myssia.plugins;装卸 fail-fast 结构化拒绝,扫描零异常 ——
                任何插件装不上/配置坏都不拦核心流水线,铁律)。
- ``channels``  通道目录 refresh/list(v1.2,10-03-messaging-feishu:
                定向推送的寻址地图;refresh 调平台列表 API,失败平台保留
                旧桶并结构化上报,绝不阻塞推送)。
- ``feedback``  反馈闭环 list/stats/mark(v0.3,薄包装 myssia.feedback;
                mark 是桌面形态的手动标记接收路,TG/飞书回调经 pipeline/
                回调端点入库,负反馈随维护阶段自动调参)。
- ``alerts``    告警规则命中历史只读 ``list``(v1;alert_fired 新→旧,
                --rule 过滤 / --limit 钳制 [1,200] / --json;桌面 sidecar
                独占写路径,规则建删启停走 alerts.* 四方法,CLI 写留 v2)。
- ``skill``     Agent Skill 安装通路 install/path(纯文件操作,退出码
                0/1;目标已存在默认结构化拒绝,--force 才覆盖;--link 符号
                链接;--path 自定义目录;真实安装目录按平台惯例探测)。
- ``osint``     一次性 OSINT 侦察(v1.1 源码型插件样板 myssia-osint:动态
                加载插件目录 adapter.py,子进程调用上游 Photon——uv 临时
                环境隔离依赖;输出结构化 JSON;vendor 缺失/适配器不可用 →
                结构化错误,绝不拦核心流水线,铁律)。
- ``proxy``     轻量代理抓取+测活(v1.1 desktop 分级 myssia-proxy:动态加载
                插件目录 adapter.py,进程内完成公开免费代理列表抓取与逐个
                测活,零 Redis 零 docker;全源失败/零可用 → 结构化错误,
                绝不拦核心流水线,铁律)。
- ``add-source`` / ``dashboard`` 为后续版本留位(结构化 not_implemented)。

源健康度判据(PRD 10-01-v02-cli-full,list/doctor 共用):

- ``ok``      本轮有产出,或 skip 原因=指纹未变(0 条合理);
- ``degraded`` 指纹未跳过却产出 0 条;或条目数 < 近 5 次基线的 50%
              (样本不足 5 次时只看 0 条判据);最新一轮失败但未满死线;
- ``dead``    连续 3 轮采集失败;
- ``unknown`` store 无该源的任何运行记录。

数据源:``runs.stats.sources``(pipeline 每轮写入的源级条目数与 skip
原因),store 已持久化,无需迁移。

Raises:
    SystemExit: ``--help`` / ``--version``(exit 0,argparse 惯例)。
"""

from __future__ import annotations

import argparse
import asyncio
import getpass
import json
import logging
import os
import shutil
import sys
import threading
import time
import types
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import replace as dataclass_replace
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from urllib.parse import urlsplit

import httpx

import myssia
from myssia.cron.jobs import AmbiguousJobReference, CronJobs
from myssia.cron.runner import CronRunner
from myssia.cron.tick import tick as cron_tick_scan
from myssia.cron.ticker import (
    DEFAULT_TICK_INTERVAL_SECONDS,
    SupervisedTickerThread,
    run_ticker_loop,
)
from myssia.dedup import DedupRegistry
from myssia.engines.fetch_base import (
    FetchContext,
    check_proxy_connectivity,
    classify_exception,
    load_proxy_pools_file,
    mask_proxy_url,
)
from myssia.engines.registry import fetch_source
from myssia.feedback import (
    DEFAULT_WINDOW_DAYS as DEFAULT_TUNING_WINDOW_DAYS,
)
from myssia.feedback import (
    FeedbackTuner,
    TuningPolicy,
    load_active_tuning,
    record_feedback,
    resolve_item_ref,
)
from myssia.analysis_lane import ANALYSIS_LANE_MEMBERS
from myssia.gates import (
    GATES_KINDS,
    GatesConfig,
    PlatformGate,
    SaaSGate,
    canonical_saas_key_ref,
    default_gates_path,
    gate_open,
    load_gates_config,
    load_gates_fail_closed,
    plugin_gate_key,
    plugin_gate_open,
    replace_analysis_switch,
    replace_platform_gate,
    replace_saas_gate,
    save_gates_config,
    valid_gate_key,
)
from myssia.pipeline import Pipeline, build_cron_trigger
from myssia.push import PLATFORMS
from myssia.push.directory import ChannelDirectory, DirectoryDiscoverUnsupported
from myssia.plugins import (
    InstalledPluginStore,
    PluginFinding,
    PluginStoreError,
    check_category_plugin,
    check_remote_modes,
    default_install_root,
)
from myssia.schema import (  # _SECRET_REF_RE 复用:与 schema 同一引用语法,避免两处漂移
    _SECRET_REF_RE,
    CategoryConfig,
    CredentialResolveError,
    LoadError,
    SchemaValueError,
    load_category_file,
    parse_secret_value,
    resolve_credential,
)
from myssia.secrets import (
    SECRET_SERVICE,
    KeychainBackend,
    SecretError,
    delete_secret,
    get_backend,
    list_secrets,
    set_secret,
    validate_secret_name,
)
from myssia.store import (
    FEEDBACK_CHANNEL_CLI,
    AlertFired,
    FeedbackRecord,
    SQLiteStore,
    StoreSchemaError,
)

__all__ = ["build_parser", "main"]

logger = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_CONFIG_ERROR = 1
EXIT_FETCH_ALL_FAILED = 2
EXIT_PARTIAL = 3

_EXIT_BY_STATUS = {
    "success": EXIT_OK,
    "failed": EXIT_FETCH_ALL_FAILED,
    "partial": EXIT_PARTIAL,
}

DEFAULT_PLUGINS_DIR = "plugins"
DEFAULT_DB_PATH = "myssia.db"
#: osint 样板插件与默认目标(PRD 10-02-v11-plugins-source-arch:合法演示域)。
OSINT_PLUGIN_ID = "myssia-osint"
DEFAULT_OSINT_TARGET = "https://example.com"
#: osint 子进程 wall-clock 预算缺省(整个侦察过程,非单请求超时)。
DEFAULT_OSINT_TIMEOUT_SECONDS = 600.0
#: 采集类失败码 → 退出码 2(其余 osint 失败码归配置/环境错误,退 1)。
#: 退出码契约归 CLI 所有(spec python/error-handling),不依赖插件侧导出。
OSINT_FETCH_FAILURE_CODES = frozenset(
    {
        "photon_failed",
        "photon_timeout",
        "photon_export_missing",
        "photon_export_invalid",
    }
)
#: 代理池插件(myssia-proxy,进程内轻量 fetcher/测活;v1.1 desktop 分级)。
PROXY_PLUGIN_ID = "myssia-proxy"
#: 代理测活期望拿到的可用代理缺省数。
DEFAULT_PROXY_COUNT = 5
#: 单代理测活超时缺省秒数。
DEFAULT_PROXY_CHECK_TIMEOUT_SECONDS = 10.0
#: 采集类失败码 → 退出码 2(全部源抓取失败 / 零可用代理);其余退 1。
PROXY_FETCH_FAILURE_CODES = frozenset({"fetch_failed", "no_alive_proxy"})
#: 视频情报插件(myssia-media,yt-dlp 扁平快扫;10-05-plugin-market-batch 首批)。
#: 上游公域(Unlicense)经 uv 临时环境子进程调用,不 vendor;版本不钉
#: (yt-dlp 抽取器时效即生命;测试全 mock,裁定 R-1)。
MEDIA_PLUGIN_ID = "myssia-media"
#: 扁平快扫缺省条目上限(频道可达数千条,输出必须有界)。
DEFAULT_MEDIA_MAX_ITEMS = 50
#: media 子进程 wall-clock 预算缺省(整个快扫过程,非单请求超时)。
DEFAULT_MEDIA_TIMEOUT_SECONDS = 180.0
#: 采集类失败码 → 退出码 2(上游非零退出/超时/输出损坏);其余退 1。
MEDIA_FETCH_FAILURE_CODES = frozenset(
    {"media_failed", "media_timeout", "media_output_invalid"}
)
#: 用户名侦察插件(myssia-maigret,MIT 上游经 uv 临时环境子进程调用,不 vendor;
#: 10-05-plugin-market-batch 首批,裁定 R-1 不钉版——站点库随上游自更新)。
MAIGRET_PLUGIN_ID = "myssia-maigret"
#: 缺省扫描范围:站点库 rank 前 N 站(全库数千站要数小时,桌面缺省必须有界)。
DEFAULT_MAIGRET_TOP_SITES = 100
#: maigret 子进程 wall-clock 预算缺省(top-100 站量级实测分钟级)。
DEFAULT_MAIGRET_TIMEOUT_SECONDS = 600.0
#: 逐站请求超时缺省秒数(上游 --timeout 语义)。
DEFAULT_MAIGRET_SITE_TIMEOUT_SECONDS = 15.0
#: 采集类失败码 → 退出码 2;零命中=合法空态不是错误;其余退 1。
MAIGRET_FETCH_FAILURE_CODES = frozenset(
    {
        "maigret_failed",
        "maigret_timeout",
        "maigret_report_missing",
        "maigret_report_invalid",
    }
)
#: 域名侦察插件(myssia-theharvester,GPL-2.0 上游 submodule 钉 4.9.2;10-05
#: plugin-market-batch 首批)。依赖与 vendor pyproject 钉版清单同源,经 uv
#: 临时环境注入,绝不进根依赖;master 49a38f8d 含 Python2 语法残留不可运行
#: (2026-10-05 实测),故钉 release tag。
HARVESTER_PLUGIN_ID = "myssia-theharvester"
#: harvester 子进程 wall-clock 预算缺省(整个侦察过程)。
DEFAULT_HARVESTER_TIMEOUT_SECONDS = 600.0
#: 采集类失败码 → 退出码 2;零命中=合法空态不是错误;其余退 1。
HARVESTER_FETCH_FAILURE_CODES = frozenset(
    {
        "harvester_failed",
        "harvester_timeout",
        "harvester_report_missing",
        "harvester_report_invalid",
    }
)
#: 凭证猎手插件(myssia-credhunter,进程内三 lane:credhunt/credcheck/exposure;
#: 10-03-aipocket-fusion;正式取数走 engine: credhunter 进管线,CLI 面是
#: 调试/冒烟口,credcheck 双入口=--apikey 显式传键 / --from-keystore 读
#: 插件侧密钥库回填状态,均不走引擎)。
CREDHUNTER_PLUGIN_ID = "myssia-credhunter"
#: credhunt 配置类失败码 → 1(GitHub 无 token 该源不启用,规格语义);
#: 采集类失败由 payload 状态面(errors/items)判定,不走失败码映射。
CREDHUNT_CONFIG_FAILURE_CODES = frozenset({"tokens_missing"})
#: credcheck/exposure 配置类失败码 → 1;采集类判定同 credhunt(状态面)。
CREDCHECK_CONFIG_FAILURE_CODES = frozenset({"invalid_record"})
EXPOSURE_CONFIG_FAILURE_CODES = frozenset({"exposure_failed"})
#: 单源试抓的每源超时(与 pipeline fetch 阶段默认一致)。
DEFAULT_TEST_TIMEOUT_SECONDS = 120.0
#: doctor/list 回看的最大 run 数(足够「连续 3 次失败 + 近 5 次基线」判据)。
HEALTH_HISTORY_RUNS = 10
#: 基线判据的样本窗口(PRD:近 5 次基线,样本不足 5 次时只看 0 条判据)。
HEALTH_BASELINE_SAMPLES = 5
#: 基线判据的降幅阈值(PRD:条目数 < 基线的 50%)。
HEALTH_BASELINE_DROP_RATIO = 0.5

#: 变更指纹「未变」的 skip 原因词表(engines/fetch_base ChangeVerdict.reason
#: 的未变子集 + 304 协商短路)。命中即「0 条合理」。
FINGERPRINT_UNCHANGED_REASONS = frozenset(
    {"not_modified", "validators_match", "hash_match"}
)

#: 引擎**显式空态**的 skip 原因词表(10-03-aipocket-fusion):credhunter
#: 链外源引擎的凭据未配置(exposure lane)与本地扫描无输入。0 条合理,
#: 但理由与变更指纹不同——doctor 文案须如实区分,不得混报「指纹未变」。
EXPLICIT_EMPTY_SKIP_REASONS = frozenset({"credential_missing", "documents_empty"})

SOURCE_HEALTH_OK = "ok"
SOURCE_HEALTH_DEGRADED = "degraded"
SOURCE_HEALTH_DEAD = "dead"
SOURCE_HEALTH_UNKNOWN = "unknown"

#: 试抓结果预览的条目上限与字段值截断(提取字段预览是给 agent 看的样本)。
TEST_PREVIEW_ITEMS = 5
TEST_PREVIEW_VALUE_CHARS = 200

#: 子命令留位表(实现排期在后续版本)。
STUB_COMMANDS: dict[str, str] = {
    "add-source": "向既有插件 YAML 追加源",
    "dashboard": "品类与源健康度终端面板",
}

#: Agent Skill 安装目标(PRD 10-02-v11:至少 claude/cursor/zcode 三类;
#: agents 兜底 Codex 等通用 ~/.agents/skills 惯例)。值是技能根目录
#: (home 下),实际安装位置 = <技能根>/myia/SKILL.md。
SKILL_AGENT_DIRS: dict[str, str] = {
    "claude": "~/.claude/skills",
    "cursor": "~/.cursor/skills",
    "zcode": "~/.zcode/skills",
    "agents": "~/.agents/skills",
}
#: 技能目录名(平台惯例:技能 = 技能根下与技能同名的目录 + SKILL.md)。
SKILL_DIR_NAME = "myia"
#: SKILL.md 源位置的显式覆盖(装进 wheel 后仓库布局探测失效时的逃生口)。
SKILL_SOURCE_ENV = "MYIA_SKILL_SOURCE"


class _UsageError(Exception):
    """argparse usage error (mapped to exit code 1, structured output)."""


class _Parser(argparse.ArgumentParser):
    """ArgumentParser whose errors raise instead of ``sys.exit(2)``.

    argparse 的用法错误默认退出码 2 会与「采集全部失败」撞码;改为抛
    :class:`_UsageError`,由 :func:`main` 归入退出码 1。
    """

    def error(self, message: str) -> None:
        raise _UsageError(message)


def build_parser() -> argparse.ArgumentParser:
    """Build the ``myssia`` argument parser (help 文本也是 AI 的输入)."""
    parser = _Parser(
        prog="myssia",
        description="世事 — AI-native intelligence hub. 一个品类一份 YAML,fetch→classify→dedup→analyze→push。",
        epilog=(
            "退出码:0 成功 / 1 配置或用法错误 / 2 采集全部失败 / 3 部分失败。\n"
            "示例:myssia run plugins/stocks.yaml --dry-run --json | jq .status\n"
            "      myssia doctor --json | jq '.findings'"
        ),
    )
    parser.add_argument(
        "--version", action="version", version=f"myssia {myssia.__version__}"
    )
    sub = parser.add_subparsers(dest="command", title="子命令")
    _add_run_parser(sub)
    _add_cron_parser(sub)
    _add_init_parser(sub)
    _add_test_parser(sub)
    _add_list_parser(sub)
    _add_doctor_parser(sub)
    _add_secret_parser(sub)
    _add_gates_parser(sub)
    _add_plugin_parser(sub)
    _add_channels_parser(sub)
    _add_feedback_parser(sub)
    _add_alerts_parser(sub)
    _add_skill_parser(sub)
    _add_osint_parser(sub)
    _add_proxy_parser(sub)
    _add_media_parser(sub)
    _add_maigret_parser(sub)
    _add_harvester_parser(sub)
    _add_credhunt_parser(sub)
    _add_credcheck_parser(sub)
    _add_exposure_parser(sub)
    for name, blurb in STUB_COMMANDS.items():
        sub.add_parser(name, help=f"{blurb}(后续版本实现)")
    return parser


def _add_run_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia run``:品类流水线单次/常驻(v0.1 契约)。"""
    run = sub.add_parser(
        "run",
        help="跑一次品类流水线(--once 默认)或常驻调度(--loop)",
        description="加载插件 YAML → 按品类跑 fetch→classify→dedup→analyze→push。",
    )
    run.add_argument("yaml", help="品类 YAML 文件路径(12 节 schema)")
    mode = run.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="跑一次后退出(默认)")
    mode.add_argument(
        "--loop",
        action="store_true",
        help="常驻:按 schedule+timezone cron 到点自动触发",
    )
    run.add_argument(
        "--dry-run",
        action="store_true",
        help="全链执行但不推送,不产生任何持久化副作用;输出将要推的条目 + route 判定 + skip 原因",
    )
    run.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout;stdout 推送通道的卡片行此时改写 stderr)",
    )
    run.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"SQLite 存储路径(默认 ./{DEFAULT_DB_PATH})",
    )
    run.add_argument(
        "--config",
        default=None,
        help="全局配置 YAML(pools 代理声明);源用 pool: 代理时必带(与 test/doctor 同一加载器)",
    )


def _add_cron_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia cron``:定时任务族(10-04-hermes-cron design §4.1 十一子命令)。

    蓝本 = Hermes ``hermes_cli/subcommands/cron.py`` 参数面,D2 裁 prompt/
    skills/monitor/model 族——MYIA 的 job 载荷是品类 YAML 管线,create 必填
    ``--category``(Q6 完整 load_category_file 校验早失败)。schedule 五形态:
    ``30m``/``every 2h``(interval)、``every monday 9am``/``weekdays at 9am``/
    ``0 9 * * *``(5 段 cron,POSIX dow)、``in 30m``/ISO 时刻(once)。
    """
    cron = sub.add_parser(
        "cron",
        help="定时任务:品类管线定时跑一遍 + 摘要投递(list/create/…/runs + serve/tick)",
        description=(
            "定时任务底座:job 注册表落 <数据根>/cron/jobs.json(数据根 = --db 父"
            "目录),执行账本落同目录 executions.db,不进 myssia.db。job 载荷 = 品类"
            " YAML(创建时完整装载校验,存绝对路径);到点跑一遍管线并把运行摘要"
            "按 deliver 目标投递(local 或 feishu:群名 等平台 spec)。常驻宿主走"
            " serve(监督守护线程)或桌面 sidecar,二者并存靠 tick 文件锁 + fire"
            " claim 互斥;pause --all 是全局急停(tick 全停,不动在途 run)。"
        ),
    )
    cron_sub = cron.add_subparsers(
        dest="cron_command", required=True, title="定时任务操作"
    )

    cron_list = cron_sub.add_parser(
        "list", help="列出定时 job(默认只看启用;--all 含暂停/终态)"
    )
    cron_list.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_list.add_argument(
        "--all", action="store_true", help="含 paused/disabled/completed job"
    )
    cron_list.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_create = cron_sub.add_parser(
        "create",
        aliases=["add"],
        help="建定时 job:schedule + 品类 YAML(装载校验早失败)",
    )
    cron_create.add_argument(
        "schedule",
        help="schedule:'30m'/'every 2h'、'every monday 9am'/'weekdays at 9am'/'0 9 * * *'"
        "(5 段,POSIX 周几)、'in 30m'/ISO 时刻(once)",
    )
    cron_create.add_argument(
        "--category",
        required=True,
        help="品类 YAML 路径(必填;完整装载校验,早失败 exit 1;存绝对路径)",
    )
    cron_create.add_argument("--name", help="人类可读 job 名(缺省取品类文件名)")
    cron_create.add_argument(
        "--deliver",
        help="运行摘要投递:'local'(缺省,落 cron/output)或平台 spec 如 'feishu:群名'",
    )
    cron_create.add_argument(
        "--failure-deliver",
        dest="failure_deliver",
        help="失败告警目标(同 --deliver 语法;'none' 关闭;缺省回落 --deliver)",
    )
    cron_create.add_argument(
        "--repeat", type=int, help="重复次数(缺省 forever;once 型自动 1)"
    )
    cron_create.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_create.add_argument(
        "--config",
        default=None,
        help="全局配置 YAML(pools 代理声明;存绝对路径,fire 时作 run --config 透传)",
    )
    cron_create.add_argument(
        "--timezone",
        default=None,
        help="IANA 时区(缺省取品类 YAML timezone,再缺省本地)",
    )
    cron_create.add_argument(
        "--run-timeout",
        dest="run_timeout",
        type=float,
        default=None,
        help="单次运行墙钟超时秒(缺省 3600;超时 kill 整个进程组)",
    )
    cron_create.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="fire 时管线 --dry-run(不推送不入库)",
    )
    cron_create.add_argument(
        "--paused", action="store_true", help="生而暂停(待 resume 放行)"
    )
    cron_create.add_argument(
        "--paused-reason",
        dest="paused_reason",
        default=None,
        help="暂停原因(审计;须搭配 --paused)",
    )
    cron_create.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_edit = cron_sub.add_parser(
        "edit", help="编辑 job(部分更新;schedule 变更重算 next_run_at)"
    )
    cron_edit.add_argument("job_id", help="job ID 或名字")
    cron_edit.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_edit.add_argument("--schedule", help="新 schedule(变更即重算 next_run_at)")
    cron_edit.add_argument("--name", help="新名字")
    cron_edit.add_argument(
        "--category", help="新品类 YAML 路径(装载校验早失败,存绝对路径)"
    )
    cron_edit.add_argument("--deliver", help="新投递目标")
    cron_edit.add_argument(
        "--failure-deliver", dest="failure_deliver", help="新失败告警目标('none' 关闭)"
    )
    cron_edit.add_argument("--repeat", type=int, help="新重复次数")
    cron_edit.add_argument("--timezone", help="新 IANA 时区")
    cron_edit.add_argument("--config", help="新 pools 配置路径(存绝对路径)")
    cron_edit.add_argument(
        "--run-timeout", dest="run_timeout", type=float, help="新墙钟超时秒"
    )
    cron_edit.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_pause = cron_sub.add_parser(
        "pause", help="暂停 job;--all 踩全局急停(tick 全停,不动在途 run)"
    )
    cron_pause.add_argument("job_id", nargs="?", help="job ID 或名字(--all 时省略)")
    cron_pause.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_pause.add_argument(
        "--all", action="store_true", help="全局急停:写 estop 标记,所有 tick 跳过派发"
    )
    cron_pause.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_resume = cron_sub.add_parser(
        "resume", help="恢复暂停的 job(--at 重挂一次性时刻);--all 解除全局急停"
    )
    cron_resume.add_argument("job_id", nargs="?", help="job ID 或名字(--all 时省略)")
    cron_resume.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_resume.add_argument(
        "--at",
        dest="run_at",
        default=None,
        help="ISO-8601 时刻:把完成/暂停的一次性 job 重挂为新 occurrence(recurring 拒收)",
    )
    cron_resume.add_argument(
        "--all", action="store_true", help="解除全局急停(删 estop 标记)"
    )
    cron_resume.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_run = cron_sub.add_parser("run", help="触发 job:下次 tick 立即跑(manual)")
    cron_run.add_argument("job_id", help="job ID 或名字")
    cron_run.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_run.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_remove = cron_sub.add_parser(
        "remove",
        aliases=["rm", "delete"],
        help="删除 job(记录删;output 目录与账本行保留)",
    )
    cron_remove.add_argument("job_id", help="job ID 或名字")
    cron_remove.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_remove.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_status = cron_sub.add_parser(
        "status", help="调度器活性:心跳龄/最后错误/下次到期/急停态"
    )
    cron_status.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_status.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_runs = cron_sub.add_parser(
        "runs", aliases=["history"], help="执行账本尾查(executions.db,新→旧)"
    )
    cron_runs.add_argument("job_id", nargs="?", help="可选 job ID 或名字过滤")
    cron_runs.add_argument("--limit", type=int, default=20, help="行数(1-500,默认 20)")
    cron_runs.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_runs.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )

    cron_serve = cron_sub.add_parser(
        "serve", help="常驻宿主:监督守护线程每 --interval 秒 tick(Ctrl-C 干净停)"
    )
    cron_serve.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    cron_serve.add_argument(
        "--interval",
        type=float,
        default=DEFAULT_TICK_INTERVAL_SECONDS,
        help=f"tick 间隔秒(默认 {DEFAULT_TICK_INTERVAL_SECONDS:g})",
    )

    cron_tick_cmd = cron_sub.add_parser(
        "tick", help="手动单次扫描(调试/外接 cron;锁被他宿主持有静默 0)"
    )
    cron_tick_cmd.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(定数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )


def _add_init_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia init``:生成品类 YAML 的结构化信息清单。"""
    init = sub.add_parser(
        "init",
        help="输出生成品类 YAML 所需的结构化信息清单(JSON,供 agent 消费)",
        description=(
            "非人机问答:stdout 恒为单份 JSON(含必填/可选项、缺省值与硬规则),"
            "agent 收集信息后生成 12 节 YAML,再用 myssia test 验证。"
        ),
    )
    init.add_argument(
        "--json", dest="as_json", action="store_true", help=argparse.SUPPRESS
    )


def _add_test_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia test``:单源试抓(不推送不入库)。"""
    test = sub.add_parser(
        "test",
        help="单源试抓:打印提取字段与指纹结果,不推送不入库",
        description="对插件的一个或全部源走真实降级链试抓;存储走 :memory:,零持久化副作用。",
    )
    test.add_argument("yaml", help="品类 YAML 文件路径")
    test.add_argument("--source", default=None, help="只试抓指定名称的源(缺省全部源)")
    test.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TEST_TIMEOUT_SECONDS,
        help=f"每源试抓超时秒数(默认 {DEFAULT_TEST_TIMEOUT_SECONDS:.0f})",
    )
    test.add_argument(
        "--config",
        default=None,
        help="全局配置 YAML(pools 代理声明);源用 pool: 代理时必带",
    )
    test.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_list_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia list``:插件清单 + 源健康度。"""
    listing = sub.add_parser(
        "list",
        help="插件清单 + 各源健康度(ok/degraded/dead/unknown)",
        description="健康度判据看源级条目数与 skip 原因,不看 run 级成败(静默 0 条不得被 success 掩盖)。",
    )
    listing.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR})",
    )
    listing.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"SQLite 存储路径(默认 ./{DEFAULT_DB_PATH})",
    )
    listing.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_doctor_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia doctor``:结构化诊断。"""
    doctor = sub.add_parser(
        "doctor",
        help="结构化诊断:源状态机/凭据/代理/调度/门槛件,--json 供 agent 自修",
        description=(
            "诊断完成即退出 0;发现的问题全部落在 findings(healthy=false)。"
            "覆盖:插件加载(含明文凭据拒载)、源健康度、engine_hints、凭据引用"
            "(env: 存在性 + keychain: 引用存在性)、代理连通性(--config)、下次触发时间、enrich 预算/缓存;"
            "市场面门槛件(未启用 = info 级 finding,用户没开是正常态不是故障;坏 gates.yaml = warning)。"
        ),
    )
    doctor.add_argument(
        "yaml", nargs="*", help="要体检的品类 YAML;缺省扫描 --plugins-dir 下全部插件"
    )
    doctor.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR})",
    )
    doctor.add_argument(
        "--dir",
        default=str(default_install_root()),
        help="市场插件安装根(门槛件分组扫描;默认 ~/.myia/plugins)",
    )
    doctor.add_argument(
        "--gates-file",
        default=None,
        help="gates.yaml 路径(缺省 MYIA_HOME env > ~/.myia/gates.yaml)",
    )
    doctor.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"SQLite 存储路径(默认 ./{DEFAULT_DB_PATH})",
    )
    doctor.add_argument(
        "--config",
        default=None,
        help="全局配置 YAML(pools 代理声明);提供则逐池做连通性探测",
    )
    doctor.add_argument(
        "--probe-timeout", type=float, default=10.0, help="代理探测超时秒数(默认 10)"
    )
    doctor.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_secret_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia secret``:钥匙链凭据 set/list/delete。"""
    secret = sub.add_parser(
        "secret",
        help="钥匙链凭据管理:set / list / delete(值永不回显)",
        description="薄包装 myssia.secrets;凭据名必须为 myia/<scope>/<name> 规范形式。",
    )
    secret_sub = secret.add_subparsers(
        dest="secret_command", required=True, title="凭据操作"
    )
    secret_set = secret_sub.add_parser("set", help="写入/覆盖一个凭据(值不落日志)")
    secret_set.add_argument("name", help="规范凭据名 myia/<scope>/<name>")
    secret_set.add_argument(
        "--value",
        default=None,
        help=(
            "凭据值;缺省时非 tty 从 stdin 读取、tty 下安全输入(不回显)。"
            "注意:经命令行参数传值会落入 shell history 与进程列表(ps),"
            "自动化请改用 stdin 管道(如 myssia secret set … < value.txt)"
        ),
    )
    secret_set.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出"
    )
    secret_list = secret_sub.add_parser("list", help="列出凭据名(只有名字,没有值)")
    secret_list.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出"
    )
    secret_delete = secret_sub.add_parser("delete", help="删除一个凭据")
    secret_delete.add_argument("name", help="规范凭据名 myia/<scope>/<name>")
    secret_delete.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出"
    )


def _add_gates_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia gates``:门槛件知情启用 show / set(D7,照 secret 命令族形状)。"""
    gates = sub.add_parser(
        "gates",
        help="门槛件知情启用:show / set(付费/留痕/自有实例/停更,fail-closed)",
        description=(
            "e 路门槛化的配置面(D4):付费 SaaS 引擎、第三方留痕通道、自有实例"
            "接入、停更分析件的激活开关全部落全局 gates.yaml,永不落品类 YAML"
            "(AI 生成配置时不可能无意开启付费通道)。fail-closed:文件缺失/损坏"
            "= 全关 + doctor warning。saas/platforms 逐件 on 需要钥匙串键在位"
            "(缺键结构化拒,先 myssia secret set 写入);platform 类组织性不执法"
            "(D6)。退出码只用 0/1(与 secret 族对齐)。"
        ),
    )
    gates_sub = gates.add_subparsers(
        dest="gates_command", required=True, title="门槛件操作"
    )
    show = gates_sub.add_parser("show", help="查看门槛配置(整份配置 + 路径)")
    show.add_argument(
        "--file",
        default=None,
        help="gates.yaml 路径(缺省 MYIA_HOME env > ~/.myia/gates.yaml)",
    )
    show.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出(单份 JSON,stdout)"
    )
    setter = gates_sub.add_parser(
        "set",
        help="逐件启停:<kind>.<name> <on|off>(总开关不带 .name)",
    )
    setter.add_argument(
        "target",
        help=(
            "目标开关:paid_engines / third_party_trace(总开关)或 "
            "saas.<name> / platforms.<name> / analysis.<name>(逐件,"
            "如 saas.zenrows / platforms.crawlab)"
        ),
    )
    setter.add_argument("value", choices=("on", "off"), help="开关值(on / off)")
    setter.add_argument(
        "--file",
        default=None,
        help="gates.yaml 路径(缺省 MYIA_HOME env > ~/.myia/gates.yaml)",
    )
    setter.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出(单份 JSON,stdout)"
    )


def _add_plugin_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia plugin``:市场插件装卸 list / install / remove(v0.3)。"""
    plugin = sub.add_parser(
        "plugin",
        help="市场插件装卸:list / install / remove(装卸失败绝不影响核心流水线)",
        description=(
            "插件 = 安装根下的一个目录(目录名 == manifest id,根下 plugin.yaml)。"
            "默认安装根 ~/.myia/plugins(环境变量 MYIA_PLUGIN_DIR 可覆盖)。"
            "装卸 fail-fast(manifest 坏/版本矩阵不兼容/已装未 force 都结构化拒绝,"
            "退出码 1);扫描零异常 —— 任何插件装不上/配置坏只产结构化 findings,"
            "核心流水线照常跑通(铁律)。"
        ),
    )
    plugin_sub = plugin.add_subparsers(
        dest="plugin_command", required=True, title="插件操作"
    )
    listing = plugin_sub.add_parser(
        "list",
        help="列出已安装插件与结构化 findings(--probe 附带 remote 端点探测)",
    )
    listing.add_argument(
        "--dir",
        default=str(default_install_root()),
        help="插件安装根(默认 ~/.myia/plugins)",
    )
    listing.add_argument(
        "--gates-file",
        default=None,
        help=(
            "gates.yaml 路径(门槛件分组/启用徽标派生;缺省 MYIA_HOME env > "
            "~/.myia/gates.yaml;坏文件 = 全关 + 顶层 gates.error)"
        ),
    )
    listing.add_argument(
        "--probe",
        action="store_true",
        help="对声明 remote 模式的插件做端点可达性探测(网络 I/O,显式 opt-in;4xx 算可达)",
    )
    listing.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )
    install = plugin_sub.add_parser(
        "install",
        help="安装一个插件目录(fail-fast:manifest 坏/版本不兼容/已装未 force 都拒)",
    )
    install.add_argument("source", help="插件目录或其 plugin.yaml 路径")
    install.add_argument(
        "--dir",
        default=str(default_install_root()),
        help="插件安装根(默认 ~/.myia/plugins)",
    )
    install.add_argument(
        "--force",
        action="store_true",
        help="已安装时覆盖;版本矩阵不兼容时强制安装(结果里 compatible_current=false 可见)",
    )
    install.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )
    remove = plugin_sub.add_parser("remove", help="按 id 移除已安装插件")
    remove.add_argument("id", help="要移除的插件 id(manifest 的 id)")
    remove.add_argument(
        "--dir",
        default=str(default_install_root()),
        help="插件安装根(默认 ~/.myia/plugins)",
    )
    remove.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_channels_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia channels``:通道目录 refresh / list(10-03-messaging-feishu D5)。"""
    channels = sub.add_parser(
        "channels",
        help="通道目录:refresh 刷新平台可达对象 / list 查看(定向推送的寻址地图)",
        description=(
            "目录 = 各平台可达推送对象(群/私聊/话题)的缓存地图,"
            "落在 <数据根>/channel_directory.json(数据根 = --db 父目录)。"
            "refresh 调平台列表 API 发现(飞书 im/v1/chats、discord 服务器频道、"
            "slack users.conversations、simplex 联系人;单平台失败保留旧桶);"
            "list 纯读不发现。私聊与无发现平台经"
            ' <数据根>/channel_aliases.json 手工登记:{"feishu": {"oc_xxx": "别名"}}。'
        ),
    )
    channels_sub = channels.add_subparsers(
        dest="channels_command", required=True, title="目录操作"
    )
    refresh = channels_sub.add_parser(
        "refresh",
        help="刷新平台通道目录(缺省全部已注册平台;失败平台保留旧桶并结构化上报)",
    )
    refresh.add_argument(
        "platforms",
        nargs="*",
        help="要刷新的平台名(缺省全部已注册平台;有自动发现的:feishu/discord/slack/simplex)",
    )
    refresh.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(目录 JSON 落数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    refresh.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )
    listing = channels_sub.add_parser(
        "list", help="列出通道目录(纯读;空目录提示先 refresh)"
    )
    listing.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"存储路径(目录 JSON 落数据根 = db 父目录;默认 ./{DEFAULT_DB_PATH})",
    )
    listing.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_feedback_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia feedback``:反馈闭环 list / stats / mark(v0.3,grill Q7)。"""
    feedback = sub.add_parser(
        "feedback",
        help="反馈闭环:list / stats / mark(推送卡片的有价值/没价值回写)",
        description=(
            "mark 手动标记一条反馈入库;list 查看反馈记录;"
            "stats 输出窗口统计(负反馈 Top 类目/词)与当前生效的调参"
            "(mute 词权重/类目降权/评分要点,随调度周期自动应用)。"
        ),
    )
    feedback_sub = feedback.add_subparsers(
        dest="feedback_command", required=True, title="反馈操作"
    )
    mark = feedback_sub.add_parser(
        "mark",
        help="手动标记:myssia feedback mark <条目> <good|bad>(桌面形态第三接收路)",
    )
    mark.add_argument(
        "item", help="条目引用:items.id 或 dedup_key(默认模板下即条目 URL)"
    )
    mark.add_argument(
        "verdict", choices=("good", "bad"), help="判定:good=有价值,bad=没价值"
    )
    mark.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"SQLite 存储路径(默认 ./{DEFAULT_DB_PATH})",
    )
    mark.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出"
    )
    listing = feedback_sub.add_parser("list", help="反馈记录(默认最近 50 条,新→旧)")
    listing.add_argument(
        "--verdict", choices=("good", "bad"), default=None, help="按判定过滤"
    )
    listing.add_argument(
        "--channel", default=None, help="按接收渠道过滤(cli/telegram/feishu)"
    )
    listing.add_argument("--limit", type=int, default=50, help="返回条数上限(默认 50)")
    listing.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"SQLite 存储路径(默认 ./{DEFAULT_DB_PATH})",
    )
    listing.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出"
    )
    stats = feedback_sub.add_parser(
        "stats", help="窗口统计:好/坏计数、负反馈 Top 类目/词、当前生效调参与历史"
    )
    stats.add_argument(
        "--window-days",
        type=int,
        default=DEFAULT_TUNING_WINDOW_DAYS,
        help=f"统计窗口天数(默认 {DEFAULT_TUNING_WINDOW_DAYS},与周期调参一致)",
    )
    stats.add_argument("--top", type=int, default=5, help="Top 类目/词条数(默认 5)")
    stats.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"SQLite 存储路径(默认 ./{DEFAULT_DB_PATH})",
    )
    stats.add_argument(
        "--json", dest="as_json", action="store_true", help="机器可读输出"
    )


def _add_alerts_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia alerts``:告警命中历史只读 list(v1;design §8,feedback 先例)."""
    alerts = sub.add_parser(
        "alerts",
        help="告警命中历史只读:list(alert_fired 新→旧;写路径留 v2)",
        description=(
            "桌面 sidecar 独占写路径;CLI 只读命中历史(alert_fired 表,对齐 "
            "feedback list 先例)。规则建/删/启停走消息屏「告警规则」子面板"
            "(alerts.* 四方法),CLI 写路径留 v2。"
        ),
    )
    alerts_sub = alerts.add_subparsers(
        dest="alerts_command", required=True, title="告警操作"
    )
    listing = alerts_sub.add_parser("list", help="告警命中历史(默认最近 100 条,新→旧)")
    listing.add_argument(
        "--rule", type=int, default=None, help="按规则 id 过滤(alert_rules.id)"
    )
    listing.add_argument(
        "--limit", type=int, default=100, help="返回条数上限(默认 100,钳制 [1,200])"
    )
    listing.add_argument(
        "--db",
        default=DEFAULT_DB_PATH,
        help=f"SQLite 存储路径(默认 ./{DEFAULT_DB_PATH})",
    )
    listing.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_skill_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia skill``:Agent Skill 安装通路 install / path(PRD 10-02-v11)。"""
    skill = sub.add_parser(
        "skill",
        help="Agent Skill 安装通路:install / path(把 skill/SKILL.md 装进 agent 的技能目录)",
        description=(
            "打通 Agent Skill 最后一公里:把仓库 skill/SKILL.md 复制(或 --link "
            "符号链接)进 agent 的技能目录。纯文件操作,装卸结果不影响核心流水线;"
            "已存在默认结构化拒绝,--force 才覆盖。"
        ),
    )
    skill_sub = skill.add_subparsers(
        dest="skill_command", required=True, title="技能操作"
    )
    install = skill_sub.add_parser(
        "install",
        help="安装 SKILL.md 到指定 agent 的技能目录(默认探测,--path 自定义)",
        description=(
            "复制(或 --link 符号链接)SKILL.md 到 <技能根>/myia/SKILL.md。"
            "缺省 --agent 时逐个探测已存在的技能根并全部安装;目标文件已存在时"
            "默认结构化拒绝(退出码 1),--force 才覆盖。"
        ),
    )
    install.add_argument(
        "--agent",
        choices=sorted(SKILL_AGENT_DIRS),
        default=None,
        help=f"目标 agent(缺省探测全部:{', '.join(sorted(SKILL_AGENT_DIRS))})",
    )
    install.add_argument(
        "--path",
        dest="target_dir",
        default=None,
        help="自定义安装目录(直接作为技能目录,优先于 --agent 探测;目录名即技能名)",
    )
    install.add_argument(
        "--link",
        action="store_true",
        help="符号链接代替复制(源仓库更新后装好的技能即跟随更新)",
    )
    install.add_argument(
        "--force",
        action="store_true",
        help="目标 SKILL.md 已存在时覆盖(缺省结构化拒绝,退出码 1)",
    )
    install.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )
    path_cmd = skill_sub.add_parser(
        "path",
        help="打印 SKILL.md 源位置与各 agent 的推荐安装路径及安装状态",
        description="信息性命令:完成即退出 0;源缺失也如实落在 found=false,不猜路径。",
    )
    path_cmd.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_osint_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia osint``:一次性 OSINT 侦察(v1.1 源码型插件样板 myssia-osint)."""
    osint = sub.add_parser(
        "osint",
        help="一次性 OSINT 侦察(myssia-osint 插件,子进程调用上游 Photon;失败绝不拦核心)",
        description=(
            "源码型插件样板:定位 <plugins-dir>/myssia-osint(适配器 adapter.py + "
            "vendor/Photon submodule),以 uv 临时环境(--no-project --with 按需装依赖,"
            "不进根依赖)隔离子进程运行上游 CLI,读取其 JSON 导出并输出结构化结果。"
            "默认目标 example.com(合法演示域)。vendor 缺失/适配器不可用/目标非法 "
            "→ 结构化错误退 1;采集失败(非零退出/超时/导出坏)退 2;任何失败都"
            "不影响核心品类流水线(铁律)。"
        ),
    )
    osint.add_argument(
        "target",
        nargs="?",
        default=DEFAULT_OSINT_TARGET,
        help=f"侦察目标 http(s) URL(默认 {DEFAULT_OSINT_TARGET},合法演示域)",
    )
    osint.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_OSINT_TIMEOUT_SECONDS,
        help=f"子进程 wall-clock 预算秒数(默认 {DEFAULT_OSINT_TIMEOUT_SECONDS:.0f})",
    )
    osint.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR},样板位于 myssia-osint/ 子目录)",
    )
    osint.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _configure_logging(as_json: bool) -> None:
    """stderr 上的结构化日志;--json 模式收敛到 WARNING,保 stdout 纯净。"""
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.WARNING if as_json else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        force=True,
    )


def _emit_config_error(
    errors: list[dict[str, Any]], *, source: str | None, as_json: bool
) -> None:
    """结构化配置错误:--json 走 stdout,人类可读走 stderr。"""
    if as_json:
        print(
            json.dumps(
                {"error": "config", "source": source, "errors": errors},
                ensure_ascii=False,
            )
        )
        return
    stream = sys.stderr
    head = "品类配置错误"
    if source:
        head += f"({source})"
    print(head, file=stream)
    for index, detail in enumerate(errors, start=1):
        print(
            f"  {index}. [{detail.get('error_type', 'error')}] {detail.get('path', '$')} — {detail.get('message', '')}",
            file=stream,
        )


def _emit_generic_error(
    error: str, message: str, *, as_json: bool, **extra: Any
) -> None:
    """非 YAML 类错误(用法/secret/存储)的结构化输出,契约同配置错误。"""
    payload = {"error": error, "message": message, **extra}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print(f"{message}", file=sys.stderr)


def _load_error_details(exc: LoadError) -> list[dict[str, Any]]:
    return exc.to_dict()["errors"]


def _value_error_details(exc: Exception) -> list[dict[str, Any]]:
    return [{"path": "$", "error_type": "config_error", "message": str(exc)}]


def _print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False))


# ---------------------------------------------------------------------------
# myssia run(v0.1 契约,保持不变)
# ---------------------------------------------------------------------------


def _print_human(result: Any) -> None:
    """人类可读摘要(与 --json 同一信息,另一种皮)。"""
    print(
        f"世事 run:{result.category}({result.category_name}) run_id={result.run_id}"
        + (" [dry-run]" if result.dry_run else "")
    )
    for stage in result.stages:
        parts = [f"{stage.name}:{stage.status}"]
        if stage.items_in or stage.items_out:
            parts.append(f"{stage.items_in}→{stage.items_out} 条")
        if stage.skips:
            parts.append(
                "跳过 " + ",".join(f"{k}×{v}" for k, v in sorted(stage.skips.items()))
            )
        if stage.failures:
            parts.append(f"失败 {len(stage.failures)} 条")
        if stage.error:
            parts.append(f"错误 {stage.error}")
        print("  - " + " | ".join(parts))
    for source in result.sources:
        state = "跳过" if source.skipped else ("失败" if source.failed else "成功")
        line = f"  源 {source.name}({state},engine={source.engine},条目 {source.item_count}"
        if source.skip_reason:
            line += f",skip={source.skip_reason}"
        line += ")"
        print(line)
    for push in result.pushes:
        line = f"  推送 {push.channel}:immediate={push.immediate} digest={push.digest} archive={push.archive}"
        line += ",发送成功" if push.ok else ",存在发送失败"
        if push.dry_run:
            line += "(dry-run,未实际发送)"
        print(line)
    print(f"状态:{result.status}")


def _selfcheck_category_plugin(config: CategoryConfig) -> None:
    """品类 ``plugin:`` 节的启动自检:只发 WARNING 日志,任何结果都不改变 run 流程.

    铁律(security-baseline):任何 plugin 装不上/配置坏/remote 不可达,核心
    流水线照常跑通 —— 本函数吞掉一切异常,findings 一律 warning 级落日志
    (--json 模式 stderr 可见,stdout 的单份 JSON 不受影响,退出码不变)。
    自检默认零网络(端点探测是 ``myssia plugin list --probe`` 的显式 opt-in)。
    """
    section = config.plugin
    if section is None:
        return
    try:
        backend = _safe_keychain_backend()
        findings = check_category_plugin(
            section, InstalledPluginStore(default_install_root()), backend=backend
        )
    except Exception as exc:  # noqa: BLE001 - 自检绝不拦核心
        logger.warning("插件自检失败(已降级跳过,核心流水线不受影响): %s", exc)
        return
    for finding in findings:
        _log_plugin_finding(finding, prefix="插件自检")


def _safe_keychain_backend() -> KeychainBackend | None:
    """Acquire the keychain backend for存在性核验;不可用返回 None(核验跳过)."""
    try:
        return get_backend()
    except SecretError as exc:
        logger.debug("钥匙链后端不可用(token 存在性核验跳过): %s", exc)
        return None


def _log_plugin_finding(finding: PluginFinding, *, prefix: str) -> None:
    logger.warning(
        "%s [%s] %s %s: %s",
        prefix,
        finding.severity,
        finding.scope,
        finding.code,
        finding.message,
    )


def _cmd_run(args: argparse.Namespace) -> int:
    """``myssia run <yaml>``:加载 → 跑一次或常驻;退出码 0/1/2/3。"""
    _configure_logging(as_json=args.as_json)
    try:
        config = load_category_file(args.yaml)
    except LoadError as exc:
        _emit_config_error(
            _load_error_details(exc), source=exc.source, as_json=args.as_json
        )
        return EXIT_CONFIG_ERROR
    _selfcheck_category_plugin(config)

    pools, pools_exit = _resolve_pools(getattr(args, "config", None), args.as_json)
    if pools is None and pools_exit != EXIT_OK:
        return pools_exit
    try:
        pipeline = Pipeline(
            config,
            db_path=args.db,
            proxy_pools=pools,
            # --json 契约(SKILL.md §0 / cli docstring):stdout 恰好一份 JSON。
            # stdout 推送通道的卡片行改写 stderr,不能与 run 报告同流。
            stdout_stream=sys.stderr if args.as_json else None,
        )
    except ValueError as exc:  # Route/规则/关键词表配置非法(fail fast)
        _emit_config_error(
            _value_error_details(exc), source=str(args.yaml), as_json=args.as_json
        )
        return EXIT_CONFIG_ERROR

    try:
        if args.loop:
            asyncio.run(pipeline.run_forever(dry_run=args.dry_run))
            logger.info("常驻模式已退出")
            return EXIT_OK
        result = asyncio.run(pipeline.run(dry_run=args.dry_run))
    except KeyboardInterrupt:
        logger.info("收到中断信号,已停止")
        return EXIT_OK
    except StoreSchemaError as exc:
        # 惰性开库发生在 run 内(cli.py:386 的 except ValueError 管不到):
        # 库损坏 / schema 版本过新必须结构化上报,不能让裸 traceback 打穿
        # --json 主消费面(agent/CI 拿不到 code/details)。
        _emit_generic_error(
            "store", str(exc), as_json=args.as_json, error_type=exc.code, **exc.details
        )
        return EXIT_CONFIG_ERROR
    finally:
        pipeline.close()

    if args.as_json:
        _print_json(result.to_dict())
    else:
        _print_human(result)
    return _EXIT_BY_STATUS.get(result.status, EXIT_PARTIAL)


# ---------------------------------------------------------------------------
# myssia cron:定时任务族(10-04-hermes-cron design §4.1;蓝本 Hermes
# hermes_cli/subcommands/cron.py 参数面 + hermes_cli/cron.py 展示层,D2 裁
# prompt/skills/monitor 族。退出码只用 0/1;--json 契约 = stdout 恰一份 JSON)
# ---------------------------------------------------------------------------

#: 心跳新鲜判据(上游 ``_ticker_age_is_fresh`` 同款:3 个周期 + 20s 裕量;
#: 与 serve 的 --interval 无关的固定判据,status 端无从得知实际间隔)。
_CRON_TICKER_FRESH_SECONDS = DEFAULT_TICK_INTERVAL_SECONDS * 3 + 20

#: 子命令别名 → 规范名(argparse 的 dest 记用户敲的原串)。
_CRON_COMMAND_ALIASES = {
    "add": "create",
    "rm": "remove",
    "delete": "remove",
    "history": "runs",
}


def _cron_data_root(db_path: str) -> Path:
    """--db → 数据根(db 父目录,与目录/账本同款推导)。"""
    return Path(db_path).parent


def _cron_job_payload(job: dict[str, Any]) -> dict[str, Any]:
    """job 记录的 JSON 载荷(逐字段拷贝,免调用方误改存储态)。"""
    return dict(job)


def _cron_resolve_ref(
    cron: CronJobs, ref: str, *, as_json: bool
) -> tuple[dict[str, Any] | None, int]:
    """id 或名字解析 job;未找到/重名自行结构化上报,返回 ``(job, exit_code)``。"""
    try:
        job = cron.resolve_job_ref(ref)
    except AmbiguousJobReference as exc:
        _emit_generic_error(
            "cron_ambiguous_job",
            str(exc),
            as_json=as_json,
            candidates=[m.get("id") for m in exc.matches],
        )
        return None, EXIT_CONFIG_ERROR
    if job is None:
        _emit_generic_error(
            "cron_job_not_found", f"找不到 cron job:{ref}", as_json=as_json
        )
        return None, EXIT_CONFIG_ERROR
    return job, EXIT_OK


def _cmd_cron_list(args: argparse.Namespace) -> int:
    """``cron list``:name/id/schedule_display/next_run_at/last_status/deliver。"""
    cron = CronJobs.for_db(args.db)
    jobs = cron.list_jobs(include_disabled=args.all)
    if args.as_json:
        _print_json(
            {
                "command": "cron",
                "action": "list",
                "data_root": str(cron.store.data_root),
                "count": len(jobs),
                "jobs": [_cron_job_payload(job) for job in jobs],
            }
        )
        return EXIT_OK
    if not jobs:
        print(f"无定时 job(数据根 {cron.store.data_root};--all 含暂停/终态)")
        print("建第一个:myssia cron create 'every 30m' --category <品类 YAML>")
        return EXIT_OK
    print(f"世事 cron list:共 {len(jobs)} 个 job(数据根 {cron.store.data_root})")
    for job in jobs:
        state = job.get("state") or (
            "scheduled" if job.get("enabled", True) else "paused"
        )
        print(f"  {job.get('name', '(未命名)')} [{state}] id={job.get('id')}")
        print(
            f"    schedule: {job.get('schedule_display') or (job.get('schedule') or {}).get('display')}"
        )
        print(f"    next_run: {job.get('next_run_at') or '-'}")
        print(
            f"    last_status: {job.get('last_status') or '-'}  deliver: {job.get('deliver') or 'local'}"
        )
    return EXIT_OK


def _cmd_cron_create(args: argparse.Namespace) -> int:
    """``cron create``:Q6 完整 load_category_file 早失败;Q5 绝对路径存储;
    时区链 --timezone > 品类 YAML timezone > 本地(锚 schedule 解析并随档存)。"""
    try:
        config = load_category_file(args.category)
    except LoadError as exc:
        _emit_config_error(
            _load_error_details(exc), source=exc.source, as_json=args.as_json
        )
        return EXIT_CONFIG_ERROR
    timezone = args.timezone or config.timezone
    cron = CronJobs.for_db(args.db)
    try:
        job = cron.create_job(
            category=args.category,
            schedule=args.schedule,
            name=args.name,
            repeat=args.repeat,
            deliver=args.deliver,
            failure_deliver=args.failure_deliver,
            timezone=timezone,
            config_path=(
                str(Path(args.config).expanduser().resolve()) if args.config else None
            ),
            run_timeout=args.run_timeout,
            # 仅显式设置才持久化(Hermes 可选键风格;create_job 对 None 不落键)
            dry_run=True if args.dry_run else None,
            paused=args.paused,
            paused_reason=args.paused_reason,
            origin={"source": "cli"},
        )
    except ValueError as exc:  # schedule 五形态/once 超窗/repeat/paused 自相矛盾
        _emit_generic_error("cron_create_failed", str(exc), as_json=args.as_json)
        return EXIT_CONFIG_ERROR
    if args.as_json:
        _print_json(
            {"command": "cron", "action": "create", "job": _cron_job_payload(job)}
        )
        return EXIT_OK
    print(f"已建定时 job:{job['name']}(id={job['id']})")
    print(f"  schedule: {job['schedule_display']}")
    print(f"  下次运行: {job['next_run_at'] or '(paused,待 resume 放行)'}")
    print(f"  品类: {job['category']}")
    return EXIT_OK


def _cmd_cron_edit(args: argparse.Namespace) -> int:
    """``cron edit``:部分更新;schedule 变更由底座重算 next_run_at 并重推导
    repeat 缺省(once↔recurring 翻转)。"""
    cron = CronJobs.for_db(args.db)
    job, exit_code = _cron_resolve_ref(cron, args.job_id, as_json=args.as_json)
    if job is None:
        return exit_code
    if args.category is not None:  # 与 create 同款 Q6 早失败/Q5 绝对路径
        try:
            load_category_file(args.category)
        except LoadError as exc:
            _emit_config_error(
                _load_error_details(exc), source=exc.source, as_json=args.as_json
            )
            return EXIT_CONFIG_ERROR
    updates: dict[str, Any] = {}
    for key in ("schedule", "name", "deliver", "failure_deliver", "timezone"):
        value = getattr(args, key)
        if value is not None:
            updates[key] = value
    if args.category is not None:
        updates["category"] = args.category
    if args.config is not None:
        updates["config_path"] = str(Path(args.config).expanduser().resolve())
    if args.repeat is not None:
        updates["repeat"] = args.repeat
    if args.run_timeout is not None:
        updates["run_timeout"] = args.run_timeout
    if not updates:
        _emit_generic_error(
            "cron_edit_no_changes",
            "未给出任何要更新的字段(--schedule/--name/--category/--deliver/…)",
            as_json=args.as_json,
        )
        return EXIT_CONFIG_ERROR
    try:
        updated = cron.update_job(job["id"], updates)
    except ValueError as exc:  # schedule 解析失败/once 超窗/终态复活拒绝
        _emit_generic_error("cron_edit_failed", str(exc), as_json=args.as_json)
        return EXIT_CONFIG_ERROR
    if args.as_json:
        _print_json(
            {
                "command": "cron",
                "action": "edit",
                "job": _cron_job_payload(updated or {}),
            }
        )
        return EXIT_OK
    print(f"已更新:{updated.get('name', args.job_id)}(id={updated.get('id')})")
    print(f"  schedule: {updated.get('schedule_display')}")
    print(f"  下次运行: {updated.get('next_run_at') or '-'}")
    return EXIT_OK


def _cmd_cron_pause(args: argparse.Namespace) -> int:
    """``cron pause <job>``:暂停;``cron pause --all``:全局急停 estop 标记(Q4)。"""
    as_json = args.as_json
    if args.all and args.job_id:
        _emit_generic_error(
            "usage", "pause --all 是全局急停,不要再带 job id", as_json=as_json
        )
        return EXIT_CONFIG_ERROR
    if not args.all and not args.job_id:
        _emit_generic_error(
            "usage", "pause 需要 job id(或 --all 踩全局急停)", as_json=as_json
        )
        return EXIT_CONFIG_ERROR
    cron = CronJobs.for_db(args.db)
    if args.all:
        marker = cron.engage_estop(reason="paused via `myssia cron pause --all`")
        if as_json:
            _print_json(
                {
                    "command": "cron",
                    "action": "pause",
                    "estopped": True,
                    "marker": str(marker),
                }
            )
        else:
            print(
                f"已踩全局急停:所有 tick 跳过派发(在途 run 不受影响);恢复用 myssia cron resume --all"
            )
        return EXIT_OK
    job, exit_code = _cron_resolve_ref(cron, args.job_id, as_json=as_json)
    if job is None:
        return exit_code
    updated = cron.pause_job(job["id"])
    if as_json:
        _print_json(
            {
                "command": "cron",
                "action": "pause",
                "job": _cron_job_payload(updated or {}),
            }
        )
    else:
        print(f"已暂停:{job.get('name')} (id={job['id']};resume 放行)")
    return EXIT_OK


def _cmd_cron_resume(args: argparse.Namespace) -> int:
    """``cron resume <job> [--at ISO]``:恢复/一次性重挂;``--all`` 解除急停。"""
    as_json = args.as_json
    if args.all and (args.job_id or args.run_at):
        _emit_generic_error(
            "usage", "resume --all 是解除全局急停,不要再带 job id/--at", as_json=as_json
        )
        return EXIT_CONFIG_ERROR
    if not args.all and not args.job_id:
        _emit_generic_error(
            "usage", "resume 需要 job id(或 --all 解除全局急停)", as_json=as_json
        )
        return EXIT_CONFIG_ERROR
    cron = CronJobs.for_db(args.db)
    if args.all:
        cleared = cron.disengage_estop()
        if as_json:
            _print_json(
                {
                    "command": "cron",
                    "action": "resume",
                    "estopped": cron.is_estopped(),
                    "cleared": cleared,
                }
            )
        else:
            print("全局急停已解除" if cleared else "本无全局急停(无需解除)")
        return EXIT_OK
    job, exit_code = _cron_resolve_ref(cron, args.job_id, as_json=as_json)
    if job is None:
        return exit_code
    try:
        updated = (
            cron.rearm_oneshot(job["id"], args.run_at)
            if args.run_at
            else cron.resume_job(job["id"])
        )
    except ValueError as exc:  # recurring 拒 --at / once 已过窗 / 覆盖活认领
        _emit_generic_error("cron_resume_failed", str(exc), as_json=as_json)
        return EXIT_CONFIG_ERROR
    if updated is None:  # pragma: no cover - resolve 已保证存在
        _emit_generic_error(
            "cron_job_not_found", f"找不到 cron job:{args.job_id}", as_json=as_json
        )
        return EXIT_CONFIG_ERROR
    if as_json:
        _print_json(
            {"command": "cron", "action": "resume", "job": _cron_job_payload(updated)}
        )
    else:
        verb = "已重挂" if args.run_at else "已恢复"
        print(f"{verb}:{updated.get('name')} (id={updated.get('id')})")
        print(f"  下次运行: {updated.get('next_run_at') or '-'}")
    return EXIT_OK


def _cmd_cron_run(args: argparse.Namespace) -> int:
    """``cron run <job>``:下次 tick 立即跑(manual;复活 paused、计入 repeat)。"""
    cron = CronJobs.for_db(args.db)
    job, exit_code = _cron_resolve_ref(cron, args.job_id, as_json=args.as_json)
    if job is None:
        return exit_code
    try:
        updated = cron.trigger_job(job["id"])
    except ValueError as exc:  # 终态 job 拒绝
        _emit_generic_error("cron_run_failed", str(exc), as_json=args.as_json)
        return EXIT_CONFIG_ERROR
    if args.as_json:
        _print_json(
            {
                "command": "cron",
                "action": "run",
                "job": _cron_job_payload(updated or {}),
            }
        )
    else:
        print(f"已触发:{job.get('name')} (id={job['id']})——下次 tick 立即跑(手动来源)")
        print(f"  next_run: {updated.get('next_run_at') or '-'}")
    return EXIT_OK


def _cmd_cron_remove(args: argparse.Namespace) -> int:
    """``cron remove <job>``:删记录;output 目录与账本行保留(运行证据)。"""
    cron = CronJobs.for_db(args.db)
    job, exit_code = _cron_resolve_ref(cron, args.job_id, as_json=args.as_json)
    if job is None:
        return exit_code
    if not cron.remove_job(job["id"]):  # pragma: no cover - resolve 已保证存在
        _emit_generic_error(
            "cron_job_not_found", f"找不到 cron job:{args.job_id}", as_json=args.as_json
        )
        return EXIT_CONFIG_ERROR
    if args.as_json:
        _print_json(
            {
                "command": "cron",
                "action": "remove",
                "removed": True,
                "job_id": job["id"],
                "name": job.get("name"),
            }
        )
    else:
        print(f"已删除:{job.get('name')} (id={job['id']};output 目录与执行账本保留)")
    return EXIT_OK


def _cmd_cron_status(args: argparse.Namespace) -> int:
    """``cron status``:ticker 活性(心跳龄/最后错误)+ 下次到期 + 急停态(F1.6)。"""
    cron = CronJobs.for_db(args.db)
    heartbeat_age = cron.get_ticker_heartbeat_age()
    success_age = cron.get_ticker_success_age()
    last_error = cron.get_ticker_last_error()
    writer_alive = cron.ticker_heartbeat_writer_alive()
    estopped = cron.is_estopped()
    jobs = cron.list_jobs(include_disabled=True)
    enabled_jobs = [job for job in jobs if job.get("enabled", True)]
    next_due_at = min(
        (job["next_run_at"] for job in enabled_jobs if job.get("next_run_at")),
        default=None,
    )
    heartbeat_fresh = (
        heartbeat_age is not None and heartbeat_age <= _CRON_TICKER_FRESH_SECONDS
    )
    ticker_alive = heartbeat_fresh and writer_alive
    payload = {
        "command": "cron",
        "action": "status",
        "data_root": str(cron.store.data_root),
        "ticker_alive": ticker_alive,
        "heartbeat_age_seconds": heartbeat_age,
        "last_success_age_seconds": success_age,
        "last_error": last_error,
        "estopped": estopped,
        "jobs_total": len(jobs),
        "jobs_enabled": len(enabled_jobs),
        "next_due_at": next_due_at,
    }
    if args.as_json:
        _print_json(payload)
        return EXIT_OK
    print(f"世事 cron status(数据根 {cron.store.data_root})")
    if estopped:
        print(
            "⚠ 全局急停中(pause --all 所踩):所有 tick 跳过派发;myssia cron resume --all 解除"
        )
    if heartbeat_age is None:
        print("⚠ 调度器从未心跳——serve 未跑过(或刚启动);常驻宿主:myssia cron serve")
    elif not heartbeat_fresh:
        print(
            f"⚠ 心跳停滞 {heartbeat_age:.0f}s(预期每 ~{DEFAULT_TICK_INTERVAL_SECONDS:.0f}s 一次)——job 不会再发"
        )
        print(
            "  启动常驻宿主:myssia cron serve(或桌面 sidecar);tick 单发调试:myssia cron tick"
        )
    elif last_error:
        print(f"⚠ ticker 活着但最近 tick 失败:{last_error}")
    else:
        print(
            f"✓ ticker 活着(心跳 {heartbeat_age:.0f}s 前,上次成功 {success_age if success_age is None else f'{success_age:.0f}s'} 前)"
        )
    print(
        f"job:{len(enabled_jobs)} 启用 / {len(jobs)} 全部;下次到期:{next_due_at or '-'}"
    )
    return EXIT_OK


def _cmd_cron_runs(args: argparse.Namespace) -> int:
    """``cron runs [job] --limit``:执行账本尾查(新→旧;--limit 钳制 1-500)。"""
    cron = CronJobs.for_db(args.db)
    job_id_filter: str | None = None
    if args.job_id:
        job, exit_code = _cron_resolve_ref(cron, args.job_id, as_json=args.as_json)
        if job is None:
            return exit_code
        job_id_filter = job["id"]
    rows = cron.ledger.list_executions(job_id=job_id_filter, limit=args.limit)
    records: list[dict[str, Any]] = []
    for row in rows:
        record = dict(row)
        raw_summary = record.pop("run_summary_json", None)
        try:
            record["run_summary"] = json.loads(raw_summary) if raw_summary else None
        except (TypeError, ValueError):  # 手编/损坏的摘要:如实带原串
            record["run_summary"] = {"raw": raw_summary}
        records.append(record)
    if args.as_json:
        _print_json(
            {
                "command": "cron",
                "action": "runs",
                "count": len(records),
                "executions": records,
            }
        )
        return EXIT_OK
    if not records:
        print(f"无执行记录(数据根 {cron.store.data_root})")
        return EXIT_OK
    print(f"世事 cron runs:共 {len(records)} 条(新→旧)")
    for record in records:
        line = (
            f"  {record.get('id', '?')} [{record.get('status', '?')}]"
            f" job={record.get('job_id', '?')} source={record.get('source', '?')}"
            f" {record.get('claimed_at', '?')}"
        )
        if record.get("run_summary"):
            line += "(含运行摘要)"
        print(line)
        if record.get("error"):
            print(f"    {record['error']}")
    return EXIT_OK


def _cmd_cron_serve(args: argparse.Namespace) -> int:
    """``cron serve``:阻塞常驻宿主(F2.1)。

    SupervisedTickerThread(ticker.py)包裹 run_ticker_loop:线程崩了自动
    respawn(restart 计数入日志);宿主主循环只做周期性 restart_if_dead 与
    Ctrl-C 干净关停。执行体注入 B1 接线(G2 端到端):``CronRunner(cron)
    .execute``(spawn ``myssia run --json`` 子进程,D11;sidecar B3 同位;
    手动 ``cron tick`` 同款注入)。
    """
    cron = CronJobs.for_db(args.db)
    interval = max(1.0, float(args.interval))
    stop_event = threading.Event()
    supervisor = SupervisedTickerThread(
        run_ticker_loop,
        args=(cron, stop_event),
        kwargs={"interval": interval, "execute_job": CronRunner(cron).execute},
        stop_event=stop_event,
        name="cron-ticker",
    )
    supervisor.start()
    logger.info(
        "myssia cron serve:常驻宿主已启动(数据根 %s,interval=%.0fs,Ctrl-C 停)",
        cron.store.data_root,
        interval,
    )
    supervision_poll = min(interval, 30.0)  # ticker 死亡的发现时延上限
    try:
        while True:
            time.sleep(supervision_poll)
            supervisor.restart_if_dead()
    except KeyboardInterrupt:
        logger.info("收到中断信号,正在停止 cron ticker…")
        stop_event.set()
        supervisor.join(timeout=supervision_poll + 5.0)
        logger.info("cron serve 已退出")
    return EXIT_OK


def _cmd_cron_tick(args: argparse.Namespace) -> int:
    """``cron tick``:手动单次扫描(F2.3;锁被他宿主持有 → 静默返回 0)。

    执行体与 serve 同款注入(复查修:``CronRunner(cron).execute``)——F2.3
    定位「外接 cron 用」,到期 fire 必须真跑;走底座 no-op stub 会把派发
    记成假成功(completed/ok + repeat 消耗),外接 cron 口径下无运行却耗
    槽位。离线测试面由 test_cli.py 注入 spawn 替身承担。
    """
    cron = CronJobs.for_db(args.db)
    try:
        fired = cron_tick_scan(
            cron, verbose=True, execute_job=CronRunner(cron).execute
        )
    except OSError as exc:  # 真锁故障(EMFILE/权限)——非锁竞争(竞争在底层静默 0)
        _emit_generic_error("cron_tick_failed", str(exc), as_json=False)
        return EXIT_CONFIG_ERROR
    logger.info("cron tick 完成:派发 %d 个 job", fired)
    return EXIT_OK


def _cmd_cron(args: argparse.Namespace) -> int:
    """``myssia cron <子命令>`` 分发(design §4.1 十一子命令;退出码 0/1)。"""
    _configure_logging(as_json=getattr(args, "as_json", False))
    handlers: dict[str, Any] = {
        "list": _cmd_cron_list,
        "create": _cmd_cron_create,
        "edit": _cmd_cron_edit,
        "pause": _cmd_cron_pause,
        "resume": _cmd_cron_resume,
        "run": _cmd_cron_run,
        "remove": _cmd_cron_remove,
        "status": _cmd_cron_status,
        "runs": _cmd_cron_runs,
        "serve": _cmd_cron_serve,
        "tick": _cmd_cron_tick,
    }
    command = _CRON_COMMAND_ALIASES.get(args.cron_command, args.cron_command)
    handler = handlers.get(command)
    if handler is None:  # pragma: no cover - argparse required=True 兜底
        _emit_generic_error(
            "usage",
            f"未知 cron 子命令:{args.cron_command}",
            as_json=getattr(args, "as_json", False),
        )
        return EXIT_CONFIG_ERROR
    return handler(args)


# ---------------------------------------------------------------------------
# myssia init:生成品类 YAML 的结构化信息清单(AI 消费,非人机问答)
# ---------------------------------------------------------------------------

_INIT_REQUIRED_INPUTS: list[dict[str, Any]] = [
    {
        "id": "identity",
        "section": "id / name",
        "description": "品类 id(小写字母/数字/连字符/下划线,字母或数字开头,1-64 字符)与中文显示名",
        "example": {"id": "gpu-prices", "name": "显卡价格"},
    },
    {
        "id": "schedule",
        "section": "schedule / timezone",
        "description": "5 段 cron 触发频率;timezone 为 IANA 名称,缺省跟随系统时区",
        "example": {"schedule": "0 9,15 * * 1-5", "timezone": "Asia/Shanghai"},
    },
    {
        "id": "sources",
        "section": "sources[]",
        "description": (
            "每个源:name、url(模板翻页含 {page})、engine(auto=L1 API→L2 静态页→L3 crawl4ai→firecrawl "
            "自动降级)、method+post_body(POST 必带 post_body)、headers(凭据位只许 env:/keychain: 引用)、"
            "extract(type: list/item/json_path + fields,至少要能取到 url)、rate_limit(qps/backoff/"
            "respect_robots)、proxy(direct / pool:<名称>)、retry(0-10);"
            "源级扩展参数(如 symbols: [...])按 URL 占位符 {symbol} 逐值展开"
        ),
        "example": {
            "name": "yahoo-chart",
            "engine": "direct_api",
            "url": "https://query1.example.com/v8/chart/{symbol}",
            "extract": {
                "type": "json_path",
                "fields": {"title": "$.meta.longName", "url": "$.meta.symbol"},
            },
            "symbols": ["NVDA", "AAPL"],
        },
    },
]

_INIT_OPTIONAL_INPUTS: list[dict[str, Any]] = [
    {
        "id": "watchlist",
        "section": "watchlist",
        "default": {"keywords": [], "mute": []},
        "description": "关键词加权与静默词(供 v0.2 LLM 精评做相关性基线与降权)",
    },
    {
        "id": "classify",
        "section": "classify",
        "default": {"builtin": True, "rules": []},
        "description": "七大类内置关键词扫描默认开;自定义规则为 name/when/tag(when 为白名单表达式,永不 eval)",
    },
    {
        "id": "dedup",
        "section": "dedup.key",
        "default": "{url}",
        "description": "去重键模板:只允许 URL 或字段组合键;{title} 永久禁止;保留字段 {date}/{slot} 可用",
    },
    {
        "id": "enrich",
        "section": "enrich",
        "default": {
            "enabled": False,
            "model": "glm-4-flash",
            "scores": ["value", "relevance", "credibility"],
            "batch": 20,
            "cache": True,
            "budget_per_run": 50000,
        },
        "description": "LLM 精评(第二层漏斗):启用时 enrich.base_url / enrich.api_key 是 schema 字段,"
        "值必须是 env:/keychain: 引用(无内置端点、无默认 key);漏配在启动期报 "
        "missing_base_url / missing_api_key。构造注入(Pipeline enrich_settings)仅是测试/编程路径",
    },
    {
        "id": "push",
        "section": "push[]",
        "default": [],
        "description": "每通道:channel(feishu_card/telegram/ntfy/dingtalk/wecom/webhook/stdout)、target(env:/keychain: 引用,"
        "stdout 不需要)、route(when→immediate/digest/archive;空 = 七大类缺省映射)、"
        "template(Jinja2,语法在加载期校验)",
    },
    {
        "id": "storage",
        "section": "storage",
        "default": {"retention": "90d", "vacuum": "monthly"},
        "description": "保留期 <n>d/<n>w 与 VACUUM 周期(daily/weekly/monthly/never)",
    },
]

_INIT_RULES: list[str] = [
    "凭据禁明文:Cookie/Authorization/Token 等凭据键的值只允许 env:VAR 或 keychain:myia/<scope>/<name> 引用;明文 = 拒载(退出码 1)",
    "永不标题指纹:dedup.key 禁用 {title},只用 URL 或组合键",
    "未知字段 fail-fast:sources[] 开放扩展参数,其余节拼错字段名即拒载(含字段路径)",
    "engine: auto 降级链固定 L1 direct_api→L2 static_html→L3 crawl4ai→firecrawl;选择结果回写 SQLite engine_hints,不改用户 YAML",
    "推送语义分层:route 管「推不推」(score 分级),AM/PM 槽位管「发没发过」(防重发),两层正交",
]

_INIT_NEXT_STEPS: list[str] = [
    "1. 向用户收集 required_inputs(与需要的 optional_inputs)",
    "2. 未收集的可选节按 default 补全,生成 12 节品类 YAML",
    "3. myssia test <yaml> --json 逐源试抓,核对提取字段与指纹",
    "4. myssia run <yaml> --dry-run --json 全链演练(不推送)",
    "5. myssia doctor --json 体检,把 findings 清零后再常驻调度",
]


def _init_payload() -> dict[str, Any]:
    """Assemble the structured wizard document (静态内容,确定性输出)."""
    return {
        "command": "init",
        "purpose": "生成品类 YAML(12 节 schema)所需的信息清单;agent 据此向用户收集信息并生成插件,"
        "而非人机问答。schema 权威定义:src/myssia/schema.py",
        "required_inputs": _INIT_REQUIRED_INPUTS,
        "optional_inputs": _INIT_OPTIONAL_INPUTS,
        "rules": _INIT_RULES,
        "next_steps": _INIT_NEXT_STEPS,
    }


def _cmd_init(args: argparse.Namespace) -> int:
    """``myssia init``:stdout 恒为单份 JSON(两种模式同一产物,人读加皮走 stderr)。"""
    payload = _init_payload()
    _print_json(payload)
    if not args.as_json:
        print(
            "世事 init:以上 JSON 是生成品类 YAML 的信息清单(供 agent 消费);"
            "生成后用 myssia test 验证。",
            file=sys.stderr,
        )
    return EXIT_OK


# ---------------------------------------------------------------------------
# 源健康度状态机(list / doctor 共用判据,PRD 10-01-v02-cli-full)
# ---------------------------------------------------------------------------


def _collect_run_history(
    store: SQLiteStore, category: str, *, max_runs: int = HEALTH_HISTORY_RUNS
) -> list[Any]:
    """Newest-first run records for one category (latest_run + previous_run 链)."""
    runs: list[Any] = []
    record = store.latest_run(category)
    while record is not None and len(runs) < max_runs:
        runs.append(record)
        if record.id is None:
            break
        record = store.previous_run(category, before_run_id=record.id)
    return runs


def _source_entries(runs: list[Any]) -> dict[str, list[dict[str, Any]]]:
    """Per-source observations newest-first, read from ``runs.stats.sources``.

    判据只看源级条目数与 skip 原因 —— run 级 status 仅随行展示,不得参与
    判定(run success 掩盖单源静默 0 条的事故不得复发)。
    """
    per_source: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        stats = run.stats if isinstance(run.stats, Mapping) else None
        raw_sources = stats.get("sources") if stats is not None else None
        if not isinstance(raw_sources, list):
            continue  # running/中断行没有 stats,或旧版本行:按无观测处理
        for entry in raw_sources:
            if not isinstance(entry, Mapping):
                continue
            name = entry.get("source")
            if not isinstance(name, str) or not name:
                continue
            item_count = entry.get("item_count")
            per_source.setdefault(name, []).append(
                {
                    "run_id": run.id,
                    "run_status": run.status,
                    "started_at": run.started_at.isoformat()
                    if run.started_at
                    else None,
                    "item_count": item_count
                    if isinstance(item_count, int) and item_count >= 0
                    else 0,
                    "skip_reason": entry.get("skip_reason")
                    if isinstance(entry.get("skip_reason"), str)
                    else None,
                    "failed": bool(entry.get("failed")),
                    "engine": entry.get("engine")
                    if isinstance(entry.get("engine"), str)
                    else None,
                }
            )
    return per_source


def evaluate_source_health(entries: list[dict[str, Any]]) -> dict[str, Any]:
    """One source's health state from newest-first observations.

    Args:
        entries: per-run observations for ONE source, newest first (见
            :func:`_source_entries` 的条目形状)。

    Returns:
        ``{"state", "reason", "observed", "latest", "baseline"}`` — state ∈
        ok/degraded/dead/unknown;baseline 为被评判轮**之前**近 5 次有产出的
        均值(样本不足 5 次时为 None,基线判据不参与;把本轮计入自身基线
        会把 50% 阈值稀释到 ~44%,边界漏报)。
    """
    base: dict[str, Any] = {
        "state": SOURCE_HEALTH_UNKNOWN,
        "reason": "暂无运行记录",
        "observed": len(entries),
        "latest": None,
        "baseline": None,
    }
    if not entries:
        return base
    latest = entries[0]
    base["latest"] = {
        "run_id": latest["run_id"],
        "run_status": latest["run_status"],
        "item_count": latest["item_count"],
        "skip_reason": latest["skip_reason"],
        "failed": latest["failed"],
    }
    last_three = entries[:3]
    if len(last_three) == 3 and all(entry["failed"] for entry in last_three):
        base.update(
            state=SOURCE_HEALTH_DEAD, reason="连续 3 轮采集失败(引擎链耗尽/超时)"
        )
        return base
    if latest["failed"]:
        base.update(
            state=SOURCE_HEALTH_DEGRADED, reason="最新一轮采集失败(未满连续 3 次的死线)"
        )
        return base
    if latest["item_count"] == 0:
        if latest["skip_reason"] in FINGERPRINT_UNCHANGED_REASONS:
            base.update(
                state=SOURCE_HEALTH_OK,
                reason=f"指纹未变({latest['skip_reason']}),0 条属正常跳过",
            )
            return base
        if latest["skip_reason"] in EXPLICIT_EMPTY_SKIP_REASONS:
            base.update(
                state=SOURCE_HEALTH_OK,
                reason=f"引擎显式空态({latest['skip_reason']}):凭据未配置或无输入,"
                "配置凭据/输入后即恢复产出(myssia secret set myia/credhunter/*)",
            )
            return base
        base.update(
            state=SOURCE_HEALTH_DEGRADED,
            reason="指纹未跳过却产出 0 条(页面结构变化/反爬升级疑似,run 级 success 不得掩盖)",
        )
        return base
    samples = [entry["item_count"] for entry in entries[1:] if entry["item_count"] > 0][
        :HEALTH_BASELINE_SAMPLES
    ]
    if len(samples) >= HEALTH_BASELINE_SAMPLES:
        baseline = sum(samples) / len(samples)
        base["baseline"] = round(baseline, 2)
        if latest["item_count"] < HEALTH_BASELINE_DROP_RATIO * baseline:
            base.update(
                state=SOURCE_HEALTH_DEGRADED,
                reason=f"本轮 {latest['item_count']} 条低于近 {len(samples)} 次基线 {baseline:.1f} 的 50%",
            )
            return base
    base.update(state=SOURCE_HEALTH_OK, reason=f"本轮产出 {latest['item_count']} 条")
    return base


def _fingerprint_skip_stats(entries: list[dict[str, Any]]) -> dict[str, int]:
    """指纹跳过率:近 5 次观测里 skip 原因=指纹未变的轮数(window 同基线)。"""
    window = entries[:HEALTH_BASELINE_SAMPLES]
    skipped = sum(
        1 for entry in window if entry["skip_reason"] in FINGERPRINT_UNCHANGED_REASONS
    )
    return {"observed": len(window), "skipped": skipped}


# ---------------------------------------------------------------------------
# 插件装载与凭据引用检查(doctor)
# ---------------------------------------------------------------------------


def _plugin_files(directory: str | Path) -> list[Path]:
    """Sorted ``*.yaml``/``*.yml`` category files directly inside ``directory``.

    Raises:
        NotADirectoryError: the directory does not exist (usage error → exit 1).
    """
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(f"插件目录不存在: {root}")
    return sorted({*root.glob("*.yaml"), *root.glob("*.yml")})


def _load_plugin(
    path: str | Path,
) -> tuple[CategoryConfig | None, list[dict[str, Any]]]:
    """Load one category YAML; load errors come back structured, never raised."""
    try:
        return load_category_file(path), []
    except LoadError as exc:
        return None, _load_error_details(exc)


def _iter_string_leaves(node: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    """Depth-first (path, string-value) leaves of a model_dump tree."""
    if isinstance(node, Mapping):
        for key, value in node.items():
            yield from _iter_string_leaves(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _iter_string_leaves(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


def _collect_credential_refs(config: CategoryConfig) -> list[dict[str, str]]:
    """env:/keychain: references declared by one loaded plugin (含 Bearer 前缀).

    ``plugin:`` 节是 sidecar(不进 ``model_dump``),其 remote token 引用在此
    合并进体检范围 —— doctor 的凭据存在性检查对它一视同仁。同一引用的多个
    使用位(如 sources 头与 plugin 节)都如实列出,不在这里做首次命中截断
    (跨插件去重由 :func:`_merge_credential_entries` 负责)。
    """
    payload = config.model_dump()
    if config.plugin is not None:
        payload["plugin"] = config.plugin.model_dump()
    refs: list[dict[str, str]] = []
    for path, value in _iter_string_leaves(payload):
        match = _SECRET_REF_RE.match(value.strip())
        if match is None:
            continue
        if match.group("env_var") is not None:
            kind, name = "env", match.group("env_var")
        else:
            kind, name = "keychain", match.group("kc")
        refs.append({"path": path, "kind": kind, "name": name, "ref": value.strip()})
    return refs


def _ref_exists(kind: str, name: str, backend: KeychainBackend | None) -> bool | None:
    """Existence probe for one reference; ``None`` = 无法判定(无钥匙链后端)."""
    if kind == "env":
        return name in os.environ
    if backend is None:
        return None
    return backend.get_password(SECRET_SERVICE, name) is not None


def _merge_credential_entries(
    loaded: Sequence[tuple[str, CategoryConfig]], backend: KeychainBackend | None
) -> list[dict[str, Any]]:
    """Dedup references across plugins and probe each one's existence.

    凭据值永不入结果:条目只含引用名与存在性。keychain 引用名非规范形式
    (``myia/<scope>/<name>``)时附迁移提示(存在性仍按原名探测,兼容旧引用)。

    Args:
        loaded: ``(plugin_id, config)`` pairs for every plugin that loaded.
        backend: probed keychain backend; ``None`` = 不可用(exists 记 None).
    """
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for plugin_id, config in loaded:
        for ref in _collect_credential_refs(config):
            key = (ref["kind"], ref["name"])
            entry = merged.setdefault(
                key,
                {
                    "kind": ref["kind"],
                    "name": ref["name"],
                    "ref": ref["ref"],
                    "paths": [],
                    "plugins": [],
                },
            )
            entry["paths"].append({"plugin": plugin_id, "path": ref["path"]})
            if plugin_id and plugin_id not in entry["plugins"]:
                entry["plugins"].append(plugin_id)
    results: list[dict[str, Any]] = []
    for entry in merged.values():
        exists = _ref_exists(entry["kind"], entry["name"], backend)
        result: dict[str, Any] = {
            "kind": entry["kind"],
            "name": entry["name"],
            "ref": entry["ref"],
            "paths": entry["paths"],
            "plugins": entry["plugins"],
            "exists": exists,
        }
        if entry["kind"] == "keychain":
            try:
                validate_secret_name(entry["name"])
            except SecretError as exc:
                result["note"] = str(exc)
        results.append(result)
    return sorted(results, key=lambda item: (item["kind"], item["name"]))


# ---------------------------------------------------------------------------
# 代理连通性(doctor --config)与 HTTP client 工厂
# ---------------------------------------------------------------------------


def _build_async_client(**kwargs: Any) -> httpx.AsyncClient:
    """HTTP client factory for trial fetches / proxy probes(测试注入点).

    测试 monkeypatch 本函数返回 ``MockTransport`` 客户端,实现零真实网络;
    生产路径即 ``httpx.AsyncClient(**kwargs)``。
    """
    return httpx.AsyncClient(**kwargs)


async def _probe_proxy_pools(
    pools: Any,
    *,
    timeout: float,
    backend: KeychainBackend | None,
) -> list[dict[str, Any]]:
    """Probe every declared upstream; credentials are expanded then never shown.

    逐池保序、池内 ``resolve_upstreams`` 展开后**全部并入同一并行集**
    (asyncio.gather):每个上游各吃自己的 probe-timeout,总耗时≈最慢上游
    而非累加 —— doctor 必须在桌面 sidecar 的固定壳超时(120s)内回话,
    v1.1 评审实测串行下 13 个不可达池即顶穿(130.6s)。每条结果带
    ``upstream_index``/``upstreams``(单上游池恒 ``0``/``1``,对既有 JSON
    消费方是纯增字段);单池凭据解析失败不拖垮其余池(部分失败语义不变)。
    """

    async def _probe_upstream(
        name: str, index: int, total: int, resolved: str
    ) -> dict[str, Any]:
        client = _build_async_client(proxy=resolved, timeout=timeout)
        try:
            check = await check_proxy_connectivity(
                resolved, client=client, timeout=timeout
            )
        finally:
            await client.aclose()
        return {
            "pool": name,
            "upstream_index": index,
            "upstreams": total,
            **check.to_dict(),
        }

    async def _probe_pool(name: str) -> list[dict[str, Any]]:
        try:
            resolved_list = pools.resolve_upstreams(name, backend=backend)
        except Exception as exc:  # noqa: BLE001 - 单池失败不拖垮其余池的诊断(部分失败语义)
            logger.warning("代理池凭据解析失败 pool=%s: %s", name, exc)
            raw = mask_proxy_url(pools.raw_url(name))
            return [
                {
                    "pool": name,
                    "upstream_index": 0,
                    "upstreams": 1,
                    "ok": False,
                    "message": f"代理池凭据引用无法解析: {exc}",
                    "proxy_url": raw,
                    "error_type": classify_exception(exc),
                }
            ]
        return list(
            await asyncio.gather(
                *(
                    _probe_upstream(name, index, len(resolved_list), resolved)
                    for index, resolved in enumerate(resolved_list)
                )
            )
        )

    pool_batches = await asyncio.gather(*(_probe_pool(name) for name in pools.names()))
    return [row for batch in pool_batches for row in batch]


# ---------------------------------------------------------------------------
# myssia test:单源试抓(不推送不入库)
# ---------------------------------------------------------------------------


def _preview_value(value: Any) -> Any:
    """Truncate one extracted field for preview(标量直出,其余转字符串截断)."""
    if value is None or isinstance(value, (str, int, float, bool)):
        text = value
    else:
        text = str(value)
    if isinstance(text, str) and len(text) > TEST_PREVIEW_VALUE_CHARS:
        return text[:TEST_PREVIEW_VALUE_CHARS] + "…"
    return text


def _dedup_key_preview(
    raw: Mapping[str, Any], registry: DedupRegistry, template: str
) -> dict[str, Any]:
    """Compute one item's dedup-key preview(组合键/URL 键,即条目指纹)."""
    view = {**registry.key_context(), **dict(raw)}
    try:
        return {"dedup_key": DedupRegistry.make_key(template, view)}
    except ValueError as exc:
        return {"dedup_key": None, "dedup_key_error": str(exc)}


async def _test_one_source(
    source: Any,
    context: FetchContext,
    registry: DedupRegistry,
    config: CategoryConfig,
    timeout: float,
) -> dict[str, Any]:
    """Trial-fetch one source through its real degrade chain (结构化结果)."""
    report: dict[str, Any] = {
        "source": source.name,
        "url": source.url,
        "engine_configured": source.engine,
        "ok": False,
        "item_count": 0,
        "fingerprint": None,
        "items": [],
        "failures": [],
        "error": None,
    }
    try:
        outcome = await asyncio.wait_for(fetch_source(source, context), timeout=timeout)
    except TimeoutError:
        report["error"] = {
            "error_type": "timeout",
            "message": f"试抓超时(>{timeout:.0f}s)",
        }
        return report
    report["engine"] = outcome.engine or source.engine
    report["ok"] = outcome.engine is not None
    report["item_count"] = len(outcome.items)
    report["failures"] = [failure.to_dict() for failure in outcome.failures]
    report["fingerprint"] = _fingerprint_view(outcome)
    for raw in outcome.items[:TEST_PREVIEW_ITEMS]:
        item: dict[str, Any] = {
            "fields": {key: _preview_value(value) for key, value in raw.items()},
            **_dedup_key_preview(raw, registry, config.dedup.key),
        }
        report["items"].append(item)
    if len(outcome.items) > TEST_PREVIEW_ITEMS:
        report["items_truncated"] = True
    return report


def _fingerprint_view(outcome: Any) -> dict[str, Any]:
    """Trial fetch's fingerprint view(变更指纹判定 + 对调度行为的含义)."""
    skip_reason = outcome.skip_reason
    if outcome.engine is None:
        verdict = "unknown"
    elif skip_reason in FINGERPRINT_UNCHANGED_REASONS:
        verdict = "unchanged_skip"
    elif skip_reason in EXPLICIT_EMPTY_SKIP_REASONS:
        verdict = "explicit_empty_skip"
    else:
        verdict = "changed_or_first_fetch"
    return {
        "skip_reason": skip_reason,
        "verdict": verdict,
        "meaning": {
            "unchanged_skip": "变更指纹未变,线上调度会跳过本轮(正常)",
            "explicit_empty_skip": "引擎显式空态(凭据未配置/无输入,AC6;配置后即恢复产出)",
            "changed_or_first_fetch": "内容有变化或首次抓取,线上调度会正常提取",
            "unknown": "引擎链耗尽,未取得指纹判定",
        }[verdict],
    }


def _print_human_test(payload: dict[str, Any]) -> None:
    """人类可读的试抓摘要(与 --json 同一信息)。"""
    print(f"世事 test:{payload['yaml']}(试抓不入库不推送)")
    for source in payload["sources"]:
        state = "成功" if source["ok"] else "失败"
        print(
            f"  源 {source['source']}({state},engine={source.get('engine')},条目 {source['item_count']})"
        )
        fingerprint = source.get("fingerprint") or {}
        if fingerprint.get("skip_reason"):
            print(
                f"    指纹:skip={fingerprint['skip_reason']}({fingerprint['meaning']})"
            )
        elif fingerprint:
            print(f"    指纹:{fingerprint['meaning']}")
        for item in source["items"]:
            print(
                f"    条目 dedup_key={item.get('dedup_key')} fields={json.dumps(item['fields'], ensure_ascii=False)}"
            )
        for failure in source["failures"]:
            print(
                f"    引擎失败 {failure['engine']} [{failure['error_type']}] {failure['message']}"
            )
        if source.get("error"):
            print(
                f"    错误 [{source['error']['error_type']}] {source['error']['message']}"
            )
    print(f"状态:{payload['status']}")


def _resolve_pools(config_path: str | None, as_json: bool) -> tuple[Any | None, int]:
    """Load the global pools declaration for ``--config``(test/run/doctor 共用;可选)."""
    if config_path is None:
        return None, EXIT_OK
    try:
        return load_proxy_pools_file(config_path), EXIT_OK
    except LoadError as exc:
        _emit_config_error(
            _load_error_details(exc), source=str(config_path), as_json=as_json
        )
        return None, EXIT_CONFIG_ERROR


def _cmd_test(args: argparse.Namespace) -> int:
    """``myssia test <yaml> [--source name]``:试抓 → 字段与指纹;0/1/2/3。"""
    _configure_logging(as_json=args.as_json)
    try:
        config = load_category_file(args.yaml)
    except LoadError as exc:
        _emit_config_error(
            _load_error_details(exc), source=exc.source, as_json=args.as_json
        )
        return EXIT_CONFIG_ERROR
    sources = list(config.sources)
    if args.source is not None:
        sources = [source for source in sources if source.name == args.source]
        if not sources:
            known = [source.name for source in config.sources]
            _emit_config_error(
                [
                    {
                        "path": "$.sources",
                        "error_type": "source_not_found",
                        "message": f"源 {args.source!r} 不存在,可用源: {known}",
                    }
                ],
                source=str(args.yaml),
                as_json=args.as_json,
            )
            return EXIT_CONFIG_ERROR
    pools, exit_code = _resolve_pools(args.config, args.as_json)
    if pools is None and exit_code != EXIT_OK:
        return exit_code
    # 试抓零持久化:基线/引擎提示全部写进内存库,命令结束即弃。
    store = SQLiteStore(":memory:")
    registry = DedupRegistry(store, tz=_category_tz(config))
    client = _build_async_client(timeout=args.timeout)
    context = FetchContext(
        client=client, store=store, timeout=args.timeout, proxy_pools=pools
    )
    try:
        reports = asyncio.run(
            _test_sources(sources, context, registry, config, args.timeout)
        )
    finally:
        store.close()

    failed = [report for report in reports if not report["ok"]]
    status = (
        "failed"
        if len(failed) == len(reports)
        else ("partial" if failed else "success")
    )
    payload = {
        "command": "test",
        "yaml": str(args.yaml),
        "note": "试抓不入库不推送;dedup_key 为去重键预览",
        "sources": reports,
        "status": status,
    }
    if args.as_json:
        _print_json(payload)
    else:
        _print_human_test(payload)
    if status == "failed":
        return EXIT_FETCH_ALL_FAILED
    return EXIT_PARTIAL if failed else EXIT_OK


async def _test_sources(
    sources: list[Any],
    context: FetchContext,
    registry: DedupRegistry,
    config: CategoryConfig,
    timeout: float,
) -> list[dict[str, Any]]:
    """Run trial fetches sequentially (同插件共享限速与指纹基线内存库)."""
    reports: list[dict[str, Any]] = []
    try:
        for source in sources:
            reports.append(
                await _test_one_source(source, context, registry, config, timeout)
            )
    finally:
        await context.aclose_pool_clients()
    return reports


# ---------------------------------------------------------------------------
# myssia list / myssia doctor:插件清单、健康度与结构化诊断
# ---------------------------------------------------------------------------


def _category_tz(config: CategoryConfig) -> ZoneInfo | None:
    """The category timezone as ZoneInfo(None = 系统本地时区,加载期已校验)."""
    if not config.timezone:
        return None
    try:
        return ZoneInfo(config.timezone)
    except (ZoneInfoNotFoundError, ValueError, OSError):  # 防御:加载期已校验
        return None


def _next_fire_at(config: CategoryConfig) -> str | None:
    """Next cron fire time in the category timezone(调度下次触发时间)."""
    try:
        trigger = build_cron_trigger(config.schedule, config.timezone)
        now = datetime.now(_category_tz(config) or ZoneInfo("UTC")).astimezone()
        next_fire = trigger.get_next_fire_time(None, now)
    except (ValueError, ZoneInfoNotFoundError, OSError) as exc:  # 防御:加载期已校验
        logger.warning("下次触发时间计算失败 id=%s: %s", config.id, exc)
        return None
    return next_fire.astimezone().isoformat() if next_fire is not None else None


def _enrich_section(
    config: CategoryConfig, store: SQLiteStore | None
) -> dict[str, Any]:
    """enrich 预算/缓存状态(只展示;端点设置走构造注入,不在 YAML)。"""
    section: dict[str, Any] = {
        "enabled": config.enrich.enabled,
        "model": config.enrich.model,
        "scores": list(config.enrich.scores),
        "batch": config.enrich.batch,
        "cache": config.enrich.cache,
        "budget_per_run": config.enrich.budget_per_run,
    }
    if store is not None:
        section["cache_rows"] = _enrich_cache_rows(store)
    return section


def _enrich_cache_rows(store: SQLiteStore) -> int | None:
    """enrich_cache 行数(默认 SQLite 后端直查;异常按 None 降级,不误报)."""
    conn = getattr(store, "conn", None)
    if conn is None:
        return None
    try:
        row = conn.execute("SELECT COUNT(*) FROM enrich_cache").fetchone()
    except Exception as exc:  # noqa: BLE001 - 诊断展示,失败降级为未知
        logger.debug("enrich_cache 计数失败(按未知处理): %s", exc)
        return None
    return int(row[0]) if row is not None else None


def _source_report(
    config: CategoryConfig | None,
    store: SQLiteStore | None,
    store_error: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    """Per-source health rows for one plugin (list/doctor 共用;未加载 → 空表).

    库打不开(store_error)时健康度如实标「存储无法打开」,不伪装成
    「暂无运行记录」——把「库坏了」报成「没跑过」属静默掩盖。
    """
    entries_by_source: dict[str, list[dict[str, Any]]] = {}
    if config is None:
        return [], entries_by_source
    if store is not None:
        runs = _collect_run_history(store, config.id)
        entries_by_source = _source_entries(runs)
    store_down_health: dict[str, Any] | None = None
    if store is None and store_error is not None:
        store_down_health = {
            "state": SOURCE_HEALTH_UNKNOWN,
            "reason": f"存储无法打开({store_error.get('error_type', 'store_error')}),健康度未知",
            "observed": 0,
            "latest": None,
            "baseline": None,
        }
    rows: list[dict[str, Any]] = []
    for source in config.sources:
        entries = entries_by_source.get(source.name, [])
        hint = store.get_engine_hint(source.url) if store is not None else None
        rows.append(
            {
                "name": source.name,
                "url": source.url,
                "engine": source.engine,
                "engine_hint": hint,
                "health": store_down_health or evaluate_source_health(entries),
                "fingerprint_skips": _fingerprint_skip_stats(entries),
            }
        )
    return rows, entries_by_source


def _plugin_identity(
    path: Path, config: CategoryConfig | None, errors: list[dict[str, Any]]
) -> dict[str, Any]:
    """Common identity block of a plugin report (list/doctor 共用)."""
    return {
        "file": str(path),
        "id": config.id if config else None,
        "name": config.name if config else None,
        "schedule": config.schedule if config else None,
        "timezone": config.timezone if config else None,
        "push_channels": [push.channel for push in config.push] if config else [],
        "loaded": config is not None,
        "load_errors": errors or None,
    }


def _plugin_report(
    path: Path, store: SQLiteStore | None, store_error: dict[str, Any] | None = None
) -> dict[str, Any]:
    """One plugin's list view: identity + per-source health (errors structured)."""
    config, errors = _load_plugin(path)
    report = _plugin_identity(path, config, errors)
    report["sources"] = (
        _source_report(config, store, store_error)[0] if config is not None else []
    )
    return report


def _print_human_list(payload: dict[str, Any]) -> None:
    """人类可读的插件清单(与 --json 同一信息)。"""
    print(
        f"世事 list:目录 {payload['plugins_dir']}(db={payload['db']})共 {len(payload['plugins'])} 个插件"
    )
    for plugin in payload["plugins"]:
        if not plugin["loaded"]:
            print(f"  {plugin['file']} — 加载失败")
            for detail in plugin["load_errors"] or []:
                print(
                    f"    [{detail['error_type']}] {detail['path']} — {detail['message']}"
                )
            continue
        print(
            f"  {plugin['file']} — {plugin['id']}({plugin['name']})schedule={plugin['schedule']}"
        )
        for source in plugin["sources"]:
            health = source["health"]
            skips = source["fingerprint_skips"]
            hint = f",hint={source['engine_hint']}" if source["engine_hint"] else ""
            print(
                f"    源 {source['name']}[{health['state']}] {health['reason']}"
                f"(指纹跳过 {skips['skipped']}/{skips['observed']}{hint})"
            )


def _cmd_list(args: argparse.Namespace) -> int:
    """``myssia list``:插件清单 + 源健康度;信息性命令,完成即 0(目录错=1)。"""
    as_json = args.as_json
    _configure_logging(as_json=as_json)
    try:
        files = _plugin_files(args.plugins_dir)
    except NotADirectoryError as exc:
        _emit_generic_error("plugins_dir", str(exc), as_json=as_json)
        return EXIT_CONFIG_ERROR
    store, store_error = _open_store(args.db, as_json=as_json)
    payload = {
        "command": "list",
        "plugins_dir": str(args.plugins_dir),
        "db": str(args.db),
        "store_error": store_error,
        "plugins": [_plugin_report(path, store, store_error) for path in files],
    }
    if store is not None:
        store.close()
    if as_json:
        _print_json(payload)
    else:
        _print_human_list(payload)
    return EXIT_OK


def _open_store(
    db_path: str, *, as_json: bool
) -> tuple[SQLiteStore | None, dict[str, Any] | None]:
    """Open the default SQLite store for diagnostics; corrupt/newer → (None, structured error).

    doctor/list 是诊断入口:库损坏或版本过新必须结构化可见,而不是让命令
    崩掉。错误**不在这里打印**——--json 契约是 stdout 恰好一份 JSON 文档,
    由调用方把错误并入唯一一份报告(list 顶层 ``store_error`` 字段 /
    doctor ``findings``);人类模式才直接打到 stderr。
    """
    try:
        return SQLiteStore(db_path), None
    except StoreSchemaError as exc:
        detail: dict[str, Any] = {
            "error_type": exc.code,
            "message": str(exc),
            **exc.details,
        }
        if not as_json:
            print(f"存储无法打开 db={db_path}: {exc}", file=sys.stderr)
        return None, detail


def _finding(
    findings: list[dict[str, Any]],
    *,
    severity: str,
    scope: str,
    code: str,
    message: str,
) -> None:
    """Append one structured finding(0=成功 1=配置 2/3 同 run 语义,doctor 只产 findings)."""
    findings.append(
        {"severity": severity, "scope": scope, "code": code, "message": message}
    )


def _plugin_findings(report: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    """Derive findings from one plugin's load errors + source health."""
    scope = f"plugin:{report['file']}"
    for detail in report["load_errors"] or []:
        _finding(
            findings,
            severity="error",
            scope=scope,
            code=str(detail.get("error_type", "config_error")),
            message=f"{detail.get('path', '$')}: {detail.get('message', '')}",
        )
    for source in report["sources"]:
        health = source["health"]
        source_scope = f"{scope}/source:{source['name']}"
        if health["state"] == SOURCE_HEALTH_DEAD:
            _finding(
                findings,
                severity="error",
                scope=source_scope,
                code="source_dead",
                message=health["reason"],
            )
        elif health["state"] == SOURCE_HEALTH_DEGRADED:
            _finding(
                findings,
                severity="warning",
                scope=source_scope,
                code="source_degraded",
                message=health["reason"],
            )


def _format_ref_paths(entry: Mapping[str, Any]) -> str:
    """Render a credential entry's usage sites as ``plugin:path``(诊断定位)."""
    return "; ".join(f"{usage['plugin']}:{usage['path']}" for usage in entry["paths"])


def _credential_findings(
    entries: list[dict[str, Any]],
    *,
    backend_error: SecretError | None,
    findings: list[dict[str, Any]],
) -> None:
    """Derive findings from credential-reference probes(引用存在性可检可修)."""
    keychain_refs = [entry for entry in entries if entry["kind"] == "keychain"]
    if backend_error is not None and keychain_refs:
        _finding(
            findings,
            severity="error",
            scope="credentials",
            code=getattr(backend_error, "code", "keychain_backend_unavailable"),
            message=f"{backend_error};以下 keychain 引用无法核验: "
            f"{[entry['ref'] for entry in keychain_refs]}",
        )
    for entry in entries:
        scope = "credentials"
        if entry["kind"] == "env" and entry["exists"] is False:
            _finding(
                findings,
                severity="warning",
                scope=scope,
                code="env_ref_missing",
                message=f"环境变量 {entry['name']} 未设置(引用于 {_format_ref_paths(entry)})",
            )
        if entry["kind"] == "keychain":
            if entry["exists"] is False:
                _finding(
                    findings,
                    severity="error",
                    scope=scope,
                    code="keychain_ref_missing",
                    message=f"钥匙链中不存在凭据 {entry['name']}(引用于 {_format_ref_paths(entry)});"
                    f"请执行 myssia secret set {entry['name']} 写入",
                )
            if entry.get("note"):
                _finding(
                    findings,
                    severity="warning",
                    scope=scope,
                    code="keychain_name_noncanonical",
                    message=entry["note"],
                )


def _proxy_findings(
    pools_result: list[dict[str, Any]], findings: list[dict[str, Any]]
) -> None:
    """Derive findings from proxy probes(代理挂 ≠ 源死,warning 语义)."""
    for entry in pools_result:
        if entry.get("ok"):
            continue
        code = entry.get("error_type") or "proxy_unreachable"
        severity = (
            "error"
            if code in ("credential_unresolved", "invalid_proxy_url")
            else "warning"
        )
        _finding(
            findings,
            severity=severity,
            scope=f"proxy:{entry.get('pool')}",
            code=code,
            message=str(entry.get("message", "代理探测失败")),
        )


def _telegram_poll_conflict_findings(
    loaded: Sequence[tuple[str, CategoryConfig]], findings: list[dict[str, Any]]
) -> None:
    """多品类共享 bot token 的单接收方语义披露(10-05-telegram-token-dedupe).

    telegram 通道的 bot token 固定解析自 ``env:TELEGRAM_BOT_TOKEN``(schema
    不设 per-channel token 位),所以 ≥2 个已加载品类共配 telegram 通道时,
    它们的常驻进程(``--loop``)名义上各起一个 ``getUpdates`` 轮询——Telegram
    对同 token 并发轮询方回 409 Conflict。产品已在库内保证同 token 单轮询器
    (轮询租约:先到常驻进程独占,后到者禁动,不再互踢),因此共配是受支持
    形态;本 finding 只披露残余语义:后到常驻品类的 TG 反馈与会话目录观测
    会入**先到**常驻品类的库。单次 run 不轮询、不受影响。
    """
    telegram_plugins = [
        plugin_id
        for plugin_id, config in loaded
        if any(push.channel == "telegram" for push in config.push)
    ]
    if len(telegram_plugins) < 2:
        return
    _finding(
        findings,
        severity="warning",
        scope="feedback",
        code="telegram_token_poll_conflict",
        message=(
            f"{len(telegram_plugins)} 个品类共享同一 bot token(env:TELEGRAM_BOT_TOKEN)"
            f"且都配置了 telegram 通道:{'、'.join(telegram_plugins)}。Telegram 对同 "
            "token 并发 getUpdates 回 409 Conflict,产品已内置同 token 单轮询器防护:"
            "先到的常驻进程(myssia run --loop)独占反馈接收,后到者轮询禁动"
            "(推送不受影响)。注意:后到常驻品类的 TG 反馈会入先到者的库——"
            "如需品类各自独立接收反馈,请为品类单独配置 bot token(另建 BotFather "
            "bot)或仅让其中一个品类常驻。"
        ),
    )


#: 表格还原组件的 (import 模块名, 发行版名) 清单(10-05-table-restore AC3)。
#: 与 pyproject extras ``table`` / desktop/resources/components.json 的
#: pip_spec 同源闭包(extras 域版本窗 >=3.0.2,<4,组件注册表钉 ==3.0.2;
#: tqdm 是 rapid-table 3.0.2 轮未声明进 requires-dist 的隐性 import,
#: extras 显式补——探测面三件齐,任一缺装即出 finding;三侧闭包发行名
#: 集合相等由 tests/cli/test_cli_full.py 三方锁测把守);
#: doctor 只探测不导入 —— find_spec 零模型加载零副作用(真引擎单例在
#: :func:`myssia.vision.table.run_table` 惰性建)。
_TABLE_COMPONENT_PACKAGES: tuple[tuple[str, str], ...] = (
    ("rapid_table", "rapid-table"),
    ("rapidocr_onnxruntime", "rapidocr-onnxruntime"),
    ("tqdm", "tqdm"),
)


def _package_available(module: str) -> bool:
    """import 探测(不执行模块代码);测试经 monkeypatch 替身控三态。"""
    import importlib.util  # 惰性:doctor 冷路径,不为它抬核心 import 面

    return importlib.util.find_spec(module) is not None


def _table_component_findings(
    loaded: Sequence[tuple[str, CategoryConfig]], findings: list[dict[str, Any]]
) -> None:
    """表格还原组件缺装披露(10-05-table-restore AC3,既有 findings 通道)。

    声明 ``images.table: true``(且图片环 ``enabled``)的品类,若
    rapid-table / rapidocr-onnxruntime / tqdm 任一未装,出 **warning** 级 finding
    带安装命令:缺装不是配置错(不翻 ``healthy``),但运行期只会静默降级为
    ``metadata.table_status = table_provider_error``(R6 红线:绝不阻管线)
    —— doctor 提前披露,让「装了开关却没装引擎」可预期、可修复。装齐 =
    正常态,零 finding(与 gate_disabled 的 info 语义不同:这里功能已声明
    且会降级,值得 warning)。``images.enabled: false`` 时整环零进入,
    table 分支不可达,不出 finding。
    """
    categories = [
        plugin_id
        for plugin_id, config in loaded
        if config.images is not None and config.images.enabled and config.images.table
    ]
    if not categories:
        return
    missing = [
        dist_name
        for module_name, dist_name in _TABLE_COMPONENT_PACKAGES
        if not _package_available(module_name)
    ]
    if not missing:
        return
    _finding(
        findings,
        severity="warning",
        scope="components",
        code="table_dependency_missing",
        message=(
            f"品类 {'、'.join(sorted(categories))} 声明 images.table: true,"
            f"但当前 Python 环境缺装 {'、'.join(missing)}:表格还原将降级为"
            f" metadata.table_status=table_provider_error(不阻管线)。安装:"
            f'uv sync --extra table(或 pip install "myssia[table]";'
            f"桌面端:设置 → Python 环境 → 组件「表格还原」开关)"
        ),
    )


def _apprise_component_findings(
    loaded: Sequence[tuple[str, CategoryConfig]], findings: list[dict[str, Any]]
) -> None:
    """apprise 统一推送依赖缺装披露(10-05-push-apprise,table 先例同通道)。

    配置了 ``apprise`` 通道的品类,若 apprise 库未装,发送期只会逐次结构化
    ``apprise_unavailable``——doctor 提前披露带安装命令(缺装不是配置错,
    不翻 ``healthy``)。**不惊扰未配置用户**:没配该通道 = 正常态零 finding
    (惰性 import 面,未配置永不触发;同 TG 凭据不可解析 INFO 先例的克制)。
    """
    categories = [
        plugin_id
        for plugin_id, config in loaded
        if any(push.channel == "apprise" for push in config.push)
    ]
    if not categories:
        return
    if _package_available("apprise"):
        return
    _finding(
        findings,
        severity="warning",
        scope="components",
        code="apprise_not_installed",
        message=(
            f"品类 {'、'.join(sorted(categories))} 配置了 apprise 通道(统一推送),"
            "但当前 Python 环境未安装 apprise 库:该通道推送将结构化失败"
            "(apprise_unavailable,不阻其他通道)。安装:uv sync --extra apprise"
            '(或 pip install "myssia[apprise]")'
        ),
    )


def _print_human_doctor(payload: dict[str, Any]) -> None:
    """人类可读的诊断报告(与 --json 同一信息)。"""
    print(
        f"世事 doctor(db={payload['db']})healthy={'是' if payload['healthy'] else '否'}"
    )
    for plugin in payload["plugins"]:
        if not plugin["loaded"]:
            print(f"  插件 {plugin['file']} — 加载失败")
            continue
        next_fire = plugin.get("next_fire_at") or "未知"
        print(f"  插件 {plugin['id']}({plugin['name']})下次触发 {next_fire}")
        for source in plugin["sources"]:
            health = source["health"]
            hint = f",hint={source['engine_hint']}" if source["engine_hint"] else ""
            print(
                f"    源 {source['name']}[{health['state']}] {health['reason']}{hint}"
            )
        enrich = plugin.get("enrich") or {}
        if enrich.get("enabled"):
            print(
                f"    enrich model={enrich['model']} budget/run={enrich['budget_per_run']} "
                f"cache={enrich.get('cache_rows')} 行"
            )
    credentials = payload["credentials"]
    for entry in credentials["entries"]:
        state = {True: "存在", False: "不存在", None: "无法核验"}[entry["exists"]]
        print(f"  凭据 {entry['ref']} — {state}")
    proxy = payload["proxy"]
    for entry in proxy.get("pools", []):
        state = "连通" if entry.get("ok") else "失败"
        latency = (
            f" {entry['latency_seconds']}s"
            if entry.get("latency_seconds") is not None
            else ""
        )
        # 逐上游序号只对多上游池展示(单上游池输出形态与既往等价,AC4)
        which = f"#{entry['upstream_index']}" if entry.get("upstreams", 1) > 1 else ""
        print(
            f"  代理池 {entry.get('pool')}{which} — {state}{latency} {entry.get('message', '')}"
        )
    gates = payload.get("gates") or {}
    if gates.get("error"):
        first = (gates["error"].get("errors") or [{}])[0]
        print(f"  门槛配置拒载(已按全关处理):{first.get('message', gates['error'])}")
    for item in gates.get("gated") or []:
        state = "已启用" if item["enabled"] else "未启用(正常态,知情后 myssia gates set 可开启)"
        print(f"  门槛件 {item['id']}[{item['gate']}] — {state}")
    for item in payload["findings"]:
        print(
            f"  [{item['severity']}] {item['scope']} {item['code']}: {item['message']}"
        )
    print(
        f"findings: {payload['summary']['errors']} 错误 / {payload['summary']['warnings']} 警告"
    )


def _cmd_doctor(args: argparse.Namespace) -> int:
    """``myssia doctor``:结构化诊断;诊断完成即 0,问题全在 findings。"""
    as_json = args.as_json
    _configure_logging(as_json=as_json)
    try:
        files = _doctor_targets(args, as_json=as_json)
    except NotADirectoryError as exc:
        _emit_generic_error("plugins_dir", str(exc), as_json=as_json)
        return EXIT_CONFIG_ERROR
    if files is None:
        return EXIT_CONFIG_ERROR

    store, store_error = _open_store(args.db, as_json=as_json)
    findings: list[dict[str, Any]] = []
    if store_error is not None:
        _finding(
            findings,
            severity="error",
            scope="store",
            code="store_error",
            message=f"存储无法打开 db={args.db}:{store_error['message']}",
        )

    plugins, loaded = _doctor_plugins(files, store, findings, store_error)
    backend, backend_error = _acquire_keychain_backend()
    credential_entries = _merge_credential_entries(loaded, backend)
    _credential_findings(
        credential_entries, backend_error=backend_error, findings=findings
    )
    _telegram_poll_conflict_findings(loaded, findings)
    _table_component_findings(loaded, findings)
    _apprise_component_findings(loaded, findings)
    proxy_section = _doctor_proxy(args, backend, findings)
    gates_section = _doctor_gates(args, findings)
    payload = _doctor_payload(
        args,
        plugins=plugins,
        backend=backend,
        backend_error=backend_error,
        credential_entries=credential_entries,
        proxy_section=proxy_section,
        gates_section=gates_section,
        findings=findings,
    )
    if as_json:
        _print_json(payload)
    else:
        _print_human_doctor(payload)
    if store is not None:
        store.close()
    return EXIT_OK


def _doctor_payload(
    args: argparse.Namespace,
    *,
    plugins: list[dict[str, Any]],
    backend: KeychainBackend | None,
    backend_error: SecretError | None,
    credential_entries: list[dict[str, Any]],
    proxy_section: dict[str, Any],
    gates_section: dict[str, Any],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Assemble the doctor report (healthy = 无 error 级 finding;info 不计病)."""
    errors = sum(1 for item in findings if item["severity"] == "error")
    warnings = sum(1 for item in findings if item["severity"] == "warning")
    return {
        "command": "doctor",
        "generated_at": datetime.now().astimezone().isoformat(),
        "db": str(args.db),
        "healthy": errors == 0,
        "plugins": plugins,
        "credentials": {
            "backend_available": backend is not None,
            "backend_error": str(backend_error) if backend_error else None,
            "entries": credential_entries,
        },
        "proxy": proxy_section,
        "gates": gates_section,
        "findings": findings,
        "summary": {
            "plugins": len(plugins),
            "sources": sum(len(report["sources"]) for report in plugins),
            "errors": errors,
            "warnings": warnings,
        },
    }


def _doctor_targets(args: argparse.Namespace, *, as_json: bool) -> list[Path] | None:
    """Resolve diagnosis targets: explicit YAMLs or the plugins-dir scan.

    Returns:
        The file list; ``None`` when an explicitly named YAML is missing
        (already reported as a structured usage error, exit code 1).
    """
    if not args.yaml:
        return _plugin_files(args.plugins_dir)
    files = [Path(path) for path in args.yaml]
    missing = [str(path) for path in files if not path.is_file()]
    if missing:
        _emit_generic_error(
            "file_not_found", f"品类 YAML 不存在: {missing}", as_json=as_json
        )
        return None
    return files


def _doctor_plugins(
    files: list[Path],
    store: SQLiteStore | None,
    findings: list[dict[str, Any]],
    store_error: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], list[tuple[str, CategoryConfig]]]:
    """Plugin section: identity + health + schedule + enrich(加载失败即 finding)."""
    plugins: list[dict[str, Any]] = []
    loaded: list[tuple[str, CategoryConfig]] = []
    for path in files:
        config, errors = _load_plugin(path)
        report = _plugin_identity(path, config, errors)
        if config is not None:
            loaded.append((config.id, config))
            report["sources"] = _source_report(config, store, store_error)[0]
            report["next_fire_at"] = _next_fire_at(config)
            report["enrich"] = _enrich_section(config, store)
        else:
            report["sources"] = []
            report["next_fire_at"] = None
            report["enrich"] = None
        _plugin_findings(report, findings)
        plugins.append(report)
    return plugins, loaded


def _acquire_keychain_backend() -> tuple[KeychainBackend | None, SecretError | None]:
    """Acquire the keychain backend for existence probes(不可用不炸诊断)."""
    try:
        return get_backend(), None
    except SecretError as exc:
        logger.warning("钥匙链后端不可用(凭据存在性核验降级): %s", exc)
        return None, exc


def _doctor_proxy(
    args: argparse.Namespace,
    backend: KeychainBackend | None,
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    """Proxy connectivity section: probe every declared pool when --config given."""
    section: dict[str, Any] = {"config": args.config, "pools": []}
    if not args.config:
        return section
    try:
        pools = load_proxy_pools_file(args.config)
    except LoadError as exc:
        section["error"] = _load_error_details(exc)
        for detail in _load_error_details(exc):
            _finding(
                findings,
                severity="error",
                scope=f"config:{args.config}",
                code=str(detail.get("error_type", "config_error")),
                message=f"{detail.get('path', '$')}: {detail.get('message', '')}",
            )
        return section
    section["pools"] = asyncio.run(
        _probe_proxy_pools(pools, timeout=args.probe_timeout, backend=backend)
    )
    _proxy_findings(section["pools"], findings)
    return section


#: 门槛类型 → 知情文案(doctor info finding / list 徽标共用;§6.2 三态模板)。
_GATE_ADVISORIES: dict[str, str] = {
    "paid": "付费知情:按页计费,你的采集目标清单将经对方服务器并与你的账号绑定",
    "trace": "第三方留痕:采集目标将经公共实例等第三方服务器",
    "platform": "自有实例门槛:需自部署实例 endpoint(组织性不执法,不拦 direct_api 源)",
    "stale": "停更知情:上游已冻结,启用即接受 pin 版自担维护",
}

#: 已知公共实例域(D9 第三方留痕知情;小清单内置,勿引外部依赖)。
#: platforms 门槛语义是「自有实例」—— endpoint 指向公共实例即目标清单经
#: 第三方服务器并留痕,doctor 出 info 提示(组织性不执法,D6;不做拦截)。
KNOWN_PUBLIC_INSTANCE_HOSTS: frozenset[str] = frozenset({"rsshub.app"})


def _public_instance_hint(endpoint: str) -> str | None:
    """endpoint 命中已知公共实例域 → 返回该域;未命中/空 endpoint → None。"""
    if not endpoint:
        return None
    host = (urlsplit(endpoint).hostname or "").lower()
    return host if host in KNOWN_PUBLIC_INSTANCE_HOSTS else None


def _doctor_gates(args: argparse.Namespace, findings: list[dict[str, Any]]) -> dict[str, Any]:
    """门槛件诊断段:坏 gates.yaml = warning(fail-closed 全关);未启用门槛件 = info。

    词表纪律(§6.2):用户没开门槛件是正常态不是故障 —— ``gate_disabled`` 走
    **info** 级,与 warning(自动降级的异常)分开;启用后不再产 finding。
    扫描面 = 市场插件安装根(--dir)里 manifest 声明 ``gate`` 的件;
    另查 gates.platforms endpoint 命中已知公共实例域(D9 留痕知情 info)。
    """
    gates_file = Path(args.gates_file).expanduser() if args.gates_file else default_gates_path()
    config, gates_error = load_gates_fail_closed(gates_file)
    section: dict[str, Any] = {
        "file": str(gates_file),
        "exists": gates_file.exists(),
        "error": gates_error,
        "gated": [],
        # 批三分析 lane 成员(启用徽标按 lane 成员资格派生,D10-2)
        "analysis_lane": [],
    }
    if gates_error is not None:
        first = (gates_error.get("errors") or [{}])[0]
        _finding(
            findings,
            severity="warning",
            scope="gates",
            code="gates_invalid",
            message=(
                f"gates.yaml 拒载,门槛件已按全关处理(fail-closed):"
                f"{first.get('message', '')};修复后重跑 doctor"
            ),
        )
    # D9 第三方留痕知情:platforms 门槛语义是自有实例,endpoint 指向已知
    # 公共实例(rsshub.app 等)时出 info 提示 —— 坏文件路径 config 已全关
    # (platforms 空),本循环自然空转,无需额外分支。
    for name, gate in sorted(config.platforms.items()):
        public_host = _public_instance_hint(gate.endpoint)
        if public_host is None:
            continue
        _finding(
            findings,
            severity="info",
            scope="gates",
            code="third_party_trace",
            message=(
                f"platforms.{name} endpoint 指向已知公共实例({public_host})——"
                f"第三方留痕知情:采集目标将经公共实例服务器并留痕;"
                f"门槛语义是自有实例,自部署可消除(rsshub 件 README 有指引)"
            ),
        )
    try:
        entries = InstalledPluginStore(args.dir).entries()
    except Exception as exc:  # noqa: BLE001 - 诊断面任何意外降级为 finding,不炸体检
        _finding(
            findings,
            severity="warning",
            scope="gates",
            code="gates_scan_failed",
            message=f"市场插件扫描失败(门槛诊断跳过): {exc}",
        )
        return section
    for entry in entries:
        if entry.manifest is None or not entry.manifest.gate:
            continue
        gate = entry.manifest.gate
        enabled = plugin_gate_open(config, gate, entry.manifest.id)
        section["gated"].append(
            {
                "id": entry.manifest.id,
                "gate": gate,
                "enabled": enabled,
            }
        )
        if not enabled:
            advisory = _GATE_ADVISORIES.get(gate, "")
            _finding(
                findings,
                severity="info",
                scope=f"plugin:{entry.manifest.id}",
                code="gate_disabled",
                message=(
                    f"门槛件 {entry.manifest.id}(gate={gate})未启用 —— 正常态,不是故障;"
                    f"{advisory};知情后 myssia gates set 可开启"
                ),
            )
    # 批三分析 lane 成员(D10-2 最小扩展):未启用 = 正常态 info(与 gate_disabled
    # 同级);按 **lane 成员资格**(analysis_lane 注册表)派生——yake 不声明
    # gate 也要可见;声明 gate 的件(snownlp: stale)已由上一循环出 finding,
    # 不双报(两处查询同一 analysis.<key> 开关,状态必然一致)。
    member_key_of = {package: key for key, package in ANALYSIS_LANE_MEMBERS.items()}
    for entry in entries:
        if entry.manifest is None:
            continue
        member_key = member_key_of.get(entry.manifest.id)
        if member_key is None:
            continue
        enabled = gate_open(config, "analysis", member_key)
        section["analysis_lane"].append(
            {"id": entry.manifest.id, "key": member_key, "enabled": enabled}
        )
        if enabled or entry.manifest.gate:
            continue
        _finding(
            findings,
            severity="info",
            scope=f"plugin:{entry.manifest.id}",
            code="analysis_lane_disabled",
            message=(
                f"分析 lane 件 {entry.manifest.id} 未启用 —— 正常态,不是故障;"
                f"知情后 myssia gates set analysis.{member_key} on 可开启"
                f"(启用后 analyze 阶段对本轮条目做本地装饰,不过滤不拦推送)"
            ),
        )
    return section


# ---------------------------------------------------------------------------
# myssia secret:钥匙链凭据管理(薄包装 myssia.secrets)
# ---------------------------------------------------------------------------


def _read_secret_value(args: argparse.Namespace) -> str:
    """Resolve the secret value: --value > stdin(非 tty)> 安全输入(tty)."""
    if args.value is not None:
        # 安全基线(--value 暴露面):argv 值必然落入 shell history 与
        # 进程列表(ps)。stderr 警告不污染 --json 的 stdout 单文档契约。
        print(
            "警告:凭据值经 --value 命令行参数传入,会落入 shell history 与进程列表(ps);"
            "自动化场景建议改用 stdin 管道:myssia secret set <name> < value.txt",
            file=sys.stderr,
        )
        return args.value
    if not sys.stdin.isatty():
        return sys.stdin.read().rstrip("\r\n")
    return getpass.getpass(f"请输入 {args.name} 的值(输入不回显):")


def _emit_secret_error(exc: SecretError, *, as_json: bool) -> None:
    """结构化 secret 错误(code + 中文原因;值永不入消息)。"""
    _emit_generic_error("secret", str(exc), as_json=as_json, code=exc.code)


def _cmd_secret(args: argparse.Namespace) -> int:
    """``myssia secret set|list|delete``:0 成功 / 1 结构化失败。"""
    as_json = getattr(args, "as_json", False)
    try:
        if args.secret_command == "set":
            value = _read_secret_value(args)
            if not value:
                _emit_generic_error(
                    "secret",
                    "凭据值为空(--value、stdin 或安全输入均未取得内容)",
                    as_json=as_json,
                )
                return EXIT_CONFIG_ERROR
            set_secret(args.name, value)
            payload = {
                "command": "secret",
                "action": "set",
                "name": args.name,
                "stored": True,
            }
        elif args.secret_command == "list":
            names = list_secrets()
            payload = {"command": "secret", "action": "list", "names": names}
        else:
            delete_secret(args.name)
            payload = {
                "command": "secret",
                "action": "delete",
                "name": args.name,
                "deleted": True,
            }
    except SecretError as exc:
        _emit_secret_error(exc, as_json=as_json)
        return EXIT_CONFIG_ERROR
    if as_json:
        _print_json(payload)
        return EXIT_OK
    if args.secret_command == "list":
        print(f"钥匙链凭据 {len(payload['names'])} 个(只有名字,值不可读出):")
        for name in payload["names"]:
            print(f"  {name}")
    elif args.secret_command == "set":
        print(f"已写入系统钥匙链 name={payload['name']}(值不落日志)")
    else:
        print(f"已从系统钥匙链删除 name={payload['name']}")
    return EXIT_OK


# ---------------------------------------------------------------------------
# myssia gates:门槛件知情启用(D4/D7,批二 10-05-plugin-market-batch)
# ---------------------------------------------------------------------------


def _gates_target_parse(target: str) -> tuple[str, str | None]:
    """解析 ``<kind>`` / ``<kind>.<name>`` 目标;非法形态结构化 ValueError。"""
    if "." in target:
        kind, _, name = target.partition(".")
    else:
        kind, name = target, None
    if kind not in GATES_KINDS:
        raise ValueError(
            f"未知门槛 kind {kind!r}(合法:{list(GATES_KINDS)};总开关不带 .name,逐件如 saas.zenrows)"
        )
    if kind in ("paid_engines", "third_party_trace"):
        if name is not None:
            raise ValueError(f"{kind} 是总开关,不带逐件名(收到 {target!r};逐件形态是 saas/platforms/analysis.<name>)")
        return kind, None
    if name is None:
        raise ValueError(f"{kind} 是逐件开关,需要 <kind>.<name> 形态(如 {kind}.zenrows)")
    if not valid_gate_key(name):
        raise ValueError(f"逐件名 {name!r} 应为小写字母/数字/连字符/下划线且字母数字开头(1-64 字符)")
    return kind, name


def _gates_keychain_name(config: GatesConfig, kind: str, name: str) -> str | None:
    """逐件 on 需在位的钥匙串键名;None = 该件不携带凭据(platforms 可无 token)。"""
    if kind == "saas":
        gate = config.saas.get(name)
        ref = gate.api_key_ref if gate is not None else None
        if ref is None:
            # 未显式配置引用:用规范缺省名检查,并在成功开启时物化进配置
            return canonical_saas_key_ref(name).removeprefix("keychain:")
        return ref.removeprefix("keychain:")
    if kind == "platforms":
        gate = config.platforms.get(name)
        if gate is None or gate.token_ref is None:
            return None  # platform 组织性不执法(D6):无 token 声明即无可检键
        return gate.token_ref.removeprefix("keychain:")
    return None  # analysis / 总开关:纯布尔,无凭据


def _gates_check_key(
    keychain_name: str | None, *, as_json: bool
) -> bool:
    """钥匙串键在位检查(缺键/后端不可用 = 结构化拒,fail-closed 不写盘)。"""
    if keychain_name is None:
        return True
    backend = _safe_keychain_backend()
    if backend is None:
        _emit_generic_error(
            "gates",
            f"钥匙链后端不可用,无法确认凭据 {keychain_name} 在位(fail-closed 拒绝开启);"
            "无钥匙串的主机请改在有钥匙串的环境启用门槛件",
            as_json=as_json,
            code="gate_key_unverifiable",
        )
        return False
    try:
        exists = backend.get_password(SECRET_SERVICE, keychain_name) is not None
    except Exception as exc:  # noqa: BLE001 - 钥匙链异常 = 无法核验,不是能开启
        _emit_generic_error(
            "gates",
            f"钥匙链读取失败,无法确认凭据 {keychain_name} 在位({exc})",
            as_json=as_json,
            code="gate_key_unverifiable",
        )
        return False
    if not exists:
        _emit_generic_error(
            "gates",
            f"钥匙链中不存在凭据 {keychain_name};先 myssia secret set {keychain_name} 写入,"
            "再开启本门槛件(付费引擎按页计费,键不在位拒绝开启)",
            as_json=as_json,
            code="gate_key_missing",
        )
        return False
    return True


def _gates_set(args: argparse.Namespace) -> int:
    """``myssia gates set <kind>[.<name>] <on|off>``:同门校验 → 键检查 → 原子落盘。"""
    as_json = args.as_json
    try:
        kind, name = _gates_target_parse(args.target)
    except ValueError as exc:
        _emit_generic_error("gates", str(exc), as_json=as_json, code="invalid_target")
        return EXIT_CONFIG_ERROR
    value = args.value == "on"
    path = Path(args.file).expanduser() if args.file else default_gates_path()
    try:
        config = load_gates_config(path)
    except LoadError as exc:
        _emit_generic_error(
            "gates",
            f"gates 配置拒载,零写入: {exc.errors[0].message if exc.errors else exc}",
            as_json=as_json,
            code="gates_invalid",
            errors=exc.to_dict().get("errors"),
        )
        return EXIT_CONFIG_ERROR
    # 逐件开启先过钥匙串键在位检查(缺键 = 结构化拒,零写入;总开关/关闭不需键)
    if value and name is not None:
        if not _gates_check_key(_gates_keychain_name(config, kind, name), as_json=as_json):
            return EXIT_CONFIG_ERROR
    if kind == "paid_engines":
        config = dataclass_replace(config, paid_engines=value)
    elif kind == "third_party_trace":
        config = dataclass_replace(config, third_party_trace=value)
    elif kind == "saas":
        existing = config.saas.get(name)
        api_key_ref = (
            existing.api_key_ref
            if existing is not None and existing.api_key_ref
            else canonical_saas_key_ref(name)
        )
        config = replace_saas_gate(config, name, SaaSGate(enabled=value, api_key_ref=api_key_ref))
    elif kind == "platforms":
        existing = config.platforms.get(name)
        config = replace_platform_gate(
            config,
            name,
            PlatformGate(
                enabled=value,
                endpoint=existing.endpoint if existing is not None else "",
                token_ref=existing.token_ref if existing is not None else None,
            ),
        )
    else:
        config = replace_analysis_switch(config, name, value)
    save_gates_config(path, config)
    payload = {
        "command": "gates",
        "action": "set",
        "target": args.target,
        "kind": kind,
        "name": name,
        "value": value,
        "path": str(path),
        "config": config.to_payload(),
    }
    if as_json:
        _print_json(payload)
    else:
        state = "开启" if value else "关闭"
        print(f"门槛 {args.target} 已{state}(gates.yaml: {path})")
    return EXIT_OK


def _gates_show(args: argparse.Namespace) -> int:
    """``myssia gates show``:整份门槛配置 + 路径;坏文件结构化拒(不装作全关)。"""
    as_json = args.as_json
    path = Path(args.file).expanduser() if args.file else default_gates_path()
    try:
        config = load_gates_config(path)
    except LoadError as exc:
        _emit_generic_error(
            "gates",
            f"gates 配置拒载: {exc.errors[0].message if exc.errors else exc}",
            as_json=as_json,
            code="gates_invalid",
            errors=exc.to_dict().get("errors"),
        )
        return EXIT_CONFIG_ERROR
    payload = {
        "command": "gates",
        "action": "show",
        "path": str(path),
        "exists": path.exists(),
        "config": config.to_payload(),
    }
    if as_json:
        _print_json(payload)
        return EXIT_OK
    print(f"门槛配置({path},{'已配置' if payload['exists'] else '未配置 = 全关(fail-closed 缺省)'}):")
    print(f"  paid_engines={'开' if config.paid_engines else '关'} third_party_trace={'开' if config.third_party_trace else '关'}")
    for key, gate in sorted(config.saas.items()):
        print(f"  saas.{key}: {'开' if gate.enabled else '关'}(key={gate.api_key_ref or '未配置'})")
    for key, gate in sorted(config.platforms.items()):
        print(f"  platforms.{key}: {'开' if gate.enabled else '关'}(endpoint={gate.endpoint or '未配置'})")
    for key, value in sorted(config.analysis.items()):
        print(f"  analysis.{key}: {'开' if value else '关'}")
    return EXIT_OK


def _cmd_gates(args: argparse.Namespace) -> int:
    """``myssia gates show|set`` 的分发入口(退出码 0/1,照 secret 族)。"""
    _configure_logging(as_json=args.as_json)
    if args.gates_command == "set":
        return _gates_set(args)
    return _gates_show(args)


# ---------------------------------------------------------------------------
# myssia channels:通道目录 refresh / list(v1.2,10-03-messaging-feishu D5)
# ---------------------------------------------------------------------------


class _PrecapturedAdapter:
    """CLI refresh 的合并壳:把已发现条目原样喂给 :meth:`ChannelDirectory.refresh`。

    CLI 需要逐平台把发现错误(如凭据缺失)结构化上报给调用方,而 refresh
    内部只记日志;所以 CLI 先自己调 ``discover_directory`` 捕获错误,成功
    的结果经本壳走 core 的 canonical 合并路径(桶替换 + updated_at 戳 +
    原子持久化),不二次发起网络请求。
    """

    def __init__(self, entries: Sequence[Any]) -> None:
        self._entries = entries

    async def discover_directory(self) -> Sequence[Any]:
        return self._entries


def _channels_data_root(args: argparse.Namespace) -> Path:
    """目录 JSON 数据根:``--db`` 父目录(与 pipeline 目录/死信账本同一收口)。"""
    return Path(args.db).expanduser().resolve().parent


def _print_channels_table(directory: ChannelDirectory) -> None:
    """目录表(人类可读;对 AI 用 --json)。"""
    platforms = directory.platforms()
    if not platforms:
        print("通道目录为空:先 myssia channels refresh <platform> 发现可达对象")
        return
    print(f"通道目录(最近刷新 {directory.updated_at or '未知'}):")
    for platform in platforms:
        entries = directory.entries(platform)
        print(f"  [{platform}] {len(entries)} 个可达对象:")
        for entry in entries:
            thread = f" thread={entry.thread_id}" if entry.thread_id else ""
            print(f"    {entry.name} ({entry.chat_id}) type={entry.type}{thread}")


def _channels_refresh(args: argparse.Namespace) -> int:
    """``myssia channels refresh [platforms...]``:发现 → 合并 → 打印目录。

    退出码:全部成功/无自动发现 0;未知平台/凭据缺失等任一结构化失败 1
    (fail-fast 家族语义;失败平台保留旧目录桶,已成功平台照常合并)。
    无自动发现平台(ntfy/dingtalk/wecom,10-03-messaging-w2-platforms 蓝本
    事实)报结构化说明(payload ``no_discovery``)而非假装刷新出空目录,
    也不是失败——条目靠直达 id / 别名手工登记。
    """
    as_json = args.as_json
    requested = [str(name) for name in args.platforms] or sorted(PLATFORMS)
    unknown = [name for name in requested if name not in PLATFORMS]
    if unknown:
        _emit_generic_error(
            "channels",
            f"未知平台: {unknown}(已注册: {sorted(PLATFORMS)})",
            as_json=as_json,
        )
        return EXIT_CONFIG_ERROR
    if not requested:
        _emit_generic_error(
            "channels",
            "尚无已注册平台(等平台适配子任务接入 PLATFORMS)",
            as_json=as_json,
        )
        return EXIT_CONFIG_ERROR
    data_root = _channels_data_root(args)
    directory = ChannelDirectory(data_root)
    refreshed: dict[str, int] = {}
    failures: list[dict[str, str]] = []
    passive: list[str] = []
    no_discovery: list[dict[str, str]] = []
    shims: dict[str, _PrecapturedAdapter] = {}
    for platform in requested:
        adapter = PLATFORMS[platform]()
        discover = getattr(adapter, "discover_directory", None)
        if not callable(discover):
            # 被动目录平台(10-03-messaging-telegram:Bot API 无「列出会话」
            # 能力):非失败——条目由 feedback 轮询入站观测积累 + 别名手工补录。
            passive.append(platform)
            continue
        try:
            entries = asyncio.run(discover())
        except DirectoryDiscoverUnsupported as exc:
            # 无自动发现平台(10-03-messaging-w2-platforms,蓝本事实):
            # 说明 ≠ 失败,目录桶不动,退出码不受影响。
            no_discovery.append({"platform": platform, "message": str(exc)})
            continue
        except Exception as exc:  # noqa: BLE001 - 单平台失败隔离:告警 + 保留旧桶
            failures.append(
                {"platform": platform, "error": f"{type(exc).__name__}: {exc}"}
            )
            continue
        shims[platform] = _PrecapturedAdapter(entries)
        refreshed[platform] = len(entries)
    if shims:
        asyncio.run(directory.refresh(shims))
    payload = {
        "command": "channels",
        "action": "refresh",
        "data_root": str(data_root),
        "refreshed": refreshed,
        "passive": passive,
        "no_discovery": no_discovery,
        "failed": failures,
        "updated_at": directory.updated_at,
        "platforms": {
            platform: [entry.to_dict() for entry in directory.entries(platform)]
            for platform in directory.platforms()
        },
    }
    if failures:
        # 失败也是单份文档的一部分(顶层 error/message 供 jq 快查,failed 留明细)
        payload["error"] = "channels_refresh_failed"
        payload["message"] = "; ".join(
            f"{failure['platform']}: {failure['error']}" for failure in failures
        )
    if as_json:
        _print_json(payload)
    else:
        for platform, count in sorted(refreshed.items()):
            print(f"已刷新 {platform} 目录:发现 {count} 个可达对象(数据根 {data_root})")
        for platform in passive:
            print(
                f"{platform} 为被动目录平台(无主动发现 API):目录由入站消息自动积累,"
                "别名文件 channel_aliases.json 可手工补录"
            )
        for entry in no_discovery:
            print(f"{entry['platform']}: {entry['message']}")
        for failure in failures:
            print(
                f"刷新失败(保留旧目录): {failure['platform']}: {failure['error']}",
                file=sys.stderr,
            )
        _print_channels_table(directory)
    return EXIT_OK if not failures else EXIT_CONFIG_ERROR


def _channels_list(args: argparse.Namespace) -> int:
    """``myssia channels list``:纯读目录(空目录是合法态,提示先 refresh)。"""
    as_json = args.as_json
    data_root = _channels_data_root(args)
    directory = ChannelDirectory(data_root)
    payload = {
        "command": "channels",
        "action": "list",
        "data_root": str(data_root),
        "updated_at": directory.updated_at,
        "platforms": {
            platform: [entry.to_dict() for entry in directory.entries(platform)]
            for platform in directory.platforms()
        },
    }
    if as_json:
        _print_json(payload)
        return EXIT_OK
    _print_channels_table(directory)
    return EXIT_OK


def _cmd_channels(args: argparse.Namespace) -> int:
    """``myssia channels refresh|list`` 的分发入口(退出码 0/1)。"""
    _configure_logging(as_json=args.as_json)
    if args.channels_command == "refresh":
        return _channels_refresh(args)
    return _channels_list(args)


# ---------------------------------------------------------------------------
# myssia plugin:市场插件装卸(v0.3;薄包装 myssia.plugins,装卸 fail-fast,
# 扫描零异常 —— 插件坏绝不拦核心,铁律)
# ---------------------------------------------------------------------------


def _plugin_list(
    args: argparse.Namespace, store: InstalledPluginStore, *, as_json: bool
) -> int:
    """``myssia plugin list``:已装清单 + findings;信息性命令,完成即 0。

    缺失安装根 = 空清单(未装插件是正常态,不是错误);--probe 显式 opt-in
    remote 端点探测(网络 I/O),探测失败只产 findings,不改退出码。

    批二门槛机制(D4/D5):manifest 声明 ``gate`` 的件独立分组进
    ``payload["gates"]["gated"]``,每件带 ``enabled`` 徽标(状态派生自
    gates.yaml,坏文件 = 全关 + 顶层 ``gates.error`` 结构化警告)。
    """
    entries = store.entries()
    if getattr(args, "probe", False):
        backend = _safe_keychain_backend()
        for entry in entries:
            if entry.manifest is None:
                continue
            entry.findings.extend(
                check_remote_modes(
                    entry.manifest,
                    backend=backend,
                    probe_remote=True,
                    client_factory=_build_async_client,
                )
            )
    gates_file = Path(args.gates_file).expanduser() if args.gates_file else default_gates_path()
    gates_config, gates_error = load_gates_fail_closed(gates_file)
    # 批三分析 lane 成员(D10-2 最小扩展):lane 件启用徽标按 **lane 成员资格**
    # 派生自 gates.analysis.<key> 开关,而非 manifest gate 字段——yake 不声明
    # gate(上游活跃,stale 徽标失实),徽标跟着 gate 走会漏(D5 词表零改动)。
    member_key_of = {package: key for key, package in ANALYSIS_LANE_MEMBERS.items()}
    plugin_payloads: list[dict[str, Any]] = []
    gated: list[dict[str, Any]] = []
    analysis_lane: list[dict[str, Any]] = []
    for entry in entries:
        payload = entry.to_dict()
        gate = payload.get("gate")
        if entry.manifest is not None and gate:
            enabled = plugin_gate_open(gates_config, gate, entry.manifest.id)
            payload["gate_enabled"] = enabled
            gated.append(
                {
                    "id": entry.manifest.id,
                    "gate": gate,
                    # 派生查询键(官方件惯例 = id 去 myssia- 前缀)
                    "key": plugin_gate_key(entry.manifest.id),
                    "enabled": enabled,
                }
            )
        else:
            payload["gate_enabled"] = None
        member_key = member_key_of.get(entry.manifest.id) if entry.manifest is not None else None
        if member_key is None:
            payload["analysis_lane"] = None
        else:
            lane_enabled = gate_open(gates_config, "analysis", member_key)
            payload["analysis_lane"] = {"key": member_key, "enabled": lane_enabled}
            analysis_lane.append(
                {"id": entry.manifest.id, "key": member_key, "enabled": lane_enabled}
            )
        plugin_payloads.append(payload)
    tiers: dict[str, int] = {}
    for entry in entries:
        if entry.manifest is not None:
            tiers[entry.manifest.tier] = tiers.get(entry.manifest.tier, 0) + 1
    payload = {
        "command": "plugin",
        "action": "list",
        "dir": str(store.root),
        "myssia_version": myssia.__version__,
        "plugins": plugin_payloads,
        "gates": {
            "file": str(gates_file),
            "exists": gates_file.exists(),
            # 坏文件 = 全关(fail-closed);错误结构化带回,不是静默吞掉
            "error": gates_error,
            "gated": gated,
            # 批三分析 lane 成员清单(启用徽标派生自 analysis.<key>,D10-2)
            "analysis_lane": analysis_lane,
        },
        "summary": {
            "installed": sum(1 for entry in entries if entry.manifest is not None),
            "usable": sum(
                1
                for entry in entries
                if entry.manifest is not None
                and entry.compatible_current
                and not any(finding.severity == "error" for finding in entry.findings)
            ),
            # v1.1 分级计数(desktop/remote/server-only,见 plugins.manifest)。
            "tiers": dict(sorted(tiers.items())),
            # 批二门槛件计数(已启用/未启用;未启用是正常态,doctor 走 info)
            "gated_total": len(gated),
            "gated_enabled": sum(1 for item in gated if item["enabled"]),
            "errors": sum(
                1
                for entry in entries
                for finding in entry.findings
                if finding.severity == "error"
            ),
            "warnings": sum(
                1
                for entry in entries
                for finding in entry.findings
                if finding.severity == "warning"
            ),
        },
    }
    if as_json:
        _print_json(payload)
    else:
        _print_human_plugin_list(payload)
    return EXIT_OK


def _print_human_plugin_list(payload: dict[str, Any]) -> None:
    """人类可读的已装插件清单(与 --json 同一信息)。"""
    summary = payload["summary"]
    print(
        f"世事 plugin list:{payload['dir']}(myssia {payload['myssia_version']})"
        f"共 {len(payload['plugins'])} 个,可用 {summary['usable']} 个"
    )
    tiers = summary.get("tiers") or {}
    if tiers:
        tier_text = ", ".join(f"{tier}={count}" for tier, count in tiers.items())
        print(f"  分级:{tier_text}")
    gates = payload.get("gates") or {}
    if gates.get("error"):
        # fail-closed:坏文件 = 全关,但必须可见(不是静默吞掉)
        first = (gates["error"].get("errors") or [{}])[0]
        print(f"  门槛配置拒载(已按全关处理):{first.get('message', gates['error'])}")
    gated = gates.get("gated") or []
    if gated:
        lines = ", ".join(
            f"{item['id']}[{item['gate']}]{'已启用' if item['enabled'] else '未启用'}"
            for item in gated
        )
        print(f"  门槛件({len(gated)}):{lines}")
    analysis_lane = gates.get("analysis_lane") or []
    if analysis_lane:
        lines = ", ".join(
            f"{item['id']}(analysis.{item['key']}){'已启用' if item['enabled'] else '未启用'}"
            for item in analysis_lane
        )
        print(f"  分析 lane 件({len(analysis_lane)}):{lines}")
    for plugin in payload["plugins"]:
        if not plugin["loaded"]:
            print(f"  {plugin['path']} — manifest 缺失或损坏")
        else:
            compatibility = (
                "兼容"
                if plugin["compatible_current"]
                else f"不兼容(要求 myssia {plugin['compatible']})"
            )
            gate_badge = (
                f"{{{plugin['gate']}:{'开' if plugin['gate_enabled'] else '未启用'}}}"
                if plugin.get("gate")
                else ""
            )
            lane = plugin.get("analysis_lane")
            lane_badge = (
                f"{{lane:analysis.{lane['key']}:{'开' if lane['enabled'] else '未启用'}}}"
                if lane
                else ""
            )
            print(
                f"  {plugin['id']}@{plugin['version']}[{plugin['tier']}]({plugin['name']}){compatibility}{gate_badge}{lane_badge}"
                f" requires={plugin['requires']} provides={plugin['provides']}"
            )
        for finding in plugin["findings"]:
            print(
                f"    [{finding['severity']}] {finding['code']}: {finding['message']}"
            )
    print(f"findings: {summary['errors']} 错误 / {summary['warnings']} 警告")


def _plugin_install(
    args: argparse.Namespace, store: InstalledPluginStore, *, as_json: bool
) -> int:
    """``myssia plugin install <source>``:fail-fast 校验后整目录拷贝;0/1。"""
    try:
        result = store.install(Path(args.source), force=args.force)
    except PluginStoreError as exc:
        extra: dict[str, Any] = {"code": exc.code}
        if exc.errors:
            extra["errors"] = exc.errors
        _emit_generic_error("plugin", str(exc), as_json=as_json, **extra)
        return EXIT_CONFIG_ERROR
    if as_json:
        _print_json({"command": "plugin", "action": "install", **result})
        return EXIT_OK
    notes = []
    if result["forced"]:
        notes.append("--force 覆盖安装")
    if not result["compatible_current"]:
        notes.append(f"警告:版本不兼容(要求 myssia {result['compatible']})")
    suffix = f"({';'.join(notes)})" if notes else ""
    print(f"已安装 {result['id']}@{result['version']} → {result['path']}{suffix}")
    return EXIT_OK


def _plugin_remove(
    args: argparse.Namespace, store: InstalledPluginStore, *, as_json: bool
) -> int:
    """``myssia plugin remove <id>``:按 id 移除;0 / 1(未装/id 非法)。"""
    try:
        result = store.remove(args.id)
    except PluginStoreError as exc:
        _emit_generic_error("plugin", str(exc), as_json=as_json, code=exc.code)
        return EXIT_CONFIG_ERROR
    if as_json:
        _print_json({"command": "plugin", "action": "remove", **result})
    else:
        print(f"已移除 {result['id']}({result['path']})")
    return EXIT_OK


def _cmd_plugin(args: argparse.Namespace) -> int:
    """``myssia plugin list|install|remove`` 的分发入口(退出码 0/1)。"""
    as_json = args.as_json
    _configure_logging(as_json=as_json)
    store = InstalledPluginStore(args.dir)
    if args.plugin_command == "list":
        return _plugin_list(args, store, as_json=as_json)
    if args.plugin_command == "install":
        return _plugin_install(args, store, as_json=as_json)
    return _plugin_remove(args, store, as_json=as_json)


# ---------------------------------------------------------------------------
# myssia feedback:反馈闭环(v0.3;CLI 是桌面形态的手动标记接收路)
# ---------------------------------------------------------------------------


def _feedback_row_dict(record: FeedbackRecord) -> dict[str, Any]:
    """Machine-readable feedback row (--json / AI 消费形态)."""
    return {
        "id": record.id,
        "item_id": record.item_id,
        "dedup_key": record.dedup_key,
        "verdict": record.verdict,
        "channel": record.channel,
        "title": record.title,
        "category": record.category,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }


def _feedback_mark(args: argparse.Namespace, *, as_json: bool) -> int:
    """``myssia feedback mark <条目> <good|bad>``:入库并回执;0/1。"""
    try:
        store = SQLiteStore(args.db)
    except StoreSchemaError as exc:
        _emit_generic_error(
            "store", str(exc), as_json=as_json, error_type=exc.code, **exc.details
        )
        return EXIT_CONFIG_ERROR
    try:
        item = resolve_item_ref(store, args.item)
        if item is None:
            _emit_generic_error(
                "item_not_found",
                f"条目不存在: {args.item!r}(可传 items.id 或 dedup_key/URL);"
                "先用 myssia list 或查询 items 表确认",
                as_json=as_json,
            )
            return EXIT_CONFIG_ERROR
        try:
            record = record_feedback(
                store, verdict=args.verdict, channel=FEEDBACK_CHANNEL_CLI, item=item
            )
        except ValueError as exc:
            _emit_generic_error("feedback", str(exc), as_json=as_json)
            return EXIT_CONFIG_ERROR
    finally:
        store.close()
    payload = {
        "command": "feedback",
        "action": "mark",
        "feedback_id": record.id,
        "item_id": record.item_id,
        "dedup_key": record.dedup_key,
        "verdict": record.verdict,
        "channel": record.channel,
    }
    if as_json:
        _print_json(payload)
    else:
        print(
            f"已记录反馈 verdict={record.verdict} item_id={record.item_id} "
            f"dedup_key={record.dedup_key}(feedback_id={record.id});"
            "负反馈将在下轮维护阶段参与调参(负反馈 Top 类目/词降权)"
        )
    return EXIT_OK


def _feedback_list(args: argparse.Namespace, *, as_json: bool) -> int:
    """``myssia feedback list``:反馈记录(新→旧);0/1。"""
    try:
        store = SQLiteStore(args.db)
    except StoreSchemaError as exc:
        _emit_generic_error(
            "store", str(exc), as_json=as_json, error_type=exc.code, **exc.details
        )
        return EXIT_CONFIG_ERROR
    try:
        rows = store.list_feedback(
            verdict=args.verdict, channel=args.channel, limit=args.limit
        )
    except ValueError as exc:  # --limit 负数等参数校验失败
        _emit_generic_error("feedback", str(exc), as_json=as_json)
        return EXIT_CONFIG_ERROR
    finally:
        store.close()
    payload = {
        "command": "feedback",
        "action": "list",
        "count": len(rows),
        "items": [_feedback_row_dict(row) for row in rows],
    }
    if as_json:
        _print_json(payload)
        return EXIT_OK
    print(f"世事 feedback list:共 {len(rows)} 条(新→旧)")
    for row in rows:
        title = f" {row.title}" if row.title else ""
        print(
            f"  #{row.id} [{row.verdict}] {row.channel} item={row.item_id or '-'} "
            f"dedup_key={row.dedup_key}{title}"
        )
    return EXIT_OK


def _feedback_stats(args: argparse.Namespace, *, as_json: bool) -> int:
    """``myssia feedback stats``:窗口统计 + 生效调参 + 可追溯历史;0/1。"""
    try:
        policy = TuningPolicy(window_days=args.window_days, top_n=args.top)
    except ValueError as exc:
        _emit_generic_error("feedback", str(exc), as_json=as_json)
        return EXIT_CONFIG_ERROR
    try:
        store = SQLiteStore(args.db)
    except StoreSchemaError as exc:
        _emit_generic_error(
            "store", str(exc), as_json=as_json, error_type=exc.code, **exc.details
        )
        return EXIT_CONFIG_ERROR
    try:
        tuner = FeedbackTuner(policy)
        stats = tuner.stats(store)
        active = load_active_tuning(store)
        history = [
            {
                "id": row.id,
                "kind": row.kind,
                "payload": dict(row.payload),
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in store.list_tuning(limit=10)
        ]
    except ValueError as exc:
        _emit_generic_error("feedback", str(exc), as_json=as_json)
        return EXIT_CONFIG_ERROR
    finally:
        store.close()
    payload = {
        "command": "feedback",
        "action": "stats",
        "window_days": policy.window_days,
        "stats": stats.to_dict(),
        "active_tuning": active.to_dict(),
        "tuning_history": history,
    }
    if as_json:
        _print_json(payload)
        return EXIT_OK
    print(
        f"世事 feedback stats(窗口 {policy.window_days} 天):"
        f"总 {stats.total} / 好 {stats.good} / 坏 {stats.bad}"
    )
    print(
        "  渠道分布: "
        + (
            ", ".join(
                f"{name}={count}" for name, count in sorted(stats.by_channel.items())
            )
            or "无"
        )
    )
    print(
        "  负反馈 Top 类目: "
        + (
            ", ".join(f"{key}×{count}" for key, count in stats.top_bad_categories)
            or "无"
        )
    )
    print(
        "  负反馈 Top 词条: "
        + (", ".join(f"{key}×{count}" for key, count in stats.top_bad_words) or "无")
    )
    mutes = ", ".join(
        f"{word}={weight}" for word, weight in sorted(active.mute_weights.items())
    )
    penalties = ", ".join(
        f"{cat}={weight}" for cat, weight in sorted(active.category_penalties.items())
    )
    print(f"  活跃词降权: {mutes or '无'}")
    print(f"  活跃类目降权: {penalties or '无'}")
    print("  (enrich 启用时应用于评分与路由;enrich 关闭时仅入库、不生效)")
    for note in active.prompt_notes[:1]:
        print(f"  评分要点: {note}")
    print(f"  调参历史: 最近 {len(history)} 条(全量在 feedback_tuning 表,可追溯)")
    return EXIT_OK


def _cmd_feedback(args: argparse.Namespace) -> int:
    """``myssia feedback list|stats|mark`` 的分发入口(退出码 0/1)。"""
    as_json = args.as_json
    _configure_logging(as_json=as_json)
    if args.feedback_command == "mark":
        return _feedback_mark(args, as_json=as_json)
    if args.feedback_command == "list":
        return _feedback_list(args, as_json=as_json)
    return _feedback_stats(args, as_json=as_json)


# ---------------------------------------------------------------------------
# myssia alerts:告警命中历史只读(v1;design §8,CLI 写路径留 v2)
# ---------------------------------------------------------------------------


def _alert_fired_row_dict(fired: AlertFired) -> dict[str, Any]:
    """Machine-readable fired row(--json / AI 消费形态;rule_name/title 为
    命中时快照,规则删除/条目剪枝后历史仍可读)。"""
    return {
        "id": fired.id,
        "rule_id": fired.rule_id,
        "rule_name": fired.rule_name,
        "item_id": fired.item_id,
        "dedup_key": fired.dedup_key,
        "title": fired.title,
        "category": fired.category,
        "action": fired.action,
        "action_status": fired.action_status,
        "created_at": fired.created_at.isoformat() if fired.created_at else None,
    }


def _alerts_list(args: argparse.Namespace, *, as_json: bool) -> int:
    """``myssia alerts list``:告警命中历史(新→旧);0/1。"""
    try:
        store = SQLiteStore(args.db)
    except StoreSchemaError as exc:
        _emit_generic_error(
            "store", str(exc), as_json=as_json, error_type=exc.code, **exc.details
        )
        return EXIT_CONFIG_ERROR
    try:
        rows = store.list_fired(rule_id=args.rule, limit=args.limit)
    finally:
        store.close()
    payload = {
        "command": "alerts",
        "action": "list",
        "count": len(rows),
        "items": [_alert_fired_row_dict(row) for row in rows],
    }
    if as_json:
        _print_json(payload)
        return EXIT_OK
    print(f"世事 alerts list:共 {len(rows)} 条命中(新→旧)")
    for row in rows:
        when = row.created_at.isoformat(sep=" ") if row.created_at else "-"
        print(
            f"  #{row.id} {when} [{row.action}:{row.action_status}] "
            f"{row.rule_name} — {row.title or '(无标题)'}"
        )
    return EXIT_OK


def _cmd_alerts(args: argparse.Namespace) -> int:
    """``myssia alerts`` 分发入口(v1 只读 ``list``;写路径留 v2,design §8)。"""
    _configure_logging(as_json=args.as_json)
    return _alerts_list(args, as_json=args.as_json)


# ---------------------------------------------------------------------------
# myssia skill:Agent Skill 安装通路(PRD 10-02-v11;纯文件操作,退出码 0/1)
# ---------------------------------------------------------------------------


def skill_source() -> Path | None:
    """Locate the canonical ``skill/SKILL.md``(装进 agent 目录的就是这份).

    探测顺序:环境变量 ``MYIA_SKILL_SOURCE``(显式逃生口——设了但文件不存在
    直接返回 None,绝不静默回退装上另一份文件)→ 仓库源码布局(src/myssia/
    cli.py 上三级 = 仓库根)→ 当前工作目录下的 skill/。找不到返回 None
    (调用方结构化上报,绝不猜路径装错文件)。
    """
    env_source = os.environ.get(SKILL_SOURCE_ENV)
    if env_source:  # 显式指定只认它自己:存在即用,不存在即失败
        candidate = Path(env_source)
        return candidate if candidate.is_file() else None
    # src/myssia/cli.py → parents: [0]=src/myssia [1]=src [2]=仓库根
    for candidate in (
        Path(__file__).resolve().parents[2] / "skill" / "SKILL.md",
        Path.cwd() / "skill" / "SKILL.md",
    ):
        if candidate.is_file():
            return candidate
    return None


def _skill_target_dir(agent: str) -> Path:
    """One agent's install directory(技能根展开 home 后拼技能目录名)."""
    return Path(SKILL_AGENT_DIRS[agent]).expanduser() / SKILL_DIR_NAME


def _skill_install_target(args: argparse.Namespace) -> tuple[Path, str | None]:
    """Resolve the install directory:--path 显式优先,否则 --agent(或探测)."""
    if args.target_dir:
        return Path(args.target_dir).expanduser(), args.agent
    agent = args.agent
    if agent is None:  # 缺省:挑第一个「技能根已存在」的 agent(本机在用的)
        agent = next(
            (
                name
                for name in sorted(SKILL_AGENT_DIRS)
                if Path(SKILL_AGENT_DIRS[name]).expanduser().is_dir()
            ),
            "claude",
        )
    return _skill_target_dir(agent), agent


def _skill_agent_entries() -> list[dict[str, Any]]:
    """Per-agent path report rows(path/install 共用;只读不写)."""
    source = skill_source()
    source_bytes = source.read_bytes() if source is not None else None
    rows: list[dict[str, Any]] = []
    for agent in sorted(SKILL_AGENT_DIRS):
        target_dir = _skill_target_dir(agent)
        skill_file = target_dir / "SKILL.md"
        installed = skill_file.is_file()
        if not installed:
            matches = False
        elif skill_file.is_symlink():
            matches = skill_file.resolve() == (source.resolve() if source else None)
        else:
            # 副本模式:比对内容,源更新后旧副本如实报不一致(agent 据此 --force 重装)
            try:
                matches = skill_file.read_bytes() == source_bytes
            except OSError:
                matches = False
        rows.append(
            {
                "agent": agent,
                "install_dir": str(target_dir),
                "skill_file": str(skill_file),
                "installed": installed,
                "is_link": installed and skill_file.is_symlink(),
                "matches_source": matches,
            }
        )
    return rows


def _skill_path_payload() -> dict[str, Any]:
    """``myssia skill path`` report(信息性:完成即 0,源缺失如实 found=false)."""
    source = skill_source()
    return {
        "command": "skill",
        "action": "path",
        "source": {
            "path": str(source) if source else None,
            "found": source is not None,
        },
        "agents": _skill_agent_entries(),
        "hint": (
            "myssia skill install [--agent claude|cursor|zcode|agents] [--path DIR] [--link] [--force]"
        ),
    }


class SkillInstallError(Exception):
    """skill 安装的结构化失败(code + 中文消息,退出码 1)."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _skill_install_one(
    source: Path, target_dir: Path, *, link: bool, force: bool
) -> dict[str, Any]:
    """Install SKILL.md into one directory(copy or symlink);refuse unless --force.

    拒绝判据是**目标 SKILL.md 已存在**(与 path 报告的 installed 同一判据);
    目录已存在但缺 SKILL.md 视为未完成安装,允许补装。返回结果字典,失败抛
    :class:`SkillInstallError`(code 结构化上抛)。
    """
    target_file = target_dir / "SKILL.md"
    if target_file.is_dir():
        raise SkillInstallError(
            "target_is_directory", f"目标是目录不是文件: {target_file}"
        )
    if target_file.exists() and not force:
        raise SkillInstallError(
            "target_exists",
            f"目标已存在: {target_file}(--force 覆盖,或 --path 换目录)",
        )
    try:
        if link:
            target_dir.mkdir(parents=True, exist_ok=True)
            if target_file.exists() or target_file.is_symlink():
                target_file.unlink()
            os.symlink(str(source.resolve()), target_file)
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            if target_file.exists() or target_file.is_symlink():
                # 先摘除旧目标(含悬空链接)再写:copy2 沿符号链接写入会把
                # 链接指向的文件(可能在安装目录之外)整体写穿。与 --link
                # 分支同一判据,授权范围是 <技能根>/myia/SKILL.md 这一路径。
                target_file.unlink()
            shutil.copy2(source, target_file)
    except OSError as exc:
        raise SkillInstallError(
            "symlink_failed" if link else "copy_failed",
            f"写入 {target_file} 失败: {exc}",
        ) from exc
    return {
        "target": str(target_file),
        "mode": "link" if link else "copy",
        "overwritten": None,  # 由调用方按安装前的存在性回填
    }


def _skill_install_payload(
    args: argparse.Namespace, *, as_json: bool
) -> tuple[dict[str, Any], int]:
    """Run one install and build its report(退出码与报告一起返回)."""
    source = skill_source()
    if source is None:
        env_source = os.environ.get(SKILL_SOURCE_ENV)
        if env_source:
            hint = f"{SKILL_SOURCE_ENV}={env_source} 指向的文件不存在"
        else:
            hint = (
                f"源码仓库内运行,或设 {SKILL_SOURCE_ENV} 指向 SKILL.md;"
                f"探测过 {Path(__file__).resolve().parents[2] / 'skill' / 'SKILL.md'}"
            )
        _emit_generic_error(
            "skill_source",
            f"找不到 skill/SKILL.md 源({hint})",
            as_json=as_json,
            code="skill_source_not_found",
        )
        return {}, EXIT_CONFIG_ERROR
    target_dir, agent = _skill_install_target(args)
    existed_before = (target_dir / "SKILL.md").exists()
    try:
        result = _skill_install_one(
            source, target_dir, link=args.link, force=args.force
        )
    except SkillInstallError as exc:
        _emit_generic_error("skill_install", str(exc), as_json=as_json, code=exc.code)
        return {}, EXIT_CONFIG_ERROR
    payload = {
        "command": "skill",
        "action": "install",
        "agent": agent,
        "source": str(source),
        "target_dir": str(target_dir),
        "target": result["target"],
        "mode": result["mode"],
        "forced": bool(args.force),
        "overwritten": existed_before,
    }
    return payload, EXIT_OK


def _print_human_skill_path(payload: dict[str, Any]) -> None:
    """人类可读的 path 报告(与 --json 同一信息)."""
    source = payload["source"]
    state = (
        str(source["path"])
        if source["found"]
        else "未找到(源码仓库内运行或设 MYIA_SKILL_SOURCE)"
    )
    print(f"世事 skill path:源 {state}")
    for agent in payload["agents"]:
        mark = "已装" if agent["installed"] else "未装"
        if agent["installed"]:
            mark += "(链接)" if agent["is_link"] else "(副本)"
        print(f"  {agent['agent']}: {agent['skill_file']} [{mark}]")


def _cmd_skill(args: argparse.Namespace) -> int:
    """``myssia skill install|path``:纯文件操作,退出码只有 0/1。"""
    as_json = args.as_json
    _configure_logging(as_json=as_json)
    if args.skill_command == "path":
        payload = _skill_path_payload()
        if as_json:
            _print_json(payload)
        else:
            _print_human_skill_path(payload)
        return EXIT_OK
    payload, exit_code = _skill_install_payload(args, as_json=as_json)
    if exit_code != EXIT_OK:
        return exit_code
    if as_json:
        _print_json(payload)
    else:
        note = f"({'--force 覆盖' if payload['overwritten'] else '新装'},{payload['mode']})"
        print(f"已安装 myssia 技能 {note} → {payload['target']}")
        print(f"源:{payload['source']}")
    return EXIT_OK


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def _not_implemented(command: str) -> int:
    """子命令留位的结构化提示(退出码 1,机器可读)。"""
    print(
        json.dumps(
            {
                "error": "not_implemented",
                "command": command,
                "message": f"{command} 子命令规划于后续版本实现,当前未实装",
                "scheduled_version": "v0.2",
            },
            ensure_ascii=False,
        )
    )
    return EXIT_CONFIG_ERROR


# ---------------------------------------------------------------------------
# myssia osint(v1.1 源码型插件样板:适配器在插件目录,动态加载,零静态耦合)
# ---------------------------------------------------------------------------


def _import_plugin_adapter(plugins_dir: str | Path, plugin_id: str) -> Any:
    """动态加载 ``<plugins_dir>/<plugin_id>/adapter.py``(插件目录非包,单文件加载).

    刻意不做静态 import:核心 wheel 不含 plugins/,静态耦合会让核心反过来
    依赖插件侧文件 —— 恰是铁律要防的反向。加载用 compile + exec(模块命名
    空间),**不走 importlib 的 SourceFileLoader**:后者会在插件目录写
    ``__pycache__`` 字节码垃圾,污染插件包形状(仓库即公开)。
    加载失败抛 OSError/SyntaxError,由调用命令结构化降级(退 1)。
    """
    adapter_file = Path(plugins_dir) / plugin_id / "adapter.py"
    if not adapter_file.is_file():
        raise FileNotFoundError(
            f"适配器不存在:{adapter_file}(样板应随仓库 plugins/ 分发)"
        )
    module = types.ModuleType(f"myssia_{plugin_id.replace('-', '_')}_adapter")
    module.__file__ = str(adapter_file)
    source = adapter_file.read_text(encoding="utf-8")
    executable = compile(source, str(adapter_file), "exec")
    exec(executable, module.__dict__)  # noqa: S102 - 适配器是仓库内受控代码,非任意用户输入
    return module


def _import_osint_adapter(plugins_dir: str | Path) -> Any:
    """``myssia osint`` 的适配器加载(:func:`_import_plugin_adapter` 的样板别名)."""
    return _import_plugin_adapter(plugins_dir, OSINT_PLUGIN_ID)


def _print_osint_human(payload: dict[str, Any]) -> None:
    """人类可读摘要(与 --json 同一信息,另一种皮)."""
    vendor = payload.get("vendor") or {}
    print(
        f"世事 osint:{payload.get('target')}({payload.get('plugin')}) 状态:{payload.get('status')}"
    )
    if vendor.get("commit"):
        print(f"  vendor pin:{vendor['commit']}")
    results = payload.get("results") or {}
    for name in sorted(results):
        values = results[name]
        count = len(values) if isinstance(values, list) else (1 if values else 0)
        if count:
            print(f"  {name}:{count} 条")
    datasets = ",".join(payload.get("datasets") or []) or "无"
    print(f"  耗时:{payload.get('duration_seconds')}s;数据集:{datasets}")


def _cmd_osint(args: argparse.Namespace) -> int:
    """``myssia osint``:跑一次上游 Photon 侦察,结构化输出.

    退出码:0 成功;1 适配器缺失/vendor 未初始化/目标非法(配置或环境错误);
    2 采集失败(Photon 非零退出/超时/导出缺失或损坏)。失败码到退出码的
    映射用 :data:`OSINT_FETCH_FAILURE_CODES`(CLI 所有,不依赖插件侧导出)。
    任何失败都只影响本命令,核心品类流水线照常(铁律)。
    """
    try:
        adapter = _import_osint_adapter(args.plugins_dir)
    except (OSError, ImportError, SyntaxError) as exc:
        _emit_generic_error(
            "osint_adapter_missing",
            str(exc),
            as_json=args.as_json,
            plugins_dir=str(args.plugins_dir),
        )
        return EXIT_CONFIG_ERROR
    try:
        payload = adapter.run(args.target, timeout=args.timeout)
    except Exception as exc:  # noqa: BLE001 — 适配器一切失败都结构化降级,绝不拦核心
        details = (
            exc.to_dict()
            if hasattr(exc, "to_dict")
            else {"code": "osint_failed", "message": str(exc)}
        )
        code = str(details.get("code", "osint_failed"))
        exit_code = (
            EXIT_FETCH_ALL_FAILED
            if code in OSINT_FETCH_FAILURE_CODES
            else EXIT_CONFIG_ERROR
        )
        extra = {
            key: value
            for key, value in details.items()
            if key not in ("code", "message")
        }
        _emit_generic_error(
            code, str(details.get("message", exc)), as_json=args.as_json, **extra
        )
        return exit_code
    if args.as_json:
        _print_json(payload)
    else:
        _print_osint_human(payload)
    return EXIT_OK


def _print_proxy_human(payload: dict[str, Any]) -> None:
    """人类可读摘要(与 --json 同一信息,另一种皮)."""
    print(
        f"MYIA proxy:{payload.get('status')}(候选 {payload.get('fetched')},"
        f"测活 {payload.get('checked')},可用 {len(payload.get('alive') or [])})"
    )
    for source in payload.get("sources") or []:
        state = (
            f"{source.get('proxies')} 条"
            if not source.get("error")
            else f"失败({source.get('error')})"
        )
        print(f"  源:{source.get('url')} → {state}")
    for item in payload.get("alive") or []:
        print(f"  可用:{item.get('proxy')}(延迟 {item.get('latency_ms')}ms)")
    print(f"  耗时:{payload.get('duration_seconds')}s")


def _cmd_proxy(args: argparse.Namespace) -> int:
    """``myssia proxy``:进程内轻量代理抓取+测活(myssia-proxy 插件,零 Redis 零 docker).

    退出码:0 成功(拿到 ≥1 个可用代理);1 适配器缺失/用法错误(count/timeout
    非法);2 采集失败(全部源抓取失败 ``fetch_failed`` / 测活零可用
    ``no_alive_proxy``)。失败码到退出码的映射用 :data:`PROXY_FETCH_FAILURE_CODES`
    (CLI 所有,不依赖插件侧导出)。任何失败都只影响本命令,核心品类流水线
    照常(铁律)。
    """
    try:
        adapter = _import_plugin_adapter(args.plugins_dir, PROXY_PLUGIN_ID)
    except (OSError, ImportError, SyntaxError) as exc:
        _emit_generic_error(
            "proxy_adapter_missing",
            str(exc),
            as_json=args.as_json,
            plugins_dir=str(args.plugins_dir),
        )
        return EXIT_CONFIG_ERROR
    try:
        payload = adapter.run(count=args.count, check_timeout=args.timeout)
    except Exception as exc:  # noqa: BLE001 — 适配器一切失败都结构化降级,绝不拦核心
        details = (
            exc.to_dict()
            if hasattr(exc, "to_dict")
            else {"code": "proxy_failed", "message": str(exc)}
        )
        code = str(details.get("code", "proxy_failed"))
        exit_code = (
            EXIT_FETCH_ALL_FAILED
            if code in PROXY_FETCH_FAILURE_CODES
            else EXIT_CONFIG_ERROR
        )
        extra = {
            key: value
            for key, value in details.items()
            if key not in ("code", "message")
        }
        _emit_generic_error(
            code, str(details.get("message", exc)), as_json=args.as_json, **extra
        )
        return exit_code
    if args.as_json:
        _print_json(payload)
    else:
        _print_proxy_human(payload)
    return EXIT_OK


def _add_proxy_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia proxy``:进程内轻量代理抓取+测活(v1.1 desktop 分级 myssia-proxy)."""
    proxy = sub.add_parser(
        "proxy",
        help="轻量代理抓取+测活(myssia-proxy 插件,进程内、零 Redis 零 docker;失败绝不拦核心)",
        description=(
            "桌面路径(默认):定位 <plugins-dir>/myssia-proxy(适配器 adapter.py),"
            "进程内抓取公开免费代理列表并逐个测活(经代理请求校验目标),输出结构化"
            "结果。零 Redis 零 docker;完整 proxy_pool 服务形态(定时抓取+池化+API)"
            "见 docker/plugins/ 下的可选服务端部署。全部源抓取失败或测活零可用 → "
            "结构化错误退 2;适配器缺失/用法错误退 1;任何失败都不影响核心品类"
            "流水线(铁律)。"
        ),
    )
    proxy.add_argument(
        "--count",
        type=int,
        default=DEFAULT_PROXY_COUNT,
        help=f"期望拿到的可用代理数(默认 {DEFAULT_PROXY_COUNT};测活凑够即止)",
    )
    proxy.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_PROXY_CHECK_TIMEOUT_SECONDS,
        help=f"单代理测活超时秒数(默认 {DEFAULT_PROXY_CHECK_TIMEOUT_SECONDS:g})",
    )
    proxy.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR},样板位于 myssia-proxy/ 子目录)",
    )
    proxy.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


# ---------------------------------------------------------------------------
# myssia media(myssia-media 插件;10-05-plugin-market-batch 首批:
# yt-dlp 公域上游经 uv 临时环境隔离子进程,扁平快扫视频/频道/播放列表。
# 退出码族:0 成功 / 1 配置或环境错误(适配器缺失/uv 缺失/目标非法)/
# 2 采集失败(上游非零退出/超时/输出损坏);--json 下 stdout 恒单份 JSON)
# ---------------------------------------------------------------------------


def _print_media_human(payload: dict[str, Any]) -> None:
    """人类可读摘要(与 --json 同一信息,另一种皮)."""
    meta = payload.get("meta") or {}
    head = meta.get("title") or payload.get("target") or ""
    channel = meta.get("channel") or meta.get("uploader") or ""
    if channel:
        head = f"{head}({channel})"
    print(
        f"世事 media:{head} 条目:{payload.get('entry_count')}/"
        f"{payload.get('entry_total')}(插件 {payload.get('plugin')})"
    )
    for entry in (payload.get("entries") or [])[:10]:
        duration = entry.get("duration")
        suffix = f"[{int(duration) // 60}:{int(duration) % 60:02d}]" if duration else ""
        views = entry.get("view_count")
        if views is not None:
            suffix += f"[{views} 次]"
        print(f"  {entry.get('title') or entry.get('id')}{suffix}")
    more = (payload.get("entry_count") or 0) - 10
    if more > 0:
        print(f"  …另有 {more} 条(--json 看全量)")
    print(f"  耗时:{payload.get('duration_seconds')}s")


def _cmd_media(args: argparse.Namespace) -> int:
    """``myssia media``:跑一次 yt-dlp 扁平快扫,结构化输出.

    退出码:0 成功(含零条目的合法空态);1 适配器缺失/uv 缺失/目标非法
    (配置或环境错误);2 采集失败(上游非零退出/超时/输出损坏)。失败码到
    退出码的映射用 :data:`MEDIA_FETCH_FAILURE_CODES`(CLI 所有,不依赖插件
    侧导出)。任何失败都只影响本命令,核心品类流水线照常(铁律)。
    """
    try:
        adapter = _import_plugin_adapter(args.plugins_dir, MEDIA_PLUGIN_ID)
    except (OSError, ImportError, SyntaxError) as exc:
        _emit_generic_error(
            "media_adapter_missing",
            str(exc),
            as_json=args.as_json,
            plugins_dir=str(args.plugins_dir),
        )
        return EXIT_CONFIG_ERROR
    try:
        payload = adapter.run(
            args.url,
            timeout=args.timeout,
            max_items=args.max_items,
        )
    except Exception as exc:  # noqa: BLE001 — 适配器一切失败都结构化降级,绝不拦核心
        details = (
            exc.to_dict()
            if hasattr(exc, "to_dict")
            else {"code": "media_failed", "message": str(exc)}
        )
        code = str(details.get("code", "media_failed"))
        exit_code = (
            EXIT_FETCH_ALL_FAILED
            if code in MEDIA_FETCH_FAILURE_CODES
            else EXIT_CONFIG_ERROR
        )
        extra = {
            key: value
            for key, value in details.items()
            if key not in ("code", "message")
        }
        _emit_generic_error(
            code, str(details.get("message", exc)), as_json=args.as_json, **extra
        )
        return exit_code
    if args.as_json:
        _print_json(payload)
    else:
        _print_media_human(payload)
    return EXIT_OK


def _add_media_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia media``:视频/频道扁平快扫(10-05-plugin-market-batch myssia-media)."""
    media = sub.add_parser(
        "media",
        help="视频/频道扁平快扫(myssia-media 插件,yt-dlp 隔离子进程;失败绝不拦核心)",
        description=(
            "定位 <plugins-dir>/myssia-media(适配器 adapter.py),以 uv 临时环境"
            "(--no-project --with yt-dlp,不进根依赖)隔离子进程跑上游 CLI 的"
            "--dump-single-json --flat-playlist 扁平快扫:单视频出元数据,频道/"
            "播放列表出条目清单(不逐条解析媒体流)。目标须 http(s) URL;采集"
            "边界由使用者自负(站点条款与当地法律)。适配器缺失/目标非法退 1;"
            "采集失败退 2;任何失败不影响核心品类流水线(铁律)。"
        ),
    )
    media.add_argument(
        "url",
        help="采集目标 http(s) URL(视频/频道/播放列表页)",
    )
    media.add_argument(
        "--max-items",
        type=int,
        default=DEFAULT_MEDIA_MAX_ITEMS,
        help=f"返回条目上限,经上游 --playlist-end 前置预算(默认 {DEFAULT_MEDIA_MAX_ITEMS})",
    )
    media.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_MEDIA_TIMEOUT_SECONDS,
        help=f"子进程 wall-clock 预算秒数(默认 {DEFAULT_MEDIA_TIMEOUT_SECONDS:g})",
    )
    media.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR},样板位于 myssia-media/ 子目录)",
    )
    media.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


# ---------------------------------------------------------------------------
# myssia maigret(myssia-maigret 插件;10-05-plugin-market-batch 首批:
# maigret(MIT)上游经 uv 临时环境隔离子进程,用户名跨站侦察(-J simple
# JSON 报告,命中对象在条目 status 键下——v0.6.6 实测契约)。
# 退出码族:0 成功(含零命中合法空态)/ 1 配置或环境错误 / 2 采集失败;
# --json 下 stdout 恒单份 JSON)
# ---------------------------------------------------------------------------


def _print_maigret_human(payload: dict[str, Any]) -> None:
    """人类可读摘要(与 --json 同一信息,另一种皮)."""
    print(
        f"世事 maigret:{payload.get('target')} 命中 {payload.get('hit_count')} 站"
        f"(范围 top-{payload.get('top_sites')},插件 {payload.get('plugin')})"
    )
    for hit in payload.get("hits") or []:
        tags = ",".join(hit.get("tags") or []) or "无标签"
        print(f"  {hit.get('site')}:{hit.get('url')}[{tags}]")
    print(f"  耗时:{payload.get('duration_seconds')}s")


def _cmd_maigret(args: argparse.Namespace) -> int:
    """``myssia maigret``:跑一次上游 maigret 跨站侦察,结构化输出.

    退出码:0 成功(含零命中合法空态);1 适配器缺失/uv 缺失/用户名非法
    (配置或环境错误);2 采集失败(上游非零退出/超时/报告缺失或损坏)。
    失败码到退出码的映射用 :data:`MAIGRET_FETCH_FAILURE_CODES`(CLI 所有)。
    任何失败都只影响本命令,核心品类流水线照常(铁律)。
    """
    try:
        adapter = _import_plugin_adapter(args.plugins_dir, MAIGRET_PLUGIN_ID)
    except (OSError, ImportError, SyntaxError) as exc:
        _emit_generic_error(
            "maigret_adapter_missing",
            str(exc),
            as_json=args.as_json,
            plugins_dir=str(args.plugins_dir),
        )
        return EXIT_CONFIG_ERROR
    try:
        payload = adapter.run(
            args.username,
            timeout=args.timeout,
            top_sites=args.top_sites,
            site_timeout=args.site_timeout,
        )
    except Exception as exc:  # noqa: BLE001 — 适配器一切失败都结构化降级,绝不拦核心
        details = (
            exc.to_dict()
            if hasattr(exc, "to_dict")
            else {"code": "maigret_failed", "message": str(exc)}
        )
        code = str(details.get("code", "maigret_failed"))
        exit_code = (
            EXIT_FETCH_ALL_FAILED
            if code in MAIGRET_FETCH_FAILURE_CODES
            else EXIT_CONFIG_ERROR
        )
        extra = {
            key: value
            for key, value in details.items()
            if key not in ("code", "message")
        }
        _emit_generic_error(
            code, str(details.get("message", exc)), as_json=args.as_json, **extra
        )
        return exit_code
    if args.as_json:
        _print_json(payload)
    else:
        _print_maigret_human(payload)
    return EXIT_OK


def _add_maigret_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia maigret``:用户名跨站侦察(10-05-plugin-market-batch myssia-maigret)."""
    maigret = sub.add_parser(
        "maigret",
        help="用户名跨站侦察(myssia-maigret 插件,uv 隔离子进程;失败绝不拦核心)",
        description=(
            "定位 <plugins-dir>/myssia-maigret(适配器 adapter.py),以 uv 临时环境"
            "(--no-project --with maigret,不进根依赖)隔离子进程跑上游 CLI:对"
            "一个用户名跨站查占用/命中(-J simple JSON 报告),站点范围按 rank"
            " 前 N 预算。零命中=合法空态;仅用于已授权侦察目标,逐站直连零第三方"
            "聚合服务器。适配器缺失/用户名非法退 1;采集失败退 2;任何失败不影响"
            "核心品类流水线(铁律)。"
        ),
    )
    maigret.add_argument(
        "username",
        help="待查用户名(字母数字开头,仅字母/数字/./_/-;授权侦察目标)",
    )
    maigret.add_argument(
        "--top-sites",
        type=int,
        default=DEFAULT_MAIGRET_TOP_SITES,
        help=f"站点库 rank 前 N 预算(默认 {DEFAULT_MAIGRET_TOP_SITES};0=不限,慎用)",
    )
    maigret.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_MAIGRET_TIMEOUT_SECONDS,
        help=f"子进程 wall-clock 预算秒数(默认 {DEFAULT_MAIGRET_TIMEOUT_SECONDS:g})",
    )
    maigret.add_argument(
        "--site-timeout",
        type=float,
        default=DEFAULT_MAIGRET_SITE_TIMEOUT_SECONDS,
        help=f"逐站请求超时秒数,透传上游 --timeout(默认 {DEFAULT_MAIGRET_SITE_TIMEOUT_SECONDS:g})",
    )
    maigret.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR},样板位于 myssia-maigret/ 子目录)",
    )
    maigret.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


# ---------------------------------------------------------------------------
# myssia harvester(myssia-theharvester 插件;10-05-plugin-market-batch 首批:
# theHarvester(GPL-2.0)上游 submodule 钉 4.9.2,经 uv 临时环境(--no-config
# --no-project --with 钉版依赖)隔离子进程,-c 唤起上游入口(上游无 __main__
# 直跑守卫,4.9.2 实测),-f 落 JSON+XML 双件,适配器读 JSON 分桶装配。
# 退出码族:0 成功(含零命中合法空态)/ 1 配置或环境错误 / 2 采集失败;
# --json 下 stdout 恒单份 JSON)
# ---------------------------------------------------------------------------


def _print_harvester_human(payload: dict[str, Any]) -> None:
    """人类可读摘要(与 --json 同一信息,另一种皮)."""
    vendor = payload.get("vendor") or {}
    print(
        f"世事 harvester:{payload.get('target')} 源 {payload.get('source_list')}"
        f"(插件 {payload.get('plugin')})"
    )
    if vendor.get("commit"):
        print(f"  vendor pin:{vendor['commit']}")
    for bucket, count in sorted((payload.get("result_totals") or {}).items()):
        print(f"  {bucket}:{count} 条")
    print(f"  耗时:{payload.get('duration_seconds')}s")


def _cmd_harvester(args: argparse.Namespace) -> int:
    """``myssia harvester``:跑一次上游 theHarvester 域名侦察,结构化输出.

    退出码:0 成功(含零命中合法空态);1 适配器缺失/vendor 未初始化/uv
    缺失/目标或源清单非法(配置或环境错误);2 采集失败(上游非零退出/超时/
    报告缺失或损坏)。失败码到退出码的映射用 :data:`HARVESTER_FETCH_FAILURE_CODES`
    (CLI 所有)。任何失败都只影响本命令,核心品类流水线照常(铁律)。
    """
    try:
        adapter = _import_plugin_adapter(args.plugins_dir, HARVESTER_PLUGIN_ID)
    except (OSError, ImportError, SyntaxError) as exc:
        _emit_generic_error(
            "harvester_adapter_missing",
            str(exc),
            as_json=args.as_json,
            plugins_dir=str(args.plugins_dir),
        )
        return EXIT_CONFIG_ERROR
    try:
        payload = adapter.run(
            args.domain,
            sources=args.sources,
            timeout=args.timeout,
        )
    except Exception as exc:  # noqa: BLE001 — 适配器一切失败都结构化降级,绝不拦核心
        details = (
            exc.to_dict()
            if hasattr(exc, "to_dict")
            else {"code": "harvester_failed", "message": str(exc)}
        )
        code = str(details.get("code", "harvester_failed"))
        exit_code = (
            EXIT_FETCH_ALL_FAILED
            if code in HARVESTER_FETCH_FAILURE_CODES
            else EXIT_CONFIG_ERROR
        )
        extra = {
            key: value
            for key, value in details.items()
            if key not in ("code", "message")
        }
        _emit_generic_error(
            code, str(details.get("message", exc)), as_json=args.as_json, **extra
        )
        return exit_code
    if args.as_json:
        _print_json(payload)
    else:
        _print_harvester_human(payload)
    return EXIT_OK


def _add_harvester_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia harvester``:域名聚合侦察(10-05-plugin-market-batch myssia-theharvester)."""
    harvester = sub.add_parser(
        "harvester",
        help="域名/组织聚合侦察(myssia-theharvester 插件,GPL 上游 submodule+uv 隔离子进程;失败绝不拦核心)",
        description=(
            "定位 <plugins-dir>/myssia-theharvester(适配器 adapter.py + "
            "vendor/theHarvester submodule,首次须 git submodule update --init),"
            "以 uv 临时环境(--no-config --no-project --with 钉版依赖,不进根依赖)"
            "隔离子进程跑上游 CLI:邮箱/子域/IP 开源聚合侦察,缺省凭据免费源 "
            "crtsh+dnsdumpster。零命中=合法空态;仅用于已授权安全研究与自有/"
            "已授权资产;本机直连零第三方聚合服务器。适配器缺失/vendor 未初始化/"
            "目标非法退 1;采集失败退 2;任何失败不影响核心品类流水线(铁律)。"
        ),
    )
    harvester.add_argument(
        "domain",
        help="侦察目标域名/组织名(字母数字开头,仅字母/数字/./_/-;授权侦察目标)",
    )
    harvester.add_argument(
        "--sources",
        default="crtsh,dnsdumpster",
        help="逗号分隔的源清单(缺省 crtsh,dnsdumpster 两凭据免费源;全量见上游 --source-list)",
    )
    harvester.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_HARVESTER_TIMEOUT_SECONDS,
        help=f"子进程 wall-clock 预算秒数(默认 {DEFAULT_HARVESTER_TIMEOUT_SECONDS:g})",
    )
    harvester.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR},样板位于 myssia-theharvester/ 子目录)",
    )
    harvester.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


# ---------------------------------------------------------------------------
# myssia credhunt / credcheck / exposure(myssia-credhunter 插件三 lane;
# 10-03-aipocket-fusion:正式取数走 engine: credhunter 进管线,本三命令是
# 调试/冒烟/后处理口 —— credhunt/exposure 单次取数 stdout JSON,credcheck
# 读凭证批探测回显。退出码族与全家桶对齐:0 成功 / 1 配置或用法错误 /
# 2 采集全部失败 / 3 部分失败;--json 下 stdout 恒单份 JSON)
# ---------------------------------------------------------------------------


def _resolve_cli_secret(value: str) -> str:
    """解析一条 CLI 凭据实参:引用(env:/keychain:)就解析,裸值原样透传。

    与品类 YAML 的「凭据只许引用」红线不同,CLI 实参是主人手工传值面
    (冒烟场景:自备活 key/构造死 key),裸值合法;但**写成引用形态**就必须
    解析成功——解析失败(钥匙串没写/环境变量缺)是真实错误,不把引用串
    本身当密钥用。
    """
    try:
        parse_secret_value(value, label="CLI 凭据实参")
    except SchemaValueError:
        return value  # 非引用形态:裸值
    return resolve_credential(value)


def _credhunter_status_exit_code(payload: dict[str, Any], *, command: str) -> int:
    """payload 状态面 → 退出码(契约归 CLI;三命令同族语义)。

    - credhunt:status partial=3 / degraded=2 / 其余(success/empty)=0;
    - credcheck:transient 全占 =2(探测全败),部分 transient =3,其余 0
      (rejected/final_verified 是探测**结论**,不是失败);
    - exposure:查询错误全量(错误数 ≥ 计划数且零 findings)=2,部分错
      误=3,无错误=0(无 key 显式空态 = 0,AC6)。
    """
    if command == "credhunt":
        status = str(payload.get("status", "empty"))
        if status == "partial":
            return EXIT_PARTIAL
        if status == "degraded":
            return EXIT_FETCH_ALL_FAILED
        return EXIT_OK
    if command == "credcheck":
        counts = payload.get("counts") or {}
        total = int(counts.get("records", 0))
        transient = int(counts.get("transient", 0))
        if total and transient == total:
            return EXIT_FETCH_ALL_FAILED
        if transient:
            return EXIT_PARTIAL
        return EXIT_OK
    # exposure:按 lane 汇总(queries_planned=0 的 credential_missing lane
    # 不计入失败面)。
    lanes = payload.get("lanes") or {}
    errors = sum(
        int(lane.get("errors", 0)) for lane in lanes.values() if isinstance(lane, dict)
    )
    planned = sum(
        int(lane.get("queries_planned", 0))
        for lane in lanes.values()
        if isinstance(lane, dict)
    )
    findings = len(payload.get("findings") or [])
    if errors == 0:
        return EXIT_OK
    if findings == 0 and planned and errors >= planned:
        return EXIT_FETCH_ALL_FAILED
    return EXIT_PARTIAL


def _run_credhunter_command(
    args: argparse.Namespace,
    *,
    command: str,
    config_failure_codes: frozenset[str],
) -> tuple[dict[str, Any] | None, int]:
    """三命令共用的装配段:加载适配器 → 调对应入口 → 结构化降级。

    Returns:
        (payload, exit_code):payload=None 表示已降级打印(退 1/2),调用方
        直接返回退出码;否则 payload 待打印,退出码由调用面继续算。
    """
    try:
        if command == "credcheck" and bool(
            getattr(args, "from_keystore", False)
        ) == bool(getattr(args, "apikeys", None)):
            # 双入口互斥校验:--apikey 与 --from-keystore 恰用其一。
            _emit_generic_error(
                "credcheck_input_conflict"
                if args.apikeys
                else "credcheck_input_missing",
                "--apikey 与 --from-keystore 必须二选一(当前"
                + ("两者都给" if args.apikeys else "两者都没给")
                + ")",
                as_json=args.as_json,
            )
            return None, EXIT_CONFIG_ERROR
        adapter = _import_plugin_adapter(args.plugins_dir, CREDHUNTER_PLUGIN_ID)
    except (OSError, ImportError, SyntaxError) as exc:
        _emit_generic_error(
            "credhunter_adapter_missing",
            str(exc),
            as_json=args.as_json,
            plugins_dir=str(args.plugins_dir),
        )
        return None, EXIT_CONFIG_ERROR
    try:
        if command == "credhunt":
            tokens = [
                _resolve_cli_secret(token) for token in (args.github_tokens or [])
            ]
            payload = adapter.run_credhunt(
                github_tokens=tokens,
                queries=args.queries,
                checkpoint=_load_credhunt_checkpoint_cli(args.checkpoint_file),
            )
        elif command == "credcheck":
            if args.from_keystore:
                payload = adapter.run_credcheck_keystore(
                    keystore_path=args.keystore_file,
                    probe_balance=args.balance,
                    limit=args.limit,
                )
            else:
                records = [
                    {"apikey": _resolve_cli_secret(key), "apiurl": args.apiurl}
                    for key in (args.apikeys or [])
                ]
                payload = adapter.run_credcheck(
                    records=records, probe_balance=args.balance
                )
        else:
            payload = adapter.run_exposure(
                fofa_key=_resolve_cli_secret(args.fofa_key) if args.fofa_key else None,
                fofa_base=args.fofa_base,
                shodan_key=_resolve_cli_secret(args.shodan_key)
                if args.shodan_key
                else None,
                probe=not args.no_probe,
            )
    except Exception as exc:  # noqa: BLE001 — 适配器一切失败都结构化降级,绝不拦核心
        if isinstance(exc, CredentialResolveError):
            # 凭据引用解析失败(钥匙串没写/env 缺失/名空间非法)= 配置错误。
            _emit_generic_error(exc.code, str(exc), as_json=args.as_json)
            return None, EXIT_CONFIG_ERROR
        details = (
            exc.to_dict()
            if hasattr(exc, "to_dict")
            else {"code": f"{command}_failed", "message": str(exc)}
        )
        code = str(details.get("code", f"{command}_failed"))
        exit_code = (
            EXIT_CONFIG_ERROR if code in config_failure_codes else EXIT_FETCH_ALL_FAILED
        )
        extra = {
            key: value
            for key, value in details.items()
            if key not in ("code", "message")
        }
        _emit_generic_error(
            code, str(details.get("message", exc)), as_json=args.as_json, **extra
        )
        return None, exit_code
    return payload, EXIT_OK


def _load_credhunt_checkpoint_cli(path: str | None) -> dict[str, Any] | None:
    """``--checkpoint-file`` 读入(坏文件=从头续跑,不拦命令)。"""
    if not path:
        return None
    try:
        loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return loaded if isinstance(loaded, dict) else None


def _save_credhunt_checkpoint_cli(path: str | None, payload: dict[str, Any]) -> None:
    if path and isinstance(payload.get("checkpoint"), dict):
        try:
            Path(path).write_text(
                json.dumps(payload["checkpoint"], ensure_ascii=False), encoding="utf-8"
            )
        except OSError:
            pass  # checkpoint 持久化失败不拦本轮输出


def _print_credhunt_human(payload: dict[str, Any], *, command: str) -> None:
    """三命令共用的中文摘要(与 --json 同一信息,另一种皮)。"""
    print(f"世事 {command}({payload.get('plugin')}):{payload.get('status')}")
    if command == "credcheck":
        counts = payload.get("counts") or {}
        print(
            f"  验证 {counts.get('records', 0)} 条:final_verified={counts.get('final_verified', 0)}"
            f" rejected={counts.get('rejected', 0)} transient={counts.get('transient', 0)}"
            f"(余额探测:{'开' if payload.get('probe_balance') else '关'})"
        )
        for result in payload.get("results") or []:
            print(
                f"  {result.get('provider')}/{result.get('validation_state')}:{result.get('error') or 'ok'}"
            )
        return
    findings = payload.get("findings") or []
    print(f"  发现 {len(findings)} 条(命中键一律前 8 后 4 掩码)")
    for item in findings[:5]:
        print(f"  - {item.get('title')}")
    if command == "credhunt":
        errors = payload.get("errors") or []
        print(f"  泳道错误 {len(errors)} 条;耗时 {payload.get('duration_seconds')}s")
        return
    for name, lane in (payload.get("lanes") or {}).items():
        if isinstance(lane, dict):
            print(
                f"  lane {name}:{lane.get('status')}(命中 {lane.get('hits', 0)},错误 {lane.get('errors', 0)})"
            )
    print(f"  耗时 {payload.get('duration_seconds')}s")


def _cmd_credhunt(args: argparse.Namespace) -> int:
    """``myssia credhunt``:单轮 GitHub 工件凭证猎取(调试/冒烟口).

    退出码:0 成功(含干净空手);1 适配器缺失/无 token(该源不启用);
    2 全部查询失败;3 部分查询失败仍有产出。正式产出走品类 YAML 的
    ``engine: credhunter`` 源进管线。
    """
    payload, exit_code = _run_credhunter_command(
        args, command="credhunt", config_failure_codes=CREDHUNT_CONFIG_FAILURE_CODES
    )
    if payload is None:
        return exit_code
    _save_credhunt_checkpoint_cli(args.checkpoint_file, payload)
    if args.as_json:
        _print_json(payload)
    else:
        _print_credhunt_human(payload, command="credhunt")
    return _credhunter_status_exit_code(payload, command="credhunt")


def _cmd_credcheck(args: argparse.Namespace) -> int:
    """``myssia credcheck``:凭证验证(+可选余额/身份探测)stdout payload.

    Q7:余额/身份探测默认关,``--balance`` 显式开;Q8:串行 + 每供应商
    RPM≤30(适配器内建 Pacer)。退出码:0 完成(rejected 是结论不是错误);
    1 适配器缺失/记录形状坏;2 全部 transient(探测全败);3 部分 transient。
    """
    payload, exit_code = _run_credhunter_command(
        args, command="credcheck", config_failure_codes=CREDCHECK_CONFIG_FAILURE_CODES
    )
    if payload is None:
        return exit_code
    if args.as_json:
        _print_json(payload)
    else:
        _print_credhunt_human(payload, command="credcheck")
    return _credhunter_status_exit_code(payload, command="credcheck")


def _cmd_exposure(args: argparse.Namespace) -> int:
    """``myssia exposure``:FOFA/Shodan 曝面 + L0 被动探测(调试/冒烟口).

    退出码:0 成功(含无 key 显式空态,AC6);1 适配器缺失;2 全部查询
    失败且零发现;3 部分查询失败。被动探测只做 L0 unauth_read。
    """
    payload, exit_code = _run_credhunter_command(
        args, command="exposure", config_failure_codes=EXPOSURE_CONFIG_FAILURE_CODES
    )
    if payload is None:
        return exit_code
    if args.as_json:
        _print_json(payload)
    else:
        _print_credhunt_human(payload, command="exposure")
    return _credhunter_status_exit_code(payload, command="exposure")


def _add_credhunt_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia credhunt``:GitHub 工件凭证猎取单轮直跑(myssia-credhunter)."""
    credhunt = sub.add_parser(
        "credhunt",
        help="GitHub 工件凭证猎取单轮直跑(myssia-credhunter 插件,调试/冒烟口;正式产出走 engine: credhunter)",
        description=(
            "按供应商指纹库查询集跑 GitHub code search + commit message 两泳道,"
            "联合正则十大密钥族全文匹配,产出掩码-only(前 8 后 4)发现。"
            "无 token 该源不启用(退 1);查询预算 12/run(checkpoint 跨 run 轮转);"
            "限速仅 403/429 退避(≤90s 只重试一轮)。授权边界:仅用于已授权"
            "安全研究与自有/已授权资产排查。"
        ),
    )
    credhunt.add_argument(
        "--github-token",
        dest="github_tokens",
        action="append",
        help="GitHub token(可重复=token 池;裸值或 env:/keychain: 引用均可)",
    )
    credhunt.add_argument(
        "--query",
        dest="queries",
        action="append",
        help="GitHub 搜索查询(可重复;缺省 = 指纹库全部包 github_terms 去重池)",
    )
    credhunt.add_argument(
        "--checkpoint-file",
        default=None,
        help="跨 run 游标持久化文件(读入+写回;不传则单轮从头发起)",
    )
    credhunt.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR},场景件位于 myssia-credhunter/ 子目录)",
    )
    credhunt.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_credcheck_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia credcheck``:凭证验证 + 可选余额探测(myssia-credhunter)."""
    credcheck = sub.add_parser(
        "credcheck",
        help="凭证验证(models 三态)+ 可选余额/身份探测(myssia-credhunter 插件)",
        description=(
            "双入口:--apikey 显式传键,或 --from-keystore 读猎手落盘的本地"
            "密钥库(缺省 $MYIA_HOME/cwd 下 credhunter-keystore.json,600 权限,"
            "验证结果回填 check_state/last_check ——「猎→存→验」闭环)。探测:"
            "resolve(域名→前缀→unknown)→ models 三态验证(final_verified/"
            "rejected/transient)→ 可选余额探测(--balance 显式开,Q7)。串行 +"
            "每供应商 RPM≤30(Q8);密钥全文只用于探测头,输出一律掩码(Q9)。"
            "冒烟口径:自备活 key 验 final_verified + 构造死 key 验 rejected。"
        ),
    )
    credcheck.add_argument(
        "--apikey",
        dest="apikeys",
        action="append",
        help="待验证密钥(可重复;裸值或 env:/keychain: 引用均可;与 --from-keystore 二选一)",
    )
    credcheck.add_argument(
        "--from-keystore",
        dest="from_keystore",
        action="store_true",
        help="读本地密钥库验证并回填状态(与 --apikey 二选一;Q9:全文不出库)",
    )
    credcheck.add_argument(
        "--keystore-file",
        dest="keystore_file",
        default=None,
        help="密钥库路径(仅 --from-keystore 时生效;缺省 $MYIA_HOME/cwd 下 credhunter-keystore.json)",
    )
    credcheck.add_argument(
        "--limit",
        dest="limit",
        type=int,
        default=None,
        help="最多验证条数(仅 --from-keystore 时生效;缺省全量,按入库顺序)",
    )
    credcheck.add_argument(
        "--apiurl",
        default="",
        help="API 基址归因提示(可空;仅 --apikey 入口生效,空则按密钥前缀/规格官方基址)",
    )
    credcheck.add_argument(
        "--balance",
        action="store_true",
        help="开余额/身份探测(默认关;Q7 决议:存活探测默认、余额显式)",
    )
    credcheck.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR})",
    )
    credcheck.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def _add_exposure_parser(sub: argparse._SubParsersAction) -> None:
    """``myssia exposure``:FOFA/Shodan 曝面 + L0 被动探测(myssia-credhunter)."""
    exposure = sub.add_parser(
        "exposure",
        help="FOFA/Shodan 曝面发现 + L0 被动探测(myssia-credhunter 插件,无 key 显式空态)",
        description=(
            "按指纹库查询集跑 FOFA(qbase64,页间 0.3s,24 查询/run)与 Shodan"
            "(机械翻译查询,页间 1.0s,16 查询/run),命中目标做 L0 unauth_read"
            "被动探测(2xx=未授权读发现,证据掩码+512 截断)。无 key 的 lane 显式"
            "空态不报错(AC6);FOFA base 可配(官方/代理域部署者自决)。"
        ),
    )
    exposure.add_argument(
        "--fofa-key", default=None, help="FOFA key(裸值或 env:/keychain: 引用)"
    )
    exposure.add_argument(
        "--fofa-base",
        default=None,
        help="FOFA base URL(官方/代理域部署者自决,刻意不写死;有 key 无 base → lane 显式 base_missing 空态)",
    )
    exposure.add_argument(
        "--shodan-key", default=None, help="Shodan key(裸值或 env:/keychain: 引用)"
    )
    exposure.add_argument(
        "--no-probe",
        action="store_true",
        help="跳过被动探测(只搜页不出曝面发现)",
    )
    exposure.add_argument(
        "--plugins-dir",
        default=DEFAULT_PLUGINS_DIR,
        help=f"插件目录(默认 ./{DEFAULT_PLUGINS_DIR})",
    )
    exposure.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="机器可读输出(单份 JSON,stdout)",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """CLI 入口(pyproject console_scripts:``myssia = "myssia.cli:main"``)。

    Args:
        argv: 参数列表;None 表示 ``sys.argv[1:]``。

    Returns:
        退出码:0 成功 / 1 配置或用法错误 / 2 采集全部失败 / 3 部分失败。

    Raises:
        SystemExit: ``--help`` / ``--version``(exit 0)。
    """
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except _UsageError as exc:
        print(
            json.dumps({"error": "usage", "message": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        return EXIT_CONFIG_ERROR
    if args.command is None:
        parser.print_help()
        return EXIT_OK
    handlers = {
        "run": _cmd_run,
        "cron": _cmd_cron,
        "init": _cmd_init,
        "test": _cmd_test,
        "list": _cmd_list,
        "doctor": _cmd_doctor,
        "secret": _cmd_secret,
        "gates": _cmd_gates,
        "plugin": _cmd_plugin,
        "channels": _cmd_channels,
        "feedback": _cmd_feedback,
        "alerts": _cmd_alerts,
        "skill": _cmd_skill,
        "osint": _cmd_osint,
        "proxy": _cmd_proxy,
        "media": _cmd_media,
        "maigret": _cmd_maigret,
        "harvester": _cmd_harvester,
        "credhunt": _cmd_credhunt,
        "credcheck": _cmd_credcheck,
        "exposure": _cmd_exposure,
    }
    handler = handlers.get(args.command)
    if handler is not None:
        return handler(args)
    return _not_implemented(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
