"""密钥钥匙串化单测(task 10-14-wechat-keys-keychain;主人令:本地保存应加密)。

mock 钥匙串 = wechat_bridge.keychain 的 pytest 态伪库(进程内 dict,
``PYTEST_CURRENT_TEST`` 自动激活,真钥匙串零触碰——判例同
myssia.secrets.InMemoryKeychainBackend)。材料全合成(红线 6):
三态(钥匙串有/仅文件/都无)+ migrate 往返 + 回退 + 验真门照跑 +
write_key_cache 迁移态明文不回流 + security argv/stdin 零外显纪律。
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

import pytest

from bridge_testkit import run_cli

import wechat_bridge.keychain as keychain
import wechat_bridge.localdb as localdb
from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError
from wechat_bridge.localdb import (
    key_cache_path,
    keys_migrate,
    keys_unmigrate,
    key_status,
    read_key_cache,
    resolve_keys,
    write_key_cache,
)

# 同目录既有装配复用(合成账号树 + page1 构造)。
from test_localdb_key import make_account, make_page1

GOOD_KEY = bytes(range(32))
BAD_KEY = (b"\xab" * 32).hex()


@pytest.fixture(autouse=True)
def fake_keychain():
    """伪钥匙串逐用例隔离(setup/teardown 双清,防跨文件残留污染)。"""
    keychain.reset_fake_store()
    yield keychain.fake_store()
    keychain.reset_fake_store()


def seed_keychain(mapping: dict[str, str], migrated_at: str = "2026-10-14T12:00:00+08:00") -> None:
    """把映射以桥外壳形态种进伪钥匙串。"""
    keychain.fake_store()[keychain.DB_KEYS_ACCOUNT] = keychain.build_db_keys_envelope(
        mapping, migrated_at=migrated_at
    )


def seed_account(tmp_path: Path, key: bytes = GOOD_KEY) -> Path:
    """合成账号树 + db_storage(不落任何缓存;返回 db_storage)。

    注意:make_account 的合成 key_info.db 对 E1 零内存途径**可命中**(E1
    成功测试同款)——「都无 = 空态」类用例须用 :func:`seed_account_no_keyinfo`
    排除 E1 兜底干扰。"""
    db_storage, _key_db = make_account(tmp_path, key)
    return db_storage


def seed_account_no_keyinfo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, key: bytes = GOOD_KEY
) -> Path:
    """无 key_info.db 的账号树(E1 零内存途径 = exit 21,排空态干扰)。"""
    fake_root = tmp_path / "xwechat_files"
    account = fake_root / "wxid_demo_8253"
    db = account / "db_storage" / "message" / "message_0.db"
    db.parent.mkdir(parents=True)
    db.write_bytes(make_page1(key))
    monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", fake_root)
    return account / "db_storage"


def write_file_cache(mapping: dict[str, str], tmp_path: Path) -> Path:
    """直写明文件缓存(绕开 write_key_cache 的迁移态分流——测「双源在场」
    的既有形态:文件先在、钥匙串后迁)。"""
    return localdb._write_key_cache_file(mapping, data_root=tmp_path / "home")


class TestResolveKeysTwoLevel:
    """resolve_keys 两级:钥匙串优先、文件兜底、都无 = 既有空态。"""

    def test_keychain_only_source(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account(tmp_path)
        seed_keychain({"message/message_0.db": GOOD_KEY.hex()})
        assert resolve_keys(db_storage, data_root=tmp_path / "home") == {
            "message/message_0.db": GOOD_KEY.hex()
        }

    def test_file_only_source_compat(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """未迁移态零变化:文件路径照走(兼容面)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account(tmp_path)
        write_key_cache({"message/message_0.db": GOOD_KEY.hex()}, data_root=tmp_path / "home")
        assert resolve_keys(db_storage, data_root=tmp_path / "home") == {
            "message/message_0.db": GOOD_KEY.hex()
        }

    def test_both_absent_existing_empty_state(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """钥匙串与文件都无(且 E1 不可闭合)= 现既有空态 exit 21。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account_no_keyinfo(tmp_path, monkeypatch)
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(db_storage, data_root=tmp_path / "home")
        assert excinfo.value.exit_code == KEY_UNAVAILABLE == 21

    def test_keychain_takes_priority_over_stale_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """双源在场:钥匙串好钥优先(文件失配被兜底层弃用,不硬配)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account_no_keyinfo(tmp_path, monkeypatch)
        write_file_cache({"message/message_0.db": BAD_KEY}, tmp_path)
        seed_keychain({"message/message_0.db": GOOD_KEY.hex()})
        assert resolve_keys(db_storage, data_root=tmp_path / "home") == {
            "message/message_0.db": GOOD_KEY.hex()
        }

    def test_stale_keychain_falls_back_to_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """钥匙串失配(轮换后旧钥)→ 文件兜底接管。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account_no_keyinfo(tmp_path, monkeypatch)
        write_file_cache({"message/message_0.db": GOOD_KEY.hex()}, tmp_path)
        seed_keychain({"message/message_0.db": BAD_KEY})
        assert resolve_keys(db_storage, data_root=tmp_path / "home") == {
            "message/message_0.db": GOOD_KEY.hex()
        }

    def test_bad_envelope_note_and_file_fallback(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """条目值坏形状 = 弃(不硬配),文件兜底;注记进最终错误(排查不盲)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account_no_keyinfo(tmp_path, monkeypatch)
        write_file_cache({"message/message_0.db": BAD_KEY}, tmp_path)
        keychain.fake_store()[keychain.DB_KEYS_ACCOUNT] = "{not json"
        with pytest.raises(BridgeError) as excinfo:
            resolve_keys(db_storage, data_root=tmp_path / "home")
        assert "钥匙串条目在场但值形状不可解析" in excinfo.value.message


class TestKeyStatusSource:
    """key_status 三态 × 源选择(镜像 resolve_keys 消费序,不谎报)。"""

    def test_missing_both_absent(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        status = key_status(
            data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None
        )["key_status"]
        assert status["state"] == "missing"
        assert status["source"] is None
        assert status["db_count"] == 0

    def test_ready_keychain_source_acquired_at_from_envelope(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """钥匙串源 acquired_at = 外壳 migrated_at(条目无 mtime,不谎)。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        seed_keychain({"message/message_0.db": GOOD_KEY.hex()}, migrated_at="2026-10-14T09:30:00+08:00")
        status = key_status(
            data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None
        )["key_status"]
        assert status["state"] == "ready"
        assert status["source"] == "keychain"
        assert status["db_count"] == 1
        assert status["acquired_at"] == "2026-10-14T09:30:00+08:00"
        assert status["verdict_note"] == "抽样 1 库验真通过(源 keychain)"

    def test_ready_file_source_unchanged_semantics(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        write_key_cache({"message/message_0.db": GOOD_KEY.hex()}, data_root=tmp_path / "home")
        status = key_status(
            data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None
        )["key_status"]
        assert status["state"] == "ready"
        assert status["source"] == "file"
        assert status["acquired_at"] == localdb._iso_local_mtime(
            key_cache_path(data_root=tmp_path / "home")
        )

    def test_stale_keychain_rescued_by_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """钥匙串失配 + 文件好钥 = ready(源 file)——镜像 resolve 消费序。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        write_file_cache({"message/message_0.db": GOOD_KEY.hex()}, tmp_path)
        seed_keychain({"message/message_0.db": BAD_KEY})
        status = key_status(
            data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None
        )["key_status"]
        assert status["state"] == "ready"
        assert status["source"] == "file"

    def test_stale_keychain_only_reports_both(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        seed_keychain({"message/message_0.db": BAD_KEY})
        status = key_status(
            data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None
        )["key_status"]
        assert status["state"] == "stale"
        assert status["source"] == "keychain"
        assert status["verdict_note"] == "抽样验真失败:keychain源 0/1"


class TestKeysMigrate:
    """keys-migrate:验真门 + 回读逐字节验证 + 断电安全(文件改名保留)。"""

    def test_happy_path(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account(tmp_path)
        mapping = {"message/message_0.db": GOOD_KEY.hex()}
        path = key_cache_path(data_root=tmp_path / "home")
        write_key_cache(mapping, data_root=tmp_path / "home")
        payload = keys_migrate(data_root=tmp_path / "home", files_root=tmp_path)["keys_migrate"]
        assert payload["db_count"] == 1
        assert payload["verified"] is True
        assert payload["keychain_account"] == "myia/wechat/db-keys"
        assert payload["file_renamed"].startswith("keys.json.migrated-")
        # 条目 = 外壳;材料逐字节一致;明文件已改名(不删)。
        raw = keychain.fake_store()["myia/wechat/db-keys"]
        got, migrated_at = keychain.parse_db_keys_envelope(raw)
        assert got == mapping
        assert migrated_at == payload["migrated_at"]
        assert not path.is_file()
        backup = path.parent / payload["file_renamed"]
        assert backup.is_file()
        assert json.loads(backup.read_text(encoding="utf-8")) == mapping
        assert (backup.stat().st_mode & 0o777) == 0o600
        # 迁移后 key-status 走钥匙串源。
        status = key_status(data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None)["key_status"]
        assert status["state"] == "ready"
        assert status["source"] == "keychain"
        assert db_storage.is_dir()

    def test_missing_file_exit21(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        with pytest.raises(BridgeError) as excinfo:
            keys_migrate(data_root=tmp_path / "home", files_root=tmp_path)
        assert excinfo.value.exit_code == 21
        assert "无物可迁" in excinfo.value.message

    def test_hmac_gate_rejects_bad_keys(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """验真门:文件钥匙失配 = 拒迁,钥匙串与文件都保持原状。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        path = key_cache_path(data_root=tmp_path / "home")
        write_key_cache({"message/message_0.db": BAD_KEY}, data_root=tmp_path / "home")
        with pytest.raises(BridgeError) as excinfo:
            keys_migrate(data_root=tmp_path / "home", files_root=tmp_path)
        assert excinfo.value.exit_code == 21
        assert "拒绝迁移" in excinfo.value.message
        assert "myia/wechat/db-keys" not in keychain.fake_store()
        assert path.is_file()

    def test_readback_mismatch_rolls_back_fresh_entry(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """回读不一致(原无条目)= 删新条目回滚;文件未动。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        write_key_cache({"message/message_0.db": GOOD_KEY.hex()}, data_root=tmp_path / "home")
        real_read = keychain.read_item
        state = {"calls": 0}

        def flaky_read(account: str) -> str | None:
            state["calls"] += 1
            if state["calls"] == 2:  # 回读那次返回坏值
                return "{corrupted"
            return real_read(account)

        monkeypatch.setattr(keychain, "read_item", flaky_read)
        with pytest.raises(BridgeError) as excinfo:
            keys_migrate(data_root=tmp_path / "home", files_root=tmp_path)
        assert excinfo.value.exit_code == 1
        assert "回读验证不一致" in excinfo.value.message
        assert "myia/wechat/db-keys" not in keychain.fake_store()  # 回滚 = 删
        assert key_cache_path(data_root=tmp_path / "home").is_file()  # 文件未动

    def test_readback_mismatch_restores_old_entry(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """回读不一致(原有条目)= 旧值原样回写。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        old_envelope = keychain.build_db_keys_envelope(
            {"message/message_0.db": BAD_KEY}, migrated_at="2026-01-01T00:00:00+08:00"
        )
        write_key_cache({"message/message_0.db": GOOD_KEY.hex()}, data_root=tmp_path / "home")
        # 文件就位后才种「旧条目」(先种会被迁移态 write_key_cache 分流掉)。
        keychain.fake_store()["myia/wechat/db-keys"] = old_envelope
        real_read = keychain.read_item
        state = {"calls": 0}

        def flaky_read(account: str) -> str | None:
            state["calls"] += 1
            if state["calls"] == 2:
                return "wrong"
            return real_read(account)

        monkeypatch.setattr(keychain, "read_item", flaky_read)
        with pytest.raises(BridgeError):
            keys_migrate(data_root=tmp_path / "home", files_root=tmp_path)
        assert keychain.fake_store()["myia/wechat/db-keys"] == old_envelope

    def test_cli_surface(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path))
        fake_root = tmp_path / "xwechat_files"
        account = fake_root / "wxid_demo_8253"
        (account / "db_storage" / "message").mkdir(parents=True)
        (account / "db_storage" / "message" / "message_0.db").write_bytes(make_page1(GOOD_KEY))
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", fake_root)
        write_key_cache({"message/message_0.db": GOOD_KEY.hex()}, data_root=tmp_path)
        exit_code, payload = run_cli(["localdb", "keys-migrate", "--json"], monkeypatch, tmp_path)
        assert exit_code == 0
        assert payload["keys_migrate"]["db_count"] == 1
        assert payload["keys_migrate"]["verified"] is True
        exit_code, status = run_cli(["localdb", "key-status", "--json"], monkeypatch, tmp_path)
        assert exit_code == 0
        assert status["key_status"]["state"] == "ready"
        assert status["key_status"]["source"] == "keychain"

    def test_cli_missing_file_exit21(self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
        monkeypatch.setattr(localdb, "WECHAT_FILES_ROOT", tmp_path / "no-root")
        exit_code, payload = run_cli(["localdb", "keys-migrate", "--json"], monkeypatch, tmp_path)
        assert exit_code == 21
        assert payload["error"]["code"] == "key_unavailable"


class TestKeysUnmigrate:
    """keys-unmigrate:钥匙串→文件(回退用;消费侧验真门照跑)。"""

    def test_happy_path_roundtrip(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        mapping = {"message/message_0.db": GOOD_KEY.hex()}
        seed_keychain(mapping, migrated_at="2026-10-14T08:00:00+08:00")
        payload = keys_unmigrate(data_root=tmp_path / "home")["keys_unmigrate"]
        assert payload["db_count"] == 1
        assert payload["keychain_entry_deleted"] is True
        assert payload["migrated_at"] == "2026-10-14T08:00:00+08:00"
        path = key_cache_path(data_root=tmp_path / "home")
        assert read_key_cache(data_root=tmp_path / "home") == mapping
        assert (path.stat().st_mode & 0o777) == 0o600
        assert "myia/wechat/db-keys" not in keychain.fake_store()
        # 回退后 key-status 走文件源,resolve 照常闭合(验真门在消费侧)。
        status = key_status(data_root=tmp_path / "home", files_root=tmp_path, version_of=lambda: None)["key_status"]
        assert status["state"] == "ready"
        assert status["source"] == "file"

    def test_absent_entry_exit21(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        with pytest.raises(BridgeError) as excinfo:
            keys_unmigrate(data_root=tmp_path / "home")
        assert excinfo.value.exit_code == 21

    def test_migrate_unmigrate_full_roundtrip(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """migrate → unmigrate 往返:材料逐字节回归文件态。"""
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        db_storage = seed_account(tmp_path)
        mapping = {"message/message_0.db": GOOD_KEY.hex()}
        write_key_cache(mapping, data_root=tmp_path / "home")
        keys_migrate(data_root=tmp_path / "home", files_root=tmp_path)
        assert not key_cache_path(data_root=tmp_path / "home").is_file()
        keys_unmigrate(data_root=tmp_path / "home")
        assert read_key_cache(data_root=tmp_path / "home") == mapping
        assert resolve_keys(db_storage, data_root=tmp_path / "home") == mapping


class TestWriteCacheMigratedMode:
    """write_key_cache 迁移态:轮换新钥进钥匙串,明文不回流。"""

    def test_migrated_mode_refreshes_keychain_not_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_account(tmp_path)
        seed_keychain({"message/message_0.db": BAD_KEY}, migrated_at="2026-10-13T00:00:00+08:00")
        fresh = {"message/message_0.db": GOOD_KEY.hex()}
        before = time.time()
        write_key_cache(fresh, data_root=tmp_path / "home")
        got, migrated_at = keychain.parse_db_keys_envelope(
            keychain.fake_store()["myia/wechat/db-keys"]
        )
        assert got == fresh  # 新钥落钥匙串
        assert migrated_at is not None and migrated_at >= "2026-10-14"  # 外壳时间随写刷新
        assert not key_cache_path(data_root=tmp_path / "home").is_file()  # 明文不回流
        assert time.time() >= before - 1

    def test_unmigrated_mode_writes_file_as_before(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        mapping = {"message/message_0.db": GOOD_KEY.hex()}
        path = write_key_cache(mapping, data_root=tmp_path / "home")
        assert path.is_file()
        assert (path.stat().st_mode & 0o777) == 0o600


class TestProbeKeyAvailableTwoSource:
    """探零成本判据两源化:迁移后明文件不在场,条目在场 = True(不谎报)。"""

    def test_true_from_keychain_post_migration(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import wechat_bridge.system_checks as sc

        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        seed_keychain({"message/message_0.db": GOOD_KEY.hex()})
        assert sc.localdb_key_available() is True

    def test_true_from_file_unmigrated(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import wechat_bridge.system_checks as sc

        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        write_file_cache({"message/message_0.db": GOOD_KEY.hex()}, tmp_path)
        assert sc.localdb_key_available() is True

    def test_false_both_absent(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import wechat_bridge.system_checks as sc

        monkeypatch.setenv("MYIA_HOME", str(tmp_path / "home"))
        keychain.fake_store()[keychain.DB_KEYS_ACCOUNT] = "{broken"
        assert sc.localdb_key_available() is False


class TestSecurityDiscipline:
    """security CLI 形状:值零入 argv(stdin 双行供给)、退出码语义、外壳回环。"""

    def test_write_argv_never_carries_value(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """security -i 形态:argv 恒 ["security","-i"],值内联进 stdin 命令行
        (JSON 引号转义)——OS argv/环境零值(128B 截断实测教训后的形态)。"""
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        # 通道可用性是被测前提不是被测对象:非 mac 宿主(CI Linux)也必须能验子进程形状
        monkeypatch.setattr(keychain, "keychain_available", lambda: True)
        recorded: dict[str, object] = {}

        def fake_run(argv, **kwargs):  # noqa: ANN001, ANN202 - 录制形状
            recorded["argv"] = list(argv)
            recorded["input"] = kwargs.get("input")
            return subprocess.CompletedProcess(argv, 0, "", "")

        monkeypatch.setattr(keychain.subprocess, "run", fake_run)
        keychain.write_item("myia/wechat/db-keys", 'VALUE-"SECRET"-\\')
        assert recorded["argv"] == ["security", "-i"]  # argv 零值
        # stdin 命令行 = add-generic-password … -w "<JSON 转义的值>";值不在 argv/环境。
        assert recorded["input"] == (
            'add-generic-password -U -s myia -a myia/wechat/db-keys'
            ' -w "VALUE-\\"SECRET\\"-\\\\"\n\n'
        )
        assert 'VALUE' not in recorded["argv"]

    def test_read_returns_none_on_44(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        # 通道可用性是被测前提不是被测对象:非 mac 宿主(CI Linux)也必须能验子进程形状
        monkeypatch.setattr(keychain, "keychain_available", lambda: True)

        def fake_run(argv, **kwargs):  # noqa: ANN001, ANN202
            return subprocess.CompletedProcess(argv, 44, "", "")

        monkeypatch.setattr(keychain.subprocess, "run", fake_run)
        assert keychain.read_item("myia/wechat/db-keys") is None

    def test_read_strips_single_trailing_newline(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        # 通道可用性是被测前提不是被测对象:非 mac 宿主(CI Linux)也必须能验子进程形状
        monkeypatch.setattr(keychain, "keychain_available", lambda: True)

        def fake_run(argv, **kwargs):  # noqa: ANN001, ANN202
            return subprocess.CompletedProcess(argv, 0, "VALUE-SECRET\n", "")

        monkeypatch.setattr(keychain.subprocess, "run", fake_run)
        assert keychain.read_item("myia/wechat/db-keys") == "VALUE-SECRET"

    def test_read_hard_failure_raises_shape_only(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        # 通道可用性是被测前提不是被测对象:非 mac 宿主(CI Linux)也必须能验子进程形状
        monkeypatch.setattr(keychain, "keychain_available", lambda: True)

        def fake_run(argv, **kwargs):  # noqa: ANN001, ANN202
            return subprocess.CompletedProcess(argv, 51, "", "")

        monkeypatch.setattr(keychain.subprocess, "run", fake_run)
        with pytest.raises(BridgeError) as excinfo:
            keychain.read_item("myia/wechat/db-keys")
        assert excinfo.value.exit_code == 1
        assert "VALUE" not in excinfo.value.message  # 消息只承载形状

    def test_delete_returns_false_on_44(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
        # 通道可用性是被测前提不是被测对象:非 mac 宿主(CI Linux)也必须能验子进程形状
        monkeypatch.setattr(keychain, "keychain_available", lambda: True)

        def fake_run(argv, **kwargs):  # noqa: ANN001, ANN202
            return subprocess.CompletedProcess(argv, 44, "", "")

        monkeypatch.setattr(keychain.subprocess, "run", fake_run)
        assert keychain.delete_item("myia/wechat/db-keys") is False

    def test_write_rejects_newline_in_value(self) -> None:
        with pytest.raises(BridgeError):
            keychain.write_item("myia/wechat/db-keys", "line1\nline2")

    def test_write_rejects_non_ascii_value(self) -> None:
        """-i 解析器不认非 ASCII(实测 mojibake)→ 拒写,不写坏值。"""
        with pytest.raises(BridgeError):
            keychain.write_item("myia/wechat/db-keys", "passphrase-中文")

    def test_envelope_is_ascii_even_with_nonascii_db_names(self) -> None:
        """非 ASCII 库名在 JSON 层转义:外壳恒 ASCII(-i 通道硬前提),parse 无损还原。"""
        mapping = {"消息/库.db": "00" * 32}
        raw = keychain.build_db_keys_envelope(mapping, migrated_at="2026-10-14T00:00:00+08:00")
        assert raw.isascii() and "\n" not in raw
        got, _stamp = keychain.parse_db_keys_envelope(raw)
        assert got == mapping

    def test_envelope_roundtrip_compact_single_line(self) -> None:
        mapping = {"a/b.db": "00" * 32, "c/d.db": "ff" * 32}
        raw = keychain.build_db_keys_envelope(mapping, migrated_at="2026-10-14T00:00:00+08:00")
        assert "\n" not in raw  # stdin 双行供给形态的前提
        got, stamp = keychain.parse_db_keys_envelope(raw)
        assert got == mapping
        assert stamp == "2026-10-14T00:00:00+08:00"

    def test_parse_legacy_raw_mapping(self) -> None:
        """裸 {rel: hex} 形态防御性兼容(手工放置;migrated_at = None 如实)。"""
        raw = json.dumps({"message/message_0.db": "00" * 32})
        got, stamp = keychain.parse_db_keys_envelope(raw)
        assert got == {"message/message_0.db": "00" * 32}
        assert stamp is None

    def test_parse_bad_shapes_return_none(self) -> None:
        for raw in ("{not json", "[]", "{}", '{"keys": "notdict", "migrated_at": "x"}', "null"):
            assert keychain.parse_db_keys_envelope(raw) == (None, None)
