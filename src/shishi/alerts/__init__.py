"""情报流告警规则引擎(PRD 10-04-alert-rules,design §5).

公共面:存储记录(:class:`AlertRule` / :class:`AlertFired`)、构造期拒
(:class:`AlertConfigError` + :func:`compile_rule`)、求值器与动作执行
(:class:`AlertEngine`)、求值上下文(:func:`alert_view`)。挂点在
``Pipeline._alert_pass``(design §6),协议/CLI/UI 在桌面批(Stage D/E)。
"""

from shishi.alerts.engine import AlertEngine, ChannelResolver, SendFunc, alert_view
from shishi.alerts.rule import (
    ALERT_SCOPES,
    AlertConfigError,
    CompiledAlertRule,
    compile_rule,
    compile_rules,
)
from shishi.store.models import AlertFired, AlertRule

__all__ = [
    "ALERT_SCOPES",
    "AlertConfigError",
    "AlertEngine",
    "AlertFired",
    "AlertRule",
    "ChannelResolver",
    "CompiledAlertRule",
    "SendFunc",
    "alert_view",
    "compile_rule",
    "compile_rules",
]
