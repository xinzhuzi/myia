"""桥组件配置面(task 10-11-wechat-ui-bridge design §7;执行者不发明配置键)。

两层配置,本模块只管**桥组件侧**:

- **MYIA push 节**(``wechat_bridge_bin`` / ``weixin_local_enabled``)归
  MYIA 本体 push 层(Phase F,对齐 ``weixin_hermes_bin`` 惯例),桥不读它。
- **桥组件侧** = 数据根私有区 ``wechat-bridge/config.json``,全部有缺省、
  **缺文件可用**(设计原文);键封闭清单:
  ``domains``(G4 缺省 message/session/contact)、
  ``limits``(AC2 参数化:sessions=20/messages=50/history_days=30)、
  ``copy_ttl_hours``(G5=24;**0 合法 = 永不过期**,localdb TTL 判定 0 =
  恒新鲜跳过重建;负数拒)/ ``copy_capacity_mb``(G5 容量上限,缺省 512)、
  ``mem_search_enabled``(D4 豁免开关,缺省关——design §4「开关默认关,
  主人显式开启才生效」;2026-10-11 主人「全部解决」令授权以配置键落位,
  替代 E1 空壳期的「无配置键」口径)、
  ``key_provider_path``(外部取钥器可执行文件路径,缺省空 = 未配置 =
  现状行为;task 10-13-wechat-keyprovider B2,协议 = docs/wechat-keyprovider.md,
  管理命令 ``localdb key-provider set|get|clear`` 代写)。
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
    "KEY_PROVIDER_PATH_DEFAULT",
    "LOCALDB_KEYS_REL_PATH",
    "MEM_SEARCH_ENABLED_DEFAULT",
    "MESSAGES_DEFAULT",
    "MYIA_HOME_ENV",
    "SESSIONS_DEFAULT",
    "SEND_STATE_REL_PATH",
    "BridgeConfig",
    "load_config",
    "myssia_home",
    "save_config_key",
]

#: MYIA 数据根 env 覆写名(壳 spawn 注入;main.rs data_root 同名锚点)。
MYIA_HOME_ENV = "MYIA_HOME"

#: 桥配置目录名(数据根下;design §7「数据根私有区 wechat-bridge/config.json」)。
BRIDGE_CONFIG_DIR_NAME = "wechat-bridge"
#: 频控状态目录名(design §2「数据根/wechat-localdb/send_state.json」——与
#: 配置目录是两个名字,照设计原文,不擅自归一)。
SEND_STATE_REL_PATH = "wechat-localdb/send_state.json"
#: 本地库密钥缓存(Phase E1;design §5.3「all_keys.json 类产物存数据根私有
#: 区并 600 权限」——仅验证通过的 key 落此,当前 E1 实测零命中故恒缺省)。
LOCALDB_KEYS_REL_PATH = "wechat-localdb/keys.json"
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
#: D4 豁免开关缺省(design §4:内存密钥搜索开关默认关,主人显式开启才生效;
#: 2026-10-11「全部解决」令把 E1 空壳期的「无配置键」口径改写为配置可启)。
MEM_SEARCH_ENABLED_DEFAULT = False
#: 外部取钥器路径缺省(task 10-13-wechat-keyprovider B2;协议 v1 =
#: docs/wechat-keyprovider.md。空串 = 未配置 = 现状行为:查询链不 spawn
#: 取钥器、不取钥;桥对取钥器零来源校验——风险件用户自备、自行担责)。
KEY_PROVIDER_PATH_DEFAULT = ""

_ALLOWED_TOP_KEYS = frozenset(
    {
        "domains",
        "limits",
        "copy_ttl_hours",
        "copy_capacity_mb",
        "mem_search_enabled",
        "key_provider_path",
    }
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
    #: D4 豁免开关(缺省关;真跑还须提权 + 主人裁决在案,三重门见 memsearch)。
    mem_search_enabled: bool = MEM_SEARCH_ENABLED_DEFAULT
    #: 外部取钥器可执行文件路径(B2;空 = 未配置 = 现状行为。运行期消费在
    #: localdb.resolve_keys:密钥缓存缺失且已配置 → 按协议 spawn;配置文件
    #: 存在性/可执行性不在装载期判(get 命令与 spawn 失败如实报)。
    key_provider_path: str = KEY_PROVIDER_PATH_DEFAULT
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
            "mem_search_enabled": self.mem_search_enabled,
            "key_provider_path": self.key_provider_path,
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
    # copy_ttl_hours:0 合法 = 永不过期(用户直觉语义:localdb TTL 判定
    # 0 = 恒新鲜、跳过重建);负数仍拒。copy_capacity_mb 须正整数(0 容量
    # = 什么都装不下,无合法语义)。
    value = raw.get("copy_ttl_hours")
    if value is not None:
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise BridgeError(
                EXIT_USAGE,
                f"桥配置 copy_ttl_hours 须为非负整数(0 = 永不过期),当前为 {value!r}",
            )
        values["copy_ttl_hours"] = value
    value = raw.get("copy_capacity_mb")
    if value is not None:
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise BridgeError(
                EXIT_USAGE, f"桥配置 copy_capacity_mb 须为正整数,当前为 {value!r}"
            )
        values["copy_capacity_mb"] = value
    mem_search_enabled = raw.get("mem_search_enabled")
    if mem_search_enabled is not None and not isinstance(mem_search_enabled, bool):
        raise BridgeError(
            EXIT_USAGE,
            f"桥配置 mem_search_enabled 须为布尔(true/false),当前为 {mem_search_enabled!r}",
            code="usage",
            fix_hint="D4 豁免开关只认布尔;开启 = true(真跑还须提权,memsearch 三重门)",
        )
    key_provider_path = raw.get("key_provider_path")
    if key_provider_path is not None and not isinstance(key_provider_path, str):
        raise BridgeError(
            EXIT_USAGE,
            f"桥配置 key_provider_path 须为字符串(取钥器可执行文件路径;空串 = 未配置),"
            f"当前为 {key_provider_path!r}",
            code="usage",
            fix_hint="外部取钥器路径配置;wechat-bridge localdb key-provider set <path> 可代写并校验",
        )
    return BridgeConfig(
        domains=[str(item).strip() for item in domains],
        sessions=values.get("sessions", SESSIONS_DEFAULT),
        messages=values.get("messages", MESSAGES_DEFAULT),
        history_days=values.get("history_days", HISTORY_DAYS_DEFAULT),
        copy_ttl_hours=values.get("copy_ttl_hours", COPY_TTL_HOURS_DEFAULT),
        copy_capacity_mb=values.get("copy_capacity_mb", COPY_CAPACITY_MB_DEFAULT),
        mem_search_enabled=(
            MEM_SEARCH_ENABLED_DEFAULT
            if mem_search_enabled is None
            else mem_search_enabled
        ),
        key_provider_path=(
            KEY_PROVIDER_PATH_DEFAULT
            if key_provider_path is None
            else key_provider_path.strip()
        ),
        source=str(config_path),
    )


def save_config_key(
    key: str,
    value: Any | None,
    *,
    path: Path | None = None,
    data_root: Path | None = None,
) -> Path:
    """管理命令的配置代写面(B2;``localdb key-provider set|clear`` 唯一后端)。

    外科式改单键:先经 :func:`load_config` 同门校验既有文件(坏文件拒改,
    不把用户的配置写花),再原样保留其余键改写目标键,原子落盘(tmp+rename,
    600/目录 700——数据根私有区纪律)。``value=None`` = 删除该键(= 回缺省)。

    本函数只收**顶层标量键**(``key_provider_path`` 族);limits 子键与整表
    替换不在管理命令面(用户直改文件,load_config 全量校验兜底)。
    """
    if key not in _ALLOWED_TOP_KEYS or key == "limits" or key == "domains":
        raise BridgeError(
            EXIT_USAGE,
            f"save_config_key 只支持顶层标量键,不支持: {key!r}",
            code="usage",
        )
    config_path = path if path is not None else default_config_path(data_root)
    load_config(config_path)  # 同门校验:既有文件坏 = 拒改(fail-fast,不写花)
    raw: dict[str, Any] = {}
    if config_path.is_file():
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            raw = loaded
    if value is None:
        raw.pop(key, None)
    else:
        raw[key] = value
    config_path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(config_path.parent, 0o700)
    tmp = config_path.with_name(f"{config_path.name}.tmp-{os.getpid()}")
    try:
        tmp.write_text(
            json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
        os.chmod(tmp, 0o600)
        os.replace(tmp, config_path)
    finally:
        if tmp.exists():
            tmp.unlink()
    return config_path
