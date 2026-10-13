"""微信统计与报告查询层(task 10-14-wechat-stats-reports R1;纯 SQL 净室)。

对**解密副本**(数据根私有区,``localdb.ensure_decrypted_copies`` 产物,
域 = ``["message", "contact"]``)做纯只读统计分析,四模式:

- **chats**:会话枚举(chat_id/显示名/kind/消息数/首末时间);表名反解
  不出的分表在 ``unattributed_tables`` 如实计数,不静默。
- **chat**:单会话聚合树(总量/方向/类型分桶/时段/活跃日/连续天数/
  高频短语/发言排行/会话切分/响应速度)。
- **annual**:年度报告(单年或全时间;只统计 private kind 私谈集——
  排除系统账号清单,WeFlow isPrivateSession 同语义)。
- **dual**:双人对照(首条消息/我-对方两列/7×24 热度/各自短语与主动性)。

纪律(prd R1/R8,红线同 ``localdb_query`` 同源):

- **零写副本**:所有连接经 ``localdb_query._open_copy``(``mode=ro``
  URI);不建索引不物化。
- **零出网零 AI 零微信进程接触**:本模块无网络 import;短语等文本只进
  stdout 契约载荷,不入日志(argv/stderr 零正文)。
- **单遍聚合原语**:每表一次复合 GROUP BY 扫描(日期/小时/周几/月 ×
  类型 × 发送者)产出全部固定宽度桶(2026-10-14 真副本 355MB 实测:
  249 表私谈集 0.1s、最大单表 111k 行 0.35s;EXPLAIN = SCAN + USE TEMP
  B-TREE FOR GROUP BY,见任务档 implement.jsonl);会话/响应需要相邻
  时序,另走单表有序行游;短语提取另走文本列受控行数流式
  (``fetchmany``,硬帽 20 万行)。
- **桶语义钉死**:hourly 24(`%H`)/weekday 7(SQL `%w` 0=周日 →
  ``((w+6)%7)+1`` 即 1=周一..7=周日)/daily ``YYYY-MM-DD``(localtime)
  /monthly 12(`%m`)。system(10000)/revoke(10002)计入 type_counts
  单列,**不计入 sent/received、不参与响应/会话/短语**;
  human_total = total − system − revoke。active_days = 真
  COUNT(DISTINCT 日期);longest_streak = daily 序列连续有消息日的最长段。
- **type_counts 契约桶**(prd R2):text/image/voice/video/sticker/
  file_or_link/location/other/system/revoke 十桶固定键序;**非清单键一律
  归 other**(2026-10-14 真库实证:存在 244813135921/21474836529 等
  位标志混合型 local_type,落 other 桶如实)。
- **self_id 推导**(4.1.15 无 isSender 列):私聊表内 sender≠该表
  chat_id 的**众数** wxid = 我方(2026-10-14 真库验证:唯一众数
  10,585 票零歧义;私聊收件行 real_sender_id 真携带对方 wxid——调研
  验证案 4 成立,PRD R1 替代规则不启用;反查为空串的行走「无从归因即
  归会话」惯例计对方)。:func:`verify_self_id` 是双路互证诊断件。
- **缓存**(prd R3):<数据根>/wechat-bridge/stats-cache/
  ``<mode>-<sha1(参数+副本指纹+桥版本+契约修订号)>``.json;副本指纹 =
  message_0.db 副本 mtime+size(副本重建即失效);键含桥版本+统计契约
  修订号(设计拷问①裁决:跨版本缓存不互认,type_counts 映射漂移不
  静默);``--refresh`` 旁路重算覆写;缓存文件存**不含 cache/copy 块**
  的载荷(computed_ms 恒随次变化,入文件会破逐字节一致性)。

时间口径注记:窗口过滤在 SQL 层按原始时间列比较(与
``localdb_query.query_messages`` 同一惯例);4.1.15 实况 = 秒级。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import statistics
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from . import __version__ as _BRIDGE_VERSION
from . import localdb, memsearch
from .codes import DECRYPT_FAILED, EXIT_OK, EXIT_USAGE, BridgeError
from .config import BRIDGE_CONFIG_DIR_NAME, load_config, myssia_home
from .localdb_query import (
    MSG_TYPE_NAMES,
    _contact_pick_names,
    _decode_text_content,
    _normalize_ts,
    _open_copy,
    find_message_tables,
    name2id_maps,
)

__all__ = [
    "STATS_CONTRACT_REVISION",
    "TYPE_COUNT_KEYS",
    "SYSTEM_ACCOUNT_IDS",
    "run_stats_query",
    "stats_history",
    "register_cli",
    "dispatch_cli",
    "verify_self_id",
]

#: 统计契约修订号(设计拷问①裁决:缓存键组成部分;桶语义/type 映射/
#: 契约键序任何变更必须 +1,旧缓存自然失效重算)。
STATS_CONTRACT_REVISION = 1

#: 缓存目录名(<数据根>/wechat-bridge/stats-cache/;数据根私有区,零出 git)。
STATS_CACHE_DIR_NAME = "stats-cache"

#: 消息库副本相对路径(主库;biz 为辅,两库并集扫描)。
_MESSAGE_RELS = ("message/message_0.db", "message/biz_message_0.db")
_CONTACT_REL = "contact/contact.db"

#: type_counts 契约十桶(键序即输出序,prd R2 钉死)。
TYPE_COUNT_KEYS: tuple[str, ...] = (
    "text",
    "image",
    "voice",
    "video",
    "sticker",
    "file_or_link",
    "location",
    "other",
    "system",
    "revoke",
)
_CONTRACT_BUCKETS = frozenset(TYPE_COUNT_KEYS)

#: annual 私谈集排除的系统账号(WeFlow isPrivateSession 同语义;gh_*/
#: @chatroom 另按 kind 排除;自己经 self_id 排除)。
SYSTEM_ACCOUNT_IDS = frozenset(
    {"filehelper", "weixin", "weixinteam", "qqmail", "weibo"}
)

#: 会话切分阈值:相邻消息间隔 >30 分钟 = 新会话(prd R1;可翻案缺省)。
SESSION_GAP_SECONDS = 30 * 60
#: 响应速度采样窗:相邻异向消息时间差仅取 ≤24h 的对(prd R1;可翻案缺省)。
RESPONSE_WINDOW_SECONDS = 24 * 3600
#: 高频短语:出现 ≥3 次才入榜、top 20(prd R1)。
PHRASE_MIN_COUNT = 3
PHRASE_TOP_N = 20
#: 短语文本行流式硬帽(单次统计运行全表累计;prd R1)。
PHRASE_ROW_CAP = 200_000
#: dual first_chat 文本截断(字符;prd R2)。
FIRST_CHAT_TEXT_MAX_CHARS = 120

#: 停用词(单字;prd R1:的了是我你吗呢吧哈)。CJK 二元组两字皆停用即弃。
_STOPWORD_CHARS = frozenset("的了是我你吗呢吧哈")

_CJK_RUN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]+")
_LATIN_RUN = re.compile(r"[0-9A-Za-z]+")

#: 结构性噪声剥离(分词前置;2026-10-14 真库实证:大群 89% 文本行内嵌
#: wxid 提及串——不剥则短语榜全是 id 碎片。URL 同理(http/https 刷榜)。
#: 这是 PRD 停用词表之外的工程缺省,与阈值类缺省同为可翻案项)。
_STRUCTURAL_NOISE = re.compile(
    r"wxid_[0-9A-Za-z_-]+|[0-9]+@chatroom|gh_[0-9A-Za-z_-]+|https?://\S+"
)


def _type_bucket(local_type: Any) -> str:
    """local_type → 契约桶名(清单外一律 other;形状异常也归 other 不炸)。"""
    try:
        code = int(local_type)
    except (TypeError, ValueError):
        return "other"
    name = MSG_TYPE_NAMES.get(code)
    if name is not None and name in _CONTRACT_BUCKETS:
        return name
    return "other"


def _is_system_type(local_type: Any) -> bool:
    try:
        return int(local_type) in (10000, 10002)
    except (TypeError, ValueError):
        return False


# =====================================================================
# 表发现与 self_id 推导
# =====================================================================


def _chat_kind(chat_id: str) -> str:
    """会话 id → kind(group/official/system/private;prd R1 词表)。"""
    if chat_id.endswith("@chatroom"):
        return "group"
    if chat_id.startswith("gh_"):
        return "official"
    if chat_id in SYSTEM_ACCOUNT_IDS:
        return "system"
    return "private"


def _is_private_id(chat_id: str) -> bool:
    return _chat_kind(chat_id) == "private"


class _Plan:
    """发现结果:消息库连接 × 表 × 会话归属(反解不出 = None 如实)。"""

    def __init__(self, copy_dir: Path) -> None:
        self.cons: list[sqlite3.Connection] = []
        # entries: (con_idx, table, colmap, chat|None)——宽表(talker 在场)
        # chat=None 但 SQL 层按 talker 过滤;Msg_ 分表 chat=None = 归属不明。
        self.entries: list[tuple[int, str, dict[str, str | None], str | None]] = []
        self.id_to_name: dict[int, str] = {}
        for rel in _MESSAGE_RELS:
            con = _open_copy(copy_dir, rel)
            if con is None:
                continue
            idx = len(self.cons)
            self.cons.append(con)
            for table, colmap in find_message_tables(con):
                if colmap.get("talker"):
                    self.entries.append((idx, table, colmap, None))
                else:
                    self.entries.append((idx, table, colmap, colmap.get("chat")))
        if self.cons and any(
            colmap.get("sender_id") for _i, _t, colmap, _c in self.entries
        ):
            self.id_to_name = name2id_maps(self.cons[0])[0]

    def close(self) -> None:
        for con in self.cons:
            con.close()

    def __enter__(self) -> _Plan:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    @property
    def unattributed_tables(self) -> int:
        """归属不明的 Msg_ 分表数(反解不出;如实计数不静默)。"""
        return sum(
            1
            for _i, _t, colmap, chat in self.entries
            if not colmap.get("talker") and chat is None
        )

    def target_entries(self, chat_id: str) -> list[tuple[int, str, dict[str, str | None]]]:
        """指定会话的表集:宽表(SQL 层 talker 过滤)+ 归属命中的分表。"""
        picked: list[tuple[int, str, dict[str, str | None]]] = []
        for idx, table, colmap, chat in self.entries:
            if colmap.get("talker") or chat == chat_id:
                picked.append((idx, table, colmap))
        return picked

    def resolve_sender(self, raw: Any, chat_id: str) -> str:
        """4.1.15 real_sender_id → Name2Id 反查;反查失败/形状异常/空名
        回落会话 id(「无从归因即归会话」惯例,
        localdb_query._sender_name 同款;真库实证 Name2Id 含空串 user_name
        行,空名不参与 self_id 投票)。"""
        try:
            rid = int(raw)
        except (TypeError, ValueError):
            return chat_id
        name = self.id_to_name.get(rid)
        return name if name else chat_id


def _accumulate_self_id_votes(
    votes: Counter, chat_id: str, sender: str, count: int
) -> None:
    if sender and sender != chat_id:
        votes[sender] += count


def _mode_winner(votes: Counter) -> str | None:
    """众数胜者;并列 = 推导不唯一,如实 None(不掷硬币)。"""
    if not votes:
        return None
    top = votes.most_common()
    if len(top) > 1 and top[0][1] == top[1][1]:
        return None
    return top[0][0]


def _derive_self_id_from_private_tables(plan: _Plan) -> str | None:
    """轻量专扫:私聊表 GROUP BY sender_id 的我方投票(私聊表普遍小,
    2026-10-14 真库实测 161 表 <0.1s;群聊目标需要全局 self_id 时用)。"""
    votes: Counter = Counter()
    for idx, table, colmap, chat in plan.entries:
        if chat is None or not _is_private_id(chat) or not colmap.get("sender_id"):
            continue
        try:
            rows = plan.cons[idx].execute(
                f'SELECT "{colmap["sender_id"]}", COUNT(*) FROM "{table}" GROUP BY 1'
            ).fetchall()
        except sqlite3.Error:
            continue
        for raw, count in rows:
            _accumulate_self_id_votes(
                votes, chat, plan.resolve_sender(raw, chat), int(count or 0)
            )
    return _mode_winner(votes)


def _derive_self_id_from_rows(
    plan: _Plan, chat_id: str, rows: list[tuple[Any, Any, Any]]
) -> str | None:
    """私聊目标表行游内推导(sender≠chat_id 众数;chat/dual 私聊路径)。"""
    if not _is_private_id(chat_id) or not rows:
        return None
    votes: Counter = Counter()
    for _ts, _local_type, sender_raw in rows:
        sender = plan.resolve_sender(sender_raw, chat_id)
        _accumulate_self_id_votes(votes, chat_id, sender, 1)
    return _mode_winner(votes)


def verify_self_id(copy_dir: Path) -> dict[str, Any]:
    """self_id 双路互证诊断(调研验证案 4 的真数据对拍件;只读)。

    路径 A = real_sender_id 反查 + 「≠chat_id 即我方」(4.1.15 主路);
    路径 B = 行级计数一致性核对:私聊表内「反查名≠chat_id」行应显著
    单一众数、「=chat_id」行为对方、空名行为残留。输出计数与判据,
    供 implement.jsonl 留证;不输出任何消息正文。
    """
    with _Plan(copy_dir) as plan:
        votes: Counter = Counter()
        per_chat: list[dict[str, Any]] = []
        for idx, table, colmap, chat in plan.entries:
            if chat is None or not _is_private_id(chat) or not colmap.get("sender_id"):
                continue
            try:
                rows = plan.cons[idx].execute(
                    f'SELECT "{colmap["sender_id"]}", COUNT(*) FROM "{table}" GROUP BY 1'
                ).fetchall()
            except sqlite3.Error:
                continue
            me_rows = other_rows = unattributed_rows = 0
            for raw, count in rows:
                count = int(count or 0)
                sender = plan.resolve_sender(raw, chat)
                if sender == chat:
                    other_rows += count
                elif sender:
                    me_rows += count
                    votes[sender] += count
                else:
                    unattributed_rows += count
            per_chat.append(
                {
                    "chat_id": chat,
                    "me_rows": me_rows,
                    "other_rows": other_rows,
                    "unattributed_rows": unattributed_rows,
                }
            )
        top = votes.most_common(3)
        return {
            "self_id": top[0][0] if top else None,
            "votes_top3": top,
            "private_tables_checked": len(per_chat),
            "agreement": bool(top) and (len(top) < 2 or top[0][1] > top[1][1]),
            "per_chat_shape": per_chat[:5],
        }


# =====================================================================
# 扫描原语(每表一次复合 GROUP BY;行游;文本流)
# =====================================================================


def _group_scan(
    con: sqlite3.Connection,
    table: str,
    colmap: dict[str, str | None],
    from_ts: int,
    to_ts: int,
    *,
    talker: str | None = None,
) -> list[tuple]:
    """单遍复合聚合:GROUP BY(日期,小时,周几,月,类型,发送者[,talker])。

    返回行 = ``(date, hour, weekday_raw, month, local_type, sender_raw,
    count[, talker])``(talker 在场时行尾附加,前七位下标恒稳定)。
    SCAN + TEMP B-TREE(EXPLAIN 留档 implement.jsonl);缺列/形状漂移 =
    空行如实降级。参数按 SQL 文本出现序绑定:talker 占位符在 SELECT
    列表,先于 WHERE 的两个窗口参数。
    """
    tcol = colmap.get("time")
    if not tcol:
        return []
    params: list[object] = []
    selects = [
        f"strftime('%Y-%m-%d', \"{tcol}\", 'unixepoch', 'localtime')",
        f"strftime('%H', \"{tcol}\", 'unixepoch', 'localtime')",
        f"strftime('%w', \"{tcol}\", 'unixepoch', 'localtime')",
        f"strftime('%m', \"{tcol}\", 'unixepoch', 'localtime')",
    ]
    group_cols = [str(i + 1) for i in range(4)]
    if colmap.get("type"):
        selects.append(f'"{colmap["type"]}"')
    else:
        selects.append("1")
    group_cols.append(str(len(selects)))
    sender_col = colmap.get("sender_id") or colmap.get("sender")
    if sender_col:
        selects.append(f'"{sender_col}"')
    else:
        selects.append("NULL")
    group_cols.append(str(len(selects)))
    selects.append("COUNT(*)")
    if talker is not None and colmap.get("talker"):
        selects.append("?")
        group_cols.append(str(len(selects)))
        params.append(talker)
    params.extend([from_ts, to_ts])
    sql = (
        f'SELECT {", ".join(selects)} FROM "{table}" '
        f'WHERE "{tcol}" >= ? AND "{tcol}" < ? '
        f"GROUP BY {', '.join(group_cols)}"
    )
    try:
        return con.execute(sql, params).fetchall()
    except sqlite3.Error:
        return []


def _row_walk(
    con: sqlite3.Connection,
    table: str,
    colmap: dict[str, str | None],
    from_ts: int,
    to_ts: int,
    *,
    talker: str | None = None,
) -> list[tuple[Any, Any, Any]]:
    """有序行游(时间升序):``(ts_raw, local_type, sender_raw)``——会话
    切分/响应速度/首条消息/热度格需要相邻时序,聚合行拿不到。"""
    tcol = colmap.get("time")
    if not tcol:
        return []
    selects = [f'"{tcol}"']
    if colmap.get("type"):
        selects.append(f'"{colmap["type"]}"')
    else:
        selects.append("1")
    sender_col = colmap.get("sender_id") or colmap.get("sender")
    selects.append(f'"{sender_col}"' if sender_col else "NULL")
    sql = f'SELECT {", ".join(selects)} FROM "{table}" WHERE "{tcol}" >= ? AND "{tcol}" < ?'
    params: list[object] = [from_ts, to_ts]
    if talker is not None and colmap.get("talker"):
        sql += f' AND "{colmap["talker"]}" = ?'
        params.append(talker)
    sql += f' ORDER BY "{tcol}" ASC'
    try:
        return con.execute(sql, params).fetchall()
    except sqlite3.Error:
        return []


class _PhraseBudget:
    """短语文本行流式预算(硬帽 20 万行,跨表累计;超帽停读如实)。"""

    def __init__(self, cap: int = PHRASE_ROW_CAP) -> None:
        self.remaining = cap
        self.capped = False


def _stream_phrases(
    con: sqlite3.Connection,
    table: str,
    colmap: dict[str, str | None],
    from_ts: int,
    to_ts: int,
    counter: Counter,
    budget: _PhraseBudget,
    *,
    talker: str | None = None,
    direction: str | None = None,
    chat_id: str = "",
    plan: _Plan | None = None,
    self_id: str | None = None,
) -> None:
    """流式扫 local_type=1 文本行 → 分词计数(fetchmany 批读;硬帽)。

    经 ``_decode_text_content`` 真解码(zstd 解不开/UTF-8 失败落占位并
    跳过——占位不是内容,不进短语);``direction`` 在场时只计该方向的行
    (dual 双列;方向判定与 :func:`_direction` 同一语义,需 plan + chat_id
    + self_id;无发送者列无法归属 → 该列如实零短语,不猜)。"""
    tcol = colmap.get("time")
    type_col = colmap.get("type")
    content_col = colmap.get("content")
    if not (tcol and type_col and content_col):
        return
    selects = [f'"{content_col}"']
    if colmap.get("ct_content"):
        selects.append(f'"{colmap["ct_content"]}"')
    else:
        selects.append("NULL")
    sender_col = colmap.get("sender_id") or colmap.get("sender")
    selects.append(f'"{sender_col}"' if sender_col else "NULL")
    sql = (
        f'SELECT {", ".join(selects)} FROM "{table}" '
        f'WHERE "{tcol}" >= ? AND "{tcol}" < ? AND "{type_col}" = 1'
    )
    params: list[object] = [from_ts, to_ts]
    if talker is not None and colmap.get("talker"):
        sql += f' AND "{colmap["talker"]}" = ?'
        params.append(talker)
    needs_direction = direction is not None
    if needs_direction and not (colmap.get("sender_id") or colmap.get("sender")):
        return  # 无发送者列无法归属 → 该方向如实零短语,不猜
    try:
        cursor = con.execute(sql, params)
    except sqlite3.Error:
        return
    while True:
        batch = cursor.fetchmany(2000)
        if not batch:
            return
        for content, ct_marker, sender_raw in batch:
            if budget.remaining <= 0:
                budget.capped = True
                cursor.close()
                return
            budget.remaining -= 1
            if needs_direction:
                assert plan is not None  # 方向判定需要 Name2Id 映射
                if _direction(plan, colmap, chat_id, sender_raw, self_id) != direction:
                    continue
            _count_phrases(content, ct_marker, counter)


def _count_phrases(content: Any, ct_marker: Any, counter: Counter) -> None:
    """一条文本 → 短语计数(CJK 二元组 + 拉丁词;停用词规则见模块头)。

    压缩/解码失败落占位(非内容)不计;空串不计。"""
    text, placeholder = _decode_text_content(content, ct_marker, None)
    if text is None or not text.strip():
        return
    del placeholder
    text = _STRUCTURAL_NOISE.sub(" ", text)
    if not text.strip():
        return
    for run in _CJK_RUN.findall(text):
        if len(run) < 2:
            continue
        for i in range(len(run) - 1):
            bigram = run[i : i + 2]
            if bigram[0] in _STOPWORD_CHARS and bigram[1] in _STOPWORD_CHARS:
                continue
            counter[bigram] += 1
    for word in _LATIN_RUN.findall(text):
        if len(word) >= 2:
            counter[word.lower()] += 1


def _top_phrases(counter: Counter, top_n: int = PHRASE_TOP_N) -> list[dict[str, Any]]:
    """计数器 → [{'phrase','count'}](≥3 次;(-count, phrase) 定序)。"""
    ranked = sorted(
        ((p, c) for p, c in counter.items() if c >= PHRASE_MIN_COUNT),
        key=lambda item: (-item[1], item[0]),
    )[:top_n]
    return [{"phrase": phrase, "count": count} for phrase, count in ranked]


# =====================================================================
# 聚合装配(纯内存:group 行/行游 → 契约树)
# =====================================================================


def _new_buckets() -> dict[str, Any]:
    return {"hourly": [0] * 24, "weekday": [0] * 7, "monthly": [0] * 12, "daily": {}}


def _absorb_group_row(buckets: dict[str, Any], row: tuple, count: int) -> None:
    """group 行 → 时段桶(weekday 归一 ((w+6)%7)+1 即 1=周一..7=周日)。"""
    d, hour, weekday_raw, month = row[0], row[1], row[2], row[3]
    if isinstance(hour, str) and hour.isdigit() and int(hour) < 24:
        buckets["hourly"][int(hour)] += count
    if isinstance(weekday_raw, str) and weekday_raw.isdigit():
        buckets["weekday"][(int(weekday_raw) + 6) % 7] += count  # %w 0=周日 → 6
    if isinstance(month, str) and month.isdigit() and 1 <= int(month) <= 12:
        buckets["monthly"][int(month) - 1] += count
    if isinstance(d, str) and len(d) == 10:
        buckets["daily"][d] = buckets["daily"].get(d, 0) + count


def _daily_sorted(buckets: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"date": d, "count": buckets["daily"][d]} for d in sorted(buckets["daily"])]


def _longest_streak(dates: list[str]) -> dict[str, Any]:
    """真连续日:日期集 → 最长连续段(含起止;空 = days 0/起止 None)。"""
    if not dates:
        return {"days": 0, "from": None, "to": None}
    ordinals = sorted(date.fromisoformat(d).toordinal() for d in set(dates))
    best_len, best_from, best_to = 1, ordinals[0], ordinals[0]
    run_len, run_start = 1, ordinals[0]
    for prev, cur in zip(ordinals, ordinals[1:]):
        if cur == prev + 1:
            run_len += 1
        else:
            run_len, run_start = 1, cur
        if run_len > best_len:
            best_len, best_from, best_to = run_len, run_start, cur
    return {
        "days": best_len,
        "from": date.fromordinal(best_from).isoformat(),
        "to": date.fromordinal(best_to).isoformat(),
    }


def _type_counts_from(counter: Counter) -> dict[str, int]:
    return {key: int(counter.get(key, 0)) for key in TYPE_COUNT_KEYS}


def _direction(
    plan: _Plan,
    colmap: dict[str, str | None],
    chat_id: str,
    sender_raw: Any,
    self_id: str | None,
) -> str:
    """行方向:旧形态 isSender(1=me);4.1.15 反查名 == self_id = me;
    self_id 缺位(推导不出)一律 other(如实,不臆造)。"""
    if colmap.get("sender"):
        return "me" if sender_raw == 1 else "other"
    sender = plan.resolve_sender(sender_raw, chat_id)
    if self_id and sender == self_id:
        return "me"
    return "other"


def _local_hour_weekday(ts: int) -> tuple[int, int]:
    """本地时 (hour, weekday_index)(weekday_index 0=周一..6=周日)。"""
    lt = time.localtime(ts)
    return lt.tm_hour, lt.tm_wday


def _collect_events(
    plan: _Plan, chat_id: str, from_ts: int, to_ts: int
) -> tuple[list[dict[str, Any]], str | None]:
    """目标会话全部行 → (全局时间排序事件流, self_id)。

    跨表合并后按 ts 排序(会话切分的时序前提)。事件 = {ts, direction,
    human, local_type, sender_raw, table_idx, table, colmap, ts_raw};
    self_id:私聊目标 = 行游内推导(≠chat_id 众数),群聊目标 = 私谈集
    全局轻量专扫;推导不出 = None(方向一律 other,如实不臆造)。"""
    events: list[dict[str, Any]] = []
    targets = plan.target_entries(chat_id)
    walked = {
        (idx, table): _row_walk(
            plan.cons[idx], table, colmap, from_ts, to_ts,
            talker=chat_id if colmap.get("talker") else None,
        )
        for idx, table, colmap in targets
    }
    self_id = None
    if _is_private_id(chat_id):
        for (_idx, _table), rows in walked.items():
            self_id = _derive_self_id_from_rows(plan, chat_id, rows)
            if self_id:
                break
    else:
        self_id = _derive_self_id_from_private_tables(plan)
    for idx, table, colmap in targets:
        for ts_raw, local_type, sender_raw in walked[(idx, table)]:
            events.append(
                {
                    "ts": _normalize_ts(ts_raw),
                    "direction": _direction(plan, colmap, chat_id, sender_raw, self_id),
                    "human": not _is_system_type(local_type),
                    "local_type": local_type,
                    "sender_raw": sender_raw,
                    "table_idx": idx,
                    "table": table,
                    "colmap": colmap,
                    "ts_raw": ts_raw,
                }
            )
    events.sort(key=lambda event: event["ts"])
    return events, self_id


def _session_metrics(
    events: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], list[tuple[int, str]]]:
    """事件流(升序)→ (sessions 块, response 块, [(dt, responder)] 样本)。

    会话:相邻人消息间隔 >30 分钟 = 新会话,initiative = 会话首条非系统
    消息方向;响应:相邻异向人消息时间差 ≤24h 的对,responder = 后者。"""
    sessions_total = me_initiated = other_initiated = 0
    samples: list[tuple[int, str]] = []
    last_ts: int | None = None
    last_dir: str | None = None
    for event in events:
        if not event["human"]:
            continue  # system/revoke 不参与会话/响应(prd R1)
        ts, direction = event["ts"], event["direction"]
        if last_ts is None or (ts - last_ts) > SESSION_GAP_SECONDS:
            sessions_total += 1
            if direction == "me":
                me_initiated += 1
            else:
                other_initiated += 1
        if (
            last_ts is not None
            and last_dir is not None
            and direction != last_dir
            and 0 <= (ts - last_ts) <= RESPONSE_WINDOW_SECONDS
        ):
            samples.append((ts - last_ts, direction))
        last_ts, last_dir = ts, direction
    if samples:
        dts = [dt for dt, _r in samples]
        response = {
            "avg_seconds": int(round(statistics.mean(dts))),
            "median_seconds": int(round(statistics.median(dts))),
            "fastest_seconds": int(min(dts)),
            "pairs": len(samples),
        }
    else:
        response = {
            "avg_seconds": None,
            "median_seconds": None,
            "fastest_seconds": None,
            "pairs": 0,
        }
    sessions = {
        "threshold_minutes": SESSION_GAP_SECONDS // 60,
        "total": sessions_total,
        "me_initiated": me_initiated,
        "other_initiated": other_initiated,
    }
    return sessions, response, samples


def _heatmap_from_events(events: list[dict[str, Any]]) -> list[list[int]]:
    """事件流 → 7×24 热度格(行 = 周一..周日;只计人消息)。"""
    grid = [[0] * 24 for _ in range(7)]
    for event in events:
        if not event["human"]:
            continue
        hour, weekday = _local_hour_weekday(event["ts"])
        grid[weekday][hour] += 1
    return grid


def _display_map(copy_dir: Path, chat_ids: list[str]) -> dict[str, str]:
    con = _open_copy(copy_dir, _CONTACT_REL)
    if con is None:
        return {}
    try:
        return _contact_pick_names(con, chat_ids)
    finally:
        con.close()


# =====================================================================
# 四模式装配
# =====================================================================


def _merge_chat_row(
    chats: dict[str, dict[str, Any]], chat_id: str, count: int, min_ts: Any, max_ts: Any
) -> None:
    entry = chats.setdefault(chat_id, {"count": 0, "first_ts": None, "last_ts": None})
    entry["count"] += count
    first = _normalize_ts(min_ts) if min_ts else None
    last = _normalize_ts(max_ts) if max_ts else None
    if first and (entry["first_ts"] is None or first < entry["first_ts"]):
        entry["first_ts"] = first
    if last and (entry["last_ts"] is None or last > entry["last_ts"]):
        entry["last_ts"] = last


def _assemble_chats(plan: _Plan, copy_dir: Path) -> dict[str, Any]:
    """stats chats:全表(两库)计数 → 会话枚举(消息数降序,再 id 定序)。"""
    chats: dict[str, dict[str, Any]] = {}
    for idx, table, colmap, chat in plan.entries:
        tcol = colmap.get("time")
        if not tcol:
            continue
        if colmap.get("talker"):
            try:
                rows = plan.cons[idx].execute(
                    f'SELECT "{colmap["talker"]}", COUNT(*), '
                    f'MIN("{tcol}"), MAX("{tcol}") FROM "{table}" GROUP BY 1'
                ).fetchall()
            except sqlite3.Error:
                continue
            for talker, count, min_ts, max_ts in rows:
                if isinstance(talker, str) and talker:
                    _merge_chat_row(chats, talker, int(count or 0), min_ts, max_ts)
        elif chat is not None:
            try:
                count, min_ts, max_ts = plan.cons[idx].execute(
                    f'SELECT COUNT(*), MIN("{tcol}"), MAX("{tcol}") FROM "{table}"'
                ).fetchone()
            except sqlite3.Error:
                continue
            _merge_chat_row(chats, chat, int(count or 0), min_ts, max_ts)
    display = _display_map(copy_dir, sorted(chats))
    rows = [
        {
            "chat_id": chat_id,
            "display_name": display.get(chat_id),
            "kind": _chat_kind(chat_id),
            "message_count": data["count"],
            "first_ts": data["first_ts"],
            "last_ts": data["last_ts"],
        }
        for chat_id, data in chats.items()
    ]
    rows.sort(key=lambda row: (-row["message_count"], row["chat_id"]))
    return {"chats": rows, "unattributed_tables": plan.unattributed_tables}


def _sender_label(
    plan: _Plan, colmap: dict[str, str | None], chat_id: str, sender_raw: Any
) -> str:
    """发言排行行标签:4.1.15 = 反查 wxid;旧形态 isSender = 「我」/
    会话 id;无发送者列 = 会话 id(无从归因即归会话)。"""
    if colmap.get("sender_id"):
        return plan.resolve_sender(sender_raw, chat_id)
    if colmap.get("sender"):
        return "我" if sender_raw == 1 else chat_id
    return chat_id


def _assemble_chat(
    plan: _Plan,
    copy_dir: Path,
    chat_id: str,
    from_ts: int,
    to_ts: int,
    window_mode: str,
) -> dict[str, Any]:
    """stats chat:单会话聚合树(私聊/群聊通用;群聊 senders=发言排行)。"""
    type_counter: Counter = Counter()
    buckets = _new_buckets()
    targets = plan.target_entries(chat_id)
    # ① 单遍复合 GROUP BY:固定宽度桶 + 类型分桶
    for idx, table, colmap in targets:
        for row in _group_scan(
            plan.cons[idx], table, colmap, from_ts, to_ts,
            talker=chat_id if colmap.get("talker") else None,
        ):
            count = int(row[6])
            type_counter[_type_bucket(row[4])] += count
            _absorb_group_row(buckets, row, count)
    total = sum(type_counter.values())
    # ② 有序行游:方向/会话/响应/首末/发言排行/self_id
    events, self_id = _collect_events(plan, chat_id, from_ts, to_ts)
    sender_counter: Counter = Counter()
    first_ts: int | None = None
    last_ts: int | None = None
    for event in events:
        if first_ts is None or event["ts"] < first_ts:
            first_ts = event["ts"]
        if last_ts is None or event["ts"] > last_ts:
            last_ts = event["ts"]
        if event["human"]:
            sender_counter[
                _sender_label(plan, event["colmap"], chat_id, event["sender_raw"])
            ] += 1
    sessions, response, _samples = _session_metrics(events)
    # ③ 文本流:高频短语
    phrases: Counter = Counter()
    budget = _PhraseBudget()
    for idx, table, colmap in targets:
        _stream_phrases(
            plan.cons[idx], table, colmap, from_ts, to_ts, phrases, budget,
            talker=chat_id if colmap.get("talker") else None,
        )
    display = _display_map(copy_dir, [chat_id] + list(sender_counter.keys()))
    human_total = total - type_counter.get("system", 0) - type_counter.get("revoke", 0)
    sent = sum(1 for event in events if event["human"] and event["direction"] == "me")
    info: dict[str, Any] = {
        "chat_id": chat_id,
        "display_name": display.get(chat_id),
        "kind": _chat_kind(chat_id),
        "window": {"mode": window_mode, "from_ts": from_ts, "to_ts": to_ts},
        "total": total,
        "sent": sent,
        "received": human_total - sent,
        "human_total": human_total,
        "type_counts": _type_counts_from(type_counter),
        "hourly": buckets["hourly"],
        "weekday": buckets["weekday"],
        "monthly": buckets["monthly"],
        "daily": _daily_sorted(buckets),
        "active_days": len(buckets["daily"]),
        "longest_streak": _longest_streak(list(buckets["daily"].keys())),
        "top_phrases": _top_phrases(phrases),
        "senders": [
            {
                "sender_id": sender,
                "display": display.get(sender, sender),
                "count": count,
            }
            for sender, count in sorted(
                sender_counter.items(), key=lambda item: (-item[1], item[0])
            )
        ],
        "sessions": sessions,
        "response": response,
        "self_id": self_id,
        "first_ts": first_ts,
        "last_ts": last_ts,
    }
    return info


def _local_year_start(year: int) -> int:
    """本地时 1 月 1 日零点 → epoch(mktime 本地时)。"""
    return int(time.mktime((year, 1, 1, 0, 0, 0, 0, 0, -1)))


def _assemble_annual(
    plan: _Plan, copy_dir: Path, year: int | None, now: float
) -> dict[str, Any]:
    """stats annual:私谈集(private kind,系统账号/群/官号排除)聚合。"""
    if year is None:
        from_ts, to_ts = 0, int(now)
    else:
        from_ts, to_ts = _local_year_start(year), _local_year_start(year + 1)
    # years_available:全归属表轻量 MIN/MAX 扫(与窗口无关;UI 年份选择真源)
    years: set[int] = set()
    for idx, table, colmap, chat in plan.entries:
        if chat is None or not colmap.get("time"):
            continue
        try:
            min_ts, max_ts = plan.cons[idx].execute(
                f'SELECT MIN("{colmap["time"]}"), MAX("{colmap["time"]}") FROM "{table}"'
            ).fetchone()
        except sqlite3.Error:
            continue
        for ts in (min_ts, max_ts):
            ts_n = _normalize_ts(ts)
            if ts_n > 0:
                years.add(time.localtime(ts_n).tm_year)
    # 私谈集:每表一次 GROUP BY 扫描 + 窗口 MIN/MAX
    type_counter: Counter = Counter()
    buckets = _new_buckets()
    votes: Counter = Counter()
    per_chat_count: Counter = Counter()
    per_chat_midnight: Counter = Counter()
    per_chat_early: Counter = Counter()
    per_chat_late: Counter = Counter()
    min_first: int | None = None
    max_last: int | None = None
    group_cache: dict[tuple[int, str], list[tuple]] = {}
    private_tables: list[tuple[int, str, dict[str, str | None], str]] = []
    for idx, table, colmap, chat in plan.entries:
        if chat is None or not _is_private_id(chat):
            continue
        private_tables.append((idx, table, colmap, chat))
        group_rows = _group_scan(plan.cons[idx], table, colmap, from_ts, to_ts)
        group_cache[(idx, table)] = group_rows
        for row in group_rows:
            count = int(row[6])
            type_counter[_type_bucket(row[4])] += count
            _absorb_group_row(buckets, row, count)
            per_chat_count[chat] += count
            hour = row[1]
            if isinstance(hour, str) and hour.isdigit() and int(hour) < 6:
                per_chat_midnight[chat] += count
            if colmap.get("sender_id"):
                sender = plan.resolve_sender(row[5], chat)
                _accumulate_self_id_votes(votes, chat, sender, count)
        tcol = colmap.get("time")
        if tcol:
            try:
                min_ts, max_ts = plan.cons[idx].execute(
                    f'SELECT MIN("{tcol}"), MAX("{tcol}") FROM "{table}" '
                    f'WHERE "{tcol}" >= ? AND "{tcol}" < ?',
                    (from_ts, to_ts),
                ).fetchone()
            except sqlite3.Error:
                min_ts = max_ts = None
            chat_first = _normalize_ts(min_ts) if min_ts else None
            chat_last = _normalize_ts(max_ts) if max_ts else None
            if chat_first and (min_first is None or chat_first < min_first):
                min_first = chat_first
            if chat_last and (max_last is None or chat_last > max_last):
                max_last = chat_last
    self_id = _mode_winner(votes)
    total = sum(type_counter.values())
    human_total = total - type_counter.get("system", 0) - type_counter.get("revoke", 0)
    sent = 0
    if self_id:
        for _idx, _table, colmap, chat in private_tables:
            if not colmap.get("sender_id"):
                continue
            for row in group_cache[(_idx, _table)]:
                if (
                    plan.resolve_sender(row[5], chat) == self_id
                    and not _is_system_type(row[4])
                ):
                    sent += int(row[6])
    # friend_contrast 半窗边界:单年 = 7 月 1 日本地零点;全时间 = 观测中点
    if year is not None:
        boundary = int(time.mktime((year, 7, 1, 0, 0, 0, 0, 0, -1)))
    else:
        boundary = (min_first + max_last) // 2 if min_first and max_last else int(now)
    boundary_date = time.strftime("%Y-%m-%d", time.localtime(boundary))
    for _idx, _table, _colmap, chat in private_tables:
        for row in group_cache[(_idx, _table)]:
            d = row[0]
            count = int(row[6])
            if isinstance(d, str) and d < boundary_date:
                per_chat_early[chat] += count
            else:
                per_chat_late[chat] += count
    # 短语:私谈集文本流
    phrases: Counter = Counter()
    budget = _PhraseBudget()
    for idx, table, colmap, _chat in private_tables:
        _stream_phrases(plan.cons[idx], table, colmap, from_ts, to_ts, phrases, budget)
    display = _display_map(copy_dir, sorted(per_chat_count))
    top_chats = [
        {"chat_id": chat_id, "display_name": display.get(chat_id), "count": count}
        for chat_id, count in sorted(
            per_chat_count.items(), key=lambda item: (-item[1], item[0])
        )[:20]
    ]
    midnight_top = None
    if per_chat_midnight:
        mid_chat, mid_count = sorted(
            per_chat_midnight.items(), key=lambda item: (-item[1], item[0])
        )[0]
        midnight_top = {
            "chat_id": mid_chat,
            "display_name": display.get(mid_chat),
            "count": mid_count,
        }
    friend_contrast = [
        {
            "chat_id": chat_id,
            "display_name": display.get(chat_id),
            "early_count": per_chat_early.get(chat_id, 0),
            "late_count": per_chat_late.get(chat_id, 0),
        }
        for chat_id in sorted(
            set(per_chat_early) | set(per_chat_late),
            key=lambda c: (-(per_chat_early.get(c, 0) + per_chat_late.get(c, 0)), c),
        )
    ]
    info: dict[str, Any] = {
        "year": year if year is not None else "all",
        "years_available": sorted(years),
        "total": total,
        "sent": sent,
        "received": human_total - sent,
        "human_total": human_total,
        "type_counts": _type_counts_from(type_counter),
        "hourly": buckets["hourly"],
        "weekday": buckets["weekday"],
        "monthly": buckets["monthly"],
        "active_days": len(buckets["daily"]),
        "longest_streak": _longest_streak(list(buckets["daily"].keys())),
        "chats_count": len(per_chat_count),
        "top_chats": top_chats,
        "top_phrases": _top_phrases(phrases),
        "midnight": {
            "count": sum(per_chat_midnight.values()),
            "top_chat": midnight_top,
        },
        "friend_contrast": friend_contrast,
    }
    return info


def _first_text(
    con: sqlite3.Connection,
    table: str,
    colmap: dict[str, str | None],
    ts_raw: Any,
    talker: str | None,
) -> tuple[Any, Any]:
    """取指定时间戳行的文本列与 CT 标记(首条消息文本;缺列 = (None,None))。"""
    content_col = colmap.get("content")
    tcol = colmap.get("time")
    if not (content_col and tcol):
        return None, None
    ct_col = colmap.get("ct_content")
    ct_expr = f'"{ct_col}"' if ct_col else "NULL"
    sql = (
        f'SELECT "{content_col}", {ct_expr} FROM "{table}" '
        f'WHERE "{tcol}" = ? AND "{colmap.get("type") or "1"}" = 1'
    )
    params: list[object] = [ts_raw]
    if talker is not None and colmap.get("talker"):
        sql += f' AND "{colmap["talker"]}" = ?'
        params.append(talker)
    try:
        row = con.execute(sql, params).fetchone()
    except sqlite3.Error:
        return None, None
    return (row[0], row[1]) if row else (None, None)


def _assemble_dual(
    plan: _Plan,
    copy_dir: Path,
    chat_id: str,
    from_ts: int,
    to_ts: int,
    window_mode: str,
) -> dict[str, Any]:
    """stats dual:双人对照(我/对方两列 + 首条消息 + 7×24 热度格)。"""
    targets = plan.target_entries(chat_id)
    events, self_id = _collect_events(plan, chat_id, from_ts, to_ts)
    # 短语双列(me/other 各自方向;共享行数硬帽;self_id 缺位 = 4.1.15
    # 全落 other 列,如实不猜)
    me_phrases: Counter = Counter()
    other_phrases: Counter = Counter()
    budget = _PhraseBudget()
    for idx, table, colmap in targets:
        talker = chat_id if colmap.get("talker") else None
        _stream_phrases(
            plan.cons[idx], table, colmap, from_ts, to_ts, me_phrases, budget,
            talker=talker, direction="me", chat_id=chat_id, plan=plan, self_id=self_id,
        )
        _stream_phrases(
            plan.cons[idx], table, colmap, from_ts, to_ts, other_phrases, budget,
            talker=talker, direction="other", chat_id=chat_id, plan=plan, self_id=self_id,
        )
    sessions, _response, samples = _session_metrics(events)
    me_response = [dt for dt, responder in samples if responder == "me"]
    other_response = [dt for dt, responder in samples if responder == "other"]
    me_count = sum(1 for e in events if e["human"] and e["direction"] == "me")
    other_count = sum(1 for e in events if e["human"] and e["direction"] == "other")
    # first_chat = 窗口内首条人消息(文本截断 120 字;非文本 = 类型名)
    first_chat: dict[str, Any] | None = None
    for event in events:
        if not event["human"]:
            continue
        text: str | None = None
        if event["local_type"] is not None:
            try:
                is_text = int(event["local_type"]) == 1
            except (TypeError, ValueError):
                is_text = False
            if is_text:
                content, ct = _first_text(
                    plan.cons[event["table_idx"]],
                    event["table"],
                    event["colmap"],
                    event["ts_raw"],
                    chat_id if event["colmap"].get("talker") else None,
                )
                decoded, _placeholder = _decode_text_content(content, ct, None)
                text = decoded
        first_chat = {
            "ts": event["ts"],
            "sender": event["direction"],
            "text": (
                text[:FIRST_CHAT_TEXT_MAX_CHARS]
                if text is not None and text
                else (_type_bucket(event["local_type"]) if text is None else None)
            ),
        }
        break
    dates = {
        time.strftime("%Y-%m-%d", time.localtime(e["ts"]))
        for e in events
        if e["human"]
    }
    display = _display_map(copy_dir, [chat_id])
    info: dict[str, Any] = {
        "chat_id": chat_id,
        "display_name": display.get(chat_id),
        "window": {"mode": window_mode, "from_ts": from_ts, "to_ts": to_ts},
        "first_chat": first_chat,
        "me": {
            "count": me_count,
            "initiated": sessions["me_initiated"],
            "avg_response_seconds": (
                int(round(statistics.mean(me_response))) if me_response else None
            ),
            "top_phrases": _top_phrases(me_phrases),
        },
        "other": {
            "count": other_count,
            "initiated": sessions["other_initiated"],
            "avg_response_seconds": (
                int(round(statistics.mean(other_response))) if other_response else None
            ),
            "top_phrases": _top_phrases(other_phrases),
        },
        "heatmap": _heatmap_from_events(events),
        "longest_streak": _longest_streak(sorted(dates)),
        "active_days": len(dates),
    }
    return info


# =====================================================================
# 缓存(prd R3)与四模式分发
# =====================================================================


def _copy_fingerprint(copy_dir: Path) -> str:
    """副本代次指纹:message_0.db 副本 mtime+size(副本重建即失效)。"""
    path = copy_dir / _MESSAGE_RELS[0]
    try:
        stat = path.stat()
        return f"{int(stat.st_mtime)}:{stat.st_size}"
    except OSError:
        return "missing"


def _cache_key(mode: str, params: dict[str, Any], fingerprint: str) -> str:
    """缓存键:sha1(参数 + 副本指纹 + 桥版本 + 统计契约修订号)。"""
    material = json.dumps(
        {
            "mode": mode,
            "params": params,
            "fingerprint": fingerprint,
            "bridge_version": _BRIDGE_VERSION,
            "stats_contract_revision": STATS_CONTRACT_REVISION,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"{mode}-{hashlib.sha1(material.encode('utf-8')).hexdigest()}"


def _cache_load(cache_dir: Path, key: str) -> dict[str, Any] | None:
    try:
        payload = json.loads((cache_dir / f"{key}.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def _cache_store(cache_dir: Path, key: str, payload: dict[str, Any]) -> None:
    """落缓存(tmp+rename 原子写;载荷不含 cache/copy 块——computed_ms 恒
    随次变化,入文件会破「同键重算逐字节一致」;写失败不拦主路)。"""
    try:
        cache_dir.mkdir(parents=True, exist_ok=True)
        tmp = cache_dir / f"{key}.json.tmp"
        tmp.write_text(
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
        tmp.replace(cache_dir / f"{key}.json")
    except OSError:
        return


def _window_of(
    since_days: int | None, all_time: bool, now: float
) -> tuple[int, int, str]:
    if all_time or since_days is None:
        return 0, int(now), "all"
    return int(now) - int(since_days) * 86400, int(now), "since"


def run_stats_query(
    *,
    copy_dir: Path,
    mode: str,
    chat_id: str | None = None,
    since_days: int | None = None,
    year: int | None = None,
    all_time: bool = False,
    refresh: bool = False,
    cache_dir: Path | None = None,
    now: float | None = None,
) -> dict[str, Any]:
    """四模式装配 + 文件缓存(查询层降级 = 空结构,恒不抛业务错)。

    返回 = 契约载荷(``{"stats_chats": …}`` 等;cache 块在最后)。
    ``computed_ms`` 计纯装配耗时(缓存命中 = 读缓存耗时)。"""
    current = time.time() if now is None else now
    params = {
        "chat_id": chat_id,
        "since_days": since_days,
        "year": year,
        "all_time": all_time,
    }
    key = _cache_key(mode, params, _copy_fingerprint(copy_dir))
    started = time.monotonic()
    if not refresh and cache_dir is not None:
        cached = _cache_load(cache_dir, key)
        if cached is not None:
            inner = dict(cached)
            inner["cache"] = {
                "hit": True,
                "computed_ms": int((time.monotonic() - started) * 1000),
            }
            return {f"stats_{mode}": inner}
    from_ts, to_ts, window_mode = _window_of(since_days, all_time, current)
    with _Plan(copy_dir) as plan:
        if mode == "chats":
            inner = _assemble_chats(plan, copy_dir)
        elif mode == "chat":
            inner = _assemble_chat(
                plan, copy_dir, str(chat_id or ""), from_ts, to_ts, window_mode
            )
        elif mode == "annual":
            inner = _assemble_annual(plan, copy_dir, year, current)
        elif mode == "dual":
            inner = _assemble_dual(
                plan, copy_dir, str(chat_id or ""), from_ts, to_ts, window_mode
            )
        else:  # pragma: no cover - 词表封闭,CLI 层已拦
            raise BridgeError(EXIT_USAGE, f"未知 stats 模式 {mode!r}", code="usage")
    computed_ms = int((time.monotonic() - started) * 1000)
    if cache_dir is not None:
        _cache_store(cache_dir, key, inner)
    inner["cache"] = {"hit": False, "computed_ms": computed_ms}
    return {f"stats_{mode}": inner}


# =====================================================================
# 编排(E2 副本 → 查询层;group_info 判例同款)与 CLI 接缝
# =====================================================================


def stats_history(
    config,  # BridgeConfig(运行时鸭子类型,防循环导入惯例)
    db_storage: Path,
    keys: dict[str, str],
    mode: str,
    *,
    chat_id: str | None = None,
    since_days: int | None = None,
    year: int | None = None,
    all_time: bool = False,
    refresh: bool = False,
    data_root: Path | None = None,
    now: float | None = None,
) -> dict[str, Any]:
    """``localdb stats`` 全链编排:E2 副本(域 ``["message","contact"]``)→
    自愈钩子(group_info 判例同款)→ :func:`run_stats_query` 装配 + 缓存。

    chats 模式附 ``copy`` 形状节(契约 v1);查询层缺表/缺列/空库恒降级
    空结构不判错(判例同 key-status:状态查询不判错)。"""
    domains = ["message", "contact"]

    def _ensure(keys_mapping: dict[str, str]) -> dict[str, object]:
        return localdb.ensure_decrypted_copies(
            db_storage,
            keys_mapping,
            domains=domains,
            ttl_hours=config.copy_ttl_hours,
            capacity_mb=config.copy_capacity_mb,
            data_root=data_root,
            now=now,
        )

    try:
        copy_info = _ensure(keys)
    except BridgeError as exc:
        if exc.exit_code != DECRYPT_FAILED:
            raise
        if not memsearch.self_heal_armed(config=config, data_root=data_root):
            raise
        healed = memsearch.try_self_heal(db_storage, config=config, data_root=data_root)
        if healed is None:
            raise
        keys = healed
        copy_info = _ensure(keys)

    root = data_root if data_root is not None else myssia_home()
    payload = run_stats_query(
        copy_dir=Path(str(copy_info["dir"])),
        mode=mode,
        chat_id=chat_id,
        since_days=since_days,
        year=year,
        all_time=all_time,
        refresh=refresh,
        cache_dir=root / BRIDGE_CONFIG_DIR_NAME / STATS_CACHE_DIR_NAME,
        now=now,
    )
    if mode == "chats":
        payload["stats_chats"]["copy"] = copy_info
    return payload


def _emit(payload: dict[str, Any]) -> None:
    """stdout 单个 JSON 对象(cli._emit 同格式;键序稳定)。"""
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=1)
    sys.stdout.write("\n")


def _parse_since_days(raw: str) -> int:
    """``--since Nd`` → 天数(cli._parse_since_days 同语义严格形态;本地
    复刻避免 cli ↔ stats_query 循环导入)。"""
    value = raw.strip().lower()
    if not value.endswith("d") or not value[:-1].isdigit() or int(value[:-1]) <= 0:
        raise BridgeError(
            EXIT_USAGE,
            f"--since 须为 '<N>d' 形态且 N 为正整数(如 7d),当前为 {raw!r}",
            code="usage",
        )
    return int(value[:-1])


def _add_window_args(node: argparse.ArgumentParser) -> None:
    node.add_argument(
        "--since", default=None, metavar="Nd",
        help="历史窗口(天;形如 30d;与 --all 互斥,缺一不可)",
    )
    node.add_argument(
        "--all", action="store_true", default=False, help="全时间(与 --since 互斥)"
    )
    node.add_argument(
        "--refresh", action="store_true", default=False, help="跳过文件缓存强制重算"
    )


def register_cli(localdb_sub: argparse.ArgumentParser) -> list[argparse.ArgumentParser]:
    """挂 ``localdb stats`` 四子命令(返回节点清单供 cli.py 的 --json/
    --config 逐层重注册循环并入;集成接线见任务档 integrationSpec)。"""
    stats = localdb_sub.add_parser(
        "stats",
        help="统计与报告(chats=会话枚举 / chat=单会话 / annual=年度 / dual=双人)",
    )
    stats_sub = stats.add_subparsers(dest="stats_cmd", required=True)
    chats = stats_sub.add_parser("chats", help="会话枚举(消息数/首末时间/kind)")
    chats.add_argument(
        "--refresh", action="store_true", default=False, help="跳过文件缓存强制重算"
    )
    chat = stats_sub.add_parser("chat", help="单会话聚合树(私聊/群聊通用)")
    chat.add_argument("chat_id", metavar="chat", help="目标会话 id")
    _add_window_args(chat)
    annual = stats_sub.add_parser("annual", help="年度报告(单年或全时间)")
    annual.add_argument("--year", type=int, default=None, metavar="N", help="统计年份(如 2025)")
    annual.add_argument("--all", action="store_true", default=False, help="全时间(与 --year 互斥)")
    annual.add_argument("--refresh", action="store_true", default=False, help="跳过文件缓存强制重算")
    dual = stats_sub.add_parser("dual", help="双人对照(私聊我-对方两列)")
    dual.add_argument("chat_id", metavar="chat", help="目标私聊 id")
    _add_window_args(dual)
    return [stats, chats, chat, annual, dual]


def dispatch_cli(args: argparse.Namespace, config_path: Path | None) -> int:
    """``localdb stats`` 分发(cli.py 集成分支的唯一调用点;自带 JSON emit
    与 BridgeError 兜底,exit 码契约同 group-info:查询层降级恒 0,密钥链
    20/21/22 结构化 error 非 0)。"""
    try:
        config = load_config(config_path)
        mode = args.stats_cmd
        chat_id: str | None = None
        since_days: int | None = None
        year: int | None = None
        all_time = False
        if mode in ("chat", "dual"):
            value = (args.chat_id or "").strip()
            if not value:
                raise BridgeError(EXIT_USAGE, "会话 id 不可为空白", code="usage")
            chat_id = value
            if bool(args.since) == bool(args.all):
                raise BridgeError(
                    EXIT_USAGE,
                    "--since Nd 与 --all 二选一(互斥且缺一不可)",
                    code="usage",
                )
            if args.since:
                since_days = _parse_since_days(args.since)
            else:
                all_time = True
        elif mode == "annual":
            if (args.year is not None) == bool(args.all):
                raise BridgeError(
                    EXIT_USAGE,
                    "--year N 与 --all 二选一(互斥且缺一不可)",
                    code="usage",
                )
            if args.year is not None:
                if not 1970 <= args.year <= 9999:
                    raise BridgeError(
                        EXIT_USAGE,
                        f"--year 须为 1970..9999 的年份,当前为 {args.year}",
                        code="usage",
                    )
                year = args.year
            else:
                all_time = True
        storage = localdb.locate_db_storage()
        keys = localdb.resolve_keys(storage, config=config)
        _emit(
            stats_history(
                config,
                storage,
                keys,
                mode,
                chat_id=chat_id,
                since_days=since_days,
                year=year,
                all_time=all_time,
                refresh=bool(getattr(args, "refresh", False)),
            )
        )
        return EXIT_OK
    except BridgeError as exc:
        _emit({"error": exc.to_payload()})
        return exc.exit_code
