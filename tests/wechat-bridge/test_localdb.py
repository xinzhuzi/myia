"""本地库通道骨架单测:定位真跑(纯目录形状),密钥骨架态如实 21。"""

from __future__ import annotations

from pathlib import Path

import pytest

from wechat_bridge.codes import KEY_UNAVAILABLE, BridgeError
from wechat_bridge.localdb import acquire_key, locate_db_storage


def _make_account(root: Path, name: str = "wxid_demo_8253") -> Path:
    account = root / name
    (account / "db_storage" / "message").mkdir(parents=True)
    return account


class TestLocate:
    def test_locates_latest_account(self, tmp_path: Path) -> None:
        first = _make_account(tmp_path, "wxid_a_1111")
        second = _make_account(tmp_path, "wxid_b_2222")
        import os

        os.utime(first, (1000, 1000))
        os.utime(second, (2000, 2000))
        located = locate_db_storage(files_root=tmp_path)
        assert located == second / "db_storage"

    def test_account_picker_overrides_mtime_choice(self, tmp_path: Path) -> None:
        _make_account(tmp_path, "wxid_a_1111")
        chosen = _make_account(tmp_path, "wxid_b_2222")
        located = locate_db_storage(
            files_root=tmp_path, account_picker=lambda _: chosen
        )
        assert located == chosen / "db_storage"

    def test_missing_root_is_db_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(BridgeError) as excinfo:
            locate_db_storage(files_root=tmp_path / "absent")
        assert excinfo.value.exit_code == 20
        assert excinfo.value.name == "db_not_found"

    def test_root_without_accounts_is_db_not_found(self, tmp_path: Path) -> None:
        (tmp_path / "Backup").mkdir()  # 非账号目录(无 db_storage)
        with pytest.raises(BridgeError) as excinfo:
            locate_db_storage(files_root=tmp_path)
        assert excinfo.value.exit_code == 20

    def test_locate_reads_no_file_content(self, tmp_path: Path) -> None:
        """定位只看目录形状;库文件不被打开(红线 6:证据只留形状)。"""
        account = _make_account(tmp_path)
        db_file = account / "db_storage" / "message" / "msg_0.db"
        db_file.write_bytes(b"not-a-real-db")
        located = locate_db_storage(files_root=tmp_path)
        assert located.is_dir()
        assert located.name == "db_storage"


class TestKeySkeleton:
    def test_acquire_key_is_honest_key_unavailable(self, tmp_path: Path) -> None:
        """骨架态:密钥途径待 D4 → exit 21 + 指引(不伪造、不试内存搜索)。"""
        account = _make_account(tmp_path)
        with pytest.raises(BridgeError) as excinfo:
            acquire_key(account / "db_storage")
        err = excinfo.value
        assert err.exit_code == KEY_UNAVAILABLE == 21
        assert err.name == "key_unavailable"
        assert "D4" in (err.fix_hint or "")
