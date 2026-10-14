"""微信渠道模块(10-14-wechat-module;超越 TG 的收拢形态,见任务档)。

导入序保证:先完整初始化 :mod:`myssia.push`(其 ``__init__`` 末段会导入
``push_local``),否则 ``sidecar → push_local → push/__init__ → push_local``
顶层回环(该环迁移前即潜伏存在,靠导入顺序侥幸;此处变为显式保证)。

门面:显式符号白名单(不做 ``import *`` 合并——遮蔽取舍无判据);仓内
消费方也可直接走子模块新径。
"""
import myssia.push  # noqa: F401  # 暖导入(见上)

from myssia.wechat.engine import WechatLocalEngine
from myssia.wechat.notify import fetch_notify, validate_options
from myssia.wechat.push_local import DEFAULT_BRIDGE_BIN, WeixinLocalChannel
from myssia.wechat.push_weixin import WeixinChannel, probe_bridge
from myssia.wechat.push_wecom import WecomChannel
from myssia.wechat.sidecar import run_bridge_command_sync
from myssia.wechat.stats_sidecar import config_path

__all__ = [
    "WechatLocalEngine",
    "validate_options",
    "fetch_notify",
    "WeixinChannel",
    "WeixinLocalChannel",
    "WecomChannel",
    "probe_bridge",
    "DEFAULT_BRIDGE_BIN",
    "run_bridge_command_sync",
    "config_path",
]
