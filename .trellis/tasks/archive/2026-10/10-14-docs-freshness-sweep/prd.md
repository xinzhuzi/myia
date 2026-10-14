# 文档新鲜度刷新与遗留问题清账

## Goal

已交付功能更新进文档、旧文档清理保正确;剩余问题任务深度探究→计划→执行清账

## Requirements

- README(双语)/docs(双语)/skill/SKILL.md 对齐已交付现实:测试数、推送通道数、微信双桥、官方品类数、桌面屏数、链外引擎、extras 清单、Windows 启动行为
- schema 双语常量表补齐已交付取值(feishu 引擎、macos_notify 通道)
- spec 索引去写死计数(行数/平台数以代码对账)
- 遗留清账:ghhunt 传输层错误处理、localdb_export 成功路径 staging 残留、doctor 并行计时测的构造开销干扰

## Acceptance Criteria

- [x] 文档陈述与代码现实一致(改动见下方终局回执改动清单)
- [x] gitnexus detect-changes(staged)无 HIGH/CRITICAL
- [x] 被改两测试件通过

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.

---

## 终局回执(2026-10-14,簿记归档员)

**码提交**:`afdb52e` — `docs(sweep): 文档新鲜度刷新+遗留清账(10-14-docs-freshness-sweep)`,17 files,+220/−50。

### 改动清单(全部入 afdb52e)

文档新鲜度:
- `README.md` / `README.en.md`:徽章 5400+→6200+;推送徽标改 34 通道(weixin-local/macos_notify/bark);微信出站双桥表述(weixin 官方桥 + weixin-local 本机桥);官方品类 7→18;桌面五屏→十四屏;架构图补链外引擎(reddit/credhunter/zenrows/scraperapi/searxng)与推送行改 34 通道;文档表补 zero-cost、build-windows、微信桥三协议单册(docs/ 根 zh/en 共用);Roadmap 补 Reddit Data API 与 SearXNG 条目
- `docs/{en,zh}/schema.md`:ENGINES 补 `feishu`;PUSH_CHANNELS 补 `macos_notify`(→34)
- `docs/{en,zh}/build-windows.md`:「已知行为:静默启动」改「启动即亮窗(2026-10 起)」——`desktop/src-tauri/tauri.windows.conf.json` 覆盖件 `visible:true` + `focus:false`,`MYIA_SHOW_ON_START=1` 转历史注记;坑表第 5 行修根因表述(WebView2 起不来,与窗口显隐无关);执行记录路径改 `archive/2026-10/10-05-win-local-build/`
- `docs/{en,zh}/getting-started.md`:extras 9→12(+apprise/telethon/browser)并写明 `all` 聚合键装哪六件、与 vision 的包交集;微信通道改双路表述
- `docs/{en,zh}/write-a-plugin.md`:新增链外源引擎 `wechat_local` 四通道(pixel/localdb/sns/notify)与 weixin-notify 整机形态(白名单出厂空即拒、cron 注册后才拉取)
- `skill/SKILL.md`:新增 `wechat_local` 浓缩参考(四通道、锚前缀、不进 auto 链、隐私红线:enrich 全关/push 空或本机零网络)
- `.trellis/spec/index.md`:sidecar-protocol 条目去写死「方法注册表(23)」,改「以代码对账」
- `.trellis/spec/python/index.md`:PLATFORMS「feishu/telegram 已接入」改「28 平台全量接入;清单不写死,事实源 = push/__init__.py」

遗留清账(码):
- `plugins/myssia-credhunter/credhunter/ghhunt.py:303-315`:`_request_json` 传输层 `httpx.HTTPError` 不再换 token 空转重试,结构化上抛 `GithubHuntError("github_unreachable")`(规格 §7:单查询失败只进 errors 不打断整轮)
- `plugins/wechat-bridge/wechat_bridge/localdb_export.py:793`:成功路径补 `shutil.rmtree(staging_dir, ignore_errors=True)`(此前仅失败路径清);`shutil` 提为模块级导入
- `tests/engines/test_proxy_transport.py:689-698`:doctor 泳道并行计时测 monkeypatch `_build_async_client` 为 MockTransport 廉价构造——生产形 `AsyncClient(proxy=…)` 同步构造 30-270ms/个串行顶穿中点阈值(本测 2026-10-14 门禁红根因)
- `tests/wechat-bridge/test_localdb_export.py:189-191`:导出往返测补「成功后 staging 根零残留」断言

### 清理清单

- 无文件删除;本任务未产生临时文件
- 旧文案清除:`MYIA_SHOW_ON_START=1` 作为 Windows 正路的所有表述(改历史注记)、「五屏」「7 品类」「9 extras」「5400+」等过期计数

### 遗留处置

- 「启动即亮窗」真机 MSI 双击验证:归 windows 线,随下个 tag 的 windows-msi 产物补做(build-windows.md 双语已如实注记)
- 并行线 `.trellis/tasks/10-14-wechat-sendmsg-direct/**` 在途改动未入本提交(簿记纪律:不碰并行线)
- 全量 6200+ 测试套未在本任务本地跑,由 CI 承接(本任务只跑了被改两件,见门禁)

### 门禁(实测)

- `gitnexus detect-changes -r shishi --scope staged` → 17 files / 136 symbols / affected flows 仅 `Hunt → _request_json`、`Hunt → _rate_limit_wait`(即 ghhunt.py 本处改动,预期内),risk **medium**(非 HIGH/CRITICAL)
- `uv run pytest tests/wechat-bridge/test_localdb_export.py tests/engines/test_proxy_transport.py -q` → **61 passed in 1.89s**

### 复查结论

- `git diff --cached --name-only` 逐件核对:暂存集恰为本线 17 件,`10-14-wechat-sendmsg-direct/**` 与本任务目录零混入
- 改动与 Goal/Requirements 对得上:文档全部对齐代码现实,三件遗留清账各有测试锚定
- 归档前工作树仅剩并行线在途件 + 本任务目录,无未记录改动
