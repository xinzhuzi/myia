"""外部取钥器单测(B2/B3/B4,task 10-13-wechat-keyprovider;协议 =
docs/wechat-keyprovider.md)。

全部用**真子进程**假取钥器(tmp 下 shebang 脚本,chmod +x)跑协议全链:
spawn → stdin 单行请求 → stdout NDJSON → 退出码矩阵 → 页1 HMAC 验真 →
缓存落盘。材料全合成(红线 6:零真实微信材料;密钥绝不入错误消息)。
参考实现 examples/keyprovider_ref.py 本体也在此被当真取钥器接线验证(B4)。
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from bridge_testkit import run_cli

import wechat_bridge.localdb as localdb
from wechat_bridge.codes import EXIT_USAGE, KEY_UNAVAILABLE, BridgeError
from wechat_bridge.config import BridgeConfig, load_config
from wechat_bridge.localdb import (
    PROVIDER_UNCONFIGURED_MESSAGE,
    acquire_keys_from_provider,
    key_cache_path,
    read_key_cache,
    resolve_keys,
)

# 合成 page1/账号树构件复用密钥套件的既有装配(同目录模块直取)。
from test_localdb_key import make_account, make_page1

EXAMPLE_PROVIDER = (
    Path(localdb.__file__).resolve().parents[1] / "examples" / "keyprovider_ref.py"
)


def _write_script(tmp_path: Path, name: str, body: str) -> Path:
    """写一个可执行假取钥器(shebang + 0755;真子进程跑)。"""
    script = tmp_path / name
    script.write_text(f"#!/usr/bin/env python3\n{body}", encoding="utf-8")
    script.chmod(0o755)
    return script


def _echo_provider(
    tmp_path: Path,
    name: str,
    result_obj: dict,
    *,
    progress_first: bool = True,
    extra_before: str = "",
) -> Path:
    """守规矩假取钥器:读一行请求 → 回放预构 NDJSON(可选 progress 前置)。"""
    lines: list[str] = []
    if progress_first:
        lines.append(
            json.dumps(
                {"type": "progress", "message": "取钥中(假件)", "level": 0},
                ensure_ascii=False,
            )
        )
    lines.append(json.dumps(result_obj, ensure_ascii=False))
    payload_file = tmp_path / f"{name}.ndjson"
    payload_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return _write_script(
        tmp_path,
        name,
        "import sys\n"
        "line = sys.stdin.readline()\n"
        "assert line.strip(), 'bridge must send one request line'\n"
        + (extra_before + "\n" if extra_before else "")
        + f"sys.stdout.write(open({str(payload_file)!r}, encoding='utf-8').read())\n"
        "sys.stdout.flush()\n",
    )


def _success_result(keys: dict[str, str]) -> dict:
    return {
        "type": "result",
        "success": True,
        "keys": keys,
        "account_id": "wxid_demo",
        "logs": ["fake provider"],
    }


def _salt(page1: bytes) -> str:
    return page1[:16].hex()


class TestProviderPositive:
    def test_salt_keyed_full_chain_via_resolve_keys(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """正例:缓存缺失 → spawn 假取钥器 → 逐把验真 → 落缓存(600)→
        请求形状(action/db_path/account_id)按协议 §3;E1 零内存不触达。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        # 第二个库、另一把 key(微信 4.1+ 每库独立密钥形态)。
        second_key = bytes(range(64, 96))
        second_db = db_storage / "session" / "session.db"
        second_db.parent.mkdir(parents=True, exist_ok=True)
        second_page1 = make_page1(second_key, salt=bytes(range(16, 32)))
        second_db.write_bytes(second_page1)
        first_page1 = (db_storage / "message" / "message_0.db").read_bytes()[:4096]

        requests_file = tmp_path / "captured.requests"
        provider = _echo_provider(
            tmp_path,
            "provider-ok.py",
            _success_result(
                {
                    _salt(first_page1): key.hex(),
                    _salt(second_page1): second_key.hex(),
                }
            ),
            extra_before=f"open({str(requests_file)!r}, 'a').write(line)",
        )

        def _must_not_run(*_a: object, **_k: object) -> dict[str, str]:
            raise AssertionError("取钥器闭合后不应回落零内存途径(协议 §1 无降级的正向面)")

        monkeypatch.setattr("wechat_bridge.localdb.acquire_key", _must_not_run)

        resolved = resolve_keys(
            db_storage,
            files_root=tmp_path,
            config=BridgeConfig(key_provider_path=str(provider)),
            data_root=tmp_path / "home",
        )
        assert resolved == {
            "message/message_0.db": key.hex(),
            "session/session.db": second_key.hex(),
        }
        cache = read_key_cache(data_root=tmp_path / "home")
        assert cache == resolved
        assert (key_cache_path(data_root=tmp_path / "home").stat().st_mode & 0o777) == 0o600
        # 桥发给取钥器的请求形状(协议 §3:单行 JSON,三必含字段)。
        request = json.loads(requests_file.read_text(encoding="utf-8"))
        assert request == {
            "action": "get_db_key",
            "db_path": str(db_storage),
            "account_id": "wxid_demo",  # all_users/login/<wxid> 前缀推导
        }

    def test_wildcard_key_form_covers_all(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """"*" 通配形态(单钥全域;协议 §5)同样闭合。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(1, 33))
        db_storage, _key_db = make_account(tmp_path, key)
        provider = _echo_provider(
            tmp_path, "provider-wild.py", _success_result({"*": key.hex()})
        )
        resolved = resolve_keys(
            db_storage,
            config=BridgeConfig(key_provider_path=str(provider)),
            data_root=tmp_path / "home",
        )
        assert resolved == {"message/message_0.db": key.hex()}

    def test_reference_example_provider_b4(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """B4 参考实现本体当取钥器:读钥匙文件({相对路径: 64hex})→
        盐映射 → 协议应答;桥侧验真闭合(样例即契约活文档)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(7, 39))
        db_storage, _key_db = make_account(tmp_path, key)
        key_file = tmp_path / "my-keys.json"
        key_file.write_text(
            json.dumps({"message/message_0.db": key.hex()}), encoding="utf-8"
        )
        monkeypatch.setenv("KEYPROVIDER_REF_KEYS", str(key_file))
        resolved = resolve_keys(
            db_storage,
            config=BridgeConfig(key_provider_path=str(EXAMPLE_PROVIDER)),
            data_root=tmp_path / "home",
        )
        assert resolved == {"message/message_0.db": key.hex()}
        assert read_key_cache(data_root=tmp_path / "home") == resolved


class TestProviderNegative:
    """四负例(超时/退出码 0 无 result/垃圾钥被拒/非零退出)+ 协议族补充。"""

    def _fixture(self, tmp_path: Path) -> tuple[Path, bytes]:
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        page1 = (db_storage / "message" / "message_0.db").read_bytes()[:4096]
        return db_storage, page1

    def test_timeout_kills_and_exit21(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """负例①超时:120s 预算(测试注入短超时)→ kill 子进程 → exit 21。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _page1 = self._fixture(tmp_path)
        sleeper = _write_script(
            tmp_path,
            "provider-slow.py",
            "import sys, time\nsys.stdin.readline()\n"
            "print('progress', flush=True)\n"
            "time.sleep(30)\n",
        )
        with pytest.raises(BridgeError) as excinfo:
            acquire_keys_from_provider(
                db_storage, str(sleeper), data_root=tmp_path / "home", timeout=2.0
            )
        err = excinfo.value
        assert err.exit_code == KEY_UNAVAILABLE == 21
        assert err.name == "key_unavailable"
        assert "超时" in err.message and "kill" in err.message and "2 秒" in err.message
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_exit0_without_result_is_failure(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """负例②退出码 0 但无 result(协议 §6:「未返回结果」)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _page1 = self._fixture(tmp_path)
        provider = _write_script(
            tmp_path,
            "provider-noresult.py",
            "import sys\n"
            "sys.stdin.readline()\n"
            "sys.stdout.write('{\"type\": \"progress\", \"message\": \"只报进度\", \"level\": 0}\\n')\n"
            "sys.stdout.flush()\n",
        )
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(
                db_storage,
                config=BridgeConfig(key_provider_path=str(provider)),
                data_root=tmp_path / "home",
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "未返回结果" in err.message
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_garbage_key_rejected_no_cache(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """负例③垃圾钥:协议成功形态但钥匙验真不过 → 弃、不落缓存、exit 21。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        page1 = (db_storage / "message" / "message_0.db").read_bytes()[:4096]
        garbage = "cd" * 32  # 非 hex 解码不冲突:解码合法但 HMAC 必不过
        provider = _echo_provider(
            tmp_path, "provider-garbage.py", _success_result({_salt(page1): garbage})
        )
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(
                db_storage,
                config=BridgeConfig(key_provider_path=str(provider)),
                data_root=tmp_path / "home",
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "验真" in err.message and "未入缓存" in err.message
        # 红线 6:任何钥匙(真/假)不入错误消息。
        assert key.hex() not in err.message and garbage not in err.message
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_nonzero_exit_attaches_stderr_tail(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """负例④非零退出且无 result:exit 21 + stderr 尾部(协议 §6)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _page1 = self._fixture(tmp_path)
        provider = _write_script(
            tmp_path,
            "provider-crash.py",
            "import sys\nsys.stdin.readline()\n"
            "sys.stderr.write('取钥器内部炸了:boom-traceback-line\\n' * 40)\n"
            "sys.exit(3)\n",
        )
        with pytest.raises(BridgeError) as excinfo:
            acquire_keys_from_provider(
                db_storage, str(provider), data_root=tmp_path / "home"
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "exit=3" in err.message
        assert "boom-traceback-line" in err.message  # stderr 尾部透出
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_success_false_error_transparent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """result success:false:error 人话透传(协议 §6/§8)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _page1 = self._fixture(tmp_path)
        provider = _echo_provider(
            tmp_path,
            "provider-refuse.py",
            {
                "type": "result",
                "success": False,
                "error": "钥匙串未解锁,请先解锁后重试",
                "logs": ["fake"],
            },
        )
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(
                db_storage,
                config=BridgeConfig(key_provider_path=str(provider)),
                data_root=tmp_path / "home",
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "外部取钥器报告失败" in err.message
        assert "钥匙串未解锁,请先解锁后重试" in err.message

    def test_missing_provider_file_spawn_failure(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """配置路径文件不存在:spawn 失败人话报错含路径(协议 §8)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _page1 = self._fixture(tmp_path)
        ghost = tmp_path / "ghost-provider.py"
        with pytest.raises(BridgeError) as excinfo:
            acquire_keys_from_provider(
                db_storage, str(ghost), data_root=tmp_path / "home"
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "启动失败" in err.message and str(ghost) in err.message

    def test_stale_cache_note_merged_into_provider_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """keys.json 在场但失效 → 取钥器也失败:两条事实都进 exit 21 消息
        (不吞缓存线索;协议 §8 错误族仍收敛 key_unavailable)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _page1 = self._fixture(tmp_path)
        localdb.write_key_cache(
            {"message/message_0.db": "cd" * 32}, data_root=tmp_path / "home"
        )
        provider = _echo_provider(
            tmp_path,
            "provider-refuse2.py",
            {"type": "result", "success": False, "error": "取钥失败XYZ", "logs": []},
        )
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(
                db_storage,
                config=BridgeConfig(key_provider_path=str(provider)),
                data_root=tmp_path / "home",
            )
        message = str(excinfo.value)
        assert excinfo.value.exit_code == 21
        assert "取钥失败XYZ" in message and "keys.json" in message


class TestProviderUnconfigured:
    def test_legal_message_appended_when_unconfigured(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """未配置取钥器:不 spawn,最终 exit 21 消息含法定文案(协议 §8)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, key_db = make_account(tmp_path, bytes(range(32)))
        stale = make_page1(b"\xab" * 32, salt=bytes(range(16, 32)))
        (db_storage / "message" / "message_0.db").write_bytes(stale)
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(db_storage, files_root=tmp_path, key_db=key_db)
        err = excinfo.value
        assert err.exit_code == 21
        assert PROVIDER_UNCONFIGURED_MESSAGE in err.message
        assert "零内存途径" in err.message  # 既有 E1 负结论措辞不被顶掉
        assert "key-provider set" in (err.fix_hint or "")


class TestKeyProviderConfig:
    """B2 配置面:key_provider_path 形状校验 + save_config_key 外科代写。"""

    def test_accepts_string_and_strips(self, tmp_path: Path) -> None:
        path = tmp_path / "config.json"
        path.write_text('{"key_provider_path": "  /usr/local/bin/my-provider  "}', encoding="utf-8")
        assert load_config(path).key_provider_path == "/usr/local/bin/my-provider"

    def test_default_empty_and_null(self, tmp_path: Path) -> None:
        assert BridgeConfig().key_provider_path == ""
        path = tmp_path / "config.json"
        path.write_text('{"key_provider_path": null}', encoding="utf-8")
        assert load_config(path).key_provider_path == ""

    def test_non_string_rejected(self, tmp_path: Path) -> None:
        path = tmp_path / "config.json"
        path.write_text('{"key_provider_path": 5}', encoding="utf-8")
        with pytest.raises(BridgeError) as excinfo:
            load_config(path)
        assert excinfo.value.exit_code == EXIT_USAGE
        assert "key_provider_path" in excinfo.value.message and "字符串" in excinfo.value.message

    def test_payload_exposes_path(self) -> None:
        assert BridgeConfig().to_payload()["key_provider_path"] == ""

    def test_save_config_key_surgical_roundtrip(self, tmp_path: Path) -> None:
        from wechat_bridge.config import save_config_key

        monkey = tmp_path / "cfg"
        monkey.mkdir()
        config_path = monkey / "config.json"
        config_path.write_text(
            json.dumps({"limits": {"messages": 9}}), encoding="utf-8"
        )
        saved = save_config_key(
            "key_provider_path", "/opt/provider", path=config_path
        )
        assert saved == config_path
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        assert raw["key_provider_path"] == "/opt/provider"
        assert raw["limits"] == {"messages": 9}  # 其余键外科保留
        assert (config_path.stat().st_mode & 0o777) == 0o600
        # clear:删除该键(= 回缺省),其余照留。
        save_config_key("key_provider_path", None, path=config_path)
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        assert "key_provider_path" not in raw
        assert load_config(config_path).key_provider_path == ""

    def test_save_config_key_refuses_broken_existing(self, tmp_path: Path) -> None:
        from wechat_bridge.config import save_config_key

        config_path = tmp_path / "config.json"
        original = "{not json"
        config_path.write_text(original, encoding="utf-8")
        with pytest.raises(BridgeError) as excinfo:
            save_config_key("key_provider_path", "/x", path=config_path)
        assert excinfo.value.exit_code == EXIT_USAGE
        assert config_path.read_text(encoding="utf-8") == original  # 拒改不写花


class TestKeyProviderCli:
    """B2 管理命令:localdb key-provider set|get|clear。"""

    def _fake_executable(self, tmp_path: Path) -> Path:
        script = tmp_path / "my-provider"
        script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        script.chmod(0o755)
        return script

    def test_set_rejects_missing_file(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "set", str(tmp_path / "nope.py")],
            monkeypatch,
            tmp_path,
        )
        assert exit_code == 2
        assert payload["error"]["code"] == "usage"
        assert "不存在" in payload["error"]["message"]
        assert str(tmp_path / "nope.py") in payload["error"]["message"]

    def test_set_rejects_non_executable(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        plain = tmp_path / "plain.txt"
        plain.write_text("data", encoding="utf-8")
        plain.chmod(0o644)
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "set", str(plain)], monkeypatch, tmp_path
        )
        assert exit_code == 2
        assert "不可执行" in payload["error"]["message"]

    def test_set_get_clear_roundtrip(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        provider = self._fake_executable(tmp_path)
        # set → 已配置;config.json 落键(数据根私有区)。
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "set", str(provider)], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_provider"]["state"] == "configured"
        assert payload["key_provider"]["path"] == str(provider)
        config_path = tmp_path / "wechat-bridge" / "config.json"
        assert json.loads(config_path.read_text(encoding="utf-8"))["key_provider_path"] == str(provider)
        # get → configured 态。
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "get"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_provider"]["state"] == "configured"
        # 文件被删后 get → missing_file(如实呈态,不判错)。
        provider.unlink()
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "get"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_provider"]["state"] == "missing_file"
        # clear → 未配置;config 键删除。
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "clear"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_provider"]["state"] == "unconfigured"
        assert "key_provider_path" not in json.loads(
            config_path.read_text(encoding="utf-8")
        )
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "get"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_provider"]["state"] == "unconfigured"
        assert payload["key_provider"]["path"] is None

    def test_get_unconfigured_by_default(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        exit_code, payload = run_cli(
            ["localdb", "key-provider", "get"], monkeypatch, tmp_path
        )
        assert exit_code == 0
        assert payload["key_provider"]["state"] == "unconfigured"
        assert "未配置外部取钥器" in payload["key_provider"]["message"]

    def test_set_preserves_existing_config_keys(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        config_dir = tmp_path / "wechat-bridge"
        config_dir.mkdir(parents=True)
        (config_dir / "config.json").write_text(
            json.dumps({"mem_search_enabled": True, "limits": {"sessions": 5}}),
            encoding="utf-8",
        )
        provider = self._fake_executable(tmp_path)
        exit_code, _payload = run_cli(
            ["localdb", "key-provider", "set", str(provider)], monkeypatch, tmp_path
        )
        assert exit_code == 0
        raw = json.loads((config_dir / "config.json").read_text(encoding="utf-8"))
        assert raw["key_provider_path"] == str(provider)
        assert raw["mem_search_enabled"] is True
        assert raw["limits"] == {"sessions": 5}


class TestProviderHygiene:
    """红线守卫:桥侧取钥器链零密钥材料入消息/缓存路径纪律。"""

    def test_no_key_material_in_error_families(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """超时/异常退出/垃圾钥三族消息只承载形状,密钥 hex 零出现。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(11, 43))
        db_storage, _key_db = make_account(tmp_path, key)
        crash = _write_script(
            tmp_path, "provider-crash2.py",
            "import sys\nsys.stdin.readline()\nsys.exit(9)\n",
        )
        with pytest.raises(BridgeError) as excinfo:
            acquire_keys_from_provider(db_storage, str(crash), data_root=tmp_path / "home")
        assert key.hex() not in str(excinfo.value)
