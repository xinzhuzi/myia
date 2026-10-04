import { yaml } from "@codemirror/lang-yaml";
import { EditorView } from "@codemirror/view";
import { oneDark } from "@codemirror/theme-one-dark";
import CodeMirror from "@uiw/react-codemirror";

import { cn } from "@/lib/utils";

interface EditorPaneProps {
  /** 受控值(编辑器内容 = 屏层 doc.content) */
  value: string;
  /** 内容变更(屏层只更新草稿,不自动保存) */
  onChange: (value: string) => void;
  className?: string;
}

/**
 * 编辑面铬色对齐 Kestra 令牌族(10-04-ui-kestra-anchor):oneDark 只留语法
 * 配色,编辑底/行号槽/激活行改走本仓 --background/--border/--accent 令牌
 * (= --ks-bg-input #14181f / --ks-border-default / --ks-bg-hover 族;
 * Kestra Monaco 同以暗于卡面的 input 底承载编辑面)。结构参照
 * Apache-2.0 kestra design-system KsEditor 的令牌用法,借语义不抄码。
 */
const KESTRA_CHROME = EditorView.theme({
  "&": { backgroundColor: "var(--background)", color: "var(--foreground)", height: "100%" },
  ".cm-scroller": { fontFamily: "var(--font-mono)" },
  ".cm-gutters": {
    backgroundColor: "var(--background)",
    color: "var(--muted-foreground)",
    borderRight: "1px solid var(--border)",
  },
  ".cm-activeLine": { backgroundColor: "color-mix(in srgb, var(--accent) 25%, transparent)" },
  ".cm-activeLineGutter": { backgroundColor: "color-mix(in srgb, var(--accent) 40%, transparent)" },
  "&.cm-focused": { outline: "none" },
  ".cm-selectionBackground": { backgroundColor: "color-mix(in srgb, var(--primary) 35%, transparent) !important" },
  ".cm-cursor": { borderLeftColor: "var(--link)" },
});

/**
 * CodeMirror 封装(@uiw/react-codemirror wrapper 路线,任务决议 5):
 * YAML 语法高亮 + oneDark 语法配色 + Kestra 铬色(底/槽/激活行走令牌)+ 行号。
 * 受控 value/onChange;快捷键(Cmd+S 保存)由屏层监听 window,编辑器不抢。
 */
export function EditorPane({ value, onChange, className }: EditorPaneProps) {
  return (
    <div
      className={cn("min-h-0 overflow-hidden rounded-md border border-border bg-background", className)}
      data-testid="yaml-editor"
    >
      <CodeMirror
        value={value}
        height="100%"
        theme={[oneDark, KESTRA_CHROME]}
        extensions={[yaml()]}
        basicSetup={{
          lineNumbers: true,
          foldGutter: true,
          highlightActiveLine: true,
          autocompletion: true,
          bracketMatching: true,
          closeBrackets: true,
        }}
        onChange={(next) => onChange(next)}
      />
    </div>
  );
}
