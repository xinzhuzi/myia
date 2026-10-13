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

    def test_ttl_zero_keeps_stale_copy_forever(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """TTL=0 = 永不过期:陈旧副本恒新鲜、跳过重建(2026-10-13 审计
        修复——用户直觉「0=永不过期」;config 装载面 0 合法见 test_config)。"""
        kwargs = dict(
            domains=["session"], ttl_hours=0, capacity_mb=512, **_copy_kwargs(tmp_path)
        )
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        plain = copy_dir(data_root=tmp_path / "home") / "session" / "session.db"
        # 人为把副本 mtime 拨回一年前:仍 kept,不重建。
        ancient = time.time() - 365 * 24 * 3600
        os.utime(plain, (ancient, ancient))
        info = ensure_decrypted_copies(fake_storage, keys, now=time.time(), **kwargs)
        assert info["kept"] == ["session/session.db"]
        assert info["built"] == []

    def test_source_db_newer_rebuilds_within_ttl(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """0.4.4 源新即重建:TTL 内、但源库 mtime 比副本新(微信又写了)
        → 缓存失效重建——近实时监控的正确性前提(10-13 实况:副本 11:47
        恒「新鲜」到次日,下午消息全盲区)。"""
        kwargs = dict(domains=["session"], ttl_hours=24, capacity_mb=512, **_copy_kwargs(tmp_path))
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        future = time.time() + 120
        os.utime(fake_storage / "session" / "session.db", (future, future))
        info = ensure_decrypted_copies(fake_storage, keys, now=time.time(), **kwargs)
        assert info["built"] == ["session/session.db"]
        assert info["kept"] == []

    def test_source_wal_newer_rebuilds(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """仅 ``-wal`` 比副本新(消息还在 WAL 未 checkpoint)也要重建;
        空 wal(零帧)不损坏解密,staging 拷贝链照常。"""
        kwargs = dict(domains=["session"], ttl_hours=24, capacity_mb=512, **_copy_kwargs(tmp_path))
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        wal = fake_storage / "session" / "session.db-wal"
        wal.write_bytes(b"")  # 零帧 wal:sqlite 语义合法
        future = time.time() + 120
        os.utime(wal, (future, future))
        info = ensure_decrypted_copies(fake_storage, keys, now=time.time(), **kwargs)
        assert info["built"] == ["session/session.db"]
        plain = copy_dir(data_root=tmp_path / "home") / "session" / "session.db"
        con = sqlite3.connect(f"file:{plain}?mode=ro", uri=True)
        (count,) = con.execute("SELECT COUNT(*) FROM t").fetchone()
        con.close()
        assert count == 3

    def test_ttl_zero_ignores_source_newer(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """TTL=0 关闸语义完整:源新也不重建(显式永不刷新模式)。"""
        kwargs = dict(
            domains=["session"], ttl_hours=0, capacity_mb=512, **_copy_kwargs(tmp_path)
        )
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        future = time.time() + 120
        os.utime(fake_storage / "session" / "session.db", (future, future))
        info = ensure_decrypted_copies(fake_storage, keys, now=time.time(), **kwargs)
        assert info["kept"] == ["session/session.db"]
        assert info["built"] == []

    def test_source_missing_keeps_existing_copy(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """源消失(账号目录迁走等极端):不炸整轮;rel 不进 domain_targets
        (上游按存在性过滤),既有副本原样留盘供 E3 查询。"""
        kwargs = dict(domains=["session"], ttl_hours=24, capacity_mb=512, **_copy_kwargs(tmp_path))
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        plain = copy_dir(data_root=tmp_path / "home") / "session" / "session.db"
        assert plain.is_file()
        (fake_storage / "session" / "session.db").unlink()
        info = ensure_decrypted_copies(fake_storage, keys, now=time.time(), **kwargs)
        assert info["built"] == [] and info["skipped"] == []
        assert plain.is_file()  # 副本未被清除/未触发崩溃

    def test_rebuild_retries_once_on_transient_decrypt_failure(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """0.4.4 活库拷贝竞态重试:第一次解密失败(注入模拟 db+wal 不一致
        对)→ 原样重拷重试一次成功;不把竞态瞬态冒成源失败。"""
        kwargs = dict(domains=["session"], ttl_hours=24, capacity_mb=512, **_copy_kwargs(tmp_path))
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        future = time.time() + 120
        os.utime(fake_storage / "session" / "session.db", (future, future))
        calls = {"n": 0}

        def flaky_runner(enc: Path, plain: Path, key: str) -> None:
            calls["n"] += 1
            if calls["n"] == 1:
                raise BridgeError(DECRYPT_FAILED, "竞态模拟:第一次失败")
            from wechat_bridge.localdb import _run_sqlcipher_decrypt

            _run_sqlcipher_decrypt(enc, plain, key)

        info = ensure_decrypted_copies(fake_storage, keys, runner=flaky_runner, **kwargs)
        assert info["built"] == ["session/session.db"]
        assert calls["n"] == 2
        plain = copy_dir(data_root=tmp_path / "home") / "session" / "session.db"
        con = sqlite3.connect(f"file:{plain}?mode=ro", uri=True)
        (count,) = con.execute("SELECT COUNT(*) FROM t").fetchone()
        con.close()
        assert count == 3

    def test_concurrent_ensure_single_flight(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """0.4.4 并发单飞:两个线程(独立 fd,flock 跨 open 生效)并发
        ensure 同一数据根——重建只发生一次,后来者锁内重估新鲜度直接复用;
        staging 不再被同名 .enc 交叉覆盖(实测每轮恰一源 decrypt_failed
        的根因)。"""
        import threading

        kwargs = dict(domains=["session"], ttl_hours=24, capacity_mb=512, **_copy_kwargs(tmp_path))
        keys = {"session/session.db": TEST_KEY}
        calls = {"n": 0}
        guard = threading.Lock()

        def counting_runner(enc: Path, plain: Path, key: str) -> None:
            with guard:
                calls["n"] += 1
            time.sleep(0.3)  # 放大交错窗:无锁时两线程都会进来
            from wechat_bridge.localdb import _run_sqlcipher_decrypt

            _run_sqlcipher_decrypt(enc, plain, key)

        results: list[dict[str, object]] = []

        def worker() -> None:
            results.append(
                ensure_decrypted_copies(fake_storage, keys, runner=counting_runner, **kwargs)
            )

        t1 = threading.Thread(target=worker)
        t2 = threading.Thread(target=worker)
        t1.start()
        t2.start()
        t1.join(timeout=60)
        t2.join(timeout=60)
        assert calls["n"] == 1  # 单飞:并发下只重建一次
        built_or_kept = sorted(
            str(r["built"] or r["kept"]) for r in results  # type: ignore[arg-type]
        )
        assert built_or_kept == ["['session/session.db']", "['session/session.db']"]

    def test_rebuild_gives_up_after_two_failures(
        self, tmp_path: Path, fake_storage: Path
    ) -> None:
        """两连败(真键错/真损坏)照实抛,不无限重试。"""
        kwargs = dict(domains=["session"], ttl_hours=24, capacity_mb=512, **_copy_kwargs(tmp_path))
        keys = {"session/session.db": TEST_KEY}
        ensure_decrypted_copies(fake_storage, keys, **kwargs)
        future = time.time() + 120
        os.utime(fake_storage / "session" / "session.db", (future, future))
        calls = {"n": 0}

        def always_fail(enc: Path, plain: Path, key: str) -> None:
            calls["n"] += 1
            raise BridgeError(DECRYPT_FAILED, "两次都失败")

        with pytest.raises(BridgeError) as excinfo:
            ensure_decrypted_copies(fake_storage, keys, runner=always_fail, **kwargs)
        assert excinfo.value.exit_code == DECRYPT_FAILED
        assert calls["n"] == 2

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
