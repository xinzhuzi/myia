# README 双语状态刷新(徽章/Windows/里程碑与实现对齐)

## Goal

gen-specs-as-issues 排查产出(2026-10-12):README.md / README.en.md 的状态
声明与实现现状**反向漂移**,开源门面第一屏修正到如实。

## 缺口证据(gen-specs Phase 2,逐条实证)

1. **Windows 状态反了**(最重):README 路线图段「Windows 构建这版未通过,
   Release 暂无 Windows 安装包(后续批次计划补上)」;Windows 安装节(245-253)
   用将来时「将随 GitHub Releases 发布」。**实测**:Release v0.0.3 资产已含
   `myssia_0.0.3_x64.msi` + `.sig`(CI windows-msi 作业 10-04 首绿,run
   37186006759)。访客读到「没有 Windows 包」即流失。
2. **徽章过时**:「tests 1300+ passing」——全量实际 **5421**(5427 过/48 skip,
   10-12 实测);「status: 0.0.1 first release」——装机/发行已是 **0.0.3**。
3. **里程碑措辞过时**:「桌面卡片内反馈按钮…随下个发布版交付(反馈 CLI 已
   可用)」——反馈按钮/开关/趋势已在装机件(10-04 桌面对齐批)。
4. demo gif 为 shishi 时期物料(README 已注记时代锁定)——本档不改物料,
   仅核对注记仍准确;重录属演示物料批另议。

## Requirements

1. README.md 与 README.en.md 同步刷新:测试徽章数字、状态徽章版本、路线图
   Windows 句、里程碑表 v1.1 行措辞、Windows 安装节改陈述句(以 Releases 页
   为准的版本占位保留)。
2. 刷新时全文扫一遍其余状态声明(架构/文档节链接/致谢)防漏。
3. 徽章数字建议改为区间表述(如「5400+」)降低维护频率——待主人定夺可翻案。

## Acceptance Criteria

- [x] AC1 双语 README 的 Windows/测试数/版本/里程碑四类声明与 Releases 页
      和 CI 实况一致(逐条对照核验)。
- [x] AC2 gh api 读 Release 资产与 README 声明互证脚本化或逐条手工核验留档。

## 边界

- 纯文档批,零代码;demo gif 不动;Web UI「规划中」行保留(如实)。
- 版本数字类(状态徽章)每次发版都会漂——AC 不含「永久不过时」,只管当下如实。

## 执行手册(2026-10-12 补全,双语逐处 old→new;执行即照单)

### README.md(8 处)

| # | 行 | 现文(关键片段) | 改为 |
|---|---|---|---|
| z1 | 13 | `tests-1300%2B%20passing` / alt "1300+ passing" | `tests-5400%2B%20passing` / "5400+ passing"(区间表述,降维护频率——PRD 建议 3 采纳) |
| z2 | 16 | `status-0.0.1%20first%20release` | `status-0.0.3%20released`(alt 同步 v0.0.3) |
| z3 | 116 | 「桌面卡片内按钮已随桌面对齐批次落地 main、随下个发布版交付;」 | 「桌面卡片内按钮已交付(桌面对齐批次,已随 Releases);」 |
| z4 | 143 | `# myssia 0.0.1` | `# myssia 0.0.3` |
| z5 | 247-248 | 「安装包(msi)将随 GitHub Releases 发布——…交付前 Releases 页暂无 msi(见路线图注记):」 | 「安装包(msi)已随 GitHub Releases 交付(v0.0.3 起挂 `myssia_<版本>_x64.msi`):」 |
| z6 | 345 | 「1300+ 测试跑在 CI 里」 | 「5400+ 测试跑在 CI 里」 |
| z7 | 348-349 | 「…随下个发布版交付(反馈闭环 CLI 现已可用);Windows 构建这版未通过,Release 暂无 Windows 安装包(后续批次计划补上)。」 | 「…已随桌面对齐批次交付;Windows 安装包(msi)已随 v0.0.3 挂上 Releases(构建流水线 10-04 首绿)。」 |
| z8 | 358 | 「已随桌面对齐批次落地、随下个发布版交付(反馈 CLI 已可用)」 | 「已交付(桌面对齐批次落地,已随 Releases)」 |

### README.en.md(7 处)

| # | 行 | 现文 | 改为 |
|---|---|---|---|
| e1 | 13 | tests-1300%2B badge | tests-5400%2B |
| e2 | 16 | status-0.0.1 first release | status-0.0.3 released |
| e3 | 158 | `# myssia 0.0.1` | `# myssia 0.0.3` |
| e4 | 280-281 | "the msi installer (shipping via Releases — see the roadmap note)" | "the msi installer (shipped via Releases since v0.0.3)" |
| e5 | 368 | "1300+ tests run in CI" | "5400+ tests run in CI" |
| e6 | 371-374 | "ship with the next release (the feedback loop already works via CLI); the Windows build did not ship in this release (no Windows installer in Releases yet; planned for a follow-up batch)" | "shipped in Releases (desktop-parity batch); the Windows msi installer ships in Releases since v0.0.3" |
| e7 | 376+ | 里程碑表 v1.1 行同款 "ship with the next release" 措辞 | 已交付陈述 |

### 核验命令(AC2 落实)

- `gh api repos/xinzhuzi/myia/releases/tags/v0.0.3 --jq '.assets[].name'` → 必含 `_x64.msi` 与 README 声明互证;
- `.venv/bin/python -m pytest -q 2>&1 | tail -1` → passed 数 ≥5400;
- 改后 `rg -n "1300|0\.0\.1 first|暂无 msi|did not ship|next release" README.md README.en.md` → 零命中(或仅历史注记类)。


## 终局回执(10-12)

- 双语 16 处(zh 8 + en 8,执行手册外补抓 en 反馈卡第 8 处)全部落地;
- 核验:Release v0.0.3 资产含 `_x64.msi`+`.sig` 与新声明互证 ✓;残留扫
  (`1300/0.0.1 first/暂无/did not ship/next release`)双语清零 ✓;5400+/v0.0.3
  新声明双语在位 ✓。测试数取自 10-12 全量实跑(5427 过/48 跳),徽章用
  5400+ 区间表述(PRD 建议 3 采纳,降维护频率)。
