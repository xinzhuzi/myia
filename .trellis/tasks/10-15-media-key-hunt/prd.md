# 微信 V2 媒体 AES 钥运行期截获(哨兵)+ 真图终验收口

## 当前执行约束（2026-10-15 接手复验）

用户因微信实际卡顿已禁止后台哨兵、循环附加与失败自动重试。下述哨兵路线仅作历史记录，不可照单执行。活进程附加须由用户明确授权本次目标、用途和最长时限，仅可前台、单次、限时执行；须先建立超时/取消/失败清理，并在结束后验证微信仍运行且无调试附加。`/tmp/wx_media_key_sentinel/launch.sh` 与本档 `research/sentinel/launch.sh` 均已封禁，禁止恢复或绕过。

本次接手范围为媒体钥与真图解密收口；spawner/uicreate 是直发支线，不混入本任务。用户随后在本聊天回复“确认”，明确授权一次前台微信媒体取钥窗口，最长 30 秒；清理验证通过后才执行，失败/超时不重试，窗口结束授权即消费。最新证据见 `research/takeover-20261015.md`；本次方案见 `design.md` 与 `implement.md`。本任务功能验收仍未完成。

## Goal

2026-10-15 续做切片：用户要求选择可独立推进的未完成项直接做。本轮补离线三样本验收工具，复用现有供钥读取与解密算法，拒绝重复样本和仅魔数成功的坏图；无钥明确阻塞。此切片不重新附加、不写凭据、不安装，也不代表下述真实媒体验收已完成。

微信图片真图最后一块:V2 每用户 16 字节 AES 钥。算法与供钥通道均已交付
(`scripts/wechat-bridge-mediadecrypt.py` 26 测 + 钥匙串/数据根双通道),
唯缺钥本身——静态路线已猎尽(并行工作流 dwfrun-a5fa5717:全进程 ~15GB
dump 七族 oracle 零确认,结论=运行期驻留),本档走**运行期断点截获**。

## 路线(照 10-13 PBKDF 哨兵成熟打法)

`wechat.dylib` import 表实证有 `_CCCrypt/_CCCryptorCreate` → LLDB 断两入口,
回调过滤 arm64 寄存器形态(x0=kCCDecrypt + x1=AES + x2 ECB 位 + x4=16)+
对 5 个真 dat 样本(`/tmp/wximg`,已验 V2 头字节账)跑 openssl oracle
(解出 jpg/png/webp/gif 魔数才收)→ 验真落 `KEY`(600)→ 停机脱附。
历史回调在假命中后自动续跑，但每次断点均会暂停微信；实际已造成严重卡顿，原“微信零感”的判断撤回。

历史排队方案已废止：禁止等待静默窗后自动武装，禁止退出后自动重挂。

## 历史实况(以下武装状态已失效)

- 哨兵已武装挂在微信(修正版回调);首轮 r0 撞 LLDB 断点命令返回语义反
  写 bug(返回真=停机,被滤命中即误停)已修正——**on_hit 返回 False=续跑**。
- 唤醒条件:任意图片渲染(聊天图/朋友圈);主人点一张图即可。
- 兜底:若点图后 CCCrypt 无 16B-ECB 形态命中 = 图片解密不走系统库 →
  转 Ghidra 深挖 `wechat.dylib` 内解密函数(资产 ~/Downloads/微信反编译/
  ghidra-wxhunt 在位,playbook spec/guides/wechat-reverse-playbook.md)。

## 钥到手后的收口链(承 selfkey 档)

供钥(钥匙串 myia/wechat/media-keys,security -i 内联防 128B 截断)→
`scripts/wechat-bridge-mediadecrypt.py` 真图终验(≥3 样本 magic 全过)→
按主人裁决接内置默认通道 → 打包装机。

## Acceptance Criteria

- [ ] KEY 验真落袋(oracle 三样本以上通过)
- [ ] 真图终验:解密件对真 dat 产出可看图(magic 校验过)
- [ ] 供钥双通道写入 + key-status 可查
- [ ] 打包覆盖安装 + 主人真机点图终验

## 资产(已固化入档,纪律§6)

research/sentinel/{cap.py, launch.sh, run.cmd};oracle 样本 /tmp/wximg/
5 件(V2 头已验);分析记录 /tmp/{scan_key,brute_key}.py(假阳性路线存照)。
