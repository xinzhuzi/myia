"""聊天媒体寻径与解密编排单测(task 10-14-wechat-media-sns R1/R2)。

夹具全合成(红线 6:零真实微信材料):合成 msg/ 树(attach/Img 三分支 +
video 明文)+ 合成 message 解密副本(Msg_<md5> 分表 + Name2Id)。外部解密件
= **真子进程**假件(tmp 下 shebang 脚本,toy 字节反转——与
examples/mediadecrypt_ref.py 同族;协议全链 spawn→NDJSON→退出码→magic
校验→缓存)。CLI 面(码表/配置/子命令)由集成员接线批后统一启用(见文件
尾 TestCliWiring 门控用例)。
"""

from __future__ import annotations

import hashlib
import os
import sqlite3
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

import wechat_bridge.media as media
from wechat_bridge.codes import DECRYPT_FAILED, BridgeError

NOW = int(time.time())
CHAT = "wxid_demo_chat"
JPEG_MAGIC = b"\xff\xd8\xff\xe0" + b"\x10JFIF" + b"\x00" * 26  # ≥16B 首字节可判


# ---------------------------------------------------------------------------
# 合成构件
# ---------------------------------------------------------------------------


def _proto_bytes(field: int, payload: bytes) -> bytes:
    """单字段 length-delimited protobuf(tag + varint 长度 + payload)。"""
    tag = (field << 3) | 2
    return bytes([tag]) + bytes([len(payload)]) + payload


def _key_blob(key: str) -> bytes:
    """packed_info_data 形状:外层字段包一层内层 32-hex 载荷(两级走读可中)。"""
    inner = _proto_bytes(2, key.encode("ascii"))
    return _proto_bytes(1, inner)


KEY1 = "a1b2c3d4e5f60718293a4b5c6d7e8f90"  # 缩略图+正图双在场
KEY2 = "b1b2c3d4e5f60718293a4b5c6d7e8f90"  # 仅正图
KEY3 = "c1b2c3d4e5f60718293a4b5c6d7e8f90"  # 全缺(文件缺失)
KEY4 = "d1b2c3d4e5f60718293a4b5c6d7e8f90"  # 视频


@pytest.fixture()
def fake_account(tmp_path: Path) -> dict:
    """合成账号:msg/ 明文树 + message 解密副本(Msg_<md5> 分表)。"""
    account = tmp_path / "wxid_demo_8253"
    db_storage = account / "db_storage"
    msg_root = account / "msg"
    month = time.strftime("%Y-%m", time.localtime(NOW))

    # —— msg/attach:<dir1(32hex)>/<yyyy-mm>/Img/<key>.dat|_t.dat ——
    dir1 = "e" * 32
    img_dir = msg_root / "attach" / dir1 / month / "Img"
    img_dir.mkdir(parents=True)
    (img_dir / f"{KEY1}_t.dat").write_bytes(b"enc-thumb-" + KEY1.encode())
    (img_dir / f"{KEY1}.dat").write_bytes(b"enc-full--" + KEY1.encode())
    (img_dir / f"{KEY2}.dat").write_bytes(b"enc-full--" + KEY2.encode())
    # KEY3 故意不放任何文件(文件缺失分支)

    # —— msg/video/<yyyy-mm>/<key>.mp4 + _thumb.jpg(明文)——
    video_dir = msg_root / "video" / month
    video_dir.mkdir(parents=True)
    (video_dir / f"{KEY4}.mp4").write_bytes(b"\x00\x00\x00\x18ftypisom" + b"v" * 32)
    (video_dir / f"{KEY4}_thumb.jpg").write_bytes(JPEG_MAGIC)

    # —— message 解密副本:4.1.15 分表形态 ——
    copy_root = tmp_path / "decrypted"
    msg_db = copy_root / "message" / "message_0.db"
    msg_db.parent.mkdir(parents=True)
    table = "Msg_" + hashlib.md5(CHAT.encode()).hexdigest()
    con = sqlite3.connect(msg_db)
    con.execute(
        f'CREATE TABLE "{table}" (local_id INTEGER PRIMARY KEY, server_id INTEGER, '
        "local_type INTEGER, sort_seq INTEGER, real_sender_id INTEGER, "
        "create_time INTEGER, status INTEGER, upload_status INTEGER, "
        "download_status INTEGER, server_seq INTEGER, origin_source TEXT, "
        "source TEXT, message_content TEXT, compress_content BLOB, "
        "packed_info_data BLOB, WCDB_CT_message_content INTEGER)"
    )
    rows = [
        # (local_type, packed, ts, real_sender_id)
        (3, _key_blob(KEY1), NOW - 600, 1),   # 图:thumb+full
        (3, _key_blob(KEY2), NOW - 700, 2),   # 图:仅正图
        (3, _key_blob(KEY3), NOW - 800, 2),   # 图:文件缺失
        (43, _key_blob(KEY4), NOW - 900, 2),  # 视频:明文
        (1, None, NOW - 1000, 2),             # 文本:只报形状
        (3, _key_blob(KEY1), NOW - 40 * 86400, 2),  # 窗口外:不进清单
    ]
    con.executemany(
        f'INSERT INTO "{table}" (local_type, packed_info_data, create_time, '
        "real_sender_id, message_content) VALUES (?,?,?,?,?)",
        [(t, p, ts, s, "") for t, p, ts, s in rows],
    )
    con.execute("CREATE TABLE Name2Id (user_name TEXT PRIMARY KEY, is_session INTEGER)")
    con.execute("INSERT INTO Name2Id VALUES (?, 1)", (CHAT,))
    con.commit()
    con.close()
    return {
        "account": account,
        "db_storage": db_storage,
        "msg_root": msg_root,
        "copy_dir": copy_root,
    }


def _write_provider(
    tmp_path: Path,
    *,
    ext: str | None = "jpg",
    mode: str = "ok",
    marker: Path | None = None,
) -> Path:
    """toy 假解密件(真子进程):字节反转 + 协议应答;mode 控制造错形态。"""
    body = f"""
import json, os, sys
req = json.loads(sys.stdin.readline())
marker = {repr(str(marker)) if marker else "None"}
if marker:
    with open(marker, "a") as fh:
        fh.write("spawn\\n")
if {mode!r} == "fail_result":
    print(json.dumps({{"type": "result", "success": False, "error": "件自报:钥不匹配", "logs": []}}), flush=True)
    sys.exit(0)
if {mode!r} == "crash":
    sys.stderr.write("件内崩溃明细一行\\n")
    sys.exit(3)
if {mode!r} == "no_result":
    print(json.dumps({{"type": "progress", "message": "半途而废", "level": 0}}), flush=True)
    sys.exit(0)
src = req["dat_path"] if req["action"] == "decrypt_dat" else req["in_path"]
out = req["out_path"]
data = open(src, "rb").read()
open(out, "wb").write(data[::-1])
print(json.dumps({{"type": "progress", "message": "解密中(假件)", "level": 0}}), flush=True)
print(json.dumps({{"type": "result", "success": True, "ext": {ext!r}, "is_wxgf": False,
                   "width": 640, "height": 480, "logs": ["toy=bytes-reverse"]}}), flush=True)
"""
    script = tmp_path / "fake-mediadecrypt.py"
    script.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
    script.chmod(0o755)
    return script


def _config(provider: str | None = None, capacity_mb: int = 2048) -> SimpleNamespace:
    """config duck-type 替身(接线批落 config.py 真键前的同形测试面)。"""
    return SimpleNamespace(
        media_decrypt_path=provider or "",
        media_cache_capacity_mb=capacity_mb,
    )


# ---------------------------------------------------------------------------
# key 提取(protobuf 走读)
# ---------------------------------------------------------------------------


class TestExtractKey:
    def test_two_level_walk_hits_32hex(self) -> None:
        assert media.media_extract_key(_key_blob(KEY1)) == KEY1

    def test_flat_field_and_non_key_shapes(self) -> None:
        assert media.media_extract_key(_proto_bytes(3, KEY2.encode())) == KEY2
        assert media.media_extract_key(_proto_bytes(3, b"not-hex!!")) is None
        assert media.media_extract_key(b"") is None
        assert media.media_extract_key(None) is None
        assert media.media_extract_key("text") is None

    def test_real_shape_lowercase_hex(self) -> None:
        key = "0123456789abcdef0123456789abcdef"
        assert media.media_extract_key(_key_blob(key)) == key


# ---------------------------------------------------------------------------
# R2 寻径(合成 msg/ 树三分支;黄金夹具)
# ---------------------------------------------------------------------------


class TestScanChatMedia:
    def _scan(self, fake: dict, days: int = 30) -> dict:
        payload = media.scan_chat_media(
            Path(fake["copy_dir"]), CHAT, days, media_root=Path(fake["msg_root"])
        )
        return payload["media"]

    def test_three_branches_and_shape(self, fake_account: dict) -> None:
        inner = self._scan(fake_account)
        items = inner["items"]
        by_key = {item.get("key"): item for item in items}
        # 图-双在场:缩略图与正图都解析出,状态待解密(缩略图优先呈现=字段在场)
        hit = by_key[KEY1]
        assert hit["type"] == "image"
        assert hit["files"]["thumb"].endswith(f"{KEY1}_t.dat")
        assert hit["files"]["full"].endswith(f"{KEY1}.dat")
        assert hit["status"] == media.STATUS_PENDING_DECRYPT
        # 图-仅正图:thumb=None 如实,仍待解密
        only_full = by_key[KEY2]
        assert only_full["files"]["thumb"] is None
        assert only_full["files"]["full"].endswith(f"{KEY2}.dat")
        assert only_full["status"] == media.STATUS_PENDING_DECRYPT
        # 图-文件缺失:双 None + 词面如实
        missing = by_key[KEY3]
        assert missing["files"] == {"thumb": None, "full": None}
        assert missing["status"] == media.STATUS_FILE_MISSING
        # 视频:明文直读零解密
        video = by_key[KEY4]
        assert video["type"] == "video"
        assert video["files"]["video"].endswith(f"{KEY4}.mp4")
        assert video["files"]["video_thumb"].endswith(f"{KEY4}_thumb.jpg")
        assert video["status"] == media.STATUS_PLAINTEXT_VIDEO
        # 其余类型只报形状(status=None)
        others = [i for i in items if i["type"] == "text"]
        assert len(others) == 1 and others[0]["status"] is None
        # 窗口外不进清单
        assert len([i for i in items if i["message_ref"]["ts"] < NOW - 30 * 86400]) == 0
        # 计数对账
        assert inner["stats"]["messages"] == 5
        assert inner["stats"]["image"] == 3
        assert inner["stats"]["video"] == 1
        assert inner["stats"]["other"] == 1
        assert inner["stats"]["image_file_missing"] == 1
        # 时间倒序(最新在前)
        times = [i["message_ref"]["ts"] for i in items]
        assert times == sorted(times, reverse=True)

    def test_sender_resolved_via_name2id(self, fake_account: dict) -> None:
        inner = self._scan(fake_account)
        senders = {i["message_ref"]["sender"] for i in inner["items"]}
        # real_sender_id 1/2 不在 Name2Id(rowid 只有隐式行 1=CHAT)→ 回落会话 id
        # Name2Id 只有 CHAT 一行(rowid=1)→ sender_id=1 反查为 CHAT,其余回落
        assert senders <= {CHAT}

    def test_month_fallback_glob(self, fake_account: dict) -> None:
        """月份段漂移(消息时间与文件月份错位)→ 全月 glob 兜底命中。"""
        account = Path(fake_account["account"])
        other_month_dir = account / "msg" / "attach" / ("f" * 32) / "1999-01" / "Img"
        other_month_dir.mkdir(parents=True)
        (other_month_dir / f"{KEY3}.dat").write_bytes(b"moved-full")
        inner = self._scan(fake_account)
        by_key = {item.get("key"): item for item in inner["items"]}
        assert by_key[KEY3]["status"] == media.STATUS_PENDING_DECRYPT
        assert by_key[KEY3]["files"]["full"].endswith(f"{KEY3}.dat")

    def test_message_copy_missing_raises(self, tmp_path: Path) -> None:
        with pytest.raises(BridgeError) as excinfo:
            media.scan_chat_media(
                tmp_path, CHAT, 30, media_root=tmp_path / "msg"
            )
        assert excinfo.value.exit_code == DECRYPT_FAILED


# ---------------------------------------------------------------------------
# R1 解密编排(真子进程假件:协议全链 + magic 校验 + 缓存幂等)
# ---------------------------------------------------------------------------


class TestDecryptOrchestration:
    @pytest.fixture()
    def provider_env(self, tmp_path: Path):
        marker = tmp_path / "spawns.txt"
        dat = tmp_path / "src.dat"
        dat.write_bytes(JPEG_MAGIC[::-1])  # toy 反转后 = JPEG 魔数
        provider = _write_provider(tmp_path, marker=marker)
        return {"marker": marker, "dat": dat, "provider": provider}

    def test_unconfigured_exit23_legal_message(self, provider_env, tmp_path):
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(
                provider_env["dat"], _config(), data_root=tmp_path
            )
        assert excinfo.value.exit_code == media.MEDIA_UNAVAILABLE == 23
        assert excinfo.value.message == media.MEDIA_DECRYPT_UNCONFIGURED_MESSAGE
        assert "media-decrypt set" in (excinfo.value.fix_hint or "")

    def test_missing_dat_usage(self, provider_env, tmp_path):
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(
                tmp_path / "nope.dat", _config(str(provider_env["provider"])),
                data_root=tmp_path,
            )
        assert excinfo.value.exit_code == 2

    def test_decrypt_success_cache_and_mode(self, provider_env, tmp_path):
        result = media.decrypt_dat_file(
            provider_env["dat"], _config(str(provider_env["provider"])),
            data_root=tmp_path,
        )
        assert result["cache"] == "miss"
        assert result["ext"] == "jpg"
        assert result["is_wxgf"] is False
        assert result["width"] == 640 and result["height"] == 480
        cached = Path(str(result["cached_path"]))
        assert cached.is_file()
        assert cached.read_bytes()[:4] == JPEG_MAGIC[:4]
        assert oct(cached.stat().st_mode & 0o777) == "0o600"
        assert oct(cached.parent.stat().st_mode & 0o777) == "0o700"

    def test_idempotent_second_run_zero_spawn(self, provider_env, tmp_path):
        cfg = _config(str(provider_env["provider"]))
        first = media.decrypt_dat_file(provider_env["dat"], cfg, data_root=tmp_path)
        second = media.decrypt_dat_file(provider_env["dat"], cfg, data_root=tmp_path)
        assert second["cache"] == "hit"
        assert second["cached_path"] == first["cached_path"]
        assert provider_env["marker"].read_text().count("spawn") == 1  # 二跑零 spawn

    def test_source_mtime_perturbation_redecrypts(self, provider_env, tmp_path):
        cfg = _config(str(provider_env["provider"]))
        media.decrypt_dat_file(provider_env["dat"], cfg, data_root=tmp_path)
        stat = provider_env["dat"].stat()
        os.utime(provider_env["dat"], (stat.st_atime, stat.st_mtime + 10))
        second = media.decrypt_dat_file(provider_env["dat"], cfg, data_root=tmp_path)
        assert second["cache"] == "miss"
        assert provider_env["marker"].read_text().count("spawn") == 2  # 源新重解

    def test_magic_mismatch_rejected(self, tmp_path):
        marker = tmp_path / "spawns.txt"
        dat = tmp_path / "src.dat"
        dat.write_bytes(JPEG_MAGIC[::-1])  # 反转后是 JPEG
        provider = _write_provider(tmp_path, ext="png", marker=marker)  # 声明 png = 不符
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(dat, _config(str(provider)), data_root=tmp_path)
        assert excinfo.value.exit_code == DECRYPT_FAILED
        assert "产物格式与声明不符" in excinfo.value.message
        # 拒收不落缓存:缓存目录无正式条目(仅 tmp 已清)
        cache_dir = media.cache_dir(tmp_path)
        leftovers = [p for p in cache_dir.iterdir() if not p.name.startswith(".")]
        assert leftovers == []

    def test_unknown_ext_rejected(self, tmp_path):
        dat = tmp_path / "src.dat"
        dat.write_bytes(JPEG_MAGIC[::-1])
        provider = _write_provider(tmp_path, ext="bmp")
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(dat, _config(str(provider)), data_root=tmp_path)
        assert excinfo.value.exit_code == DECRYPT_FAILED
        assert "未知产物格式" in excinfo.value.message

    def test_wxgf_exempt_from_magic_check(self, tmp_path):
        """wxgf 产物免魔数对照,原样保留(词面归消费方)。"""
        body = f"""
import json, sys
req = json.loads(sys.stdin.readline())
open(req["out_path"], "wb").write(b"wxgf-binary-not-jpeg")
print(json.dumps({{"type": "result", "success": True, "ext": "wxgf",
                   "is_wxgf": True, "width": None, "height": None, "logs": []}}), flush=True)
"""
        provider = tmp_path / "wxgf-provider.py"
        provider.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
        provider.chmod(0o755)
        dat = tmp_path / "src.dat"
        dat.write_bytes(b"whatever")
        result = media.decrypt_dat_file(
            dat, _config(str(provider)), data_root=tmp_path
        )
        assert result["ext"] == "wxgf"
        assert result["is_wxgf"] is True
        assert Path(str(result["cached_path"])).read_bytes() == b"wxgf-binary-not-jpeg"

    def test_provider_fail_result_transparent(self, tmp_path):
        dat = tmp_path / "src.dat"
        dat.write_bytes(JPEG_MAGIC[::-1])
        provider = _write_provider(tmp_path, mode="fail_result")
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(dat, _config(str(provider)), data_root=tmp_path)
        assert excinfo.value.exit_code == DECRYPT_FAILED
        assert "件自报:钥不匹配" in excinfo.value.message

    def test_provider_crash_stderr_tail_attached(self, tmp_path):
        dat = tmp_path / "src.dat"
        dat.write_bytes(JPEG_MAGIC[::-1])
        provider = _write_provider(tmp_path, mode="crash")
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(dat, _config(str(provider)), data_root=tmp_path)
        assert excinfo.value.exit_code == DECRYPT_FAILED
        assert "件内崩溃明细一行" in excinfo.value.message  # stderr 尾部附入
        assert "exit=3" in excinfo.value.message

    def test_provider_exit0_without_result(self, tmp_path):
        dat = tmp_path / "src.dat"
        dat.write_bytes(JPEG_MAGIC[::-1])
        provider = _write_provider(tmp_path, mode="no_result")
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(dat, _config(str(provider)), data_root=tmp_path)
        assert excinfo.value.exit_code == DECRYPT_FAILED
        assert "未返回结果" in excinfo.value.message

    def test_spawn_failure_exit23(self, tmp_path):
        dat = tmp_path / "src.dat"
        dat.write_bytes(JPEG_MAGIC[::-1])
        with pytest.raises(BridgeError) as excinfo:
            media.decrypt_dat_file(
                dat,
                _config(str(tmp_path / "not-executable.bin")),
                data_root=tmp_path,
            )
        assert excinfo.value.exit_code == media.MEDIA_UNAVAILABLE
        assert "启动失败" in excinfo.value.message


class TestCacheCapacity:
    def test_lru_removes_oldest_until_under_cap(self, tmp_path):
        directory = media.cache_dir(tmp_path)
        directory.mkdir(parents=True)
        mb = 1024 * 1024
        old = directory / "aaaa.dat"
        with old.open("wb") as fh:
            fh.truncate(int(1.5 * mb))  # 稀疏文件:旧且大
        fresh = directory / "bbbb.dat"
        fresh.write_bytes(b"y")
        os.utime(old, (NOW - 9999, NOW - 9999))
        stats = media.ensure_cache_capacity(directory, 1)
        assert not old.exists()  # 最旧先清
        assert fresh.exists()
        assert stats["removed"] == 1
        assert stats["files"] == 1
        assert stats["total_bytes"] == 1

    def test_under_cap_zero_removal(self, tmp_path):
        directory = media.cache_dir(tmp_path)
        directory.mkdir(parents=True)
        (directory / "a.dat").write_bytes(b"x" * 10)
        stats = media.ensure_cache_capacity(directory, 2048)
        assert stats["removed"] == 0 and stats["files"] == 1


# ---------------------------------------------------------------------------
# 编排:media scan --decrypt(逐条解密回填 + 幂等)与 media status
# ---------------------------------------------------------------------------


class TestScanOrchestration:
    @pytest.fixture()
    def wired(self, monkeypatch, tmp_path, fake_account):
        marker = tmp_path / "spawns.txt"
        # 密文 = toy 反转后 JPEG(KEY1 缩略图内容改成可解形态)
        for p in (Path(fake_account["msg_root"])).rglob(f"{KEY1}_t.dat"):
            p.write_bytes(JPEG_MAGIC[::-1])
        provider = _write_provider(tmp_path, marker=marker)
        copy_info = {"dir": str(fake_account["copy_dir"]), "built": [], "kept": []}
        monkeypatch.setattr(
            media, "ensure_decrypted_copies", lambda *a, **k: copy_info
        )
        return {
            "marker": marker,
            "provider": str(provider),
            "fake": fake_account,
            "config": _config(str(provider)),
            "data_root": tmp_path,
        }

    def test_scan_decrypt_refills_cached_path(self, wired):
        payload = media.media_scan_history(
            wired["config"],
            Path(wired["fake"]["db_storage"]),
            {},
            CHAT,
            30,
            decrypt=True,
            data_root=wired["data_root"],
        )
        inner = payload["media"]
        by_key = {item.get("key"): item for item in inner["items"]}
        assert by_key[KEY1]["status"] == media.STATUS_DECRYPTED
        assert by_key[KEY1].get("cached_path")
        # 解密失败项(KEY2 的密文反转后非 JPEG)→ 词面如实,不炸整轮
        assert by_key[KEY2]["status"] == media.STATUS_DECRYPT_FAILED
        assert inner["stats"]["decrypted"] == 1
        assert inner["stats"]["decrypt_failed"] == 1
        # 视频不解密、缺失项不解密;provider 节呈配置态
        assert by_key[KEY4]["status"] == media.STATUS_PLAINTEXT_VIDEO
        assert by_key[KEY3]["status"] == media.STATUS_FILE_MISSING
        assert inner["provider"]["configured"] is True

    def test_scan_decrypt_unconfigured_exit23(self, monkeypatch, wired):
        copy_info = {"dir": str(wired["fake"]["copy_dir"]), "built": [], "kept": []}
        monkeypatch.setattr(
            media, "ensure_decrypted_copies", lambda *a, **k: copy_info
        )
        with pytest.raises(BridgeError) as excinfo:
            media.media_scan_history(
                _config(),
                Path(wired["fake"]["db_storage"]),
                {},
                CHAT,
                30,
                decrypt=True,
                data_root=wired["data_root"],
            )
        assert excinfo.value.exit_code == media.MEDIA_UNAVAILABLE
        assert excinfo.value.message == media.MEDIA_DECRYPT_UNCONFIGURED_MESSAGE

    def test_scan_without_decrypt_never_spawns(self, wired):
        media.media_scan_history(
            wired["config"],
            Path(wired["fake"]["db_storage"]),
            {},
            CHAT,
            30,
            data_root=wired["data_root"],
        )
        assert not wired["marker"].exists() or wired["marker"].read_text() == ""


class TestMediaStatus:
    def test_unconfigured_and_configured_states(self, tmp_path):
        payload = media.media_status(_config(), data_root=tmp_path)
        inner = payload["media"]
        assert inner["provider"]["state"] == "unconfigured"
        assert inner["cache"]["files"] == 0

        provider = _write_provider(tmp_path)
        payload = media.media_status(_config(str(provider)), data_root=tmp_path)
        assert payload["media"]["provider"]["state"] == "configured"

    def test_missing_file_state(self, tmp_path):
        payload = media.media_status(
            _config(str(tmp_path / "gone.py")), data_root=tmp_path
        )
        assert payload["media"]["provider"]["state"] == "missing_file"

    def test_cache_counts(self, tmp_path):
        directory = media.cache_dir(tmp_path)
        directory.mkdir(parents=True)
        (directory / "a.jpg").write_bytes(b"x" * 100)
        (directory / ".tmp-1-x").write_bytes(b"y" * 50)  # tmp 不计
        payload = media.media_status(_config(), data_root=tmp_path)
        cache = payload["media"]["cache"]
        assert cache["files"] == 1
        assert cache["total_bytes"] == 100
        assert cache["capacity_mb"] == 2048
