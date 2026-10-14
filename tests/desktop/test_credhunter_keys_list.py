"""_m_credhunter_keys_list 单测(10-14-cred-hunter-panel §3.4 / AC1+AC2)。

数据面 = 本地密钥库纯文件读(MYIA_HOME env 逐例注入,同 _serve_context 惯例);
掩码-only 红线:应答 JSON 序列化文本不得含库内全文 apikey(协议流零全文)。
掩码/路径/错误族三处规则在 entry.py 内联镜像插件侧,本文件对拍插件
findings.mask_apikey(importlib 直载,防镜像漂移)。
"""

from __future__ import annotations

import importlib.util
import json
import logging
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
ENTRY_PATH = REPO_ROOT / "desktop" / "entry.py"

_spec = importlib.util.spec_from_file_location("desktop_entry", ENTRY_PATH)
entry = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(entry)

# 插件侧掩码函数直载对拍(插件动态加载不进包路径;findings.py stdlib-only)
_findings_spec = importlib.util.spec_from_file_location(
    "credhunter_findings",
    REPO_ROOT / "plugins" / "myssia-credhunter" / "credhunter" / "findings.py",
)
findings = importlib.util.module_from_spec(_findings_spec)
_findings_spec.loader.exec_module(findings)


@pytest.fixture(autouse=True)
def _isolated_serve_state(monkeypatch):
    """每例独立:ambient MYIA_HOME 不影响用例(dev 默认前提,协议测试同款);
    serve() 会 configure root logging,快照恢复防泄漏到邻域测试(同款纪律)。"""
    monkeypatch.delenv("MYIA_HOME", raising=False)
    saved_handlers = logging.getLogger().handlers[:]
    saved_factory = logging.getLogRecordFactory()
    yield
    logging.getLogger().handlers[:] = saved_handlers
    logging.setLogRecordFactory(saved_factory)

#: 库内全文密钥夹具(只存在测试库文件与断言里,永不进应答)
FULL_KEY = "xai-Hs5vQCmZ0dGhvdXNhbmRvbWd1aXNlZA-Yc3f"


def _rpc(*requests: dict) -> list[dict]:
    """单轮协议往返(serve stdout 应答行;importlib 直载同门)。"""
    import io

    stdin = io.StringIO("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in requests))
    out = io.StringIO()
    entry.serve(stdin=stdin, stdout=out)
    return [json.loads(line) for line in out.getvalue().splitlines()]


def _write_keystore(home: Path, payload: dict) -> Path:
    path = home / "credhunter-keystore.json"
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def test_registry_registered():
    """方法注册:_HANDLERS 含 credhunter.keys.list(AC1 前半)。"""
    assert entry._HANDLERS["credhunter.keys.list"] is entry._m_credhunter_keys_list


def test_missing_keystore_is_legal_empty(monkeypatch, tmp_path):
    """① exists=false 空态:合法未建库,不报错不建文件(§3.1 冻结形状)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    responses = _rpc({"id": 1, "method": "credhunter.keys.list", "params": {}})
    assert responses[0] == {
        "id": 1,
        "result": {
            "path": str(tmp_path / "credhunter-keystore.json"),
            "exists": False,
            "version": None,
            "count": 0,
            "records": [],
        },
    }
    # 纯读红线:库缺绝不建档(Keystore 构造即建档,handler 不得触发)
    assert not (tmp_path / "credhunter-keystore.json").exists()


def test_projection_masked_sorted_no_full_key(monkeypatch, tmp_path):
    """② 正常投影:掩码前 8 后 4、last_seen 新→旧、sources 透传、
    应答序列化文本不含库内全文 apikey(掩码-only 红线)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    _write_keystore(
        tmp_path,
        {
            "version": 1,
            "records": {
                "sha256-aaaaaaaaaaaaaaaa": {
                    "apikey": FULL_KEY,
                    "provider": "xai",
                    "first_seen": "2026-10-01T00:00:00+00:00",
                    "last_seen": "2026-10-01T00:00:00+00:00",
                    "hit_count": 1763,
                    "sources": ["https://github.com/o/r/blob/main/c1#L1", "https://github.com/o/r/blob/main/c2#L2"],
                    "last_check": None,
                    "check_state": None,
                },
                "sha256-bbbbbbbbbbbbbbbb": {
                    "apikey": "sk-second-key-zzzzzzzzzzzzzzz",
                    "provider": "openai",
                    "first_seen": "2026-09-01T00:00:00+00:00",
                    "last_seen": "2026-10-12T00:00:00+00:00",
                    "hit_count": 2,
                    "sources": ["https://github.com/o/r2/blob/main/c3#L3"],
                    "last_check": "2026-10-13T00:00:00+00:00",
                    "check_state": "final_verified",
                },
            },
        },
    )
    responses = _rpc({"id": 1, "method": "credhunter.keys.list", "params": {}})
    result = responses[0]["result"]
    assert result["exists"] is True and result["version"] == 1 and result["count"] == 2
    # last_seen 新→旧(openai 记录 10-12 在前,xai 记录 10-01 在后)
    assert [r["provider"] for r in result["records"]] == ["openai", "xai"]
    top = result["records"][0]
    assert top["fingerprint"] == "sha256-bbbbbbbbbbbbbbbb"
    assert top["check_state"] == "final_verified" and top["last_check"] == "2026-10-13T00:00:00+00:00"
    xai = result["records"][1]
    assert xai["masked_apikey"] == f"{FULL_KEY[:8]}…MASKED…{FULL_KEY[-4:]}"
    assert xai["sources"] == [
        "https://github.com/o/r/blob/main/c1#L1",
        "https://github.com/o/r/blob/main/c2#L2",
    ]
    assert xai["hit_count"] == 1763
    # 掩码-only 红线:应答整帧序列化不含全文;记录无 apikey 键
    assert FULL_KEY not in json.dumps(responses, ensure_ascii=False)
    assert all("apikey" not in r for r in result["records"])


def test_version_mismatch_structured_invalid(monkeypatch, tmp_path):
    """③ 版本不符 → keystore_invalid 结构化错(镜像 keystore 错误族)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    _write_keystore(tmp_path, {"version": 2, "records": {}})
    responses = _rpc({"id": 1, "method": "credhunter.keys.list", "params": {}})
    assert responses[0]["error"]["code"] == "keystore_invalid"
    assert "version=1" in responses[0]["error"]["message"]


def test_unreadable_keystore_structured_error(monkeypatch, tmp_path):
    """④(AC2)库不可读 → keystore_unreadable(目录占位 = read_text OSError)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "credhunter-keystore.json").mkdir()  # 存在但不可读文本
    responses = _rpc({"id": 1, "method": "credhunter.keys.list", "params": {}})
    assert responses[0]["error"]["code"] == "keystore_unreadable"


def test_short_key_mask_mirrors_plugin_findings(monkeypatch, tmp_path):
    """⑤ 短键掩码退化逐字镜像 findings.mask_apikey:>12 前8+省略+后4;
    9-12 只前 8;≤8 只前 2(防内联镜像漂移,同输入对拍插件侧)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    keys = {
        "sha256-long0000000000": "xai-" + "a" * 20 + "-tail1234",  # >12:前8+后4
        "sha256-mid00000000000": "sk-123456789",  # 9-12:只前 8
        "sha256-tiny0000000000": "abc12345",  # =8:只前 2
        "sha256-mini0000000000": "abc12",  # <8:只前 2
    }
    _write_keystore(
        tmp_path,
        {
            "version": 1,
            "records": {
                fp: {**{"apikey": key, "provider": "p", "first_seen": "2026-10-01T00:00:00+00:00",
                        "last_seen": "2026-10-01T00:00:00+00:00", "hit_count": 1, "sources": [],
                        "last_check": None, "check_state": None}}
                for fp, key in keys.items()
            },
        },
    )
    responses = _rpc({"id": 1, "method": "credhunter.keys.list", "params": {}})
    records = {r["fingerprint"]: r["masked_apikey"] for r in responses[0]["result"]["records"]}
    for fp, key in keys.items():
        assert records[fp] == findings.mask_apikey(key), f"掩码镜像漂移:{fp}"
        assert key not in json.dumps(responses, ensure_ascii=False)
