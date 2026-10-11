"""桥 CLI(task 10-11-wechat-ui-bridge design §6;执行者零设计,照此实现)。

调用形态对齐 ``src/myssia/push/weixin.py`` 桥接 Hermes 惯例:一次性子进程、
``--json`` 机器可读应答、exit 三段语义(0 成功 / 1 通用失败 / 2 用法错,
失败段按 §6 细化码值)。**stdout 恒为单个 JSON 对象**(成功 = §6 各命令的
契约形状;失败 = ``{"error": {...}}``;argparse 用法错同样 JSON 化——
子类化 parser.error),人读诊断一律走 stderr——MYIA 侧只解析 stdout。

命令表(§6 原文):

.. code-block:: text

    wechat-bridge --probe
    wechat-bridge sessions list --json
    wechat-bridge messages read <id> -k 50
    wechat-bridge send_text <id> --file -
    wechat-bridge localdb query <chat> --since 7d --json

私有数据红线(prd 红线 6):argv 永不携带消息正文(send_text 正文走
stdin,weixin.py D0 同款——日志可安全打 argv);stderr 诊断只承载形状与
指引,永不承载聊天内容/密钥材料。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from . import __version__, ax, localdb
from .codes import EXIT_OK, EXIT_USAGE, BridgeError
from .config import BridgeConfig, load_config
from .probe import run_probe
from .send_state import SendRateState

__all__ = ["JsonArgumentParser", "build_parser", "main"]

_BRIDGE_VERSION = __version__


class JsonArgumentParser(argparse.ArgumentParser):
    """用法错也走 JSON 契约的 parser(stdout 恒单 JSON;usage 文本照旧进
    stderr 给人读,exit 2 与 §6 表一致)。"""

    def error(self, message: str) -> None:  # noqa: D401 - argparse 签名
        self.print_usage(sys.stderr)
        _emit({"error": {"code": "usage", "message": message}})
        raise SystemExit(EXIT_USAGE)


def build_parser() -> argparse.ArgumentParser:
    """§6 命令表(子命令形状零发挥;参数超纲即 usage 拒)。"""
    parser = JsonArgumentParser(
        prog="wechat-bridge",
        description="微信本机桥(UI 自动化 + 本地库只读;task 10-11-wechat-ui-bridge)",
    )
    parser.add_argument(
        "--version", action="version", version=f"wechat-bridge {_BRIDGE_VERSION}"
    )
    # §6 全表 JSON 应答;--json 为契约显式形态(缺省即 JSON,旗标收下不改变行为)。
    parser.add_argument(
        "--json",
        action="store_true",
        default=False,
        help="机器可读 JSON 应答(当前唯一输出形态,缺省即开;契约兼容旗标)",
    )
    parser.add_argument(
        "--probe",
        action="store_true",
        default=False,
        help='三态探针:{"ok","state","checks","wechat_version",…}(零成本,不读消息内容)',
    )
    parser.add_argument(
        "--config",
        default=None,
        metavar="PATH",
        help="桥配置文件覆写(缺省 <数据根>/wechat-bridge/config.json;缺文件可用)",
    )
    sub = parser.add_subparsers(dest="group", parser_class=JsonArgumentParser)

    sessions = sub.add_parser("sessions", help="UI 读通道(会话列表;Phase C1)")
    sessions_sub = sessions.add_subparsers(dest="sessions_cmd", required=True)
    sessions_list = sessions_sub.add_parser("list", help="列出前 N 个会话(名称+未读数)")
    sessions_list.add_argument(
        "-n", "--limit", type=int, default=None, help="条数覆写(缺省配置 limits.sessions=20)"
    )

    messages = sub.add_parser("messages", help="UI 读通道(消息;Phase C2)")
    messages_sub = messages.add_subparsers(dest="messages_cmd", required=True)
    messages_read = messages_sub.add_parser("read", help="读指定会话最近 K 条文本消息")
    messages_read.add_argument("chat_id", metavar="id", help="会话 id(sessions list 所得)")
    messages_read.add_argument(
        "-k", "--count", type=int, default=None, help="条数覆写(缺省配置 limits.messages=50)"
    )

    send = sub.add_parser("send_text", help="UI 写通道(Phase D;G6 硬频控)")
    send.add_argument("chat_id", metavar="id", help="目标会话 id")
    send.add_argument(
        "--file",
        required=True,
        metavar="PATH",
        help="正文来源;'-' = stdin(argv 永不携带正文,日志可安全打 argv)",
    )

    localdb_cmd = sub.add_parser("localdb", help="本地库只读通道(Phase E)")
    localdb_sub = localdb_cmd.add_subparsers(dest="localdb_cmd", required=True)
    localdb_query = localdb_sub.add_parser("query", help="指定会话最近 N 天文本消息(三域)")
    localdb_query.add_argument("chat_id", metavar="chat", help="目标会话 id")
    localdb_query.add_argument(
        "--since",
        required=True,
        metavar="Nd",
        help="历史窗口(天;形如 7d;窗口缺省参照配置 limits.history_days=30)",
    )

    # §6 文样把 --json 放在子命令之后(sessions list --json)——全局旗标在
    # argparse 里必须逐层重注册才收得到;default=SUPPRESS 防子层缺省覆写
    # 顶层已解析值(--config 同款,覆写路径跟在子命令后是合法调用位)。
    for node in (sessions, sessions_list, messages, messages_read, send, localdb_cmd, localdb_query):
        node.add_argument(
            "--json",
            action="store_true",
            default=argparse.SUPPRESS,
            help="机器可读 JSON 应答(契约兼容旗标;与顶层同名同义)",
        )
        node.add_argument(
            "--config",
            default=argparse.SUPPRESS,
            metavar="PATH",
            help="桥配置文件覆写(与顶层同名同义)",
        )

    return parser


def _emit(payload: dict[str, Any]) -> None:
    """stdout 单个 JSON 对象(键序稳定,golden 基件对账用)。"""
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")


def _read_body(file_spec: str) -> str:
    """send_text 正文读取(仅支持 '-';文件路径形态是 Phase D 的攻击面,
    骨架态直接拒——不给「看起来能用」的假象)。"""
    if file_spec != "-":
        raise BridgeError(
            EXIT_USAGE,
            f"send_text --file 仅支持 '-'(stdin);不接受文件路径: {file_spec!r}",
            code="usage",
            fix_hint="正文经 stdin 传入(weixin.py D0 同款;argv/文件路径都不携带正文)",
        )
    return sys.stdin.read()


def _parse_since_days(raw: str) -> int:
    """``--since Nd`` → 天数(严格形态;窗口是查询参数,不设上限截断)。"""
    value = raw.strip().lower()
    if not value.endswith("d") or not value[:-1].isdigit() or int(value[:-1]) <= 0:
        raise BridgeError(
            EXIT_USAGE,
            f"--since 须为 '<N>d' 形态且 N 为正整数(如 7d),当前为 {raw!r}",
            code="usage",
        )
    return int(value[:-1])


def _require_chat_id(chat_id: str) -> str:
    """会话 id 规整(去首尾空白;空白 id = usage 拒)。"""
    value = chat_id.strip()
    if not value:
        raise BridgeError(EXIT_USAGE, "会话 id 不可为空白", code="usage")
    return value


def _now() -> float:
    """时钟注入点(单测换假钟;独立函数避免 import time 散布)。"""
    import time

    return time.time()


def main(argv: Sequence[str] | None = None) -> int:
    """CLI 入口:返回 exit 码;stdout 恒 JSON,诊断走 stderr。"""
    parser = build_parser()
    args = parser.parse_args(argv)
    # --json/--config 可能落在任意层(SUPPRESS 缺省不覆写):统一归位。
    config_value = getattr(args, "config", None)

    # —— --probe:契约首个形态(与子命令互斥,防歧义)——
    if args.probe:
        if args.group is not None:
            parser.error("--probe 不与子命令并用(§6 契约:探针是独立调用形态)")
            raise AssertionError("parser.error 必抛 SystemExit")  # pragma: no cover
        try:
            config = load_config(
                Path(config_value).expanduser() if config_value else None
            )
        except BridgeError as exc:
            _emit({"error": exc.to_payload()})
            return exc.exit_code
        _emit(run_probe(config=config, bridge_version=_BRIDGE_VERSION).to_payload())
        # 探针本体跑成 = exit 0;三态在载荷里,消费方按 state 映射 UI(§6)。
        return EXIT_OK

    if args.group is None:
        parser.error("缺命令:--probe 或 sessions/messages/send_text/localdb 之一")
        raise AssertionError("parser.error 必抛 SystemExit")  # pragma: no cover

    try:
        config = load_config(Path(config_value).expanduser() if config_value else None)
        if args.group == "sessions" and args.sessions_cmd == "list":
            if args.limit is not None and args.limit <= 0:
                raise BridgeError(
                    EXIT_USAGE, f"--limit 须为正整数,当前为 {args.limit}", code="usage"
                )
            ax.ensure_ui_preconditions()
            ax.list_sessions(config, args.limit)  # Phase C1 落位;骨架态结构化拒
        elif args.group == "messages" and args.messages_cmd == "read":
            chat_id = _require_chat_id(args.chat_id)
            if args.count is not None and args.count <= 0:
                raise BridgeError(
                    EXIT_USAGE, f"-k 须为正整数,当前为 {args.count}", code="usage"
                )
            ax.ensure_ui_preconditions()
            ax.read_messages(config, chat_id, args.count)  # Phase C2 落位
        elif args.group == "send_text":
            chat_id = _require_chat_id(args.chat_id)
            body = _read_body(args.file)
            if not body.strip():
                raise BridgeError(
                    EXIT_USAGE, "正文为空(stdin 无内容);拒发空消息", code="usage"
                )
            ax.ensure_ui_preconditions()
            # G6 频控门:检查零副作用;真发送成功后由实现层 record_send 落
            # 时间戳(失败尝试不落,不吞重试窗口)。
            SendRateState().check_send_allowed(now=_now())
            ax.send_text(config, chat_id, body)  # Phase D1 落位
        elif args.group == "localdb" and args.localdb_cmd == "query":
            chat_id = _require_chat_id(args.chat_id)
            days = _parse_since_days(args.since)
            # 本地库通道不依赖 UI 前置(窗口未开不影响);失败族 = 20/21/22。
            storage = localdb.locate_db_storage()
            localdb.acquire_key(storage)  # Phase E1(D4)落位;骨架态 exit 21
            localdb.query_history(chat_id, days)  # Phase E2/E3 落位
        else:  # pragma: no cover - 子 parser required=True 已封住其余形态
            parser.error("未知子命令形态")
    except BridgeError as exc:
        _emit({"error": exc.to_payload()})
        return exc.exit_code
    # 实现层落地后各分支在此 emit §6 契约形状;骨架态 handler 恒 raise,
    # 走到这里 = 实现层提前返回(契约漂移),按通用失败如实报。
    raise BridgeError(  # pragma: no cover - 防实现层静默无应答
        EXIT_USAGE, "命令执行完成但无应答载荷(实现层契约漂移)", code="usage"
    )
