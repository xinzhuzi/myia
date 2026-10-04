"""myssia-theharvester 适配器:子进程调用上游 theHarvester(GPL-2.0)——MYIA 侧代码.

本文件由 MYIA 仓库创作与维护,**不是**上游代码;上游 theHarvester(GPL-2.0,
laramies/theHarvester)只以 git submodule 钉在 ``vendor/theHarvester``
(pin 4.9.2 / ba853666,选型记录见 plugin.yaml:master 当日实跑含 Python2
语法残留不可运行),零复制、零修改、零分发。

适配器职责:对域名/组织跑一次上游聚合侦察(邮箱/子域/IP 等),装配结构化
结果。上游接入事实(2026-10-05 对 4.9.2 实测):

- 上游 pip 包为空壳(装得上、无模块),必须源码运行:cwd=vendor 子进程;
- 上游无 ``__main__`` 直跑守卫,经 ``python -c "from theHarvester.theHarvester
  import main; main()"`` 唤起,``-d/-b/-f/-q`` 落在 sys.argv[1:];
- ``-f NAME`` 落 NAME.json + NAME.xml(适配器只读 JSON);
- 依赖与 4.9.2 pyproject 的钉版清单逐条同源(uv ``--with`` 注入临时环境,
  绝不进根依赖);``--no-config`` 防止 uv 读 vendor pyproject 的自有配置。

错误契约(spec python/error-handling):所有失败抛
:class:`HarvesterAdapterError`(code + message + 结构化 details)。code 词表:

- ``domain_invalid``    目标非法(防 argv 注入:首字符禁 ``-``)
- ``vendor_missing``    vendor/theHarvester 源码未就位(未 init submodule)
- ``uv_missing``        宿主无 uv(隔离运行时不可用)
- ``harvester_failed``  上游子进程非零退出(采集失败)
- ``harvester_timeout`` 子进程超过 wall-clock 预算(采集失败)
- ``harvester_report_missing`` / ``harvester_report_invalid``
                        退出 0 但 JSON 缺失/不可解析(采集失败)

零命中=合法空态(success 且各桶空),不是错误。失败码 → CLI 退出码的映射
归 CLI 所有(:data:`myssia.cli.HARVESTER_FETCH_FAILURE_CODES`)。铁律:
任何失败只影响 ``myssia harvester`` 自身,核心品类流水线照常跑通(测试钉在
tests/plugins/test_theharvester_plugin.py)。

采集边界:仅用于已授权安全研究与自有/已授权资产;缺省源 crtsh+dnsdumpster
为凭据免费源,带 key 的源(shodan/censys 等)未配凭据会被上游跳过;本机
直连,零第三方聚合服务器(P0 本地执行硬规则)。
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

__all__ = [
    "DEFAULT_SOURCES",
    "DEFAULT_TIMEOUT_SECONDS",
    "HarvesterAdapterError",
    "THEHARVESTER_DEPENDENCIES",
    "build_command",
    "is_available",
    "normalize_domain",
    "plugin_dir",
    "run",
    "vendor_commit",
    "vendor_root",
]

#: 适配器所在插件目录(本文件按样板布局固定在 plugins/myssia-theharvester/ 下)。
PLUGIN_DIR = Path(__file__).resolve().parent

#: 上游 submodule 相对插件目录路径(与 plugin.yaml ``vendor.path`` 同源)。
VENDOR_RELATIVE_PATH = "vendor/theHarvester"

#: 上游包体存在性判据(相对 vendor 根)。
VENDOR_PACKAGE = "theHarvester/theHarvester.py"

#: 唤起上游的 -c 片段:上游无 __main__ 直跑守卫(4.9.2 实测),经入口函数唤起。
ENTRY_SNIPPET = "from theHarvester.theHarvester import main; main()"

#: 隔离子进程注入的上游依赖(与 4.9.2 pyproject 钉版清单逐条同源;uvloop 带
#: 平台标记与上游声明一致)。绝不进根依赖。
THEHARVESTER_DEPENDENCIES = (
    "aiodns==3.6.1",
    "aiofiles==25.1.0",
    "aiohttp==3.13.2",
    "aiomultiprocess==0.9.1",
    "aiosqlite==0.22.1",
    "beautifulsoup4==4.14.3",
    "censys==2.2.19",
    "certifi==2025.11.12",
    "dnspython==2.8.0",
    "fastapi==0.128.0",
    "lxml==6.0.2",
    "netaddr==1.3.0",
    "playwright==1.57.0",
    "PyYAML==6.0.3",
    "python-dateutil==2.9.0.post0",
    "httpx==0.28.1",
    "retrying==1.4.2",
    "shodan==1.31.0",
    "slowapi==0.1.9",
    "ujson==5.11.0",
    "uvicorn==0.40.0",
    "uvloop==0.22.1; sys_platform != 'win32'",
    "winloop==0.6.3; sys_platform == 'win32'",
)

#: 缺省源:凭据免费且长期稳定的两源(带 key 的源未配凭据会被上游跳过)。
DEFAULT_SOURCES = "crtsh,dnsdumpster"

#: 子进程 wall-clock 预算缺省值(整个侦察过程)。
DEFAULT_TIMEOUT_SECONDS = 600.0

#: 目标合法性:域名/组织名公共子集;首字符禁 ``-`` = argv 注入面。
_DOMAIN_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,252}$")

#: 结构化错误里 stderr/stdout 摘录的上限(保持 JSON 输出有界)。
_PROCESS_TAIL_CHARS = 2000


class HarvesterAdapterError(Exception):
    """结构化适配器错误:code + message + details,``to_dict()`` 进 JSON 输出."""

    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        """结构化形态:{"code", "message", **details}(供 CLI --json 与 agent 自修)."""
        return {"code": self.code, "message": self.message, **self.details}


def plugin_dir() -> Path:
    """本插件目录(适配器所在处)."""
    return PLUGIN_DIR


def vendor_root(plugin_dir: str | Path | None = None) -> Path:
    """上游 vendor 根目录(可注入 plugin_dir 供测试/安装根场景)."""
    root = Path(plugin_dir) if plugin_dir is not None else PLUGIN_DIR
    return root / VENDOR_RELATIVE_PATH


def is_available(plugin_dir: str | Path | None = None) -> bool:
    """上游源码是否就位(submodule 已 init 且包体存在)."""
    return (vendor_root(plugin_dir) / VENDOR_PACKAGE).is_file()


def vendor_commit(
    plugin_dir: str | Path | None = None,
    *,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
) -> str | None:
    """读 vendor 工作树钉住的 commit;取不到返回 None(纯溯源,绝不抛)."""
    do_run = runner if runner is not None else subprocess.run
    vendor = vendor_root(plugin_dir)
    if not vendor.is_dir() or not (vendor / ".git").exists():
        return None
    try:
        completed = do_run(
            ["git", "-C", str(vendor), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10.0,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return (completed.stdout or "").strip() or None


def normalize_domain(domain: str) -> str:
    """校验侦察目标:域名/组织名公共子集,首字符禁 ``-``(防 argv 注入)."""
    value = (domain or "").strip()
    if not _DOMAIN_RE.fullmatch(value):
        raise HarvesterAdapterError(
            "domain_invalid",
            f"侦察目标非法:{value!r}(须字母数字开头,仅字母/数字/./_/-;示例:example.com)",
            domain=value,
        )
    return value


def _validate_sources(sources: str) -> str:
    """源清单合法性:逗号分隔的标识符,同样防注入(首字符禁 ``-``)."""
    value = (sources or "").strip()
    tokens = [token.strip() for token in value.split(",") if token.strip()]
    if not tokens or not all(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", t) for t in tokens):
        raise HarvesterAdapterError(
            "domain_invalid",
            f"源清单非法:{sources!r}(逗号分隔的源标识符,如 crtsh,dnsdumpster)",
            sources=sources,
        )
    return ",".join(tokens)


def build_command(
    domain: str,
    sources: str,
    report_prefix: str | Path,
    *,
    extra_args: tuple[str, ...] | list[str] = (),
) -> list[str]:
    """装配隔离子进程命令:uv 临时环境注入钉版依赖,-c 唤起上游入口.

    ``--no-config`` 防 uv 读 vendor pyproject 的自有配置(实测会告警);
    ``-f`` 落 JSON+XML 双件(适配器只读 JSON);``-q`` 抑制缺 key 提示噪音。
    """
    command = ["uv", "run", "--no-config", "--no-project"]
    for dependency in THEHARVESTER_DEPENDENCIES:
        command += ["--with", dependency]
    command += [
        "python",
        "-c",
        ENTRY_SNIPPET,
        "-d",
        domain,
        "-b",
        sources,
        "-f",
        str(report_prefix),
        "-q",
        *extra_args,
    ]
    return command


def _tail(text: str | None) -> str:
    """进程输出摘录(尾部),保持结构化错误有界."""
    value = (text or "").strip()
    return value[-_PROCESS_TAIL_CHARS:]


def run(
    domain: str,
    *,
    sources: str = DEFAULT_SOURCES,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    extra_args: tuple[str, ...] | list[str] = (),
    plugin_dir: str | Path | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """对 ``domain`` 跑一次上游 theHarvester 聚合侦察.

    Args:
        domain: 域名/组织名(授权侦察目标,由使用者自负边界)。
        sources: 逗号分隔的源清单(缺省 crtsh,dnsdumpster 两凭据免费源)。
        timeout: 子进程 wall-clock 预算秒数,超时抛 ``harvester_timeout``。
        extra_args: 透传给上游 CLI 的附加参数(如 ``("-l", "200")``)。
        plugin_dir: 插件目录覆盖(测试/自定义安装根)。
        runner: subprocess.run 注入口(测试 mock 用)。
        clock: 单调时钟注入口(测试 mock 用)。

    Returns:
        结构化结果 dict:plugin/target/status/vendor(path+commit)/command/
        exit_code/duration_seconds/source_list/results(上游 JSON 的分桶:
        emails/hosts/ips 等列表字段)+result_totals(各桶条数)。

    Raises:
        HarvesterAdapterError: 全部失败形态都是结构化错误(见模块 docstring 词表)。
        零命中不是错误:status=success 且各桶空(合法空态)。
    """
    do_run = runner if runner is not None else subprocess.run
    root = Path(plugin_dir) if plugin_dir is not None else PLUGIN_DIR
    clean_domain = normalize_domain(domain)
    clean_sources = _validate_sources(sources)
    vendor = vendor_root(root)
    if not (vendor / VENDOR_PACKAGE).is_file():
        raise HarvesterAdapterError(
            "vendor_missing",
            (
                f"上游源码未就位:{vendor / VENDOR_PACKAGE} 不存在。"
                f"先初始化 submodule(在插件目录 {root} 下执行):"
                f"git submodule update --init {VENDOR_RELATIVE_PATH}"
            ),
            plugin_dir=str(root),
            vendor_path=str(vendor),
        )
    if shutil.which("uv") is None:
        raise HarvesterAdapterError(
            "uv_missing",
            "隔离运行时不可用: PATH 上找不到 uv(https://docs.astral.sh/uv/)。"
            "适配器以 uv 临时环境运行上游 CLI,依赖不进根依赖。",
            domain=clean_domain,
        )
    started = clock()
    with tempfile.TemporaryDirectory(prefix="myssia-theharvester-") as scratch:
        report_prefix = Path(scratch) / "harvest"
        command = build_command(
            clean_domain, clean_sources, report_prefix, extra_args=extra_args
        )
        try:
            completed = do_run(
                command,
                cwd=str(vendor),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise HarvesterAdapterError(
                "harvester_timeout",
                f"theHarvester 子进程超过 {timeout:g}s 预算被终止(目标 {clean_domain})",
                domain=clean_domain,
                timeout_seconds=timeout,
                stderr_tail=_tail(exc.stderr if isinstance(exc.stderr, str) else None),
            ) from exc
        duration = round(clock() - started, 3)
        if completed.returncode != 0:
            raise HarvesterAdapterError(
                "harvester_failed",
                (
                    f"theHarvester 子进程非零退出(code={completed.returncode};"
                    f"目标 {clean_domain},源 {clean_sources})"
                ),
                domain=clean_domain,
                exit_code=completed.returncode,
                stderr_tail=_tail(completed.stderr),
                stdout_tail=_tail(completed.stdout),
            )
        report_file = report_prefix.with_suffix(".json")
        if not report_file.is_file():
            raise HarvesterAdapterError(
                "harvester_report_missing",
                f"theHarvester 退出 0 但未产出 {report_file}(目标 {clean_domain})",
                domain=clean_domain,
                stdout_tail=_tail(completed.stdout),
            )
        try:
            report = json.loads(report_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise HarvesterAdapterError(
                "harvester_report_invalid",
                f"theHarvester 报告不可解析:{exc}",
                domain=clean_domain,
            ) from exc
        if not isinstance(report, dict):
            raise HarvesterAdapterError(
                "harvester_report_invalid",
                f"theHarvester 报告不是对象:{type(report).__name__}",
                domain=clean_domain,
            )
    results = {
        key: value for key, value in report.items() if isinstance(value, list)
    }
    result_totals = {key: len(value) for key, value in results.items()}
    return {
        "plugin": "myssia-theharvester",
        "target": clean_domain,
        "status": "success",
        "vendor": {
            "path": str(vendor),
            "commit": vendor_commit(root),
        },
        "command": command,
        "exit_code": completed.returncode,
        "duration_seconds": duration,
        "source_list": clean_sources,
        "results": results,
        "result_totals": result_totals,
    }
