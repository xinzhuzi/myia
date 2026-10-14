"""微信统计报告 sidecar 协议面(task 10-14-wechat-stats-reports R5/R6)。

两个协议动作的实现本体(``desktop/entry.py`` ``_HANDLERS`` 只做薄壳转接,
集成接线见任务档 integrationSpec):

- ``wechat_local.stats`` {mode, chat_id?, since_days?|all?, year?, refresh?}
  → 桥 ``localdb stats <mode> …`` 直转(参数校验 → 一次性子进程 → 契约
  载荷透传/结构化错误归一)。判例同 :mod:`myssia.wechat.sidecar`
  的 query 通道,复用其 ``_run_bridge``/错误族;超时走 600s 查询上界
  (stats 冷跑可能触发副本首建)。
- ``wechat_local.stats_report`` {mode, stats_payload, tone?} → AI 叙事
  报告(MYIA 侧;桥不重查,``json_payload`` 判例)。端点 = 新
  ``config/wechat-stats.yaml``(enrich 段形态;装载复用
  :class:`~myssia.enrich.settings.EnrichSettings` + ``resolve_endpoint``
  + credentials ref 解析,明文拒载)。``enabled: false`` 或端点缺 = 结构化
  ``ai_disabled``;openai 包缺位 = ``dependency_missing``(带安装指引)。

**隐私缺省(R5,可翻案需主人显式指令)**:喂模型 = 纯聚合数字 +
top_phrases top20 + dual first_chat 截断条;**零逐条消息原文**——入口
做防御性剥离(载荷里出现 ``messages`` 列表即整键丢弃,形态漂移不致漏喂)。

端点凭据只以引用名进日志/错误(EnrichSettings 同门);报告文本与统计
载荷不入日志。
"""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any

from myssia.enrich.client import INSTALL_COMMAND, OpenAICompatClient
from myssia.enrich.errors import EnrichConfigError
from myssia.enrich.settings import EnrichSettings, resolve_endpoint
from myssia.wechat.sidecar import (
    WechatLocalSidecarError,
    _QUERY_TIMEOUT_SECONDS,
    _run_bridge,
)

__all__ = [
    "STATS_CONFIG_NAME",
    "handle_wechat_stats",
    "config_path",
    "load_stats_report_config",
    "StatsReportConfig",
]

#: 配置文件名(<数据根>/config/wechat-stats.yaml;桌面包 Resources/config
#: 种子补缺同 vision.yaml 判例)。
STATS_CONFIG_NAME = "wechat-stats.yaml"

#: 协议参数上界(防一把梭全量;桥内另有窗口纪律)。
_SINCE_DAYS_MAX = 36500
_YEARS = (1970, 9999)
_TONE_MAX_CHARS = 40

_STATS_MODES = ("chats", "chat", "annual", "dual")

#: LLM 报告提示词(章节钉死 prd R5:总览/时段画像/关系洞察/结语)。
_REPORT_SYSTEM_PROMPT = (
    "你是一位尊重隐私的数据叙事作者。输入是一段微信聊天统计的 JSON 聚合"
    "数字(无任何逐条消息原文)。请只用这些数字写一份中文叙事报告,分四章:"
    "「总览」「时段画像」「关系洞察」「结语」。要求:每章 2-5 句;引用数字"
    "要具体(次数/天数/时段/排行);不编造输入中不存在的数字或事件;不输出"
    "与统计无关的内容;用 Markdown 二级标题分章。"
)

_REPORT_USER_TEMPLATE = (
    "报告类型:{mode_label}\n语气要求:{tone}\n统计载荷(JSON):\n{payload}"
)

_MODE_LABELS = {
    "chats": "会话清单",
    "chat": "单会话分析(私聊或群聊)",
    "annual": "年度报告",
    "dual": "双人关系报告",
}


def _require_str(params: dict[str, Any], key: str) -> str:
    value = params.get(key)
    if not isinstance(value, str) or not value.strip():
        raise WechatLocalSidecarError(
            "invalid_params", f"params.{key} 必须是非空字符串", path=f"params.{key}"
        )
    return value.strip()


def _optional_int(
    params: dict[str, Any], key: str, *, maximum: int
) -> int | None:
    value = params.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0 or value > maximum:
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.{key} 须为 1..{maximum} 的整数",
            path=f"params.{key}",
        )
    return value


# =====================================================================
# 动作一:stats(桥中继)
# =====================================================================


def _stats(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.stats`` → 桥 ``localdb stats`` 四子命令直转。"""
    mode = _require_str(params, "mode")
    if mode not in _STATS_MODES:
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.mode 须为 {list(_STATS_MODES)} 之一,当前为 {mode!r}",
            path="params.mode",
        )
    argv = ["localdb", "stats", mode]
    if mode in ("chat", "dual"):
        chat_id = _require_str(params, "chat_id")
        since = _optional_int(params, "since_days", maximum=_SINCE_DAYS_MAX)
        all_time = bool(params.get("all"))
        if (since is not None) == all_time:
            raise WechatLocalSidecarError(
                "invalid_params",
                "chat/dual 须二选一:since_days(天)或 all=true",
                path="params",
            )
        argv += [chat_id]
        argv += ["--all"] if all_time else ["--since", f"{since}d"]
    elif mode == "annual":
        year = _optional_int(params, "year", maximum=_YEARS[1])
        all_time = bool(params.get("all"))
        if (year is not None) == all_time:
            raise WechatLocalSidecarError(
                "invalid_params",
                "annual 须二选一:year(年)或 all=true",
                path="params",
            )
        argv += ["--all"] if all_time else ["--year", str(year)]
    if params.get("refresh"):
        argv += ["--refresh"]
    argv += ["--json"]
    return _run_bridge([_base()] + argv, timeout=_QUERY_TIMEOUT_SECONDS)


def _base() -> str:
    """桥 bin 缺省落点(延迟解析:wechat_local_sidecar._BASE 可被单测注入)。"""
    from myssia.wechat.sidecar import _BASE

    return str(_BASE)


# =====================================================================
# 配置装载(config/wechat-stats.yaml)
# =====================================================================


class StatsReportConfig:
    """``wechat-stats.yaml`` 的内存形态(缺文件 = 全缺省,合法未配置态)。"""

    def __init__(
        self,
        *,
        enabled: bool,
        model: str,
        base_url_ref: str | None,
        api_key_ref: str | None,
        timeout_seconds: float,
    ) -> None:
        self.enabled = enabled
        self.model = model
        self.base_url_ref = base_url_ref
        self.api_key_ref = api_key_ref
        self.timeout_seconds = timeout_seconds


def config_path(data_root: Path | None = None) -> Path | None:
    """配置文件定位:<数据根>/config/wechat-stats.yaml;数据根 = 显式参 >
    ``MYIA_HOME`` env;开发态回落仓库 config/(自本文件向上找,找不到 =
    None → 全缺省)。"""
    root = data_root
    if root is None:
        env = os.environ.get("MYIA_HOME")
        if env:
            root = Path(env).expanduser()
    if root is not None:
        candidate = root / "config" / STATS_CONFIG_NAME
        if candidate.is_file():
            return candidate
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "config" / STATS_CONFIG_NAME
        if candidate.is_file():
            return candidate
    return None


def load_stats_report_config(
    data_root: Path | None = None,
) -> StatsReportConfig:
    """装载配置(文件缺失/坏文件 = 全缺省,不判错——统计数字面不受影响)。"""
    enabled = False
    model = "glm-5.3-flash"
    base_url_ref: str | None = None
    api_key_ref: str | None = None
    timeout = 60.0
    path = config_path(data_root)
    if path is not None:
        try:
            import yaml

            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError, yaml.YAMLError):
            doc = None  # 坏文件 = 全缺省(统计数字面不受影响)
        section = doc.get("stats_report") if isinstance(doc, dict) else None
        if isinstance(section, dict):
            enabled = section.get("enabled") is True
            if isinstance(section.get("model"), str) and section.get("model").strip():
                model = section["model"].strip()
            for key in ("base_url", "api_key"):
                value = section.get(key)
                if isinstance(value, str) and value.strip():
                    if key == "base_url":
                        base_url_ref = value.strip()
                    else:
                        api_key_ref = value.strip()
            raw_timeout = section.get("timeout_seconds")
            if isinstance(raw_timeout, (int, float)) and raw_timeout > 0:
                timeout = float(raw_timeout)
    return StatsReportConfig(
        enabled=enabled,
        model=model,
        base_url_ref=base_url_ref,
        api_key_ref=api_key_ref,
        timeout_seconds=timeout,
    )


# =====================================================================
# 动作二:stats_report(AI 叙事报告)
# =====================================================================


def _sanitize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """防御性递归剥离:任何层级的 ``messages`` 键整键丢弃(隐私缺省 R5;
    正常桥 stats 载荷本就没有该键——出现即形态漂移,剥掉喂不出逐条原文)。"""
    cleaned: dict[str, Any] = {}
    for key, value in payload.items():
        if key == "messages":
            continue
        if isinstance(value, dict):
            cleaned[key] = _sanitize_payload(value)
        elif isinstance(value, list):
            cleaned[key] = [
                _sanitize_payload(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            cleaned[key] = value
    return cleaned


def _stats_report(params: dict[str, Any], data_root: Path | None) -> dict[str, Any]:
    mode = _require_str(params, "mode")
    if mode not in _MODE_LABELS:
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.mode 须为 {list(_MODE_LABELS)} 之一,当前为 {mode!r}",
            path="params.mode",
        )
    payload = params.get("stats_payload")
    if not isinstance(payload, dict):
        raise WechatLocalSidecarError(
            "invalid_params",
            "params.stats_payload 必须是对象(前端已持的桥 stats 应答)",
            path="params.stats_payload",
        )
    tone = params.get("tone")
    if tone is not None and (not isinstance(tone, str) or not tone.strip()
                             or len(tone) > _TONE_MAX_CHARS):
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.tone 须为 ≤{_TONE_MAX_CHARS} 字的非空字符串",
            path="params.tone",
        )
    config = load_stats_report_config(data_root)
    if not config.enabled:
        raise WechatLocalSidecarError(
            "ai_disabled",
            "AI 报告未开启(config/wechat-stats.yaml 的 stats_report.enabled)",
            data={
                "fix_hint": "编辑配置文件把 enabled 改为 true 并配好 "
                "base_url/api_key(env:/keychain: 引用),重启后生效;统计"
                "数字与图表不依赖此开关"
            },
        )
    if not config.base_url_ref or not config.api_key_ref:
        missing = [name for name, v in (("base_url", config.base_url_ref),
                                        ("api_key", config.api_key_ref)) if not v]
        raise WechatLocalSidecarError(
            "ai_disabled",
            f"AI 报告端点未配置(缺 {', '.join(missing)};只收 env:/keychain: 引用)",
            data={
                "fix_hint": "在 config/wechat-stats.yaml 的 stats_report 段补齐 "
                "base_url 与 api_key 引用;keychain 条目可经设置屏录入"
            },
        )
    import json

    user = _REPORT_USER_TEMPLATE.format(
        mode_label=_MODE_LABELS[mode],
        tone=(tone.strip() if tone else "平实自然"),
        payload=json.dumps(_sanitize_payload(payload), ensure_ascii=False),
    )
    try:
        settings = EnrichSettings(
            base_url_ref=config.base_url_ref,
            api_key_ref=config.api_key_ref,
            timeout_seconds=config.timeout_seconds,
        )
        base_url, api_key = resolve_endpoint(settings)
    except EnrichConfigError as exc:
        raise WechatLocalSidecarError(
            "ai_disabled",
            f"AI 报告端点配置不可用: {exc}",
            data={"fix_hint": "核对 config/wechat-stats.yaml 的引用可解析"
            "(env 变量已设/keychain 条目在位),明文值会被拒载"},
        ) from exc
    client = OpenAICompatClient(
        base_url,
        api_key,
        timeout_seconds=config.timeout_seconds,
        max_output_tokens=2048,
    )
    try:
        result = asyncio.run(
            client.complete(
                model=config.model, system=_REPORT_SYSTEM_PROMPT, user=user
            )
        )
    except EnrichConfigError as exc:
        if exc.code == "dependency_missing":
            raise WechatLocalSidecarError(
                "dependency_missing",
                f"AI 报告依赖 openai 未安装: {exc}",
                data={"fix_hint": f"先执行 {INSTALL_COMMAND}"},
            ) from exc
        raise WechatLocalSidecarError(
            "ai_disabled", f"AI 报告端点错误: {exc}", data=None
        ) from exc
    except TimeoutError as exc:
        raise WechatLocalSidecarError(
            "llm_timeout",
            f"AI 报告生成超时(上限 {config.timeout_seconds:.0f}s)",
            data={"fix_hint": "稍后重试;持续超时可调大 timeout_seconds"},
        ) from exc
    finally:
        asyncio.run(client.aclose())
    return {
        "report_markdown": result.text,
        "model": config.model,
        "total_tokens": result.total_tokens,
    }


# =====================================================================
# 分发入口
# =====================================================================


def handle_wechat_stats(
    action: str, params: dict[str, Any] | None, *, data_root: Path | None = None
) -> dict[str, Any]:
    """协议分发入口(entry.py 薄壳各转接一个 action)。

    Args:
        action: ``stats`` / ``stats_report``。
        params: 协议 params(None 视同空对象)。
        data_root: 数据根(配置定位;None = MYIA_HOME env/开发回落)。

    Raises:
        WechatLocalSidecarError: 结构化错误(薄壳换轨 ``ProtocolError``)。
    """
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise WechatLocalSidecarError("invalid_params", "params 必须是对象", path="params")
    if action == "stats":
        return _stats(params)
    if action == "stats_report":
        return _stats_report(params, data_root)
    raise WechatLocalSidecarError(
        "invalid_params",
        f"未知 wechat_stats 动作 {action!r}(合法:stats, stats_report)",
        path="method",
    )
