"""组件戳(component.json)真锁对账(design §4:版本锁惯例;戳与代码漂移
即红——版本、入口、exit 码表、配置缺省四处单一出处互相钉住)。"""

from __future__ import annotations

import json
from pathlib import Path

import wechat_bridge
import wechat_bridge.codes as codes_mod
from wechat_bridge.config import (
    COPY_CAPACITY_MB_DEFAULT,
    COPY_TTL_HOURS_DEFAULT,
    DEFAULT_DOMAINS,
    HISTORY_DAYS_DEFAULT,
    HTTP_API_ENABLED_DEFAULT,
    HTTP_API_HOST_DEFAULT,
    HTTP_API_PORT_DEFAULT,
    HTTP_API_TOKEN_DEFAULT,
    KEY_PROVIDER_PATH_DEFAULT,
    MEDIA_CACHE_CAPACITY_MB_DEFAULT,
    MEDIA_DECRYPT_PATH_DEFAULT,
    MEM_SEARCH_ENABLED_DEFAULT,
    MESSAGES_DEFAULT,
    SESSIONS_DEFAULT,
)

COMPONENT_ROOT = Path(wechat_bridge.__file__).resolve().parents[1]
STAMP = COMPONENT_ROOT / "component.json"


def _stamp() -> dict:
    return json.loads(STAMP.read_text(encoding="utf-8"))


class TestStampLock:
    def test_version_matches_package(self) -> None:
        """戳版本 = 包版本(真锁;升级必同票)。"""
        assert _stamp()["version"] == wechat_bridge.__version__

    def test_id_is_component_name(self) -> None:
        """G7 命名:组件 id wechat-bridge,push 通道 weixin-local。"""
        stamp = _stamp()
        assert stamp["id"] == "wechat-bridge"
        assert stamp["push_channel"] == "weixin-local"
        assert stamp["kind"] == "bridge"

    def test_entry_file_exists(self) -> None:
        entry = COMPONENT_ROOT / _stamp()["entry"]
        assert entry.is_file(), f"组件戳 entry 指向不存在的文件: {entry}"

    def test_exit_code_table_matches_codes_module(self) -> None:
        """§6 十二项错误码:戳表与 codes 模块互钉(design §6 封闭表)。"""
        stamp_codes = {int(k): v for k, v in _stamp()["cli_contract"]["exit_codes"].items()}
        expected = {0: "成功", 1: codes_mod.EXIT_GENERIC_FAILURE, 2: "usage"}
        # 0/1/2 的戳值是人读语义;具名族与 CODE_NAMES 逐值对账。
        named = {k: v for k, v in stamp_codes.items() if k not in (0, 1)}
        assert named == codes_mod.CODE_NAMES
        assert set(expected) <= set(stamp_codes)
        assert set(stamp_codes) == {0, 1, 2, *codes_mod.CODE_NAMES}

    def test_config_defaults_match_module_constants(self) -> None:
        """§7 配置缺省:戳与 config 模块常量互钉(单一出处=config.py)。"""
        defaults = _stamp()["config_defaults"]
        assert defaults["domains"] == DEFAULT_DOMAINS
        assert defaults["limits"] == {
            "sessions": SESSIONS_DEFAULT,
            "messages": MESSAGES_DEFAULT,
            "history_days": HISTORY_DAYS_DEFAULT,
        }
        assert defaults["copy_ttl_hours"] == COPY_TTL_HOURS_DEFAULT
        assert defaults["copy_capacity_mb"] == COPY_CAPACITY_MB_DEFAULT
        # D4 豁免开关缺省关(真锁:戳与 config.py 单一出处互钉)。
        assert defaults["mem_search_enabled"] is MEM_SEARCH_ENABLED_DEFAULT
        assert MEM_SEARCH_ENABLED_DEFAULT is False
        # 外部取钥器路径缺省空 = 未配置 = 现状行为(B2 真锁;协议
        # docs/wechat-keyprovider.md)。
        assert defaults["key_provider_path"] == KEY_PROVIDER_PATH_DEFAULT
        assert KEY_PROVIDER_PATH_DEFAULT == ""
        # 媒体解密件两键(0.8.0,10-14-wechat-media-sns:空路径=未配置=
        # 媒体面 exit 23 结构化降级;缓存容量 2048MB)。
        assert defaults["media_decrypt_path"] == MEDIA_DECRYPT_PATH_DEFAULT
        assert MEDIA_DECRYPT_PATH_DEFAULT == ""
        assert defaults["media_cache_capacity_mb"] == MEDIA_CACHE_CAPACITY_MB_DEFAULT
        # HTTP API 四键(0.8.0,10-14-wechat-http-api R10:缺省关/回环/5032/
        # 空 token=非 health 全拒)。
        assert defaults["http_api_enabled"] is HTTP_API_ENABLED_DEFAULT
        assert HTTP_API_ENABLED_DEFAULT is False
        assert defaults["http_api_host"] == HTTP_API_HOST_DEFAULT
        assert defaults["http_api_port"] == HTTP_API_PORT_DEFAULT
        assert defaults["http_api_token"] == HTTP_API_TOKEN_DEFAULT
        assert HTTP_API_TOKEN_DEFAULT == ""
        # defaults 只装真配置键;"无配置键"类声明(频控/路径)在 config 节。
        assert set(defaults) == {
            "domains",
            "limits",
            "copy_ttl_hours",
            "copy_capacity_mb",
            "mem_search_enabled",
            "key_provider_path",
            "media_decrypt_path",
            "media_cache_capacity_mb",
            "http_api_enabled",
            "http_api_host",
            "http_api_port",
            "http_api_token",
        }
        assert "G6" in _stamp()["config"]["rate_limit"]

    def test_redlines_documented(self) -> None:
        """三条红线(静默/不破解/私有数据)在戳中显式在场(UI 不隐藏 ToS 性质
        的同款纪律:组件自我披露)。"""
        redlines = "\n".join(_stamp()["redlines"])
        assert "静默" in redlines
        assert "不破解" in redlines or "内存密钥搜索" in redlines
        assert "私有数据" in redlines
