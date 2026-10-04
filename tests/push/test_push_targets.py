"""Tests for myssia.push.targets — 对象解析(蓝本移植自 Hermes send_message_targets).

覆盖任务 10-03-messaging-core 步骤 2:四路径(直达 id/@username 钩子 →
目录精确 id → 精确名 → 唯一前缀)+ 多义/未命中结构化错误(内嵌候选,
MYIA 偏离注记)+ 安全(无 eval);三段话题形态
``platform:<名或id>:<thread_id>`` 末段拆分回退(10-04-feishu-thread-send,
supports_threads 平台 opt-in)。
"""

from __future__ import annotations

import re

import pytest

from myssia.push.directory import ChannelDirectory, ChannelEntry
from myssia.push.targets import (
    RESOLVED_DIRECT,
    RESOLVED_DIRECTORY_ID,
    RESOLVED_DIRECTORY_NAME,
    RESOLVED_DIRECTORY_PREFIX,
    ChannelTarget,
    TargetResolveError,
    parse_spec,
    resolve_all,
    resolve_target,
)


class FakeFeishuPlatform:
    """直达解析钩子测试替身(feishu 子任务提供真实实现 FeishuCardChannel)。"""

    #: 话题寻址 opt-in 旗标(10-04-feishu-thread-send;真实类同款声明)。
    supports_threads = True

    @staticmethod
    def parse_direct_ref(ref: str) -> ChannelTarget | None:
        if re.fullmatch(r"(?:oc|ou|on|chat|open)_[-A-Za-z0-9]+", ref):
            return ChannelTarget(platform="feishu", chat_id=ref)
        return None


PLATFORMS = {"feishu": FakeFeishuPlatform}


def _directory(tmp_path, entries: list[ChannelEntry]) -> ChannelDirectory:
    directory = ChannelDirectory(tmp_path)
    directory.replace_platform("feishu", entries, now=1.0)
    return directory


@pytest.fixture()
def populated(tmp_path):
    # chat_id 不用 oc_ 前缀形态,让「目录精确 id」路径不被直达钩子抢先。
    return _directory(
        tmp_path,
        [
            ChannelEntry(platform="feishu", chat_id="g1", name="AI中转站合伙人群"),
            ChannelEntry(platform="feishu", chat_id="g2", name="服务器折扣群"),
            ChannelEntry(platform="feishu", chat_id="g3", name="Server-English"),
            ChannelEntry(platform="feishu", chat_id="dm1", name="张三", type="dm"),
            ChannelEntry(platform="feishu", chat_id="g4", name="AI资讯群"),
        ],
    )


class TestParseSpec:
    def test_valid_spec(self):
        assert parse_spec("feishu:群名") == ("feishu", "群名")
        assert parse_spec(" telegram:12345 ") == ("telegram", "12345")
        assert parse_spec("telegram:@user_name") == ("telegram", "@user_name")

    @pytest.mark.parametrize(
        "bad", ["", "feishu", "feishu:", "群名", "Feishu:x", "fei-shu:x", ":x"]
    )
    def test_bad_format_rejected(self, bad):
        with pytest.raises(TargetResolveError) as excinfo:
            parse_spec(bad)
        assert excinfo.value.reason == "bad_format"


class TestDirectRefHook:
    def test_explicit_feishu_id_bypasses_directory(self, populated):
        target = resolve_target("feishu:oc_zzznotindir", populated, platforms=PLATFORMS)

        assert target.chat_id == "oc_zzznotindir"
        assert target.resolved_from == RESOLVED_DIRECT

    def test_hook_miss_falls_through_to_directory(self, populated):
        # 钩子只认 oc_/ou_/… 前缀;群名走目录。
        target = resolve_target(
            "feishu:AI中转站合伙人群", populated, platforms=PLATFORMS
        )

        assert target.chat_id == "g1"
        assert target.resolved_from == RESOLVED_DIRECTORY_NAME

    def test_no_registry_still_resolves_directory(self, populated):
        target = resolve_target("feishu:g1", populated, platforms={})

        assert target.resolved_from == RESOLVED_DIRECTORY_ID

    def test_hook_returning_bare_tuple_is_upgraded(self, tmp_path):
        class TupleHookPlatform:
            @staticmethod
            def parse_direct_ref(ref: str):
                return (f"oc_{ref}", "th1") if ref.isdigit() else None

        directory = _directory(tmp_path, [])
        target = resolve_target(
            "feishu:42", directory, platforms={"feishu": TupleHookPlatform}
        )

        assert (target.chat_id, target.thread_id) == ("oc_42", "th1")


class TestDirectoryResolution:
    def test_exact_chat_id_case_sensitive(self, populated):
        target = resolve_target("feishu:g2", populated, platforms=PLATFORMS)

        assert (target.chat_id, target.name, target.resolved_from) == (
            "g2",
            "服务器折扣群",
            RESOLVED_DIRECTORY_ID,
        )

    def test_exact_name_case_insensitive(self, populated):
        target = resolve_target(
            "feishu:ai中转站合伙人群", populated, platforms=PLATFORMS
        )

        assert target.chat_id == "g1"
        assert target.resolved_from == RESOLVED_DIRECTORY_NAME

    def test_exact_name_with_hash_prefix_normalized(self, populated):
        target = resolve_target(
            "feishu:#AI中转站合伙人群", populated, platforms=PLATFORMS
        )

        assert target.chat_id == "g1"  # Hermes # 前缀规范化的等价物

    def test_unique_prefix(self, populated):
        target = resolve_target("feishu:服务器", populated, platforms=PLATFORMS)

        assert target.chat_id == "g2"
        assert target.resolved_from == RESOLVED_DIRECTORY_PREFIX

    def test_prefix_across_case_and_ascii(self, populated):
        target = resolve_target("feishu:server", populated, platforms=PLATFORMS)

        assert target.chat_id == "g3"


class TestResolveErrors:
    def test_ambiguous_prefix_lists_candidates(self, populated):
        # "AI" 前缀同时命中 AI中转站合伙人群 / AI资讯群 → 多义即未命中。
        with pytest.raises(TargetResolveError) as excinfo:
            resolve_target("feishu:AI", populated, platforms=PLATFORMS)

        error = excinfo.value
        assert error.reason == "ambiguous_prefix"
        assert error.platform == "feishu"
        labels = " ".join(error.candidates)
        assert "AI中转站合伙人群 (g1)" in labels and "AI资讯群 (g4)" in labels

    def test_miss_embeds_candidates(self, populated):
        with pytest.raises(TargetResolveError) as excinfo:
            resolve_target("feishu:不存在的群", populated, platforms=PLATFORMS)

        error = excinfo.value
        assert error.reason == "unresolvable"
        assert len(error.candidates) == 5  # 全量候选内嵌(MYIA 偏离注记)
        assert "AI中转站合伙人群 (g1)" in error.candidates
        assert "不存在的群" in str(error)

    def test_empty_platform_bucket_reports_unknown_platform(self, tmp_path):
        directory = _directory(tmp_path, [])

        with pytest.raises(TargetResolveError) as excinfo:
            resolve_target("feishu:任意名", directory, platforms={})

        assert excinfo.value.reason == "unknown_platform"

    def test_target_key_shape(self):
        target = ChannelTarget(platform="Feishu", chat_id=" oc_1 ", name="群")

        assert target.key == "feishu:oc_1"


class TestResolveAll:
    def test_partial_failure_returns_targets_and_errors(self, populated):
        targets, errors = resolve_all(
            ["feishu:AI中转站合伙人群", "feishu:没有这个群", "feishu:oc_directid"],
            populated,
            platforms=PLATFORMS,
        )

        assert [t.chat_id for t in targets] == ["g1", "oc_directid"]
        assert len(errors) == 1
        assert errors[0].reason == "unresolvable"

    def test_empty_specs(self, populated):
        assert resolve_all([], populated, platforms=PLATFORMS) == ([], [])


class TestSafety:
    def test_no_eval_dangerous_looking_names_just_fail(self, populated):
        """安全验收:spec 只做字符串匹配,任何「代码样」名称都不执行、仅未命中。"""
        with pytest.raises(TargetResolveError):
            resolve_target(
                "feishu:__import__('os').system('echo pwned')",
                populated,
                platforms=PLATFORMS,
            )

        assert populated.find("feishu", "g1").name == "AI中转站合伙人群"  # 目录未被触碰


class TestThreadSpecSplit:
    """三段形态 ``platform:<名或id>:<thread_id>``(10-04-feishu-thread-send)。

    回退语义:整体 ref 四路径全部未命中后才拆末段;仅 supports_threads
    平台;显式段覆盖目录条目存量 thread_id;话题段字符集保守
    (THREAD_REF_RE)——非 id 形态(中文/空段)不拆,按原语义报错。
    """

    def test_exact_name_base_with_thread(self, populated):
        target = resolve_target(
            "feishu:AI中转站合伙人群:om_t1", populated, platforms=PLATFORMS
        )

        assert (target.chat_id, target.thread_id, target.resolved_from) == (
            "g1",
            "om_t1",
            RESOLVED_DIRECTORY_NAME,
        )

    def test_exact_chat_id_base_with_thread(self, populated):
        target = resolve_target("feishu:g2:om_t2", populated, platforms=PLATFORMS)

        assert (target.chat_id, target.thread_id, target.resolved_from) == (
            "g2",
            "om_t2",
            RESOLVED_DIRECTORY_ID,
        )

    def test_prefix_base_with_thread(self, populated):
        target = resolve_target("feishu:服务器:om_t3", populated, platforms=PLATFORMS)

        assert (target.chat_id, target.thread_id, target.resolved_from) == (
            "g2",
            "om_t3",
            RESOLVED_DIRECTORY_PREFIX,
        )

    def test_direct_id_base_with_thread(self, populated):
        """base 走直达钩子(整段 ref 因冒号不匹配钩子正则,拆段后命中)。"""
        target = resolve_target("feishu:oc_9a79:om_t4", populated, platforms=PLATFORMS)

        assert (target.chat_id, target.thread_id, target.resolved_from) == (
            "oc_9a79",
            "om_t4",
            RESOLVED_DIRECT,
        )

    def test_explicit_thread_overrides_entry_thread(self, tmp_path):
        directory = _directory(
            tmp_path,
            [
                ChannelEntry(
                    platform="feishu", chat_id="g1", name="群A", thread_id="om_old"
                )
            ],
        )

        bare = resolve_target("feishu:群A", directory, platforms=PLATFORMS)
        explicit = resolve_target("feishu:群A:om_new", directory, platforms=PLATFORMS)

        assert bare.thread_id == "om_old"  # 无显式段:目录存量透传(既有行为)
        assert explicit.thread_id == "om_new"  # 显式段覆盖存量

    def test_whole_ref_with_colon_name_wins_over_split(self, tmp_path):
        """含冒号的目录名称照旧整体精确名命中,不被三段回退抢跑。"""
        directory = _directory(
            tmp_path,
            [ChannelEntry(platform="feishu", chat_id="gc1", name="带:冒号的群")],
        )

        target = resolve_target("feishu:带:冒号的群", directory, platforms=PLATFORMS)

        assert (target.chat_id, target.thread_id) == ("gc1", None)

    def test_cjk_thread_segment_not_split(self, populated):
        """话题段中文:不匹配保守 id 字符集 → 不拆,整体未命中。"""
        with pytest.raises(TargetResolveError) as excinfo:
            resolve_target(
                "feishu:AI中转站合伙人群:话题甲", populated, platforms=PLATFORMS
            )

        assert excinfo.value.reason == "unresolvable"

    def test_blank_thread_segment_not_split(self, populated):
        """空话题段(``feishu:群名:``)不拆 → 未命中(原语义)。"""
        with pytest.raises(TargetResolveError):
            resolve_target("feishu:AI中转站合伙人群:", populated, platforms=PLATFORMS)

    def test_ambiguous_base_prefix_reports_ambiguity(self, populated):
        """base 前缀多义(AI 前缀双命中):按 ambiguous_prefix 上报,候选取 base 命中。"""
        with pytest.raises(TargetResolveError) as excinfo:
            resolve_target("feishu:AI:om_t5", populated, platforms=PLATFORMS)

        error = excinfo.value
        assert error.reason == "ambiguous_prefix"
        assert error.spec == "feishu:AI:om_t5"
        labels = " ".join(error.candidates)
        assert "AI中转站合伙人群 (g1)" in labels and "AI资讯群 (g4)" in labels

    def test_platform_without_flag_never_splits(self, tmp_path):
        """未声明 supports_threads 的平台:三段 spec 仍按未命中报错(零行为变化)。"""

        class NoThreadFlagPlatform:
            @staticmethod
            def parse_direct_ref(ref: str) -> ChannelTarget | None:
                return None

        directory = ChannelDirectory(tmp_path)
        directory.replace_platform(
            "feishu",
            [ChannelEntry(platform="feishu", chat_id="g1", name="AI中转站合伙人群")],
            now=1.0,
        )

        with pytest.raises(TargetResolveError) as excinfo:
            resolve_target(
                "feishu:AI中转站合伙人群:om_t6",
                directory,
                platforms={"feishu": NoThreadFlagPlatform},
            )

        assert excinfo.value.reason == "unresolvable"
