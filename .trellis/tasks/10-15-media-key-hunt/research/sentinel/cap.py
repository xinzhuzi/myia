"""媒体钥哨兵回调(LLDB python)。

用法(配合 run.cmd):断 CCCrypt/CCCryptorCreate 两入口,arm64 寄存器口径
(x0=op,x1=alg,x2=options,x3=key 指针,x4=keyLength)。回调过滤
AES-128-ECB 解密形态 → 读 16 字节钥 → 对 /tmp/wximg 真样本首块跑
openssl oracle(jpg/png/webp/gif 魔数)→ 验真才落 KEY 文件并停机
(外层随即 detach);不中则静默自动续跑,微信零感知。

红线:钥只写 /tmp/wx_media_key_sentinel/KEY(hex 文本,600);零日志外泄、
零微信内存写、命中即脱附。
"""

import lldb
import pathlib
import subprocess

OUT_DIR = pathlib.Path("/tmp/wx_media_key_sentinel")
SAMPLES = sorted(pathlib.Path("/tmp/wximg").glob("*.dat"))
_MAGICS = (b"\xff\xd8\xff", b"\x89PNG", b"GIF8", b"RIFF")


def _oracle(key16: bytes) -> bool:
    """真样本首块 AES-ECB oracle:解出任一图像魔数即真。"""
    for sample in SAMPLES[:5]:
        ct = sample.read_bytes()[15:31]
        proc = subprocess.run(
            ["openssl", "enc", "-aes-128-ecb", "-d", "-K", key16.hex(), "-nopad"],
            input=ct,
            capture_output=True,
            timeout=10,
        )
        head = proc.stdout[:4]
        if any(head.startswith(m) for m in _MAGICS):
            return True
    return False


def _want(frame) -> bool:
    """arm64 过滤:kCCDecrypt(1) + kCCAlgorithmAES(0) + keyLength 16 + ECB 位。"""
    for name in ("x0", "x1", "x2", "x4"):
        if frame.FindRegister(name).IsValid() is False:
            return False
    if frame.FindRegister("x0").GetValueAsUnsigned() != 1:
        return False
    if frame.FindRegister("x1").GetValueAsUnsigned() != 0:
        return False
    if frame.FindRegister("x4").GetValueAsUnsigned() != 16:
        return False
    if frame.FindRegister("x2").GetValueAsUnsigned() & 0x2 == 0:
        return False
    return True


def on_hit(frame, bp_loc, extra):
    """断点回调:命中 → 过滤 → 读钥 → oracle → 验真落盘停机,否则续跑。

    lldb `-F` 断点命令返回语义 = 「是否停机」(实测 r0 轮实证:返回真值
    即停机触发 detach):False = 自动续跑零扰动;True = 停机(仅验真命中,
    外层随即 detach)。首版返回值写反,r0 轮首个被滤命中即误停——本版纠正。
    """
    try:
        if not _want(frame):
            return False  # 非 AES-128-ECB 解密形态:自动续跑
        key_ptr = frame.FindRegister("x3").GetValueAsUnsigned()
        if key_ptr == 0:
            return False
        err = lldb.SBError()
        key = frame.GetThread().GetProcess().ReadMemory(key_ptr, 16, err)
        if not err.Success() or len(key) != 16:
            return False
        if _oracle(key):
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            key_file = OUT_DIR / "KEY"
            key_file.write_text(key.hex() + "\n")
            key_file.chmod(0o600)
            print("MEDIA-KEY-FOUND", key.hex(), flush=True)
            return True  # 验真命中:停机 → 外层 detach
    except Exception as exc:  # noqa: BLE001 - 哨兵绝不因自体异常扰宿主
        print("cap error:", exc, flush=True)
    return False


def __lldb_init_module(debugger, _internal_dict):
    print("media-key sentinel cap loaded; samples:", len(SAMPLES), flush=True)
