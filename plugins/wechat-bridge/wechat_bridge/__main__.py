"""``python -m wechat_bridge`` 入口(装机形态:桥以目录树整份落在
``~/.myia/plugins/wechat-bridge/``,宿主 python 直跑本模块;§6 调用形态 =
一次性子进程)。"""

from __future__ import annotations

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
