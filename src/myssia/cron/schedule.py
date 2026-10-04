"""Schedule 解析与 next-run 计算(cron 子系统的纯函数层)。

MYIA 移植重写自 Hermes ``cron/jobs.py`` 的 schedule 段(NousResearch/
Hermes-Agent,MIT;上游路径 ``~/.hermes/hermes-agent/cron/jobs.py``,
642-1238 行)。上游行号对照(``H:`` 前缀):normalize_repeat_value H:642 /
parse_duration H:674 / _WEEKDAY_TO_CRON_DOW H:690 / _parse_clock_time H:706 /
_natural_every_to_cron H:731 / _cron_schedule H:767 / parse_schedule H:784 /
时间工具族 H:860-917 / _recoverable_oneshot_run_at H:920 /
_compute_grace_seconds H:938 / _classify_dispatch_lateness H:953 /
_schedule_cadence_seconds H:1014 / compute_next_run H:1175。

移植要点:

- **自然语言前端照抄**(:func:`parse_schedule` 五形态 + 错误文案逐字):
  ``30m``/``every 2h``(interval)、``every monday 9am``/``weekdays at
  9am``/``0 9 * * *``(cron)、``in 30m``/ISO 时间戳(once);
  ``noon``/``midnight``、12/24 时制、逗号周几。
- **cron 时刻计算 = APScheduler ``CronTrigger`` + dow 归一化层**(偏离
  D1,design §6):不引 croniter(核心依赖红线);POSIX dow 语义
  (0/7=周日)由 :func:`normalize_dow` 展开为周名集合后再进
  ``CronTrigger.from_crontab``——探针实证 APScheduler 数字周几为**周一系**
  (0=周一),``0 9 * * 1`` 不归一化会射到周二(ground-truth C17-C18,
  实证器 ``research/probe-dow-normalizer.py``);cron 表达式**限恰好
  5 段**(上游 croniter 允许 5-6 段,6 段在本层结构化拒绝,D1 附注)。
  cron 分支 = ``CronTrigger.from_crontab(归一化 expr, ZoneInfo(tz))
  .get_next_fire_time(last_run_at or None, now)``:重锚严格后继、DST
  回拨无回环(C20-C21 探针实证)。
- **interval 加 UTC**(偏移变更不漂移)、**once 朴素时间戳锚配置时区**
  (#51021 修复照抄)、once 恢复窗 :func:`_recoverable_oneshot_run_at`
  照抄。

与上游的差异(其余逐行对照):

- 时区不再是 Hermes 的 profile 全局(``hermes_time.get_timezone``),
  而是显式 ``tz`` 参数——解析链 job > 品类 YAML ``schedule.timezone``
  > 本地在上层组装,本模块 ``tz=None`` 缺省本地;
- ``now`` 可注入(测试控时范式:显式 aware datetime,无 freezegun);
- croniter 的 cadence 量测换 ``CronTrigger`` 两次射点差(D1);
- 损坏的 schedule 记录(interval/cron 分支)返回 None 而非抛异常——
  「recurring 算不出 next → state=error 绝不静默停摆」的信号位
  (design §2.1,A4 消费)。
"""

from __future__ import annotations

import re
from contextlib import suppress
from datetime import datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from apscheduler.triggers.cron import CronTrigger

__all__ = [
    "ONESHOT_GRACE_SECONDS",
    "compute_next_run",
    "normalize_dow",
    "normalize_repeat_value",
    "parse_duration",
    "parse_schedule",
    "resolve_zone",
]


# ---------------------------------------------------------------------------
# 时区解析
# ---------------------------------------------------------------------------


def _local_zone() -> ZoneInfo:
    """本机 IANA 时区(tzlocal;APScheduler 3.x 的既有传递依赖,零新增)。"""
    from tzlocal import get_localzone  # 惰性 import:显式传 tz 的调用方不付成本

    zone = get_localzone()
    if isinstance(zone, ZoneInfo):
        return zone
    return ZoneInfo(str(zone))  # 理论路径(旧 tzlocal 返 pytz);锁内 tzlocal 5 恒 ZoneInfo


def resolve_zone(tz: str | ZoneInfo | None = None) -> ZoneInfo:
    """调度计算用的 IANA 时区;``None`` → 本机时区。

    Args:
        tz: IANA 名称或现成 ``ZoneInfo``;``None`` 取本地。

    Raises:
        ValueError: 名称不是有效 IANA 时区(结构化报错,措辞对齐
            :func:`myssia.pipeline.build_cron_trigger` 先例)。
    """
    if tz is None:
        return _local_zone()
    if isinstance(tz, ZoneInfo):
        return tz
    try:
        return ZoneInfo(tz)
    except (ZoneInfoNotFoundError, ValueError, OSError) as exc:
        raise ValueError(f"timezone 不是有效的 IANA 时区名称: {tz!r}") from exc


# ---------------------------------------------------------------------------
# repeat / duration(照抄 H:642-683)
# ---------------------------------------------------------------------------


def normalize_repeat_value(repeat: Any) -> int | None:
    """把 repeat 值(int 或用户面字符串)规整为 ``int | None``。

    ``'forever'`` 族 → None(无限)、``'once'`` 族 → 1、数字(含数字串
    ``'3'``)→ int、0/负数 → None,其余 ValueError。照抄 H:642:工具
    schema 暴露的是整数,但 agent/用户合法地传用户面字符串;未规整的
    字符串过去在创建路径死于 ``'<=' not supported between 'str' and
    'int'``,并被 update 路径原样入库、拖垮后续 mark_job_run。
    """
    if repeat is None:
        return None
    if isinstance(repeat, str):
        repeat_str = repeat.strip().lower()
        if repeat_str in ("forever", "infinite", "inf", "none", ""):
            return None
        if repeat_str in ("once", "one", "1x"):
            return 1
        try:
            repeat = int(repeat_str)
        except ValueError:
            raise ValueError(
                f"Invalid repeat value {repeat!r}: use an integer, "
                f"'forever', or 'once'."
            ) from None
    return None if repeat <= 0 else int(repeat)


_DURATION_MULTIPLIERS = {"m": 1, "h": 60, "d": 1440}


def parse_duration(s: str) -> int:
    """时长串 → 分钟数:"30m" → 30、"2h" → 120、"1d" → 1440、裸单位 "hour" → 60。"""
    s = s.strip().lower()
    match = re.match(r"^(\d*)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)$", s)
    if not match:
        raise ValueError(
            f"Invalid duration: '{s}'. Use format like '30m', '2h', '1d', "
            "or a bare unit like 'hour' (defaults to 1).")
    value = int(match.group(1)) if match.group(1) else 1
    return value * _DURATION_MULTIPLIERS[match.group(2)[0]]


# ---------------------------------------------------------------------------
# 自然语言 → cron 前端(照抄 H:686-764)
# ---------------------------------------------------------------------------

# "every monday 9am" / "every day at 9am" 的周几词表。编号是 POSIX cron 语义
# (0=周日 … 6=周六,上游 croniter 默认);MYIA 侧由 normalize_dow 转为周名
# 后再进 CronTrigger(数字直接进 CronTrigger 会按周一系错位一天,C17)。
_WEEKDAY_TO_CRON_DOW = {
    "sunday": "0", "sun": "0",
    "monday": "1", "mon": "1",
    "tuesday": "2", "tue": "2", "tues": "2",
    "wednesday": "3", "wed": "3", "weds": "3",
    "thursday": "4", "thu": "4", "thur": "4", "thurs": "4",
    "friday": "5", "fri": "5",
    "saturday": "6", "sat": "6",
}

# 关键词日 spec → cron dow 字段。
_DAYSPEC_TO_CRON_DOW = {
    "day": "*", "daily": "*", "everyday": "*",
    "weekday": "1-5", "weekdays": "1-5",
    "weekend": "0,6", "weekends": "0,6",
}


def _parse_clock_time(text: str) -> tuple[int, int] | None:
    """解析 ``9am``/``9:30am``/``14:00``/``7``(裸 24h 小时)/``noon``/
    ``midnight`` 为 24 小时制 ``(hour, minute)``;不认识返回 None。"""
    t = text.strip().lower().replace(" ", "")
    if not t:
        return None
    if t in ("noon", "midday"):
        return (12, 0)
    if t == "midnight":
        return (0, 0)
    match = re.match(r"^(\d{1,2})(?::(\d{2}))?(am|pm)?$", t)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    meridiem = match.group(3)
    if meridiem:
        if not 1 <= hour <= 12:
            return None
        hour = hour % 12 + (12 if meridiem == "pm" else 0)
    if hour > 23 or minute > 59:
        return None
    return (hour, minute)


def _natural_every_to_cron(rest: str) -> str | None:
    """``<日spec> [at] <时间>``("monday 9am"、"weekday at 9am"、"monday,
    wednesday at 9am")→ 5 段 cron expr;不匹配返回 None,让
    :func:`parse_schedule` 落到 interval 路径。"""
    tokens = rest.lower().replace(",", " ").split()
    if not tokens:
        return None
    # 首部日 token:关键词 spec("weekdays")或逗号/"and" 分隔的周几列表。
    dow = _DAYSPEC_TO_CRON_DOW.get(tokens[0])
    idx = 1
    if dow is None:
        days = []
        idx = len(tokens)
        for i, tok in enumerate(tokens):
            if tok == "and":
                continue
            mapped = _WEEKDAY_TO_CRON_DOW.get(tok)
            if mapped is None:
                idx = i
                break
            if mapped not in days:
                days.append(mapped)
        if not days:
            return None
        dow = ",".join(days)
    time_tokens = tokens[idx:]
    if time_tokens and time_tokens[0] == "at":  # 可选分隔词:"every day at 9am"
        time_tokens = time_tokens[1:]
    if not time_tokens:
        return None
    parsed = _parse_clock_time(" ".join(time_tokens))
    if parsed is None:
        return None
    hour, minute = parsed
    return f"{minute} {hour} * * {dow}"


# ---------------------------------------------------------------------------
# dow 归一化(偏离 D1 的核心;实证器 research/probe-dow-normalizer.py 转正)
# ---------------------------------------------------------------------------

_DOW_NAMES: tuple[str, ...] = ("sun", "mon", "tue", "wed", "thu", "fri", "sat")
_DOW_NAME_TO_POSIX: dict[str, int] = {name: num for num, name in enumerate(_DOW_NAMES)}


def _dow_token(token: str, field: str) -> int:
    """周名(``sun``..``sat``)或 0-7 数字 → POSIX dow 编号(0=周日)。"""
    tok = token.strip().lower()
    if tok in _DOW_NAME_TO_POSIX:
        return _DOW_NAME_TO_POSIX[tok]
    try:
        return int(tok)
    except ValueError as exc:
        raise ValueError(f"dow 字段 {field!r} 含无法识别的周几 token {token!r}") from exc


def normalize_dow(field: str) -> str:
    """POSIX dow 字段 → 排序后的周名集合(逗号连接;或裸 ``*`` 原样)。

    POSIX 语义:0/7=周日、1=周一 … 6=周六;支持列表(``0,6``)、区间
    (``1-5``)、步进(``*/2``、``1-5/2``)、**环绕区间**(``5-1`` = 周五
    经周日绕回周一)、周名(``mon``、``mon-fri``),大小写不敏感。裸
    ``*`` 原样保留:通配在 APScheduler 与 POSIX 下语义相同,且使存储
    expr 保持可读(design §2.1 示例 ``0 9 * * *`` 即此形态);其余一切
    形态展开为周名集合。

    归一化的动因(偏离 D1):APScheduler ``CronTrigger`` 的数字周几按
    **周一系**(0=周一)解析,``0 9 * * 1`` 会射到周二;周名两方语义
    无歧义。九用例 + 端到端射日实证:ground-truth C17-C18。

    Args:
        field: cron 第 5 段 dow 字段原文。

    Returns:
        归一化 dow 字段(周名按 sun..sat 排序逗号连接;或 ``*``)。

    Raises:
        ValueError: 空项、非法步进(≤0)、周几越界(POSIX 0-7)、无法
            识别的 token。
    """
    if field.strip() == "*":
        return "*"
    days: set[int] = set()
    for item in field.split(","):
        item = item.strip().lower()
        if not item:
            raise ValueError(f"dow 字段 {field!r} 含空项")
        base, _, step_text = item.partition("/")
        step = int(step_text) if step_text else 1
        if step <= 0:
            raise ValueError(f"dow 字段 {field!r} 步进非法: {step}")
        if base == "*":
            lo, hi = 0, 6
        elif "-" in base:
            lo_text, _, hi_text = base.partition("-")
            lo = _dow_token(lo_text, field)
            hi = _dow_token(hi_text, field)
        else:
            lo = _dow_token(base, field)
            hi = 6 if step_text else lo
        if not (0 <= lo <= 7 and 0 <= hi <= 7):
            raise ValueError(f"dow 字段 {field!r} 周几越界(POSIX 0-7)")
        if lo <= hi:
            seq: list[int] = list(range(lo, hi + 1, step))
        else:  # 环绕区间(如 5-1 = 周五经 7(周日)绕回周一)
            seq = list(range(lo, 8, step)) + list(range(0, hi + 1, step))
        days.update(d % 7 for d in seq)
    return ",".join(_DOW_NAMES[d] for d in sorted(days))


_CRON_FIELD_CHARSET = re.compile(r"^[A-Za-z\d\*\-,/]+$")


def _normalize_cron_expr(expr: str) -> str:
    """5 段 cron 的 dow 段过 :func:`normalize_dow`,其余四段原样保留。

    其余段的字母(月名 JAN-DEC 等)由 CronTrigger 原生支持(C20 探针),
    无需归一化。幂等:已归一化(周名)expr 再过一遍结果不变——compute
    路径对存储 expr 现场再归一化,兼容手编的数字 dow 行。
    """
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError(
            f"cron 表达式应为恰好 5 段(minute hour day month dow),实得 {len(parts)} 段"
        )
    return " ".join((*parts[:4], normalize_dow(parts[4])))


def _cron_trigger(expr: Any, zone: ZoneInfo) -> CronTrigger | None:
    """归一化后构造 ``CronTrigger.from_crontab(expr, zone)``。

    malformed expr 返回 None 而非抛异常:compute/cadence 把 None 当
    「算不出」信号上交,上层落 ``state=error`` 绝不静默停摆(design
    §2.1);表达式合法性的一手校验在 :func:`parse_schedule`(结构化
    报错),这里是防手编 jobs.json 的第二道闸。
    """
    try:
        return CronTrigger.from_crontab(_normalize_cron_expr(str(expr)), timezone=zone)
    except (TypeError, ValueError):
        return None


def _cron_schedule(expr: str, display: str, invalid_label: str) -> dict[str, Any]:
    """校验 cron expr(dow 归一化 + CronTrigger 实构)并产出存储 schedule dict。

    上游用 croniter 校验(H:767);MYIA 以归一化 + ``CronTrigger.from_crontab``
    实构等价校验(偏离 D1),报错文案形态照抄 ``Invalid {label} '{display}': {e}``。
    """
    try:
        normalized = _normalize_cron_expr(expr)
        CronTrigger.from_crontab(normalized, timezone=ZoneInfo("UTC"))  # 仅校验;时刻计算按 job 时区
    except ValueError as exc:
        raise ValueError(f"Invalid {invalid_label} '{display}': {exc}") from exc
    return {"kind": "cron", "expr": normalized, "display": display}


def _interval_schedule(minutes: int) -> dict[str, Any]:
    return {"kind": "interval", "minutes": minutes, "display": f"every {minutes}m"}


# ---------------------------------------------------------------------------
# parse_schedule(照抄 H:784-857;cron 分支 D1 改造、tz/now 参数化)
# ---------------------------------------------------------------------------


def parse_schedule(
    schedule: str,
    *,
    tz: str | ZoneInfo | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """schedule 串 → ``{"kind": "once"|"interval"|"cron", ...}``。

    五形态(H:784 文案照抄):``"30m"``/``"every 30m"`` 为周期 interval;
    ``"every monday 9am"``/``"weekdays at 9am"``/``"0 9 * * *"`` 为 cron;
    ``"in 30m"``/ISO 时间戳为 once。schedule dict 形状冻结(design §2.2):
    interval 带 ``minutes``、cron 带 ``expr``(dow 归一化后)、once 带
    ``run_at``(aware ISO),``display`` 一律保留用户原文。

    Args:
        schedule: schedule 串原文。
        tz: 配置时区(IANA 名或 ``ZoneInfo``;``None`` 本地)。once 朴素
            时间戳锚该时区(#51021 修复照抄:锚**配置**时区而非服务器
            本地,存储值不依赖检查时刻的系统时区)。
        now: 可注入的当前时刻(aware);仅 ``in <duration>`` 形态消费。

    Raises:
        ValueError: 无法解析时,报五形态用法清单(文案照抄 H:850-857)。
    """
    zone = resolve_zone(tz)
    schedule = schedule.strip()
    original = schedule
    schedule_lower = schedule.lower()

    # 自然语言日/时短语 → cron("every monday 9am",或无前缀 "weekdays at
    # 9am");其余一切 "every X" → 周期 interval。
    is_every = schedule_lower.startswith("every ")
    rest = schedule[6:].strip() if is_every else schedule_lower
    cron_expr = _natural_every_to_cron(rest)
    # 同一 helper 复用——两种短语形状去掉 "every " 前缀后一致(上游 #51975)。
    if cron_expr is not None:
        return _cron_schedule(cron_expr, original, "schedule")
    if is_every:
        return _interval_schedule(parse_duration(rest))

    # cron 表达式。限恰好 5 段(D1 附注:上游 croniter 允许 5-6 段,
    # CronTrigger 只收 5 段,6 段在本层结构化拒绝);段内允许字母,月名/
    # 周名(JAN-DEC、MON-FRI)由 CronTrigger 原生支持(C20 探针)。
    parts = schedule.split()
    if len(parts) >= 5 and all(_CRON_FIELD_CHARSET.match(p) for p in parts[:5]):
        return _cron_schedule(schedule, schedule, "cron expression")

    # ISO 时间戳(含 T 或形如日期)。
    if "T" in schedule or re.match(r"^\d{4}-\d{2}-\d{2}", schedule):
        try:
            dt = datetime.fromisoformat(schedule.replace("Z", "+00:00"))
        except ValueError as e:
            raise ValueError(f"Invalid timestamp '{schedule}': {e}") from e
        if dt.tzinfo is None:
            # 朴素时间戳锚配置时区(#51021 修复照抄):due 检查对拍的
            # 是同一面配置时钟,"20:07" 必须指调度器检查时钟上的 20:07,
            # 否则 one-shot 永不到期或错小时射出。
            dt = dt.replace(tzinfo=zone)
        return {
            "kind": "once",
            "run_at": dt.isoformat(),
            "display": f"once at {dt.strftime('%Y-%m-%d %H:%M')}",
        }

    # "in 30m"/"in 2h" 是显式的一次性延迟形态;裸时长("30m")按文档
    # 契约是**周期** interval。
    if schedule_lower.startswith("in "):
        duration_str = schedule[3:].strip()
        try:
            minutes = parse_duration(duration_str)
        except ValueError:
            raise ValueError(
                f"Invalid duration '{duration_str}' after 'in '. Use e.g. 'in 30m', 'in 2h'."
            ) from None
        base = _ensure_aware(now, zone) if now is not None else datetime.now(tz=zone)
        # 时长度量的是流逝时间,不是跨 DST 边界的墙钟小时(上游同款)。
        run_at = (base.astimezone(timezone.utc) + timedelta(minutes=minutes)).astimezone(base.tzinfo)
        return {"kind": "once", "run_at": run_at.isoformat(), "display": f"once in {duration_str}"}
    with suppress(ValueError):
        return _interval_schedule(parse_duration(schedule))

    raise ValueError(
        f"Invalid schedule '{original}'. Use:\n"
        f"  - Interval: '30m', 'every 30m', 'every 2h' (recurring)\n"
        f"  - One-shot delay: 'in 30m', 'in 2h' (fires once)\n"
        f"  - Weekly/daily: 'every monday 9am', 'weekdays at 9am' (recurring)\n"
        f"  - Cron: '0 9 * * *' (cron expression)\n"
        f"  - Timestamp: '2026-02-03T14:00:00' (one-shot at time)"
    )


# ---------------------------------------------------------------------------
# 时间工具族(照抄 H:860-917;目标时区由参数显式传入)
# ---------------------------------------------------------------------------


def _ensure_aware(dt: datetime, zone: ZoneInfo) -> datetime:
    """换算到配置时区的 aware 时刻。

    遗留朴素值按**系统本地**墙钟(创建它时的语义)解释再换算——保持
    跨时区变更的排序不变,避免假性 not-due(上游 H:860 同款语义)。
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.now().astimezone().tzinfo).astimezone(zone)
    return dt.astimezone(zone)


def _elapsed_seconds(later: datetime, earlier: datetime) -> float:
    """两 aware 时刻间的真实流逝秒数(与墙钟无关)。"""
    return (later.astimezone(timezone.utc) - earlier.astimezone(timezone.utc)).total_seconds()


def _instant_after(left: datetime, right: datetime) -> bool:
    """*left* 是否是晚于 *right* 的绝对时刻。"""
    return left.astimezone(timezone.utc) > right.astimezone(timezone.utc)


def _instant_at_or_before(left: datetime, right: datetime) -> bool:
    """*left* 是否不晚于(≤)*right* 的绝对时刻。"""
    return left.astimezone(timezone.utc) <= right.astimezone(timezone.utc)


def _instant_before(left: datetime, right: datetime) -> bool:
    """*left* 是否是早于 *right* 的绝对时刻。"""
    return left.astimezone(timezone.utc) < right.astimezone(timezone.utc)


def _seconds_after(dt: datetime, seconds: float) -> datetime:
    """*dt* 加真实 *seconds*,落在 *dt* 的时区。

    aware ``+ timedelta`` 是墙钟算术(丢 fold),fall-back 小时内会偏
    一小时;先换 UTC 做绝对加法再换回。
    """
    return (dt.astimezone(timezone.utc) + timedelta(seconds=seconds)).astimezone(dt.tzinfo)


def _parse_aware(value: Any, zone: ZoneInfo) -> datetime | None:
    """ISO 串 → 配置时区 aware 时刻;不可解析返回 None。

    值来自磁盘(job 记录),广撒网捕获是有意的:任何不可解析都要落
    None 由上层规整,绝不让 tick 崩在脏数据上(上游 H:896 同款)。
    """
    try:
        return _ensure_aware(datetime.fromisoformat(value), zone)
    except Exception:
        return None


def _timezone_offset_mismatch(stored: datetime, current: datetime) -> bool:
    """存储的 aware 时间戳是否用了不同的 UTC 偏移。

    朴素值返回 False:它们经 :func:`_ensure_aware` 规整,有意不走偏移
    修复路径(上游 H:905 同款)。
    """
    if stored.tzinfo is None or current.tzinfo is None:
        return False
    return stored.utcoffset() != current.utcoffset()


def _stored_wall_clock_is_future(stored: datetime, current: datetime) -> bool:
    """存储的本地墙钟时刻是否还没到。

    cron 表达的是墙钟意图;时区变更后旧偏移会让未来 run 看似到期
    (21:00+10 → 13:00+02)。比较朴素墙钟把它与真正的错过区分开
    (上游 H:913 同款)。
    """
    return stored.replace(tzinfo=None) > current.replace(tzinfo=None)


# ---------------------------------------------------------------------------
# once 恢复窗 + 宽限/迟到分级(照抄 H:920-960)
# ---------------------------------------------------------------------------

#: once 调度过期后仍可恢复触发的宽限窗秒数(上游定义于 H cron/jobs.py:111,
#: 随恢复窗语义一起归入本模块)。
ONESHOT_GRACE_SECONDS = 120


def _recoverable_oneshot_run_at(
    schedule: dict[str, Any],
    now: datetime,
    *,
    last_run_at: str | None = None,
    zone: ZoneInfo | None = None,
) -> str | None:
    """one-shot 仍可触发的 ``run_at``:小宽限窗覆盖「创建晚于其分钟」的
    job;已跑过(last_run_at 在场)的 one-shot 永不再触发。"""
    resolved = resolve_zone(zone)
    if not isinstance(schedule, dict) or schedule.get("kind") != "once" or last_run_at:
        return None
    run_at = schedule.get("run_at")
    run_at_dt = _parse_aware(run_at, resolved) if run_at else None
    if run_at_dt is not None and _elapsed_seconds(now, run_at_dt) <= ONESHOT_GRACE_SECONDS:
        return str(run_at)
    return None


_MIN_GRACE_SECONDS = 120
_MAX_GRACE_SECONDS = 7200

# 周期派发距计划的误差在该秒数内算 "on_time":忙碌的分钟级 ticker 滑几分
# 是正常节律,不是网关宕机(上游 #99879)。
_LATE_DISPATCH_TOLERANCE_SECONDS = 300


def _classify_dispatch_lateness(lateness_seconds: float, grace_seconds: int) -> str:
    """``on_time``(ticker 弹性内)/ ``late``(补射宽限窗内)/ ``catch_up``
    (超窗;累计错过被跳过,现在补发一发)。"""
    if lateness_seconds > grace_seconds:
        return "catch_up"
    if lateness_seconds > _LATE_DISPATCH_TOLERANCE_SECONDS:
        return "late"
    return "on_time"


# ---------------------------------------------------------------------------
# cadence 量测(照抄 H:1014;cron 分支 croniter → CronTrigger,D1)
# ---------------------------------------------------------------------------

# _schedule_cadence_seconds 的 cron 量测 per-expr 缓存:它在锁内每 tick
# 跑,不匀称 expr 的差值随基准时刻浮动,作为陈旧度*阈值*可接受(上游
# 同款注释);硬上限防长命进程里已删/已改 expr 无界增长缓存。
_cron_cadence_cache: dict[str, float | None] = {}
_CADENCE_CACHE_BOUND = 256


def _schedule_cadence_seconds(
    schedule: dict[str, Any], *, tz: str | ZoneInfo | None = None, now: datetime | None = None
) -> float | None:
    """schedule 的近似周期秒数;算不出(malformed expr 等)返回 None。"""
    if not isinstance(schedule, dict):
        return None
    kind = schedule.get("kind")
    if kind == "interval":
        minutes = schedule.get("minutes")
        try:
            return float(minutes) * 60.0 if minutes else None
        except (TypeError, ValueError):
            return None
    if kind != "cron":
        return None
    expr = schedule.get("expr")
    if not expr:
        return None
    if expr in _cron_cadence_cache:
        return _cron_cadence_cache[expr]
    zone = resolve_zone(tz)
    trigger = _cron_trigger(expr, zone)
    if trigger is None:
        result = None
    else:
        base = _ensure_aware(now, zone) if now is not None else datetime.now(tz=zone)
        first = trigger.get_next_fire_time(None, base)
        # 第二射点以 first 为锚(previous=now=first:内部有 start==previous 的
        # +1µs 守卫);若仍传 base 作 now,base<previous 时 start 取 base,
        # 会重复返回 first 本身。
        second = trigger.get_next_fire_time(first, first) if first is not None else None
        result = (
            _elapsed_seconds(second, first)
            if first is not None and second is not None and _instant_after(second, first)
            else None
        )
    if len(_cron_cadence_cache) >= _CADENCE_CACHE_BOUND:
        _cron_cadence_cache.clear()
    _cron_cadence_cache[expr] = result
    return result


def _compute_grace_seconds(schedule: dict[str, Any]) -> int:
    """迟到多少秒内仍补射而非 fast-forward:周期一半,夹在 [120s, 2h]——
    日级 job 能补射,高频 job 快速 fast-forward。"""
    period_seconds = _schedule_cadence_seconds(schedule)
    if not period_seconds:
        return _MIN_GRACE_SECONDS
    return max(_MIN_GRACE_SECONDS, min(int(period_seconds) // 2, _MAX_GRACE_SECONDS))


# ---------------------------------------------------------------------------
# compute_next_run(照抄 H:1175 前端;cron 分支 D1)
# ---------------------------------------------------------------------------


def compute_next_run(
    schedule: dict[str, Any],
    last_run_at: str | None = None,
    *,
    tz: str | ZoneInfo | None = None,
    now: datetime | None = None,
) -> str | None:
    """schedule 的下一运行时刻(aware ISO 串);无更多运行返回 None。

    - **once**:恢复窗判定(:func:`_recoverable_oneshot_run_at`);
    - **interval**:锚 ``last_run_at``(重启不重锚),UTC 加法——profile
      偏移变更时 interval 仍保持其时长(上游 H:1189 注释照抄);
    - **cron**(D1):``CronTrigger.from_crontab(归一化 expr, ZoneInfo(tz))
      .get_next_fire_time(last_run_at or None, now)``——重锚严格后继、
      DST 回拨小时无过去时刻回环、锚恰在射点返回下一射点(C20-C21 探针
      实证)。已知边界:``last_run_at`` 缺席且 ``now`` 恰为整秒射点时,
      该公式返回 ``now`` 本身(创建路径的 now 带微秒,实务不触发)。

    Args:
        schedule: schedule dict(design §2.2 冻结形状)。
        last_run_at: 上次运行时刻 ISO 串(recurring 的重锚基准)。
        tz: 配置时区;cron 按该时区墙钟匹配,缺省本地。
        now: 可注入的当前时刻(aware);缺省真实时钟。
    """
    zone = resolve_zone(tz)
    now_dt = _ensure_aware(now, zone) if now is not None else datetime.now(tz=zone)
    if not isinstance(schedule, dict):
        return None
    kind = schedule.get("kind")
    if kind == "once":
        return _recoverable_oneshot_run_at(schedule, now_dt, last_run_at=last_run_at, zone=zone)
    # recurring 种类锚 last_run_at:重启不重锚 schedule(上游 H:1183)。
    base_time = (_parse_aware(last_run_at, zone) if last_run_at else None) or now_dt
    if kind == "interval":
        minutes = schedule.get("minutes")
        if minutes is None:
            return None
        try:
            minutes_value = float(minutes)
        except (TypeError, ValueError):
            # 损坏记录(jobs.json 手编/遗留):算不出 → 上层 state=error。
            return None
        # UTC 加法:偏移变更时 interval 保持时长(墙钟加法会在 DST 边界漂一小时)。
        next_run = base_time.astimezone(timezone.utc) + timedelta(minutes=minutes_value)
        return next_run.astimezone(base_time.tzinfo).isoformat()
    if kind == "cron":
        expr = schedule.get("expr")
        if not expr:
            return None
        trigger = _cron_trigger(expr, zone)
        if trigger is None:
            return None  # malformed → 算不出,上层 state=error(design §2.1)
        previous = _parse_aware(last_run_at, zone) if last_run_at else None
        next_fire = trigger.get_next_fire_time(previous, now_dt)
        return next_fire.isoformat() if next_fire is not None else None
    return None
