# 产品面深度文档:五大新特性完整文档

## Goal

微信本机工作台六屏(C1-C6)/代理池管理面板/凭证猎手面板/五步建源向导/weixin-notify 品类整机形态,写 docs/zh+en 双语深文档,mention 级升级为完整产品面文档(docs-freshness-sweep 轮建议另立,本档即其落地)。

## Requirements

- 四篇新文档(8 件):wechat-local(微信本机工作台六屏+通知线)/proxy-pool(池化后端+面板+G10)/cred-hunter(引擎+面板+红线)/source-wizard(五步向导)
- 每处功能主张带代码锚(path:line 亲读),零编造;zh/en 同结构同事实;BILINGUAL_PAGES 注册进守卫
- 文风对齐既有 docs(cron.md/write-a-plugin.md 锚);相对链接可解析;yaml 示例过真加载器

## Acceptance Criteria

- [x] AC1 八件文档交付:docs/zh+en 下 wechat-local/proxy-pool/cred-hunter/source-wizard 四篇(三文档员并行,每员自查 zh/en 对应+锚列表回执)
- [x] AC2 守卫全绿:pytest tests/test_docs.py 143 passed(三员各自跑+主会话终验;BILINGUAL_PAGES 四页全注册)
- [x] AC3 主张带锚:wechat-local 9 节(UI 六屏/sidecar 11 动作表/notify 引擎/macOS 通知/HTTP API/只读红线)、proxy-pool 5 节(fetch_base 池化 L577-1274/proxy_panel/设置屏 G10)、cred-hunter 6 节(lanes/keystore/面板 G11 三不借)、source-wizard 五步(向导五件/schema 正则锚)
- [x] AC4 双语结构对齐:标题层级/围栏数/yaml 形状守卫逐项过(测试锁定)

## 回执

主会话集成收尾:143 passed 亲验;pathspec 提交(docs 8 件+test_docs.py+本档);并行线在途件(Cargo/system-confirm/macos_notify/sendmsg 系)零混入。Reddit API 申请转待定(主人令,2026-10-14)。
