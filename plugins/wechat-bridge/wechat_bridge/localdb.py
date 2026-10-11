"""本地库只读通道骨架(task 10-11-wechat-ui-bridge Phase E 落点位)。

当前可真跑的部分(全部纯文件系统只读,零微信进程交互、零出网):

- :func:`locate_db_storage` —— 定位已登录账号的 ``db_storage/`` 目录
  (prd Notes 实测布局:``~/Library/Containers/com.tencent.xinWeChat/
  Data/Documents/xwechat_files/<wxid+设备后缀>/db_storage/``);找不到 →
  §6 exit 20 ``db_not_found``。**只看目录形状,不进库、不读内容**。

待裁决/待落地部分(骨架态如实应答,不谎报):

- 密钥获取(E1)= **D4 开放决策**(prd:零内存方案可用则用;内存密钥搜索
  为降级候选,启用前须主人裁决)。骨架态 :func:`acquire_key` 恒应答
  §6 exit 21 ``key_unavailable`` + D4 指引——这是「桥此刻拿不到密钥」的
  如实陈述,不是「密钥不存在」的结论(A3 探查归 Phase A)。
- 解密副本(E2,G5 TTL/容量)与三域查询(E3,G4)在本模块占位。

红线备忘(实现时生效,先立在此处):

- 内存密钥搜索若经 D4 豁免:**独立模块 + 开关默认关**,主人显式开启才
  生效(design §4);本骨架不含该模块,也**禁止真跑**。
- 解密副本落 MYIA 数据根私有区(600 权限),TTL 24h + 容量上限,解密
  失败触发重建;副本与查询结果不入 git/日志/上下文原文(prd 红线 6)。
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from .codes import DB_NOT_FOUND, KEY_UNAVAILABLE, BridgeError
from .system_checks import WECHAT_FILES_ROOT

__all__ = ["locate_db_storage", "acquire_key", "query_history"]

#: 单账号本地库目录名(db_storage;research §7.1 实测)。
DB_STORAGE_DIR_NAME = "db_storage"


def locate_db_storage(
    *,
    files_root: Path | None = None,
    account_picker: Callable[[list[Path]], Path] | None = None,
) -> Path:
    """定位已登录账号的 ``db_storage/`` 目录(纯只读;多账号时取最新)。

    多账号目录 = 带 ``db_storage/`` 的直接子目录;骨架态取 mtime 最新一个
    (「当前已登录账号」的零交互近似——prd R4:桥只操作当前已登录账号,
    不做账号管理)。真账号判定归 Phase E(登录态元数据)。

    Raises:
        BridgeError: exit 20 ``db_not_found``(数据根缺位 / 无账号目录)。
    """
    root = files_root if files_root is not None else WECHAT_FILES_ROOT
    if not root.is_dir():
        raise BridgeError(
            DB_NOT_FOUND,
            f"微信本地库数据根不存在: {root}",
            fix_hint="确认微信曾在本机登录并产生本地数据;桥不做登录流程(prd R4)",
        )
    candidates = [
        child
        for child in root.iterdir()
        if child.is_dir() and (child / DB_STORAGE_DIR_NAME).is_dir()
    ]
    if not candidates:
        raise BridgeError(
            DB_NOT_FOUND,
            f"数据根在场但无带 {DB_STORAGE_DIR_NAME}/ 的账号目录: {root}",
            fix_hint="确认微信在本机登录过;多账号场景等待 Phase E 的登录态判定",
        )
    if account_picker is not None:
        return account_picker(candidates) / DB_STORAGE_DIR_NAME
    latest = max(candidates, key=lambda item: item.stat().st_mtime)
    return latest / DB_STORAGE_DIR_NAME


def acquire_key(db_storage: Path) -> bytes:
    """密钥获取实现位(Phase E1;途径按 A4/D4 裁决)。

    骨架态恒应答 §6 exit 21 ``key_unavailable``——D4 未裁决,桥此刻确实
    拿不到密钥;**绝不伪造密钥材料,绝不触发任何内存搜索路径**。
    """
    raise BridgeError(
        KEY_UNAVAILABLE,
        "本地库密钥不可得:密钥途径(D4)未裁决,骨架态无获取实现",
        fix_hint=(
            "等待 Phase A3/A4 零内存方案探查结论与主人 D4 裁决;"
            "内存密钥搜索为降级候选,默认关、启用须主人裁决(prd 红线 1)"
        ),
    )


def query_history(chat_id: str, since_days: int) -> dict[str, object]:
    """``localdb query`` 实现位(Phase E2/E3:副本 → 三域只读查询)。"""
    raise BridgeError(
        KEY_UNAVAILABLE,
        "本地库查询不可用:密钥途径(D4)未裁决,解密副本(Phase E2)未落地",
        fix_hint="等待 D4 裁决与 Phase E 落地;域清单/副本 TTL 见桥配置(design §7)",
    )


# 静态对账:本地库族码值与 codes 表一致(改码先改 design §6)。
assert DB_NOT_FOUND == 20 and KEY_UNAVAILABLE == 21

#: 数据根私有区里本地库通道的落点前缀(副本/查询产物;design §1/§2)。
LOCALDB_PRIVATE_DIR = "wechat-localdb"
