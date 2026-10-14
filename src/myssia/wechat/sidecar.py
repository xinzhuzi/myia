"""微信本机桥 sidecar 协议面(task 10-11-wechat-ui-bridge Phase F2)。

四个协议方法的实现本体(desktop/entry.py ``_HANDLERS`` 只做薄壳转接):
``wechat_local.probe`` / ``wechat_local.sessions`` / ``wechat_local.messages``
/ ``wechat_local.query`` —— 受管组件 wechat-bridge(design §6 CLI 契约)的
sidecar 适配层:参数校验 → 一次性子进程 → 应答透传 / 结构化错误归一。

职责边界(刻意薄):发送频控(G6)、AX 静默铁律(prd 红线 4)、私有数据
红线(prd 红线 6)全在桥内实施,本层零复制零覆写——handler 只递参数、
透传契约载荷、把桥的具名错误族原样上抛(码名即 design §6 表,UI 按码
映射文案与三态)。聊天内容/密钥材料只活在应答载荷里(stdout 契约),
本层不打日志、不落盘、不进异常文本。

bin 路径真源 = :data:`~myssia.wechat.push_local.DEFAULT_BRIDGE_BIN`(受管
组件安装落点;品类 YAML push 条目的 ``wechat_bridge_bin`` 覆写作用于发送
通道,协议面用缺省落点——不给协议 params 留任意路径执行缝)。

模块位置:src/myssia(随包打包,myssia-core.spec 自动覆盖),entry.py
接线 = 每方法一个三行薄壳(``WechatLocalSidecarError`` → ``ProtocolError``
换轨)。设计依据:任务档 design §1「local-db 通道:CLI + sidecar handler
挂载」+ sidecar-protocol.md 变更纪律(纯加法批不 bump PROTOCOL_VERSION,
循 gates/run.status 历史行批「地基路」先例)。
"""

from __future__ import annotations

from typing import Any

from myssia.wechat.push_local import (
    DEFAULT_BRIDGE_TIMEOUT_SECONDS,
    DEFAULT_PROBE_TIMEOUT_SECONDS,
    LocalBridgeTimeoutError,
    bin_path,
    parse_bridge_payload,
    probe_local_bridge,
    run_bridge_command_sync,
)

__all__ = [
    "WechatLocalSidecarError",
    "handle_wechat_local",
]

#: 桥命令族超时:probe 走探针专用上界;读命令(sessions/messages)与发送
#: 走发送同款 60s(本地单命令上界;超时 = 桥挂起,kill 兜底)。
_COMMAND_TIMEOUT_SECONDS = DEFAULT_BRIDGE_TIMEOUT_SECONDS
#: ``localdb query`` 专用上界(秒):桥侧 sqlcipher **单库**解密超时上限
#: 300s(wechat_bridge.localdb ``SQLCIPHER_TIMEOUT_SECONDS``),D4 引入外部
#: 密钥后首查大概率触发多域副本**首建**(design §7 缺省 3 域 4 库),累计
#: 可超 60s——60s 会把首查误杀成 ``bridge_timeout``。取 2×单库上界盖住缺省
#: 域首建;副本 kept 语义(G5)让超时 kill 后重试只补缺库,不推倒重来。
#: 真超 600s 的解密已属异常,kill 兜底如实 ``bridge_timeout``。
_QUERY_TIMEOUT_SECONDS = 600.0

#: 协议参数上界(防一把梭全量拉取;桥内另有配置 limits 兜底)。
_LIMIT_SESSIONS_MAX = 100
_LIMIT_MESSAGES_MAX = 200
_SINCE_DAYS_MAX = 3650
#: C1 分页/普查上界(桥 localdb_page.PAGE_LIMIT_CAP/CONVERSATIONS_LIMIT_MAX 同值)。
_LIMIT_PAGE_MAX = 1000
_LIMIT_CONVERSATIONS_MAX = 5000
#: C3 朋友圈/媒体窗口上界(sns feed 判例同值)。
_LIMIT_MEDIA_SINCE_DAYS_MAX = 3650
#: C4 联系人 limit 三态上界(0 = 全量导出态合法;桥 contacts_query 帽同值)。
_LIMIT_CONTACTS_MAX = 1000


class WechatLocalSidecarError(Exception):
    """协议层结构化错误(entry.py 薄壳换轨为 ``ProtocolError``)。

    ``code`` 对外三族:协议参数错 = ``invalid_params``;桥超时 =
    ``bridge_timeout``;其余 = 桥具名错误族原样(design §6 码名,如
    ``not_implemented`` / ``wechat_not_running`` / ``key_unavailable``)。
    """

    def __init__(
        self, code: str, message: str, *, path: str = "$", data: Any = None
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path
        self.data = data


def _require_str(params: dict[str, Any], key: str) -> str:
    value = params.get(key)
    if not isinstance(value, str) or not value.strip():
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.{key} 必须是非空字符串",
            path=f"params.{key}",
        )
    return value.strip()


def _optional_int(
    params: dict[str, Any],
    key: str,
    *,
    default: int | None,
    maximum: int,
) -> int | None:
    value = params.get(key)
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0 or value > maximum:
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.{key} 须为 1..{maximum} 的整数",
            path=f"params.{key}",
        )
    return value


def _run_bridge(argv: list[str], *, timeout: float) -> dict[str, Any]:
    """跑桥子进程并归一应答:成功载荷原样;失败映射结构化错误。

    桥 stdout 恒单 JSON:成功 = 命令契约载荷;失败 = ``{"error": {...}}``
    (码名/人话/指引,design §6)。bin 缺失 = ``component_missing``(与
    :func:`probe_local_bridge` 的合成码同词表)。
    """
    resolved = bin_path(argv[0])
    if not (resolved.is_file() and resolved.stat().st_mode & 0o111):
        raise WechatLocalSidecarError(
            "component_missing",
            f"微信本机桥组件 bin 不存在或不可执行: {resolved}",
            data={
                "fix_hint": "到设置安装 wechat-bridge 组件(前置 brew install "
                "sqlcipher),或用品类 YAML push 条目的 wechat_bridge_bin 覆写路径"
            },
        )
    try:
        exit_code, stdout, _stderr = run_bridge_command_sync(argv, "", timeout)
    except LocalBridgeTimeoutError as exc:
        raise WechatLocalSidecarError("bridge_timeout", str(exc)) from exc
    payload = parse_bridge_payload(stdout)
    if exit_code == 0 and isinstance(payload, dict) and not payload.get("error"):
        return payload
    error = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(error, dict) and error.get("code"):
        data: dict[str, Any] = {}
        if error.get("fix_hint"):
            data["fix_hint"] = str(error["fix_hint"])
        if error.get("retry_after_seconds") is not None:
            data["retry_after_seconds"] = error["retry_after_seconds"]
        raise WechatLocalSidecarError(
            str(error["code"]), str(error.get("message") or f"桥 exit={exit_code}"),
            data=data or None,
        )
    raise WechatLocalSidecarError(
        "bridge_error",
        f"wechat-bridge 组件返回了无法识别的结果(exit={exit_code});请重装或升级该组件",
    )


def _probe(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.probe`` {} → 桥 ``--probe`` 三态载荷(缺参不拒)。

    探针是健康面:组件缺席/超时/应答不可解析都返回**同形合成载荷**
    (state 恒 ``bridge_unavailable``),永不抛——UI 卡永远拿到可渲染三态。
    """
    del params  # 探针零参数;多余键宽容(地基路纯加法纪律)
    return probe_local_bridge(None, timeout=DEFAULT_PROBE_TIMEOUT_SECONDS)


def _sessions(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.sessions`` {limit?} → 桥 ``sessions list --json``。"""
    limit = _optional_int(params, "limit", default=None, maximum=_LIMIT_SESSIONS_MAX)
    argv = [_BASE, "sessions", "list", "--json"]
    if limit is not None:
        argv += ["-n", str(limit)]
    return _run_bridge(argv, timeout=_COMMAND_TIMEOUT_SECONDS)


def _messages(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.messages`` {chat_id, count?} → 桥 ``messages read``。"""
    chat_id = _require_str(params, "chat_id")
    count = _optional_int(params, "count", default=None, maximum=_LIMIT_MESSAGES_MAX)
    argv = [_BASE, "messages", "read", chat_id, "--json"]
    if count is not None:
        argv += ["-k", str(count)]
    return _run_bridge(argv, timeout=_COMMAND_TIMEOUT_SECONDS)


def _query(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.query`` {chat_id, since_days?} → 桥 ``localdb query``。

    since_days 缺省 30(design §7 limits.history_days 缺省同值);上界
    3650 天是协议面防呆,不是业务约束。超时走 :data:`_QUERY_TIMEOUT_SECONDS`
    (盖住桥侧多域副本首建,见该常量注记),不用 60s 命令族上界。
    """
    chat_id = _require_str(params, "chat_id")
    since_days = _optional_int(
        params, "since_days", default=30, maximum=_SINCE_DAYS_MAX
    )
    argv = [_BASE, "localdb", "query", chat_id, "--since", f"{since_days}d", "--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


def _optional_int_min0(
    params: dict[str, Any], key: str, *, maximum: int
) -> int | None:
    """C4 联系人 limit 三态:0 = 全量导出态合法(:func:`_optional_int` 拒 0,
    此变体放行;负数/非 int/超帽仍 invalid_params)。"""
    value = params.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > maximum:
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.{key} 须为 0..{maximum} 的整数(0 = 全量导出态)",
            path=f"params.{key}",
        )
    return value


def _optional_ts(params: dict[str, Any], key: str) -> int | None:
    """C1 时间窗参数:非负整数时间戳(秒;桥侧 normalize_ts_input 再归一)。"""
    value = params.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise WechatLocalSidecarError(
            "invalid_params",
            f"params.{key} 须为非负整数时间戳(unix 秒)",
            path=f"params.{key}",
        )
    return value


def _page(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.page`` {chat_id, cursor?, limit?, asc?, from_ts?, to_ts?,
    types?, sender?} → 桥 ``localdb page``(C1 keyset 分页;10-14-wechat-chat-export)。

    limit 帽 1000(桥 PAGE_LIMIT_CAP 同值);types 数组 → CLI 逗号分隔;
    超时走 :data:`_QUERY_TIMEOUT_SECONDS`(副本首建判例同 query)。
    """
    chat_id = _require_str(params, "chat_id")
    limit = _optional_int(params, "limit", default=None, maximum=_LIMIT_PAGE_MAX)
    asc = params.get("asc")
    if asc is not None and not isinstance(asc, bool):
        raise WechatLocalSidecarError(
            "invalid_params", "params.asc 须为布尔", path="params.asc"
        )
    from_ts = _optional_ts(params, "from_ts")
    to_ts = _optional_ts(params, "to_ts")
    types = params.get("types")
    if types is not None:
        if not isinstance(types, list) or not all(
            isinstance(item, str) and item.strip() for item in types
        ):
            raise WechatLocalSidecarError(
                "invalid_params",
                "params.types 须为非空字符串数组(转 CLI 逗号分隔)",
                path="params.types",
            )
    sender = params.get("sender")
    if sender is not None and (not isinstance(sender, str) or not sender.strip()):
        raise WechatLocalSidecarError(
            "invalid_params", "params.sender 必须是非空字符串", path="params.sender"
        )
    cursor = params.get("cursor")
    if cursor is not None and not isinstance(cursor, str):
        raise WechatLocalSidecarError(
            "invalid_params", "params.cursor 须为字符串", path="params.cursor"
        )
    argv = [_BASE, "localdb", "page", chat_id]
    if cursor:
        argv += ["--cursor", cursor]
    if limit is not None:
        argv += ["--limit", str(limit)]
    if asc is not None:
        argv += ["--asc" if asc else "--desc"]
    if from_ts is not None:
        argv += ["--from-ts", str(from_ts)]
    if to_ts is not None:
        argv += ["--to-ts", str(to_ts)]
    if types:
        argv += ["--types", ",".join(t.strip() for t in types)]
    if sender:
        argv += ["--sender", sender.strip()]
    argv += ["--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


def _conversations(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.conversations`` {limit?} → 桥 ``localdb conversations``
    (C1 会话清单普查;limit 帽 5000 = 桥 CONVERSATIONS_LIMIT_MAX 同值)。"""
    limit = _optional_int(
        params, "limit", default=None, maximum=_LIMIT_CONVERSATIONS_MAX
    )
    argv = [_BASE, "localdb", "conversations"]
    if limit is not None:
        argv += ["--limit", str(limit)]
    argv += ["--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


def _sns_feed(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.sns_feed`` {since_days?} → 桥 ``localdb sns feed``
    (C3;缺省 30d,帽 3650d;argv 契约钉死在
    tests/desktop/test_wechat_local_media_handlers.py)。"""
    since_days = _optional_int(
        params, "since_days", default=30, maximum=_LIMIT_MEDIA_SINCE_DAYS_MAX
    )
    argv = [_BASE, "localdb", "sns", "feed", "--since", f"{since_days}d", "--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


def _sns_export(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.sns_export`` {format?, out?, since_days?, with_media?} →
    桥 ``localdb sns export``(C3;format ∈ json|html 缺省 json)。"""
    fmt = params.get("format", "json")
    if fmt not in ("json", "html"):
        raise WechatLocalSidecarError(
            "invalid_params",
            "params.format 须为 json|html",
            path="params.format",
        )
    since_days = _optional_int(
        params, "since_days", default=30, maximum=_LIMIT_MEDIA_SINCE_DAYS_MAX
    )
    out = params.get("out")
    if out is not None and (not isinstance(out, str) or not out.strip()):
        raise WechatLocalSidecarError(
            "invalid_params", "params.out 必须是非空字符串", path="params.out"
        )
    with_media = params.get("with_media", False)
    if not isinstance(with_media, bool):
        raise WechatLocalSidecarError(
            "invalid_params", "params.with_media 须为布尔", path="params.with_media"
        )
    argv = [_BASE, "localdb", "sns", "export", "--format", fmt, "--since", f"{since_days}d"]
    if out:
        argv += ["--out", out.strip()]
    if with_media:
        argv += ["--with-media"]
    argv += ["--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


def _media_scan(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.media_scan`` {chat_id, since_days?, decrypt?} → 桥
    ``localdb media scan``(C3 寻径;--decrypt 逐条解密回填)。"""
    chat_id = _require_str(params, "chat_id")
    since_days = _optional_int(
        params, "since_days", default=30, maximum=_LIMIT_MEDIA_SINCE_DAYS_MAX
    )
    decrypt = params.get("decrypt", False)
    if not isinstance(decrypt, bool):
        raise WechatLocalSidecarError(
            "invalid_params", "params.decrypt 须为布尔", path="params.decrypt"
        )
    argv = [_BASE, "localdb", "media", "scan", chat_id, "--since", f"{since_days}d"]
    if decrypt:
        argv += ["--decrypt"]
    argv += ["--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


def _media_decrypt(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.media_decrypt`` {dat_path} → 桥 ``localdb media
    decrypt``(C3 单件 .dat 解密;未配置解密件 = exit 23 原样上抛)。"""
    dat_path = _require_str(params, "dat_path")
    argv = [_BASE, "localdb", "media", "decrypt", dat_path, "--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


#: C4 联系人六桶词表(桥 contacts_query.TYPE_FILTERS 同源)。
_CONTACTS_TYPE_FILTERS = ("friend", "group", "official", "former", "other")


def _contacts(params: dict[str, Any]) -> dict[str, Any]:
    """``wechat_local.contacts`` {type?, keyword?, limit?, cursor?,
    with_residue?, include_stranger?} → 桥 ``localdb contacts``(C4;limit
    0 = 全量导出态合法;include_stranger 缺省开=超参不传)。超时走
    :data:`_QUERY_TIMEOUT_SECONDS`(residue 首跑触发 message 域副本首建)。"""
    type_filter = params.get("type")
    if type_filter is not None:
        if not isinstance(type_filter, str) or type_filter not in _CONTACTS_TYPE_FILTERS:
            raise WechatLocalSidecarError(
                "invalid_params",
                f"params.type 须为 {'|'.join(_CONTACTS_TYPE_FILTERS)} 之一",
                path="params.type",
            )
    keyword = params.get("keyword")
    if keyword is not None and not isinstance(keyword, str):
        raise WechatLocalSidecarError(
            "invalid_params", "params.keyword 须为字符串", path="params.keyword"
        )
    limit = _optional_int_min0(params, "limit", maximum=_LIMIT_CONTACTS_MAX)
    cursor = params.get("cursor")
    if cursor is not None and not isinstance(cursor, str):
        raise WechatLocalSidecarError(
            "invalid_params", "params.cursor 须为字符串", path="params.cursor"
        )
    with_residue = params.get("with_residue", False)
    if not isinstance(with_residue, bool):
        raise WechatLocalSidecarError(
            "invalid_params",
            "params.with_residue 须为布尔",
            path="params.with_residue",
        )
    include_stranger = params.get("include_stranger")
    if include_stranger is not None and not isinstance(include_stranger, bool):
        raise WechatLocalSidecarError(
            "invalid_params",
            "params.include_stranger 须为布尔",
            path="params.include_stranger",
        )
    argv = [_BASE, "localdb", "contacts"]
    if type_filter:
        argv += ["--type", type_filter]
    if keyword:
        argv += ["--keyword", keyword]
    if limit is not None:
        argv += ["--limit", str(limit)]
    if cursor:
        argv += ["--cursor", cursor]
    if with_residue:
        argv += ["--with-residue"]
    # include_stranger:CLI 缺省 True,显式 false 桥侧无旗标可关(v1 如实
    # 只透传开态;协议面收形状不炸)。
    if include_stranger is False:
        raise WechatLocalSidecarError(
            "invalid_params",
            "params.include_stranger=false 暂不支持(桥 CLI 缺省开且无关闭旗标)",
            path="params.include_stranger",
        )
    argv += ["--json"]
    return _run_bridge(argv, timeout=_QUERY_TIMEOUT_SECONDS)


#: 桥 bin 缺省落点(构造期展开一次;模块单测经 monkeypatch 换注入点)。
_BASE = str(bin_path(None))


#: 动作 → 处理器(封闭词表;未知动作 = invalid_params,新增动作先扩此表)。
#: 六域接线批(0.8.0)纯加法七动作:C1 page/conversations、C3 sns_feed/
#: sns_export/media_scan/media_decrypt、C4 contacts——判例 F2 地基路,
#: 不 bump PROTOCOL_VERSION(stats 两动作在 wechat_stats_sidecar.py 独立模块)。
_ACTIONS = {
    "probe": _probe,
    "sessions": _sessions,
    "messages": _messages,
    "query": _query,
    "page": _page,
    "conversations": _conversations,
    "sns_feed": _sns_feed,
    "sns_export": _sns_export,
    "media_scan": _media_scan,
    "media_decrypt": _media_decrypt,
    "contacts": _contacts,
}


def handle_wechat_local(action: str, params: dict[str, Any] | None) -> dict[str, Any]:
    """协议分发入口(entry.py 四个薄壳各转接一个 action)。

    Args:
        action: ``probe`` / ``sessions`` / ``messages`` / ``query``。
        params: 协议 params(原样;各处理器自校验;None 视同空对象)。

    Raises:
        WechatLocalSidecarError: 结构化错误(薄壳换轨 ``ProtocolError``)。
    """
    handler = _ACTIONS.get(action)
    if handler is None:
        raise WechatLocalSidecarError(
            "invalid_params",
            f"未知 wechat_local 动作 {action!r}(合法:{sorted(_ACTIONS)})",
            path="method",
        )
    if params is None:
        params = {}
    if not isinstance(params, dict):
        raise WechatLocalSidecarError("invalid_params", "params 必须是对象", path="params")
    return handler(params)
