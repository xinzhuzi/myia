import { useEffect, useState } from "react";
import { convertFileSrc, invoke } from "@tauri-apps/api/core";
import { Button } from "@/components/ui/button";

/** Preliminary shape check only; the Rust command owns data-root authorization. */
function absoluteImagePath(path: string): boolean {
  return !path.includes("\0") && (/^\//.test(path) || /^[A-Za-z]:[\\/]/.test(path) || path.startsWith("\\\\"))
    && !path.split(/[\\/]/).includes("..");
}

function SavedImage({ path, index }: { path: string; index: number }) {
  const [src, setSrc] = useState<string | null>(null);
  const [phase, setPhase] = useState<"loading" | "ready" | "denied" | "error">("loading");
  const [fullSize, setFullSize] = useState(false);
  useEffect(() => {
    let active = true;
    void (async () => {
      try {
        if (!absoluteImagePath(path)) throw new Error("invalid path");
        const allowed = await invoke<string>("feed_image_path", { path });
        if (!active) return;
        if (typeof allowed !== "string" || !absoluteImagePath(allowed)) throw new Error("invalid authorization");
        setSrc(convertFileSrc(allowed));
      } catch {
        if (active) setPhase("denied");
      }
    })();
    return () => { active = false; };
  }, [path]);

  const failed = phase === "denied" || phase === "error";
  return (
    <li className="flex min-w-0 flex-col gap-1.5">
      {src && !failed ? (
        <figure className="flex min-w-0 flex-col items-start gap-1.5">
          <div className="max-h-96 max-w-full overflow-auto rounded-md border border-border/60 bg-muted/20">
            <img src={src} alt={`已保存配图 ${index + 1}`} decoding="async"
              className={fullSize ? "block max-w-none" : "block h-auto max-h-48 w-64 max-w-full object-contain"}
              onLoad={() => setPhase("ready")} onError={() => setPhase("error")} />
          </div>
          {phase === "ready" ? (
            <Button variant="ghost" size="sm" aria-expanded={fullSize}
              aria-label={fullSize ? `收起图片 ${index + 1} 原尺寸` : `查看图片 ${index + 1} 原尺寸`}
              onClick={(event) => { event.stopPropagation(); setFullSize((value) => !value); }}>
              {fullSize ? "收起原图" : "查看原尺寸"}
            </Button>
          ) : null}
        </figure>
      ) : null}
      {phase !== "ready" ? (
        <span role="status" className="text-2xs text-muted-foreground">
          {phase === "denied" ? "图片不可预览，文件可能已移动或不在保存目录内"
            : phase === "error" ? "图片加载失败，可核对下方保存路径" : "图片加载中…"}
        </span>
      ) : null}
      <span className="break-all font-mono text-2xs text-muted-foreground">{path}</span>
    </li>
  );
}

/** Same-screen previews follow the existing WeChat media slot pattern. */
export function FeedLocalImages({ paths, testId }: { paths: unknown; testId?: string }) {
  if (!Array.isArray(paths)) return null;
  const files = [...new Set(paths.filter((value): value is string => typeof value === "string" && value.trim().length > 0))];
  if (!files.length) return null;
  return (
    <div className="mt-1.5 flex min-w-0 flex-col gap-1" data-testid={testId}>
      <span className="text-2xs text-muted-foreground">图文件 {files.length} 张</span>
      <ul className="flex min-w-0 flex-col gap-3">
        {files.map((path, index) => <SavedImage key={path} path={path} index={index} />)}
      </ul>
    </div>
  );
}
