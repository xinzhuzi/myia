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
    ALERT_RULE_KIND_CRON_STALE,
    ALERT_RULE_KIND_ITEM,
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
                if compiled_rule.rule.kind != ALERT_RULE_KIND_ITEM:
                    continue  # cron_stale 不进条目求值路径(heartbeat_pass 专属)
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
        return await self._execute_push_with(compiled_rule, item)

    async def _execute_push_with(
        self, compiled_rule: CompiledAlertRule, item: Any, resolver: ChannelResolver | None = None
    ) -> str:
        channel_name = compiled_rule.channel or ""
        resolve = resolver or self._channel_resolver
        channel = resolve(channel_name) if resolve else None
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


# ---------------------------------------------------------------------------
# cron 心跳(10-05-cron-heartbeat):时间驱动规则,executions 账本只读评估
# ---------------------------------------------------------------------------

#: auto 阈值 = 2× 账本观测节奏,夹 [1, 168] 小时(下限防空敏感抖动,上限
#: 防周更品类永不告警的另一个极端)。
HEARTBEAT_AUTO_MULTIPLIER = 2.0
HEARTBEAT_AUTO_MIN_HOURS = 1.0
HEARTBEAT_AUTO_MAX_HOURS = 168.0


class _HeartbeatNotice:
    """心跳告警的合成通知对象(Item 鸭子形态;引擎不 import Pipeline,
    依赖方向红线见模块头注)。url 用 myssia-alert: 伪协议如实标注来源,
    不伪装成可点链接。"""

    def __init__(self, *, category: str, title: str, content: str, dedup_key: str) -> None:
        self.url = f"myssia-alert://heartbeat/{category}"
        self.title = title
        self.source = "cron-heartbeat"
        self.category = category
        self.scores = None
        self.dedup_key = dedup_key
        self.content = content
        self.metadata: dict = {}

    def view(self) -> dict:
        return dict(self.metadata, url=self.url, title=self.title, source=self.source,
                    category=self.category, scores=self.scores, dedup_key=self.dedup_key)

    def add_tags(self, tags) -> None:  # tag 动作鸭子面(items 行不在库,回写由调用方注记)
        for tag in tags:
            if tag not in self.metadata.setdefault("tags", []):
                self.metadata["tags"].append(tag)


async def heartbeat_pass(
    store: Store,
    rules,
    *,
    last_success_at,
    now,
    cadence_hours=None,
    channel_resolver_for=None,
    send: SendFunc = send_immediate,
    registry: DedupRegistry | None = None,
    tz=None,
) -> list:
    """心跳扫描(10-05-cron-heartbeat):逐 cron_stale 规则判「品类久未成功触发」。

    - 阈值:params.threshold_hours 显式,或 auto = 2× cadence_hours(观测集)
      夹 [1,168];auto 且观测不可得 → WARNING 跳过(fail-fast 不猜)。
    - 观测集:params.job_id 缺省 = 品类级聚合(该品类全部 job);带 job_id =
      精确到单任务(PRD 需求 1:被盯单任务的停摆不被同品类健康任务掩蔽)。
    - stale 判定:距 last_success_at(观测集最近一次成功执行)超阈值;
      从未成功 → 以规则 created_at 起算(冷静期 = 1× 阈值,防装完即报)。
    - 冷却:dedup_key 带时间桶(cron-stale:<品类>[:<job_id>]:<桶号>,桶宽
      = 阈值),record_fired 的 UNIQUE 门闩天然 at-most-once 每桶一条,
      零新状态机(UNIQUE=(rule_id, dedup_key),同品类品类级/精确级规则互不挤占)。
    - 恢复:不再 stale 且上一桶 stale 行在库(has_fired 精确查)→ 发一条
      恢复通知(cron-recovered:<同前缀>:<桶号>,同 UNIQUE 冷却)。
    - 动作:push 用 channel_resolver_for(规则品类, 规则通道名)——**按规则
      品类解析,禁止借用评估宿主品类凭据**(跨品类借凭据红线同
      _execute_push);tag 作用于合成通知(内存语义,items 行不在库如实注记)。

    Args:
        last_success_at: (品类 id, job_id|None) → 观测集最近成功执行
            datetime(UTC)| None;job_id None = 品类级聚合。
        cadence_hours: (品类 id, job_id|None) → 观测集账本节奏(小时)|
            None(auto 阈值用)。
        channel_resolver_for: (品类 id, 通道类型名) → 该品类 push[] 内该
            类型第一条的实例 | None(未配置 = 动作降级)。两参缺一不可:
            品类定凭据来源,通道名定投递面——规则明配 stdout 而品类只有
            telegram 时必须降级,不许错型投递。
    """
    compiled_all = compile_rules(rules)
    fired_rows: list = []
    for compiled_rule in compiled_all:
        rule = compiled_rule.rule
        if rule.kind != ALERT_RULE_KIND_CRON_STALE:
            continue
        if rule.id is None:
            logger.warning("心跳规则未落库(无 id,无法占坑去重),跳过: %s", rule.name)
            continue
        category = rule.scope
        params = rule.params or {}
        job_id = params.get("job_id")
        if "threshold_hours" in params:
            threshold_hours = float(params["threshold_hours"])
        else:  # auto
            cadence = cadence_hours(category, job_id) if cadence_hours else None
            if cadence is None or cadence <= 0:
                logger.warning(
                    "心跳规则 auto 阈值观测不足(账本节奏不可得),本轮跳过"
                    "(fail-fast 不猜): rule=%s category=%s job_id=%s",
                    rule.name, category, job_id,
                )
                continue
            threshold_hours = min(
                max(HEARTBEAT_AUTO_MULTIPLIER * cadence, HEARTBEAT_AUTO_MIN_HOURS),
                HEARTBEAT_AUTO_MAX_HOURS,
            )
        last = last_success_at(category, job_id)
        stale, silent_hours = _stale_since(rule, last, now, threshold_hours)
        bucket = int(now.timestamp() // (threshold_hours * 3600))
        # 身份前缀:精确模式带 job_id——同品类一条品类级 + 一条精确级规则
        # 各自独立占坑/冷却,恢复通知也按各自前缀精确查。
        identity = f"{category}:{job_id}" if job_id else category
        if stale:
            key = f"cron-stale:{identity}:{bucket}"
            subject = f"品类 {category} 的任务 {job_id}" if job_id else f"品类 {category}"
            title = f"心跳:{subject} 已 {silent_hours:.0f} 小时无成功采集"
            content = (
                f"规则 {rule.name}:距最近一次成功执行已超过阈值 {threshold_hours:.1f} 小时。"
                "请到定时任务屏查看执行历史(可能调度停摆、任务持续失败或配置损坏)。"
            )
        else:
            if last is None:
                continue  # 从未成功谈不上恢复
            stale_recent = any(
                store.has_fired(rule.id, f"cron-stale:{identity}:{bucket - offset}")
                for offset in (0, 1)
            )
            recovered_recent = any(
                store.has_fired(rule.id, f"cron-recovered:{identity}:{bucket - offset}")
                for offset in (0, 1)
            )
            if not stale_recent or recovered_recent:
                continue  # 近两桶无 stale 告警,或恢复已通知过:无事发生
            key = f"cron-recovered:{identity}:{bucket}"
            subject = f"品类 {category} 的任务 {job_id}" if job_id else f"品类 {category}"
            title = f"心跳恢复:{subject} 采集已恢复"
            content = f"规则 {rule.name}:观测目标已重新出现成功执行,此前的心跳告警解除。"
        notice = _HeartbeatNotice(category=category, title=title, content=content, dedup_key=key)
        fired = store.record_fired(AlertFired(
            rule_id=rule.id,
            rule_name=rule.name,
            item_id=None,
            dedup_key=key,
            title=title,
            category=category,
            action=rule.action,
        ))
        if fired is None:
            continue  # UNIQUE 冲突:本桶已告警过(冷却门闩)
        if rule.action == ALERT_ACTION_TAG:
            notice.add_tags(compiled_rule.tags)
            status = ALERT_STATUS_TAGGED
        else:
            channel = (
                channel_resolver_for(category, compiled_rule.channel)
                if channel_resolver_for is not None and compiled_rule.channel
                else None
            )
            if channel is None:
                logger.warning(
                    "心跳 push 降级(规则品类 %r 的 push[] 未配置 %r 类型通道,"
                    "禁止跨品类借凭据): rule=%s", category, compiled_rule.channel, rule.name,
                )
                status = ALERT_STATUS_DEGRADED_NO_CHANNEL
            else:
                reports = await send(
                    [notice],
                    channels=[channel],
                    registry=registry,
                    tz=tz,
                    now=now,
                    category=category,
                    item_specs=[list(compiled_rule.targets) if compiled_rule.targets else None],
                )
                status = (
                    ALERT_STATUS_SENT
                    if any(report.ok for report in reports)
                    else ALERT_STATUS_SEND_FAILED
                )
        store.mark_alert_fired_status(fired.id, status)
        fired.action_status = status
        fired_rows.append(fired)
    return fired_rows


def _stale_since(rule, last, now, threshold_hours):
    """stale 判定 + 静默时长(小时);从未成功用规则年龄当冷静期。"""
    if last is not None:
        silent = (now - last).total_seconds() / 3600
        return silent > threshold_hours, silent
    if rule.created_at is None:
        return False, 0.0  # 无 created_at 可判(未落库形态):保守不报
    age = (now - rule.created_at).total_seconds() / 3600
    return age > threshold_hours, age
