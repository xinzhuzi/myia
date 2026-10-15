#!/usr/bin/env python3
"""微信媒体解密件——生产件(协议壳 + 实测算法落地)。

本件 = docs/wechat-mediadecrypt.md v1 协议的生产件:照
plugins/wechat-bridge/examples/mediadecrypt_ref.py 的协议形状
(stdin 单行 JSON → stdout NDJSON:progress 0..N + result 恰一次 → 退出码
按协议 §6 矩阵;失败姿势同 ref:result ``success:false`` + 退出码 0)。
``decrypt_dat`` / ``decrypt_stream`` 两算法位已按**本仓勘察结论 +
生态逆向记录(只学思想,零抄码)**填入。

算法形态(勘察实录:mac WeChat 4.1.15 Build 270135,本机 20000 dat 全 V2;
参考思想源 = ZedeX/weixin-decrypte-script 与 liuggchen/wechatDatDecode
(均无 LICENSE,仅对齐算法形态)、lc044.love/post/16 逆向记录):

- **V2 容器**(4.0.3+,当前主力):头 15 字节 = 魔数 ``07 08 56 32 08 07``
  (\x07\x08V2\x08\x07)+ u32LE aes_size + u32LE xor_size + 版本字节 0x01;
  payload 分三段:①[15,15+aes) 图像头 **AES-128-ECB**(钥=每用户 16 字节
  ASCII,本机实测全库同一把,须自外部供给——参考形态为从运行中的微信进程
  内存提取,属进程内存取证,本件不含提取器);②中段明文透传;③尾部
  xor_size 字节**单字节 XOR**(本机钥 0xE9,可由 JPEG/PNG 标志异或计票
  自推,见 ``derive_xor_key``)。
- **V1 容器**(4.0~4.0.2):同构三段,唯 AES 钥为公开固定钥
  ``cfcd208495d565ef``(md5('0') 前 16 hex 字符;2025-04-01 起换 V2 钥,
  本机实测旧钥解不开 V2 样本)。
- **legacy**(3.x):无头,整文件单字节 XOR,钥 = 首字节 ^ 图像魔数首字节。
- **decrypt_stream**:朋友圈 CDN 流按 Isaac64 keystream XOR(协议文档 §2/
  WeFlow 判例);Isaac64 = Bob Jenkins 1996 Public Domain,照参考 C 机械
  移植并与参考编译产物 KAT 对齐(测试内嵌黄金向量)。**seeding 形态为本件
  约定**(数字串字节循环填充 2048 字节种子缓冲,randinit(TRUE);消费序按
  参考 rand() 宏 = 每轮 randrsl 降序,qword 小端展开)——本仓无 CDN 实测
  样本,该约定未经真流验证,与真流不符时按实测调整 seeding 即可。

落位纪律(勿动):

- 本件落位仓根 ``scripts/``——**不随产品包分发**(app resources 白名单不含
  仓根 ``scripts/``,亦无 CI 复制钩子)。
- **本件永不放入 ``plugins/wechat-bridge/`` 目录**——该目录是 tauri 整目录
  复制面(desktop/src-tauri/tauri.conf.json:94 resources 映射
  ``"../../plugins/wechat-bridge": "components/wechat-bridge"``),放进去
  即随产品包分发。**解密产物永不写进本件所在目录**(只写请求的 out_path)。

钥匙 intake 钩(仅手动联调形态有效;边界如实):

- 钩 = env ``WX_MEDIA_XOR_KEY`` / ``WX_MEDIA_AES_KEY`` 或 ``--key-file``
  (JSON,字段 ``xor_key``/``aes_key``)——钥匙**仅内存过手、零落盘、零
  日志**:永不写盘、永不进 result/logs/stderr。
- ``xor_key`` 形态:单字节,``0xE9``/``E9``/``233`` 均可;缺省时按尾部
  JPEG/PNG 标志异或计票自推(推不出 → 人话报错,见 ``derive_xor_key``)。
- ``aes_key`` 形态:V2 每用户钥 = 16 字节 ASCII;或 32 位 hex 串(自动
  解码为 16 字节)。V1 固定钥件内自带,无需供给。
- 但 env/--key-file **仅手动联调形态有效**:桥 spawn 链 argv 恒只传件
  路径零参数(media.py:254-260 ``subprocess.Popen([str(exe)])``,无
  ``env=`` 显式传参),``--key-file`` 在桥链上永远收不到;世事.app 为
  macOS GUI app(launchd 起),用户 shell export 的 env 不进桥进程。
  钥匙进真实件的现实通道 = **件内自理**:件内写死路径/自带钥匙文件约定
  (docs/wechat-mediadecrypt.md §2/§4「钥匙=件内自理」)。

依赖:AES 用 ``cryptography``(本仓 uv 锁内在,经 pyopenssl/secretstorage
传递引入);不可用时回落 ``openssl enc -d -aes-128-ecb`` CLI,再不可用则
人话报错。Isaac64 纯 Python 无三方依赖。

手动联调(不经桥):

.. code-block:: bash

    chmod +x scripts/wechat-bridge-mediadecrypt.py
    echo '{"action":"decrypt_dat","dat_path":"/abs/a.dat","out_path":"/tmp/out"}' \\
        | ./scripts/wechat-bridge-mediadecrypt.py
    # V2 样本需先供钥:WX_MEDIA_AES_KEY=<16字> [WX_MEDIA_XOR_KEY=0xE9]

接进桥(接线闭环验收):

    wechat-bridge localdb media-decrypt set /abs/path/scripts/wechat-bridge-mediadecrypt.py
    wechat-bridge localdb media decrypt /abs/a.dat --json
"""

from __future__ import annotations

import argparse
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

#: 协议 v1 合法动作(docs §4)。
_ACTIONS = ("decrypt_dat", "decrypt_stream")

#: --key-file 的 JSON 字段名(仅手动联调形态;见模块头注边界)。
_KEY_FILE_FIELDS = ("xor_key", "aes_key")


def emit(obj: dict) -> None:
    """stdout 按行输出协议 NDJSON(写行即 flush——桥流式可读,协议 §5)。"""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def fail(message: str, logs: list[str] | None = None) -> int:
    """失败形态 result + 退出码 0(协议 §6 推荐姿势:catch 后退 0)。"""
    emit({"type": "result", "success": False, "error": message, "logs": logs or []})
    return 0


# ═══════════════════════════════════════════════════════════════════
# 钥匙 intake(仅手动联调形态有效;边界见模块头注;零落盘零日志)
# ═══════════════════════════════════════════════════════════════════


def load_keys_manual(key_file: str | None) -> dict[str, str]:
    """手动联调形态的钥匙 intake:env WX_MEDIA_XOR_KEY/WX_MEDIA_AES_KEY
    或 --key-file(JSON:{xor_key,aes_key})。

    钥匙仅内存过手:零落盘、零日志——返回值只在本进程内存里流转,永不
    写盘、永不进 result/logs/stderr(诊断只可报「有无」布尔,不报值)。
    """
    keys: dict[str, str] = {}
    for field, env_name in (
        ("xor_key", "WX_MEDIA_XOR_KEY"),
        ("aes_key", "WX_MEDIA_AES_KEY"),
    ):
        value = (os.environ.get(env_name) or "").strip()
        if value:
            keys[field] = value
    if key_file:
        try:
            data = json.loads(Path(key_file).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            # 走 stderr 调试旁路 + 非 0 退出(手动联调形态才会到这里;
            # 协议 §6:无 result 非 0 退出 = 失败,stderr 尾部附入)。
            sys.stderr.write(f"--key-file 读取/解析失败(须 JSON,字段 {_KEY_FILE_FIELDS}): {exc}\n")
            raise SystemExit(2) from exc
        if isinstance(data, dict):
            for field in _KEY_FILE_FIELDS:
                value = str(data.get(field) or "").strip()
                if value:
                    keys[field] = value
    return keys


# ═══════════════════════════════════════════════════════════════════
# 算法位 A:聊天图片 .dat(V2/V1 三段容器 + legacy 整文件 XOR)
# —— 形态锚:本仓勘察(4.1.15 真机 20000 dat)+ lc044/ZedeX/liuggchen
#    生态记录(只学思想,零抄码)
# ═══════════════════════════════════════════════════════════════════


class DecryptError(Exception):
    """算法位人话失败(被 run_action 接进协议 result success:false)。"""


_DAT_V1_MAGIC = b"\x07\x08V1\x08\x07"
_DAT_V2_MAGIC = b"\x07\x08V2\x08\x07"
_DAT_HEADER_LEN = 15
_DAT_HEADER_VER = 0x01
#: V1(4.0~4.0.2)公开固定钥 = md5('0') 前 16 hex 字符(生态记录;本机
#: 实测其解不开 V2——2025-04-01 起已换代)。
_V1_FIXED_AES_KEY = b"cfcd208495d565ef"
_AES_BLOCK = 16

#: 尾段计票用的成对标志(异或差与钥无关,计票法见 derive_xor_key):
#: JPEG EOI/SOS/DHT/DQT/SOF(基线+渐进)+ PNG 块名。
_TAIL_MARKER_PAIRS = (
    b"\xff\xd9", b"\xff\xda", b"\xff\xc4", b"\xff\xdb",
    b"\xff\xc0", b"\xff\xc2", b"\xff\xc8", b"\xff\xc9",
    b"IDAT", b"IEND", b"IHDR", b"PLTE",
)
#: legacy(3.x)整文件 XOR 的首字节锚:密文首 ^ 键 = 图像魔数首字节。
_LEGACY_HEAD_ANCHORS = (0xFF, 0x89, ord("G"), ord("B"), ord("R"))


def derive_xor_key(tail: bytes) -> int | None:
    """单字节 XOR 钥自推:成对标志异或差计票 + 严格尾锚兜底(勘察法)。

    计票原理:两字节标志 m=(a,b) 在密文里呈现为 (a^k, b^k),其异或差
    a^b 与钥无关——遍历相邻字节对,差命中标志差的位点上给
    ``tail[i]^a`` 投一票;真钥聚合全部真标志票,背景票散布在各键
    (n×标志差数/256/256 量级/键)。判峰:≥3 票且绝对领先次名 ≥2。
    计票无峰时回落严格尾锚:缩略图/正图密文尾与已知尾标志异或自洽
    (JPEG EOI=FF D9 两字节;PNG IEND CRC=AE 42 60 82 四字节)——
    勘察即以缩略图尾 EOI 异或推钥(98% 命中)。皆不成 → None。
    """
    if len(tail) < 2:
        return None
    by_diff: dict[int, list[int]] = {}
    for marker in _TAIL_MARKER_PAIRS:
        by_diff.setdefault(marker[0] ^ marker[1], []).append(marker[0])
    votes = [0] * 256
    prev = tail[0]
    for byte in tail[1:]:
        heads = by_diff.get(prev ^ byte)
        if heads is not None:
            for head in heads:
                votes[prev ^ head] += 1
        prev = byte
    best = max(range(256), key=votes.__getitem__)
    runner = max((v for k, v in enumerate(votes) if k != best), default=0)
    if votes[best] >= 3 and votes[best] - runner >= 2:
        return best
    for anchor_len, anchor in ((2, b"\xff\xd9"), (4, b"\xae\x42\x60\x82")):
        if len(tail) >= anchor_len:
            key = tail[-anchor_len] ^ anchor[0]
            if bytes(byte ^ key for byte in tail[-anchor_len:]) == anchor:
                return key
    return None


def _parse_xor_key(text: str | None) -> int | None:
    """intake 形态解析:``0xE9``/``E9`` 按 hex;纯数字超单字节时回十进制。"""
    if text is None:
        return None
    value = text.strip()
    if not value:
        return None
    try:
        key = int(value, 0) if value.lower().startswith(("0x", "0o", "0b")) else int(value, 16)
    except ValueError:
        return None
    if 0 <= key <= 0xFF:
        return key
    if value.isdigit():  # ``233`` 十进制回退(hex=0x233 超界)
        key = int(value, 10)
        return key if 0 <= key <= 0xFF else None
    return None


def _parse_aes_key(text: str | None) -> bytes | None:
    """intake 形态解析:16 字节 ASCII 直用;32 位 hex 串自动解码。"""
    if text is None:
        return None
    value = text.strip()
    if len(value) == _AES_BLOCK:
        return value.encode("latin-1")
    if len(value) == 2 * _AES_BLOCK:
        try:
            decoded = bytes.fromhex(value)
        except ValueError:
            return None
        if len(decoded) == _AES_BLOCK:
            return decoded
    return None


def _aes_ecb_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """AES-128-ECB 解密:cryptography 优先,openssl CLI 回落,再败人话。"""
    if not ciphertext or len(ciphertext) % _AES_BLOCK:
        raise DecryptError(
            f"AES 段长度非法({len(ciphertext)} 字节,须 16 的倍数)——头部字段不自洽"
        )
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

        decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    except ImportError:
        pass
    try:
        proc = subprocess.run(
            ["openssl", "enc", "-d", "-aes-128-ecb", "-nopad", "-K", key.hex()],
            input=ciphertext, capture_output=True, check=False,
        )
    except OSError as exc:
        raise DecryptError(
            "AES 后端不可用(无 cryptography 包且 openssl CLI 拉起失败)——"
            "请在该件的运行环境装 cryptography 或确保 openssl 在 PATH"
        ) from exc
    if proc.returncode != 0 or len(proc.stdout) != len(ciphertext):
        raise DecryptError("openssl CLI AES 解密失败(返回码非 0)")
    return proc.stdout


def _aes_plain_truncate(plain: bytes, aes_size: int) -> bytes:
    """AES 段明文按 aes_size 截断(nopad 语义)。

    实测依据:5 样本 filesize-xor_size 恒 = 15+1024+16,即 aes=1024 时
    密文区恰 1024 字节、无整块 PKCS7 追加(否则差值应为 15+1040+16)——
    aes_size 语义 = 明文头长度,密文区按 16 对齐取 ceil,解后截断到
    aes_size。不做 PKCS7 剥离:图像头尾字节偶然成合法填充会被误剥。
    """
    return plain[:aes_size]


def decrypt_dat(payload: bytes, keys: dict[str, str]) -> bytes:
    """聊天图片 .dat:V2/V1 三段容器,legacy 整文件单字节 XOR。

    ``keys`` = ``load_keys_manual()`` 载入的钥匙(V2 的 aes_key 必供,
    xor_key 可缺省自推;真实件走件内自理——见模块头注边界)。
    """
    magic = payload[:6]
    if magic in (_DAT_V2_MAGIC, _DAT_V1_MAGIC):
        return _decrypt_dat_container(payload, keys, v2=magic == _DAT_V2_MAGIC)
    return _decrypt_dat_legacy(payload, keys)


def _decrypt_dat_container(payload: bytes, keys: dict[str, str], *, v2: bool) -> bytes:
    """V2/V1 共用三段解:AES 段 + 中段透传 + 尾段单字节 XOR。"""
    if len(payload) < _DAT_HEADER_LEN + 2 * _AES_BLOCK:
        raise DecryptError(f"文件过短({len(payload)} 字节),不足以承载 V4 容器头+密段")
    aes_size, xor_size = struct.unpack_from("<II", payload, 6)
    if payload[14] != _DAT_HEADER_VER:
        raise DecryptError(f"V4 容器版本字节非 0x01(得 {payload[14]:#04x})——形态未知,拒解")
    aes_ct_len = (aes_size + _AES_BLOCK - 1) // _AES_BLOCK * _AES_BLOCK
    middle_start = _DAT_HEADER_LEN + aes_ct_len
    tail_start = len(payload) - xor_size
    if aes_size <= 0 or xor_size <= 0 or middle_start > tail_start:
        raise DecryptError(
            f"V4 容器头部字段不自洽(aes_size={aes_size}, xor_size={xor_size}, "
            f"总长={len(payload)})——拒绝按错误布局拼产物"
        )
    if v2:
        aes_key = _parse_aes_key(keys.get("aes_key"))
        if aes_key is None:
            raise DecryptError(
                "V2 容器需每用户 AES-128 钥(16 字节 ASCII 或 32 位 hex):"
                "手动联调用 WX_MEDIA_AES_KEY/--key-file 供给;真实件走件内自理"
                "(钥提取属进程内存取证,本件不含提取器;见 docs/wechat-mediadecrypt.md §2)"
            )
    else:
        aes_key = _V1_FIXED_AES_KEY
    aes_plain = _aes_plain_truncate(_aes_ecb_decrypt(payload[_DAT_HEADER_LEN:middle_start], aes_key), aes_size)
    middle = payload[middle_start:tail_start]
    xor_key = _parse_xor_key(keys.get("xor_key"))
    if xor_key is None:
        xor_key = derive_xor_key(payload[tail_start:])
    if xor_key is None:
        raise DecryptError(
            "尾段单字节 XOR 钥自推失败(标志计票无峰)——请以 WX_MEDIA_XOR_KEY "
            "显式供给(本机实测钥形态如 0xE9)"
        )
    tail_plain = bytes(byte ^ xor_key for byte in payload[tail_start:])
    return aes_plain + middle + tail_plain


def _decrypt_dat_legacy(payload: bytes, keys: dict[str, str]) -> bytes:
    """legacy(3.x):无头整文件单字节 XOR;钥自推=计票,回落=首字节锚。"""
    if not payload:
        raise DecryptError("空文件,无从解起")
    xor_key = _parse_xor_key(keys.get("xor_key"))
    if xor_key is None:
        xor_key = derive_xor_key(payload)
    if xor_key is None:
        for anchor in _LEGACY_HEAD_ANCHORS:
            candidate = payload[0] ^ anchor
            head = bytes(byte ^ candidate for byte in payload[:8])
            if head[:3] == b"\xff\xd8\xff" or head[:4] == b"\x89PNG" or head[:4] in (b"GIF8", b"RIFF"):
                xor_key = candidate
                break
    if xor_key is None:
        raise DecryptError("legacy 整文件 XOR 钥自推失败——请以 WX_MEDIA_XOR_KEY 显式供给")
    return bytes(byte ^ xor_key for byte in payload)


# ═══════════════════════════════════════════════════════════════════
# 算法位 B:朋友圈 CDN 媒体流(Isaac64 keystream XOR)
# —— Isaac64 = Bob Jenkins 1996 Public Domain,照参考 C(burtleburtle.net
#    /bob/c/isaac64.c)机械移植;seeding/消费序约定见模块头注
# ═══════════════════════════════════════════════════════════════════


class _Isaac64:
    """ISAAC64 随机流(参考 C 机械移植;KAT 见 tests/scripts/)。

    消费序严格照参考 ``rand()`` 宏:每轮 256 个 qword 自 randrsl[255]
    降序取用,取尽即 isaac64() 再生;种子 = 循环填充 2048 字节种子缓冲。
    """

    _SIZ = 256
    _M64 = (1 << 64) - 1
    _GOLDEN = 0x9E3779B97F4A7C13
    _IND_MASK = 0x7F8  # (RANDSIZ-1)<<3:按字节偏移索引 mm

    def __init__(self, seed: bytes) -> None:
        if not seed:
            seed = b"\x00"
        buf = (seed * (2048 // len(seed) + 1))[:2048]
        rsl = [int.from_bytes(buf[i * 8:i * 8 + 8], "little") for i in range(self._SIZ)]
        self._mm = [0] * self._SIZ
        self._randrsl = [0] * self._SIZ
        self._aa = self._bb = self._cc = 0
        self._randcnt = 0
        self._randinit(rsl)

    # —— 参考 ind(mm,x):按 x 低 9 位对齐的字节偏移读 mm ——
    def _ind(self, value: int) -> int:
        return self._mm[(value & self._IND_MASK) >> 3]

    def _rngstep(self, mix: int, a: int, b: int, m: int, m2: int, ri: int) -> tuple[int, int, int, int, int]:
        mm, rsl = self._mm, self._randrsl
        x = mm[m]
        a = (mix + mm[m2]) & self._M64
        m2 += 1
        y = (self._ind(x) + a + b) & self._M64
        mm[m] = y
        m += 1
        b = (self._ind(y >> 8) + x) & self._M64  # 参考:ind(mm, y>>RANDSIZL)
        rsl[ri] = b
        return a, b, m, m2, ri + 1

    def _isaac64(self) -> None:
        a, b = self._aa, (self._bb + self._cc + 1) & self._M64
        self._cc = (self._cc + 1) & self._M64
        m = m2 = ri = 0
        m2 = self._SIZ // 2
        while m < self._SIZ // 2:
            a, b, m, m2, ri = self._rngstep(~(a ^ ((a << 21) & self._M64)) & self._M64, a, b, m, m2, ri)
            a, b, m, m2, ri = self._rngstep(a ^ (a >> 5), a, b, m, m2, ri)
            a, b, m, m2, ri = self._rngstep((a ^ ((a << 12) & self._M64)) & self._M64, a, b, m, m2, ri)
            a, b, m, m2, ri = self._rngstep(a ^ (a >> 33), a, b, m, m2, ri)
        m2 = 0
        while m2 < self._SIZ // 2:
            a, b, m, m2, ri = self._rngstep(~(a ^ ((a << 21) & self._M64)) & self._M64, a, b, m, m2, ri)
            a, b, m, m2, ri = self._rngstep(a ^ (a >> 5), a, b, m, m2, ri)
            a, b, m, m2, ri = self._rngstep((a ^ ((a << 12) & self._M64)) & self._M64, a, b, m, m2, ri)
            a, b, m, m2, ri = self._rngstep(a ^ (a >> 33), a, b, m, m2, ri)
        self._bb, self._aa = b, a

    def _mix(self, state: list[int]) -> None:
        a, b, c, d, e, f, g, h = state
        m = self._M64
        a = (a - e) & m; f ^= h >> 9; h = (h + a) & m
        b = (b - f) & m; g ^= (a << 9) & m; a = (a + b) & m
        c = (c - g) & m; h ^= b >> 23; b = (b + c) & m
        d = (d - h) & m; a ^= (c << 15) & m; c = (c + d) & m
        e = (e - a) & m; b ^= d >> 14; d = (d + e) & m
        f = (f - b) & m; c ^= (e << 20) & m; e = (e + f) & m
        g = (g - c) & m; d ^= f >> 17; f = (f + g) & m
        h = (h - d) & m; e ^= (g << 14) & m; g = (g + h) & m
        state[:] = [a, b, c, d, e, f, g, h]

    def _randinit(self, rsl: list[int]) -> None:
        mm = self._mm
        state = [self._GOLDEN] * 8
        for _ in range(4):
            self._mix(state)
        for i in range(0, self._SIZ, 8):
            for j in range(8):
                state[j] = (state[j] + rsl[i + j]) & self._M64
            self._mix(state)
            mm[i:i + 8] = state[:]
        for i in range(0, self._SIZ, 8):
            for j in range(8):
                state[j] = (state[j] + mm[i + j]) & self._M64
            self._mix(state)
            mm[i:i + 8] = state[:]
        self._isaac64()
        self._randcnt = self._SIZ

    def next_qword(self) -> int:
        """按参考 rand() 宏消费序取下一个 64 位随机值。"""
        if self._randcnt == 0:
            self._isaac64()
            self._randcnt = self._SIZ - 1
            return self._randrsl[self._randcnt]
        self._randcnt -= 1
        return self._randrsl[self._randcnt]


def _isaac64_keystream(key: str, length: int) -> bytes:
    """数字串钥 → Isaac64 keystream(qword 小端展开,截取 length 字节)。"""
    gen = _Isaac64(key.encode("utf-8"))
    chunks: list[bytes] = []
    remaining = length
    while remaining > 0:
        block = gen.next_qword().to_bytes(8, "little")
        chunks.append(block)
        remaining -= 8
    return b"".join(chunks)[:length]


def decrypt_stream(payload: bytes, key: str) -> bytes:
    """朋友圈 CDN 媒体流:Isaac64 keystream XOR(自逆,加解密同式)。

    ``key`` = 桥经请求 JSON 单次透传的库内数字串(协议 §4;零落盘零
    日志,只在内存消费);seeding/消费序约定见模块头注(未经真流实测)。
    """
    if not key:
        raise DecryptError("decrypt_stream 缺 key(协议 §4:请求必含数字串钥)")
    keystream = _isaac64_keystream(key, len(payload))
    return bytes(p ^ k for p, k in zip(payload, keystream))


# ⬆⬆ 算法位(已按实测填入;实测边界与生态参考见各 docstring)⬆⬆


def guess_ext(head: bytes) -> str | None:
    """产物首字节猜格式(协议 §5:result 必含 ext;§7 魔数表同源)。"""
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    if head[4:8] == b"ftyp":
        return "mp4"
    return None


def run_action(request: dict, keys: dict[str, str]) -> int:
    """两动作共用协议壳:读密文 → 算法位 → 写产物 → 应答 result。"""
    action = request.get("action")
    if action == "decrypt_dat":
        in_field, in_path = "dat_path", str(request.get("dat_path") or "")
        extra: list[str] = []
    else:  # decrypt_stream(分支封闭:main 已校验动作合法)
        in_field, in_path = "in_path", str(request.get("in_path") or "")
        extra = ["key 经请求透传,仅内存消费(协议 §4)"]
    out_path = str(request.get("out_path") or "")
    if not in_path or not out_path:
        return fail(f"{in_field}/out_path 缺失(协议 §4:两动作均必含)")

    emit({"type": "progress", "message": f"读取密文: {Path(in_path).name}", "level": 0})
    try:
        payload = Path(in_path).read_bytes()
    except OSError as exc:
        return fail(f"读取密文失败: {exc}")

    emit({"type": "progress", "message": "进入算法位", "level": 0})
    try:
        if action == "decrypt_dat":
            plaintext = decrypt_dat(payload, keys)
        else:
            plaintext = decrypt_stream(payload, str(request.get("key") or ""))
    except DecryptError as exc:
        # 算法位人话失败(钥缺失/形态不自洽/后端不可用)→ 协议 §5 失败形态。
        return fail(
            str(exc),
            logs=[
                f"action={action}",
                f"bytes={len(payload)}",
                f"keys_intake={bool(keys)}(仅手动联调形态;真实件钥匙=件内自理,见件头注)",
                *extra,
            ],
        )

    ext = guess_ext(plaintext[:16])
    if ext is None:
        return fail(
            "产物首字节不属于已知格式(算法位填入后按你的产物格式应答 ext)",
            logs=[f"head_hex={plaintext[:16].hex()}"],
        )
    emit({"type": "progress", "message": f"写明文产物: {Path(out_path).name}", "level": 0})
    try:
        Path(out_path).write_bytes(plaintext)
    except OSError as exc:
        return fail(f"写明文产物失败: {exc}")

    emit(
        {
            "type": "result",
            "success": True,
            "ext": ext,
            "is_wxgf": False,
            "width": None,
            "height": None,
            "logs": [f"action={action}", f"bytes={len(payload)}"],
        }
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="微信媒体解密件(协议壳+实测算法;仅手动联调形态收 --key-file)"
    )
    parser.add_argument(
        "--key-file",
        help="钥匙文件(JSON:{xor_key,aes_key})——仅手动联调形态有效,"
        "桥 spawn 链 argv 恒空收不到(见件头注)",
    )
    args = parser.parse_args()

    keys = load_keys_manual(args.key_file)

    line = sys.stdin.readline()  # 桥写一行后关 stdin,不会有更多输入(协议 §3)
    try:
        request = json.loads(line)
    except ValueError:
        return fail("请求不是合法 JSON(协议 §4:stdin 单行 JSON)")
    if not isinstance(request, dict):
        return fail("请求须为 JSON 对象")

    if request.get("action") not in _ACTIONS:
        return fail(
            f"未知动作: {request.get('action')!r}(v1 合法动作 = {' / '.join(_ACTIONS)})"
        )
    return run_action(request, keys)


if __name__ == "__main__":
    sys.exit(main())
