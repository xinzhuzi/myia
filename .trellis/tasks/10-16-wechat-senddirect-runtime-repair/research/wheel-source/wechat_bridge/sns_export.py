"""朋友圈只读导出(task 10-14-wechat-media-sns R3/R4)。

``localdb sns export --format json|html --out <dir> [--since Nd] [--with-media]``:

- **JSON** = ``entries[]``(复用 sns_query 既有解析惯例 + nickname 反查)+ 每条
  媒体全量字段(type/cdn_url/md5/key/尺寸/状态词面)+ 评论区关联
  (``SnsMessage_tmp3.feed_id`` ↔ 条目 id;关联率如实入 ``stats``,未关联
  notices 单独成节,不强求 100%)。
- **HTML** = 单文件自包含正文 + ``files/`` 目录相对引用媒体;媒体状态人话
  占位,**禁 base64 内嵌**(346MB 级消息库教训:防单文件爆炸)。
- 导出产物落 ``--out``(缺省 = 数据根私有区 ``wechat-localdb/exports/
  sns-<时间戳>/``),文件 600/目录 700。

R4 朋友圈媒体回源(**缺省关**;帖级唯一路径——本地缓存与帖映射实测不存在):

- ``--with-media`` 开 = 对 content XML 逐 media 节点做 HTTPS GET(**唯一受限
  出网豁免**:只 GET、URL/token 全来自库内、零进程干预、不重试;见
  docs/wechat-mediadecrypt.md §11 网络纪律修订注记)。
- 响应头 ``x-enc:1`` = 密文 → 落临时文件交外部解密件 ``decrypt_stream``
  (协议 v1);403/404 = 链接失效如实「未能下载(链接已失效)」。
- 本地明文视频缓存无帖级映射(实测),不参与帖级导出;真 CDN 端到端属
  主人开箱裁量(AC4 注记),本模块 ``http_get`` 注入点供夹具级验证。

媒体状态词面(R3 判例 + 全链状态机补全,全人话):「已解密」「明文复制」
「未能下载(链接已失效)」「未配置解密件,未解密」「本地文件缺失」「实况
格式,暂不支持预览」;补全词:「未开启媒体下载」(缺省关)「解密失败」
「未能下载(网络错误)」「语音,暂不支持」。

私有数据红线:导出内容 = 用户私有产物,只落 ``--out`` 私有目录,不入日志
不入 git;错误消息只承载形状计数。微信侧零写入、微信进程零接触。
"""

from __future__ import annotations

import html as _html
import json
import os
import re
import sqlite3
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Callable

from .codes import DB_NOT_FOUND, DECRYPT_FAILED, EXIT_USAGE, BridgeError
from .localdb import LOCALDB_PRIVATE_DIR, ensure_decrypted_copies
from .localdb_query import _contact_pick_names, _open_copy
from .media import (
    STATUS_DECRYPTED,
    STATUS_WXGF,
    decrypt_stream_file,
    media_provider_path,
)
from .sns_query import (
    FEED_TABLE,
    _query_notices,
    _sanitize_numeric_entities,
    _text_of,
)

__all__ = [
    "EXPORTS_DIR_NAME",
    "parse_export_row",
    "run_sns_export",
    "sns_export_history",
    "render_html",
    "HttpTransportError",
]

#: 导出缺省根目录(数据根私有区 wechat-localdb/exports/)。
EXPORTS_DIR_NAME = "exports"

#: 媒体状态词面(R3 判例 + 状态机补全)。
STATUS_MEDIA_NOT_ENABLED = "未开启媒体下载"
STATUS_LINK_EXPIRED = "未能下载(链接已失效)"
STATUS_NETWORK_ERROR = "未能下载(网络错误)"
STATUS_PROVIDER_UNCONFIGURED = "未配置解密件,未解密"
STATUS_PLAIN_COPY = "明文复制"
STATUS_DECRYPT_FAILED = "解密失败"
STATUS_VOICE = "语音,暂不支持"

#: 单媒体回源 HTTP 超时(秒;只读单发,不重试)。
HTTP_TIMEOUT_SECONDS = 30.0

#: 语音帖 media type(非目标:如实词面不导出内容)。
_MEDIA_TYPE_VOICE = "4"
#: 视频 media type(已实证:2=图/6=视频)。
_MEDIA_TYPE_VIDEO = "6"


class HttpTransportError(Exception):
    """HTTP 传输层失败(非状态码语义;词面「未能下载(网络错误)」)。"""


def _default_http_get(
    url: str, timeout: float = HTTP_TIMEOUT_SECONDS
) -> tuple[int, dict[str, str], bytes]:
    """缺省回源实现:只读 GET(零进程干预;403/404 以状态码回给调用方)。

    Returns:
        ``(status, headers(小写键), body)``。

    Raises:
        HttpTransportError: 传输层失败(连接拒绝/DNS/超时——与链接失效分家)。
    """
    import urllib.error
    import urllib.request

    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as resp:  # noqa: S310 - URL 来自库内 content XML
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return int(resp.status), headers, resp.read()
    except urllib.error.HTTPError as exc:
        return int(exc.code), {}, b""
    except (urllib.error.URLError, OSError, ValueError) as exc:
        raise HttpTransportError(f"{type(exc).__name__}") from exc


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_export_row(content: object) -> dict[str, object] | None:
    """一行 SnsTimeLine.content(XML)→ 导出条目(含 media 全量字段)。

    与 sns_query.parse_feed_row 同判(必要字段缺失/解析不干净 = None 弃行
    计错);差异 = media 节点展开为全量清单(type/cdn_url/md5/key/enc_idx/
    token(内部用)/width/height)。尺寸属性 best-effort(media 节点或 url
    节点的 width/height 属性;缺 = None 如实)。
    """
    if not isinstance(content, str) or not content.strip():
        return None
    try:
        root = ET.fromstring(_sanitize_numeric_entities(content))
    except ET.ParseError:
        return None
    timeline = root.find("TimelineObject")
    if timeline is None:
        return None
    entry_id = _text_of(timeline.find("id"))
    username = _text_of(timeline.find("username"))
    create_time_raw = _text_of(timeline.find("createTime"))
    if not entry_id or not username or create_time_raw is None:
        return None
    try:
        create_time = int(create_time_raw)
    except ValueError:
        return None
    media_nodes: list[dict[str, object]] = []
    media_list = timeline.find("ContentObject/mediaList")
    if media_list is not None:
        for media in media_list.findall("media"):
            node: dict[str, object] = {
                "type": _text_of(media.find("type")),
                "cdn_url": None,
                "md5": None,
                "key": None,
                "enc_idx": None,
                "token": None,  # 内部回源用;JSON 载荷不吐(隐私最小化)
                "width": _int_or_none(media.get("width")),
                "height": _int_or_none(media.get("height")),
            }
            url_el = media.find("url")
            if url_el is not None:
                node["cdn_url"] = (url_el.text or "").strip() or None
                node["md5"] = url_el.get("md5") or None
                node["key"] = url_el.get("key") or None
                node["enc_idx"] = url_el.get("enc_idx") or None
                node["token"] = url_el.get("token") or None
                if node["width"] is None:
                    node["width"] = _int_or_none(url_el.get("width"))
                if node["height"] is None:
                    node["height"] = _int_or_none(url_el.get("height"))
            media_nodes.append(node)
    return {
        "id": entry_id,
        "username": username,
        "nickname": None,  # 编排层 contact 反查回填
        "create_time": create_time,
        "text": _text_of(timeline.find("contentDesc")),
        "media": media_nodes,
        "ref_username": _text_of(timeline.find("sourceUserName")),
        "ref_nickname": _text_of(timeline.find("sourceNickName")),
    }


def _payload_media(node: dict[str, object]) -> dict[str, object]:
    """媒体节点的 JSON 载荷形态(吐协议字段,内部回源字段不吐)。"""
    return {
        "type": node.get("type"),
        "cdn_url": node.get("cdn_url"),
        "md5": node.get("md5"),
        "key": node.get("key"),
        "width": node.get("width"),
        "height": node.get("height"),
        "status": node.get("status"),
        "local_path": node.get("local_path"),
    }


def _link_notices(
    entries: list[dict[str, object]], notices: list[dict[str, object]]
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """评论区关联:``feed_id`` ↔ 条目 id;未关联 notices 单独成节。

    关联词面:comment 型进条目 ``comments``、like 型进 ``likes``、其余类型
    与无 feed_id 的进未关联节(不强求 100%,关联率如实入 stats)。

    Returns:
        ``(unlinked_notices, 关联统计)``。
    """
    by_id = {str(entry["id"]): entry for entry in entries}
    for entry in entries:
        entry["comments"] = []
        entry["likes"] = []
    unlinked: list[dict[str, object]] = []
    comments_total = 0
    comments_linked = 0
    likes_total = 0
    likes_linked = 0
    for notice in notices:
        feed_id = notice.get("feed_id")
        target = by_id.get(str(feed_id)) if feed_id is not None else None
        notice_type = notice.get("type")
        if target is not None and notice_type == "comment":
            comments_total += 1
            comments_linked += 1
            comments = target["comments"]
            assert isinstance(comments, list)
            comments.append(
                {
                    "create_time": notice.get("create_time"),
                    "from_username": notice.get("from_username"),
                    "from_nickname": notice.get("from_nickname"),
                    "content": notice.get("content"),
                    "is_relative_me": notice.get("is_relative_me"),
                }
            )
        elif target is not None and notice_type == "like":
            likes_total += 1
            likes_linked += 1
            likes = target["likes"]
            assert isinstance(likes, list)
            likes.append(
                {
                    "create_time": notice.get("create_time"),
                    "from_username": notice.get("from_username"),
                    "from_nickname": notice.get("from_nickname"),
                }
            )
        else:
            if notice_type == "comment":
                comments_total += 1
            elif notice_type == "like":
                likes_total += 1
            unlinked.append(notice)
    stats = {
        "notices_total": len(notices),
        "comments_total": comments_total,
        "comments_linked": comments_linked,
        "likes_total": likes_total,
        "likes_linked": likes_linked,
        "unlinked_notices": len(unlinked),
        "comment_link_rate": (
            f"{comments_linked}/{comments_total}" if comments_total else "0/0"
        ),
    }
    return unlinked, stats


def _safe_name(text: str) -> str:
    """文件名净化(保留字母数字与连字符;其余折叠为 ``_``)。"""
    return re.sub(r"[^0-9A-Za-z_-]+", "_", text)[:80] or "item"


def _fetch_one_media(
    node: dict[str, object],
    files_dir: Path,
    base_name: str,
    *,
    config: Any,
    http_get: Callable[..., tuple[int, dict[str, str], bytes]],
    provider_runner: Callable[..., dict[str, Any]] | None = None,
) -> None:
    """R4 单媒体回源:GET → x-enc 判密 → decrypt_stream/明文复制(词面回填)。

    就地回填 ``node["status"]`` 与 ``node["local_path"]``;一切失败以词面
    收编,不抛(单媒体失败不炸整轮导出——宁缺毋假)。
    """
    url = node.get("cdn_url")
    if not isinstance(url, str) or not url:
        node["status"] = STATUS_LINK_EXPIRED
        return
    try:
        status, headers, body = http_get(url)
    except HttpTransportError as exc:
        node["status"] = f"{STATUS_NETWORK_ERROR}({exc})"
        return
    if status in (403, 404):
        node["status"] = STATUS_LINK_EXPIRED
        return
    if status != 200:
        node["status"] = f"未能下载(HTTP {status})"
        return
    encrypted = str(headers.get("x-enc", "")).strip() == "1"
    out_base = files_dir / base_name
    if not encrypted:
        ext = "mp4" if node.get("type") == _MEDIA_TYPE_VIDEO else "jpg"
        target = out_base.with_suffix(f".{ext}")
        tmp = out_base.with_name(f".tmp-{os.getpid()}-{out_base.name}")
        try:
            tmp.write_bytes(body)
            os.replace(tmp, target)
            os.chmod(target, 0o600)
        except OSError:
            node["status"] = STATUS_DECRYPT_FAILED
            return
        finally:
            if tmp.exists():
                try:
                    tmp.unlink()
                except OSError:
                    pass
        node["status"] = STATUS_PLAIN_COPY
        node["local_path"] = target.name
        return
    # 密文:交外部解密件 decrypt_stream(协议 v1;未配置 = 词面如实)
    if not media_provider_path(config):
        node["status"] = STATUS_PROVIDER_UNCONFIGURED
        return
    tmp_cipher = out_base.with_name(f".cipher-{os.getpid()}-{out_base.name}")
    try:
        tmp_cipher.write_bytes(body)
        os.chmod(tmp_cipher, 0o600)
        outcome = decrypt_stream_file(
            tmp_cipher,
            str(node.get("key") or ""),
            config,
            out_base,
            provider_runner=provider_runner,
        )
    except BridgeError:
        node["status"] = STATUS_DECRYPT_FAILED
        return
    finally:
        if tmp_cipher.exists():
            try:
                tmp_cipher.unlink()
            except OSError:
                pass
    node["status"] = (
        STATUS_WXGF if outcome.get("is_wxgf") else STATUS_DECRYPTED
    )
    node["local_path"] = Path(str(outcome["path"])).name


def _apply_default_media_status(
    entries: list[dict[str, object]], *, with_media: bool, config: Any
) -> None:
    """回源前的基线词面(缺省关 = 未开启;语音/无 URL 如实)。"""
    for entry in entries:
        media_list = entry["media"]
        assert isinstance(media_list, list)
        for node in media_list:
            assert isinstance(node, dict)
            node["status"] = None
            node["local_path"] = None
            if node.get("type") == _MEDIA_TYPE_VOICE:
                node["status"] = STATUS_VOICE
            elif not with_media:
                node["status"] = STATUS_MEDIA_NOT_ENABLED


def _media_status_counts(entries: list[dict[str, object]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    total = 0
    for entry in entries:
        media_list = entry["media"]
        assert isinstance(media_list, list)
        for node in media_list:
            assert isinstance(node, dict)
            total += 1
            word = str(node.get("status") or "未知")
            counts[word] = counts.get(word, 0) + 1
    counts["total"] = total
    return counts


def _write_private(path: Path, text: str) -> None:
    """私有区写文件(tmp+rename 原子落位;文件 600)。"""
    tmp = path.with_name(f".tmp-{os.getpid()}-{path.name}")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass


def render_html(payload: dict[str, object]) -> str:
    """HTML 单文件渲染:自包含正文 + files/ 相对引用;媒体状态人话占位。

    **禁 base64 内嵌**(R3:防单文件爆炸);未回源/未解密媒体 = 灰底占位块。
    """
    entries = payload["entries"]
    assert isinstance(entries, list)
    stats = payload["stats"]
    assert isinstance(stats, dict)
    unlinked = payload["unlinked_notices"]
    assert isinstance(unlinked, list)
    esc = _html.escape
    parts: list[str] = []
    parts.append(
        "<!DOCTYPE html><html lang=\"zh\"><head><meta charset=\"utf-8\">"
        "<title>朋友圈导出</title><style>"
        "body{font-family:-apple-system,'PingFang SC',sans-serif;max-width:680px;"
        "margin:24px auto;padding:0 12px;color:#1f2328;background:#fff}"
        "article{border:1px solid #e5e7eb;border-radius:12px;padding:12px 14px;"
        "margin-bottom:14px}"
        ".who{font-weight:600}.time{color:#6b7280;font-size:12px;margin-left:8px}"
        ".text{white-space:pre-wrap;word-break:break-word;margin:8px 0}"
        ".media{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}"
        ".media img,.media video{max-width:180px;max-height:240px;border-radius:8px}"
        ".slot{background:#f3f4f6;color:#6b7280;border-radius:8px;padding:18px 10px;"
        "font-size:12px;max-width:180px;text-align:center}"
        ".ref{color:#6b7280;font-size:12px}"
        ".comments{margin-top:8px;border-top:1px dashed #e5e7eb;padding-top:6px;"
        "font-size:13px}.comments h4{margin:6px 0 2px;font-size:12px;color:#6b7280}"
        ".cmt{margin:2px 0}.cmt .who{font-size:13px}"
        "footer{color:#9ca3af;font-size:12px;margin:18px 0}"
        "</style></head><body><h2>朋友圈导出</h2>"
    )
    for entry in entries:
        assert isinstance(entry, dict)
        nickname = entry.get("nickname") or entry.get("username") or "?"
        when = time.strftime(
            "%Y-%m-%d %H:%M", time.localtime(int(entry["create_time"]))  # type: ignore[arg-type]
        )
        parts.append(f"<article data-id=\"{esc(str(entry['id']))}\">")
        parts.append(
            f"<header><span class=\"who\">{esc(str(nickname))}</span>"
            f"<span class=\"time\">{esc(when)}</span></header>"
        )
        text = entry.get("text")
        if isinstance(text, str) and text.strip():
            parts.append(f"<p class=\"text\">{esc(text)}</p>")
        media_list = entry["media"]
        assert isinstance(media_list, list)
        if media_list:
            parts.append("<div class=\"media\">")
            for node in media_list:
                assert isinstance(node, dict)
                status = str(node.get("status") or "未知")
                local_name = node.get("local_path")
                rendered = False
                if isinstance(local_name, str) and local_name:
                    if node.get("type") == _MEDIA_TYPE_VIDEO:
                        parts.append(
                            f"<video controls src=\"files/{esc(local_name)}\"></video>"
                        )
                        rendered = True
                    elif status in (STATUS_DECRYPTED, STATUS_PLAIN_COPY):
                        parts.append(f"<img src=\"files/{esc(local_name)}\" alt=\"\">")
                        rendered = True
                if not rendered:
                    parts.append(f"<div class=\"slot\">{esc(status)}</div>")
            parts.append("</div>")
        ref_nick = entry.get("ref_nickname")
        if isinstance(ref_nick, str) and ref_nick:
            parts.append(f"<p class=\"ref\">转发自 {esc(ref_nick)}</p>")
        comments = entry["comments"]
        likes = entry["likes"]
        assert isinstance(comments, list) and isinstance(likes, list)
        if comments or likes:
            parts.append("<div class=\"comments\">")
            if likes:
                names = ", ".join(
                    esc(str(item.get("from_nickname") or item.get("from_username") or "?"))
                    for item in likes
                    if isinstance(item, dict)
                )
                parts.append(f"<h4>赞({len(likes)})</h4><p class=\"cmt\">{names}</p>")
            if comments:
                parts.append(f"<h4>评论({len(comments)})</h4>")
                for item in comments:
                    assert isinstance(item, dict)
                    who = item.get("from_nickname") or item.get("from_username") or "?"
                    content = item.get("content") or "(无文本)"
                    parts.append(
                        f"<p class=\"cmt\"><span class=\"who\">{esc(str(who))}</span>:"
                        f"{esc(str(content))}</p>"
                    )
            parts.append("</div>")
        parts.append("</article>")
    if unlinked:
        parts.append(
            f"<footer>另有 {len(unlinked)} 条互动通知未关联到窗口内条目"
            "(好友间互动或条目在窗口外;JSON 载荷 unlinked_notices 节可查)。</footer>"
        )
    # 摘要行单独拼(CSS 花括号与 str.format 不共容——正文零 format 化)
    parts.append(
        f"<footer>条目 {stats.get('entries', len(entries))} 条;"
        f"评论关联 {stats.get('comment_link_rate', '0/0')};"
        f"媒体 {_media_summary_line(stats)}。由 MYIA 微信本机桥只读导出。"
        "</footer></body></html>"
    )
    return "".join(parts)


def _media_summary_line(stats: dict[str, object]) -> str:
    """stats 的 media_status 摘要行(词面×计数,人读)。"""
    media_status = stats.get("media_status")
    if not isinstance(media_status, dict):
        return "无"
    pieces = [
        f"{word}×{count}"
        for word, count in sorted(media_status.items())
        if word != "total"
    ]
    return ";".join(pieces) or "无"


def run_sns_export(
    *,
    copy_dir: Path,
    since_days: int,
    copy_info: dict[str, object],
    fmt: str = "json",
    out_dir: Path | None = None,
    data_root: Path | None = None,
    with_media: bool = False,
    config: Any = None,
    http_get: Callable[..., tuple[int, dict[str, str], bytes]] | None = None,
    provider_runner: Callable[..., dict[str, Any]] | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """R3 导出编排本体(对解密副本纯只读;命令壳在 cli.py 接线批)。

    Returns:
        ``{"sns_export": {format, out_dir, files[], with_media, stats{}}}``。
    """
    from .config import myssia_home

    if fmt not in ("json", "html"):
        raise BridgeError(
            EXIT_USAGE, f"--format 须为 json|html,当前为 {fmt!r}", code="usage"
        )
    con = _open_copy(copy_dir, "sns/sns.db")
    if con is None:
        raise BridgeError(
            DECRYPT_FAILED,
            "sns 域解密副本不可用(导出前置;副本缺失或损坏)",
            fix_hint="重跑 localdb sns export 触发副本重建;持续失败先核密钥与 sqlcipher",
        )
    since_ts = int(time.time() if now is None else now) - since_days * 86400
    entries: list[dict[str, object]] = []
    parse_errors = 0
    out_of_window = 0
    rows_total = 0
    notices: list[dict[str, object]] = []
    notices_note: str | None = None
    try:
        try:
            rows = con.execute(
                f'SELECT user_name, content FROM "{FEED_TABLE}"'
            ).fetchall()
        except sqlite3.Error as exc:
            raise BridgeError(
                DECRYPT_FAILED,
                f"sns 副本 {FEED_TABLE} 查询失败({type(exc).__name__});疑似副本损坏",
                fix_hint="删除数据根 wechat-localdb/decrypted/sns/ 触发下轮重建(纯派生缓存,安全)",
            ) from exc
        rows_total = len(rows)
        for _user_name, content in rows:
            entry = parse_export_row(content)
            if entry is None:
                parse_errors += 1
                continue
            if int(entry["create_time"]) < since_ts:  # type: ignore[arg-type]
                out_of_window += 1
                continue
            entries.append(entry)
        entries.sort(key=lambda item: int(item["create_time"]))  # type: ignore[arg-type]
        contact_con = _open_copy(copy_dir, "contact/contact.db")
        if contact_con is not None:
            try:
                names = _contact_pick_names(
                    contact_con,
                    [str(item["username"]) for item in entries],
                )
                for item in entries:
                    nickname = names.get(str(item["username"]))
                    if nickname:
                        item["nickname"] = nickname
            finally:
                contact_con.close()
        try:
            notices = list(_query_notices(con, since_ts, since_days)["notices"])
        except BridgeError as exc:
            # 通知表缺位/漂移 = 评论区降级为空(导出以正文为主,如实注记不判错)
            notices_note = f"互动通知不可用({exc.name})"
    finally:
        con.close()

    unlinked, link_stats = _link_notices(entries, notices)
    _apply_default_media_status(entries, with_media=with_media, config=config)

    # —— 产物落位(--out 用户自选;缺省 = 数据根私有区 exports/sns-<ts>/)——
    if out_dir is not None:
        target_dir = Path(out_dir).expanduser()
    else:
        root = data_root if data_root is not None else myssia_home()
        stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(time.time() if now is None else now))
        target_dir = root / LOCALDB_PRIVATE_DIR / EXPORTS_DIR_NAME / f"sns-{stamp}"
    target_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(target_dir, 0o700)
    files: list[str] = []

    if with_media:
        files_dir = target_dir / "files"
        files_dir.mkdir(exist_ok=True)
        os.chmod(files_dir, 0o700)
        fetcher = http_get if http_get is not None else _default_http_get
        for entry in entries:
            media_list = entry["media"]
            assert isinstance(media_list, list)
            for index, node in enumerate(media_list):
                assert isinstance(node, dict)
                if node.get("status") is not None and node.get("status") != STATUS_MEDIA_NOT_ENABLED:
                    continue  # 语音等基线词面已定,不回源
                base_name = f"{_safe_name(str(entry['id']))}_{index}"
                _fetch_one_media(
                    node,
                    files_dir,
                    base_name,
                    config=config,
                    http_get=fetcher,
                    provider_runner=provider_runner,
                )
                if node.get("local_path"):
                    files.append(f"files/{node['local_path']}")

    stats: dict[str, object] = {
        "entries": len(entries),
        "rows_total": rows_total,
        "rows_out_of_window": out_of_window,
        "parse_errors": parse_errors,
        "since_days": since_days,
        "with_media": with_media,
        "media_status": _media_status_counts(entries),
    }
    stats.update(link_stats)
    if notices_note is not None:
        stats["notices_note"] = notices_note

    if fmt == "json":
        payload = {
            "entries": [
                {**entry, "media": [_payload_media(n) for n in entry["media"]]}  # type: ignore[index,attr-defined]
                for entry in entries
            ],
            "unlinked_notices": unlinked,
            "stats": stats,
        }
        artifact = target_dir / "sns-export.json"
        _write_private(
            artifact,
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
        )
        files.append("sns-export.json")
    else:
        payload = {
            "entries": [
                {**entry, "media": [_payload_media(n) for n in entry["media"]]}  # type: ignore[index,attr-defined]
                for entry in entries
            ],
            "unlinked_notices": unlinked,
            "stats": stats,
        }
        artifact = target_dir / "index.html"
        _write_private(artifact, render_html(payload))
        files.append("index.html")

    return {
        "sns_export": {
            "format": fmt,
            "out_dir": str(target_dir),
            "files": files,
            "with_media": with_media,
            "stats": stats,
        }
    }


def sns_export_history(
    config: Any,
    db_storage: Path,
    keys: dict[str, str],
    fmt: str,
    out_dir: Path | None,
    since_days: int,
    *,
    with_media: bool = False,
    data_root: Path | None = None,
    http_get: Callable[..., tuple[int, dict[str, str], bytes]] | None = None,
    provider_runner: Callable[..., dict[str, Any]] | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """``localdb sns export`` 全链编排(与 sns_history 同构,域 sns+contact)。"""
    copy_info = ensure_decrypted_copies(
        db_storage,
        keys,
        domains=["sns", "contact"],
        ttl_hours=getattr(config, "copy_ttl_hours", 24),
        capacity_mb=getattr(config, "copy_capacity_mb", 512),
        data_root=data_root,
        now=now,
    )
    return run_sns_export(
        copy_dir=Path(str(copy_info["dir"])),
        since_days=since_days,
        copy_info=copy_info,
        fmt=fmt,
        out_dir=out_dir,
        data_root=data_root,
        with_media=with_media,
        config=config,
        http_get=http_get,
        provider_runner=provider_runner,
        now=now,
    )


# 静态对账:表名锚与 sns_query 同源(缺表判据共用)。
assert FEED_TABLE == "SnsTimeLine"
