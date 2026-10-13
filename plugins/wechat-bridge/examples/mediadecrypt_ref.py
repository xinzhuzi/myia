#!/usr/bin/env python3
"""媒体解密件参考实现(task 10-14-wechat-media-sns R1;协议形状示范)。

⚠️ **非真实微信解密——toy 算法(字节反转),解不出真实微信媒体。**
⚠️ 真实算法(V4 分段 XOR/AES、Isaac64 keystream)用户自备;本件只示范
   「怎么按协议把桥给的请求接住、把产物写到 out_path、怎么应答 result」。
   生态教训(PyWxDump/chatlog 自删、wechat-dump-rs DMCA)= 解密算法件不进
   MYIA 仓库是硬约束(AC7 守卫:仓内零真实算法)。

协议全文 = 仓内 docs/wechat-mediadecrypt.md(只认协议,无须读桥源码):

- 桥 spawn 本件 → stdin 写**一行** JSON 请求后关 stdin;
- 本件 stdout 按行输出 NDJSON(``progress`` 0..N 次 + ``result`` 恰一次,
  写行即 flush);调试信息一律走 stderr(失败时桥取尾部 500 字符);
- 动作 ``decrypt_dat``(请求 {dat_path, out_path}):读 dat_path 全字节 →
  (真实件在此解 V4 分段;本件做字节反转)→ 明文写到 out_path;
  钥匙=件内自理(真实件在此消费你自备的 imageXorKey/imageAesKey——
  本 toy 无钥需求);
- 动作 ``decrypt_stream``(请求 {in_path, key, out_path}):读 in_path 全
  字节 → (真实件在此以 key 做 Isaac64 keystream XOR;本件仍字节反转,
  key 只回显进 logs 不参与计算)→ 明文写到 out_path;
- ``result`` 成功形态:{success, ext, is_wxgf, width?, height?, logs};
  ext 按产物首字节猜(jpg/png/gif;猜不出 = 失败如实用 error);
- 发完 result 以退出码 0 退出;全程 ≤ 120 秒(超时桥 kill);
- 无状态:不写桥的缓存、不依赖桥内文件布局、可并发重入。

用法(手动联调,不经桥):

.. code-block:: bash

    chmod +x mediadecrypt_ref.py
    echo '{"action":"decrypt_dat","dat_path":"/abs/a.dat","out_path":"/tmp/out"}' \\
        | ./mediadecrypt_ref.py

接进桥::

    wechat-bridge localdb media-decrypt set /abs/path/mediadecrypt_ref.py

本件故意不追求健壮(够读懂即可):真解密件请在此基础上换成你的算法与钥匙来源。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def emit(obj: dict) -> None:
    """stdout 按行输出协议 NDJSON(写行即 flush——桥流式可读,协议 §5)。"""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def fail(message: str, logs: list[str] | None = None) -> int:
    """失败形态 result + 退出码 0(协议 §6 推荐姿势:catch 后退 0)。"""
    emit({"type": "result", "success": False, "error": message, "logs": logs or []})
    return 0


def guess_ext(head: bytes) -> str | None:
    """产物首字节猜格式(toy 级;真实件自己知道产物是什么)。"""
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


def main() -> int:
    line = sys.stdin.readline()  # 桥写一行后关 stdin,不会有更多输入(协议 §3)
    try:
        request = json.loads(line)
    except ValueError:
        return fail("请求不是合法 JSON(协议 §4:stdin 单行 JSON)")
    if not isinstance(request, dict):
        return fail("请求须为 JSON 对象")

    action = request.get("action")
    if action == "decrypt_dat":
        in_path = str(request.get("dat_path") or "")
        out_path = str(request.get("out_path") or "")
        note = "dat_path"
    elif action == "decrypt_stream":
        in_path = str(request.get("in_path") or "")
        out_path = str(request.get("out_path") or "")
        note = "in_path(key 单次过手,不落盘不入日志)"
    else:
        return fail(
            f"未知动作: {action!r}(v1 合法动作 = decrypt_dat / decrypt_stream)"
        )
    if not in_path or not out_path:
        return fail(f"{note}/out_path 缺失(协议 §4:两动作均必含)")

    emit({"type": "progress", "message": f"读取密文: {Path(in_path).name}", "level": 0})
    try:
        payload = Path(in_path).read_bytes()
    except OSError as exc:
        return fail(f"读取密文失败: {exc}")

    # —— toy 算法:字节反转(⚠️ 非真实微信解密;真实件在此放你的算法)——
    plaintext = payload[::-1]
    head = plaintext[:16]
    ext = guess_ext(head)
    if ext is None:
        return fail(
            "toy 算法解出的产物首字节不属于已知格式(本参考件只处理可猜出"
            "格式的输入;真实件按你的产物格式应答 ext)",
            logs=["toy=bytes-reverse", f"head_hex={head.hex()}"],
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
            "is_wxgf": False,  # toy 不产实况格式;真实件按产物如实报
            "width": None,
            "height": None,
            "logs": [
                "参考实现:toy 字节反转,非真实微信解密(协议形状示范)",
                f"action={action}",
                f"bytes={len(payload)}",
            ],
        }
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
