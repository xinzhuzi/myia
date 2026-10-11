#!/usr/bin/env python
"""AX 深探脚本 — WeChat 4.1.15 macOS(任务 10-11-wechat-ui-bridge A1,implement.md 手册第 2-5 步)

用途:对运行中的微信进程做 AX 树只读探查,输出 role/计数/属性名形状,回答 AC1 三问。
红线合规:
  - 只读属性 + 只写 AXManualAccessibility/AXEnhancedUserInterface 两个激活开关(手册第 4 步);
  - 不激活窗口、不合成点击、不抢焦点;
  - 绝不导出消息文本:AXTitle/AXValue/AXDescription 等取值一律只记 Python 类型 + 长度;
  - 会话标题等文本零落盘,证据只有形状。
用法:  .venv/bin/python ax-probe-script.py [--pid PID] [--json OUT.json]
        (缺省自动探测 WeChat 进程;--json 另存机器可读结果)
复跑:  仓库根 `.venv/bin/python .trellis/tasks/10-11-wechat-ui-bridge/research/ax-probe-script.py`
"""
from __future__ import annotations

import json
import sys
import time
from typing import Any

import ApplicationServices as AS
import Foundation

MAX_DEPTH = 14          # 树深上限
MAX_NODES = 20000       # 全树节点上限(防爆炸)
WALK_TIMEOUT_S = 45.0   # 单次遍历墙钟上限

MANUAL_ACCESSIBILITY = "AXManualAccessibility"
ENHANCED_USER_INTERFACE = "AXEnhancedUserInterface"

# 记录形状时,这些"取值类"属性只记类型+长度,不记内容
VALUE_ATTRS = {
    "AXTitle", "AXDescription", "AXValue", "AXHelp", "AXPlaceholderValue",
    "AXLabel", "AXNumberOfCharacters", "AXSelectedText",
}


def find_wechat_pid() -> int:
    """按进程名找 WeChat 主进程 pid(不激活、不拉起)。"""
    ns = Foundation.NSRunningApplication
    apps = ns.runningApplicationsWithBundleIdentifier_("com.tencent.xinWeChat")
    if apps:
        return int(apps[0].processIdentifier())
    raise SystemExit("wechat_not_running: com.tencent.xinWeChat 无运行实例(探查脚本不负责拉起)")


def shape_value(v: Any) -> str:
    """取值的脱敏形状:类型(+长度/+数值)。数值(如未读数)可记,文本只记长度。"""
    if v is None:
        return "null"
    if isinstance(v, (int, float, bool)):
        return f"number:{v!r}"
    if isinstance(v, Foundation.NSString) or isinstance(v, str):
        return f"str(len={len(str(v))})"
    if isinstance(v, Foundation.NSURL):
        return f"url(len={len(str(v))})"
    if isinstance(v, (Foundation.NSArray, list, tuple)):
        return f"array(len={len(v)})"
    if isinstance(v, (Foundation.NSDictionary, dict)):
        return f"dict(keys={len(v)})"
    return f"{type(v).__name__}"


def ax_attr_names(el) -> list[str]:
    names_ref = AS.AXUIElementCopyAttributeNames(el, None)
    if names_ref is None:
        return []
    return [str(n) for n in names_ref]


def ax_get(el, attr: str):
    err, val = AS.AXUIElementCopyAttributeValue(el, attr, None)
    if err != 0:
        return None, err
    return val, 0


def ax_role(el) -> str:
    val, err = ax_get(el, "AXRole")
    return str(val) if err == 0 and val is not None else "?"


def set_flag(el, attr: str, value=True) -> int:
    return AS.AXUIElementSetAttributeValue(el, attr, Foundation.NSNumber.numberWithBool_(value))


ERR_NAMES = {
    -25200: "Failure", -25201: "IllegalArgument", -25202: "InvalidUIElement",
    -25203: "InvalidUIElementObserver", -25204: "CannotComplete",
    -25205: "AttributeUnsupported", -25206: "ActionUnsupported",
    -25207: "NotificationUnsupported", -25208: "NotImplemented",
    -25211: "APIDisabled", -25212: "NoValue", -25213: "ParameterizedAttributeUnsupported",
}


def err_name(code: int) -> str:
    return f"{code}({ERR_NAMES.get(code, '?')})"


def ax_action_names(el) -> list[str]:
    names_ref = AS.AXUIElementCopyActionNames(el, None)
    if names_ref is None:
        return []
    return [str(n) for n in names_ref]


def tree_outline(el, depth: int, out: list[str], budget: int = 240) -> None:
    """轮廓:role[子计数] 缩进行;只形状不内容。"""
    if len(out) >= budget or depth > 10:
        return
    role = ax_role(el)
    v, err = ax_get(el, "AXChildren")
    n = len(v) if err == 0 and v is not None else err_name(err)
    extra = ""
    if role in ("AXButton", "AXTextField", "AXTextArea", "AXTable", "AXCell"):
        acts = ax_action_names(el)
        if acts:
            extra = f" actions={acts}"
        names = ax_attr_names(el)
        interesting = [a for a in ("AXPlaceholderValue", "AXValue", "AXDescription", "AXFocused") if a in names]
        if interesting:
            extra += f" valueAttrs={interesting}"
    out.append("  " * depth + f"{role}[children={n}]{extra}")
    if err == 0:
        for child in v or []:
            tree_outline(child, depth + 1, out, budget)
            if len(out) >= budget:
                return


class Walker:
    def __init__(self) -> None:
        self.nodes = 0
        self.role_counts: dict[str, int] = {}
        self.role_attr_names: dict[str, set[str]] = {}
        self.errors: dict[str, int] = {}
        self.deadline = time.monotonic() + WALK_TIMEOUT_S
        self.max_depth_seen = 0
        # 目标节点收集(第 5 步):只记路径与属性名形状
        self.cells: list[dict] = []          # 会话列表 cell 候选
        self.static_texts: list[dict] = []   # 消息区文本节点候选(只记形状)
        self.textfields: list[dict] = []     # 输入框候选
        self.buttons: list[dict] = []        # 按钮候选(找发送按钮 AXConfirm)

    def note_err(self, where: str, err: int) -> None:
        key = f"{where}:{err}"
        self.errors[key] = self.errors.get(key, 0) + 1

    def walk(self, el, path: str, depth: int) -> None:
        if self.nodes >= MAX_NODES or time.monotonic() > self.deadline or depth > MAX_DEPTH:
            return
        self.nodes += 1
        self.max_depth_seen = max(self.max_depth_seen, depth)
        role = ax_role(el)
        self.role_counts[role] = self.role_counts.get(role, 0) + 1
        names = ax_attr_names(el)
        self.role_attr_names.setdefault(role, set()).update(names)

        rec = None
        if role == "AXStaticText":
            rec = self.static_texts
        elif role in ("AXTextField", "AXTextArea"):
            rec = self.textfields
        elif role == "AXButton":
            rec = self.buttons
        elif role in ("AXCell", "AXRow", "AXListItem", "AXGroup"):
            # cell/row 才可能当会话行;AXGroup 太泛,只在列表直系下记
            rec = self.cells if role != "AXGroup" else None
        if rec is not None and len(rec) < 400:
            item: dict[str, Any] = {"path": path, "role": role, "attrs": names,
                                    "actions": ax_action_names(el)}
            for a in ("AXTitle", "AXDescription", "AXValue", "AXPlaceholderValue", "AXFocused"):
                if a in names:
                    v, err = ax_get(el, a)
                    if err == 0:
                        item[a] = shape_value(v)
                    else:
                        self.note_err(f"get:{a}", err)
            rec.append(item)

        # 子节点
        v_children, err = ax_get(el, "AXChildren")
        if err != 0:
            self.note_err("children", err)
            return
        for i, child in enumerate(v_children or []):
            self.walk(child, f"{path}/{i}", depth + 1)

    def summary(self) -> dict[str, Any]:
        return {
            "nodes": self.nodes,
            "max_depth": self.max_depth_seen,
            "role_counts": self.role_counts,
            "errors": self.errors,
            "cells_n": len(self.cells),
            "static_texts_n": len(self.static_texts),
            "textfields_n": len(self.textfields),
            "buttons_n": len(self.buttons),
        }


def probe_app(pid: int) -> dict[str, Any]:
    app = AS.AXUIElementCreateApplication(pid)
    out: dict[str, Any] = {"pid": pid}
    out["attr_names"] = ax_attr_names(app)
    # 关键属性逐一探测
    for attr in ("AXWindows", "AXMainWindow", "AXFocusedWindow", "AXMenuBar", "AXTitle", "AXHidden", "AXFrontmost"):
        v, err = ax_get(app, attr)
        if err == 0:
            if isinstance(v, (Foundation.NSArray, list)):
                out[attr] = f"array(len={len(v)})"
            elif attr == "AXMenuBar":
                out[attr] = "present(barLayout)"
            else:
                out[attr] = shape_value(v)
        else:
            out[attr] = f"err={err}"
    out["windows_ax"] = []
    v_win, err = ax_get(app, "AXWindows")
    if err == 0 and v_win is not None:
        for i, w in enumerate(v_win):
            wrole = ax_role(w)
            wnames = ax_attr_names(w)
            wrec: dict[str, Any] = {"i": i, "role": wrole, "attr_names": wnames}
            for a in ("AXTitle", "AXSubrole", "AXMinimized", "AXFocused"):
                if a in wnames:
                    wv, werr = ax_get(w, a)
                    if werr == 0:
                        wrec[a] = shape_value(wv)
            out["windows_ax"].append(wrec)
    return out


def window_refs(app) -> list[tuple[str, Any]]:
    """收集窗口级 AX 引用:AXWindows 数组 + AXMainWindow/AXFocusedWindow 单元素。"""
    refs: list[tuple[str, Any]] = []
    v, err = ax_get(app, "AXWindows")
    if err == 0 and v is not None:
        for i, w in enumerate(v):
            refs.append((f"AXWindows[{i}]", w))
    for attr in ("AXMainWindow", "AXFocusedWindow", "AXMain"):
        v, err = ax_get(app, attr)
        if err == 0 and v is not None and not isinstance(v, (int, float, str, Foundation.NSString, Foundation.NSArray)):
            refs.append((attr, v))
    v, err = ax_get(app, "AXChildren")
    if err == 0 and v is not None:
        for i, w in enumerate(v):
            refs.append((f"AXChildren[{i}]", w))
    return refs


def main() -> int:
    pid_args: list[int] = []
    json_out = None
    force_activation = False
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--pid":
            pid_args.append(int(args[i + 1])); i += 2
        elif args[i] == "--json":
            json_out = args[i + 1]; i += 2
        elif args[i] == "--force-activation":
            force_activation = True; i += 1
        else:
            i += 1
    if not pid_args:
        pid_args = [find_wechat_pid()]
    report: dict[str, Any] = {"pids": pid_args, "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z")}

    per_pid: dict[str, Any] = {}
    for pid in pid_args:
        sec: dict[str, Any] = {}
        # ── 第 2 步:深探(原始态) ─────────────────────────────────
        sec["app_raw"] = probe_app(pid)
        app = AS.AXUIElementCreateApplication(pid)
        w_raw = Walker()
        refs = window_refs(app)
        sec["window_refs_raw"] = [name for name, _ in refs]
        for name, w in refs:
            w_raw.walk(w, name, 0)
        sec["walk_raw"] = w_raw.summary()

        # ── 第 4 步:空树分支 → AXManualAccessibility / AXEnhancedUserInterface ──
        if w_raw.nodes == 0 or force_activation:
            err1 = set_flag(app, MANUAL_ACCESSIBILITY, True)
            err2 = set_flag(app, ENHANCED_USER_INTERFACE, True)
            sec["activation"] = {
                "set_AXManualAccessibility": f"err={err1}",
                "set_AXEnhancedUserInterface": f"err={err2}",
            }
            time.sleep(1.5)  # Chromium 渲染层建树需要一点时间
            sec["app_after_activation"] = probe_app(pid)
            w_act = Walker()
            for name, w in window_refs(app):
                w_act.walk(w, name, 0)
            sec["walk_after_activation"] = w_act.summary()
            walker = w_act if w_act.nodes > w_raw.nodes else w_raw
        else:
            sec["activation"] = "skipped(tree non-empty)"
            walker = w_raw

        # ── 第 5 步:三类目标节点(形状级) ────────────────────────
        def dedup(items: list[dict], key: str, limit: int = 12) -> list[dict]:
            seen: set[str] = set()
            out: list[dict] = []
            for it in items:
                sig = it.get(key)
                if sig in seen:
                    continue
                seen.add(sig)
                out.append(it)
                if len(out) >= limit:
                    break
            return out

        sec["targets"] = {
            "list_cell_samples": dedup(walker.cells, "path"),
            "static_text_samples": dedup(walker.static_texts, "path"),
            "textfield_samples": dedup(walker.textfields, "path"),
            "button_samples": dedup(walker.buttons, "path"),
            "roles_with_confirm_attr": [r for r, names in walker.role_attr_names.items() if "AXConfirm" in names],
            "roles_with_placeholder": [r for r, names in walker.role_attr_names.items() if "AXPlaceholderValue" in names],
        }
        sec["role_attr_names"] = {r: sorted(n) for r, n in sorted(walker.role_attr_names.items())}
        # 窗口树轮廓(最终态;只 role/计数/动作名)
        outline: list[str] = []
        for name, w in window_refs(app):
            outline.append(f"ROOT {name}")
            tree_outline(w, 1, outline)
            if len(outline) > 400:
                break
        sec["tree_outline"] = outline
        per_pid[str(pid)] = sec

    report["per_pid"] = per_pid

    text = json.dumps(report, ensure_ascii=False, indent=1, default=str)
    print(text)
    if json_out:
        with open(json_out, "w", encoding="utf-8") as f:
            f.write(text)
    return 0

    # ── 第 5 步:三类目标节点(形状级) ────────────────────────────
    def dedup(items: list[dict], key: str, limit: int = 12) -> list[dict]:
        seen: set[str] = set()
        out: list[dict] = []
        for it in items:
            sig = it.get(key)
            if sig in seen:
                continue
            seen.add(sig)
            out.append(it)
            if len(out) >= limit:
                break
        return out

    report["targets"] = {
        "list_cell_samples": dedup(walker.cells, "path"),
        "static_text_samples": dedup(walker.static_texts, "path"),
        "textfield_samples": dedup(walker.textfields, "path"),
        "button_samples": dedup(walker.buttons, "path"),
        "roles_with_confirm_attr": [r for r, names in walker.role_attr_names.items() if "AXConfirm" in names],
        "roles_with_placeholder": [r for r, names in walker.role_attr_names.items() if "AXPlaceholderValue" in names],
    }
    report["role_attr_names"] = {r: sorted(n) for r, n in sorted(walker.role_attr_names.items())}

    text = json.dumps(report, ensure_ascii=False, indent=1, default=str)
    print(text)
    if json_out:
        with open(json_out, "w", encoding="utf-8") as f:
            f.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
