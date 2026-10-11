"""AC3: TG 网页线配置档本地备份(10-11-tg-manage-absorb)—— 全零网络零浏览器.

覆盖:整档打包落盘与权限纪律(0600/0700)/滚动保留 3 份/登录收尾挂钩
(登录成功即备份)/失败不拦登录(备份炸 → run 仍成功)/回执披露⑤在场。
"""

from __future__ import annotations

import tarfile
from pathlib import Path
from typing import Any

import pytest

from myssia.telegram.web_backup import (
    BACKUP_DIR_NAME,
    BACKUP_KEEP,
    backup_profile,
)
from myssia.telegram.web_line import (
    PROFILE_DIR_MODE,
    PROFILE_FILE_MODE,
    PROFILE_ROOT_DIR,
    TelegramWebLoginFlow,
    login_marker_path,
    profile_dir,
    profile_root,
)


def _seed_profile(tmp_path: Path, key: str = "telegram-alt1") -> Path:
    """预置假档(登录态面:标记 + cookies),返回配置档目录."""
    directory = profile_dir(tmp_path, key)
    sub = directory / "Default"
    sub.mkdir(parents=True)
    (sub / "Cookies").write_text("{}", encoding="utf-8")
    login_marker_path(directory).write_text(
        '{"logged_in_at": "2026-10-11T00:00:00+00:00", "line": "tg_web"}',
        encoding="utf-8",
    )
    return directory


# --------------------------------------------------------------- 落盘


def test_backup_profile_writes_gz_with_permissions(tmp_path: Path) -> None:
    """整档打包:backups/ 下恰一个 <键>-*.tar.gz;0600/0700 权限纪律;
    tar 可开且成员含标记文件(登录态 = 凭据面)。"""
    directory = _seed_profile(tmp_path)
    result = backup_profile(tmp_path, "telegram-alt1")
    backups = profile_root(tmp_path) / BACKUP_DIR_NAME
    assert result is not None and result.parent == backups
    archives = list(backups.glob("telegram-alt1-*.tar.gz"))
    assert len(archives) == 1 and archives[0] == result
    assert (result.stat().st_mode & 0o777) == PROFILE_FILE_MODE
    assert (backups.stat().st_mode & 0o777) == PROFILE_DIR_MODE
    assert not list(backups.glob("*.tmp")), "原子写不得留 .tmp 残件"
    with tarfile.open(result, "r:gz") as tar:
        names = tar.getnames()
    assert any(name.endswith("myssia-login.json") for name in names)
    assert any(name.endswith("Cookies") for name in names)
    # backups 目录名不匹配 ACCOUNT_KEY_RE:list_accounts 不冒充账号行(已核
    # 键规约,此处守回归)
    from myssia.telegram.web_line import list_accounts

    assert list_accounts(tmp_path) == ["telegram-alt1"]


def test_backup_profile_rolls_to_keep_three(tmp_path: Path) -> None:
    """滚动保留:预置 3 个同前缀旧备份(时间戳递增)+ 新备份 → 最旧删、
    恰剩 3(UTC 时间戳字典序 = 时间序)。"""
    _seed_profile(tmp_path)
    backups = profile_root(tmp_path) / BACKUP_DIR_NAME
    backups.mkdir(parents=True)
    for stamp in ("20260101T000000Z", "20260102T000000Z", "20260103T000000Z"):
        (backups / f"telegram-alt1-{stamp}.tar.gz").write_bytes(b"old")
    result = backup_profile(tmp_path, "telegram-alt1")
    assert result is not None
    remaining = sorted(path.name for path in backups.glob("telegram-alt1-*.tar.gz"))
    assert len(remaining) == BACKUP_KEEP
    assert "telegram-alt1-20260101T000000Z.tar.gz" not in remaining  # 最旧删
    assert result.name in remaining


# ----------------------------------------------------------- 登录挂钩


def test_login_flow_hooks_backup_at_tail(tmp_path: Path) -> None:
    """登录成功收尾自动备份:flow.run(states=[logged_in])→ 目录返回 +
    backups/ 出现档(此点 context 已关/标记已落,Playwright 零写者)。"""
    import asyncio

    from tests.telegram.test_web_line import make_factory

    factory, _, _, _ = make_factory([{"state": "logged_in", "hit": ".chatlist-container"}])
    flow = TelegramWebLoginFlow(print_fn=lambda _: None, playwright_factory=factory)
    directory = asyncio.run(flow.run(tmp_path, "telegram-alt1"))
    assert directory == profile_dir(tmp_path, "telegram-alt1")
    backups = profile_root(tmp_path) / BACKUP_DIR_NAME
    assert len(list(backups.glob("telegram-alt1-*.tar.gz"))) == 1


def test_backup_failure_does_not_block_login(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """失败不拦例:tarfile.open 抛 OSError → flow.run 仍成功返回目录,
    无异常上浮(登录成功不被备份失败拦)。"""
    import asyncio

    from tests.telegram.test_web_line import make_factory

    def refuse_open(*args: Any, **kw: Any) -> Any:
        raise OSError("no space left on device")

    monkeypatch.setattr(tarfile, "open", refuse_open)
    factory, _, _, _ = make_factory([{"state": "logged_in", "hit": ".chatlist-container"}])
    flow = TelegramWebLoginFlow(print_fn=lambda _: None, playwright_factory=factory)
    directory = asyncio.run(flow.run(tmp_path, "telegram-alt1"))
    assert directory.is_dir()
    backups = profile_root(tmp_path) / BACKUP_DIR_NAME
    assert list(backups.glob("telegram-alt1-*.tar.gz")) == []  # 零残档


def test_backup_skipped_while_probe_running(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """并发相处:同键体检探针在跑(web_line._ACTIVE_PROBES 登记)→ 跳过
    本次备份留痕返回 None(探针中的档是旧登录态,备份无意义)。"""
    import myssia.telegram.web_line as web_line

    directory = _seed_profile(tmp_path)
    monkeypatch.setattr(
        web_line, "_ACTIVE_PROBES", {str(directory)}
    )
    # web_backup 按模块属性读 registry,直接换模块引用后的集合
    result = backup_profile(tmp_path, "telegram-alt1")
    assert result is None
    backups = profile_root(tmp_path) / BACKUP_DIR_NAME
    assert not backups.exists() or list(backups.glob("*.tar.gz")) == []


def test_login_receipt_disclosure_mentions_backup(tmp_path: Path) -> None:
    """回执文案例:成功回执披露⑤在场(含 backups 与「服务端吊销不救」
    —— 诚实边界:本地损坏可回滚,服务端吊销不救)。"""
    import asyncio

    from tests.telegram.test_web_line import make_factory

    factory, _, _, _ = make_factory([{"state": "logged_in", "hit": ".chatlist-container"}])
    lines: list[str] = []
    flow = TelegramWebLoginFlow(print_fn=lines.append, playwright_factory=factory)
    asyncio.run(flow.run(tmp_path, "telegram-alt1"))
    receipt = "\n".join(lines)
    assert "backups" in receipt
    assert "服务端吊销不救" in receipt


def test_backup_profile_invalid_account_structured(tmp_path: Path) -> None:
    """键同门校验:违全称律 → TelegramWebError(invalid_account)。"""
    from myssia.telegram.web_line import TelegramWebError

    with pytest.raises(TelegramWebError) as exc_info:
        backup_profile(tmp_path, "bad-key")
    assert exc_info.value.reason == "invalid_account"


# 模块常量与配置档根的关系(防 BACKUP_DIR_NAME 漂移到别的根)
def test_backup_dir_lives_under_profile_root(tmp_path: Path) -> None:
    _seed_profile(tmp_path)
    result = backup_profile(tmp_path, "telegram-alt1")
    assert result is not None
    assert result.parent.parent == tmp_path / PROFILE_ROOT_DIR
