"""wechat-bridge 组件单测的共享装配(design §8:AX/localdb 层全 mock,CI
无微信全绿;真实客户端测试一律 ``MYIA_WECHAT_E2E=1`` 门控)。

**为什么不是 conftest.py**:仓库测试通用裸 ``from conftest import …``
(tests/conftest.py 注记),多一个子目录 conftest.py 会在 prepend 导入模式下
按 basename 抢注 ``sys.modules["conftest"]``,把 tests/conftest.py 的共享
夹具整个顶掉(2026-10-11 实测:全量跑踩进 4 个假失败)。故本目录用**普通
模块**承载共享件——test 文件与本模块同目录,pytest prepend 导入模式天然
把目录放进 sys.path,``import bridge_testkit`` 直取,零遮蔽。

组件不是 uv workspace 成员(MYIA 只做子进程调用,不 vendor 也不依赖它
——design §1),故此处以 sys.path 直插组件源码根导入;零第三方依赖,
纯 stdlib + pytest 即可全绿。
"""

from __future__ import annotations

import io
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))


@dataclass(frozen=True)
class CheckMocks:
    """一组检查器 mock(全部可关,逐一对应 system_checks 注入点)。"""

    process: bool = True
    version: str | None = "4.1.15"
    ax_trusted: bool | None = True
    window: bool | None = False
    accounts: int | None = 1
    key: bool = False


def apply_mocks(mocks: CheckMocks, monkeypatch: pytest.MonkeyPatch) -> None:
    """把一组检查器 mock 打到 system_checks 注入点(probe/前置门共消费)。"""
    import wechat_bridge.system_checks as sc

    monkeypatch.setattr(sc, "wechat_process_running", lambda: mocks.process)
    monkeypatch.setattr(sc, "wechat_version", lambda: mocks.version)
    monkeypatch.setattr(sc, "ax_permission_trusted", lambda: mocks.ax_trusted)
    monkeypatch.setattr(sc, "wechat_main_window_open", lambda: mocks.window)
    monkeypatch.setattr(sc, "localdb_storage_accounts", lambda: mocks.accounts)
    monkeypatch.setattr(sc, "localdb_key_available", lambda: mocks.key)


def tray_mocks(monkeypatch: pytest.MonkeyPatch, mocks: CheckMocks | None = None) -> CheckMocks:
    """托盘态 mock(2026-10-11 实况形状:进程在/AX 在/窗口关/库在/密钥缺)。"""
    resolved = mocks or CheckMocks()
    apply_mocks(resolved, monkeypatch)
    return resolved


def green_mocks(monkeypatch: pytest.MonkeyPatch) -> CheckMocks:
    """全绿态 mock(窗口开 + 密钥可得 → probe 应 ok)。"""
    resolved = CheckMocks(window=True, key=True)
    apply_mocks(resolved, monkeypatch)
    return resolved


def run_cli(
    argv: list[str],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    stdin_text: str | None = None,
) -> tuple[int, dict]:
    """进程内跑 CLI:隔离 MYIA_HOME(配置/频控落 tmp),回 (exit, JSON)。"""
    import wechat_bridge.cli as cli

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    if stdin_text is not None:
        monkeypatch.setattr(sys, "stdin", io.StringIO(stdin_text))
    stdout = io.StringIO()
    real_stdout = sys.stdout
    monkeypatch.setattr(sys, "stdout", stdout)
    try:
        exit_code = cli.main(argv)
    finally:
        monkeypatch.setattr(sys, "stdout", real_stdout)
    payload = json.loads(stdout.getvalue())
    return exit_code, payload
