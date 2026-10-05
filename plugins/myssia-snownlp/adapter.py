"""myssia-snownlp 适配器:uv 隔离子进程调用上游 snownlp(MIT)——MYIA 侧代码.

本文件由 MYIA 仓库创作与维护,**不是**上游代码;上游 snownlp
(isnowfy/snownlp,MIT)不 vendor、不复制,以 ``uv run --no-project --with
snownlp==0.12.3`` 的 pip 依赖形态隔离调用,依赖只进 uv 缓存的临时环境,
绝不进根依赖。**版本钉死**(gate: stale 的停更纪律:上游 2020-01-19 后
冻结,pin 号 = 2026-10-05 收录时 PyPI 末版亲核)。

分析 lane 契约(task 10-05-plugin-market-batch 批三 D10;契约面见
:mod:`myssia.analysis_lane`):暴露 ``decorate(texts)``——对一批
``{"url", "text"}`` 做中文情感装饰,输出 ``{"decorations": {url:
{"sentiment_score": 0..1, "sentiment_label": "正面"|"负面"}}}``。
**每轮单次 spawn** stdin JSON 批处理:snownlp import 即载训练模型,逐条
spawn 会反复载模(纪律在 manifest 注释与 design §7.3)。

上游契约(2026-10-05 对 snownlp 0.12.3 源码面核):

- ``SnowNLP(text).sentiments`` 返回贝叶斯正面概率(0..1,越高越正面);
- 情感模型按句切分训练语料,长文整段代入既慢又稀释放大——shim 侧截前
  :data:`MAX_TEXT_CHARS` 字符(装饰件,不追求全文精度);
- 空文本/不可解析条目**跳过不装饰**(装饰失败 ≠ 条目失败,lane 对缺装饰
  条目零动作)。

错误契约(spec python/error-handling,词表照 urlwatch):所有失败抛
:class:`SnownlpAdapterError`(code + message + 结构化 details)。code 词表:

- ``texts_invalid``       输入形状非法(非列表/缺 url/超上限)
- ``uv_missing``          宿主无 uv(隔离运行时不可用=上游依赖缺失的结构化形态)
- ``snownlp_failed``      子进程非零退出(spawn/装载/执行失败)
- ``snownlp_timeout``     子进程超过 wall-clock 预算
- ``snownlp_output_invalid``  退出 0 但 stdout 不是可解析的装饰 JSON

零装饰(全部条目被跳过)= 合法空态,不是错误。铁律:任何失败只影响本次
调用,核心品类流水线照常跑通(测试钉在 tests/plugins/test_analysis_plugins.py,
全 mock 子进程零网络)。

采集边界:纯本地装饰,零网络、零凭据、零第三方服务器(P0 本地执行硬规则)。
"""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

__all__ = [
    "DEFAULT_TIMEOUT_SECONDS",
    "MAX_TEXT_CHARS",
    "MAX_TEXTS_PER_RUN",
    "SNOWNLP_DEPENDENCIES",
    "SNOWNLP_PIN",
    "SHIM_SOURCE",
    "SnownlpAdapterError",
    "build_command",
    "decorate",
    "is_available",
    "plugin_dir",
]

#: 适配器所在插件目录(样板布局固定在 plugins/myssia-snownlp/ 下)。
PLUGIN_DIR = Path(__file__).resolve().parent

#: 上游钉版(gate: stale 停更纪律;2026-10-05 收录时 PyPI 末版亲核)。
SNOWNLP_PIN = "0.12.3"

#: 隔离子进程注入的上游依赖(钉版见模块 docstring)。
SNOWNLP_DEPENDENCIES = (f"snownlp=={SNOWNLP_PIN}",)

#: 单次批处理条目上限(桌面缺省必须有界;更多条目分轮跑)。
MAX_TEXTS_PER_RUN = 256

#: 单条文本截断上限(情感模型对长文既慢又稀释放大;装饰件不追求全文精度)。
MAX_TEXT_CHARS = 1200

#: 子进程 wall-clock 预算缺省值(载模 ~1-2s + 逐条贝叶斯推断的有界预算)。
DEFAULT_TIMEOUT_SECONDS = 120.0

#: 结构化错误/trace 的截断上限。
_TEXT_TAIL_CHARS = 2000


class SnownlpAdapterError(Exception):
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


def is_available() -> bool:
    """运行前提是否就位:宿主有 uv(上游依赖经 uv 临时环境注入)."""
    return shutil.which("uv") is not None


def _normalize_texts(texts: Any) -> list[dict[str, str]]:
    """校验并规整输入:``[{"url": str, "text": str}]``(text 可为空串).

    Raises:
        SnownlpAdapterError: ``texts_invalid``(非列表/元素形状不对/超上限)。
    """
    if not isinstance(texts, (list, tuple)):
        raise SnownlpAdapterError(
            "texts_invalid",
            f"texts 应为 {{url, text}} 映射列表,当前为 {type(texts).__name__}",
        )
    if len(texts) > MAX_TEXTS_PER_RUN:
        raise SnownlpAdapterError(
            "texts_invalid",
            f"单次批处理最多 {MAX_TEXTS_PER_RUN} 条(当前 {len(texts)}),更多条目分轮跑",
        )
    normalized: list[dict[str, str]] = []
    for entry in texts:
        if not isinstance(entry, dict) or not isinstance(entry.get("url"), str) or not entry["url"]:
            raise SnownlpAdapterError(
                "texts_invalid",
                f"texts 条目非法(须为含非空 url 字符串的映射):{entry!r}",
            )
        text = entry.get("text")
        if text is not None and not isinstance(text, str):
            raise SnownlpAdapterError(
                "texts_invalid",
                f"texts 条目 text 字段须为字符串:{entry.get('url')!r}",
            )
        normalized.append({"url": entry["url"], "text": (text or "").strip()})
    return normalized


#: 隔离环境内跑的 MYIA 薄 shim(**非上游代码**):stdin 读 JSON 批,逐条
#: ``SnowNLP(text).sentiments`` 贝叶斯正面概率,stdout 只打印一个 JSON 对象
#: (上游无 logging 配置,stderr 旁路不承载协议)。
SHIM_SOURCE = '''\
"""MYIA shim: batch snownlp sentiment over stdin JSON (runs inside uv temp env)."""
import json
import sys

from snownlp import SnowNLP

MAX_TEXT_CHARS = 1200

payload = json.load(sys.stdin)
decorations = {}
for entry in payload.get("texts", []):
    url = entry.get("url")
    text = (entry.get("text") or "").strip()[:MAX_TEXT_CHARS]
    if not isinstance(url, str) or not url or not text:
        continue  # 空文本/无 url:跳过不装饰(缺装饰 != 条目失败)
    try:
        score = float(SnowNLP(text).sentiments)
    except Exception:  # noqa: BLE001 - 单条失败只丢该条装饰,不废整批
        continue
    decorations[url] = {
        "sentiment_score": round(score, 4),
        "sentiment_label": "正面" if score >= 0.5 else "负面",
    }
print(json.dumps({"decorations": decorations}, ensure_ascii=False))
'''


def build_command(shim_path: str | Path) -> list[str]:
    """装配隔离子进程命令:uv 临时环境跑 MYIA shim(钉版 snownlp)."""
    command = ["uv", "run", "--no-project"]
    for dependency in SNOWNLP_DEPENDENCIES:
        command += ["--with", dependency]
    command += ["python", str(shim_path)]
    return command


def _tail(text: str | None, limit: int = _TEXT_TAIL_CHARS) -> str:
    """文本摘录(尾部),保持结构化结果有界."""
    return (text or "").strip()[-limit:]


def decorate(
    texts: Any,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    runner: Callable[..., subprocess.CompletedProcess[str]] | None = None,
    clock: Callable[[], float] = time.monotonic,
) -> dict[str, Any]:
    """对 ``texts`` 跑一次批量中文情感装饰(单次 spawn stdin JSON 批处理).

    Args:
        texts: ``[{"url": str, "text": str}]``(text 可空=跳过不装饰)。
        timeout: 子进程 wall-clock 预算秒数,超时抛 ``snownlp_timeout``。
        runner: subprocess.run 注入口(测试 mock 用)。
        clock: 单调时钟注入口(测试 mock 用)。

    Returns:
        结构化结果 dict:plugin/decorations(``{url: {"sentiment_score",
        "sentiment_label"}}``)/decorated/skipped/command/exit_code/
        duration_seconds/snownlp_pin。

    Raises:
        SnownlpAdapterError: 全部失败形态都是结构化错误(见模块 docstring 词表)。
        零装饰(全部跳过)不是错误:decorations 为空映射。
    """
    do_run = runner if runner is not None else subprocess.run
    entries = _normalize_texts(texts)
    if shutil.which("uv") is None:
        raise SnownlpAdapterError(
            "uv_missing",
            "隔离运行时不可用: PATH 上找不到 uv(https://docs.astral.sh/uv/)。"
            "适配器以 uv 临时环境钉版运行上游 snownlp,依赖不进根依赖。",
            texts=len(entries),
        )
    started = clock()
    with tempfile.TemporaryDirectory(prefix="myssia-snownlp-") as scratch:
        shim_path = Path(scratch) / "shim.py"
        shim_path.write_text(SHIM_SOURCE, encoding="utf-8")
        command = build_command(shim_path)
        try:
            completed = do_run(
                command,
                input=json.dumps({"texts": entries}, ensure_ascii=False),
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise SnownlpAdapterError(
                "snownlp_timeout",
                f"snownlp 子进程超过 {timeout:g}s 预算被终止({len(entries)} 条)",
                timeout_seconds=timeout,
                text_count=len(entries),
                stderr_tail=_tail(exc.stderr if isinstance(exc.stderr, str) else None),
            ) from exc
        duration = round(clock() - started, 3)
        if completed.returncode != 0:
            raise SnownlpAdapterError(
                "snownlp_failed",
                f"snownlp 子进程非零退出(code={completed.returncode};{len(entries)} 条)",
                exit_code=completed.returncode,
                stderr_tail=_tail(completed.stderr),
                stdout_tail=_tail(completed.stdout),
            )
        try:
            payload = json.loads(completed.stdout)
        except (json.JSONDecodeError, ValueError) as exc:
            raise SnownlpAdapterError(
                "snownlp_output_invalid",
                f"shim stdout 不是可解析 JSON:{exc}",
            ) from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("decorations"), dict):
            raise SnownlpAdapterError(
                "snownlp_output_invalid",
                f"shim 输出形状不对(缺 decorations 映射):{str(completed.stdout)[:120]!r}",
            )
    decorations = payload["decorations"]
    return {
        "plugin": "myssia-snownlp",
        "decorations": decorations,
        "decorated": len(decorations),
        "skipped": max(0, len(entries) - len(decorations)),
        "command": command,
        "exit_code": completed.returncode,
        "duration_seconds": duration,
        "snownlp_pin": SNOWNLP_PIN,
    }
