"""wechat_local 引擎 notify 通道件(10-14-wechat-notify-revoke R4;新文件)。

引擎第四通道 ``notify`` 的实现体,与 :mod:`myssia.engines.wechat_local`
既有三通道(pixel/localdb/sns)同一形态族——**本模块只提供实现件**
(词表校验/水位 kv/条目铸锚/取数全链),通道词表与分发接线在引擎本体
(``CHANNELS`` 加 ``"notify"``、``_options``/``_fetch_impl`` 分支),由
集成会话统一落笔(见任务档 integrationSpec):

.. code-block:: python

    # wechat_local._options():channel == "notify" 分支
    return wechat_local_notify.validate_options(options)
    # wechat_local._fetch_impl():channel == "notify" 分支
    return await wechat_local_notify.fetch_notify(self, options)

机制(单源单次 ``localdb notify-scan`` 桥调用):

- **会话白名单** ``chat_whitelist``(id 或显示名;显示名经桥 ``localdb query``
  应答 sessions 列表二查解析,localdb 通道同款惯例;id 形态
  ``@chatroom``/``wxid_`` 直通零二查)。空清单 = 声明即拒(白名单空 =
  功能空转,构造期 FetchError)。**键名注记**:PRD 原文写 ``sessions``——
  与 schema 全文档凭据基线撞名(``session`` 是凭据键后缀,子串命中即要求
  env:/keychain: 引用,会话 id 清单装不进去,schema.py ``is_credential_key``);
  故引擎键定名 ``chat_whitelist``(与桥 stdin 载荷键 ``whitelist`` 同词表),
  声明 ``sessions`` = 结构化拒并指路,不静默忽略。
- ``notify_self`` 缺省 false(自己发的消息不通知;桥侧同键 stdin 透传)。
- **水位**:store ``change_baseline`` 键 ``wechat-local://watermark/<源名>``,
  ``etag`` 存 JSON ``{"<chatId>": {"ts":…, "unread":…}}``(与 localdb 通道
  同键空间不同源名;TEXT 列零 schema 改动);**仅成功轮回写**,skip/失败
  不推进(下轮重开,lookback+锚去重消化重叠)。
- **条目锚(强幂等)**:新消息 ``wechat-local://notify/<urlencoded(chat)>
  #wxn-<server_id>``、撤回 ``#wxnr-<revoke server_id>``——比 #wx- 内容
  哈希锚强(重读/重装恒同锚);title=「<会话显示名> · <发送者>」(
  TITLE_MAX_CHARS 截断);content=预览(撤回=三态文案);metadata 平铺
  ``{event, session_id, session_display, sender_display, server_id,
  local_type, revoke, replacemsg_text}``(macos_notify 通道按
  ``session_display``/``event`` 取用;撤回另携 ``revoke_recovery``/
  ``revoke_original_preview`` 供浏览面)。
- **错误码表沿用**(引擎既有码表零新增):``key_unavailable`` 结构化
  skip 不算失败;db_not_found/decrypt_failed/bridge_timeout/
  component_missing 原样透传(消费引擎既有 ``_check_bridge_result`` 的
  映射,本模块零复制判定逻辑)。

私有数据红线:stdin 载荷/事件内容只活在桥 stdout → 管线内存 → store;
日志只留形状(白名单数/事件数/码名),永不打正文。
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

from myssia.engines.fetch_base import FetchError
from myssia.push.weixin_local import (
    LocalBridgeTimeoutError,
    bin_path,
    run_bridge_command_sync,
)

__all__ = [
    "DEFAULT_NOTIFY_TIMEOUT_SECONDS",
    "NOTIFY_ANCHOR_PREFIX",
    "REVOKE_ANCHOR_PREFIX",
    "fetch_notify",
    "notify_anchor",
    "read_notify_baseline",
    "revoke_anchor",
    "validate_options",
    "watermark_key",
    "write_notify_baseline",
]

logger = logging.getLogger(__name__)

#: notify 通道单次桥调用超时缺省(秒;notify-scan 恒轻——SessionTable 单查
#: + 候选分表定点,120 = 品类 timeouts.fetch 同值口径 + 首建副本余量)。
DEFAULT_NOTIFY_TIMEOUT_SECONDS = 120.0

#: 条目锚前缀(R4:#wxn- 新消息 / #wxnr- 撤回;#wx- 内容哈希锚同族命名)。
NOTIFY_ANCHOR_PREFIX = "#wxn-"
REVOKE_ANCHOR_PREFIX = "#wxnr-"

#: 显示名白名单的 id 形态直通判据(免二查;其余形态走 sessions 名解析)。
_ID_LIKE_SUFFIX = "@chatroom"
_ID_LIKE_PREFIX = "wxid_"

#: 标题截断(引擎 TITLE_MAX_CHARS 同值;惰性 import 见 _title_max)。
_TITLE_MAX_CHARS = 80


def _title_max() -> int:
    """引擎标题帽(惰性取,防循环导入;缺省 80 与引擎常量同值)。"""
    try:
        from myssia.engines.wechat_local import TITLE_MAX_CHARS

        return int(TITLE_MAX_CHARS)
    except Exception:  # noqa: BLE001 - 词表常量缺位 = 缺省帽,不炸取数
        return _TITLE_MAX_CHARS


def _watermark_key(source_name: str) -> str:
    """源级水位键(引擎 ``watermark_key`` 同族;惰性取防循环导入)。"""
    try:
        from myssia.engines.wechat_local import watermark_key

        return watermark_key(source_name)
    except Exception:  # noqa: BLE001 - 引擎不在场(单测直构)= 本地同构
        return f"wechat-local://watermark/{quote(source_name, safe='')}"


def watermark_key(source_name: str) -> str:
    """notify 水位键(公开面;与 localdb 通道同键空间,etag 形态不同)。"""
    return _watermark_key(source_name)


def notify_anchor(chat: str, server_id: object) -> str:
    """新消息强锚:``wechat-local://notify/<chat>#wxn-<server_id>``。"""
    return (
        f"wechat-local://notify/{quote(chat, safe='')}"
        f"{NOTIFY_ANCHOR_PREFIX}{server_id}"
    )


def revoke_anchor(chat: str, server_id: object) -> str:
    """撤回强锚:``wechat-local://notify/<chat>#wxnr-<server_id>``。"""
    return (
        f"wechat-local://notify/{quote(chat, safe='')}"
        f"{REVOKE_ANCHOR_PREFIX}{server_id}"
    )


# =====================================================================
# 词表校验(引擎 _options 的 notify 分支实现体)
# =====================================================================


def validate_options(options: dict[str, Any]) -> dict[str, Any]:
    """``engine_options.wechat_local`` 的 notify 通道校验与缺省化。

    消费键:``chat_whitelist``(非空字符串清单 = 会话白名单;显示名或
    会话 id——键名注记见模块 docstring,schema 凭据基线不容 ``sessions``
    键名)、``notify_self``(bool,缺省 false)、``read_timeout_seconds``
    (正数秒,缺省 120)。会话/朋友圈通道专属键(``chat``/``sides``/
    ``count``/``since_days``/``feed_kind``)交叉声明即拒——消费面不同,
    静默忽略会谎报配置生效(引擎既有 fail-fast 哲学)。
    """
    if "sessions" in options:
        raise FetchError(
            "engine_options.wechat_local.sessions 键不可用:schema 全文档凭据基线"
            "把含 session 的键当凭据位(值必须是 env:/keychain: 引用,会话 id"
            " 清单装不进去);notify 通道白名单键定名 chat_whitelist",
            error_type="invalid_engine_options",
        )
    for chat_key in ("chat", "sides", "count", "since_days", "feed_kind"):
        if chat_key in options:
            raise FetchError(
                f"engine_options.wechat_local.{chat_key} 是会话/朋友圈通道"
                "(pixel/localdb/sns)的配置,notify 通道不消费(白名单用"
                " chat_whitelist 声明;窗口 = 桥侧会话基线水位,零天数参数)",
                error_type="invalid_engine_options",
            )
    sessions = options.get("chat_whitelist")
    if (
        not isinstance(sessions, list)
        or not sessions
        or any(
            isinstance(item, bool) or not isinstance(item, str) or not item.strip()
            for item in sessions
        )
    ):
        raise FetchError(
            "engine_options.wechat_local.chat_whitelist 应为非空字符串清单"
            "(notify 会话白名单:会话 id(wxid_xxx/xxx@chatroom)或显示名;"
            "空清单 = 白名单空 = 功能空转,构造期即拒;不声明即不通知)",
            error_type="invalid_engine_options",
        )
    notify_self = options.get("notify_self", False)
    if not isinstance(notify_self, bool):
        raise FetchError(
            "engine_options.wechat_local.notify_self 应为布尔(缺省 false:"
            f"自己发的消息不通知),当前为 {notify_self!r}",
            error_type="invalid_engine_options",
        )
    timeout = options.get("read_timeout_seconds", DEFAULT_NOTIFY_TIMEOUT_SECONDS)
    if (
        isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
        or timeout <= 0
    ):
        raise FetchError(
            "engine_options.wechat_local.read_timeout_seconds 应为正数秒"
            f"(单次桥 notify-scan 上界;notify 缺省 {DEFAULT_NOTIFY_TIMEOUT_SECONDS:.0f}"
            " 恒轻扫描),当前为 "
            f"{timeout!r}",
            error_type="invalid_engine_options",
        )
    return {
        "channel": "notify",
        "chat_whitelist": [item.strip() for item in sessions],
        "notify_self": notify_self,
        "read_timeout_seconds": float(timeout),
    }


# =====================================================================
# 水位 kv(JSON 基线;仅成功轮回写)
# =====================================================================


def read_notify_baseline(store: Any, source_name: str) -> dict[str, Any]:
    """读 notify 水位(桥契约 baseline 形状);无 store/无水位/坏值 = {}。

    坏值(非 JSON/非对象)按无水位处理并告警形状——试抓/干跑无 store 时
    如实降级(首轮语义,桥侧只建基线零事件,不轰炸)。
    """
    if store is None:
        return {}
    try:
        baseline = store.get_baseline(_watermark_key(source_name))
    except Exception:  # noqa: BLE001 - store 面故障不炸取数(缺省窗重开)
        return {}
    if baseline is None or not baseline.etag:
        return {}
    try:
        data = json.loads(baseline.etag)
    except ValueError:
        logger.warning(
            "wechat_local notify 水位值不可解析,按无水位处理 source=%s"
            "(形状级:etag 非 JSON)",
            source_name,
        )
        return {}
    if not isinstance(data, dict):
        return {}
    cleaned: dict[str, Any] = {}
    for chat_id, entry in data.items():
        if isinstance(chat_id, str) and isinstance(entry, dict):
            cleaned[chat_id] = entry
    return cleaned


def write_notify_baseline(store: Any, source_name: str, baseline: dict[str, Any]) -> None:
    """成功轮后回写水位(etag = JSON 基线;键序稳定便于人读/对账)。"""
    if store is None:
        return
    store.set_baseline(
        _watermark_key(source_name),
        etag=json.dumps(baseline, ensure_ascii=False, sort_keys=True),
        last_changed=datetime.now(timezone.utc),
    )


# =====================================================================
# 条目铸形(events → 管线条目)
# =====================================================================


def _clip_title(text: str) -> str:
    limit = _title_max()
    return text if len(text) <= limit else text[:limit] + "…"


def _event_server_id(event: dict[str, Any], fallback: object) -> object:
    server_id = event.get("server_id")
    if isinstance(server_id, int) and server_id > 0:
        return server_id
    return fallback


def _revoke_body(event: dict[str, Any]) -> str:
    """撤回三态文案(R3 契约:恢复原文 / replacemsg 兜底 / 未能恢复)。"""
    original = event.get("original")
    if isinstance(original, dict):
        preview = original.get("content_preview")
        if isinstance(preview, str) and preview.strip():
            return f'原内容:"{preview}"'
    replacemsg = event.get("replacemsg_text")
    if isinstance(replacemsg, str) and replacemsg.strip():
        return replacemsg
    return "原内容未能恢复"


def items_from_events(events: list[Any]) -> list[dict[str, Any]]:
    """桥 notify_scan 事件 → 管线条目(#wxn-/#wxnr- 强锚;Item 契约)。

    metadata 平铺 R4 契约键(撤回另携 ``revoke_recovery``/
    ``revoke_original_preview``,供浏览面/通知通道三态取用);``sender``/
    ``side``/``ts``/``chat`` 留 raw 面(feed v1 不投影,localdb 通道同款)。
    """
    items: list[dict[str, Any]] = []
    for index, raw in enumerate(events):
        if not isinstance(raw, dict):
            continue
        event_name = raw.get("event")
        chat = str(raw.get("session_id") or "")
        ts = raw.get("ts")
        ts = ts if isinstance(ts, int) else None
        if event_name == "message.revoke":
            revoker = str(raw.get("revoker_display") or raw.get("sender_display") or "")
            session_display = str(raw.get("session_display") or chat)
            original = raw.get("original")
            recovery = (
                original.get("recovery")
                if isinstance(original, dict)
                else ("replacemsg" if raw.get("replacemsg_text") else "none")
            )
            original_preview = (
                original.get("content_preview") if isinstance(original, dict) else None
            )
            replacemsg_text = raw.get("replacemsg_text")
            body = _revoke_body(raw)
            items.append({
                "url": revoke_anchor(chat, _event_server_id(raw, f"{ts}-{index}")),
                "title": _clip_title(f"{session_display} · {revoker} 撤回了一条消息"),
                "content": f"{revoker}撤回了一条消息:{body}" if revoker else body,
                "sender": revoker or None,
                "side": "left",
                "ts": ts,
                "chat": chat,
                "event": "message.revoke",
                "session_id": chat,
                "session_display": session_display,
                "sender_display": revoker or None,
                "server_id": raw.get("server_id"),
                "local_type": raw.get("local_type"),
                "revoke": True,
                "replacemsg_text": (
                    replacemsg_text if isinstance(replacemsg_text, str) else None
                ),
                "revoke_recovery": recovery,
                "revoke_original_preview": (
                    original_preview if isinstance(original_preview, str) else None
                ),
            })
            continue
        # message.new(未知 event 形状按 new 处理?不——如实跳过,不臆造)
        if event_name != "message.new":
            continue
        sender = str(raw.get("sender_display") or "")
        session_display = str(raw.get("session_display") or chat)
        preview = raw.get("content_preview")
        preview = preview if isinstance(preview, str) else ""
        items.append({
            "url": notify_anchor(chat, _event_server_id(raw, f"{ts}-{index}")),
            "title": _clip_title(f"{session_display} · {sender}".rstrip(" ·")),
            "content": preview,
            "sender": sender or None,
            "side": "right" if raw.get("is_self") else "left",
            "ts": ts,
            "chat": chat,
            "event": "message.new",
            "session_id": chat,
            "session_display": session_display,
            "sender_display": sender or None,
            "server_id": raw.get("server_id"),
            "local_type": raw.get("local_type"),
            "revoke": False,
            "replacemsg_text": None,
        })
    return items


# =====================================================================
# 取数全链(引擎 _fetch_impl 的 notify 分支实现体)
# =====================================================================


async def _run_bridge_stdin(
    argv: list[str], input_text: str, timeout: float, *, label: str
) -> tuple[int, str]:
    """桥子进程往返(带 stdin 载荷;引擎 ``_run_bridge`` 的 stdin 形态)。

    to_thread 不堵事件循环;超时 = ``bridge_timeout``(引擎码表)。
    """
    try:
        exit_code, stdout, _stderr = await asyncio.to_thread(
            run_bridge_command_sync,
            argv,
            input_text,
            timeout,
        )
    except LocalBridgeTimeoutError as exc:
        raise FetchError(
            f"{label}超时:{exc}(上限 {timeout:.0f} 秒;多为暂时现象,稍后重试即可)",
            error_type="bridge_timeout",
        ) from exc
    return exit_code, stdout


def _looks_like_session_id(entry: str) -> bool:
    """id 形态直通判据(@chatroom 后缀 / wxid_ 前缀;其余按显示名二查)。"""
    return entry.endswith(_ID_LIKE_SUFFIX) or entry.startswith(_ID_LIKE_PREFIX)


async def _resolve_display_names(
    engine: Any, bridge_bin: str, declared: list[str], timeout: float
) -> list[str]:
    """显示名白名单二查解析(localdb 通道 ``_resolve_session_id`` 同款惯例)。

    id 形态直通;显示名经一次 ``localdb query <名> --since 1d`` 应答的
    sessions 列表按名精确匹配解析(桥 best-effort 前 20 行,不在列表 =
    解析不到,如实保留原名——桥侧 SessionTable 无此行 = 零事件,不猜)。
    解析调用失败(密钥缺位/桥错)不炸本轮:保留原名如实零产出,主扫描
    随后给出真实的失败/skip。
    """
    resolved: list[str] = []
    for entry in declared:
        if _looks_like_session_id(entry):
            resolved.append(entry)
            continue
        argv = [bridge_bin, "localdb", "query", entry, "--since", "1d", "--json"]
        try:
            exit_code, stdout = await engine._run_bridge(
                argv, timeout, label="解析会话显示名"
            )
            payload = engine._check_bridge_result(
                exit_code, stdout, skip_codes=frozenset({"key_unavailable"})
            )
        except FetchError as exc:
            logger.info(
                "wechat_local notify 显示名解析不可用,保留声明名 source=%s"
                " entry_shape=%s error=%s(形状级;主扫描随后给出真实态)",
                getattr(getattr(engine, "source", None), "name", "?"),
                "display-name",
                exc.error_type,
            )
            resolved.append(entry)
            continue
        if payload is None:
            resolved.append(entry)  # 密钥缺位:保留原名(主扫描同 skip)
            continue
        session_id = None
        sessions = payload.get("sessions")
        if isinstance(sessions, list):
            for session in sessions:
                if not isinstance(session, dict):
                    continue
                candidate = session.get("id")
                if (
                    isinstance(candidate, str)
                    and candidate
                    and session.get("name") == entry
                ):
                    session_id = candidate
                    break
        if session_id is not None:
            logger.info(
                "wechat_local notify 白名单显示名解析出会话 id source=%s"
                "(形状级:二查,不记内容)",
                getattr(getattr(engine, "source", None), "name", "?"),
            )
            resolved.append(session_id)
        else:
            resolved.append(entry)
    return resolved


async def fetch_notify(engine: Any, options: dict[str, Any]) -> list[dict[str, Any]]:
    """notify 通道取数全链:白名单解析 → 水位读 → 单次 notify-scan → 条目。

    ``engine`` 鸭子类型(消费引擎既有件:``source.name``/``context.store``/
    ``_run_bridge``/``_check_bridge_result``/``last_skip_reason``——全部
    当前锋线在位方法,零共享文件改动)。key_unavailable = 结构化 skip
    (零条目不算失败,水位不推进);成功轮(含零事件)回写桥侧新基线。
    """
    resolved_bin = bin_path(None)
    if not (resolved_bin.is_file() and os.access(resolved_bin, os.X_OK)):
        raise FetchError(
            "微信本机桥组件 bin 不存在或不可执行: "
            f"{resolved_bin}。修复指引:到设置安装 wechat-bridge 组件"
            "(前置 brew install sqlcipher)",
            error_type="component_missing",
        )
    bridge_bin = str(resolved_bin)
    timeout = options["read_timeout_seconds"]
    whitelist = await _resolve_display_names(engine, bridge_bin, options["chat_whitelist"], timeout)
    store = getattr(getattr(engine, "context", None), "store", None)
    source_name = getattr(getattr(engine, "source", None), "name", "")
    baseline = read_notify_baseline(store, source_name)
    stdin_payload = json.dumps(
        {
            "whitelist": whitelist,
            "baseline": baseline or None,
            "notify_self": options["notify_self"],
        },
        ensure_ascii=False,
    )
    argv = [bridge_bin, "localdb", "notify-scan", "--file", "-", "--json"]
    exit_code, stdout = await _run_bridge_stdin(
        argv, stdin_payload, timeout, label="扫描微信新消息通知"
    )
    payload = engine._check_bridge_result(
        exit_code, stdout, skip_codes=frozenset({"key_unavailable"})
    )
    if payload is None:
        engine.last_skip_reason = "key_unavailable"
        logger.info(
            "wechat_local notify 显式空态:解密密钥未就绪(key_unavailable),"
            "本轮跳过不算失败 source=%s。指引:跑仓库 %s(主人 sudo 一键"
            "内存密钥扫描,命中自动落 keys.json,下一轮即通)",
            source_name,
            "scripts/wechat-bridge-d4-keyscan.sh",
        )
        return []
    node = payload.get("notify_scan")
    if not isinstance(node, dict):
        raise FetchError(
            "wechat-bridge 组件返回的结果缺 notify_scan 节;请重装或升级该"
            "组件(需要 0.8.0+)",
            error_type="bridge_error",
        )
    events = node.get("events")
    if not isinstance(events, list):
        raise FetchError(
            "wechat-bridge 组件返回的结果缺 notify_scan.events 列表;请重装"
            "或升级该组件(需要 0.8.0+)",
            error_type="bridge_error",
        )
    items = items_from_events(events)
    new_baseline = node.get("baseline")
    if isinstance(new_baseline, dict) and new_baseline:
        # 仅成功轮回写;空基线(白名单会话全不在 SessionTable)如实写空
        # 之外——空 dict 不写,防首轮把「未见过」误固化为「已见过」。
        write_notify_baseline(store, source_name, new_baseline)
    stats = node.get("stats")
    logger.info(
        "wechat_local notify 窗口取得 source=%s whitelist=%s events=%s items=%s"
        " busy=%s(形状级,不记内容)",
        source_name,
        len(whitelist),
        len(events),
        len(items),
        stats.get("db_busy") if isinstance(stats, dict) else None,
    )
    return items
