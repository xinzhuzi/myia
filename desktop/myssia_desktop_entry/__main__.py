"""``python -m myssia_desktop_entry`` 命令分发(协议面 = ``entry.py`` 原样)。

argv 形态与冻结 sidecar 时代完全一致(壳零感知):

- ``serve``:行分隔 JSON-RPC 服务(Tauri 壳常驻后端;stdin EOF = 干净退出 0);
- 其余:直通 myssia CLI(退出码 0/1/2/3 契约由 CLI 层原样保证,v02 spike 兼容)。
"""

from __future__ import annotations

import sys
from collections.abc import Sequence

from myssia_desktop_entry import load_entry_module


def main(argv: Sequence[str] | None = None) -> int:
    """分发入口:镜像 ``entry.py`` ``__main__`` 块语义,零改动。

    Args:
        argv: 参数列表;None 表示 ``sys.argv[1:]``(与 myssia.cli.main 同口径)。

    Returns:
        进程退出码(serve:EOF=0/致命=1;直通:CLI 契约 0/1/2/3)。
    """
    args = list(sys.argv[1:] if argv is None else argv)
    entry = load_entry_module()
    if args and args[0] == "serve":
        return entry.serve()
    return entry.cli_main(args)


if __name__ == "__main__":
    sys.exit(main())
