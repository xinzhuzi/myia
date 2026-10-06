"""统一日志模块(10-07-unified-logging R0;design §1)。

一个模块、一个漏斗、一种文件形状、一套轮转保留:

- ``configure()`` 单点配置(幂等:先摘自己上次的 handler 再挂,force 互踩
  从根上消失——R4);stderr handler(mode 分级:human=INFO / json·serve=
  WARNING)+ RingHandler(``CAPACITY`` 帽,UI 数据面)+ JsonlFileHandler
  (``<data_root>/logs/myssia-YYYYMMDD.jsonl`` 本地日轮转,保留 ``RETENTION_DAYS``)
  同挂 root。数据根解析不在本模块:各入口用既有解析后传 ``data_root``
  (单一职责,不引入第二套路径规则,design §2)。
- seq 单源单调:``logging.setLogRecordFactory`` 盖章(进程内装一次),ring
  与文件两 handler 读同一 ``record.seq``;**文件行不落 seq**——多进程
  (sidecar/cron CLI/手动 CLI)并发 append 时各进程计数器独立必冲突
  (design §0),回填时由本模块按读入顺序重发新 seq。
- 落盘 = date-in-filename + ``O_APPEND`` 每-进程-自开当日文件,无 rename:
  stdlib ``TimedRotatingFileHandler`` 的 rename 轮转在多进程同写场景下丢行
  (design §1 对照结论),手写面因此最小且必要。
- 降级(R6):首错向 ring append 一条提示并永久禁用文件路,绝不向上抛;
  ``handleError`` 静默 override——日志模块自身故障不经 logging 通路放大。
"""

from __future__ import annotations

import json
import logging
import re
import sys
import threading
from collections import deque
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal, TextIO

__all__ = [
    "BACKFILL_BUDGET",
    "CAPACITY",
    "RETENTION_DAYS",
    "backfill",
    "configure",
    "is_configured",
    "reset_ring",
    "resume_stderr",
    "ring_snapshot",
    "stream_line",
    "suspend_stderr",
]

#: 环形帽(行);沿 desktop/entry.py LOG_RING_CAPACITY=4000 现值,logs.tail 硬上限。
CAPACITY = 4000
#: 文件保留天数(design §4;Python/Rust 各持一份,无 UI/env 旋钮——非目标)。
RETENTION_DAYS = 7
#: 冷回填预算(行);帽的一半,给当期实时流留量(design §5)。
BACKFILL_BUDGET = 2000

#: 文件名单前缀(决议③:vision 并入单前缀;壳侧 shell-*.log 归 tauri-plugin-log,不在此)。
_FILE_PREFIX = "myssia"
#: 文件名形状 myssia-YYYYMMDD.jsonl——清理 glob 钉死此前缀,绝不整目录清理(design §4 红线)。
_FILE_NAME_RE = re.compile(rf"^{_FILE_PREFIX}-(\d{{8}})\.jsonl$")
#: 子进程行落点 logger(run_id/stream/proc 经 extra 注入,design §1 stream_line)。
_STREAM_LOGGER = "myssia.stream"
#: 单行上限(字节):单行单次 write + O_APPEND 的 POSIX 行级原子前提(design §0;
#: 逐行转发天然远小,超限截断保原子性声明成立)。
_MAX_LINE_BYTES = 65536
#: root 统一级别 INFO:stream 行与模块 INFO 入漏斗;终端分级由 stderr handler 自持。
_ROOT_LEVEL = logging.INFO
#: stderr 行格式(沿 CLI 现状 %(asctime)s …,design §1)。
_STDERR_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
#: configure 挂载标记:幂等摘除的锚点(只摘自己挂的,不碰他人 handler)。
_HANDLER_TAG = "_myssia_unified_log"

_SEQ = 0
_SEQ_LOCK = threading.Lock()

_RING: deque[dict[str, Any]] = deque(maxlen=CAPACITY)
_RING_LOCK = threading.Lock()

#: 进程内 seq 盖章工厂(装一次守卫;卸载/复位仅测试经 _reset_module_state)。
_OUR_FACTORY: Any = None
_PREV_FACTORY: Any = None


class _ModuleState:
    """configure 后的进程级状态(proc 缺省值/挂点引用/挂起旗)。"""

    mode: str | None = None
    proc: str = "cli"
    data_root: Path | None = None
    stderr_handler: logging.Handler | None = None
    stderr_suspended = False


_STATE = _ModuleState()


# ---------------------------------------------------------------------------
# 基元:seq / 时间 / 行帽
# ---------------------------------------------------------------------------


def _next_seq() -> int:
    global _SEQ
    with _SEQ_LOCK:
        _SEQ += 1
        return _SEQ


def _now_iso() -> str:
    """ISO-UTC 毫秒(沿 entry.py _now_iso 同款)。"""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _today() -> date:
    """本地日期(文件名/轮转/保留清理共用;测试 monkeypatch 此处注入跨天)。"""
    return datetime.now().date()


def _cap_line(line: str) -> str:
    """超限行按字节截断(单行原子上限的守卫,design §0)。"""
    data = line.encode("utf-8")
    if len(data) <= _MAX_LINE_BYTES:
        return line
    return data[:_MAX_LINE_BYTES].decode("utf-8", errors="ignore") + "…[超长截断]"


def _entry_from_record(record: logging.LogRecord) -> dict[str, Any]:
    """record → 统一条目形状(=今天环形条目超集,design §0)。

    run_id/stream 从 extra 注入的属性读,缺省 ``None/"stderr"``(模块自身
    WARNING+ 日志的口径);proc 缺省用本进程 configure 的 proc。
    """
    return {
        "seq": getattr(record, "seq", 0),
        "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(
            timespec="milliseconds"
        ),
        "run_id": getattr(record, "run_id", None),
        "stream": getattr(record, "stream", "stderr"),
        "line": _cap_line(record.getMessage()),
        "proc": getattr(record, "proc", _STATE.proc),
    }


def _install_factory() -> None:
    """装 seq 盖章工厂(进程内只装一次;已被他人替换时以当前工厂为链头重装)。"""
    global _OUR_FACTORY, _PREV_FACTORY
    if _OUR_FACTORY is not None and logging.getLogRecordFactory() is _OUR_FACTORY:
        return
    prev = logging.getLogRecordFactory()

    def stamped(*args: Any, **kwargs: Any) -> logging.LogRecord:
        record = prev(*args, **kwargs)
        record.seq = _next_seq()
        return record

    _PREV_FACTORY = prev
    _OUR_FACTORY = stamped
    logging.setLogRecordFactory(stamped)


def _purge_stale(logs_dir: Path) -> None:
    """超期清理(design §4):仅 ``myssia-YYYYMMDD.jsonl`` 单前缀,名形不合不碰。

    cutoff = 本地今天 − RETENTION_DAYS;清理失败静默(只读根/竞态删除),
    保留策略失守不破主链。
    """
    try:
        cutoff = _today() - timedelta(days=RETENTION_DAYS)
        for path in logs_dir.glob(f"{_FILE_PREFIX}-*.jsonl"):
            matched = _FILE_NAME_RE.match(path.name)
            if matched is None:
                continue
            try:
                day = datetime.strptime(matched.group(1), "%Y%m%d").date()
            except ValueError:
                continue
            if day < cutoff:
                path.unlink(missing_ok=True)
    except Exception:
        pass


def _read_tail(path: Path, limit: int) -> list[dict[str, Any]]:
    """文件尾取至多 ``limit`` 条完整可解析 JSONL 行(坏行/空行跳过,时序保持)。"""
    with open(path, encoding="utf-8") as fh:
        rows = fh.read().splitlines()
    tail: list[dict[str, Any]] = []
    for raw in reversed(rows):
        if len(tail) >= limit:
            break
        raw = raw.strip()
        if not raw:
            continue
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            tail.append(parsed)
    tail.reverse()
    return tail


# ---------------------------------------------------------------------------
# Handler 两件:RingHandler / JsonlFileHandler
# ---------------------------------------------------------------------------


class RingHandler(logging.Handler):
    """环形缓冲 handler:record → 条目 append(帽内自动逐出最旧)。"""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            entry = _entry_from_record(record)
            with _RING_LOCK:
                _RING.append(entry)
        except Exception:
            self.handleError(record)


class JsonlFileHandler(logging.Handler):
    """JSONL 文件 handler:惰性开当日文件、本地日切换、每行 flush。

    - 文件行不落 seq(多进程并发 append 各进程 seq 独立必冲突,design §0);
    - 单行单次 write + ``open(..., "a")`` 的 O_APPEND 保 POSIX 行级原子;
    - 轮转 = 日期变更时换文件名,**无 rename**(多进程安全形态,design §1);
    - 降级(R6):首错关句柄、置永久禁用、向 ring append 一条提示(不经
      logging,防递归),此后静默。
    """

    def __init__(self, logs_dir: Path) -> None:
        super().__init__()
        self._logs_dir = logs_dir
        self._day: date | None = None
        self._fh: TextIO | None = None
        self._degraded = False

    def emit(self, record: logging.LogRecord) -> None:
        if self._degraded:
            return
        try:
            self._ensure_open()
            payload = _entry_from_record(record)
            payload.pop("seq")
            assert self._fh is not None
            self._fh.write(json.dumps(payload, ensure_ascii=False) + "\n")
            self._fh.flush()
        except Exception:
            self._degrade()

    def _ensure_open(self) -> None:
        today = _today()
        if self._fh is not None and self._day == today:
            return
        if self._fh is not None:
            try:
                self._fh.close()
            except Exception:
                pass
        self._logs_dir.mkdir(parents=True, exist_ok=True)
        self._fh = open(
            self._logs_dir / f"{_FILE_PREFIX}-{today:%Y%m%d}.jsonl",
            "a",
            encoding="utf-8",
        )
        self._day = today

    def _degrade(self) -> None:
        """首错降级:永久禁用 + ring 一条提示;后续任何 emit 直接返回。"""
        if self._degraded:
            return
        self._degraded = True
        if self._fh is not None:
            try:
                self._fh.close()
            except Exception:
                pass
            self._fh = None
        notice = {
            "seq": _next_seq(),
            "ts": _now_iso(),
            "run_id": None,
            "stream": "stderr",
            "line": "myssia 日志落盘已降级(数据根不可写,本进程内不再尝试);环形缓冲与 stderr 不受影响",
            "proc": _STATE.proc,
        }
        with _RING_LOCK:
            _RING.append(notice)

    def handleError(self, record: logging.LogRecord) -> None:
        """静默 override(design §1 自举):logging 默认把 handler 异常打到
        stderr,装机件无人接收且会刷屏;降级态必须静默。"""

    def close(self) -> None:
        if self._fh is not None:
            try:
                self._fh.close()
            except Exception:
                pass
            self._fh = None
        super().close()


def _build_stderr_handler(mode: str) -> logging.StreamHandler:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(_STDERR_FORMAT))
    handler.setLevel(logging.INFO if mode == "human" else logging.WARNING)
    return handler


# ---------------------------------------------------------------------------
# 公开面
# ---------------------------------------------------------------------------


def configure(
    *,
    mode: Literal["human", "json", "serve"],
    data_root: Path | None,
    ring: bool = False,
    proc: str = "cli",
) -> None:
    """单点配置(幂等):先摘自己上次的 handler 再挂,force 互踩不可能(R4)。

    - ``mode``:human → stderr INFO;json/serve → stderr WARNING(对齐现契约);
    - ``data_root``:None → 不挂文件 handler(决议②:裸 repo 终端跑仅 stderr,
      防 logs/ 建进仓库);非 None → ``<data_root>/logs`` 落盘 + 启动超期清理;
    - ``ring``:True → 挂 RingHandler(serve 数据面)。环形本身不清:进程内
      重配(如 serve 内嵌 CLI 调用)保留既有行;
    - ``proc``:本进程条目的 proc 缺省值(sidecar/cli/cron/vision,决议③)。

    重配摘下的旧 handler 会被 close(文件句柄不泄漏)。

    **挂起窗跨重配存续**(批1 design §3):``suspend_stderr()`` 打开的窗口内
    即使再次 configure(如 sidecar 内嵌 cli_main 的重配),新 stderr handler
    也不挂回 root——窗口语义由「窗口方」负责收口(resume 或恢复配置),
    窗口内任何重配不得把 logging 行漏进被捕获的 stderr(双份防线)。
    """
    _install_factory()
    root = logging.getLogger()
    for handler in list(root.handlers):
        if getattr(handler, _HANDLER_TAG, False):
            root.removeHandler(handler)
            handler.close()
    root.setLevel(_ROOT_LEVEL)
    data_root = Path(data_root) if data_root is not None else None
    _STATE.mode = mode
    _STATE.proc = proc
    _STATE.data_root = data_root
    if data_root is not None:
        logs_dir = data_root / "logs"
        file_handler = JsonlFileHandler(logs_dir)
        setattr(file_handler, _HANDLER_TAG, True)
        root.addHandler(file_handler)
        _purge_stale(logs_dir)
    if ring:
        ring_handler = RingHandler()
        setattr(ring_handler, _HANDLER_TAG, True)
        root.addHandler(ring_handler)
    stderr_handler = _build_stderr_handler(mode)
    setattr(stderr_handler, _HANDLER_TAG, True)
    _STATE.stderr_handler = stderr_handler
    if not _STATE.stderr_suspended:
        root.addHandler(stderr_handler)


def stream_line(
    run_id: int | None, stream: str, line: str, *, proc: str | None = None
) -> dict[str, Any]:
    """子进程一行输出 → 同一漏斗;返回入环形的条目供协议事件发射。

    经 ``myssia.stream`` logger INFO + extra 注入走 root 三 handler:ring+盘
    必得;stderr 因 INFO 不过 WARNING 门(与今天子进程行只进 ring+事件的
    现状一致,design §1)。返回条目与环形同 seq 同 ts——调用方(entry.py
    pump)用它发射协议 ``type:"log"`` 事件,协议事件仍属 sidecar 层。

    ``proc``:显式进程标注(sidecar 进程内转发的 vision 子进程行传
    ``"vision"``,决议③——本进程缺省值会把它错标成 sidecar);缺省用
    configure 时定的本进程 proc。
    """
    logger = logging.getLogger(_STREAM_LOGGER)
    record = logger.makeRecord(
        _STREAM_LOGGER,
        logging.INFO,
        "(myssia.log)",
        1,
        line,
        None,
        None,
        extra={
            "run_id": run_id,
            "stream": stream,
            "proc": proc if proc is not None else _STATE.proc,
        },
    )
    logger.handle(record)
    return _entry_from_record(record)


def ring_snapshot(run_id: int | None = None, lines: int = CAPACITY) -> list[dict[str, Any]]:
    """环形快照(logs.tail 数据面;语义沿 entry.py _m_logs_tail:run_id 过滤+尾部截取)。"""
    with _RING_LOCK:
        snapshot = list(_RING)
    if run_id is not None:
        snapshot = [entry for entry in snapshot if entry.get("run_id") == run_id]
    return snapshot[-lines:] if lines > 0 else []


def is_configured() -> bool:
    """root 上是否已有本模块 handler(进程级「统一日志已配置」判定)。

    供 vision server 的惰性自举(批1 design §2):sidecar/CLI 进程内已有
    配置(尤其 sidecar 的 ring 必须保住)时 no-op,仅独立调用形态才自行
    configure。
    """
    return any(
        getattr(handler, _HANDLER_TAG, False) for handler in logging.getLogger().handlers
    )


def reset_ring() -> None:
    """清环形缓冲(serve 会话冷启动;批1)。

    serve() 可重入(entry.py「lifetime = serve」)——重入即新会话,语义
    对齐新进程冷启动:旧会话行已落盘,由 ``backfill`` 从盘尾拉回接管
    历史;不清则 backfill 会把上一会话已入环形的行再 seed 一遍(重复)。
    进程内普通重配(``configure``)不清环形(既有契约,design §1)。
    """
    with _RING_LOCK:
        _RING.clear()


def backfill(data_root: Path) -> list[dict[str, Any]]:
    """serve 启动冷回填(design §5):盘尾预算内条目 seed 环形并重发新 seq。

    文件按日期升序、逐文件取尾,合计至多 ``BACKFILL_BUDGET`` 行;只收完整
    可解析 JSONL 行(坏行跳过,崩溃截尾容忍);proc 字段原样保留(可辨
    「上一程是谁」)。任何异常(无文件/无目录/全坏行)静默通过 = 与现状
    全同。返回回填条目(时间序),供调用方留痕/测试断言。
    """
    seeded: list[dict[str, Any]] = []
    try:
        logs_dir = Path(data_root) / "logs"
        files = sorted(p for p in logs_dir.glob(f"{_FILE_PREFIX}-*.jsonl") if p.is_file())
        collected: list[dict[str, Any]] = []
        budget = BACKFILL_BUDGET
        for path in reversed(files):
            if budget <= 0:
                break
            tail = _read_tail(path, budget)
            collected = tail + collected
            budget -= len(tail)
        for payload in collected:
            entry = dict(payload)
            entry["seq"] = _next_seq()
            with _RING_LOCK:
                _RING.append(entry)
            seeded.append(entry)
    except Exception:
        pass
    return seeded


def suspend_stderr() -> None:
    """摘 stderr handler(_cli_json 内嵌 CLI 窗口:防 logging 行双份进被捕获 err,design §3)。

    ring/文件路不受影响;未配置或已挂起时 no-op。
    """
    handler = _STATE.stderr_handler
    if handler is None or _STATE.stderr_suspended:
        return
    logging.getLogger().removeHandler(handler)
    _STATE.stderr_suspended = True


def resume_stderr() -> None:
    """复挂 stderr handler(窗口结束);未挂起时 no-op。"""
    handler = _STATE.stderr_handler
    if handler is None or not _STATE.stderr_suspended:
        return
    if handler not in logging.getLogger().handlers:
        logging.getLogger().addHandler(handler)
    _STATE.stderr_suspended = False


# ---------------------------------------------------------------------------
# 测试隔离专用(design §1.2;生产代码不调用)
# ---------------------------------------------------------------------------


def _reset_module_state() -> None:
    """批0 测试隔离:摘本模块 handler、卸工厂(身份核验)、清环形/状态/seq。

    工厂卸载按身份核验(``getLogRecordFactory() is _OUR_FACTORY``)——若
    他人(或测试夹具)已替换工厂,不动它;复位后由测试夹具自行恢复其
    保存的工厂快照。
    """
    root = logging.getLogger()
    for handler in list(root.handlers):
        if getattr(handler, _HANDLER_TAG, False):
            root.removeHandler(handler)
            handler.close()
    global _OUR_FACTORY, _SEQ
    if _OUR_FACTORY is not None and logging.getLogRecordFactory() is _OUR_FACTORY:
        logging.setLogRecordFactory(_PREV_FACTORY)
        _OUR_FACTORY = None
    with _RING_LOCK:
        _RING.clear()
    _SEQ = 0
    _STATE.mode = None
    _STATE.proc = "cli"
    _STATE.data_root = None
    _STATE.stderr_handler = None
    _STATE.stderr_suspended = False
