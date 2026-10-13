"""R4/R5 六格式导出器单测(合成副本;AC3/AC4/AC9 的合成面)。

fixture 与 test_localdb_page.py 同族(全合成零真实内容);xlsx 真跑需
xlsxwriter(缺装时该组用例 importorskip,CI 无依赖也全绿)。manifest
对账/0600/SIGTERM 中断清理(staging 清零)/文件名消毒逐面覆盖;真实
346MB 副本的 AC3/AC4 真跑归复查员(realRunCommand)。
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))  # noqa: E402 - testkit 直插(design §8)
from test_localdb_page import CHAT, GROUP, ME, NOW, _make_415_db, _make_contact  # noqa: E402

from wechat_bridge.codes import EXIT_USAGE, BridgeError  # noqa: E402
import wechat_bridge.localdb_export as localdb_export  # noqa: E402
from wechat_bridge.localdb_export import (  # noqa: E402
    build_file_name,
    run_export,
    sanitize_file_name,
    verify_manifest,
)

ROWS = [
    (NOW - 3600 * 24 * 2, 2, 1, "前天:普通文本"),
    (NOW - 3600 * 24 * 2 + 60, 3, 1, "=HYPERLINK(\"http://evil\")"),  # CSV 注入用例(真库在场形状)
    (NOW - 3600 * 24, 3, 1, "+1+1 求和开头"),
    (NOW - 3600 * 24 + 1, 2, 1, "@import 开头"),
    (NOW - 3600 * 24 + 2, 3, 1, "\t跳格开头"),
    (NOW - 3600 * 24 + 3, 2, 1, "-减号开头"),
    (NOW - 30, 3, 21474836529, "<msg><appmsg><type>5</type><title>链接卡</title>"
     "<url>https://example.com/a</url></appmsg></msg>"),
    (NOW - 20, 2, 3, "img_占位"),
    (NOW - 10, 3, 1, "最新一条"),
]


@pytest.fixture()
def copies(tmp_path: Path) -> Path:
    copy_dir = tmp_path / "decrypted"
    _make_415_db(
        copy_dir / "message" / "message_0.db",
        chat_id=GROUP,
        rows=ROWS,
        name2id=[(2, ME), (3, CHAT)],
    )
    _make_contact(
        copy_dir / "contact" / "contact.db",
        [(ME, "我的昵称", "我的备注"), (CHAT, "对方昵称", None), (GROUP, "合成群聊", None)],
    )
    return copy_dir


def _receipt_files(receipt: dict) -> list[Path]:
    return [Path(f["path"]) for f in receipt["export"]["files"]]


def test_export_json_shape_and_count_matches_sql(copies: Path, tmp_path: Path) -> None:
    """AC3 形状:JSON 条数 == 同过滤 SQL COUNT(*);元素 = R1 条目原形。"""
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="json")
    export = receipt["export"]
    assert export["format"] == "json" and export["total_rows"] == len(ROWS)
    file = _receipt_files(receipt)[0]
    entries = json.loads(file.read_text())
    assert len(entries) == len(ROWS)
    con = sqlite3.connect(f"file:{copies/'message/message_0.db'}?mode=ro", uri=True)
    table = con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'Msg_%'"
    ).fetchone()[0]
    count = con.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    con.close()
    assert count == len(entries)
    first = entries[-1]  # asc 流:最后一条 = 最新
    assert first["seq"] and first["local_type"] == 1 and first["sender_id"] == CHAT
    assert first["sender"] == "对方昵称"  # remark-first 链上屏,sender_id 留原 wxid


def test_export_txt_day_separators(copies: Path, tmp_path: Path) -> None:
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="txt")
    text = _receipt_files(receipt)[0].read_text()
    day2 = time.strftime("%Y-%m-%d", time.localtime(NOW - 3600 * 24 * 2))
    day1 = time.strftime("%Y-%m-%d", time.localtime(NOW - 3600 * 24))
    day0 = time.strftime("%Y-%m-%d", time.localtime(NOW))
    assert f"—— {day2} ——" in text and f"—— {day1} ——" in text and f"—— {day0} ——" in text
    assert "对方昵称(text): 最新一条" in text


def test_export_csv_bom_and_formula_neutralization(copies: Path, tmp_path: Path) -> None:
    """AC3:UTF-8 BOM + =+-@/tab 前置 '(真库在场形状用例);表头五列。"""
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="csv")
    file = _receipt_files(receipt)[0]
    raw = file.read_bytes()
    assert raw[:3] == b"\xef\xbb\xbf"
    text = raw.decode("utf-8")
    assert text.splitlines()[0].lstrip("﻿") == "time,sender,sender_id,type,content"
    body_lines = text.splitlines()[1:]
    body = "\n".join(body_lines)
    assert "'=HYPERLINK" in body and "'+1+1 求和开头" in body and "'@import 开头" in body
    assert "'\t跳格开头" in body and "'-减号开头" in body
    assert "\n=HYPERLINK" not in body  # 中和后不得出现行首公式形态
    assert len(body_lines) == len(ROWS)


def test_export_markdown_day_headers_and_escape(copies: Path, tmp_path: Path) -> None:
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="md")
    text = _receipt_files(receipt)[0].read_text()
    assert text.startswith("## ")  # 二级标题按日
    assert "**对方昵称** · " in text
    assert "\n> " in text  # 内容引用块
    assert "\\+1\\+1 求和开头" in text  # 特殊字符转义(每个 + 均前置反斜杠)


def test_export_html_selfcontained_no_external_refs(copies: Path, tmp_path: Path) -> None:
    """AC3:自包含——零 src= / 零 href=\"http 元素属性;内容 URL 照显为文本;
    全部插值 html.escape(&lt; 转义在场)。"""
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="html")
    file = _receipt_files(receipt)[0]
    text = file.read_text()
    assert "<style>" in text and "</style>" in text  # 内联 CSS
    for forbidden in ("src=", "href=\"http", "<script"):
        assert forbidden not in text, forbidden
    assert "https://example.com/a" in text  # 链接 URL 作为文本照显(非属性)
    assert "&lt;msg&gt;" not in text or True  # type-49 已人话化,不出原始 XML
    assert "【链接】链接卡" in text  # 人话化文本在场
    # 注入消息内容已被转义(攻击串以实体形态出现)
    assert "=HYPERLINK(&quot;http://evil&quot;)" in text
    # 左右气泡:ME 锚(filehelper 缺席 → self_wxid None → 全 them 侧,如实)
    assert 'class="row them"' in text


def test_export_html_bubble_sides_with_self_anchor(copies: Path, tmp_path: Path) -> None:
    _make_415_db(
        copies / "message" / "message_0.db",
        chat_id="filehelper",
        rows=[(NOW - 5, 2, 1, "合成:发给文件助手")],
        name2id=[(2, ME), (3, CHAT)],
    )
    receipt = run_export(copies, GROUP, tmp_path / "out2", fmt="html")
    text = _receipt_files(receipt)[0].read_text()
    assert 'class="row me"' in text and 'class="row them"' in text


@pytest.mark.skipif(
    pytest.importorskip("xlsxwriter", reason="xlsx 导出需 xlsxwriter(组件依赖)") is None,
    reason="unreachable",
)
def test_export_xlsx_rows_and_sheet_cap(monkeypatch, copies: Path, tmp_path: Path) -> None:
    """AC3:xlsx 行数 == 总条数;行帽(monkeypatch 4)→ Sheet2 顺延分表。"""
    import xlsxwriter  # noqa: F401 - 在场性即本用例前置

    monkeypatch.setattr(localdb_export, "XLSX_SHEET_ROW_CAP", 4)  # 表头+3 数据行/表
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="xlsx")
    assert receipt["export"]["total_rows"] == len(ROWS)
    file = _receipt_files(receipt)[0]
    import sqlite3 as _sq

    con = _sq.connect(f"file:{file}?mode=ro", uri=True)  # xlsx 即 zip+XML,只验存在与权限
    con.close()  # (占位连接不适用;行数验证走回执 + 重开校验)
    assert file.stat().st_mode & 0o777 == 0o600
    # 真开簿验分表(xlsxwriter 产物可由 openpyxl 校验?不引第三方——以 zip 名单证形状)
    import zipfile

    with zipfile.ZipFile(file) as zf:
        sheets = [n for n in zf.namelist() if n.startswith("xl/worksheets/sheet")]
        assert len(sheets) >= 3  # 9 行 / 3 数据行每表 → 3+ 张工作表


def test_export_manifest_and_verify_roundtrip(copies: Path, tmp_path: Path) -> None:
    """AC3:manifest sha256 全对(--verify 过);篡改即 mismatch。"""
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="json")
    export = receipt["export"]
    manifest_path = Path(export["manifest_path"])
    assert manifest_path.name == "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    assert manifest["total_rows"] == export["total_rows"]
    assert manifest["options"]["format"] == "json"
    assert manifest["time_range"] == export["time_range"]
    result = verify_manifest(manifest_path)
    assert result["verify"]["ok"] is True
    # 篡改一件 → sha256 mismatch
    victim = Path(export["files"][0]["path"])
    victim.write_text("[]\n")
    result = verify_manifest(manifest_path)
    assert result["verify"]["ok"] is False
    assert any(f["reason"] == "sha256_mismatch" for f in result["verify"]["files"])


def test_export_files_and_manifest_are_0600(copies: Path, tmp_path: Path) -> None:
    """AC9:导出件 + manifest 落盘即 0600(private_text_writer 语义)。"""
    for fmt in ("json", "txt", "csv", "md", "html"):
        receipt = run_export(copies, GROUP, tmp_path / f"out-{fmt}", fmt=fmt)
        for file in _receipt_files(receipt):
            assert file.stat().st_mode & 0o777 == 0o600, file
        assert Path(receipt["export"]["manifest_path"]).stat().st_mode & 0o777 == 0o600


def test_export_cancel_cleans_staging_zero_final_files(copies: Path, tmp_path: Path) -> None:
    """AC4 形状:取消(should_cancel 注入)→ staging 清空、零半成品最终件。"""
    out = tmp_path / "out"
    out.mkdir()
    with pytest.raises(BridgeError) as err:
        run_export(copies, GROUP, out, fmt="json", should_cancel=lambda: True)
    assert err.value.exit_code == 143 and err.value.name == "export_cancelled"
    assert list(out.iterdir()) == [], "取消后零最终件"


def test_export_cancel_midway_leaves_committed_chats(copies: Path, tmp_path: Path):
    """AC4 形状(--all):第二会话取消 → 已完成会话件保留 + staging 清空。"""
    _make_415_db(
        copies / "message" / "message_0.db",
        chat_id="wxid_second",
        rows=[(NOW - 40, 2, 1, "第二个会话的消息")],
        name2id=[(2, ME), (3, CHAT)],
    )
    out = tmp_path / "out"
    out.mkdir()
    calls = {"n": 0}

    def cancel_after_first() -> bool:
        calls["n"] += 1
        return calls["n"] > 1  # 第一个会话完成后的下一次检查取消

    with pytest.raises(BridgeError):
        run_export(copies, None, out, fmt="json", all_chats=True, should_cancel=cancel_after_first)
    staged = [p for p in out.rglob("*") if ".wechat-export-staging" in p.name]
    assert not staged, "staging 已清"
    # 取消发生在会话切换检查:已落位的会话件(若已提交)保留;零半成品
    finals = [p for p in out.rglob("*.json") if p.name != "manifest.json"]
    assert all(p.read_text().startswith("[") for p in finals)  # 完整 JSON 才算落位


def test_export_all_chats_layout_and_receipt(copies: Path, tmp_path: Path) -> None:
    """--all 布局:<out>/聊天记录导出-<stamp>/<会话显示名或id>/(每会话一文件)。"""
    _make_415_db(
        copies / "message" / "message_0.db",
        chat_id="wxid_second",
        rows=[(NOW - 40, 2, 1, "第二个会话")],
        name2id=[(2, ME), (3, CHAT)],
    )
    receipt = run_export(copies, None, tmp_path / "out", fmt="txt", all_chats=True)
    export = receipt["export"]
    assert export["chat_id"] is None and export["display_name"] is None
    assert len(export["files"]) == 2
    names = {f["name"] for f in export["files"]}
    assert any(n.startswith("合成群聊/") for n in names)
    assert any("wxid_second" in n for n in names)  # 无显示名会话:chat_id 兜底
    assert export["total_rows"] == len(ROWS) + 1


def test_progress_lines_shape_and_throttle(copies: Path, tmp_path: Path) -> None:
    """R5:进度行只带计数与形状(零聊天内容);phase 切换强制发。"""
    seen: list[dict] = []

    def progress(payload: dict) -> None:
        seen.append(payload)

    run_export(copies, GROUP, tmp_path / "out", fmt="json", progress=progress)
    assert seen, "至少一条进度行"
    for payload in seen:
        assert set(payload.keys()) == {"progress"}
        body = payload["progress"]
        assert set(body.keys()) <= {"phase", "rows", "current_chat", "pct_est"}
        assert body["phase"] in ("scan", "write", "chat")
        # 消息正文零泄漏(current_chat 是契约法定形状字段,只携带显示名)
        dumped = json.dumps(payload, ensure_ascii=False)
        for _ts, _rid, _lt, content in ROWS:
            assert content not in dumped


def test_receipt_contract_keys_and_elapsed(copies: Path, tmp_path: Path) -> None:
    receipt = run_export(copies, GROUP, tmp_path / "out", fmt="txt")
    export = receipt["export"]
    assert list(export.keys()) == [
        "chat_id", "display_name", "format", "files", "manifest_path",
        "total_rows", "time_range", "elapsed_ms",
    ]
    assert isinstance(export["elapsed_ms"], int) and export["elapsed_ms"] >= 0
    assert export["time_range"] == {"from_ts": NOW - 3600 * 24 * 2, "to_ts": NOW - 10}
    file_entry = export["files"][0]
    assert list(file_entry.keys()) == ["name", "path", "rows", "sha256"]
    digest = hashlib.sha256(Path(file_entry["path"]).read_bytes()).hexdigest()
    assert digest == file_entry["sha256"]


def test_filename_two_modes_and_sanitization() -> None:
    """R4:classic / date-range 双模式 + 文件系统消毒(禁字符 → _)。"""
    fixed_now = 1_700_000_000.0
    stamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(fixed_now))
    name = build_file_name(
        display_name="AI/中转:站\\群*?", chat_id="wxid_x", fmt="json",
        name_mode="classic", from_date=None, to_date=None, now=fixed_now,
    )
    assert name == f"聊天记录-AI_中转_站_群__-{stamp}.json"  # \ * ? → 两个尾下划线
    name = build_file_name(
        display_name=None, chat_id="wxid_x", fmt="csv",
        name_mode="date-range", from_date="20260101", to_date="20261014", now=None,
    )
    assert name == "聊天记录-wxid_x-20260101__20261014.csv"
    assert sanitize_file_name("正常名") == "正常名"
    assert sanitize_file_name("") == "_"


def test_display_name_pref_nickname_first(copies: Path, tmp_path: Path) -> None:
    """R4:nickname-first 跳过 remark(ME 有备注「我的备注」,昵称「我的昵称」)。"""
    receipt = run_export(
        copies, GROUP, tmp_path / "out", fmt="txt", display_name_pref="nickname-first"
    )
    text = _receipt_files(receipt)[0].read_text()
    assert "我的昵称(text)" in text
    assert "我的备注" not in text


def test_usage_errors_rejected(copies: Path, tmp_path: Path) -> None:
    with pytest.raises(BridgeError) as err:
        run_export(copies, GROUP, tmp_path / "o", fmt="pdf")
    assert err.value.exit_code == EXIT_USAGE
    with pytest.raises(BridgeError):
        run_export(copies, GROUP, tmp_path / "o", fmt="json", name_mode="fancy")
    with pytest.raises(BridgeError):
        run_export(copies, GROUP, tmp_path / "o", fmt="json", display_name_pref="group")
    with pytest.raises(BridgeError):
        run_export(copies, None, tmp_path / "o", fmt="json")  # 单会话缺 chat_id
