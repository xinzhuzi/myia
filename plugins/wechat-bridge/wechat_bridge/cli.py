"""桥 CLI(task 10-11-wechat-ui-bridge design §6;执行者零设计,照此实现)。

调用形态对齐 ``src/myssia/push/weixin.py`` 桥接 Hermes 惯例:一次性子进程、
``--json`` 机器可读应答、exit 三段语义(0 成功 / 1 通用失败 / 2 用法错,
失败段按 §6 细化码值)。**stdout 恒为单个 JSON 对象**(成功 = §6 各命令的
契约形状;失败 = ``{"error": {...}}``;argparse 用法错同样 JSON 化——
子类化 parser.error),人读诊断一律走 stderr——MYIA 侧只解析 stdout。

命令表(§6 原文 + 六域接线批 0.8.0 增补):

.. code-block:: text

    wechat-bridge --probe
    wechat-bridge sessions list --json
    wechat-bridge messages read <id> -k 50
    wechat-bridge send_text <id> --file -
    wechat-bridge localdb query <chat> --since 7d --json
    wechat-bridge localdb page <chat> --limit 500 [--cursor/--from-ts/--to-ts/--types/--sender/--asc]
    wechat-bridge localdb conversations [--limit 500]
    wechat-bridge localdb export <chat> --format json|txt|csv|md|html|xlsx --out <dir> [--all/--verify]
    wechat-bridge localdb stats chats|chat <chat>|annual|dual <chat> …
    wechat-bridge localdb media status|decrypt <dat>|scan <chat> --since Nd [--decrypt]
    wechat-bridge localdb media-decrypt set <path>|get|clear
    wechat-bridge localdb sns feed|notices|export --since Nd
    wechat-bridge localdb contacts [--type/--keyword/--limit/--cursor/--with-residue]
    wechat-bridge localdb notify-scan --file -
    wechat-bridge localdb revoke-list <chat> --since Nd
    wechat-bridge localdb serve [--host H] [--port P]
    wechat-bridge localdb http-token generate|show|clear

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

from . import (
    __version__,
    ax,
    contacts_query,
    httpapi,
    localdb,
    localdb_export,
    localdb_page,
    media,
    memsearch,
    notify_query,
    sendtarget,
    sns_export,
    stats_query,
)
from .codes import EXIT_GENERIC_FAILURE, EXIT_OK, EXIT_USAGE, BridgeError
from .config import BridgeConfig, load_config, save_config_key
from .probe import run_doctor, run_probe
from .send_state import SendRateState

__all__ = ["JsonArgumentParser", "build_parser", "main"]

_BRIDGE_VERSION = __version__


def _compact_body(text: str) -> str:
    """回执对账的空白不敏感形态(receipt_query 闭包用;委托
    :func:`.sendui.squash` = 单一对账形态出处,防近亲漂移)。"""
    from .sendui import squash

    return squash(text)


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
    send.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="走到粘贴回读不回车;零频控副作用可重跑(导航/哨兵/聚焦证据链实测面)",
    )

    # doctor(task 10-14-wechat-send-text design §E-2):--probe 超集 + send
    # 链就绪度(AX 门态/输入区能力);零前台扰动,状态查询恒 exit 0。
    doctor = sub.add_parser(
        "doctor",
        help="send 链就绪度探针(--probe 超集 + AX 门态;零前台扰动)",
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
    # 群信息只读查询(task 10-13-wechat-groupinfo;应答契约 v1 = 群显示名/
    # 群主/公告/状态/成员列表)。查询层缺表/缺域如实降级空结构恒 exit 0
    # (判例同 key-status:状态查询不判错);密钥链与 query/sns 同一全链。
    localdb_groupinfo = localdb_sub.add_parser(
        "group-info",
        help="群信息只读查询(群主/公告/成员;缺表降级恒 exit 0)",
    )
    localdb_groupinfo.add_argument(
        "chat_id", metavar="chat", help="目标群 id(@chatroom;sessions list 所得)"
    )
    # —— C1 分页/会话普查/导出(task 10-14-wechat-chat-export R1/R2/R4)——
    localdb_page_cmd = localdb_sub.add_parser(
        "page",
        help="指定会话 keyset 分页(游标续拉;时间窗/类型/发送者过滤)",
    )
    localdb_page_cmd.add_argument(
        "chat_id", metavar="chat", help="目标会话 id(wxid 或 @chatroom)"
    )
    localdb_page_cmd.add_argument(
        "--cursor", default=None, metavar="B64",
        help="续拉游标(上页应答 next_cursor;首发缺省)",
    )
    localdb_page_cmd.add_argument(
        "--limit", type=int, default=None, metavar="N",
        help="页大小:缺省 200,帽 1000",
    )
    page_order = localdb_page_cmd.add_mutually_exclusive_group()
    page_order.add_argument(
        "--asc", action="store_true", default=False, help="时间升序(旧在前;缺省 desc 最新在前)"
    )
    page_order.add_argument(
        "--desc", action="store_true", default=False, help="时间降序(缺省;显式给齐)"
    )
    localdb_page_cmd.add_argument(
        "--from-ts", default=None, metavar="TS",
        help="时间窗起点(unix 秒;毫秒/微秒自动归一)",
    )
    localdb_page_cmd.add_argument(
        "--to-ts", default=None, metavar="TS", help="时间窗终点(unix 秒)"
    )
    localdb_page_cmd.add_argument(
        "--types", default=None, metavar="A,B",
        help="类型过滤(逗号分隔:text/file/link/quote/…或 type_<N> 字面量)",
    )
    localdb_page_cmd.add_argument(
        "--sender", default=None, metavar="wxid", help="按解析前原始 wxid 精确匹配"
    )
    localdb_conversations = localdb_sub.add_parser(
        "conversations",
        help="会话清单普查(逐表 COUNT/MIN/MAX;按最近消息排序)",
    )
    localdb_conversations.add_argument(
        "--limit", type=int, default=None, metavar="N",
        help="清单截断条数:缺省 500,帽 5000",
    )
    localdb_export_cmd = localdb_sub.add_parser(
        "export",
        help="聊天记录导出(六格式 json|txt|csv|md|html|xlsx + manifest 对账)",
    )
    localdb_export_cmd.add_argument(
        "chat_id", metavar="chat", nargs="?", default=None,
        help="目标会话 id(--all 全量导出时可省)",
    )
    localdb_export_cmd.add_argument(
        "--format", required=True, metavar="F",
        help="导出格式:json|txt|csv|md|html|xlsx",
    )
    localdb_export_cmd.add_argument(
        "--out", required=True, metavar="DIR", help="导出目录(须已可建;staging 原子落位)"
    )
    localdb_export_cmd.add_argument(
        "--from-ts", default=None, metavar="TS", help="时间窗起点(unix 秒)"
    )
    localdb_export_cmd.add_argument(
        "--to-ts", default=None, metavar="TS", help="时间窗终点(unix 秒)"
    )
    localdb_export_cmd.add_argument(
        "--since", default=None, metavar="Nd",
        help="时间窗糖(近 N 天;与 --from-ts 互斥)",
    )
    localdb_export_cmd.add_argument(
        "--types", default=None, metavar="A,B", help="类型过滤(逗号分隔,同 page)"
    )
    localdb_export_cmd.add_argument(
        "--sender", default=None, metavar="wxid", help="按解析前原始 wxid 精确匹配"
    )
    localdb_export_cmd.add_argument(
        "--display-name-pref", default="remark-first", metavar="P",
        help="显示名优先序:remark-first|nickname-first(缺省 remark-first)",
    )
    localdb_export_cmd.add_argument(
        "--name-mode", default="classic", metavar="M",
        help="文件命名:classic|date-range(缺省 classic)",
    )
    localdb_export_cmd.add_argument(
        "--all", action="store_true", default=False,
        help="全量导出(逐会话各一文件;chat 可省)",
    )
    localdb_export_cmd.add_argument(
        "--verify", default=None, metavar="MANIFEST",
        help="对账子动作:校验既有 manifest(sha256 逐件),不导出",
    )
    # —— C2 统计四子命令(task 10-14-wechat-stats-reports;parser 本体在
    #    stats_query.register_cli,chats/chat/annual/dual 四形态)——
    stats_nodes = stats_query.register_cli(localdb_sub)
    # —— C3 媒体/朋友圈导出(task 10-14-wechat-media-sns)——
    localdb_mediadecrypt = localdb_sub.add_parser(
        "media-decrypt",
        help="媒体解密件管理(set|get|clear;协议 docs/wechat-mediadecrypt.md)",
    )
    mediadecrypt_sub = localdb_mediadecrypt.add_subparsers(
        dest="media_decrypt_cmd", required=True
    )
    mediadecrypt_set = mediadecrypt_sub.add_parser(
        "set", help="配置媒体解密件路径(校验文件存在且有可执行位)"
    )
    mediadecrypt_set.add_argument(
        "path", metavar="path", help="媒体解密件可执行文件路径(须绝对路径)"
    )
    mediadecrypt_get = mediadecrypt_sub.add_parser(
        "get", help="查看媒体解密件配置与在位状态"
    )
    mediadecrypt_clear = mediadecrypt_sub.add_parser(
        "clear", help="清除媒体解密件配置(媒体面回结构化降级)"
    )
    localdb_media = localdb_sub.add_parser(
        "media", help="媒体面(status=配置态 / decrypt=单件解密 / scan=会话寻径)"
    )
    media_sub = localdb_media.add_subparsers(dest="media_cmd", required=True)
    media_status_node = media_sub.add_parser(
        "status", help="解密件配置态 + 缓存统计(状态查询恒不判错)"
    )
    media_decrypt_node = media_sub.add_parser(
        "decrypt", help="单件 .dat 解密到媒体缓存(jpg/png/webp/gif/mp4)"
    )
    media_decrypt_node.add_argument(
        "dat_path", metavar="dat_path", help="待解密 .dat 文件绝对路径"
    )
    media_scan_node = media_sub.add_parser(
        "scan", help="会话媒体寻径(缩略图/正图;--decrypt 逐条解密回填)"
    )
    media_scan_node.add_argument(
        "chat_id", metavar="chat", help="目标会话 id(wxid 或 @chatroom)"
    )
    media_scan_node.add_argument(
        "--since", required=True, metavar="Nd", help="历史窗口(天;形如 30d)"
    )
    media_scan_node.add_argument(
        "--decrypt", action="store_true", default=False,
        help="逐条调解密件回填 cached_path(未配置 = exit 23)",
    )
    sns_export_node = sns_sub.add_parser(
        "export",
        help="朋友圈导出(json 载荷 / html 单件浏览;--with-media 下载媒体)",
    )
    sns_export_node.add_argument(
        "--format", default="json", choices=("json", "html"), metavar="F",
        help="导出格式:json|html(缺省 json)",
    )
    sns_export_node.add_argument(
        "--out", default=None, metavar="DIR", help="导出目录(缺省数据根私有区)"
    )
    sns_export_node.add_argument(
        "--since", required=True, metavar="Nd", help="历史窗口(天;形如 30d)"
    )
    sns_export_node.add_argument(
        "--with-media", action="store_true", default=False,
        help="下载媒体原件(唯一受限 CDN GET 豁免;docs/wechat-mediadecrypt.md §11)",
    )
    # —— C4 联系人六桶(task 10-14-wechat-contacts;group-info 判例同族)——
    localdb_contacts = localdb_sub.add_parser(
        "contacts",
        help="联系人分类浏览/找回考古(friend|group|official|former|other;缺表降级恒 exit 0)",
    )
    localdb_contacts.add_argument(
        "--type", dest="type_filter", default=None, metavar="T",
        help="六桶过滤:friend|group|official|former|other(缺省全量分桶浏览)",
    )
    localdb_contacts.add_argument(
        "--keyword", default=None, metavar="K", help="显示名/备注/别名模糊过滤"
    )
    localdb_contacts.add_argument(
        "--limit", type=int, default=None, metavar="N",
        help="页大小:缺省 100,上帽 1000;0 = 全量导出态(帽豁免,has_more 恒 false)",
    )
    localdb_contacts.add_argument(
        "--cursor", default=None, metavar="B64", help="续拉游标(上页 next_cursor)"
    )
    localdb_contacts.add_argument(
        "--with-residue", action="store_true", default=False,
        help="找回考古:message 域残迹交叉(首跑触发消息域副本首建)",
    )
    localdb_contacts.add_argument(
        "--include-stranger", action="store_true", default=True,
        help="包含陌生人桶(缺省开;PRD R2「缺省开」)",
    )
    # —— C5 通知扫描/撤回历史(task 10-14-wechat-notify-revoke)——
    localdb_notifyscan = localdb_sub.add_parser(
        "notify-scan",
        help="轮询水位通知扫描+撤回检测/恢复阶梯(stdin JSON 载荷,argv 零内容)",
    )
    localdb_notifyscan.add_argument(
        "--file", required=True, metavar="PATH",
        help="载荷来源;仅支持 '-'(stdin;argv 永不携带白名单内容)",
    )
    localdb_revokelist = localdb_sub.add_parser(
        "revoke-list", help="会话撤回历史(--since Nd 窗口;同一恢复阶梯)"
    )
    localdb_revokelist.add_argument(
        "chat_id", metavar="chat", help="目标会话 id(wxid 或 @chatroom)"
    )
    localdb_revokelist.add_argument(
        "--since", required=True, metavar="Nd", help="历史窗口(天;形如 7d)"
    )
    # —— C6 本机 HTTP API(task 10-14-wechat-http-api;key-provider 族形态)——
    localdb_serve = localdb_sub.add_parser(
        "serve",
        help="本机 HTTP API 常驻服务(回环强制+token;协议 docs/wechat-http-api.md)",
    )
    localdb_serve.add_argument(
        "--host", default=None, metavar="H", help="绑定地址(缺省配置 http_api_host;回环强制)"
    )
    localdb_serve.add_argument(
        "--port", type=int, default=None, metavar="P", help="端口(缺省配置 http_api_port)"
    )
    localdb_httptoken = localdb_sub.add_parser(
        "http-token", help="HTTP token 管理(generate|show|clear;轮换热生效)"
    )
    httptoken_sub = localdb_httptoken.add_subparsers(dest="http_token_cmd", required=True)
    httptoken_generate = httptoken_sub.add_parser("generate", help="生成并落盘新 token(轮换热生效)")
    httptoken_show = httptoken_sub.add_parser("show", help="查看 token 配置态(只呈形状不呈值)")
    httptoken_clear = httptoken_sub.add_parser("clear", help="吊销 token(回未配置=全拒)")

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
        sns_export_node,
        localdb_groupinfo,
        localdb_page_cmd,
        localdb_conversations,
        localdb_export_cmd,
        localdb_mediadecrypt,
        mediadecrypt_set,
        mediadecrypt_get,
        mediadecrypt_clear,
        localdb_media,
        media_status_node,
        media_decrypt_node,
        media_scan_node,
        localdb_contacts,
        localdb_notifyscan,
        localdb_revokelist,
        localdb_serve,
        localdb_httptoken,
        httptoken_generate,
        httptoken_show,
        httptoken_clear,
        doctor,
        *stats_nodes,
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
            dry_run = bool(getattr(args, "dry_run", False))
            branch_started = _now()
            # 三源合体序列(task 10-14-wechat-send-text design §1):
            # 2) localdb 链**单次**解析(取钥器交互/自愈链全程至多一次,
            #    §J-19)——storage/keys 注入 resolve_target 与 receipt 闭包。
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            # 3) DB 侧目标解析(红线 2 第一验:三形态 id → username 真源;
            #    查无/多义在零 UI 扰动下拒发——此时未激活未占位)。
            target = sendtarget.resolve_target(
                config, chat_id, storage=storage, keys=keys
            )
            if target is None:
                raise BridgeError(
                    EXIT_GENERIC_FAILURE,
                    f"DB 侧未解析到目标(chat_id={chat_id},username/alias/展示名三路均无)",
                    code="send_target_not_found",
                    fix_hint="确认 id;用 localdb query 先验目标存在",
                )
            key = sendtarget.fingerprint(target, body)
            # 4) UI 前置门(码序 10 → 11(screen) → 12,不变;dry-run 同过
            #    ——它要驱动 UI,微信不在/窗口关/权限缺都无从演练)。
            ax.ensure_ui_preconditions()
            rate_state = SendRateState()
            now: float | None = None
            previous: float | None = None
            if not dry_run:
                # 5) G6+防重合成占位:同一 flock 临界区,**指纹门在前、
                #    间隔门在后**(幂等命中不该被间隔拦;§J-5)。BridgeError
                #    = 契约内失败(未发出)→ rollback_reserve 还原占位(失败
                #    不吞重试窗口);armed(on_armed 已成功)之后的失败绝不
                #    rollback(指纹 pending 在档,uncertain-never-retry)。
                now = _now()
                outcome = rate_state.reserve_send_dedup(now=now, fingerprint=key)
                previous = outcome.previous
                if outcome.dedup == "sent_recently":
                    _emit(
                        {
                            "send": {
                                "chat": chat_id,
                                "target": {
                                    "username": target.username,
                                    "display_name": target.display_name,
                                },
                                "sent": False,
                                "deduped": True,
                                "dedup_status": "sent_recently",
                                "elapsed_ms": round((_now() - branch_started) * 1000),
                            }
                        }
                    )
                    return EXIT_OK
            else:
                # --dry-run 跳过频控与防重(零发送零占位零指纹,可无限重跑)。
                pass
            armed = {"v": False}

            def _on_armed() -> None:
                # on_armed = fail-closed 门(design §C-5):先落 pending 再置
                # armed 标志——落盘失败 → armed 仍 False → CLI rollback 可
                # 安全重试;成功后置位,此后失败不再 rollback(§C-4)。
                rate_state.mark_fingerprint_pending(key, now=_now())
                armed["v"] = True

            def _on_receipt_green() -> None:
                rate_state.mark_fingerprint_sent(key, now=_now())

            def receipt_query(
                username: str, body_text: str, since_epoch: float
            ) -> bool | None:
                """localdb 回执终验闭包(红线 4;design §C-6)。

                判定 = ``query_history(username, since 1d)`` 的 messages 中
                存在(text 空白不敏感对账命中 body)AND(int(ts) >
                since_epoch - 2)——ts 已归一秒(localdb_query.
                _normalize_ts),容差 2s 防同正文历史消息假绿(§J-8)。
                localdb 链 BridgeError → None(如实,不算失败也不算成功)。
                """
                try:
                    result = localdb.query_history(
                        config, storage, keys, username, 1
                    )
                except BridgeError:
                    return None
                messages = result.get("messages") if isinstance(result, dict) else None
                if not isinstance(messages, list):
                    return None
                want = _compact_body(body_text)
                for message in messages:
                    if not isinstance(message, dict):
                        continue
                    text = message.get("text")
                    if not isinstance(text, str):
                        continue
                    if _compact_body(text) != want:
                        continue
                    ts = message.get("ts")
                    if (
                        isinstance(ts, (int, float))
                        and not isinstance(ts, bool)
                        and int(ts) > since_epoch - 2
                    ):
                        return True
                return False

            try:
                payload = ax.send_text(
                    config,
                    target,
                    body,
                    dry_run=dry_run,
                    on_armed=None if dry_run else _on_armed,
                    on_receipt_green=_on_receipt_green,
                    receipt_query=receipt_query,
                )
            except BridgeError:
                # rollback 边界 = on_armed 之前(armed 闭包标志判;§C-5)。
                if not dry_run and not armed["v"]:
                    rate_state.rollback_reserve(now, previous)
                raise
            payload.setdefault("send", {})["chat"] = chat_id
            _emit(payload)
            return EXIT_OK
        elif args.group == "doctor":
            # 状态查询不判错(key-status 判例,design §E-2):恒 exit 0,
            # 三态在载荷(ax_gate.state: open|closed|unknown)。
            _emit(run_doctor(config=config, bridge_version=_BRIDGE_VERSION))
            return EXIT_OK
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
        elif args.group == "localdb" and args.localdb_cmd == "sns" and args.sns_cmd in ("feed", "notices"):
            # 朋友圈只读查询(10-13-wechat-sns-feed):密钥链与 query 同一
            # 全链(resolve_keys:缓存/取钥器/自愈/E1);E2 副本域固定
            # sns+contact(nickname 反查),不带消息域;成功 emit 契约载荷
            # (朋友圈内容属 stdout 契约,不入日志;红线 6 同款)。export
            # 子模式归 C3 sns_export(下方分支)。
            days = _parse_since_days(args.since)
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(localdb.sns_history(config, storage, keys, args.sns_cmd, days))
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "group-info":
            # 群信息只读查询(10-13-wechat-groupinfo):密钥链与 query/sns
            # 同一全链(resolve_keys);E2 副本域固定 contact 单域(成员
            # member_id 即 contact rowid,零消息域解密成本)。查询层缺表/
            # 缺域如实降级空结构恒 exit 0(判例同 key-status);成功 emit
            # 契约 v1 载荷(群数据属 stdout 契约,不入日志;红线 6 同款)。
            chat_id = _require_chat_id(args.chat_id)
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(localdb.group_info(config, storage, keys, chat_id))
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "page":
            # C1 分页查询(10-14-wechat-chat-export R1):密钥链与 query 同一
            # 全链;时间戳经 normalize_ts_input 归一(秒/毫秒/微秒);游标
            # scope 守卫与类型词表校验在 run_page/decode_cursor/
            # type_filter_values(invalid_cursor/invalid_types → exit 2)。
            chat_id = _require_chat_id(args.chat_id)
            from_ts = localdb_page.normalize_ts_input(args.from_ts, flag="from-ts")
            to_ts = localdb_page.normalize_ts_input(args.to_ts, flag="to-ts")
            types = (
                [t.strip() for t in args.types.split(",") if t.strip()]
                if args.types
                else None
            )
            asc: bool | None = True if args.asc else (False if args.desc else None)
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(
                localdb.page_history(
                    config,
                    storage,
                    keys,
                    chat_id,
                    cursor=args.cursor,
                    limit=args.limit,
                    asc=asc,
                    from_ts=from_ts,
                    to_ts=to_ts,
                    types=types,
                    sender=args.sender,
                )
            )
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "conversations":
            # C1 会话普查(R2):密钥链同 query;消息域副本普查(逐表
            # COUNT/MIN/MAX,副本指纹缓存),清单缺省 500/帽 5000 在桥侧。
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(
                localdb.conversations_census(
                    config, storage, keys, limit=args.limit
                )
            )
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "export":
            # C1 导出(R4):stdout 是 NDJSON 流(progress 行经 run_export
            # 的单行 JSON 打印器原样转印;终态/错误 _emit_ndjson_line 单行
            # 收尾——key-acquire 判例)。--verify 子动作走对账不导出。
            if args.verify is not None:
                _emit(
                    localdb_export.verify_manifest(
                        Path(args.verify.strip()).expanduser()
                    )
                )
                return EXIT_OK
            if args.since is not None and (args.from_ts is not None or args.to_ts is not None):
                raise BridgeError(
                    EXIT_USAGE,
                    "--since 与 --from-ts/--to-ts 互斥(时间窗只给一份)",
                    code="usage",
                )
            from_ts = localdb_page.normalize_ts_input(args.from_ts, flag="from-ts")
            to_ts = localdb_page.normalize_ts_input(args.to_ts, flag="to-ts")
            if args.since is not None:
                from_ts = int(_now()) - _parse_since_days(args.since) * 86400
            types = (
                [t.strip() for t in args.types.split(",") if t.strip()]
                if args.types
                else None
            )
            chat_id = (args.chat_id or "").strip() or None
            if not args.all and not chat_id:
                raise BridgeError(
                    EXIT_USAGE,
                    "单会话导出必须给 chat(或 --all 全量导出)",
                    code="usage",
                )
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            try:
                payload = localdb.export_history(
                    config,
                    storage,
                    keys,
                    chat_id,
                    fmt=args.format,
                    out_dir=Path(args.out.strip()).expanduser(),
                    from_ts=from_ts,
                    to_ts=to_ts,
                    types=types,
                    sender=args.sender,
                    display_name_pref=args.display_name_pref,
                    name_mode=args.name_mode,
                    all_chats=bool(args.all),
                    progress=_emit_ndjson_line,
                )
                exit_code = EXIT_OK
            except BridgeError as exc:
                payload = {"error": exc.to_payload()}
                exit_code = exc.exit_code
            _emit_ndjson_line(payload)
            return exit_code
        elif args.group == "localdb" and args.localdb_cmd == "stats":
            # C2 统计四子命令(10-14-wechat-stats-reports):dispatch_cli 自带
            # JSON emit 与 BridgeError 兜底;exit 码契约 = 查询层降级恒 0,
            # 密钥链 20/21/22,用法 2。
            return stats_query.dispatch_cli(args, config_path)
        elif args.group == "localdb" and args.localdb_cmd == "media-decrypt":
            # C3 媒体解密件管理(key-provider set 判例:绝对路径/存在/可执行
            # 校验;get 状态查询恒不判错;clear 回未配置)。
            if args.media_decrypt_cmd == "set":
                provider = Path(args.path.strip()).expanduser()
                if not provider.is_absolute():
                    raise BridgeError(
                        EXIT_USAGE,
                        f"媒体解密件路径必须是绝对路径: {provider}",
                        code="usage",
                        fix_hint="给出绝对路径(~ 开头会自动展开)",
                    )
                if not provider.is_file():
                    raise BridgeError(
                        EXIT_USAGE,
                        f"媒体解密件文件不存在: {provider}",
                        code="usage",
                        fix_hint="给出解密件可执行文件的路径(协议:docs/wechat-mediadecrypt.md)",
                    )
                if not os.access(provider, os.X_OK):
                    raise BridgeError(
                        EXIT_USAGE,
                        f"媒体解密件文件不可执行(缺可执行位): {provider}",
                        code="usage",
                        fix_hint="chmod +x 后重试",
                    )
                save_config_key("media_decrypt_path", str(provider), path=config_path)
                _emit(
                    {
                        "media_decrypt": {
                            "path": str(provider),
                            "state": "configured",
                            "message": f"已配置媒体解密件: {provider}",
                        }
                    }
                )
                return EXIT_OK
            if args.media_decrypt_cmd == "get":
                _emit(media.media_status(config))
                return EXIT_OK
            # clear(分支封闭:media_decrypt_cmd required=True 三选一)
            save_config_key("media_decrypt_path", None, path=config_path)
            _emit(
                {
                    "media_decrypt": {
                        "path": None,
                        "state": "unconfigured",
                        "message": "已清除媒体解密件配置(媒体面回结构化降级:exit 23)",
                    }
                }
            )
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "media":
            # C3 媒体面:status=配置态查询恒不判错;decrypt=单件解密;
            # scan=寻径(密钥链与 query 同序,域固定 message)。
            if args.media_cmd == "status":
                _emit(media.media_status(config))
                return EXIT_OK
            if args.media_cmd == "decrypt":
                dat_path = args.dat_path.strip()
                if not dat_path:
                    raise BridgeError(
                        EXIT_USAGE, "dat_path 不可为空白", code="usage"
                    )
                _emit(media.media_decrypt_command(dat_path, config))
                return EXIT_OK
            # scan(分支封闭:media_cmd required=True 三选一)
            chat_id = _require_chat_id(args.chat_id)
            days = _parse_since_days(args.since)
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(
                media.media_scan_history(
                    config, storage, keys, chat_id, days, decrypt=bool(args.decrypt)
                )
            )
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "sns" and args.sns_cmd == "export":
            # C3 朋友圈导出(域 sns+contact 同 feed;--with-media = 唯一受限
            # CDN GET 豁免,缺省关——docs/wechat-mediadecrypt.md §11)。
            days = _parse_since_days(args.since)
            fmt = args.format or "json"
            out_dir = Path(args.out.strip()).expanduser() if args.out else None
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(
                sns_export.sns_export_history(
                    config,
                    storage,
                    keys,
                    fmt,
                    out_dir,
                    days,
                    with_media=bool(args.with_media),
                )
            )
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "contacts":
            # C4 联系人六桶(10-14-wechat-contacts):密钥链同 query;limit
            # 三态(缺省 100/0=全量/帽 1000)与 --type 五桶校验都在密钥链
            # 之前(用法错先炸,不混 21);缺表降级恒 exit 0(判例
            # key-status)。
            limit = contacts_query.normalize_cli_limit(args.limit)
            contacts_query._norm_filter(args.type_filter, args.keyword)
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(
                localdb.contacts_inventory(
                    config,
                    storage,
                    keys,
                    type_filter=args.type_filter,
                    keyword=args.keyword,
                    limit=limit,
                    cursor=args.cursor,
                    with_residue=bool(args.with_residue),
                    include_stranger=bool(args.include_stranger),
                )
            )
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "notify-scan":
            # C5 轮询水位通知扫描(10-14-wechat-notify-revoke):stdin JSON
            # 载荷(argv 零内容,红线 6);notify_query 属性调用形态(gated
            # 桩生效点);sqlite busy 本轮跳过不判死(载荷内 stats)。
            if args.file != "-":
                raise BridgeError(
                    EXIT_USAGE,
                    f"notify-scan --file 仅支持 '-'(stdin 载荷),当前为 {args.file!r}",
                    code="usage",
                    fix_hint="白名单/水位等载荷经 stdin 传入(argv 永不携带内容)",
                )
            payload = notify_query.read_scan_payload(sys.stdin.read())
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(notify_query.notify_scan(config, storage, keys, payload))
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "revoke-list":
            # C5 会话撤回历史:同一恢复阶梯(notify_scan 的 R1.3 阶梯两壳)。
            chat_id = _require_chat_id(args.chat_id)
            days = _parse_since_days(args.since)
            storage = localdb.locate_db_storage()
            keys = localdb.resolve_keys(storage, config=config)
            _emit(notify_query.revoke_list(config, storage, keys, chat_id, days))
            return EXIT_OK
        elif args.group == "localdb" and args.localdb_cmd == "serve":
            # C6 本机 HTTP API 常驻(10-14-wechat-http-api R4):serve 自管
            # stdout(就绪单行 JSON/错误 JSON)与 SIGTERM/exit 码,勿再包
            # _emit;回环强制在 serve 面(exit 2)。
            return httpapi.run_serve(
                config_path=config_path, host=args.host, port=args.port
            )
        elif args.group == "localdb" and args.localdb_cmd == "http-token":
            # C6 token 管理(key-provider 族形态:generate=secrets 轮换热
            # 生效,show=状态查询恒 exit 0,clear=吊销)。
            if args.http_token_cmd == "generate":
                _emit(httpapi.http_token_generate(config_path=config_path))
                return EXIT_OK
            if args.http_token_cmd == "show":
                _emit(httpapi.http_token_show(config_path=config_path))
                return EXIT_OK
            # clear(分支封闭:http_token_cmd required=True 三选一)
            _emit(httpapi.http_token_clear(config_path=config_path))
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
