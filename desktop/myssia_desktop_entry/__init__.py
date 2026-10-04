"""桌面 sidecar 入口包(``python -m myssia_desktop_entry``)。

10-05-desktop-managed-py-env D1/D3:桌面端从 PyInstaller 冻结 sidecar 切换为
自管 Python 环境——壳 spawn ``<数据根>/python/bin/python3 -m myssia_desktop_entry``
(Windows 为 ``python/python.exe``),``PYTHONPATH`` 指向随包 Resources/myssia-src
(本包、``entry.py`` 与 :mod:`myssia` 核心包同树)。

协议面**零新增零改动**:本包只做装载与分发,真实实现 = 同父目录的
``entry.py``(直通/serve 双模式、方法集、事件面、退出码契约全部照旧;
与 tests/desktop/test_desktop_sidecar_protocol.py 的 importlib 直载同一手法,
零拷贝防两处漂移)。

布局约定(资源树与仓库开发树同形,本包相对定位在两种布局下恒成立):

- 资源树(Resources/myssia-src/):``myssia_desktop_entry/`` + ``entry.py`` + ``myssia/``
- 开发树(desktop/):``myssia_desktop_entry/`` + ``entry.py``(``myssia`` 走 src/ 注入)
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

#: 协议实现文件:本包父目录下的 ``entry.py``(资源树 = Resources/myssia-src/entry.py,
#  开发树 = desktop/entry.py;tauri.conf.json resources 映射保证两树同形)。
ENTRY_PY = Path(__file__).resolve().parent.parent / "entry.py"

#: 直载模块名:挂在本包名下(不污染顶层命名空间,也不与测试侧 ``desktop_entry``
#: 直载名冲突);每次调用装载为独立模块对象,importlib 缓存零依赖。
_MODULE_NAME = __name__ + "._entry"


def load_entry_module() -> ModuleType:
    """importlib 直载 ``entry.py`` 并执行其顶层(只定义符号,零副作用)。

    Raises:
        FileNotFoundError: 布局不符(缺 ``entry.py``)——资源映射断裂的早期信号,
            而不是让壳在 spawn 后收到裸 ImportError。
    """
    if not ENTRY_PY.is_file():
        raise FileNotFoundError(f"未找到 sidecar 协议实现: {ENTRY_PY}")
    spec = importlib.util.spec_from_file_location(_MODULE_NAME, ENTRY_PY)
    if spec is None or spec.loader is None:  # pragma: no cover — 理论防御路径
        raise ImportError(f"无法构造 entry.py 装载器: {ENTRY_PY}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


__all__ = ["ENTRY_PY", "load_entry_module"]
