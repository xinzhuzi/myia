"""Alert engine: mute 预筛 → when 求值 → fired 占坑 → 动作执行.

设计(10-04-alert-rules design §5-§7)要点:

- 求值上下文(grill Q7):``alert_view(item)`` = ``item.view()``(metadata
  平铺 + url/title/source/category/scores/dedup_key 顶层)后补 ``content``
  ——``Item.view()`` 不含正文(``from_extracted`` 摘出 content),正文条件
  (``'融资' in content``)在原生 view 写不了;补丁在告警引擎侧,route 共享的
  ``view()`` 零波及。
- mute 硬规则(grill Q5):引擎自跑 ``mute_hit(item.title, mute_words)``
  (title 子串语义),不读 ``metadata['muted']`` 标记(与品类 enrich 开关
  解耦);命中 mute 的条目跳过全部规则求值,不落 fired。
- 求值隔离:classify 白名单 AST 的既有机器(资源护栏防 ``9**9**9``,
  never eval),求值错 = 单条 WARNING + 未命中,不 break 批。
- fired 占坑(grill Q3):命中先 ``record_fired``(INSERT,UNIQUE
  (rule_id, dedup_key) 冲突返回 None 即跳过动作)——崩溃在动作前或重跑
  再评估都被唯一约束拦住,at-most-once,无需额外状态机。
- 动作(grill Q4):push = 注入的通道解析器取「当前品类 ``push[]`` 内该
  类型第一条」实例走 ``send_immediate`` 同门(与 run 共享 DedupRegistry,
  槽位防重发免费获得——route immediate 先发则告警被拦,反向亦然);品类
  未配该类型 = 降级 WARNING + ``degraded_no_channel``,禁止跨品类借凭据。
  tag = ``item.add_tags``(内存)+ ``store.update_item_tags``(回写)两步。

依赖方向:engine 只依赖 classifier Rule(经 rule.py 编译)、push
send_immediate、store 协议;**不 import Pipeline**——mute 词表 / 通道解析器 /
registry / 时钟全部由 Pipeline 注入(测试同样由此注入假件)。
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable, Sequence
from datetime import datetime, tzinfo
from typing import Any

from myssia.dedup import DedupRegistry
from myssia.enrich.scoring import mute_hit
from myssia.push.base import Channel, SendReport
from myssia.push.digest import send_immediate
from myssia.store.base import Store
from myssia.store.models import (
    ALERT_ACTION_TAG,
    ALERT_STATUS_DEGRADED_NO_CHANNEL,
    ALERT_STATUS_SEND_FAILED,
    ALERT_STATUS_SENT,
    ALERT_STATUS_TAGGED,
    AlertFired,
    AlertRule,
)

from myssia.alerts.rule import CompiledAlertRule, compile_rules

__all__ = ["AlertEngine", "ChannelResolver", "SendFunc", "alert_view"]

logger = logging.getLogger(__name__)

#: 通道解析器:通道类型名 → 当前品类 ``push[]`` 内该类型第一条的实例;
#: 未配置该类型返回 None(动作降级)。由 Pipeline 注入(``_build_channel``
#: 同门),「禁止跨品类借凭据」由注入方只看本品类 push[] 天然满足。
ChannelResolver = Callable[[str], "Channel | None"]

#: 发送函数(send_immediate 同形;测试注入假件,缺省真实现)。
SendFunc = Callable[..., Awaitable[list[SendReport]]]


def alert_view(item: Any) -> dict[str, Any]:
    """求值上下文(grill Q7):``item.view()`` + ``content`` 补丁.

    ``Item.view()`` 把 metadata 平铺并置顶 url/title/source/category/
    scores/dedup_key,但不含正文(``from_extracted`` 将 content 摘出
    metadata)——正文条件在原生 view 写不了,这里补上。补丁只落在本 dict
    (``view()`` 每次返回新 dict),``Item.view()`` 本体零波及,route 求值
    用例原样绿。score 阈值用 ``metadata['score']`` 标量(enrich 回填,route
    同读法;``scores`` 是 dict,白名单禁下标不构成障碍——单维阈值写
    ``score >= 4`` 而非 ``scores['x']``)。
    """
    ctx = item.view()
    ctx["content"] = item.content
    return ctx


class AlertEngine:
    """One ingest pass over the alert rules(求值/mute 预筛/动作执行).

    Args:
        store: run 用的存储(fired 占坑 / 状态回填 / tag 回写;规则由调用方
            先读出再传入 ``run_pass``)。
        mute_words: effective mute 词表(Pipeline 并入反馈 0.0 权重词后传入)。
        channel_resolver: push 动作的通道解析器(见 :data:`ChannelResolver`)。
        send: 发送函数(send_immediate 同形;测试注入)。
        registry: 与 run 共享的 AM/PM 去重注册表(双向压制;None = 不抑制)。
        tz: 槽位时区(品类 schedule 时区)。
        now: 发送时刻(注入时钟;None = send_immediate 内部取 now)。
        category: 卡片标题上下文里的品类名。
    """

    def __init__(
        self,
        *,
        store: Store,
        mute_words: Sequence[str] = (),
        channel_resolver: ChannelResolver | None = None,
        send: SendFunc = send_immediate,
        registry: DedupRegistry | None = None,
        tz: tzinfo | None = None,
        now: datetime | None = None,
        category: str | None = None,
    ) -> None:
        self._store = store
        self._mute_words = list(mute_words)
        self._channel_resolver = channel_resolver
        self._send = send
        self._registry = registry
        self._tz = tz
        self._now = now
        self._category = category

    async def run_pass(
        self, items: Sequence[Any], rules: Sequence[AlertRule]
    ) -> list[AlertFired]:
        """逐条目 × 逐启用规则求值;返回本轮新占坑的 fired 行(含终态).

        mute 命中 → 跳过该条目全部规则(硬规则);求值错 → 单条 WARNING +
        未命中(evaluate 内隔离);命中 → 先占坑(冲突即跳过动作,
        at-most-once),再执行动作并回填 ``action_status`` 终态。动作执行
        自身的失败已按降级语义编码进状态(降级/发送失败),本方法不向调用方
        抛条目级错误。
        """
        compiled = compile_rules(rules)  # 读库构造门:坏行 WARNING 跳过(隔离)
        fired_rows: list[AlertFired] = []
        for item in items:
            hit_word = mute_hit(item.title, self._mute_words)
            if hit_word:
                logger.info(
                    "告警 mute 预筛命中(跳过全部规则求值) word=%s title=%r",
                    hit_word, item.title,
                )
                continue
            view = alert_view(item)
            for compiled_rule in compiled:
                await self._evaluate_one(compiled_rule, item, view, fired_rows)
        return fired_rows

    async def _evaluate_one(
        self,
        compiled_rule: CompiledAlertRule,
        item: Any,
        view: dict[str, Any],
        fired_rows: list[AlertFired],
    ) -> None:
        if not compiled_rule.applies_to_scope(view.get("category")):
            return  # 品类 scope 钉死:非本品类条目不求值
        if not compiled_rule.evaluator.evaluate(view):
            return  # 求值错在 evaluate 内 WARNING + False(隔离,未命中)
        rule = compiled_rule.rule
        key = item.dedup_key or item.url  # digest.py 同款兜底:dedup_key or url
        item_row = self._store.get_item_by_dedup_key(key)
        fired = self._store.record_fired(
            AlertFired(
                rule_id=rule.id or 0,
                rule_name=rule.name,
                item_id=item_row.id if item_row is not None else None,
                dedup_key=key,
                title=item.title,
                category=item.category,
                action=rule.action,
            )
        )
        if fired is None:
            return  # UNIQUE 冲突:占坑失败,跳过动作(at-most-once 门闩)
        status = await self._execute_action(compiled_rule, item, key)
        self._store.mark_alert_fired_status(fired.id, status)
        fired.action_status = status
        fired_rows.append(fired)

    async def _execute_action(
        self, compiled_rule: CompiledAlertRule, item: Any, key: str
    ) -> str:
        """执行单条规则的动作,返回终态状态(§2.1 枚举);不抛条目级错误."""
        if compiled_rule.rule.action == ALERT_ACTION_TAG:
            return self._execute_tag(compiled_rule, item, key)
        return await self._execute_push(compiled_rule, item)

    def _execute_tag(self, compiled_rule: CompiledAlertRule, item: Any, key: str) -> str:
        # 两步(design §7.2):内存合并(add_tags 保序去重)+ items.tags 回写
        # (否则标签只在当批内存对象,库行不带走)。
        item.add_tags(compiled_rule.tags)
        tags = list(item.metadata.get("tags") or [])
        updated = self._store.update_item_tags(dedup_key=key, tags=tags)
        if not updated:
            logger.warning(
                "告警 tag 回写未命中(items 行可能已被 retention 剪枝,标签只在"
                "当批内存对象) key=%s tags=%s", key, compiled_rule.tags,
            )
        return ALERT_STATUS_TAGGED

    async def _execute_push(self, compiled_rule: CompiledAlertRule, item: Any) -> str:
        channel_name = compiled_rule.channel or ""
        channel = self._channel_resolver(channel_name) if self._channel_resolver else None
        if channel is None:
            logger.warning(
                "告警 push 降级(当前品类 push[] 未配置 %r 类型通道,禁止跨品类"
                "借凭据,本次不发) rule=%s", channel_name, compiled_rule.name,
            )
            return ALERT_STATUS_DEGRADED_NO_CHANNEL
        reports = await self._send(
            [item],
            channels=[channel],
            registry=self._registry,
            tz=self._tz,
            now=self._now,
            category=self._category,
            item_specs=[list(compiled_rule.targets) if compiled_rule.targets else None],
        )
        if any(report.ok for report in reports):
            return ALERT_STATUS_SENT
        if not reports:
            # 同槽位防重发拦截(route immediate 先发)或零定向对象:零报告 =
            # 未送达(§7.1 字面:any(ok) → sent,否则 send_failed),如实注记。
            logger.info(
                "告警推送未产生任何发送报告(同槽位防重发拦截或零对象): rule=%s",
                compiled_rule.name,
            )
        return ALERT_STATUS_SEND_FAILED
