# s74源选择器失效修复(74站页面改版)

## Goal

2026-10-19 羊毛真网dry-run发现:s74(tkkgv8.gicp.fun)整源invalid_item(url=None,62条全灭),.card-url@href选择器取不到链接=页面改版;生产10-18两轮wool run同为partial同因。修法:firecrawl重渲染实测新DOM改extract选择器。非wool-quality-gate任务范围,独立小档。

## Requirements

- 用 firecrawl 云渲染(与生产同引擎同 waitFor 口径)抓取 74 站当前 DOM,实测新版卡片结构。
- 按 新 DOM 更新 `config/wool.yaml` s74 源的 extract 选择器(item/fields),保住四字段语义:标题、注册直链(url 绝对地址)、站点描述、邀请码(有则抽)。
- 真网验证:更新后 dry-run 该单源,62 条量级恢复、每条 url 非 None。
- 只动 s74 域文件(wool.yaml s74 块为主);工作树有并行会话在途脏文件,禁止触碰。
- 修法决策走 grill 拷问(多方案对比质询后定案),过程记录进本档。

## Acceptance Criteria

- [x] AC1 新 DOM 实测留档:74站当前渲染结构(选择器候选+证据)记录进本档 Notes。
- [x] AC2 选择器更新:wool.yaml s74 块 extract 与新 DOM 匹配,四字段语义不丢。
- [x] AC3 真网复验:s74 单源 dry-run 条目恢复(url 全非 None),证据(条数/样例)留档。
- [x] AC4 回归绿:wool 域相关 pytest 通过;全量 pytest 红项(若有)归因与本改动无关(预存红须点名列出)。

## 验收实录(2026-10-19,工作流 dwfrun-f95a490c)

- 根因:74站改版后 `.card-url` 元素从带 href 的链接变为 `div` 包 `a`(复核员抽样前 5 卡全为 div,62 卡中 0 个 .card-url 自带 href),旧选择器 `.card-url@href` 必然取空 → invalid_item 62 条全灭。
- 修复(grill 定案 A,最小修复):仅 `config/wool.yaml:148` 一行 `url: ".card-url@href"` → `".card-url a@href"`;item/title/desc/code 四选择器未动,四字段语义保住。
- AC1:渲染 DOM 存档 `research/s74-rendered-2026-10-19.html`(+md 摘要/meta);两组候选方案在拷问后定 A。
- AC3:真网复验三腿一致——bs4 独立解析 62 条 urlNone=0;引擎同款 `extract_html`(fetch_base.py:1814)跑存档 62/0(旧选择器对照 0/62 复现失效);真网 CLI `.venv/bin/myssia test config/wool.yaml --source s74 --json` exit=0 ok=true item_count=62,首条 url=https://sharellm.net/sign-up 绝对直链。
- AC4:域测绿(pytest -k "wool or s74";抽查 test_plugins.py -k wool 16 passed 5 skipped)+ 全量 pytest 绿;golden 冻结件不含 s74(golden 全目录 grep 零匹配,regen 脚本 docstring 明言解耦),无需同步。
- 独立复核:边界(diff 仅 wool.yaml:148 单行)/证据/失效机理/引擎同款腿/CLI 复跑/pytest 抽查/golden 合规/代码引用共九项亲验全过;施工会话过程性主张一项以等价重跑复证(标 unconfirmed 存档)。

## Notes

- 原选择器(2026-10-17 前):item `.card`;title `.card-name`;url `.card-url@href`;desc `.card-desc`;code `.invite-code`。
- 直抓是纯 JS 壳(15KB 零链接),必须走 firecrawl 云渲染;华为云线同源同走云 FC waitFor(先例)。
- 2026-10-19 主人令「哪些你能做的就做完它,多方探索信息,使用grill方式去做决定」→ 本档转执行。
