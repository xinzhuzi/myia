"""E1 密钥模块单测(合成数据全链;零真实微信材料——红线 6)。

合成 page1 按公开 SQLCipher 4 页格式构造(salt/数据区/IV/HMAC-SHA512,
mac_key=PBKDF2-HMAC-SHA512(key, salt⊕0x3A, 2 轮));合成 key_info.db 按
A3 实测 schema。校验机制(verify/extract/acquire)在此全链验证——真机
材料永远不入测试。
"""

from __future__ import annotations

import hashlib
import hmac
import sqlite3
import struct
from pathlib import Path

import pytest

import wechat_bridge.memsearch as memsearch
from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError
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
    """内存搜索空壳(红线 1/3):默认关、恒拒绝、源码零进程 API。"""

    def test_default_off_and_refuses(self) -> None:
        assert memsearch.MEMORY_SEARCH_ENABLED is False
        with pytest.raises(BridgeError) as excinfo:
            memsearch.acquire_key_from_memory(anything=1)
        assert excinfo.value.exit_code == 21
        assert "默认关" in str(excinfo.value)

    def test_source_contains_no_process_api(self) -> None:
        source = Path(memsearch.__file__).read_text(encoding="utf-8")
        for token in (
            "task_for_pid",
            "OpenProcess",
            "ptrace",
            "vm_read",
            "ctypes",
            "subprocess",
            "task_read",
        ):
            assert token not in source, f"空壳不得出现进程级 API 引用: {token}"

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
