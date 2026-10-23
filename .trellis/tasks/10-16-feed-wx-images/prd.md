# 情报流 3 级聊天工作台直接渲染微信消息真图

## Goal

主人令(2026-10-16 凌晨):微信消息图片在情报流 3 级聊天工作台直接渲染。
前置已闭环(10-15-media-key-hunt):钥入库(钥匙串 16-ASCII 形态)、解密件
全链通(`localdb media decrypt` → media-cache 原子落图)、外置件通道接线。
本档 = UI 消费面:消息 → 媒体引用 → 解密/服务 → 气泡内 <img> 渲染。

## 已知弹药(承 media-key-hunt window5-result.md)

- 解密:`scripts/wechat-bridge-mediadecrypt.py`(协议 v1,系统 python3+openssl
  即可跑);桥 `localdb media decrypt <dat>` 全链通;`media.py scan_chat_media`
  已有 R2 寻径(local_type 3=图:packed_info_data 32-hex key → msg/attach/
  <dir>/<yyyy-mm>/Img/<key>[_t].dat,缩略图优先;43=视频明文)。
- 缓存:数据根 wechat-localdb/media-cache/(600/700,LRU 容量治理)。
- httpapi 有媒体下发面(R7:allowlist 目录 http-media)——与 media-cache 的
  关系待探(C6 注记说 media-cache 是指定读取落点,两目录名不一致需核)。
- UI:3 级聊天工作台(TG/微信同构双栏;气泡 data-item-key=dedup_key)。

## 待探(研究先行)

1. 微信消息怎么变成 feed 条目(localdb page/export → 何引擎消费 → store)?
   条目现在带不带媒体信息(dat key/类型)?
2. 图片怎么到 webview:桥 HTTP(httpapi+token)直连 / Tauri asset 协议 /
   sidecar IPC 转发 base64,选型(装机件约束:assetProtocol scope 现状)。
3. 3 级气泡渲染点(we Chat 消息当前渲染什么形态;TG 图怎么处理——TG 线
   是否已有图片渲染可复用)。
4. 撞面:并行会话在途的 localdb_export.py 改动(会话初 git status 有 M,
   现已提交——先读现状)。

## Acceptance Criteria

- [x] 微信图片消息在 3 级工作台渲染出真图(Phase1 引擎 29e7bb37:image 行
      出条目+media scan 解密回填 image_files;Phase2 1b147007:气泡槽
      FeedLocalImages + feed_images.rs 双授权根 images/+media-cache)
- [x] 解密失败/未配置/文件缺失 = 结构化降级(占位「[图片]」条目仍在;wxgf
      后缀放行但魔数拒授权 → UI 人话降级「图片不可预览」)
- [x] 私有数据红线:引擎日志形状级;测试全合成路径;media-cache 不进 git
- [x] 门禁全绿(tests/engines 827 + vitest 943 + tsc + cargo feed_images 5)
- [x] 打包覆盖安装(见下方执行记录)
- [ ] 主人真机看图终验(装机后开 feed 微信渠道 3 级;首轮采集解密可分钟级,
      稳态缓存秒回)

## 执行记录

- Phase1(29e7bb37):engine.py 图片行占位+media scan 回填+300s 超时地板。
- Phase2(1b147007):feed_images.rs 双授权根(canonicalize 囚禁+魔数门,
  wxgf 天然拒);气泡槽 tg|wx 通用;并行会话 5 个基线件(feed_images.rs/
  feed-local-images/main.rs 挂载/tauri.conf CSP/feed-screen)自洽入树,
  出处已在提交信息注记——若并行会话后续提交撞同文件,以内容等价收编论,
  交主人仲裁。

## 边界

- 视频渲染不在本档(视频=明文直读,后续按需);wxgf 实况容器如实占位
  「实况格式,暂不支持预览」。

> 2026-10-19 主会话收尾注:未勾 AC(真机看图)维持主人目验本意。尝试记录:装机 app 在跑但无窗(后台态),冒烟实例抢单例槽有假警前科(10-11)故未强起;数据根 images/ 两 PNG 系 10-03 视觉线产物,微信媒体 image_files 指向另径,未深挖(并行线领域);fixture 冒烟(desktop/scripts/feed-images-smoke.py,在途未跟踪)可作自动化代理。

> 2026-10-20 真机回归定位与修复:截图「看不了」= 缓存图严格解码失败。根因
> `scripts/wechat-bridge-mediadecrypt.py` 把 V2 AES 段的 PKCS7 整块(1024
> 对齐时补满 16 字节密文)当作中段明文透传;实测 2000 个 V2 样本中 1990 个
> 密文长 = `(aes_size // 16 + 1) * 16`,与旧假设相反。已改为 PKCS7 去填充
> + 长度自洽校验(`_aes_plain_unpad`),回归测试 35 项全绿;36 个既有缓存按
> 原缓存键用修正脚本重解覆盖(29 个坏图全部转为严格可解,旧件备份在
> `wechat-localdb/media-cache-pre-pkcs7-fix-20261020-074706/`)。解密件由桥
> 按配置路径直接 spawn,无需重装 app;待主人重开 feed 微信渠道 3 级目验。
>
> 2026-10-20 08:00 换装与复拉:07:52 构建 exit 0 → 旧包备份
> `/tmp/世事.app.bak-20261020-075620` → ditto 换装 `/Applications/世事.app`
> (v0.0.6,ad-hoc 重签 + strict verify 过)→ 清 WKWebView 缓存 →
> `open -g` 静默拉起(MYIA 43055 / sidecar 43061,主窗 onscreen)。手动复拉
> 两线:weixin-ai-token run 9137(39 入/28 新,新图
> `media-cache/93617a231eb511b8.jpg` 210×237 严格可解)、weixin run 9141
> (50 入/10 新,零图);昨日条目 8834 的 `dc0e4f0a6e9e5843.jpg` 复验
> 180×102 可解。推送 archive-only 零外发、enrich 关。像素终验仍归主人:
> 新图在「今天 28 条」按新→旧第 18 条(当前视口下方约 8 泡),或看昨日
> 19:02 那条;本会话无辅助功能权限,不代滚动。

> 2026-10-20 点击放大增量:主人真机目验图已可见后问「微信图片不能点击
> 放大?」——旧交互仅图下「查看原尺寸」内联展开,窄气泡列里只能横向滚。
> 改为点击缩略图直接弹整屏模态大图(feed-local-images.tsx:缩略图包进
> button + 复用自研 Dialog 整屏画布 data-fullcanvas 范式,ESC/遮罩/右上角
> 标三途可关;旧内联按钮退役)。气泡/展开行/详情弹窗三处用图点一次全享。
> 门禁:scoped vitest 226 + 全量 959 + tsc/vite build 全绿。10:07 重建包
> (二进制内含 DTwhPUPU 资源块验源)→ 10:14 静默换装(旧包备份
> /tmp/世事.app.bak-20261020-101441,ad-hoc 重签 strict verify 过,清
> WKWebView 缓存,open -g 复起 MYIA 30084/sidecar 30090)。夹具冒烟同步
> 改弹窗语义并过(键盘放大/四档视口适配/ESC 关/零 pageerror),截图中心
> 像素 (70,123,145) 命中夹具色、大图占画面 25% = contain 理论值,像素级
> 实锤。待主人真机复验点击放大。
