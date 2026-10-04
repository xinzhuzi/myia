# 钥匙串凭据名探测零弹窗(macOS 授权框消扰)

## Goal

打开消息屏(及设置屏凭据区、CLI `myssia secret list`)时,凭据名探测**零授权
弹窗**——macOS 上不再因「读数据」路径触发系统钥匙串授权框;凭据**值**的
读取授权语义保持不变。

## 背景与证据(2026-10-05 主人报障,当轮全量探查)

- 现象:装机版 app 打开消息屏,macOS 弹「"myssia-core"想要使用您钥匙串中
  的信息」要求输登录密码。
- 触发链:消息屏挂载 → `secret.list`(平台卡 已连接/需要设置 判定信号,
  `messaging/api.ts:522` → `entry.py:1070`)→ `list_secrets()` 读
  ①`__index__` 索引项 JSON 数据 + ②逐项 `get_password` 存在性核对
  (`secrets.py:345-371`)——两步都是**数据读取**,对不在条目 ACL 里的
  二进制,macOS 必弹授权框。
- 为什么现在才弹:本机钥匙链两条凭据(`myia/image/api_key`、
  `myia/llm/base_url`)系 10-03 看图线经**开发链路 python** 写入(ACL 归
  .venv 二进制);装机版 myssia-core 此前从未真正读过它们;消息屏历次
  目验走 dev 侧(有权限),装机版今天首开消息屏+钥匙链恰有这俩项。
- 实测定向:macOS 元数据查询(attributes-only)不触发授权——
  `security find-generic-password`(不带 `-w`)与 `security dump-keychain`
  均零弹窗(本机 login 钥匙串 186 条、svce=myia 恰 3 条,当轮实跑验证);
  授权框只作用于**数据读取**。被拒绝的读取不被系统记忆,拒绝后每次开屏
  重复弹(实际拒绝也不挡屏:`messaging-screen.tsx:128` catch 降级空名单)。

## Requirements

- R1:`list_secrets` 在 macOS 系统缺省路径上改走 attributes-only 枚举
  (`security dump-keychain` 元数据过滤 service=myia 的条目 account),
  枚举全程零凭据数据读取。
- R2:枚举结果的名单纪律:剔除 `__index__`、过 `_SECRET_NAME_RE` 校验、
  去重排序——与既有契约(「只有名字、按序」)完全一致。
- R3:回落:非 darwin / security CLI 不可用 / dump 非零退出 / 超时,回落
  既有「索引+逐项存在性」路径,行为与现状零差异(回落路径可能弹窗属
  平台既有限制,如实接受)。
- R4:注入 backend(测试/显式选择)时**永不**走枚举路径——既有
  InMemory 测试套零漂移。
- R5:凭据值读取(`get_secret`/`resolve_keychain_ref`)与写入/删除的授权
  语义零变化——修的是「探测」,不是「用凭据」。
- R6:装机包刷新(构建+静默换装)随本任务走,主人只做目验终裁。

## Acceptance Criteria

- [x] AC1:macOS 系统缺省路径 `list_secrets` 采用枚举结果且不触碰
  keyring(测试:monkeypatch 枚举函数返回名单,断言原样采用)。
- [x] AC2:`__index__` 与不合规名剔除、去重排序(测试覆盖)。
- [x] AC3:注入 backend 的行为与现状逐字节一致——既有测试文件零改动
  全绿。(2026-10-05:tests/test_secrets.py 55 passed+1 skipped,新增
  describe 为纯追加,既有用例零修改)
- [x] AC4:枚举不可用回落索引路径(测试:枚举返回 None → InMemory
  往返不受影响)。
- [x] AC5:`get_secret`/`set_secret`/`delete_secret` 零改动(diff 证明:
  变更面仅 list_secrets 分支+枚举函数+模块 docstring+正则常量)。
- [x] AC6:`pytest tests/test_secrets.py` 全绿 + ruff 绿;
  `gitnexus detect-changes --scope staged` 面净;零协议变更
  (`secret.list` 应答形状不变)。(真机另验:枚举结果与旧路径逐字节
  一致,`list_secrets()` 安静返回同两条名)
- [x] AC7:装机换装后装机版打开消息屏零授权弹窗(装机链回执留档;
  终裁=主人目验)。(2026-10-05 01:09 换装 732b424 构建,备份
  /tmp/世事.app.bak-ks-010926,/tmp/ks-install.exit=ok installed;
  **装机版 myssia-core 实跑 `secret list` 安静返回两条名 exit=0 零授权框
  ——若走旧读数据路径,未授权二进制必弹**;GUI 开屏零弹窗终裁=主人
  重开 app 目验)

## Constraints

- 不改 sidecar 协议(secret.list 方法与应答形状不变);不动前端。
- 枚举范围=默认钥匙串(dump-keychain 无参口径);跨钥匙串条目属罕见
  配置,如实接受并在 docstring 注明。
- 不 push(推送归主人);提交按 path 白名单与并行会话分离。

## Notes

- 主人 2026-10-05 报障「打开消息为什么需要输入密码?这不对吧」+ 批
  「立项修(推荐)」。
- 值读取的授权框(真用凭据时 macOS 问一次、始终允许即终)是正确安全
  行为,不在本任务消扰范围;若主人希望装机版对 vision 线两条凭据静默,
  授权一次「始终允许」即可,不改代码。
- 技术方案与取舍见 design.md。

## r2 回归修复补记(2026-10-05,主人令「修」)

- **缺陷**:R4 承诺「注入 backend 时永不走枚举路径」在 macOS 上被违背——`list_secrets()` 的枚举短路(`secrets.py` `_dump_macos_service_accounts`)发生在注入检查之前,`set_backend()` 全局注入(桌面/CLI 测试的实际通道)被整体绕过,真钥匙串名单漏进无参调用。AC3 的「注入行为逐字节一致」验证在 Linux CI 完成,darwin 枚举分支为零覆盖;暴露条件 = macOS + 钥匙串存有真实 `myia/*` 凭据(本机 2026-10-05 新增 image/llm 两条后全量 2 红:`test_set_list_delete_roundtrip` / `test_human_mode_secret_list`)。既有测试 `test_dump_never_consulted_when_backend_injected` 只测显式传参通道,注入通道无测试——两者一并补齐。
- **修法**:`_backend_injected` 标记区分「主动注入」与「懒发现缓存」,枚举前置条件改为 `backend is None and not _backend_injected`;懒缓存不算注入,系统缺省路径(枚举+自愈)行为不变。新增回归 `test_dump_never_consulted_when_set_backend_injected`。影响面 gitnexus impact LOW(单调用方 `cli.py:_cmd_secret`)。
- **验证**:定向 `tests/test_secrets.py + tests/cli/test_cli_full.py` 98 passed(含原两红转绿);全量因并行会话在途半成品(cli.py `_add_harvester_parser` 未定义)暂不可跑,以提交后净室 worktree 全量为准——结果见下行补记。
