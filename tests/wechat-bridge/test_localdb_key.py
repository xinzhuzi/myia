"""密钥模块单测(E1 零内存 + 0.4.0 内存管道 + setuid 自愈;零真实微信材料——红线 6)。

合成 page1 按公开 SQLCipher 4 页格式构造(salt/数据区/IV/HMAC-SHA512,
mac_key=PBKDF2-HMAC-SHA512(key, salt⊕0x3A, 2 轮));合成 key_info.db 按
A3 实测 schema。校验机制(verify/extract/acquire)与 0.4.0 内存管道
(C 收集器 subprocess / sqlcipher 试开全 mock)在此全链验证——真机材料
与真实进程永不入测试;C 收集器源码级守卫(只读 mach 四调用,零 exec)
钉死在 native/collector.c。
"""

from __future__ import annotations

import hashlib
import hmac
import os
import sqlite3
import struct
from pathlib import Path

import pytest

import wechat_bridge.localdb as localdb
import wechat_bridge.memsearch as memsearch
from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError
from wechat_bridge.config import BridgeConfig
from wechat_bridge.localdb import (
    acquire_key,
    extract_key_candidates,
    key_cache_path,
    locate_key_info_db,
    page1_targets,
    read_key_cache,
    resolve_keys,
    verify_key_for_page,
    verify_key_mapping,
    write_key_cache,
)

PAGE_SZ = 4096


def _varint(value: int) -> bytes:
    out = bytearray()
    while True:
        b = value & 0x7F
        value >>= 7
        if value:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def make_page1(key: bytes, salt: bytes | None = None) -> bytes:
    """合成加密库 page1(对已知 key 可通过 verify_key_for_page)。"""
    salt = salt if salt is not None else bytes(range(16))
    mac_salt = bytes(b ^ 0x3A for b in salt)
    mac_key = hashlib.pbkdf2_hmac("sha512", key, mac_salt, 2, dklen=32)
    data = bytes(4000)  # page1 加密数据区 [16:4016](合成数据不参与解密)
    iv = bytes(16)  # [4016:4032]
    hm = hmac.new(mac_key, data + iv, hashlib.sha512)
    hm.update(struct.pack("<I", 1))
    return salt + data + iv + hm.digest()


def make_key_blob(key: bytes, *, ts: int = 1791713859, version: int = 2024) -> bytes:
    """合成 key_info_data BLOB(A3 实测 protobuf 形状:f1=168B 载荷/f2 版本/f3 时间戳)。

    key 藏在 168B 载荷的 [32:64](公开结构报告的「32 字节跨库常量」位)。
    """
    payload = bytearray(168)
    payload[32:64] = key
    return (
        b"\x0a" + _varint(168) + bytes(payload)  # field1
        + b"\x10" + _varint(version)  # field2
        + b"\x18" + _varint(ts)  # field3
    )


def make_key_db(path: Path, blobs: list[bytes]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.execute(
        "CREATE TABLE LoginKeyInfoTable(user_name_md5 TEXT, key_md5 TEXT, "
        "key_info_md5 TEXT, key_info_data BLOB)"
    )
    for blob in blobs:
        con.execute(
            "INSERT INTO LoginKeyInfoTable VALUES (?,?,?,?)",
            ("a" * 32, "", hashlib.md5(blob).hexdigest(), blob),
        )
    con.commit()
    con.close()
    return path


def make_account(root: Path, key: bytes) -> tuple[Path, Path]:
    """合成账号树:db_storage(含一个加密库)+ all_users/login/key_info.db。"""
    account = root / "wxid_demo_8253"
    msg_db = account / "db_storage" / "message" / "message_0.db"
    msg_db.parent.mkdir(parents=True, exist_ok=True)
    with msg_db.open("wb") as fh:
        fh.write(make_page1(key))
    key_db = make_key_db(
        root / "all_users" / "login" / "wxid_demo" / "key_info.db",
        [make_key_blob(key)],
    )
    return account / "db_storage", key_db


SALT_LEN = 16  # noqa: F841 - 备忘:salt 定长 16(SQLCipher 4)


class TestVerify:
    def test_right_key_verifies(self) -> None:
        key = bytes(range(32))
        assert verify_key_for_page(key, make_page1(key)) is True

    def test_wrong_key_fails(self) -> None:
        page1 = make_page1(bytes(range(32)))
        assert verify_key_for_page(b"\x01" * 32, page1) is False

    def test_short_page_fails(self) -> None:
        assert verify_key_for_page(b"\x00" * 32, b"x" * 100) is False


class TestExtract:
    def test_finds_key_at_const_offset_window(self) -> None:
        key = bytes(range(32))
        candidates = extract_key_candidates([make_key_blob(key)])
        assert key in candidates

    def test_sha256_derivation_included(self) -> None:
        blob = make_key_blob(b"\x0a" * 32)
        candidates = extract_key_candidates([blob])
        assert hashlib.sha256(blob).digest() in candidates

    def test_candidates_deduped_32b_only(self) -> None:
        key = bytes(32)
        candidates = extract_key_candidates([make_key_blob(key), make_key_blob(key)])
        assert len(candidates) == len(set(candidates))
        assert all(len(c) == 32 for c in candidates)

    def test_malformed_blob_yields_no_crash(self) -> None:
        """坏 BLOB 不炸:候选可能为空,有候选也必为 32B(形状合法)。"""
        candidates = extract_key_candidates([b"\xff\xff\xff", b"", b"\x08\x96\x80"])
        assert all(len(cand) == 32 for cand in candidates)


class TestAcquirePositive:
    def test_full_chain_with_synthetic_material(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """合成材料全链:BLOB 藏 key → 候选 → page1 校验命中 → 缓存落盘。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)
        matched = acquire_key(db_storage, files_root=tmp_path)
        assert matched == {"message/message_0.db": key.hex()}
        cache = read_key_cache(data_root=tmp_path / "home")
        assert cache is not None and cache["message/message_0.db"] == key.hex()
        # 缓存文件 600 权限(红线 6 全套)。
        assert (key_cache_path(data_root=tmp_path / "home").stat().st_mode & 0o777) == 0o600


class TestAcquireNegative:
    def test_no_key_info_db_is_honest_21(self, tmp_path: Path) -> None:
        account = tmp_path / "wxid_demo_8253"
        (account / "db_storage" / "message").mkdir(parents=True)
        with pytest.raises(BridgeError) as excinfo:
            acquire_key(account / "db_storage", files_root=tmp_path)
        err = excinfo.value
        assert err.exit_code == KEY_UNAVAILABLE == 21
        assert err.name == "key_unavailable"
        assert "D4" in (err.fix_hint or "")

    def test_infeasible_material_reports_shape_only(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """材料在但不匹配(真实世界负结论形态):exit 21 + 形状计数 + 零材料泄漏。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, key_db = make_account(tmp_path, bytes(range(32)))
        # 库的 page1 用另一把 key → 候选全不命中。
        stale_page1 = make_page1(b"\xab" * 32, salt=bytes(range(16, 32)))
        (db_storage / "message" / "message_0.db").write_bytes(stale_page1)
        with pytest.raises(BridgeError) as excinfo:
            acquire_key(db_storage, files_root=tmp_path, key_db=key_db)
        err = excinfo.value
        assert err.exit_code == 21
        message = str(err)
        for token in ("候选", "校验"):
            assert token in message
        assert "D4" in (err.fix_hint or "")
        # 真实 key / 其 hex 绝不出现在错误消息(红线 6)。
        assert bytes(range(32)).hex() not in message
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_schema_drift_is_honest_21(self, tmp_path: Path) -> None:
        key_db = tmp_path / "all_users" / "login" / "wx" / "key_info.db"
        key_db.parent.mkdir(parents=True)
        con = sqlite3.connect(key_db)
        con.execute("CREATE TABLE Other(x)")
        con.commit()
        con.close()
        with pytest.raises(BridgeError) as excinfo:
            acquire_key(tmp_path / "wxid_1_1" / "db_storage", files_root=tmp_path, key_db=key_db)
        assert excinfo.value.exit_code == 21
        assert "schema" in str(excinfo.value)


class TestLocateKeyInfo:
    def test_prefers_account_prefix(self, tmp_path: Path) -> None:
        (tmp_path / "all_users" / "login" / "wxid_demo").mkdir(parents=True)
        (tmp_path / "all_users" / "login" / "other").mkdir(parents=True)
        match = make_key_db(tmp_path / "all_users" / "login" / "wxid_demo" / "key_info.db", [])
        make_key_db(tmp_path / "all_users" / "login" / "other" / "key_info.db", [])
        db_storage = tmp_path / "wxid_demo_8253" / "db_storage"
        db_storage.mkdir(parents=True)
        assert locate_key_info_db(db_storage, files_root=tmp_path) == match

    def test_missing_is_21(self, tmp_path: Path) -> None:
        with pytest.raises(BridgeError) as excinfo:
            locate_key_info_db(tmp_path / "a" / "db_storage", files_root=tmp_path)
        assert excinfo.value.exit_code == 21


class TestPage1Targets:
    def test_small_first_and_skip_small_files(self, tmp_path: Path) -> None:
        big = tmp_path / "message" / "big.db"
        small = tmp_path / "session" / "small.db"
        big.parent.mkdir(parents=True)
        small.parent.mkdir(parents=True)
        big.write_bytes(b"\x00" * (PAGE_SZ * 3))
        small.write_bytes(make_page1(b"\x01" * 32))
        tiny = tmp_path / "tiny.db"
        tiny.write_bytes(b"\x00" * 100)  # < PAGE_SZ,跳过
        targets = page1_targets(tmp_path)
        assert [rel for rel, _sz, _p1 in targets] == ["session/small.db", "message/big.db"]


class TestVerifyMapping:
    """密钥映射逐条重验(keys.json 消费前的放行门;宁缺毋假)。"""

    def test_right_key_passes_wrong_key_dropped(self, tmp_path: Path) -> None:
        key = bytes(range(32))
        db_storage, _ = make_account(tmp_path, key)
        verified = verify_key_mapping(
            db_storage,
            {
                "message/message_0.db": key.hex(),
                "message/other.db": ("ff" * 32),  # 库不在场 → 弃
            },
        )
        assert verified == {"message/message_0.db": key.hex()}

    def test_wrong_key_for_existing_db_dropped(self, tmp_path: Path) -> None:
        db_storage, _ = make_account(tmp_path, bytes(range(32)))
        assert verify_key_mapping(db_storage, {"message/message_0.db": "ab" * 32}) == {}

    def test_non_hex_and_wrong_length_dropped(self, tmp_path: Path) -> None:
        key = bytes(range(32))
        db_storage, _ = make_account(tmp_path, key)
        verified = verify_key_mapping(
            db_storage,
            {
                "message/message_0.db": "not-hex!",
                "message/message_0.db2": "aabb",  # 库不在场
            },
        )
        assert verified == {}


class TestResolveKeys:
    """D4② 外部密钥消费通路(resolve_keys):keys.json 重验 → 零内存回落。"""

    def test_external_keys_file_closes_chain_without_zero_memory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """主人放置 keys.json(全量验证命中)→ 一步闭合,零内存途径不触达。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _ = make_account(tmp_path, key)
        # 主人以任意手段放置(与缓存同位同权;组件 write_key_cache 同一路径)。
        write_key_cache({"message/message_0.db": key.hex()}, data_root=tmp_path / "home")

        def _must_not_run(*_a: object, **_k: object) -> dict[str, str]:
            raise AssertionError("keys.json 全量命中后不应回落零内存途径")

        monkeypatch.setattr("wechat_bridge.localdb.acquire_key", _must_not_run)
        resolved = resolve_keys(db_storage, files_root=tmp_path)
        assert resolved == {"message/message_0.db": key.hex()}

    def test_wrong_keys_file_falls_through_with_honest_note(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """keys.json 在场但验证不过 → 回落零内存;exit 21 如实并入 keys.json 未命中。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, key_db = make_account(tmp_path, bytes(range(32)))
        # 库 page1 用另一把 key → keys.json 错、零内存候选族也全不命中(真负结论)。
        # 注:错 key 取 "cd"*32(b"\xcd"*32);不可取 "ab"*32 —— 它 hex 解码即
        # b"\xab"*32,恰是 page1 的真 key,验证器放行是对的(宁缺毋假的反面教材)。
        stale_page1 = make_page1(b"\xab" * 32, salt=bytes(range(16, 32)))
        (db_storage / "message" / "message_0.db").write_bytes(stale_page1)
        write_key_cache({"message/message_0.db": "cd" * 32}, data_root=tmp_path / "home")
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(db_storage, files_root=tmp_path, key_db=key_db)
        err = excinfo.value
        assert err.exit_code == 21
        assert "keys.json" in str(err)
        # 真 key / 其 hex 绝不入错误消息(红线 6)。
        assert bytes(range(32)).hex() not in str(err)

    def test_partial_keys_file_falls_to_zero_memory_full_hit(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """keys.json 只盖部分库 → 回落零内存途径;其全量命中照常放行。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, key_db = make_account(tmp_path, key)
        second = db_storage / "session" / "session.db"
        second.parent.mkdir(parents=True, exist_ok=True)
        second.write_bytes(make_page1(key, salt=bytes(range(16, 32))))  # 同 key 交叉可用
        write_key_cache({"message/message_0.db": key.hex()}, data_root=tmp_path / "home")
        resolved = resolve_keys(db_storage, files_root=tmp_path, key_db=key_db)
        assert resolved == {
            "message/message_0.db": key.hex(),
            "session/session.db": key.hex(),
        }
        # 零内存全量命中照常落缓存(缓存=全量验证子集)。
        cache = read_key_cache(data_root=tmp_path / "home")
        assert cache is not None and "session/session.db" in cache

    def test_no_keys_file_keeps_zero_memory_exit21_untouched(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """keys.json 缺位 → 纯 E1 零内存负结论原样(exit 21;无 keys.json 并注)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, key_db = make_account(tmp_path, bytes(range(32)))
        stale_page1 = make_page1(b"\xab" * 32, salt=bytes(range(16, 32)))
        (db_storage / "message" / "message_0.db").write_bytes(stale_page1)
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(db_storage, files_root=tmp_path, key_db=key_db)
        err = excinfo.value
        assert err.exit_code == 21
        assert "keys.json" not in str(err)
        assert "零内存途径" in str(err)


class TestMemsearchShell:
    """内存搜索(D4 豁免执行件,0.4.0 管道):三重门 + 新管道全 mock 全链。

    D4 豁免口径(主人 2026-10-11「全部解决」令;2026-10-13 固化令换轨
    C 收集器管道):mach 只读逻辑全在 native/collector.c(本模块零 ctypes/
    零 mach),收集器 subprocess 与 sqlcipher 试开全 mock,绝不触碰真实
    进程/真实 sqlcipher;材料全合成(红线 6)。
    """

    # —— 门:缺省关 + 逐门拒(既有测试锚,语义不变)——
    def test_default_off_and_refuses(self, tmp_path: Path) -> None:

        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(
                tmp_path, config=BridgeConfig(), pids=[1]
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "默认关" in str(err)
        assert "mem_search_enabled" in str(err)

    def test_enabled_but_not_elevated_refuses(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        # 豁免令检查在平台门之后:非 darwin CI 上须钉住平台判定才能到门
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        # 数据根指到空目录:keyscanner 未装 → 门③只剩 euid(非 root)即拒。
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))

        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(
                tmp_path,
                config=BridgeConfig(mem_search_enabled=True),
                elevated=False,
                pids=[1],
            )
        assert excinfo.value.exit_code == 21
        assert "提权" in str(excinfo.value)
        assert "密码" in excinfo.value.fix_hint  # 豁免令边界:绝不索要密码

    def test_non_darwin_refuses(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:

        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: False)
        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(
                tmp_path,
                config=BridgeConfig(mem_search_enabled=True),
                elevated=True,
                pids=[1],
            )
        assert excinfo.value.exit_code == 21
        assert "darwin" in str(excinfo.value)

    def test_pids_absent_is_exit10(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:

        db_storage, _key_db = make_account(tmp_path, bytes(range(32)))
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(
                db_storage,
                config=BridgeConfig(mem_search_enabled=True),
                elevated=True,
                pids=[],
            )
        assert excinfo.value.exit_code == 10

    def test_keyscanner_elevation_in_place(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """门③新形态:setuid keyscanner 在位 = 提权在位(免 sudo 扫描的判据)。"""
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        monkeypatch.setattr(memsearch, "_current_euid_is_root", lambda: False)
        data_root = tmp_path / "home"
        assert memsearch.self_heal_armed(
            config=BridgeConfig(mem_search_enabled=True), data_root=data_root
        ) is False
        scanner = memsearch.keyscanner_path(data_root=data_root)
        scanner.parent.mkdir(parents=True)
        scanner.write_bytes(b"#!/bin/sh\nexit 0\n")
        scanner.chmod(0o4750)  # 假件:只验形状判据,永不执行
        assert memsearch.keyscanner_available(data_root=data_root) is True
        assert memsearch.self_heal_armed(
            config=BridgeConfig(mem_search_enabled=True), data_root=data_root
        ) is True
        # 配置门缺省关 → 即便件在位也不武装(三重门缺一不可)。
        assert memsearch.self_heal_armed(config=BridgeConfig(), data_root=data_root) is False
        scanner.chmod(0o750)  # 掉 setuid 位 = 未安装语义
        assert memsearch.keyscanner_available(data_root=data_root) is False

    # —— 守卫:源码级红线钉死(mach 只读逻辑只许活在 C 收集器源码)——
    @staticmethod
    def _c_code_only(source: str) -> str:
        """C 源去注释(守卫只打代码;注释里的 API 名是文档不是调用)。"""
        import re

        no_block = re.sub(r"/\*.*?\*/", " ", source, flags=re.S)
        return re.sub(r"//[^\n]*", " ", no_block)

    @staticmethod
    def _py_code_only(source: str) -> str:
        """Python 源去注释/文档串(tokenize;守卫只打代码)。"""
        import io
        import tokenize

        tokens: list[str] = []
        try:
            for tok in tokenize.generate_tokens(io.StringIO(source).readline):
                if tok.type not in (tokenize.COMMENT, tokenize.STRING):
                    tokens.append(tok.string)
        except tokenize.TokenError:  # pragma: no cover - 源码恒可 tokenize
            return source
        return " ".join(tokens)

    def test_collector_source_readonly_guards(self) -> None:
        """C 收集器:只读机械在场;写/注入/调试/exec 类 API 零引用(setuid 审计焦点)。"""
        source = self._c_code_only(
            (
                Path(memsearch.__file__).resolve().parents[1] / "native" / "collector.c"
            ).read_text(encoding="utf-8")
        )
        # 只读机械必须真实在场(不是装样子的空壳)。
        for required in ("task_for_pid", "mach_vm_region", "mach_vm_read", "mach_vm_deallocate"):
            assert required in source, f"只读机械缺位: {required}"
        # 写/注入/调试/子进程类 API 一个字都不许出现(固化红线:零 exec)。
        for forbidden in (
            "vm_write",
            "vm_protect",
            "vm_copy",
            "ptrace",
            "task_set_",
            "task_suspend",
            "task_resume",
            "thread_create",
            "thread_set_",
            "task_policy",
            "OpenProcess",
            "WriteProcessMemory",
            "popen",
            "system",
            "fork",
            "posix_spawn",
        ):
            assert forbidden not in source, f"只读收集器不得出现: {forbidden}"

    def test_memsearch_module_has_no_mach_or_exec(self) -> None:
        """桥侧 Python:零 ctypes/mach(内存接触全在 C 件)/零外壳执行。"""
        source = self._py_code_only(Path(memsearch.__file__).read_text(encoding="utf-8"))
        for forbidden in ("ctypes", "task_for_pid", "mach_vm", "shell =", "os.system"):
            assert forbidden not in source, f"memsearch 模块不得出现: {forbidden}"

    # —— 新管道全链(收集器/sqlcipher 全 mock;材料全合成)——
    @staticmethod
    def _collector_stdout(hex_keys: list[str]) -> bytes:
        return ("\n".join(hex_keys) + "\n").encode("utf-8")

    @staticmethod
    def _sqlcipher_opens_only(true_hex: str):
        """试开 mock:仅真钥匙(缺省参数组)开锁,其余变体/候选全拒。"""
        calls: list[tuple[str, str]] = []

        def runner(argv: list[str], input_bytes: bytes) -> "subprocess.CompletedProcess[bytes]":
            import subprocess as sp

            sql = input_bytes.decode("utf-8")
            key_hex = sql.split("x'")[1].split("'")[0]
            calls.append((key_hex, argv[1]))
            opened = key_hex == true_hex and "cipher_" not in sql
            out = b"1\n" if opened else b""
            return sp.CompletedProcess(
                args=argv, returncode=0 if opened else 1, stdout=out, stderr=b"" if opened else b"file is not a database"
            )

        return runner, calls

    def _run_scan(self, tmp_path, monkeypatch, *, stdout: bytes, sqlcipher_runner):
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        key = bytes(range(1, 33))  # 32B 无零字节、高熵(>3.5 bits/B)
        db_storage, _key_db = make_account(tmp_path, key)
        fake_binary = tmp_path / "fake-collector"
        fake_binary.write_bytes(b"")
        collector_calls: list[tuple[list[str], bytes]] = []

        def collector_runner(argv: list[str], input_bytes: bytes):
            import subprocess as sp

            collector_calls.append((list(argv), input_bytes))
            return sp.CompletedProcess(
                args=argv, returncode=0, stdout=stdout, stderr=b"salts: 1\ncandidates: 2\n"
            )

        payload = memsearch.acquire_key_from_memory(
            db_storage,
            config=BridgeConfig(mem_search_enabled=True),
            targets=page1_targets(db_storage),
            elevated=True,
            pids=[4242],
            data_root=tmp_path / "home",
            collector_binary=fake_binary,
            collector_runner=collector_runner,
            sqlcipher_runner=sqlcipher_runner,
        )
        return key, db_storage, payload, collector_calls

    def test_pipeline_full_chain_hit(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """新管道全链:收集器候选 → 熵筛 → sqlcipher 试开 → 交叉验证 → keys.json(600)。"""
        key = bytes(range(1, 33))
        runner, calls = self._sqlcipher_opens_only(key.hex())
        decoy_low = ("00" * 32)  # 全零:熵 0,预筛即弃
        payload_keys = [decoy_low, key.hex()]
        _key, db_storage, payload, collector_calls = self._run_scan(
            tmp_path, monkeypatch,
            stdout=self._collector_stdout(payload_keys), sqlcipher_runner=runner,
        )
        assert payload["matched"] == {"count": 1, "total": 1}
        scan = payload["scan"]
        assert scan["pids"] == [4242]
        assert scan["candidates"] == 2
        assert scan["entropy_kept"] == 1  # 全零候选被熵筛弃
        assert scan["sqlcipher_hits"] == 1
        assert scan["salts"] == 1
        # 收集器收到:白名单 argv(pid)+ stdin 盐清单(page1 前 16B)。
        argv, stdin_bytes = collector_calls[0]
        assert argv == [str(tmp_path / "fake-collector"), "4242"]
        assert stdin_bytes.decode().strip() == bytes(range(16)).hex()
        # 试开只打了熵筛后的候选(全零候选零试开)。
        assert [c[0] for c in calls] == [key.hex()]
        # 缓存落盘 600;内容 = canonical 验证后的映射。
        cache_path = tmp_path / "home" / "wechat-localdb" / "keys.json"
        assert (cache_path.stat().st_mode & 0o777) == 0o600
        cache = read_key_cache(data_root=tmp_path / "home")
        assert cache == {"message/message_0.db": key.hex()}
        # 候选临时件用后即清(红线 6:密钥材料只进 keys.json 私有区)。
        assert not (tmp_path / "home" / "wechat-localdb" / "scan").exists()

    def test_zero_hit_is_honest_exit21(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """零命中:exit 21 + 形状计数;不落缓存。"""
        key = bytes(range(1, 33))
        runner, _calls = self._sqlcipher_opens_only(key.hex())
        with pytest.raises(BridgeError) as excinfo:
            self._run_scan(
                tmp_path, monkeypatch,
                stdout=self._collector_stdout([("ab" * 32)]), sqlcipher_runner=runner,
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "零命中" in str(err)
        assert "候选" in str(err) and "试开" in str(err)
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_partial_hit_no_cache(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """两库一库命中:部分命中不落缓存(缓存=全量验证子集)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        key_a, key_b = bytes(range(1, 33)), bytes(range(33, 65))
        account = tmp_path / "wxid_demo_8253"
        (account / "db_storage" / "message").mkdir(parents=True)
        (account / "db_storage" / "message" / "message_0.db").write_bytes(
            make_page1(key_a)
        )
        (account / "db_storage" / "session").mkdir(parents=True)
        (account / "db_storage" / "session" / "session.db").write_bytes(
            make_page1(key_b)
        )
        runner, _calls = self._sqlcipher_opens_only(key_a.hex())
        import subprocess as sp

        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(
                account / "db_storage",
                config=BridgeConfig(mem_search_enabled=True),
                targets=page1_targets(account / "db_storage"),
                elevated=True,
                pids=[1],
                data_root=tmp_path / "home",
                collector_binary=tmp_path / "fake",
                collector_runner=lambda argv, data: sp.CompletedProcess(
                    args=argv, returncode=0,
                    stdout=(key_a.hex() + "\n").encode(), stderr=b"",
                ),
                sqlcipher_runner=runner,
            )
        assert excinfo.value.exit_code == 21
        assert "部分命中" in str(excinfo.value)
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_collector_failure_is_honest_exit21(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """收集器失败(task_for_pid 被拒形状):exit 21 如实,不规避。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        db_storage, _key_db = make_account(tmp_path, bytes(range(1, 33)))
        import subprocess as sp

        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(
                db_storage,
                config=BridgeConfig(mem_search_enabled=True),
                targets=page1_targets(db_storage),
                elevated=True,
                pids=[1],
                data_root=tmp_path / "home",
                collector_binary=tmp_path / "fake",
                collector_runner=lambda argv, data: sp.CompletedProcess(
                    args=argv, returncode=1, stdout=b"",
                    stderr=b"task_for_pid failed: 5\n",
                ),
                sqlcipher_runner=lambda argv, data: sp.CompletedProcess(
                    args=argv, returncode=1, stdout=b"", stderr=b""
                ),
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "task_for_pid" in str(err)
        assert read_key_cache(data_root=tmp_path / "home") is None

    def test_collector_binary_missing_cc_structured_error(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """收集器不可得(keyscanner 未装/组件 bin 未编/cc 缺装):结构化 exit 21 + CLT 指引。"""
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        monkeypatch.setattr(memsearch, "_current_euid_is_root", lambda: True)
        monkeypatch.setattr(memsearch, "_cc_available", lambda: False)
        # 组件 bin/collector 若已编(本机真跑过)会短路解析——钉住组件根到空目录。
        empty_root = tmp_path / "empty-component"
        (empty_root / "native").mkdir(parents=True)
        (empty_root / "native" / "collector.c").write_text("/* stub */\n")
        monkeypatch.setattr(memsearch, "_component_root", lambda: empty_root)
        db_storage, _key_db = make_account(tmp_path, bytes(range(1, 33)))

        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(
                db_storage,
                config=BridgeConfig(mem_search_enabled=True),
                elevated=True,
                pids=[1],
                data_root=tmp_path / "home",
            )
        err = excinfo.value
        assert err.exit_code == 21
        assert "cc" in str(err) or "Xcode" in str(err)
        assert "xcode-select" in (err.fix_hint or "")

    def test_keyscanner_preferred_over_component_build(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """二进制解析序:setuid 自愈件优先于组件 bin/(免 sudo 的根基)。"""
        monkeypatch.setattr(memsearch, "_platform_is_darwin", lambda: True)
        data_root = tmp_path / "home"
        scanner = memsearch.keyscanner_path(data_root=data_root)
        scanner.parent.mkdir(parents=True)
        scanner.write_bytes(b"")
        scanner.chmod(0o4750)
        resolved, kind = memsearch.resolve_collector_binary(data_root=data_root)
        assert kind == "keyscanner"
        assert resolved == scanner

    # —— 缓存/进程定位(保留锚)——
    def test_find_wechat_pids_parses_pgrep(self) -> None:
        import subprocess as sp

        class FakeResult:
            returncode = 0
            stdout = b"85172\n85173\n"

        pids = memsearch.find_wechat_pids(runner=lambda argv: FakeResult())
        assert pids == [85172, 85173]

        class FailResult:
            returncode = 1
            stdout = b""
        assert memsearch.find_wechat_pids(runner=lambda argv: FailResult()) == []

    def test_cache_roundtrip_and_bad_json(self, tmp_path: Path) -> None:
        """缓存读写回环 + 坏 JSON 如实 None + 600 权限(红线 6)。"""
        assert read_key_cache(data_root=tmp_path) is None
        path = key_cache_path(data_root=tmp_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{not json", encoding="utf-8")
        assert read_key_cache(data_root=tmp_path) is None
        write_map = {"a/b.db": "00" * 32}
        written = write_key_cache(write_map, data_root=tmp_path)
        assert (written.stat().st_mode & 0o777) == 0o600
        assert read_key_cache(data_root=tmp_path) == write_map

    def test_entropy_prefilter_shape(self) -> None:
        """熵筛配方:全零/单字节=0;真随机 32B ≥ 3.5 bits/B。"""
        assert memsearch.entropy_bits_per_byte(bytes(32)) == 0.0
        assert memsearch.entropy_bits_per_byte(b"\xab" * 32) == 0.0
        assert (
            memsearch.entropy_bits_per_byte(bytes(range(32)))
            >= memsearch.ENTROPY_MIN_BITS_PER_BYTE
        )

    def test_param_sets_shape(self) -> None:
        """参数变体 4 组(/tmp verify.py 已验配方;缺省组在首位=E2 消费参数)。"""
        assert len(memsearch.PARAM_SETS) == 4
        assert memsearch.PARAM_SETS[0] == ()


class TestSelfHeal:
    """setuid 自愈钩子(0.4.0):query 链密钥缺位/失效零人工重取的口径;
    0.4.1 失败退避:未闭合落冷却戳,窗内零重扫(损坏即忘却不卡死)。"""

    def test_self_heal_dormant_without_armed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """未武装(配置关/件未装):resolve_keys 保持现状语义(E1 如实 21)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, key_db = make_account(tmp_path, bytes(range(32)))
        stale_page1 = make_page1(b"\xab" * 32, salt=bytes(range(16, 32)))
        (db_storage / "message" / "message_0.db").write_bytes(stale_page1)

        def _must_not_run(*_a: object, **_k: object) -> dict[str, str]:
            raise AssertionError("未武装时不得触达自愈扫描")

        monkeypatch.setattr("wechat_bridge.memsearch.try_self_heal", _must_not_run)
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(db_storage, files_root=tmp_path, key_db=key_db)
        assert excinfo.value.exit_code == 21

    def test_self_heal_closes_cache_miss(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """缓存缺位 + 件在位 + 门开 → 自愈重取,query 链一步闭合。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(32))
        db_storage, _key_db = make_account(tmp_path, key)

        def fake_heal(storage, *, config, targets=None, data_root=None):
            write_key_cache({"message/message_0.db": key.hex()}, data_root=data_root)
            return {"message/message_0.db": key.hex()}

        monkeypatch.setattr(
            "wechat_bridge.memsearch.self_heal_armed",
            lambda *, config, data_root=None: True,
        )
        monkeypatch.setattr("wechat_bridge.memsearch.try_self_heal", fake_heal)

        def _must_not_run(*_a: object, **_k: object) -> dict[str, str]:
            raise AssertionError("自愈闭合后不应回落 E1 零内存途径")

        monkeypatch.setattr("wechat_bridge.localdb.acquire_key", _must_not_run)
        resolved = resolve_keys(db_storage, files_root=tmp_path, config=BridgeConfig(mem_search_enabled=True))
        assert resolved == {"message/message_0.db": key.hex()}
        assert read_key_cache(data_root=tmp_path / "home") is not None

    def test_self_heal_failure_falls_through_with_note(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """自愈未闭合(如实 None)→ 回落 E1;exit 21 并入自愈注记。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, key_db = make_account(tmp_path, bytes(range(32)))
        stale_page1 = make_page1(b"\xab" * 32, salt=bytes(range(16, 32)))
        (db_storage / "message" / "message_0.db").write_bytes(stale_page1)
        monkeypatch.setattr(
            "wechat_bridge.memsearch.self_heal_armed",
            lambda *, config, data_root=None: True,
        )
        monkeypatch.setattr(
            "wechat_bridge.memsearch.try_self_heal",
            lambda *a, **k: None,
        )
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(
                db_storage,
                files_root=tmp_path,
                key_db=key_db,
                config=BridgeConfig(mem_search_enabled=True),
            )
        assert excinfo.value.exit_code == 21
        assert "自愈" in str(excinfo.value)

    def test_try_self_heal_gate_guards(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """try_self_heal 本体:未武装 → 零扫描;武装 + 扫描未闭合 → None +
        落冷却戳(600);冷却窗内 → 零扫描直 None(0.4.1 失败退避);
        过窗重扫 → 全量命中落缓存并返回验证映射,且成功清戳。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _key_db = make_account(tmp_path, bytes(range(1, 33)))
        # 假 setuid 件(只验形状判据,永不执行)+ 配置开 = 武装;
        # 件未装/配置关 = 未武装(三重门缺一不可)。
        scanner = memsearch.keyscanner_path(data_root=tmp_path / "home")
        scanner.parent.mkdir(parents=True)
        scanner.write_bytes(b"")
        scanner.chmod(0o4750)

        def _must_not_scan(*_a: object, **_k: object) -> dict[str, object]:
            raise AssertionError("未武装/冷却窗内不得扫描")

        monkeypatch.setattr(memsearch, "acquire_key_from_memory", _must_not_scan)
        assert (
            memsearch.try_self_heal(
                db_storage, config=BridgeConfig(), data_root=tmp_path / "home"
            )
            is None
        )

        t0 = 1_800_000_000.0
        monkeypatch.setattr(
            memsearch,
            "acquire_key_from_memory",
            lambda *a, **k: (_ for _ in ()).throw(BridgeError(21, "零命中(注入)")),
        )
        assert (
            memsearch.try_self_heal(
                db_storage,
                config=BridgeConfig(mem_search_enabled=True),
                data_root=tmp_path / "home",
                now=t0,
            )
            is None
        )
        stamp = memsearch.self_heal_cooldown_path(data_root=tmp_path / "home")
        assert stamp.is_file()
        assert (stamp.stat().st_mode & 0o777) == 0o600  # 冷却戳私有区 600

        # 冷却窗内:直接 None,零扫描——不可闭合态不再逐次 query 重读
        # 微信全进程内存(复审 medium;分钟级扫描 × 无限次重试的退避)。
        monkeypatch.setattr(memsearch, "acquire_key_from_memory", _must_not_scan)
        assert (
            memsearch.try_self_heal(
                db_storage,
                config=BridgeConfig(mem_search_enabled=True),
                data_root=tmp_path / "home",
                now=t0 + 60.0,
            )
            is None
        )

        key = bytes(range(1, 33))

        def fake_scan(storage, *, config, **_k):
            write_key_cache({"message/message_0.db": key.hex()}, data_root=tmp_path / "home")
            return {"matched": {"count": 1, "total": 1}, "scan": {}, "cache": "x"}

        monkeypatch.setattr(memsearch, "acquire_key_from_memory", fake_scan)
        healed = memsearch.try_self_heal(
            db_storage,
            config=BridgeConfig(mem_search_enabled=True),
            data_root=tmp_path / "home",
            now=t0 + memsearch.SELF_HEAL_COOLDOWN_SECONDS + 1.0,  # 过窗重扫
        )
        assert healed == {"message/message_0.db": key.hex()}
        assert not stamp.exists()  # 成功闭合 = 冷却理由消失,戳即清

    def test_self_heal_cooldown_remaining_bounds(self, tmp_path: Path) -> None:
        """冷却剩余纯函数边界:缺/坏 JSON/形状不符 → 0(损坏即忘却,
        负缓存绝不把自愈永久卡死);窗内递减;过窗 → 0;未来戳(时钟
        回拨)→ 恒整窗(阻塞上界有界)。"""
        data_root = tmp_path / "home"
        t0 = 1_800_000_000.0
        assert memsearch.self_heal_cooldown_remaining(data_root=data_root, now=t0) == 0.0
        memsearch._record_self_heal_failure(data_root=data_root, now=t0)
        window = memsearch.SELF_HEAL_COOLDOWN_SECONDS
        assert memsearch.self_heal_cooldown_remaining(data_root=data_root, now=t0) == window
        mid = memsearch.self_heal_cooldown_remaining(
            data_root=data_root, now=t0 + window - 1.0
        )
        assert 0.0 < mid <= window
        assert memsearch.self_heal_cooldown_remaining(
            data_root=data_root, now=t0 + window + 1.0
        ) == 0.0
        stamp = memsearch.self_heal_cooldown_path(data_root=data_root)
        stamp.write_text("{corrupt", encoding="utf-8")
        assert memsearch.self_heal_cooldown_remaining(data_root=data_root, now=t0) == 0.0
        stamp.write_text('["not", "a", "dict"]', encoding="utf-8")
        assert memsearch.self_heal_cooldown_remaining(data_root=data_root, now=t0) == 0.0
        stamp.write_text('{"failed_at": "not-a-number"}', encoding="utf-8")
        assert memsearch.self_heal_cooldown_remaining(data_root=data_root, now=t0) == 0.0
        stamp.write_text(f'{{"failed_at": {t0 + 999_999.0}}}', encoding="utf-8")
        assert memsearch.self_heal_cooldown_remaining(data_root=data_root, now=t0) == window

    def test_self_heal_cooldown_corrupt_stamp_still_scans(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """冷却戳损坏 → 自愈照常重扫(损坏即忘却),失败后重写合法戳。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _key_db = make_account(tmp_path, bytes(range(1, 33)))
        scanner = memsearch.keyscanner_path(data_root=tmp_path / "home")
        scanner.parent.mkdir(parents=True)
        scanner.write_bytes(b"")
        scanner.chmod(0o4750)
        memsearch.self_heal_cooldown_path(data_root=tmp_path / "home").write_text(
            "{corrupt", encoding="utf-8"
        )
        scanned: list[bool] = []

        def fake_scan(*_a: object, **_k: object) -> dict[str, object]:
            scanned.append(True)
            raise BridgeError(21, "零命中(注入)")

        monkeypatch.setattr(memsearch, "acquire_key_from_memory", fake_scan)
        assert (
            memsearch.try_self_heal(
                db_storage,
                config=BridgeConfig(mem_search_enabled=True),
                data_root=tmp_path / "home",
                now=1_800_000_000.0,
            )
            is None
        )
        assert scanned == [True]  # 损坏戳没挡住重扫
        assert memsearch.self_heal_cooldown_remaining(
            data_root=tmp_path / "home", now=1_800_000_000.0
        ) == memsearch.SELF_HEAL_COOLDOWN_SECONDS  # 失败重写合法戳

    def test_resolve_keys_cooldown_note_is_honest(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """武装 + 冷却窗内:resolve_keys 零重扫,exit 21 如实注记「冷却中」
        (不谎称重取过——诚实语义与「未闭合」措辞区分)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, key_db = make_account(tmp_path, bytes(range(32)))
        stale_page1 = make_page1(b"\xab" * 32, salt=bytes(range(16, 32)))
        (db_storage / "message" / "message_0.db").write_bytes(stale_page1)
        monkeypatch.setattr(
            "wechat_bridge.memsearch.self_heal_armed",
            lambda *, config, data_root=None: True,
        )
        memsearch._record_self_heal_failure(data_root=tmp_path / "home")

        def _must_not_heal(*_a: object, **_k: object) -> dict[str, str]:
            raise AssertionError("冷却窗内不得触达自愈扫描")

        monkeypatch.setattr("wechat_bridge.memsearch.try_self_heal", _must_not_heal)
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(
                db_storage,
                files_root=tmp_path,
                key_db=key_db,
                config=BridgeConfig(mem_search_enabled=True),
            )
        assert excinfo.value.exit_code == 21
        assert "冷却" in str(excinfo.value)

    def test_query_history_decrypt_failure_cooldown_propagates(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """E2 解密失败 + 武装 + 冷却窗内 → 零重扫,decrypt_failed 原样透传
        (query_history 钩子受 try_self_heal 内部冷却门节流,0.4.1)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _key_db = make_account(tmp_path, bytes(range(1, 33)))
        scanner = memsearch.keyscanner_path(data_root=tmp_path / "home")
        scanner.parent.mkdir(parents=True)
        scanner.write_bytes(b"")
        scanner.chmod(0o4750)
        memsearch._record_self_heal_failure(data_root=tmp_path / "home")

        def fake_ensure(*_a: object, **_k: object) -> dict[str, object]:
            raise BridgeError(22, "sqlcipher 解密失败(注入)")

        def _must_not_scan(*_a: object, **_k: object) -> dict[str, object]:
            raise AssertionError("冷却窗内不得触达自愈扫描")

        monkeypatch.setattr("wechat_bridge.localdb.ensure_decrypted_copies", fake_ensure)
        monkeypatch.setattr(memsearch, "acquire_key_from_memory", _must_not_scan)
        with pytest.raises(BridgeError) as excinfo:
            localdb.query_history(
                BridgeConfig(mem_search_enabled=True),
                db_storage,
                {"message/message_0.db": "cd" * 32},
                "filehelper",
                7,
                data_root=tmp_path / "home",
            )
        assert excinfo.value.exit_code == 22

    def test_query_history_decrypt_failure_heals_once(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """E2 解密失败(密钥失效形状)→ 自愈重取 → 重建一次 → 查询成功。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        key = bytes(range(1, 33))
        db_storage, _key_db = make_account(tmp_path, key)
        stale_keys = {"message/message_0.db": "cd" * 32}
        healed_keys = {"message/message_0.db": key.hex()}
        copy_infos: list[dict[str, object]] = []

        def fake_ensure(_storage, keys_mapping, **_k):
            copy_infos.append(dict(keys_mapping))
            if len(copy_infos) == 1:
                raise BridgeError(22, "sqlcipher 解密失败(注入:密钥失效)")
            return {"dir": str(tmp_path / "dec"), "built": ["message/message_0.db"], "kept": [], "skipped": [], "total_bytes": 1}

        monkeypatch.setattr("wechat_bridge.localdb.ensure_decrypted_copies", fake_ensure)
        monkeypatch.setattr(
            "wechat_bridge.memsearch.self_heal_armed",
            lambda *, config, data_root=None: True,
        )
        monkeypatch.setattr(
            "wechat_bridge.memsearch.try_self_heal",
            lambda *a, **k: healed_keys,
        )
        monkeypatch.setattr(
            "wechat_bridge.localdb_query.run_query",
            lambda **_k: {"messages": [], "healed": True},
        )
        result = localdb.query_history(
            BridgeConfig(mem_search_enabled=True),
            db_storage,
            stale_keys,
            "filehelper",
            7,
            data_root=tmp_path / "home",
        )
        assert result == {"messages": [], "healed": True}
        assert copy_infos == [stale_keys, healed_keys]  # 第二次用自愈后的钥匙

    def test_query_history_decrypt_failure_unarmed_propagates(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """未武装时解密失败原样透传(不吞、不谎报)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _key_db = make_account(tmp_path, bytes(range(1, 33)))

        def fake_ensure(*_a, **_k):
            raise BridgeError(22, "sqlcipher 解密失败(注入)")

        monkeypatch.setattr("wechat_bridge.localdb.ensure_decrypted_copies", fake_ensure)
        with pytest.raises(BridgeError) as excinfo:
            localdb.query_history(
                BridgeConfig(),
                db_storage,
                {"message/message_0.db": "cd" * 32},
                "filehelper",
                7,
                data_root=tmp_path / "home",
            )
        assert excinfo.value.exit_code == 22

    def test_query_history_decrypt_failure_heal_none_propagates(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """武装但自愈未闭合(None)→ decrypt_failed 原样(不制造半真状态)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage, _key_db = make_account(tmp_path, bytes(range(1, 33)))

        def fake_ensure(*_a, **_k):
            raise BridgeError(22, "sqlcipher 解密失败(注入)")

        monkeypatch.setattr("wechat_bridge.localdb.ensure_decrypted_copies", fake_ensure)
        monkeypatch.setattr(
            "wechat_bridge.memsearch.self_heal_armed",
            lambda *, config, data_root=None: True,
        )
        monkeypatch.setattr(
            "wechat_bridge.memsearch.try_self_heal",
            lambda *a, **k: None,
        )
        with pytest.raises(BridgeError) as excinfo:
            localdb.query_history(
                BridgeConfig(mem_search_enabled=True),
                db_storage,
                {"message/message_0.db": "cd" * 32},
                "filehelper",
                7,
                data_root=tmp_path / "home",
            )
        assert excinfo.value.exit_code == 22


class TestSudoOwnerRestore:
    """sudo 会话落盘属主归还(v1 已验锚,0.4.0 原样保留)。"""

    def test_sudo_write_restores_owner_to_invoking_user(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """sudo 会话(euid==0 + SUDO_UID/SUDO_GID)落盘属主归还发起用户。

        D4 复审缺陷回归:门③只放行 root,root 写缓存建成 root 属主后,
        用户侧 query 读不动(PermissionError 被 read_key_cache 如实 None
        语义收编)→ resolve_keys 静默回落 E1,命中被谎报为零命中。
        """
        monkeypatch.setattr(os, "geteuid", lambda: 0)
        monkeypatch.setenv("SUDO_UID", str(os.getuid()))
        monkeypatch.setenv("SUDO_GID", str(os.getgid()))
        chowns: list[tuple[str, int, int]] = []
        monkeypatch.setattr(
            os, "chown", lambda p, u, g, **_k: chowns.append((str(p), u, g))
        )
        write_key_cache({"a/b.db": "00" * 32}, data_root=tmp_path)
        file_path = key_cache_path(data_root=tmp_path)
        expected = (os.getuid(), os.getgid())
        assert (str(file_path), *expected) in chowns
        assert (str(file_path.parent), *expected) in chowns
        assert (file_path.stat().st_mode & 0o777) == 0o600  # 600 权限语义不变

    def test_root_without_sudo_env_no_chown(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """非 sudo 的 root 会话无从判定目标属主:不 chown,落盘不受影响。"""
        monkeypatch.setattr(os, "geteuid", lambda: 0)
        monkeypatch.delenv("SUDO_UID", raising=False)
        monkeypatch.delenv("SUDO_GID", raising=False)
        chowns: list[tuple[object, ...]] = []
        monkeypatch.setattr(os, "chown", lambda *a, **k: chowns.append(a))
        write_key_cache({"a/b.db": "00" * 32}, data_root=tmp_path)
        assert chowns == []
        assert read_key_cache(data_root=tmp_path) is not None

    def test_sudo_uid_dirty_value_not_fatal(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """SUDO_UID 脏值(非数字):归还失败不拦落盘(文档尾部 chown 兜底)。"""
        monkeypatch.setattr(os, "geteuid", lambda: 0)
        monkeypatch.setenv("SUDO_UID", "not-a-number")
        monkeypatch.setenv("SUDO_GID", "0")
        write_key_cache({"a/b.db": "00" * 32}, data_root=tmp_path)
        assert read_key_cache(data_root=tmp_path) is not None
