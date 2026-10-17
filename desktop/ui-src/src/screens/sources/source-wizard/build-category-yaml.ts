/**
 * 建源向导纯逻辑模块(表单模型 + 分步校验 + YAML 生成;无 IO、无 React,
 * 可直接单测)。PRD:.trellis/tasks/10-14-visual-source-builder(prd.md R2/R3)。
 *
 * 生成器契约:
 * - 产物 = 最小合法模板(desktop/entry.py `_CATEGORY_TEMPLATE`)的严格超集,
 *   覆盖「列表页 + 字段 + 翻页三件套 + 可选 push 单条目」:generatePush 勾选
 *   时在文末追加最小 feishu_card 单条(与 config/ai-news.yaml:473-475 的
 *   push 节同构);watchlist/classify 等其余下游段全不生成(schema 有
 *   default_factory,src/myssia/schema.py:1797-1802)。
 * - 字符串值一律双引号;引号内对 `\` 与 `"` 做 YAML 双引号转义(设计拷问修正①:
 *   品类名自由中文可含 ",CSS 选择器(DevTools Copy selector)常产
 *   `div[data-id="x"]`;不转义即语法坏或语义漂,后端只会报莫名的
 *   category_invalid)。选择在生成器转义而不是输入层拒绝:选择器带引号是
 *   正常形态,拒掉会把用户推向手写 YAML。
 * - 字段名裸作 YAML 键:输入层约束 `^[A-Za-z][A-Za-z0-9_-]*$`(设计拷问修正②:
 *   空格/冒号/`true`/纯数字做裸键会坏解析或改类型;约束在 stepErrors 第 3 步拦,
 *   生成器对空名行防御性跳过)。
 * - 翻页 template/selector 两模式都出 max_pages 输入,缺省 5(设计拷问修正③:
 *   schema.py:661 max_pages 缺省=1,不出即「选择被静默架空只抓 1 页」)。
 * - 品类名/源名长度 ≤64(schema.py:318 ShortStr 亲读;stepErrors 第 1/2 步拦)。
 *
 * 后端终门锚点(前端只做预检,两处语义一致):
 * - 品类 id 正则:src/myssia/schema.py:368 `^[a-z0-9][a-z0-9_-]{0,63}$`
 *   (TS 镜像 = screens/yaml-editor/api.ts CATEGORY_ID_PATTERN,同一常量语义)。
 * - url 必须 http(s):schema.py:850-856(invalid_url)。
 * - fields 必含 url:schema.py:789-795(missing_url_field)。
 * - list 必有 item:schema.py:740-747(missing_extract_item)。
 * - schedule 必填、cron 由 CronTrigger.from_crontab 终门:schema.py:1794、
 *   schema.py:1859-1866(invalid_cron)。
 * - pagination:mode selector 必带 selector、max_pages 1-10000:schema.py:655-675。
 */

// ---------------------------------------------------------------------------
// 表单模型(五步向导的单一真相;表单态只驻内存,落盘真相只有 YAML 本身)
// ---------------------------------------------------------------------------

/** gpu-prices 同款 Chrome UA 串(config/gpu-prices.yaml:17,预填;留空 = 不生成 headers 节) */
export const DEFAULT_USER_AGENT =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36";

/** 抓取频率预设(cron 原文即 value;PRD R2 第 1 步) */
export const SCHEDULE_PRESETS: ReadonlyArray<{ value: string; label: string }> = [
  { value: "0 10 * * *", label: "每天一次(上午 10 点)" },
  { value: "0 * * * *", label: "每小时一次" },
  { value: "0 */6 * * *", label: "每 6 小时" },
  { value: "0 9 * * 1", label: "每周一上午 9 点" },
];

/** 下拉「自定义」哨兵值(选中后出 cron 五段输入框) */
export const SCHEDULE_CUSTOM = "__custom__";

/** 字段表一行:字段名 + CSS 选择器;url 行可勾「取链接地址」自动追加 @href */
export interface WizardFieldRow {
  name: string;
  selector: string;
  /** 勾选 = 选择器追加 @href(gpu-prices.yaml:25-27 `h3 a@href` 同构;已带则不重复追加) */
  useHref: boolean;
}

/** 翻页三态:不翻页不出 pagination 节;两种翻页都带 max_pages(修正③) */
export type WizardPagination =
  | { mode: "none" }
  | { mode: "template"; maxPages: number }
  | { mode: "selector"; selector: string; maxPages: number };

/** 五步向导的完整表单态 */
export interface WizardForm {
  /** 第 1 步:品类 id(= YAML id: 与文件 stem,一处输入两处用途) */
  categoryId: string;
  /** 第 1 步:品类名(中文自由填) */
  categoryName: string;
  /** 第 1 步:预设 cron 原文或 SCHEDULE_CUSTOM 哨兵(空 = 未选) */
  schedulePreset: string;
  /** 第 1 步:自定义 cron 五段表达式(schedulePreset=SCHEDULE_CUSTOM 时生效) */
  scheduleCustom: string;
  /** 第 2 步:源名(默认 main) */
  sourceName: string;
  /** 第 2 步:页面地址 */
  url: string;
  /** 第 2 步:浏览器标识(预填 DEFAULT_USER_AGENT;清空 = 不生成 headers 节) */
  userAgent: string;
  /** 第 2 步:翻页 */
  pagination: WizardPagination;
  /** 第 3 步:列表整条的选择器 */
  itemSelector: string;
  /** 第 3 步:字段表(预置 title/url 两行) */
  fields: WizardFieldRow[];
  /** 第 4 步:同时生成推送(默认勾;勾 = 产物文末追加最小 push 单条目) */
  generatePush: boolean;
}

/** 初始表单(向导 dirty 判定的对照基线;默认值也是预填值) */
export function initialWizardForm(): WizardForm {
  return {
    categoryId: "",
    categoryName: "",
    schedulePreset: "",
    scheduleCustom: "",
    sourceName: "main",
    url: "",
    userAgent: DEFAULT_USER_AGENT,
    pagination: { mode: "none" },
    itemSelector: "",
    fields: [
      { name: "title", selector: "", useHref: false },
      { name: "url", selector: "", useHref: true },
    ],
    generatePush: true,
  };
}

/** 解析生效的 cron 串(预设原文或自定义输入;trim 后空串 = 未填) */
export function resolveScheduleCron(form: WizardForm): string {
  return form.schedulePreset === SCHEDULE_CUSTOM ? form.scheduleCustom.trim() : form.schedulePreset;
}

// ---------------------------------------------------------------------------
// 分步校验(纯函数;返回人话错误行,空数组 = 本步可进下一步)
// ---------------------------------------------------------------------------

/** 字段名字符集(裸 YAML 键安全集;修正②) */
export const FIELD_NAME_RE = /^[A-Za-z][A-Za-z0-9_-]*$/;

/** url 前端预检镜像(schema.py:850-856 的 urlparse 门:scheme http(s) + host 非空) */
export function looksLikeHttpUrl(value: string): boolean {
  try {
    const parsed = new URL(value);
    return (parsed.protocol === "http:" || parsed.protocol === "https:") && parsed.host !== "";
  } catch {
    return false;
  }
}

/** cron 五段形状预检(分 时 日 月 周;终门 = CronTrigger.from_crontab,schema.py:1859-1866) */
export function looksLikeCrontab(value: string): boolean {
  return /^\S+(\s+\S+){4}$/.test(value);
}

/** max_pages 合法区间(schema.py:661 ge=1 le=10000) */
export function isValidMaxPages(value: number): boolean {
  return Number.isInteger(value) && value >= 1 && value <= 10000;
}

/** 表单是否与初始态一致(JSON 逐字段对照;向导 dirty 守卫的基线) */
export function isPristineForm(form: WizardForm): boolean {
  return JSON.stringify(form) === JSON.stringify(initialWizardForm());
}

/**
 * 分步校验:给定步号(1-5)返回人话错误行。第 4/5 步无表单门(第 4 步的钉序
 * 校验走真实 yaml.validate 干跑,见 use-source-wizard.ts)。
 */
export function wizardStepErrors(form: WizardForm, step: 1 | 2 | 3 | 4 | 5): string[] {
  const errors: string[] = [];
  if (step === 1) {
    const id = form.categoryId.trim();
    if (id === "") {
      errors.push("品类 id 还没填(小写字母/数字/-/_,也是文件名)");
    } else if (!/^[a-z0-9][a-z0-9_-]{0,63}$/.test(id)) {
      errors.push(
        "品类 id 只能用小写字母/数字/-/_,以字母或数字开头,1-64 字符;中文名放「品类名」",
      );
    }
    const name = form.categoryName.trim();
    if (name === "") {
      errors.push("品类名还没填(中文随意,显示用)");
    } else if (name.length > 64) {
      errors.push("品类名太长了(最多 64 个字符)");
    }
    if (form.schedulePreset === "") {
      errors.push("抓取频率还没选(多久自动抓一次)");
    } else if (form.schedulePreset === SCHEDULE_CUSTOM) {
      const cron = form.scheduleCustom.trim();
      if (cron === "") {
        errors.push("自定义频率还没填(5 段:分 时 日 月 周,如 0 9 * * *)");
      } else if (!looksLikeCrontab(cron)) {
        errors.push("自定义频率要填 5 段 cron(分 时 日 月 周,空格隔开),如 0 9 * * *");
      }
    }
  } else if (step === 2) {
    const sourceName = form.sourceName.trim();
    if (sourceName === "") {
      errors.push("源名还没填(默认 main 就能用)");
    } else if (sourceName.length > 64) {
      errors.push("源名太长了(最多 64 个字符)");
    }
    const url = form.url.trim();
    if (url === "") {
      errors.push("页面地址还没填(要 http:// 或 https:// 开头)");
    } else if (!looksLikeHttpUrl(url)) {
      errors.push("页面地址要填 http:// 或 https:// 开头的完整网址");
    }
    if (form.pagination.mode === "template") {
      if (!url.includes("{page}")) {
        errors.push('选了「网址带页码」翻页,页面地址里要有 {page} 占位(抓的时候会依次换成页码)');
      }
      if (!isValidMaxPages(form.pagination.maxPages)) {
        errors.push("最多翻几页要填 1-10000 的整数");
      }
    } else if (form.pagination.mode === "selector") {
      if (form.pagination.selector.trim() === "") {
        errors.push("「下一页」按钮的 CSS 选择器还没填");
      }
      if (!isValidMaxPages(form.pagination.maxPages)) {
        errors.push("最多翻几页要填 1-10000 的整数");
      }
    }
  } else if (step === 3) {
    if (form.itemSelector.trim() === "") {
      errors.push("列表整条的选择器还没填(先框住页面上重复的整条,比如一行商品)");
    }
    const rows = form.fields.filter((row) => row.name.trim() !== "");
    if (rows.length === 0) {
      errors.push("至少要有一个字段(比如标题 title、链接 url)");
    }
    if (!rows.some((row) => row.name === "url")) {
      errors.push("字段里必须有 url(每条内容的链接;没有它配置装不上)");
    }
    const seen = new Set<string>();
    for (const row of rows) {
      const name = row.name.trim();
      if (!FIELD_NAME_RE.test(name)) {
        errors.push(`字段名「${name}」不合规:只能英文字母开头,后接字母/数字/_/-`);
      }
      if (seen.has(name)) {
        errors.push(`字段名「${name}」重复了`);
      }
      seen.add(name);
      if (row.selector.trim() === "") {
        errors.push(`字段「${name}」的选择器还没填(不需要的字段可以删掉这行)`);
      }
    }
  }
  return errors;
}

// ---------------------------------------------------------------------------
// YAML 生成器(纯函数;产物逐字节钉死,由 build-category-yaml.test.ts 锁定)
// ---------------------------------------------------------------------------

/**
 * YAML 双引号标量转义:先 `\` 后 `"`(顺序保证不二次转义自身引入的反斜杠),
 * 换行/回车归一为 `\n` 转义(双引号标量里的裸换行会被 YAML 折叠成空格,
 * 悄悄改语义;单行输入框正常到不了这里,防御性兜底)。
 */
export function yamlQuote(value: string): string {
  const escaped = value
    .replace(/\\/g, "\\\\")
    .replace(/"/g, '\\"')
    .replace(/[\r\n]+/g, "\\n");
  return `"${escaped}"`;
}

/** 字段行值:勾了取链接地址 → 追加 @href(已带 @href 结尾则不重复追加) */
export function fieldSelectorValue(row: WizardFieldRow): string {
  const selector = row.selector.trim();
  if (!row.useHref || selector.endsWith("@href")) return selector;
  return `${selector}@href`;
}

/**
 * 表单态 → 品类 YAML 文本。缩进/引号风格与 config/gpu-prices.yaml 对齐;
 * id 裸写(正则锁定字符集),其余字符串值一律 yamlQuote。空字段名行防御性
 * 跳过(第 3 步校验已拦,此处兜底防生成坏键)。timezone 不生成(缺省走本地)。
 */
export function buildCategoryYaml(form: WizardForm): string {
  const lines: string[] = [
    "# 由建源向导生成:普通网页列表采集(每天到点抓一页/几页,提取列表字段)。",
    "# 覆盖「列表页 + 字段 + 翻页」三件套 + 可选 push 单条目(飞书卡片);关键词过滤、分类等进「YAML配置」补全。",
    `id: ${form.categoryId.trim()}`,
    `name: ${yamlQuote(form.categoryName.trim())}`,
    `schedule: ${yamlQuote(resolveScheduleCron(form))}`,
    "sources:",
    `  - name: ${yamlQuote(form.sourceName.trim())}`,
    "    engine: static_html",
    `    url: ${yamlQuote(form.url.trim())}`,
    "    method: GET",
  ];

  const userAgent = form.userAgent.trim();
  if (userAgent !== "") {
    lines.push("    headers:              # 浏览器标识;不需要可整节删掉");
    lines.push(`      User-Agent: ${yamlQuote(userAgent)}`);
  }

  if (form.pagination.mode === "template") {
    lines.push("    pagination:           # 翻页:网址里的 {page} 依次换成页码");
    lines.push("      mode: template");
    lines.push(`      max_pages: ${form.pagination.maxPages}`);
  } else if (form.pagination.mode === "selector") {
    lines.push("    pagination:           # 翻页:沿「下一页」链接一直抓到头");
    lines.push("      mode: selector");
    lines.push(`      selector: ${yamlQuote(form.pagination.selector.trim())}`);
    lines.push(`      max_pages: ${form.pagination.maxPages}`);
  }

  lines.push("    extract:              # 提取:item 框住重复的整条,fields 取每条里的字段");
  lines.push("      type: list");
  lines.push(`      item: ${yamlQuote(form.itemSelector.trim())}`);
  lines.push("      fields:");
  for (const row of form.fields) {
    const name = row.name.trim();
    if (name === "") continue;
    lines.push(`        ${name}: ${yamlQuote(fieldSelectorValue(row))}`);
  }

  // 可选 push 单条目(与 config/ai-news.yaml:473-475 的 push 节同构):
  // 凭据在「配置 → 机器人凭据」填、发给谁在「推送 → 消息」勾选,产物只落最小三条
  if (form.generatePush) {
    lines.push("push:                     # 推送:飞书卡片;机器人凭据到「配置 → 机器人凭据」填");
    lines.push("  - channel: feishu_card");
    lines.push("    target: env:FEISHU_CHAT_ID  # 发给谁:建好后在「推送 → 消息」勾选");
  }
  return `${lines.join("\n")}\n`;
}
