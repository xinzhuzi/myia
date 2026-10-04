"""Cron job 注册表存储:``<data_root>/cron/jobs.json``(原子写 + 跨进程建议锁)。

上游蓝本:``~/.hermes/hermes-agent/cron/jobs.py`` 存储段(L115-631 路径/锁/规整、
L1355-1673 解析/装载/合并/落盘),原子写原语按 hermes-agent ``utils.py``
L167-251(``atomic_replace``/``mkstemp_beside``/``fsync_directory``)等价重写。
NousResearch/Hermes-Agent,MIT——逐段对照重写为 MYIA 风格,非整块拷贝。

MYIA 适配(10-04-hermes-cron design §1/§6,非照抄处仅此):

- **数据根** = ``Path(db_path).parent``(ground-truth A6,``pipeline.py:858``
  ``ChannelDirectory`` 同款先例);cron 目录 = ``<data_root>/cron``,首跑自建。
  替代 Hermes 的 profile home + ``use_cron_store()`` ContextVar 覆盖机器
  (per-profile 隔离是 Hermes 专属物,D8);MYIA 用显式 ``CronJobStore(data_root)``
  实例替代模块级全局路径。
- **不搬**:_preserve_file_ownership(gateway/CLI 双用户部署形态,MYIA 单用户,
  上游 #68483 场景不存在)、fire fence / self_removal_delivery 族(jobs.py 生命周期
  批的域)、心跳标记文件族(同上)、croniter 惰性导入(D1:CronTrigger 随核心依赖
  常在)。
- job 记录字段按 design §2.1:载荷 = ``category``(D2,prompt/skills 族不搬),
  规整函数的 name 回退链相应取 category 文件名。

锁语义照抄:写者持锁期间全量重写;另一进程磁盘新增的未知 job 记录合并不覆盖
(上游 #80624);无 flock 后端或 flock 超时降级为仅进程内锁(短暂撕裂胜过死调度器)。
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Collection, Iterator, Optional, Union

# 跨进程建议锁双平台:fcntl(Unix)/ msvcrt(Windows)。两者皆缺时 _acquire_flock
# 返回 None,_jobs_lock 退化为仅进程内锁而不是失败(上游 jobs.py L18-27 注释头)。
try:
    import fcntl  # noqa: F401  (可能缺,保名字存在)
except ImportError:  # pragma: no cover - non-Unix
    fcntl = None  # type: ignore[assignment]
try:
    import msvcrt  # type: ignore[import-not-found]  # noqa: F401
except ImportError:  # pragma: no cover - non-Windows
    msvcrt = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

# 跨进程 .jobs.lock 的等待上限:每个 cron 函数都过 jobs_lock(),对卡死同胞进程
# 无限阻塞会冻结整个 ticker;30s 远高于任何合法临界区、又低于一条状态告警阈值
# (上游 L106-109)。
JOBS_LOCK_TIMEOUT_SECONDS = 30.0

# 落盘前 shrink-merge 循环的最多重试轮次(verify-after-stage;上游 L1564)。
SAVE_MERGE_ATTEMPTS = 5

# job 记录的终态集合(effective_job_state/is_terminal_job 消费;design §2.1
# state ∈ scheduled|paused|completed|error)。
TERMINAL_JOB_STATES = frozenset({"completed", "error"})


def _now_iso() -> str:
    """aware 本地 ISO 时间戳(与上游 hermes_time.now 缺省行为同:本地时区带偏移)。"""
    return datetime.now().astimezone().isoformat()


def _coerce_text(value: Any, fallback: str = "") -> str:
    """遗留/手编的可空字段规整为字符串(读取方永不因 None 崩溃;上游 L460)。"""
    return fallback if value is None else str(value)


# --- 记录规整(纯函数,存储不触碰;上游 L460-573 照抄,D2 换载荷) -------------


def schedule_display_for_job(job: dict[str, Any]) -> str:
    """schedule 展示文案:显式 schedule_display > schedule dict 的
    display/expr/run_at > 原值字符串 > "?"(上游 _schedule_display_for_job L489)。"""
    display = _coerce_text(job.get("schedule_display")).strip()
    if display:
        return display
    schedule = job.get("schedule")
    if isinstance(schedule, dict):
        for key in ("display", "expr", "run_at"):
            text = _coerce_text(schedule.get(key)).strip()
            if text:
                return text
    elif schedule is not None:
        return str(schedule)
    return "?"


def _has_pause_marker(job: dict[str, Any]) -> bool:
    """记录上是否存在任何面向操作者的暂停信号(state=paused 或 paused_at;上游 L528)。"""
    return _coerce_text(job.get("state")).strip() == "paused" or bool(job.get("paused_at"))


def effective_job_state(job: dict[str, Any]) -> str:
    """由 ``enabled`` 推导的操作者视角 state:enabled job 绝不显示为 paused
    (列表看似冻结而 job 仍在发);终态无条件保留(上游 L539-552)。"""
    stored = _coerce_text(job.get("state")).strip()
    if stored in TERMINAL_JOB_STATES:
        return stored
    if not job.get("enabled", True):
        if _has_pause_marker(job) or stored == "paused":
            return "paused"
        return stored or "paused"
    # enabled=true 是权威:绝不宣称 paused
    if stored == "paused" or job.get("paused_at"):
        return "scheduled"
    return stored or "scheduled"


def is_job_runnable(job: dict[str, Any]) -> bool:
    """调度器是否可发此 job:``enabled`` 加暂停信号双闸——半暂停的自相矛盾记录
    在自愈跑之前也不许发(上游 L533)。"""
    return bool(job.get("enabled", True)) and not _has_pause_marker(job)


def is_terminal_job(job: dict[str, Any]) -> bool:
    """job 记录是否处于终态调度状态(上游 L555)。"""
    return job.get("state") in TERMINAL_JOB_STATES


def is_recoverable_error_job(job: dict[str, Any]) -> bool:
    """recurring job 卡在 ``state=error``(仅当 compute_next_run 失败时置入)是否可恢复:
    这类 job 在底层问题解决后仍有未来到期,当终态处理会永远堵死 due-scan 自愈与
    resume(上游 #16265,L560)。once 的 completed 是真终态,不在此列。"""
    return (
        job.get("state") == "error"
        and (job.get("schedule") or {}).get("kind") in {"cron", "interval"}
    )


def normalize_job_record(job: dict[str, Any]) -> dict[str, Any]:
    """读取安全的 job 形状:遗留/手编记录的 name/schedule_display/state 可能缺省,
    规整让消费者在格式化时永不崩(存储不动,返回新 dict;上游
    _normalize_job_record L504,D2:name 回退链取 category 文件名)。"""
    normalized = dict(job)
    job_id = normalized["id"] = _coerce_text(normalized.get("id"), "unknown")
    category = _coerce_text(normalized.get("category")).strip()
    name = _coerce_text(normalized.get("name")).strip()
    if not name:
        label_source = (
            Path(category).name
            if category
            else ""
        ) or job_id or "cron job"
        name = label_source[:50].strip() or "cron job"
    normalized["name"] = name
    normalized["schedule_display"] = schedule_display_for_job(normalized)
    # 从调度器实际尊重的 ``enabled`` 推导,半暂停记录不可能一边显示 paused
    # 一边继续发(上游注释 L522)。
    normalized["state"] = effective_job_state(normalized)
    return normalized


# --- 原子写原语(hermes-agent utils.py L167-251 等价重写,MYIA 简化点:-------
# --- jobs.json 与 tmp 同目录同文件系统,无符号链接改写与 EXDEV 回退需求)-----


def _fsync_directory(path: Path) -> None:
    """尽力而为的目录项 fsync,让刚 rename 落位的文件扛住断电;Windows 开不了
    目录 fd(文件级 fsync 已生效)、任何 OSError 吞掉——目录项持久性永远不值得
    让一次已就位的写失败(上游 L234)。"""
    if os.name == "nt":
        return
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    except OSError:
        return
    try:
        with contextlib.suppress(OSError):
            os.fsync(fd)
    finally:
        os.close(fd)


def _secure_dir(path: Path) -> None:
    """目录收权 0700(best-effort;上游经共享助手套 managed/container 规则,MYIA
    无该形态,直接尽力 chmod)。"""
    if os.name == "nt":
        return
    with contextlib.suppress(OSError):
        path.chmod(0o700)


def _secure_file(path: Path) -> None:
    """文件收权 0600(best-effort,同上)。"""
    if os.name == "nt":
        return
    with contextlib.suppress(OSError):
        path.chmod(0o600)


def _mkstemp_beside(target: Path, **kwargs: Any) -> tuple[int, str]:
    """在 target 同目录开 mkstemp:tmp 与最终 rename 目标同文件系统,发布 rename
    才是原子的(上游 mkstemp_beside L214 的同目录保证)。"""
    return tempfile.mkstemp(dir=str(target.parent), **kwargs)


# --- 跨进程建议锁(上游 L251-336 照抄)---------------------------------------


def _acquire_flock(lock_fd: Any, timeout: float) -> Optional[bool]:
    """有界独占锁:True=已拿到 / False=超时 / None=无后端。已持进程内锁时再阻塞
    flock(LOCK_EX) 会让一个卡死的同胞进程冻结所有 cron 函数,所以拿 LOCK_NB
    轮询到期限为止;降级模式由调用方定(上游 L251)。"""
    if fcntl is not None:
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return True
            except (OSError, IOError):
                if time.monotonic() >= deadline:
                    return False
                time.sleep(0.1)
    if msvcrt is not None:
        getattr(msvcrt, "locking")(lock_fd.fileno(), getattr(msvcrt, "LK_LOCK"), 1)
        return True
    return None


def _release_flock(lock_fd: Any) -> None:
    """解锁(尽力)并关锁文件(上游 L272)。"""
    try:
        if fcntl is not None:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        elif msvcrt is not None:
            getattr(msvcrt, "locking")(lock_fd.fileno(), getattr(msvcrt, "LK_UNLCK"), 1)
    except (OSError, IOError):
        pass
    finally:
        lock_fd.close()


class CronJobStore:
    """一个数据根的 cron job 注册表(``<data_root>/cron/jobs.json``)。

    Args:
        data_root: 数据根目录(db 路径的父目录;``pipeline.py:858`` 先例)。
            cron 目录 ``<data_root>/cron`` 与输出目录 ``<data_root>/cron/output``
            首次写前自建(:meth:`ensure_dirs`)。

    契约冻结(10-04-hermes-cron implement A2):``jobs.py``(生命周期批)经本类
    原语读写 jobs.json,接口形状不得擅改。
    """

    def __init__(self, data_root: Union[str, Path]) -> None:
        self.data_root = Path(data_root)
        self.cron_dir = self.data_root / "cron"
        self.jobs_file = self.cron_dir / "jobs.json"
        self.output_dir = self.cron_dir / "output"
        # 进程内锁:load_jobs→改→save_jobs 临界区串行(并行 tick 线程的
        # mark_job_run / advance_next_runs 互踩;上游 L98-104)。
        self._file_lock = threading.RLock()
        self._lock_state = threading.local()

    @classmethod
    def for_db(cls, db_path: Union[str, Path]) -> "CronJobStore":
        """从 myia.db 路径定位存储(数据根 = db 父目录,A6;CLI 传 ``--db`` 即得)。"""
        return cls(Path(db_path).parent)

    @property
    def jobs_lock_file(self) -> Path:
        """跨进程建议锁文件路径(``<cron_dir>/.jobs.lock``)。"""
        return self.cron_dir / ".jobs.lock"

    def ensure_dirs(self) -> None:
        """建 cron 目录与输出目录并收权(上游 ensure_dirs L631;无 profile 形态,
        parents=True 首跑可用)。"""
        self.cron_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        _secure_dir(self.cron_dir)
        _secure_dir(self.output_dir)

    def job_output_dir(self, job_id: str) -> Path:
        """job 输出目录,拒绝任何路径逃逸(``..``/绝对路径/分隔符):id 是
        OUTPUT_DIR 下的路径成分,放任更新可把 ``../escape`` 泄进输出写/删
        (上游 _job_output_dir L423)。"""
        text = str(job_id or "").strip()
        if (
            not text or text in {".", ".."} or "/" in text or "\\" in text
            or Path(text).is_absolute() or Path(text).drive
        ):
            raise ValueError(f"Invalid cron job id for output path: {job_id!r}")
        return self.output_dir / text

    # --- 锁(上游 _jobs_lock L285-336 照抄,状态改挂实例) -------------------

    @contextlib.contextmanager
    def jobs_lock(self) -> Iterator[None]:
        """串行化一个 load_jobs→改→save_jobs 临界区:进程内 RLock(并行 tick
        线程)+ 跨进程 flock(``<cron_dir>/.jobs.lock``,serve 与 CLI 写互斥——
        否则一条 ``cron pause`` 可能被覆写而继续发)。同线程嵌套复用已持锁。
        无 flock 后端、或 flock 超时(大声记日志)时降级为仅进程内锁:短暂撕裂
        的跨进程写胜过死掉的调度器。"""
        depth = getattr(self._lock_state, "depth", 0)
        if depth:
            self._lock_state.depth = depth + 1
            try:
                yield
            finally:
                self._lock_state.depth -= 1
            return

        with self._file_lock:
            self._lock_state.depth = 1
            # 本临界区 load_jobs() 时的 jobs.json 戳:让 _save_jobs_unlocked 在
            # 文件可证未变时跳过 shrink-merge 解析。进出重置,锁外加载或上一
            # 临界区的陈旧戳永远不可能压掉一次需要的合并(上游 #80703)。
            self._lock_state.load_stamp = None
            lock_fd = None
            try:
                try:
                    self.ensure_dirs()
                    lock_fd = open(self.jobs_lock_file, "a+")
                    lock_fd.seek(0)
                    if _acquire_flock(lock_fd, JOBS_LOCK_TIMEOUT_SECONDS) is False:
                        logger.error(
                            "Timed out after %.0fs waiting for the cron jobs lock "
                            "(%s) — another process is holding it. Proceeding with "
                            "in-process locking only so the scheduler stays alive.",
                            JOBS_LOCK_TIMEOUT_SECONDS, self.jobs_lock_file,
                        )
                        with contextlib.suppress(OSError):
                            lock_fd.close()
                        lock_fd = None
                except (OSError, IOError) as e:
                    # 锁失败绝不许拖垮 cron 写——进程内锁仍持有。
                    logger.warning(
                        "jobs.json cross-process lock unavailable (%s); "
                        "proceeding with in-process lock only", e)
                try:
                    yield
                finally:
                    if lock_fd is not None:
                        _release_flock(lock_fd)
            finally:
                self._lock_state.depth = 0
                self._lock_state.load_stamp = None

    # --- 读(上游 L1355-1456 照抄)-----------------------------------------

    def _parse_jobs_file(self) -> tuple[Any, bool]:
        """容错解析 jobs.json → ``(data, used_strict_fallback)``:utf-8-sig 吸收
        BOM,严格失败换 ``strict=False`` 重试。IO/回退错误向上抛(调用方决定修复
        还是放弃)。"""
        with open(self.jobs_file, "r", encoding="utf-8-sig") as f:
            raw = f.read()
        try:
            return json.loads(raw), False
        except json.JSONDecodeError:
            return json.loads(raw, strict=False), True

    def _peek_jobs_unlocked(self) -> Optional[list[dict[str, Any]]]:
        """``jobs_lock()`` 内的无修复读:缺失 → ``[]``,损坏 → ``None``(绝不对着
        未知基线做 shrink-merge)。绝不保存——那会递归。"""
        if not self.jobs_file.exists():
            return []
        try:
            data, _ = self._parse_jobs_file()
        except Exception:
            return None
        if isinstance(data, dict):
            jobs = data.get("jobs", [])
            return jobs if isinstance(jobs, list) else None
        return data if isinstance(data, list) else None

    def _jobs_file_stamp(self) -> Optional[tuple[int, int, int]]:
        """shrink-merge 快路径戳 ``(mtime_ns, size, ino)``;stat 不到 → None。
        含 st_ino 是因为每个写者都是 mkstemp+rename,同一 mtime 量子内的同尺寸
        写不可能假匹配。"""
        try:
            st = self.jobs_file.stat()
            return (st.st_mtime_ns, st.st_size, st.st_ino)
        except OSError:
            return None

    def _record_load_stamp(self, stamp: Optional[tuple[int, int, int]]) -> None:
        """把 jobs.json 的戳记给所在 jobs_lock() 临界区(锁外无效操作)。读**前**
        取戳:读中途落地的同胞写会戳不匹配(fail-safe);读后取戳会把一次没看
        到的写错误地认证为已见(上游 #80703)。"""
        if getattr(self._lock_state, "depth", 0):
            self._lock_state.load_stamp = stamp

    def load_jobs(self) -> list[dict[str, Any]]:
        """从存储读全部 job(含损坏自修复;上游 L1367-1456 照抄)。"""
        self.ensure_dirs()
        # 读前取戳(见 _record_load_stamp)。
        pre_read_stamp = self._jobs_file_stamp()
        if not self.jobs_file.exists():
            self._record_load_stamp(None)
            return []

        try:
            data, _strict_retry = self._parse_jobs_file()
        except IOError as e:
            logger.error("IOError reading jobs.json: %s", e)
            raise RuntimeError(f"Failed to read cron database: {e}") from e
        except Exception as e:
            logger.error("Failed to auto-repair jobs.json: %s", e)
            raise RuntimeError(f"Cron database corrupted and unrepairable: {e}") from e

        # 接受规范 dict 或裸列表(自动修复);其他顶层形状即损坏。修复细节只由
        # 持锁那一轮记日志(锁外那轮会在下面锁内重跑),每次修复告警只发一次。
        repair: Optional[str] = "had invalid control characters" if _strict_retry else None
        notes: list[str] = []
        unmergeable = False  # 磁盘形状 _peek_jobs_unlocked 读不了:只有 replace 落盘能治
        if isinstance(data, dict):
            jobs = data.get("jobs", [])
            if isinstance(jobs, dict):
                # 外部工具写的 id 键映射:拍平(内联 "id" 优先,否则取键),跳过垃圾。
                # _peek_jobs_unlocked 故意不拍平,合并型落盘会拒绝此形状;
                # 下面的修复以 replace=True 重写。
                skipped = [k for k, v in jobs.items() if not isinstance(v, dict)]
                if skipped:
                    notes.append("Skipping %d non-dict entr%s in id-keyed jobs map: %s" % (
                        len(skipped), "y" if len(skipped) == 1 else "ies",
                        ", ".join(map(repr, skipped))))
                jobs = [{**v, "id": v.get("id") or k} for k, v in jobs.items() if isinstance(v, dict)]
                repair = "id-keyed jobs map flattened to list"
                unmergeable = True
            elif not isinstance(jobs, list):
                notes.append("Replacing invalid jobs.json 'jobs' field (%s) with an empty list"
                             % type(jobs).__name__)
                jobs = []
                repair = "invalid jobs field replaced with list"
                unmergeable = True
        elif isinstance(data, list):
            jobs = data
            repair = "bare list wrapped as dict"
        else:
            raise RuntimeError(
                f"Cron database corrupted: expected {{'jobs': [...]}}, got {type(data).__name__}")
        junk = [j for j in jobs if not isinstance(j, dict)]
        if junk:
            # 每个读方和 due 扫描索引都按 dict 记:一条垃圾会崩整个 tick、冻住所有
            # 健康 sibling job,所以像 id 键映射一样跳过。只报类型:原始值是任意
            # 文件内容,不许进日志。
            notes.append("Skipping %d non-object entr%s in jobs.json (types: %s)" % (
                len(junk), "y" if len(junk) == 1 else "ies",
                ", ".join(sorted({type(j).__name__ for j in junk}))))
            jobs = [j for j in jobs if isinstance(j, dict)]
            repair = repair or "non-object entries dropped"
        for job in jobs:
            # 手编的 "completed" 不是非负 int(null、"2"、1.0、-5、Infinity)会崩掉
            # 所有计数读方(None += 1、"2"+1)、渲染成 "None/3" / "2.0/3"、或白送
            # 额外运行;在此一次性规整,读方即可信任非负 int。OverflowError:
            # json.loads 把 Infinity / 1e999 变成 float inf,int(inf) 会抛。
            rep = job.get("repeat")
            if isinstance(rep, dict) and "completed" in rep and (
                    type(rep["completed"]) is not int or rep["completed"] < 0):
                try:
                    rep["completed"] = max(int(rep["completed"]), 0)
                except (TypeError, ValueError, OverflowError):
                    rep["completed"] = 0
                repair = repair or "invalid repeat.completed normalized"
        # 即使空结果也落盘,否则全垃圾存储会每 tick 重复修复。
        if repair:
            if not getattr(self._lock_state, "depth", 0):
                # 锁外快照可能早于锁内写者对它已持有 job 的更新(shrink-merge 只
                # 恢复缺失 id),所以锁内重读重修。
                with self.jobs_lock():
                    return self.load_jobs()
            for note in notes:
                logger.warning("%s", note)
            # 保留 shrink-merge(降级锁同胞的 create 可能已在我们读后落地),除非
            # 磁盘仍是合并会拒绝的形状:同胞可能已重写它。
            self.save_jobs(jobs, replace=unmergeable and self._peek_jobs_unlocked() is None)
            logger.warning("Auto-repaired jobs.json (%s)", repair)
        self._record_load_stamp(pre_read_stamp)
        return jobs

    # --- 写(上游 L1499-1620 照抄)-----------------------------------------

    def _unmerged_disk_jobs(
        self, jobs: list[dict[str, Any]], removed_ids: Optional[Collection[str]],
    ) -> list[dict[str, Any]]:
        """在磁盘上、却不在 *jobs* 里、且非有意删除的 job。戳匹配 ⇒ 什么都没落,
        不解析直接回;读不了的存储 ⇒ RuntimeError(fail closed:对着未知基线写
        会静默丢掉里面每一个 job)。"""
        stamp = getattr(self._lock_state, "load_stamp", None)
        if stamp is not None and self._jobs_file_stamp() == stamp:
            return []
        disk_jobs = self._peek_jobs_unlocked()
        if disk_jobs is None:
            raise RuntimeError(
                f"Cron database corrupted; refusing to overwrite {self.jobs_file}")
        seen = {str(j["id"]) for j in jobs if isinstance(j, dict) and j.get("id")}
        seen |= {str(i) for i in (removed_ids or ()) if i}
        recovered: list[dict[str, Any]] = []
        for disk_job in disk_jobs:
            if not isinstance(disk_job, dict) or not disk_job.get("id"):
                continue
            disk_id = str(disk_job["id"])
            if disk_id not in seen:
                recovered.append(disk_job)
                seen.add(disk_id)
        return recovered

    def _merge_unexpected_disk_jobs(
        self, jobs: list[dict[str, Any]], *, removed_ids: Optional[Collection[str]] = None,
    ) -> list[dict[str, Any]]:
        """*jobs* 加上磁盘上有、载荷里缺的 job(降级 flock 超时路径下,陈旧写者
        否则会碾掉并发 create)。删除方传 ``removed_ids``;绝不改动 *jobs*。"""
        recovered = self._unmerged_disk_jobs(jobs, removed_ids)
        if not recovered:
            return jobs
        logger.warning(
            "Preserved %d cron job(s) present on disk but missing from the "
            "in-memory save payload (concurrent create under degraded lock "
            "or stale writer): %s",
            len(recovered), [j.get("id") for j in recovered])
        return jobs + recovered

    def _stage_jobs_payload(self, jobs: list[dict[str, Any]]) -> str:
        """把存储载荷序列化进 jobs_file 旁一个已 fsync 的临时文件;返回其路径。"""
        fd, tmp_path = _mkstemp_beside(self.jobs_file, suffix=".tmp", prefix=".jobs_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(
                    {"jobs": jobs, "updated_at": _now_iso()},
                    f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
        except BaseException:
            _unlink_quiet(tmp_path)
            raise
        return tmp_path

    def _save_jobs_unlocked(
        self, jobs: list[dict[str, Any]], *,
        removed_ids: Optional[Collection[str]] = None, replace: bool = False,
    ) -> None:
        """落盘全部 job;调用方必须已持 jobs_lock()。``removed_ids`` = 有意删除;
        ``replace=True`` 跳过 shrink-merge 守卫与损坏存储拒绝(测试、灾难恢复、
        load_jobs 对不可合并形状的自动修复用的整体重写)。"""
        self.ensure_dirs()
        # shrink-merge 循环:合并、staging、再 peek、重试;最后一轮不 re-peek 直写。
        tmp_path: Optional[str] = None
        try:
            for attempt in range(SAVE_MERGE_ATTEMPTS + 1):
                if not replace:
                    jobs = self._merge_unexpected_disk_jobs(jobs, removed_ids=removed_ids)
                tmp_path = self._stage_jobs_payload(jobs)
                # stage 后校验:序列化期间落地的同胞写迫使再来一轮合并。
                if (
                    not replace
                    and attempt < SAVE_MERGE_ATTEMPTS
                    and self._unmerged_disk_jobs(jobs, removed_ids)
                ):
                    _unlink_quiet(tmp_path)
                    tmp_path = None
                    continue
                # rename 原子发布;目录 fsync 让目录项扛住断电。
                os.replace(tmp_path, self.jobs_file)
                tmp_path = None
                _fsync_directory(self.jobs_file.parent)
                _secure_file(self.jobs_file)
                # 使戳失效(绝不刷新):刷新会让嵌套 save 拿外层调用者的陈旧载荷
                # 认证磁盘。后续 save 走全量合并(fail-safe)。
                self._record_load_stamp(None)
                return
        except BaseException:
            _unlink_quiet(tmp_path)
            raise

    def save_jobs(
        self, jobs: list[dict[str, Any]], *,
        removed_ids: Optional[Collection[str]] = None, replace: bool = False,
    ) -> None:
        """持锁落盘全部 job;``removed_ids``/``replace`` 语义见
        :meth:`_save_jobs_unlocked`。"""
        with self.jobs_lock():
            self._save_jobs_unlocked(jobs, removed_ids=removed_ids, replace=replace)


def _unlink_quiet(path: Optional[str]) -> None:
    """静默删除临时文件(None 安全;上游 L1542)。"""
    if path is not None:
        with contextlib.suppress(OSError):
            os.unlink(path)
