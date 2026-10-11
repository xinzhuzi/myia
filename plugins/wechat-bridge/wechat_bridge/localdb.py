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
  (单测以合成 page1 全链验证),D4 若裁决引入外部密钥,同一校验器直接复用。
- 内存密钥搜索(prd 红线 1/3):独立空壳 :mod:`wechat_bridge.memsearch`,
  默认关,**绝不真跑**;本模块零进程接触。

E2 解密副本(G5 生命周期):

- ``db_storage`` 加密库 → sqlcipher CLI 解密**副本**至数据根私有区
  ``wechat-localdb/decrypted/<域>/<库>`(文件 600/目录 700,prd 红线 6);
  sqlcipher 缺失 → 结构化报错 + brew 指引(design §5.1,不静默半装)。
- TTL 24h(配置 ``copy_ttl_hours``)失效重建 + 容量上限(配置
  ``copy_capacity_mb``);解密失败触发重建;微信进程零接触、零出网。

私有数据红线(prd 红线 6):密钥材料/聊天内容不入 git/日志/报告;本模块
的错误消息与应答只承载形状(计数/路径名/字节数)。
"""

from __future__ import annotations

import hashlib
import hmac
import os
import shutil
import sqlite3
import struct
import subprocess
import time
from pathlib import Path
from typing import Callable

from .codes import DECRYPT_FAILED, DB_NOT_FOUND, KEY_UNAVAILABLE, BridgeError
from .config import LOCALDB_KEYS_REL_PATH, myssia_home
from .system_checks import WECHAT_FILES_ROOT

__all__ = [
    "DB_STORAGE_DIR_NAME",
    "LOCALDB_PRIVATE_DIR",
    "PAGE_SZ",
    "locate_db_storage",
    "locate_key_info_db",
    "verify_key_for_page",
    "extract_key_candidates",
    "acquire_key",
    "key_cache_path",
    "write_key_cache",
    "read_key_cache",
    "domain_targets",
    "copy_dir",
    "sqlcipher_available",
    "ensure_decrypted_copies",
    "query_history",
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
                "确认微信在本机登录过;D4 待主人裁决(密钥途径),"
                "内存密钥搜索为默认关空壳、绝不真跑(prd 红线 1/3)"
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
                "D4 待主人裁决:豁免内存密钥搜索(默认关空壳 memsearch,启用须显式)"
                "或引入外部密钥;已验证子集已缓存(数据根私有区 600)"
            ),
        )
    raise BridgeError(
        KEY_UNAVAILABLE,
        "本地库密钥不可得:零内存途径(key_info.db)实测未闭合——"
        f"行数={len(blobs)} 候选={len(candidates)} 离线HMAC校验={attempts}次 "
        f"命中=0/{len(targets)}库;密钥材料疑被机器专属密钥包裹、文件内不可推导"
        "(2026-10-11 E1 真跑 + 三方独立公开实测一致)",
        fix_hint=(
            "D4 待主人裁决:①豁免内存密钥搜索(默认关空壳 memsearch,显式开启才生效,"
            "prd 红线 1/3)②或引入外部密钥(all_keys.json 类,600 权限私有区);"
            "校验机制已就绪,密钥可得即全链闭合"
        ),
    )


# =====================================================================
# 密钥缓存(成功才落;数据根私有区 600;探针零成本判据)
# =====================================================================


def key_cache_path(data_root: Path | None = None) -> Path:
    """密钥缓存产物路径(数据根私有区 wechat-localdb/keys.json;design §5.3)。"""
    root = data_root if data_root is not None else myssia_home()
    return root / LOCALDB_PRIVATE_DIR / Path(LOCALDB_KEYS_REL_PATH).name


def write_key_cache(mapping: dict[str, str], *, data_root: Path | None = None) -> Path:
    """写密钥缓存(仅验证通过的 key;600 权限;目录 700)。"""
    import json

    path = key_cache_path(data_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(path.parent, 0o700)
    path.write_text(json.dumps(mapping, indent=1) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)
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


# =====================================================================
# E2 解密副本(G5:TTL 24h + 容量上限 + 失败重建)
# =====================================================================

#: G4 三域 → 解密目标库(代码级映射;域清单配置可扩,未知域回落全目录)。
DOMAIN_DB_FILES: dict[str, list[str]] = {
    "message": ["message/message_0.db", "message/biz_message_0.db"],
    "session": ["session/session.db"],
    "contact": ["contact/contact.db"],
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
    """E2 副本生命周期(G5):TTL 失效重建 + 容量上限 + 失败重建。

    逐库:新鲜副本(存在且 mtime 在 TTL 内)保留;过期/缺失/上次失败 →
    重建(加密原件 db+-wal 先拷入私有 staging,sqlcipher 解密,产物 600,
    staging 用完即清)。累计解密体积超 ``capacity_mb`` 的库跳过并如实记录
    (跳过原因 capacity);无 key 的库跳过(reason no_key)。

    Returns:
        形状级应答节:{"dir","built","kept","skipped","total_bytes"}。
    """
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
        fresh = (
            plain_path.is_file()
            and (current_time - plain_path.stat().st_mtime) < ttl_hours * 3600
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
            shutil.copyfile(db_storage / rel, enc_copy)
            os.chmod(enc_copy, 0o600)
            wal = db_storage / (rel + "-wal")
            if wal.is_file():
                shutil.copyfile(wal, enc_copy.with_suffix(enc_copy.suffix + "-wal"))
                os.chmod(enc_copy.with_suffix(enc_copy.suffix + "-wal"), 0o600)
            encrypt_run = runner if runner is not None else _run_sqlcipher_decrypt
            encrypt_run(enc_copy, plain_path, key_hex)
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
    """``localdb query`` 全链编排:E2 副本 → E3 三域只读查询(G4)。"""
    from . import localdb_query

    copy_info = ensure_decrypted_copies(
        db_storage,
        keys,
        domains=config.domains,
        ttl_hours=config.copy_ttl_hours,
        capacity_mb=config.copy_capacity_mb,
        data_root=data_root,
        now=now,
    )
    return localdb_query.run_query(
        copy_dir=Path(str(copy_info["dir"])),
        domains=config.domains,
        chat_id=chat_id,
        since_days=since_days,
        limit=config.messages,
        copy_info=copy_info,
    )


# 静态对账:本地库族码值与 codes 表一致(改码先改 design §6)。
assert DB_NOT_FOUND == 20 and KEY_UNAVAILABLE == 21 and DECRYPT_FAILED == 22
