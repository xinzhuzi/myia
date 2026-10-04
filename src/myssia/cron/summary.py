"""cron 运行摘要:RunResult 精简 + markdown 模板 + 定向投递(design §5)。

MYIA 移植重写自 Hermes(NousResearch/Hermes-Agent,MIT;上游路径
``~/.hermes/hermes-agent/cron/``):

- ``cron/scheduler.py`` ``_summarize_cron_failure_for_delivery`` H:289 ——
  失败摘要的文案纪律:告警卡只带**一行式有界摘要**(错误剥壳、空白折叠、
  截断),全量细节留在 run 输出目录;上游的 provider 分类器/incidents/
  quota_hold 提示族是 LLM agent 故障面专属物,不搬(D7)。
- ``cron/scheduler.py`` ``_compose_run_delivery`` H:2928 —— 成功投运行
  内容、失败投告警的分流思路;上游的 origin 回投/delivery_queue/
  blocked-config 静默族不搬(D4/D5)。

MYIA 形态(10-04-hermes-cron design §3.2 步骤 5 / §5,grill Q3):

- 摘要数据**全部**来自 ``RunResult.to_dict()``(子进程 ``--json`` stdout,
  ground-truth A1)——本模块只做归约(计数/截断),零新统计;
- markdown 版式 spec 固定(design §5 八字段),非用户模板——Jinja 侧仅
  ``CRON_SUMMARY_TEMPLATE`` 一个透传模板(把伪条目携带的 markdown 原样
  交给通道渲染器:feishu 走 ``build_markdown_card`` 直载 A7、telegram 走
  纯文本),通道构造凭据走默认 env/keychain 引用链(§8.1 直构裁决,
  push.test 先例 entry.py);
- 投递失败返回结构化错误文本(**不抛**):调用方(runner)把它记作
  ``delivery_error`` 三态,运行成败不被投递波及(F1.7)。
"""

from __future__ import annotations

import asyncio
import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Optional

from myssia.push import PLATFORMS, StdoutChannel
from myssia.push.base import SendContext, clip_text
from myssia.push.delivery import DeliveryLedger, send_batch_to_targets
from myssia.push.directory import ChannelDirectory
from myssia.push.targets import parse_spec

logger = logging.getLogger(__name__)

__all__ = [
    "CRON_SUMMARY_TEMPLATE",
    "FAILURE_ERROR_CLIP_CHARS",
    "SUMMARY_FAILURE_LINE_CLIP",
    "SUMMARY_FAILURE_LINE_LIMIT",
    "SUMMARY_STATUS_LABELS",
    "deliver_run_summary",
    "render_failure_markdown",
    "render_summary_markdown",
    "summarize_run",
]

#: 摘要卡透传模板:把伪条目携带的 markdown 原样交给通道渲染器。feishu 侧
#: ``FeishuCardChannel._build_card`` 模板路径 → ``build_markdown_card`` 直载
#: (A7);telegram 侧模板渲染产物按纯文本发送(design §5)。StrictUndefined
#: 保证伪条目缺 ``markdown`` 键时炸成结构化 ``template_render_error`` 而
#: 不是静默空卡。
CRON_SUMMARY_TEMPLATE = "{{ items[0]['markdown'] }}"

#: 失败摘要行上限与单行截断(design §5「失败摘要行截断」;上游 180 字符
#: 一行式纪律的同款量级)。
SUMMARY_FAILURE_LINE_LIMIT = 5
SUMMARY_FAILURE_LINE_CLIP = 120

#: 失败告警错误正文的截断(上游 generic_failure_notice 的 180 字符同款纪律)。
FAILURE_ERROR_CLIP_CHARS = 180

#: 摘要状态 → 卡面文案(emoji + 机器值;ok|partial|failed 三值,design §5)。
SUMMARY_STATUS_LABELS = {
    "ok": "✅ ok",
    "partial": "🟡 partial",
    "failed": "❌ failed",
}


# ---------------------------------------------------------------------------
# RunResult → 精简摘要(design §3.2 步骤 3;零新统计,只做归约)
# ---------------------------------------------------------------------------


def summarize_run(
    job: Mapping[str, Any],
    *,
    payload: Optional[Mapping[str, Any]],
    exit_code: Optional[int],
    timed_out: bool = False,
    error: Optional[str] = None,
) -> dict[str, Any]:
    """把一次子进程运行归约为摘要 dict(design §5 八字段的数据面)。

    Args:
        job: 派发快照(id/name/category/deliver…)。
        payload: ``RunResult.to_dict()``(``--json`` stdout 解析物);失败路径
            可能为 None(超时/无法解析/退出码 1 的错误 JSON)。
        exit_code: 子进程退出码(None = 无法拿到,如 spawn 失败)。
        timed_out: 墙钟超时(D12)。
        error: 运行错误文本(超时/解析失败/退出码非 0 时的结构化原因)。

    Returns:
        JSON 可落盘的纯 dict(runs 摘要快照 / markdown 渲染 / 投递共用)。
    """
    sources = payload.get("sources") if isinstance(payload, Mapping) else None
    sources = [s for s in (sources or []) if isinstance(s, Mapping)]
    failed_sources = [s for s in sources if s.get("failed")]
    pushes = (
        [p for p in (payload.get("push") or []) if isinstance(p, Mapping)]
        if isinstance(payload, Mapping)
        else []
    )
    failures = (
        [f for f in (payload.get("failures") or []) if isinstance(f, Mapping)]
        if isinstance(payload, Mapping)
        else []
    )
    duration = payload.get("duration_seconds") if isinstance(payload, Mapping) else None

    if timed_out:
        status = "failed"
    elif exit_code == 0:
        status = "ok"
    elif exit_code == 3:
        # CLI 契约 3 = partial:按 job 语义算成功,附注 partial(design §3.2 步骤 4)。
        status = "partial"
    else:
        status = "failed"

    return {
        "job": {
            "id": str(job.get("id") or ""),
            "name": str(job.get("name") or job.get("id") or "cron job"),
            "category": str(job.get("category") or ""),
        },
        "run": {
            "status": status,
            "exit_code": exit_code,
            "timed_out": bool(timed_out),
            "run_id": payload.get("run_id") if isinstance(payload, Mapping) else None,
            "dry_run": bool(payload.get("dry_run"))
            if isinstance(payload, Mapping)
            else bool(job.get("dry_run")),
            "duration_seconds": duration,
            "error": error,
        },
        "sources": {
            "total": len(sources),
            "ok": len(sources) - len(failed_sources),
            "failed": len(failed_sources),
            "items": sum(int(s.get("item_count") or 0) for s in sources),
        },
        "items_retained": len(payload.get("items") or [])
        if isinstance(payload, Mapping)
        else 0,
        "push": [
            {
                "channel": str(p.get("channel") or ""),
                "ok": bool(p.get("ok", True)),
                "immediate": int(p.get("immediate") or 0),
                "digest": int(p.get("digest") or 0),
                "archive": int(p.get("archive") or 0),
            }
            for p in pushes
        ],
        "failures": [
            clip_text(
                "{source} · {error_type} · {message}".format(
                    source=str(f.get("source") or "?"),
                    error_type=str(f.get("error_type") or "error"),
                    message=str(f.get("message") or ""),
                ),
                SUMMARY_FAILURE_LINE_CLIP,
            )
            for f in failures[:SUMMARY_FAILURE_LINE_LIMIT]
        ],
        "failure_count": len(failures),
    }


# ---------------------------------------------------------------------------
# markdown 模板(design §5:job 名/品类/状态/时长/源统计/留存/push 桶/失败行)
# ---------------------------------------------------------------------------


def _job_label(summary: Mapping[str, Any]) -> tuple[str, str]:
    job = summary.get("job") or {}
    name = str(job.get("name") or "cron job")
    category = str(job.get("category") or "")
    return name, category


def render_summary_markdown(summary: Mapping[str, Any]) -> str:
    """运行摘要 markdown(成功/部分成功共用;版式 spec 固定,零用户模板)。"""
    name, category = _job_label(summary)
    run = summary.get("run") or {}
    sources = summary.get("sources") or {}
    lines = [
        f"**{name}** · 定时运行摘要",
        f"- 品类:{category or '(未知)'}",
        "- 状态:{label} · 退出码 {exit}{note}".format(
            label=SUMMARY_STATUS_LABELS.get(
                str(run.get("status")), str(run.get("status"))
            ),
            exit=run.get("exit_code") if run.get("exit_code") is not None else "n/a",
            note=" · ⏱ 墙钟超时被终止" if run.get("timed_out") else "",
        ),
    ]
    duration = run.get("duration_seconds")
    if isinstance(duration, (int, float)):
        lines.append(f"- 时长:{duration:.1f}s")
    if run.get("dry_run"):
        lines.append("- 模式:dry-run(零持久化)")
    lines.append(
        "- 源:{total} 个,正常 {ok} / 失败 {failed},采集条目 {items}".format(
            total=sources.get("total", 0),
            ok=sources.get("ok", 0),
            failed=sources.get("failed", 0),
            items=sources.get("items", 0),
        )
    )
    lines.append(f"- 条目留存:{summary.get('items_retained', 0)}")
    for push in summary.get("push") or []:
        lines.append(
            "- 推送:{channel}(immediate {immediate} / digest {digest} / archive {archive}{ok})".format(
                channel=push.get("channel") or "?",
                immediate=push.get("immediate", 0),
                digest=push.get("digest", 0),
                archive=push.get("archive", 0),
                ok="" if push.get("ok", True) else " · 发送失败",
            )
        )
    failures = list(summary.get("failures") or [])
    if failures:
        total = summary.get("failure_count") or len(failures)
        lines.append(f"- 失败摘要(共 {total} 条,示前 {len(failures)} 条):")
        lines.extend(f"  - {line}" for line in failures)
    return "\n".join(lines)


def render_failure_markdown(
    summary: Mapping[str, Any],
    *,
    stderr_tail: Optional[list[str]] = None,
    output_path: Optional[Path] = None,
) -> str:
    """失败告警 markdown(上游一行式告警纪律:有界、剥壳、细节留档)。

    Args:
        summary: :func:`summarize_run` 产物(取 job/错误/streak 面)。
        stderr_tail: 子进程 stderr 尾部行(runner 已截好;缺省无)。
        output_path: 本 run 输出文档路径(告警里指路,全量细节所在)。
    """
    name, category = _job_label(summary)
    run = summary.get("run") or {}
    error_text = str(run.get("error") or "unknown error")
    lines = [
        f"**{name}** · 定时运行失败",
        f"- 品类:{category or '(未知)'}",
        "- 状态:{label} · 退出码 {exit}".format(
            label=SUMMARY_STATUS_LABELS.get(
                str(run.get("status")), str(run.get("status"))
            ),
            exit=run.get("exit_code") if run.get("exit_code") is not None else "n/a",
        ),
        f"- 错误:{clip_text(error_text, FAILURE_ERROR_CLIP_CHARS)}",
    ]
    if run.get("timed_out"):
        lines.append("- ⏱ 墙钟超时被终止(run_timeout)")
    if stderr_tail:
        lines.append("- 日志尾部:")
        lines.extend(
            f"  - {clip_text(line, SUMMARY_FAILURE_LINE_CLIP)}" for line in stderr_tail
        )
    if output_path is not None:
        lines.append(f"- 详情:{output_path}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 定向投递(design §3.2 步骤 5;宿主进程内 asyncio.run + 平台直构)
# ---------------------------------------------------------------------------


def _build_summary_item(
    markdown: str, *, job: Mapping[str, Any], now: datetime
) -> dict[str, Any]:
    """摘要伪条目:通道收到的「一条消息载荷」(markdown 原文由透传模板取回)。"""
    return {
        "title": f"cron summary {job.get('name') or job.get('id') or ''}".strip(),
        "markdown": markdown,
        "source": "cron",
        "category": None,
        "dedup_key": "cron-summary-{jid}-{stamp}".format(
            jid=job.get("id") or "?", stamp=now.strftime("%Y%m%d%H%M%S")
        ),
        "url": None,
    }


def _deliver_summary_via_stdout(
    item: dict[str, Any], context: SendContext
) -> Optional[str]:
    """stdout 系 deliver spec 的特殊分支(design §8.1 末条)。

    stdout 通道在 :data:`CHANNELS` 但**永不支持寻址**(``supports_targeting
    = False``,不入 :data:`PLATFORMS`)——spec 的 ref 段无寻址意义,一行
    JSON 直接发,不入 ``send_batch_to_targets`` 的解析/死信路径(stdout 无
    传输失败面)。serve 模式下直写 stdout 会污染 sidecar 协议流:卡片行入
    内存缓冲(``out=StringIO`` 注入,push.test 先例 entry.py ``_m_push_test``
    的同款特殊分支),经 logger 回显(stderr 日志面,CLI/桌面双宿主一致
    可见),协议流零污染。
    """
    buffer = io.StringIO()
    channel = StdoutChannel(template=CRON_SUMMARY_TEMPLATE, out=buffer)
    try:
        asyncio.run(channel.send([item], context))
    except Exception as exc:  # noqa: BLE001 - 三态语义同主路径:投递崩不上抛
        logger.error(
            "Cron 摘要投递异常(stdout 通道): %s", exc, exc_info=True
        )
        return f"[delivery_crashed] {type(exc).__name__}: {exc}"
    for line in buffer.getvalue().splitlines():
        if line.strip():
            logger.info("Cron 摘要(stdout 通道回显): %s", line)
    return None


def deliver_run_summary(
    spec: str,
    markdown: str,
    *,
    job: Mapping[str, Any],
    data_root: Path,
    now: datetime,
) -> Optional[str]:
    """把一段摘要 markdown 定向投递到 *spec*;失败返回错误文本,绝不抛。

    - ``"local"`` / 空 → ``None``(本地落盘由 runner 的输出文档承担,D4);
    - ``"stdout:<任意>"`` → stdout 特殊分支(§8.1 末条:入内存缓冲 +
      logger 回显,协议流零污染——见 :func:`_deliver_summary_via_stdout`);
    - 平台 spec(``feishu:群名`` / ``telegram:12345``)→ 通道按
      :data:`myssia.push.PLATFORMS` 直构(凭据走通道默认 env/keychain 引用链,
      §8.1),``send_batch_to_targets`` 逐对象发送 + 死信语义;SendContext
      ``kind="cron_summary"``(grill Q3)、slot/date 按 *now* 本地。
    """
    spec_text = str(spec or "").strip()
    if not spec_text or spec_text.lower() == "local":
        return None
    try:
        platform, _ = parse_spec(spec_text)
    except Exception as exc:  # noqa: BLE001 - spec 坏 = 投递失败,不上抛
        return f"[bad_deliver_spec] {type(exc).__name__}: {exc}"

    context = SendContext(
        slot="am" if now.hour < 12 else "pm",
        date=now.strftime("%Y-%m-%d"),
        category=None,
        kind="cron_summary",
    )
    item = _build_summary_item(markdown, job=job, now=now)
    if platform == "stdout":
        return _deliver_summary_via_stdout(item, context)

    channel_cls = PLATFORMS.get(platform)
    if channel_cls is None:
        return (
            f"[unknown_platform] deliver spec 平台 {platform!r} 未注册"
            f"(可用:{sorted(PLATFORMS)})"
        )
    try:
        channel = channel_cls(template=CRON_SUMMARY_TEMPLATE)
    except TypeError:
        # 构造器不接受 template 的通道:裸构降级,伪条目走通道自带版式。
        channel = channel_cls()

    try:
        reports = asyncio.run(
            send_batch_to_targets(
                [item],
                specs=[spec_text],
                channel=channel,
                context=context,
                directory=ChannelDirectory(data_root),
                ledger=DeliveryLedger(data_root),
            )
        )
    except Exception as exc:  # noqa: BLE001 - 三态语义:投递崩了也不带走运行成败
        logger.error(
            "Cron 摘要投递异常: job=%s spec=%s error=%s",
            job.get("id"),
            spec_text,
            exc,
            exc_info=True,
        )
        return f"[delivery_crashed] {type(exc).__name__}: {exc}"
    errors = [str(r.error) for r in reports if not r.ok]
    if errors:
        return "; ".join(errors)
    logger.info("Cron 摘要已投递: job=%s spec=%s", job.get("id"), spec_text)
    return None
