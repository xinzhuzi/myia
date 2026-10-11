"""wechat-bridge —— 微信本机桥(UI 自动化 + 本地库只读)。

受管组件(task 10-11-wechat-ui-bridge,G7 命名):独立 Python 实现、原生
运行,MYIA 本体只做一次性子进程调用(push 通道 ``weixin-local``,Phase F
注册;``weixin`` 通道名保持归官方 Hermes 桥 ``src/myssia/push/weixin.py``
——蓝本在,永不改动它)。

- CLI 契约与错误码:design §6(十二项错误码,封闭表);
- 配置面:design §7(数据根私有区 wechat-bridge/config.json,缺文件可用,
  无频控键);
- 测试纪律:design §8(AX/localdb 全 mock;真实客户端测试一律
  ``MYIA_WECHAT_E2E=1`` 门控,CI 无微信必须全绿);
- 静默铁律(prd 红线 4):不抢前台焦点、不合成鼠标点击、不激活微信窗口;
- 私有数据红线(prd 红线 6):聊天内容/密钥材料不入 git/日志/报告。

版本单一出处:本 ``__version__``;组件戳 component.json 同步维护(真锁
惯例,design §4)。
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
