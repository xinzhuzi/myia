# 随包远取锁 plugins.lock.json 发布门禁(10-06-plugin-src-remote-fetch 批4;design D8)。
#
# 深审 medium「坏包窗口」的封口:批3 已把 resources 收窄为纯声明面后,锁缺席/
# 欠件 = main 可构建出「组件包全不可装」的安装包——本文件把「锁必须在、11 件
# 全覆盖、schema 自洽、resources 有映射」钉成 CI 红线,坏包窗口无法静默过闸。
# 真锁由 desktop/scripts/release-plugins-lock.mjs 产出(just release-plugins
# <tag> [--dry-run]);纪律:动过 plugins/myssia-* 源码必重跑产锁——锁钉的
# sha256 随树漂移,本文件不校验哈希与 dist 的一致性(dist 不入 git,发布时
# 由脚本同树重建+锁同写,确定性保证一致)。
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from myssia.plugins.remote import load_plugins_lock

REPO_ROOT = Path(__file__).resolve().parents[2]
LOCK_DIR = REPO_ROOT / "desktop" / "resources"
LOCK_PATH = LOCK_DIR / "plugins.lock.json"
TAURI_CONF = REPO_ROOT / "desktop" / "src-tauri" / "tauri.conf.json"
PLUGINS_DIR = REPO_ROOT / "plugins"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_installer_resources import ALL_BUNDLED_PACKAGES  # noqa: E402

#: 与锁 schema(remote.py _check_sha256)同口径:严格 64 位小写十六进制。
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_VERSION_RE = re.compile(r"^version:\s*(\S+)\s*$", re.MULTILINE)


def _load_committed_lock():
    """提交在树的真锁必须存在且过真实载入器(pydantic 自洽含 url 前缀互证)。"""
    assert LOCK_PATH.exists(), (
        f"{LOCK_PATH.relative_to(REPO_ROOT)} 缺席:批3 收窄后锁缺席=装机件组件包"
        "全不可装(坏包窗口);跑 just release-plugins <tag> --dry-run 产锁"
    )
    lock = load_plugins_lock(LOCK_DIR)
    assert lock is not None, "锁文件存在却载出 None(形态漂移,查 load_plugins_lock)"
    return lock


def test_lock_covers_exactly_all_bundled_packages():
    """锁条目恰覆盖随包组件包全集(欠件=该件不可装,多件=脏锁)。"""
    lock = _load_committed_lock()
    assert set(lock.assets) == set(ALL_BUNDLED_PACKAGES), (
        f"锁与随包清单漂移:缺 {set(ALL_BUNDLED_PACKAGES) - set(lock.assets)},"
        f"多 {set(lock.assets) - set(ALL_BUNDLED_PACKAGES)}"
    )


def test_lock_tag_is_release_shaped():
    """锁 tag 必须是 v 开头的 release 形态(资产 url 与 gh release 同 tag 语义)。"""
    lock = _load_committed_lock()
    assert lock.tag.startswith("v") and lock.tag[1:2].isdigit(), (
        f"锁 tag {lock.tag!r} 非 v* 形态;发布脚本 argv 约束被绕过或锁过期"
    )


def test_asset_entries_are_content_addressed():
    """每条目:严格小写 64hex 字节钉、size>0、url 落 {repo}/releases/download/{tag}/、
    version 与源树 plugin.yaml 一致(装机预显不骗人)。"""
    lock = _load_committed_lock()
    prefix = f"{lock.repo}/releases/download/{lock.tag}/"
    for plugin_id, asset in lock.assets.items():
        assert _SHA256_RE.fullmatch(asset.sha256), f"{plugin_id}: sha256 形态 {asset.sha256!r}"
        assert asset.size > 0, f"{plugin_id}: size 非正"
        assert asset.url == f"{prefix}plugin-{plugin_id}.tar.gz", f"{plugin_id}: url {asset.url!r}"
        yaml_path = PLUGINS_DIR / plugin_id / "plugin.yaml"
        yaml_text = yaml_path.read_text(encoding="utf-8")
        match = _VERSION_RE.search(yaml_text)
        assert match, f"{plugin_id}: 源树 plugin.yaml 无 version"
        assert asset.version == match.group(1), (
            f"{plugin_id}: 锁 version {asset.version!r} ≠ 源树 {match.group(1)!r}"
            "(动过源码未重跑 release-plugins 产锁)"
        )


def test_tauri_resources_maps_lock():
    """resources 必须映射锁件(批3 偏离记录①的收口:锁随真锁同船)。"""
    conf = json.loads(TAURI_CONF.read_text(encoding="utf-8"))
    resources = (conf.get("build") or {}).get("resources") or (conf.get("bundle") or {}).get(
        "resources"
    )
    assert isinstance(resources, dict), "tauri.conf.json resources 非 map 形态"
    assert resources.get("../resources/plugins.lock.json") == "plugins.lock.json", (
        "resources 缺 plugins.lock.json 映射——装机件带不上锁,组件包安装全落 "
        "plugin_lock_missing(坏包窗口)"
    )
