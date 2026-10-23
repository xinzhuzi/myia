"""本地库只读通道(task 10-11-wechat-ui-bridge Phase E1/E2)。

E1 零内存密钥途径的**真实现 + 如实负结论**(2026-10-11 E1 真跑):

- 途径 = ``all_users/login/<wxid>/key_info.db``(明文 SQLite,A3 实测)→
  解码 ``key_info_data`` BLOB(180B protobuf:f1=168B 包裹物/f2=版本常数/
  f3=写入时间戳,``md5(blob)==key_info_md5`` 完整性关系实测成立)→
  候选 32B key(滑窗/字段/sha256 派生)→ 对 ``db_storage`` 各库 page1 做
  离线 HMAC-SHA512 校验(SQLCipher 4 原始密钥语义,stdlib 实现)。
- **真跑结论 = 不可行**:本机 35 行 × 全候选族 × 20 库 page1,209,300 次
  校验 0 命中;与三方独立公开实测一致(4995 种派生 / 15,987 候选 × 51 库 /
  12,058 窗口,均零命中;0xlane 逆向结论:key_info_data 是**登录 key**
  (每次登录变),不是**数据库 key**,被机器专属密钥包裹、文件内不可推导)。
  故 :func:`acquire_key` 如实应答 §6 exit 21 ``key_unavailable`` + D4 裁决
  指引——**骨架语义已被真跑证据替换,不是占位**。校验机制本身完整可用
  (单测以合成 page1 全链验证),D4 裁决②的外部密钥消费通路已闭合:
  :func:`resolve_keys` 先重验 ``keys.json``(缓存/外部同位,数据根私有区
  600)再回落零内存途径,主人放置密钥产物后查询一步闭合。
- 内存密钥搜索(prd 红线 1/3;D4 豁免 2026-10-11「全部解决」令):独立
  模块 :mod:`wechat_bridge.memsearch`,配置 ``mem_search_enabled`` 默认关,
  显式开启 + 提权才生效;本模块零进程接触。

E2 解密副本(G5 生命周期):

- ``db_storage`` 加密库 → sqlcipher CLI 解密**副本**至数据根私有区
  ``wechat-localdb/decrypted/<域>/<库>`(文件 600/目录 700,prd 红线 6);
  sqlcipher 缺失 → 结构化报错 + brew 指引(design §5.1,不静默半装)。
- TTL 24h(配置 ``copy_ttl_hours``)失效重建 + 容量上限(配置
  ``copy_capacity_mb``);解密失败触发重建;微信进程零接触、零出网。
  2026-10-14 修订:CDN GET(sns export --with-media,缺省关)为唯一受限
  豁免,见 docs/wechat-mediadecrypt.md §11。
  **0.4.4 源新即重建**:源库(含 ``-wal``)mtime 比副本新 = 缓存失效
  (微信持续写库,TTL 内的新消息也要可见——近实时监控的正确性前提)。

密钥钥匙串化(task 10-14-wechat-keys-keychain;主人令 2026-10-14:
密钥是保密数据,本地保存应加密):

- 读取两级化:macOS 钥匙串条目 ``myia/wechat/db-keys``(:mod:`.keychain`
  最小通道,值 = 完整 keys.json 的 JSON 外壳)优先;文件 keys.json 兜底
  (兼容);两者都无 = 现既有空态。:func:`keys_migrate` /
  :func:`keys_unmigrate` 是容器迁移对(文件↔钥匙串,验真门照跑,断电安全:
  先写钥匙串并回读验证成功才动文件)。
- ``acquired_at`` 语义:钥匙串条目无 mtime,取外壳 ``migrated_at`` 字段
  (写入即刷新,key-status 不谎;文件源仍是文件 mtime,零漂移)。

外部取钥器(B3,task 10-13-wechat-keyprovider;协议 v1 +
v1.1 扩展 = docs/wechat-keyprovider.md):

- MYIA 产品代码**零取钥实现**:取钥能力整体外包给用户自备的外部可执行件,
  桥只认协议——不校验来源与签名、不内置降级(取钥器故障 = exit 21 如实,
  绝不静默回退内置取钥)。:func:`acquire_keys_from_provider` 是桥侧全链:
  spawn 子进程 → stdin 单行 JSON 请求 → stdout 按行 NDJSON(progress +
  result)→ 退出码矩阵判定 → 逐把页 1 HMAC 验真 → 全量命中才落 keys.json
  (缓存由桥独占写)。挂点 = :func:`resolve_keys` 密钥缓存缺失分支
  (配置 ``key_provider_path``,管理命令 ``localdb key-provider set|get|clear``)。

密钥状态/交互式取钥(task 10-13-wechat-monitor-ui D2/D3;协议 v1.1):

- :func:`key_status` = ``localdb key-status`` 三态真源(missing/stale/
  ready):探针的零成本判据只看 keys.json 在场,钥匙失配时会说谎——本命令
  自带**抽样重验**(mapping 前中后各 1 把、至多 3 把,复用
  :func:`verify_key_for_page` 同一验真器),秒级、恒 exit 0(三态即正常态,
  不判错)。``acquired_at`` = keys.json 文件 mtime(零格式变更,cache 不加
  元数据键——「键=库相对路径」消费方零破坏)。
- :func:`key_acquire` = ``localdb key-acquire`` 交互式取钥编排:ready 且无
  ``--force`` → ``already_ready`` 短路;否则 spawn 取钥器(协议 v1.1:请求
  携带 ``timeout_hint_seconds``,桥内硬帽 = clamp(hint, 120, 1800));
  provider stdout 的 progress 行**原样转印**到桥 stdout(NDJSON 流,终态单
  行 JSON 收尾);启动先清残留取消哨兵(:data:`CANCEL_SENTINEL_NAME`);
  收到 SIGTERM(壳 kill)→ kill provider 进程组 + 自身退出码 143(提权段
  清理由部署件哨兵轮询自理,docs §12.3)。未配置取钥器 = exit 21 法定文案
  (:data:`PROVIDER_UNCONFIGURED_MESSAGE`,与 query 缺钥同族同码)。

私有数据红线(prd 红线 6):密钥材料/聊天内容不入 git/日志/报告;本模块
的错误消息与应答只承载形状(计数/路径名/字节数)。
"""

from __future__ import annotations

import fcntl
import hashlib
import hmac
import os
import queue
import shutil
import signal
import sqlite3
import struct
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

from . import keychain, system_checks
from .codes import DECRYPT_FAILED, DB_NOT_FOUND, EXIT_GENERIC_FAILURE, KEY_UNAVAILABLE, BridgeError
from .config import LOCALDB_KEYS_REL_PATH, myssia_home
from .system_checks import WECHAT_FILES_ROOT

if TYPE_CHECKING:  # 仅供类型注解(运行时鸭子类型,防循环导入——原注释纪律)
    from .config import BridgeConfig

__all__ = [
    "DB_STORAGE_DIR_NAME",
    "LOCALDB_PRIVATE_DIR",
    "PAGE_SZ",
    "PROVIDER_ACTION_GET_DB_KEY",
    "PROVIDER_STDERR_TAIL_CHARS",
    "PROVIDER_TIMEOUT_SECONDS",
    "PROVIDER_TIMEOUT_HINT_MAX_SECONDS",
    "PROVIDER_TIMEOUT_HINT_MIN_SECONDS",
    "PROVIDER_UNCONFIGURED_MESSAGE",
    "KEY_ACQUIRE_TIMEOUT_HINT_DEFAULT",
    "KEY_STATUS_SAMPLE_MAX",
    "CANCEL_SENTINEL_NAME",
    "locate_db_storage",
    "locate_key_info_db",
    "verify_key_for_page",
    "verify_key_mapping",
    "extract_key_candidates",
    "acquire_key",
    "acquire_keys_from_provider",
    "clamp_provider_timeout",
    "cancel_sentinel_path",
    "clear_cancel_sentinel",
    "key_status",
    "key_acquire",
    "keys_migrate",
    "keys_unmigrate",
    "resolve_keys",
    "read_db_keys_from_keychain",
    "keychain_available_guarded",
    "key_cache_path",
    "write_key_cache",
    "read_key_cache",
    "domain_targets",
    "copy_dir",
    "sqlcipher_available",
    "ensure_decrypted_copies",
    "query_history",
    "group_info",
    "page_history",
    "export_history",
    "contacts_inventory",
    "sessions_list",
    "conversations_census",
]

#: 单账号本地库目录名(db_storage;research §7.1 实测)。
DB_STORAGE_DIR_NAME = "db_storage"

#: 数据根私有区里本地库通道的落点前缀(副本/密钥缓存;design §1/§2)。
LOCALDB_PRIVATE_DIR = "wechat-localdb"

# —— SQLCipher 4 页格式常量(参考件 wechat-mcp-macos crypto/keys/common.py
#    与 crypto/decrypt.py 的配方;纯 stdlib 复刻,零第三方依赖)——
PAGE_SZ = 4096
SALT_SZ = 16
KEY_SZ = 32
RESERVE_SZ = 80  # IV(16) + HMAC-SHA512(64)
SQLCIPHER_TIMEOUT_SECONDS = 300.0


# =====================================================================
# 定位(纯只读)
# =====================================================================


def locate_db_storage(
    *,
    files_root: Path | None = None,
    account_picker: Callable[[list[Path]], Path] | None = None,
) -> Path:
    """定位已登录账号的 ``db_storage/`` 目录(纯只读;多账号时取最新)。

    多账号目录 = 带 ``db_storage/`` 的直接子目录;取 mtime 最新一个
    (「当前已登录账号」的零交互近似——prd R4:桥只操作当前已登录账号,
    不做账号管理)。

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
            fix_hint="确认微信在本机登录过;多账号场景以登录态元数据判定(Phase E 已注记)",
        )
    if account_picker is not None:
        return account_picker(candidates) / DB_STORAGE_DIR_NAME
    latest = max(candidates, key=lambda item: item.stat().st_mtime)
    return latest / DB_STORAGE_DIR_NAME


def locate_key_info_db(
    db_storage: Path, *, files_root: Path | None = None
) -> Path:
    """定位当前账号的 ``key_info.db``(E1 零内存途径的入口文件)。

    布局(A3 实测):``<数据根>/all_users/login/<wxid>/key_info.db``——login
    子目录名是 wxid(不带设备后缀),与账号目录(带后缀)前缀对应;多候选
    时优先取「名字是账号目录前缀」者,其余取 mtime 最新。

    Raises:
        BridgeError: exit 21 ``key_unavailable``(数据根缺位 / 无 key_info.db)。
    """
    root = files_root if files_root is not None else db_storage.parents[1]
    login_dir = root / "all_users" / "login"
    candidates = (
        sorted(login_dir.glob("*/key_info.db")) if login_dir.is_dir() else []
    )
    if not candidates:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"key_info.db 不在场(零内存密钥途径入口缺失): {login_dir}",
            fix_hint=(
                "确认微信在本机登录过;D4 密钥途径:内存扫描(localdb key-scan,"
                "配置 mem_search_enabled 显式开启+提权,默认关,prd 红线 1/3)"
                "或引入外部密钥(keys.json,600 权限)"
            ),
        )
    account_name = db_storage.parent.name
    prefixed = [c for c in candidates if account_name.startswith(c.parent.name)]
    if prefixed:
        return prefixed[0]
    return max(candidates, key=lambda item: item.stat().st_mtime)


# =====================================================================
# E1 密钥:离线校验器 + 候选提取(机制完整;材料在途即弃,零落盘)
# =====================================================================


def verify_key_for_page(enc_key: bytes, db_page1: bytes) -> bool:
    """对加密库 page1 做离线 HMAC-SHA512 校验(SQLCipher 4 原始密钥语义)。

    配方 = 参考件 wechat-mcp-macos ``crypto/keys/common.py:19-28`` 逐行复刻
    (纯 hashlib/hmac,零第三方依赖):salt=page1 前 16B → mac_salt=salt⊕0x3A
    → mac_key=PBKDF2-HMAC-SHA512(key, mac_salt, 2 轮) → HMAC 对
    page1[16:4032] + 小端页号(1) 比对尾部 64B 存档 HMAC。纯离线,零进程接触。
    """
    if len(db_page1) < PAGE_SZ:
        return False
    salt = db_page1[:SALT_SZ]
    mac_salt = bytes(b ^ 0x3A for b in salt)
    mac_key = hashlib.pbkdf2_hmac("sha512", enc_key, mac_salt, 2, dklen=KEY_SZ)
    hmac_data = db_page1[SALT_SZ : PAGE_SZ - RESERVE_SZ + SALT_SZ]
    stored_hmac = db_page1[PAGE_SZ - RESERVE_SZ + SALT_SZ : PAGE_SZ]
    hm = hmac.new(mac_key, hmac_data, hashlib.sha512)
    hm.update(struct.pack("<I", 1))
    return hmac.compare_digest(hm.digest(), stored_hmac)


def verify_key_mapping(
    db_storage: Path,
    keys: dict[str, str],
    *,
    targets: list[tuple[str, int, bytes]] | None = None,
) -> dict[str, str]:
    """对密钥映射逐条离线 HMAC 重验(keys.json 消费前的唯一放行门)。

    条目形状:键 = 相对 ``db_storage`` 的库路径,值 = 64-hex SQLCipher 密钥。
    库不在场 / 非 hex / 长度非 32B / HMAC 不符的条目一律弃(宁缺毋假)——
    缓存与外部供给同位同权(:func:`resolve_keys`),验证不过的 key 进不了
    解密链(红线 6 同源纪律:假钥匙既解不开库,也不能制造半真状态)。

    Returns:
        验证通过的子集(相对路径 → key hex 原文)。
    """
    page_targets = targets if targets is not None else page1_targets(db_storage)
    page1_by_rel = {rel: page1 for rel, _size, page1 in page_targets}
    verified: dict[str, str] = {}
    for rel, hex_key in keys.items():
        page1 = page1_by_rel.get(rel)
        if page1 is None:
            continue  # 库不在场(账号切换/域漂移):条目弃,不硬配
        try:
            raw = bytes.fromhex(hex_key)
        except ValueError:
            continue  # 非 hex:条目弃
        if len(raw) == KEY_SZ and verify_key_for_page(raw, page1):
            verified[rel] = hex_key
    return verified


def _read_varint(buf: bytes, i: int) -> tuple[int, int]:
    """protobuf varint 读取(形状级解析用;越界/超长 = 解析失败)。"""
    result = 0
    shift = 0
    while True:
        if i >= len(buf):
            raise ValueError("varint 越界")
        b = buf[i]
        i += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            return result, i
        shift += 7
        if shift > 63:
            raise ValueError("varint 超长")


def _proto_length_delimited(buf: bytes) -> list[tuple[int, int, bytes]]:
    """无 schema protobuf 走读,取全部 length-delimited 字段 (fno, len, payload)。

    只取形状(字段号/长度/切片引用),解析不干净(非法 tag/越界)即回空——
    E1 候选提取宁可少选不可误吞。
    """
    fields: list[tuple[int, int, bytes]] = []
    i = 0
    try:
        while i < len(buf):
            tag, i = _read_varint(buf, i)
            fno, wt = tag >> 3, tag & 7
            if fno == 0:
                return []
            if wt == 0:
                _, i = _read_varint(buf, i)
            elif wt == 2:
                ln, i = _read_varint(buf, i)
                if i + ln > len(buf):
                    return []
                fields.append((fno, ln, buf[i : i + ln]))
                i += ln
            elif wt == 5:
                i += 4
            elif wt == 1:
                i += 8
            else:
                return []
    except ValueError:
        return []
    return fields


def extract_key_candidates(blobs: list[bytes]) -> list[bytes]:
    """从 key_info_data BLOB 族提取候选 32B key(顺序保序去重)。

    候选族 = E1 真跑所用全族(与公开独立实测同形):
    ① 各 length-delimited 字段 payload 的全部 32B 滑窗;
    ② 整 BLOB 的全部 32B 滑窗;
    ③ 各 payload 与整 BLOB 的 sha256 派生。
    """
    candidates: list[bytes] = []
    seen: set[bytes] = set()

    def push(item: bytes) -> None:
        if len(item) == KEY_SZ and item not in seen:
            seen.add(item)
            candidates.append(item)

    for blob in blobs:
        payloads = [payload for _f, _l, payload in _proto_length_delimited(blob)]
        payloads.append(blob)
        for payload in payloads:
            for off in range(0, max(len(payload) - KEY_SZ + 1, 0)):
                push(payload[off : off + KEY_SZ])
            push(hashlib.sha256(payload).digest())
    return candidates


def read_key_info_blobs(key_db: Path) -> list[bytes]:
    """读 key_info.db 全行 ``key_info_data``(只读;BLOB 仅入内存即弃)。

    schema 形状先验证(LoginKeyInfoTable 四列在场;A3 实测形状),不符 =
    exit 21(版本脆弱性如实报,红线 7)。
    """
    if not key_db.is_file():
        raise BridgeError(
            KEY_UNAVAILABLE, f"key_info.db 不在场: {key_db}", fix_hint="确认微信在本机登录过"
        )
    try:
        con = sqlite3.connect(f"file:{key_db}?mode=ro", uri=True)
    except sqlite3.Error as exc:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"key_info.db 只读打开失败({type(exc).__name__}): {key_db}",
        ) from exc
    try:
        tables = {
            row[0]
            for row in con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        if "LoginKeyInfoTable" not in tables:
            raise BridgeError(
                KEY_UNAVAILABLE,
                f"key_info.db schema 形状漂移(LoginKeyInfoTable 不在场;表数={len(tables)})",
                fix_hint="微信版本升级可能改变密钥落盘形状(prd 红线 7);D4 裁决前不硬解析",
            )
        rows = con.execute(
            "SELECT key_info_data FROM LoginKeyInfoTable WHERE key_info_data IS NOT NULL"
        ).fetchall()
    except sqlite3.Error as exc:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"key_info.db 只读查询失败({type(exc).__name__})",
        ) from exc
    finally:
        con.close()
    return [bytes(row[0]) for row in rows if row[0]]


def page1_targets(db_storage: Path) -> list[tuple[str, int, bytes]]:
    """枚举 ``db_storage`` 各加密库的 page1(形状:相对路径/大小/page1)。

    小库在前(校验便宜优先);零进程接触、零出网。
    """
    targets: list[tuple[str, int, bytes]] = []
    for db in sorted(db_storage.rglob("*.db")):
        size = db.stat().st_size
        if size < PAGE_SZ:
            continue
        rel = db.relative_to(db_storage).as_posix()
        with db.open("rb") as fh:
            page1 = fh.read(PAGE_SZ)
        targets.append((rel, size, page1))
    targets.sort(key=lambda item: item[1])
    return targets


def acquire_key(
    db_storage: Path,
    *,
    files_root: Path | None = None,
    key_db: Path | None = None,
    targets: list[tuple[str, int, bytes]] | None = None,
) -> dict[str, str]:
    """E1 零内存密钥获取全链(真实现;当前如实负结论 → exit 21)。

    链路:定位 key_info.db → 读 BLOB 族 → 候选提取 → 对各库 page1 离线
    HMAC 校验(先小库)→ 命中 key 交叉验证其余库。成功返回
    ``{相对路径: key hex}``;失败抛 §6 exit 21,消息只承载形状计数 + D4
    指引(**绝无材料**)。

    Returns:
        dict: 加密库相对路径 → 32B key 的 hex(可含多库各自 key)。
    """
    key_file = key_db if key_db is not None else locate_key_info_db(
        db_storage, files_root=files_root
    )
    blobs = read_key_info_blobs(key_file)
    targets = targets if targets is not None else page1_targets(db_storage)
    candidates = extract_key_candidates(blobs)

    matched: dict[str, str] = {}
    attempts = 0
    for rel, _size, page1 in targets:
        if rel in matched:
            continue
        for key in candidates:
            attempts += 1
            if verify_key_for_page(key, page1):
                hex_key = key.hex()
                matched[rel] = hex_key
                # 交叉验证:同一 key 试其余未匹配库(参考件 common.py:113 同款)。
                for rel2, _s2, page1_2 in targets:
                    if rel2 not in matched and verify_key_for_page(key, page1_2):
                        matched[rel2] = hex_key
                break

    if matched and len(matched) == len(targets):
        write_key_cache(matched)
        return matched
    if matched:
        # 部分命中:不整体成功、不落缓存(缓存=全量验证子集,探针判据
        # 以它为准,半套缓存会让探针与 query 状态互相矛盾)。
        raise BridgeError(
            KEY_UNAVAILABLE,
            "本地库密钥部分命中:"
            f"候选={len(candidates)} 校验={attempts}次 命中={len(matched)}/{len(targets)}库;"
            "其余库的 key 不在零内存候选族内(D4 待裁决)",
            fix_hint=(
                "D4 待主人裁决:豁免内存密钥搜索(配置 mem_search_enabled 显式开启,"
                "memsearch 三重门)或引入外部密钥(数据根私有区 wechat-localdb/keys.json,"
                "600 权限,键=库相对路径/值=64-hex);部分命中不落缓存(缓存=全量验证子集)"
            ),
        )
    raise BridgeError(
        KEY_UNAVAILABLE,
        "本地库密钥不可得:零内存途径(key_info.db)实测未闭合——"
        f"行数={len(blobs)} 候选={len(candidates)} 离线HMAC校验={attempts}次 "
        f"命中=0/{len(targets)}库;密钥材料疑被机器专属密钥包裹、文件内不可推导"
        "(2026-10-11 E1 真跑 + 三方独立公开实测一致)",
        fix_hint=(
            "D4 待主人裁决:①豁免内存密钥搜索(配置 mem_search_enabled 显式开启"
            "+提权,memsearch 三重门,prd 红线 1/3)②或引入外部密钥:数据根私有区"
            "wechat-localdb/keys.json(600 权限,键=库相对路径,值=64-hex SQLCipher "
            "密钥,查询前逐条重验);校验机制已就绪,密钥可得即全链闭合"
        ),
    )


# =====================================================================
# 密钥缓存(成功才落;数据根私有区 600;探针零成本判据)
# =====================================================================


def key_cache_path(data_root: Path | None = None) -> Path:
    """密钥缓存产物路径(数据根私有区 wechat-localdb/keys.json;design §5.3)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / LOCALDB_PRIVATE_DIR / Path(LOCALDB_KEYS_REL_PATH).name


def _restore_owner_for_sudo(path: Path) -> None:
    """sudo 会话落盘把属主归还给发起 sudo 的用户(SUDO_UID/SUDO_GID)。

    背景(D4 复审坐实):key-scan 门③只放行 euid==0(memsearch 提权门),
    root 写 keys.json 会把缓存目录与文件建成 root 属主;此后用户侧
    ``localdb query`` 读缓存 PermissionError(被 :func:`read_key_cache`
    如实 None 语义收编)→ :func:`resolve_keys` 静默回落 E1 → 扫描实为
    命中却被报成零命中,「一步闭合」自坏。sudo 会话自带 SUDO_UID/
    SUDO_GID,即取即还;非 sudo 的 root 会话无从判定目标属主,保持原样
    (文档命令尾部另有显式 chown 兜底)。
    """
    if os.geteuid() != 0:
        return
    uid = os.environ.get("SUDO_UID")
    gid = os.environ.get("SUDO_GID")
    if uid is None or gid is None:
        return
    try:
        os.chown(path, int(uid), int(gid))
    except (OSError, ValueError):
        pass  # 归还失败不拦扫描本身;文档命令尾部显式 chown 兜底


def write_key_cache(mapping: dict[str, str], *, data_root: Path | None = None) -> Path:
    """写密钥缓存(仅验证通过的 key;600 权限;目录 700;sudo 下属主归还)。

    钥匙串化(task 10-14-wechat-keys-keychain):**迁移态**(钥匙串条目
    ``myia/wechat/db-keys`` 已在场)下落点改为刷新钥匙串条目(外壳随写刷新
    migrated_at),明文件不再重建——密钥轮换后明文不回流(主人令:本地保存
    应加密);返回值仍是规范文件路径(缓存落点标识,消费方报告零改面)。
    钥匙串写失败(锁死等)= 回落明文件(可用性优先;之后 ``keys-migrate``
    归拢)。root 会话(euid==0)触不到用户钥匙串,同样回落明文件(判例同
    :func:`_restore_owner_for_sudo` 的 sudo 形态)。
    """
    path = key_cache_path(data_root)
    if os.geteuid() != 0 and keychain_available_guarded():
        try:
            existing = keychain.read_item(keychain.DB_KEYS_ACCOUNT)
        except BridgeError:
            existing = None  # 探测失败按未迁移处理:落明文件,keys-migrate 可后补归拢
        if existing is not None:
            try:
                keychain.write_item(
                    keychain.DB_KEYS_ACCOUNT,
                    keychain.build_db_keys_envelope(mapping),
                )
                return path
            except BridgeError:
                pass  # 回落明文件(可用性;docstring 已述)
    _write_key_cache_file(mapping, data_root=data_root)
    return path


def keychain_available_guarded() -> bool:
    """钥匙串通道在场性(:mod:`.keychain` 薄封装;测试可整体关闸的接缝)。"""
    return keychain.keychain_available()


def _write_key_cache_file(mapping: dict[str, str], *, data_root: Path | None = None) -> Path:
    """明文件落盘(原 write_key_cache 本体;600/目录 700/sudo 属主归还)。"""
    import json

    path = key_cache_path(data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    path.write_text(json.dumps(mapping, indent=1) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)
    _restore_owner_for_sudo(path.parent)
    _restore_owner_for_sudo(path)
    return path


def read_key_cache(*, data_root: Path | None = None) -> dict[str, str] | None:
    """读密钥缓存(缺文件/坏 JSON → None 如实;探针零成本判据用)。"""
    import json

    path = key_cache_path(data_root)
    if not path.is_file():
        return None
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(raw, dict) or not raw:
        return None
    return {str(k): str(v) for k, v in raw.items()}


def read_db_keys_from_keychain(
    notes: list[str] | None = None,
) -> tuple[dict[str, str] | None, str | None]:
    """读钥匙串 db-keys 条目 → ``(映射, migrated_at)``。

    缺席/通道不可用/坏形状 = ``(None, None)``(「源缺席」语义,兜底链照走);
    读失败(锁死等)如实入 ``notes``(排查者不被静默带偏)。值永不入
    notes/异常消息(红线 6)。
    """
    try:
        raw = keychain.read_item(keychain.DB_KEYS_ACCOUNT)
    except BridgeError as exc:
        if notes is not None:
            notes.append(f"钥匙串条目读取失败({exc.message})")
        return None, None
    if raw is None:
        return None, None
    mapping, migrated_at = keychain.parse_db_keys_envelope(raw)
    if mapping is None and notes is not None:
        notes.append("钥匙串条目在场但值形状不可解析(弃,不硬配)")
    return mapping, migrated_at


# =====================================================================
# 外部取钥器(B3;协议 v1 = docs/wechat-keyprovider.md——桥只认协议,
# 零取钥实现零来源校验:风险件用户自备、自行担责)
# =====================================================================

#: 取钥器子进程硬上限 v1 基线(协议 §6:120 秒 = spawn 起全程预算,与 progress
#: 输出无关,无延长协商;模块常量非配置面——协议钉死的边界)。v1.1 的
#: key-acquire 调用以 :func:`clamp_provider_timeout` 在 [MIN, MAX] 内放宽。
PROVIDER_TIMEOUT_SECONDS = 120.0
#: v1.1 timeout_hint 桥内硬帽下限(协议 §12:hint 再小也至少给 v1 基线窗)。
PROVIDER_TIMEOUT_HINT_MIN_SECONDS = 120
#: v1.1 timeout_hint 桥内硬帽上限(协议 §12:防取钥器/调用方乱报大值)。
PROVIDER_TIMEOUT_HINT_MAX_SECONDS = 1800
#: key-acquire 等待窗提示缺省(秒;design §2 决议⑥:重登是分钟级人操作)。
KEY_ACQUIRE_TIMEOUT_HINT_DEFAULT = 600
#: key-status 抽样重验的把数上限(mapping 前中后各 1;design §A.1)。
KEY_STATUS_SAMPLE_MAX = 3
#: 取消哨兵文件名(design §C/§12.3:壳/上层取消 = 落文件;取钥器提权段
#: 轮询见即自杀+清孤儿+删哨兵;桥 key-acquire 启动先清残留)。
CANCEL_SENTINEL_NAME = "cancel.keyacquire"
#: 失败场景 stderr 消费的尾部字符数(协议 §2/§6:stderr 是调试旁路,
#: 仅失败被取尾部 500 字符附入错误信息;成功时桥不读)。
PROVIDER_STDERR_TAIL_CHARS = 500
#: 未配置取钥器的法定错误文案(协议 §8;查询链密钥不可得且未配置时
#: 并入 exit 21 消息——设置页/文档引导的锚文本)。
PROVIDER_UNCONFIGURED_MESSAGE = "未配置外部取钥器,请在设置中指定可执行文件路径"
#: 协议 v1 唯一动作(桥只发 ``get_db_key``;未知动作的处理属取钥器侧事务)。
PROVIDER_ACTION_GET_DB_KEY = "get_db_key"


def _configured_provider_path(config: Any) -> str:
    """已配置的取钥器路径(空白 = 未配置;duck-type 容错测试替身)。"""
    return str(getattr(config, "key_provider_path", "") or "").strip()


def clamp_provider_timeout(hint: int) -> int:
    """v1.1 等待窗硬帽 = clamp(hint, 120, 1800)(协议 §12;防乱报双向夹逼)。"""
    return max(
        PROVIDER_TIMEOUT_HINT_MIN_SECONDS,
        min(PROVIDER_TIMEOUT_HINT_MAX_SECONDS, int(hint)),
    )


def cancel_sentinel_path(data_root: Path | None = None) -> Path:
    """取消哨兵路径(``<数据根>/wechat-localdb/cancel.keyacquire``;design §C)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / LOCALDB_PRIVATE_DIR / CANCEL_SENTINEL_NAME


def clear_cancel_sentinel(*, data_root: Path | None = None) -> bool:
    """清残留取消哨兵(key-acquire 启动面;在场即删,缺席 = False 如实)。

    残留 = 上轮获取流崩溃/被杀,部署件未及轮询即死——哨兵只在获取进行中
    生效,清掉不影响任何在途行为(design §7 风险表)。
    """
    try:
        cancel_sentinel_path(data_root).unlink()
        return True
    except OSError:
        return False


def _iso_local_mtime(path: Path) -> str | None:
    """文件 mtime → ISO 本地时(秒精度;文件缺位 → None)。"""
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return None
    return datetime.fromtimestamp(mtime).astimezone().isoformat(timespec="seconds")


def _kill_process_group(proc: subprocess.Popen) -> None:
    """kill 取钥器进程组(start_new_session spawn → pgid == pid)。"""
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except OSError:
        try:
            proc.kill()  # 组已消亡/权限面的兜底单杀
        except OSError:
            pass


def _provider_account_id(db_storage: Path) -> str:
    """请求 ``account_id`` 的零交互推导(只读,供多账号场景选钥)。

    与 :func:`locate_key_info_db` 同序:``all_users/login/<wxid>`` 目录名是
    账号目录名(wxid_xxx 带设备后缀)的前缀 → 前缀匹配优先;匹配不到回落
    账号目录名(取钥器侧自行取舍,桥只给最佳推断)。
    """
    root = db_storage.parents[1] if len(db_storage.parents) > 1 else db_storage.parent
    login_dir = root / "all_users" / "login"
    account_dir = db_storage.parent.name
    if login_dir.is_dir():
        prefixed = sorted(
            child.name
            for child in login_dir.iterdir()
            if child.is_dir() and account_dir.startswith(child.name)
        )
        if prefixed:
            return prefixed[0]
    return account_dir


def acquire_keys_from_provider(
    db_storage: Path,
    provider_path: str,
    *,
    account_id: str | None = None,
    targets: list[tuple[str, int, bytes]] | None = None,
    data_root: Path | None = None,
    timeout: float = PROVIDER_TIMEOUT_SECONDS,
    timeout_hint_seconds: int | None = None,
    on_progress: Callable[[str], None] | None = None,
    on_spawn: Callable[[subprocess.Popen], None] | None = None,
) -> dict[str, str]:
    """spawn 外部取钥器取钥(协议 v1 全链 + v1.1 可选扩展;任何失败 =
    exit 21,无降级)。

    时序照协议 §2:spawn(独立进程组,取消面可 killpg)→ stdin 写**单行**
    JSON 请求(写完即关 stdin)→ stdout **按行流式**读 NDJSON(progress
    0..N + result 恰一次;``on_progress`` 逐行实时回调,v1.1 key-acquire 的
    progress 转印挂点)→ 退出码矩阵判定(§6)→ 返回钥匙逐把页 1 离线验真
    (§7,复用 :func:`verify_key_for_page`)→ 全量命中才
    :func:`write_key_cache`(600,缓存由桥独占写、验真后才落;部分命中不落
    缓存 = 全链既有纪律)。超时 = spawn 起全程预算(与 progress 输出无关),
    到点 kill 子进程组;``timeout_hint_seconds``(v1.1 可选)透传进请求字段
    供取钥器自整等待窗——query 链(v1)恒不携带,行为不变。

    判定取舍(§6 矩阵 + v1 未定义处的确定性实现):``result``
    ``success:false``(任意退出码)= 失败透传取钥器 ``error``;退出码非 0 =
    失败附 stderr 尾部;退出码 0 无 ``result`` = 失败「未返回结果」;超时 =
    kill 失败。首条 ``result`` 即终态、其后行忽略排空(v1 未定义桥的取舍);
    非 JSON/非协议行不计入协议(有 ``result`` 时忽略,无时计入失败明细)。
    ``keys`` 键 = salt_hex(匹配库文件前 16 字节)或 ``"*"`` 通配(全域同钥);
    混用时 ``"*"`` 铺底、逐 salt 后到覆盖;盐不匹配任何在场库的条目弃。

    Returns:
        dict: 加密库相对路径 → key hex(全部经页 1 离线验证)。

    Raises:
        BridgeError: exit 21(一切取钥器侧失败收敛 ``key_unavailable``;
            消息只承载形状与取钥器自报 ``error``,绝无密钥材料——红线 6)。
    """
    import json

    page_targets = targets if targets is not None else page1_targets(db_storage)
    if not page_targets:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"外部取钥器不适用:db_storage 下无待解密库(无 ≥{PAGE_SZ}B 的 .db): {db_storage}",
        )
    exe = Path(provider_path).expanduser()
    request: dict[str, Any] = {
        "action": PROVIDER_ACTION_GET_DB_KEY,
        "db_path": str(db_storage),
        "account_id": (
            account_id if account_id is not None else _provider_account_id(db_storage)
        ),
    }
    if timeout_hint_seconds is not None:
        # v1.1(§12):可选请求字段;v1 取钥器不认识的自有字段应忽略,向后兼容。
        request["timeout_hint_seconds"] = int(timeout_hint_seconds)
    try:
        proc = subprocess.Popen(  # noqa: S603 - 用户自备外部件,契约=docs/wechat-keyprovider.md
            [str(exe)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,  # 独立进程组:取消面(key-acquire SIGTERM)可 killpg 整组
        )
    except OSError as exc:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"取钥器子进程启动失败({type(exc).__name__}): {exe}",
            fix_hint=(
                "核对路径存在且有可执行位(localdb key-provider get 可查在位状态);"
                "运行期 spawn 失败如实报(协议 §8)"
            ),
        ) from exc
    if on_spawn is not None:
        on_spawn(proc)

    # —— 流式读:v1 只判终态(等效 communicate);v1.1 key-acquire 经 on_progress
    #    逐行转印。读者线程 + 队列 = 行级超时的唯一便携形态;stderr 并发排空
    #    防 64KB 管道写满死锁(communicate 同款职责)。——
    deadline = time.monotonic() + timeout
    line_queue: queue.Queue[str | None] = queue.Queue()
    stderr_chunks: list[bytes] = []

    def _stdout_reader() -> None:
        assert proc.stdout is not None
        try:
            for raw in proc.stdout:
                line_queue.put(raw.decode("utf-8", errors="replace"))
        finally:
            line_queue.put(None)  # EOF 哨兵(读尽/异常同形收尾)

    def _stderr_reader() -> None:
        assert proc.stderr is not None
        try:
            stderr_chunks.append(proc.stderr.read())
        except OSError:
            pass  # 诊断旁路读失败不拦协议判定(stderr 尾部缺席 = 明细少一段)

    threads = [
        threading.Thread(target=_stdout_reader, daemon=True),
        threading.Thread(target=_stderr_reader, daemon=True),
    ]
    for thread in threads:
        thread.start()
    try:
        assert proc.stdin is not None
        proc.stdin.write(
            json.dumps(request, ensure_ascii=False).encode("utf-8") + b"\n"
        )
        proc.stdin.close()
    except (BrokenPipeError, OSError):
        pass  # 取钥器秒退不读 stdin:请求已尽力送达,判定交给退出码矩阵

    out_lines: list[str] = []
    result_seen = False
    timed_out = False
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            break
        try:
            line = line_queue.get(timeout=remaining)
        except queue.Empty:
            timed_out = True
            break
        if line is None:
            break
        out_lines.append(line)
        if on_progress is not None and not result_seen:
            stripped = line.strip()
            if stripped:
                try:
                    obj = json.loads(stripped)
                except ValueError:
                    obj = None
                if isinstance(obj, dict) and obj.get("type") == "progress":
                    on_progress(line.rstrip("\r\n"))
                elif isinstance(obj, dict) and obj.get("type") == "result":
                    result_seen = True  # result 后的行协议上不存在,不再转印

    if not timed_out:
        try:  # stdout EOF 后收尸(留 ≥1s 余量防 EOF 恰在预算边界)
            proc.wait(timeout=max(deadline - time.monotonic(), 1.0))
        except subprocess.TimeoutExpired:
            timed_out = True
    if timed_out:
        _kill_process_group(proc)
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:  # pragma: no cover - SIGKILL 后罕见
            pass
        for thread in threads:
            thread.join(timeout=2)
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"外部取钥器超时(>{timeout:.0f} 秒已 kill 子进程): {exe.name}",
            fix_hint=(
                "协议 v1 硬上限 120 秒、无延长协商;预计耗时的步骤应尽早输出"
                " result 或主动失败,不要挂满预算"
                if timeout_hint_seconds is None
                else (
                    "协议 v1.1:本次硬帽 = clamp(timeout_hint, 120, 1800) = "
                    f"{timeout:.0f} 秒;交互式等待窗见 docs/wechat-keyprovider.md §12"
                )
            ),
        )
    for thread in threads:
        thread.join(timeout=2)

    stdout_text = "".join(out_lines)
    stderr_tail = _stderr_tail(
        b"".join(stderr_chunks).decode("utf-8", errors="replace")
    )
    result: dict[str, Any] | None = None
    progress_lines = 0
    junk_lines = 0
    for raw_line in stdout_text.splitlines():
        line = raw_line.strip()
        if not line or result is not None:
            continue  # result 即终态,其后行忽略排空(v1 未定义取舍)
        try:
            obj = json.loads(line)
        except ValueError:
            junk_lines += 1
            continue
        if not isinstance(obj, dict):
            junk_lines += 1
            continue
        obj_type = obj.get("type")
        if obj_type == "progress":
            progress_lines += 1
        elif obj_type == "result":
            result = obj
        else:
            junk_lines += 1

    if result is not None and result.get("success") is False:
        provider_error = (
            str(result.get("error") or "").strip()
            or "(取钥器未给出人话 error 字段)"
        )
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"外部取钥器报告失败: {provider_error}",
            fix_hint="取钥器自报错误原样透传(协议 §6);排查取钥器实现或更换取钥件",
        )
    if proc.returncode != 0:
        tail = stderr_tail.strip()
        detail = f";stderr 尾部: {tail}" if tail else ""
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"外部取钥器异常退出(exit={proc.returncode}): {exe.name}{detail}",
        )
    if result is None:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"取钥器未返回结果(退出码 0 但无 result 行;progress {progress_lines} 行,"
            f"非协议行 {junk_lines} 行): {exe.name}",
            fix_hint=(
                "协议 §6:退出码 0 必须恰有一条 result;调试输出一律走 stderr,"
                "stdout 只准协议 NDJSON"
            ),
        )
    if result.get("success") is not True:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"取钥器 result 行形状不符(success 须为布尔): {exe.name}",
            fix_hint="协议 §4:result 的 success 字段必含且为布尔(true/false)",
        )

    keys_raw = result.get("keys")
    if not isinstance(keys_raw, dict) or not keys_raw:
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"取钥器成功应答未携带 keys 映射(空映射或形状不符): {exe.name}",
            fix_hint="协议 §4:成功形态必含 keys({salt_hex: key_hex} 或 \"*\" 通配)",
        )

    page1_by_rel: dict[str, bytes] = {rel: page1 for rel, _size, page1 in page_targets}
    salt_to_rel: dict[str, str] = {
        page1[:SALT_SZ].hex(): rel for rel, _size, page1 in page_targets
    }
    wildcard_count = sum(1 for k in keys_raw if k == "*")
    candidates: dict[str, str] = {}
    unmatched_salts = 0
    # "*" 铺底在前、逐 salt 后到覆盖(混用形态的确定性取舍;协议 §5 建议不混用)
    for salt_key, key_value in sorted(keys_raw.items(), key=lambda kv: kv[0] != "*"):
        if not isinstance(key_value, str):
            continue  # 非 hex 字符串:验真阶段自然弃,此处不硬拒
        hex_key = key_value.strip().lower()
        if salt_key == "*":
            for rel in page1_by_rel:
                candidates[rel] = hex_key
            continue
        rel = salt_to_rel.get(salt_key.strip().lower())
        if rel is None:
            unmatched_salts += 1  # 盐不匹配任何在场库:条目弃(宁缺毋假)
            continue
        candidates[rel] = hex_key

    verified: dict[str, str] = {}
    for rel, hex_key in candidates.items():
        try:
            raw_key = bytes.fromhex(hex_key)
        except ValueError:
            continue  # 非 hex:条目弃(verify_key_mapping 同款纪律)
        if len(raw_key) == KEY_SZ and verify_key_for_page(raw_key, page1_by_rel[rel]):
            verified[rel] = hex_key
    if len(verified) != len(page_targets):
        raise BridgeError(
            KEY_UNAVAILABLE,
            "外部取钥器返回的密钥验真未全量通过:"
            f"给出 {len(keys_raw)} 把(含 '*' 通配 {wildcard_count} 把),"
            f"覆盖在场库 {len(candidates)}/{len(page_targets)}"
            f"(盐不匹配 {unmatched_salts} 条),"
            f"页1 HMAC 验真通过 {len(verified)}/{len(page_targets)};未入缓存",
            fix_hint=(
                "验真 = 页1 离线 HMAC(SQLCipher 4 原始密钥语义);不通过说明钥匙"
                "与库不匹配(登录态轮换后旧钥失效,重取后重试);协议 §5:宁可多给"
                "候选,不要只给一把没把握的钥"
            ),
        )
    write_key_cache(verified, data_root=data_root)
    return verified


def _stderr_tail(text: str) -> str:
    """stderr 尾部截取(协议 §6:500 字符;只入错误信息,不另落盘)。"""
    return text[-PROVIDER_STDERR_TAIL_CHARS:]


# =====================================================================
# 密钥状态 + 交互式取钥编排(task 10-13-wechat-monitor-ui D2/D3;
# 契约 = design §A.1/§A.2;协议 v1.1 = docs/wechat-keyprovider.md §12)
# =====================================================================


def _sample_rels(mapping: dict[str, str]) -> list[str]:
    """抽样库清单(mapping 前中后各 1,至多 :data:`KEY_STATUS_SAMPLE_MAX` 把;
    键序取样保证同库跨次稳定)。"""
    rels = sorted(mapping)
    if len(rels) <= KEY_STATUS_SAMPLE_MAX:
        return rels
    return [rels[0], rels[len(rels) // 2], rels[-1]]


def _verify_cached_entry(db_storage: Path, rel: str, hex_key: str) -> bool:
    """单条缓存条目的页 1 HMAC 验真(:func:`verify_key_mapping` 同器同纪律;
    库不在场 / 非 hex / 长度错 / HMAC 不过 → False,与消费门同判)。"""
    try:
        with (db_storage / rel).open("rb") as fh:
            page1 = fh.read(PAGE_SZ)
    except OSError:
        return False
    if len(page1) < PAGE_SZ:
        return False
    try:
        raw = bytes.fromhex(hex_key)
    except ValueError:
        return False
    return len(raw) == KEY_SZ and verify_key_for_page(raw, page1)


def key_status(
    *,
    data_root: Path | None = None,
    files_root: Path | None = None,
    version_of: Callable[[], str | None] | None = None,
) -> dict[str, object]:
    """密钥缓存三态真源(``localdb key-status``;design §A.1,恒不抛错)。

    三态判据(探针的零成本判据只看文件在场,钥匙失配时会说谎——本命令
    自带抽样重验,与 :func:`write_key_cache` 消费前重验同一验真器),源
    选择镜像 :func:`resolve_keys` 消费序(钥匙串优先、文件兜底——首个
    抽样通过的源即如实态,不谎报):

    - ``missing``:钥匙串条目与 keys.json 文件双双缺位 →「密钥缓存缺位」;
    - ``stale``:在场源的抽样(mapping 前中后各 1,≤3 把)页 1 HMAC 有一把
      不过、且无更低优先源补救 →「抽样验真失败」(微信版本变化/换号后
      失配的如实态);
    - ``ready``:某源抽样全过 →「抽样 N 库验真通过」。

    ``db_count`` = 生效源 mapping 键数(missing=0);``acquired_at`` =
    生效源写入时间 ISO 本地时(钥匙串源 = 外壳 ``migrated_at``,条目无
    mtime;文件源 = 文件 mtime——零漂移);``source`` = ``"keychain"`` |
    ``"file"`` | None(10-14-wechat-keys-keychain 增补);``wechat_version``
    = 探针同源(:func:`wechat_bridge.system_checks.wechat_version`,拿不到
    = None)。钥内容永不出现(计数/时间戳 = 形状级证据,红线 6)。库根
    不可定位时全部抽样按未过计(stale + 注记),不判错——三态查询不
    制造第四态。

    Returns:
        ``{"key_status": {state, db_count, acquired_at, source, wechat_version,
        verdict_note}}``(恒正常应答,exit 0 由 CLI 层兜)。
    """
    version_fn = version_of if version_of is not None else system_checks.wechat_version
    wechat_version_value = version_fn()
    kc_mapping, kc_migrated_at = read_db_keys_from_keychain()
    file_mapping = read_key_cache(data_root=data_root)
    candidates: list[tuple[str, dict[str, str], str | None]] = []
    if kc_mapping is not None:
        candidates.append(("keychain", kc_mapping, kc_migrated_at))
    if file_mapping is not None:
        candidates.append(
            ("file", file_mapping, _iso_local_mtime(key_cache_path(data_root)))
        )
    if not candidates:
        return {
            "key_status": {
                "state": "missing",
                "db_count": 0,
                "acquired_at": None,
                "source": None,
                "wechat_version": wechat_version_value,
                "verdict_note": "密钥缓存缺位",
            }
        }
    unlocatable: BridgeError | None = None
    try:
        db_storage = locate_db_storage(files_root=files_root)
    except BridgeError as exc:
        db_storage = None
        unlocatable = exc

    def _sample_pass(mapping: dict[str, str]) -> tuple[bool, int, int]:
        sample = _sample_rels(mapping)
        passed = 0
        if db_storage is not None:
            for rel in sample:
                if _verify_cached_entry(db_storage, rel, mapping[rel]):
                    passed += 1
        return passed == len(sample), passed, len(sample)

    failures: list[str] = []
    for source, mapping, acquired_at in candidates:
        ok, passed, total = _sample_pass(mapping)
        if ok:
            return {
                "key_status": {
                    "state": "ready",
                    "db_count": len(mapping),
                    "acquired_at": acquired_at,
                    "source": source,
                    "wechat_version": wechat_version_value,
                    "verdict_note": f"抽样 {total} 库验真通过(源 {source})",
                }
            }
        failures.append(f"{source}源 {passed}/{total}")
    source, mapping, acquired_at = candidates[0]
    note = f"抽样验真失败:{'; '.join(failures)}"
    if unlocatable is not None:
        note += "(库根不可定位,全部按未过计)"
    return {
        "key_status": {
            "state": "stale",
            "db_count": len(mapping),
            "acquired_at": acquired_at,
            "source": source,
            "wechat_version": wechat_version_value,
            "verdict_note": note,
        }
    }


def _default_progress_writer() -> Callable[[str], None]:
    """progress 转印缺省落点(桥自身 stdout,逐行 flush——流式可被壳即时读到)。"""

    def _write(line: str) -> None:
        sys.stdout.write(line + "\n")
        sys.stdout.flush()

    return _write


def _acquire_diag(message: str) -> None:
    """stderr 摘要行(§A.2:诊断用计数,不进 stdout 协议流)。"""
    try:
        sys.stderr.write(message + "\n")
    except OSError:  # pragma: no cover - stderr 关闭的极端形态
        pass


def key_acquire(
    *,
    config: "BridgeConfig | None" = None,
    force: bool = False,
    timeout_hint: int = KEY_ACQUIRE_TIMEOUT_HINT_DEFAULT,
    data_root: Path | None = None,
    files_root: Path | None = None,
    version_of: Callable[[], str | None] | None = None,
    emit_line: Callable[[str], None] | None = None,
    targets: list[tuple[str, int, bytes]] | None = None,
) -> dict[str, object]:
    """交互式取钥编排(``localdb key-acquire``;design §A.2,协议 v1.1)。

    时序:①启动清残留取消哨兵(:func:`clear_cancel_sentinel`;§C/§12.3);
    ②**already_ready 短路**(缺省且抽样过 → 直接返回,不 spawn;missing/
    stale 不短路直走取钥器——失效场景不空转;``--force`` = ready 态也跳过
    短路,「重新获取」的旗标);③未配置取钥器 = exit 21 法定文案(与 query
    缺钥同族同码,§F);④spawn 取钥器(:func:`acquire_keys_from_provider`
    全链:请求携带 ``timeout_hint_seconds``,桥内硬帽 = :func:
    `clamp_provider_timeout`,progress 行经 ``emit_line`` **原样转印**);
    ⑤全量验真落缓存后返回 ``{"key_acquire": {result, db_count,
    acquired_at, wechat_version}}``(形状级,钥内容永不出现)。

    取消联动(§A.2):SIGTERM(壳 kill)→ kill 取钥器进程组(SIGKILL)+
    自身退出码 143(SystemExit);root 段清理由部署件哨兵轮询自理。非主
    线程调用(库态)不装信号钩子,取消面交还调用方。

    Raises:
        BridgeError: exit 21(未配置取钥器 / 取钥器侧失败 / 验真未全量,
            全族收敛 ``key_unavailable``)或 exit 20(库根不可定位)。
    """
    clear_cancel_sentinel(data_root=data_root)
    if not force:
        status = key_status(
            data_root=data_root, files_root=files_root, version_of=version_of
        )
        inner = status["key_status"]
        assert isinstance(inner, dict)
        if inner["state"] == "ready":
            return {
                "key_acquire": {
                    "result": "already_ready",
                    "db_count": inner["db_count"],
                    "acquired_at": inner["acquired_at"],
                    "wechat_version": inner["wechat_version"],
                }
            }
    provider_path = _configured_provider_path(config)
    if not provider_path:
        raise BridgeError(
            KEY_UNAVAILABLE,
            PROVIDER_UNCONFIGURED_MESSAGE,
            fix_hint=(
                "wechat-bridge localdb key-provider set <取钥器可执行文件路径> "
                "配置后重试(协议文档 docs/wechat-keyprovider.md)"
            ),
        )
    db_storage = locate_db_storage(files_root=files_root)
    effective_timeout = clamp_provider_timeout(timeout_hint)
    forward = emit_line if emit_line is not None else _default_progress_writer()
    progress_count = 0

    def _forward(line: str) -> None:
        nonlocal progress_count
        progress_count += 1
        forward(line)

    proc_holder: dict[str, subprocess.Popen | None] = {"proc": None}
    previous_handler: Any = None
    handler_installed = False

    def _on_sigterm(_signum: int, _frame: Any) -> None:  # noqa: ANN001 - signal 签名
        live = proc_holder["proc"]
        if live is not None:
            _kill_process_group(live)
        raise SystemExit(143)  # 128+SIGTERM 惯例(§A.2 取消联动)

    try:
        previous_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, _on_sigterm)
        handler_installed = True
    except ValueError:
        pass  # 非主线程(库态调用):不装,取消面交还调用方
    try:
        verified = acquire_keys_from_provider(
            db_storage,
            provider_path,
            targets=targets,
            data_root=data_root,
            timeout=float(effective_timeout),
            timeout_hint_seconds=effective_timeout,
            on_progress=_forward,
            on_spawn=lambda spawned: proc_holder.__setitem__("proc", spawned),
        )
    except BridgeError:
        _acquire_diag(
            f"key-acquire: 取钥失败(硬帽 {effective_timeout}s,"
            f"progress {progress_count} 行转印)"
        )
        raise
    finally:
        if handler_installed:
            signal.signal(signal.SIGTERM, previous_handler)
    _acquire_diag(
        f"key-acquire: 取钥成功 {len(verified)} 库全量验真落缓存"
        f"(硬帽 {effective_timeout}s,progress {progress_count} 行转印)"
    )
    return {
        "key_acquire": {
            "result": "ok",
            "db_count": len(verified),
            "acquired_at": _iso_local_mtime(key_cache_path(data_root)),
            "wechat_version": (
                system_checks.wechat_version() if version_of is None else version_of()
            ),
        }
    }


def _migration_ts() -> str:
    """迁移备份文件名时间戳(判例 = channel_directory.json.bak-YYYYmmdd-HHMMSS)。"""
    return time.strftime("%Y%m%d-%H%M%S")


def keys_migrate(
    *,
    data_root: Path | None = None,
    files_root: Path | None = None,
    targets: list[tuple[str, int, bytes]] | None = None,
) -> dict[str, object]:
    """文件密钥 → 钥匙串迁移(``localdb keys-migrate``;断电安全,不删明文)。

    全链(原子性:先写钥匙串验证成功,才动文件;任何一步失败保持原状):
    ① 读文件 keys.json(缺位 = exit 21「无物可迁」);② HMAC 验真门
    (:func:`verify_key_mapping` 全量命中才放行——与查询消费同一验真器,
    假钥匙进不了钥匙串);③ 写钥匙串条目 ``myia/wechat/db-keys``(JSON
    外壳 migrated_at 随写刷新;旧值先备底,回读不一致时回滚恢复);④
    **回读逐字节验证**(条目值 == 外壳原文且材料映射 == 原映射);⑤ 文件
    改名 ``keys.json.migrated-<ts>`` **保留**(断电安全,不删;重跑幂等)。

    Returns:
        ``{"keys_migrate": {db_count, migrated_at, keychain_account, file_renamed,
        verified, message}}``(形状级回执,钥内容永不出现——红线 6)。

    Raises:
        BridgeError: exit 21(文件缺位/验真未闭合)、exit 1(钥匙串通道
        不可用/回读不一致(已回滚)/文件改名失败)。
    """
    mapping = read_key_cache(data_root=data_root)
    if mapping is None:
        raise BridgeError(
            KEY_UNAVAILABLE,
            "文件密钥缓存缺位,无物可迁",
            fix_hint=(
                "先 localdb key-acquire / key-scan 取钥,或放置 keys.json"
                "(数据根私有区,600)后再迁"
            ),
        )
    db_storage = locate_db_storage(files_root=files_root)
    page_targets = targets if targets is not None else page1_targets(db_storage)
    verified = verify_key_mapping(db_storage, mapping, targets=page_targets)
    if not page_targets or len(verified) != len(page_targets):
        raise BridgeError(
            KEY_UNAVAILABLE,
            "文件密钥未全量验真:"
            f"命中 {len(verified)}/{len(page_targets)}库,拒绝迁移(宁缺毋假)",
            fix_hint="重取密钥后重试(keys.json 与库不匹配,登录态轮换后旧钥失效)",
        )
    if not keychain_available_guarded():
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "本机无钥匙串通道(须 macOS + security CLI),无法迁移",
            code="keychain_backend_unavailable",
        )
    old_raw = keychain.read_item(keychain.DB_KEYS_ACCOUNT)
    envelope = keychain.build_db_keys_envelope(mapping)
    keychain.write_item(keychain.DB_KEYS_ACCOUNT, envelope)
    read_raw = keychain.read_item(keychain.DB_KEYS_ACCOUNT)
    read_mapping, migrated_at = (
        (None, None) if read_raw is None else keychain.parse_db_keys_envelope(read_raw)
    )
    if read_raw != envelope or read_mapping != mapping:
        # 回滚:恢复迁移前原值(原缺席 = 删;原在场 = 原样回写),文件未动。
        rollback_error: str | None = None
        try:
            if old_raw is None:
                keychain.delete_item(keychain.DB_KEYS_ACCOUNT)
            else:
                keychain.write_item(keychain.DB_KEYS_ACCOUNT, old_raw)
        except BridgeError as exc:
            rollback_error = exc.message
        detail = "钥匙串条目已尽力回滚恢复原状" if rollback_error is None else (
            f"钥匙串回滚失败(条目可能停留在新值): {rollback_error}"
        )
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "钥匙串回读验证不一致(材料映射不等),迁移中止;"
            f"{detail};文件未动",
            code="keychain_migration_failed",
            fix_hint="钥匙串状态异常(锁死/损坏);钥匙串访问.app 检查后重试",
        )
    path = key_cache_path(data_root)
    backup = path.with_name(f"{path.name}.migrated-{_migration_ts()}")
    try:
        os.replace(path, backup)
    except OSError as exc:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"明文件改名失败({type(exc).__name__}):钥匙串已迁入且回读验证通过,"
            "明文件保持原位;修复后重跑(幂等)",
            code="keychain_migration_failed",
        ) from exc
    return {
        "keys_migrate": {
            "db_count": len(mapping),
            "migrated_at": migrated_at,
            "keychain_account": keychain.DB_KEYS_ACCOUNT,
            "file_renamed": backup.name,
            "verified": True,
            "message": (
                f"已迁入钥匙串 {keychain.DB_KEYS_ACCOUNT}({len(mapping)} 钥,"
                "回读逐字节验证通过);明文件改名保留: "
                f"{backup.name}(消费序 = 钥匙串优先、文件兜底)"
            ),
        }
    }


def keys_unmigrate(*, data_root: Path | None = None) -> dict[str, object]:
    """钥匙串 → 文件密钥回退(``localdb keys-unmigrate``;容器迁移,不验真门)。

    读钥匙串条目 → 明文件落盘(:func:`_write_key_cache_file`,600/目录 700
    ——消费侧 :func:`resolve_keys` 的 HMAC 验真门照跑,此处不重复设门)→
    回读一致才删条目(删失败如实呈态:双源并存同值,钥匙串仍优先)。

    Returns:
        ``{"keys_unmigrate": {db_count, file, migrated_at, keychain_entry_deleted,
        message}}``(形状级回执)。

    Raises:
        BridgeError: exit 21(条目缺位/通道不可用)、exit 1(形状不可解析/
        文件回读不一致)。
    """
    raw = keychain.read_item(keychain.DB_KEYS_ACCOUNT)
    if raw is None:
        raise BridgeError(
            KEY_UNAVAILABLE,
            "钥匙串条目缺位(或本机无钥匙串通道),无可回退",
            fix_hint=f"须先 localdb keys-migrate 建立条目 {keychain.DB_KEYS_ACCOUNT}",
        )
    mapping, migrated_at = keychain.parse_db_keys_envelope(raw)
    if mapping is None:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "钥匙串条目值形状不可解析,拒绝回退(宁缺毋假)",
            code="keychain_migration_failed",
        )
    path = _write_key_cache_file(mapping, data_root=data_root)
    if read_key_cache(data_root=data_root) != mapping:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "回退明文件回读不一致(钥匙串条目保留未删)",
            code="keychain_migration_failed",
        )
    deleted: bool
    try:
        deleted = keychain.delete_item(keychain.DB_KEYS_ACCOUNT)
    except BridgeError:
        deleted = False  # 删失败不毁整轮:双源并存同值(钥匙串仍优先),回执如实
    return {
        "keys_unmigrate": {
            "db_count": len(mapping),
            "file": str(path),
            "migrated_at": migrated_at,
            "keychain_entry_deleted": deleted,
            "message": (
                f"已回退为明文件: {path}({len(mapping)} 钥,600);"
                + ("钥匙串条目已删" if deleted else
                   "钥匙串条目删除失败(双源并存同值,钥匙串仍优先;可手动删)")
            ),
        }
    }


def resolve_keys(
    db_storage: Path,
    *,
    files_root: Path | None = None,
    key_db: Path | None = None,
    targets: list[tuple[str, int, bytes]] | None = None,
    data_root: Path | None = None,
    config: "BridgeConfig | None" = None,
) -> dict[str, str]:
    """密钥解析全链(D4 裁决②「外部密钥引入即闭合」的消费通路;query 入口)。

    顺序:① **macOS 钥匙串条目** ``myia/wechat/db-keys``(task
    10-14-wechat-keys-keychain;迁移态首选源,值 = keys.json 的 JSON 外壳)
    逐条 HMAC 重验,全量命中即放行;② ``keys.json`` 文件(缓存与外部供给
    同位:既可能是组件全量验证后的落盘,也可能是主人以任意可行手段提供的
    all_keys.json 类产物)同门重验——钥匙串未闭合/未迁移时文件兜底(兼容);
    ③ **外部取钥器**(B3,task 10-13-wechat-keyprovider):``key_provider_path``
    已配置时 :func:`acquire_keys_from_provider` 按协议 spawn 取钥——已配置 =
    首选取钥路(先于一切内置途径),**失败即 exit 21 不降级**(协议 §1「无
    降级」:绝不静默回退任何内置取钥实现,含下列钩子);④ 自愈钩子
    (0.4.0,task 10-13-wechat-key-subsystem):缓存缺位/未闭合且
    ``mem_search_enabled`` 开 + setuid keyscanner 在位时,零人工重取
    (:func:`wechat_bridge.memsearch.try_self_heal`,全量命中才落缓存;
    0.4.1 失败退避:未闭合落冷却戳,30 分钟窗内不重扫、零内存读);
    ⑤ 回落 E1 零内存途径(:func:`acquire_key`,当前如实负结论出口)。
    ①②④⑤未闭合会如实并入 exit 21 消息(放了钥匙串/keys.json 却被弃的
    排查者不再被零内存措辞带偏);③④冷却中同样如实注记(不谎称重取过);
    未配置取钥器时最终 exit 21 消息并入法定文案
    :data:`PROVIDER_UNCONFIGURED_MESSAGE`(协议 §8——用户知道 remedy 在哪)。

    Returns:
        dict: 加密库相对路径 → key hex(全部经 page1 离线验证)。

    Raises:
        BridgeError: exit 21(各源都未闭合;消息只承载形状,绝无材料)。
    """
    notes: list[str] = []
    staged_targets = targets if targets is not None else page1_targets(db_storage)
    # —— ① 钥匙串条目(迁移态首选源;缺席/未闭合 = 落到文件兜底)——
    staged, _stamp = read_db_keys_from_keychain(notes)
    if staged is not None:
        verified = verify_key_mapping(db_storage, staged, targets=staged_targets)
        if staged_targets and len(verified) == len(staged_targets):
            return verified
        notes.append(
            f"钥匙串条目在场({len(staged)}条)但全量验证未闭合:"
            f"命中 {len(verified)}/{len(staged_targets) if staged_targets else 0}库"
        )
    # —— ② 文件 keys.json(缓存与外部供给同位)——
    staged = read_key_cache(data_root=data_root)
    if staged is not None:
        verified = verify_key_mapping(db_storage, staged, targets=staged_targets)
        if staged_targets and len(verified) == len(staged_targets):
            try:  # 主人自放产物权限规整到 600(design §5.3;失败不拦查询)
                os.chmod(key_cache_path(data_root=data_root), 0o600)
            except OSError:
                pass
            return verified
        notes.append(
            f"keys.json 在场({len(staged)}条)但全量验证未闭合:"
            f"命中 {len(verified)}/{len(staged_targets) if staged_targets else 0}库"
        )
    # —— ③ 外部取钥器(B3;已配置 = 首选取钥路,先于内置自愈/零内存;失败
    # 即 exit 21 不降级——协议 §1:绝不静默回退内置取钥实现)——
    provider_path = _configured_provider_path(config)
    if provider_path:
        try:
            return acquire_keys_from_provider(
                db_storage, provider_path, targets=staged_targets, data_root=data_root
            )
        except BridgeError as exc:
            if not notes:
                raise
            raise BridgeError(
                KEY_UNAVAILABLE,
                f"{exc.message};另有:{'; '.join(notes)}",
                fix_hint=exc.fix_hint,
            ) from exc
    # —— ④ 自愈钩子(setuid keyscanner + 配置门开 → 零人工重取;未武装 = 保持现状;
    # 0.4.1 失败退避:未闭合落冷却戳,窗内不重扫、零内存读——不可闭合态
    # 不再逐次 query 重读微信全进程内存;冷却注记如实,不谎称重取过)——
    from . import memsearch  # 延迟导入:memsearch 顶导本模块,防循环

    if memsearch.self_heal_armed(config=config, data_root=data_root):
        cooldown = memsearch.self_heal_cooldown_remaining(data_root=data_root)
        if cooldown > 0:
            notes.append(
                "keyscanner 自愈冷却中(上次未闭合后 "
                f"{memsearch.SELF_HEAL_COOLDOWN_SECONDS / 60:.0f} 分钟内不重扫,"
                f"剩 {cooldown / 60:.0f} 分钟;冷却门不挡一键脚本/手动 key-scan)"
            )
        else:
            healed = memsearch.try_self_heal(
                db_storage, config=config, targets=staged_targets, data_root=data_root
            )
            if healed is not None:
                return healed
            notes.append("keyscanner 自愈未闭合(重取后缓存仍未全量命中)")
    try:
        return acquire_key(
            db_storage, files_root=files_root, key_db=key_db, targets=staged_targets
        )
    except BridgeError as exc:
        detail = (
            exc.message if not notes else f"{exc.message};另有:{'; '.join(notes)}"
        )
        raise BridgeError(
            KEY_UNAVAILABLE,
            f"{detail};{PROVIDER_UNCONFIGURED_MESSAGE}",
            fix_hint=(
                (f"{exc.fix_hint};" if exc.fix_hint else "")
                + "外部取钥器:wechat-bridge localdb key-provider set <取钥器可执行"
                "文件路径> 配置后查询自动取钥(协议文档 docs/wechat-keyprovider.md);"
                "keys.json 排查:键=相对 db_storage 的库路径,值=该库的 64-hex "
                "SQLCipher 密钥(逐条重验未命中 = 钥匙与库不匹配,登录态轮换后"
                "旧 key 失效,重取后覆盖重试)"
            ),
        ) from exc


# =====================================================================
# E2 解密副本(G5:TTL 24h + 容量上限 + 失败重建 + 源新即重建(0.4.4))
# =====================================================================

#: G4 三域 → 解密目标库(代码级映射;域清单配置可扩,未知域回落全目录)。
#: sns 域(10-13-wechat-sns-feed):DEFAULT_DOMAINS 不含它——query 命令的
#: 缺省解密面零变化,sns 副本只在 ``localdb sns`` 命令显式请求时解密。
DOMAIN_DB_FILES: dict[str, list[str]] = {
    "message": ["message/message_0.db", "message/biz_message_0.db"],
    "session": ["session/session.db"],
    "contact": ["contact/contact.db"],
    "sns": ["sns/sns.db"],
}


def copy_dir(*, data_root: Path | None = None) -> Path:
    """解密副本落点(数据根私有区 wechat-localdb/decrypted/)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / LOCALDB_PRIVATE_DIR / "decrypted"


def sqlcipher_available() -> bool:
    """sqlcipher CLI 在场性(design §5.1 安装前置;本机 2026-10-11 brew 装就)。"""
    return shutil.which("sqlcipher") is not None


def domain_targets(
    domains: list[str], db_storage: Path
) -> list[tuple[str, int]]:
    """按域清单(G4)展开解密目标(相对路径 + 源大小;小库优先)。"""
    selected: dict[str, int] = {}
    for domain in domains:
        known = DOMAIN_DB_FILES.get(domain)
        if known is not None:
            rels = known
        else:  # 配置扩展域:目录内全部顶层 .db(小库优先,容量上限兜底)
            base = db_storage / domain
            rels = (
                sorted(
                    (f.relative_to(db_storage).as_posix() for f in base.glob("*.db")),
                    key=lambda rel: (db_storage / rel).stat().st_size,
                )
                if base.is_dir()
                else []
            )
        for rel in rels:
            path = db_storage / rel
            if path.is_file() and rel not in selected:
                selected[rel] = path.stat().st_size
    return sorted(selected.items(), key=lambda item: item[1])


def _run_sqlcipher_decrypt(
    enc_path: Path, plain_path: Path, key_hex: str, *, timeout: float = SQLCIPHER_TIMEOUT_SECONDS
) -> None:
    """sqlcipher CLI 解密单库(SQL 走 stdin,密钥材料零 argv 暴露)。"""
    sql = (
        f'PRAGMA key = "x\'{key_hex}\'";\n'
        f"ATTACH DATABASE '{plain_path.as_posix()}' AS plain KEY '';\n"
        "SELECT sqlcipher_export('plain');\n"
        "DETACH plain;\n"
    )
    try:
        result = subprocess.run(  # noqa: S603 - 字面量命令,无外壳
            ["sqlcipher", enc_path.as_posix()],
            input=sql.encode("utf-8"),
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise BridgeError(
            DECRYPT_FAILED,
            "sqlcipher 不在场(解密副本前置缺失;design §5.1 不静默半装)",
            fix_hint="brew install sqlcipher 后重试(组件安装前置)",
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            DECRYPT_FAILED,
            f"sqlcipher 解密超时(>{timeout:.0f}s,已 kill): {enc_path.name}",
        ) from exc
    if result.returncode != 0 or not plain_path.is_file():
        stderr_lines = len(result.stderr.splitlines())
        raise BridgeError(
            DECRYPT_FAILED,
            f"sqlcipher 解密失败(exit={result.returncode},stderr {stderr_lines} 行): "
            f"{enc_path.name}(key 与库不匹配或库形漂移 → 副本重建流程)",
            fix_hint="重取密钥后重建副本(G5:解密失败即触发重建)",
        )


def _source_newer(db_storage: Path, rel: str, copy_mtime: float) -> bool:
    """源库(含 ``-wal``)是否比副本新(0.4.4 近实时:微信写库后下轮查询即见)。

    只读 ``stat`` 零打开;``-wal`` 缺席只看主库。源消失(极端:账号目录
    迁走)返回 False——留着既有副本供查询,不炸整轮。
    """
    source = db_storage / rel
    try:
        newest = source.stat().st_mtime
    except OSError:
        return False
    wal = db_storage / (rel + "-wal")
    try:
        if wal.is_file():
            newest = max(newest, wal.stat().st_mtime)
    except OSError:  # stat 竞态(拷贝瞬间被删):以主库时间为据
        pass
    return newest > copy_mtime


def ensure_decrypted_copies(
    db_storage: Path,
    keys: dict[str, str],
    *,
    domains: list[str],
    ttl_hours: int,
    capacity_mb: int,
    data_root: Path | None = None,
    now: float | None = None,
    runner: Callable[[Path, Path, str], None] | None = None,
) -> dict[str, object]:
    """E2 副本生命周期(G5):TTL 失效重建 + 容量上限 + 失败重建 + 源新即重建。

    逐库:新鲜副本(存在、mtime 在 TTL 内、**且不比源库(含 ``-wal``)
    旧)保留;TTL 过期/缺失/上次失败/**源库有新写入** → 重建(加密原件
    db+-wal 先拷入私有 staging,sqlcipher 解密,产物 600,staging 用完即
    清)。**TTL=0 = 永不过期**(config ``copy_ttl_hours`` 语义:恒新鲜、
    跳过重建;负数在装载期已拒)。累计解密体积超 ``capacity_mb`` 的库跳过
    并如实记录(跳过原因 capacity);无 key 的库跳过(reason no_key)。

    **并发单飞(0.4.4)**:同数据根的并发查询(*/2 双源同轮并发 fetch)
    会在共享 staging 用同名 ``.enc`` 互相覆盖,做出 db+wal 不一致对
    (实测:每轮恰一源 decrypt_failed)。整轮重建以 ``.rebuild.lock``
    排他锁串行;后来者在锁内重估新鲜度,通常直接复用先到者刚建好的
    副本(重建工作也被去重)。

    Returns:
        形状级应答节:{"dir","built","kept","skipped","total_bytes"}。
    """
    target_dir = copy_dir(data_root=data_root)
    target_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(target_dir, 0o700)
    lock_fh = open(target_dir / ".rebuild.lock", "a")  # 700 目录内,600 由 umask 缺省
    try:
        fcntl.flock(lock_fh, fcntl.LOCK_EX)
        return _ensure_decrypted_copies_locked(
            db_storage,
            keys,
            domains=domains,
            ttl_hours=ttl_hours,
            capacity_mb=capacity_mb,
            data_root=data_root,
            now=now,
            runner=runner,
        )
    finally:
        lock_fh.close()


def _ensure_decrypted_copies_locked(
    db_storage: Path,
    keys: dict[str, str],
    *,
    domains: list[str],
    ttl_hours: int,
    capacity_mb: int,
    data_root: Path | None = None,
    now: float | None = None,
    runner: Callable[[Path, Path, str], None] | None = None,
) -> dict[str, object]:
    target_dir = copy_dir(data_root=data_root)
    target_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(target_dir, 0o700)
    current_time = time.time() if now is None else now
    built: list[str] = []
    kept: list[str] = []
    skipped: list[dict[str, str]] = []
    total_bytes = 0
    capacity_bytes = capacity_mb * 1024 * 1024

    for rel, source_size in domain_targets(domains, db_storage):
        key_hex = keys.get(rel)
        if key_hex is None:
            skipped.append({"rel": rel, "reason": "no_key"})
            continue
        if total_bytes + source_size > capacity_bytes:
            skipped.append({"rel": rel, "reason": "capacity"})
            continue
        plain_path = target_dir / rel
        fresh = plain_path.is_file() and (
            ttl_hours == 0  # 0 = 永不过期:陈旧副本也恒新鲜,跳过重建
            or (
                (current_time - plain_path.stat().st_mtime) < ttl_hours * 3600
                and not _source_newer(db_storage, rel, plain_path.stat().st_mtime)
            )
        )
        if fresh:
            kept.append(rel)
            total_bytes += plain_path.stat().st_size
            continue
        plain_path.parent.mkdir(parents=True, exist_ok=True)
        os.chmod(plain_path.parent, 0o700)
        if plain_path.exists():
            plain_path.unlink()  # 上次失败/过期的残留,重建前清除
        staging = target_dir / ".staging"
        staging.mkdir(parents=True, exist_ok=True)
        os.chmod(staging, 0o700)
        enc_copy = staging / (plain_path.name + ".enc")
        try:
            # 活库拷贝竞态(0.4.4):微信持续写库,db+wal 两段拷贝非原子,
            # 偶发不一致对 → sqlcipher 解密失败;原样重拷一次再试(竞态窗
            # 毫秒级,两连败概率平方级衰减;真键错/真损坏则两次同败照实抛)。
            for attempt in (1, 2):
                try:
                    shutil.copyfile(db_storage / rel, enc_copy)
                    os.chmod(enc_copy, 0o600)
                    wal = db_storage / (rel + "-wal")
                    if wal.is_file():
                        shutil.copyfile(wal, enc_copy.with_suffix(enc_copy.suffix + "-wal"))
                        os.chmod(enc_copy.with_suffix(enc_copy.suffix + "-wal"), 0o600)
                    encrypt_run = runner if runner is not None else _run_sqlcipher_decrypt
                    encrypt_run(enc_copy, plain_path, key_hex)
                    break
                except BridgeError:
                    if attempt == 2:
                        raise
        finally:
            shutil.rmtree(staging, ignore_errors=True)
        if not plain_path.is_file():
            raise BridgeError(
                DECRYPT_FAILED,
                f"解密副本未产出(注入 runner 未落产物?): {rel}",
            )
        os.chmod(plain_path, 0o600)
        built.append(rel)
        total_bytes += plain_path.stat().st_size

    return {
        "dir": str(target_dir),
        "built": built,
        "kept": kept,
        "skipped": skipped,
        "total_bytes": total_bytes,
    }


# =====================================================================
# E3 编排(query 层本体在 localdb_query.py;此处只做装配)
# =====================================================================


def query_history(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    chat_id: str,
    since_days: int,
    *,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """``localdb query`` 全链编排:E2 副本 → E3 三域只读查询(G4)。

    自愈钩子(0.4.0):E2 解密失败(密钥失效形状,如登录态轮换 G5)且
    setuid keyscanner 在位 + 配置门开时,零人工重取一次(:func:
    ``wechat_bridge.memsearch.try_self_heal`)并重建副本;未武装/未闭合 =
    原样透传 decrypt_failed(诚实,不吞)。0.4.1 失败退避:未闭合落
    冷却戳,窗内(30 分钟)解密失败不再重扫,原样透传。
    """
    from . import localdb_query, memsearch

    def _ensure(keys_mapping: dict[str, str]) -> dict[str, object]:
        return ensure_decrypted_copies(
            db_storage,
            keys_mapping,
            domains=config.domains,
            ttl_hours=config.copy_ttl_hours,
            capacity_mb=config.copy_capacity_mb,
            data_root=data_root,
            now=now,
        )

    try:
        copy_info = _ensure(keys)
    except BridgeError as exc:
        if exc.exit_code != DECRYPT_FAILED:
            raise
        if not memsearch.self_heal_armed(config=config, data_root=data_root):
            raise  # 未安装自愈件 = 保持现状(指引一键脚本)
        healed = memsearch.try_self_heal(db_storage, config=config, data_root=data_root)
        if healed is None:
            raise  # 自愈未闭合:原样透传,不制造半真状态
        keys = healed
        copy_info = _ensure(keys)

    return localdb_query.run_query(
        copy_dir=Path(str(copy_info["dir"])),
        domains=config.domains,
        chat_id=chat_id,
        since_days=since_days,
        limit=config.messages,
        copy_info=copy_info,
    )


def sns_history(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    mode: str,
    since_days: int,
    *,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """``localdb sns feed|notices`` 全链编排(task 10-13-wechat-sns-feed)。

    与 :func:`query_history` 同构:E2 副本(feed 域 ``["sns", "contact"]``——
    contact 供 nickname 反查;**notices 域收缩 ``["sns"]``**,grill 深化批:
    通知的 from_nickname 是 SQL 直列不消费 contact,而微信持续写 contact
    会触发「源新即重建」——*/2 频率的通知源不该反复重解 32MB 的 contact
    副本)→ 解密失败自愈钩子同款(setuid keyscanner 在位+门开 = 零人工
    重取一次)→ E3 :func:`wechat_bridge.sns_query.run_sns_query` 装配。
    """
    from . import memsearch, sns_query

    domains = ["sns", "contact"] if mode == "feed" else ["sns"]

    def _ensure(keys_mapping: dict[str, str]) -> dict[str, object]:
        return ensure_decrypted_copies(
            db_storage,
            keys_mapping,
            domains=domains,
            ttl_hours=config.copy_ttl_hours,
            capacity_mb=config.copy_capacity_mb,
            data_root=data_root,
            now=now,
        )

    try:
        copy_info = _ensure(keys)
    except BridgeError as exc:
        if exc.exit_code != DECRYPT_FAILED:
            raise
        if not memsearch.self_heal_armed(config=config, data_root=data_root):
            raise
        healed = memsearch.try_self_heal(db_storage, config=config, data_root=data_root)
        if healed is None:
            raise
        keys = healed
        copy_info = _ensure(keys)

    return sns_query.run_sns_query(
        copy_dir=Path(str(copy_info["dir"])),
        mode=mode,
        since_days=since_days,
        copy_info=copy_info,
    )


def group_info(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    chat_id: str,
    *,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """``localdb group-info`` 全链编排(task 10-13-wechat-groupinfo)。

    与 :func:`sns_history` 同构:E2 副本(域固定 ``["contact"]``——群信息
    单 contact 域自足:chat_room/chat_room_info_detail/chatroom_member 全在
    contact 库,member_id 即 contact rowid(2026-10-13 实拍裁决,见
    localdb_query._contact_rowid_usernames),显示名同库直查;**不带
    message/session**,零消息域解密成本)→ 解密失败自愈钩子同款(setuid
    keyscanner 在位+门开 = 零人工重取一次)→ E3
    :func:`localdb_query.group_info` 装配。查询层缺表/缺域恒降级空结构不判错
    (判例同 key-status:状态查询不判错)。
    """
    from . import localdb_query, memsearch

    def _ensure(keys_mapping: dict[str, str]) -> dict[str, object]:
        return ensure_decrypted_copies(
            db_storage,
            keys_mapping,
            domains=["contact"],
            ttl_hours=config.copy_ttl_hours,
            capacity_mb=config.copy_capacity_mb,
            data_root=data_root,
            now=now,
        )

    try:
        copy_info = _ensure(keys)
    except BridgeError as exc:
        if exc.exit_code != DECRYPT_FAILED:
            raise
        if not memsearch.self_heal_armed(config=config, data_root=data_root):
            raise
        healed = memsearch.try_self_heal(db_storage, config=config, data_root=data_root)
        if healed is None:
            raise
        keys = healed
        copy_info = _ensure(keys)

    return localdb_query.group_info(
        copy_dir=Path(str(copy_info["dir"])),
        chat_id=chat_id,
    )


def _ensure_copies_with_self_heal(
    config,  # BridgeConfig(鸭子类型;避免循环导入)
    db_storage: Path,
    keys: dict[str, str],
    domains: list[str],
    *,
    data_root: Path | None = None,
    now: float | None = None,
) -> tuple[dict[str, object], dict[str, str]]:
    """E2 副本 + 解密失败自愈钩子(与 :func:`query_history` 同构;task
    10-14-wechat-http-api R4 终位平移,httpapi 经 import 消费)。

    Returns:
        ``(copy_info, 实际生效 keys)``——自愈成功后以新 keys 重建的副本
        供后续查询消费(与 query_history 的 keys 重指派同款)。
    """
    from . import memsearch

    def _ensure(keys_mapping: dict[str, str]) -> dict[str, object]:
        return ensure_decrypted_copies(
            db_storage,
            keys_mapping,
            domains=domains,
            ttl_hours=config.copy_ttl_hours,
            capacity_mb=config.copy_capacity_mb,
            data_root=data_root,
            now=now,
        )

    try:
        return _ensure(keys), keys
    except BridgeError as exc:
        if exc.exit_code != DECRYPT_FAILED:
            raise
        if not memsearch.self_heal_armed(config=config, data_root=data_root):
            raise  # 未安装自愈件 = 保持现状(与 query_history 同判)
        healed = memsearch.try_self_heal(db_storage, config=config, data_root=data_root)
        if healed is None:
            raise  # 自愈未闭合:原样透传,不制造半真状态
        return _ensure(healed), healed


def sessions_list(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    limit: int,
    *,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """会话清单全链编排(task 10-14-wechat-http-api R4;PRD 终位 = 本函数,
    httpapi 经 ``from .localdb import sessions_list`` 消费)。与
    :func:`query_history` 同构:确保 ``[session, contact]`` 域副本 →
    :func:`localdb_query.list_sessions`。

    应答即编排载荷(HTTP 应答=CLI 载荷同源):``{"sessions":[…],
    "domains":{…},"copy":{…}}``。
    """
    from . import localdb_query

    copy_info, _keys = _ensure_copies_with_self_heal(
        config, db_storage, keys, ["session", "contact"],
        data_root=data_root, now=now,
    )
    copy_dir = Path(str(copy_info["dir"]))
    rel_map = {"session": "session/session.db", "contact": "contact/contact.db"}
    domain_status = {
        domain: ("ok" if (copy_dir / rel).is_file() else "copy_missing")
        for domain, rel in rel_map.items()
    }
    con = localdb_query._open_copy(copy_dir, "session/session.db")
    if con is None:
        raise BridgeError(
            DECRYPT_FAILED,
            "session 域解密副本不可用(副本缺失或损坏;G5 重建流程未产出可用库)",
            fix_hint="重试触发副本重建;持续失败先核密钥与 sqlcipher(design §5.1)",
        )
    try:
        sessions = localdb_query.list_sessions(con, int(limit))
    finally:
        con.close()
    return {"sessions": sessions, "domains": domain_status, "copy": copy_info}


def page_history(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    chat_id: str,
    *,
    cursor: str | None = None,
    limit: int | None = None,
    asc: bool | None = None,
    from_ts: int | None = None,
    to_ts: int | None = None,
    types: list[str] | None = None,
    sender: str | None = None,
    data_root: Path | None = None,
) -> dict[str, object]:
    """``localdb page`` 全链编排(task 10-14-wechat-chat-export R1)。

    与 :func:`query_history` 同构:E2 副本(域 ``["message", "contact"]``——
    contact 供 wxid→显示名解析)→ 解密失败自愈钩子同款(setuid keyscanner
    在位+门开 = 零人工重取一次)→ E3 :func:`localdb_page.run_page`;尾部经
    :func:`localdb_query._contact_pick_names` 批量解析 wxid→显示名(remark>
    nickname>alias)回填消息 sender 与会话 display_name(未命中维持 wxid,
    陌生群成员如实)。``invalid_cursor`` / ``invalid_types``(exit 2)由
    run_page/decode_cursor/type_filter_values 抛,本层不吞。
    """
    from . import localdb_page, localdb_query

    copy_info, keys = _ensure_copies_with_self_heal(
        config, db_storage, keys, ["message", "contact"], data_root=data_root
    )
    copy_dir = Path(str(copy_info["dir"]))
    payload = localdb_page.run_page(
        copy_dir,
        chat_id,
        cursor=cursor,
        limit=limit,
        asc=asc,
        from_ts=from_ts,
        to_ts=to_ts,
        types=types,
        sender=sender,
    )
    page = payload.get("page")
    messages = page.get("messages") if isinstance(page, dict) else None
    names: dict[str, str] = {}
    if isinstance(messages, list):
        wanted = [chat_id] + [
            message.get("sender_id")
            for message in messages
            if isinstance(message, dict)
            and isinstance(message.get("sender_id"), str)
        ]
        contact_con = localdb_query._open_copy(copy_dir, "contact/contact.db")
        try:
            if contact_con is not None:
                names = localdb_query._contact_pick_names(contact_con, wanted)
        finally:
            if contact_con is not None:
                contact_con.close()
    if names and isinstance(page, dict):
        for message in messages or []:
            if not isinstance(message, dict):
                continue
            wxid = message.get("sender_id")
            if isinstance(wxid, str) and wxid in names:
                message["sender"] = names[wxid]
        if chat_id in names:
            page["display_name"] = names[chat_id]
    return payload


def export_history(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    chat_id: str | None,
    *,
    fmt: str,
    out_dir: Path,
    from_ts: int | None = None,
    to_ts: int | None = None,
    types: list[str] | None = None,
    sender: str | None = None,
    display_name_pref: str = "remark-first",
    name_mode: str = "classic",
    all_chats: bool = False,
    progress=None,
    data_root: Path | None = None,
) -> dict[str, object]:
    """``localdb export`` 全链编排(task 10-14-wechat-chat-export R2/R4)。

    与 :func:`page_history` 同构:E2 副本(域 ``["message", "contact"]``)
    → 解密失败自愈钩子 → :func:`localdb_export.run_export`(staging → 流式
    写 → manifest 对账 → 原子落位;143 ``export_cancelled`` / usage 族由
    run_export 抛,本层不吞)。``progress`` = CLI 侧单行 JSON 打印器
    (NDJSON 转印判例 key-acquire)。
    """
    from . import localdb_export

    copy_info, keys = _ensure_copies_with_self_heal(
        config, db_storage, keys, ["message", "contact"], data_root=data_root
    )
    return localdb_export.run_export(
        Path(str(copy_info["dir"])),
        chat_id,
        out_dir,
        fmt=fmt,
        from_ts=from_ts,
        to_ts=to_ts,
        types=types,
        sender=sender,
        display_name_pref=display_name_pref,
        name_mode=name_mode,
        all_chats=all_chats,
        progress=progress,
    )


def contacts_inventory(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    *,
    type_filter: str | None = None,
    keyword: str | None = None,
    limit: int = 100,
    cursor: str | None = None,
    with_residue: bool = False,
    include_stranger: bool = True,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """``localdb contacts`` 全链编排(task 10-14-wechat-contacts R1;镜像
    :func:`group_info` 同构)。域收缩纪律(AC9):``with_residue`` 才带
    message 域(找回考古要消息残迹),否则 contact 单域;缺表降级恒
    exit 0(判例同 key-status)。尾调 :func:`contacts_query.contacts_page`。
    """
    from . import contacts_query

    domains = ["contact", "message"] if with_residue else ["contact"]
    copy_info, keys = _ensure_copies_with_self_heal(
        config, db_storage, keys, domains, data_root=data_root, now=now
    )
    return contacts_query.contacts_page(
        Path(str(copy_info["dir"])),
        type_filter=type_filter,
        keyword=keyword,
        limit=limit,
        cursor=cursor,
        with_residue=with_residue,
        include_stranger=include_stranger,
    )


def conversations_census(
    config,  # BridgeConfig(避免循环导入,运行时鸭子类型)
    db_storage: Path,
    keys: dict[str, str],
    *,
    limit: int | None = None,
    data_root: Path | None = None,
) -> dict[str, object]:
    """``localdb conversations`` 全链编排(task 10-14-wechat-chat-export
    R2;集成侧补的最小编排,与 page_history 同族)。E2 副本(域
    ``["message", "contact"]``)→ 自愈钩子 → :func:`localdb_page.
    run_conversations`(逐表 COUNT/MIN/MAX 普查 + contact 显示名解析,
    副本指纹缓存)。清单截断(缺省 500/帽 5000)在 run_conversations。
    """
    from . import localdb_page

    copy_info, keys = _ensure_copies_with_self_heal(
        config, db_storage, keys, ["message", "contact"], data_root=data_root
    )
    return localdb_page.run_conversations(
        Path(str(copy_info["dir"])), limit=limit
    )


# 静态对账:本地库族码值与 codes 表一致(改码先改 design §6)。
assert DB_NOT_FOUND == 20 and KEY_UNAVAILABLE == 21 and DECRYPT_FAILED == 22
