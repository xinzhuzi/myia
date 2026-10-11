"""TG 网页线配置档本地备份(10-11-tg-manage-absorb AC3)—— 登录成功收尾
的 tar.gz 整档打包 + 滚动保留。

登录态 = 配置档文件(cookies/localStorage),Chromium 配置档损坏(磁盘/
升级事故)会让整条 web 线失效且不可重建(重登要人输验证码)。本模块在
**登录成功收尾**挂一次整档备份(:meth:`TelegramWebLoginFlow.run` 的
``_write_login_marker`` 之后):此刻 context 已关、权限已硬化、标记已落,
打包时 Playwright 零写者 —— CLI web-login 与桌面 browser.open 线程共用
同一登录流,挂一处全覆盖。

诚实边界(回执披露同步):本地损坏可回滚(删档 → 解包恢复);**服务端
吊销不救**(TG 侧踢会话后 cookie 失效,备份里的登录态同样失效)。

并发相处:同键体检探针在跑时跳过本次备份留痕(探针中的档是旧登录态,
备份无意义,下次登录再备)—— 探针登记面 = web_line ``_ACTIVE_PROBES``
(进程内;批量采集是独立进程短时占用,无法感知,不在此兜底)。
"""

from __future__ import annotations

import contextlib
import logging
import os
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from myssia.telegram import web_line
from myssia.telegram.web_line import (
    PROFILE_DIR_MODE,
    PROFILE_FILE_MODE,
    profile_dir,
    profile_root,
    validate_account_key,
)

logger = logging.getLogger(__name__)

#: 备份目录名(配置档根下;名字不匹配 ACCOUNT_KEY_RE(^telegram- 前缀),
#: list_accounts 天然跳过,不冒充账号行 —— 已核 web_line 键规约)。
BACKUP_DIR_NAME = "backups"

#: 滚动保留份数(登录收尾频率低,3 份足够覆盖最近两次误操作)。
BACKUP_KEEP = 3

__all__ = [
    "BACKUP_DIR_NAME",
    "BACKUP_KEEP",
    "backup_profile",
]


def backup_profile(data_root: str | Path, account: str) -> Path | None:
    """整档打包配置档到 ``telegram-web/backups/<键>-<UTC 时间戳>.tar.gz``.

    Returns:
        备份文件路径;**一切失败只留痕不抛**(登录成功不被备份失败拦 ——
        ``_write_login_marker`` 的 OSError 判例),返回 None。标记返回前
        已做:同键探针在跑跳过(数据一致性)、滚动删最旧至剩 3 份。

    权限纪律:备份含登录态(凭据面)—— 目录 0700、文件 0600(tmp 先
    chmod 再 ``os.replace``,最终态即 0600;原子判例 gates/offsets)。
    """
    key = validate_account_key(account)
    directory = profile_dir(data_root, key)
    if not directory.is_dir():  # pragma: no cover - 登录收尾调用点目录必在,防御
        logger.warning(
            "TG 网页线配置档备份跳过(配置档缺)path=%s", directory
        )
        return None
    with web_line._ACTIVE_PROBES_LOCK:  # noqa: SLF001 - 同包探针登记面(跳过判据)
        if str(directory) in web_line._ACTIVE_PROBES:  # noqa: SLF001
            logger.info(
                "TG 网页线配置档备份跳过(账号 %s 体检探针在跑,旧登录态"
                "备份无意义;下次登录再备)",
                key,
            )
            return None
    backups = profile_root(data_root) / BACKUP_DIR_NAME
    try:
        backups.mkdir(parents=True, exist_ok=True)
        backups.chmod(PROFILE_DIR_MODE)
    except OSError as exc:  # 目录就位失败 = 后续必失败,早退留痕
        logger.warning(
            "TG 网页线备份目录就位失败(忽略)path=%s: %s", backups, exc
        )
        return None
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target = backups / f"{key}-{stamp}.tar.gz"
    tmp = target.with_name(target.name + ".tmp")
    try:
        with tarfile.open(tmp, "w:gz") as tar:
            tar.add(directory, arcname=key)
        tmp.chmod(PROFILE_FILE_MODE)
        os.replace(tmp, target)
    except Exception as exc:  # noqa: BLE001 - 备份失败不拦登录成功(AC3)
        logger.warning(
            "TG 网页线配置档备份失败(忽略;登录态已落配置档不受影响)"
            " target=%s: %s",
            target,
            exc,
        )
        with contextlib.suppress(OSError):
            tmp.unlink(missing_ok=True)
        return None
    _prune_backups(backups, key)
    logger.info(
        "TG 网页线配置档已备份(%s 滚动留 %d 份)path=%s",
        key,
        BACKUP_KEEP,
        target,
    )
    return target


def _prune_backups(backups: Path, key: str) -> None:
    """滚动保留:同前缀 ``<键>-*.tar.gz`` 删最旧至剩 :data:`BACKUP_KEEP` 份.

    文件名 UTC 时间戳(``YYYYmmddTHHMM%SZ``)字典序 = 时间序,sorted()
    即新到旧的稳定序;删失败只留痕(下此登录再补删)。
    """
    try:
        mine = sorted(
            path for path in backups.glob(f"{key}-*.tar.gz") if path.is_file()
        )
    except OSError as exc:  # pragma: no cover - glob 极少失败,防御面
        logger.warning("TG 网页线备份清点失败(忽略)path=%s: %s", backups, exc)
        return
    for old in mine[:-BACKUP_KEEP] if len(mine) > BACKUP_KEEP else []:
        try:
            old.unlink()
        except OSError as exc:
            logger.warning(
                "TG 网页线旧备份删除失败(忽略;下次登录再补删)path=%s: %s",
                old,
                exc,
            )
