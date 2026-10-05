"""判据验证:pagetype 文章形态判别力 + extract=None 现状拒载实证。"""
# ruff: noqa: F821
# ↑ :7 exec(open(...)) 运行时注入三夹具常量(ARTICLE/LISTING 等,定义在
# /tmp/traf-eval-matrix.py),静态分析不可见;evidence 脚本勿以此为由清全文件。
import json
from types import SimpleNamespace
from trafilatura import extract as traf_extract
from myssia.engines.static_html import StaticHTMLEngine

exec(open("/tmp/traf-eval-matrix.py").read().split("def rules_result")[0])  # 复用三夹具常量

def probe(name, html, url):
    raw = traf_extract(html, url=url, output_format="json", with_metadata=True)
    if raw is None:
        print(f"{name}: extract() -> None(无正文判定)")
        return
    doc = json.loads(raw)
    print(f"{name}: pagetype={doc.get('pagetype')!r} title={doc.get('title')!r} "
          f"date={doc.get('date')!r} text_chars={len(doc.get('text') or '')}")

print("== pagetype 判别力 ==")
probe("A 文章页  ", ARTICLE, PAGE_URL)
probe("B 列表页  ", LISTING, LIST_URL)
probe("C2 改版文章页", REVAMPED_ARTICLE, PAGE_URL)
probe("C3 改版列表页", REVAMPED, LIST_URL)
# 纯噪声页(全导航)
NOISE = """<html><body><nav><a href="/">首页</a><a href="/a">A</a><a href="/b">B</a></nav>
<footer><p>© 2026 | 隐私 | 条款</p></footer></body></html>"""
probe("D 纯导航页", NOISE, "https://example.org/nav")

print("\n== extract=None 现状(static_html 拒载) ==")
engine = StaticHTMLEngine.__new__(StaticHTMLEngine)  # 绕过 __init__,只测 _check_extract_support
engine.source = SimpleNamespace(extract=None)
try:
    engine._check_extract_support()
    print("未拒绝(意外!)")
except Exception as exc:
    print(f"raise {type(exc).__name__}: error_type={exc.error_type} msg={exc}")
