"""E2 解密副本单测(sqlcipher 在场门控 + 生命周期:G5 TTL/容量/失败重建)。

真 sqlcipher 环节用**测试自造的加密库**(raw key 由测试生成,非任何真实
微信材料);sqlcipher 缺席(CI)整类跳过——design §8 环境门控纪律。
"""

from __future__ import annotations

import os
import sqlite3
import subprocess
import time
from pathlib import Path

import pytest

from wechat_bridge.codes import DECRYPT_FAILED, BridgeError
from wechat_bridge.localdb import (
    copy_dir,
    domain_targets,
    ensure_decrypted_copies,
    sqlcipher_available,
)

pytestmark = pytest.mark.skipif(
    not sqlcipher_available(), reason="sqlcipher CLI 缺席(CI):解密链测试跳过"
)

TEST_KEY = bytes(range(32)).hex()


def _make_encrypted_db(path: Path, key_hex: str = TEST_KEY, rows: int = 3) -> Path:
    """sqlcipher 自造加密库(raw key;内容全合成)。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    sql = (
        f'PRAGMA key = "x\'{key_hex}\'";\n'
        "CREATE TABLE t(id INTEGER PRIMARY KEY, note TEXT);\n"
        + "".join(f"INSERT INTO t(note) VALUES ('row-{i}');\n" for i in range(rows))
    )
    result = subprocess.run(  # noqa: S603 - 字面量命令
        ["sqlcipher", path.as_posix()],
        input=sql.encode(),
        capture_output=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, f"造加密库失败: {result.stderr[:200]}"
    assert path.is_file() and path.stat().st_size > 0
    return path


@pytest.fixture()
def fake_storage(tmp_path: Path) -> Path:
    """合成 db_storage:session/session.db 为测试加密库。"""
    storage = tmp_path / "wxid_x_1" / "db_storage"
    _make_encrypted_db(storage / "session" / "session.db")
    return storage


def _copy_kwargs(tmp_path: Path) -> dict:
    return {"data_root": tmp_path / "home"}


class TestDecryptRoundtrip:
    def test_decrypt_produces_readable_sqlite_600(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        info = ensure_decrypted_copies(
            fake_storage,
            {"session/session.db": TEST_KEY},
            domains=["session"],
            ttl_hours=24,
            capacity_mb=512,
            **_copy_kwargs(tmp_path),
        )
        assert info["built"] == ["session/session.db"]
        assert info["skipped"] == []
        plain = copy_dir(data_root=tmp_path / "home") / "session" / "session.db"
        assert (plain.stat().st_mode & 0o777) == 0o600
        con = sqlite3.connect(f"file:{plain}?mode=ro", uri=True)
        (count,) = con.execute("SELECT COUNT(*) FROM t").fetchone()
        con.close()
        assert count == 3
        # 私有区目录 700(红线 6)。
        assert (copy_dir(data_root=tmp_path / "home").stat().st_mode & 0o777) == 0o700

    def test_ttl_keeps_fresh_and_rebuilds_stale(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        kwargs = dict(domains=["session"], ttl_hours=24, capacity_mb=512, **_copy_kwargs(tmp_path))
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        plain = copy_dir(data_root=tmp_path / "home") / "session" / "session.db"
        # 新鲜 → kept(不重建)
        info = ensure_decrypted_copies(fake_storage, keys, now=time.time(), **kwargs)
        assert info["kept"] == ["session/session.db"] and info["built"] == []
        # 过期(TTL+2h)→ 重建
        stale = time.time() - 26 * 3600
        os.utime(plain, (stale, stale))
        info = ensure_decrypted_copies(fake_storage, keys, now=time.time(), **kwargs)
        assert info["built"] == ["session/session.db"] and info["kept"] == []

    def test_capacity_skips_and_records(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        source_size = (fake_storage / "session" / "session.db").stat().st_size
        tiny_cap = max(0, source_size // (1024 * 1024))  # MB 取整 → 0MB 必跳
        info = ensure_decrypted_copies(
            fake_storage,
            {"session/session.db": TEST_KEY},
            domains=["session"],
            ttl_hours=24,
            capacity_mb=tiny_cap,
            **_copy_kwargs(tmp_path),
        )
        assert info["built"] == []
        assert info["skipped"] == [{"rel": "session/session.db", "reason": "capacity"}]

    def test_no_key_skips(self, tmp_path: Path, fake_storage: Path) -> None:
        info = ensure_decrypted_copies(
            fake_storage,
            {},
            domains=["session"],
            ttl_hours=24,
            capacity_mb=512,
            **_copy_kwargs(tmp_path),
        )
        assert info["skipped"] == [{"rel": "session/session.db", "reason": "no_key"}]

    def test_wrong_key_is_decrypt_failed_22(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        with pytest.raises(BridgeError) as excinfo:
            ensure_decrypted_copies(
                fake_storage,
                {"session/session.db": "ab" * 32},
                domains=["session"],
                ttl_hours=24,
                capacity_mb=512,
                **_copy_kwargs(tmp_path),
            )
        err = excinfo.value
        assert err.exit_code == DECRYPT_FAILED == 22
        assert "解密失败" in str(err) or "sqlcipher 解密失败" in str(err)

    def test_staging_cleaned_after_run(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        ensure_decrypted_copies(
            fake_storage,
            {"session/session.db": TEST_KEY},
            domains=["session"],
            ttl_hours=24,
            capacity_mb=512,
            **_copy_kwargs(tmp_path),
        )
        staging = copy_dir(data_root=tmp_path / "home") / ".staging"
        assert not staging.exists() or not any(staging.iterdir())


class TestDomainTargets:
    def test_known_domain_mapping(self, fake_storage: Path) -> None:
        targets = domain_targets(["session"], fake_storage)
        assert targets == [("session/session.db", (fake_storage / "session" / "session.db").stat().st_size)]

    def test_unknown_domain_falls_back_to_dir_scan(self, fake_storage: Path) -> None:
        targets = domain_targets(["custom"], fake_storage)
        assert targets == []  # custom/ 目录不存在 → 如实空

    def test_missing_file_in_mapping_skipped(self, tmp_path: Path) -> None:
        storage = tmp_path / "s" / "db_storage"
        (storage / "session").mkdir(parents=True)
        assert domain_targets(["session"], storage) == []


class TestSqlcipherGuard:
    def test_missing_binary_is_22_with_brew_hint(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """sqlcipher 缺位(FileNotFoundError)→ exit 22 + brew 指引(design §5.1
        不静默半装;本机已装 sqlcipher,以注入方式模拟缺位)。"""
        import wechat_bridge.localdb as ld

        # 先用真 sqlcipher 造库,再注入缺位(注入是全局的,顺序不能反)。
        enc = _make_encrypted_db(tmp_path / "enc.db")
        plain = tmp_path / "out.db"

        def raise_missing(*args: object, **kwargs: object) -> None:
            raise FileNotFoundError(2, "No such file or directory", "sqlcipher")

        monkeypatch.setattr(ld.subprocess, "run", raise_missing)
        with pytest.raises(BridgeError) as excinfo:
            ld._run_sqlcipher_decrypt(enc, plain, TEST_KEY)
        err = excinfo.value
        assert err.exit_code == 22
        assert "brew install sqlcipher" in (err.fix_hint or "")
