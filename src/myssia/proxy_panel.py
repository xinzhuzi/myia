"""代理池管理面板 sidecar 协议面(task 10-14-proxy-pool-panel R1)。

两个协议动作的实现本体(``desktop/entry.py`` ``_HANDLERS`` 只注册
:func:`make_proxy_panel_handlers` 产出的薄壳,集成接线见任务档
integrationSpec;判例同 :mod:`myssia.wechat_stats_sidecar`):

- ``proxy.probe`` ``{config?, config_auto?, probe_timeout?}``(形状 =
  DoctorParams 子集)→ **字面内部复用** entry ``_m_doctor``(零逻辑分叉,
  ``config_auto`` 非布尔的 invalid_params 门在 doctor 内原样生效)→
  应答 = doctor 应答原形状 + 纯增键 ``snapshot: {persisted, reason?}``;
  随后把 ``payload.proxy``(config + pools 打码行,引擎 ``mask_proxy_url``
  已打码)作为一条快照追加落盘。落盘失败不 fail 探测(探测结果已到手,
  ``persisted=false`` + 原因如实回);dev 无 home → 探测照跑、
  ``persisted=false, reason="no_home"``(G10 dev 回退同款降级)。
- ``proxy.history`` ``{limit?, pool?}`` → 零网络纯读:
  ``{snapshots:[{at, config, pools}…], count, truncated, home_available,
  skipped}``(新→旧)。limit 钳制 [1,100] 缺省 20;pool 给值只回该池行;
  坏行/不可解析行跳过且 ``skipped`` 如实计数(logs backfill 坏行跳过
  先例);文件不存在 = 合法空表。``home_available=false`` = dev 无数据根
  (历史无处落),面板空态据此说明,不发探测探路(挂载零网络红线)。

持久化落点 = ``<home>/proxy-probe-history.jsonl``:一行一条快照
``{at, config, pools}``(pools 行已打码,PRD 红线 4);append 后超
``HISTORY_KEEP_MAX``(200)条裁最旧并原子重写(tmp 先 chmod 0600 再
``os.replace``,最终态即 0600 —— telegram/web_backup.py 权限纪律同款);
文件创建即 0600(``os.open`` O_CREAT 带 mode,内容虽已打码,防御纵深
顺手事);无 home 不落盘。

本模块零引擎依赖(不动 fetch_base/pipeline;D7「健康状态 run 内即焚」
决议不翻案,这里只是把 doctor 探测**应答**存档);serve 单线程
(entry.py ``_handle_line`` 串行)下 append+裁旧无并发竞态。
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Protocol

__all__ = [
    "PROBE_HISTORY_FILENAME",
    "HISTORY_KEEP_MAX",
    "HISTORY_LIMIT_DEFAULT",
    "HISTORY_LIMIT_MAX",
    "HISTORY_LIMIT_MIN",
    "PROBE_HISTORY_FILE_MODE",
    "append_snapshot",
    "clamp_limit",
    "make_proxy_panel_handlers",
    "read_history",
]

#: 快照历史文件名(``<home>/proxy-probe-history.jsonl``;``<home>`` 文件
#: 落位先例 = gates.yaml / remote-plugins.json)。
PROBE_HISTORY_FILENAME = "proxy-probe-history.jsonl"

#: 保留帽:append 后超此数裁最旧(PRD R1.3)。
HISTORY_KEEP_MAX = 200

#: ``proxy.history`` limit 钳制窗与缺省(PRD R1.2)。
HISTORY_LIMIT_MIN = 1
HISTORY_LIMIT_MAX = 100
HISTORY_LIMIT_DEFAULT = 20

#: 快照文件权限(创建即 0600;镜像 keystore/登录标记的凭据面纪律——
#: 内容虽已打码,防御纵深顺手事,设计拷问修正④)。
PROBE_HISTORY_FILE_MODE = 0o600


class ProtocolErrorFactory(Protocol):
    """entry.ProtocolError 的构造面(依赖注入;code/message/path 同形)。"""

    def __call__(self, code: str, message: str, *, path: str = "$") -> Any: ...


def _now_utc() -> datetime:
    """快照时间戳源(可注入定轴;默认真实 UTC 时钟)。"""
    return datetime.now(timezone.utc)


def clamp_limit(value: int) -> int:
    """钳制 ``proxy.history`` limit 进 [1,100](类型门在调用侧)。"""
    return max(HISTORY_LIMIT_MIN, min(HISTORY_LIMIT_MAX, value))


def _read_raw_lines(path: Path) -> list[str]:
    """逐字节读行(``splitlines`` 保内容;解码坏字节替换成坏行跳过)。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text.splitlines()


def _atomic_rewrite(path: Path, lines: list[str]) -> None:
    """同目录 tmp(0600)+ ``os.replace`` 原子重写(entry `_atomic_write_text`
    同判例;tmp 先 chmod 再 replace,最终态即 0600)。"""
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, PROBE_HISTORY_FILE_MODE)
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
        handle.write("".join(line + "\n" for line in lines))
    os.chmod(tmp, PROBE_HISTORY_FILE_MODE)  # 已存在旧 tmp 的兜底(umask 不放大权限)
    os.replace(tmp, path)


def append_snapshot(home: Path, snapshot: dict[str, Any]) -> None:
    """一条快照追加落盘 + 超帽裁最旧(OSError 上抛 → 调用侧转 persisted=false)。

    单纯 append 走 ``os.open(O_APPEND|O_CREAT, 0o600)``:创建即 0600,
    无「先 644 后补 chmod」窗口;既有文件权限偏差顺手收紧(失败不拦)。
    裁旧重读重写属尽力而为(读失败只留帽外多几行,下次成功即收)。
    """
    path = home / PROBE_HISTORY_FILENAME
    line = json.dumps(snapshot, ensure_ascii=False)
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, PROBE_HISTORY_FILE_MODE)
    with os.fdopen(fd, "a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    try:
        os.chmod(path, PROBE_HISTORY_FILE_MODE)
    except OSError:  # pragma: no cover - 异常 FS 的防御纵深,不拦探测应答
        pass
    try:
        lines = _read_raw_lines(path)
    except OSError:  # pragma: no cover - append 已成功,读失败只跳过裁旧
        return
    if len(lines) > HISTORY_KEEP_MAX:
        try:
            _atomic_rewrite(path, lines[-HISTORY_KEEP_MAX:])
        except OSError:  # pragma: no cover - 同上,帽外多几行不是失败态
            return


def read_history(
    home: Path | None, *, limit: int, pool: str | None = None
) -> dict[str, Any]:
    """纯读快照历史(新→旧;坏行跳过且 ``skipped`` 如实计数)。

    - ``home=None``(dev)或文件不存在 → 合法空表(``home_available`` 如实);
    - ``pool`` 给值:快照的 pools 只留该池行,无该池的快照整条不出;
    - ``count`` = 本答应答行数;``truncated`` = 窗外还有(池过滤后)。
    """
    if home is None:
        return {
            "snapshots": [],
            "count": 0,
            "truncated": False,
            "home_available": False,
            "skipped": 0,
        }
    path = home / PROBE_HISTORY_FILENAME
    base: dict[str, Any] = {
        "snapshots": [],
        "count": 0,
        "truncated": False,
        "home_available": True,
        "skipped": 0,
    }
    if not path.exists():
        return base
    try:
        lines = _read_raw_lines(path)
    except OSError:  # pragma: no cover - 读不出的文件按空表 + 全量坏行
        base["skipped"] = 1
        return base
    valid: list[dict[str, Any]] = []
    skipped = 0
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue  # 空行不算坏行(人为编辑痕迹,静默忽略)
        try:
            obj = json.loads(stripped)
        except ValueError:
            skipped += 1
            continue
        if not isinstance(obj, dict) or not isinstance(obj.get("at"), str):
            skipped += 1
            continue
        pools = obj.get("pools")
        if not isinstance(pools, list):
            skipped += 1
            continue
        config = obj.get("config")
        if config is not None and not isinstance(config, str):
            config = None
        rows = pools
        if pool is not None:
            rows = [row for row in pools if isinstance(row, dict) and row.get("pool") == pool]
            if not rows:
                continue
        valid.append({"at": obj["at"], "config": config, "pools": rows})
    valid.reverse()  # 文件旧→新,应答新→旧
    base["truncated"] = len(valid) > limit
    base["snapshots"] = valid[:limit]
    base["count"] = len(base["snapshots"])
    base["skipped"] = skipped
    return base


def _snapshot_of(payload: dict[str, Any], now: datetime) -> dict[str, Any] | None:
    """doctor 应答 → 快照行(``proxy`` 节形状不符 → None,不硬造)。"""
    proxy = payload.get("proxy")
    if not isinstance(proxy, dict):
        return None
    pools = proxy.get("pools")
    if not isinstance(pools, list):
        pools = []
    config = proxy.get("config")
    if config is not None and not isinstance(config, str):
        config = None
    return {
        "at": now.astimezone(timezone.utc).isoformat(timespec="milliseconds"),
        "config": config,
        "pools": pools,
    }


def make_proxy_panel_handlers(
    *,
    doctor: Callable[[dict[str, Any]], dict[str, Any]],
    home_resolver: Callable[[], Path | None],
    protocol_error: ProtocolErrorFactory,
    now: Callable[[], datetime] = _now_utc,
) -> dict[str, Callable[[dict[str, Any]], dict[str, Any]]]:
    """产出 ``proxy.probe`` / ``proxy.history`` 两 handler(entry 依赖全注入)。

    entry.py 集成接线(一行)::

        _HANDLERS.update(make_proxy_panel_handlers(
            doctor=_m_doctor, home_resolver=lambda: _serve_context().home,
            protocol_error=ProtocolError))

    Args:
        doctor: entry ``_m_doctor``(字面内部复用,零逻辑分叉;config_auto
            非布尔门在其中原样生效)。
        home_resolver: 返回 serve 上下文数据根(dev 回退 None)。
        protocol_error: entry ``ProtocolError`` 构造器(参数门错误直上协议面)。
        now: 快照时间戳源(测试定轴注入)。
    """

    def _bad(message: str, path: str) -> Any:
        return protocol_error("invalid_params", message, path=path)

    def _m_proxy_probe(params: dict[str, Any]) -> dict[str, Any]:
        payload = dict(doctor(params))
        snapshot_meta: dict[str, Any] = {"persisted": False}
        snapshot = _snapshot_of(payload, now())
        home = home_resolver()
        if home is None:
            snapshot_meta["reason"] = "no_home"
        elif snapshot is None:
            # doctor 应答无 proxy 节(形状漂移)——探测结果照回,不落盘
            snapshot_meta["reason"] = "no_proxy_section"
        else:
            try:
                append_snapshot(home, snapshot)
                snapshot_meta = {"persisted": True}
            except OSError as exc:
                snapshot_meta["reason"] = f"write_failed: {exc}"
        payload["snapshot"] = snapshot_meta
        return payload

    def _m_proxy_history(params: dict[str, Any]) -> dict[str, Any]:
        limit_raw = params.get("limit")
        if limit_raw is None:
            limit = HISTORY_LIMIT_DEFAULT
        elif isinstance(limit_raw, bool) or not isinstance(limit_raw, int):
            raise _bad("limit 必须是整数", "params.limit")
        else:
            limit = clamp_limit(limit_raw)
        pool = params.get("pool")
        if pool is not None and (not isinstance(pool, str) or not pool):
            raise _bad("pool 必须是非空字符串", "params.pool")
        home = home_resolver()
        result = read_history(home, limit=limit, pool=pool)
        if pool is not None:
            # 池过滤行化:调用方给定池名原样回带(应答自描述)
            result["pool"] = pool
        return result

    return {
        "proxy.probe": _m_proxy_probe,
        "proxy.history": _m_proxy_history,
    }
