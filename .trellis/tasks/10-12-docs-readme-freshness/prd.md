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

- [ ] AC1 双语 README 的 Windows/测试数/版本/里程碑四类声明与 Releases 页
      和 CI 实况一致(逐条对照核验)。
- [ ] AC2 gh api 读 Release 资产与 README 声明互证脚本化或逐条手工核验留档。

## 边界

- 纯文档批,零代码;demo gif 不动;Web UI「规划中」行保留(如实)。
- 版本数字类(状态徽章)每次发版都会漂——AC 不含「永久不过时」,只管当下如实。
