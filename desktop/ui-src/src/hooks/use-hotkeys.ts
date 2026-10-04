import { useEffect, useRef } from "react";

/**
 * 最小快捷键底座(注册表 + 输入框守卫 + 清理):
 * - 注册表:`useHotkeys({ "[": fn, "mod+k": fn })` 一次声明一组组合键,
 *   handler 经 ref 读取 —— 闭包永远是最新的,不必列进依赖数组。
 * - 输入框守卫:焦点在 INPUT/TEXTAREA/contentEditable(含 CodeMirror)时
 *   默认不触发(与 feed 屏 U 键同口径);`allowInInput: true` 放行
 *   (escape 关弹窗这类场景用)。
 * - 清理:单个 window keydown 监听随组件卸载移除,无残留。
 *
 * 组合键语法(刻意最小):单键("[" / "k" / "escape")或 "mod+单键"
 * (mod = ⌘ 或 Ctrl,桌面跨平台一份声明);主键比较走 toLowerCase。
 * 单键不允许带任何修饰键(⌘[/Alt[ 不算 "[");shift 不拦截 —— 符号键
 * 本就不经 shift 直出,字母键大写触发视为同键。其余组合(mod+shift+…)、
 * 序列键(g g)不在底座范围。
 */

export type HotkeyHandler = (event: KeyboardEvent) => void;

export interface HotkeyOptions {
  /** 焦点在输入框/文本域/富文本内也触发(默认 false,输入框守卫生效) */
  allowInInput?: boolean;
}

/** 单条组合键的解析形:主键(小写)+ 是否要求 mod */
interface ParsedCombo {
  key: string;
  mod: boolean;
}

/** 解析组合键描述;支持 单键 / "mod+单键" / 裸 "+" */
export function parseHotkey(combo: string): ParsedCombo {
  if (combo === "+") return { key: "+", mod: false };
  const parts = combo.split("+");
  const mod = parts.length > 1 && parts[0].toLowerCase() === "mod";
  const key = (mod ? parts.slice(1) : parts).join("+").toLowerCase();
  return { key, mod };
}

/** 事件侧是否命中已解析组合键 */
function matchesCombo(event: KeyboardEvent, combo: ParsedCombo): boolean {
  if (event.key.toLowerCase() !== combo.key) return false;
  const modHeld = event.metaKey || event.ctrlKey;
  if (combo.mod) return modHeld && !event.altKey;
  // 单键:meta/ctrl/alt 任一按住即视为别的快捷键,不认领
  return !modHeld && !event.altKey;
}

/** 输入框守卫:正在打字的元素上不触发(除非 allowInInput) */
function isTypingTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  // 富文本(CodeMirror 的 .cm-content 等):isContentEditable 覆盖继承;
  // jsdom 不实算该属性(恒 undefined),回退读 contenteditable 特性本身
  if (target.isContentEditable === true) return true;
  const editable = target.getAttribute("contenteditable");
  if (editable === "" || editable === "true" || editable === "plaintext-only") return true;
  const tag = target.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
}

/**
 * 注册全局快捷键(键 = 组合键描述,值 = 处理器)。同一次调用的所有键共用
 * 一份 options;需要差异化(如 escape 允许输入框内触发)就再调一次。
 */
export function useHotkeys(map: Record<string, HotkeyHandler>, options: HotkeyOptions = {}): void {
  const mapRef = useRef(map);
  const optionsRef = useRef(options);

  // 每次提交后刷新 ref:监听器读到的永远是最新 handlers/options
  useEffect(() => {
    mapRef.current = map;
    optionsRef.current = options;
  });

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      for (const [combo, handler] of Object.entries(mapRef.current)) {
        if (!matchesCombo(event, parseHotkey(combo))) continue;
        if (!optionsRef.current.allowInInput && isTypingTarget(event.target)) continue;
        handler(event);
        return; // 首个命中即止:一条击键只触发一个动作
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);
}
