"""插件源码远取链单测(10-06-plugin-src-remote-fetch 批1/批2)。

全 mock 零真网(仓库测试纪律,与 conftest 同款 httpx.MockTransport / 注入
client_factory):锁载入(缺文件=回退语义 / 坏文件与自洽违例=结构化拒)、
资产拉取(2xx / 非 2xx / 网络层失败)、sha256 校验(对/错)、安全解包
(好包剥壳 / 穿越·绝对路径·反斜杠·链接·错顶层前缀恶意件 / 坏包)、编排
(成功落仓同门 / 已装未 force 零网络拒 / 失败零残件零半装 / 本地目录直装
通道零依赖)。

manifest 声明面(install.source 升为内容寻址引用)的向后兼容与校验同套:
旧式仓库 URL 照载、新式 url+sha256+size 载入、坏 sha256/坏 size fail-fast。
"""

from __future__ import annotations

import hashlib
import io
import json
import tarfile
from pathlib import Path

import httpx
import pytest

from myssia.plugins.installed import InstalledPluginStore, PluginStoreError
from myssia.plugins.manifest import LoadError, load_manifest
from myssia.plugins.remote import (
    DEFAULT_FETCH_TIMEOUT_SECONDS,
    LOCK_FILENAME,
    PluginArchiveError,
    PluginFetchError,
    PluginLockError,
    PluginRemoteError,
    PluginsLock,
    extract_staging,
    fetch_plugin_asset,
    install_remote,
    load_plugins_lock,
    verify_sha256,
)

REPO = "https://github.com/xinzhuzi/shishi"
TAG = "v0.0.2"
ASSET_URL = f"{REPO}/releases/download/{TAG}/plugin-myssia-demo.tar.gz"

#: 最小合法 manifest(版本兼容当前 myssia;内容寻址新式 install 节)。
MINIMAL_MANIFEST = """id: myssia-demo
name: 演示件
version: 1.0.0
compatible: ">=0.0.1,<999"
tier: desktop
requires: []
provides: [demo_cap]
modes:
  local:
    install: myssia plugin install plugins/myssia-demo
install:
  source: https://github.com/xinzhuzi/shishi/releases/download/v0.0.2/plugin-myssia-demo.tar.gz
  sha256: "{sha256}"
  size: 999
"""


# ---------------------------------------------------------------------------
# 夹具:真 tar.gz 资产字节 + 锁 + mock 客户端工厂
# ---------------------------------------------------------------------------


def build_asset_tarball(
    plugin_id: str = "myssia-demo",
    *,
    manifest_text: str | None = None,
    extra_files: dict[str, bytes] | None = None,
    member_override: list[tarfile.TarInfo] | None = None,
) -> bytes:
    """打包 ``plugins/<id>/`` 前缀 tar.gz(远取资产形态;git archive 同前缀)。

    ``member_override`` 直接指定成员(恶意件构造用:穿越/链接/错前缀)。
    """
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as tar:
        if member_override is not None:
            for info, data in member_override:
                tar.addfile(info, io.BytesIO(data) if data is not None else None)
        else:
            files = {
                "plugin.yaml": (manifest_text or MINIMAL_MANIFEST.format(sha256="0" * 64)).encode("utf-8"),
                "README.md": b"# demo\n",
                "adapter.py": b"print('remote adapter')\n",
            }
            files.update(extra_files or {})
            for name, data in sorted(files.items()):
                info = tarfile.TarInfo(f"plugins/{plugin_id}/{name}")
                info.size = len(data)
                tar.addfile(info, io.BytesIO(data))
    return buffer.getvalue()


def build_lock_payload(
    tarball: bytes,
    *,
    plugin_id: str = "myssia-demo",
    url: str | None = None,
    sha256: str | None = None,
    size: int | None = None,
    repo: str = REPO,
    tag: str = TAG,
    manifest_version: int = 1,
) -> dict:
    """构造锁 JSON 载荷(缺省自洽:url/sha256/size 全对得上资产字节)。"""
    return {
        "manifest_version": manifest_version,
        "repo": repo,
        "tag": tag,
        "generated_at": "2026-10-06T00:00:00+08:00",
        "assets": {
            plugin_id: {
                "url": url or ASSET_URL,
                "sha256": sha256 or hashlib.sha256(tarball).hexdigest(),
                "size": size if size is not None else len(tarball),
                "version": "1.0.0",
            }
        },
    }


def write_lock(root: Path, payload: dict) -> Path:
    path = Path(root) / LOCK_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return path


def mock_factory(handler) -> "type(httpx.Client) | object":
    """注入 MockTransport 的 httpx.Client 工厂(fetch 的 client_factory 面)。"""
    return lambda **kwargs: httpx.Client(transport=httpx.MockTransport(handler), **kwargs)


def serve_bytes(payload: bytes, *, status: int = 200):
    """固定应答工厂:恒回 payload(或非 2xx 状态)。"""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, content=payload)
    return mock_factory(handler)


def exploding_factory(message: str = "network must not be touched"):
    """一碰就炸的工厂:断言「不应发生网络请求」用。"""
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError(message)
    return mock_factory(handler)


@pytest.fixture()
def store(tmp_path) -> InstalledPluginStore:
    """一次性安装根(远取落仓目标;.staging 在其下,零共享状态)。"""
    return InstalledPluginStore(tmp_path / "install-root")


def staging_root(store: InstalledPluginStore) -> Path:
    return store.root / ".staging"


def assert_no_residue(store: InstalledPluginStore, plugin_id: str = "myssia-demo") -> None:
    """零残件断言:安装根无该件、.staging 无残留目录。"""
    assert not (store.root / plugin_id).exists(), "绝不该出现半装目录"
    residue = list(staging_root(store).iterdir()) if staging_root(store).is_dir() else []
    assert residue == [], f".staging 残留: {residue}"


# ---------------------------------------------------------------------------
# 锁载入:缺文件 / 坏文件 / 自洽校验
# ---------------------------------------------------------------------------


def test_load_lock_missing_file_returns_none_for_fallback(tmp_path):
    """缺文件 = None(旧包回退语义由调用方定;绝不虚构空锁)。"""
    assert load_plugins_lock(tmp_path) is None
    assert load_plugins_lock(tmp_path / "nonexistent") is None


def test_load_lock_valid_roundtrip(tmp_path):
    """自洽锁载入:字段全达;asset 字节钉与预显版本可取。"""
    tarball = build_asset_tarball()
    path = write_lock(tmp_path, build_lock_payload(tarball))
    lock = load_plugins_lock(tmp_path)
    assert lock is not None
    assert lock.manifest_version == 1
    assert lock.repo == REPO
    assert lock.tag == TAG
    asset = lock.assets["myssia-demo"]
    assert asset.url == ASSET_URL
    assert asset.sha256 == hashlib.sha256(tarball).hexdigest()
    assert asset.size == len(tarball)
    assert asset.version == "1.0.0"
    assert lock.asset_url("myssia-demo") == ASSET_URL
    assert lock.asset_url("myssia-unknown") is None
    assert path.name == LOCK_FILENAME


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda payload: payload.update(manifest_version=2), id="manifest_version 不识"),
        pytest.param(lambda payload: payload.update(repo="http://insecure.example/x"), id="repo 非 https"),
        pytest.param(lambda payload: payload.update(tag=""), id="tag 空"),
        pytest.param(lambda payload: payload.update(tag="v1/evil"), id="tag 含斜杠"),
        pytest.param(lambda payload: payload["assets"]["myssia-demo"].update(sha256="deadbeef"), id="sha256 非 64hex"),
        pytest.param(lambda payload: payload["assets"]["myssia-demo"].update(sha256="A" * 64), id="sha256 大写拒"),
        pytest.param(lambda payload: payload["assets"]["myssia-demo"].update(size=0), id="size 零"),
        pytest.param(lambda payload: payload["assets"]["myssia-demo"].update(size=-1), id="size 负"),
        pytest.param(
            lambda payload: payload["assets"]["myssia-demo"].update(url="https://evil.example/asset.tar.gz"),
            id="url 脱离 repo/tag 前缀",
        ),
        pytest.param(lambda payload: payload.update(assets={"../escape": payload["assets"]["myssia-demo"]}), id="资产键穿越形"),
        pytest.param(lambda payload: payload.update(unknown_field=1), id="未知字段 fail-fast"),
    ],
)
def test_load_lock_violations_are_structured_reject(tmp_path, mutate):
    """载入即拒族:自洽违例/形状违例 → plugin_lock_invalid,errors 带定位。"""
    write_lock(tmp_path, build_lock_payload(build_asset_tarball()))
    payload = json.loads((tmp_path / LOCK_FILENAME).read_text(encoding="utf-8"))
    mutate(payload)
    write_lock(tmp_path, payload)
    with pytest.raises(PluginLockError) as excinfo:
        load_plugins_lock(tmp_path)
    assert excinfo.value.code == "plugin_lock_invalid"
    assert isinstance(excinfo.value, PluginStoreError)  # 错误面全走 store 同门
    assert excinfo.value.errors, "结构化明细不可空"


def test_load_lock_bad_json_and_non_object_are_structured(tmp_path):
    """坏 JSON / 非 JSON 对象 → plugin_lock_invalid(data 带路径与原因)。"""
    (tmp_path / LOCK_FILENAME).write_text("{not json", encoding="utf-8")
    with pytest.raises(PluginLockError) as excinfo:
        load_plugins_lock(tmp_path)
    assert excinfo.value.code == "plugin_lock_invalid"
    assert excinfo.value.data["path"].endswith(LOCK_FILENAME)
    (tmp_path / LOCK_FILENAME).write_text('["array"]', encoding="utf-8")
    with pytest.raises(PluginLockError) as excinfo:
        load_plugins_lock(tmp_path)
    assert excinfo.value.code == "plugin_lock_invalid"


# ---------------------------------------------------------------------------
# 拉取:2xx / 非 2xx / 网络层失败
# ---------------------------------------------------------------------------


def _asset_for(tarball: bytes) -> PluginsLock:
    return PluginsLock.model_validate(build_lock_payload(tarball)).assets["myssia-demo"]


def test_fetch_success_returns_exact_bytes():
    """2xx → 逐字节返回资产内容。"""
    tarball = build_asset_tarball()
    got = fetch_plugin_asset(_asset_for(tarball), client_factory=serve_bytes(tarball))
    assert got == tarball


def test_fetch_http_error_is_structured_with_status():
    """非 2xx → plugin_fetch_failed,data 带 status/url(AC3 定位面)。"""
    tarball = build_asset_tarball()
    asset = _asset_for(tarball)
    with pytest.raises(PluginFetchError) as excinfo:
        fetch_plugin_asset(asset, client_factory=serve_bytes(b"gone", status=404))
    assert excinfo.value.code == "plugin_fetch_failed"
    assert excinfo.value.data == {"url": ASSET_URL, "status": 404}


def test_fetch_network_failure_is_structured_not_raw():
    """网络层失败(超时/连接错)→ plugin_fetch_failed 结构化,data 带 reason/url;
    绝不让 httpx 原生异常裸穿。"""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route to host", request=request)
    with pytest.raises(PluginFetchError) as excinfo:
        fetch_plugin_asset(_asset_for(build_asset_tarball()), client_factory=mock_factory(handler))
    assert excinfo.value.code == "plugin_fetch_failed"
    assert excinfo.value.data["url"] == ASSET_URL
    assert "ConnectError" in excinfo.value.data["reason"]


def test_fetch_default_timeout_is_60s():
    """缺省超时 60s(设计 D9 钉死;防回归漂移)。"""
    assert DEFAULT_FETCH_TIMEOUT_SECONDS == 60.0


# ---------------------------------------------------------------------------
# sha256 校验
# ---------------------------------------------------------------------------


def test_verify_sha256_match_is_silent():
    """字节钉对上 → 无异常。"""
    payload = build_asset_tarball()
    verify_sha256(payload, hashlib.sha256(payload).hexdigest())


def test_verify_sha256_mismatch_is_structured_with_both_digests():
    """不符 → integrity_mismatch,data 带期望/实得(AC3)。"""
    payload = build_asset_tarball()
    with pytest.raises(PluginRemoteError) as excinfo:
        verify_sha256(payload, "0" * 64, url=ASSET_URL)
    assert excinfo.value.code == "integrity_mismatch"
    assert excinfo.value.data["expected"] == "0" * 64
    assert excinfo.value.data["actual"] == hashlib.sha256(payload).hexdigest()
    assert excinfo.value.data["url"] == ASSET_URL


# ---------------------------------------------------------------------------
# 安全解包:好包 / 恶意件矩阵 / 坏包
# ---------------------------------------------------------------------------


def test_extract_staging_good_tarball_strips_plugins_prefix(tmp_path):
    """好包:剥 plugins/<id>/ 壳,plugin.yaml 落暂存根;嵌套目录树完整。"""
    tarball = build_asset_tarball(extra_files={"sub/credhunter/__init__.py": b"x = 1\n"})
    staging = extract_staging(tarball, tmp_path / "staging", expected_plugin_id="myssia-demo")
    assert (staging / "plugin.yaml").is_file()
    assert (staging / "README.md").is_file()
    assert (staging / "adapter.py").is_file()
    assert (staging / "sub" / "credhunter" / "__init__.py").read_text(encoding="utf-8") == "x = 1\n"
    assert not (staging / "plugins").exists(), "壳前缀必须剥净(staging 根=包根)"


def _evil_member(name: str, *, symlink: str | None = None, is_dir: bool = False, data: bytes = b"evil\n"):
    info = tarfile.TarInfo(name)
    if symlink is not None:
        info.type = tarfile.SYMTYPE
        info.linkname = symlink
        return info, None
    if is_dir:
        info.type = tarfile.DIRTYPE
        return info, None
    info.size = len(data)
    return info, data


@pytest.mark.parametrize(
    "member",
    [
        pytest.param(_evil_member("plugins/myssia-demo/../../escape.txt"), id=".. 穿越"),
        pytest.param(_evil_member("/etc/evil.txt"), id="绝对路径"),
        pytest.param(_evil_member("plugins\\myssia-demo\\evil.txt"), id="反斜杠(Windows 穿越)"),
        pytest.param(_evil_member("plugins/myssia-demo/link", symlink="/etc/passwd"), id="符号链接"),
        pytest.param(_evil_member("plugins/myssia-demo/hard", symlink="../../x"), id="硬链接形态"),
        pytest.param(_evil_member("other-prefix/plugin.yaml"), id="错顶层前缀"),
        pytest.param(_evil_member("plugins/myssia-other/plugin.yaml"), id="他人 id 前缀"),
        pytest.param(_evil_member("plugins"), id="裸 plugins 文件件"),
    ],
)
def test_extract_staging_rejects_malicious_members(tmp_path, member):
    """恶意件矩阵 → plugin_archive_invalid(白名单违例),暂存零落盘。"""
    tarball = build_asset_tarball(member_override=[member])
    staging_dir = tmp_path / "staging"
    with pytest.raises(PluginArchiveError) as excinfo:
        extract_staging(tarball, staging_dir, expected_plugin_id="myssia-demo")
    assert excinfo.value.code == "plugin_archive_invalid"
    assert excinfo.value.data["member"] == member[0].name
    assert not staging_dir.exists() or not any(staging_dir.iterdir()), "恶意件不得留半解包残件"


def test_extract_staging_rejects_garbage_payload(tmp_path):
    """非 tar.gz 字节 → plugin_archive_invalid(结构化,不裸穿 TarError)。"""
    with pytest.raises(PluginArchiveError) as excinfo:
        extract_staging(b"this is not a tarball at all", tmp_path / "staging", expected_plugin_id="myssia-demo")
    assert excinfo.value.code == "plugin_archive_invalid"


# ---------------------------------------------------------------------------
# 编排 install_remote:成功同门 / 失败零残 / 已装不触发远取 / 本地通道
# ---------------------------------------------------------------------------


def test_install_remote_success_lands_in_store_same_gate(tmp_path, store):
    """成功链:拉取→校验→解包→store.install 同门落位;应答 CLI 同形状;
    成功后 .staging 清残;随包锁原件不动。"""
    tarball = build_asset_tarball()
    write_lock(tmp_path, build_lock_payload(tarball))
    lock = load_plugins_lock(tmp_path)
    result = install_remote(lock, "myssia-demo", store, client_factory=serve_bytes(tarball))
    assert result["id"] == "myssia-demo"
    assert result["version"] == "1.0.0"
    assert result["path"] == str(store.root / "myssia-demo")
    installed = store.root / "myssia-demo"
    assert (installed / "plugin.yaml").is_file()
    assert (installed / "adapter.py").read_text(encoding="utf-8") == "print('remote adapter')\n"
    assert not staging_root(store).is_dir() or not any(staging_root(store).iterdir())
    # manifest 实拉校验为准:装进来的 plugin.yaml 就是资产里的那份
    assert (installed / "plugin.yaml").read_text(encoding="utf-8") == (
        MINIMAL_MANIFEST.format(sha256="0" * 64)
    )
    # 已装态翻真(发现面对齐)
    entry = store.locate("myssia-demo")
    assert entry is not None and entry.manifest is not None
    assert entry.manifest.version == "1.0.0"


def test_install_remote_bad_hash_rejects_with_zero_residue(store):
    """坏 hash 拒:integrity_mismatch + 期望/实得;零半装零残件(AC3)。"""
    tarball = build_asset_tarball()
    lock = PluginsLock.model_validate(build_lock_payload(tarball))
    with pytest.raises(PluginRemoteError) as excinfo:
        install_remote(lock, "myssia-demo", store, client_factory=serve_bytes(b"tampered bytes"))
    assert excinfo.value.code == "integrity_mismatch"
    assert excinfo.value.data["expected"] == lock.assets["myssia-demo"].sha256
    assert excinfo.value.data["url"] == ASSET_URL
    assert_no_residue(store)


def test_install_remote_fetch_failure_is_structured_no_half_install(store):
    """网络失败拒:plugin_fetch_failed 带 status;零半装零残件。"""
    tarball = build_asset_tarball()
    lock = PluginsLock.model_validate(build_lock_payload(tarball))
    with pytest.raises(PluginFetchError) as excinfo:
        install_remote(lock, "myssia-demo", store, client_factory=serve_bytes(b"boom", status=503))
    assert excinfo.value.code == "plugin_fetch_failed"
    assert excinfo.value.data["status"] == 503
    assert_no_residue(store)


def test_install_remote_corrupt_archive_cleans_staging(store):
    """包损坏拒:plugin_archive_invalid;解包残件即清(AC3 零残目录)。"""
    tarball = build_asset_tarball()
    corrupt = build_asset_tarball(member_override=[_evil_member("plugins/myssia-demo/../../escape.txt")])
    lock = PluginsLock.model_validate(build_lock_payload(corrupt))
    with pytest.raises(PluginArchiveError):
        install_remote(lock, "myssia-demo", store, client_factory=serve_bytes(corrupt))
    assert_no_residue(store)
    assert tarball, "夹具自证"


def test_install_remote_missing_entry_is_structured(store):
    """锁内无条目 → plugin_lock_missing(编排层防御深度;data 带锁上下文)。"""
    lock = PluginsLock.model_validate(build_lock_payload(build_asset_tarball()))
    with pytest.raises(PluginLockError) as excinfo:
        install_remote(lock, "myssia-unknown", store, client_factory=exploding_factory())
    assert excinfo.value.code == "plugin_lock_missing"
    assert excinfo.value.data["plugin_id"] == "myssia-unknown"


def test_install_remote_already_installed_never_fetches(tmp_path, store):
    """已装未 force → already_installed 且**零网络**(已装件不触发远取)。"""
    tarball = build_asset_tarball()
    lock = PluginsLock.model_validate(build_lock_payload(tarball))
    install_remote(lock, "myssia-demo", store, client_factory=serve_bytes(tarball))
    with pytest.raises(PluginStoreError) as excinfo:
        install_remote(lock, "myssia-demo", store, client_factory=exploding_factory())
    assert excinfo.value.code == "already_installed"
    # force 覆盖装照旧(D7 复用 force 语义)
    refreshed = build_asset_tarball(manifest_text=MINIMAL_MANIFEST.format(sha256="0" * 64).replace("version: 1.0.0", "version: 1.1.0"))
    lock2 = PluginsLock.model_validate(build_lock_payload(refreshed))
    result = install_remote(lock2, "myssia-demo", store, force=True, client_factory=serve_bytes(refreshed))
    assert result["version"] == "1.1.0"


def test_install_remote_store_gates_pass_through(store):
    """store 同门透传:资产内 manifest 坏 → manifest_invalid;版本不兼容未
    force → incompatible_version;force 强装照旧(INV-6 语义零漂移)。"""
    bad_manifest = "id: myssia-demo\nunknown_field: 1\n"
    tarball = build_asset_tarball(manifest_text=bad_manifest)
    lock = PluginsLock.model_validate(build_lock_payload(tarball))
    with pytest.raises(PluginStoreError) as excinfo:
        install_remote(lock, "myssia-demo", store, client_factory=serve_bytes(tarball))
    assert excinfo.value.code == "manifest_invalid"
    assert_no_residue(store)
    future = MINIMAL_MANIFEST.format(sha256="0" * 64).replace('">=0.0.1,<999"', '">=999.0.0"')
    tarball2 = build_asset_tarball(manifest_text=future)
    lock2 = PluginsLock.model_validate(build_lock_payload(tarball2))
    with pytest.raises(PluginStoreError) as excinfo:
        install_remote(lock2, "myssia-demo", store, client_factory=serve_bytes(tarball2))
    assert excinfo.value.code == "incompatible_version"
    result = install_remote(lock2, "myssia-demo", store, force=True, client_factory=serve_bytes(tarball2))
    assert result["forced"] is True
    assert result["compatible_current"] is False


def test_installed_entries_skip_staging_and_unchanged_semantics(tmp_path, store):
    """INV-6:远取链运行后 store.entries 扫描不含 .staging;已装旧件逐字节
    零扰动(成功/失败两态都比对);卸载语义原样(remove 同门)。"""

    def tree_digest(root: Path) -> dict[str, bytes]:
        return {
            str(item.relative_to(root)): item.read_bytes()
            for item in sorted(root.rglob("*"))
            if item.is_file()
        }

    legacy = store.root / "myssia-legacy"
    legacy.mkdir(parents=True)
    (legacy / "plugin.yaml").write_text(
        MINIMAL_MANIFEST.replace("myssia-demo", "myssia-legacy").format(sha256="0" * 64), encoding="utf-8"
    )
    (legacy / "adapter.py").write_text("# legacy\n", encoding="utf-8")
    before = tree_digest(legacy)
    tarball = build_asset_tarball()
    lock = PluginsLock.model_validate(build_lock_payload(tarball))
    install_remote(lock, "myssia-demo", store, client_factory=serve_bytes(tarball))
    # 失败态(坏 hash)同样不得扰动已装件
    with pytest.raises(PluginRemoteError):
        install_remote(lock, "myssia-demo", store, force=True, client_factory=serve_bytes(b"tamper"))
    assert tree_digest(legacy) == before, "已装旧件必须逐字节零扰动"
    ids = {entry.plugin_id or entry.dir_name for entry in store.entries()}
    assert ids == {"myssia-demo", "myssia-legacy"}, f".staging 不得成条目: {ids}"
    removed = store.remove("myssia-legacy")
    assert removed["removed"] is True
    assert not legacy.exists()


def test_local_directory_install_channel_needs_no_lock(tmp_path, store):
    """dev/本地仓库通道保留:store.install(<本地目录>) 直装,零锁零远取
    (CLI ``myssia plugin install plugins/<id>`` 同路,INV-7)。"""
    source = tmp_path / "plugins" / "myssia-local"
    source.mkdir(parents=True)
    (source / "plugin.yaml").write_text(
        MINIMAL_MANIFEST.replace("myssia-demo", "myssia-local").format(sha256="0" * 64), encoding="utf-8"
    )
    (source / "adapter.py").write_text("# local dev\n", encoding="utf-8")
    result = store.install(source)
    assert result["id"] == "myssia-local"
    assert (store.root / "myssia-local" / "adapter.py").is_file()


# ---------------------------------------------------------------------------
# manifest 声明面:install.source 内容寻址升级(旧字段向后兼容)
# ---------------------------------------------------------------------------


def _manifest_data(install: dict) -> dict:
    return {
        "id": "myssia-demo",
        "name": "演示件",
        "version": "1.0.0",
        "compatible": ">=0.0.1,<999",
        "tier": "desktop",
        "requires": [],
        "provides": ["demo_cap"],
        "modes": {"local": {"install": "myssia plugin install plugins/myssia-demo"}},
        "install": install,
    }


def test_manifest_legacy_repo_url_install_section_still_loads():
    """旧式声明(仓库 URL,21 处存量形态)零迁移照载:sha256/size 缺省 None。"""
    manifest = load_manifest(_manifest_data({"source": "https://github.com/xinzhuzi/myia.git"}))
    assert manifest.install.source == "https://github.com/xinzhuzi/myia.git"
    assert manifest.install.sha256 is None
    assert manifest.install.size is None


def test_manifest_content_addressed_install_section_loads():
    """新式声明(release 资产 url + sha256 字节钉 + size)载入(D1 选型)。"""
    manifest = load_manifest(
        _manifest_data({"source": ASSET_URL, "sha256": "a" * 64, "size": 4096})
    )
    assert manifest.install.source == ASSET_URL
    assert manifest.install.sha256 == "a" * 64
    assert manifest.install.size == 4096


@pytest.mark.parametrize(
    "install",
    [
        pytest.param({"source": ASSET_URL, "sha256": "deadbeef"}, id="sha256 短"),
        pytest.param({"source": ASSET_URL, "sha256": "A" * 64}, id="sha256 大写"),
        pytest.param({"source": ASSET_URL, "sha256": "a" * 64, "size": 0}, id="size 零"),
        pytest.param({"source": ASSET_URL, "sha256": "a" * 64, "size": -5}, id="size 负"),
    ],
)
def test_manifest_bad_content_addressing_fails_fast(install):
    """坏字节钉/坏 size → LoadError fail-fast(错误路径精确到 install.sha256/size)。"""
    with pytest.raises(LoadError) as excinfo:
        load_manifest(_manifest_data(install))
    paths = {detail.path.removeprefix("$.") for detail in excinfo.value.errors}
    assert any(path.startswith("install.") for path in paths), excinfo.value.errors
