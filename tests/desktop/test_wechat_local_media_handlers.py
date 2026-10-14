"""Tests for wechat_local.* 媒体/朋友圈四动作(task 10-14-wechat-media-sns R5)。

覆盖计划接线批的契约形状:``sns_feed`` / ``sns_export`` / ``media_scan`` /
``media_decrypt`` 的参数校验、argv 形状、桥应答透传、桥具名错误原样上抛。
桥子进程全 mock(照 test_wechat_local_handlers.py 的 fake_bridge 惯例),
零真跑。

**接线门控**:四个动作在 ``wechat_local_sidecar._ACTIONS`` 封闭表注册之前
本文件整体跳 skip(集成员接线批落地后自动启用,勿手删门控)。
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from myssia.wechat import sidecar as wls

#: 接线门控:四动作入 _ACTIONS 后自动启用(rationale 见模块 docstring)。
_ACTIONS_WIRED = all(
    action in wls._ACTIONS
    for action in ("sns_feed", "sns_export", "media_scan", "media_decrypt")
)

pytestmark = pytest.mark.skipif(
    not _ACTIONS_WIRED,
    reason="待集成员接线批:wechat_local_sidecar._ACTIONS 扩 sns_feed/sns_export/"
    "media_scan/media_decrypt(10-14-wechat-media-sns integrationSpec)",
)

SNS_FEED_PAYLOAD = {
    "sns": {
        "mode": "feed",
        "since_days": 30,
        "feed": [
            {
                "id": "9001",
                "username": "wxid_a",
                "nickname": "昵称甲",
                "create_time": 1760000000,
                "text": "合成正文",
                "media_count": 2,
                "media_types": ["2", "2"],
                "ref_username": None,
                "ref_nickname": None,
            }
        ],
        "rows_total": 1,
        "rows_out_of_window": 0,
        "parse_errors": 0,
    }
}

SNS_EXPORT_PAYLOAD = {
    "sns_export": {
        "format": "html",
        "out_dir": "/tmp/exports/sns-20261014",
        "files": ["index.html"],
        "with_media": False,
        "stats": {"entries": 1, "comment_link_rate": "1/2"},
    }
}

MEDIA_SCAN_PAYLOAD = {
    "media": {
        "chat_id": "filehelper",
        "since_days": 30,
        "items": [
            {
                "message_ref": {"ts": 1760000000, "sender": "wxid_a", "local_type": 3},
                "type": "image",
                "key": "a" * 32,
                "files": {"thumb": "/abs/x_t.dat", "full": "/abs/x.dat"},
                "status": "已解密",
                "cached_path": "/cache/a.jpg",
            }
        ],
        "stats": {"messages": 1, "image": 1, "video": 0, "other": 0},
        "provider": {"configured": True, "path": "/abs/provider"},
    }
}

MEDIA_DECRYPT_PAYLOAD = {
    "media_decrypt": {
        "dat_path": "/abs/x_t.dat",
        "cached_path": "/cache/a.jpg",
        "ext": "jpg",
        "is_wxgf": False,
        "width": 640,
        "height": 480,
        "cache": "miss",
    }
}


@pytest.fixture()
def fake_bridge(tmp_path, monkeypatch):
    """fake bridge(照 test_wechat_local_handlers 惯例;键取 argv[1:4] 三段,
    localdb media/sns 的二级子命令才不撞键)。"""
    calls: list[dict[str, Any]] = []
    responses: dict[str, tuple[int, str]] = {}
    bridge_bin = tmp_path / "fake-wechat-bridge"
    bridge_bin.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    bridge_bin.chmod(0o755)

    def fake_run(argv, input_text, timeout):
        calls.append({"argv": list(argv), "timeout": timeout})
        key = " ".join(argv[1:4])
        exit_code, stdout = responses.get(key, (0, json.dumps(MEDIA_SCAN_PAYLOAD)))
        return exit_code, stdout, ""

    monkeypatch.setattr(wls, "_BASE", str(bridge_bin))
    monkeypatch.setattr(wls, "run_bridge_command_sync", fake_run)
    return calls, responses


class TestSnsFeed:
    def test_default_since_30d_argv(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb sns feed"] = (0, json.dumps(SNS_FEED_PAYLOAD))
        payload = wls.handle_wechat_local("sns_feed", {})
        assert payload == SNS_FEED_PAYLOAD
        assert calls[0]["argv"][1:] == [
            "localdb", "sns", "feed", "--since", "30d", "--json",
        ]
        assert calls[0]["timeout"] >= 300  # 盖住副本首建(判例同 query 600s)

    def test_since_days_forwarded(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb sns feed"] = (0, json.dumps(SNS_FEED_PAYLOAD))
        wls.handle_wechat_local("sns_feed", {"since_days": 3})
        assert calls[0]["argv"][calls[0]["argv"].index("--since") + 1] == "3d"

    def test_bad_params_rejected(self, fake_bridge):
        for params in ({"since_days": 0}, {"since_days": "7"}, {"since_days": 9999}):
            with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
                wls.handle_wechat_local("sns_feed", params)
            assert excinfo.value.code == "invalid_params"


class TestSnsExport:
    def test_default_argv_and_passthrough(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb sns export"] = (0, json.dumps(SNS_EXPORT_PAYLOAD))
        payload = wls.handle_wechat_local("sns_export", {})
        assert payload == SNS_EXPORT_PAYLOAD
        argv = calls[0]["argv"][1:]
        assert argv[:6] == ["localdb", "sns", "export", "--format", "json", "--since"]
        assert argv[argv.index("--since") + 1] == "30d"
        assert argv[-1] == "--json"
        assert "--with-media" not in argv
        assert "--out" not in argv

    def test_out_and_with_media_forwarded(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb sns export"] = (0, json.dumps(SNS_EXPORT_PAYLOAD))
        wls.handle_wechat_local(
            "sns_export",
            {"format": "html", "out": "/tmp/my-export", "with_media": True},
        )
        argv = calls[0]["argv"]
        assert argv[argv.index("--format") + 1] == "html"
        assert argv[argv.index("--out") + 1] == "/tmp/my-export"
        assert "--with-media" in argv

    def test_bad_format_rejected(self, fake_bridge):
        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("sns_export", {"format": "xml"})
        assert excinfo.value.code == "invalid_params"
        assert excinfo.value.path == "params.format"


class TestMediaScan:
    def test_argv_and_passthrough(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb media scan"] = (0, json.dumps(MEDIA_SCAN_PAYLOAD))
        payload = wls.handle_wechat_local(
            "media_scan", {"chat_id": "filehelper"}
        )
        assert payload == MEDIA_SCAN_PAYLOAD
        argv = calls[0]["argv"][1:]
        assert argv[:5] == ["localdb", "media", "scan", "filehelper", "--since"]
        assert argv[argv.index("--since") + 1] == "30d"
        assert "--decrypt" not in argv

    def test_decrypt_flag_forwarded(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb media scan"] = (0, json.dumps(MEDIA_SCAN_PAYLOAD))
        wls.handle_wechat_local(
            "media_scan", {"chat_id": "x", "since_days": 7, "decrypt": True}
        )
        argv = calls[0]["argv"]
        assert "--decrypt" in argv
        assert argv[argv.index("--since") + 1] == "7d"

    def test_chat_id_required(self, fake_bridge):
        for params in ({}, {"chat_id": ""}, {"chat_id": 123}, {"decrypt": "yes"}):
            with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
                wls.handle_wechat_local("media_scan", params)
            assert excinfo.value.code == "invalid_params"


class TestMediaDecrypt:
    def test_argv_and_passthrough(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb media decrypt"] = (0, json.dumps(MEDIA_DECRYPT_PAYLOAD))
        payload = wls.handle_wechat_local(
            "media_decrypt", {"dat_path": "/abs/x_t.dat"}
        )
        assert payload == MEDIA_DECRYPT_PAYLOAD
        assert calls[0]["argv"][1:] == [
            "localdb", "media", "decrypt", "/abs/x_t.dat", "--json",
        ]

    def test_dat_path_required(self, fake_bridge):
        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("media_decrypt", {"dat_path": "  "})
        assert excinfo.value.code == "invalid_params"

    def test_media_unavailable_passthrough(self, fake_bridge):
        """AC1:未配置解密件 → exit 23 media_unavailable 码名原样上抛。"""
        calls, responses = fake_bridge
        responses["localdb media decrypt"] = (
            23,
            json.dumps(
                {
                    "error": {
                        "code": "media_unavailable",
                        "message": "未配置媒体解密件,请在设置中指定可执行文件路径",
                        "fix_hint": "localdb media-decrypt set <path>",
                    }
                },
                ensure_ascii=False,
            ),
        )
        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("media_decrypt", {"dat_path": "/abs/x.dat"})
        assert excinfo.value.code == "media_unavailable"
        assert excinfo.value.data == {"fix_hint": "localdb media-decrypt set <path>"}
