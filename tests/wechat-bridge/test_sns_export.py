"""朋友圈只读导出单测(task 10-14-wechat-media-sns R3/R4;全合成,零真实内容)。

夹具形状照 test_sns_query.py(SnsTimeLine content XML + SnsMessage_tmp3),
差异 = content XML 携带 media 节点全量属性(url/md5/key/enc_idx/token)。
R4 回源用 ``http_get`` 注入 stub(AC4:夹具级验证;真 CDN 端到端 = 主人
开箱后补验),外部解密件用 ``provider_runner`` 注入替身(协议 spawn 链已在
test_media.py 用真子进程覆盖)。
"""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

import wechat_bridge.sns_export as sns_export
from wechat_bridge.codes import DECRYPT_FAILED, EXIT_USAGE, BridgeError
from wechat_bridge.sns_query import FEED_TABLE, NOTICES_TABLE

NOW = int(time.time())
JPEG_MAGIC = b"\xff\xd8\xff\xe0" + b"\x00" * 12

#: 合成 media 节点(url 属性全量;真形状:attrs type/md5/key/enc_idx/token)。
_MEDIA_NODE = (
    '<media><type>{mtype}</type>'
    '<url type="1" md5="{md5}" key="{key}" enc_idx="{enc}"{token}>{url}</url>'
    "</media>"
)


def _feed_xml(
    entry_id: str,
    user: str,
    ts: int,
    text: str,
    media: list[dict] | None = None,
) -> str:
    nodes = "".join(
        _MEDIA_NODE.format(
            mtype=m["type"],
            md5=m.get("md5", "md5x"),
            key=m.get("key", "123456"),
            enc=m.get("enc", "1"),
            token=f' token="{m["token"]}"' if m.get("token") else "",
            url=m["url"],
        )
        for m in (media or [])
    )
    return (
        "<SnsDataItem><TimelineObject>"
        f"<id>{entry_id}</id><username>{user}</username>"
        f"<createTime>{ts}</createTime><contentDesc>{text}</contentDesc>"
        f"<ContentObject><mediaList>{nodes}</mediaList></ContentObject>"
        "</TimelineObject></SnsDataItem>"
    )


@pytest.fixture()
def sns_copies(tmp_path: Path) -> Path:
    copy_root = tmp_path / "decrypted"
    sns = copy_root / "sns" / "sns.db"
    sns.parent.mkdir(parents=True)
    con = sqlite3.connect(sns)
    con.execute(
        f'CREATE TABLE "{FEED_TABLE}" (tid INTEGER, user_name TEXT, '
        "content TEXT, pack_info_buf TEXT)"
    )
    rows = [
        # 双图 + 视频;评论区可关联(feed_id=9001)
        (1, "wxid_a", _feed_xml("9001", "wxid_a", NOW - 600, "合成正文一", [
            {"type": "2", "url": "https://cdn.test/a/0", "md5": "ma", "key": "111", "enc": "1", "token": "ta"},
            {"type": "2", "url": "https://cdn.test/b/0", "md5": "mb", "key": "222", "enc": "1"},
            {"type": "6", "url": "https://cdn.test/v/0", "md5": "mv", "key": "333", "enc": "0"},
        ])),
        # 语音帖(非目标:词面如实不导出内容)
        (2, "wxid_b", _feed_xml("9002", "wxid_b", NOW - 1200, "语音帖", [
            {"type": "4", "url": "https://cdn.test/voice/0", "md5": "ms", "key": "444", "enc": "0"},
        ])),
        # 窗口外
        (3, "wxid_a", _feed_xml("9003", "wxid_a", NOW - 40 * 86400, "旧帖", [])),
        # 坏 XML:弃行计错
        (4, "wxid_c", "<SnsDataItem><TimelineObject>未闭合"),
    ]
    con.executemany(
        f'INSERT INTO "{FEED_TABLE}" VALUES (?,?,?,?)',
        [(t, u, c, "") for t, u, c, in rows],
    )
    con.execute(
        f'CREATE TABLE "{NOTICES_TABLE}" (local_id INTEGER PRIMARY KEY, '
        "create_time INTEGER, type INTEGER, feed_id INTEGER, is_unread INTEGER, "
        "from_username TEXT, from_nickname TEXT, to_username TEXT, "
        "to_nickname TEXT, content TEXT, serialized_comment_buf BLOB, "
        "comment_id INTEGER, client_id TEXT, comment64_id INTEGER, "
        "comment_flag INTEGER, del_status INTEGER, is_relative_me INTEGER)"
    )
    notices = [
        (1, NOW - 300, 2, 9001, "wxid_c", "评论者丙", "有道理", 0),
        (2, NOW - 200, 1, 9001, "wxid_d", "点赞者丁", None, 0),
        (3, NOW - 100, 2, 7777, "wxid_e", "未关联评论", "窗口外条目的评论", 0),
    ]
    con.executemany(
        f'INSERT INTO "{NOTICES_TABLE}" (local_id, create_time, type, feed_id, '
        "from_username, from_nickname, content, is_relative_me) "
        "VALUES (?,?,?,?,?,?,?,?)",
        notices,
    )
    con.commit()
    con.close()

    contact = copy_root / "contact" / "contact.db"
    contact.parent.mkdir(parents=True)
    con = sqlite3.connect(contact)
    con.execute(
        "CREATE TABLE contact (username TEXT PRIMARY KEY, alias TEXT, "
        "nickname TEXT, remark TEXT, localType INTEGER)"
    )
    con.execute("INSERT INTO contact VALUES ('wxid_a','','昵称甲','备注甲',1)")
    con.commit()
    con.close()
    return copy_root


def _stub_http(responses: dict[str, tuple[int, dict[str, str], bytes]], calls: list):
    """http_get 注入 stub:按 URL 前缀应答;calls 记录(AC4 无网断言用)。"""

    def get(url: str, timeout: float = 30.0):
        calls.append(url)
        for prefix, answer in responses.items():
            if url.startswith(prefix):
                return answer
        return (404, {}, b"")

    return get


def _media_by_url(payload: dict) -> dict:
    """全条目 media 节点按 cdn_url 汇平(entries 升序,勿按序号定位条目)。"""
    flat: dict = {}
    for entry in payload["entries"]:
        for node in entry["media"]:
            if node.get("cdn_url"):
                flat[str(node["cdn_url"])] = node
    return flat


def _stub_provider(tmp_out_writer=None):
    """provider_runner 注入替身:解出 JPEG(ext=jpg;wxgf 形态可覆写)。"""
    holder: dict = {"calls": [], "result": None}

    def runner(provider_path: str, request: dict) -> dict:
        holder["calls"].append(
            {k: request[k] for k in ("action", "in_path") if k in request}
        )
        out = Path(request["out_path"])
        if holder["result"] and holder["result"].get("is_wxgf"):
            out.write_bytes(b"wxgf-container")
        else:
            out.write_bytes(JPEG_MAGIC)
        return {
            "type": "result",
            "success": True,
            "ext": (holder["result"] or {}).get("ext", "jpg"),
            "is_wxgf": (holder["result"] or {}).get("is_wxgf", False),
            "width": 640,
            "height": 480,
            "logs": [],
        }

    return runner, holder


def _run(
    copy_dir: Path,
    fmt: str = "json",
    out_dir: Path | None = None,
    data_root: Path | None = None,
    with_media: bool = False,
    config=None,
    http_get=None,
    provider_runner=None,
) -> dict:
    return sns_export.run_sns_export(
        copy_dir=copy_dir,
        since_days=30,
        copy_info={"dir": str(copy_dir), "built": [], "kept": []},
        fmt=fmt,
        out_dir=out_dir,
        data_root=data_root,
        with_media=with_media,
        config=config,
        http_get=http_get,
        provider_runner=provider_runner,
    )


# ---------------------------------------------------------------------------
# 解析:media 全量字段
# ---------------------------------------------------------------------------


class TestParseExportRow:
    def test_media_full_fields(self) -> None:
        entry = sns_export.parse_export_row(
            _feed_xml("1", "u", 100, "t", [
                {"type": "2", "url": "https://x/1", "md5": "m", "key": "9", "enc": "1", "token": "tk"},
            ])
        )
        assert entry is not None
        node = entry["media"][0]
        assert node["type"] == "2"
        assert node["cdn_url"] == "https://x/1"
        assert node["md5"] == "m"
        assert node["key"] == "9"
        assert node["enc_idx"] == "1"
        assert node["token"] == "tk"
        assert node["width"] is None and node["height"] is None

    def test_bad_shapes(self) -> None:
        assert sns_export.parse_export_row("不是 XML") is None
        assert sns_export.parse_export_row(None) is None


# ---------------------------------------------------------------------------
# R3 JSON 导出(缺省关:零网络请求 + 评论区关联 + 状态词面)
# ---------------------------------------------------------------------------


class TestJsonExport:
    def test_default_no_media_zero_http_and_payload(self, sns_copies, tmp_path):
        calls: list = []
        result = _run(
            sns_copies, fmt="json", out_dir=tmp_path / "out", data_root=tmp_path,
            http_get=_stub_http({}, calls),
        )
        inner = result["sns_export"]
        assert inner["format"] == "json"
        assert inner["with_media"] is False
        assert calls == []  # AC4:--with-media 缺省关 = 零网络请求
        artifact = Path(inner["out_dir"]) / "sns-export.json"
        assert artifact.is_file()
        assert oct(artifact.stat().st_mode & 0o777) == "0o600"
        payload = json.loads(artifact.read_text(encoding="utf-8"))
        entries = payload["entries"]
        assert len(entries) == 2  # 4 行 - 窗口外 - 坏 XML
        by_id = {e["id"]: e for e in entries}
        entry = by_id["9001"]
        # nickname 反查回填;媒体全量字段在载荷(token 不吐)
        assert entry["nickname"] == "备注甲"
        media = entry["media"]
        assert [m["type"] for m in media] == ["2", "2", "6"]
        assert all("token" not in m for m in media)
        assert all(m["status"] == "未开启媒体下载" for m in media)
        # 评论区关联:comment 进条目、like 进条目、未关联单独成节
        assert entry["comments"][0]["from_nickname"] == "评论者丙"
        assert entry["comments"][0]["content"] == "有道理"
        assert entry["likes"][0]["from_nickname"] == "点赞者丁"
        unlinked = payload["unlinked_notices"]
        assert len(unlinked) == 1 and unlinked[0]["feed_id"] == "7777"
        # 关联率如实入 stats
        stats = payload["stats"]
        assert stats["comment_link_rate"] == "1/2"
        assert stats["comments_linked"] == 1 and stats["comments_total"] == 2
        assert stats["likes_linked"] == 1
        assert stats["media_status"]["未开启媒体下载"] == 3
        assert stats["media_status"]["语音,暂不支持"] == 1
        assert stats["parse_errors"] == 1 and stats["rows_out_of_window"] == 1

    def test_default_out_dir_under_data_root(self, sns_copies, tmp_path):
        result = _run(sns_copies, fmt="json", data_root=tmp_path)
        out_dir = Path(result["sns_export"]["out_dir"])
        assert tmp_path in out_dir.parents
        assert out_dir.name.startswith("sns-")

    def test_usage_rejects_bad_format(self, sns_copies, tmp_path):
        with pytest.raises(BridgeError) as excinfo:
            _run(sns_copies, fmt="xml", out_dir=tmp_path / "o", data_root=tmp_path)
        assert excinfo.value.exit_code == EXIT_USAGE

    def test_copy_missing_raises_decrypt_failed(self, tmp_path):
        with pytest.raises(BridgeError) as excinfo:
            _run(tmp_path, out_dir=tmp_path / "o", data_root=tmp_path)
        assert excinfo.value.exit_code == DECRYPT_FAILED


# ---------------------------------------------------------------------------
# R3 HTML 导出(单文件 + files/ 相对引用;禁 base64)
# ---------------------------------------------------------------------------


class TestHtmlExport:
    def test_html_self_contained_placeholders(self, sns_copies, tmp_path):
        calls: list = []
        result = _run(
            sns_copies, fmt="html", out_dir=tmp_path / "out", data_root=tmp_path,
            http_get=_stub_http({}, calls),
        )
        inner = result["sns_export"]
        page = (Path(inner["out_dir"]) / "index.html").read_text(encoding="utf-8")
        assert calls == []
        assert "data:image" not in page  # 禁 base64 内嵌
        assert "files/" not in page or "未开启媒体下载" in page
        # 人话占位词面 + 正文 + 评论 + 摘要
        assert "未开启媒体下载" in page
        assert "语音,暂不支持" in page
        assert "备注甲" in page and "合成正文一" in page
        assert "评论者丙" in page and "有道理" in page
        assert "点赞者丁" in page
        assert "评论关联 1/2" in page

    def test_html_escapes_user_text(self, sns_copies, tmp_path):
        con = sqlite3.connect(sns_copies / "sns" / "sns.db")
        con.execute(
            f'UPDATE "{FEED_TABLE}" SET content = ? WHERE tid = 1',
            (_feed_xml("9001", "wxid_a", NOW - 600, "&lt;script&gt;alert(1)&lt;/script&gt;&amp;", []),),
        )
        con.commit()
        con.close()
        result = _run(sns_copies, fmt="html", out_dir=tmp_path / "out", data_root=tmp_path)
        page = (Path(result["sns_export"]["out_dir"]) / "index.html").read_text(encoding="utf-8")
        assert "<script>alert(1)</script>" not in page
        assert "&lt;script&gt;" in page

    def test_html_media_refs_with_media(self, sns_copies, tmp_path):
        calls: list = []
        http = _stub_http(
            {
                "https://cdn.test/a/0": (200, {"x-enc": "1"}, b"cipher-image"),
                "https://cdn.test/v/0": (200, {}, b"\x00\x00\x00\x18ftypisom" + b"v"),
            },
            calls,
        )
        runner, _holder = _stub_provider()
        result = _run(
            sns_copies, fmt="html", out_dir=tmp_path / "out", data_root=tmp_path,
            with_media=True,
            config=SimpleNamespace(media_decrypt_path="/fake/provider"),
            http_get=http,
            provider_runner=runner,
        )
        page = (Path(result["sns_export"]["out_dir"]) / "index.html").read_text(encoding="utf-8")
        assert '<img src="files/' in page
        assert "<video controls" in page
        assert "data:image" not in page


# ---------------------------------------------------------------------------
# R4 回源(x-enc 判密/失效标注/未配置词面;夹具级)
# ---------------------------------------------------------------------------


class TestWithMedia:
    def _run_with_media(self, sns_copies, tmp_path, http, config=None, runner=None):
        return _run(
            sns_copies, fmt="json", out_dir=tmp_path / "out", data_root=tmp_path,
            with_media=True,
            config=config if config is not None else SimpleNamespace(media_decrypt_path="/fake/p"),
            http_get=http,
            provider_runner=runner,
        )

    def test_xenc_stream_decrypt_flow(self, sns_copies, tmp_path):
        """x-enc:1 → 临时密文交件 decrypt_stream;产物落 files/;词面已解密。"""
        calls: list = []
        http = _stub_http(
            {"https://cdn.test/a/0": (200, {"x-enc": "1"}, b"cipher-a")}, calls
        )
        runner, holder = _stub_provider()
        result = self._run_with_media(sns_copies, tmp_path, http, runner=runner)
        inner = result["sns_export"]
        # decrypt_stream 被调用且经 stdin 载荷传 key(替身记录)
        stream_calls = [c for c in holder["calls"] if c["action"] == "decrypt_stream"]
        assert len(stream_calls) == 1
        # 产物文件在 files/ 且 600
        media_files = [f for f in inner["files"] if f.startswith("files/")]
        assert len(media_files) == 1
        artifact = Path(inner["out_dir"]) / media_files[0]
        assert artifact.read_bytes()[:4] == JPEG_MAGIC[:4]
        assert oct(artifact.stat().st_mode & 0o777) == "0o600"
        # 密文临时件已清(不留 .cipher-* 残留)
        assert list((Path(inner["out_dir"]) / "files").glob(".cipher-*")) == []
        payload = json.loads(
            (Path(inner["out_dir"]) / "sns-export.json").read_text(encoding="utf-8")
        )
        by_url = _media_by_url(payload)
        assert by_url["https://cdn.test/a/0"]["status"] == "已解密"
        assert by_url["https://cdn.test/a/0"]["local_path"] == media_files[0].split("/")[-1]

    def test_plaintext_copy_and_link_expired(self, sns_copies, tmp_path):
        calls: list = []
        http = _stub_http(
            {
                "https://cdn.test/v/0": (200, {}, b"\x00\x00\x00\x18ftypisom" + b"v"),
            },
            calls,
        )
        result = self._run_with_media(sns_copies, tmp_path, http)
        payload = json.loads(
            (Path(result["sns_export"]["out_dir"]) / "sns-export.json")
            .read_text(encoding="utf-8")
        )
        by_url = _media_by_url(payload)
        assert by_url["https://cdn.test/v/0"]["status"] == "明文复制"
        # 其余 URL stub 缺省 404 → 链接失效如实
        assert by_url["https://cdn.test/a/0"]["status"] == "未能下载(链接已失效)"
        assert by_url["https://cdn.test/b/0"]["status"] == "未能下载(链接已失效)"

    def test_unconfigured_provider_wording(self, sns_copies, tmp_path):
        calls: list = []
        http = _stub_http(
            {"https://cdn.test/a/0": (200, {"x-enc": "1"}, b"cipher")}, calls
        )
        result = self._run_with_media(
            sns_copies, tmp_path, http, config=SimpleNamespace(media_decrypt_path="")
        )
        payload = json.loads(
            (Path(result["sns_export"]["out_dir"]) / "sns-export.json")
            .read_text(encoding="utf-8")
        )
        by_url = _media_by_url(payload)
        assert by_url["https://cdn.test/a/0"]["status"] == "未配置解密件,未解密"

    def test_wxgf_kept_with_wording(self, sns_copies, tmp_path):
        calls: list = []
        http = _stub_http(
            {"https://cdn.test/a/0": (200, {"x-enc": "1"}, b"cipher")}, calls
        )
        runner, holder = _stub_provider()
        holder["result"] = {"ext": "wxgf", "is_wxgf": True}
        result = self._run_with_media(sns_copies, tmp_path, http, runner=runner)
        payload = json.loads(
            (Path(result["sns_export"]["out_dir"]) / "sns-export.json")
            .read_text(encoding="utf-8")
        )
        by_url = _media_by_url(payload)
        assert by_url["https://cdn.test/a/0"]["status"] == "实况格式,暂不支持预览"
        # wxgf 产物原样保留(字节不解码)
        kept = Path(result["sns_export"]["out_dir"]) / "files" / str(
            by_url["https://cdn.test/a/0"]["local_path"]
        )
        assert kept.read_bytes() == b"wxgf-container"

    def test_voice_not_fetched(self, sns_copies, tmp_path):
        calls: list = []
        http = _stub_http({}, calls)
        self._run_with_media(sns_copies, tmp_path, http)
        assert all("voice" not in url for url in calls)  # 语音帖不回源
