"""微信渠道模块(10-14-wechat-module;超越 TG 的收拢形态,见任务档)。

导入序保证:先完整初始化 :mod:`myssia.push`(其 ``__init__`` 末段会导入
``push_local``),否则 ``sidecar → push_local → push/__init__ → push_local``
顶层回环(该环迁移前即潜伏存在,靠导入顺序侥幸;此处变为显式保证)。
"""
import myssia.push  # noqa: F401  # 暖导入(见上)
