"""golden AX 树快照回归(S1;10-14 r3 后立)。

夹具 = 真机 System Events 全量转储(tests/wechat-bridge/fixtures/
ax_tree_snapshot.json,采集脚本与采时事实见 meta)。本测试把**桥代码的
世界模型**钉在真机快照上:微信改版若挪走/改名承重元素,这里先红,
而不是等真机 dry-run 再踩一遍(r2 教训:mock 编码了错误世界模型全绿
而真机全红)。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "ax_tree_snapshot.json"


@pytest.fixture(scope="module")
def snapshot() -> dict:
    import json

    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class TestWorldModelAnchor:
    """axui 匹配的元素名必须存在于真机主窗快照(核心锚)。"""

    def test_axui_anchors_exist_in_main_window(self, snapshot: dict) -> None:
        named = set(snapshot["main_window"]["named"])
        assert "chat_input_field" in named, "AX 主链写入锚消失:微信改版?重审 axui 常量与 FINDINGS"
        assert "current_chat_name_label" in named, "标题直读锚消失"
        assert any(i.startswith("session_item_") for i in named), "会话列表行锚消失"
        assert "chat_message_list" in named, "消息列表锚消失(发送后回读依赖区)"

    def test_main_window_tree_has_substance(self, snapshot: dict) -> None:
        """树量级漂移守卫:命名元素 <15 或节点 <60 = 大改版,重审整套 AX 假设。"""
        main = snapshot["main_window"]
        assert len(main["named"]) >= 15
        assert main["node_count"] >= 60

    def test_search_anchors_live_only_in_main_window(self, snapshot: dict) -> None:
        """chat_input_field/session_item_ 不在浮窗 → axui 主窗(最大面积)BFS 的正当性。"""
        float_named = set(snapshot["search_float"]["named"])
        assert "chat_input_field" not in float_named
        assert not any(i.startswith("session_item_") for i in float_named)

    def test_search_float_has_named_rows(self, snapshot: dict) -> None:
        """浮窗结果行有命名 id(search_item_* 族,含功能分类区)——
        推翻旧档『搜索面板全空 id』;空 id virtual_cell 属聊天记录区。"""
        float_named = snapshot["search_float"]["named"]
        assert any(i.startswith("search_item_") for i in float_named)
        assert "search_list" in float_named

    def test_meta_records_capture_conditions(self, snapshot: dict) -> None:
        """采集前提留在档:主窗须打开(托盘态 System Events 窗数 0)。"""
        meta = snapshot["meta"]
        assert meta["wechat_version"]
        assert meta["capture"]
        assert any("托盘" in f for f in meta["facts"])
