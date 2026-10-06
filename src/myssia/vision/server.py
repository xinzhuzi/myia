"""mlx_vlm.server 生命周期代管(10-03-vision-v2;PRD R2「重启机器后 vl 零手工」)。

当前形态的痛点:本地 VL 端点(:8080)是手工 ``nohup`` 起的裸进程,重启
机器后静默消失,管线 VL 全部 ``vl_skipped_error``。本模块把它收编:

- :func:`vision_server_status` —— 探 ``{local_base_url}/models``(2s 帽):
  ``running`` = 拿到任何 HTTP 应答(端口有活物),``healthy`` = 200
  (OpenAI 兼容 ``/v1/models``,与 mlx_vlm.server 实现面一致);
- :func:`ensure_vision_server` —— 未跑且 ``local.model`` 已配且目录在 →
  ``nohup`` 自启 ``uvx --from mlx-vlm mlx_vlm.server --model <path>
  --host 127.0.0.1 --port <从 base_url 解析>``,健康等待 ≤120s(Metal JIT
  首载慢是常态,不是故障);失败结构化上抛(:class:`VisionServerError`)。
  三条自守纪律:并发 ensure 互斥(:data:`_ENSURE_LOCK`,锁内重探健康防双
  spawn);超健康窗先杀子进程再上抛(孤儿不留,:func:`_terminate_proc`);
  子进程 stdout/stderr 管道泵入统一日志流(10-07-unified-logging 批1
  决议③:落 ``myssia-*.jsonl`` 的 proc=vision 行,vision-server.log 退役)。

调用方:管线侧 collect 环 ``vl:local`` 前 ensure 一次(失败沿用
``vl_skipped_error`` 降级,绝不阻管线,见 :mod:`myssia.pipeline`);协议侧
``image.server.status`` / ``image.server.ensure``(desktop/entry.py)。

纪律:零重依赖(httpx + subprocess,均为核心依赖面);spawn 用
``start_new_session=True``(setsid = nohup 语义:脱离终端、不受壳退出
SIGHUP 波及),子进程输出走 stdout/stderr 管道 → daemon 泵线程逐行
:func:`myssia.log.stream_line`(崩溃 traceback 不丢;serve 进程的 stdout
是协议流,子进程输出绝不裸穿)——泵线程随进程退出,setsid 子进程在
泵线程死后写满管道缓冲属可接受终态(server 死→管道读端全关)。健康
等待跑在调用方线程(pipeline 经 ``asyncio.to_thread``,协议层同步等待)。
"""

from __future__ import annotations

import contextlib
import subprocess
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx

from myssia import log as unified_log
from myssia.vision.settings import VisionConfig

__all__ = [
    "HEALTH_POLL_INTERVAL_SECONDS",
    "HEALTH_WAIT_SECONDS",
    "PROBE_TIMEOUT_SECONDS",
    "TERMINATE_GRACE_SECONDS",
    "VisionServerError",
    "ensure_vision_server",
    "vision_server_status",
]

#: /models 探测超时(秒;status 面向 UI,快失败)。
PROBE_TIMEOUT_SECONDS = 2.0
#: 自启后的健康等待上限(秒):Metal JIT 首次加载 30-60s 是常态,120s 是
#: 上限不是预期(10-03 装机冒烟实证)。
HEALTH_WAIT_SECONDS = 120.0
#: 健康轮询间隔(秒)。
HEALTH_POLL_INTERVAL_SECONDS = 2.0
#: 超窗孤儿进程的 SIGTERM 宽限秒数(到期 SIGKILL;run.cancel 同款纪律)。
TERMINATE_GRACE_SECONDS = 2.0

#: ensure 互斥(并发 ensure 双检门):协议层后台线程与管线 ``asyncio.to_thread``
#: 可能同时进 ensure —— 拿不到锁就等(对等调用 ≤health_wait 必收尾),锁内
#: 重探健康再 spawn,杜绝双 spawn 抢同一端口。
_ENSURE_LOCK = threading.Lock()
#: 最近一次 spawn 的子进程登记(诊断面/孤儿清理定位;赋值原子,读取方容 None)。
_LAST_PROC: subprocess.Popen | None = None


class VisionServerError(ValueError):
    """server 代管结构化错误(code + message + details;协议层翻译为应答 error)。

    Attributes:
        code: ``no_local_model`` / ``model_dir_missing`` / ``spawn_failed`` /
            ``server_died`` / ``server_start_failed``。
        details: 结构化上下文(port / model 路径 / 日志路径 / 退出码)。
    """

    def __init__(self, code: str, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.details: dict[str, Any] = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Machine-readable form(协议错误 data / 诊断消费)。"""
        return {"error_type": self.code, "message": str(self), **self.details}


def _parse_port(base_url: str) -> int:
    """从 base_url 解析端口(http 缺省 80 / https 缺省 443)。"""
    parsed = urlparse(base_url)
    if parsed.port:
        return parsed.port
    return 443 if parsed.scheme == "https" else 80


def _probe(base_url: str, *, timeout: float = PROBE_TIMEOUT_SECONDS) -> tuple[bool, bool]:
    """GET ``{base_url}/models`` → ``(running, healthy)``(零异常上抛)。

    running = 拿到 HTTP 应答(端口有进程在听);healthy = 200。连接拒绝/
    超时/DNS 失败 = ``(False, False)``。

    ``trust_env=False``:探测目标恒为本地通道端点(缺省 127.0.0.1:8080),
    必须直连——httpx 0.28.1 的 trust_env 除进程 env 外还会吃 macOS 系统代理
    (urllib.getproxies → scutil;collect._client_egress_is_proxied 同源发现)。
    经代理探死端口会拿到代理 502 应答,running 误报 True(2026-10-03 实证:
    本机 clash 系统代理下 ``127.0.0.1:9`` → HTTP 502),「本地通道零出网」
    边界也要求探测不经代理。
    """
    url = base_url.rstrip("/") + "/models"
    try:
        response = httpx.Client(timeout=timeout, trust_env=False).get(url)
    except httpx.HTTPError:
        return (False, False)
    return (True, response.status_code == 200)


def vision_server_status(
    config: VisionConfig, *, timeout: float = PROBE_TIMEOUT_SECONDS
) -> dict[str, Any]:
    """本地 VL server 状态 → ``{running, base_url, model, healthy}``。

    ``model`` = vision.yaml ``local.model`` 配置值(端口上跑的**应该是**它;
    不问 server 实载 —— /models 列表与配置不符属配置漂移,交 UI 呈现)。
    """
    running, healthy = _probe(config.local_base_url, timeout=timeout)
    return {
        "running": running,
        "base_url": config.local_base_url,
        "model": config.local_model,
        "healthy": healthy,
    }


def _server_command(model_path: str, port: int) -> list[str]:
    """spawn 命令行(冻结契约,勿改):uvx 拉起 mlx_vlm.server 本地端点。"""
    return [
        "uvx", "--from", "mlx-vlm", "mlx_vlm.server",
        "--model", model_path,
        "--host", "127.0.0.1",
        "--port", str(port),
    ]


def _ensure_unified_logging(data_root: Path | None) -> None:
    """进程级惰性自举(10-07-unified-logging 批1,design §2 vision 行)。

    root 已有统一模块 handler(sidecar/CLI 进程内)→ no-op——尤其 sidecar
    的 ring 是 logs.tail 数据面,绝不能被 vision 的 configure 摘掉;独立调用
    形态才自行 ``configure(mode="serve", ring=False, proc="vision")``。
    ``data_root`` 为 None 时同样 no-op:未配置进程里 stream_line 的 INFO 无
    handler 可达,行为同旧 DEVNULL(决议②裸跑零落盘)。
    """
    if data_root is None or unified_log.is_configured():
        return
    unified_log.configure(mode="serve", data_root=data_root, ring=False, proc="vision")


def _pump_output(stream_obj: Any, stream_name: str) -> None:
    """逐行泵子进程管道输出 → 统一日志流(proc=vision;design §2)。

    daemon 线程跑:server 活多久泵多久(ensure 返回后照常),父进程退出
    随之退出;行 decode 容错(uvicorn 启动 banner 偶非 UTF-8 字节)。
    """
    for raw in stream_obj:
        if isinstance(raw, bytes):
            line = raw.decode("utf-8", errors="replace").rstrip("\n")
        else:
            line = str(raw).rstrip("\n")
        if line.strip():
            unified_log.stream_line(None, stream_name, line, proc="vision")


def _attach_output_pumps(proc: Any) -> None:
    """给 spawn 出的子进程挂输出泵(测试替身无管道属性 = 零动作)。"""
    stderr = getattr(proc, "stderr", None)
    stdout = getattr(proc, "stdout", None)
    if stderr is not None:
        threading.Thread(
            target=_pump_output, args=(stderr, "stderr"),
            daemon=True, name="vision-server-stderr-pump",
        ).start()
    if stdout is not None:
        threading.Thread(
            target=_pump_output, args=(stdout, "stdout"),
            daemon=True, name="vision-server-stdout-pump",
        ).start()


def _terminate_proc(proc: subprocess.Popen, *, grace: float = TERMINATE_GRACE_SECONDS) -> None:
    """SIGTERM → 宽限秒 → SIGKILL(超窗孤儿绝不留;run.cancel 同款纪律)。

    对已退出进程零动作;每步 OSError 容忍(进程可能刚好死在指缝里)。
    """
    if proc.poll() is not None:
        return
    with contextlib.suppress(OSError, ValueError):
        proc.terminate()
    try:
        proc.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        with contextlib.suppress(OSError, ValueError):
            proc.kill()
        with contextlib.suppress(OSError, ValueError):
            proc.wait()
    except OSError:
        pass  # wait 本身失败(已 reap 等):尽力而为


def ensure_vision_server(
    config: VisionConfig,
    *,
    data_root: Path | str | None = None,
    timeout: float = PROBE_TIMEOUT_SECONDS,
    health_wait: float = HEALTH_WAIT_SECONDS,
    poll_interval: float = HEALTH_POLL_INTERVAL_SECONDS,
    _spawn: Any = None,
) -> dict[str, Any]:
    """确保本地 mlx_vlm.server 在跑:健康即返;未跑且可跑则自启并等健康。

    前置门槛(不满足 = 结构化拒绝,不盲目 spawn):``local.model`` 已配且
    目录存在 —— 配置缺失是用户态问题,不是本函数该掩盖的。

    日志(10-07-unified-logging 批1,决议③):子进程 stdout/stderr 走管道,
    daemon 泵线程逐行 ``myssia.log.stream_line(proc="vision")`` 落统一
    ``myssia-*.jsonl``(崩溃 traceback 不丢);``data_root`` 是数据根锚点
    (= 旧 ``log_path`` 的父目录语义),进程未配置统一日志且给了锚点时
    惰性自举(:func:`_ensure_unified_logging`)。

    并发互斥:spawn + 健康等待全程持 :data:`_ENSURE_LOCK`(拿不到就等
    对等调用收尾,≤health_wait);锁内**重探健康**再 spawn —— 并发窗口里
    另一个 ensure 可能刚把 server 拉起来,双检直接吃到 started=False。

    超窗收尾:健康窗耗尽时**先杀子进程再上抛**(``terminate → 宽限 → kill``,
    见 :func:`_terminate_proc`)—— 半死不活的 JIT 僵局进程不该变孤儿占着
    端口,让下一次 ensure 从干净状态重来。

    Returns:
        ``{running, base_url, model, healthy, started}``;``started=True``
        表示本次调用真的拉起了子进程(False = 本就在跑/对等调用已拉起)。

    Raises:
        VisionServerError: ``no_local_model`` / ``model_dir_missing`` /
            ``spawn_failed``(uvx 缺装等)/ ``server_died``(子进程提前退出)/
            ``server_start_failed``(超健康窗仍未就绪,子进程已收尾;JIT 慢
            可重试)。
    """
    global _LAST_PROC
    status = vision_server_status(config, timeout=timeout)
    if status["healthy"]:
        return {**status, "started": False}
    if not config.local_model:
        raise VisionServerError(
            "no_local_model",
            "vision.yaml 未配置 local.model,无从自启(先在设置屏下载/激活模型)",
            details={"base_url": config.local_base_url},
        )
    model_dir = Path(config.local_model).expanduser()
    if not model_dir.is_dir():
        raise VisionServerError(
            "model_dir_missing",
            f"local.model 目录不存在: {model_dir}",
            details={"model": str(model_dir)},
        )
    root = Path(data_root) if data_root is not None else None
    _ensure_unified_logging(root)
    port = _parse_port(config.local_base_url)
    cmd = _server_command(str(model_dir), port)
    spawn = _spawn or subprocess.Popen
    with _ENSURE_LOCK:
        # 双检:等锁期间对等 ensure 可能已把 server 拉起 —— 重探健康,
        # 命中即返(started=False = 不是本次调用拉起)。
        status = vision_server_status(config, timeout=timeout)
        if status["healthy"]:
            return {**status, "started": False}
        try:
            proc = spawn(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                start_new_session=True,  # setsid = nohup 语义:脱离终端,壳退出不波及
            )
        except OSError as exc:
            raise VisionServerError(
                "spawn_failed",
                f"无法拉起 mlx_vlm.server(uvx 可用吗?brew install uv): {type(exc).__name__}: {exc}",
                details={"cmd": cmd, "port": port},
            ) from exc
        _attach_output_pumps(proc)  # 管道泵 → myssia-*.jsonl(proc=vision)
        _LAST_PROC = proc  # 模块级登记:诊断/孤儿定位(赋值原子;serve 单写)
        deadline = time.monotonic() + health_wait
        while time.monotonic() < deadline:
            if proc.poll() is not None:
                raise VisionServerError(
                    "server_died",
                    f"mlx_vlm.server 子进程提前退出(exit={proc.returncode};常见:模型与权重"
                    f"不匹配 / 端口被占 / mlx-vlm 未装;输出已泵入统一日志 proc=vision 行)",
                    details={"exit_code": proc.returncode, "port": port},
                )
            running, healthy = _probe(config.local_base_url, timeout=timeout)
            if healthy:
                return {
                    "running": running,
                    "base_url": config.local_base_url,
                    "model": config.local_model,
                    "healthy": True,
                    "started": True,
                }
            time.sleep(poll_interval)
        # 超窗:先杀再抛 —— 半死进程不留孤儿(下一次 ensure 从干净状态重来)。
        _terminate_proc(proc)
        raise VisionServerError(
            "server_start_failed",
            f"{health_wait:.0f}s 内 {config.local_base_url}/models 未就绪,子进程已收尾"
            f"(Metal JIT 首载慢,可稍后重试 image.server.ensure;输出已泵入统一日志 proc=vision 行)",
            details={"port": port, "cmd": cmd},
        )
