"""localdb key-status / key-acquire 单测(D2/D3,task 10-13-wechat-monitor-ui;
契约 = design §A.1/§A.2,协议 v1.1 = docs/wechat-keyprovider.md §12)。

真子进程假取钥器 + 合成账号树(装配复用 test_localdb_keyprovider 同族件);
材料全合成(红线 6:零真实微信材料)。七个用例族对齐 implement.md D 节验证
清单:key_status 三态 / key_status 恒 exit0 / key_acquire 短路 already_ready /
force 走假 provider 正例 / 未配 exit21 文案 / hint clamp 边界 / progress 转印顺序;
外加 D3 硬规格的「启动清残留哨兵」。
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import pytest

from bridge_testkit import run_cli

import wechat_bridge.localdb as localdb
from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError
from wechat_bridge.config import BridgeConfig
from wechat_bridge.localdb import (
    KEY_ACQUIRE_TIMEOUT_HINT_DEFAULT,
    KEY_STATUS_SAMPLE_MAX,
    PROVIDER_TIMEOUT_HINT_MAX_SECONDS,
    PROVIDER_TIMEOUT_HINT_MIN_SECONDS,
    PROVIDER_UNCONFIGURED_MESSAGE,
    clamp_provider_timeout,
    key_acquire,
    key_status,
    read_key_cache,
    cancel_sentinel_path,
)

# 同目录既有装配复用(合成账号树 + 假取钥器脚本件)。
from test_localdb_key import make_account, make_page1
from test_localdb_keyprovider import _echo_provider, _salt, _success_result


def _seed_ready_cache(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, bytes]:
    """合成账号树 + 已闭合密钥缓存(ready 态);回 (db_storage, page1)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
    key = bytes(range(32))
    db_storage, _key_db = make_account(tmp_path, key)
    localdb.write_key_cache(
        {"message/message_0.db": key.hex()}, data_root=tmp_path / "home"
    )
    page1 = (db_storage / "message" / "message_0.db").read_bytes()[:4096]
    return db_storage, page1


def run_cli_lines(
    argv: list[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> tuple[int, list[dict]]:
    """进程内跑 CLI,stdout 按 NDJSON 行解析(key-acquire 流形态专用;
    run_cli 的整流单 JSON 解析对 progress+终态流不适用)。"""
    import wechat_bridge.cli as cli

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    stdout = io.StringIO()
    real_stdout = sys.stdout
    monkeypatch.setattr(sys, "stdout", stdout)
    try:
        exit_code = cli.main(argv)
    finally:
        monkeypatch.setattr(sys, "stdout", real_stdout)
    lines = [ln for ln in stdout.getvalue().splitlines() if ln.strip()]
    return exit_code, [json.loads(ln) for ln in lines]


class TestKeyStatusThreeStates:
    """用例①:key_status 三态(§A.1 判据表逐行)。"""

    def test_missing_state(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        status = key_status(
            data_root=tmp_path / "home",
            files_root=tmp_path,
            version_of=lambda: "4.1.15",
        )["key_status"]
        assert status == {
            "state": "missing",
            "db_count": 0,
            "acquired_at": None,
            "wechat_version": "4.1.15",
            "verdict_note": "密钥缓存缺位",
        }

    def test_ready_state(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        db_storage, _page1 = _seed_ready_cache(tmp_path, monkeypatch)
        status = key_status(
            data_root=tmp_path / "home",
            files_root=tmp_path,
            version_of=lambda: "4.1.15",
        )["key_status"]
        assert status["state"] == "ready"
        assert status["db_count"] == 1
        assert status["verdict_note"] == "抽样 1 库验真通过"
        # acquired_at = keys.json mtime(ISO 本地时,秒精度)。
        mtime_iso = localdb._iso_local_mtime(
            localdb.key_cache_path(data_root=tmp_path / "home")
        )
        assert status["acquired_at"] == mtime_iso
        assert db_storage.is_dir()

    def test_stale_state_wrong_key(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        # 缓存在场但钥匙失配(微信版本变化/换号后的形态):抽样验真必不过。
        localdb.write_key_cache(
            {"message/message_0.db": (b"\xab" * 32).hex()}, data_root=tmp_path / "home"
        )
        status = key_status(
            data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None
        )["key_status"]
        assert status["state"] == "stale"
        assert status["db_count"] == 1
        assert status["verdict_note"] == "抽样验真失败:0/1"
        assert status["wechat_version"] is None  # 拿不到 = None 如实

    def test_empty_and_broken_cache_are_missing(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """空 dict / 坏 JSON = missing(§A.1:解析失败同缺位,不判错)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        cache = localdb.key_cache_path(data_root=tmp_path / "home")
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text("{}", encoding="utf-8")
        assert key_status(data_root=tmp_path / "home", version_of=lambda: None)[
            "key_status"
        ]["state"] == "missing"
        cache.write_text("{not json", encoding="utf-8")
        assert key_status(data_root=tmp_path / "home", version_of=lambda: None)[
            "key_status"
        ]["state"] == "missing"

    def test_sampling_front_middle_back(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """抽样 = mapping 前中后各 1(5 库取 3):中位库失配 → stale 2/3,
        非抽样库失配不影响判定(抽样是抽查不是全量,key-status 秒级承诺)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        root = tmp_path
        account = root / "wxid_demo_8253"
        keys: dict[str, str] = {}
        for idx, name in enumerate(["a", "b", "c", "d", "e"]):
            key = bytes([idx + 1]) * 32
            db = account / "db_storage" / name / f"{name}.db"
            db.parent.mkdir(parents=True, exist_ok=True)
            db.write_bytes(make_page1(key, salt=bytes([idx]) * 16))
            keys[f"{name}/{name}.db"] = key.hex()
        localdb.write_key_cache(keys, data_root=tmp_path / "home")
        # sorted 前中后 = a/c/e;把 c 的缓存钥换成失配钥 → 抽样验真 2/3。
        keys["c/c.db"] = (b"\xab" * 32).hex()
        localdb.write_key_cache(keys, data_root=tmp_path / "home")
        status = key_status(
            data_root=tmp_path / "home", files_root=root, version_of=lambda: None
        )["key_status"]
        assert status["state"] == "stale"
        assert status["db_count"] == 5
        assert status["verdict_note"] == "抽样验真失败:2/3"
        assert KEY_STATUS_SAMPLE_MAX == 3


class TestKeyStatusAlwaysExitZero:
    """用例②:key-status 恒 exit 0(三态即正常态,不判错)。"""

    def test_missing_exit0(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", tmp_path / "no-root")
        exit_code, payload = run_cli(
            ["localdb", "key-status", "--json"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_status"]["state"] == "missing"

    def test_stale_exit0(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        key = bytes(range(32))
        fake_root = tmp_path / "xwechat_files"
        account = fake_root / "wxid_demo_8253"
        (account / "db_storage" / "message").mkdir(parents=True)
        (account / "db_storage" / "message" / "message_0.db").write_bytes(
            make_page1(key)
        )
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", fake_root)
        localdb.write_key_cache(
            {"message/message_0.db": (b"\xab" * 32).hex()}, data_root=tmp_path
        )
        exit_code, payload = run_cli(
            ["localdb", "key-status", "--json"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_status"]["state"] == "stale"

    def test_ready_exit0(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        key = bytes(range(32))
        fake_root = tmp_path / "xwechat_files"
        account = fake_root / "wxid_demo_8253"
        (account / "db_storage" / "message").mkdir(parents=True)
        (account / "db_storage" / "message" / "message_0.db").write_bytes(
            make_page1(key)
        )
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", fake_root)
        localdb.write_key_cache(
            {"message/message_0.db": key.hex()}, data_root=tmp_path
        )
        exit_code, payload = run_cli(
            ["localdb", "key-status", "--json"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_status"]["state"] == "ready"
        assert payload["key_status"]["db_count"] == 1

    def test_db_root_gone_with_cache_is_stale_not_error(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """库根整体不可定位 + 缓存在场:全抽样按未过计 = stale + exit 0
        (三态封闭,不制造第四态/不判错)。"""
        localdb.write_key_cache(
            {"message/message_0.db": (bytes(range(32))).hex()}, data_root=tmp_path
        )
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", tmp_path / "vanished")
        exit_code, payload = run_cli(
            ["localdb", "key-status", "--json"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_status"]["state"] == "stale"
        assert "库根不可定位" in payload["key_status"]["verdict_note"]


class TestKeyAcquireShortCircuit:
    """用例③:ready 态缺省短路 already_ready(不 spawn 取钥器)。"""

    def test_already_ready_short_circuit(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _db_storage, _page1 = _seed_ready_cache(tmp_path, monkeypatch)
        marker = tmp_path / "provider-ran"
        provider = _echo_provider(
            tmp_path,
            "provider-never.py",
            _success_result({"*": (bytes(range(32))).hex()}),
            extra_before=f"open({str(marker)!r}, 'w').write('ran')",
        )
        forwarded: list[str] = []
        payload = key_acquire(
            config=BridgeConfig(key_provider_path=str(provider)),
            data_root=tmp_path / "home",
            files_root=tmp_path,
            version_of=lambda: "4.1.15",
            emit_line=forwarded.append,
        )["key_acquire"]
        assert payload == {
            "result": "already_ready",
            "db_count": 1,
            "acquired_at": localdb._iso_local_mtime(
                localdb.key_cache_path(data_root=tmp_path / "home")
            ),
            "wechat_version": "4.1.15",
        }
        assert not marker.exists()  # 短路 = 未 spawn(progress 零转印)
        assert forwarded == []

    def test_stale_cache_goes_to_provider_without_force(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """失效场景不空转(grill 决议②的正向面):缓存在场但抽样不过 =
        不短路,无需 --force 直走取钥器。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        page1 = (db_storage / "message" / "message_0.db").read_bytes()[:4096]
        localdb.write_key_cache(
            {"message/message_0.db": (b"\xab" * 32).hex()}, data_root=tmp_path / "home"
        )
        provider = _echo_provider(
            tmp_path, "provider-heal.py", _success_result({_salt(page1): key.hex()})
        )
        payload = key_acquire(
            config=BridgeConfig(key_provider_path=str(provider)),
            data_root=tmp_path / "home",
            files_root=tmp_path,
            version_of=lambda: None,
        )["key_acquire"]
        assert payload["result"] == "ok"
        assert payload["db_count"] == 1
        assert read_key_cache(data_root=tmp_path / "home") == {
            "message/message_0.db": key.hex()
        }  # 失配旧钥被全量验真通过的新钥覆写


class TestKeyAcquireForce:
    """用例④:--force 跳过短路走假 provider 正例。"""

    def test_force_runs_provider_positive(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        _db_storage, page1 = _seed_ready_cache(tmp_path, monkeypatch)
        key = bytes(range(32))
        marker = tmp_path / "provider-ran"
        provider = _echo_provider(
            tmp_path,
            "provider-ok.py",
            _success_result({_salt(page1): key.hex()}),
            extra_before=f"open({str(marker)!r}, 'w').write('ran')",
        )
        payload = key_acquire(
            config=BridgeConfig(key_provider_path=str(provider)),
            force=True,
            data_root=tmp_path / "home",
            files_root=tmp_path,
            version_of=lambda: "4.1.15",
        )["key_acquire"]
        assert payload["result"] == "ok"
        assert payload["db_count"] == 1
        assert marker.exists()  # force = 真跑了取钥器(ready 态不空转)
        assert read_key_cache(data_root=tmp_path / "home") == {
            "message/message_0.db": key.hex()
        }


class TestKeyAcquireUnconfigured:
    """用例⑤:未配置取钥器 = exit 21 法定文案(§F;同 query 缺钥族)。"""

    def test_unconfigured_exit21_legal_message_direct(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        make_account(tmp_path, bytes(range(32)))
        with pytest.raises(BridgeError) as excinfo:
            key_acquire(data_root=tmp_path / "home", files_root=tmp_path)
        err = excinfo.value
        assert err.exit_code == KEY_UNAVAILABLE == 21
        assert err.name == "key_unavailable"
        assert err.message == PROVIDER_UNCONFIGURED_MESSAGE  # 法定文案逐字
        assert "key-provider set" in (err.fix_hint or "")

    def test_unconfigured_exit21_cli_stream(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """CLI 面:错误也是 NDJSON 单行(整流逐行可解析)。"""
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", tmp_path / "no-root")
        exit_code, lines = run_cli_lines(
            ["localdb", "key-acquire", "--json"], monkeypatch, tmp_path
        )
        assert exit_code == 21
        assert len(lines) == 1
        assert lines[0]["error"]["code"] == "key_unavailable"
        assert lines[0]["error"]["message"] == PROVIDER_UNCONFIGURED_MESSAGE


class TestHintClamp:
    """用例⑥:hint clamp 边界(clamp(N,120,1800)双向夹逼)+ 透传形状。"""

    def test_clamp_boundaries(self) -> None:
        assert PROVIDER_TIMEOUT_HINT_MIN_SECONDS == 120
        assert PROVIDER_TIMEOUT_HINT_MAX_SECONDS == 1800
        assert KEY_ACQUIRE_TIMEOUT_HINT_DEFAULT == 600
        for hint, expected in [
            (-5, 120),
            (0, 120),
            (1, 120),
            (119, 120),
            (120, 120),
            (121, 121),
            (600, 600),
            (1800, 1800),
            (1801, 1800),
            (99999, 1800),
        ]:
            assert clamp_provider_timeout(hint) == expected, hint

    def test_hint_clamped_and_passed_in_request(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """hint=5000 → 桥内硬帽 1800,请求透传 timeout_hint_seconds=1800。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        page1 = (db_storage / "message" / "message_0.db").read_bytes()[:4096]
        requests_file = tmp_path / "captured.requests"
        provider = _echo_provider(
            tmp_path,
            "provider-hint.py",
            _success_result({_salt(page1): key.hex()}),
            extra_before=f"open({str(requests_file)!r}, 'a').write(line)",
        )
        key_acquire(
            config=BridgeConfig(key_provider_path=str(provider)),
            timeout_hint=5000,
            data_root=tmp_path / "home",
            files_root=tmp_path,
            version_of=lambda: None,
        )
        request = json.loads(requests_file.read_text(encoding="utf-8"))
        assert request["timeout_hint_seconds"] == 1800
        assert request["action"] == "get_db_key"  # v1 三必含字段原样

    def test_v1_query_path_request_has_no_hint(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """v1 向后兼容:query 链(resolve_keys)请求不带 hint 字段(旧行为)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        page1 = (db_storage / "message" / "message_0.db").read_bytes()[:4096]
        requests_file = tmp_path / "captured.requests"
        provider = _echo_provider(
            tmp_path,
            "provider-v1.py",
            _success_result({_salt(page1): key.hex()}),
            extra_before=f"open({str(requests_file)!r}, 'a').write(line)",
        )
        localdb.resolve_keys(
            db_storage,
            config=BridgeConfig(key_provider_path=str(provider)),
            data_root=tmp_path / "home",
        )
        request = json.loads(requests_file.read_text(encoding="utf-8"))
        assert "timeout_hint_seconds" not in request


class TestProgressForwarding:
    """用例⑦:progress 转印顺序(CLI 全链:stdout = progress 行…+终态单行)。"""

    def test_progress_lines_forwarded_in_order(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        key = bytes(range(32))
        fake_root = tmp_path / "xwechat_files"
        account = fake_root / "wxid_demo_8253"
        (account / "db_storage" / "message").mkdir(parents=True)
        (account / "db_storage" / "message" / "message_0.db").write_bytes(
            make_page1(key)
        )
        page1 = (account / "db_storage" / "message" / "message_0.db").read_bytes()
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", fake_root)
        config_dir = tmp_path / "wechat-bridge"
        config_dir.mkdir(parents=True, exist_ok=True)
        provider = tmp_path / "provider-progress.py"
        payload = "\n".join(
            [
                json.dumps(
                    {"type": "progress", "message": "等待输入管理员密码", "level": 0},
                    ensure_ascii=False,
                ),
                json.dumps(
                    {"type": "progress", "message": "请在微信中退出登录并重新扫码", "level": 0},
                    ensure_ascii=False,
                ),
                json.dumps(
                    _success_result({_salt(page1): key.hex()}), ensure_ascii=False
                ),
            ]
        )
        provider.write_text(
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "sys.stdin.readline()\n"
            f"sys.stdout.write({payload!r})\n"
            "sys.stdout.write('\\n')\n"
            "sys.stdout.flush()\n",
            encoding="utf-8",
        )
        provider.chmod(0o755)
        (config_dir / "config.json").write_text(
            json.dumps({"key_provider_path": str(provider)}), encoding="utf-8"
        )
        exit_code, lines = run_cli_lines(
            ["localdb", "key-acquire", "--json", "--timeout-hint", "600"],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 0
        assert len(lines) == 3
        # progress 两行按序在先(原样转印:type/message 逐字节保留)…
        assert lines[0] == {
            "type": "progress",
            "message": "等待输入管理员密码",
            "level": 0,
        }
        assert lines[1] == {
            "type": "progress",
            "message": "请在微信中退出登录并重新扫码",
            "level": 0,
        }
        # …终态单行 JSON 收尾(恰一行,流闭合)。
        assert lines[2]["key_acquire"]["result"] == "ok"
        assert lines[2]["key_acquire"]["db_count"] == 1


class TestSentinelCleanup:
    """D3 硬规格:启动先清残留哨兵(design §C/§7 风险表)。"""

    def test_startup_clears_residual_sentinel(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        make_account(tmp_path, bytes(range(32)))  # 缓存缺失态(不短路)
        sentinel = cancel_sentinel_path(data_root=tmp_path / "home")
        sentinel.parent.mkdir(parents=True, exist_ok=True)
        sentinel.write_text("", encoding="utf-8")  # 上轮崩溃残留
        # 未配置取钥器 → exit 21;但哨兵清理先于短路/取钥器检查(启动即清)。
        with pytest.raises(BridgeError) as excinfo:
            key_acquire(
                config=BridgeConfig(),
                data_root=tmp_path / "home",
                files_root=tmp_path,
            )
        assert excinfo.value.exit_code == 21
        assert not sentinel.exists()  # 启动即清,残留不跨轮
