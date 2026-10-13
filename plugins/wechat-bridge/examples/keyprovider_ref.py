#!/usr/bin/env python3
"""外部取钥器参考实现(B4;task 10-13-wechat-keyprovider)。

给第三方当样例的**最小合规取钥器**:读一个钥匙 JSON 文件 + 协议包装,
零扫描、零内存读取、零微信进程接触——钥匙从哪来(钥匙串/你自己的取钥
机制/手工维护)是你的事,本件只示范「怎么按协议把钥匙交给桥」。

协议全文 = 仓内 docs/wechat-keyprovider.md(只认协议,无须读桥源码):

- 桥 spawn 本件 → stdin 写**一行** JSON 请求后关 stdin;
- 本件 stdout 按行输出 NDJSON(``progress`` 0..N 次 + ``result`` 恰一次,
  写行即 flush);调试信息一律走 stderr(失败时桥取尾部 500 字符);
- ``result`` 成功形态携带 ``keys``:``{salt_hex: key_hex}``(逐库)或
  ``{"*": key_hex}``(全域同钥通配);盐 = 库文件前 16 字节的 hex;
- 发完 result 以退出码 0 退出;全程 ≤ 120 秒(超时桥 kill);
- 无状态:不写桥的 keys.json、不依赖桥内文件布局、可并发重入。

钥匙文件形态(与桥的密钥缓存 keys.json 同形,可复用):

.. code-block:: json

    {
      "message/message_0.db": "<64-hex SQLCipher 密钥>",
      "session/session.db": "<64-hex>",
      "*": "<64-hex>(可选:未逐条列出的库全部用这把)"
    }

键 = 相对 ``db_path`` 的库路径;本件枚举 ``db_path`` 下各 ``.db`` 读前
16 字节得盐,再按键取钥应答(库不在钥匙文件内 = 该库无钥,如实不给)。

用法(手动联调,不经桥):

.. code-block:: bash

    chmod +x keyprovider_ref.py
    echo '{"action":"get_db_key","db_path":"/abs/db_storage","account_id":"wxid_x"}' \\
        | ./keyprovider_ref.py /path/to/keys.json

接进桥::

    wechat-bridge localdb key-provider set /abs/path/keyprovider_ref.py
    # 钥匙文件路径经 argv[1] 或 env KEYPROVIDER_REF_KEYS 传入

本件故意不追求健壮(够读懂即可):真取钥器请在此基础上换成你的钥匙来源。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

#: 钥匙文件缺省落点(桥数据根的密钥缓存同位;argv[1]/env 可覆写)。
DEFAULT_KEY_FILE = (
    Path.home() / "Library" / "Application Support" / "MYIA" / "wechat-localdb" / "keys.json"
)

SALT_BYTES = 16  # SQLCipher 4:salt = 库文件前 16 字节(协议 §5)


def emit(obj: dict) -> None:
    """stdout 按行输出协议 NDJSON(写行即 flush——桥流式可读,协议 §4)。"""
    sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def fail(message: str, logs: list[str] | None = None) -> int:
    """失败形态 result + 退出码 0(协议 §6 推荐姿势:catch 后退 0)。"""
    emit({"type": "result", "success": False, "error": message, "logs": logs or []})
    return 0


def load_keys(key_file: Path) -> dict[str, str]:
    """读钥匙文件({相对路径: 64hex};坏文件 = 人话失败,不猜。"""
    try:
        raw = json.loads(key_file.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RuntimeError(f"读取钥匙文件失败: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError(f"钥匙文件不是合法 JSON: {exc}") from exc
    if not isinstance(raw, dict) or not raw:
        raise RuntimeError(f"钥匙文件须为非空映射({{相对路径: 64hex}}): {key_file}")
    return {str(k): str(v).strip().lower() for k, v in raw.items()}


def salt_of(db_file: Path) -> str | None:
    """读库文件前 16 字节的 hex(SQLCipher salt;读不动 = None 跳过)。"""
    try:
        with db_file.open("rb") as fh:
            head = fh.read(SALT_BYTES)
    except OSError:
        return None
    return head.hex() if len(head) == SALT_BYTES else None


def main() -> int:
    line = sys.stdin.readline()  # 桥写一行后关 stdin,不会有更多输入(协议 §2)
    try:
        request = json.loads(line)
    except ValueError:
        return fail("请求不是合法 JSON(协议 §3:stdin 单行 JSON)")
    if not isinstance(request, dict):
        return fail("请求须为 JSON 对象")
    if request.get("action") != "get_db_key":
        return fail(f"未知动作: {request.get('action')!r}(v1 唯一动作 = get_db_key)")

    key_file = (
        Path(sys.argv[1]).expanduser()
        if len(sys.argv) > 1
        else Path(os.environ.get("KEYPROVIDER_REF_KEYS") or DEFAULT_KEY_FILE).expanduser()
    )
    emit({"type": "progress", "message": f"读取钥匙文件: {key_file}", "level": 0})
    try:
        keys = load_keys(key_file)
    except RuntimeError as exc:
        return fail(str(exc), logs=[f"key_file={key_file}"])

    db_path = Path(str(request.get("db_path") or ""))
    wildcard = keys.get("*", "")
    per_db = {k: v for k, v in keys.items() if k != "*"}
    answer: dict[str, str] = {}
    scanned = 0
    for db_file in sorted(db_path.rglob("*.db")):
        salt = salt_of(db_file)
        if salt is None:
            continue
        scanned += 1
        rel = db_file.relative_to(db_path).as_posix()
        key_hex = per_db.get(rel) or wildcard  # 逐条优先,通配兜底
        if key_hex:
            answer[salt] = key_hex
    emit(
        {
            "type": "progress",
            "message": f"枚举 {scanned} 个库,组出 {len(answer)} 把钥匙",
            "level": 0,
        }
    )
    if not answer:
        return fail(
            f"钥匙文件未能覆盖任何库(枚举 {scanned} 个;钥匙文件 {key_file})",
            logs=[f"key_file={key_file}", f"per_db_keys={len(per_db)}", f"wildcard={'yes' if wildcard else 'no'}"],
        )
    emit(
        {
            "type": "result",
            "success": True,
            "keys": answer,
            "account_id": str(request.get("account_id") or ""),
            "logs": [
                f"key_file={key_file}",
                f"dbs_scanned={scanned}",
                "参考实现:读钥匙文件 + 协议包装,零扫描零内存读取",
            ],
        }
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
