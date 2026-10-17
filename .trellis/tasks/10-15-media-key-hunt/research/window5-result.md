# 2026-10-16 凌晨:钥到手(四窗授权链,第 4 窗命中)

授权与形态:四窗均主人明示「开」(目标微信/取媒体钥/前台单次限时纯读);
窗 1=解引用链误(读到隔壁全局字符串,反证地址模型对);窗 2=收尾输出目录
bug 数据随进程亡;窗 3=指针阈值过严(本机堆址 1e10 量级,阈值误设 1e12)
断链但拿到 svc 指针;窗 4=修正后全中。每窗 3.5-4.8 秒,detach-first,微信
全程零伤(重启均另一会话注入实验所致,崩溃帧归因在案)。

## 命中链(全实证)

svc_dat(0xa45df38 指针变量)= 0x0bb6932300 → 服务对象 vtable=0x132ec2400
(= slide 0x129030000 + 0x9e92400,**精确命中**)= keyobj 0xbb6bed418 →
+0x228 std::string{ptr,size=32,cap} → 掩码串 32B → XOR 已知 32B 掩码 →
**b8fd713023a5e467845dbe6b73328cd1**(32 hex);AES-128-ECB 钥 = 前 16 ASCII
`b8fd713023a5e467`(hex 解码形态实证为错路:同钥解出垃圾首字节)。

## oracle 与终验

- /tmp/wximg 5 样本:1 PNG + 4 wxgf(实况容器,合法产物)——5/5 解密正确。
- 近 60 dat 扫描 6 张可看 jpg;**三图终验 PASS**(180x102/210x210 JFIF,
  /tmp/wx-decrypt-test{1,2,3}.jpg 留验)。
- 供钥:钥匙串 myia/wechat/media-keys(16-ASCII 形态,security -i 内联)+
  数据根 media-keys.json(600)双通道;回读验真过。
- 桥级接线:media-decrypt set → `localdb media decrypt` 全链通,产物原子落
  media-cache(magic 校验门实测拦错形态钥一次,验后放行)。

## 未了(交主人)

- feed 3 级真图展示链(按裁决「接内置默认通道」/UI 消费面)未动——当前
  形态 = 外置解密件通道(协议 v1 原设计)已全通,UI 链另立。
