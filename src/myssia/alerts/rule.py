"""Alert rule construction gate(构造期拒,PRD 10-04-alert-rules grill Q7).

存储层(:class:`myssia.store.models.AlertRule`)是纯行 ↔ 对象记录;本模块是
读库(store 载入)与写库(alerts.save)共用的同一道构造门:

- name 非空 / action ∈ {push, tag} / scope ∈ {'global'} ∪ 已知品类;
- ``when`` 表达式经 classify 白名单 AST 试建(:class:`myssia_classifier Rule`,
  与 ``RouteRule.__post_init__`` 同构):属性访问/下标/lambda/超 1000 字符等
  越权构造在装载期即拒;
- ``action_config`` 形状:push 需 ``channel ∈ myssia.push.CHANNELS`` + 可选
  ``targets: list[str]`` / ``template: str``;tag 需非空 ``tags: list[str]``;
  未知键拒(schema 铁律:未知字段不许静默忽略)。

读库坏行 = 调用方(:meth:`AlertEngine.compile_rules`)单行 WARNING 跳过
(隔离);写库 = alerts.save 结构化拒整批(Stage D)。
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Sequence

from myssia.classify.custom import Rule, RuleSyntaxError
from myssia.push import CHANNELS
from myssia.push.route import CATEGORY_DEFAULT_ROUTES
from myssia.store.models import (
    ALERT_ACTION_PUSH,
    ALERT_ACTION_TAG,
    ALERT_RULE_KIND_CRON_STALE,
    ALERT_RULE_KINDS,
    ALERT_SCOPE_GLOBAL,
    AlertRule,
)

__all__ = [
    "ALERT_SCOPES",
    "AlertConfigError",
    "CompiledAlertRule",
    "compile_rule",
]

logger = logging.getLogger(__name__)

#: 合法 scope 词表:'global' + 品类 id(七品类 + channel,与
#: ``push.route.CATEGORY_DEFAULT_ROUTES`` 键集同源——items.category 的合法值域)。
ALERT_SCOPES: frozenset[str] = frozenset({ALERT_SCOPE_GLOBAL, *CATEGORY_DEFAULT_ROUTES})


class AlertConfigError(ValueError):
    """Invalid alert rule config(name/scope/when 语法/action/config 形状).

    消息结构化(中文 ``字段校验失败: …``,RouteConfigError 同款文案):
    读库侧 WARNING 隔离,协议侧(alerts.save)转 ``alert_rule_invalid`` 整批拒。
    """


@dataclass(slots=True)
class CompiledAlertRule:
    """One validated rule plus its compiled evaluation/action parts.

    ``evaluator`` 是 classify 白名单 AST 求值器(``Rule``);``channel`` /
    ``targets`` / ``template`` 是 push 动作解析后的配置(``template`` 随行
    存储与 alerts.test 展示,v1 发送路径走通道自身模板);``tags`` 是 tag
    动作的标签(push 动作为空列表)。
    """

    rule: AlertRule
    evaluator: Rule = field(init=False, repr=False, compare=False)
    channel: str | None = None
    targets: list[str] | None = None
    template: str | None = None
    tags: list[str] = field(default_factory=list)

    @property
    def name(self) -> str:
        return self.rule.name

    def applies_to_scope(self, category: str | None) -> bool:
        """Whether this rule's scope covers an item of ``category``.

        ``global`` 覆盖所有品类;品类 id 只覆盖同品类条目(scope 钉死)。
        """
        return self.rule.scope == ALERT_SCOPE_GLOBAL or self.rule.scope == category


def _require_str_list(value: Any, label: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (
        not allow_empty and not value
    ) or not all(isinstance(element, str) and element for element in value):
        shape = "非空字符串列表" if not allow_empty else "字符串列表"
        raise AlertConfigError(f"字段校验失败: {label} 必须是{shape},得到 {value!r}")
    return list(value)


def _validate_cron_stale(rule: AlertRule) -> None:
    """cron_stale 规则的构造门(10-05-cron-heartbeat):scope 钉品类、when
    占位 'true'、params 形状 {threshold_hours>0} 或 {auto:true}(可选 job_id)。

    - scope 拒 global:心跳监控的是具体品类的调度健康,global 无所指;
    - when 恒 'true':存储列 NOT NULL 需占位;该 kind 不进条目求值路径
      (engine.run_pass 按 kind 过滤),表达式永不被消费——非 'true' 即拒,
      防读者误以为心跳还看条目条件;
    - 阈值两选一:显式 threshold_hours(>0)或 auto(评估侧以 2× 账本观测
      节奏推导,观测不足 WARNING 跳过——fail-fast 不猜)。
    """
    if rule.scope == ALERT_SCOPE_GLOBAL:
        raise AlertConfigError(
            "字段校验失败: cron_stale 规则的 scope 必须钉死品类(global 无所指,"
            "心跳监控的是具体品类的调度健康)"
        )
    if rule.when.strip() != "true":
        raise AlertConfigError(
            "字段校验失败: cron_stale 规则的 when 恒为占位 'true'(该类型不评估"
            "条目条件;条件规则请用 item 类型)"
        )
    if not isinstance(rule.params, dict):
        raise AlertConfigError(
            f"字段校验失败: cron_stale 规则的 params 必须是键值映射,"
            f"得到 {type(rule.params).__name__}"
        )
    unknown = set(rule.params) - {"threshold_hours", "auto", "job_id"}
    if unknown:
        raise AlertConfigError(
            f"字段校验失败: cron_stale 规则的 params 含未知键 {sorted(unknown)}"
            "(允许 threshold_hours/auto/job_id)"
        )
    has_explicit = "threshold_hours" in rule.params
    has_auto = bool(rule.params.get("auto"))
    if has_explicit == has_auto:
        raise AlertConfigError(
            "字段校验失败: cron_stale 规则的阈值必须二选一——显式 threshold_hours"
            " 或 auto:true(观测节奏推导)"
        )
    if has_explicit:
        threshold = rule.params["threshold_hours"]
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or threshold <= 0:
            raise AlertConfigError(
                f"字段校验失败: threshold_hours 必须是正数,得到 {threshold!r}"
            )
    if "job_id" in rule.params:
        job_id = rule.params["job_id"]
        if not isinstance(job_id, str) or not job_id:
            raise AlertConfigError(
                f"字段校验失败: job_id 必须是非空字符串,得到 {job_id!r}"
            )


def compile_rule(rule: AlertRule) -> CompiledAlertRule:
    """构造门:validate + compile one AlertRule(fail fast on config).

    Raises:
        AlertConfigError: name 空 / scope 越表 / action 越表 / ``when`` 违反
            白名单文法(wraps :class:`RuleSyntaxError`)/ ``action_config``
            形状不符或含未知键。
    """
    if not rule.name or not rule.name.strip():
        raise AlertConfigError("字段校验失败: alert_rules.name 不能为空")
    if rule.scope not in ALERT_SCOPES:
        raise AlertConfigError(
            f"字段校验失败: alert_rules.scope 必须是 {sorted(ALERT_SCOPES)} 之一,"
            f"得到 {rule.scope!r}"
        )
    if rule.action not in (ALERT_ACTION_PUSH, ALERT_ACTION_TAG):
        raise AlertConfigError(
            f"字段校验失败: alert_rules.action 必须是 "
            f"['{ALERT_ACTION_PUSH}', '{ALERT_ACTION_TAG}'] 之一,得到 {rule.action!r}"
        )
    if rule.kind not in ALERT_RULE_KINDS:
        raise AlertConfigError(
            f"字段校验失败: alert_rules.kind 必须是 {sorted(ALERT_RULE_KINDS)} 之一,"
            f"得到 {rule.kind!r}"
        )
    if rule.kind == ALERT_RULE_KIND_CRON_STALE:
        _validate_cron_stale(rule)
    elif rule.params is not None:
        raise AlertConfigError(
            "字段校验失败: alert_rules.params 仅 cron_stale 规则可配(item 规则恒空,"
            "防误配)"
        )
    compiled = CompiledAlertRule(rule=rule)
    try:
        compiled.evaluator = Rule(
            name=f"alert→{rule.action}", when=rule.when, tag=rule.action
        )
    except RuleSyntaxError as exc:
        raise AlertConfigError(f"字段校验失败: alert_rules.when_expr 无效({exc})") from exc
    config = rule.action_config if isinstance(rule.action_config, dict) else None
    if not isinstance(config, dict):
        raise AlertConfigError(
            f"字段校验失败: alert_rules.action_config 必须是键值映射,"
            f"得到 {type(rule.action_config).__name__}"
        )
    if rule.action == ALERT_ACTION_PUSH:
        unknown = set(config) - {"channel", "targets", "template"}
        if unknown:
            raise AlertConfigError(
                f"字段校验失败: alert_rules.action_config 含未知键 {sorted(unknown)}"
                f"(push 允许 channel/targets/template)"
            )
        channel = config.get("channel")
        if not isinstance(channel, str) or channel not in CHANNELS:
            raise AlertConfigError(
                f"字段校验失败: push 动作的 channel 必须是 "
                f"{sorted(CHANNELS)} 之一,得到 {channel!r}"
            )
        compiled.channel = channel
        if "targets" in config:
            compiled.targets = _require_str_list(config["targets"], "push 动作的 targets")
        template = config.get("template")
        if template is not None and not isinstance(template, str):
            raise AlertConfigError(
                f"字段校验失败: push 动作的 template 必须是字符串,得到 {template!r}"
            )
        compiled.template = template
    else:  # tag
        unknown = set(config) - {"tags"}
        if unknown:
            raise AlertConfigError(
                f"字段校验失败: alert_rules.action_config 含未知键 {sorted(unknown)}"
                f"(tag 允许 tags)"
            )
        compiled.tags = _require_str_list(config.get("tags"), "tag 动作的 tags")
    return compiled


def compile_rules(rules: Sequence[AlertRule]) -> list[CompiledAlertRule]:
    """Compile a batch, WARNING + skipping bad rows(读库隔离,不 break 批).

    Store 载入路径的构造门:一行坏配置只损失该行规则(单行 WARNING 跳过),
    其余规则照常求值——与 classify 自定义规则的 per-item 隔离哲学一致。
    """
    compiled: list[CompiledAlertRule] = []
    for rule in rules:
        try:
            compiled.append(compile_rule(rule))
        except AlertConfigError as exc:
            logger.warning(
                "告警规则拒载(跳过该行,不影响其余规则): rule_id=%s name=%r: %s",
                rule.id, rule.name, exc,
            )
    return compiled
