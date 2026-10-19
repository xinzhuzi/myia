"""s74 新 DOM 选择器验证(2026-10-19)——与 src/myssia/engines/fetch_base.py
extract_html 完全同款语义:selectolax HTMLParser + tree.css(item) +
node.css(field) 首匹配 + @attr + urljoin(base_url)。输出各候选方案的
节点计数与四字段覆盖率,不产出任何凭据。
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urljoin

from selectolax.parser import HTMLParser

HERE = Path(__file__).resolve().parent
HTML = (HERE / "s74-rendered-2026-10-19.html").read_text(encoding="utf-8")
BASE = "https://tkkgv8.gicp.fun/"

URL_ATTRS = {"href", "src"}


def split_attr(selector: str) -> tuple[str, str | None]:
    if "@" in selector:
        css, _, attr = selector.rpartition("@")
        return css, attr
    return selector, None


def field_value(root, selector: str):
    css, attr = split_attr(selector)
    nodes = root.css(css) if css else [root]
    if not nodes:
        return None
    node = nodes[0]
    if attr:
        value = node.attributes.get(attr)
        if value is None:
            return None
        return urljoin(BASE, value) if (BASE and attr in URL_ATTRS) else value
    text = node.text(separator=" ", strip=True)
    return text if text else None


def evaluate(name: str, item_sel: str, fields: dict[str, str]) -> dict:
    tree = HTMLParser(HTML)
    cards = tree.css(item_sel)
    per_field_hit = {k: 0 for k in fields}
    records = []
    for node in cards:
        rec = {}
        for fname, sel in fields.items():
            v = field_value(node, sel)
            if v is not None:
                per_field_hit[fname] += 1
                rec[fname] = v
        records.append(rec)
    samples = []
    for rec in records[:2] + records[-1:]:
        samples.append(
            {
                "title": (rec.get("title") or "")[:40],
                "url": (rec.get("url") or "")[:60],
                "desc": (rec.get("desc") or "")[:30],
                "code": rec.get("code"),
            }
        )
    return {
        "plan": name,
        "item_selector": item_sel,
        "item_nodes": len(cards),
        "field_hits": per_field_hit,
        "samples": samples,
    }


def main() -> None:
    # 旧配置(基线,证明失效点)
    old = evaluate(
        "旧配置(失效基线)",
        ".card",
        {"title": ".card-name", "url": ".card-url@href", "desc": ".card-desc", "code": ".invite-code"},
    )
    # 方案A:最小修复——只改 url 选择器(div.card-url 内的 a)
    plan_a = evaluate(
        "A(最小修复)",
        ".card",
        {"title": ".card-name", "url": ".card-url a@href", "desc": ".card-desc", "code": ".invite-code"},
    )
    # 方案B:防包裹层再变——url 取卡内第一个 href,code 取 invite-row 内文本
    plan_b = evaluate(
        "B(抗结构漂移)",
        ".card",
        {"title": ".card-name", "url": "a@href", "desc": ".card-desc", "code": ".invite-row .invite-code"},
    )
    print(json.dumps([old, plan_a, plan_b], ensure_ascii=False, indent=2))

    # 附加结构侦察:卡内元素标签形态分布 + 顶层骨架
    tree = HTMLParser(HTML)
    card_url_tags: dict[str, int] = {}
    for n in tree.css(".card .card-url"):
        card_url_tags[n.tag] = card_url_tags.get(n.tag, 0) + 1
    print("card-url 标签分布:", card_url_tags)
    invite_rows = len(tree.css(".card .invite-row"))
    invite_codes = len(tree.css(".card .invite-code"))
    copy_btns = len(tree.css(".card .copy-code-btn"))
    print(f"invite-row={invite_rows} invite-code={invite_codes} copy-code-btn={copy_btns}")
    # 无邀请码的卡:card 内没有 .invite-row 的数量
    no_code = sum(1 for c in tree.css(".card") if not c.css(".invite-row"))
    print("无 invite-row 的卡数:", no_code)
    # 卡内 a[href] 覆盖
    cards_with_a = sum(1 for c in tree.css(".card") if c.css("a[href]"))
    print("含 a[href] 的卡数:", cards_with_a)


if __name__ == "__main__":
    main()
