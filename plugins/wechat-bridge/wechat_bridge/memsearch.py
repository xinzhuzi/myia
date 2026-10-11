"""内存密钥搜索空壳(task 10-11-wechat-ui-bridge E1;默认关,**绝不真跑**)。

红线锚点(prd 红线 1/3,design §4):

- 内存密钥搜索(PyWxDump / 参考件 wechat-mcp-macos ``crypto/keys/scanner_macos.py``
  的进程内存扫描路数)是本地库密钥的**降级候选**——启用前须主人 D4 裁决
  豁免,**本模块即 D4 未豁免期的全部实现:一个默认关的空壳**。
- 空壳语义:本文件**不含任何进程内存读取代码**(无进程句柄/内存读/调试
  API 的任何引用,一个字都不写),只有启用开关与拒绝性应答;
  ``acquire_key_from_memory`` 恒抛 §6 exit 21 ``key_unavailable`` 并如实
  说明「默认关,主人显式开启才生效」。
- 启用判据(D4 豁免后的三重门):①主人裁决记录在案(任务档 A4);②
  :data:`MEMORY_SEARCH_ENABLED` 在代码层显式改 True(无配置键——design §7
  封闭清单刻意不提供开关配置面);③真实现另行评审后落位(本空壳不含)。
- 2026-10-11 E1 实测背景:零内存途径(key_info.db)已证不可推导,但
  **「零内存失败」不构成内存搜索的自动豁免**——那是红线 1 的独立裁决项,
  归主人。
"""

from __future__ import annotations

from .codes import KEY_UNAVAILABLE, BridgeError

__all__ = ["MEMORY_SEARCH_ENABLED", "acquire_key_from_memory"]

#: 内存密钥搜索总开关(**默认关**;唯一改法 = D4 豁免后代码层显式改值;
#: 刻意无配置键,防「配置了却没生效」的假象与误开)。
MEMORY_SEARCH_ENABLED = False


def acquire_key_from_memory(*args: object, **kwargs: object) -> bytes:
    """内存密钥搜索入口(**空壳,恒拒绝**)。

    任何调用(无论参数)都返回 §6 exit 21 ``key_unavailable`` 结构化错误;
    本函数**绝不触碰任何进程、绝不导入任何进程级 API**。
    """
    raise BridgeError(
        KEY_UNAVAILABLE,
        "内存密钥搜索默认关(空壳):主人未作 D4 豁免裁决,本路径拒绝执行"
        f"(MEMORY_SEARCH_ENABLED={MEMORY_SEARCH_ENABLED})",
        fix_hint=(
            "D4 豁免裁决在案后,由主人在代码层显式开启(无配置键,design §7);"
            "当前合法途径仅剩外部密钥引入(all_keys.json 类,600 权限私有区)"
        ),
    )
