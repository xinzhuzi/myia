"""myssia-urlwatch 渲染 helper 契约测试(10-06-ai-news-sources §12).

被钉住的契约:

1. **归一化**:图片/链接 URL 剔除(fbcdn CDN 签名轮换 `oe=`/`_nc_oc=` 出局,
   两份仅签名不同的 markdown 归一相等——快照只随真实内容变化),标题/
   日期正文文字保留;
2. **CLI 面**:stdout 只打印归一化正文(诊断走 stderr);退出码词表
   0 成功 / 1 渲染失败 / 3 渲染后端缺失(装机 doctor 面可辨)。

测试纪律:零网络、零真实 crawl4ai(``_crawl_markdown`` 注入替换);helper
以 compile+exec 装载(插件目录不是包,与 adapter 测试同手法)。
"""

from __future__ import annotations

import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HELPER_FILE = REPO_ROOT / "plugins" / "myssia-urlwatch" / "render_crawl4ai.py"


def load_helper() -> types.ModuleType:
    module = types.ModuleType("myssia_urlwatch_render_helper_test")
    module.__file__ = str(HELPER_FILE)
    exec(  # noqa: S102 - 仓库内受控代码
        compile(HELPER_FILE.read_text(encoding="utf-8"), str(HELPER_FILE), "exec"),
        module.__dict__,
    )
    return module


MARKDOWN_A = """[![Meta](https://x.fbcdn.net/v/logo.svg?_nc_oc=Ab12&oe=6ADE1234)](https://ai.meta.com/blog/)
The latest AI news from Meta
[FEATURED ![cover](https://y.fbcdn.net/cover.png?_nc_oc=Cd34&oe=6ADE5678)](https://ai.meta.com/blog/introducing-muse-spark/)
Research
[Introducing Muse Spark 1.1 ](https://ai.meta.com/blog/introducing-muse-spark/)
July 9, 2026
"""

MARKDOWN_B = """Meta
The latest AI news from Meta
FEATURED
Research
Introducing Muse Spark 1.1
July 9, 2026
"""  # 与 A 同内容、但图片/链接 URL 全部剔除后的期望形


def test_strip_markdown_noise_removes_images_and_link_urls():
    helper = load_helper()
    normalized = helper.strip_markdown_noise(MARKDOWN_A)
    assert "fbcdn.net" not in normalized
    assert "https://" not in normalized
    assert "Introducing Muse Spark 1.1" in normalized
    assert "July 9, 2026" in normalized
    assert "The latest AI news from Meta" in normalized


def test_strip_markdown_noise_is_cdn_signature_invariant():
    """仅 CDN 轮换签名不同的两份 markdown 归一相等(快照漂移噪声出局)."""
    helper = load_helper()
    other = MARKDOWN_A.replace("oe=6ADE1234", "oe=6ACF9999").replace(
        "_nc_oc=Ab12", "_nc_oc=Xy98"
    )
    assert helper.strip_markdown_noise(MARKDOWN_A) == helper.strip_markdown_noise(other)


def test_strip_markdown_noise_collapses_blank_runs_and_terminates_once():
    helper = load_helper()
    normalized = helper.strip_markdown_noise("a\n\n\n\n\nb\n\n\n")
    assert normalized == "a\n\nb\n"


def test_main_prints_normalized_text_to_stdout(monkeypatch, capsys):
    helper = load_helper()

    async def fake_crawl(url):  # noqa: ANN001, ANN202
        return MARKDOWN_A

    monkeypatch.setattr(helper, "_crawl_markdown", fake_crawl)
    rc = helper.main(["https://ai.meta.com/blog"])
    assert rc == helper.EXIT_OK == 0
    captured = capsys.readouterr()
    assert "fbcdn.net" not in captured.out
    assert "Introducing Muse Spark 1.1" in captured.out
    assert captured.err == ""  # 成功路径零 stderr


def test_main_backend_missing_exits_three(monkeypatch, capsys):
    helper = load_helper()

    async def missing(url):  # noqa: ANN001, ANN202
        raise ImportError("No module named 'crawl4ai'")

    monkeypatch.setattr(helper, "_crawl_markdown", missing)
    rc = helper.main(["https://ai.meta.com/blog"])
    assert rc == helper.EXIT_BACKEND_MISSING == 3
    assert "渲染后端" in capsys.readouterr().err


def test_main_fetch_failure_exits_one(monkeypatch, capsys):
    helper = load_helper()

    async def boom(url):  # noqa: ANN001, ANN202
        raise RuntimeError("net::ERR_TIMED_OUT")

    monkeypatch.setattr(helper, "_crawl_markdown", boom)
    rc = helper.main(["https://ai.meta.com/blog"])
    assert rc == helper.EXIT_FETCH_FAILED == 1
    assert "ERR_TIMED_OUT" in capsys.readouterr().err
