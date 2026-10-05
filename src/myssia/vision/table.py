"""表格结构化引擎封装:rapid_table(RapidAI 家族 onnx 版,task 10-05-table-restore)。

截图里的表格(行情/比价/参数对比/榜单)还原成 GFM Markdown 进条目
``metadata.tables``(R6 产出契约 ``{markdown, rows, cols}``)。与整图语义
描述(既有 VL 环)分工边界:表格结构化 = 本模块;互不替代(R5)。

调用形态(:func:`run_table`):

- 单图 → 单表;``None`` = 图内未检出表格(合法结果,不是错误);
- 引擎 = rapid_table 3.x(``RapidTable()``,缺省 SLANET-plus 结构模型),
  **OCR 结果显式喂入**(rapidocr-onnxruntime,与 vision extras 同栈):
  rapid_table 3.x 默认 ``use_ocr=True`` 但其内置 OCR 走新版 ``rapidocr``
  包,未装时 ``ocr_engine=None`` 调用即炸(3.0.2 轮 main.py 实读);走
  ``ocr_results=[(boxes, txts, scores)]`` 参数即可完全绕开——同栈复用、
  零新增 OCR 发行版(R1:不引 Paddle 全家,复用自管环境 onnxruntime);
- 模型说明:**rapid_table 3.x 轮并不内置模型**(README「打包进 whl」措辞
  已过期,3.0.2 轮实读无 models/),首次 ``RapidTable()`` 初始化从
  modelscope 下载 slanet-plus.onnx(6.8MB,SHA256 校验)到包目录,之后
  离线复用;
- 引擎单例 + 推理互斥锁:结构模型几十 MB,逐调用重建 = 逐次重载;
  onnxruntime 会话线程安全性未承诺,串行化最稳(管线侧并发本就为 1)。

HTML → Markdown:rapid_table 产出 ``pred_html``(``<td colspan/rowspan>``
原样保留),经 selectolax(核心依赖,零新增)解析成占位格网——colspan
原格保留内容(不复制),rowspan 影子格补空(GFM 无跨行语义)——再投影
GFM(首行为表头,契约样式 ``|a|b|`` 无空格填充)。

依赖红线:rapid_table / rapidocr-onnxruntime 全部惰性 import(extras
``myssia[table]``),未装时 :class:`TableError`(``dependency_missing``)
结构化报错并附安装命令;管线环(:mod:`myssia.vision.collect`)统一落
``metadata.table_status = "table_provider_error"``,绝不阻管线(R6)。
"""

from __future__ import annotations

import importlib
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from selectolax.parser import HTMLParser

__all__ = [
    "INSTALL_COMMAND",
    "TableError",
    "TableResult",
    "html_table_to_markdown",
    "run_table",
]

INSTALL_COMMAND = 'pip install "myssia[table]"  # 或 uv add "myssia[table]"'

#: colspan/rowspan 属性值解析上限(防结构模型吐出畸形大跨度撑爆格网)。
_MAX_SPAN = 64

#: 引擎单例(结构模型 + OCR 模型都只在首次调用加载;测试经 _reset_engines 重置)。
_TABLE_ENGINE: Any = None
_OCR_ENGINE: Any = None
#: 推理互斥锁:构造与推理都串行(单例惰性初始化 + onnxruntime 会话不保证线程安全)。
_INFERENCE_LOCK = threading.Lock()


class TableError(RuntimeError):
    """表格还原结构化失败;管线环统一落 ``table_status = "table_provider_error"``。

    Attributes:
        code: ``dependency_missing``(extras 未装,附 :data:`INSTALL_COMMAND`)/
            ``engine_failed``(引擎执行失败,原文原因入 message)。
        details: 结构化上下文(package / install)。
    """

    def __init__(self, code: str, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.details: dict[str, Any] = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Machine-readable form。"""
        return {"error_type": self.code, "message": str(self), **self.details}


@dataclass(frozen=True)
class TableResult:
    """一张还原表:GFM Markdown + 规整后行列数(R6 契约三键的数据形态)。"""

    markdown: str
    rows: int
    cols: int

    def to_dict(self) -> dict[str, Any]:
        """R6 产出契约形:``{markdown, rows, cols}``(metadata.tables 元素)。"""
        return {"markdown": self.markdown, "rows": self.rows, "cols": self.cols}


def run_table(image_path: Path | str) -> TableResult | None:
    """对单图做表格结构化还原;``None`` = 图内未检出表格(合法,非错误)。

    Raises:
        TableError: ``dependency_missing``(rapid-table / rapidocr-onnxruntime
            任一未装)或 ``engine_failed``(引擎执行失败)。
    """
    path = Path(image_path)
    with _INFERENCE_LOCK:
        ocr_feed = _ocr_feed(path)
        if ocr_feed is None:  # 图内零可识别文字:表格内容无从谈起
            return None
        engine = _get_table_engine()
        try:
            result = engine(str(path), ocr_results=[ocr_feed])
            html = result.pred_htmls[0] if result.pred_htmls else ""
        except Exception as exc:  # noqa: BLE001 — 引擎内部任何失败统一结构化包装
            raise TableError(
                "engine_failed",
                f"rapid_table 表格还原失败: {type(exc).__name__}: {exc}",
                details={"engine": "rapid_table"},
            ) from exc
    return html_table_to_markdown(html)


def _get_table_engine() -> Any:
    """rapid_table 引擎单例(结构模型只加载一次);未装 → 结构化缺装报错。"""
    global _TABLE_ENGINE
    if _TABLE_ENGINE is not None:
        return _TABLE_ENGINE
    try:
        rapid_table = importlib.import_module("rapid_table")
    except ImportError as exc:
        raise TableError(
            "dependency_missing",
            f"表格还原依赖 rapid-table 未安装:请先执行 {INSTALL_COMMAND}",
            details={"package": "rapid-table", "install": INSTALL_COMMAND},
        ) from exc
    try:
        # 缺省 RapidTableInput:SLANET-plus 结构模型 + use_ocr=True。OCR 走
        # ocr_results 显式喂入,不触其内置 rapidocr 通道(见模块头)。
        _TABLE_ENGINE = rapid_table.RapidTable()
    except Exception as exc:  # noqa: BLE001 — 模型下载/装载失败同样是 provider 级
        raise TableError(
            "engine_failed",
            f"rapid_table 引擎初始化失败(结构模型装载/下载): {type(exc).__name__}: {exc}",
            details={"engine": "rapid_table"},
        ) from exc
    return _TABLE_ENGINE


def _get_ocr_engine() -> Any:
    """rapidocr_onnxruntime 引擎单例(表格单元格文字来源;与 vision extras 同栈)。"""
    global _OCR_ENGINE
    if _OCR_ENGINE is not None:
        return _OCR_ENGINE
    try:
        rapidocr = importlib.import_module("rapidocr_onnxruntime")
    except ImportError as exc:
        raise TableError(
            "dependency_missing",
            f"表格还原依赖 rapidocr-onnxruntime 未安装(单元格文字识别):请先执行 {INSTALL_COMMAND}",
            details={"package": "rapidocr-onnxruntime", "install": INSTALL_COMMAND},
        ) from exc
    try:
        _OCR_ENGINE = rapidocr.RapidOCR()
    except Exception as exc:  # noqa: BLE001 — 模型装载失败 = provider 级
        raise TableError(
            "engine_failed",
            f"rapidocr 引擎初始化失败(表格 OCR 通道): {type(exc).__name__}: {exc}",
            details={"engine": "rapidocr"},
        ) from exc
    return _OCR_ENGINE


def _ocr_feed(path: Path) -> tuple[Any, tuple[str, ...], tuple[float, ...]] | None:
    """图 OCR → rapid_table ``ocr_results`` 形状 ``(boxes, txts, scores)``。

    零文字 → ``None``(调用方按「未检出表格」处理,省一次结构推理)。
    boxes 用 numpy 堆叠成 (N,4,2)(format_ocr_results 按 polygon 取极值)。
    """
    import numpy as np  # 核心传递依赖(rapidocr/onnxruntime 域),惰性引用

    engine = _get_ocr_engine()
    try:
        result, _elapse = engine(str(path))
    except Exception as exc:  # noqa: BLE001 — 引擎内部任何失败统一结构化包装
        raise TableError(
            "engine_failed",
            f"rapidocr 表格前 OCR 失败: {type(exc).__name__}: {exc}",
            details={"engine": "rapidocr"},
        ) from exc
    if not result:  # 无文字图片:合法空结果(表格内容无从谈起)
        return None
    boxes = np.array([item[0] for item in result], dtype=np.float32)
    txts = tuple(str(item[1]) for item in result)
    scores = tuple(float(item[2]) for item in result)
    return boxes, txts, scores


def _parse_span(raw: str | None) -> int:
    """colspan/rowspan 属性值 → [1, 64] 内整数(畸形值按 1,防撑爆格网)。"""
    if not raw:
        return 1
    match = re.search(r"\d+", raw)
    if match is None:
        return 1
    return max(1, min(int(match.group()), _MAX_SPAN))


def _clean_cell_text(text: str) -> str:
    """格文本规整:空白折叠、管道转义(GFM 单元格不能裸 |)、去首尾。"""
    collapsed = " ".join(text.split())
    return collapsed.replace("|", "\\|")


def html_table_to_markdown(html: str) -> TableResult | None:
    """``pred_html`` → :class:`TableResult`;非表格/全空表 → ``None``。

    占位格网算法与 rapid_table ``decode_one_logic_points`` 同构:按文档序
    走 ``<tr>``/``<td|th>``,每格找本行下一个未占列,按 colspan/rowspan
    标记占用;colspan 内容留在原格(GFM 无列合并语义,渲染自然占一格),
    rowspan 影子格补空(GFM 无跨行语义)。首行为表头,输出契约样式
    ``|a|b|`` + ``|---|---|``(无空格填充)。
    """
    tree = HTMLParser(html)
    tr_nodes = tree.css("tr")
    if not tr_nodes:
        return None
    grid: dict[tuple[int, int], str] = {}
    occupied: set[tuple[int, int]] = set()
    cols = 0
    saw_cell = False
    for row, tr in enumerate(tr_nodes):
        col = 0
        for cell in tr.css("td, th"):
            saw_cell = True
            while (row, col) in occupied:
                col += 1
            colspan = _parse_span(cell.attributes.get("colspan"))
            rowspan = _parse_span(cell.attributes.get("rowspan"))
            grid[(row, col)] = _clean_cell_text(cell.text(separator=" "))
            for r in range(row, row + rowspan):
                for c in range(col, col + colspan):
                    if (r, c) != (row, col):
                        grid.setdefault((r, c), "")
                    occupied.add((r, c))
            col += colspan
            cols = max(cols, col)
    if not saw_cell or cols == 0:
        return None
    rows = len(tr_nodes)
    # 全空表(结构模型对非表格图的退化输出)与「未检出表格」同待遇:None。
    if all(not text.strip() for text in grid.values()):
        return None
    lines = [
        "|" + "|".join(grid.get((r, c), "") for c in range(cols)) + "|"
        for r in range(rows)
    ]
    markdown = "\n".join([lines[0], "|" + "---|" * cols, *lines[1:]])
    return TableResult(markdown=markdown, rows=rows, cols=cols)


def _reset_engines() -> None:
    """测试钩子:清引擎单例(sys.modules 假引擎注入后必须重置,防串台)。"""
    global _TABLE_ENGINE, _OCR_ENGINE
    with _INFERENCE_LOCK:
        _TABLE_ENGINE = None
        _OCR_ENGINE = None
