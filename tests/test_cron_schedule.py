"""Tests for myssia.cron.schedule — schedule 解析 + next-run 计算。

覆盖任务 10-04-hermes-cron 步骤 A1(implement.md):五形态解析与错误文案
照抄(上游 H cron/jobs.py:784)、compute_next_run(interval 重锚/UTC 加法、
cron 严格后继/恰在射点、once 恢复窗)、DST 回拨(America/New_York
2026-11-01 折叠小时——探针 research/probe-apscheduler.py 场景固化,
ground-truth C20)、normalize_dow 实证器九用例 + 端到端射日
(research/probe-dow-normalizer.py 场景固化,ground-truth C17-C18)。

控时纪律(ground-truth B16):无 freezegun,一律显式 aware datetime 注入
``now`` 参数;时区显式 ZoneInfo,不依赖机器本地时区。
"""

from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from myssia.cron.schedule import (
    ONESHOT_GRACE_SECONDS,
    _classify_dispatch_lateness,
    _compute_grace_seconds,
    _ensure_aware,
    _schedule_cadence_seconds,
    _seconds_after,
    _stored_wall_clock_is_future,
    _timezone_offset_mismatch,
    compute_next_run,
    normalize_dow,
    normalize_repeat_value,
    parse_duration,
    parse_schedule,
    resolve_zone,
)

SH = ZoneInfo("Asia/Shanghai")
NY = ZoneInfo("America/New_York")

# 探针 dow-normalizer 九用例(research/probe-dow-normalizer.py 冻结值)。
DOW_PROBE_CASES = [
    ("0", "sun"),  # POSIX 0=周日(APScheduler 数字系会把 0 当周一,C17)
    ("1", "mon"),
    ("7", "sun"),  # POSIX 7=周日(裸进 CronTrigger 直接 ValueError,C17)
    ("*/2", "sun,tue,thu,sat"),
    ("1-5", "mon,tue,wed,thu,fri"),
    ("0,6", "sun,sat"),
    ("5-1", "sun,mon,fri,sat"),  # 环绕区间:周五经周日绕回周一
    ("mon", "mon"),
    ("mon-fri", "mon,tue,wed,thu,fri"),
]


class TestResolveZone:
    def test_none_falls_back_to_local(self) -> None:
        zone = resolve_zone(None)
        assert isinstance(zone, ZoneInfo)
        assert zone.key  # IANA 键非空(tzlocal 本地解析)

    def test_name_and_instance_passthrough(self) -> None:
        assert resolve_zone("Asia/Shanghai") == SH
        assert resolve_zone(SH) is SH

    def test_invalid_name_structured_error(self) -> None:
        with pytest.raises(ValueError, match=r"^timezone 不是有效的 IANA 时区名称: 'bogus/zone'$"):
            resolve_zone("bogus/zone")


class TestNormalizeRepeatValue:
    @pytest.mark.parametrize(
        ("value", "want"),
        [
            (None, None),
            ("forever", None),
            ("infinite", None),
            ("inf", None),
            ("none", None),
            ("", None),
            (" FOREVER ", None),  # strip + lower
            ("once", 1),
            ("one", 1),
            ("1x", 1),
            ("3", 3),
            (5, 5),
            (0, None),  # 0/负数 → 无限(照抄 H:668)
            (-2, None),
        ],
    )
    def test_coercion(self, value: object, want: int | None) -> None:
        assert normalize_repeat_value(value) == want

    def test_invalid_string_error_text(self) -> None:
        with pytest.raises(ValueError) as exc:
            normalize_repeat_value("x2")
        assert str(exc.value) == "Invalid repeat value 'x2': use an integer, 'forever', or 'once'."


class TestParseDuration:
    @pytest.mark.parametrize(
        ("text", "minutes"),
        [
            ("30m", 30),
            ("2h", 120),
            ("1d", 1440),
            ("hour", 60),  # 裸单位缺省 1
            ("2 hours", 120),  # 数字与单位间空格
            ("45min", 45),
            ("Day", 1440),  # 大小写不敏感
        ],
    )
    def test_durations(self, text: str, minutes: int) -> None:
        assert parse_duration(text) == minutes

    def test_invalid_error_text(self) -> None:
        with pytest.raises(ValueError) as exc:
            parse_duration("xyz")
        assert str(exc.value) == (
            "Invalid duration: 'xyz'. Use format like '30m', '2h', '1d', "
            "or a bare unit like 'hour' (defaults to 1)."
        )


class TestParseScheduleFiveForms:
    """五形态解析;schedule dict 形状冻结(design §2.2),逐字段断言。"""

    def test_interval_bare(self) -> None:
        assert parse_schedule("30m") == {"kind": "interval", "minutes": 30, "display": "every 30m"}

    def test_interval_every_prefix(self) -> None:
        assert parse_schedule("every 2h") == {
            "kind": "interval",
            "minutes": 120,
            "display": "every 120m",  # 上游同款:display 由分钟数重渲染
        }

    def test_natural_weekday_9am(self) -> None:
        # 前端产出 POSIX 编号(monday→1),归一化层转周名(C17:数字直进
        # CronTrigger 会错位一天)。
        assert parse_schedule("every monday 9am") == {
            "kind": "cron",
            "expr": "0 9 * * mon",
            "display": "every monday 9am",
        }

    def test_natural_weekdays_without_prefix(self) -> None:
        assert parse_schedule("weekdays at 9am") == {
            "kind": "cron",
            "expr": "0 9 * * mon,tue,wed,thu,fri",
            "display": "weekdays at 9am",
        }

    def test_natural_comma_weekdays_24h(self) -> None:
        assert parse_schedule("every monday, wednesday at 14:00") == {
            "kind": "cron",
            "expr": "0 14 * * mon,wed",
            "display": "every monday, wednesday at 14:00",
        }

    def test_natural_day_noon_and_12h(self) -> None:
        assert parse_schedule("every day at noon") == {
            "kind": "cron",
            "expr": "0 12 * * *",  # dow 通配保留为 *;design §2.1 示例形态
            "display": "every day at noon",
        }
        assert parse_schedule("every day at 9:30pm") == {
            "kind": "cron",
            "expr": "30 21 * * *",
            "display": "every day at 9:30pm",
        }

    def test_raw_cron_passthrough(self) -> None:
        assert parse_schedule("0 9 * * *") == {
            "kind": "cron",
            "expr": "0 9 * * *",
            "display": "0 9 * * *",
        }

    def test_raw_cron_dow_normalized(self) -> None:
        parsed = parse_schedule("*/15 9-17 * * 1-5")
        assert parsed["kind"] == "cron"
        assert parsed["expr"] == "*/15 9-17 * * mon,tue,wed,thu,fri"
        assert parsed["display"] == "*/15 9-17 * * 1-5"  # display 保留用户原文

    def test_raw_cron_named_month_kept(self) -> None:
        # 月名(JAN)由 CronTrigger 原生支持、原样保留;仅 dow 段归一化(C20)。
        assert parse_schedule("0 9 * JAN MON")["expr"] == "0 9 * JAN mon"

    def test_raw_cron_posix_7_is_sunday(self) -> None:
        assert parse_schedule("0 0 * * 7")["expr"] == "0 0 * * sun"
        assert parse_schedule("0 0 * * 0")["expr"] == "0 0 * * sun"

    def test_once_in_duration_injected_now(self) -> None:
        assert parse_schedule("in 30m", now=datetime(2026, 10, 5, 12, 0, tzinfo=SH)) == {
            "kind": "once",
            "run_at": "2026-10-05T12:30:00+08:00",
            "display": "once in 30m",
        }

    def test_once_iso_naive_anchored_to_configured_tz(self) -> None:
        # #51021 修复照抄:朴素时间戳锚**配置**时区,不是服务器本地。
        assert parse_schedule("2030-06-01T09:00:00", tz=NY)["run_at"] == "2030-06-01T09:00:00-04:00"
        assert parse_schedule("2030-06-01T09:00:00", tz=SH)["run_at"] == "2030-06-01T09:00:00+08:00"

    def test_once_iso_aware_kept(self) -> None:
        parsed = parse_schedule("2030-01-01T09:00:00Z", tz=SH)
        assert parsed == {
            "kind": "once",
            "run_at": "2030-01-01T09:00:00+00:00",
            "display": "once at 2030-01-01 09:00",
        }

    def test_once_date_only_midnight(self) -> None:
        parsed = parse_schedule("2030-01-01", tz=SH)
        assert parsed["kind"] == "once"
        assert parsed["run_at"] == "2030-01-01T00:00:00+08:00"


class TestParseScheduleErrors:
    """错误文案照抄(H:850-857 五形态清单;D1 的 5 段限制结构化报错)。"""

    def test_unparseable_five_form_message(self) -> None:
        with pytest.raises(ValueError) as exc:
            parse_schedule("totally bogus")
        assert str(exc.value) == (
            "Invalid schedule 'totally bogus'. Use:\n"
            "  - Interval: '30m', 'every 30m', 'every 2h' (recurring)\n"
            "  - One-shot delay: 'in 30m', 'in 2h' (fires once)\n"
            "  - Weekly/daily: 'every monday 9am', 'weekdays at 9am' (recurring)\n"
            "  - Cron: '0 9 * * *' (cron expression)\n"
            "  - Timestamp: '2026-02-03T14:00:00' (one-shot at time)"
        )

    def test_six_field_cron_structured_rejection(self) -> None:
        # D1 附注:上游 croniter 允许 5-6 段;MYIA 限恰好 5 段。
        with pytest.raises(ValueError) as exc:
            parse_schedule("0 9 * * * *")
        assert str(exc.value) == (
            "Invalid cron expression '0 9 * * * *': "
            "cron 表达式应为恰好 5 段(minute hour day month dow),实得 6 段"
        )

    def test_out_of_range_field(self) -> None:
        with pytest.raises(ValueError) as exc:
            parse_schedule("60 9 * * *")
        assert str(exc.value).startswith("Invalid cron expression '60 9 * * *': Error validating expression")

    def test_dow_out_of_posix_range(self) -> None:
        with pytest.raises(ValueError) as exc:
            parse_schedule("0 9 * * 8")
        assert str(exc.value) == (
            "Invalid cron expression '0 9 * * 8': dow 字段 '8' 周几越界(POSIX 0-7)"
        )

    def test_invalid_timestamp(self) -> None:
        with pytest.raises(ValueError) as exc:
            parse_schedule("2026-02-30T10:00:00")
        assert str(exc.value).startswith("Invalid timestamp '2026-02-30T10:00:00':")

    def test_in_duration_error_text(self) -> None:
        with pytest.raises(ValueError) as exc:
            parse_schedule("in xyz")
        assert str(exc.value) == "Invalid duration 'xyz' after 'in '. Use e.g. 'in 30m', 'in 2h'."

    def test_every_weekday_without_time_falls_to_duration_error(self) -> None:
        # 照抄上游形状:无时间的 "every monday" 落 interval 路径,报时长错。
        with pytest.raises(ValueError) as exc:
            parse_schedule("every monday")
        assert str(exc.value).startswith("Invalid duration: 'monday'.")


class TestNormalizeDow:
    @pytest.mark.parametrize(("field", "want"), DOW_PROBE_CASES)
    def test_probe_cases(self, field: str, want: str) -> None:
        assert normalize_dow(field) == want

    def test_bare_star_passthrough(self) -> None:
        # 通配语义两方一致,保留使存储 expr 可读(design §2.1 示例 0 9 * * *)。
        assert normalize_dow("*") == "*"

    def test_case_insensitive_names(self) -> None:
        assert normalize_dow("MON-FRI") == "mon,tue,wed,thu,fri"
        assert normalize_dow("Sun") == "sun"

    def test_empty_item_rejected(self) -> None:
        with pytest.raises(ValueError, match="含空项"):
            normalize_dow("1,,2")

    def test_zero_step_rejected(self) -> None:
        with pytest.raises(ValueError, match="步进非法"):
            normalize_dow("*/0")

    def test_out_of_range_rejected(self) -> None:
        with pytest.raises(ValueError, match="周几越界"):
            normalize_dow("8")

    def test_unknown_token_rejected(self) -> None:
        with pytest.raises(ValueError, match="无法识别的周几 token"):
            normalize_dow("funday")


class TestComputeNextRunInterval:
    def test_reanchors_on_last_run_not_now(self) -> None:
        # 重锚:30m 周期,上次 10:00,now 10:20 → 10:30(不是 now+30m)。
        schedule = {"kind": "interval", "minutes": 30, "display": "every 30m"}
        got = compute_next_run(
            schedule, "2026-10-05T10:00:00+08:00", tz=SH, now=datetime(2026, 10, 5, 10, 20, tzinfo=SH)
        )
        assert got == "2026-10-05T10:30:00+08:00"

    def test_fresh_anchor_is_now(self) -> None:
        schedule = {"kind": "interval", "minutes": 30, "display": "every 30m"}
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 5, 10, 20, tzinfo=SH))
        assert got == "2026-10-05T10:50:00+08:00"

    def test_utc_addition_across_dst_fallback(self) -> None:
        # UTC 加法(C20 先验):NY 2026-11-01 回拨,01:50 EDT +30m 的真实
        # 半小时落进第二遍 01:20 EST;墙钟算术会错成 02:20。
        schedule = {"kind": "interval", "minutes": 30, "display": "every 30m"}
        got = compute_next_run(
            schedule,
            "2026-11-01T01:50:00-04:00",
            tz=NY,
            now=datetime(2026, 11, 1, 1, 55, tzinfo=NY),  # fold=0:01:55 EDT
        )
        assert got == "2026-11-01T01:20:00-05:00"

    def test_corrupt_record_returns_none(self) -> None:
        assert compute_next_run({"kind": "interval", "minutes": "abc"}, tz=SH) is None
        assert compute_next_run({"kind": "interval"}, tz=SH) is None


class TestComputeNextRunCron:
    def test_posix_digit_dow_end_to_end(self) -> None:
        # C17 决定性回归:POSIX 1=周一;未归一化直进 CronTrigger 会射周二。
        schedule = parse_schedule("0 9 * * 1")
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 4, 0, 0, tzinfo=SH))
        assert got == "2026-10-05T09:00:00+08:00"  # 周一(2026-10-05),不是周二

    def test_step_dow_end_to_end_from_probe(self) -> None:
        # 探针端到端固化:*/2 周一午 → 周二(不归一化会错成周三)。
        schedule = parse_schedule("0 9 * * */2")
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 5, 12, 0, tzinfo=SH))
        assert got == "2026-10-06T09:00:00+08:00"  # 2026-10-06 = 周二

    def test_posix_zero_and_seven_both_sunday(self) -> None:
        for expr in ("0 0 * * 0", "0 0 * * 7"):
            schedule = parse_schedule(expr)
            got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 3, 12, 0, tzinfo=SH))
            assert got == "2026-10-04T00:00:00+08:00", expr  # 2026-10-04 = 周日

    def test_strict_successor_from_anchor(self) -> None:
        # 严格后继:锚=周一 09:00,now=当刻之后 → 下周一,绝不重射同刻。
        schedule = parse_schedule("0 9 * * mon")
        got = compute_next_run(
            schedule, "2026-10-05T09:00:00+08:00", tz=SH, now=datetime(2026, 10, 5, 9, 30, tzinfo=SH)
        )
        assert got == "2026-10-12T09:00:00+08:00"

    def test_anchor_exactly_on_fire_point_returns_next(self) -> None:
        # 恰在射点:last_run_at 与 now 都恰在射点上 → 下一射点(非同刻)。
        schedule = parse_schedule("0 9 * * mon")
        got = compute_next_run(
            schedule, "2026-10-05T09:00:00+08:00", tz=SH, now=datetime(2026, 10, 5, 9, 0, tzinfo=SH)
        )
        assert got == "2026-10-12T09:00:00+08:00"

    def test_no_anchor_boundary_returns_now_itself(self) -> None:
        # 冻结公式的已知边界(docstring 在案):previous 缺席且 now 恰为
        # 整秒射点(µs=0)→ 返回 now 本身(即刻到期);创建路径 now 带微秒,
        # 实务不触发。
        schedule = parse_schedule("0 9 * * mon")
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 5, 9, 0, 0, tzinfo=SH))
        assert got == "2026-10-05T09:00:00+08:00"

    def test_no_anchor_next_occurrence(self) -> None:
        schedule = parse_schedule("0 9 * * mon")
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 4, 0, 0, tzinfo=SH))
        assert got == "2026-10-05T09:00:00+08:00"

    def test_restart_keeps_anchor_across_downtime(self) -> None:
        # 重启不重锚:锚=周一 09:00,停机到周三 18:00 → 仍是下周一。
        schedule = parse_schedule("0 9 * * mon")
        got = compute_next_run(
            schedule, "2026-10-05T09:00:00+08:00", tz=SH, now=datetime(2026, 10, 7, 18, 0, tzinfo=SH)
        )
        assert got == "2026-10-12T09:00:00+08:00"

    def test_matches_configured_timezone_wall_clock(self) -> None:
        schedule = parse_schedule("0 9 * * *")
        got = compute_next_run(
            schedule, tz=NY, now=datetime(2026, 10, 4, 0, 0, tzinfo=SH)  # = NY 10-03 12:00
        )
        # 按配置时区(NY)墙钟取下一射点:周六午 → 周日 09:00 EDT;
        # 绝不是 now 原有的 +08:00 表示(08:00Z)也不是已过的当日 09:00。
        assert got == "2026-10-04T09:00:00-04:00"

    def test_hand_edited_numeric_dow_dict_renormalized(self) -> None:
        # 存储行手编成数字 dow(jobs.json 直编)也按 POSIX 语义现场归一化。
        schedule = {"kind": "cron", "expr": "0 9 * * 1", "display": "hand"}
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 4, 0, 0, tzinfo=SH))
        assert got == "2026-10-05T09:00:00+08:00"

    def test_malformed_expr_returns_none(self) -> None:
        # 算不出 → None(A4 落 state=error,绝不静默停摆,design §2.1)。
        assert compute_next_run({"kind": "cron", "expr": "garbage expr"}, tz=SH) is None
        assert compute_next_run({"kind": "cron"}, tz=SH) is None
        assert compute_next_run({"kind": "cron", "expr": ""}, tz=SH) is None


class TestComputeNextRunOnce:
    def test_future_run_at_returned_as_is(self) -> None:
        schedule = {"kind": "once", "run_at": "2030-01-01T00:00:00+00:00", "display": "once at ..."}
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 5, 12, 0, tzinfo=SH))
        assert got == "2030-01-01T00:00:00+00:00"

    def test_recently_past_within_grace_recovered(self) -> None:
        schedule = {"kind": "once", "run_at": "2026-10-05T12:01:30+08:00", "display": "once at ..."}
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 5, 12, 3, 0, tzinfo=SH))
        assert got == "2026-10-05T12:01:30+08:00"  # 过去 90s ≤ 120s 宽限窗

    def test_past_beyond_grace_never_again(self) -> None:
        schedule = {"kind": "once", "run_at": "2026-10-05T12:00:00+08:00", "display": "once at ..."}
        got = compute_next_run(schedule, tz=SH, now=datetime(2026, 10, 5, 12, 5, 0, tzinfo=SH))
        assert got is None

    def test_already_ran_never_again(self) -> None:
        schedule = {"kind": "once", "run_at": "2026-10-05T12:00:00+08:00", "display": "once at ..."}
        got = compute_next_run(
            schedule, "2026-10-05T12:00:05+08:00", tz=SH, now=datetime(2026, 10, 5, 12, 0, 10, tzinfo=SH)
        )
        assert got is None

    def test_grace_constant(self) -> None:
        assert ONESHOT_GRACE_SECONDS == 120


class TestDstFallBackNewYork:
    """America/New_York 2026-11-01 折叠小时;探针场景固化(ground-truth C20)。

    当日 01:00-02:00 出现两遍:01:xx EDT(-04:00)= 第一遍,01:xx EST
    (-05:00)= 第二遍;``30 1 * * *`` 的射点 01:30 也随之出现两遍。
    """

    def _schedule(self) -> dict[str, object]:
        return {"kind": "cron", "expr": "30 1 * * *", "display": "daily 1:30"}

    def test_from_second_occurrence_no_past_loop(self) -> None:
        # 探针 fold=1 场景:base = 第二遍 01:45(06:45Z)→ 次日 01:30 EST;
        # 无 Hermes #11723 类「下一射点在过去」回环。
        got = compute_next_run(
            self._schedule(),
            "2026-11-01T01:45:00-05:00",
            tz=NY,
            now=datetime(2026, 11, 1, 2, 0, tzinfo=NY),  # 回拨后 02:00 EST
        )
        assert got == "2026-11-02T01:30:00-05:00"

    def test_from_first_occurrence_hits_second_same_day(self) -> None:
        # 探针 fold=0 场景:base = 第一遍 01:45(05:45Z)→ 当日第二遍
        # 01:30 EST(06:30Z):墙钟同刻、绝对时刻在后。
        got = compute_next_run(
            self._schedule(),
            "2026-11-01T01:45:00-04:00",
            tz=NY,
            now=datetime(2026, 11, 1, 1, 45, tzinfo=NY),  # fold=0:01:45 EDT
        )
        assert got == "2026-11-01T01:30:00-05:00"

    def test_result_is_strictly_after_anchor(self) -> None:
        got = compute_next_run(
            self._schedule(),
            "2026-11-01T01:45:00-05:00",
            tz=NY,
            now=datetime(2026, 11, 1, 2, 0, tzinfo=NY),
        )
        assert got is not None
        base = datetime.fromisoformat("2026-11-01T01:45:00-05:00")
        nxt = datetime.fromisoformat(got)
        # 绝对时刻严格在后(比较 UTC,与 fold 表示无关)。
        assert nxt.astimezone(ZoneInfo("UTC")) > base.astimezone(ZoneInfo("UTC"))


class TestUnknownSchedules:
    def test_unknown_kind_and_non_dict_return_none(self) -> None:
        assert compute_next_run({"kind": "weird"}, tz=SH) is None
        assert compute_next_run("not-a-dict", tz=SH) is None  # type: ignore[arg-type]


class TestGraceAndCadence:
    def test_interval_cadence(self) -> None:
        assert _schedule_cadence_seconds({"kind": "interval", "minutes": 30}) == 1800.0

    def test_cron_cadence_measured_by_trigger(self) -> None:
        schedule = parse_schedule("0 9 * * mon")
        got = _schedule_cadence_seconds(schedule, tz=SH, now=datetime(2026, 10, 5, 9, 30, tzinfo=SH))
        assert got == 604800.0  # 7 天

    def test_malformed_and_missing_return_none(self) -> None:
        assert _schedule_cadence_seconds({"kind": "cron", "expr": "garbage expr"}, tz=SH) is None
        assert _schedule_cadence_seconds({}, tz=SH) is None
        assert _schedule_cadence_seconds(None, tz=SH) is None  # type: ignore[arg-type]

    def test_grace_half_period_clamped(self) -> None:
        assert _compute_grace_seconds({"kind": "interval", "minutes": 30}) == 900  # 半周期
        assert _compute_grace_seconds({"kind": "interval", "minutes": 2}) == 120  # 下夹
        assert _compute_grace_seconds({"kind": "interval", "minutes": 2880}) == 7200  # 上夹(2d)
        assert _compute_grace_seconds({"kind": "cron", "expr": "0 9 * * *", "display": ""}) == 7200
        assert _compute_grace_seconds({}) == 120  # cadence 未知 → 下限

    def test_dispatch_lateness_classification(self) -> None:
        assert _classify_dispatch_lateness(100, 900) == "on_time"
        assert _classify_dispatch_lateness(300, 900) == "on_time"  # 容差边界(≤)
        assert _classify_dispatch_lateness(400, 900) == "late"
        assert _classify_dispatch_lateness(1000, 900) == "catch_up"


class TestTimeUtilities:
    def test_ensure_aware_converts_between_zones(self) -> None:
        got = _ensure_aware(datetime(2026, 1, 1, 12, 0, tzinfo=SH), NY)
        assert got == datetime(2025, 12, 31, 23, 0, tzinfo=NY)  # 12:00+08 = 前日 23:00 EST

    def test_ensure_aware_naive_reads_system_local(self) -> None:
        # 朴素值按系统本地墙钟解释(创建时语义,H:860);只断言「换算发生
        # 且落在目标时区」,具体墙钟值随机器时区、不做定值断言。
        got = _ensure_aware(datetime(2026, 1, 1, 12, 0), SH)
        assert got.tzinfo is not None
        assert got.tzinfo.key == "Asia/Shanghai"

    def test_seconds_after_is_absolute_not_wall_clock(self) -> None:
        # fall-back 小时内 +30m:_seconds_after 走 UTC 绝对加法,落进第二遍。
        got = _seconds_after(datetime(2026, 11, 1, 1, 50, tzinfo=NY, fold=0), 1800)
        assert got == datetime(2026, 11, 1, 1, 20, tzinfo=NY, fold=1)

    def test_timezone_offset_mismatch(self) -> None:
        assert _timezone_offset_mismatch(
            datetime(2026, 1, 1, 12, 0, tzinfo=NY), datetime(2026, 6, 1, 12, 0, tzinfo=NY)
        )  # EST vs EDT
        assert not _timezone_offset_mismatch(
            datetime(2026, 1, 1, 12, 0, tzinfo=SH), datetime(2026, 6, 1, 12, 0, tzinfo=SH)
        )
        assert not _timezone_offset_mismatch(  # 朴素值有意不走偏移修复(H:905)
            datetime(2026, 1, 1, 12, 0), datetime(2026, 6, 1, 12, 0, tzinfo=NY)
        )

    def test_stored_wall_clock_is_future(self) -> None:
        # 时区迁移场景:旧偏移的 21:00+10 换算后墙钟 13:00+02——墙钟意图
        # 21:00 未到,不该被当成因错过而到期(H:913)。
        stored = datetime(2026, 1, 1, 21, 0, tzinfo=ZoneInfo("Australia/Sydney"))
        current = datetime(2026, 1, 1, 13, 0, tzinfo=ZoneInfo("Europe/Brussels"))
        assert _stored_wall_clock_is_future(stored, current)
