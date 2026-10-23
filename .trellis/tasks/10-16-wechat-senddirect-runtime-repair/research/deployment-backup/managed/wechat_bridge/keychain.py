"""桥内最小 macOS 钥匙串读写(task 10-14-wechat-keys-keychain;零新 pip 依赖)。

主人令(2026-10-14):密钥是保密数据,本地保存应加密——keys.json 明文面
收进钥匙串,桥读取两级化(钥匙串优先、文件兜底)。本模块是桥侧的**最小**
钥匙串通道:不 import myssia(桥是独立包),不用 keyring 库(零新依赖),
直接子进程 ``security`` CLI,与 MYIA 本体 :mod:`myssia.secrets` 的既有
``myia/*`` 条目族同命名位:

- service = ``myia``;account = ``myia/<scope>/<name>`` 全名(myssia 同款:
  ``security find-generic-password -s myia -a myia/wechat/db-keys`` 命中;
  Keychain Access 里与 MYIA 其余凭据同组,myssia 的 list 枚举也天然可见)。
- 本桥两条目:``myia/wechat/db-keys``(值 = 完整 keys.json 的 JSON 外壳,
  见 :data:`MIGRATED_AT_FIELD`)与 ``myia/wechat/passphrase``(取钥蓝本
  passphrase,由部署件 keyprovider_wrap.py 搬运,本模块只提供通道)。

token 零外显纪律(桥惯例,红线 6 同源):

- **读** = ``find-generic-password … -w``,值走 stdout 管道捕获,argv
  永不携带值;缺席 = exit 44 → None 如实。
- **写** = ``security -i`` 交互命令模式:命令行(含值,JSON 引号转义)经
  **stdin 管道**喂入——不在 OS argv(``ps`` 零暴露),不在环境。长值硬前提:
  裸 ``-w`` 提示形态(password+retype 双行)经管道 stdin 时 **128 字节截断**
  (2026-10-14 本机实测:500/1000/2000/4000B 全部落成 128B),密钥外壳
  (~2KB)必须走 ``-i`` 内联形态(2107B 外壳逐字节回读一致实测)。``-i``
  解析器认 JSON 式引号/反斜杠转义、**不认 U 转义序列与裸多字节 UTF-8**
  (实测 mojibake),故值必须纯 ASCII——:func:`build_db_keys_envelope` 用
  ``ensure_ascii`` 钉死(JSON 层转义,材料里的非 ASCII 路径照样往返)。

钥匙串条目没有 mtime 可取——``db-keys`` 条目的值是 JSON 外壳
``{"migrated_at": <ISO>, "keys": {…}}``,时间戳随写入刷新(key-status 的
acquired_at 语义据此不谎);缺外壳的裸 {rel: hex} 映射按防御性兼容读取
(手工放置/旧形态),migrated_at = None 如实。

测试态(pytest):函数调用时发现 ``PYTEST_CURRENT_TEST`` 在环境里 → 自动
改用**进程内伪钥匙串**(:data:`_FAKE_STORE`),真钥匙串零触碰(判例 =
myssia.secrets.InMemoryKeychainBackend「mock 钥匙串,零真实触碰」);
专测 ``security`` argv/stdin 形态时 monkeypatch 掉该 env + subprocess。
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from typing import Any

from .codes import EXIT_GENERIC_FAILURE, BridgeError

__all__ = [
    "DB_KEYS_ACCOUNT",
    "KEYCHAIN_SERVICE",
    "MIGRATED_AT_FIELD",
    "PASSPHRASE_ACCOUNT",
    "SECURITY_NOT_FOUND_EXIT",
    "SECURITY_TIMEOUT_SECONDS",
    "build_db_keys_envelope",
    "delete_item",
    "fake_store",
    "keychain_available",
    "parse_db_keys_envelope",
    "read_item",
    "reset_fake_store",
    "write_item",
]

#: 全部条目的 service(MYIA 凭据命名族;myssia.secrets.SECRET_SERVICE 同值)。
KEYCHAIN_SERVICE = "myia"
#: 微信库密钥映射条目(值 = :func:`build_db_keys_envelope` 的 JSON 外壳)。
DB_KEYS_ACCOUNT = "myia/wechat/db-keys"
#: 取钥蓝本 passphrase 条目(部署件 keyprovider_wrap.py 消费)。
PASSPHRASE_ACCOUNT = "myia/wechat/passphrase"
#: 外壳里的写入时间字段(条目无 mtime,写入即刷新;key-status acquired_at 源)。
MIGRATED_AT_FIELD = "migrated_at"
#: ``security find`` 的「条目不存在」退出码(其余非 0 = 硬失败,如实抛)。
SECURITY_NOT_FOUND_EXIT = 44
#: security 子进程预算(秒;钥匙串交互本地即答,拖满即异常形态)。
SECURITY_TIMEOUT_SECONDS = 15.0

#: pytest 态的进程内伪钥匙串(account → value;None = 未激活)。函数调用时
#: 惰性判 ``PYTEST_CURRENT_TEST`` 决定走伪库还是真 ``security`` 子进程。
_FAKE_STORE: dict[str, str] | None = None


def _fake_active() -> bool:
    """本次调用是否落在 pytest 测试态(真钥匙串零触碰的缺省门)。"""
    return os.environ.get("PYTEST_CURRENT_TEST") is not None


def fake_store() -> dict[str, str]:
    """取(并惰性激活)伪钥匙串(测试态专用;非 pytest 调用 = 编程错)。"""
    global _FAKE_STORE
    if _FAKE_STORE is None:
        _FAKE_STORE = {}
    return _FAKE_STORE


def reset_fake_store() -> None:
    """清伪钥匙串(测试 setup/teardown 双清,防跨用例/跨文件残留)。"""
    global _FAKE_STORE
    _FAKE_STORE = {}


def keychain_available() -> bool:
    """本机是否有 security CLI 钥匙串通道(非 darwin / CLI 缺位 = False)。"""
    if _fake_active():
        return True
    return sys.platform == "darwin" and shutil.which("security") is not None


def read_item(account: str) -> str | None:
    """读一条 generic-password(值走 stdout 管道;缺席 = None 如实)。

    钥匙串通道不可用(非 darwin / CLI 缺位)= None(「源缺席」语义,
    resolve_keys 兜底链不受影响);其余非 44 失败(锁死/损坏)如实抛
    BridgeError(通用失败段,消息只承载形状,绝无值)。
    """
    if not keychain_available():
        return None
    if _fake_active():
        return fake_store().get(account)
    try:
        result = subprocess.run(  # noqa: S603 - 字面量 security CLI,无外壳
            [
                "security", "find-generic-password",
                "-s", KEYCHAIN_SERVICE,
                "-a", account,
                "-w",
            ],
            capture_output=True,
            text=True,
            timeout=SECURITY_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"钥匙串读取子进程异常({type(exc).__name__}): account={account}",
            code="keychain_operation_failed",
        ) from exc
    if result.returncode == SECURITY_NOT_FOUND_EXIT:
        return None
    if result.returncode != 0:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"钥匙串读取失败(exit={result.returncode}): account={account}",
            code="keychain_operation_failed",
            fix_hint="钥匙串可能被锁(钥匙串访问.app 解锁 login 钥匙串)后重试",
        )
    value = result.stdout
    if value.endswith("\n"):
        value = value[:-1]  # find -w 的行尾换行(恰一枚;值本身零换行,写入门已拒)
    return value


def write_item(account: str, value: str) -> None:
    """写一条 generic-password(-U 在场即覆写;``security -i`` 内联形态,argv 零值)。

    钥匙串通道不可用 = 如实抛(写路径不容静默降级);值含换行/非 ASCII =
    拒(``-i`` 解析器硬前提:换行破命令行形态,非 ASCII 被 mojibake——
    :func:`build_db_keys_envelope` 的 ensure_ascii 已钉死 ASCII 面)。
    """
    if not keychain_available():
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"本机无钥匙串通道(须 macOS + security CLI),无法写入: account={account}",
            code="keychain_backend_unavailable",
        )
    if "\n" in value or not value.isascii():
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "钥匙串写入值含换行或非 ASCII 字符(security -i 通道硬前提不支持): "
            f"account={account}",
            code="keychain_operation_failed",
        )
    if _fake_active():
        fake_store()[account] = value
        return
    # security -i:命令行经 stdin 管道(值内联,JSON 引号转义)——OS argv 与
    # 环境零值;裸 -w 提示形态 128B 截断(模块 docstring 实测),长外壳必走此路。
    command = (
        f"add-generic-password -U -s {KEYCHAIN_SERVICE} -a {account}"
        f" -w {json.dumps(value)}\n\n"
    )
    try:
        result = subprocess.run(  # noqa: S603 - 字面量 security CLI,无外壳
            ["security", "-i"],
            input=command,
            capture_output=True,
            text=True,
            timeout=SECURITY_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"钥匙串写入子进程异常({type(exc).__name__}): account={account}",
            code="keychain_operation_failed",
        ) from exc
    if result.returncode != 0:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"钥匙串写入失败(exit={result.returncode}): account={account}",
            code="keychain_operation_failed",
            fix_hint="钥匙串可能被锁或满;钥匙串访问.app 检查后重试",
        )


def delete_item(account: str) -> bool:
    """删一条条目(缺席 = False 如实;在场且删成 = True)。

    Raises:
        BridgeError: 通道不可用 / 非 44 的删除失败(通用失败段)。
    """
    if not keychain_available():
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"本机无钥匙串通道(须 macOS + security CLI),无法删除: account={account}",
            code="keychain_backend_unavailable",
        )
    if _fake_active():
        return fake_store().pop(account, None) is not None
    try:
        result = subprocess.run(  # noqa: S603 - 字面量 security CLI,无外壳
            [
                "security", "delete-generic-password",
                "-s", KEYCHAIN_SERVICE,
                "-a", account,
            ],
            capture_output=True,
            text=True,
            timeout=SECURITY_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"钥匙串删除子进程异常({type(exc).__name__}): account={account}",
            code="keychain_operation_failed",
        ) from exc
    if result.returncode == SECURITY_NOT_FOUND_EXIT:
        return False
    if result.returncode != 0:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"钥匙串删除失败(exit={result.returncode}): account={account}",
            code="keychain_operation_failed",
        )
    return True


def build_db_keys_envelope(mapping: dict[str, str], *, migrated_at: str | None = None) -> str:
    """密钥映射 → 钥匙串条目值(JSON 外壳,紧凑单行;stdin 供给形态前提)。

    ``migrated_at`` 缺省 = 当前 ISO 本地时(秒精度,与文件 mtime 口径同族);
    条目无 mtime 可取,时间戳写进外壳、随每次写入刷新(key-status 语义不谎)。
    ``ensure_ascii=True`` 钉死 ASCII 面(security -i 通道硬前提;非 ASCII
    库名在 JSON 层转义,parse 侧无损还原)。
    """
    stamp = migrated_at if migrated_at is not None else (
        datetime.now().astimezone().isoformat(timespec="seconds")
    )
    return json.dumps(
        {MIGRATED_AT_FIELD: stamp, "keys": mapping},
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def parse_db_keys_envelope(raw: str) -> tuple[dict[str, str] | None, str | None]:
    """钥匙串条目值 → (映射, migrated_at);坏形状 = (None, None) 如实。

    两种合法形态:① 外壳 ``{"migrated_at": …, "keys": {…}}``(桥写入形态);
    ② 裸 ``{rel: hex}`` 映射(防御性兼容:手工放置/旧形态,migrated_at=None)。
    解析不干净/非字符串值 = None(宁缺毋假,与 :func:`read_key_cache` 同判)。
    出现 ``keys``/``migrated_at`` 键但形状不符 = 外壳族损坏,不再当裸映射
    兜(库相对路径键不含这两个名字,不构成误伤面)。
    """
    try:
        data: Any = json.loads(raw)
    except ValueError:
        return None, None
    if not isinstance(data, dict) or not data:
        return None, None
    if "keys" in data or MIGRATED_AT_FIELD in data:
        inner = data.get("keys")
        if (
            not isinstance(inner, dict)
            or not inner
            or not isinstance(data.get(MIGRATED_AT_FIELD), str)
            or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in inner.items()
            )
        ):
            return None, None
        return dict(inner), str(data[MIGRATED_AT_FIELD])
    if all(isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        return dict(data), None
    return None, None
