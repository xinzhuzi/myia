# 微信 V2 媒体 AES 钥运行期截获(哨兵)+ 真图终验收口

## Goal

微信图片真图最后一块:V2 每用户 16 字节 AES 钥。算法与供钥通道均已交付
(`scripts/wechat-bridge-mediadecrypt.py` 26 测 + 钥匙串/数据根双通道),
唯缺钥本身——静态路线已猎尽(并行工作流 dwfrun-a5fa5717:全进程 ~15GB
dump 七族 oracle 零确认,结论=运行期驻留),本档走**运行期断点截获**。

## 路线(照 10-13 PBKDF 哨兵成熟打法)

`wechat.dylib` import 表实证有 `_CCCrypt/_CCCryptorCreate` → LLDB 断两入口,
回调过滤 arm64 寄存器形态(x0=kCCDecrypt + x1=AES + x2 ECB 位 + x4=16)+
对 5 个真 dat 样本(`/tmp/wximg`,已验 V2 头字节账)跑 openssl oracle
(解出 jpg/png/webp/gif 魔数才收)→ 验真落 `KEY`(600)→ 停机脱附。
假命中静默自动续跑,微信零感(实测 CPU 0.5%)。

排队纪律:微信 task port 单占——并行直发线(r20-r26)在跑则礼让,退场+
180s 静默窗后自动武装。

## 实况(10-15 晚)

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
