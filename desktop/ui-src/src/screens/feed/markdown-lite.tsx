/**
 * Markdown-Lite 渲染(10-06-feed-channel-groups:prompt/store_report 渠道
 * 日报的「markdown 文档视图」)。零依赖最小集——块级:标题 #/##/###、无序/
 * 有序列表、代码围栏、引用、分隔线、段落;行内:**加粗**、`code`、裸
 * http(s) 链接。React 文本节点天然转义,不做 HTML 直插(安全面零让步);
 * 未覆盖的语法按原文呈现(degrade gracefully,日报可读性不破)。
 *
 * 链接出口(深审 F4):裸链接此前是 `preventDefault` 的死链(点击无路)。
 * 现走 openInBrowser 受控门 —— plugin-shell open(capabilities 同「打开
 * 原文」:scope 仅 https?://),与 feed 卡片原文链接同一纪律;正则只匹配
 * http(s)://,门与词表同面。浏览器直开(vitest/预览)不加载壳包,点击才
 * 动态 import(失败静默,不炸文档视图)。
 */
import type { ReactNode } from "react";

/** 受控开链(plugin-shell open;动态 import:浏览器直开零加载)。 */
async function openLinkInBrowser(url: string): Promise<void> {
  try {
    const shell = await import("@tauri-apps/plugin-shell");
    await shell.open(url);
  } catch {
    // 壳不可用(浏览器直开/门拒绝):静默 —— 文档视图不为开链炸渲染
  }
}

/** 行内解析:**加粗** / `code` / 裸 http(s) 链接(其余原样文本节点) */
function inlineNodes(text: string, keyPrefix: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  // 捕获组:加粗 | 行内代码 | 裸链接
  const pattern = /(\*\*[^*]+\*\*)|(`[^`]+`)|(https?:\/\/[^\s)>\]]+)/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;
  let index = 0;
  while ((match = pattern.exec(text)) !== null) {
    if (match.index > lastIndex) nodes.push(text.slice(lastIndex, match.index));
    const token = match[0];
    const key = `${keyPrefix}-i${index}`;
    index += 1;
    if (token.startsWith("**")) {
      nodes.push(
        <strong key={key} className="font-semibold text-foreground">
          {token.slice(2, -2)}
        </strong>,
      );
    } else if (token.startsWith("`")) {
      nodes.push(
        <code key={key} className="rounded-sm bg-muted/60 px-1 py-0.5 font-mono text-xs text-foreground">
          {token.slice(1, -1)}
        </code>,
      );
    } else {
      nodes.push(
        <a
          key={key}
          href={token}
          className="text-primary underline underline-offset-2 hover:text-primary/80"
          data-md-link={token}
          title={`在浏览器打开:${token}`}
          onClick={(event) => {
            event.preventDefault(); // webview 不导航(死链根因),走受控门
            void openLinkInBrowser(token);
          }}
        >
          {token}
        </a>,
      );
    }
    lastIndex = match.index + token.length;
  }
  if (lastIndex < text.length) nodes.push(text.slice(lastIndex));
  return nodes;
}

type Block =
  | { type: "heading"; level: 1 | 2 | 3; text: string }
  | { type: "paragraph"; text: string }
  | { type: "list"; ordered: boolean; items: string[] }
  | { type: "code"; lines: string[] }
  | { type: "quote"; lines: string[] }
  | { type: "hr" };

/** 块级解析:逐行扫描,围栏/列表/引用聚块,其余按段落(空行分隔) */
function parseBlocks(markdown: string): Block[] {
  const blocks: Block[] = [];
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  let paragraph: string[] = [];
  const flushParagraph = () => {
    if (paragraph.length > 0) {
      blocks.push({ type: "paragraph", text: paragraph.join(" ") });
      paragraph = [];
    }
  };
  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const fence = line.match(/^```/);
    if (fence) {
      flushParagraph();
      const code: string[] = [];
      index += 1;
      while (index < lines.length && !lines[index].startsWith("```")) {
        code.push(lines[index]);
        index += 1;
      }
      blocks.push({ type: "code", lines: code });
      continue;
    }
    if (/^\s*$/.test(line)) {
      flushParagraph();
      continue;
    }
    if (/^(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) {
      flushParagraph();
      blocks.push({ type: "hr" });
      continue;
    }
    const heading = line.match(/^(#{1,3})\s+(.*)$/);
    if (heading) {
      flushParagraph();
      blocks.push({ type: "heading", level: heading[1].length as 1 | 2 | 3, text: heading[2] });
      continue;
    }
    const bullet = line.match(/^\s*[-*+]\s+(.*)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.*)$/);
    if (bullet || ordered) {
      flushParagraph();
      const isOrdered = Boolean(ordered);
      const items: string[] = [];
      while (index < lines.length) {
        const current = lines[index];
        const currentBullet = current.match(/^\s*[-*+]\s+(.*)$/);
        const currentOrdered = current.match(/^\s*\d+[.)]\s+(.*)$/);
        if (isOrdered ? currentOrdered : currentBullet) {
          items.push((isOrdered ? currentOrdered : currentBullet)![1]);
          index += 1;
        } else {
          break;
        }
      }
      index -= 1; // 外层 for 自增回当前未消费行
      blocks.push({ type: "list", ordered: isOrdered, items });
      continue;
    }
    const quote = line.match(/^>\s?(.*)$/);
    if (quote) {
      flushParagraph();
      const quoted: string[] = [quote[1]];
      index += 1;
      while (index < lines.length) {
        const next = lines[index].match(/^>\s?(.*)$/);
        if (!next) break;
        quoted.push(next[1]);
        index += 1;
      }
      blocks.push({ type: "quote", lines: quoted });
      continue;
    }
    paragraph.push(line.trim());
  }
  flushParagraph();
  return blocks;
}

const HEADING_CLASS: Record<1 | 2 | 3, string> = {
  1: "text-base font-semibold text-foreground",
  2: "text-sm font-semibold text-foreground",
  3: "text-sm font-medium text-foreground/90",
};

/** markdown-lite 文档视图:data-testid 前缀供渠道卡定位(doc 日报呈现) */
export function MarkdownLite({ markdown, testId }: { markdown: string; testId?: string }) {
  const blocks = parseBlocks(markdown);
  return (
    <div className="flex flex-col gap-1.5 text-sm leading-relaxed text-foreground/90" data-testid={testId}>
      {blocks.map((block, index) => {
        const key = `b${index}`;
        switch (block.type) {
          case "heading": {
            const Tag = (`h${block.level}` as const);
            return (
              <Tag key={key} className={HEADING_CLASS[block.level]} data-md-heading={block.level}>
                {inlineNodes(block.text, key)}
              </Tag>
            );
          }
          case "code":
            return (
              <pre
                key={key}
                className="overflow-x-auto whitespace-pre-wrap break-words rounded-md border border-border/60 bg-muted/30 px-2.5 py-2 font-mono text-xs leading-relaxed text-foreground/90"
              >
                {block.lines.join("\n")}
              </pre>
            );
          case "list":
            return block.ordered ? (
              <ol key={key} className="ml-4 list-decimal space-y-0.5" data-md-list="ol">
                {block.items.map((entry, itemIndex) => (
                  <li key={`${key}-${itemIndex}`}>{inlineNodes(entry, `${key}-${itemIndex}`)}</li>
                ))}
              </ol>
            ) : (
              <ul key={key} className="ml-4 list-disc space-y-0.5" data-md-list="ul">
                {block.items.map((entry, itemIndex) => (
                  <li key={`${key}-${itemIndex}`}>{inlineNodes(entry, `${key}-${itemIndex}`)}</li>
                ))}
              </ul>
            );
          case "quote":
            return (
              <blockquote
                key={key}
                className="border-l-2 border-border pl-2.5 text-muted-foreground"
              >
                {block.lines.map((entry, lineIndex) => (
                  <span key={`${key}-${lineIndex}`} className="block">
                    {inlineNodes(entry, `${key}-${lineIndex}`)}
                  </span>
                ))}
              </blockquote>
            );
          case "hr":
            return <hr key={key} className="border-border/70" />;
          default:
            return <p key={key}>{inlineNodes(block.text, key)}</p>;
        }
      })}
    </div>
  );
}
