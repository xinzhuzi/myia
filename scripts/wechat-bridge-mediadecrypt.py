#!/usr/bin/env python3
"""微信媒体解密件——生产起步骨架(协议壳 + 钥匙 intake 钩;算法位留空)。

本件 = docs/wechat-mediadecrypt.md v1 协议的生产起步骨架:照
plugins/wechat-bridge/examples/mediadecrypt_ref.py 的协议形状
(stdin 单行 JSON → stdout NDJSON:progress 0..N + result 恰一次 → 退出码
按协议 §6 矩阵;失败姿势同 ref:result ``success:false`` + 退出码 0),
``decrypt_dat`` / ``decrypt_stream`` 两动作的**算法位显式留空**——命中即按
§5 失败形态回人话「算法位留空:按 docs/wechat-mediadecrypt.md §9 填入你
的实现」。真实算法(V4 XOR/AES 分段、Isaac64 keystream)用户自备,照该
文档 §9 填进下方两个留空函数;协议形状参考 examples/mediadecrypt_ref.py。

落位纪律(勿动):

- 本件落位仓根 ``scripts/``——**不随产品包分发**(app resources 白名单不含
  仓根 ``scripts/``,亦无 CI 复制钩子)。
- **本件永不放入 ``plugins/wechat-bridge/`` 目录**——该目录是 tauri 整目录
  复制面(desktop/src-tauri/tauri.conf.json:94 resources 映射
  ``"../../plugins/wechat-bridge": "components/wechat-bridge"``),放进去
  即随产品包分发。

钥匙 intake 钩(仅手动联调形态有效;边界如实):

- 钩 = env ``WX_MEDIA_XOR_KEY`` / ``WX_MEDIA_AES_KEY`` 或 ``--key-file``
  (JSON,字段 ``xor_key``/``aes_key``)——钥匙**仅内存过手、零落盘、零
  日志**:永不写盘、永不进 result/logs/stderr。
- 但 env/--key-file **仅手动联调形态有效**:桥 spawn 链 argv 恒只传件
  路径零参数(media.py:254-260 ``subprocess.Popen([str(exe)])``,无
  ``env=`` 显式传参),``--key-file`` 在桥链上永远收不到;世事.app 为
  macOS GUI app(launchd 起),用户 shell export 的 env 不进桥进程。
  钥匙进真实件的现实通道 = **件内自理**:件内写死路径/自带钥匙文件约定
  (docs/wechat-mediadecrypt.md §2/§4「钥匙=件内自理」)。

手动联调(不经桥):

.. code-block:: bash

    chmod +x scripts/wechat-bridge-mediadecrypt.py
    echo '{"action":"decrypt_dat","dat_path":"/abs/a.dat","out_path":"/tmp/out"}' \\
        | ./scripts/wechat-bridge-mediadecrypt.py
    # 预期:stdout NDJSON(progress + result success:false,error=算法位留空…)
    # 退出码 0(协议 §6:result success:false 任意退出码均判失败)

接进桥(接线闭环验收):

    wechat-bridge localdb media-decrypt set /abs/path/scripts/wechat-bridge-mediadecrypt.py
    wechat-bridge localdb media decrypt /abs/a.dat --json
    # 预期:exit 22 decrypt_failed,error 透传「算法位留空:按
    # docs/wechat-mediadecrypt.md §9 填入你的实现」
"""

from __future__ import annotations

import argparse
import json
import os
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
# ⬇⬇ 算法位(留空)——按 docs/wechat-mediadecrypt.md §9 填入你的实现 ⬇⬇
# ═══════════════════════════════════════════════════════════════════


def decrypt_dat(payload: bytes, keys: dict[str, str]) -> bytes:
    """算法位留空:聊天图片 .dat(V4 分段 XOR/AES)。

    填入你的实现后:
    - ``keys`` = ``load_keys_manual()`` 在手动联调形态载入的钥匙(真实
      件走件内自理——见模块头注边界);
    - 返回解密后的明文字节;main() 负责写 out_path / 猜 ext / 应答 result。
    """
    raise NotImplementedError("decrypt_dat 算法位留空")


def decrypt_stream(payload: bytes, key: str) -> bytes:
    """算法位留空:朋友圈 CDN 媒体流(Isaac64 keystream XOR)。

    ``key`` = 桥经请求 JSON 单次透传的库内数字串(协议 §4;零落盘零
    日志,只在内存消费);返回解密后的明文字节。
    """
    raise NotImplementedError("decrypt_stream 算法位留空")


# ⬆⬆ 算法位(留空)——按 docs/wechat-mediadecrypt.md §9 填入你的实现 ⬆⬆


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
    except NotImplementedError:
        # 算法位留空 = 骨架终态:人话指路(诊断只报钥匙「有无」布尔,零钥值)。
        return fail(
            "算法位留空:按 docs/wechat-mediadecrypt.md §9 填入你的实现",
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
        description="微信媒体解密件骨架(协议壳;算法位留空;仅手动联调形态收 --key-file)"
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
