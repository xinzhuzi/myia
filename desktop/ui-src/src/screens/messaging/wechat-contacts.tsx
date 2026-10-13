/**
 * 微信联系人工作台浏览器(task 10-14-wechat-contacts R5;挂载点 =
 * wechat-local.tsx WechatLocalSection CardContent 尾部分区,判例
 * SessionReader/LocalDbQuery 同款——集成批接线)。
 *
 * 面板四件套(prd R5):
 * - 计数 chip 行(五桶人话 + 实值):点击 chip = type 筛选 + 首页拉取
 *   (counts 恒全量,chip 数字来自查询实值,非硬编码);
 * - 搜索框:debounce 200ms 触发,清空恢复当前桶首页;
 * - 列表:100/页 + 「加载更多」cursor 续拉(C1「加载更早」同 idiom,不引
 *   入虚拟列表);行 = 显示名 + username(mono)+ 类型徽标 + former 行证据
 *   徽标(「会话痕迹」/「身份字段残留」;无徽标 = 仅残留低置信);
 * - 考古面(「曾经的好友」chip 才进):顶部常驻声明行(人话,如实声明
 *   「部分找回、非保证」)+ with_residue 仅此触发(AC9 域收缩:346MB
 *   message 副本只在考古面按需解密,「考古中…」态如实呈现)+ Tier 计数
 *   + stranger/room_verify 子卡 + 标签尾注。
 * - 导出行:三格式勾选(JSON 文件 / CSV 表格 / 通讯录 VCF)+ 「导出当前
 *   筛选」→ 壳命令(保存对话框定基础名,取消 = 静默)→ 回执路径列表
 *   (群导出面板判例:截断 + title 悬浮全路径)。
 *
 * 错误族 asSidecarError 结构化直显不重试(ReadOnlyError 判例同款;桥
 * 20/21/22 → code + 修复指引)。读回仅展示,不入情报管线(G3 同纪律)。
 */
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { SidecarRequestError } from "@/lib/api";

import { asSidecarError } from "./api";
import {
  wechatContactsExport,
  wechatLocalContacts,
  type WechatContactsCounts,
  type WechatContactsExportResult,
  type WechatContactRow,
  type WechatStrangerRow,
} from "./wechat-contacts-api";

/** 可见五桶(chip 词面人话 + wire 值;文案判例:UI 人话/协议英文)。 */
const BUCKETS: Array<{ type: string; label: string }> = [
  { type: "friend", label: "好友" },
  { type: "group", label: "群聊" },
  { type: "official", label: "公众号" },
  { type: "former", label: "曾经的好友" },
  { type: "other", label: "其他" },
];

/** 桶 wire 值 → 人话(行内类型徽标/导出文案共用)。 */
function typeLabel(type: string): string {
  return BUCKETS.find((bucket) => bucket.type === type)?.label ?? "其他";
}

/** evidence wire 值 → 人话徽标(「会话痕迹」/「身份字段残留」)。 */
function evidenceBadges(evidence: string[]): Array<{ key: string; label: string }> {
  const badges: Array<{ key: string; label: string }> = [];
  if (evidence.includes("msg_residue")) badges.push({ key: "msg_residue", label: "会话痕迹" });
  if (evidence.includes("identity_fields")) badges.push({ key: "identity_fields", label: "身份字段残留" });
  return badges;
}

/** 只读命令的结构化错误行(wechat-local.tsx ReadOnlyError 同形孪生——面板
 * 内联内容不带 role="alert",页面级 alert 语义归屏顶 ErrorBox)。 */
function ContactsError({ error, testId }: { error: SidecarRequestError; testId: string }) {
  const fixHint =
    typeof error.data === "object" && error.data !== null && "fix_hint" in error.data
      ? String((error.data as Record<string, unknown>).fix_hint)
      : null;
  return (
    <div
      className="flex min-w-0 flex-col gap-0.5 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive"
      data-testid={testId}
    >
      <span className="min-w-0 break-words">
        {error.message}(code={error.code})
      </span>
      {fixHint ? <span className="min-w-0 break-words text-2xs opacity-80">修复指引:{fixHint}</span> : null}
    </div>
  );
}

/** 导出态机(idle/导出中/成功/失败;取消 = 静默回 idle,群导出判例)。 */
type ExportState =
  | { phase: "idle" }
  | { phase: "exporting" }
  | { phase: "success"; result: WechatContactsExportResult }
  | { phase: "failed"; error: SidecarRequestError };

/** 导出回执行(成功):件名 + 路径(截断 + title 悬浮全路径)。 */
function ExportReceipt({ result }: { result: WechatContactsExportResult }) {
  return (
    <div className="flex min-w-0 flex-col gap-0.5" role="status" data-testid="wechat-contacts-receipt">
      <p className="text-2xs text-ok">
        已导出 {result.total_rows.toLocaleString("en-US")} 行,共 {result.files.length} 件:
      </p>
      {result.files.map((file) => (
        <p key={file.path} className="min-w-0 truncate font-mono text-2xs text-muted-foreground" title={file.path}>
          {file.name}({file.rows.toLocaleString("en-US")} 行):{file.path}
        </p>
      ))}
    </div>
  );
}

/** 联系人工作台浏览器(微信本机工作台族尾部分区;纯组件态,读回不入管线)。 */
export function ContactsBrowser() {
  const [activeType, setActiveType] = useState("friend");
  const [keywordInput, setKeywordInput] = useState("");
  const [debouncedKeyword, setDebouncedKeyword] = useState("");
  const [counts, setCounts] = useState<WechatContactsCounts | null>(null);
  const [rows, setRows] = useState<WechatContactRow[]>([]);
  const [nextCursor, setNextCursor] = useState<string | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  // 考古面伴随件(仅「曾经的好友」chip 的应答携带;跨 chip 保留最后一次,
  // 换桶不即时清空——考古子卡是面板级呈现,重进 former chip 即刷新)
  const [tiers, setTiers] = useState<{ msg_residue: number; table_only: number } | null>(null);
  const [stranger, setStranger] = useState<WechatStrangerRow[]>([]);
  const [roomVerify, setRoomVerify] = useState<{ present: boolean; rows: number } | null>(null);
  const [labelsCount, setLabelsCount] = useState<number | null>(null);
  // 导出面
  const [formats, setFormats] = useState<Record<string, boolean>>({ json: true, csv: false, vcf: false });
  const [exportState, setExportState] = useState<ExportState>({ phase: "idle" });

  // 请求序号防串页(快速切 chip/搜索时旧应答作废)
  const requestSeq = useRef(0);
  // 搜索 debounce 200ms(WeFlow 120ms 语义取整避抖)
  const debounceTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  useEffect(() => {
    if (debounceTimer.current) clearTimeout(debounceTimer.current);
    debounceTimer.current = setTimeout(() => setDebouncedKeyword(keywordInput.trim()), 200);
    return () => {
      if (debounceTimer.current) clearTimeout(debounceTimer.current);
    };
  }, [keywordInput]);

  const isFormer = activeType === "former";
  const trimmedKeyword = debouncedKeyword || undefined;

  const fetchPage = useCallback(
    async (mode: "first" | "more", cursor?: string | null) => {
      const seq = ++requestSeq.current;
      if (mode === "first") {
        setLoading(true);
        setRows([]);
        setNextCursor(null);
        setHasMore(false);
      } else {
        setLoadingMore(true);
      }
      setError(null);
      try {
        const view = await wechatLocalContacts({
          type: activeType,
          keyword: trimmedKeyword,
          limit: 100,
          cursor: cursor ?? undefined,
          // AC9 域收缩:with_residue 仅考古 chip(「曾经的好友」)触发,
          // 346MB message 副本不进常规浏览/轮询
          with_residue: activeType === "former",
        });
        if (seq !== requestSeq.current) return; // 过期应答作废
        setCounts(view.counts);
        setLabelsCount(view.labels.length);
        if (activeType === "former") {
          setTiers(view.former_tiers);
          setStranger(view.stranger);
          setRoomVerify(view.room_verify);
        }
        if (mode === "first") {
          setRows(view.rows);
        } else {
          setRows((previous) => [...previous, ...view.rows]);
        }
        setNextCursor(view.next_cursor);
        setHasMore(view.has_more);
      } catch (raw) {
        if (seq !== requestSeq.current) return;
        setError(asSidecarError(raw));
      } finally {
        if (seq === requestSeq.current) {
          setLoading(false);
          setLoadingMore(false);
        }
      }
    },
    [activeType, trimmedKeyword],
  );

  // 首/翻条件变化(桶或关键词)→ 首页拉取;挂载即取(计数 chip 立刻有实值)
  useEffect(() => {
    void fetchPage("first");
  }, [fetchPage]);

  const runExport = useCallback(async () => {
    const selected = Object.entries(formats)
      .filter(([, checked]) => checked)
      .map(([format]) => format);
    if (selected.length === 0) {
      setExportState({
        phase: "failed",
        error: new SidecarRequestError({
          code: "invalid_params",
          path: "$.formats",
          message: "至少勾选一种导出格式(JSON / CSV / VCF)",
        }),
      });
      return;
    }
    setExportState({ phase: "exporting" });
    try {
      // null = 用户取消保存对话框:静默回 idle(群导出判例)
      const result = await wechatContactsExport({
        type: activeType,
        keyword: trimmedKeyword,
        withResidue: isFormer,
        formats: selected,
      });
      setExportState(result === null ? { phase: "idle" } : { phase: "success", result });
    } catch (raw) {
      setExportState({ phase: "failed", error: asSidecarError(raw) });
    }
  }, [activeType, formats, isFormer, trimmedKeyword]);

  const exportFormats = useMemo(
    () => [
      { key: "json", label: "JSON 文件" },
      { key: "csv", label: "CSV 表格" },
      { key: "vcf", label: "通讯录 VCF" },
    ],
    [],
  );

  return (
    <div className="flex min-w-0 flex-col gap-2" data-testid="wechat-contacts">
      <p className="min-w-0 break-words text-xs font-medium text-foreground">
        联系人
        <span className="ml-2 text-2xs font-normal text-muted-foreground">
          解密副本只读分类浏览(好友/群聊/公众号/曾经的好友);找回是考古呈现,只列表与导出,零重加操作
        </span>
      </p>

      {/* 计数 chip 行:五桶人话 + 实值;点击 = type 筛选 + 首页拉取 */}
      <div className="flex min-w-0 flex-wrap items-center gap-1.5" data-testid="wechat-contacts-chips">
        {BUCKETS.map((bucket) => {
          const active = activeType === bucket.type;
          return (
            <button
              key={bucket.type}
              type="button"
              aria-pressed={active}
              className={cn(
                "inline-flex shrink-0 items-center gap-1 rounded-full border px-2.5 py-1 text-2xs transition-colors duration-(--duration-fast) ease-out-expo",
                active
                  ? "border-primary/40 bg-primary/10 font-medium text-foreground"
                  : "border-border/60 text-muted-foreground hover:bg-accent/60",
              )}
              data-testid={`wechat-contacts-chip-${bucket.type}`}
              onClick={() => setActiveType(bucket.type)}
            >
              {bucket.label}
              <span className="font-mono">
                {counts ? counts[bucket.type as keyof WechatContactsCounts].toLocaleString("en-US") : "…"}
              </span>
            </button>
          );
        })}
      </div>

      {/* 搜索框:debounce 200ms;清空恢复当前桶首页 */}
      <div className="flex min-w-0 flex-wrap items-center gap-2">
        <Input
          aria-label="联系人搜索"
          placeholder="按备注 / 昵称 / 别名 / 微信号 / 拼音搜索"
          className="h-8 w-64 text-xs"
          value={keywordInput}
          disabled={loading}
          onChange={(event) => setKeywordInput(event.target.value)}
          data-testid="wechat-contacts-search"
        />
        <span className="text-2xs text-muted-foreground">
          {loading ? (isFormer ? "考古中…(首次需解密消息库副本,稍候)" : "查询中…") : ""}
        </span>
      </div>

      {/* 考古面:声明行常驻(仅「曾经的好友」chip)——如实声明非保证 */}
      {isFormer ? (
        <div
          className="flex min-w-0 flex-col gap-1 rounded-md border border-warning/40 bg-warning/10 p-2.5"
          data-testid="wechat-contacts-declaration"
        >
          <p className="min-w-0 break-words text-2xs leading-relaxed text-foreground">
            考古呈现:从本地库残留找出,不保证完整与准确;按证据分层,可能含群内陌生人缓存。
          </p>
          {tiers ? (
            <p className="min-w-0 break-words text-2xs text-muted-foreground" data-testid="wechat-contacts-tiers">
              分层:有会话痕迹 {tiers.msg_residue.toLocaleString("en-US")} · 仅通讯录残留{" "}
              {tiers.table_only.toLocaleString("en-US")}
            </p>
          ) : (
            <p className="text-2xs text-muted-foreground">分层计数尚未取得(消息库副本缺席或考古未跑)。</p>
          )}
        </div>
      ) : null}

      {error ? <ContactsError error={error} testId="wechat-contacts-error" /> : null}

      {/* 列表:行序 = 库序(v1 不承诺时间序);加载更多 cursor 续拉 */}
      {rows.length > 0 ? (
        <ul className="flex min-w-0 flex-col gap-1" data-testid="wechat-contacts-list">
          {rows.map((row) => (
            <li
              key={row.username}
              className="flex min-w-0 flex-wrap items-center gap-1.5 rounded-md border border-border/50 px-2.5 py-1.5 text-xs"
              data-testid="wechat-contacts-row"
            >
              <span className="min-w-0 max-w-56 shrink truncate font-medium text-foreground" title={row.display_name}>
                {row.display_name}
              </span>
              <span className="min-w-0 max-w-48 shrink truncate font-mono text-2xs text-muted-foreground" title={row.username}>
                {row.username}
              </span>
              <Badge variant="outline">{typeLabel(row.type)}</Badge>
              {row.type === "group" && typeof row.member_count === "number" ? (
                <Badge variant="secondary">成员 {row.member_count.toLocaleString("en-US")}</Badge>
              ) : null}
              {evidenceBadges(row.evidence).map((badge) => (
                <Badge key={badge.key} variant="secondary" data-testid="wechat-contacts-evidence">
                  {badge.label}
                </Badge>
              ))}
            </li>
          ))}
        </ul>
      ) : null}
      {!loading && rows.length === 0 && !error ? (
        <p className="text-2xs text-muted-foreground">当前筛选零条(库内无命中或副本缺域)。</p>
      ) : null}
      {hasMore ? (
        <div>
          <Button
            size="sm"
            variant="outline"
            disabled={loadingMore}
            data-testid="wechat-contacts-load-more"
            onClick={() => void fetchPage("more", nextCursor)}
          >
            {loadingMore ? "加载中…" : "加载更多"}
          </Button>
        </div>
      ) : null}

      {/* 考古子卡:stranger(非好友联系人缓存)+ room_verify(群申请记录) */}
      {isFormer ? (
        <div className="flex min-w-0 flex-col gap-1.5" data-testid="wechat-contacts-archaeology">
          <div className="flex min-w-0 flex-col gap-1 rounded-md border border-border/60 bg-muted/30 p-2.5">
            <p className="min-w-0 break-words text-2xs font-medium text-foreground">
              非好友联系人缓存{stranger.length > 0 ? `,${stranger.length.toLocaleString("en-US")} 条` : ""}
            </p>
            {stranger.length === 0 ? (
              <p className="text-2xs text-muted-foreground" data-testid="wechat-contacts-stranger">
                本机无记录(尚未入正常联系集的类联系人记录)。
              </p>
            ) : (
              <ul className="flex min-w-0 flex-col gap-0.5" data-testid="wechat-contacts-stranger">
                {stranger.map((entry) => (
                  <li key={entry.username} className="flex min-w-0 flex-wrap items-center gap-1.5 text-2xs">
                    <span className="min-w-0 max-w-48 shrink truncate text-foreground" title={entry.display_name}>
                      {entry.display_name}
                    </span>
                    <span className="min-w-0 max-w-64 shrink truncate font-mono text-muted-foreground" title={entry.username}>
                      {entry.username}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="flex min-w-0 flex-col gap-1 rounded-md border border-border/60 bg-muted/30 p-2.5">
            <p className="min-w-0 break-words text-2xs font-medium text-foreground" data-testid="wechat-contacts-room-verify">
              群申请记录{roomVerify && roomVerify.rows > 0 ? `,有 ${roomVerify.rows.toLocaleString("en-US")} 条` : ",本机无记录"}
            </p>
            <p className="min-w-0 break-words text-2xs text-muted-foreground">推断语义:群验证/入群申请记录(来源表只读呈现)。</p>
          </div>
        </div>
      ) : null}

      {/* 导出行:三格式勾选 + 导出当前筛选(壳侧保存对话框;取消 = 静默) */}
      <div className="flex min-w-0 flex-col gap-1.5" data-testid="wechat-contacts-export-row">
        <div className="flex min-w-0 flex-wrap items-center gap-2">
          {exportFormats.map((format) => (
            <label key={format.key} className="inline-flex shrink-0 cursor-pointer items-center gap-1 text-2xs text-muted-foreground">
              <input
                type="checkbox"
                checked={formats[format.key] ?? false}
                onChange={(event) => setFormats((previous) => ({ ...previous, [format.key]: event.target.checked }))}
                data-testid={`wechat-contacts-export-${format.key}`}
              />
              {format.label}
            </label>
          ))}
          <Button
            size="sm"
            variant="outline"
            className="shrink-0"
            disabled={exportState.phase === "exporting"}
            data-testid="wechat-contacts-export"
            onClick={() => void runExport()}
          >
            {exportState.phase === "exporting" ? "导出中…" : `导出当前筛选(${typeLabel(activeType)})`}
          </Button>
        </div>
        {exportState.phase === "success" ? <ExportReceipt result={exportState.result} /> : null}
        {exportState.phase === "failed" ? <ContactsError error={exportState.error} testId="wechat-contacts-export-error" /> : null}
      </div>

      {/* 标签尾注:库内标签清单计数,不做逐人关联(归属在加密缓冲内,诚实不臆造) */}
      <p className="text-2xs text-muted-foreground" data-testid="wechat-contacts-labels">
        {labelsCount !== null ? `库内标签:${labelsCount} 个(标签与联系人的归属在加密缓冲内,不做逐人关联)` : ""}
      </p>
    </div>
  );
}
