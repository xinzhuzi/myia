"""AC6 品类级端到端(验收员 2026-10-05 沙箱 /tmp/table-e2e,-e '.[table]')。

「跑品类」的字面满足:品类 YAML(``images.table: true``)经
``load_category_file`` 从磁盘装载 → ``collect.process_item_images`` 图片环跑
**真** ``run_table``(不打桩、真 rapid_table/rapidocr 引擎、真 SLANET-plus
模型)→ 图片经 ``httpx.MockTransport`` 本地路由喂入(与
tests/vision/test_vision_table.py 的 ``serve()`` :358-365 同款手法),DNS
解析覆写同 ``public_dns`` fixture(:342-351)同款——零外网,SSRF 门照走。

模型门:rapid_table 3.0.2 不内置模型,SLANET-plus 首用从 modelscope 下载
(slanet-plus.onnx 7.4M 落本 venv 包目录,主口径 pytest 预热完成);本脚本
随后离线可复跑。

运行(venv 需含 myssia[table] + 真引擎):
    /tmp/table-e2e/bin/python category-e2e.py

断言面(AC6):条目 ``metadata.tables`` 恰三键 ``{markdown, rows, cols}``,
逐格对齐真引擎探针基准(与 TestRealEngineFixture 同一事实源)。
"""

from __future__ import annotations

import asyncio
import ipaddress
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import httpx

REPO = Path(__file__).resolve().parents[4]
FIXTURE = REPO / "tests" / "vision" / "fixtures" / "table_sample.png"
#: 真引擎探针基准(2026-10-05,rapid-table 3.0.2 + rapidocr-onnxruntime
#: 实跑逐格输出;与 tests/vision/test_vision_table.py:51-57 同一事实源)。
FIXTURE_MARKDOWN = (
    "|品种|价格|涨跌幅|\n"
    "|---|---|---|\n"
    "|BTC|65000|+2.3%|\n"
    "|ETH|3200|-1.2%|\n"
    "|SOL|150|+5.6%|"
)

CATEGORY_YAML = """\
id: table-e2e
name: 表格还原品类级验证
schedule: "0 9 * * *"
sources:
  - name: example
    url: https://example.com/list?page={page}
images:
  enabled: true
  table: true
  min_bytes: 1
  ocr_engine: rapidocr
"""

PUBLIC_IPS = ["93.184.216.34"]


def main() -> int:
    import myssia.vision.collect as collect
    from myssia.schema import load_category_file
    from myssia.vision.settings import VisionConfig

    assert FIXTURE.exists(), f"夹具缺位:{FIXTURE}"
    png = FIXTURE.read_bytes()

    # ① 品类 YAML 从磁盘装载(装载面即 AC6 验证面:images.table 过 schema)
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False) as fh:
        fh.write(CATEGORY_YAML)
        yaml_path = fh.name
    cfg = load_category_file(yaml_path)
    assert cfg.images is not None and cfg.images.table is True, "品类装载后 table 应为 True"
    print(f"[load] 品类装载 OK:id={cfg.id} images.table={cfg.images.table} "
          f"ocr_engine={cfg.images.ocr_engine}")

    # ② DNS 解析覆写(public_dns fixture 同款:非 IP 主机名 → 固定公网 IP)
    def _resolve(host: str) -> list[str]:
        try:
            ipaddress.ip_address(host)
        except ValueError:
            return list(PUBLIC_IPS)
        return [host]

    collect._resolve_host = _resolve  # 脚本面直接覆写,进程即退

    # ③ serve() 同款:MockTransport 本地路由,夹具真图字节喂入
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/pic.png":
            return httpx.Response(200, content=png)
        return httpx.Response(404, text="missing")

    client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler), follow_redirects=False
    )

    # ④ 图片环真跑:真 run_table(不 monkeypatch)、真 OCR(rapidocr)
    item = SimpleNamespace(
        url="https://example.com/item", title="示例条目",
        metadata={"image": "https://example.com/pic.png"},
    )
    status = asyncio.run(collect.process_item_images(
        item, images_cfg=cfg.images, vision_cfg=VisionConfig(), client=client,
    ))
    print(f"[collect] image_status={status!r}")
    print(f"[collect] metadata keys={sorted(item.metadata)}")
    ocr_text = item.metadata.get("image_ocr", "")
    print(f"[collect] image_ocr(前 80 字符)={ocr_text[:80]!r}")

    # ⑤ 断言面:tables 恰三键、逐格对齐探针基准
    tables = item.metadata.get("tables")
    assert tables is not None, f"tables 未落(table_status={item.metadata.get('table_status')!r})"
    assert len(tables) == 1, f"恰一张表,实际 {len(tables)}"
    table = tables[0]
    assert set(table) == {"markdown", "rows", "cols"}, f"三键契约,实际键集 {set(table)}"
    assert table["rows"] == 4 and table["cols"] == 3, f"4x3,实际 {table['rows']}x{table['cols']}"
    assert table["markdown"] == FIXTURE_MARKDOWN, (
        f"逐格不对齐:\n--- 实际 ---\n{table['markdown']}\n--- 基准 ---\n{FIXTURE_MARKDOWN}"
    )
    assert "table_status" not in item.metadata, "零失败不应写降级标记"
    print("[assert] metadata.tables 恰三键 {markdown,rows,cols},4x3 逐格对齐真引擎探针基准")
    print("[assert] AC6 品类级端到端 PASS(品类 YAML 装载 + collect 环真 run_table + 三键契约)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
