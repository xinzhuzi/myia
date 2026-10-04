"""cron 执行体:spawn ``myia run --json`` 子进程 + 摘要投递 + 孤儿回收。

MYIA 移植重写自 Hermes(NousResearch/Hermes-Agent,MIT;上游路径
``~/.hermes/hermes-agent/cron/``):

- ``cron/scheduler.py`` ``_run_one_job_body`` H:3284 —— 执行主干。上游在
  调度进程内组装 agent 运行时;MYIA 的 job 载荷是品类 YAML 管线,执行体 =
  spawn ``myia run <yaml> --db <db> --json`` 子进程(偏离 D11:sidecar 从不
  进程内构造 Pipeline 是现状铁律,B14;runs 表/退出码语义/崩溃隔离天然获得)。
- ``cron/scheduler.py`` ``_submit_with_guard`` H:4239 / ``run_job`` H:2546 ——
  派发守卫与审计归 :mod:`myia.cron.tick`;``_FireOwnership`` H:2981 的 fire
  认领保活同归 tick 层(本模块只报告,宿主互斥/事件钩子语义见 design §3.3)。
- ``cron/scheduler.py`` H:3744 ``start_new_session=True`` —— 子进程自成进程
  组,超时/取消走 killpg 一锅端(冻结包 onefile 双进程漏孙进程的实证,
  desktop/entry.py run.start 同款范式 B14)。
- ``cron/jobs.py`` ``_job_output_dir`` H:423 / ``save_job_output`` H:3380 /
  ``_prune_job_output`` H:3358 —— 输出目录(路径逃逸拒收)、``<ts>.md``
  原子写、按文件名(时间戳)倒序裁剪留新。
- 不活跃看门狗(``HERMES_CRON_TIMEOUT``)不搬:子进程内活性宿主不可见,以
  ``run_timeout`` 墙钟 + killpg 等价实现资源护栏(偏离 D12);孤儿 adopt
  机器不搬——重启恢复时对遗留子进程 killpg + execution 终态化 ``unknown``
  (偏离 D14:slot 已消耗不重发,杀孤防与新 fire 并发写同 db)。

``--json`` 契约(cli.py ``_cmd_run``,B9):stdout 恰一份 JSON
(``RunResult.to_dict()``)、日志走 stderr、退出码 0=success / 1=config
error / 2=failed / 3=partial。job 语义映射(design §3.2 步骤 4):0=ok、
3=ok+partial 附注(记 ``summary.run.status="partial"``,不进
``last_error``)、其余(1/2/负值/超时/无法解析)= failed。
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Tuple

from myia.cron.executions import (
    _owner_is_live,  # noqa: SLF001 同包私有(属主存活判定的唯一纪律,不另写)
    pid_exists,
    process_start_time,
    start_time_fingerprints_match,
)
from myia.cron.jobs import (
    DEFAULT_RUN_TIMEOUT_SECONDS,
    _atomic_write_marker,  # noqa: SLF001 同包私有(tick 用 cron._now() 先例)
    resolve_failure_deliver,
)
from myia.cron.summary import (
    deliver_run_summary,
    render_failure_markdown,
    render_summary_markdown,
    summarize_run,
)

logger = logging.getLogger(__name__)

__all__ = [
    "DEFAULT_DB_NAME",
    "InflightContext",
    "OUTPUT_RETENTION_KEEP",
    "STDERR_TAIL_LINES",
    "TERMINATE_GRACE_SECONDS",
    "CronRunner",
    "SubprocessResult",
    "job_command",
    "job_db_path",
    "reap_orphaned_subprocesses",
    "run_subprocess",
    "self_command",
]

#: SIGTERM 后等子进程自清理的宽限,过时 SIGKILL 兜底(desktop/entry.py
#: ``_CANCEL_KILL_GRACE_SECONDS`` 同值同序:SIGTERM → 宽限 → SIGKILL)。
TERMINATE_GRACE_SECONDS = 5.0

#: SIGKILL 后的收尸等待(防御性:SIGKILL 后仍不退出的内核级楔死)。
KILL_REAP_SECONDS = 5.0

#: 失败告警携带的 stderr 尾部行数(design §5:细节留档 output 目录,告警有界)。
STDERR_TAIL_LINES = 8

#: 每 job 输出文档留存上限(上游 ``_CRON_OUTPUT_DEFAULT_KEEP`` 同值;
#: 文件名 = 时间戳,倒序裁剪留新)。
OUTPUT_RETENTION_KEEP = 50

#: 数据根缺省 db 名(tick ``DEFAULT_DB_NAME`` 同源;db_path 无覆写的 job 用它)。
DEFAULT_DB_NAME = "myia.db"

#: D14 在途子进程登记目录(``output/<job_id>/.inflight/<execution_id>.json``):
#: 宿主崩溃后重启恢复据此找到孤儿进程组;runner 正常收尾即删。
INFLIGHT_DIRNAME = ".inflight"

_ORPHAN_REASON = (
    "Host process died before this execution reached a terminal state; the "
    "orphaned pipeline subprocess was killed by startup recovery (killpg) and "
    "whether side effects completed is unknown."
)


@dataclass(frozen=True)
class SubprocessResult:
    """一次子进程 spawn 的全部观测(执行体决策的唯一输入面)。

    ``payload``:``RunResult.to_dict()``。真 spawn 恒 None——解析归
    :func:`_parse_run_payload`;测试替身可直接携带,免写 JSON 字符串。
    ``spawn_error``:无法 spawn / 收尸失败等结构化错误(非空 = failed)。
    ``pid``:子进程 pid(诊断/测试断言 killpg 效果;替身可缺省)。
    """

    exit_code: Optional[int]
    payload: Optional[dict[str, Any]] = None
    stdout_text: str = ""
    stderr_text: str = ""
    timed_out: bool = False
    spawn_error: Optional[str] = None
    pid: Optional[int] = None


@dataclass(frozen=True)
class InflightContext:
    """D14 在途登记上下文(spawn 成功即记 ``.inflight`` 标记,收尾即删)。"""

    store: Any
    job_id: str
    execution_id: str


#: 可注入子进程层(spawn 测试替身):签名同 :func:`run_subprocess`。
SpawnFn = Callable[..., SubprocessResult]

#: 可注入投递层(deliver 测试替身):签名同
#: :func:`myia.cron.summary.deliver_run_summary`(spec, markdown, job,
#: data_root, now 逐参传入)。
DeliverFn = Callable[..., Optional[str]]


# ---------------------------------------------------------------------------
# 自调命令与进程组杀(entry.py run.start 范式 B14)
# ---------------------------------------------------------------------------


def self_command(argv_tail: list[str]) -> tuple[list[str], dict[str, str]]:
    """构造等价 CLI 自调命令:冻结包直通 / dev 下 ``python -m myia.cli``。

    dev 下子进程未必装了 myia(conftest 靠 sys.path 注入 src/),以
    PYTHONPATH 指到 ``<repo>/src`` 保证可复现(desktop/entry.py
    ``_self_command`` 同款;冻结模式 PyInstaller 包自带全部模块)。
    """
    env = os.environ.copy()
    if getattr(sys, "frozen", False):
        return [sys.executable, *argv_tail], env
    src_root = Path(__file__).resolve().parents[2]  # <repo>/src
    env["PYTHONPATH"] = str(src_root) + os.pathsep + env.get("PYTHONPATH", "")
    return [sys.executable, "-m", "myia.cli", *argv_tail], env


def job_db_path(cron: Any, job: Mapping[str, Any]) -> Path:
    """job 的 db 路径:``db_path`` 覆写,缺省数据根 ``<data_root>/myia.db``
    (tick ``_job_db_key`` 同口径;~ 展开 + 绝对化)。"""
    override = job.get("db_path")
    if isinstance(override, str) and override.strip():
        return Path(os.path.abspath(os.path.expanduser(override.strip())))
    return Path(cron.store.data_root) / DEFAULT_DB_NAME


def job_command(cron: Any, job: Mapping[str, Any]) -> tuple[list[str], dict[str, str]]:
    """组装 ``myia run`` 子进程命令(design §3.2 步骤 1)。

    ``["run", category, "--db", db, "--json"]`` + 可选 ``--dry-run`` /
    ``--config``(job 可选键;cli.py ``_add_run_parser`` 参数面)。
    """
    argv = [
        "run",
        str(job.get("category") or ""),
        "--db",
        str(job_db_path(cron, job)),
        "--json",
    ]
    if job.get("dry_run"):
        argv.append("--dry-run")
    config = job.get("config_path")
    if isinstance(config, str) and config.strip():
        argv += ["--config", config.strip()]
    return self_command(argv)


def _signal_pid(pid: int, sig: int) -> None:
    """对 *pid* 发信号:**组长(pid == pgid)→ killpg 一锅端**(冻结包 onefile
    双进程,裸 kill 只杀 bootloader 漏采集孙进程);非组长(异常形态)→ 只杀
    本体,绝不误伤继承来的进程组(测试替身/外部残留的防御)。已收尸/权限
    边界静默——宽限兜底自然无事可做(entry.py ``_kill_group`` 同款吞法;
    Windows 无 killpg → AttributeError 一并吞,单进程杀兜底)。"""
    if pid <= 0:
        return
    try:
        pgid = os.getpgid(pid)
    except (ProcessLookupError, PermissionError, OSError, AttributeError):
        return
    try:
        if pgid == pid:
            os.killpg(pgid, sig)
        else:
            os.kill(pid, sig)
    except (ProcessLookupError, PermissionError, OSError, AttributeError):
        pass


def _terminate_process_tree(proc: subprocess.Popen, grace: float) -> None:
    """SIGTERM → 宽限 → SIGKILL(墙钟超时的资源护栏,D12)。"""
    _signal_pid(proc.pid, signal.SIGTERM)
    try:
        proc.wait(timeout=grace)
        return
    except subprocess.TimeoutExpired:
        pass
    _signal_pid(proc.pid, signal.SIGKILL)
    try:
        proc.wait(timeout=KILL_REAP_SECONDS)
    except subprocess.TimeoutExpired:  # pragma: no cover - 内核级楔死
        logger.error("Cron 子进程 SIGKILL 后仍未退出: pid=%s", proc.pid)


# ---------------------------------------------------------------------------
# 子进程层(spawn → 双流 → 墙钟超时;JSON 解析归执行体)
# ---------------------------------------------------------------------------


def _inflight_marker_path(store: Any, job_id: str, execution_id: str) -> Path:
    """在途标记路径(store 的 ``job_output_dir`` 自带路径逃逸拒收)。"""
    return store.job_output_dir(job_id) / INFLIGHT_DIRNAME / f"{execution_id}.json"


def _write_inflight_marker(
    store: Any, job_id: str, execution_id: str, proc: subprocess.Popen
) -> Path:
    """登记在途子进程(pid + 起始指纹):宿主崩溃后恢复期据此杀孤(D14)。"""
    marker = _inflight_marker_path(store, job_id, execution_id)
    record = {
        "execution_id": execution_id,
        "job_id": job_id,
        "pid": proc.pid,
        "process_start_time": process_start_time(proc.pid),
        "started_at": datetime.now().astimezone().isoformat(),
    }
    marker.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_marker(marker, json.dumps(record, ensure_ascii=False), ".inflight_")
    return marker


def _drop_inflight_marker(marker: Path) -> None:
    with contextlib.suppress(OSError):
        marker.unlink(missing_ok=True)


def run_subprocess(
    cmd: list[str],
    env: dict[str, str],
    *,
    timeout: float,
    inflight: Optional[InflightContext] = None,
) -> SubprocessResult:
    """spawn 子进程并收全双流;墙钟 *timeout* 到点 killpg(D12)。

    ``start_new_session=True``:子进程自成进程组——超时杀整组,不留采集
    孙进程孤儿。stdout/stderr 全量收齐后才返回(communicate 无死锁;超时
    路径二次 communicate 收残余)。*inflight* 在场时:spawn 成功即写 D14
    在途标记、任何收尾路径删除——宿主崩溃窗口内标记留盘,恢复期杀孤。
    """
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=True,
        )
    except OSError as exc:
        return SubprocessResult(
            exit_code=None,
            spawn_error=f"[spawn_failed] {type(exc).__name__}: {exc}",
        )
    marker: Optional[Path] = None
    if inflight is not None:
        try:
            marker = _write_inflight_marker(
                inflight.store, inflight.job_id, inflight.execution_id, proc
            )
        except Exception:  # noqa: BLE001 - 登记尽力而为,绝不拦执行
            logger.warning("Cron inflight marker write failed", exc_info=True)
    try:
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            logger.warning(
                "Cron 子进程墙钟超时(%ss),killpg 终止: pid=%s", timeout, proc.pid
            )
            _terminate_process_tree(proc, TERMINATE_GRACE_SECONDS)
            try:
                stdout, stderr = proc.communicate(timeout=KILL_REAP_SECONDS)
            except subprocess.TimeoutExpired:  # pragma: no cover - 楔死兜底
                stdout, stderr = "", ""
            return SubprocessResult(
                exit_code=proc.returncode,
                stdout_text=stdout or "",
                stderr_text=stderr or "",
                timed_out=True,
                pid=proc.pid,
            )
        return SubprocessResult(
            exit_code=proc.returncode,
            stdout_text=stdout or "",
            stderr_text=stderr or "",
            pid=proc.pid,
        )
    finally:
        if marker is not None:
            _drop_inflight_marker(marker)


def _parse_run_payload(result: SubprocessResult) -> Optional[dict[str, Any]]:
    """解析 stdout 的 ``RunResult.to_dict()``(``--json`` 契约:恰一份 JSON)。

    只在退出码 0/2/3(管线真跑过)时解析 stdout;替身直携 ``payload`` 的
    直接采信。形状守卫(``status``/``sources`` 键在场)把 config-error
    JSON(exit 1 的错误文档)挡在外面。解析失败 → None(调用方按 failed
    + 结构化错误处理),绝不部分采信。
    """
    if result.payload is not None:
        return result.payload
    if result.exit_code not in (0, 2, 3):
        return None
    text = result.stdout_text.strip()
    if not text:
        return None
    try:
        payload = json.loads(text)
    except ValueError:
        return None
    if (
        not isinstance(payload, dict)
        or "status" not in payload
        or "sources" not in payload
    ):
        return None
    return payload


def _run_error_text(result: SubprocessResult, payload: Optional[dict[str, Any]]) -> str:
    """failed 路径的结构化错误文本(优先级:spawn/超时/JSON 契约破裂 >
    RunResult 状态 > stderr 尾行 > 退出码)。"""
    if result.spawn_error:
        return result.spawn_error
    if result.timed_out:
        return "Pipeline subprocess timed out (run_timeout) and was killed by killpg."
    if result.exit_code in (0, 3) and payload is None:
        # 退出码说成功但 stdout 不是 RunResult JSON = --json 契约破裂
        # (design §3.2 步骤 4:无法解析 = failed,绝不静默当成功)。
        snippet = result.stdout_text.strip()[:200] or "(empty stdout)"
        return f"[run_json_invalid] stdout 不是可解析的 RunResult JSON: {snippet!r}"
    if isinstance(payload, Mapping):
        failed_sources = [
            str(s.get("source") or s.get("url") or "?")
            for s in (payload.get("sources") or [])
            if isinstance(s, Mapping) and s.get("failed")
        ]
        if payload.get("status") == "failed":
            return "Pipeline failed: all sources exhausted their engine chains."
        if failed_sources:
            return (
                f"Pipeline partial failure; failed sources: {', '.join(failed_sources)}"
            )
        failures = payload.get("failures")
        if isinstance(failures, list) and failures:
            return f"Pipeline reported {len(failures)} item-level failure(s)."
    tail = [line for line in result.stderr_text.splitlines() if line.strip()]
    if tail:
        return " | ".join(tail[-3:])
    return f"Pipeline subprocess exited with code {result.exit_code}."


# ---------------------------------------------------------------------------
# 输出文档(照抄 Hermes output 目录习惯;增 .log 与微秒戳防同秒碰撞)
# ---------------------------------------------------------------------------


def _prune_job_outputs(job_dir: Path, keep: int) -> int:
    """删最旧的 ``*.md``/``*.log`` 至 *keep* 个(文件名 = 时间戳,倒序 = 新先;
    上游 ``_prune_job_output`` 同款,失败吞——裁剪绝不弄崩执行体)。"""
    if keep <= 0:
        return 0
    deleted = 0
    for pattern in ("*.md", "*.log"):
        try:
            files = sorted(
                (f for f in job_dir.glob(pattern) if f.is_file()),
                key=lambda f: f.name,
                reverse=True,
            )
        except OSError:  # pragma: no cover - glob 失败吞
            continue
        for stale in files[keep:]:
            try:
                stale.unlink()
                deleted += 1
            except OSError as exc:
                logger.debug("Failed to prune cron output %s: %s", stale.name, exc)
    return deleted


def _stderr_tail(stderr_text: str) -> list[str]:
    """失败告警携带的 stderr 尾部行(去空行,尾部 N 行)。"""
    lines = [line.rstrip() for line in stderr_text.splitlines() if line.strip()]
    return lines[-STDERR_TAIL_LINES:]


# ---------------------------------------------------------------------------
# D14:孤儿回收(宿主崩溃遗留的子进程 → killpg + execution 终态化 unknown)
# ---------------------------------------------------------------------------


def _kill_orphan_group(pid: int, recorded_start: Any, *, grace: float) -> bool:
    """杀孤儿进程组(先验指纹防 PID 复用误杀;组长校验防误伤继承组)。

    Returns:
        True = 确认发了杀信号(SIGTERM,必要时 SIGKILL 兜底;不保证已收尸)。
    """
    if pid <= 0 or not pid_exists(pid):
        return False
    if recorded_start is not None:
        current = process_start_time(pid)
        if current is not None and not start_time_fingerprints_match(
            float(recorded_start), current
        ):
            logger.warning(
                "Cron orphan pid %s fingerprint mismatch (PID recycled?) — not killing",
                pid,
            )
            return False
    _signal_pid(pid, signal.SIGTERM)
    deadline = time.monotonic() + grace
    while time.monotonic() < deadline:
        if not pid_exists(pid):
            return True
        time.sleep(0.1)
    _signal_pid(pid, signal.SIGKILL)
    return True


def reap_orphaned_subprocesses(cron: Any) -> int:
    """D14:宿主崩溃遗留的孤儿子进程——killpg + execution 终态化 ``unknown``。

    扫 ``output/*/.inflight/*.json`` 登记项,逐条判定:

    - 属主仍活(账本行 pid+指纹存活)→ **跳过**:活属主的 runner 自己收
      (绝不止血别人的在途 run);
    - 属主死/行缺失 → 指纹核对后杀进程组(SIGTERM→宽限→SIGKILL;指纹不符
      = PID 已被复用,只清登记绝不误杀),账本行仍在 claimed/running 则
      ``terminalize_dead_owner`` 落 ``unknown``(副作用是否已跑未知);
    - 行已终态 → 仍杀孤儿清登记(启动恢复可能已先行把行标 unknown,孤儿
      本身要杀——防与新 fire 并发写同 db,D14 的杀孤独立于记账)。

    尽力而为:单条失败只告警,绝不抛(tick 的 reap 步骤吞一切)。
    """
    store = cron.store
    reaped = 0
    try:
        markers = sorted(store.output_dir.glob(f"*/{INFLIGHT_DIRNAME}/*.json"))
    except OSError:  # pragma: no cover - 目录不可读
        return 0
    for marker in markers:
        try:
            record = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _drop_inflight_marker(marker)  # 坏登记:清掉,不留永久噪声
            continue
        execution_id = str(record.get("execution_id") or marker.stem)
        try:
            row = cron.ledger.get_execution(execution_id)
        except Exception:  # noqa: BLE001 - 账本不可读按行缺失处理
            row = None
        if row is not None and _owner_is_live(
            int(row["pid"]), row.get("process_start_time")
        ):
            continue  # 活属主在途:不越权
        try:
            killed = _kill_orphan_group(
                int(record.get("pid") or 0),
                record.get("process_start_time"),
                grace=TERMINATE_GRACE_SECONDS,
            )
        except Exception as exc:  # noqa: BLE001 - 单孤儿失败不拖垮回收
            logger.warning("Cron orphan kill failed for %s: %s", marker, exc)
            killed = False
        terminalized = False
        if row is not None and row.get("status") in ("claimed", "running"):
            try:
                terminalized = bool(
                    cron.ledger.terminalize_dead_owner(
                        execution_id, reason=_ORPHAN_REASON
                    )
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Cron orphan execution terminalize failed for %s: %s",
                    execution_id,
                    exc,
                )
        _drop_inflight_marker(marker)
        reaped += 1
        logger.warning(
            "Reaped orphaned cron execution %s (job %s): killed=%s terminalized=%s",
            execution_id,
            record.get("job_id"),
            killed,
            terminalized,
        )
    return reaped


# ---------------------------------------------------------------------------
# 执行体(design §3.2 步骤 1-6;JobRunner 协议形态归 tick 派发)
# ---------------------------------------------------------------------------


class CronRunner:
    """一个数据根的 cron 执行体(tick 派发回调注入形态)。

    Args:
        cron: :class:`~myia.cron.jobs.CronJobs` 门面(存储/账本/注入时钟同根)。
        spawn: 子进程层替身(:func:`run_subprocess` 缺省);测试注入 mock
            子进程失败/超时/携带 payload。
        deliverer: 投递层替身(:func:`myia.cron.summary.deliver_run_summary`
            缺省);测试注入 RecordingChannel 形态。

    契约冻结(implement B1)::meth:`execute` 即 :data:`myia.cron.tick.JobRunner`
    协议——入参派发快照(含 ``execution_id``/``_scheduled_instant``),返回
    ``(success, error, delivery_error)`` 三元组;``skipped_busy`` 语义在 tick
    的 ``dispatch_gate`` 注入,本层只报告(design §3.3)。
    """

    def __init__(
        self,
        cron: Any,
        *,
        spawn: Optional[SpawnFn] = None,
        deliverer: Optional[DeliverFn] = None,
    ) -> None:
        self.cron = cron
        self._spawn = spawn or run_subprocess
        self._deliverer = deliverer or deliver_run_summary

    # -- 内部 ---------------------------------------------------------------

    def _run_timeout(self, job: Mapping[str, Any]) -> float:
        """墙钟超时秒:job ``run_timeout`` 覆写,缺省 3600(D12)。"""
        try:
            timeout = float(job.get("run_timeout") or DEFAULT_RUN_TIMEOUT_SECONDS)
        except (TypeError, ValueError):
            timeout = DEFAULT_RUN_TIMEOUT_SECONDS
        return timeout if timeout > 0 else DEFAULT_RUN_TIMEOUT_SECONDS

    def _write_run_document(
        self,
        job: Mapping[str, Any],
        *,
        summary: dict[str, Any],
        markdown: str,
        stderr_text: str,
        cmd: list[str],
    ) -> Path:
        """输出落 ``output/<job_id>/<ts>.md``(+ stderr ``.log``)并裁剪
        (design §3.2 步骤 6;Hermes save_job_output 习惯)。返回文档路径
        (失败告警指路用)。"""
        store = self.cron.store
        job_id = str(job.get("id") or "unknown")
        job_dir = store.job_output_dir(job_id)
        job_dir.mkdir(parents=True, exist_ok=True)
        stamp = self.cron._now().strftime(  # noqa: SLF001 同包私有(注入时钟口径)
            "%Y-%m-%d_%H-%M-%S_%f"
        )
        document = job_dir / f"{stamp}.md"
        header = [
            f"# cron run {job.get('name') or job_id}",
            "",
            f"- command: `{' '.join(cmd)}`",
            f"- exit: {summary['run']['exit_code']!r}  status: {summary['run']['status']}",
            "",
            markdown,
            "",
            "```json",
            json.dumps(summary, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
        _atomic_write_marker(document, "\n".join(header), ".output_")
        if stderr_text.strip():
            _atomic_write_marker(job_dir / f"{stamp}.log", stderr_text, ".output_")
        _prune_job_outputs(job_dir, OUTPUT_RETENTION_KEEP)
        return document

    def _record_execution_summary(
        self,
        execution_id: str,
        *,
        success: bool,
        error: Optional[str],
        summary: dict[str, Any],
    ) -> None:
        """D10:摘要快照随终态入账本(公开 API ``finish_execution``;tick 随后
        的 best-effort finish 对已终态行返回 None,零冲突)。"""
        try:
            self.cron.ledger.finish_execution(
                execution_id, success=success, error=error, run_summary=summary
            )
        except Exception:
            logger.warning(
                "Failed to record run summary on execution %s",
                execution_id,
                exc_info=True,
            )

    # -- 主入口 -------------------------------------------------------------

    def execute(self, job: dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
        """跑一个 job:spawn → 退出码映射 → 摘要 → 落盘 → 投递(design §3.2)。

        Returns:
            ``(success, error, delivery_error)``:success 只反映**运行**成败
            (exit 0/3 = True);delivery_error 分立才有
            ``last_status="delivery_failed"`` 三态(F1.7,投递失败不动 streak)。
        """
        job_id = str(job.get("id") or "")
        label = job.get("name") or job_id
        execution_id = str(job.get("execution_id") or "") or None
        cmd, env = job_command(self.cron, job)
        logger.info("Cron job '%s' spawning: %s", label, " ".join(cmd))

        inflight = (
            InflightContext(self.cron.store, job_id, execution_id)
            if (execution_id and job_id)
            else None
        )
        result = self._spawn(
            cmd, env, timeout=self._run_timeout(job), inflight=inflight
        )
        payload = _parse_run_payload(result)
        success = (
            not result.timed_out
            and result.spawn_error is None
            and result.exit_code in (0, 3)
            and payload is not None
        )
        error: Optional[str] = None if success else _run_error_text(result, payload)

        summary = summarize_run(
            job,
            payload=payload,
            exit_code=result.exit_code,
            timed_out=result.timed_out,
            error=error,
        )
        stderr_tail = _stderr_tail(result.stderr_text)
        document = self._write_run_document(
            job,
            summary=summary,
            markdown=(
                render_summary_markdown(summary)
                if success
                else render_failure_markdown(summary, stderr_tail=stderr_tail)
            ),
            stderr_text=result.stderr_text,
            cmd=cmd,
        )

        if execution_id:
            self._record_execution_summary(
                execution_id, success=success, error=error, summary=summary
            )

        # 摘要投递(§3.2 步骤 5):成功走 deliver,失败走 failure_deliver
        # (缺省回落 deliver、显式 none 关闭,§8.1);"local"/空由投递层吸收
        # (本地落盘即上面的输出文档,D4)。投递失败只记 delivery_error,
        # 绝不翻转运行成败(F1.7)。
        data_root = Path(self.cron.store.data_root)
        now = self.cron._now()  # noqa: SLF001 同包私有(注入时钟口径)
        delivery_error: Optional[str] = None
        if success:
            delivery_error = self._deliverer(
                str(job.get("deliver") or "local"),
                render_summary_markdown(summary),
                job=job,
                data_root=data_root,
                now=now,
            )
        else:
            failure_spec = resolve_failure_deliver(dict(job))
            if failure_spec:
                delivery_error = self._deliverer(
                    failure_spec,
                    render_failure_markdown(
                        summary, stderr_tail=stderr_tail, output_path=document
                    ),
                    job=job,
                    data_root=data_root,
                    now=now,
                )

        status_text = summary["run"]["status"]
        if delivery_error:
            logger.error(
                "Cron job '%s' run %s but delivery failed: %s",
                label,
                status_text,
                delivery_error,
            )
        else:
            logger.info("Cron job '%s' finished: %s", label, status_text)
        return success, error, delivery_error
