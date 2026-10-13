"""AX 读写原语层(task 10-14-wechat-send-text design §B-2;send_text
AX 主链的元素操作,osascript System Events 封装)。

元素事实源(REV = research/FINDINGS.md + /tmp/ax_chat_test 实测,prd
三源表):微信 4.1.15 的 Qt AX 树(门开后)暴露命名元素——
``chat_input_field``(聊天输入区,AXValue 可写可读)、
``current_chat_name_label``(当前会话标题)、``session_item_<名字>``
(搜索结果行,AXPress 可按)。

**遍历实现纪律(0.8.1 修正,证据 /tmp/wxsend-e2e/ 真机 dry-run 报告)**:

- **弃 ``entire contents``**:System Events 的 entire contents 在
  4.1.15 动态树上返回空(Qt 元素重建竞态,同路径一分钟内复现
  ``invalid index -1719``);逐层走树(axwalk2 实证)可达全部命名元素
  ——本模块全部元素原语改为 **BFS 逐层遍历**(队列 + 节点预算上限
  :data:`WALK_BUDGET`,单次 osascript 内完成,找到即返)。
- ``write_search_value`` 走 **AXFocusedUIElement 直写**(REF 同路线,
  不依赖树遍历——焦点元素是系统级查询)。
- **0.8.2(r2 真机修正,/tmp/wxsend-e2e/r2/)**:walk 底座**遍历全部
  windows**(搜索态下搜索浮窗是 window 1、主窗是 window 3,绑死
  z-order 首窗恒搜错窗);匹配属性改 **AXIdentifier**(命名元素的名称
  在 identifier,AXDescription 为空);``missing value`` 字面量 stdout
  过滤(否则当标题值泄漏)。
- **AXPress 聚焦行为未经桥内复验——P9 预验先行(design §I-7),不可达
  即降级,零阻塞**(design §D-1:调用方按返回 False 计入 AX 能力缺失,
  下一尝试 forced_fallback 直走 CGEvent+OCR 降级链)。

实现纪律(桥风格):

- 全部经模块级 ``_run``(osascript 子进程;``SUBPROC_TIMEOUT_S=10``
  挂起 → exit 30,惯例抄 sendui.py);``_run``/``monotonic``/``sleep``
  是注入点(单测全 mock);
- 参数经 osascript argv 传递(``--`` 后置实参进 run handler),正文/
  元素名不走 AppleScript 字符串拼接 = 零转义面;
- 每个函数都是单次探测/单次操作,轮询节奏由调用方(sendui)管;
- 探测类函数失败一律返回 False/None 如实,**不抛**(通道判定消费);
  操作类子进程挂起仍按 exit 30 上抛(与 sendui 同族)。

probe 副作用如实注记(design §D-1):probe 即一次无障碍查询,自然触发
QNSView activateQtAccessibility(REV:20-24,微信自身行为,非前台扰动)。
"""

from __future__ import annotations

import subprocess
import time
from typing import Callable

from .codes import TIMEOUT, BridgeError

__all__ = [
    "AX_NODE_GATE_THRESHOLD",
    "WALK_BUDGET",
    "probe_wechat_ax",
    "focus_input",
    "focused_is_input",
    "press_session_item",
    "read_current_chat_name",
    "read_input_value",
    "write_input_value",
    "write_search_value",
]

#: 平台子进程超时上限(osascript;挂起 → exit 30,sendui/system_checks 惯例)。
SUBPROC_TIMEOUT_S = 10.0
#: AX 门判据阈值:全窗子树深度枚举节点数 > 此值 = 门开(REV 判据,
#: 靶场实证门开时 ~122 节点;真机 dry-run 实证直查第一层恒 4——Qt 树
#: 挂 AXGroup 深层,计数必须深度枚举,/tmp/wxsend-e2e/axwalk2-out.txt)。
AX_NODE_GATE_THRESHOLD = 5
#: BFS 逐层遍历的节点预算上限(防动态树异常膨胀拖死单次探测;门开实测
#: ~122 节点,400 足量)。
WALK_BUDGET = 400

# ------------------------------------------------------------ 注入点 --------
monotonic: Callable[[], float] = time.monotonic
sleep: Callable[[float], None] = time.sleep


def _run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
    """osascript 子进程(超时 kill → exit 30;sendui.py 同款惯例)。"""
    try:
        return subprocess.run(  # noqa: S603 - argv 白名单字面量,无外壳
            argv,
            capture_output=True,
            timeout=SUBPROC_TIMEOUT_S,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            TIMEOUT,
            f"平台子进程超时({' '.join(argv[:2])}…,{SUBPROC_TIMEOUT_S:.0f}s 未退出,已 kill)",
            fix_hint="重试;持续超时说明 osascript 层挂起,查系统日志",
        ) from exc


def _bool_result(result: subprocess.CompletedProcess[bytes]) -> bool:
    return result.returncode == 0 and result.stdout.decode("utf-8", "replace").strip() in ("true", "1")


def _text_result(result: subprocess.CompletedProcess[bytes]) -> str | None:
    """stdout 文本(去尾换行);脚本失败/空/``missing value`` 字面量 →
    None 如实(r2 真机实证:osascript 把 ``return missing value`` 序列化
    为字面文本 'missing value' 输出——不过滤会当标题值泄漏)。"""
    if result.returncode != 0:
        return None
    text = result.stdout.decode("utf-8", "replace").rstrip("\n")
    if text.strip() in ("", "missing value"):
        return None
    return text


def _run_handler(script_body: str, *, arg: str | None = None) -> subprocess.CompletedProcess[bytes]:
    """osascript run handler 包装:遍历 {微信, WeChat} 两进程名,第一个
    命中的执行 body(可用 ``theArg``;返回 missing value = None 语义)。
    参数经 ``--`` 后置实参(argv 注入,零转义面)。"""
    script = (
        "on run {theArg}\n"
        '  tell application "System Events"\n'
        '    repeat with pname in {"微信", "WeChat"}\n'
        "      try\n"
        "        tell process (pname as text)\n"
        f"{script_body}"
        "        end tell\n"
        "      end try\n"
        "    end repeat\n"
        "  end tell\n"
        "  return missing value\n"
        "end run"
    )
    argv = ["osascript", "-e", script, "--", arg if arg is not None else ""]
    return _run(argv)


# ------------------------------------------------------- BFS 逐层遍历底座 ----

_BFS_HEAD = (
    # 0.8.3 窗口选择=**最大面积窗**(主窗选择;r3 真机实证):全窗 BFS 在
    # 搜索态被浮窗动态树膨胀到 >10s(press_session_item 恒超时挂死);
    # 命名元素(chat_input_field/session_item_*/current_chat_name_label)
    # 全在主窗(聊天主窗恒为微信最大窗),浮窗内是空 id 的 virtual_cell
    # 对 AX 无用——先选最大窗再走树。0.8.2 全窗遍历修正的是「绑死
    # window 1 搜错窗」(r2),本修正不回退该结论:最大窗≠z-order 首窗。
    "          set budget to " + str(WALK_BUDGET) + "\n"
    "          set mainWin to missing value\n"
    "          set bestArea to 0\n"
    "          repeat with w in windows\n"
    "            try\n"
    "              set sz to size of w\n"
    "              set a to ((item 1 of sz) * (item 2 of sz))\n"
    "              if a > bestArea then\n"
    "                set bestArea to a\n"
    "                set mainWin to w\n"
    "              end if\n"
    "            end try\n"
    "          end repeat\n"
    "          if mainWin is missing value then return missing value\n"
    "          set theQueue to {contents of mainWin}\n"
    "          repeat while (count of theQueue) > 0 and budget > 0\n"
    "              set nextQueue to {}\n"
    "              repeat with elem in theQueue\n"
    "                try\n"
    "                  set kids to UI elements of elem\n"
    "                on error\n"
    "                    set kids to {}\n"
    "                end try\n"
    "                repeat with kid in kids\n"
    "                  set budget to budget - 1\n"
    "                  try\n"
    "                    set elemId to (value of attribute \"AXIdentifier\" of kid) as text\n"
    "                  on error\n"
    "                    set elemId to \"\"\n"
    "                  end try\n"
)

_BFS_TAIL = (
    "                  copy kid to end of nextQueue\n"
    "                end repeat\n"
    "              end repeat\n"
    "              set theQueue to nextQueue\n"
    "            end repeat\n"
)


def _walk_find(match_body: str, *, arg: str | None = None) -> subprocess.CompletedProcess[bytes]:
    """BFS 逐层遍历**最大面积窗(主窗)**找元素(整程一个 osascript 内
    走完;``match_body`` 是 each-kid 级匹配块——命中即 return,否则入队
    继续)。

    窗口选择(0.8.3,r3 真机实证):**最大面积窗**——全窗遍历在搜索态
    被浮窗动态树拖到 >10s 超时;0.8.2 修的「绑死 window 1 搜错窗」由
    「最大窗≠z-order 首窗」继续保证(搜索浮窗 464×375 恒小于主窗)。

    匹配属性(r2 真机实证):**AXIdentifier**——命名元素
    (chat_input_field/session_item_*/current_chat_name_label)的名称在
    AXIdentifier,AXDescription 为空(axwalk2-out.txt 全树同证)。

    ``match_body`` 内可用:``elemId``(kid 的 AXIdentifier)、``kid``、
    ``theArg``(argv 注入参数)。
    """
    return _run_handler(_BFS_HEAD + match_body + _BFS_TAIL, arg=arg)


def probe_wechat_ax(
    *,
    node_count: Callable[[], int | None] | None = None,
    input_reader: Callable[[], str | None] | None = None,
) -> bool:
    """AX 主链可用性双判据(design §D-1/§J-4/13):

    (a) ``system_checks.wechat_ax_node_count()``(**全部窗口子树的深度
    枚举节点数**取最大,0.8.1 修正:直查第一层在 4.1.15 恒 ~4——Qt 树挂
    AXGroup 深层,真机实证 /tmp/wxsend-e2e/axwalk2-out.txt)>
    :data:`AX_NODE_GATE_THRESHOLD`(门开)AND
    (b) ``read_input_value() is not None``(chat_input_field 能力面——
    主链依赖写/读输入区,光 label 可读不够;「label 可读、输入区不可写」
    的半开态按此判据直接走降级链)。

    **label 不进门**(§J-13):「门开但当前无会话打开(label 缺位)」不
    误判——label 是读路增强,缺位时标题验证走 OCR 兜底。
    probe 即一次无障碍查询,副作用 = QNSView activateQtAccessibility 自然
    置位(REV:20-24,微信自身行为,非前台扰动)。
    """
    if node_count is None:
        from .system_checks import wechat_ax_node_count

        node_count = wechat_ax_node_count
    if input_reader is None:
        input_reader = read_input_value
    count = node_count()
    if count is None or count <= AX_NODE_GATE_THRESHOLD:
        return False
    return input_reader() is not None


def write_search_value(term: str) -> bool:
    """Cmd+F 后向焦点元素(搜索框)AXValue 直写(REF:27-28 同款,零剪贴板;
    不依赖树遍历——AXFocusedUIElement 是系统级焦点查询)。"""
    result = _run_handler(
        "          set focusedElement to value of attribute \"AXFocusedUIElement\"\n"
        "          set value of attribute \"AXValue\" of focusedElement to theArg\n"
        "          return true\n",
        arg=term,
    )
    return _bool_result(result)


def press_session_item(name: str) -> bool:
    """单次探测:BFS 遍历找 name 含 <display_name> 的 ``session_item_*``
    元素并 AXPress(零坐标点击;轮询节奏由调用方管)。"""
    result = _walk_find(
        '                  if elemId starts with "session_item_" and elemId contains theArg then\n'
        "                    perform action \"AXPress\" of kid\n"
        "                    return true\n"
        "                  end if\n",
        arg=name,
    )
    return _bool_result(result)


def read_current_chat_name() -> str | None:
    """``current_chat_name_label`` 直读(emoji 精确;缺位 → None 不拦通道)。"""
    result = _walk_find(
        '                  if elemId is "current_chat_name_label" then\n'
        "                    set val to value of attribute \"AXValue\" of kid\n"
        "                    if val is missing value then return missing value\n"
        "                    return (val as text)\n"
        "                  end if\n"
    )
    return _text_result(result)


def read_input_value() -> str | None:
    """``chat_input_field`` AXValue 直读(精确全量;不可达 → None 如实)。

    空输入框返回 ``""``(与不可达 None 严格区分——哨兵空断言/清空轮询
    的判据面):osascript 对空串与 missing value 的 stdout 同为空,故脚本
    侧以 ``"v:"`` 前缀包装可达路径,Python 侧剥前缀。
    """
    result = _walk_find(
        '                  if elemId is "chat_input_field" then\n'
        "                    set val to value of attribute \"AXValue\" of kid\n"
        "                    if val is missing value then set val to \"\"\n"
        "                    return (\"v:\" & (val as text))\n"
        "                  end if\n"
    )
    if result.returncode != 0:
        return None
    text = result.stdout.decode("utf-8", "replace").rstrip("\n")
    return text[2:] if text.startswith("v:") else None


def write_input_value(text: str) -> bool:
    """``chat_input_field`` AXValue 直写(REV 实弹配方;写入正文主链)。"""
    result = _walk_find(
        '                  if elemId is "chat_input_field" then\n'
        "                    set value of attribute \"AXValue\" of kid to theArg\n"
        "                    return true\n"
        "                  end if\n",
        arg=text,
    )
    return _bool_result(result)


def focus_input() -> bool:
    """``chat_input_field`` AXPress(聚焦)。**行为未实证 = P9 预验项**
    (design §J-1/§I-7);返回 False = 能力缺失,调用方按降级处理。
    聚焦后的正文保全由调用方复读 value 断言(design §D-2)。"""
    result = _walk_find(
        '                  if elemId is "chat_input_field" then\n'
        "                    perform action \"AXPress\" of kid\n"
        "                    return true\n"
        "                  end if\n"
    )
    return _bool_result(result)


def focused_is_input() -> bool | None:
    """osascript 读 AXFocusedUIElement 是否输入区(尽力断言;取不到 →
    None 如实,调用方降为前两条判据,design §D-2)。"""
    result = _run_handler(
        "          set focusedElement to value of attribute \"AXFocusedUIElement\"\n"
        "          try\n"
        "            set elemId to (value of attribute \"AXIdentifier\" of focusedElement) as text\n"
        "          on error\n"
        "            return missing value\n"
        "          end try\n"
        '          if elemId is "chat_input_field" then return true\n'
        "          return false\n"
    )
    if result.returncode != 0:
        return None
    text = result.stdout.decode("utf-8", "replace").strip()
    if text == "true":
        return True
    if text == "false":
        return False
    return None
