"""scripts/wechat-bridge-mediadecrypt.py 算法位单测(全合成,零微信材料)。

覆盖面(红线:夹具全 mock/合成,不触任何真实微信数据):

- Isaac64:对参考 C(burtleburtle.net/bob/c/isaac64.c,Bob Jenkins 1996
  Public Domain)编译产物的消费序 KAT(黄金向量内嵌)+ 确定性/种子敏感/
  自逆往返;
- .dat 三形态:V2(每用户 AES 钥)/V1(固定钥)/legacy(整文件 XOR)
  的合成加密→解密往返;头部字段不自洽拒解;V2 缺钥人话报错;
- 钥推导:单字节 XOR 钥标志计票(JPEG/PNG 成对标志)、xor_key/aes_key
  intake 解析形态;
- 协议子进程壳:decrypt_dat/decrypt_stream 全链(stdin 单行 JSON →
  NDJSON progress+result → out_path 产物;缺钥失败形态)。
"""

from __future__ import annotations

import importlib.util
import json
import struct
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "wechat-bridge-mediadecrypt.py"

#: 合成 V2 每用户钥(16 ASCII;测试值,非任何真实钥)。
TEST_AES_KEY = "unit-test-key-01"
TEST_AES_KEY_B = TEST_AES_KEY.encode("ascii")
#: 合成 XOR 钥(避开 0x00/0xFF 常见值)。
TEST_XOR_KEY = 0x5A

#: 合成 JPEG 载荷:魔数 + SOI 后续段标志若干 + 长尾(含 EOI 配对标志)。
_SYNTH_JPEG = (
    b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00\x48\x00\x48"
    + b"\x00" * 1008          # 补足 1024 字节「图像头」段
    + b"\x11" * 16             # 中段明文 16 字节
    + b"\x99" * 512 + b"\xff\xd9\xff\xda" + b"\x77" * 128 + b"\xff\xd9" + b"\x33" * 64
)


def _load_module():
    spec = importlib.util.spec_from_file_location("wechat_bridge_mediadecrypt", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def md():
    return _load_module()


def _xor(data: bytes, key: int) -> bytes:
    return bytes(byte ^ key for byte in data)


def _aes_ecb_encrypt(plaintext: bytes, key: bytes, *, nopad_to: int | None = None) -> bytes:
    """合成加密助手:nopad_to=密文区长度(不足补任意字节,模拟对齐密文)。"""
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

    data = plaintext
    if nopad_to is not None:
        data = plaintext + b"\xA5" * (nopad_to - len(plaintext))
    encryptor = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    return encryptor.update(data) + encryptor.finalize()


def _build_container(plain: bytes, *, v2: bool, aes_key: bytes, xor_key: int,
                     aes_size: int = 1024) -> bytes:
    """按实测形态合成 V2/V1 容器:15B 头 + AES 段 + 中段 16B + 尾段 XOR。"""
    magic = b"\x07\x08V2\x08\x07" if v2 else b"\x07\x08V1\x08\x07"
    head = plain[:aes_size]
    middle = plain[aes_size:aes_size + 16]
    tail = plain[aes_size + 16:]
    ct_len = (aes_size + 15) // 16 * 16
    ciphertext = _aes_ecb_encrypt(head, aes_key, nopad_to=ct_len)
    header = magic + struct.pack("<II", aes_size, len(tail)) + b"\x01"
    return header + ciphertext + middle + _xor(tail, xor_key)


# ---------------------------------------------------------------------------
# Isaac64:参考 C KAT + 结构性质
# ---------------------------------------------------------------------------

#: 消费序前 16 qword 黄金向量(参考 C 编译产物 /tmp 生成后内嵌;种子循环
#: 填充 2048 字节种子缓冲,randinit(TRUE))。
_KAT = {
    b"": "9d39247e33776d412af7398005aaa5c744db0150246235479c15f73e62a76ae2"
         "75834465489c0c893290ac3a203001bf0fbbad1f61042279e83a908ff2fb60c"
         "a0d7e765d58755c101a083822ceafe02d9605d5f0e25ec3b0d021ff5cd13a2e"
         "d540bdf15d4a672e32011355146fd563955db4832046f3d9e5239f8b2d7ff719cc",
    b"1234567890": "3feba15e16ae6455b6afbd9672ba9740ecaf263a607852a05f6a973889c07f2"
                   "3743dbcfd715061df8162f91c206f9fb46df3d3d7db5756d6a17762c076aa074e"
                   "d23107c319d0b73a2ce10aee873ebde5f3d8a7aad64ed8fd9a8c4cbb16b41d1d"
                   "851b19880f7ad39be650f7ab468f6de5311e32315e6b522cc5b8c26fdc0e25fb",
    b"7": "6960dd421118bf673c099b14c88e598db99a3c54d72dda93887575c6e5cb5744"
         "d21005ae2166e3fe7196df56249b2220785cfd4dff516ea896f95a8d5df5f7c3"
         "2495cd20d120ca507e9995a5eef1f11e217e5d075234ac59372d6fa0aea12be4"
         "bca4d186449c60110ea21acd18fc06980358372d9fae9820a6fec48ed0746912",
}


class TestIsaac64:
    @pytest.mark.parametrize("seed", list(_KAT))
    def test_kat_against_reference_c(self, md, seed):
        gen = md._Isaac64(seed)
        got = "".join(f"{gen.next_qword():016x}" for _ in range(16))
        assert got == _KAT[seed]

    def test_deterministic_and_seed_sensitive(self, md):
        a1 = "".join(f"{md._Isaac64(b'42').next_qword():016x}" for _ in range(4))
        a2 = "".join(f"{md._Isaac64(b'42').next_qword():016x}" for _ in range(4))
        b = "".join(f"{md._Isaac64(b'43').next_qword():016x}" for _ in range(4))
        assert a1 == a2
        assert a1 != b

    def test_keystream_roundtrip_and_length(self, md):
        payload = b"\xAB" * 5000  # 跨 2+ 轮(每轮 2048 字节)
        enc = md.decrypt_stream(payload, "998877")
        assert len(enc) == len(payload)
        assert enc != payload
        assert md.decrypt_stream(enc, "998877") == payload

    def test_stream_empty_key_rejected(self, md):
        with pytest.raises(md.DecryptError):
            md.decrypt_stream(b"\x00" * 8, "")


# ---------------------------------------------------------------------------
# .dat 三形态:识别 + 往返 + 拒解
# ---------------------------------------------------------------------------


class TestDecryptDat:
    def test_v2_roundtrip_full(self, md):
        dat = _build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY)
        keys = {"aes_key": TEST_AES_KEY, "xor_key": hex(TEST_XOR_KEY)}
        assert md.decrypt_dat(dat, keys) == _SYNTH_JPEG

    def test_v2_roundtrip_derived_xor_key(self, md):
        """xor_key 缺省 → 尾段标志计票自推(合成尾含 FFD9/FFDA 配对)。"""
        dat = _build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY)
        assert md.decrypt_dat(dat, {"aes_key": TEST_AES_KEY}) == _SYNTH_JPEG

    def test_v2_unaligned_aes_size(self, md):
        """aes_size 非 16 对齐(实测余量样本 780~1006)→ ceil 密文区+截断。"""
        plain = _SYNTH_JPEG[:780] + b"\x11" * 16 + _SYNTH_JPEG[796:]
        dat = _build_container(plain, v2=True, aes_key=TEST_AES_KEY_B,
                               xor_key=TEST_XOR_KEY, aes_size=780)
        assert md.decrypt_dat(dat, {"aes_key": TEST_AES_KEY, "xor_key": hex(TEST_XOR_KEY)}) == plain

    def test_v2_requires_user_aes_key(self, md):
        dat = _build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY)
        with pytest.raises(md.DecryptError) as excinfo:
            md.decrypt_dat(dat, {})
        assert "每用户" in str(excinfo.value) and "WX_MEDIA_AES_KEY" in str(excinfo.value)

    def test_v1_fixed_key_roundtrip(self, md):
        dat = _build_container(_SYNTH_JPEG, v2=False, aes_key=md._V1_FIXED_AES_KEY, xor_key=0x37)
        assert md.decrypt_dat(dat, {}) == _SYNTH_JPEG

    def test_legacy_roundtrip_and_derivation(self, md):
        dat = _xor(_SYNTH_JPEG[:2048], TEST_XOR_KEY)
        assert md.decrypt_dat(dat, {}) == _SYNTH_JPEG[:2048]

    def test_legacy_anchor_fallback(self, md):
        """计票无峰的短 legacy 载荷 → 首字节锚(密文首^0xFF=JPEG 魔数首)。"""
        plain = b"\xff\xd8\xff\xe0" + b"\x55" * 32
        dat = _xor(plain, 0xC3)
        assert md.decrypt_dat(dat, {}) == plain

    def test_bad_version_byte_rejected(self, md):
        dat = _build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY)
        dat = b"\x07\x08V2\x08\x07" + struct.pack("<II", 1024, 100) + b"\x02" + dat[15:]
        with pytest.raises(md.DecryptError, match="版本字节"):
            md.decrypt_dat(dat, {"aes_key": TEST_AES_KEY})

    def test_inconsistent_header_rejected(self, md):
        header = b"\x07\x08V2\x08\x07" + struct.pack("<II", 10**9, 100) + b"\x01"
        with pytest.raises(md.DecryptError, match="不自洽"):
            md.decrypt_dat(header + b"\x00" * 64, {"aes_key": TEST_AES_KEY})

    def test_too_short_rejected(self, md):
        with pytest.raises(md.DecryptError, match="过短"):
            md.decrypt_dat(b"\x07\x08V2\x08\x07" + b"\x00" * 20, {"aes_key": TEST_AES_KEY})


# ---------------------------------------------------------------------------
# 钥推导与 intake 解析
# ---------------------------------------------------------------------------


class TestKeyDerivation:
    def test_derive_xor_key_jpeg_markers(self, md):
        tail = _xor(b"\x99" * 64 + b"\xff\xd9" + b"\x88" * 8 + b"\xff\xda" + b"\x77" * 8 + b"\xff\xd9", 0xE9)
        assert md.derive_xor_key(tail) == 0xE9

    def test_derive_xor_key_png_markers(self, md):
        tail = _xor(b"\x00" * 16 + b"IDAT" + b"\xDE" * 24 + b"IDAT" + b"\xAD" * 8 + b"IEND", 0x3C)
        assert md.derive_xor_key(tail) == 0x3C

    def test_derive_xor_key_no_peak_returns_none(self, md):
        # 字节对差 {0,2,8} 均不命中标志差集 → 计票零票;尾亦非 EOI/IEND 锚
        assert md.derive_xor_key(b"\x00\x02\x00\x08" * 64) is None
        assert md.derive_xor_key(b"\x01") is None

    def test_derive_xor_key_end_anchor_fallback(self, md):
        """计票不足但密文尾严格=EOI/IEND CRC 异或 → 尾锚推钥(勘察缩略图法)。"""
        plain = b"\x42" * 64 + b"\xff\xd9"  # 无内部标志对(42 差 0)
        tail = _xor(plain, 0x77)
        assert md.derive_xor_key(tail) == 0x77
        png_tail = _xor(b"\xDE" * 60 + b"\xae\x42\x60\x82", 0x21)
        assert md.derive_xor_key(png_tail) == 0x21

    def test_parse_xor_key_forms(self, md):
        assert md._parse_xor_key("0xE9") == 0xE9
        assert md._parse_xor_key("E9") == 0xE9
        assert md._parse_xor_key("e9") == 0xE9
        assert md._parse_xor_key("233") == 0xE9
        assert md._parse_xor_key("") is None
        assert md._parse_xor_key("zz") is None
        assert md._parse_xor_key("1000") is None  # 超单字节

    def test_parse_aes_key_forms(self, md):
        assert md._parse_aes_key(TEST_AES_KEY) == TEST_AES_KEY_B
        assert md._parse_aes_key("00112233445566778899aabbccddeeff") == bytes.fromhex("00112233445566778899aabbccddeeff")
        assert md._parse_aes_key("short") is None
        assert md._parse_aes_key("00112233445566778899aabbccddeefg") is None


# ---------------------------------------------------------------------------
# 协议子进程壳(真子进程:stdin 单行 JSON → NDJSON → 退出码)
# ---------------------------------------------------------------------------


def _run_provider(request: dict, env_extra: dict[str, str] | None = None) -> tuple[list[dict], dict | None, int]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=json.dumps(request) + "\n",
        capture_output=True, text=True, timeout=60,
        env={**{k: v for k, v in __import__("os").environ.items()
                if not k.startswith("WX_MEDIA_")}, **(env_extra or {})},
    )
    lines = [json.loads(ln) for ln in proc.stdout.splitlines() if ln.strip()]
    result = next((obj for obj in reversed(lines) if obj.get("type") == "result"), None)
    return lines, result, proc.returncode


class TestProtocolShell:
    def test_decrypt_dat_v2_success(self, tmp_path):
        dat = tmp_path / "synth.dat"
        dat.write_bytes(_build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY))
        out = tmp_path / "out.bin"
        lines, result, rc = _run_provider(
            {"action": "decrypt_dat", "dat_path": str(dat), "out_path": str(out)},
            {"WX_MEDIA_AES_KEY": TEST_AES_KEY, "WX_MEDIA_XOR_KEY": hex(TEST_XOR_KEY)},
        )
        assert rc == 0
        assert result is not None and result["success"] is True
        assert result["ext"] == "jpg"
        assert out.read_bytes() == _SYNTH_JPEG
        assert lines[-1] is result  # result 恰为最后一行

    def test_decrypt_dat_v2_missing_key_human_error(self, tmp_path):
        dat = tmp_path / "synth.dat"
        dat.write_bytes(_build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY))
        lines, result, rc = _run_provider(
            {"action": "decrypt_dat", "dat_path": str(dat), "out_path": str(tmp_path / "out.bin")},
            # 测试洁净性(10-18):宿主机钥匙串可能已供真媒体钥(生产件内
            # 自理通道),缺钥人话路径须隔离两通道——WX_MEDIA_SKIP_COMPONENT。
            {"WX_MEDIA_SKIP_COMPONENT": "1"},
        )
        assert rc == 0  # 协议 §6:failure result + 退 0
        assert result is not None and result["success"] is False
        assert "每用户" in result["error"]

    def test_decrypt_stream_roundtrip(self, tmp_path):
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # noqa: F401
        payload = md_stream_plain = b"\xff\xd8\xff\xe0" + b"\x42" * 300
        keystream = _load_module()._isaac64_keystream("12345", len(payload))
        cipher = bytes(p ^ k for p, k in zip(payload, keystream))
        src = tmp_path / "cdn.bin"
        src.write_bytes(cipher)
        out = tmp_path / "out.bin"
        lines, result, rc = _run_provider(
            {"action": "decrypt_stream", "in_path": str(src), "key": "12345", "out_path": str(out)}
        )
        assert rc == 0
        assert result is not None and result["success"] is True
        assert result["ext"] == "jpg"
        assert out.read_bytes() == md_stream_plain

    def test_unknown_action_rejected(self):
        lines, result, rc = _run_provider({"action": "bogus"})
        assert result is not None and result["success"] is False
        assert "未知动作" in result["error"]


class TestComponentKeyIntake:
    """件内自理双通道(钥匙串+数据根文件;2026-10-15 落地)。"""

    def test_data_root_channel_e2e(self, tmp_path):
        """桥 spawn 形态(MYIA_HOME 指数据根,零 argv/env 钥)走文件通道。"""
        root = tmp_path / "MYIA_HOME"
        (root / "wechat-bridge").mkdir(parents=True)
        (root / "wechat-bridge" / "media-keys.json").write_text(
            json.dumps({"aes_key": TEST_AES_KEY, "xor_key": hex(TEST_XOR_KEY)}),
            encoding="utf-8",
        )
        dat = tmp_path / "synth.dat"
        dat.write_bytes(_build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY))
        out = tmp_path / "out.bin"
        lines, result, rc = _run_provider(
            {"action": "decrypt_dat", "dat_path": str(dat), "out_path": str(out)},
            # 只跳钥匙串通道(宿主真钥会让位测试钥的先到先得序);数据根通道
            # 本测的被测面,保留(WX_MEDIA_SKIP_KEYCHAIN,10-18 seam)。
            {"MYIA_HOME": str(root), "WX_MEDIA_SKIP_KEYCHAIN": "1"},
        )
        assert rc == 0
        assert result is not None and result["success"] is True
        assert out.read_bytes() == _SYNTH_JPEG

    def test_missing_key_hermetic_via_skip_component(self, tmp_path):
        """SKIP_COMPONENT 旁路=洁净零钥环境;人话报错须指明三供钥通道。"""
        dat = tmp_path / "synth.dat"
        dat.write_bytes(_build_container(_SYNTH_JPEG, v2=True, aes_key=TEST_AES_KEY_B, xor_key=TEST_XOR_KEY))
        lines, result, rc = _run_provider(
            {"action": "decrypt_dat", "dat_path": str(dat), "out_path": str(tmp_path / "o.bin")},
            {"MYIA_HOME": str(tmp_path), "WX_MEDIA_SKIP_COMPONENT": "1"},
        )
        assert rc == 0
        assert result is not None and result["success"] is False
        assert "media-keys" in result["error"] and "WX_MEDIA_AES_KEY" in result["error"]

    def test_keychain_channel_parses_json(self, monkeypatch):
        """钥匙串通道:security 成功回 JSON → 解析为钥匙;值不落 stderr。"""
        module = _load_module()

        class Proc:
            returncode = 0
            stdout = json.dumps({"aes_key": "kc-key-123456789"}).encode()

        monkeypatch.setattr(module.subprocess, "run", lambda *a, **k: Proc())
        keys = module._component_keys_from_keychain()
        assert keys == {"aes_key": "kc-key-123456789"}

    def test_keychain_bad_json_silent_fallback(self, monkeypatch, capsys):
        """钥匙串有内容但非 JSON → 静默归零命中(不抛、不回显值)。"""
        module = _load_module()

        class Proc:
            returncode = 0
            stdout = b"not-json{"
        monkeypatch.setattr(module.subprocess, "run", lambda *a, **k: Proc())
        assert module._component_keys_from_keychain() == {}
        assert "kc-key" not in capsys.readouterr().err

    def test_keychain_not_found_returns_empty(self, monkeypatch):
        module = _load_module()

        class Proc:
            returncode = 44
            stdout = b""
        monkeypatch.setattr(module.subprocess, "run", lambda *a, **k: Proc())
        assert module._component_keys_from_keychain() == {}

    def test_manual_env_overrides_component(self, monkeypatch):
        """合并序:手动 env 显式供给覆盖件内自理(调试语义)。"""
        module = _load_module()
        monkeypatch.setenv("MYIA_HOME", "/nonexistent-selfkey-test")
        monkeypatch.setenv("WX_MEDIA_AES_KEY", "manual-wins-key0")
        monkeypatch.setattr(
            module, "_component_keys_from_keychain",
            lambda: {"aes_key": "kc-key-123456789"},
        )
        keys = module.load_keys(None)
        assert keys["aes_key"] == "manual-wins-key0"

    def test_data_root_loose_perms_warns_but_supplies(self, tmp_path, monkeypatch, capsys):
        """权限过宽只提醒不拦解密(钥匙仍供给)。"""
        module = _load_module()
        root = tmp_path / "root"
        (root / "wechat-bridge").mkdir(parents=True)
        kf = root / "wechat-bridge" / "media-keys.json"
        kf.write_text(json.dumps({"xor_key": "5A"}), encoding="utf-8")
        kf.chmod(0o644)
        monkeypatch.setenv("MYIA_HOME", str(root))
        monkeypatch.setattr(module, "_component_keys_from_keychain", lambda: {})
        keys = module.load_keys(None)
        assert keys == {"xor_key": "5A"}
        assert "chmod 600" in capsys.readouterr().err
