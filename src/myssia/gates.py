"""Gates — ``<MYIA_HOME>/gates.yaml`` 门槛件知情启用配置(fail-closed).

e 路门槛化(D4,task 10-05-plugin-market-batch 批二):付费 SaaS / 第三方
留痕 / 自有实例 / 停更分析件的激活策略不落品类 YAML(AI 生成配置时不可能
无意开启付费通道),落全局配置文件 ``gates.yaml`` —— 与 ``vision.yaml``
同一位序(``<home>/gates.yaml``;路径解析在 desktop/entry.py ``_serve_context``
优先级链:显式 params > ``MYIA_HOME`` env > bundle 探测 > dev cwd)。

**fail-closed(D4 铁律)**:文件缺失 = 全关(未配置是合法态);文件损坏 /
未知字段 / 非法凭据引用 = :class:`LoadError` 结构化拒载,**调用侧以全关态
继续**(:func:`load_gates_fail_closed`)—— 门槛件永不因配置坏而意外打开,
doctor 出 warning 提示。门槛件任何失败(含引擎侧 ``gate_closed``)不拦核心
品类(security-baseline 铁律)。

凭据铁律与 vision.yaml 同门(security-baseline):``saas.<name>.api_key`` 与
``platforms.<name>.token`` 只收纯 ``keychain:`` 引用(明文与 ``env:`` 一律
拒载),键名走规范名空间 ``myia/saas/<name>-key`` / ``myia/platforms/<name>-token``。

装载与保存共用同一道门(:class:`GatesConfig` 构造即校验),保存
(:func:`save_gates_config`)只接收已构造的配置,tmp+rename 原子落盘。
"""

from __future__ import annotations

import os
import re
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

import yaml

from myssia.schema import (
    LoadError,
    LoadErrorDetail,
    SchemaValueError,
    parse_secret_value,
)

__all__ = [
    "GATES_FILE_NAME",
    "GATES_KINDS",
    "GatesConfig",
    "GatesLoadError",
    "PlatformGate",
    "SaaSGate",
    "canonical_saas_key_ref",
    "default_gates_path",
    "gate_open",
    "load_gates_config",
    "load_gates_fail_closed",
    "plugin_gate_key",
    "plugin_gate_open",
    "replace_analysis_switch",
    "replace_platform_gate",
    "replace_saas_gate",
    "save_gates_config",
    "valid_gate_key",
]

#: gates.yaml 文件名(置于应用数据根 <home>/ 下;路径解析在 desktop/entry.py)。
GATES_FILE_NAME = "gates.yaml"

#: ``myssia gates set`` 的合法 kind 词表(D7):前两个是总开关(无逐件名),
#: 后三个逐件(saas/platforms 带 keychain 凭据检查,analysis 纯布尔)。
GATES_KINDS = ("paid_engines", "third_party_trace", "saas", "platforms", "analysis")

#: saas/platforms/analysis 的逐件键名(小写标识符;官方件惯例 = 插件 id 去掉
#: ``myssia-`` 前缀,如 myssia-crawlab → platforms.crawlab)。
_GATE_KEY_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


def valid_gate_key(name: str) -> bool:
    """逐件键名是否合法(CLI ``gates set`` 目标解析与构造校验共用)。"""
    return isinstance(name, str) and bool(_GATE_KEY_RE.match(name))

#: 文档允许的顶层键(from_payload 未知键拒收的对照名单;version 必须为 1)。
_TOP_KEYS = ("version", "paid_engines", "third_party_trace", "saas", "platforms", "analysis")
_SAAS_KEYS = ("enabled", "api_key")
_PLATFORM_KEYS = ("enabled", "endpoint", "token")

#: saas 逐件凭据的规范缺省引用(创建新件时物化进配置,显式优于隐式)。
_SAAS_KEY_TEMPLATE = "keychain:myia/saas/{name}-key"


class GatesLoadError(LoadError):
    """gates.yaml 拒载(结构化明细与品类 :class:`LoadError` 同形状)。

    继承而非另立异常:CLI/doctor 的 ``LoadError`` 捕获与 ``to_dict`` 消费
    零改动;仅头行文案按本文件改写(不冒称「品类 YAML 校验失败」)。
    """

    def _format(self) -> str:
        head = f"gates.yaml 门槛配置校验失败,共 {len(self.errors)} 处"
        if self.source:
            head += f"({self.source})"
        lines = [head]
        for index, detail in enumerate(self.errors, start=1):
            lines.append(f"  {index}. [{detail.error_type}] {detail.path} — {detail.message}")
        return "\n".join(lines)


def _detail(path: str, code: str, message: str) -> LoadErrorDetail:
    return LoadErrorDetail(path, code, message)


@dataclass(frozen=True)
class SaaSGate:
    """付费 SaaS 引擎逐件门槛:{enabled, api_key(keychain 引用|None)}."""

    enabled: bool = False
    api_key_ref: str | None = None


@dataclass(frozen=True)
class PlatformGate:
    """自有实例逐件门槛:{enabled, endpoint(https 占位校验), token(钥匙串引用|None)}."""

    enabled: bool = False
    endpoint: str = ""
    token_ref: str | None = None


@dataclass(frozen=True)
class GatesConfig:
    """门槛配置(gates.yaml 的内存形态;构造即校验,非法值拒构造)。

    任何缺失/坏文件路径 → 全 False / 全空(fail-closed);``saas`` /
    ``platforms`` / ``analysis`` 的键名与凭据引用形态在构造期与
    :meth:`from_payload` 同门校验 —— 直接构造也不许绕过。
    """

    paid_engines: bool = False
    third_party_trace: bool = False
    saas: dict[str, SaaSGate] = field(default_factory=dict)
    platforms: dict[str, PlatformGate] = field(default_factory=dict)
    analysis: dict[str, bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        errors: list[LoadErrorDetail] = []
        for name in ("paid_engines", "third_party_trace"):
            value = getattr(self, name)
            if not isinstance(value, bool):
                errors.append(
                    _detail(name, "invalid_field", f"{name} 必须是布尔,当前为 {value!r}")
                )
        for key in self.saas:
            if not _GATE_KEY_RE.match(key):
                errors.append(
                    _detail(
                        f"saas.{key}",
                        "invalid_gate_key",
                        f"saas 键名 {key!r} 应为小写字母/数字/连字符/下划线且字母数字开头(1-64 字符)",
                    )
                )
        for key, gate in self.saas.items():
            if not isinstance(gate, SaaSGate):
                errors.append(
                    _detail(f"saas.{key}", "invalid_field", f"saas.{key} 必须是 SaaSGate,当前为 {type(gate).__name__}")
                )
                continue
            # 凭据引用形态构造期同门(复审补):直接构造/replace_saas_gate 裸
            # SaaSGate 也不许绕过 —— save 永远写不出 load 拒收的文件。
            errors.extend(_gate_ref_errors(gate.api_key_ref, f"saas.{key}.api_key"))
        for key in self.platforms:
            if not _GATE_KEY_RE.match(key):
                errors.append(
                    _detail(
                        f"platforms.{key}",
                        "invalid_gate_key",
                        f"platforms 键名 {key!r} 应为小写字母/数字/连字符/下划线且字母数字开头(1-64 字符)",
                    )
                )
        for key, gate in self.platforms.items():
            if not isinstance(gate, PlatformGate):
                errors.append(
                    _detail(f"platforms.{key}", "invalid_field", f"platforms.{key} 必须是 PlatformGate,当前为 {type(gate).__name__}")
                )
                continue
            if not isinstance(gate.endpoint, str):
                errors.append(
                    _detail(
                        f"platforms.{key}.endpoint",
                        "invalid_endpoint",
                        f"platforms.{key}.endpoint 必须是 http(s) 地址字符串,当前为 {gate.endpoint!r}",
                    )
                )
            elif gate.endpoint and not gate.endpoint.startswith(("http://", "https://")):
                errors.append(
                    _detail(
                        f"platforms.{key}.endpoint",
                        "invalid_endpoint",
                        f"platforms.{key}.endpoint 必须是 http(s) 地址(自有实例占位),当前为 {gate.endpoint!r}",
                    )
                )
            # token 引用形态构造期同门(复审补,与 saas.api_key 对称)
            errors.extend(_gate_ref_errors(gate.token_ref, f"platforms.{key}.token"))
        for key, value in self.analysis.items():
            if not _GATE_KEY_RE.match(key):
                errors.append(
                    _detail(
                        f"analysis.{key}",
                        "invalid_gate_key",
                        f"analysis 键名 {key!r} 应为小写字母/数字/连字符/下划线且字母数字开头(1-64 字符)",
                    )
                )
            if not isinstance(value, bool):
                errors.append(
                    _detail(f"analysis.{key}", "invalid_field", f"analysis.{key} 必须是布尔,当前为 {value!r}")
                )
        if errors:
            raise GatesLoadError(errors)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> GatesConfig:
        """从协议/文档字典构造(未知键拒收、类型逐字段校验;缺省键可省)。"""
        if not isinstance(payload, Mapping):
            raise GatesLoadError(
                [_detail("$", "gates_unreadable", f"gates 配置必须是对象,当前为 {type(payload).__name__}")]
            )
        errors: list[LoadErrorDetail] = []
        unknown = sorted(key for key in payload if key not in _TOP_KEYS)
        if unknown:
            errors.append(
                _detail(
                    "$",
                    "unknown_field",
                    f"存在未知字段: {unknown}(允许:{list(_TOP_KEYS)};手滑字段名不会静默失效)",
                )
            )
        version = payload.get("version", 1)
        if version != 1:
            errors.append(
                _detail("version", "unsupported_version", f"version 必须是 1,当前为 {version!r}")
            )
        switches: dict[str, bool] = {}
        for name in ("paid_engines", "third_party_trace"):
            value = payload.get(name, False)
            if not isinstance(value, bool):
                errors.append(_detail(name, "invalid_field", f"{name} 必须是布尔,当前为 {value!r}"))
            else:
                switches[name] = value
        saas = _parse_named_sections(payload, "saas", _SAAS_KEYS, errors)
        platforms = _parse_named_sections(payload, "platforms", _PLATFORM_KEYS, errors)
        analysis_raw = payload.get("analysis")
        analysis: dict[str, bool] = {}
        if analysis_raw is not None:
            if not isinstance(analysis_raw, Mapping):
                errors.append(_detail("analysis", "invalid_field", f"analysis 必须是对象,当前为 {analysis_raw!r}"))
            else:
                for key, value in analysis_raw.items():
                    path = f"analysis.{key}"
                    if not isinstance(key, str) or not _GATE_KEY_RE.match(key):
                        errors.append(
                            _detail(path, "invalid_gate_key", f"analysis 键名 {key!r} 应为小写字母/数字/连字符/下划线且字母数字开头(1-64 字符)")
                        )
                        continue
                    if not isinstance(value, bool):
                        errors.append(_detail(path, "invalid_field", f"{path} 必须是布尔,当前为 {value!r}"))
                    else:
                        analysis[key] = value
        if errors:
            raise GatesLoadError(errors)
        saas_gates = {
            key: SaaSGate(
                enabled=bool(section.get("enabled", False)),
                api_key_ref=_require_keychain_ref(section.get("api_key"), f"saas.{key}.api_key"),
            )
            for key, section in saas.items()
        }
        platform_gates = {
            key: PlatformGate(
                enabled=bool(section.get("enabled", False)),
                endpoint=section.get("endpoint") or "",
                token_ref=_require_keychain_ref(section.get("token"), f"platforms.{key}.token"),
            )
            for key, section in platforms.items()
        }
        return cls(
            paid_engines=switches.get("paid_engines", False),
            third_party_trace=switches.get("third_party_trace", False),
            saas=saas_gates,
            platforms=platform_gates,
            analysis=analysis,
        )

    def to_payload(self) -> dict[str, Any]:
        """协议/落盘视图(嵌套原文形状;keychain 引用原样回显,永不携带解析值)。"""
        return {
            "version": 1,
            "paid_engines": self.paid_engines,
            "third_party_trace": self.third_party_trace,
            "saas": {
                key: {"enabled": gate.enabled, "api_key": gate.api_key_ref}
                for key, gate in sorted(self.saas.items())
            },
            "platforms": {
                key: {"enabled": gate.enabled, "endpoint": gate.endpoint, "token": gate.token_ref}
                for key, gate in sorted(self.platforms.items())
            },
            "analysis": dict(sorted(self.analysis.items())),
        }


def _parse_named_sections(
    payload: Mapping[str, Any],
    name: str,
    allowed: tuple[str, ...],
    errors: list[LoadErrorDetail],
) -> dict[str, dict[str, Any]]:
    """取 ``saas``/``platforms`` 子节(None=空;非对象/坏键名/未知字段结构化拒收)."""
    raw = payload.get(name)
    if raw is None:
        return {}
    if not isinstance(raw, Mapping):
        errors.append(_detail(name, "invalid_field", f"{name} 必须是对象,当前为 {raw!r}"))
        return {}
    sections: dict[str, dict[str, Any]] = {}
    for key, section in raw.items():
        path = f"{name}.{key}"
        if not isinstance(key, str) or not _GATE_KEY_RE.match(key):
            errors.append(
                _detail(
                    path,
                    "invalid_gate_key",
                    f"{name} 键名 {key!r} 应为小写字母/数字/连字符/下划线且字母数字开头(1-64 字符)",
                )
            )
            continue
        if not isinstance(section, Mapping):
            errors.append(_detail(path, "invalid_field", f"{path} 必须是对象,当前为 {section!r}"))
            continue
        unknown = sorted(field_name for field_name in section if field_name not in allowed)
        if unknown:
            errors.append(
                _detail(path, "unknown_field", f"{path} 存在未知字段: {unknown}(允许:{list(allowed)})")
            )
            continue
        enabled = section.get("enabled", False)
        if not isinstance(enabled, bool):
            errors.append(_detail(f"{path}.enabled", "invalid_field", f"{path}.enabled 必须是布尔,当前为 {enabled!r}"))
            continue
        sections[key] = dict(section)
    return sections


def _require_keychain_ref(value: Any, field_name: str) -> str | None:
    """凭据位只收纯 ``keychain:`` 引用(security-baseline:明文/env: 拒载)。

    与 vision/settings.py 的 ``cloud.api_key`` 同门;返回 None = 未配置。
    """
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        raise GatesLoadError(
            [
                _detail(
                    field_name,
                    "invalid_field",
                    f"{field_name} 必须是 keychain: 引用字符串或 null",
                )
            ]
        )
    try:
        ref = parse_secret_value(value, label=field_name, allow_scheme=False)
    except SchemaValueError as exc:
        code = "credential_plaintext" if exc.code == "credential_plaintext" else "invalid_credential_ref"
        raise GatesLoadError(
            [
                _detail(
                    field_name,
                    code,
                    f"{field_name} {exc}(只接受 keychain: 引用;先 myssia secret set 写入再引用)",
                )
            ]
        ) from exc
    if ref.kind != "keychain":
        raise GatesLoadError(
            [
                _detail(
                    field_name,
                    "invalid_credential_ref",
                    f"{field_name} 只接受 keychain: 引用(收到 {value!r})",
                )
            ]
        )
    return value


def _gate_ref_errors(value: Any, field_name: str) -> list[LoadErrorDetail]:
    """构造期凭据引用校验(同门 :func:`_require_keychain_ref`,错误收集不抛)。

    :meth:`GatesConfig.__post_init__` 的批量收集风格适配:直接构造 /
    :func:`replace_saas_gate` 裸 :class:`SaaSGate` 与 ``from_payload`` 走
    同一道门 —— docstring「直接构造也不许绕过」的兑现点。
    """
    try:
        _require_keychain_ref(value, field_name)
    except GatesLoadError as exc:
        return exc.errors
    return []


def load_gates_config(path: Path | str) -> GatesConfig:
    """装载 gates.yaml;文件不存在 = 全关(合法未配置态,不报错)。

    Raises:
        LoadError: ``gates_unreadable``(文件不可读/YAML 无法解析/非对象)或
            构造校验的任一 error_type —— fail fast,绝不半载。调用侧
            (CLI 市场面/doctor/sidecar)经 :func:`load_gates_fail_closed`
            捕获后以全关态继续。
    """
    file_path = Path(path)
    if not file_path.exists():
        return GatesConfig()
    try:
        doc = yaml.safe_load(file_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise GatesLoadError(
            [_detail("$", "gates_unreadable", f"gates 配置无法解析: {file_path} ({exc})")],
            source=str(file_path),
        ) from exc
    if doc is None:  # 空文件 = 未配置态,与缺文件同权(fail-closed 全关)
        return GatesConfig()
    try:
        return GatesConfig.from_payload(doc)
    except GatesLoadError as exc:
        raise GatesLoadError(exc.errors, source=str(file_path)) from exc


def load_gates_fail_closed(path: Path | str) -> tuple[GatesConfig, dict[str, Any] | None]:
    """消费侧装载(市场面/doctor/引擎前置检查):坏文件 = 全关态继续。

    D4 fail-closed 的调用侧落地:门槛件永不因 gates.yaml 坏而意外打开;
    结构化错误(dict,``LoadError.to_dict`` 形状)带回给调用方落 doctor
    warning / list 顶层 ``error``,不是静默吞掉。
    """
    try:
        return load_gates_config(path), None
    except LoadError as exc:
        return GatesConfig(), exc.to_dict()


def save_gates_config(path: Path | str, config: GatesConfig) -> Path:
    """原子落盘(同目录临时文件 + ``os.replace``);入参已过构造校验,写路径零再判。"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(config.to_payload(), allow_unicode=True, sort_keys=False)
    tmp = file_path.with_name(file_path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.replace(tmp, file_path)
    return file_path


def default_gates_path() -> Path:
    """CLI 侧缺省路径:``MYIA_HOME`` env > ``~/.myia/gates.yaml``。

    与安装根 ``~/.myia/plugins`` 同一根(CLI 每用户目录);桌面 sidecar 不走
    本函数 —— 它在 desktop/entry.py 经 ``_serve_context`` 优先级链解析出
    ``<home>/gates.yaml``(与 vision.yaml 同位),env 名同一 ``MYIA_HOME``。
    """
    env_home = os.environ.get("MYIA_HOME")
    if env_home:
        return Path(env_home).expanduser() / GATES_FILE_NAME
    return Path.home() / ".myia" / GATES_FILE_NAME


def gate_open(config: GatesConfig, kind: str, name: str | None = None) -> bool:
    """门槛状态唯一查询口(引擎/插件/市场面共用;未知键 = 关,fail-closed)。

    - ``paid_engines`` / ``third_party_trace``:总开关(name 不适用);
    - ``saas``:总开关 ∧ 逐件开关(§6.3:任一未开即 ``gate_closed``);
    - ``platforms`` / ``analysis``:逐件开关(无总开关)。

    逐件键不在 gates.yaml = 未配置 = 关(不是错误);kind 拼错是编程错误,
    当场抛 ValueError 而不是静默全关。
    """
    if kind in ("paid_engines", "third_party_trace"):
        return bool(getattr(config, kind))
    if kind == "saas":
        if name is None:
            raise ValueError("gate_open(kind='saas') 需要逐件名,如 gate_open(config, 'saas', 'zenrows')")
        gate = config.saas.get(name)
        return config.paid_engines and gate is not None and gate.enabled
    if kind == "platforms":
        if name is None:
            raise ValueError("gate_open(kind='platforms') 需要逐件名,如 gate_open(config, 'platforms', 'crawlab')")
        gate = config.platforms.get(name)
        return gate is not None and gate.enabled
    if kind == "analysis":
        if name is None:
            raise ValueError("gate_open(kind='analysis') 需要逐件名,如 gate_open(config, 'analysis', 'snownlp_sentiment')")
        return config.analysis.get(name, False)
    raise ValueError(f"未知门槛 kind {kind!r}(合法:{list(GATES_KINDS)})")


def plugin_gate_key(plugin_id: str) -> str:
    """manifest 件 → gates.yaml 逐件键:官方惯例去掉 ``myssia-`` 前缀。

    myssia-crawlab → ``crawlab``;不带前缀的 id 原样使用(社区件自担命名)。
    """
    return plugin_id.removeprefix("myssia-")


def plugin_gate_open(config: GatesConfig, gate: str, plugin_id: str) -> bool:
    """manifest ``gate`` 字段 → gates.yaml 状态派生(plugin list 徽标/doctor 用)。

    - ``paid`` → saas 逐件(内含 paid_engines 总开关);
    - ``trace`` → third_party_trace 总开关(当前无执法点,D9);
    - ``platform`` → platforms 逐件(组织性不执法,D6);
    - ``stale`` → analysis 逐件(批三解锁,D8)。
    """
    key = plugin_gate_key(plugin_id)
    if gate == "paid":
        return gate_open(config, "saas", key)
    if gate == "trace":
        return gate_open(config, "third_party_trace")
    if gate == "platform":
        return gate_open(config, "platforms", key)
    if gate == "stale":
        return gate_open(config, "analysis", key)
    raise ValueError(f"未知 manifest gate {gate!r}(合法:paid/trace/platform/stale;缺省不声明=无门槛件)")


def replace_saas_gate(config: GatesConfig, name: str, gate: SaaSGate) -> GatesConfig:
    """返回替换了一个 saas 逐件的新配置(不可变风格;键名走同门校验)。"""
    saas = dict(config.saas)
    saas[name] = gate
    return replace(config, saas=saas)


def replace_platform_gate(config: GatesConfig, name: str, gate: PlatformGate) -> GatesConfig:
    """返回替换了一个 platforms 逐件的新配置(不可变风格;键名走同门校验)。"""
    platforms = dict(config.platforms)
    platforms[name] = gate
    return replace(config, platforms=platforms)


def replace_analysis_switch(config: GatesConfig, name: str, value: bool) -> GatesConfig:
    """返回替换了一个 analysis 开关的新配置(不可变风格;键名走同门校验)。"""
    analysis = dict(config.analysis)
    analysis[name] = value
    return replace(config, analysis=analysis)


def canonical_saas_key_ref(name: str) -> str:
    """saas 逐件的规范缺省钥匙串引用(``keychain:myia/saas/<name>-key``)。"""
    return _SAAS_KEY_TEMPLATE.format(name=name)
