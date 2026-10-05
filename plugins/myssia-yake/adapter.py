"""myssia-yake 适配器:进程内惰性 import 上游 yake(AGPL-3.0 免费档)——MYIA 侧代码.

本文件由 MYIA 仓库创作与维护,**不是**上游代码;上游 yake(LIAAD/yake,
AGPL-3.0 免费档+商业双轨,2026-10-05 gh api LICENSE 原文核)不 vendor、
不复制,以**进程内惰性 import** 形态接入(credhunter 先例 engines/
credhunter.py:67)。AGPL 纪律(research 第五波裁定):只声明依赖零复制,
pip 运行时自装不构成分发。

安装形态:上游不随包分发、不进根依赖——启用前用户自行装进宿主环境
(``uv pip install yake``,2026-10-05 PyPI 末版 0.7.3);**未装 =
``dependency_missing`` 条目级降级 warning**,绝不拦核心(铁律)。

分析 lane 契约(task 10-05-plugin-market-batch 批三 D10;契约面见
:mod:`myssia.analysis_lane`):暴露 ``decorate(texts)``——对一批
``{"url", "text"}`` 做无监督关键词抽取,输出 ``{"decorations": {url:
{"keywords": [词, ...]}}}``。

上游契约(2026-10-05 对 yake 0.7.3 源码面核):

- ``yake.KeywordExtractor(lan=..., n=3, top=N)``.extract_keywords(text)
  返回 ``[(keyword, score), ...]``(score 越低越重要),lan 词表含
  ``zh``(StopwordsList/stopwords_zh.txt 在位);
- YAKE 的分词器(segtok)面向空格分隔文本,中文连续段落会被当成整句
  单 token——适配器在抽取前做 **CJK 逐字切分**(连续汉字间插空格,
  ASCII 词保持完整),否则中文源抽出的「关键词」是整段话;
- 装饰件定位:关键词是启发式抽取(route 规则/模板的辅助信号),不是
  分类依据——装饰不过滤。

错误契约(spec python/error-handling,词表照 urlwatch):所有失败抛
:class:`YakeAdapterError`(code + message + 结构化 details)。code 词表:

- ``texts_invalid``       输入形状非法(非列表/缺 url/超上限)
- ``dependency_missing``  宿主未装 yake(安装指引随 message)
- ``yake_failed``         抽取执行失败

零关键词(空文本全跳过)= 合法空态,不是错误。铁律:任何失败只影响本次
调用,核心品类流水线照常跑通(测试钉在 tests/plugins/test_analysis_plugins.py,
mock import 零网络)。

采集边界:纯本地装饰,零网络、零凭据、零第三方服务器(P0 本地执行硬规则)。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

__all__ = [
    "DEFAULT_KEYWORDS_TOP",
    "DEFAULT_LANGUAGE",
    "MAX_TEXTS_PER_RUN",
    "YAKE_INSTALL_HINT",
    "YakeAdapterError",
    "decorate",
    "normalize_text",
    "plugin_dir",
]

#: 适配器所在插件目录(样板布局固定在 plugins/myssia-yake/ 下)。
PLUGIN_DIR = Path(__file__).resolve().parent

#: 缺省语言(YAKE 0.7.3 StopwordsList 含 zh;MYIA 官方品类以中文源为主)。
DEFAULT_LANGUAGE = "zh"

#: 缺省每条目抽取的关键词上限(装饰件,克制输出)。
DEFAULT_KEYWORDS_TOP = 5

#: 单次批处理条目上限(桌面缺省必须有界)。
MAX_TEXTS_PER_RUN = 256

#: 未装 yake 的安装指引(message 随行,agent 可自修)。
YAKE_INSTALL_HINT = "uv pip install yake(进宿主环境,不进根依赖;PyPI 末版 0.7.3)"

#: 连续 CJK 字符间插空格(YAKE 的 segtok 分词器面向空格分隔文本;中文连续
#: 段落会被当成整句单 token,不切分则中文「关键词」是整段话)。ASCII 词与
#: 标点原样保留。
_CJK_BETWEEN_RE = re.compile(r"([\u3400-\u9fff\uf900-\ufaff])(?=[\u3400-\u9fff\uf900-\ufaff])")

#: 结构化错误消息的截断上限。
_TEXT_TAIL_CHARS = 500


class YakeAdapterError(Exception):
    """结构化适配器错误:code + message + details,``to_dict()`` 进 JSON 输出."""

    def __init__(self, code: str, message: str, **details: Any) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        """结构化形态:{"code", "message", **details}(供 --json 输出与 agent 自修)."""
        return {"code": self.code, "message": self.message, **self.details}


def plugin_dir() -> Path:
    """本插件目录(适配器所在处)."""
    return PLUGIN_DIR


def normalize_text(text: str) -> str:
    """CJK 逐字切分(连续汉字间插空格,ASCII 词保持完整)——YAKE 中文前置。"""
    return _CJK_BETWEEN_RE.sub(r"\1 ", text)


def _normalize_texts(texts: Any) -> list[dict[str, str]]:
    """校验并规整输入:``[{"url": str, "text": str}]``(text 可为空串).

    Raises:
        YakeAdapterError: ``texts_invalid``(非列表/元素形状不对/超上限)。
    """
    if not isinstance(texts, (list, tuple)):
        raise YakeAdapterError(
            "texts_invalid",
            f"texts 应为 {{url, text}} 映射列表,当前为 {type(texts).__name__}",
        )
    if len(texts) > MAX_TEXTS_PER_RUN:
        raise YakeAdapterError(
            "texts_invalid",
            f"单次批处理最多 {MAX_TEXTS_PER_RUN} 条(当前 {len(texts)}),更多条目分轮跑",
        )
    normalized: list[dict[str, str]] = []
    for entry in texts:
        if not isinstance(entry, dict) or not isinstance(entry.get("url"), str) or not entry["url"]:
            raise YakeAdapterError(
                "texts_invalid",
                f"texts 条目非法(须为含非空 url 字符串的映射):{entry!r}",
            )
        text = entry.get("text")
        if text is not None and not isinstance(text, str):
            raise YakeAdapterError(
                "texts_invalid",
                f"texts 条目 text 字段须为字符串:{entry.get('url')!r}",
            )
        normalized.append({"url": entry["url"], "text": (text or "").strip()})
    return normalized


def decorate(
    texts: Any,
    *,
    top: int = DEFAULT_KEYWORDS_TOP,
    language: str = DEFAULT_LANGUAGE,
) -> dict[str, Any]:
    """对 ``texts`` 跑一次批量关键词抽取(进程内惰性 import yake).

    Args:
        texts: ``[{"url": str, "text": str}]``(text 可空=跳过不装饰)。
        top: 每条目关键词上限(缺省 :data:`DEFAULT_KEYWORDS_TOP`)。
        language: YAKE 语言(缺省 ``zh``;StopwordsList 词表内)。

    Returns:
        结构化结果 dict:plugin/decorations(``{url: {"keywords": [词, ...]}}``)/
        decorated/skipped/yake_version。

    Raises:
        YakeAdapterError: 全部失败形态都是结构化错误(见模块 docstring 词表)。
        零关键词(全部跳过)不是错误:decorations 为空映射。
    """
    entries = _normalize_texts(texts)
    try:
        import yake  # 惰性 import(credhunter 先例):gate 关时零装载,lane 装载在 gate 判定后
    except ImportError as exc:
        raise YakeAdapterError(
            "dependency_missing",
            f"上游 yake 未安装(进程内件需宿主环境可 import):{YAKE_INSTALL_HINT}",
            install_hint=YAKE_INSTALL_HINT,
        ) from exc
    extractor = yake.KeywordExtractor(lan=language, n=3, top=max(1, int(top)))
    decorations: dict[str, dict[str, Any]] = {}
    for entry in entries:
        text = entry["text"]
        if not text:
            continue  # 空文本:跳过不装饰(缺装饰 != 条目失败)
        try:
            ranked = extractor.extract_keywords(normalize_text(text))
        except Exception as exc:  # noqa: BLE001 - 单条失败只丢该条装饰,不废整批
            continue
        keywords = [keyword for keyword, _score in ranked if keyword and keyword.strip()]
        if not keywords:
            continue
        decorations[entry["url"]] = {"keywords": keywords[: max(1, int(top))]}
    return {
        "plugin": "myssia-yake",
        "decorations": decorations,
        "decorated": len(decorations),
        "skipped": max(0, len(entries) - len(decorations)),
        "yake_version": getattr(yake, "__version__", None),
    }
