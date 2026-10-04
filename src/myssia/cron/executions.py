"""Cron 执行账本:``<data_root>/cron/executions.db``(cron 专属 SQLite,不进 myssia.db)。

账本记录的是「每次尝试已知什么」,不是重试队列。被打断的尝试只有在属主进程
**被证实死亡**后才落 ``unknown``——claim 时记的指纹读不匹配不是死亡证明。终态
不可变。

上游蓝本:``~/.hermes/hermes-agent/cron/executions.py``(520 行,2026-10-04
HEAD)。NousResearch/Hermes-Agent,MIT——逐段对照重写为 MYIA 风格,非整块拷贝。

MYIA 适配(10-04-hermes-cron design §2.3/§6,全部有档):

- **DDL 按 design §2.3**:增 ``run_summary_json`` 列(D10,RunResult 摘要快照,
  上游从 Hermes 会话 DB 取,MYIA 无会话存储);裁 ``handoff_pending``/
  ``handoff_started_at``/``delivery_outcome`` 三列——handoff 属 detached
  external worker 机器(D3 不搬),投递成败落 job 记录
  ``last_status="delivery_failed"``(§2.1)。属主判定因此不再需要 Hermes 的
  ``process_id`` 列:无 handoff 转移时 ``(pid, process_start_time)`` 指纹唯一
  确定进程实例,语义等价。
- **裁 metrics 上报**(implement A3 明令):上游 ``_emit_execution_state``/
  ``record_cron_finish``(Hermes observability/monitoring 族,D8 域)不搬。
- **裁 live-owner 楔死路径**(上游 ``_live_owner_stale_after_seconds`` +
  ``_OWNER_WEDGED_REASON``):stale bound 派生自 HERMES_CRON_TIMEOUT 不活跃
  旋钮,MYIA 已以 ``run_timeout`` 墙钟超时替代(D12,由 runner killpg 执行),
  旋钮不存在;design §2.3 定语义「unknown 只在属主证实死亡后」,恢复只扫
  可证死行,活属主行一律不动(fail-safe)。
- **数据根** = ``Path(db_path).parent``(ground-truth A6),显式
  ``ExecutionLedger(data_root)`` 实例替代上游模块级 profile home 解析 +
  ``EXECUTIONS_FILE`` 测试覆写。
- **指纹源无 psutil**(核心依赖红线,上游 psutil 是硬依赖):Linux 走
  ``/proc/<pid>/stat``(照抄,字段解析在 ``)`` 后重切,进程名含空格不错位);
  macOS/其他 POSIX 走 ``ps -o lstart=``(C locale 固定英文月名解析为 epoch 秒);
  Windows 无源 → None → 按读不出处理(不能证死 ⇒ 不重写)。各平台只与同源
  读数比较,跨平台单位差异无关(上游同款论证)。
"""

from __future__ import annotations

import contextlib
import json
import os
import sqlite3
import subprocess
import threading
import uuid
from collections.abc import Iterator, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Union

# 终态行数裁剪上限(上游同值):超过即按 newest-first 删旧。
MAX_TERMINAL_EXECUTIONS = 1000

# 属主指纹比对容差(秒,按各平台自身刻度):同机两次 start-time 读数可漂 ~1s
# (macOS kern.boottime 校正,上游 #117505 论证为 ±2s);回收 PID 几乎不可能
# 落进这个窗。
START_TIME_DRIFT_TOLERANCE = 2.0

# 声称→运行→终态;终态不可变(上游 _TERMINAL_STATES)。
_TERMINAL_STATES = ("completed", "failed", "unknown")

# SQLite 打开参数:busy 5s + WAL + synchronous=FULL(审计账本,上游
# open_db(synchronous_full=True) 同款)。
_BUSY_TIMEOUT_SECONDS = 5.0

_OWNER_GONE_REASON = (
    "Scheduler host restarted after this execution's owner exited before a "
    "durable terminal state; whether side effects ran is unknown."
)

# ``ps -o lstart=`` 输出为 C locale 英文周/月名(Python strptime 按进程 locale
# 解析,非英文 locale 下会错),固定映射表自解。
_PS_MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def _now_iso() -> str:
    """aware 本地 ISO 时间戳(与 store._now_iso 同款;账本列全是这个形态)。"""
    return datetime.now().astimezone().isoformat()


# --- 属主指纹(上游 L122-146 照抄;指纹源按上文适配)-------------------------


def _linux_start_seconds(pid: int) -> Optional[float]:
    """``/proc/<pid>/stat`` 第 22 字段(自 boot 的时钟滴答)换算为秒。comm 字段
    可含空格(如 "(Web Content)"),在最后一个 ``)`` 之后重切再数,滴答数不会
    错位(上游 split()[21] 的盲数在此加固)。"""
    try:
        text = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8")
        tail = text[text.rindex(")") + 1:].split()
        return int(tail[19]) / os.sysconf("SC_CLK_TCK")
    except (OSError, IndexError, ValueError):
        return None


def _ps_start_epoch(pid: int) -> Optional[float]:
    """``ps -o lstart= -p <pid>`` 的本地墙钟起始时间换算 epoch 秒(macOS/BSD;
    无 /proc 的 POSIX 平台)。失败/超时/形状不对 → None。"""
    try:
        result = subprocess.run(
            ["ps", "-o", "lstart=", "-p", str(pid)],
            capture_output=True, text=True, timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    tokens = (result.stdout or "").split()
    # "Sun Oct  4 04:36:00 2026" → 5 个 token(月内单日前有双空格,split 吸收)。
    if len(tokens) != 5:
        return None
    month = _PS_MONTHS.get(tokens[1])
    if month is None:
        return None
    try:
        day = int(tokens[2])
        year = int(tokens[4])
        hour, minute, second = (int(part) for part in tokens[3].split(":"))
        started = datetime(year, month, day, hour, minute, second)
    except ValueError:
        return None
    return started.timestamp()  # naive → 按本地时区解释(ps 给的就是本地墙钟)


def process_start_time(pid: int) -> Optional[float]:
    """进程起始时间指纹(PID 复用守卫):(pid, start_time) 唯一确定一个进程,
    回收的 PID(同号不同进程)读数不同,不会误认。Linux = /proc(自 boot 秒);
    macOS/其他 POSIX = ps lstart(epoch 秒);Windows 无源 → None。同机同源比较,
    刻度差异无关(上游 _get_process_start_time L464 的论证照搬)。"""
    started = _linux_start_seconds(pid)
    if started is not None:
        return started
    if os.name == "posix":  # pragma: no branch - darwin/linux 全覆盖,win 走 None
        return _ps_start_epoch(pid)
    return None  # pragma: no cover - Windows:读不出即「不能证死」


def pid_exists(pid: int) -> bool:
    """PID 是否存在。POSIX 用 ``os.kill(pid, 0)``(EPERM = 存在但属别人);
    Windows 用 OpenProcess 探测。判定不了按存在(fail-safe,与 _owner_is_live
    的「不能证死 ⇒ 不重写」同一取向)。"""
    if pid <= 0:
        return False
    if os.name != "nt":
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        except OSError:
            return True
        return True
    # pragma: no cover - Windows 路径本仓无 CI 覆盖
    import ctypes

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    ERROR_INVALID_PARAMETER = 87
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)  # type: ignore[attr-defined]
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
    if handle:
        kernel32.CloseHandle(handle)
        return True
    return ctypes.get_last_error() != ERROR_INVALID_PARAMETER


def start_time_fingerprints_match(
    recorded: Any, current: Any,
    tolerance: float = START_TIME_DRIFT_TOLERANCE,
) -> bool:
    """存活比对器:记录值与当前读数在 ``tolerance`` 内即同一进程化身。垃圾输入
    抛错;读不出(None)那一侧的语义由调用方决定(上游 L449,容差按 MYIA 指纹
    刻度取秒)。"""
    return abs(float(current) - float(recorded)) <= tolerance


def _owner_is_live(pid: int, started_at: Optional[float]) -> bool:
    """属主是否存活:PID 不在 ⇒ 死;start_time 读不出 ⇒ 不能证死 ⇒ 活(误读
    绝不许改写状态);两者都在 ⇒ 容差内比对,漂移的同机读数不是死亡证明(上游
    L130-146)。"""
    try:
        if not pid_exists(pid):
            return False
    except Exception:
        return True  # fail safe:证明不了死亡就绝不重写状态
    if started_at is None:
        return pid == os.getpid()
    current = process_start_time(pid)
    if current is None:
        return True  # 比不了 → 证不了死;活误读仍留给「不重写」兜底
    return start_time_fingerprints_match(float(started_at), current)


def canonical_scheduled_instant(value: Any) -> Optional[str]:
    """到期身份规范化:aware ISO → UTC ISO;naive/非字符串/解析失败 → None
    (无精确身份)。occurrences.py(A5)复用本函数,勿重复实现。"""
    if not isinstance(value, str):
        return None
    try:
        instant = datetime.fromisoformat(value)
    except ValueError:
        return None
    if instant.tzinfo is None:
        return None
    return instant.astimezone(timezone.utc).isoformat()


def _fetch(conn: sqlite3.Connection, execution_id: str) -> Optional[dict[str, Any]]:
    row = conn.execute("SELECT * FROM executions WHERE id=?", (execution_id,)).fetchone()
    return dict(row) if row is not None else None


# --- executions 账本 ----------------------------------------------------------


class ExecutionLedger:
    """一个数据根的 cron 执行账本(``<data_root>/cron/executions.db``)。

    Args:
        data_root: 数据根目录(db 路径父目录,A6)。db 首次开事务时自建目录。

    契约冻结(10-04-hermes-cron implement A3):jobs/tick/runner/occurrences/
    CLI(runs)经本账本读写执行历史,接口形状不得擅改;跨模块裸查询走公开的
    :meth:`transaction`(上游 occurrences.py 引 ``_transaction`` 的对应物)。
    """

    def __init__(self, data_root: Union[str, Path]) -> None:
        self.data_root = Path(data_root)
        self.db_path = self.data_root / "cron" / "executions.db"
        # 进程内串行:tick 线程 + 派发池线程共用一个账本实例(上游 _lock L35)。
        self._lock = threading.RLock()

    @classmethod
    def for_db(cls, db_path: Union[str, Path]) -> "ExecutionLedger":
        """从 myssia.db 路径定位账本(数据根 = db 父目录,A6)。"""
        return cls(Path(db_path).parent)

    # --- 连接与事务(上游 _connect/_transaction L41-101 照抄,裁 open_db 外包)--

    def _connect(self) -> sqlite3.Connection:
        """每事务一开一关:``with conn`` 只提交不关闭,漏关会泄连接与 WAL/SHM
        fd 直到 GC(上游 #69567),故提交-回滚-必关三件套内置。"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.db_path), timeout=_BUSY_TIMEOUT_SECONDS)
        try:
            conn.row_factory = sqlite3.Row
            conn.execute(f"PRAGMA busy_timeout={int(_BUSY_TIMEOUT_SECONDS * 1000)}")
            # WAL 首开需要独占瞬间,繁忙错误重试一轮(上游 wal_lock_retries=1)。
            for attempt in range(2):
                try:
                    conn.execute("PRAGMA journal_mode=WAL")
                    break
                except sqlite3.OperationalError:
                    if attempt == 1:
                        raise
            conn.execute("PRAGMA synchronous=FULL")
            self._initialize_schema(conn)
        except BaseException:
            conn.close()
            raise
        return conn

    @staticmethod
    def _initialize_schema(conn: sqlite3.Connection) -> None:
        """DDL = design §2.3(D10 增 run_summary_json;handoff/delivery_outcome
        裁,见模块 docstring)。索引照抄上游:列表分页、恢复扫描、occurrence
        去重各一。"""
        conn.execute(
            """CREATE TABLE IF NOT EXISTS executions (
                 id TEXT PRIMARY KEY,
                 job_id TEXT NOT NULL,
                 source TEXT NOT NULL,
                 status TEXT NOT NULL CHECK(status IN
                   ('claimed','running','completed','failed','unknown')),
                 scheduled_instant TEXT,
                 pid INTEGER NOT NULL,
                 process_start_time REAL,
                 claimed_at TEXT NOT NULL,
                 started_at TEXT,
                 finished_at TEXT,
                 error TEXT,
                 run_summary_json TEXT
               )"""
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_executions_job_claimed "
            "ON executions(job_id, claimed_at DESC, id DESC)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_executions_status_claimed "
            "ON executions(status, claimed_at DESC, id DESC)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_executions_occurrence "
            "ON executions(job_id, scheduled_instant) WHERE status='completed'"
        )

    @contextlib.contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """进程内锁内开连接、成功提交/出错回滚、**必关**。账本方法内部与
        occurrences.py 的裸查询共用此纪律。"""
        with self._lock:
            conn = self._connect()
            try:
                with conn:
                    yield conn
            finally:
                conn.close()

    # --- 属主判定 --------------------------------------------------------------

    @staticmethod
    def _row_is_own(row: sqlite3.Row) -> bool:
        """行是否本进程当前化身所拥有:pid 同 + 指纹匹配(读不出指纹按己方,
        fail-safe 绝不恢复自己)。pid 同而指纹不匹配 = 同号前任进程 → 非己方
        (上游以 process_id 判,等价论证见模块 docstring)。"""
        if int(row["pid"]) != os.getpid():
            return False
        started = row["process_start_time"]
        own = process_start_time(os.getpid())
        if started is None or own is None:
            return True
        return start_time_fingerprints_match(float(started), own)

    # --- 状态机(上游 L186-308 照抄,列适配)-----------------------------------

    def create_execution(
        self, job_id: str, *, source: str, scheduled_instant: Optional[str] = None,
    ) -> dict[str, Any]:
        """派发前先落一行 claimed(审计在先;source ∈ 'tick'|'manual',
        design §2.3)。"""
        now = _now_iso()
        execution_id = uuid.uuid4().hex
        pid = os.getpid()
        with self.transaction() as conn:
            conn.execute(
                """INSERT INTO executions
                   (id, job_id, source, status, scheduled_instant,
                    pid, process_start_time, claimed_at)
                   VALUES (?, ?, ?, 'claimed', ?, ?, ?, ?)""",
                (execution_id, str(job_id), str(source),
                 canonical_scheduled_instant(scheduled_instant),
                 pid, process_start_time(pid), now),
            )
            record = _fetch(conn, execution_id)
        if record is None:  # pragma: no cover - INSERT 后必在
            raise RuntimeError("execution row vanished right after insert")
        return record

    def mark_execution_running(self, execution_id: str) -> Optional[dict[str, Any]]:
        """claimed → running,恰一次;非己方/非 claimed 行 → None。"""
        now = _now_iso()
        with self.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM executions WHERE id=?", (execution_id,)
            ).fetchone()
            if row is None or row["status"] != "claimed" or not self._row_is_own(row):
                return None
            cur = conn.execute(
                """UPDATE executions
                   SET status='running', started_at=?
                   WHERE id=? AND status='claimed' AND pid=? AND process_start_time IS ?""",
                (now, execution_id, row["pid"], row["process_start_time"]),
            )
            if cur.rowcount != 1:
                return None
            record = _fetch(conn, execution_id)
        return record

    def finish_execution(
        self, execution_id: str, *, success: bool, error: Optional[str] = None,
        run_summary: Optional[Mapping[str, Any]] = None,
    ) -> Optional[dict[str, Any]]:
        """终态写入恰一次(claimed/running → completed/failed);终态行不可再改写
        (再调返回 None,行原样)。``run_summary`` = RunResult 摘要快照
        (D10,JSON 落 run_summary_json)。"""
        now = _now_iso()
        status = "completed" if success else "failed"
        detail = None if success else (str(error) if error else "unknown failure")
        summary_json = (
            json.dumps(dict(run_summary), ensure_ascii=False)
            if run_summary is not None else None
        )
        with self.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM executions WHERE id=?", (execution_id,)
            ).fetchone()
            if (
                row is None
                or row["status"] not in ("claimed", "running")
                or not self._row_is_own(row)
            ):
                return None
            cur = conn.execute(
                """UPDATE executions
                   SET status=?, finished_at=?, error=?, run_summary_json=?
                   WHERE id=? AND status IN ('claimed','running')
                     AND pid=? AND process_start_time IS ?""",
                (status, now, detail, summary_json,
                 execution_id, row["pid"], row["process_start_time"]),
            )
            if cur.rowcount != 1:
                return None
            _prune_unlocked(conn)
            record = _fetch(conn, execution_id)
        return record

    # --- 恢复(上游 L322-441 裁 wedged 路径后照抄)-----------------------------

    def recover_interrupted_executions(self) -> int:
        """把被遗弃的尝试标 ``unknown`` 而不排重试:只动属主**可证死**的行
        (PID 消失,或同号进程已换化身);活属主与读不出的行一律不动
        (design §2.3「unknown 只在属主证实死亡后」)。"""
        now = _now_iso()
        changed = 0
        with self.transaction() as conn:
            rows = conn.execute(
                """SELECT id, status, pid, process_start_time, claimed_at
                   FROM executions
                   WHERE status IN ('claimed','running')"""
            ).fetchall()
            for row in rows:
                if self._row_is_own(row):
                    continue
                if _owner_is_live(int(row["pid"]), row["process_start_time"]):
                    continue
                cur = conn.execute(
                    """UPDATE executions
                       SET status='unknown', finished_at=?, error=?
                       WHERE id=? AND status=? AND pid=? AND process_start_time IS ?""",
                    (now, _OWNER_GONE_REASON,
                     row["id"], row["status"], row["pid"], row["process_start_time"]),
                )
                changed += cur.rowcount
            if changed:
                _prune_unlocked(conn)
        return changed

    def terminalize_dead_owner(self, execution_id: str, *, reason: str) -> bool:
        """把一次尝试记为 ``unknown`` 且带上本进程**实际观察到**的死因(runner
        对孤儿子进程 killpg 后调用,D14)。行缺失/已终态/属本进程/属主仍活 →
        False(调用方回落到 recover 的通用扫)。状态仍是 ``unknown`` 而非
        ``failed``:副作用是否已跑依旧未知,只有**死因**变得更诚实(上游
        L389 论证照抄,handoff 宽限随 handoff 机器裁)。"""
        now = _now_iso()
        with self.transaction() as conn:
            row = conn.execute(
                "SELECT * FROM executions WHERE id=?", (execution_id,)
            ).fetchone()
            if row is None or row["status"] not in ("claimed", "running"):
                return False
            if self._row_is_own(row):
                return False
            if _owner_is_live(int(row["pid"]), row["process_start_time"]):
                return False
            cur = conn.execute(
                """UPDATE executions
                   SET status='unknown', finished_at=?, error=?
                   WHERE id=? AND status=? AND pid=? AND process_start_time IS ?""",
                (now, reason, execution_id, row["status"],
                 row["pid"], row["process_start_time"]),
            )
            if cur.rowcount != 1:
                return False
            _prune_unlocked(conn)
        return True

    # --- 查询(上游 L444-520 照抄)--------------------------------------------

    def list_executions(
        self, *, job_id: Optional[str] = None, limit: int = 50,
        before_claimed_at: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """索引化的最新优先执行历史,游标分页。"""
        clauses: list[str] = []
        params: list[Any] = []
        if job_id is not None:
            clauses.append("job_id=?")
            params.append(str(job_id))
        if before_claimed_at is not None:
            # 与 ORDER BY 同一 (instant, text) 键,一页永不跳行/重行。
            clauses.append("(julianday(claimed_at), claimed_at) < (julianday(?), ?)")
            params.extend([str(before_claimed_at)] * 2)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        params.append(max(1, min(int(limit), 500)))
        # 时间戳带本地偏移,DST/换区后文本序≠时间序;julianday() 比瞬间(毫秒),
        # 文本破同毫秒平局。
        with self.transaction() as conn:
            rows = conn.execute(
                "SELECT * FROM executions" + where
                + " ORDER BY julianday(claimed_at) DESC, claimed_at DESC, id DESC LIMIT ?",
                params,
            ).fetchall()
        return [dict(row) for row in rows]

    def get_execution(self, execution_id: str) -> Optional[dict[str, Any]]:
        """精确取一行,缺失 → None。"""
        with self.transaction() as conn:
            return _fetch(conn, str(execution_id))

    def latest_execution(self, job_id: str) -> Optional[dict[str, Any]]:
        """一个 job 的最新一行。"""
        rows = self.list_executions(job_id=job_id, limit=1)
        return rows[0] if rows else None

    def live_inflight_execution(self, job_id: str) -> Optional[dict[str, Any]]:
        """job 仍在**存活属主**名下 claimed/running 的最新尝试,否则 None。这是
        调度器所有权判定而非「最近活动」:长执行可以长时间不写心跳但仍是活属主,
        而进程死掉的尝试不算。只读——不像 recover 那样改写任何行。"""
        record = self.latest_execution(job_id)
        if not record or record.get("status") not in ("claimed", "running"):
            return None
        if not _owner_is_live(int(record["pid"]), record.get("process_start_time")):
            return None
        return record

    def latest_executions(self, job_ids: Sequence[str]) -> dict[str, dict[str, Any]]:
        """一次查询载入多 job 的最新执行(窗口化排序;每行相关子查询用不上
        索引,随历史平方增长,上游 L500 论证照抄)。"""
        clean = [str(job_id) for job_id in dict.fromkeys(job_ids) if job_id]
        if not clean:
            return {}
        placeholders = ",".join("?" for _ in clean)
        with self.transaction() as conn:
            rows = conn.execute(
                f"""SELECT e.* FROM executions e WHERE e.id IN (
                      SELECT id FROM (
                        SELECT id, ROW_NUMBER() OVER (
                                 PARTITION BY job_id
                                 ORDER BY julianday(claimed_at) DESC, claimed_at DESC, id DESC
                               ) AS rn
                        FROM executions WHERE job_id IN ({placeholders}))
                      WHERE rn=1)""",
                clean,
            ).fetchall()
        return {row["job_id"]: dict(row) for row in rows}


def _prune_unlocked(conn: sqlite3.Connection) -> None:
    """终态行按 newest-first 裁到 MAX_TERMINAL_EXECUTIONS(上游 L174)。"""
    conn.execute(
        """DELETE FROM executions WHERE id IN (
             SELECT id FROM executions
             WHERE status IN ('completed','failed','unknown')
             ORDER BY julianday(finished_at) DESC, finished_at DESC,
                      julianday(claimed_at) DESC, claimed_at DESC, id DESC LIMIT -1 OFFSET ?
           )""",
        (max(0, int(MAX_TERMINAL_EXECUTIONS)),),
    )
