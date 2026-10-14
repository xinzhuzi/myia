"""兼容壳(10-14-wechat-module):真身已迁 myssia.wechat.push_weixin;仓内一律新径,壳只保仓外。"""
from myssia.wechat.push_weixin import *  # noqa: F401,F403
from myssia.wechat.push_weixin import WeixinChannel, probe_bridge  # noqa: F401
