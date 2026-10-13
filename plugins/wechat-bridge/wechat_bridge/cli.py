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
import os
import sys
from pathlib import Path
from typing import Any, Sequence

from . import __version__, ax, localdb, memsearch
from .codes import EXIT_OK, EXIT_USAGE, BridgeError
from .config import BridgeConfig, load_config, save_config_key
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
    # D4 豁免执行件(主人 2026-10-11「全部解决」令):内存密钥批处理扫描。
    # 默认关(配置 mem_search_enabled 显式开启)+ 须提权;只读单遍零常驻,
    # 机制与边界见 memsearch 模块 docstring。
    localdb_key_scan = localdb_sub.add_parser(
        "key-scan", help="内存密钥批处理扫描(D4 豁免;默认关+须提权;只读单遍零常驻)"
    )
    # 外部取钥器管理(B2,task 10-13-wechat-keyprovider;协议 =
    # docs/wechat-keyprovider.md)。设置页与 CLI 的唯一配置通道(壳层不直写
    # 桥 config.json);set 校验存在+可执行,其余状态查询不判错。
    localdb_keyprov = localdb_sub.add_parser(
        "key-provider",
        help="外部取钥器管理(set|get|clear;协议 docs/wechat-keyprovider.md)",
    )
    keyprov_sub = localdb_keyprov.add_subparsers(dest="key_provider_cmd", required=True)
    keyprov_set = keyprov_sub.add_parser(
        "set", help="配置取钥器路径(校验文件存在且有可执行位)"
    )
    keyprov_set.add_argument(
        "path", metavar="path", help="取钥器可执行文件路径(脚本须带 shebang)"
    )
    keyprov_get = keyprov_sub.add_parser("get", help="查看取钥器配置与在位状态")
    keyprov_clear = keyprov_sub.add_parser("clear", help="清除取钥器配置(回未配置现状)")
    # 密钥状态/交互式取钥(task 10-13-wechat-monitor-ui D2/D3;协议 v1.1 =
    # docs/wechat-keyprovider.md §12)。key-status 三态查询恒 exit 0(缺文件
    # = missing 也是正常态);key-acquire = ready 短路/--force 直走取钥器/
    # hint clamp(120,1800)/progress 原样转印 stdout(NDJSON 流)。
    localdb_keystatus = localdb_sub.add_parser(
        "key-status",
        help="密钥缓存三态查询(ready/stale/missing;抽样页1 HMAC 重验;恒 exit 0)",
    )
    localdb_keyacquire = localdb_sub.add_parser(
        "key-acquire",
        help="交互式取钥编排(ready 短路 already_ready;--force 直走取钥器;progress 转印)",
    )
    localdb_keyacquire.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="跳过 already_ready 短路直走取钥器(「重新获取」场景:缓存 ready 也要真取)",
    )
    localdb_keyacquire.add_argument(
        "--timeout-hint",
        type=int,
        default=600,
        metavar="N",
        help="取钥器等待窗提示秒数(透传 timeout_hint_seconds;桥内硬帽 clamp(N,120,1800))",
    )
    # 朋友圈只读查询(task 10-13-wechat-sns-feed;key-provider 多层子命令同款
    # 形态)。feed=SnsTimeLine 动态(XML 解析)/notices=SnsMessage_tmp3 互动
    # 通知(赞/评);两模式都不跑 UI 前置(localdb 族同纪律,零截窗零 AX)。
    localdb_sns = localdb_sub.add_parser(
        "sns", help="朋友圈只读查询(feed=动态 / notices=互动通知)"
    )
    sns_sub = localdb_sns.add_subparsers(dest="sns_cmd", required=True)
    sns_feed = sns_sub.add_parser(
        "feed", help="朋友圈动态(SnsTimeLine;content XML 解析,窗口过滤在解析后)"
    )
    sns_notices = sns_sub.add_parser(
        "notices", help="朋友圈互动通知(赞/评;窗口过滤在 SQL)"
    )
    for sns_node in (sns_feed, sns_notices):
        sns_node.add_argument(
            "--since",
            required=True,
            metavar="Nd",
            help="历史窗口(天;形如 3d;窗口含当天,水位增量由调用方管)",
        )

    # §6 文样把 --json 放在子命令之后(sessions list --json)——全局旗标在
    # argparse 里必须逐层重注册才收得到;default=SUPPRESS 防子层缺省覆写
    # 顶层已解析值(--config 同款,覆写路径跟在子命令后是合法调用位)。
    for node in (
        sessions,
        sessions_list,
        messages,
        messages_read,
        send,
        localdb_cmd,
        localdb_query,
        localdb_key_scan,
        localdb_keyprov,
        keyprov_set,
        keyprov_get,
        keyprov_clear,
        localdb_keystatus,
        localdb_keyacquire,
        localdb_sns,
        sns_feed,
        sns_notices,
    ):
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


def _emit_ndjson_line(payload: dict[str, Any]) -> None:
    """NDJSON 流终态行(key-acquire 专属:progress 转印行已是单行 JSON,
    终态/错误同形单行收尾——整条 stdout 流逐行可解析,壳侧逐行读转事件;
    ``_emit`` 的缩进多行形态会破流,不用于此)。"""
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
    sys.stdout.flush()


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
        config_path = Path(config_value).expanduser() if config_value else None
        config = load_config(config_path)
        if args.group == "sessions" and args.sessions_cmd == "list":
            if args.limit is not None and args.limit <= 0:
                raise BridgeError(
                    EXIT_USAGE, f"--limit 须为正整数,当前为 {args.limit}", code="usage"
                )
            ax.ensure_ui_preconditions()
            _emit(ax.list_sessions(config, args.limit))  # Phase C1:像素链(§6 契约+诊断附加键)
            return EXIT_OK
        elif args.group == "messages" and args.messages_cmd == "read":
            chat_id = _require_chat_id(args.chat_id)
            if args.count is not None and args.count <= 0:
                raise BridgeError(
                    EXIT_USAGE, f"-k 须为正整数,当前为 {args.count}", code="usage"
                )
            ax.ensure_ui_preconditions()
            _emit(ax.read_messages(config, chat_id, args.count))  # Phase C2:像素链
            return EXIT_OK
        elif args.group == "send_text":
            chat_id = _require_chat_id(args.chat_id)
            body = _read_body(args.file)
            if not body.strip():
                raise BridgeError(
                    EXIT_USAGE, "正文为空(stdin 无内容);拒发空消息", code="usage"
                )
            ax.ensure_ui_preconditions()
            # G6 频控门(并发封闭):「检查+占位」同一 flock 临界区——并发
            # 两个 send_text 子进程只有一个能过检占位(红线 ≥10s 硬间隔在
            # 并发下成立,两段式 check/record 的 TOCTOU 缝不进发送路径)。
            # BridgeError = 契约内失败(未发出)→ rollback_reserve 还原占位
            # (失败不吞重试窗口);非契约异常不还原——宁可多吃 10s 窗口,
            # 不冒「已发出却放开第二发」的二次发送风险(红线方向)。
            rate_state = SendRateState()
            now = _now()
            previous = rate_state.reserve_send(now=now)
            try:
                ax.send_text(config, chat_id, body)  # Phase D1 落位
            except BridgeError:
                rate_state.rollback_reserve(now, previous)
                raise
        elif args.group == "localdb" and args.localdb_cmd == "query":
            chat_id = _require_chat_id(args.chat_id)
            days = _parse_since_days(args.since)
            # 本地库通道不依赖 UI 前置(窗口未开不影响);失败族 = 20/21/22。
            # 密钥解析(D4 裁决②消费通路):keys.json(缓存/外部同位)逐条
            # 重验 → 全量命中即放行;未闭合且自愈在位(mem_search_enabled
            # + setuid keyscanner,0.4.0)→ 零人工重取;再回落 E1 零内存
            # 途径(exit 21 = D4 语义如实)→ E2 副本 → E3 三域查询;成功
            # 在此 emit 契约载荷(消息内容属 stdout 契约,不入日志;红线 6)。
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(localdb.query_history(config, storage, keys, chat_id, days))
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "key-scan":
            # D4 豁免执行件(2026-10-11「全部解决」令):内存密钥批处理扫描。
            # 三重门在 memsearch.acquire_key_from_memory 内逐门校验(配置/
            # 提权/平台);只读单遍零常驻,命中全量验证才落 keys.json(600),
            # 消息/载荷只承载形状(红线 6);拒绝与零命中如实 exit 21。
            storage = localdb.locate_db_storage()
            _emit(memsearch.acquire_key_from_memory(storage, config=config))
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "key-provider":
            # 外部取钥器管理(B2;协议 docs/wechat-keyprovider.md §10)。
            # set 阶段校验存在+可执行+绝对路径(文件不可执行/相对路径在这里
            # 拒——协议 §8;相对路径落盘后随桥 cwd 漂移,spawn 面不可靠);
            # get 是状态查询恒 exit 0(未配置/文件缺失如实呈态,不判错)。
            if args.key_provider_cmd == "set":
                provider = Path(args.path.strip()).expanduser()
                if not provider.is_absolute():
                    raise BridgeError(
                        EXIT_USAGE,
                        f"取钥器路径必须是绝对路径: {provider}",
                        code="usage",
                        fix_hint="给出绝对路径(~ 开头会自动展开),如 /Users/you/bin/my-keyprovider",
                    )
                if not provider.is_file():
                    raise BridgeError(
                        EXIT_USAGE,
                        f"取钥器文件不存在: {provider}",
                        code="usage",
                        fix_hint="给出取钥器可执行文件的路径;脚本须带 shebang(如 #!/usr/bin/env python3)并有可执行位",
                    )
                if not os.access(provider, os.X_OK):
                    raise BridgeError(
                        EXIT_USAGE,
                        f"取钥器文件不可执行(缺可执行位): {provider}",
                        code="usage",
                        fix_hint="chmod +x 后重试;脚本还须带 shebang(协议 v1:可直接执行的可执行文件)",
                    )
                save_config_key(
                    "key_provider_path", str(provider), path=config_path
                )
                _emit(
                    {
                        "key_provider": {
                            "path": str(provider),
                            "state": "configured",
                            "message": f"已配置外部取钥器: {provider}",
                        }
                    }
                )
                return EXIT_OK
            if args.key_provider_cmd == "get":
                configured = (config.key_provider_path or "").strip()
                if not configured:
                    state, message = (
                        "unconfigured",
                        "未配置外部取钥器;localdb key-provider set <path> 配置(协议:docs/wechat-keyprovider.md)",
                    )
                else:
                    provider = Path(configured).expanduser()
                    if not provider.is_file():
                        state, message = (
                            "missing_file",
                            f"已配置但文件不存在: {provider}",
                        )
                    elif not os.access(provider, os.X_OK):
                        state, message = (
                            "not_executable",
                            f"已配置但文件缺可执行位: {provider}",
                        )
                    else:
                        state, message = (
                            "configured",
                            f"外部取钥器已配置: {provider}",
                        )
                _emit(
                    {
                        "key_provider": {
                            "path": configured or None,
                            "state": state,
                            "message": message,
                        }
                    }
                )
                return EXIT_OK
            # clear(分支封闭:key_provider_cmd required=True 三选一)
            save_config_key("key_provider_path", None, path=config_path)
            _emit(
                {
                    "key_provider": {
                        "path": None,
                        "state": "unconfigured",
                        "message": "已清除外部取钥器配置(查询链恢复现状:不 spawn 取钥器)",
                    }
                }
            )
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "key-status":
            # D2 三态真源(design §A.1):恒 exit 0——三态即正常态,缺文件 =
            # missing 不判错;抽样重验在 key_status 内(与 keys.json 消费门
            # 同一验真器,不另写一份)。
            _emit(localdb.key_status())
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "sns":
            # 朋友圈只读查询(10-13-wechat-sns-feed):密钥链与 query 同一
            # 全链(resolve_keys:缓存/取钥器/自愈/E1);E2 副本域固定
            # sns+contact(nickname 反查),不带消息域;成功 emit 契约载荷
            # (朋友圈内容属 stdout 契约,不入日志;红线 6 同款)。
            days = _parse_since_days(args.since)
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(localdb.sns_history(config, storage, keys, args.sns_cmd, days))
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "key-acquire":
            # D3 交互式取钥编排(design §A.2):stdout 是 NDJSON 流——progress
            # 行由 key_acquire 原样转印(已逐行落 stdout,终态前合法行序),
            # 终态/错误由本分支单行 JSON 收尾;错误不走通用 _emit 缩进形态
            # (多行 JSON 在逐行流里不可解析)。取消联动 = SIGTERM → kill
            # provider 进程组 + SystemExit(143)(localdb 内装)。
            try:
                payload = localdb.key_acquire(
                    config=config,
                    force=args.force,
                    timeout_hint=args.timeout_hint,
                )
                exit_code = EXIT_OK
            except BridgeError as exc:
                payload = {"error": exc.to_payload()}
                exit_code = exc.exit_code
            _emit_ndjson_line(payload)
            return exit_code
        else:  # pragma: no cover - 子 parser required=True 已封住其余形态
            parser.error("未知子命令形态")
    except BridgeError as exc:
        _emit({"error": exc.to_payload()})
        return exc.exit_code
    # 实现层落地后各分支在此 emit §6 契约形状;UI 读/写通道尚未落地
    # (Phase C/D),handler 恒 raise;localdb query 已emit 后提前 return。
    raise BridgeError(  # pragma: no cover - 防实现层静默无应答
        EXIT_USAGE, "命令执行完成但无应答载荷(实现层契约漂移)", code="usage"
    )
