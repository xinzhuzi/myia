# 微信密钥攻坚战(磁盘路:key_info 解包+MMKV 派生)

## Goal

主人裁决 B(2026-10-13):攻坚到底不设时限,打穿自动通电 TMS 群;内存路全排除在案(四形态+chatlog 模式+时序修正+API 监听),正解=磁盘路 key_info.db 152B 加密体解包,机器密钥来源嫌疑=MMKV tinfo 设备信息派生;资产固化+四阶段路线图在档

## Requirements

- 打穿 4.1.15 取钥使 TMS 群真消息自动通电入流;路线与资产固化见 research/crack-roadmap.md(四阶段),工具资产在 research/tools/。

## Acceptance Criteria

- [x] AC1 密钥到手并全库验真:LLDB `CCKeyDerivationPBKDF $x2==32` 断点一击命中(10-13 11:22),passphrase 取得,**20/20 salts 全库验真**,keys.json 落数据根(crack-roadmap.md 终局战报 L95-107,随 975faf4 入库)。
- [x] AC2 下链闭环:桥 E2 解密副本 404MB,TMS 群 9745 条真消息实时在流;E3 查询适配(4.1.15 分表)由 keyprovider B0 收口(19c606b 0.4.2→f51d5ac 0.4.3,该档已归档);重取 SOP 固化于本档 research/tools/lldb-shot.sh。

## 收口注记(2026-10-14 档务批)

主人令「先解决后归档」档务核:prd 骨架虽为 TBD,真实验收以 crack-roadmap 阶段 4 为准——LLDB 路全胜,密钥攻坚本体完结;后续固化线(keyprovider/key-subsystem)另档在案。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
