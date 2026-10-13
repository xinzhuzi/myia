#!/usr/bin/env python3
"""10-14-wechat-contacts 真库 AC 复核脚本(只读;复查员可直接跑)。

对活解密副本(``~/Library/Application Support/MYIA/wechat-localdb/decrypted``)
跑 AC1/AC2/AC3 的对拍:判定闭包 / 游标零重漏 / keyword 对拍 / invalid_cursor /
Tier 分层 / 严判据对照 / stranger·room_verify。**零写入零微信进程接触**
(sqlite3 URI mode=ro);CLI 面未接线(集成批落位),本脚本直驱查询层
contacts_page——集成后等价命令 = ``python -m wechat_bridge localdb contacts
--json``(同层装配)。

用法(仓库根):
    python3 .trellis/tasks/10-14-wechat-contacts/research/realdb_ac_check.py

输出:逐项 PASS/FAIL(FAIL 任一项 = exit 1)。数字是活副本时点值(库随
微信使用漂移,AC 以「同刻对拍一致」为准,prd 实测者注)。
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "plugins" / "wechat-bridge"))

from wechat_bridge.codes import BridgeError  # noqa: E402
from wechat_bridge.contacts_query import contacts_page  # noqa: E402

COPY = Path.home() / "Library/Application Support/MYIA/wechat-localdb/decrypted"
CONTACT = f"file:{COPY}/contact/contact.db?mode=ro"
MESSAGE = f"file:{COPY}/message/message_0.db?mode=ro"

failures: list[str] = []


def check(name: str, ok: bool, detail: str) -> None:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}: {detail}")
    if not ok:
        failures.append(name)


def rocon(uri: str) -> sqlite3.Connection:
    return sqlite3.connect(uri, uri=True)


# ---------------------------------------------------------------- AC1 判定闭包
view = contacts_page(COPY, limit=1)["contacts"]
counts = view["counts"]
con = rocon(CONTACT)
(total,) = con.execute("SELECT COUNT(*) FROM contact").fetchone()
bucket_sum = sum(counts.values())
check("AC1 六桶加和 == COUNT(*)", bucket_sum == total, f"sum={bucket_sum} total={total}")

gh = "username NOT LIKE 'gh\\_%' ESCAPE '\\'"
person = (
    "username NOT IN ('medianote','floatbottle','qmessage','qqmail','fmessage',"
    "'weixin','weixinigram','weixin_team')"
)
for bucket, where in {
    "system": "username IN ('medianote','floatbottle','qmessage','qqmail',"
    "'fmessage','weixin','weixinigram','weixin_team')",
    "group": "username LIKE '%@chatroom'",
    "official": "username LIKE 'gh\\_%' ESCAPE '\\'",
    "former": f"{person} AND username NOT LIKE '%@chatroom' AND {gh} "
    "AND local_type = 3 AND COALESCE(nick_name,'') <> ''",
    "friend": f"{person} AND username NOT LIKE '%@chatroom' AND {gh} AND local_type = 1",
}.items():
    (expected,) = con.execute(f"SELECT COUNT(*) FROM contact WHERE {where}").fetchone()
    check(f"AC1 桶[{bucket}] 同刻对拍", counts[bucket] == expected,
          f"module={counts[bucket]} sql={expected}")
# other = 余数闭包
expected_other = total - sum(counts[b] for b in ("system", "group", "official", "former", "friend"))
check("AC1 桶[other] 余数闭包", counts["other"] == expected_other,
      f"module={counts['other']} residual={expected_other}")
check("AC1 degraded 空(健康)", view["degraded"] == [], f"degraded={view['degraded']}")

# ---------------------------------------------------------------- AC2 分页与过滤
for bucket in ("official", "friend"):
    seen: list[str] = []
    cursor = None
    while True:
        page = contacts_page(COPY, type_filter=bucket, limit=100, cursor=cursor)["contacts"]
        seen.extend(row["username"] for row in page["rows"])
        cursor = page["next_cursor"]
        if not page["has_more"]:
            break
    check(f"AC2 桶[{bucket}] 游标全量翻页零重漏",
          len(seen) == len(set(seen)) == counts[bucket],
          f"rows={len(seen)} unique={len(set(seen))} count={counts[bucket]}")

keyword = "微信"
kw_where = (
    f"{person} AND (remark LIKE ? OR nick_name LIKE ? OR alias LIKE ? "
    "OR username LIKE ? OR quan_pin LIKE ?)"
)
(expected_kw,) = con.execute(
    f"SELECT COUNT(*) FROM contact WHERE {kw_where}", [f"%{keyword}%"] * 5
).fetchone()
kw_rows = contacts_page(COPY, keyword=keyword, limit=0)["contacts"]["rows"]
kw_names = {row["username"] for row in kw_rows}
sql_names = {
    row[0]
    for row in con.execute(f"SELECT username FROM contact WHERE {kw_where}", [f"%{keyword}%"] * 5)
}
# 注:system 桶按契约①不出行(手写 SQL 已用 person 域排除「微信团队」
# 等系统号命中),对拍口径 = 可见五桶。
check("AC2 keyword 五列 LIKE 对拍", kw_names == sql_names,
      f"rows={len(kw_rows)} sql={expected_kw}")

try:
    contacts_page(COPY, type_filter="friend", cursor=contacts_page(COPY, limit=1)
                  ["contacts"]["next_cursor"] or "")
    check("AC2 invalid_cursor 串筛选守卫", False, "未抛")
except BridgeError as exc:
    check("AC2 invalid_cursor 串筛选守卫",
          exc.code == "invalid_cursor" and exc.exit_code == 2,
          f"code={exc.code} exit={exc.exit_code}")

con.close()

# ---------------------------------------------------------------- AC3 考古分层
residued = contacts_page(COPY, with_residue=True, type_filter="former", limit=1)["contacts"]
con, msg = rocon(CONTACT), rocon(MESSAGE)
former_sql = {
    row[0]
    for row in con.execute(
        f"SELECT username FROM contact WHERE {person} AND username NOT LIKE '%@chatroom' "
        f"AND {gh} AND local_type = 3 AND COALESCE(nick_name,'') <> ''"
    )
}
name2id = {row[0] for row in msg.execute("SELECT user_name FROM Name2Id")}
expected_a = len(former_sql & name2id)
tiers = residued["former_tiers"] or {}
check("AC3 Tier 对拍(候选 ∩ Name2Id)",
      tiers.get("msg_residue") == expected_a
      and tiers.get("table_only") == len(former_sql) - expected_a,
      f"tierA={tiers.get('msg_residue')} expected={expected_a} "
      f"tierB={tiers.get('table_only')} expected={len(former_sql) - expected_a}")

(strict,) = con.execute(
    f"SELECT COUNT(*) FROM contact WHERE {person} AND username NOT LIKE '%@chatroom' "
    f"AND {gh} AND ((local_type = 0 AND COALESCE(quan_pin,'') <> '') "
    "OR (local_type = 3 AND COALESCE(flag,0) <> 4 AND (COALESCE(quan_pin,'') <> '' "
    "OR COALESCE(alias,'') <> '' OR COALESCE(remark,'') <> '')))"
).fetchone()
check("AC3 strict_residual_count 对拍(WeFlow 式人集作用域)",
      residued["strict_residual_count"] == strict,
      f"module={residued['strict_residual_count']} sql={strict}")

# 逐行 evidence 抽查:取一个 Tier A 用户名拉满其页
sample_a = sorted(former_sql & name2id)[0]
full = contacts_page(COPY, with_residue=True, type_filter="former", limit=0)["contacts"]["rows"]
row_a = next((row for row in full if row["username"] == sample_a), None)
check("AC3 evidence 抽查(Tier A 行含 msg_residue)",
      row_a is not None and "msg_residue" in row_a["evidence"],
      f"username={sample_a[:16]}… evidence={row_a['evidence'] if row_a else None}")

(stranger_rows,) = con.execute("SELECT COUNT(*) FROM stranger").fetchone()
(rv_rows,) = con.execute("SELECT COUNT(*) FROM room_verify_application").fetchone()
check("AC3 stranger/room_verify 如实",
      len(residued["stranger"]) == stranger_rows
      and residued["room_verify"] == {"present": True, "rows": rv_rows},
      f"stranger={len(residued['stranger'])}/{stranger_rows} room_verify={residued['room_verify']}")
con.close()
msg.close()

print()
if failures:
    print(f"共 {len(failures)} 项 FAIL: {failures}")
    sys.exit(1)
print("全部 PASS(活副本同刻对拍一致;数字随库漂移,以一致性为准)")
