"""桥组件配置面(task 10-11-wechat-ui-bridge design §7;执行者不发明配置键)。

两层配置,本模块只管**桥组件侧**:

- **MYIA push 节**(``wechat_bridge_bin`` / ``weixin_local_enabled``)归
  MYIA 本体 push 层(Phase F,对齐 ``weixin_hermes_bin`` 惯例),桥不读它。
- **桥组件侧** = 数据根私有区 ``wechat-bridge/config.json``,全部有缺省、
  **缺文件可用**(设计原文);键封闭清单:
  ``domains``(G4 缺省 message/session/contact)、
  ``limits``(AC2 参数化:sessions=20/messages=50/history_days=30)、
  ``copy_ttl_hours``(G5=24)/ ``copy_capacity_mb``(G5 容量上限,缺省 512)。
  **无频控键**(G6 硬编码,刻意不提供——design §7 原文)。

数据根解析与 MYIA 本体同源(desktop/entry.py ``myssia_home`` /
desktop/src-tauri/main.rs ``data_root`` 同一序):显式 ``MYIA_HOME`` env
优先,darwin ``~/Library/Application Support/MYIA``,Linux/其余 ``~/.myia``。

未知键/形状错 **fail-fast**(exit 2 usage,结构化明细)——与仓库 schema
文化一致;频控键若出现在配置里同样拒载(G6 是红线不是默认值)。
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .codes import EXIT_USAGE, BridgeError

__all__ = [
    "BRIDGE_CONFIG_DIR_NAME",
    "BRIDGE_CONFIG_REL_PATH",
    "COPY_CAPACITY_MB_DEFAULT",
    "COPY_TTL_HOURS_DEFAULT",
    "DEFAULT_DOMAINS",
    "HISTORY_DAYS_DEFAULT",
    "MESSAGES_DEFAULT",
    "MYIA_HOME_ENV",
    "SESSIONS_DEFAULT",
    "SEND_STATE_REL_PATH",
    "BridgeConfig",
    "load_config",
    "myssia_home",
]

#: MYIA 数据根 env 覆写名(壳 spawn 注入;main.rs data_root 同名锚点)。
MYIA_HOME_ENV = "MYIA_HOME"

#: 桥配置目录名(数据根下;design §7「数据根私有区 wechat-bridge/config.json」)。
BRIDGE_CONFIG_DIR_NAME = "wechat-bridge"
#: 频控状态目录名(design §2「数据根/wechat-localdb/send_state.json」——与
#: 配置目录是两个名字,照设计原文,不擅自归一)。
SEND_STATE_REL_PATH = "wechat-localdb/send_state.json"
#: 桥配置文件相对数据根的路径。
BRIDGE_CONFIG_REL_PATH = f"{BRIDGE_CONFIG_DIR_NAME}/config.json"

# —— §7 键缺省值(唯一出处;component.json 的 config_defaults 抄这里)——
#: G4 域清单缺省(message + session + contact 三域,配置可扩)。
DEFAULT_DOMAINS: list[str] = ["message", "session", "contact"]
#: AC2 参数化:sessions list 首版 N=20。
SESSIONS_DEFAULT = 20
#: AC2 参数化:messages read 首版 K=50。
MESSAGES_DEFAULT = 50
#: AC7/E3:历史查询缺省窗口 30 天。
HISTORY_DAYS_DEFAULT = 30
#: G5:解密副本 TTL(小时)。
COPY_TTL_HOURS_DEFAULT = 24
#: G5:解密副本容量上限(design §7 未钉数值,取 512MB 并随戳披露)。
COPY_CAPACITY_MB_DEFAULT = 512

_ALLOWED_TOP_KEYS = frozenset(
    {"domains", "limits", "copy_ttl_hours", "copy_capacity_mb"}
)
_ALLOWED_LIMIT_KEYS = frozenset({"sessions", "messages", "history_days"})


def myssia_home() -> Path:
    """MYIA 数据根(MYIA_HOME env > 平台缺省;与 entry.py 同序同值)。"""
    override = (os.environ.get(MYIA_HOME_ENV) or "").strip()
    if override:
        return Path(override).expanduser()
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "MYIA"
    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        root = Path(base) if base else Path.home() / "AppData" / "Roaming"
        return root / "MYIA"
    return Path.home() / ".myia"


@dataclass(frozen=True)
class BridgeConfig:
    """桥组件侧配置(§7 键封闭;缺文件 = 全缺省)。"""

    domains: list[str] = field(default_factory=lambda: list(DEFAULT_DOMAINS))
    sessions: int = SESSIONS_DEFAULT
    messages: int = MESSAGES_DEFAULT
    history_days: int = HISTORY_DAYS_DEFAULT
    copy_ttl_hours: int = COPY_TTL_HOURS_DEFAULT
    copy_capacity_mb: int = COPY_CAPACITY_MB_DEFAULT
    #: 配置实际来源(None = 缺文件全缺省,health/诊断如实呈现)。
    source: str | None = None

    def to_payload(self) -> dict[str, Any]:
        """诊断面形状(probe/doctor 可复用;不含敏感内容,纯配置形状)。"""
        return {
            "domains": list(self.domains),
            "limits": {
                "sessions": self.sessions,
                "messages": self.messages,
                "history_days": self.history_days,
            },
            "copy_ttl_hours": self.copy_ttl_hours,
            "copy_capacity_mb": self.copy_capacity_mb,
            "source": self.source,
        }


def default_config_path(data_root: Path | None = None) -> Path:
    """桥配置文件绝对路径(数据根私有区 wechat-bridge/config.json)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / BRIDGE_CONFIG_DIR_NAME / "config.json"


def load_config(path: Path | None = None, *, data_root: Path | None = None) -> BridgeConfig:
    """读桥配置:缺文件 → 全缺省(设计原文「缺文件可用」);坏文件 fail-fast。

    Raises:
        BridgeError: exit 2(usage 段)——JSON 不可解析 / 顶层或 limits 出现
            未知键 / 形状不符。**出现频控类键同样拒**(G6:频控是硬编码
            红线,配置面刻意不提供,写进来 = 契约漂移,静默忽略会造出
            「配置了却没生效」的假象)。
    """
    config_path = path if path is not None else default_config_path(data_root)
    if not config_path.is_file():
        return BridgeConfig()
    try:
        raw: Any = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise BridgeError(
            EXIT_USAGE,
            f"桥配置文件不可读或非合法 JSON: {config_path}({type(exc).__name__})",
            code="usage",
            fix_hint="修正 JSON 语法,或删除该文件回落全缺省配置",
        ) from exc
    if not isinstance(raw, dict):
        raise BridgeError(
            EXIT_USAGE,
            f"桥配置顶层须为键值映射,当前为 {type(raw).__name__}: {config_path}",
            code="usage",
        )
    unknown = sorted(set(raw) - _ALLOWED_TOP_KEYS)
    if unknown:
        raise BridgeError(
            EXIT_USAGE,
            f"桥配置含未知键 {unknown}(封闭清单: {sorted(_ALLOWED_TOP_KEYS)};G6 频控无配置键)",
            code="usage",
            fix_hint="删除未知键;域/上限/TTL 之外的一律不许配置(design §7)",
        )
    limits_raw = raw.get("limits", {})
    if not isinstance(limits_raw, dict):
        raise BridgeError(
            EXIT_USAGE, f"桥配置 limits 须为键值映射,当前为 {type(limits_raw).__name__}", code="usage"
        )
    unknown_limits = sorted(set(limits_raw) - _ALLOWED_LIMIT_KEYS)
    if unknown_limits:
        raise BridgeError(
            EXIT_USAGE,
            f"桥配置 limits 含未知键 {unknown_limits}(封闭清单: {sorted(_ALLOWED_LIMIT_KEYS)})",
            code="usage",
        )
    domains = raw.get("domains", list(DEFAULT_DOMAINS))
    if not isinstance(domains, list) or not domains or not all(
        isinstance(item, str) and item.strip() for item in domains
    ):
        raise BridgeError(
            EXIT_USAGE,
            "桥配置 domains 须为非空字符串列表(G4 三域缺省;配置可扩但不可为空)",
            code="usage",
        )
    values: dict[str, int] = {}
    for key in sorted(_ALLOWED_LIMIT_KEYS):
        value = limits_raw.get(key)
        if value is None:
            continue
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise BridgeError(
                EXIT_USAGE,
                f"桥配置 limits.{key} 须为正整数,当前为 {value!r}",
                code="usage",
            )
        values[key] = value
    for key in ("copy_ttl_hours", "copy_capacity_mb"):
        value = raw.get(key)
        if value is None:
            continue
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise BridgeError(
                EXIT_USAGE, f"桥配置 {key} 须为正整数,当前为 {value!r}", code="usage"
            )
        values[key] = value
    return BridgeConfig(
        domains=[str(item).strip() for item in domains],
        sessions=values.get("sessions", SESSIONS_DEFAULT),
        messages=values.get("messages", MESSAGES_DEFAULT),
        history_days=values.get("history_days", HISTORY_DAYS_DEFAULT),
        copy_ttl_hours=values.get("copy_ttl_hours", COPY_TTL_HOURS_DEFAULT),
        copy_capacity_mb=values.get("copy_capacity_mb", COPY_CAPACITY_MB_DEFAULT),
        source=str(config_path),
    )
