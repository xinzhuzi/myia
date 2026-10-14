// @vitest-environment node
//
// 建源向导生成器测试(PRD AC4):≥3 组表单态逐字节断言产物文本 + 转义规则
// (设计拷问修正①②③:max_pages 双模式/引号转义/字段名约束)+ 分步校验规则
// + validate 契约桩(镜像 schema.py 后端终门语义的 JS 桩,经真实
// screens/yaml-editor/api.ts validateYaml 通道调用,证明产物过同门校验)。
// 真后端装载验证(load_category)归复查员的真数据命令,不在此伪造。
import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { CATEGORY_ID_PATTERN, validateYaml } from "../../yaml-editor/api";
import {
  DEFAULT_USER_AGENT,
  SCHEDULE_CUSTOM,
  buildCategoryYaml,
  fieldSelectorValue,
  initialWizardForm,
  looksLikeCrontab,
  looksLikeHttpUrl,
  resolveScheduleCron,
  wizardStepErrors,
  yamlQuote,
} from "./build-category-yaml";
import type { WizardForm } from "./build-category-yaml";

// ---------------------------------------------------------------------------
// 夹具:直接构造表单态(绕过 UI 交互;交互链归 source-wizard-dialog.test.tsx)
// ---------------------------------------------------------------------------

function form(overrides: Partial<WizardForm> = {}): WizardForm {
  return { ...initialWizardForm(), ...overrides };
}

/** 羽翼丰满的基础表单(不翻页/无 UA):逐字节断言组 A */
const FORM_A: WizardForm = form({
  categoryId: "news-list",
  categoryName: "每日新闻",
  schedulePreset: "0 10 * * *",
  url: "https://example.com/news",
  userAgent: "",
  itemSelector: "div.list-item",
  fields: [
    { name: "title", selector: "h3 a", useHref: false },
    { name: "url", selector: "h3 a", useHref: true },
  ],
});

/** template 翻页 + 默认 UA + 自定义 cron + 自定义字段:逐字节断言组 B */
const FORM_B: WizardForm = form({
  categoryId: "gpu-daily",
  categoryName: "显卡行情日报",
  schedulePreset: SCHEDULE_CUSTOM,
  scheduleCustom: "0 */6 * * *",
  sourceName: "zol",
  url: "https://detail.zol.com.cn/vga/{page}.html",
  userAgent: DEFAULT_USER_AGENT,
  pagination: { mode: "template", maxPages: 5 },
  itemSelector: "div.list-item",
  fields: [
    { name: "title", selector: "h3 a", useHref: false },
    { name: "url", selector: "h3 a", useHref: true },
    { name: "price", selector: "span.price-type", useHref: false },
  ],
});

/** selector 翻页 + 值里带引号的选择器(DevTools Copy selector 常态):逐字节断言组 C */
const FORM_C: WizardForm = form({
  categoryId: "board-top",
  categoryName: '榜单"热帖"榜',
  schedulePreset: "0 9 * * 1",
  sourceName: "main",
  url: "https://b.example.com/top",
  userAgent: "",
  pagination: { mode: "selector", selector: 'a[aria-label="Next"]', maxPages: 3 },
  itemSelector: 'li.row[class~="odd"]',
  fields: [
    { name: "title", selector: 'div[data-id="x"] > a', useHref: false },
    { name: "url", selector: "a", useHref: true },
  ],
});

// ---------------------------------------------------------------------------
// 逐字节断言(PRD R3:产物钉死;行数组写法让每一行都显式)
// ---------------------------------------------------------------------------

describe("build-category-yaml:逐字节断言", () => {
  it("组 A:不翻页 + 清空 UA → 无 headers/pagination 节", () => {
    expect(buildCategoryYaml(FORM_A)).toBe(
      [
        "# 由建源向导生成:普通网页列表采集(每天到点抓一页/几页,提取列表字段)。",
        "# 只配了采集;关键词过滤、分类、推送等下游配置请到「YAML配置」补全。",
        'id: news-list',
        'name: "每日新闻"',
        'schedule: "0 10 * * *"',
        "sources:",
        '  - name: "main"',
        "    engine: static_html",
        '    url: "https://example.com/news"',
        "    method: GET",
        "    extract:              # 提取:item 框住重复的整条,fields 取每条里的字段",
        "      type: list",
        '      item: "div.list-item"',
        "      fields:",
        '        title: "h3 a"',
        '        url: "h3 a@href"',
        "",
      ].join("\n"),
    );
  });

  it("组 B:template 翻页 + 默认 UA → headers/pagination(template)节 + max_pages", () => {
    expect(buildCategoryYaml(FORM_B)).toBe(
      [
        "# 由建源向导生成:普通网页列表采集(每天到点抓一页/几页,提取列表字段)。",
        "# 只配了采集;关键词过滤、分类、推送等下游配置请到「YAML配置」补全。",
        "id: gpu-daily",
        'name: "显卡行情日报"',
        'schedule: "0 */6 * * *"',
        "sources:",
        '  - name: "zol"',
        "    engine: static_html",
        '    url: "https://detail.zol.com.cn/vga/{page}.html"',
        "    method: GET",
        "    headers:              # 浏览器标识;不需要可整节删掉",
        `      User-Agent: "${DEFAULT_USER_AGENT}"`,
        "    pagination:           # 翻页:网址里的 {page} 依次换成页码",
        "      mode: template",
        "      max_pages: 5",
        "    extract:              # 提取:item 框住重复的整条,fields 取每条里的字段",
        "      type: list",
        '      item: "div.list-item"',
        "      fields:",
        '        title: "h3 a"',
        '        url: "h3 a@href"',
        '        price: "span.price-type"',
        "",
      ].join("\n"),
    );
  });

  it("组 C:selector 翻页 + 值带双引号 → YAML 双引号转义(修正①)+ max_pages", () => {
    expect(buildCategoryYaml(FORM_C)).toBe(
      [
        "# 由建源向导生成:普通网页列表采集(每天到点抓一页/几页,提取列表字段)。",
        "# 只配了采集;关键词过滤、分类、推送等下游配置请到「YAML配置」补全。",
        "id: board-top",
        'name: "榜单\\"热帖\\"榜"',
        'schedule: "0 9 * * 1"',
        "sources:",
        '  - name: "main"',
        "    engine: static_html",
        '    url: "https://b.example.com/top"',
        "    method: GET",
        "    pagination:           # 翻页:沿「下一页」链接一直抓到头",
        "      mode: selector",
        '      selector: "a[aria-label=\\"Next\\"]"',
        "      max_pages: 3",
        "    extract:              # 提取:item 框住重复的整条,fields 取每条里的字段",
        "      type: list",
        '      item: "li.row[class~=\\"odd\\"]"',
        "      fields:",
        '        title: "div[data-id=\\"x\\"] > a"',
        '        url: "a@href"',
        "",
      ].join("\n"),
    );
  });

  it("反斜杠也转义(先 \\ 后 \",顺序保证不二次转义)", () => {
    expect(yamlQuote('a"b\\c')).toBe('"a\\"b\\\\c"');
    const content = buildCategoryYaml(
      form({
        categoryId: "x",
        categoryName: "x",
        schedulePreset: "0 10 * * *",
        url: "https://example.com/",
        userAgent: "",
        itemSelector: "a\\.title",
        fields: [{ name: "url", selector: "a\\.title", useHref: true }],
      }),
    );
    expect(content).toContain('item: "a\\\\.title"');
    expect(content).toContain('url: "a\\\\.title@href"');
  });

  it("@href 快捷开关:已带 @href 结尾不重复追加;未勾不加", () => {
    expect(fieldSelectorValue({ name: "url", selector: "h3 a", useHref: true })).toBe("h3 a@href");
    expect(fieldSelectorValue({ name: "url", selector: "h3 a@href", useHref: true })).toBe("h3 a@href");
    expect(fieldSelectorValue({ name: "title", selector: "h3 a", useHref: false })).toBe("h3 a");
  });
});

// ---------------------------------------------------------------------------
// 分步校验(前端预检镜像后端终门;锚点见 build-category-yaml.ts 头注释)
// ---------------------------------------------------------------------------

describe("build-category-yaml:分步校验", () => {
  it("第 1 步:id 正则镜像 schema.py:368 / 品类名 ≤64(schema.py:318)/ schedule 必选(schema.py:1794)", () => {
    expect(wizardStepErrors(form(), 1)).toHaveLength(3); // 空 id + 空名 + 未选频率
    expect(
      wizardStepErrors(
        form({ categoryId: "Bad Id", categoryName: "x".repeat(65), schedulePreset: SCHEDULE_CUSTOM, scheduleCustom: "0 9 *" }),
        1,
      ).join("\n"),
    ).toContain("小写字母");
    expect(wizardStepErrors(form({ categoryId: "Bad Id", categoryName: "正常名" }), 1).join("\n")).not.toContain("太长");
    // 正则本体与 CATEGORY_ID_PATTERN 同源(schema.py:368 逐字符)
    expect(CATEGORY_ID_PATTERN.test("gpu-prices")).toBe(true);
    expect(CATEGORY_ID_PATTERN.test("GPU")).toBe(false);
    // 自定义 cron 形状门(终门 schema.py:1859-1866 CronTrigger)
    expect(looksLikeCrontab("0 9 * * *")).toBe(true);
    expect(looksLikeCrontab("0 9 * *")).toBe(false);
  });

  it("第 2 步:url http(s) 镜像 schema.py:850-856 / template 需 {page} / max_pages 1-10000(schema.py:661)", () => {
    const base = form({ sourceName: "main", url: "https://example.com/list" });
    expect(wizardStepErrors(base, 2)).toHaveLength(0);
    expect(wizardStepErrors(form({ sourceName: "main", url: "ftp://example.com" }), 2).join("\n")).toContain("http");
    expect(looksLikeHttpUrl("https://example.com/{page}")).toBe(true);
    expect(looksLikeHttpUrl("example.com/list")).toBe(false);
    // template 缺 {page} 占位
    expect(
      wizardStepErrors(form({ url: "https://example.com/list", pagination: { mode: "template", maxPages: 5 } }), 2).join("\n"),
    ).toContain("{page}");
    // max_pages 边界(缺省 5 在 UI 层;两端外即拦)
    for (const bad of [0, 10001, 2.5]) {
      expect(
        wizardStepErrors(form({ url: "https://e.com/{page}", pagination: { mode: "template", maxPages: bad } }), 2),
      ).toContain("最多翻几页要填 1-10000 的整数");
    }
    // selector 模式同样要 max_pages(修正③:schema 缺省 1 会静默架空用户选择)
    expect(
      wizardStepErrors(
        form({ url: "https://e.com/top", pagination: { mode: "selector", selector: "a.next", maxPages: 5 } }),
        2,
      ),
    ).toHaveLength(0);
    expect(wizardStepErrors(form({ url: "https://e.com/top", pagination: { mode: "selector", selector: "", maxPages: 5 } }), 2).join("\n")).toContain("下一页");
  });

  it("第 3 步:item 必填(schema.py:740-747)/ fields 必含 url(schema.py:789-795)/ 字段名约束(修正②)/ 查重", () => {
    const good = form({
      itemSelector: "div.item",
      fields: [
        { name: "title", selector: "h3 a", useHref: false },
        { name: "url", selector: "h3 a", useHref: true },
      ],
    });
    expect(wizardStepErrors(good, 3)).toHaveLength(0);
    // item 空
    expect(wizardStepErrors({ ...good, itemSelector: "" }, 3).join("\n")).toContain("列表整条的选择器");
    // 缺 url 字段名
    const noUrl = { ...good, fields: [{ name: "title", selector: "h3 a", useHref: false }] };
    expect(wizardStepErrors(noUrl, 3).join("\n")).toContain("必须有 url");
    // 字段名字符集(裸 YAML 键安全)
    const badName = {
      ...good,
      fields: [
        { name: "my field", selector: "h3 a", useHref: false },
        { name: "url", selector: "h3 a", useHref: true },
      ],
    };
    expect(wizardStepErrors(badName, 3).join("\n")).toContain("字段名「my field」不合规");
    // 数字开头 / 纯数字 / true 之类都会坏裸键语义
    expect(wizardStepErrors({ ...good, fields: [{ name: "1price", selector: "a", useHref: false }, { name: "url", selector: "a", useHref: true }] }, 3).join("\n")).toContain("不合规");
    // 字段名重复
    const dup = {
      ...good,
      fields: [
        { name: "title", selector: "h3 a", useHref: false },
        { name: "title", selector: "h2 a", useHref: false },
        { name: "url", selector: "h3 a", useHref: true },
      ],
    };
    expect(wizardStepErrors(dup, 3).join("\n")).toContain("重复");
    // 行选择器空
    expect(wizardStepErrors({ ...good, fields: [{ name: "url", selector: "", useHref: true }] }, 3).join("\n")).toContain("选择器还没填");
  });

  it("resolveScheduleCron:预设直通 / 自定义取输入", () => {
    expect(resolveScheduleCron(FORM_A)).toBe("0 10 * * *");
    expect(resolveScheduleCron(FORM_B)).toBe("0 */6 * * *");
  });
});

// ---------------------------------------------------------------------------
// validate 契约桩(PRD AC4:「生成器快照 + validate 契约桩分离断言」路线)
// 桩 = schema.py 后端终门对生成器可达形态的 JS 镜像:引号标量完整性(转义感知)、
// 裸键安全集、id/schedule/url/pagination/extract 结构门。经真实 validateYaml
// (screens/yaml-editor/api.ts)通道调用,负例证明桩不是恒真。
// ---------------------------------------------------------------------------

interface StubFinding {
  path: string;
  code: string;
  message: string;
  level: "error" | "warning";
}

/** 去引号还原值(引号形态强校验;非引号形态原样返回供裸字面量断言) */
function unquote(raw: string): string {
  const match = /^"((?:[^"\\]|\\.)*)"$/.exec(raw);
  if (match === null) return raw;
  return match[1];
}

function contractValidate(content: string): { valid: boolean; findings: StubFinding[] } {
  const findings: StubFinding[] = [];
  const error = (path: string, code: string, message: string) =>
    findings.push({ path, code, message, level: "error" });
  const lines = content.split("\n");

  // 1) 引号标量完整性:双引号必须成对闭合(转义感知;生成器产物单行标量)
  for (const [index, line] of lines.entries()) {
    if (!line.includes('"')) continue;
    let inQuote = false;
    for (let i = 0; i < line.length; i += 1) {
      const ch = line[i];
      if (ch === "\\") {
        i += 1; // 转义吃掉下一字符
        continue;
      }
      if (ch === '"') inQuote = !inQuote;
    }
    if (inQuote) error(`line:${index + 1}`, "yaml_syntax", "双引号标量未闭合(转义损坏?)");
  }

  // 2) 裸键安全:每行的键(引号外首个 ':')必须是安全标识符(修正②的下游证明)
  const keyRe = /^(?:- )?[A-Za-z][A-Za-z0-9_-]*$/;
  for (const [index, line] of lines.entries()) {
    if (line.trim() === "" || line.trimStart().startsWith("#")) continue;
    const colonAt = line.indexOf(":");
    if (colonAt === -1) {
      error(`line:${index + 1}`, "yaml_syntax", `无键值形态:${line}`);
      continue;
    }
    const key = line.slice(0, colonAt).trim();
    if (!keyRe.test(key)) error(`line:${index + 1}`, "yaml_syntax", `裸键不安全:${key}`);
  }

  // 3) 结构门(镜像 schema.py 对生成器可达形态的终门)
  const valueOf = (prefix: string): string | null => {
    const line = lines.find((candidate) => candidate.startsWith(prefix));
    return line === undefined ? null : unquote(line.slice(prefix.length).replace(/\s+#.*$/, "").trim());
  };
  const id = valueOf("id: ");
  if (id === null || id === "") error("$.id", "invalid_id", "缺 id");
  else if (!CATEGORY_ID_PATTERN.test(id)) error("$.id", "invalid_id", `id 不合规:${id}`);
  const name = valueOf("name: ");
  if (name === null || name === "") error("$.name", "invalid_name", "缺 name");
  else if (name.length > 64) error("$.name", "invalid_name", "name 超 64 字符(schema.py:318 ShortStr)");
  const schedule = valueOf("schedule: ");
  if (schedule === null || schedule === "") error("$.schedule", "invalid_cron", "缺 schedule(schema.py:1794 必填)");
  else if (!/^\S+(\s+\S+){4}$/.test(schedule)) error("$.schedule", "invalid_cron", `cron 非 5 段:${schedule}`);
  if (!lines.includes("sources:")) error("$.sources", "invalid_params", "缺 sources");
  const sourceName = valueOf("  - name: ");
  if (sourceName === null || sourceName === "") error("$.sources[0].name", "invalid_name", "缺源 name");
  const url = valueOf("    url: ");
  if (url === null || url === "") error("$.sources[0].url", "invalid_url", "缺 url");
  else if (!/^https?:\/\/\S+$/.test(url) || !looksLikeHttpUrl(url)) error("$.sources[0].url", "invalid_url", `url 非 http(s):${url}`);
  if (valueOf("    engine: ") !== "static_html") error("$.sources[0].engine", "invalid_engine", "engine 应为 static_html");
  if (valueOf("    method: ") !== "GET") error("$.sources[0].method", "invalid_params", "method 应为 GET");

  const hasLine = (prefix: string): boolean => lines.some((line) => line.startsWith(prefix));
  if (hasLine("    headers:")) {
    const ua = valueOf("      User-Agent: ");
    if (ua === null || ua === "") error("$.sources[0].headers", "invalid_params", "headers 节缺 User-Agent");
  }
  if (hasLine("    pagination:")) {
    const mode = valueOf("      mode: ");
    if (mode !== "template" && mode !== "selector") {
      error("$.sources[0].pagination.mode", "invalid_params", `mode 非法:${mode}`);
    } else if (mode === "selector") {
      const selector = valueOf("      selector: ");
      if (selector === null || selector === "") {
        error("$.sources[0].pagination.selector", "missing_pagination_selector", "selector 模式缺 selector(schema.py:665-672)");
      }
    }
    const maxPagesRaw = valueOf("      max_pages: ");
    const maxPages = Number(maxPagesRaw);
    if (maxPagesRaw === null || !Number.isInteger(maxPages) || maxPages < 1 || maxPages > 10000) {
      error("$.sources[0].pagination.max_pages", "invalid_params", `max_pages 越界(schema.py:661 ge=1 le=10000):${maxPagesRaw}`);
    }
  }

  if (hasLine("    extract:")) {
    if (valueOf("      type: ") !== "list") error("$.sources[0].extract.type", "invalid_params", "type 应为 list");
    const item = valueOf("      item: ");
    if (item === null || item === "") error("$.sources[0].extract.item", "missing_extract_item", "缺 item(schema.py:740-747)");
    const fieldEntries = lines
      .filter((line) => /^ {8}[^ ].*:/.test(line))
      .map((line) => {
        const colonAt = line.indexOf(":");
        return [line.slice(8, colonAt).trim(), unquote(line.slice(colonAt + 1).trim())] as const;
      });
    if (fieldEntries.length === 0) error("$.sources[0].extract.fields", "invalid_params", "fields 至少 1 项(schema.py:727)");
    if (!fieldEntries.some(([key]) => key === "url")) {
      error("$.sources[0].extract.fields", "missing_url_field", "fields 必含 url(schema.py:789-795)");
    }
    for (const [key, value] of fieldEntries) {
      if (value === "") error(`$.sources[0].extract.fields.${key}`, "invalid_params", "字段选择器为空");
    }
  } else {
    error("$.sources[0].extract", "missing_extract_item", "向导产物必有 extract");
  }

  return { valid: findings.every((finding) => finding.level !== "error"), findings };
}

describe("build-category-yaml:validate 契约", () => {
  beforeEach(() => {
    mocks.invoke.mockReset();
    mocks.invoke.mockImplementation(async (_command: string, args: { method: string; params?: unknown }) => {
      if (args.method !== "yaml.validate") {
        throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
      }
      const { content } = args.params as { content: string };
      return contractValidate(content);
    });
  });

  it("三组表单态产物过契约桩(valid=true,零 findings),且经真实 validateYaml 通道", async () => {
    for (const fixture of [FORM_A, FORM_B, FORM_C]) {
      const content = buildCategoryYaml(fixture);
      const result = await validateYaml(content, null);
      expect(result.findings).toEqual([]);
      expect(result.valid).toBe(true);
    }
    // 通道断言:走的是 yaml.validate 干跑(params.file=null,PRD R2 第 4 步钉序①)
    const call = mocks.invoke.mock.calls.at(-1)?.[1] as { method: string; params: unknown };
    expect(call.method).toBe("yaml.validate");
    expect(call.params).toMatchObject({ file: null });
  });

  it("负例:桩不是恒真 —— 缺 url 字段 / 坏裸键 / 未闭合引号各自报 error", async () => {
    const noUrl = buildCategoryYaml(FORM_A).replace('        url: "h3 a@href"\n', "");
    const resultNoUrl = await validateYaml(noUrl, null);
    expect(resultNoUrl.valid).toBe(false);
    expect(resultNoUrl.findings.some((finding) => finding.code === "missing_url_field")).toBe(true);

    const badKey = buildCategoryYaml(FORM_A).replace("        title:", "        my field:");
    const resultBadKey = await validateYaml(badKey, null);
    expect(resultBadKey.valid).toBe(false);
    expect(resultBadKey.findings.some((finding) => finding.code === "yaml_syntax")).toBe(true);

    const brokenQuote = buildCategoryYaml(FORM_C).replace(/name: ".*"/, 'name: "未闭合');
    const resultQuote = await validateYaml(brokenQuote, null);
    expect(resultQuote.valid).toBe(false);
    expect(resultQuote.findings.some((finding) => finding.code === "yaml_syntax")).toBe(true);
  });
});
