"""插件源码远取链:内容寻址锁 → 拉取 → sha256 校验 → 安全解包 → 同门落仓.

规范出处(task 10-06-plugin-src-remote-fetch):装机包内插件组件包只准携带
声明件(``plugin.yaml`` + ``README.md``),源码(adapter.py/场景件/自有子包)
与数据件(vendor/缓存)不进包(INV-1/2/3)。点装时按随包
``plugins.lock.json`` 的内容寻址条目(url + sha256)远取 per-plugin
release 资产 tar.gz,字节校验后经既有
:class:`myssia.plugins.installed.InstalledPluginStore.install` **同门**落
安装根 ``~/.myia/plugins/<id>``——manifest 校验/版本矩阵/整目录拷贝/绝不
半装/已装未 force 拒/卸载语义零变化(INV-6),已装件不触发远取。

链路四步(全部结构化失败,零静默零半装,INV-5):

1. :func:`load_plugins_lock` — 读随包锁;缺文件 = ``None``(旧包回退语义,
   由调用方走包内直拷);坏文件 = :class:`PluginLockError`
   (``plugin_lock_invalid``)。
2. :func:`fetch_plugin_asset` — httpx 同步客户端拉资产(trustenv 沿系统
   代理、follow_redirects——GitHub release 资产 302 到 CDN);非 2xx /
   网络失败 = :class:`PluginFetchError`(``plugin_fetch_failed``,
   data 带 url/status)。
3. :func:`verify_sha256` — 字节钉校验;不符 = :class:`IntegrityMismatch`
   (``integrity_mismatch``,data 带期望/实得)。
4. :func:`extract_staging` — tarfile 安全解包:成员白名单(相对路径、无
   ``..``、无反斜杠、非符号/硬链接、非设备件)+ 唯一顶层前缀
   ``plugins/<id>/`` 剥壳(py>=3.12 ``filter="data"`` 与手工白名单双保险,
   3.11 老补丁位走纯手工);违例 = :class:`PluginArchiveError`
   (``plugin_archive_invalid``)。

:func:`install_remote` 编排以上四步:暂存 ``<安装根>/.staging/<id>-<4hex
随机>/``(隐藏目录,store 扫描天然跳过),成功失败一律清残(D8),最终
``store.install(staging, force=force)`` 原子收口。错误面全走
:class:`myssia.plugins.installed.PluginStoreError` 子类(code/中文
message/结构化 errors + ``data`` 定位信息),CLI/sidecar 沿既有包装透传。

锁契约(D2/D3;与 desktop/resources/runtime-manifest.json 的
url+sha256+archive 同构判例)::

    {
      "manifest_version": 1,
      "repo": "https://github.com/xinzhuzi/shishi",
      "tag": "v0.0.2",
      "generated_at": "2026-10-06T00:00:00+08:00",
      "assets": {
        "myssia-proxy": {"url": "…/releases/download/v0.0.2/plugin-myssia-proxy.tar.gz",
                          "sha256": "<64hex>", "size": 4096, "version": "1.0.0"}
      }
    }

载入即拒(结构化 ``plugin_lock_invalid``):manifest_version 不识、repo 非
https、tag 空/含斜杠、sha256 非 64 位小写十六进制、size<=0、资产 url 不以
``{repo}/releases/download/{tag}/`` 开头(锁内自洽,防字段互相矛盾)。
"""

from __future__ import annotations

import copy
import hashlib
import io
import json
import logging
import secrets
import shutil
import tarfile
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from myssia.plugins.installed import InstalledPluginStore, PluginStoreError
from myssia.plugins.manifest import SHA256_HEX_RE
from myssia.schema import _PLUGIN_ID_RE

logger = logging.getLogger(__name__)

__all__ = [
    "DEFAULT_FETCH_TIMEOUT_SECONDS",
    "LOCK_FILENAME",
    "LOCK_MANIFEST_VERSION",
    "IntegrityMismatch",
    "PluginArchiveError",
    "PluginFetchError",
    "PluginLockAsset",
    "PluginLockError",
    "PluginRemoteError",
    "PluginsLock",
    "extract_staging",
    "fetch_plugin_asset",
    "install_remote",
    "load_plugins_lock",
    "verify_sha256",
]

#: 随包远取锁的规范文件名(落 Resources/plugins 根,与组件包声明件同目录)。
LOCK_FILENAME = "plugins.lock.json"
#: 锁 schema 版本(不识即拒,不静默猜)。
LOCK_MANIFEST_VERSION = 1
#: 资产拉取超时秒数(单件 KB~百 KB 级,60s 富余;D9)。
DEFAULT_FETCH_TIMEOUT_SECONDS = 60.0
#: 暂存目录名(安装根下隐藏目录;store.entries 跳过点前缀目录,零扰动)。
STAGING_DIRNAME = ".staging"


# ---------------------------------------------------------------------------
# 结构化错误(全走 PluginStoreError 语义:code/中文 message/errors + data)
# ---------------------------------------------------------------------------


class PluginRemoteError(PluginStoreError):
    """远取链结构化失败的公共基类。

    与父类唯一差异:``data`` 携带机器可读定位信息(url/sha256 期望实得/
    HTTP status 等),sidecar 侧并入协议错误 ``data`` 字段(UI 可见,
    INV-5「零静默」)。
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        errors: list[dict[str, Any]] | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(code, message, errors=errors)
        self.data: dict[str, Any] = dict(data or {})


class PluginLockError(PluginRemoteError):
    """远取锁缺失条目/坏文件/校验失败(``plugin_lock_invalid`` | ``plugin_lock_missing``)。"""


class PluginFetchError(PluginRemoteError):
    """资产拉取失败(``plugin_fetch_failed``;非 2xx 或网络层错误)。"""


class IntegrityMismatch(PluginRemoteError):
    """sha256 校验不符(``integrity_mismatch``;资产字节与锁钉不一致)。"""


class PluginArchiveError(PluginRemoteError):
    """资产包损坏/恶意(``plugin_archive_invalid``;解包白名单违例)。"""


# ---------------------------------------------------------------------------
# 锁 schema(D3:pydantic fail-fast,未知字段拒)
# ---------------------------------------------------------------------------


class _StrictLockModel(BaseModel):
    """锁子模型基类:未知字段 fail-fast(与 manifest schema 同一纪律)。"""

    model_config = ConfigDict(extra="forbid")


class PluginLockAsset(_StrictLockModel):
    """单个组件包的内容寻址条目:url(锁内 repo/tag 自洽)+ sha256 字节钉。"""

    url: str = Field(min_length=1, max_length=1024)
    sha256: str = Field(min_length=64, max_length=64)
    size: int = Field(gt=0)
    # 冗余自资产内 plugin.yaml(装机预显用;装机后以实拉 manifest 校验为准,
    # 锁只作发现面提示,不放松 store 校验——D3)。
    version: str | None = Field(default=None, max_length=64)

    @field_validator("sha256")
    @classmethod
    def _check_sha256(cls, value: str) -> str:
        if not SHA256_HEX_RE.match(value):
            raise ValueError(
                f"sha256 必须是 64 位小写十六进制(当前为 {value!r};资产字节钉不认缩写/大写)"
            )
        return value


class PluginsLock(_StrictLockModel):
    """随包远取锁:``{repo, tag, assets}`` 的内容寻址事实源(D2/D3)。"""

    manifest_version: int
    repo: str = Field(min_length=1, max_length=512)
    tag: str = Field(min_length=1, max_length=64)
    generated_at: str | None = Field(default=None, max_length=64)
    assets: dict[str, PluginLockAsset] = Field(default_factory=dict)

    @field_validator("manifest_version")
    @classmethod
    def _check_manifest_version(cls, value: int) -> int:
        if value != LOCK_MANIFEST_VERSION:
            raise ValueError(
                f"manifest_version 必须是 {LOCK_MANIFEST_VERSION}(当前为 {value!r};"
                "不识版本即拒,不静默降级猜格式)"
            )
        return value

    @field_validator("repo")
    @classmethod
    def _check_repo(cls, value: str) -> str:
        if not value.startswith("https://"):
            raise ValueError(f"repo 必须是 https URL(当前为 {value!r})")
        return value.rstrip("/")

    @field_validator("tag")
    @classmethod
    def _check_tag(cls, value: str) -> str:
        if "/" in value or any(character.isspace() for character in value):
            raise ValueError(f"tag 不得含斜杠或空白(当前为 {value!r};会破坏 url 前缀自洽)")
        return value

    @field_validator("assets")
    @classmethod
    def _check_asset_keys(cls, value: dict[str, PluginLockAsset]) -> dict[str, PluginLockAsset]:
        for plugin_id in value:
            if not _PLUGIN_ID_RE.match(plugin_id):
                raise ValueError(
                    f"assets 键 {plugin_id!r} 不是合法插件 id(小写字母/数字/连字符/下划线,"
                    "字母数字开头 2-64 字符;id 直接拼暂存路径,不认穿越形态)"
                )
        return value

    @model_validator(mode="after")
    def _check_url_prefix_self_consistency(self) -> PluginsLock:
        """锁内自洽:资产 url 必须落在 ``{repo}/releases/download/{tag}/`` 下。

        防锁字段互相矛盾(repo 写 A、url 指 B)——锁是机器事实源,自相矛盾
        即整体不可信,载入即拒。
        """
        prefix = f"{self.repo}/releases/download/{self.tag}/"
        for plugin_id, asset in self.assets.items():
            if not asset.url.startswith(prefix):
                raise ValueError(
                    f"assets.{plugin_id}.url 必须以 {prefix} 开头"
                    f"(当前为 {asset.url!r};锁内 repo/tag 与资产 url 互相矛盾)"
                )
        return self

    def asset_url(self, plugin_id: str) -> str | None:
        """取某插件条目的资产 url;无条目 None(调用方定回退/拒)。"""
        asset = self.assets.get(plugin_id)
        return asset.url if asset is not None else None


def _validation_details(exc: ValidationError) -> list[dict[str, Any]]:
    """pydantic 校验错误 → 结构化明细(path/type/message,人读中文不硬凑)。"""
    details: list[dict[str, Any]] = []
    for error in exc.errors():
        location = ".".join(str(part) for part in error.get("loc", ()))
        message = str(error.get("msg", ""))
        # 「Value error, <中文>」前缀剥壳:校验器消息本身已是完整中文原因。
        if message.startswith("Value error, "):
            message = message[len("Value error, ") :]
        details.append({"path": location or "$", "type": str(error.get("type", "")), "message": message})
    return details


def load_plugins_lock(root: str | Path) -> PluginsLock | None:
    """读随包目录下的 ``plugins.lock.json``。

    Returns:
        None:锁文件缺失(旧装机包形态;回退语义由调用方决定,D3)。

    Raises:
        PluginLockError: ``plugin_lock_invalid`` —— 文件在但不可读/非合法
            JSON/不是对象/schema 校验失败(含自洽性违例)。
    """
    path = Path(root) / LOCK_FILENAME
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PluginLockError(
            "plugin_lock_invalid",
            f"远取锁 {path} 不可读或不是合法 JSON: {exc}",
            data={"path": str(path), "reason": str(exc)},
        ) from exc
    if not isinstance(data, dict):
        raise PluginLockError(
            "plugin_lock_invalid",
            f"远取锁 {path} 必须是 JSON 对象,当前为 {type(data).__name__}",
            data={"path": str(path)},
        )
    try:
        return PluginsLock.model_validate(data)
    except ValidationError as exc:
        details = _validation_details(exc)
        first = details[0]["message"] if details else str(exc)
        raise PluginLockError(
            "plugin_lock_invalid",
            f"远取锁 {path} 校验失败: {first}",
            errors=details,
            data={"path": str(path)},
        ) from exc


# ---------------------------------------------------------------------------
# 拉取与校验
# ---------------------------------------------------------------------------

#: 客户端工厂签名(测试注入 MockTransport;缺省真 httpx.Client)。
ClientFactory = Callable[..., httpx.Client]


def fetch_plugin_asset(
    asset: PluginLockAsset,
    *,
    timeout: float = DEFAULT_FETCH_TIMEOUT_SECONDS,
    client_factory: ClientFactory | None = None,
) -> bytes:
    """按锁条目拉取组件包资产字节。

    httpx 同步客户端;trustenv 缺省开(沿系统 HTTPS_PROXY 既有行为);
    follow_redirects 开(GitHub release 资产 302 到 CDN,不跟即失败)。

    Raises:
        PluginFetchError: ``plugin_fetch_failed`` —— HTTP 非 2xx(data 带
            status/url)或网络层失败(超时/连接错,data 带 reason/url)。
    """
    factory = client_factory or httpx.Client
    try:
        with factory(timeout=timeout, follow_redirects=True) as client:
            response = client.get(asset.url)
    except httpx.HTTPError as exc:
        raise PluginFetchError(
            "plugin_fetch_failed",
            f"插件资产拉取失败({asset.url}): {type(exc).__name__}: {exc}",
            data={"url": asset.url, "reason": f"{type(exc).__name__}: {exc}" if str(exc) else type(exc).__name__},
        ) from exc
    if response.status_code < 200 or response.status_code >= 300:
        raise PluginFetchError(
            "plugin_fetch_failed",
            f"插件资产拉取失败({asset.url}): HTTP {response.status_code}",
            data={"url": asset.url, "status": response.status_code},
        )
    payload = response.content
    logger.debug("插件资产已拉取 url=%s bytes=%d", asset.url, len(payload))
    return payload


def verify_sha256(payload: bytes, expected: str, *, url: str | None = None) -> None:
    """字节钉校验:sha256(payload) 必须逐字符等于锁钉值。

    Raises:
        IntegrityMismatch: ``integrity_mismatch`` —— data 带 expected/actual
            (与可选 url;AC3 定位信息面)。
    """
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected.strip().lower():
        raise IntegrityMismatch(
            "integrity_mismatch",
            f"插件资产 sha256 校验不符(期望 {expected},实得 {actual})",
            data={"expected": expected, "actual": actual, **({"url": url} if url else {})},
        )


# ---------------------------------------------------------------------------
# 安全解包
# ---------------------------------------------------------------------------


def _validated_member(member: tarfile.TarInfo, expected_plugin_id: str) -> None:
    """解包白名单单件校验(违例即 :class:`PluginArchiveError`,D9 双保险)。

    - 路径:相对、无 ``..``、无反斜杠(Windows 路径分隔穿越)、非绝对;
    - 类型:普通文件/目录 only(符号链接/硬链接/设备/FIFO 一律拒——组件包
      资产没有合法链接件);
    - 前缀:必须落在 ``plugins/<expected_plugin_id>/`` 唯一顶层前缀下。
    """
    name = member.name

    def reject(reason: str) -> PluginArchiveError:
        return PluginArchiveError(
            "plugin_archive_invalid",
            f"插件资产包含非法成员 {name!r}: {reason}",
            data={"member": name, "reason": reason},
        )

    if "\\" in name:
        raise reject("含反斜杠(疑似 Windows 路径穿越)")
    if member.issym() or member.islnk():
        raise reject("符号/硬链接件(组件包资产不允许链接)")
    if member.isdev():
        raise reject("设备件")
    if not member.isfile() and not member.isdir():
        raise reject(f"非普通文件/目录(type={member.type!r})")
    posix = PurePosixPath(name)
    if posix.is_absolute() or not posix.parts:
        raise reject("绝对路径或空路径")
    if ".." in posix.parts:
        raise reject("含 .. 路径穿越段")
    parts = posix.parts
    if parts[0] != "plugins":
        raise reject(f"顶层前缀必须是 plugins/{expected_plugin_id}/")
    if len(parts) >= 2 and parts[1] != expected_plugin_id:
        raise reject(f"顶层前缀必须是 plugins/{expected_plugin_id}/")
    if len(parts) < 2 and not member.isdir():
        raise reject(f"顶层前缀必须是 plugins/{expected_plugin_id}/")


def extract_staging(payload: bytes, staging_dir: Path, *, expected_plugin_id: str) -> Path:
    """把资产字节安全解包进暂存目录(剥 ``plugins/<id>/`` 壳,staging 根=包根)。

    Raises:
        PluginArchiveError: ``plugin_archive_invalid`` —— 非 tar.gz/坏包/
            成员白名单违例(见 :func:`_validated_member`)。违例时目标目录
            不留半解包残件(整体先校验后落盘)。
    """
    staging_dir = Path(staging_dir)
    try:
        with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as tar:
            members: list[tarfile.TarInfo] = []
            for member in tar.getmembers():
                _validated_member(member, expected_plugin_id)
                stripped_parts = PurePosixPath(member.name).parts[2:]
                if not stripped_parts:
                    continue  # plugins/ 与 plugins/<id>/ 壳目录成员,内容件自建父目录
                sanitized = copy.copy(member)
                sanitized.name = PurePosixPath(*stripped_parts).as_posix()
                sanitized.mode = member.mode & 0o777  # 剥 setuid/setgid/sticky 高位
                members.append(sanitized)
            staging_dir.mkdir(parents=True, exist_ok=True)
            try:
                tar.extractall(staging_dir, members=members, filter="data")
            except TypeError:  # py<3.11.4 无 filter 参数:成员白名单已手工过筛
                tar.extractall(staging_dir, members=members)
    except tarfile.TarError as exc:
        shutil.rmtree(staging_dir, ignore_errors=True)
        raise PluginArchiveError(
            "plugin_archive_invalid",
            f"插件资产不是合法 tar.gz 包: {exc}",
            data={"reason": str(exc)},
        ) from exc
    return staging_dir


# ---------------------------------------------------------------------------
# 编排:拉取 → 校验 → 解包 → store.install 同门收口
# ---------------------------------------------------------------------------


def install_remote(
    lock: PluginsLock,
    plugin_id: str,
    store: InstalledPluginStore,
    *,
    force: bool = False,
    timeout: float = DEFAULT_FETCH_TIMEOUT_SECONDS,
    client_factory: ClientFactory | None = None,
) -> dict[str, Any]:
    """按锁远取一件组件包并装进安装根(编排,编排失败零残件)。

    流程:已装未 force 零网络先拒 → fetch → sha256 校验 → 解包暂存 →
    ``store.install(staging, force=force)`` 同门落位(manifest 校验/版本
    矩阵/整目录拷贝/绝不半装全在 store,本函数零复制)。暂存目录
    ``<安装根>/.staging/<id>-<4hex>/``(隐藏目录,store 扫描跳过);成功
    失败一律清残(D8)。

    Returns:
        store.install 的结果 dict(id/name/version/path/…,CLI 同形状)。

    Raises:
        PluginLockError: ``plugin_lock_missing`` —— 锁内无该插件条目。
        PluginStoreError: 已装未 force(``already_installed``)及 store 门
            全部结构化拒绝;远取链失败见各步错误类。
    """
    asset = lock.assets.get(plugin_id)
    if asset is None:
        raise PluginLockError(
            "plugin_lock_missing",
            f"远取锁(tag {lock.tag})内没有插件 {plugin_id!r} 的资产条目;"
            f"可用件见锁 assets 键集 {sorted(lock.assets)}",
            data={"plugin_id": plugin_id, "tag": lock.tag, "repo": lock.repo},
        )
    # 已装未 force:零网络先拒(store 同门口径前置;资产 manifest id 与请求
    # id 漂移的病态件仍由 store.install 装后门兜底)。已装件不触发远取。
    destination = store.root / plugin_id
    if destination.exists() and not force:
        raise PluginStoreError(
            "already_installed",
            f"插件 {plugin_id} 已安装于 {destination};覆盖安装请用 force",
        )
    staging_dir = store.root / STAGING_DIRNAME / f"{plugin_id}-{secrets.token_hex(2)}"
    try:
        payload = fetch_plugin_asset(asset, timeout=timeout, client_factory=client_factory)
        verify_sha256(payload, asset.sha256, url=asset.url)
        extract_staging(payload, staging_dir, expected_plugin_id=plugin_id)
        return store.install(staging_dir, force=force)
    except OSError as exc:
        # 解包/暂存阶段的文件系统失败(权限/磁盘满等)结构化(io_error),
        # 与 store.install 的 IO 包裹同款语义,绝不裸 traceback 打穿协议面。
        raise PluginStoreError(
            "io_error", f"插件远取暂存失败({staging_dir}): {exc}"
        ) from exc
    finally:
        shutil.rmtree(staging_dir, ignore_errors=True)
