"""三态探针(task 10-11-wechat-ui-bridge design §6 --probe + 三态判据矩阵)。

状态机(矩阵照抄,执行者零设计):

| 探测结果 | 态 |
|---|---|
| 微信进程未运行 | ``bridge_unavailable`` |
| AX 辅助功能权限缺失 | ``bridge_unavailable`` |
| 微信运行但主窗口未开(UI 通道) | ``degraded``(localdb 不受影响) |
| AX 树空/残缺 | ``degraded``(像素链兜底;Phase C 才有判据,骨架态 unknown) |
| 本地库不可定位/密钥不可得 | ``degraded``(localdb 不可用) |
| 全部通过 | ``ok`` |

探针零成本(设计原文):进程存在性 + 版本号 + AX 可达性自检 + 窗口快照 +
本地库落盘计数,**不读消息内容**;全部检查器经 :mod:`.system_checks` 的
模块级注入点,单测全 mock。

组件自身未安装/版本不符的矩阵行在本 CLI 里不可达——CLI 能跑起来即组件
在场(版本以组件戳为准,随载荷 ``bridge_version`` 如实携带)。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from . import system_checks as sc
from .codes import DB_NOT_FOUND, KEY_UNAVAILABLE, WECHAT_NOT_RUNNING
from .config import BridgeConfig, load_config

__all__ = ["ProbeResult", "run_probe", "run_doctor"]

#: 密钥不可得的码名字符串(与 codes 表 exit 21 的码名对账,不裸写串)。
CODE_KEY_UNAVAILABLE_NAME = "key_unavailable"
# 静态对账护栏:矩阵用到的 §6 码值不被无声改动(改码先改 design §6 表)。
assert KEY_UNAVAILABLE == 21 and CODE_KEY_UNAVAILABLE_NAME == "key_unavailable"
assert WECHAT_NOT_RUNNING == 10 and DB_NOT_FOUND == 20

#: AX 门 closed 时的处置提示(0.8.4 勘误:重开配方仅在**长期运行**进程上
#: 历史成功过一次;2026-10-14 五组对照实证——重启后的新进程无论 LLDB
#: 开位/增强位(plist 键/启动者/时间+使用)树均不暴露,门位可写=1 无效。
#: 新进程的正解 = CGEvent+OCR 降级链(已真机三连绿),不再误导用户去开门)。
AX_GATE_FIX_HINT = (
    "AX 树浅为供给侧机理定论(2026-10-14 双线收敛:门位自愈=红鲱鱼,"
    "主窗 mmui accessibleRoot 恒 nil;见 10-14-wechat-ax-gate-exp)→ "
    "send_text 自动走 CGEvent+OCR 降级链(真机验证绿)"
)
#: AX 门 closed 的判定注记(REV 判据;design §J-22)。0.8.1:nodes 为
#: 全窗子树**深度枚举**节点数(直查第一层在 4.1.15 恒 ~4——Qt 树挂
#: AXGroup 深层,真机实证 /tmp/wxsend-e2e/axwalk2-out.txt)。
AX_GATE_CLOSED_NOTE = (
    "进程外枚举 5 节点级 = Qt AX 门未开(REV 判据);nodes 为全窗子树"
    "深度枚举节点数(直查第一层在 4.1.15 恒约 4,Qt 树挂深层)"
)

#: 单条降级原因(码名 + 修复指引;MYIA 侧映射 UI 文案)。
@dataclass(frozen=True)
class ProbeReason:
    code: str
    fix_hint: str

    def to_payload(self) -> dict[str, str]:
        return {"code": self.code, "fix_hint": self.fix_hint}


@dataclass(frozen=True)
class ProbeResult:
    """``--probe`` 应答(§6 契约四键 ok/state/checks/wechat_version + 诊断附加键)。

    ``ok`` ≡ ``state == "ok"``;``reasons`` 汇总全部降级/不可用因(三态判据
    矩阵的行级落点);附加键是对四键契约的超集( additive,消费端宽容)。
    """

    state: str
    checks: dict[str, str]
    wechat_version: str | None
    reasons: list[ProbeReason] = field(default_factory=list)
    bridge_version: str | None = None
    config: dict[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return self.state == "ok"

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "ok": self.ok,
            "state": self.state,
            "checks": dict(self.checks),
            "wechat_version": self.wechat_version,
            "bridge_version": self.bridge_version,
            "reasons": [reason.to_payload() for reason in self.reasons],
        }
        if self.config is not None:
            payload["config"] = self.config
        return payload


def run_probe(
    *,
    config: BridgeConfig | None = None,
    process_running: Callable[[], bool] | None = None,
    version_of: Callable[[], str | None] | None = None,
    ax_trusted: Callable[[], bool | None] | None = None,
    window_open: Callable[[], bool | None] | None = None,
    storage_accounts: Callable[[], int | None] | None = None,
    key_available: Callable[[], bool] | None = None,
    bridge_version: str | None = None,
    screen_granted: Callable[[], bool | None] | None = None,
) -> ProbeResult:
    """跑全部探针项并按判据矩阵归态(检查器全部可注入 = 单测主战场)。

    ``key_available`` 缺省接本地库密钥缓存的零成本自询(:func:`.system_checks.
    localdb_key_available`——缓存只在密钥全量验证命中时落盘,故探针不谎报
    ok;E1 实测零内存途径未闭合,如实 degraded)。
    """
    cfg = config if config is not None else load_config()
    process = process_running if process_running is not None else sc.wechat_process_running
    version = version_of if version_of is not None else sc.wechat_version
    trusted = ax_trusted if ax_trusted is not None else sc.ax_permission_trusted
    screen = screen_granted if screen_granted is not None else sc.screen_recording_granted
    window = window_open if window_open is not None else sc.wechat_main_window_open
    storage = storage_accounts if storage_accounts is not None else sc.localdb_storage_accounts
    key = key_available if key_available is not None else sc.localdb_key_available

    wechat_version_value = version()
    checks: dict[str, str] = {"bridge_component": "ok"}
    reasons: list[ProbeReason] = []

    process_ok = bool(process())
    checks["wechat_process"] = "ok" if process_ok else "fail"
    if not process_ok:
        reasons.append(
            ProbeReason("wechat_not_running", "启动微信客户端(桥不代启,不碰前台)")
        )
        return ProbeResult(
            state="bridge_unavailable",
            checks=checks,
            wechat_version=wechat_version_value,
            reasons=reasons,
            bridge_version=bridge_version,
            config=cfg.to_payload(),
        )

    trusted_value = trusted()
    # 2026-10-12 勘误:AX 通道 A1 定论死路后,ax_permission 不再驱动 degraded
    # (保留报告值;UI 徽标已改消费 screen_recording)。
    checks["ax_permission"] = sc.check_summary(trusted_value)
    screen_value = screen()
    checks["screen_recording"] = sc.check_summary(screen_value)
    if screen_value is False:
        reasons.append(
            ProbeReason(
                "screen_recording_denied",
                "系统设置 → 隐私与安全性 → 屏幕录制,给 MYIA(或桥宿主进程)授权(像素链截窗前置)",
            )
        )
        return ProbeResult(
            state="bridge_unavailable",
            checks=checks,
            wechat_version=wechat_version_value,
            reasons=reasons,
            bridge_version=bridge_version,
            config=cfg.to_payload(),
        )

    window_value = window()
    checks["main_window"] = sc.check_summary(window_value)
    if window_value is False:
        reasons.append(
            ProbeReason(
                "window_closed",
                "打开微信主窗口(UI 通道恢复;本地库只读通道不受影响)",
            )
        )

    accounts = storage()
    if accounts is None:
        checks["localdb_storage"] = "fail"
        reasons.append(
            ProbeReason(
                "db_not_found",
                "未找到已登录账号的本地库落盘(db_storage);确认微信在本机登录过",
            )
        )
    else:
        checks["localdb_storage"] = "ok" if accounts > 0 else "fail"
        if accounts == 0:
            reasons.append(
                ProbeReason(
                    "db_not_found",
                    "本地库数据根在场但无带 db_storage 的账号目录;确认微信在本机登录过",
                )
            )

    key_ok = bool(key())
    checks["localdb_key"] = "ok" if key_ok else "unavailable"
    if not key_ok:
        reasons.append(
            ProbeReason(
                CODE_KEY_UNAVAILABLE_NAME,
                "零内存密钥途径(key_info.db)实测不可推导(E1 真跑:候选全数"
                "离线 HMAC 未命中;材料疑被机器专属密钥包裹);D4 途径:内存"
                "扫描(localdb key-scan,配置 mem_search_enabled 显式开启"
                "+提权,默认关)或引入外部密钥(keys.json,600)",
            )
        )

    # AX 树判据(矩阵行「AX 树空/残缺 → degraded」)属 Phase C 能力探测;
    # 骨架态如实 unknown,不据此降级也不据此报 ok。
    checks["ax_tree"] = "unknown"

    state = "degraded" if reasons else "ok"
    return ProbeResult(
        state=state,
        checks=checks,
        wechat_version=wechat_version_value,
        reasons=reasons,
        bridge_version=bridge_version,
        config=cfg.to_payload(),
    )


def run_doctor(
    *,
    config: BridgeConfig | None = None,
    bridge_version: str | None = None,
    node_counter: Callable[[], int | None] | None = None,
    input_probe: Callable[[], str | None] | None = None,
    direct_validator: Callable[[], dict[str, Any]] | None = None,
    direct_lldb_check: Callable[[], str | None] | None = None,
) -> dict[str, Any]:
    """``wechat-bridge doctor`` 载荷(task 10-14-wechat-send-text design
    §E-2):= ``--probe`` 超集 + send 链就绪度,**仍零前台扰动**(AX 读
    查询不激活不点击;probe 即一次无障碍查询,副作用 = 微信自身
    activateQtAccessibility 自然置位,REV:20-24)。

    形状::

        {"doctor": {"probe": {run_probe 载荷原样},
                    "ax_gate": {"nodes", "state": open|closed|unknown,
                                "input_field": ok|missing, "note", "fix_hint"},
                    "cgevent_channel": {"post_key", "note"},
                    "direct_channel": {"enabled", "anchored", "lldb",
                                       "last_anchor_build",
                                       "slice_sha256_matched"}}}

    - ``ax_gate.nodes`` = ``system_checks.wechat_ax_node_count()``(全部
      窗口子树的**深度枚举节点数**取最大,0.8.1 修正:直查第一层在
      4.1.15 恒 ~4,Qt 命名树挂 AXGroup 深层;>5 = open,≤5 = closed,
      失败 = unknown);``input_field`` = axui.read_input_value() 探测
      (ok/missing);均可注入 = 单测主战场。
    - ``cgevent_channel.host_ax_trusted`` = 宿主辅助功能授权自检
      (ax_permission_trusted;False = CGEvent/keystroke 对他 app 无效
      的实锤——发送前置)。
    - ``direct_channel`` = 阶段3 §3.5 直发通道探针(senddirect.
      doctor_direct_channel;轻量 attach 验证仅 enabled 时做,探针失败
      ≠通道失败,anchored 三态+unknown 如实);validator/lldb 检查器
      可注入 = 单测主战场。
    - doctor 是状态查询不判错:调用方恒 exit 0(key-status 判例)。
    """
    probe_result = run_probe(config=config, bridge_version=bridge_version)
    if node_counter is None:
        node_counter = sc.wechat_ax_node_count
    if input_probe is None:
        from . import axui

        input_probe = axui.read_input_value

    nodes = node_counter()
    if nodes is None:
        gate_state, note = "unknown", "AX 节点数探测不可及(脚本失败/进程不在)"
        fix_hint = "确认微信在运行后重试;持续 unknown 查辅助功能授权(osascript System Events)"
    elif nodes > 5:
        gate_state, note, fix_hint = "open", None, None
    else:
        gate_state, note, fix_hint = "closed", AX_GATE_CLOSED_NOTE, AX_GATE_FIX_HINT

    input_value = input_probe()
    ax_gate: dict[str, Any] = {
        "nodes": nodes,
        "state": gate_state,
        "input_field": "ok" if input_value is not None else "missing",
        "note": note,
        "fix_hint": fix_hint,
    }
    from . import senddirect

    direct_channel = senddirect.doctor_direct_channel(
        config or load_config(),
        validator=direct_validator,
        lldb_check=direct_lldb_check,
    )
    return {
        "doctor": {
            "probe": probe_result.to_payload(),
            "ax_gate": ax_gate,
            "cgevent_channel": {
                "post_key": "unverified",
                "host_ax_trusted": sc.ax_permission_trusted(),
                "note": (
                    "辅助功能授权为发送前置(host_ax_trusted=false = CGEvent/"
                    "keystroke 对他 app 无效实锤);非发送键 = System Events "
                    "keystroke 优先(失败可检测)/CGEvent 兜底;doctor 不合成"
                    "事件,以首次 dry-run 实测为准"
                ),
            },
            "direct_channel": direct_channel,
        }
    }
