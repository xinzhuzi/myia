"""微信本机通道(``weixin-local``;task 10-11-wechat-ui-bridge Phase F1,G7 命名)。

蓝本 = 同包 :mod:`myssia.push.weixin`(官方 Hermes iLink 桥,**出站主口**)。
调用形态逐条对齐蓝本:一次性子进程、正文经 stdin(argv 不携带内容,日志可
安全打 argv)、超时 kill 兜底、模板渲染对齐(TemplateRenderer 在场走模板,
缺省内置纯文本版式 ``build_message``)、显式可选(构造期零文件系统检查,
无桥环境配置照常加载)。与蓝本的差异如实落档,不静默:

- **定位(prd R2 定案)**:weixin-local 是**同机便捷补充**,不是主出站口——
  程序化出站的合规位由官方 iLink 通道(research §4)站住;本通道缺省关
  (schema ``weixin_local_enabled``,缺省 False,加载期 fail-fast),
  关闭 = 通道不注册,UI 卡显灰。
- **桥 = 受管组件 wechat-bridge**(G7;``plugins/wechat-bridge/``,组件戳
  0.2.0):MYIA 只做子进程调用,不 vendor 任何上游代码(prd R5 红线)。
  CLI 契约 = 任务档 design §6(exit 三段 + 具名错误族 10/11/12/13/14/15/
  20/21/22/30;stdout 恒单 JSON),组件侧 ``--probe`` 三态判据矩阵与
  发送频控(G6:单条、硬间隔 ≥10s、无批量接口)都**在桥内**,MYIA 侧
  零复制零覆写——频控状态落盘桥的数据根(``send_state.json`` + flock),
  本模块不做任何频控(做了就是绕过桥内硬门)。
- **静默铁律(prd 红线 4)**由桥内实施(AX 属性读 + AX 动作,禁合成鼠标、
  禁激活窗口);MYIA 侧只递参数,零前台语义可违反。
- **超时**::data:`DEFAULT_BRIDGE_TIMEOUT_SECONDS` = 60s 模块常量,不设
  配置口。与蓝本 120s 的差异是刻意事实:Hermes 内部有重试嵌套(上界
  ≈105s)所以要盖住它,本桥一次性执行无重试嵌套,60s 对本地 AX/localdb
  单命令已宽裕;超时 → kill 兜底 + ``bridge_timeout`` 瞬态。
- **零死信**(蓝本 design D3 同款):桥错误族全是环境态(未运行/未授权/
  窗口未开/频控/密钥),没有 forbidden/not_found 语义 → 任何分支都不标
  dead;桥内错误文案全中文(见 ``wechat_bridge/codes.py``),与 core 死信
  分类器的 ASCII marker 表无交集(静态对账测试钉死)。

寻址:``supports_targeting = False``(无目录寻址——桥的会话列表是只读
浏览面,不是推送地址簿;targets spec 的平台前缀词表 ``[a-z][a-z0-9_]*``
也容不下连字符)。会话寻址 = legacy ``target`` 引用(缺省
:data:`DEFAULT_TARGET_ENV_REF`,发送期解析;schema 对无 CHANNEL_PLATFORMS
条目强制必填 target,webhook 同款)。目录无自动发现
(:class:`~myssia.push.directory.DirectoryDiscoverUnsupported`)。

纯 stdlib(asyncio 子进程);测试经 ``runner`` 注入点 mock,不触真桥
(真实子进程冒烟仅两条:fake bridge 回显预录 JSON 成功 / sleep 超时 kill)。
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Awaitable, Callable, Sequence

from myssia.push.base import PushSendError, SendContext, TrendAwareChannel
from myssia.push.directory import DirectoryDiscoverUnsupported
from myssia.push.ntfy import build_message
from myssia.push.templates import TemplateRenderError, TemplateRenderer
from myssia.schema import CredentialResolveError, resolve_credential

__all__ = [
    "DEFAULT_BRIDGE_BIN",
    "DEFAULT_BRIDGE_TIMEOUT_SECONDS",
    "DEFAULT_PROBE_TIMEOUT_SECONDS",
    "DEFAULT_TARGET_ENV_REF",
    "BridgeRunner",
    "LocalBridgeTimeoutError",
    "WeixinLocalChannel",
    "bin_path",
    "parse_bridge_payload",
    "probe_local_bridge",
    "run_bridge_command",
    "run_bridge_command_sync",
]

logger = logging.getLogger(__name__)

#: 桥接子进程超时上限(秒;模块常量,不设配置口)。与蓝本 120s 的差异是
#: 刻意事实:本桥一次性执行无上游重试嵌套,60s 对本地单命令已宽裕。
#: 超时 → kill + ``bridge_timeout`` 瞬态。
DEFAULT_BRIDGE_TIMEOUT_SECONDS = 60.0
#: ``--probe`` 探针超时(秒):探针零成本(进程存在性 + 版本号 + AX 自检 +
#: 窗口快照 + 落盘计数,不读消息内容),30s 纯防挂死兜底。
DEFAULT_PROBE_TIMEOUT_SECONDS = 30.0
#: 受管组件缺省 bin 路径(design §7;组件安装链路 = Phase B3,装到别处时
#: 用品类 YAML push 条目的 ``wechat_bridge_bin`` 覆写)。
DEFAULT_BRIDGE_BIN = "~/.myia/plugins/wechat-bridge/bin/wechat-bridge"
#: legacy 会话 id 引用缺省(发送期解析;与 weixin/ntfy/wecom 先例同构)。
DEFAULT_TARGET_ENV_REF = "env:WEIXIN_LOCAL_CHAT_ID"

#: runner 契约:async ``(argv, input_text, timeout) -> (exit_code, stdout, stderr)``。
#: 测试注入点;缺省 :func:`run_bridge_command`(asyncio 子进程)。
BridgeRunner = Callable[[Sequence[str], str, float], Awaitable["tuple[int, str, str]"]]

#: design §6 具名错误码 → exit 码(错误族判定以码名为主键;exit 0 却带
#: error 载荷的契约漂移场景也归对族)。与 wechat_bridge/codes.py 的
#: CODE_NAMES 互为镜像(桥不改表,本表不改)。
_CODE_NAME_TO_EXIT: dict[str, int] = {
    "usage": 2,
    "wechat_not_running": 10,
    "ax_permission_denied": 11,
    "screen_recording_denied": 11,
    "window_closed": 12,
    "ax_tree_empty": 13,
    "send_rate_limited": 14,
    "send_ax_focus_required": 15,
    "db_not_found": 20,
    "key_unavailable": 21,
    "decrypt_failed": 22,
    "timeout": 30,
}


class LocalBridgeTimeoutError(RuntimeError):
    """缺省 runner 的超时终态(子进程已 kill);通道层映射 ``bridge_timeout``。"""


def bin_path(bridge_bin: str | None) -> Path:
    """bin 路径规整(覆写值或缺省;``~`` 展开)。通道与 sidecar 适配层共用。"""
    return Path(bridge_bin or DEFAULT_BRIDGE_BIN).expanduser()


def parse_bridge_payload(stdout: str) -> dict[str, Any] | None:
    """桥 stdout → JSON 对象(恒单 JSON 契约;解析失败 = None,映射层兜底)。"""
    try:
        payload = json.loads(stdout) if stdout.strip() else None
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


def _require_executable(bin_path: Path) -> None:
    """发送期预检(蓝本同款:构造期零检查,探测只在发送期/UI 探测发生)。"""
    if not (bin_path.is_file() and os.access(bin_path, os.X_OK)):
        raise PushSendError(
            "bridge_unavailable",
            f"微信本机通道不可用:桥组件 bin 不存在或不可执行: {bin_path}。"
            "修复指引:到设置安装 wechat-bridge 组件(前置 brew install sqlcipher),"
            "或在品类 YAML 的 push 条目配 wechat_bridge_bin 指向桥 bin 路径",
        )


def parse_bridge_payload(stdout: str) -> dict[str, Any] | None:
    """桥 stdout → JSON 对象(恒单 JSON 契约;解析失败 = None,映射层兜底)。"""
    try:
        payload = json.loads(stdout) if stdout.strip() else None
    except ValueError:
        return None
    return payload if isinstance(payload, dict) else None


async def run_bridge_command(
    argv: Sequence[str], input_text: str, timeout: float
) -> tuple[int, str, str]:
    """缺省 runner(蓝本 :func:`myssia.push.weixin.run_bridge_command` 同款):
    ``asyncio.create_subprocess_exec`` + 超时 kill 兜底。

    正文经 stdin(UTF-8);环境原样继承(MYIA 不注入任何凭据)。超时 =
    :class:`LocalBridgeTimeoutError`(先 kill 再 reap,不留孤儿进程);
    argv[0] 不存在 = ``FileNotFoundError``(通道层归 ``bridge_unavailable``)。
    """
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input_text.encode("utf-8")), timeout=timeout
        )
    except asyncio.TimeoutError as exc:
        with contextlib.suppress(ProcessLookupError):  # 已退出的竞态:kill 落空无害
            proc.kill()
        await proc.wait()
        raise LocalBridgeTimeoutError(
            f"wechat-bridge 超过 {timeout:.0f}s 未退出,子进程已终止"
        ) from exc
    return (
        proc.returncode if proc.returncode is not None else 0,
        stdout.decode("utf-8", "replace"),
        stderr.decode("utf-8", "replace"),
    )


def run_bridge_command_sync(
    argv: Sequence[str], input_text: str = "", timeout: float = DEFAULT_PROBE_TIMEOUT_SECONDS
) -> tuple[int, str, str]:
    """同步 runner(sidecar handler 宿主是同步函数;``subprocess.run`` 超时
    自带 kill+reap)。仅 ``--probe`` 与只读命令族走这里;发送通道恒走异步
    runner(管线宿主是 asyncio)。
    """
    try:
        proc = subprocess.run(  # noqa: S603 - argv 由 MYIA 代码构造,非用户拼接
            list(argv),
            input=input_text.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise LocalBridgeTimeoutError(
            f"wechat-bridge 超过 {timeout:.0f}s 未退出,子进程已终止"
        ) from exc
    return (
        proc.returncode if proc.returncode is not None else 0,
        proc.stdout.decode("utf-8", "replace"),
        proc.stderr.decode("utf-8", "replace"),
    )


def probe_local_bridge(
    bridge_bin: str | None = None,
    *,
    timeout: float = DEFAULT_PROBE_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """跑受管组件 ``--probe`` 三态探针(design §2 判据矩阵;纯探测零读取)。

    返回桥 JSON 载荷原样(键序即组件 ``ProbeResult.to_payload``;消费方按
    ``state`` 映射 UI 三态)。桥缺席/超时/应答不可解析时返回**同形合成
    载荷**(state 恒 ``bridge_unavailable``),UI 永远拿到可渲染的三态,
    不裸抛——探针是健康面,健康面自己必须先健康。
    """
    resolved_bin = bin_path(bridge_bin)
    if not (resolved_bin.is_file() and os.access(resolved_bin, os.X_OK)):
        return {
            "ok": False,
            "state": "bridge_unavailable",
            "checks": {"bridge_component": "missing"},
            "wechat_version": None,
            "bridge_version": None,
            "reasons": [
                {
                    "code": "component_missing",
                    "fix_hint": (
                        "到设置安装 wechat-bridge 组件(前置 brew install sqlcipher),"
                        "或在品类 YAML 的 push 条目配 wechat_bridge_bin 指向桥 bin 路径"
                    ),
                }
            ],
        }
    argv = [str(resolved_bin), "--probe"]
    try:
        exit_code, stdout, _stderr = run_bridge_command_sync(argv, "", timeout)
    except LocalBridgeTimeoutError:
        return {
            "ok": False,
            "state": "bridge_unavailable",
            "checks": {"bridge_component": "timeout"},
            "wechat_version": None,
            "bridge_version": None,
            "reasons": [
                {"code": "probe_timeout", "fix_hint": f"探针超过 {timeout:.0f}s 未返回(已终止);重试一次,持续超时先查桥组件"}
            ],
        }
    payload = parse_bridge_payload(stdout)
    if exit_code != 0 or not isinstance(payload, dict) or "state" not in payload:
        return {
            "ok": False,
            "state": "bridge_unavailable",
            "checks": {"bridge_component": "unparseable"},
            "wechat_version": None,
            "bridge_version": None,
            "reasons": [
                {"code": "probe_unparseable", "fix_hint": f"桥探针应答不是契约 JSON(exit={exit_code});重装或升级桥组件"}
            ],
        }
    return payload


class WeixinLocalChannel(TrendAwareChannel):
    """``weixin-local`` channel:出站桥接受管组件 wechat-bridge(每条一次
    ``send_text`` 子进程;G6 频控在桥内,MYIA 零复制)。

    Args:
        target: 会话 id 的凭据引用(``env:WEIXIN_LOCAL_CHAT_ID`` style,发送期
            解析)。本通道无目录寻址(schema 对无 CHANNEL_PLATFORMS 条目强制
            必填 target,webhook 同款);桥会话列表是只读浏览面,不作地址簿。
        template: 可选用户模板(Jinja2);在场时渲染输出为整条消息,省略 →
            内置纯文本版式(ntfy ``build_message`` 同款,蓝本对齐)。
        renderer: 模板渲染器;缺省共享沙箱实例。
        bridge_bin: 桥 bin 路径覆写(本地路径,非凭据;schema
            ``wechat_bridge_bin``);缺省 :data:`DEFAULT_BRIDGE_BIN`。构造期只
            存字符串,零文件系统检查(显式可选:无桥环境配置加载零报错)。
        timeout: 子进程超时秒数(缺省 :data:`DEFAULT_BRIDGE_TIMEOUT_SECONDS`)。
        runner: 测试注入点(:data:`BridgeRunner` 契约);缺省真子进程。

    Raises:
        PushSendError: 桥/组件不可用(``bridge_unavailable`` + 修复指引)、
            UI 通道环境降级(``bridge_degraded``:窗口未开/AX 树空/静默发送
            不可行)、频控拒发(``send_rate_limited``,G6,带剩余等待秒数)、
            发送失败(``weixin_local_send_error``)、用法契约漂移
            (``bridge_usage_error``)、超时(``bridge_timeout``)或模板渲染
            失败。**全部不标 dead**(零死信:桥错误族全是环境态)。
    """

    name = "weixin-local"
    #: 无目录寻址(bridge 会话列表 = 只读浏览面;targets spec 前缀词表容不
    #: 下连字符;schema 侧本通道不入 CHANNEL_PLATFORMS,targets 配即拒)。
    supports_targeting = False

    def __init__(
        self,
        *,
        target: str | None = None,
        template: str | None = None,
        renderer: TemplateRenderer | None = None,
        bridge_bin: str | None = None,
        timeout: float = DEFAULT_BRIDGE_TIMEOUT_SECONDS,
        runner: BridgeRunner | None = None,
    ) -> None:
        self._target = target
        self._template = template
        self._renderer = renderer or TemplateRenderer()
        self._bridge_bin = bridge_bin
        self._timeout = timeout
        self._runner = runner

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """Compose + one-shot ``send_text`` 子进程。

        Raises:
            PushSendError: on any bridge failure (callers isolate per
                channel; nothing is raised on success).
        """
        chat_id = self._resolve_chat(context)
        body = self._compose(items, context)
        resolved_bin = bin_path(self._bridge_bin)
        # 发送期预检(蓝本同款):bin 缺失先于子进程失败,给结构化修复指引
        # 而非裸 FileNotFoundError。
        _require_executable(resolved_bin)
        argv = [str(resolved_bin), "send_text", chat_id, "--file", "-"]
        runner = self._runner or run_bridge_command
        try:
            exit_code, stdout, stderr = await runner(argv, body, self._timeout)
        except LocalBridgeTimeoutError as exc:
            raise PushSendError(
                "bridge_timeout",
                f"微信本机通道超时:{exc}(桥内频控与 AX 动作均应在秒级返回,"
                "超时即桥挂起;瞬态可重试)",
            ) from exc
        except FileNotFoundError as exc:
            raise PushSendError(
                "bridge_unavailable",
                f"微信本机通道不可用:桥 bin 无法执行: {resolved_bin}"
                f"({type(exc).__name__}: {exc})。修复指引:安装 wechat-bridge"
                " 组件,或用 wechat_bridge_bin 覆写桥 bin 路径",
            ) from exc
        self._raise_for_result(exit_code, stdout, stderr)
        logger.debug(
            "weixin-local 已桥接发送: slot=%s kind=%s count=%d chat=%s",
            context.slot,
            context.kind,
            len(items),
            chat_id,
        )

    # ------------------------------------------------------------- compose

    def _compose(self, items: Sequence[Any], context: SendContext) -> str:
        """消息文本:用户模板在场走渲染器,缺省内置纯文本版式(蓝本对齐)。

        长文不预切——分块语义随桥(G6 单条契约:一条调用 = 一条消息,桥侧
        也不切;超长由发送方模板自行约束)。
        """
        if self._template is not None:
            try:
                return self._renderer.render(
                    self._template, items, context, **self.trend_render_kwargs()
                )
            except TemplateRenderError as exc:
                raise PushSendError(
                    "template_render_error", f"push[].template 渲染失败: {exc}"
                ) from exc
        return build_message(items, context)

    def _resolve_chat(self, context: SendContext) -> str:
        """legacy target 引用解析(本通道无目录寻址,``context.target`` 恒
        None;防御性忽略之)。

        两条路都缺席 → ``missing_target``;解析失败 → 上游结构化码原样;
        解析值空白 → ``invalid_credential_ref``(同时保证 argv 的
        ``send_text <chat>`` 段不携带空白会话 id)。
        """
        if self._target is not None:
            try:
                value = resolve_credential(self._target).strip()
            except CredentialResolveError as exc:
                raise PushSendError(exc.code, f"weixin-local target 解析失败: {exc}") from exc
        else:
            raise PushSendError(
                "missing_target",
                "weixin-local 无目录寻址:必须配置 legacy target(会话 id 引用,"
                f"缺省 {DEFAULT_TARGET_ENV_REF})",
            )
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                "weixin-local 会话 id 解析结果为空白(target 引用的值不能是空串)",
            )
        return value

    # ------------------------------------------------ 错误映射(design §6 全表)

    def _raise_for_result(self, exit_code: int, stdout: str, stderr: str) -> None:
        """(exit_code, stdout JSON) → 成功放行 / 结构化 PushSendError。

        映射表(design §6 具名错误族 → 通道错误码;失败族全环境态,零死信):

        ======  ======================  ================================
        exit    通道码                  语义
        ======  ======================  ================================
        0       (放行)                  成功(无 error 载荷)
        2       bridge_usage_error      argv 契约漂移(自家 bug,ERROR 日志)
        10      bridge_unavailable      微信进程不在
        11      bridge_unavailable      AX 权限缺失
        12      bridge_degraded         主窗口未开(UI 通道降级态)
        13      bridge_degraded         AX 树空/残缺
        14      send_rate_limited       G6 频控拒发(带剩余等待秒数;瞬态)
        15      bridge_degraded         AX 静默发送不可行(AC4 语义)
        20/21/22 weixin_local_send_error  localdb 族对 send 不适用(防御)
        30      bridge_timeout          子进程超时(kill 兜底)
        其他    weixin_local_send_error  兜底(exit 1 通用失败段等)
        ======  ======================  ================================
        """
        payload = parse_bridge_payload(stdout)
        error = payload.get("error") if isinstance(payload, dict) else None
        upstream = str(error.get("message")) if isinstance(error, dict) else ""
        fix_hint = str(error.get("fix_hint")) if isinstance(error, dict) and error.get("fix_hint") else ""
        upstream_code = str(error.get("code")) if isinstance(error, dict) and error.get("code") else ""
        detail = f"{upstream_code}: {upstream}" if upstream_code else upstream
        if exit_code == 2:
            # 用法错 = MYIA argv 契约与桥 CLI 漂移,自家 bug,需介入。
            hint = stderr.strip() or upstream
            logger.error(
                "微信本机通道用法错误(MYIA 与 wechat-bridge CLI 契约漂移,需要介入):"
                " exit=2 stderr=%r",
                hint[:300],
            )
            raise PushSendError(
                "bridge_usage_error",
                f"微信本机通道用法错误(argv 契约漂移,需要介入): {hint[:300]!r}",
            )
        if exit_code == 0 and not error:
            # 桥契约:exit 0 ⟺ 无 error 载荷。
            return
        # 错误族判定:具名族以**码名**为准(defensive:exit 0 却带 error 载荷
        # 的契约漂移场景也归对族),未具名/无码名回落 exit 码。
        family = _CODE_NAME_TO_EXIT.get(upstream_code, exit_code)
        suffix = f"。修复指引:{fix_hint}" if fix_hint else ""
        if family == 14:
            retry_after = error.get("retry_after_seconds") if isinstance(error, dict) else None
            wait = f"(须再等 {retry_after:g} 秒)" if isinstance(retry_after, (int, float)) else ""
            raise PushSendError(
                "send_rate_limited",
                f"微信本机通道频控拒发(G6:两次发送硬间隔 ≥10s,桥内硬编码不可配置)"
                f"{wait}: {detail}{suffix}",
            )
        if family in (10, 11):
            raise PushSendError(
                "bridge_unavailable",
                f"微信本机通道不可用(前置缺失): {detail or f'exit={exit_code}'}{suffix}",
            )
        if family in (12, 13, 15):
            raise PushSendError(
                "bridge_degraded",
                f"微信本机通道降级(UI 通道环境态): {detail or f'exit={exit_code}'}{suffix}",
            )
        if family == 30:
            raise PushSendError(
                "bridge_timeout",
                f"微信本机通道超时(桥内 kill 兜底): {detail}{suffix}",
            )
        stderr_fragment = stderr.strip()[:160]
        stderr_part = f" stderr={stderr_fragment!r}" if stderr_fragment else ""
        raise PushSendError(
            "weixin_local_send_error",
            f"微信本机通道发送失败: {detail or f'exit={exit_code}'}"
            f" stdout={stdout[:120]!r}{stderr_part}{suffix}",
        )

    # --------------------------------------------- 目录(无自动发现)

    async def discover_directory(self) -> list[Any]:
        """无自动发现(设计事实):桥的会话列表是只读浏览面(消息屏只读
        入口消费),不是推送地址簿——结构化说明而非假装刷新。
        """
        raise DirectoryDiscoverUnsupported(
            "weixin-local 无目录寻址(设计定案):桥会话列表只供消息屏只读浏览,"
            "推送对象走 legacy target 引用(缺省 env:WEIXIN_LOCAL_CHAT_ID)"
        )
