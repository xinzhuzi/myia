"""R4/R5 六格式导出器:JSON/TXT/CSV/Markdown/HTML/Excel(task 10-14-wechat-chat-export)。

数据面 = R1 分页通道复用(:func:`wechat_bridge.localdb_page.run_page` 同游标
逐批,批 :data:`EXPORT_PAGE_BATCH`);**禁全量载入内存**——JSON 手写流式
数组、xlsx 走 ``xlsxwriter constant_memory=True``、文本族逐行写。

取消安全(prd R5,替代 WeFlow worker 协议):全部产物先写
``<out>/.wechat-export-staging-<pid>-<ts>/``,完成(含 manifest)后逐件
``os.replace`` 原子落位;SIGTERM/异常 → staging 整目录清除,零半成品最终件
(``--all`` 每会话完成即落位,会话粒度提交)。

清单密封(WeChatDataAnalysis 思想,零码借):``manifest.json`` 最后写,含每件
sha256 + 导出选项回显 + 行数 + 时间范围;``--verify`` 子动作重算对账。

隐私(prd 红线 6;chatlog-keeper private_text_writer 语义):导出件与
manifest 落盘即 ``0600``(``os.open`` mode 位);聊天内容不入日志/报告——
进度行只带计数与形状;本模块错误消息只承载路径与原因。

许可红线:WeFlow(CC BY-NC-SA)与 WeChatDataAnalysis(无许可)零码借;
chatlog-keeper(MIT)语义参考(per-shard keyset 游标/显示名回退链/0600),
自写实现。
"""

from __future__ import annotations

import hashlib
import html as _html
import io
import json
import os
import re
import signal
import shutil
import time
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from . import localdb_page, localdb_query
from .codes import EXIT_USAGE, BridgeError
from .localdb_page import (
    EXPORT_PAGE_BATCH,
    run_page,
    scan_conversations,
    self_wxid,
)
from .localdb_query import _open_copy

__all__ = [
    "EXPORT_FORMATS",
    "XLSX_SHEET_ROW_CAP",
    "PROGRESS_MIN_INTERVAL_SECONDS",
    "PROGRESS_MIN_ROWS",
    "sanitize_file_name",
    "build_file_name",
    "run_export",
    "run_export_all",
    "verify_manifest",
]

#: 六格式词表(CLI --format 校验源)。
EXPORT_FORMATS = ("json", "txt", "csv", "md", "html", "xlsx")

#: xlsx 单表行帽(含表头;Excel 硬上限 1,048,576)→ Sheet2/Sheet3… 顺延分表。
XLSX_SHEET_ROW_CAP = 1_048_576

#: 进度节流:最小间隔 400ms 或增量 1200 条(先到即发);phase 切换强制发。
PROGRESS_MIN_INTERVAL_SECONDS = 0.4
PROGRESS_MIN_ROWS = 1200

#: staging 目录前缀(``<pid>-<ts>`` 防并发撞名;完成后逐件原子落位)。
_STAGING_PREFIX = ".wechat-export-staging-"

#: 显示名优先级词表(prd R4:remark-first 缺省 = 既有链;群昵称档不做)。
DISPLAY_NAME_PREFS = ("remark-first", "nickname-first")

#: 文件名双模式词表(prd R4:classic / date-range,WeFlow 语义)。
NAME_MODES = ("classic", "date-range")

# ---------------------------------------------------------------------------
# 纯函数:文件名与消毒
# ---------------------------------------------------------------------------

#: 文件系统消毒字符(Windows 禁字符全集 + 控制符;其余字符保真不 ASCII 化)。
_SANITIZE_PATTERN = re.compile(r'[\\/:*?"<>|\x00-\x1f]')


def sanitize_file_name(raw: str) -> str:
    """显示名 → 文件系统安全名(禁字符/控制符 → ``_``;中文/表情保真)。"""
    cleaned = _SANITIZE_PATTERN.sub("_", raw).strip().strip(".")
    return cleaned or "_"


def build_file_name(
    *,
    display_name: str | None,
    chat_id: str,
    fmt: str,
    name_mode: str,
    from_date: str | None,
    to_date: str | None,
    now: float | None = None,
) -> str:
    """导出件名(prd R4 双模式):

    - classic:``聊天记录-{显示名|chat_id}-{YYYYMMDD-HHMMSS}.{ext}``
    - date-range:``聊天记录-{显示名|chat_id}-{from}__{to}.{ext}``(YYYYMMDD;
      窗口缺边 → 以数据实际边界补,零行 → 当天;缺哪补哪,不臆造宽窗)。
    """
    who = sanitize_file_name(display_name if display_name else chat_id)
    ext = {"md": "md", "json": "json", "txt": "txt", "csv": "csv", "html": "html", "xlsx": "xlsx"}[fmt]
    if name_mode == "date-range":
        today = time.strftime("%Y%m%d", time.localtime(now if now is not None else time.time()))
        lo = from_date or today
        hi = to_date or today
        return f"聊天记录-{who}-{lo}__{hi}.{ext}"
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(now if now is not None else time.time()))
    return f"聊天记录-{who}-{stamp}.{ext}"


# ---------------------------------------------------------------------------
# 显示名解析器(remark-first / nickname-first;惰性缓存,流式友好)
# ---------------------------------------------------------------------------


class _DisplayNameResolver:
    """wxid → 显示名(优先级可调;单点查询 + 进程内缓存,流式导出友好)。

    remark-first = 既有链 remark>nickname>alias(localdb_query._contact_pick_names
    同族);nickname-first = 跳过 remark(nickname>alias,prd R4 两档;群昵称
    档不进本期)。contact 域缺席 = 不解析,sender 维持 wxid(如实)。
    """

    _NAME_COLS_REMARK = ("remark", "Remark", "conRemark", "nick_name", "nickname", "nickName", "NickName", "alias")
    _NAME_COLS_NICK = ("nick_name", "nickname", "nickName", "NickName", "alias")

    def __init__(self, copy_dir: Path, pref: str) -> None:
        if pref not in DISPLAY_NAME_PREFS:
            raise BridgeError(
                EXIT_USAGE,
                f"--display-name-pref 须为 {'|'.join(DISPLAY_NAME_PREFS)},当前为 {pref!r}",
                code="usage",
            )
        self._pref = pref
        self._copy_dir = copy_dir
        self._cache: dict[str, str | None] = {}

    def resolve(self, wxid: str | None) -> str | None:
        if not wxid or wxid not in self._cache:
            if not wxid:
                return None
            self._cache[wxid] = self._lookup(wxid)
        return self._cache[wxid]

    def _lookup(self, wxid: str) -> str | None:
        con = _open_copy(self._copy_dir, "contact/contact.db")
        if con is None:
            self._cache_everything_miss()  # contact 域缺席:后续全 miss 快速路
            return None
        try:
            candidates = (
                self._NAME_COLS_REMARK
                if self._pref == "remark-first"
                else self._NAME_COLS_NICK
            )
            tables = [
                row[0]
                for row in con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                )
            ]
            for table in tables:
                if "contact" not in table.lower():
                    continue
                columns = [
                    row[1] for row in con.execute(f'PRAGMA table_info("{table}")')
                ]
                lowered = {c.lower(): c for c in columns}
                id_col = next(
                    (lowered[c.lower()] for c in ("username", "userName", "UserName", "user_name") if c.lower() in lowered),
                    None,
                )
                if id_col is None:
                    continue
                selects = []
                for cand in candidates:
                    actual = lowered.get(cand.lower())
                    if actual and actual not in selects:
                        selects.append(actual)
                if not selects:
                    continue
                quoted = ", ".join(f'"{c}"' for c in selects)
                try:
                    row = con.execute(
                        f'SELECT {quoted} FROM "{table}" WHERE "{id_col}" = ?',
                        (wxid,),
                    ).fetchone()
                except Exception:  # noqa: BLE001 - 表漂移试下一张(同族判例)
                    continue
                if row:
                    value = next((v for v in row if isinstance(v, str) and v.strip()), None)
                    if value:
                        return value
        finally:
            con.close()
        return None

    def _cache_everything_miss(self) -> None:
        self._lookup = lambda wxid: None  # type: ignore[method-assign]

    def batch(self, wxids: Iterable[str]) -> dict[str, str]:
        """批量解析(首帧 display_name/导出件名用;未命中不入映射)。"""
        out: dict[str, str] = {}
        for wxid in wxids:
            display = self.resolve(wxid)
            if display:
                out[wxid] = display
        return out


# ---------------------------------------------------------------------------
# 流式源(R1 通道复用;游标逐批)
# ---------------------------------------------------------------------------


def iter_export_entries(
    copy_dir: Path,
    chat_id: str,
    *,
    from_ts: int | None = None,
    to_ts: int | None = None,
    types: list[str] | None = None,
    sender: str | None = None,
    asc: bool = True,
    cancel: Callable[[], bool] | None = None,
) -> Iterator[dict[str, object]]:
    """按批产出 R1 消息条目(升序流;批 :data:`EXPORT_PAGE_BATCH`;取消即停)。

    导出恒升序(时间线阅读序);sender 显示名在调用方按条套(resolve 惰性)。
    """
    cursor: str | None = None
    while True:
        if cancel is not None and cancel():
            raise BridgeError(143, "导出已取消", code="export_cancelled")
        payload = run_page(
            copy_dir,
            chat_id,
            cursor=cursor,
            limit=EXPORT_PAGE_BATCH,
            asc=asc,
            from_ts=from_ts,
            to_ts=to_ts,
            types=types,
            sender=sender,
        )
        page = payload["page"]
        yield from page["messages"]
        if not page["has_more"] or page["next_cursor"] is None:
            return
        cursor = page["next_cursor"]


# ---------------------------------------------------------------------------
# 写出件(0600 落盘 + 写入即哈希;文本族统一门面)
# ---------------------------------------------------------------------------


class _Sink:
    """staging 内单件:``os.open`` 0600 建档,写文本同时喂 sha256。"""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        self._hash = hashlib.sha256()
        self._buffer = io.TextIOWrapper(
            open(self._fd, "wb", closefd=False), encoding="utf-8", newline=""
        )

    def write(self, text: str) -> None:
        self._buffer.write(text)
        self._hash.update(text.encode("utf-8"))

    def close(self) -> None:
        self._buffer.close()
        os.close(self._fd)

    @property
    def sha256(self) -> str:
        return self._hash.hexdigest()


def _entry_content(entry: dict[str, object]) -> str:
    text = entry.get("text")
    if isinstance(text, str):
        return text
    placeholder = entry.get("placeholder")
    return placeholder if isinstance(placeholder, str) else ""


def _day_of(ts: int) -> str:
    return time.strftime("%Y-%m-%d", time.localtime(ts)) if ts > 0 else ""


def _clock_of(ts: int) -> str:
    return time.strftime("%H:%M:%S", time.localtime(ts)) if ts > 0 else "--:--:--"


# ---------------------------------------------------------------------------
# 六格式流式写手(entry 迭代器 → 单件;全部禁全量入内存)
# ---------------------------------------------------------------------------


def write_json(sink: _Sink, entries: Iterator[dict[str, object]]) -> int:
    """JSON:流式数组(元素 = R1 条目原形,零信息丢失)。"""
    sink.write("[")
    count = 0
    for entry in entries:
        sink.write(("," if count else "") + json.dumps(entry, ensure_ascii=False))
        count += 1
    sink.write("]\n")
    return count


def write_txt(sink: _Sink, entries: Iterator[dict[str, object]]) -> int:
    """TXT:日分隔 + ``[HH:MM:SS] 发送者(类型): 内容``;缺时间 → 无日分隔。"""
    count = 0
    current_day = None
    for entry in entries:
        ts = int(entry.get("ts") or 0)
        day = _day_of(ts)
        if day and day != current_day:
            sink.write(f"—— {day} ——\n")
            current_day = day
        sink.write(
            f"[{_clock_of(ts)}] {entry.get('sender')}({entry.get('type')}): "
            f"{_entry_content(entry)}\n"
        )
        count += 1
    return count


def _csv_field(field: str) -> str:
    """CSV 单元格:注入中和(= + - @ / tab 开头前置 ')→ RFC 4180 引号转义
    (中和先于引号判定,wechat_group_export.rs 判例同款)。"""
    if field and field[0] in ("=", "+", "-", "@", "\t"):
        field = "'" + field
    if any(ch in field for ch in (",", '"', "\n", "\r")):
        field = '"' + field.replace('"', '""') + '"'
    return field


def write_csv(sink: _Sink, entries: Iterator[dict[str, object]]) -> int:
    """CSV:UTF-8 BOM + 表头 time,sender,sender_id,type,content + 注入中和;
    CRLF 行尾(Excel 直开判例);全部经 sink.write(哈希同流)。"""
    sink.write("﻿time,sender,sender_id,type,content\r\n")
    count = 0
    for entry in entries:
        ts = int(entry.get("ts") or 0)
        cells = (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)) if ts > 0 else "",
            str(entry.get("sender") or ""),
            str(entry.get("sender_id") or ""),
            str(entry.get("type") or ""),
            _entry_content(entry),
        )
        sink.write(",".join(_csv_field(cell) for cell in cells) + "\r\n")
        count += 1
    return count


_MD_ESCAPE_CHARS = "\\`*_{}[]()#+-.!|<>~"


def _md_escape(text: str) -> str:
    out: list[str] = []
    for ch in text:
        out.append("\\" + ch if ch in _MD_ESCAPE_CHARS else ch)
    return "".join(out)


def write_md(sink: _Sink, entries: Iterator[dict[str, object]]) -> int:
    """Markdown:二级标题按日 + ``**发送者** · HH:MM:SS`` + 内容引用块。"""
    count = 0
    current_day = None
    for entry in entries:
        ts = int(entry.get("ts") or 0)
        day = _day_of(ts)
        if day and day != current_day:
            sink.write(f"\n## {day}\n\n" if count else f"## {day}\n\n")
            current_day = day
        content = _md_escape(_entry_content(entry)).replace("\n", "\n> ")
        sink.write(
            f"**{_md_escape(str(entry.get('sender') or ''))}** · {_clock_of(ts)}\n"
            f"> {content}\n\n"
        )
        count += 1
    return count


_HTML_CSS = (
    "body{font-family:-apple-system,'PingFang SC',sans-serif;background:#f2f2f2;"
    "margin:0;padding:16px;color:#1f1f1f}"
    "h1{font-size:18px;margin:0 0 4px}"
    ".meta{font-size:12px;color:#888;margin-bottom:12px}"
    ".day{text-align:center;color:#999;font-size:12px;margin:16px 0 8px}"
    ".row{display:flex;margin:6px 0}"
    ".row.me{justify-content:flex-end}"
    ".bubble{max-width:72%;border-radius:10px;padding:8px 12px;background:#fff;"
    "box-shadow:0 1px 1px rgba(0,0,0,.06);font-size:14px;line-height:1.5;"
    "white-space:pre-wrap;word-break:break-word}"
    ".row.me .bubble{background:#95ec69}"
    ".head{font-size:11px;color:#999;margin-bottom:2px}"
)


def write_html(
    sink: _Sink,
    entries: Iterator[dict[str, object]],
    *,
    title: str,
    self_id: str | None,
    total_hint: int | None = None,
) -> int:
    """HTML:自包含单文件——内联 CSS、零外链零脚本零远程请求,全部插值
    html.escape;日分隔 + 左右气泡(自端 = self_id 锚定,缺锚单侧如实)。"""
    esc = _html.escape
    sink.write(
        "<!DOCTYPE html>\n<html lang=\"zh\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{esc(title)}</title>\n<style>{_HTML_CSS}</style>\n</head>\n<body>\n"
        f"<h1>{esc(title)}</h1>\n"
    )
    if total_hint is not None:
        sink.write(f"<div class=\"meta\">{esc(str(total_hint))} 条消息</div>\n")
    count = 0
    current_day = None
    for entry in entries:
        ts = int(entry.get("ts") or 0)
        day = _day_of(ts)
        if day and day != current_day:
            sink.write(f"<div class=\"day\">—— {esc(day)} ——</div>\n")
            current_day = day
        sender = str(entry.get("sender") or "")
        sender_id = str(entry.get("sender_id") or "")
        mine = self_id is not None and sender_id == self_id
        side = "me" if mine else "them"
        sink.write(
            f"<div class=\"row {side}\"><div class=\"bubble\">"
            f"<div class=\"head\">{esc(sender)} · {esc(_clock_of(ts))} · "
            f"{esc(str(entry.get('type') or ''))}</div>"
            f"{esc(_entry_content(entry))}</div></div>\n"
        )
        count += 1
    sink.write("</body>\n</html>\n")
    return count


def write_xlsx(path: Path, entries: Iterator[dict[str, object]]) -> int:
    """Excel:xlsxwriter constant_memory 流式;单表行帽(含表头)
    :data:`XLSX_SHEET_ROW_CAP` → Sheet2/Sheet3… 顺延分表(阈值行为夹具演练
    = 测试 monkeypatch 帽值)。sha256 由调用方收尾读文件计算(xlsxwriter
    直写内层,哈希在 close 后一遍过)。"""
    xlsxwriter = _import_xlsxwriter()
    workbook = xlsxwriter.Workbook(str(path), {"constant_memory": True})
    header = ("时间", "发送者", "类型", "内容")
    data_cap = XLSX_SHEET_ROW_CAP - 1  # 含表头
    sheet_index = 0
    sheet = workbook.add_worksheet(f"Sheet{sheet_index + 1}")
    sheet.write_row(0, 0, header)
    written_in_sheet = 0
    count = 0
    for entry in entries:
        if written_in_sheet >= data_cap:
            sheet_index += 1
            sheet = workbook.add_worksheet(f"Sheet{sheet_index + 1}")
            sheet.write_row(0, 0, header)
            written_in_sheet = 0
        ts = int(entry.get("ts") or 0)
        sheet.write_row(
            written_in_sheet + 1,
            0,
            (
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts)) if ts > 0 else "",
                str(entry.get("sender") or ""),
                str(entry.get("type") or ""),
                _entry_content(entry),
            ),
        )
        written_in_sheet += 1
        count += 1
    workbook.close()
    os.chmod(path, 0o600)
    return count


def _import_xlsxwriter() -> Any:
    try:
        import xlsxwriter  # noqa: PLC0415 - 惰性导入:非 xlsx 格式零依赖
    except ImportError as exc:
        raise BridgeError(
            1,
            "xlsx 导出需要 xlsxwriter 组件依赖(pip install xlsxwriter)",
            code="dependency_missing",
            fix_hint="桥组件环境执行 pip install xlsxwriter(或随组件安装脚本装齐)",
        ) from exc
    return xlsxwriter


# ---------------------------------------------------------------------------
# 进度节流器(prd R5:400ms / 1200 条 / phase 切换强制)
# ---------------------------------------------------------------------------


class _ProgressPacer:
    """进度节流:最小间隔或增量先到即发;phase 变化强制发;首条强制发。"""

    def __init__(self, emit: Callable[[dict[str, object]], None]) -> None:
        self._emit = emit
        self._last_ts = 0.0
        self._last_rows = 0
        self._last_phase = ""

    @property
    def rows(self) -> int:
        """已发进度行数位(会话间续接用)。"""
        return self._last_rows

    def tick(
        self,
        *,
        phase: str,
        rows: int,
        current_chat: str | None = None,
        pct_est: float | None = None,
        force: bool = False,
    ) -> None:
        now = time.monotonic()
        phase_switch = phase != self._last_phase
        due = (
            force
            or phase_switch
            or self._last_ts == 0.0
            or (now - self._last_ts) >= PROGRESS_MIN_INTERVAL_SECONDS
            or (rows - self._last_rows) >= PROGRESS_MIN_ROWS
        )
        if not due:
            return
        progress: dict[str, object] = {"phase": phase, "rows": rows}
        if current_chat is not None:
            progress["current_chat"] = current_chat
        if pct_est is not None:
            progress["pct_est"] = pct_est
        self._emit({"progress": progress})
        self._last_ts = now
        self._last_rows = rows
        self._last_phase = phase


# ---------------------------------------------------------------------------
# 编排:单会话导出 + 全库导出 + 对账
# ---------------------------------------------------------------------------


class _CancelState:
    """SIGTERM/回调双路取消位(测试注入回调,生产装信号处理器)。"""

    def __init__(self) -> None:
        self.flag = False
        self._prev_handler: Any = None

    def cancel(self) -> bool:
        return self.flag

    def install_signal(self) -> None:
        self._prev_handler = signal.signal(signal.SIGTERM, self._on_sigterm)

    def restore_signal(self) -> None:
        if self._prev_handler is not None:
            signal.signal(signal.SIGTERM, self._prev_handler)
            self._prev_handler = None

    def _on_sigterm(self, signum: int, frame: Any) -> None:  # noqa: ARG002
        self.flag = True


class _RangeTracker:
    """条目流时间范围追踪(迭代透传;min/max ts 记入 holder)。"""

    def __init__(self) -> None:
        self.from_ts: int | None = None
        self.to_ts: int | None = None

    def wrap(
        self, entries: Iterable[dict[str, object]]
    ) -> Iterator[dict[str, object]]:
        for entry in entries:
            ts = int(entry.get("ts") or 0)
            if ts > 0:
                self.from_ts = ts if self.from_ts is None else min(self.from_ts, ts)
                self.to_ts = ts if self.to_ts is None else max(self.to_ts, ts)
            yield entry

    def as_dict(self) -> dict[str, int] | None:
        if self.from_ts is None:
            return None
        return {"from_ts": self.from_ts, "to_ts": self.to_ts}


def _apply_display_to_entries(
    entries: Iterable[dict[str, object]], resolver: _DisplayNameResolver
) -> Iterator[dict[str, object]]:
    for entry in entries:
        wxid = entry.get("sender_id")
        display = resolver.resolve(wxid if isinstance(wxid, str) else None)
        if display:
            entry["sender"] = display
        yield entry


def _write_one_format(
    fmt: str,
    staging_dir: Path,
    file_name: str,
    entries: Iterator[dict[str, object]],
    *,
    html_title: str,
    self_id: str | None,
    total_hint: int | None,
) -> dict[str, object]:
    """单件写出(staging 内)→ ``{"name","path","rows","sha256","bytes"}``。"""
    target = staging_dir / file_name
    if fmt == "xlsx":
        rows = write_xlsx(target, entries)
        digest = _hash_file(target)
    else:
        sink = _Sink(target)
        try:
            if fmt == "json":
                rows = write_json(sink, entries)
            elif fmt == "txt":
                rows = write_txt(sink, entries)
            elif fmt == "csv":
                rows = write_csv(sink, entries)
            elif fmt == "md":
                rows = write_md(sink, entries)
            else:
                rows = write_html(
                    sink, entries, title=html_title, self_id=self_id, total_hint=total_hint
                )
        finally:
            sink.close()
        digest = sink.sha256
    return {
        "name": file_name,
        "path": str(target),
        "rows": rows,
        "sha256": digest,
        "bytes": target.stat().st_size,
    }


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _commit_file(staging_path: Path, final_dir: Path) -> Path:
    final_dir.mkdir(parents=True, exist_ok=True)
    final = final_dir / staging_path.name
    os.replace(staging_path, final)
    return final


def run_export(
    copy_dir: Path,
    chat_id: str | None,
    out_dir: Path,
    *,
    fmt: str,
    from_ts: int | None = None,
    to_ts: int | None = None,
    types: list[str] | None = None,
    sender: str | None = None,
    display_name_pref: str = "remark-first",
    name_mode: str = "classic",
    all_chats: bool = False,
    progress: Callable[[dict[str, object]], None] | None = None,
    should_cancel: Callable[[], bool] | None = None,
    now: float | None = None,
) -> dict[str, object]:
    """导出编排主体(staging → 流式写 → manifest → 原子落位)。

    Returns:
        回执 ``{"export": {chat_id?, display_name, format, files[…],
        manifest_path, total_rows, time_range?, elapsed_ms}}``(键序 = prd R5)。

    Raises:
        BridgeError: 143 ``export_cancelled``(SIGTERM/回调取消,staging 已清);
        其余具名族透传(usage/dependency/index_plan_scan…)。
    """
    if fmt not in EXPORT_FORMATS:
        raise BridgeError(
            EXIT_USAGE,
            f"--format 须为 {'|'.join(EXPORT_FORMATS)} 之一,当前为 {fmt!r}",
            code="usage",
        )
    if name_mode not in NAME_MODES:
        raise BridgeError(
            EXIT_USAGE,
            f"--name-mode 须为 {'|'.join(NAME_MODES)} 之一,当前为 {name_mode!r}",
            code="usage",
        )
    started = time.monotonic()
    pacer = _ProgressPacer(progress or (lambda _payload: None))
    cancel_state = _CancelState()
    if should_cancel is not None:
        effective_cancel = should_cancel  # 测试/编排层注入取消位(不装信号)
    else:
        cancel_state.install_signal()
        effective_cancel = cancel_state.cancel
    resolver = _DisplayNameResolver(copy_dir, display_name_pref)
    out_dir.mkdir(parents=True, exist_ok=True)
    staging_dir = out_dir / f"{_STAGING_PREFIX}{os.getpid()}-{int(time.time())}"
    staging_dir.mkdir(parents=True)
    os.chmod(staging_dir, 0o700)
    try:
        if all_chats:
            files = _export_all_chats(
                copy_dir,
                out_dir,
                staging_dir,
                resolver,
                fmt=fmt,
                from_ts=from_ts,
                to_ts=to_ts,
                types=types,
                sender=sender,
                name_mode=name_mode,
                pacer=pacer,
                cancel=effective_cancel,
                now=now,
            )
            chat_id_out: str | None = None
            display_out: str | None = None
        else:
            if not chat_id:
                raise BridgeError(EXIT_USAGE, "单会话导出必须给 chat_id", code="usage")
            chat_display = resolver.resolve(chat_id)
            files = [
                _export_one_chat(
                    copy_dir,
                    chat_id,
                    chat_display,
                    staging_dir,
                    fmt=fmt,
                    from_ts=from_ts,
                    to_ts=to_ts,
                    types=types,
                    sender=sender,
                    name_mode=name_mode,
                    pacer=pacer,
                    cancel=effective_cancel,
                    resolver=resolver,
                    now=now,
                    final_dir=out_dir,
                )
            ]
            chat_id_out = chat_id
            display_out = chat_display
        total_rows = sum(int(f["rows"]) for f in files)
        time_range = _files_time_range(files)
        manifest_path = _write_manifest(
            staging_dir,
            files,
            final_dir=out_dir,
            fmt=fmt,
            chat_id=chat_id_out,
            display_name=display_out,
            options={
                "format": fmt,
                "from_ts": from_ts,
                "to_ts": to_ts,
                "types": types or [],
                "sender": sender,
                "display_name_pref": display_name_pref,
                "name_mode": name_mode,
                "all": all_chats,
            },
            total_rows=total_rows,
            time_range=time_range,
        )
        shutil.rmtree(staging_dir, ignore_errors=True)  # 成功路径零残留(清 staging 根)
        return {
            "export": {
                "chat_id": chat_id_out,
                "display_name": display_out,
                "format": fmt,
                "files": [
                    {"name": f["name"], "path": f["path"], "rows": f["rows"], "sha256": f["sha256"]}
                    for f in files
                ],
                "manifest_path": str(manifest_path),
                "total_rows": total_rows,
                "time_range": time_range,
                "elapsed_ms": int((time.monotonic() - started) * 1000),
            }
        }
    except BaseException:
        shutil.rmtree(staging_dir, ignore_errors=True)  # 零半成品(staging 内未落位件)
        raise
    finally:
        cancel_state.restore_signal()


def _export_one_chat(
    copy_dir: Path,
    chat_id: str,
    chat_display: str | None,
    staging_dir: Path,
    *,
    fmt: str,
    from_ts: int | None,
    to_ts: int | None,
    types: list[str] | None,
    sender: str | None,
    name_mode: str,
    pacer: _ProgressPacer,
    cancel: Callable[[], bool],
    resolver: _DisplayNameResolver,
    now: float | None,
    final_dir: Path,
    staging_prefix: str = "",
) -> dict[str, object]:
    """单会话导出(--all 的每会话单元同走这里;会话粒度提交)。

    staging_prefix:--all 共用 staging 目录,同名文件先落序号前缀防互覆;
    单会话路径无前缀(staging 只有本会话一件)。
    """
    pacer.tick(phase="write", rows=pacer.rows, current_chat=chat_display or chat_id, force=True)
    tracker = _RangeTracker()
    entries = iter_export_entries(
        copy_dir,
        chat_id,
        from_ts=from_ts,
        to_ts=to_ts,
        types=types,
        sender=sender,
        cancel=cancel,
    )
    displayed = _apply_display_to_entries(entries, resolver)
    from_date = time.strftime("%Y%m%d", time.localtime(from_ts)) if from_ts else None
    to_date = time.strftime("%Y%m%d", time.localtime(to_ts)) if to_ts else None
    file_name = build_file_name(
        display_name=chat_display,
        chat_id=chat_id,
        fmt=fmt,
        name_mode=name_mode,
        from_date=from_date,
        to_date=to_date,
        now=now,
    )
    info = _write_one_format(
        fmt,
        staging_dir,
        staging_prefix + file_name,
        tracker.wrap(displayed),
        html_title=f"聊天记录-{chat_display or chat_id}",
        self_id=self_wxid(copy_dir) if fmt == "html" else None,
        total_hint=None,
    )
    committed = _commit_file(Path(str(info["path"])), final_dir)
    info["path"] = str(committed)
    info["time_range"] = tracker.as_dict()
    pacer.tick(phase="write", rows=pacer.rows + int(info["rows"]), force=True)
    return info


def _export_all_chats(
    copy_dir: Path,
    out_dir: Path,
    staging_dir: Path,
    resolver: _DisplayNameResolver,
    *,
    fmt: str,
    from_ts: int | None,
    to_ts: int | None,
    types: list[str] | None,
    sender: str | None,
    name_mode: str,
    pacer: _ProgressPacer,
    cancel: Callable[[], bool],
    now: float | None,
) -> list[dict[str, object]]:
    """全库导出:普查会话清单 → 逐会话子目录(每会话完成即落位)。

    布局(prd R4):``<out>/聊天记录导出-<YYYYMMDD-HHMMSS>/<会话显示名或id>/``;
    同名显示名撞目录 → 追加序号(不猜归属不覆盖)。
    """
    pacer.tick(phase="scan", rows=0, force=True)
    census = scan_conversations(copy_dir)
    conversations = [
        c for c in census["conversations"] if int(c.get("msg_count") or 0) > 0
    ]
    total_rows_expected = sum(int(c.get("msg_count") or 0) for c in conversations)
    run_dir_name = "聊天记录导出-" + time.strftime(
        "%Y%m%d-%H%M%S", time.localtime(now if now is not None else time.time())
    )
    run_dir = out_dir / run_dir_name
    run_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(run_dir, 0o700)
    taken_dirs: set[str] = set()
    files: list[dict[str, object]] = []
    done_rows = 0
    for conv in conversations:
        chat_id = str(conv["chat_id"])
        base = sanitize_file_name(str(conv.get("display_name") or chat_id))
        dir_name = base
        serial = 2
        while dir_name in taken_dirs:
            dir_name = f"{base}-{serial}"
            serial += 1
        taken_dirs.add(dir_name)
        info = _export_one_chat(
            copy_dir,
            chat_id,
            conv.get("display_name"),
            staging_dir,
            fmt=fmt,
            from_ts=from_ts,
            to_ts=to_ts,
            types=types,
            sender=sender,
            name_mode=name_mode,
            pacer=pacer,
            cancel=cancel,
            resolver=resolver,
            now=now,
            final_dir=run_dir / dir_name,
            staging_prefix=f"{len(files):04d}-",
        )
        info["name"] = f"{dir_name}/{info['name']}"
        files.append(info)
        done_rows += int(info["rows"])
        pct = (
            round(done_rows / total_rows_expected, 4) if total_rows_expected else None
        )
        pacer.tick(phase="chat", rows=done_rows, current_chat=dir_name, pct_est=pct, force=True)
    return files


def _files_time_range(files: list[dict[str, object]]) -> dict[str, int] | None:
    ranges = [f["time_range"] for f in files if f.get("time_range")]
    if not ranges:
        return None
    lo = min(r["from_ts"] for r in ranges)  # type: ignore[index,union-attr]
    hi = max(r["to_ts"] for r in ranges)  # type: ignore[index,union-attr]
    return {"from_ts": lo, "to_ts": hi}


def _write_manifest(
    staging_dir: Path,
    files: list[dict[str, object]],
    *,
    final_dir: Path,
    fmt: str,
    chat_id: str | None,
    display_name: str | None,
    options: dict[str, object],
    total_rows: int,
    time_range: dict[str, int] | None,
) -> Path:
    """manifest.json 最后写(staging → 原子落位;0600;sha256 清单)。"""
    manifest = {
        "format": fmt,
        "chat_id": chat_id,
        "display_name": display_name,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "options": options,
        "files": [
            {
                "name": f["name"],
                "path": f["path"],
                "rows": f["rows"],
                "sha256": f["sha256"],
                "bytes": f["bytes"],
            }
            for f in files
        ],
        "total_rows": total_rows,
        "time_range": time_range,
    }
    staging_manifest = staging_dir / "manifest.json"
    sink = _Sink(staging_manifest)
    try:
        sink.write(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    finally:
        sink.close()
    committed = _commit_file(staging_manifest, final_dir)
    return committed


def run_export_all(**kwargs: Any) -> dict[str, object]:
    """``--all`` 语法糖(run_export(all_chats=True) 直转)。"""
    kwargs["all_chats"] = True
    return run_export(**kwargs)


def verify_manifest(manifest_path: Path) -> dict[str, object]:
    """``--verify`` 对账:重算每件 sha256 + 行数存在性 → ``{"verify": …}``。"""
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, ValueError) as exc:
        raise BridgeError(
            EXIT_USAGE,
            f"manifest 不可读: {manifest_path}({exc})",
            code="usage",
        ) from exc
    results: list[dict[str, object]] = []
    ok = True
    for entry in manifest.get("files", []):
        path = Path(str(entry.get("path") or ""))
        name = str(entry.get("name") or "")
        if not path.is_file():
            results.append({"name": name, "ok": False, "reason": "missing"})
            ok = False
            continue
        digest = _hash_file(path)
        entry_ok = digest == entry.get("sha256")
        results.append(
            {"name": name, "ok": entry_ok, "reason": None if entry_ok else "sha256_mismatch"}
        )
        ok = ok and entry_ok
    return {
        "verify": {
            "manifest_path": str(manifest_path),
            "ok": ok,
            "files": results,
            "total_rows": manifest.get("total_rows"),
        }
    }
